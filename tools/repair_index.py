#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复 inventory.json 的 name_zh/name_en 错切，并按清单重生成 api-index.md。

背景：采集时用 name.split("/") 切中英文，遇到「搜索直播间(抖音号/昵称)」
这类名字里本来就带 "/" 的，会把中文名切掉一半（name_zh="搜索直播间(抖音号"），
下游 search/show/速查表全部跟着错。这里按"右侧不含中文"的边界重新切。

用法：
    python tools/repair_index.py            # 只打印将要改的内容
    python tools/repair_index.py --write    # 实际写入 inventory.json + api-index.md
"""
import argparse
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF = os.path.join(ROOT, "src", "platforms", "douyin", "references")
INV = os.path.join(REF, "inventory.json")
IDX = os.path.join(REF, "api-index.md")
CJK = re.compile(r"[\u4e00-\u9fff]")


def split_name(name):
    """在「左边有中文、右边没有中文」的第一个斜杠处切中英文名。"""
    for m in re.finditer(r"/(?=\s*[A-Za-z\[])", name):
        left, right = name[:m.start()], name[m.start() + 1:]
        if CJK.search(left) and not CJK.search(right):
            return left.strip(), right.strip()
    return name.strip(), ""


def broken(r):
    zh, en = r.get("name_zh") or "", r.get("name_en") or ""
    if zh.count("(") != zh.count(")"):
        return True
    if en and (CJK.search(en) or en[0] in "）)"):
        return True
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    rows = json.load(open(INV, encoding="utf-8"))
    fixed = 0
    for r in rows:
        zh, en = split_name(r["name"])
        if not en:                      # 纯中文名，保留原英文
            en = r.get("name_en") or ""
        if en and CJK.search(en):       # 英文名里混着中文，说明源文档只有中文名
            en = ""
        if (zh, en) != (r.get("name_zh"), r.get("name_en")):
            tag = "BROKEN" if broken(r) else "align "
            print(f"[{tag}] {r['path']}")
            print(f"    zh: {r.get('name_zh')!r} -> {zh!r}")
            print(f"    en: {r.get('name_en')!r} -> {en!r}")
            r["name_zh"], r["name_en"] = zh, en
            fixed += 1

    # 速查表：沿用原文件的行序（采集时人工排过序，不要重排），只更新名称列
    order = []
    if os.path.exists(IDX):
        for line in open(IDX, encoding="utf-8"):
            m = re.search(r"`(/api/\S+)`", line)
            if m and line.startswith("| "):
                order.append(m.group(1))
    by_path = {r["path"]: r for r in rows}
    order = [p for p in dict.fromkeys(order) if p in by_path]
    order += [r["path"] for r in rows if r["path"] not in set(order)]

    def cell(s):
        return (s or "").replace("|", "\\|").replace("\n", " ").strip()

    out = ["# TikHub 抖音接口速查表", "",
           "| 分类 | 接口 | 方法 | 路径 |", "|---|---|---|---|"]
    for p in order:
        r = by_path[p]
        out.append(f"| {r['folder']} | {cell(r['name_zh'])} | {r['method']} | `{p}` |")
    text = "\n".join(out) + "\n"

    print(f"\n共 {len(rows)} 条接口，修正 {fixed} 条名称。")
    if args.write:
        with open(INV, "w", encoding="utf-8", newline="\n") as f:
            json.dump(rows, f, ensure_ascii=False, indent=1)
            f.write("\n")
        with open(IDX, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        print(f"已写入 {os.path.relpath(INV, ROOT)} 与 {os.path.relpath(IDX, ROOT)}")
    else:
        print("（未写入，加 --write 生效）")


if __name__ == "__main__":
    main()
