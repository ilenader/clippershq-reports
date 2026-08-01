# MEMEBOT-025: The song store is normalised — and the same wrong-reference bug had one more level in it

**Date:** 2026-08-01 · **Type:** Implementation + measurement · **Spend:** $0.00 · **No paid call**

Honesty tiers: **VERIFIED** (measured here), **CORRECTION**, **JUDGEMENT** (a threshold I chose), **GAP**.

---

## Verdict first

Every track in the store is measured once and corrected to a **target** (-14 LUFS, -1.0 dBTP ceiling) instead of by a chosen gain. The loudness spread across the store falls from **2.7 LU to 0.1 LU**. MEMEBOT-021's open item is closed: the muted render now lands **+0.6 LU** from the clip it replaced, against **-13.3 LU** uncorrected.

Three things beyond the brief:

1. **The bug had one more level.** A target correction derived from the WHOLE FILE and applied to the WINDOW a render actually plays is still a gain against the wrong reference. song01 is -9.5 LUFS whole-file and **-17.9 LUFS over the 19 s the render used** — 8.3 LU apart. The whole-file correction landed 7.9 LU low and nothing failed. The correction is now measured over the window.
2. **The claim tool was genuinely mis-parsing, and it was hiding a live conflict.** Fixed, with the before/after on the actual claim that was invisible.
3. **All four tracks already clip** — true peaks of **+0.4 to +1.9 dBTP**. One track's correction is capped by the ceiling and reports the shortfall rather than absorbing it.

---

## Part 1 — The claim tool (instruction 5). It was really broken.

**VERIFIED.** `--write` is `action="append"`, so `--write "a.py,b.py"` stores the whole string as ONE path, and `conflicts()` compared whole strings. At the time of the fix **2 of 9 live claims were in that shape**.

The live proof, run against the real `.claims/` directory:

```
old (whole-string compare): [('MEMEBOT-024', 'memebot/scraper/edit.py')]
new (split both sides)    : [('MEMEBOT-023', 'memebot/scraper/edit.py'),
                             ('MEMEBOT-024', 'memebot/scraper/edit.py')]
```

**MEMEBOT-023 was holding `duck.py, edit.py, config.yaml, tests/test_duck.py` as one string and was invisible.** It is the round that rewrote all four files during this one. A tool whose entire purpose is "who is doing what right now" was answering "nobody", with confidence.

`split_paths()` splits on **both sides** — on write so new claims are stored correctly, and inside `conflicts()` so claims **already on disk** in the broken shape are matched. Fixing only the writer would have left every in-flight claim invisible until it ended, which is exactly when the information stops being useful. `tests/test_claim.py` gains checks for both halves, including a hand-planted broken record on disk. **30 checks, ALL PASS.**

---

## Part 2 — Every song measured, before and after

**VERIFIED.** One ffmpeg `loudnorm` analysis pass per track (5.4–13.8 s each), cached in `scratch/song_loudness.json` keyed by repo-relative path + size + mtime.

| track | BEFORE | AFTER | gain | true peak | LRA | occupancy |
|---|---|---|---|---|---|---|
| song01.mp3 | **-9.5 LUFS** | -14.0 | -4.47 dB | **+1.5 dBTP** | 11.5 LU | 0.43 |
| song02.mp3 | **-12.2** | -14.1 | -1.90 | **+0.9** | 3.0 | 0.68 |
| song03.mp3 | **-10.4** | -14.0 | -3.64 | **+1.9** | 8.4 | 0.44 |
| song04.mp3 | **-9.5** | -14.0 | -4.53 | **+0.4** | 8.9 | 0.39 |

**Loudness spread across the store: 2.7 LU → 0.1 LU.**

**Every one of the four already clips.** True peak above 0 dBTP means the files are over full scale before anything is done to them. song02 could not be brought all the way to target without going further over the -1.0 dBTP ceiling, so its correction is capped at -1.90 dB and the row records *"the track lands 0.1 LU under target"* rather than claiming the target. A capped correction that quietly claimed success would be the same failure in a new costume.

**GAP:** nothing here limits or re-masters. The tracks are the operator's and are left untouched; a track that clips still clips, and only the *level* is corrected.

---

## Part 3 — The level the brief did not know was there

**VERIFIED, and this is the finding.** A render plays a *window* of a track, not the track. song01:

| span | integrated |
|---|---|
| whole file (162 s) | **-9.5 LUFS** |
| first 20 s (the intro) | **-17.2 LUFS** |
| 60–80 s | -7.1 |
| 120–140 s | -7.1 |

