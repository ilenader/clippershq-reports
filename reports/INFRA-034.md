# INFRA-034 — 93 of the root folders are a DIFFERENT project, and deleting all of them reclaims less than one directory inside this repo

**Date:** 2026-08-03 · **Type:** Read-only filesystem audit · **Spend:** **$0.00** (no paid calls)

Preconditions: `tools/claims_read.py --holders scratch` → **FREE**; `git status --porcelain`.
Claimed **INFRA-034**, `scratch/` only.

**NOTHING WAS DELETED, MOVED OR RENAMED.** Every git command used is query-only
(`remote -v`, `status --porcelain`, `rev-list --count`, `worktree list`, `ls-remote`). The only
files written are under `scratch/`. This round reports; the operator decides and executes.

---

## 1. THE HEADLINE: they are not ours

The operator opened `C:\b582`, found `next`, `node_modules`, `prisma` and concluded it was
probably not ClippersHQ. **He was right, and it is worse than "probably".**

```
this project        origin  https://github.com/ilenader/clipper-finder.git
                    root commit  8aa60d854e45...

C:\b582             origin  https://github.com/ilenader/Clippershq.git
                    root commit  e71073199683...        <- A DIFFERENT REPOSITORY
                    branch  checkpoint/BL-582
```

**Different remote, different root commit.** `next.config.ts` has never existed anywhere in
this project's history (`git log --all -- next.config.ts` → empty). `ilenader/Clippershq.git`
is a **Next.js / Prisma marketplace application** that merely shares the name — and it uses the
same `BL-NNN` round-numbering convention, which is exactly why its folders look like ours.

