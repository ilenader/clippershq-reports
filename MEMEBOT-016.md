# MEMEBOT-016: The three blockers are fixed. Two of the other three were not what I said they were.

**Date:** 2026-08-01 · **Class:** Fix + measurement · **Spend:** **$0.0006** of the $0.05 budget — one paid call, for the one real render. Everything else reused bytes already on disk.
**Claim:** `MEMEBOT-016`, filed at start, declaring exactly which regions of `edit.py` and `config.yaml` I would touch.
**Files changed:** `memebot/scraper/edit.py`, `memebot/scraper/config.yaml`, `memebot/scraper/templates.yaml`, `scratch/memebot010_run.py`, and a new `memebot/scraper/tests/test_caption_fit.py`. All backed up (`*.20260801_161*.mb016.bak`). **No clippershq module was edited.**

**Tests: 65/65 suites, 2,824 checks, all green.** Plus 15 new caption tests (see the honesty note at the end about where they live).

---

## The proof, up front

| # | blocker | before | after |
|---|---|---|---|
| 1 | caption clipped | 1 line, **1304px on a 1080px canvas** | 3 lines, **853px**, ellipsized, inside the frame |
| 2 | bitrate | 16.15 Mbps / 82 MB | **2.82 Mbps** / 1.5 MB |
| 3 | dead black | **48.0%** of frame | **11.3%** — 76% less |
| 4 | `--dry-run` | $0.0018, exit 1 | **$0.0000, exit 0**, spend.json untouched |

Items 5 and 6 turned out differently. Details below, including a correction to my own INFRA-007 report.

---

## 1. The caption — two bugs, not one

**Root cause, `edit.py:511`:**

```python
return text, 22, 1        # <- the ORIGINAL, UNWRAPPED text
```

`compute_caption_layout` had four steps. Step 2 tried a **two-line** wrap; steps 1, 3 and 4 were all **single-line** shrinks. A caption too long for two lines fell past every step and hit that final `return`, which handed back the untouched original at 22pt. Reproduced exactly on the caption that shipped:

```
caption  : 118 chars, the real one from the ledger
result   : lines=1  size=22  widest=1304px  max_width=864
           OVERFLOWS max_width : True
           RUNS OFF 1080 CANVAS: True
```

**The second bug made the first one inevitable.** `templates.yaml` had declared `max_lines: 2` since it was written, with the comment *"informational; current auto-fit caps at 2 lines"* — and it was informational, because **nothing ever passed it in**. The fitter had no idea a line budget existed.

**The fix.** `_wrap_to_width` wraps greedily on word boundaries by *measured pixel width* (measuring, not counting characters — "Illinois" and "WWWWWWWW" are the same length and nowhere near the same width in Montserrat). `compute_caption_layout` now takes `max_lines`, tries the largest size that fits within that budget, and ends at `_ellipsize_to_box`, which trims until the text fits and **always returns something that fits**. Overflow is now structurally impossible rather than merely unlikely.

**`max_lines` raised 2 → 3**, on measurement rather than taste:

| budget | result on the caption that shipped |
|---|---|
| 2 lines | 38pt, keeps **74%** of the text |
| **3 lines** | **42pt, keeps 100%** |
| 4 lines | would start at y = −8 — off the top of the frame |

3 lines is both bigger type and the whole sentence. 4 is impossible, because `y: "275-text_h"` anchors the caption's bottom at 275px and a four-line block is taller than that.

**Proven on real renders.** Two frames sampled from actual output, text read back:

> `@Moviezar posts the best movie memes` / `on instagram daily Minions (2015) is an` / `animated film that explores the origins…`

> `Brad Pitt ruined Tarantino's original` / `script in the best way possible… Aldo` / `Raine was originally written to speak…`

Three lines, inside the frame, ellipsis where it was cut.

### The thing I found while fixing it: captions are 922 characters

Median caption length across 1,058 library captions is **922 characters**, because the stored caption is the poster's *entire* Instagram caption including the hashtag block — `#meme #memes #memeindonesia #fyp #fypage …`. Fitting that produces a correct, non-overflowing wall of hashtags: fixed, and still useless.

