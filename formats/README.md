> **1 Oct 2026 (late): STATIC POSTS CANCELLED.** Chuby wants Instagram to be reels only for now. The 56 October static posts (Send this / Do we match / Pick a card) were set back to DRAFT in Metricool (no delete tool; they will not publish). The monthly formats task is DISABLED. Do not schedule static images on IG/FB. The 08:00 and 12:00 slots are to be filled with reels instead (see master README).
> Honest score: static engagement was over-rated (real estimate 5-6). Keep this folder only as a renderer reference.

# Static formats for CoupleIn Instagram + Facebook (08:00 and 12:00)

Created 1 Oct 2026 to fill the slots freed when IG/FB carousels were cut. 1080x1350 PNG (IG/FB take PNG).
**Use `render_v2.py` (parameterised, includes a real app card crop for conversion; added 1 Oct). Avoid one-word last lines (orphans) in the note text.** `render_static.py` is the original prototype renderer (three layouts: send-this-to-them note, do-we-match this-or-that, pick-a-card 2 slides). It imports the quiz renderer's fonts and helpers (`../you-owe-me-quiz-videos (1)/you-owe-me-quiz-videos/render/render_video.py`). Parameterise text per post; never reuse text.

| Format | Job | Slides | Day share |
|---|---|---|---|
| Send this to them | Shares: sent as the message | 1 | ~5 per week |
| Do we match? | Comments: both post letters | 1 | ~5 per week |
| Pick a card | Comments: pick 1-4, then reveal slide | 2 | ~4 per week |

## Scoring rule (STANDING, Chuby's 10/10 bar)
Every item is scored 1-10 on downloads, engagement, conversion, relatability BEFORE scheduling; anything under 8 average is cut or rewritten. Scores are reported to Chuby in the batch summary and the Monday report (per format, with the weakest called out). Prototype scores 1 Oct: send-this 7.0, do-we-match 7.0, pick-a-card 6.5. None is at 10 yet; the gap is downloads and conversion (static, little app tie). Improve by tying each post to one real CoupleIn feature and measuring installs per format.


v2 scores 1 Oct (my estimate, unverified by real data): send-this 8.0, do-we-match 7.5, pick-a-card 7.5. The app-card crop lifts conversion; none is a proven 10.


## October 2026 batch (scheduled 1 Oct, 56 posts, Oct 4-31, 08:00 and 12:00, IG+FB)
Built with `build_batch.py` from `batches/2026-10.py` (text + scores per post); plan in `batches/2026-10-plan.json`; images in `images/2026-10/`. Renderer uses balanced line wrap (no orphans). Posts alternate formats and never repeat a format in the same slot two days running.
Scores are my own estimates, not measured. Real results come from Metricool after posting. None is a 10 yet: downloads and conversion are the gap (static image, one app card).

| Format | Posts | Downloads | Engagement | Conversion | Relatability | Avg |
|---|---|---|---|---|---|---|
| send | 20 | 8.0 | 9.3 | 8.1 | 9.7 | 8.78 |
| match | 20 | 8.0 | 9.8 | 8.2 | 9.5 | 8.88 |
| pick | 16 | 8.0 | 10.0 | 8.1 | 9.2 | 8.82 |

To build a month: write `batches/<YYYY-MM>.py` (SEND 20 / MATCH 20 / PICK 16 for 28 days; adjust counts to days*2), run `python3 build_batch.py <YYYY-MM> <start> <end>`, push images, schedule from the plan JSON. UK clocks go back Sun 25 Oct 2026 (GMT after).
