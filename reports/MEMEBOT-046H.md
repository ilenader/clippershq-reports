# MEMEBOT-046H: the harness was reading stale bytecode. Fixed, proven, re-measured — 56.0%.

> **Relocated and corrected 2026-08-01 by MEMEBOT-053.** This report was first published to
> the repo **root** as `MEMEBOT-046.md`, which is not the canonical path — the README puts
> reports at `reports/<TICKET>.md`. It now lives at `reports/MEMEBOT-046H.md`, suffixed per
> `CONVENTION.md` ("suffix the filename, not renumber someone else's ticket") because
> `reports/MEMEBOT-046.md` belongs to the bed-level round that claimed the number first.
>
> **The collision this report predicted did not happen.** The two documents were written to
> two different paths and have different blob SHAs, so neither overwrote the other. The real
> defect was subtler: a report at the root is outside `reports/` and therefore outside
> `MANIFEST.tsv`, so it is published but not indexed. See MEMEBOT-053.

**Date:** 2026-08-01 · **Class:** Tooling fix + re-measurement · **Spend:** **$0.00**, no paid calls.
**Claim:** filed as **`MEMEBOT-046H`**, five repeated `--write` flags, *"5 path(s) registered individually"*. **The suffix is deliberate: round `MEMEBOT-046` was already in flight** (started 21:27, bed-level work on `memebot/scraper/edit.py` + `clippershq/song_loudness.py`). I write none of its paths — but **it will presumably also want to publish `MEMEBOT-046.md`, and one of us will overwrite the other.** Flagging so you can rename one.
**`claim.py brief` (run first):** 10 rounds in flight — BL-849 (383 min, *nothing written yet*), MEMEBOT-039, MEMEBOT-044, BL-895, BL-896, MEMEBOT-046, BL-898, BL-897, BL-899, BL-900. **MEMEBOT-036 confirmed RELEASED** — its claim file is gone.
One advisory: BL-895 claims `scratch/` broadly; my paths are `scratch/mb046h_*`, a distinct prefix.

---

## 1. The cause: CPython was executing the *previous* mutant

Every mutation changes **one character**, so `ast.unparse(mutant)` is the **same length** for every mutant of a given kind — and the old harness reused one copy of the tree, writing them milliseconds apart.

**CPython validates a cached `.pyc` against the source's `(mtime, size)` pair.** Same size, same coarse mtime ⇒ the cache looks valid ⇒ Python runs the **previous mutant's bytecode**. The verdict you read belongs to whichever mutant was cached, not the one you wrote.

Controlled proof — six mutants, each with ground truth established by running it **alone in a fresh copy**:

```
AS SHIPPED (reuses one copy):     1 of 6 verdicts disagree with ground truth
   L195  4->5   CAUGHT  (truth lived)  <-- WRONG
FIXED (no bytecode + purge):      0 of 6 verdicts disagree
```

**It errs in both directions** — reporting CAUGHT for a mutant that truly survives (inflating a score) and lived for one that is truly caught (deflating it). That is exactly the 2/8, 3/8, clean-CAUGHT spread MEMEBOT-041 saw for the same site.

**Ruled out first, with evidence:** unseeded RNG in the tests (all seeded — checked statically) and `PYTHONHASHSEED` randomisation. Pinning the hash seed to 0 and to 1 changed nothing: the same mutant came back CAUGHT **8/8 in all three environments**. The tests were never the problem; the harness was.

### The fix

`scratch/mb046h_mutate.py`: `PYTHONDONTWRITEBYTECODE=1` so no `.pyc` is written, **and** `__pycache__` purged before every run so none can be read. Plus `PYTHONHASHSEED=0` pinned — it was not the cause, but a metric this load-bearing should not have a second source of drift.

**Sampling deliberately left alone.** A per-module seed would be tidier, but it draws a *different* sample and the re-measurement could no longer separate "the fix changed the answer" from "the dice changed". Measured: per-module seeding moved transforms.py from 8 sites scoring 50% to a different 8 scoring 12.5% — same code, same tests. `--only` is valid for a determinism check, not for comparison against a full run.

### Determinism, proven

Five consecutive runs, same module, comparing the full verdict sequence:

```
run 1..5: transforms.py  8 mutants  caught 1 / survived 7  = 12.5%   (per-module seed)
distinct verdict-sequences across 5 runs: 1  => DETERMINISTIC
```

and three more with the shipped sampling restored: **50.0%, 50.0%, 50.0%.**

## 2. Re-measurement — 8 of 9 modules were unaffected

Same seed, same sites, deterministic harness:

| module | MEMEBOT-041 (buggy) | **MEMEBOT-046H** | |
|---|---|---|---|
| transforms.py | 25.0% | **50.0%** | the bug, −2 mutants |
| band.py | 43.8% | **50.0%** | my tightened test, +1 |
| jobs.py | 100.0% | 100.0% | unchanged |
| render.py | 50.0% | 50.0% | unchanged |
| download.py | 62.5% | 62.5% | unchanged |
| text.py | 50.0% | 50.0% | unchanged |
| reword.py | 50.0% | 50.0% | unchanged |
| ocr.py | 50.0% | 50.0% | unchanged |
| cli.py | 60.0% | 60.0% | unchanged |
| **OVERALL** | **52.4%** | **56.0%** (60.3% adjusted) | |

