# Black Background Carousels — canonical spec

**Format:** Black Background carousel, v1
**Owner:** CoupleIn (coupleinapp.com)
**Status:** in production since Sept 2026
**This file is the source of truth.** If chat history and this file disagree, this file wins. Anyone — human or a new Claude session with no prior context — should be able to rebuild the whole pipeline from this folder alone.

---

## 1. What this format is

A four-slide static carousel. Dark cover, light middle, dark close. The name comes from slide 1: near-black background, two lines of Poppins Bold, a pink glow bleeding in from the top-right corner.

The rhetorical shape, and the only thing that actually matters:

| Slide | Background | Job |
|---|---|---|
| 1 — hook | dark | A claim, then the everyday truth that undercuts it. `He'd take a bullet for you. / He won't take the bins out.` |
| 2 — sharpen | light | Twists the knife. Stays concrete. `Dying is a moment. / Improving is a Tuesday.` |
| 3 — release + poll | light | Lets him off the hook (**he's not refusing, he doesn't know how**) and asks a 1-or-2 question. |
| 4 — proof | dark | A real app screenshot, one payoff line, and the closer. |

**Slide 3 is load-bearing.** If the sting is never released, the logical action for the reader is to leave her partner, not download an app. Every release line must be diagnosis-shaped (`He's not careless. / Nothing ever reminds him.`), never instruction-shaped (`Stop having the same fight`) — an instruction makes the 1/2 poll underneath it a non-sequitur.

**The reader and the subject are different people.** The person indicted on screen is usually him; the person downloading is usually her. Copy is aimed at the reader *about* her partner. Roughly 70/30 him/her across a batch.

---

## 2. Copy rules

- Four to eight words a line. If a line needs a comma, it's too long.
- Never `them` for one person. Him and her throughout.
- One idea per slide. Slide 2 does not introduce a second grievance.
- Cut anything below a 10/10. A weak hook in a batch of 90 costs more than the gap it fills.
- Fixed closer on every post: **`7 days. Uninstall if nothing changes.`**

### Three themes only

Mapped to app features. **Mood was deliberately dropped — do not reintroduce it.**

| Theme | Feature | Territory |
|---|---|---|
| Calendar | shared calendar | chores, forgetting, plans, the mental load |
| Brownies | brownie points / wishlist | appreciation, effort, what actually counts |
| Resolve | conflict resolution | arguments, avoidance, shutting down |

Comment keywords, one per theme: Calendar `NUDGE`, Brownies `COUNTS`, Resolve `CALM`.

---

## 3. Brand constants

Poppins, from `/usr/share/fonts/truetype/google-fonts/` (Bold, Medium, Regular).

```python
PINK     = (255, 107, 157)   # #FF6B9D — the brand pink
ORANGE   = (255, 169, 77)    # gradient partner, never used alone
INK      = (13, 8, 12)       # near-black, the "black background"
CREAM    = (255, 245, 249)   # body text on dark
LIGHT_BG = (255, 245, 248)
LIGHT_INK= (26, 20, 22)
MUTED    = (138, 120, 128)   # second line on light slides
```

Cover glow, exactly:
```python
img = add_glow(img, w * 0.92, h * 0.10, int(w * 0.52), PINK,   62)
img = add_glow(img, w * -0.02, h * 0.95, int(w * 0.44), ORANGE, 30)
```

---

## 4. Sizes and safe areas

```python
SIZES = {"ig": (1080, 1350),   # 4:5
         "tt": (1080, 1920)}   # 9:16
```

Safe boxes return `(top, bottom, margin)`:

```python
margin = 96
ig:  (210, h - 190, 96)   # keeps text inside the 1:1 grid crop
tt:  (340, h - 500, 96)   # clears TikTok's caption/button UI
```

The TikTok bottom is 500px up for a reason. TikTok's own UI eats the bottom of a 9:16 photo post. Do not tighten it.

### TikTok will not accept PNG

Photo posts reject `image/png` outright:
> `The content format of the Tiktok photo is incorrect. The 'image/png' type is not allowed, use 'image/jpeg' or 'image/webp' instead.`

This is enforced at **publish** time, not at schedule time, so a scheduled post looks fine and then silently fails. Rule: **Instagram/Facebook/Pinterest = PNG, TikTok = JPEG q92.** Already handled in `render.py`'s `build()`.

---

## 5. Slide 4 — the app screenshot

Source screenshots are 1290×2796, in `shots/`. They are cropped, never squashed, and the crop must contain the moment the user gets the value. An earlier version cut the timer, the buttons and half the events off — that was the single biggest quality complaint and it must not recur.

Two crop tables, because the two platforms have different vertical room:

```python
# render.py — used by the in-carousel slide 4
CROPS = {"points":   (930, 2180),
         "resolve":  (1150, 2520),
         "calendar": (330, 1700)}

# render_ig_end.py — the tuned Instagram end slide
VALUE_CROPS = {
    "resolve":  (1430, 2570),  # "Reflect back" through Next step, nothing clipped
    "points":   (1050, 2150),  # two wishlist items incl. both "I did this" buttons
    "calendar": (340, 1610),   # coral header + Upcoming Events + two whole events
}
```

