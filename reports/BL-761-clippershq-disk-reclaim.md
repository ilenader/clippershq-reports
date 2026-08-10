# BL-761 — rescue the work, then reclaim the disk

**190.97 GB reclaimed. Free space went from 47.67 GB to 238.64 GB.** Nothing was lost. Every piece of
work BL-759 flagged is now on GitHub, verified from a second checkout, before anything was deleted.

| | Before | After |
| --- | --- | --- |
| Free space on C: | **47.67 GB** | **238.64 GB** |
| Used | 882.92 GB | 691.94 GB |
| Registered worktrees | 152 | **1**, the owner's working copy |
| `clone_rehearsal_*` in `%TEMP%` | 171 | **1**, skipped for being 20 minutes old |
| Work existing only on this machine | 9 places | **0** |

Order was rescue first, delete second, and nothing was deleted that BL-759 had not already classified
SAFE. Each path was re-verified in the same breath as its own removal.

## PART 1 — THE LANDMINE: `C:\Users\Game Centar\clippershq-bl439-wt`

### What the 370 lines actually were

Re-checked at the start of this round and unchanged from BL-759: five modified files, all unstaged,
370 insertions and 3 deletions, written 2026-07-13 on top of `e096bc64` (Merge BL-435) and untouched
for four weeks.

| File | Lines added |
| --- | --- |
| `src/lib/growth/in-app.ts` | +244 |
| `src/lib/growth/triggers.ts` | +76 |
| `src/components/layout/notif-href.ts` | +34 |
| `src/lib/notifications.ts` | +15 |
| `src/lib/notification-severity.ts` | +4 |

**It is real work, not stray output.** It is exhaustive life-event coverage for the growth engine:
eleven new triggers (`VIEW_MILESTONE`, `EARNINGS_MILESTONE`, `LEVEL_UP`, `STREAK_MILESTONE`,
`FIRST_PAYOUT_REQUESTED`, `FIRST_PAYOUT_PAID`, `REFERRAL_CONVERTED`, `ACCOUNT_VERIFICATION_FAILED`,
`REPEATED_REJECTIONS`, `NEW_CAMPAIGN_LIVE`, `WIN_BACK`), two new `TriggerKind` values (`milestone`
and `reengage`), each registered with `source: "event"` so the pure `decideNextTrigger` ladder and its
14 assertions are deliberately untouched.

The load-bearing piece is `collapseGrowthBurst` in `growth/in-app.ts`: a pure function taking every
trigger that fires at the same moment and returning ONE email carrier plus all of them in-app, with
friction triggers never outranking a celebration. That is what stops a clipper who crosses four
milestones at once from receiving four emails. Around it sit the eleven types added to
`NotificationType`, bell and toast routing for every `growth_*` type in `notif-href.ts`, and amber
WARNING severity for the two friction triggers.

**No judgement is offered on whether it is good.** It was written against a four-week-old main and has
never been compiled against current main. It touches `src/lib/growth/*`, which CLAUDE.md places in the
ALWAYS-OPUS tier along with anything deciding who gets emailed. The commit message says all of this
so whoever finds the branch is warned before they rebase it.

### Preserved, and verified from a second checkout

```
branch : rescue/BL-439-uncommitted-growth-life-events
commit : 7c700f5a67f1297b4cea2fe26d5404cbc989d0df
staged : exactly the 5 files, by explicit pathspec, 370 insertions 3 deletions
```

Committed byte for byte as found, with no edit, no build and no test, because changing it would have
made it something other than what was rescued. **Not merged to main and not merged anywhere.**

Verification was done from the MAIN checkout, not from the folder being deleted, so it could not be
fooled by local state: `git rev-parse origin/rescue/BL-439-uncommitted-growth-life-events` returns
`7c700f5a`, `git show --stat` on that ref lists the five files with the right line counts, and
`git grep collapseGrowthBurst origin/rescue/...` finds it. Only then did the folder become eligible.

### The junction, and why a careless delete would have been a disaster

`C:\Users\Game Centar\clippershq-bl439-wt\node_modules` was a real NTFS **Junction**
(`LinkType = Junction`) whose target was `C:\Users\Game Centar\OneDrive\Desktop\ClippersHQ\node_modules`,
the live working copy's dependencies. Both resolved to the same 564-entry directory.

On Windows a junction is a directory that IS the target for the purposes of recursive traversal.
`rmdir /s`, `rm -rf`, `Remove-Item -Recurse` and `git worktree remove --force` all walk into it and
delete the target's contents. The folder that must not be lost was also the folder that was dangerous
to delete.

