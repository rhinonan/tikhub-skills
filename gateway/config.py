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
  MOCK_UPSTREAM=1      跳过真实 TikHub 调用，返回样例数据
  本地假验付见 tests/mock_server.py（仅测试目录，不进生产镜像）
"""
import json
import os
import pathlib

SANDBOX_GATEWAY = "https://openapi-sandbox.dl.alipaydev.com/gateway.do"


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


def _normalize_private_key(raw: str) -> str:
    """统一成 alipay-sdk-python 需要的 PKCS#1 裸 Base64。

    生产密钥常由密钥工具导出为 PKCS#8；SDK 的 rsa.load_pkcs1 只接受
    PKCS#1。这里在加载边界做一次格式转换，密钥内容本身不变。
    """
    if not raw:
        return ""
    text = raw.strip()
    if "-----BEGIN" in text:
        import re
        text = re.sub(r"-----[^-]+-----", "", text)
    text = "".join(text.split())
    try:
        import base64
        from Crypto.PublicKey import RSA
        key = RSA.import_key(base64.b64decode(text))
        return base64.b64encode(key.export_key(format="DER", pkcs=1)).decode()
    except Exception:
        # 无法识别时保留原值，由真实调用处给出明确错误
        return raw.strip()


def _tikhub_key() -> str:
    key = _read_key(_env("TIKHUB_API_KEY"))
    if key:
        return key
    fallback = pathlib.Path.home() / ".workbuddy" / "tikhub_token"
    if fallback.is_file():
        return fallback.read_text(encoding="utf-8").strip()
    return ""


_GATEWAY = _env("ALIPAY_GATEWAY", "https://openapi.alipay.com/gateway.do")
# 只有网关地址严格等于沙箱地址时才加载本地沙箱配置，避免误把测试密钥用于生产。
_SANDBOX_MODE = _GATEWAY == SANDBOX_GATEWAY


def _load_sandbox() -> dict:
    if not _SANDBOX_MODE:
        return {}
    path = pathlib.Path(_env(
        "SANDBOX_CONFIG_PATH",
        str(pathlib.Path(__file__).parent / ".alipay-sandbox.json"))).expanduser()
    if not path.is_file():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


_SANDBOX = _load_sandbox()


def _sandbox_app() -> dict:
    apps = _SANDBOX.get("appIds") or []
    if isinstance(apps, list) and apps and isinstance(apps[0], dict):
        return apps[0]
    return {}


_SANDBOX_APP = _sandbox_app()


def _sandbox_seller_id() -> str:
    accounts = _SANDBOX.get("sandboxAccounts") or {}
    merchant = accounts.get("partner") or accounts.get("merchant") or {}
    return str(merchant.get("userId") or "").strip()


def _sandbox_value(name: str) -> str:
    return str(_SANDBOX_APP.get(name) or "").strip()


class Config:
    # ---- 运行模式 ----
    # 验付没有 mock 开关：生产与服务端始终走真实 SDK 校验。
    # 本地测试请用 tests/mock_server.py（仅测试目录，不进生产镜像）。
    MOCK_UPSTREAM = _env_bool("MOCK_UPSTREAM", False)
    SANDBOX_MODE = _SANDBOX_MODE
    # 沙箱 serviceId 固定为 api_mock_service_id，其登记价是 0.01 元。
    # 生产金额仍由 pricing.py 决定。
    SANDBOX_AMOUNT = "0.01"

    # ---- 基础 ----
    BASE_URL = _env("GATEWAY_BASE_URL", "http://127.0.0.1:3006").rstrip("/")
    DB_PATH = _env("DB_PATH",
                   str(pathlib.Path(__file__).parent / ".local" / "gateway.db"))
    HOST = _env("HOST", "127.0.0.1")
    PORT = int(_env("PORT", "3006") or 3006)

    # ---- 卖家身份 ----
    # 沙箱模式下从 .alipay-sandbox.json 的 appIds[0] 和商家账号补齐，
    # 环境变量始终优先。缺失时保持空值，由调用方明确失败，不使用占位身份。
    SELLER_ID = _env("SELLER_ID") or _sandbox_seller_id()
    SELLER_NAME = _env("SELLER_NAME", "社交数据服务")
    SELLER_APP_ID = _env("SELLER_APP_ID") or _sandbox_value("appId")

    # ---- 支付宝 ----
    ALIPAY_GATEWAY = _GATEWAY
    ALIPAY_PRIVATE_KEY = _normalize_private_key(
        _read_key(_env("ALIPAY_PRIVATE_KEY"))
        or _sandbox_value("appPrivatePkcsKey"))
    ALIPAY_PUBLIC_KEY = (_read_key(_env("ALIPAY_PUBLIC_KEY"))
                         or _sandbox_value("alipayPublicKey"))

    def is_exact_sandbox(self, service_id: str = "api_mock_service_id") -> bool:
        """严格沙箱模式：网关与 serviceId 同时是沙箱值，才允许验付字段兜底。"""
        return self.ALIPAY_GATEWAY == SANDBOX_GATEWAY and \
            service_id == "api_mock_service_id"

    def missing_alipay_fields(self) -> list:
        """真实 SDK 调用前的配置完整性检查，缺任何一项都必须明确失败。"""
        missing = []
        if not self.SELLER_APP_ID:
            missing.append("SELLER_APP_ID")
        if not self.ALIPAY_PRIVATE_KEY:
            missing.append("ALIPAY_PRIVATE_KEY")
        if not self.ALIPAY_PUBLIC_KEY:
            missing.append("ALIPAY_PUBLIC_KEY")
        return missing

    # ---- 上游 ----
    TIKHUB_BASE = _env("TIKHUB_BASE", "https://api.tikhub.io").rstrip("/")
    TIKHUB_API_KEY = _tikhub_key()
    UPSTREAM_TIMEOUT = int(_env("UPSTREAM_TIMEOUT", "60") or 60)

    # ---- 账单 ----
    PAY_BEFORE_MINUTES = int(_env("PAY_BEFORE_MINUTES", "30") or 30)

    def warn(self) -> list:
        out = []
        if self.SANDBOX_MODE:
            out.append("SANDBOX_MODE：使用本地 .alipay-sandbox.json，禁止上线")
        if self.MOCK_UPSTREAM:
            out.append("MOCK_UPSTREAM=1：不调用 TikHub，返回样例数据")
        if not self.TIKHUB_API_KEY and not self.MOCK_UPSTREAM:
            out.append("缺少 TIKHUB_API_KEY，真实转发会全部失败")
        if not self.ALIPAY_PRIVATE_KEY:
            out.append("缺少 ALIPAY_PRIVATE_KEY，账单无法签名")
        if not self.ALIPAY_PUBLIC_KEY:
            out.append("缺少 ALIPAY_PUBLIC_KEY，无法验证支付宝响应")
        return out


cfg = Config()
