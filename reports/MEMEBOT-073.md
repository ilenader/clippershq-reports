# MEMEBOT-073 — the gate was already fixed, its guard was not, and 20 of 20 renders carry their track

**Date:** 2026-08-02 · **Class:** Correction + guard + measurement at scale · **Spend:** **$0.0114** of a **$0.05** budget (ledger delta; 20 renders, 45 minutes)

Preconditions read before any write: `tools/claims_read.py --holders` per target **and**
`git status --porcelain` with the index and worktree columns read separately. Claimed as
`MEMEBOT-073`, eight repeated `--write` flags, no path conflicts. Ledger backed up
(`scratch/mb073_runs.pre.bak`, 210 lines).

---

## 0. THE CORRECTION, FIRST — the brief's premise and my own report were both out of date

**`MIN_DURATION_S` was not 5.0. The mismatch was not open.** BL-958 landed the derivation in
commit `b45d66a` at **12:54:41**:

```python
RENDER_FLOOR_S        = 8.0    # config.yaml transform.duration_floor.floor_s
RENDER_FLOOR_MARGIN_S = 0.20   # edit.py _floor_trim_budget: `target = floor + 0.20`
RENDER_MIN_SPEED      = 0.93   # config.yaml transform.speed.min — below 1.0 LENGTHENS
MIN_DURATION_S = round((RENDER_FLOOR_S + RENDER_FLOOR_MARGIN_S) * RENDER_MIN_SPEED, 3)
```

**MEMEBOT-072 published a limits section calling it open at 13:40 — 42 minutes later.** That
is mine. I carried MEMEBOT-064's finding forward as a live limitation without re-reading the
constant, in a file I had edited and committed that same hour. A limitation inherited from an
earlier report is a claim about the code *now*, and it has to be re-measured like any other
number. [MEMEBOT-072 is corrected in place](https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/MEMEBOT-072.md):
the wrong paragraph is struck through with the correction above it, so a reader following a
link to the old text still sees what it said and why it was wrong.

**So this round did not fix the gate. It fixed the guard on the gate, and then measured what
nobody had.**

---

## 1. THE DRIFT GUARD READ EDIT.PY THROUGH A PREFIX

BL-958's guard checks two of the three numbers against `memebot/scraper/config.yaml` — a real
read, and right. The third, the margin, is not in the config; it is a literal in edit.py, and
the guard looked for it like this:

```python
self.assertIn("target = floor + %s" % CP.RENDER_FLOOR_MARGIN_S, body)
```

`"%s" % 0.20` is **`"0.2"`**. The needle is `target = floor + 0.2` — a **prefix**:

```
edit.py says 'target = floor + 0.20'    -> guard passes: True
edit.py says 'target = floor + 0.25'    -> guard passes: True    <-- a 25% drift, silent
edit.py says 'target = floor + 0.2999'  -> guard passes: True    <-- a 50% drift, silent
edit.py says 'target = floor + 0.30'    -> guard passes: False
```

The one number the gate takes from the renderer's *source* could move by half and the guard
stayed green. **It now reads the constant out of edit.py's AST and compares numerically**, and
a second test asserts the reader returns the number rather than a matching string — because a
guard nobody has watched fail is a guard nobody has tested. The third time in this repo a text
scan has been mistaken for a parse.

`tests/test_clip_pipeline_entrypoint.py` — **32 checks, green.**

---

## 2. THE ADMIT-THEN-REFUSE COUNT — nobody had measured it, and it is **zero**

Unattended, `n=20`, real library, real ranker, no explicit song.

| | |
|---|---:|
| library | 2,003 clips |
| admitted by the derived floor | **1,594** |
| clips the **old 5.0s floor** would have admitted that can never render | **163** (9.3%) |
| candidates handed to the run (`n × 3`) | 60, **60 servable**, declared 8.3–88.5s |
| **refused by the renderer for DURATION** | **0 of 22** |
| refused for anything else | 2 |

**The two refusals are not the mismatch.** Both are `no audio class supplied, so the treatment
cannot be routed` — MEMEBOT-066's deliberate refusal in `duck.py` — at declared **56.10s** and
**85.05s**, seven and ten times the floor. Reporting them as the cost of the gate/floor
disagreement would have been the easy wrong answer; the number the brief asked for is **0**.

### The residual the gate cannot see, measured rather than assumed

The gate reads the library's **declared** duration; the renderer probes the **staged file**.
Across the 166 records carrying both:

