# BL-939: the tracker never stopped

**Tracking is running and never stopped. The alarm was false.** Since 2026-10-07 18:00 UTC, every ten minute tick has run, and every clip that was due got checked. Two things went wrong instead:

• **CRON_DID_NOTHING has been a false alarm on 1,942 ticks since 2026-09-21.** The monitor counted 7,395 tracking jobs as "due", and every one of them is a job the tracker skips on purpose.
• **The fix is merged and pushed.** The count now uses the tracker's own filter, and a guard stops the two from drifting apart again.

Both CRON_DID_NOTHING and a provider running out of credit now also reach Discord, at most once every 6 hours each. **The owner's one step:** add DISCORD_ALERT_CHANNEL_ID to the Railway cron service. It has the bot token but no alert channel, so the Discord alert cannot post from the cron until it does (Part 4).

Merged to main at d7d8c0d (branch checkpoint/BL-939, tip dc327e0). Tags: `pre-BL-939`, `post-BL-939`, `pre-merge-BL-939`, `post-merge-BL-939`. To roll back: `git reset --hard pre-merge-BL-939`. Both pushes were verified by safe-push (origin == local). Clips are named by the first 8 characters of an md5 of their id. No handle and no key appears here.

## Part 1: is it still happening

All figures come from the platform's own records: the `cron_runs` heartbeat, the TRACKING_TICK_STEPS audit row the tick writes every run, `clip_stats`, and the usage ledger. Every timestamp is the database's own, and the database time at the first read was 2026-10-08 13:45:48 UTC.

**Ticks from 2026-10-07 18:00 to 2026-10-08 13:40 UTC**
• 119 tracking heartbeats.
• No gap longer than 15 minutes.
• 0 `tracking-timeout` rows.
• All 119 ticks ran the batch.
• 0 batch errors.
• 0 failed post steps.

**The :00 ticks** checked 32, 26, 33, 46, 90 (plus 21 at 22:11), 11, 7, 9, 8, 14, 13, 9, 4, 9, 6, 6, 9, 11, 17 and 7 clips, hour by hour. The five ticks after each :00 processed 0 clips with "7,394" or "7,395" due. That is the false alarm (Part 2).

**Fetches since 18:00 yesterday, by provider**

| Provider | Answered | Failed | Notes |
| --- | --- | --- | --- |
| HikerAPI, Instagram | 341 | 34 | Every failure was the post being gone (31) or a profile being gone (3). 0 errors and 0 answers of 402. Last good answer 13:00:28. |
| Instagram fan out | 22 rows, 362 clips | 0 | |
| TikTok, LamaTok only | 9 fan out rows, 26 clips | 0 | 8 LamaTok rows. 1 `none-tiktok` row at 01:00. |

**Freshness**
• Newest automatic ClipStat: 13:00:32 UTC (Instagram) and 12:01:57 UTC (TikTok).
• 346 automatic stats were written since 18:00 yesterday.

