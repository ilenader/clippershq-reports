# BL-1723 -- next editor batch (b23_face31) + ONE sheet, 1 Nov 2026

Orders: 1_LEADS 2026-10-31_2340 (numbers), 2026-11-01_0013 + 0020 (next batch, $5 line, free methods), 0216 (farm bounce),
1249 (Dusan: one sheet by 18:30, 1,000 good/hour). Nothing was sent (docs/NO_SEND.md). Vendor money: $0.

## Result
| what | number |
|---|---|
| pages queued (old-list TikTok accounts the text judge called "not editor", never sent, in no file, never picture-checked) | 67,998 |
| pictures read on the 3090 (TikTok embed + avatar + 9 covers) | 67,058 |
| judged by Haiku on the 3090 (2,868 jobs, 8,442 sheets) | 67,032 |
| F = faceless edit page (kept) | 4,342 (6.5%) |
| C own face / creator | 53,989 |
| X not edit / B business / P pet / U unsure | 5,232 / 2,841 / 529 / 99 |
| NEW_editors_after_29_Oct.xlsx | 1,301 -> 5,644 (+4,343) |
| overlap with frozen ALL file / sent list (28 Oct 20:30, 4,791) | 0 / 0 |
| cost per good e-mail | $0.00 (Claude Haiku on the 3090 sign-in only) |

F% by text-signal band: score 1 = 5.6%, 2 = 13.7%, 3 = 7.8%, 5 = 9.7%, 6 = 16.5% -- the edit-word score barely predicts.

ONE sheet (`Desktop\Tools\ALL_editors_ONE_SHEET_1_Nov.xlsx`, scratch/bl1723/onesheet31.py): 10,025 good editor e-mails,
8,892 never sent, 1,133 already sent (marked from `Downloads\all emails that were sent.xlsx`). 844 rows left out because the
same e-mail sits in a reject tab; **43 of them are rows of the frozen ALL file** that are the 26 Oct fake '.ae/.cc' handles.

## Speed (Dusan: 250/h too slow, goal 1,000/h)
- 00:16-12:56: 8 readers on the 3090, 2 Haiku lanes: ~4,700 pages/h, ~270 good/h.
- 12:56-16:45: 16 readers, 4 lanes, file every 5 min: ~7,700 pages/h, ~320 good/h (lower-signal pages at the end).
- The "15-28 min stall" of the file = the apply loop wrote it every 30 min; now 5 min.
- Fixed on the way: farm-queue bounce (judge89 submit --nofarm), O(n^2) handle list, old failures re-tried before new pages,
  verdicts() opening a sheet map per answer line (~70k opens: apply > 15 min on a busy disk -> ~3 min).
- **Limit is supply, not checkers:** every e-mail Finder ever found (116,333 in the all-time sheet) has now had a text and/or
  picture check. 1,000 good/h needs ~15,000 new e-mail pages/h = paid walks (~$250/h at $17.60 per 1,000 e-mails). The $5/day
  wallet buys ~280 good editors per day.

## Code
- scratch/bl1723/face31.py -- run b23_face31 on top of face29b (own ids/sheets); prep / pipeline / apply / rate.
- scratch/bl1689/judge89.py -- `submit --nofarm` (job file stays local; podjudge23 rebuilds the cmd).
- scratch/bl1723/onesheet31.py -- the ONE sheet.
- %LOCALAPPDATA%\ClippersHQ\bl1723_work\apply_loop31.py -- `--every SECONDS` (stopped: STOP_APPLY31).
