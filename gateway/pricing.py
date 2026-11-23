#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""定价：端点 → 档位 → serviceId / 金额。

支付宝按「服务」定价，一个 serviceId 只能有一个价，所以档位必须在网关侧
先把端点归好类，再映射到不同的 serviceId。新平台里暂时归不进去的端点按
标准档处理，后续用 inventory 的 unit_cost 逐接口校准。
"""
import json
import os
import re
import sys

# 本产品只卖这 7 个国内平台（外加通用演示/混合解析）。
# 网关必须校验，否则任何拿到付费包的人都能用作者的 Key 调 TikTok 等平台。
SUPPORTED_PREFIXES = (
    "/api/v1/douyin/",
    "/api/v1/weibo/",
    "/api/v1/xiaohongshu/",
    "/api/v1/bilibili/",
    "/api/v1/zhihu/",
    "/api/v1/kuaishou/",
    "/api/v1/wechat_channels/",
    "/api/v1/wechat_mp/",
    "/api/v1/wechat_search/",
    "/api/v1/demo/",
    "/api/v1/hybrid/",
)


def platform_of(path: str) -> str:
    """路径 → 平台 slug（用于日志与白名单）。未知平台返回 other。"""
    for prefix in SUPPORTED_PREFIXES:
        if path.startswith(prefix):
            seg = prefix.strip("/").split("/")[-1]
            if seg.startswith("wechat_"):
                return "wechat"
            if seg in ("demo", "hybrid"):
                return "common"
            return seg
    return "other"


def is_supported(path: str) -> bool:
    return any(path.startswith(p) for p in SUPPORTED_PREFIXES)

# 一个 credit 约等于一次 standard 调用的批发价（200 credits / ¥9.90）。
# 高价值/批量只走额度包，不再按次出 ¥0.50/¥2.00 的账单。
TIERS = {
    "standard": {
        "amount": "0.10",
        "credits": 1,
        "goods_name": "社媒数据查询（标准）",
        "service_id_env": "SERVICE_ID_STANDARD",
        "pay_per_call": True,
    },
    "premium": {
        "amount": "0.50",
        "credits": 6,
        "goods_name": "社媒数据查询（高价值，额度）",
        "service_id_env": "SERVICE_ID_PREMIUM",
        "pay_per_call": False,
    },
    "batch": {
        "amount": "2.00",
        "credits": 30,
        "goods_name": "社媒数据查询（批量，额度）",
        "service_id_env": "SERVICE_ID_BATCH",
        "pay_per_call": False,
    },
}

CREDIT_PACKS = {
    # 200 credits 按接口档位扣 1/6/30：标准 200 次、高价值 33 次、批量 6 次
    "starter": {"amount": "9.90", "credits": 200,
                "goods_name": "数据额度包 200 点"},
}

# 路径命中这些词，按批量档计价（上游多为固定价端点）
_BATCH_HINTS = re.compile(r"(multi_|/batch|_batch|bulk)", re.I)
# 路径命中这些词，按高价值档计价（指数、商业平台、榜单/热榜）
_PREMIUM_HINTS = re.compile(
    r"(/index/|_index|/xingtu|billboard|huahuo|/pgy/|"
    r"hot_search|hot_list|hot_board|ranking|top_list)", re.I)

# 逐接口定价：tools/collect_inventory.py 从官方描述里抽出的上游单次价格（USD）。
# 有标价的接口按真实成本归档；没标价的再退回路径正则。
_COST_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "endpoint_costs.json")
_COST_MAP = None
# 现有最高档 ¥2.00 约覆盖 $0.27 成本；更高的接口付费版暂不开放，
# 避免出现“卖一次亏一次”。需要开卖时先登记更高的支付宝价档。
MAX_COVERED_COST = 0.25


def _cost_map() -> dict:
    global _COST_MAP
    if _COST_MAP is None:
        try:
            with open(_COST_PATH, encoding="utf-8") as f:
                _COST_MAP = (json.load(f) or {}).get("costs") or {}
        except Exception:
            _COST_MAP = {}
            print("[pricing] WARN 读不到 endpoint_costs.json，退回路径正则定价",
                  file=sys.stderr)
    return _COST_MAP


def unit_cost_of(path: str):
    """上游单次成本（USD）；没有标价返回 None。"""
    return _cost_map().get(path)


def is_uncovered(path: str) -> bool:
    """上游成本超过现有最高档覆盖能力的端点。"""
    cost = unit_cost_of(path)
    return cost is not None and cost > MAX_COVERED_COST


def classify(path: str) -> str:
    """成本优先、正则兜底。

    成本档位（$1≈¥7.2）：
        ≤ $0.01          → standard  ¥0.10（微信 $0.01 的接口仍留在标准档）
        $0.01 < c < $0.05 → premium  ¥0.50
        ≥ $0.05          → batch     ¥2.00（当前最高 $0.25，覆盖成本后仍有薄利）
    成本高于 $0.27 的接口现有档位无法覆盖，需要人工核价。
    """
    cost = unit_cost_of(path)
    if cost is not None:
        if cost <= 0.0105:
            return "standard"
        if cost < 0.05:
            return "premium"
        return "batch"
    if _BATCH_HINTS.search(path):
        return "batch"
    if _PREMIUM_HINTS.search(path):
        return "premium"
    return "standard"


def tier_of(path: str) -> dict:
    name = classify(path)
    t = dict(TIERS[name])
    t["name"] = name
    return t


# ---------------------------------------------------------------- 任务包

# 一次付费、内部多次调用的「商品化任务」。
# 步骤里的 query 值支持两种写法：
#   "{{input}}"                 → 取请求参数
#   {"from": "step0", "path": "data.user.sec_uid"} → 取前一步返回的字段
TASKS = {
    "douyin_account_analysis": {
        "amount": "1.99",
        "goods_name": "抖音账号数据分析",
        "resource_id": "task:douyin_account_analysis",
        "inputs": ["unique_id"],
        "steps": [
            {"path": "/api/v1/douyin/web/handler_user_profile_v2",
             "query": {"unique_id": "{{unique_id}}"}},
            {"path": "/api/v1/douyin/web/fetch_user_post_videos",
             "query": {"sec_user_id": {"from": "step0", "path": "data.user.sec_uid"},
                       "max_cursor": "0", "count": "20"}},
        ],
    },
}


def resolve_ref(steps_result: list, ref: dict):
    """从已完成步骤的返回里取字段，例如 data.user.sec_uid。"""
    idx = int(str(ref.get("from", "step0")).replace("step", ""))
    node = steps_result[idx] if idx < len(steps_result) else None
    for key in str(ref.get("path", "")).split("."):
        if not key:
            continue
        if isinstance(node, dict) and key in node:
            node = node[key]
        else:
            return None
    return node


def build_query(step: dict, inputs: dict, steps_result: list) -> dict:
    out = {}
    for key, spec in (step.get("query") or {}).items():
        if isinstance(spec, str):
            m = re.fullmatch(r"\{\{(\w+)\}\}", spec.strip())
            out[key] = str(inputs.get(m.group(1), "")) if m else spec
        elif isinstance(spec, dict) and "from" in spec:
            val = resolve_ref(steps_result, spec)
            if val is None:
                raise ValueError(f"步骤引用取不到值: {spec}（接口返回结构可能变了）")
            out[key] = str(val)
        else:
            out[key] = str(spec)
    return out
