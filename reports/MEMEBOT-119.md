# MEMEBOT-119 — 10 postable of 30, and the caption we compute has never been drawn

**Date:** 2026-08-03 · **Type:** Viewing audit · **Spend:** **$0.0384** of a $0.12 cap (hard cap $0.15)

Preconditions: `tools/claims_read.py` and `git status --porcelain`. Claim filed with repeated
`--write`. **This round changed no shipped file** — `scratch/` and a claims manifest only.

---

## The number, and the one that matters more

**10 postable of 30.** Three audits now read **13 → 10 → 10**. The rate has not moved, and this
round did not expect it to; the interesting result is *why*.

**The caption this pipeline computes is passed to the renderer and thrown away on every
render, and has been for as long as `white_frame` has been the template.** Not inferred —
edit.py says it, in the run I captured:

```
i  Template 'white_frame' ships with captions OFF, so --override-text is NOT being drawn.
   The source clip's own burned-in caption is the hook (MEMEBOT-076: better on 9 of 10).
   Pass --force-caption to draw it anyway.
```

That is a **deliberate policy** (MEMEBOT-076) and it is defensible. What is not defensible is
that **the policy has no fallback and nothing refuses a clip that cannot satisfy it.** Five of
the thirty have no burned-in text of their own, so they ship with **no hook at all** — a
finished, verified, ledger-joined video that says nothing. `clean_caption()` still trims the
Instagram caption to 120 characters and hands it over on all thirty; it is dead work.

**Every headline I read in these frames is the source page's pixels, not ours.** That single
fact re-assigns most of the defects this lineage has been calling "render".

---

## 1. The run

`python clippershq/run.py --funnel clip_render --target 30 --cap 0.12` — the shipping entry
point, no `explicit_song`, real library, real ranker, interleaving live. **30 of 30 finished in
1,123 s for $0.0384.** Parent `045d459`, memebot `c06f336`.

**Interleaving, measured on today's library rather than quoted:**

| top 30 candidates | distinct accounts | most from one account |
|---|--:|--:|
| `interleave=False` | 11 | **7** (`cawncept`) |
| `interleave=True` (live) | **30** | **1** |

All thirty finished videos come from thirty different accounts. MEMEBOT-108's sharpest caveat —
*18 of 30 from four accounts* — is gone, and it is gone because of a code change, not luck.

**The selection gate at library scale:** 2,728 clips → **2,274 kept, 454 refused**
(`non_english_caption` 298, `third_party_watermark` 117, `static_non_clip` 62). The gate is
wired into `clip_pipeline.gate()` now; MEMEBOT-108 had to apply it in a harness.

**Every one of the thirty passed the gate.** `postable=True`, `reasons=[]`, 30 of 30.

---

## 2. Verification — four ways, and two of MEMEBOT-108's gaps are closed

| check | result | vs MEMEBOT-108 |
|---|--:|---|
| video stream (ffprobe) | **30 / 30** | — |
| audio stream (ffprobe) | **30 / 30** | — |
| 8.0s floor | **30 / 30** | — |
| 20.0s ceiling | **30 / 30** | — |
| **ceiling provenance tag** | **30 / 30** | **0 / 30 → fixed** |
| configured track, 40–250 Hz signed correlation vs the APPLIED window | 29 / 30 | — |
| join key resolves + `joinable` | **30 / 30** | 27 / 30 |
| **all of the above on one row** | **29 / 30** | — |

Correlation against the **applied** window, lag bounded to **one hook period**, every other
store track as the null on the identical code path:

```
r  configured   min 0.3147   median 0.9045   max 0.9652
r  best OTHER   min 0.1786   median 0.2943   max 0.4146
unbounded minus bounded:  max +0.0000   (the bound removed nothing on this sample)
```

**The one failure is honest, not a missing song.** `victoriashannon23`, r = 0.3147 against a
null of 0.2484 — margin 0.066, under the 0.10 bar. Its class is `dialogue-over-music` and its
treatment is `keep-original`, so the bed sits far under speech that was never attenuated. This
is the case the 40–250 Hz band exists for and the case where it still runs out of room. It is
reported as *undecided*, not as *absent*.

**24 of 30 sit exactly at 20.0s**, so the ceiling is not a rare trim — it is the modal outcome,
and every row now carries the tag saying which ceiling was applied and why.

### The instrument that lied first was mine

My verify harness reported **join 0/30** against MEMEBOT-108's 27/30 on the same code path.
`check_joinable()` returns a **tuple** `(ok, reason)`; I wrote `joinable is True` against it,
which is never true. **The pipeline was fine and the audit was broken.** It was caught only
because 0/30 was too clean to believe. The fix is in `scratch/mb119_verify.py` with the reason
in a comment.

---

## 3. The bar, stated before I looked

