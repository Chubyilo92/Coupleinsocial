#!/usr/bin/env python3
"""Instagram end slide, re-cropped so the part that shows the value is
always fully in frame: prompt+timer+button, wishlist items with their
buttons, calendar header with real events."""

import os
from PIL import Image, ImageDraw
import numpy as np
import render as R

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "ig_end")
os.makedirs(OUT, exist_ok=True)
SHOTS = os.path.join(HERE, "shots")
W, H = 1080, 1350

# source is 1290x2796. These crops contain the whole payoff and nothing dead.
VALUE_CROPS = {
    "resolve":  (1430, 2570),   # "Reflect back" through Next step, no clipped text
    "points":   (1050, 2150),   # two wishlist items incl. both "I did this" buttons
    "calendar": (340, 1610),    # coral header + Upcoming Events + two whole events
}


def ig_end(payoff, closer, feature):
    img = R.new_canvas("ig", dark=True)
    d = ImageDraw.Draw(img)
    m = 96
    box_w = W - m * 2
    t, b = 210, 1160

    shot = Image.open(os.path.join(SHOTS, feature + ".png")).convert("RGB")
    top, bot = VALUE_CROPS[feature]
    shot = shot.crop((0, top, shot.width, min(bot, shot.height)))

    pf = R.font(R.F_BOLD, 76)
    plines = R.wrap(d, payoff, pf, box_w)
    cf = R.font(R.F_MED, 38)
    head_h = len(plines) * int(pf.size * 1.14)
    foot_h = int(cf.size * 1.3)

    avail = (b - t) - head_h - foot_h - 90
    card_w = box_w
    card_h = int(card_w * shot.height / shot.width)
    if card_h > avail:
        card_h = int(avail)
        card_w = int(card_h * shot.width / shot.height)
    shot = shot.resize((card_w, card_h))
    mask = Image.new("L", (card_w, card_h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, card_w, card_h], 36, fill=255)

    total = head_h + 45 + card_h + 45 + foot_h
    y = t + ((b - t) - total) / 2
    y = R.draw_lines(d, plines, pf, m, y, R.CREAM, 1.14)
    y += 45
    cx = int((W - card_w) / 2)
    img.paste(shot, (cx, int(y)), mask)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([cx, int(y), cx + card_w, int(y) + card_h], 36,
                        outline=R.PINK, width=3)
    y += card_h + 45
    d.text((m, y), closer, font=cf, fill=R.PINK)
    return R.wordmark(img, "ig", dark=True)


ORDER = [("P043", "calendar", "Now it's in his week."),
         ("P046", "calendar", "Now it's in his week."),
         ("P051", "calendar", "He gets the nudge. Not you."),
         ("P064", "calendar", "Now it's in her week."),
         ("P073", "points", "Now he knows what counts."),
         ("P079", "points", "You list it. He does it."),
         ("P094", "points", "Now you know what counts."),
         ("P103", "resolve", "Seven steps. One timer."),
         ("P107", "resolve", "He knows what to say next."),
         ("P124", "resolve", "You both know what's next.")]
CLOSER = "7 days. Uninstall if nothing changes."
for pid, feat, payoff in ORDER:
    ig_end(payoff, CLOSER, feat).save(f"{OUT}/{pid}_ig_4b.png", "PNG")
print("rendered", len(ORDER))
