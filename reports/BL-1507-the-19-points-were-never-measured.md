# BL-1507 — his four decisions, and the 19 points that were never measured

**Round:** BL-1507 · **Filed:** 2026-09-05 · **Cap:** $1.00 · **Spent: $0.0168** (28 billed
vendor calls, counted by the run's own counter, never a ledger delta)

---

## What shipped, with its fix category

| # | change | file(s) | category |
|---|---|---|---|
| 1a | the 1.4 s floor, re-spread, and `short_clips()` | `clippershq/frame_text.py` | **GENERAL** — every caller of `extract_frames` |
| 1a | one owner for the constant (imported, not retyped) | `clippershq/frame_text.py` ← `video_strip.py` | GENERAL |
| 1b | 9 Instagram/edits reject exemplars | `output/bl1507_ig_edits_rejects/` | data |
| 1c | `mode` stamped at write time, both manifest generations | `score_sheet.py`, `outcome_sheet.py`, `bl1397_build_sheet.py`, `bl1442_sheet.py` | **GENERAL** — every sheet any of the four builds |

No judging rule was added or loosened. No threshold was moved.

---

## 0. The one-line answer

**All four of his decisions are implemented and proved by driving the real code.** But the
figure that justified the largest of them — *"the 1.4-second rule is worth 19 points: frame zero
79.2% text readability, two seconds in 98.4%"* — **does not exist anywhere in this repo**, and
when I measured it properly on 48 clips it is **worth nothing measurable at all**: +1.7 points
pooled (p = 0.227), and **−0.6 points on the population where his rule actually binds**
(p = 1.000).

The rule still ships. It is his instruction, and it removes a real worst case. But it is a
**correctness fix, not an accuracy win**, and the next round to plan around those 19 points
would be planning around nothing.

---

## 1a. The 1.4-second rule: implemented — and its justification refuted

### What was wrong

`HERO_T_DEFAULT = 1.4` sits at `clippershq/video_strip.py:324` under a comment quoting him
directly: *"take the text frame at the first or second second, not at zero."* It had **zero
production readers**. Its only references anywhere were two bounds assertions in
`tests/test_bl1469_hero_and_counters.py`. It was a comment with a number attached.

Meanwhile `frame_text.extract_frames` sampled frame *i* at `dur * (i + 0.5) / n`, so with the
shipped `n = 6` the **first frame landed at `dur/12`** — crossing 1.4 s only at a clip length of
**16.8 s**.

### What shipped

`clippershq/frame_text.py` now **imports the constant from its one owner** (no second copy of
1.4 to drift), floors the first sample, and re-spreads the rest:

```python
floor = min(HERO_T, dur * 0.8)      # a clip shorter than 1.4 s cannot honour the rule;
span  = max(0.0, dur - floor)       # clamp INSIDE the clip, never seek past its end
at    = floor + span * (i + 0.5) / float(n)
```

**Fix category: GENERAL.** It changes the sampling rule for every caller of `extract_frames`,
not a `t` at one call site. Clips too short to honour the rule are **recorded** via a new
`short_clips()` accessor rather than silently clamped — *"the rule was applied"* and *"the rule
could not be applied"* are different facts.

Re-spreading rather than `max(HERO_T, at)` is deliberate, and the reason is **correctness, not
accuracy**: `max()` collapses the first several samples of a short clip onto one instant. On
**2 of 28** measured clips the floor-only rule produced fewer than *n* distinct timestamps, and
the frame-agreement vote downstream would have counted one frame two or three times.

### The measurement he asked for — same clips, same question, before and after

48 clips fetched fresh from the vendor, each downloaded **once** and cut under **both** samplers,
every frame OCR'd with RapidOCR through the shipped `clip_ocr.reader()`. *Readable* was defined
before measuring and identically for both arms: **≥1 OCR box at confidence ≥ 0.60 with ≥3
characters**. Two controls fired first — a frame with text known to be present read as readable
(1/1), a blank frame did not (0/1) — so a zero below is the clip, not the engine.

⚠️ **The clip, not the frame, is the unit of analysis.** Six frames cut from one clip are six
looks at the same content; if a clip carries no on-screen text all six fail together. Quoting
288 frames as 288 trials would shrink every interval by roughly √6 for free.

| population | arm | old → new | clips better / worse | sign test |
|---|---|---|---|---|
| **17 of 28 clips sampled before 1.4 s** — the population his rule is *about* | **his rule alone** | 89.9% → **89.3%** (−0.6) | 0 / 1 | **p = 1.000** |
| same | floor + re-spread (shipped) | 89.9% → 88.7% (−1.2) | 0 / 1 | p = 1.000 |
| same | the re-spread alone | 89.3% → 88.7% (−0.6) | 0 / 1 | p = 1.000 |
| long edits clips, 4 of 20 below the floor | shipped | 71.7% → **77.5%** (+5.8) | 8 / 2 | p = 0.109 |
| **pooled, 48 clips** | shipped | 82.3% → **84.0%** (+1.7) | 8 / 3 | **p = 0.227** |

**Not one arm is distinguishable from no effect.**

And the reason is visible in the raw rows: the population where his floor binds is **short meme
clips**, and there readability is **already saturated at 6/6**. There is no headroom to win.
The apparent +5.8 came from the long-clip sample, where the floor barely binds at all — so it
cannot be credited to his rule either.

### ⚠️ The 19 points: traced, and it is not a measurement

I checked the number that **authorises my own work**, which is the easy one to leave alone.

A word-boundary scan of **12,234 files** (`scratch/bl1507_trace_19points.py`) finds the pair
`79.2` / `98.4` on **exactly two lines in the entire repository**, both docstrings in
`scratch/bl1499_strip_build.py`:

> *"Measured elsewhere: frame zero scores 79.2% text readability, two seconds in 98.4% — 19
> points from one setting."*

Its ancestor, `scratch/bl1475_corpus2.py:11`, says: *"a measurement someone already paid for."*
**Neither names a round, a file, a denominator or a date.** No report, no dataset, no output
file anywhere contains the figure. Every `79.2` that appears in a report is a **different
quantity** — a fan-page guard's accuracy (BL-1167), a cost cut (BL-1300), or the upper Wilson
bound of `75.8% [72.1, 79.2]` (BL-1475/1493/1495).

⚠️ **BL-1504 did not measure it either.** Its *"17 of 30 clips"* is real and reproduces, but it
is **pure arithmetic**: `midpoint_table()` computes `dur/12` from a list of durations. That
round never cut a frame or ran OCR. Its own text says so — *"reporting it instead"*.

So the brief's "19 points" is **two unrelated things fused**: BL-1504's timestamp arithmetic,
and a readability figure with no origin that has propagated through docstrings for three rounds.

**I repeated it myself.** My first version of the shipped comment stated 79.2/98.4 as measured
fact. That comment is corrected in place and now carries the measurement above.

⚠️ **First-run correction:** my first sample drew only from the edits list and landed on clips of
15–63 s, where the floor binds on 4 of 20 — a sample that could not test the rule it was
measuring. The three-arm re-run mixing in meme pages landed at **17 of 28 below 1.4 s, earliest
0.425 s**, which reproduces BL-1504's profile (17 of 30, earliest 0.417 s) almost exactly. Both
runs are reported; the pooled figure is the *weaker* evidence, not the stronger.

---

## 1b. The Instagram/edits reject side — 13 filled, 9 shipped

**All 13 rejects on `output/bl1427_edits_instagram/` — the sheet he actually typed on — resolve
to the sheet's OWN picture, 0 matched from elsewhere.** "Own" is manifest-attested: the sheet's
`rows_000.json` names `img/<handle>.png` for every row, so it is not inferred from a directory.
Scores: eleven 1s, one 3, one 4. **Four were disqualified, so 9 shipped** — a real shortfall,
not padded.

**This corrects BL-1504.** Its table said 10 of 13 had the sheet's own picture; its prose said
13 of 13. **The prose was right** — the table's image index tokenised filenames and missed three.

### ⚠️ Two corrections that changed the answer

**1. The first battery measured the wrong builder and was wrong by 8 pages.** Run unchanged from
BL-1500, it disqualified **12 of 13**. But these are not TikTok contact sheets: every picture is
a paid grid from `clippershq/paid_grid.py` — 1720 px wide, `CELL_PX=560`, `COLS=3`, **variable
row heights**, canvas **WHITE (255,255,255)** at `paid_grid.py:189`. The RGB(24,24,27) canvas is
`tiktok_finder.py:1606`, correct for TikTok, and on this corpus it reads **0.5% blank on a page
that is 76.7% bare**. Rebuilt against the real builder: **4 of 13**. The void instrument is kept
with a banner marking its numbers dead.

**2. "Mostly white" is not "empty" when the canvas is white.** At tol=10 a fully drawn white
quote card reads **94.9% blank**, and a ≥0.90 rule called **four drawn covers empty** on two
pages. Emptiness is now decided at tol=0 — a cell the builder never painted is *exactly* the
canvas colour — gated on a planted white-text-card negative control.

### Disqualifiers, each with the control that fired

| disqualifier | count | control |
|---|---|---|
| BLANK (unpainted cells, exact) | 1 | white reads 1.00, detail reads 0.00, text-card is not empty |
| EMPTY CELLS | 1 (same page) | 1-tile sheet → 3 cells, 1 drawn, 2 empty |
| REPEATED COVER (cells hashed, not files) | 1 | repeat9 reads 8, distinct9 reads 0 |
| HANDLE PRINTED IN THE GRID | 2 | fires on a 7 px semi-transparent watermark at real tile scale |
| LOGIN WALL / AGE GATE / PRIVATE | **0 each** | all three fired on planted positives — these are **measured zeros** |
| EMAIL PRINTED | 0 | positive and negative both fired |

**26 controls, 26 fired. `UNMEASURED` is empty on all 13.** The nine geometry controls are built
*by* `paid_grid.build_sheet` itself, so their geometry is the real geometry — and the repeat9
control caught a genuine off-by-ten-pixels bug in the row recovery.

⚠️ **The chooser moved one of these.** Resolved through the **current shipped**
`meme_finder._pick_grid` (11,159 stems, controlled both directions), **1 of 21** pages now
returns a *different file by content* than the sheet's own. The sheet's own was used, because
the manifest names it. Identity is sha256 **of the bytes** plus realpath and size throughout,
with a one-byte-flip control proving the comparison moves.

### The held car pool: 11, held and unused

**Rejects by the brief, not by his keystroke** — TikTok/edits pages he scored 6–9 (a KEEP) whose
subject the edits brief reverses. All have the sheet's own picture; **0 contributed to the 13**,
proved by an overlap test with a positive control.

⚠️ **A false zero caught inside this work:** a handle-only sweep reported **0** reversed-subject
pages among the 21 Instagram/edits handles. With the discovery keyword added it finds **2** — one
KEEP found via `reels:car edits` (now held, taking the pool to 11) and one page he scored **1**,
found via `reels:motivation quotes`, which is a reject by *his own keystroke* and stays in,
flagged.

### Denominator, stated both ways

The 18-file BL-1504 corpus gives 21 pages / 13 rejects. A whole-repo `discover()` gives only
11 / 7, because `resolve()` refuses mode adoption for 10 handles that also appear on meme
sheets. The curated corpus is the right denominator; the wide sweep is reported, not hidden.

**8 of 8 verification checks pass**, each with a control — including **no handle in any
filename** (9 files × 21 handles, with a planted-handle positive control) and *measured drawn
cells == the funnel's own `tiles_read` note on 13 of 13*, an independent witness written months
earlier.

⚠️ **The nine PNGs are on disk at `output/bl1507_ig_edits_rejects/` but are NOT in git** —
`.gitignore:98` excludes `output/`. That is the same place, and the same status, as the existing
pinned exemplar grids (`output/bl1428_grids/`), so this matches how every pack in this project
already lives. The measurements about them are committed; the pixels are not.

---

## 1c. Mode stamped at write time — 14 write sites, 0 recorded a mode

### What was wrong

An AST census over every `.py` in `clippershq/ tools/ scratch/ dashboard/ tests/` found **14
sites that write a sheet manifest and 0 that record a mode.** Downstream,
`tools/mark_reader.py` recovers the brain from the **directory name** — so an edits sheet built
into a directory that does not spell "edits" was filed as memes, silently, and every per-brain
figure computed from it is wrong in a way nothing prints.

Positive controls on the same method and the same 14 sites: `platform` found in 4 payloads,
`sheet_id` in 5, `mode` in **0** — while the literal string `"mode"` occurs 19 times in those
same files. The zero is real, not an artefact of the instrument.

**There is no single shipped builder.** Four functions write a real sheet manifest and they
disagree about the filename:

| builder | writes | note |
|---|---|---|
| `scratch/bl1397_build_sheet.py:470` | `sheet_meta.json` | the de-facto shipped builder — all 15 newer-generation sheets on disk are its |
| `scratch/bl1442_sheet.py:231` | `sheet_meta.json` | a copy of the above |
| `clippershq/score_sheet.py:262` | `meta.json` | **no production caller**, yet it wrote 7 of the 8 older-generation sheets |
| `clippershq/outcome_sheet.py:347` | `meta.json` | send outcomes, not a graded review sheet |

### ⚠️ The finding inside the finding: the mode was already on disk, one level too deep

`output/bl1427_edits_instagram/meta.json` and `output/bl1427_edits_tiktok/meta.json` **already
carry `stats.mode = "edits"` and `reconcile.mode = "edits"`**. `mark_reader` does `j.get(k)` —
**top level only** — so it has never seen either, and has been falling back to the directory
name for sheets that state the answer one level down. For `score_sheet.py` this fix is therefore
a **lift of a value the caller already supplies**, not a new value invented here.

### What shipped

All four builders now stamp `"mode"` at the top level **and write both manifest generations**.
Eight sheets on disk carry only the older name and the two names have **never co-occurred**, so
any reader knowing one name silently missed a third of the corpus. Both readers walk
`("sheet_meta.json", "meta.json")`, take the first that parses and stop — so identical content
under both names is safe today and removes the failure mode permanently.

A builder that genuinely does not know writes **`None`**, which `mark_reader` prints as NOT
RECORDED. Defaulting to `"memes"` would manufacture the exact false fact this is meant to stop.

### Proved by driving the real code

Not a grep, not a docstring, not a passing test. Each builder was **called**, into a throwaway
directory, and the manifest read back with the **shipped reader**:

| arm | mode read | source | verdict |
|---|---|---|---|
| `bl1397_build_sheet.build` | `'edits'` | `sheet_meta.json:mode` | OK |
| `bl1397` with **no mode set** | `None` | — | OK (honest blank) |
| `bl1442_sheet.assemble` | `'memes'` | `sheet_meta.json:mode` | OK |
| `score_sheet.write_sheet(mode=)` | `'edits'` | `sheet_meta.json:mode` | OK |
| `score_sheet` with **`stats.mode` only** | `'edits'` | `sheet_meta.json:mode` | OK — the lift works |
| `score_sheet` with **no mode anywhere** | `None` | — | OK (honest blank) |
| `outcome_sheet.write_sheet(mode=)` | `'edits'` | `sheet_meta.json:mode` | OK |

**7 of 7 arms pass; 7 of 7 write both generations.**

⚠️ **The control is the directory name.** Every probe directory was named `probe_a`…`probe_g` —
mode-free — so a reader that still recovered "edits" could only have got it from the manifest.
Building into a directory called `edits` would have let the old fallback pass the test, which is
how a fix gets credited to itself.

**Fix category: GENERAL for the writing side** — every sheet built by any of the four gets a
stamp from now on, whatever its directory is called. It does **not** retro-fix the 25 manifests
already on disk; those still depend on the directory-name fallback, which is stated here rather
than fixed by rewriting his delivered sheets.

### No verdict moved — controlled, per platform

| platform | file inventory | `rows_*.json` (these carry the verdicts) | manifest keys that differ |
|---|---|---|---|
| tiktok | same | **byte-identical** | `['mode']` — `None → 'edits'` |
| instagram | same | **byte-identical** | `['mode']` — `None → 'edits'` |

⚠️ The comparison **excludes the manifests** and then compares them separately: the manifest is
*supposed* to differ, so a whole-directory diff would report the intended change as a regression
and prove nothing. `built` and `sheet_id` are timestamps and are excluded by name. And the
control can fail — **a one-byte flip in a rows payload is caught (True)**.

---

## 2. What the 21 flipped pages invalidated — re-derived

The mark reader keyed on `(platform, handle)` while platform was the thing being inferred, so
pages landed under two keys and ran two private last-keystroke-wins races.

**First question: is the key already fixed? Yes — and it was verified, not taken on trust.**
`tools/mark_reader.resolve()` carries the BL-1504 adoption pass, committed at `b6a78bb`. Three
keyings re-derived independently on the same marks:

| keying | pages (26-file kept corpus) | pages (all 30 candidates) |
|---|---|---|
| PRE-FIX raw `(platform, handle)` | 1,587 | 1,787 |
| SHIPPED `resolve()` | 1,514 | 1,681 |
| **key = HANDLE (independent)** | **1,511** | **1,678** |

The pre-fix key invented **76 phantom pages** on the kept corpus and **109** on the full
candidate set. The shipped reader lands within **3** of the independent answer, and those 3 are
handles whose marks name **two different platforms** — the reader refuses to merge them, and
that refusal is **correct**: one handle can exist on both networks. **There is no residual bug.**

### The figures, old against new

| figure | denominator | OLD | NEW | moved? |
|---|---|---|---|---|
| **Ceiling** (file-collapse) | pages graded in ≥2 distinct sittings | 75.8% 135/178 [69.1, 81.5] | **75.6% 136/180 [68.8, 81.3]** | no |
| Ceiling, independent 2nd derivation | sittings read off the **clock** (6 h gap) | — | **74.2% 115/155 [66.8, 80.4]** | confirms |
| **Obvious pages** (score 1 or 10) | repeat-graded, in band | 91.1% 51/56 | **89.2% 83/93 [81.3, 94.1]** | **yes, −1.9 on a 1.7× denominator** |
| **Near his line** (5, 6, 7) | same | 50.0% 10/20 | **48.0% 12/25 [30.0, 66.5]** | yes; still spans 50% |
| Near his line, tight (5, 6) | same | — | **41.2% 7/17 [21.6, 64.0]** | new |
| **Sweep @90 kills** (unanimous truth) | pages an authorised cutter answered | 3/76 = 3.9% | **3/71 = 4.2% [1.4, 11.7]** | denominator only |
| **Sweep @90 under LAST KEYSTROKE WINS** | same | *never published* | **5/84 = 6.0% [2.6, 13.2]** | **yes — the big one** |
| Catches @90 | his low-scored pages | 58.0% | **52.7% [43.5, 61.7]** | yes |
| Traffic removed @90 | all answered pages | 36.9% | **33.9%** | yes |
| **Constant answer** | *unscoped in the old figure* | 61.5% always-reject | **58.1% / 66.1% / 56.4% / 59.1%** by scope | **yes — no single value exists** |
| **seed** approval | marked pages with a `found_via` | 38.6% (17/44) | **31.9–37.6%** on 93–222 pages | **yes — denominator 2–5× too small** |
| **hashtag** approval | same | 33.3% (24) | **25.0–35.2%** on 28–593 pages | yes |
| **reels** approval | same | five published values | **73.8–82.9%** across 12 readings | explained, not resolved |

At every threshold, at 100 the sweep cuts nothing (0/84, 0/71) — the curve is real, and **no
threshold clears a 95% floor on kills**. That old conclusion survives.

**Corpus:** 30 candidate mark files found by `os.walk` on provenance (never field shape — a
whole-repo shape sweep admits 5,094 files / 631,082 records). 26 kept, 3,367 marks, **1,511
resolved pages**.

**Four excluded, and one of them is new:** `ground_truth/BL-1296-FRESH100_marks.jsonl`
reproduces `judge_verdict` on **96 of 100** rows with all 100 `reason` fields empty — it is the
judge's own answer, and **it was inside previous ceiling figures.** Also excluded: the
BL-1257 pair (97/100 reproduction, no reason field at all; one is a byte-identical duplicate,
md5 `07758df4…`) and `bl1296_his_marks.tsv`, which is the same sitting under another name.

**Kept despite the filename:** the three `DO_NOT_USE_THIS_SHEET.txt` folders whose own text
reads *"your marks in this folder are kept and are still used as ground truth"* — 266 marks. The
other 11 such folders hold zero.

**Seven zero-controls passed**, including: the reader's semantics are not inverted (623 rows
agree, 0 differ); **335 authorised REJECT answers exist (157 at ≥90)**, so a zero kill count
would have been meaningful; and **552 unplatformed pages were left unassigned, never guessed** —
no page was put in a brain it does not carry.

