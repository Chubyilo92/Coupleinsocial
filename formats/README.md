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
