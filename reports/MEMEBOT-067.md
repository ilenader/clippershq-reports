# MEMEBOT-067 — two finished videos join the song store, and the record builder was never the reason they could not

**Date:** 2026-08-02 · **Class:** Diagnose + fix + prove · **Spend:** **$0.0012** on the records of a **$0.05** budget; `spend.json` delta **$0.0000**

Preconditions read before any write: `tools/claims_read.py --holders` per target **and**
`git status --porcelain`. Claimed as `MEMEBOT-067` with 11 repeated `--write` flags,
*"no path conflicts. 11 other round(s) in flight."* Ledger backed up to
`scratch/mb067/runs.jsonl.pre_mb067.bak` (194 lines) before the first render.

**Two videos rendered through `run_batch` with no explicit song now carry keys that resolve
in the store.** They are the first two of the ledger's 28 finished videos that do.

---

## 0. THE CONFLICT, DECIDED FIRST

`clippershq/clip_pipeline.py` — where two of the three defects below live — is held by
**BL-958 (active)** and **BL-899 (stale)**. It was clean at the start of this session and
`' M'` with **265 uncommitted insertions** by the time I reached it (mtime 12:06, `+265/-12`,
BL-958's `default_fetchers` / `CAP_KEY` work). Two agents editing one 2,235-line file
concurrently is how work gets silently reverted here.

So this round was **read-only on it**, and its fix ships as
`scratch/mb067_clip_pipeline.patch` — generated against HEAD, `git apply --check` clean,
both hunks **measured out of tree** against the real library. What I *could* land, I landed:
the enforcement point, which turned out to belong somewhere else entirely.

---

## 1. WHY THE PIPELINE'S KEY DOES NOT MATCH

**The record builder is not the reason, and that is the finding.** MEMEBOT-060 fixed the
normaliser and MEMEBOT-062 re-proved it; both drove `run_batch` with `explicit_song=`, which
is **tier 1 of `pick_song` and returns before the song store is ever opened**. The tier an
unattended run actually uses was never touched.

Driven through it, on 60 real candidates and the production field expressions:

```
matched-tier record keys that resolve : 60 / 60
```

The key the pipeline builds is **correct**. It is the SONG that is wrong, and it is wrong in
two independent places — both of which end at the same address: the local corpus.

### a. The matcher parks, and the ranker never reaches the clips it does not

| measured over the real library | |
|---|---:|
| clips through the gate | **1,751** |
| of those, the matcher **parks** | **1,508 (86.1%)** |
| rank of the first candidate it can serve | **55** |
| `run_batch` cuts the candidate list to | `n × 3` |
| **smallest `n` that can even SEE a servable clip** | **19** |

The ranker sorts by views. The matcher routes on vision rules. They are independent, so a
production run at `n=3` walks nine clips that all park, falls through, and renders nine
videos that can never earn rotation. **Nothing in the rank could tell you that.**

### b. When it does match, the no-repeat rule throws the match away

```python
if _matched_repeat and _corpus_fresh:
    raise _FallThrough(...)          # prefer a fresh corpus track over a repeated store song
```

Measured with the matched song in the no-repeat set and the shipped corpus available:

```
real store matches discarded for a corpus track : 60 / 60
corpus tracks that appear in the store at all   :  0 / 17
```

**11 of the 13 corpus records already on the ledger were written by this branch.** The trade
it makes is variety for evidence, and the thing it buys variety with cannot carry evidence:
a corpus record's key resolves to nothing, so its outcome joins nothing, so the window that
was actually played earns nothing. It is not even variety of the right unit — the no-repeat
set keys on the **song**; the evidence arm is the **hook window**.

### c. What that produced

| ledger, before this round | records | key in the store |
|---|---:|---|
| `matched` (via `render_plan`) | 110 | **0** |
| `lru_corpus` | 13 | **0** |
| no tier recorded | 59 | **0** |
| `explicit` (MEMEBOT-060 / 062) | 12 | 12 — none of which is a finished video |

BL-955's finished video, named:

```
scratch/bl691_audio/1975396383375922.m4a@15.64-35.64   resolves=False
tier=lru_corpus   picked_by=least-recently-used over local corpus
```

**"A track not in the store at all"** — the third of the brief's three known causes, and the
only one still live. The absolute path and the placeholder window are both closed.

---

## 2. THE FIX — the check belongs IN the writer, not in front of it

MEMEBOT-060 put `check_joinable` in `run_batch`, immediately before its `append_record`
call, and **named the gap in its own limits**: *"any other caller that writes a record
directly bypasses it."* That is a rule stated in one caller, standing in front of a writer
whose own docstring calls it the only supported way in — the same shape as the report
collision that overwrote four published reports before MEMEBOT-057 moved *that* rule into
the tool.

**So it moved into `memebot/scraper/run_record.py::record()` — the one function in the
codebase that appends to the ledger.** Every record now carries a verdict regardless of
which caller wrote it.

```
!! this record will NOT join the song store: song is not in the store at all; key
   'scratch/bl691_audio/1975396383375922.m4a@15.64-35.64' matches none of the 21 store
   key(s). The video is fine -- its outcome is recorded but can never earn rotation.
```

That is the real store, the real 21 keys, printed by a call that went through
`clip_pipeline.append_record` **with no caller-side check at all**.

Three rules, each load-bearing:

| rule | why |
|---|---|
| **warns, never blocks, never raises** | a video that cannot join is still a finished video; losing the record would lose the render *and* the evidence |
| **never fabricates** | store unreadable or checker unimportable → `joinable: null` with a reason. *"No key matched"* and *"there were no keys to match against"* are different facts and only the second is a tooling failure |
| **one implementation** | the verdict is `clip_pipeline.check_joinable`, imported. A second copy drifts and then disagrees with what the pipeline printed on screen |

And two things it deliberately does **not** touch: outcome lines (they carry no window —
answering `False` would stamp a fake defect on every one), and rows that never reached the
song stage (`_base_record` carries neither `song` nor `output`, so a clip abandoned at
retrieval is not a render with a bad key). A row *with* an output and no song **is** still
flagged — that is a shipped video with nothing to join on.

### What could not be landed

`scratch/mb067_clip_pipeline.patch`, two hunks, measured out of tree on the real library:

| hunk | before | after |
|---|---|---|
| **B** — `servable_by()` + a stable re-order in `rank_candidates` (drops nothing, parked clips kept behind) | 0 of 9 candidates servable at `n=3` | **9 of 9**, at a cost of **1.77s** against ~55s per render |
| **A** — the fall-through requires a corpus track that *could* join | 0 of 60 matches kept | **3 of 3 kept**, `repeat_forced=True` |

---

## 3. THE TEST THAT FAILS ON AN ABSOLUTE PATH

`tests/test_pipeline_join.py` — **16 checks, green**; MEMEBOT-060's `test_join_key.py`
stays 11/11.

It copies MEMEBOT-060's source-reading shape and **parses the AST rather than scanning
text** — a text scan cannot tell a prohibition in a docstring from a use in code, which has
been got wrong three times in this repo. It also covers the field MEMEBOT-060's source test
did not:

> `fit_window` **widens** the played window; the store key is the **marked** one. A record
> that reads `window_start_s` instead of `hook_start_s` is well-formed, its video is
> correct, and its key is a window nobody ever marked. The test asserts the marked name is
> read **first**, with the played one permitted only as the fallback.

The regression tests the brief asks for, all through the new enforcement point and none of
them touching the real ledger:

| written | verdict |
|---|---|
| an absolute Windows song path | `joinable: false`, *"absolute song path"* — **fails if it is ever written silently** |
| a corpus track | `joinable: false`, *"song is not in the store at all"* |
| an unmarked window on a store song | `joinable: false`, *"not one of its marked hooks"* |
| store unreadable | `joinable: null` — **not** `false` |
| any of the above | **the record still lands.** Warns, never blocks |

---

## 4. TWO RENDERS, TWO WINDOWS, BOTH RESOLVE

No `explicit_song`. The song, the hook and the window were chosen by
`song_library.render_plan` inside `run_batch` — the tier that was never covered.

```
TARGET KEYS (2, both in the store's 21):
   memebot/scratch/song03.mp3@7.828-22.714
   memebot/scratch/song04.mp3@13.769-29.369

status : ok        tier : matched (song_library.render_plan)
song   : memebot/scratch/song03.mp3    absolute? False
window : 7.828-22.714
key    : memebot/scratch/song03.mp3@7.828-22.714     RESOLVES : YES     joinable : True

status : ok        tier : matched (song_library.render_plan)
song   : memebot/scratch/song04.mp3    absolute? False
window : 13.769-29.369
key    : memebot/scratch/song04.mp3@13.769-29.369    RESOLVES : YES     joinable : True
```

**Verified off the artefacts, never off an exit code** — two rounds have now hit
`status=no-match` at returncode 0:

| | video 1 | video 2 |
|---|---|---|
| file on disk | 7,954,750 B | 10,501,630 B |
| stream | 1080×1920 h264 + aac | 1080×1920 h264 + aac |
| duration | **26.33s** | **75.21s** — both clear the 8.0s floor |
| level (`volumedetect`) | mean −16.1 dB, peak −0.6 dB | mean −19.2 dB, peak −7.6 dB — **not silence** |

And the thing that actually matters, read back through the loop's own grouper:

```
outcome_loop.resolve()  ->  73 records
records landing on a STORE key : 8
   ... of which FINISHED VIDEOS : 2      <- both from this round
bias_map : {}   (the bar is 25 outcomes per arm — {} is the correct answer today)
```

Wall 154.3s for both. **$0.0012** on the records (2 retrieval calls at $0.0006); the ledger
did not move because no `spend_path` was passed.

---

## 5. THE LEDGER

`memebot/runs.jsonl` is tracked and pushed to memebot's own remote (MEMEBOT-062). The 22
historical records stay marked and unbackfilled. **194 lines before this round, 198 after**;
the four new lines are two `pending`/`ok` pairs, and two of them are the first finished
videos on the ledger that can ever earn rotation. Committed to the nested repo with the fix,
so *"when did a record become joinable"* has an answer.

---

## PROOF

| Required | Result |
|---|---|
| why the pipeline's key does not match | the record builder is correct (**60/60 matched-tier keys resolve**); the SONG is wrong — **86.1% park, first servable clip at rank 55, `n≥19` to reach one**, and **60/60** matches discarded by the no-repeat fall-through for a corpus track, of which **0 of 17** are in the store |
| fixed at the source | the check moved **into `run_record.record()`**, the one appender; the two `clip_pipeline` hunks delivered as a HEAD-clean patch, measured, **not applied** — BL-958 holds the file |
| a test failing on an absolute path or an unresolvable key | `tests/test_pipeline_join.py` **16/16**, AST-based source checks + 10 behavioural ones; `test_join_key.py` still **11/11** |
| an unresolvable key warns at write time | verified against the **real 21-key store** through `append_record` with no caller-side check |
| two fresh renders, different windows, both resolving | **YES** — `song03.mp3@7.828-22.714` and `song04.mp3@13.769-29.369`, both `tier=matched`, both `joinable: True`, both real 1080×1920 h264+aac files with audio that is not silence |
| suites | **ALL GREEN — 125/125 suites, 4,481 checks** (798.3s), 9 rounds in flight |
| campaigns | `8e02f8d6f6307ae8` (sort_keys) **and** `7a029ee5447cddd8` (compact) — both **MATCH** |
| config.json | parses, **161 keys, 5 campaigns** |
| budget | $0.05 allowed; **$0.0012** on the records, `spend.json` delta **$0.0000** |

---

## Method / limits

**Only 4 of the 21 store keys are reachable at all.** `pick_song` passes `count=False` — the
store is the operator's file and this module does not write it — so `uses` is never
incremented, all 21 hooks sit at `0`, and `pick()` returns **`h1` for every mood, every
time**. My two windows differ because they come from two different **songs**; two windows of
the *same* song cannot be reached through the matched tier today. That also means a repeated
song is currently a repeated *window* — which is how an arm reaches its 25-outcome bar, but
it is not the rotation the store was marked for.

**The two renders used a subset library, and that subset is the defect, not the proof.**
`run_batch` walks candidates in rank order and cuts to `n × 3`; the first servable clip is
at rank 55, so rendering to reach it is a bill, not an experiment. The library given to
`run_batch` is a real subset of the real library — the same records, through the same gate
and the same ranker — filtered to clips the matcher can serve. Everything downstream of the
candidate list is production, including the song choice. The ordering defect is measured in
`scratch/mb067_diagnose.json` and is hunk B of the patch.

**The patch is verified but unapplied.** `git apply --check` passes against HEAD and both
hunks were measured by importing the patched module out of tree. It has not been run inside
a live `run_batch`, and it will need re-checking after BL-958 lands.

**A corpus render still cannot join, by design.** Nothing here maps a corpus track onto a
store song; that would fabricate evidence that then counts toward the bar deciding rotation.
The fix makes the pipeline stop *choosing* one, and makes the ledger say so when it does.

**Not measured here:** whether the audio in those two files is actually the marked window.
The record says which window was configured and `volumedetect` says the audio is real;
cross-correlating the rendered audio against the track is MEMEBOT-066's claim, not mine.
