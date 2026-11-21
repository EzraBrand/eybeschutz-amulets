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

## First cipher result

The Metz amulets show one consistent key: **partial atbash**. Some letters
are replaced by their atbash pair and the others are kept. The atbash pairs
that occur are ב/ש, כ/ל, י/מ and ו/פ(ף).

- `אכהי` = אלהי, 11 times; `יבראל`/`יבראך` = ישראל, 6 times. These are
  ordinary amulet formulae.
- **The same key** gives `מביחף`/`מבמחף`/`משמחף` = **משיחו** ("His
  messiah"), 4 times.
- It also gives **שבתי** twice, inside `קבבתיקא` (amulet 1, line 3) and
  `בבתיק` (amulet 1, line 9).

The null model draws random letters with the letter frequencies of these
texts, searching substrings inside words:

| target | expected by chance | observed |
|---|---|---|
| שבתי | 0.09 | 2 |
| משיחו | 0.00 | 4 |
| משיח | 0.06 | 4 |
| צבי | 0.92 | 5 (`הביק`, `הבית`, `להבין`…) |
| אלהי | 0.04 | 11 |
| ישראל | 0.00 | 6 |

**How to read this:**
- The random-letter null is too weak. The amulets are clearly coded Hebrew
  (אלהי ישראל), so any coherent Hebrew text beats it. So these numbers do
  **not** yet show that the text is Sabbatean.
- What they **do** show:
  1. One simple, consistent key (partial atbash) turns the "Holy Names" into
     a connected text. This supports Emden and Leiman against Eybeschütz's
     "separate Names" defence, at least for amulets 1–4.
  2. Under that one key, **משיחו** and **שבתי** come out without any extra
     freedom. Emden's printed method ("atbash, albam, sometimes double") is
     much looser. Under that looser letter-by-letter rule, a random four-letter
     word becomes שבתי with p ≈ 0.007, which is about 0.5 expected hits per
     corpus of this size.
  3. **צבי** is not evidence: the hits are ordinary words.
- **Variants that matter:** the MS reading `קבבתי` (print `קבכתי`) and
  Eybeschütz's `בבהמים` (MS `בבתמים`) each turn on exactly the letter that
  makes or breaks `בבת…` → `שבת…`. The other "בכתי" forms (amulet 2
  `זבכתי`, amulet 4 `בכתמי`, seal 4 `בכתי`) give שבתי only if כ is read as ב,
  which is the confusion that Eybeschütz himself blamed on the copyist. This
  is a hypothesis to check. It is not established.

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
