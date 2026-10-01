"""Static IG/FB formats v2: parameterised, with a real app-screen crop for conversion.
Usage (import): from render_v2 import send, match, pick
  send(text, thanks, out_png, hl=None)         # 'Send this to them' note + Brownie Points card
  match(pairs, foot, out_png)                  # 5 A/B pairs (list of 5 (a,b) tuples)
  pick(outcomes, out_pick, out_reveal)         # 4 outcome strings -> 2 slides
Fonts/helpers come from the quiz renderer. App crop: black-background-carousels/shots/points.png.
"""
import os, importlib.util
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
RV = os.path.join(HERE, "..", "you-owe-me-quiz-videos (1)", "you-owe-me-quiz-videos", "render", "render_video.py")
spec = importlib.util.spec_from_file_location("rv", RV); rv = importlib.util.module_from_spec(spec); spec.loader.exec_module(rv)
_greedy = rv.wrap
def _balanced(d, text, f, maxw):
    """Same line count as greedy, but the narrowest width that keeps it: evens out lines, kills orphans."""
    ls = _greedy(d, text, f, maxw)
    if len(ls) < 2: return ls
    lo, hi = 50, maxw
    while hi - lo > 4:
        mid = (lo + hi) / 2
        if len(_greedy(d, text, f, mid)) <= len(ls) and all(d.textlength(w, font=f) <= mid for w in text.split()): hi = mid
        else: lo = mid
    return _greedy(d, text, f, hi)
rv.wrap = _balanced
SHOTS = os.path.join(HERE, "..", "black-background-carousels", "shots", "points.png")
W, H = 1080, 1350
BG = (17, 17, 17)

def card(width):
    c = Image.open(SHOTS).convert("RGB").crop((56, 1085, 1238, 1684))
    c = c.resize((width, int(c.height * width / c.width)), Image.LANCZOS)
    m = Image.new("L", c.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, c.width - 1, c.height - 1), 40, fill=255)
    return c, m

def paste_card(img, cx, y, width):
    c, m = card(width); img.paste(c, (int(cx - c.width / 2), int(y)), m); return y + c.height

def send(text, thanks, out, hl=None):
    a = Image.new("RGB", (W, H), (255, 77, 109))
    rv.boxed(a, "SEND THIS TO THEM", W / 2, 130, 38, rv.INK, rv.WHITE)
    rv.block(a, text, W / 2, 440, 84, rv.WHITE, maxlines=4, hl=hl)
    rv.block(a, thanks, W / 2, 740, 48, rv.INK, path=rv.FM, maxlines=2)
    paste_card(a, W / 2, 830, 760)
    rv.block(a, "The small stuff counts. Log it in CoupleIn.", W / 2, 1290, 32, rv.WHITE, path=rv.FM, maxlines=1)
    a.save(out)

def match(pairs, foot, out):
    b = Image.new("RGB", (W, H), BG)
    rv.boxed(b, "DO WE MATCH?", W / 2, 130, 44, rv.YELLOW, rv.INK)
    rv.block(b, "Both comment your letters. Count the matches.", W / 2, 245, 38, rv.WHITE, path=rv.FM, maxlines=2)
    d = ImageDraw.Draw(b); y = 360
    for p, q in pairs:
        for j, (t, col) in enumerate(((p, rv.OPT[0]), (q, rv.OPT[1]))):
            x = 60 + j * 495
            d.rounded_rectangle((x, y, x + 465, y + 118), radius=32, fill=col[0])
            f = rv.font(rv.FB, 38); tt = ("A  " if j == 0 else "B  ") + t
            d.text((x + 232 - d.textlength(tt, font=f) / 2, y + 59 - 24), tt, font=f, fill=col[1])
        y += 142
    rv.block(b, "5/5 = soulmates.  0/5 = how are you still together?", W / 2, 1120, 34, rv.YELLOW, path=rv.FM, maxlines=2)
    rv.block(b, foot, W / 2, 1230, 32, (230, 230, 230), path=rv.FM, maxlines=2)
    rv.block(b, "CoupleIn  |  link in bio", W / 2, 1300, 28, (150, 150, 150), path=rv.FM, maxlines=1)
    b.save(out)

def pick(outcomes, out_pick, out_reveal):
    c = Image.new("RGB", (W, H), BG)
    rv.boxed(c, "PICK A CARD", W / 2, 140, 44, rv.YELLOW, rv.INK)
    rv.block(c, "Comment 1, 2, 3 or 4. Then tag your partner.", W / 2, 260, 38, rv.WHITE, path=rv.FM, maxlines=2)
    d = ImageDraw.Draw(c)
    for i in range(4):
        x = 70 + (i % 2) * 490; y = 380 + (i // 2) * 440
        d.rounded_rectangle((x, y, x + 450, y + 410), radius=40, fill=rv.OPT[i][0])
        f = rv.font(rv.FB, 190); s = str(i + 1); d.text((x + 225 - d.textlength(s, font=f) / 2, y + 70), s, font=f, fill=rv.OPT[i][1])
    rv.block(c, "swipe to see what you got", W / 2, 1270, 32, (170, 170, 170), path=rv.FM)
    c.save(out_pick)
    e = Image.new("RGB", (W, H), BG)
    rv.boxed(e, "YOUR CARD", W / 2, 100, 44, rv.YELLOW, rv.INK)
    d = ImageDraw.Draw(e); y = 190
    for i, t in enumerate(outcomes):
        d.rounded_rectangle((60, y, 1020, y + 160), radius=32, fill=rv.OPT[i][0])
        f = rv.font(rv.FB, 84); d.text((100, y + 34), str(i + 1), font=f, fill=rv.OPT[i][1])
        rv.block(e, t, 590, y + 82, 36, rv.OPT[i][1], maxw=640, maxlines=3, path=rv.FB)
        y += 180
    rv.block(e, "They'll 'forget'. Log it in CoupleIn.", W / 2, y + 40, 36, rv.WHITE, path=rv.FM, maxlines=1)
    paste_card(e, W / 2, y + 80, 560)
    e.save(out_reveal)

if __name__ == "__main__":
    os.makedirs("/tmp/proto2", exist_ok=True)
    send("you still make my tea exactly how I like it.", "thank you for noticing.", "/tmp/proto2/send.png", hl="exactly")
    match([("Tea","Coffee"),("Stay in","Go out"),("Text","Call"),("Early bird","Night owl"),("Plan it","Wing it")], "Settle who owes who in CoupleIn.", "/tmp/proto2/match.png")
    pick(["Your partner owes you a cuddle. They don't know yet.","Pick the next date. No veto.","You get the last bite. Of anything.","You were right. They have to say it out loud."], "/tmp/proto2/pick1.png", "/tmp/proto2/pick2.png")
