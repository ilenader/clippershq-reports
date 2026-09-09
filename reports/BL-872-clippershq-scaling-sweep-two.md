# BL-872 — the database is fine, the cron is not, and the real number is 512 clips rather than 4,035

**2026-09-09. AUDIT ONLY. Nothing was changed, no index created, no row deleted, no config applied.
One markdown file. No build was run and none is claimed, because a markdown diff cannot change
TypeScript.**

---

## THE ANSWER IN ONE PARAGRAPH

The Small instance is healthy and is not the constraint: 26 of 90 connections, a **99.96 percent
cache hit rate**, 725 MB on disk. **The one real problem is the tracking cron, and it is smaller and
more precise than it first looks.** 8,427 jobs are active and 4,035 are more than 24 hours overdue,
but **79 percent of those are on deliberately long intervals** the auto-ladder set because the clips
stopped growing, so they are not late, they are dormant. **The genuine finding is 512 clips on an
ACTIVE cadence of under a day that have not been checked for 24 days, carrying $876.11.** They are
starved by a sort order that serves fresh clips first, by design, and nothing measures or reports
them. That is worth roughly $70 to $120 a month of clipper earnings and it is the only thing in this
sweep that is costing money today.

## PART 0 — HOW THIS ROUND AVOIDED CAUSING WHAT IT WAS LOOKING FOR

BL-825 exhausted the pool and caused four real failed reads. BL-816 disclosed its own dev server
adding 62 connections. So the concurrency cap here was set at the only number that cannot repeat it:

**ZERO database connections from any subagent.** Every subagent in this round was forbidden from
running a query or any script that opens a connection, and every one of them was given a code or
report assignment only. **Every database query in this report was run by me, serially, one shell at
a time, through `run-select.js`, which opens one short-lived connection and closes it.** At peak this
round held **3** connections of 90, visible in the measurement below as the `(none)` application_name
rows.

Nothing heavy was run. No `VACUUM`, no `REINDEX`, no `pg_stat_statements` reset, no `EXPLAIN ANALYZE`
on a large table. Row counts were taken with `COUNT(*)` on tables whose entire heap fits in the
512 MB buffer pool, which is why the cache hit rate did not move.

---

## PART 1 — WHERE THE PLATFORM STANDS, MEASURED TODAY

All figures below against DB `now()`, cast to `::text`, measured between
`2026-09-09 17:12:33.981042+00` and `2026-09-09 17:17:41.685932+00`.

### The instance

| Measure | Value |
|---|---|
| PostgreSQL | 17.6 on aarch64 |
| Database size | **725 MB** |
| Connections | **26 of 90** (1 active, 17 idle, **0 idle in transaction**) |
| Cache hit rate | **99.96 percent** |
| shared_buffers | 512 MB |
| effective_cache_size | 1.5 GB |
| work_mem | 5 MB |
| Replication slots | 0 |

**Only about four of those 26 connections belong to the app.** The rest are Supabase's own services:
12 idle plus 1 active on Supavisor (the pooler), 2 on Supavisor auth_query, 1 postgres_exporter, 1
postgrest idle for 21 hours, 1 Storage API, 1 pg_net, 1 pg_cron. **Connection exhaustion is not
close**, and because the app reaches Postgres through Supavisor rather than directly, the pooler
absorbs the per-process pool arithmetic BL-856 worried about.

### The WAL did NOT shrink, and it never will

**32 WAL files, 496 MB.** `min_wal_size` is **1024 MB** and `max_wal_size` is **4096 MB**.

**That is configuration, not a leak.** Postgres never recycles the WAL below `min_wal_size`, so
496 MB is not a residue of the crash still draining; it is a floor the server is holding on purpose
and will grow toward 1 GB and stay there. With 0 replication slots, nothing is pinning it. **The
honest finding is that the swelling will not reverse and does not need to**, and the disk budget
should simply be read as 725 MB of data plus up to 1 GB of WAL.

*Sourcing note: the brief attributes the 128 MB to 496 MB figures to BL-855. BL-855 does not contain
them. It explicitly declined to measure infrastructure figures during the outage, on the grounds
that numbers taken then would measure the outage rather than a regression. The 496 MB above is mine,
measured today; the 128 MB baseline I could not source and do not repeat.*

