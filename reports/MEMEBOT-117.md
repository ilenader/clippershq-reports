# MEMEBOT-117 — The detector is right to the pixel, and the trim is still refused

**Round:** MEMEBOT-117 · **Date:** 2026-08-03 · **Spend:** **$0.00** (budget $0.30 — the
renders are local ffmpeg and this round bought nothing)
**Claim:** `MEMEBOT-117`, repeated `--write` flags. Preconditions read per target:
`tools/claims_read.py --holders <path>` (all FREE) and `git status --porcelain` **by column**.
`memebot/` is its **own git repository** (MEMEBOT-048) — committed in both.

Acts on [MEMEBOT-115](https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/MEMEBOT-115.md),
whose findings are the starting conditions and are **not re-derived**.

> **THE RESULT IN ONE LINE.** I built the detector MEMEBOT-115 specified, scored it **16/16**
> against 40 hand labels, proved it defeats the dark-caption-bar case that killed 115, wired
> it, rendered 20 and read the frames — and **six of six trimmed renders came back with the
> source's headline sliced.** The detector is not the problem: measured against the first
> inked column it is off by **0 px on 8 of 11** sources. **The padding boundary *is* the
> headline's boundary.** With a safety margin sized from the renderer's own zoom, **0 of 40
> labelled sources have any horizontal slack left.** The axis stays pinned — now for a
> reason that closes the question instead of deferring it.

---

## 0. CLEAN ON ARRIVAL

`memebot/scraper/edit.py` at `76aa802` carries **no duplicated working-tree markers** — no
`<<<<<<<`/`=======`/`>>>>>>>` and no duplicated `def` (3,337 lines, every function name
unique), checked against **HEAD** rather than the worktree. Nothing to remove and nothing of
anyone else's committed as mine. `runs.jsonl` is ` M` throughout from another writer's
appends and was **not** committed.

---

## 1. THE DETECTOR 115 SPECIFIED, AND THE TWO LINES THAT HAD FAILED

115's rule was *"a column counts as padding only if it is near-uniform down its full height
and matches the corner"*, built so a caption bar could not pass. A **light** bar cannot. A
**dark** one can — over an inset picture the edge columns are bar-dark above and
letterbox-dark below, uniform all the way down, **carrying the caption's first and last
letters**. Reading the code, that happens for two specific reasons:

| # | the defect | the fix |
|---|---|---|
| 1 | **The test was on MEANS.** `col.std(axis=0).mean()` and `\|col.mean(axis=0) − corner\|` average **down** a 1920-row column; a 26 px letter stroke moves them ~1%. *The average of a column containing ink is not its brightest row, and the brightest row is the whole question.* | a per-pixel **MAXIMUM** over all rows |
| 2 | **It ran at 160 px wide.** 1080 → 160 puts 6.75 source columns in each sampled one, so the resampler blended anti-aliased text into the bar **before the test saw it**. | **full resolution**, no `scale` in the path |

A column is padding only if **every pixel** in it is within `PAD_INK_TOL = 24` of the pad
colour. One inked row disqualifies it — "no row carries ink" as code, not as an intention.

**Kept from 115 unchanged, because it was right:** sampling at 5/25/50/75/95% of duration and
taking the **minimum** (its widening fixture caught the front-loaded version cutting 66 px of
picture per frame), skipping globally-uniform frames, returning `None` on any failure.

---

## 2. FORTY HAND LABELS — MINE, MADE BEFORE THE DETECTOR RAN

**Never scored against another detector.** That circularity produced a fake 4.15× here once,
and **four detectors in this sequence have been wrong in the same direction** — which is
exactly what two agreeing instruments look like.

> **The bar, stated before any verdict.** **PILLARBOX** — uniform vertical canvas strip left
> and/or right of the picture, present in **all three** sampled frames, **≥ 5%** of width.
> **DARK_BORDER** — under 5%, or a matte belonging to the picture itself. **FULL_BLEED** —
> picture reaches both side edges in at least one frame. **UNREADABLE** — excluded, not
> counted as a negative.

Deterministic sample: sorted corpus of **786 sources**, every 19th, first 40 — it re-runs
identically and cannot be drifted toward whatever flatters the detector. Three frames per
source, because one frame is not a video.

| Class | n |
|---|---:|
| PILLARBOX | **16** |
| FULL_BLEED | 21 |
| DARK_BORDER | 1 |
| UNREADABLE (excluded) | 2 |
| **scored** | **38** |

16 of 38 = **42.1%**, reached independently of 115's 47.4% and without using it.

### My own contact-sheet reading was wrong on three of forty

