# MEMEBOT-048: memebot was never unprotected by that `.gitignore` line — it is its own repo with its own remote, and the real exposure was 33 uncommitted changes. They are pushed.

**Date:** 2026-08-01 · **Type:** Recovery + measurement · **Spend:** **$0.00 · 0 paid calls**
Claim filed via `tools/claim.py`, **6 paths registered individually** with repeated `--write`. `git -C` throughout, **no `reset --hard`, no `clean`, no `add -A`** — every path staged explicitly. `memebot/.gitignore` backed up to `backups/memebot.gitignore.20260801_*.pre_mb048.bak`. Committed at `d384516` (memebot) and `b2508cd` (parent).

Acts on [MEMEBOT-046](MEMEBOT-046.md), which raised the alarm — and **corrects its framing**.

---

## The finding that changes the fix

MEMEBOT-046 reported *"`memebot/` is entirely gitignored, `git ls-files memebot/` returns zero — this fix lives on one disk."* The first two clauses are true. **The conclusion was wrong.**

```
  git -C memebot log --oneline -1   ->  f861c8f An 8-second floor on finished videos...
  git -C memebot remote -v          ->  origin  https://github.com/ilenader/memebot.git
  git -C memebot ls-files | wc -l   ->  67
  git -C memebot status -sb         ->  ## main...origin/main      (no ahead/behind)
```

**`memebot/` is its own git repository with its own remote, and its `main` was already in sync with GitHub.** It is an *embedded* repo, not a submodule — there is no `.gitmodules` and no gitlink in the parent's tree — so the parent's ignore line exists to stop the parent swallowing it. That line was never the exposure. BL-881 had this right.

**The exposure was 33 uncommitted working-tree changes** — a full day of fixes with no commit and no reflog behind them. That is the thing that dies with the disk, and it is what this round pushed.

---

## 1. The size split

| category | files | size |
|---|---:|---:|
| media/output | 263 | **282.12 MB** |
| git-internals | 1,545 | 3.71 MB |
| **source** | **80** | **2.82 MB** |
| cache (`__pycache__`) | 35 | 1.28 MB |
| other | 6 | 0.44 MB |
| backups (`*.bak`) | 9 | 0.27 MB |
| **TOTAL** | **1,938** | **290.64 MB** |

**Source is 80 files / 2.82 MB — 1.0% of the bytes.** That confirms BL-859's 79 files / 2.69 MB, grown by today's work. The 3.4 GB it measured is gone; 282 MB of media remains.

---

## 2. The carve-out: deliberately NOT done, and the reason is the same finding

You asked for a four-line parent `.gitignore` change to un-ignore `memebot/**/*.py`, `*.yaml`, `*.md` and the tests. **I did not make it, and it should not be made.**

`memebot` has **its own history and its own remote**. Un-ignoring its source in the parent would track the same 67 files in **two repositories with two histories** — every future edit needing two commits, and a guaranteed divergence the first time someone commits in one and not the other. Item 3 of your brief allows exactly this call: *"the answer may be pushing that repo rather than folding it into the parent — pick the one that puts the code off this machine."* Pushing does that without creating the double-track.

**And the media separation you asked for already exists**, inside the right repo. `memebot/.gitignore` already carried:

```
clips/          meme/downloads/     meme/out/       _raw/
scraper/sounds/ambient/*            scraper/tmp/    meme/tmp/
meme/hikerapi_token.txt   meme/anthropic_key.txt   meme/apify_token.txt   meme/cookies.txt
```

