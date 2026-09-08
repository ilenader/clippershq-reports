# BL-856 — everything that will bring the site down again

**AUDIT ONLY. Nothing was changed, no index was created, no row was deleted, no fix was applied.**
Branch `checkpoint/BL-856`. Base `b2475636`. Database read at `2026-09-08 20:01:28.360998+00` onward, PostgreSQL 17.6.

---

## The single most valuable thing to do first

**`/api/health` returns `{ok:true}` without ever touching the database.** Its own comment says so: *"Deliberately lightweight: no DB hit, no external calls."* That is why a 27 hour outage went unnoticed. Railway's probe kept reporting the container healthy for the whole 27 hours, because it was healthy. The database was not, and nothing asked it.

**Add a second endpoint that runs `SELECT 1`, and point a free external uptime monitor at it, alerting to Discord.** Thirty minutes of work. Everything else in this report is a slow accumulation you have months to deal with. This one is the difference between knowing in four minutes and knowing when a clipper complains.

---

## PART 0 — how this round avoided repeating the incident

**Concurrency cap: exactly one database connection, held by me, queries issued strictly one at a time.**

**Ten subagents ran, all ten reported, and not one was allowed to touch the database.** Every one was given the same hard rule in writing: no `run-select.js`, no Prisma, no connection. They read code only. Every figure in this report that came from the database came from my single sequential connection. That is a deliberate inversion of the usual pattern: parallelism where it is free, serial where it is dangerous.

The cost of each heavy query was stated before running it, in the shell, for example *"cost: one sequential scan of clip_stats heap, 46 MB, expected about one second"*. The heaviest thing this round ran was three sequential scans totalling about 193 MB. Nothing was run against production without that statement first.

**Measured during the round:** connections went 29, then 40, on a ceiling of 90. Zero connections were ever `idle in transaction`. No read failed.

---

## PART 1 — the four duplicate queries, and the scans, named in code

### The four `per_day` queries: found, and it is worse than four

**File: `src/app/api/admin/analytics/views-by-day/route.ts:374-404`.** Twins at `src/app/api/analytics/views-by-day/route.ts:299-329` and `src/app/api/client/campaigns/[id]/route.ts:124-149`, all three commented as the same copied pattern.

**Why it runs four times, proven in code rather than guessed.** `src/app/(app)/admin/analytics/page.tsx:373` declares `const metricsToFetch = ["views","likes","comments","shares","earnings"]`, and `:374-388` does `Promise.all(metricsToFetch.map(m => fetch(...)))`. Five parallel HTTP requests, one per metric. Four of them (`views`, `likes`, `comments`, `shares`) reach the same CTE, differing by exactly one identifier: `MAX(s."views")` versus `MAX(s."likes")` and so on. **They are not four unrelated callers, not React StrictMode, and not polling. They are one `useEffect` fanning out over an array.**

**Measured in `pg_stat_statements`, not inferred:**

| query | calls | total ms | mean ms | rows returned |
| --- | --- | --- | --- | --- |
| `per_day ... MAX(s."comments")` | 4 | 9,335 | 2,333.7 | 108 |
| `per_day ... MAX(s."likes")` | 4 | 9,250 | 2,312.6 | 108 |
| `per_day ... MAX(s."shares")` | 4 | 9,205 | 2,301.3 | 108 |
| `per_day ... MAX(s."views")` | 4 | 9,038 | 2,259.6 | 108 |
| the earnings branch, `SELECT s."clipId", date_trunc(...)` | 4 | 5,963 | 1,490.8 | 200,746 |
| a second `per_day` set, the per-campaign twin | 5 each | ~600 each | ~600 | 125 |

**36,828 milliseconds of database time to produce 432 rows.** Add the earnings branch and one visit to that page costs roughly 43 seconds of database work.

**Why each one is slow is a schema fact, not a mystery.** The CTE filters `s."isManual" = false` and joins `clips`, and the day window is applied **after** the CTE, on the aggregated `day` column. So the raw `clip_stats` scan carries **no `checkedAt` bound at all**: a request for the last 7 days still reads the entire history. Every index on `clip_stats` leads with `clipId`, and this query has no `clipId` predicate, so none of them can be used.

