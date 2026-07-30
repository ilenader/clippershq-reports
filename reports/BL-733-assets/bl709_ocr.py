"""bl709_ocr.py — run the SHIPPED ocr_features path over the 60-image sample, plus two
pre-processing variants, so part 5's "cheapest fix" question is answered with a measurement
instead of a suggestion.

Variants (same engine, same language pack, only the pixels differ):
  base   ocr_features.ocr_one() exactly as production calls it -> max_side=512 downscale.
         The sampled covers are 540x960, so production is OCR-ing a 288x512 image.
  full   no downscale (max_side=None). Isolates the cost of that resize.
  bar2x  crop to the geometrically-detected caption band, then upscale 2x. This is the
         "crop to the bar before OCR" option named in the brief.

READ-ONLY on pipeline code: imports ocr_features and repost_layout, changes neither.
Writes only scratch/bl709/ocr_runs.json.
"""
import os, sys, json, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "clippershq"))
import ocr_features as OF
import repost_layout as RL

OUT = os.path.join(ROOT, "scratch", "bl709")
IMG = os.path.join(OUT, "images")
sample = json.load(open(os.path.join(OUT, "sample.json"), encoding="utf-8"))

if not OF.probe():
    print("easyocr not importable — cannot measure. STOP."); sys.exit(1)
reader = OF.get_reader(("en",))
if reader is None:
    print("easyocr reader failed to load. STOP."); sys.exit(1)
print("easyocr reader ready (lang=en, cpu)\n")


def bar_crop_2x(path):
    """Crop to the detected band(s) and upscale 2x. Falls back to the whole image."""
    from PIL import Image
    lay = RL.layout_features(path)
    runs = lay.get("bar_runs") or []
    im = Image.open(path).convert("RGB")
    W, H = im.size
    if not runs:
        return im.resize((W * 2, H * 2))
    y0 = max(0, int(min(r[0] for r in runs)) - 4)
    y1 = min(H, int(max(r[1] for r in runs)) + 4)
    if y1 - y0 < 8:
        return im.resize((W * 2, H * 2))
    c = im.crop((0, y0, W, y1))
    return c.resize((c.width * 2, c.height * 2))


rows = []
t_all = time.perf_counter()
for i, r in enumerate(sample, 1):
    p = os.path.join(IMG, r["saved_as"])
    rec = {"id": r["id"], "file": r["file"], "saved_as": r["saved_as"],
           "stratum": r["stratum"], "tag": r["tag"], "kind": r["kind"],
           "bar": r["bar"], "bar_top_frac": r["bar_top_frac"],
           "bar_bot_frac": r["bar_bot_frac"], "bar_color": r["bar_color"],
           "ocr_cached": r["ocr_cached"]}
    t = time.perf_counter()
    rec["base"] = OF.ocr_one(p, reader=reader)                       # production path
    rec["ms_base"] = round((time.perf_counter() - t) * 1000)
    t = time.perf_counter()
    rec["full"] = OF.ocr_one(p, reader=reader, max_side=None)        # no downscale
    rec["ms_full"] = round((time.perf_counter() - t) * 1000)
    t = time.perf_counter()
    try:
        rec["bar2x"] = OF.ocr_one(bar_crop_2x(p), reader=reader, max_side=None)
    except Exception as exc:
        rec["bar2x"] = ""
        rec["bar2x_err"] = type(exc).__name__
    rec["ms_bar2x"] = round((time.perf_counter() - t) * 1000)
    rows.append(rec)
    print(f"  [{i:2d}/60] {rec['id']}  base={rec['base'][:44]!r}")

json.dump(rows, open(os.path.join(OUT, "ocr_runs.json"), "w", encoding="utf-8"),
          indent=1, ensure_ascii=False)
print(f"\ntotal {time.perf_counter()-t_all:.1f}s")
n = len(rows)
for v in ("base", "full", "bar2x"):
    ne = sum(1 for r in rows if (r.get(v) or "").strip())
    ms = sum(r.get("ms_" + v, 0) for r in rows) / n
    print(f"  {v:6s} non-empty {ne}/{n} = {100*ne/n:4.1f}%   mean {ms:6.0f} ms/img")
print("wrote scratch/bl709/ocr_runs.json")
