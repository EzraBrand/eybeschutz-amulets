"""Crop helpers for reading the amulet plates.

  py -3.13 scripts/crop.py grid IMG OUT [step]      -> thumbnail with a labelled pixel grid
  py -3.13 scripts/crop.py crop IMG OUT x0 y0 x1 y1 [scale]  -> upscaled crop (native px)
"""
import sys

from PIL import Image, ImageDraw

cmd, src, out = sys.argv[1], sys.argv[2], sys.argv[3]
im = Image.open(src).convert("RGB")
if cmd == "grid":
    step = int(sys.argv[4]) if len(sys.argv) > 4 else 100
    d = ImageDraw.Draw(im)
    for x in range(0, im.width, step):
        d.line([(x, 0), (x, im.height)], fill=(255, 0, 0), width=1)
        d.text((x + 2, 2), str(x), fill=(255, 0, 0))
    for y in range(0, im.height, step):
        d.line([(0, y), (im.width, y)], fill=(0, 0, 255), width=1)
        d.text((2, y + 2), str(y), fill=(0, 0, 255))
    im.thumbnail((900, 1400))
    im.save(out)
else:
    x0, y0, x1, y1 = map(int, sys.argv[4:8])
    scale = float(sys.argv[8]) if len(sys.argv) > 8 else 2
    c = im.crop((x0, y0, x1, y1))
    c = c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS)
    c.save(out)
