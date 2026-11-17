#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""付费网关：统一 402 闸门 + 两级计价。

两种付费商品走同一套流程：
  /v1/task      任务包：一次付费，内部调 N 次上游
  /v1/recharge  额度包：一次付费，拿到账户 token，后续按余量按次调用

按次调用（/v1/call）用 Bearer token 计费；没 token 或余额不足时同样返回 402，
所以「未付款就返回 402」的语义对所有资源接口都成立。

启动： python server.py
"""
import hashlib
import json
import sys
import traceback
import uuid
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

import alipay_a2m as alipay
import pricing
import store
import upstream
from config import cfg

METER_REFUND_REASON = "upstream-failed"


class Reply:
    def __init__(self, status: int, body: dict, headers: dict = None):
        self.status = status
        self.body = body
        self.headers = headers or {}


def json_bytes(obj) -> bytes:
    return json.dumps(obj, ensure_ascii=False).encode("utf-8")


def amounts_equal(a, b) -> bool:
    try:
        return round(float(str(a).strip()), 2) == round(float(str(b).strip()), 2)
    except Exception:
        return False


def parse_time(text: str) -> float:
    try:
        return datetime.fromisoformat(text).timestamp()
    except Exception:
        return 0.0


# ---------------------------------------------------------------- 出单 / 402

def payment_required(order: dict) -> Reply:
    """用订单快照出单，保证重试时账单金额和截止时间都与订单一致。

    serviceId 按金额反查：支付宝一个 serviceId 只有一个登记价，
    用档位名去查会在任务包/额度包上对不上。
    """
    service_id = alipay.service_id_for(order["amount"])
    bill = alipay.build_bill(
        order["out_trade_no"], order["amount"], order["resource_id"],
        order["goods_name"], service_id, order["pay_before"])
    return Reply(402, {
        "code": "Payment-Needed",
        "message": "需要支付",
        "out_trade_no": order["out_trade_no"],
        "amount": order["amount"],
        "currency": "CNY",
        "goods_name": order["goods_name"],
    }, {"Payment-Needed": bill})


def new_order(kind: str, resource_id: str, amount: str, goods_name: str,
              payload: dict, credits: int = 0) -> dict:
    # 沙箱的 api_mock_service_id 只登记了 0.01 元，账单金额必须与登记价一致
    billing_amount = cfg.SANDBOX_AMOUNT if cfg.SANDBOX_MODE else amount
    oid = store.create_order(kind, resource_id, goods_name, billing_amount,
                             alipay.pay_before_iso(), payload, credits)
    return store.find_order(oid)


def validation_header(trade_no: str, out_trade_no: str, resource_id: str) -> str:
    return alipay.b64url_encode(json.dumps({
        "trade_no": trade_no,
        "out_trade_no": out_trade_no,
        "validated": True,
        "resource_id": resource_id,
    }, ensure_ascii=False))


# ---------------------------------------------------------------- 付费资源

def run_paid_resource(kind: str, resource_id: str, amount: str, goods_name: str,
                      payload: dict, producer_factory,
                      proof_header: str, credits: int = 0) -> Reply:
    """402 → 验付 → 履约 → 交付。task 与 recharge 共用这一条路径。"""

    # ① 没有凭证：出单
    if not proof_header or not proof_header.strip():
        return payment_required(
            new_order(kind, resource_id, amount, goods_name, payload, credits))

    # ② 解析凭证
    try:
        proof = alipay.parse_proof(proof_header)
    except alipay.AlipayError as exc:
        print(f"[warn] {exc}")
        return payment_required(
            new_order(kind, resource_id, amount, goods_name, payload, credits))

    # ③ 先按凭证自带的订单号定位；沙箱收银返回的 Payment-Proof 可能不带该字段，
    #    因此最终以验付响应的 out_trade_no 为准再查一次本地订单。
    order = store.find_order(proof["out_trade_no"]) if proof["out_trade_no"] else None
    if order is not None:
        # 凭证必须属于当前请求的资源，否则就是拿 A 的付款去换 B 的货
        if order["resource_id"] != resource_id:
            print(f"[warn] 凭证资源不符: 订单={order['resource_id']} 请求={resource_id}")
            return payment_required(
                new_order(kind, resource_id, amount, goods_name, payload, credits))
        if order["status"] == "REFUNDED":
            return Reply(409, {"code": "ORDER_REFUNDED", "message": "该订单已退款，请重新下单"})

    # ④ 验付
    try:
        resp = alipay.verify_payment(proof["payment_proof"], proof["trade_no"],
                                     proof["client_session"])
    except alipay.AlipayError as exc:
        print(f"[error] 验付异常: {exc}")
        return Reply(502, {"code": "VERIFY_ERROR", "message": str(exc)})

    if resp.get("code") != "10000" or resp.get("active") is not True:
        print(f"[warn] 验付未通过: {resp.get('sub_msg') or resp.get('code')}")
        return payment_required(
            order or new_order(kind, resource_id, amount, goods_name, payload, credits))

    # 验付响应的 out_trade_no 是权威订单号；缺失即拒绝
    verify_out_trade_no = (resp.get("out_trade_no") or "").strip()
    if not verify_out_trade_no:
        print("[warn] 验付响应缺少 out_trade_no，拒绝交付")
        return payment_required(
            order or new_order(kind, resource_id, amount, goods_name, payload, credits))

    if order is None:
        order = store.find_order(verify_out_trade_no)
        if order is None:
            print(f"[warn] 本地订单不存在: {verify_out_trade_no}")
            return payment_required(
                new_order(kind, resource_id, amount, goods_name, payload, credits))
        if order["resource_id"] != resource_id:
            print(f"[warn] 凭证资源不符: 订单={order['resource_id']} 请求={resource_id}")
            return payment_required(
                new_order(kind, resource_id, amount, goods_name, payload, credits))
        if order["status"] == "REFUNDED":
            return Reply(409, {"code": "ORDER_REFUNDED", "message": "该订单已退款，请重新下单"})
    elif verify_out_trade_no != order["out_trade_no"]:
        print("[warn] 验付 out_trade_no 与本地订单不一致，拒绝交付")
        return payment_required(order)

    service_id = alipay.service_id_for(order["amount"])
    exact_sandbox = cfg.is_exact_sandbox(service_id)

    returned_trade_no = (resp.get("trade_no") or "").strip()
    if exact_sandbox:
        returned_trade_no = returned_trade_no or proof["trade_no"]
    if not returned_trade_no or returned_trade_no != proof["trade_no"]:
        print("[warn] trade_no 不一致，拒绝交付")
        return payment_required(order)

    # 金额：生产环境必须校验，缺失即拒绝；仅严格沙箱允许用订单金额兜底
    verified_amount = resp.get("amount")
    if verified_amount in (None, ""):
        if not exact_sandbox:
            print("[error] 验付响应缺少金额，拒绝交付")
            return Reply(402, {"code": "Payment-Needed", "message": "验付响应异常，请重新支付"},
                         {"Payment-Needed": alipay.build_bill(
                             order["out_trade_no"], order["amount"], order["resource_id"],
                             order["goods_name"], service_id,
                             order["pay_before"])})
        verified_amount = order["amount"]

    if not amounts_equal(verified_amount, order["amount"]):
        print(f"[warn] 金额不一致: 验付={verified_amount} 订单={order['amount']}")
        return payment_required(order)

    # 资源归属：生产环境缺字段即拒绝，只有严格沙箱允许回退本地订单
    verified_resource = resp.get("resource_id") or (
        order["resource_id"] if exact_sandbox else "")
    if not verified_resource or verified_resource != order["resource_id"] \
            or order["resource_id"] != resource_id:
        print(f"[warn] resource_id 不一致: 验付={verified_resource} "
              f"订单={order['resource_id']} 请求={resource_id}")
        return payment_required(order)

    # 订单状态必须处于可履约区间，防止退款/异常状态被重放
    if order["currency"] != "CNY":
        return payment_required(order)
    if order["status"] not in ("PENDING_PAYMENT", "PAID", "FULFILLED"):
        print(f"[warn] 订单状态不可用: {order['status']}")
        return payment_required(order)
    if order["fulfill_status"] not in ("UNFULFILLED", "PENDING_CONFIRM", "FULFILLED"):
        return Reply(500, {"code": "FULFILL_STATE_ERROR", "message": "订单履约状态异常"})

    # 只有还没履约过的订单才检查支付有效期
    if order["fulfill_status"] == "UNFULFILLED":
        if parse_time(order["pay_before"]) and \
                datetime.now().timestamp() > parse_time(order["pay_before"]):
            return Reply(402, {"code": "Payment-Needed", "message": "订单已过期，请重新下单"},
                         {"Payment-Needed": alipay.build_bill(
                             order["out_trade_no"], order["amount"], order["resource_id"],
                             order["goods_name"], alipay.service_id_for(order["amount"]),
                             order["pay_before"])})

    # ⑤ 原子履约：已进入 PENDING_CONFIRM/FULFILLED 的订单不会再次执行 producer
    #    执行用订单里存档的参数，不用客户端重传的内容
    try:
        stored = json.loads(order["payload_json"] or "{}")
        result = store.prepare_fulfillment(order["out_trade_no"], returned_trade_no,
                                           lambda: producer_factory(stored)())
    except upstream.UpstreamError as exc:
        print(f"[warn] 资源生成失败（不履约，可重试）: {exc}")
        return Reply(502, {"code": "UPSTREAM_FAILED", "message": str(exc),
                           "retryable": exc.retryable})
    except Exception as exc:
        traceback.print_exc()
        return Reply(500, {"code": "FULFILL_PREPARE_FAILED", "message": str(exc)})

    state = result.get("state")
    service_result = result.get("service_result")
    if state == "MISSING" or service_result is None:
        return Reply(500, {"code": "FULFILL_STATE_ERROR", "message": "订单状态异常"})

    # ⑥ 履约确认：成功后才标记完成
    if state != "FULFILLED":
        try:
            ok = alipay.confirm_fulfillment(returned_trade_no)
        except alipay.AlipayError as exc:
            print(f"[error] 履约确认异常: {exc}")
            return Reply(502, {"code": "FULFILLMENT_CONFIRM_FAILED",
                               "message": "资源已生成但履约确认异常，请用同一凭证重试"})
        if not ok:
            return Reply(502, {"code": "FULFILLMENT_CONFIRM_FAILED",
                               "message": "资源已生成但履约确认失败，请用同一凭证重试"})
        store.mark_fulfilled(order["out_trade_no"])

    return Reply(200, {
        "code": 0,
        "resource_id": order["resource_id"],
        "content": service_result,
        "data": service_result,
        "out_trade_no": order["out_trade_no"],
        "trade_no": returned_trade_no,
        "already_fulfilled": state == "FULFILLED",
    }, {"Payment-Validation": validation_header(
        returned_trade_no, order["out_trade_no"], order["resource_id"])})


# ---------------------------------------------------------------- 业务

def do_recharge(pack_name: str, proof_header: str) -> Reply:
    pack = pricing.CREDIT_PACKS.get(pack_name)
    if pack is None:
        return Reply(400, {"code": "BAD_PACK", "message": f"未知套餐: {pack_name}"})

    def producer_factory(payload):
        def produce():
            # 账户与入账都由订单履约驱动，重复执行也只会有一个账户
            return {"token": store.issue_account(pack["credits"], ref=uuid.uuid4().hex),
                    "credits": pack["credits"]}
        return produce

    return run_paid_resource(
        kind="recharge",
        resource_id=f"recharge:{pack_name}",
        amount=pack["amount"],
        goods_name=pack["goods_name"],
        payload={"pack": pack_name},
        producer_factory=producer_factory,
        proof_header=proof_header,
        credits=pack["credits"],
    )


def do_task(task_name: str, params: dict, proof_header: str) -> Reply:
    spec = pricing.TASKS.get(task_name)
    if spec is None:
        return Reply(400, {"code": "BAD_TASK", "message": f"未知任务: {task_name}"})

    missing = [k for k in spec.get("inputs", []) if not str(params.get(k, "")).strip()]
    if missing:
        return Reply(400, {"code": "MISSING_PARAM",
                           "message": f"缺少参数: {', '.join(missing)}"})

    def producer_factory(payload):
        def produce():
            params = payload.get("params") or {}
            steps_result = []
            for step in spec["steps"]:
                query = pricing.build_query(step, params, steps_result)
                steps_result.append(upstream.call(step["path"], step.get("method", "GET"), query))
            return {"task": task_name, "steps": len(steps_result), "results": steps_result}
        return produce

    return run_paid_resource(
        kind="task",
        resource_id=spec["resource_id"],
        amount=spec["amount"],
        goods_name=spec["goods_name"],
        payload={"task": task_name, "params": params},
        producer_factory=producer_factory,
        proof_header=proof_header,
    )


def do_call(token: str, body: dict, proof_header: str = "") -> Reply:
    path = str(body.get("path", "")).strip()
    if not path.startswith("/api/"):
        return Reply(400, {"code": "BAD_PATH", "message": "path 必须以 /api/ 开头"})

    tier = pricing.tier_of(path)

    # 已有余额：保持扣额度路径
    if token and store.get_credits(token) >= tier["credits"]:
        ref = f"call:{uuid.uuid4().hex}"
        if not store.take_credits(token, tier["credits"], ref):
            return do_recharge("starter", "")
        try:
            data = upstream.call(path, body.get("method", "GET"),
                                 body.get("query") or {}, body.get("body"))
        except upstream.UpstreamError as exc:
            # 上游失败不该让用户承担成本
            store.add_credits(token, tier["credits"], ref, reason=METER_REFUND_REASON)
            store.log_call(token, body.get("platform", ""), path, tier["credits"], "upstream_error")
            return Reply(502, {"code": "UPSTREAM_FAILED", "message": str(exc),
                               "retryable": exc.retryable, "credits_refunded": True})

        store.log_call(token, body.get("platform", ""), path, tier["credits"], "ok")
        return Reply(200, {
            "code": 0,
            "data": data,
            "meta": {"tier": tier["name"], "unit_cost": tier["credits"],
                     "credits_left": store.get_credits(token)},
        })

    # 无余额：按次直接 402 收款，金额取当前档位登记价。
    # 生产环境只有已登记 serviceId 的档位可售；未登记的档位明确拒绝，
    # 不回落 api_mock_service_id，也不拿别的价档顶替。
    if not cfg.SANDBOX_MODE and not cfg.MOCK_UPSTREAM \
            and not alipay.configured_service_id_for(tier["amount"]):
        return Reply(503, {"code": "TIER_NOT_AVAILABLE",
                           "message": f"{tier['name']} 档位暂未开通，请使用标准档接口"})

    method = str(body.get("method") or "GET").upper()
    query = body.get("query") or {}
    raw_body = body.get("body")
    # 资源标识绑定本次调用的实际参数，防止拿 A 的付款换 B 的查询结果
    fingerprint = hashlib.sha256(json.dumps(
        {"path": path, "method": method, "query": query, "body": raw_body},
        ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()[:16]

    def producer_factory(payload):
        def produce():
            return upstream.call(payload["path"], payload["method"],
                                 payload.get("query") or {}, payload.get("body"))
        return produce

    return run_paid_resource(
        kind="call",
        resource_id=f"call:{path}#{fingerprint}",
        amount=tier["amount"],
        goods_name=tier["goods_name"],
        payload={"path": path, "method": method, "query": query, "body": raw_body},
        producer_factory=producer_factory,
        proof_header=proof_header,
    )


# ---------------------------------------------------------------- HTTP

class Handler(BaseHTTPRequestHandler):
    server_version = "tikhub-skills-gateway/0.1"

    def _send(self, reply: Reply) -> None:
        raw = json_bytes(reply.body)
        self.send_response(reply.status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        for k, v in reply.headers.items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(raw)

    def _read_json(self) -> dict:
        length = int(self.headers.get("Content-Length") or 0)
        if not length:
            return {}
        try:
            return json.loads(self.rfile.read(length).decode("utf-8"))
        except Exception:
            return {}

    def _bearer_token(self) -> str:
        auth = self.headers.get("Authorization", "")
        return auth[7:].strip() if auth.lower().startswith("bearer ") else ""

    @staticmethod
    def _mask_token(token: str) -> str:
        return token[:6] + "…" + token[-4:] if len(token) > 12 else "***"

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        if path.startswith("/healthz"):
            self._send(Reply(200, {"ok": True, "sandbox_mode": cfg.SANDBOX_MODE,
                                   "mock_upstream": cfg.MOCK_UPSTREAM}))
            return
        if path in ("/v1/balance", "/v1/usage"):
            token = self._bearer_token()
            if not token or not store.account_exists(token):
                self._send(Reply(401, {"code": "UNAUTHORIZED",
                                       "message": "缺少或无效的账户 token"}))
                return
            payload = {"code": 0, **store.usage_summary(token),
                       "token": self._mask_token(token)}
            if path == "/v1/usage":
                try:
                    limit = int((parse_qs(parsed.query).get("limit") or ["20"])[0])
                except ValueError:
                    limit = 20
                limit = max(1, min(limit, 100))
                tier_name = {1: "standard", 5: "premium", 20: "batch"}
                calls = store.list_calls(token, limit)
                for c in calls:
                    c["tier"] = tier_name.get(c["unit_cost"], "custom")
                payload["calls"] = calls
            self._send(Reply(200, payload))
            return
        self._send(Reply(404, {"code": "NOT_FOUND", "message": "请用 POST"}))

    def do_POST(self):
        try:
            body = self._read_json()
            proof = self.headers.get("Payment-Proof", "")
            if self.path.startswith("/v1/recharge"):
                self._send(do_recharge(body.get("pack") or "starter", proof))
                return
            if self.path.startswith("/v1/task"):
                self._send(do_task(body.get("task", ""), body.get("params") or {}, proof))
                return
            if self.path.startswith("/v1/call"):
                auth = self.headers.get("Authorization", "")
                token = auth[7:].strip() if auth.lower().startswith("bearer ") else ""
                self._send(do_call(token, body, proof))
                return
            self._send(Reply(404, {"code": "NOT_FOUND"}))
        except Exception as exc:
            traceback.print_exc()
            self._send(Reply(500, {"code": "INTERNAL", "message": str(exc)}))

    def log_message(self, fmt, *args):
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))


def main():
    store.init(cfg.DB_PATH)
    for w in cfg.warn():
        print(f"[config] {w}")
    print(f"[gateway] listening on http://{cfg.HOST}:{cfg.PORT}  db={cfg.DB_PATH}")
    ThreadingHTTPServer((cfg.HOST, cfg.PORT), Handler).serve_forever()


if __name__ == "__main__":
    main()
