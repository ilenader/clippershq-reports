# BL-1624: TikTok editor money audit: every cent is accounted for; the price is set by a 2.2% email rate, not by waste

## Card

| | |
|---|---|
| **1. Total spent, and $ per delivered editor** | **$21.34** on TikTok editor emails from BL-1614 to BL-1623: LamaTok $20.61 by the vendor's balance reads, OpenRouter $0.72, TikHub $0.01. **382 faceless editors delivered = $55.9 per 1,000.** Counting the 156 freelancer and any-niche editors too: $39.7 per 1,000. |
| **2. Where it went** | Hashtag pages **$12.55** · tag lookups **$6.15** (one call per tag to turn its name into an ID; $0.72 of it on tags that don't exist) · feed (profile) checks **$1.67** · probes and tests **$0.22**, plus judge calibration $0.62 (OpenRouter, one-off) · retries, 5xx and 427 throttles **$0** (never billed) · unexplained **$0.03** |
| **3. The unexplained requests** | **Found.** Only 43 of 34,356 billed requests are left over. BL-1622's "~423 unexplained" were **396 tag lookups** plus 18 small ones. The meter runs ahead of the bill only by 5xx and 427 answers, which the vendor does not bill. |
| **4. The biggest hole** | **Walking thin tag pools: about $26 per 1,000 delivered.** BL-1619 spent $14.89 (72% of everything) for 170 editors, at 0.084 emails per page. Second: **tag lookups, about $16 per 1,000**. Tags now last only 1.5–2 pages, so a lookup is a third of every walk. |
| **5. Lowest realistic $ per 1,000 after fixes** | **About $13.5–20 per 1,000 faceless.** Under $10 is impossible on TikTok hashtags: only **2.2% of new accounts have an email in their bio**, the same 2.2% (963 of 44,611) as the edit app's own proven edit pages, and only **about 20%** of those are faceless edit pages. |
| **6. The one change to make first** | Make the walker's own stop rule **"a source stops after $0.30 once its $ per eye-checked editor is over the line"**. BL-1619 would have stopped about $10 earlier. |

**Read-only, $0:** no vendor call (not even a balance read), no config change. Every number below comes from records already on disk.

## Your decisions

| | Question | My recommendation |
|---|---|---|
| A | TikTok faceless can't get under about $13.5 per 1,000 with hashtags. | Accept about $15–20 per 1,000 for the best niche (celebrities), or take faceless editors from a source where emails are 7× more common (YouTube showed 15% of channels). |
| B | The edit app's stored bios give about 38 email accounts a day, free. | Re-mine them every day at $0 (about 2–5 faceless a day). |

## 1. Every cent, BL-1614 to BL-1623

**Billed requests by kind** (1 request = $0.0006), reconciled to each round's own balance reads:

| Round | Billed (balance) | Pages | Pages lost in crash | Tag lookups (found) | Lookups for tags that don't exist | Feed / picture / audit | Probes, tests | Residual | Faceless delivered | $ per 1,000 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| BL-1614 | 3,225 | 2,776 | 0 | 131 | 0 | 252 | 69 | −3 | 119 | $16.3 |
| BL-1615 | 2,038 | 1,729 | 0 | 150 | 0 | 158 | 0 | 1 | 21 | $58.2 |
| BL-1616 | 425 | 0 | 0 | 0 | 0 | 360 | 61 | 4 | 0 (84 any-niche) | — |
| BL-1617 | 1,207 | 692 | 0 | 405 | 0 | 107 | 0 | 3 | 6 | $120.7 |
| BL-1619 | 24,818 | 13,093 | **1,467** | 7,885 | **1,165** | 1,043 | 146 | 19 | 170 | $87.6 |
| BL-1622 | 1,574 | 792 | 0 | 369 | 27 | 368 | 0 | 18 | 62 | $24.6* |
| BL-1623 | 1,069 | 364 | 0 | 117 | 6 | 488 | 93 | 1 | 4 (+72 freelancers) | $160 (faceless) / $8.4 (any editor) |
| **Total** | **34,356** | **19,446** | **1,467** | **9,057** | **1,198** | **2,776** | **369** | **43** | **382** | **$55.9** |

\* BL-1622 includes its OpenRouter judge.

- **Not billed, measured from the balance reads:**
  - Retried 5xx: 23 in BL-1615 and 520 lookups in BL-1619.
  - 500s on tags that don't exist: 183 in BL-1617.
  - Unbilled 5xx and 427 answers the meter counted: 34 in BL-1622 and 24 in BL-1623.
  - Each time, the meter or ledger ran *ahead* of the balance by exactly that count. Retries cost $0.
- **Pages lost in the crash.** The 10-10 power cut zeroed the tag ledger. BL-1619 rebuilt 668 tags by hand with pages = 0, so the 1,467 pages bought for them aren't in the ledger. They are not missing money: the walk's booked total minus everything else equals them.
- **Lookups for tags that don't exist.** The vendor answers "200, no hashtag id", which *is* billed: 1,165 in BL-1619 ($0.70), mostly speculative name variants.
- **Is one call ever more than one request?** **No.**
  - The BL-1623 page-size test made 2 calls and the balance fell by exactly 2. A 50-item page is still 1 request.
  - BL-1623's 1,068 explained calls met a balance drop of 1,069; BL-1615's 2,037 met 2,038.
  - The vendor's spec (`openapi.json` v1.4.5) has no per-endpoint price, only a link to its pricing page.

**OpenRouter (judge):**

| | One-off calibration | Judging accounts |
|---|---:|---:|
| BL-1622 | $0.5201 | $0.0485 live (430 judged = $0.11 per 1,000) + $0.0117 strict re-check |
| BL-1623 | $0.101 | about $0.039 TikTok (366 judged, $0.11 per 1,000); YouTube $0.017 is not counted here |

## 2. The funnel in cents

**BL-1622 hashtag sources** (free sources excluded), all eye-checked:

| Step | Count | $ per 1,000 at this step |
|---|---:|---:|
| Tag lookups + pages | 351 + 711 | — |
| Items on those pages (≈ accounts) | ~14.6 per page | — |
| New authors (not his, not seen this round) | 57% of items (6,475 of 11,397) | — |
| New with a new email | **140 = 2.2% of new authors**, 0.18 per page | **$5.24** |
| Passed views / recency / photos | 124 | $5.91 |
| AI judge keep | 43 | $17.05 |
| **Eye-real faceless** | **26** | **$28.20** |

**The step that multiplies the price is "new author → has an email"**: 2.2%. After it, only 26 of 140 email accounts (18.6%) are real faceless editors.

**By source (BL-1622), $ per 1,000 eye-real:**

| Source | $ per 1,000 |
|---|---|
| Celebrities | **$17.5** (0.29 emails per page) |
| Movies names | $29.9 |
| UFC | $33.8 |
| NBA | $36.3 |
| F1 | $129 |
| Football, tennis | 0 delivered |

BL-1623 community tags: $1.12 per 1,000 emails found, but **$137 per 1,000 faceless** ($7.62 per 1,000 freelancers).

**What the owner's arithmetic misses** ($0.0006 / 15 accounts = $0.04 per 1,000 accounts):

| | Per page |
|---|---:|
| Items | 14.6 |
| … already his, or already seen this round | −43% → 8.3 new |
| … with an email in the bio | × 2.2% → **0.18** |
| … real faceless edit pages | × 18.6% → **0.034** |

That's **29 pages per delivered editor = $17.6 per 1,000 from pages alone.** Add 0.5 tag lookups per page (+$8 per 1,000) and the feeds and judge (+$3 per 1,000), and you reach the measured $28.

**The specific checks:**

| Question | Measured |
|---|---|
| Pages bought twice | **About 0.** Every walker skips a tag already in the ledger under either key. The one ledger loss (the BL-1619 crash) was rebuilt over-marked on purpose, so nothing was re-bought. |
| Share of each page he already has | 43% of items are already his *or* already seen this round (BL-1622: 11,397 → 6,475; BL-1623: 33–35%). The two can't be told apart from the rows kept. |
| Feeds lost to the views / recency gate | 137 of 628 hashtag feed checks (22%) = $0.08, about **$0.4 per 1,000**. **No free follower filter:** the hashtag payload's follower count is **0 on 628 of 628**. The item's own play count and date are in the payload but weren't saved, so it can't be tested from records. |
| Feeds for accounts the judge then dropped | A free "edit word in handle / nickname / bio" filter would have dropped 328 of 345 judge drops, **but also 18 of the 30 eye-real faceless editors (60%)** and 31 of 72 freelancers. **Not viable.** |
| Older rounds' email accounts | Delivered: BL-1614 119 / 415 (29%), BL-1619 170 / 2,277 (7%). BL-1619's drops: creators 644, out-of-niche 528, out of scope 260, person names 391, unclear 172. |
| The edit app's own discovery | It has spent about $21.9 (BL-1599/1600/1601/1602 + EDITS + APP). It stores **44,611 accounts, 963 with an email in the bio (2.2%)**; last week about 6,800 new accounts and 268 with an email (about 38 a day). BL-1622 delivered **33 faceless from 245 new addresses there at $2.04 per 1,000**: its money was already spent. |

## 3. The holes, ranked

| # | Hole | $ lost | $ per 1,000 delivered (overall basis $55.9) | Proof | Fix | After the fix |
|---|---|---:|---:|---|---|---|
| 1 | **Walking thin tag pools** | about $10.1 | **about $26** | BL-1619: $14.89 for 170 at 0.084 emails per page, vs 0.18 (BL-1622) and 0.23 (BL-1614). At BL-1622's rate those 170 cost $4.8 | Stop each source after $0.30 once its **$ per eye-checked editor** is over the line (BL-1623 did this by hand; BL-1619's stop used a raw-email estimate) | Overall → about $30 per 1,000 |
| 2 | **Tag lookups** | $6.15 | about $16 (BL-1622 alone: $8.1) | 9,057 found + 1,198 no-tag lookups. Pages per tag fell from 21 (BL-1614) to 1.5–2, so lookups are 34–73% of walk calls | Fewer speculative name variants; take tag IDs **free** from items already bought (caption hashtags carry them); prefer deep tags | BL-1622 → about $20 per 1,000 |
| 3 | Non-editor email accounts | $0.08 in BL-1622 | about $3 | 114 of 140 fed email accounts were not real faceless | None free: a text filter loses 60% of real editors | — |
| 4 | One-off tests and calibration | $0.84 | about $2.2 | Probes $0.22 + judge calibration $0.62 | One-off; don't repeat | — |
| 5 | Views / recency gate fails | $0.08 | about $0.4 | 137 of 628 feeds | Save the item's play count and date and test them as a free pre-check next round | — |
| 6 | Retries, 5xx, 427 | **$0** | 0 | Balance-proven, every round | — | — |
| 7 | Pages bought twice | about $0 | 0 | Ledger guard | — | — |

