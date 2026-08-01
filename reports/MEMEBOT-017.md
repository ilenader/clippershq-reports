# MEMEBOT-017 — One loop, one ledger, one writer. `loop_runner.py` is retired into `clip_pipeline.py`, and the join key that makes the feedback loop work was **one line away from silently never matching**

**Date:** 2026-08-01 · **Type:** Reconciliation + live proof · **Spend:** **$0.0006 · 1 paid call** (the proof render). Budget was $0.05; **1.2% of it was used.**
Claim `MEMEBOT-017` filed before the first edit, with the `loop_runner.py` conflict declared in the claim text. Config, `spend.json`, `memebot/scraper/config.yaml` and the ledger were backed up to `scratch/memebot017_backup/` first. Per-file mtime guard held before every deletion. **No credential was printed, logged or committed.**

Honesty tiers: **VERIFIED** (measured this round), **CORRECTION**, **GAP** (not measured).

---

## Verdict first

**`clippershq/clip_pipeline.py` survives. `clippershq/loop_runner.py` and `tests/test_loop_runner.py` are deleted** (archived to `scratch/memebot017_retired/` so the deletion is reversible).

**The ledger is `memebot/runs.jsonl`. The writer is `memebot/scraper/run_record.py`. The reader is `outcome_loop`.** `scratch/renders.jsonl` — the second ledger MEMEBOT-010 was writing — is migrated and retired.

```
1. ONE IMPLEMENTATION            OK  loop_runner.py + its tests deleted, archived, guarded
2. THE THREE FIXES               OK  all present, each with a regression test
3. ONE LEDGER, ONE WRITER        OK  11 renders, both readers resolve the same 11
4. THE LOOP CLOSES               OK  render -> outcome -> bias key, byte-identical
5. SAFETY                        OK  campaigns 8e02f8d6f6307ae8, config 162 keys
ALL GREEN (0 check(s) failed)        -- scratch/memebot017_verify.py, re-runnable
```

**Suites: 65/65 green, 2,824 checks.** `tests/test_clip_pipeline.py` is now **82 tests**. One video rendered end to end through the surviving path for **$0.0006**; a second was then rendered by *another round* using the same path, which is better evidence than my own.

**The finding that matters most is not the deduplication.** It is what the merge nearly did to the feedback loop, and it is in §4.

---

## 1. The comparison

| | `clip_pipeline.py` (MEMEBOT-010) | `loop_runner.py` (MEMEBOT-015/018) |
|---|---|---|
| lines | 1,418 | 340 → 24 KB |
| renders via | **`edit.py` as a subprocess** | **`ffmpeg` directly** |
| captions burned in | **yes** (`drawtext`, template) | **no** |
| template / canvas | **yes** (`white_frame`, 1080×1920) | no |
| anti-fingerprint transforms | **yes** (zoom, EQ, grain, CRF…) | **no** |
| ducking (`duck.py`) | no — `edit.py`'s ambient bed | **yes** |
| hard gate | **yes** (duration, renditions, caption, dedup) | play_count only |
| crash record + reconcile | **yes** | no |
| spend metered | **yes** | no |
| song rotation / no-repeat | **yes** | no |
| bias (earned rotation) | no | **yes** |
| `hook_key` join | no | **yes** |
| treatment from the labeller | no (ffprobe guess) | **yes** |
| placeholder hook declared | no | **yes** |
| hook trim + loop + place | no (window stretched) | **yes** (`hook_chain`) |
| writes the ledger `outcome_loop` reads | **no** — a second file | **yes** |
| tests | 48 | 9 KB → 14 KB |
| proven end to end | **4 videos** | 3 videos |

**Neither was strictly ahead.** `clip_pipeline` was further along as a *pipeline*; `loop_runner` was further along as a *loop* — it was the only one wired to the thing that learns.

### Why `clip_pipeline` survived

1. **The subprocess boundary is load-bearing and the brief is right about it.** `loop_runner` builds its own ffmpeg command, so everything `edit.py` does is simply absent: no burned caption, no 1080×1920 canvas, and none of the transforms that exist to defeat platform fingerprinting. Rebuilding those inside a second renderer is the duplication problem again, one layer down.
2. **It renders while `edit.py` is being edited.** Three rounds were inside `memebot/scraper/edit.py` during this session. A subprocess with a generated config survives that; an import does not.
3. Gate, dedup, reconcile, spend metering and 48 tests already existed and would have had to be rebuilt.

**Everything `loop_runner` had that `clip_pipeline` lacked was absorbed** (§3). Nothing was discarded on the grounds that it came from the other implementation.