⚠️ **One second derivation was computed and then refused.** A "declared sitting stamp" reading
gave 85.5% (259/303) and is **refuted**: two mark files carry different stamps for the *same*
sitting, so it counts 303 repeat pages where there are 180 — a copy agreeing with itself. The
valid second derivation is the clock-based 74.2%.

---

## 3. Part 3 — the instruments, re-taken

### The pack signature, now over CONTENT

This one control has now been wrong twice in two different ways:

| version | hashed | defect |
|---|---|---|
| v1 (BL-1505, first attempt) | `os.path.basename` | **blind by construction** — the thin capture and the full sheet *share a filename* and differ only in directory |
| v2 (BL-1505, shipped) | relpath + `getsize` | misses a file **rewritten in place at the same length** — exactly what a re-render at the same layout does |
| **v3 (here)** | **the file bytes** | answers the question the control is actually asking |

Both directions controlled: a rename with identical bytes **holds** the signature; a rewrite in
place at an **identical 508 bytes** **moves** it — and the v2 signature is demonstrated to miss
that same case.

**The result, over all six call shapes:**

| call | signature | pictures |
|---|---|---|
| tiktok/memes · tiktok/edits · instagram/memes · instagram/edits · instagram (shipped call) · no platform | **`dac6e900648e` — all six identical** | 8, all byte-distinct |

