# INFRA-033 — the index is disarmed, the last stale claim is ended, and HEAD stands alone

**One number: 137 of 137.** Every shipping module in both repos imports from a `git archive`
extract of HEAD alone — **zero clone defects**. That is the check `git status` structurally
cannot perform, and it is the one that says the repository is whole.

Two of the brief's four named items had already been resolved by other rounds. Both are
reported rather than re-done, and I say so up front because acting on a stale table is how a
sweep creates the mess it came to clear.

---

## THE PREMISE, RE-CHECKED BEFORE ANYTHING WAS TOUCHED

| the brief said | measured now |
|---|---|
| `dashboard/server.py` is modified shipping code with **no claim** | **clean**, committed by INFRA-026, and re-claimed by **BL-1040** — not an orphan, not mine |
| `tests/test_clip_pipeline_gate.py` untracked, claimant departed | **already committed** by BL-1028 at `bda25e3` |
| **eight** paths staged by ended rounds | **thirteen**, and two more appeared mid-round |
| MEMEBOT-039, the last stale claim | still live at **39.6 h** — real, and now ended |

BL-1026's table was accurate when written. Sixteen rounds were in flight while this ran.

---

## 1. THE ARMED INDEX — 15 paths, all committed, none unstaged

Thirteen paths sat staged in the **shared** index, owned by three rounds — **BL-1002,
BL-1002b and MEMEBOT-115 — all ended, all with published reports**. Nobody was ever going to
claim them, so the index would have stayed armed indefinitely and any bare `git commit` among
sixteen live rounds would have swept them into someone else's commit under someone else's
name. That is the `b6abeee` / BL-961 race.

**Why touching another round's staged files is correct here, stated explicitly:** the normal
rule is to stand off, because the owner will come back and finish. These owners are *gone* —
claim ended, report published. Standing off a departed round is not deference, it is leaving
a loaded trap for whoever commits next.

Every one was **committed verbatim, never edited**, and every one was checked first: index
and worktree agreed on all 15, all `.py` parse, all `.json` parse, the `.jsonl` parses per
line. **None needed unstaging**, because unstaging is the disposition for a *partial* change
and there wasn't one.

| group | paths | disposition |
|---|---:|---|
| BL-1002b (7) | report + 6 harness/data files | **committed**, `Claim-Override: BL-1002 BL-1002b` |
| MEMEBOT-115 (5 code) | report + render harness + 3 data | **committed**, code first |
| MEMEBOT-115 (manifest) | `docs/claims/MEMEBOT-115.claims` | **committed second** — a manifest waits for its code |
| BL-1031 (1) | its report | **committed** |
| INFRA-031 (1) | its incident note | **committed** |

**Two overrides, not one, for BL-1002b.** The files' docstrings say `BL-1002` and
`tools/commit.py` resolves the `scratch/bl1002_*` namespace to `BL-1002` — but the round that
wrote them **publishes as BL-1002b**: it registered the `BL-1002` id before noticing a
completed matcher audit already held it, and its own report opens with that note. Both ids
are acknowledged so neither attribution is lost. `scratch/bl1002_dist.json` at HEAD belongs
to the *other* BL-1002 and was left alone.

### The hazard regenerates

`scratch/BL-1031.md` and `scratch/INFRA-031-INCIDENT-for-BL-1027.md` were **not staged when
this round began**. Both rounds ended *during* it — one of them between the orphan sweep and
the liveness check that followed roughly a minute later. **Disarming the index is a snapshot,
not a fix.** In a sixteen-round tree it re-arms continuously, and the only durable answer is
a release path that cannot leave staged work behind.

---

## 2. MEMEBOT-039 — ended, but only after its seven orphans landed

Age **2,374 min (39.6 h)**, far past the 480-minute takeable threshold. The other condition
did **not** hold: its declared paths were untracked. Ending it there would have deleted the
only record that anyone owned them and left seven orphans — the failure this whole session
has been undoing.

`claim.py end` refuses a dirty release for exactly that reason, and **the right move was to
satisfy the guard, not route around it**. So the files landed first, attributed to
MEMEBOT-039, and the claim ended cleanly after.

**The guard found three files my own triage missed.** I read the claim's `will_write` — four
paths. The guard checks the *namespace*, and named `memebot039_record.jsonl`, then
`memebot039_fields.json` and `memebot039_mkpatch.py`. **A declaration is what a round intended
to write, not what it wrote.** Trusting `will_write` alone would have released the claim and
orphaned three files in the same move.

It reports what is uncommitted *now*, so it surfaces them in batches; enumerating the whole
namespace at once is what finished it. `memebot039_record.jsonl.lock` was deliberately left —
a lock file is transient and gitignored, and leaving it is a disposition, not an omission.

**MEMEBOT-039 was the last claim past the threshold. There are now none.**

---

