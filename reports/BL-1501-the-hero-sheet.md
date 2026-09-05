# BL-1501 — The sheet was built correctly and then three quarters of it was thrown away

> **Reading this cold?** This project finds social-media pages worth contacting. A vision
> model — the "judge" — is shown a picture of a page and decides whether the operator would
> want it. The operator's standing request has been: *take the whole video, cut it into four
> to six frames, make the text readable, biggest possible picture, send that.*
>
> Creator handles are redacted throughout. Paths are repository-relative. No port numbers, no
> addresses, no keys appear. **No corpus image is published** — see §6.

---

## The answer, in one paragraph

**The hero layout works. The delivery destroys it. And none of it is in production.**

Measured on 420 model calls for **$0.0374**: a hero sheet sent **whole** transcribes its
burned-in text at **100.0% median character accuracy**, clearing his 99% bar on 9 of 10 pages.
The same sheet as **actually delivered** — a 195×346 crop — scores **43.6%**, with **0 of 10
pages clearing the bar** and a worst page of **0.0%**. The 56.4-point gap sits far outside the
5.7–13.3 point repeat noise. The model is not failing to read: it is reading the left third of
every line, verbatim — *"I have officially rea bothered by light opened, loud"*. **Meanwhile
the differences among all six full-sheet arms are zero at the median**, so hero+3, hero+4,
hero+5 and the plain uniform grid are indistinguishable from one another. **And it is moot in
production: `video_strip` has zero production importers, and no video is decoded anywhere on
the judge path at all.**

---

## 1. Round ID, date, and what it was asked to do

**BL-1501**, 2026-09-05. Build the hero contact sheet — one large frame for the text, three to
five smaller ones for motion — and measure whether the model can actually read it against his
**99% bar**.

**Conditions at start**: no dashboard or sheet-server listener (read from the listening-port
table, never a command-line filter), 5 Python processes, 374 GiB free. Two other rounds live;
BL-1500 was producing corpus material and owns `scratch/bl1500_*` and `output/bl1500_*`.

**This round adds no judging rule, loosens none, and moves no threshold.**

**Spend: $0.0374 by the run's own counter**, on 420 calls. The ledger was deliberately not
written. A ledger delta cannot attribute — it is shared, and one model bills per token, counts
as a free send and never books.

---

## 2. What actually shipped

Nothing was wired into the judge. This round **measured**, and produced pictures he can open.

| artefact | what it is |
|---|---|
| **`output/bl1501_what_the_model_sees/`** | **12 images + a plain-words README. Every panel at TRUE SCALE.** |
| `scratch/bl1501_show_him.py` | builds the true-scale comparison |
| `scratch/bl1501_payload_compare.py` | decodes both payloads **off the wire** and puts them side by side |
| `scratch/bl1501_agentA_*` | the geometry audit |
| `scratch/bl1501_agentB_*` | the wiring audit |
| `scratch/bl1501_agentC_*` | the threshold sweep |
| `scratch/bl1501_agentD_*` | the readability measurement |

### ⚠️ THE PICTURES ARE ON HIS MACHINE, HERE

```
output/bl1501_what_the_model_sees/
```

Open `payload_01.jpg`. **Left panel is what the model actually got. Right panel is the same
sheet with one argument changed.** Nothing is resized; both panels are exactly as big as the
pictures really are. `READ_ME_FIRST.md` explains it in plain words.

---

## 3. What was measured

### 3.1 The hero is 416×740 at every count — and that is arithmetic, not accuracy

Driven through the shipped `video_strip.hero_geometry`:

| n_small | hero | small | sheet |
|---:|---|---|---|
| 1 | 416×740 | 416×740 | 862×760 |
| 2 | 416×740 | 208×370 | 654×760 |
| 3 | 416×740 | 139×247 | 585×760 |
| 4 | 416×740 | 104×185 | 550×760 |
| 6 | 416×740 | 69×123 | 516×760 |
| 8 | 416×740 | 52×92 | 498×760 |

`hero_h = cap − 2·gutter = 760 − 20 = 740`; `hero_w = 740 × 9/16 = 416`. **The frame count
never enters the sum**, so the constancy is a definition, not a result. **Reported as a pixel
argument, which is what it is.**

