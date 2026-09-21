# BL-920 — every route by which the platform reaches its owner, measured, and the dead ones brought back to life

> **NOTHING IS UNREMOVABLE AND NO SQL IS OWED. FIRST LINE, AS THE ROUND REQUIRES.** Two sandboxes.
> `bl920sbx-` (the proof): 75 ledgered rows, **`VERIFIED: 0 of 75 remain`**, 0 failed.
> `bl920rsbx-` (the renders): 24 ledgered rows, 15 of them written by the product for the sandbox
> people (arrivals, refusals, the re-extraction's audit rows, the frame job's trace rows naming a
> sandbox clip, the sandbox owner's bells), **`0 of 24 remain`** (2 lines were duplicates of rows an
> earlier line had already removed). Counted afterwards: 0 `bl920%sbx-` rows across users, campaigns,
> v2 clips, audit (by user and by target), activity, notifications and the new email ledger.
> **NO REAL PERSON WAS SENT ANYTHING.** The provider key was overwritten with a fake one in the proof
> process BEFORE any send path was imported (asserted, K1); every fan-out was scoped to the sandbox
> owner; the payout reminders ran against fake payouts; the provider was a stub on 127.0.0.1; the
> render server ran with every provider variable unset. Real owner alarm rows were counted before
> and after every part: unchanged. **No real row was written by this round from this machine:** the
> money fingerprints, the payout state fingerprint (status, amount and the three reminder
> bookkeeping columns of every payout) and the real v2 clip status fingerprint are byte-identical
> before and after (PART 7). **The only real rows the fix legitimately writes, in production, after
> the deploy:** `audit_logs` (`TRACKING_TICK_STEPS` every tick, `CRON_JOB_RUN` per job run),
> `cron_runs` heartbeats for six routes that had none, `email_send_outcomes` (one row per send
> attempt), `notifications` for the OWNER accounts when a monitor or the reminder sweep fires,
> `payout_requests.lastReminderTierSent / lastReminderSentAt / remindersSentCount` when a reminder
> fires (never status, never amount), `magic_link_tokens` deletions of used or expired tokens older
> than seven days, and the burst notification's `body / isRead / metadata` rewritten inside its
> window. No paid vendor call, no Apify actor.

**2026-09-21. Shipped on `checkpoint/BL-920` (`876b9326`, backlog `118d792`), merged to `main` as
`98f87993`, pushed and verified (`origin/main == local HEAD`). Tags `pre-BL-920`, `post-BL-920`,
`pre-merge-BL-920`, `post-merge-BL-920`. Branch and merge trees identical by OID. Worktree
`C:\w\b920` removed and verified gone. `checkpoint/BL-723` not merged. All six protected money files
byte-identical by blob OID (`git rev-parse HEAD:<path>`) against `pre-BL-920` and against
`pre-merge-BL-920`; `tracking.ts` in no diff. The 11 BL-678 guards untouched.**

**Model split.** Opus judged every finding, decided owner action versus code defect, wrote every
line that touches a cron entry point or a send path, every proof, and this report. One Haiku reader
read BL-910, BL-917 and HANDOFF PART SEVEN (READ; its summary was used to find lines, every number
below was then read from the source or the database by Opus, VERIFIED). The accessibility lead
reviewed the badge BEFORE its markup was written (READ, then VERIFIED in the renders). Subagents
opened no database connection. Connection cap: one Prisma client per script, one script at a time,
disconnected at exit; the render server held its own pool for about twelve minutes and was killed by
its PID, twice.

**Measurements of my own that were wrong, disclosed.** (1) The render harness first expected the
badge to say 3 (the sandbox clips); it said 6, because the badge counts every pending clip for the
owner, real and sandbox, which is exactly the queue's own total: the expectation was wrong, the code
right. (2) The first render run showed the queue's count sentence WITHOUT its population because the
server had been built before that edit; rebuilt and re-run. (3) A first proof run tripped on my own
proof's untyped callbacks under `tsc`, not on product code.

---

## THE HEADLINE