## 3. THE ORPHAN TRIAGE — and the resolver you must use

**4,340 orphans of 5,098 dirty paths**, and almost all of them are genuine scratch. The
dispositions that mattered:

| disposition | n | what |
|---|---:|---|
| **COMMIT** | 15 | the staged set above, plus MEMEBOT-039's seven |
| **REPORT, not commit** | 4 | below |
| **LEAVE** | the rest | scratch nobody reads, or held by a live round |

### Report, not commit — committing half a change is worse than leaving it

| path | why it is not committed |
|---|---|
| `docs/claims/BL-1013.claims` | **live work, misattributed by both mechanisms.** The namespace resolver says BL-1013 (ended) because the *filename* carries that id; the diff says *"SUPERSEDED BY BL-1036"* and **BL-1036 is live**. It is an undeclared write by a live round — committing it would land in-flight work under a foreign name, the precise race this round exists to prevent. **BL-1036 should declare this path.** |
| `dashboard/static/runs.json` | **+2,695 lines of accumulated run records with no single author.** Generated by many rounds' pipeline runs; attributing a dozen rounds' output to one commit would be a false record, and the content is reproduced by running the pipeline. |
| `names` (repo root), `scratch/mem.out` | **empty stray files**, 0 bytes, owned by nobody. Nothing to commit. |

### The resolver is the load-bearing choice

`claims_read.holders_of` is **exact-path only** — deliberately, because it is the fallback
reader and a second copy of the overlap logic would drift. `claim.rounds_owning` expands a
declared path to a **prefix glob**. **The two disagree, and I hit it live**: `claims_read`
called seven staged paths `FREE` while `commit.py` refused them as BL-1002's. A triage built
on the exact-path reader would have declared those seven ownerless and been contradicted by
the guard at the moment of commit. **This sweep uses the same resolver the guard uses.**

And `rounds_owning` resolves by **namespace, not liveness** — which is why the final table
carries an *effective* column. Reading "BL-1013" as "someone is on it" is exactly the mistake
that leaves work sitting for a day.

---

## 4. DOES HEAD STAND ALONE? — 137 / 137

`git status` compares the **worktree** to HEAD. A module that is untracked but present on
disk is invisible to that comparison, because *both sides have the file*. That is how three
tools were found untracked while working perfectly, and eight untracked shipping modules
turned up in one session. The only instrument that can see it is a tree built from HEAD alone.

| | |
|---|---:|
| Modules extracted and imported (both repos, memebot nested) | **137** |
| Imported OK | **137** |
| **Missing from HEAD (clone defect)** | **0** |
| Failed for another reason (not a clone defect) | 0 |

A missing module is a clone defect; a module that raises because a config, key or dataset is
absent has imported fine and is failing for a reason a clone legitimately has. The two are
separated by exception type so the distinction is visible rather than asserted.

---

## 5. THE STATE TABLE — what the next session opens with

Taken **2026-08-03 12:43**. A count is a moment, not a property.

### Staged in the shared index

**NONE. The index is disarmed.**

### Live claims (9) — none past the 480-minute threshold

| round | age | paths |
|---|---:|---:|
| MEMEBOT-117 | 63 min | 8 |
| BL-1035 | 57 min | 10 |
| BL-1036 | 50 min | 12 |
| BL-1039 | 41 min | 11 |
| BL-1038 | 40 min | 9 |
| BL-1041 | 39 min | 18 |
| BL-1042 | 38 min | 22 |
| BL-1043 | 37 min | 8 |
| INFRA-033 | 36 min | 10 |

### Untracked shipping files (5) — every one held by a live round

`docs/claims/BL-1039.claims` (BL-1039) · `docs/claims/MEMEBOT-117.claims` (MEMEBOT-117) ·
`tests/test_decision_log_redaction.py` (BL-1038) · `tools/backup_schedule.ps1` (BL-1035) ·
`tools/bootstrap.py` (BL-1043)

**No untracked shipping file is orphaned.**

### Dirty outside `scratch/` (20) — 18 held, 2 orphaned

18 belong to live rounds (BL-1035/1036/1038/1041/1042/1043). The two orphans are
`dashboard/static/runs.json` and `docs/claims/BL-1013.claims`, both reported above with the
reason they are not committed.

---

## WHAT I GOT WRONG

Three, all caught before they reached a commit, and all the same species — **a rule that
looked principled and misclassified correct files.**

1. **I flagged 14 files as "not whole" and 13 were correct.** My coherence check treated any
   empty file as partial. Thirteen were `__init__.py` and `.gitkeep` inside other rounds'
   `git archive` extracts — **empty by convention**, and wrong if they weren't. A rule that
   flags a correct file is a rule that gets ignored.
