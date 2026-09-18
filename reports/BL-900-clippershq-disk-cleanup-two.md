# BL-900 — 9.34GB deleted, 2,154 clips kept, and there is no such thing as a raw twitch stream on this machine

**2026-09-18. No database touched. No product code changed. BL-900 made ZERO commits to the ClippersHQ repository.**

## THE HEADLINE: THE STREAM CLASS IS EMPTY, MEASURED, NOT GUESSED
Every video file in the 13 directories was probed with ffprobe. **3,572 videos. Longest 62.90 seconds. Mean 13.22s. Shortest 3.83s.** There is no second mode, no order of magnitude gap, no threshold to justify, because **there is nothing on this disk that is a raw twitch stream.** A stream is hours; the longest thing here is a minute and three seconds. So the "delete raw streams if genuinely large" half of your rule matched **0 files and 0 MB**, and I did not invent a cutoff to make it match something.

What I did delete is the half that was unambiguous: **1,418 comparison render files, 4,887.0MB**, and **196 zip archives, 4,681.6MB**, whose contents were 1,348 more comparison renders plus 218 small files I extracted and preserved first. **9,568MB gone, 1,614 files, 0 refused, 0 failed.** The 13 directories went from **19,904.2MB to 10,336.1MB**.

**Every clip survived. 2,154 of them, 3,873.7MB.** The full index with path, bytes and duration for each is published beside this report as `BL-900-surviving-clips.tsv`.

## PART 0 — EXCLUDED, AND ONE THING THAT MOVED UNDER ME
• Primary checkout, `C:\w`, `C:\bl898-sandbox` and every registered worktree: excluded.
• **`C:\w2` and the twitch clipper project: untouched, and the standing risk is restated.** That repository still carries **27 local only commits** on `main` and `sfx-001-emoji-002` that are not on its origin, and `C:/w2` is still its registered worktree with two uncommitted modified scripts. **Not acted on. Still yours to deal with.**
• **BL-898 merged while this round ran.** The primary HEAD moved `97fdf3a8` to `499fe10b` and its worktree deregistered itself. That is BL-898's work, named below in PART 5 so it is not mistaken for mine.
• No system directory was entered. Only the 13 in scope directories were read or written.

## PART 1 — EVERY VIDEO CLASSIFIED BY MEASUREMENT

| class | the rule I used | files | MB | action |
|---|---|---:|---:|---|
| comparison render | filename carries `__ORIGINAL` or `__OURS`. Name, not guess, and the pairing below proves the intent | 1,418 | 4,887.0 | **DELETED** |
| raw stream | duration an order of magnitude above the clip mode. **No file qualifies. Max on disk is 62.90s** | 0 | 0.0 | **class is empty** |
| clip | a finished short video: a `_work/final` render, a downloaded source, or a video outside the render tree | 1,514 | 3,106.1 | **KEPT** |
| unclassified | `head.mp4` (625) and `_bl*_magenta.mp4` (15): pipeline intermediates the rule does not name | 640 | 767.5 | **KEPT, and said so** |

**Duration histogram, all 3,572 videos:** under 5s: 11 (5.3MB). 5 to 10s: 1,080 (1,391.3MB). 10 to 20s: 2,288 (6,022.7MB). 20 to 30s: 103 (348.1MB). 30 to 60s: 67 (711.6MB). 60 to 63s: 22 (281.6MB). One file had no readable duration (a 0.3MB `.tmp.mp4`), so it was left alone.

**NOT ONE COMPARISON FILE WAS MISSING ITS PARTNER. 709 `__ORIGINAL` and 709 `__OURS`, exactly 709 complete pairs, zero lone files.** That was the risk you named, that a solitary `__OURS` might be a finished clip carrying the suffix by accident. It does not occur here even once.

The four totals were measured and are stated above **before** anything was deleted, and the deletion list was written to a file of full paths from them.

