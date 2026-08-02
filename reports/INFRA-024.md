# INFRA-024 — the first day, from a clean clone

**One number: of twelve first-day steps walked inside a `git archive` extract of both repos,
ONE now fails from a clone that works here.** It was two when the round started.

The deliverable is the difference between this machine and a clone, so the walk was done in
an extract of HEAD rather than reasoned about. Everything below is what that produced.

---

## 1. THE WALK — 12 steps in an extract of HEAD of both repos

`scratch/infra024_firstday.py`. Both repos extracted with `git archive HEAD` (3,639 files,
79 in `memebot/`, which must be nested because its own tests hardcode
`memebot/scraper/config.yaml`). Every step classified `WORKS` / `FAILS-IN-CLONE` /
`BLOCKED` / `SKIPPED`.

| # | step | verdict |
|---|---|---|
| 0 | extract produced a tree | OK — 3,639 files |
| 1 | `send_identity.json` from its example | OK — 7 fields |
| 2 | `message_template` loads the identity | OK |
| 3 | `--strict` gate NAMES the unfilled fields | OK — `['SENDER_NAME', 'REPLY_TO', 'RATE']` |
| 4 | send gate imports | OK |
| 5 | dashboard imports | OK — 20 routes |
| 6 | `memebot/scraper/edit.py` runs | OK |
| 7 | a missing font REFUSES BY NAME | OK — `FACE=Montserrat TOFU='ש'` |
| 8 | `clip_render --cap 0.001` binds | **BLOCKED** — see below |
| 9 | and it spent nothing | OK — `$0.0000` |
| 10 | `outcome_loop export` | OK |
| 11 | `core.hooksPath` set in a clone | **FAILS** — `core.hooksPath=''` |

**Step 8 is BLOCKED, not failed, and that distinction is the point of the harness.** The
clone printed `! The clip library at ./clip_library is empty — build it first (menu 'k')`.
`clip_library/` is gitignored DATA; a clone legitimately has none, and the funnel refused
loudly and named the fix. Counting that as a clone defect would have been a false alarm —
an absent input is not a broken build. A step that fails for want of a credential or a
dataset is not scored as a divergence.

### The one real divergence: the guards are inert in every clone

`core.hooksPath` is **local git config**. Every hook script under `tools/githooks/` is
versioned and travels with the repository; the single setting that points git at them lives
in `.git/config`, which no clone copies. So in a fresh clone the commit-msg guard, the
manifest guard and the secret scan are all **INERT, and nothing says so**. Commits simply go
through unchecked.

That is the same shape as the missing font: correct on this machine, absent in every clone,
silent about it.

---

## 2. FIXED AT CAUSE

### `tools/repo_guard.py check-hooks` — new, and in `preflight`

The tool that *installs* the hooks never checked whether they were installed. It does now,
and it refuses in three distinct ways rather than one:

- unset → *"every commit guard is INERT … Fix: `python tools/repo_guard.py --install-hooks`"*
- set somewhere else → *"the guards in this tree are not the ones running"*
- set correctly but the scripts absent → named

### The font — INFRA-023's, and I verified it rather than claiming it

INFRA-023 was four minutes old and claimed `memebot/scraper/fonts/Inter-Bold.ttf` with item 2
as its stated intent, so I stood off it. **It took the loud-refusal branch, not the commit
branch**: `memebot/.gitignore` still carries `scraper/fonts/*.ttf`, and `face_cannot_draw`
now detects the fallback face boxing a caption.

I re-pointed my own step 7 at the property that fix actually promises. Running it in the
clone: `FACE=Montserrat TOFU='ש'` — the clone has no Inter, falls back to Montserrat, and
the boxing **is caught** instead of shipping a video with a line of boxes where the caption
was. The licence question did not arise, because the font was not committed.

### The gate that should have caught eight untracked modules

`check-untracked` decided "load-bearing" from `LOAD_BEARING`, a **hand-written list of nine
paths**. Measured: it printed *"OK: every load-bearing file is tracked"* in a tree where
`clippershq/clip_motion.py` was untracked, on a day with eight untracked-module incidents.
The list was not wrong — it was blind. It can only ever catch a file somebody remembered to
add to it, which is the same defect as a guard that hardcodes the vocabulary it checks.

