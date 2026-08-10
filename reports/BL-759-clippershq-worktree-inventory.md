# BL-759 — every git worktree on the owner's machine, and exactly which are safe to delete

**AUDIT ONLY. Nothing was deleted, pruned, committed, pushed, stashed or checked out.** Every git
command run was a read: `worktree list`, `status`, `log`, `diff`, `rev-list`, `rev-parse`,
`merge-base --is-ancestor`, `stash list`, `ls-files`, `branch -r --contains`, `hash-object` without
`-w`, `config --get`, `reflog`. Sizes came from `robocopy /L`, which lists and copies nothing.

## THE HEADLINE, FIRST

1. **`C:\Users\Game Centar\clippershq-bl439-wt` holds 370 lines of uncommitted source code that
   exists NOWHERE on origin.** This is the BL-729 scenario, live. Do not delete it.
2. **That same folder has its `node_modules` junctioned into the owner's real working copy.**
   Deleting it carelessly destroys the main checkout's `node_modules`. Details in PART 4.
3. **Eight more worktrees each hold one commit that is on no origin ref at all**, every one a written
   audit or design document, 155 to 321 lines.
4. **`C:\b575`'s famous 77 dirty files are NOT work.** Proven below: the index equals commit
   `1d69a62c`, which is already on origin. It is safe.
5. **The worktrees are not the biggest problem.** They total 107.3 GB, not 200 GB. The user TEMP
   folder holds **251.76 GB**, of which roughly **170 GB is 170 abandoned `clone_rehearsal_*`
   directories** still being created today. PART 3.

Disk right now: **C: is 930.6 GB, 891.6 GB used, only 38.9 GB free.** That is the slowness.

## PART 1 — THE COMPLETE INVENTORY, RECONCILED

`git worktree list --porcelain` reports **153** worktrees. A filesystem sweep for any directory
containing a `.git` entry, across `C:\*`, `C:\wt\*`, `C:\Users\Game Centar\*` and the repo's own
`.claude\worktrees\*`, found **190**.

| Reconciliation | Count | Detail |
| --- | --- | --- |
| Registered AND present | **153** | every registered worktree exists on disk |
| Registered but MISSING | **0** | git tracks no folder that is gone; `git worktree list` reports 0 prunable |
| Present but UNREGISTERED | **38** | none of them is a ClippersHQ worktree |

The 38 unregistered are not stray worktrees. They are **36 independent clones of
`ilenader/clippershq-reports`** (`C:\chq-reports`, `chq-reports-671/673/675/681`, `chqr`,
`rep734/737/739/742/743/744/746/747/748/750/751/754`, `rp757`,
`rpt610/613/628/629/631/632/633/634/683/689/691/692/693/694/698`, `C:\wt\reports`,
`C:\wt\reports596`), one per publishing round, plus **2 unrelated projects**
(`C:\Users\Game Centar\OBLITERATUS`, `C:\Users\Game Centar\ugcbounty`). **There is no stale
registration and no orphaned worktree folder.** The two sets reconcile completely.

### Size, split by component

| Group | Count | Total | node_modules | .next | everything else |
| --- | --- | --- | --- | --- | --- |
| All registered worktrees | 153 | **107.3 GB** | 82.7 GB | 18.6 GB | 6.0 GB |
| The same, excluding the main checkout | 152 | **105.0 GB** | 81.8 GB | 17.7 GB | 5.5 GB |
| Reports-repo clones | 36 | 1.6 GB | 0 | 0 | 1.6 GB |
| Unrelated repos | 2 | 0.5 GB | 0 | 0 | 0.5 GB |

**The owner's ~200 GB estimate is roughly double the truth for worktrees: the correct figure is
107.3 GB.** He was not wrong that ~200 GB is missing, he was wrong about where it went. See PART 3.

### The shape of it, which is the whole lever

| | Count | Total |
| --- | --- | --- |
| Worktrees WITH a real `node_modules` | **93** | **105.5 GB** (avg 1.13 GB each) |
| Worktrees WITHOUT `node_modules` | **60** | **1.8 GB** (avg 30 MB each) |

**Sixty rounds already completed without ever installing `node_modules`, and they cost 30 MB each
instead of 1.13 GB.** A worktree with dependencies costs 38 times more than one without. 87 of the
153 also carry a `.next` build at ~210 MB each.

