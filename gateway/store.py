#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""订单与账户存储。

A2M 对幂等的要求很高，这里的几条硬规则：
  - out_trade_no 唯一，一单只存在一份
  - 同一 trade_no 只能被履约一次
  - 资源生成是原子的：进入 PENDING_CONFIRM 后绝不重新执行上游
  - 额度扣减用条件更新，避免并发下扣成负数
"""
import json
import os
import sqlite3
import threading
import time
import uuid

_lock = threading.RLock()
_conn = None
_conn_path = None
# 同一订单的履约必须串行：数据库事务只覆盖认领和落结果，
# 不覆盖中间的上游调用，并发重试会各跑一遍 producer。
_order_locks = {}
_order_locks_guard = threading.Lock()


def _order_lock(out_trade_no: str) -> threading.Lock:
    with _order_locks_guard:
        lock = _order_locks.get(out_trade_no)
        if lock is None:
            lock = threading.Lock()
            _order_locks[out_trade_no] = lock
        return lock

SCHEMA = """
CREATE TABLE IF NOT EXISTS orders (
    out_trade_no   TEXT PRIMARY KEY,
    kind           TEXT NOT NULL,              -- task | recharge
    resource_id    TEXT NOT NULL,
    goods_name     TEXT NOT NULL,
    amount         TEXT NOT NULL,
    currency       TEXT NOT NULL DEFAULT 'CNY',
    payload_json   TEXT,                       -- 原始请求快照，重试时以它为准
    credits        INTEGER NOT NULL DEFAULT 0,
    status         TEXT NOT NULL,              -- PENDING_PAYMENT | PAID | FULFILLED | REFUNDED
    fulfill_status TEXT NOT NULL,              -- UNFULFILLED | PENDING_CONFIRM | FULFILLED
    trade_no       TEXT,
    result_json    TEXT,
    pay_before     TEXT NOT NULL,
    created_at     TEXT NOT NULL,
    updated_at     TEXT NOT NULL
);
CREATE UNIQUE INDEX IF NOT EXISTS ux_orders_trade_no
    ON orders(trade_no) WHERE trade_no IS NOT NULL;

