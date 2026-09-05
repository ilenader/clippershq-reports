# BL-838: Instagram costs 17 times more than TikTok, and 15 of those 17 are calls rather than price

**2026-09-05 · DB `now()` = `2026-09-05 12:40:14.004187+00` (first read) to `2026-09-05 13:35:08` (last) · AUDIT ONLY.**
Base `origin/main` @ `2a8d8ec4`. Branch `checkpoint/BL-838`. Isolated worktree `C:/w838`, a short path, `node_modules` never junctioned, **removed at the end**. **NOTHING WAS CHANGED**: no code, no config, no data, no schema. Every database read through `scripts/run-select.js`, every timestamp cast `::text` against DB `now()`. Handles redacted. **No Apify actor was run; the 11 BL-678 guards were read, never touched.**

> ## THE ANSWER IN ONE LINE
> **Instagram costs 17.3 times more because it makes 15.0 times more provider calls at a 1.15 times higher price, and it makes 15 times more calls because it now has 12 times more clips actually being tracked and receives 21 times more new clips, not the four to five times the brief assumed.**

> **THE BRIEF'S PREMISE IS OUT OF DATE, AND THAT IS THE ENTIRE GAP.** BL-745's platform mix (Instagram 777, TikTok 171, YouTube 71) is a 14-day window from late July. **In the last 14 days it is Instagram 1,961, TikTok 93, YouTube 0.** TikTok is **4.5 percent** of new clips now. **The 18.6 percent figure appears nowhere in BL-745 or in any of the eleven reports read for this round**, and BL-745's own numbers work out to 16.8 percent. It is corrected rather than quietly substituted.

> **THE PRICE CAME FROM THE VENDORS, NOT FROM THE CODE, AND THE CODE IS WRONG IN BOTH DIRECTIONS.** Both vendors answer `GET /sys/balance`. HikerAPI: `{"requests":111125,"rate":15,"currency":"USD","amount":76.9146}`. LamaTok: `{"requests":429591,"rate":15,"currency":"USD","amount":257.786}`. The rates are **$0.00069214** and **$0.00060007** per request. This repo bills HikerAPI at **$0.001**, which is **44.5 percent high**, and bills one LamaTok label at **$0.10**, which is **167 times** the truth.

> **THERE IS NO RUNAWAY, AND IT IS PROVEN AGAINST THE VENDOR'S OWN METER RATHER THAN INFERRED.** Across two bracketed windows the HikerAPI counter fell by **293 requests in 45 minutes** while the platform's ledger recorded **256**. The 12.6 percent it did not count has three named homes. Corrected for it, the platform's own data predicts **266.1 calls an hour against the 274.5 the invoice implies: a 3.1 percent residual.**

---

## PART 1: THE EXPECTED HOURLY CALL COUNT, FROM OUR OWN DATA, BEFORE THE INVOICE

### What actually gets polled, which is not what a clip count suggests

The cron's own `where` clause (`src/lib/tracking.ts:3611-3656`) excludes far more than a raw clip count does: `isDeleted`, **`videoUnavailable: false`** (`:3615`), clip status `ARCHIVED`, and campaigns whose status is `PAST`, `COMPLETED` or `DRAFT`, plus any archived campaign (`:3640-3653`). `PAUSED` is deliberately allowed through.

| | Instagram | TikTok | YouTube |
|---|---|---|---|
| live clips (`isDeleted = false`) | **6,284** | 1,437 | 1,395 |
| tracking jobs marked `isActive` | 5,963 | 1,327 | 669 |
| **jobs the cron can actually poll** | **3,607** | **299** | **0** |
| new clips, last 5 days | **677** | 34 | 0 |
| new clips, last 14 days | **1,961** | 93 | 0 |
| new clips, last 30 days | **4,083** | 198 | 0 |

