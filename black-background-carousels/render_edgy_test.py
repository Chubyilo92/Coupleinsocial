#!/usr/bin/env python3
"""Edgy test batch (E001-E003), TikTok 9:16 only.

Differences from the standard Black Background carousel:
  - slide 3 is a SHARE slide (release lines + "Send this to him" pill)
    instead of the 1-or-2 comment poll, which produced zero comments
  - each post gets a different cover glow, so consecutive posts
    don't look identical in the feed
  - slide 4 is the standard TikTok end slide (full screenshot + CTA pill)
Run:  python3 render_edgy_test.py   ->  edgy_test/E00x_tt_n.jpg
"""

import os
import numpy as np
from PIL import Image, ImageDraw
import render as R

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "edgy_test")
FMT = "tt"
W, H = R.SIZES[FMT]
CLOSER = "7 days. Uninstall if nothing changes."

# cover variants: (glow1 x, y, colour, strength), (glow2 ...), payoff colour
COVERS = {
    "a": (((0.92, 0.10), R.PINK, 62), ((-0.02, 0.95), R.ORANGE, 30), R.PINK),
    "b": (((0.05, 0.08), R.ORANGE, 58), ((1.0, 0.92), R.PINK, 52), R.ORANGE),
    "c": (((0.50, -0.05), R.PINK, 70), ((0.50, 1.05), R.PINK, 34), R.PINK),
}

POSTS = [
    ("E001", "a", "calendar",
     ('"Tell me what to do."', "The laziest sentence a man says."),
     ("He runs a team of 12 at work.", "At home he needs a list?"),
     ("He's not lazy.", "Nobody made it visible.", "Send this to him. Say nothing.")),
    ("E002", "b", "calendar",
     ("He remembers his fantasy draft.", "Not your anniversary."),
     ("Three reminders for kick-off.", "Zero for your birthday dinner."),
     ("He's not careless.", "His phone reminds him. You don't.",
      "Send this to him. Don't explain.")),
    ("E003", "c", "calendar",
     ("You split the bill 50/50.", "She does 80% of the thinking."),
     ("Birthdays. Bins. Dentist.", "His mum's present."),
     ("He'd do it.", "He's never seen the list.",
      "Send this to whoever's carrying it.")),
]


def cover(variant, top_text, payoff):
    g1, g2, pay_col = COVERS[variant]
    img = Image.new("RGB", (W, H), R.INK)
    for (fx, fy), col, s in (g1, g2):
        img = R.add_glow(img, W * fx, H * fy, int(W * 0.52), col, s)
    d = ImageDraw.Draw(img)
    t, b, m = R.safe_box(FMT)
    box_w = W - m * 2
    fnt = R.fit_block(d, [(top_text, 2), (payoff, 2)], box_w, 120, 70, R.F_BOLD)
    l1, l2 = R.wrap(d, top_text, fnt, box_w), R.wrap(d, payoff, fnt, box_w)
    lh, gap = int(fnt.size * 1.14), int(fnt.size * 0.52)
    y = t + ((b - t) - ((len(l1) + len(l2)) * lh + gap)) / 2
    y = R.draw_lines(d, l1, fnt, m, y, R.CREAM, 1.14) + gap
    R.draw_lines(d, l2, fnt, m, y, pay_col, 1.14)
    return img


def pill(img, x, y, w, h, label, size=50):
    gx = np.linspace(0, 1, w)[None, :, None]
    g = np.array(R.PINK)[None, None, :] * (1 - gx) + np.array(R.ORANGE)[None, None, :] * gx
    bar = Image.fromarray(np.repeat(g, h, axis=0).astype("uint8"))
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, w, h], h // 2, fill=255)
    img.paste(bar, (x, int(y)), mask)
    d = ImageDraw.Draw(img)
    f = R.font(R.F_BOLD, size)
    while d.textlength(label, font=f) > w - 70 and size > 34:
        size -= 2
        f = R.font(R.F_BOLD, size)
    lw = d.textlength(label, font=f)
    d.text((x + (w - lw) / 2, y + (h - size) / 2 - 6), label, font=f, fill=(255, 255, 255))


def share_slide(line_a, line_b, prompt):
    img = R.new_canvas(FMT, dark=False)
    d = ImageDraw.Draw(img)
    t, b, m = R.safe_box(FMT)
    box_w = W - m * 2
    fnt = R.fit_block(d, [(line_a, 2), (line_b, 2)], box_w, 100, 60, R.F_BOLD)
    l1, l2 = R.wrap(d, line_a, fnt, box_w), R.wrap(d, line_b, fnt, box_w)
    lh, gap, ph = int(fnt.size * 1.18), int(fnt.size * 0.48), 124
    total = (len(l1) + len(l2)) * lh + gap + 96 + ph
    y = t + ((b - t) - total) / 2
    R.accent_bar(d, m, y - 74)
    y = R.draw_lines(d, l1, fnt, m, y, R.LIGHT_INK, 1.18) + gap
    y = R.draw_lines(d, l2, fnt, m, y, R.MUTED, 1.18) + 96
    pill(img, m, y, box_w, ph, prompt)
    return img


def tt_end(feature):
    """Same as render_tt_end.tt_end (copied: that module renders on import)."""
    img = Image.new("RGB", (W, H), R.INK)
    shot = Image.open(os.path.join(HERE, "shots", feature + ".png")).convert("RGB")
    m, sh = 96, 1430
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
    d.text(((W - d.textlength(CLOSER, font=cf)) / 2, y), CLOSER, font=cf, fill=R.PINK)
    pill(img, m, y + 66, W - m * 2, 126, "Search CoupleIn  ·  free on both stores", 52)
    return img


def main():
    os.makedirs(OUT, exist_ok=True)
    for pid, var, feat, hook, sharpen, release in POSTS:
        slides = [
            (cover(var, *hook), True),
            (R.slide_line(FMT, *sharpen), False),
            (share_slide(*release), False),
            (tt_end(feat), None),
        ]
        for i, (img, dark) in enumerate(slides, start=1):
            if dark is not None:
                img = R.wordmark(img, FMT, dark=dark)
            p = os.path.join(OUT, f"{pid}_tt_{i}.jpg")
            img.convert("RGB").save(p, "JPEG", quality=92, optimize=True)
            print(p)


if __name__ == "__main__":
    main()