**The docstring is wrong**: `hero_geometry` claims "hero 428×760"; the code returns 416×740.
Named, left.

**The grid series re-derived exactly**: n = 3, 6, 8, 12, 16 → **241 → 207 → 138 → 104 → 69**.
"A grid holds 253 px from 3 to 8 frames" is **refuted** — it drops to 207 the instant a second
row appears at n=4, because `cols = min(n,3)` freezes the width while every row adds height.

**Row versus grid at 16 frames**: row 4490×500 → sent **760×84**, tile **46×81**; grid
850×2960 → sent **218×760**, tile **69×123**. **1.50× the width, 2.28× the area** — the
inherited 1.5×/2.3× confirmed. And the correction holds: **the row tile is 46×81, not square,
and the "84" is the sheet height, not the tile's.**

### 3.2 The crop — proved four ways, and it cuts through the text

`output/bl1461_corpus/`, 276 pages, 2,302 sheets per family.

| family | median | distinct sizes |
|---|---|---|
| hero / sent_hero_grid | 585×760 | **1** |
| **sent_hero_tile** | **195×346** | **1** |
| sent_uniform_grid | 651×760 | 142 |
| sent_uniform_tile | 283×503 | 103 |

**These files are the wire bytes, proved not assumed.** The sha256 of
`base64.b64decode(tile_b64(hero, 760, tiles=4))` from the **live shipped** encoder equals the
sha256 of the file on disk on **60 of 60** sampled pages; a negative control with the wrong
`tiles` matched **0 of 20**.

1. **Arithmetic** — 195×346 = 67,470 px against 585×760 = 444,600. **15.2%: 84.8% of the built
   sheet is gone before the model sees it.**
2. **Geometry** — the hero tile is *smaller* than the uniform tile (283×503). The arm built to
   beat the grid delivers a smaller picture than the grid.
3. **Coordinates** — the hero panel occupies x 10–426, y 10–750. The crop keeps **185 of 416
   hero columns (44.5%)** and **336 of 740 rows (45.4%)** = **20.19% of the hero**. Its right
   edge stops **231 px inside** the hero, its bottom edge **404 px inside**, and it contains
   **zero motion pixels**. The hero is intact in **0 of 2,302** sheets.
4. **Visually.** On one page the built sheet and the uniform tile both read *"Boomers having
   $35,000 homes while housing is now unaffordable"* — complete. **The hero tile actually sent
   reads "Boomers having $" and "housing is now una". Cut mid-word, twice.**

**The mechanism, driven at the encoder.** `tile_b64` takes the top-left cell as
`width // cols` (`free_judge.py:813`); 585 / 3 = 195.

| encoder | delivered | share |
|---|---|---|
| `grid_b64` | 585×760 | 100.0% |
| `tile_b64`, default cols=3 | **195×346** | **15.2%** |
| `tile_b64(tiles=1)` | 585×760 | 100.0% |

**The fix is one argument the function already supports and documents in its own docstring.**
The production selector (`meme_finder.py:6779-6787`) computes `_cols = min(_tiles,3) if
_single else 3`, where `_single` means 1–2 tiles. **A hero sheet is one hero plus n smalls, so
it is not "1–2 tiles" and falls to the default 3.** The code has no concept of a composed
layout, only of tile counts.

**FIX CATEGORY.** Passing `tiles=1` at one call site is **LOCAL** — and only 1 of 7 past fixes
here was general while 3 of the 6 local ones were still failing. The **GENERAL** form is a
boundary assertion: after encoding, assert the decoded width is not a whole-number fraction of
the source width, so no future layout can be silently quartered. **A comment cannot fail; an
assertion can.**

### 3.3 Aspect — stretched, and the share is 24.1%, not 12.7%

`video_strip.py:382` is an unconditional `hero.resize((hw,hh))` — no letterbox, no crop. A
square source exits **1.779× vertically stretched** (the inherited 1.78× confirmed).

**The share that is not 9:16 is 24.1%**, agreed by three independent instruments: source
pixels 555/2,303 = 24.10%, hero frame as fed 554/2,302 = 24.07%, extracted motion frames
3,314/13,814 = 23.99%. Stretch factor median 1.0006, **p90 1.7788, p95 2.3718, max 3.9530**;
22.20% are stretched more than 1.10×. **The inherited 12.7% is not reproducible on any of
eight denominators tried** — the true figure is roughly double, so this affects about **one
page in four**, not one in eight.

