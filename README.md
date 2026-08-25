# artss — an art screensaver

**Live: https://artss.pages.dev/**

Also on GitHub Pages at `https://rpanchanathan.github.io/artss/`, but send people the
`pages.dev` link. GitHub gives an account one `<user>.github.io` subdomain shared by every
repo, so one bad page takes them all down — which happened. Cloudflare gives each project
its own subdomain (`pages.dev` is on the Public Suffix List), so projects can't poison each
other. See `~/code/wiki/incidents/2026-08-18-github-pages-safebrowsing-flag.md`.

Open it on any screen (TV, laptop, tablet), press F11 / hit fullscreen, and leave it running.
It cycles through 1,028 paintings, each shown large with a short note on what was going on when
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
| s | ambient drone on / off |
| g _or_ Enter | studio view on / off |

Arrow keys mean a TV remote works as-is. The numeric keypad works as arrows too (with Num Lock
off, numpad 8/4/6/2 act as ↑/←/→/↓).

## On-screen controls

For touch screens and any setup where a keyboard isn't handy, everything above is also available
without keys:

- A **gear (⚙) button, top-left** opens a *Choose what to show* menu — pick an artist or a
  style/movement/period from lists (no typing a substring), and choose the layout (Auto / Split
  view / Full frame). It writes the same URL parameters below and reloads, so there is one
  filtering path whether the choice came from a typed URL or a tap.
- A **grid (▦) button, next to the gear** opens **Studio** — a page of tiles, one per
  ready-made collection, each with a painting from it and a count. Use it when you want to
  pick by looking rather than by knowing what to type. The tiles are built from the collection
  itself (artists with 8+ works, movements and regions with 20+, and every period), so they
  stay right as the collection grows — there is no hand-maintained list.
  Tap tiles to pick them and **Play** to start; tapping a picked tile again unpicks it.
  Picking several plays them **together** — van Gogh *plus* Sher-Gil *plus* ukiyo-e is all
  67 works, not the none that are all three. Reopening the studio mid-show shows what is
  playing, so you can add a collection to it rather than start again.
- A **control bar along the bottom** mirrors the keys: prev · less-often · pause · more-often ·
  skip. Both the gear and the bar fade out while idle and reappear on any pointer or touch.

`m` or Esc also open/close the menu; `g`, Enter or Esc do the same for the studio (Enter is
there because a TV remote's d-pad sends no letters). Inside the studio the arrow keys move
between tiles, Enter picks and unpicks, and Down from the last row lands on **Play** — so a
d-pad drives the whole thing. Inside the studio
the arrow keys move between tiles and Enter picks one, so a TV remote's d-pad drives it without
a pointer.

The ↑/↓ frequency preference is stored per device in `localStorage`, along with a seen count —
paintings you've watched a lot drift back in the rotation, ones you nudge up come round sooner.
Nothing is ever excluded outright.

## Sound

Off by default. `s`, or the **Sound** row in the ⚙ menu, turns on an ambient drone — a low bed
that sits under the paintings without ever becoming music you'd listen to.

It is synthesised in the browser rather than played from a file, so there's no track to license
and, more to the point, nothing loops. Five partials over a low root each fade in and out on
their own slow cycle (23s, 35s, 46s and so on — no common multiple, so they never all swell
together twice), and every two to four minutes the root glides to another note of a pentatonic
set over fourteen seconds. Pitched at D2–B2 because TV speakers roll off below about 150Hz and
a drone the television can't reproduce is just a silent CPU load.

The preference is stored per device. One catch on the TV: browsers won't start audio until
they've seen a real input event, and the ADB launch below supplies none — so after launching,
send any keypress (`adb shell input keyevent 52`) and the drone comes up. `?drone=1` turns it on
from the URL, still subject to that first keypress.

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

Either tap the **⚙ menu** or the **▦ studio** (see above) and pick from lists, or set the
parameters directly. Every artwork carries tags for region, century and (where it belongs to
one) movement.

There are two filtering moods, and they are opposites:

**Narrowing** — every condition must hold. This is what the ⚙ menu writes.

- `?artist=gogh` — substring match on artist name
- `?tags=impressionism` — single tag
- `?tags=impressionism,france` — all listed tags must match

**Widening** — a union; a work needs to match any one of the collections listed. This is what
the ▦ studio writes when you pick several tiles.

- `?sets=artist:Claude Monet|tag:baroque` — Monet *or* anything baroque
- `?sets=tag:ukiyo-e` — one collection, same as `?tags=ukiyo-e`

`sets` and `artist`/`tags` say opposite things, so they don't combine: whichever you used last
is the one in the URL, and the menu and the studio each clear the other's parameters.

Tags in use include `impressionism`, `post-impressionism`, `dutch-golden-age`, `baroque`,
`renaissance`, `romanticism`, `realism`, `fauvism`, `ukiyo-e`, `south-asia`, `china`, `japan`,
`persia`, `france`, `italy`, and `17th-century` through `20th-century`. Movement tags come from
an explicit artist lookup rather than being inferred, so a work without a movement tag simply
isn't classified — it hasn't been guessed at.

Outside Europe and Asia the tags name the tradition rather than a movement: `africa`,
`americas` and `oceania` at the top level, then `ethiopia`, `ancient-egypt`, `roman-egypt`,
`nubia`, `ghana`, `mesoamerica`, `maya`, `andes`, `aboriginal-australia`, plus `manuscript`
and `rock-art` for the medium. Works older than the era covered by the century tags carry
`ancient` instead.

## Other URL options

- `?intro=20&scene=30&bigDeal=30&outro=45` — phase durations in seconds
- `?shuffle=0` — play in file order instead of shuffled
- `?drone=1` — start with the ambient drone on (`?drone=0` forces it off)

## On the TV

The Android TV (TCL, `10.0.0.32`) runs it in TV Bro. Launch and unmute:

```
adb connect 10.0.0.32:5555
adb -s 10.0.0.32:5555 shell am start -a android.intent.action.VIEW \
  -d "https://artss.pages.dev/" com.phlox.tvwebbrowser
sleep 8 && adb -s 10.0.0.32:5555 shell input keyevent 52   # any key; unlocks audio
```

The remote's d-pad covers the keyboard controls and the ▦ studio (its tiles are d-pad
navigable), but the ⚙ menu needs a pointer for its dropdowns. Three ways to get one: a USB keyboard or mouse in the TV's own USB port (it reports `android.hardware.usb.host`),
a Bluetooth one paired to the TV, or — with no hardware at all — drive it from the Mac:

