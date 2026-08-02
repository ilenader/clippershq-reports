# INFRA-019: the decision log landed in the pipeline — and the patch was wrong by 47

**Date:** 2026-08-02 · **Type:** Land + correct + measure · **Spend: $0.0036 of a $0.10 budget**

Claim filed via `tools/claim.py`, **18 paths registered individually** with repeated `--write`.
Registry read with `tools/claims_read.py --holders` (not `claim.py`), plus
`git status --porcelain` on every target.

**`clippershq/clip_pipeline.py` was taken with disclosure.** The brief's condition was "verify
clean and free first; if ' M', report and stop". Porcelain showed **no entry** — clean. BL-899
still held it at **1,301 minutes** (21.7 h), its own files untouched for 1,298 and
`scratch/bl899_findings.md` never created; its stated intent (BL-894's `dict_of` work) has been
completed since by MEMEBOT-042/072/081/088, and the file has been committed three times by
other rounds while that claim stood. `claim.py` printed the advisory and this is it, said out
loud.

---

## 1. The patch landed — and measuring it first was the point

`git apply --check` was clean, exactly as BL-983B left it. It was applied, and then the numbers
it produced were checked against the library rather than trusted.

**`gate_report()` counts REASONS, not CLIPS.** A clip refused for two things contributes two:

```
clips in library        2,661
clips FAILING the gate    731
sum(gate_report)          778     <- reasons, not clips
clips with >1 reason       45
```

The patch fed that histogram straight into a stage whose `emitted` is DERIVED as
`took − Σdrops`. So it recorded **1,883 survivors where 1,930 actually reach the ranker** — the
decision log misreporting by 47 in the first number it prints. That is the exact class of
defect the module was built to catch, in the module's own wiring.

Landed instead: **one drop per CLIP**, attributed to its first refusal, with the full
co-occurring histogram kept as a note. Nothing is lost and the arithmetic holds.

## 2. Every stage, not two

The patch instrumented `gating` and `ranking` and stopped. Every `continue` in the render loop
is a row leaving the pipeline, and four of them said nothing. Now: **gating → ranking →
retrieval → render**, with `out()` supplied explicitly on the last two so `unaccounted` is able
to fire at all.

A real run, n=1, one billed re-fetch, **$0.0012**:

```
gating       in=2661  out=1926  dropped=735   unaccounted=0
      370  duration Ns outside [N N]
      139  no audio class — the renderer refuses rather than guess
      114  cover frame is uniform — no imagery to read
       89  already rendered
      ...  and 3 more, each named
      note: 45 clip(s) failed for more than one reason; each counted once under its
            first. Full reason histogram: ...
ranking      in=1926  out=3     dropped=1923  unaccounted=0
     1923  not needed: over-provision cut at 3 (want 1 x 3)
retrieval    in=3     out=1     dropped=2     unaccounted=0
        2  not attempted: stopped early (target reached)
render       in=1     out=1     dropped=0     unaccounted=0
      note: song tier used: matched=1
produced 1   spend $0.0006 of $0.01 cap
no silent stages, nothing unaccounted for.
```

## 3. THE ONE NUMBER: a self-balancing drop silently disabled the guard

The over-provision cut was first written as `_cut = _survivors - len(cands)` — the observed
difference. That is **self-balancing by construction**: whatever the ranker loses, for whatever
reason, lands inside a drop defined as "everything missing".

Planted the `dict_of` shape — `rank_candidates` monkeypatched to discard 11 of 12 rows
recording nothing — and got **`unaccounted = 0` and no problem reported at all.** The guard was
disabled on that stage by the line meant to keep it quiet.

Computed from the RULE instead (`min(survivors, want × OVER_PROVISION)`), the same plant gives
**`unaccounted = 8` and an `UNACCOUNTED` problem in the summary.**

The lesson is sharper than the fix: **a drop computed from the gap can never leave anything
unaccounted**, which makes the invariant decorative. Pinned by
`test_the_over_provision_drop_cannot_absorb_a_silent_loss`.

## 4. The three planted failures, through the real path

`scratch/infra019_plants.py` — 5/5 explained by the log alone, fetches injected, **$0.00**.

| plant | what the log says, with no source read |
|---|---|
| A. silent drop | `ranking unaccounted=8`, `PROBLEM UNACCOUNTED` |
| B. missing audio_class | `gating: no audio class — the renderer refuses rather than guess` |
| C. unreachable media | `retrieval: media unreachable: not_found` |
| D. no matching song rule | **not a drop at all** — `pick_song` returned `lru_corpus` |
| D2. the tier is named | render-stage note: `song tier used: matched=1` |

**D corrects BL-983B.** It reported "1 no song rule matches" as a gate reason. Through the real
path it is not one: `pick_song` DEGRADES a tier rather than failing — failure mode 2, degrade
and record, never block — so such a clip still becomes a finished video and no stage drops it.

That is **worse** than a refusal. MEMEBOT-067 measured that a fallback render writes a join key
the store cannot hold, so the video can never earn rotation: a silent, plausible, permanently
useless deliverable. The log had nowhere to say so, so the render stage now counts the tier of
every render and names the fall-throughs explicitly.

## 5. Redaction

`scratch/infra019_redaction.py` — 11 checks, all green.

Live artifact: 6 runs, 336 string leaves, **0 credential values, 0 emails, 0 handles**. The
secret scanner passes under `--profile private` (the parent repo's question) and under
`--profile public`.

Then adversarially: **21 real config credential values**, a real-shaped email and a handle
pushed through `drop(**example)` and `note()` — the two paths that take free text. Nothing
survives; the markers are present in the **in-memory** object, so redaction is at record time
rather than write time; and redacted text is MARKED rather than deleted, because a silently
dropped example is loss, not redaction.

## 6. The dashboard

`/api/decisions` plus a two-card panel on History: the runs list (made / dropped / unaccounted
/ cost) and the per-stage detail with every drop by name. Its own fetch, so an unreadable
runs.json leaves exactly that card waiting.

`unaccounted` is styled as an alarm **and always carries the word** — "none" when zero, the
count when not — so the state never depends on colour. Verified live: 12 rows, one selected,
table caption present, `aria-live="polite"`, **zero console errors, zero external requests**,
0 of 42 tab/width combinations overflow, 18 accessibility checks pass.

## 7. The fourth time a test wrote production state

My own tests wrote **`dashboard/static/runs.json`** — the artifact the dashboard serves, capped
at `KEEP_RUNS = 25`, so synthetic runs do not merely pollute it, **they evict real ones**.
**18 of 24 runs in the live file were mine** before anyone looked.

The others were INFRA-011's settings save landing in the live `config.json`, the status markers
landing in the real `scratch/`, and the suite putting 155 phantom rows in the money ledger.
Each time the fix was the same line: make the path redirectable.

**And the env var alone was not enough.** I set it in my test file;
`tests/test_clip_pipeline_entrypoint.py` calls `run_batch` too, had never heard of the
variable, and re-polluted the file from a suite that did nothing wrong. Patching each caller is
discipline, and discipline is what had just failed. So a test process now gets a temp
destination **by default** (`_under_test()`), failing safe toward losing a log rather than
evicting a real run. Verified: that suite's 32 tests now leave the live artifact untouched.

---

## Honest limits

* **The patch was corrected, not just landed.** Both faults — the 47-row error and the missing
  render stages — were found by measuring after applying, not by `git apply --check`.
* **Three of my own instruments were wrong first**: the over-provision drop that disabled its
  own guard; a plant that passed because the injected fetch failed before the code under test
  ran; and a terminal bookkeeping stage that made a two-video run print `produced 0` and raise
  a false SILENT. All three are described above and each has a regression test.
* **`dashboard/static/runlog.html`** (BL-983's standalone page) is untouched; it reads the same
  file and still works. The brief asked for the dashboard run detail, which is what was built.
* **`tests/test_clip_pipeline_entrypoint.py` was not edited** — the auto-redirect covers it
  without claiming another round's file.
* **Spend: $0.0036** of the $0.10 budget, across four real runs. Every plant harness injects
  its fetchers and bills nothing.

## Still broken, and whose file

* **BL-899's claim is still open on `clip_pipeline.py`** at 21.7 h with no work under it. The
  file was taken with disclosure; releasing the claim is the owner's call.
* **`MIN_DURATION_S` 5.0 vs `edit.py`'s 8.0 floor** — `memebot/scraper/`, MEMEBOT-071/072's.
* **The guard detector under-reports** — `tests/test_guard_resolution.py`, mine from INFRA-018,
  still deliberately not widened.

## 8. A test fixture is committed into memebot's history — found, attributed, not mine

`tests/test_verify_claims.py::test_it_reads_HEAD_and_not_the_working_tree` appends a marker
function to `memebot/scraper/edit.py`, checks that a working-tree-only symbol does NOT verify,
and restores the bytes in a `finally`. Its own comment warns that it perturbs a file another
round owns.

**Another round committed `edit.py` while that marker was in the working tree.** Measured:

```
grep -c BL921_WORKING_TREE_ONLY_MARKER memebot/scraper/edit.py   ->  2  (lines 2980, 2984)
vc.head_text("memebot/scraper/edit.py") contains the marker      ->  True
git -C memebot log -S BL921_WORKING_TREE_ONLY_MARKER             ->  1319228 MEMEBOT-094
```

So the symbol genuinely IS at HEAD, the test's premise is false, and it fails permanently
until someone removes it from memebot's history. It is in the shipped renderer twice, from two
interleaved runs. **This round never touched `memebot/`** — the three memebot commits are
MEMEBOT-094, MEMEBOT-064 and MEMEBOT-086.

**RESOLVED WHILE THIS ROUND WAS WRITING.** MEMEBOT-094 removed both stubs in memebot commit
`fbeb1ec` ("remove a test marker I committed into the renderer"); `git -C memebot show
HEAD:scraper/edit.py` now contains the marker zero times and `test_verify_claims.py` is green.
Recorded because the finding stands whatever happened next: a test that mutates a live file
cannot be safe in a tree where eleven rounds commit concurrently, however careful its
`finally` is, and this one put a stub function into the shipped renderer's history twice.

## 9. A dashboard test asserted more than its docstring, and was vacuous until today

`test_an_absent_marker_is_unknown_never_failed` forbade **any** row from carrying
`status: failed`. Its docstring says something narrower and correct: a funnel with *no marker*
must read `unknown`, because calling it failed invents a failure and hides the funnels that
really ran. `/api/now` passes `status` through verbatim by contract, so a run that really
failed is reported as failed — and during this round one did (`repost_finder`, pid 13500,
marker on disk `failed`, note "funnel logged 1 error(s)").

It had passed for as long as no funnel happened to fail while the suite ran. **A test that
only holds while the system is healthy is not testing the system.** Narrowed to the absent
case, plus a companion asserting that the absent case is actually exercised — a guard over an
empty list passes vacuously.

## Suite and spend

`PYTHONUTF8=1 python tests/run_all.py`, discovery rule: **every `test_*.py` under `tests/` and
under any nested `<pkg>/tests/` directory** (MEMEBOT-026 — a suite count without its discovery
rule is not a count).

**ALL GREEN — 154/154 suites, 5,100 checks, 487.4 s**, with five rounds in flight.

An earlier run during this round was 151/154. All three reds were run individually and none
was this round's: `test_manifest_prose_refused.py` and `test_suites_parse.py` both pass
standalone (they walk `tests/` while other rounds write into it — MEMEBOT-093 reported the
same flake independently in the same window), and `test_verify_claims.py` was §8, since fixed
at source by MEMEBOT-094.

A fourth red appeared when the directly-affected suites were run together —
`test_an_absent_marker_is_unknown_never_failed`, §9 — and was fixed rather than attributed,
because it is a real defect in a test this round holds. After that fix, the five suites this
round touches run **205 tests green together**: `tests/test_pipeline_decision_log.py` (15,
new), `tests/test_clip_pipeline_entrypoint.py` (32), `tests/test_decision_log.py`,
`tests/test_dashboard.py` and `tests/test_dashboard_video.py`.

The 154/154 figure is the post-commit run, taken after every fix in this report had landed.

`config.json` is byte-identical (0-byte diff) and the campaigns block is untouched.
