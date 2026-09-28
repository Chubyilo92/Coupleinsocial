#!/usr/bin/env python3
"""CoupleIn carousel renderer — 4-slide 'viral cut' format.
Outputs Instagram 1080x1350 (4:5) and TikTok 1080x1920 (9:16)."""

import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

GF = "/usr/share/fonts/truetype/google-fonts/"
F_BOLD = GF + "Poppins-Bold.ttf"
F_MED = GF + "Poppins-Medium.ttf"
F_REG = GF + "Poppins-Regular.ttf"

# --- CoupleIn brand ---
PINK = (255, 107, 157)       # #FF6B9D
ORANGE = (255, 169, 77)      # gradient partner
INK = (13, 8, 12)            # near-black
CREAM = (255, 245, 249)
LIGHT_BG = (255, 245, 248)
LIGHT_INK = (26, 20, 22)
MUTED = (138, 120, 128)

SIZES = {"ig": (1080, 1350), "tt": (1080, 1920)}
SHOTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "shots")

# per-feature crop of the 1290x2796 source screenshots (top, bottom)
CROPS = {
    "mood": (820, 2180),
    "points": (930, 2180),
    "resolve": (1150, 2520),
    "calendar": (330, 1700),
}


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_block(draw, blocks, max_w, start_size, min_size, font_path):
    size = start_size
    while size > min_size:
        fnt = font(font_path, size)
        if all(len(wrap(draw, t, fnt, max_w)) <= n for t, n in blocks):
            return fnt
        size -= 4
    return font(font_path, min_size)


def add_glow(img, cx, cy, radius, colour, strength):
    layer = Image.new("RGB", img.size, (0, 0, 0))
    ImageDraw.Draw(layer).ellipse(
        [cx - radius, cy - radius, cx + radius, cy + radius],
        fill=tuple(int(c * strength / 255) for c in colour))
    layer = layer.filter(ImageFilter.GaussianBlur(radius * 0.55))
    arr = np.clip(np.asarray(img, int) + np.asarray(layer, int), 0, 255)
    return Image.fromarray(arr.astype("uint8"))


def new_canvas(fmt, dark=True):
    w, h = SIZES[fmt]
    img = Image.new("RGB", (w, h), INK if dark else LIGHT_BG)
    if dark:
        img = add_glow(img, w * 0.92, h * 0.10, int(w * 0.52), PINK, 62)
        img = add_glow(img, w * -0.02, h * 0.95, int(w * 0.44), ORANGE, 30)
    return img


def wordmark(img, fmt, dark=True):
    """Small CoupleIn lock-up at the foot of the slide."""
    d = ImageDraw.Draw(img)
    w, h = SIZES[fmt]
    _, b, m = safe_box(fmt)
    f = font(F_BOLD, 34)
    d.text((m, b + 26), "CoupleIn", font=f, fill=PINK)
    d.text((m + d.textlength("CoupleIn", font=f) + 18, b + 28),
           "free on iOS & Android", font=font(F_REG, 30),
           fill=(120, 96, 108) if dark else MUTED)
    return img


def safe_box(fmt):
    w, h = SIZES[fmt]
    margin = 96
    if fmt == "ig":
        return 210, h - 190, margin      # inside the 1:1 grid crop
    return 340, h - 500, margin          # clear of TikTok's caption UI


def draw_lines(d, lines, fnt, x, y, fill, leading=1.18):
    lh = int(fnt.size * leading)
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def accent_bar(d, x, y):
    d.rounded_rectangle([x, y, x + 96, y + 14], 7, fill=PINK)


def slide_hook(fmt, top_text, payoff):
    img = new_canvas(fmt, dark=True)
    d = ImageDraw.Draw(img)
    w, h = SIZES[fmt]
    t, b, m = safe_box(fmt)
    box_w = w - m * 2

    fnt = fit_block(d, [(top_text, 2), (payoff, 2)], box_w, 120, 70, F_BOLD)
    l1, l2 = wrap(d, top_text, fnt, box_w), wrap(d, payoff, fnt, box_w)
    lh, gap = int(fnt.size * 1.14), int(fnt.size * 0.52)
    total = (len(l1) + len(l2)) * lh + gap
    y = t + ((b - t) - total) / 2

    y = draw_lines(d, l1, fnt, m, y, CREAM, 1.14)
    y += gap
    draw_lines(d, l2, fnt, m, y, PINK, 1.14)
    return img