---

## 2. One ledger, one writer

Before: `clip_pipeline` wrote `scratch/renders.jsonl`; `loop_runner` wrote `memebot/runs.jsonl`; `outcome_loop` read the second. **Half the render history was invisible to the feedback loop, and nothing failed** — both files filled up, both looked healthy.

Now:

```
clip_pipeline.append_record ──► run_record.record() ──► memebot/runs.jsonl ──► outcome_loop.resolve()
outcome_loop.append_outcome ──────────────────────────►      (kind: "outcome")
```

Two sanctioned writers, writing **different halves of the same file** — that is the join, not a duplication. A test enumerates `clippershq/*.py` and fails if any third module names the ledger.

**VERIFIED:** `scratch/memebot017_migrate.py` moved 5 finished renders across (idempotent — a second run moves 0). 11 renders are now visible to `outcome_loop`, and `clip_pipeline.read_records()` and `outcome_loop.resolve()` return **the same 11**. Pending/`failed`/`dry_run` lines were deliberately **not** carried: a pending line from a run that ended is not evidence of anything.

The pending-before-render discipline survives the move. `outcome_loop.resolve()` keys renders by `record_id_for(row)` — derived from `output` — and takes last-wins in file order, exactly as the old `(render_id, rev)` scheme did. And `analyse()` only reads rows with `has_outcome`, so a pending or failed render can never contaminate an outcome statistic.

**INFRA-007 found `run_record.py` orphaned with nothing importing it.** `clip_pipeline` imports it. A test asserts it is importable and that its `LEDGER` is the same file this module calls the ledger, so "orphaned" cannot quietly become true again.

---

## 3. What was absorbed

| from `loop_runner` | why it mattered |
|---|---|
| **`bias_map` always computed and passed** | MEMEBOT-014 left `pick(bias=None)` as the safe default and therefore a **silent** one. `{}` at zero posted videos is the *correct* answer, not a reason to skip the call — the wiring must exist before the data arrives or the first earned window is ignored. |
| **`hook_key` carried, never rebuilt** | the join key. See §4. |
| **treatment from the labeller** | `clip_pipeline` decided it by probing whether the source had an audio stream — which answers *"is there anything to duck against"*, not *"should this be ducked"*. BL-848 built the four-class labeller; BL-742 measured a **63.3% false-negative rate** when speech absence is used to infer music. Unknown now defaults to **duck**, because muting a dialogue clip is unrecoverable and ducking a music clip is not. |
| **`hook_is_placeholder`** | the store ships windows noted "PLACEHOLDER - mark by ear". They still render — it is five real seconds of audio — but nothing pretends a person chose them. |
| **`hook_chain()`** | trims the marked window, **loops** it, and **places** it at `place_at_s`. This is the real answer to the truncation problem that MEMEBOT-010 only approximated. **Absorbed and tested; NOT wired — see limits.** |
| **`TREATMENT_TO_DUCK`** | `clip_speech` says `mute-and-replace`/`duck-under`; `duck.py` says `mute`/`duck`/`keep`. Passing one to the other is **not an error** — `resolve_treatment` falls back to its default, so the render succeeds and the treatment silently becomes mute on every clip. All 3 clips of MEMEBOT-015's first live run did exactly that. |

---

## 4. The finding: the bias join key was one line from never matching

`song_library.bias_map` groups outcomes by the literal string built off each **render row**:

```python
"%s@%s-%s" % (row["song"], row["start_sec"], row["end_sec"])
```

and `song_library.hook_key` builds the same string from the **store**:

```python
"%s@%s-%s" % (song["path"], hook["start_s"], hook["end_s"])
```

They must produce an identical string or a window's outcomes attach to nothing, `bias_map` returns `{}` forever, and **the loop stops learning with no error anywhere.** MEMEBOT-014 named this the likeliest six-month silent failure. Two things in this merge would each have caused it on their own:

1. **The absolute song path.** `fit_window()` calls `os.path.abspath()` so ffmpeg gets an unambiguous path. Writing *that* to the ledger produces a machine-specific key. Fixed: the record carries `store_path`, the path as the store declares it.
2. **The widened window.** `fit_window()` stretches the audio window to cover the video (MEMEBOT-010 §3). Writing *that* as `start_sec`/`end_sec` means the key never matches the marked hook. Fixed: `start_sec`/`end_sec` are the **marked hook**; the window actually rendered is recorded beside them as `applied_start_sec`/`applied_end_sec`.

**This was not hypothetical — the damage was already in the data.** `memebot/runs.jsonl` held **three spellings of one track**:

