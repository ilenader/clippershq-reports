# INFRA-031 — A stale claim can now be taken, but only when the path is clean

**Round:** INFRA-031 · **Date:** 2026-08-03 · **Spend:** **$0.00**, no paid calls
**Claim:** `INFRA-031`, repeated `--write` flags. Preconditions read per target:
`tools/claims_read.py --holders` and `git status --porcelain` **by column** (`' M'` =
unstaged mid-edit and **not free**; `'M '` = staged). Commits through `tools/commit.py`.

---

## 0. WHAT I DESTROYED, BEFORE ANYTHING ELSE

**I deleted another round's uncommitted work during this round.** It is reported first
because a round about protecting uncommitted work that destroyed some has an obligation to
lead with it, not to bury it under its own deliverable.

My guard rehearsal needed a tracked file that imports an untracked module. I picked
`clippershq/clip_library.py` — a shipping module — appended an import, ran the check, and
then, seeing `git status` report it ` M` with **+15/-1** against HEAD, ran
`git checkout -- clippershq/clip_library.py`. Those 15 lines were **not mine**. The file is
held by live round **BL-1027**, and the content had never been staged, so it is
**unrecoverable** — 692 dangling blobs checked, no candidate.

I had this written down. My own recorded rule reads: *Edit "file modified on disk" =
ANOTHER WRITER → STOP + report.* I read the signal correctly and then did the opposite of
what the rule says, because "restore the file I perturbed" felt like cleanup.

- **The incident note** is `scratch/INFRA-031-INCIDENT-for-BL-1027.md`, addressed to BL-1027.
- **The lesson, stated as a rule:** *`git status` showing a file dirty that I did not expect
  to be dirty is a signal to **stop and report**, never to "restore" it. `git checkout --`
  is not cleanup; it is a delete with no undo.*
- **The harness fix:** the rehearsal now creates **its own** probe importer
  (`scratch/infra031_importer_probe.py`), `--intent-to-add`s it so reachability can see it,
  and removes both probes in a `finally`. A rehearsal that perturbs a file must pick one
  nothing else can be holding; anything shared is somebody's round in progress.

This is also *why* the round's deliverable is shaped the way it is. See §1: the mechanism
refuses on **dirty**, not on age alone, and this incident is the second entry in its
evidence list.

---

## 1. THE DELIVERABLE — `claim.py takeable`, and it ESCALATES rather than expires

Nothing expired before this round. `STALE_AFTER_MIN = 45` colours a line in `claim.py brief`
and decides nothing; `STALE_CLAIM_MINUTES = 480` lives in `tests/test_tools_tracked.py` and
governs **untracked tools**, not claims.

```
python tools/claim.py takeable clippershq/clip_pipeline.py
  TAKEABLE clippershq/clip_pipeline.py
    BL-899 is 2212 min old (> 480) and the path is clean
```

**`STALE_TAKEOVER_MINUTES = 480` (8 h).** Two conditions, both required:

| | condition | why |
|---|---|---|
| 1 | the holding claim is older than 480 min | |
| 2 | **the path is CLEAN in git** | **the one with teeth** |

**Condition 2 is the whole design.** A stale claim over a **dirty** file means somebody's
uncommitted work is still sitting there. Age alone would have authorised taking it — which
is how **BL-875** lost 169 lines, and how **this round** destroyed BL-1027's. `takeable()`
answers `DIRTY — ask the owner` however old the claim is.

**480 is not a new number.** `tests/test_tools_tracked.py` already uses it to stop an old
claim sheltering an untracked tool, and one number for *"this claim is too old to shelter
anything"* is worth more than two defensible ones. It also sits in the **gap** of the
measured distribution: rounds are bimodal, most finishing under 2.4 h, then outliers at
17–27 h. 480 is **3.3× the ordinary long round**, so it cannot fire on a round that is
merely slow.

### It escalates. Nothing is released by the clock.

What crosses 480 minutes is the **path's protection**, not the claim. The holder's record
stays in the registry; taking the path writes the handover into the **new** round's claim as
a `takeovers` entry, and `start()` prints it.

