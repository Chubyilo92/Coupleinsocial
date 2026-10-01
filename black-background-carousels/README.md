# Black Background Carousels

**Update 1 Oct 2026: Instagram and Facebook carousels are CUT from 4 Oct and no new ones are made. Carousels continue on TikTok only, as JPEG (see SPEC.md platform rules). Master plan: repo root README.md.**

The four-slide static carousel format CoupleIn runs on TikTok (and, before 4 Oct, Instagram, Facebook and Pinterest).

**Read [SPEC.md](SPEC.md) first.** It is the canonical spec — copy rules, brand constants, sizes, crops, platform gotchas, scheduling. Everything needed to rebuild this from nothing.

```bash
pip install pillow numpy openpyxl
python3 render_batch.py P043    # one post, both sizes
```

Fonts: Poppins (Bold/Medium/Regular) must be installed — on Debian/Ubuntu, `apt install fonts-poppins` or drop the TTFs into the path set at the top of `render.py`.