def slide_line(fmt, line_a, line_b=None):
    img = new_canvas(fmt, dark=False)
    d = ImageDraw.Draw(img)
    w, h = SIZES[fmt]
    t, b, m = safe_box(fmt)
    box_w = w - m * 2

    blocks = [(line_a, 2)] + ([(line_b, 2)] if line_b else [])
    fnt = fit_block(d, blocks, box_w, 106, 62, F_BOLD)
    l1 = wrap(d, line_a, fnt, box_w)
    l2 = wrap(d, line_b, fnt, box_w) if line_b else []
    lh = int(fnt.size * 1.18)
    gap = int(fnt.size * 0.48) if l2 else 0
    total = (len(l1) + len(l2)) * lh + gap
    y = t + ((b - t) - total) / 2

    accent_bar(d, m, y - 74)
    y = draw_lines(d, l1, fnt, m, y, LIGHT_INK, 1.18)
    if l2:
        y += gap
        draw_lines(d, l2, fnt, m, y, MUTED, 1.18)
    return img


def slide_cta(fmt, line_a, line_b, keyword):
    img = new_canvas(fmt, dark=False)
    d = ImageDraw.Draw(img)
    w, h = SIZES[fmt]
    t, b, m = safe_box(fmt)
    box_w = w - m * 2

    fnt = fit_block(d, [(line_a, 2), (line_b, 2)], box_w, 100, 60, F_BOLD)
    l1, l2 = wrap(d, line_a, fnt, box_w), wrap(d, line_b, fnt, box_w)
    lh, gap = int(fnt.size * 1.18), int(fnt.size * 0.48)

    cf = font(F_BOLD, 54)
    label = f'Comment  "{keyword}"'
    chip_w = d.textlength(label, font=cf) + 100
    chip_h = 116

    total = (len(l1) + len(l2)) * lh + gap + 96 + chip_h + 66
    y = t + ((b - t) - total) / 2

    accent_bar(d, m, y - 74)
    y = draw_lines(d, l1, fnt, m, y, LIGHT_INK, 1.18)
    y += gap
    y = draw_lines(d, l2, fnt, m, y, MUTED, 1.18)
    y += 96

    # gradient pill, matching the app's button
    grad = Image.new("RGB", (int(chip_w), chip_h))
    gx = np.linspace(0, 1, int(chip_w))[None, :, None]
    grad_arr = (np.array(PINK)[None, None, :] * (1 - gx)
                + np.array(ORANGE)[None, None, :] * gx)
    grad = Image.fromarray(np.repeat(grad_arr, chip_h, axis=0).astype("uint8"))
    mask = Image.new("L", (int(chip_w), chip_h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, chip_w, chip_h], chip_h // 2, fill=255)
    img.paste(grad, (m, int(y)), mask)
    d.text((m + 50, y + 26), label, font=cf, fill=(255, 255, 255))

    d.text((m, y + chip_h + 30), "and it lands in your DMs",
           font=font(F_REG, 34), fill=MUTED)
    return img


def slide_poll(fmt, line_a, line_b, opt1, opt2):
    """Engagement slide — light, with a two-option comment poll."""
    img = new_canvas(fmt, dark=False)
    d = ImageDraw.Draw(img)
    w, h = SIZES[fmt]
    t, b, m = safe_box(fmt)
    box_w = w - m * 2

    fnt = fit_block(d, [(line_a, 2), (line_b, 2)], box_w, 96, 58, F_BOLD)
    l1, l2 = wrap(d, line_a, fnt, box_w), wrap(d, line_b, fnt, box_w)
    lh, gap = int(fnt.size * 1.18), int(fnt.size * 0.46)

    of = font(F_BOLD, 50)
    nf = font(F_BOLD, 50)
    row_h, row_gap = 116, 22
    poll_h = row_h * 2 + row_gap + 74

    total = (len(l1) + len(l2)) * lh + gap + 86 + poll_h
    y = t + ((b - t) - total) / 2

    accent_bar(d, m, y - 74)
    y = draw_lines(d, l1, fnt, m, y, LIGHT_INK, 1.18)
    y += gap
    y = draw_lines(d, l2, fnt, m, y, MUTED, 1.18)
    y += 86

    for n, (label, filled) in enumerate([(opt1, True), (opt2, False)], start=1):
        ry = y + (n - 1) * (row_h + row_gap)
        if filled:
            grad_w = box_w
            gx = np.linspace(0, 1, grad_w)[None, :, None]
            arr = (np.array(PINK)[None, None, :] * (1 - gx)
                   + np.array(ORANGE)[None, None, :] * gx)
            tile = Image.fromarray(np.repeat(arr, row_h, axis=0).astype("uint8"))
            mask = Image.new("L", (grad_w, row_h), 0)
            ImageDraw.Draw(mask).rounded_rectangle(
                [0, 0, grad_w, row_h], row_h // 2, fill=255)
            img.paste(tile, (m, int(ry)), mask)
            d = ImageDraw.Draw(img)
            num_col, txt_col = (255, 255, 255), (255, 255, 255)
        else:
            d.rounded_rectangle([m, ry, m + box_w, ry + row_h], row_h // 2,
                                outline=PINK, width=4)
            num_col, txt_col = PINK, LIGHT_INK
        d.text((m + 48, ry + 30), str(n), font=nf, fill=num_col)
        d.text((m + 108, ry + 30), label, font=of, fill=txt_col)

    d.text((m, y + row_h * 2 + row_gap + 30), "Comment your number.",
           font=font(F_REG, 36), fill=MUTED)
    return img


def load_shot(feature):
    path = os.path.join(SHOTS, feature + ".png")
    if not os.path.exists(path):
        return None
    im = Image.open(path).convert("RGB")
    top, bot = CROPS.get(feature, (0, im.height))
    return im.crop((0, top, im.width, min(bot, im.height)))


def slide_proof(fmt, payoff, closer, feature):
    img = new_canvas(fmt, dark=True)
    d = ImageDraw.Draw(img)
    w, h = SIZES[fmt]
    t, b, m = safe_box(fmt)
    box_w = w - m * 2

    pf = font(F_BOLD, 82)
    plines = wrap(d, payoff, pf, box_w)
    cf = font(F_MED, 38)
    clines = wrap(d, closer, cf, box_w)
    head_h = len(plines) * int(pf.size * 1.14)
    foot_h = len(clines) * int(cf.size * 1.3)

    shot = load_shot(feature)
    card_w = w - m * 2
    avail = (b - t) - head_h - foot_h - 150

    if shot:
        card_h = int(card_w * shot.height / shot.width)
        if card_h > avail:
            # scale the whole card down rather than crop the anchor away
            card_h = int(avail)
            card_w = int(card_h * shot.width / shot.height)
        shot = shot.resize((card_w, card_h))
        mask = Image.new("L", (card_w, card_h), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, card_w, card_h], 44, fill=255)
    else:
        card_h = int(avail)

    cx = int((w - card_w) / 2)
    y = t + ((b - t) - (head_h + 60 + card_h + 60 + foot_h)) / 2
    y = draw_lines(d, plines, pf, m, y, CREAM, 1.14)
    y += 60

    if shot:
        img.paste(shot, (cx, int(y)), mask)
        ImageDraw.Draw(img).rounded_rectangle(
            [cx, int(y), cx + card_w, int(y) + card_h], 44,
            outline=(255, 107, 157), width=3)
    else:
        d.rounded_rectangle([cx, y, cx + card_w, y + card_h], 44,
                            outline=(120, 70, 92), width=4)
    y += card_h + 60
    d = ImageDraw.Draw(img)
    draw_lines(d, clines, cf, m, y, PINK, 1.3)
    return img


def build(post_id, slides, outdir):
    os.makedirs(outdir, exist_ok=True)
    made = []
    for fmt in ("ig", "tt"):
        for i, s in enumerate(slides, start=1):
            kind = s[0]
            if kind == "hook":
                img = slide_hook(fmt, s[1], s[2])
            elif kind == "line":
                img = slide_line(fmt, s[1], s[2] if len(s) > 2 else None)
            elif kind == "cta":
                img = slide_cta(fmt, s[1], s[2], s[3])
            elif kind == "poll":
                img = slide_poll(fmt, s[1], s[2], s[3], s[4])
            elif kind == "proof":
                img = slide_proof(fmt, s[1], s[2], s[3])
            img = wordmark(img, fmt, dark=kind in ("hook", "proof"))
            # TikTok rejects image/png on photo posts — JPEG or WebP only.
            if fmt == "tt":
                path = os.path.join(outdir, f"{post_id}_{fmt}_{i}.jpg")
                img.convert("RGB").save(path, "JPEG", quality=92, optimize=True)
            else:
                path = os.path.join(outdir, f"{post_id}_{fmt}_{i}.png")
                img.save(path, "PNG")
            made.append(path)
    return made


if __name__ == "__main__":
    slides = [
        ("hook", "He'd die for you.", "Would he improve for you?"),
        ("line", "Dying is a moment.", "Improving is a Tuesday."),
        ("cta", "He's not refusing.", "He doesn't know how.", "BETTER"),
        ("proof", "Now he knows.", "7 days. Uninstall if nothing changes.", "mood"),
    ]
    out = build("P043", slides, os.path.join(os.path.dirname(
        os.path.abspath(__file__)), "P043"))
    print("\n".join(out))
