# BL-1660: a video with longer sound than picture was called "broken"; the length is now the picture's ($0)

Follow-up to BL-1659. 2 APP checked the AI reviewer's first decisions on the 7 videos sent back to review. 6 got a normal
look (5 unsure for the friend, 1 sure NO). The 7th was **"broken" again**, in 31 s, so not a timeout.

## Card

| # | Item | Result |
|---|---|---|
| 1 | **Cause** | The file is fine: a clean full decode, but its **picture is 121 s long and its sound 271 s**. `probe()` took the length from the whole file (271 s), so `analyze()` expected ~2x the frames it got and called it broken. The Flashcut farm sheet job has the same file-length check, which is why it returned 0 pictures for this video 3 times (and for the other 4-min one). |
| 2 | **Fix** | `clippershq/edits_ai_review.py` `_probe()` also reads the video stream's duration and uses it when it is shorter than the file's. A container without a stream duration (webm) keeps the file's. The Claude lane gets it too (`sheets()` uses `AI.duration`). The farm job `neuraltrack/build/work/finder/finder_sheets_job.py` (2 APP's file, BL-1654) has the same fix. |
| 3 | **Proof** | The real file now: 120.8 s, 600 frames decoded, sheet made, no problem (12.4 s). Test +1 in `tests/test_bl1637_ai_review.py` (271.5 s file with 120.8 s picture -> 120.8; webm with no stream duration -> file length): 23/23; 1639/1641/1642/1647 all OK. |
| 4 | **Older cases** | Every AI "broken" row left: 2, both the BL-1659 videos already corrected to YES. Nothing else to undo. |
| 5 | **Live** | `restart_app` again (new server answers 8793 + 8794). The video's AI row (backed up in `scratch/bl1660/before.jsonl`) was cleared so the reviewer looks at it again at once. Its 21:53 NO had never moved it (still in review). The new look at 22:00 is a real look: **unsure** (models asked, 20 s), so it stays in review. |
| 6 | **Farm proof** | The 2 long videos the farm returned 0 pictures for 3 times: after the farm-job fix, **2 sheets, 0 unreadable** (finder-sheets-1016220106-1, 8.7 s). They go through the normal Claude lane. |