**Every brain receives byte-identical pictures.** `platform=` and `mode=` change nothing. This
**confirms** what `_exemplar_pack`'s own comments claim — the per-mode and per-platform approved
lists are empty, so every caller falls back to the one pinned TikTok pack — but it is now
established over **bytes across all six shapes**, where previous rounds measured two shapes at
the network boundary. No pack shows a picture twice.

### My own guards with the `if line in brief_text` shape

An AST sweep (not a grep — a grep for `" in "` matches every `for` loop, which is the same
mistake the sweep is looking for) over `tests/ scratch/ tools/ clippershq/`, controlled in both
directions:

- **430** substring guards over a proven-text haystack, **4,039** where the haystack type could
  not be proven (reported, not dropped — "unprovable" and "safe" are different facts)
- of the 430: **29** are character-class membership (`if ch in "{["` — correct code), **309**
  ask a real question about prose or data, and **92 search Python source**, which is the shape
  that can lie
- of those 92, **24 sit in `tests/`, `tools/` or `clippershq/`**, where they gate something

⚠️ **430 is not the answer, and publishing it would have been the same mistake the scan is
about.** The shape is only a defect when a guard asserts *that a rule is in force* by looking
for its text in source — where a match inside a comment, a docstring or a longer identifier
reads as "the rule is live".

