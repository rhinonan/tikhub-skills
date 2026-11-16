#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""联调用的买家侧支付模拟器（真实环境由 alipay-bot 承担）。

用法：
    python mock_pay.py <Payment-Needed 头的内容>

从 402 账单里读出订单号和金额，生成一个 Payment-Proof 头的内容打印出来，
把它塞回原请求的 Payment-Proof 头里重试即可。
仅用于 MOCK_ALIPAY=1 的本地联调。
"""
import json
import sys
import uuid

import alipay


def make_proof(payment_needed: str, trade_no: str = None) -> str:
    bill = json.loads(alipay.b64url_decode(payment_needed.strip()))
    protocol = bill.get("protocol") or {}
    method = bill.get("method") or {}

    out_trade_no = protocol.get("out_trade_no", "")
    if not out_trade_no:
        raise SystemExit("账单里没有 out_trade_no")

    protocol["payment_proof"] = "MOCKPROOF" + uuid.uuid4().hex
    protocol["trade_no"] = trade_no or ("2026MOCK" + uuid.uuid4().hex[:16].upper())
    method["client_session"] = "mock-session"

    print(f"# 订单: {out_trade_no}  金额: {protocol.get('amount')}  "
          f"商品: {method.get('goods_name')}", file=sys.stderr)
    return alipay.b64url_encode(json.dumps(
        {"protocol": protocol, "method": method}, ensure_ascii=False))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    print(make_proof(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None))
