#!/usr/bin/env python3
"""Build a contact sheet so a human (or Claude) can look at a batch at once.

Usage: sheet.py candidates.json [out.jpg]

The point is the eyeball pass. Filters catch resolution and licence; only
looking catches a hanging scroll photographed with 60% silk mounting, a
painting shot at an angle, a near-duplicate of something already in the
collection, or a "portrait" that is actually a photo of a frame.
"""
import json, sys, io, urllib.request
from concurrent.futures import ThreadPoolExecutor
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) artss/1.0"}
TILE = 300
COLS = 8


def fetch(a):
    try:
        with urllib.request.urlopen(urllib.request.Request(a["image"], headers=UA), timeout=60) as r:
            im = Image.open(io.BytesIO(r.read())).convert("RGB")
        im.thumbnail((TILE, TILE))
        return im
    except Exception:
        return None


def main():
    path = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else "contact-sheet.jpg"
    arts = json.load(open(path))

    with ThreadPoolExecutor(max_workers=6) as ex:
        tiles = list(ex.map(fetch, arts))

    pairs = [(im, a) for im, a in zip(tiles, arts) if im]
    rows = (len(pairs) + COLS - 1) // COLS
    sheet = Image.new("RGB", (COLS * (TILE + 8) + 8, rows * (TILE + 8) + 8), (18, 18, 18))
    for i, (im, a) in enumerate(pairs):
        x = (i % COLS) * (TILE + 8) + 8 + (TILE - im.width) // 2
        y = (i // COLS) * (TILE + 8) + 8 + (TILE - im.height) // 2
        sheet.paste(im, (x, y))
    sheet.save(out, quality=85)

    print(f"{out}  {len(pairs)} tiles, {COLS} per row, reading order:")
    for i, (_, a) in enumerate(pairs):
        print(f"  {i + 1:3}. {a['artist'][:28]:30} {a['title'][:44]}")
    missing = [a["title"] for im, a in zip(tiles, arts) if not im]
    if missing:
        print(f"\nunreachable ({len(missing)}): " + ", ".join(m[:30] for m in missing))


if __name__ == "__main__":
    main()
