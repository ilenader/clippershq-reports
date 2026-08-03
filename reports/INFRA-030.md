# INFRA-030 — runs.json was losing **12 records in 13**. It is now a locked read-modify-write, and the audit found one more file with exactly the same shape: **`clip_seen.json`**.

**Date:** 2026-08-03 · **Type:** concurrency fix · **Spend:** **$0.00**, no paid call
**Wrote:** `clippershq/decision_log.py`, `tests/test_decision_log_lock.py` (`6852614`),
`scratch/infra030_*`. **Read but never wrote:** `clippershq/main.py`, `spend_ledger.py`,
`song_library.py`, `clip_runner.py`, `dashboard/server.py`, `tools/claim.py`.

---

## The shape: atomic writes that still lose records

Every individual write to `runs.json` was **already atomic** — tmp + `os.replace`, no reader
ever saw a torn file — and the records vanished anyway. `os.replace` makes one write
indivisible. It cannot make a *pair* of them ordered:

```
A: runs = read()                 B: runs = read()      <- the same contents
A: runs.insert(0, mine)          B: runs.insert(0, mine)
A: replace()  -> file has A      B: replace()  -> file has B.   A IS GONE
```

**The merge semantics were already correct.** Drop any record carrying my `run_id`, insert
mine at the front, keep the rest — that is merge-append, not last-writer-wins. They were
simply being applied to a snapshot another process had already superseded. Holding the lock
across the **read** and the **replace** is the entire fix; not one line of the merge changed.

That is the same shape and the same fix as the clip library, where 236 clips once collided at
equal rev and merge-on-append *inside the lock* resolved it.

---

## The proof, with a control that fails

### 13 real processes, started on one wall-clock tick

| variant | survived | lost |
|---|---:|---:|
| **unlocked** (the code as it shipped) | **1 of 13** | **12** |
| **locked** (this round) | **13 of 13** | **0** |

Processes, not threads: the GIL serialises bytecode, so a threaded version understates the
race it is meant to measure. Every worker busy-waits to a shared start instant so the read
windows genuinely overlap rather than being spread by process startup.

### And the deterministic version, because a race is a bad test

A threaded race sometimes passes by ordering luck, **which is exactly why this went unnoticed
for so long**. So the same failure is also modelled with no timing at all — a snapshot taken
before another writer and applied after it:

```
CONTROL (old shape): run_ids in runs.json = ['A', 'seed']   LOST: ['B']
FIXED  (real write): run_ids in runs.json = ['A', 'B', 'seed']   LOST: nothing
```

**`tests/test_decision_log_lock.py` keeps the old code as a literal copy and asserts it still
loses a record.** If that control ever goes green, the scenario has stopped being able to
detect the bug and the fix's green means nothing. 8 tests, all passing.

### A second door the lock does not close

The unlocked control also threw:

```
PermissionError: [WinError 5] Access is denied: 'runs.json.tmp.r04' -> 'runs.json'
```

**The lock stops writers, not readers.** The dashboard reads this file and correctly does not
take the lock — a reader should not have to. On Windows `os.replace` fails while another
process holds the destination open, so a dashboard poll landing on the same millisecond as a
write would kill the record: `write`'s handler catches it, prints, returns `None`. That is the
same silent loss arriving through the other door. The swap now goes through
`atomic_io.replace`, which retries it (~1.2s; BL-927 measured this exposure at up to 85% of
`master_leads.csv` finalises).

---

## The contracts that had to survive the fix

| contract | why it was at risk | result |
|---|---|---|
| a logging failure **never** raises into the caller | a lock is a **new** way to fail | tested — a planted lock failure returns `None`, the run is unaffected |
| **INFRA-025**: a torn read refuses rather than rewriting | this round rewrote the same function | tested — a corrupt `runs.json` is left **untouched**, not overwritten from an empty list |
| the lock is on the **data** path, not the lock path | BL-817: `file_lock` appends `.lock` itself | tested — `runs.json.lock` exists, `runs.json.lock.lock` does not |
| cap at `KEEP_RUNS` | | tested |