**The fix, and it is one fix for all four.** Compute all four metrics in one pass. One `per_day` CTE with four `MAX` aggregates, one `deltas` CTE with four `LAG` windows, one result row per day carrying four numbers. The four `MAX` aggregates are nearly free once the rows are being scanned and grouped anyway.
**Expected saving: about 27 of those 37 seconds, and three quarters of the scans.** **Risk: low.** It is display-only SQL, touches no money file, writes nothing. It still needs its own build and verification pass.

### The 353,687 row scan: found, and it is the worst query on the platform

**Measured, top of `pg_stat_statements` by total time: 9 calls, 14,499 ms total, 1,611 ms mean, 3,184,259 rows returned. That is 353,806 rows per call, against a `clip_stats` table holding 353,934 rows. It reads essentially the entire table, every time.**

The full text, recovered from the catalog:

```
SELECT "clip_stats"."id", "views", "likes", "comments", "shares", "clipId"
  FROM "public"."clip_stats"
 WHERE "clipId" IN ($1 ... $9595)
 ORDER BY "clip_stats"."checkedAt" DESC
 OFFSET $9596
```

**9,595 bind parameters. The query text is 56,786 characters long. There is no `LIMIT`.** The platform has 9,678 clips, so this passes very nearly every clip id on the platform and asks for every snapshot each one ever had.

**This is BL-816's disease in a new place.** BL-816 found `sortBy=views_desc` building an `IN` list of 6,918 bind parameters, which made Postgres re-plan almost every execution, and fixed it by switching to `= ANY($1::text[])`, taking that query from 4,021 ms to 129 ms. This query has the same enormous `IN` list **and** no row limit.

**HONEST LIMIT, STATED RATHER THAN GUESSED: I could not identify its call site with certainty.** I enumerated all 17 `clipStat.findMany` sites. The closest candidates are `src/lib/tracking.ts:3122` and `:3166`, which use `orderBy: {checkedAt: "desc"}` with `distinct: ["clipId"]` and a relation filter that Prisma expands into exactly this shape of `IN` list, and `src/app/api/admin/fraud-review/route.ts:184`, which has no `take:` at all. **Neither matches the selected column list exactly**, so I am not going to name one and be wrong.

**How to settle it in one minute:** run this while reproducing, and read `query` and `application_name` off the live row.
```sql
SELECT pid, application_name, now()-query_start AS running, left(query,120)
  FROM pg_stat_activity
 WHERE state='active' AND query LIKE '%clip_stats%' AND pid <> pg_backend_pid();
```

**The fix, once the caller is known:** replace the `IN` list with `= ANY($1::text[])`, add a `LIMIT`, and if the caller only wants the newest snapshot per clip, use `DISTINCT ON (clipId)` in the database rather than fetching every row and reducing in JavaScript. **Expected saving: 14.5 seconds of database time per nine calls, and 3.18 million rows that never leave the disk.** **Risk: low to medium** depending on the caller.

### The 432,048 rows across 60 calls

60 calls of about 7,200 rows each. Consistent with the per-campaign twin at `src/app/api/client/campaigns/[id]/route.ts:123-162`, which runs the same CTE **four times inside one HTTP request** via `Promise.all` over `["views","likes","comments","shares"]`. Fifteen page views times four queries is sixty. The same single-pass fix applies.

### Indexes named, as owner-triggered steps this round did NOT apply

```sql
-- Serves the per_day CTE's isManual filter and any checkedAt range.
-- Every existing clip_stats index leads with clipId, so a query with no clipId
-- predicate can use none of them.
CREATE INDEX CONCURRENTLY IF NOT EXISTS clip_stats_checkedat_ismanual_idx
  ON public.clip_stats USING btree ("checkedAt", "isManual");

-- Serves the OWNER sidebar's PENDING-accounts badge, which runs on nearly every
-- admin page load and today can use no index at all.
CREATE INDEX CONCURRENTLY IF NOT EXISTS clip_accounts_status_updatedat_idx
  ON public.clip_accounts USING btree (status, "updatedAt");

-- Serves the refresh-account-profiles cron's ORDER BY updatedAt LIMIT 60.
CREATE INDEX CONCURRENTLY IF NOT EXISTS clip_accounts_status_deleted_updatedat_idx
  ON public.clip_accounts USING btree (status, "deletedByUser", "updatedAt");
```

