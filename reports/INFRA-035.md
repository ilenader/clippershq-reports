# INFRA-035 — the runner was never hanging. It was silent for 112 minutes.

**One number: 6,742 seconds.** That is the sum of every suite's runtime — the wall clock of
a `jobs=1` run, which is the default every stalled round used. **112 minutes.** And the
runner printed *nothing at all* until the last suite finished, so a 112-minute run and a
permanent hang were the same observation. Every round that waited twenty minutes and killed
it was killing a working run at **18% completion**.

`tests/run_all.py --jobs 4` now completes in **1,719 s (28.7 min)**, streaming a line per
suite, with **0 TIMEOUT**.

---

## 1. WHERE IT STALLS — and it is two defects, not one

### A. It printed nothing until every suite had finished

```python
_results = list(ex.map(_one, suites))      # drains EVERYTHING
for label, ok, secs, out in _results:      # only then does anything print
```

`list()` drains the whole iterator before the printing loop runs, and the serial branch
built its list the same way. So **one slow suite produced zero suite lines for the entire
run**, and killing it produced nothing to show for the CPU already burned.

This is the first fix because it is the one that makes every other diagnosis possible: **a
runner that buffers until completion cannot be debugged.**

### B. The per-suite timeout could not fire

There *was* a 600 s per-suite timeout. It was armed and it could not go off.

**Measured, not reasoned** (`scratch/infra035_probe.py`):

| probe | timeout | returned after | verdict |
|---|---:|---:|---|
| a suite that hangs on its own | 6 s | **6.2 s** | correct |
| the same hang, but a **grandchild** holds stdout | 6 s | **never — killed from outside at 260 s** | **>43× the limit** |

`subprocess.run(timeout=)` kills the **direct child** and then calls `communicate()` again to
drain the pipes. If the suite spawned a grandchild that inherited the stdout handle — ffmpeg,
git, a probe server, all of which this repo shells out to constantly — the write end is still
open, EOF never arrives, and the drain blocks **after the timeout has already expired**. The
code that was supposed to give up is itself stuck.

**Exposure: 48 of 204 suites (23.5%) spawn a subprocess.**

### Which one actually caused the observed stalls

**A, compounded by the serial default.** No suite timed out in any run here. The stalls were
a 112-minute silent run being killed at 20 minutes. B is the mechanism that would make a
stall *permanent* rather than merely long, and it is fixed because a 23.5% exposure surface
with a disarmed timeout is not something to leave standing.

---

## 2. THE FIX

**`run_suite` now returns within `timeout + DRAIN_GRACE`, unconditionally:**

* stdout is read on a **daemon thread**, so an unclosed pipe can never block the runner
* on timeout the **whole process tree** is killed (`taskkill /F /T` on Windows, `killpg`
  elsewhere) — a killed parent does not free the pipe
* the reader is joined with a **bounded grace** and then abandoned

A daemon thread stuck on a read costs one thread. A runner stuck on a read costs the project
its most quoted claim.

**TIMEOUT is a third state**, never folded into FAIL:

```
FAILED -- 5 red + 2 TIMED OUT of 204 suite(s)
  - tests/test_x.py   [TIMEOUT — did not finish, NOT a failure]

  2 suite(s) hit the 600s per-suite limit and had their process tree killed.
  A TIMEOUT is not a red: it means the suite never finished, so nothing was learned about it.
```

"Could not run" and "ran and failed" need different actions from whoever reads the summary,
and conflating them is the family this project has spent fifteen rounds removing.

**Results stream and persist.** Each result prints the moment it lands and is appended,
flushed and **fsynced** to a JSONL. Demonstrated: a run killed mid-flight left **178 results
on disk**, where the old runner left nothing after fourteen minutes of CPU.

---

## 3. `--jobs`, `--mine` AND THE DISCOVERY RULE

All three confirmed working:

* **`--jobs 4`** — 1,719 s versus a 6,742 s serial sum. The per-worker ledger sandbox
  BL-1037 added is untouched.