### 3.4 The tile-width guard is on the wrong side of the cap — confirmed, claim overstated

`MIN_TILE_W = 220` is applied at `video_strip.py:264-265` **before** the sheet is written;
`free_judge.py:519-522` rescales by `760 / long-edge` **afterwards, in a different module**
that never names `MIN_TILE_W` and imports nothing from `video_strip`. Nothing re-checks after
the cap.

Measured on **2,303 delivered sheets**: median delivered cell **206.9 px**, p95 248.2, min
165.5. **1,788 below the 220 floor = 77.64%.** Of the 1,732 sheets from a 9:16 source, 100%
fail; of the 571 wider-source sheets, 9.81% do.

**But "every delivered tile at every frame count including four" is too strong** — n=3
delivers **241**, above the floor. The mechanism is real and universal at the shipped default
(`scaled:6`, 9:16); the absolute is not.

### 3.5 Can the model read it? His 99% bar, measured

n = 10 pages × 3 repeats = 30 cells per arm. A blank scores 0.0. Every image was opened **out
of the JSON request body** by a spy raising a `BaseException` subclass — uncatchable by the
`except Exception` in every fallback path, so no silent retry on a second model.

| arm | boundary px | **median accuracy** | blank % | self-disagreement | pages ≥ 99% |
|---|---|---:|---:|---:|---:|
| built hero+3 | 585×760 | **100.0%** | 6.7% | 7.7% | 8/10 |
| built hero+4 | 550×760 | **100.0%** | 0.0% | 13.3% | 9/10 |
| built hero+5 | 530×760 | **100.0%** | 0.0% | 6.7% | **10/10** |
| delivered hero grid | 585×760 | **100.0%** | 6.7% | 3.8% | 9/10 |
| delivered uniform grid | 651×760 | **100.0%** | 3.3% | 7.1% | **10/10** |
| delivered uniform tile | 283×503 | **100.0%** | 0.0% | 6.7% | 9/10 |
| **delivered hero tile** | **195×346** | **43.6%** | **26.7%** | 10.5% | **0/10** |

**His 99% bar is cleared on every sheet sent whole and missed only on the arm that is
cropped.** The 56.4-point gap is far outside the 5.7–13.3 point repeat noise. Three pages
score a flat 0.0%, and the **positive control passed** — the same page, key and model on the
hero grid scores 77.1 / 100 / 100, so the zero belongs to the arm and not to the page.

**The differences among the six full-sheet arms are zero at the median — inside their own
noise. No arm is claimed better than another.** More frames did not help and did not hurt.

**Blanks are budget overruns, not refusals.** Every text blank had `completion_tokens == 2600`,
exactly the cap.

**Tokens.** Going from 3 frames to 5 costs **540 → 516 prompt tokens — it goes *down*, by
4.4%.** Tokens scale with **area**, not frame count: 174 (hero tile) to 604 (uniform grid),
3.5×. **The crop "saves" 68% of the prompt tokens by deleting the text.** So the geometry is
free to optimise: the cost of more frames is legibility, not money.

### 3.6 The 25-point trap reproduced — at 45 points

Asked about cutting rhythm:

| arm | modal answer | entropy | self-agreement |
|---|---|---|---|
| uniform grid (6 frames) | medium 37.5% | **1.91 bits** | **55.0%** |
| uniform tile (1 pane) | single **100%** | **0.00 bits** | **100.0%** |
| hero tile (fragment) | single **100%** | **0.00 bits** | **100.0%** |

**A 45-point apparent gain in reliability, bought by deleting five sixths of the evidence.**
One pane has no rhythm, so the model settles on a constant and agrees with itself perfectly
about nothing. **If a metric in this round improved, this is the first thing to check** — and
it is why no craft figure here is quoted as a result.

### 3.7 The threshold — named as a confound, with the sweep

**I did not re-tune it.** I measured the confound and produced the curve so it can be put to
him.

**The real bars**: `z-ai/glm-5.3-flash` **90** and `nex-agi/nex-n2-mini` **90**
(`free_judge.py:242-243`); every fallback-chain model has **no reject authority**
(`:1656`). The only cut site is `free_judge.py:1656-1657`.