**Which conclusions survive: nearly all of them.** The bug corrupted **one module out of nine** in this sample, by two mutants. The direction across four rounds — 41.2% → 52.4% → **56.0%** — is intact, and eight of nine per-module figures reproduce exactly.

**And it exonerates MEMEBOT-041's tests.** That round wrote transforms tests, measured 25%, and reported them as apparently ineffective while flagging the harness as untrustworthy. The tests worked; the harness was hiding two kills. transforms' four remaining survivors are now **all equivalent-or-default**: two swap guards (`if hi < lo`, provably no-op at equality) and two config fallbacks. There is no real gap left in that module's sample.

**What I could NOT re-measure, and why.** MEMEBOT-029 and -034 measured *earlier states of the test files*, and **`memebot/` is entirely gitignored** (`.gitignore:158`; `git log` shows **0 commits** for `test_band.py`). Those states no longer exist anywhere. Their figures cannot be re-derived by anyone — the honest status is **"unverifiable, and off by up to ~1 module's worth"**, not "confirmed". Only the current state is measurable, and it is measured above.

## 3. The two known-bad tests

**`band.py:383` — FIXED and verified killing its target.** MEMEBOT-041 asserted `band["top"] <= 2` against a mutation that shifts the search window by **one pixel**. Now exact:

```
verdict: CAUGHT
AssertionError: 1 != 0 : a band flush with the top edge must report top=0 exactly
```

**`band.py:385` — NOT fixable, and MEMEBOT-041 mis-diagnosed it.** It recorded *"my fixture missed the equality boundary"*. It is not a fixture problem: `if y1 <= y0: return None` mutated to `<` skips the early return at `y1 == y0`, but the scan below is `while y < y1` starting from `y = y0`, so it runs **zero times** and returns `None` regardless. **A true equivalent mutant** — no input distinguishes them. The test now documents that and pins the behaviour (an empty window yields no band) instead of pretending to catch something uncatchable.

## 4. The three uncovered band functions

Covered in MEMEBOT-041 and re-confirmed here: `_bridge_light_gaps`, `_find_dark_band` and `_cfg_get` were imported by **no test at all** while 45 well-written tests all drove `_find_band_in_array`. `test_band.py` is now **61 tests** and band scores 50.0%.

The one worth naming again: the *sides-of-different-colours* bridging test kills the `axis=1`→`axis=2` mutant on the row-median. `axis=1` is the row's dominant **colour**; `axis=2` throws colour away. A greyscale fixture gives the same number either way — the test uses a blue side and a red side with **identical per-pixel channel medians**, so only the correct axis sees a boundary.

Eight survivors remain in band, all real: `t >= duration`, `AGREE_TOL_PX = 8`, the `bg_match_tol` comparison, three conditions in the gap loop, `len(static_rows) >= bottom`, and `bottom - top < min_band_px`.

## 5. Carried correction

**`round(x, 4)` → `round(x, 5)` is NOT an equivalent mutant.** MEMEBOT-034 called it "unobservable at these magnitudes" and was wrong twice over: the rounded value is the audit record *and* it is substituted into the ffmpeg filter string —

```
vf_prefix: crop=iw/1.1357:...  eq=saturation=1.0799:gamma=1.1273
```

— so changing the rounding changes the command that renders the video. Under the mutation the test fails with `AssertionError: 0.99313 != 0.9931`. This correction is now carried in the test's own docstring, where the next reader will meet it.

## Suite

**99 of 100 green.** The red is `tests/test_clip_pipeline.py` (`AssertionError: 'lru_corpus' != 'matched'`) — a song-matcher tier assertion in clippershq, whose file BL-899 holds and is actively changing. "memebot" appears in that file only in docstrings. All my suites pass; `test_band.py` reports 61 checks.

---

## Limits

**`memebot/` is gitignored, so none of this work is under version control** — the fixed harness lives in `scratch/` (tracked), but every test file I have written across four rounds exists on one disk with no history. That is also why MEMEBOT-029's and -034's numbers can never be re-derived.

The plants remain samples — 6–16 per module against hundreds of sites — so per-module percentages carry wide error bars and adjacent modules still cannot be ranked. What changed is that a *repeat* of the same measurement now returns the same answer; that is reproducibility, not precision.

I proved determinism over 5 runs of one module and 3 of another, not over 5 full passes (a full pass is ~35 minutes, dominated by band at ~77 s per mutant). The bytecode mechanism is proven by the controlled 6-mutant ground-truth comparison, which is the stronger evidence.

The fix is belt-and-braces by choice: either `PYTHONDONTWRITEBYTECODE` or purging `__pycache__` would likely suffice alone, and I did not isolate which — after this metric misled three rounds, cheap redundancy beat a tidy minimal diff.
