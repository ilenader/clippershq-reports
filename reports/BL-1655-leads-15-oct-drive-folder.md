# BL-1655 -- the 15 Oct first-world editors in ONE Drive folder "Leads - 15 Oct" ($0)

Order: office 1_LEADS 2026-10-16_1431 (ALFRED for Dusan). No vendor call, $0.

## What was done
- The BL-1649 first-world editor files (football b1-b5, movies b1-b4, sports b1-b3, plus the three 16 Oct second-look
  files) merged into 4 Excel files, one row per email, deduped across all files:
  - Football 344 / Movies 233 / Sports 152 (eye-checked editors, first world)
  - Less sure 138 (football 35, movies 66, sports 37) -- the second look; 2 of the 140 rows were addresses already in
    the main files, so they are dropped there. 867 unique addresses in all (869 rows delivered on 15/16 Oct).
- Columns: email, handle, niche, hashtag, followers, date, profile link, country. The local "page picture" and "run"
  columns are left out (they point to this PC). The less-sure file has an About sheet.
- Uploaded to Drive "ClippersHQ Sends/Leads - 15 Oct" with clippershq/edits_gdrive.Backend (rclone); size + sha256 of
  every file checked against the local copy: 4/4 ok. Link set to anyone-with-the-link can view; an unauthenticated
  GET of the folder returns 200.
- Local copies: operator\leads_15_oct\. Script: scratch/bl1655/up.py.

## Link
In the office reply (1_LEADS/replies/2026-10-16_1431_...) -- not printed here (a folder id is shaped like a key).
