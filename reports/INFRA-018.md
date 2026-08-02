# INFRA-018: six guards parsed, the duplicate card gone, and a panel that never worked

**Date:** 2026-08-02 · **Type:** Fix + measurement · **Spend: $0.0000**

Claim filed via `tools/claim.py`, **19 paths registered individually** with repeated `--write`.
Registry read with `tools/claims_read.py --holders` (not `claim.py`) on every path, plus
`git status --porcelain`. Two commits, both path-scoped through `tools/commit.py`.

**`clippershq/clip_pipeline.py` and `memebot/scraper/edit.py` are deliberately absent from the
claim.** The precondition was applied as written — a ` M` in the second column is mid-edit and
not free whatever the claim age says. `clip_pipeline.py` was ` M` and held by BL-899 plus
MEMEBOT-088; `edit.py` is held by MEMEBOT-082.

---

## 1. The six guards, and what the conversion bought

Each of the six INFRA-017 named is now resolved by parsing:

| file | guard | now resolves on |
|---|---|---|
| test_caps | `google_play_now_has_a_governor` | `run()` declares `max_run_usd`; `_over_budget` is **defined AND called** |
| test_caps | `a_zero_price_cannot_fire_the_cap` | an `If` in `_over_budget` over both inputs, with a falsy return |
| test_caps | `youtube_takes_the_smallest_of_every_ceiling` | the top-level key appears as a read key; a `min()` call exists |
| test_headless | `the_parameter_is_gone_from_every_layer` | arg / keyword / Name / Attribute / non-docstring Constant |
| test_meter_guard | `a_candidate_accumulates_every_free_caption` | a `.setdefault("free_captions", [])` whose default is an **empty** list |
| test_meter_guard | `the_recheck_is_wired_into_the_runner` | `load_index` before `append_many` by lineno; `skipped_raced` **assigned** |
| test_repost_finder | `there_is_no_email_path_at_all` | the same four shapes, docstrings excluded |

### THE ONE NUMBER: AST 10/10, text 3/10

`scratch/infra018_plants.py` applies each guard's own defect to a **copy** of the production
file — nothing under version control is mutated, since three of these modules are held by other
rounds — and runs BOTH the old text form and the new parsed form against the same file. Five
plants are real defects that must go red; five are behaviour-preserving edits that must stay
green.

```
AST guards  10/10 correct
TEXT guards  3/10 correct  — 7 of the same 10 edits would have been called wrongly
```

The seven split **both ways**, which is the argument in one line:

* **passed a real defect** — a governor defined and never called (a write-only cap, the exact
  bug `test_caps.py` exists to prevent); a counter surviving only in a comment; the
  `resolve_emails` knob resurrected as a live config read.
* **failed a correct edit** — a reformat across two lines; a variable rename `root` →
  `lib_root`; a docstring correctly documenting a removal.

### The guard that punished the documentation, and missed the bug in the same expression

`test_there_is_no_email_path_at_all` could only pass by slicing the documentation out first:

```python
src.split('"""', 2)[-1].split("# NOTE")[0]
```

That hack exists because `repost_finder.py:101` carries a `# NOTE:` saying there is
deliberately no `resolve_emails` knob and why. The guard had to hide correct documentation
from itself to pass.

And the slice searched only the ~86 lines between the module docstring and the first NOTE
marker — leaving **~1,350 lines unsearched**. The plant that resurrects the knob as a real
config read near `account_consistency()` goes **green** on the text form and red on the parsed
one. It punished the documentation and missed the defect, in one expression.

`tests/test_guard_resolution.py`'s `BASELINE` is now **empty**. Its own
`test_the_baseline_has_not_gone_stale` is what forced the emptying — it went red the moment the
sixth conversion landed, because a baseline entry for a guard somebody has since fixed is a lie
about the code.

### The detector under-reports by at least three

Three of the guards converted here were **not** in INFRA-017's six. Its `_identifier_shaped`
rejects any needle containing a space or a parenthesis, so
`"if not max_run_usd or not link_cost_per_call:"`, `'config.get("youtube_finder_max_run_usd")'`
and `"min(_caps)"` were invisible — all three in `test_caps.py`, one line from a guard it did
flag. They were converted because they sat in a file this round held; the rule itself is left
unchanged rather than widened blind, because widening it will surface more sites in files other
rounds hold.

---

## 2. The duplicate funnel card — and the panel underneath it

`_canon_funnel()` already existed and was already used for `same_funnel_as_marker`. It was
never applied to the emitted rows. So markers said `repost_finder` / `spotify_finder`, headless
runs said `repost` / `spotify`, `collect()` in app.js deduped on the RAW name, and the grid drew
both. Measured on live state: **10 idle rows for 6 funnels**, `repost` appearing five times.

**Reconciled by pid, not by name, exactly as required.** `_reconcile` is untouched and still
merges per process. `_funnel_cards()` is a second, narrower view on top of it, for the grid
alone — because "what funnels exist" and "what is running" are different questions:

```
funnel_cards   one per canonical funnel   -> the "Every funnel" grid
running        one per live PID           -> the live panels and the Stop control
```