It now also derives the set **by import-reachability**: any untracked module that tracked
code imports, exempting paths a live claim declares (the `test_tools_tracked.py`
distinction — a gate that is red whenever anyone is mid-write gets ignored).

`tests/test_repo_guard_coverage.py`, 11 tests on a throwaway `git init` tree, **both
directions on every check**: a clean tree reports nothing, a planted orphan is found *and
its importer named*, a live claim exempts it, committing it clears it, a crashed git raises
rather than returning an empty list that reads as clean.

---

## 3. THE UNTRACKED TRIAGE — 4,529 files, by kind

`scratch/infra024_triage.py`. Not "how many are untracked" (the number is useless) but
**which would a clone miss**:

| kind | before | after |
|---|---|---|
| SHIPPING | 18 | **8** |
| GENERATED DATA | 8 | 0 |
| SCRATCH | 4,543 | 4,521 |

All 8 remaining are held by a live round (`BL-899`, `BL-1022`, `BL-1023`, `INFRA-025`) or by
me. **Nothing ownerless is left untracked.** The generated-data column reached zero without
my help — BL-1023 committed `outputs_for_operator/` at `222aa58` while this round ran.

### Rescued: 18 files, 11 commits, 7 author rounds, none split across owners

`MEMEBOT-066` (4 files), `MEMEBOT-077` (7+manifest), `MEMEBOT-078` (6+manifest), `BL-919`,
`BL-999`, `MEMEBOT-063`, `BL-962` (2). Every commit carries `Claim-Override:` naming its
author, all of which are finished rounds holding no live claim.

The highest-value one: `scratch/mb066_corr.py` is imported by **eight** tracked verify
harnesses (mb073, mb074, mb074_watch, mb086_watch, mb089, mb094, mb095, mb108). A clone had
eight committed files that could not run at all.

**A manifest is a second authority on what ships.** `scratch/mb066_render.py` is imported by
nothing, so reachability said nothing about it — but `MEMEBOT-066.claims` declares it
`file:`, which is an author stating outright that it is load-bearing. The pre-commit hook is
what surfaced it, by refusing the manifest until all eight of its claims held. Correct
refusal, and the reason each round needed two commits: **the manifest waits for the code,
never the reverse.**

`MEMEBOT-078.claims` also settled an ownership question: `tests/test_variant_preconditions.py`
attributes itself to MEMEBOT-077 in its docstring, but 078's manifest claims it. The manifest
is the authority — a docstring names the round that prompted work, the manifest names the
round accountable for it — so it landed with 078 and was not split.

### backups/ is not disaster recovery

`backups/` holds 252 files, **inside the working tree, on the same disk, under the same
OneDrive folder as the thing it backs up**. Every event that takes the subject — a
`git clean -fd`, a disk failure, a bad sync, an `rm -rf` one directory too high — takes the
backup in the same instant. That is a copy, not a backup, and it is worth saying because a
directory named `backups/` reads as protection it does not provide. The three
remote-tracking refs are the only off-machine copy, which is why *"is it tracked"* is the
question this triage sorts by.

---

## 4. THE LINE DRIFT, AND A TEST SO IT CANNOT ROT AGAIN

`docs/SEND_DAY.md` cited `clippershq/message_template.py:675` for `OPERATOR_FIELDS`, which is
at **677**. Two lines — harmless that morning, and exactly how a runbook becomes confidently
wrong: written once against a tree that then moves under it, and nothing ever re-reads it.

Fixed, and made standing. `tests/test_doc_citations.py`, 12 tests. The convention the docs
already used is now load-bearing:

> The list lives at `clippershq/message_template.py:677` (`OPERATOR_FIELDS`).

A citation resolves when the **anchor** actually appears at that line. A bare `foo.py:123`
asserts nothing a test can confirm and is refused. **When it fails it computes the answer** —
*"the anchor is at line 677 in HEAD"* — because a guard that says "wrong" without saying
"should be 677" gets postponed.

