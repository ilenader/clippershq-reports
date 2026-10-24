# BL-1701: Dusan 17:55 -- move LEADS, FIXER and APP to the 3090 (done by 19:00)

## What runs where now (24 Oct 18:10)
| work | where | since | measured |
|---|---|---|---|
| FIXER (window + its tests/patches) | 3090 | 23 Oct | relay on the PC forwards orders; CLIPPERSHQ_REMOTE_HOST=vast3090 made a persistent user setting 14:40, so a relay restart stays on the 3090 |
| LEADS vendor calls (LamaTok walks, following lists, feeds) | 3090 | 22 Oct 21:27 | 37,606 of the $50 run's 47,079 requests (80%); the other 9,473 were the 22 Oct afternoon runs from the PC |
| LEADS pictures (covers -> page sheets) | 3090 | 23 Oct | pics3090 |
| LEADS free picture path (profile embed covers) | 3090 | 24 Oct (BL-1700) | same videos as the paid feed |
| **LEADS eyes (Claude page checks)** | **3090, from today** | 24 Oct 18:05 | see below |
| LEADS window (the conductor) | PC | -- | stays, see below |
| APP (review app, friend link, library, Drive sends) | PC | -- | stays, see below |

## The eyes moved: every 3090 judge job had come back EMPTY since 22 Oct
Two faults in the farm judge job (`neuraltrack/build/work/finder/finder_judge_job.py`, ours):
1. it copied the sheets into a `/tmp` folder that `claude -p` on the 3090 did not see ("the files it names aren't in my
   working folder") -> the work folder is now inside the job's own output folder;
2. the 3090 hands inputs over under content-hash names (`f7720c6c....jpg`) while the prompt names `s0001.jpg` ->
   `judge89.py` now passes the original names (`--names`) and the job restores them.
Calibration on 10 sheets of run q4 (80 pages, 6 real editors by the final verdicts), as **2 helpers side by side**:

| look | where | pages | seconds | real editors kept | pages passed on |
|---|---|---|---|---|---|
| first look (Sonnet) | 3090 | 80 | 24 (2 jobs at once) | 6 of 6 | 16 |
| first look (Sonnet), the original | PC | 80 | -- | 5 of 6 | 13 |
| second look (Opus) | 3090 | 40 | 49 | 6 of 6 marked K | 2 others marked K |

Agreement 3090 vs PC first look: 70 of 80. Command: `python scratch/bl1689/judge89.py submit <run> --to vast3090
--per 5` (one helper per 5 sheets, all at once) -> `collect` -> the same merge77 files as before.

## What stays on the PC, and why (numbers)
- **LEADS window** (claude.exe, 425 MB): it is the only process that touches the lead data, which lives on the PC --
  raw_store 50.2 GB, raw_emails 6.9 GB, master_leads.csv, the dedupe guard, the Google sheets. Copying lead data to the
  rented 3090 is against BL-1682 (lead data stays home), and the relay cannot yet run HQ steps for a remote LEADS window.
  All its heavy work (calls, pictures, eyes) already runs on the 3090; what is left on the PC is light (dedupe, delivery).
- **APP**: the app (PID 18392) serves ports 8793/8794 to the friend over Tailscale from this PC, reads the approved library
  on F: and the review folder on D:, and sends to Drive. Moving it moves the library and the friend's link.
- To move these two WINDOWS too: the relay must carry roles other than 3_FIXER and get a small allowlist of HQ commands
  (run a named step on the PC, read back its result). That is 3 FIXER's tool; estimated 2-3 h with tests. Not done by 19:00.

## Searches in small batches
The next paid search (only on Dusan's yes, inside the daily cap) runs as several small batches at once on the 3090: the
tag list split into slices, one tag3090 / fol3090 process per slice with its own run name and its own share of the cap,
eyes as one judge job per 5 sheets. No search is running now.
