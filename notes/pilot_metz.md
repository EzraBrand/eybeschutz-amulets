# Pilot: the five Metz amulets (21-Nov-2026)

## What we did

1. Read Leiman & Schwarzfuchs 2006 (`sources/secondary/leiman-schwarzfuchs_95_amulets-from-metz_REJ-2006.pdf`;
   text in `notes/extracted/leiman-schwarzfuchs_metz.txt`).
2. Extracted the two plates at native resolution (`work/metz/`):
   - `ms_notarized.png`: the notarized sheet, Pl. 4 (1403×2274 px)
   - `print_sefat-emet.png`: the 1752 *Sefat Emet* fold-out (1023×2332 px)
3. Transcribed all five amulets (four inner texts and five seals) into
   `corpus/metz_amulets.json`. Line breaks come from the 1752 fold-out, and
   letters were resolved with the Lemberg 1877 reprint where possible.
   **This is a draft from one reading. It is not collated with the
   manuscript.**
4. Ran a first cipher test: `scripts/cipher_freedom.py`.

## Facts from the paper that change our plan

- **Who owned which amulet:** the owner lines are footers. Amulet 1 belonged
  to Moshe b. Uri Feibush (mother Miriam), and amulet 2 to Avraham b. Uri
  Feibush. In the 1752 fold-out these lines look like headings of the next
  amulet.
- **The witnesses agree.** After the corrigenda, the 1752 print equals the
  notarized sheet except for three letters:

  | Place | MS | 1752 print |
  |---|---|---|
  | amulet 1, line 6 | גוזג | גיזג |
  | amulet 2, seal | הן ם בם [או] ס | הן בם [או] ס |
  | amulet 3, line 3 | **קבבתי** | **קבכתי** |

- **Eybeschütz's own copy** of amulet 5 (*Luḥot Edut* 1755, pp. 63a–71a)
  differs in two places: the order in the top triangle, and in the center
  **בבהמים** for the MS **בבתמים**.
- **Eybeschütz's defence:** he had an eye disorder, he was not used to square
  script, and the scribe confused look-alike letters (ב/כ, ד/ר). He did not
  claim that letters were added or removed.
- **Amulet 5:** read clockwise from the bottom triangle, the seal gives the
  first seven words of Isaiah 9:5, `כי ילד יֻלד לנו בן נתן לנו` (Leiman
  p. 243). The same verse is in two Alsace amulets printed in *Sefat Emet*
  pp. 18, 21.
- **Authorship:** *Sefat Emet* is often given to Emden, but the author is
  unknown. Leiman suggests Nehemiah Reischer.
- **The cipher rule is stated in print.** *Sefat Emet* (Lemberg 1877, PDF
  p. 6) says that an amulet "uses א"ת ב"ש and א"ל ב"ם, and sometimes a
  double substitution". It gives the worked example `בילב היי` → `שבתי צבי`.
  The script checks that example.

## Cipher result (reading 2, from the notarized MS)

Reading 1 came from the low-resolution 1752 print plate, and it had errors of
mine (for example `עבטחף` for MS `מבמחף`, and `בכתי` for MS `בבתי`). Reading 2
follows the notarized manuscript (Pl. 4) at native resolution. Each amulet
keeps reading 1 as `reading_1_print_lowres`, and doubtful letters are in
`line_notes`.

The Metz amulets use one consistent key, **partial atbash**: some letters are
replaced by their atbash pair and the others are kept. The pairs that occur
are ב/ש, כ/ל, י/מ and ו/פ(ף). Under this one key:

- `אכהי` = אלהי (11×), `יבראל`/`יבראך`/`ישרתל` = ישראל (7×), `שך` = של.
  These are ordinary amulet formulae.
- `מביחף`/`מבמחף` = **משיחו**, "His messiah" (4×).
- `בבתי` / `בבתמ` = **שבתי** (7×, in **all four** inner texts):
  `קבבתיקא`, `בבתיק` (a1); `זבבתי` (a2); `בבתיל`, `בבתינ` (a3); `הבבתמל`,
  `בבתמי` (a4). The seals add `בבתי` (seal 4) and `בבתמים` (seal 5).
- **Adjacency.** Three times, in two amulets (a2, a4), משיחו comes directly
  before a שבתי string:
  - a2 l. 3 `אכהם מבמחף זבבתי` → "אלהים משיחו [ז]שבתי"
  - a4 l. 1–2 `אכהם מבמחף / הבבתמל` → "אלהים משיחו / השבתי…"
  - a4 l. 7 `ומביחף בבתמי הבמי` → **"ומשיחו שבתי צבי"** (Liebes's example;
    `הבמי` → צבי by ה/צ, מ/י)

The null model draws random letters with the corpus letter frequencies, and
searches substrings inside words:

| target | expected by chance | observed |
|---|---|---|
| שבתי | 0.10 | **7** |
| משיחו | 0.00 | **4** |
| צבי | 0.93 | 6 (mostly ordinary words: `הביק`, `הבית`, `הבין`…) |
| אלהי | 0.04 | 11 |
| ישראל | 0.00 | 7 |

**How to read this:**
1. One simple key turns the "separate Holy Names" into connected Hebrew. This
   is evidence against Eybeschütz's defence for amulets 1–4.
2. The incriminating words need **no extra freedom**. The key that gives the
   harmless formula אלהי ישראל also gives משיחו and שבתי. The decoders' looser
   printed rule ("atbash, albam, sometimes double") is not needed for the Metz
   texts.
3. The random-letter null is still too weak, because Hebrew has natural `בבת`
   sequences (בבתי = "in my houses"). The real test is a control on real
   Hebrew amulet text (see Next steps). The **adjacency** of משיחו + שבתי
   (3 times, in 2 amulets) will be the hardest result to explain away.
4. Variants: Leiman's MS `קבבתי` vs print `קבכתי` (a3 l. 3), and Eybeschütz's
   own `בבהמים` vs MS `בבתמים` (seal 5). Each turns on the letter that makes or
   breaks `בבת…` → `שבת…`. Eybeschütz's defence (that the copyist confused
   ב/כ) points at exactly this letter.

## Next steps

1. **Second reading** of all five amulets, from the MS plate, and a
   collation against the 1752 print. Mark each letter where the readings
   differ. Read *Luḥot Edut* 1755 p. 60a (amulet 4) and pp. 63a–71a
   (amulet 5).
2. **A proper control.** Apply the same partial-atbash search to:
   (a) the *decoded* plain Hebrew of ordinary amulets of the period, run
   through a random partial-atbash, and (b) the other Eybeschütz amulets in
   *Sefat Emet* (Lemberg 1877, pp. 5–25 carry many more amulets with their
   decodings). The question to ask: how often does a coherent childbirth
   amulet text contain משיחו / שבתי?
3. **Formalize Emden's decodings.** Take every cipher word → decoded word
   pair that *Sefat Emet* prints, and record the transform used for each
   letter. This measures how often the decoders went beyond plain partial
   atbash.
