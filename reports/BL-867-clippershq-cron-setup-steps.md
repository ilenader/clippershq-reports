# BL-867 — how to switch on the clip liveness recheck, on the setup you actually have

**2026-09-09. Audit only. Nothing was changed, deployed or configured. Read only.**

**THE SHORT ANSWER: BL-865's instruction named the right variable and the WRONG SERVICE.**
`RAILWAY_NATIVE_CRON` is real and it is already in use, but it belongs on your **web** service, not
on **tracking-cron**. You looked on tracking-cron, correctly found no such variable, and concluded
the instruction was wrong. It was wrong, but only about where to look.

---

## PART 1 — HOW YOUR CRONS ACTUALLY WORK

### There are TWO separate mechanisms, and that is the thing to understand first

**Mechanism A, your four Railway cron services.** Railway's "Cron Schedule" setting runs a service on
a schedule by starting it and running its Start Command. `scripts/run-tracking-cron.ts:1-6` says so
in its own header: *"Railway's Cron Schedule setting runs a service on a schedule by invoking its
startCommand. This script is the startCommand for the cron service."*

**Mechanism B, an in-process scheduler inside the web app.** `instrumentation.ts:15` reads
`RAILWAY_NATIVE_CRON`, and if it is non-empty it starts `startRailwayCronScheduler()` at
`instrumentation.ts:19`. That ticks every 30 seconds and calls the cron endpoints over localhost.

### Service by service

| Your service | What it invokes | How it authenticates | Where the schedule lives |
|---|---|---|---|
| **tracking-cron** | `scripts/run-tracking-cron.ts`, which imports `runDueTrackingJobs` and calls it **directly in-process** (`run-tracking-cron.ts:11-13`) | **None needed.** It never makes an HTTP request, so `CRON_SECRET` is not used on this path | Railway "Cron Schedule" field on the service. **Not in the repo.** |
| **cron-decay-strikes** | `/api/cron/marketplace/decay-strikes` (`route.ts:30-39`) | `Authorization: Bearer <CRON_SECRET>` | Railway "Cron Schedule" field. **Not in the repo.** |
| **cron-expire-deadlines** | `/api/cron/marketplace/expire-deadlines` (`route.ts:83-92`) | `Authorization: Bearer <CRON_SECRET>` | Railway "Cron Schedule" field. **Not in the repo.** |
| **cron-cleanup-magic-lin** | `/api/cron/cleanup-magic-links` (`route.ts:20-29`) | `Authorization: Bearer <CRON_SECRET>` | Railway "Cron Schedule" field. **Not in the repo.** |
| **web** | `npm start` (`railway.json:6`), serves every `/api/cron/*` endpoint | n/a | n/a |

**THE PATTERN, PLAINLY.** One Railway service per job. Railway starts it on a schedule. The service
either runs a script that calls the library directly (tracking-cron) or calls the endpoint over HTTP
with a bearer token (the other three). **Every one of the 14 cron endpoints uses the identical auth
check**: 500 if `CRON_SECRET` is unset, 401 unless the `Authorization` header equals
`Bearer <CRON_SECRET>`.

**WHAT I COULD NOT DETERMINE, STATED RATHER THAN GUESSED.** The Start Command and Cron Schedule of
each of your four services live in the Railway dashboard, not in this repository. `railway.json`
declares only the `web` service. So I can tell you exactly what each endpoint expects, but I cannot
tell you the exact text currently in the Start Command box of `cron-decay-strikes`. Step 6 below
handles that by having you copy it rather than me invent it.

### Does `RAILWAY_NATIVE_CRON` exist, and why did BL-865 name it

**Yes.** It appears in 11 files. It is read in exactly one place that matters,
`instrumentation.ts:15`, and `instrumentation.ts` is Next.js's server boot hook, so it runs **only
inside the `web` service**, which is the only service running `next start`. tracking-cron runs a bare
`tsx` script with no Next server, so `register()` never fires there. **That is precisely why the
variable is not among tracking-cron's 40 variables, and why it never could be.**

It is also already in use. `docs/CRON-ALERT-STORM-AUDIT.md:42` records it measured in production as
`RAILWAY_NATIVE_CRON=lifecycle,watchdog`, and `:58` confirms both fired reliably over 30 hours. So
your `lifecycle` and `watchdog` jobs are running by Mechanism B right now, on the web service.