### The tables, largest first

| Table | Rows | Total | Heap | Index | Growth per day | 3 months | 6 months |
|---|---|---|---|---|---|---|---|
| `email_events` | 377,901 | **200 MB** | 77 MB | 123 MB | **8** | 378k | 379k |
| `user_events` | 518,372 | **151 MB** | 58 MB | 94 MB | **4,457** | 920k / 268 MB | 1.32M / 385 MB |
| `clip_stats` | 360,281 | **146 MB** | 46 MB | 100 MB | **5,585** | 863k / 350 MB | 1.37M / 555 MB |
| `apify_usage_entries` | 291,237 | **92 MB** | 60 MB | 33 MB | **6,519** | 878k / 277 MB | 1.47M / 464 MB |
| `clip_accounts` | 1,491 | 28 MB | 584 kB | 272 kB | flat | flat | flat |
| `audit_logs` | 27,849 | 14 MB | 7.9 MB | 6.4 MB | **226** | 48k | 68k |
| `clips` | 9,839 | 13 MB | 6.2 MB | 7.1 MB | ~50 | 14k | 19k |
| `notifications` | 14,647 | 8.5 MB | 3.9 MB | 4.6 MB | slow | | |
| `cron_runs` | **23,166** | 4.5 MB | 2.0 MB | 2.5 MB | **257** | 46k | 70k |
| `activity_events` | **0** | new | | | **0 until redeploy** | | |

Growth traced to a single query counting rows in the last 7 days and last 24 hours by each table's
own timestamp column.

**Tables that grow and never shrink**, meaning no code path deletes from them by age:
`user_events`, `clip_stats`, `apify_usage_entries`, `audit_logs`, `cron_runs`, `email_events` (which
has effectively stopped at 8 rows a day), and `activity_events` once deployed. **`notifications` is
the only table on this platform with a working retention policy**, and BL-856 said the same thing;
it deletes read notifications after 60 days and **keeps unread ones for ever**, of which there are
now **1,751**.

**Projected at six months, on today's rates, the four big tables reach about 1.4 GB combined** from
589 MB today. That is comfortable on a 2 GB instance's disk but it is the number to watch, and it is
dominated by three tables nobody reads.

### The clip ceiling, and a correction

**The 50,000 clip ceiling is BL-642's, not BL-617's.** BL-856 already made this correction and the
brief repeats the original error. BL-617 is a money and invariant audit and contains no such figure.

Re-derived today: **9,839 clips total**, of which the aggregate the ceiling applies to holds about
**7,242 APPROVED, not deleted, not unavailable**. At BL-642's measured 0.000571 ms per row that is
about **4 ms**, against a 25 ms trigger. **Headroom is roughly 7x and this is not what breaks
first.**

### One thing that looks alarming and is not

`pg_stat_user_tables` reports `email_events` with **8 live rows** and `last_autovacuum: never` on
almost every large table, and `pg_stat_database.stats_reset` is NULL. That is the cumulative
statistics collector having been lost, which is what an unclean shutdown does in PostgreSQL 15 and
later. **It is cosmetic.** The planner does not read those counters; it reads `pg_class.reltuples`,
which lives in the catalog on disk and survived: 353,415 against a real 377,901 on `email_events`,
508,467 against 518,372 on `user_events`, 347,045 against 360,281 on `clip_stats`. **Every estimate
is within 7 percent of the truth, so no query is being planned badly.** I raise it only because it
would read as a vacuum emergency to anyone who met it cold.

---

## PART 2 — THE CRON CEILING, VERIFIED INDEPENDENTLY, AND CORRECTED TWICE

### What BL-856 said, and what is actually true

BL-856 computed a ceiling of about **4,320** snapshots a day from `CLIPS_PER_TICK` defaulting to 30
across 144 ticks. **Both halves of that are wrong today.**

Measured over the last 24 hours:

