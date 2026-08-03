# INFRA-026 — both briefed items were already shipped, so I verified instead, and found six defects doing it

**Date:** 2026-08-03 · **Type:** Dashboard verification + fixes · **Spend:** **$0.00** (no paid calls)

Preconditions: `tools/claims_read.py --holders dashboard` → **FREE**; `git status --porcelain` clean on `dashboard/` except the pipeline-written `static/runs.json`. Claimed under **INFRA-026** — `claim.py` refused **INFRA-024**, which has a published report on origin under a name the registry had already recycled. Two namespaces, and it checked both.

**Server on port 8847.** 8787, 8797, 8807, 8817, 8827 and 8837 were all held by concurrent rounds. **To find the live one:** `netstat -ano | grep LISTENING | grep 127.0.0.1:88` and match the pid to a python process — the port is a `--port` argument, not config, so it is not discoverable from the repo.

---

## 1. Verify before building — and both briefed items were already there

The brief asked me to surface the decision log and the outcome loop. **Both were already on the page, complete**, exactly the INFRA-022 precedent the brief cited:

- **The decision log** — `index.html`'s "Why rows were dropped" card renders every stage's `in` / `out` / each drop **by name**, the `SILENT` flag and `unaccounted`, from `/api/decisions`, with its own fetch so an unreadable `runs.json` leaves that one card waiting. Landed by **INFRA-019**.
- **The outcome loop** — the "After posting" card renders the headline in words, the best post with **its song, its hook window and its url**, the lead half against its 4–8% expectation, and labels `bias_map == {}` as **CORRECT**. Landed by **BL-1022**.

I re-shipped neither. What I did instead was try to break them, and that is where the round's value is.

**Item 2's sub-clauses, checked individually rather than assumed:** the "NOT ENOUGH DATA in words" case prints *"No video carries a number yet. Nothing is broken — export the sheet, fill it in, and import it."* The lead half prints *"Nothing marked sent yet"* — and critically it **does not** print the `reply_rate: 0.0` the API returns on a zero denominator, because `renderOutcomes` guards on `!L.totals.sent` first. A 0.0% rendered beside a "4–8% expected" column would have read as catastrophic failure of a message nobody has sent yet. That guard was already right.

---

## 2. The fifth rows-versus-records check: **every count is correct**, and the only counting errors were mine

`scratch/infra026_verify.py` recomputes every figure from the raw source file and compares. Final run: **ALL COUNTS AGREE.**

| endpoint | figure | hand-count | shown |
|---|---|--:|--:|
| `/api/library` | clips (distinct `clip_id`, rev-resolved) | **2,728** | 2,728 |
| | shards / accounts | 54 / 241 | 54 / 241 |
| `/api/videos` | attempted (distinct records) | 289 | 289 |
| | rendered / failed / pending | 224 / 63 / 2 | 224 / 63 / — |
| | `by_source` production / test / unstamped | 98 / 20 / 106 | 98 / 20 / 106 |
| | `cost_lifetime_usd` | 0.1602 | 0.1602 |
| `/api/outcomes` | `n_records` / `n_with_outcome` / `n_with_numbers` | 289 / 22 / 0 | 289 / 22 / 0 |
| `/api/decisions` | every stage `unaccounted == in − Σnamed − out` | 0 violations | 0 |

**The library is 2,728. Any 2,003 or 2,661 is stale** — 2,661 was true when I rendered thirty videos yesterday afternoon.

### I made the rows-versus-records error twice, in the checker written to catch it

**First:** I folded the ledger on `record_id`. On this file `record_id` exists on the 48 `kind: outcome` rows **only** — all 529 render rows carry `render_id`. The fold degenerated to one-record-per-line and reported 551 "records" for 577 lines, producing ten confident mismatches against a dashboard that was right about all ten. The dashboard delegates to `clip_pipeline.read_records` — the renderer's own resolver — which is the correct design and the thing I second-guessed.

Reconciled exactly: **226 `ok` LINES → 220 `ok` RECORDS + 4 legacy rows with no status but a real `output` = 224 finished.** The line count is the wrong answer and it is the one I reached for first.

**Second:** I asserted `rendered + failed == attempted` with the note *"a third status would break this and go unnoticed"*. It then broke, on **`pending`** — a render paid for and started but not landed. Genuinely attempted, genuinely neither. The dashboard's `attempted` was right; my identity was missing a term.

**Third, and it is the one worth generalising:** five "mismatches" in one run were a **moving denominator**. Another round was rendering, and `runs.jsonl` grew 265 → 278 records between my read and the server's. The checker now **pins the file and refuses to report at all** if it moves under the check, rather than publishing a diff of two different files as a defect.

---

## 3. Six defects found, all fixed

