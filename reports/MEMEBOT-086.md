# MEMEBOT-086 — the duration ceiling, decided against the hand labels: **trim keeps 1,487 clips and 93% of payoffs; a gate keeps 481.** 30 re-rendered: **source median 55.3 s → finished 18.4 s, 30/30 inside 7–20 s, nothing over 20.0 s.** A 100k page would post **5** — up from MEMEBOT-074's 3, and this time **all five are actual video clips**, not infographics.

**Date:** 2026-08-02 · **Type:** fix + viewer audit · **Spend:** **$0.0180** of a $0.30 budget
**Wrote:** `memebot/scraper/duration.py`, `memebot/scraper/config.yaml`,
`memebot/scraper/tests/test_duration.py` (commit `9fd3b5c`), and `scratch/mb086_*`.
**Read but never wrote:** `memebot/scraper/edit.py`, `templates.yaml`,
`clippershq/clip_pipeline.py`, `ground_truth/`.

---

## The scope I could take, said first

`memebot/scraper/edit.py` and `templates.yaml` were claimed by **MEMEBOT-082 at 15:44, twenty
minutes before this round started**, and its intent covers **items 2 and 3 of my brief
verbatim** — the `caption_hook` payoff word and the vertical content crop. It was not an idle
claim: `edit.py` moved four times while I worked (16:06, 16:12, 16:25, 16:54) and grew 14 KB.

So I did not write it. Two writers on one file is the hazard this repo has paid for most, and
the collision is silent. **Items 2 and 3 were delivered by MEMEBOT-082 (`ba0ce2b`); I verified
both independently and they hold** (§3, §4). Item 1 is mine and its policy shipped; its one
wiring call is the only thing I could not land, and it is handed over exactly rather than
guessed at.

---

## 1. Duration: gate or trim, decided by measurement

Two options, priced against `ground_truth/clip_drop_labels.json` — 28 clips, each with the
payoff second chosen by a human off a 1 fps contact sheet (BL-963) — and against all 1,999
library clips carrying a duration. `scratch/mb086_duration.py`.

### Where the payoff actually is

```
drop second : median 7.0s   p75 16.2s   p90 20.0s   max 30.0s
as a fraction of duration : median 0.43   IQR 0.27-0.65
```

**It is not proportional, and that is the whole question.** If the payoff sat at a fixed
fraction, a head window would systematically miss it on long clips and trimming would be
indefensible. It does not:

| | clips ≤ 20 s (n=17) | clips > 20 s (n=11) |
|---|---:|---:|
| drop, median | **5.0 s** | **17.0 s** |
| drop as a fraction | 0.46 | **0.34** |

`corr(duration, drop) = 0.73`. As clips get longer the payoff moves proportionally **earlier**.
On no measured clip is it in the last third of a long one. **Cutting the tail cuts away from
the payoff; cutting the head cuts toward it.**

### Survival, both options, at the same number

| ceiling | **GATE** — clips surviving the *whole* gate | **TRIM** — clips kept | payoff kept |
|---|---:|---:|---:|
| 15 s | 339 | 1,487 | 20/28 (71%) |
| **20 s** | **481** | **1,487** | **26/28 (93%)** |
| 25 s | 559 | 1,487 | 27/28 (96%) |
| 30 s | 652 | 1,487 | 28/28 (100%) |

*(1,487 is what passes the gate today at `MAX_DURATION_S=90`; the gate column runs the whole
gate, not just its duration term, because the other seven terms cut clips too.)*

**A 20 s gate discards 1,006 of the 1,487 renderable clips — 68% — to protect a payoff a tail
trim keeps nine times in ten.** That is not a trade worth making. **The ceiling trims.**

**Why 20.0 and what 22.0 would buy.** 20 s is the top of the stated 7–20 s norm. It is not
free: 3 of those 26 land within 2 s of the cut, so the window ends almost on the drop. A 22 s
ceiling keeps the same 26/28 *with* 2 s of post-roll on all of them (23/28 → 26/28 with
post-roll). That is a taste call about two seconds and it is the operator's — which is why
`ceiling_s` is a config knob, not a constant.