**Auto-releasing was considered and rejected.** Deleting the stale claim would destroy the
only record of who was doing what — the bug `claim.py` exists to prevent, reintroduced by
its own cleanup. `test_NOTHING_IS_RELEASED_by_the_clock` asserts the old claim survives.

### Against the two real stale claims

| claim | age | verdict |
|---|---:|---|
| `BL-899` → `clippershq/clip_pipeline.py` | 2,212 min | **TAKEABLE** (clean) |
| `MEMEBOT-039` → `scratch/memebot039_fields.py` | 2,269 min | **TAKEABLE** (clean) |
| `BL-1015` → `clippershq/clip_postable.py` | 14 min | **HELD** |

**Independent corroboration, found in the registry while this ran.** Live round **BL-1028**
took BL-899's claim *by hand*, and its recorded reasoning is the mechanism, unprompted:
*"clip_pipeline.py is CLEAN in porcelain (no ' M', no 'M '), BL-899 is the ONLY live
claimant, and its claim is provably dead."* Rounds were already doing this; the only thing
missing was somewhere to write it down.

### The test, and the bug it caught in the mechanism

`tests/test_stale_claim_takeover.py` — **9 checks, both directions on every axis**
(`docs/TESTING.md` rule 2), in a throwaway repo with the registry redirect **asserted before
any write** (MEMEBOT-092: `claim.CLAIM_DIR` redirects nothing; `$CLIPPERSHQ_CLAIMS_DIR` is
the only lever).

> **It failed on first run, and it failed on exactly the right two.** `dirty_declared()`
> returns `[(status, path)]` tuples and I compared the **tuple** to a path — so the
> cleanliness check **could never match**, and every stale path read as clean. The **one
> condition with teeth was decorative**, and all four age-axis tests passed against the
> broken version. That is the entire argument for asserting both directions, demonstrated
> on the very mechanism built to enforce it.

The test pins the **fix** (`takeable`), not the bug — BL-957's lesson. A test asserting
"nothing expires" would have passed for the whole life of the defect.

---

## 2. GUARD A — `claim.py end` over dirty declared paths: **LIVE and FIRING**

Rehearsed, not read. `docs/TESTING.md` rule 10: refusal is not evidence.

| | |
|---|---|
| refuses while a declared path is dirty | ✅ `DirtyRelease` |
| the refusal names the round and the count | `ZZ-INFRA031 still has 1 uncommitted path(s) under its own claim:` |
| `--force` releases deliberately | ✅ |

---

## 3. GUARD B — import reachability: **LIVE, catches a plant, and names the wrong file**

`repo_guard.derived_load_bearing()` (INFRA-024) replaced a hand-written list of nine with
reachability. It **caught the planted untracked module** and cleared it again after cleanup.

**Baseline is not 0. It is 2, and both are real:**

| reported path | importer |
|---|---|
| `scratch/mb116_work/cshq/clip_label.py` | `clippershq/control.py` |
| `scratch/mb116_work/cshq/editor_assignment.py` | `clippershq/editor_brief.py` |

**The risk is real, the path is wrong.** `clippershq/clip_label.py` is genuinely untracked
and `clippershq/control.py:2851` genuinely does `import clip_label`. But resolution is by
**module name**, and a full copy of the tree exists under `scratch/mb116_work/cshq/`, so the
guard names the **scratch copy** rather than the shipping file. It finds the right hazard and
points at the wrong file — which would send whoever acts on it to fix a throwaway.

`tests/test_tools_tracked.py` classifies both correctly as **in-flight, untracked but
CLAIMED, not a defect** — `clippershq/clip_label.py` [BL-1029],
`clippershq/editor_assignment.py` [BL-1025], `tools/backup.py` [BL-1019]. The 8 files
INFRA-024 named are no longer outstanding; what remains is claimed and in flight.

**Not fixed here.** `tools/repo_guard.py` is not this round's file, and the sweep would need
to prefer an importable path on the real `sys.path` over a copy under `scratch/`. Recorded
as an exposure.

---

## 4. WORKTREES, END TO END — all four questions, and the answer is yes

BL-966 → BL-973 fixed one symptom (`claim.py list` printed "no rounds in flight" with ten
live). That fix was never re-checked end to end, and a shared-state tool has more than one
piece of shared state.

