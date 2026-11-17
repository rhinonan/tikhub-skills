#!/usr/bin/env python3
"""从 1024 母版导出 skill 图标。

    assets/icon-src/<platform>.png  (1024x1024 RGBA 母版)
        -> src/platforms/<platform>/_icon.png      512x512 自备 API Key 版
        -> src/platforms/<platform>/_icon_pro.png  512x512 付费版（右下金色 PRO 徽章）

母版是手绘/生成的成品图，本脚本只做等比缩放与角标合成，不改图形本身。
build.py 在打包时会按版本挑选对应文件，见 build_one()。

依赖：pillow（build.py 本身仍是零依赖，这个脚本只在改图时手动跑）

    python tools/make_icons.py                # 全部平台
    python tools/make_icons.py douyin         # 单个平台
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(ROOT, "assets", "icon-src")
PLATFORMS_DIR = os.path.join(ROOT, "src", "platforms")

OUT_SIZE = 512          # 产物尺寸
MASTER_SIZE = 1024      # 母版尺寸
CORNER_RATIO = 0.214    # 圆角半径 / 边长（与整套一致）
INSET_RATIO = 0.004     # 四周内缩，避免母版边缘残留白边

PRO_TEXT = "PRO"
PRO_COLOR_TOP = (255, 226, 150)
PRO_COLOR_BOTTOM = (223, 160, 52)
PRO_COLOR_TEXT = (40, 26, 2)
PRO_COLOR_RIM = (255, 205, 105)

FONT_CANDIDATES = [
    "C:/Windows/Fonts/segoeuib.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]


def load_font(size):
    for path in FONT_CANDIDATES:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    raise SystemExit("找不到可用的粗体字体，请检查 FONT_CANDIDATES")


def _gradient(size, c1, c2):
    w, h = size
    strip = Image.new("RGB", (1, h))
    px = strip.load()
    for y in range(h):
        t = y / max(h - 1, 1)
        px[0, y] = tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))
    return strip.resize((w, h), Image.BILINEAR)


def _rounded_mask(size, radius, inset):
    ss = 4  # 超采样，保证圆角平滑
    m = Image.new("L", (size * ss, size * ss), 0)
    ImageDraw.Draw(m).rounded_rectangle(
        [inset * ss, inset * ss, (size - inset) * ss - 1, (size - inset) * ss - 1],
        radius=radius * ss, fill=255)
    return m.resize((size, size), Image.LANCZOS)


def apply_rounded(im, radius=None, inset=None):
    """裁成统一圆角，圆角外透明。母版若已带 alpha 则相当于再收一次边。"""
    size = im.size[0]
    radius = radius if radius is not None else round(size * CORNER_RATIO)
    inset = inset if inset is not None else round(size * INSET_RATIO)
    out = im.convert("RGBA")
    out.putalpha(Image.composite(out.getchannel("A"),
                                Image.new("L", out.size, 0),
                                _rounded_mask(size, radius, inset)))
    return out


def add_pro_badge(im, text=PRO_TEXT):
    """在底部居中压一枚金色胶囊徽章。尺寸按画布等比，1024 与 512 观感一致。"""
    im = im.copy()
    W, H = im.size
    s = W / MASTER_SIZE

    font_px = int(74 * s)
    pad = int(54 * s)
    height = int(128 * s)
    radius = height // 2
    track = int(4 * s)
    margin = int(30 * s)

    font = load_font(font_px)
    widths = [font.getbbox(ch)[2] - font.getbbox(ch)[0] for ch in text]
    text_w = sum(widths) + track * (len(text) - 1)
    box_w = int(text_w + pad * 2)
    x0 = (W - box_w) // 2
    y0 = H - margin - height
    x1, y1 = x0 + box_w, y0 + height

    # 徽章外发光
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(glow).rounded_rectangle([x0, y0, x1, y1], radius=radius,
                                           fill=PRO_COLOR_RIM + (140,))
    im = Image.alpha_composite(im, glow.filter(ImageFilter.GaussianBlur(20 * s)))

    # 胶囊本体
    pill = Image.new("RGBA", (box_w, height), (0, 0, 0, 0))
    clip = Image.new("L", (box_w, height), 0)
    ImageDraw.Draw(clip).rounded_rectangle([0, 0, box_w - 1, height - 1],
                                          radius=radius, fill=255)
    pill.paste(_gradient((box_w, height), PRO_COLOR_TOP, PRO_COLOR_BOTTOM).convert("RGBA"),
               (0, 0), clip)

    d = ImageDraw.Draw(pill)
    d.rounded_rectangle([0, 0, box_w - 1, height - 1], radius=radius,
                        outline=(255, 248, 220, 200), width=max(1, int(3 * s)))
    bbox = font.getbbox(text)
    ty = (height - (bbox[3] - bbox[1])) // 2 - bbox[1]
    cx = (box_w - text_w) // 2
    for ch, w in zip(text, widths):
        d.text((cx, ty), ch, font=font, fill=PRO_COLOR_TEXT + (255,))
        cx += w + track

    im.alpha_composite(pill, (x0, y0))

    # 极淡的金色内描边，远看即有「付费版」质感
    rim = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    inset = round(3 * s)
    ImageDraw.Draw(rim).rounded_rectangle(
        [inset, inset, W - inset - 1, H - inset - 1],
        radius=round(W * CORNER_RATIO) - inset,
        outline=PRO_COLOR_RIM + (70,), width=max(1, round(3 * s)))
    return Image.alpha_composite(im, rim)


def export(platform):
    master_path = os.path.join(SRC_DIR, f"{platform}.png")
    if not os.path.exists(master_path):
        raise SystemExit(f"缺母版：{os.path.relpath(master_path, ROOT)}")

    target_dir = os.path.join(PLATFORMS_DIR, platform)
    os.makedirs(target_dir, exist_ok=True)

    master = apply_rounded(Image.open(master_path).convert("RGBA"))
    free = master.resize((OUT_SIZE, OUT_SIZE), Image.LANCZOS)
    free.save(os.path.join(target_dir, "_icon.png"), optimize=True)

    pro = add_pro_badge(master)
    pro.resize((OUT_SIZE, OUT_SIZE), Image.LANCZOS).save(
        os.path.join(target_dir, "_icon_pro.png"), optimize=True)

    print(f"[icon] {platform:12s} -> _icon.png / _icon_pro.png  ({OUT_SIZE}px)")


def main():
    only = sys.argv[1:] or [
        os.path.splitext(f)[0]
        for f in sorted(os.listdir(SRC_DIR))
        if f.endswith(".png")
    ]
    for platform in only:
        export(platform)


if __name__ == "__main__":
    main()