**The limit, stated where the number is.** The labelled set spans 8–60 s and is not random
(`ground_truth/README.md` limit 5). **Nothing here measures where the payoff sits on a clip
longer than 60 s**, and 5% of the library is over 90 s. Above 60 s this is extrapolation.
Excluding the 3 low-confidence labels changes nothing: 23/25 at 20 s, the same 92%.

### What shipped

`duration.plan_ceiling()` and `duration.assert_ceiling()`, in the module that already owns
`FLOOR_S`, `plan()` and `assert_floor()`, plus a `transform.duration_ceiling` config block.
**13 new tests; 32/32 green in `test_duration.py`; all 9 memebot suites green (208 tests).**

Two details the tests pin, because both are easy to get wrong and silent when wrong:

- **The arithmetic is in OUTPUT seconds.** edit.py applies speed *after* trimming, so a 1.08×
  roll on 20 s of source finishes at 18.5 s and a 0.93× roll at 21.5 s — over a ceiling that
  source-seconds arithmetic calls satisfied. The fixture asserts the two shipped speeds give
  **different** answers before asserting either, so it cannot pass vacuously.
- **It never double-counts the rolled trim.** The anti-fingerprint roll has already shortened
  the clip; `already_trimmed_s` is subtracted first.

A ceiling below the floor **raises** rather than resolving silently — they are the same video's
maximum and minimum and cannot cross.

### The one thing that is NOT wired, said plainly

**`plan_ceiling` has no production caller.** Its home is one block in
`edit.py:build_transform_filters`, immediately after `_floor_trim_budget`, plus two config
readers and one `assert_ceiling` call beside `assert_floor`. `edit.py` was held and being
written throughout. The exact patch is **`scratch/mb086_wiring.patch`** — the block, the
readers, the call site, and the two tests that fail if either argument is dropped.
**Owner: whoever next holds `memebot/scraper/edit.py`.**

I did not bolt it into `verify_transforms.py` to avoid being "uncalled". That file is a
variant-comparison tool; putting a duration check there to dodge a lint would be worse than an
honest hand-off.

---

## 2. The trailing-word bug — fixed by MEMEBOT-082, verified here on all 5 real cases

MEMEBOT-074's five, run through `edit.caption_hook` at the current build:

```
'lil bro pulled an ELITE'                -> 'lil bro pulled an ELITE'
'Hype is real'                           -> 'Hype is real'
'I knew you in another life'             -> 'I knew you in another life'
'people actually believed this'          -> 'people actually believed this'
'Might have to rewatch bleach honestly'  -> 'Might have to rewatch bleach honestly'
```

**5 of 5 intact.** Previously each lost its last word to the no-terminator rule.