**The honest math.** Take the best niche with every fix applied (celebrities, no lookups):
- Pages: 355 / 21 = 16.9 per editor → $10.1 per 1,000.
- Feeds: 4.9 per editor → $2.9.
- Judge: $0.5.
- **Floor: about $13.5 per 1,000.** For the BL-1622 niche mix the floor is about $20.

**It cannot go under $10 on TikTok hashtags because of two numbers:**
- **2.2%** of new accounts carry an email in their bio. The same 2.2% holds across the edit app's 44,611 proven edit pages.
- **About 20%** of those email accounts are faceless edit pages; the rest are creators, fans and out-of-niche pages.
- Together that's 0.44% of new accounts, or 0.036 deliverable editors per page: 27 pages ($0.016) per editor before any other cost.

**What would break it:** a source where faceless edit pages show an address several times more often. On TikTok none was found:
- The profile has no contact field (BL-1616).
- Link-in-bio pages are crawler-blocked by linktr.ee.
- Following lists are refused; "suggested" returns celebrities (BL-1614).

Off TikTok, YouTube channels showed an email on **15%** (186 of 1,243). The owner has parked that.

## 4. What I got wrong / limits

- Before BL-1622, per-page item and author counts weren't kept, so the per-page funnel is from BL-1622/1623 only.
- "Already his" and "already seen this round" can't be split, because the stream counted them together.
- The edit app's discovery spend is from ledger labels; its $ per email can't be split per page.
- **Outside the brief:** while I worked, the tag ledger kept receiving 15-page walks with 0 emails from **another session**. Its records show "page_ceiling" and authors 51–77 per tag. I didn't touch it.

## 5. Money and stores

**$0. No vendor call, no config change, no master or workbook write.** Read only: spend.json, the tag ledger, status files, work folders, reports and edits.db (read-only).

## 6. Leak scan

| Scan | Result |
|---|---|
| Secret scan (publish_report) | PASS (run at publish) |
| Two-corpus scan (`scratch/bl1604/leak_adjudicate.py`, edit and lead corpora, every committed file) | 36 hits, all explained by the public vocabulary; **0 unexplained, 0 leaks**. |

## 7. Next (propose only)

1. The stop rule by $ per eye-checked editor, in the walker itself.
2. Free tag IDs from items already bought, and no speculative name variants.
3. A daily free re-mine of the edit app's stored bios.
4. Save each hashtag item's play count and date, so the free pre-check can be tested at $0 next time.

## 8. Paths

`scratch/bl1624/` (money.py, split.py, funnel.py + money.json, split.json, funnel.json, PROGRESS.md)