So `caption_headline()` now keeps the leading prose, stops at the first tag-only line, and strips any trailing inline tag run — falling back to the original if a caption is *only* tags, so nothing renders blank. **This is scope I added on my own judgement**, beyond "wrap it". I took it because without it the fix produces garbage that merely fits. Flagging it so you can reverse it if you disagree.

## 2. Grain — narrowed to 2–4

`frame_noise` is now `strength_min: 2, strength_max: 4`, the range MEMEBOT-011 recommended, with the reasoning written beside it. Eight live rolls from the config: `4, 2, 4, 2, 2, 4, 3, 3` — every one on the cheap side of the cliff (1.12×–1.26× the no-grain bitrate, against up to 9.91× before).

**Measured on the real render: 2.82 Mbps**, against 16.15 Mbps for the deliverable INFRA-007 caught. Honest caveat: that render was a different, shorter clip, so this is not a controlled A/B — Mbps is duration-independent, but content differs. The controlled evidence is MEMEBOT-011's table, where everything but grain was held fixed.

## 3. Letterbox — cropped before scaling

`detect_content_crop()` runs `cropdetect` over sampled frames and returns a crop, applied **first** in the chain, ahead of the zoom and the scale.

On the clip INFRA-007 measured: source `720x1280`, content `720x546` — **57% of the source was letterbox**.

```
without crop: scale=864:1640:force_original_aspect_ratio=decrease,...
with crop:    crop=720:546:0:334,scale=864:1640:force_original_aspect_ratio=decrease,...
```

Same source, same template, only the crop varying:

```
cropoff    black 48.0% of frame
cropon     black 11.3% of frame
  -> 36.7 points, 76% less dead frame
```

**The MEMEBOT-005 pad bug did not come back.** The scale still uses `force_original_aspect_ratio=decrease`, which absorbs any aspect the crop produces by shrinking to fit the box rather than trusting arithmetic to land exactly on 1920. Both A/B renders completed; no "padded dimensions" failure.

Safety, because a bad crop silently destroys the picture: `reset=0` accumulates the **largest** box across frames, so one dark scene cannot shrink it; the crop is rejected if it keeps under 20% of the frame (the signature of a genuinely dark clip rather than a letterboxed one); it is skipped unless it buys at least 2%; any probe failure returns `None` and is never fatal. Results are cached by path+mtime, and sampling at 4fps keeps it to a fraction of a full decode.

**One honest caveat on composition.** Removing 57% letterbox makes the *picture* smaller — the video band is now 655px instead of 1536px, and the template's white pad fills the rest. Dead **black** went 48% → 11.3%, but the frame is now bottom-heavy with **white**. That is the pad doing exactly what you asked ("fill only what is genuinely missing"), and white is the template's own colour rather than an artifact — but it is a composition question I deliberately did not answer, because redesigning `white_frame` is outside a claim scoped to three blockers. If you want the picture larger, the lever is `video.scale_width` (864 → 1080), which trades the white side margins for a bigger image.

## 4. `--dry-run` — free, and exits 0

```
RESULT memebot010: planned=3 calls=0 cost=$0.0000  (dry run)
EXIT CODE: 0
spend.json changed: False
```

The paid call happens inside `clip_pipeline.run_batch`, which retrieves *before* it consults `dry_run` — and that file is a clippershq module this round does not edit. So the fix is to never enter that path: `--dry-run` now plans exactly like `--plan-only` and stops. It also returns 0; it used to fall through to `return 0 if made else 1`, and a dry run always makes nothing, so a clean plan reported failure.

The module docstring claiming "no paid call" is now true instead of aspirational.

---

## 5. The library is not 32% duplicates. I was wrong about that.

**Correcting my own INFRA-007 report.** I counted raw rows and called the surplus "duplicates", implying corruption. It isn't.

Measured on a frozen snapshot (BL-851 is appending live, so I copied the bytes first):