Every worktree is one of exactly three sizes: **~30 MB** (checkout only), **~0.93 GB** (checkout plus
`node_modules`) or **~1.13 GB** (checkout plus `node_modules` plus `.next`).

### The largest, and the main checkout named explicitly

| Path | Size | node_modules | .next | Branch or commit | Last modified |
| --- | --- | --- | --- | --- | --- |
| **`C:\Users\Game Centar\OneDrive\Desktop\ClippersHQ`** | **2.31 GB** | 0.89 | 0.96 | detached `018c22ca` | 2026-08-10 15:01 |
| `C:\m757` | 1.14 GB | 0.89 | 0.21 | detached `018c22ca` | 2026-08-10 14:29 |
| `C:\m750`, `m747`, `m741`, `m738`, `m735`, `m731`, `m727`, `m720`, `m719`, `m718` | 1.14 GB each | 0.89 | 0.21 | merge rounds | 2026-08-05 to 08-09 |

> **THE MAIN CHECKOUT IS `C:\Users\Game Centar\OneDrive\Desktop\ClippersHQ`. It is the owner's
> working copy and is NEVER a deletion candidate, nor is its `node_modules` or its `.git`.** It is
> the only path here holding the repository's real object database; every other entry is a worktree
> pointing back at it. Deleting it destroys all 152 others at once.

## PART 2 — WHAT WOULD BE LOST, PER WORKTREE

### Repo-wide facts that apply to all of them

* **Stashes: 13, and they are SAFE from any worktree deletion.** `refs/stash` lives in the main
  checkout's `.git`, shared by every worktree, so deleting a worktree folder cannot delete a stash.
  They date from 2026-07-12 to 2026-07-14: eleven named `BL-###-preexisting` (snapshots taken before
  a round began) and three `WIP on ...` from BL-384, BL-404 and BL-420. None belongs to any folder
  listed below. They are worth a separate look one day; they are not part of this decision.
* **Untracked files are almost entirely build logs.** Across all 44 worktrees with any dirt, the
  untracked set is dominated by `tsc.log` (31), `npmci.log` (29), `build.log` (28), `build2.log`
  (13), `gen.log` (9), `push.log` (8) and similar. Only **40** untracked entries are not `.log`,
  `.exit` or `.tmp`.
* **Every one of those 40 was checked individually and none is unique.** `docs/BL-533-`, `BL-575-`,
  `BL-685-`, `BL-687-`, `BL-697-MERGE-REPORT.md`, `docs/SCRAPBADGER-TIKHUB-AUDIT.md`,
  `scripts/bl721-revival-pilot.ts`, `bl721-map-buckets.ts`, `bl721-inspect-200.ts`,
  `bl669-merged-proof.ts`, `bl580-probe.cjs` are all present on `origin/main`. The report drafts
  `_report_BL-576/581/587/591.md`, `BL-580-REPORT.md` and `BL-584-REPORT.md` were each published to
  `ilenader/clippershq-reports` as `reports/BL-576.md`, `BL-581.md`, `BL-587.md`, `BL-591.md`,
  `BL-580.md` and `BL-584.md`. The rest are probe output (`bl580-probe-results.json`,
  `bl721-pilot-results.json`, `before-snapshot.json`, `tA/tB/tC.sql`, `rollback.sql`, `DONE`,
  `ci.done`, rendered HTML previews), all reproducible.

### `C:\b575` — the 77 dirty files, settled

The worry was justified and the answer is clean. The breakdown is **76 STAGED entries and ZERO
unstaged**, plus one untracked file:

* `git diff --cached --name-only 1d69a62c` returns **0 files**. The index is byte-for-byte the commit
  `1d69a62c` ("Merge BL-572", 2026-07-17 22:47).
* `git merge-base --is-ancestor 1d69a62c origin/main` returns **true**. That commit is on GitHub.
* `git diff --name-only` (working tree against index) returns **0 files**. Nobody edited anything.
* The single untracked file, `docs/BL-575-MERGE-REPORT.md`, is present on `origin/main`.

What happened is mechanical, not human: b575 has the `main` branch checked out, its checkout was left
at the July 17 state, and the local `main` ref later moved forward to `91b84410`. Git then reports the
gap between the two as 48 deletions and 28 modifications. Those "deletions" are files added to main
after July 17 (`retire-dead-clips.ts`, `gone-counter.ts`, `platform-fee.ts`, the iOS splash PNGs) and
those "modifications" are ordinary later edits to `tracking.ts`, `balance.ts` and the rest. **No hand
written work exists in b575. It is SAFE TO DELETE.** A pleasant side effect: removing it releases the
`main` branch, which is currently checked out there and has been forcing round after round into
separate worktrees.

