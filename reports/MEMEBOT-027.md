# MEMEBOT-027: One answer in both files — and the guard that was supposed to catch this had been replaced by a copy of itself

**Date:** 2026-08-01 · **Type:** Implementation · **Spend:** $0.00 · **No paid call**

Honesty tiers: **VERIFIED** (measured/run here), **JUDGEMENT** (a threshold chosen, not validated by ear), **GAP**.

---

## Verdict first

`clip_speech.treatment_for()` now says **keep-original** for both dialogue classes, matching what `duck.py` has actually done since MEMEBOT-023, and `duck.py` gains the alias that makes the pair coherent. **Both edits are required; neither is safe alone**, and the new guard proved that within seconds of the first one landing.

Three things beyond the brief:

1. **The drift guard had already been replaced by something that cannot detect drift.** MEMEBOT-023 swapped the equality check for a test that pins the divergence as deliberate — by **hardcoding a copy of clip_speech's table instead of calling it**. A copy drifts with you. It passed happily while the two modules disagreed, and it would have gone on passing after I changed one of them.
2. **A third copy of the same vocabulary map exists**, `clip_pipeline.TREATMENT_TO_DUCK`, and it is now **incomplete** — no entry for `keep-original`. It is dead code today. It is also the exact shape that broke in MEMEBOT-015.
3. **Hook windows drift from their own files by -4.8 to +2.6 LU**, and two windows of the *same track* need corrections **5.9 dB apart**. A per-file correction cannot be right for both.

---

## Part 1 — The divergence, and why half of it was not safe