**Active, trackable clips** (the tracker's own population): 1,436 in total, 1,213 on Instagram and 223 on TikTok.
• **Overdue now: 0.** Overdue by an hour: 0.
• With no stat in 6 hours: 1,385. In 12 hours: 1,348. In 24 hours: 1,065.
• Those 1,065 are the cadence ladder working as designed:
  ◦ 1,047 sit on cadences of 3 days or slower.
  ◦ 16 sit on 1 or 2 day cadences.
  ◦ 2 short cadence clips sit on PAUSED campaigns: one marked dead, one deferred since 2026-08-23.
  ◦ 3 have never had a stat. They are rejected clips on a paused campaign, on a 5 day cadence.

**CRON_DID_NOTHING rows:** one per owner (3 rows). Each was created 2026-09-21 19:20:58 UTC and refreshed in place every off hour tick since. Before the fix, the last refresh was 13:51:08 today, with metadata "7,395 due, 0 processed".

## Part 2: the cause, by evidence

**The cause**
• `scripts/run-tracking-cron.ts` counted "due" as `isActive && nextCheckAt <= now`.
• The tracker selects with more filters (`src/lib/tracking.ts`, the cron `where.clip` block under `if (!campaignIds)`): clip not deleted, video available, clip not ARCHIVED, campaign not archived and not PAST, COMPLETED or DRAFT.

At 13:46 UTC the 7,395 "due" jobs broke down like this:

| Why the tracker skips them | Jobs |
| --- | --- |
| Campaign PAST | 5,202 |
| Video unavailable | 2,155 |
| Clip deleted | 35 |
| Campaign archived | 3 |
| **Trackable** | **0** |

Every check lands on :00, so the off hour ticks really have nothing to do. Each of them read "7,395 due, 0 processed" and alerted.

That began when BL-920 wired the monitor into the script. The first tick row is 2026-09-21 19:10:40, and the first false alarm came at 19:21:04. Of 2,416 tick rows since, 1,942 were false alarms. The notification is refreshed in place, so its timestamp always looked new. BL-938's sandbox owner had no row yet, received a fresh one at 20:31, and that is why it looked like a first.

**Suspects ruled out**

| Suspect | Evidence |
| --- | --- |
| Instagram provider balance | 341 good answers since 18:00 yesterday, the last at 13:00:28 today. 0 answers of 402 recorded in the usage ledger, ever. No HIKER_BALANCE_LOW since 2026-06-07. Daily volume 518 to 1,087 calls, healthy. No vendor was called to check this, and no free balance endpoint has been verified (BL-933), so none was used. |
| A tick crashing before its loop | 0 batch errors on all 119 ticks. Every tick reported that it ran the batch. |
| A deploy restarting a tick | No heartbeat gap. |
| A lock never released | `cron_locks` is empty, and every tick acquired the lock. |
| The 210 second wall clock | 0 timeout rows. The busiest tick (90 clips) wrote its row 2 minutes after the hour. |
| A configuration change | The env flags are identical on every tick row. |

## Part 3: the fix, and proof that views are not lost

**The fix**
• New `countTrackableDueJobs` (`src/lib/tracking-due-count.ts`) counts exactly the tracker's cron population.
• Both the script and the `/api/cron/tracking` route use it.
• Guard `check:cron-wiring` W5:
  ◦ It refuses a bare `trackingJob.count(` in either entry point.
  ◦ It compares the helper's clip filter with tracking.ts clause by clause, with comments and CRLF removed.
  ◦ It also checks the `isActive` and `nextCheckAt` gates.
  ◦ It was shown failing on 6 mutations, each in its own words: the script count reverted, the route not using the helper, a clause added to the tracker, a clause dropped from the helper, PAST no longer excluded, and the due gate changed. The clean copy passed: 7 of 7.
• tracking.ts was read, never edited.

**Live counts at 14:03:58 UTC**
• Old count: 7,395.
• New count: 0.

**Production after the deploy** (main d7d8c0d, read from the tick rows):
• The first two ticks on the new build, at 14:20:49 and 14:31:27 UTC, each recorded "0 due, 0 processed", with no error and the batch run.
• The same off hour ticks on the old build recorded "7,395 due".
• The CRON_DID_NOTHING bell was last refreshed at 14:11:57, by the last old build tick, and not since.
• The next :00 tick on the new build had not run when this report was written. The memory pressure on this machine stopped my background poll, and I did not restart it. tracking.ts is byte identical, so what a :00 tick processes is unchanged. The last :00 tick, at 14:02 on the old build, checked 8 clips.

**Missed views are recovered.** The tick prices TOTAL views: `earnings-calc.ts:103`, `(views / 1000) * rate`, fed the provider's total at `tracking.ts:2201`. Checked on one clip, f4e82a20, an approved post on the $0.20 campaign:
• Its last two checks were 24 hours apart (2026-10-06 20:01 and 2026-10-07 20:00).
• Its views went from 1,480 to 1,501.
• It holds $0.14. That is 1,501 views at $0.20, which is $0.30 gross, at the 45% poster share. The 21 new views alone would be $0.00.

A late check therefore credits everything up to now.

## Part 4: it cannot be missed again

**CRON_DID_NOTHING** (`src/lib/operational-monitor.ts`)
• Trigger: a tick that ran the batch, with trackable clips due, that checked 0.
• Rate: at most one Discord message per 6 hours while that lasts.

**A provider out of credit**
• Trigger: HikerAPI answering 402 (the branch that already sets its balance cooldown), or LamaTok answering 402 on a video fetch.
• Rate: at most one Discord message per provider per 6 hours.
• The message says Instagram or TikTok clips are not being checked, and where to top up.

**How the rate holds**
• The window lives in `audit_logs` (`INDEPENDENT_ALERT_SENT`, `src/lib/independent-alert-durable.ts`). Railway starts a fresh process every tick, so BL-933's in-memory 30 minute cooldown alone would have allowed six messages an hour.
• If the window cannot be read, the alert sends anyway, so an outage cannot silence its own alarm.
• The kill switch `INDEPENDENT_ALERTS_ENABLED=false` still works.

**Wording fix:** the HikerAPI bell no longer says Instagram "stays on Apify (clippers unaffected)". Apify has been off since BL-678, so it now says Instagram clips are not checked until a top up.

**Demonstrated on sandbox signals: 20 of 20.** The real code paths ran, with fetch stubbed and every write captured in memory: 0 real rows were written and no request left the machine.
• A tick with 41 clips due and 0 checked posted one message to the alert channel and recorded the attempt.
• 36 further ticks, each a fresh process, inside the window posted nothing.
• After the window it posted again.
• With the database unreadable, it still sent.
• With the kill switch off, it stayed silent.
• HikerAPI 402 posted one message naming hikerapi.com, and the fetch result was unchanged ("balance 402").
• LamaTok 402 posted one message naming lamatok.com, and the verdict was unchanged (transient). A second 402 inside the window was silent.

**Whether the cron service can reach Discord** is now written on every tick row, as booleans only: `env.discordBotToken`, `env.discordAlertChannel`.

The first two production rows read **token true, channel false**. The Railway cron service holds the bot token but neither DISCORD_ALERT_CHANNEL_ID nor DISCORD_DROPS_CHANNEL_ID, so from the cron the Discord path would refuse with "no DISCORD_ALERT_CHANNEL_ID or DISCORD_DROPS_CHANNEL_ID configured" and record that refusal once per 6 hours. The bell and email alerts are unaffected.

**The owner's one step:** in Railway, on the cron service, add DISCORD_ALERT_CHANNEL_ID with the id of the channel alerts should go to (the web service's value, if it has one).