> Would a 100k-follower repost page post this **unedited**? It fails on any of: a machine-output
> or truncated/sliced caption, a competitor's handle or logo, non-English on-screen content, a
> static non-clip, half-dead canvas (the picture floating in padding on all four sides rather
> than spanning the frame), unreadable footage, or reportable content.

Six frames per video, **full frame, never cropped**, one sheet at a time —
`scratch/mb119_frames/`. Per-clip verdicts and reasons in `scratch/mb119_verdict.json`.

**PASS: #1 wisecon, #2 dirtyclips67, #10 memesworlds8, #12 solidshampooz, #14 scenespectrumhq,
#17 movies.avengers, #23 brainmate_ai, #26 valentinaturner7050, #29 lol_buzzmemes,
#30 realmacjones.**

Five were borderline (#1 dark, #2 carries a Cartoon Network *broadcaster* bug which I do not
count as a competitor's mark, #12 dark and magenta-cast, #17 low-resolution, #23 a generic
hook). A stricter reader lands at 6; a looser one at 12. The frames are on disk so the
judgement can be overturned.

---

## 4. The split: **6 RENDER / 14 SELECTION** — and it is not MEMEBOT-108's 10/10

MEMEBOT-108 split exactly down the middle. This round moved several defects across the line,
and it moved them **by extracting frames from the staged SOURCE file and comparing**, which is
the check that decides the question.

### RENDER — 6

| # | account | defect |
|--:|---|---|
| 6 | hollywood_jan07 | source has no burned-in text; captions are OFF, so **no hook at all** |
| 13 | the_avengers_secretwars | source sticker on the first second only; **no persistent hook** |
| 22 | thefamousinventory | **no hook**, and a landscape source at `scale_width: 864` leaves most of the 1920-tall canvas empty |
| 24 | uncledaddybr | **no hook** (plus a pixel logo and a Portuguese caption the gate missed) |
| 28 | victoriashannon23 | **no hook** + a near-black source (also the one song failure) |
| 7 | jakeswims69 | **our crop slices the source's own headline** |

**Five of the six are one defect**: captions off, source has nothing, nothing refuses it.

**#7 is ours and it is proven.** The staged source reads **"Bob Lee Swagger proves he planned
for his own frame job"**. The finished video reads **"3ob Lee Swagger…"** — the B cut off on the
left in every frame. This is the LEFT-slice MEMEBOT-102 found and MEMEBOT-108 saw recur; it is
now confirmed as a property of our crop rather than of the source, by comparing the two files.

### SELECTION — 14, and each one classified

| gate status | n | clips |
|---|--:|---|
| **a term exists and it MISSED** | **6** | #8, #9, #11, #15, #16, #27 |
| deliberately ungated, measurement on record | 5 | #3, #5, #18, #20, #21 |
| **no term, none proposed** | 3 | #4, #19, #25 |

- **Ungated with a measurement on record** — #3, #18, #20 are dead canvas / padded inset
  (BL-1004: every cheap geometric candidate 0.00–0.23 precision); #5 is graphic violence against
  a child and #21 is an ethnic slur legible in a burned-in subtitle (BL-988: 4 candidates in
  2,661, all 4 false; the real case needs on-screen text, missing on 92.3%). **Those refusals
  still measure correctly. They are not errors; they are unpaid bills.**
- **No term** — #4 the source's own hook ends mid-clause on the word "in"; #19 the source page's
  promo line stacked above the hook; #25 a "Part 10" fragment of somebody else's series with
  untranslated Korean dialogue.

### The correction MEMEBOT-108 could not make

**The pillarboxed inset is the SOURCE's layout, not our crop.** I pulled the staged source for
#4 and #18 and the padded inset with rounded corners is *already there* before we touch the
file. MEMEBOT-108 listed "pillarboxed inset / dead canvas" as its largest **render** class; on
this sample it is a **selection** property. Our template contributes — `white_frame` scales the
video to **864 px on a 1080 canvas** with `y_offset: 280`, so 108 px of canvas each side is by
design and a landscape source can never fill the height — but the four-sided inset that reads as
the defect arrives with the clip.

Likewise **#4's truncated hook is the source's own text**, stored truncated and burned into the
source's pixels. We did not cut it.

---

## 5. The watermark term is aimed at the wrong reference, and that is now the dominant cause

Six videos ship somebody's brand. I asked the term about each rather than guessing:

```
#8  'PaxToPrime' + 'DAY-98'   burned_in_identity -> (False, False)   caption: "follow @paxtoprime.in"
#15 '@house_of_julmi'         burned_in_identity -> (True,  False)   <- SAW IT, CLEARED IT
#16 '@CartoonHub'             burned_in_identity -> (False, False)   pixel text EMPTY
#9  '@culturemeetsonline'     burned_in_identity -> (False, False)   pixel text EMPTY
#11 '@movi.facts'             burned_in_identity -> (False, False)   pixel text EMPTY
#27 'MC' logo                 is_static_non_clip -> False
```

