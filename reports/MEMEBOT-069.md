# MEMEBOT-069 — the rehearsal runs now, and the hook's arguments are executed rather than read

**Brief:** promote `scratch/mb065_clone.py` into `tests/` so the suite runs it; close the
argv-contract gap `test_governance_rules.py` leaves; keep the legal-case and attribution
properties; keep the known-broken commit as a regression fixture; record *refusal is not
evidence* in `docs/TESTING.md`.

**Headline:** the only detector for the third failure mode now runs on every suite run, for
**86 s**, and the gap that let a hook pass a flag its tool did not have is closed by a test
that **runs the invocation** — parsed out of the hook file, executed against HEAD's
committed tools, in **6 s**.

**Cost: $0.00.** No paid calls. git, argparse, and temp directories.

---

## Preconditions

```
tools/claims_read.py --holders tests/test_governance_rules.py   -> FREE
tools/claims_read.py --holders tests/test_clone_rehearsal.py    -> FREE
tools/claims_read.py --holders scratch/mb065_clone.py           -> FREE
tools/claims_read.py --holders docs/TESTING.md                  -> FREE
tools/claims_read.py --holders docs/ENFORCEMENT.md              -> FREE
git status --porcelain   -> 9 other rounds in flight, none touching these paths
```

Claimed `MEMEBOT-069` with repeated `--write` flags. `MEMEBOT-066`, `-067` and `-068` were
already held by live rounds. `docs/ENFORCEMENT.md` was added to the claim mid-round when it
turned out to need re-pointing; the claim was re-registered rather than the file written
unclaimed.

**A note on the tree.** `git status --porcelain` showed ten modified files belonging to
other rounds. That is irrelevant to every measurement here *by construction*: the rehearsal
clones HEAD, and the argv fixture is built with `git archive HEAD`. Neither can see a
working tree — which is the entire point, because the historical break was a working tree
holding the fixed file while HEAD did not.

---

## 1. The rehearsal is in `tests/`, and the suite runs it

`tests/test_clone_rehearsal.py` — 9 tests, **25 assertions**, one shared clone.

```
Ran 9 tests in 86.526s
OK
```

The engine moved; `scratch/mb065_clone.py` stays as a thin CLI over it, because
MEMEBOT-065's published report names `python scratch/mb065_clone.py --at 2f3c4e6` as its
verification block. A published verification command that stops working is a small version
of the same disease.

**Why 86 s and not more.** Promoting the file as written would have cost **160 s**. Two
defects in my own previous round's harness accounted for the difference, and both were
found by measuring rather than reading:

| | before | after |
|---|---|---|
| pre-push fixture (STATE 7) | `git init --bare` + `git push` → transfers all 238 commits: **74 s**, more than every other state combined | `git clone --bare` the throwaway clone (hardlinks, both temp): **0.5 s** |
| second rehearsal on one clone | `shutil.rmtree(..., ignore_errors=True)` races open git handles on Windows, leaves a partial dir, next `git clone` refuses → **"pre-push fixture could not be built"**, a failure about the fixture, not the hook | fresh remote directory per invocation; states 3–7 re-run cleanly |

**Transport, measured three ways.** MEMEBOT-065 used `--no-hardlinks` on a path-transport
clone, correctly refusing to hardlink into a repository nine rounds are writing to. There
was a third option:

| transport | time | size | safe? |
|---|---|---|---|
| path, hardlinked | ~9 s | 2635 MB | **no** — shares the object store with a live repo |
| path, `--no-hardlinks` | 49–145 s | 2635 MB | yes, copies every byte |
| **`file://` (pack protocol)** | **~57 s** | **434 MB** | yes — and it is what a real remote clone does |

`file://` is simultaneously the safest, the smallest and the most faithful. The clone is
sparse-checked-out to `tools/ docs/ tests/`, which is what keeps it at 434 MB.

**The blind spot that opens, and its guard.** A sparse checkout could hide a file a hook
depends on, and the hook would then fail for a reason the rehearsal misreads. So STATE 0
now parses every `tools/*.py` the clone's own hook files invoke and asserts each is present
in the checkout. Read from the hooks, never a hardcoded list — a guard that hardcodes what
it checks cannot detect drift (MEMEBOT-027).

---

## 2. The argv gap: assert the invocation, not the string

Everything `TheHookActuallyCallsTheCheck` asserted is a string match — that `pre-commit`
contains `claim.py" staged`, that it reads `$?` off the command rather than a pipeline,
that the non-zero branch exits 1. All correct. All green throughout the ~12 hours and 57
commits in which `pre-commit` passed `--enrolling` to a `verify_claims.py` that had no such
flag. **A string match cannot see an argparse contract.**

