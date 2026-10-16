# BL-1654: the downloaded tennis videos are all reviewed, and none is a new tennis edit; the review pictures were made on Flashcut farm PCs ($0)

Order `2_APP/2026-10-16_1713` (ALFRED for Dusan 17:13): go on with BL-1654; put all 5 real tennis edits in the Drive
folder "Tennis - all edits", the 12 unsure ones in a subfolder "Not sure"; review in small batches on the pod or a farm
PC, not Dusan's PC; add each new tennis edit to the same folder. Money: **$0** (no paid AI; the app's AI reviewer day cap
stays $0 while BL-1654 is open).

## Card

| # | Item | Result |
|---|---|---|
| 1 | **Drive folder** | "Tennis - all edits" = **all 5 real tennis edits** (the one posted 30 Sep copied in server-side) + subfolder **"Not sure" = the 12 wave-1 unsure** videos, cleaned like a send (metadata removed, checked for the video's own id/handle/name). **17/17 size + sha256 match** what Drive reports; both folders open without a login (anonymous GET 200, all names shown). Link: in the reply only (a Drive id is credential-shaped). |
| 2 | **Reviewed** | **578** downloaded tennis-tag videos (40 earlier + 538 now). Final: **86 YES** (84 film/TV -> superhero niche, 1 UFC, 1 football), **398 NO**, **94 UNSURE** (left for the friend). |
| 3 | **New tennis edits** | **0.** Of 754 answers, one video was tennis by subject: a TV broadcast of an umpire dispute with captions = not an edit (eye-checked by 2 APP). So nothing new went to Drive. |
| 4 | **Where the pictures were made** | Flashcut farm PCs (mostly Bane), never Dusan's PC: 13 farm_only jobs of <= 40 videos, 46-148 s of farm time each; 534 sheets, 4 unreadable. Dusan's PC only copied files and ran the Claude sub-agents. |
| 5 | **Second look** | Opus on all 176 first-look unsure, from the SAME farm sheets (no decode here): 82 decided (11 YES, 71 NO), 94 stay unsure. |
| 6 | **Every decision landed** | `scratch/bl1654/ingest_check.py`: every applied YES/NO changed the video's state in the app (0 not landed, LESSONS 13). |
| 6b | **2 not pictured** | 2 long videos (4.1 and 4.5 min; the files are fine, h264 + aac) came back unreadable from the farm twice (retry 20:02, finder-sheets-1016200205-1). They stay in review for the friend; Dusan's PC did not make them. |
| 7 | **Not done** | Downloads stopped at 17:06 on the downloader's own breaker (10 failures in a row, "no video stream"): **1,183 tennis videos are still not downloaded.** Not restarted: needs Dusan's word. |

## How the farm part works
- `neuraltrack/build/work/finder/finder_sheets_job.py` (a NEW file of 2 APP in Flashcut's tree; no Flashcut file changed)
  runs Clipper Finder's own `clippershq/edits_claude_lane.py` `sheets()`, shipped as an input and lifted (one source).
  Local check: byte-identical picture to `sheets()` on a real video.
- `scratch/bl1654/farm_sheets.py submit|collect|status` queues `farm_only` script jobs (Flashcut's lane never runs them on
  this PC; when no farm PC is free it re-offers them) and turns the returned pictures into normal claude-lane batches.
- `scratch/bl1654/opus_prep.py` = the second look from the same sheets.
- 3 FIXER built the same idea as a proper tool (BL-1658, `clippershq/farm_sheets.py`), blocked until Flashcut adds a
  `sheets` job kind. When that lands, 2 APP switches to it and deletes the build/work/finder file.

## Numbers by round
| round | videos | YES | NO | UNSURE |
|---|---|---|---|---|
| wave 1 (this PC, before the order) | 40 | 4 | 24 | 12 |
| Sonnet, farm sheets | 538 | 71 | 303 | 164 |
| Opus second look (176 unsure) | 176 | 11 | 71 | 94 |

## Closed 20:15
- The app's AI reviewer day cap is back at **$1.00** (it was set to $0 for this round only, 14:47).
- Separate small order (3 FIXER, 20:05): video m10306, a TV-series dialogue edit the Claude lane wrongly said NO to, was
  re-decided YES (superhero) as a new decision. Checked: it left review and is in the approved library with its file.
