"""Inventory the PDFs in sources/: page count, text layer, metadata, first text."""
import sys
from pathlib import Path

import fitz  # PyMuPDF

sys.stdout.reconfigure(encoding="utf-8")
root = Path(__file__).resolve().parent.parent / "sources"
for pdf in sorted(root.rglob("*.pdf")):
    doc = fitz.open(pdf)
    n = doc.page_count
    sample = [min(i, n - 1) for i in (0, 1, n // 2)]
    chars = sum(len(doc[i].get_text().strip()) for i in sample)
    meta = {k: v for k, v in (doc.metadata or {}).items() if v and k in ("title", "author", "subject")}
    first = ""
    for i in range(min(n, 4)):
        t = " ".join(doc[i].get_text().split())
        if t:
            first = t[:160]
            break
    print(f"{pdf.relative_to(root)} | pages={n} | text_chars_sampled={chars} | meta={meta}")
    if first:
        print(f"    first text: {first}")
