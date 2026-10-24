# BL-1697: cost audit of the $50 run (BL-1689, 22-23 Oct) -- where 47,079 requests went

Dusan's question (HELM 14:06): at $0.0006 a request, ~30 videos a hashtag page and a 5-8% email rate, 1,000 real editors
should cost $3-5. The run spent $28.25 on the LamaTok counter for 891 real editors (~$32 per 1,000). $0 spent on this audit;
every number below is read from the run's own logs (bl1689_work cot_/fol_/old_/deep_ logs, raw_emails status.json,
money89.txt, bl1677_work/<run>eyes/final.json, MILOJE wallet.json).

## The short answer
The 5-8% email rate is right: a hashtag page call returned 15.6 author entries and 1.38 of them had an email in the bio
(8.9%). Two things the $3-5 estimate leaves out:
1. **61% of those email authors were already in our store** (earlier rounds since September, and the same accounts on many
   tags/pages). Only 0.54 NEW email accounts per hashtag call.
2. **Only 6.7% of the new email accounts are real editors** under his filter (faceless edit page, not a creator/fan/business,
   photos <= 30%, Sonnet + Opus). 93% are creators, fan pages, faces, businesses.
So one real editor costs 1 / 0.54 / 0.067 = **27.6 hashtag calls + 14.8 picture-check calls = 42 calls = $0.025 -> $25 per 1,000**
on the main method (co-tag walks, 23 Oct). The run's $32 average includes the bad first day (movie/anime tags) and the losses below.

## Does the hashtag call already return the bio?
**Yes.** The bio (author signature) and the email in it come with the hashtag page -- no per-account profile call is needed to
find the email. Profile (user) calls were only 649 requests (1.4%), in the small partner routes. The per-account call we DO pay
for is the **feed (12 covers) = the picture check** that his filter needs (face / photos / creator): 11,835 requests, 25% of
the spend, one per NEW email account -- and 93% of those accounts are then rejected.

## By call type (all LamaTok requests, 22-23 Oct)
| call type | requests | share | $ |
|---|---|---|---|
| hashtag pages (walk, tag-id lookups, deep, refill, co-tags) | 27703 | 59.0% | $16.62 |
| following lists | 3124 | 6.7% | $1.87 |
| profile (user) lookups | 649 | 1.4% | $0.39 |
| feeds = picture check (1 per NEW email account) | 11835 | 25.2% | $7.10 |
| lost / stopped / never processed | 3616 | 7.7% | $2.17 |
| not attributable to a run (counter moved by retries / others) | 152 | 0.3% | $0.09 |
| **total (counter 128,513 -> 81,434)** | **47,079** | 100% | **$28.25** |

## Per chunk
`real` = strict good from that run's checks (a page found by two runs counts in both: 934 here vs 891 unique delivered).
`authors returned` are author entries on the pages (repeats included). 22 Oct chain runs logged calls and spend but not the
author counts; their feeds are counted inside the next run's spend (the chain bought them between walks).