**The raw clip ratio is 4.4 to 1. The polled ratio is 12.1 to 1.** The difference is TikTok's own history: 899 of its 1,437 clips sit on `PAST` campaigns and are excluded, so five sixths of TikTok's clips cost nothing at all. **YouTube polls zero, because every YouTube clip is on a PAST campaign, and its newest snapshot is `2026-08-12 11:55:04.66`, 24 days before this read.** That confirms BL-819's dormancy finding, still unfixed, and it costs nothing because YouTube runs on Google's Data API rather than a paid vendor.

### The expected hourly call count, computed from the ladder

`checkIntervalMin` is read as hours to skip between `:00` ticks (`src/lib/tracking-intervals.ts:76-113`), so each job contributes `60 / checkIntervalMin` calls an hour. Summed over every pollable job:

| | Instagram | TikTok |
|---|---|---|
| **EXPECTED tracking calls per hour** | **269.0** | **19.8** |
| measured: `hikerapi-v2` ledger rows per hour, 50 h | **236.3** (hourly mean 231.5, range 197 to 353) | not counted at all |
| measured: `fanout:*` clips per hour, 50 h | 227.6 | **16.8** |
| measured: `clip_stats` snapshots per hour, 50 h | 214.2 | 16.1 |
| **IMPLIED BY THE INVOICE at the vendor's own rate** | **274.5** | **18.3** |

Instagram's invoice range of $0.1352 to $0.3063 an hour is **195 to 443 calls an hour**, and the ledger's own hourly range of 197 to 353 sits inside it at both ends. TikTok's $0.0042 to $0.0636 is **7 to 106** an hour against a predicted 19.8.

### Every other caller, counted

`clipper-submit-core.ts:512` calls `harvestInstagramRawMeta` (`:277`), **exactly one** HikerAPI call per Instagram submit, from which it reads the caption, BL-686's `taken_at` freshness stamp and BL-746's first view count. At 1,961 submits in 14 days that is **5.8 calls an hour**. The freshness retry beside it (`apify.ts:2582`) passes `skipHikerOverlay: true`, so it costs **no** HikerAPI call.

`retire-dead-clips` runs once daily at 06:00 UTC (`railway-cron-scheduler.ts:92`), capped at 100 candidates (`retire-dead-clips.ts:198`) inside a 240 second budget at 1,200 ms pacing: at most **4.2 media calls an hour**.

**Only two crons touch a paid provider at all**: `tracking` every 10 minutes and `retire-dead-clips` daily (`railway-cron-scheduler.ts:63`, `:92`). Measured: **300 tracking runs in 50 hours, exactly 6.00 an hour, and every single one recorded `isBatchTick = true`, meaning it fully drained with no backlog.**

### THE GAP, MEASURED AGAINST THE VENDOR'S OWN COUNTER

`requests` in `/sys/balance` is a live counter. Two windows were bracketed in which this round made no media call of its own:

| window | span | **vendor counter fell by** | platform ledger recorded | **uncounted** |
|---|---|---|---|---|
| 1 | `12:48:48Z` to `13:03:48Z`, 15 min | **87** | 85 | **2** (2.3%) |
| 2 | `13:05:08Z` to `13:35:08Z`, 30 min | **206** | 171 | **35** (17.0%) |
| **combined** | **45 min** | **293** | **256** | **37 (12.6%)** |

At most 2 of those 37 are this round's own boundary reads. The under-count is **bursty**, which is exactly what the thumbnail path predicts: a clipper opening their clips page fires a batch of captures at once.

```
invoice implies                                   274.5 calls/hour
  ledger counts                                   236.3
  + the 12.6 percent it does not count            + 29.8
                                                 --------
  reconciled                                       266.1
  RESIDUAL                                            8.4 calls/hour  = 3.1 percent
```

**BL-677'S SHAPE IS NOT PRESENT.** Its signature was a rate rising twentyfold in seven days to roughly 250 rejected calls an hour. This one is flat: 263, 206, 251, 197, 236, 216, 247, 230, 268, 230, 247, 223, 301 calls across thirteen consecutive hours, with a 50-hour mean of 231.5 and no spike anywhere.

