# BL-1663 -- sports / football editors from a fresh named-subject co-tag list: 111 editors (63 first world) for $2.39

Order: office 1_LEADS 2026-10-17_1215 (ALFRED for Dusan): start on the parts that need no new money, e.g. the hashtag
walk on sports/football. Money: what was left of Dusan's $30 hard cap ("Finder leads", wallet.json; base = LamaTok
request counter 191,812). Guard limit $29.50. **Spent: $2.39** (counter delta, $26.78 -> $29.17 of the $30). No paid
step after 13:55. The 13:37 budget rule ($5/day + what Dusan adds) came in during the last walk; the walk stayed inside the $30.
Counts only -- no handle, name or email here.

## What was done
1. Co-tags that confirmed editors use, not walked before: football 1,580, sports 647 (scratch/bl1663/tags63.py).
2. Sonnet sorted the tag text into named subjects (players, clubs, drivers, cars), then hand-pruned (World Cup words,
   common words, everyday car brands out): list a = 54 tags, list b = 187 tags (LESSONS 8: generic co-tags = junk).
3. Walked with clippershq/raw_emails.py (v1 hashtag pages, price line $10/1k new, caps $0.35-0.70 per list), detached
   (jobs bl1663_chain, bl1663_chain2).
4. Every new-email page -> covers -> page pictures -> 8-page sheets -> eye check: Haiku first look, Sonnet re-check of
   every sheet with an E or U (rubric scratch/bl1646/eyes46.js) -> verdicts -> deliver -> first-world cut (author.region).

## Results
| list | tags | new emails | editors (E) | first world | spend (walk + feeds) | $/1k editors | $/1k first world |
|---|---|---|---|---|---|---|---|
| football a | 28 | 541 | 34 | 21 | $0.48 | $14 | $23 |
| sports a | 26 | 174 | 22 | 16 | $0.57 | $26 | $36 |
| football b | 124 | 493 | 37 | 15 | $0.86 | $23 | $57 |
| sports b | 63 | 246 | 18 | 11 | $0.47 | $26 | $43 |
| **total** | **241** | **1,454** | **111** | **63** | **$2.39** | **$21.5** | **$38** |

Per-list spend is approximate (a list's feeds/pictures run while the next list walks); the total is the counter delta.
Editors are 7.6% of new email pages here (creators ~80%, business ~7%, game/anime/freelancer go to their own files).
No tag took more than 17% of a list's emails (LESSONS 7 check passed). The biggest tags were city-named clubs
(#marseille, #valencia, #memphis 8-17%) -- city names bring local creators, not editors.

## Files (operator home, never the Desktop)
- `operator\editors_football_20261017_firstworld_f1.xlsx`, `..._f2.xlsx` (21 + 15 first world) + `_other_countries`
- `operator\editors_sports_20261017_firstworld_s1.xlsx`, `..._s2.xlsx` (16 + 11 first world) + `_other_countries`
- all editors: `operator\{football,sports}_EDITORS_20261017_{f1,f2,s1,s2}.xlsx`; raw + creators/game/anime/freelancer side files next to them.
- Rows appended to his one workbook and master (deliver read-back ok on all 4).

## What we learned
- Named-subject co-tags of football/sports editors still pay: **$14-26 per 1,000 editors (all countries)**, about the
  BL-1649 price. First world is ~57% of them, so ~$38 per 1,000 first world.
- List a (the top-ranked tags) beat list b (the long tail) on first world: $23-36 vs $43-57 per 1,000. The tail is
  more South-American / African clubs -> fewer first-world editors.
- City-named club tags (#marseille, #valencia, #memphis) are mostly local creators. Cut tags that are also a city name.
- Common Crawl is not a free source of bios: CC-MAIN-2026-39 holds fewer than 3,000 rows for all of www.tiktok.com.