**It caught real drift within the hour.** A live round committed `clippershq/outcome_loop.py`
while this round was still running, moving `def main(` from 665 to **905**.
`docs/FINAL_STATE.md` cited 665 in two places, both now wrong in HEAD *and* on disk, so the
two-tree rule correctly stopped excusing it and the suite went red. That is the test doing
exactly the job it was written for, sixty minutes after being written. Both citations
corrected.

But **the number it computed was wrong**, which is a worse failure than not computing one.
`find_anchor_line` searched by substring, so asked where `main` had gone it answered line 69 —
a list entry reading `"main",` — when the definition was at 905. A failure message that
computes a fix is only worth having if the fix is right; a confidently wrong one gets pasted
into the doc. A *definition* now wins, a bare mention is the fallback, and the fallback
matches on a word boundary so `main` never matches `domain` or `remaining`.

Two design decisions worth stating:

- **It reads HEAD *and* disk.** Reading only the working tree made it red because another
  round had `outcome_loop.py` mid-edit, which had pushed `main` down the file — the doc's
  owner could not have fixed that, and the only way to green it would have been to cite a
  line that is *wrong at HEAD*. Reading only HEAD breaks a round landing a module and its doc
  in one commit. A citation resolves in **either** tree; genuine rot means the anchor is at
  that line in neither, and the test still fires.
- **A baseline, not an exemption list.** `docs/CLIENT_DECISIONS.md` (BL-1010) and
  `docs/RUNBOOK.md` (BL-1000) are held by live rounds. Their unanchored citations are a
  COUNT that may not grow; adding one anywhere turns this red, and the doc's owner is the one
  who anchors it.

---

## 5. THE CLONE REHEARSAL, RE-RUN

`tests/test_clone_rehearsal.py` — **9/9**. Hooks inert before the installer, firing after it,
a **legal commit ACCEPTED**, and each refusal attributed to its own check's marker. The legal
case is the one that matters: without it, a guard that refuses everything passes a
refusal-only test.

---

## 6. ONE RED I DID NOT CAUSE, FIXED BECAUSE "SUITES GREEN" IS A DELIVERABLE

`tests/test_claim.py` was red before this round touched anything, for a reason that gets
worse with time: its fixtures borrow **real round ids** (`BL-901`, `BL-903`, `BL-910`…), and
`check_id_free` refuses an id that already has a published report. Every id those fixtures
borrow eventually becomes somebody's report, so the test was **scheduled** to fail.

The registry is what that test is about; the published-report namespace is a separate concern
it should not depend on. `start()` calls now pass `check_reports=False`, CLI calls pass
`--no-reports-check`, and the one `claim()` call the flag does not reach uses a suffixed id —
the convention the file already had at `BL-914-rt`. No coverage lost: nothing in it asserts
anything about `check_id_free`.

**It needed two `Claim-Override`s, not one.** `commit_guard` reads the committing round from
the **subject line**, so a commit whose subject attributes work to `BL-914` treats
INFRA-024's own claim on the file as *foreign* and refuses. Correct behaviour — the round in
the subject is the one being held accountable — but worth knowing before it refuses you.

---

## WHAT I GOT WRONG

Nine, all self-caught, several of the same family — **an assertion that looked right and
measured something else**.

1. **The regex was corrupted by the shell, not by logic.** `BARE_ANCHOR` matched nothing.
   `repr()` gave `'\x08([A-Za-z_][A-Za-z0-9_]{2,})\x08'` — the `\b` word boundaries I wrote
   through a bash heredoc landed in the file as literal **backspace bytes**, so the pattern
   required a backspace on either side. Fixed by stripping the bytes and never writing a
   regex through a heredoc again.
2. **I guessed an API instead of reading it.** `Operator.unfilled` does not exist; `unfilled`
   is a module function over rendered text and `Operator.value(field)` is the accessor. I
   scored the resulting `AttributeError` as a clone defect until I read the source.
3. **Prose words passed as anchors.** The bare-anchor fallback, meant for fenced tables,
   accepted `This`/`loop`/`that` for `outcome_loop.py:665` — any of which could land on the
   target line by chance and green a citation nobody checked. Now fence-scoped.
