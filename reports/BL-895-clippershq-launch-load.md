# BL-895 — can the platform carry fifty new people, and can the owner keep up with them

**VERDICT IN ONE LINE: the machine carries this launch with roughly three times the headroom it needs, and ONE defect in the approval queue will hide your editors' submissions from you after about seventeen days, which must be fixed before you open it.**

**MODEL SPLIT AND SAVING.** Two cheap subagents did the mechanical code reading (cron constants and cadence ladder; approval queue and pending copy), about 183,000 subagent tokens that would otherwise have been mine. The strongest model ran EVERY database measurement itself, judged what breaks first, and wrote this. Claims are marked **VERIFIED** where I measured or read them myself and **READ** where a subagent reported them and I did not re-derive. **Two subagent claims were wrong and both are corrected below.**

**PART 0 — I DID NOT CAUSE THE INCIDENT I WAS MEASURING.** Subagents were forbidden to open a database connection, run any `.ts` file, touch `run-select.js` or make any network call, and none did. Every query was mine, run one at a time, sequentially, from a single short-lived process. **Measured connection cap while I worked: 17 of 90 total, 1 active** (db_now 2026-09-18 09:55:07). No Apify actor ran and no vendor call was made. Nothing was changed: this round writes one markdown file. A markdown-only diff cannot change tsc or the build, so **no build was run and none is claimed**.

## PART 1 — where the cron stands today, re-measured

All figures VERIFIED at db_now **2026-09-18 09:53 to 09:55**.

| measure | today |
|---|---|
| users / clips / campaigns | 1,762 / 10,243 / 35 |
| tracking jobs, active | 8,664 |
| active jobs **on a live campaign** | **648** |
| of those, overdue by any amount | **ZERO**, oldest due 2026-09-18 10:00, seven minutes in the future |
| snapshots written, last 24h | 1,444 (1,253 live campaigns, 191 finished, 13.2 percent) |
| capacity | **4,320 per day** |
| **headroom** | **~2,876 snapshots per day, about 2 in every 3 unused** |

**CAPACITY IS 4,320 AND THAT IS CONFIRMED FROM THE CONSTANT, NOT INHERITED.** `clipsPerTick` defaults to **30** (`tracking.ts:164-178`, changed 60 to 30 by BL-197) and the cron fires **every 10 minutes**, so 30 × 144 ticks = 4,320 per day. That is exactly BL-856's figure, re-derived. The loop budget is 210 seconds (300s route ceiling minus a 90s reserve, `cron-budget.ts`). **READ from the subagent, spot-checked by me against `tracking.ts:164`.**

**THE 512 STARVED CLIPS HAVE BECOME 3,732, AND THAT IS NOT THE ALARM IT LOOKS LIKE.** I re-ran BL-872's query: 6,946 active jobs are due now, 4,140 overdue by a week, **3,732 overdue by more than 24 days**, the oldest due 2026-05-14. Then I asked the question that matters and it reversed the finding: **of the 4,140 overdue by a week, ZERO are on an ACTIVE non-archived campaign.** They are 2,452 still-earnable clips, 1,346 whose video is gone and 659 not approved, every one of them on a campaign that is paused, completed, past or archived. Those clips are not owed money; their campaign is over. **The backlog is job rows never deactivated when a campaign ended, which is untidy and costs 13.2 percent of the cron, not money not arriving.**

**AND IT IS DELIBERATE.** BL-200 changed the due query to `orderBy [{ checkIntervalMin: asc }, { nextCheckAt: asc }]` (`tracking.ts:3975-4096`, READ, and it exactly predicts my measurements): short-cadence live clips are collected BEFORE ancient long-cadence dead ones. That is why 648 live jobs have zero lag while 3,732 dead ones are months overdue. The system is starving the right clips on purpose.

**THE TICKS ARE ALL LANDING AND ALL DRAINING.** `cron_runs` shows **144 of 144 ticks per day, every day for five days, every one fully drained** (`isBatchTick` true), last tick 09:50:38 against my 09:53 query. There is no hidden backlog.

