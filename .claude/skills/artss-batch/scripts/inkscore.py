#!/usr/bin/env python3
"""Score how much of an image is actually painted, as opposed to blank paper.

Usage: inkscore.py candidates.json [--reject-below 0.22]

Manuscript-heavy searches return a lot of things that are technically in the
collection but useless on a screen: calligraphy pages, faint pencil sketches,
palm-leaf text strips, and folios where the painting is a small panel in a
large blank margin. They all share one property - very little saturated
colour - so a single measurement separates them from paintings.

Writes `ink` onto each record and optionally drops anything below a floor.
Genuinely monochrome works (ink landscapes, grisaille) score low too, which is
a real limitation, but they also read poorly on a TV across a room.
"""
import json, sys, io, urllib.request
from concurrent.futures import ThreadPoolExecutor
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) artss/1.0"}


def ink(url):
    """Fraction of pixels carrying saturated, non-black colour."""
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
            im = Image.open(io.BytesIO(r.read())).convert("RGB")
    except Exception:
        return None
    im.thumbnail((220, 220))
    hsv = im.convert("HSV")
    px = list(hsv.getdata())
    if not px:
        return None
    hit = sum(1 for _, s, v in px if s > 64 and v > 40)
    return round(hit / len(px), 4)


def main():
    path = sys.argv[1]
    floor = None
    if "--reject-below" in sys.argv:
        floor = float(sys.argv[sys.argv.index("--reject-below") + 1])

    arts = json.load(open(path))
    with ThreadPoolExecutor(max_workers=6) as ex:
        for a, s in zip(arts, ex.map(lambda x: ink(x["image"]), arts)):
            a["ink"] = s if s is not None else 0.0

    arts.sort(key=lambda a: a["ink"])
    print("lowest 15 (most blank):")
    for a in arts[:15]:
        print(f"  {a['ink']:.3f}  {a['title'][:60]}")
    print("\nhighest 5:")
    for a in arts[-5:]:
        print(f"  {a['ink']:.3f}  {a['title'][:60]}")

    if floor is not None:
        keep = [a for a in arts if a["ink"] >= floor]
        print(f"\nfloor {floor}: kept {len(keep)}, dropped {len(arts) - len(keep)}")
        arts = keep
    json.dump(arts, open(path, "w"), ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
