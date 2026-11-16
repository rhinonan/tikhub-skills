#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""支付宝 A2M 协议：账单签发、凭证解析、验付、履约确认。

只实现 AI 按量付费需要的两个接口：
    alipay.aipay.agent.payment.verify
    alipay.aipay.agent.fulfillment.confirm
不涉及网页/APP 收款的统一收单与异步通知。
"""
import base64
import json
import time
from datetime import datetime, timedelta

from config import cfg

SIGN_KEYS = ["amount", "currency", "goods_name", "out_trade_no",
             "pay_before", "resource_id", "seller_id", "service_id"]


class AlipayError(RuntimeError):
    pass


# ---------------------------------------------------------------- 编码

def b64url_encode(raw) -> str:
    if isinstance(raw, str):
        raw = raw.encode("utf-8")
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("utf-8")


def b64url_decode(text: str) -> str:
    pad = 4 - len(text) % 4
    if pad != 4:
        text += "=" * pad
    return base64.urlsafe_b64decode(text).decode("utf-8")


# ---------------------------------------------------------------- 签名

def _sign_content(fields: dict) -> str:
    parts = [f"{k}={fields[k]}" for k in SIGN_KEYS
             if fields.get(k) not in (None, "")]
    return "&".join(parts)


def sign_bill(fields: dict) -> str:
    """商家本地签名，不请求支付宝服务端。"""
    content = _sign_content(fields)

    if not cfg.ALIPAY_PRIVATE_KEY:
        raise AlipayError("缺少 ALIPAY_PRIVATE_KEY，无法生成账单签名")

    try:
        from Crypto.Hash import SHA256
        from Crypto.PublicKey import RSA
        from Crypto.Signature import pkcs1_15
    except ImportError as exc:
        raise AlipayError("缺少 pycryptodome，无法签名：pip install pycryptodome") from exc

    key_der = base64.b64decode(cfg.ALIPAY_PRIVATE_KEY, validate=True)
    key = RSA.import_key(key_der)
    signature = pkcs1_15.new(key).sign(SHA256.new(content.encode("utf-8")))
    return base64.b64encode(signature).decode("utf-8")


# ---------------------------------------------------------------- 账单

def pay_before_iso() -> str:
    """出单时算一次，账单和本地订单共用同一个截止时间。"""
    return (datetime.now().astimezone()
            + timedelta(minutes=cfg.PAY_BEFORE_MINUTES)).isoformat()


def build_bill(out_trade_no: str, amount: str, resource_id: str,
               goods_name: str, service_id: str, pay_before: str) -> str:
    fields = {
        "amount": amount,
        "currency": "CNY",
        "goods_name": goods_name,
        "out_trade_no": out_trade_no,
        "pay_before": pay_before,
        "resource_id": resource_id,
        "seller_id": cfg.SELLER_ID,
        "service_id": service_id,
    }
    bill = {
        "protocol": {
            "out_trade_no": out_trade_no,
            "amount": amount,
            "currency": "CNY",
            "resource_id": resource_id,
            "pay_before": pay_before,
            "seller_signature": sign_bill(fields),
            "seller_sign_type": "RSA2",
            "seller_unique_id": cfg.SELLER_ID,
        },
        "method": {
            "seller_name": cfg.SELLER_NAME,
            "seller_id": cfg.SELLER_ID,
            "seller_app_id": cfg.SELLER_APP_ID,
            "goods_name": goods_name,
            "seller_unique_id_key": "seller_id",
            "service_id": service_id,
        },
    }
    return b64url_encode(json.dumps(bill, ensure_ascii=False))


def service_id_of(env_name: str) -> str:
    import os
    return os.environ.get(env_name, "").strip() or "api_mock_service_id"


# 支付宝按「服务」登记单价，一个 serviceId 只能对应一个价。
# 所以映射键必须是金额，不能是档位名——任务包和额度包的价钱各不相同。
SERVICE_ENV_BY_AMOUNT = {
    "0.10": "SERVICE_ID_STANDARD",   # 普通查询
    "0.50": "SERVICE_ID_PREMIUM",    # 指数/星图
    "2.00": "SERVICE_ID_BATCH",      # 批量
    "1.99": "SERVICE_ID_TASK",       # 任务包
    "9.90": "SERVICE_ID_PACK",       # 额度包
}


def service_id_for(amount: str) -> str:
    """按账单金额取对应的 serviceId，保证账单金额与登记单价一致。"""
    env = SERVICE_ENV_BY_AMOUNT.get(f"{float(amount):.2f}")
    if not env:
        print(f"[warn] 金额 {amount} 没有对应的 serviceId 登记，回落到沙箱标识")
        return "api_mock_service_id"
    return service_id_of(env)


# ---------------------------------------------------------------- 凭证

def parse_proof(header_value: str) -> dict:
    """解出验付需要的最小字段；任何异常都交给调用方按 402 处理。"""
    try:
        payload = json.loads(b64url_decode(header_value))
    except Exception as exc:
        raise AlipayError(f"Payment-Proof 解析失败: {exc}") from exc

    protocol = payload.get("protocol") or {}
    method = payload.get("method") or {}
    proof = (protocol.get("payment_proof") or "").strip()
    trade_no = (protocol.get("trade_no") or "").strip()
    out_trade_no = (protocol.get("out_trade_no") or "").strip()
    if not proof or not trade_no:
        raise AlipayError("Payment-Proof 缺少 payment_proof / trade_no")
    return {
        "payment_proof": proof,
        "trade_no": trade_no,
        "out_trade_no": out_trade_no,
        "client_session": (method.get("client_session") or "").strip(),
    }


# ---------------------------------------------------------------- 验付

def verify_payment(payment_proof: str, trade_no: str, client_session: str = "") -> dict:
    try:
        from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
        from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
        from alipay.aop.api.domain.AlipayAipayAgentPaymentVerifyModel import (
            AlipayAipayAgentPaymentVerifyModel)
        from alipay.aop.api.request.AlipayAipayAgentPaymentVerifyRequest import (
            AlipayAipayAgentPaymentVerifyRequest)
    except ImportError as exc:
        raise AlipayError("缺少 alipay-sdk-python：pip install alipay-sdk-python") from exc

    conf = AlipayClientConfig()
    conf.server_url = cfg.ALIPAY_GATEWAY
    conf.app_id = cfg.SELLER_APP_ID
    conf.app_private_key = cfg.ALIPAY_PRIVATE_KEY
    conf.alipay_public_key = cfg.ALIPAY_PUBLIC_KEY
    conf.charset = "utf-8"
    conf.sign_type = "RSA2"
    client = DefaultAlipayClient(alipay_client_config=conf)

    model = AlipayAipayAgentPaymentVerifyModel()
    model.payment_proof = payment_proof
    model.trade_no = trade_no
    if client_session:
        model.client_session = client_session
    request = AlipayAipayAgentPaymentVerifyRequest()
    request.biz_model = model

    raw = json.loads(client.execute(request))
    return raw.get("alipay_aipay_agent_payment_verify_response", raw)


def confirm_fulfillment(trade_no: str) -> bool:
    try:
        from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
        from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
        from alipay.aop.api.domain.AlipayAipayAgentFulfillmentConfirmModel import (
            AlipayAipayAgentFulfillmentConfirmModel)
        from alipay.aop.api.request.AlipayAipayAgentFulfillmentConfirmRequest import (
            AlipayAipayAgentFulfillmentConfirmRequest)
    except ImportError as exc:
        raise AlipayError("缺少 alipay-sdk-python：pip install alipay-sdk-python") from exc

    conf = AlipayClientConfig()
    conf.server_url = cfg.ALIPAY_GATEWAY
    conf.app_id = cfg.SELLER_APP_ID
    conf.app_private_key = cfg.ALIPAY_PRIVATE_KEY
    conf.alipay_public_key = cfg.ALIPAY_PUBLIC_KEY
    conf.charset = "utf-8"
    conf.sign_type = "RSA2"
    client = DefaultAlipayClient(alipay_client_config=conf)

    model = AlipayAipayAgentFulfillmentConfirmModel()
    model.trade_no = trade_no
    request = AlipayAipayAgentFulfillmentConfirmRequest()
    request.biz_model = model

    raw = json.loads(client.execute(request))
    resp = raw.get("alipay_aipay_agent_fulfillment_confirm_response", raw)
    return resp.get("code") == "10000"


def now_ts() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime())
