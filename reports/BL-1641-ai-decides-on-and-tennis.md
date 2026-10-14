# BL-1641: "AI decides" is ON; 100 tennis asked, 1 real tennis edit sent -- tennis edits are scarce, and the library's "tennis" was mostly other sports

2 APP order `2026-10-14_1510_P1-AI-decides-ON-and-100-tennis` (owner 15:06: "I want AI to decide and give me, let's say,
100 ... do tennis").
Money: **LamaTok $2.61 of $3** (tennis-page walk $0.11 + tennis discovery $2.50). **OpenRouter ~$0.25** (the AI judging
~400 videos, the send's niche check).

## Card

| # | Item | Result |
|---|---|---|
| 1 | **Sent** | **1 tennis edit.** Drive folder "ClippersHQ Sends / Tennis 2026-10-14 (1)", anyone with the link (the link is in 2 APP's reply, not here) |
| 2 | **Why 1, not 100** | (a) The library's 8 local "tennis" videos were filed by the PAGE's hashtag. The send's picture check found 7 of them were UFC, superhero, gaming, football x3 and basketball; they were relabelled to what they show (BL-1636 gates working as built). (b) The 398 older "tennis" rows exist only in the old Drive account (no file on this PC). (c) New tennis supply is mostly raw match clips, creators, and football edits that tennis tags pick up. Haiku's first look calls only 11 of 255 waiting "tennis" videos a tennis edit. |
| 3 | **"AI decides"** | **ON** since ~15:25 (Settings API). Only sure verdicts are carried out, as reviewer "ai", BACK works. So far: **17 YES, 98 NO** carried out. **0 of them tennis**: no tennis video had all looks sure and agreeing. |
| 4 | **Re-queued** | **101** tennis videos the friend had said NO to on out-of-scope days were put back in review (`edits_review.undo`, reviewer `requeue_tennis`). The AI took 21 sure NO (creators, podcasts); the rest wait for the friend. |
| 5 | **Paid supply** | Walk of his **184** approved tennis pages: 186 calls, $0.11, 30 viral videos. Then `edits.py job --tennis 91 --budget 2.5`: 4,163 calls, $2.50, **1,485 new tennis pages**, 271 videos into review. |
| 6 | **Waiting for the friend** | **255 tennis videos** (266 in all). Anything he approves can go out with the next Send. |
| 7 | **Fixed on the way** | (a) `job` refused under the go-live rules (it read the old Drive switch); it now needs only "Download videos for me". (b) Sure verdicts made in shadow are carried out once "AI decides" goes on. (c) **3 FIXER found** AI YES videos filed under the page's niche (tennis) although the AI saw football / UFC. An AI YES now takes the niche it saw before it is filed, and the 5 misfiled rows were moved. (d) The job's "queue idle" check hung after the reviewer was upgraded mid-job (it compared rows with its old version). It now checks "every waiting video has a review". The stuck job (budget already spent) was stopped by its own PID. |
| 8 | **Tests** | `tests/test_bl1641_tennis_job.py` (2) + new cases in `tests/test_bl1637_ai_review.py` (shadow verdicts carried out; filed by the niche it saw). `run_all -k test_bl1631*,1636*,1637*,1639*,1641*,1642*`: **6/6 green, 52 checks**. One earlier red of `test_bl1636_send_gates` was the live discovery run booking into the shared ledger during the test. It is green once the run stopped. |

## What the owner can do
1. Ask the friend to go through the **255 tennis** waiting (Approve videos). Then "send N tennis" again.
2. If you want Claude to eye-check the ~30 most likely tennis edits instead, say so. It is not done now: you asked for
   the AI to decide, and hand approvals would blur the AI's score.

- 17:50 FINDER BL-1641 AI decides ON + tennis: 1 real tennis edit sent (7 library "tennis" were other niches), 255 tennis wait for the friend, LamaTok $2.61 (DONE)
