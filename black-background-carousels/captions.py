#!/usr/bin/env python3
"""Captions for the week-4 batch. Varied by design: identical captions
across posts is the one thing that genuinely reads as automated."""

from batch_week4 import build_rows

ASKS = [
    "So which is it — 1 or 2? Tell me below.",
    "Be honest. 1 or 2?",
    "Comment 1 or 2. I read every one.",
    "Which one is he? Drop a 1 or a 2.",
    "1 or 2 — no wrong answer, but pick one.",
    "Genuinely curious on this one: 1 or 2?",
]
ASKS_SHE = [
    "So which is it — 1 or 2? Tell me below.",
    "Be honest. 1 or 2?",
    "Comment 1 or 2. I read every one.",
    "Which one is she? Drop a 1 or a 2.",
    "1 or 2 — no wrong answer, but pick one.",
    "Genuinely curious on this one: 1 or 2?",
]
CTAS = [
    "CoupleIn is free on iOS and Android. Link in bio.",
    "Free on iOS and Android — link in bio.",
    "We built CoupleIn for exactly this. Link in bio.",
    "Link in bio if you want the fix, not just the diagnosis.",
]
TAGS = [
    "#relationshipadvice #couplegoals #relationships #marriedlife #relationshiptips",
    "#couplegoals #relationshipgoals #lovelanguages #datenight #couples",
    "#relationshipadvice #marriageadvice #communication #couples #mentalload",
    "#relationships #relationshiptips #loveadvice #partnership #couplestuff",
    "#couplegoals #relationshipadvice #connection #couples #emotionalintelligence",
]
# one per feature, so the caption's middle line isn't the same shape every time
BRIDGE = {
    "Calendar": [
        "The forgetting isn't the problem. The system is.",
        "Nobody is doing this on purpose. That's the frustrating part.",
        "This is what the mental load actually looks like day to day.",
    ],
    "Brownies": [
        "Effort aimed at the wrong thing still reads as no effort.",
        "Most people aren't refusing to try. They're guessing.",
        "Being appreciated and being noticed are not the same thing.",
    ],
    "Resolve": [
        "Most arguments don't need more feeling. They need a structure.",
        "Shutting down usually isn't coldness. It's not knowing the next line.",
        "The same fight on repeat is a process problem, not a love problem.",
    ],
}


def caption(row, i):
    asks = ASKS_SHE if row["aimed_at"] == "she" else ASKS
    parts = [
        f"{row['s1a']} {row['s1b']}",
        "",
        BRIDGE[row["feature"]][i % 3],
        "",
        f"{row['s3a']} {row['s3b']}",
        asks[i % len(asks)],
        "",
        CTAS[i % len(CTAS)],
        "",
        TAGS[i % len(TAGS)],
    ]
    return "\n".join(parts)


def all_captions(start_id=43):
    rows = build_rows(start_id)
    return {r["id"]: caption(r, i) for i, r in enumerate(rows)}


if __name__ == "__main__":
    caps = all_captions()
    print(caps["P043"])
    print("\n---\n")
    print(caps["P107"])
    print(f"\n{len(caps)} captions; unique: {len(set(caps.values()))}")
