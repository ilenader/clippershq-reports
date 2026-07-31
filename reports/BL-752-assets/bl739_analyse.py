"""scratch/bl739_analyse.py — analyse the completed BL-722 audio benchmark. $0, offline.

Reports each stratum SEPARATELY with a Wilson interval, because a blended average hides the
only condition the question turns on. Reads bl722_results.jsonl + bl722_genre_labels.json
(hand grades for the A-declared stratum, which is the only stratum with objective ground
truth) and writes bl739_analysis.json.

WHAT IS AND IS NOT GRADEABLE, stated up front because it constrains every number below:
  A-declared      the clip's own music_info names a real track+artist -> gradeable.
  C-dialogue      speech-dominant by construction; the corpus builder's stated expectation
                  is genre='none' -> gradeable against that expectation.
  B-music-no-title  NO declared track and no transcript. There is no ground truth, and the
                  grader cannot hear audio, so NO accuracy number is computable. Reported as
                  an output distribution and a consistency signal only. Inventing hand
                  labels here would be fabrication.
"""
import json
import math
import os
import collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = os.path.join(ROOT, "scratch")

rows = []
for line in open(os.path.join(S, "bl722_results.jsonl"), encoding="utf-8"):
    try:
        rows.append(json.loads(line))
    except Exception:
        pass
corpus = {c["pk"]: c for c in json.load(open(os.path.join(S, "bl722_corpus.json"),
                                            encoding="utf-8"))}
labels = json.load(open(os.path.join(S, "bl722_genre_labels.json"), encoding="utf-8"))
grade_by_track = {(l["track"].strip().lower(), (l["artist"] or "").strip().lower()): l
                  for l in labels["labels"]}


def find_grade(title, artist):
    """Join a result row to its hand grade.

    Exact (title, artist) first. One A-declared title carries mojibake from the source
    payload — 'Like a Prayer (Choir Version From ?Deadpool & Wolverine?)' — so an exact
    match silently drops a graded row and quietly shrinks the denominator. Fall back to
    artist + a title-prefix match, which is unambiguous on a 16-row stratum.
    """
    t, a = (title or "").strip().lower(), (artist or "").strip().lower()
    g = grade_by_track.get((t, a))
    if g:
        return g
    for (lt, la), lab in grade_by_track.items():
        if la and la == a:
            return lab
        if lt and (t.startswith(lt[:18]) or lt.startswith(t[:18])):
            return lab
    return None


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (round(100 * max(0.0, c - h), 1), round(100 * min(1.0, c + h), 1))


def line(lbl, k, n, extra=""):
    if n == 0:
        print(f"  {lbl:46s}  n=0")
        return
    lo, hi = wilson(k, n)
    print(f"  {lbl:46s}  {k:3d}/{n:<3d} = {100*k/n:5.1f}%   95% CI [{lo:4.1f}, {hi:4.1f}] {extra}")


p1 = [r for r in rows if r["pass"] == 1]
by_st = collections.defaultdict(list)
for r in p1:
    by_st[r["stratum"]].append(r)

out = {"n_rows": len(rows), "n_pass1": len(p1),
       "by_stratum": {k: len(v) for k, v in by_st.items()}}

print("=" * 104)
print("COVERAGE")
print("=" * 104)
for st in sorted(by_st):
    print(f"  {st:20s} pass1 n={len(by_st[st]):3d}")
print(f"  repeats: " + str(dict(collections.Counter(r["pass"] for r in rows if r["pass"] > 1))))

# ---------------------------------------------------------------- A: graded accuracy
print("\n" + "=" * 104)
print("STRATUM A-declared — genre vs the clip's OWN declared track (the only objective truth)")
print("=" * 104)
A = by_st.get("A-declared", [])
gr = collections.Counter()
a_rows = []
for r in A:
    g = find_grade(r.get("title"), r.get("artist"))
    grade = g["grade"] if g else "ungraded"
    gr[grade] += 1
    a_rows.append({**r, "grade": grade})
for k in ("correct", "defensible", "wrong", "unverifiable", "ungraded"):
    if gr[k]:
        print(f"    {k:14s} {gr[k]}")
gradeable = [r for r in a_rows if r["grade"] in ("correct", "defensible", "wrong")]
nb = len(gradeable)
print()
line("A: strict correct (of gradeable)", sum(1 for r in gradeable if r["grade"] == "correct"), nb)
line("A: correct OR defensible (of gradeable)",
     sum(1 for r in gradeable if r["grade"] in ("correct", "defensible")), nb)
out["A"] = {"grades": dict(gr), "n_gradeable": nb,
            "strict": sum(1 for r in gradeable if r["grade"] == "correct"),
            "lenient": sum(1 for r in gradeable if r["grade"] in ("correct", "defensible"))}

