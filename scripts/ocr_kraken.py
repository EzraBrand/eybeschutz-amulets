"""Kraken OCR of PDF pages (printed square Hebrew), resumable.

  py -3.13 scripts/ocr_kraken.py PDF FIRST LAST OUTDIR [WORKERS]

Uses the Kraken install and PP-OCRv6 medium model from the Emden project
(reads printed Hebrew with 1-3 errors per page there). Writes
OUTDIR/pNNN.png (600 dpi grey), OUTDIR/pNNN.vis.txt (Kraken visual order)
and OUTDIR/pNNN.txt (logical order). Skips pages that are done.
Purpose here: an objective second reader for look-alike letters (ב/כ).
"""
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pymupdf

sys.stdout.reconfigure(encoding="utf-8")
KRAKEN = Path(r"C:\Users\ezrab\Ezra Brandt\Claude\syriac-ocr\.venv\Scripts\kraken.exe")
MODEL = Path(r"C:\Users\ezrab\AppData\Local\htrmopo\htrmopo\1980fa54-b49e-5256-95b6-928290bc48f8\medium.safetensors")
ENV = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")

pdf, first, last, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), Path(sys.argv[4])
workers = int(sys.argv[5]) if len(sys.argv) > 5 else 3
out.mkdir(parents=True, exist_ok=True)


def one(n):
    txt = out / f"p{n:03d}.txt"
    if txt.exists():
        return f"p{n:03d} skip"
    img, vis = out / f"p{n:03d}.png", out / f"p{n:03d}.vis.txt"
    if not img.exists():
        pymupdf.open(pdf)[n - 1].get_pixmap(dpi=600, colorspace=pymupdf.csGRAY).save(img)
    t = time.time()
    r = subprocess.run([str(KRAKEN), "-i", str(img), str(vis), "segment", "-bl", "ocr", "-m", str(MODEL)],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", env=ENV)
    if r.returncode or not vis.exists():
        return f"p{n:03d} FAILED: {r.stderr[-300:]}"
    lines = vis.read_text(encoding="utf-8").splitlines()
    txt.write_text("\n".join(l[::-1] for l in lines) + "\n", encoding="utf-8")
    return f"p{n:03d} ok {time.time() - t:.0f}s {len(lines)} lines"


pages = list(range(first, last + 1))
with ThreadPoolExecutor(workers) as ex:
    for i, msg in enumerate(ex.map(one, pages), 1):
        print(f"{i}/{len(pages)} {msg}", flush=True)
print("finished", flush=True)