```
rows 2580 | distinct clip_id 2003 | duplicate rows 577 (22.4%)
same file : 558      across files: 0
byte-identical: 3    differing: 555
fields that differ: provenance 544, rev 531, vision_scene 412,
                    vision_model 412, vision_beats 412, ...
rev present on 2580/2580 rows
```

Every surplus row carries a **`rev`**, and the differing fields are the vision columns BL-849 is writing right now. These are not duplicates — they are **revisions**. The library is an append-only log, and a re-labelled clip gets a new row rather than a rewritten one.

And the canonical reader already handles it:

```python
def read_all(root):
    """LAST-WINS by (clip_id, rev). This is what a consumer should call."""
```

It keeps the highest `rev` per `clip_id`. The orchestrator prints `library 2003 clips`, which is exactly the distinct count. **Nothing is double-counted and there is nothing to dedup.**

So I did not dedup it, and I recommend you don't either. The only real cost is parsing 2,580 rows to yield 2,003 clips — about 29% overhead in read time and disk. A compaction pass could reclaim that, but it is an optimisation, not a repair, and it must not run while BL-849 and BL-851 are both appending.

## 6. The two ledgers already collapsed into one — another round did it

`scratch/renders.jsonl` is **gone**. `memebot/runs.jsonl` has 26 rows. And `run_record` is no longer orphaned:

```
clip_pipeline.py: import run_record
```

MEMEBOT-017 claimed exactly this ("one ledger one writer, wire outcome_loop") and landed it while I was working. My own render is in the surviving ledger:

```
clip_id   3583723729168186711_5769514091
account   moviezar     status ok     cost_usd 0.0006
```

I did nothing here. Doing it would have meant editing clippershq under someone else's claim and risked producing the third format the brief warned about.

---

## Two things I fixed that nobody asked for

**The font was re-parsed on every measurement.** `ImageFont.truetype()` was called per width query, so a caption fit meant hundreds of `.ttf` parses. Now cached — necessary, because my measured wrap asks for many more widths than the old character-counting version.

**The ellipsizer was O(n²).** My first version walked back one word at a time, re-wrapping each round; the test sweep took **263 seconds**, and a render with a long caption would have paid the same. "Fits with N words" is monotonic, so bisection finds the identical answer in O(n log n). **263s → 39s.**

## State on exit

`config.yaml` picked up MEMEBOT-021's ambient-routing changes while I worked; my `frame_noise: 2-4` is intact alongside them. `edit.py` was written by MEMEBOT-021 mid-round — it declared it would touch only the ambient decision layer, and it kept to that; all my functions survived, verified by name. The claim-by-region protocol worked: four rounds declared overlapping interest in these two files and none clobbered another.

## Limits, and one that matters

**My 15 caption tests do not run in CI.** `tests/run_all.py` scans `tests/test_*.py` only, and I put them in `memebot/scraper/tests/test_caption_fit.py` next to the module they test, matching `test_duck.py` and `test_edit.py`. They pass — `Ran 15 tests, OK` — but you must invoke them: `cd memebot && python -m unittest scraper.tests.test_caption_fit`. Nothing in the 65-suite run covers the caption fitter. That is a real gap and I am naming it rather than letting "all green" imply coverage it doesn't have.

Two suites (`test_ig_clips_fallback`, `test_repost_finder`) were red on an intermediate run and green on the final one; both pass in isolation, both import only clippershq modules I never touched, and one passed and failed across consecutive full runs. Flaky under eleven concurrent rounds, not caused by these changes — but I cannot prove a negative about a flake.

The bitrate figure is one render of one clip; grain rolls per render, so another run lands elsewhere in 1.12×–1.26×. The crop A/B is one clip — a source with *no* letterbox correctly gets no crop (the 2% gain floor), but I did not sweep the library to count how many clips benefit. The caption fix is proven on two real renders and 15 synthetic cases including 2,400-character input; I did not re-render all 2,003 clips. I did not listen to any audio this round.