---

## 3b. The suite — and three standing reds that are not mine

⚠️ **Coverage is stated by what it covers, not by a total.** The full runner takes 44.3 minutes
and my execution ceiling is under ten, so three partial full-suite runs plus one slice covered
**~150 of 444 suites**. To make the coverage of *this change* complete rather than sampled, I
enumerated **every test in the repo that names any of the five files I touched** — or
`HERO_T`, `extract_frames`, `write_sheet`, `sheet_meta` — and ran all 23:

**20 pass. 3 fail, and all three were already failing in BL-1496's full run, before this round
existed.** I checked their causes rather than accepting the label, because a standing red can
acquire a second cause:

| suite | cause | mine? |
|---|---|---|
| `test_bl1307_veto_refused` | an untracked `scratch/bl1441_ast_sink_tests.json` from **30 August** | no |
| `test_bl1444_board_and_sheets` | `config.json` carries `tiktok_finder.picture_judge: true`; config last written **2 Sept** | no |
| `test_silent_zero_shape` | `clippershq/main.py:203 _cap_backups()`, plus a ratchet entry for `meme_finder._png_area` and `mark_reader.load_records` | **the `_png_area` entry is mine, from BL-1505** |

⚠️ **`_png_area` returns 0 on any `OSError`, so "could not read this file" scores the same as
"this file has no area".** I introduced that in BL-1505 and it shipped. I am **not** fixing it
here: the honest repairs are to raise or to narrow the handler, both of which change a shipped
grid chooser's failure behaviour, and doing that without measuring how often a candidate is
actually unreadable is how a settled decision gets reversed on a guess. It is reported so the
next round can price it rather than inherit it silently.