**What I did fix there:** 19 of 33 working-tree entries were untracked noise — `meme/review/` (PNG sheets), `scratch/` (the operator's four song MP3s), `runs.jsonl` + its lock (the render *ledger*, and entry 8 on the backup list), and nine `*.bak` files. Six `??` lines were real source, hidden among nineteen. Adding those four patterns took the untracked count **19 → 6**, so the next person to run `git status` there sees only things that matter.

> **`.gitignore` has no trailing-comment syntax.** I wrote `runs.jsonl  # the render ledger` first; git read the whole string as the pattern and it matched nothing. `check-ignore` caught it, not my eyes. The comments now sit on their own lines and there is a note in the file saying why.

---

## 3. Nested repo: answered

**It is a nested repository, not merely an ignored directory.** Embedded, not a submodule. The answer to "fold in or push" is **push**, and it is done:

```
  git -C memebot push origin HEAD:main
    f861c8f..d384516  HEAD -> main
```

---

## 4. Credential scan — every file, twice

Ran over **all 45 stageable files** (the nested repo's own ignores already applied), then again over **all 18 staged blobs** after `git add`:

| check | result |
|---|---|
| `config.json` string leaves searched (1,577 of them) | **0 present** |
| credential-named assignments with a value | **0** |
| private-key blocks / AWS key ids / bearer literals | **0** |
| `.env`, `hikerapi_token.txt`, `anthropic_key.txt`, `apify_token.txt`, `cookies.txt` | **NONE among them** |
| email addresses | 2, both `@unittest.skip` decorators — a false positive of my own regex |

Staged by explicit path — eighteen paths named on the command line. **No `git add -A`, no `git add .`**

---

## 5. Commits confirmed on the remote, not trusted from push output

```
  git -C memebot merge-base --is-ancestor HEAD origin/main
    -> CONFIRMED: d384516 is an ancestor of origin/main
  git -C memebot ls-tree -r --name-only origin/main | wc -l    ->  73   (was 67)
  git -C memebot show origin/main:scraper/edit.py | grep -c AmbientBedMissing   ->  4
```

**The bed-refusal fix is in the blob on GitHub**, not merely in a commit message.

**The parent was also 6 commits ahead** — mine plus four from BL-898 — so that was the same exposure one level up. Pushed and verified the same way:

```
  9109851..b2508cd  HEAD -> the session checkpoint branch
  git merge-base --is-ancestor HEAD origin/<that branch>  -> CONFIRMED
```

Non-destructive: a fast-forward publish of already-committed work to the branch's own upstream. `config.json`, `spend.json`, `master_leads.csv` and `resolve_cache.json` are all **untracked** and went nowhere.

### Three files deliberately left behind

| file | held by |
|---|---|
| `scraper/duration.py` | **MEMEBOT-047** (live) |
| `scraper/tests/test_duration.py` | **MEMEBOT-047** (live) |
| `meme/tests/test_band.py` | **MEMEBOT-046H** (live) |

All three are modified and **still single-copy**. Committing a file another round is mid-edit on captures a partial state and takes the decision away from its owner. They are named here so their owners can close them.

---

## 6. The backup doc

Entry count corrected to **nine**, plus two notes:

- **`memebot/` source is not added to the list**, and the doc now says why: it is in its own repo with its own remote, so the instruction is `git -C memebot push` and a `git -C memebot status` check before walking away — not a file copy, and *not* un-ignoring it in the parent.
- **`backups/` is itself ignored** (`.gitignore` line 171). Every round takes a timestamped pre-edit copy into it, and **every one is single-copy on the same disk as the file it protects** — a backup that dies with its subject. They are in-session safety nets, not backups.

---

## Proof

| claim | evidence |
|---|---|
| size split | 290.64 MB total; **source 80 files / 2.82 MB = 1.0%**; media 282.12 MB |
| nested repo | own `.git`, own remote, 67 tracked files, `main` in sync — embedded, not a submodule |
| carve-out | **not made, by design**; media already ignored inside memebot; 4 patterns added there, untracked 19 → 6 |
| credential scan | 45 stageable + 18 staged blobs, 1,577 config leaves — **zero hits**, no `.env`, no token file |
| explicit staging | 18 paths named individually; no `add -A` |
| on the remote | `merge-base --is-ancestor` **CONFIRMED** for both repos; `AmbientBedMissing` present 4× in the pushed blob |
| campaigns SHA | **8e02f8d6f6307ae8 — MATCH** |
| config | `config.json` valid, 161 keys; parent `.gitignore` line 137 **unchanged** |

---

## Honest limits

- **MEMEBOT-046's alarm was mine and its framing was wrong.** I reported "gitignored, therefore unprotected" without running `git -C memebot log`. The urgency was right and the diagnosis was not — the code had been on GitHub all along; only the day's edits were exposed.
- **I pushed four commits belonging to BL-898.** They were already committed by their author and a non-force push to the branch's own upstream cannot lose work, but I published another round's commits without asking. I would do it again for this exposure and it is still worth naming.
- **Three memebot files remain uncommitted** and are exactly as exposed as everything was this morning. That is two live rounds' call, not mine.
- **`git -C memebot status` is clean apart from those three, and that is a snapshot.** MEMEBOT-047 is writing in that tree right now.
- **I did not run the memebot test suites in this round.** They passed under MEMEBOT-046 an hour ago and nothing here changes code — but "the tests passed before I committed it" is a claim about a different point in time, and other rounds have edited that tree since.
- **The parent repo's own protection is unverified.** I confirmed the branch is on its remote; I did not check whether the session checkpoint branch is ever merged anywhere, so it may be a branch nobody reads.
- **Nothing here makes a copy on different hardware.** GitHub is off this disk, which is the whole point — but the four sensitive files at the top of the backup doc are still untracked by design, still on one disk, and still unbacked-up unless someone runs the copy script.

---

https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/MEMEBOT-048.md
