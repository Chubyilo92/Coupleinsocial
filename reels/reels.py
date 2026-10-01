"""Programmatic IG/FB reels (1080x1920, 30fps) for CoupleIn: new experimental formats.
Formats: flags (red/green flag), translate (what they say / mean), tier (tier list), board (scoreboard), quiz (via quiz renderer).
Usage: python3 reels.py specs/<name>.json out.mp4
Reuses fonts/helpers from the quiz renderer. No stock footage needed. Safe zone: keep key content between y=240 and y=1560.
"""
import os, sys, json, math, subprocess, importlib.util
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
RV = os.path.join(HERE, "..", "you-owe-me-quiz-videos (1)", "you-owe-me-quiz-videos", "render", "render_video.py")
spec = importlib.util.spec_from_file_location("rv", RV); rv = importlib.util.module_from_spec(spec); spec.loader.exec_module(rv)
BED = os.path.join(HERE, "..", "you-owe-me-quiz-videos (1)", "you-owe-me-quiz-videos", "assets", "music_bed.wav")
W, H, FPS = 1080, 1920, 30
INK, WHITE, YELLOW, RED, PINK = rv.INK, rv.WHITE, rv.YELLOW, rv.RED, rv.PINK
GREEN = (34, 197, 94); BLUE = (58, 134, 255); PURPLE = (131, 56, 236); GREY = (150, 150, 150)
ease, back, block, boxed, font, FB, FM = rv.ease, rv.back, rv.block, rv.boxed, rv.font, rv.FB, rv.FM

# balanced line wrap (no one-word last lines)
_g = rv.wrap
def _bal(d, text, f, maxw):
    ls = _g(d, text, f, maxw)
    if len(ls) < 2: return ls
    lo, hi = 50, maxw
    while hi - lo > 4:
        mid = (lo + hi) / 2
        if len(_g(d, text, f, mid)) <= len(ls) and all(d.textlength(w, font=f) <= mid for w in text.split()): hi = mid
        else: lo = mid
    return _g(d, text, f, hi)
rv.wrap = _bal

def emo(img, ch, cx, top, size): rv.paste_emoji(img, ch, cx, top, size)
def bar(img, frac, y=180, col=YELLOW):
    d = ImageDraw.Draw(img); d.rounded_rectangle((90, y, 990, y + 22), radius=11, fill=(60, 60, 60))
    if frac > 0: d.rounded_rectangle((90, y, 90 + 900 * min(1, frac), y + 22), radius=11, fill=col)
def end_card(t, big, sub, tag, extra=None):
    img = Image.new("RGB", (W, H), PINK); p = back(t / 0.35)
    y = block(img, big, W / 2, 520, 104 * (0.85 + 0.15 * p), WHITE, maxlines=3)
    if t > 0.7: block(img, sub, W / 2, y + 120, 60, INK, path=FM, maxlines=2, maxw=900)
    if extra and t > 1.3: block(img, extra, W / 2, 1050, 52, WHITE, path=FM, maxlines=3, maxw=900)
    if t > 2.0:
        s = 1.6 - 0.6 * back((t - 2.0) / 0.3); boxed(img, tag, W / 2, 1330, 62, WHITE, (230, 40, 110), scale=s)
    if t > 2.6: block(img, "CoupleIn. Free on iOS & Android.", W / 2, 1480, 38, WHITE, path=FM, maxlines=1)
    return img