| Measure | Value |
|---|---|
| Tracking cron runs | **128** (not 144), average **11.3 minutes** apart |
| `clip_stats` rows written | **6,527** |
| Of which manual | **0** |
| Distinct clips polled | **2,529** |
| Snapshots per clip per day | **2.58** |
| Implied clips per tick | **51** |

6,527 divided by 128 gives 51 clips a tick, so `CLIPS_PER_TICK` is set in Railway well above the
code default of 30. **I could not read its production value from here and do not guess it.** The real
ceiling is 128 ticks times whatever that number is, and the measured throughput of 6,527 a day is
**51 percent above BL-856's stated 4,320**, so the capacity is larger than that round believed.

### The queue, and the correction that halves the alarm

| Measure | Value |
|---|---|
| Tracking jobs, total | 9,800 |
| **Active** | **8,427** |
| Due now | 4,165 |
| Overdue by more than 1 hour | 4,118 |
| Overdue by more than 6 hours | 4,077 |
| **Overdue by more than 24 hours** | **4,035** |

**MY FIRST READING OF THIS WAS WRONG AND THE CORRECTION IS THE MOST USEFUL THING IN THIS ROUND.**
"Overdue" compares `nextCheckAt` to now, and `nextCheckAt` is set by the auto-ladder, which
deliberately pushes a clip that gained under 10 views in 72 hours to a **3 day** interval and one
that gained under 100 views in 14 days to **15 days**. A dormant clip 37 days past a 15 day interval
has missed about two checks, not 37 days of them.

Split by whether the interval is deliberately long:

| The clip's own cadence | Overdue 24h+ | Approved | Earnings | Avg days overdue |
|---|---|---|---|---|
| **Under 1 day, an ACTIVE cadence** | **512** | **511** | **$876.11** | **24.0** |
| 1 to 2 days, settled | 324 | 323 | $1,717.89 | 44.4 |
| 3 days or longer, dead or dormant BY DESIGN | **3,199** | 2,556 | $8,745.50 | 37.8 |

**79 percent of the backlog is clips the system correctly decided to stop watching closely.** Those
are not a failure.

**THE REAL FINDING IS THE FIRST ROW: 512 clips whose own ladder says they deserve checking at least
daily, unchecked for 24 days on average, carrying $876.11.**

### Why those 512 starve, and it is a deliberate trade

The due-jobs query orders by **`checkIntervalMin` ascending first**, with `nextCheckAt` only as a
tie-break inside a cadence tier (`tracking.ts:3832`). BL-200 made that change on purpose, and its
comment says why: under the per-tick cap the old pure `nextCheckAt` ordering "let 30+ day overdue
dead clips consume the whole budget every tick, starving clips posted an hour ago."

**So the platform chose to starve the old tail rather than the fresh head, which is the right choice.
But there is no fairness guarantee ACROSS tiers**, so whenever short-cadence demand alone fills a
tick, nothing below it moves at all. The 512 are clips that sit at the bottom of their own tier and
never quite get reached.

### Sizing it honestly

The platform's **effective rate is $0.2077 per 1,000 views**, measured as $14,442.48 across
69,519,852 recorded views on 7,242 approved clips.

Clips still on a sub-24-hour cadence are, by the ladder's own definition, not dormant. Using the
measured 30-to-60-day growth rate of **299.5 views per clip per 14 days** as the fair proxy:
512 clips gives about **11,000 views a day**, or **$2.28 a day, roughly $68 a month**.

The 3,199 dormant clips are bounded above by the dormancy threshold itself, under 100 views per 14
days, which is at most another **$4.75 a day** and in practice much less.

**The honest range is roughly $70 to $120 a month of earnings not being credited**, and the part that
is a genuine scheduling failure rather than a design choice is the smaller half of it.

### Would anyone notice? No.

Nothing measures queue depth. Nothing alerts on an overdue tracking job. The cron watchdog checks
only that the cron RAN, not that it kept up, so a cron that fires perfectly 128 times a day while
serving a third of its queue reports itself healthy for ever. A clipper sees their view count stop
moving and has no way to tell that from a video that stopped being watched.

### The new consumers

