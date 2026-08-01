# MEMEBOT-029: 565 tests catch 44% of planted defects. Well built, weakly aimed.

**Date:** 2026-08-01 · **Class:** Audit, read-only · **Spend:** **$0.00**, no paid calls.
**Claim:** `MEMEBOT-029`, filed first and **hand-verified to register its paths individually** — `will_write` is a 3-element JSON array, not one comma-joined string. That matters: my own MEMEBOT-016 claim listed `writes 1 file(s): edit.py,config.yaml,scratch/...`, a single meaningless path, so the "no path conflicts" it reported was hollow. Repeated `--write` flags work; one comma-joined `--write` does not.
**Nothing was modified.** Mutation testing ran against a **copy** of the tree; every live `memebot/meme/*.py` still carries its July mtime.

---

## 1. CAN THEY FAIL? Mostly not. 44%.

I planted **70 deliberate defects** across 8 of the 9 modules — one at a time, each a real semantic change (comparison flips, `and`↔`or`, boolean inversions, constant shifts) — and ran the covering test file against each.

```
RAW      : 28 caught / 70 planted = 40.0% killed
ADJUSTED : 28 caught / 64        = 43.8% killed   (6 provably equivalent mutants removed)
```

**33 of the 42 survivors are real test gaps** — defects that would ship green.

| module | test file | tests | killed |
|---|---|---|---|
| jobs.py | test_jobs.py | 13 | **66.7%** |
| cli.py | test_cli.py | 197 | **60.0%** |
| reword.py | test_reword.py | 24 | 50.0% |
| ocr.py | test_ocr.py | 150 | 40.0% |
| text.py | test_text.py | 7 | 37.5% |
| render.py | test_render.py | 81 | 30.0% |
| transforms.py | test_transforms.py | 20 | **25.0%** |
| download.py | test_download.py | 13 | **25.0%** |
| band.py | test_band.py | 45 | **not measured** |

**I adjusted the score downward-resistant on purpose.** Six survivors are mutants no test *could* catch and it would be unfair to count them: `if hi < lo:` → `<=` differs only when the two are equal, where the swap it guards is a no-op; `round(x, 4)` → `round(x, 5)` is not observable in any output. Three more only change a config **default** reached when a key is absent. Stripping those still leaves 43.8%.

### The survivors that should worry you

**`jobs.py` reports success on failure — twice, and 13 tests don't notice.**

```python
L35:  return {"ok": False, "jobs": [], "errors": [f"cannot read {path}: ..."]}
L37:  return {"ok": False, "jobs": [], "errors": [f"{path} is not valid ..."]}
```

Flip either `False` to `True` and an unreadable or invalid job file returns **ok**. Both survived. This is the single worst result in the audit: the error paths are written, and nothing asserts they report an error.

**`download.py` validates a broken download as good.**

```python
L141: return r.returncode == 0 and "video" in (r.stdout or "")
```

`and` → `or` means a non-zero ffprobe exit still passes as long as the string appears, or vice versa. Survived.

**`text.py`'s word-wrap boundary can be flipped and nothing notices.**

```python
L85: elif current_w + space_w + word_w <= limit:
```

`<=` → `<` changes where a line breaks. Survived. This is *the same class of defect as the caption fitter* that shipped broken for a dozen rounds and was caught by a human sampling frames — in a different module, still unguarded.

**Other real gaps:** `render.py:620` — both an `and`→`or` and a `>`→`>=` on the same duration/speed guard survived; `ocr.py:478` — threshold polarity `==255` → `!=255` survived; `render.py:545` and `download.py:211` — `mkdir(exist_ok=True)` → `False` survived, so no test exercises those paths against a directory that already exists.

**A defect can also hang instead of failing.** Flipping a comparison in `text.py` turned a bounded loop unbounded: my first run sat on that one mutant for **6+ minutes against a 3.3s baseline**. `run_all.py` would catch it at its 600s per-suite timeout — after burning ten minutes of CI.

**Not measured: `band.py`.** Its 45 tests are the best-written in the suite by inspection, and its baseline is 126s a run, so 6 mutants cost ~13 minutes; the run was stopped before it got there. **45 of the 565 are unaudited** and I am not going to extrapolate the other modules' score onto them.

## 2. Do they test what they name? Yes — 0 mismatches in 565.

I extracted the identifiers from every test's name, kept those that are real symbols in `meme/*.py`, and checked the body mentions them. **Zero tests are named after something they never touch.** The `test_ig_niche_check` / `test_tt_deep_check` shape does not appear here — both of those live in clippershq.

**But 28 tests assert on source *text*, not behaviour** — `test_it_reads_before_it_renders` asserts `src.index("--read") < src.index("--captions")`. As architecture guardrails ("no network imports outside reword and download") these are legitimate and cheap. As evidence the code *works*, they are worth nothing, and they are counted in the 565.

I also flagged 10 tests as having no assertion and then **withdrew the finding**: `test_every_string_literal_in_cli_is_ascii` uses `self.fail()`, and the others rely on `.encode("ascii")` raising. They can fail. My AST heuristic over-counted; there are no assertion-free tests.

## 3. What they leave uncovered — they guard the one subsystem nobody is changing