**The safe removal is `rmdir` with no `/s`**, which deletes the reparse point itself and cannot
recurse, because without `/s` it refuses any directory that is not empty and treats a junction as the
empty link it is:

```
cmd /c rmdir "C:\Users\Game Centar\clippershq-bl439-wt\node_modules"
```

Measured before and after, in one step, so the claim is not an argument:

```
BEFORE  main node_modules children : 564
        junction LinkType          : Junction
        junction Target            : C:\...\ClippersHQ\node_modules
RMDIR_EXITCODE                     : 0
AFTER   junction still exists      : False
        main node_modules exists   : True
        main node_modules children : 564
```

**Zero children lost.** Only after that did the worktree get removed. A follow-up sweep of all 151
approved paths for reparse points returned **0**, confirming this was the only junction on the
machine and that every subsequent `--force` had nothing to follow.

## PART 2 — THE EIGHT NEEDING A PUSH

Each was probed first: correct branch checked out, exactly 1 unpushed commit, 0 dirty, and the branch
**ABSENT on origin**. Absent matters, because it means the push could only ever CREATE a ref. No
force was used and no existing ref could be clobbered. Each was pushed under its own already-clear
name, with up to 3 attempts, then verified by reading the ref back off origin.

| Worktree | Branch now on origin | Commit | What it holds |
| --- | --- | --- | --- |
| `C:\r1` | `research/R-1` | `69410d3f` | `docs/CLIP-REVIEW-RULES-RESEARCH.md`, 321 lines |
| `C:\b577` | `checkpoint/BL-577` | `bcd34a71` | `docs/HIKER-COOLDOWN-AUDIT.md`, 200 lines |
| `C:\b579` | `checkpoint/BL-579` | `fa93f445` | `docs/SLIDESHOW-REPLACEMENT.md`, 180 lines |
| `C:\b583` | `checkpoint/BL-583` | `c40e77bc` | `docs/SLIDESHOW-FULL-PROOF.md`, 155 lines |
| `...\.claude\worktrees\bl595` | `checkpoint/BL-595` | `65fb31fd` | `docs/EMAIL-DELIVERABILITY.md`, 174 lines |
| `C:\chq-bl598` | `checkpoint/BL-598` | `a2b7b2c3` | `docs/MULTIPOST-DESIGN.md`, 279 lines |
| `C:\chq-bl601` | `checkpoint/BL-601` | `36bacca8` | `docs/MULTIPOST-VERIFY.md`, 256 lines |
| `C:\bl604` | `checkpoint/BL-604` | `adc633b1` | `docs/SLIDESHOW-SIX-POST-PROOF.md`, 161 lines |

**8 pushed, 8 verified on origin, 0 failures.** No push failed, so no worktree had to be left alone
on this account.

## PART 3 — THE DELETION

### The approved list, and how it was bounded

The list was built from BL-759's own classification, never re-derived: its 142 SAFE paths, plus the 9
rescued in PARTs 1 and 2, and only those rescued paths whose push came back `VERIFIED_ON_ORIGIN`. The
main checkout and the LIVE worktree were then subtracted explicitly rather than trusted to be absent,
and the assertions printed:

```
BL759_SAFE = 142     RESCUED = 9     APPROVED_TOTAL = 151
MAIN_IN_LIST = 0     LIVE_IN_LIST = 0     APPROVED_BUT_NOT_REGISTERED = 0
```

Every approved path was a registered worktree of this repository. Nothing outside BL-759's named
paths was touched.

**Note on the LIVE worktree.** `C:\b758` had already removed itself between BL-759 and this round: it
was gone from both the registration and the disk before any deletion began. It was never touched here
and its guard stayed armed throughout regardless.

### Re-verification, which is the whole safety property

A dry run re-checked all 151 immediately before anything was deleted, testing four things per path:
staged changes, unstaged changes, commits absent from every origin ref, and any untracked non-log file
that had appeared since BL-759 wrote its inventory. **151 GO, 0 SKIP.** Nothing had drifted.

`C:\b575` was handled by name rather than by rule, because its 76 staged entries would otherwise have
tripped the generic test. BL-759's proof was re-run at deletion time rather than quoted:
`git diff --cached --name-only 1d69a62c` returned 0 files and `1d69a62c` was still an ancestor of
`origin/main`. Its index is that commit, that commit is on GitHub, and its working tree had zero
unstaged changes. Only on that basis was it removed.