**① `/api/decisions` truncated silently.** 21 runs on disk, 12 returned, and **nothing in the payload** the page could use to say so. Its own docstring claimed the endpoint *"gives the contract a place to live… the cap"* — and the cap was the one thing it never reported. This panel is the answer to *"why did it only make 3 videos?"*, so a run below the cut is that question going unanswered on a page that looks complete. Added `runs_total` / `runs_shown` / `limit`, extended the note, and put it in a `<caption>` the table did not have: **"Pipeline runs: the 12 most recent of 21 on the decision log."**

**② Clicking a decision row loaded the WRONG run into "Run detail".** The router matched `tr.pick`, which **both** tables emit; only the past-runs table carries `data-run`, so for a decision row `Number(null) === 0` and `showRunDetail(window.__runs[0])` repainted the History tab with a **real, different run's numbers** under the row the operator did not click. The reset loop also cleared `aria-selected` across both tables at once. `Number(null) === 0` is named at the top of `app.js` as the shape that must never recur — and it had recurred in the row router itself. Scoped to `tr[data-run]`, and **asserted** in the screenshot pass, because a screenshot of this bug looks perfectly correct.

**③ A poll moved the operator's selection.** `renderDecisions` called `showDecision(runs[0], 0)` unconditionally on every redraw, so the moment any run finished the panel jumped to the newest one while the operator was reading a different one — and every `data-dec="N"` had already re-pointed at a different run. Selection is now remembered by **`run_id`**, not array index.

**④ The hand-audit panel was pinned to one round's filename.** It read `scratch/mb095_watch.json` and nothing else, so it could only ever show MEMEBOT-095's result. It was showing **13 of 30** while **MEMEBOT-108's published audit sat on disk at 10 of 30** against a newer render stack. A quality figure that cannot move is worse than none, because it looks maintained. Now takes the newest audit on disk, handles both file shapes (`{postable:[...], n}` and `{postable:N, of:M}`), names the file on screen, and still invents nothing.

**⑤ `measured_at` was the file's mtime, labelled as a measurement date.** INFRA-022 put a date on that panel *precisely* so the figure reads as a sample taken on a day; a date derived from the wrong event defeats that — any process rewriting the file re-dates a number nobody re-measured. Now carries `date_basis` saying what it actually is.

**⑥ Decision-log drop rows sat under the wrong column headers.** Headers are `stage | in | out | dropped | unaccounted`; each drop row put the **count** under `in` and the **reason** spanning `out|dropped|unaccounted`. Read aloud that is *"in, 382"* for a drop count — on the one panel whose entire job is explaining where rows went. Reason now under `stage`, count under `dropped`.

---

## 4. The accessibility review, and four claims in the code that were false

I ran the accessibility team over the five front-end files before editing them. It returned a long audit; I applied what was in this round's scope and am **naming the rest rather than silently dropping it**.

**Applied:** the 5-second re-announce loop on `#ocHeadline` (`textContent =` replaces the text node, so `role="status"` re-announces even when the string is byte-identical — a `setText` guard mirroring the existing `_sigs` discipline); nine `.tablewrap` scroll containers with **no keyboard access at all** (`markScrollers()` adds `tabindex` only while a container actually scrolls, so no dead tab stops); `#decisionDetail` demoted from a live region that announced a whole multi-row table on every poll; `runlog.html` had **no `<html>` element**, therefore no `lang` (3.1.1) and no viewport meta.

**Contrast, measured rather than trusted:** `--dimmer` was commented *"4.6:1 — only ever on large or decorative text"* and **both halves were false** — 4.56:1 is the ratio against the one surface it is never used on, and measured where it appears it was **3.61–4.38:1** across five normal-size text sites. `.btn.primary`'s label was **3.79:1** on the upper half of its own gradient. Both fixed by token change.

**The hatch that never rendered.** `charts.js` sets `class="ch-bar-b"` and `fill="url(#ch-hatch)"` on the same rect. An SVG presentation attribute has specificity 0 at the start of the author origin, so `.ch-bar-b{fill:...}` beat it **unconditionally**: the `<pattern>` was built, appended to `<defs>`, and never painted. Metered and reconstructed spend — which `charts.js` says must never be summed — rendered as two flat fills separated by hue alone, and `index.html` printed a "hatched" tag next to a bar that wasn't.

**False claims corrected on the record:**

| where | claimed | actually |
|---|---|---|
| `index.html` outcome card | "there is one implementation now" | **two** resolvers — see §5 |
| `index.html` `#playerNote` | the describedby line "is the text alternative available" | provenance, not content; confers no conformance |
| `app.css` `--dimmer` | "4.6:1 — only ever on large or decorative text" | 3.61–4.38:1, five normal-text sites |
| `app.css` tab | selected is "border + **weight** + colour" | there was no weight change |