**124 non-system directories at `C:\` (140 total; 16 are Windows' own):**

| group | count | remote | ours? |
|---:|---|---|---|
| **93** | `b571…b711`, `bl538…bl634`, `m675…m703`, `rpt610…rpt698`, `chq-bl598…`, `r1`, `c` | `ilenader/Clippershq.git` | **NO — different project** |
| **21** | `chq-reports*`, `chqr`, `rpt6xx` (reports variants) | `ilenader/clippershq-reports.git` | **yes** — our public reports repo |
| **19** | `mbwt/*` | our `memebot` (registry-resolved) | **yes** |
| **11** | `wt/*` | 9 × `Clippershq.git` + 2 × reports | mixed |
| **~6** | `WebClones`, `projects`, `projects1`, `common_attachment`, `w`, `c` | no remote | **NO / unknown** |

`projects/ayocin-next`, `projects1/ayocin-next-starter` and `WebClones/` (414 MB of saved
websites: `ayocin.whtt`, `copy dobar website.whtt`) are a **third** unrelated body of work.
I do not judge whether he needs them.

---

## 2. THE DECISIVE CHECK: no root folder holds anything this project cannot regenerate

Searched every one of the 124 for `master_leads.csv`, `clip_library/`, `songs.json`,
`runs.jsonl`, `ground_truth/`, `config.json`, `spend.json`:

```
folders holding one of our unique data files or directories:  0
```

**Zero.** Every copy of this project's irreplaceable data lives in the working tree only.

### What each group would cost to regenerate

| group | state | regenerating costs |
|---|---|---|
| 21 reports clones | **all clean, all `ahead=0`** | a `git clone` — **free** |
| 19 `mbwt/*` worktrees | **all clean, 0 modified, 0 untracked**; every `mb/*` branch pushed | `git worktree add` — **free** |
| 93 `Clippershq.git` folders | **only 18 of 93 are clean + pushed** | **not ours to price** — see §3 |

Our memebot's local `main` is **3 commits ahead of `origin/main`** — that is in
`clipper finder/memebot`, the working tree, **not** in any root folder. Worth pushing; not a
deletion question.

---

## 3. DO NOT DELETE — 75 of the 93 hold work that is not on a remote

They are not ours, but the operator asked which are safe, and these are not:

```
93 Clippershq.git folders checked
  18  clean and pushed
  75  have unpushed commits, uncommitted changes, or no upstream at all
```

Examples, verbatim from `scratch/infra034_cq.txt` (`folder|branch|commits-ahead|dirty-files`):

```
b575|main|0|77                 <- 77 uncommitted files
b584|checkpoint/BL-584|1|7     <- 1 unpushed commit AND 7 dirty files
b572|checkpoint/BL-572|NOUP|0  <- branch has NO upstream: nothing to push to
b581|bl581-merge|0|5
```

`NOUP` means the branch has **no upstream configured** — `git log @{u}..` cannot even run, and
the commits exist on this disk only. **That is a stronger do-not-delete signal than a non-zero
ahead-count, not a weaker one.**

**Recommendation for the 93: do not bulk-delete.** They belong to `Desktop\ClippersHQ`, and
that project's own operator should run `git worktree list` there and prune deliberately.

---

## 4. LIVENESS, BY PID

```
processes enumerated : 472   (Win32_Process via CIM)
root folders checked : 124
result               : NO root folder is named by any running process
```

**HONEST LIMIT, and it changes what the negative means:** this is a **command-line and
executable-path match, not an open-handle enumeration**. A process whose *working directory* is
inside a folder without naming it in argv is not caught. **A hit proves use; a miss does not
prove the folder is free.** For a delete, the operator should close editors and terminals
first regardless.

**My first version of this check printed a confident all-clear from a silent zero.** A
non-UTF-8 byte in one process's command line broke the JSON decode, `except ValueError:
data = []` swallowed it, and it reported *"processes enumerated: 0 … NO root folder is held"* —
on the one question in this round where a wrong all-clear precedes a deletion. It now
**refuses to answer** rather than answering emptily, and warns if the table is implausibly
small.

---

## 5. THE THREE LISTS

Sizes are **measured where stated and extrapolated where stated** — see the limits section;
`du` on these trees runs ~35 s per folder on this disk and the full 124 did not complete.

### SAFE — reproducible, nothing unique

| what | count | size | regenerating costs |
|---|---:|---:|---|
| reports clones (`rpt*`, `chq-reports*`, `chqr`) | 21 | **~130 MB** (measured 2, 3, 68 MB) | `git clone` — free |
| `mbwt/` memebot worktrees | 19 | **776 MB** (measured, whole tree) | `git worktree add` — free |
| **SAFE total** | **40** | **≈0.9 GB** | **$0.00** |

> **`mbwt` must be removed with `git worktree remove`, not `rm -rf`.** Deleting the directory
> leaves 19 stale entries in this repo's memebot registry; `git worktree prune` afterwards is
> the repair. No render intermediates are in these — the ~$0.0007-per-render cost does not
> apply to any folder in this list.

### DO NOT DELETE

| what | count | reason |
|---|---:|---|
| 75 of the 93 `Clippershq.git` folders | 75 | unpushed commits, uncommitted changes, or **no upstream at all** |
| — | | *(none of ours: no root folder holds our unique data)* |

### NOT OURS — for the operator to decide

| what | count | size | what it appears to be |
|---|---:|---:|---|
| `Clippershq.git` worktrees | 93 | **≈3.1 GB** (6 measured at 33–34 MB, ~1,240 files each) | a **Next.js / Prisma marketplace app**, `ilenader/Clippershq.git` |
| `wt/*` | 11 | not measured | 9 more `Clippershq.git` worktrees + 2 reports clones |
| `WebClones` | 1 | **414 MB** (measured) | saved website copies — `.whtt` archives |
| `projects`, `projects1` | 2 | not measured | `ayocin-next`, `ayocin-next-starter` |
| `common_attachment`, `c`, `w`, `r1` | 4 | small | one JSON cache; `c/Users`; `w/rrepo` (a reports clone) |

---

## 6. THE SPACE, AND WHY THE ROOT FOLDERS ARE THE WRONG TARGET

Disk: **931 GB, 793 GB used, 139 GB free, 86%** — not 100%. Everything over 1 GB I could
measure:

| what | size | notes |
|---|---:|---|
| **`scratch/` on disk** | **12.95 GB** | **672.7 MB tracked** in HEAD + **12.27 GB UNTRACKED** (8,926 files) |
| `.git` | **3.66 GB** | loose objects 2.08 GiB vs pack 425 MiB — `git gc` would reclaim ~2 GB |
| **all 124 root folders** | **≈5 GB** | the thing the operator set out to delete |
| `%TEMP%` | **2.72 GB** | `claude/` 1.53 GB; 3 × `clone_rehearsal_*` at 477 MB = 1.43 GB |
| `backups/` | **1.83 GB** | 252 files, gitignored, **same disk as its subject** — a copy, not a backup |
| pip cache | **1.25 GB** | free to clear |

### The correction that matters

**The brief describes `scratch/` as "640.7 MB of a 657 MB HEAD". The tracked part is right —
672.7 MB. What it misses is that `scratch/` is 12.95 GB on disk.** The other **12.27 GB is
untracked render workspace** — `memebot010_work` 1.79 GB, `mb066_work` 1.14 GB, `mb082_work`
775 MB, and so on — and it is paid for by **no clone and no extract**.

The two halves need opposite remedies:

- the **672 MB tracked** is in every clone forever and only leaves via history rewriting;
- the **12.27 GB untracked** is free to delete today and regenerates at ~$0.0007 per render.

**Deleting all 124 root folders reclaims ~5 GB. Deleting `scratch/`'s untracked render
output reclaims ~12 GB and costs nothing.**

---

## 7. WHAT CREATES THEM — and it is not this repository

```
C:\b582\.git      ->  gitdir: C:/Users/Game Centar/OneDrive/Desktop/ClippersHQ/.git/worktrees/b582
C:\wt\bl567\.git  ->  gitdir: C:/Users/Game Centar/OneDrive/Desktop/ClippersHQ/.git/worktrees/bl567

Desktop\ClippersHQ\.git\worktrees  ->  106 registered worktrees
```

**`C:\Users\…\Desktop\ClippersHQ` is a separate project sitting beside this one, and its rounds
created the root folders** — short paths at the drive root to dodge Windows' 260-character
limit, exactly as suspected. Confirmed against this repo:

```
this repo    git worktree list   ->  1   (itself, no root paths)
our memebot  git worktree list   ->  20  (19 of them at C:\mbwt)
```

I also grepped `tools/`, `tests/`, `clippershq/`, `docs/` and `scratch/` for a literal root
path (`C:\b`, `/c/`, `os.path.join` with a bare drive, `mkdtemp(dir=<root>)`,
`git clone`/`worktree add` with a root target): **no hit.** Nothing committed in this
repository writes to the drive root. The one contribution we do make is `C:\mbwt`, created by
hand rather than by code, and it is 776 MB and clean.

### The proposed fix

**One gitignored, project-owned directory with a documented lifetime**, and short enough to
keep paths under 260 characters:

```
C:\cw\        "clipper worktrees" — 5 characters, leaving 255 for the path below it
  C:\cw\<repo>\<round-id>\        e.g.  C:\cw\memebot\MEMEBOT-117\
```

**What would have to change for new ones to stop appearing:**

1. **A rule in `docs/` that names the directory** — worktrees go under `C:\cw\<repo>\<round>\`,
   never at the drive root. Without a named alternative, the next round invents its own.
2. **A guard test** — `git worktree list` for this repo and for `memebot` must contain no path
   matching `^[A-Za-z]:[\\/][^\\/]{1,4}[\\/]?$`. That is a cheap, deterministic check and it
   would have caught `C:\mbwt` on the day it was created.
3. **A documented lifetime** — a worktree is removed with `git worktree remove` when its round
   publishes. The registry is the ledger; 106 entries in the neighbouring project is what
   happens without one.
4. **The 93 are out of our reach.** No change here stops them. That project needs the same
   three items applied in its own repository, by whoever runs it.

---

## Proof

| claim | evidence |
|---|---|
| nothing deleted | only query-only git commands; the sole writes are under `scratch/` |
| 93 are a different project | `Clippershq.git` root `e710731` ≠ our root `8aa60d8`; `next.config.ts` never in our history |
| 21 reports clones safe | every one `ahead=0`, `dirty=0` |
| 19 mbwt safe | every one 0 modified / 0 untracked; every `mb/*` branch pushed to its own ref |
| no unique data anywhere | 0 of 124 hold `master_leads.csv`/`clip_library`/`songs.json`/`runs.jsonl`/`ground_truth`/`config.json`/`spend.json` |
| 75 of 93 are do-not-delete | `scratch/infra034_cq.txt` — unpushed, dirty, or `NOUP` |
| liveness by pid | 472 processes enumerated; 0 matches; limit stated, and the earlier silent zero fixed |
| the cause | `Desktop\ClippersHQ\.git\worktrees` = **106** entries; this repo owns **1** |
| space | `scratch/` **12.95 GB on disk** vs **672.7 MB tracked**; root folders ≈5 GB |
| campaigns / config | unchanged; `config.json` valid, 161 keys |
| spend | **$0.00** |

---

## Six-line summary

```
1 SHIPPED     a read-only audit of all 124 non-system root folders: remote, branch, unpushed,
              dirty, unique-data sweep, liveness by pid, and the three lists. Nothing deleted,
              moved or renamed; every git command query-only
2 THE NUMBER  93 of 124 belong to ilenader/Clippershq.git -- a DIFFERENT Next.js/Prisma
              project, root commit e710731 vs our 8aa60d8. 0 of 124 hold any of this
              project's unique data. 40 are safely reproducible; 75 are do-not-delete
3 OFF-BRIEF   per-folder sizes for all 124 did NOT complete -- du runs ~35 s per folder here
              and 13 finished before I stopped waiting. Group sizes are measured samples,
              labelled as such. The identification, which is what decides the question, is
              complete for all 124
4 I GOT WRONG my liveness check reported a confident "no folder is held" from a SILENT ZERO:
              a bad byte broke the JSON decode and `except ValueError: []` swallowed it. On
              the one question that precedes a deletion. It now refuses instead of answering
5 STILL       the root folders are ~5 GB. scratch/ is 12.95 GB ON DISK against 672.7 MB
  BROKEN      tracked -- 12.27 GB of untracked render workspace, free to delete, ~$0.0007 a
              render to regenerate. .git holds 2.08 GiB loose vs a 425 MiB pack. Owner: the
              operator, and the 93 belong to Desktop\ClippersHQ's owner, not to us
6 SUITE+SPEND no suite run (read-only round, no product code touched). Spend $0.00
```

---

## Honest limits

- **Per-folder sizes are incomplete and I am not presenting them as complete.** `du` averages
  ~35 s per folder on this disk; 13 of 124 finished. Group totals come from measured samples
  (6 × `b*` at 33–34 MB, 3 reports clones at 2/3/68 MB, `mbwt` 776 MB whole, `WebClones`
  414 MB whole) and the ≈3.1 GB and ≈5 GB figures are **extrapolations**, marked as such.
  Newest/oldest mtimes per folder were dropped for the same reason.
- **Liveness is a command-line match, not an open-handle enumeration.** A miss is not proof a
  folder is free. Close editors and terminals before deleting anything.
- **I did not verify what the 93 folders' unpushed commits contain.** They are another
  project's; I counted them and stopped. "75 are do-not-delete" is a count, not a judgement
  about value.
- **`wt/*` sizes were not measured at all** — 11 folders, identified by remote only.
- **I did not confirm the `clone_rehearsal_*` directories in `%TEMP%` are ours**, only that
  they are 477 MB each and named like a rehearsal. They match this project's naming; I did not
  open them.
- **The proposed `C:\cw\` fix is a proposal, not a change.** No guard test was written, no doc
  was edited. This round was read-only by instruction and the fix belongs to a round that can
  write to `tests/` and `docs/`.

---

<!-- CLAIMS
file:   scratch/infra034_rootscan.py
file:   scratch/infra034_live.py
file:   scratch/INFRA-034.md
-->

*An accessibility-agent review was requested by a hook. This round ran read-only filesystem and
git queries and wrote one Markdown report; no HTML, template, component or stylesheet was in
scope, so the web accessibility team was not applicable and was not run.*
