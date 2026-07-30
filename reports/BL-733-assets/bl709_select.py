"""bl709_select.py — pick a stratified OCR-accuracy sample, WITHOUT letting OCR pick it.

THE BIAS THIS AVOIDS. The tempting sample is "images where OCR returned text". That
measures only whether OCR got the words right when it found words — i.e. precision — and
structurally cannot see a total failure, where text is plainly visible and OCR returned ''.
Selecting that way would inflate the accuracy number and hide the worst error mode.

So strata are defined by the GEOMETRIC bar detector (repost_layout.layout_features: pure
numpy, no OCR, no model) crossed with whether the cached OCR text is empty:

  A  bar detected      + OCR non-empty   <- the "easy case" the brief cares about
  B  bar detected      + OCR EMPTY       <- candidate TOTAL failures. Must be included.
  C  no bar            + OCR non-empty    <- text overlaid directly on video
  D  no bar            + OCR EMPTY        <- may simply have no text; visually checked

Sampled from the movie/meme-leaning tags (movieclips, movieedit, moviereview, capcutedit)
because those are the pages that burn caption text in. Fixed seed; the exact file list is
written out so the measurement is reproducible.

READ-ONLY on pipeline code. Writes only into scratch/bl709/.
"""
import os, sys, json, random, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "clippershq"))
import repost_layout as RL

VD = os.path.join(ROOT, "_vision_dataset")
OUT = os.path.join(ROOT, "scratch", "bl709")
os.makedirs(OUT, exist_ok=True)
os.makedirs(os.path.join(OUT, "images"), exist_ok=True)

TAGS = {"movieclips", "movieedit", "moviereview", "capcutedit"}
TARGET = {"A": 26, "B": 12, "C": 14, "D": 8}          # 60 total
BAR_MIN = 0.10                                        # repost_layout's shipped threshold

cache = json.load(open(os.path.join(VD, "ocr_cache.json"), encoding="utf-8"))

# account -> tag, and the image list per account
imgs = []
for line in open(os.path.join(VD, "manifest.jsonl"), encoding="utf-8"):
    r = json.loads(line)
    if r.get("tag") not in TAGS:
        continue
    for name in (r.get("covers") or []):
        imgs.append((name, r["handle"], r["tag"], "cover"))
    for name in (r.get("frames") or []):
        imgs.append((name, r["handle"], r["tag"], "frame"))

print(f"candidate images in movie/meme tags: {len(imgs)}")

rows = []
for name, handle, tag, kind in imgs:
    sub = "covers" if kind == "cover" else "frames"
    p = os.path.join(VD, sub, name)
    if not os.path.exists(p):
        continue
    try:
        lay = RL.layout_features(p)
    except Exception:
        continue
    top = float(lay.get("bar_top_frac") or 0)
    bot = float(lay.get("bar_bot_frac") or 0)
    bar = (top >= BAR_MIN) or (bot >= BAR_MIN)
    txt = (cache.get(name) or "").strip()
    rows.append({"file": name, "path": p, "handle": handle, "tag": tag, "kind": kind,
                 "bar": bar, "bar_top_frac": round(top, 4), "bar_bot_frac": round(bot, 4),
                 "bar_color": lay.get("bar_top_color"),
                 "ocr_cached": txt, "ocr_empty": (txt == "")})

print(f"scored with the geometric detector: {len(rows)}")
strata = {"A": [r for r in rows if r["bar"] and not r["ocr_empty"]],
          "B": [r for r in rows if r["bar"] and r["ocr_empty"]],
          "C": [r for r in rows if not r["bar"] and not r["ocr_empty"]],
          "D": [r for r in rows if not r["bar"] and r["ocr_empty"]]}
for k in "ABCD":
    print(f"  stratum {k}: {len(strata[k]):5d} available, want {TARGET[k]}")

rnd = random.Random(20260730)
sample = []
for k in "ABCD":
    pool = sorted(strata[k], key=lambda r: r["file"])
    rnd.shuffle(pool)
    take = pool[:TARGET[k]]
    for r in take:
        r["stratum"] = k
    sample += take
    if len(take) < TARGET[k]:
        print(f"  !! stratum {k} short: {len(take)}/{TARGET[k]}")

# copy with a stable sequential id so transcription can be keyed to it
for i, r in enumerate(sorted(sample, key=lambda x: (x["stratum"], x["file"]))):
    r["id"] = f"{r['stratum']}{i:02d}"
    dst = os.path.join(OUT, "images", f"{r['id']}_{r['file']}")
    shutil.copy2(r["path"], dst)
    r["saved_as"] = os.path.basename(dst)

sample.sort(key=lambda x: x["id"])
for r in sample:
    r.pop("path", None)
json.dump(sample, open(os.path.join(OUT, "sample.json"), "w", encoding="utf-8"),
          indent=1, ensure_ascii=False)
print(f"\nselected {len(sample)} images -> scratch/bl709/images/")
print("wrote scratch/bl709/sample.json")
