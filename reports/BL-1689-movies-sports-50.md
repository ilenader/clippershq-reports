# BL-1689: Dusan's $50 for movie + sports editor e-mails (22 Oct) - paused at $6.00 under his 70% rule

**Orders:** 1_LEADS 1643 (Dusan HELM 16:43: $50 hard cap, 1,000-2,000 new movie + sports editor e-mails, $2 test first,
report every $10), 1850 (stop the test method), 1916/1939/1951 (A20/A24: rest the old way; pause if fewer than 70% of new
e-mails are real editors; editor check in the 1 LEADS window while the farm Claude account is blocked).
Wallet line "Finder leads 22 Oct (movies + sports)" $50; $10.14 booked; **$6.0012 spent** (LamaTok counter 128513 -> 118511).
Paid walks ran on Dusan's PC under his written exception (bl1689_work\HQ_OK.txt, his 16:43 words).

## Result
- **990 new e-mails** (none in any older lead file), **123 real movie/sports editors delivered** (strict check) =
  **$48.8 per 1,000 real editors**; **13%** of the new e-mails. Dusan's 70% line is not reached by any route, so the run is
  paused with $44.00 unspent.
- Delivered: `operator\editors_bl1689_real_20261022.xlsx` (sheet Editors) + "New emails - never sent" sheet +123 (909 rows).
- Dusan's own look at the 102 test e-mails (Desktop\Tools\Finder test 22 Oct - 102 new emails.xlsx): about 90% content creators.

| route | new e-mails | first look K | strict good |
|---|---|---|---|
| test: 60 never-walked movie edit tags | 60 | 9 (15%) | 7 |
| test: 100 new sports name tags (<name>edit) | 42 | 15 (36%) | 14 |
| 241 sports name tags | 88 | 21 (24%) | 19 |
| 550 movie edit tags (co-tags of editors) | 201 + 162 | 27 + 17 (12%) | 22 + 12 |
| 167 movie/anime name tags | 70 | 9 (13%) | 5 |
| 277 movie edit tags (stopped at 18:51) | 39 | not processed | - |
| partners of proven editors (116 pages, $0.14) | 16 + 124 | 10 + 25 (25%) | 9 + 21 |
| re-walk of 151 proven-editor tags (stopped, $0.56) | 227 | 22 (10%) | 13 |

First look = Sonnet, `scratch/bl1689/RUBRIC89.md` (RUBRIC77 without the Spanish reject: Dusan 18:25). Strict = Opus on every
K/U page + photo share > 70% out (`scratch/bl1677/merge77.py score`). The rest of the pages: content creators 269+,
anime/games/business 193+, singers 24+.

## What I got wrong
- I scaled the $2 test on **cost per new e-mail** ($7.15/1k) before any editor count. The headline must be cost per GOOD
  lead. Movie/TV character edit tags were already known as fan/creator pools (BL-1656) and I walked 887 of them.
- The old way's share was checkable for $0 before spending (20 Oct eyes: 12-15% K) - done for 1916, and it held (10% today).

## Tools (scratch/bl1689/)
- `prep89.py` never-walked candidate tags (global + own ledgers); `combo89.py` + `names89*.txt` named <name>edit/edits/4k tags.
- `test89x.py` the 102-test Excel; `deliver89.py` strict-good editors -> operator Excel (header `email`, sheet `Editors`,
  so `new_emails_sheet.py push` picks it up).
- `judge89.py` + neuraltrack `build/work/finder/finder_judge_job.py`: editor check as a FARM Claude job (sheets in a temp
  folder on the farm PC, deleted after; only `sNNNN n: K` lines come back). Works in a local tool test (8 lines / 23 s);
  on the 3090 it returned empty (farm Claude account blocked, per Dusan 19:51). Ready for when the farm account is back.
- `wait89.py` bounded waiter (540 s), `restamp89.sh` re-stamps WAITING status lines.

## Open
- Dusan/ALFRED: how to go on with the $44.00 (no route reaches 70% of new e-mails; best = partners of proven editors, pool
  used up today; refills of proven tags in 2-3 days). 1916 asks a (70% of the checked list) / b (keep the money).
