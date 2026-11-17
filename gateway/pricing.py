#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""定价：端点 → 档位 → serviceId / 金额。

支付宝按「服务」定价，一个 serviceId 只能有一个价，所以档位必须在网关侧
先把端点归好类，再映射到不同的 serviceId。归不进去的端点一律当最贵档处理，
宁可多收也不亏（构建期另有校验）。
"""
import re

# 一个 credit 约等于一次 standard 调用
TIERS = {
    "standard": {
        "amount": "0.10",
        "credits": 1,
        "goods_name": "社媒数据查询（标准）",
        "service_id_env": "SERVICE_ID_STANDARD",
    },
    "premium": {
        "amount": "0.50",
        "credits": 5,
        "goods_name": "社媒数据查询（指数/星图）",
        "service_id_env": "SERVICE_ID_PREMIUM",
    },
    "batch": {
        "amount": "2.00",
        "credits": 20,
        "goods_name": "社媒数据查询（批量）",
        "service_id_env": "SERVICE_ID_BATCH",
    },
}

CREDIT_PACKS = {
    # 200 credits 按接口档位扣 1/5/20，实际可用 10–200 次（批量档最少，标准档最多）
    "starter": {"amount": "9.90", "credits": 200,
                "goods_name": "数据额度包 10–200 次"},
}

# 路径命中这些词，按批量档计价（TikHub 侧多为固定价端点）
_BATCH_HINTS = re.compile(r"(multi_|/batch|_batch|bulk)", re.I)
# 路径命中这些词，按高价值档计价（巨量算数指数、星图达人）
_PREMIUM_HINTS = re.compile(r"(/index/|_index|/xingtu|billboard)", re.I)


def classify(path: str) -> str:
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
