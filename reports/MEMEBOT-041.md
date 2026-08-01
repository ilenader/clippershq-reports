# MEMEBOT-041: band.py 33.3% → 43.8% on a plant 2.7× wider. And my harness is not reproducible.

**Date:** 2026-08-01 · **Class:** Fix + measurement · **Spend:** **$0.00**, no paid calls. `memebot/meme/` only.
**Claim:** `MEMEBOT-041`, eight repeated `--write` flags, *"8 path(s) registered individually"*. One advisory: BL-867 claims `scratch/` broadly; my paths are `scratch/mb041_*`, a distinct prefix, so I proceeded.
**`claim.py brief` (run first, as asked):** 8 rounds in flight — BL-849 (327 min, *nothing written yet*), BL-867, MEMEBOT-036, MEMEBOT-038, MEMEBOT-039, MEMEBOT-040, BL-887, BL-888 (*nothing written yet*). **MEMEBOT-036 holds every `memebot/scraper/` path**; I wrote none of them.

**+26 tests**, all in `memebot/meme/tests/`: band 45→60, transforms 20→28, download 20→23.

---

## The scores

```
MEMEBOT-034 : 38 caught / 74 planted = 51.4%   (57.6% adjusted)
MEMEBOT-041 : 44 caught / 84 planted = 52.4%   (57.1% adjusted)
```

| module | 034 | 041 | |
|---|---|---|---|
| **band.py** | 33.3% (6 planted) | **43.8% (16 planted)** | plant 2.7× wider **and** score up |
| **download.py** | 50.0% | **62.5%** | `parents=True` closed |
| jobs.py | 100.0% | 100.0% | held |
| cli.py | 60.0% | 60.0% | untouched |
| render / text / reword / ocr | 50.0% | 50.0% | untouched |
| transforms.py | 25.0% | **disputed — see below** | |

**On the denominator (item 5).** This round changed **zero production code** — every module in `memebot/meme/` still carries its pre-round mtime, and the only edits are test files. So no new mutation sites were created and nothing is hidden by a shrinking denominator. The total moved 74→84 for exactly one reason: band's plant widened from 6 to 16. Like-for-like on the eight non-band modules: **36/68 → 37/68**.

MEMEBOT-034's own warning was the opposite case — it added a loop bound, which *was* a new site. Worth keeping the distinction: adding tests never moves the denominator; adding code always can.

## 1. band.py — widened and raised

Its 45 tests were called the best-written in the suite, and they are. The 33.3% was never about quality — it was **coverage shape**. Every existing test drove `_find_band_in_array`; `_bridge_light_gaps`, `_find_dark_band` and `_cfg_get` were imported by **nothing**. Well-written tests of one function cannot defend another.

15 new tests target exactly those three. The one worth naming:

A test named for *sides of different colours not being bridged*, whose docstring reads
*"Kills the axis=1 -> axis=2 mutant on the row-median."*

`np.median(img, axis=1)` is the row's dominant **colour** (H,3); `axis=2` is the median across channels per pixel (H,W), which throws colour away. A greyscale fixture cannot tell them apart — both give the same number. The test uses a blue side and a red side whose per-pixel channel medians are *identical* (10), so only the correct axis sees a boundary.

**Nine survivors remain**, and two of them are tests I aimed and missed:

- **`L383` `y0 = max(0, int(search_top_frac * frame_h))` → `max(1, …)`.** I wrote the *band-flush-with-the-top-edge* test for this and asserted `band["top"] <= 2`. The mutation shifts the search start by **one pixel**, so my tolerance was wider than the defect. `assertEqual(band["top"], 0)` would have caught it.
- **`L385` `if y1 <= y0: return None` → `<`.** I wrote the *inverted-search-window* test using fracs 0.9/0.1, which gives `y1 < y0`. The mutation only differs when `y1 == y0`, which my fixture never produces.

Both are the same lesson the caption fitter taught: **a boundary is only tested by landing exactly on it**. I am reporting these rather than quietly re-tuning them, because "I wrote a test for that" is precisely the belief mutation testing exists to check.

The rest: `t >= duration` (`>=`→`>`), `AGREE_TOL_PX = 8`, the `bg_match_tol` comparison at L281, three conditions in the gap loop at L157, `len(static_rows) >= bottom`, `bottom - top < min_band_px`, and a glyph-row lookahead.

## 2. transforms.py — the equivalence claim is HALF WRONG, and my harness disagrees with itself

**MEMEBOT-034 said transforms' survivors "are the equivalent ones". Verified: two of six are, and two are not.**

**CONFIRMED equivalent** — `if hi < lo: lo, hi = hi, lo` mutated to `<=` (twice). The only value it changes is `hi == lo`, and swapping two equal values is a no-op. No test can distinguish them and none should try. What I pinned instead is the behaviour the guard exists for: inverted bounds must still roll inside the range.