**OUT OF SCOPE, FOR WHOEVER OWNS `tests/`:** `tests/test_dashboard_video.py:418` is named `test_the_video_element_has_a_text_alternative` and asserts only that the string `aria-describedby="playerWhat playerNote"` appears in the HTML. **A green test whose name claims a WCAG obligation is met is how that belief survives review.** The renders genuinely ship with no captions, no transcript and no audio description, and the "no speech" premise is false for the `duck`/`keep` audio treatments. I rewrote the on-page sentence to disclose the gap; I did **not** touch `tests/`, which is outside `dashboard/` and outside my claim.

---

## 5. One number, two derivations — do not "unify" them

The outcome card's comment said *"there is one implementation now."* Measured on the live ledger:

```
outcome_loop.resolve       -> 289 records   has_outcome = 22
clip_pipeline.read_records -> 289 records   has_outcome =  0
same key set? NO — the intersection is FOUR
```

`resolve` keys on the **output path**; `read_records` keys on **`render_id`**. Both panels print the same total on the same tab, and they agree **by arithmetic coincidence on this file**, not by construction.

**The asymmetry is load-bearing in one direction.** Outcome rows carry the output path as their `record_id`, which is the only reason an imported outcome attaches to a render at all — hence 22 versus 0 on the same file. Unifying both onto `render_id`, which is the obvious tidy-up, would **silently detach every outcome the operator has typed in**: the exact loss that card exists to make visible. Written into `index.html` beside the claim it corrects.

---

## 6. Every existing property, re-asserted

