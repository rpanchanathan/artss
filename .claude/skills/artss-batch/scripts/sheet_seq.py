#!/usr/bin/env python3
"""Contact sheet built one thumbnail at a time, for Commons batches.

Usage: sheet_seq.py candidates.json   ->  sheet.jpg

sheet.py fetches in parallel, which Commons throttles into near-total
failure. Thumbnail URLs come from the API (iiurlwidth); they cannot be
hand-constructed. Look at the output: this is the step that catches
prints sold as paintings, frame-dominated plates and damaged canvases.
"""
import json, urllib.request, urllib.parse, time, os, math, sys
from PIL import Image, ImageDraw
Image.MAX_IMAGE_PIXELS = None
UA = {"User-Agent": "artss-collection/1.0 (offline art screensaver; rajesh@genwise.in)"}
PATH = sys.argv[1] if len(sys.argv) > 1 else 'candidates.json'
recs = json.load(open(PATH))
os.makedirs('thumbs', exist_ok=True)
# official thumbnail URLs from the API — never hand-constructed
files = [r['sourceUrl'].rsplit('/',1)[-1] for r in recs]
thumb = {}
for i in range(0, len(files), 30):
    grp = files[i:i+30]
    u = ("https://commons.wikimedia.org/w/api.php?action=query&format=json&prop=imageinfo"
         "&iiprop=url&iiurlwidth=400&titles=" + urllib.parse.quote("|".join(urllib.parse.unquote(g) for g in grp)))
    d = json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=90))
    nrm = {n["to"]: n["from"] for n in d.get("query",{}).get("normalized",[])}
    for p in d["query"]["pages"].values():
        key = nrm.get(p["title"], p["title"])
        thumb[key] = p["imageinfo"][0].get("thumburl")
    time.sleep(1.5)
COLS, CW, CH = 9, 300, 300
rows = math.ceil(len(recs)/COLS)
sheet = Image.new("RGB", (COLS*CW, rows*(CH+22)), "white")
dr = ImageDraw.Draw(sheet)
for n, r in enumerate(recs):
    key = urllib.parse.unquote(r['sourceUrl'].split('/wiki/')[-1])
    url = thumb.get(key)
    x, y = (n % COLS)*CW, (n//COLS)*(CH+22)
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as resp:
            im = Image.open(resp).convert("RGB")
        im.thumbnail((CW-8, CH-8))
        sheet.paste(im, (x + (CW-im.width)//2, y + (CH-im.height)//2))
    except Exception as e:
        dr.text((x+6, y+CH//2), "FAIL", fill="red")
    dr.text((x+4, y+CH+4), f"{n+1}. {r['title'][:40]}", fill="black")
    time.sleep(0.8)
    if (n+1) % 20 == 0: print(f"  {n+1}/{len(recs)}", flush=True)
sheet.save("sheet.jpg", quality=82)
print("wrote sheet.jpg", sheet.size)