```
staged - declared :  min -0.099s   median 0.000s   max 0.000s
```

One-sided, and the derived floor has **zero headroom** for it by construction — `MIN_DURATION_S`
is exactly the renderer's requirement. So a clip declared in **[7.626, 7.725)** is admitted and
then refused. **Two of the 1,588 admitted clips are in that band (0.13%)**; 23 sit within 0.5s
of the floor.

**Left as a reported residual, not patched.** A second margin in the gate would be a second
threshold for one decision — the shape this repo has been unpicking for four rounds — and a
0.099s bound taken from one source type is exactly the sort of number that ages badly. It is
0.13% of admissions and it is now on the record with its population.

---

## 3. ROTATION AT SCALE — nothing is starved by rotation

This run drew **9 distinct windows**. Cumulatively, across every real render on the ledger:

| song | mood | windows | uses | spread |
|---|---|---|---|---:|
| `sng_0004` | hype | h1–h5 | **7 / 7 / 7 / 6 / 6** (33 renders) | **max−min = 1** |
| `sng_0003` | warm | h1–h5 | 1 / 1 / 1 / 1 / 2 (6) | 1 |
| `sng_0001` | melancholy | h1–h5 | 2 / 0 / 0 / 0 / 0 | — |
| `sng_0002` | triumphant | h1–h6 | 0 / 0 / 0 / 0 / 0 / 0 | — |

**Every window of every song the library can actually reach has been played, and the spread
inside a song is at most one.** Thirty-three renders over five windows landing 7/7/7/6/6 is
what a working least-used rotation looks like.

**The 10 windows never played are a SUPPLY problem, not a rotation problem:**

```
whole library, 2,003 clips:   PARKED 1,717   hype 249   warm 34   melancholy 3   triumphant 0
top 60 candidates:            hype 51        warm 7     melancholy 2
```

**Not one clip in 2,003 matches `triumphant`,** so `sng_0002`'s six hand-marked windows cannot
be drawn by anything in the library — the song exists, the clips do not. `melancholy` has three
matching clips in total. Rotation spreads **windows**; it cannot spread **songs that no clip
selects**. 16 of this run's 20 renders drew `sng_0004`, and that is the library speaking, not
the rotation.

**What the operator should see:** 10 of 21 hand-marked windows are unreachable today, and no
code change reaches them. Two more `hype` tracks would put 87% of matches behind three songs
instead of one; a `triumphant` window needs `triumphant` clips, not a `triumphant` song.

---

## 4. EVERY OUTPUT VERIFIED BY MEASUREMENT — 20 of 20 on all four checks

| check | result |
|---|---:|
| file exists, ffprobe reads it | **20 / 20** |
| has an audio stream | **20 / 20** |
| clears edit.py's 8.0s floor | **20 / 20** |
| **carries the CONFIGURED track** (40–250 Hz band-limited signed correlation, every other store track as the null) | **20 / 20** |
| join key resolves in the store | **20 / 20** |
| record says `joinable` | **20 / 20** |

```
r      min/median/max : 0.2515 / 0.9052 / 0.9968
margin min/median/max : 0.109  / 0.5718 / 0.8448      (bar: r >= 0.25 AND margin >= 0.10)
```

Correlation is MEMEBOT-066's method, **imported, not re-implemented** — its thresholds only
mean something if the code behind them is the same code.

### The nine "missing" tracks were my verifier, not the renderer

The first pass returned **11 of 20**, and every failure was a **long** video. The cause was
mine: I correlated against the **marked hook** while `fit_window` WIDENS the audio window to
cover the clip — on a 60s video the bed edit.py actually laid down is `46.6–107.5s` where the
marked hook is `46.6–67.0s`. I was correlating against a segment that was never played.

Against the **applied** window: **20 of 20**, and the same nine files score r = 0.25 → 0.97.
Had I published the first pass it would have read as nine videos silently missing their song.
The record carries both fields for exactly this reason — `start_sec`/`end_sec` is the marked
hook (the join key, what rotation and the bias map group on) and `applied_*` is what was
rendered.

---

## 5. THE ROTATION DESIGN NOTE, CARRIED

> **The counter is DERIVED from the ledger, never persisted to the store.**
> `count=True` + `save()` moves it at PLAN time, which is BL-888's defect: `render_plan()`
> defaulted to counting, the dashboard polls it every 5 seconds, and rotation advanced
> ~1,440 times a day against clips nobody rendered. A ledger record exists only for a render
> that really happened, so a poll cannot advance rotation **by construction** — there is no
> flag for a future caller to get wrong — and `scratch/songs.json` is never written at run
> time. It counts **distinct records** (`record_id_for` keys on the output path; one render
> writes both a `pending` and an `ok` line) and only `status: ok`.