```
scrcpy -s 10.0.0.32:5555 --no-audio
```

That mirrors the TV into a window and forwards the Mac's mouse and keyboard to it, so the menu
is clickable from the desk. Note the panel is genuinely 720p (`wm size` reports 1280×720 and
offers no other mode), which is the ceiling on how much of the source images' detail ever lands.

Example: `https://artss.pages.dev/?tags=post-impressionism&intro=10&scene=20`

## What's in it

- `index.html` — the whole app. No build step, no dependencies.
- `artworks.json` — 1,028 entries spanning 372 artists, from sixth-century Ethiopian
  Gospel illumination and ancient Egyptian tomb painting to Matisse. Images are hotlinked
  from six museums' open-access collections — Cleveland Museum of Art, The Met, Rijksmuseum,
  Smithsonian, National Gallery of Art DC and the Victoria & Albert Museum — and from
  Wikimedia Commons, which is the only route to works in the Louvre, Prado, Uffizi and
  Kunsthistorisches, and to everything outside the Western canon.
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
- **Wikimedia images**: fetch them one at a time with a descriptive User-Agent naming a
  contact. A normal browser User-Agent gets refused as a robot, and the refusal arrives as
  a 429 that reads like rate limiting — so a parallel fetch reports an entire batch as
  broken when none of it is. Use `measure_seq.py` and `sheet_seq.py` for Commons.

The skill file in `.claude/skills/artss-batch/` carries the rest: the traps each source has
already cost a batch, and the sourcing decisions — including which traditions were left out
of the non-Western material on copyright or cultural-restriction grounds, and why.

## Running locally

```
python3 -m http.server 8000
```

Then open http://localhost:8000. Opening `index.html` as a `file://` URL won't work — the
`artworks.json` fetch needs a server.

## Deploying

Cloudflare Pages, from the repo root:

```
CLOUDFLARE_API_TOKEN=$CLOUDFLARE_PAGES_TOKEN \
  npx wrangler pages deploy . --project-name=artss --branch=main --commit-dirty=true
```

The token has to be inlined — wrangler does not read `~/.env`, and the variable literally
named `CLOUDFLARE_API_TOKEN` there is a Workers-only token that fails every Pages call.

GitHub Pages still deploys on push, so both stay current.