## Part 5: safety

**Money files:** all 6 byte identical, by `git rev-parse` of the blob before and after:
• clip-earnings-writer.ts 80418a1
• earnings-calc.ts 0041063
• balance.ts 67c30c8
• tracking.ts dcc8d48
• clip-earnings-invariant-middleware.ts 61cef39
• money-decimal.ts ef5cdae

No earnings rule changed.

**Invariants:** 13 of 13 across the full population at 14:13 UTC.
• 10,340 live clips with earnings equal to base plus bonus, 0 negative.
• No campaign over budget.
• No double legs.
• Both reconciliation forms returned 0 rows.
• ANGIE BROWN: $45.76 spent of its $2,700 budget.

**Build**
• `npm run build` exit 0.
• The prebuild ran all 22 guards and the hooks gate (0 errors, 10 warnings).
• TypeScript clean.
• The merge tree equals the built branch tree (a039dc9).

**Other checks**
• BL-678: 0 lines changed. The hard off test passed 28 of 28, with 0 Apify requests.
• The existing BL-123 monitor test passed 38 of 38.

**Data and connections**
• No real row touched. Reads only, through one connection at a time.
• No vendor called. No `prisma migrate`.
• No `.tsx` file changed, so no render pass was needed.

## Found, not changed (BACKLOG BL-939a to d)

1. Of 1,065 trackable clips with no stat in 24 hours, two short cadence clips on PAUSED campaigns are stale. Not a tracker failure.
2. 5,202 active jobs on PAST campaigns and 2,155 on unavailable videos are never selected. A deactivation sweep would make `isActive` honest.
3. The Railway cron service has no Discord alert channel (`discordAlertChannel: false` on its tick rows). Owner adds DISCORD_ALERT_CHANNEL_ID.
4. LamaTok's out of credit status is assumed to be 402, like HikerAPI's. It was not verified, because that needs a paid call.