If a future round "improves" this into a persisted counter, the 7/7/7/6/6 above is what it
must still produce, and BL-888 is what it will reintroduce.

---

## PROOF

| Required | Result |
|---|---|
| the gate derived from edit.py | **already true** — BL-958, `b45d66a` 12:54:41; `(8.0 + 0.20) × 0.93 = 7.626`. MEMEBOT-072 said otherwise and is corrected in place |
| a drift test that READS edit.py's numbers | the margin check was a **prefix match** that passed on 0.25 and 0.2999; now an **AST read** compared numerically, plus a test that the reader catches a drift. 32/32 |
| admit-then-refuse at n≥15 | **0 of 22 for duration.** 2 refused for a missing `audio_class` at 56.1s and 85.1s — a different defect. 163 clips (9.3%) correctly excluded by the derived floor |
| the residual | **2 of 1,588 (0.13%)** in `[7.626, 7.725)`, where a measured one-sided declared-vs-staged shortfall (max −0.099s over 166 records) can push a clip under. Reported, not patched |
| window distribution over 20 renders | 9 this run; cumulative **7/7/7/6/6** on hype, spread ≤ 1 on every reachable song. **Nothing starved by rotation**; 10 unreachable windows are 0 `triumphant` and 3 `melancholy` clips in 2,003 |
| every output verified by measurement | **20/20 on all four**, r median 0.905, margin median 0.572, min margin 0.109 |
| suites | **135 of 138 green, 4,790 checks** (1,580s, 13 rounds in flight). `test_clip_pipeline_entrypoint.py` **32/32**, `test_hook_rotation.py` 17/17. All three reds attributed below; **none is in a file this round touched** |
| campaigns | `8e02f8d6f6307ae8` (sort_keys) **and** `7a029ee5447cddd8` (compact) — both **MATCH** |
| config.json | parses, **161 keys, 5 campaigns** |
| budget | $0.05 allowed; ledger delta **$0.0114** |

---

## Method / limits

**The three red suites, attributed rather than waved at.** Two of them REPRODUCE standalone,
so calling them flakes would have been wrong:

| red | verdict |
|---|---|
| `test_no_unchecked_stdout.py` | **9/9 standalone** — a load flake in a 1,580s run with 13 rounds in flight |
| `test_claims_manifest.py` | fails on `docs/claims/MEMEBOT-075.claims`, another round's **in-flight manifest**. Reproduces; not mine, and not a flake |
| `test_matcher_boundary.py` | `dict_of()` drops `vision_control_declined`, which `song_library` now reads. That read exists **only in the uncommitted worktree** — `git show HEAD:clippershq/song_library.py` has zero occurrences. An in-flight round added a field read without the `dict_of` passthrough; the boundary test caught it exactly as designed, on someone else's change |

Running a full suite against a worktree that thirteen rounds are writing means some reds are
other people's in-flight state. The distinction that matters is whether the red **reproduces**
and whether it is **in a file you touched** — these are checked, and neither of the two real
ones is mine.

**The 2 failed renders are a live defect in someone else's file.** `no audio class supplied,
so the treatment cannot be routed` is MEMEBOT-066's refusal in `memebot/scraper/duck.py`,
firing on clips whose library record carries no `audio_class`. It is a correct refusal — BL-950
is what guessing costs — but 2 of 22 candidates reaching the renderer without a class is a gap
upstream of it, in the labeller. Not my file, not my round; reported with both clip ids in
`scratch/mb073_scale.json`.

**The correlation null is per SONG, not per window.** Four songs, so four reference contours.
Two windows of the same track share a track, and the honest failure mode this cannot separate
is two different tracks with the same loudness contour — `margin` is on every row so that case
is visible rather than hidden in a boolean.

**The declared-vs-staged bound is 166 records of one source type.** Instagram progressive MP4s
on this machine. It is a measurement, not a constant, and it should not be turned into one
without a wider sample — which is the main reason the residual is reported rather than patched.

**`hook_uses_from_ledger` counts every round's renders, not just mine.** That is correct — the
ledger is the shared record of what was played — but it means the cumulative 7/7/7/6/6 includes
renders from MEMEBOT-066, -067, -071 and -072.