**Read the write-cost warning in PART 3 before adding anything to `clip_stats`.** It is already carrying more index than heap.

---

## PART 2 — how big is `clip_stats`, and where is it going

**Measured, one scan:**

| measure | value |
| --- | --- |
| rows | **353,934** |
| oldest snapshot | `2026-04-22 19:57:55.505` |
| newest snapshot | `2026-09-08 20:01:11.027` |
| span | **139.0 days** |
| lifetime average | **2,546 rows per day** |
| **last 7 days** | **37,267 rows, so 5,324 per day** |
| manual rows (Force Now, and the BL-846/BL-848 sweeps) | 2,288 |
| total size | **144 MB**, of which 46 MB heap and **98 MB index** |
| bytes per row, all in | about **427** |

**The rate has more than doubled against its own lifetime average.** That is the slow accumulation the owner described, in one line.

**Projection at today's 5,324 rows per day, holding clip count flat:**

| horizon | rows | size |
| --- | --- | --- |
| today | 353,934 | 144 MB |
| **+3 months** | **838,000** | **about 340 MB** |
| **+6 months** | **1,328,000** | **about 540 MB** |

**With ten times the clippers, and therefore roughly ten times the tracked clips, that becomes about 53,000 rows a day and roughly 4 GB within six months.** The whole database is 717 MB today.

### The clip-count ceiling, re-derived, and a correction

**The 50,000 clip ceiling is BL-642's, not BL-617's.** BL-617 is an unrelated health check and contains no such figure. The brief attributed it to the wrong round.

BL-642's arithmetic: the campaign spend aggregate measured 2.36 ms over 4,132 clips, which is 0.000571 ms per row, and it is a sequential scan so cost is linear. The trigger it set was **50,000 rows in the aggregate, or p95 over 25 ms**, and 50,000 x 0.000571 is about 28.5 ms.

**BL-642's own watch query, run today:**
```sql
SELECT count(*) AS clips_in_aggregate FROM clips
 WHERE status='APPROVED' AND "isDeleted"=false AND "videoUnavailable"=false;
```
**Answer: 7,108.** That is **14.2 percent of the ceiling**, implying about 4 ms today. **This is not close, and it is not what will break first.**

Full clip population: **9,678 total**, 8,133 APPROVED, 1,410 REJECTED, 51 PENDING, 1 FLAGGED, 83 deleted.

### What could be thinned, and what would be lost. Nothing was deleted.

A clip on a campaign that finished months ago does not need an hourly history forever.

- **Option A, aggregate old snapshots to one row per clip per day.** Beyond 90 days, keep the daily maximum and drop the intra-day rows. **Saves roughly 60 to 80 percent of the old rows.** **What is lost:** the six hour arrival curve, which is BL-775's bot-detection signal, and any future ability to re-examine an old clip's hour by hour climb.
- **Option B, keep only the first and last snapshot per clip on finished campaigns.** **Saves more, near 95 percent on those rows.** **What is lost:** the entire shape of the growth curve on historical clips. Views totals survive.
- **Option C, do nothing and let it grow.** At 540 MB in six months this is survivable on a Small instance. **This is a real option and the honest recommendation for now**, because the query problems above cost far more today than the row count does.

**The stronger argument for A or B is not disk, it is that every full-table scan in PART 1 gets slower in direct proportion.** Fix the queries first and the table size stops mattering for a long while.

---

## PART 3 — every other accumulation

### The two biggest tables are not the ones anybody was watching

| table | rows | total size | recent growth | note |
| --- | --- | --- | --- | --- |
| **email_events** | **377,893** | **200 MB** | **10 per day** | Newest row `2026-09-07 14:02:10`. It grew to 377k in 55 days then effectively stopped. |
| **user_events** | **514,523** | **151 MB** | **4,911 per day** | Still growing. Started `2026-07-13`. |
| clip_stats | 353,934 | 144 MB | 5,324 per day | see PART 2 |
| **apify_usage_entries** | **283,258** | **89 MB** | **6,148 per day** | **The fastest growing table on the platform.** |
| clip_accounts | 1,487 | 28 MB | flat | 27 MB of that is bloat, see below |
| audit_logs | 26,269 | 14 MB | slow | |
| clips | 9,678 | 13 MB | slow | |
| creator_scans | 480 | 11 MB | flat | 10 MB is bloat |
| rule_shadow_decisions | 3,432 | 11 MB | slow | 5 MB is bloat |
| notifications | 14,353 | 8.4 MB | slow | |