* **`--mine INFRA-035`** — *"attribution for INFRA-035: 7 declared path(s) …
  `tests/test_doc_citations.py` touches nothing you declared"*.
* **The discovery rule is IMPORTED, never restated.** `tests/test_run_all_runner.py` asserts
  `"scratch" in run_all.SKIP_DIRS` and that every discovered label starts `test_`, ends
  `.py`, sits under a `tests/` directory and is not under `scratch/`. One round restated the
  rule by hand and got **331 suites across 19 dirs** where the real answer is 204 across 3 —
  because `SKIP_DIRS` contains `scratch`.

`tests/test_run_all_runner.py`, **9 tests**, both directions: a passing suite passes, a
failing suite fails and is **not** called TIMEOUT, a plain hang times out, and the
grandchild case — the one that ran past 260 s — now times out within its bound.

---

## 4. THREE RUNS UNDER LOAD — all completed, none stalled, zero timeouts

| run | suites | red | **TIMEOUT** | wall | rounds in flight |
|---|---:|---:|---:|---:|---:|
| 1 | **204** | 7 | **0** | 1,719 s (28.7 min) | 6 at start, 5 at end |
| 2 | **204** | 7 | **0** | 1,189 s (19.8 min) | 5 at start, 6 at end |
| 3 | **204** | 5 | **0** | **820 s (13.7 min)** | 5 at start, 5 at end |

**Every one printed a verdict.** Before this round, two consecutive runs sat twenty minutes
and produced nothing at all.

### The red sets are now STABLE — which they were not

| run | reds |
|---|---|
| 1 | doc_citations · gate_audio_class · guard_resolution · no_unchecked_stdout · **runner_contract** · selection_gate_wired · vendor_sources |
| 2 | *identical to run 1 — 7 of 7* |
| 3 | the same **minus** `runner_contract` (I fixed it) and `gate_audio_class` (another round fixed it) |

The brief notes two historical runs 45 minutes apart with **zero overlap** in their red sets.
Runs 1 and 2 here overlap **7 of 7**, and run 3 differs only by two suites that were
genuinely repaired in between. A stable red set is what makes a red actionable: it is now
evidence about the code rather than noise from the runner.

**None of the five surviving reds is this round's.** `runner_contract` was mine and is fixed;
the rest are other rounds' live work and reproduce identically across runs.

**The wall clock fell 1,719 → 1,189 → 820 s** as the machine drained — the same 204 suites.
That spread is the load, and it is why a count without its concurrency context is not a
count.

---

## WHAT I GOT WRONG

**I introduced the shared-mutable-state bug while fixing a concurrency bug.** My first
partial-results file used one fixed name in the shared temp directory. With nine rounds in
flight a second `run_all.py` started, deleted it at its own startup, and a run that had
recorded **178** results reported **45**. A partial-results file that lies is worse than
none — and it is the same shape as the `bl932_probe_` collision that reddens concurrent runs
in this very tree. The path is now per-pid.

I also first wrote the partial file into `tests/`, which plants an untracked file in the one
directory this project has guards watching. And my own probe hung with its output buffered
and lost — the exact defect I was there to fix, reproduced on my own harness.

---

## STILL BROKEN, AND WHOSE

| what | whose |
|---|---|
| **`test_claims_manifest.py` takes 506 s** — a quarter of the parallel wall clock in one file | unowned; the obvious next shard |
| 5 suites over 200 s each (`test_secret_scanner` 275, `test_scratch_gc` 252, `test_content_crop` 243, `test_band` 232, `test_lock_and_snapshot` 228) | unowned |
| **`jobs=1` is still the default**, and at 112 minutes it will look like a hang to the next person | unowned — I did not change the default this round |
| The 7 reds in run 1 are other rounds' live work, not this fix | named per run below |

---

## VERIFICATION

| | |
|---|---|
| **Campaigns** | unchanged — `test_governance_rules.py` **25/25** |
| **Config** | valid — 162 keys |
| **Spend** | **$0.00** — no paid calls |