**THE LIVENESS RECHECK AND THE CHASER DO NOT SPEND THIS BUDGET.** BL-865's recheck runs on its own 300-second route daily at 07:00 UTC, about 297 probes, and is not gated by the tracking deadline. BL-871's chaser is spec only and not scheduled. **READ.**

**HEADROOM AS NEW CLIPS PER DAY.** A new clip costs **30.75 snapshots in its first seven days** (VERIFIED across 3,169 real clips created 7 to 30 days ago), about 4.4 a day, then falls to the 1,440 or 4,320 minute tiers. In week one alone the headroom absorbs about **650 new clips a day**. Sustained for a month, where clips accumulate at roughly half a snapshot a day each, it absorbs about **150 new tracked clips a day**.

## PART 2 — what fifty people actually add

**THE DISTRIBUTION, NOT A MEAN (VERIFIED, 14 days):** 55 active clippers, **median 0.64 clips a day**, mean 1.66, p90 **4.27**, p99 11.61, max **12.57**. The skew BL-772 measured is still there: the median clipper posts two clips every three days and the busiest posts twelve a day.

**THE MULTIPLIER RUNS THE OPPOSITE WAY TO THE WORRY, AND THIS IS THE ROUND'S MOST USEFUL CORRECTION.** I verified it in the source rather than reasoning about it: `grep -c` for `clip.create` in the editor submit path returns **ZERO**, while the poster path creates the Clip, the ClipStat and the trackingJob together (`marketplace-v2-poster.ts:554, 591, 598`). **An editor's submission creates no tracked clip and costs the cron nothing at all.** A v2 clip only becomes tracked work when a POSTER posts it.

So **30 editors add zero cron load** and the entire tracking cost of this launch comes from **20 posters**.

| scenario | new tracked clips a day | fits in ~150 a day |
|---|---|---|
| 20 posters at the platform median (0.64) | 13 | yes, trivially |
| 20 posters at p90 (4.27) | **85** | **yes, with room** |
| 20 posters at the platform maximum (12.57) | 251 | no, about 1.7 times over |
| worst case: 30 editors approved daily, all 20 posters take all 30 | **600** | no, four times over |

**IT FITS AT ANY REALISTIC RATE AND STOPS FITTING AT ABOUT 150 NEW TRACKED CLIPS A DAY**, which needs each of the 20 posters to post about 7.5 clips a day, above the platform's p90 and below its observed maximum. The worst case is real but requires every editor's clip to be approved daily AND every poster to take every one, which BL-879's design encourages but no measured clipper behaviour comes close to.

## PART 3 — what saturation looks like from outside

**WHICH CLIPS STOP FIRST: the longest-cadence ones**, because the due query sorts by `checkIntervalMin` ascending. Under saturation a fresh 60-minute clip is always collected before a 4,320-minute one. **Nobody's fresh work stops; the oldest, slowest, mostly dead clips stall further.** That is the good failure mode and it is already in production.

**WOULD ANYONE NOTICE? Probably not, and that is the danger.** A clipper sees a view count that stops rising, which is indistinguishable from a video nobody is watching. The owner sees nothing at all. There is no screen anywhere that shows queue depth.

**THE MONEY.** BL-872 priced 512 starved clips at roughly $70 to $120 a month, about **$0.14 to $0.23 per starved clip per month**. At launch volume, saturation would strand the long tail first, so a week of genuine saturation stalling, say, 300 live clips would strand roughly **$40 to $70 a month** while it persisted. Real, and an order of magnitude smaller than the approval defect below.

**WOULD ANY ALERT FIRE? NO, AND THE REASON IS SHARPER THAN BL-872's.** The watchdog runs every 30 minutes and alerts when the tracking heartbeat is more than **45 minutes** stale (`cron-watchdog-policy.ts:156-165`, READ). BL-872's point stands that it reads `cron_runs` from the same database the cron writes to, so a database outage silences it. **But the saturation case is worse than that: under saturation the cron still ticks every ten minutes and still writes its heartbeat, so the watchdog sees a perfectly healthy platform and stays silent for ever.** It detects a STOPPED cron. It cannot detect a BEHIND one.