**`email_events` at 200 MB is 28 percent of the entire database and has added ten rows a day for the past week.** It is the largest object you own and it is nearly static. Whatever wrote 377,893 rows in 55 days is no longer running. **Worth an owner decision: if the growth engine is off, this is 200 MB of history that could be archived.**

**Combined, these four tables add about 16,400 rows a day and are 584 MB of a 717 MB database.**

### Bloat, and it is real and measured

**`clip_accounts` has 1,487 rows and a 27 MB TOAST relation. I measured the live TOASTable data: `lastVerifyBio` holds 35 kB in total across 394 rows, averaging 55 characters.** Live data cannot exceed about 600 kB. **So roughly 26 MB is dead space that was never reclaimed.**

Same shape on **`creator_scans`** (480 rows, 10 MB TOAST) and **`rule_shadow_decisions`** (3,432 rows, 5 MB TOAST).

**That is the explanation for the 26 percent cache hit rate.** Every read of `clip_accounts` wades through a bloated relation holding almost nothing. And two real queries filter that table with no `userId`, so neither of its indexes applies: the OWNER sidebar's PENDING badge count on nearly every admin page load, and the `refresh-account-profiles` cron. A cold seq scan of a bloated table on a tight loop is exactly a 26 percent hit rate.

**Autovacuum is `on` with a scale factor of 0.2, but the nano instance plainly never kept up.** **The fix is one command per table, and it needs a lock, so it is an owner-triggered step:**
```sql
VACUUM (FULL, ANALYZE) public.clip_accounts;        -- expect 28 MB to fall to under 1 MB
VACUUM (FULL, ANALYZE) public.creator_scans;
VACUUM (FULL, ANALYZE) public.rule_shadow_decisions;
```
**`VACUUM FULL` takes an exclusive lock and rewrites the table.** On these sizes it is seconds, but run it when nobody is working. **Expected saving: about 40 MB and, far more importantly, the cache hit rate on `clip_accounts`.**

### Indexes: 442 of them, and more index than table on the hottest one

**Measured: 442 indexes totalling 383 MB, against a 717 MB database. More than half of what you are paying to store and cache is index.**

**`clip_stats` carries 98 MB of index on 46 MB of heap, and three of them are near duplicates:**

| index | columns | size |
| --- | --- | --- |
| `idx_clip_stats_clip_checkedat_desc` | `(clipId, checkedAt DESC)` | 26 MB |
| `clip_stats_clipId_checkedAt_idx` | `(clipId, checkedAt)` | 26 MB |
| `idx_clip_stats_clip_manual_checkedat_desc` | `(clipId, isManual, checkedAt DESC)` | 26 MB |
| `clip_stats_pkey` | `(id)` | 17 MB |
| `clip_stats_clipId_idx` | `(clipId)` | 3.7 MB |

**A btree scans backwards perfectly well, so `(clipId, checkedAt)` and `(clipId, checkedAt DESC)` do the same work. And `(clipId)` alone is a strict prefix of both.** On the highest-write table on the platform, at 5,324 inserts a day, **every insert currently writes five index entries where two would do.**

**I cannot prove which are unused, and I will not pretend otherwise.** `pg_stat_database.stats_reset` is null and the counters restarted when the instance was upgraded, about fifteen minutes before I looked. 361 of 442 indexes showed zero scans, which means nothing yet. **Run this after a week of normal traffic and it becomes real evidence:**
```sql
SELECT relname, indexrelname, idx_scan,
       pg_size_pretty(pg_relation_size(indexrelid)) AS size
  FROM pg_stat_user_indexes
 WHERE relname IN ('clip_stats','clips','clip_accounts')
 ORDER BY idx_scan ASC;
```

### The tracking cron has a hard ceiling, and a submission rate saturates it long before clip count does

**This is the most important scaling fact in the round, and it is not what anyone expected.**

The cron does not poll every clip on every tick. `CLIPS_PER_TICK` defaults to **30** (`src/lib/tracking.ts:164-178`), the external ping is every 10 minutes, and the hour-claim gate leaves the hour open when a tick hits the cap. **That is a hard ceiling of about 4,320 `clip_stats` writes a day, roughly 180 an hour, and it does not rise when clip count rises.**

