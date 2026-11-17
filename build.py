#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 src/ 组装出 8 个 skill 目录到 skills/。

单一数据源：
    src/core/tikhub.py            唯一的 CLI 实现
    src/core/SKILL.*.template.md  SKILL.md 模板（按版本）
    src/platforms/<平台>/          inventory.json + references + 平台正文
    src/editions/<版本>.json       版本配置

产物：
    skills/tikhub-douyin/  skills/tikhub-douyin-pro/  ...

用法：
    python build.py            # 构建所有平台 × 所有版本
    python build.py --check    # 只校验，不写文件
    python build.py --zip      # 构建并生成 dist/<skill>.zip
    GATEWAY_URL=https://x python build.py   # 覆盖付费版网关地址
"""
import argparse
import json
import os
import shutil
import sys
import zipfile

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
OUT = os.path.join(ROOT, "skills")
DIST = os.path.join(ROOT, "dist")
PLATFORMS_DIR = os.path.join(SRC, "platforms")
EDITIONS_DIR = os.path.join(SRC, "editions")
CORE = os.path.join(SRC, "core")

# 每个 skill 必须有这些文件，少一个就算构建不合格
REQUIRED = ["SKILL.md", "skill_meta.json", "_skillhub_meta.json",
            "scripts/tikhub.py", "references/inventory.json"]


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


def load_platforms():
    if not os.path.isdir(PLATFORMS_DIR):
        die(f"找不到 {PLATFORMS_DIR}")
    out = []
    for name in sorted(os.listdir(PLATFORMS_DIR)):
        pdir = os.path.join(PLATFORMS_DIR, name)
        if not os.path.isdir(pdir):
            continue
        meta_path = os.path.join(pdir, "meta.json")
        inv_path = os.path.join(pdir, "references", "inventory.json")
        if not os.path.exists(meta_path):
            print(f"[build] 跳过 {name}：缺 meta.json")
            continue
        if not os.path.exists(inv_path):
            print(f"[build] 跳过 {name}：缺 references/inventory.json（等 P4 采集）")
            continue
        out.append((load_json(meta_path), pdir))
    if not out:
        die("没有任何可构建的平台")
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


def index_table(rows):
    counts = {}
    for r in rows:
        counts[r["folder"]] = counts.get(r["folder"], 0) + 1
    lines = ["| 分类 | 接口数 | 参考文件 |", "|---|---|---|"]
    for folder, n in sorted(counts.items(), key=lambda x: -x[1]):
        lines.append(f"| {folder} | {n} | `references/{folder}.md` |")
    return "\n".join(lines)


def biggest_folder(rows):
    counts = {}
    for r in rows:
        counts[r["folder"]] = counts.get(r["folder"], 0) + 1
    return max(counts, key=counts.get) if counts else ""


def description(meta, edition, count):
    zh, en, scope = meta["platform_zh"], meta.get("platform_en", ""), meta.get("scope", "")
    if edition == "pro":
        head = (f"{zh}（{en}）数据接口调用（付费版，按次付费："
                f"标准 ¥0.10/次、高价值 ¥0.50/次、批量 ¥2.00/次，"
                f"用户无需注册或充值 TikHub），收录 {count} 个{zh}相关接口：")
    else:
        head = (f"{zh}（{en}）数据接口调用与接口查询，基于 TikHub.io API，"
                f"收录 {count} 个{zh}相关接口：")
    tail = (f"。当用户要抓取{zh}作品/账号/评论/搜索/热榜数据，"
            f"或问\"{zh}某个数据怎么拿\"\"TikHub 有没有 XX 接口\"时使用。"
            f"本 skill 只收{zh}，不含其他平台；"
            f"不提供登录、发布、点赞等写操作。")
    return head + scope + tail


def skill_meta_json(meta, edition, count):
    zh = meta["platform_zh"]
    ed = "付费版" if edition == "pro" else "自备 API Key 版"
    if edition == "pro":
        desc_zh = (f"{zh}数据接口索引与调用工具（付费版），含 {count} 个接口与 CLI。"
                   "按次付费：标准 ¥0.10/次、高价值 ¥0.50/次、批量 ¥2.00/次；"
                   "额度包 ¥9.90（约 10–200 次）。")
        desc_en = (f"{zh} data API index and client (paid) with {count} endpoints and a CLI. "
                   "Pay per call: standard CNY 0.10, premium 0.50, batch 2.00; "
                   "credit pack CNY 9.90 (~10-200 calls).")
    else:
        desc_zh = (f"{zh}数据接口索引与调用工具（自备 API Key），含 {count} 个接口与 CLI。"
                   "需自备 TikHub Token（起充 5 美元）；不想充值可使用 Pro 版。")
        desc_en = (f"{zh} data API index and client (bring your own API key) "
                   f"with {count} endpoints and a CLI. "
                   "Requires your own TikHub token (USD 5 minimum top-up); "
                   "use the Pro version if you prefer pay-per-call.")
    return {
        "name": f"TikHub {zh}数据接口（{ed}）",
        "version": meta.get("version", "1.0.0"),
        "pay_mode": 0 if edition == "free" else 1,
        "description_zh": desc_zh,
        "description_en": desc_en,
        "examples_zh": meta.get("usage_zh", []),
        "iconSource": "letter:auto",
    }


def render(template, values):
    out = template
    for k, v in values.items():
        out = out.replace("{{" + k + "}}", str(v))
    if "{{" in out:
        leftover = out[out.index("{{"):out.index("{{") + 40]
        die(f"模板还有未替换的占位符: {leftover}")
    return out


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


def build_one(meta, pdir, ed, check, do_zip=False):
    platform = meta["platform"]
    name = f"tikhub-{platform}{ed['suffix']}"
    target = os.path.join(OUT, name)
    rows = load_json(os.path.join(pdir, "references", "inventory.json"))
    count = len(rows)

    tpl_name = f"SKILL.{ed['edition']}.template.md"
    tpl_path = os.path.join(CORE, tpl_name)
    if not os.path.exists(tpl_path):
        die(f"找不到模板 {tpl_path}")
    body = open(os.path.join(pdir, "skill.body.md"), encoding="utf-8").read() \
        if os.path.exists(os.path.join(pdir, "skill.body.md")) else ""

    skill_md = render(open(tpl_path, encoding="utf-8").read(), {
        "name": name,
        "description": description(meta, ed["edition"], count),
        "version": meta.get("version", "1.0.0"),
        "platform_zh": meta["platform_zh"],
        "platform": platform,
        "api_prefix": meta.get("api_prefix", ""),
        "scope": meta.get("scope", ""),
        "count": count,
        "folder_example": biggest_folder(rows),
        "index_table": index_table(rows),
        "platform_body": body,
    })

    if check:
        ok = os.path.isdir(target) and all(
            os.path.exists(os.path.join(target, f)) for f in REQUIRED)
        print(f"[build] {'OK  ' if ok else 'MISS'} {name:26s} {count:4d} 接口 "
              f"({ed['label_zh']})")
        return ok

    # 1. references：整份复制，保证清单与分类文档同源
    dst_ref = os.path.join(target, "references")
    if os.path.isdir(dst_ref):
        shutil.rmtree(dst_ref)
    shutil.copytree(os.path.join(pdir, "references"), dst_ref)

    # 2. 图标：付费版优先用带 PRO 角标的 _icon_pro.png（由 tools/make_icons.py 生成）
    icon_src = os.path.join(pdir, "_icon_pro.png" if ed["edition"] == "pro" else "_icon.png")
    if not os.path.exists(icon_src):
        icon_src = os.path.join(pdir, "_icon.png")
    if os.path.exists(icon_src):
        os.makedirs(target, exist_ok=True)
        shutil.copy2(icon_src, os.path.join(target, "_icon.png"))

    # 3. 唯一的 CLI 实现
    dst_scripts = os.path.join(target, "scripts")
    os.makedirs(dst_scripts, exist_ok=True)
    shutil.copy2(os.path.join(CORE, "tikhub.py"), os.path.join(dst_scripts, "tikhub.py"))

    # 4. 运行时元信息：平台与版本都在这里，CLI 靠它区分行为
    write(os.path.join(target, "skill_meta.json"), json.dumps({
        "platform": platform,
        "platform_zh": meta["platform_zh"],
        "edition": ed["edition"],
        "base_url": ed["base_url"],
        "gateway_url": ed.get("gateway_url", ""),
        "api_prefix": meta.get("api_prefix", ""),
    }, ensure_ascii=False, indent=2) + "\n")

    # 5. 文档与上架元信息
    write(os.path.join(target, "SKILL.md"), skill_md)
    write(os.path.join(target, "_skillhub_meta.json"),
          json.dumps(skill_meta_json(meta, ed["edition"], count),
                     ensure_ascii=False, indent=2) + "\n")

    print(f"[build] 生成 {name:26s} {count:4d} 接口 ({ed['label_zh']})")
    if do_zip:
        out = zip_skill(name, target)
        print(f"[build] 打包 {os.path.relpath(out, ROOT)}  ({os.path.getsize(out)} bytes)")
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="只校验产物完整性，不写文件")
    ap.add_argument("--zip", action="store_true", help="构建后额外生成 dist/<skill>.zip")
    args = ap.parse_args()

    platforms = load_platforms()
    editions = load_editions()
    if not editions:
        die("src/editions 下没有版本配置")

    ok_all = True
    for meta, pdir in platforms:
        for ed in editions.values():
            if ed["edition"] == "pro" and not ed.get("gateway_url") and not args.check:
                print("[build] 注意：付费版未配置 gateway_url，"
                      "生成的 skill 调用时会报错（用 GATEWAY_URL 环境变量覆盖）")
            ok_all &= build_one(meta, pdir, ed, args.check, args.zip)

    total = len(platforms) * len(editions)
    print(f"\n[build] {'校验' if args.check else '构建'}完成："
          f"{len(platforms)} 平台 × {len(editions)} 版本 = {total} 个 skill")
    if not ok_all:
        sys.exit(1)


if __name__ == "__main__":
    main()