**BUT THE LEDGER IS A FLOOR, NOT A COUNT, AND THAT IS A REAL DEFECT.** `probeHiker` (`hikerapi.ts:370`) is the function that makes the HTTP request and it records **nothing**. Only `tryHikerForInstagram` (`:794`) and the profile fetcher (`:314`) write a row. **So the submit path, the thumbnail path, the retirement cron and the admin shadow route are invisible in the platform's own cost dashboard, and so is the second leg of every 404. For LamaTok it is worse: nothing counts LamaTok calls at all.** `lamatok.ts` calls `logApifyUsage` zero times, and `fanout:tiktok` counts **URLs**, not requests, so every rescue, short-link HEAD and retry is invisible.

---

## PART 2: THE PRICE, TAKEN FROM THE VENDOR

### Measured by direct request

| vendor | `/sys/balance` at `12:44 UTC` | **price per request** |
|---|---|---|
| HikerAPI | `{"requests":111125,"rate":15,"currency":"USD","amount":76.9146}` | **$0.00069214** |
| LamaTok | `{"requests":429591,"rate":15,"currency":"USD","amount":257.786}` | **$0.00060007** |

Both accounts are prepaid quotas, so `amount / requests` is the contracted rate. **Three independent routes agree on the HikerAPI figure**: this ratio, the peer project's separately measured $0.00069, and the owner's own invoice divided by the measured call count ($0.19 ÷ 274.5 = $0.000692). `rate: 15` is the requests-per-second ceiling, and this repo already honours it at `HIKER_GLOBAL_CONCURRENCY = 15` (`apify.ts:1467`).

**One vendor-side reading did NOT reconcile, and it is named rather than dropped.** Across window 1 the `amount` field fell $0.2394 while `requests` fell 87, which would imply $0.002752 a call and a $699 monthly bill. Across window 2 it fell **$0.0000 while `requests` fell 206**. So `amount` settles in lumps and is **not** a per-call meter; `requests` is. The ratio stands, and the lumpy field is why it needed two windows rather than one.

### THE SPLIT, WHICH IS THE ANSWER THE OWNER ASKED FOR

```
invoice ratio      $0.19 / $0.011              = 17.27x
  price ratio      $0.00069214 / $0.00060007   =  1.15x
  volume ratio     274.5 / 18.3 calls per hour = 14.98x
  check            14.98 x 1.15                = 17.27x  exactly
```

**FIFTEEN OF THE SEVENTEEN IS MORE CALLS. ONE POINT ONE FIVE IS A HIGHER PRICE.** In log terms volume is **93 percent** of the gap and price **7 percent**. **This is a volume question, and a volume question has no pricing fix.** The split is a ratio of two prices, so it survives even if both absolute figures were wrong by the same factor.

### The repo's own constants are wrong, and one of them by 167 times

* **`src/lib/apify-ledger.ts:214`** sets `[HIKER_PROVIDER_NAME]: 0.001`, described in its own comment as the "flat per-URL contract rate". The real rate is **$0.00069214**, so the ledger **overstates HikerAPI by 44.5 percent**: $11.82 recorded against $8.18 real over the last 50 hours.
* **BL-745's claim that $0.001 was verified is circular and must not be relied on again.** It reads "40,452 calls, $40.45, derived from `apify_usage_entries`", but `estimatedCostUsd` in that table is computed **from this same constant**. Dividing it back out can only ever return $0.001. **The constant had never been checked against HikerAPI until this round.**
* **There is no LamaTok price constant anywhere.** `"lamatok-tiktok-only"` sits in `ZERO_COST_PROVIDERS` (`:284`) on the written grounds that both vendors bill from a prepaid quota, which is an observation of an unchanged balance rather than a rate. The BACKLOG records the price as unknown after three separate audits (`BACKLOG.md:19163`, `:19171`, `:19223`). **It is $0.00060007, and this round is the first to establish it.**
* **A LIVE LEDGER DEFECT: the bare label `"lamatok-tiktok"`** (written by `apify.ts:482`) appears in none of `PER_ITEM_USD`, `PER_CALL_USD`, `ZERO_COST_PROVIDERS` or `VALID_PROVIDERS`, so `estimateCost` falls to the unknown-provider branch and charges `APIFY_COST_PER_CALL_USD = $0.10` (`:40`). Measured over the last 50 hours: **13 rows, $1.30 of invented cost** on calls that really cost $0.0078. **That is 167 times the truth.** It is the exact artifact BL-551 fixed for the batch label and missed for this one. No real money moves, but every TikTok cost figure the owner reads is wrong, and it has already misled three audits.