Four borderline sources were re-read from a **full-resolution edge crop with a 10-px ruler**,
and **three of my four calls flipped** (05 and 28 and 39 to PILLARBOX, 34 to DARK_BORDER).
A label set taken from the contact sheet alone would have been wrong on 3 of 40 — and those
are exactly the sources a detector is judged on.

**On one, my eye was flatly worse than the instrument.** On #39 I estimated the right border
at ~25 px; the column deviations go `0.0 → 0.0 → 6.0 → 180.0` and the boundary is razor-sharp
at **54**. Recorded because it cuts against my own labels: the **class** was mine to judge,
the **width** was not — and only the class is scored.

---

## 3. THE SCORE, AND THE PLANT

| | value |
|---|---|
| TP / FP / FN / TN | **16 / 0 / 0 / 22** |
| **precision** | **100.0%** (16/16) · Wilson95 **[80.6%, 100%]** |
| **recall** | **100.0%** (16/16) · Wilson95 [80.6%, 100%] |
| deduplicated by `clip_id` (n=31) | 13/13 · precision Wilson95 **[77.2%, 100%]** |

The corpus repeats `clip_id`s across work directories, so the deduplicated row is the honest
one; both are given. **The point estimate clears the ~90% bar; the Wilson lower bound does
not** (80.6%, 77.2% deduplicated). With 16 positives that is what 16/16 is worth.

### The plant — the MEMEBOT-115 killer, built rather than waited for

A picture **inset 140 px** each side under a **dark full-width caption bar** whose ink reaches
**x = 60**:

| case | honest answer | got |
|---|---|---|
| dark bar over 140 px inset, ink from x=60 | **60** | **(60, 60)** ✅ |
| same bar over a **full-width** picture | **None** | **None** ✅ |

**140 would have sliced the headline. It answers 60.** Both directions asserted, per
`docs/TESTING.md` rule 2.

---

## 4. I WIRED IT, RENDERED 20, READ THE FRAMES — AND TOOK IT OUT

**Which ranking (item 5): NONE — a PINNED LIST.** The 20 clip_ids are MEMEBOT-115's own
recorded render order from `scratch/mb115_render.json`. 115 used the live `rank_candidates`
against a growing library and so could not compare clip-for-clip; pinning to its list makes
these frames directly comparable — same sources, same order, one variable changed.

**17 of 20 rendered.** The 3 failures are an **ffmpeg AAC decode fault**
(`Error submitting packet to decoder: Not yet implemented in FFmpeg, patches welcome`),
nothing to do with framing — and two of the three had `side_pad=None`, no horizontal trim at
all. 11 of 20 were trimmed; 10 of those rendered.

### Six of six trimmed renders I read had the headline sliced

| clip | trim | SOURCE headline | FINAL |
|---|---|---|---|
| `3941137148442927658` | 54/58 | "The moment Mikhail Kalashnikov / designs his first legendary assault rifle" | **cut at both edges** — *the very clip 115 named* |
| `3941096583528765637` | 60/64 | "A contract killer uses / a knife to silence his victim" | **cut at both edges** |
| `3940297261774935571` | 48/54 | "Xander Cage exposes the fake / waitress during a diner robbery" | **cut at both edges** |
| `3947344016691407324` | 50/50 | "Come on, man." | **"Come on."** — the `, man.` is gone |
| `3931285888038729468` | 42/42 | "**W**ait until you hear what…" | **"ait until you hear what"** |
| `3947016010508623331` | 74/80 | "Recruiting the most dangerou**s** / …suicide missio**n**" | **both lines cut at the right** |

### THE DETECTOR WAS NOT WRONG. That is the finding.

Measured against the **first inked column** on 11 real sources:

| clip | trim found | first ink column | margin left |
|---|---:|---:|---:|
| 3941096583528765637 | 60 | 60 | **0 px** |
| 3941137148442927658 | 54 | 54 | **0 px** |
| 3940297261774935571 | 48 | 48 | **0 px** |
| 3931285888038729468 | 42 | 42 | **0 px** |
| …8 of 11 at 0 px, the other three at 1–2 px | | | |

**The trim lands exactly on the ink, because the padding boundary IS the headline's
boundary.** On these sources the caption is **wider than the picture beneath it**, so the
only pure-canvas columns are the ones beside the text. Trimming them is *correct* and still
ruinous: it puts the first letter on the frame edge with nothing to spare.

Then the template applies its own jitter to what remains — from `config.yaml`, not guessed:

```
zoom 1.05 .. 1.20      -> up to (1 - 1/1.20)/2 = 8.33% eaten per side
position_shift_x -8..+8 px      rotation -0.8..+0.8 deg
```