**Reconciled against my own measurement, because the two figures disagree and the difference matters.** I measured **5,324 rows a day** over the last 7 days against a cron ceiling of 4,320. The gap is the writes that do not come from the cron: one snapshot at clip creation, manual Force Now checks, and the 2,288 `isManual` rows left by the BL-846 and BL-848 historical sweeps. **So the cron is already running at or near its cap.**

**The age ladder makes old clips nearly free**, and the code says so itself: a dead clip settles at one check every 72 hours, about two cents a month. **Daily writes are approximately `59S + r(N - 10S)`**, where `S` is clips submitted per day, `N` is total active clips, and `r` is between 0.07 and 0.5 checks a day for settled clips. A fresh clip costs about 59 checks across its first 10 days and almost nothing after that.

**So growth in total clips barely moves the load. Growth in the submission rate moves it linearly.** Solving `59S = 4320` gives **about 73 new clips a day, sustained, which on its own saturates the entire cron capacity.**

**And it does not degrade gracefully.** The due-jobs query orders by `checkIntervalMin` ascending, so fresh fast-cadence clips are always collected first. Past saturation **the settled and dead tail simply stops being polled**, silently, which breaks resurrection detection on older clips while fresh ones look perfectly healthy. **Nothing alerts on this.**

**The knob already exists and needs no redeploy:** `CLIPS_PER_TICK` is an environment variable clamped between 5 and 500.

### The vendor bill has no ceiling at all

**Apify is permanently hard off.** `APIFY_HARD_OFF: true` is a compile-time constant with no environment override, enforced by the **11 guards** the brief refers to: five in `apify.ts`, four in `apidojo.ts`, one in `account-profile.ts`, one in `verify-cascade.ts`. Those guards are a vendor circuit breaker. **They are not what stops the cron running away**, which is the row lock, the wall-clock budget and the per-tick cap.

The live providers are **LamaTok** for TikTok and **HikerAPI** for Instagram. **`HIKERAPI_DAILY_BUDGET_USD`, default ten dollars, is an email alarm and not a cap.** The runbook says it plainly: Hiker is never blocked, paused, or rerouted by spend, it always runs. **There is no spend ceiling on the live Instagram provider.** The only brake is the cron's own per-tick cap above.

### Two clean negatives, and one table that is already solved

**`notifications` is the only table on the platform with a working retention policy.** A daily cron hard-deletes read notifications older than 60 days, and keeps unread ones forever by design. **It needs nothing.**

**`marketplace_messages` is a dead table with zero write sites in the entire codebase**, defined in a phase that was never wired up. **`PayoutRefusal` is not a table at all**, it is an in-memory error type, so it cannot accumulate. The brief listed both as accumulations.

**The `audit_logs` cascade problem is already fixed.** BL-835 found the live foreign key cascading on user delete while the schema declared `SetNull`, and **BL-837 corrected it and proved it**. That commit is an ancestor of today's `main`. Confirm with:
```sql
SELECT rc.delete_rule FROM information_schema.referential_constraints rc
 WHERE rc.constraint_name = 'audit_logs_userId_fkey';   -- expect SET NULL
```

**A latent correctness bug found in passing, named because it sends real messages.** `src/lib/marketplace-timers.ts:760-767` reads deadline-reminder notifications with `take: 5000`, **no `createdAt` filter and no `orderBy`**. Once that notification type passes 5,000 rows the dedup lookup can miss recent ones and **send a clipper the same deadline reminder twice**. It runs on every tracking tick.

### Connections: what holds 27 while idle

**Three pollers are mounted for every signed-in user on every page, and none of them stops when the tab is hidden:**

| poller | file:line | interval | visibility guard | database cost |
| --- | --- | --- | --- | --- |
| presence heartbeat | `app-layout.tsx:404` | 30 s | **no** | none, writes to memory |
| notification count | `navbar.tsx:219` | 60 s | **no** | one query, and its cache TTL is 10 s so a 60 s poll **never** hits it |
| call banner | `CallBanner.tsx:90` | 2 min | **no** | one uncached `findMany` with `include` |

**A backgrounded tab, phone locked, still sends 3.5 requests and 1.5 database queries a minute, forever.** At 500 such tabs that is 1,750 requests and 750 queries a minute with nobody doing anything.