| run | day | route | walk/following calls | feed calls | total calls | $ | authors returned | with email in bio | NEW email accounts | real | $/1k real |
|---|---|---|---|---|---|---|---|---|---|---|---|
| m1(22) | 22 Oct | hashtag walk (chain70) | 452 | 0 | 452 | 0.27 | - | - | - | 7 | 39 |
| s1(22) | 22 Oct | hashtag walk (chain70) | 670 | 93 | 763 | 0.46 | - | - | - | 14 | 33 |
| s2(22) | 22 Oct | hashtag walk (chain70) | 1606 | 0 | 1606 | 0.96 | - | - | - | 19 | 51 |
| m2(22) | 22 Oct | hashtag walk (chain70) | 1953 | 75 | 2028 | 1.22 | - | - | - | 34 | 36 |
| a1(22) | 22 Oct | hashtag walk (chain70) | 1205 | 174 | 1379 | 0.83 | - | - | - | 5 | 165 |
| m3(22) | 22 Oct | hashtag walk (chain70) | 1889 | 62 | 1951 | 1.17 | - | - | - | 12 | 98 |
| m4(22) | 22 Oct | hashtag walk (chain70) | 459 | 0 | 459 | 0.28 | - | - | - | 0 | - |
| r1 | 22 Oct | re-walk proven tags (chain72) | 933 | 167 | 1100 | 0.66 | - | - | 227 | 13 | 51 |
| pa+pb | 22 Oct | partner pages (user+feed) | - | - | 233 | 0.14 | - | - | 140 | 30 | 5 |
| f3 | 22-23 Oct | following lists | 1500 | 1325 | 2825 | 1.69 | 14917 | 2587 | 1325 | 96 | 18 |
| f4 | 22-23 Oct | following lists | 953 | 717 | 1670 | 1.00 | 9602 | 1538 | 717 | 44 | 23 |
| f3 lost | 22 Oct | following (lost: MemoryError) | 2801 | 0 | 2801 | 1.68 | - | - | 0 | 0 | - |
| f1+f2 | 22 Oct | following lists | - | - | 671 | 0.40 | - | - | - | 28 | 14 |
| o1 | 22-23 Oct | re-walk proven tags | 2028 | 594 | 2622 | 1.57 | 33740 | 2936 | 594 | 65 | 24 |
| o2 | 22-23 Oct | refill walked tags | 1261 | 606 | 1867 | 1.12 | 21677 | 2746 | 606 | 11 | 102 |
| d2 | 22-23 Oct | deep pages 5-8 | 1118 | 251 | 1369 | 0.82 | 13747 | 1293 | 251 | 20 | 41 |
| c1 | 22-23 Oct | co-tag walk | 249 | 107 | 356 | 0.21 | 4443 | 388 | 107 | 12 | 18 |
| c2 | 22-23 Oct | co-tag walk | 766 | 375 | 1141 | 0.68 | 12787 | 1177 | 375 | 28 | 24 |
| c3 | 22-23 Oct | co-tag walk | 192 | 84 | 276 | 0.17 | 3253 | 303 | 84 | 14 | 12 |
| m1s | 22-23 Oct | co-tag walk | 492 | 174 | 666 | 0.40 | 8448 | 788 | 319 | 19 | 21 |
| m2 | 22-23 Oct | co-tag walk | 1658 | 933 | 2591 | 1.55 | 27376 | 2519 | 933 | 59 | 26 |
| k3 | 22-23 Oct | co-tag walk | 1657 | 803 | 2460 | 1.48 | 27588 | 2341 | 803 | 57 | 26 |
| k4 | 22-23 Oct | co-tag walk | 1662 | 904 | 2566 | 1.54 | 27364 | 2335 | 904 | 70 | 22 |
| k5 | 22-23 Oct | co-tag walk | 1647 | 852 | 2499 | 1.50 | 27116 | 2383 | 852 | 68 | 22 |
| q1 | 22-23 Oct | co-tag walk | 1699 | 978 | 2677 | 1.61 | 26616 | 2344 | 978 | 68 | 24 |
| q2 | 22-23 Oct | co-tag walk | 1699 | 1134 | 2833 | 1.70 | 25422 | 2459 | 1185 | 61 | 28 |
| q3 | 22-23 Oct | co-tag walk | 1699 | 837 | 2536 | 1.52 | 26196 | 2109 | 837 | 43 | 35 |
| q4 | 22-23 Oct | co-tag walk | 940 | 316 | 1256 | 0.75 | 7021 | 663 | 316 | 20 | 38 |
| d1 | 23 Oct | deep pages 5-8 | - | - | 228 | 0.14 | - | - | - | 7 | 20 |
| m1t | 23 Oct | feeds only (m1s leftovers) | 0 | 146 | 146 | 0.09 | - | - | - | 9 | 10 |
| p1 | 22 Oct | partners (part3090) | - | - | 544 | 0.33 | - | - | - | 1 | 326 |
| q6 | 23 Oct | stopped for pause | 356 | 0 | 356 | 0.21 | - | - | 0 | 0 | - |

