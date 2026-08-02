# BL-955: the chain produces a video, and the two halves are not connected to each other

**Date:** 2026-08-02 · **Type:** End-to-end smoke test · **Budget:** $0.50 · **Spent: $0.0624**

Honesty tiers: **VERIFIED** (run here), **BOUNDARY** (what one stage hands the next), **CORRECTION** (mine).

> **Published as `BL-955-full-chain-smoke-test.md`.** `reports/BL-955.md` already existed on origin — another round took the number while this one ran. `publish_report.py`'s collision check refused the push and I suffixed the path per `CONVENTION.md`: suffix the filename, keep your own ticket number, never renumber someone else's. Second time this gate has fired for me, both times correctly.

---

## The headline

**A finished video exists** — 1080×1920 h264+aac, 52.8 s, 24.1 MB, produced from a cold library. **And no shipping code path can produce one.** `clip_pipeline.run_batch` — retrieve → vision → song → render — has **no caller anywhere outside tests**, and neither `run.py` nor `control.py` mentions `clip_pipeline` at all. I had to wire the live fetcher by hand, in a scratch file, to make the back half run.

The brief said "every stage has been proven in isolation; nothing has run the whole chain". That is exactly right, and the reason is structural: **the front half (discovery, walk) and the back half (retrieve, render) have no connection in shipping code.**

---

## 0. Preconditions, and why this run wrote to a private library

Nine claims live. **Three rounds are inside the clip library right now** — BL-946 holds `clip_library/` *and* `clip_vision.py`, BL-947 holds `clip_library.py`, BL-951 the label scripts. Item 5 exists because four concurrent appenders collided 236 clips earlier; running a walk into the shared library would have made me the fourth.

So every clip write this round made went to **`scratch/bl955_library`** via `config.clip_library_dir`. I **executed** modules held by others (`clip_pipeline` → BL-899, `clip_vision` → BL-946, `edit.py` → MEMEBOT-063) and **edited none of them**. `config.json` and `spend.json` were backed up first; metering went to the **real** ledger because the money is real.

---

## 1. The run, stage by stage

| # | stage | wall | cost | result |
|---|---|---|---|---|
| 1 | repost discovery | **902 s — KILLED** | $0.0018 | timed out at my 900 s limit, 5 pages / 147 clips, target 3 **not reached** |
| 2 | clip walk | 335 s | $0.0498 | **50 clips, 50 accounts, 10 shards** ✓ |
| 3–5 | retrieve → vision → song → render | 47 s | $0.0006 | **1 video, `made: 1`** ✓ |
| — | cap-binding test | 44 s | $0.0102 | **cap bound and stopped the run** ✓ |

**Total wall clock 10:16:59 → 10:45:22 = 28 m 23 s. Total spend $0.0624 of $0.50.**

**Stage 1 never finished.** Repost discovery ran 15 minutes against a target of **3** and was still walking pages when the timeout killed it. Its paid calls are rare by design (`~$0.00 … only when a free contact isn't found`), so the time is spent on free frame analysis — but an unattended daily run needs to know that "target 3" does not mean "a few minutes".

---

## 2. BOUNDARY FAILURES — what each stage hands the next

### (a) The two halves are not connected at all

```
callers of run_batch outside tests : NONE
clip_pipeline referenced in run.py : NO
clip_pipeline referenced in control.py : NO
```

`run.py` exposes nine funnels; only `repost` and `clip_walk` are on this chain. Everything after the library — retrieve, vision, song, render — is `clip_pipeline.run_batch`, which has **no CLI and no production caller**. It is a library that only tests invoke.

### (b) `run_batch` with its own defaults crashes opaquely

The natural unattended call is `run_batch(n=1, library_root=...)`. Its defaults are `fetch_clips_page=None, http_get=None`, and nothing checks them:

```
TypeError: 'NoneType' object is not callable
  clip_media.py:315   env = fetch_clips_page(uid, token)
```