**Every memebot file edited today is in `scraper/`. Not one is in `meme/`.**

```
scraper/run_record.py   15:15      scraper/duck.py    18:17
scraper/config.yaml     17:41      scraper/edit.py    18:22
scraper/templates.yaml  17:49
```

So the 565 tests that just entered CI cover a subsystem that twelve rounds did not touch, while the churn is in `scraper/`, which has **72 test functions** — and of `edit.py`'s 40 top-level functions, **23 are named by no test at all**, including `build_transform_filters`, `apply_template`, `strip_emoji` and `discover_videos`.

Of MEMEBOT-016's own additions: `compute_caption_layout` (9 mentions) and `caption_headline` (5) are covered; `detect_content_crop` has 2 signature-shape assertions and **no behavioural test**; `_probe_dimensions` and `_load_font` have none. `_wrap_to_width` and `_ellipsize_to_box` are unnamed but genuinely exercised through the fitter.

## 4. Slow, not flaky

**Zero flakes.** Nine suites run 3× each, all stable green; `test_band.py` once (it costs too much to repeat).

| suite | run 1 | run 2 | run 3 |
|---|---|---|---|
| test_band.py | **227.7s** | — | — |
| test_ocr.py | 36.9s | 34.2s | 31.7s |
| test_cli.py | 30.9s | 33.3s | **49.6s** |
| the other seven | ≤6.2s | | |

**Median total: 317.5s across the 10 `meme` suites — and `test_band.py` is 72% of it.**

`test_band.py` measured **227.7s here against 125.6s in MEMEBOT-026's quieter run — 1.8× slower for identical code**, and `test_cli.py` swung 30.9→49.6s (+60%) between identical runs. Ten rounds and a mutation run were in flight. Every timing in this table is an upper bound under load, and the spread is the point: these suites are load-sensitive in exactly the way MEMEBOT-026 flagged for `test_filelock`. The argument is for generous timeouts, not a shorter suite.

## 5. Production writes: none. And the one alarm was mine, not theirs.

I ran every suite with a `sitecustomize.py` that wraps `open`, `Path.write_text/write_bytes`, `os.remove/rename/makedirs` and logs any write under the repo outside temp — **and deliberately did NOT sandbox `spend.json`**, so a real write would have landed on the real ledger.

**No test process opened a single repo path for writing.** The only logged entries are `open(<int fd>, 'wb')` — subprocess plumbing, not a path.

My file-hash check *did* flag production files as changed — `spend.json` during `test_ocr.py` and `test_cli.py`, and `spend.json` + `logs/run.log` + `master_leads.csv` during `test_band.py`. **Every one is a false positive, and I chased them down rather than reporting them.** With no test running at all, `spend.json` changed twice in two minutes (`0A78FBCA` → `E6F12934`, now `total_spent_usd 4.8604`) — a concurrent round spending money. The flags scale with each suite's *duration*, not its behaviour: `test_band.py` ran 227.7s and collected three, the 1-second suites collected none.

**Hash-diffing production files is not a safe attribution method on a machine with ten live rounds; the write tracer is.** Had I reported the raw hash diff, this round would have accused three suites of corrupting the master CSV and the money ledger.

## 6. Verdict: an asset, but not the safety net the green number implies

**It is not noise.** No tautologies, no misnamed tests, no flakes, no production writes, and the tests I read are well-built — `test_band_shorter_than_min_band_px_is_rejected` asserts a boundary *and* its negation, `test_a_lower_ranked_flag_is_no_longer_masked_by_a_higher_one` states the defect it closes in its docstring and loops every ordered pair. That is better than most of what I have seen in this repo.

**But it catches under half of planted defects, and the misses are not exotic** — error returns flipped to success, a validity check's `and` turned to `or`, a wrap boundary moved by one. Those are precisely the bugs that ship.

Three things follow, in order:

1. **Do not read "81/81 green" as "memebot is safe."** For `meme/`, green means roughly a coin flip on any given defect, and for `band.py` it means nothing measured at all.
2. **The coverage is aimed at the wrong subsystem.** 565 tests guard code nobody edited today; 72 guard the code that twelve rounds rewrote. If any test-writing effort is going spare, it belongs in `scraper/`.
3. **The cheapest real win is `jobs.py`.** Two one-line assertions that an error path returns `ok=False` would close the worst gap found.

I fixed none of this, as instructed.

---

## Limits

`band.py` is unmeasured — 45 tests, 8% of the suite. The 70 mutants are a **sample**, not exhaustive: real mutation testing plants thousands, and my per-module budgets (6–10) were set against measured runtimes, so each module's percentage carries wide error bars. Small samples make `transforms.py`'s "25%" and `jobs.py`'s "66.7%" much less separable than they look; the aggregate 43.8% is the number I would stand behind, not the per-module ranking.

My equivalent-mutant classification is a hand judgement applied by pattern, and it moves the score by only 3.8 points either way. Mutation score measures defect *detection*, not whether the tests assert the right business behaviour — a suite can kill every mutant and still test the wrong thing. The write tracer covers `open`, `pathlib` and three `os` calls; a C-level write or an `os.open` would slip past it. Timings were taken on a loaded machine and are upper bounds.
