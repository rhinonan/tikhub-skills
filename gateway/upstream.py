#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""上游转发：注入作者 Key，把请求打到 TikHub。

MOCK_UPSTREAM=1 时返回样例数据，用于在没有 TikHub Key 的情况下跑通全链路。
"""
import json
import urllib.error
import urllib.parse
import urllib.request

from config import cfg


class UpstreamError(RuntimeError):
    def __init__(self, message: str, status: int = 0, retryable: bool = False):
        super().__init__(message)
        self.status = status
        self.retryable = retryable


def _mock(path: str, query: dict) -> dict:
    """样例数据，字段名对齐 TikHub 真实返回，便于验证任务链的字段引用。"""
    if path.endswith("handler_user_profile_v2"):
        return {"code": 200, "data": {"user": {
            "unique_id": query.get("unique_id", ""),
            "sec_uid": "MS4wLjABAAAAmock_sec_uid",
            "nickname": "样例账号",
            "follower_count": 123456,
            "aweme_count": 200,
        }}}
    if path.endswith("fetch_user_post_videos"):
        return {"code": 200, "data": {"aweme_list": [
            {"aweme_id": f"73000000000000000{i}", "desc": f"样例作品 {i}",
             "statistics": {"play_count": 10000 * (6 - i), "digg_count": 500 * i}}
            for i in range(1, 4)
        ], "has_more": False, "echo": dict(query)}}
    if path.endswith("fetch_hot_search_result"):
        return {"code": 200, "data": {"data": {"word_list": [
            {"word": "样例热点", "hot_value": 9999}]}}}
    return {"code": 200, "data": {"mock": True, "path": path, "query": query}}


def call(path: str, method: str = "GET", query: dict = None, body: dict = None) -> dict:
    query = {k: v for k, v in (query or {}).items() if v not in ("", None)}

    if cfg.MOCK_UPSTREAM:
        return _mock(path, query)

    if not cfg.TIKHUB_API_KEY:
        raise UpstreamError("服务端未配置 TikHub Key", status=500, retryable=False)

    url = cfg.TIKHUB_BASE + path
    if query:
        url += "?" + urllib.parse.urlencode(query)
    data = None
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {cfg.TIKHUB_API_KEY}",
        "User-Agent": "cn-social-data-gateway/2.0",
    }
    if body is not None:
        data = json.dumps(body, ensure_ascii=False).encode()
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, data=data, headers=headers,
                                 method="POST" if body is not None else "GET")
    try:
        with urllib.request.urlopen(req, timeout=cfg.UPSTREAM_TIMEOUT) as resp:
            return json.loads(resp.read().decode("utf-8", "replace"))
    except urllib.error.HTTPError as exc:
        # 429 / 5xx 属于上游临时问题，不应当让用户为这次失败付费
        raise UpstreamError(f"TikHub 返回 HTTP {exc.code}", status=exc.code,
                            retryable=exc.code in (429, 500, 502, 503, 504))
    except Exception as exc:
        raise UpstreamError(f"TikHub 调用失败: {exc}", status=0, retryable=True)