Each removal then re-asserted the two fatal conditions one final time in the same loop iteration as
the `git worktree remove`, so a path that changed mid-run would have been skipped rather than deleted.

### Result

`git worktree remove --force` was used throughout, which deletes the folder and clears the
registration in one step, so no stale registration was left for a later `prune` to clean up. `--force`
was required because every one of these folders held untracked build logs, and it was safe for these
specific paths because the dry run had already established that is all it was overriding.

```
PROCESSED = 151
REMOVED   = 151   (60 in the first pass, 91 in the final pass)
FAILED    = 0     PARTIAL = 0     SKIPPED = 0     REFUSED = 0
```

**Skipped: nothing.** All 151 approved paths were removed and all 151 are confirmed absent from disk.

### One honest problem, and how it was handled

The first removal loop was launched in the foreground and the tool call timed out at ten minutes. The
loop itself was NOT killed by that timeout: it kept running detached. A resume loop was then started,
and for a few minutes **two loops were deleting from the same list**. That race produced a run of
`unpushed=ERR` and `gone before removal` rows, which look alarming and are not: `ERR` was git failing
to read a worktree whose admin directory the other loop had just removed, and every one of those rows
is a **SKIP**, meaning nothing was deleted on bad information. The guards did exactly what they exist
for.

Both loops were stopped, the filesystem was reconciled against the approved list, and a single clean
pass finished the remaining 91 with no race and no ambiguity. The final state was then verified from
the filesystem rather than from either loop's log. The lesson is recorded in PART 5.

### Disk

The honest measure is free space, taken from the volume before and after rather than summed from
per-directory estimates: **47.67 GB free before, 238.64 GB free after, 190.97 GB reclaimed**, of which
the worktrees and the temp folder both contributed. A correction to BL-759 is in PART 4.

## PART 4 — THE TEMP FOLDER, AND WHY IT KEPT COMING BACK

### What creates them, exactly

```
C:\Users\Game Centar\OneDrive\Desktop\clipper finder\tests\test_clone_rehearsal.py:450
    _WORK = tempfile.mkdtemp(prefix="clone_rehearsal_")

C:\Users\Game Centar\OneDrive\Desktop\clipper finder\tests\test_clone_rehearsal.py:458
    shutil.rmtree(_WORK, ignore_errors=True)
```

It is **not** the ClippersHQ repository. A grep for `clone_rehearsal` across ClippersHQ returns
nothing, which is why it was never found from here. It belongs to a different project on the same
machine, `clipper finder`, and it is that project's own git-hook rehearsal test.

It runs on every suite run: `tests/run_all.py` discovers "every `test_*.py` under `tests/` and under
any nested `<pkg>/tests/`", so `test_clone_rehearsal.py` is picked up unconditionally. `setUpModule`
makes one temp directory per module run and clones the repo into it; the module's own comments at
lines 398 to 402 explain that it clones rather than pushes because cloning hardlinks the object store
at about 0.5 s instead of transferring history at about 74 s. There is also a scheduled task,
`ClippersHQ-Backup`, running `tools\backup_schedule.ps1` daily since 2026-08-03, which is exactly the
date of the oldest surviving directory.

### Why deleting them never stuck, which is the actual bug

**The cleanup already exists and it silently fails.** `shutil.rmtree(..., ignore_errors=True)` on
Windows cannot delete read-only files: `os.unlink` raises `PermissionError`, and `ignore_errors=True`
swallows it without a word. Git marks every loose object and every pack file read-only.

The evidence is the wreckage itself. In a surviving directory, **every single remaining file is a git
object and every single one is `-r--r--r--`**:

```
remote1.git/objects/pack/pack-0d5b0bd...pack   -r--r--r--   505,329,588 bytes
remote1.git/objects/<17 loose objects>         -r--r--r--
repo/.git/objects/pack/pack-0d5b0bd...pack     -r--r--r--   505,329,588 bytes
repo/.git/objects/<24 loose objects>           -r--r--r--
```

Everything writable, the `config`, `HEAD`, `refs`, the index and the whole working tree, was deleted
successfully. Only the read-only objects survived. That is the signature of this exact defect, and it
explains the owner's experience perfectly: his manual deletions DID work, but the test recreates a
directory on every suite run, so the count climbed straight back.

### Does anything need them afterwards

**No.** `_WORK` is module-local state, discarded in `tearDownModule` in the same run. Nothing reads a
previous run's directory, and no path outside that module references the prefix. They are pure
leftovers from the moment the test finishes.

