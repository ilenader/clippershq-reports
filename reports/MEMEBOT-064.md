# MEMEBOT-064: it was never the audio codec — the renderer was trimming clips under a floor it was about to enforce

**Date:** 2026-08-02 · **Type:** Diagnose + fix · **Spend:** **$0.0192 of a $0.15 budget** · `memebot/scraper/edit.py` was FREE and is the only module changed

*Published as MEMEBOT-064: the round id MEMEBOT-063 is claimed, and `reports/MEMEBOT-063.md` was already taken by the time this was ready. Publishing under a claimed-but-occupied id overwrites another round's report, which MEMEBOT-061 hit yesterday.*

Acting on [MEMEBOT-061](https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/MEMEBOT-061.md), which fixed the bed path and left 17 of 42 renders failing on something else.

---

## 1. THE HYPOTHESIS WAS WRONG, and measuring it was the whole job

The brief offered: ~35.5% of clips carry an xHE-AAC profile ffmpeg 8.0 cannot decode. **REFUTED by measurement.**

| source audio profile | succeeded | failed | success rate |
|---|---:|---:|---:|
| **xHE-AAC** | **19** | 14 | 58% |
| HE-AAC | 6 | 3 | 67% |

**Nineteen of the twenty-five successes were xHE-AAC.** HE-AAC failed at a comparable rate. Nothing separated on codec, audio-stream count, video codec or sample rate either.

**Duration separates them perfectly:**

```
succeeded  n=25   min  9.7s   median 19.9s   max 79.9s
FAILED     n=17   min  5.1s   median  7.2s   max 10.1s
```

All 17 logged `edit:under-floor`. Not one was an audio failure.

### The mechanism

`edit.py` randomly **trims up to 1.5s off the head and 1.0s off the tail, and applies a speed of up to 1.08×** — anti-fingerprint transforms — and *then* enforces an 8.0s floor on the finished file. Nothing reconciled the two. The renderer trimmed clips below a floor it was about to check, did all the work, and refused its own output.

Measured finished/source ratios: **median 0.81**, range 0.54–0.97. A 10.05s source finished at 7.82s.

**Two numbers disagreed and neither knew it:**

```
clip_pipeline.gate   MIN_DURATION_S = 5.0     <- what is admitted
edit.py              floor_s        = 8.0     <- what is required
```

Clearing the floor from a worst-case roll needs **8.0 × 1.08 + 2.5 ≈ 11.1s** of source. The gate admits 5.0s. Of the 17 failures, **11 had sources already under 8.0s** — admitted by a gate that could not have produced a legal video — and **6 were above 8.0s and pushed under by the trim alone.**

---

## 2. THE FIX — spend the budget the clip actually has

`_floor_trim_budget()` in `edit.py`. Output length is `(src − trim_start − trim_end) / speed`, so total trim may not exceed `src − floor × speed`.

- When the rolled trims exceed the budget they are **scaled down proportionally**, not clipped to zero — the head:tail ratio of the roll survives, so the transform stays random and the anti-fingerprint intent is untouched.
- When even zero trim is not enough, the **speed walks down toward the configured minimum** (0.93× lengthens).
- When that still cannot reach the floor, the clip is genuinely too short and `assert_floor` refuses it — now the *only* reason a render is refused for length.
- **It never lengthens by looping or freezing.** `duration.py` forbids both; a test asserts the function contains neither.

**The floor is not weakened and the gate is not widened.** A 20s source still keeps its entire random trim (asserted).

### Result: 78.1%, from 59.5%, from a corrected 29.7%

| | historical | MEMEBOT-061 | **this round** |
|---|---:|---:|---:|
| records | 64 | 42 | **32** |
| ok | 19 | 25 | **25** |
| **success rate** | **29.7%** | 59.5% | **78.1%** |
| died on the bed path | 41 | 0 | **0** |
| died under-floor | — | 17 | **7** |

**All 7 remaining refusals are CORRECT.** Every one has a source under 7.63s — the minimum that can reach 8.0s even at the slowest configured speed:

```
5.18s  5.40s  5.41s  6.20s  6.39s  7.01s  7.22s      (all < 7.63s)
```

**Zero avoidable failures remain in this batch.** The residual loss is now entirely the gate/floor mismatch, and that lives in `clippershq/clip_pipeline.py`, **held by BL-899 for hours** — reported, not touched. Raising `MIN_DURATION_S` from 5.0 to ~8.0 would stop the pipeline paying to retrieve clips it can never ship.

---

## 3. EVERY OUTPUT VERIFIED BY MEASUREMENT, never an exit code

Two rounds have hit `status=no-match` at returncode 0 with an empty stderr, so an exit code is not evidence a video exists. All 25 were read off the artefact:

| check | result |
|---|---|
| file exists on disk | **25 / 25** |
| has an audio stream | **25 / 25** |
| **not digital silence** (`volumedetect`, peak > −60 dB) | **25 / 25** |
| **meets the 8.0s floor** | **25 / 25** |
| a render record matches | 25 / 25 |

Durations **8.17s / 16.77s / 76.61s** (min/median/max) — the minimum is now *above* the floor rather than under it. Levels **−24.3 to −13.0 dBFS mean**.

