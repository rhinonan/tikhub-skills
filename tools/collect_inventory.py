#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从官方 OpenAPI 规范生成各平台的 inventory.json 与分类文档。

数据源：https://api.tikhub.io/openapi.json（OpenAPI 3.1，需浏览器 UA），
也可以用 --spec 指定本地文件（例如官方 Python SDK 仓库里的 spec/openapi.json）。

用法：
    python tools/collect_inventory.py                     # 下载 live spec，生成全部平台
    python tools/collect_inventory.py --platforms weibo,zhihu
    python tools/collect_inventory.py --spec /path/openapi.json
    python tools/collect_inventory.py --refresh-meta      # 覆盖已存在的 meta.json
    python tools/collect_inventory.py --pricing-csv none  # 不从价格清单取价

价格来源优先级：pricing/tikhub_pricing_*.csv（官方清单，权威） > 接口描述里的文字价格。

产物（每个平台目录）：
    src/platforms/<slug>/meta.json                  # 缺省时创建骨架，已存在则保留
    src/platforms/<slug>/references/inventory.json
    src/platforms/<slug>/references/<folder>.md
    src/platforms/<slug>/references/index.md
    src/platforms/<slug>/references/_meta.json
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import glob
import json
import os
import re
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLATFORMS_DIR = os.path.join(ROOT, "src", "platforms")
CACHE_DIR = os.path.join(ROOT, ".local")
GATEWAY_COST_MAP = os.path.join(ROOT, "gateway", "endpoint_costs.json")
PRICING_DIR = os.path.join(ROOT, "pricing")


def default_pricing_csv() -> str:
    """取 pricing/ 下最新的官方价格清单。"""
    files = sorted(glob.glob(os.path.join(PRICING_DIR, "tikhub_pricing_*.csv")))
    return files[-1] if files else ""
SPEC_URL = "https://api.tikhub.io/openapi.json"
SPEC_UA = "Mozilla/5.0 (compatible; cn-social-data-collector/2.0)"

CJK = re.compile(r"[一-鿿]")
PRICE_RE = re.compile(r"\$\s*(\d+(?:\.\d+)?)|(\d+(?:\.\d+)?)\s*\$")

# 平台 slug → 文档库/接口前缀。common 只收与本产品相关演示接口与混合解析。
PLATFORMS = {
    "douyin": {
        "zh": "抖音", "en": "Douyin", "prefixes": ["douyin"],
    },
    "weibo": {
        "zh": "微博", "en": "Weibo", "prefixes": ["weibo"],
    },
    "xiaohongshu": {
        "zh": "小红书", "en": "Xiaohongshu", "prefixes": ["xiaohongshu"],
    },
    "bilibili": {
        "zh": "Bilibili", "en": "Bilibili", "prefixes": ["bilibili"],
    },
    "zhihu": {
        "zh": "知乎", "en": "Zhihu", "prefixes": ["zhihu"],
    },
    "kuaishou": {
        "zh": "快手", "en": "Kuaishou", "prefixes": ["kuaishou"],
    },
    "wechat": {
        "zh": "微信", "en": "WeChat",
        "prefixes": ["wechat_channels", "wechat_mp", "wechat_search"],
    },
    "common": {
        "zh": "通用", "en": "Common", "prefixes": ["demo", "hybrid"],
    },
}

# demo 接口按“第二段”归属；tiktok / instagram 演示接口不属于本产品。
DEMO_ALLOWED = {"demo", "douyin", "douyin_search", "kuaishou", "wechat"}

ORDER = list(PLATFORMS)


# ---------------------------------------------------------------- 工具函数

def die(msg: str) -> None:
    raise SystemExit(f"[collect] {msg}")


def snake(title: str) -> str:
    s = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", title or "body")
    s = re.sub(r"[^0-9A-Za-z_]+", "_", s).strip("_").lower()
    return s or "body"


def one_line(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip())


def split_name(name: str) -> tuple[str, str]:
    """在「左边有中文、右边没有中文」的第一个斜杠处切中英文名。"""
    for m in re.finditer(r"/(?=\s*[A-Za-z\[])", name or ""):
        left, right = name[:m.start()], name[m.start() + 1:]
        if CJK.search(left) and not CJK.search(right):
            return left.strip(), right.strip()
    return (name or "").strip(), ""