### The exact change, for the owner to make

This is another project, so it was diagnosed and NOT edited here. Replace line 458:

```python
def tearDownModule():
    if _WORK:
        shutil.rmtree(_WORK, ignore_errors=True)
```

with a handler that clears the read-only bit and retries, which is the standard Windows fix:

```python
def _force_rw(func, path, _exc):
    # Windows: git marks loose objects and packs read-only, and rmtree cannot
    # unlink a read-only file. ignore_errors=True hid this for 171 runs and left
    # about half a gigabyte of pack behind each time.
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except Exception:
        pass


def tearDownModule():
    if _WORK:
        if sys.version_info >= (3, 12):
            shutil.rmtree(_WORK, onexc=_force_rw)
        else:
            shutil.rmtree(_WORK, onerror=_force_rw)
```

`import stat` is needed; `os`, `sys` and `shutil` are already imported at lines 48, 52 and 50.

Two supporting measures worth taking at the same time. Add a sweep at the top of `setUpModule` that
deletes any `clone_rehearsal_*` older than a day, so a crashed run cannot leak forever. And note that
`CLIPPERSHQ_SKIP_CLONE_REHEARSAL=1` (line 73) already disables the test entirely: that is the
emergency brake, not the fix, because it silences a real safety check.

### What was deleted here

`171` directories existed. **1 was skipped for being modified 20 minutes earlier** and is named so the
owner can see the rule was applied rather than asserted:

```
SKIP  clone_rehearsal_dyncc37x   2026-08-10 16:53
```

The other **170 were removed, 0 failed**, by clearing the read-only attribute first and then deleting,
which is the same fix the test needs. Only `%TEMP%\clone_rehearsal_*` was touched. Nothing else in
`%TEMP%` and nothing outside it was.

### A correction to BL-759

BL-759 estimated these at "roughly 170 GB" from a robocopy sample. That figure **double-counted**. The
two pack files inside each directory are the same physical file: `stat` shows both at inode
`10977524092774061` with a link count of 2, because `git clone --local` hardlinks the object store, as
the test's own comment at line 399 says it does. Robocopy's `/L` listing counts each path separately.
The real physical cost was roughly half the reported figure. The 190.97 GB reclaimed is measured from
the volume and is not affected by that error.

## PART 5 — WHAT SURVIVED

### The main repo checkout, intact and unchanged

```
path            : C:\Users\Game Centar\OneDrive\Desktop\ClippersHQ
HEAD            : 018c22cab303e7b122cad74da1a17319c0c61c15   (unchanged, == origin/main)
git status      : 8 entries, byte for byte the same 8 untracked files as before this round
node_modules    : present, 564 real entries
.git            : present     package.json : present
git log         : reads normally
stashes         : 13, all still present
```

The 8 untracked entries are the same ones recorded at the start: `.claude/`,
`docs/BL-533-MERGE-REPORT.md`, `docs/SCRAPBADGER-TIKHUB-AUDIT.md`, `lp.html`, `lpv.html`, `pp.html`,
`r.html`, `rendered.html`. Nothing in the working copy was added, removed or modified.

### The LIVE worktree

`C:\b758` was already gone before this round began, removed by its own round. It was excluded from the
approved list, guarded by name in every deletion loop, and never touched.

### Every rescued branch, on origin and locally

Worktree removal deletes a checkout, never a branch, so all nine refs survive in the repository as
well as on GitHub. Verified after all deletion:

```
rescue/BL-439-uncommitted-growth-life-events  origin=7c700f5a local=7c700f5a  src/components/layout/notif-href.ts
research/R-1                                  origin=69410d3f local=69410d3f  docs/CLIP-REVIEW-RULES-RESEARCH.md
checkpoint/BL-577                             origin=bcd34a71 local=bcd34a71  docs/HIKER-COOLDOWN-AUDIT.md
checkpoint/BL-579                             origin=fa93f445 local=fa93f445  docs/SLIDESHOW-REPLACEMENT.md
checkpoint/BL-583                             origin=c40e77bc local=c40e77bc  docs/SLIDESHOW-FULL-PROOF.md
checkpoint/BL-595                             origin=65fb31fd local=65fb31fd  docs/EMAIL-DELIVERABILITY.md
checkpoint/BL-598                             origin=a2b7b2c3 local=a2b7b2c3  docs/MULTIPOST-DESIGN.md
checkpoint/BL-601                             origin=36bacca8 local=36bacca8  docs/MULTIPOST-VERIFY.md
checkpoint/BL-604                             origin=adc633b1 local=adc633b1  docs/SLIDESHOW-SIX-POST-PROOF.md
```

