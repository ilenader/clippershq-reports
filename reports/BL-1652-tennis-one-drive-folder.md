# BL-1652: one Drive folder "Tennis - all edits" -- 4 real tennis edits posted in the last 14 days are in it; 1 older one listed apart; every new tennis send now goes into the same folder

2 APP order `2026-10-16_1037_2-APP-DUSAN-WANTS-ONE-GOOGLE-DRIVE-FOLDE` (ALFRED for Dusan, 10:37). Money: **$0** (no paid call).

## Card

| # | Item | Result |
|---|---|---|
| 1 | **Folder** | `My Drive / ClippersHQ Sends / Tennis - all edits`, **anyone with the link can view**. The link is in the office reply only (this report is public). Opened with no Google sign-in (plain `curl`, no cookies): HTTP 200, all 4 file names on the page |
| 2 | **In it** | **4** real tennis edits, posted 4, 5, 6 and 10 Oct (6.0-11.9 days old on 16 Oct 10:50) |
| 3 | **Older than 14 days** | **1**: posted 30 Sep 22:31 (15.5 days), file `tennis_2026-10-15_001.mp4` in the old folder "Tennis 2026-10-15 (3)". Not put in the new folder |
| 4 | **How copied** | Drive server-side copy from the 14, 15 and 16 Oct folders (the files are the ones already cleaned + verified when they were sent; nothing re-made). Each copy's size + sha256 as Google Drive reports it == the send record: **4/4** |
| 5 | **The post date** | Two sources agree for all 5: the library's `posted_at` and the upload time written inside the TikTok video id itself (top 32 bits): at most 32 s apart |
| 6 | **From now on** | `clippershq/edits_send.py`: `FIXED_FOLDERS = {"tennis": "Tennis - all edits"}`. A tennis Send (app button or `tools/edits.py send`) goes into that ONE folder, never a new one; only edits posted within 14 days (`FIXED_MAX_AGE_DAYS`); file names continue after the ones already there. Other niches still get a new folder per send |
| 7 | **Old folders** | The 3 per-day tennis folders are left as they were (their links keep working). Nothing deleted |

## The code change (clippershq/edits_send.py)
- `FIXED_FOLDERS` + `FIXED_MAX_AGE_DAYS = 14`. In `run()`, for a fixed niche: a video posted more than 14 days ago is gated `posted_over_14_days`; a video with no post date is gated `posted_unknown` (positive evidence only). These gates are free (no model asked) and use none of the paid-try budget. Gated videos stay in the library, unsent.
- Names: `_free_names()` lists the folder first and skips every name already in it (a second tennis send today gets `tennis_2026-10-16_002.mp4`, never overwrites `_001`).
- A failed send into the fixed folder deletes **only its own uploads** -- the old code purged the whole send folder on failure, which for a shared folder would have trashed every earlier tennis edit.
- The send worker runs in its own process (`tools/edits.py send-run`), so the change is live for the next Send without a server restart.

## Tests
- `tests/test_edits_send_fixed_folder.py` (new, BL-1631's synthetic world: temp homes, fake Drive): two sends -> one folder, names continue, one link; >14 days and no date gated; a failed send keeps the earlier files and the folder; a niche not in the map still gets a new folder. **4/4 pass; control: 4/4 fail against HEAD's `edits_send.py`.**
- `test_bl1631_library_send` + `test_bl1636_send_gates`: 20/20. `test_bl1639_film_is_superhero`: 2/2.
- `tests/run_all.py --jobs 4 --mine BL-1652`: **NOT completed** -- Claude Code stopped it because the PC was critically low on memory. Its partial output (206 pass / 376 fail, 325 of the fails in under 1 s = suites that could not even start) is no evidence either way, and it was not re-run (the host says not to while memory is short). The full suite is still owed: for 3 FIXER, when memory allows.

## Open (Dusan's call, one line)
- Edits in the folder get older every day; nothing takes them out after 14 days. Say if they should be moved out (to a "older" folder) as they age.

## Files
- `scratch/bl1652/seed.py` -- the one-time copy (plan without `--go`; idempotent: skips names already there; checks size + sha256; links).
- `scratch/bl1652/ids.py`, `look.py`, `drive_ls.py` -- read-only checks (dates, sends, Drive listing; no links or ids printed).
