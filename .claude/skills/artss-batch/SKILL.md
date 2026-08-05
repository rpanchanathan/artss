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

### Batches 7 and 8 are done — the collection is at 1028

Batch 7 added 104 celebrated works; batch 8 added 139 (97 more Western canon
plus 42 from Africa, Oceania and the pre-Columbian Americas). The target range
was 800–1000 and the collection is now slightly over it, by the owner's
decision to keep everything written rather than trim to land on the number.

**Africa, Oceania and pre-Columbian America are now represented** — the open
question recorded below was settled by the owner in favour of including them.
What went in: Ethiopian Gospel illumination and icons, ancient Egyptian tomb
painting and Books of the Dead, Fayum mummy portraits, Nubian frescoes from
Faras, Fante asafo flags, Mesoamerican codices, Teotihuacan and Maya painting,
colonial Andean Cusco School canvases, and Arnhem Land rock art.

The harvested pools are cached, gitignored, in `.work/` — `by_artist.json`
(23,807 Wikidata works across 72 artists), `matched.json`, `imginfo.json`,
`selected.json` and `region_info.json` (4,003 Commons files). Rebuilding them
costs about thirty minutes of API calls, so check there before re-harvesting.

**Deliberately excluded, and why** — repeat these decisions rather than
relitigating them. Contemporary Aboriginal bark and acrylic painting is in
copyright and controlled by the artists' communities. Wandjina imagery is
culturally restricted and was dropped even though Commons hosts it; the
Arnhem Land sites used (Ubirr, publicly interpreted and jointly managed) are
ones whose traditional owners have agreed may be photographed and shown.

Still genuinely thin: **Oceania has only three works**, all from Ubirr, because
in-situ rock art photography is mostly too low-contrast to read full-screen.
Māori and Hawaiian painted work returned nothing usable. **Bonnard is still
absent.** Sub-Saharan African rock art (San, Drakensberg) was tried and
rejected — the paintings are too faint in every available photograph.

### The earlier batch-8 plan (superseded)

Batch 7 added 104 celebrated works and took the collection to 889. Every work
and every artist named below is now in, except where noted. **Batch 8 needs
~110 more to reach 1000, and the candidates are already picked**: the Wikidata
harvest produced 300 filtered, licence-checked, deduped works and batch 7 used
104 of them. The remaining ~195 cover Ingres, Millet, Hogarth, Chardin,
Fragonard, Watteau, Canaletto, Rubens, Hals, Veronese, Arcimboldo, Bronzino,
Mantegna, El Greco, Dürer, Blake, Repin, Rousseau, Degas, Renoir, Cézanne,
Gauguin, Toulouse-Lautrec, Seurat, Schiele, Sargent, Grünewald, Böcklin,
Fuseli, Wright of Derby, Gainsborough, Constable, Vigée Le Brun and Duccio.
Rebuild that pool by rerunning the harvest described below — it takes about
fifteen minutes — then write notes for the ones worth having.

Two gaps batch 7 could not close. **Bonnard** is still absent entirely — his
only strong candidate was a plate given over to its gilt frame, so source him
deliberately rather than from a title search. **Seurat's Grande Jatte** is
unreachable: the painting is at the Art Institute, whose images 403 in a
browser, and Commons offers only Seurat's studies for it, several of which the
collection already holds.

### The brief batch 7 worked from (kept for batch 8)

The collection had 785 artworks and was missing the Mona Lisa, Las Meninas,
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

### Sourcing outside the museum APIs

For traditions with no open-access museum API, harvest Commons categories —
but **search for the category name, never guess it**. Fourteen of thirty
guessed names returned zero: it is "Ethiopian manuscripts" not "Ethiopian
illuminated manuscripts", "Papyrus of Hunefer" not "Book of the Dead of
Hunefer", "Burrungkuy (Nourlangie) rock art" not "Kakadu rock art".

Category contents lie about themselves more than museum records do, and only
the contact sheet catches it. In batch 8: the "Faras Cathedral" and "Faras
Gallery" categories are mostly photographs of the Warsaw gallery's interior and
loose architectural fragments, not the frescoes; every high-resolution
"Bonampak" file is a photograph of the building's exterior rather than the
murals inside it; "Tassili n'Ajjer" is maps, satellite imagery and colonial-era
expedition photographs with no rock art in the usable set. Budget for roughly a
third of a shortlist drawn this way to fail on sight.

Two sources that worked well and are worth going back to: the **Getty's MS 102
Ethiopian Gospel Book** and **Walters MS W850**, both fully digitised at high
resolution, and the **Fayum mummy portrait** categories, which hold hundreds of
flat, frontal, well-lit reproductions.

### Regions still absent, and why that needs a decision *(settled — see above)*

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
- **`iiurlwidth` is a request, not a promise.** Asking for 3000 returned 3840px
  files — Commons snaps to its own rendering buckets. The returned
  `thumbwidth`/`thumbheight` were also wrong for those files. Measure what is
  actually served; do not write the API's numbers into `w`/`h`.
