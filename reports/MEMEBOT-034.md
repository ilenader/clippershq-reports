# MEMEBOT-034: 41.2% → 52.9% on the same 70 defects. jobs.py went to 100%.

**Date:** 2026-08-01 · **Class:** Fix + measurement · **Spend:** **$0.00**, no paid calls. `memebot/` only.
**Claim:** `MEMEBOT-034`, filed with **nine repeated `--write` flags**, and the tool confirmed *"9 path(s) registered individually"* — the failure mode MEMEBOT-029 caught in its own earlier claim (one comma-joined string registering as a single meaningless path) did not recur.
**+68 tests.** jobs 13→17, download 13→20, text 7→18, render 81→91, ocr 150→154, plus 30 new in `scraper/`.

---

## The number

Same mutation harness, **same seed**, so the same defects are planted in the same places:

```
MEMEBOT-029 (8 modules) : 28 caught / 68 = 41.2%
MEMEBOT-034 (8 modules) : 36 caught / 68 = 52.9%      +11.7 points
with band.py included   : 38 caught / 74 = 51.4%   (57.6% adjusted)
```

| module | before | after | |
|---|---|---|---|
| jobs.py | 66.7% | **100.0%** | the cheapest win, taken |
| render.py | 30.0% | **50.0%** | |
| download.py | 25.0% | **50.0%** | |
| ocr.py | 40.0% | **50.0%** | |
| text.py | 37.5% | **50.0%** | see caveat — different sites |
| cli.py | 60.0% | 60.0% | untouched |
| reword.py | 50.0% | 50.0% | untouched |
| transforms.py | 25.0% | 25.0% | untouched; its survivors are the equivalent ones |
| **band.py** | *not measured* | **33.3%** | now measured, and the worst |

**Caveat on `text.py`.** It is the one module whose source I changed (the loop bound), so its AST shifted and the seed selected **different** sites. Its 37.5%→50.0% is not a like-for-like comparison; the other seven are.

## Which named survivors are dead

| target | result |
|---|---|
| `jobs.py:35` + `:37` — `{"ok": False}` → `True` | **killed** (both) |
| `download.py:141` — `and` → `or` | **killed** |
| `download.py:278` — `enumerate(start=1)` | **killed** |
| `text.py:85` — wrap boundary `<=` → `<` | **killed** |
| `text.py:40/46/18/191` | **killed** |
| `render.py:620` — `and` → `or` | **killed** |
| `render.py:545` — `mkdir(exist_ok=True)` | **killed** |
| `ocr.py:478` — threshold polarity `==` → `!=` | **killed** |
| `render.py:620` — `>` → `>=` | **not killable** — see below |
| `download.py:211` — `mkdir(exist_ok=True)` | **NOT CLOSED** — see below |

### `render.py:620`'s `>` is an equivalent mutant, and I did not fake a kill

I wrote the test, it failed, and it was the test that was wrong. `_build_cmd` reads:

```python
speed = float(tx.get("speed", 1.0) or 1.0)
```

`0.0 or 1.0` is **1.0**, because 0.0 is falsy. Zero speed never reaches the guard, and 0.0 is the only value at which `>` and `>=` differ. The comparison is untestable through this path *by construction*.

So instead of a fake kill there is now a test that **pins the coercion**: `speed=0.0` must produce `-t 30.000`, not a division by zero. The day someone drops the `or 1.0`, that test fails instead of the renderer crashing. This is the same `or`-swallows-an-explicit-zero family already recorded in this project for `str(v or "")`.

### `download.py:211` — named in the brief, not closed

The `mkdir(parents=True, exist_ok=True)` inside `download_url` needs the whole HTTP path stubbed to reach, and I judged a network-shaped fixture worse value than the 30 `scraper/` tests. **Stating it plainly rather than letting the score imply it was covered.** Its sibling at `render.py:545` — the same defect, reachable directly — is killed.

## The runaway loop is bounded

`_wrap_to` binary-searches the narrowest line limit. Mutating `while lo < hi` to `<=` makes the `lo == hi` case assign `hi = mid = lo` forever — one mutant ran **6+ minutes against a 3.3s suite**, and `run_all.py` would only have killed it at its 600s per-suite timeout.

