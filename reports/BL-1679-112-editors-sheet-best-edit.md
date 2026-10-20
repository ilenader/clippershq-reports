# BL-1679: the 112-editors sheet now links each editor's best edit; 3 ways to get below $40 per 1,000 ($0)

Order (2 APP, 2026-10-20 15:41, Dusan HELM 15:31 via ALFRED): the 112 editors in ONE Google Sheet (name, profile link,
email, followers, a thumbnail or link to their best edit, one line on why they are a real editor), shared. Then 3 lines
on bringing $46.50 per 1,000 below $40. Spend nothing, keep CPU low.

## Result
- The sheet already existed (1 LEADS, BL-1677 `s112.py`, 14:00) with name, profile link, email, followers, the
  why-line, how found and test. It lacked only the best edit.
- `scratch/bl1679/best112.py` read the LIVE sheet back, kept every cell, and added two columns: **Best edit (most
  plays)** (a clickable TikTok video link: the stored post with the most plays) and **Best edit plays**.
  Read back from Drive: 112/112 rows, 112/112 best-edit links. The sheet opens for anyone with the link (anonymous
  GET 200). It is a link and not a thumbnail, because TikTok cover image URLs expire within days.
- $0. No vendor calls. Light CPU (a few seconds of local reads + 2 Drive API calls).

## Below $40 per 1,000 (from 1 LEADS's measured T1-T5 tests, 20 Oct)
1. Pay only for the two routes that already beat $40: T3 (re-walk tags that gave 1 editor before: 44 good for $1.57 =
   $36) and T4 (refill re-walk of proven tags: 22 for $0.84 = $38). Together 66 for $2.41 = **$36.5 per 1,000**. Drop T2
   (TikHub, $95) and the broad T1 re-walk ($47). T5 ($48) is used up.
2. Space re-walks of the same tag at least 2-3 days apart. T4 cost $49 after removing the editors T1/T3 had just
   found, so a too-early re-walk pays for repeats.
3. Keep the tag list self-pruning: after each walk, add every tag that produced a good editor (T3's source list) and
   drop tags with 0 good editors on 2 walks in a row. Price each chunk and stop at > $40.

## Files
`scratch/bl1679/best112.py`. Sheet state: `%LOCALAPPDATA%\ClippersHQ\bl1677_work\s112\sheet.json` (BL-1677's).