**Why that pins connections rather than merely costing queries:** the pool's idle reaper is pg's default **10 seconds**, and neither `src/lib/db.ts` nor `src/lib/db-cron.ts` overrides it. A connection is only reclaimed after a full 10 seconds of complete disuse. Unsynchronised polls from many sessions mean some poll lands in almost every 10 second window. **The 27 connections are not held by one request. They are kept warm by the arrival rate of polls that do nothing.**

**Pools: web `max: 48` at `src/lib/db.ts:107`, cron `max: 10` at `src/lib/db-cron.ts:82`. 58 per Node process. `max_connections` is now 90.** Two Railway instances would be 116 against 90. **Confirm your replica count before scaling out; that alone can reproduce the outage on any instance size.**

`src/lib/use-auto-refresh.ts:27-45` already does this correctly and stops on hidden. The three above simply do not use it.

**No transaction anywhere in `src/` holds a connection across a vendor HTTP call**, checked across 95 `$transaction` sites. **No per-request Prisma client**, only the two singletons. Those are both clean.

### A curiosity worth one line

**`SELECT name FROM pg_timezone_names` ran 4 times for 3,766 ms, a mean of 941 ms each.** Nearly four seconds of database time spent listing timezone names. It is small, but it is free to remove once someone finds what asks for it.

---

## PART 4 — what actually breaks first, ranked

**Ranked by what fails soonest as the platform grows, with the figure at which each bites.**

0. **The tracking cron's per-tick cap, at roughly 73 new clips a day sustained.** **This is the one the owner is about to hit**, because it scales with the submission rate and he is adding hundreds of clippers. Past it, old clips silently stop being polled while fresh ones look fine, and nothing alerts. **The fix is an environment variable, `CLIPS_PER_TICK`, and needs no redeploy.**
1. **The analytics page, already broken.** 43 seconds of database time per visit, today, at 9,678 clips. It scales with total `clip_stats` rows, which are growing 5,324 a day. **At 2x it is roughly 90 seconds. This is the thing that makes the site feel slow and it is a query bug, not an instance size.**
2. **The unlimited `clip_stats` fetch, already broken.** 1.6 seconds and 353,806 rows per call, growing linearly with the table. **At 2x clip_stats it is over 3 seconds and 700,000 rows per call.** No instance size fixes an unbounded query; it just moves the wall.
3. **Connection exhaustion, at roughly 90 concurrent Node processes worth of pool, or 2 Railway replicas.** **This is the one that reproduces the actual outage.** It is set by `max: 48` times replica count against `max_connections` 90, and it does not care how many clippers you have.
4. **Idle poll load, at around 500 to 1,000 concurrent sessions.** 750 queries a minute from tabs where nobody is doing anything. Survivable on Small, wasteful at any size.
5. **`clip_stats` size, at roughly 12 to 18 months** on current growth, or **4 to 6 months at 10x clippers**. Disk is cheap; the cost is that every scan above gets proportionally slower.
6. **Vendor spend, immediately and linearly.** BL-838 measured $146.73 a month at today's volume. **At 10x clips that is roughly $1,470 a month.** **This is the accumulation with no technical cliff and the steepest bill**, and no instance upgrade touches it.
7. **The campaign spend ceiling, at 50,000 clips in the aggregate against 7,108 today.** **Not close. Sixth or seventh on this list, not first.**

**At 2x, 5x and 10x, and which the Small instance survives:**

**Item 0 is driven by the SUBMISSION RATE rather than by clip count, so the figures below understate it if the new clippers are active rather than merely registered.**

- **2x, roughly 300 clippers and 19,000 clips.** Small survives comfortably **if and only if the analytics query and the unbounded fetch are fixed.** Unfixed, the analytics page takes about 90 seconds of database time per visit and one owner visit can stall everything else.
- **5x, roughly 750 clippers and 48,000 clips.** Small survives on CPU and memory. **The pool becomes the binding constraint, not the instance**, and vendor spend is about $730 a month. `clip_stats` is around 1.8 million rows.
- **10x, roughly 1,500 clippers and 96,000 clips.** **Small does not survive this without the query fixes, and with them it probably does.** `clip_stats` approaches 4 GB, the campaign spend aggregate finally crosses BL-642's ceiling at 50,000, and vendor spend near $1,470 a month is the dominant cost.

