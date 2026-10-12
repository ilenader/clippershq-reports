# BL-1610 — Drive check, and the C: disk rescue

$0, zero vendor calls. Counts and sizes only. Nothing deleted; files were moved and each move verified.

## Drive check (asked first)

- Google Drive for desktop has **1** account signed in. It **is** his account (YES). Its My Drive is **G:**.
- G: reports 999.1 GB total and 26.7 GB free. That is exactly C:'s size, so it is the local disk, not the Drive quota. **2 TB is NOT shown on this PC.** The real plan shows at one.google.com/storage.
- The app's Drive pin is that account: YES. The marker matches, and the "me" package carries the same pin. Nothing was re-pinned.

## C: — where the space went

C: had **24.9 GB** free at the start of this round (57.8 GB the night before).

Bytes written in the last 24 h, estimated from files created or modified in that window (deleted files are invisible):

| Folder | Size | Last 24 h |
|---|---|---|
| `%LOCALAPPDATA%\Temp\claude` (Claude Code's temp folder; the **neuraltrack** project's sessions hold 58.4 GB) | 60.8 GB | **+34.6 GB** |
| `%APPDATA%\Claude\vm_bundles` (the Claude desktop app) | 14.9 GB | **+14.8 GB** |
| `%LOCALAPPDATA%\Microsoft\OneDrive` | 9.9 GB | +9.0 GB |
| `OneDrive\Desktop` (neuraltrack build +2.5, Flashcut +2.2, this repo +1.2) | 205.4 GB | +6.3 GB |
| `%LOCALAPPDATA%\Google\Chrome` | 31.8 GB | +2.2 GB |
| `%LOCALAPPDATA%\ClippersHQ\edits` (this app) | 14.1 GB | +1.2 GB |

The 15 largest folders are, in order:

| Folder | Size |
|---|---|
| `Videos\editing content - Movies` | 349.2 GB |
| `OneDrive\Desktop` | 205.4 GB |
| `OneDrive\Desktop\neuraltrack` | 130.6 GB |
| its `build` folder | 105.6 GB |
| `%LOCALAPPDATA%\Temp` | 93.6 GB |
| `Temp\claude` | 60.8 GB |
| `C:\Windows` | 38.0 GB |
| `OneDrive\Desktop\clipper finder` | 32.2 GB |
| Chrome | 31.8 GB |
| `twitch-clipper\library` | 25.9 GB |
| `Roaming` | 25.0 GB |
| `Downloads` | 22.5 GB |
| `CapCut` | 18.5 GB |
| `ClippersHQ` | 16.3 GB |
| `vm_bundles` | 14.9 GB |

The Google Drive local cache (`%LOCALAPPDATA%\Google\DriveFS`) is **0.2 GB**, so there is nothing to move.

None of those other folders was touched. The two biggest growers are other sessions' working files and the Claude desktop app's own image.

## The review folder → D:

The app had no setting for the review folder; it was hard-wired to `<edits home>\review`. This round adds one:

- **`review_dir`** (in `edits_overrides.json`, written with `edits_db.set_override`). When it is set, `edits_review.review_root()` uses it.
- A folder inside OneDrive or on a Desktop is refused. A relative value is ignored.

The move (`scratch/bl1610/move_review.py`):

- **Copy:** 2,067 files (10.29 GB) copied to `D:\ClippersHQ\review`. Each copy was re-read and compared by size **and** sha256: 0 failed, and 0 differ from the database's sha256.
- **Reviews kept going during the copy:** someone was reviewing at the same time (8 YES and 1 NO in the hour). The copy was made to skip files that left review mid-copy, and was then resumed.
- **Server stopped:** the app server was stopped by its PID only, during the switch.
- **Database backup:** the database was backed up to `D:\ClippersHQ` and passed an integrity check.
- **Stored paths:** rewritten in one transaction: `videos.staging_path` 2,067, `review_log.path` 4,892, `scope_log.prior_reason` 1,960. After the rewrite, no stored path pointed at the old folder, and every waiting video's file was present on D:.
- **Sources:** removed only after their copy verified (the second half of each move). 10.29 GB was freed on C:.
- **Review cap:** raised from **20 to 40 GB**. D: had 200.4 GB free afterwards. The 25 GB review floor now watches D:.
- **Playback proof:** the server was restarted the way the app's shortcut starts it.
  - `/review-file/<id>` returned the D: file byte-for-byte (sha256 equal), and a Range request returned 206.
  - In a headless browser with its own throwaway profile, the **Approve videos** screen played a waiting video from D:. Its clock went from 0.0 s to 2.0 s, the frame was 768×576, and there was no error.
  - The setup wizard (unfinished on this PC since before this round) was skipped with its own per-session "Later" flag, in the throwaway browser only.
- **The "me" package:** the builder now takes the waiting videos from `review_root()`. It also drops `review_dir` from the package's settings and maps the stored paths back to `<edits home>\review`, so the package stays self-contained.
- **Tests:** `tests/test_bl1610_review_dir.py` passes, and so do BL-1605 (fresh rules, review), BL-1606 (package, phase 1), BL-1607 (me) and BL-1608 (drive).

**C: free: 24.9 GB before this round → 34.3 GB after.** Other sessions kept writing to C: meanwhile, so the gain is less than the 10.29 GB moved.

## Process slips (disclosed)

- One stray command contained an empty heredoc, which breaks the "no heredocs" rule. It was stopped; it ran nothing and wrote nothing.
- In tool output only, never in a report: one traceback showed one review file's name, and two folder listings showed Drive's numeric account folder name. The masks were then fixed (`\d{9}` → masked).
