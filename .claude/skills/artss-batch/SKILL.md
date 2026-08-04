---
name: artss-batch
description: Add a batch of ~50 artworks to the artss screensaver collection. Queries open-access museum APIs, applies licence/resolution/composition filters, writes the house-style context notes, verifies every image, and appends to artworks.json. Use when expanding the artss collection or when asked to "run the next artss batch".
argument-hint: [batch-focus, e.g. "impressionism" or "south-asia post-1850"]
allowed-tools: Bash, Read, Write, Edit, Grep
---

# artss batch expansion

Adds ~50 artworks per run to `artworks.json`. The collection is going from 310
to 800–1000; each batch is one increment. Quality is the point — a batch that
adds 30 good works beats one that adds 50 padded ones.

## Target mix

Current gaps, in priority order. Check the live counts before choosing a focus:

```bash
python3 .claude/skills/artss-batch/scripts/stats.py
```

| Bucket | Target | Notes |
|--------|--------|-------|
| Impressionism / Post-Impressionism | ~140 | biggest gap; van Gogh, Monet, Cézanne all under-represented |
| South Asia | ~110 | existing 32 are all pre-1850 Mughal/Pahari; need Company School, Ravi Varma, early Bengal School |
| East Asia | ~110 | China/Japan/Korea |
| Renaissance + Baroque non-Dutch | ~150 | Italy, Spain |
| Modern (licensed tier) | 30–40 | see "Modern tier" below — hand-curated only |
| Dutch Golden Age | leave as-is | dilute by growth, do not cut |

## Sources

All have open APIs and serve public-domain images:

| Museum | API | Image URL notes |
|--------|-----|-----------------|
| The Met | `https://collectionapi.metmuseum.org/public/collection/v1/search?q=&hasImages=true` | use `primaryImage` (full size), not `primaryImageSmall` |
| Cleveland | `https://openaccess-api.clevelandart.org/api/artworks/?cc0=1` | **always `_print.jpg`, never `_web.jpg`** (666px vs 2515px) |
| ~~Art Institute of Chicago~~ | — | **Unusable.** Its IIIF server requires an `AIC-User-Agent` header, which an `<img>` tag cannot send, so images 403 in the browser even though curl-with-header works. Verified in Chrome. Do not add AIC works. |
| Rijksmuseum | `https://www.rijksmuseum.nl/api/en/collection` | needs a key |
| NGA (Washington) | `https://api.nga.gov/art/` | |
| V&A | `https://api.vam.ac.uk/v2/objects/search` | IIIF: use `/full/full/0/default.jpg`, not `/full/800,/` |
| Smithsonian | `https://api.si.edu/openaccess/api/v1.0/search` | |

Prefer breadth of source — a batch drawn from one museum inherits that
museum's collecting bias.

**Always verify a new source loads as a plain `<img>` in a real browser before
building a batch on it.** An API that answers curl is not the same as an image
server that will serve a hotlinked page. Test with `new Image()` in Chrome,
not with curl, because the failure is header-based and curl can be made to
succeed where the browser cannot.

Two filter traps that have already cost a batch:
- AIC's `classification_title` is the *medium* ("oil on canvas"), not a type.
  Filter on `artwork_type_title` instead. A "painting" test against the wrong
  field silently rejects everything and looks like a thin result.
- The Met's `classification` **is** "Paintings". The two APIs disagree; check
  the field before filtering on it.

## Hard filters

Apply before writing anything. Reject silently, but `log` the count rejected
per reason so a batch that mostly bounced is visible rather than looking thin.

1. **Licence** — public domain or CC0/CC-BY only. Record it in `license`.
   Anything unclear is a reject, not a maybe.
2. **Resolution** — min dimension ≥ 1000px AND ≥ 2.5 megapixels. Fetch and
   measure; never trust the API's stated dimensions.
3. **Aspect** — reject anything outside 0.33–3.0. Beware handscrolls: museum
   mid-size derivatives cap the *long* edge, so a 120000×2834 scroll arrives
   as 3400×80 with the height destroyed. Cleveland offers only web/print/full
   with no IIIF, so for those there is no usable middle size — check before
   including, don't assume a bigger derivative exists.