1. **ELEVEN OF FIFTEEN CRON ROUTES HAD NEVER RUN IN PRODUCTION**, and four of them could not have
   been run by anyone: they were in no registry, no `vercel.json` and no script. Six wrote no
   heartbeat, so a run, a failure and no run were the same silence. Read from `cron_runs`: only
   `tracking` (16,977 rows, the script's), `lifecycle` (6,436), `watchdog` (3,215) and, by side
   effect, `retire-dead-clips` (35 to 49 clips retired at 06:00 UTC every day this week) and
   `clip-liveness-recheck` (three `CLIP_REVIVED` bells) have ever left a trace.
2. **THE TRACKING ROUTE HELD SEVEN POST-STEPS THAT NEVER RAN**: the magic-link cleanup, the L4
   earnings drift probe, the cron-zero-work monitor, the YouTube quota monitor, the
   serializable-retry monitor, the L5 agency-earning monitor and the payout reminder sweep. Every
   one of them exists to tell the owner something. BL-918 found the first member of this family
   (the preview sweep) and moved it; this round moved the rest into `runTrackingPostSteps`, which
   the script Railway runs AND the route both call, and which writes one `TRACKING_TICK_STEPS` row
   every tick with every step's outcome. **An eighth alarm was reachable only through another
   alarm:** the budget hard-lock spike detector ran only on a tick that had also found earnings
   drift (`earnings-monitor.ts`, after the `count === 0` return). It runs every probe now.
3. **THE BURST NOTIFICATION IS NOW THE REAL NUMBER.** It never counted a page; it counted the
   whole population once, at the start of a fifteen-minute window, and dropped every later
   submission as a duplicate (`marketplace-v2-submit-notify.ts`, the `DEDUPED` branch). It now
   REWRITES the window's one message with the count as it stands, counted with
   `v2QueueWhere("pending")`, the queue's own and only filter. Proved on 56 pending clips against a
   page of 50.
4. **THE UNSEEN BADGE EXISTS.** "Marketplace review" carries a pill counting the clips waiting
   for the owner's decision that arrived since he last opened the queue, from the same filter, its
   population in words for a screen reader, seen only on the exact route.
5. **EVERY EMAIL SEND NOW RECORDS ITS OUTCOME** in `email_send_outcomes`: accepted with Resend's
   id, refused with Resend's own words, timed out, errored, or not attempted with the missing
   variable's name. The two addresses BL-910 measured as refused were ACCEPTED on the first live
   tick (ADDENDUM); the owner action in PART 4 applies only if a web-service row reads refused.
6. **THE SITE SAYS WHAT IT RUNS.** `GET /api/version` answers sha, branch and build time baked at
   build from Railway's own variables, and every trace row carries the sha.
7. **A GUARD NOW FAILS THE BUILD ON THIS WHOLE FAMILY** (`check:cron-wiring`, four rules,
   demonstrated failing seven ways, including BL-918's exact defect, tree restored byte-identical).

**PROOFS: 28 of 28 sandbox checks, 30 of 30 HTTP and render checks (7 failure paths each its own
person, 2 success paths, PART 6, 20 renders at 320, 375, 414, 1280 and 1440 in four states), 9 of
9 guard demonstrations, all 19 prebuild guards (18 plus this round's), hooks gate 0 errors 10
warnings against a cap of 11, tsc 0 errors, build exit 0 on the branch and on main.**

**THE COUNT, IN ONE LINE, is at the end, with the production addendum.**

---

## PART 1 — EVERY ROUTE TO THE OWNER, ENUMERATED, AND WHICH ONES ARRIVE (nothing changed here)

**The scheduled and background jobs.** Counted with `find … -name route.ts | grep -c .`: **15**
cron routes; one script; one in-process scheduler (`railway-cron-scheduler.ts`, 11 registered
jobs before this round); the tracking route's post-steps (7, plus the stuck-job sweep and the
LamaTok sampler that precede the batch); two request-triggered background kicks
(`kickV2ThumbnailSweep`, `kickV2FrameJob`, both in the web service, both traced by BL-918 and
BL-919). **What Railway actually invokes:** the cron service runs `scripts/run-tracking-cron.ts`
every ten minutes (every `tracking` heartbeat for the last three hours is the script's,
`isBatchTick=true` at every minute, BL-200's shape; the route writes `false` first and none exist);
the web service runs the in-process scheduler with `RAILWAY_NATIVE_CRON` set, by evidence, to
`lifecycle,watchdog,retire-dead-clips,clip-liveness-recheck` (the four with traces; the docs and the
watchdog comment say `lifecycle,watchdog`, and the retire and liveness traces say the owner added
two). `vercel.json` still lists five schedules and nothing reads it.

| job | entry point | Railway invokes it | last demonstrably ran | evidence | needs |
| --- | --- | --- | --- | --- | --- |
| tracking (batch) | script `run-tracking-cron.ts` | yes, every 10 min | 18:01:11 today | `cron_runs` kind `tracking` | DATABASE_URL, Apify keys |
| tracking route post-steps (7) | HTTP `/api/cron/tracking` | **never** | **never** | zero rows of any of their kinds (no `EARNINGS_DRIFT` probe trace, no reminder bookkeeping, no cleanup) | see PART 2 |
| lifecycle | HTTP via scheduler | yes, every 15 min | 18:00:12 | `cron_runs` `lifecycle` 6,436 | EMAIL_API_KEY, EMAIL_FROM (web has them) |
| watchdog | HTTP via scheduler | yes, every 30 min | 18:00:12 | `cron_runs` `watchdog` 3,215 | EMAIL for CRON_DOWN |
| retire-dead-clips | HTTP via scheduler | yes, daily 06:00 | 06:04:28 today | `clips.videoUnavailableSince` at 06:00 daily, 227 this week | HikerAPI key |
| clip-liveness-recheck | HTTP via scheduler | yes, daily 07:00 | 2026-09-14 07:08 | `CLIP_REVIVED` bells (3), **no heartbeat** | HikerAPI key |
| expire-deadlines | HTTP, registered | **no** (not in the allowlist) | never | 0 `cron_runs` `marketplace-expire-deadlines` | DB |
| discord-role-reconcile | HTTP, registered | no | never | 0 rows | Discord bot token |
| notifications-cleanup | HTTP, registered | no | never | 0 rows | DB |
| decay-strikes | HTTP, registered | no | never | 0 rows | DB |
| counter-recompute | HTTP, registered | no | never | 0 rows | DB |
| marketplace-v2-frames (BL-919) | HTTP, registered opt in | no | never | 0 rows | storage |
| cleanup-magic-links | HTTP, **unregistered** | **could not be** | never | 0 rows | DB |
| expire-submissions | HTTP, **unregistered** | could not be | never | 0 EXPIRED submissions ever | DB |
| refresh-account-profiles | HTTP, **unregistered** | could not be | never | no heartbeat, no marker | Apify (paid) |
| tiktok-analytics-capture | HTTP, **unregistered** | could not be | never | 0 `clip_analytics_snapshots` ever | TikTok import (paid) |

**The second family, asked for by name.** The first family is "routes nobody calls". The second is
"steps inside a route that IS a job", which is where the seven post-steps hid; the third is "jobs
that run and leave nothing", the six heartbeat-less routes. The enumeration above is the union.

**The owner's notifications and emails.** 23 files find OWNER users to notify or email
(`grep -rln 'role: "OWNER"' … | xargs grep -l createNotification|sendEmail`). Every owner-facing
type in `notifications.ts` and its delivery evidence, read from `notifications` joined to the three
OWNER accounts:

| type (trigger) | bell rows ever, last | email | ever delivered in production |
| --- | --- | --- | --- |
| MKT_V2_CLIP_SUBMITTED (a maker submits) | 39, 2026-09-20 12:41 | yes (OWNER_EMAIL_TYPES) | bells yes; email to ONE address only (below) |
| CAMPAIGN_AUTO_PAUSED (budget cap) | 138, 09-11 | yes | bells yes; one address |
| CAMPAIGN_APPROACHING_BUDGET_80 / 90 | 69 / 258, 09-20 | in-app | yes |
| CRON_DOWN (watchdog) | 48, 07-17 | yes | last fired 07-17 |
| CRON_STATUS (watchdog) | 9, 09-08 | in-app | yes |
| BUDGET_PROBE_BYPASS | 23, 09-20 | yes | yes |
| HIKER_OUTAGE_DETECTED / HIKER_BALANCE_LOW | 40 / 4 | yes | yes |
| DISCORD_ROLE_ASSIGN_FAILING | 4, 06-06 | yes | yes |
| CLIP_REVIVED (liveness) | 3, 09-14 | in-app | yes |
| CLIENT_CLIP_FLAG, CLIP_FLAGGED, TRACKING_CLIP_AUTO_DEACTIVATED, REVIEWER_PROPOSAL_PENDING, TRAINER_APPEAL_OPENED, MKT_NEW_LISTING_PENDING, PAYOUT_* decisions, CMNTY_* | 1,440 / 222 / 96 / 12 / 3 / … | in-app or yes | yes |
| **EARNINGS_DRIFT_DETECTED** (L4 probe) | **0** | yes | **never: the probe never ran** |
| **BUDGET_HARDLOCK_SPIKE** | **0** | yes | **never: reachable only through drift** |
| **CRON_0_WORK**, **YOUTUBE_QUOTA_HIGH**, **SERIALIZATION_RETRY_HIGH** | **0 / 0 / 0** | yes | **never: the monitors never ran** |
| **PAYOUT_REMINDER_HEADS_UP / PAY_NOW / OVERDUE** (BL-179) | **0 / 0 / 0** | yes | **never: the sweep never ran** (11 payouts qualify today, 9 past deadline) |
| **STUCK_JOB_SWEEP_SPIKE** | **0** | in-app | never: the sweep never ran (and stays route-only, PART 2) |

Twelve owner-facing types have never fired, all for the one reason. The email channel behind
every "yes" above reaches ONE of the three owner addresses; the other two are refused (below).

**The burst undercount as it stands today.** The number is produced at
`src/lib/marketplace-v2-submit-notify.ts` line 128 (before this round: `const pending = await
db.marketplaceV2Clip.count({ where: { status: "PENDING" } })`), a whole-population database count,
NOT a page: the count itself was never wrong. The message was, because lines 116 to 124 returned
`DEDUPED` for every submission inside the fifteen-minute window after the first, so the number in
the one message was the number at the window's START. Today's rows for the owner's account: the
12:41 window yesterday said "4 clips are now waiting" and one more arrived inside it (5 by the end);
the 07:47 and 05:24 windows said 8 and 7 with one submission each (right); BL-910's day said 3 with
14 by the end. The queue's own derivation is `v2QueueWhere("pending")` at
`src/lib/marketplace-v2-queue.ts:70`, one function, which the count now imports (PART 3).

**The email situation.** Three OWNER accounts: `di…@gmail.com` (created 2026-03-24, the one that
receives), `da…@gmail.com` and `ci…@gmail.com`. `sendOwnerAlert` (`email.ts:1183`) goes through
`sendEmail` (`email.ts:140`) to Resend with `EMAIL_FROM`; BL-908 and BL-910 measured `403
validation_error` on every attempt to the second and third address: Resend's account has no
verified sending domain, and an unverified account may send only to its own login address. **That
is an OWNER ACTION and no code can do it** (PART 4 has the numbered list). The code defect beside it
is that the platform recorded nothing: `sendEmail` returned `false` and wrote the provider's answer
to `console.error` (`email.ts:229`), a Railway log unreachable for two rounds; `notifications.ts`
lines 651 to 659 caught the failure and wrote another `console.error`; `sendOwnerAlert` lines 1210
to 1212 turned any throw into `{ ok: false }`. No table, no row, no way to ask "which address is
refused". Fixed in PART 4. The growth engine's 377,988 `email_events` are 377,441 dry runs and 547
live rows (319 email, 228 in-app), a different channel (marketing consent) and not this family.

**The BL-919 backfill, read back (closes BL-919's only pending confirmation).** The owner has NOT
pressed the backfill button; he has approved two clips since the deploy, and both ran the frame
job in production: **2 `V2_FRAMES_JOB` rows**, 13:24:17 and 13:25:11 UTC, caller `approval`,
attempt 1. Container: linux x64, node v20.20.2, `totalMemMB 393439`, `rssMB 2203` and `1713`,
`tmpFreeMB 1550844` of `3333196` (the host's disk, not a small container volume). Tooling present,
`ffmpeg version N-47683-g0e8eb07980-static`. Downloads: 150,296,610 bytes in 2,273 ms (**66.1
MB/s**) and 150,009,104 bytes in 4,730 ms (31.7 MB/s), both `mp4`, both 200 from
`drive.usercontent.google.com`. Probe 159 and 149 ms; three frames each (604 to 2,151 ms per
frame, 25 to 49 KB); luminance 51.9 to 107.5 (no near-solid frame), default 50 on both;
**`videoDeletedBeforeUpload: true` on both**, `tempDirRemoved: true` on both, `staleTempRemoved:
[]`, no failure, 5,648 and 10,367 ms end to end. 18 approved clips today, **2 with three frames**,
0 absent, 0 locked; the 16 older ones wait for the button.

**What swallows an error on these paths, file:line, before this round.**
`src/app/api/cron/tracking/route.ts` 381 (`await runEarningsMonitor()` unguarded but never
reached), 397 to 399, 407 to 409, 417 to 419, 440 to 442, 476 to 479 (each monitor's `catch` writes
`console.error` and nothing else); `src/lib/email.ts` 229 (`[EMAIL FAIL]` to console, `return
false`), 251 and 256 (timeout and error to console), 1210 to 1212 (`sendOwnerAlert` catch);
`src/lib/notifications.ts` 651 to 659 (`[NOTIFY-FAIL][EMAIL]` to console);
`src/lib/marketplace-v2-submit-notify.ts` 171 to 176 (`FAILED` to console);
`src/lib/payout-reminders.ts` 258, 272, 326, 341, 346 (every failure a `console.error` and a
counter the caller printed to console); `src/lib/earnings-monitor.ts` 69 to 72 (probe SQL failure
returned silently), 175 to 177; `src/lib/operational-monitor.ts` 131 (quota probe failure). Every
one of them now lands in a row: the tick's `TRACKING_TICK_STEPS` entry carries the error text for a
failed step, `email_send_outcomes` carries the provider's words, and the route-level catches stay
as the last line of defence with a row above them.

---

## PART 2 — EVERY DEAD JOB RUNS WHERE RAILWAY RUNS THINGS, AND SAYS SO EVERY TIME

**`src/lib/tracking-post-steps.ts` (new).** `runTrackingPostSteps({ caller, db, batch, dueAtStart
})`, called by `scripts/run-tracking-cron.ts` after its batch (with `dueAtStart` counted before the
batch, as the route did) and by `/api/cron/tracking` in place of its ten blocks. Ten steps, each in
its own try, each recorded as `ok` (with numbers), `skipped` (with the reason) or `failed` (with
the error's words), in one `TRACKING_TICK_STEPS` audit row per run whatever happened:

| step | what it does | credential checked first |
| --- | --- | --- |
| earnings-monitor | L4 drift probe; now returns `{ violationCount, notified }`; the hard-lock spike detector runs on every probe | database |
| cron0-work-monitor | a batch that had due work and did none | database, `dueAtStart` |
| youtube-quota-monitor | 24 h units against the alert percent | database |
| serializable-retry-monitor | in-process retry counters | database |
| agency-monitor | L5, `fix: false`, `{ checked, violations, skippedAmbiguous }` | database |
| v2-thumb-sweep | BL-918's sweep, its own row too | storage (the sweep records its skip) |
| payout-reminders | BL-179's sweep, **at most 5 fires per tick** (`maxFire`) | `PAYOUT_REMINDERS_ENABLED`; email presence recorded |
| magic-link-cleanup | used tokens and tokens expired more than seven days ago | database |
| stuck-job-sweep | **route-only by decision**, recorded as skipped, measured read-only every tick (`soonDue`, `wouldReset`, `wouldThrottle`) | |
| lamatok-shadow-sample | **route-only by decision** (paid vendor sampler, off by default), recorded as skipped | |

The row also carries `env` (which of DATABASE_URL, storage, EMAIL_API_KEY, EMAIL_FROM, ABLY_API_KEY
the process holds, names only), `build` (sha, branch, built at), `frameTooling` (the ffmpeg probe),
the batch's numbers and a `summary` of ok/skipped/failed counts. **Why two stay in the route:** the
stuck-job sweep writes `tracking_jobs.nextCheckAt` (resets some jobs to now, throttles others to 24
hours), which is a tracking cadence decision the pipeline has run without for months, not a
reachability fix; the sampler spends on LamaTok. Both are said in the row every tick rather than
left silent. **Credential facts, stated:** the cron service's `TRACKING_TICK_STEPS.env` will say
whether it holds `EMAIL_API_KEY` and `EMAIL_FROM`; if it does not, the reminder and monitor BELLS
still write (they need only the database) and their EMAILS record `not-attempted: EMAIL_API_KEY is
not set on this service` in `email_send_outcomes`. **Owner action if that is what the row says:** add
`EMAIL_API_KEY` and `EMAIL_FROM` (the same values the web service has) to the Railway **cron**
service. The ADDENDUM reads the first row back.

**`src/lib/cron-run-record.ts` (new)** and the six silent routes: `recordCronRun({ kind, outcome,
reason, metrics })` writes the `cron_runs` heartbeat the watchdog family reads AND one
`CRON_JOB_RUN` audit row with the outcome, so `clip-liveness-recheck`, `retire-dead-clips`,
`refresh-account-profiles`, `tiktok-analytics-capture`, `marketplace/expire-submissions` and
`marketplace-v2-frames` each say ok, skipped (with why: dry run, nothing to do, import cap, no
storage) or failed. **The four unregistered routes are registered** in the scheduler (opt in like
everything there; `refresh-account-profiles` and `tiktok-analytics-capture` are `explicitOnly` so
`*` can never spend on a vendor by accident), at the cadences their own headers name. They remain
OPT IN: enabling any of the eleven route-only jobs is one word in `RAILWAY_NATIVE_CRON` and a
decision, because each of them writes (bans, deletions, counters, vendor spend). Registered is the
fix; enabled is the owner's call, and the BACKLOG says which ones and why.

**The guard.** `scripts/check-cron-wiring.js`, in `prebuild` (19 guards now): **W1** every
`src/app/api/cron/**/route.ts` is registered by exact path; **W2** every registered path has a
route file; **W3** the tick's post-steps have one definition (both entry points call
`runTrackingPostSteps(` exactly once, neither calls any of the seven post-step functions directly,
the shared module calls each at least once); **W4** every cron route records its run
(`cronRun.create(` or `recordCronRun(` on a word boundary). Matching is on word boundaries and
counts are per named file. **Demonstrated failing, one rule at a time, never sampled, each naming
itself, sha256 of every touched file identical afterwards (`bl920-guard-demo.mjs`, 9 of 9):** an
unregistered route (W1), a ghost registry entry (W2), a path renamed with a suffix (trips W1 and W2
both, exact match not substring), the script's call renamed with a suffix (W3, `0 time(s)`), **BL-
918's exact defect reintroduced, `runPayoutRemindersOnce(` called directly from the HTTP route**
(W3 names the file and the function), a post-step renamed out of the shared module (W3, "runs
nowhere"), a route's `recordCronRun(` renamed with a suffix (W4). Green again on the restored tree.

---

## PART 3 — THE TRUTH ABOUT WHAT IS WAITING

**The burst notification** (`src/lib/marketplace-v2-submit-notify.ts`). The count is now `await
db.marketplaceV2Clip.count({ where: v2QueueWhere("pending") })` at line 128, `v2QueueWhere`
imported from `src/lib/marketplace-v2-queue.ts:70`, the one function the queue's "Waiting for you"
tab counts with (`fetchV2QueuePage`, line 136). Inside the window the one message per owner is
**REFRESHED** (a new result value): its body rewritten to "N clips are now waiting for your
decision. Nobody can post them until you approve them.", `metadata.pending` set to N, `isRead`
back to false. The first submission of a window still creates the message and sends the email;
the email's number is the number at that moment and cannot be unsent, which is said plainly.

**The unseen badge** (`src/lib/sidebar-badges-shared.ts`, `src/lib/sidebar-badges.ts`,
`src/components/layout/sidebar.tsx`). A new section `marketplaceReview` on the existing owner-only
pill machinery: count = `db.marketplaceV2Clip.count({ where: { ...v2QueueWhere("pending"),
createdAt: { gt: lastSeen } } })`, the same filter narrowed to what arrived since he last opened
`/market/admin`, stamped "seen" on the EXACT route only (opening the overview at
`/market/admin/overview` does not count, `SIDEBAR_EXACT_SEEN_SECTIONS`). Built to the accessibility
lead's hard requirements: the digits are `aria-hidden` in the pill, a sibling `sr-only` span carries
the REAL number (never the "9+" cap) with a leading separator, so the link reads "Marketplace review,
6 marketplace clips waiting for your decision, new since you last looked"; no `aria-label` on a
span, no `title`, no live region (a sixty-second poll would chatter); hidden at zero. `CountPill`
is used for this section only; the other eight pills are untouched and their bare digits and their
3.39 to 1 contrast are logged for one shared fix (BACKLOG).

**Every count states its population.** The queue's sentence now reads "Showing 6 of 6 clips
waiting for your decision." (and "clips you have decided" on the other tab); the badge's words are
above; the notification's body always said "waiting for your decision"; `SIDEBAR_BADGE_POPULATION`
holds the words for all eight sections for the day the shared fix lands. Nothing else on the queue
was touched. No money figure is computed on any surface this round touched.

---

## PART 4 — THE EMAIL, MADE VISIBLE, AND WHAT ONLY THE OWNER CAN DO

**Fixed in code.** `email_send_outcomes` (`scripts/migrations/BL-920-email-send-outcomes.sql`, run
through `run-schema-sql.js`, 4 statements, 11 columns read back; Prisma model `EmailSendOutcome`;
rollback in the file). `sendEmail` records ONE row on every exit: `accepted` (status, Resend's
`id`), `refused` (status and the provider's body, up to 1,000 characters), `timeout` ("no answer
from the provider within 10 s"), `error` (the exception's message), `not-attempted` ("EMAIL_FROM is
not set on this service", "EMAIL_API_KEY is not set on this service", "recipient is on the
suppression list"). Each row names its `kind`: `owner-alert` (set in `sendOwnerAlert`),
`marketing` (set in the growth engine's one call), `transactional`, `selftest` (the watchdog's
self-test, which posted directly and now records too), or `unknown`. A refused send and an accepted
send are different rows; the boolean the callers get is unchanged.

**Read back after the push (ADDENDUM): the first fifteen production sends, from the cron service at
19:10 UTC, were ACCEPTED by Resend to all three addresses.** The 403 that BL-908 and BL-910 measured on
2026-09-14 came from the web service; whether the web service still meets it is answered by its next
owner alert's row. **If that row reads `refused 403 validation_error`, this is what the owner must do,
with exact values (no code can do this):**

1. Sign in to Resend as the account that owns `EMAIL_API_KEY`.
2. Open **Domains** (https://resend.com/domains) and add **`clipershq.com`** (one P).
3. Add the DNS records Resend shows at your DNS host for `clipershq.com`: the **DKIM** TXT record
   (`resend._domainkey`), the **SPF** TXT record on the sending subdomain Resend names (a value of
   the form `v=spf1 include:amazonses.com ~all`), and the **MX** record it lists for that
   subdomain; then press Verify and wait until the domain reads **Verified**.
4. Make sure `EMAIL_FROM` on the Railway **web** service is an address at that domain (it must be,
   or every send to anyone but your own login address stays `403 validation_error`); the value is
   in Railway, not in this repository.
5. Then read `SELECT "to", outcome, "httpStatus", left(reason, 120), "createdAt"::text FROM
   email_send_outcomes ORDER BY "createdAt" DESC LIMIT 30;` in the Supabase SQL editor. The two
   addresses that read `refused 403` today will read `accepted` with a provider id. (The exact
   Resend sentence the stub used in the proof is the one BL-908 quoted: "The clipershq.com domain
   is not verified. Please, add and verify your domain on https://resend.com/domains".)
6. Optionally, on the Railway **cron** service, add `EMAIL_API_KEY` and `EMAIL_FROM` with the web
   service's values IF the first `TRACKING_TICK_STEPS.env` row reads `emailApiKey: false` (ADDENDUM),
   so a monitor that fires from the cron emails you as well as bells you.

**Sent nothing to a real person.** The proof's provider was a stub on `127.0.0.1:39200`
(`EMAIL_API_URL`, an endpoint override that exists for this and that production never sets); the
key in the process was `bl920sbx-fake-key-never-real` before `email.ts` was imported (K1).

---

## PART 5 — THE SITE SAYS WHAT IT IS RUNNING

`next.config.ts` resolves, ONCE at build time, `RAILWAY_GIT_COMMIT_SHA` and `RAILWAY_GIT_BRANCH`
(Railway's own build variables; `git rev-parse` on a developer machine) and the build instant, and
bakes them into the bundle as `NEXT_PUBLIC_BUILD_SHA / _BRANCH / _TIME`. `GET /api/version` (new,
public, `Cache-Control: no-store`, no auth because the point is that a round can ask production
without a session) answers `{ sha, shortSha, branch, builtAt, appVersion, processUptimeSec }` and
nothing else: no environment, no hostnames, no secrets, no database call. Every trace row this round
writes carries `build.sha` too, so a row says which commit produced it. Locally: `sha 21e7c660…`,
`branch checkpoint/BL-920`, `builtAt 2026-09-21T18:38:24Z`. Production: ADDENDUM.

---

## PART 6 — THE BL-919 LOCKOUT, LABELLED AS THE BOLT-ON IT IS

No code was needed: BL-919 already shipped the per-clip control. `POST
/api/marketplace-v2/admin/clips/[id]/frames` with `{ action: "extract" }`
(`src/app/api/marketplace-v2/admin/clips/[id]/frames/route.ts`, the `extract` branch) resets
`frameAttempts` to 0, clears `frameStatus` and `frameFailedReason`, kicks the job for that one clip,
and writes an `MKT_V2_FRAMES_REEXTRACT` audit row naming the previous attempts and status; the queue's
"Take the three pictures again" button calls it. **Proved on a sandbox clip stuck at three attempts
(P6): 202, `attempts 3 -> 1`** (0 after the reset, 1 as the fresh attempt ran and failed on the
bogus file), the clip still APPROVED, its Drive placeholder untouched. The brief's premise that no
route back existed was inherited from BL-919's brief, not from its shipped code; it is stated here so
it is not repeated.

---

## PART 7 — THE PROOF, THE TEARDOWN, THE MERGE

**`scripts/sandbox/bl920-prove.ts`, 28 of 28**, sandbox `bl920sbx-`: opening snapshot before anything
(users 1785, campaigns 36, clips 10321, v2 clips 27, payouts 252, notifications 15373, email outcomes
0, trace rows 0, real owner bells 2675, six fingerprints). What made each pass:

* **K1** the key in the process is the fake one and the provider URL is the stub, asserted before
  the send path is imported.
* **B1 SKIPPED** (db null): all 10 steps `skipped` with a reason, summary `{ok 0, skipped 10,
  failed 0}`, the row written. **B2 OK beside SKIPPED** (a fake db object for the db-taking steps,
  the monitors on the real database read-only): `earnings-monitor=ok{violationCount 0}`,
  `cron0-work-monitor=ok`, `youtube-quota-monitor=ok`, `serializable-retry-monitor=ok`,
  `agency-monitor=ok{checked 0}`, `magic-link-cleanup=ok{deleted 0}`; `v2-thumb-sweep=skipped`
  naming `SUPABASE_SERVICE_ROLE_KEY`, `payout-reminders=skipped` naming
  `PAYOUT_REMINDERS_ENABLED`, the two route-only steps `skipped` by decision; `env.storage false`,
  `env.emailApiKey true`, `frameTooling.present true`. **B3 FAILED** (a fake db whose
  `magicLinkToken.deleteMany` and `trackingJob.findMany` throw): those two `failed` with the thrown
  words, the others still ran, summary `{5, 3, 2}`. **B4** the three summaries differ. **B5** the
  real owners' alarm rows unchanged (39).
* **C1** seven fake overdue payouts, cap five: `{candidates 7, fired 5, skipped 2, errors 0}`,
  five bookkeeping updates all tier OVERDUE, five bells for the sandbox owner and none for a real
  one. **C2** five `owner-alert` ledger rows, accepted by the stub with a provider id.
* **D1, D2** fifty-three sandbox PENDING clips (prime, above the page of fifty) plus the 3 real
  ones: the first submission `SENT`; the fifty-third `REFRESHED` the ONE message with **"56 clips
  are now waiting for your decision"**, `metadata.pending 56`, equal to the queue's
  `totals.pending` 56 while its page held 50 of them, unread again. **D3** the badge counted 56 in
  the same words; **D4** with the queue stamped seen it fell to 0 while the queue's total stayed 56.
  **D5** the burst's email went to the stub, accepted, and no real owner was told.
* **E1 to E5** accepted (200, id), refused (403, "The clipershq.com domain is not verified…"),
  timeout (10,276 ms, "no answer from the provider within 10 s"), not-attempted ("EMAIL_API_KEY is
  not set on this service"), and refused ≠ accepted.
* **F1 to F6, the full population:** 10,226 live clips, 0 invariant breaches, 0 negative; every
  maker leg's invariant holds; no double pay across agency, maker, platform and posts; 22 budgeted
  campaigns, 0 over budget counting both v2 aggregates and the owner's cut; paid is final for the
  MAKER and the V2 POSTER separately; ANGIE BROWN's budget $2700.00, ACTIVE, spent $5.91. **G1**
  both reconciliation forms: 0 rows each. **H1** every money fingerprint AND the payout state
  fingerprint (status, amount, the three reminder columns of all 252 payouts) identical: **no
  payout state changed** because a reminder fired. **H2** no real v2 clip's status changed, no real
  owner gained a bell (2675 → 2675).

**`scripts/sandbox/bl920-render.mjs`, 30 of 30**, against a PRODUCTION build on port 3920
(`DEV_AUTH_BYPASS=false`, every provider variable unset, fake storage variables so the extract path
runs), sandbox `bl920rsbx-` (an owner, a poster, a maker, a campaign, three PENDING clips, one
APPROVED clip at three attempts, one burst bell written directly with the queue's count). Failure
paths, each its own person, none 429: nobody signed in reading the badge counts 401; the POSTER
reading them 403; the MAKER stamping a section 403; the owner stamping a section that does not exist
400; the tracking route without the secret 500 (401 in production); the POSTER asking for a
re-extraction 403. Success: `/api/version` 200 with exactly six keys; the owner's counts carry
`marketplaceReview` = the queue's total. **Renders** at 320, 375, 414, 1280 and 1440, innerWidth and
URL read back, pan 0 px everywhere, `--bg-page` uses 0 on every page: **badge PRESENT** on the
overview (the pill "6", `aria-hidden`, the link text "Marketplace review, 6 marketplace clips waiting
for your decision, new since you last looked", and the dashboard visit did NOT stamp the queue seen);
**the queue** ("Showing 6 of 6 clips waiting for your decision."); **badge ABSENT** after the queue
was opened (no pill, the link reads only its label); **the notification at its real count** on
`/notifications` ("6 clips are now waiting for your decision" under "Marketplace clips are
waiting"). Phone screenshots carry the install prompt over the page (the BL-918 note); the
assertions are on the DOM.

**Guards.** `npm run prebuild` exit 0 on the branch: 19 guards including `check:cron-wiring`
(15 routes registered and recording, 7 post-step functions in one place). Hooks gate 0 errors, 10
warnings against a cap of 11. `eslint` present in the build log. `tsc --noEmit` 0 errors. `npm run
build` exit 0 on the branch and on main (read from the log, the exit code echoed).

**Teardown.** `bl920sbx-` 75 of 75; `bl920rsbx-` 24 of 24 (15 product-written rows ledgered by a
script that finds them by the sandbox prefix in `userId`, `targetId` or `to`, then destroyed by the
same gate). Zero traces. The render server killed by PID (10696, then 21228 after the rebuild), read
from the port. Worktree removed and verified gone. `sweep-round-leftovers` dry run then `--apply`:
six three-day-old sandbox directories removed (4 MB), seven kept by its refusals.

**The merge.** `pre-merge-BL-920` → `git merge --no-ff` → `98f87993` → `post-merge-BL-920`,
`safe-push` verified. Branch and merge trees identical by OID; main rebuilt afterwards (Prisma
regenerated, build exit 0). Money files by blob OID: six of six SAME against `pre-BL-920` and against
`pre-merge-BL-920`. `checkpoint/BL-723` untouched. BACKLOG 229 → 230 entries.

---

## ADDENDUM — PRODUCTION, READ BACK AFTER THE PUSH

**The first production tick after the push, read back from `audit_logs` at 19:11 UTC (the push
landed at 19:05; the cron service built and ran the new script within six minutes).** One
`TRACKING_TICK_STEPS` row, `caller run-tracking-cron`, **`build.sha 98f8799346460ebc668cb9b7544c301ed9e8296c`,
`branch main`** (the merge commit; `builtAt` is null in the cron process because that script runs
under tsx, not the Next build, so it reads Railway's variables at runtime and has no build instant),
`frameTooling.present true`, `batch { didRunBatch true, processed 1, errors 0, dueAtStart 7074 }`,
**summary `{ ok 7, skipped 3, failed 0 }`:**

| step | outcome | ms | what it said |
| --- | --- | --- | --- |
| earnings-monitor | ok | 31 | `violationCount 0, notified false` |
| cron0-work-monitor | ok | 16 | `dueAtStart 7074, processed 1` |
| youtube-quota-monitor | ok | 13 | |
| serializable-retry-monitor | ok | 0 | |
| **agency-monitor (L5)** | ok | 1,561 | **`checked 7310, violations 92, skippedAmbiguous 126`** |
| v2-thumb-sweep | skipped | 70 | storage not configured on this service (the known BL-918 fact) |
| **payout-reminders** | ok | 4,935 | **`candidates 11, fired 5, skipped 6, errors 0, capPerTick 5, emailConfigured true`** |
| magic-link-cleanup | ok | 12 | `deleted 22` |
| stuck-job-sweep | skipped | 11 | route-only by decision; `soonDue 50, wouldReset 0, wouldThrottle 0` |
| lamatok-shadow-sample | skipped | 0 | route-only by decision; `LAMATOK_SHADOW_SAMPLE_PER_TICK=5` |

**The cron service's credentials, read from the row rather than guessed:** `databaseUrl true,
storage false, emailApiKey true, emailFrom true, ablyApiKey true, payoutRemindersEnabled unset
(default on)`. So no owner action is needed for the cron service's email; the storage pair remains
the BL-918 option.

**Three things the first tick did, all of them the fix working and all of them said here.**
1. **The L5 agency monitor gave its first reading ever: 92 violations across 7,310 agency rows,
   126 skipped as rate-era mismatches.** This round changed no money and did not act on it: the
   monitor runs with `fix: false` and only records. It is exactly what a money guard that never ran
   would find on its first run, and it is the next round's first question (BL-916 changed the
   owner's cut base for marketplace v2 clips; whether these 92 are that era, the pre-BL-916 legacy
   the monitor's `skippedAmbiguous` did not catch, or a live defect is not determined here). The
   number repeats every ten minutes in the row until it is examined.
2. **The payout reminder sweep fired for the first time: 5 of the 11 qualifying payouts (the cap),
   tier OVERDUE, 15 `PAYOUT_REMINDER_OVERDUE` bells (5 payouts × 3 OWNER accounts) at 19:10:36.**
   The five rows read `status REQUESTED, lastReminderTierSent OVERDUE, remindersSentCount 1`; all
   11 qualifying payouts are still REQUESTED; **no payout status or amount changed**. The remaining
   six fire over the next two ticks, then OVERDUE re-fires every six hours per payout (BACKLOG item
   4 says why that wants a digest).
3. **The email ledger's first fifteen production rows, one per reminder email: `owner-alert`,
   `accepted`, `200`, a provider id each, to ALL THREE owner addresses** (`di…`, `da…`, `ci…`). So
   as of 19:10:40 UTC Resend accepts mail to the two addresses that BL-908 and BL-910 measured as
   `403 validation_error` on 2026-09-14: either the domain has been verified since, or the cron
   service's `EMAIL_FROM` is on a verified sender. The web service has not sent since the deploy;
   its next owner alert (the next maker submission) writes its own row, and PART 4's numbered list
   applies only if that row reads `refused 403`.

**`GET https://clipershq.com/api/version` at 19:11:25 UTC:** `200 application/json`, `{ "sha":
"98f8799346460ebc668cb9b7544c301ed9e8296c", "shortSha": "98f87993", "branch": "main", "builtAt":
"2026-09-21T19:07:49.702Z", "appVersion": "0.1.1", "processUptimeSec": 22 }`. The web service runs
the merge commit, built two minutes and forty seconds after the push. Two rounds burned time on this
question; it now takes one request.

**Still unconfirmed in production, said plainly:** the six routes that now write `CRON_JOB_RUN`
rows have written none yet, because none of them was due between the deploy and this reading
(`retire-dead-clips` at 06:00 and `clip-liveness-recheck` at 07:00 UTC are the next two; the other
four are opt in). The web service's first `TRACKING_TICK_STEPS` row through the HTTP route will
never appear, because nothing calls that route, which is the point of the round. The badge and the
burst rewrite run in the web service on the owner's next visit and the next submission; both are
proven on the production build locally and neither leaves a row until a real person acts.

---

**THE COUNT, IN ONE LINE:** **35 of the platform's 36 owner-facing alarm types can now reach him, against 24 of 36 before** (12 could never fire because their jobs never ran; one, the stuck-job spike, stays route-only by decision); **all 3 of his email addresses were accepted by Resend on the first live tick, against 1 of 3 in BL-910**; the burst message carries the real number; the badge exists; and the site answers which commit it runs.