None of the three reds involves `frame_text.py`, `score_sheet.py`, `outcome_sheet.py`,
`bl1397_build_sheet.py` or `bl1442_sheet.py`.

---

## 4. Which published numbers are now wrong

1. **"The 1.4-second rule is worth 19 points."** It is worth **nothing measurable**: +1.7 points
   pooled on 48 clips (p = 0.227), **−0.6 where the rule actually binds** (p = 1.000). The
   79.2%/98.4% pair has **no source in this repo**.
2. **"61.5% always-reject"** — unscoped and unreproducible as a single number. It is 58.1% /
   66.1% / 56.4% / 59.1% depending on the pool. Always-reject beats always-want in every scope.
3. **"91.1% on obvious pages"** → **89.2%** (83/93). **"50.0% near his line"** → **48.0%**
   (12/25); the conclusion strengthens, since the interval still spans 50%.
4. **The sweep's headline kill rates were computed under unanimous-marks truth, not his
   documented last word.** Under last-keystroke-wins, @90 is **6.0% (5/84)**, not 3.9%.
   Unanimity discards exactly the pages he changed his mind about — the population the ceiling
   says is hardest.
5. **Sweep denominators 195/76 and 175/68** → 183/71 and 163/63 (unanimous) or 214/84 and 193/75
   (last keystroke). **Catches @90: 58.0% → 52.7%. Traffic: 36.9% → 33.9%.**