BL-865 named it because it registered the new job in that scheduler's list
(`railway-cron-scheduler.ts:101`, daily 07:00 UTC). That registration is correct. The instruction
that followed it simply failed to say **which service** to put the variable on, and you reasonably
looked at the cron service.

---

## PART 2 — WHAT THE RECHECK NEEDS

• **Entry point:** `GET /api/cron/clip-liveness-recheck` (`route.ts:22`).
• **Invocation:** header `Authorization: Bearer <CRON_SECRET>` (`route.ts:23-32`). Optional query
  parameters `?dryRun=1` (probe and report, revive nothing), `?max=N`, `?bucket=N` (0 to 4).
• **Frequency:** once a day. It splits the population into five fixed buckets and does one bucket per
  day, so every clip is checked every five days.
• **Run size and duration:** 1,450 clips are flagged right now (1,448 excluding deleted), holding
  $3,933.60, newest mark `2026-09-09 06:03:16.475` against DB `now()` =
  `2026-09-09 13:09:06.923747+00`. One bucket is about **290 clips**. BL-865's full sweep did 1,482
  clips in 39 minutes 26 seconds, which is 1.60 seconds per clip, so **a daily run takes roughly 8
  minutes**.
• **Cost per run:** 290 clips at two provider requests each (a gone clip costs two, because a 404
  falls through to a second lookup) times $0.00069214 = **about $0.40 a day, roughly $12 a month**,
  against your existing Instagram spend of about $139 a month.
• **Snapshot budget: it does not compete.** BL-856's ceiling of about 4,320 snapshot rows a day
  counts `ClipStat` writes, and a clip that is still gone writes no row at all. Only an actual
  revival writes one, and BL-865 measured revivals at roughly 0.7 a day. So this adds under one row a
  day to a 4,320 budget.

**One honest flag.** `route.ts:5` sets `maxDuration = 300`, five minutes, and a run takes about
eight. That setting is a serverless host's timeout and is **not enforced by `next start` on Railway**,
so it should not bite. If it ever did, being cut short is harmless by design: clips still gone are
never written to, and any clip not reached is simply due on the next cycle.

---

## PART 3 — THE EXACT STEPS

**Do steps 1 to 5. Only fall through to step 6 if step 2 tells you to.**

1. Go to **railway.app** and sign in. On the **Dashboard**, click your Clippers HQ **project**.
   You will see your services as tiles: `web`, `tracking-cron`, `cron-decay-strikes`,
   `cron-expire-deadlines`, `cron-cleanup-magic-lin`.

2. Click the **`web`** tile. Not tracking-cron. Click the **Variables** tab. Look for a variable named
   **`RAILWAY_NATIVE_CRON`**.
   • **If it is there** (expected value `lifecycle,watchdog`), go to step 3.
   • **If it is NOT there**, go to step 4.

3. **It exists.** Click the pencil or edit icon on the `RAILWAY_NATIVE_CRON` row. Put the cursor at
   the very end of the existing value and type a comma then the job name, so the whole value reads
   exactly:

   ```
   lifecycle,watchdog,clip-liveness-recheck
   ```

   If your existing value is not `lifecycle,watchdog`, keep whatever is there and just append
   `,clip-liveness-recheck` to the end. Click **Save**, then skip to step 5.

4. **It does not exist.** Click **New Variable**. In the name box type exactly
   `RAILWAY_NATIVE_CRON`. In the value box type exactly:

   ```
   clip-liveness-recheck
   ```

   Click **Add**, then **Save**. Then, still on the `web` service's Variables tab, confirm a variable
   named **`CRON_SECRET`** exists. If it does not, copy its value from the `tracking-cron` service's
   Variables tab and add it here under the same name. Do not paste that value anywhere else and do
   not share it.

5. Railway redeploys the `web` service automatically, taking about a minute. Click the **Deployments**
   tab, wait for the newest row to read **Success**, then click it and click **View Logs**. Within a
   few seconds of boot you should see a line beginning:

   ```
   [RAILWAY-CRON] started. enabled jobs:
   ```

   and `clip-liveness-recheck` must appear in that list. **If you do not see that line, the variable
   did not take: go back to step 2 and check the spelling.**