**The timeout is 10s, not filelock's 120s default.** This lock protects a dashboard
convenience file, and the standing contract one line above it is that logging never takes down
a run. A render batch is ~40s per clip; blocking it for two minutes to record a log line would
be the tail wagging the run. Thirteen writers each holding this for the milliseconds a
25-record merge takes will never approach 10s, so a timeout means something is genuinely wrong
— and losing **one log record** is then the right outcome. Losing the render is not.

If `filelock` cannot be imported at all, the write **degrades to the old unlocked behaviour
and says so out loud**. Refusing to write would turn a missing helper into total loss of the
operator's only window on why a run dropped clips. A silent degradation to the exact bug this
round fixed is how the bug comes back.

---

## The shared-JSON audit — and how it over-reported first

| file | protection | verdict |
|---|---|---|
| `dashboard/static/runs.json` | `file_lock` + `atomic_io.replace` | **FIXED THIS ROUND** (was neither) |
| `spend.json` | `filelock.file_lock` in `main.record_spend` | **locked** |
| `.claims/<ROUND>.json` | one file **per round** + retried `os.replace` | **no shared RMW — a lock is unnecessary** |
| `dashboard/config.json` | **version check** (compare-and-swap) + validate-then-replace | **deliberate alternative** (INFRA-012) |
| `clip_library/` | `file_lock` + merge-on-append | locked |
| `output/master_leads.csv` | `file_lock` + merge-on-save | locked |
| `scratch/songs.json` | tmp + `os.replace`, **no lock** | **unlocked RMW — real, low exposure** |
| **`clip_seen.json`** | tmp + `os.replace`, **no lock** | **THE runs.json SHAPE, UNFIXED** |

**The AST scan I wrote first reported 5 unlocked, and 3 of those were false positives.** It
asked whether a *module* mentions a lock; the property is whether a *file's* read-modify-write
is serialised, and **a file can be written by one module and locked by its caller**. It flagged
`spend_ledger.py`, which delegates and does not write `spend.json` at all — `main.py:530` does,
under `file_lock`. It flagged `tools/claim.py`, where each round owns its own path so there is
no read-modify-write to serialise. It flagged `dashboard/server.py`, which uses a documented
version check instead. Every row above is hand-verified against the code.

### The one that matters: `clip_seen.json`

`clip_runner.save_seen()` (lines 213–219) writes a **set** that concurrent clip runs read, add
to, and write back — with tmp + `os.replace` and no lock. **That is precisely the runs.json
shape**, in a file whose whole purpose is remembering what has already been walked. Two
overlapping runs lose one run's seen-ids, and the symptom would be re-walking clips that were
already seen — costly rather than merely invisible.

**Not fixed here, and the reason is scope rather than availability.** This brief's item 3 asks
me to *check and report* the other shared JSON files, not to change them; item 1 is `runs.json`.
`clippershq/clip_runner.py` was ` M` when I found this and is **clean and unheld as I publish**
— re-checked, because a "held by another round" caveat that was true an hour ago is exactly the
kind of stale claim this project keeps paying for. So it is available to whoever takes it, and
the fix is the four lines this round just wrote for `decision_log`: wrap the read-modify-write
in `file_lock(path)` and swap through `atomic_io.replace`. **Handoff, unowned.**

`scratch/songs.json` is the same shape with far lower exposure — the operator hand-edits it and
there is no concurrent writer today, but nothing enforces that.

---

## The dashboard still reads it, and a torn read says so

Three states, exercised against the live endpoint (`api_decisions`):

