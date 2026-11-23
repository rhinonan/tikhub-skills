#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 AI 出的图标收拾成可用的 1024 母版。

生图模型输出有三个固定毛病，这里一次性修掉：

1. 右下角压着「AI生成 WORKBUDD」水印 —— 按行取左侧干净列的中位色重建，边缘羽化；
2. 圆角外可能是纯白 / 纯黑底 —— 换成与内部一致的底色（圆角交给 make_icons.py 统一裁）；
3. 尺寸不一定是 1024 正方形 —— 居中裁切后缩放。

    python tools/prep_ai_icon.py .local/logos/gen/xxx.png \\
        --out assets/icon-src/cn-social-data.png

依赖：pillow
"""

import os
import sys
from statistics import median

from PIL import Image, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SIZE = 1024


def _median_rgb(pixels):
    return tuple(round(median([p[i] for p in pixels])) for i in range(3))


def _lum(p):
    return 0.2126 * p[0] + 0.7152 * p[1] + 0.0722 * p[2]


def normalize(im):
    """居中裁成正方形再缩放到 SIZE。"""
    w, h = im.size
    if w != h:
        side = min(w, h)
        im = im.crop(((w - side) // 2, (h - side) // 2,
                      (w + side) // 2, (h + side) // 2))
    if im.size[0] != SIZE:
        im = im.resize((SIZE, SIZE), Image.LANCZOS)
    return im


def clean_corners(im):
    """圆角外若露出白/黑底，用内侧底色铺平（圆角由 make_icons 统一裁）。"""
    w, h = im.size
    probe = [(3, 3), (w - 4, 3), (3, h - 4), (w - 4, h - 4)]
    corners = [im.getpixel(p) for p in probe]
    edge = _median_rgb([im.getpixel((w // 2, 3)), im.getpixel((3, h // 2)),
                        im.getpixel((w - 4, h // 2)), im.getpixel((w // 2, h - 4))])
    spread = max(max(c) - min(c) for c in corners)
    if spread < 26 and max(abs(_lum(c) - _lum(edge)) for c in corners) < 26:
        return im, False            # 四角已经是同一片暗底，不动

    fill = _median_rgb([im.getpixel((int(w * 0.14), int(h * 0.14))),
                        im.getpixel((int(w * 0.86), int(h * 0.14))),
                        im.getpixel((int(w * 0.14), int(h * 0.86))),
                        im.getpixel((int(w * 0.86), int(h * 0.86)))])
    mask = Image.new("L", (w, h), 0)
    from PIL import ImageDraw
    ImageDraw.Draw(mask).rounded_rectangle(
        [0, 0, w - 1, h - 1], radius=round(w * 0.30), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(6)).point(lambda v: 255 - v)
    solid = Image.new("RGB", (w, h), fill)
    return Image.composite(solid, im, mask), True


def remove_watermark(im, box_ratio=(0.80, 0.88, 1.0, 1.0)):
    """右下角水印：按行用左侧干净列的中位色重建，左侧与上方各羽化 40px。"""
    w, h = im.size
    x0, y0 = int(w * box_ratio[0]), int(h * box_ratio[1])
    x0, y0 = max(x0 - 14, 0), max(y0 - 14, 0)

    # 用该行左侧 200px 干净带的中位色
    px = im.load()
    patch = Image.new("RGB", (w - x0, h - y0))
    ppx = patch.load()
    for y in range(y0, h):
        band = [px[x, y] for x in range(max(x0 - 240, 0), max(x0 - 40, 1))]
        c = _median_rgb(band) if band else px[x0 - 1, y]
        for x in range(x0, w):
            ppx[x - x0, y - y0] = c
    patch = patch.filter(ImageFilter.GaussianBlur(2))

    # 羽化遮罩：左侧 / 上方渐入
    mask = Image.new("L", patch.size, 255)
    mpx = mask.load()
    feather = 44
    for y in range(mask.size[1]):
        for x in range(mask.size[0]):
            a = 255
            if x < feather:
                a = min(a, round(255 * x / feather))
            if y < feather:
                a = min(a, round(255 * y / feather))
            mpx[x, y] = a

    base = im.copy()
    base.paste(patch, (x0, y0), mask)
    return base


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    if not args:
        raise SystemExit(__doc__)
    src = args[0]
    out = os.path.join(ROOT, "assets", "icon-src", "cn-social-data.png")
    if "--out" in sys.argv:
        out = sys.argv[sys.argv.index("--out") + 1]
        out = out if os.path.isabs(out) else os.path.join(ROOT, out)

    im = normalize(Image.open(src).convert("RGB"))
    im, fixed = clean_corners(im)
    im = remove_watermark(im)

    os.makedirs(os.path.dirname(out), exist_ok=True)
    im.save(out, optimize=True)
    print(f"[prep] {os.path.relpath(src, ROOT)} -> {os.path.relpath(out, ROOT)}"
          f"（{SIZE}px，四角{'已铺平' if fixed else '无需处理'}，水印已清）")


if __name__ == "__main__":
    main()
