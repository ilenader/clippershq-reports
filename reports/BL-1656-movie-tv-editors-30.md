# BL-1656 -- more MOVIE & TV editors + clippers, $30 hard cap: 490 first world (+86 less sure) for $26.66

Order: office 1_LEADS 2026-10-16_1829 "New Dusan budget: $30, hard cap, never" (ALFRED for Dusan). Money: Dusan's own words,
HELM chat 16 Oct 18:28: "we need even more leads. You can do 30 dollars more we need more clippers ... Just focus more on
movies ... any movies or TV show editor". Counts only; nothing is sent (docs/NO_SEND.md).

## Money (vendor counter, the only truth)
- LamaTok request counter 191,812 (16 Oct 18:31) -> 147,375 (17 Oct 04:14) = 44,437 x $0.0006 = **$26.66 of $30.00**.
- Every walk went through a chain guard that reads the counter before each walk and refuses when spent + walk cap + feed
  reserve would pass $29.80; one paid walk at a time (chains 2-4 waited for the previous chain to stop walking).
- $3.34 left unspent: the last movie lists had run out of tags worth walking.

## Delivered
Drive folder **"Leads - 17 Oct"** (anyone with the link; 4/4 files size + sha256 checked; link in the office reply):

| file | first-world editors | cost (share of $26.66) | $ / 1,000 first world |
|---|---|---|---|
| Leads 17 Oct - Movies & TV | 194 | ~$13.91 | ~$72 |
| Leads 17 Oct - Clippers (edit pages of athletes, singers, celebrities) | 296 | ~$12.75 | ~$43 |
| ... - Movies & TV - less sure (second look) | 38 | $0 | - |
| ... - Clippers - less sure (second look) | 48 | $0 | - |
| **total** | **490 sure + 86 less sure = 576 unique** | **$26.66** | **$54 sure / $46 all** |

- First world = US, Europe, CA/AU/NZ by the account's v2 region. 0 repeats of the 15 Oct Drive files (checked by handle
  and email); the walk itself never re-buys an address already in master, the workbook or any operator file.
- Local copies: operator\leads_17_oct\; waves operator\editors_{movies,clippers}_20261017_firstworld_b*.xlsx.

## What was walked (19 walks, 3 lists types)
Tags = hashtags that >= 2 confirmed editors (1,962 movie-side, 506 football, 102 sports) use in their own captions, never
walked before (5,308), cut by 4 Sonnet classifiers into: movie/TV subject (533), other named subject (1,353), non-Western
(51), drop (rest).

| list type | walks | first world | $ / 1,000 first world |
|---|---|---|---|
| movie/TV title + "edit" (tv_e) | 2 | 17 | ~$55 |
| bare movie/TV titles, characters, actors (tv_k) | 5 | 140 | ~$67 |
| title + edits / scenepack / scenes (tv_v) | 6 | 37 | ~$97 |
| other named subjects = clippers (cl_k) | 6 | 296 | ~$43 |

(per-walk cost = walk spend + feed calls, scaled to the counter total; the per-run sums over-count by ~12%.)

## Learned
1. Movie/TV editors cost ~2x other editors: on bare title tags ~85-90% of pages are FANS filming themselves (reaction,
   cosplay, nostalgia: #meangirlsday, #juryduty, #dancingwiththestars). Big tags (60+ accounts) were 1.9% editors, tags
   with <= 10 accounts 7.3%.
2. "title+scenes/scenepack" tags are mostly empty or fan clip pages too -- no better than bare titles.
3. A text pre-filter (edit words in handle/name/bio/captions) before the paid feed step keeps only 52-62% of editors
   while still paying for 24-32% of the others: it saves less than it loses (measured over 44,204 judged pages).
4. Clippers lists fade by list 5-6 ($64-85 / 1,000) and carry concert / festival / Latin-African music fan tags; cut
   those tags before walking (done for lists 3-8: 969 of 1,061 kept).
5. The free second look at "unsure" pages added 125 editors (86 first world) at $0.

Scripts: scratch/bl1656/ (tags56, lists56, variants56, chain56 with --after-log, process56, done56, unsure56, merge56,
up56, textcut56, tagrate56, cost56). Progress log: scratch/bl1656/PROGRESS.md.