**80 governs nothing — confirmed, and more strongly than claimed**: `should_reject` accepts
`reject_at=REJECT_AT` at `:1463` and **never reads it in the body**. It is a dead parameter.
*But 80 is not inert*: it is a live import-time assert floor (`:430-435`), a preflight check
(`preflight.py:145-152`), and it decides GOOD-versus-MAYBE inside `classify` (`:1407`). **It
decides no rejection anywhere.** **95 is a label** (`KEEP_AT`, `meme_finder.py:4369`).

**The sweep. Denominator: 195 marked pages a live cutter answered on — 76 wanted, 119 not.**

| threshold | traffic removed | catches of his lows | **kills of wanted** | **Wilson 95%** |
|---:|---:|---|---:|---|
| 60 | 59.0% | 84.0% | 15/76 = 19.7% | [12.3, 30.0] |
| 80 | 51.3% | 76.5% | 9/76 = 11.8% | [6.4, 21.0] |
| **90 (ships)** | **36.9%** | **58.0%** | **3/76 = 3.9%** | **[1.4, 11.0]** |
| 95 | 24.1% | 37.8% | 2/76 = 2.6% | [0.7, 9.1] |
| 100 | 0.0% | 0 | 0/76 | [0.0, 4.8] |

With the label-reversed sheets excluded (n=175, 68 wanted): at 90, **1 of 68 = 1.5%
[0.3, 7.9]** — **and that page he scored 10**. At 95, 0 of 68 [0.0, 5.3].

**No threshold clears a 95% floor on this evidence.** 0/68 needs n ≥ 73 for the bound to fall
under 5% — **five more graded wanted pages, and only at 95.** **I am not picking a number.**

⚠️ **`free_judge.py:243`'s own comment, "0 of 60 wanted killed at 90", is refuted at scale**:
that model kills 5 of 177 wanted pages and 3 of 110 of his 8–10s.

**THE CONFOUND, MEASURED — and its direction is opposite to the assumption.** The bar was
never calibrated on one picture. Inside the **single 214-page pool that set `MAY_REJECT`**,
the encoder delivered **431×760 to 25.2% of pages and 760×760 to 24.8%** — a **1.76× area
difference inside one measurement** — plus forty further sizes. Across grid directories the
delivered area spans **7.6×**. So "calibrated at 155×275, now ships at 356×760" understates
it: **every kill rate above pools at least four geometries.** It cannot be stratified away,
because `should_reject`'s detail dict (`:1476`) records no image dimensions — adding that
field is a write, and this round left it.

### 3.8 His marks are the ceiling — and two of the three quoted figures are not his marks

**75.8% verified exactly** (135/178 on the widened corpus; the published 41-file glob gives
115/149 = 77.2% [69.8, 83.2]).

**92.9% and 59.6% are refuted as self-agreement figures.** 92.9% is a keep-rate lower bound
from a different round; 59.6% is another round's all-rows agreement at iteration 5. Two
unrelated numbers pulled into a sentence about his marks.

**Measured instead**: on obvious pages (scored 1 or 10) **51/56 = 91.1% [80.7, 96.1]**; near
his decision line (5–7) **10/20 = 50.0% [29.9, 70.1]**. **Every near-line interval contains
50%.** On exactly the pages the filter sorts, his marks are indistinguishable from a coin
flip. **Nothing scored against them can exceed that, which is why the 95% bar belongs on kills
of wanted pages and not on accuracy.**

**Excluded**: a 100-row mark file with no reason field where he pressed GOOD on 97 of 100 —
those are the judge's verdicts through an agree button. ⚠️ **The claim "100 of 100" could not
be reproduced; the maximum anywhere in the corpus is 97/100.** Also excluded: two label-reversed
edits sheets, one of which is 30 wants of 31 rows — all-positive by construction.

**And a counting bug worth keeping**: there are **15 mark files, not 14**; three are empty; and
the fifteenth (150 rows, 90 wanted) is invisible to `scratch/bl1452_ceiling.py:32`, which globs
one directory too shallow. **Those 150 marks have been outside every published ceiling figure.**

### 3.9 None of this is in production, and the reason is supply

