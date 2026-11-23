#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""中文社媒数据引擎 CLI（多平台）。

同一个文件由 build.py 复制到免费版 / 付费版两个 skill 里，运行时配置从
脚本上级目录的 skill_meta.json 读取：

    {"skill": "cn-social-data", "edition": "free",
     "base_url": "https://api.tikhub.io", "gateway_url": "",
     "platforms": [{"platform": "douyin", "platform_zh": "抖音",
                    "api_prefixes": ["/api/v1/douyin"]}, ...]}

免费版（edition=free）：用户自备上游 Key，直连上游 API。
付费版（edition=pro） ：经作者网关转发，按次 402 付费。

用法:
  python social.py doctor                      # 自检：环境/清单/凭证一次看完
  python social.py search "关键词" [--platform X]
  python social.py show <关键词或path> [--platform X]
  python social.py list [--platform X] [--folder F]
  python social.py call <path> [-q k=v ...] [-b '{...}'] [--dry-run]
  python social.py token [<token>]
  python social.py ping
  python social.py recharge [--pack starter] [--proof X]   # 仅付费版

兼容性约定：
  * 解释器：`python3` 优先，老环境用 `python`；脚本兼容 Python 3.8+。
  * 运行目录：脚本用 __file__ 定位 skill 根目录，在任意 cwd 下都能跑；
    仍建议用 `python3 <skill目录>/scripts/social.py ...` 的绝对路径调用。
  * 清单缺失/损坏不影响 call：给完整 path 仍可直连；search/show 会退回扫描
    references/*.md 的降级模式。
"""
import argparse
import difflib
import glob
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

VERSION = "2.0.0"

if sys.version_info < (3, 8):
    sys.stderr.write("[ERROR] 需要 Python 3.8+，当前 %s\n" % sys.version.split()[0])
    sys.exit(1)

# Windows 控制台（cp936）打印生僻字会抛 UnicodeEncodeError，宁可乱码不要报错
try:
    sys.stdout.reconfigure(errors="replace")
    sys.stderr.reconfigure(errors="replace")
except Exception:
    pass

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
META_PATH = os.path.join(SKILL_DIR, "skill_meta.json")
REF_DIR = os.path.join(SKILL_DIR, "references")
INV = os.path.join(REF_DIR, "inventory.json")
HOME = os.path.join(os.path.expanduser("~"), ".workbuddy")
HOME_TOKEN = os.path.join(HOME, "tikhub_token")
HOME_GW_TOKEN = os.path.join(HOME, "tikhub_gateway_token")
TIMEOUT = 90
RETRY_STATUS = (429, 500, 502, 503, 504)
# 文档没写默认值时，给分页类参数补一个安全默认，省掉用户手填和 422 往返
PAGE_DEFAULTS = {"cursor": 0, "max_cursor": 0, "max_time": 0, "offset": 0,
                 "page": 1, "count": 20, "counts": 20, "page_size": 20,
                 "limit": 20}


class NetError(Exception):
    """网络层失败（超时、DNS、连接被重置），由调用方决定是否重试。"""


def die(msg, code=1):
    print(f"[ERROR] {msg}", file=sys.stderr)
    sys.exit(code)


def warn(msg):
    print(f"[WARN] {msg}", file=sys.stderr)


def load_meta():
    if not os.path.exists(META_PATH):
        warn(f"找不到 {META_PATH}（skill 包不完整，用 build.py 重新生成）；"
             "先按默认值继续，call 仍可用")
        return {}
    try:
        with open(META_PATH, encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        warn(f"{META_PATH} 解析失败（{e}）；先按默认值继续")
        return {}


META = load_meta()
SKILL_NAME = META.get("skill", "cn-social-data")
SKILL_ZH = META.get("name_zh", "中文社媒数据引擎")
EDITION = META.get("edition", "free")
BASE = (META.get("base_url") or "https://api.tikhub.io").rstrip("/")
GATEWAY = (META.get("gateway_url") or "").rstrip("/")
IS_PRO = EDITION == "pro"
TOKEN_FILE = HOME_GW_TOKEN if IS_PRO else HOME_TOKEN

# 与 gateway/pricing.py 保持一致的定价参数（build.py --check 会校验）
_PRICING_DEFAULT = {
    "tiers": {
        "standard": {"credits": 1, "amount": "0.10", "per_call": True},
        "premium": {"credits": 6, "amount": "0.50", "per_call": False},
        "batch": {"credits": 30, "amount": "2.00", "per_call": False},
    },
    "cost_thresholds": {"standard_max": 0.0105, "premium_max": 0.05},
    "pack": {"credits": 200, "amount": "9.90"},
}
PRICING = META.get("pricing") or _PRICING_DEFAULT
TIER_CFG = PRICING.get("tiers") or _PRICING_DEFAULT["tiers"]
COST_STANDARD_MAX = float((PRICING.get("cost_thresholds") or {})
                          .get("standard_max", 0.0105))
COST_PREMIUM_MAX = float((PRICING.get("cost_thresholds") or {})
                         .get("premium_max", 0.05))
PACK_CFG = PRICING.get("pack") or _PRICING_DEFAULT["pack"]

# 平台表：缺省时按已知 slug 兜底，保证 skill_meta.json 损坏也能跑
_DEFAULT_PLATFORMS = [
    ("douyin", "抖音", ["/api/v1/douyin"]),
    ("weibo", "微博", ["/api/v1/weibo"]),
    ("xiaohongshu", "小红书", ["/api/v1/xiaohongshu"]),
    ("bilibili", "B站", ["/api/v1/bilibili"]),
    ("zhihu", "知乎", ["/api/v1/zhihu"]),
    ("wechat", "微信", ["/api/v1/wechat_channels", "/api/v1/wechat_mp",
                        "/api/v1/wechat_search"]),
    ("kuaishou", "快手", ["/api/v1/kuaishou"]),
    ("common", "通用", ["/api/v1/demo", "/api/v1/hybrid"]),
]


def _load_platforms():
    platforms = META.get("platforms")
    if platforms:
        return [(p.get("platform", ""), p.get("platform_zh", ""),
                 p.get("api_prefixes") or [f"/api/v1/{p.get('platform', '')}"])
                for p in platforms]
    return _DEFAULT_PLATFORMS


PLATFORMS = _load_platforms()
PLATFORM_ZH = {slug: zh for slug, zh, _ in PLATFORMS}
_PREFIXES = sorted(
    [(pre.rstrip("/") + "/", slug) for slug, _, pres in PLATFORMS for pre in pres],
    key=lambda x: -len(x[0]),
)


def platform_of(path):
    """按路径前缀推断平台；未知返回 other。"""
    p = "/" + (path or "").replace("\\", "/").lstrip("/")
    if not p.startswith("/api/"):
        i = p.lower().find("/api/")
        p = p[i:] if i >= 0 else p
    for prefix, slug in _PREFIXES:
        if p.startswith(prefix):
            return slug
    return "other"


def platform_zh_of(path):
    slug = platform_of(path)
    return PLATFORM_ZH.get(slug, slug if slug != "other" else "其他")


def _match_platform(value):
    """--platform 支持 slug 或中文名。"""
    if not value:
        return ""
    v = value.strip().lower()
    for slug, zh, _ in PLATFORMS:
        if v == slug.lower() or v == zh.lower():
            return slug
    return value.strip().lower()


def _row_platform(r):
    return r.get("platform") or platform_of(r.get("path", ""))


_SEG_TO_SLUG = {}
for _slug, _zh, _pres in PLATFORMS:
    for _pre in _pres:
        _SEG_TO_SLUG[_pre.rstrip("/").split("/")[-1]] = _slug


def platform_from_key(key):
    """`douyin/web/...` / `wechat_mp/v2/...` 这类简写自带平台线索。"""
    seg = _norm(key).lstrip("/").split("/")[0]
    return _SEG_TO_SLUG.get(seg, "")


# ---------------------------------------------------------------- 凭证

def _read(p):
    if os.path.exists(p):
        t = open(p, encoding="utf-8").read().strip()
        return t[7:].strip() if t.lower().startswith("bearer ") else t
    return ""


def get_token():
    """免费版优先级：环境变量 > skill/.token > ~/.workbuddy/tikhub_token"""
    if IS_PRO:
        return (_read(os.path.join(SKILL_DIR, ".token")) or _read(HOME_GW_TOKEN))
    for p in (os.environ.get("TIKHUB_API_KEY", "").strip(),
              _read(os.path.join(SKILL_DIR, ".token")),
              _read(HOME_TOKEN)):
        if p:
            return p
    return ""


def save_token(tok):
    os.makedirs(HOME, exist_ok=True)
    with open(TOKEN_FILE, "w", encoding="utf-8") as f:
        f.write(tok)
    # 如果用户手动放了 skill/.token（优先级更高），充值后一并更新，避免新 token 被旧文件遮住
    local = os.path.join(SKILL_DIR, ".token")
    if IS_PRO and os.path.exists(local):
        try:
            with open(local, "w", encoding="utf-8") as f:
                f.write(tok)
        except Exception:
            pass
    try:
        os.chmod(TOKEN_FILE, 0o600)
    except Exception:
        pass
    return TOKEN_FILE


# ---------------------------------------------------------------- 接口清单

_INV_CACHE = {"rows": None, "err": ""}


def load_inventory():
    """读清单；失败返回 [] 并记下原因，由调用方决定降级还是退出。"""
    if _INV_CACHE["rows"] is not None or _INV_CACHE["err"]:
        return _INV_CACHE["rows"] or []
    if not os.path.exists(INV):
        _INV_CACHE["err"] = f"找不到接口清单 {INV}"
        return []
    try:
        with open(INV, encoding="utf-8") as f:
            rows = json.load(f)
        if not isinstance(rows, list) or not rows:
            raise ValueError("清单不是非空数组")
    except Exception as e:
        _INV_CACHE["err"] = f"接口清单无法读取（{e}）"
        return []
    _INV_CACHE["rows"] = rows
    return rows


def inventory_error():
    return _INV_CACHE["err"]


MD_BLOCK_CACHE = {}


def _md_blocks():
    """降级通道：把 references/<分类>.md 解析成条目，清单坏了也能搜索。"""
    if MD_BLOCK_CACHE:
        return MD_BLOCK_CACHE["blocks"]
    blocks = []
    for path in sorted(glob.glob(os.path.join(REF_DIR, "*.md"))):
        name = os.path.basename(path)
        if name in ("index.md", "api-index.md"):
            continue
        folder = name[:-3]
        try:
            text = open(path, encoding="utf-8").read()
        except Exception:
            continue
        for chunk in re.split(r"\n(?=##\s)", text):
            m = re.match(r"##\s+(.+)\n+`(GET|POST|PUT|DELETE|PATCH)\s+(\S+)`", chunk.strip())
            if not m:
                continue
            blocks.append({"title": m.group(1).strip(), "method": m.group(2),
                           "path": m.group(3), "folder": folder, "text": chunk.strip()})
    MD_BLOCK_CACHE["blocks"] = blocks
    return blocks


def _norm(key):
    """兼容 Git Bash 把 /api/... 转成 Windows 路径的情况。"""
    k = key.replace("\\", "/")
    i = k.lower().find("/api/")
    return (k[i:] if i >= 0 else k).rstrip("/")


def _find(rows, key):
    """按精确度分层返回候选：完整 path > path 结尾 > path 包含 > 名称包含。"""
    k = _norm(key).lower().strip("/")
    buckets = ([], [], [], [])
    for r in rows:
        p = r["path"].lower()
        if p.strip("/") == k:
            buckets[0].append(r)
        elif p.endswith("/" + k):
            buckets[1].append(r)
        elif k in p:
            buckets[2].append(r)
        elif k in (r.get("name_zh") or "").lower() or k in (r.get("name") or "").lower():
            buckets[3].append(r)
    for b in buckets:
        if b:
            return b
    return []


def _suggest(key, pool, n=5):
    """找不到时给最接近的几条，而不是只说"没找到"。"""
    key = str(key).lower()
    scored = []
    for r in pool:
        p = (r.get("path") or "").lower()
        t = (r.get("name_zh") or r.get("title") or "").lower()
        ratio = max(difflib.SequenceMatcher(None, key, p).ratio(),
                    difflib.SequenceMatcher(None, key, t).ratio())
        scored.append((ratio, r))
    scored.sort(key=lambda x: -x[0])
    return [r for ratio, r in scored[:n] if ratio > 0.3]


def _platform_filter(rows, platform):
    slug = _match_platform(platform)
    if not slug:
        return rows
    return [r for r in rows if _row_platform(r) == slug]


# ---------------------------------------------------------------- 本地命令

def _repair_hint():
    warn(f"{inventory_error()}；已切到降级模式（扫 references/*.md）")
    print("[降级] 修复方式：确认 skill 包完整（应有 references/inventory.json），"
          "缺失就用 build.py 重新生成；期间可用 `list`、`search`（走 md 扫描）"
          "或直接翻 references/<分类>.md。", file=sys.stderr)


def _md_rows():
    """把 md 块转成与 inventory 同形状的字段，供 search/show 复用同一套打印逻辑。"""
    out = []
    for b in _md_blocks():
        out.append({"platform": platform_of(b["path"]), "folder": b["folder"],
                    "name": b["title"], "name_zh": b["title"], "name_en": "",
                    "method": b["method"], "path": b["path"], "purpose": "",
                    "returns": "", "query_params": [], "body_params": [],
                    "request_example": "", "doc": "", "_md_text": b["text"]})
    return out


def _load_rows():
    rows = load_inventory()
    if not rows:
        rows = _md_rows()
        if rows:
            _repair_hint()
    return rows


def _row_text(r):
    return " ".join([r.get("name", ""), r.get("name_zh", ""), r.get("name_en", ""),
                     r.get("path", ""), r.get("purpose", ""), r.get("folder", "")]).lower()


def cmd_search(args):
    rows = _load_rows()
    if not rows:
        die("接口清单和 references/*.md 都读不到，skill 包疑似不完整："
            "重新解压/构建该 skill 后再试")
    rows = _platform_filter(rows, args.platform)
    if not rows:
        die(f"没有平台 {args.platform} 的接口；可用："
            + "、".join(f"{s}({z})" for s, z, _ in PLATFORMS))
    kw = [k.lower() for k in args.keyword]
    hits = [r for r in rows if all(k in _row_text(r) for k in kw)]
    relaxed = False
    if not hits and len(kw) > 1:
        # 多关键词按 AND 搜不到时退一步按 OR 再搜，避免"加了个词就 0 结果"
        hits = [r for r in rows if any(k in _row_text(r) for k in kw)]
        relaxed = bool(hits)
    if not hits:
        print(f"没匹配到接口（关键词: {' '.join(args.keyword)}）")
        sug = _suggest(" ".join(args.keyword), rows)
        if sug:
            print("相近的接口：")
            for r in sug:
                print(f"  [{platform_zh_of(r['path'])}] {r['method']} {r['path']}"
                      f"   # {r.get('name_zh') or r.get('name')}")
        folders = sorted({r["folder"] for r in rows})
        print("也可以按分类浏览：" + "、".join(folders[:6])
              + ("…" if len(folders) > 6 else "") + "（list --folder <分类>）")
        print("清单里的中文名/英文名/路径/用途都能当关键词，换一个更短的词试试。")
        return
    limit = args.limit or 25
    head = f"命中 {len(hits)} 个接口"
    if relaxed:
        head += "（按 OR 放宽后）"
    print(head + (f"，显示前 {limit} 个：" if len(hits) > limit else "："))
    for r in hits[:limit]:
        print(f"- [{platform_zh_of(r['path'])}/{r['folder']}] "
              f"{r.get('name_zh') or r.get('name')}")
        print(f"  {r['method']} {r['path']}")
        if r.get("purpose") and r["purpose"] != (r.get("name_zh") or r.get("name")):
            print(f"  用途: {r['purpose'][:100]}")
    if len(hits) > limit:
        print(f"... 还有 {len(hits)-limit} 个，用 --limit 扩大或加关键词")


def _print_params(title, params):
    print(f"\n{title}:")
    for p in params or []:
        req = "必填" if p.get("required") else "可选"
        name = p.get("name", "?")
        default = p.get("default")
        print(f"  {name} ({req}, {p.get('type', '')}"
              + (f", 默认 {default}" if default not in ("", None) else "")
              + f")  {p.get('desc', '')}")


def _print_entry(r):
    print(f"# {r.get('name_zh') or r.get('name')}")
    print(f"平台: {platform_zh_of(r['path'])}（{platform_of(r['path'])}）")
    if IS_PRO:
        print(f"接口 {r['method']} {r['path']}")
        print(f"经由网关 POST {GATEWAY}/v1/call（按次付费）")
    else:
        print(f"{r['method']} {BASE}{r['path']}")
    print(f"文件夹: {r['folder']}")
    if r.get("unit_cost_usd") is not None:
        print(f"上游成本: ${r['unit_cost_usd']:g}/次（付费版按档位计价，不直接透传成本）")
    if r.get("deprecated"):
        print("状态: 已标记 deprecated，可能随时失效")
    if r.get("purpose"):
        print(f"用途: {r['purpose']}")
    if r.get("returns"):
        print(f"返回: {r['returns']}")
    if r.get("notice"):
        print(f"注意: {r['notice']}")
    if r.get("query_params"):
        _print_params("Query 参数", r["query_params"])
    if r.get("body_params"):
        _print_params("Body(JSON) 参数", r["body_params"])
        if r.get("body_schema", {}).get("type") == "array":
            print("  （该接口的 body 是 JSON 数组，直接传 -b '[\"id1\",\"id2\"]'）")
    if r.get("request_example"):
        ex = r["request_example"]
        print("\n请求示例:\n" + (json.dumps(ex, ensure_ascii=False, indent=2)
                              if not isinstance(ex, str) else ex))
    if r.get("returns_detail"):
        print("\n返回结构（实测）：")
        for line in r["returns_detail"]:
            print(f"  - {line}")
    if r.get("doc"):
        print(f"\n文档: {r['doc']}")
    elif r.get("_md_text"):
        print("\n--- references 原文 ---\n" + r["_md_text"])
    if r.get("query_params") or r.get("body_params"):
        example = ("-b '{...}'" if r.get("body_params") or r["method"] == "POST" else "-q k=v")
        print("\n下一步：python3 scripts/social.py call "
              f"{r['path']} {example} --out out/result.json")


def _hint_platform(key, given=""):
    if given:
        return given
    k = _norm(key)
    if k.startswith("/api/"):
        return platform_of(k)
    return platform_from_key(k)


# ---------------------------------------------------------------- 付费预估

def tier_for_cost(cost):
    """与网关一致：成本 ≤$0.01 标准、<$0.05 高价值、其余批量；无标价按标准。"""
    if cost is None:
        return "standard"
    if cost <= COST_STANDARD_MAX:
        return "standard"
    if cost < COST_PREMIUM_MAX:
        return "premium"
    return "batch"


def tier_credits(name):
    return int((TIER_CFG.get(name) or {}).get("credits", 1))


TIER_LABEL = {"standard": "标准", "premium": "高价值", "batch": "批量"}


def tier_amount(name):
    return str((TIER_CFG.get(name) or {}).get("amount", "0.10"))


def tier_per_call(name):
    return bool((TIER_CFG.get(name) or {}).get("per_call", name == "standard"))


def _credit_cny(credits):
    pack_credits = int(PACK_CFG.get("credits") or 200)
    pack_amount = float(PACK_CFG.get("amount") or 9.9)
    return credits * pack_amount / pack_credits if pack_credits else 0.0


def _gateway_balance(timeout=4):
    """付费版读一次余额；失败返回 None，不影响预估展示。"""
    if not IS_PRO or not GATEWAY:
        return None
    token = get_token()
    if not token:
        return 0
    try:
        status, _, text = _raw_request(
            GATEWAY + "/v1/balance",
            {"Accept": "application/json", "User-Agent": _ua(),
             "Authorization": f"Bearer {token}"}, None, timeout)
        if status == 200:
            return int(json.loads(text).get("credits", 0))
    except Exception:
        pass
    return None


def _estimate_items(items, title="", json_out=False, no_balance=False):
    """items: [{"row": inventory_row, "repeat": n}]；返回预估汇总 dict。"""
    balance = None if no_balance else _gateway_balance()
    out_items = []
    total_credits = 0
    total_calls = 0
    total_percall = 0.0
    total_usd = 0.0
    has_non_per_call = False
    for idx, item in enumerate(items, 1):
        row = item["row"]
        repeat = int(item.get("repeat", 1))
        tier = tier_for_cost(row.get("unit_cost_usd"))
        credits = tier_credits(tier)
        per_call = tier_per_call(tier)
        calls = repeat
        total_calls += calls
        total_credits += credits * calls
        if per_call:
            total_percall += float(tier_amount(tier)) * calls
        else:
            has_non_per_call = True
        cost = row.get("unit_cost_usd")
        if cost is not None:
            total_usd += float(cost) * calls
        out_items.append({
            "index": idx,
            "name": row.get("name_zh") or row.get("name") or row["path"],
            "platform": platform_zh_of(row["path"]),
            "method": row.get("method", "GET"),
            "path": row["path"],
            "tier": tier,
            "tier_label": TIER_LABEL.get(tier, tier),
            "credits": credits,
            "per_call": per_call,
            "repeat": repeat,
            "unit_cost_usd": cost,
        })

    approx_cny = _credit_cny(total_credits)
    summary = {
        "title": title or "本次调用",
        "total_calls": total_calls,
        "total_credits": total_credits,
        "approx_cny": round(approx_cny, 2),
        "per_call_cny": round(total_percall, 2),
        "upstream_usd": round(total_usd, 4),
        "balance": balance,
        "balance_skipped": bool(no_balance),
        "has_non_per_call": has_non_per_call,
        "items": out_items,
    }

    if json_out:
        print(json.dumps(summary, ensure_ascii=False, indent=1))
        return summary

    print(f"\n== {'付费' if IS_PRO else '调用'}预估 ==\n任务: {summary['title']}")
    print(f"预计请求: {total_calls} 次接口调用")
    if IS_PRO:
        if no_balance:
            print("当前额度: 未查询（--no-balance）")
        else:
            print("当前额度: " + ("未知（网关不可达）" if balance is None else f"{balance} 点"))
    print()
    print("| # | 平台 | 接口 | 档位 | 本次扣费 |")
    print("|---|---|---|---|---|")
    for it in out_items:
        charge = (f"{it['credits']} 点" if IS_PRO
                  else f"上游 ${it['unit_cost_usd']:g}" if it["unit_cost_usd"] is not None
                  else "未知")
        if IS_PRO and it["per_call"]:
            charge += f"（无额度时 ¥{tier_amount(it['tier'])}/次）"
        suffix = f" ×{it['repeat']}" if it["repeat"] > 1 else ""
        print(f"| {it['index']} | {it['platform']} | {it['method']} {it['path']}{suffix} "
              f"| {it['tier_label']} | {charge} |")

    print()
    if IS_PRO:
        print(f"合计: {total_credits} 点（按额度包折算约 ¥{approx_cny:.2f}）")
        pack_credits = int(PACK_CFG.get("credits") or 200)
        pack_amount = float(PACK_CFG.get("amount") or 9.9)
        if no_balance:
            print("当前额度: 未查询（--no-balance）")
            balance_view, unknown = 0, True
        elif balance is None:
            print("当前额度: 未知（网关不可达）")
            balance_view, unknown = 0, True
        else:
            print(f"当前额度: {balance} 点")
            balance_view, unknown = balance, False

        print("覆盖方案:")
        if has_non_per_call:
            if not unknown and balance_view >= total_credits:
                print(f"  - 当前余额足够，无需购买（执行后约剩 "
                      f"{balance_view - total_credits} 点）")
            else:
                short = total_credits - balance_view
                packs = max(1, -(-short // pack_credits))
                print(f"  - 额度包 ×{packs}：¥{pack_amount:.2f} / {pack_credits} 点"
                      f"（任务含高价值/批量，必须走额度）")
            print("  - 按次付款：不可用（任务含高价值/批量接口）")
        else:
            print(f"  - 按次付款：约 ¥{total_percall:.2f}（全部为标准接口）")
            if not unknown and balance_view >= total_credits:
                print(f"  - 额度扣费：当前 {balance_view} 点足够（执行后约剩 "
                      f"{balance_view - total_credits} 点）")
            elif total_percall >= pack_amount:
                print(f"  - 额度包 ×1：¥{pack_amount:.2f} / {pack_credits} 点"
                      "（比按次付款更划算）")
            else:
                print(f"  - 额度包（可选）：¥{pack_amount:.2f} / {pack_credits} 点"
                      "（本次按次更便宜）")
    else:
        print(f"上游成本合计: 约 ${total_usd:.4f}（由你的上游账户扣费）")
    print("预估仅供参考，实际以网关/上游扣费为准。")
    return summary


def _confirm_paid(items, args, title=""):
    """付费前打印清单并要求确认；--yes 或终端输入 y 才继续。"""
    if not IS_PRO:
        cost = sum(float(it["row"].get("unit_cost_usd") or 0) * int(it.get("repeat", 1))
                   for it in items)
        if cost:
            print(f"[cost] 本次调用上游成本约 ${cost:.4f}（由你的上游账户扣费）")
        return True
    summary = _estimate_items(items, title, json_out=False,
                              no_balance=getattr(args, "no_balance", False))
    if getattr(args, "dry_run", False):
        return True
    if getattr(args, "yes", False):
        return True
    if sys.stdin.isatty():
        try:
            answer = input("\n确认执行本次付费调用？输入 y 继续，其他任意键取消：").strip().lower()
        except (EOFError, KeyboardInterrupt):
            answer = ""
        if answer in ("y", "yes"):
            return True
        print("已取消，未发出请求。")
        sys.exit(5)
    print("\n未确认，未发出请求。确认后请加 --yes 重跑本命令。")
    sys.exit(5)


def cmd_show(args):
    rows = _load_rows()
    rows = _platform_filter(rows, _hint_platform(args.key, args.platform))
    if not rows:
        die(f"没有平台 {args.platform} 的接口；去掉 --platform 或换一个平台")
    hits = _find(rows, args.key) if rows else []
    if not hits:
        msg = f"没找到接口: {args.key}"
        sug = _suggest(args.key, rows)
        if sug:
            msg += "\n最接近的几个：\n" + "\n".join(
                f"  [{platform_zh_of(r['path'])}] {r['method']} {r['path']}"
                f"   # {r.get('name_zh') or r.get('name')}"
                for r in sug)
            msg += "\n先用 `search <关键词>` 缩小范围，再用完整 path `show`。"
        die(msg)
    r = hits[0]
    _print_entry(r)
    if len(hits) > 1:
        plat = {platform_of(x["path"]) for x in hits}
        extra = "（跨平台命中，可用 --platform 指定）" if len(plat) > 1 else ""
        print(f"\n另有 {len(hits)-1} 个同类候选{extra}：")
        for x in hits[1:15]:
            print(f"  [{platform_zh_of(x['path'])}] {x['method']} {x['path']}"
                  f"   # {x.get('name_zh') or x.get('name')}")


def cmd_list(args):
    rows = _load_rows()
    if not rows:
        die("接口清单不可用，且 references/*.md 也读不到")
    rows = _platform_filter(rows, args.platform)
    if args.folder:
        rows = [r for r in rows if r["folder"].lower() == args.folder.lower()]
        if not rows:
            folders = sorted({r["folder"] for r in _load_rows()})
            die(f"没有分类 {args.folder}；可选：" + "、".join(folders))
    if args.platform or args.folder:
        folders = {}
        for r in rows:
            folders[r["folder"]] = folders.get(r["folder"], 0) + 1
        for f, c in sorted(folders.items(), key=lambda x: (-x[1], x[0])):
            print(f"{c:4d}  {f}")
        print(f"合计 {len(rows)} 个接口")
        return

    # 无参数：按平台分组，只列分类与数量（不铺全量接口）
    by_platform = {}
    for r in rows:
        by_platform.setdefault(_row_platform(r), []).append(r)
    for slug, zh, _ in PLATFORMS:
        items = by_platform.pop(slug, [])
        if not items:
            continue
        print(f"\n{zh}（{slug}） {len(items)} 个接口")
        folders = {}
        for r in items:
            folders[r["folder"]] = folders.get(r["folder"], 0) + 1
        for f, c in sorted(folders.items(), key=lambda x: (-x[1], x[0])):
            print(f"  {c:4d}  {f}")
    for slug, items in sorted(by_platform.items()):
        print(f"\n{slug} {len(items)} 个接口")
    print(f"\n合计 {len(rows)} 个接口；用 `search <关键词>` 或 `show <path>` 查具体接口。")


# ---------------------------------------------------------------- 请求

def _raw_request(url, headers, body=None, timeout=TIMEOUT):
    data = None
    if body is not None:
        data = json.dumps(body, ensure_ascii=False).encode()
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers,
                                 method="POST" if body is not None else "GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, dict(resp.headers), resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), e.read().decode("utf-8", "replace")
    except Exception as e:
        # 交给上层判断能否重试，不再一遇网络抖动就整条命令失败
        raise NetError(f"{type(e).__name__}: {e}")


HINTS_FREE = {
    401: "token 无效/缺失：运行 `python3 scripts/social.py token <你的token>` 保存；"
         "token 在上游控制台生成（见 SKILL.md 的 Token 章节）",
    400: "上游拒绝了请求（多为接口暂时不可用或参数与文档不符），本次通常不计费；换同类通道或稍后重试",
    402: "余额不足：该接口需付费（部分不吃免费额度），先查上游账户余额或用免费 Demo 接口",
    403: "无权限：账号被停用 / 邮箱未验证 / token 权限不足",
    404: "接口路径不存在：检查 path（用 show 确认）",
    422: "参数不合法：看上面的字段级提示，或用 `show <path>` 核对必填项",
    429: "限流：降低并发或稍后重试（已自动重试仍失败就过 30s 再跑）",
    500: "服务端错误：已自动重试；持续失败换同类接口（如 Web → App V3）",
}

HINTS_PRO = {
    401: "账户 token 无效：运行 `python3 scripts/social.py recharge` 充值获取",
    400: "上游拒绝了请求（多为接口暂时不可用或参数与文档不符），本次未计费；换同类通道或稍后重试",
    402: "需要付款：完成支付宝付款后重试；已付款可用 --proof 手动重试",
    403: "无权限：账户被停用或接口未开放",
    404: "接口路径不存在：检查 path（用 show 确认）",
    422: "参数不合法：看上面的字段级提示，或用 `show <path>` 核对必填项",
    429: "限流：降低并发或稍后重试（已自动重试仍失败就过 30s 再跑）",
    500: "服务端/网关错误：已自动重试；持续失败换同类接口",
    502: "上游失败：本次未计费，可直接重试",
}

HINTS = HINTS_PRO if IS_PRO else HINTS_FREE


def _ua():
    return f"cn-social-data/{VERSION}"


def _direct_request(path, query=None, body=None, timeout=TIMEOUT):
    """免费版：直连上游 API。"""
    url = BASE + path
    if query:
        url += "?" + urllib.parse.urlencode({k: v for k, v in query.items() if v != ""})
    headers = {"Accept": "application/json", "User-Agent": _ua()}
    token = get_token()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return _raw_request(url, headers, body, timeout)


def _gateway_request(path, query=None, body=None, timeout=TIMEOUT, proof=""):
    """付费版：经网关。platform 由 path 推断，交给网关做白名单校验。"""
    if not GATEWAY:
        die("付费版未配置网关地址（skill_meta.json 的 gateway_url）")
    token = get_token()
    headers = {"Accept": "application/json", "User-Agent": _ua()}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if proof:
        headers["Payment-Proof"] = proof
    method = "POST" if body is not None else "GET"
    payload = {"platform": platform_of(path), "path": path, "method": method,
               "query": query or {}, "body": body}
    return _raw_request(GATEWAY + "/v1/call", headers, payload, timeout)


def _request(path, query=None, body=None, timeout=TIMEOUT, proof="", retry=2):
    """带自动重试：网络抖动 / 429 / 5xx 退避重试，其余状态码原样返回。"""
    attempt = 0
    while True:
        try:
            res = _gateway_request(path, query, body, timeout, proof) if IS_PRO \
                else _direct_request(path, query, body, timeout)
        except NetError as e:
            if attempt >= retry:
                die(f"请求失败（已重试 {retry} 次）：{e}\n"
                    "  排查：网络/代理是否可用？`ping` 能否连通？把 --timeout 调大再试")
            attempt += 1
            wait = 2 ** attempt
            print(f"[retry {attempt}/{retry}] 网络错误，{wait}s 后重试（{e}）",
                  file=sys.stderr)
            time.sleep(wait)
            continue
        status = res[0]
        if status in RETRY_STATUS and attempt < retry:
            attempt += 1
            retry_after = ""
            for k, v in res[1].items():
                if k.lower() == "retry-after":
                    retry_after = v
            wait = 2 ** attempt
            try:
                wait = max(wait, min(int(float(retry_after)), 30)) if retry_after else wait
            except ValueError:
                pass
            print(f"[retry {attempt}/{retry}] HTTP {status}，{wait}s 后重试",
                  file=sys.stderr)
            time.sleep(wait)
            continue
        return res


# ---------------------------------------------------------------- call

def _autofill(spec, given, where):
    """按清单里的默认值补参数，省掉"少传一个 count 就 422"的往返。"""
    filled = {}
    for p in spec or []:
        name = p.get("name")
        if not name or name in given or p.get("required") and p.get("default") in ("", None):
            continue
        typ = (p.get("type") or "").lower()
        default = p.get("default")
        if default in ("", None):
            cand = PAGE_DEFAULTS.get(name)
            # 游标类参数可能是字符串（微信 cursor、微博 max_id），类型不明时不要补数字
            if cand is None or typ == "string" or (
                    not typ and name in ("cursor", "max_cursor", "since_id", "max_id",
                                         "session_id", "search_id", "pcursor",
                                         "next_cursor", "token")):
                continue
            default = cand
        given[name] = default
        filled[name] = default
    if filled:
        print("[autofill] 已补默认参数(" + where + "): "
              + ", ".join(f"{k}={v}" for k, v in filled.items()), file=sys.stderr)
    return filled


def _spec_for(path):
    rows = load_inventory()
    if not rows:
        return None
    return next((r for r in rows if r["path"].lower() == path.lower()), None)


def _dry_run(path, query, body, spec):
    method = "POST" if body is not None else "GET"
    print("[dry-run] 不会发出请求、不计费")
    print(f"平台: {platform_zh_of(path)}（{platform_of(path)}）")
    if IS_PRO:
        print(f"POST {GATEWAY}/v1/call")
        print("Body: " + json.dumps({"platform": platform_of(path), "path": path,
                                     "method": method, "query": query, "body": body},
                                    ensure_ascii=False))
    else:
        print(f"{method} {BASE}{path}" + ("?" + urllib.parse.urlencode(query) if query else ""))
        print("Headers: Accept: application/json, "
              + ("Authorization: Bearer ***" if get_token() else "Authorization: (未配置 token)"))
        if body is not None:
            print("Body: " + json.dumps(body, ensure_ascii=False))
    if spec:
        print(f"接口: {spec.get('name_zh') or spec.get('name')}（{spec['method']}）")
        req_q = [p["name"] for p in spec.get("query_params") or [] if p.get("required")]
        req_b = [p["name"] for p in spec.get("body_params") or [] if p.get("required")]
        if req_q or req_b:
            print("必填: query=" + str(req_q) + " body=" + str(req_b))


def _plan_items(paths, file_path, repeat=1):
    """把命令行的路径或计划 JSON 转成 [{"row":..., "repeat":...}]。"""
    entries = []
    title = ""
    if file_path:
        try:
            plan = json.load(open(file_path, encoding="utf-8"))
        except Exception as e:
            die(f"计划文件读取失败：{e}")
        if isinstance(plan, list):
            raw = plan
        elif isinstance(plan, dict):
            raw = plan.get("endpoints") or []
            title = plan.get("title") or ""
        else:
            die("计划文件必须是数组，或含 endpoints 数组的对象")
        for e in raw:
            entries.append({"path": e} if isinstance(e, str) else dict(e))
    for p in paths or []:
        entries.append({"path": p})
    if not entries:
        die("没有可预估的接口：用 `estimate <path ...>` 或 `--file plan.json`")

    rows = load_inventory() or _md_rows()
    by_path = {r["path"]: r for r in rows}
    items = []
    for e in entries:
        path = _resolve_path(_norm(e["path"]), e.get("platform", ""))
        row = by_path.get(path)
        if row is None:
            row = {"path": path, "method": e.get("method", "GET"),
                   "name_zh": path, "unit_cost_usd": None}
        n = int(e.get("repeat", 1)) * int(repeat)
        items.append({"row": row, "repeat": max(1, n)})
    return title, items


def cmd_estimate(args):
    title, items = _plan_items(args.paths, args.file, args.repeat)
    summary = _estimate_items(items, args.title or title, json_out=args.json,
                              no_balance=args.no_balance)
    if args.json:
        return
    if IS_PRO:
        if summary["balance"] is not None and summary["total_credits"] > summary["balance"]:
            if summary["has_non_per_call"]:
                print("下一步：先 `recharge` 充值（高价值/批量只能走额度），"
                      "或直接执行让 CLI 自动购买。")
            else:
                print("下一步：可直接按次付款，或 `recharge` 买额度包。")
        print("确认后逐个执行：`python3 scripts/social.py call <path> --yes`；"
              "多接口任务建议先展示本清单给用户确认。")
    else:
        print("免费版无需确认；直接 `call <path>` 即可（费用由你的上游账户扣）。")


def _resolve_path(key, platform=""):
    """把简称/后缀解析成唯一 path；命中多个时列出候选并退出。"""
    rows = _load_rows()
    if not rows:
        die("清单不可用，无法把简称解析成完整 path；请传完整路径（可先 `search` 或用 references/*.md 查）")
    rows = _platform_filter(rows, _hint_platform(key, platform))
    hits = _find(rows, key)
    if len(hits) == 1:
        return hits[0]["path"]
    for r in hits[:12]:
        print(f"  [{platform_zh_of(r['path'])}] {r['method']} {r['path']}"
              f"   # {r.get('name_zh') or r.get('name')}")
    tip = "请传完整 /api/v1/<平台>/... 路径"
    if len(hits) > 1 and len({platform_of(r["path"]) for r in hits}) > 1:
        tip += "，或用 --platform 限定平台"
    die(f"路径需唯一，命中 {len(hits)} 个；{tip}")


def cmd_call(args):
    # Git Bash 会把 /api/... 改写成 C:/.../api/...，先归一化再判断
    path = _norm(args.path)
    if not path.startswith("/api/"):
        path = _resolve_path(path, args.platform)
    if args.platform and _match_platform(args.platform) != platform_of(path):
        die(f"--platform {args.platform} 与路径所属平台 "
            f"{platform_of(path)} 不一致")

    query = {}
    for kv in args.query or []:
        if "=" not in kv:
            die(f"--query 需要 k=v 形式: {kv}")
        k, v = kv.split("=", 1)
        query[k] = v

    body = None
    if args.body:
        try:
            body = json.loads(args.body)
        except Exception as e:
            die(f"--body 不是合法 JSON: {e}")
    if args.post:
        body = body or {}

    spec = _spec_for(path)

    # 预检 + 自动补全：先在本地把能查出来的问题拦掉，别用真金白银换 422
    if spec:
        is_post = spec["method"].upper() == "POST"
        if is_post and body is None:
            body = {}
        _autofill(spec.get("query_params"), query, "query")
        body_is_array = (spec.get("body_schema") or {}).get("type") == "array"
        if body is not None and not body_is_array:
            _autofill(spec.get("body_params"), body, "body")
        missing = [("query", p["name"]) for p in spec.get("query_params") or []
                   if p.get("required") and p["name"] not in query]
        if not body_is_array:
            missing += [("body", p["name"]) for p in spec.get("body_params") or []
                        if p.get("required") and p["name"] not in (body or {})]
        if missing and not args.force:
            print("[precheck] 还缺必填参数，未发出请求（不计费）：", file=sys.stderr)
            for where, name in missing:
                hint = next((p.get("desc", "") for p in (spec.get("query_params") or [])
                             + (spec.get("body_params") or []) if p.get("name") == name), "")
                print(f"  --{where} {name}=...   # {hint[:80]}", file=sys.stderr)
            print("  补上再调；确实要带缺参试一次，加 --force。"
                  f"完整参数表：python3 scripts/social.py show {path}", file=sys.stderr)
            sys.exit(3)

    est_row = spec or {"path": path, "method": "POST" if body is not None else "GET",
                       "name_zh": path, "unit_cost_usd": None}
    _confirm_paid([{"row": est_row}], args,
                  title=spec.get("name_zh") if spec else "单次接口调用")

    if args.dry_run:
        _dry_run(path, query, body, spec)
        return

    proof = getattr(args, "proof", "") or ""
    status, headers, text = _request(path, query, body,
                                     timeout=args.timeout, proof=proof,
                                     retry=args.retry)

    # 付费版 402：
    #   * 标准档按次：账单只覆盖本次调用，直接付款后重试
    #   * 高价值/批量：不按次卖，返回 CREDITS_REQUIRED；买额度包后重试
    if IS_PRO and status == 402 and not proof:
        needed = next((v for k, v in headers.items()
                       if k.lower() == "payment-needed"), None)
        if needed:
            try:
                bill = json.loads(_b64url_decode(needed))
            except Exception:
                die("网关返回的 Payment-Needed 账单解析失败")
            amount = (bill.get("protocol") or {}).get("amount")
            goods = (bill.get("method") or {}).get("goods_name") or "按次调用"
            if amount:
                print(f"需要按次付款：{goods}  ¥{amount}")
                bill_path = os.path.join(SKILL_DIR, ".payment-needed.txt")
                open(bill_path, "w", encoding="utf-8").write(needed)
                result = _alipay_bot_pay(bill_path, GATEWAY + "/v1/call",
                                         f"按次调用 {goods}")
                out = (result.stdout or "") + (result.stderr or "")
                print(out.strip()[:1500])
                proof = _extract_proof(out)
                if not proof:
                    die("没能从支付结果里取到 Payment-Proof，"
                        "可手动用 --proof 传入后重试")
                status, headers, text = _request(path, query, body,
                                                 timeout=args.timeout, proof=proof)
        else:
            try:
                info = json.loads(text)
            except Exception:
                info = {}
            if info.get("code") == "CREDITS_REQUIRED":
                need = info.get("credits_required")
                left = info.get("credits_left", 0)
                if not getattr(args, "no_auto_recharge", False):
                    print(f"[quota] 该接口需要 {need} 点额度（当前 {left} 点），"
                          "先购买额度包…")
                    if _buy_pack("starter"):
                        print("[quota] 额度已到账，重试本次调用…")
                        status, headers, text = _request(path, query, body,
                                                         timeout=args.timeout,
                                                         retry=args.retry)

    try:
        payload = json.loads(text)
    except Exception:
        payload = None

    if status != 200:
        try:
            err = json.loads(text)
        except Exception:
            err = {}
        if status == 402 and isinstance(err, dict) and err.get("code") == "CREDITS_REQUIRED":
            print(f"高价值/批量接口需要 {err.get('credits_required')} 点额度、"
                  f"当前 {err.get('credits_left', 0)} 点。")
            print("先运行 `python3 scripts/social.py recharge` 购买 "
                  "¥9.90 / 200 点，再重试本次调用。")
            sys.exit(4)
        print(f"HTTP {status}: {HINTS.get(status, '')}")
        if IS_PRO and status == 402:
            print("  可完成支付宝付款后用 --proof 手动重试")
        if status == 404:
            sug = _suggest(path, _load_rows(), n=3)
            if sug:
                print("  是不是这几个？")
                for r in sug:
                    print(f"    [{platform_zh_of(r['path'])}] {r['method']} {r['path']}"
                          f"   # {r.get('name_zh') or r.get('name')}")
        if status == 422:
            try:
                det = json.loads(text).get("detail")
            except Exception:
                det = None
            if isinstance(det, list):
                for e in det:
                    loc = ".".join(str(x) for x in e.get("loc") or [])
                    print(f"  参数问题: {loc} -> {e.get('msg')}（{e.get('type')}）")
                print("  提示: 必填参数漏了，用 show 看完整参数表")
        print(text[:2000])
        sys.exit(2)

    if payload is None:
        print(text[:args.preview])
        return

    data = payload.get("data")
    if IS_PRO:
        # 网关包了一层：{code, data, meta}
        meta = payload.get("meta") or {}
        if meta:
            print(f"[quota] {meta.get('tier')} 档，本次扣 {meta.get('unit_cost')}，"
                  f"剩余 {meta.get('credits_left')}")
        inner = data
    else:
        info = {k: payload.get(k) for k in
                ("code", "message", "message_zh", "router", "cache_url") if k in payload}
        print(json.dumps(info, ensure_ascii=False))
        inner = data

    if args.raw:
        print(json.dumps(payload, ensure_ascii=False))
        return

    print(f"data 类型: {type(inner).__name__}"
          + (f", 长度 {len(inner)}" if isinstance(inner, (list, dict)) else ""))
    explained = False
    if inner is None and isinstance(payload, dict):
        # 有些接口不套 data，真实内容在 business_data 等顶层字段，
        # 只说 "data 为 null" 会把人带偏，这里直接把有内容的顶层字段列出来
        extra = {k: v for k, v in payload.items()
                 if k not in ("code", "message", "message_zh", "router",
                              "cache_url", "data") and v not in (None, "", [], {})}
        if extra:
            print("[note] data 为空，内容在其它顶层字段里：")
            for k, v in extra.items():
                desc = f"{type(v).__name__}" + (f"[{len(v)}]" if isinstance(v, (list, dict)) else "")
                print(f"  {k}: {desc}")
            print("  提示：用 --out 落盘后按上面字段取数据；`show` 里也能看到实测结构。")
            explained = True
    s = inner if isinstance(inner, str) else json.dumps(inner, ensure_ascii=False, indent=1)
    if args.out:
        # data 为空时落盘完整响应，而不是 "null"
        content = inner if isinstance(inner, str) else (
            json.dumps(inner, ensure_ascii=False, indent=1) if inner is not None else text)
        out_dir = os.path.dirname(os.path.abspath(args.out))
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)   # out/ 不存在时别直接抛异常
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"已保存到 {args.out}（{len(content)} 字符）")
    elif not explained:
        print(s[:args.preview] + ("\n...(截断，用 --out 存全量或 --preview N)"
                                  if len(s) > args.preview else ""))


# ---------------------------------------------------------------- doctor

def cmd_doctor(args):
    """一条命令看清"这包装好没有"：环境、清单、文档、凭证、网络。"""
    problems = []
    notes = []
    print(f"== {SKILL_ZH} 自检（CLI {VERSION} / {EDITION}）==")
    print(f"python    : {sys.version.split()[0]}  ({sys.executable})")
    if sys.version_info < (3, 8):
        problems.append("Python 版本低于 3.8")
    print(f"skill 目录: {SKILL_DIR}")
    if not os.path.isdir(SKILL_DIR):
        problems.append(f"skill 目录不存在：{SKILL_DIR}")

    if META:
        print(f"元信息    : OK（skill={SKILL_NAME}, 平台 {len(PLATFORMS)} 个, "
              f"base={BASE or '-'}）")
    else:
        problems.append(f"skill_meta.json 缺失或损坏：{META_PATH}")

    rows = load_inventory()
    if rows:
        by_plat = {}
        for r in rows:
            slug = _row_platform(r)
            by_plat[slug] = by_plat.get(slug, 0) + 1
        folders = {r["folder"] for r in rows}
        print(f"清单      : OK，{len(rows)} 个接口 / {len(folders)} 个分类")
        print("            " + "，".join(f"{PLATFORM_ZH.get(k, k)} {v}"
                                       for k, v in by_plat.items()))
        print(f"文件      : {INV}（{os.path.getsize(INV)} bytes）")
        nofile = [f for f in folders
                  if not os.path.exists(os.path.join(REF_DIR, f + ".md"))]
        if nofile:
            notes.append("以下分类缺参考文档（search/show 仍可用）：" + "、".join(sorted(nofile)))
    else:
        problems.append(inventory_error() or "接口清单不可用")
        blocks = _md_blocks()
        print(f"降级      : references/*.md 解析到 {len(blocks)} 个条目")
        if not blocks:
            problems.append("references/*.md 也没有可解析内容，skill 包不完整")

    for extra in ("index.md", "_meta.json"):
        p = os.path.join(REF_DIR, extra)
        print(f"{extra:10}: {'OK' if os.path.exists(p) else '缺失'}")

    env_tok = os.environ.get("TIKHUB_API_KEY", "").strip()
    tok = get_token()
    if env_tok:
        print(f"凭证      : 环境变量 TIKHUB_API_KEY（长度 {len(env_tok)}）")
    elif tok:
        print(f"凭证      : {TOKEN_FILE}（{tok[:6]}...{tok[-4:]}）")
    else:
        notes.append("未配置 token：search/show/list 可用，真实调用会 401；"
                     "Demo 接口（通用/演示）可先跑通链路")

    if args.net:
        print("网络      : 检测中…")
        try:
            if IS_PRO:
                if not GATEWAY:
                    problems.append("付费版未配置 gateway_url")
                else:
                    status, _, _ = _raw_request(GATEWAY + "/healthz",
                                                {"Accept": "application/json"}, None, 15)
                    print(f"网络      : OK（HTTP {status}）")
            else:
                status, _, _ = _direct_request("/api/v1/tikhub/user/get_user_info",
                                               None, None, 15)
                print(f"网络      : OK（HTTP {status}）")
                if status in (401, 403):
                    notes.append("网络通，但凭证被拒（看上面的 401/403 提示）")
        except NetError as e:
            problems.append(f"网络不可达：{e}")

    print("\n== 结论 ==")
    for p in problems:
        print(f"[FAIL] {p}")
    for n in notes:
        print(f"[NOTE] {n}")
    if not problems:
        print("[OK] 环境、清单、文档都齐，可以正常使用。")
    print("\n常用：search <关键词> | show <path> | call <path> -q k=v --out out/x.json")
    sys.exit(1 if problems else 0)


# ---------------------------------------------------------------- token / ping

def cmd_token(args):
    if args.token_value:
        p = save_token(args.token_value.strip())
        print(f"已保存 token 到 {p}")
        return
    t = get_token()
    if not t:
        if IS_PRO:
            print("未配置账户 token。运行 `python3 scripts/social.py recharge` 充值获取。")
        else:
            print("未配置 token。到上游控制台生成后执行: "
                  "python3 scripts/social.py token <token>")
        return
    print(f"当前 token: {t[:6]}...{t[-4:]} (长度 {len(t)})")


def cmd_ping(args):
    if IS_PRO:
        if not GATEWAY:
            die("付费版未配置网关地址（skill_meta.json 的 gateway_url）")
        status, _, text = _raw_request(GATEWAY + "/healthz", {"Accept": "application/json"})
        print(f"gateway HTTP {status}")
        print(text[:800])
        return
    if not get_token():
        die("未配置 token，先运行: python3 scripts/social.py token <token>")
    status, _, text = _direct_request("/api/v1/tikhub/user/get_user_info")
    print(f"HTTP {status}")
    print(text[:800])


def _gateway_get(path, timeout=TIMEOUT):
    """付费版只读查询：带账户 token 的 GET。"""
    if not GATEWAY:
        die("付费版未配置网关地址（skill_meta.json 的 gateway_url）")
    token = get_token()
    if not token:
        die("未配置账户 token。先运行 `python3 scripts/social.py recharge` 购买额度包。")
    headers = {"Accept": "application/json", "User-Agent": _ua(),
               "Authorization": f"Bearer {token}"}
    return _raw_request(GATEWAY + path, headers, None, timeout)


def cmd_balance(args):
    status, _, text = _gateway_get("/v1/balance")
    if status != 200:
        print(f"HTTP {status}: {HINTS.get(status, '')}")
        print(text[:800])
        sys.exit(2)
    data = json.loads(text)
    print(f"剩余额度: {data.get('credits', 0)} credits")
    print(f"累计购买: {data.get('purchased', 0)} credits")
    print(f"累计消耗: {data.get('consumed', 0)} credits")
    print(f"累计退款: {data.get('refunded', 0)} credits")
    print(f"账户 token: {data.get('token', '')}")


def cmd_usage(args):
    limit = max(1, min(int(args.limit), 100))
    status, _, text = _gateway_get(f"/v1/usage?limit={limit}")
    if status != 200:
        print(f"HTTP {status}: {HINTS.get(status, '')}")
        print(text[:800])
        sys.exit(2)
    data = json.loads(text)
    print(f"剩余额度: {data.get('credits', 0)} credits")
    print(f"累计购买: {data.get('purchased', 0)}  / "
          f"累计消耗: {data.get('consumed', 0)}  / "
          f"累计退款: {data.get('refunded', 0)}")
    calls = data.get("calls") or []
    if not calls:
        print("暂无调用记录。")
        return
    print("\n最近调用：")
    for c in calls:
        print(f"  {c.get('created_at', '')}  {c.get('tier', ''):8s} "
              f"-{c.get('unit_cost', 0):<2d}  {c.get('status', ''):8s} "
              f"{c.get('path', '')}")


# ---------------------------------------------------------------- 付费版充值

def _alipay_bot_pay(bill_path, resource_url, intent):
    """调用支付宝买家侧 CLI（@alipay/agent-payment 提供的 alipay-bot）。"""
    cmd = ["alipay-bot", "402-buyer-pay",
           "--session-id", "cn-social-data-recharge",
           "--file", bill_path,
           "--resource-url", resource_url,
           "--method", "POST",
           "--intent-summary", intent]
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    except FileNotFoundError:
        die("没找到 alipay-bot。付费版需要安装买家侧支付依赖：\n"
            "  npx -y @alipay/agent-payment@latest install\n"
            "装好后重新运行本次命令。")
    except subprocess.TimeoutExpired:
        die("支付超时，未完成付款。")


def _buy_pack(pack="starter", proof="") -> bool:
    """购买额度包：402 → alipay-bot 付款 → 带 proof 兑换账户 token。

    成功返回 True，并把新 token 保存到本地；失败打印原因并返回 False。
    """
    if not GATEWAY:
        die("付费版未配置网关地址（skill_meta.json 的 gateway_url）")
    body = {"pack": pack}
    headers0 = {"Accept": "application/json", "User-Agent": _ua()}
    tok = get_token()
    if tok:
        # 已有账户时并入原账户，避免充值后旧额度被新 token 顶掉
        headers0["Authorization"] = f"Bearer {tok}"
    status, headers, text = _raw_request(GATEWAY + "/v1/recharge", headers0, body)

    if status == 402 and not proof:
        needed = None
        for k, v in headers.items():
            if k.lower() == "payment-needed":
                needed = v
                break
        if not needed:
            print("网关返回 402 但没有 Payment-Needed 头", file=sys.stderr)
            return False
        try:
            bill = json.loads(_b64url_decode(needed))
        except Exception:
            print("账单解析失败", file=sys.stderr)
            return False
        amount = bill.get("protocol", {}).get("amount")
        goods = bill.get("method", {}).get("goods_name")
        print(f"需要付款：{goods}  ¥{amount}")
        # 真实支付交给官方 CLI，本脚本只负责编排
        bill_path = os.path.join(SKILL_DIR, ".payment-needed.txt")
        open(bill_path, "w", encoding="utf-8").write(needed)
        result = _alipay_bot_pay(bill_path, GATEWAY + "/v1/recharge",
                                 f"充值 {goods}")
        out = (result.stdout or "") + (result.stderr or "")
        print(out.strip()[:1500])
        proof = _extract_proof(out)
        if not proof:
            print("没能从支付结果里取到 Payment-Proof，可手动用 --proof 传入",
                  file=sys.stderr)
            return False

    if status == 402 and proof:
        headers1 = {"Accept": "application/json", "User-Agent": _ua(),
                    "Payment-Proof": proof}
        if tok:
            headers1["Authorization"] = f"Bearer {tok}"
        status, _, text = _raw_request(GATEWAY + "/v1/recharge", headers1, body)

    try:
        payload = json.loads(text)
    except Exception:
        payload = {}

    if status != 200:
        print(f"HTTP {status}: {HINTS.get(status, '')}", file=sys.stderr)
        print(text[:800], file=sys.stderr)
        return False

    data = payload.get("data") or {}
    token = data.get("token")
    if not token:
        print(f"网关没有返回 token：{text[:300]}", file=sys.stderr)
        return False
    p = save_token(token)
    print(f"充值成功：{data.get('credits')} 点额度，token 已保存到 {p}")
    print(f"订单 {payload.get('out_trade_no')}  trade_no {payload.get('trade_no')}")
    return True


def cmd_recharge(args):
    if not IS_PRO:
        die("免费版无需在此充值，用你自己的 token：python3 scripts/social.py token <token>")
    pack_credits = int(PACK_CFG.get("credits") or 200)
    pack_amount = PACK_CFG.get("amount") or "9.90"
    print(f"\n== 购买额度包 ==\n商品: 额度包 ¥{pack_amount} / {pack_credits} 点")
    print("用途: 高价值/批量接口只能扣点；标准接口有额度时也优先扣点。")
    print("支付: 支付宝 AI 按量付费（alipay-bot）")
    if not getattr(args, "yes", False):
        if sys.stdin.isatty():
            try:
                answer = input("确认购买？输入 y 继续，其他任意键取消：").strip().lower()
            except (EOFError, KeyboardInterrupt):
                answer = ""
            if answer not in ("y", "yes"):
                print("已取消，未发起支付。")
                sys.exit(5)
        else:
            print("未确认，未发起支付。确认后请加 --yes 重跑本命令。")
            sys.exit(5)
    if not _buy_pack(args.pack or "starter", args.proof or ""):
        sys.exit(2)


def _b64url_decode(text):
    import base64
    pad = 4 - len(text) % 4
    if pad != 4:
        text += "=" * pad
    return base64.urlsafe_b64decode(text).decode("utf-8")


def _extract_proof(text):
    """从 alipay-bot 输出里找 Payment-Proof 值。"""
    import re
    m = re.search(r"Payment-Proof[:=]\s*([A-Za-z0-9_\-=]+)", text, re.I)
    return m.group(1) if m else ""


# ---------------------------------------------------------------- 入口

def main():
    ap = argparse.ArgumentParser(
        description=f"{SKILL_ZH} CLI（{EDITION} v{VERSION}）",
        epilog="首次使用先跑 doctor 自检；call 前可用 show 看参数、--dry-run 预览请求。")
    ap.add_argument("--version", action="version",
                    version=f"{SKILL_NAME} {VERSION} ({EDITION})")
    sub = ap.add_subparsers(dest="cmd")

    s = sub.add_parser("doctor", help="自检：环境/清单/文档/凭证（推荐第一步）")
    s.add_argument("--net", action="store_true", help="额外检测网络连通性")
    s.set_defaults(func=cmd_doctor)

    s = sub.add_parser("search", help="搜索接口（跨平台）")
    s.add_argument("keyword", nargs="+")
    s.add_argument("--platform", help="只看某个平台（slug 或中文名）")
    s.add_argument("--limit", type=int, default=25)
    s.set_defaults(func=cmd_search)

    s = sub.add_parser("show", help="查看接口详情")
    s.add_argument("key")
    s.add_argument("--platform", help="只在某个平台内匹配")
    s.set_defaults(func=cmd_show)

    s = sub.add_parser("list", help="按平台/分类列出")
    s.add_argument("--platform", help="只看某个平台（slug 或中文名）")
    s.add_argument("--folder")
    s.set_defaults(func=cmd_list)

    s = sub.add_parser("call", help="调用接口")
    s.add_argument("path")
    s.add_argument("--platform", help="短路径命中多个平台时用于消歧")
    s.add_argument("--query", "-q", action="append", help="k=v，可重复")
    s.add_argument("--body", "-b", help="JSON 字符串，作为请求体(POST)")
    s.add_argument("--post", action="store_true", help="强制 POST，无 body 时发空对象")
    s.add_argument("--out", "-o", help="把 data 存到文件（目录不存在会自动建）")
    s.add_argument("--preview", type=int, default=1500)
    s.add_argument("--raw", action="store_true", help="输出完整响应")
    s.add_argument("--timeout", type=int, default=TIMEOUT)
    s.add_argument("--retry", type=int, default=2,
                   help="网络错误/429/5xx 自动重试次数，默认 2，0 为关闭")
    s.add_argument("--dry-run", action="store_true",
                   help="只打印将要发出的请求，不发送、不计费")
    s.add_argument("--force", action="store_true",
                   help="必填参数缺失时仍然发送（默认拦截）")
    s.add_argument("--proof", help="手动传入 Payment-Proof，跳过付款步骤（联调用）")
    s.add_argument("--no-auto-recharge", action="store_true",
                   help="额度不足时只提示充值，不自动购买额度包")
    s.add_argument("--yes", "-y", action="store_true",
                   help="跳过付费前确认（agent 已向用户确认后使用）")
    s.add_argument("--no-balance", action="store_true",
                   help="预估时不查询当前额度（避免额外网络请求）")
    s.set_defaults(func=cmd_call)

    s = sub.add_parser("estimate", help="付费前预估：接口数、档位、额度与套餐")
    s.add_argument("paths", nargs="*", help="一个或多个接口路径/简称")
    s.add_argument("--file", help="计划 JSON：{\"title\":..., \"endpoints\":[{\"path\":...,\"repeat\":N}]}")
    s.add_argument("--repeat", type=int, default=1, help="所有接口统一重复次数（分页/批量）")
    s.add_argument("--title", help="任务名（展示用）")
    s.add_argument("--json", action="store_true", help="输出机器可读 JSON")
    s.add_argument("--no-balance", action="store_true", help="不查询当前额度")
    s.set_defaults(func=cmd_estimate)

    s = sub.add_parser("token", help="查看/保存 token")
    s.add_argument("token_value", nargs="?")
    s.set_defaults(func=cmd_token)

    s = sub.add_parser("ping", help="验证网络/凭证")
    s.set_defaults(func=cmd_ping)

    if IS_PRO:
        s = sub.add_parser("balance", help="查询剩余额度")
        s.set_defaults(func=cmd_balance)

        s = sub.add_parser("usage", help="查询最近调用与消耗")
        s.add_argument("--limit", type=int, default=20, help="返回最近 N 条，最多 100")
        s.set_defaults(func=cmd_usage)

        s = sub.add_parser("recharge", help="充值额度（需要买家侧支付依赖）")
        s.add_argument("--pack", default="starter")
        s.add_argument("--proof", help="手动传入 Payment-Proof，跳过 payment 步骤（联调用）")
        s.add_argument("--yes", "-y", action="store_true",
                       help="跳过购买前确认（agent 已向用户确认后使用）")
        s.set_defaults(func=cmd_recharge)

    args = ap.parse_args()
    if not getattr(args, "func", None):
        ap.print_help()
        sys.exit(0)
    args.func(args)


if __name__ == "__main__":
    main()
