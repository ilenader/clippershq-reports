# BL-1678: one Google Drive link with everything -- 970 approved videos (6.66 GB), cleaned, in 6 niche folders, every file checked on Drive ($0)

Order (2 APP, 2026-10-19 16:18, Dusan helm 15:45 via ALFRED): "Give him a Google Drive with everything inside,
accessible through one link."

## Result
- ONE folder `My Drive\ClippersHQ Sends\ClippersHQ - all approved edits 2026-10-19`, "anyone with the link can view".
  The link is in the 2 APP reply (not in this public report). An anonymous GET opens it (200, no sign-in page).
- **970 videos**: Football 580, Movies and TV (superhero) 267, Basketball 59, UFC 56, Tennis 5, Other (outside the 5
  niches) 3. That is all 1,003 approved videos in the local library minus 33 (below).
- Each copy is cleaned the same way a Send cleans it (edits_clean: every tag, udta box and SEI unit gone, nothing
  re-encoded, neutral names like `football_0001.mp4`) and verified: no metadata, no handle or id in the bytes, and the
  decoded picture and sound match the library file.
- Drive check: all 970 files on Drive match the cleaned copy's size + sha256 (970/970). Nothing else is in the folder.
- Library rows are **not** marked sent. This folder is a copy of everything, so later "send 20 football" orders still
  work as before.

## Left out (33 of 1,003)
| why | n | detail |
|---|---|---|
| corrupt file | 24 | ffmpeg cannot decode 85-92 % of the frames (checked fresh on an idle PC, not a timeout) |
| repost | 3 | the same video as one already in the folder (frame hashes) |
| metadata check failed | 6 | 5 x exiftool `Track1:Unknown_hvcC` (HEVC files), 1 x `strings:lavc`. The safety rule keeps them out |

## Findings
1. **A detached job starved at BelowNormal priority.** It got 2 s of CPU in 7 min while the PC sat at 0 % load
   (python + ffmpeg BelowNormal, working set trimmed to 24 MB). I stopped my own task by its PIDs and reran the job at
   normal priority from the window's shell: ~7.5 s per video. Resumable through a manifest, so nothing was lost.
2. **A stale "broken" cache hid 3 good videos.** `send_gates` caches the picture verdict per file size. 2 rows from
   14 Oct said broken (one had 11 of 94 frames), but both files now decode fully. A third (240 s) decodes cleanly yet
   fails the "frames >= 80 % of duration x 2" rule. All 3 were re-added after a fresh full decode + clean + verify.
   Follow-up for the app (not changed here): a picture-pass timeout or failure is cached as `broken` forever. LESSON 22
   says a timeout is not a verdict.
3. **`Unknown_hvcC` is HEVC's decoder-config box.** That is usually structure, but it can carry SEI NAL units, so
   allowing it needs a test that strips or inspects hvcC SEI first. Not changed.
4. Upload throughput was ~0.5-1.15 MB/s while the line sent 5-6 MB/s (other programs share it). 6.6 GB took 2.5 h.

## Not inside: the old "ClippersHQ Edits" Drive folder
14,661 library rows live only in `My Drive\ClippersHQ Edits` (the harvester's output before 12 Oct). They were never
cleaned of metadata (OWNER_RULES 12 Oct: "full metadata needs to be removed fully"). The app's Drive connection
(rclone, scope drive.file) also cannot see files it did not create. Putting them behind the same link needs Dusan's
call: download -> clean -> re-upload (~$0, many hours), or share that folder himself as it is (metadata stays).

## Money
$0. The paid niche-vision gate was not asked; folders follow the library's niche (the account's niche).

## Files
- `scratch/bl1678/everything.py` (main job), `scratch/bl1678/addon.py` (the 3 re-adds), `scratch/bl1678/PROGRESS.md`.
  The manifest stays local (it holds video ids).
