"""Count search terms per page in the OCR text layer of each primary PDF.

The HebrewBooks OCR is noisy, so this only gives a first map of where the
amulet texts and discussions sit. Usage: py -3.13 scripts/find_terms.py
"""
import sys
from pathlib import Path

import pymupdf

sys.stdout.reconfigure(encoding="utf-8")
TERMS = ["קמיע", "קמע", "שבתי", "צבי", "משיח"]
root = Path(__file__).resolve().parent.parent / "sources" / "primary"
for pdf in sorted(root.glob("*.pdf")):
    doc = pymupdf.open(pdf)
    hits = []
    for i, page in enumerate(doc):
        t = page.get_text()
        c = {k: t.count(k) for k in TERMS}
        score = c["קמיע"] + c["קמע"]
        if score >= 3:
            hits.append((i + 1, score, c["שבתי"]))
    top = sorted(hits, key=lambda h: -h[1])[:12]
    print(f"{pdf.name}: {len(hits)} pages with >=3 amulet-word hits")
    print("    top pages (pdf page, amulet hits, 'שבתי' hits):", sorted(top))