**Where the honest answer is that instance size is the constraint:** nowhere yet, and that is the useful finding. **The 27 hour outage was a nano instance being genuinely too small, but at Micro and Small the binding constraints are three specific queries, the pool ceiling against the replica count, and the vendor bill.** Upgrading to Large would not fix a query with no `LIMIT`.

---

## PART 5 — security and exposure

**One real finding, live today.**

**`src/app/api/campaigns/route.ts:135-142`** uses `db.campaign.findMany({ where, include: {...} })` with **no `select`**, so every Campaign column is fetched. The only clipper redaction is `shapeCampaignsForClipper` in `src/lib/campaign-clipper-view.ts:78-87`, whose field list strips eight rate and split fields and **does not strip `clientName` or `aiKnowledge`**. Both reach every CLIPPER on the main campaign list, hit on `/campaigns`, the dashboard and the submit flow.

**This directly violates the standing rule that `clientName` and `aiKnowledge` are never selected into any clipper-facing response**, and three sibling routes already treat it as settled: `campaigns/[id]/route.ts:78` destructures both out, `campaigns/past/route.ts:96-118` carries a comment about removing exactly this leak, and `marketplace/listings/[id]/route.ts:165` says they are intentionally not selected. **The main list route was missed by all three.**

**Fix:** convert `:135-142` to an explicit `select:`, the stronger guarantee, rather than adding two more names to the strip list. **Not applied by this round.**

**One finding that is inert today but will not stay inert.** `src/app/api/campaigns/[id]/route.ts:52-89` returns the full campaign row to any non-CLIENT, non-CLIPPER role with **no ADMIN campaign-assignment check** on GET, though PATCH has one at `:217-238`. **Zero accounts hold ADMIN today**, so nobody can use it. It reopens the moment an ADMIN is granted.

**A third, which is both a security and a storage finding.** `src/app/api/upload/route.ts:122` checks session and ban status but **no role**, while its own header comment at `:88-89` claims it is OWNER and ADMIN gated. **Any signed-in clipper can upload 20 files an hour at 5 MB each into the shared public bucket**, with no owning database row required.

**Checked and clean, stated so rather than padded:** all 13 cron routes require `CRON_SECRET` and fail closed. No `process.env` secret in any client component. No client-side Supabase `createClient`, no `.from(table)` call anywhere, so the deny-all RLS posture is intact. `campaigns/spend` still carries BL-840's test-campaign filter. Every other clipper-reachable route uses narrow selects.

**One exposure to weigh rather than fix:** creator-scan evidence screenshots live in the same **public** `uploads` bucket under a random filename, with no signed URL. The API gate is correct; the storage object has no gate at all.

---

## PART 6 — the plan, ranked and costed

### Monitoring, which does not exist

| item | effort | what it buys | needs a click |
| --- | --- | --- | --- |
| **1. A `SELECT 1` health endpoint plus an external uptime monitor to Discord** | 30 min | **Detects the exact outage that happened, in minutes rather than 27 hours** | Yes, UptimeRobot free, and a Discord webhook |
| 2. Supabase database alerts for CPU, disk IO and connections | 10 min | Warns before the cliff rather than at it | Yes, Supabase dashboard |
| 3. Confirm the Railway replica count | 2 min | **48 connections per replica against 90; two replicas reproduces the outage** | Yes, Railway dashboard |

**Every existing alert in the codebase reads or writes the same database it is meant to be watching.** The cron watchdog, the `SERVER_ERROR` capture, the earnings monitors, the `/admin/health` page. During a database outage each one throws or writes nowhere. That is the whole gap in one sentence.

### Code fixes, in value order