`TheToolsActuallyACCEPTWhatTheHookPasses` parses each invocation **out of** the hooks and
runs it:

```
pre-commit           tools/verify_claims.py       ['--enrolling']
pre-commit           tools/claim.py               ['staged']
pre-push             tools/repo_guard.py          ['pre-push-hook']
prepare-commit-msg   tools/guard_amend.py         ['--check']
```

Against **HEAD's committed tools** — `git archive HEAD tools docs` into a throwaway repo,
about a second. Never the working tree.

**What counts as passing is deliberately narrow.** Not exit 0: these tools are *supposed*
to exit 1 when they refuse. The contract is that argparse accepts the argument vector. So
the assertions are: not (exit 2 with `usage:` and `error:`), no traceback, and exit in
`(0, 1)` — because a callee that exits anything else reaches the user as a refusal for a
reason the hook then misattributes.

**Three ways this test could be hollow, each closed:**

- *the regex matches nothing* → `test_the_hooks_invoke_something_at_all` requires ≥4
  invocations and names the four expected scripts. A regex that matches nothing is a test
  that checks nothing.
- *it passes because the tools are fine and always would be* →
  `test_the_argv_check_can_detect_the_difference` drops in `2f3c4e6:tools/verify_claims.py`
  and requires the exact invocation to be **rejected with exit 2**.
- *it reads the working tree* → the fixture is built from `git archive HEAD`.

It costs ~6 s and holds even if someone sets the skip variable on the slow rehearsal.

---

## 3. The two properties, intact

**The legal case is committed and accepted.** STATE 3 commits an ordinary file; STATE 7
performs an ordinary push; STATE 6 exercises the documented `GUARD_AMEND_OK=1` override.
`test_the_legal_case_is_accepted` asserts all three. Without them, a hook that refuses
universally passes a suite that only ever plants violations — which is exactly what
happened.

**Every refusal names the check that made it,** from a marker the check itself emits, never
the hook's epilogue, which prints for any non-zero exit:

| state | marker | emitted by |
|---|---|---|
| 4 | `STAGED PATHS SPAN 2 LIVE ROUNDS` | `claim.py staged` |
| 5 | `THIS COMMIT WOULD NEWLY ENROL 1 manifest(s)` | `verify_claims.py --enrolling` |
| 6 | `THE INDEX CONTAINS FILES THAT ARE NOT IN THE COMMIT YOU ARE AMENDING` | `guard_amend.py` |
| 7 | `BLOCKED by repo_guard pre-push: HEAD is 7 commits BEHIND` | `repo_guard.py` |

Plus a crash detector in every state: an argparse usage line or a traceback scores as
**failure**, not refusal. And isolation is by **fixture**, never by stubbing — STATE 4
plants a cross-round commit with no staged manifest; STATE 5 plants an unready manifest
with no live claims at all. Both tools run unmodified in every state.

---

## 4. It can still fail — same 11, no second clone

The regression fixture injects `2f3c4e6:tools/verify_claims.py` — the last committed copy
without the flag, verified to contain no occurrence of `enrolling` before it is used — into
the HEAD clone and re-runs the states. It reproduces **the same 11 failures** MEMEBOT-065
measured against the whole historical tree, for **6.8 s** instead of a second 57-second
clone. `python scratch/mb065_clone.py --at 2f3c4e6` still rehearses the whole tree when the
original comparison is wanted.

And here is the finding, now pinned as an assertion that is **expected to pass on a broken
tree**:

```
  cross-round commit REFUSED                               PASS  exit 1
  unready-manifest commit REFUSED                          PASS  exit 1
  amend absorbing a foreign file REFUSED                   PASS  exit 1
  HEAD unmoved by the refused amend                        PASS
  ---
  refused BY claim.py staged                               *** FAIL ***
  refused BY verify_claims.py --enrolling                  *** FAIL ***
  refused BY guard_amend.py (index-vs-HEAD)                *** FAIL ***
  a normal commit is ACCEPTED with hooks installed         *** FAIL ***  exit 1
  no tool crashed during a normal commit                   *** FAIL ***  argparse usage error
```

`test_refusal_alone_still_looks_like_success` asserts the top block **passes** and the
attribution block **fails**. If someone ever "fixes" the harness so the top block goes red
on a broken tree, that test fails and tells them why: refusal was never the signal.

---

## 5. `docs/TESTING.md` rule 10 — refusal is not evidence

> A guard that refuses everything, and a guard that refuses because it crashed, are both
> indistinguishable from one that works — unless the test also proves the legal case passes
> and names which check did the refusing.

