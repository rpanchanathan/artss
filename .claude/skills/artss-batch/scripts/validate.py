#!/usr/bin/env python3
"""Validate artworks.json. Exits non-zero on any error.

Usage: validate.py [artworks.json]

Checks structure and the invariants the page depends on. Deliberately strict:
a missing w/h silently changes an artwork's layout, and a duplicate id breaks
the per-device seen counts.
"""
import json, sys, collections, re

REQUIRED = ["id", "title", "artist", "year", "image", "museum", "license",
            "w", "h", "tags", "sceneContext", "whyBigDeal"]
BANNED = ["masterpiece", "iconic", "timeless", "beloved", "stunning",
          "captures the essence", "breathtaking", "must-see"]
MIN_PIXELS = 2_500_000
MIN_DIM = 1000


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "artworks.json"
    arts = json.load(open(path))
    errors, warnings = [], []

    ids = collections.Counter(a.get("id") for a in arts)
    for k, v in ids.items():
        if v > 1:
            errors.append(f"duplicate id {k} ({v} times)")

    # Same image URL is always a genuine duplicate. Same artist+title is not:
    # Rembrandt painted many canvases titled "Self-Portrait" and the collection
    # legitimately holds more than one, so that case only warrants a look.
    imgs = collections.Counter(a.get("image") for a in arts)
    for k, v in imgs.items():
        if v > 1:
            errors.append(f"duplicate image URL ({v} times): {k}")

    seen = collections.Counter((a.get("artist", ""), a.get("title", "")) for a in arts)
    for (artist, title), v in seen.items():
        if v > 1:
            warnings.append(f"{v} works share artist+title: {artist} — {title} "
                            "(fine if genuinely different paintings; check the images)")

    for a in arts:
        who = f"{a.get('id')} {a.get('title', '?')[:40]}"
        for f in REQUIRED:
            if f not in a or a[f] in (None, "", []):
                errors.append(f"{who}: missing {f}")
        if not isinstance(a.get("tags"), list):
            errors.append(f"{who}: tags must be a list")
        w, h = a.get("w") or 0, a.get("h") or 0
        if not w or not h:
            errors.append(f"{who}: no measured dimensions")
        else:
            if min(w, h) < MIN_DIM or w * h < MIN_PIXELS:
                warnings.append(f"{who}: {w}x{h} below quality floor")
            r = w / h
            if r > 3.0 or r < 0.33:
                errors.append(f"{who}: {w}x{h} is {r:.1f}:1 — too extreme to display. "
                              "Handscrolls in particular: the museum's mid-size "
                              "derivative caps the LONG edge, which flattens the "
                              "short edge to nothing. Check for a version with a "
                              "usable short edge before including.")
        if not str(a.get("image", "")).startswith("https://"):
            errors.append(f"{who}: image URL not https")
        if "_web.jpg" in str(a.get("image", "")):
            errors.append(f"{who}: Cleveland _web derivative — use _print")
        if "/full/800," in str(a.get("image", "")):
            errors.append(f"{who}: V&A capped at 800px — use /full/full/")
        blob = f"{a.get('sceneContext','')} {a.get('whyBigDeal','')}".lower()
        for b in BANNED:
            if b in blob:
                warnings.append(f"{who}: banned phrase '{b}'")
        sc = len(str(a.get("sceneContext", "")).split())
        bd = len(str(a.get("whyBigDeal", "")).split())
        if sc and not (18 <= sc <= 70):
            warnings.append(f"{who}: sceneContext {sc} words (target 25-50)")
        if bd and not (30 <= bd <= 95):
            warnings.append(f"{who}: whyBigDeal {bd} words (target 40-80)")

    print(f"{len(arts)} artworks, {len(errors)} errors, {len(warnings)} warnings")
    for e in errors[:40]:
        print("  ERROR  " + e)
    for w in warnings[:40]:
        print("  warn   " + w)
    if len(warnings) > 40:
        print(f"  ... {len(warnings) - 40} more warnings")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
