# BL-1651: 100 real tennis edits asked -- only 51 tennis videos were waiting; a 3rd closer look found 1 new real tennis edit (sent); 100 needs ~3,400 more tennis pages

2 APP order `2026-10-16_0620_2-APP-DUSAN-WANTS-100-REAL-TENNIS-EDITS` (ALFRED for Dusan, 06:20). Money: **$0** (no paid call).

## Card

| # | Item | Result |
|---|---|---|
| 1 | **Tennis videos waiting** | **51**, not ~255 (the whole review queue was 54). The Claude lane had already looked at all 51 twice (Sonnet, then Opus, small frames): every one UNSURE |
| 2 | **What they show** | Only ~11 of the 51 show tennis; the rest are football / film / superhero / ufc videos from pages found on tennis tags |
| 3 | **3rd look** | Opus on the LARGE sheets (144x256 frames, 30 per sheet), then 2 APP's own eye on every tennis sheet. Tennis: **1 real edit** (a Sinner quote edit: many settings, scribble overlays, lyric text). The other tennis videos are broadcast rally / trick-shot / ball-kid compilations with name labels, circles, a grade -- raw by the spec rule from BL-1647 -- or a couple video made of paparazzi photos (left for the friend) |
| 4 | **Applied** | 26 sure answers that agree with the earlier look's lean (or that 2 APP eyed): **10 YES** (tennis 1, superhero 4, football 3, basketball 1, ufc 1) into the local library, **14 NO** rejected. 9 answers that DISAGREED with the earlier look were held (sure:false) -> they stay UNSURE for the friend |
| 5 | **Friend's queue** | 54 -> **30** (27 of them from tennis pages) |
| 6 | **Drive** | New folder **ClippersHQ Sends / Tennis 2026-10-16 (1)**: 1 video, cleaned + verified + Drive size/sha checked. The link is in the office reply only (this report is public). Real tennis edits in Drive now: **5** (10-14: 1, 10-15: 3, 10-16: 1) |
| 7 | **Pages needed for 100** | See below: **~3,400 more tennis pages** at today's rate (likely range ~1,500-10,000) |

## The rate (review era only; the 398 pre-review "old_drive" tennis rows are excluded -- their files are no longer in his Drive)
- Tennis-page videos judged: **397 from 179 pages** -> **5 real tennis edits from 4 pages**.
- = 1 real tennis edit per ~80 tennis-page videos (1.26 %), **1 per ~36 tennis pages** (each page brings ~2.2 viral videos).
- 95 more edits -> ~**7,500 more tennis-page videos**, i.e. ~**3,400 more tennis pages**. 5 is a small count: the 95 % range is ~1,500-10,500 pages.
- Already found and waiting for download (QUALIFIED, last 14 days): **1,834 tennis-page videos from 811 pages** -> at 1.26 % about **~23 tennis edits**. Downloads are OFF until Dusan says so (his rule); downloading is $0 (his downloader), reviewing them is $0 (AI script + Claude lane).
- So: the 811 waiting pages give ~23; the rest (~72) needs ~2,600 NEW tennis pages (finding pages = 1 LEADS, paid).

## One question that changes the count
Most "tennis edits" on these pages are **broadcast rally compilations with name text, circles and a colour grade** ("pov: a master of his craft", "the art of ..."). By the spec (from the friend's labels, BL-1647) they are RAW, not edits. If Dusan counts them as tennis edits, ~7 more of today's 51 qualify at once and the rate rises several times.

## Found (for 3 FIXER)
- `edits_claude_lane.ingest()` uses `op_for(vid)` = `claude-<id>`: for a video that was decided before and then sent back with BACK, the new decision reuses the old op id and the journal silently skips it as a repeat. Hit 2 videos today (yesterday's NO -> BACK -> recheck). 2 APP put their lane rows back to the saved UNSURE rows, so the lane claims nothing the app did not do. Fix to make: a fresh op per decision (as `correct()` already does).
- `edits_send.run()` skips `sent_hashes()` (the "already sent" duplicate check) whenever a custom `GATE` is set. scratch/bl1651/send_free.py adds the hashes back itself.
- The 51 lane rows before the 3rd look are kept in scratch/bl1651/lane_before.jsonl; the 3rd look's untouched answers in each batch's answers_raw.jsonl (`<edits home>\claude_lane\batches\bl1651_tennis3_00{1..4}`).

## How
`scratch/bl1651/prep3.py` (backup + large-sheet batches) -> 4 Opus sub-agents -> `gate3.py` (hold disagreements) ->
`tools/edits.py claude-lane ingest ... --by claude-opus-large` -> `restore2.py` -> `send_free.py tennis 1` (the Send to Drive
of `tools/edits.py send`, with the niche gate's paid vision-model call OFF -- Claude already judged the niche; picture,
duplicate, clean, verify and Drive check all ran). Counts: `q7.py`, `q8.py`.

- 07:10 FINDER BL-1651 tennis: 51 waiting (not 255), 3rd look -> 1 new real tennis edit sent to Drive "Tennis 2026-10-16 (1)" (5 in Drive in all); 100 needs ~3,400 more tennis pages; $0 (DONE)
