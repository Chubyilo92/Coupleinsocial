#!/usr/bin/env python3
"""Render selected rows of the week-4 batch at both sizes."""

import os
import sys
from batch_week4 import build_rows
from render import build

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")

# feature -> screenshot key used on slide 4
SHOT_FOR = {"Calendar": "calendar", "Brownies": "points", "Resolve": "resolve"}


def poll_options(direction):
    who = "He" if direction == "he" else "She"
    return (f"{who} doesn't know", f"{who} doesn't care")


def slides_for(row):
    o1, o2 = poll_options(row["aimed_at"])
    return [
        ("hook", row["s1a"], row["s1b"]),
        ("line", row["s2a"], row["s2b"]),
        ("poll", row["s3a"], row["s3b"], o1, o2),
        ("proof", row["s4"], row["closer"], SHOT_FOR[row["feature"]]),
    ]


def main(ids):
    rows = {r["id"]: r for r in build_rows(43)}
    made = []
    for pid in ids:
        r = rows[pid]
        outdir = os.path.join(OUT, pid)
        made += build(pid, slides_for(r), outdir)
        print(f"{pid}  {r['feature']:9s} {r['aimed_at']:3s}  {r['s1a']} | {r['s1b']}")
    print(f"\n{len(made)} images in {OUT}")
    return made


if __name__ == "__main__":
    ids = sys.argv[1:] or ["P043", "P044", "P046", "P051",
                           "P073", "P079", "P086",
                           "P103", "P107", "P117"]
    main(ids)
