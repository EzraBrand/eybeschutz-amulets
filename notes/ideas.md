# Ideas and plan

## Goal

Measure whether Emden's decoding rules find Sabbatean content in the
Eybeschütz amulets **more often than chance**, with the rules fixed before
we look at the results. This is the method that settled the Bible-codes
debate (McKay et al. 1999): fix the procedure, then run it on target texts
and on control texts.

## Possible results

- **The rules find "Shabbetai Zevi" equally often in the controls:** Emden's
  method proves nothing alone. The case then rests on the other evidence
  (*Va-Avo ha-Yom*, Wolf, Landau's letter).
- **The rules find it much more often in the Eybeschütz amulets:** this is
  the first quantitative support for Emden's reading.
- **Both results are publishable.** The second is the more surprising one,
  because the consensus is already on Emden's side without a number.

## Steps

### Phase 1: Build the corpus
1. Download Leiman–Schwarzfuchs 2006 (Metz). Transcribe the five Metz
   amulets. This is the pilot, because the notarized copies avoid the
   "tampered" defence.
2. Find each amulet in *Luḥot Edut* 1755 and *Sefat Emet*. Read the page
   images, not the OCR. Transcribe them into a structured format:
   `corpus/amulets.jsonl`, one record per amulet per witness, with these
   fields: `id, city, date, witness, page, layout (lines / star / circle), text_lines[]`.
3. Align the witnesses for each amulet and list every letter variant.

### Phase 2: Write down Emden's rules
4. From *Sefat Emet* and *Shevirat*, extract each decoding step that Emden
   applies. For each step, record the input letters, the rule
   (gematria / atbash / albam / notarikon / letter skip / reversal) and the
   output.
5. Encode each rule as a function. Record which rules Emden uses and how
   many steps he chains. The "degrees of freedom" of the method is the
   number that matters.

### Phase 3: Controls
6. Control amulets: childbirth amulets of the same period by authors whom
   nobody accuses of Sabbateanism. Candidates:
   - printed amulet manuals (*Sefer Raziel*, Zacuto's *Shorshei ha-Shemot*,
     *Toledot Adam*);
   - surviving 18th-c. Ashkenazi childbirth amulets in museum collections
     (Israel Museum, JTS, Jewish Museum NY);
   - Eybeschütz's defenders' own sample amulets, if any are printed.
7. Also randomized controls: shuffle the Holy-Name blocks; make texts with
   the same letter frequencies.

### Phase 4: The test
8. Run every rule chain, with the same budget of steps, on the targets and on
   the controls. Count hits for a fixed list of target strings: שבתי, צבי,
   שבתי צבי, משיח, משיח אלהי יעקב, and so on, plus their gematria values.
9. Report the hit rates with a permutation p-value. Pre-register the target
   list and the rule budget in this file **before** step 8.

## Risks

- **Small corpus.** There may be only tens of amulets. The test may have
  little power. A clear null result is still useful.
- **Selection.** Emden printed the amulets he thought incriminating. The
  Metz set (notarized by the community, not chosen by Emden) is the best
  defence against this.
- **Emden's rules may be too free to formalize.** If so, that is itself the
  finding: show how many degrees of freedom he used.
- **Transcription errors** in the diagrams. Two independent transcriptions
  of each amulet, then a comparison.

## Tools we already have

- Kraken plus page-image reading for Hebrew prints (from the Emden
  *Megillat Sefer* project).
- Line-crop workflow for close reading of small type (see memory note).
- Gematria / atbash functions are simple to write.

## Open questions for the owner

- Do you want to publish this as a public repo and site, like the realia
  projects?
- Will you try to get Perlmuter (1947) and Scholem's *Tarbiz* article
  (JSTOR)? Scholem's close reading of one amulet is the best model for
  phase 2.

## Pre-registration: control test 1 (written 21-Nov-2026, before the run)

**Question.** Under the same partial-atbash key (each letter kept or replaced
by its atbash pair), how often does ordinary Hebrew text produce what the
Metz amulets produce?

**Why plain text works as the control.** Partial atbash is its own inverse
letter by letter. Encrypting a plain text with any partial atbash and then
searching the ciphertext with partial atbash gives the same matches as
searching the plain text. So no simulated encryption step is needed: we search
real Hebrew directly.

**Units.** Words = maximal runs of Hebrew letters; nikud, cantillation,
punctuation and HTML removed; final letters normalized. A word "is a hit" for
target T if any substring of it matches T under partial atbash.

**Statistics (fixed now):**
- S = number of words that hit שבתי
- M = number of words that hit משיחו
- A = number of adjacent word pairs (i, i+1) where word i hits משיחו and word
  i+1 hits שבתי

**Metz values (reading 2):** 257 words; S = 7, M = 4, A = 3.

**Controls (local copies from other projects, not copied into this repo):**
1. Hebrew Bible, consonantal text (tanach.us via Sefaria, public domain)
2. Babylonian Talmud, Aramaic/Hebrew (Sefaria, William Davidson ed.)
3. Emden, *Megillat Sefer* (Kahana 1896, my OCR'd and checked text)
4. *Me'or Einayim* (my OCR'd text, Imrei Binah chapters)

**Procedure.** For each control: the rates per 1,000 words, and 20,000 random
contiguous 257-word windows (seed 1751). p_S = share of windows with S ≥ 7;
p_M = share with M ≥ 4; p_A = share with A ≥ 3; p_joint = share with all
three. A result is "unusual" if p < 0.01 in every control.

**Known weakness, stated in advance.** None of the controls is amulet text.
Amulets repeat formulae (אלהי ישראל), and the decoded Metz texts are
liturgical. A control from real amulet manuals is still needed (test 2).