**It is now moot in the rendered output as well, for a second reason.** MEMEBOT-082 also set
`caption.enabled: false` — the source's own overlay is the hook. Verified end to end on a live
render whose ledger caption was `'I'm sorry for the Batman glaze'` (no terminator, exactly the
bug's shape): the finished frame carries **no added caption at all**, and the source's own
`"Let's not forget how Darkseid felt Batman aura from the other side of the universe"` intact.

**One thing that follows and is worth someone's attention (not chased here):**
`clip_pipeline.render_one` still always passes `--override-text`, and `run_batch` still records
`render.caption` in the ledger. With `caption.enabled: false` that text is computed, recorded,
passed — and never appears. That is a recorded-but-not-acted-on mismatch of the shape this
project keeps finding. **Owner: `clippershq/clip_pipeline.py` (held by BL-899 and MEMEBOT-081).**

---

## 3. The vertical content crop — fixed by MEMEBOT-082, verified on the same source

MEMEBOT-074 measured, on `thomasabg`'s 720×1280 staged source, that the caption ink begins at
**row 197** and `detect_content_crop` returned `crop=720:798:0:200` — three rows of ascenders
discarded, then scaled up ~1.43×.

Re-run against the same file at the current build:

```
was : crop=720:798:0:200     ink at row 197  ->  3 rows of the headline cut
now : crop=720:830:0:184     ink at row 197  ->  13 rows of clearance
```

**Fixed, with margin.** Across the 30 fresh renders I read no instance of `"rIFA WORLD CUr"` or
`"Kip Wheeler"` — the source headlines are intact.

---

## 4. Thirty re-rendered and watched

Rendered through the real library, `rank_candidates`, the real paid re-fetch, `pick_song` with
no `explicit_song`, `fit_window`, `audio_treatment` and `render_one` — with the ceiling applied
to the staged source, since its shipped call site was held. **One `edit.py` build across all 30**
(sha `c6339217`, checked before and after — MEMEBOT-074 was bitten by a split build).

### Duration: the defect is closed

```
SOURCE   median 55.3s   max 87.1s   25 of 30 over 30 seconds
FINISHED median 18.4s   max 20.0s   min 8.2s
inside the 7-20s norm : 30 / 30          over 30s : 0 / 30
under the 20s ceiling : 30 / 30 (assert_ceiling on the artefact)
still clearing the 8s floor : 30 / 30
```

MEMEBOT-074: 20 of 30 over 30 s, longest **91.6 s**. Now: **none over 20.0 s.**

### Would a 100k page post them? **5 of 30 — and all five are video clips.**

| # | account | what it is | dur | dead | verdict |
|---|---|---|---:|---:|---|
| 4 | moviexsuggestion | Bend It Like Beckham, title card + subs | 18.9s | **12.7%** | **Post** — fills the frame, hook intact, right length |
| 6 | zackrawrrshorts | "Women vs Men with 1 leg" reaction | 18.3s | **8.5%** | **Post** — native format, fills the frame |
| 3 | smoovereactss | Batman/Darkseid reaction | 19.8s | 22.5% | **Post** — source's hook is the joke and it is intact |
| 9 | ashoraif | "Curiosidade na América" card | 18.8s | 13.6% | **Post** — fills the frame; it is another page's brand |
| 1 | matheuxmendex | House of the Dragon, PT-BR subs | 18.0s | 25.7% | **Post** for a PT audience; marginal for a general one |
| 24 | cinemavault.01 | Reacher, CINEMAVAULT bar | 19.7s | 15.7% | **Near miss** — republishes a rival's *verified tick* |
| 8 | solidshampooz | "How the coworkers you DESPISE…" | 8.2s | 54% | **Near miss** — best hook in the batch, half the frame is white |

The other 23 fail on composition or legibility, not on length and not on captions.

### What is wrong with the rest, ranked

| rank | problem | videos | why |
|---|---|---:|---|
| **1** | **Nested letterbox — ≥40% dead canvas** | **18 / 30** | the source is *already* a padded canvas (black bars + its own caption bar + a rounded video window); ours pads it a second time. Median dead canvas **44.0%**, worst 60.5% |
| 2 | Another page's watermark or brand bar republished | ~10 / 30 | `#24` carries a verified tick; `#19` a third party's URL; PRIMECUTTV, @CartoonHub, @GUCCI_BELLUCCI |
| 3 | Too dark to read on a phone | ~5 / 30 | `#5` is near-black throughout |
| 4 | Song not attributable | 7 / 30 | see §5 — partly a real cost of the ceiling |
| 5 | Static collage, nothing moves | 2 / 30 | `#27` is a 6-panel text collage |
| 6 | Song concentration unchanged | 26 / 30 = song04 | 87% one track, as MEMEBOT-074 measured. Not this round's item |

**Rank 1 is now the whole problem, and it is a different problem from MEMEBOT-074's.** There,
the top two were duration and scraped captions. Both are gone. What is left is that this
library is mostly reposts-of-reposts whose sources are already letterboxed, and a 1080×1920
white canvas cannot rescue a 4:3 picture inside a black box.

---

## 5. The instruments, bounded

- **The correlation null is hook-bounded, always.** MEMEBOT-074's first null handed
  `best_corr` a whole 162 s track, which let the lag search slide across its full duration and
  score **0.94 against a track the render never touched**. Every reference here is a marked
  hook window (10–27 s), which bounds the search to the window. **23 of 30 carry the configured
  track** (median r 0.80).
- **That is down from 27/30, and part of it is the ceiling's own cost.** A 20 s video gives the
  envelope a fifth of the frames a 90 s one did, and the bed loops more within it. Five of the
  seven misses have small negative margins (−0.03 to −0.49) rather than absent audio — the bed
  is audible on all 30. I am not claiming the ceiling caused all seven; I am saying a shorter
  clip gives this method less to work with and that is a real, stated cost.
- **There is no automated caption-clip detector in this round.** MEMEBOT-074 wrote one, it
  flagged 7 and 4 were false — it counted the source's own dark band edge as a caption line. A
  detector wrong 57% of the time is worse than none, because its count gets quoted. Caption
  defects here were found by reading bands at full resolution.
- **Frames read:** 5 full 4-up sheets at half resolution, 25 more as three labelled montages,
  2 full-resolution caption bands, 1 full frame. **All 30 looked at; 5 in detail.** Fine detail
  on the 25 is montage-resolution, and a defect finer than that would not have shown.

---

## 6. Noted, not chased (brief item 6)

- **Dead canvas is not fixed and is marginally worse: median 44.0% here vs 39.2% in
  MEMEBOT-074.** MEMEBOT-082's `vertical_align: center` splits the waste evenly instead of
  piling it at the bottom, which reads far better — but centring *moves* white, it does not
  remove it, and the bounding-box measure is unchanged by where the margin sits. The mix of
  sources also differs between the two batches. Not this round's item.
- **`position_shift_y` does not walk the video into the caption** — `edit.py` adds the same
  shift to the caption's `y`, so the clearance is preserved at every shift. MEMEBOT-074
  corrected itself on this mid-audit; re-verified, still true, and now moot because the added
  caption is off by default.

---

## Verification

| check | result |
|---|---|
| gate-vs-trim decided against | **28 hand labels** + 1,999 library clips, `scratch/mb086_duration.py` |
| ceiling policy | `duration.plan_ceiling` / `assert_ceiling`, **13 new tests** |
| memebot suites | **9 files, 208 tests, all green** (`test_duration.py` 32/32) |
| trailing-word fix proven on | **5 of 5** real MEMEBOT-074 cases, plus one live render end to end |
| vertical crop | `crop=…:0:200` → `crop=…:0:184`, ink at row 197 — **13 rows of clearance** |
| renders | **30**, one `edit.py` build (sha `c6339217` before and after) |
| duration | 30/30 in 7–20 s, max **20.0 s**, 0 over 30 s; 30/30 still clear the 8 s floor |
| postable | **5 of 30**, all five video clips |
| paid calls | 30 re-fetches, **$0.0180** |
| shipped code changed | `memebot/scraper/` only — `duration.py`, `config.yaml`, `tests/test_duration.py` |

## Limits

- **The ceiling is not live.** `plan_ceiling` has no production caller; the 30 renders applied
  the same arithmetic one stage earlier, to the staged source. That measures what the ceiling
  buys a viewer, which is the question, but it is **not** a test of the shipped call path.
  `scratch/mb086_wiring.patch` is the hand-off.
- **Above 60 s the ceiling is an extrapolation.** The labelled set spans 8–60 s and is not
  random; 5% of the library is over 90 s and nothing measures where their payoff sits.
- **n = 28, one labeller, one pass, 1 s resolution.** No inter-rater figure exists. A second
  labeller on the same 28 sheets costs $0 and is the cheapest thing anyone could do to this
  result.
- **These 30 renders did not write `memebot/runs.jsonl`.** They carry a ceiling the shipped
  code does not apply, and a shared append-only ledger has no way to tell them apart from
  production afterwards. So there is no ledger-join evidence for this batch.
- **"Would a page post this" is judgement.** The duration and caption findings are measured;
  the count of 5 is taste, informed by the format.
- **I declared `scratch/mb086_render.json` and `scratch/mb086_work` too late** — they were
  written before being added to the claim, and `commit.py` flagged them as unclaimed. Harmless
  here, and the kind of thing that is not harmless when two rounds share a directory.
