# INFRA-022: 11 test renders were being counted as videos the system made — and two of the brief's four gaps were already shipped

**Date:** 2026-08-02 · **Type:** Dashboard, measured against the live server · **Spend:** **$0.00 · 0 paid calls**
Claim filed with **repeated `--write` flags** (12 paths). `claims_read.py --holders` and `git status --porcelain` on every target: all six dashboard source files **FREE and clean** (only `dashboard/static/runs.json`, a data file the servers write, was ` M` — untouched here). `config.json` unmodified (`sha256 5fb1a8a2…`, 161 keys, 5 campaigns unchanged). Server on **:8830** — 8787, 8797, 8807, 8817 and 8827 were all held by other rounds.

**Two of the four things the brief asks for were already on the page.** I checked before building, and say so rather than re-shipping them.

---

## 0. What was already there, verified not assumed

| the brief asks for | state before this round |
|---|---|
| **the decision log** — in/out/dropped-by-reason, the SILENT flag, `unaccounted` | **already shipped.** `showDecision()` on the History tab renders every stage with in / out / dropped / unaccounted, the `silent` tag, each drop by name, and the problems list. INFRA-019 landed it. |
| **BL-995's cap precision fix** | **already shipped.** `moneyCell(r.usd, 4)` and `money(r.cap_usd, 4)` — a $0.0018 cap renders as `$0.0018`, not `$0.00`. |
| **counts on the live library (2,661)** | **already correct.** `/api/library` returns `clips: 2661, accounts: 237`. |
| **ledger provenance split** | **MISSING — and it was wrong by 11.** |

`runlog.html` existed but was reachable only by typing the URL, and it read `runs.json` off disk while the card that shows the same thing reads `/api/decisions`.

---

## 1. The real defect: 11 test renders counted as production

`memebot/runs.jsonl` has stamped `source` since MEMEBOT-094. Every consumer was adding the populations together:

```
163 finished renders  =  106 unstamped  +  46 production  +  11 TEST
```

So **"163 videos made" overstated what the system actually produced by 11 renders that exist only because a test drove the pipeline.** Same family as INFRA-019's finding that test runs *evict* real ones from the capped `runs.json` — a test writing production state, one layer over.

`_ledger_state()` now returns `by_source` and `today_by_source`, and the Video tab shows them as three rows that are never added up:

```
PROVENANCE   LIFETIME  TODAY   WHAT IT MEANS
production        58      58   a real operator run
test              11      11   driven by a test — NOT a product of the system
unstamped        106      83   written before run_record stamped a source — UNKNOWN
```

**`unstamped` is a third series, not production.** Those rows predate the stamp, so the honest answer about them is *unknown*. Folding them in would be the `Number(null) == 0` shape this dashboard has already been burned by twice (INFRA-013 rendered a null spend as `$0.000`). The response carries `provenance_note` saying the series are never summed, because a number that must not be added up has to say so where it is read.

---

## 2. The fourth rows-versus-records check — and my own harness cried wolf first

Three counting defects have shipped on this page and every one looked plausible: INFRA-013's 5.7×, INFRA-016's `clips_by_month` counting lines (6,503 vs 2,003, 3.25×), INFRA-019's `gate_report` counting reasons not clips (off by 47).

`scratch/infra022_handcount.py` recomputes each panel **straight from the source file** and compares. First run:

```
rendered_lifetime    api=163   hand=159   *** DISAGREE ***
attempted_lifetime   api=217   hand=216   *** DISAGREE ***
failed_lifetime      api=54    hand=57    *** DISAGREE ***
```

**All three were my harness's fault, not the server's.** I keyed on `render_id` and counted only `status == "ok"`. The server resolves through `clip_pipeline.read_records()` (LAST-WINS by `rev`) and its `_is_finished` *deliberately* also counts legacy rows that carry no status but do carry an `output` — because `rendered_ok_ids()` counts them and the two readers must agree or the same file means two different things depending on who asks.

Re-run against the server's own documented rule:

```
rendered_lifetime    api=172   hand=172   OK
attempted_lifetime   api=227   hand=227   OK
failed_lifetime      api=54    hand=54    OK
library.clips        api=2661  hand=2661  OK
library.accounts     api=237   hand=237   OK

library rows-vs-records:  7,835 raw rows vs 2,661 records (2.94x)
```

**5 of 5 agree.** That 2.94× is the number that matters: any panel counting library *rows* would be ~3× over, and none is.

The counts move between runs (163 → 172 during this round) because other rounds are rendering. **A count here is a moment, not a property**, and the harness prints its own timestamped JSON so a later reader can tell which moment.

---

## 3. The audit, with its date

`/api/audit` reads the hand audit and reports **13 of 30 postable, 43.3%, measured 2026-08-02**.