`activity_events` currently holds **0 rows** because BL-870's recorder has not been deployed yet, so
it costs nothing today and will add its own small load once it is. BL-865's liveness recheck probes
about 290 clips a day but **writes a `clip_stats` row only on a successful revival**, which was
measured at roughly 2.5 percent, so it adds single digits a day to this budget. BL-871's spec'd
chaser is a database query with **zero provider calls**. **Neither is the problem. The problem is the
8,427 jobs already queued.**

### The fix, and it is not code

**It is one environment variable and it is free.** `CLIPS_PER_TICK` is clamped in code between 5 and
500 (`tracking.ts:164-178`) and read from the environment at every call, so raising it needs **no
redeploy**. Going from the current effective 51 to, say, 150 would take daily capacity from about
6,500 to about 19,200, which clears an 8,427 job queue comfortably.

**What it costs.** Every extra poll is one vendor call. At BL-838's measured **$0.00069214** per
HikerAPI request, tripling from 6,527 to 19,200 polls a day adds about **8.8 dollars a day**, which
is **$263 a month on top of the existing $146.73**. That is the honest number and it is not small.

**The cheaper version is to fix the demand rather than the supply**: the auto-ladder should push a
71-day-old settled clip to a much longer interval so it stops competing with a three-day-old one.
That IS code, and it is the better answer, but it needs a round of its own because it changes how
often every clip on the platform is measured.

---

## PART 3 — TWELVE ACCUMULATIONS, EACH MEASURED

| # | Accumulation | Size today | Growth | The cliff | Alerts? |
|---|---|---|---|---|---|
| 1 | **Tracking queue depth** | 4,035 jobs over 24h late | saturated | **already breached** | **NO** |
| 2 | Unused indexes | **281 of 448**, 128 MB | with tables | write cost, no hard cliff | no |
| 3 | TOAST bloat | **43 MB** | static | disk only, no longer performance | no |
| 4 | `clip_stats` | 360,281 / 146 MB | 5,585/day | 1.37M / 555 MB at 6 months | no |
| 5 | `apify_usage_entries` | 291,237 / 92 MB | **6,519/day, fastest** | 1.47M at 6 months | no |
| 6 | `user_events` | 518,372 / 151 MB | 4,457/day | 1.32M at 6 months | no |
| 7 | `audit_logs` | 27,849 | 226/day | 68k at 6 months, trivial | no |
| 8 | `cron_runs` | **23,166** | 257/day | 70k at 6 months, trivial | no |
| 9 | `notifications` unread | **1,751 kept for ever** | slow | trivial | no |
| 10 | `activity_events` | **0**, undeployed | starts on redeploy | 30 day retention already built | no |
| 11 | Connections | **26 of 90** | flat | not close, pooler absorbs | Supabase only |
| 12 | Vendor spend | **$146.73/month** | linear with clips | **no cap exists, only an alarm** | alarm only |

### The three worth naming precisely

**Unused indexes.** 448 indexes holding **388 MB against a 725 MB database, so index is 54 percent of
the whole thing.** 281 have not been scanned since the restart, holding 128 MB. Two dominate:

```
user_events_userId_type_createdAt_idx                    52 MB   0 scans
email_events_userId_triggerId_dryRun_createdAt_idx       40 MB   0 scans
```

Both sit on tables nobody queries any more. **The caveat matters: `idx_scan` counters were lost with
the statistics, so "never scanned" means "not in the last 2.5 days".** An index used weekly by a
report would look identical. BL-856 hit the same wall with 15 minutes of data and said it needed a
week; I have two and a half days and it still needs a week. **These are candidates, not a delete
list.**

One is not a candidate but a duplicate, and it is safe to name:

```sql
-- tracking_jobs_isActive_nextCheckAt_idx, 1544 kB, 0 scans.
-- Redundant with idx_tracking_jobs_active_interval_next, which took 130 scans
-- in the same window, matching the 128 cron ticks. The cron IS index served;
-- it just uses the other one. OWNER TRIGGERED, not applied by this round:
DROP INDEX CONCURRENTLY IF EXISTS tracking_jobs_isActive_nextCheckAt_idx;
```

