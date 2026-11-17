#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把实测返回结构（returns-detail.json）写进 inventory.json 与分类 md。

为什么单独一层：分类 md 是采集脚本生成的，手改会被覆盖；
把"实测结构"放在独立 JSON 里，再由本脚本注入，既能进 CLI 的 show，
也能在文档里显示，重建后仍需跑一次 --write 即可复原。

用法：
    python tools/patch_returns.py            # 只预览
    python tools/patch_returns.py --write    # 写入 inventory.json + references/*.md
"""
import argparse
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDIR = os.path.join(ROOT, "src", "platforms", "douyin")
REF = os.path.join(PDIR, "references")
SRC = os.path.join(PDIR, "returns-detail.json")
INV = os.path.join(REF, "inventory.json")
MARK = "- 返回结构（实测 2026-11-17）："


def load_map():
    raw = json.load(open(SRC, encoding="utf-8"))
    return {k: v for k, v in raw.items() if not k.startswith("_")}


def inject_block(block, lines):
    """在 `- 返回：` 之后插入实测结构；已有则先删旧块，保证幂等。

    注意：只删「MARK 行 + 紧跟着的缩进行」，别整块按前缀过滤——
    参数行（`  - \\`uid\\` ...`）长得一样，会被一起吃掉。
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

    idx = text.find("\n- 返回：")
    if idx >= 0:
        nl = text.find("\n", idx + 1)
        if nl < 0:
            nl = len(text)
        head, tail = text[:nl], text[nl:]
    else:
        # 没有"返回："行就插在路径行之后
        m = re.search(r"\n`(?:GET|POST|PUT|DELETE|PATCH) [^\n]+\n", text)
        cut = m.end() - 1 if m else len(text)
        head, tail = text[:cut], text[cut:]
    payload = "\n" + MARK + "\n" + "\n".join(f"  - {l}" for l in lines)
    return head + payload + tail


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    mapping = load_map()
    rows = json.load(open(INV, encoding="utf-8"))
    by_path = {r["path"]: r for r in rows}

    missing = [p for p in mapping if p not in by_path]
    if missing:
        raise SystemExit(f"inventory 里没有这些 path：{missing}")

    for p, lines in mapping.items():
        by_path[p]["returns_detail"] = lines
    print(f"inventory: 写入 {len(mapping)} 条 returns_detail")

    # 分类 md：按 `## ` 分块，替换/插入
    touched = {}
    for folder in sorted({by_path[p]["folder"] for p in mapping}):
        fp = os.path.join(REF, f"{folder}.md")
        text = open(fp, encoding="utf-8").read()
        chunks = re.split(r"\n(?=## )", text)
        out = []
        for chunk in chunks:
            m = re.search(r"\n`(?:GET|POST|PUT|DELETE|PATCH) (/api/\S+)`", chunk)
            if m and m.group(1) in mapping:
                chunk = inject_block(chunk, mapping[m.group(1)])
                touched[m.group(1)] = folder
            out.append(chunk)
        new = "\n".join(out)
        if args.write and new != text:
            open(fp, "w", encoding="utf-8", newline="\n").write(new)
        print(f"{folder}.md: {sum(1 for p in mapping if by_path[p]['folder'] == folder)} 个接口已注入")

    lost = [p for p in mapping if p not in touched]
    if lost:
        print(f"[WARN] 这些 path 在 md 里没找到对应标题，未注入：{lost}")

    if args.write:
        with open(INV, "w", encoding="utf-8", newline="\n") as f:
            json.dump(rows, f, ensure_ascii=False, indent=1)
            f.write("\n")
        print(f"已写入 {os.path.relpath(INV, ROOT)} 与 {len(touched)} 个 md 块")
    else:
        print("（未写入，加 --write 生效）")


if __name__ == "__main__":
    main()