- **A placeholder contact in the User-Agent gets 403 Forbidden.** The scripts
  ship with `set-your-contact@example.com` and refuse to run until it is
  replaced — without that guard they report every image as unreachable, which
  looks exactly like the two failure modes below. Wikimedia wants a real
  address, not merely a well-formed one.
- **A generic browser User-Agent is refused, and the refusal reads "Too many
  requests".** `upload.wikimedia.org` answered 89 of 104 image requests with
  429 and "your request does not comply with our robot policy" when the UA was
  a normal Chrome string, having served all 104 minutes earlier under the
  descriptive UA. So the 429 is UA classification, not rate. **`measure.py` and
  `sheet.py` both send a generic UA and both fan out in parallel, so both report
  near-total failure against Commons and neither failure is real.** Use
  `measure_seq.py` and `sheet_seq.py` for Commons batches.

**Finding a named work on Commons — go through Wikidata, not category names.**
Query the artwork entity for `P18`, which points at the canonical file. Traps,
all of which failed silently and each of which cost a rebuild:

- **Never match an artist by English label.** Wikidata spells Bruegel
  "Pieter Brueghel the Elder" and Goya "Francisco de Goya", so exact-label
  queries returned *zero* for both. Resolve the artist to a Q-id with
  `wbsearchentities` first, then query `wdt:P170 wd:Qxxxx`. This is the accent
  bug again in a new place.
- **Check what the Q-id actually resolved to.** Filtering search hits on the
  word "artist" in the description matched "Spanish recording *artist*", so
  Raphael resolved to a 1960s pop singer and returned no paintings. Fetch the
  entity's description and confirm it names a painter before trusting it.
- **Matching a title returns copies and other media.** "Mona Lisa" also returns
  the Prado copy. Worse, the *same title* returns prints of the painting: the
  first hit for The Potato Eaters was van Gogh's lithograph and for The Return
  of the Prodigal Son was Rembrandt's etching. A tie-break on shortest title
  actively prefers these. Only the contact sheet catches it.
- **`P31/P279*` is slow enough to look hung** — around 90s per artist. Use a
  direct `P31` against an explicit `VALUES ?cls` list of painting/drawing/print
  classes and batch several artists per query with `VALUES ?c`; that runs about
  five artists per ten seconds.
- **A partly-filled cache from an earlier query shape is invisible.** Five
  artists cached under a truncated `LIMIT 400` label query survived the rewrite
  and silently had no Mona Lisa, Scream or Starry Night in them. When the query
  changes, drop the cache rather than skipping what is already there.
- **Never name a working file after a stdlib module.** A local `select.py`
  shadowed `select` and broke `urllib` with an unrelated-looking traceback.
- **Build records from the filtered pool, not from the raw hit list.** Keying
  the raw matches by (artist, title) and taking the first entry silently
  substituted a smaller duplicate file for ten works in batch 8 — Millet's
  Sower arrived at 759×1200 instead of 6395×8000. The pool's scored choice must
  win; the raw list is a fallback only. Batch 7 shipped five works this way
  before it was caught, including **The Raft of the Medusa as Géricault's oil
  sketch rather than the Louvre painting**, which the contact sheet passed
  because a sketch of the Raft still looks like the Raft.
- **A title match can return a different medium of the same subject.** The
  first hit for "Jane Avril" was a preparatory drawing, not the 1893 poster the
  note described. Check the medium against what you wrote, not just the title.

**Deduplicating against the collection.** Two rules, learned the hard way:

- **Do not take the last word of the artist field as the surname.** The
  collection stores "El Greco (Domenikos Theotokopoulos)", which keys as
  *theotokopoulos* and therefore never matched a new "El Greco" — so View of
  Toledo and Laocoön were both added a second time despite already being held
  from the Met and the NGA. Strip parenthetical real names before keying.
- **A shared artist and title is not proof of a duplicate.** An automated sweep
  on that basis deleted Rembrandt's 1659 NGA self-portrait (the collection
  legitimately holds it alongside the Met's 1660) and one of two different Kano
  Shōei screens. Cluster them, then look at the images before removing anything.

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
   **For a Commons batch use `measure_seq.py` instead** — `measure.py`'s
   parallel fetch with a generic UA reports almost the whole batch as
   unreachable when none of it is.
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
   (`sheet_seq.py` for Commons) then Read the output image. Look at it. This is
   where mount-dominated scrolls, damaged works, near-duplicate compositions and
   bad crops get caught. Do not skip this; it is one image and it catches what
   no filter can.

   In batch 7 it caught five of 105 that every automated check had passed: the
   Potato Eaters *lithograph* and the Prodigal Son *etching* standing in for the
   paintings, the National Gallery's Execution of Maximilian, which is
   fragments remounted with bare canvas between them, a Rouen Cathedral scanned
   so faded it read as blank, and a Bonnard whose gilt frame took a quarter of
   the plate. Nothing but looking would have found any of them.
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
