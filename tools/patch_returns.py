#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把实测返回结构（returns-detail.json）写进 inventory.json 与分类 md。

分类 md 是采集脚本生成的，手改会被覆盖；把"实测结构"放在独立 JSON 里，
再由本脚本注入，既能进 CLI 的 show，也能在文档里显示，重建后重跑一次即可复原。

用法：
    python tools/patch_returns.py                 # 全部平台，只预览
    python tools/patch_returns.py --all --write   # 全部平台，写入
    python tools/patch_returns.py --platforms weibo,zhihu --write
"""

import argparse
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLATFORMS_DIR = os.path.join(ROOT, "src", "platforms")
MARK = "- 返回结构（实测）："


def platforms_from_arg(value):
    if value == "all":
        return sorted(
            d for d in os.listdir(PLATFORMS_DIR)
            if os.path.isdir(os.path.join(PLATFORMS_DIR, d))
            and os.path.exists(os.path.join(PLATFORMS_DIR, d, "references", "inventory.json"))
        )
    return [s.strip() for s in value.split(",") if s.strip()]


def load_map(path):
    raw = json.load(open(path, encoding="utf-8"))
    return {k: v for k, v in raw.items() if not k.startswith("_")}


def inject_block(block, lines):
    """在 `- 返回：` 之后插入实测结构；已有则先删旧块，保证幂等。

    只删「MARK 行 + 紧跟着的缩进行」，别整块按前缀过滤——参数行长得一样。
    """
    kept = []
    skipping = False
    for line in block.split("\n"):
        if line.startswith(MARK):
            skipping = True
            continue
        if skipping and line.startswith("  "):
            continue
        skipping = False
        kept.append(line)
    text = "\n".join(kept)
    payload = "\n" + MARK + "\n" + "\n".join(f"  - {l}" for l in lines)
    return text.rstrip("\n") + payload + "\n"


def patch_platform(slug, write):
    pdir = os.path.join(PLATFORMS_DIR, slug)
    ref = os.path.join(pdir, "references")
    src = os.path.join(pdir, "returns-detail.json")
    inv = os.path.join(ref, "inventory.json")
    if not os.path.exists(src):
        print(f"[patch] {slug:12s} 跳过：没有 returns-detail.json")
        return
    mapping = load_map(src)
    if not mapping:
        print(f"[patch] {slug:12s} 跳过：returns-detail.json 没有条目")
        return

    rows = json.load(open(inv, encoding="utf-8"))
    by_path = {r["path"]: r for r in rows}
    missing = [p for p in mapping if p not in by_path]
    if missing:
        print(f"[patch] {slug:12s} WARN inventory 里没有：{missing[:5]}")

    for p, lines in mapping.items():
        if p in by_path:
            by_path[p]["returns_detail"] = lines

    touched = {}
    for folder in sorted({by_path[p]["folder"] for p in mapping if p in by_path}):
        fp = os.path.join(ref, f"{folder}.md")
        if not os.path.exists(fp):
            continue
        text = open(fp, encoding="utf-8").read()
        chunks = text.split("\n## ")
        out = [chunks[0]]
        for chunk in chunks[1:]:
            block = "## " + chunk
            m = re.search(r"`(?:GET|POST|PUT|DELETE|PATCH) (/api/\S+)`", block)
            if m and m.group(1) in mapping:
                block = inject_block(block, mapping[m.group(1)])
                touched[m.group(1)] = folder
            out.append(block)
        new = "\n".join(out)
        if write and new != text:
            open(fp, "w", encoding="utf-8", newline="\n").write(new)

    lost = [p for p in mapping if p in by_path and p not in touched]
    if lost:
        print(f"[patch] {slug:12s} WARN 以下 path 没在 md 里找到标题：{lost[:5]}")

    if write:
        with open(inv, "w", encoding="utf-8", newline="\n") as f:
            json.dump(rows, f, ensure_ascii=False, indent=1)
            f.write("\n")
    print(f"[patch] {slug:12s} 注入 {len([p for p in mapping if p in by_path])} 条"
          + (f"，写到 {len(touched)} 个分类 md" if write else "（未写入，加 --write 生效）"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--platforms", default="all", help="逗号分隔的 slug，或 all")
    ap.add_argument("--all", action="store_true", help="等价于 --platforms all")
    ap.add_argument("--write", action="store_true", help="实际写入")
    args = ap.parse_args()
    slugs = platforms_from_arg("all" if args.all else args.platforms)
    for slug in slugs:
        patch_platform(slug, args.write)


if __name__ == "__main__":
    main()