## Exactly where the extra requests went
| where | requests | $ | note |
|---|---|---|---|
| hashtag pages whose email authors were ALREADY KNOWN | ~16,900 of 27,703 | ~$10.1 | 61% of email authors on the pages were in our store already (duplicates across tags, pages and earlier rounds) |
| picture checks of accounts that then failed his filter | ~11,000 of 11,835 | ~$6.6 | one feed per new email account, 93% rejected |
| lost run: f3 following lists died of MemoryError after paying | 2,801 | $1.68 | LESSON 82; re-run paid again |
| m4 (22 Oct) walked, never checked (Dusan's 18:50 stop) | 459 | $0.28 | |
| q6 started after the pause order, stopped | 356 | $0.21 | LESSON 90 |
| first day's movie/anime tags (a1, m3: $98-165 per 1,000 real) | 3,330 | $2.00 | Dusan stopped it: ~90% creators |
| refill of tags walked 2-4 days earlier (o2) | 1,867 | $1.12 | $102 per 1,000 real |
| partner lookups p1 | 544 | $0.33 | 1 real |
| following lists that were PRIVATE (403) | 1,186 of 2,453 | $0.71 | 48% of seed lists private |
| tests ($2 test) | 1,215 | $0.73 | inside the 22 Oct rows |
| tag-id lookups, 404 tags, retries | small | <$0.15 | e.g. s2: 1,606 calls for 1,478 pages; 24 tags 404 |

## Why the wallet shows $45.35
The wallet holds **bookings**, not spend: money_guard books each chunk's CAP before it runs and nothing ever trues the booking
down to what was used. 35 bookings = $45.35; real spend = $28.25 LamaTok + $0.32 HikerAPI (Instagram test) = $28.57;
unused headroom $16.78. Booked twice: b89_f2 ($0.30 at 21:24 and 21:27, $0.24 used) and b89_f3 ($3.00 at 21:35 for the run
that was lost, $3.00 again at 21:51 for its re-run; $3.37 used of $6.00). Booked but nothing walked: q5 $1.20. q6 $1.90 booked,
$0.21 used; q4 $1.90 booked, $0.75 used. The two 22 Oct bookings ($2 + $8) covered ~$5.9 of chain walks.
Fix (proposed, not done): after each chunk, book a correction of (actual - booked) so the wallet shows spend.

## Plan: 1,000 real editors for $5 or less, same filter -- tested free first
At $5 per 1,000 one real editor may cost 8 requests in total. Today it costs 42, and 28 of them are hashtag pages. Free
pictures alone cannot get there (the pages are 2/3 of the cost); it needs pages that are ~4x richer in real editors.
Free tests (no paid call), in this order:
1. **Free picture check** ($0): read the 12 covers from TikTok's own profile page on the 3090 (worked for 14,548 reads before a
   403 on 22 Oct) for 200 accounts we already judged (100 real, 100 rejected) and compare verdicts with the paid feeds.
   If they match, the 25% picture-check cost goes to $0 -> ~$17 per 1,000 on the co-tag method.
2. **Which tags are rich** ($0): from the 23 Oct walks (ledger + final.json) the real editors per tag; check whether the top
   tags of round N predict the real rate of round N+1 (a forecast, not a hindsight pick).
3. **Following lists of the 891 real editors** ($0 part): check on the 3090 for free which seed lists are public before
   paying (48% were private) -> following lists measured $18 per 1,000 without the lost run; half the calls saved -> ~$12.
4. Only then one paid test on his yes ($1 cap, ~1,700 requests), best combination of 1-3, priced per real editor.
Honest expectation: $10-15 per 1,000 with the same filter. **$5 is not in sight**: the only route that measured $5 (partner
pages of proven editors, 30 real) had a pool of 116 pages and is used up. I will say so with numbers after the free tests.
No paid call without Dusan's yes.

## The HQ spend ledger misses the 3090 runs (14:20, 3 FIXER's follow-up)
`spend.json` for 22-24 Oct holds only the runs made on this PC: 9,473 LamaTok calls / $5.68 (22 Oct m1, s1, s2, m2, a1, m3,
m4 part, r1 and their feeds) and ig89 $0.31 (HikerAPI). Every run made on the 3090 (f2-f4, o1, o2, p1, d1, d2, c1-c3,
m1s/m1t, the 23 Oct m2-m4/k5, q1-q4, q6) wrote only zero-call feed rows: ~37,600 calls / ~$22.57 are not in the ledger, so
the ledger's lifetime TikTok total understates by that much. tag3090/fol3090/part3090/feeds89 book the wallet and
money89.txt from the counter but never append a spend.json row. Offered: a backfill row per run from money89.txt, a FACTS
re-stamp, and a ledger write in the 3090 runners -- on a yes.