A collapsed card carries `live_runs`, `records`, `pids` and `names`, so two concurrent repost
runs are **one card that says two processes are live** — pinned by
`test_two_concurrent_runs_of_one_funnel_stay_two_runs`. A live run always wins the card over a
dead one, so a card can never report idle while that funnel is running.

### `running` was a field nobody sent

Checking what `runCard()` actually tests turned up something larger. It tests `r.running`.

**No row has ever carried that key.** The server emitted `status` and `stale`; the page tested
a third name that did not exist. `undefined` is falsy, so:

* "Runs live now" read **0**, always;
* "Live runs" and "Running now" read **"Nothing is running"**, always;
* every funnel card rendered as idle or stale;
* and the **Stop control was never rendered**, because it is gated on `live && r.pid`.

An operator who could start a run from this page had no way to end one from this page.

Measured at the moment of the fix: `/api/now` reporting
`repost_finder, pid 13500, status running, stale False` in the same response the page drew as
"Nothing is running". Derived server-side, like `stale`, because liveness is the server's
answer — it owns the `OpenProcess` probe.

After, on the live page: grid **6 cards / 0 duplicates**, live panel 1 card,
**`Stop run (pid 13500)`** present, KPI "runs live now" = 1.

---

## 3. Third rows-versus-records sweep — clean, and now structural

`scratch/infra018_counts.py`, **30 checks, all green**, every number computed twice: once by the
endpoint, once by reading the file with no dashboard code in the path.

The two previous defects were found by checking the panels somebody thought to check. So this
sweep adds a structural pass: **every counting loop in `dashboard/server.py` enumerated by AST**
and labelled record-count or line-count. **32 loops, exactly one line loop** —
`_compute_series():1979`, which increments `["lines"]` beside `["clips"]` and is the labelled
diagnostic INFRA-017 shipped on purpose. **No third instance exists.**

New this round: one card per funnel with no duplicates; `live_runs` equal to live processes;
every row carries `running`; no row claims running while stale.

---

## 4. `test_render_argv` — resolved as a decision, not a caller

`--force-caption` is MEMEBOT-082's and **uncommitted**: 3 occurrences in the worktree copy of
`edit.py`, 0 at HEAD. Wiring a caller would commit a caller for a flag that does not exist, so
it is recorded in `NOT_WIRED` with a real reason: `white_frame` ships `caption.enabled: false`
because MEMEBOT-076 measured the clip's own burned-in caption better on 9 of 10, the pipeline
renders the measured-better variant, and forcing a second caption over it is a per-render human
judgement rather than a value the pipeline computes.

Added `test_no_not_wired_entry_names_an_option_edit_py_no_longer_accepts` so the entry cannot
outlive the flag. `--help` is excluded with its reason: argparse adds it implicitly, so it is
absent by construction, not by drift.

---

## 5. Instruments

One of mine was wrong again, and it is the third round in a row. `infra018_plants.py`'s
`record()` set `ok = ast_fires` for every row, so the four behaviour-preserving plants printed
**FAIL** while the summary underneath correctly reported 10/10. A harness whose per-row verdict
disagrees with its own total is not reporting. The expected direction is now an input.

The server was **restarted before every screenshot** — INFRA-017 shot a stale process and drew
the old chart, entirely plausibly.

---

## Honest limits

* **INFRA-017's detector under-reports** — at least 9 sites exist, not 6. Left unwidened.
* **`tests/test_caps.py` and `tests/test_render_argv.py` were UNTRACKED** — never committed,
  ~19 hours old, unclaimed, and running in the suite the whole time. This round commits both,
  removing an orphan hazard nobody had noticed.
* **`clip_pipeline.py` and `edit.py` were not touched**, per the precondition.
* Zero external requests and zero console errors at all four screenshot widths, every tab;
  0 of 42 tab/width combinations overflow; 18 accessibility checks still pass.

## Still broken, and whose file

* **`--force-caption` is still uncommitted** — `memebot/scraper/edit.py`, MEMEBOT-082's. The
  NOT_WIRED entry is correct either way and self-cleans if the flag goes.
* **The guard detector's needle rule** — `tests/test_guard_resolution.py`, mine, deliberately
  not widened this round.
* **`MIN_DURATION_S` 5.0 vs `edit.py`'s 8.0 floor** — `memebot/scraper/`, MEMEBOT-071/072's.

## Suite and spend

`PYTHONUTF8=1 python tests/run_all.py`, discovery rule: **every `test_*.py` under `tests/` and
under any nested `<pkg>/tests/` directory** (MEMEBOT-026 — a suite count without its discovery
rule is not a count).

**ALL GREEN — 149/149 suites, 5,036 checks, 412.8 s**, with five rounds in flight.

That includes `tests/test_render_argv.py`, which was the single red INFRA-017 inherited and
could not take. The tree has no red suite for the first time across these four rounds.

Directly affected and green: `test_dashboard` + `test_dashboard_video` + `test_guard_resolution`
+ `test_caps` + `test_meter_guard` + `test_render_argv` = **199 tests**; plus `test_headless`
(46) and `test_repost_finder` (100). `config.json` byte-identical, campaigns untouched.

**Spend this round: $0.0000.** No paid call was made.
