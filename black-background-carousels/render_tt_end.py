#!/usr/bin/env python3
"""TikTok end slide: the FULL uncropped app screenshot, full-bleed,
with the download CTA over a scrim at the bottom. Nothing cut off."""

import os
from PIL import Image, ImageDraw
import numpy as np
import render as R

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "tt_end")
os.makedirs(OUT, exist_ok=True)
SHOTS = os.path.join(HERE, "shots")
W, H = 1080, 1920


def tt_end(closer, feature):
    img = Image.new("RGB", (W, H), R.INK)
    d = ImageDraw.Draw(img)
    shot = Image.open(os.path.join(SHOTS, feature + ".png")).convert("RGB")

    m = 96
    box_w = W - m * 2

    # the FULL screenshot, uncropped, as large as fits above the CTA —
    # nothing overlaid on it, so the timer and buttons stay visible
    sh = 1430
    sw = int(shot.width * sh / shot.height)
    shot = shot.resize((sw, sh))
    sx, sy = int((W - sw) / 2), 16
    mask = Image.new("L", (sw, sh), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, sw, sh], 40, fill=255)
    img.paste(shot, (sx, sy), mask)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([sx, sy, sx + sw, sy + sh], 40, outline=R.PINK, width=3)

    y = sy + sh + 34
    cf = R.font(R.F_MED, 38)
    tw = d.textlength(closer, font=cf)
    d.text(((W - tw) / 2, y), closer, font=cf, fill=R.PINK)
    y += 66

    bar_h = 126
    gx = np.linspace(0, 1, box_w)[None, :, None]
    g = (np.array(R.PINK)[None, None, :] * (1 - gx)
         + np.array(R.ORANGE)[None, None, :] * gx)
    bar = Image.fromarray(np.repeat(g, bar_h, axis=0).astype("uint8"))
    bmask = Image.new("L", (box_w, bar_h), 0)
    ImageDraw.Draw(bmask).rounded_rectangle([0, 0, box_w, bar_h], bar_h // 2, fill=255)
    img.paste(bar, (m, int(y)), bmask)
    d = ImageDraw.Draw(img)

    bf = R.font(R.F_BOLD, 52)
    label = "Search CoupleIn  ·  free on both stores"
    lw = d.textlength(label, font=bf)
    if lw > box_w - 60:
        bf = R.font(R.F_BOLD, 44)
        lw = d.textlength(label, font=bf)
    d.text((m + (box_w - lw) / 2, y + (bar_h - bf.size) / 2 - 6),
           label, font=bf, fill=(255, 255, 255))
    return img


ORDER = [("P043", "calendar"), ("P046", "calendar"), ("P051", "calendar"),
         ("P064", "calendar"), ("P073", "points"), ("P079", "points"),
         ("P094", "points"), ("P103", "resolve"), ("P107", "resolve"),
         ("P124", "resolve")]
CLOSER = "7 days. Uninstall if nothing changes."
for pid, feat in ORDER:
    tt_end(CLOSER, feat).convert("RGB").save(
        f"{OUT}/{pid}_tt_4b.jpg", "JPEG", quality=92, optimize=True)
print("rendered", len(ORDER))