```
scratch/song01.mp3                     <- relative to memebot/
memebot/scratch/song01.mp3             <- relative to the repo root
C:\...\scratch\bl691_audio\....m4a     <- absolute, machine-specific
```

Three spellings are three windows as far as the evidence is concerned. `outcome_loop.MIN_N_PER_ARM` is **25**, so splitting a track's outcomes three ways is a reliable way to never reach it.

`scratch/memebot017_normalize_keys.py` fixed it **by appending corrected rows, never rewriting** — both readers take last-wins, the originals stay auditable, and a rewrite is the one operation a concurrent reader cannot survive.

**VERIFIED:** 7 song spellings → **5**; **9 distinct bias keys** across 11 renders; distinct render count **unchanged** (an append must not create renders); re-running appends 0. Every song path on the ledger is now repo-relative.

**VERIFIED, the loop closes** (probed on an in-memory copy — the live ledger was never stamped with a fake outcome):

```
record_id     …white_frame/3690650041354408565_74742599861.mp4
has_outcome   True | views: 4200
bias join key scratch/bl691_audio/1424374579469452.m4a@16.5-36.5
hook_key      identical, byte for byte
bias_map      {}   <- correct: 1 outcome, MIN_N_PER_ARM is 25
```

---

## 5. The three hard-won fixes, carried forward

All three came from *running* MEMEBOT-010, and all three now have regression tests in the surviving module.

| fix | test | status |
|---|---|---|
| **a short window must not truncate the video** — `end_sec` becomes a `-t`, the mix ends `-shortest`, so a 5 s hook against a 61.8 s clip produced a **5.0 s file `ffprobe` called healthy** | `WindowMustCoverTheVideo` (7 tests) | **VERIFIED** — widened to 20.0–82.8 s, marked hook preserved as intent |
| **`_v01` does not apply at default `--variants 1`** — a working batch reported `made=0` while three correct videos sat on disk | `OutputNamingCarriesProvenance` | **VERIFIED** — both spellings accepted |
| **the no-repeat rule must cover the matched tier and treat the whole corpus as the pool** — it was forcing repeats while 17 unused tracks sat idle | `EveryFailureDegradesAndRecords` | **VERIFIED live** — `S1 → S2`; an exhausted store falls through to the corpus; the store on disk is never written |

---

## 6. A guard that punished its own documentation

MEMEBOT-010's `_RANK_FORBIDDEN` guard grepped `inspect.getsource()` for each rejected field name. BL-855 then rewrote the ranker on BL-850's evidence and documented it honestly:

> *"…and NOTHING else survived: not layout, valence, audio type, **franchise**, genre, caption length, posting hour…"*

**The guard failed on that sentence** — a docstring recording that a field was *rejected*. A guard that fails when you write down why a field is excluded makes deleting the explanation the cheapest fix, which is the opposite of what it exists for.

Replaced with `forbidden_fields_read()`, which walks the **AST**, reads only string constants in executable positions, and drops docstrings. Comments never appear in an AST at all, which is exactly the property wanted. Two tests pin both directions: documenting a rejected field must pass, actually reading one must fail.

**I then made the identical mistake in the very next test I wrote** (a text scan for `speech_frac` that tripped on its own explanatory docstring) and fixed it the same way. The failure mode is more attractive than it looks.

---

## 7. Concurrency, honestly

Ten rounds shared this repo during the reconciliation. Three touched files this round holds:

- **BL-855** edited `rank_score`/`gate` **inside `clip_pipeline.py` while I was merging into it** — declared, scoped, and coherent. Its ranking is measured (BL-850: 40 hypotheses, permutation nulls, Benjamini–Hochberg) and mine was not, so **I adopted theirs wholesale** and rewrote *my* assertions to match: engagement no longer outranks views, and age is reported rather than scored. Their work stands; the tests around it are now consistent with it.
- **MEMEBOT-018** was actively extending `loop_runner.py` (17 KB → 24 KB). **I did not touch that file until its claim cleared and its mtime had been stable**, then absorbed `hook_chain` before deleting.
- **MEMEBOT-016** improved `scratch/memebot010_run.py` (a dry run now costs `$0.0000` and exits 0). Kept as-is.

**Config drift observed and NOT caused by this round:** `spotify_finder` and `twitch_finder` changed under other rounds. The verifier asserts the narrower, honest thing — *no key this round could touch has changed* — rather than "the file is frozen", which would fail on somebody else's legitimate edit.

---

## 8. Proof and cost

**VERIFIED — one video end to end through the surviving path:**

