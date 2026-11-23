#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 src/ 组装出中文社媒数据引擎的两个 skill 目录到 skills/。

单一数据源：
    src/product.json              产品与平台清单（唯一事实源）
    src/core/social.py            唯一的 CLI 实现
    src/core/SKILL.*.template.md  SKILL.md 模板（按版本）
    src/platforms/<平台>/          inventory.json + references + 平台正文
    src/editions/<版本>.json       版本配置

产物：
    skills/cn-social-data/       免费版（自备上游 Key）
    skills/cn-social-data-pro/   付费版（按次付费）

用法：
    python build.py            # 构建两个版本
    python build.py --check    # 只校验，不写文件
    python build.py --zip      # 构建并生成 dist/<skill>.zip
    python build.py --clean    # 构建后删除本次未产出的旧 skill 目录
    GATEWAY_URL=https://x python build.py   # 覆盖付费版网关地址
"""
import argparse
import json
import os
import re
import shutil
import sys
import zipfile

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
OUT = os.path.join(ROOT, "skills")
DIST = os.path.join(ROOT, "dist")
PRODUCT_PATH = os.path.join(SRC, "product.json")
PLATFORMS_DIR = os.path.join(SRC, "platforms")
EDITIONS_DIR = os.path.join(SRC, "editions")
CORE = os.path.join(SRC, "core")

# 每个 skill 必须有这些文件，少一个就算构建不合格
REQUIRED = ["SKILL.md", "skill_meta.json", "_skillhub_meta.json",
            "scripts/social.py", "references/inventory.json", "references/index.md"]

# 分类接口平铺表：SKILL.md 里不允许出现（完整分类请在 references/index.md）
FULL_TABLE = re.compile(r"^\|\s*[^|]+\s*\|\s*\d+\s*\|\s*`references/", re.M)


def die(msg):
    print(f"[build] ERROR {msg}", file=sys.stderr)
    sys.exit(1)


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def load_product():
    if not os.path.exists(PRODUCT_PATH):
        die(f"找不到 {PRODUCT_PATH}")
    product = load_json(PRODUCT_PATH)
    for key in ("slug", "name_zh", "version", "platforms"):
        if not product.get(key):
            die(f"{PRODUCT_PATH} 缺字段 {key}")
    return product


def load_platforms(product):
    """按 product.json 的顺序加载平台，缺文件直接报错。"""
    out = []
    for slug in product["platforms"]:
        pdir = os.path.join(PLATFORMS_DIR, slug)
        meta_path = os.path.join(pdir, "meta.json")
        inv_path = os.path.join(pdir, "references", "inventory.json")
        if not os.path.exists(meta_path):
            die(f"平台 {slug} 缺 meta.json")
        if not os.path.exists(inv_path):
            die(f"平台 {slug} 缺 references/inventory.json")
        meta = load_json(meta_path)
        if meta.get("platform") != slug:
            die(f"{meta_path} 的 platform={meta.get('platform')!r} 与目录名 {slug} 不一致")
        out.append((meta, pdir))
    if not out:
        die("product.json 里没有可构建的平台")
    return out


def load_editions():
    out = {}
    for fn in sorted(os.listdir(EDITIONS_DIR)):
        if fn.endswith(".json"):
            ed = load_json(os.path.join(EDITIONS_DIR, fn))
            if ed.get("edition") == "pro":
                ed["gateway_url"] = os.environ.get("GATEWAY_URL", ed.get("gateway_url", ""))
            out[ed["edition"]] = ed
    return out


def short_use(meta, n=3):
    parts = [p for p in (meta.get("scope") or "").split("、") if p]
    if not parts:
        return ""
    text = "、".join(parts[:n])
    return text + ("…" if len(parts) > n else "")


def platform_table(loaded):
    lines = ["| 平台 | 接口数 | 典型用途 |", "|---|---|---|"]
    for meta, pdir in loaded:
        rows = load_json(os.path.join(pdir, "references", "inventory.json"))
        lines.append(f"| {meta['platform_zh']} | {len(rows)} | {short_use(meta)} |")
    return "\n".join(lines)


def platform_bodies(loaded):
    out = []
    for meta, pdir in loaded:
        body_path = os.path.join(pdir, "skill.body.md")
        if not os.path.exists(body_path):
            die(f"平台 {meta['platform']} 缺 skill.body.md")
        body = open(body_path, encoding="utf-8").read().strip()
        out.append(f"## {meta['platform_zh']}\n\n{body}")
    return "\n\n".join(out)


def description(product, loaded, edition, count):
    name = product["name_zh"]
    names = "、".join(m["platform_zh"] for m, _ in loaded if m["platform"] != "common")
    uses = "下载无水印视频、解析分享链接、批量导出评论、查账号与作品数据、追热搜热榜、找达人"
    if edition == "pro":
        head = (f"{name}（{product.get('name_en', '')}）：{uses}。"
                f"付费版：标准 ¥0.10/次；高价值/批量走额度包（6/30 点每次，"
                f"¥9.90/200 点），无需注册上游。收录 {count} 个接口，覆盖{names}。")
    else:
        head = (f"{name}（{product.get('name_en', '')}）：{uses}。"
                f"收录 {count} 个接口，覆盖{names}；免费版需自备上游 TikHub API Key。")
    tail = ("当用户说\"下载这个抖音视频无水印\"\"把这个号的评论导出\""
            "\"今天微博热搜是什么\"\"找几个小红书达人\"时使用；"
            "只提供只读数据接口，不含登录、发布、点赞等写操作。")
    return head + tail


def skillhub_meta(product, loaded, edition, count):
    ed = "付费版" if edition == "pro" else "自备 API Key 版"
    uses = "下载无水印视频、解析分享链接、批量导出评论、查账号与作品数据、追热搜热榜、找达人"
    if edition == "pro":
        desc_zh = (f"{product['name_zh']}（付费版）：{uses}。"
                   f"含 {count} 个接口与 CLI，覆盖抖音、微博、小红书、B站、知乎、微信、快手。"
                   "标准 ¥0.10/次；高价值/批量走额度包（6/30 点每次，¥9.90/200 点）。")
        desc_en = (f"{product.get('name_en', '')} (paid): download watermark-free videos, "
                   "parse share links, export comments, inspect accounts and trends, find creators. "
                   f"{count} endpoints and a CLI covering 7 Chinese social platforms. "
                   "Standard CNY 0.10 per call; premium/batch via credits "
                   "(6/30 credits per call, CNY 9.90 for 200 credits).")
    else:
        desc_zh = (f"{product['name_zh']}（自备 API Key）：{uses}。"
                   f"含 {count} 个接口与 CLI，覆盖抖音、微博、小红书、B站、知乎、微信、快手。"
                   "需自备上游 TikHub Token（起充 5 美元）；不想充值可使用付费版。")
        desc_en = (f"{product.get('name_en', '')} (bring your own API key): download "
                   "watermark-free videos, parse share links, export comments, inspect accounts "
                   f"and trends, find creators. {count} endpoints and a CLI covering 7 platforms. "
                   "Requires your own TikHub token; use the paid version for pay-per-call.")
    examples = list(product.get("examples_zh") or [])
    for meta, _ in loaded:
        for x in meta.get("usage_zh") or []:
            if x not in examples:
                examples.append(x)
    return {
        "name": f"{product['name_zh']}（{ed}）",
        "version": product["version"],
        "pay_mode": 0 if edition == "free" else 1,
        "description_zh": desc_zh,
        "description_en": desc_en,
        "examples_zh": examples[:12],
        "iconSource": "letter:auto",
    }


def check_pricing(product):
    """product.json 的 pricing 必须与 gateway/pricing.py 一致，否则预估价会和实扣不一致。"""
    sys.path.insert(0, os.path.join(ROOT, "gateway"))
    try:
        import pricing
    except Exception as exc:  # noqa: BLE001
        die(f"无法导入 gateway/pricing.py 做定价一致性校验：{exc}")
    p = product.get("pricing") or {}
    tiers = p.get("tiers") or {}
    for name, spec in pricing.TIERS.items():
        mine = tiers.get(name) or {}
        for key in ("credits", "amount"):
            if mine.get(key) != spec.get(key):
                die(f"pricing 不一致：{name}.{key} product={mine.get(key)!r} "
                    f"gateway={spec.get(key)!r}")
        if mine.get("per_call") != spec.get("pay_per_call"):
            die(f"pricing 不一致：{name}.per_call product={mine.get('per_call')!r} "
                f"gateway={spec.get('pay_per_call')!r}")
    pack = (p.get("pack") or {})
    starter = pricing.CREDIT_PACKS["starter"]
    if pack.get("credits") != starter["credits"] or pack.get("amount") != starter["amount"]:
        die(f"pricing 不一致：pack product={pack} gateway={starter}")

    # 客户端的预估价来自 inventory 的 unit_cost_usd；网关用的是 endpoint_costs.json，
    # 两者必须一致，否则“预估”和“实扣”会对不上。
    cost_path = os.path.join(ROOT, "gateway", "endpoint_costs.json")
    if os.path.exists(cost_path):
        costs = (load_json(cost_path) or {}).get("costs") or {}
        for slug in product["platforms"]:
            inv_path = os.path.join(PLATFORMS_DIR, slug, "references", "inventory.json")
            if not os.path.exists(inv_path):
                continue
            for row in load_json(inv_path):
                cost = row.get("unit_cost_usd")
                want = costs.get(row["path"])
                if cost is not None and (want is None or abs(float(want) - float(cost)) > 1e-9):
                    die(f"定价表与清单不一致：{row['path']} inventory={cost} "
                        f"gateway={want}；重跑 tools/collect_inventory.py")


def render(template, values):
    out = template
    for k, v in values.items():
        out = out.replace("{{" + k + "}}", str(v))
    if "{{" in out:
        leftover = out[out.index("{{"):out.index("{{") + 40]
        die(f"模板还有未替换的占位符: {leftover}")
    return out


def merged_index(product, groups):
    """groups: [(meta, rows)]，生成 references/index.md。"""
    total = sum(len(rows) for _, rows in groups)
    folders = sum(len({r["folder"] for r in rows}) for _, rows in groups)
    lines = [
        f"# {product['name_zh']} · 接口分类导航",
        "",
        f"共 {total} 个接口，{folders} 个分类，{len(groups)} 个平台。"
        "按需打开对应文件，**不要一次全部载入上下文**。",
        "",
        "- 机器可读清单：`references/inventory.json`",
        "- 查接口：`python3 scripts/social.py search <关键词>` / `show <path>`",
        "",
    ]
    for meta, rows in groups:
        counts = {}
        for r in rows:
            counts[r["folder"]] = counts.get(r["folder"], 0) + 1
        lines += [f"## {meta['platform_zh']}（{len(rows)}）", "",
                  "| 分类 | 接口数 | 参考文件 |", "|---|---|---|"]
        for folder, n in sorted(counts.items(), key=lambda x: (-x[1], x[0])):
            lines.append(f"| {folder} | {n} | `references/{folder}.md` |")
        lines.append("")
    return "\n".join(lines)


def merge_references(product, loaded, dst_ref):
    """把多个平台的 references/ 合并成一份，并生成全局索引。"""
    if os.path.isdir(dst_ref):
        shutil.rmtree(dst_ref)
    os.makedirs(dst_ref, exist_ok=True)

    groups = []
    merged = []
    plat_meta = {}
    folder_owner = {}
    for meta, pdir in loaded:
        slug = meta["platform"]
        ref = os.path.join(pdir, "references")
        for fn in sorted(os.listdir(ref)):
            if not fn.endswith(".md") or fn in ("index.md", "api-index.md"):
                continue
            if fn in folder_owner and folder_owner[fn] != slug:
                die(f"分类文档重名：{fn}（{folder_owner[fn]} / {slug}），"
                    "请在采集器里给 folder 加平台前缀")
            folder_owner[fn] = slug
            shutil.copy2(os.path.join(ref, fn), os.path.join(dst_ref, fn))
        rows = load_json(os.path.join(ref, "inventory.json"))
        for r in rows:
            r["platform"] = slug
            r["platform_zh"] = meta["platform_zh"]
        merged.extend(rows)
        groups.append((meta, rows))
        pm = os.path.join(ref, "_meta.json")
        if os.path.exists(pm):
            plat_meta[slug] = load_json(pm)

    paths = [r["path"] for r in merged]
    if len(paths) != len(set(paths)):
        dup = sorted({p for p in paths if paths.count(p) > 1})
        die(f"合并后的 path 不唯一：{dup[:5]}")

    with open(os.path.join(dst_ref, "inventory.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(merged, f, ensure_ascii=False, indent=1)
        f.write("\n")
    write(os.path.join(dst_ref, "index.md"), merged_index(product, groups))
    write(os.path.join(dst_ref, "_meta.json"), json.dumps({
        "skill": product["slug"],
        "version": product["version"],
        "count": len(merged),
        "priced_endpoints": sum(1 for r in merged if r.get("unit_cost_usd") is not None),
        "platforms": {
            meta["platform"]: {
                "zh": meta["platform_zh"],
                "count": len(rows),
                "spec_version": (plat_meta.get(meta["platform"]) or {}).get("spec_version", ""),
            } for meta, rows in groups
        },
    }, ensure_ascii=False, indent=1) + "\n")
    return merged, groups


def zip_skill(name, target):
    """把 skills/<name>/ 打成 dist/<name>.zip，zip 根下保留 skill 目录。"""
    os.makedirs(DIST, exist_ok=True)
    out = os.path.join(DIST, f"{name}.zip")
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk(target):
            # _probe / out 是本地调试产物，别打进发布包
            dirs[:] = [d for d in dirs if d not in ("__pycache__", ".git", "_probe", "out")]
            for f in files:
                if f in (".token", ".payment-needed.txt", "_usage.txt") or f.endswith(".local"):
                    continue
                p = os.path.join(root, f)
                z.write(p, os.path.relpath(p, OUT))
    return out


def check_one(product, loaded, ed, name, target):
    ok = os.path.isdir(target) and all(
        os.path.exists(os.path.join(target, f)) for f in REQUIRED)
    problems = []
    if ok:
        skill_md = open(os.path.join(target, "SKILL.md"), encoding="utf-8").read()
        lines = skill_md.count("\n") + 1
        if "{{" in skill_md:
            problems.append("SKILL.md 仍有未替换占位符")
        if FULL_TABLE.search(skill_md):
            problems.append("SKILL.md 出现分类接口平铺表")
        if lines > 320:
            problems.append(f"SKILL.md 行数 {lines} > 320")
        inv = load_json(os.path.join(target, "references", "inventory.json"))
        by_p = {}
        for r in inv:
            by_p[r.get("platform")] = by_p.get(r.get("platform"), 0) + 1
        missing = [m["platform"] for m, _ in loaded if not by_p.get(m["platform"])]
        if missing:
            problems.append("清单缺平台：" + "、".join(missing))
        folders = {r["folder"] for r in inv}
        nofile = [f for f in folders
                  if not os.path.exists(os.path.join(target, "references", f + ".md"))]
        if nofile:
            problems.append("缺分类文档：" + "、".join(sorted(nofile)))
        if os.path.exists(os.path.join(target, "references", "api-index.md")):
            problems.append("不应再有 references/api-index.md")
    else:
        problems.append("产物缺文件")
    print(f"[build] {'OK  ' if not problems else 'FAIL'} {name:22s} "
          f"({ed['label_zh']})" + ("" if not problems else "：" + "；".join(problems)))
    return not problems


def build_one(product, loaded, ed, check, do_zip=False):
    name = f"{product['slug']}{ed['suffix']}"
    target = os.path.join(OUT, name)

    tpl_path = os.path.join(CORE, f"SKILL.{ed['edition']}.template.md")
    if not os.path.exists(tpl_path):
        die(f"找不到模板 {tpl_path}")

    if check:
        return check_one(product, loaded, ed, name, target)

    merge_references(product, loaded, os.path.join(target, "references"))
    count = len(load_json(os.path.join(target, "references", "inventory.json")))
    groups = [(meta, load_json(os.path.join(pdir, "references", "inventory.json")))
              for meta, pdir in loaded]

    # 图标：付费版优先用带 PRO 角标的版本
    icon_src = os.path.join(SRC, "assets", "_icon_pro.png" if ed["edition"] == "pro"
                            else "_icon.png")
    if not os.path.exists(icon_src):
        die(f"找不到图标 {icon_src}；先运行 python tools/make_icons.py --product")
    shutil.copy2(icon_src, os.path.join(target, "_icon.png"))

    # 唯一的 CLI 实现
    dst_scripts = os.path.join(target, "scripts")
    os.makedirs(dst_scripts, exist_ok=True)
    shutil.copy2(os.path.join(CORE, "social.py"), os.path.join(dst_scripts, "social.py"))

    # 运行时元信息：版本与平台都在这里，CLI 靠它区分行为
    write(os.path.join(target, "skill_meta.json"), json.dumps({
        "skill": product["slug"],
        "name_zh": product["name_zh"],
        "edition": ed["edition"],
        "base_url": ed["base_url"],
        "gateway_url": ed.get("gateway_url", ""),
        "pricing": product.get("pricing", {}),
        "platforms": [{
            "platform": meta["platform"],
            "platform_zh": meta["platform_zh"],
            "api_prefixes": meta.get("api_prefixes") or [f"/api/v1/{meta['platform']}"],
        } for meta, _ in loaded],
    }, ensure_ascii=False, indent=2) + "\n")

    skill_md = render(open(tpl_path, encoding="utf-8").read(), {
        "name": name,
        "description": description(product, loaded, ed["edition"], count),
        "version": product["version"],
        "count": count,
        "platform_table": platform_table(loaded),
        "platform_bodies": platform_bodies(loaded),
    })
    write(os.path.join(target, "SKILL.md"), skill_md)
    write(os.path.join(target, "_skillhub_meta.json"),
          json.dumps(skillhub_meta(product, loaded, ed["edition"], count),
                     ensure_ascii=False, indent=2) + "\n")

    print(f"[build] 生成 {name:22s} {count:4d} 接口 / {len(groups)} 平台 "
          f"({ed['label_zh']})")
    if do_zip:
        out = zip_skill(name, target)
        print(f"[build] 打包 {os.path.relpath(out, ROOT)}  ({os.path.getsize(out)} bytes)")
    return True


def clean_old(expected):
    if not os.path.isdir(OUT):
        return
    for name in sorted(os.listdir(OUT)):
        p = os.path.join(OUT, name)
        if os.path.isdir(p) and name not in expected:
            shutil.rmtree(p)
            print(f"[build] 清理旧产物 skills/{name}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="只校验产物完整性，不写文件")
    ap.add_argument("--zip", action="store_true", help="构建后额外生成 dist/<skill>.zip")
    ap.add_argument("--clean", action="store_true", help="删除本次未产出的旧 skill 目录")
    args = ap.parse_args()

    product = load_product()
    check_pricing(product)
    loaded = load_platforms(product)
    editions = load_editions()
    if not editions:
        die("src/editions 下没有版本配置")

    ok_all = True
    expected = []
    for ed in editions.values():
        name = f"{product['slug']}{ed['suffix']}"
        expected.append(name)
        if ed["edition"] == "pro" and not ed.get("gateway_url") and not args.check:
            print("[build] 注意：付费版未配置 gateway_url，"
                  "生成的 skill 调用时会报错（用 GATEWAY_URL 环境变量覆盖）")
        ok_all &= build_one(product, loaded, ed, args.check, args.zip)

    if args.clean and not args.check:
        clean_old(set(expected))

    print(f"\n[build] {'校验' if args.check else '构建'}完成："
          f"{len(loaded)} 平台 × {len(editions)} 版本 = {len(expected)} 个 skill")
    if not ok_all:
        sys.exit(1)


if __name__ == "__main__":
    main()
