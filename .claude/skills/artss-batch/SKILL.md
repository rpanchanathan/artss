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

785 of a target 1000. Check live counts before choosing a focus:

```bash
python3 .claude/skills/artss-batch/scripts/stats.py
```

Batches 1–6 filled every regional and period bucket in the original plan.
What remains is **not** more depth — it is the canonical works themselves.

### Batches 7–8: the celebrated works (~215 to reach 1000)

The collection has 785 artworks and is missing the Mona Lisa, Las Meninas,
The Scream, Starry Night, The Birth of Venus, Girl with a Pearl Earring, The
Garden of Earthly Delights, The Arnolfini Portrait, The Ambassadors, Hunters
in the Snow, The Third of May, Liberty Leading the People, The Raft of the
Medusa, Le Déjeuner sur l'herbe, A Bar at the Folies-Bergère, and the School
of Athens. Fourteen major artists are absent entirely, including **Leonardo,
Bosch, Friedrich, Géricault, Giorgione, Uccello, Piero della Francesca,
Bonnard and Matisse**.

The reason is structural: batches 1–5 harvested only the Met and Cleveland,
and these works are in the Louvre, Prado, Uffizi, Rijksmuseum, National
Gallery London, Alte Pinakothek and Kunsthistorisches. **Source them from
Wikimedia Commons by named work, not by artist category** — search the
specific painting, take the highest-resolution public-domain file.

Still out of copyright reach and not worth attempting: Picasso, Matisse after
1930, Kahlo, Hopper, Wyeth, Dalí, O'Keeffe, Rothko, Pollock, and every Indian
modern after Sher-Gil (Husain, Souza, Raza, Gaitonde).

### Regions still absent, and why that needs a decision

Africa, Oceania and pre-Columbian America have **no** representation. Do not
repeat the earlier reasoning that their museum holdings are "sculpture rather
than painting" — that was a fact about what two American museums digitised,
not about the traditions. Ethiopian illuminated manuscripts run continuously
from the sixth century, Mesoamerican codices are painting, and Aboriginal
Australian bark painting is among the longest continuous traditions anywhere.
The real obstacles are copyright (most Aboriginal work is contemporary and
rightly controlled by its communities) and repatriation-sensitive provenance.
Ethiopian manuscript painting and Mesoamerican codices are both reachable and
out of copyright. Raise this with the owner rather than deciding it silently.

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
| Wikimedia Commons | `https://commons.wikimedia.org/w/api.php` | The only route to the 20th century — see below. |

### Wikimedia Commons

The Met holds **nothing** post-1930 in the public domain, so the twentieth
century is only reachable through Commons, which records a licence per file.
It is also the only source for modern Indian painting — Ravi Varma, Sher-Gil
and the Tagores are in Indian collections, not American ones.

- **Use a descriptive User-Agent naming the tool and a contact.** A generic
  browser string is rejected outright.
- **Take dimensions from the API, never by downloading.** imageinfo returns
  exact width/height. Downloading 500 images to measure them earns a 429.
- **Thumbnails cannot be hand-constructed.** Take `thumburl` from the API with
  `iiurlwidth`; guessed sizes return 400 whatever number you pick.
- **Recurse one level into subcategories.** The bulk of a painter's work sits
  in `... by title` / `by year` / `by decade`, so a flat categorymembers query
  returns almost nothing for the best-covered artists.
- **Rate limits look exactly like broken data.** Three separate times a burst
  produced hundreds of "unreachable" images that were all fine at 3-4s
  spacing. Before concluding a source is broken, retest a few slowly.
- **Categories are far dirtier than museum classifications.** Expect in-situ
  mural photographs, gallery installation shots, newspaper clippings, book
  scans, detail crops, and objects merely *derived* from a painting (a
  Mondrian dress, a Red Fort photo filed under Tagore). Title filtering plus a
  contact sheet is mandatory here, not optional.
- **EXIF-rotated photos report swapped w/h.** A stored portrait that measures
  landscape is usually a phone snapshot of a painting in a gallery rather than
  a reproduction — check rather than just correcting the numbers.

**Licensing.** Accept only public domain, CC0 and CC-BY variants; record the
exact licence string. CC licences require visible credit, so fetch the file's
`Artist`/`Credit` fields for an attribution — the painter is long dead, so the
rights holder is whoever made the reproduction. `index.html` renders a credit
line for any work whose licence matches `cc[ -]?(by|0)`.