6. **seed 38.6% (17/44)** and **hashtag 33.3% (8/24)** do not reproduce on any of 12 readings.
7. **The five "disagreeing" reels readings are not a disagreement** — 73.8 / 75.6 / 79.4 / 80.6 /
   81.8 / 82.9 all fall out of **one dataset of 33–42 pages** under two binary choices. None
   should be quoted alone. **The ranking survives every reading:** reels and search above seed
   and hashtag, reels/seed intervals disjoint.
8. **`ground_truth/BL-1296-FRESH100_marks.jsonl` was inside previous ceiling figures** and is
   96/100 the judge's own answer.
9. **"100 of 100 reproduction"** cannot be reproduced. Across 12 files with ≥50 comparable rows
   the maximum anywhere is **97/100**. Do not repeat the claim.

**75.8% itself is NOT wrong.** It reproduces at 75.6% [68.8, 81.3] on a two-page-larger
denominator and is independently confirmed at 74.2% by a derivation sharing no mechanism with it.

---

## 5. What I got wrong this round

* **I shipped a NameError and my own AST check did not catch it.** Patching `score_sheet.py` I
  added `mode` to the manifest body while the edit adding `mode=` to the signature silently
  failed to apply. `ast.parse` passed — an unbound name is valid syntax. This is the **same
  shape as BL-1496**, where a kwarg added to `record_spend` whose arithmetic lived in
  `_record_spend_locked` shipped a NameError on every call. Fixed within the minute, and I wrote
  `scratch/bl1507_unbound_names.py` — which asks, per function, which names are read but never
  bound — so the class is caught next time rather than the instance.
