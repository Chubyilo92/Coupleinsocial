# CoupleIn reels (Instagram + Facebook = REELS ONLY)

Decision 1 Oct 2026 (Chuby): Instagram is reels only. Static posts and carousels on IG/FB are cancelled (TikTok carousels continue separately). Reels should be quizzes, relatable, or daring/experimental formats. Non-copyrighted images are allowed if they make a reel better.

## Files
- `reels.py`: renderer. `python3 reels.py specs/<name>.json media/<name>.mp4` (1080x1920, 30fps, music bed from the quiz renderer, loudnorm, ~1-3 min per reel; run several in parallel in the background).
- `specs/*.json`: one per reel. `media/*.mp4`: finished reels (hosted via raw.githubusercontent.com/Chubyilo92/Coupleinsocial/main/reels/media/<name>.mp4).
- Needs the quiz renderer folder `you-owe-me-quiz-videos (1)/` (fonts, helpers, assets/music_bed.wav).

## Formats and spec fields (format key = "format")
- **flags**: Red flag or green flag. `hook`, `items` [[text,"red"|"green"],...] (6-7), `end_big`, `tag`. 3s to decide, then a stamp. Running tally. End card shows "Mine: X red, Y green".
- **translate**: What they say vs what they mean. `title`, `hook`, `items` [[say, mean],...] (4-5), `end_big`, `end_sub`, `tag`. Setup shows ~3s, the answer then holds ~3s. Provocative version: harsh line -> empathetic real meaning ("You're such a child." = "I'm tired of planning everything. Take some initiative.").
- **tier**: Tier list S/A/B/C/D, S = unforgivable. `title`, `title_small`, `sub`, `hook`, `items` [[text, "S".."D"],...] (8), `end_big`, `end_sub`, `tag`.
- **board**: Household scoreboard. `title`, `sub`, `hook`, `cats` [[category, you, them],...] (5), `end_big`, `end_sub`, `tag`. Bars count up after ~2s.
- Chat-style reels: Viral-Chat-Video renderer (chubyilo92/viral-chat-video/render.py), only with scripts accurate to real app features (Brownie Points wishlist + partner confirms, shared calendar, Resolve repeat-back). Unconfirmed: mood options, calendar notes field, whether wishlist can hold "divorce".

## Rules learned (all apply)
1. **Pacing**: Chuby said the first version was too fast. Keep: setup visible ~3s before the answer/stamp, then hold ~3s. Reels ~33-40s.
2. **Safe zones**: IG UI covers roughly the bottom 300px and top 200px of 1080x1920. Keep key text out of them.
3. **Verify by looking**: extract frames with ffmpeg into a contact sheet and view them; check audio stream present, size < 25MB.
4. **Score honestly** on downloads, engagement, conversion, relatability (0-10) and report scores every time. Never inflate. Static posts were wrongly scored 9-10 (real ~5-6). Plain-card reels honestly scored: flags 6.6, tier 6.8, translate 7.1, board 6.9, flags2 6.6, triggering translate 7.4. "Plain card" = flat dark background, white bubble, coloured answer box, no photo/footage. Chuby said that look is fine for now. Ship only 7+ average; cut or improve weaker. Scripts that look good on paper are not 10/10: viral needs a genuine twist.
5. **Captions**: unique per reel; hook line, comment-bait question, "Couples communicate better with CoupleIn. Free on iOS and Android, link in bio.", 3-5 hashtags, no clickable IG links. End card always "CoupleIn. Free on iOS & Android."
6. **Provocative translate reels** are an experiment (Chuby asked for them): always empathetic, never abusive, no gender stereotyping. Compare comments vs other formats after 10 Oct.

## Scheduling recipe (Metricool, blogId 7074518, tz Europe/London)
createScheduledPost: date 12:00 local (+01:00 until Sun 25 Oct, then +00:00), info {autoPublish true, draft false, text, media [raw URL], providers [{network instagram},{network facebook}], publicationDate {dateTime, timezone Europe/London}, instagramData {type REEL, showReelOnFeed true}, facebookData {type REEL, title}}. There is no delete tool: unschedule by updating with draft true and resending full content. Probe slots with getScheduledPosts one day at a time (output is huge).

## Current schedule (12:00 UK)
4 Oct flags1 | 5 Oct tier1 | 6 Oct translate1 | 7 Oct translate2 (provocative) | 8 Oct board1 | 9 Oct flags2 | 10 Oct translate3 (provocative). IG/FB 08:00 slots still empty.
Weekly task "Weekly CoupleIn reels" (trig_014VMVTFnUrSyw8tsYnKHcBF) runs 10:07 UK on 11, 18, 25 Oct to fill the following 7 days, then disables itself.


