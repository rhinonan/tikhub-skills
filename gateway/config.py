#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""网关配置：全部来自环境变量，代码里不出现任何密钥。

必填（生产）：
  SELLER_ID            卖家支付宝账号（2088 开头）
  SELLER_NAME          卖家名称，会出现在支付页
  SELLER_APP_ID        支付宝开放平台应用 AppID
  ALIPAY_PRIVATE_KEY   应用私钥（PKCS#1/PKCS#8 均可，字符串或文件路径）
  ALIPAY_PUBLIC_KEY    支付宝公钥（验签用）
  SERVICE_ID_*         支付宝登记的 serviceId，每档一个
  TIKHUB_API_KEY       TikHub 主 Key（也可从 ~/.workbuddy/tikhub_token 读）

开发/联调：
  MOCK_ALIPAY=1        跳过真实验付，用本地凭证直接放行
  MOCK_UPSTREAM=1      跳过真实 TikHub 调用，返回样例数据
"""
import os
import pathlib


def _env(name: str, default: str = "") -> str:
    return os.environ.get(name, default).strip()


def _env_bool(name: str, default: bool = False) -> bool:
    v = _env(name)
    if not v:
        return default
    return v.lower() in ("1", "true", "yes", "on")


def _read_key(value: str) -> str:
    """密钥支持两种给法：直接给内容，或给文件路径。"""
    if not value:
        return ""
    p = pathlib.Path(value).expanduser()
    if "\n" not in value and p.is_file():
        return p.read_text(encoding="utf-8").strip()
    return value


def _tikhub_key() -> str:
    key = _read_key(_env("TIKHUB_API_KEY"))
    if key:
        return key
    fallback = pathlib.Path.home() / ".workbuddy" / "tikhub_token"
    if fallback.is_file():
        return fallback.read_text(encoding="utf-8").strip()
    return ""


class Config:
    # ---- 运行模式 ----
    MOCK_ALIPAY = _env_bool("MOCK_ALIPAY", True)
    MOCK_UPSTREAM = _env_bool("MOCK_UPSTREAM", True)

    # ---- 基础 ----
    BASE_URL = _env("GATEWAY_BASE_URL", "http://127.0.0.1:8088").rstrip("/")
    DB_PATH = _env("DB_PATH",
                   str(pathlib.Path(__file__).parent / ".local" / "gateway.db"))
    HOST = _env("HOST", "127.0.0.1")
    PORT = int(_env("PORT", "8088") or 8088)

    # ---- 卖家身份 ----
    SELLER_ID = _env("SELLER_ID", "2088000000000000")
    SELLER_NAME = _env("SELLER_NAME", "社交数据服务")
    SELLER_APP_ID = _env("SELLER_APP_ID", "2021000000000000")

    # ---- 支付宝 ----
    ALIPAY_GATEWAY = _env("ALIPAY_GATEWAY", "https://openapi.alipay.com/gateway.do")
    ALIPAY_PRIVATE_KEY = _read_key(_env("ALIPAY_PRIVATE_KEY"))
    ALIPAY_PUBLIC_KEY = _read_key(_env("ALIPAY_PUBLIC_KEY"))

    # ---- 上游 ----
    TIKHUB_BASE = _env("TIKHUB_BASE", "https://api.tikhub.io").rstrip("/")
    TIKHUB_API_KEY = _tikhub_key()
    UPSTREAM_TIMEOUT = int(_env("UPSTREAM_TIMEOUT", "60") or 60)

    # ---- 账单 ----
    PAY_BEFORE_MINUTES = int(_env("PAY_BEFORE_MINUTES", "30") or 30)

    def warn(self) -> list:
        out = []
        if self.MOCK_ALIPAY:
            out.append("MOCK_ALIPAY=1：验付被跳过，只用于本地联调，不能上线")
        if self.MOCK_UPSTREAM:
            out.append("MOCK_UPSTREAM=1：不调用 TikHub，返回样例数据")
        if not self.TIKHUB_API_KEY and not self.MOCK_UPSTREAM:
            out.append("缺少 TIKHUB_API_KEY，真实转发会全部失败")
        if not self.ALIPAY_PRIVATE_KEY and not self.MOCK_ALIPAY:
            out.append("缺少 ALIPAY_PRIVATE_KEY，账单无法签名")
        return out


cfg = Config()
