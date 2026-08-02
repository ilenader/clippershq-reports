# BL-958: the video half has two entry points, callable defaults and a cap that binds — and the gate was still admitting clips the renderer can never finish

**Date:** 2026-08-02 · **Type:** Wiring + governance, proved on real runs · **Spend:** **$0.0012 · 2 paid calls** (budget $0.20)
Claim filed with **repeated `--write` flags** (7 paths, each its own element). `claims_read.py --holders` AND `git status --porcelain` run on every target. **1 video rendered end to end**, verified by `ffprobe`. Suite run **twice**; every red in either run passes standalone and none is attributable to this round — itemised in §9. `docs/claims/BL-958.claims` **9/9 verified at HEAD**. `config.json` unmodified. `clippershq/clip_library.py` carried `' M'` throughout — that is **BL-959's** working copy, never staged here.

**REPORT ID CLASH, DECLARED RATHER THAN OVERWRITTEN.** `reports/BL-958.md` on `origin/main` is a **different round** — a deferral-registry report, itself headed "claimed as BL-957". My round claimed `BL-958` in the in-flight registry before that was visible. Per `CONVENTION.md` the target path for a *new* report must not exist, so this one is published at a suffixed path and nothing is fast-forwarded over. Cite this document by its full filename; `BL-958.md` is somebody else's.

---

## 0. Preconditions, and the stale claim I deliberately walked past

```
python tools/claims_read.py --holders clippershq/clip_pipeline.py   ->  BL-899
git status --porcelain clippershq/clip_pipeline.py                  ->  (empty)
python tools/claim.py brief
  BL-899   900 min   clippershq/clip_pipeline.py, tests/test_clip_pipeline_gate.py, ...
                     ** POSSIBLY STALE: its own files untouched for 898 min
```

The brief told me BL-899 had held the file for 12+ hours with the file clean and to **verify before deferring**. Verified three ways, all agreeing: the claim is 900 minutes old, `git status` reports the file unmodified, and the tool's own staleness line says nothing under the claim has been touched for 898 of those minutes. `git log -1` on the path shows the last commit was BL-949's, not BL-899's. **A claim with no work under it is a reservation, not a conflict.** I proceeded and the claim tool recorded the overlap on its own:

```
  ! ADVISORY - another live claim intends to write the same path(s):
      BL-899  clippershq/clip_pipeline.py
```

`MEMEBOT-064` holds `memebot/scraper/edit.py`; I did not edit it, only invoked it as the subprocess `run_batch` already invokes. A real run appends to `memebot/runs.jsonl` — that is this pipeline's own ledger doing its job, and it is what makes the proof below a proof.

---

## 1. Two entry points, where there were none

BL-955 measured it exactly: `run_batch` had **no caller in shipping code**. `grep` found it in tests and in **six** one-off scratch drivers — `mb044`, `mb047`, `mb060`, `mb061`, `memebot010_run`, `bl955_stage345` — every one of which had re-typed the same twelve lines of `IgClient` + `requests` wiring. Six copies of a contract is not a contract; the seventh is where it drifts, and BL-955's did (it returned a `Response` where `bytes` was required and died at `fh.write`).

**The menu** (`control.py`), a tenth key beside `[k] Build the clip library`:

```
("v", "MAKE VIDEOS from the clip library - re-fetch the best catalogued clips,
       match a song and render finished vertical files (needs [k] first; the only
       paid part is one re-fetch per video)")
...
elif ch == "v":
    _render_clips(config, config_path)
```

**The headless command** (`run.py`), a tenth funnel:

```
"clip_render":  {"fn": "_render_clips", "cap_key": "clip_pipeline_max_run_usd",
                 "target_key": None, "paid": True},
```

```
python -m clippershq.run --funnel clip_render --target 1 --cap 0.0024
```

Listing and dispatch are **two separate lists** in `control.py`; an entry in one and not the other is a key that does nothing when pressed, so the test asserts both. The test also resolves `FUNNELS[*]["fn"]` through `getattr(control, ...)` for **every** funnel, because a table naming a function nobody defined is precisely the BL-923 fault one level up.