2. **I reported three clone defects that do not exist.** The import check put each module's
   *own* directory on `sys.path`, because `clippershq/` imports its neighbours flat. But
   `memebot/meme/` is a real package importing `from meme.text import ...`, so it needs the
   package's **parent**. Three modules came back `No module named 'meme'` — my harness's
   convention, not HEAD's defect. Both roots are now supplied and it reads 137/137.
3. **My first state table called live work an orphan.** It printed the namespace owner as the
   holder, so `docs/claims/BL-1013.claims` read as held by BL-1013 — a round that has ended —
   when BL-1036 is live and actively writing it. Had I trusted that column I would have
   committed a live round's in-flight file under a departed round's name.

---

## STILL BROKEN, AND WHOSE

| what | whose |
|---|---|
| **THE DISK IS 100% FULL** — 1.2 GB free of 931 GB. The suite cannot complete and extract-based guards fail on `tar`. **768 harness temp dirs older than 2 h are provably dead** (oldest live claim ≈ 1 h) | unowned, and the top item for the next session |
| **`scratch/` is 640.7 MB of a 657 MB HEAD** — 286 MB `.m4a`, 192 MB `.mp4`, 87 MB `.png`. Every clone pays it; every extract writes it | unowned; needs a policy on tracking media |
| **The armed-index hazard regenerates** — two paths re-armed *during* this round, one between two checks a minute apart | open. Disarming is a snapshot; the fix is a release path that cannot leave staged work behind |
| `docs/claims/BL-1013.claims` written by BL-1036 **undeclared** | **BL-1036** — and it has since landed the file itself at `f9db039`, which is the confirmation that declining to commit it was right |
| `dashboard/static/runs.json` — generated data, many authors, no attributable owner | open; needs a policy (regenerate, or gitignore), not a commit |
| `names`, `scratch/mem.out` — empty strays at 0 bytes | unowned litter |
| `claims_read.holders_of` and `claim.rounds_owning` give different answers | by design, and correctly so — but it is a trap for any round that picks the wrong one |

---

## 6. THE DISK IS FULL, AND IT IS WHY THE SUITE CANNOT BE PROVEN GREEN

I could not obtain a full-suite run. Four attempts: one completed in an earlier round at
1,579 s, three stalled after printing their header and were killed (checking first that no
`bl932_probe_` file was planted — killing mid-probe is what leaves a permanent red). I chased
that as CPU contention. It is not.

```
C:  931G  930G  1.2G  100% /c        <- 1.2 GB free
```

`tests/test_tools_tracked.py` fails with `tar -xf ... exit 1`, and run by hand the tar says
**`No space left on device`**. That is not a repository defect and not an untracked-file
finding — it is the machine. The same check in `infra033_imports.py` passes 137/137 because
it uses `shutil.unpack_archive` and cleans up in a `finally`.

**Two compounding causes, both measurable:**

| | |
|---|---:|
| Harness temp directories left in `%TEMP%` | **3,801** |
| …older than 2 h, i.e. from rounds that have ended (oldest live claim ≈ 1 h) | **768** |
| `git archive HEAD` of the parent repo | **657 MB** |
| …of which `scratch/` | **640.7 MB (97.5%)** |

`scratch/` holds **286 MB of `.m4a`, 192 MB of `.mp4`, 87 MB of `.png`, 36 MB of `.jpg`** at
HEAD. Every clone downloads it, every `git archive` extract writes it, and there are dozens
of those extracts per session — which is how 931 GB filled.

**I did not delete anything.** The 768 dead temp directories are provably safe to remove (no
live claim is older than an hour) and removing them is the fastest way to give the machine
room back — but they are another process's files, deleting is not reversible, and it is
outside what this brief asked for. It is recorded here with the exact safe predicate so the
operator or a briefed round can act on it deliberately.

---

## VERIFICATION

| | |
|---|---|
| **Suite** | **NOT PROVEN.** Three of four full runs stalled on a disk with 1.2 GB free; see §6. The claim/commit suites this round could affect were run individually: `test_verify_claims`, `test_staged_cross_round`, `test_commit_guard`, `test_claim`, `test_governance_rules`, `test_suites_parse` — **all green**. `test_tools_tracked` errors on `tar`, from the full disk, not from this round. **This round edited no file**, so its blast radius on the suite is zero: every commit is content that was already on disk. |
| **Clean-extract import** | **137 / 137**, both repos, memebot nested — 0 clone defects |
| **Staged in the shared index** | **0** |
| **Claims past 480 min** | **0** (MEMEBOT-039 was the last, and is ended) |
| **Campaigns** | unchanged — `test_governance_rules.py` 25/25, where rule 3 pins `7a029ee5447cddd8` ≡ `8e02f8d6f6307ae8` |
| **Config** | valid |
| **Spend** | **$0.00** — no paid calls. Every check is git, the filesystem and offline Python. |
| **Files edited** | **none** — every commit is verbatim |