## Batch 2: 08:00 UK reels, 4-10 Oct (made 1 Oct 2026)
Scores = downloads / engagement / conversion / relatability, honest, plain-card look.
| Date 08:00 | Reel | Format | Scores | Avg |
|---|---|---|---|---|
| Sun 4 Oct | translate4 "when they're overwhelmed" | translate | 6.5/7.5/7/8 | 7.25 |
| Mon 5 Oct | translate5 "when they feel unloved" | translate | 6.5/7.5/6.5/8 | 7.1 |
| Tue 6 Oct | tier3 "Things you do but never admit" | tier | 6.5/7.5/6.5/8 | 7.1 |
| Wed 7 Oct | EMPTY: flags3 scored 6.9 (below the 7 bar), held back | flags | 6/7.5/6.5/7.5 | 6.9 |
| Thu 8 Oct | translate6 "after a fight" | translate | 6.5/7.5/7/8 | 7.25 |
| Fri 9 Oct | translate7 "when they feel insecure" | translate | 6.5/7.5/6.5/7.5 | 7.0 |
| Sat 10 Oct | tier2 "Things that quietly end relationships" | tier | 6.5/7.5/6.5/7.5 | 7.0 |
Analytics so far: no meaningful reel data yet (one older reel: 0 comments, 2 saves, 97 reach). Leaning on translate (best honest scores) and tier/flags with a confession or surprise twist; the first-pass tier/flags/board cards scored 6.6-6.9 and were rewritten with bolder hooks.

## Batch 3: 7 Oct 08:00 and 11-13 Oct (made 1 Oct 2026, run-now)
| Date | Time | Reel | Format | Scores (dl/eng/conv/rel) | Avg |
|---|---|---|---|---|---|
| Wed 7 Oct | 08:00 | board3 "The guilty scoreboard" | board | 6/7.5/6.5/8 | 7.0 |
| Sun 11 Oct | 08:00 | translate8 "need space" | translate | 6.5/7.5/6.5/8 | 7.1 |
| Sun 11 Oct | 12:00 | tier4 "Things every couple fakes" | tier | 6.5/8/6.5/7.5 | 7.1 |
| Mon 12 Oct | 08:00 | translate9 "taken for granted" | translate | 6.5/7.5/6.5/8 | 7.1 |
| Mon 12 Oct | 12:00 | flags4 "some nice things are red flags" | flags | 6/7.5/7/7.5 | 7.0 |
| Tue 13 Oct | 08:00 | EMPTY: board4 "Who's worse at..." held back | board | 6/7/6/8 | 6.75 |
| Tue 13 Oct | 12:00 | translate10 "money stress" | translate | 6.5/7.5/6.5/7.5 | 7.0 |
Still empty: flags3 (6.9) was held earlier but 7 Oct 08:00 now has board3. tier4 first render overflowed the S row (4 items); max 3 items per tier row.


## Batch 4: 13 Oct 08:00 to 19 Oct 12:00 (made 10 Oct 2026 by the Thursday task, run-now)
Analytics read 10 Oct (IG reels 4-9 Oct 12:00/08:00, Metricool): every reel reached ~35-135 people, 0 comments, 0 saves, 0 shares on all plain-card reels. Best reach: flags2 (121), tier1 (112), translate6/7 (106-110); worst: board1 (13), board3 (48), translate3 (57). Quiz videos (18:00) are the only ones with a comment (1 each). Signal is thin, so: boards cut, translate kept as the weekly backbone (6 this week), flags/tier mixed with relatable everyday twists. Plain cards are not driving comments; photo/footage backgrounds are the next thing to try (needs Chuby's OK or assets).
| Date | Time | Reel | Format | Scores (dl/eng/conv/rel) | Avg |
|---|---|---|---|---|---|
| Tue 13 Oct | 08:00 | flags5 "Plot twist: some of these are red" | flags | 6.5/7.5/6.5/7.5 | 7.0 |
| Wed 14 Oct | 08:00 | translate11 "when they're jealous" | translate | 6.5/7.5/6.5/8 | 7.1 |
| Wed 14 Oct | 12:00 | tier5 "Excuses ranked by how annoying" | tier | 6.5/8/6.5/8 | 7.25 |
| Thu 15 Oct | 08:00 | flags6 "Texting edition" | flags | 6.5/7.5/7/8 | 7.25 |
| Thu 15 Oct | 12:00 | translate12 "when they're exhausted" | translate | 6.5/7.5/7/8 | 7.25 |
| Fri 16 Oct | 08:00 | translate13 "when they feel disrespected" | translate | 6.5/7.5/6.5/7.5 | 7.0 |
| Fri 16 Oct | 12:00 | tier6 "What you do when you're annoyed" | tier | 6.5/8/6.5/8 | 7.25 |
| Sat 17 Oct | 08:00 | flags7 "Household edition" | flags | 6/7.5/7/8 | 7.1 |
| Sat 17 Oct | 12:00 | translate14 "when they're scared of the future" | translate | 6.5/7.5/6.5/7.5 | 7.0 |
| Sun 18 Oct | 08:00 | translate15 "when work has broken them" | translate | 6.5/7.5/7/8 | 7.25 |
| Sun 18 Oct | 12:00 | tier7 "What wins them back fastest" | tier | 6.5/7.5/7/7.5 | 7.1 |
| Mon 19 Oct | 08:00 | flags8 "Fighting edition" | flags | 6/7.5/7/7.5 | 7.0 |
| Mon 19 Oct | 12:00 | translate16 "when they feel left out" | translate | 6.5/7.5/6.5/7.5 | 7.0 |
Spare (rendered, unscheduled, reuse next week): translate17 "when they go quiet" 7.1.
The earlier "Current schedule" note about a weekly task is superseded: the Thursday task now extends the schedule indefinitely (7-day window from the first gap).
