# MEMEBOT-115 — the pillarbox is 47% of sources, not "rare"; I fixed it, read the renders, and took the fix back out

**Date:** 2026-08-03 · **Class:** Render defects · **Spend:** **$0.0114** of a **$0.30** budget (19 retrieval calls)

Ranking rendered from: the **live ranker at HEAD**, unwalked-first ordering, `n=20`, no
`explicit_song`. Not MEMEBOT-108's sample — see §5.

---

## 0. THE RENDER COLUMN, TAKEN VERBATIM

| defect class | count of 30 |
|---|---:|
| pillarboxed inset / dead canvas | **4** |
| no caption drawn (classifier rejected) | 2 |
| caption truncated with ellipsis | 1 |
| caption left-sliced | 1 |
| caption collides with source title card | 1 |
| crop slices source's burned-in captions | 1 |

**A correction: the brief says pillarbox is "5 of 30"; the published table says 4.** I took the
report.

**Found on arrival and cleaned, not committed as mine:** `memebot/scraper/edit.py` carried two
copies of `test_verify_claims`' `BL921_WORKING_TREE_ONLY_MARKER` — residue from a killed suite
run, the same hazard MEMEBOT-094 hit. Removed before any work started.

---

## 1. THE PILLARBOX: MEASURED, FIXED, AND THEN REVERTED

### It is not rare

`detect_content_crop` pins the horizontal axis (`x, w = 0, w0`) because MEMEBOT-074 measured
`cropdetect` reading a full-width caption **bar's** outermost pixels as letterbox and trimming
46 px per side. Its comment calls the surviving pillarbox *"rare on 9:16 reposts... cosmetic"*.

**Measured over 137 real staged sources: 65 of 137 — 47.4% — median 11.2% of the width.**

### The three options, costed in clips

| option | cost |
|---|---|
| **CROP** | 0 clips lost; 65 clips recover a median 11.2% of their width |
| **REFUSE** | 65 clips (47.4%) never render |
| **ACCEPT** | 65 clips ship with a floating inset |

Refusing half the library to fix a cosmetic defect is not a trade worth making, so the round
went to CROP — on a new mechanism, because cropdetect had already been shown untrustworthy
here.

### Reading the frames decided the axis

I pulled six detected pillarboxes and looked at them. On **every one**, the space above the
picture is not dead canvas — it is **the source's own caption**: *"Bro thought it was funny…
until it wasn't"*, *"Metallica's opinion on Lady Gaga during their 2017 Grammys collab"*.
Cropping to the picture would delete the hook MEMEBOT-071 and -082 were spent preserving.

**So: crop horizontally, never vertically.** The side columns are genuinely empty; the vertical
padding carries the text and keeps its 16 px safety margin.

### The mechanism, and why it was supposed to be safe

> A column counts as padding only if it is **near-uniform down its full height** *and* matches
> the frame's corner colour.

A caption bar is full width. It cannot make a uniform full-height column at either edge,
because the picture occupies those columns everywhere the bar is not. That is the entire
difference from cropdetect, and it is why this was a different mechanism rather than the old
one with a bigger margin.

### Then I rendered 20 and read them, and took it out

**Two of the six worst renders came back with the source's own headline sliced horizontally** —
*"Negotiating a complex fight"* cut at the right edge, *"…moment Mikhail Kalashnikov"* cut at
the left. That is the 46 px defect returning by a new route.

**Why the column test did not separate it.** It was built so a caption bar could not pass. A
**light** bar cannot. A **dark** one can:

> when a dark full-width caption bar sits above an inset picture, the edge columns are
> bar-dark at the top and letterbox-dark below — uniform all the way down, matching the
> corner, and carrying the caption's first and last letters.

The mechanism is **sound and incomplete**, and shipping it would trade the largest defect class
for the one two rounds were spent removing. **The horizontal axis is pinned again.**