### THE ONE THAT HOLDS REAL WORK

**`C:\Users\Game Centar\clippershq-bl439-wt` — HAS UNCOMMITTED WORK. DO NOT DELETE.**

Branch `checkpoint/BL-439`, HEAD `e096bc64` (Merge BL-435, 2026-07-13). **Five modified files, all
UNSTAGED, 370 insertions and 3 deletions**, last touched 2026-07-13 15:51 to 15:56:

```
src/lib/growth/in-app.ts              +244
src/lib/growth/triggers.ts             +76
src/components/layout/notif-href.ts    +34
src/lib/notifications.ts               +15
src/lib/notification-severity.ts        +4
```

It is in-app growth notification work: a new exported `collapseGrowthBurst`, plus handling for
`EARNINGS_MILESTONE`, `VIEW_MILESTONE`, `LEVEL_UP`, `STREAK_MILESTONE`, `FIRST_PAYOUT_REQUESTED`,
`FIRST_PAYOUT_PAID`, `REFERRAL_CONVERTED`, `NEW_CAMPAIGN_LIVE`, `REPEATED_REJECTIONS`,
`ACCOUNT_VERIFICATION_FAILED` and `WIN_BACK`.

**It was never shipped.** `git grep collapseGrowthBurst` across `origin/main` returns nothing, and a
sweep of **every** `refs/remotes/origin/*` ref returns nothing. This code exists in exactly one place
on earth: that folder. Whether the owner still wants the feature is his call; losing it by accident
is not.

### THE EIGHT WITH UNPUSHED COMMITS

Each holds exactly **one** commit reachable from no origin ref and no local tag, and in every case the
document it adds is **absent from `origin/main`**. Each is ~30 MB, so keeping all eight costs 0.2 GB.

| Worktree | Branch | Commit | Adds | Date |
| --- | --- | --- | --- | --- |
| `C:\r1` | `research/R-1` | `69410d3f` | `docs/CLIP-REVIEW-RULES-RESEARCH.md`, 321 lines | 2026-07-16 |
| `C:\b577` | `checkpoint/BL-577` | `bcd34a71` | `docs/HIKER-COOLDOWN-AUDIT.md`, 200 lines | 2026-07-18 |
| `C:\b579` | `checkpoint/BL-579` | `fa93f445` | `docs/SLIDESHOW-REPLACEMENT.md`, 180 lines | 2026-07-18 |
| `C:\b583` | `checkpoint/BL-583` | `c40e77bc` | `docs/SLIDESHOW-FULL-PROOF.md`, 155 lines | 2026-07-18 |
| `...\.claude\worktrees\bl595` | `checkpoint/BL-595` | `65fb31fd` | `docs/EMAIL-DELIVERABILITY.md`, 174 lines | 2026-07-20 |
| `C:\chq-bl598` | `checkpoint/BL-598` | `a2b7b2c3` | `docs/MULTIPOST-DESIGN.md`, 279 lines | 2026-07-20 |
| `C:\chq-bl601` | `checkpoint/BL-601` | `36bacca8` | `docs/MULTIPOST-VERIFY.md`, 256 lines | 2026-07-20 |
| `C:\bl604` | `checkpoint/BL-604` | `adc633b1` | `docs/SLIDESHOW-SIX-POST-PROOF.md`, 161 lines | 2026-07-20 |

Each is a finished, self-contained audit: the HikerAPI cooldown hypothesis refuted, LamaTok resolving
TikTok slideshows, the six-post slideshow proof, the Resend delivered-but-unmeasured verdict, and the
batch-submission design plus its verification naming two money traps. **Deleting these folders erases
those commits permanently.** They are cheap to rescue and they are not junk.

### CANNOT DETERMINE

**`C:\b758`** — registered, detached at `018c22ca`, no `node_modules` yet, **modified 27 minutes
before this audit ran**. A round is live in it right now. `C:\chq-reports` was touched at the same
minute and is its reports clone. **Do not touch either until that round finishes.** Classified
CANNOT DETERMINE rather than assumed safe, on purpose.

