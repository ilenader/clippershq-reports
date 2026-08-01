# MEMEBOT-015 — The loop is connected. **3 real videos for $0.0018.** And wiring it caught two silent bugs of my own, one of which you predicted the shape of.

**Date:** 2026-08-01 · **Type:** Integration + live run · **Spend:** **$0.0018** of $0.10 (3 paid calls)
**New:** `clippershq/loop_runner.py`, `tests/test_loop_runner.py`.
`outcome_loop.py` **untouched** — it stays the single owner of the statistics.

---

## The three videos

| clip | song/hook | treatment | applied | output | ffprobe |
|---|---|---|---|---|---|
| `3903533101…80578444437` | sng_0001/h1 | duck-under | mute (forced) | 5.5 MB | h264 720×1280, **42.57 s** + aac |
| `3712056345…333045814` | sng_0001/h3 | duck-under | mute (forced) | 4.2 MB | h264 1080×1920, **19.90 s** + aac |
| `3430176313…65975240301` | sng_0001/h2 | **mute-and-replace** | mute (requested) | 832 KB | h264 720×1280, **7.20 s** + aac |

All three play — video and audio streams present, durations matching their source clips.
`scratch/mb015/out/`.

**Cost, per step:**

```
paid clips-page calls : 3  ->  $0.0018       (1 page each, max_pages=2 never needed a 2nd)
CDN download          : free (6.5 MB total)
render (local ffmpeg) : $0.00
rank + song match     : $0.00 (offline)
TOTAL                 : $0.0018   elapsed 25s
```

---

## Two silent bugs the wiring caught — both mine

### 1. The treatment was computed correctly and thrown away at the boundary

**This is the exact failure shape you asked me to pin for `hook_key`, in a different place.**

`clip_speech.treatment_for()` returns `mute-and-replace` / `duck-under`. `memebot/duck.py`
speaks `mute` / `duck` / `keep`. Passing one to the other is **not an error** —
`resolve_treatment` falls back to its default and returns a *reason*, so the render succeeds.

First live run, all three clips:

```
mute (unknown treatment 'duck-under', falling back to mute (valid: mute, duck, keep))
mute (unknown treatment 'mute-and-replace', falling back to mute ...)
```

**Every clip silently rendered muted.** BL-848's whole four-class labeller was being discarded
one function call from where it mattered. Fixed with an explicit `_TREATMENT_TO_DUCK` map, and
`tests/test_loop_runner.py` now asserts **every class the labeller can emit maps to a treatment
`duck.py` accepts** — a rename on either side fails the suite.

After the fix the decision reaches `duck.py` and its override is honest:

```
mute (requested)                                                    <- music-only, as decided
mute (duck requested but the source has no audio stream: nothing
     to duck against, forced to mute) [source has no audio stream]  <- MEMEBOT-011's DASH note
```

The record now carries `treatment` (decided), `treatment_applied` (what happened) and
`treatment_forced`, so the two can never diverge unnoticed again.

### 2. The videos were 5 seconds long

I put `-t (to - ss)` on the audio input. With `-shortest`, that bounded the **whole output**:
40-second clips rendered as 5-second files, video included. Fixed by seeking the song to the
hook and letting `-shortest` bound by the **video**. Durations went 5.0/6.0/5.0 s →
42.6/19.9/7.2 s.

`hook_len_s` and `loop_count` stay in the record so a later round can implement true
window-looping and compare against this.

---

## The requirements, each proved

**1. The chain runs** — rank → match → retrieve → render → record → readable by
`outcome_loop`. `resolve()` finds all 3; `export_csv` lists them with **blank metric cells**
ready to fill.

**2. The bias is always passed.**

```
bias_map: 0 window(s) have earned extra rotation
```

`run()` computes `SL.bias_map()` and passes it on every call — never `None`. At zero posted
videos `{}` is the correct answer, and a test asserts `run()`'s source contains `bias_map`, so
dropping the argument fails the suite rather than silently reverting to plain rotation.

**3. `hook_key` is pinned.** Two tests: the literal string
`scratch/song01.mp3@20.0-25.0`, and a **round trip** — a record written by the orchestrator is
rebuilt the way `outcome_loop`'s grouper builds it and must match. Drift fails the suite instead
of returning `{}` forever with no error.