## PART 2 — THE TWO DATA BACKUPS, AND THEY WERE NEVER AT RISK
Copied out and sha256 verified **before anything in `ClippersHQ_renders` was touched**: `bl1235_backup\` (4 files, 620KB: a CSV and an XLSX export of 288 repost accounts, and a 3,972 row bot ready lead CSV with its metadata) and `songs.json.backup_20260812_160748` (45KB, the hand edited song library with its hook windows). **681KB total, 5 of 5 hashes matched.**

**Then measurement found something better than a copy: all five already exist in the `clipper finder` repository**, matched by blob OID. They were never one disk error from gone. They remain exactly where they were, undeleted, plus a verified copy now at `Desktop\BL900-preserved-backups\`. They are deliberately **not** in the pushed archive, because `output_ALL_BOT_READY.csv` carries 3,972 email addresses.

## PART 3 — THE UNIQUE CODE: 19GB HELD HOSTAGE BY 23MB
I did not trust BL-899's list. Every non media file in all 13 directories was hashed **two ways**, raw bytes and LF normalized, and checked against **eight object stores**: ClippersHQ, twitch clipper, ClippersHQ-Deck-2026, ceo-dashboard, clipper finder, insta outreach, neuraltrack and clippershq-reports. Two hashes because the CRLF trap is real: `git hash-object --no-filters CLAUDE.md` gives `736dca59`, the stored blob is `1f4a6672`, and only the LF form matches.

**3,996 non media files. 1,078 already in a repository. 2,918 exist nowhere else, 163.23MB raw, 66.02MB once deduplicated.**

**A BL-899 FINDING WAS WRONG AND THIS IS THE CORRECTION.** BL-899 reported `C:\temp\render003\RENDER-003.md` as existing "here and nowhere else" because it differed from `origin/main`. Its blob `d8411234` **is** in the twitch clipper repository, committed as `de57e29 RENDER-003: the five defaults were already right`, which is on that repo's origin. It is simply the earlier version, later amended by `9fcde1f`. Comparing against the tip only tells you the tip. Nothing was lost by the error, and nothing had been deleted on it.

**The archive: `preserved/BL-900/BL-900-unique-files.tar.gz`, 3,106 files, 23.04MB compressed, 62.54MB raw**, paths preserved so any file returns to where it came from, plus a 3,106 line manifest of path, size and blob OID. **That is the finding, stated plainly: 19.4GB of directories were being held hostage by 23 megabytes.** Once you are happy with the archive, the rest of those directories can go.

**VERIFIED FROM ORIGIN, NOT FROM PUSH OUTPUT.** `ls-remote` says `refs/heads/main = 0205d1482b7f5b5a33154a5c3cc57c8827b6ac2b`, and a **fresh shallow clone straight from GitHub** gives the archive back with sha256 `7197da11...`, byte identical to the local file, containing 3,106 files.

**THE SECRET AND PERSONAL DATA SCAN EXCLUDED 30 FILES, 100.69MB, AND THEY WERE NEVER PUSHED ANYWHERE.** They stay exactly where they were on disk, undeleted: four copies of `master_leads.csv` carrying **9,784 to 10,136 email addresses each** plus api key, Resend key and wallet pattern matches; `master_leads_delta.csv` with 352 addresses; 18 `spotify_finder` sources with 7 to 76 addresses each in fixtures and policy lists; `C:\tmp\bl882-prompt.txt`, which contains **an Auth.js session token**; and 6 wallet pattern matches that are near certainly false positives on base58 style strings (`package-lock.json` integrity hashes, OCR report tokens), excluded anyway because the safe direction is out.

**Is the reports repository the right home? No, and the README in `preserved/BL-900/` says so.** `spotify_finder` is outreach tooling, `mbwt` is meme render OCR evidence, `wt` and `temp` are twitch clipper scratch, and every future clone of the report log now pays 23MB for them. It is there because creating a new repository is an outward facing action nobody authorised and pushing into other projects' repositories changes them unasked. **Recommendation: move it to a dedicated `clippershq-attic`, or split it back to `clipper finder` and `twitch clipper`, then `git rm` it from here.**

## PART 4 — THE DELETIONS
From a written list of **1,614 full paths**, one at a time, **no wildcard and no recursive directory removal**. Four checks ran **immediately before each file was unlinked**, not from the census taken an hour earlier: the path is under one of the two permitted roots; it is still a regular file; **its size still matches exactly what PART 1 measured**; and its name still carries the comparison suffix. For a zip a fifth check re listed the archive **live** and refused it if a single entry was neither a comparison render nor already sitting in the preservation staging.

**1,614 deleted, 0 refused, 0 failed, 9,568MB reclaimed.** Nothing was held open by a stray shell, so there is nothing to name under BL-885's rule. `clipper_render_test` held 16 files and all 16 were comparison renders: the files went and **the folder was left in place**, as were its subfolders. Confirmed afterwards: `0` comparison files and `0` zips remain anywhere in scope.

## PART 5 — TOTALS AND VERIFICATION
**Enumerated** 41,179 files, 19,904.2MB across 13 directories. **Deleted** 1,614 files, 9,568.0MB. **Preserved** 3,106 files, 23.04MB compressed, verified from origin. **Excluded from preservation** 30 files, 100.69MB, still on disk. **Kept** 10,336.1MB.

**Surviving clips: 2,154 files, 3,873.7MB.** Where they are: `ClippersHQ_renders` 1,872 (3,276.4MB), `mbwt` 273 (532.9MB), `temp` 6 (52.3MB), `tmp` 2 (10.9MB), `C:\c` 1 (1.1MB, the DZD render BL-899 flagged as the only surviving copy: it is 1.1MB and short, so it is a clip and it stays). Durations: 11 under 5s, 710 at 5 to 10s, 1,299 at 10 to 20s, 89 at 20 to 30s, 32 at 30 to 60s, 12 at 60 to 63s, 1 unreadable. **Every path, size and duration is in `BL-900-surviving-clips.tsv` beside this report, so you can check the list yourself.**

**Left unclassified and kept, with what you would need to decide:**
• **14,805 PNG files, 5,881.0MB, the single biggest thing still on the disk.** 14,094 of them sit under `_work/` and are named `sub_N.png`, `srcline_N.png`, `lb_N.png`, `srcbig_N.png`, `readback.png`: subtitle tiles, source lines and letterbox probes, render intermediates rather than pictures of anything. Your rule named videos, not images, so they stay. **Say the word and they go.**
• **640 pipeline intermediate videos, 767.5MB** (`head.mp4`, `_bl*_magenta.mp4`). Same reason.
• **184MB free for nothing: 19 of the 22 large `fixture.mp4` files in `mbwt` are byte identical**, sha256 `c9e67061`, one copy per evidence folder. Keeping one loses nothing. I did not do it because `mbwt` is the directory that holds unique work and you did not ask.

**Repository state.**
• **BL-900 committed nothing to the ClippersHQ repository.** `git log --grep=BL-900` returns 0.
• `git status --porcelain` shows the **same 19 untracked entries** as at session start, all other sessions' files, none staged, modified or swept.
• **`src/lib/clip-earnings-writer.ts` DID change, and it was not me.** BL-898 merged mid round: `989a4683` and `499fe10b`, +142/-1 on that file, which is its stated purpose, the budget lock pricing every leg it causes. The other five money files are **byte identical by blob OID** across `97fdf3a8` to `499fe10b`: `earnings-calc.ts 00410634`, `balance.ts 67c30c89`, `tracking.ts 8e2a62f5`, `clip-earnings-invariant-middleware.ts 61cef393`, `money-decimal.ts ef5cdae7`.
• **ClippersHQ origin moved only by BL-898**, `97fdf3a8` to `499fe10b`, confirmed by `ls-remote`. This round's only commit anywhere is the preservation commit `0205d14` to the reports repository.
• **No database was touched.** No build was run and none is claimed.

Disk level free space read 157G at the start and 135G now, which moved the wrong way because BL-898 was building on this machine throughout. The scope measurement is the honest number: **19,904.2MB to 10,336.1MB, 9,568MB reclaimed**, and it was taken by walking the same 13 directories before and after.