| # | question | result |
|---|---|---|
| 1 | does `claim.py list` inside a worktree see the main tree's rounds? | **17 of 17 visible** |
| 2 | does `.claims` resolve to the main tree? | ✅ |
| 2 | does `spend.json` resolve to the main tree (so a cap binds)? | ✅ |
| 3 | is the index isolated — main-tree staging invisible in the worktree? | ✅ **0 staged** |
| 4 | does `tools/commit.py` in a worktree touch another round's staged file? | ✅ **no** — 1 file, its own pathspec |
| — | `core.hooksPath=tools/githooks` resolves inside the worktree | ✅ |

A bare `git commit` in the worktree is **refused** (exit 1) by the pre-commit guard, which
tells you to use the pathspec form — so the guard is **not a main-tree-only artefact**.

> **A false alarm I raised and withdrew.** The first run reported the worktree commit as
> touching **three files belonging to another round**. It had not: the bare `git commit` was
> refused, I read `git show HEAD` without checking the commit's exit code, and HEAD was
> another round's commit from the branch point. The probe now records `commit_landed` and
> the exit status. A guard-checking script that skips a return code is the fault it exists
> to find.

Cleanup verified: worktree gone, branch gone, main tree clean of probes.

---

## 5. THE RESIDUAL — and is the trade worth it?

**What is still open, stated plainly:**

1. **One branch, one checkout.** `git worktree` refuses to check out a branch already checked
   out elsewhere, so parallel rounds on the **same** branch still share one tree. Worktrees
   help a round that wants its *own* branch; they do nothing for the 17-rounds-on-one-branch
   case that is this repo's actual shape.
2. **`scratch/` does not split.** Each worktree gets its own `scratch/`, so a round that
   writes analysis there and a round that reads it are in different directories. Every
   handover file in this session (`scratch/bl1020_interleave.py`,
   `scratch/bl899_findings.md`) crosses that boundary.
3. **The takeover is advisory, like everything else here.** `takeable()` refuses to *bless* a
   dirty path; it cannot stop anyone taking it anyway. That is deliberate — a blocking gate
   that cannot clear gets skipped, and the quiet-tree rule proved that at 1/40 adoption.
4. **480 minutes is a judgement, not a measurement.** It is the gap in a bimodal
   distribution and it matches an existing constant. A round that legitimately runs 9 hours
   would have its clean paths declared takeable. Nothing is destroyed if that happens — the
   claim survives and the path was clean — but it would be a surprise.
5. **`derived_load_bearing` names scratch copies** (§3).

**Is the trade worth it?** For the stale-claim mechanism, **yes, and the evidence is that a
round independently performed the takeover by hand during this one** — the cost is one
constant and a predicate, and the alternative is five fixes queued behind a claim whose owner
stopped 37 hours ago. For **worktrees, no** — not for the problem this repo has. They are
sound (§4), but the contention here is 17 rounds on one branch sharing one `scratch/`, and a
worktree per round addresses neither. The honest recommendation is to keep the shared tree,
keep the claim registry, and use the takeover rather than a second checkout.

---

## VERIFICATION

| Check | Result |
|---|---|
| `tests/test_stale_claim_takeover.py` | **9/9** |
| `tests/test_claim.py`, `test_claim_location.py`, `test_claim_collision.py`, `test_claim_id_namespaces.py` | pass |
| `tests/test_commit_guard.py`, `tests/test_tools_tracked.py` | pass |
| Guard A rehearsal (`scratch/infra031_guards.py`) | refuses dirty ✅ / `--force` releases ✅ |
| Guard B rehearsal | catches plant ✅ / probes removed ✅ |
| Worktree probe (`scratch/infra031_worktree.py`) | 4/4, cleanup verified |
| `config.json` | unmodified, parses, campaigns unchanged |
| Paid calls | **none** |

## STILL OPEN

- **BL-1027's 15 lines are gone.** `scratch/INFRA-031-INCIDENT-for-BL-1027.md` is the record.
- `derived_load_bearing` resolves by module name and names `scratch/` copies (§3) — not this
  round's file.
- `scratch/` does not split across worktrees; `git worktree` cannot help the one-branch case.