### THE CLASSIFICATION

| Class | Count | Disk |
| --- | --- | --- |
| **SAFE TO DELETE** | **142** | **103.9 GB** |
| HAS UNPUSHED COMMITS | 8 | 0.2 GB |
| HAS UNCOMMITTED WORK | 1 | see the junction warning |
| CANNOT DETERMINE (live round) | 1 | 0.03 GB |
| MAIN CHECKOUT (excluded, never delete) | 1 | 2.31 GB |

Every one of the 142 satisfies all three tests: `git rev-list HEAD --not --remotes=origin --count`
is **0**, working tree against index is **0 files**, and every untracked file is either a build log or
provably present on `origin/main` or in the reports repo. `b584` is included: its HEAD is not on
`origin/main` but it is on `origin/checkpoint/BL-584`, so nothing is lost.

**SAFE, with `node_modules` (91 worktrees, 102.4 GB)** — this is where the disk actually is:
`a745 a749 b571 b573 b575 b576 b580 b581 b586 b587 b590 b591 b625 b630 b648 b659 b668 b669 b671 b672
b673 b676 b678 b679 b681 b682 b683 b686 b689 b692 b694 b698 b699 b700 b701 b704 b705 b707 b709 b711
b713 b715 b718 b719 b720 b721 b723 b724 b725 b728 b729 b733 b734 b736 b739 b740 b744 b746 b748
bl538 bl603 bl605 bl606 bl607 bl610 bl632 chq-bl602 m675 m685 m687 m691 m693 m697 m702 m703 m718
m719 m720 m727 m731 m735 m738 m741 m747 m750 m757 wt\bl641 wt\bl649 wt\bl650 wt\bl666 wt\bl667`

**SAFE, without `node_modules` (51 worktrees, 1.5 GB)** — deleting these barely helps:
`a732 a752 b572 b582 b584 b588 b627 b635 b640 b642 b644 b647 b652 b656 b661 b665 b670 b674 b677 b680
b684 b688 b690 b695 b696 b706 b708 b710 b714 b716 b717 b722 b726 b730 b737 b742 b743 b751 b754
bl549 bl608 bl628 bl629 bl633 bl634 m729 wt\bl567 wt\bl596 wt\bl655 wt\bl657
...\.claude\worktrees\checkpoint+BL-636`

## PART 3 — WHAT ELSE IS EATING DISK, AND IT IS BIGGER THAN THE WORKTREES

| Artefact | Size | Safe to remove |
| --- | --- | --- |
| **`%TEMP%\clone_rehearsal_*` — 170 directories** | **~170 GB** (8-dir sample, avg 1.0 GB) | **YES, and this is the single biggest win** |
| `%TEMP%` overall (measured) | **251.76 GB** | mostly yes, see below |
| `%TEMP%\claude\...twitch-clipper\...` | **55.28 GB** | a DIFFERENT project's scratchpad, full of `.mp4` files; the owner's call |
| `%LOCALAPPDATA%\npm-cache` | **16.00 GB** | yes, npm refetches on demand |
| All 153 worktrees | 107.3 GB | per PART 2 |
| `%TEMP%\claude\...` other project | 3.01 GB | scratchpad, yes |
| `C:\Windows\Temp` | 1.21 GB | yes |
| Reports-repo clones, 36 of them | 1.64 GB | yes, all clean and fully pushed |
| `%TEMP%\bl929i_*\head.tar`, 2 dirs | ~1.5 GB | yes |
| `%TEMP%\claude\...ClippersHQ` scratchpad | 0.83 GB | yes |
| Unrelated repos (OBLITERATUS, ugcbounty) | 0.5 GB | the owner's call, not repo related |
| **`C:\Users\Game Centar\OneDrive\Desktop\ClippersHQ`** | **2.31 GB** | **NO. Working copy. Excluded.** |
| **that folder's `node_modules` and `.git`** | 0.89 + included | **NO. Never.** |

