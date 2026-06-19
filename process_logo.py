"""One-shot processor for the FieldPoint logo.

Reads the edited source logo (Downloads or wherever you point it),
produces two outputs in assets/brand/:
  - logo.png        : transparent background, original colors
  - logo-light.png  : transparent background, dark-green pixels recolored to cream

Run after replacing the source artwork to refresh both variants in one go.
"""
from PIL import Image
import os
import sys

SRC = sys.argv[1] if len(sys.argv) > 1 else \
    r"C:/Users/Ben/Downloads/FieldPoint Advisors Logo - Edited.png"
OUT_DIR = "assets/brand"
TRANSPARENT_OUT = os.path.join(OUT_DIR, "logo.png")
LIGHT_OUT = os.path.join(OUT_DIR, "logo-light.png")

CREAM = (246, 241, 230)
WHITE_THRESHOLD = 240        # pixels with R, G, B all >= this become transparent
NEAR_WHITE_FEATHER = 220     # pixels close to white get partial alpha (smooths edges)
DARK_BRIGHTNESS = 130        # pixels with avg < this become cream (for light variant)

os.makedirs(OUT_DIR, exist_ok=True)
img = Image.open(SRC).convert("RGBA")
w, h = img.size
print(f"Source: {SRC}  ({w}x{h}, mode RGBA)")

# Pass 1 — strip white background
transparent = img.copy()
px = transparent.load()
made_transparent = 0
softened = 0
for y in range(h):
    for x in range(w):
        r, g, b, a = px[x, y]
        m = min(r, g, b)
        if m >= WHITE_THRESHOLD:
            px[x, y] = (r, g, b, 0)
            made_transparent += 1
        elif m >= NEAR_WHITE_FEATHER:
            # Linear feather: closer to white = more transparent
            new_a = int(((m - NEAR_WHITE_FEATHER) / (WHITE_THRESHOLD - NEAR_WHITE_FEATHER)) * 255)
            new_a = max(0, 255 - new_a)
            px[x, y] = (r, g, b, new_a)
            softened += 1
transparent.save(TRANSPARENT_OUT, "PNG", optimize=True)
print(f"  -> {TRANSPARENT_OUT}  ({made_transparent:,} px cleared, {softened:,} feathered)")

# Pass 2 — light variant for dark backgrounds (recolor dark to cream)
light = transparent.copy()
px = light.load()
recolored = 0
for y in range(h):
    for x in range(w):
        r, g, b, a = px[x, y]
        if a == 0:
            continue
        avg = (r + g + b) / 3
        if avg < DARK_BRIGHTNESS:
            px[x, y] = (CREAM[0], CREAM[1], CREAM[2], a)
            recolored += 1
light.save(LIGHT_OUT, "PNG", optimize=True)
print(f"  -> {LIGHT_OUT}  ({recolored:,} px recolored to cream)")