**`video_strip` has zero production importers**, established by three instruments each with a
passing positive control — an AST walk aware of bare sibling imports (controls: `meme_finder`
313, `free_judge` 206, and 54 of free_judge's are inside a `def`, so deferred imports are
visible), a string/dynamic-load search, and a runtime closure under an audit hook (controls
8/8). All 11 importers are tests and scratch. **A first runtime instrument produced a false
zero and its controls failed; it was discarded and recorded.**

**This is the seventh round to say so, not the fourth.**

**The claim that the module "cannot be imported at all" is false as stated.** It imports both
ways; the `atomic_io` import at `:205` is deferred inside `extract()`. It raises under exactly
one path — repository root on `sys.path` *without* `clippershq/` — driven in five isolated
subprocesses. **Its own 35 tests all pass, including a real end-to-end ffmpeg build.**

**`HERO_T_DEFAULT = 1.4` has no extractor.** Its only readers are two range-checks in a test.
Zero production readers and **zero readers inside the module itself**; `strip_for_video` uses
`frame_times()` midpoints instead, so the first frame of an 89-second clip lands at **7.4 s**,
not 1.4 s. Control: the same sweep finds `JUDGE_MAX_PX` 5 times and `GUTTER` 9 times in that
file, so the zero is real. **The 1-to-2-second text-frame rule is declared and not
implemented.**

**⚠️ AND THE FINDING NO PRIOR ROUND RECORDED: the blocker is supply, not the tiler.** **No
video is decoded anywhere on the judge path.** The free, un-billed mp4 download exists
(`tiktok_finder.py:1262`, signed URL, called at `:2815` *before* the judge) and is inert:
`speech_fracs` is hard-coded `None` at `:2803`, and `ocr_can_change_a_verdict(None)` returns
`False` — executed and confirmed. **Six rounds audited the tiler. None named this.** A better
sheet cannot help while there are no frames to put in it.

---

## 4. What was refused, and why

**I did not wire the module in.** Wiring changes verdicts three ways — a different image, a
note inserted into the prompt at `free_judge.py:1044`, and a crop flag flipping at `:4087` —
and this round's terms forbid moving a verdict without re-tuning the threshold, which the
evidence does not support doing yet.

**I did not delete it either.** It uniquely holds the hero layout, the k/N badges, `probe()`'s
no-video-stream check, and **the only ffmpeg tree-kill in the repository** — the live
alternative spawns one ffmpeg per frame and reaps no grandchild.

**I did not re-tune the threshold.** The curve is above; the confound is measured; **no value
clears a 95% floor on 68 wanted pages.** Picking a number for him on that evidence would be
guessing with his money.

**I did not run the Part 4 paired verdict scoring** — 50–100 pages per brain, same pages and
brief with only the image changing, scored for kills and the uncertain band. **It was not
done.** Doing it means sending real judgements, which changes verdicts, on a threshold this
round has just shown is confounded across at least four geometries. **What I measured instead
was readability, which is the input to that test and is reported on its own terms.** The
uncertain-band split before and after — the number that actually pays — **is not in this
report.**

**No image is published.** Corpus frames carry burned-in creator handles, a handle detector
here once failed its own first control, and a JPEG's compressed bytes can trip a handle
pattern by chance. **A previous round withheld images rather than publish ones it could not
prove clean, and this round does the same.** The illustrations produced for the geometry audit
use **synthetic** frame content through the real builder and real encoder.

---

## 5. What I got wrong, and what the brief got wrong

**Mine.** I nearly reported the corpus as "already-cut frames" before checking what the
`sent_*` prefix meant — it is the wire bytes, and that had to be proved by hashing against the
live encoder rather than inferred from a filename.

**Three inherited figures do not survive measurement**, and all three were checked before use:

- **"12.7% of the corpus is not 9:16" → 24.1%.** Three instruments agree; the inherited figure
  reproduces on none of eight denominators. **The problem is twice as common as stated.**
- **"Every delivered equal-grid tile is below the 220 floor at every frame count including
  four."** 77.64% are, and **n=3 delivers 241, which passes**. The mechanism is right; the
  absolute is wrong.
- **"The module cannot be imported the obvious way at all."** It imports both ways; the failure
  needs one specific `sys.path`.

