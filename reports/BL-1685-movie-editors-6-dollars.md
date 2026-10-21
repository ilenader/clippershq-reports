# BL-1685 -- $6 for 1,000 movie editors, and the plan B test

Orders (Dusan's HELM chat 21 Oct, relayed by ALFRED): 11:08 "spend up to $6.00 to find 1,000 NEW good editors with
email in the movie niche"; 11:21 "YES to plan B: $0.35 test first, then up to $3.40 more ($3.75 max), on top of the $6".
**Money: $0.3453** (plan B test). The $6 is untouched: the wallet has no line for it yet, and the test says no route
we have measured gets near $6 per 1,000.

| | Result |
|---|---|
| **1. Plan B test** | 500 approved no-email editors (fixed shuffle of the 4,673 left after a free cut) -> 500 HikerAPI profile calls for the Instagram with exactly the TikTok handle: **144 exist, 7 show a NEW e-mail** ($49 per 1,000 e-mails). |
| **2. Strict check** | TikTok page picture from the edit app's own stored covers ($0) + the Instagram facts; two blind readers (Opus, Sonnet) with STRICT83 + a same-person code; 6/7 agree, 1 split by my own look. **2 good** (both faceless edit pages, same editor on Instagram). The rest: 2 creators (own face), 1 golf academy, 1 anime page, 1 too empty to judge. |
| **3. Price** | **$0.3453 / 2 = $173 per 1,000 good editors.** The plan's stop line was $60, so the other $3.40 was not spent. Sample is small (7), but even 6 of 7 good would have been $58. |
| **4. Why** | An approved video does not make an editor page (5 of 7 pages were not edit pages), and people who show an e-mail on Instagram lean to creators and businesses. |
| **5. Free cut before paying** | `pre85.py`: 171 Spanish-caption pages + 1 photo page dropped from the plan B pool from stored captions ($0). `accounts.verified` in edits.db is 1 on 15,638 of 47,802 accounts, so it is NOT TikTok's blue check and was not used. |
| **6. The $6** | 1,000 for $6 is not reachable: plan A's $5.90/1k route had 271 accounts and is used up (it grows only by a slow free read of new editors' tags, a farm-PC job); movie hashtag walks cost ~$150-300/1k under the strict rules (BL-1683: movie tags ~3x football, $65-140/1k all niches). Asked Dusan: (a) $6 on small movie edit-tag walks for ~20-40 good editors, or (b) keep it. |

Delivered: `operator/editors_planb85_20261021.xlsx` (2) -> "New emails - never sent" (+2, 786 rows).

## Files

- `scratch/bl1685/igb85.py` plan / run / score (plan B; `--pool raw` = the 27,016 edit-named movie/TV no-email pages, not run).
- `scratch/bl1685/pre85.py` free pool cut; `chk85.py` pages / collect / deliver; `pagesraw85.py` TikTok pages for raw-pool finds (not run).
- Work data (private, not in git): `%LOCALAPPDATA%\ClippersHQ\bl1685_work\`.
