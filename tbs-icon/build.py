#!/usr/bin/env python3
"""
Trippy Bento Studio - pixel wordmark asset builder.

Everything is generated from the pixel maps below. Edit the maps or the
palette, re-run, and every PNG / SVG / APNG regenerates consistently.

    python3 build.py

Requires Pillow:  pip install pillow
Output lands in ./out/
"""

import colorsys
import os

from PIL import Image

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")

# ---------------------------------------------------------------- palette

BASE = {
    "K": "#2e1b47",  # outline
    "P": "#a86fd0",  # box body
    "L": "#c99ae8",  # box rim highlight
    "D": "#7d4aa6",  # box body shadow
    "W": "#fdfdff",  # rice
    "S": "#fdfdff",  # rice / eye sparkle
    "N": "#2e1b47",  # nori
    "R": "#e8453c",  # shrimp
    "r": "#ff7a63",  # shrimp highlight
    "O": "#f2a13a",  # tempura
    "E": "#4fae5a",  # veg
    "e": "#388144",  # veg shadow
    "c": "#ff8fbe",  # cheek
    "B": "#241634",  # eye
    "T": "#2e1b47",  # wordmark type
}

# "ink" swaps the plum-black outline for Angkor's brown-black (#2e2013)
# so the studio mark sits cleanly on top of game art.
INK_OVERRIDES = {"K": "#2e2013", "N": "#2e2013", "B": "#2e2013", "T": "#2e2013"}

PALETTES = {
    "plum": BASE,
    "ink": {**BASE, **INK_OVERRIDES},
}

# The purple keys are the ones that drift during the animation.
DRIFT_KEYS = ("P", "L", "D")

# ---------------------------------------------------------------- pixel maps

# 24 x 19 bento box icon
ICON = [
    "........................",
    ".............RR.........",
    "............RrrR........",
    "...KKKK.....RrrR...EEE..",
    "..KWWWWK...RRrrRR.EeEEE.",
    ".KWWSWWWK..RrrrrR.EEEEe.",
    ".KWWWWWWWK.RRrrRR.EEEEe.",
    ".KWWWWWWWK.RrrrR.OOEEEE.",
    ".KNNNNNNNK.RRRR.OOOOOOO.",
    "KKKKKKKKKKKKKKKKKKKKKKKK",
    "KLLLLLLLLLLLLLLLLLLLLLLK",
    "KPPPPPPPPPPPPPPPPPPPPPPK",
    "KPPPPBBBPPPPPPPPPBBBPPPK",
    "KPcPPBSBPPPKKPPPPBSBPcPK",
    "KPcPPBBBPPPKKPPPPBBBPcPK",
    "KPPPPPPPPPPPPPPPPPPPPPPK",
    "KDDDDDDDDDDDDDDDDDDDDDDK",
    "KKKKKKKKKKKKKKKKKKKKKKKK",
    "..KK...............KK...",
]

ICON_W, ICON_H = 24, 19

# Rows on which the eyes live, used by the blink frame.
EYE_ROWS = (12, 13, 14)

# 5x7 pixel face. Only the glyphs the wordmark needs.
FONT = {
    "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    "I": ["11111", "00100", "00100", "00100", "00100", "00100", "11111"],
    "P": ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
    "Y": ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
    "B": ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    "N": ["10001", "11001", "10101", "10101", "10011", "10001", "10001"],
    "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    "U": ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
    "D": ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    " ": ["00000"] * 7,
}

ADVANCE = 6  # 5px glyph + 1px letter gap
GLYPH_H = 7


def text_width(s):
    return len(s) * ADVANCE - 1


# ---------------------------------------------------------------- canvas