The search now carries an iteration budget of `max(8, (hi-lo).bit_length() + 2)`. Halving an interval cannot need more, so a correct search is unaffected and a runaway stops. Verified: layout output is byte-identical on four real captions, and a synthetic 400-word wrap still converges to 4 lines **in under 1 ms**.

## `scraper/`, where the churn actually is — 30 new tests

MEMEBOT-029's structural finding was that all 565 enrolled tests cover `meme/`, which nobody edited, while every file twelve rounds *did* edit lives in `scraper/`. `memebot/scraper/tests/test_edit_behaviour.py` covers, prioritised by churn rather than ease:

- **`detect_content_crop`** — had two signature-shape assertions and **no behavioural test**, despite deciding whether a source's letterbox is cropped (the 48%→11% dead-frame change). Now tested in both directions: a synthetic 320×120-in-320×240 letterbox **is** cropped back to its picture (±16px on height and offset), a tight source is **left alone**, the `min_area_pct` guard refuses an over-aggressive crop, a missing file is not fatal, and the result caches per path.
- **`_probe_dimensions`** and **`_load_font`** — added by MEMEBOT-016, previously untested. The font cache is asserted to actually return the identical object.
- **`strip_emoji`** — including that typographic `’` and `…` **survive**, since stripping them would mangle real captions.
- **`escape_drawtext`**, **`wrap_caption`**, **`parse_only`**, **`resolve_asset`** (from a foreign CWD — the `ambient_bed.file` resolution bug class), **`build_transform_filters`** (8-tuple arity, and a seeded roll reproducing).

## Suite

**88 of 89 green.** The one red is **`tests/test_claims_manifest.py`**, and it is not mine:

```
docs/claims/MEMEBOT-022.claims claims that no longer hold:
  const clippershq/song_library.py::TIER_TITLE: no assignment at HEAD
```

MEMEBOT-032 is in flight and was tasked with deleting that tier, which invalidates MEMEBOT-022's published manifest. I touched no clippershq file and left it alone.

## What still survives, and where the next gains are

36 survivors: **28 real gaps**, 5 provably equivalent, 3 default-only. The remaining clusters:

- **`band.py` at 33.3%** is now the weakest and the most expensive to improve — 100s a run. Its survivors are real: `if t >= duration` (`>=`→`>`), a `> tol` row-difference threshold, and two array-index constants.
- **`reword.py`** — `status_code == 429` and a `max(3, max_changed)` floor both survive; retry and change-cap behaviour is unasserted.
- **`cli.py:1553`** — `if rendered > 0 and failures:` flipped to `or` survives, so the mixed-outcome summary line is unguarded.
- **`ocr.py:1019`** — `mean_conf < conf_floor` boundary, and `ocr.py:523`'s `max(0, ...)` clamps.

## Note where the 565 is quoted

**28 of the 565 assert on source *text*, not behaviour** — `test_it_reads_before_it_renders` compares `src.index("--read") < src.index("--captions")`. As architecture guardrails ("no network imports outside reword and download") they are legitimate and cheap. As evidence the code works they are worth nothing, and they are counted in the 565. Any figure quoting that total should carry this sentence.

---

## Limits

The mutants are a **sample** — 6–10 per module, budgeted against runtime — so per-module percentages carry wide error bars and the ranking between adjacent modules is not meaningful. The aggregate and the direction are. `band.py`'s 33.3% rests on **six** mutants; treat it as "measured, and low", not as a precise figure.

Mutation score measures defect *detection*, not whether the assertions encode the right behaviour. My own new bound at `text.py:117` is itself now a surviving site (`max(8, ...)` → `max(9, ...)` changes nothing, since the budget is deliberately generous) — a reminder that adding code adds sites, and that a rising score is not the same as a rising guarantee.

I did not run a render this round; the crop and caption behaviour is covered by tests, and MEMEBOT-016 holds the frame evidence. Timings were taken with nine other rounds live.