`foreign()` contains:

```python
if n in acct or acct in n:
    return False
```

**The source account's own handle is never third-party.** For a reposter that is backwards:
every clip we take is somebody else's, so the source page's own burned-in mark is *precisely*
the one that must not ship. MEMEBOT-108 named this as an honest limit on a single case (`@nm`);
here it is the cause of **half the watermark escapes**, and on #15 the term read the handle and
actively cleared it.

**What removing that clause would cost, measured:**

```
clips where a handle/domain appears in the text at all : 211  (7.7% of 2,728)
  ...already refused as third-party                    : 117
  ...currently CLEARED as the source's own             :  94  (3.4% of the library)
       of those 94, the handle is in the PIXEL text    :  94   <- all of them
       ...in the caption only, no evidence in frame    :   0
```

**All 94 are real burned-in marks**, not captions saying "follow me" — samples: `@planet_mim`
on `planet_mim`, `@WAYNE___29` on `wayne__29`, `@memedwyd` on `memedwyd`. This is the cheapest
real improvement this audit found: **one deleted condition, 3.4% of supply, no new detector.**

The other three escapes are the emptiness problem and no rule reaches them.

---

## 6. Instruments, validated against the frames before being believed

The brief named four detectors in this family that produced confident wrong numbers. Everything
below was checked against hand-read frames first.

**`vision_on_screen_text` empty is wrong on 5 of 9.** The field is empty on 9 of the 30. Reading
the frames, **five of those nine carry plenty of burned-in text** — #7, #9, #11, #16, #19 — and
four are genuinely bare. BL-988 wrote the emptiness rule from the field's own statistics and
said it could not validate recall against pixels. **This validates it from the pixel side: a
56% error rate on this sample**, consistent with BL-1002b's 0% watermark recall.

**The Portuguese caption that got through, and the obvious fix that does not fix it.** #24's
caption is plainly Portuguese and `is_non_english_caption` returned **False** — none of
`_ROMANCE_ID`'s stopwords (`que para com uma dos das …`) appear in it. The obvious candidate is
an orthographic signal:

```
add [ãõç] to is_non_english_caption
   captions containing one            : 59  (2.2%)
   already caught by the stopword list: 54
   NEW refusals                       :  5   -- 4 Portuguese, 1 English-with-a-flag-emoji
   does it catch #24?                 : NO  -- its accents are á, é, ó
```

**+5 clips at roughly 80% precision, and it does not catch the case that motivated it.** Adding
`do`/`da` would, and `do` is an English word. **Reported as a gap, not shipped as a rule.**

I built no geometric dead-canvas detector. BL-1004 measured nineteen thresholds against hand
labels and the best scored 0.23 precision; MEMEBOT-108 reproduced it from the other direction.
Two independent refusals is enough.

---

## 7. Not copying anything to `outputs_for_operator/`

The brief's floor was **15**. It is **10**. **No folder was created and nothing was copied.** The
eight videos an earlier round left there are untouched. Ten of thirty is not a shippable batch,
and a folder of "the best available" invites exactly the reading the threshold exists to prevent.

---

## 8. One clip lost to somebody else's edit

A candidate died inside edit.py during the run:

```
apply:exception  NameError: name '_caption_margin_px' is not defined
```

Not my code and not in HEAD — a concurrent round was mid-edit on `edit.py`. The orchestrator did
the right thing and took the next candidate, which is why the batch still finished 30 of 30. It
is recorded here because a NameError in a shipped renderer is worth its owner's attention.

---

## 9. Suites — 9 red of 201, every one checked directly, none of them mine

`tests/run_all.py`, 201 suites, **5,734 s: 192 green, 9 red.** I changed no shipped file, so I
re-ran every red on its own with the exit code read without a pipe rather than waving at them:

| suite | in the batch | direct re-run | cause |
|---|---|--:|---|
| `test_claim_location.py` | FAIL | **0** | false red under concurrency |
| `test_enrich_concurrent.py` | FAIL | **0** | false red under concurrency |
| `test_runner_contract.py` | FAIL | **0** | false red under concurrency |
| `test_doc_citations.py` | FAIL | 1 | `docs/FINAL_STATE.md:45` cites `tests/run_all.py:76`; the anchor moved to line 79 |
| `test_no_unchecked_stdout.py` | FAIL | 1 | `tests/run_all.py:192,207` — same live edit |
| `test_gate_audio_class.py` | FAIL | 1 | a **108-line uncommitted edit** to `clip_pipeline.gate()` |
| `test_guard_resolution.py` | FAIL | 1 | another round's `tests/test_decision_log_redaction.py` |
| `test_selection_gate_wired.py` | FAIL | 1 | `edit._UNRENDERABLE` tuples changed shape under a live edit |
| `test_vendor_sources.py` | FAIL | 1 | `tools/run_status.py:73` — **clean at HEAD, so pre-existing** |