6. **Only if you would rather have a separate service like your other crons.** Click the
   **`cron-decay-strikes`** tile, then **Settings**. Copy the exact text in the **Start Command** box
   and note the **Cron Schedule** value. Then back on the project screen click **New** then
   **Empty Service**, name it `cron-liveness-recheck`, connect the same GitHub repo, and in its
   **Settings** paste that same Start Command with the path changed from
   `marketplace/decay-strikes` to `clip-liveness-recheck`, and set **Cron Schedule** to `0 7 * * *`.
   In its **Variables** tab add `CRON_SECRET` with the same value as on `tracking-cron`. **Steps 3 to
   5 are simpler and I recommend them**: they are one variable on a service you already run, with no
   new service, no start command and no second copy of your secrets.

### How you will know it worked

**On the next 07:00 UTC** open the `web` service, **Deployments**, newest row, **View Logs**, and
search for `LIVENESS`. You should see, in order:

```
[RAILWAY-CRON] fired clip-liveness-recheck -> HTTP 200
[LIVENESS] bucket=N of 5, ~290 clips due, dryRun=false
[LIVENESS] bucket=N probed 290, revived 0, still gone 290, transient 0, ...
```

**`revived 0` is a normal and good result on most days.** Roughly one clip in 400 comes back, so
most days revive nothing. What matters is that the line appears at all.

To check from the database after a week, run:

```
node scripts/run-select.js "SELECT COUNT(*) AS flagged, now()::text AS db_now FROM clips WHERE \"videoUnavailable\" = true AND \"isDeleted\" = false"
```

and, to see any revivals:

```
node scripts/run-select.js "SELECT type, title, \"createdAt\"::text AS at, now()::text AS db_now FROM notifications WHERE type = 'CLIP_REVIVED' ORDER BY \"createdAt\" DESC LIMIT 5"
```

When a clip does come back you get a bell notification saying so, and the clipper gets one too.

---

## PART 4 — WHAT HAPPENS IF YOU DO NOTHING

**What is already done, permanently, with no further action.** BL-865's one-time sweep already ran
against all 1,482 flagged clips. **34 were revived and $33.30 is counting again for 6 clippers.**
That is finished and it does not need the recurring job. The `tracking.ts` fix in that round also
repaired your **Force Now** button, which had been doing nothing on every clip older than 48 hours,
so you can now revive any single clip by hand from the admin screen whenever you want.

**What only the recurring job adds.** `retire-dead-clips` keeps flagging roughly 30 to 70 clips a
day, and BL-865 measured that **4.34%** of what it flags is wrong and the video eventually comes
back. Across the 761 clips it had flagged, 33 were revivable and they carried $32.48, which is about
$0.98 each. That works out at roughly **two thirds of a clip a day, or about $20 a month** of
already-earned money sitting hidden from its clipper until something looks again.

**SO THE RECURRING JOB IS GENUINELY OPTIONAL, AND I WILL SAY SO PLAINLY.** The alternative is that
you ask for a sweep round every few weeks. The script is already committed
(`scripts/bl865-sweep.ts`, `detect` then `revive`), a full sweep of the whole population costs about
$1 to $2, and it recovers exactly the same money the daily job would. **If you would rather not touch
Railway at all, do that instead. Nothing breaks and nobody loses money permanently**, because the
earnings are never deleted from the row, only hidden while the flag is on.

**A third option, which is code and not configuration.** Your `tracking-cron` service already runs
`scripts/run-tracking-cron.ts` every ten minutes. A small change to that script could run one
liveness bucket once a day inside a run that already happens, which would need **no Railway change
at all, no new variable and no new service**. That is a code round, not something to do in the
dashboard, and it is worth considering if you would rather keep configuration out of it entirely.

---

## WHAT WAS CHECKED, AND HOW

Read only, one document written, no code, config or data touched, nothing deployed. Worktree at
`C:/w867` on `checkpoint/BL-867`, removed at the end. No key or secret is printed anywhere in this
report. Every timestamp is cast `::text` and quoted against DB `now()`.

**Model split, since the round asked for a cheap one throughout.** The mechanical file mapping, which
endpoint exists, which line holds the auth check, what the scheduler registry contains, was done by a
Haiku subagent. I checked its work and **corrected one error before using it**: it read
`railway.json` declaring only the `web` service and concluded your four cron services "are not yet
deployed" and are "architectural plans". That is wrong. Railway services can be created in the
dashboard without any repository entry, and you have told us these services exist and hold 40
variables. Absence from `railway.json` proves only that the repo does not define them. No judgement
in this report rests on that claim.

No build was run and none is claimed. This round changed one markdown file, which cannot affect
TypeScript or the build.