**TOAST bloat, unchanged since BL-856.** `clip_accounts` is 584 kB of heap and 272 kB of index
carrying **27 MB of TOAST**; `creator_scans` 328 kB carrying **11 MB**; `rule_shadow_decisions`
6 MB carrying **5.4 MB**. About **43 MB reclaimable**. **But the symptom BL-856 attributed to it is
gone**: it reported a 26 percent cache hit rate on `clip_accounts`, and today that table does not
appear in the top twelve by disk reads at all, because 512 MB of shared_buffers on the Small
instance simply holds it. **This is now a disk-space item worth 6 percent of the database, not a
performance item.** The SQL, owner-triggered, takes an exclusive lock and should be run when nobody
is using the site:

```sql
VACUUM (FULL, ANALYZE) public.clip_accounts;
VACUUM (FULL, ANALYZE) public.creator_scans;
VACUUM (FULL, ANALYZE) public.rule_shadow_decisions;
```

**Sequential scans on `clips`.** 3,740 sequential scans reading **36,504,078 tuples** in 2.5 days,
about 1,500 full table scans a day at 9,839 rows each. Today that is free, which the 100 percent
cache hit rate on `clips` confirms. **It is linear: at 50,000 clips it is five times the work, and
that is the same wall BL-642's ceiling describes from the other side.**

### The vendor position, and the one real gap

`HIKERAPI_DAILY_BUDGET_USD` defaults to ten dollars and is **an email alarm, not a cap**. The code
says so in as many words: Hiker is never blocked, paused or rerouted by spend. **There is no ceiling
on the live Instagram provider**, so the cron fix in PART 2 has no automatic brake on it.

YouTube is the opposite and worse in a different way: quota exhaustion is a **hard block** that
**silently freezes every YouTube clip at its last known view count**, with an alarm at 80 percent of
a configurable `YT_DAILY_QUOTA`. LamaTok runs in shadow mode with no cap and no alarm. Browserless,
Sentry and Resend have no ceilings in code. **No vendor key has an expiry or rotation warning
anywhere**, though all are read at call time so rotating one needs no redeploy.

---

## PART 4 — WHAT BREAKS FIRST, WITH A NUMBER

| Order | What | Breaks at | Where it is now |
|---|---|---|---|
| **0** | **Tracking queue depth** | **capacity below ACTIVE-cadence demand** | **ALREADY BROKEN, but 512 clips not 4,035. 8,427 jobs active, 2,529 served a day** |
| 1 | Vendor spend | no cliff, linear | $146.73/month, and it triples if PART 2's fix is applied by raising the cap |
| 2 | `clip_stats` and friends on disk | about 4 GB of a 2 GB instance's disk allowance | 589 MB across four tables, 1.4 GB at six months |
| 3 | Sequential scans on `clips` | ~50,000 clips | 9,839, so **5x headroom** |
| 4 | Campaign spend aggregate | 50,000 rows or 25 ms | 7,242 rows, ~4 ms, **7x headroom** |
| 5 | Connections | 90 | 26, of which ~4 are the app |
| 6 | Cache hit rate | below 90 percent | **99.96 percent** |

### At 2x, 5x and 10x

**2x (about 3,400 clippers, 20,000 clips).** The instance is fine: connections, cache and disk all
have room. **The tracking queue roughly doubles to about 17,000 jobs against the same capacity, and the
starved active-cadence group roughly doubles with it, to about 1,000 clips.** Vendor spend goes to about $290 a month.

**5x (8,500 clippers, 50,000 clips).** The instance is still fine on memory and connections.
**Sequential scans on `clips` reach BL-642's ceiling and the campaign spend aggregate hits 25 ms.**
`clip_stats` growth reaches about 28,000 rows a day and the four big tables pass 3 GB within a year.
Vendor spend is about **$730 a month**, which is the real constraint at this size, not the database.

**10x (17,000 clippers, 100,000 clips).** **Small does not survive this**, but not for the reason
the outage suggests: the failure is vendor cost at roughly **$1,470 a month** and a tracking queue
of 85,000 jobs that no per-tick cap can serve. The database itself would need the next size mostly
for disk and buffer pool.