---

## 4. THE ERROR MESSAGE THAT COST FOUR ROUNDS

The refusal was **correct** and its message sent everyone to the wrong place:

```
ambient_bed.file='C:\...\clipper finder' was requested and does not exist
```

The real cause was a caller passing a **directory** — `os.path.join(cwd, "")` resolves to the repo root — and *"does not exist"* reads as a missing mp3. Four rounds looked for missing audio files. There were none.

It now names what the path **is**:

```
ambient_bed.file='C:\...\clipper finder' is a DIRECTORY, not an audio file. A caller almost
certainly joined an empty filename onto a folder — os.path.join(cwd, "") returns the folder
itself, and os.path.exists() is True for it. Check the producer of this path, not the audio.
```

with distinct wording for an **empty** path, a path that **exists but is not readable audio**, and one that genuinely **is not there**. An accurate refusal with a misleading message is worse than a vague one: it is confidently wrong, and it costs more than silence.

---

## 5. ROTATION AT EXHAUSTION — it falls back, then repeats. It never stops.

Measured two ways, because the answer differs by configuration:

**With the real 17-track corpus** — it **falls back to the LRU corpus at render #3** (confirmed in MEMEBOT-061; 7 of 12 leave the store).

**With no corpus** — it **repeats**, and says so:

```
 1 matched sng_0003  repeat_forced=False        8 matched sng_0003  repeat_forced=True
 2 matched sng_0004  repeat_forced=False        9 matched sng_0004  repeat_forced=True
 3 matched sng_0003  repeat_forced=True   <--  10 matched sng_0004  repeat_forced=True
 ...                                           14 matched sng_0004  repeat_forced=True

distinct songs used: 2 of 4      repeat_forced: 11 of 14
```

**It never stops and never errors.** It relaxes to "not the immediately previous track" and records `repeat_forced=True`, so the degradation is on the record rather than silent. That is the right behaviour.

**What the operator actually needs: more songs in the moods the library has — not a relaxed no-repeat rule.** Only **2 of the 4 songs are ever reachable**: `hype` carries 249 of 286 matches and `warm` 34, while `melancholy` matches 3 and `triumphant` matches **zero of 2,003 clips**. Relaxing no-repeat would not add variety; it would only make the repetition quieter. Two more `hype` tracks would do more than any rule change.

---

## 6. THE BASELINE CORRECTION, carried

**29.7% (19 of 64), not 36%.** The earlier figure was 19/53 and silently dropped 11 records that carried no status. Every comparison in this report uses 29.7%, which makes the improvement **larger** than the older figure implies: 29.7% → 78.1%.

---

## Proof

| check | result |
|---|---|
| residual defect named | `edit:under-floor` on 17/17; xHE-AAC hypothesis REFUTED by measurement |
| fix | `_floor_trim_budget`; **78.1%** vs 59.5%; 7 remaining refusals all CORRECT |
| every output measured | 25/25 exist, have audio, are not silence, clear the 8.0s floor |
| error message | names DIRECTORY / EMPTY / exists-but-unreadable / absent |
| rotation at exhaustion | falls back at #3 with a corpus; repeats with `repeat_forced=True` without one |
| **campaigns** | **`7a029ee5447cddd8` — MATCH**, unchanged |
| config | parses, 161 keys, `config_defaults` imports |
| **suites** | **ALL GREEN — 122/122, 4,413 checks** |
| spend | **$0.0192** of $0.15 |

### Concurrency

`claims_read.py --holders` reported `memebot/scraper/edit.py` and `config.yaml` **FREE** — this round changed only `edit.py`. `clippershq/clip_pipeline.py` is still held by **BL-899** (many hours); the gate/floor mismatch lives there and is reported rather than fixed. `git status --porcelain` distinguished ` M` (unstaged — my own `tests/test_clip_pipeline.py` from MEMEBOT-061) from `??` (untracked — BL-899's `test_clip_pipeline_gate.py`); neither was disturbed.

**A note on the claim itself:** it named `tests/test_edit_audio_profile.py`, because the claim was filed while the xHE-AAC hypothesis was still live. The measurement refuted it, so the test shipped as `tests/test_edit_duration_budget.py` — named for the defect that exists rather than the one that was predicted.

**And a third instance of a lesson I have now hit three times.** The first draft of `test_it_never_lengthens_by_looping_or_freezing` scanned `inspect.getsource()` for `"loop"` and failed on the function's own docstring, which says *"never lengthens by looping or freezing"*. A text scan cannot tell a prohibition from a use — the same shape as MEMEBOT-042's forbidden-field scan and MEMEBOT-049's resolver. It now parses the AST, strips the docstring, and inspects real string constants and names.

---

## What is next

1. **`MIN_DURATION_S` 5.0 → ~8.0** in `clip_pipeline.gate`, once BL-899 releases. It is the only remaining source of avoidable render loss, and it currently pays to retrieve clips that cannot ship.
2. **Two more `hype` songs.** One mood carries 87% of matches behind two usable tracks.
3. The 8.0s floor and the gate should read from **one constant**, not two that drifted 3 seconds apart.
