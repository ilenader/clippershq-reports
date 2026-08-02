# MEMEBOT-065 — the hook was broken at HEAD, it is not any more, and the harness that missed it can now fail

**Brief:** fix the pre-commit hook, which is broken at HEAD. Commit BL-921's
`verify_claims.py` if it is coherent; prove the hooks from a clean clone; assert **which**
check fired; record the third failure mode in `docs/ENFORCEMENT.md`.

**Headline: the break was already closed before this round started — by `eff154b`, 19
minutes after MEMEBOT-063 published the finding.** That does not make the round moot. The
break lasted **~12 hours and 57 commits** in the versioned hook, invisible to every test in
the repository, and the reason it was invisible is still true: *nothing asserted that a
normal commit succeeds*. That assertion now exists, and the harness that reported PROVEN
through the break now reports **NOT PROVEN, 11 of 24** when pointed at the broken tree.

**Cost: $0.00.** No paid calls. Everything here is git, argparse and a temp directory.

---

## Preconditions

```
tools/claims_read.py --holders docs/ENFORCEMENT.md          -> FREE
tools/claims_read.py --holders tools/verify_claims.py       -> FREE
tools/claims_read.py --holders tools/githooks/pre-commit    -> FREE
tools/claims_read.py --holders tests/test_governance_rules.py -> FREE
git status --porcelain                                      -> clean for every path above
```