**Where instance size is simply the constraint.** Nowhere yet. At 99.96 percent cache hit, 26 of 90
connections and 725 MB on a 2 GB instance, **no query fix is needed and no upgrade is needed today.**
The next size up on Supabase is Medium at roughly $110 a month against Small's roughly $25, and
**the honest recommendation is not to buy it yet.**

---

## PART 5 — WHAT WOULD TELL HIM, WHICH IS THE REAL LESSON

### The health endpoint, tested live just now

```
GET https://clipershq.com/api/health
{"ok":true,"ts":1788974286552}
HTTP 200 in 0.172718s
```

**It is byte for byte what it was during the outage.** Its own comment says it is deliberately
lightweight with no database hit. I probed for a database-aware sibling at `/api/health/db`,
`/api/healthz`, `/api/ready` and `/api/status`: **all four return 404. None exists.**

### The deeper problem, which is worse than the health endpoint

**The cron watchdog cannot fire when the database is down, because it reads the heartbeats out of
the database.** `watchdog/route.ts` returns 500 immediately if `db` is unavailable, and otherwise
reads `cron_runs` to decide whether each job is stale. **A monitor that needs the database to tell
you the database is down cannot tell you the database is down.**

Every operational alert on the platform has the same shape. All nine of them, CRON_DOWN,
SERVER_ERROR_SPIKE, YOUTUBE_QUOTA_HIGH, HIKER_BUDGET_THRESHOLD and the rest, are delivered by
writing a `notifications` row and emailing from it. **All nine are silent in exactly the failure they
most need to report.** And there is no external uptime monitor configured anywhere in the repo.

### The specific alerts