**REFUTED** — `round(saturation, 4)` → `round(…, 5)`. MEMEBOT-034 called this "unobservable at these magnitudes". It is observable twice over:

```
rolled:    {'saturation': 1.07989, 'speed': 0.9931,  'zoom': 1.1357}   <- mutated
vf_prefix: crop=iw/1.1357:...  eq=saturation=1.0799:gamma=1.1273
```

The rounded value is the **audit record** *and* it is substituted into the **ffmpeg filter string** — changing the rounding changes the command that renders the video. Under the mutation the new test fails with:

```
AssertionError: 0.99313 != 0.9931 : speed is reported at more than 4 dp
```

**Now the uncomfortable part.** My batch harness scored transforms **2/8** both before and after these tests. An isolated re-run of the same module with the same mechanism scored **3/8**. A single-mutant reproduction of `L150` — printing the assertion above — shows it **CAUGHT**. Three runs, three answers.

I could not reconcile them, and I am not going to quote whichever flatters the round. **The verified facts are per-site:** L147 and L150 are caught (assertion text reproduced), L195 and L257 survive, the two swap guards are equivalent. **The batch number for transforms is unreliable.**

This matters beyond one module: **every figure in MEMEBOT-029, -034 and -041 came from this harness.** Treat them as ±1 mutant per module, not as exact. The direction (41% → 52%) rests on many modules moving together and on per-site verification, not on any single percentage.

## 3. download.py:211 — decided, and it was mis-described

Named in two briefs and left open by MEMEBOT-034, which judged it needed a network fixture. **It did not — the file's own `router`/`FakeResp` harness covers it in six lines**, and it is now closed (download 50% → 62.5%).

It was also mis-described. That line carries **two** booleans:

```python
dest_dir.mkdir(parents=True, exist_ok=True)
```

`exist_ok` was already covered — the harness's dest always exists, so flipping it turns a passing download red. **The survivor was `parents=True`**: nothing had ever downloaded into a nested folder whose parent was missing, which is the only situation that flag exists for. Three tests now cover created-nested, reused-existing, and uncreatable.

## 4. The `or`-swallows-zero sweep

**76 `or`-defaults on a keyed lookup across `memebot/`. 19 sit on a knob where 0/""/False is meaningful. Nine use the dangerous `x.get(k, D) or D` form — and only ONE actually changes a value.**

The rest are `X or X`: `tx.get("seek_sec", 0.0) or 0.0`, `rolled.get("shift_x", 0) or 0`, `v.get("width", 0) or 0`, `_amb_start_offset, 0.0) or 0.0`. The fallback equals the falsy value, so the `or` is redundant but harmless. Noise, not bugs.

The one that bites is the one already known:

```python
speed = float(tx.get("speed", 1.0) or 1.0)      # render.py:608 — 0.0 becomes 1.0
```

**And one new, with a twist** — `reword.py:260`:

```python
max_changed = int(rcfg.get("max_words_changed") or DEFAULTS["max_words_changed"])
...
if changed > max(3, max_changed):               # reword.py:184
```

Setting `max_words_changed: 0` — "reject any rewrite that changes a word" — is swallowed **twice**: the `or` replaces 0 with the default, and even if it survived, the `max(3, …)` floor would raise it to 3. **A deliberate 0 is unreachable through two independent guards.** Whether that is wrong depends on whether zero was ever meant to be settable; I am reporting it, not changing it.

Minor: `download.py:180` `timeout_sec or DEFAULT_TIMEOUT` makes a 0 timeout unsettable; `reword.py:258/259` the same for `timeout_sec`/`max_tokens`, where 0 is meaningless anyway.

`band._cfg_get` is the **correct** idiom and is now pinned by a test:

```python
return DEFAULT_CFG[key] if value is None else value
```

## Suite

**94 of 96 green.** Both reds are other rounds', neither imports a memebot module:

- `tests/test_funnel.py` — `TypeError: simulated bad response shape` in a clippershq fixture.
- `tests/test_matcher_boundary.py` — created 20:55 and **modified 21:09, mid-run**: MEMEBOT-042's file, still being written.

All three of my touched suites pass: band 60 checks, transforms 28, download 23.

---

## Limits

**The harness's per-module numbers are not reproducible run-to-run** (section 2). That is the most important limit in this report and it applies retroactively to MEMEBOT-029 and -034. Per-site verification with the failing assertion printed is trustworthy; a single batch percentage is not.

The plants are still samples — 6–16 per module against hundreds of available sites — so a module's percentage has wide error bars and adjacent modules cannot be ranked against each other. band.py at 43.8% rests on 16 mutants.

Two of my own band tests were aimed at specific survivors and missed, by a one-pixel tolerance and a fixture that never hit the equality case. I left both as they are and named them rather than tuning them until they passed, which would have proved nothing.

The `or` sweep is static and matches `.get()`/subscript forms only; an `or` default reached through a helper would not appear. Whether a swallowed zero *matters* is my judgement of each knob, not a measurement.
