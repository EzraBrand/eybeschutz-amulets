"""Control test 1 (pre-registered in notes/ideas.md, 21-Nov-2026).

Under partial atbash (each letter kept or replaced by its atbash pair), count in
ordinary Hebrew text what the Metz amulets give:
  S = words that hit שבתי, M = words that hit משיחו,
  A = adjacent pairs (word hits משיחו, next word hits שבתי).
Then sample 20,000 random 257-word windows per control (seed 1751).

Control texts are local copies from other projects (paths below); they are not
part of this repository. Usage: py -3.13 scripts/control_test.py
"""
import glob
import html
import json
import random
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
CLAUDE = ROOT.parent
ALEF = "אבגדהוזחטיכלמנסעפצקרשת"
IDX = {c: i for i, c in enumerate(ALEF)}
FINALS = str.maketrans("ךםןףץ", "כמנפצ")


def atbash(c):
    return ALEF[21 - IDX[c]]


def words_of(text):
    text = html.unescape(re.sub(r"<[^>]+>", " ", text)).translate(FINALS)
    return re.findall(r"[א-ת]+", text)  # nikud/cantillation fall outside this range


def hit(word, target):
    n = len(target)
    for i in range(len(word) - n + 1):
        if all(c == t or c == atbash(t) for c, t in zip(word[i:i + n], target)):
            return True
    return False


def flatten(x):
    if isinstance(x, str):
        yield x
    elif isinstance(x, list):
        for y in x:
            yield from flatten(y)


def sefaria_words(pattern):
    out = []
    for f in sorted(glob.glob(pattern)):
        d = json.loads(Path(f).read_text(encoding="utf-8"))
        for s in flatten(d.get("text", [])):
            out += words_of(s)
    return out


def text_words(pattern):
    out = []
    for f in sorted(glob.glob(pattern)):
        out += words_of(Path(f).read_text(encoding="utf-8"))
    return out


def metz_words():
    d = json.loads((ROOT / "corpus" / "metz_amulets.json").read_text(encoding="utf-8"))
    out = []
    for a in d["amulets"]:
        for line in a["inner_text_lines"]:
            out += words_of(line)
    return out


CONTROLS = {
    "Hebrew Bible": lambda: sefaria_words(str(CLAUDE / "bochart-hierozoicon/data/tanakh/*.json")),
    "Bavli": lambda: sefaria_words(str(CLAUDE / "talmud-zoology-factcheck/data/sefaria/*_he.json")),
    "Emden, Megillat Sefer": lambda: text_words(str(CLAUDE / "emden-megillat-sefer/data/body/*.txt")),
    "Me'or Einayim": lambda: text_words(str(CLAUDE / "meor-einayim/data/*.he.txt")),
}


def flags(ws):
    s = [hit(w, "שבתי") for w in ws]
    m = [hit(w, "משיחו") for w in ws]
    a = [m[i] and s[i + 1] for i in range(len(ws) - 1)] + [False]
    return s, m, a


mw = metz_words()
s, m, a = flags(mw)
N = len(mw)
MS, MM, MA = sum(s), sum(m), sum(a)
print(f"Metz: {N} words, S={MS} M={MM} A={MA}")
print(f"  S words: {[w for w, f in zip(mw, s) if f]}")
print(f"  M words: {[w for w, f in zip(mw, m) if f]}")
print(f"  A pairs: {[(mw[i], mw[i+1]) for i in range(N - 1) if a[i]]}\n")

rng = random.Random(1751)
TRIALS = 20000
print(f"{'control':24} {'words':>9} | {'S/1k':>6} {'M/1k':>6} {'A/1k':>6} | {'p_S':>7} {'p_M':>7} {'p_A':>7} {'p_all':>7} | examples")
for name, load in CONTROLS.items():
    ws = load()
    s, m, a = flags(ws)
    n = len(ws)
    # prefix sums for fast windows
    def pref(v):
        p = [0]
        for x in v:
            p.append(p[-1] + x)
        return p
    ps, pm, pa = pref(s), pref(m), pref(a[:-1] + [False])
    cS = cM = cA = cAll = 0
    for _ in range(TRIALS):
        i = rng.randrange(0, n - N)
        vS = ps[i + N] - ps[i]
        vM = pm[i + N] - pm[i]
        vA = pa[i + N - 1] - pa[i]  # pairs fully inside the window
        cS += vS >= MS
        cM += vM >= MM
        cA += vA >= MA
        cAll += (vS >= MS and vM >= MM and vA >= MA)
    ex_s = sorted({w for w, f in zip(ws, s) if f}, key=lambda w: -ws.count(w) if n < 200000 else 0)[:4]
    ex_m = sorted({w for w, f in zip(ws, m) if f})[:3]
    ex_a = [(ws[i], ws[i + 1]) for i in range(n - 1) if a[i]][:2]
    k = 1000 / n
    print(f"{name:24} {n:9d} | {sum(s)*k:6.2f} {sum(m)*k:6.2f} {sum(a)*k:6.3f} | "
          f"{cS/TRIALS:7.4f} {cM/TRIALS:7.4f} {cA/TRIALS:7.4f} {cAll/TRIALS:7.4f} | "
          f"S:{' '.join(ex_s)} M:{' '.join(ex_m)} A:{ex_a}")
print(f"\nMetz rates per 1k words: S={MS*1000/N:.2f} M={MM*1000/N:.2f} A={MA*1000/N:.2f}")
