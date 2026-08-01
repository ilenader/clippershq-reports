# MEMEBOT-013 — The feedback loop is built. At n=20 it answers **nothing**, on all six questions — including one where I planted a real 1.6× effect and it correctly failed to find it.

**Date:** 2026-08-01 · **Type:** Implementation · **Spend:** $0.00 · **Paid calls:** 0
**New:** `clippershq/outcome_loop.py`, `tests/test_outcome_loop.py`, `scratch/mb013_demo.py`.
No existing clippershq or memebot module was edited. `memebot/runs.jsonl` untouched (433 bytes).

---

## The demonstration that matters

I generated 20 fake outcomes where **`song01` really is 1.6× better** — a genuine effect, built
into the data on purpose. Here is what the analysis says:

```
song            2 groups   VERDICT: NOT_ENOUGH_DATA
    scratch/song01.mp3    n=10  median=2244   NOT_ENOUGH_DATA
    scratch/song02.mp3    n=10  median=2316   NOT_ENOUGH_DATA
```

**The planted winner shows a median 3% LOWER than the loser.** A real 60% advantage is invisible
at n=10 per arm, because view counts are log-normal and the spread swamps it. That is not a bug
in the analysis — it is the honest answer, and it is exactly why a dashboard showing a winner
here would be worse than one showing nothing.

The demo also contains the tempting false signal you would have acted on:

```
hook  scratch/song01.mp3@20.0-25.0    n=4   median=18,038
      scratch/song01.mp3@120.0-162.0  n=3   median=   760
```

**A 24× apparent gap.** Both are `NOT_ENOUGH_DATA`. On n=4 versus n=3 that gap is what random
log-normal draws look like.

**All six questions return `NOT_ENOUGH_DATA` at n=20.** A test pins that as a contract.

---

## 1. The record format

`memebot/runs.jsonl` carries **no id field** — I checked, its 13 keys have nothing addressable.
Rather than rewrite those lines to add one (which would break append-only on the very first
change), **`record_id` is DERIVED from `output`**, the rendered file path, unique per video by
construction. Existing lines become addressable without being touched.

An outcome is a **new line**:

```json
{"record_id": "out/vid_000.mp4", "rev": 1, "kind": "outcome",
 "posted_to": "instagram", "posted_at": "2026-08-03",
 "views": 12400, "likes": 310, "comments": 12, "saves": 44, "shares": 9, "note": ""}
```

Fill numbers in later by appending `rev: 2`. `resolve()` takes the **highest rev per
record_id**, so a correction never destroys what it corrected — the earlier line stays readable,
which is what lets you see that a number was revised and when.

**Proven, not asserted:**

```
REV CORRECTION: out/vid_000.mp4  5209 -> 999999   (file is now 41 lines; nothing rewritten)
```

A test asserts the original bytes are a strict prefix of the file afterwards — pure append.

**Three edge cases are handled deliberately:**

- **`has_outcome` distinguishes unposted from zero.** An unposted video has no `views` key at
  all, not a 0. A recorded 0 *is* an outcome. Conflating them poisons every median.
- **Out-of-order revs resolve correctly** — writing `rev 2` after `rev 5` does not win.
- **An orphan outcome surfaces** with `orphan: true` rather than vanishing, so a typo'd
  record_id is visible instead of silently dropping the data you typed.
- A torn line is skipped, never fatal — the whole reason this is JSONL.

## 2 + 3. The analysis, and the minimum n

**Medians with a bootstrap CI, not means with a t-test.** View counts are log-normal: a handful
of videos carry most of the views, so a mean is dominated by the outlier. The comparison is
non-parametric, with a fixed seed so the same data always gives the same interval — an interval
that moved between runs would not be evidence.

Three verdicts only: `NOT_ENOUGH_DATA` · `NO_DIFFERENCE_DETECTED` · `DIFFERENT`. **No p-value,
no "leading" arm, no ranking of groups that have not separated.**