| property | evidence |
|---|---|
| **zero external requests** | 0 at 1920, 1280 **and 700** — every request off-origin fails the pass |
| **zero console errors** | 0 at all three widths, including `pageerror` |
| **no overflow at 700px** | `scrollWidth − clientWidth == 0` on **all 7 tabs at 700px** |
| **one tabpanel visible** | 1 on all 7 tabs × 3 widths (INFRA-015's 12,232px stack, as a number) |
| **money(null) → "unknown"** | `money()` returns null for `null`/`undefined`/`''`; `moneyCell` emits an aria-hidden dash + a visually-hidden "unknown" |
| **per-pid liveness via OpenProcess** | `ctypes` `OpenProcess`, no subprocess — `tasklist` was 2.77s each / 40.2s in bulk |
| **panels render independently** | each endpoint has its own promise; `Promise.all` only reports completion |
| **in-place poll keeps focus** | `setHTML`'s `activeElement` guard, plus ③ above which was the one thing still moving under the operator |
| **no credential on any endpoint** | 11 endpoints scanned; every long opaque value classified — all run ids, clip ids and a `backfill_vision_tokens_est` **label**. Zero credentials |
| **the dashboard NEVER advances rotation** | **40 polls** of `/api/rotation` + `/api/videos` + `/api/audit`: ledger **sha256 unchanged**, rotation output **byte-identical** |

**21 screenshots** — 7 tabs × 3 widths — in `scratch/infra026_shots/`, **after restarting the server**. That restart is not ceremony: an edited `api_decisions` returned the OLD payload on my first check because uvicorn had already imported the module. INFRA-015 recorded that trap; this round hit it live and caught it because the assertion was on the payload, not on the picture.

---

## Proof

| claim | evidence |
|---|---|
| both briefed items already shipped | "Why rows were dropped" (INFRA-019) and "After posting" (BL-1022) render fully; neither re-shipped |
| every count hand-verified | `scratch/infra026_verify.py` — **ALL COUNTS AGREE**, library **2,728** |
| the errors were mine, twice | `record_id` fold (551 vs 289) and the missing `pending` term, both named in the harness |
| a moving denominator is not a defect | stability gate refuses to report if the ledger moves under the check |
| the silent cap | `runs_total: 21, runs_shown: 12`; caption reads "the 12 most recent of 21" |
| the wrong-run bug | asserted in the screenshot pass: decision row clicked, `#runDetail` **unchanged** |
| the stale audit | was `13 of 30` from `mb095_watch.json`; now **10 of 30** from `mb108_verdict.json`, file named on screen |
| the hatch | `.ch-bar-b{fill:…}` beat the presentation attribute at specificity 0; removed |
| rotation unmoved | 40 polls, ledger sha256 identical, rotation byte-identical |
| screenshots | 21 images, **0 console errors, 0 external requests, 0px overflow at 700px** |
| suites | dashboard **153/153 green** (99 + 11 + 43); parent suite **KILLED** with five other `run_all` in flight — see Honest limits. No orphan probe left behind (`ls tests/bl932_probe_*` clean) |
| campaigns / config | `campaigns/` and `config.json` untouched; config parses, 161 blocks |
| spend | **$0.00** — no paid call in this round |

---

## Six-line summary

```
1 VERIFIED     both briefed items were ALREADY SHIPPED (decision log INFRA-019, outcome card
               BL-1022) — the INFRA-022 precedent held. Re-shipped neither; tried to break
               them instead, which is where this round's value is
2 COUNTS       fifth rows-vs-records check: EVERY dashboard count is correct. Library 2,728.
               The only counting errors were MINE, twice — I folded on record_id, which only
               the 48 outcome rows carry, and got 551 records for 577 lines
3 SIX DEFECTS  a silent cap (12 of 21, never reported); clicking a decision row loaded the
               WRONG run via Number(null)===0 in the row router; a poll moved the operator's
               selection; the audit panel was pinned to one filename and showed 13 of 30
               while MEMEBOT-108's 10 of 30 sat on disk; measured_at was an mtime; drop rows
               sat under the wrong column headers. All fixed
4 TWO RESOLVER the "one implementation" comment was FALSE: outcome_loop.resolve and
               read_records both return 289 and share FOUR keys. Do NOT unify onto render_id
               — has_outcome is 22 vs 0, and tidying it detaches every typed-in outcome
5 A11Y + LIES  applied the a11y review; corrected four claims the code made about itself,
               incl. a hatch that never rendered and a --dimmer comment wrong in both halves.
               OUT OF SCOPE: a test NAMED "has_a_text_alternative" that checks one attribute
6 PROPERTIES   0 external requests, 0 console errors, 0px overflow at 700px across 21 shots
               at 3 widths; rotation unmoved by 40 polls (ledger sha identical). Dashboard
               suites 153/153. Campaigns and config untouched. Spend $0.00
```

---

## Honest limits

- **The parent suite was KILLED, not merely unfinished** — and "killed" is a different fact, so it is corrected here rather than left as the softer one. **FIVE other `tests/run_all.py` processes were in flight simultaneously.** The three dashboard suites are green at 153/153 (99 + 11 + 43, verified twice) and my diff touches only `api_decisions` and `api_audit` — `git diff -U0` confirms no hunk near `api_now`, `_reconcile` or any other handler — but I am not claiming a full-tree green I did not see. A second full run was started after publication.
- **A killed `run_all` used to poison the tree for every other round, and no longer does.** BL-1023 recorded that `test_suites_parse.py` planted `tests/bl932_probe_<random>.py` and asserted on the *prefix*, so concurrent runs reddened each other and a killed run left an orphan that stayed red forever. **That is fixed**: the plant now goes to a `tempfile.mkdtemp(prefix="bl932_plant_")` with `addCleanup(shutil.rmtree)` and the assertion is scoped to that temp dir. I checked `ls tests/bl932_probe_*` after my run died — **clean**. Checked, not assumed, because the consequence lands on other rounds and not on me.
- **What still makes concurrent suite runs unreliable is live-state tests, not litter.** `test_dashboard.py::test_no_two_running_rows_share_a_pid` reads `/api/now` and asserts no two running rows share a pid; with nine rounds in flight there genuinely were duplicates. It failed once mid-round and passed minutes later with nothing changed.
- **My own audit-panel rewrite broke a test and I caught it from the suite, not from reasoning.** Scanning a directory instead of one fixed path collapsed "malformed" and "absent" into one message; `test_a_malformed_audit_file_is_refused_rather_than_guessed` was right to fail. The refusal now names the offending file.
- **I applied roughly half the accessibility findings.** Table `<caption>`s are still missing on six generated tables, row selection is still a focusable `<tr>` with no role or name, chart data tables are still destroyed and rebuilt twice per poll, and there is no `forced-colors` handling. Named, not fixed, and not counted as done.
- **The screenshots prove properties, not beauty.** They assert external requests, console errors, panel count and overflow. Nothing in this round asserts that a chart drew the right *shape*, and the `money` tab is a 9,040px page at every width — pre-existing, unmeasured, and not something I improved.
- **The hand-count agrees with the dashboard, which is not the same as both being right.** Both read the same file with the same resolver by design (that is the point — one implementation, not two that can drift). If `clip_pipeline.read_records` is wrong about what a record is, this round's check would not detect it.
- **The two-resolver finding is measured on one file.** That both return 289 today is the coincidence; that they share four keys is the structural fact. I did not change either resolver.

---

<!-- CLAIMS
file:   dashboard/server.py
file:   dashboard/static/app.js
file:   dashboard/static/app.css
file:   dashboard/static/index.html
file:   dashboard/static/runlog.html
file:   scratch/infra026_verify.py
file:   scratch/infra026_shots.py
func:   dashboard/server.py::api_audit
func:   dashboard/server.py::api_decisions
func:   dashboard/static/app.js::setText
func:   dashboard/static/app.js::markScrollers
-->

*An accessibility-agent review was requested by a hook and WAS run — the accessibility-lead team audited all five front-end files before any edit. Its applied findings are in §4; the ones I did not apply are named there rather than dropped.*
