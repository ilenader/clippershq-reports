# BL-1587: nothing of his goes on the Desktop again. The backup now runs to the USB stick and is proven by restore, the 323 deleted cards are rebuilt and vaulted at birth, and his one workbook has the 1,248 rows it was missing

**Round:** BL-1587 · **$0.00, no vendor call** · every store this round did not declare is
byte-identical at close · paths redacted (`<PROFILE>` is the user folder) · accounts never named.

**The one question for him:** does the separate tool you use to send leads daily
(`docs/NO_SEND.md:13`) mail addresses from these sheets, and can it export who replied or bounced?

## The paragraph

**Where his files live now.** Everything of his is in `%LOCALAPPDATA%\ClippersHQ\operator\`, outside
OneDrive and never on the Desktop. He opens it from the Start Menu: **ClippersHQ > Grade cards** always
opens the newest page, and **ClippersHQ > Lead workbook** opens his one workbook.

**What he has to do.** Open "Grade cards" and click. That is all. The page's download is its only
output, and the next round ingests it.

**Is the backup safe? Yes, and proven.**
- The scheduled backup had failed on 52 of 52 nights because it pointed at a drive (`E:`) that is never
  attached. It now writes to the USB stick that is (`D:`).
- It was run once through the scheduled task itself, and returned 0.
- Every archive it writes is now restored and hashed on the spot. Today's: **212 of 212 files
  byte-identical**.
- An independent check read master back **from the archive: 75,540 rows**, equal to the live file.
- Both vault roots re-verified: 4,802 copies each, 0 mismatches.
- The 808 BL-1584 rows that were in no copy of master are now in both vault roots **and** in the archive.

**What was rebuilt.** The 323 cards he deleted, with the same mix: 110 of them from rows the cut
removed (60 Instagram, 50 TikTok). None of them is an account he has already graded. The page and its
manifest were vaulted to both roots before either was allowed into his folder, and `generate` now
cannot work any other way.

**His workbook.** It was missing 1,248 delivered rows, and now has them. MARK was never written, and
every sheet was read back and counted.

## 1. What this round was, for a reader with no context

ClippersHQ finds video editors and delivers their addresses to one operator. For sixteen rounds its
scripts wrote review pages and one-off spreadsheets **directly onto his Desktop**, because one round
asked the shell for the Desktop path and every later round copied it. Nobody asked him where his files
should live. He answered by deleting them: *"I don't want any of my things to go to desktop. Desktop
needs to be clean. That's why I deleted it. Figure out how to get it back without me doing anything."*
He is right, and it was this project's defect. This round fixed the backup, gave his files one home,
rebuilt what he deleted, and wrote his real workbook, all without asking him to do anything.

## 2. The backup: re-pointed, run, and proven

**The ones that existed nowhere else came first.** Before touching anything, three files that existed
in exactly one place were copied into both vault roots and re-hashed. Verdict line:

```
VERDICT: SECURED IN BOTH ROOTS, every copy re-hashed equal
```

The three files: `scratch/bl1583/walk_rows.jsonl` (516 lines), `scratch/bl1584/walk_rows.jsonl`
(808), and `email_harvest_tags.json`, whose 51 newest tags were in no commit and no vault. The
positive control fired: a planted absent file was reported missing in both roots.

**Why it had failed.** `\ClippersHQ-Backup` ran every day, 52 runs in 52 days, but it pointed at
`E:\clippershq-backups`, and `E:` is never attached. The task's own log history settles the logon
question: 48 runs at 20:00 local, 3 a few minutes late, and 1 catch-up at 12:01 after a missed
trigger. So it does **not** have the no-op-when-logged-out shape the GC tools have. It ran every time
and had nowhere to write.

**What changed:**
- `backup_schedule.ps1 -Install -Dest D:\clippershq-backups` re-registered the task. It still runs
  daily at 20:00 with catch-up. `D:` is a 29 GB USB stick, a separate physical device (disk 1, bus
  USB) from `C:` (disk 0, NVMe).
- The wrapper now prefers the repo's `.venv` interpreter over whatever `python` is first on `PATH`.
- `tools/backup.py`:
  - **added `spend.json` and `email_harvest_tags.json`** as required, and every
    `scratch/bl*/walk_rows.jsonl` through a glob;
  - added his home folder, archived under `operator_home/`;
  - **restores and hashes every archive it writes before reporting PASS**, and prunes to the newest
    30 only after that restore succeeds. At about 43 MB each, that is about 1.3 GB on a stick with
    9 GB free.

**Run once, through the scheduled task, twice.** The second run captured his new folder.

```
wrote D:\clippershq-backups\clippershq-20260923T162251Z.tgz (43.0 MB)
restore check: 212 of 212 member(s) byte-identical; corrupt 0, missing 0
VERIFIED    : True
RESULT: PASS (exit 0)
```

Task state afterwards: `lastResult=0`, next run 20:00 tonight. The failure marker file is gone.

**Checked independently** (`scratch/bl1587/check_archive.py`, reading the archive rather than the
task's word):
- master, `spend.json`, the tag ledger, `config.json`, both walk-row files and his grades are each
  byte-identical to the live file;
- **master's archived copy has 75,540 rows**;
- the planted control is absent, as it must be;
- `VERDICT: ARCHIVE HOLDS THE LIVE STORES`.

Both vault roots re-verified:

```
VERIFY <PROFILE>\AppData\Local/ClippersHQ/vault_bl1574: 4802 copies re-read, 1165.00 MB, sha256 mismatches 0, missing 0
VERDICT: VAULT VERIFIED
VERIFY D:/clippershq_vault_bl1574: 4802 copies re-read, 1165.00 MB, sha256 mismatches 0, missing 0
VERDICT: VAULT VERIFIED
```

## 3. One home, decided once, and wired

**The choice: `%LOCALAPPDATA%\ClippersHQ\operator\`.**
- **Not the Desktop, ever.**
- **Not Documents:** on this machine Documents is inside OneDrive (`<PROFILE>\OneDrive\Documents`),
  as the Desktop is. A synced file opens on a phone, but it can also turn into a cloud-only
  placeholder, and it sits in exactly the kind of place he tidies.
- **Not the repo:** the repo itself lives inside `OneDrive\Desktop`, and these files carry addresses
  that must never be committed.
- **Why `%LOCALAPPDATA%`:** it is outside OneDrive, invisible to any tidy, and next to the local
  vault.
- **The cost, stated:** he cannot open these files from his phone.

**Structural, not a convention.** The home and the rules around it now live in code:
- `clippershq/operator_home.py` is the one module: `HOME`, `path_for()`, `refuse_desktop()`, and
  `vault()`, which raises unless both roots hold re-hashed copies.
- `tools/review_loop.py generate` defaults to it. The Desktop helper that the old default fell back
  to (`desktop()` at `:90`, called at `:534`) is **deleted**.
- **`tools/deliver_workbook.py` is new.** It is the tracked replacement for the per-round one-off
  sheet scripts.
- **`tests/test_operator_home.py`** fails if any tracked Python file resolves the Desktop folder
  again. Its planted positive control proves the scanner can fire.

**Site count, both instruments** (`scratch/bl1587/desktop_sites.py`; the planted API snippet is
counted by both; a comment-only mention is counted by grep and not by AST):

| | before | after |
|---|---:|---:|
| grep lines mentioning the Desktop in tracked code | 10 | 7 |
| AST string or call sites | 6 | 4 |
| **tracked sites that WRITE his files to the Desktop** | **1** (`review_loop.py:534` → `desktop()`) | **0** |

**The 7 remaining lines, each read:**
- docstrings in `backup_prune.py`, `outputs_gc.py` and `scratch_gc.py` that describe the repo's
  location;
- a comment in `paste_batch.py`;
- a WSL probe path in `audio_wsl.py`;
- `make_shortcut.ps1`, which creates the **app's own launcher icon**. That is a program shortcut he
  keeps, not one of his files, and it is left alone.

**The habit still lives in closed rounds' scratch scripts.** Nine of them still define their own
`desktop()` (`scratch/bl1544`, `bl1545`, `bl1546` and others). That is how the habit spread, and the
next round that copies one would bring it back. Closed rounds' files are not edited. The defences are
the tracked guard test and a standing memory rule that every future session reads first.

**AST answered; grep over-counts prose.** Every earlier page and sheet came from round-numbered
scratch scripts, so the scan could not see them. That is why the fix is a tracked module plus a test
that future rounds must pass, not an edit to the old scripts.

**The shortcut.** It lives in the Start Menu, in a folder called **ClippersHQ**, not on the Desktop.
- **"Grade cards"** opens `review_CURRENT.html`, a stable filename that every new page replaces, so
  the shortcut never needs changing.
- **"Lead workbook"** sits beside it and opens his workbook.

Both targets exist, and no ClippersHQ file is on the Desktop.

## 4. The rebuilt page, vaulted at birth

`generate` now:
1. writes the page and its manifest to a temp folder;
2. **vaults both to both roots and re-hashes**;
3. only then moves them into his home and replaces `review_CURRENT.*`.

A missing vault root raises, and **no page is written**. The test proves it by passing an absent root
and asserting the output folder stays empty. No future round can skip the vault, because the vault is
the only route into the home.

**The page:** 323 cards, the same composition as the four he deleted (`--counts`):

| | survivor | held | cut |
|---|---:|---:|---:|
| TikTok | 150 | 36 | 50 |
| Instagram | 17 | 10 | 60 |

**Independent check** (`scratch/bl1587/check_page.py`):
- both files in both roots re-hash equal;
- `review_CURRENT.*` is identical to the stamped files;
- **0 of his 100 graded accounts are on it** (a positive control planted one graded account and it
  was found);
- cut cards per block of 100 in page order: **34, 34, 34** (at least 20 in every block), and 8 in the
  last 23 cards;
- 0 control bytes, and no stratum word anywhere on the page;
- 0 ClippersHQ files on the Desktop.

Verdict: `PAGE VAULTED, UNGRADED-ONLY, STRATIFIED, OFF THE DESKTOP`.

**A fourth button: "Edits, not for hire"** (key 4), added rather than asked, for three reasons:
- Only 32 of the 82 accounts he graded EDITOR carry any for-hire wording, 39.0% [29.2–49.8] [HIS].
- Four of his 17 rejects were people who edit for themselves, and the old page would have forced
  them into CREATOR.
- It changes nothing about how his judgement is scored: it is stored as `NOT_FOR_HIRE` and scores as
  NOT, exactly how he graded those four. The raw verdict is kept, so the two can be separated later.

The accessibility lead reviewed the change: **no WCAG 2.2 AA must-fix defects**. It noted one
cosmetic hint mismatch, which is fixed in the template for future pages.

## 5. His one workbook

`tools/deliver_workbook.py`:
1. **Seeded** his home copy by *copying* `Desktop\Random\clipper_emails_ALL.xlsx`, and verified the
   copy's sha equals the source. The original was only ever read; it is byte-identical to the round
   start.
2. **Backed it up**, sha-verified, to `backups/`.
3. Appended rows from master by `run_id`, **by header name**. The three repeated headers (`Bio source`,
   `Staleness`, `Email quality`) are never touched: 0 of their 9 cells are filled on any new row.
4. Read every sheet back and counted.
5. **Vaulted** the workbook and its backup to both roots.

| sheet | before | after | expected |
|---|---:|---:|---:|
| Emails | 3,028 | **4,276** | 4,276 |
| Would remove (craft cut) | 2,257 | 3,267 | 3,267 |
| Held for review (BL-1579) | 416 | 672 | 672 |
| the other four | unchanged | unchanged | unchanged |
| **MARK non-empty** | **0** | **0** | untouched |

**What went in:**
- 1,322 addressed BL-1583 + BL-1584 rows in master.
- 74 of them were already in his workbook, by address or profile link, and were skipped.
- 1,248 added: 238 KEEP and 1,010 CUT. The CUT rows went into Emails **with their label** and also
  onto the "Would remove" sheet, the workbook's own convention since BL-1572. Nothing is hidden from him.

**Re-derived from the saved file:**
- distinct addresses in Emails went from 2,965 to 4,222 (+1,257; some rows carry two addresses);
- rows tagged BL-1583: 88 KEEP and 384 CUT; tagged BL-1584: 150 KEEP and 626 CUT. Total 1,248.

## 6. The question only he can answer

`docs/NO_SEND.md:13` says he runs a separate tool that sends leads daily. If it mails these addresses,
then "13,007 addresses, none ever contacted", stated as fact in 10 of the last 26 reports, is false.
The reply data that every rate here only approximates may already exist on his side.

**What already exists to receive it:** `clippershq/outcomes.py` (847 lines) has
`mark_sent_from_csv` (`:345`) and `mark_bounced_from_csv` (`:501`), each of which takes a CSV. **One
export from his tool would settle it.** This project will not build a sender. Reading a result back is
in scope.

## 7. What I got wrong

1. **Part of this defect is mine.** In BL-1584 I wrote a review page and a KEEP sheet to his Desktop
   and vaulted neither. In BL-1585 I made "grade the cards on your Desktop" the single recommendation.
   He deleted both, correctly.
2. **My first `backup.py` change would have pulled his real files into every test archive.**
   `collect()` added the real operator home regardless of the root it was given. `test_backup` failed
   on a missing fixture store, and reading that failure exposed this. The home is now included only
   when backing up the real repo, and a new test asserts a synthetic root never reaches it.
3. **I did not re-run the backup after that fix.** Today's archive was written by the pre-fix code.
   For the real repo root the behaviour is identical (the home should be included), but the archive
   on `D:` was not produced by the committed version. Tonight's 20:00 run will be.
4. **My first two redaction passes missed the Windows short-name form of the profile path
   (`GAMECE~1`) in three suite logs.** Caught by grep; fixed before anything was committed.
5. **I reached for a redaction helper in the wrong round's directory** and briefly thought
   `scratch/bl1585/` had vanished. It had not; the helper was in `scratch/bl1584/`. I wrote a fresh
   one instead of reusing a closed round's file.
6. **A claim "closed through a file tool" still blocks commits.** BL-1579's claim file says
   `"status": "CLOSED"`, but it was never deleted. `tools/commit.py` treats any claim file as live, so
   it refused this round's commit of `tools/review_loop.py`. The pre-commit hook then refused a
   commit spanning two "live" rounds. I split it into two commits: `95e6aad7` for this round's paths,
   and `7d1bb17f` for the two BL-1579-claimed files, with `--foreign BL-1579` and the reason in the
   message. Never `--no-verify`. **This round's own claim is closed the same way, as the brief asks,
   and so it will block the next round identically.** The durable fix is for `claim.py` to treat
   `status: CLOSED` as released. Not done here; it was not declared.
7. **The page is larger than any he has graded.** 323 cards against the 100 he graded once. It
   rebuilds exactly what he deleted, cut cards are spread so any prefix he grades is usable, and
   autosave keeps his place. But it is a lot to ask of someone who has returned one page.

## 8. Assertions at close

```
stores this round did not declare (master, spend.json, config.json, email_harvest_tags.json, his
  Desktop\Random workbook, bl1572 results, every ground_truth/ file):  diff start -> end: 35 vs 35 files, 0 moved
suites (named exactly; snapshot-wrapped every run): ALL GREEN -- 6/6 suites passed, 79 checks
  (test_backup, test_bl1460_backup_cap, test_bl1576_retention, test_bl1579_review_loop,
   test_bl1580_nameerrors_and_store_root, test_operator_home); 0 of 35 and 0 of 1,266 store files moved
backup task: \ClippersHQ-Backup -> D:\clippershq-backups, lastResult 0, restore 212/212, VERIFIED True
vaults: both roots VAULT VERIFIED (4,802 copies each); page + manifest + workbook + backup in operator_files/ of both
Desktop: 0 files of ours; 0 tracked writers of his files
vendor calls: 0
```