class Canvas:
    """A grid of palette keys. None means transparent."""

    def __init__(self, w, h):
        self.w, self.h = w, h
        self.px = [[None] * w for _ in range(h)]

    def set(self, x, y, key):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.px[y][x] = key

    def blit_icon(self, ox, oy, blink=False):
        for y, row in enumerate(ICON):
            for x, key in enumerate(row):
                if key == ".":
                    continue
                if blink and y in EYE_ROWS and key in ("B", "S"):
                    # During a blink the eyes collapse to a single dark line.
                    if y == EYE_ROWS[1]:
                        self.set(ox + x, oy + y, "B")
                    continue
                self.set(ox + x, oy + y, key)

    def blit_text(self, s, ox, oy, key="T", limit=None, nudge=None):
        for i, ch in enumerate(s):
            if limit is not None and i >= limit:
                break
            glyph = FONT.get(ch)
            if not glyph:
                continue
            dy = nudge(i) if nudge else 0
            for gy in range(GLYPH_H):
                for gx in range(5):
                    if glyph[gy][gx] == "1":
                        self.set(ox + i * ADVANCE + gx, oy + gy + dy, key)


# ---------------------------------------------------------------- lockups

def lockup_horizontal(blink=False):
    c = Canvas(101, 22)
    c.blit_icon(0, 2, blink=blink)
    c.blit_text("TRIPPY BENTO", 30, 4)
    c.blit_text("STUDIO", 30, 15)
    return c


def lockup_short(blink=False):
    c = Canvas(101, 19)
    c.blit_icon(0, 0, blink=blink)
    c.blit_text("TRIPPY BENTO", 30, 6)
    return c


def lockup_stacked(blink=False):
    c = Canvas(71, 37)
    c.blit_icon(23, 0, blink=blink)
    c.blit_text("TRIPPY BENTO", 0, 21)
    c.blit_text("STUDIO", 18, 30)
    return c


def lockup_icon(blink=False):
    c = Canvas(ICON_W, ICON_H)
    c.blit_icon(0, 0, blink=blink)
    return c


def lockup_type_only():
    c = Canvas(71, 18)
    c.blit_text("TRIPPY BENTO", 0, 0)
    c.blit_text("STUDIO", 18, 11)
    return c


LOCKUPS = {
    "horizontal": lockup_horizontal,
    "short": lockup_short,
    "stacked": lockup_stacked,
    "icon": lockup_icon,
}

# ---------------------------------------------------------------- renderers

def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def drift(hex_color, amount):
    """Rotate hue by `amount` (0-1). Used for the slow purple shimmer."""
    r, g, b = [v / 255 for v in hex_to_rgb(hex_color)]
    hh, ll, ss = colorsys.rgb_to_hls(r, g, b)
    r, g, b = colorsys.hls_to_rgb((hh + amount) % 1.0, ll, ss)
    return (round(r * 255), round(g * 255), round(b * 255))


def to_image(canvas, palette, scale=1, hue=0.0):
    img = Image.new("RGBA", (canvas.w, canvas.h), (0, 0, 0, 0))
    px = img.load()
    cache = {}
    for y in range(canvas.h):
        for x in range(canvas.w):
            key = canvas.px[y][x]
            if key is None:
                continue
            ck = (key, hue)
            if ck not in cache:
                col = palette[key]
                cache[ck] = (drift(col, hue) if (hue and key in DRIFT_KEYS)
                             else hex_to_rgb(col)) + (255,)
            px[x, y] = cache[ck]
    if scale != 1:
        img = img.resize((canvas.w * scale, canvas.h * scale), Image.NEAREST)
    return img


def to_svg(canvas, palette):
    """One rect per horizontal run of identical pixels."""
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {canvas.w} {canvas.h}" '
        f'width="{canvas.w}" height="{canvas.h}" shape-rendering="crispEdges">'
    ]
    for y in range(canvas.h):
        x = 0
        while x < canvas.w:
            key = canvas.px[y][x]
            if key is None:
                x += 1
                continue
            run = 1
            while x + run < canvas.w and canvas.px[y][x + run] == key:
                run += 1
            parts.append(
                f'<rect x="{x}" y="{y}" width="{run}" height="1" fill="{palette[key]}"/>'
            )
            x += run
    parts.append("</svg>")
    return "\n".join(parts)


# ---------------------------------------------------------------- animation

FPS = 24
TOTAL_FRAMES = 72

L1, L2 = "TRIPPY BENTO", "STUDIO"
ICON_IN = 4          # frame the box lands
L1_START, L1_STEP = 10, 2
L2_START, L2_STEP = 36, 2
BLINK = range(58, 61)