The intro is **7.7 LU** quieter than the body. Correct the FILE to -14 and render the INTRO and you land at -21.8 LUFS — and the render succeeds, the arithmetic is right, and the reference is wrong. That is the fourth instance of the same shape, after MEMEBOT-007's -49 dB placeholder, MEMEBOT-021's -48.9 dB clip-mean, and MEMEBOT-021's -28.8 dB solo gain.

So `measure()` and `measurement_for()` take `start_s`/`end_s`, and the window is part of the cache identity — one row per file would hand a window the file's correction. The store is built around hook windows, so the window is the right unit.

### The proof (instruction: a muted render at a comparable level)

Real music-only clip, real track, `mute` treatment, three renders differing only in the gain:

| correction derived from | gain | output | vs the clip it replaced |
|---|---|---|---|
| nothing (MEMEBOT-021 behaviour) | -10.00 dB | -27.3 LUFS | **-13.3 LU** |
| the WHOLE FILE | -4.47 dB | -22.0 LUFS | -7.9 LU |
| **the WINDOW played** | **+3.49 dB** | **-13.5 LUFS** | **+0.6 LU** |

The clip was -14.1 LUFS. Note the corrected gain is **positive** — the window needed lifting, while the whole file needed attenuating. A whole-file correction pushed it the wrong way.

---

## Part 4 — Which songs can sit under dialogue

MEMEBOT-021 measured the **clip** side: a median **+2.9 dB** speech-to-bed gap across real dialogue-over-music clips, one clip **negative**. This is the **song** side — whether a track can use the room a clip leaves.

**VERIFIED** measurements; the dense/sparse **thresholds are JUDGEMENT** and are labelled as such in the code:

| track | LRA | p10–p90 spread | occupancy | can sit under dialogue |
|---|---|---|---|---|
| song01 | 11.5 LU | 16.5 dB | 0.43 | **YES** |
| song02 | **3.0 LU** | 8.0 dB | 0.68 | **NO — dense** |
| song03 | 8.4 | 13.2 dB | 0.44 | YES |
| song04 | 8.9 | 15.0 dB | 0.39 | YES |

**One of the four cannot go under dialogue at all.** song02 is a compressed wall of sound: it sits at one level continuously and leaves a voice nowhere to be.

And the clip can veto regardless of the song — against a negative-gap clip, `can_sit_under_dialogue()` returns NO for every track, because that is a property of the clip and no song however sparse can fix it.

**GAP:** the thresholds (LRA ≤ 5.0 LU, occupancy ≥ 0.80) are conventional figures, not validated by listening here.

---

## Part 5 — Did MEMEBOT-021's reconciliation hold? (instruction 4)

**Mostly, and one part was deliberately overturned by a round that ran during this one.**

| what | state |
|---|---|
| bed level and treatment both routing from the four-way class | **held** |
| `mode: auto` routing on class, not source loudness | **held** |
| dialogue bed at -8..-5 dB | **held** (`BED_OFFSET_DIALOGUE_DB = (-8.0, -5.0)`) |
| `volume_mode: auto`, `treatment: auto` | **held** |
| `relative_basis()` preferring the speech level | **held** |
| duck.py and `clip_speech.treatment_for()` agreeing class-for-class | **NO LONGER TRUE** |

MEMEBOT-023 demoted ducking (`DUCK_ENABLED_DEFAULT = False`) on its own measurement that no setting reaches 4 dB on real material, and routed both dialogue classes to `keep`. So:

```
music-only          -> mute | clip_speech: mute-and-replace | agree
dialogue-over-music -> keep | clip_speech: duck-under       | DISAGREE
dialogue-only       -> keep | clip_speech: duck-under       | DISAGREE
silent              -> mute | clip_speech: mute-and-replace | agree
```

The drift guard I added in MEMEBOT-021 **fired** — I observed 8 of 72 scraper tests red mid-round, all in `test_duck.py`. MEMEBOT-023 then updated them and the suite is green at **86 tests**. The guard did its job; what it caught was an intentional change, not a mistake. **But the divergence itself is still live**: `clip_speech.treatment_for()` still says `duck-under` for both dialogue classes and nothing in the renderer will ever do that now. Two modules disagreeing about the same decision is how MEMEBOT-015 happened. I did not touch either file — both were held — so this is **reported, not fixed**.

---

## Concurrency, which was the whole texture of this round

Four rounds wanted the files I did:

