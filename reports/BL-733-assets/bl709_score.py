"""bl709_score.py — score OCR output against the hand transcriptions.

Metrics, defined explicitly because "accuracy" is ambiguous:
  exact   normalised-whitespace string equality, case and punctuation KEPT.
  usable  every meaningful word right: compare the multiset of alphanumeric word tokens,
          lowercased, punctuation and emoji stripped. Order-insensitive because OCR
          returns regions in reader order, which is not a transcription error.
  CER     Levenshtein(pred, truth) / len(truth) on lowercased, whitespace-collapsed text.
  caption_hit  softer and more practical: does the output contain EVERY word of the
          PRIMARY caption (the main overlay), ignoring watermarks and incidental text?

Images whose truth is empty are NOT accuracy cases — they are true negatives, scored
separately as a false-positive (hallucination) rate.
"""
import os, json, re, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "bl709")

truth = {}
for f in ("truth_A.json", "truth_B.json", "truth_CD.json"):
    for r in json.load(open(os.path.join(D, f), encoding="utf-8")):
        truth[r["id"]] = r
runs = {r["id"]: r for r in json.load(open(os.path.join(D, "ocr_runs.json"), encoding="utf-8"))}
print(f"truth {len(truth)}  ocr runs {len(runs)}\n")


def strip_emoji(s):
    return "".join(c for c in s if unicodedata.category(c) not in ("So", "Sk", "Cn"))


def norm_ws(s):
    return re.sub(r"\s+", " ", strip_emoji(s or "")).strip()


def words(s):
    s = strip_emoji((s or "").lower())
    return sorted(w for w in re.findall(r"[^\W_]+", s, flags=re.UNICODE) if w)


def lev(a, b):
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def score(pred, t):
    tn, pn = norm_ws(t), norm_ws(pred)
    exact = (tn == pn)
    usable = (words(t) == words(pred))
    cer = lev(pn.lower(), tn.lower()) / max(1, len(tn))
    return exact, usable, min(cer, 1.0)


def caption_hit(pred, primary):
    if not primary:
        return None
    pw, tw = set(words(pred)), words(primary)
    return all(w in pw for w in tw)


rows = []
for i, r in truth.items():
    run = runs.get(i)
    if not run:
        continue
    t = r.get("truth", "")
    rec = {"id": i, "stratum": i[0], "script": r.get("script"), "bar": r.get("bar"),
           "size": r.get("size"), "font": r.get("font"), "truth": t,
           "has_text": bool(norm_ws(t))}
    for v in ("base", "full", "bar2x"):
        p = run.get(v, "")
        rec[v] = p
        if rec["has_text"]:
            e, u, c = score(p, t)
            rec[v + "_exact"], rec[v + "_usable"], rec[v + "_cer"] = e, u, round(c, 3)
            rec[v + "_caphit"] = caption_hit(p, r.get("primary") or t)
        else:
            rec[v + "_fp"] = bool(norm_ws(p))          # hallucination on a blank image
    rows.append(rec)

json.dump(rows, open(os.path.join(D, "scored.json"), "w", encoding="utf-8"),
          indent=1, ensure_ascii=False)

TXT = [r for r in rows if r["has_text"]]
BLK = [r for r in rows if not r["has_text"]]


def block(name, rs, variant="base"):
    if not rs:
        print(f"  {name:44s}  n=0")
        return
    n = len(rs)
    ex = sum(1 for r in rs if r[variant + "_exact"])
    us = sum(1 for r in rs if r[variant + "_usable"])
    ch = sum(1 for r in rs if r.get(variant + "_caphit"))
    cer = sum(r[variant + "_cer"] for r in rs) / n
    print(f"  {name:44s}  n={n:3d}  exact {ex:3d}={100*ex/n:5.1f}%  "
          f"usable {us:3d}={100*us/n:5.1f}%  caption-hit {ch:3d}={100*ch/n:5.1f}%  "
          f"CER {cer:.3f}")


LATIN = ("latin",)
print("=" * 108)
print("HEADLINE — the EASY CASE first (solid bar + large + plain font + Latin script)")
print("=" * 108)
easy = [r for r in TXT if r["bar"] and "solid" in str(r["bar"]) and r["size"] == "large"
        and r["font"] == "plain" and r["script"] in LATIN]
block("EASY CASE (production settings)", easy, "base")
block("EASY CASE (no 512px downscale)", easy, "full")
block("EASY CASE (crop to bar + 2x upscale)", easy, "bar2x")

print("\n" + "=" * 108)
print("ALL TEXT-BEARING IMAGES")
print("=" * 108)
for v in ("base", "full", "bar2x"):
    block(f"all text-bearing [{v}]", TXT, v)

print("\n" + "=" * 108)
print("BY CONDITION (production 'base' settings)")
print("=" * 108)
print("\n -- script --")
for s in sorted({r["script"] for r in TXT}):
    block(f"script={s}", [r for r in TXT if r["script"] == s])
print("\n -- Latin vs non-Latin --")
block("Latin only", [r for r in TXT if r["script"] in LATIN])
block("any non-Latin script present", [r for r in TXT if r["script"] not in LATIN])
print("\n -- bar vs no bar (Latin only, to isolate the variable) --")
lat = [r for r in TXT if r["script"] in LATIN]
block("in a solid caption bar", [r for r in lat if "solid" in str(r["bar"])])
block("directly on video (no bar)", [r for r in lat if r["bar"] == "none"])
print("\n -- font (Latin only) --")
for f in sorted({str(r["font"]) for r in lat}):
    block(f"font={f}", [r for r in lat if str(r["font"]) == f])
print("\n -- size (Latin only) --")
for s in sorted({str(r["size"]) for r in lat}):
    block(f"size={s}", [r for r in lat if str(r["size"]) == s])

print("\n" + "=" * 108)
print("BLANK IMAGES — hallucination check")
print("=" * 108)
for v in ("base", "full", "bar2x"):
    fp = sum(1 for r in BLK if r.get(v + "_fp"))
    print(f"  {v:6s}  emitted text on {fp}/{len(BLK)} images with NO text = {100*fp/max(1,len(BLK)):.1f}%")

print("\n" + "=" * 108)
print("EVERY TEXT-BEARING CASE (production settings)")
print("=" * 108)
for r in sorted(TXT, key=lambda x: (not x["base_usable"], x["id"])):
    flag = "OK " if r["base_usable"] else ("~" if r.get("base_caphit") else "XX ")
    print(f"  {flag} {r['id']} [{r['script'][:9]:9s} {str(r['bar'])[:14]:14s} {str(r['font'])[:10]:10s}] "
          f"CER {r['base_cer']:.2f}")
    print(f"       truth: {norm_ws(r['truth'])[:92]}")
    print(f"       base : {norm_ws(r['base'])[:92]}")
print("\nwrote scratch/bl709/scored.json")