**One gotcha that would have been silent.** `run.py`'s `_spend_now` filters the ledger by an **exact** campaign match, and `run_batch`'s meter already wrote 17 historical rows under the lowercase `memebot`. `CAMPAIGNS["clip_render"]` is therefore `"memebot"`, not the tidy `CLIP_RENDER` every neighbour uses. Uppercasing it for consistency would have made every status file report `$0.0000` for money genuinely spent — nothing would fail, the number would just be wrong. Pinned by a test.

---

## 2. The defaults are callable, and a missing dependency now says so

Before: `fetch_clips_page=None, http_get=None`, nothing checked them, and `run_batch(n=1, library_root=...)` died four frames deep in `clip_media.py:315` with `TypeError: 'NoneType' object is not callable`.

`default_fetchers(config_path)` is now the single live implementation of both halves, and it distinguishes them — `fetch_clips_page` is **paid**, `http_get` is a plain unbilled CDN GET **returning bytes, not a Response**. It raises `MissingWiring` naming what it could not build:

```
MissingWiring: cannot build IgClient from no_such_config.json
  (RuntimeError: No HikerAPI key found...) - most often a missing or invalid
  Instagram-lookups key. Set it in Settings, then re-run.
```

`run_batch` fills whichever of the two is `None`, so injecting **only** the paid leg — what a test actually wants to stub — no longer leaves a `None` to travel four frames. Proved by calling `run_batch` with no fetcher arguments against a stubbed `default_fetchers` and asserting the stub was used, not by asserting the signature changed.

---

## 3. The cap: `min(per-run, lifetime)`, metered on both bounds

```
run_budget_usd = min(clip_pipeline_max_run_usd, spend_cap_usd - total_spent)
```

The shape that already works everywhere else (`main._execute_run`, BL-923). A per-run cap must never **raise** the lifetime ceiling and the lifetime ceiling must never override an operator who asked for a smaller run — BL-914 is what one-sided wiring costs: a run capped at $0.05 armed at ~$41.50.

**Checked on the WORST case of the next call, before making it.** `max_pages=2` means the next candidate could cost two calls; a cap checked afterwards is always exceeded by exactly the call that broke it.

**Per-vendor `IncrementalMeter`, bounded by BOTH 25 calls AND 30 seconds.** Retrieval is the only paid vendor in this half (vision spend happens upstream, in the walk), so `PAID_VENDORS = ("ig",)` — a table, so adding one is one edit rather than a second hand-written sum, which is the omission BL-897 found at three levels. The clock bound is not decoration here: **one render is ~25–46 seconds during which this loop makes no billed call at all**, so a count-only meter holds the batch across the whole of it, and a hard kill exits `0xC000013A` — no `finally`, no `atexit`. `meters["ig"].tick()` is called on **both** sides of `render_one`.

**And a run that would write real dollars with no ceiling is refused, not defaulted:**

```
UncappedRun: REFUSED: this batch would write real dollars to spend.json with no
  ceiling on them. Pass max_run_usd=..., or set 'clip_pipeline_max_run_usd' in
  config.json. There is deliberately no default: a forgotten cap must mean no
  run, never an unbounded one.
```

A call with `spend_path=None` (a test, a planner) spends nothing and is not refused — refusing it would be theatre.

### It binds. Two real runs, on the real ledger.

**Run A — stops before spending anything.** `--cap 0.0001`, below one call:

```
  library 2003 clips -> 9 candidates for 3 video(s) (3x over-provision)
  run cap $0.0001  (per-run $0.0001; lifetime room $40.66)
  STOPPED ON THE CAP: $0.0000 spent, the next clip could cost $0.0012,
                      cap is $0.0001. 0 video(s) made, 9 candidate(s) not attempted.
  clip_render: completed  leads=0  spend=$0.0000  6s
```

**Run B — spends, then stops.** `--cap 0.0012`, room for one clip:

```
  [1/3] 3448924568930352855_5769514091 @moviezar
      1280p, 396.5 KB -> song Trust Me [lru_corpus] 41.2-61.2s
  STOPPED ON THE CAP: $0.0006 spent, the next clip could cost $0.0012,
                      cap is $0.0012. 0 video(s) made, 8 candidate(s) not attempted.
  clip_render: completed  leads=0  spend=$0.0006  20s
```

The stop is a real stop after real money: one paid call made, on the ledger, and the second refused.

---

