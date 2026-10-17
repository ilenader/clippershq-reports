# BL-1665 -- 2,000 / 5,000 / 10,000 real editor emails per $30? Where the money goes, and what free tests showed

Orders: office 1_LEADS 2026-10-17_1337 (budget rule + goal) and 1449 (learning day, <= $10 per 1,000 real emails).
**Spent: $0** (all tests free; the $30 "Finder leads" budget stopped at $29.17 at 13:55, nothing paid after the
13:37 rule). Counts only -- no handle, name or email here.

## Today's price, measured (BL-1663, the best current route)
| | all countries | first world |
|---|---|---|
| best list (football a, top named tags) | **$14 per 1,000 editors** (~2,100 per $30) | $23 per 1,000 (~1,300 per $30) |
| whole round (4 lists, 241 tags) | $21.5 per 1,000 (~1,400 per $30) | $38 per 1,000 (~790 per $30) |

So 2,000 per $30 is already reached on the best lists when every country counts. 5,000-10,000 per $30
($3-6 per 1,000) is not reachable with any route tested so far.

## Where the money goes (one $30)
- **Walk ~70%** ($1.66 of BL-1663's $2.39): one hashtag page ($0.0006) = ~25 accounts with bio. New addresses cost ~$1.3-1.4 per 1,000.
- **Feeds ~30%** ($0.72): one paid feed call per new-email account, so its eye-check picture shows real covers.
- **The price is set by two rates, not by the vendor**: editors are **7.6%** of new email pages on named-subject
  tags (28-50% on small edit tags, but those pools are walked dry), and **only 1.75% of edit-named accounts put an
  email in their bio** (raw store: 66,094 edit-named accounts, 1,156 with an email). Proven editors from the review
  app: 255 of 5,126 (5%) have an email.

## Free tests today
| test | result | verdict |
|---|---|---|
| Web research: cheaper TikTok data vendors (TikHub, EnsembleData, ScrapeCreators, Apify, Bright Data, influencer DBs) | none is cheaper per bio than LamaTok; influencer DBs sell emails at ~$150-230 per 1,000 | no gain |
| Common Crawl (CC-MAIN-2026-39) as a free bio source | < 3,000 index rows for all of www.tiktok.com (TikTok blocks the crawler) | dead |
| Free bio-link read: 200 edit-named, 1k+ follower pages with no email (headless Chrome, own temp profile) | 196 read, 30 with a link, **2 new emails (1%)**, 17 min, no block | +~7 emails/hour, a top-up only |
| Instagram handle named in a no-email edit bio | 1,037 of 64,938 (1.6%) | small pool; ~$0.72 of IG calls to test (not run today) |
| Free covers from the web profile (to drop the paid feeds, -30%) | user JSON yes, post list EMPTY logged-out (12/12) | dead -- feeds stay paid |
| Stored bios with an email hint but nothing parsed | 418 edit-named (of 64,938) mention email/contact words with no address parsed; only 9 of all 64,938 even say "gmail" | tiny; the extractor already handles spaced and at/dot forms (bio_parser) -- the 418 were not read one by one |

## What could move the price (not yet proven)
1. **Cut the city-named and big-pool tags before walking** (BL-1663: #marseille, #valencia, #memphis brought local
   creators): the best list was $14/1k; trimming the tail toward it is the cheapest lever (~$10-14/1k all countries).
2. **Instagram business email for the 1.6% that name their IG** (~1,000 accounts in the store, ~$0.0007 each):
   a $0.10 test tomorrow inside the $5/day.
3. Cross-platform lookup of proven editors without an email (BL-1667): measured separately.