**4. Treatment comes from the labeller.** `audio_treatment()` reads a stored measured class
first, then `clip_speech.declared_class()` (free — `licensed_music` states it outright), and
**never thresholds `speech_frac`**. A local AST test asserts that in this module by name, on top
of the existing guard.

**Unknown → duck, not mute.** Muting a dialogue clip is unrecoverable; ducking a music clip
costs a little CPU. `audio_class` is **0% populated** across all 664 clips and `speech_frac` is
3%, so the free declared path did the work: 1 of 3 clips resolved to `music-only`, 2 to unknown.

**5. Placeholders declared, not hidden.** All three windows are still placeholders and all three
said so, on the console and in the record:

```
! 3903533101225116852_80578444437: hook h1 is a PLACEHOLDER (PLACEHOLDER - mark by ear)
  — rendering, but the window was not marked by ear
```

**6. Ranking on trustworthy fields only.** `RANK_FIELDS = ("play_count",
"engagement_per_follower")`, with `save_count`, `content_genre` and `track_title` excluded and
the measured reason for each in a comment. A test asserts none of the three is in the key.
Top-ranked play counts: 42.5M, 23.6M, 22.9M.

**7. Retrieval.** `clip_media.retrieve(clip_id, max_pages=2)`, `clip_id` **verbatim** — no
reconstruction. All 3 found on page 1. **Nothing caches a rendition URL**, and this run showed
why: the same clips returned heights `1920, 1920, 1920` on the first run and `1280, 1920, 1280`
on the second. **A cached URL would have been wrong within minutes.**

---

## Verification

| check | result |
|---|---|
| `tests/run_all.py` | **ALL GREEN — 64/64 suites, 2,723 checks** |
| `tests/test_loop_runner.py` | **PASS — 20 checks** |
| 3 videos, ffprobe | h264 + aac, 42.6 / 19.9 / 7.2 s |
| `bias_map` passed, `{}` at n=0 | ✓, asserted in source |
| `hook_key` ↔ grouper | pinned literal **and** round trip |
| treatment vocabulary ↔ `duck.py` | every labeller class maps to a valid treatment |
| placeholders | 3/3 flagged, console + record |
| `export_csv` | 3 present, metric cells blank |
| campaigns SHA | **8e02f8d6f6307ae8 — MATCH** |
| `config.json` | parses, 162 keys, untouched |
| `outcome_loop.py` | **unmodified** |

The full suite came back green — **64/64 suites, 2,723 checks** — with `test_filelock.py`
passing in this batch (it is the concurrency-sensitive one you flagged; it happened to get a
quiet window).

---

## Limits

- **All three clips resolved on tier FALLBACK**, because `scratch/songs.json` ships with empty
  mood maps (MEMEBOT-008, deliberate). The four-tier matcher is exercised but not
  *discriminating* — every clip got the house mood.
- **One song, three windows.** `sng_0002`/`sng_0003` are still `enabled: false` templates, so
  song-level rotation was untested; only hook-level rotation ran.
- **Every window is still a placeholder.** The videos are real but the musical timing is not
  chosen — they demonstrate the pipeline, not a good edit.
- **The hook does not loop.** `loop_count` is computed and recorded but the render plays the
  song continuously from the hook start. True window-looping needs `aloop`/`atrim` and is not
  built.
- **`place_at_s` is recorded and not applied.** The song starts at t=0 of the video; the
  computed placement is carried for a later round.
- **`treatment_applied` was `mute` on all 3** — the retrieved DASH video rendition carries no
  audio, so duck had nothing to duck against. The duck path is therefore wired and *untested on
  real media*.
- **`audio_class` is 0% populated library-wide**, so classification leaned entirely on the free
  declared signal. The measured VAD path is wired but unexercised here.

---

## Method

Filed a claim (10 rounds in flight, no path conflicts). Surveyed the existing pieces before
writing anything — `clip_media.retrieve`, `clip_speech.treatment_for`, `duck.build_audio_graph`,
`run_record.record` — and delegated to each rather than re-implementing. The decision layer
(`plan_one`) is separated from `run()` so placeholder, treatment and ranking behaviour are
testable with no network, key or ffmpeg. Live run: 3 paid `/gql/user/clips` calls ($0.0018),
free CDN downloads, local ffmpeg renders, records appended to `memebot/runs.jsonl` through
memebot's own `run_record`. Both bugs above were found by reading the actual console output of
the first live run rather than assuming the wiring worked. No key was read, printed or logged.
