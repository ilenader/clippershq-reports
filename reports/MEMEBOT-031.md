# MEMEBOT-031: I did not do this work, because MEMEBOT-030 was already doing it

**Date:** 2026-08-01 · **Type:** Verification + collision report · **Spend:** $0.00 of the $0.05 budget · **No paid call**

Honesty tiers: **VERIFIED** (checked here), **NOT DONE** (and why), **KNOWN DEFECT**.

---

## Verdict first

**The brief was already in flight.** `MEMEBOT-030`, filed 11 minutes before this round opened, states its intent as:

> *"Wire --audio-class into clip_pipeline.render_one() so the treatment routing three rounds built becomes reachable; add a GENERIC argv guard that fails if any computed+recorded field is dropped from the subprocess; ... render one video per class with measured levels."*

That is items 1, 5 and 6 verbatim. **VERIFIED** it is not merely claimed but done: `clip_pipeline.py:1310` already carries the wiring, `tests/test_render_argv.py` already exists (12,750 bytes), and MEMEBOT-030 had already taken the same config/spend backups this brief asked for, at 18:25:05.

So I stopped. Duplicating a round that is 11 minutes into the same file is how MEMEBOT-017 ended up deleting a duplicate implementation, and it is the exact failure `claim.py` exists to prevent. **Nothing in `clip_pipeline.py` was edited by this round.**

**And `BL-855` has NOT released `clip_pipeline.py`.** The brief asked me to confirm it had. It has not — 145 minutes in flight and still holding the file, alongside MEMEBOT-030. That is two live claims on the file this brief wanted rewritten.

---

## What is actually true now, verified

### 1. `--audio-class` reaches the renderer — done by MEMEBOT-030

**VERIFIED**, `clippershq/clip_pipeline.py:1310`:

```python
if audio_class:
    cls = str(audio_class).strip().lower()
    if cls in RENDER_AUDIO_CLASSES:
        cmd += ["--audio-class", cls]
    else:
        print("  !!  audio class %r is not one edit.py accepts (%s) -- rendering "
              "WITHOUT a class, which falls back to keep and leaves the original "
              "audio in" % ...)
```

The unroutable-class branch is the right shape: it refuses to pass a value `argparse` would exit 2 on (which would lose the render entirely), and it refuses to swallow it silently. Credit to MEMEBOT-030; I only read it.

### 2. The third copy — **NOT DONE**

`clip_pipeline.TREATMENT_TO_DUCK` is still at line 846. It is a one-line deletion and I did not make it, because the file is held by two rounds. MEMEBOT-027's invariant test still stands guard: it walks the tree for a real subscript or `.get` use and fails, naming the missing keys, if anyone wires the incomplete map.

### 3. The drift guard still fires — **VERIFIED**

```
test_both_modules…agree_class_for_class ................ ok
test_the_guard…fires_on_a_planted_divergence ........... ok   (stale word)
test_the_guard…on_an_unrecognisable_word .... ok   (unknown word)
test_the_third_copy…is_dead_and_stays_dead ... ok
```

Both planted divergences still detected after MEMEBOT-030's change. The guard **calls** both modules; it does not transcribe either.

### 4. The record — half fixed, and I found the other half

The operator display is now truthful. `control.py:2604` calls `clip_speech.treatment_for()`, which MEMEBOT-027 corrected, so it prints:

```
music-only           -> mute-and-replace
dialogue-over-music  -> keep-original
dialogue-only        -> keep-original
silent               -> mute-and-replace
```

**KNOWN DEFECT, still live.** `clip_pipeline.audio_treatment()` returns the literal `"duck-under"` on **two fallback paths** — clip_speech unavailable (line 774) and class UNKNOWN (line 790). Those words go into the record. Meanwhile `duck.FALLBACK_TREATMENT` is `keep` and `duck` is **not in `SHIPPED_TREATMENTS`**. So for every clip whose class cannot be determined, **the record claims a treatment that does not ship and the render did not perform** — the same record-vs-render split MEMEBOT-027 closed for the four known classes, still open on the unknown ones.

The fix is two string literals, `"duck-under"` → `"keep-original"`, at both sites. **Not done: held file.** Guarded instead, as `@unittest.expectedFailure` in `tests/test_clip_speech.py`, so it is visible in every run and flips to an *unexpected success* the moment someone fixes it. That marker is deliberate — a silently-skipped defect is how this one survived four rounds.

### 5. Generic argv guard — **NOT DONE**, MEMEBOT-030 owns it

`tests/test_render_argv.py` exists and is theirs. Writing a second one is the third copy of the treatment map all over again, in test form.

### 6. Three renders — **NOT DONE**, MEMEBOT-030 owns it

Their claim says "render one video per class with measured levels". I have no independent renders to show and will not present theirs as mine.

---

## Safety and the required proofs