# ------------------------------------------------- ITEM 4: split by DETECTED speech
print("\n" + "=" * 104)
print("ITEM 4 — accuracy split by whether the MODEL detected speech (A-declared only)")
print("=" * 104)
for tag, sel in (("vocals=speech", lambda r: r["vocals"] == "speech"),
                 ("vocals!=speech", lambda r: r["vocals"] != "speech")):
    sub = [r for r in a_rows if sel(r)]
    subg = [r for r in sub if r["grade"] in ("correct", "defensible", "wrong")]
    unv = sum(1 for r in sub if r["grade"] == "unverifiable")
    print(f"\n  {tag}: n={len(sub)}  gradeable={len(subg)}  unverifiable={unv}")
    if subg:
        line(f"    strict correct", sum(1 for r in subg if r["grade"] == "correct"), len(subg))
        line(f"    correct or defensible",
             sum(1 for r in subg if r["grade"] in ("correct", "defensible")), len(subg))
out["item4_speech_split"] = {
    t: {"n": len([r for r in a_rows if f(r)]),
        "gradeable": len([r for r in a_rows if f(r) and r["grade"] in ("correct", "defensible", "wrong")]),
        "unverifiable": len([r for r in a_rows if f(r) and r["grade"] == "unverifiable"]),
        "lenient": len([r for r in a_rows if f(r) and r["grade"] in ("correct", "defensible")])}
    for t, f in (("speech", lambda r: r["vocals"] == "speech"),
                 ("not_speech", lambda r: r["vocals"] != "speech"))}

# ---------------------------------------------------------------- C: the null case
print("\n" + "=" * 104)
print("STRATUM C-dialogue — speech-dominant; the builder's stated expectation is genre='none'")
print("=" * 104)
C = by_st.get("C-dialogue", [])
if C:
    none_n = sum(1 for r in C if r["genre"] == "none")
    sp_n = sum(1 for r in C if r["vocals"] == "speech")
    line("C: genre == 'none' (the null case)", none_n, len(C))
    line("C: vocals == 'speech' (did it hear the talking)", sp_n, len(C))
    print("    genre distribution:", dict(collections.Counter(r["genre"] for r in C)))
    print("    vocals distribution:", dict(collections.Counter(r["vocals"] for r in C)))
    sfs = [(corpus.get(r["pk"], {}).get("speech_frac"), r["genre"]) for r in C]
    out["C"] = {"n": len(C), "genre_none": none_n, "vocals_speech": sp_n,
                "genre_dist": dict(collections.Counter(r["genre"] for r in C)),
                "vocals_dist": dict(collections.Counter(r["vocals"] for r in C))}

# ---------------------------------------------------------------- B: no ground truth
print("\n" + "=" * 104)
print("STRATUM B-music-no-title — NO declared track, NO transcript, grader cannot hear audio")
print("=" * 104)
B = by_st.get("B-music-no-title", [])
if B:
    print("  *** NO ACCURACY NUMBER IS COMPUTABLE FOR THIS STRATUM. Distribution only. ***")
    print("    genre :", dict(collections.Counter(r["genre"] for r in B)))
    print("    vocals:", dict(collections.Counter(r["vocals"] for r in B)))
    print("    energy:", dict(collections.Counter(r["energy"] for r in B)))
    print("    build :", dict(collections.Counter(r["has_build"] for r in B)))
    sf = [(corpus.get(r["pk"], {}).get("speech_frac"), r) for r in B]
    hi = [r for s, r in sf if s is not None and s >= 0.20]
    lo = [r for s, r in sf if s is not None and s < 0.20]
    print(f"\n    speech_frac >= 0.20 (music genuinely UNDER dialogue): n={len(hi)}")
    print("       genre:", dict(collections.Counter(r["genre"] for r in hi)))
    print("       heard speech:", sum(1 for r in hi if r["vocals"] == "speech"), "/", len(hi))
    print(f"    speech_frac <  0.20 (music mostly clean): n={len(lo)}")
    print("       genre:", dict(collections.Counter(r["genre"] for r in lo)))
    print("       heard speech:", sum(1 for r in lo if r["vocals"] == "speech"), "/", len(lo))
    out["B"] = {"n": len(B), "genre_dist": dict(collections.Counter(r["genre"] for r in B)),
                "vocals_dist": dict(collections.Counter(r["vocals"] for r in B)),
                "n_speech_ge_20pct": len(hi),
                "heard_speech_in_those": sum(1 for r in hi if r["vocals"] == "speech")}

# ---------------------------------------------------------------- consistency
print("\n" + "=" * 104)
print("ITEM 2 — CONSISTENCY: same clip, two passes, temperature 0")
print("=" * 104)
byk = collections.defaultdict(dict)
for r in rows:
    byk[r["pk"]][r["pass"]] = r
