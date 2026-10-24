# BL-1708 -- one-page plan: a cheap new seed source (free test first, ONE paid test <= $0.60)

> **HQ numbers (1 LEADS, 25 Oct 01:05, $0; council order 00:46):**
> - **Follow-list seeds left: 229** checked e-mail editors not yet walked (of 970; 741 walked) -- and most of those 229
>   were PRIVATE lists at the last free check, so ~0-30 usable. Also 2,023 public lists read only on page 1 (deeper pages
>   measured $12.4 per 1,000 good on 24/25 Oct, n5).
> - **Free covers vs paid labels: 92.9% match** (92 of 99 pages judged on paid-feed pictures on 23 Oct, re-pictured free from
>   the TikTok profile embed on 25 Oct, same Sonnet + Opus eyes): 36 of 39 paid-good stay good, 4 of 60 paid-not-good turn
>   good. Part of the gap is two days of new posts.

Written by 3 FIXER on the 3090, 24 Oct night. Code and counts only: no data, no handles, no keys on this machine.

## What the free fixes need (3 FIXER has no data here)
1. Crash-safe saving: read in the repo, not changed. The writers that matter for the lead stores already use temp file + `atomic_io.replace` (crawl_suggested append to master, edits_db, state, edits_scope). The direct `open(..., "w")` calls I found are test fixtures or one-line flag files (`run.stop`, `run.pause`). So I cannot name a real crash-unsafe result path from code alone. To go further I need the council's actual failure (what was lost, in which run). Not guessed.
2. Cover check against the paid labels: needs the paid label file and the cover files, both on HQ. Not available here. I can write the compare script as soon as HQ names the label file and its columns.
3. Seed count of the follow-list seeds left: needs the seed file and the already-used list on HQ (`suggest_harvest.load_seeds` reads one handle per line / JSON list). Count = distinct seeds minus seeds already walked. Not available here, so no number is given.

## The seed source: Instagram hashtag "popular" pages, read headless, no login
Measured on the 3090 tonight, $0 (counts only):
- `/explore/tags/<tag>/` renders with no login wall and shows 12 posts with the author named on each; 20+ famous profile pages and 30+ more pages answered with no block, no 429.
- Tag -> authors -> profile render (bio, covers) worked for every author tried: of the first 6 niche tags, 8 profiles each rendered 8 of 8; bio e-mail found in 1, 0, 3, 0, 1, 1 of 8 (6 of 48 = 12.5%). Time: about 6 s per page plus the 30 s spacing, so about 100 pages an hour from one IP.
- Edit-page share and bio links are still being counted (the bio-link counter was wrong and is reported as unreliable); full 10-tag numbers come in the IG-pipeline reply.
- Cost today: $0. Compare the paid follow-list route: `PRICE_PER_CALL_USD` 0.00069064 per call, about 2 calls per seed + 1 per candidate (`suggest_harvest.estimate`), and the repo's own note says that route gives net-new supply but NO e-mail lift (26.7% vs 24.5% control).
- Caveat: only about 12 authors per tag per visit. Supply per hour is therefore about 8 profiles x 100/9 pages = roughly 90 profiles/hour, of which about 12% show a bio e-mail = about 10 e-mails/hour from one IP, before the editor check.

## Free test (do this first, $0)
Run the pipeline script (work/igtest/pipe5.py) on 20 more niche tags, 8 authors each, 30 s spacing, stop at the first wall. Then HQ (not me, no data here) checks how many of the authors are NEW against the master (net-new share) and how many bio e-mails pass the existing e-mail checks. Pass line: net-new >= 70% and e-mail rate >= 10%. Fail: stop, no paid test.

## ONE paid test, at most $0.60, only on Dusan's yes, only if the free test passes
- Purpose: judge whether the free route's authors are real EDIT pages without a human, using the paid labels the project already has.
- What: take the free route's net-new authors (up to 870 calls fit in $0.60 at 0.00069064 per call) and run only the existing paid profile call + cover label on the ones with a bio e-mail. Everything else stays free.
- Measure: of the paid-labelled authors, share labelled EDITOR/LIKELY, and cost per labelled editor with an e-mail. Pass line: the all-in cost per 1,000 good editor e-mails is projected under $10, using the free-route supply rate above.
- Hard stop: `tools/money_guard.py` cap $0.60, the harvest `Budget` class (`cap_usd=0.60`), stop at the cap, never above.
- Honest limit: nothing here shows $10 per 1,000 is reachable yet. The tag route is free for supply, but the cost sits in the paid label and any e-mail verification step; the free test above shows the supply, the paid test shows the cost. Only both together decide.
