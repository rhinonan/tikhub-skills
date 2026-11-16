#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""TikHub 数据接口 CLI（平台无关、版本无关）。

同一个文件由 build.py 分发到 8 个 skill 里，运行时的平台与版本从
脚本同级目录的 skill_meta.json 读取：

    {"platform": "douyin", "platform_zh": "抖音",
     "edition": "free",  "base_url": "https://api.tikhub.io",
     "gateway_url": ""}

免费版（edition=free）：用户自己的 TikHub Token，直连 api.tikhub.io
付费版（edition=pro） ：经作者网关转发，按次 402 付费

用法:
  python tikhub.py search "关键词"             # 搜接口
  python tikhub.py show <关键词或path>          # 看接口参数
  python tikhub.py list [--folder X]           # 按分类列
  python tikhub.py call <path> [--query k=v ...] [--body '{...}']
  python tikhub.py token [<token>]             # 查看/保存凭证
  python tikhub.py ping                        # 验证凭证
  python tikhub.py recharge [--pack starter] [--proof X]   # 仅付费版：充值
"""
import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
META_PATH = os.path.join(SKILL_DIR, "skill_meta.json")
INV = os.path.join(SKILL_DIR, "references", "inventory.json")
HOME = os.path.join(os.path.expanduser("~"), ".workbuddy")
HOME_TOKEN = os.path.join(HOME, "tikhub_token")
HOME_GW_TOKEN = os.path.join(HOME, "tikhub_gateway_token")
TIMEOUT = 90


def die(msg, code=1):
    print(f"[ERROR] {msg}", file=sys.stderr)
    sys.exit(code)


def load_meta():
    if not os.path.exists(META_PATH):
        die(f"找不到 {META_PATH}（skill 包不完整，用 build.py 重新生成）")
    return json.load(open(META_PATH, encoding="utf-8"))


META = load_meta()
PLATFORM = META.get("platform", "")
PLATFORM_ZH = META.get("platform_zh", PLATFORM)
EDITION = META.get("edition", "free")
BASE = (META.get("base_url") or "https://api.tikhub.io").rstrip("/")
GATEWAY = (META.get("gateway_url") or "").rstrip("/")
IS_PRO = EDITION == "pro"
TOKEN_FILE = HOME_GW_TOKEN if IS_PRO else HOME_TOKEN


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
    try:
        os.chmod(TOKEN_FILE, 0o600)
    except Exception:
        pass
    return TOKEN_FILE


# ---------------------------------------------------------------- 接口清单

def load_inventory():
    if not os.path.exists(INV):
        die(f"找不到接口清单 {INV}")
    return json.load(open(INV, encoding="utf-8"))


def _norm(key):
    """兼容 Git Bash 把 /api/... 转成 Windows 路径的情况。"""
    k = key.replace("\\", "/")
    i = k.lower().find("/api/")
    return (k[i:] if i >= 0 else k).rstrip("/")


def _find(rows, key):
    k = _norm(key).lower()
    for r in rows:
        if r["path"].lower() == k:
            return [r]
    cand = [r for r in rows if k in r["path"].lower()]
    if not cand:
        cand = [r for r in rows if k in (r.get("name_zh") or "").lower()
                or k in (r.get("name") or "").lower()]
    return cand


# ---------------------------------------------------------------- 本地命令

def cmd_search(args):
    rows = load_inventory()
    kw = [k.lower() for k in args.keyword]
    hits = []
    for r in rows:
        hay = " ".join([r.get("name", ""), r.get("name_zh", ""), r.get("name_en", ""),
                        r.get("path", ""), r.get("purpose", ""), r.get("folder", "")]).lower()
        if all(k in hay for k in kw):
            hits.append(r)
    if not hits:
        print(f"没匹配到接口（关键词: {' '.join(args.keyword)}）")
        return
    limit = args.limit or 25
    print(f"命中 {len(hits)} 个接口" + (f"，显示前 {limit} 个：" if len(hits) > limit else "："))
    for r in hits[:limit]:
        print(f"- [{r['folder']}] {r['name_zh'] or r['name']}")
        print(f"  {r['method']} {r['path']}")
        if r.get("purpose") and r["purpose"] != (r["name_zh"] or r["name"]):
            print(f"  用途: {r['purpose'][:100]}")
    if len(hits) > limit:
        print(f"... 还有 {len(hits)-limit} 个，用 --limit 扩大或加关键词")


def _print_params(title, params):
    print(f"\n{title}:")
    for p in params:
        req = "必填" if p.get("required") else "可选"
        print(f"  {p['name']} ({req}, {p.get('type','')}"
              + (f", 默认 {p['default']}" if p.get("default") not in ("", None) else "")
              + f")  {p.get('desc','')}")


def cmd_show(args):
    rows = load_inventory()
    hits = _find(rows, args.key)
    if not hits:
        die(f"没找到接口: {args.key}（可先 search）")
    if len(hits) > 1:
        print(f"匹配 {len(hits)} 个，列出前 15 个，请用完整 path 再查：")
        for r in hits[:15]:
            print(f"  {r['method']} {r['path']}   # {r['name_zh'] or r['name']}")
        return
    r = hits[0]
    print(f"# {r['name_zh'] or r['name']}")
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
    print(f"\n文档: {r['doc']}")


def cmd_list(args):
    rows = load_inventory()
    if args.folder:
        rows = [r for r in rows if r["folder"].lower() == args.folder.lower()]
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
        die(f"请求失败: {e}")


HINTS_FREE = {
    401: "token 无效/缺失：运行 `python tikhub.py token <你的token>` 保存；token 在 https://user.tikhub.io 生成",
    402: "余额不足：该接口需付费（部分不吃免费额度），先查账户余额或用免费 Demo 接口",
    403: "无权限：账号被停用 / 邮箱未验证 / token 权限不足",
    404: "接口路径不存在：检查 path（用 show 确认）",
    429: "限流：降低并发或稍后重试",
    500: "服务端错误：重试一次，持续失败换同类接口（如 Web → App V3）",
}

HINTS_PRO = {
    401: "账户 token 无效：运行 `python tikhub.py recharge` 充值获取",
    402: "需要付款：完成支付宝付款后重试；已付款可用 --proof 手动重试",
    403: "无权限：账户被停用或接口未开放",
    404: "接口路径不存在：检查 path（用 show 确认）",
    429: "限流：降低并发或稍后重试",
    500: "服务端/网关错误：重试一次，持续失败换同类接口",
    502: "上游失败：本次未扣额度，可直接重试",
}

HINTS = HINTS_PRO if IS_PRO else HINTS_FREE


def _direct_request(path, query=None, body=None, timeout=TIMEOUT):
    """免费版：直连 TikHub。"""
    url = BASE + path
    if query:
        url += "?" + urllib.parse.urlencode({k: v for k, v in query.items() if v != ""})
    headers = {"Accept": "application/json",
               "User-Agent": f"tikhub-{PLATFORM}-skill/1.0"}
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
               "User-Agent": f"tikhub-{PLATFORM}-skill/1.0"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if proof:
        headers["Payment-Proof"] = proof
    method = "POST" if body is not None else "GET"
    payload = {"platform": PLATFORM, "path": path, "method": method,
               "query": query or {}, "body": body}
    return _raw_request(GATEWAY + "/v1/call", headers, payload, timeout)


def _request(path, query=None, body=None, timeout=TIMEOUT, proof=""):
    return _gateway_request(path, query, body, timeout, proof) if IS_PRO \
        else _direct_request(path, query, body, timeout)


# ---------------------------------------------------------------- call

def cmd_call(args):
    path = args.path
    if not path.startswith("/"):
        hits = _find(load_inventory(), path)
        if len(hits) != 1:
            for r in hits[:10]:
                print(f"  {r['method']} {r['path']}   # {r['name_zh'] or r['name']}")
            die(f"路径需唯一，命中 {len(hits)} 个；请传完整 /api/v1/{PLATFORM}/... 路径")
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

    proof = getattr(args, "proof", "") or ""
    status, headers, text = _request(path, query, body,
                                     timeout=args.timeout, proof=proof)

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
    s = inner if isinstance(inner, str) else json.dumps(inner, ensure_ascii=False, indent=1)
    if args.out:
        # 与旧版保持一致：data 为空时落盘原始响应，而不是 "null"
        content = inner if isinstance(inner, str) else (
            json.dumps(inner, ensure_ascii=False, indent=1) if inner is not None else text)
        open(args.out, "w", encoding="utf-8").write(content)
        print(f"已保存 data 到 {args.out}")
    else:
        print(s[:args.preview] + ("\n...(截断，用 --out 存全量或 --preview N)"
                                  if len(s) > args.preview else ""))


# ---------------------------------------------------------------- token / ping

def cmd_token(args):
    if args.token_value:
        p = save_token(args.token_value.strip())
        print(f"已保存 token 到 {p}")
        return
    t = get_token()
    if not t:
        if IS_PRO:
            print("未配置账户 token。运行 `python tikhub.py recharge` 充值获取。")
        else:
            print("未配置 token。到 https://user.tikhub.io 生成后执行: "
                  "python tikhub.py token <token>")
        return
    print(f"当前 token: {t[:6]}...{t[-4:]} (长度 {len(t)})")


def cmd_ping(args):
    if not get_token():
        die("未配置 token，先运行: python tikhub.py token <token>"
            if not IS_PRO else "未配置账户 token，先运行: python tikhub.py recharge")
    if IS_PRO:
        status, _, text = _raw_request(GATEWAY + "/healthz", {"Accept": "application/json"})
    else:
        status, _, text = _direct_request("/api/v1/tikhub/user/get_user_info")
    print(f"HTTP {status}")
    print(text[:800])


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
        die("免费版不需要充值，用你自己的 token：python tikhub.py token <token>")
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
    ap = argparse.ArgumentParser(description=f"TikHub {PLATFORM_ZH}接口 CLI（{EDITION}）")
    sub = ap.add_subparsers(dest="cmd", required=True)

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
    s.add_argument("--out", "-o", help="把 data 存到文件")
    s.add_argument("--preview", type=int, default=1500)
    s.add_argument("--raw", action="store_true", help="输出完整响应")
    s.add_argument("--timeout", type=int, default=TIMEOUT)
    s.add_argument("--proof", help="手动传入 Payment-Proof，跳过付款步骤（联调用）")
    s.set_defaults(func=cmd_call)

    s = sub.add_parser("token", help="查看/保存 token")
    s.add_argument("token_value", nargs="?")
    s.set_defaults(func=cmd_token)

    s = sub.add_parser("ping", help="验证 token")
    s.set_defaults(func=cmd_ping)

    if IS_PRO:
        s = sub.add_parser("recharge", help="充值额度（需要买家侧支付依赖）")
        s.add_argument("--pack", default="starter")
        s.add_argument("--proof", help="手动传入 Payment-Proof，跳过 payment 步骤（联调用）")
        s.set_defaults(func=cmd_recharge)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
