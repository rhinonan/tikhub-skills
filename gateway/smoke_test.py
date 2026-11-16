#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""全链路自测：402 → 支付 → 重试 → 履约 → 数据。

先启动网关（另开终端）：python server.py
再运行：            python smoke_test.py
"""
import json
import os
import sys
import urllib.error
import urllib.request

import mock_pay

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8088"
passed, failed = [], []


def decode_bill(headers):
    v = headers.get("Payment-Needed")
    if not v:
        return None
    pad = 4 - len(v) % 4
    if pad != 4:
        v += "=" * pad
    import base64
    return json.loads(base64.urlsafe_b64decode(v).decode())


def expect_svc(env_name):
    """支付宝一个 serviceId 只对应一个价，所以按金额取；未配置时回落沙箱标识。"""
    return os.environ.get(env_name) or "api_mock_service_id"


def request(path, body=None, headers=None):
    data = json.dumps(body, ensure_ascii=False).encode() if body is not None else b"{}"
    hdrs = {"Content-Type": "application/json"}
    hdrs.update(headers or {})
    req = urllib.request.Request(BASE + path, data=data, headers=hdrs, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, dict(resp.headers), json.loads(resp.read().decode())
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", "replace")
        try:
            payload = json.loads(raw)
        except Exception:
            payload = {"raw": raw}
        return exc.code, dict(exc.headers), payload


def check(name, cond, detail=""):
    if cond:
        passed.append(name)
        print(f"  [OK]   {name}")
    else:
        failed.append(name)
        print(f"  [!]    {name}  {detail}")


def pay_and_retry(path, body, headers=None):
    """不带凭证 → 402 → 模拟支付 → 带凭证重试。"""
    st, hdrs, payload = request(path, body, headers)
    needed = hdrs.get("Payment-Needed")
    if st != 402 or not needed:
        return None, st, payload, hdrs
    proof = mock_pay.make_proof(needed)
    h = dict(headers or {})
    h["Payment-Proof"] = proof
    st2, hdrs2, payload2 = request(path, body, h)
    return proof, st2, payload2, hdrs2


print(f"\n== 网关自测 {BASE} ==\n")

# ---------------------------------------------------------------- 1. 任务包
print("[1] 任务包：抖音账号分析")
body = {"task": "douyin_account_analysis", "params": {"unique_id": "test_user"}}
st, hdrs, payload = request("/v1/task", body)
check("未付款返回 402", st == 402, f"实际 {st}")
check("402 带 Payment-Needed 头", bool(hdrs.get("Payment-Needed")))
check("账单金额 = 1.99", str(payload.get("amount")) == "1.99", str(payload.get("amount")))
check("账单商品名正确", bool(payload.get("goods_name")), str(payload))
bill_task = decode_bill(hdrs)
check("任务包使用 ¥1.99 对应的 serviceId",
      (bill_task or {}).get("method", {}).get("service_id") == expect_svc("SERVICE_ID_TASK"),
      str((bill_task or {}).get("method")))
check("账单金额与订单金额一致",
      (bill_task or {}).get("protocol", {}).get("amount") == "1.99")

proof, st, payload, hdrs = pay_and_retry("/v1/task", body)
check("付款后返回 200", st == 200, f"实际 {st} {payload}")
data = (payload or {}).get("data") or {}
check("任务执行了 2 步", data.get("steps") == 2, str(data.get("steps")))
results = data.get("results") or []
if len(results) == 2:
    step2 = results[1].get("data") or {}
    check("第二步拿到数据", bool(step2.get("aweme_list")), str(step2)[:160])
    echo = step2.get("echo") or {}
    check("步骤间字段引用生效（sec_uid 来自第一步）",
          echo.get("sec_user_id") == "MS4wLjABAAAAmock_sec_uid", str(echo))
check("返回 Payment-Validation 头", bool((hdrs or {}).get("Payment-Validation")))

if proof:
    st3, _, payload3 = request("/v1/task", body, {"Payment-Proof": proof})
    check("同凭证重试返回 200", st3 == 200, f"实际 {st3}")
    check("同凭证重试标记 already_fulfilled",
          (payload3 or {}).get("already_fulfilled") is True, str(payload3)[:140])
    check("同凭证重试订单号一致",
          (payload3 or {}).get("out_trade_no") == (payload or {}).get("out_trade_no"))

# ---------------------------------------------------------------- 2. 额度包
print("\n[2] 额度包：充值后按次调用")
st, hdrs, payload = request("/v1/recharge", {"pack": "starter"})
check("未付款返回 402", st == 402, f"实际 {st}")
check("额度包金额 = 9.90", str(payload.get("amount")) == "9.90", str(payload.get("amount")))
bill_pack = decode_bill(hdrs)
check("额度包使用 ¥9.90 对应的 serviceId",
      (bill_pack or {}).get("method", {}).get("service_id") == expect_svc("SERVICE_ID_PACK"),
      str((bill_pack or {}).get("method")))
check("额度包与任务包用的是不同 serviceId",
      (bill_pack or {}).get("method", {}).get("service_id")
      != (bill_task or {}).get("method", {}).get("service_id")
      or expect_svc("SERVICE_ID_TASK") == expect_svc("SERVICE_ID_PACK"))

proof_r, st, payload, _ = pay_and_retry("/v1/recharge", {"pack": "starter"})
check("充值付款后 200", st == 200, f"实际 {st} {payload}")
token = ((payload or {}).get("data") or {}).get("token")
check("拿到账户 token", bool(token))

if proof_r and token:
    _, _, payload_dup = request("/v1/recharge", {"pack": "starter"},
                                {"Payment-Proof": proof_r})
    check("重复提交同一充值不发新账户",
          ((payload_dup or {}).get("data") or {}).get("token") == token, str(payload_dup)[:140])

# ---------------------------------------------------------------- 3. 按次调用
print("\n[3] 按次调用与分档计费")
call_body = {"platform": "douyin", "path": "/api/v1/douyin/web/fetch_one_video",
             "query": {"aweme_id": "7300000000000000001"}}
st, _, payload = request("/v1/call", call_body)
check("无 token 时返回 402", st == 402, f"实际 {st}")

st, _, payload = request("/v1/call", call_body, {"Authorization": f"Bearer {token}"})
check("有余额返回 200", st == 200, f"实际 {st} {payload}")
meta = (payload or {}).get("meta") or {}
check("标准端点扣 1 额度", meta.get("unit_cost") == 1, str(meta))
check("余额变为 199", meta.get("credits_left") == 199, str(meta))

batch_body = {"platform": "douyin",
              "path": "/api/v1/douyin/web/fetch_multi_video", "body": {}}
_, _, payload = request("/v1/call", batch_body, {"Authorization": f"Bearer {token}"})
meta = (payload or {}).get("meta") or {}
check("批量端点扣 20 额度", meta.get("unit_cost") == 20, str(meta))
check("余额变为 179", meta.get("credits_left") == 179, str(meta))

premium_body = {"platform": "douyin",
                "path": "/api/v1/douyin/index/fetch_index_data"}
_, _, payload = request("/v1/call", premium_body, {"Authorization": f"Bearer {token}"})
meta = (payload or {}).get("meta") or {}
check("指数端点扣 5 额度", meta.get("unit_cost") == 5, str(meta))
check("余额变为 174", meta.get("credits_left") == 174, str(meta))

# ---------------------------------------------------------------- 4. 边界
print("\n[4] 边界：余额耗尽与无效凭证")
# 纯走接口把余额烧干：批量端点一次扣 20，比一次扣 1 快得多
drain_body = {"platform": "douyin", "path": "/api/v1/douyin/web/fetch_multi_video", "body": {}}
st = 200
for _ in range(20):
    st, _, _ = request("/v1/call", drain_body, {"Authorization": f"Bearer {token}"})
    if st != 200:
        break
check("余额耗尽后回到 402", st == 402, f"实际 {st}")

st, _, _ = request("/v1/task", body, {"Payment-Proof": "eyJwcm90b2NvbCI6e30sIm1ldGhvZCI6e319"})
check("无效凭证仍返回 402", st == 402, f"实际 {st}")

st, _, payload = request("/v1/task", {"task": "not_exists", "params": {}})
check("未知任务返回 400", st == 400, f"实际 {st}")

st, _, payload = request("/v1/task", {"task": "douyin_account_analysis", "params": {}})
check("缺参数返回 400", st == 400, f"实际 {st}")

# ---------------------------------------------------------------- 5. 安全
print("\n[5] 安全：凭证不能跨资源使用")
if proof and proof_r:
    st, _, payload = request("/v1/recharge", {"pack": "starter"}, {"Payment-Proof": proof})
    check("任务包凭证不能拿去换额度包", st == 402, f"实际 {st}")
    st, _, payload = request("/v1/task", body, {"Payment-Proof": proof_r})
    check("额度包凭证不能拿去换任务数据", st == 402, f"实际 {st}")

# ---------------------------------------------------------------- 汇总
print(f"\n== 结果：{len(passed)} 通过 / {len(failed)} 失败 ==")
if failed:
    for f in failed:
        print(f"  - {f}")
    sys.exit(1)
print("全部通过")