* **That checker's first version reported 69 unbound names in correct code**, 56 of them `self`,
  read inside a handler class defined within `make_handler()`. `self` is bound by the *method*,
  not the enclosing function. I fixed the checker, not the code — a guard going red on correct
  code is the failure mode this repo keeps paying for.
* **Both measurement runs wrote to the same JSON path**, so run 2 overwrote run 1's per-clip
  rows. Recovered by parsing run 1's log, and the recovered rows are flagged as such. An output
  path that does not carry the run's identity will be clobbered by the next run.
* **My first trace for the 19 points printed real creator handles.** A bare `79.2` matched
  `ratio79.2x` inside `master_leads.csv`, giving 3,463 hits that were almost entirely one CSV
  column. Re-run with word boundaries and the lead stores excluded: 495 hits. Nothing from that
  run was written into the repo or committed.
* **My first readability sample could not test the rule it was measuring** — long clips only, 4
  of 20 below the floor. Re-run with a real duration spread.

## 6. What the brief got wrong

* **"It is worth 19 points."** Traced to two docstring lines citing "measured elsewhere". No
  source, and measured properly it is not distinguishable from zero. This is the brief's central
  premise for Part 1a.
* **"17 of 30 measured clips sample earlier"** is right about the arithmetic but the word
  *measured* overstates it — BL-1504 computed `dur/12` from durations and never cut a frame.