```
1. MISSING -> runs=0  "no pipeline run has written a decision log yet — start one from
                       the Run tab with funnel clip_render"
2. GOOD    -> runs=1  unavailable=''   stage: in=100 out=60 dropped=40 unaccounted=0
3. TORN    -> runs=0  "decision log unreadable: JSONDecodeError"
```

**A torn read is never an empty panel that looks like a quiet day.** "Nobody has run one yet"
and "the file is broken" are different messages, and only one of them is a reason to go and
look at something.

---

## Verification

| check | result |
|---|---|
| 13 concurrent processes, unlocked | **1 of 13 survived** — the harness detects the bug |
| 13 concurrent processes, locked | **13 of 13 survived, 0 lost** |
| deterministic stale-snapshot control | old shape **loses B**; fixed shape loses nothing |
| tests | **8 of 8**, including the control that must keep failing |
| never-raise contract | planted lock failure → `None`, run unaffected |
| INFRA-025 torn-read refusal | corrupt file left **untouched** |
| lock path | `runs.json.lock` yes, `runs.json.lock.lock` no (BL-817) |
| dashboard | missing / good / torn all distinct |
| shared-JSON audit | 8 files, hand-verified; **1 unfixed match** (`clip_seen.json`) |
| campaigns | **5, unchanged** — ZHUS 216, PANICBABY 1811, STRAENGE 113, DAYLIGHT 95, ANIME15K 5 |
| config | parses, 161 keys, `spend_cap_usd` 50.0 |
| suite | **176 of 180 green** (2773s — 17 rounds in flight, 40+ python processes) |
| the four red | **none are mine**, and two are real — see below |
| paid calls | **none** |

### The four reds, attributed

| suite | standalone | fails on | owner |
|---|---|---|---|
| `test_dashboard_panels` | **OK** | — | transient |
| `test_clip_pipeline` | **OK** | — | transient |
| `test_no_unchecked_stdout` | **FAILS** | `clippershq/editor_brief.py:491` | **BL-1025**, file is ` M` mid-edit |
| `test_silent_zero_shape` | **FAILS** | `dashboard/server.py:1874 api_audit()` — `except OSError` makes `names = []`, so "could not look" resolves to "nothing there" | **unheld and clean — genuinely open** |

**I checked these against my own change first, not last.** I added a `print()` to `_runs_lock`
and a fallback `except Exception: _atomic_replace = os.replace`, which are exactly the shapes
those two guards exist to catch — an unchecked stdout read and a silent degradation. Both
scanners walk the whole tree, and **neither names `decision_log.py`**. The `print` is a *loud*
degradation, which `test_silent_zero_shape` explicitly permits
(`test_a_loud_degradation_stays_legal`), and that is why it is there rather than a bare
fallback.

The `api_audit` one is worth someone's time: it is the same class as INFRA-025's `load_spend`
bug named in this brief — a read failure resolving to the same value as a true empty answer.

## Limits and what I got wrong

- **My first "fixed" scenario passed on unfixed code.** It called `write()` twice
  sequentially, and `write()` re-reads on every call — so no stale snapshot ever existed and
  the test proved nothing. It only became a real demonstration once the snapshot was forced to
  survive across another writer, and once 13 real processes were involved. **A green result
  from a scenario that cannot fail is worth less than no result**, because it gets quoted.
- **My AST audit over-reported 3 of 5.** Corrected by hand against the code. The lesson is the
  narrower one: a module-level scan cannot answer a file-level question.
- **`clip_seen.json` is left broken**, deliberately — its writer is mid-edit by another round.
  The fix is four lines and is now written down twice.
- **The 13-process figure is one machine, one run.** "1 of 13 survived" is not a rate; it is a
  demonstration that loss is the normal outcome rather than an unlucky one. The control's job
  is to show the harness can see the bug at all, and it does.
- **I did not test lock contention under a real render batch** — the workers here write a
  minimal record. A 25-record merge is milliseconds, so the 10s timeout has orders of magnitude
  of headroom, but that is arithmetic rather than measurement.
