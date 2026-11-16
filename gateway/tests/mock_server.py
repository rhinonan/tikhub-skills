#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""仅测试用的本地假验付服务，不进入生产镜像。

用法（在项目根目录另开终端）：
    MOCK_UPSTREAM=1 python tests/mock_server.py
然后运行：
    python smoke_test.py

它通过 monkeypatch 替换 verify/confirm/sign，生产 server.py 本身没有 mock 分支。
"""
import base64
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import alipay_a2m


def _decode(value: str) -> dict:
    pad = 4 - len(value) % 4
    if pad != 4:
        value += "=" * pad
    return json.loads(base64.urlsafe_b64decode(value).decode("utf-8"))


def fake_verify(payment_proof: str, trade_no: str, client_session: str = "") -> dict:
    data = _decode(payment_proof)
    return {
        "code": "10000",
        "active": True,
        "trade_no": trade_no,
        "out_trade_no": data["out_trade_no"],
        "amount": data["amount"],
        "resource_id": data["resource_id"],
    }


def fake_confirm(trade_no: str) -> bool:
    return True


def fake_sign(fields: dict) -> str:
    return "TEST_ONLY_SIGNATURE"


alipay_a2m.verify_payment = fake_verify
alipay_a2m.confirm_fulfillment = fake_confirm
alipay_a2m.sign_bill = fake_sign

import server  # noqa: E402  (必须在 monkeypatch 之后导入)

if __name__ == "__main__":
    server.main()
