#!/usr/bin/env python3
"""Show the collection's current shape against the expansion targets.

Usage: stats.py [artworks.json]
"""
import json, sys, collections

TARGETS = {
    "impressionism": 90, "post-impressionism": 50, "south-asia": 110,
    "china": 55, "japan": 45, "korea": 10, "persia": 25,
    "renaissance": 45, "northern-renaissance": 30, "baroque": 60,
    "romanticism": 40, "realism": 35, "ukiyo-e": 40,
    "dutch-golden-age": 38, "modern": 35,
}


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "artworks.json"
    arts = json.load(open(path))
    tags = collections.Counter(t for a in arts for t in a.get("tags", []))

    print(f"{len(arts)} artworks, target 800-1000\n")
    print(f"{'tag':24} {'now':>5} {'target':>7} {'gap':>6}")
    for t, target in sorted(TARGETS.items(), key=lambda kv: kv[1] - tags.get(kv[0], 0), reverse=True):
        now = tags.get(t, 0)
        gap = target - now
        flag = "  <-- next" if gap >= 30 else ""
        print(f"{t:24} {now:5} {target:7} {gap:+6}{flag}")

    print("\nby museum:")
    for m, c in collections.Counter(a.get("museum", "?") for a in arts).most_common():
        print(f"  {c:4}  {m}")

    print("\nlayout split:")
    b = collections.Counter()
    for a in arts:
        r = (a.get("w") or 1) / (a.get("h") or 1)
        b["scroll (pans)" if r < 0.5 else "split" if r < 1.15 else "fit"] += 1
    for k, v in b.items():
        print(f"  {v:4}  {k}")

    untagged = [a["title"] for a in arts if len(a.get("tags", [])) <= 2]
    if untagged:
        print(f"\n{len(untagged)} works with 2 or fewer tags (thin metadata)")


if __name__ == "__main__":
    main()
