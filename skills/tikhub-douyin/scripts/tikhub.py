#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""TikHub 数据接口 CLI（平台无关、版本无关）。

同一个文件由 build.py 分发到 8 个 skill 里，运行时的平台与版本从
脚本同级目录的 skill_meta.json 读取：

    {"platform": "douyin", "platform_zh": "抖音",
     "edition": "free",  "base_url": "https://api.tikhub.io",
     "gateway_url": ""}

自备 API Key 版（edition=free）：用户自己的 TikHub Token，直连 api.tikhub.io
付费版（edition=pro） ：经作者网关转发，按次 402 付费

用法:
  python tikhub.py doctor                      # 自检：环境/清单/凭证一次看完
  python tikhub.py search "关键词"             # 搜接口
  python tikhub.py show <关键词或path>          # 看接口参数
  python tikhub.py list [--folder X]           # 按分类列
  python tikhub.py call <path> [--query k=v ...] [--body '{...}'] [--dry-run]
  python tikhub.py token [<token>]             # 查看/保存凭证
  python tikhub.py ping                        # 验证凭证
  python tikhub.py recharge [--pack starter] [--proof X]   # 仅付费版：充值

兼容性约定（很重要）：
  * 解释器：`python3` 优先，老环境用 `python`；脚本同时兼容 Python 3.8+。
  * 运行目录：脚本用 __file__ 定位 skill 根目录，在任意 cwd 下都能跑；
    但仍建议用 `python3 <skill目录>/scripts/tikhub.py ...` 的绝对路径调用，
    避免 agent 在别的目录里 `python scripts/tikhub.py` 找不到文件。
  * 清单缺失/损坏不影响 call：只要给完整 path 仍可直连，search/show 会退回
    扫 references/*.md 的降级模式，并给出修复提示。
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

VERSION = "1.1.0"

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
PLATFORM = META.get("platform", "")
PLATFORM_ZH = META.get("platform_zh", PLATFORM) or "抖音"
EDITION = META.get("edition", "free")
BASE = (META.get("base_url") or "https://api.tikhub.io").rstrip("/")
GATEWAY = (META.get("gateway_url") or "").rstrip("/")
API_PREFIX = META.get("api_prefix") or (f"/api/v1/{PLATFORM}" if PLATFORM else "")
IS_PRO = EDITION == "pro"
TOKEN_FILE = HOME_GW_TOKEN if IS_PRO else HOME_TOKEN


# ---------------------------------------------------------------- 凭证

def _read(p):
    if os.path.exists(p):
        t = open(p, encoding="utf-8").read().strip()
        return t[7:].strip() if t.lower().startswith("bearer ") else t
    return ""


def get_token():
    """自备 API Key 版优先级：环境变量 > skill/.token > ~/.workbuddy/tikhub_token"""
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
    try:
        os.chmod(TOKEN_FILE, 0o600)
    except Exception:
        pass
    return TOKEN_FILE


# ---------------------------------------------------------------- 接口清单

_INV_CACHE = {"rows": None, "err": ""}


def load_inventory():
    """读清单；失败返回 [] 并记下原因，由调用方决定降级还是退出。

    以前这里直接 die()，一旦 inventory.json 缺失/损坏，search/show 全线报错，
    只剩"背下完整 path 再 call"一条路。现在改成可降级。
    """
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
    """降级通道：把 references/<分类>.md 解析成条目，清单坏了也能搜索。

    文档结构固定为「## 标题 / `METHOD /path` / 参数列表」，按二级标题切块即可。
    """
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
    """按精确度分层返回候选：完整 path > path 结尾 > path 包含 > 名称包含。

    分层后 `show web/fetch_video_comments` 只会命中 web 那一条，
    不再因为"命中 2 个"就只丢一张列表让你自己再查一遍。
    """
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


# ---------------------------------------------------------------- 本地命令

def _repair_hint():
    """清单不可用时的修复指引，直接告诉人/agent 下一步做什么。"""
    warn(f"{inventory_error()}；已切到降级模式（扫 references/*.md）")
    print("[降级] 修复方式：确认 skill 包完整（应有 references/inventory.json，约 400KB），"
          "缺失就用 build.py 重新生成；期间可用 `list`、`search`（走 md 扫描）"
          "或直接翻 references/<分类>.md。", file=sys.stderr)


def _md_rows():
    """把 md 块转成与 inventory 同形状的字段，供 search/show 复用同一套打印逻辑。"""
    out = []
    for b in _md_blocks():
        out.append({"folder": b["folder"], "name": b["title"], "name_zh": b["title"],
                    "name_en": "", "method": b["method"], "path": b["path"],
                    "purpose": "", "returns": "", "query_params": [], "body_params": [],
                    "request_example": "", "doc": "", "_md_text": b["text"]})
    return out


def cmd_search(args):
    rows = load_inventory()
    if not rows:
        rows = _md_rows()
        if rows:
            _repair_hint()
    if not rows:
        die("接口清单和 references/*.md 都读不到，skill 包疑似不完整："
            "重新解压/构建该 skill 后再试")
    kw = [k.lower() for k in args.keyword]
    hits = [r for r in rows
            if all(k in " ".join([r.get("name", ""), r.get("name_zh", ""),
                                  r.get("name_en", ""), r.get("path", ""),
                                  r.get("purpose", ""), r.get("folder", "")]).lower()
                   for k in kw)]
    relaxed = False
    if not hits and len(kw) > 1:
        # 多关键词按 AND 搜不到时退一步按 OR 再搜，避免"加了个词就 0 结果"
        hits = [r for r in rows
                if any(k in " ".join([r.get("name", ""), r.get("name_zh", ""),
                                      r.get("path", ""), r.get("purpose", "")]).lower()
                       for k in kw)]
        relaxed = bool(hits)
    if not hits:
        print(f"没匹配到接口（关键词: {' '.join(args.keyword)}）")
        sug = _suggest(" ".join(args.keyword), rows)
        if sug:
            print("相近的接口：")
            for r in sug:
                print(f"  {r['method']} {r['path']}   # {r.get('name_zh') or r.get('name')}")
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
        print(f"- [{r['folder']}] {r.get('name_zh') or r.get('name')}")
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
    if IS_PRO:
        print(f"接口 {r['method']} {r['path']}")
        print(f"经由网关 POST {GATEWAY}/v1/call（按次付费）")
    else:
        print(f"{r['method']} {BASE}{r['path']}")
    print(f"文件夹: {r['folder']}")
    if r.get("purpose"):
        print(f"用途: {r['purpose']}")
    if r.get("returns"):
        print(f"返回: {r['returns']}")
    if r.get("query_params"):
        _print_params("Query 参数", r["query_params"])
    if r.get("body_params"):
        _print_params("Body(JSON) 参数", r["body_params"])
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
        # 降级模式：md 里就是完整条目，原样输出
        print("\n--- references 原文 ---\n" + r["_md_text"])
    if r.get("query_params") or r.get("body_params"):
        print("\n下一步：python3 scripts/tikhub.py call "
              f"{r['path']} -q k=v --out out/result.json")


def cmd_show(args):
    rows = load_inventory()
    if not rows:
        rows = _md_rows()
        if rows:
            _repair_hint()
    hits = _find(rows, args.key) if rows else []
    if not hits:
        msg = f"没找到接口: {args.key}"
        sug = _suggest(args.key, rows)
        if sug:
            msg += "\n最接近的几个：\n" + "\n".join(
                f"  {r['method']} {r['path']}   # {r.get('name_zh') or r.get('name')}"
                for r in sug)
            msg += "\n先用 `search <关键词>` 缩小范围，再用完整 path `show`。"
        die(msg)
    r = hits[0]
    _print_entry(r)
    if len(hits) > 1:
        print(f"\n另有 {len(hits)-1} 个同类候选（去掉关键词或用完整 path 精确定位）：")
        for x in hits[1:15]:
            print(f"  {x['method']} {x['path']}   # {x.get('name_zh') or x.get('name')}")


def cmd_list(args):
    rows = load_inventory()
    if not rows:
        rows = _md_rows()
        if rows:
            _repair_hint()
    if not rows:
        die("接口清单不可用，且 references/*.md 也读不到")
    if args.folder:
        rows = [r for r in rows if r["folder"].lower() == args.folder.lower()]
        if not rows:
            folders = sorted({r["folder"] for r in _md_rows() or load_inventory()})
            die(f"没有分类 {args.folder}；可选：" + "、".join(folders))
    folders = {}
    for r in rows:
        folders[r["folder"]] = folders.get(r["folder"], 0) + 1
    for f, c in sorted(folders.items(), key=lambda x: -x[1]):
        print(f"{c:4d}  {f}")
    print(f"合计 {len(rows)} 个接口")


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
    401: "token 无效/缺失：运行 `python3 scripts/tikhub.py token <你的token>` 保存；token 在 https://user.tikhub.io 生成",
    400: "上游拒绝了请求（多为接口暂时不可用或参数与文档不符），本次通常不计费；换同类通道或稍后重试",
    402: "余额不足：该接口需付费（部分不吃免费额度），先查账户余额或用免费 Demo 接口",
    403: "无权限：账号被停用 / 邮箱未验证 / token 权限不足",
    404: "接口路径不存在：检查 path（用 show 确认）",
    422: "参数不合法：看上面的字段级提示，或用 `show <path>` 核对必填项",
    429: "限流：降低并发或稍后重试（已自动重试仍失败就过 30s 再跑）",
    500: "服务端错误：已自动重试；持续失败换同类接口（如 Web → App V3）",
}

HINTS_PRO = {
    401: "账户 token 无效：运行 `python3 scripts/tikhub.py recharge` 充值获取",
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


def _direct_request(path, query=None, body=None, timeout=TIMEOUT):
    """自备 API Key 版：直连 TikHub。"""
    url = BASE + path
    if query:
        url += "?" + urllib.parse.urlencode({k: v for k, v in query.items() if v != ""})
    headers = {"Accept": "application/json",
               "User-Agent": f"tikhub-{PLATFORM}-skill/{VERSION}"}
    token = get_token()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return _raw_request(url, headers, body, timeout)


def _gateway_request(path, query=None, body=None, timeout=TIMEOUT, proof=""):
    """付费版：经网关。"""
    if not GATEWAY:
        die("付费版未配置网关地址（skill_meta.json 的 gateway_url）")
    token = get_token()
    headers = {"Accept": "application/json",
               "User-Agent": f"tikhub-{PLATFORM}-skill/{VERSION}"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if proof:
        headers["Payment-Proof"] = proof
    method = "POST" if body is not None else "GET"
    payload = {"platform": PLATFORM, "path": path, "method": method,
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
        default = p.get("default")
        if default in ("", None):
            default = PAGE_DEFAULTS.get(name)
        if default in ("", None):
            continue
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


def cmd_call(args):
    # Git Bash 会把 /api/... 改写成 C:/.../api/...，先归一化再判断
    path = _norm(args.path)
    rows = load_inventory()
    if not path.startswith("/"):
        if not rows:
            die("清单不可用，无法把简称解析成完整 path；请传完整路径（可先 `search` 或用 references/*.md 查）")
        hits = _find(rows, path)
        if len(hits) != 1:
            for r in hits[:10]:
                print(f"  {r['method']} {r['path']}   # {r.get('name_zh') or r.get('name')}")
            die(f"路径需唯一，命中 {len(hits)} 个；请传完整 /api/v1/{PLATFORM or 'douyin'}/... 路径")
        path = hits[0]["path"]

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
        if body is not None:
            _autofill(spec.get("body_params"), body, "body")
        missing = [("query", p["name"]) for p in spec.get("query_params") or []
                   if p.get("required") and p["name"] not in query]
        missing += [("body", p["name"]) for p in spec.get("body_params") or []
                    if p.get("required") and p["name"] not in (body or {})]
        if missing and not args.force:
            print("[precheck] 还缺必填参数，未发出请求（不计费）：", file=sys.stderr)
            for where, name in missing:
                hint = next((p.get("desc", "") for p in (spec.get("query_params") or [])
                             + (spec.get("body_params") or []) if p.get("name") == name), "")
                print(f"  --{where} {name}=...   # {hint[:80]}", file=sys.stderr)
            print(f"  补上再调；确实要带缺参试一次，加 --force。"
                  f"完整参数表：python3 scripts/tikhub.py show {path}", file=sys.stderr)
            sys.exit(3)

    if args.dry_run:
        _dry_run(path, query, body, spec)
        return

    proof = getattr(args, "proof", "") or ""
    status, headers, text = _request(path, query, body,
                                     timeout=args.timeout, proof=proof,
                                     retry=args.retry)

    # 付费版按次 402：唤起支付宝买家侧付款，拿到 Payment-Proof 后重试同一请求
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

    try:
        payload = json.loads(text)
    except Exception:
        payload = None

    if status != 200:
        print(f"HTTP {status}: {HINTS.get(status, '')}")
        if IS_PRO and status == 402:
            print("  可完成支付宝付款后用 --proof 手动重试")
        if status == 404:
            sug = _suggest(path, rows or _md_rows(), n=3)
            if sug:
                print("  是不是这几个？")
                for r in sug:
                    print(f"    {r['method']} {r['path']}   # "
                          f"{r.get('name_zh') or r.get('name')}")
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
        # 有些接口不套 data（如 general_search_v2 的真实内容在 business_data），
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
    print(f"== {PLATFORM_ZH} skill 自检（CLI {VERSION} / {EDITION}）==")
    print(f"python    : {sys.version.split()[0]}  ({sys.executable})")
    if sys.version_info < (3, 8):
        problems.append("Python 版本低于 3.8")
    print(f"skill 目录: {SKILL_DIR}")
    if not os.path.isdir(SKILL_DIR):
        problems.append(f"skill 目录不存在：{SKILL_DIR}")

    # 元信息
    if META:
        print(f"元信息    : OK（platform={PLATFORM}, base={BASE or '-'}）")
    else:
        problems.append(f"skill_meta.json 缺失或损坏：{META_PATH}")

    # 清单
    rows = load_inventory()
    if rows:
        folders = {}
        for r in rows:
            folders[r["folder"]] = folders.get(r["folder"], 0) + 1
        print(f"清单      : OK，{len(rows)} 个接口 / {len(folders)} 个分类")
        print("           " + "，".join(f"{k} {v}" for k, v in
                                       sorted(folders.items(), key=lambda x: -x[1])[:6]))
        print(f"文件      : {INV}（{os.path.getsize(INV)} bytes）")
        nofile = [f for f in folders
                  if not os.path.exists(os.path.join(REF_DIR, f + ".md"))]
        if nofile:
            notes.append("以下分类缺参考文档（search/show 仍可用）：" + "、".join(nofile))
    else:
        problems.append(inventory_error() or "接口清单不可用")
        blocks = _md_blocks()
        print(f"降级      : references/*.md 解析到 {len(blocks)} 个条目")
        if not blocks:
            problems.append("references/*.md 也没有可解析内容，skill 包不完整")

    for extra in ("index.md", "api-index.md"):
        p = os.path.join(REF_DIR, extra)
        print(f"{extra:10}: {'OK' if os.path.exists(p) else '缺失'}")

    # 凭证
    env_tok = os.environ.get("TIKHUB_API_KEY", "").strip()
    tok = get_token()
    if env_tok:
        print(f"凭证      : 环境变量 TIKHUB_API_KEY（长度 {len(env_tok)}）")
    elif tok:
        print(f"凭证      : {TOKEN_FILE}（{tok[:6]}...{tok[-4:]}）")
    else:
        notes.append("未配置 token：search/show/list 可用，真实调用会 401；"
                     "Demo-API 的 /api/v1/demo/... 免鉴权可先跑通链路")

    # 网络（可选）
    if args.net:
        print("网络      : 检测中…")
        try:
            if IS_PRO:
                status, _, _ = _raw_request(GATEWAY + "/healthz",
                                            {"Accept": "application/json"}, None, 15)
            else:
                status, _, _ = _direct_request("/api/v1/tikhub/user/get_user_info",
                                               None, None, 15)
            print(f"网络      : OK（HTTP {status}）")
            if status in (401, 403):
                notes.append("网络通，但凭证被拒（看上面的 401/403 提示）")
        except NetError as e:
            problems.append(f"网络不可达：{e}")

    print("\n== 结论 ==")
    if problems:
        for p in problems:
            print(f"[FAIL] {p}")
    if notes:
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
            print("未配置账户 token。运行 `python3 scripts/tikhub.py recharge` 充值获取。")
        else:
            print("未配置 token。到 https://user.tikhub.io 生成后执行: "
                  "python3 scripts/tikhub.py token <token>")
        return
    print(f"当前 token: {t[:6]}...{t[-4:]} (长度 {len(t)})")


def cmd_ping(args):
    if not get_token():
        die("未配置 token，先运行: python3 scripts/tikhub.py token <token>"
            if not IS_PRO else "未配置账户 token，先运行: python3 scripts/tikhub.py recharge")
    if IS_PRO:
        status, _, text = _raw_request(GATEWAY + "/healthz", {"Accept": "application/json"})
    else:
        status, _, text = _direct_request("/api/v1/tikhub/user/get_user_info")
    print(f"HTTP {status}")
    print(text[:800])


def _gateway_get(path, timeout=TIMEOUT):
    """付费版只读查询：带账户 token 的 GET。"""
    if not GATEWAY:
        die("付费版未配置网关地址（skill_meta.json 的 gateway_url）")
    token = get_token()
    if not token:
        die("未配置账户 token。先运行 `python3 scripts/tikhub.py recharge` 购买额度包。")
    headers = {"Accept": "application/json",
               "User-Agent": f"tikhub-{PLATFORM}-skill/1.0",
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
           "--session-id", "tikhub-recharge",
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


def cmd_recharge(args):
    if not IS_PRO:
        die("自备 API Key 版无需在此充值，用你自己的 token：python3 scripts/tikhub.py token <token>")
    if not GATEWAY:
        die("付费版未配置网关地址（skill_meta.json 的 gateway_url）")

    pack = args.pack or "starter"
    body = {"pack": pack}
    status, headers, text = _raw_request(
        GATEWAY + "/v1/recharge", {"Accept": "application/json"}, body)

    proof = args.proof

    if status == 402 and not proof:
        needed = None
        for k, v in headers.items():
            if k.lower() == "payment-needed":
                needed = v
                break
        if not needed:
            die("网关返回 402 但没有 Payment-Needed 头")
        try:
            bill = json.loads(_b64url_decode(needed))
        except Exception:
            die("账单解析失败")
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
            die("没能从支付结果里取到 Payment-Proof，可手动用 --proof 传入")

    if status == 402 and proof:
        status, _, text = _raw_request(
            GATEWAY + "/v1/recharge",
            {"Accept": "application/json", "Payment-Proof": proof},
            body)

    try:
        payload = json.loads(text)
    except Exception:
        payload = {}

    if status != 200:
        print(f"HTTP {status}: {HINTS.get(status, '')}")
        print(text[:800])
        sys.exit(2)

    data = payload.get("data") or {}
    token = data.get("token")
    if not token:
        die(f"网关没有返回 token：{text[:300]}")
    p = save_token(token)
    print(f"充值成功：{data.get('credits')} 次额度，token 已保存到 {p}")
    print(f"订单 {payload.get('out_trade_no')}  trade_no {payload.get('trade_no')}")


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
        description=f"TikHub {PLATFORM_ZH}接口 CLI（{EDITION} v{VERSION}）",
        epilog="首次使用先跑 doctor 自检；call 前可用 show 看参数、--dry-run 预览请求。")
    ap.add_argument("--version", action="version",
                    version=f"tikhub-{PLATFORM or 'skill'} {VERSION} ({EDITION})")
    sub = ap.add_subparsers(dest="cmd")

    s = sub.add_parser("doctor", help="自检：环境/清单/文档/凭证（推荐第一步）")
    s.add_argument("--net", action="store_true", help="额外检测网络连通性")
    s.set_defaults(func=cmd_doctor)

    s = sub.add_parser("search", help="搜索接口")
    s.add_argument("keyword", nargs="+")
    s.add_argument("--limit", type=int, default=25)
    s.set_defaults(func=cmd_search)

    s = sub.add_parser("show", help="查看接口详情")
    s.add_argument("key")
    s.set_defaults(func=cmd_show)

    s = sub.add_parser("list", help="按分类列出")
    s.add_argument("--folder")
    s.set_defaults(func=cmd_list)

    s = sub.add_parser("call", help="调用接口")
    s.add_argument("path")
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
    s.set_defaults(func=cmd_call)

    s = sub.add_parser("token", help="查看/保存 token")
    s.add_argument("token_value", nargs="?")
    s.set_defaults(func=cmd_token)

    s = sub.add_parser("ping", help="验证 token")
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
        s.set_defaults(func=cmd_recharge)

    args = ap.parse_args()
    if not getattr(args, "func", None):
        ap.print_help()
        sys.exit(0)
    args.func(args)


if __name__ == "__main__":
    main()
