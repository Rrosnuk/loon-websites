#!/usr/bin/env python3
"""Truffe website images made from the app's brand folder.

  python3 tools/truffe_assets.py <path to furry-friends/brand>

- img/mascot/<name>.webp: Maymay and Murphy portraits, cropped to their round frame with a transparent
  background (the page paints the disc, so it follows light and dark mode). 480 px, plus a 288 px copy.
- img/wordmark.png: the "Truffe" wordmark from the master logo as an alpha mask (the page colours it),
  so the header never retypes the wordmark."""
import sys, numpy as np
from pathlib import Path
from PIL import Image, ImageDraw

BRAND = Path(sys.argv[1])
OUT = Path(__file__).resolve().parent.parent / "src" / "truffe" / "static" / "img"
PORTRAITS = {   # web name: brand file
    "maymay": "maymay/maymay-cutout.png", "maymay-cheer": "maymay/maymay-cheer-cutout.png",
    "maymay-curious": "maymay/maymay-curious-cutout.png", "maymay-calm": "maymay/maymay-calm-cutout.png",
    "murphy": "cat/cat-3-cutout.png", "murphy-curious": "cat/cat-2-cutout.png", "murphy-sleepy": "cat/cat-1-cutout.png",
}

def fit_circle(alpha):
    """The cutouts sit in a round frame; find it from the lower edge of the picture."""
    h, w = alpha.shape
    pts = [(x, np.where(alpha[:, x] > 128)[0].max()) for x in range(0, w, 6) if (alpha[:, x] > 128).any()]
    P = np.array(pts, float); P = P[P[:, 1] > h * .6]
    A = np.c_[P[:, 0], P[:, 1], np.ones(len(P))]
    D, E, F = np.linalg.lstsq(A, -(P[:, 0] ** 2 + P[:, 1] ** 2), rcond=None)[0]
    cx, cy = -D / 2, -E / 2
    return cx, cy, float(np.sqrt(cx * cx + cy * cy - F))

def portrait(src, name):
    im = Image.open(src).convert("RGBA")
    cx, cy, r = fit_circle(np.array(im)[..., 3])
    r = min(r, cx, im.width - cx, cy + 40)      # keep the square inside the picture sideways
    box = tuple(int(round(v)) for v in (cx - r, cy - r, cx + r, cy + r))
    sq = Image.new("RGBA", (box[2] - box[0], box[3] - box[1]), (0, 0, 0, 0))
    sq.paste(im, (-box[0], -box[1]))
    big = 4 * sq.width
    m = Image.new("L", (big, big), 0); ImageDraw.Draw(m).ellipse((0, 0, big - 1, big - 1), fill=255)
    m = m.resize(sq.size, Image.LANCZOS)
    a = np.minimum(np.array(sq)[..., 3], np.array(m)); sq.putalpha(Image.fromarray(a))
    for size, suffix in ((480, ""), (288, "-sm")):
        sq.resize((size, size), Image.LANCZOS).save(OUT / "mascot" / f"{name}{suffix}.webp", quality=80, method=6)

def wordmark():
    logo = np.array(Image.open(BRAND / "truffe-logo-master.png").convert("L")).astype(np.float32)
    h, w = logo.shape
    band = logo[int(h * .63):int(h * .82)]                  # the wordmark sits between the nose and the rule
    ink = np.clip((235 - band) / (235 - 70), 0, 1)           # cream paper -> 0, espresso ink -> 1
    rows, cols = np.where(ink > .5)
    y0, y1, x0, x1 = rows.min() - 4, rows.max() + 5, cols.min() - 4, cols.max() + 5
    a = (ink[y0:y1, x0:x1] * 255).astype(np.uint8)
    img = Image.new("LA", (a.shape[1], a.shape[0])); img.putdata([(0, v) for v in a.flatten()])
    tall = 96
    img = img.resize((round(img.width * tall / img.height), tall), Image.LANCZOS)
    img.save(OUT / "wordmark.png", optimize=True)
    return img.size

if __name__ == "__main__":
    (OUT / "mascot").mkdir(parents=True, exist_ok=True)
    for name, f in PORTRAITS.items():
        portrait(BRAND / f, name)
    print("wordmark", wordmark())
    for f in sorted((OUT / "mascot").glob("*.webp")): print(f.name, f.stat().st_size // 1024, "KB")
