"""Render + plan a month of IG/FB static posts.  python3 build_batch.py 2026-10 2026-10-04 2026-10-31
Writes formats/images/<YYYY-MM>/<date>-<HHMM>-<fmt>[-n].png and formats/batches/<YYYY-MM>-plan.json
"""
import sys, os, json, random, datetime as dt, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from render_v2 import send, match, pick

month, start, end = sys.argv[1], sys.argv[2], sys.argv[3]
spec = importlib.util.spec_from_file_location("b", os.path.join(HERE, "batches", f"{month}.py"))
B = importlib.util.module_from_spec(spec); spec.loader.exec_module(B)
d0, d1 = dt.date.fromisoformat(start), dt.date.fromisoformat(end)
days = [(d0 + dt.timedelta(i)) for i in range((d1 - d0).days + 1)]
need = {"S": len(B.SEND), "M": len(B.MATCH), "P": len(B.PICK)}
assert sum(need.values()) == 2 * len(days), (need, len(days))

# slot plan: two different formats per day, never the same format in the same slot two days running
rng = random.Random(7)
def plan():
    left = dict(need); out = []
    for i in range(len(days)):
        opts = [(a, b) for a in "SMP" for b in "SMP" if a != b and left[a] > 0 and left[b] > 0
                and not (out and (out[-1][0] == a or out[-1][1] == b))]
        if not opts: return None
        # prefer formats with most remaining per day left
        opts.sort(key=lambda ab: -(left[ab[0]] + left[ab[1]]) + rng.random() * 3)
        a, b = opts[0]; left[a] -= 1; left[b] -= 1; out.append((a, b))
    return out
for _ in range(5000):
    P = plan()
    if P: break
assert P

TAGS = {"S": "#couplegoals #relationships #smallthings #lovelanguages #couplein",
        "M": "#thisorthat #couplegoals #relationships #couplesquiz #couplein",
        "P": "#pickacard #couplegoals #relationships #couplestuff #couplein"}
BODY = {"S": "The small stuff is the big stuff. CoupleIn turns it into Brownie Points so none of it goes unnoticed.",
        "M": "Both of you comment, then count the matches. CoupleIn is where you settle the rest.",
        "P": "Swipe for your card. Then log it in CoupleIn so it actually happens."}
img = os.path.join(HERE, "images", month); os.makedirs(img, exist_ok=True)
it = {"S": iter(B.SEND), "M": iter(B.MATCH), "P": iter(B.PICK)}
NAME = {"S": "send", "M": "match", "P": "pick"}
posts = []
for day, pair in zip(days, P):
    for hhmm, f in zip(("08:00", "12:00"), pair):
        x = next(it[f]); stem = f"{day}-{hhmm.replace(':','')}-{NAME[f]}"
        if f == "S":
            note, thanks, hl, hook, sc = x; files = [stem + ".png"]
            send(note, thanks, os.path.join(img, files[0]), hl=hl)
        elif f == "M":
            pairs, foot, hook, sc = x; files = [stem + ".png"]
            match(pairs, foot, os.path.join(img, files[0]))
        else:
            outs, hook, sc = x; files = [stem + "-1.png", stem + "-2.png"]
            pick(outs, os.path.join(img, files[0]), os.path.join(img, files[1]))
        cap = f"{hook}\n\n{BODY[f]}\n\nFree on iOS and Android. Link in bio.\n\n{TAGS[f]}"
        posts.append({"date": str(day), "time": hhmm, "format": NAME[f], "files": files, "caption": cap,
                      "scores": dict(zip(("downloads", "engagement", "conversion", "relatability"), sc)),
                      "avg": sum(sc) / 4})
json.dump(posts, open(os.path.join(HERE, "batches", f"{month}-plan.json"), "w"), indent=1)
print(len(posts), "posts;", " ".join(a + b for a, b in P))