---

## PART 3: EVERY HIKERAPI CALL SITE, AND WHAT EACH BUYS

`fetchHikerInstagramByUrl` (`hikerapi.ts:239`) is **not one HTTP call**. It probes `/v2/media/info/by/code` first and, **on a 404, makes a second call to `/v2/media/info/by/url`** (`:262-273`), because HikerAPI can hold a stale shortcode mapping.

| # | `file:line` | what it fetches | trigger and rate | logged? |
|---|---|---|---|---|
| 1 | `apify.ts:1580` | views, likes, comments, shares, `sharesSource` for one clip | the tracking cron's per-URL fan-out, **227.6 clips an hour** | yes, one row |
| 2 | `apify.ts:2407` | the same fields, one clip | individual fallback after a batch miss, **7.4 an hour**, capped at 5 a run | yes, one row |
| 3 | `clipper-submit-core.ts:283` | caption, `taken_at`, first view/like/comment snapshot | one per Instagram submit, **5.8 an hour** | **NO** |
| 4 | `clip-thumbnail.ts:309` | the cover image from `rawBody.image_versions2` | `POST /api/clips/[id]/thumbnail`, fired by `ClipCardNew.tsx:176` once per visible coverless clip per browser session | **NO** |
| 5 | `retire-dead-clips.ts:297` | the gone-or-not re-probe | daily 06:00 UTC, capped 100, **4.2 an hour** | **NO** |
| 6 | `retire-dead-clips.ts:243` | `/v2/user/by/username`, account corroboration | only when the media side already looks gone, **cached one call per account** | yes, `profile_*` |
| 7 | `accounts/[id]/verify/route.ts:141` | `/v2/user/by/username`, bio code match | one per verification press | yes, `profile_*` |
| 8 | `admin/hikerapi-shadow/route.ts:246` | raw diagnostic | OWNER only, manual | **NO** |

**ONE CALL PER PROFILE IS RESPECTED, AND TRACKING NEVER ENGAGES IT.** Sites 1 to 5 are per-post media lookups; only 6 and 7 touch a profile, and 6 caches its verdict per account (`retire-dead-clips.ts:238-247`). This round made no profile call at all.

**The fan-out is not a bulk endpoint.** `apify.ts:1564` maps one `tryHikerForInstagram` per URL behind a semaphore. HikerAPI is called once per clip; there is no multi-URL form in use.

### The Instagram ledger, by what each call bought, 50 hours

| kind | outcome | calls | per hour | what it bought |
|---|---|---|---|---|
| (media success) | ok | **10,490** | 209.8 | a real view count |
| `gone_404` | fallback | **964** | 19.3 | a definitive "deleted", **at two HTTP calls each** |
| (unlabelled) | ok | 177 | 3.5 | pre-BL-169 rows |
| `null_views_on_200` | error | 112 | 2.2 | a 200 with no readable count |
| `profile_resolved` | ok | 60 | 1.2 | an account bio |
| `classification_not_reel_single` | fallback | 10 | 0.2 | nothing usable |
| `profile_404` | fallback | 3 | 0.1 | a missing account |

### DUPLICATE FETCHES, NAMED

**1. The 404 double call, the largest single piece of waste.** Every `gone_404` costs two HTTP calls and buys one verdict. **19.3 extra calls an hour, $9.75 a month, 7.0 percent of the Instagram bill.** It is worse than the row count shows: a post whose `by/code` 404s and whose `by/url` then **succeeds** writes a plain `ok` row while costing two calls, and nothing distinguishes it.