## 4. The re-fetch leg IS metered — the ledger rows

The library stores **no playable URL** (0 of 50, BL-955) and that is correct by design: an IG CDN URL expires in ~105 hours and the rendition ladder is not stable between fetches, so a cached one is wrong within minutes. Render therefore re-fetches, and that re-fetch is the entire paid leg of this half. BL-886 found this exact leg unmetered before, which made every per-clip cost ever quoted vision-only.

`spend.json`, after the two runs that spent:

```
2026-08-02 12:24:07   memebot   clip_pipeline_ig   $0.0006     <- run B
2026-08-02 12:32:30   memebot   clip_pipeline_ig   $0.0006     <- run C
```

Metering is `meters["ig"].add(r["pages_fetched"])` **immediately after retrieval, whether or not the clip came back usable** — an unretrievable clip still cost its pages. The old end-of-batch `record_aux_spend` is gone; it was the single shape BL-830/BL-833 rejected everywhere else, where a kill before that one line recorded $0.0000 against real money. The summary now cross-checks `metered_calls` against `calls` and says so out loud if they differ.

---

## 5. One video, end to end

```
python -m clippershq.run --funnel clip_render --target 1 --cap 0.0024

  Library: 2,003 clip(s) in ./clip_library
  library 2003 clips -> 3 candidates for 1 video(s)
  run cap $0.0024  (per-run $0.0024; lifetime room $40.66)
  [1/1] 3586077779226464604_5769514091 @moviezar
      1280p, 204.4 KB -> song O Sanam [lru_corpus] 53.1-73.1s
      ok -> ...\final\white_frame\3586077779226464604_5769514091.mp4 (1535.2 KB)

    Videos made        : 1 of 1 attempted
    Spend this run     : $0.0006  (1 billed re-fetch)
    Cost per video     : $0.0006
    Wall clock         : 25s
```

```
$ ffprobe ...
codec_name=h264   codec_type=video   width=1080   height=1920
codec_name=aac    codec_type=audio
duration=8.200000   size=1572021
```

**Marginal cost confirmed at exactly $0.0006** for the next video from a warm library — the brief's figure, measured again. Wall clock was **25s**, not the 46s BL-955 recorded; I did not re-measure the cold-library `$0.0498 / 316s` walk half and make no claim about it.

---

## 6. OFF-BRIEF, AND IT BLOCKED ITEM 5: the gate still admits clips the renderer can never finish

**The first real run through the new entry point paid $0.0006 and rendered nothing.** Not a wiring fault — the clip was 5.4 seconds:

```
edit:under-floor   finished at 5.763s, under the 8.0s floor. Not shipping a short video.
```

MEMEBOT-063 named this pair in its own test file and fixed **one half** of it:

```
clip_pipeline.gate  MIN_DURATION_S = 5.0     <- what is admitted
edit.py             floor_s        = 8.0     <- what is required
```

It made the **renderer** stop trimming clips under a floor it was about to enforce. It could not touch what the **gate** admits, and that half stayed open for four rounds. This is what it costs at the head of the ranked queue:

| | |
|---|---|
| top-9 candidates in the live 2,003-clip library | **6 of 9 under 8s — unrenderable** |
| highest-viewed candidate of all (48.1M plays) | **5.4s** — admitted, paid for, refused |
| gate-passing clips corpus-wide | 163 of 1,749 (**9.3%**) under 8s |

