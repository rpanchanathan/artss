# artss — an art screensaver

**Live: https://rpanchanathan.github.io/artss/**

Open it on any screen (TV, laptop, tablet), press F11 / hit fullscreen, and leave it running.
It cycles through 310 paintings, each shown large with a short note on what was going on when
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

## URL options

Append to the live link:

- `?intro=20&scene=30&bigDeal=30&outro=45` — phase durations in seconds
- `?shuffle=0` — play in file order instead of shuffled
- `?layout=split` — split-screen layout (painting one side, text the other)

Example: `https://rpanchanathan.github.io/artss/?intro=10&scene=20&bigDeal=20&outro=20`

## What's in it

- `index.html` — the whole app. No build step, no dependencies.
- `artworks.json` — 310 entries. Images are hotlinked from the Met's open-access collection.

Each entry looks like:

```json
{
  "id": 436535,
  "title": "Wheat Field with Cypresses",
  "artist": "Vincent van Gogh",
  "artistBio": "Dutch, Zundert 1853–1890 Auvers-sur-Oise",
  "year": "1889",
  "medium": "Oil on canvas",
  "image": "https://images.metmuseum.org/...jpg",
  "sceneContext": "Painted from the window and grounds of the asylum at Saint-Rémy...",
  "whyBigDeal": "Van Gogh sold almost nothing while alive..."
}
```

To add a painting, append an object in that shape to `artworks.json` and push — GitHub Pages
serves the change within a minute.

## Running locally

```
python3 -m http.server 8000
```

Then open http://localhost:8000. Opening `index.html` as a `file://` URL won't work — the
`artworks.json` fetch needs a server.