Prefer breadth of source — a batch drawn from one museum inherits that
museum's collecting bias.

**Always verify a new source loads as a plain `<img>` in a real browser before
building a batch on it.** An API that answers curl is not the same as an image
server that will serve a hotlinked page. Test with `new Image()` in Chrome,
not with curl, because the failure is header-based and curl can be made to
succeed where the browser cannot.

The National Gallery of Art has **no search API** — every documented endpoint
404s. It publishes open data as CSVs on GitHub instead, which would work but
is a bigger job than an API call. Existing NGA works in the collection came in
by another route; don't expect to query for more.

Filter traps that have each already cost a batch. All of them fail *silently* —
they return a thin result that looks like a small collection rather than a
broken query, which is why each one survived until someone noticed a famous
artist missing:

- **Strip diacritics on both sides when matching names.** Comparing
  `"velazquez"` against the Met's `"Velázquez"` rejected every match and lost
  *Juan de Pareja* and all the Zurbaráns. Same trap for Cézanne, Dürer, Miró.
- **The Met's `artistOrCulture=true` returns zero** for "Vincent van Gogh"
  (280 results without it). Do not use it.
- AIC's `classification_title` is the *medium* ("oil on canvas"), not a type.
  Filter on `artwork_type_title` instead.
- The Met's `classification` **is** "Paintings". The two APIs disagree; check
  the field before filtering on it.
- Scan depth matters. The Met's search returns prints and drawings before
  paintings, so a shallow ID scan finds almost nothing. Use 300+ and fetch
  objects concurrently or a batch takes hours.

**Write results to disk after every artist.** A harvest killed partway with
everything in memory loses the whole run.

Sanity check before moving on: if a household name returns zero, that is a bug
in the query, not a fact about the museum. Verify one by hand before accepting
it.

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
5. **Duplicate** — dedupe on **image URL**, not artist+title. Rembrandt painted
   several canvases titled "Self-Portrait" and the collection holds two
   genuinely different ones (Met 1660, NGA 1659); keying on title deletes one.
   Also watch for museum "parent" records that show several panels of a
   triptych at once while the individual panels exist as separate records —
   keep the panels, drop the composite.
6. **Not a fragment** — no detail shots, no single manuscript pages of pure
   text, no coins or fragments. It has to work as a full screen.

   Islamic and Persian manuscript searches return a great many pure-text pages
   with illuminated borders. They score *high* on ink coverage, so the ink
   filter cannot see them — but they are titled honestly, so a title pass
   removes them cleanly. Drop titles containing: `text page`, `calligraphy`,
   `persian couplets`, `persian verses:`, `persian prose`, `illuminated
   folio`, `preface`, `shamsa`, `colophon`, `frontispiece`. The same pass
   should collapse `(recto)`/`(verso)` records, which museums list as two
   objects for one physical folio.

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
4b. Score ink coverage and drop blank pages:
   `python3 .claude/skills/artss-batch/scripts/inkscore.py candidates.json --reject-below 0.15`
   Essential for manuscript-heavy sources. It catches blank paper, faint
   pencil sketches and objects photographed on a plain ground; it does **not**
   catch calligraphy pages with illuminated borders, which score high. Pair it
   with a keyword pass on the title and medium.

   **Set the floor by tradition, not by habit.** 0.15 suits South Asian
   miniatures. It is wrong for East Asia: at 0.15 it dropped 55 works and cut
   China from 73 to 31, because literati painting is deliberately monochrome
   ink on paper and the filter was scoring the tradition's defining quality as
   a defect. Use 0.05 there. Check what a floor removes before accepting it -
   if a whole region collapses, the filter is measuring the wrong thing.
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
- **Verify browser loads sequentially, not as a parallel burst.** Firing 76
  `new Image()` loads at once made 48 Cleveland URLs appear broken; the same
  URLs all loaded fine one at a time with a short pause. Cleveland's CDN
  throttles concurrent requests. A screensaver shows one painting at a time,
  so a parallel test measures something the app never does — and reports
  failures that are not real.
- `artworks.json` parses and every record has all required fields.
- Load the page locally (`python3 -m http.server`) and confirm the new works
  render in their assigned layout.
- Never report a count you have not checked against the file.