pairs = [(v[1], v[2]) for v in byk.values() if 1 in v and 2 in v]
if pairs:
    for f in ("genre", "energy", "vocals", "has_build"):
        line(f"identical on {f}", sum(1 for a, b in pairs if a[f] == b[f]), len(pairs))
    allf = sum(1 for a, b in pairs if all(a[f] == b[f] for f in
                                          ("genre", "energy", "vocals", "has_build")))
    line("identical on ALL FOUR fields", allf, len(pairs))
    print("\n    disagreements:")
    for a, b in pairs:
        d = [f"{f}: {a[f]} -> {b[f]}" for f in ("genre", "energy", "vocals", "has_build")
             if a[f] != b[f]]
        if d:
            print(f"      {a['pk'][-6:]} {str(a.get('title'))[:26]:26s} " + " | ".join(d))
    out["consistency"] = {"n_pairs": len(pairs), "all_four": allf,
                          **{f: sum(1 for a, b in pairs if a[f] == b[f])
                             for f in ("genre", "energy", "vocals", "has_build")}}

# ---------------------------------------------------------------- item 3: the Zimmer clip
print("\n" + "=" * 104)
print("ITEM 3 — the Hans Zimmer / Cornfield Chase failure, repeated")
print("=" * 104)
z = sorted([r for r in rows if "cornfield" in (r.get("title") or "").lower()],
           key=lambda r: r["pass"])
for r in z:
    print(f"    pass {r['pass']}: genre={r['genre']:22s} energy={r['energy']:9s} "
          f"vocals={r['vocals']:8s} build={r['has_build']}")
if z:
    gs = collections.Counter(r["genre"] for r in z)
    print(f"\n    distinct genres across {len(z)} passes: {dict(gs)}")
    verdict = ("REPEATABLE -> a model limitation, not instability"
               if len(gs) == 1 else "VARYING -> instability is the bigger problem")
    print(f"    VERDICT: {verdict}")
    out["zimmer"] = {"passes": len(z), "genres": dict(gs), "verdict": verdict}

# ---------------------------------------------------------------- cost
print("\n" + "=" * 104)
print("COST — from ACTUAL token usage on the rows this backend produced")
print("=" * 104)
orr = [r for r in rows if r.get("backend") == "openrouter"]
IN, OUT_ = 0.0000005, 0.0000015           # Flex $/token, audio in / completion out
if orr:
    ti = sum(r.get("tokens_in", 0) for r in orr)
    to = sum(r.get("tokens_out", 0) for r in orr)
    cost = ti * IN + to * OUT_
    print(f"  openrouter rows: {len(orr)}   tokens in {ti:,}  out {to:,}")
    print(f"  cost this backend: ${cost:.4f}   per clip ${cost/len(orr):.6f}   "
          f"per 1,000 clips ${cost/len(orr)*1000:.2f}")
    lat = [r.get("latency_s") for r in orr if r.get("latency_s")]
    if lat:
        lat.sort()
        print(f"  latency: median {lat[len(lat)//2]:.1f}s  max {lat[-1]:.1f}s")
    print(f"  served_by: {dict(collections.Counter(r.get('served_by','') for r in orr))}")
    out["cost"] = {"rows": len(orr), "tokens_in": ti, "tokens_out": to,
                   "usd_total": round(cost, 4), "usd_per_clip": round(cost / len(orr), 6),
                   "usd_per_1000": round(cost / len(orr) * 1000, 2)}
    billed = [r["or_cost"] for r in orr if r.get("or_cost") is not None]
    if billed:
        b = sum(billed)
        print(f"  CROSS-CHECK: OpenRouter's own usage.cost on the {len(billed)} rows that "
              f"recorded it: ${b:.5f}  (${b/len(billed):.6f}/clip -> ${b/len(billed)*1000:.2f}/1,000)")
        tb = sum(r.get("tokens_in",0) for r in orr if r.get("or_cost") is not None)*IN +              sum(r.get("tokens_out",0) for r in orr if r.get("or_cost") is not None)*OUT_
        print(f"               token-rate estimate for the same rows: ${tb:.5f} "
              f"({100*(tb-b)/b:+.1f}% vs billed)")
        out["cost"]["billed_subset_usd"] = round(b,5)
        out["cost"]["billed_subset_rows"] = len(billed)
        out["cost"]["billed_per_1000"] = round(b/len(billed)*1000,2)

json.dump(out, open(os.path.join(S, "bl739_analysis.json"), "w", encoding="utf-8"),
          indent=1, ensure_ascii=False)
print("\nwrote scratch/bl739_analysis.json")
