# Control test 1: real Hebrew (run 21-Nov-2026)

Pre-registered in `notes/ideas.md` (commit 1212b7c) before the run. Script:
`scripts/control_test.py` (seed 1751, 20,000 windows per control, runtime 15 s).

## Result

Per 1,000 words, under partial atbash:

| Text | Words | S: שבתי | M: משיחו | A: משיחו + שבתי |
|---|---|---|---|---|
| **Metz amulets** | **257** | **27.2** | **15.6** | **11.7** |
| Hebrew Bible | 306,872 | 0.68 | 0.15 | 0 |
| Bavli | 597,832 | 0.29 | 0.01 | 0 |
| Emden, *Megillat Sefer* | 55,402 | 1.10 | 0.02 | 0 |
| *Me'or Einayim* | 174,825 | 0.28 | 0.01 | 0 |

Random 257-word windows that reach the Metz values:

| Text | p_S (S ≥ 7) | p_M (M ≥ 4) | p_A (A ≥ 3) | p_all |
|---|---|---|---|---|
| Hebrew Bible | < 0.0001 | < 0.0001 | < 0.0001 | < 0.0001 |
| Bavli | 0.0001 | < 0.0001 | < 0.0001 | < 0.0001 |
| Emden | < 0.0001 | < 0.0001 | < 0.0001 | < 0.0001 |
| *Me'or Einayim* | < 0.0001 | < 0.0001 | < 0.0001 | < 0.0001 |

("< 0.0001" = no window out of 20,000.)

By the pre-registered rule (p < 0.01 in every control), the Metz result is
**unusual**.

- **שבתי strings** come 25–100 times more often in the amulets than in real
  Hebrew. In real Hebrew they are ordinary words: ושבתי, חשבתי, שבאמת, בשתי.
- **משיחו strings** come about 100 times more often. In real Hebrew they are
  mostly ישמחו and similar words.
- **No control has a single משיחו + שבתי adjacency in 1.13 million words.** The
  Metz amulets have three in 257 words.

## Limits

1. **Not amulet text.** The controls are Bible, Talmud and 18th-century prose.
   Amulets are formulaic. The right next control is real childbirth amulets of
   the period (test 2).
2. **The four amulets share a template.** The counts are not independent:
   each amulet repeats a formula that holds the משיחו/שבתי words. Counted
   per amulet, שבתי is in all four and the adjacency is in two. One adjacency
   in a short amulet is already something no control window produced.
3. **The key comes from the same texts.** Partial atbash was inferred from the
   uncontroversial formulae (אלהי ישראל), not from the targets. The targets
   themselves (שבתי, משיחו) are the 1751 accusation, not chosen after looking.
4. **Transcription.** One reader, from a journal photograph. A single misread
   ב/כ changes S. The doubtful letters are listed in `corpus/metz_amulets.json`.
5. **OCR'd controls.** The Emden and *Me'or Einayim* texts are checked OCR;
   small errors cannot create the Metz rates.
