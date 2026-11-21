"""How much freedom does the atbash / albam decoding rule give?

Sefat Emet (Lemberg 1877 reprint, PDF p. 6) states the method for one amulet:
"א"ת ב"ש and א"ל ב"ם, and sometimes a double substitution", and gives the
example בילב היי -> שבתי צבי (first letter by atbash, next letters by
albam then atbash).

Two regimes:
  word  - one transform for the whole word (5 choices)
  letter- a free choice of transform for EACH letter (Emden's worked example)

For each target word we compute:
  p      - probability that a random word of the same length (letters drawn
           with the letter frequencies of the Metz inner texts) decodes to
           the target under the regime;
  E      - expected number of such words among the Metz inner-text words of
           that length;
  hits   - the Metz words that actually decode to the target.

Usage: py -3.13 scripts/cipher_freedom.py
"""
import json
import sys
from collections import Counter
from itertools import product
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ALEF = "אבגדהוזחטיכלמנסעפצקרשת"
FINALS = str.maketrans("ךםןףץ", "כמנפצ")
IDX = {c: i for i, c in enumerate(ALEF)}


def norm(w):
    return "".join(c for c in w.translate(FINALS) if c in IDX)


def atbash(c):
    return ALEF[21 - IDX[c]]


def albam(c):
    i = IDX[c]
    return ALEF[i + 11] if i < 11 else ALEF[i - 11]


TRANSFORMS = {
    "id": lambda c: c,
    "atbash": atbash,
    "albam": albam,
    "albam>atbash": lambda c: atbash(albam(c)),
    "atbash>albam": lambda c: albam(atbash(c)),
}

# Check against the worked example in Sefat Emet: בילב -> שבתי
ex = "".join(f(c) for f, c in zip(
    [atbash, TRANSFORMS["albam>atbash"], TRANSFORMS["albam>atbash"], TRANSFORMS["albam>atbash"]],
    "בילב"))
assert ex == "שבתי", ex

root = Path(__file__).resolve().parent.parent
data = json.loads((root / "corpus" / "metz_amulets.json").read_text(encoding="utf-8"))
words = []
for a in data["amulets"]:
    for line in a["inner_text_lines"]:
        words += [norm(w) for w in line.split() if norm(w)]
freq = Counter("".join(words))
total = sum(freq.values())
P = {c: freq[c] / total for c in ALEF}
by_len = Counter(len(w) for w in words)
print(f"Metz inner texts: {len(words)} words, {total} letters\n")


def preimages(target_letter):
    return {c for c in ALEF for f in TRANSFORMS.values() if f(c) == target_letter}


def p_letter_regime(target):
    p = 1.0
    for t in target:
        p *= sum(P[c] for c in preimages(t))
    return p


def p_word_regime(target):
    srcs = set()
    for f in TRANSFORMS.values():
        inv = {f(c): c for c in ALEF}
        srcs.add("".join(inv[t] for t in target))
    p = 0.0
    for s in srcs:
        q = 1.0
        for c in s:
            q *= P[c]
        p += q
    return p, srcs


def decodes_letter(w, target):
    return len(w) == len(target) and all(c in preimages(t) for c, t in zip(w, target))


TARGETS = ["שבתי", "צבי", "משיח", "משיחו", "ישראל", "אלהי"]


# Regime 3: "partial atbash" - each letter is either kept or atbash'd.
# This is the key the Metz amulets themselves show: אכהי=אלהי, יבראל=ישראל,
# מביחף=משיחו (ב/ש, כ/ל, י/מ, ו/פ are atbash pairs).
def pa_pre(t):
    return {t, atbash(t)}


def p_partial(target):
    p = 1.0
    for t in target:
        p *= sum(P[c] for c in pa_pre(t))
    return p


def pa_match(s, target):
    return all(c in pa_pre(t) for c, t in zip(s, target))


letters_by_word = words  # substring search stays inside words


def substr_hits(target, regime_match):
    n = len(target)
    out, windows = [], 0
    for w in letters_by_word:
        for i in range(len(w) - n + 1):
            windows += 1
            if regime_match(w[i:i + n], target):
                out.append(w if len(w) == n else f"{w}[{i}:{i+n}]")
    return out, windows
print("Letter freedom: how many source letters can stand for each target letter")
for t in sorted(set("".join(TARGETS))):
    print(f"  {t}: {''.join(sorted(preimages(t), key=IDX.get))}")
print()
print(f"{'target':8} {'n':>2} {'words_n':>7} | {'p word':>8} {'E word':>6} | {'p letter':>8} {'E letter':>8} | letter-regime hits in Metz")
for tg in TARGETS:
    n = len(tg)
    pw, _ = p_word_regime(tg)
    pl = p_letter_regime(tg)
    hits = [w for w in words if decodes_letter(w, tg)]
    print(f"{tg:8} {n:>2} {by_len[n]:>7} | {pw:8.5f} {pw*by_len[n]:6.2f} | {pl:8.5f} {pl*by_len[n]:8.2f} | {' '.join(hits) or '-'}")

print("\nPartial atbash (each letter kept or atbash'd), searched as SUBSTRINGS inside words")
print(f"{'target':8} | {'p':>8} {'windows':>7} {'E':>6} | observed")
for tg in TARGETS:
    pp = p_partial(tg)
    hits, win = substr_hits(tg, pa_match)
    print(f"{tg:8} | {pp:8.5f} {win:7d} {pp*win:6.2f} | {len(hits)}: {' '.join(hits) or '-'}")
