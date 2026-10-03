#!/usr/bin/env python3
"""Re-render the October TikTok black carousels (v2, 3 Oct 2026).

Why: the v1 posts plateaued at ~700 views with 0 comments and 0 shares, then
dropped to 41 and 0. v1 had an identical black cover every day and a
"1 or 2 / comment your number" poll on slide 3 that nobody answered.

v2 changes, modelled on what top faceless relationship slideshows do:
  - covers rotate through 5 looks so consecutive posts never match:
    three glow variants, a light cover, and a text-message cover
  - slide 3 is a SHARE slide: release lines + "Send this to him" pill
    (sends are the strongest signal for photo posts; matches the captions)
  - slide 4 is the standard TikTok end slide (full screenshot + CTA)

Run:  python3 render_oct_v2.py   ->  ../October_v2/V2_<slot>_tt_<n>.jpg
"""

import os
from PIL import Image, ImageDraw
import render as R
from render_edgy_test import cover as glow_cover, share_slide, tt_end, pill
from oct_v2_data import ROWS

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "October_v2")
FMT = "tt"
W, H = R.SIZES[FMT]

COVER_CYCLE = ["a", "light", "text", "b", "c"]
SEND = ["Send this to {x}. Say nothing.", "Send this to {x}.",
        "Send this to {x}. Don't explain.", "Send this to {x}. No context."]

IOS_BG = (242, 242, 247)
GREY_BUBBLE = (229, 229, 234)


def split2(text):
    """'A. B.' -> ('A.', 'B.'); single sentence -> (text, None)."""
    i = text.find(". ")
    if i == -1:
        return text, None
    return text[: i + 1], text[i + 2:]


def light_cover(top, payoff):
    img = Image.new("RGB", (W, H), R.LIGHT_BG)
    img = R.add_glow(img, W * 0.95, H * 0.05, int(W * 0.45), (0, 0, 0), 0)
    d = ImageDraw.Draw(img)
    t, b, m = R.safe_box(FMT)
    box_w = W - m * 2
    fnt = R.fit_block(d, [(top, 2), (payoff, 2)], box_w, 120, 70, R.F_BOLD)
    l1, l2 = R.wrap(d, top, fnt, box_w), R.wrap(d, payoff, fnt, box_w)
    lh, gap = int(fnt.size * 1.14), int(fnt.size * 0.52)
    y = t + ((b - t) - ((len(l1) + len(l2)) * lh + gap)) / 2
    R.accent_bar(d, m, y - 74)
    y = R.draw_lines(d, l1, fnt, m, y, R.LIGHT_INK, 1.14) + gap
    R.draw_lines(d, l2, fnt, m, y, R.PINK, 1.14)
    return img


def bubble(d, img, text, fnt, max_w, y, right, fill, ink):
    lines = R.wrap(d, text, fnt, max_w - 80)
    lh = int(fnt.size * 1.22)
    bw = int(max(d.textlength(l, font=fnt) for l in lines)) + 80
    bh = lh * len(lines) + 56
    x = W - 70 - bw if right else 70
    d.rounded_rectangle([x, y, x + bw, y + bh], 48, fill=fill)
    ty = y + 24
    for l in lines:
        d.text((x + 40, ty), l, font=fnt, fill=ink)
        ty += lh
    return y + bh


def text_cover(top, payoff):
    """iMessage-style: the claim arrives grey, the undercut goes back pink."""
    img = Image.new("RGB", (W, H), IOS_BG)
    d = ImageDraw.Draw(img)
    t, b, _ = R.safe_box(FMT)
    max_w = int(W * 0.80)
    fnt = R.fit_block(d, [(top, 3), (payoff, 3)], max_w - 80, 78, 54, R.F_MED)
    lh = int(fnt.size * 1.22)
    h1 = lh * len(R.wrap(d, top, fnt, max_w - 80)) + 56
    h2 = lh * len(R.wrap(d, payoff, fnt, max_w - 80)) + 56
    sf = R.font(R.F_REG, 30)
    total = 50 + h1 + 30 + h2 + 50
    y = t + ((b - t) - total) / 2
    stamp = "Today 21:47"
    d.text(((W - d.textlength(stamp, font=sf)) / 2, y), stamp, font=sf,
           fill=(142, 142, 147))
    y += 70
    y = bubble(d, img, top, fnt, max_w, y, False, GREY_BUBBLE, (0, 0, 0)) + 30
    y = bubble(d, img, payoff, fnt, max_w, y, True, R.PINK, (255, 255, 255))
    d.text((W - 70 - d.textlength("Read", font=sf), y + 10), "Read",
           font=sf, fill=(142, 142, 147))
    return img


def sharpen_slide(a, b):
    """Light slide; up to 3 lines per block so one-sentence lines stay big."""
    img = R.new_canvas(FMT, dark=False)
    d = ImageDraw.Draw(img)
    t, bt, m = R.safe_box(FMT)
    box_w = W - m * 2
    blocks = [(a, 3)] + ([(b, 3)] if b else [])
    fnt = R.fit_block(d, blocks, box_w, 100, 64, R.F_BOLD)
    l1 = R.wrap(d, a, fnt, box_w)
    l2 = R.wrap(d, b, fnt, box_w) if b else []
    lh = int(fnt.size * 1.18)
    gap = int(fnt.size * 0.48) if l2 else 0
    y = t + ((bt - t) - ((len(l1) + len(l2)) * lh + gap)) / 2
    R.accent_bar(d, m, y - 74)
    y = R.draw_lines(d, l1, fnt, m, y, R.LIGHT_INK, 1.18)
    if l2:
        R.draw_lines(d, l2, fnt, m, y + gap, R.MUTED, 1.18)
    return img


def make_cover(kind, top, payoff):
    if kind == "light":
        return light_cover(top, payoff), False
    if kind == "text":
        return text_cover(top, payoff), False
    return glow_cover(kind, top, payoff), True


def main(only=None):
    os.makedirs(OUT, exist_ok=True)
    made = []
    for i, (slot, _id, _uuid, who, feat, ha, hb, sharpen, release) in enumerate(ROWS):
        if only and slot not in only:
            continue
        x = "him" if who == "he" else "her"
        cov, cov_dark = make_cover(COVER_CYCLE[i % len(COVER_CYCLE)], ha, hb)
        s2a, s2b = split2(sharpen)
        r1, r2 = split2(release)
        slides = [
            (cov, cov_dark),
            (sharpen_slide(s2a, s2b), False),
            (share_slide(r1, r2 or "", SEND[i % len(SEND)].format(x=x)), False),
            (tt_end(feat), None),
        ]
        for n, (img, dark) in enumerate(slides, start=1):
            if dark is not None:
                img = R.wordmark(img, FMT, dark=dark)
            p = os.path.join(OUT, f"V2_{slot}_tt_{n}.jpg")
            img.convert("RGB").save(p, "JPEG", quality=92, optimize=True)
            made.append(p)
    print(len(made), "images ->", OUT)
    return made


if __name__ == "__main__":
    import sys
    main(sys.argv[1:] or None)