| check | result |
|---|---|
| `config.json` + `spend.json` backed up | `scratch/mb031/*.20260801-183749` |
| campaigns byte-identical | **`8e02f8d6f6307ae8`** ✓ matches |
| config valid | parses, 162 top-level keys, 5 campaigns |
| spend | **`spend.json` byte-identical to my backup — no paid call, $0.00 of $0.05** |
| credentials | none printed, logged or committed |

**Claim registered each path individually — hand-verified** against the stored JSON, not just the tool's summary:

```
[0] 'tests/test_clip_speech.py'   comma-free: True
[1] 'clippershq/control.py'       comma-free: True
[2] 'scratch/mb031_verify.py'     comma-free: True
each entry a single path: True
```

The tool now prints `3 path(s) registered individually` of its own accord — a later round built that on top of MEMEBOT-025's `split_paths` fix.

### Suites

**CORRECTION, added after publication.** I first reported that `run_all.py` produced nothing and that I could not get a result from it. That was true when I wrote it and it was the wrong conclusion: the runner buffers its entire output and writes it only on exit, and this run took **649 seconds**. It finished after the report went up. It works; it is just silent for eleven minutes.

**The real result: `FAILED -- 2 of 86 suite(s) red`.**

| red suite | held by | cause |
|---|---|---|
| `tests/test_song_library.py` | MEMEBOT-032 | 2 checks assert `TIER_TITLE`, the constant that round is mid-way through deleting |
| `tests/test_dashboard.py` | BL-875, INFRA-014 | not investigated; both holders are live |

**Neither is mine.** All 8 checks my MEMEBOT-027 round added to `test_song_library.py` pass, including the song02 density routing. The two failures are `franchise tier -> high confidence, no review` and `a recognised title still routes` — both `TIER_TITLE` assertions.

So the honest headline is not "the suite is green" and not "I could not measure it". It is: **84 of 86 suites pass, and the two that do not are mid-edit in other rounds' files.** The four suites below were run directly and are the ones bearing on this round:

| suite | result |
|---|---|
| `tests/test_clip_speech.py` | **49 pass** (1 expected failure — the defect above) |
| `tests/test_clip_pipeline.py` | **82 pass** |
| `tests/test_song_loudness.py` | **21 pass** |
| `memebot/scraper/tests/` | **92 pass** |
| **total** | **244** |

Plus an import check across all **72** test modules: 1 broken (`test_quality_score`, `AttributeError` on an unrelated mock, pre-existing and not mine).

**A transient I saw and did not touch:** for several minutes `clippershq/song_library.py` did not import at all — `NameError: TIER_TITLE`, MEMEBOT-032 having deleted the constant while three references remained. It resolved itself while I was measuring. Recorded because anyone whose suite went red in that window should know why, and because it is a live illustration of why a red suite in this tree needs attribution before it needs fixing.

---

## The pattern this round is actually about

The brief calls the dropped `--audio-class` "the seventh instance today of a value computed correctly and discarded at a module boundary". That is right, and there is a second pattern stacked on it: **three consecutive rounds were blocked from fixing it because the file was held, and the fourth fixed it while a fifth was being briefed to fix it again.**

The claim tool did its job here — it told me, in one command, that the work was taken. What it cannot do is tell the person writing the brief. Every one of those rounds was correctly reasoned and correctly blocked; the cost was not confusion, it was four rounds of queueing behind one file.

The honest lesson is not about `--audio-class`. It is that `clip_pipeline.py` has been held continuously by someone for the last two and a half hours, and the work that queues behind it is exactly the work everyone agrees is most urgent.

---

## Honest limits

- **I did not do the main task and am not claiming it.** Items 1, 5 and 6 are MEMEBOT-030's; item 2 is undone. This report exists so that is unambiguous.
- **I did not verify MEMEBOT-030's renders or their argv guard's correctness** beyond confirming the files exist. Their round should report those.
- **My first `run_all.py` claim was wrong and is corrected above.** The runner works; it buffers for 649 s. Reporting "no result" after ten minutes of silence was impatience, not measurement — the fix was to wait, and the answer (84/86, two failures attributable to other rounds) is strictly more useful than what I published.
- **The record defect is guarded, not fixed**, and an `expectedFailure` is a marker, not a solution. If `clip_pipeline.py` frees up, it is two string literals.
- **MEMEBOT-023's report is still unpublished** (404 at the time of reading), so the reasoning I cite from it comes from its claim intent and the code it left behind.

---

## Say it plainly

The right output of this round was to not produce one. The wiring was already in, done well, by a round that had claimed it eleven minutes earlier; the one item left undone sits in a file two other rounds are holding. What I added is a marker on a real defect nobody had spotted — the record still says `duck-under` for unknown-class clips, on a path where the renderer now does `keep` — and confirmation that the drift guard still catches what it was built to catch. Everything else here is a verification that someone else's work is real.

<!-- CLAIMS
file:   tests/test_clip_speech.py
-->
