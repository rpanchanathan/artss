# artss — an art screensaver

**Live: https://rpanchanathan.github.io/artss/**

Open it on any screen (TV, laptop, tablet), press F11 / hit fullscreen, and leave it running.
It cycles through 684 paintings, each shown large with a short note on what was going on when
it was painted and why it matters.

## How a slide plays

Each painting runs through four phases:

1. **Intro** (20s) — painting alone, no text
2. **The Scene** (30s) — title appears, plus context on when and where it was painted
3. **Why It's a Big Deal** (30s) — the context panel swaps for the significance note
4. **Outro** (45s) — text clears, painting alone again, unobstructed

## Controls

| Key | Action |
|-----|--------|
| Space | pause / resume |
| ← | previous painting |
| → | skip to next phase |
| ↑ / ↓ (or + / −) | show this painting more / less often |

Arrow keys mean a TV remote works as-is.

The ↑/↓ frequency preference is stored per device in `localStorage`, along with a seen count —
paintings you've watched a lot drift back in the rotation, ones you nudge up come round sooner.
Nothing is ever excluded outright.

## Layout

A 16:9 screen and a portrait painting don't agree, and most paintings are portrait. Rather
than letterbox them into a narrow column with black bars either side, each slide picks its
own layout from the artwork's aspect ratio:

- **Landscape** (ratio ≥ 1.15) — fills the screen, text overlaid along the bottom.
- **Portrait** (0.5–1.15) — painting takes the full screen height on the left, text sits in a
  panel on the right. Half of a 16:9 screen is 8:9, which is close to the shape of most
  portrait paintings, so they end up larger than they would fitted whole.
- **Ultra-tall** (< 0.5, hanging scrolls) — blown up past the screen and panned slowly
  downward, which is how you'd read a scroll and shows far more detail than shrinking it.

`?layout=fit` restores plain letterboxing; `?layout=split` forces the split view on everything.

## Filtering

Every artwork carries tags for region, century and (where it belongs to one) movement.

- `?artist=gogh` — substring match on artist name
- `?tags=impressionism` — single tag
- `?tags=impressionism,france` — all listed tags must match

Tags in use include `impressionism`, `post-impressionism`, `dutch-golden-age`, `baroque`,
`renaissance`, `romanticism`, `realism`, `ukiyo-e`, `south-asia`, `china`, `japan`, `persia`,
`france`, `italy`, and `17th-century` through `20th-century`. Movement tags come from an
explicit artist lookup rather than being inferred, so a work without a movement tag simply
isn't classified — it hasn't been guessed at.

## Other URL options

- `?intro=20&scene=30&bigDeal=30&outro=45` — phase durations in seconds
- `?shuffle=0` — play in file order instead of shuffled

Example: `https://rpanchanathan.github.io/artss/?tags=post-impressionism&intro=10&scene=20`

## What's in it

- `index.html` — the whole app. No build step, no dependencies.
- `artworks.json` — 684 entries. Images are hotlinked from six museums' open-access
  collections: Cleveland Museum of Art, The Met, Rijksmuseum, Smithsonian, National Gallery
  of Art DC, and the Victoria & Albert Museum.
- `.claude/skills/artss-batch/` — the workflow and scripts for adding to the collection.

Each entry looks like:

```json
{
  "id": "met-436535",
  "title": "Wheat Field with Cypresses",
  "artist": "Vincent van Gogh",
  "artistBio": "Dutch, Zundert 1853–1890 Auvers-sur-Oise",
  "year": "1889",
  "medium": "Oil on canvas",
  "image": "https://images.metmuseum.org/...jpg",
  "sourceUrl": "https://www.metmuseum.org/art/collection/search/436535",
  "museum": "The Met",
  "license": "public-domain",
  "w": 4000, "h": 3186,
  "tags": ["post-impressionism", "france", "19th-century", "landscape-format"],
  "sceneContext": "Painted from the window and grounds of the asylum at Saint-Rémy...",
  "whyBigDeal": "Van Gogh sold almost nothing while alive..."
}
```

`w` and `h` are the image's real measured dimensions, not whatever the museum API claims —
the layout decision depends on them, so they're verified by fetching each image.

## Adding artworks

```
python3 .claude/skills/artss-batch/scripts/stats.py      # current shape vs targets
python3 .claude/skills/artss-batch/scripts/validate.py   # structure, aspect, quality floor
```

Two things that will bite you if you add works by hand:

- **Cleveland URLs**: use `_print.jpg`, never `_web.jpg`. The `_web` derivative is 666×900
  where `_print` is 2515×3400. The V&A's IIIF URLs default to `/full/800,/` — use
  `/full/full/`. `validate.py` errors on both.
- **Horizontal handscrolls**: museum mid-size derivatives cap the *long* edge, so a
  120000×2834 scroll arrives as 3400×80 with its height destroyed and no usable middle size
  available. Anything outside a 0.33–3.0 aspect ratio is rejected.

## Running locally

```
python3 -m http.server 8000
```

Then open http://localhost:8000. Opening `index.html` as a `file://` URL won't work — the
`artworks.json` fetch needs a server.
