"""Contact sheet of PDF pages, to find diagram pages by eye.

  py -3.13 scripts/contact_sheet.py PDF FIRST LAST OUT.png [cols]
Pages are 1-based and inclusive.
"""
import sys

import pymupdf
from PIL import Image, ImageDraw

pdf, first, last, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
cols = int(sys.argv[5]) if len(sys.argv) > 5 else 6
doc = pymupdf.open(pdf)
thumbs = []
for n in range(first, last + 1):
    pix = doc[n - 1].get_pixmap(dpi=28)
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    ImageDraw.Draw(im).text((3, 3), str(n), fill=(255, 0, 0))
    thumbs.append(im)
w = max(t.width for t in thumbs)
h = max(t.height for t in thumbs)
rows = (len(thumbs) + cols - 1) // cols
sheet = Image.new("RGB", (cols * w, rows * h), "white")
for i, t in enumerate(thumbs):
    sheet.paste(t, ((i % cols) * w, (i // cols) * h))
sheet.save(out)
