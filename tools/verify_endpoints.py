#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""对每个平台抽检 2–3 个核心接口，把真实返回结构写进 returns-detail.json。

默认只打印将要调用的接口与预估费用，加 --yes 才真正发出请求（会产生上游费用）。
token 读取顺序：TIKHUB_API_KEY 环境变量 > ~/.workbuddy/tikhub_token。

用法：
    python tools/verify_endpoints.py                 # 预览
    python tools/verify_endpoints.py --yes           # 抽检全部平台
    python tools/verify_endpoints.py --platforms weibo,zhihu --yes
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://api.tikhub.io"
UA = "Mozilla/5.0 (compatible; cn-social-data-verify/2.0)"
HOME_TOKEN = os.path.join(os.path.expanduser("~"), ".workbuddy", "tikhub_token")

# 每个平台挑 2–3 个高频、参数稳定的接口；参数值来自官方文档示例或实测可用值。
VERIFY = {
    "douyin": [
        {"path": "/api/v1/douyin/web/fetch_one_video",
         "query": {"aweme_id": "7372484719365098803"}},
        {"path": "/api/v1/douyin/web/fetch_video_comments",
         "query": {"aweme_id": "7372484719365098803", "count": 5}},
        {"path": "/api/v1/douyin/web/fetch_hot_search_result"},
    ],
    "weibo": [
        {"path": "/api/v1/weibo/app/fetch_user_info", "query": {"uid": "7648703289"}},
        {"path": "/api/v1/weibo/web_v2/fetch_user_posts",
         "query": {"uid": "7277477906", "page": 1}},
        {"path": "/api/v1/weibo/web_v2/fetch_hot_search_summary"},
    ],
    "xiaohongshu": [
        {"path": "/api/v1/xiaohongshu/app_v2/get_user_posted_notes",
         "query": {"user_id": "61b46d790000000010008153"}},
        {"path": "/api/v1/xiaohongshu/web_v3/fetch_user_info",
         "query": {"user_id": "5e3a8ee700000000010070c6"}},
        {"path": "/api/v1/xiaohongshu/app_v2/search_notes",
         "query": {"keyword": "美食推荐", "page": 1}},
    ],
    "bilibili": [
        {"path": "/api/v1/bilibili/web/fetch_one_video", "query": {"bv_id": "BV1M1421t7hT"}},
        {"path": "/api/v1/bilibili/web/fetch_video_comments",
         "query": {"bv_id": "BV1M1421t7hT", "pn": 1}},
        {"path": "/api/v1/bilibili/web/fetch_com_popular"},
    ],
    "zhihu": [
        {"path": "/api/v1/zhihu/web/fetch_column_articles",
         "query": {"column_id": "zhangjiawei", "limit": 10}},
        {"path": "/api/v1/zhihu/web/fetch_hot_list"},
        {"path": "/api/v1/zhihu/web/fetch_column_article_detail",
         "query": {"article_id": "669214677"}},
    ],
    "kuaishou": [
        {"path": "/api/v1/kuaishou/app/fetch_one_video",
         "query": {"photo_id": "3xhpk3xcf6e4iac"}},
        {"path": "/api/v1/kuaishou/app/fetch_hot_board_categories"},
        {"path": "/api/v1/kuaishou/app/search_video_v2", "query": {"keyword": "人工智能"}},
    ],
    "wechat": [
        {"path": "/api/v1/wechat_channels/v2/fetch_channel_info",
         "body": {"username": "v2_060000231003b20faec8c6e4811dc1d4c602ee30b0771bbcf220c67926bb76ab7702ac335a53@finder"}},
        {"path": "/api/v1/wechat_search/v2/fetch_search",
         "body": {"keyword": "人民日报", "business_type": "article", "raw": False}},
        {"path": "/api/v1/wechat_mp/v2/fetch_article_detail_h5",
         "body": {"url": "$wechat_article_url"}},
    ],
    "common": [
        {"path": "/api/v1/demo/douyin/web/fetch_one_video"},
        {"path": "/api/v1/hybrid/video_data", "query": {"url": "https://v.douyin.com/L4FJNR3/"}},
    ],
}


def die(msg):
    print(f"[verify] {msg}", file=sys.stderr)
    sys.exit(1)


def token():
    t = os.environ.get("TIKHUB_API_KEY", "").strip()
    if t:
        return t
    if os.path.exists(HOME_TOKEN):
        return open(HOME_TOKEN, encoding="utf-8").read().strip()
    return ""


def call(path, query=None, body=None, tok=""):
    url = BASE + path
    if query:
        url += "?" + urllib.parse.urlencode(query)
    data = None
    headers = {"Accept": "application/json", "User-Agent": UA}
    if tok:
        headers["Authorization"] = f"Bearer {tok}"
    if body is not None:
        data = json.dumps(body, ensure_ascii=False).encode()
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers,
                                 method="POST" if body is not None else "GET")
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            return resp.status, resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")
    except Exception as e:  # noqa: BLE001
        return 0, f"{type(e).__name__}: {e}"


def keys_of(obj, n=12):
    return ", ".join(f"`{k}`" for k in list(obj)[:n])