`duck.py` closed ducking on measurement in MEMEBOT-023 (23 settings over 11 real clips, none reaching 4 dB; at ratio 20 the threshold cancels and the dip reduces to the clip's own speech-to-bed contrast, r = 0.920, 0 of 11 clips beating their own contrast, one ducking backwards). `clip_speech.treatment_for()` kept saying `duck-under` for another two rounds.

**The render was never wrong** — `duck.py` gates an explicit duck request, so a stale word could not produce a duck. What was wrong was **everything downstream of the word**:

- `control.py:2604` prints `treatment_for(cls)` to the operator, per class. It was reporting `duck-under` for clips the system renders `keep`.
- `clip_pipeline.audio_treatment()` returns that word **into the record**.

So the render was right and the evidence was wrong. That is the MEMEBOT-015 shape with the blast radius moved from the output to the record, which is harder to notice and outlives the render.

**VERIFIED, the pair.** Changing `clip_speech` alone put `keep-original` into a table `duck.py` had never heard of. The new guard failed immediately:

```
AssertionError: 'keep-original' not found in {'mute-and-replace': 'mute',
  'duck-under': 'duck', 'replace': 'mute', 'mix': 'keep'} : duck.py cannot resolve
  clip_speech's word 'keep-original' for dialogue-over-music -- this is the MEMEBOT-015
  boundary: an unrecognised word does not raise, it falls back, and the render
  succeeds with the wrong treatment
```

`"keep-original": TREATMENT_KEEP` closes it. **`"duck-under" stays in the alias table** — ducking is disabled, not deleted, and re-enabling it should be a config flag rather than a vocabulary migration.

---

## Part 2 — The guard, and the guard's own failure mode

The test MEMEBOT-023 left behind, `test_routing_diverges…_DELIBERATELY`, hardcoded what it believed the upstream module said:

```python
upstream = {duck.CLASS_DIALOGUE_OVER_MUSIC: "duck-under", ...}   # a COPY, never called
```

It was true when written. It stopped being true the moment `clip_speech` moved, and **it kept passing throughout** — a copy cannot detect drift because it drifts with you. That is a real lesson about guards, not a criticism of the round: the divergence it documented was a deliberate decision, and pinning it was reasonable. Pinning it *by transcription* was the mistake.

**Shipped instead:** `tests/test_clip_speech.py::TestNoTreatmentDrift`, which **calls both modules** and compares live values.

**VERIFIED, it fires.** Three tests, not one:

| test | plants | result |
|---|---|---|
| `test_both_modules…agree_class_for_class` | nothing | passes; **failed for real** on the missing alias before duck.py was updated |
| `test_the_guard…fires_on_a_planted_divergence` | `clip_speech` → `duck-under` while duck.py routes `keep` — i.e. exactly the state MEMEBOT-023 left | guard raises ✓ |
| `test_the_guard…on_an_unrecognisable_word` | a word duck.py has never heard (`silence-it`) — the MEMEBOT-015 half | guard raises ✓ |

It **skips** rather than fails when `memebot/` is absent, because that tree is gitignored and a checkout without it must not turn a real suite red.

MEMEBOT-023's test is replaced by `test_the_disabled…vocabulary_is_still_recognised`, which keeps the part that is genuinely duck.py's own business — the disabled vocabulary must survive — and drops the transcribed copy.

### The third copy

`clip_pipeline.TREATMENT_TO_DUCK` translates the same vocabulary a second time. **VERIFIED it has no consumer** outside its own tests, and it now lacks `keep-original`. Harmless while dead; the moment anything routes through it, both dialogue classes fall off the end of the map.

`clippershq/clip_pipeline.py` was held by BL-855, so it was not edited. Instead the invariant is policed: `test_the_third_copy…is_dead_and_stays_dead` walks the tree for a real subscript/`.get` use and fails with the missing keys named if anyone wires it. **The one-line fix is to delete the map** in favour of `duck.TREATMENT_ALIASES` — recommended, not done.

---

## Part 3 — Hook windows wired

**VERIFIED.** All 8 windows across the 4 songs measured once and written into the song record, per window:

| song | window | LUFS | gain to target | drift vs its own file |
|---|---|---|---|---|
| song01 | h1 20–25 s | -14.3 | **-0.88 dB** | -4.8 LU |
| song01 | h2 60–65 s | -7.2 | **-6.76 dB** | +2.3 LU |
| song01 | h3 110–116 s | -14.0 | -0.03 dB | -4.4 LU |
| song02 | h1 30–36 s | -12.4 | -1.56 dB | -0.3 LU |
| song03 | h1 45–51 s | -9.8 | -4.20 dB | +0.6 LU |
| song04 | h1 15–21 s | -13.3 | -0.74 dB | -3.8 LU |
| song04 | h2 55–61 s | -8.0 | -5.98 dB | +1.5 LU |
| song04 | h3 95–101 s | -6.9 | -7.12 dB | +2.6 LU |

**song01's h1 and h2 need corrections 5.9 dB apart.** One per-file number cannot serve both, which is the MEMEBOT-025 finding stated as a range rather than a single example.

**Where the line is.** `songs.json` opens with *"Edit this file by hand — nothing infers any value in it"*, and that rule is load-bearing — an inferred hook window is the BL-690 fabrication. So everything written goes inside a `measured` block, per song and per hook, marked machine-owned and regenerable. Nothing outside those blocks is touched.

**The windows are still placeholders**, all four songs `enabled: false`. Measuring a placeholder span is honest arithmetic about a real span; the correction belongs to *that* span, and because the loudness cache is keyed by `(path, size, mtime, window)`, re-marking a window simply fails to match and the correction re-derives. That self-invalidation is the only reason writing a correction next to a placeholder is safe at all.

---

## Part 4 — song02 cannot sit under dialogue, and the matcher now knows

**VERIFIED:** song02 measures **LRA 3.0 LU** and sits within 3 dB of its own ceiling **68%** of the time. The other three measure LRA 8.4–11.5 with occupancy 0.39–0.44.

MEMEBOT-021 measured the other side: a dialogue clip leaves a median of **+2.9 dB** under its own speech, and one clip leaves **negative** room. A wall of sound put there covers the voice wherever it sits.

`song_library.can_use_for_class()` reads `measured.can_sit_under_dialogue` from the record, and `pick()` takes an optional `audio_class` and drops blocked candidates **before** the least-used tie-break — filtering afterwards would let rotation return the one song that cannot be used and call it the answer. With nothing left, the clip **parks**: *never force a match*.

Two deliberate non-behaviours, both tested:
- **An unmeasured song is allowed**, not assumed dense. Absence of a measurement is not evidence, and withholding every unmeasured song would empty a four-song rotation.
- **A withheld song is not counted as used** — a rejected candidate must not have its rotation counter bumped.

**JUDGEMENT:** the thresholds (LRA ≤ 5.0 LU, occupancy ≥ 0.80) are conventional figures and are **not validated by ear**. The verdict lives in the song record rather than in code precisely so an operator who disagrees can overrule it by editing one field.

---

## Part 5 — MEMEBOT-025's two mistakes, recorded at their sites

1. **`ambient_bed.file` resolves against `memebot/`, not the repo root** its own docstring claims — `ROOT` is `memebot/scraper`, so `ROOT.parent` is `memebot/`. A genuinely repo-relative path resolved to `memebot/memebot/...`, found nothing, and produced three renders with no bed at all whose numbers were non-monotonic. Recorded in `memebot/scraper/edit.py::pick_ambient_file`, where the resolution happens.
2. **A guard searched all of stdout for `"skipped"`**, which matches the summary line `skipped=0`, and rejected three good renders. Recorded at the check in `scratch/mb025_loudness.py`, and the family lesson added to `song_loudness.py`'s docstring — which now lists **five** instances of one bug: correct arithmetic against a reference nobody checked.

---

## Concurrency

MEMEBOT-022 and MEMEBOT-025 had released before this round opened. **MEMEBOT-023 had not** — it held `duck.py`, `edit.py`, `config.yaml` and `test_duck.py`, so the round began by changing only `clip_speech.py` and building the guard, which is what surfaced the missing alias. MEMEBOT-023 and MEMEBOT-024 both released mid-round; the claim was re-filed each time the scope genuinely changed, four times in total, so the registry never described work that was not happening.

`claim.py` reported paths correctly throughout — MEMEBOT-025's `split_paths` fix is in place and another round has since built `validate_paths`/`paths_overlap` on top of it.

---

## Tests

| suite | result |
|---|---|
| `tests/test_clip_speech.py` | **48 pass** (4 new: the live guard + two planted divergences + the dead-map invariant) |
| `memebot/scraper/tests/` | **90 pass** |
| `tests/test_clip_pipeline.py` | **82 pass** (unchanged by the new word) |
| `tests/test_song_loudness.py` | **21 pass** |
| `tests/test_song_library.py` | **121 checks, ALL PASS** (3 new) |
| `tests/test_claim.py` | **ALL PASS** |
| **unittest total** | **241** |

---

## Honest limits

- **I cannot listen.** Every verdict here is a measurement; the dense/sparse thresholds are conventional figures applied to real numbers, not something checked by ear.
- **The hook windows are placeholders.** Their corrections are arithmetically right for spans nobody chose. The cache invalidates them the moment a window is re-marked, which is the safeguard, but no window in this store has yet been marked by ear.
- **`clip_pipeline.TREATMENT_TO_DUCK` is left incomplete**, policed rather than fixed, because its file was held.
- **The bigger live gap is untouched and is not mine to close:** `clip_pipeline` computes the audio class and then calls the renderer **without `--audio-class`**, so class routing is unreachable from the pipeline that matters — every clip through it takes the no-class fallback. MEMEBOT-023 recorded this in `duck.py` and measured the consequence: BL-853 put ~51.9% of the library music-only and MEMEBOT-020's VAD put the local downloads at 80.3%, and **every one of those should mute and instead keeps its original song**. That is the copyright-shaped failure, arrived at by omission. `clip_pipeline.py` is held by BL-855.
- **Figures carried from earlier rounds keep their caveats**: the 61-clip corpus is 80.3% music-only with **zero dialogue-only clips** against the library's 51.9/43/7.6, and MEMEBOT-021's dialogue-only render was **constructed**, so that class's real behaviour remains unmeasured.

---

## Say it plainly

The divergence itself was two lines. What took the round was that the mechanism built to catch it had been quietly replaced by a transcription of the thing it was checking, and a third copy of the same map was sitting one module away, already incomplete. One decision was being stored in three places and guarded by a photograph of one of them. The fix that matters is not the word `keep-original` — it is that a test now calls both modules, has been watched failing on a real divergence and on two planted ones, and that the surviving third copy will fail loudly the moment anyone tries to use it.

<!-- CLAIMS
func:   clippershq/clip_speech.py::treatment_for
const:  clippershq/clip_speech.py::TREATMENT_BY_CLASS
func:   clippershq/song_library.py::can_use_for_class
const:  clippershq/song_library.py::DIALOGUE_CLASSES
file:   clippershq/clip_speech.py
file:   clippershq/song_library.py
file:   clippershq/song_loudness.py
file:   tests/test_clip_speech.py
file:   tests/test_song_library.py
-->