CREATE TABLE IF NOT EXISTS accounts (
    token       TEXT PRIMARY KEY,
    credits     INTEGER NOT NULL DEFAULT 0,
    created_at  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS ledger (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    token       TEXT NOT NULL,
    delta       INTEGER NOT NULL,
    reason      TEXT NOT NULL,
    ref         TEXT NOT NULL,
    created_at  TEXT NOT NULL,
    UNIQUE(token, ref, reason)
);

CREATE TABLE IF NOT EXISTS calls (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    token       TEXT,
    platform    TEXT,
    path        TEXT,
    unit_cost   INTEGER NOT NULL,
    status      TEXT NOT NULL,
    created_at  TEXT NOT NULL
);
"""


def now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime())


def init(db_path: str) -> None:
    global _conn, _conn_path
    with _lock:
        if _conn is not None and _conn_path == db_path:
            return
        parent = os.path.dirname(os.path.abspath(db_path))
        os.makedirs(parent, exist_ok=True)
        _conn = sqlite3.connect(db_path, check_same_thread=False)
        _conn.row_factory = sqlite3.Row
        _conn.execute("PRAGMA journal_mode=WAL")
        _conn.execute("PRAGMA foreign_keys=ON")
        _conn.executescript(SCHEMA)
        _conn.commit()
        _conn_path = db_path


def _db() -> sqlite3.Connection:
    if _conn is None:
        raise RuntimeError("store 未初始化，先调 init(db_path)")
    return _conn


# ---------------------------------------------------------------- 订单

def create_order(kind: str, resource_id: str, goods_name: str, amount: str,
                 pay_before: str, payload: dict = None, credits: int = 0) -> str:
    out_trade_no = "SK" + time.strftime("%Y%m%d%H%M%S") + uuid.uuid4().hex[:10].upper()
    ts = now_iso()
    with _lock:
        _db().execute(
            "INSERT INTO orders (out_trade_no, kind, resource_id, goods_name, amount, "
            "payload_json, credits, status, fulfill_status, pay_before, created_at, updated_at) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (out_trade_no, kind, resource_id, goods_name, amount,
             json.dumps(payload or {}, ensure_ascii=False), credits,
             "PENDING_PAYMENT", "UNFULFILLED", pay_before, ts, ts))
        _db().commit()
    return out_trade_no


def find_order(out_trade_no: str):
    with _lock:
        row = _db().execute("SELECT * FROM orders WHERE out_trade_no=?",
                            (out_trade_no,)).fetchone()
    return dict(row) if row else None


def mark_paid(out_trade_no: str, trade_no: str) -> None:
    ts = now_iso()
    with _lock:
        _db().execute(
            "UPDATE orders SET status='PAID', trade_no=?, updated_at=? "
            "WHERE out_trade_no=? AND status='PENDING_PAYMENT'",
            (trade_no, ts, out_trade_no))
        _db().commit()


def prepare_fulfillment(out_trade_no: str, trade_no: str, producer) -> dict:
    """同一订单串行履约，避免并发重试重复执行 producer。"""
    with _order_lock(out_trade_no):
        return _prepare_fulfillment(out_trade_no, trade_no, producer)


def _prepare_fulfillment(out_trade_no: str, trade_no: str, producer) -> dict:
    """原子地把订单推进到 PENDING_CONFIRM 并只生成一次资源。

    已经处于 PENDING_CONFIRM / FULFILLED 且有结果的订单直接返回已存结果，
    不会再次执行 producer —— 这是防重复扣费/重复调上游的关键。

    两种异常情况必须能自愈，否则用户付了钱永远拿不到货：
      - producer 抛错、或结果无法序列化 → 回退 UNFULFILLED，允许重试
      - 进程在「已认领」和「已存结果」之间崩溃 → 下次请求重新执行
    """
    ts = now_iso()
    with _lock:
        db = _db()
        db.execute("BEGIN IMMEDIATE")
        try:
            row = db.execute("SELECT * FROM orders WHERE out_trade_no=?",
                             (out_trade_no,)).fetchone()
            if row is None:
                db.execute("ROLLBACK")
                return {"state": "MISSING"}

            fulfill = row["fulfill_status"]
            has_result = bool(row["result_json"])

            if fulfill == "FULFILLED" and has_result:
                db.execute("ROLLBACK")
                return {"state": "FULFILLED",
                        "service_result": json.loads(row["result_json"])}
            if fulfill == "PENDING_CONFIRM" and has_result:
                db.execute("ROLLBACK")
                return {"state": "PENDING_CONFIRM",
                        "service_result": json.loads(row["result_json"])}

            # 认领订单：之后即使进程崩了，重试也会走到下面重新执行
            db.execute(
                "UPDATE orders SET fulfill_status='PENDING_CONFIRM', trade_no=?, "
                "result_json=NULL, status='PAID', updated_at=? WHERE out_trade_no=?",
                (trade_no, ts, out_trade_no))
            db.commit()
        except Exception:
            try:
                db.execute("ROLLBACK")
            except Exception:
                pass
            raise

        try:
            result = producer()
            # 序列化也放在这里：结果不可存同样算失败，必须能回退重试
            result_json = json.dumps(result, ensure_ascii=False)
        except Exception:
            db.execute(
                "UPDATE orders SET fulfill_status='UNFULFILLED', updated_at=? "
                "WHERE out_trade_no=?", (now_iso(), out_trade_no))
            db.commit()
            raise

        db.execute(
            "UPDATE orders SET result_json=?, updated_at=? WHERE out_trade_no=?",
            (result_json, now_iso(), out_trade_no))
        db.commit()
        return {"state": "PENDING_CONFIRM", "service_result": result}


def mark_fulfilled(out_trade_no: str) -> None:
    with _lock:
        _db().execute(
            "UPDATE orders SET fulfill_status='FULFILLED', status='FULFILLED', updated_at=? "
            "WHERE out_trade_no=?", (now_iso(), out_trade_no))
        _db().commit()


def mark_refunded(out_trade_no: str) -> None:
    with _lock:
        _db().execute(
            "UPDATE orders SET status='REFUNDED', updated_at=? WHERE out_trade_no=?",
            (now_iso(), out_trade_no))
        _db().commit()


# ---------------------------------------------------------------- 账户

def issue_account(credits: int, ref: str) -> str:
    token = "sk_" + uuid.uuid4().hex
    with _lock:
        _db().execute("INSERT INTO accounts (token, credits, created_at) VALUES (?,?,?)",
                      (token, 0, now_iso()))
        _db().commit()
    if credits:
        add_credits(token, credits, ref)
    return token


def get_credits(token: str) -> int:
    with _lock:
        row = _db().execute("SELECT credits FROM accounts WHERE token=?", (token,)).fetchone()
    return int(row["credits"]) if row else 0


def add_credits(token: str, delta: int, ref: str, reason: str = "purchase") -> bool:
    """入账。同一 (token, ref, reason) 只生效一次，防止同一订单重复加额度。"""
    with _lock:
        db = _db()
        try:
            db.execute("INSERT INTO ledger (token, delta, reason, ref, created_at) "
                       "VALUES (?,?,?,?,?)", (token, delta, reason, ref, now_iso()))
        except sqlite3.IntegrityError:
            return False
        db.execute("UPDATE accounts SET credits = credits + ? WHERE token=?", (delta, token))
        db.commit()
    return True


def take_credits(token: str, cost: int, ref: str) -> bool:
    """条件扣减：额度不足则整笔失败，不会扣成负数。"""
    with _lock:
        db = _db()
        cur = db.execute(
            "UPDATE accounts SET credits = credits - ? WHERE token=? AND credits >= ?",
            (cost, token, cost))
        if cur.rowcount == 0:
            db.commit()
            return False
        db.execute("INSERT OR IGNORE INTO ledger (token, delta, reason, ref, created_at) "
                   "VALUES (?,?,?,?,?)", (token, -cost, "consume", ref, now_iso()))
        db.commit()
    return True


def log_call(token: str, platform: str, path: str, unit_cost: int, status: str) -> None:
    with _lock:
        _db().execute("INSERT INTO calls (token, platform, path, unit_cost, status, created_at) "
                      "VALUES (?,?,?,?,?,?)",
                      (token, platform, path, unit_cost, status, now_iso()))
        _db().commit()