Rule 1 says a fixture must prove it can detect the difference; rule 10 is its companion for
**guards**, where the fixture works, the assertion is true, and the conclusion is still
wrong because `exit != 0` was read as "the rule fired". It carries the four requirements
(legal case, attribution, crash-as-failure, isolate by fixture), the argv-contract pattern
with its code shape, and the generalisation:

> A caller is the one dependency with no import to break and no test to go red. Hooks,
> `subprocess` calls, shell wrappers, cron entries, `Makefile` recipes: for each of them,
> the only assertion that means anything is the one that runs the command.

`docs/ENFORCEMENT.md` is re-pointed from `scratch/` to `tests/`, with three rows added to
its Part 1 index.

---

## What I got wrong

**The harness I shipped last round spent 74 of its 86 seconds on one avoidable thing, and
could not run twice.** I wrote STATE 7's `git init --bare` + `git push` in MEMEBOT-065,
reported the harness as complete, and never timed its states or ran it twice against one
clone. Both defects were found in the first ten minutes of measuring here. A harness is
code; "it printed PROVEN" is not the same as "it is correct", which is uncomfortably close
to the rule this round exists to write down.

**I also had the transport wrong.** `--no-hardlinks` was the right instinct — do not
hardlink into a repo other rounds are writing — but I stopped at the first safe option
rather than the best one. `file://` is safer *and* six times smaller.

---

## Off-brief

The two harness defects above were not in the brief; they were found while promoting the
file and fixed because leaving a 74-second avoidable cost in a test that now runs every
time would have made the gate a candidate for being switched off — which is how the
original hazard (`docs/ENFORCEMENT.md`, third failure mode) reproduces.

---

## What is still broken, and whose file

**The skip switch is the failure mode with a bow on it.**
`CLIPPERSHQ_SKIP_CLONE_REHEARSAL=1` turns off the only detector of "installation is
uncommitted local state", and it is itself uncommitted local state. It skips loudly (rule
6) and says so in the skip message, but a loud skip in a 124-suite run is still one line
among many. **Mine, unresolved by design** — the alternative is a test with no escape
hatch, and BL-818 measured that a gate which cannot be bypassed gets bypassed by not being
installed (1 of 40 adoption).

**`core.hooksPath` still cannot be versioned.** Unchanged by this round and unchangeable in
git. All the rehearsal can prove is that the install command works and the hooks are
correct once it is run. Nothing detects a *contributor* who never ran it.

**The rehearsal's 86 s is measured on an idle-ish machine.** Under nine concurrent rounds
the clone alone was observed at 145 s (path transport) and 52–57 s (`file://`).
`run_all.py`'s per-suite timeout is 600 s, so there is margin, but it is not unlimited
margin. **Nobody's file yet** — if it ever trips, the fix is the transport, not the states.

---

## Suites

```
ALL GREEN -- 131/131 suites passed, 4623 checks   (803.4s)
  (131 suite file(s) discovered; 10 round(s) in flight)
```

Quoted **with its discovery rule**: `run_all.py` walks nested `tests/` directories as well
as `tests/` (MEMEBOT-026), and both new/edited files were confirmed in the discovery list
before the run. 131 suites against MEMEBOT-065's 124 — this round adds one; six came from
other rounds landing in the same window, which is also why a suite count is a moment and
not a property.

**Campaigns unchanged, config valid**, both asserted rather than eyeballed:
`AFingerprintCarriesItsEncoding` reproduces `8e02f8d6f6307ae8` (default separators) and
`7a029ee5447cddd8` (compact) from the live `config.json`; `tests/test_config_contract.py`
returns `ALL OK` including its defaultless-read AST pass.

`PYTHONUTF8=1` is required; without it a cp1252 crash reads as a false RED.

**One honesty note on the total.** 803.4 s is *lower* than MEMEBOT-065's 847 s despite
seven more suites and this round's added 72–86 s. Machine load differs between runs by more
than the thing being measured, so do not read that as "the rehearsal is free." The
defensible number is the isolated one: **86.5 s** measured alone, **72.3 s** measured while
the full suite ran concurrently.

---

## Verification

```
PYTHONUTF8=1 python -m unittest tests.test_clone_rehearsal      # 9 tests, 86.5s, OK
PYTHONUTF8=1 python -m unittest tests.test_governance_rules     # 25 tests, ~6s, OK
PYTHONUTF8=1 python scratch/mb065_clone.py                      # PROVEN 25/25
PYTHONUTF8=1 python scratch/mb065_clone.py --at 2f3c4e6         # NOT PROVEN
python tools/verify_claims.py docs/claims/MEMEBOT-069.claims
cat scratch/mb069_timing.txt                                    # the cost breakdown
```
