# BL-1617: the niche supply is gone; 6 editors, stopped at $0.72 of $15

## Answer card

| | |
|---|---|
| **New editors delivered** | **6**: football **4**, tennis **0**, movies **2** |
| **Total spent** | **$0.72** by the vendor's free balance read (346,659 → 345,452 = 1,207 requests). The ledger booked **$0.83** (1,390 calls). The 183 extra are HTTP 500 answers on hashtags that don't exist: the client counts them, the vendor doesn't bill them. So the ledger is $0.11 high, the safe side. |
| **$ per 1,000** | **$121** (6 for $0.724) |
| **Per source ($ per 1,000 new kept, pictures included)** | Snowball (tags from keepers' posts) **$70**, but it ran out of tags. Long-tail movies **$170**. Long-tail football **$156**. Long-tail tennis: 0 new emails in 49 calls. |
| **Why I stopped at $0.72** | Your rule: stop early once every source is above $60 per 1,000. The only source under that line, the snowball, ran dry: its third mining round found 1 new tag. |
| **Audit** | All 7 picture keeps were re-judged blind on fresh covers: **6 real editors (85.7%)**. That is under 90%, so I tightened: the 7th (AI-generated Star Wars images, not video edits) was dropped. **The 6 delivered passed both looks.** |
| **File** | `<PROFILE>\AppData\Local\ClippersHQ\operator\editor_emails_20261009_BL1617.xlsx` (6 rows) |
| **Also written** | master +6 through `crossdedup.append_leads` (run_id bl1617). Workbook: Emails 4,416 → 4,422, every other sheet unchanged, **MARK untouched**, backup sha-verified and vaulted. **No email was sent.** |
| **Checkpoints** | $5 and $10 were never reached. |

## 1. Snowball (the cheapest source), and why it ran dry

- **Keepers:** 140 from BL-1614/1615. 73 had their posts' hashtags stored in edits.db (free). The other 67 got one feed call each ($0.040) for their newest 30 posts' hashtags.
- **Tags:** 4,116 distinct. Only **43** were unwalked edit tags naming football, tennis or the movie pack. 71 more were already walked, and 399 edit tags named something else: TV shows, anime, non-pack films.
- **Wave 1:** 43 tags, 134 calls, 12 raw new emails, **3 kept**.
- **Round 2 mining** (from the new keepers' feeds): **0** new tags.
- **Round 3:** 1 mined tag plus 5 I picked from the unclassified list that are in scope (Hayden Christensen, Brian O'Conner, Harry Osborn, World Cup 2026, Lucas Bergvall). 21 calls, 4 raw new, **0 kept**.
- **Snowball total:** 232 calls ($0.139), 2 kept after the audit, **$70 per 1,000**.
- **The snowball closes on itself.** Editors in these niches use the same tags, and the four earlier rounds have already walked them.

## 2. Long-tail sources

| Source | Tags | Calls (walk + pictures) | Raw new emails | Kept | $/1k new kept |
|---|---:|---:|---:|---:|---:|
| Movies: single films, characters and actors of the 60-name pack | 191 | 567 | 27 | 2 | **$170** |
| Football: squad, young and smaller-club players (BL-1600 pack) | 228 | 521 | 4 | 2 | **$156** |
| Tennis: smaller players | 29 | 49 | 0 | 0 | — |

- **Drop rule:** each tag stopped after **2 pages with 0 new emails** (your rule), so most long-tail tags cost 2–4 calls.
- **The vendor answers HTTP 500 for a hashtag that doesn't exist.** Long-tail name lists hit many of those, and they tripped the vendor-health breaker twice (wave 2 at 20, wave 3 at 150).
  - They are not billed (see the money row).
  - I left the remaining ~750 tennis and football names unwalked. At 0.009 raw new emails per call, they could not come under $60.

## 3. Quality, exactly as BL-1614

- Text may only drop. Every keep needs a 6-cover picture judged by me, and unclear means drop.
- Earlier rounds' verdicts were reused, so no account was judged or paid for twice.
- **Pictures this round:** 33 accounts. 7 editors, 14 creators, 9 out of scope (memes, anime, TV reviews), 1 business, 2 unclear.
- **Audit:** all 7 keeps, blind, on newest covers, gave 6 editors. The 7th was dropped.

## 4. What this means

- Across BL-1614 to BL-1617, **every cheap source of football, tennis and mainstream-movie edit pages has now been walked.** That covers search, suggested, following, likes, comments, link pages, contact fields, account search, foreign-language tags, long-tail names, pro-tool tags and the snowball.
- The remaining cost is **$120–170 per 1,000 kept**.
- **The only sources still cheap are outside your rule:** the pro-tool "any niche" video editors (BL-1616: $4.84 per 1,000, 40 of 40 real editors). A wider niche would be another, for example anime or TV-show edit pages, which made up 399 of the snowball's unclassified edit tags.

## 5. Notes

- **Where the data lives.** Work data is in `%LOCALAPPDATA%\ClippersHQ\bl1617_work\`, never in the repo. The repo files hold counts only.
- **My stale claim.** My own BL-1616 claim was still open at the start. I closed it.
- **The tag ledger** (`email_harvest_tags.json`) records every tag walked this round, so none is paid twice.

Files: `scratch/bl1617/` (walk.py with the 2-dry-pages rule, mine.py, gen_movies.py, verdict.py, the BL-1615 tooling retargeted, PROGRESS.md and the JSON counts).