**2. The same post fetched twice in one tick.** A batch miss on a clip under 48 hours old re-fetches the identical URL through `fetchClipStats` in the same tick (`tracking.ts:1349-1430`), capped at 5 a run. Measured **7.4 an hour**, **$3.74 a month**.

**3. NO field-splitting duplicate exists, and that is a credit to BL-746, BL-686 and BL-820.** One response carries views, likes, comments, shares, `sharesSource`, the caption, `taken_at` and the cover image. Nothing fetches a second time for a second field. The thumbnail path is the only caller that re-fetches a post the tick already holds, and it does so from a different process on a different trigger.

---

## PART 4: THE WASTE CATEGORIES, EACH TESTED

### PAST, COMPLETED, ARCHIVED and DRAFT campaigns: **CORRECTLY EXCLUDED**

`tracking.ts:3640-3653` drops them at the `where` clause. Measured: **1,541 Instagram, 1,028 TikTok and 669 YouTube `isActive` jobs sit on excluded campaigns and cost nothing.** BL-765's shape is not present here.

### `videoUnavailable` clips: **EXCLUDED FROM THE CRON, NOT FROM EVERYTHING**

`tracking.ts:3615` excludes them, dropping **1,265 Instagram jobs on gone clips** that would otherwise be 97.5 calls an hour. BL-717's exclusion still holds.

**They are NOT excluded from the thumbnail path, and that is a real unbounded retry loop.** **988 Instagram clips have no `thumbnailUrl`, and 751 of them are `videoUnavailable = true`.** HikerAPI 404s on all 751 at **two HTTP calls each**, the capture returns null, and `ClipCardNew.tsx:181-190` deliberately **does not set the session marker on failure** so that "a later visit retries". A permanently deleted post therefore pays two HikerAPI calls **every time its owner opens the clips page in a new browser session, forever.** This is BL-677's shape on a new vendor, smaller and slower. **Its exact rate cannot be read from any log**, but it is the best explanation of window 2's 35 uncounted calls in 30 minutes against window 1's 2 in 15, and of the 12.6 percent under-count overall.

### Retired clips: **CORRECTLY EXCLUDED.** Clip status `ARCHIVED` is dropped at `:3644`.

### REJECTED and PAUSED: allowed through on purpose, and cheap

| | jobs | calls/hour | monthly |
|---|---|---|---|
| Instagram REJECTED on ACTIVE campaigns | 314 | 2.62 | **$1.32** |
| Instagram APPROVED on PAUSED campaigns | 28 | 0.39 | **$0.20** |
| TikTok APPROVED on PAUSED campaigns | 112 | 4.39 | **$1.92** |
| TikTok REJECTED | 53 | 0.44 | $0.19 |

REJECTED clips are forced to 2,880 minutes, so each costs one call every 48 hours, which is what `F-REJECTED-CLIP-48H-TRACKING` intended. **PAUSED is 22.2 percent of TikTok's entire bill and 0.1 percent of Instagram's**, purely because TikTok's live population is so small.

### Retries: **no retry loop on the Instagram side**

`fetchHikerInstagramByUrl` has no backoff and no repeat. A 402 sets a 10 minute cooldown, a 429 sets 60 seconds, and a rolling 50 percent failure rate over 30 calls sets 10 minutes (`hikerapi.ts:1058-1096`). Each of those **stops** calls rather than repeating them, and a failing clip's cadence backs off through the ladder. **A call that 404s costs exactly 2, never 5.**

