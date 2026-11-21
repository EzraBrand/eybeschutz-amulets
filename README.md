# Eybeschütz amulets

A project to test, with explicit and reproducible methods, the most famous
decoding dispute in early modern Jewish history: the amulets of R. Jonathan
Eybeschütz (1690–1764) and R. Jacob Emden's claim (1751) that they hide
Sabbatean content, including the name of Shabbetai Zevi.

Started 21-Nov-2026.

## The question

Emden decoded the amulets with gematria, notarikon, atbash and similar
letter rules, and he read them as Sabbatean. Eybeschütz said that they are
only separate Holy Names and that they carry no continuous message. Most
modern scholars (Scholem, Liebes, Leiman–Schwarzfuchs) accept Emden's
reading. **As far as we know, no one has tested Emden's methods
statistically.** The test is: do the same rules "find" Shabbetai Zevi and
messianic phrases in control amulets of the same period, which nobody
suspects, as often as in the Eybeschütz amulets?

## Status (21-Nov-2026)

- 16 sources are in `sources/` (9 primary, 7 secondary; see
  [SOURCES.md](SOURCES.md)). PDFs are not in git (see `.gitignore`).
- **Pilot done (draft):** the five notarized Metz amulets are transcribed in
  `corpus/metz_amulets.json`, and a first cipher test is done. See
  [notes/pilot_metz.md](notes/pilot_metz.md). Main finding: one consistent
  "partial atbash" key turns the texts into connected Hebrew (אלהי ישראל), and
  the same key gives משיחו 4 times and שבתי twice. There is no proper control
  yet.
- The HebrewBooks *Sefat Emet* is the Lemberg 1877 reprint. Its pp. 5–25 hold
  many more Eybeschütz amulets with their decodings: the next corpus.

## Layout

| Path | What |
|---|---|
| `SOURCES.md` | Every source: file, edition, link, status, what it gives us |
| `notes/research.md` | Current state of research and scholarship |
| `notes/ideas.md` | Method, test design, open questions, next steps |
| `notes/extracted/` | Plain-text extracts of born-digital papers |
| `corpus/metz_amulets.json` | Five Metz amulets: inner texts, seals, variants (draft) |
| `notes/pilot_metz.md` | Pilot method, results, next steps |
| `scripts/cipher_freedom.py` | Chance rates of decoding targets under atbash/albam regimes |
| `scripts/crop.py`, `scripts/contact_sheet.py` | Plate crops and page contact sheets for reading |
| `work/metz/` | Plate images and crops, rebuilt from the PDFs (not in git) |
| `scripts/inventory.py` | Page count and text-layer check for all PDFs |
| `scripts/find_terms.py` | Amulet-word hits per page, per book |
| `sources/primary/` | 18th–19th c. polemical books (HebrewBooks, Google Books) |
| `sources/secondary/` | Modern scholarship |

## Run

```
py -3.13 scripts/inventory.py
py -3.13 scripts/find_terms.py
```
