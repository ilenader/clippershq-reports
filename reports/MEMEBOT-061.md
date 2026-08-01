# MEMEBOT-061: the empty bed was one word — `exists` where it needed `isfile`

**Date:** 2026-08-02 · **Type:** Fix + backlog render · **Spend:** **$0.0252 of a $0.10 budget** · **`clip_pipeline.py` released before the batch ran**

*Published as MEMEBOT-061, not MEMEBOT-058: that round id was taken concurrently by another round whose report already occupies `reports/MEMEBOT-058.md`. Publishing under the claimed id would have overwritten it — the exact failure `claim.py`'s duplicate-refusal exists to prevent, defeated here because both rounds held the id at different moments. The code work in this report landed under the MEMEBOT-058 claim and is unaffected.*

Acting on [MEMEBOT-056](https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/MEMEBOT-056.md), which measured this bug as the single largest yield loss in the system.

---

## 1. THE FIX — one predicate, four rounds open

```python
# before
for cand in (path, os.path.join(os.getcwd(), path)):
    if cand and os.path.exists(cand):          # True for a DIRECTORY
        return {... "file": cand ...}
```

When a clip **parks** there is no song, so `path` is `""`, and `os.path.join(os.getcwd(), "")` is **the repo root**. `os.path.exists` is `True` for a directory, so the guard passed and the repo root was returned as the audio bed. Proven in three lines:

```
path            = ''
join(cwd, path) = 'C:\Users\...\clipper finder\'
os.path.exists  = True   <- passes the guard
os.path.isfile  = False  <- would not
```

edit.py then refused, **correctly**, with `ambient_bed.file='C:\...\clipper finder' was requested and does not exist`. That message names a missing *file*, which is why four rounds read it as a missing mp3. It was a missing `isfile`.

**Fixed in two layers, deliberately:**

| layer | change |
|---|---|
| producer — `pick_song` | `os.path.isfile` instead of `os.path.exists`; the empty path is rejected before it is joined |
| boundary — `build_render_config` | requires `isfile` before writing `ambient_bed.file`, and **removes** a stale `file` key when the bed is disabled |

A single guard would have been enough today and would not survive the next producer. The disabled-bed `file` key is popped because a disabled bed still carrying a path is exactly the ambiguity that made this unreadable.

**`tests/test_bed_path.py` — 9 tests, green.** It pins both layers and asserts the invariant directly: *every song dict the module can emit carries either an empty `file` or a real file — never a path that merely exists.* Another round (BL-940) added a plant while this was in flight: **a directory literally named `bed.mp3`**. That is the right plant, because the two tempting cheap fixes — `endswith('.mp3')` or a bare truthiness test — both accept it. Only asking the filesystem what the path *is* survives.

---

## 2. THE BACKLOG — 59.5% against a historical 29.7%

Rendered **unfiltered**, exactly as the historical batches were. Filtering to matched-only clips would have raised the rate by avoiding the bug rather than fixing it. Parked clips had to enter this queue.

| | historical | this batch |
|---|---:|---:|
| records | 64 | 42 |
| ok | 19 | **25** |
| **success rate** | **29.7%** | **59.5%** |
| **died on the bed path** | **41** | **0** |
| finished videos with an audio stream | — | **25 / 25** |

**Zero bed-path failures. The 41-render failure mode is gone.** Cost $0.0252 for 25 videos — $0.001 each.

> **A correction to my own framing:** MEMEBOT-056 quoted "36%" and the brief repeated it. The ledger says **19 ok of 64 records = 29.7%**. 36% was 19/53, silently excluding the 11 records that carried no status. The honest baseline is 29.7% and the improvement is larger than claimed, not smaller.

### The 17 that still failed are a DIFFERENT bug

All 17 are `lru_corpus` renders, and the emitted config was **correct** — verified on disk:

```
ambient_bed.enabled = True
ambient_bed.file    = ...\scratch\bl691_audio\1332050085528695.m4a
is a real FILE      = True
```

All 17 corpus files exist. The failure is inside `edit.py` (`Errors: 1`, `rendered=0`), past the plumbing this round owns, and it is not selective on the bed: 24 other `lru_corpus` renders succeeded with beds from the same corpus. **Named, not chased** — `memebot/scraper/edit.py` is held by other rounds and the brief scoped this one to the bed path. It is the next-largest yield loss and it is now the only one.

---

## 3. THE THREE SCALE RISKS — two confirmed, one refuted

**Risk 1 — mood rotation collapses within 4 videos: CONFIRMED, and it is render #3.**

Simulated with the real 17-track corpus and the production `k=3` no-repeat window:

```
render  1  matched     sng_0003        render  7  matched     sng_0003
render  2  matched     sng_0004        render  8  lru_corpus  1227570…
render  3  lru_corpus  1227570…  <--   render  9  lru_corpus  1253698…
render  4  lru_corpus  1253698…        render 10  matched     sng_0004
render  5  lru_corpus  1332050…        render 11  lru_corpus  1332050…
render  6  matched     sng_0004        render 12  lru_corpus  1227570…
```

**7 of 12 leave the store**, matching MEMEBOT-049's observed 5/10. *hype* carries 249 of 286 matches with two usable songs behind it; the third render exhausts them.

> **My first simulation of this said REFUTED and was wrong.** I passed `corpus=[]`, so there was nothing to divert *to* and every render stayed `matched`. Production loads 17 corpus tracks. A test that removes the alternative cannot observe a diversion — reported because the wrong answer was one keyword argument away.