**The TikTok side is different and worse.** `fetchLamatokTiktokByUrl` (`lamatok.ts:338-372`) is a three stage chain: `by/url`, then a slideshow rescue via `by/id`, then one retry on a 5xx or timeout. **Worst case is 3 LamaTok calls plus a HEAD to tiktok.com, about 43.6 seconds for one clip.** BL-712's failing call still exists at `lamatok.ts:392` and is now the unconditional first leg of every TikTok poll; with **0 canonical `/photo/` URLs and 1,077 short links** among 1,437 TikTok clips, every slideshow on the platform takes the **most expensive** branch. And `fetchClipFreshnessWithRetry` (`apify.ts:2526`) runs that whole chain **three times** with backoff `[500, 2000, 5000]` on a submit, so one flaky TikTok submit can cost **9 LamaTok requests**. At 93 TikTok submits in 14 days that is bounded at 2.5 calls an hour, but it is **up to 14 percent of TikTok's entire bill** for a freshness check.

### Cadence: is anything polling faster than it needs to?

| Instagram, by clip age | jobs | calls/hour | share of the Instagram bill | monthly |
|---|---|---|---|---|
| **day 0, 0 to 24 h** | 203 | **131.37** | **48.8%** | **$66.37** |
| day 1 to 2 | 117 | 32.84 | 12.2% | $16.59 |
| day 2 to 5 | 347 | 51.92 | 19.3% | $26.23 |
| day 5+ | 2,941 | 53.86 | 20.0% | $27.21 |

**Half the Instagram bill is 203 clips in their first day.** That is precisely the window BL-775 measured as decisive, and PART 5 states plainly what cutting it would cost.

### Anything other than the tick and the submit path?

The LamaTok shadow sampler is **off** (`LAMATOK_SHADOW_SAMPLE_PER_TICK` default 0, zero `scraper_shadow_samples` rows in 7 days). No backfill is scheduled. The two admin shadow routes are manual, but **`admin/lamatok-shadow` will make up to 200 LamaTok calls on a single click** (`?count=100`, double-fetching each URL at `route.ts:87-90`), and `admin/hikerapi-shadow` writes no ledger row.

---

## PART 5: WHAT COULD SAFELY BE CUT, RANKED

| # | change | monthly saving | what is lost |
|---|---|---|---|
| 1 | **Persist the `gone` verdict so a 404 stops paying twice.** Skip the `by/url` leg when `by/code` 404s on a clip already known gone | **$9.75** (7.0%) | **Nothing measurable.** The second leg exists for stale shortcode mappings; keeping it for a clip's FIRST 404 and skipping it on repeats preserves that entirely |
| 2 | **Stop the thumbnail path re-probing permanently gone posts.** Persist a per-clip capture failure for the 751 `videoUnavailable` clips instead of retrying every session | **$4.50 or more** (3.2%+) | **Nothing.** The post is deleted; there is no cover to fetch. The clipper sees the same placeholder either way |
| 3 | **Do not re-fetch a clip individually in the same tick that already fanned it out** | **$3.74** (2.7%) | The fresh-clip fallback for clips under 48 h. It becomes a next-tick retry, a 10 minute delay on a first snapshot |
| 4 | **Stop polling REJECTED clips on Instagram** | **$1.32** (1.0%) | The visibility `F-REJECTED-CLIP-48H-TRACKING` was built for: seeing a rejected clip go viral elsewhere. **A real loss, small** |
| 5 | **Stop polling APPROVED clips on PAUSED campaigns** | **$2.12** across both vendors | Analytics continuity while the owner fixes something. `F-BUDGET-HARD-LOCK` allowed this on purpose |
| 6 | **Correct `apify-ledger.ts:214` to $0.00069214, add LamaTok at $0.00060007, and give the bare `lamatok-tiktok` label an entry** | **$0.00** | Nothing. **It changes no vendor call.** It stops the dashboard overstating Instagram by 44.5 percent and TikTok by 167 times |
| 7 | **Log every request at `probeHiker` and in `lamatok.ts`** | **$0.00**, and costs about $0.55 a month in database writes | Nothing. It is the only way this question stops needing an audit round, and it would have made this one an hour's work |
| | **TOTAL SAFE (1, 2, 3, 6, 7)** | **about $18 a month, 12 percent** | **nothing real** |

### THE TRADE THE OWNER MUST NOT MAKE, STATED EXPLICITLY