The date is part of the number. A hand sample taken on a day against a render stack that changes hourly reads as a property of the system when the date is stripped (MEMEBOT-073's rule generalised). When the file is absent or malformed the endpoint says so and **invents no score** — a dashboard that guesses a quality figure is worse than one that admits it has none, and both cases are pinned by tests.

---

## 4. One decision log, one source

The main page now links to the full-page run log, and `runlog.html` was switched from reading `runs.json` off disk to `/api/decisions` — the same endpoint the card beside the link uses, with the server's limit, cache and `unavailable` handling.

**Linked, not duplicated.** Two renderers of one decision log is two things to keep in step; the card already shows the stages, the named drops, the SILENT flag and `unaccounted`. What was missing was a way to reach the standalone view without typing a URL — and, more quietly, the fact that a reader who *did* reach it could see a different set of runs from the card that describes it.

---

## 5. Every property, re-asserted per screenshot

Suite: **ALL GREEN, 158/158, 5,149 checks.** Screenshots: 14 — 7 tabs × 2 widths — taken **after restarting the server** (a pass once measured pre-edit code because the old process still held the port, so the harness now records the build it is shooting):

```
                1440px                       700px
external requests      0                          0
console errors         0                          0
horizontal overflow    0 px                       0 px      <- INFRA-017 found 9 here
```

Zero external requests is asserted by intercepting **every** request the page makes and failing on any host that is not `127.0.0.1` — not by reading the source for a CDN link. `money(null)` renders the word *unknown* on the tabs that have nulls (Run ×6, Clips ×2, Settings ×1); the single `$0.0000` on History is a **real** capped run that genuinely spent nothing, not a null formatted as zero.

Rotation is unchanged and still derived: `/api/rotation` reports 21 windows, 18 used, `writes_nothing: true`. The page cannot advance it — BL-888's ~1,440 phantom uses a day are impossible by construction, and `tests/test_dashboard_video.py` (43 checks) still passes.

---

## 6. What I got wrong

* **My hand-count harness reported three disagreements that were entirely its own.** I used a cruder definition than the server's documented one and nearly published a counting defect that did not exist. It was caught by reading `_is_finished` before writing the finding — the same discipline that MEMEBOT-093 needed for "38.2% scene-confirmed". The harness now applies the server's rule and prints the naive numbers beside it, labelled a definition mismatch, so it verifies instead of crying wolf.
* **I added `/api/audit` using `io.open` in a module that never imports `io`.** A 500 on the first request. Caught by hitting the endpoint after the restart rather than assuming the code was right.

---

## 7. Still broken, and whose

* **106 of 172 finished renders are `unstamped`** — provenance unknowable retrospectively. Only renders written after MEMEBOT-094 carry a source; the backlog cannot be recovered, only aged out.
* **`dashboard/static/runs.json` is ` M`** and written by whichever servers are running. Untouched here; it is a data file, not source.
* Six other dashboard/server processes are holding 8787–8827. Not mine to stop.

---

## SUMMARY

- **Shipped:** ledger provenance as three never-summed series (`by_source`, `today_by_source`) on a new Video card; `/api/audit` carrying **13 of 30 postable with its measurement date**; `runlog.html` repointed at `/api/decisions` and linked from the main page; `scratch/infra022_handcount.py` (5/5 panels hand-verified) and `scratch/infra022_shots.py` (14 screenshots, properties asserted per shot). **11 new checks.**
- **The one number: 11.** Eleven test-driven renders were being counted as videos the system made, inside a headline figure of 163. They are now a separate row that says *NOT a product of the system*.
- **Off-brief:** two of the brief's four gaps were **already shipped** — the decision log with drops/SILENT/`unaccounted` (INFRA-019) and BL-995's 4-decimal cap — and the library counts were already 2,661/237. I verified before building rather than re-shipping them.
- **Got wrong:** my hand-count harness reported three counting defects that were **its own definition mismatch**, not the server's; and I shipped `/api/audit` with an `io.open` in a module that never imports `io`, which 500'd on the first request. Both caught by measuring after the restart instead of trusting the code.
- **Still broken, and whose:** 106 of 172 finished renders are `unstamped` — provenance is unrecoverable for the backlog, only aged out. `dashboard/static/runs.json` is ` M`, written by the running servers; six other rounds hold ports 8787–8827.
- **Suite / spend:** `tests/run_all.py` **ALL GREEN — 158/158 suites, 5,149 checks** (721.6s), including `test_dashboard_panels.py` 11/11, `test_dashboard` 99/99 and `test_dashboard_video` 43/43. Screenshots: **0 external requests, 0 console errors, 0 overflow at 700px** across all 14. **$0.00, zero paid calls.** `config.json` unmodified, 5 campaigns unchanged.