The `clone_rehearsal_*` finding deserves its own paragraph. Each directory contains **two** copies of
the same ~600 MB git pack, once under `remote1.git\objects\pack\` and once under
`repo\.git\objects\pack\`. They are backup and restore drill leftovers. There are **170** of them,
the oldest dated **2026-08-03** and the newest **2026-08-10, today**, so whatever creates them is
still running and still not cleaning up. At roughly 1 GB apiece that is about **170 GB, more than
every ClippersHQ worktree put together**, accumulated in one week.

`%TEMP%` also holds **65,817 child directories**. That count alone slows every process that touches
the temp path, independently of the bytes.

Honest limit: `%TEMP%` at 251.76 GB is a measured total and `clone_rehearsal_*` at ~170 GB is a
sampled estimate, not a census. A full recursive walk of `%TEMP%` exceeded the time budget twice, and
`du` proved unusable here, taking over ten minutes on a single 1.13 GB worktree while `robocopy /L`
did the same job in 1.7 seconds. The remaining ~25 GB of `%TEMP%` is spread across tens of thousands
of small directories and was not itemised.

## PART 4 — THE SAFE DELETION PROCEDURE, SPEC'D AND NOT PERFORMED

**NONE of the following was run. Every command below is for the owner to run himself.**

### STOP. Read this first, it is the one that bites.

`C:\Users\Game Centar\clippershq-bl439-wt\node_modules` is **not a folder. It is a junction pointing
at `C:\Users\Game Centar\OneDrive\Desktop\ClippersHQ\node_modules`**, confirmed by
`LinkType = Junction`, and both resolve to the same live 564-entry directory.

`rmdir /s`, `rm -rf` and `git worktree remove --force` all follow that junction and **delete the
contents of the real `node_modules` in the working copy**. The worktree that must not be deleted is
therefore also the one that is dangerous to delete. If it is ever removed, **delete the junction
first** with `rmdir "C:\Users\Game Centar\clippershq-bl439-wt\node_modules"` (no `/s`, which removes
the link only), and only then the folder. No other worktree has a junction; only that one.

Two related reparse points are harmless and must not be confused with it: the main checkout's own
`node_modules` and `.git` carry a reparse attribute with **no link type and no target**, which is
OneDrive Files On-Demand marking placeholders, not a junction.

### Step 1, rescue what is not on GitHub, BEFORE deleting anything

The eight unpushed commits, each already committed and needing only a push:

```
git -C C:\r1          push origin research/R-1
git -C C:\b577        push origin checkpoint/BL-577
git -C C:\b579        push origin checkpoint/BL-579
git -C C:\b583        push origin checkpoint/BL-583
git -C "C:\Users\Game Centar\OneDrive\Desktop\ClippersHQ\.claude\worktrees\bl595" push origin checkpoint/BL-595
git -C C:\chq-bl598   push origin checkpoint/BL-598
git -C C:\chq-bl601   push origin checkpoint/BL-601
git -C C:\bl604       push origin checkpoint/BL-604
```

Verify each with `git ls-remote origin <branch>` before deleting that folder. Then those eight become
SAFE and can be removed with the same procedure as the rest.

The uncommitted work in `clippershq-bl439-wt` is the one thing a push cannot rescue on its own. Either
copy the five files out:

```
robocopy "C:\Users\Game Centar\clippershq-bl439-wt\src" "C:\bl439-rescue\src" ^
  in-app.ts triggers.ts notif-href.ts notifications.ts notification-severity.ts /S