**Minimum posts needed** — 80% power, α=0.05, large effect (Cohen's d=0.8 → 16/d² ≈ 25 per arm):

| question | groups | per arm | **posts needed** |
|---|---:|---:|---:|
| song | 2 | 25 | **50** |
| treatment (mute vs duck) | 2 | 25 | **50** |
| clip_source | 3 | 25 | **75** |
| hook window | 4 | 25 | **100** |
| content_genre | 4 | 25 | **100** |
| duration_band | 4 | 25 | **100** |

**So: keep rotating blindly for about 50 posts before the first question (song, treatment) can
be answered at all, and ~100 before hook windows can.** And that is the floor for a *large*
effect. A subtle one — the kind most of these probably are — needs several times it: a medium
effect (d=0.5) is 64/arm, so 128 posts for a two-arm question.

**I would not power for a small effect.** At d=0.3 you need 178 per arm — 356 posts for one
two-arm question — and an effect that small is not actionable even when real.

## 4. The feedback rule

Rotation stays **least-used-first** (MEMEBOT-008) until a hook window clears **both** bars:

1. **≥ 25 outcomes on that window**, and
2. its median beats the pooled rest by a bootstrap CI that **excludes zero**

Then rotation may bias toward it, and only to **`BIAS_WEIGHT = 2.0`** — at most twice as often,
**never exclusively**, because a window that stops being sampled can never be shown to have
degraded.

The gate on the demo data:

```
best-looking window : scratch/song01.mp3@20.0-25.0 (n=4, median 10,602)
bias allowed        : False
reason              : need >= 25 per arm; have 4 and 16. Any gap here is noise.
```

Tests pin all four refusals: thin data, CI straddling zero, and — the one people forget — a
window that is **significantly worse** never earns bias either.

## 5. The manual path

```python
export_csv(runs_jsonl, "outcomes_blank.csv")   # one row per video with no outcome yet
# ... fill views/likes/comments/saves/shares in any spreadsheet ...
import_csv("outcomes_blank.csv", runs_jsonl)   # appends one outcome line per filled row
```

`only_missing=True` by default, so you never re-type a video you have already recorded. Numbers
parse with commas (`1,234` → `1234`).

**A blank row writes nothing.** A test asserts an all-blank sheet imports **0 rows** — "not
filled in" and "zero views" are different facts, and a fabricated zero would drag every median
down permanently.

**No platform API.** Not built, not stubbed, deliberately out of scope.

## 6. What would make this wrong

Six confounds, in `CONFOUNDS` in the module so they travel with the code:

| confound | why it manufactures a trend |
|---|---|
| **best-clips-first** | **The subtle one.** Early videos use the best clips, so later ones look worse **by construction**. A downward trend over time is the *expected artefact*, not degradation. Compare within a time window, never across the whole history. |
| posting_time | 7pm vs 4am swamps most song effects |
| account_size | The same video on 200 vs 20k followers differs by an order of magnitude. Compare *within* an account, or the account **is** the finding. |
| boosting | A boosted post is not an organic sample, and nothing here can detect it — record it in `note` and exclude by hand |
| platform_drift | Reach on identical content changes as ranking changes; March vs August is partly the platform |
| survivorship | A deleted flop is absent, so the surviving median is optimistic |

**The demo's own `clip_source` numbers are a live example**: `cultureh0f` shows a median of
14,095 against `movies.avengers` at 896 — 16× — on n=7 vs n=6. That is the account-size confound
and small-n noise, indistinguishable from each other and from a real effect. The analysis
refuses all three readings.

---

## Verification

| check | result |
|---|---|
| `tests/run_all.py` | **ALL GREEN — 62/62 suites, 2,633 checks** |
| `tests/test_outcome_loop.py` | **PASS — 42 checks** |
| append-only proven | original bytes are a strict prefix after 2 outcome appends |
| rev last-wins | including out-of-order revs |
| blank CSV row | **writes 0 records** |
| 100× gap at n=5 | **NOT_ENOUGH_DATA**, no interval offered |
| real gap at n=40 | **DIFFERENT**, CI excludes zero |
| bootstrap determinism | same data → same interval |
| n=20 across 6 questions | **all NOT_ENOUGH_DATA** |
| campaigns SHA | **8e02f8d6f6307ae8 — MATCH** |
| `config.json` | parses, 162 keys, untouched |
| existing modules | **none edited**; `memebot/runs.jsonl` still 433 bytes |

---

## Limits

- **The 20 outcomes are fake.** Generated log-normal with a planted effect to show what the
  analysis does; they say nothing about real performance.
- **`MIN_N_PER_ARM = 25` is a standard power calculation, not a measurement from this domain.**
  It assumes a large effect on log views. If real between-song variance is wider than assumed,
  25 is optimistic.
- **Every comparison is one group against the pooled rest**, not pairwise. With six questions
  and several groups each, pairwise testing would inflate false positives and there is nowhere
  near the data to pay for a correction.
- **Nothing is wired.** `outcome_loop` reads and writes JSONL; no renderer calls it and
  `song_library.pick()` does not yet consult `should_bias()`. That wiring is one line each and
  is deliberately not done here — the rule should be agreed before it is enforced.
- **The confound list is not exhaustive**, and none of the six is *corrected for* — they are
  named so you do not read an artefact as a trend. Correcting for them needs stratification,
  which needs more data than answering the base question does.
- **`import_csv` has no dry-run.** It appends immediately. Appends are non-destructive, so the
  fix for a mistake is another `rev` — but there is no preview.

---

## Method

Filed a claim (10 rounds in flight, no path conflicts). Read the real `memebot/runs.jsonl` to
confirm its key set and the absence of any id field before designing around it. Built the module
against that shape, then generated 20 render records **in the real MEMEBOT-007 format** and
20 log-normal outcomes with a deliberately planted 1.6× effect, so the analysis had something
true to miss. Bootstrap CIs use 2,000 resamples with a fixed seed. Minimum-n figures are the
standard `16/d²` two-sample requirement at 80% power and α=0.05. No API call, no spend, and no
edit to any existing module in either project.
