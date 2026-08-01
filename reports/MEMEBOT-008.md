# MEMEBOT-008 — The song library is built. Rotation spreads **50 picks over 7 windows to a spread of 1**, and the fallback never fired on 20 real clips because valence caught everything.

**Date:** 2026-08-01 · **Type:** Implementation · **Spend:** $0.00 · **Paid calls:** 0
**New:** `clippershq/song_library.py`, `tests/test_song_library.py`, `scratch/songs.json`.
No existing clippershq module was edited. Claim filed as `.claims/MEMEBOT-008.json`.

---

## The one thing I would not do

**I did not mark the hook windows.** Every `start_s`/`end_s` in `scratch/songs.json` is a
placeholder, labelled `"PLACEHOLDER - mark by ear"`, and the store's own `_readme` says so.

Writing `"start_s": 21.0, "note": "the drop"` would have made the deliverable look finished.
It would also have been **exactly the failure the module exists to prevent** — BL-690 measured
automatic drop detection at **100% fabrication**, returning a timestamp on all 36 clips
including all 19 that had nothing there. A number I invented by looking at a waveform I never
heard is the same fabrication with a human in the loop.

So the plumbing is real and tested; the windows are yours to fill. **Open `song01.mp3`, find
the window, overwrite three numbers.**

---

## 1. The store

`scratch/songs.json` — one record per song, hand-editable, atomic on save (tmp + fsync +
`os.replace`, so a crash mid-write cannot destroy your marked windows).

| song | path | duration | hooks | state |
|---|---|---:|---:|---|
| `sng_0001` | `memebot/scratch/song01.mp3` | **162.54 s** (ffprobe) | 3 | **enabled — the real file** |
| `sng_0002` | `…/REPLACE_ME_02.mp3` | null | 1 | `enabled: false` |
| `sng_0003` | `…/REPLACE_ME_03.mp3` | null | 1 | `enabled: false` |

Only one real audio file exists in the tree, so the other two ship as **templates with
`enabled: false`** — `pick()` skips them, so a half-filled store can never silently render
against a missing file. Point `path` at a file, set `duration_s`, mark the hooks, flip
`enabled`.

**Counters at both levels**, as specified: `song.uses` and `hook.uses`.

`validate()` catches the hand-edit mistakes and returns a list rather than raising — a bad
record should be reportable, not fatal, in a file you edit by hand. It flags: missing
path/mood/`song_id`, duplicate ids, `end_s <= start_s`, negative starts, **a hook past
`duration_s`**, and **a song with no hooks at all** (which could never be picked).

## 2. Hand-marked, enforced in code

`hooks_auto[]` exists on every record and **`pick()` never reads it**. A test pins this
directly: a store where the auto window has `uses: 0` and the hand window has `uses: 9` still
returns the hand window. A second test proves `hooks_auto` survives load→save untouched, so a
future detector has somewhere to write without endangering a render.

Both measurements are in the module docstring, with their report numbers, so "improving" this
means arguing with a figure rather than a preference.

## 3 + 4. The matcher — four tiers, provenance is not a gate

Run over **20 real clips** from the 634-clip library, deliberately sampled 7 franchise-bearing
/ 6 genre-only / 7 with neither:

```
tier distribution: {GENRE_MOOD: 10, VALENCE_MOOD: 9, FRANCHISE_MOOD: 1}
```

| # | tier | mood | conf | song/hook | review | ss | to | place_at |
|---:|---|---|---|---|---|---:|---:|---:|
| 5 | **FRANCHISE** | goofy | **high** | sng_0001/h2 | **no** | 60.00 | 65.00 | 24.51 |
| 2 | GENRE | goofy | medium | sng_0001/h1 | yes | 20.00 | 25.00 | 25.33 |
| 20 | VALENCE | warm | medium | sng_0002/h1 | yes | 0.00 | 5.00 | **0.00** |

**The fallback never fired on real data** — all 7 "neither genre nor franchise" clips resolved
on **valence**. That is the spec's central claim (99% vs 28%) reproducing on the real library:
the tier that feels like a backstop is the one carrying half the corpus, and tier 4 is there
for the residue.

`matched_on` is a readable string on every result — `valence:positive -> mood:warm`,
`genre:comedy -> mood:goofy` — so a row can be argued with later.

**Provenance is not consulted at all.** A test asserts a `derived` genre still matches. Instead
every result carries the tier as **`confidence`** (high/medium/low) and **`needs_review`**
(false only on a franchise hit). Confidence is the tier name, not a number — a 0.0–1.0 score
would imply a calibration nothing here has earned.

## 5. The fallback is the primary path

`match()` **never returns None**. With a house set configured it answers from it; with none
configured it still returns a tier and an explanatory `matched_on` rather than failing. A test
pins that an entirely empty clip resolves.

