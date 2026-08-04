#!/usr/bin/env python3
"""Fetch every image in a candidate file and record its true dimensions.

Usage: measure.py candidates.json [--inplace]

Reads only the leading bytes of each image, enough for PIL to report a size.
Writes w/h back onto each record. Records that fail to load get w/h of 0 so
the filter step drops them.
"""
import json, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageFile

Image.MAX_IMAGE_PIXELS = None
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) artss/1.0"}


def dims(url):
    p = ImageFile.Parser()
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
            for _ in range(120):
                c = r.read(4096)
                if not c:
                    break
                p.feed(c)
                if p.image:
                    return p.image.size
    except Exception:
        return (0, 0)
    return (0, 0)


def main():
    path = sys.argv[1]
    arts = json.load(open(path))

    def job(a):
        time.sleep(0.05)  # be a polite guest on museum CDNs
        return dims(a["image"])

    with ThreadPoolExecutor(max_workers=6) as ex:
        for n, (a, wh) in enumerate(zip(arts, ex.map(job, arts)), 1):
            a["w"], a["h"] = wh
            if n % 25 == 0:
                print(f"{n}/{len(arts)}", file=sys.stderr, flush=True)

    json.dump(arts, open(path, "w"), ensure_ascii=False, indent=2)
    failed = sum(1 for a in arts if not a["w"])
    print(f"measured {len(arts) - failed}/{len(arts)}  ({failed} unreachable)")


if __name__ == "__main__":
    main()
