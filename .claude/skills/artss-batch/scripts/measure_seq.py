#!/usr/bin/env python3
"""Measure images one at a time, for Commons batches.

Usage: measure_seq.py candidates.json

measure.py fans out over six threads with a generic browser User-Agent, which
upload.wikimedia.org answers with 429 "does not comply with our robot policy"
for most of the batch. The failures are not real. This does the same job
sequentially under a descriptive UA.

Note PIL reports the STORED size and ignores EXIF orientation, while the
browser applies it. Cross-check against the API height/width and against a
browser new Image() load before trusting a landscape result for an obviously
upright painting.
"""
import json, urllib.request, time, sys
from PIL import Image, ImageFile
Image.MAX_IMAGE_PIXELS = None
UA = {"User-Agent": "artss-collection/1.0 (offline art screensaver; rajesh@genwise.in)"}
PATH = sys.argv[1] if len(sys.argv) > 1 else 'candidates.json'
recs = json.load(open(PATH))
def dims(url):
    for attempt in range(3):
        p = ImageFile.Parser()
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
                for _ in range(300):
                    c = r.read(8192)
                    if not c: break
                    p.feed(c)
                    if p.image: return p.image.size
        except Exception:
            time.sleep(5*(attempt+1))
    return (0, 0)
for i, a in enumerate(recs, 1):
    a['w'], a['h'] = dims(a['image'])
    if i % 15 == 0:
        json.dump(recs, open(PATH,'w'), indent=1, ensure_ascii=False)
        print(f"  {i}/{len(recs)}", flush=True)
    time.sleep(1.2)                       # sequential: a screensaver shows one at a time
json.dump(recs, open(PATH,'w'), indent=1, ensure_ascii=False)
bad = [a['title'] for a in recs if not a['w']]
print(f"measured {len(recs)-len(bad)}/{len(recs)}", "unreachable:", bad)
import json, urllib.request, time, sys
from PIL import Image, ImageFile
Image.MAX_IMAGE_PIXELS = None
UA = {"User-Agent": "artss-collection/1.0 (offline art screensaver; rajesh@genwise.in)"}
PATH = sys.argv[1] if len(sys.argv) > 1 else 'candidates.json'
recs = json.load(open(PATH))
def dims(url):
    for attempt in range(3):
        p = ImageFile.Parser()
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
                for _ in range(300):
                    c = r.read(8192)
                    if not c: break
                    p.feed(c)
                    if p.image: return p.image.size
        except Exception:
            time.sleep(5*(attempt+1))
    return (0, 0)
for i, a in enumerate(recs, 1):
    a['w'], a['h'] = dims(a['image'])
    if i % 15 == 0:
        json.dump(recs, open(PATH,'w'), indent=1, ensure_ascii=False)
        print(f"  {i}/{len(recs)}", flush=True)
    time.sleep(1.2)                       # sequential: a screensaver shows one at a time
json.dump(recs, open(PATH,'w'), indent=1, ensure_ascii=False)
bad = [a['title'] for a in recs if not a['w']]
print(f"measured {len(recs)-len(bad)}/{len(recs)}", "unreachable:", bad)
