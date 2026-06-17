"""Generate a light-on-dark variant of the FieldPoint logo for footer use.

Strategy: any pixel darker than ~mid brightness becomes cream (#f6f1e6).
Sage / mid-green pixels stay as-is so the two-tone detail survives.
"""
from PIL import Image
import os

SRC = "assets/brand/logo.png"
DST = "assets/brand/logo-light.png"

CREAM = (246, 241, 230)  # site --paper
BRIGHTNESS_CUTOFF = 130   # pixels w/ avg < this → cream; above → keep

img = Image.open(SRC).convert("RGBA")
pixels = img.load()
w, h = img.size

changed = 0
for y in range(h):
    for x in range(w):
        r, g, b, a = pixels[x, y]
        if a == 0:
            continue
        avg = (r + g + b) / 3
        if avg < BRIGHTNESS_CUTOFF:
            # dark forest / wordmark → cream
            pixels[x, y] = (CREAM[0], CREAM[1], CREAM[2], a)
            changed += 1

img.save(DST, "PNG", optimize=True)
print(f"Wrote {DST} ({changed:,} pixels recolored, image {w}x{h})")