**THE ONE ALERT THAT WOULD, AND IT IS ALREADY HALF BUILT.** `isBatchTick` is set true only when a tick **fully drained**; a tick that hits the 30-clip cap leaves it false. That column is the saturation signal and it reads **144 true, 0 false** every day right now. The alert is: *any tracking tick in the last hour with `isBatchTick = false`*. **Cost: one query added to the existing watchdog route, which already runs every 30 minutes and already emails owners. Code only, no vendor, no external click, no new service, and no new schedule.** I am not building it in this round; I am specifying it.

## PART 4 — the owner's own capacity, and the defect that must be fixed

**THE DEFECT, VERIFIED BY READING THE ROUTE MYSELF** (`src/app/api/marketplace-v2/admin/queue/route.ts:43-47`):

```
const clips = await db.marketplaceV2Clip.findMany({
  select: OWNER_QUEUE_SELECT,
  orderBy: { createdAt: "asc" },
  take: 500,
});
```

**There is no `where` clause.** The queue returns the **oldest 500 v2 clips that have ever existed**, approved and rejected ones included, sorted oldest first. Today there are **zero** v2 clips so nothing is wrong yet. Once the total passes 500, the query returns 500 decided clips and **every newer PENDING submission falls off the end and becomes invisible to you.** The editor is told "There is no fixed clock. He reviews these by hand, so it takes as long as it takes" and waits for ever, for a clip you cannot see.

**WHEN IT BITES: about 17 days.** 30 editors submitting one clip a day each is 30 a day; 500 ÷ 30 ≈ 17. If they submit more than one a day it arrives sooner. This is the only finding in this round that silently loses a person's work.

**THE REST OF THE QUEUE IS SOUND AT THIS SIZE.** It makes **one** network request on load, has no per-row fetch, and the thumbnail is a plain `<img>` against a stored URL. It does split the fetched array client side into pending and decided (`admin-client.tsx:119-120`), which is the BL-836 shape, but **it renders both halves so nothing is hidden by it** and no count is displayed that could disagree with the list. At 30 and at 100 pending it is fine. At 500 it is one large payload with no pagination, and past 500 the defect above dominates anyway. **READ from the subagent, with the route quoted above re-read and VERIFIED by me.**

**YOUR TIME, WHICH IS THE REAL CONSTRAINT.** One decision means opening a Drive link in a new tab, watching a clip, coming back and choosing, and typing a reason if you reject. Realistically **two to four minutes each**, and a rejection costs more than an approval because the reason is required (the route validates a non-empty reason, READ). At 30 editors submitting daily that is **one to two hours every day, seven days a week**, before you do anything else. At 30 submissions a day you are the bottleneck long before the cron is: **the machine's limit is 150 new tracked clips a day and yours is roughly 20 to 30 decisions.**

**HOW TO GO FASTER: nothing here decides for you, and that is deliberate.** BL-771 measured every computable signal at under 21 percent precision against a 99.2 percent human bar, so no auto-approve is defensible. What genuinely helps without deciding anything: the thumbnail already stored means you can reject an obviously wrong clip without opening Drive; keyboard-only approve and reject would remove the mouse round trip; and batching one sitting a day rather than reacting to each notification. **Each of those speeds up your hand, not your judgement.**

**AN EDITOR WAITING THREE DAYS IS TOLD NOTHING, AND THAT IS WHAT SHIPS, CONFIRMED.** I checked for a promised wait anywhere in the v2 copy: **zero time estimates**. `V2_HOW_LONG_APPROVAL` reads "There is no fixed clock. He reviews these by hand, so it takes as long as it takes", and the copy file records why inventing a number would be dishonest. The pending row says "The owner has not looked at this yet. Nobody can see it until it is approved." **He is told the truth and given no estimate, which is correct, but he is also given no position in a queue and no sign of progress.**

## PART 5 — everything else that scales with people