def describe(path, status, text):
    if status != 200:
        try:
            msg = json.loads(text).get("message_zh") or json.loads(text).get("message")
        except Exception:
            msg = text[:120]
        return [f"⚠️ 实测失败：HTTP {status}（{msg}）"]

    try:
        payload = json.loads(text)
    except Exception:
        return [f"HTTP 200，但响应不是 JSON（{len(text)} 字符）"]

    lines = []
    data = payload.get("data")
    if data is None:
        extra = {k: v for k, v in payload.items()
                 if k not in ("code", "message", "message_zh", "router", "cache_url")
                 and v not in (None, "", [], {})}
        lines.append("`data` 为 null；内容在顶层字段：" + (keys_of(extra) or "无"))
        return lines

    if isinstance(data, dict):
        lines.append(f"`data` 是对象（{len(data)} 个字段）：{keys_of(data)}")
        for k, v in list(data.items())[:4]:
            if k == "data":
                continue  # 下面会单独展开一层
            if isinstance(v, dict):
                lines.append(f"`data.{k}` 是对象（{len(v)} 个字段）：{keys_of(v, 8)}")
            elif isinstance(v, list):
                first = v[0] if v else None
                hint = f"；首元素字段：{keys_of(first, 8)}" if isinstance(first, dict) else ""
                lines.append(f"`data.{k}` 是数组（长度 {len(v)}）{hint}")
    elif isinstance(data, list):
        first = data[0] if data else None
        hint = f"；首元素字段：{keys_of(first, 10)}" if isinstance(first, dict) else ""
        lines.append(f"`data` 是数组（长度 {len(data)}）{hint}")
    else:
        lines.append(f"`data` 类型：{type(data).__name__}，值：{str(data)[:80]}")

    # 多数平台把业务数据再包一层 data.data / data.items，顺手展开一级
    inner = data.get("data") if isinstance(data, dict) else None
    if isinstance(inner, dict):
        lines.append(f"`data.data` 是对象（{len(inner)} 个字段）：{keys_of(inner, 10)}")
        for lk in ("list", "items", "notes", "feeds", "cards"):
            if isinstance(inner.get(lk), list):
                arr = inner[lk]
                first = arr[0] if arr else None
                hint = f"；首元素字段：{keys_of(first, 8)}" if isinstance(first, dict) else ""
                lines.append(f"`data.data.{lk}` 是数组（长度 {len(arr)}）{hint}")
    elif isinstance(inner, list):
        first = inner[0] if inner else None
        hint = f"；首元素字段：{keys_of(first, 10)}" if isinstance(first, dict) else ""
        lines.append(f"`data.data` 是数组（长度 {len(inner)}）{hint}")

    msg = payload.get("message_zh") or payload.get("message")
    if msg:
        lines.append(f"响应消息：{msg}")
    lines.append(f"实测时间：{__import__('datetime').date.today().isoformat()}")
    return lines


def resolve_wechat_url(tok):
    status, text = call("/api/v1/wechat_search/v2/fetch_search", None,
                        {"keyword": "人民日报", "business_type": "article", "raw": False}, tok)
    try:
        items = json.loads(text)["data"]["items"]
        return items[0]["doc_url"].replace("http://", "https://")
    except Exception:
        die("无法先拿到一篇公众号文章 URL（微信搜索接口失败）")


def update_returns(slug, path, lines, write):
    fp = os.path.join(ROOT, "src", "platforms", slug, "returns-detail.json")
    data = {}
    if os.path.exists(fp):
        data = json.load(open(fp, encoding="utf-8"))
    if data.get("_note") is None:
        data["_note"] = ("实测返回结构。tools/patch_returns.py 会写入 inventory.json 的 "
                         "returns_detail 并注入分类 md；CLI 的 show 也会打印。")
    data[path] = lines
    if write:
        with open(fp, "w", encoding="utf-8", newline="\n") as f:
            json.dump(data, f, ensure_ascii=False, indent=1)
            f.write("\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--platforms", default="all")
    ap.add_argument("--yes", action="store_true", help="真正发出请求（会产生费用）")
    args = ap.parse_args()

    slugs = list(VERIFY) if args.platforms == "all" else [
        s.strip() for s in args.platforms.split(",") if s.strip()]
    bad = [s for s in slugs if s not in VERIFY]
    if bad:
        die(f"未知平台 {bad}；可选 {list(VERIFY)}")

    calls = sum(len(VERIFY[s]) for s in slugs)
    print(f"[verify] 计划抽检 {calls} 个接口（{', '.join(slugs)}），"
          f"上游费用按每个 $0.001–0.01 估算，总计约 $0.01–0.05。")
    for s in slugs:
        for e in VERIFY[s]:
            mode = "POST" if "body" in e else "GET"
            print(f"  {s:12s} {mode:4s} {e['path']}")
    if not args.yes:
        print("\n未加 --yes，未发出任何请求。")
        return

    tok = token()
    if not tok:
        die("没有 token：设置 TIKHUB_API_KEY 或写入 ~/.workbuddy/tikhub_token")

    wechat_url = None
    for slug in slugs:
        for e in VERIFY[slug]:
            body = e.get("body")
            if body and body.get("url") == "$wechat_article_url":
                wechat_url = wechat_url or resolve_wechat_url(tok)
                body = dict(body, url=wechat_url)
            print(f"[verify] {slug} {e['path']} ...", end="", flush=True)
            status, text = call(e["path"], e.get("query"), body, tok)
            lines = describe(e["path"], status, text)
            update_returns(slug, e["path"], lines, write=True)
            print(f" HTTP {status} -> {lines[0][:70]}")
    print("\n[verify] 已写入各平台 returns-detail.json；"
          "接着运行 python tools/patch_returns.py --all --write")


if __name__ == "__main__":
    main()
