#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""拼一张产品图标的验收图：深/浅底 512、PRO 版、32–128px 小尺寸。

    python tools/make_icon_preview.py
    -> assets/icon-product-preview.png

读的是导出后的 src/assets/_icon.png / _icon_pro.png，所以要先跑 make_icons.py --product。
依赖：pillow
"""

import os

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "icon-product-preview.png")
ICON = os.path.join(ROOT, "src", "assets", "_icon.png")
ICON_PRO = os.path.join(ROOT, "src", "assets", "_icon_pro.png")

W, H = 1480, 880
DARK, LIGHT = (14, 15, 19), (244, 245, 247)
FG, FG_DARK, MUTED = (232, 236, 244), (28, 30, 36), (138, 144, 158)

FONT_BOLD = "C:/Windows/Fonts/msyhbd.ttc"
FONT_REG = "C:/Windows/Fonts/msyh.ttc"


def find_font(candidates, size):
    for p in candidates:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def main():
    f_big = find_font([FONT_BOLD, "/System/Library/Fonts/PingFang.ttc"], 32)
    f = find_font([FONT_REG, "/System/Library/Fonts/PingFang.ttc"], 22)
    f_sm = find_font([FONT_REG, "/System/Library/Fonts/PingFang.ttc"], 19)

    for p in (ICON, ICON_PRO):
        if not os.path.exists(p):
            raise SystemExit(f"缺图标 {os.path.relpath(p, ROOT)}；先跑 python tools/make_icons.py --product")

    canvas = Image.new("RGB", (W, H), DARK)
    d = ImageDraw.Draw(canvas)
    d.rectangle([W // 2, 0, W, H], fill=LIGHT)

    free = Image.open(ICON).convert("RGBA")
    pro = Image.open(ICON_PRO).convert("RGBA")

    def put(im, size, x, y):
        t = im.resize((size, size), Image.LANCZOS)
        canvas.paste(t, (x, y), t)

    d.text((48, 40), "产品图标 · 中文社媒数据引擎", font=f_big, fill=FG)
    d.text((W // 2 + 48, 40), "浅色底 / 小尺寸实测", font=f_big, fill=FG_DARK)

    top, main_size = 118, 300
    put(free, main_size, 60, top)
    d.text((60, top + main_size + 16), "免费版 512", font=f, fill=MUTED)
    put(pro, main_size, 60 + main_size + 56, top)
    d.text((60 + main_size + 56, top + main_size + 16), "付费版 512 · PRO 徽章", font=f, fill=MUTED)
    put(free, main_size, W // 2 + 60, top)
    d.text((W // 2 + 60, top + main_size + 16), "同一母版，浅底无白边", font=f, fill=(108, 114, 126))

    sizes = [128, 96, 64, 48, 32]
    base = 720
    for row_x, dark in ((60, True), (W // 2 + 60, False)):
        label_color = MUTED if dark else (108, 114, 126)
        d.text((row_x, 540), "小尺寸辨识度" + ("（深底）" if dark else "（浅底）"),
               font=f, fill=label_color)
        x = row_x
        for s in sizes:
            put(free, s, x, base - s)
            d.text((x, base + 12), f"{s}px", font=f_sm, fill=label_color)
            x += s + 46

    d.text((48, H - 52), "母版 1024 · assets/icon-src/cn-social-data.png",
           font=f_sm, fill=(96, 102, 116))
    d.text((W // 2 + 48, H - 52), "导出 src/assets/_icon.png / _icon_pro.png（512）",
           font=f_sm, fill=(140, 146, 158))

    canvas.save(OUT, optimize=True)
    print(f"[preview] -> {os.path.relpath(OUT, ROOT)}")


if __name__ == "__main__":
    main()