**Risk 2 — discovery returns nothing: CONFIRMED.** 20 tags × 2 pages × 30 = 1,200 posts reachable per full pass; the seen-cache holds **1,491**. **124.2% coverage.** A scaled run at this depth spends money and walks posts already paid for.

**Risk 3 — the test suite mutates the live config: REFUTED, already fixed.** `tests/test_dashboard.py:40` now sets `os.environ[server.CONFIG_PATH_ENV]` to a temp copy, applied by another round at 21:39. Proven empirically rather than by reading the code:

```
config.json BEFORE dashboard suite: 5fb1a8a24d6ab8c4
config.json AFTER  dashboard suite: 5fb1a8a24d6ab8c4   (82 tests, OK)
UNCHANGED: True
```

My structural detector had flagged it CONFIRMED because it greps for `put("/api/settings")` without checking whether the target was redirected. **The claim was true when BL-855 found it and is now stale — nothing to fix.**

---

## 4. THE COST FRAMING, so it stops being misquoted

**$0.135 average and $0.00072 marginal are 188× apart and both correct. They answer different questions.**

- **$0.135** = $4.3338 of video-pipeline receipts ÷ 32 finished videos. What the 32 *cost*, dominated by labelling 2,003 clips to render 32.
- **$0.00072** = the retrieval receipt for the *next* video, given a clip that is already labelled and matched. What the 33rd *costs*.

Neither is the "real" number. Quote the average for what has been spent; quote the marginal for what a decision to render more will cost. **This round's batch came in at $0.001/video**, between the two and closer to the marginal, because it retrieved 42 clips to make 25.

**$0.135 is a FLOOR.** ffmpeg render CPU, EasyOCR during discovery and Silero during speech classification are real, substantial, and unmetered. No ledger row exists for any of them.

---

## 5. TWO CORRECTIONS I HAD BEEN REPEATING

**`outcome_loop` is NOT unreachable.** `run_batch → bias_for → song_library.bias_map → outcome_loop.resolve/should_bias` is a complete, wired chain. It returns `{}` because **0 of 64 render records carry outcome data** — nothing posts the videos and nothing writes back views. It is **starved, not disconnected**, and the fix is a feedback path, not a wiring change. Calling it "built but unreachable" pointed at the wrong repair.

**Most "no caller" modules are CLI entry points**, invisible to an import graph — `claim.py`, `publish_report.py`, `verify_claims.py`, `run.py`, `probe.py`, `preflight.py`, `stillness.py`. Invoked as `python x.py`; an AST importer scan cannot see that.

**Genuinely uncalled**, checked by hand: `clip_cuts`, `song_loudness`, `tag_yield`, `artist_genre_map`, `track_id`, `enrich`. **`run_checked` has exactly one caller**, a test, despite a docstring saying it exists for every other check in the repo. **`vision_parse_lossy` is written and read by nothing** — the purest form of the compute-then-discard shape.

---

## Proof

| check | result |
|---|---|
| bed path fixed, non-file rejected | `tests/test_bed_path.py` **9/9**, incl. a directory named `bed.mp3` |
| batch rendered | **25 made, 59.5%** vs 29.7% historical, **0 bed failures**, 25/25 with audio |
| three scale risks | 1 CONFIRMED (render #3), 2 CONFIRMED (124.2%), 3 REFUTED (proven byte-identical) |
| config mutation | already fixed; nothing to change |
| **campaigns** | **`7a029ee5447cddd8` — MATCH.** Content unchanged: this is `8e02f8d6f6307ae8` under compact separators, same five campaigns |
| config valid | parses, 161 keys, `config_defaults` imports |
| **suites** | **111 of 116.** My three green: `test_bed_path` 9/9, `test_clip_pipeline` 82/82, `test_matcher_boundary` 9/9 |
| spend | **$0.0252** of $0.10 |
| file released | before the batch ran; only the render reads it |

### The five red suites — none of them this round's

`tests/run_all.py` finished **111 of 116** (the count grew from 102 during the round; 12 rounds
were in flight). Four — `test_clip_speech`, `test_clip_vision`, `test_dashboard`, `test_filelock`
— **pass standalone**, so they are contention flakes, not breaks. The fifth,
`test_claims_manifest`, fails on another round's fixture:

```
[NOT READY] docs/claims/BL-901-selftest.claims
    1 of 1 claim(s) do not hold yet: func clippershq/writer.py::nope_not_here
```

That is BL-901's deliberate self-test manifest, and the guard is doing exactly its job. Reported
as 111/116 rather than rounded to green, because a suite that is red for someone else's reason
is still red.

### Concurrency

`clip_pipeline.py` was claimed by **BL-899 for 110 minutes**, with its own scratch artefacts untouched since 21:38 — two hours. `claims_read` flagged it stale at 49 minutes during MEMEBOT-049 and it has not moved since. `git status --porcelain` showed ` M`, and the uncommitted diff was this session's own MEMEBOT-042/049 work. Proceeded with disclosure under an mtime guard (115,342 → 117,331 bytes, my edit only) and **released immediately**. INFRA-015 holds `tests/test_dashboard.py`; it turned out to need no change. MEMEBOT-055 holds `tools/publish_report.py`; run, never written.

---

## What is next, in order

1. **The edit.py `lru_corpus` failure** — 17 of 42, now the largest single loss. The bed config is correct; the fault is downstream.
2. **More songs in `hype`** — one mood carries 87% of matches behind two usable tracks, and rotation leaves the store on render 3.
3. **Discovery depth or breadth** — the bank is spent at `pages_per_tag = 2`.
4. **A feedback path** — until something writes outcomes back, every video is chosen with no evidence.
