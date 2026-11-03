# BL-1744 -- paid LamaTok edit search for ALFRED's search-first edit finder

Orders 2026-11-03_1831 (get it ready, no spend) and 2026-11-03_1855 (Dusan HELM 18:46: yes, cap $3.00). 1 LEADS.

## Result
- Every niche reached 20 links in `S8-Videos/NEWEST 03 Nov`: **79 new edits kept** (football 15, UFC 15, basketball 16,
  movies 16, anime 17) for **$0.179 real** of the $3.00 cap (wallet line `Edits search 3 Nov`), 19:36-20:59.
- Per 100 kept: ~380 LamaTok requests, $0.23, ~105 min wall (incl. a 25-min hang); ~70 min without it.
- 0 download failures at 21:00 (Video Downloader worker; a few still downloading).

## How
`scratch/bl1744/edit_search_paid.py` lists LamaTok `/v2/search` pages (keywords) and `/v2/hashtag/medias` pages
(edit hashtags) per niche, maps items with `clippershq/edits_signals.video_from_item` into ALFRED's candidate dict,
and runs ALFRED's own `MILOJE/tools/edit_scan_ytdlp.search_round` (list filter 48 h / 5 d at 250K likes, 1 like
per 10 views, English, one per creator, no repeats -> Haiku cover+caption check -> Video Downloader hand-off).
Money: `money_guard.spend(<line>, cap)` before any call (Finder lines refused), the `edits_vendor.Vendor` meter
stops before the cap, settle to the metered requests at the end. `wait_line.py` started it within 30 s of the line.

| run | sources | rounds | calls | kept | note |
|---|---|---|---|---|---|
| 1 | 9 keywords + 10 hashtags | 12 | ~170 | 64 | rounds 1-4 gave 32/10/8/7, then 4 rounds of ~0; stopped by PID, settled by hand |
| 2 | 38 named subjects | 1 (hung) | <= 60 | 0 | stuck 25 min in ALFRED's `fetch_cover` (SSL read on a CloseWait socket, py-spy); stopped by PID, settled $0.036 |
| 3 | 38 named subjects | 3 | 68 | 15 | ended by itself: all niches at 20 |

## Findings
1. Generic edit keywords/hashtags give most of their 48 h videos on the first 3-4 pages; deeper pages are older
   (LamaTok lists are not newest-first). Named subjects (players, fighters, titles) refill fast on page 1.
2. ALFRED's `fetch_cover` (urllib, timeout=15) can hang on a dead socket: the runner now passes `get=` with a hard
   20 s deadline (thread + `result(timeout)`). Told ALFRED (ROOM 21:02).
3. The 3 Nov 15:xx `search_round` checked only the first 2 x target survivors, dropping paid listings unseen; the
   20:27 version (target per niche, pool 3 x need) is used as is.
4. Stops added: 2 rounds with 0 kept, a `bl1744_work/STOP_RUN` file.

Commits: 4b6cd6a1, 3a25c930, 827f346c. Selftest: `python scratch/bl1744/edit_search_paid.py selftest`.