4. **Composition** — reject where the museum photograph is mostly mount,
   frame, backing board or hanging cord rather than artwork. This is the
   failure mode for East Asian hanging scrolls and album folios, and it is
   only visible by looking. See the contact sheet step.
5. **Duplicate** — no repeat `id`, and check title+artist against existing.
   The collection already has legitimate repeated titles (six *Annunciation*s
   as a `comparisonSet`), so match on artist+title, not title alone.
6. **Not a fragment** — no detail shots, no single manuscript pages of pure
   text, no coins or fragments. It has to work as a full screen.

## Per-artwork record

```json
{
  "id": 436535,
  "title": "Wheat Field with Cypresses",
  "artist": "Vincent van Gogh",
  "artistBio": "Dutch, Zundert 1853–1890 Auvers-sur-Oise",
  "year": "1889",
  "medium": "Oil on canvas",
  "image": "https://images.metmuseum.org/.../DP-42549-001.jpg",
  "sourceUrl": "https://www.metmuseum.org/art/collection/search/436535",
  "museum": "The Met",
  "license": "public-domain",
  "w": 4000, "h": 3186,
  "tags": ["post-impressionism", "france", "19th-century", "landscape-format"],
  "sceneContext": "...",
  "whyBigDeal": "..."
}
```

`w`/`h` are **measured**, not copied from the API — layout depends on them.

## Writing the notes

This is the slow part and the part that carries the collection. Match the
existing voice exactly; read a dozen entries before starting.

**sceneContext** — ~35 words, target 25–50. What was happening when this was
painted. Concrete circumstance, not description of the image (the viewer can
see the image). Where the painter was, what had just happened to them, who
commissioned it, what the room was.

**whyBigDeal** — ~55 words, target 40–80. Why it matters. A specific fact
that changes how you look at it, then what it changed in art. Earn the claim;
do not assert greatness.

Rules:
- No "masterpiece", "iconic", "timeless", "beloved", "stunning", "capturing
  the essence of".
- No sentence that would be true of any painting by that artist.
- Prefer one verifiable specific over three generalities. "Painted on the
  reverse of a still life because he couldn't afford fresh canvas" beats a
  paragraph about his poverty.
- If you don't know something specific about a work, that work does not go in
  the batch. Padding here is how the collection gets worse.
- Never invent a date, patron, or circumstance. If uncertain, drop the work.

## Workflow

1. Pick the focus (from `$1` or the biggest gap in `stats.py`).
2. Query sources; assemble ~70 candidates to survive filtering down to ~50.
3. Fetch and measure every image:
   `python3 .claude/skills/artss-batch/scripts/measure.py candidates.json`
4. Apply the hard filters. Report rejects per reason.
5. **Contact sheet** — `python3 .claude/skills/artss-batch/scripts/sheet.py candidates.json`
   then Read the output image. Look at it. This is where mount-dominated
   scrolls, damaged works, near-duplicate compositions and bad crops get
   caught. Do not skip this; it is one image and it catches what no filter can.
6. Write `sceneContext` / `whyBigDeal` for the survivors.
7. Validate: `python3 .claude/skills/artss-batch/scripts/validate.py`
8. Append to `artworks.json`, commit with the batch focus in the message.
9. Report: added, rejected per reason, new totals per bucket.

## Modern tier

Post-1930 work is still in copyright and cannot be sourced the way the rest
is. Do not bulk-query for it. Each entry needs an individually verified
licence — CC-released by the artist or estate, or a museum's own open
contemporary holding. Set `license` to the actual licence string and add an
`attribution` field where the licence requires it. If a licence cannot be
verified in one step, the work does not go in.

## Verification before claiming done

- Every image URL returns 200 and measures ≥ the filter floor.
- `artworks.json` parses and every record has all required fields.
- Load the page locally (`python3 -m http.server`) and confirm the new works
  render in their assigned layout.
- Never report a count you have not checked against the file.