**Three of the nine are false red** — they pass alone. Of the six that reproduce, five are
traced to named uncommitted edits in other rounds (16 tracked files are `' M'`; none are mine)
and one is pre-existing at HEAD. **No red mentions any file this round wrote.**

**The first attempt at the suite did not run at all**: `NameError: name 'threading' is not
defined` from `tests/run_all.py` while it was being written. The second attempt, after that
edit settled, is the run above.

**And this bears on reproducibility, so it goes on the front and not in a footnote:** the thirty
were rendered against the **working tree**, not a pinned HEAD snapshot. `clip_pipeline.py`'s
current 108-line edit was written at **15:25**, forty-nine minutes after the batch finished at
14:36, so it is not what my run executed — but I recorded the parent SHA and not the dirty
state, so I cannot prove the tree was clean at 14:17. The gate wiring and the interleaving I
credit in §1 are both **in HEAD** (`postability_reasons` ×3, `interleave_by_account` at line
759), not in anybody's uncommitted work.

## Proof

| claim | evidence |
|---|---|
| 30 through the real shipping path | `run.py --funnel clip_render --target 30 --cap 0.12`; `scratch/mb119_render.log` |
| interleaving live | 30 accounts / max 1, against 11 / max 7 with `interleave=False`; `scratch/mb119_interleave.json` |
| gate at scale | 2,728 → 2,274 kept / 454 refused (298 / 117 / 62); `scratch/mb119_gate_scale.json` |
| four verifications | video 30/30, audio 30/30, floor 30/30, ceiling 30/30, **prov 30/30**, song 29/30, join 30/30 |
| song is the configured track | 40–250 Hz signed r vs the APPLIED window, lag bounded to one hook period, every other store track as null; 0.3147 / 0.9045 / 0.9652 against nulls 0.1786 / 0.2943 / 0.4146 |
| all 30 watched | 30 contact sheets, six full frames each, `scratch/mb119_frames/` |
| the caption is never drawn | edit.py's own stdout, captured; `templates.yaml` → `white_frame.caption.enabled: false` |
| the LEFT-slice is ours | source frame reads "Bob Lee Swagger", output reads "3ob Lee Swagger" |
| the pillarbox is the source's | staged source frames for #4 and #18 already carry the padded inset |
| the number | **10 postable of 30**, bar stated in §3 |
| the split | **6 RENDER / 14 SELECTION**; of the 14: **6 missed by an existing term, 5 ungated with a measurement, 3 with no term** |
| the own-account rule costs 94 clips | 211 with an identity, 117 already refused, 94 cleared as own — **94 of 94 in pixel text** |
| the emptiness field is wrong on 5 of 9 | hand-read frames vs `vision_on_screen_text` |
| no operator folder | 10 < 15; `outputs_for_operator/` untouched |
| spend | **$0.0384** of a $0.12 cap; ledger delta $0.0582 across concurrent rounds |
| suites | **192 of 201 green**; 3 of the 9 reds pass standalone, 5 traced to other rounds' live edits, 1 pre-existing at HEAD |
| config valid, campaigns unchanged | `config.json` parses; `clip_pipeline_max_run_usd` still `None` so `--cap` was not persisted; the file is gitignored and this round never writes it |

---

## Honest limits

- **PASS/FAIL is my judgement against a stated bar, not a measurement.** Five calls were
  borderline; a stricter reader lands at 6 and a looser one at 12.
- **Six frames per video.** A defect that lives between sampled frames is invisible here.
- **I proved the pillarbox is the source's on two clips (#4, #18), not on all four.** The
  template's 864/1080 geometry is read from `templates.yaml` and applies to all thirty, but the
  attribution of the *four-sided inset* rests on two source comparisons.
- **`config.json` changed on disk during the round.** It is gitignored, I never write it, and
  `run.py` deep-copies before mutating (its own comment: *never mutate the caller's dict*);
  `clip_pipeline_max_run_usd` is still `None`, so my `--cap` was not persisted. But I recorded
  only a hash at the start, so I can say it changed and **not** what changed.
- **The ledger delta ($0.0582) is larger than this run's own figure ($0.0384)** because
  `spend.json` is shared. The run's own meter is the round's number.
- **I did not re-measure BL-988's or BL-1004's precision figures**; their refusals are taken as
  given and only their *consequences* are counted here.
- **The 94-clip figure for the own-account fix is a supply cost, not a precision measurement.**
  All 94 have a handle in pixel text; I did not hand-read 94 sets of frames to confirm each mark
  is visible.
