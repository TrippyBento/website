# Trippy Bento Studio — pixel wordmark kit

Everything is generated from pixel maps in `build.py`. There are no binary
source files to keep in sync — edit the map, re-run, all outputs regenerate.

```
build.py        generates every PNG, SVG, and the APNG
wordmark.html   standalone animated preview, open it in any browser
out/            generated assets (safe to delete and rebuild)
```

## Rebuilding

```
pip install pillow
python3 build.py
```

## What's in `out/`

```
png/{plum,ink}/tbs-{horizontal,stacked,short,icon,type-only}@{1,2,4,8}x.png
png/{plum,ink}/app-icon/icon-{16,32,64,128,256,512}.png
svg/{plum,ink}/tbs-*.svg
anim/tbs-wordmark.apng
anim/frames/frame-000.png … frame-071.png
```

Everything is transparent PNG. The SVGs are one `<rect>` per pixel run with
`shape-rendering="crispEdges"` — they scale to any size without blurring, which
makes them the right choice for print and for oversized web headers.

## The two outline variants

| Variant | Outline | Use it for |
|---|---|---|
| `plum` | `#2e1b47` | The default. Matches the original icon. Web, social, itch. |
| `ink` | `#2e2013` | Anywhere the mark sits on Angkor art — this is Angkor's outline color, so the logo doesn't fight the game's line weight. |

Pick one per surface and don't mix them in a single composition.

## The three lockups

- **horizontal** (101×22) — the default. Steam capsule, itch header, footer, docs.
- **stacked** (71×37) — square-ish slots. Splash screens, Discord, avatars.
- **short** (101×19) — drops "STUDIO". Use when width is tight; the name is the
  memorable part and "STUDIO" only adds width.
- **type-only** (71×18) — for when the box already appears elsewhere on screen.
- **icon** (24×19) — the box alone.

## Rules

**Scale by whole numbers only.** 2×, 3×, 4×, 8×. A 1.5× scale puts pixel edges
on half-pixel boundaries and the outline goes soft — this is the single fastest
way to make pixel art look cheap. Every PNG here is an integer multiple, and the
SVGs use `crispEdges` so they stay hard at any size.

**Never re-typeset the name.** The letterforms are a custom 5×7 face defined in
`build.py` under `FONT`. Setting "Trippy Bento" in a downloaded pixel font will
not match, because the grid and the stroke weight won't agree with the box.

**Minimum sizes.** Horizontal lockup: don't go below 1× (101px wide) — below
that the 1px letter strokes drop out. Icon alone: 16px is the floor, and at 16px
the face is what survives, so never crop it out.

**Clear space.** Leave at least 4 grid cells (4px at 1×, 32px at 8×) on all
sides. Don't put the mark on a busy background — it has no container of its own.

## Palette

| Role | Hex |
|---|---|
| Outline (plum) | `#2e1b47` |
| Outline (ink) | `#2e2013` |
| Box body | `#a86fd0` |
| Box rim | `#c99ae8` |
| Box shadow | `#7d4aa6` |
| Rice | `#fdfdff` |
| Shrimp | `#e8453c` / `#ff7a63` |
| Tempura | `#f2a13a` |
| Veg | `#4fae5a` / `#388144` |
| Cheek | `#ff8fbe` |

## The animation

3 seconds, 24fps, 72 frames. The box lands with a one-pixel squash, then the
letters tile in left to right — each letter arrives one pixel high and settles.
The eyes blink once near the end. The purple drifts ±0.02 in hue across the
loop, which reads as a very slow shimmer rather than a visible color change.

`anim/tbs-wordmark.apng` loops forever and keeps its alpha channel. If you need
another format, `anim/frames/` holds the raw 4× PNGs:

```
ffmpeg -framerate 24 -i frames/frame-%03d.png -c:v libvpx-vp9 -pix_fmt yuva420p tbs.webm
ffmpeg -framerate 24 -i frames/frame-%03d.png -vf palettegen palette.png
ffmpeg -framerate 24 -i frames/frame-%03d.png -i palette.png -lavfi paletteuse tbs.gif
```

Avoid GIF where you can — its 1-bit alpha puts a hard fringe on the outline.

Steam does not accept animated logos in any store slot. The animation is for the
Angkor splash screen, trailers, and social clips.

## Changing things

- **New text** — add glyphs to `FONT` in `build.py` (5 wide, 7 tall, `"1"` is on).
- **New lockup** — add a `lockup_*` function and register it in `LOCKUPS`.
- **New palette** — add an entry to `PALETTES`; every output regenerates for it.
- **Retiming the animation** — the constants sit together above `animation_frame`.
