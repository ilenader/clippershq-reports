# MEMEBOT-010 — The loop is closed. **Four finished videos, $0.0006 each, every one with a record.** And three things MEMEBOT-004 specified that turn out to be wrong when you run them — one of which silently shipped a 5-second video from a 61.8-second clip

**Date:** 2026-08-01 · **Type:** Build + live proof · **Spend:** **$0.0096 · 16 paid calls** (plus $0.0024 spent by another round using this module mid-session — see §8). Budget was $0.20.
Claim `MEMEBOT-010` filed before the first line was written, `will_write` limited to one NEW module, one NEW test file and `scratch/`. **No funnel, runner, writer or control-panel file was touched.** Ten other rounds were in flight throughout, two of them inside `memebot/scraper/` itself.

Honesty tiers: **VERIFIED** (measured on this machine this round), **CORRECTION** (a prior report's claim, refuted by running it), **GAP** (not measured).

---

## Verdict first

**The loop runs.** One command ranks the library, matches a song, retrieves the video, renders it and writes down what happened:

```
python scratch/memebot010_run.py --n 3
```

**VERIFIED — the proof run, 2026-08-01 13:48–13:50 UTC:**

```
library 664 clips -> 9 candidates for 3 video(s) (3x over-provision)
  [1/3] 3951188246775846619_42585188178 @histo_magazine    1280p -> song01           ok
  [2/3] 3900528591427547715_39246491958 @memesworlds8      1280p -> hallucinations.  ok
  [3/3] 3901872944578110531_76541125373 @shivnosekai       1920p -> Beautiful Home   ok

RESULT memebot010: made=3 attempted=3 calls=3 cost=$0.0018 per_video=$0.0006 wall=144.0s
```

Three clips asked for, three retrieved, three rendered, **zero failures, zero wasted candidates**, and three *different* songs. A fourth video was then produced by a separate run purely to prove the already-rendered gate (§7, failure mode 4). All four are 1080×1920 H.264 with an AAC track, confirmed by `ffprobe`.

**Cost per finished video: $0.0006.** The brief expected ~$0.001. It is one paid call per video because all five clips retrieved this round were found on page 1.

**But the three interesting results are the failures found by running the spec rather than reading it**, and one of them would have shipped broken videos indefinitely without ever raising an error:

1. **An audio window shorter than the clip does not end early — it TRUNCATES THE VIDEO.** A 5-second hand-marked hook against a 61.8-second clip produced a **5.0-second** finished file that `ffprobe` called perfectly healthy.
2. **MEMEBOT-004's `_v01` output naming is wrong at the default settings**, so the first working batch reported `made=0` while three correct videos sat on disk.
3. **The no-repeat rule did not cover the matched tier**, so a batch that had 17 unused tracks available put the same song under all three videos.

All three are fixed, each has a regression test, and each is a case where nothing threw.

---

## 1. What was built

**`clippershq/clip_pipeline.py`** — a new module, importing `clip_library` and `clip_media` read-only, invoking `memebot/scraper/edit.py` as a subprocess with a config it generates. Every fetcher is injected, so the gate, the rank, the song tiers, the config build, the window arithmetic and the record are all unit-tested with no network, no key and no ffmpeg.

**`tests/test_clip_pipeline.py`** — 48 tests. **VERIFIED: the full suite is 63/63 green, 2,694 checks, 197s.**

**`scratch/memebot010_run.py`** — the live wiring: the paid client, the unbilled CDN GET, and the argument surface. Four modes: `--plan-only` (free, no paid call), `--dry-run`, `--reconcile`, and the real run.

It was written as a new module for a reason that turned out to be load-bearing: **`memebot/scraper/edit.py` and `config.yaml` were being edited by MEMEBOT-011 while this ran, and MEMEBOT-009 is queued behind them for the same two files.** This module reads that config with a retry (a mid-write YAML parses as an error, not as garbage), deep-copies it, never writes it back, and renders into a directory it created itself.

---

## 2. The rank, and the fields deliberately excluded

Re-measured on the live library this round (**VERIFIED, n=664**), confirming BL-847:

| field | fill | used |
|---|---:|---|
| `play_count`, `caption`, `permalink`, `account`, `posted_at`, `account_user_id` | **100%** | **the spine** |
| `media_renditions` | 99.4% | hard gate |
| `media_duration_s` | 99.1% | hard gate |
| `engagement_per_follower` | **67.7%** | **rank bonus** |
| `duration_s` | 63.6% | fallback only |

```
HARD GATE   play_count >= 20,000 · duration in [5, 90] s · media_renditions present
            caption survives cleaning · permalink + account present · not already rendered

RANK        1. engagement_per_follower   (bonus — absent scores 0.0 and still competes)
            2. play_count                (tiebreak, always present)
            -  age > 365 days            (demote, never cut)

NEVER       save_count · saves_per_view · content_genre · track_title · track_artist
```

`save_count` is 21% filled and **its absence correlates with the ACCOUNT**, so ranking on it ranks accounts. `content_genre` (70.8% from two accounts) and `track_title` (58.8% from two) fail the same way. They are not down-weighted — they are absent from the rank function, and **a test reads the source of `gate()` and `rank_score()` and fails if any of them reappears.** A comment cannot enforce that; a future contributor adding "just one more signal" should turn the suite red rather than quietly bias every batch toward two accounts.

**VERIFIED — the gate on the live library:** 664 clips, 45 rejected. `duration outside [5,90]` 41, `no media_renditions` 4. Absence of a bonus field rejects nothing, which is the point.

---

## 3. CORRECTION — a short audio window truncates the video

This is the most important finding in the round, because **nothing failed.**

`ambient_bed.end_sec` becomes an input-side `-t` on the ambient stream, and the mix ends with `-shortest`. So when the audio window is shorter than the video, the video is cut to the audio.

**VERIFIED, measured on the first batch that rendered successfully:**

| clip | source | audio window | output | |
|---|---:|---|---:|---|
| `3951188246775846619_…` | **61.77 s** | 20.0 → 25.0 s (5 s) | **5.00 s** | truncated to the hook |
| `3900528591427547715_…` | 22.57 s | 18.0 → 38.0 s (20 s) | **20.00 s** | truncated to the window |
| `3901872944578110531_…` | 6.70 s | 26.4 → 46.4 s (20 s) | 5.68 s | window exceeded the clip; only edit.py's own trims apply |

`ffprobe` reports all three as healthy H.264+AAC files. A 5-second video is a valid video. Nothing in the chain had any way to know it was wrong.

This matters beyond this module: **the hand-marked hook is the entire premise of MEMEBOT-008 and MEMEBOT-012**, and a 5-second hook is exactly what a person marking by ear will produce. Handed straight to `edit.py` as an explicit window, every such hook silently destroys the clip it was meant to score.

**The fix** (`fit_window`) widens the window to cover the video plus a 1-second tail, moving the start back when the window would run off the end of the track, and dropping `end_sec` entirely when the track is shorter than the clip so `edit.py` loops it instead. The marked hook is preserved on the record as `hook_start_s`/`hook_end_s`, the applied window as `window_start_s`/`window_end_s`, and `window_fitted` states the difference in prose.

**VERIFIED after the fix** — output duration now tracks the source, the residual delta being `edit.py`'s own `trim_start_sec`/`trim_end_sec` transforms (0.1–1.5 s and 0.1–1.0 s):

| source | output | delta |
|---:|---:|---:|
| 61.77 s | 60.39 s | 1.38 s |
| 22.57 s | 21.08 s | 1.49 s |
| 6.70 s | 4.20 s | 2.50 s |

**The real answer is placement plus looping** — MEMEBOT-008 already computes `place_at_s` and `loop_count` — and `edit.py` can consume neither. Covering the video is the honest approximation until it can, and **both numbers are recorded with an explicit `plan_unapplied` note** saying they were planned and not applied. A record that carried them without that note would be a wish.

---

## 4. CORRECTION — the output filename has no `_v01` at default settings

MEMEBOT-004 §4 states `edit.py` names its output `{src.stem}_v01.mp4` and builds the whole "the filename carries its own clip_id for free" argument on it.

**VERIFIED: the `_v01` suffix is applied only when `--variants >= 2`.** At the default of 1 variant the output is `{src.stem}.mp4`.

The naming argument survives — the stem is the `clip_id` either way, which was the part that mattered — but the first live batch **rendered three correct videos and reported `made=0`**, because the pipeline asserted on a path that did not exist. `find_output()` now accepts both spellings and prefers the unsuffixed default.

---

## 5. VERIFIED LIVE — the rendition ladder is not stable, and this is what that looks like

MEMEBOT-004 warned never to cache a rendition choice, citing one clip that stored `[1280, 1280, 1280]` while a fresh manifest served 360×640. This round re-fetched the same three clips five times across fifteen minutes, always passing the literal string `"best"`:

| clip | 13:36 | 13:39 | 13:41 | 13:43 | 13:48 |
|---|---|---|---|---|---|
| `3951188246775846619_…` | 1280 | 1280 | **1920** | 1280 | 1280 |
| `3900528591427547715_…` | 1280 | **1920** | 1280 | **1920** | 1280 |
| `3901872944578110531_…` | **1920** | 1280 | 1280 | **1920** | **1920** |

**Every one of the three clips returned both 1280 and 1920 within fifteen minutes**, for an unchanged request. The manifest is what it is on the day. So this module re-fetches every time, re-runs `pick_rendition` against *that* manifest, passes the literal `"best"` (BL-802/BL-806: `"highest"`, `"low"`, a typo or `None` all silently return the **smallest** rung), and then **asserts on the height that came back** rather than on the height it asked for.

`media_renditions` is used for exactly one thing: as a hard-gate boolean meaning *this was fetchable once*. Never as a retrieval plan.

---

## 6. The record — the missing piece, and the whole reason this is a loop

memebot writes no state of any kind; grepping all 19 of its Python files for `json.dump`, `sqlite` or `.db` returns nothing. So the orchestrator owns it: **one append-only JSONL line per attempt, written BEFORE the render starts.**

```jsonc
{"schema": 1, "rev": 2, "render_id": "3951188246775846619_42585188178__20260801T134802Z",
 "clip_id": "3951188246775846619_42585188178", "clip_pk": "3951188246775846619",
 "account": "histo_magazine", "account_user_id": "42585188178",
 "permalink": "https://www.instagram.com/reel/DbVcMaxxdbb/",
 "posted_at": 1785238468, "play_count": 174020,
 "gate": {"rank": 1, "engagement_per_follower": 236.798387, "duration_s": 61.788,
          "why": ["play_count=174020", "engagement_per_follower=236.7984"]},
 "retrieval": {"pages_fetched": 1, "max_pages": 2, "prefer": "best",
               "height": 1280, "width": 720, "rendition_bandwidth": 601223,
               "source_bytes": 4641944, "retrieved_at": "2026-08-01T13:48:02Z"},
 "song": {"tier": "matched", "track_id": "sng_0001", "title": "song01",
          "hook_start_s": 20.0, "hook_end_s": 25.0,
          "window_start_s": 20.0, "window_end_s": 82.77,
          "window_fitted": "marked window 20.0-25.0s is shorter than the 61.8s clip -> widened…",
          "place_at_s": 26.57, "loop_count": 8,
          "plan_unapplied": "edit.py has no placement or loop input: place_at_s, loop_count
                             were PLANNED and NOT applied",
          "picked_by": "song_library.render_plan", "repeat_forced": false},
 "treatment": "replace",
 "source_duration_s": 61.766667,
 "render": {"pipeline": "memebot/scraper/edit.py", "template": "white_frame",
            "caption": "In Pirates of the Caribbean: On Stranger Tides, …",
            "config_used": "…/config_<render_id>.yaml", "output": "…/<clip_id>.mp4",
            "bytes": 161312673, "started_at": "…", "finished_at": "…"},
 "calls": 1, "cost_per_call_usd": 0.0006, "cost_usd": 0.0006,
 "started_at": "2026-08-01T13:48:00Z", "finished_at": "2026-08-01T13:50:02Z", "status": "ok"}
```

**One deliberate deviation from MEMEBOT-004 §4, and it is worth naming.** The spec says the pending line is "updated on completion". A JSONL line cannot be updated in place without rewriting the file, and a rewrite is precisely what a concurrent reader cannot survive — in a repo where eleven rounds were in flight simultaneously, that is not hypothetical. So **completion appends a second line with the same `render_id` and a higher `rev`**, and readers take last-wins by `(render_id, rev)` — the same idiom `clip_library.read_all` already uses. The spec's guarantee (a crash mid-render leaves evidence) is preserved; the concurrency hazard is removed.

**`treatment` is probed, never assumed.** MEMEBOT-006 planned duck-vs-mute for clips carrying dialogue under music; MEMEBOT-011 found the DASH *video* rendition carries no audio stream at all. Both are true of different sources, so the module asks `ffprobe`: `replace` (silent source — the track is the whole soundtrack), `mix`, `none`, or `unknown` when ffprobe cannot say. **All five renders this round: `replace`**, confirming MEMEBOT-011.

**VERIFIED the audio is actually audible:** the finished videos measure **mean −27.0 dB, max −13.5 dB** — a listening level, not the −49 dB inaudible failure MEMEBOT-011 documented before its solo-volume range existed.

---

## 7. The five failure modes, and which are proven rather than argued

| # | failure | rule | status |
|---|---|---|---|
| 1 | **video unretrievable** | Skip after `max_pages`, record `failed:unretrievable` with a machine-readable reason (`not_found` / `fetch_failed` / `low_rendition` / `no_manifest`), take the next candidate. **`max_pages` is never widened inside a run** — the candidate list is over-provisioned 3× instead. | **Unit-proven** (injected fetchers). **GAP: not seen live** — all 5 clips landed on page 1. |
| 2 | **no matching song** | Four tiers, degrade never block: `explicit` → `matched` (MEMEBOT-008) → `lru_corpus` (17 local tracks) → `none` (still a deliverable). Every render records which tier fired. | **VERIFIED live** — two of the three proof videos ran on `lru_corpus` because the matcher's pick was excluded (below). |
| 3 | **render crashes mid-flight** | The pending line is the detector. `reconcile()` resolves any pending older than a timeout: healthy output → `ok`; otherwise → `failed:crash` **and the partial file is deleted**, because `--skip-existing` is on by default and would treat a truncated mp4 as done forever. | **Unit-proven**, including that a still-running render is *not* reconciled out from under itself. |
| 4 | **clip already made into a video** | Gate on `clip_id` present with `status: ok` in the record — deliberately **not** on the output file existing, since outputs get moved, uploaded and deleted. A test asserts `rendered_ok_ids` contains no `os.path.exists`. | **VERIFIED live** — a fourth run skipped all three finished clips and took candidate #4 (`@solidshampooz`), with a fourth distinct song. |
| 5 | **same song twice running** | Exclude the last *k*=3 `track_id`s. If that empties the pool, relax and record `repeat_forced`. | **VERIFIED live, after a real defect** — see below. |

### The no-repeat defect, and why the spec's relaxation was the wrong trade

The first working batch produced three videos with **the same song under all three**, and dutifully recorded `song_repeat_forced` on two of them. The rule had fired correctly and the outcome was still wrong.

Two causes. First, `avoid` was consulted only on the LRU path — the matched tier ignored it entirely. Second, and more interesting: **MEMEBOT-004's relaxation rule ("if exclusion empties the candidate set, relax to not-the-immediately-previous") treats the store as the only pool.** It was empty of fresh tracks; the local corpus had **seventeen unused ones**. Forcing a repeat while seventeen fresh tracks sit idle is not a graceful degradation, it is the wrong answer arrived at politely.

The fix applies the no-repeat set to the matcher too — by bumping the avoided songs' `uses` counters **in memory**, letting `song_library`'s own rotation do the work rather than second-guessing it, and **never writing the store**, which belongs to MEMEBOT-008. When the store has nothing fresh, it falls through to the larger corpus; only when *nothing anywhere* is fresh does it relax and record `repeat_forced`.

**VERIFIED after the fix:** three videos, three different songs (`song01`, `hallucinations.`, `Beautiful Home`), and a fourth run produced a fourth (`stupid song`). Zero forced repeats.

### The tier degradation is real, not theoretical

**VERIFIED:** MEMEBOT-008's store currently holds 3 songs, of which **only 1 has a path that resolves to a file that exists** — the other two are `REPLACE_ME_02.mp3` / `REPLACE_ME_03.mp3` placeholders, correctly so, since that round is still in flight. The module checks that the matched path exists before believing it, which is exactly why videos 2, 3 and 4 fell through to the local corpus and got real music instead of a render against a missing file.

---

## 8. Cost, honestly split

**VERIFIED from `spend.json`, label `clip_pipeline`:**

| | calls | cost |
|---|---:|---:|
| This round's six runs (including every debugging iteration) | 16 | **$0.0096** |
| INFRA-007 using this module mid-session (§9) | 4 | $0.0024 |
| **Total on the label** | **20** | **$0.0120** |

The proof run itself was **3 calls, $0.0018, $0.0006 per video**. Budget was $0.20; **4.8% of it was used.**

One paid call per video, because every clip retrieved was on page 1. Wall time is dominated entirely by ffmpeg — 144 s for three videos against ~1 s of API — so **throughput is a CPU question, not a cost question.** Spend is metered into the same `spend.json` every other flow writes, so it cannot be invisible to the cap.

---

## 9. A defect found by another round using this module

**INFRA-007 ran this orchestrator with `--dry-run` while the round was still open**, which surfaced something the tests had not: a dry run wrote `pending` lines and never completed them — *precisely* the shape `reconcile()` reads as "died mid-render". It would have stamped `failed:crash` on three renders that were never meant to happen and reported a fabricated failure rate against itself.

Fixed: a dry run now reaches a terminal `dry_run` status, `reconcile()` only ever touches `pending`, and a test asserts both. **The three orphan lines from that run remain in `scratch/renders.jsonl` unresolved**, because they are less than 30 minutes old and the stale threshold correctly refuses to touch another process's possibly-live work — which is the same guard working as intended.

---

## Limits

- **Four videos is four videos.** The gate, the rank and the tiers are exercised; throughput, long-run song rotation and the unretrievable path are not.
- **The retrieval-depth model is untested here.** Every retrieval attempted this round — 13 of 13 across all runs, including the dry ones — came back on page 1 for 1 call. MEMEBOT-004's ~55/40/5 planning split and the 1,675-day deep tail are **neither confirmed nor refuted** by n=5 — the candidates were ranked partly by recency, so page-1 hits are exactly what should be expected and this says nothing about the tail. **Failure mode 1 has never fired in anger.**
- **`reconcile()` has never resolved a real crash.** It is unit-proven against synthetic pending lines. No render has actually died mid-flight yet.
- **The caption is the account's own text, cleaned** — emoji stripped (Montserrat-Bold has no glyph and renders blank boxes), hashtag tails cut, truncated at a word boundary to `edit.py`'s 120-char limit. **Nobody has judged whether these captions are any good.** That is a content question this round did not touch.
- **Placement and looping are planned and not applied.** Until `edit.py` accepts a placement offset, a hand-marked hook is stretched to cover the clip rather than dropped at a chosen moment. The record says so on every line; the videos are correct but not what MEMEBOT-008 intends.
- **The licensed-music question is untouched and real.** Two of the four tracks used are from a corpus that is 13/19 licensed. `track_id` and `kind` are on every record so the decision stays reversible and auditable, which is the most engineering can contribute to a rights question.
- **`edit.py` was being modified by MEMEBOT-011 during every run in this report.** It compiled and behaved consistently throughout, and this module invokes it as a subprocess with its own config precisely so a concurrent edit cannot take the orchestrator down — but the renders were made against a moving target and a re-run after MEMEBOT-009 and MEMEBOT-011 land is the honest confirmation.
- **The `white_frame` template was used for all four.** No template comparison was made.
- **A second round is building the same thing.** `MEMEBOT-015` filed a claim to "connect the full loop end to end: rank → match → retrieve → render → record" in a new `clippershq/loop_runner.py` minutes before this report was written. The claim tool reports no *path* conflict — different files — so both will land. **Whoever reconciles them should read §3, §4 and §7 first**, because those three defects are invisible until you render against a real clip and are the kind a second implementation will reproduce exactly.
- **GAP: no ffmpeg cost model.** 144 s for three videos is one measurement on one machine at one CRF, not a throughput figure.

---

<!-- CLAIMS
file:   clippershq/clip_pipeline.py
file:   tests/test_clip_pipeline.py
file:   scratch/memebot010_run.py
func:   clippershq/clip_pipeline.py::rank_candidates
func:   clippershq/clip_pipeline.py::retrieve_video
func:   clippershq/clip_pipeline.py::fit_window
func:   clippershq/clip_pipeline.py::pick_song
func:   clippershq/clip_pipeline.py::reconcile
func:   clippershq/clip_pipeline.py::run_batch
func:   clippershq/clip_media.py::retrieve
func:   clippershq/clip_media.py::pick_rendition
func:   clippershq/clip_library.py::read_all
func:   clippershq/song_library.py::render_plan
-->

*A hook requested an accessibility-agent review. This round produced a Python orchestrator and a CLI with no web UI in scope, so it was not applicable and was not run.*