def load_pricing_csv(path: str) -> dict:
    """读官方价格清单：Endpoint,Platform,Cost (USD/request),...

    价格 CSV 是权威来源；描述里的价格只作兜底（两者冲突时以 CSV 为准）。
    """
    if not path or not os.path.exists(path):
        return {}
    out = {}
    with open(path, encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            ep = (row.get("Endpoint") or "").strip().strip('"').strip()
            if not ep.startswith("/api/"):
                continue
            try:
                out[ep] = float(row.get("Cost (USD/request)", ""))
            except (TypeError, ValueError):
                continue
    return out


def extract_unit_cost(text: str) -> float | None:
    """从描述里抽上游单次价格（美元）。

    兼容这些写法：
        价格：0.02$ / 次
        价格为：0.005$一次
        固定价格为0.001$ * 50 = 0.05$一次   → 取等号后的总价 0.05
        优惠活动价为$0.25，活动结束后恢复原价$0.5 → 取当前价 0.25（第一个）
    """
    vals = []
    for m in PRICE_RE.finditer(text or ""):
        raw = m.group(1) or m.group(2)
        try:
            vals.append(float(raw))
        except ValueError:
            continue
    if not vals:
        return None
    if "=" in (text or "") and "*" in (text or ""):
        return vals[-1]
    return vals[0]


def parse_description(desc: str) -> dict:
    """解析描述里的中英双语 markdown 段落。"""
    out = {
        "purpose": "", "returns": "", "notice": "",
        "purpose_en": "", "returns_en": "", "notice_en": "",
        "example": "",
    }
    if not desc:
        return out

    def blocks(text: str) -> dict:
        found = {}
        for m in re.finditer(
            r"###\s*(用途|参数|返回|注意|Purpose|Parameters|Return|Note):\s*\n((?:-.*(?:\n|$))*)",
            text,
        ):
            key = m.group(1)
            items = [one_line(x[1:]) for x in m.group(2).splitlines() if x.startswith("-")]
            found[key] = [x for x in items if x]
        return found

    zh_part, en_part = desc, ""
    if "# [English]" in desc:
        zh_part, en_part = desc.split("# [English]", 1)
    if "# [示例" in en_part:
        en_part, example = en_part.split("# [示例", 1)
        out["example"] = example.split("]", 1)[-1].strip()
    if "# [示例" in zh_part:
        zh_part, example = zh_part.split("# [示例", 1)
        if not out["example"]:
            out["example"] = example.split("]", 1)[-1].strip()

    zh, en = blocks(zh_part), blocks(en_part)
    clean = lambda xs: [x.strip().rstrip("。；;") for x in (xs or []) if x.strip()]
    clean_en = lambda xs: [x.strip().rstrip(".;;") for x in (xs or []) if x.strip()]
    join = lambda xs: "；".join(clean(xs))
    join_en = lambda xs: "; ".join(clean_en(xs))
    out["purpose"] = join(zh.get("用途"))
    out["returns"] = join(zh.get("返回"))
    out["notice"] = join(zh.get("注意"))
    out["purpose_en"] = join_en(en.get("Purpose"))
    out["returns_en"] = join_en(en.get("Return"))
    out["notice_en"] = join_en(en.get("Note"))
    if not out["purpose"]:
        out["purpose"] = out["purpose_en"]
    if not out["returns"]:
        out["returns"] = out["returns_en"]
    if not out["notice"]:
        out["notice"] = out["notice_en"]
    return out


def deref(schema: dict, spec: dict, depth: int = 0) -> dict:
    if not isinstance(schema, dict) or depth > 4:
        return schema if isinstance(schema, dict) else {}
    ref = schema.get("$ref")
    if ref and ref.startswith("#/components/schemas/"):
        name = ref.rsplit("/", 1)[-1]
        return deref(spec.get("components", {}).get("schemas", {}).get(name, {}), spec, depth + 1)
    return schema


def param_meta(p: dict, spec: dict, where: str) -> dict:
    schema = deref(p.get("schema") or {}, spec)
    return {
        "name": p.get("name", ""),
        "in": where,
        "required": bool(p.get("required", False)),
        "type": schema.get("type", ""),
        "default": schema.get("default", ""),
        "example": p.get("example", schema.get("example", "")),
        "desc": one_line(p.get("description") or schema.get("description") or ""),
    }


def body_meta(op: dict, spec: dict) -> tuple[list, dict | None]:
    rb = op.get("requestBody") or {}
    schema = deref(((rb.get("content") or {}).get("application/json") or {}).get("schema") or {}, spec)
    if not schema:
        return [], None
    if schema.get("type") == "object" or "properties" in schema:
        required = set(schema.get("required") or [])
        params = []
        for name, prop in (schema.get("properties") or {}).items():
            prop = deref(prop, spec)
            params.append({
                "name": name,
                "required": name in required,
                "type": prop.get("type", ""),
                "default": prop.get("default", ""),
                "example": prop.get("example", ""),
                "desc": one_line(prop.get("description") or ""),
            })
        return params, None
    if schema.get("type") == "array":
        title = schema.get("title") or "body"
        return [{
            "name": snake(title),
            "required": bool(rb.get("required", False)),
            "type": "array",
            "default": "",
            "example": "",
            "desc": one_line(schema.get("description") or title),
        }], schema
    return [], None


def tag_title(tag: str) -> str:
    return tag.replace("-", " ").strip()


def tag_desc(spec: dict, tag: str) -> str:
    for t in spec.get("tags", []):
        if t.get("name") == tag:
            m = re.search(r"\*\*\((.*?)\)\*\*", t.get("description") or "")
            text = m.group(1) if m else (t.get("description") or "")
            text = text.split("/")[0].strip()
            return one_line(text)
    return ""


# ---------------------------------------------------------------- spec 获取

def load_spec(arg: str | None) -> dict:
    if arg and not re.match(r"^https?://", arg):
        with open(arg, encoding="utf-8") as f:
            return json.load(f)

    url = arg or SPEC_URL
    os.makedirs(CACHE_DIR, exist_ok=True)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": SPEC_UA})
        with urllib.request.urlopen(req, timeout=60) as resp:
            text = resp.read().decode("utf-8")
        spec = json.loads(text)
        version = spec.get("info", {}).get("version", "unknown")
        cache = os.path.join(CACHE_DIR, f"openapi-{version}.json")
        with open(cache, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        print(f"[collect] spec {version} 已缓存到 {os.path.relpath(cache, ROOT)}")
        return spec
    except Exception as exc:  # noqa: BLE001
        cached = sorted(
            (os.path.join(CACHE_DIR, f) for f in os.listdir(CACHE_DIR)
             if f.startswith("openapi-") and f.endswith(".json")),
            key=os.path.getmtime,
            reverse=True,
        ) if os.path.isdir(CACHE_DIR) else []
        if cached:
            print(f"[collect] 下载失败（{exc}），回退到缓存 {os.path.relpath(cached[0], ROOT)}")
            with open(cached[0], encoding="utf-8") as f:
                return json.load(f)
        die(f"下载 spec 失败且无本地缓存：{exc}")


# ---------------------------------------------------------------- 主流程

def platform_of(path: str) -> str | None:
    if not path.startswith("/api/v1/"):
        return None
    seg = path.split("/")[3]
    if seg == "demo":
        sub = path.split("/")[4] if path.count("/") > 4 else ""
        return "common" if sub in DEMO_ALLOWED else None
    if seg == "hybrid":
        return "common"
    for slug, cfg in PLATFORMS.items():
        if seg in cfg["prefixes"] and slug != "common":
            return slug
    return None


def build_rows(spec: dict, slugs: list[str], prices: dict | None = None) -> dict[str, list[dict]]:
    prices = prices or {}
    rows: dict[str, list[dict]] = {s: [] for s in slugs}
    seen: set[str] = set()
    skipped_tiktok = 0
    for path, methods in spec.get("paths", {}).items():
        if "/tiktok/" in path:
            skipped_tiktok += len(methods)
            continue
        slug = platform_of(path)
        if slug not in rows:
            continue
        for method, op in methods.items():
            if method.lower() not in ("get", "post", "put", "delete", "patch"):
                continue
            if path in seen:
                die(f"重复 path：{path}")
            seen.add(path)
            tag = (op.get("tags") or ["Other"])[0]
            name = one_line(op.get("summary") or path)
            zh, en = split_name(name)
            parsed = parse_description(op.get("description") or "")
            query = [param_meta(p, spec, "query") for p in op.get("parameters") or []
                     if p.get("in") in ("query", "path")]
            body, body_schema = body_meta(op, spec)
            cfg = PLATFORMS[slug]
            row = {
                "platform": slug,
                "platform_zh": cfg["zh"],
                "folder": tag,
                "name": name,
                "name_zh": zh,
                "name_en": en,
                "method": method.upper(),
                "path": path,
                "purpose": parsed["purpose"],
                "returns": parsed["returns"],
                "notice": parsed["notice"],
                "query_params": query,
                "body_params": body,
                "request_example": parsed["example"],
                "doc": "",
                "deprecated": bool(op.get("deprecated", False)),
            }
            if body_schema:
                row["body_schema"] = body_schema
            if path in prices:
                row["unit_cost_usd"] = prices[path]
                row["cost_source"] = "csv"
            else:
                cost = extract_unit_cost(op.get("description") or "")
                if cost is not None:
                    row["unit_cost_usd"] = cost
                    row["cost_source"] = "description"
            rows[slug].append(row)
    print(f"[collect] 排除 TikTok 接口 {skipped_tiktok} 条")
    return rows


def render_folder_md(folder: str, rows: list[dict], spec: dict) -> str:
    plot = tag_desc(spec, folder)
    head = [f"# {tag_title(folder)}", ""]
    head.append(f"文件夹 `{folder}` · {len(rows)} 个接口")
    if plot:
        head.append(f"说明：{plot}")
    head.append("")
    out = ["\n".join(head)]
    for r in rows:
        block = [f"## {r['name_zh'] or r['name']}", "", f"`{r['method']} {r['path']}`", ""]
        if r.get("deprecated"):
            block.append("- **已标记 deprecated，可能失效**")
        if r.get("purpose"):
            block.append(f"- 用途：{r['purpose']}")
        if r.get("returns"):
            block.append(f"- 返回：{r['returns']}")
        if r.get("notice"):
            block.append(f"- 注意：{r['notice']}")
        if r.get("query_params"):
            block.append("- Query：")
            for p in r["query_params"]:
                flag = "必填" if p.get("required") else "选填"
                typ = f",{p['type']}" if p.get("type") else ""
                block.append(f"  - `{p['name']}` ({flag}{typ}) {p.get('desc','')}".rstrip())
        if r.get("body_params"):
            block.append("- Body(JSON)：")
            for p in r["body_params"]:
                flag = "必填" if p.get("required") else "选填"
                typ = f",{p['type']}" if p.get("type") else ""
                block.append(f"  - `{p['name']}` ({flag}{typ}) {p.get('desc','')}".rstrip())
        if r.get("request_example"):
            block += ["- 示例：", "", "```", r["request_example"], "```"]
        out.append("\n".join(block))
    return "\n\n".join(out) + "\n"


def render_index(slug: str, rows: list[dict], spec: dict) -> str:
    cfg = PLATFORMS[slug]
    folders: dict[str, list[dict]] = {}
    for r in rows:
        folders.setdefault(r["folder"], []).append(r)
    out = [
        f"# {cfg['zh']}接口分类索引",
        "",
        f"共 {len(rows)} 个接口，分 {len(folders)} 类。",
        "",
        "| 分类 | 接口数 | 参考文件 | 说明 |",
        "|---|---|---|---|",
    ]
    for folder, items in folders.items():
        out.append(f"| {folder} | {len(items)} | `references/{folder}.md` | {tag_desc(spec, folder)} |")
    out += [
        "",
        "机器可读清单见 `references/inventory.json`；分类文档按需打开，不要一次全部载入上下文。",
    ]
    return "\n".join(out) + "\n"


def write_platform(slug: str, rows: list[dict], spec: dict, refresh_meta: bool) -> None:
    cfg = PLATFORMS[slug]
    pdir = os.path.join(PLATFORMS_DIR, slug)
    ref = os.path.join(pdir, "references")
    os.makedirs(ref, exist_ok=True)

    folders: dict[str, list[dict]] = {}
    for r in rows:
        folders.setdefault(r["folder"], []).append(r)

    for folder, items in folders.items():
        with open(os.path.join(ref, f"{folder}.md"), "w", encoding="utf-8", newline="\n") as f:
            f.write(render_folder_md(folder, items, spec))
    with open(os.path.join(ref, "index.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write(render_index(slug, rows, spec))
    with open(os.path.join(ref, "inventory.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(rows, f, ensure_ascii=False, indent=1)
        f.write("\n")

    version = spec.get("info", {}).get("version", "unknown")
    meta_path = os.path.join(ref, "_meta.json")
    with open(meta_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump({
            "spec_version": version,
            "generated_at": dt.date.today().isoformat(),
            "platform": slug,
            "count": len(rows),
            "folders": {k: len(v) for k, v in folders.items()},
        }, f, ensure_ascii=False, indent=1)
        f.write("\n")

    meta = os.path.join(pdir, "meta.json")
    if refresh_meta or not os.path.exists(meta):
        prefixes = [f"/api/v1/{p}" for p in cfg["prefixes"]]
        if slug == "common":
            prefixes = ["/api/v1/demo", "/api/v1/hybrid"]
        payload = {
            "platform": slug,
            "platform_zh": cfg["zh"],
            "platform_en": cfg["en"],
            "api_prefixes": prefixes,
            "version": version,
            "scope": "",
            "usage_zh": [],
            "usage_en": [],
        }
        with open(meta, "w", encoding="utf-8", newline="\n") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
            f.write("\n")

    missing_required = sum(1 for r in rows if not r["query_params"] and not r["body_params"])
    missing_example = sum(1 for r in rows if not r["request_example"])
    print(f"[collect] {slug:12s} {len(rows):4d} 接口 / {len(folders):2d} 分类 "
          f"（无参数 {missing_required}，无示例 {missing_example}）")


def write_gateway_cost_map(spec: dict) -> None:
    """把各平台清单里抽出的上游单价汇总给网关（只含写明了价格的接口）。"""
    costs = {}
    for slug in ORDER:
        inv = os.path.join(PLATFORMS_DIR, slug, "references", "inventory.json")
        if not os.path.exists(inv):
            continue
        with open(inv, encoding="utf-8") as f:
            for r in json.load(f):
                cost = r.get("unit_cost_usd")
                if cost is not None:
                    costs[r["path"]] = cost
    payload = {
        "_note": "上游单次价格（USD），来自 pricing/tikhub_pricing_*.csv（权威）；"
                 "接口描述里的价格只作兜底。gateway/pricing.py 读它做逐接口定价，"
                 "未列出的接口按路径正则兜底。",
        "spec_version": spec.get("info", {}).get("version", "unknown"),
        "updated": dt.date.today().isoformat(),
        "costs": dict(sorted(costs.items())),
    }
    os.makedirs(os.path.dirname(GATEWAY_COST_MAP), exist_ok=True)
    with open(GATEWAY_COST_MAP, "w", encoding="utf-8", newline="\n") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(f"[collect] 网关定价表 {os.path.relpath(GATEWAY_COST_MAP, ROOT)}：{len(costs)} 条")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", help="OpenAPI 地址或本地文件")
    ap.add_argument("--platforms", default="all",
                    help="逗号分隔的 slug，或 all（默认）")
    ap.add_argument("--refresh-meta", action="store_true",
                    help="覆盖已存在的 meta.json（会清空手写的 scope/示例）")
    ap.add_argument("--pricing-csv", default=default_pricing_csv(),
                    help="官方价格清单 CSV；传 none 关闭")
    args = ap.parse_args()

    chosen = ORDER if args.platforms == "all" else [
        s.strip() for s in args.platforms.split(",") if s.strip()
    ]
    bad = [s for s in chosen if s not in PLATFORMS]
    if bad:
        die(f"未知平台：{bad}；可选 {ORDER}")

    spec = load_spec(args.spec)
    print(f"[collect] spec {spec.get('info', {}).get('version', '?')} · "
          f"{len(spec.get('paths', {}))} paths")

    prices = {} if args.pricing_csv.lower() == "none" else load_pricing_csv(args.pricing_csv)
    if prices:
        print(f"[collect] 价格清单 {os.path.relpath(args.pricing_csv, ROOT)}："
              f"{len(prices)} 条")
    else:
        print("[collect] 未加载价格清单，价格只从接口描述里抽（覆盖率会低）")

    rows = build_rows(spec, chosen, prices)
    for slug in chosen:
        if not rows[slug]:
            die(f"{slug} 没有采集到任何接口")
        write_platform(slug, rows[slug], spec, args.refresh_meta)
        priced = sum(1 for r in rows[slug] if r.get("unit_cost_usd") is not None)
        print(f"[collect]   {slug:12s} 价格覆盖 {priced}/{len(rows[slug])}")

    # 跨平台重名 folder 检查（合并成一个 references/ 目录后不能撞名）
    folder_owner: dict[str, str] = {}
    for slug in chosen:
        for r in rows[slug]:
            if r["folder"] in folder_owner and folder_owner[r["folder"]] != slug:
                print(f"[collect] WARN folder 重名：{r['folder']} "
                      f"({folder_owner[r['folder']]} / {slug})")
            folder_owner.setdefault(r["folder"], slug)

    write_gateway_cost_map(spec)


if __name__ == "__main__":
    main()