```

or commit and push them from inside that folder onto `checkpoint/BL-439`. Until one of those is done,
**that folder is not deletable at any price**.

### Step 2, remove the safe worktrees the correct way

The right command is `git worktree remove`, which deletes the folder AND clears the registration in
one step. Run it from the main checkout:

```
git -C "C:\Users\Game Centar\OneDrive\Desktop\ClippersHQ" worktree remove --force C:\b571
git -C "C:\Users\Game Centar\OneDrive\Desktop\ClippersHQ" worktree remove --force C:\b573
...one line per safe path...
```

`--force` is required here and is not a shortcut: every one of these folders contains untracked build
logs, and plain `worktree remove` refuses any worktree that is not pristine. `--force` is safe for
these specific 142 **because PART 2 already proved that what it overrides is `tsc.log` and
`build.log` and nothing else**. Never apply it to `clippershq-bl439-wt`, both for the junction and
for the 370 lines.

Two of the safe paths also have a local branch that survives the folder's removal, which is correct
and wanted: `git worktree remove` deletes the checkout, never the branch or its commits.

### What happens if he just deletes the folders in Explorer

The disk is reclaimed and no commit is lost, but **git keeps a stale registration for every one**.
`git worktree list` then shows 142 phantom entries, each printing `prunable: gitdir file points to
non-existent location`, and the administrative files under
`ClippersHQ\.git\worktrees\<name>\` stay behind. Worse, the branch each one held stays marked as
checked out, so `git checkout <that-branch>` fails with "already checked out at ..." pointing at a
folder that no longer exists. The repair is one command:

```
git -C "C:\Users\Game Centar\OneDrive\Desktop\ClippersHQ" worktree prune
```

So Explorer deletion followed by a single `worktree prune` is an acceptable path and is much faster
for 142 folders. **The one thing he must not do either way is drag `clippershq-bl439-wt` to the
Recycle Bin**, because Explorer follows the junction into the real `node_modules` too.

### Disk reclaimed

| Action | Reclaimed |
| --- | --- |
| The 142 safe worktrees | **103.9 GB** |
| The 36 reports clones (all clean and pushed, leave `chq-reports` until the live round ends) | 1.6 GB |
| The 170 `clone_rehearsal_*` temp directories | **~170 GB** |
| The npm cache | 16.0 GB |
| The twitch-clipper scratchpad, a different project, the owner's call | 55.3 GB |
| **Total, without touching anything that holds work** | **~292 GB, and ~347 GB with the twitch scratchpad** |

Against 38.9 GB free today, the worktrees alone take him to roughly 143 GB free, and adding the
`clone_rehearsal_*` sweep to roughly 313 GB.

### What must happen first for the ones that are not safe

| Path | Required first |
| --- | --- |
| `clippershq-bl439-wt` | Copy the 5 files out, or commit and push them. **Then remove the `node_modules` junction with `rmdir` before deleting the folder.** |
| `r1`, `b577`, `b579`, `b583`, `bl595`, `chq-bl598`, `chq-bl601`, `bl604` | `git push` the branch, verify with `git ls-remote`, then delete |
| `b758`, `chq-reports` | Wait for the live round to finish, re-run `git status` and `git rev-list HEAD --not --remotes=origin`, then decide |
| The main checkout | Nothing. It is never deleted. |

## PART 5 — THE ROOT CAUSE IS THE PROMPT TEMPLATE

Every round's prompt says some version of *"merge in a SEPARATE clean worktree at a SHORT path"*.
**None of them says what to do with it afterwards.** So 153 worktrees exist, and 93 of them ran
`npm ci` and then `npm run build`, which is where 105.5 of the 107.3 GB comes from.

The isolation itself has earned its place and must not be dropped. `C:\b575` holding `main` in a
stale state has forced round after round into a separate folder, exactly as designed, and parallel
sessions have not collided because of it. BL-729 recovered real work from an isolated worktree, and
this audit found another 370 lines in one. The isolation is not the problem. **The leftover is.**

Three options, and the smallest one wins:

* **One persistent shared worktree.** Rejected. It reintroduces exactly the collision the isolation
  prevents, and a stale shared folder is precisely what `b575` already is.
* **Skip `node_modules` entirely.** Tempting, and 60 rounds already do it, but a merge round has to
  run `npm ci`, `tsc` and `npm run build` to report a real exit code. Removing that removes the
  verification, which is worse than the disk.
* **Keep the isolation, keep the build, delete the folder at the end.** This is the smallest change
  that works. The build has already produced its verdict by then; the 1.13 GB has no further purpose
  once the branch is pushed and the report is written.

### Exact wording to add to the standing prompt template

Add this as a step immediately before the notify step:

> **CLEANUP (last step, after the verified push and the published report, before notify):** if you
> created a worktree for this round, remove it now from the main checkout with
> `git -C "<main checkout>" worktree remove --force <your worktree path>`, and state the path removed
> and the disk reclaimed in the report. Remove ONLY the worktree you created this round. Do NOT
> remove it if it still holds uncommitted changes or a commit absent from origin: in that case leave
> it, and say in the report exactly what it holds and why it was kept. If you junctioned or symlinked
> `node_modules` into the worktree, delete the link with plain `rmdir <path>\node_modules` BEFORE
> removing the worktree, because `--force` follows a junction and will empty the real directory.

And tighten the existing setup line so the cheap rounds stay cheap:

> **WORKTREE:** create it at a SHORT path. Install dependencies ONLY if this round actually runs
> `tsc` or `npm run build`; an audit, a doc change or a report needs neither, and skipping the install
> takes the worktree from about 1.13 GB to about 30 MB. Never junction `node_modules` from another
> checkout.

Two further one-line changes worth making at the same time:

> **REPORTS CLONE:** reuse a single reports clone at a fixed path rather than a new `rep###` per
> round, or delete yours at the end. There are 36 of them.
>
> **REHEARSALS AND DRILLS:** any drill that clones the repo into `%TEMP%` must delete its directory
> when it finishes. 170 `clone_rehearsal_*` directories are currently holding roughly 170 GB.