* **"Frame zero"** — the shipped sampler never took a frame at zero. Its earliest sample across
  48 clips was **0.425 s**, and the median was 1.57 s.

---

## 7. Spending — booked explicitly

**$0.0168 against a $1.00 cap.**

⚠️ **`clippershq/api_client.py` contains no booking of any kind.** A sweep for `record_spend`,
`_book_paid_call` and `record_aux_spend` across it returns nothing — so every LamaTok search
this round made was **invisible to the ledger**, as is every LamaTok search any round has ever
made through that client. They are now booked explicitly:

```
BOOKED: 28 LamaTok calls x $0.000600 = $0.0168 under campaign BL-1507
rows before 26,364 -> after 26,365   added: 1   mine: 1
my row: calls=28  dollars=0.0168
```

⚠️ **The count is the run's own in-process counter (12 + 16, each printed by its run), never a
ledger delta** — `spend.json` is shared, and its mtime moved at 15:16 today, hours before my
first call. And the safety check is the **row**, not the total: exactly one row carrying my
campaign and my call count, which a concurrent peer write cannot break. Comparing totals was the
shape of a false alarm in BL-1496.

The price is LamaTok's **$0.000600**, not HikerAPI's $0.00069064 — BL-1496 established these
must never be unified. Video
downloads are unbilled CDN GETs. Every video was deleted as soon as its frames were cut and the
delete verified **after** by listing the directory — **0 leftover non-PNG files across 48 clips**
— and free space was re-read before every batch with a 5 GB abort floor.