Separately, `pick()` falls back to **any enabled song** when no song carries the requested
mood — a library with no `eerie` track must still produce a video, and the caller can compare
the mood it asked for against what it got.

## 6. Rotation — 50 picks, spread of 1

```
sng_0001/h1  7      sng_0002/h1  8      sng_0003/h1  7
sng_0001/h2  7      sng_0002/h2  7      sng_0003/h2  7
sng_0001/h3  7
min 7   max 8   spread 1   (perfect = 7.1)
song-level: sng_0001 21, sng_0002 15, sng_0003 14
deterministic across two fresh loads: True
```

`min(candidates, key=(hook.uses, song.uses, song_id, hook_id))` — a total, stable tie-break, so
the same store state and the same clip list reproduce the same assignment. That is what makes a
comparison re-runnable, and it is why an under-performing window is now distinguishable from an
under-sampled one.

`count=False` plans without mutating, so a dry run can show the assignment before committing it.

## 7. Length math

```
place_at_s = 0.0                                   if clip_len < 2 * hook_len
             clamp(0.43 * clip_len, 0, clip_len - hook_len)   otherwise
loop_count = ceil((clip_len - place_at_s) / hook_len)
```

| clip | hook | place_at | loop |
|---:|---:|---:|---:|
| 57.1 s | 4.0 s | 24.54 | 9 |
| 40.7 s | 6.0 s | 17.50 | 4 |
| 10.0 s | 5.0 s | 4.30 | 2 |
| **8.0 s** | **5.0 s** | **0.00** | 2 |

`audio_ss_s` / `audio_to_s` are **copied verbatim** from the marked window — a test asserts
`12.345 / 17.891` survive with no rounding. A further test proves the hook always fits inside
the clip, and garbage inputs (`None`, `0`, strings) return `0.0` rather than raising.

## 8. The mood maps ship empty

`franchise_mood_map`, `genre_mood_map`, `valence_mood_map` and `fallback_moods` are all `{}` /
`[]` in both `new_store()` and the shipped file, with a test asserting it. Tiers 1–3 simply do
not fire until you fill them — which is correct behaviour, not a broken state.

The maps used in §3's table are a **test fixture inside `scratch/mb008_prove.py`**, not
defaults. Nothing I wrote decides that Two and a Half Men is goofy.

---

## Verification

| check | result |
|---|---|
| `tests/run_all.py` | **ALL GREEN — 60/60 suites, 2,553 checks** |
| `tests/test_song_library.py` | **PASS — 55 checks** |
| store loads + `validate()` | **CLEAN** |
| matcher over 20 real clips | 20/20 resolved, tiers 1/10/9/0 |
| rotation, 50 picks / 7 windows | **spread 1**, deterministic |
| campaigns SHA | **8e02f8d6f6307ae8 — MATCH** |
| `config.json` | parses, 162 keys, untouched |
| existing clippershq modules | **none edited** |

The full suite ran green after a delayed flush — **60/60 suites, 2,553 checks**, with
`test_song_library.py` contributing 55. Nothing else moved.

---

## Limits

- **The hook windows are placeholders.** Nothing renders correctly until you mark them. This is
  the deliberate gap, not an oversight.
- **Two of three songs are templates** (`enabled: false`) because only one audio file exists in
  the tree.
- **The 20-clip sample was chosen to exercise the tiers**, not at random — 7/6/7 by design. The
  tier distribution is therefore *not* an estimate of the library's real mix.
- **`fallback_moods` was never exercised on real data**, because valence caught every clip in
  the sample. It is covered by unit test only.
- **Rotation evenness was measured on a store where every song shared one mood.** With mixed
  moods, a mood that matches few songs will concentrate use on those — even rotation is
  guaranteed *within* a mood, not across the library.
- **Nothing is wired to a renderer.** `render_plan()` returns the instruction; MEMEBOT-007 is
  the round holding the end-to-end path.
- **`song01.mp3`'s 162.54 s is from ffprobe**; the two template rows have `duration_s: null`
  until you fill them, so `validate()` cannot check their hooks.

---

## Method

Filed a claim (no path conflicts against three live rounds). Read MEMEBOT-003 and
`scratch/memebot003_song_library.json`, then built to that schema, keeping the sample's field
names so a store written against the spec loads unchanged. Duration measured with `ffprobe`.
The matcher proof reads **real records** from `clip_library/` through the shipping
`clip_library.iter_lines`/`field`, so absent values stay absent rather than becoming defaults.
Rotation evenness and determinism were measured by running `pick()` 50 and 2×12 times over
fresh loads. No API call, no spend, no edit to any existing clippershq module.