**And two quoted self-agreement figures are not self-agreement at all** — 92.9% is a keep-rate
lower bound and 59.6% is a different round's all-rows agreement. The real near-line figure is
**50.0% [29.9, 70.1]**.

**"100 of 100" could not be reproduced** — the maximum agreement in the corpus is 97 of 100.

---

## 6. Money and safety

**$0.0374 on 420 calls**, by the run's own counter, against a $1.00 cap. The ledger was
deliberately not written; `_book_paid_call` was never called. Three of the four strands made
**zero** calls.

**Protected files: 7 of 8 byte-identical** at start and again at publication —
`config.json`, `master_leads.csv` and **all five seen stores**. **No seen-store row was
deleted or rewritten.**

**The eighth moved, and it is reported as movement rather than claimed unchanged.**
`spend.json` went `5042a676602a2b0f` → `2eba0c166506fb72` during this round. It is **not
mine**: my only billed strand used a text model and never called `_book_paid_call`, and the
ledger's newest rows are Instagram auxiliary calls timestamped inside the window in which a
*different* live round was fetching Instagram video. **Five rounds were in flight by the end.**
This is exactly why the $0.0374 above is counted by the run's own driver and not by a ledger
delta: on a file five rounds are writing, a delta cannot attribute anything to anyone.

*(One further working-tree modification, `clippershq/api_client.py`, is also not mine — it has
been modified since 31 August, days before this round opened.)*

**No judging rule was added or loosened. No threshold was moved. No verdict was changed.**

**This report contains no creator handle, email, key, absolute path with a username, or port
number, and no image at all.** It was scanned by reading its bytes, with every detector proved
on a planted control first and zero C0 control bytes asserted before writing.

---

## 7. What to do next — ranked

**1. Pass `tiles=1` when the sheet is a composed layout — and add the boundary assertion.**
The one-argument change is local and will be forgotten; the assertion that a decoded payload
is not a whole-number fraction of its source is general and cannot be. **Without it, wiring the
hero sheet in delivers 15.2% of the picture and looks like a layout failure.**

**2. Decide the module's fate on the real reason.** It is not dead code — it holds the only
hero layout and the only ffmpeg tree-kill in the tree. **It is unwired because no video is
decoded on the judge path at all.** Wiring the tiler without fixing supply changes nothing.
That is the decision, and it is the seventh time the file has been raised.

**3. Fix the aspect stretch.** One unconditional `resize` at `video_strip.py:382` distorts
**one page in four**, up to 3.95× at the tail.

**4. Implement the 1–2 second text frame, or delete the constant.** It is declared and unread;
the shipped path takes a midpoint, putting the first frame of an 89-second clip at 7.4 s.

**5. Record the delivered image dimensions in `should_reject`'s detail dict.** Until that
exists, every kill rate pools at least four geometries and the threshold cannot be honestly
re-tuned.

**6. Grade five more wanted pages.** At 95, kills are 0 of 68; **five more takes the Wilson
upper bound under 5%** and makes a threshold decision defensible for the first time.

---

## 8. Paths to open

| path | what is in it |
|---|---|
| **`output/bl1501_what_the_model_sees/`** | **the pictures, true scale, with a plain-words README** |
| `clippershq/video_strip.py:331` | `hero_geometry` — and the 428×760 docstring the code contradicts |
| `clippershq/video_strip.py:382` | the unconditional resize that stretches one page in four |
| `clippershq/video_strip.py:324` | `HERO_T_DEFAULT = 1.4`, declared and never read |
| `clippershq/video_strip.py:264` | the 220 floor, applied before the cap |
| `clippershq/free_judge.py:813` | `tile_b64` — `width // cols`, and its own docstring naming the fix |
| `clippershq/free_judge.py:519` | the cap, applied afterwards in a different module |
| `clippershq/meme_finder.py:6779` | the selector that sends a hero sheet down the cols=3 path |
| `clippershq/free_judge.py:242` | the bars that actually cut: 90, per model |
| `clippershq/free_judge.py:1463` | `reject_at` — a dead parameter |
| `clippershq/tiktok_finder.py:2803` | `speech_fracs = None`, which makes the free download inert |
| `scratch/bl1452_ceiling.py:32` | the glob one directory too shallow, hiding 150 marks |

https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/BL-1501-the-hero-sheet.md
