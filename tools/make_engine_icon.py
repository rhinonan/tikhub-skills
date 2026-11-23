#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成「中文社媒数据引擎」的 1024 图标母版。

    assets/icon-src/cn-social-data.png

只是一个中性占位母版：深色渐变 + 七节点网络 + 「社媒数据」字样。

⚠️ 正式母版走 AI 出图：生图模型 → tools/prep_ai_icon.py → tools/make_icons.py --product。
   本脚本只在无网 / 无生图额度时兜底，直接运行会覆盖正式母版。

后续有正式设计稿时，直接替换该文件并重跑：

    python tools/make_engine_icon.py
    python tools/make_icons.py --product

依赖：pillow
"""

import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "icon-src", "cn-social-data.png")

SIZE = 1024
CENTER = (SIZE // 2, 400)
RING = 205
NODE = 27
CORE = 62

FONT_CANDIDATES = [
    "C:/Windows/Fonts/msyhbd.ttc",
    "C:/Windows/Fonts/msyh.ttc",
    "/System/Library/Fonts/PingFang.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
]

NODE_COLORS = [
    (56, 189, 248), (45, 212, 191), (129, 140, 248),
    (244, 114, 182), (250, 204, 21), (52, 211, 153), (96, 165, 250),
]


def gradient(size, c1, c2):
    w, h = size
    strip = Image.new("RGB", (1, h))
    px = strip.load()
    for y in range(h):
        t = y / max(h - 1, 1)
        px[0, y] = tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))
    return strip.resize((w, h), Image.BILINEAR)


def find_font(size):
    for path in FONT_CANDIDATES:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def main():
    im = gradient((SIZE, SIZE), (15, 23, 42), (30, 58, 138)).convert("RGBA")

    glow = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([CENTER[0] - 330, CENTER[1] - 330, CENTER[0] + 330, CENTER[1] + 330],
               fill=(56, 189, 248, 55))
    im = Image.alpha_composite(im, glow.filter(ImageFilter.GaussianBlur(130)))

    d = ImageDraw.Draw(im)
    # 同心调试圈
    for r, alpha in ((300, 26), (235, 34)):
        d.ellipse([CENTER[0] - r, CENTER[1] - r, CENTER[0] + r, CENTER[1] + r],
                  outline=(148, 163, 184, alpha), width=2)

    # 七节点网络
    import math
    points = []
    for i in range(7):
        ang = -math.pi / 2 + i * 2 * math.pi / 7
        points.append((CENTER[0] + RING * math.cos(ang),
                       CENTER[1] + RING * math.sin(ang)))
    for p in points:
        d.line([CENTER, p], fill=(148, 163, 184, 120), width=5)
    for i, p in enumerate(points):
        col = NODE_COLORS[i % len(NODE_COLORS)]
        d.ellipse([p[0] - NODE, p[1] - NODE, p[0] + NODE, p[1] + NODE], fill=col + (255,))
    d.ellipse([CENTER[0] - CORE, CENTER[1] - CORE, CENTER[0] + CORE, CENTER[1] + CORE],
              fill=(241, 245, 249, 255))

    # 标题（放在 PRO 徽章上方，留出底部空间）
    font = find_font(104)
    text = "社媒数据"
    track = 8
    widths = [font.getbbox(ch)[2] - font.getbbox(ch)[0] for ch in text]
    total = sum(widths) + track * (len(text) - 1)
    x = (SIZE - total) // 2
    bbox = font.getbbox(text)
    y = 690 - bbox[1]
    for ch, w in zip(text, widths):
        d.text((x, y), ch, font=font, fill=(248, 250, 252, 255))
        x += w + track

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    im.save(OUT, optimize=True)
    print(f"[icon] 已生成 {os.path.relpath(OUT, ROOT)}（{SIZE}px）")


if __name__ == "__main__":
    main()