### Registration consistent with the filesystem

```
$ git worktree list
C:/Users/Game Centar/OneDrive/Desktop/ClippersHQ  018c22ca (detached HEAD)

prunable entries : 0
approved paths still on disk : 0 of 151
```

**One worktree registered, one worktree on disk, and it is the working copy.** No phantom entries, no
orphaned folders, nothing left for a `prune` to find. Because `git worktree remove` was used
throughout, no branch is still marked as checked out at a folder that no longer exists, so the owner
can now `git checkout main` in his own copy, which `C:\b575` had been blocking for weeks.

### Untouched, on purpose

The 36 reports-repo clones (`C:\chq-reports`, `C:\rp757`, `rep*`, `rpt*`, `C:\wt\reports*`) and the two
unrelated projects (`OBLITERATUS`, `ugcbounty`) were outside this round's mandate and were not touched.
They hold about 2.1 GB and are safe to delete whenever the owner wants; BL-759 verified all 36 clones
clean and fully pushed.

### The total

| | |
| --- | --- |
| Worktrees removed | **151** of 151 approved, 0 failed, 0 skipped |
| Temp directories removed | **170** of 171, 1 skipped as too recent |
| Work rescued to origin first | **9** branches, all verified |
| **Free space reclaimed** | **190.97 GB** (47.67 GB to 238.64 GB) |
| Work lost | **none** |

## WHAT THE OWNER SHOULD DO HIMSELF

1. **Fix the leak at its source**, PART 4, in `clipper finder\tests\test_clone_rehearsal.py:458`. It is
   another project so it was not edited from here. Until it is fixed, roughly half a gigabyte returns
   per suite run. This is the only item that matters; everything else is optional.
2. **Decide what to do with `rescue/BL-439-uncommitted-growth-life-events`.** Rebase, build and review
   it, or delete the branch deliberately. It should not sit unexamined forever, but it is now safe
   either way.
3. **Optionally delete the 36 reports clones and the twitch-clipper scratchpad.** BL-759 measured the
   scratchpad at 55.28 GB of `.mp4` files under `%TEMP%\claude\...twitch-clipper\...`, belonging to a
   different project. That is his call, not a repo matter.
4. **Nothing needs doing about the ClippersHQ repository itself.** It is clean, consistent and
   unchanged.

## WHAT PREVENTS THIS RECURRING

The worktrees came back at about 1.13 GB per round because the prompt template said to create one and
never said to remove it. BL-759 gave the exact wording; it is worth repeating because this round is
the proof it works:

> **CLEANUP (last step, after the verified push and the published report):** if you created a worktree
> for this round, remove it with `git -C "<main checkout>" worktree remove --force <path>`, and state
> the path removed and the disk reclaimed. Remove ONLY the worktree you created. Do NOT remove it if it
> holds uncommitted changes or a commit absent from origin: leave it and say what it holds. If you
> junctioned `node_modules` into it, delete the link with plain `rmdir <path>\node_modules` FIRST,
> because `--force` follows a junction and will empty the real directory.

> **WORKTREE:** create it at a SHORT path. Install dependencies ONLY if this round actually runs `tsc`
> or `npm run build`. Never junction `node_modules` from another checkout.

Three additions this round earned:

> **NEVER JUNCTION `node_modules`.** One junction in 153 worktrees was one away from destroying the
> working copy's dependencies during cleanup. If a round wants to save the install cost, it should skip
> the install, not borrow someone else's.

> **A LONG DELETION LOOP MUST RUN IN THE BACKGROUND.** A foreground tool timeout does NOT kill the
> shell it launched. This round had two deletion loops racing over one list for several minutes. It was
> harmless only because every iteration re-verified its own path and skipped on any doubt. Launch long
> loops with `run_in_background` and poll, and never start a resume pass without confirming the first
> one is dead.

> **A TEST THAT MAKES A TEMP DIRECTORY MUST DELETE IT ON WINDOWS TERMS.** `shutil.rmtree(...,
> ignore_errors=True)` over a git object store is a silent leak, because git's files are read-only.
> 171 directories accumulated in one week behind a cleanup that looked correct.

Nothing outside BL-759's named paths was touched, no other project on the machine was modified, and
no branch was merged to main.