TikTok (`render_tt_end.py`) does it differently: the **full uncropped screenshot** scaled to `sh = 1430` at `sy = 16`, pink 3px outline, closer centred under it, then a full-width gradient pill reading `Search CoupleIn  ·  free on both stores`. Nothing is overlaid on the screenshot — the CTA sits *below* it. That's because TikTok has no clickable link in the caption (see §8), so the download instruction has to be in the image.

Feature → screenshot: `Calendar → calendar.png`, `Brownies → points.png`, `Resolve → resolve.png`.

---

## 6. The files in this folder

| File | What it does |
|---|---|
| `render.py` | The renderer. Slide kinds: `hook`, `line`, `poll`, `cta`, `proof`. `build(post_id, slides, outdir)` writes both sizes. Run it directly for a single-post smoke test. |
| `batch_week4.py` | The content. `build_rows(start_id=43)` → 90 rows, P043–P132, 30 per theme, 21 he / 9 she each. Holds the hook lists, release lines, payoffs and keywords. |
| `captions.py` | `all_captions(43)` → 90 *unique* captions from rotating ask/CTA/hashtag/bridge pools. Identical captions across posts is the one thing that genuinely reads as automated. |
| `render_batch.py` | Maps rows → slides and renders. `python3 render_batch.py P043 P044 …`, or no args for the default ten. |
| `render_ig_end.py` | Instagram end slide, value-cropped. Outputs `{pid}_ig_4b.png`. |
| `render_tt_end.py` | TikTok end slide, full screenshot + CTA pill. Outputs `{pid}_tt_4b.jpg`. |
| `make_xlsx.py` | Review workbook: Batch sheet (90 rows, caption column, yes/no/maybe dropdown in col N) + Summary sheet with live COUNTIF counts. |
| `shots/` | The four source app screenshots at 1290×2796. |

All four scripts are path-independent — they resolve `shots/` and their output folders relative to their own location. Clone the folder anywhere, `pip install pillow numpy openpyxl`, and run.

Rebuild from cold:
```bash
python3 render_batch.py P043      # one post, both sizes → out/P043/
python3 render_ig_end.py          # → ig_end/
python3 render_tt_end.py          # → tt_end/
python3 make_xlsx.py              # → CoupleIn_week4_90_hooks.xlsx
```

---

## 7. File naming, and why it matters

```
P043_ig_1.png … P043_ig_4.png     Instagram / Facebook / Pinterest
P043_tt_1.jpg … P043_tt_4.jpg     TikTok
P043_ig_4b.png                    replacement Instagram end slide
P043_tt_4b.jpg                    replacement TikTok end slide
```

**Metricool caches images by URL.** It copies whatever is at the URL onto its own CDN (`static.metricool.com`) at schedule time. Re-uploading a *changed* file to the *same* GitHub path does nothing — Metricool serves the old copy. A fixed image must get a **new filename** (hence the `4b` suffix) and the scheduled post must be repointed at it.

---

## 8. Hosting and scheduling

**Hosting:** GitHub, served over `raw.githubusercontent.com`. Metricool accepts public image URLs only — there is no upload endpoint. GitHub does not unzip uploads, so images go up as loose files, and nested folders shift the raw URL, so always verify a URL with `curl -I` before scheduling against it.

**Metricool account:**
```
brandId         7074518
timezone        Europe/London
instagram       coupleinappp
tiktok          coupleinapp
threads         coupleinapp
pinterest       Coupleinapp   (board 925771335842299478, "Relationship advice")
facebook        1361829787006849
```

Cadence in production: IG / FB / TikTok 08:00 daily; Threads 12:30 + 20:00; Pinterest 17:00. Two posts a day per channel was the agreed ceiling to stay clear of spam heuristics.

### Per-platform gotchas

- **TikTok** requires `tiktokData.title` on every post or scheduling is rejected outright. Use the slide-1 hook line.
- **Pinterest** needs a numeric `boardId`. A board *name* will not resolve.
- **Instagram and TikTok captions cannot carry a clickable link.** Instagram has no follower gate — the link lives in bio. TikTok's bio-link restriction applies to personal accounts under 1k followers; either way the download CTA is baked into the slide-4 image.
- **Facebook** captions *can* carry a clickable link. Use it.
- **Threads is a text network.** Do not transcribe a carousel into it. Native shape is three short lines and one specific question — a carousel pasted as text reads as debris.

### Silent failure is the real risk

A post can schedule successfully and then fail at publish (the TikTok PNG case). Nothing surfaces this. The standing mitigations:

1. A twice-daily watchdog scheduled task comparing scheduled vs. published.
2. Publishing reliability sits at the top of the Monday numbers report, above engagement.

If you rebuild the scheduling from scratch, rebuild the watchdog with it.

---

## 9. Known open items

- The app's Resolve screen clips the "Emma" label under her avatar. Fix app-side; it shows in every Resolve slide 4.
- App copy: "Trade kindness" should read "Exchange kindness".
- P043–P132 exist as content; only the first ten are rendered.