| Would have caught | Alert | Configurable in code? |
|---|---|---|
| **The 7 September outage** | An EXTERNAL monitor hitting a DB-touching endpoint | The endpoint yes, the monitor **no, manual** |
| **The tracking backlog** (this round's finding) | Queue depth: count active jobs overdue by more than 6 hours, alert above a threshold | **Yes, entirely in code** |
| Vendor overspend | A real CAP on `HIKERAPI_DAILY_BUDGET_USD` rather than an alarm | **Yes** |
| YouTube freeze | Already exists at 80 percent | Already built |
| Disk growth | A monthly size report | **Yes** |

**The minimum he must do himself, and it is two things.** First, point a free external uptime monitor
at a database-touching endpoint, because nothing inside a system can report that system being down.
Second, decide the `CLIPS_PER_TICK` number, because it trades money for coverage and that is his
call, not mine.

---

## PART 6 — THE PLAN, RANKED AND COSTED

| # | What | Type | Effort | Saves or gains | If ignored | He must |
|---|---|---|---|---|---|---|
| **1** | **Raise `CLIPS_PER_TICK`** | **config** | one variable, no redeploy | clears the active-cadence starvation; recovers roughly $70 to $120/month of clipper earnings | 512 active-cadence clips stay unmeasured | **choose the number** |
| **2** | **A `SELECT 1` health endpoint plus an external monitor** | code + one signup | ~30 min | catches the next outage in minutes not 24 hours | it happens again exactly the same way | **create the monitor** |
| **3** | **Queue depth alert** | code | small | tells him this round's finding automatically | he finds out from a clipper | nothing |
| **4** | Auto-ladder: push settled clips to a longer interval | code | a round | cuts demand instead of buying supply; makes item 1 cheaper | item 1 costs $263/month | nothing |
| **5** | A real cap on HikerAPI spend | code | small | bounds the bill item 1 raises | an unbounded bill | nothing |
| **6** | `DROP INDEX` on the one proven-redundant index | schema | one statement | 1.5 MB and write time | trivial | **run one statement** |
| **7** | `VACUUM FULL` the three bloated tables | maintenance | minutes, exclusive lock | 43 MB, 6 percent of the database | trivial today | **run it when quiet** |
| **8** | Retention on `cron_runs`, `audit_logs`, `apify_usage_entries` | code | small | bounds three unbounded tables | 1.4 GB at six months | nothing |
| **9** | Review the 128 MB of unscanned indexes | analysis | needs a week of counters first | up to 128 MB | write overhead | nothing yet |

**Nothing here is an emergency, including item 1.** Item 1 is worth roughly $70 to $120 a month and
should be done this week, but it is a leak rather than a cliff, and the database it runs on has
years of headroom.

### Is anything close to a cliff? Two prior rounds correctly recommended against building things, so this deserves a straight answer.

**The database is fine and I am not going to manufacture a finding about it.** 99.96 percent cache
hit, 26 of 90 connections, zero idle-in-transaction, planner estimates within 7 percent, 725 MB on a
2 GB instance. **The Small upgrade worked.** BL-856's 26 percent cache hit on `clip_accounts` is gone
without anybody fixing the bloat that caused it, because the larger buffer pool simply absorbed it.
The 50,000 clip ceiling is 5x away. Connections are 3.5x away. **Buy nothing this month.**

**The cron is the exception, and it is a leak rather than a cliff.** BL-856 got its ceiling
arithmetic wrong in both directions and still pointed at the right component. My own first reading
was wrong too, in the alarming direction, until the tier split showed that 79 percent of the
"overdue" population is dormant by design. **What is left is 512 clips on an active cadence,
24 days unchecked, worth $876.11 on the row and roughly $70 to $120 a month in uncredited views, and
nothing anywhere measures or reports it.**

### The single most valuable thing to do this week

**Raise `CLIPS_PER_TICK` and watch the active-cadence overdue count fall.** It is one environment
variable in Railway, it needs no deploy, it is reversible in seconds, and it is the only item on this
list currently costing clippers money. The query to watch it with, which needs no new code:

```sql
SELECT COUNT(*) FILTER (
         WHERE "isActive"
           AND "checkIntervalMin" < 1440
           AND "nextCheckAt" <= now() - interval '24 hours'
       ) AS starved_active_cadence,
       COUNT(*) FILTER (WHERE "isActive") AS active_jobs,
       now()::text AS db_now
FROM tracking_jobs;
```

**It reads 512 and 8,427 today.** The `checkIntervalMin < 1440` clause is the whole point: without it
the number reads 4,035 and most of that is dormant clips behaving exactly as intended. **If the first
column is not falling within a day of the change, the number was not raised enough.**

---

## WHAT COULD NOT BE MEASURED

• **The production value of `CLIPS_PER_TICK`.** It is a Railway variable, not in the repo. I derived
  its effect (51 clips a tick) from throughput rather than reading it.
• **CPU, memory and disk IO percentages.** Those live in the Supabase dashboard, not in SQL. I
  measured the database's own view of itself instead, which is the cache hit rate, connections and
  buffer statistics, all healthy.
• **Whether an index is genuinely unused.** 2.5 days of counters is not enough; a week is.
• **The 128 MB WAL baseline** the brief attributes to BL-855. That report does not contain it.

---

## THE MODEL SPLIT

**Sonnet and Haiku did the mechanical work**, on separate assignments with no overlap: the vendor key
and quota census, the monitoring and health-endpoint code map, the retention audit, the cron budget
code, and the distillation of six prior reports. **None of them was permitted to open a database
connection**, which is what made PART 0's guarantee possible.

**Opus did every measurement and every judgement**: all 17 database queries, deciding that the lost
statistics were cosmetic rather than a vacuum emergency, deciding that the WAL will never shrink and
why that is fine, the failure ordering, and this report. **It also got the headline wrong once.** The
first draft read the 4,035 overdue jobs as 3,390 starved earning clips worth $154 a month. A
subagent's reading of the due-jobs sort order prompted the re-measurement that split the population
by cadence tier and showed 79 percent of it to be dormant by design. **The published number is 512
clips and roughly $70 to $120 a month**, and the correction is in the report rather than quietly
folded away, because a sweep that overstates its own finding teaches the owner to discount the next
one.

**Rough saving: the cheap tiers handled roughly two thirds of the reading volume**, which is where
the token cost of a sweep like this lives. **Nothing money-touching was split**, and the one place it
mattered was the starved-clip exposure: a subagent reporting "$154 a month" would have been a claim
about whether clippers are being underpaid, which is not mechanical work.