- **MEMEBOT-023** and **MEMEBOT-024** were both inside `memebot/scraper/edit.py`.
- **MEMEBOT-022** was inside `song_library.py`, `songs.json` and `tests/test_song_library.py`.

So none of them was touched. Loudness is a separate concern from mood matching, so it went into a **new module** (`clippershq/song_loudness.py`) with its own cache, and the correction reaches the renderer through the gain knob `ambient_bed` already takes. Nothing held by another round had to change — which is also why the fix works without a renderer edit at all.

I re-filed my own claim once, after discovering MEMEBOT-022's hold, to name the real paths rather than the ones I first guessed.

---

## Two things I got wrong in this round, both the same shape

1. **`ambient_bed.file` resolves against `memebot/`, not the repo root** — despite the config comment saying repo-root-relative. I made the cache keys repo-relative for portability, passed one of those keys straight into the render config, and got three renders whose numbers were *non-monotonic* (a +3.5 dB gain producing a quieter output than a -10 dB one) because none of them had a bed at all. edit.py does warn on stdout; my bench swallowed it.
2. **My guard against that then produced a false positive**: it searched the whole stdout for `"skipped"`, which matches the summary line `skipped=0`, and rejected three good renders. A check against the wrong reference — in the round about checks against the wrong reference.

Both are fixed and both are commented at the site. The bench now inspects the `ambient_bed` line specifically and refuses to report a number when the bed did not engage.

---

## Tests

| suite | result |
|---|---|
| `tests/test_song_loudness.py` | **21 pass** (new) |
| `tests/test_claim.py` | **30 checks, ALL PASS** (4 new for the split fix) |
| `memebot/scraper/tests/` | **86 pass** |
| **total** | **137** |

The loudness tests cover the structural defence directly: `gain_for_target()` raises `MeasurementMissing` rather than defaulting, and the refusal names the failure it prevents. One test exists only to record that the fixture's own -6.0 dBTP peak caps a +6 dB lift to +5 dB — a trap this test file fell into first.

---

## Honest limits

- **I cannot listen.** Every number here is a measurement. -14 LUFS is a platform convention, not something verified by ear on this material.
- **The density thresholds are judgement.** LRA ≤ 5.0 and occupancy ≥ 0.80 are conventional; the *measurements* are real, the *verdict line* is a heuristic a human should overrule freely.
- **Four tracks.** The store is small and all four already clip, which may say more about how they were produced than about anything general.
- **Nothing is limited or re-mastered.** A clipping track still clips; only its level is corrected, and one track cannot reach target because of it.
- **The window correction needs a window.** All four hook windows in `songs.json` are placeholders with `enabled: false` on purpose, so today nothing supplies one and callers get the whole-file figure — which Part 3 shows can be 8 LU wrong. Wiring the store's hook windows into the correction is the obvious next step and was **not** done here: `songs.json` is held by MEMEBOT-022.
- **The duck.py / clip_speech divergence is live and unfixed**, for the same reason.
- **Renders and clip-side figures cited from MEMEBOT-021 carry its caveats**: the 61-clip corpus is 80.3% music-only with **zero dialogue-only clips** against the library's 51.9/43/7.6, and that round's dialogue-only render was **constructed**, so the class's real behaviour remains unmeasured.

---

## Say it plainly

The store is normalised and the muted render lands where it should. The more useful result is that the bug the brief asked me to close had one more level in it than the brief knew, and I then reproduced the same mistake twice more inside a single afternoon — once resolving a path against the wrong root, once matching a substring against the wrong line. That is four instances across four rounds of one thing: **arithmetic against a reference nobody checked**. The defence that actually works is not care, it is structure — a correction that cannot be produced without a measurement, and a measurement that carries the span it was taken over.

<!-- CLAIMS
file:   clippershq/song_loudness.py
file:   tests/test_song_loudness.py
func:   clippershq/song_loudness.py::measure
func:   clippershq/song_loudness.py::gain_for_target
func:   clippershq/song_loudness.py::resulting_lufs
func:   clippershq/song_loudness.py::measurement_for
func:   clippershq/song_loudness.py::window_key
func:   clippershq/song_loudness.py::is_dense
func:   clippershq/song_loudness.py::can_sit_under_dialogue
const:  clippershq/song_loudness.py::TARGET_LUFS
const:  clippershq/song_loudness.py::TRUE_PEAK_CEILING_DBTP
func:   tools/claim.py::split_paths
file:   tools/claim.py
-->
