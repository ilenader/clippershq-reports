# BL-1657 -- free ($0) ways to get editor emails: tested, ranked

Order: office 1_LEADS 2026-10-16_1829 "Between runs, test free ways to get" (ALFRED for Dusan). Spend: **$0** -- no paid
vendor call; tools in their own venv (%LOCALAPPDATA%\ClippersHQ\bl1657_work\venv); every browser had its own temp
profile and was closed by its own handle. Counts only.

## Samples
- A: 40 confirmed editors WITH an email in the bio (can a free method recover it?).
- B: 40 confirmed editors with NO email in the bio (can a free method find a new one?). Only 82 such editors exist in all
  local verdicts (the walk keeps email accounts), so B is 40 of 82.

## Results (n = 8-40 per method, rough)
| method | tried | result | s/account | blocked? | unattended? | verdict |
|---|---|---|---|---|---|---|
| a. TikTok profile page, plain requests | 80 | 2.5% usable | 2.4 | JS WAF page with HTTP 200 | no | dead |
| a2. same page in headless Chrome | A25 B40 | A: 23/23 emails re-read; B: 0 new | ~4 | no (65/65 clean) | yes, ~900/h | works, re-reads known bios only |
| b. bio link, plain requests | 10 links | 1 email (already known) | ~4 | no | yes | weak |
| b2. bio link rendered in Chrome | 11 links | A: 2 known; B: 1 new (unverified) | 5.7 | no | yes (20 s timeout) | only free path to NEW emails |
| c. Instagram, same handle | 80 | 0 | - | 429 on the first 3 calls | no | dead |
| c. YouTube, same handle | 80 | 3 in A (known), 0 in B | ~2 | no | yes | useless |
| d. sherlock (15 sites) | 16 | 29 hits, 0 new emails | 33 | no | slow | dead (false positives) |
| e. free DISCOVERY: tiktok.com/tag, search page, TikTokApi | 2 tags, 1 search | 0 accounts | 40-68 | empty body / EmptyResponse | no | dead |
| f. DuckDuckGo / Bing site: queries | 10 | 0 | ~10 | DDG 202 on 5/5; Bing 0 TikTok results | no | dead |

Paid baseline for comparison: $25-35 per 1,000 first-world editors with an email (LamaTok walk, BL-1649).

## Conclusion
- **Free discovery is closed.** Logged-out TikTok tag/search feeds return empty bodies; only the paid walk finds new accounts.
- **Best $0 method:** enrichment of accounts we already hold -- headless Chrome (own temp profile) reads the profile
  (~4 s), renders the bio link (20 s timeout) and pulls an email; drop generic addresses (info@, support@).
  Expected ~900 profiles/h, ~10% have a link, ~1 in 4 loaded link pages shows an email: **~20 candidate emails/h,
  ~150-200 per night at $0 (+-3x)**. Risks: the WAF may tighten at volume (65 reads tested); emails unverified.
  Limit: it only squeezes more out of accounts already walked (the no-email pool).
- Lessons 20 + 21 added to office LESSONS.md.

Files: scratch/bl1657/RESULTS.md + m_*.py, build_samples.py. Raw per-account data only under %LOCALAPPDATA%\ClippersHQ\bl1657_work\.