An operator gets a `NoneType` error four frames deep in a module they did not call, rather than *"no clip fetcher supplied"*.

### (c) The library stores no playable URL — by design, and undocumented at the boundary

```
playable url (render needs)      0 / 50
```

Verified twice: no `video_url`/`play_url`/`download_url` field exists, and `media_renditions` — present on all 50 — carries `bandwidth`, `codecs`, `height`, `id` and **no URL**. So render must **re-fetch the manifest from Instagram** for every clip. That is a deliberate choice (`clip_media.retrieve`'s docstring explains there is no fetch-one-media-by-pk endpoint), but it means **the library alone is not sufficient input to the renderer**, and nothing at the boundary says so.

### (d) The finished video cannot join the song store

The pipeline reported this itself, and it is the sharpest hand-off failure of the run:

```
!! this record will NOT join the song store: song is not in the store at all;
   key 'scratch/bl691_audio/1975396383375922.m4a@15.64-35.64' matches none of
   the 21 store key(s). The video is fine -- its outcome is recorded but can
   never earn rotation.
```

The video rendered correctly with a real song (`Let Him Cook`). Its **outcome record is keyed by a path+window string that no store key matches**, so the rotation system can never learn from it. Every video this pipeline makes is, for rotation purposes, invisible.

### (e) `ocr` is UNWIRED, and the estimator bills for it anyway

The pre-run estimate budgeted the single largest CPU line:

```
ocr               18 clips    281.4 s
```

The run reported:

```
ocr            UNWIRED  (no counter site and no parameter; ocr_features() only scores layout)
```

The estimator quotes a stage that does not execute. It is honest **in the summary** and wrong **in the estimate** — and the estimate is what an operator reads before saying yes.

### (f) Cost estimate was 4.6× low

```
ESTIMATED COST : $0.0108
Paid calls     : 107
Spent          : $0.0498
```

Not fatal at these sizes; at a daily 1,000-clip target that is the difference between $0.22 and $1.00.

---

## 3. The true end-to-end cost of one finished video

**From a cold start: $0.0504 and 6 m 2 s.**

| component | cost | time |
|---|---|---|
| clip walk → 50 clips in the library | $0.0498 | 316 s |
| retrieve + vision + song + render → 1 video | $0.0006 | 46 s |
| **one finished video, cold** | **$0.0504** | **362 s** |

**Marginal cost of the next video from that same library: ~$0.0006** — the library is the expensive part and it is reusable. 50 clips yielded 3 render candidates at 3× over-provision, so this library supports roughly **16 more videos at $0.0006 each** before another walk is needed.

**Discovery is excluded from that figure and I am saying so.** Repost discovery is a *lead-generation* funnel — it finds meme pages to contact — and does not feed clips to the renderer. The brief grouped it into "the pipeline"; it is a second chain that shares the ledger, not a stage of this one. Including its killed 902 s would inflate the number with work the video never used.

---

## 4. Caps: one bound, one could not be made to bind, one is unreachable

**VERIFIED binding** — I lowered `clip_finder_max_run_usd` to $0.01 and re-ran the walk into a second private library:

```
Spent          : $0.0102
Library now    : 3 clips, 3 accounts, 2 shards
! STOPPED at your run spending limit.
```

**The cap stopped a live run at 43 s.** Overshoot $0.0002 — one call's granularity, which is the correct behaviour for a counter that checks between calls.

**Not bound, honestly:** neither stage 1 ($0.15 cap, $0.0018 spent) nor stage 2's first run ($0.15 cap, $0.0498 spent) came near its ceiling. A cap that is not reached is not evidence the cap works; only the $0.01 test is.

**Unreachable:** the render stage takes `cost_per_call` but has **no dollar ceiling parameter at all** — `run_batch` has no `max_run_usd`. At $0.0006 per video that is defensible, and it means **the back half of the pipeline is ungoverned**. An operator who loops `run_batch` has no dollar stop.

---

## 5. Locks and row integrity

**In my isolated libraries, nothing was lost.**

```
scratch/bl955_library   lines=50   distinct=50   rev_collisions=0   hidden=0
scratch/bl955_lib_cap   lines=3    distinct=3    rev_collisions=0   hidden=0
12 .lock files present, 0 .tmp orphans
```

Every shard had its lock; no partial writes survived.

**In the shared library, under three concurrent rounds:**

```
clip_library            lines=6503 distinct=2003 rev_collisions=319 hidden=3
```

**The 319 is not the finding, and reporting it as one would be crying wolf** — `clip_library.py`'s own docstring says so explicitly: *"THIS IS THE ACTIONABLE CHECK, AND `rev_collisions` IS NOT"*, because a collision is permanent in an append-only file and the count can never return to zero. The actionable number is **3 clips whose on-disk values `read_all` cannot return**, all three the same fields:

```
vision_attempts, vision_last_error, vision_last_attempt_ts
```

Three clips' vision **retry history** is written and unreadable. Not clip content — but it is exactly the data a labelling round needs to decide whether to retry, and it is invisible to the reader while sitting in the file.

---

## 6. A measurement hazard that would have made this report wrong

A `memebot`/`clip_pipeline` row for **$0.0192 landed in the shared ledger at 10:36:29 — during my walk**, written by another round.

| method | figure |
|---|---|
| ledger delta (rows 220 → end) | **$0.0816** |
| attributed by campaign **and timestamp** | **$0.0624** |

**Differencing the shared ledger overstates this round by 31%.** BL-930 had to correct exactly this class of error in itself, and BL-944 avoided it; a fourth round would have repeated it. In a tree where rounds run concurrently, **a ledger delta is not a cost measurement** — attribution has to be by campaign, and where a campaign is shared (`memebot` held both another round's $0.0192 and my render's $0.0006), by timestamp.

---

## 7. What an operator would have to do to run this daily

**Today, they cannot run it unattended at all.** Concretely:

1. **Write the missing runner.** There is no entry point for the back half. `scratch/bl955_stage345.py` is that runner and it should not live in `scratch/`.
2. **Wire two fetchers by hand.** `ig_client.make_clip_fetch_page()` exists and is exactly the right shape; `http_get` must return **bytes, not a `Response`** — a contract stated only in a docstring and exercised only by a test double, which is why my first live wiring got it wrong (§8).
3. **Budget ~6 minutes and $0.05 per video cold**, ~$0.0006 warm; re-walk when the library's candidates are exhausted (~16 videos per 50-clip walk).
4. **Not run repost discovery on the same schedule** — it did not finish in 15 minutes on a target of 3.

**What to watch, in priority order:**

| watch | why | signal |
|---|---|---|
| the song-store join | every video today is invisible to rotation | `will NOT join the song store` in the render log |
| `hidden_by_collision(clip_library)` | currently **3**; concurrent appenders make it grow | should be 0 |
| estimate vs actual cost | ran 4.6× low | `ESTIMATED COST` vs `Spent` |
| stale `status: running` markers | a killed run leaves one with a dead pid | reconcile **by PID**, not name (INFRA-013) |
| the back half's spend | `run_batch` has no dollar cap | ledger rows labelled `clip_pipeline` |

---

## 8. Corrections — two of mine, caught before publication

**(a) I reported `0/50` for four fields, and three of those zeroes were my harness.** `clip_library.read_all` returns a **dict keyed by clip_id**, not a list. My first probe iterated it directly, got the *keys* (strings), and every field read as absent — including `audio_class`, for which the walk had **just printed a distribution** in its own summary. That is `TESTING.md` rule 5 exactly: *"I cannot see it" must not look like "it is not there".* Corrected: `audio_class` **49/50**, duration **50/50** (as `media_duration_s`). Only `playable url` and `vision label` are real zeroes, and both were then verified a second way.

I caught it by disbelieving my own zero against the run's own output — not because the harness told me.

**(b) My `http_get` returned a `Response` where the contract wants bytes**, dying at `fh.write(res["bytes"])` with *"a bytes-like object is required, not 'Response'"*. My bug. Worth recording anyway: **a contract that has only ever had a test double has never been checked against a real implementation.** `fake_get` returns `b"..."`, so the docstring's `http_get(url) -> bytes` was true and untested for as long as it has existed.

---

## Proofs

| check | result |
|---|---|
| claim filed with **repeated `--write` flags** | ✓ 7 paths, each registered individually |
| writes isolated from the shared library | ✓ `clip_library_dir` → `scratch/bl955_library`; **0 rows** added to `clip_library/` |
| modules held by others executed, **never edited** | ✓ `clip_pipeline` (BL-899), `clip_vision` (BL-946), `edit.py` (MEMEBOT-063) |
| chain run in order with a cap on each | ✓ 4 stages, per-stage ceiling |
| **a finished video** | ✓ 1080×1920 h264+aac, 52.8 s, 24.1 MB, ffprobe-verified |
| every boundary failure named | ✓ **six** (§2 a–f) |
| true end-to-end cost, one video, cold | **$0.0504 / 362 s**; marginal ~$0.0006 |
| a cap **binding on a live run** | ✓ `! STOPPED at your run spending limit.` at $0.0102 |
| meter survives a **hard kill** | ✓ 3 rows / $0.0018 written *during* the killed stage 1 |
| no row lost, locks held | ✓ 50=50 and 3=3 distinct, 0 hidden, 12 locks, 0 `.tmp` orphans |
| cost attributed, not differenced | ✓ $0.0624 mine vs $0.0816 raw delta |
| campaigns | **`7a029ee5447cddd8`** — unchanged |
| config valid | parses, 161 keys; the live `config.json` was **never modified** (a copy was used) |
| suite | **ALL GREEN — 123 of 123, 4,420 checks (365 s)** |
| **spend** | **$0.0624 of $0.50** |

---

## Honest limits

- **Stage 1 did not complete.** I killed it at 900 s. Whether repost discovery *would* have hit its target, and at what cost, is unmeasured — I have a floor (902 s, $0.0018), not a figure.
- **One video, not a sample.** `n=1`. Yield, failure rate and cost variance across many renders are unmeasured; the $0.0504 is one observation.
- **The walk cost is for 50 clips at one moment.** It ran 4.6× its own estimate; I did not investigate why, and it is another round's file.
- **The vision stage did not visibly run.** `vision label 0/50` in the library, and the render succeeded anyway — so either vision ran inside `run_batch` without persisting to my library, or the song match used title/caption text instead. I did not separate the two, and `clip_vision.py` is BL-946's.
- **I did not fix anything.** Six boundary failures reported, none repaired: every file involved belongs to a live round. `scratch/bl955_stage345.py` is a demonstration, not the runner the project needs.
- **The 3 hidden clips are in the shared library and I did not touch them.** Repair means appending a merged row at a higher rev — BL-946's and BL-947's call.
- **`hidden_by_collision` was 3 at one instant** in a library three rounds are actively appending to. Like every count in this tree, it is a moment, not a property.

---

## Say it plainly

The pipeline works. A real video came out of it, from a cold library, for five cents and six minutes — and the parts that were proven in isolation all did their jobs. What does not exist is the wiring between them: no production code calls the renderer, the renderer's own defaults crash, the library does not carry what the renderer needs, and the video it produces cannot be joined back to the store that decides what to make next. Five stages, each correct, connected by nothing.

That is a better position than it sounds, because every gap here is a missing adapter rather than a wrong answer — the fetcher already exists with exactly the right signature, and connecting it took four lines. But nobody should call this pipeline runnable until those four lines live somewhere other than a scratch file, and until a finished video can tell the store it was made.

<!-- CLAIMS
file:   scratch/bl955_stage345.py
file:   scratch/bl955_findings.md
-->