# ---------------- FLAGS ----------------
def flags(t, S):
    items = S["items"]; HOOK, IT, END = 3.2, 4.6, 5.0; n = len(items)
    if t < HOOK:
        img = Image.new("RGB", (W, H), INK); p = back(t / 0.4)
        block(img, "RED FLAG", W / 2, 620, 150 * (0.8 + 0.2 * p), RED, maxlines=1)
        if t > 0.5: block(img, "or", W / 2, 820, 80, WHITE, path=FM, maxlines=1)
        if t > 0.8: block(img, "GREEN FLAG", W / 2, 1020, 150 * (0.8 + 0.2 * back((t - 0.8) / 0.4)), GREEN, maxlines=1)
        if t > 2.0: boxed(img, S.get("hook", "No 'it depends'. Be honest."), W / 2, 1330, 52, YELLOW, INK, maxw=900)
        return img
    if t >= HOOK + n * IT:
        reds = sum(1 for _, v in items if v == "red"); greens = n - reds
        return end_card(t - HOOK - n * IT, S.get("end_big", "How many red flags did you get?"),
                        f"Mine: {reds} red, {greens} green.", S.get("tag", "Tag who has the most"), S.get("end_extra"))
    k = int((t - HOOK) // IT); lt = (t - HOOK) - k * IT
    img = Image.new("RGB", (W, H), INK); d = ImageDraw.Draw(img)
    bar(img, (k + lt / IT) / n, col=YELLOW)
    stamped = lt > 3.0
    reds = sum(1 for j in range(k) if items[j][1] == "red") + (1 if stamped and items[k][1] == "red" else 0)
    greens = (k + (1 if stamped else 0)) - reds
    boxed(img, f"RED {reds}", 300, 300, 44, RED, WHITE); boxed(img, f"GREEN {greens}", 780, 300, 44, GREEN, WHITE)
    p = back(lt / 0.3); cw = 920 * (0.85 + 0.15 * p)
    d.rounded_rectangle((W / 2 - cw / 2, 520, W / 2 + cw / 2, 1180), radius=48, fill=WHITE)
    block(img, items[k][0], W / 2, 850, 84 * (0.8 + 0.2 * p), INK, maxw=780, maxlines=4)
    if not stamped:
        d.rounded_rectangle((200, 1140, 880, 1156), radius=8, fill=(225, 225, 225)); d.rounded_rectangle((200, 1140, 200 + 680 * (lt / 3.0), 1156), radius=8, fill=INK)
        block(img, "decide…", W / 2, 1330, 54, GREY, path=FM, maxlines=1)
    else:
        red = items[k][1] == "red"; q = (lt - 3.0) / 0.4; s = 1.9 - 0.9 * back(q)
        boxed(img, "RED FLAG" if red else "GREEN FLAG", W / 2, 1330, 100, RED if red else GREEN, WHITE, scale=s, angle=-6 if red else 5)
    return img

# ---------------- TRANSLATE ----------------
def translate(t, S):
    items = S["items"]; HOOK, IT, END = 3.4, 6.2, 5.0; n = len(items)
    if t < HOOK:
        img = Image.new("RGB", (W, H), INK); p = back(t / 0.4)
        block(img, S.get("title", "What they say"), W / 2, 640, 120 * (0.8 + 0.2 * p), WHITE, maxlines=2)
        if t > 0.6: block(img, "vs", W / 2, 900, 70, GREY, path=FM, maxlines=1)
        if t > 0.9: block(img, "what they mean", W / 2, 1100, 120 * (0.8 + 0.2 * back((t - 0.9) / 0.4)), PINK, maxlines=2)
        if t > 1.7: boxed(img, S.get("hook", "Translated. Tag the one who says it."), W / 2, 1420, 48, YELLOW, INK, maxw=900)
        return img
    if t >= HOOK + n * IT:
        return end_card(t - HOOK - n * IT, S.get("end_big", "Tag the one who says it"), S.get("end_sub", "Hear it before you answer."), S.get("tag", "Say it properly in CoupleIn"), S.get("end_extra"))
    k = int((t - HOOK) // IT); lt = (t - HOOK) - k * IT
    img = Image.new("RGB", (W, H), INK); d = ImageDraw.Draw(img)
    bar(img, (k + lt / IT) / n, col=PINK)
    d.text((W / 2, 290), f"{k + 1}/{n}", font=font(FB, 44), fill=YELLOW, anchor="mm")
    say, mean = items[k]
    p = ease(lt / 0.3); xo = -W * (1 - p)
    d.rounded_rectangle((90 + xo, 430, 930 + xo, 860), radius=60, fill=WHITE)
    d.polygon([(150 + xo, 850), (240 + xo, 850), (170 + xo, 930)], fill=WHITE)
    block(img, say, 510 + xo, 645, 92, INK, maxw=700, maxlines=4)
    if lt > 2.9:
        q = back((lt - 2.9) / 0.45); sc = 0.6 + 0.4 * q
        d.rounded_rectangle((W / 2 - 480 * sc, 1060, W / 2 + 480 * sc, 1060 + 420 * sc), radius=60, fill=PINK)
        block(img, "means:", W / 2, 1120, 40 * sc, (255, 220, 230), path=FM, maxlines=1)
        block(img, mean, W / 2, 1290, 78 * sc, WHITE, maxw=820, maxlines=4)
    return img

# ---------------- TIER ----------------
TIER_COL = {"S": RED, "A": (255, 140, 0), "B": YELLOW, "C": GREEN, "D": BLUE}
def tier_layout(S):
    rows = {r: [] for r in "SABCD"}; pos = {}
    for i, (txt, r) in enumerate(S["items"]):
        f = font(FB, 34); w = ImageDraw.Draw(Image.new("RGB", (4, 4))).textlength(txt, font=f) + 36
        rows[r].append((i, txt, w))
    for r, lst in rows.items():
        x = 0; y = 0
        for i, txt, w in lst:
            if x + w > 740: x = 0; y += 56
            pos[i] = (x, y, w); x += w + 10
    return pos
def tier(t, S):
    items = S["items"]; HOOK, IT, END = 3.2, 3.4, 5.0; n = len(items); pos = tier_layout(S)
    if t < HOOK:
        img = Image.new("RGB", (W, H), INK); p = back(t / 0.4)
        block(img, S.get("title", "TIER LIST"), W / 2, 640, 130 * (0.8 + 0.2 * p), WHITE, maxlines=2)
        if t > 0.7: boxed(img, S.get("sub", "S = unforgivable"), W / 2, 1000, 62, RED, WHITE)
        if t > 1.5: block(img, S.get("hook", "Fight me in the comments."), W / 2, 1250, 56, YELLOW, path=FM, maxlines=2)
        return img
    if t >= HOOK + n * IT:
        return end_card(t - HOOK - n * IT, S.get("end_big", "Fight me. Rank your own."), S.get("end_sub", "Comment your S tier."), S.get("tag", "Tag who disagrees"), S.get("end_extra"))
    k = int((t - HOOK) // IT); lt = (t - HOOK) - k * IT
    img = Image.new("RGB", (W, H), INK); d = ImageDraw.Draw(img)
    boxed(img, S.get("title_small", "TIER LIST"), W / 2, 230, 40, YELLOW, INK)
    y0 = 330; rh = 188
    for ri, r in enumerate("SABCD"):
        y = y0 + ri * rh
        d.rounded_rectangle((60, y, 1020, y + rh - 14), radius=22, fill=(38, 38, 38))
        d.rounded_rectangle((60, y, 200, y + rh - 14), radius=22, fill=TIER_COL[r])
        d.text((130, y + (rh - 14) / 2), r, font=font(FB, 90), fill=INK, anchor="mm")
    def place(i, x_override=None):
        txt, r = items[i]; ri = "SABCD".index(r); x, yy, w = pos[i]
        return 220 + x, y0 + ri * rh + 12 + yy, w
    for i in range(k):
        x, yy, w = place(i); d.rounded_rectangle((x, yy, x + w, yy + 48), radius=24, fill=WHITE)
        d.text((x + w / 2, yy + 25), items[i][0], font=font(FB, 34), fill=INK, anchor="mm")
    # current item: shows big in the middle, then flies into its row
    txt, r = items[k]; x, yy, w = place(k)
    if lt < 2.0:
        p = back(lt / 0.3); block(img, txt, W / 2, 1480, 76 * (0.7 + 0.3 * p), WHITE, maxw=900, maxlines=2)
        block(img, "where does it go?", W / 2, 1600, 38, GREY, path=FM, maxlines=1)
    else:
        q = ease((lt - 2.0) / 0.8); cx = W / 2 + (x + w / 2 - W / 2) * q; cy = 1480 + (yy + 24 - 1480) * q
        fs = 76 + (34 - 76) * q
        ww = d.textlength(txt, font=font(FB, fs)) + 36 * q + 40 * (1 - q)
        d.rounded_rectangle((cx - ww / 2, cy - fs * 0.8, cx + ww / 2, cy + fs * 0.8), radius=24 + 30 * (1 - q), fill=WHITE)
        d.text((cx, cy + 2), txt, font=font(FB, fs), fill=INK, anchor="mm")
    return img

# ---------------- BOARD ----------------
def board(t, S):
    cats = S["cats"]; HOOK, IT, END = 3.2, 5.0, 5.0; n = len(cats)
    ty = sum(c[1] for c in cats); tt = sum(c[2] for c in cats)
    if t < HOOK:
        img = Image.new("RGB", (W, H), INK); p = back(t / 0.4)
        block(img, S.get("title", "The household scoreboard"), W / 2, 640, 112 * (0.8 + 0.2 * p), WHITE, maxlines=3)
        if t > 0.8: boxed(img, S.get("sub", "Who really does more?"), W / 2, 1000, 62, YELLOW, INK)
        if t > 1.5: block(img, S.get("hook", "Receipts only."), W / 2, 1250, 56, PINK, path=FM, maxlines=2)
        return img
    if t >= HOOK + n * IT:
        return end_card(t - HOOK - n * IT, S.get("end_big", "ME or THEM?"), S.get("end_sub", "Comment who does more at yours."), S.get("tag", "Log it. Points don't lie."), S.get("end_extra"))
    k = int((t - HOOK) // IT); lt = (t - HOOK) - k * IT
    img = Image.new("RGB", (W, H), INK); d = ImageDraw.Draw(img)
    bar(img, (k + lt / IT) / n, col=BLUE)
    done_y = sum(c[1] for c in cats[:k]); done_t = sum(c[2] for c in cats[:k])
    cat, a, b = cats[k]; q = ease(max(0, lt - 1.8) / 2.0)
    ca, cb = round(a * q), round(b * q)
    block(img, "THIS WEEK", W / 2, 285, 38, GREY, path=FM, maxlines=1)
    p = back(lt / 0.3); block(img, cat, W / 2, 470, 96 * (0.8 + 0.2 * p), WHITE, maxw=900, maxlines=2)
    mx = max(a, b, 1); L = 640
    for j, (lab, val, shown, col) in enumerate((("YOU", a, ca, PINK), ("THEM", b, cb, BLUE))):
        y = 700 + j * 280
        d.text((90, y), lab, font=font(FB, 52), fill=col)
        d.rounded_rectangle((90, y + 80, 90 + L + 140, y + 160), radius=40, fill=(45, 45, 45))
        w = max(20, (L + 140) * (shown / mx) * (1 if val == mx else 0.999))
        if shown > 0: d.rounded_rectangle((90, y + 80, 90 + w, y + 160), radius=40, fill=col)
        d.text((990, y + 40), str(shown), font=font(FB, 90), fill=WHITE, anchor="rm")
    cy = done_y + (ca if lt > 3.8 else 0); ct = done_t + (cb if lt > 3.8 else 0)
    d.rounded_rectangle((60, 1330, 1020, 1520), radius=36, fill=(30, 30, 30))
    d.text((300, 1400), "YOU", font=font(FB, 40), fill=PINK, anchor="mm"); d.text((780, 1400), "THEM", font=font(FB, 40), fill=BLUE, anchor="mm")
    d.text((300, 1470), str(cy), font=font(FB, 80), fill=WHITE, anchor="mm"); d.text((780, 1470), str(ct), font=font(FB, 80), fill=WHITE, anchor="mm")
    return img

FORMATS = {"flags": (flags, lambda S: 3.2 + len(S["items"]) * 4.6 + 5.0),
           "translate": (translate, lambda S: 3.4 + len(S["items"]) * 6.2 + 5.0),
           "tier": (tier, lambda S: 3.2 + len(S["items"]) * 3.4 + 5.0),
           "board": (board, lambda S: 3.2 + len(S["cats"]) * 5.0 + 5.0)}

def render(S, out):
    fn, dur = FORMATS[S["format"]]; total = dur(S); n = int(total * FPS)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-stream_loop", "-1", "-i", BED, "-map", "0:v", "-map", "1:a", "-t", f"{total:.2f}",
           "-af", f"loudnorm=I=-19:TP=-2:LRA=7,afade=t=out:st={total - 0.7:.2f}:d=0.7", "-c:v", "libx264", "-preset", "medium", "-crf", "19",
           "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-movflags", "+faststart", out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(n): p.stdin.write(fn(i / FPS, S).tobytes())
    p.stdin.close(); p.wait(); return total

if __name__ == "__main__":
    S = json.load(open(sys.argv[1])); print(render(S, sys.argv[2]))