Claimed `MEMEBOT-065` with repeated `--write` flags (`claim.py` registers `a,b,c` as one
path otherwise — MEMEBOT-016's hollow "no conflicts"). Seven other rounds in flight, no
path conflicts. **`MEMEBOT-064` was already held** by a live caption-trim round, so this
one is 065.

---

## 1. BL-921's `verify_claims.py` — coherent, and already committed

The brief said the file was still unstaged. It is not: `git status --porcelain` shows
`tools/verify_claims.py` clean, and `git diff HEAD` for it is empty.

```
$ git log --oneline -S"--enrolling" -- tools/verify_claims.py
eff154b Rescue orphaned tooling + governance work (BL-797, BL-807, BL-865, BL-874,
        BL-881, BL-892, BL-921, BL-925, BL-932, BL-941, MEMEBOT-022/032/033/056)
```

So the answer to "commit it if it is coherent" is: **it is coherent, and it landed at
`eff154b`, attributed to BL-921 in the commit message alongside fourteen other rescued
rounds.** Re-committing it would have been a no-op that rewrote a correct attribution.
Verified rather than assumed:

| check | result |
|---|---|
| flag parses at HEAD | `git show HEAD:tools/verify_claims.py` → `--help` lists `--enrolling` with its BL-892 rationale |
| flag is functional at HEAD | STATE 5 of the rehearsal refuses a planted unready manifest **using the HEAD copy, unmodified** |
| BL-921's own manifest | `verify_claims.py docs/claims/BL-921.claims` → **9/9 verified at HEAD** |
| working tree vs HEAD | `git diff --stat HEAD -- tools/verify_claims.py` → empty |

**The one thing worth flagging about `eff154b`:** it is a fifteen-round bundle, exactly the
shape `claim.py staged` exists to refuse. It was the right call for a rescue — orphaned
work degrades, and this file's twelve hours as an orphan *became* the HEAD break — but the
per-round intermediate states inside it are not reconstructible, which is the cost
`docs/CORRECTIONS.md` already prices.

---

## 2. The break, measured

`tools/githooks/pre-commit` calls `python "$ROOT/tools/verify_claims.py" --enrolling`. The
versioned hook has done so since it was first committed. `verify_claims.py` did not carry
the flag until `eff154b`.

| | |
|---|---|
| window opens | `64c0fc4` 2026-08-01 22:45 — versioned `pre-commit` committed, already calling `--enrolling` |
| flag absent | `git show 64c0fc4:tools/verify_claims.py \| grep -c enrolling` → **0** |
| window closes | `eff154b` 2026-08-02 10:43 |
| duration | **~12 hours, 57 commits** |
| escalation | `2210eb9` (10:10) unified both installers on `core.hooksPath` — from then on, *installing* the hooks was what armed the break |

What a clean clone got, for those twelve hours, on **every** commit:

```
usage: verify_claims.py [-h] paths [paths ...]
verify_claims.py: error: the following arguments are required: paths

  pre-commit REFUSED: a manifest above would be enrolled into permanent
  enforcement before the code it claims is committed.
```

Note the second half. The tool died on argparse; the hook printed a **specific, plausible,
entirely wrong** explanation, because a hook's epilogue fires on any non-zero exit. A round
that hit this would have gone looking for a manifest it had not staged.

**Why no test caught it.** `tests/test_governance_rules.py` asserts the wiring *as text*:
that the hook contains `claim.py" staged`, that it reads `$?` off the command rather than a
pipeline, that the non-zero branch exits 1. All correct, all passing, all blind — a string
match cannot see an argparse contract. **A hook is the one caller with no import to break
and no test to go red:** it is a shell file, it invokes a tool by path, and its failure mode
is a refusal, which is also what it prints when it is working.

---

## 3. The rehearsal — `scratch/mb065_clone.py`, 24 assertions, nothing stubbed

Clones HEAD into a temp directory (local path, no network), then:

```
STATE 0  core.hooksPath : (unset)    all three hooks versioned, none in .git/hooks
STATE 1  CONTROL, before install     cross-round + unready manifest -> commit ACCEPTED
STATE 2  repo_guard.py --install-hooks           -> core.hooksPath = tools/githooks
STATE 3  A NORMAL COMMIT                         -> ACCEPTED
STATE 4  cross-round commit          REFUSED by  claim.py staged
STATE 5  unready manifest            REFUSED by  verify_claims --enrolling
STATE 6  cross-round amend           REFUSED by  guard_amend.py (prepare-commit-msg)
         same amend, GUARD_AMEND_OK=1                -> ACCEPTED
STATE 7  push 7 behind upstream      REFUSED by  repo_guard pre-push
         ordinary push                               -> ACCEPTED
```

**Result at HEAD: 24 PASS, 0 FAIL, verdict PROVEN.** All three hooks are inert in a fresh
clone; `python tools/repo_guard.py --install-hooks` alone is sufficient to arm all three;
normal commits and normal pushes succeed afterwards.

### Which check fired — attributed from the check's own output

The brief's item 3 is the load-bearing one. Every refusal is matched against a marker
emitted by the **check itself**, never the hook's generic banner:

| state | marker asserted | emitted by |
|---|---|---|
| 4 | `STAGED PATHS SPAN 2 LIVE ROUNDS` | `tools/claim.py staged` |
| 5 | `THIS COMMIT WOULD NEWLY ENROL 1 manifest(s)` / `[NOT READY]` | `verify_claims.py --enrolling` |
| 6 | `THE INDEX CONTAINS FILES THAT ARE NOT IN THE COMMIT YOU ARE AMENDING` | `guard_amend.py` |
| 7 | `BLOCKED by repo_guard pre-push: HEAD is 7 commits BEHIND` | `repo_guard.py pre-push-hook` |

Plus, in every state, a **crash detector**: an `argparse` usage line or a `Traceback` in the
output scores as a **failure**, not as proof. And the negative assertions matter as much as
the positive ones — STATE 4 asserts the enrolling check *ran and did not object*; STATE 5
asserts the cross-round check *did not fire*.

### Isolation by construction, not by deletion

MEMEBOT-063's `mb059_clone.py` isolated `claim.py staged` by **overwriting
`verify_claims.py` with `sys.exit(0)`**. That is a genuine isolation and it also destroys
the evidence: the run that prints PROVEN is the run in which the broken tool is no longer
present. This harness isolates by *arranging the fixture* instead —

- STATE 4 plants a cross-round commit with **no staged manifest**, so the enrolling check
  has nothing to object to.
- STATE 5 plants an unready manifest with **no live claims at all**, so `claim.py staged`
  cannot be the refuser.

Both tools run unmodified, from the clone, in every state.

### The harness can fail — proven, not asserted

A harness that has never gone red on a tree known to be broken is an untested test.
`mb065_clone.py --at <ref>` rehearses an older tree. Pointed at `2f3c4e6`, the last commit
before the repair:

```
=== VERDICT ===
  *** NOT PROVEN — 11 assertion(s) failed ***
      - a normal commit is ACCEPTED with hooks installed
      - no tool crashed during a normal commit
      - the enrolling check RAN and passed
      - refused BY claim.py staged
      - the enrolling check ran and did NOT object
      - nothing crashed (the refusal is a decision, not a death)
      - refused BY verify_claims.py --enrolling
      - nothing crashed
      - refused BY guard_amend.py (index-vs-HEAD)
      - nothing crashed
      - GUARD_AMEND_OK=1 lets the amend through
```

Read what stayed green there. `cross-round commit REFUSED` — **PASS**.
`unready-manifest commit REFUSED` — **PASS**. `amend absorbing a foreign file REFUSED` —
**PASS**. On a tree where the hook rejected literally every commit, three of four
"the guard works" assertions still passed. **That is the whole finding**: refusal is not
evidence. Only attribution is.

The last failure is worth its own line: `GUARD_AMEND_OK=1 lets the amend through` fails on
the broken tree because an amend still runs pre-commit, and the documented escape hatch for
one guard cannot get you past a different guard that is crashing. The override *looked*
broken; it was fine.

---

## 4. `docs/ENFORCEMENT.md` — the third failure mode, corrected

The section existed (MEMEBOT-059 wrote it) and **both of its "live instances" had gone
stale within hours of being written** — a small instance of the same disease.

- Instance 1 said *"the pre-commit hook is broken at HEAD ... BL-921's is in flight"*.
  Now recorded as **CLOSED**, with the window, the duration, the commit count, the closing
  commit, and the generalisation about hooks having no import to break.
- Instance 2 said the harness *"neutralises the other check to isolate it"*. That is now
  named as a third defect (the isolation gap) alongside the attribution gap it did fix and
  the **coverage gap** — no state ever committed anything legal — which is the single
  assertion that would have caught instance 1 the moment it landed.
- A third stale claim, elsewhere in the file: *"running repo_guard's installer today writes
  hooks git will never execute."* Fixed at `4a60cc5`; now marked CLOSED **and confirmed by
  rehearsal**, which is stronger than reading the source.

Two rows added to Part 1 (the amend guard; the rehearsal rule itself) and two to Part 2's
refusal index — including the one that is *not* a refusal:

> **a commit refused with no check named above it** → Not a refusal, a **crash**. An
> `argparse` usage line or a traceback above the hook's banner means the tool died and the
> hook reported it as a violation.

That row is the docs half of the harness's crash detector. A round that hits this again
gets an answer in one search instead of hunting a manifest it never staged.

---

## What is NOT fixed

**The text-level wiring assertions are still text-level.** `test_governance_rules.py` proves
the hook *names* the tools; nothing proves the tools *accept the arguments the hook passes*.
The rehearsal covers it now, but the rehearsal is a `scratch/` script that nothing runs
automatically — which is, precisely, the third failure mode wearing a different hat. The
honest status is: **detectable now, not yet enforced.** Wiring an argv-contract assertion
into `tests/test_governance_rules.py` is a small, well-defined next step; it is a test file
this round does not need to touch to deliver its brief, and it belongs to whoever takes it.

**`core.hooksPath` still cannot be versioned.** Nothing in this round changes that. A fresh
clone still runs no hooks until someone types the install command. All this round can prove
is that the command works and that the hooks are correct once it has been run.

---

## Suites

```
ALL GREEN -- 124/124 suites passed, 4456 checks   (847.1s)
  (124 suite file(s) discovered; 11 round(s) in flight)
```

The count is quoted **with its discovery rule** — `run_all.py` walks `tests/` recursively
(MEMEBOT-026 found it was searching one level and hiding 637 test functions), and a suite
count is a moment under eleven concurrent rounds, not a property.

That run began before the `docs/ENFORCEMENT.md` edits landed, so the doc-sensitive suites
were re-run afterwards: `test_governance_rules` 22 OK, `test_claims_manifest` 24 OK,
`test_suites_parse` 6 OK, `test_verify_claims` 6 OK, `test_tools_tracked` 7 OK.

`PYTHONUTF8=1` is required; without it a cp1252 crash reads as a false RED.

---

## Verification

```
python tools/verify_claims.py docs/claims/BL-921.claims        # 9/9 at HEAD
python tools/verify_claims.py docs/claims/MEMEBOT-065.claims   # this round
PYTHONUTF8=1 python scratch/mb065_clone.py                     # 24/24, exit 0
PYTHONUTF8=1 python scratch/mb065_clone.py --at 2f3c4e6        # 11 failures, exit 1
```