## PART 6 — THE VERDICT

| | |
| --- | --- |
| Worktrees registered | **153**, all present, 0 missing, 0 stale registrations, 0 unregistered ClippersHQ worktrees |
| **SAFE TO DELETE now** | **142 worktrees, 103.9 GB** |
| **Need action first** | **9 worktrees**: 8 need one `git push` each, 1 needs its files rescued |
| Cannot determine | **1** (`C:\b758`, a round is live in it) |
| Excluded, never delete | **1**, `C:\Users\Game Centar\OneDrive\Desktop\ClippersHQ`, the working copy |
| Also safe, outside the worktrees | 36 reports clones (1.6 GB), 170 `clone_rehearsal_*` (~170 GB), npm cache (16 GB) |
| **Total reclaimable without touching any work** | **~292 GB** |
| Free space today | **38.9 GB of 930.6 GB** |

### NAMED PROMINENTLY, BECAUSE BL-729 PROVED THIS IS REAL

> ## `C:\Users\Game Centar\clippershq-bl439-wt`
>
> **370 lines of uncommitted in-app growth notification code, written 2026-07-13, present on no
> origin branch anywhere. `collapseGrowthBurst` and eleven notification types exist in this folder
> and nowhere else.**
>
> **Its `node_modules` is a junction into the main working copy. Deleting this folder with
> `rm -rf`, `rmdir /s` or `--force` will also empty the real `node_modules` at
> `C:\Users\Game Centar\OneDrive\Desktop\ClippersHQ\node_modules`.**
>
> Rescue the five files first. Then `rmdir` the junction. Only then consider the folder.

Eight more folders (`r1`, `b577`, `b579`, `b583`, `bl595`, `chq-bl598`, `chq-bl601`, `bl604`) each
hold one finished audit document that is on no origin ref. Together they occupy 0.2 GB, so there is
no disk argument for rushing them. **Push those eight, rescue bl439, and the other 142 can go
today.**

## WHAT COULD NOT BE DETERMINED, AND WHY

* **`C:\b758` and `C:\chq-reports`.** A round was writing to both 27 minutes before this audit. Their
  state at the moment of any deletion cannot be known from here, so they are CANNOT DETERMINE rather
  than assumed safe.
* **The full `%TEMP%` itemisation.** 251.76 GB and 65,817 child directories are measured facts; the
  `clone_rehearsal_*` total of ~170 GB is extrapolated from an 8-directory sample averaging 1.0 GB.
  A complete walk was attempted twice and exceeded the time budget both times. A first sampling pass
  over 150 random `%TEMP%` subdirectories extrapolated to 400 GB, which is impossible against the
  measured 251.76 GB, so that estimate was discarded rather than reported: the distribution is
  heavy-tailed and a small sample overstates it. The `clone_rehearsal_*` figure is more reliable
  because those directories are uniform by construction, each holding the same pack twice.
* **The 13 stashes were listed, not evaluated.** Their contents were not diffed. They are unaffected
  by any worktree deletion, so they did not need to be resolved for this decision.
* **`git worktree list` was read, never pruned**, so any registration that git would consider stale
  is reported as git currently sees it: there were none.
* **`git checkout main` was NOT run**, contrary to the round's opening line, and could not have been:
  `main` is checked out in `C:\b575`, and checking out anywhere else is a state change this audit was
  forbidden to make. `git fetch origin` was run because it only updates remote-tracking refs and
  touches no worktree. All work was done from the main checkout as instructed, reading only.
* **No `checkpoint/BL-759` branch was created in ClippersHQ.** Creating a branch is a state-modifying
  git command, which the safety block forbids in every worktree including the main one. An audit that
  changes no file would have nothing to put on it. The report is published to the reports repository,
  which is a separate repository and the actual deliverable.

Nothing was deleted, pruned, committed, pushed, stashed, reset or checked out in the ClippersHQ
repository or in any of its 153 worktrees.