**Do not slow the day-0 cadence.** It is the biggest line on the bill at **$66.37 a month, 48.8 percent of Instagram**, and it is the cheapest-looking saving on this page. It is also the fraud signal.

BL-775 measured that **66.4 percent of an approved Instagram clip's views have arrived by 6 hours, against 7.8 percent for a bought-view rejection**, and that separation is the strongest discriminator the platform has on Instagram. The day-0 floor is 60 minutes (`tracking-intervals.ts:20-31`), yielding at most **6 snapshots inside that 6 hour window**. Moving day 0 to 120 minutes would halve the largest line on the bill **and halve the arrival curve to 3 points**. Moving it to 240 minutes leaves **1 point**, which is not a curve at all.

**BL-775 also measured the trap that makes this worse than it looks:** 87.9 percent of approved clips above 100,000 views were ALSO under 10 percent at six hours, so a reviewer working from a coarser curve would flag the platform's best clips first. **A cheaper day-0 poll does not merely weaken fraud detection, it points it at the wrong clips.** The owner has said accuracy beats cost. **This is the line where the two genuinely conflict, and the recommendation is to pay the $66.37.**

**Day 5+ is the only cadence that could honestly be slowed**: 2,941 clips producing 53.86 calls an hour, one call per clip per 54.6 hours, **$27.21 a month**. Halving it saves about **$13.60** and delays recognition of a late viral clip by up to five days. **No money would be lost, only recognised later**, because earnings recompute from whatever the view count eventually reads. It is a real option, it is the owner's call, and this report does not recommend it.

---

## PART 6: THE VERDICT

> **Instagram costs 17.3 times more than TikTok because it makes 15.0 times more calls at 1.15 times the price, and the volume is justified: 12.1 times more clips are actually tracked, 21 times more are arriving, and 95.1 percent of every Instagram call is an APPROVED clip on an ACTIVE campaign whose views decide what a clipper is paid.**

| | HikerAPI, Instagram | LamaTok, TikTok |
|---|---|---|
| invoice per hour | $0.19 (range $0.1352 to $0.3063) | $0.011 (range $0.0042 to $0.0636) |
| **current monthly run rate, 730 hours** | **$138.70** | **$8.03** |
| verified price per request | **$0.00069214** | **$0.00060007** |
| implied calls per hour | 274.5 | 18.3 |
| **after the cuts that lose nothing (1, 2, 3)** | **about $120.71** | **$8.03** |
| **combined today** | **$146.73 a month** | |
| **combined after** | **about $128.74 a month, a 12.2 percent cut** | |

**THE SPEND IS SUBSTANTIALLY JUSTIFIED AND THIS ROUND WILL NOT MANUFACTURE A SAVING OUT OF IT.** Of the $138.70, **$129.28 is APPROVED clips on ACTIVE campaigns being tracked to compute money** and $5.12 is PENDING clips feeding the review queue. **$1.52 is the only spend on this bill that buys nothing anyone asked for.** The rest of the recommended cut is not waste in the queue at all: it is **the same clips fetched more times than once** · a 404 answered twice, a deleted post's cover requested forever, and a clip fetched again in the tick that just fetched it.

**Roughly $140 a month is close to the true price of tracking 3,607 Instagram clips accurately, and the honest recommendation is to keep paying it.** What should change is the three duplications, the two wrong cost constants, and the fact that the platform cannot count its own vendor calls.

**PERFORM NO FIX. Nothing in this round was changed.**

---

## PROBES, DISCLOSED IN FULL

| requests | cost | why |
|---|---|---|
| `GET api.hikerapi.com/sys/balance` x **7** | $0.00484 | establish the real price, then bracket two passive windows to measure the true call rate |
| `GET api.lamatok.com/sys/balance` x **1** | $0.00060 | establish the real price |
| `GET api.lamatok.com/openapi.json` | **$0.00**, unauthenticated | enumerate the endpoint surface; it is how `/sys/balance` was found. HikerAPI's own OpenAPI is behind a 401 |
| `hikerapi.com/`, `/pricing`, `/p/tariffs`, `lamatok.com/` | **$0.00** | attempt to read the published price. **Both marketing sites are JavaScript single-page apps and returned no pricing text** |
| **TOTAL** | **8 billable requests, $0.00544** | cap was roughly 20 |