| item | file:line | effort | saving | risk |
| --- | --- | --- | --- | --- |
| **4. One query for four metrics** | `admin/analytics/views-by-day/route.ts:374` + `page.tsx:373` | half a day | **about 27 s of 37 s of database time per page visit** | low, display only |
| **5. Bound the unlimited `clip_stats` fetch** | caller unidentified, see PART 1 | half a day incl. identifying it | **14.5 s per 9 calls, 3.18 M rows** | low to medium |
| **6. Stop the three pollers when the tab is hidden** | `app-layout.tsx:404`, `navbar.tsx:219`, `CallBanner.tsx:90` | 1 hour | idle load to near zero, connections drain | very low |
| **7. Close the `clientName` and `aiKnowledge` leak** | `api/campaigns/route.ts:135` | 1 hour | a live data leak to every clipper | low |
| **8. Add the missing role check on upload** | `api/upload/route.ts:122` | 15 min | closes an ungated public write | low |
| **8b. Raise `CLIPS_PER_TICK` before onboarding** | env only, no code | **stops the cron silently starving old clips** | very low, a clamped env var |
| 8c. Fix the duplicate deadline reminder | `lib/marketplace-timers.ts:760` | 15 min | stops sending a clipper the same reminder twice | low |
| 9. Batch the per-payee ban check | `api/payouts/route.ts:148` | 1 hour | 2N queries to 2 | low |
| 10. Raise the notification-count cache TTL to match its poll | `api/notifications/count/route.ts:20` | 5 min | a guaranteed cache miss becomes a hit | very low |

### Schema changes, owner-triggered

| item | effort | saving | risk |
| --- | --- | --- | --- |
| **11. `VACUUM (FULL, ANALYZE)` on the three bloated tables** | 5 min | **about 40 MB, and the 26 percent cache hit rate** | takes an exclusive lock, run when quiet |
| 12. The three indexes in PART 1 | 10 min | turns three seq scans into range scans | additive, `CONCURRENTLY`, safe |
| 13. Drop two of the three duplicate `clip_stats` indexes | 10 min | about 52 MB and two index writes per insert forever | **confirm with a week of `idx_scan` data first** |
| 14. Thin `clip_stats` beyond 90 days | a round | 60 to 95 percent of old rows | loses the arrival curve, see PART 2 |

### Plan and vendor

| item | note |
| --- | --- |
| 15. **Small is the right size and is not the constraint** | The constraints are three queries, the pool against replica count, and the vendor bill |
| 16. **Vendor spend is the steepest curve, and it has NO CAP** | $146.73 a month today, roughly $1,470 at 10x. `HIKERAPI_DAILY_BUDGET_USD` is an email alarm and not a limit, so Instagram spend is uncapped by design. **A spending ceiling does not exist and arguably should.** BL-838 named about $18 a month of safe cuts |
| 17. `email_events` at 200 MB, static since 2026-09-07 | An owner decision: archive it or leave it |

### What could not be measured, stated plainly

- **The call site of the worst query.** Named as unidentified, with the one-minute query to settle it.
- **Unused indexes.** The counters reset at the upgrade. The query to run in a week is given.
- **Railway replica count.** Not visible from here, and it decides item 3.
- **Storage bucket size and orphan count.** Needs the Supabase dashboard.
- **The actual submission rate, which decides item 0 in PART 4.** Run
  `SELECT date_trunc('day',"createdAt")::text, count(*) FROM clips GROUP BY 1 ORDER BY 1 DESC LIMIT 30;`
  and compare it against 73 a day.
- **The real external cron interval.** Two comments in the repo disagree, 5 minutes against 10, and
  `vercel.json` does not list the tracking route at all. **If it fires every 5 minutes the cron ceiling is
  double what I stated and item 0 moves down the ranking.**
- **Whether Prisma compiles a nested `stats: { take: 1 }` into one join or one query per row.** If it is per
  row, `admin/export` at 10,000 clips is a larger villain than the analytics page.
- **A premise correction on the cost report.** `BL-838` exists in the reports repository but not in `docs/`;
  the in-repo cost audit is `BL-540` at $167.72 a month. Both were read and BL-838's newer figures are used.

---

## Honesty notes

**No build was run and none is claimed; this round produced one markdown file and changed no code.** Every figure above is traceable to a query in this report or a `file:line`. Every timestamp is the database's own `now()` or a column cast to `::text`. Ten subagents ran and none was permitted a database connection; all database work went through one sequential connection, with each heavy query's cost stated before it ran. Connections went 29 to 40 against a ceiling of 90 and no read failed. **Two premises in the brief are corrected on the record: the 50,000 clip ceiling belongs to BL-642 and not BL-617, and the largest tables are `email_events` and `user_events`, not `clip_stats`.** No handle, key or wallet address appears anywhere above. The worktree `C:/w856` was removed and verified gone.