With 0 px of margin, the zoom alone takes the first and last letters. **The pillarbox was
load-bearing** — it was the slack the renderer's own jitter had always been eating.

### With a correctly-sized margin, nothing is trimmable at all

`PAD_SIDE_SAFETY_PCT = 10.0` of the **retained** width (the zoom applies to the crop, so that
is the right base) — the horizontal twin of `CROP_EDGE_SAFETY_PX`, which MEMEBOT-082 sized
the same way vertically. The result:

| population | trimmed before the margin | after |
|---|---:|---:|
| the 40 labelled sources | 16 | **0** |
| the 20 rendered | 11 | **0** |

**Not one source in forty has enough horizontal canvas to trim safely.** So the axis stays
pinned, and `x, w = 0, w0` is restored at the call site.

> **This is MEMEBOT-115's own vertical finding arriving on the other axis.** 115 read six
> sources and established that the space **above** the picture is the source's own caption.
> The space **beside** it is governed by the same caption — it is wider than the picture, so
> the side canvas is the caption's bleed. **47.4% of sources being pillarboxed never meant
> 47.4% were trimmable.** That is a different claim from 115's, and it is the one that closes
> the question: the next attempt does not need a better detector. This one is accurate to the
> pixel.

---

## 5. WHAT SHIPPED

**Kept**, because it is strictly better and now proven:
- `_side_padding_raw` — the full-resolution per-pixel measurement (16/16, 0 px error, beats
  the dark-bar plant).
- `_side_padding_columns` — the **judgement**: raw boundary minus the renderer's jitter
  allowance. **Split from the measurement on purpose**: collapsing them made the first
  attempt untestable, because "where is the boundary" and "is it safe to cut there" are
  different questions and only one of them is about the source.
- `PAD_INK_TOL`, `PAD_SIDE_SAFETY_PCT`, and four new checks in `test_content_crop.py`
  including the planted dark bar and its full-bleed control.

**Not shipped:** the trim. The call site is `x, w = 0, w0` with the measurement recorded
above it.

`PAD_COL_STD_MAX` / `PAD_COL_CORNER_TOL` are unread; renamed `_SUPERSEDED_*` with a note
rather than deleted, so nobody reinvents a mean-based test.

**The vertical axis is untouched**, deliberately.

---

## VERIFICATION

| Check | Result |
|---|---|
| memebot suite (`unittest discover`) | **254 tests, OK** |
| `test_content_crop.py` (11, incl. 4 new) | **OK** |
| shipped `edit.py` vs scored prototype, 40 sources | **40 agree / 0 differ** |
| renders read frame by frame | **10 trimmed rendered, 6 read, 6/6 sliced** |
| `edit.py` duplicated markers at HEAD | **none** |
| Paid calls | **none — $0.00** |

## WHAT I GOT WRONG

- **I wired it before rendering.** The score and the plant were both good and both
  insufficient; §4 is the frames overruling them. The suite was green the whole time — which
  is the project's own standing lesson arriving again.
- **My first render harness pointed at `memebot/edit.py`** (it is `memebot/scraper/edit.py`)
  and at the parent's `config.json` instead of the per-run `config.yaml`, and rendered zero.
- **My first headline zoom used a hardcoded account→clip mapping** and showed two unrelated
  clips; I rebuilt it from the render record before drawing any conclusion.
- **I killed my own render run** with a 10-minute blocking wait in the calling shell, at 7 of
  20; the harness is now resumable rather than wiping the tree.
- **I renamed a constant that belongs to another round's contract.** Marking
  `PAD_COL_STD_MAX` dead, I renamed it `_SUPERSEDED_PAD_COL_STD_MAX` — and
  `docs/claims/MEMEBOT-115.claims` **enrols that symbol under permanent enforcement**.
  `verify_claims` caught it on the next run (115 went 3/3 → 2/3). The names are restored and
  the supersession is a comment. **Superseding a constant's meaning is this round's business;
  renaming its symbol is not.** Worth recording that this is the manifest system doing
  precisely the job it was built for, on me.

## STILL OPEN

- **The disk hit 0.00 GB during the first render run** and the failures were reported as
  "Not enough disk". Nothing of another round's was deleted; I reclaimed only my own
  duplicate staged sources.
- **3 of 20 sources cannot be rendered at all** — an ffmpeg AAC decode fault, unexamined.
- **2 of 40 sources decode no frames**; excluded from scoring, cause unknown.
- **The Wilson lower bound is 80.6%** (77.2% deduplicated) — moot for shipping now, but the
  number to improve if this is ever revisited.