| thing | today (VERIFIED) | rate now | what fifty people change |
|---|---|---|---|
| **Vendor spend** | Instagram **1,447 calls a day**, TikTok 93 (94 percent Instagram) | BL-838's $139 a month | 20 posters at p90 add ~85 clips a day, about **1,650 extra snapshots a day at steady state**, ~94 percent of them Instagram. **Roughly doubles the bill to about $290 a month.** At the 150-clip ceiling it would reach about $400. |
| **Connection pool** | **17 of 90**, 1 active | flat | Web traffic from 50 users is a rounding error against 90. **No concern.** |
| **Refusal rows** (BL-870/889) | **78 total, all 78 in the last 7 days** | ~11 a day with two people using v2 | Brand new and unbounded. Fifty people might make it a few hundred a day. At ~0.5 KB a row that is tens of MB a year. **Watch it, do not act.** |
| **Notifications** | **15,157** | 273 in 7 days, ~39 a day | Every approve and reject writes one. 30 decisions a day roughly doubles it. Still small. |
| **Audit rows** | **29,083** | 985 in 7 days, ~141 a day | Grows with decisions. Table is 15 MB. **No concern.** |
| **clip_stats** | **380,639 rows, 153 MB** (~420 bytes a row) | ~1,540 a day | At full 4,320 a day saturation that is 1.8 MB a day, about **55 MB a month**. **No concern.** |
| **Thumbnails** | 0 v2 clips today | one URL per v2 CLIP, not per post | A stored URL string, not a blob in this database. **No storage concern here.** |
| **Largest tables** | email_events 200 MB, user_events 160 MB, clip_stats 153 MB, apify_usage 102 MB | — | The two biggest are not driven by clip volume at all. **Fifty people do not move them.** |

## PART 6 — the verdict and the plan

**The tracking machine carries this launch comfortably: 648 live jobs with zero lag, 144 of 144 ticks draining every day, and about two thirds of its 4,320 a day capacity unused. It stops fitting at roughly 150 new tracked clips a day, which 20 posters reach only by each posting more than seven a day, above the platform's p90. You are the bottleneck, not the cron.**

### Before you open it

1. **Add a `where` to the approval queue.** `where: { status: "PENDING" }` in `queue/route.ts:43`. Without it, after about 17 days your editors' submissions stop appearing and they wait for ever on work you cannot see. **Cost: one line, code only. This is the only item on this list that loses someone's work.**

### Soon after, in this order

2. **Alert on a tick that did not drain.** One query on `cron_runs` for `isBatchTick = false` in the last hour, added to the watchdog route that already runs every 30 minutes and already emails you. **Code only, no vendor, no external click.** Without it, saturation is invisible: the cron keeps ticking, the heartbeat keeps arriving, and the existing watchdog stays silent.
3. **Deactivate tracking jobs when a campaign ends.** 6,946 jobs are due on finished campaigns and consume 13.2 percent of every tick. It costs you nothing today because the cadence ordering protects live work, but it is 13 percent of your headroom spent on campaigns that are over. **Code only.**
4. **Expect the Instagram bill to roughly double**, from about $139 to about $290 a month at realistic volume. **Vendor, no action needed beyond knowing.**

### What I could not measure

Nothing on a real v2 clip, because **there are zero of them**: the platform has never had a marketplace v2 submission. Every v2 figure here is structural, read from the code and the schema, and the tracking figures are measured on the 10,243 ordinary clips that do exist. The first real editor submission will be the first true test of the approval path end to end.

### The three numbers to watch in your first week

1. **Undrained ticks.** `SELECT count(*) FROM cron_runs WHERE kind='tracking' AND NOT "isBatchTick" AND "firedAt" > now() - interval '24 hours';` Today it is **0**. **Anything above 0 for two days running means the cron is behind and view counts are going stale.**
2. **Pending clips older than two days.** `SELECT count(*) FROM marketplace_v2_clips WHERE status='PENDING' AND "createdAt" < now() - interval '2 days';` Today **0**. **Above about 20 means you are falling behind your editors**, and past 500 total v2 clips it also means the queue defect is hiding work from you.
3. **Overdue jobs on LIVE campaigns.** The query in PART 1. Today it is **0 and has no lag at all**. **Anything above a few dozen means real clips are not being polled and real money is not arriving.**