4. **20 false positives from a name match.** The triage called
   `scratch/mb089_head/clippershq/clip_library.py` and nineteen like it shipping. Tracked
   code does import `clip_library` — it resolves to the *tracked* module, never to another
   round's `git archive` extract. Committing them would have duplicated the package into
   `scratch/` on the strength of a filename.
5. **Then five more, one repo boundary out.** `scratch/mb099_extract/scraper/*.py` survived
   the fix above because `git ls-files` in the parent cannot see memebot — a nested repo. The
   tracked-name set has to span both repos.
6. **`.claims` manifests were misclassified as scratch** for three runs: neither `.py` nor a
   data extension, so they fell through. `verify_claims.py` reads them from HEAD, so an
   untracked manifest is a promise with no object behind it.
7. **`tests/bl932_probe_67vrvaav.py` was called shipping "by location"** — `run_all.py:76`
   collects `test_*.py` only, so nothing runs it. It is a leaked fixture whose entire content
   is an unterminated docstring. Named for its owner, not committed.
8. **I moved a broken edge instead of closing it.** Committing `scratch/bl962_smtp.py`
   because a tracked harness imports it left `scratch/bl962_dns.py`, which *it* imports,
   still untracked — a tracked file that still could not run. Reachability has to be followed
   to a fixed point, not applied once.
9. **My own failure message computed the wrong fix.** `find_anchor_line` matched by
   substring, so it reported `main` at line 69 (`"main",` in a list) rather than the `def` at
   905. The whole argument for computing the answer is that a guard which only says "wrong"
   gets postponed — a guard that says the wrong number is worse, because it gets obeyed.

I also left `docs/claims/MEMEBOT-078.claims` staged `A ` in the **shared index** for about a
minute when a concurrent round took the index lock mid-commit. That is the exact hazard
INFRA-023 reported against `MEMEBOT-094.claims`; I unstaged it before retrying so no other
round's bare commit could sweep it.

---

## STILL BROKEN, AND WHOSE

| what | whose |
|---|---|
| `tools/commit.py` prints `unclaimed : %d path(s)` — the format argument is missing | unowned; cosmetic, in a tool everyone reads |
| `docs/FINAL_STATE.md` §1 still quotes *"159/159 green"* — the runner now discovers **175** suites | mine (BL-1001), but that doc is a snapshot verified against a named sha, so it is not silently edited |
| `tests/bl932_probe_67vrvaav.py` — leaked fixture, unterminated docstring, in `tests/` | BL-932 |
| `backups/` shares a failure domain with its subject | unowned; needs an off-machine target, not a fix here |
| `docs/CLIENT_DECISIONS.md` 6 unanchored citations | BL-1010 (baselined, may not grow) |
| 8 untracked shipping files | BL-899, BL-1022, BL-1023, INFRA-025 — all live, all named |

`core.hooksPath` is now *detected* loudly, not *fixed* — nothing can make git config travel
with a clone. A clone is still unguarded until somebody runs the installer; the change is
that it now says so instead of staying quiet.

---

## VERIFICATION

| | |
|---|---|
| **Suite** | **175/175 green, 5,423 checks** (448 s) — one runner covers both repos; 24 of those suites are `memebot/` |
| **Campaigns** | unchanged — `test_governance_rules.py` 25/25, where rule 3 pins `7a029ee5447cddd8` ≡ `8e02f8d6f6307ae8` as one object under two separators |
| **Config** | valid — 161 keys, `test_config_contract.py` ALL OK |
| **Claims** | `verify_claims.py` — ALL CLAIMS VERIFIED |
| **Backup** | `verify-remote` — 0 local-only commits in either repo, every commit reachable from HEAD is on a remote |
| **Spend** | **$0.00.** Everything here is git, the filesystem and offline Python. The one funnel invocation ran capped at `$0.001` inside the clone and reported `$0.0000`. |

A suite count is a moment, not a property: three rounds were in flight at the time of that
run, and the tree moves under any number quoted from it.