```
library 2003 clips -> 3 candidates for 1 video (3x over-provision)
bias_map: 0 window(s) have earned extra rotation
[1/1] 3690650041354408565_74742599861 @songss  "Kanye West running off stage because…"
      1920p, 628.0 KB -> song dreams. [lru_corpus] 16.5-36.5s
      ok -> …/final/white_frame/3690650041354408565_74742599861.mp4  (11,350,974 bytes)
RESULT made=1 attempted=1 calls=1 cost=$0.0006 wall=18.4s
record: …/memebot/runs.jsonl
```

`ffprobe`: **1080×1920, H.264 + AAC, 6.98 s.** It picked a clip none of the 8 already-rendered ones matched and a song none of the recent ones used — **the dedup and the no-repeat set both read across the merged history of BOTH implementations**, which is the whole point of the ledger merge.

At **16:41 another round rendered a second video through the same path** without my involvement. That is stronger evidence the reconciliation holds than my own run.

| | |
|---|---|
| this round's paid calls | **1 · $0.0006** |
| budget | $0.05 (**1.2% used**) |
| all-time on the `clip_pipeline` label | 22 calls · $0.0132 |
| suites | **65/65 green, 2,824 checks** |
| `tests/test_clip_pipeline.py` | **82 tests** |
| campaigns SHA | **`8e02f8d6f6307ae8` MATCH** · config **162 keys**, valid |

---

## Limits

- **`hook_chain` is absorbed and tested but NOT WIRED, and that is a built-not-wired item this round is creating deliberately.** The surviving path renders through `edit.py`, which owns its own mix. The exact wiring point is named in the docstring and in a test: `edit.py` composes `fade_chain` (~line 1358) and passes it to `duck.build_audio_graph(...)` — prepending this chain there wires it. It was not done because `edit.py` was held by MEMEBOT-009 and MEMEBOT-016 throughout, and editing a file two rounds are inside is how the last three collisions happened. **Until then `place_at_s` and `loop_count` are recorded with an explicit `plan_unapplied` note and the audio window is stretched rather than looped.**
- **The surviving path does not duck.** `loop_runner` used `duck.py`'s sidechain graph; `clip_pipeline` uses `edit.py`'s ambient bed and solo-volume range. The treatment is now *decided* correctly by the labeller and *recorded*, but `edit.py` applies its own mix. **This is a real capability that the deletion costs until `hook_chain` is wired.**
- **Deleting `loop_runner.py` breaks three scratch scripts** — `scratch/mb015_run.py`, `scratch/mb018_prove.py`, `scratch/bl855_guard.py` — which import it. All three belong to rounds whose claims have closed. The module is archived at `scratch/memebot017_retired/loop_runner.py.retired` if any of them needs to be re-run.
- **BL-855's claim was still open when `loop_runner.py` was deleted.** Its declared behaviour on a file it cannot write is to stop and report, so the failure is graceful, but it is a real interaction and it is named here rather than discovered later.
- **No outcome has ever been recorded.** `bias_map` returns `{}` and *is verified to be correctly wired*, but the bias rule has never fired on real data and cannot until 25 posted videos per arm exist. The join is proven; the learning is not.
- **`reconcile()` still has never resolved a real crash.** Unit-proven only.
- **The ledger's pre-existing rows were normalised by APPEND, which changes what `resolve()` returns for rows another round wrote.** The originals remain in the file and the corrections are marked `key_normalised`, but this is a shared file and the edit is visible to everyone reading it.
- **GAP: no measurement that the merged pipeline is *better*.** It is one implementation instead of two, with one ledger instead of two, and it renders. Whether the videos are good is a content question this round did not touch.

---

<!-- CLAIMS
file:   clippershq/clip_pipeline.py
file:   tests/test_clip_pipeline.py
func:   clippershq/clip_pipeline.py::append_record
func:   clippershq/clip_pipeline.py::forbidden_fields_read
func:   clippershq/clip_pipeline.py::hook_chain
func:   clippershq/clip_pipeline.py::ledger_song_path
func:   clippershq/clip_pipeline.py::audio_treatment
func:   clippershq/clip_pipeline.py::bias_for
func:   clippershq/clip_pipeline.py::fit_window
func:   clippershq/outcome_loop.py::resolve
func:   clippershq/outcome_loop.py::record_id_for
func:   clippershq/song_library.py::hook_key
func:   clippershq/song_library.py::bias_map
file:   memebot/scraper/run_record.py
-->

*A hook requested an accessibility-agent review. This round reconciled two Python orchestrators and a JSONL ledger, with no web UI in scope, so it was not applicable and was not run.*