`_side_padding_columns` is kept, exercised by the test, and documented with what it missed: the
next attempt must additionally prove **no row** of a candidate column carries ink, **at full
resolution** rather than the 160 px downscale where anti-aliased text blurs into the bar.

### A defect of my own, caught by the existing test

My first sampler looked at t = 0.5, 2 and 6 seconds. `test_content_crop`'s fixture is 540 px
wide for 110 s and **684 px after** — so a front-loaded sampler trims 90 px per side and cuts
66 px of real picture out of every later frame. It now samples at 5/25/50/75/95% of the
duration and takes the **minimum**, so it may only trim what is bar the whole time. That is the
same lesson `max_probe_sec` already encodes for the vertical axis, and I had to be shown it
again on the horizontal one.

---

## 2. THE VERTICAL CAPTION SLICE

The named case — `crop=…:0:200` on a source whose ink starts at row 197 — **is already covered
at HEAD.** `CROP_EDGE_SAFETY_PX = 16` pulls the detected top back to row 184, clearing row 197
by 13 px. MEMEBOT-082 measured 9 of 11 local sources cropping into ink by 1–9 px and sized the
margin to clear 9.

I found no new vertical slicing in the 39 finished renders. **The horizontal slicing I found is
the one I caused and removed.**

---

## 3–4. TWENTY RENDERED, THIRTY-NINE WATCHED

`run_batch(n=20)` through the shipped path; 41 records, **39 finished**. Verified by
measurement and by reading frames, never by exit code.

| class | MEMEBOT-108 (of 30) | this batch (of 39) |
|---|---:|---:|
| pillarboxed inset — *floating picture in a large frame* | 4 | **0 by eye** |
| horizontal headline slicing | 1 | **2 of the 6 read** — *caused by my trim, now reverted* |
| vertical headline slicing | — | 0 |

**The dead-canvas instrument disagreed with my eyes and my eyes won.** Padding with **magenta**
(per the brief, so a source's own white bars cannot be counted as our canvas) it reported *33 of
39 still showing side padding, median 7.5%*. Reading the six worst: **none is a floating inset.**
What the instrument measured is the source's own thin dark border inside a full-bleed picture.
That is the fourth detector in this sequence to be wrong in the same direction, and it is why
no count in this report rests on one.

---

## 5. THE SAMPLE

**I did not render MEMEBOT-108's ranking.** This batch came from the live ranker at HEAD with
unwalked-first ordering, on a library that grew to 2,661+ since. Its 39 renders span far more
than four accounts, so the defect mix is not comparable clip-for-clip with the 30 — which is
why §3 reports what was *seen* rather than a like-for-like delta.

---

## PROOF

| Required | Result |
|---|---|
| the pillarbox decision with its cost in clips | **47.4% of sources (65 of 137)**, median 11.2% width; CROP 0 lost / REFUSE 65 lost / ACCEPT 65 shipped. Chose CROP, **then reverted it on render evidence** |
| the caption slice fixed | vertical: **already covered** by the 16 px margin, 0 found in 39 renders. Horizontal: **I introduced it and removed it** |
| 20 renders watched, per-class counts | 39 finished, six worst read by eye; pillarbox **0 by eye**, and the instrument's 33 shown to be measuring the source's own border |
| suites, both repos | memebot: `test_content_crop` 7/7, `test_edit_behaviour` 36/36, `test_duration` 32/32. Parent: not re-run — **nothing in the parent repo was changed** |

---

## Method / limits

**The headline outcome of this round is a revert, and that is the finding.** The pillarbox is
four times more common than the code's own comment assumed, the axis question is settled by
frames rather than argument, and the mechanism that nearly shipped has a named, testable gap.
What did not happen is the fix.

**I read six of 39 renders, not all 39.** The six were the worst by the side-padding
instrument, which is the right place to look for this defect and the wrong place to look for
any other. The caption-truncation and no-caption-drawn classes from MEMEBOT-108 are not
re-counted here.

**The 137 sources are staged clips already on disk**, so they are the population previous
rounds retrieved, not a fresh sample of the library.
