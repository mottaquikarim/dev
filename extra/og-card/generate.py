#!/usr/bin/env python3
"""Regenerate blog/static/og-card.jpg, the 1200x630 image used for Open Graph /
Twitter link previews.

Only needs re-running when the name, tagline or photo on the card changes.

    pip install Pillow
    python3 extra/og-card/generate.py

Colours are the ones the etch theme uses in dark mode (themes/etch/assets/css/dark.css).
"""

import os

from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
PHOTO = os.path.join(ROOT, "blog", "static", "img", "taq_karim_profile.jpg")
OUT = os.path.join(ROOT, "blog", "static", "og-card.jpg")

W, H = 1200, 630
BG = (18, 18, 18)  # #121212  body background
FG = (235, 235, 235)  # #ebebeb  body text
MUTED = (154, 160, 163)
ACCENT = (0, 177, 237)  # #00b1ed  link colour

FONTS = "/usr/share/fonts/truetype/dejavu/"
NAME = "Taq Karim"
TAGLINE = ["Thoughts on code and", "building things."]
URL = "mottaquikarim.github.io/dev"


def main():
    name_f = ImageFont.truetype(FONTS + "DejaVuSans-Bold.ttf", 82)
    tag_f = ImageFont.truetype(FONTS + "DejaVuSans.ttf", 34)
    url_f = ImageFont.truetype(FONTS + "DejaVuSansMono.ttf", 26)

    card = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(card)

    # Circular headshot on the right.
    photo = ImageOps.exif_transpose(Image.open(PHOTO)).convert("RGB")
    diameter = 360
    photo = ImageOps.fit(
        photo, (diameter, diameter), method=Image.LANCZOS, centering=(0.5, 0.32)
    )
    # Draw the mask oversized and downsample it so the circle edge stays smooth.
    mask = Image.new("L", (diameter * 4, diameter * 4), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, diameter * 4 - 1, diameter * 4 - 1), fill=255)
    mask = mask.resize((diameter, diameter), Image.LANCZOS)

    px, py = W - diameter - 90, (H - diameter) // 2
    d.ellipse(
        (px - 5, py - 5, px + diameter + 4, py + diameter + 4),
        outline=(46, 46, 46),
        width=5,
    )
    card.paste(photo, (px, py), mask)

    # Text block on the left.
    x = 90
    d.text((x, 214), NAME, font=name_f, fill=FG)
    for i, line in enumerate(TAGLINE):
        d.text((x, 322 + i * 44), line, font=tag_f, fill=MUTED)
    d.text((x, 440), URL, font=url_f, fill=ACCENT)

    # Accent rule along the bottom edge.
    d.rectangle((0, H - 8, W, H), fill=ACCENT)

    card.save(OUT, "JPEG", quality=88, optimize=True, progressive=True)
    print("wrote %s (%dx%d)" % (OUT, W, H))


if __name__ == "__main__":
    main()