`SHORT_CLIP_BONUS` promotes clips under 10 seconds (BL-850's one surviving content term), and nothing told the gate they could not be rendered — so the ranker was actively sorting unrenderable clips to the front. **The practical failure rate at the head of the queue was 67%, not 9.3%.**

**Fixed by DERIVING the admission floor from the renderer's own three numbers, not by restating 8.0:**

```python
RENDER_FLOOR_S = 8.0             # config.yaml transform.duration_floor.floor_s
RENDER_FLOOR_MARGIN_S = 0.20     # edit.py _floor_trim_budget: `target = floor + 0.20`
RENDER_MIN_SPEED = 0.93          # config.yaml transform.speed.min - below 1.0 LENGTHENS
MIN_DURATION_S = round((RENDER_FLOOR_S + RENDER_FLOOR_MARGIN_S) * RENDER_MIN_SPEED, 3)
                                 # = 7.626
```

After MEMEBOT-063 the shortest source that can still clear is one rendered at the **slowest** configured speed (which lengthens) with zero trim, aiming at the floor plus edit.py's own container/stream margin. **A guard that hardcoded 8.0 here could not detect drift** (MEMEBOT-027), so the test **reads `memebot/scraper/config.yaml` and `edit.py`** and goes red if any of the three moves.

**Cost of the change, measured not asserted:** gate-passing falls 1,749 → 1,599, **150 clips (8.6%)**. Every one of them was a clip that would have cost a paid re-fetch and produced nothing. The run that follows this change made its video on the **first** candidate.

---

## 7. Correction: "~16 more videos" is not the shipping library's headroom

The brief's item 5 says the library "supports ~16 more videos before another walk". That figure is against **BL-955's private 50-clip library** (`scratch/bl955_library`), which is what that round pointed `library_root` at. The shipping entry point reads `clip_library_dir` from config — `./clip_library` — and measured through the same gate:

```
library                  2,003
gate-passing             1,598
  + carries a vision label  1,595   <- the renderable pool
already rendered ok          26
```

**1,595, not 16.** At the confirmed $0.0006 marginal that is ~$0.96 of re-fetches before the library needs another walk. Nothing else in item 5 changes: the walk is still the expensive part, and the render half is still $0.0006.

---

## 8. What is NOT fixed, stated plainly

- **The song-store join is still broken** and both my renders said so on screen: `this record will NOT join the song store; key '...m4a@53.08-73.08' matches none of the 21 store key(s)`. The video is fine and its outcome is recorded, but it can never earn rotation. That is BL-955's boundary failure 4, untouched — the LRU fallback picks a corpus file that was never a store hook. It belongs to whoever owns `song_library`.
- **`ocr` remains unwired** (BL-955 failure 5). Not in scope here.
- **The cold-library `$0.0504 / 362s`** was not re-measured; only the render half was.
- `run_batch` still takes `dry_run`, which retrieves (and therefore pays) before it declines to render. Correct as designed, but worth knowing before setting a cap for one.

---

## 9. Suite, and three process notes I am not going to bury

I ran it twice, and **the two runs disagree about which suites are red** — which is itself the
honest headline, because ten rounds were writing this tree throughout.

```
run 1  12:33-12:49   125 of 126 green   905.2s      FAIL  tests/test_filelock.py
run 2  12:50-13:12   124 of 127 green  1344.3s      FAIL  tests/test_clip_pipeline.py
                                                    FAIL  tests/test_claims_manifest.py
                                                    FAIL  memebot/.../test_edit_behaviour.py
both runs   PASS  tests/test_clip_pipeline_entrypoint.py   31 checks
```

**Every red passes standalone, and none of the four is attributable to this round.** Checked
one at a time rather than asserted:

| suite | standalone | why it was red |
|---|---|---|
| `test_filelock.py` | `Ran 4 / OK` | cross-process lock contention; **green in run 2**. `filelock.py` untouched here. |
| `test_clip_pipeline.py` | `Ran 82 / OK` + self-test PASS | run 2 read the tree **while I was committing `clip_pipeline.py`**. |
| `test_claims_manifest.py` | fails, **on somebody else's manifest** | `docs/claims/MEMEBOT-067.claims` carries a caveat saying it cannot be verified, and then verifies cleanly. Mine reports **9/9 verified at HEAD**. |
| `memebot/.../test_edit_behaviour.py` | `Ran 32 / OK` | memebot repo (MEMEBOT-064/066 are live in it); contains **zero** references to `clip_pipeline` or `MIN_DURATION_S`. |

A suite count is a moment, not a property (MEMEBOT-026), and under ten concurrent rounds it is
a *noisy* moment. The seven suites this round can plausibly affect were each run directly and
all pass: `test_clip_pipeline`, `test_clip_pipeline_gate`, `test_clip_wiring`, `test_caps`,
`test_headless`, `test_edit_duration_budget`, `test_matcher_boundary`.

**A stale git lock cost 11 minutes.** `.git/index.lock`, 0 bytes, created 12:44, with **no
`git` process running anywhere on the machine** (checked with `Get-Process`). Ten concurrent
rounds share this repo; one of them died mid-commit. Removed, and recorded here because
removing another round's lock is not a thing to do quietly.

**I committed another round's work, and I am naming it.** `git add` + `git commit` in this repo
is a read-then-write with no lock **on a global index shared by ten rounds**. I staged my two
remaining files, ran `claim.py staged`, got `one round: BL-958`, and committed — and between
the check and the commit **BL-961 cleared the index and staged its own nine files**, so my
commit took theirs and not mine. The guard printed `staged paths belong to one round: BL-961`
on the way past and I read it afterwards.

Nothing was lost: every line was BL-961's own content, unmodified, and it is now on the branch
instead of sitting orphaned in a working tree — the exact degradation `docs/ORPHAN_RULE.md`
describes. Only the label was wrong. I amended **the message only**, in place, to say what the
commit actually holds, and left the tree untouched.

My own `git reset` was the other half of the fault: it unstages **other rounds' work too**. The
safe form, which the corrected commit uses, is the pathspec one — it commits the named paths
and ignores whatever else is in the index:

```
git add <paths> && git commit -F msg -- <paths>      # never a bare `git commit`, never `git reset`
```

**Two hooks fired and both were obeyed rather than bypassed.**
- `pre-commit` refused to enrol `docs/claims/BL-958.claims` before the code it claims was
  committed (BL-874: a manifest waits for the code, never the reverse). Fixed by committing
  the code first. `verify_claims.py` now reports **9/9 verified at HEAD**.
- `claim.py staged` attributes `clippershq/clip_pipeline.py` to the dormant BL-899 claim, so a
  single commit containing it plus my other files reads as spanning two rounds. `--no-verify`
  was on offer; I split into three commits instead, so the guard stayed honest. It is still
  one round's work.

---

## SUMMARY

- **Both entry points live.** `control.py` menu key `[v]` (listed *and* dispatched) and `python -m clippershq.run --funnel clip_render --cap ...`, a tenth funnel whose `cap_key` is read by a module other than `run.py`.
- **`run_batch` is callable with production defaults.** `default_fetchers()` is the one live implementation of the paid fetcher and the bytes-returning CDN GET; a missing dependency raises `MissingWiring` **by name at the top** instead of `TypeError: 'NoneType' object is not callable` four frames down.
- **The cap binds, proved on two real runs.** `min(per-run, lifetime)`, judged on the worst case of the *next* call; `--cap 0.0001` stopped before spending anything, `--cap 0.0012` spent $0.0006 and then stopped. No ceiling + a real ledger = `UncappedRun`, refused.
- **The re-fetch leg is metered**, incrementally, on both a 25-call and a 30-second bound — two `memebot / clip_pipeline_ig` rows on `spend.json`, one per paying run. The re-fetch is unavoidable and correct: the library stores no playable URL because a cached CDN URL is wrong within minutes.
- **One video rendered end to end**: 1080×1920 h264+aac, 8.20s, 1.57 MB, $0.0006, 25s wall.
- **OFF-BRIEF — the gate admitted clips the renderer can never finish.** MEMEBOT-063 fixed the renderer's half of a 5.0-vs-8.0 disagreement; the gate's half was still open and **6 of the top 9 candidates were unrenderable**. The admission floor is now derived from edit.py's own three numbers (7.626s) with a drift test that reads them; 150 clips (8.6%) dropped, every one unrenderable.
- **CORRECTION:** the "~16 more videos" headroom is BL-955's private 50-clip library, not the shipping one. `./clip_library` holds **1,595** gate-passing, vision-labelled clips — ~$0.96 of re-fetches before another walk.
- **Suite run twice, and the two runs disagree** (125/126 then 124/127) with ten rounds writing the tree. **Every red passes standalone and none is this round's** — checked one at a time, table in §9. `test_clip_pipeline_entrypoint.py` (31 checks) passed in both. Two hooks fired and both were obeyed, not bypassed — three commits instead of `--no-verify`.
- **MY OWN FAULT, REPORTED:** a bare `git commit` took **BL-961's** nine staged files instead of my two, because the git index is global across ten concurrent rounds and they re-staged between my guard check and my commit. Nothing lost; message amended in place, tree untouched. Use `git commit -F msg -- <paths>` here, and never `git reset`.