def animation_frame(f):
    """Build the horizontal lockup as it looks on frame `f`."""
    c = Canvas(101, 22)

    if f >= ICON_IN:
        # 2-frame squash on landing: box sits 1px low, then settles.
        oy = 3 if f < ICON_IN + 2 else 2
        c.blit_icon(0, oy, blink=(f in BLINK))

    def reveal(text, ox, oy, start, step):
        shown = 0
        for i in range(len(text)):
            if f >= start + i * step:
                shown = i + 1
        if not shown:
            return
        # Each letter lands 1px high on its first frame, then settles.
        def nudge(i):
            return -1 if f == start + i * step else 0
        c.blit_text(text, ox, oy, limit=shown, nudge=nudge)

    reveal(L1, 30, 4, L1_START, L1_STEP)
    reveal(L2, 30, 15, L2_START, L2_STEP)
    return c


def hue_at(f):
    """Seamless ±0.02 hue drift across the loop."""
    import math
    return 0.02 * math.sin(2 * math.pi * f / TOTAL_FRAMES)


# ---------------------------------------------------------------- main

def write(path, data, mode="w"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, mode) as fh:
        fh.write(data)
    print("  " + os.path.relpath(path, OUT))


def main():
    os.makedirs(OUT, exist_ok=True)
    print("building assets ->", OUT)

    for pname, palette in PALETTES.items():
        print(f"\n[{pname}]")
        for lname, fn in LOCKUPS.items():
            canvas = fn()
            for scale in (1, 2, 4, 8):
                img = to_image(canvas, palette, scale)
                p = os.path.join(OUT, "png", pname, f"tbs-{lname}@{scale}x.png")
                os.makedirs(os.path.dirname(p), exist_ok=True)
                img.save(p)
            p = os.path.join(OUT, "svg", pname, f"tbs-{lname}.svg")
            write(p, to_svg(canvas, palette))

        # type-only mark, for when the box already appears elsewhere
        canvas = lockup_type_only()
        for scale in (1, 2, 4, 8):
            img = to_image(canvas, palette, scale)
            p = os.path.join(OUT, "png", pname, f"tbs-type-only@{scale}x.png")
            os.makedirs(os.path.dirname(p), exist_ok=True)
            img.save(p)
        write(os.path.join(OUT, "svg", pname, "tbs-type-only.svg"),
              to_svg(canvas, palette))

        # square app / favicon sizes, integer-scaled and centred
        for size in (16, 32, 64, 128, 256, 512):
            base = lockup_icon()
            k = max(1, min(size // ICON_W, size // ICON_H))
            img = to_image(base, palette, k)
            sq = Image.new("RGBA", (size, size), (0, 0, 0, 0))
            sq.paste(img, ((size - img.width) // 2, (size - img.height) // 2))
            p = os.path.join(OUT, "png", pname, "app-icon", f"icon-{size}.png")
            os.makedirs(os.path.dirname(p), exist_ok=True)
            sq.save(p)

    # animation: frames + APNG, plum palette at 4x
    print("\n[animation]")
    palette = PALETTES["plum"]
    frames = []
    fdir = os.path.join(OUT, "anim", "frames")
    os.makedirs(fdir, exist_ok=True)
    for f in range(TOTAL_FRAMES):
        img = to_image(animation_frame(f), palette, 4, hue=hue_at(f))
        img.save(os.path.join(fdir, f"frame-{f:03d}.png"))
        frames.append(img)
    frames[0].save(
        os.path.join(OUT, "anim", "tbs-wordmark.apng"),
        save_all=True,
        append_images=frames[1:],
        duration=int(1000 / FPS),
        loop=0,
        disposal=2,
        default_image=False,
    )
    print(f"  anim/tbs-wordmark.apng  ({TOTAL_FRAMES} frames @ {FPS}fps)")
    print(f"  anim/frames/            ({TOTAL_FRAMES} PNGs, 4x)")

    print("\ndone.")


if __name__ == "__main__":
    main()