**ZERO media calls, ZERO profile calls, ZERO Apify actor runs.** One call per profile is not engaged because no profile was fetched.

---

## WHAT COULD NOT BE MEASURED

* **The vendors' published price lists.** Both marketing sites are JavaScript single-page apps that return a bare `HikerAPI` or `LamaTok` heading to a fetch. The prices in PART 2 come from each account's own `/sys/balance`, which is the effective contracted rate and is the better number anyway.
* **Why the `amount` field moved $0.2394 in one window and $0.0000 in the next.** It settles in lumps rather than per call. `requests` is the real-time meter and is what this report uses; the dollar field is reported as observed and not explained.
* **The thumbnail path's exact call rate.** Nothing logs it, and it is driven by how often clippers open their clips page. It is the best explanation of the measured 12.6 percent under-count, inferred rather than counted.
* **LamaTok's true request count.** Nothing counts LamaTok calls. `fanout:tiktok` counts URLs, so 839 in 50 hours is a **floor**; every rescue, short-link HEAD and retry is invisible. The invoice-implied 18.3 an hour against a predicted 19.8 says the floor is close, but it is not proven.
* **Whether a failed call is billed.** `lamatok.ts:265-266` asserts twice that server errors are free, and its retry design depends on that being true. **It is an unverified assertion.** HikerAPI's 404 behaviour is the same open question and it bears directly on PART 5 item 1: if a 404 is free, that saving is smaller than stated.
* **The live Railway environment values** for `CLIPS_PER_TICK`, `SCRAPER_TIKTOK_PROVIDER`, `LAMATOK_SLIDESHOW_BYID` and `HIKERAPI_DAILY_BUDGET_USD`. Behaviour was inferred from the ledger instead: 6 fully-drained ticks an hour carrying about 42 clips each says `CLIPS_PER_TICK` is above its code default of 30.
* **Whether HikerAPI sells a cheaper bulk media endpoint.** Its OpenAPI is behind a 401 and the fan-out at `apify.ts:1564` is one call per URL. If a bulk form exists it would be the largest saving available on this bill, and this round could not find out.
* **The `rate: 15` field's exact meaning.** It reads as a requests-per-second ceiling and the repo already sets `HIKER_GLOBAL_CONCURRENCY = 15`, but the vendor does not document it anywhere readable.

---

## SAFETY

| | |
|---|---|
| changes made | **none.** No code, config, data or schema. The only files added are this report and one read-only probe script, which was superseded by direct `curl` reads and is committed for the record |
| Apify | **no actor run.** The 11 BL-678 guards were read and are untouched; `APIFY_HARD_OFF` is still a typed `true` literal |
| money | **no clip, payout, earning or campaign was created, modified or deleted.** Every request in this round was a GET |
| the 6 money files and `tracking.ts` | **not edited and not in any diff** |
| database | read-only through `scripts/run-select.js`, every timestamp cast `::text` against DB `now()` |
| build | **not run.** A markdown-only diff cannot change `tsc`, and no build is claimed |
| worktree `C:/w838` | **removed** |
| counting | every count taken with a SQL `COUNT(*)` or `grep -c`, never piped through `head` |
| subagents | two ran in parallel under the same constraints, one on the eleven prior reports and one on the LamaTok path. **Their findings are reconciled, not averaged**: the report digest claimed BL-745 verified $0.001 against the ledger, and PART 2 rejects that as circular rather than repeating it |

**MOVED DURING THE ROUND AND NOT MINE:** the tracking cron ran normally throughout, adding roughly 250 Instagram snapshots an hour. This round's eight vendor requests are all `/sys/balance` reads, which fetch no media and write nothing.
