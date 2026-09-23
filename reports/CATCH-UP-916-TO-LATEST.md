# CATCH-UP: every ClippersHQ round from BL-916 to the latest (BL-923, in flight)

**Written 2026-09-23, 08:06 to 08:20 UTC. AUDIT ONLY.** This is a working handover for whoever writes the next brief. It is not a summary for a reader.

**How it was made.** Everything below comes from one of five sources, and each claim names its source:
1. **Commit messages** on `main` (`git log 109fb3a9..78d12570`).
2. **`BACKLOG.md`**, lines 27331 to 27602 (the BL-916 to BL-922 entries).
3. **The full round reports** in `ilenader/clippershq-reports` (`reports/BL-916-...` to `BL-922-...`).
4. **The session transcripts** of the rounds, for BL-921 (which published nothing) and BL-923 (unfinished).
5. **Fresh read-only queries** against production, run today with `scripts/run-select.js`.

**Tags used on claims.** **VERIFIED** means re-measured today by this audit. **READ** means taken from a round's own report or transcript and not re-derived.

**Constraints kept.** Nothing was changed, built, merged or branched in the ClippersHQ repo. There was no vendor call and no Apify actor. At most one database connection was open at a time: 22 sequential `run-select.js` calls, each one connection, opened and closed. No subagents were used, so none opened a connection. One harmless `GET https://clipershq.com/api/version` was made.

**Model note, disclosed.** The brief asked for the cheapest capable model. This audit ran on Opus with no subagents. The reason: the task is mostly judging which claims survived later rounds, and past retrieval subagents here have read the wrong same-numbered files (BL-919 disclosed exactly that). The cost was about 20 read-only tool calls, no build.

**Why the digest was not also committed to the ClippersHQ repo.** It lives only in the reports repo. The brief said change nothing, and a live session is editing the shared tree's BL-923 worktree right now (see the last section).

---

## 0. READ THIS FIRST: FOUR THINGS THE BRIEF-WRITER DOES NOT KNOW

1. **BL-921 exists, and it was an AUDIT-ONLY round. It shipped nothing: no commit, no report, no backlog entry.** It examined the 92 L5 violations and concluded **open legacy, not a monitor defect and not a live defect**. Its only record is its terminal answer in the session transcript (reproduced in full below). Trap: `reports/BL-921.md` and `reports/BL-923.md` in the reports repo **belong to the OTHER project** (the leadgen clipper-finder). `MANIFEST.tsv` classes them as `leadgen`, dated 2026-08-01. Do not cite them.
2. **BL-923 IS BEING RESUMED RIGHT NOW.** Session `339eae0a` received a "CONTINUE — BL-923 RESUME" brief at 08:01:46 UTC today. It is actively editing `C:\w\b923`: its last edit was at 08:08:49 UTC, on `detail-client.tsx`. The worktree changed while this audit was reading it, from 10 modified files to 13. **Do not brief a second BL-923 resume without first checking whether that session finished.**
3. **A NEW, UNREPORTED MONEY-PATH FINDING (VERIFIED today, not fixed).** BL-917 closed two faces of the Serializable write conflict. A THIRD face has written **6 `TRACKING_RECALC_FAIL` rows since 2026-09-21 17:00 UTC**:
   * Message `"TransactionWriteConflict"`, a `DriverAdapterError` with `code` null.
   * `isTransactionConflict` (`src/lib/clip-earnings-writer.ts:161-166`) tests codes P2034, 40001 and 40P01 plus a message regex. Neither matches this error, so by reading the code the retry treats it as a plain error (READ, not demonstrated).
   * In all 6 rows the proposed `Clip.earnings` equalled the stored value. All 6 clips were written again by later ticks, so no clipper figure is known to be wrong.
   * Not established: whether the proposed owner figure differed. One row proposed owner $0.46; the stored figure at that moment was not captured.
   * 4 of the 6 are on "Zhus Edit (0.50 CPM)" (`cmsisj3d`, PAUSED MANUAL), which is the same campaign BL-917 left open as item 3.
4. **Two numbers in circulation are stale.**
   * **Hooks gate:** the BL-923 brief says "11 warnings against a cap of 11, zero headroom". BL-920 and BL-922 both MEASURED **10 of 11** (READ).
   * **`--bg-page`:** CLAUDE.md and the BL-923 brief say "33 references". Today on `main` there are **0 live uses and 6 mentions, all inside comments**, in 4 files (VERIFIED by `git grep`).

---

## 1. BL-916: the owner's cut on a marketplace clip was taken of the poster's leg alone

**Asked.** The owner's ordinary cut on a v2 clip might be computed on the wrong base, paying him about half his locked guarantee.

**Preceded by BL-915-CHECK, audit only, same session.** BL-915 never ran, and its premise was partly disproved:
* Clip `cmu84hotx009...` carried `marketplaceV2PostId`, all three legs and an AgencyEarning row.
* Across 16 v2 posts there were 0 agency rows without v2 rows. The "missing money" shape did not exist.

**Found (READ, report PART 2, measured on the real clip at 1681 views).**
* The legs were $0.16 + $0.15 + $0.04 = **$0.35**. The stored owner cut was **$0.08**, an owner share of 18.6 percent.
* The correct cut is **$0.17**: $0.17238 / $0.52238 = **0.32998325**, the locked share to eight places.
* History of the row: the approval route wrote **$0.14** from the gross at 1399 views (`review/route.ts:624`). The tick's BL-163 owner lock then multiplied `Clip.earnings`, which on a v2 clip is the poster's 45 percent leg, and wrote the row DOWN while views rose: $0.07 at 1570, $0.08 at 1681.
* **A second live defect:** `gamification.ts recalculateUnpaidEarnings` excluded only `isMarketplaceClip`. So `updateUserLevel` and `updateStreak` rewrote two real v2 posters at **100 percent** of clipper CPM, one second after approval:
  * poster $0.39, maker $0.36, platform $0.08 against a $0.36 gross;
  * poster $0.57, maker $0.54, platform $0.12 against $0.54.

**Changed.**
* `src/lib/owner-share-guard.ts:82` `ownerCutClipperGross`: the one definition of the base. On a v2 clip it is the three legs; on every other clip it is `Clip.earnings`, untouched.
* `tracking.ts`: a protected file, changed on purpose. The owner lock now calls `calculateOwnerEarningsGuaranteed` on that base. `grep -c "s / (1 - s)" tracking.ts` is now 0.
* `agency-monitor.ts` reads the same base, so `--fix` cannot write the row back down (BL-541's self-revert).
* `gamification.ts` excludes `marketplaceV2PostId`.
* Guards: `check:v2-single-share-writers` now discovers writers by the INNER helper too and lists `gamification.ts`. `check:v2-editor-balance` gained S3 (the monitor) and S4 (the sixth excluder) on its allow lists.
* The owner's clip row now says in words which figures are written and which wait for the first check.

**Proved (READ).**
* 42 sandbox checks: **41 passed and 1 failed honestly** (PART 6).
* 10 of 10 failure-path and render checks; 4 of 4 guard demonstrations.
* Control clip: $0.18, $0.28 and $0.34 at 1681, 2677 and 3331 views, identical to the pre-fix inline expression.
* 3,876 of 4,145 ordinary agency rows on guarantee campaigns equal `earnings x s/(1-s)`. The 269 that do not are pre-existing BL-539 shapes.
* The production 11:00 UTC tick wrote gross-based cuts ($0.05, $0.18), which proved by behaviour that the deploy had landed.

**Refused.** No backfill. The tick rewrites agency rows from total views, and the four live rows would self-correct on their next tick:

| clip | before | after |
|---|---|---|
| cmu84hot | $0.08 | $0.17 |
| cmu8fa1r | | $0.18 |
| cmu8tf4p | | $0.28 |
| cmu855k9 | | $0.05 |

The two bases differ by $0.37 in total across the four, all unpaid. BL-921 later confirmed none of these four is among the 92 violations.

**Open, as named by BL-916.**
1. **STILL OPEN (VERIFIED today on main).** The tick's inline committed-spend read (`tracking.ts:2559`, `earningsAgg = tx.clip.aggregate`) and the approval route's (`review/route.ts:637`) omit both v2 aggregates. The L1 lock reads the full figure, so nothing overspends. But per-tick truncation and auto-pause see 55 cents less per v2 dollar.
2. Reconciliation blind to bonuses: CLOSED in BL-917.
3. **OWNER DECISION, never taken.** Approval writes the owner's cut at once, while the three legs wait up to 480 minutes for the first tick. Should approval skip the agency write for v2 clips, as BL-880 made it skip the poster's?
4. The stuck clip `cmu8tf4p`: CLOSED in BL-917.
5. Pre-existing accessibility gaps on the owner's clip row, still open:
   * `text-accent` money is 3.22:1 in the light theme;
   * the "Made by" and "Posted by" links underline on hover only;
   * the trust score number has no accessible name.

**Merged** as `b750a080` (branch `5ea1bfb0`). Report: `reports/BL-916-clippershq-owner-cut-base.md`.

---

## 2. BL-917: the stuck clip, the swallowed money failure, and two faces of one conflict (three merges)

**Asked.** Clip `cmu8tf4p` carried gamification's doubled figures through ticks that wrote a stat and no money, while its job read 0 failures. Investigate before touching any money row.

**Found (READ).**
* The same code corrected the clip from the audit machine in three shapes, so the fault lived in the production process.
* The first `TRACKING_RECALC_FAIL` row (13:00 UTC, VERIFIED today, still in `audit_logs`) named it: `P2034` on `marketplaceV2PlatformEarning.update()`.
* **Mechanism:** at every :00, fifteen campaign groups start at once. Each group's first money transaction reads the v2 aggregates through `getCampaignBudgetStatus` under Serializable isolation. The v2 tables are one index page (17 rows), so any SUM predicate-locks the row being written.
* `cmu8tf4p` had the shortest interval (60 minutes), which made it the first v2 write of every hour.
* **Second face (14:01):** the error read "current transaction is aborted", with code null. The chokepoint's L1 gate catch (`clip-earnings-writer.ts`, after `[F-BUDGET-HARD-LOCK] gate query failed ... passing through`), the fairness gate catch and the v2 sync's point read all swallowed the P2034. The tick's retry was keyed on `code === "P2034"`, so it gave up after one attempt.

**Changed.**
* `3ff484ff` merged as `6b74838f`:
  * the tick writes a `TRACKING_RECALC_FAIL` audit row on a failed money transaction;
  * `DUE_JOB_CLIP_SELECT` became a named constant;
  * `check:v2-single-share-writers` now discovers by `writeClipEarnings(` on a word boundary: 15 writers, W5 and W6 added;
  * `marketplace-v2-sync.ts`: both reconciliation forms compare the earner BASES and require each leg to sum, so a bonus is no longer a leak.
* `c751f94f` merged as `fd74aa01`: retry up to 6 attempts, 500 ms to 8 s doubling plus up to 250 ms jitter (`RECALC_RETRY_MAX_ATTEMPTS`, `recalcRetryDelayMs`). That is 15.5 s of patience where there was 1.5 s.
* `68535ab7` merged as `0da96dfb`: `isTransactionConflict` is exported from the chokepoint, rethrown by all three catches and used by the retry.
* Protected files changed on purpose: `tracking.ts` and `clip-earnings-writer.ts` (blob `416972e9` to `5b40d49e`).

**Proved (READ).** 19 of 19 sandbox checks, 5 of 5 HTTP failure paths, 6 of 6 guard demonstrations. The P2034 schedule is pinned by `bl917-retry-schedule.ts` (6 of 6). The conflict demo ran on a fake transaction, before (swallowed) and after (rethrown).

**Wrote real rows.** One manual `ClipStat`, plus the correction of `cmu8tf4p` through the tick's own code at 12:04:45 UTC: poster $0.26, maker $0.25, platform $0.06, owner $0.28 at 2821 views. The 15:00 UTC production tick then wrote poster $0.28, maker $0.27, platform $0.05, owner $0.30 at 2960 views by itself. Nothing is paid against that clip.

**Corrections to itself.** The first draft said the cause was not nameable; 40 minutes later it named itself. Also, the audit row's `attempts` field records the schedule's MAXIMUM, not the number of attempts reached (a nit, still unfixed).

**Open, as named by BL-917.**
1. `fix-budget/route.ts` and `payouts/[id]/adjust/route.ts` test `isMarketplaceClip` alone and scale the poster leg's stored figure. They are filed as SCALERS, and W6 fails the day either starts naming the v2 identifier. Still open.
2. Closed (the cause was named).
3. A clip on the MANUAL-paused campaign `cmsisj3d` ("Zhus Edit (0.50 CPM)") got no money write at 09:00 and 11:00 on 2026-09-20. Not investigated. **See finding 3 in section 0: 4 of today's 6 new failures are on this campaign.**

Report: `reports/BL-917-clippershq-stuck-recalc.md`.

---

## 3. BL-918: every marketplace preview had failed (27 of 27), and the cause was the site's own CSP (five merges)

**Found (READ).**
* `next.config.ts:76` `media-src 'self' blob: data:` refused the `<video>` before any byte left the browser, within 0 to 4 ms. **BL-878's canvas capture could never have worked.**
* Behind that wall, Drive sends no CORS header, shows an interstitial for 13 files over about 25 MB, and a sign-in page for 4 unshared files.
* Google's `drive.google.com/thumbnail?id=&sz=w640` returned a real frame for 22 of 26 file ids.

**Changed.**
* `0d7f8566` merged as `7efe3702`. `marketplace-v2-thumbnail.ts` now:
  * fetches that picture server side;
  * sniffs the bytes;
  * stores our own copy through `uploadImageToBucket`;
  * writes a STATUS in `thumbnailSource`: `drive-thumbnail`, or one of `ABSENT_NOT_SHARED`, `ABSENT_NO_FILE_ID`, `ABSENT_NO_FILE`, `ABSENT_UNAVAILABLE`, `ABSENT_STORAGE`, each with its plain sentence.
  * The browser capture and its report route are deleted.
* Then, the same evening:
  * `c0da7d74`: a `V2_THUMB_SWEEP` trace row on every attempt.
  * `8e173936`: **the sweep had been wired into the HTTP route's post-steps, which production never calls.** Railway's cron runs `scripts/run-tracking-cron.ts`. The sweep moved there.
  * `aa449775`: **the cron service has no storage credentials.** Its first sweep fetched 17 pictures and lost all 17 at `storage-not-configured`. So the sweep refuses to start without `NEXT_PUBLIC_SUPABASE_URL` + `SUPABASE_SERVICE_ROLE_KEY`. `kickV2ThumbnailSweep` runs it from the poster's catalogue and detail loaders in the web service: single-flight, at most once per 10 minutes per process. `ABSENT_STORAGE` rows retry at once.
  * `47ebeae5`: the backlog close.

**Disclosed (READ, first line of the report).** One real email reached the owner's own address. A sandbox submission ran the real notification, because deleting the provider key before loading `.env.local` did nothing (the file loads afterwards).

**Result then:** 20 of 27 with a picture, 5 saying why not, 2 waiting. **Result now (VERIFIED):**
* 24 v2 clips carry `drive-thumbnail`: the 20 APPROVED and 4 REJECTED.
* 3 are ABSENT: 1 PENDING `ABSENT_NOT_SHARED`, 1 REJECTED `ABSENT_NO_FILE_ID`, 1 REJECTED `ABSENT_NOT_SHARED`.

**Open.**
1. An unshared file and a wrong id are indistinguishable from outside.
2. Pre-existing on the catalogue card: light-theme contrast; hardcoded `text-emerald-400`; the stagger animation ignoring reduced motion. BL-923 is addressing the card.
3. Shared `server-only` shim wanted.
4. **OWNER OPTION:** give the Railway cron service the two storage variables. Still not done: today's tick row reads `v2-thumb-sweep skipped: storage not configured` (VERIFIED).

Report: `reports/BL-918-clippershq-thumbnails.md`.

---

## 4. BL-919: three real frames at 25, 50 and 75 percent; the owner picks; the video is deleted at once

**Changed.** Commit `2fab9d4b`, merged as `21e7c660`.
* On APPROVAL, `approveV2Clip` kicks `kickV2FrameJob` (fire and forget). It runs in the WEB service:
  1. downloads the maker's video to a `v2frames-` temp dir;
  2. probes the duration;
  3. extracts three 640 px JPEGs;
  4. **unlinks the video before the first upload**;
  5. stores the frames and measures luminance on a 16 by 16 grey downscale;
  6. sets the default: 50, unless near solid black or white (then 25, then 75).
* The owner picks a frame on the queue's decided tab (three native radios), can re-extract, and has a deliberate backfill button.
* Every limit is in `src/lib/marketplace-v2-frames.ts`: 600 MB cap, 180 s download, 30 s probe, 60 s per frame, one job per process, 3 attempts, 15 minute lock, 20 minute temp sweep.
* Five new ABSENT codes: `ABSENT_VIDEO_TOO_LARGE`, `_DOWNLOAD`, `_TIMEOUT`, `ABSENT_NOT_A_VIDEO`, `ABSENT_VIDEO_TOOLING`.
* ffmpeg 4.1 and ffprobe 5.2 ship as npm platform packages.
* Schema: 12 columns on `marketplace_v2_clips` (`scripts/migrations/BL-919-v2-video-frames.sql`).

**Proved (READ).** 37 of 37 and 30 of 30. The biggest real clip (322.9 MB) ran end to end in 36.7 s locally. The 16 approved clips then ranged from 23.6 MB to 322.9 MB (2,715 MB in total).

**Disclosed.** Its first Haiku reader read the WRONG files (same-numbered reports of the other project) and its summary was discarded. Lesson: `NULL` is not "not X" in SQL; the first claim used `frameStatus != 'video-frames'`.

**Production, then unobserved and now VERIFIED.** 20 `V2_FRAMES_JOB` rows, from 2026-09-21 13:24:17 to 2026-09-22 18:02:57 UTC, all 20 ok-like by text match. **All 20 APPROVED v2 clips have `frameStatus = video-frames`.**

**Open.**
1. The cron route `/api/cron/marketplace-v2-frames` is OPT IN (`RAILWAY_NATIVE_CRON`). Until the owner adds it, a clip whose first attempt failed is retried only by his button.
2. Google's answer for a bogus id varies by time of day.
3. `--mp-*` tokens are defined only under `.dark`.
4. **PRODUCT QUESTION:** the poster's card now names the maker ("Made by @username") in the absent state, which the poster catalogue never did before. The owner may want it removed.

Report: `reports/BL-919-clippershq-midpoint-thumbnails.md`.

---

## 5. BL-920: every route to the owner, measured, and the dead ones brought back

**Found (READ, PART 1).**
* **11 of 15 cron routes had never run in production.** 4 could not be enabled by anyone, and 6 wrote no heartbeat.
* The tracking route's **seven post-steps had never run**: magic-link cleanup, L4 drift probe, cron-zero-work, YouTube quota, serializable-retry, **L5 agency monitor**, payout reminders.
* An eighth alarm, the hard-lock spike detector, only ran on a tick that had also found drift.
* The burst notification dropped later submissions (BL-910: said 3, real 14).

**Changed.** Commit `876b9326`, merged as `98f87993`.
* `src/lib/tracking-post-steps.ts`: one definition, called by the script and the route. It writes one `TRACKING_TICK_STEPS` row per tick. Reminders are capped at 5 per tick.
* `src/lib/cron-run-record.ts`, plus a heartbeat and a `CRON_JOB_RUN` row in the six silent routes. The four unregistered routes were registered (opt in; the paid ones `explicitOnly`).
* Guard `check:cron-wiring` (W1 to W4), demonstrated failing seven ways.
* The burst message is REWRITTEN with the true count from `v2QueueWhere("pending")`.
* **The "Marketplace review" sidebar count pill** (unseen since last opened, exact route) states its population in words; the queue's count sentence states its population.
* `email_send_outcomes`: the table plus model `EmailSendOutcome`.
* `GET /api/version`.

**Proved (READ).** 28 of 28 sandbox checks, 30 of 30 HTTP and render checks, 9 of 9 guard demos. All 19 prebuild guards pass. **Hooks gate 0 errors, 10 warnings, cap 11.**

**Correction it made to ITSELF (addendum).** PART 1 said two of the three owner addresses were refused by Resend (403 `validation_error`). The first live tick then ACCEPTED all three, from the cron service. **VERIFIED today:** `email_send_outcomes` has 232 rows and **0 refused, ever**: owner-alert 210, unknown 19, marketing 3. So the owner's "verify clipershq.com in Resend" action appears unnecessary.

**First production tick (READ, 19:11 UTC 2026-09-21):**
* `build.sha 98f87993`;
* **L5: checked 7,310, violations 92, skippedAmbiguous 126**;
* payout reminders: candidates 11, fired 5;
* magic-link cleanup: deleted 22.

**Today (VERIFIED, 08:01 UTC tick):** `build.sha 78d12570`; L5 checked 7,278, violations **92**, skippedAmbiguous 126.

**Open.**
1. The stuck-job sweep and the LamaTok sampler are route-only by decision.
2. The other eight sidebar pills put bare digits into link names and measure 3.39:1. BL-923 says it moved all eight onto `CountPill`; unmerged.
3. `--mp-*` tokens are dark-only.
4. **PAYOUT REMINDER VOLUME, now measured (VERIFIED):**
   * 189 of the 210 owner-alert emails since 2026-09-21 19:10 UTC are "Payout overdue" reminders.
   * 11 payouts are REQUESTED and 9 are past their deadline.
   * OVERDUE re-fires every 6 hours per payout, forever. BL-920 suggested a digest.
   * The owner's kill switch is `PAYOUT_REMINDERS_ENABLED=false`.
5. Seven route-only jobs need an env word each plus a decision, because each writes: `expire-deadlines`, `decay-strikes`, `counter-recompute`, `discord-role-reconcile`, `notifications-cleanup`, `cleanup-magic-links`, `expire-submissions`.

Report: `reports/BL-920-clippershq-owner-reachability.md`.

---

## 6. BL-921: the 92 L5 violations (AUDIT ONLY, nothing shipped, no report exists)

**Asked (READ, the brief, 2026-09-21 20:02 UTC).** Is the monitor wrong, or the data? And did any violation postdate BL-916's merge `b750a080`? Change nothing, and publish nothing. The terminal answer was capped at 30 lines.

**Its answer, verbatim in substance (READ, transcript 2026-09-21 20:09 UTC; Opus alone, one Prisma client):**
* **No violation was created or updated after `b750a080`** (merged 2026-09-20 10:30:54Z). The newest agency row among them was created 2026-06-09 11:06:50 and updated 2026-06-23 14:41:57.
* **The monitor is NOT wrong.** Its population, in `src/lib/agency-monitor.ts`:
  * APPROVED, not deleted, not `videoUnavailable`, `isMarketplaceClip = false` clips on CPM_SPLIT campaigns (line 111);
  * v2 posts found via the relation;
  * predicate `Math.abs(expected - actual) > TOLERANCE` with `TOLERANCE = 0.10` (lines 50 and 252);
  * expected = `gross x s/(1-s)` when `guaranteeOwnerSplit` and `|s/(1-s) - oCpm/cCpm| <= 0.01`; skipped as "ambiguous" when they disagree (the 126);
  * gross = `ownerCutClipperGross`, which includes bonus.
  * It uses the same helpers as the writer (`tracking.ts` 2276-2283 and 2900-2940). A replay reproduced 7,310 / 92 / 126 exactly.
* **All 92 are ordinary clips on three PAST campaigns:** "somesome" 88 (s 0.32885906), "bees.n.honey" 3 (s 0.45054945), "GainzAlgo" 1 (s 0.5).
  * 90 have an agency row. 2 are override clips that never had one.
  * Created May 2026 (20) and June 2026 (70).
  * Tracking jobs last checked 2026-08-06, and the tick skips PAST campaigns, so these rows are **FROZEN and will not self-correct**.
* **Signed, actual minus expected:**
  * 63 UNDERPAID, totalling **-$139.96** (median -0.58, largest -79.31);
  * 29 OVERPAID, totalling **+$20.34** (median +0.49, largest +3.72);
  * net **$119.62 owed to the owner**.
* **By clipper-side payout status:** 51 of the 92 clips have a PAID payout after approval.
  * Underpaid: -$102.56 on paid clips, -$37.40 on unpaid.
  * Overpaid: +$18.70 on paid, +$1.64 on unpaid.
  * Agency rows carry no paid marker of their own.
* **Hand-worked examples:**
  * A (-79.31): the row froze at a gross of 153.14 while the clip moved to 315.
  * B (+3.72): the pre-guarantee per-view formula at an older ownerCpm.
  * E (-0.15): the legacy base-only formula, bonus excluded.
  * The two no-row clips: -0.87 and -1.92.
* **BL-916's four clips are not among the 92.**
* **Budget:** correcting every row moves the owner net +$119.62. No campaign would be breached: somesome 5,354.29 of 9,750; bees 2,879.48 of 3,000 (+0.40); GainzAlgo 522.30 of 2,000. ANGIE BROWN is untouched.
* **OWNER OPTIONS (undecided):**
  1. Leave them. The L5 row repeats 92 every tick.
  2. Credit the 63 underpaid (+$139.96).
  3. Also reduce the 29 overpaid (-$20.34 from the owner himself).
  4. Run `--fix` as written. It does both, and it cannot tell an old-era row from drift.
  * Separately, a one-line monitor filter for PAST campaigns would silence the repeat without deciding anything.
* **Not established:** the exact rule each stale row was written under, and why rows stopped updating after 2026-06-23 while clips moved until 06-29.

**ARITHMETIC SLIP IN ITS VERDICT LINE, found by this audit.** It says "$121.26 net sits on paid clips and $35.76 net on unpaid clips". The paid net is **-102.56 + 18.70 = -$83.86**. The 121.26 is 102.56 + 18.70, a gross absolute sum, not a net. Check: 83.86 + 35.76 = 119.62, which matches the stated total. So the paid/unpaid split for a brief is **$83.86 on paid clips, $35.76 on unpaid**, net owed to the owner.

**Today (VERIFIED).** L5 still reads 92 violations, with checked 7,278 (was 7,310) and skippedAmbiguous 126. Nothing has been decided.

---

## 7. BL-922: the owner's clips list scoped by campaign state, in the query

**Found before any code (READ).**
* `/api/clips` applied NO campaign-state predicate for the OWNER since BL-850 (`route.ts:461-466`). The unscoped list already held all 10,232 live clips.
* What hid old campaigns was **rank**: newest first, and the first finished campaign's clip sat at row 289.
* The **campaign picker** could not name PAST campaigns: 26 of 36 named, 0 of the 10 PAST.
* **Correction to BL-850:** its claim that the picker "can name every campaign now" was not what shipped.
* Era (`campaign-era.ts`) is a money concept and excludes nothing from lists.

**The mapping,** once, in `src/lib/campaign-state-scope.ts`:

| owner's word | column value |
|---|---|
| running | ACTIVE |
| paused | PAUSED with pauseSource MANUAL or null |
| frozen | PAUSED with pauseSource AUTO |
| completed | COMPLETED |
| finished | PAST |
| archived | isArchived |

The first five require `isArchived = false`. Populations on 2026-09-21: 29 / 1,179 / 939 / 162 / **6,835** / 1,088, and draft 0.

**Changed.** Commit `c32ec1af`, merged as `d19025ec`.
* A "Campaign state" `MultiDropdown` on `/admin/clips`, OWNER only.
* Sent as `campaignStates=` and applied in `where.campaign` (`route.ts:488-493`).
* An id tie-break on the sort (`:859`).
* `totalCountAllStates` is echoed only when a scope applies (`:1064-1072`).
* The count sentence reads both figures from the server.
* The selection persists in `sessionStorage`.
* The picker sends `includePast=true` for the OWNER: **36 of 36**.
* Guard `check:clips-list-scope` (S1 to S6) in prebuild, demonstrated 10 of 10.

**Proved (READ).**
* 40 of 40 on two production builds side by side. The default view is byte-identical: the same 30 ids, the same order, the same 10,232.
* Finished walked to 6,835 over 7 pages with 0 duplicates. Offset 6,000 served.
* 0 archived rows among the other five words.
* 21 of 21 renders, pan 0.
* ANGIE BROWN budget $2,700.00, spent $6.03 at the time.
* The hooks gate measured 10, not the brief's 11.

**OWNER DECISIONS PUT TO HIM, not taken.**
1. The default view still includes archived clips (1,088). That is BL-850, on his instruction. Excluding archived is one line in `fetchPage`, and the total would become 9,144.
2. Clippers' `/api/clips/mine:106` hides ARCHIVED campaigns' clips only. The poster's v2 dashboard hides nothing.

**Open.**
1. The Track modal's per-campaign counts come from loaded rows. An endpoint `/api/admin/campaigns/[id]/clip-count` exists.
2. REVIEWER and ADMIN ignore `campaignStates` (0 ADMIN accounts).
3. Six a11y SHOULD-FIX items on the shared `MultiDropdown`.
4. A non-archived DRAFT campaign's clips fall in no scoped word.
5. `/api/campaigns` `archived=true&includePast=true` returns archived rows only; the flag name misleads.
6. It needed a Railway redeploy. It has one: see section 9.

Report: `reports/BL-922-clippershq-clips-campaign-scope.md`.

---

## 8. BL-923 (in brief): the marketplace made obvious on a phone. UNMERGED, IN FLIGHT. Full handover in section 11.

---

## 9. CURRENT STATE OF PLAY (VERIFIED, db `now()` = 2026-09-23 08:06:27 UTC unless stated)

### Code and deploy

* **`main` = `78d12570`** ("BL-922: the full report (doc only)"). Production runs it: `GET /api/version` returned `78d12570cf25b2eaac37e23735cae7ec81289bd3`, `builtAt 2026-09-22T09:57:14Z`. The cron tick row agrees.
* `origin` has **no** `checkpoint/BL-923` branch and no BL-923 tags. `pre-BL-923` exists locally only.

### Marketplace v2 population

| metric | value |
|---|---|
| v2 clips | **27**: 20 APPROVED, 1 PENDING, 6 REJECTED. Newest submitted 2026-09-20 12:43:44, so no maker has submitted in three days |
| v2 posts | **39**, on 16 distinct v2 clips. All 39 tracking jobs active. 16 posted in the last 48 hours; newest 2026-09-23 00:38:31 |
| post clip status | 27 APPROVED, 4 PENDING, 8 REJECTED |
| makers (distinct submitters) | **6** |
| posters (distinct) | **9** |
| test users among makers or posters | 0 |
| side chosen | **37** users (1 is a test user): EDITOR 11, POSTER 26 |
| side chosen by non-test CLIPPERs | 36; 5 chose in the last 48 hours |
| users | 1,788 total, of which 1,731 are non-test CLIPPERs. Briefs still say 1,771 |

### The live funnel

* **Arrived** (this audit's definition): **50** non-test CLIPPERs have any `activity_events` row on an `mkt2.*` surface since the first on 2026-09-17 18:55 UTC. 28 of them in the last 48 hours.
* **Chose a side:** 36. **Makers who submitted:** 6. **Posters who posted:** 9.
* **Compared with the brief's figure** ("1,551 emailed, 19 arrived, 15 chose a side, 3 submitting"): that figure is **second hand and NOT re-derived here**. Its source is not in this repo, `email_events` or `BACKLOG.md`; `email_events` shows only 93 sends since 2026-09-10. The "arrived" definitions probably differ. Say which one you mean before quoting either.

### Campaigns

36 campaigns: 34 NORMAL, 1 MARKETPLACE_ONLY, 1 BOTH.

| campaign | type | status | budget | clipperCpm / ownerCpm | requirements | card picture |
|---|---|---|---|---|---|---|
| **ANGIE BROWN THE REAL ME** (`cmu7c01hi001d...`) | MARKETPLACE_ONLY | ACTIVE | $2,700 | 0.2 / 0.0985 | yes, 859 chars | yes |
| **Marketplace test campaign** (`cmu5yeax2...`) | BOTH | ACTIVE | $500 | 1 / 0.5 | **none** | **none** |

The test campaign is hidden from non-test users by BL-904's filter (READ). It has 0 live clips.

Campaign data across all 36:
* **requirements:** 16 have them, **20 do not**, including the test campaign;
* **pictures:** 19 have `cardImageUrl`, 4 have `imageUrl`.

### Money through the marketplace

**No real money has left.** There are **0** `payout_requests` on either marketplace campaign. There are 0 payouts whose `clipIdsSnapshot` names a v2 post's clip, and 0 null-campaign payouts by any maker or poster since 2026-09-13. v2 cashout goes through `/api/payouts` (`CashoutModal.tsx:211`).

**Earned and unpaid, all on ANGIE BROWN:**

| leg | amount | notes |
|---|---|---|
| poster (`Clip.earnings` on APPROVED, not `videoUnavailable`) | **$2.21** | $2.31 without the `videoUnavailable` filter |
| maker | **$2.19** | 39 rows, 0 with a paid floor (`savedAmount`) |
| platform 10 percent | **$0.46** | 39 rows |
| owner's ordinary cut (agency rows on v2 clips) | **$2.42** | |
| **stored total** | **$7.28** | against the $2,700 budget |

BL-922 read $6.03 of spend on 2026-09-22. The $7.28 is this audit's own sum of the four stored legs, not `getCampaignBudgetStatus`.

Invariants were **not** re-run by this audit. BL-922's full-population run was the last: 0 violations, 0 of 21 budgeted campaigns over budget (READ).

### Alarms and machinery

* **L5:** 92 violations every tick (see BL-921).
* **`TRACKING_RECALC_FAIL`:** 9 rows ever. 3 are BL-917's faces (2026-09-20). **6 are the new `TransactionWriteConflict` face** (2026-09-21 17:00 to 2026-09-22 20:00; see section 0, item 3).
* **`TRACKING_TICK_STEPS`:** 222 rows. **`CRON_JOB_RUN`:** 4 rows ever.
* **Frames:** all 20 approved clips have them.
* **Thumbnail sweep:** still skipped on the cron service (no storage variables).
* **Email:** 0 refused ever. 189 of 210 owner alerts are payout-overdue reminders.
* **`campaign_rules_seen` exists in production with 0 rows.** It was created by BL-923; see section 11.

---

## 10. EVERY OPEN ITEM AND OWNER DECISION NAMED BY BL-916 TO BL-923, IN ONE LIST

**Owner decisions (nobody may take these for him):**
1. **BL-921, the 92 frozen legacy agency rows.** Options: leave them, credit +$139.96, also reduce -$20.34, or run `--fix`. Alternatively, a PAST-campaign filter on the monitor to stop the repeat.
2. **BL-916 item 3:** should approval skip the owner-cut write for v2 clips until the legs exist?
3. **BL-922 item 1:** should the owner's default clips view exclude archived (1,088 rows)?
4. **BL-922 item 2:** clippers' pages hide archived campaigns only; the poster v2 dashboard hides nothing.
5. **BL-919:** keep or remove "Made by @username" on the poster's absent-state card.
6. **BL-918 / BL-920 Railway variables:**
   * storage pair on the cron service;
   * `RAILWAY_NATIVE_CRON` words for the frames cron and the seven writing jobs;
   * `PAYOUT_REMINDERS_ENABLED`, or ask for a digest round (189 reminder emails in 37 hours).
7. **Resend domain verification.** Probably moot: 0 refused rows (VERIFIED).
8. **Marketplace supply.** One real marketplace campaign exists. No maker has submitted since 2026-09-20.

**Engineering items still open:**
1. **NEW:** the `TransactionWriteConflict` face is not matched by `isTransactionConflict` (`clip-earnings-writer.ts:161-166`). Money file, Opus only. 6 rows so far.
2. BL-916 item 1: the committed-spend reads omit v2 aggregates (`tracking.ts:2559`, `review/route.ts:637`).
3. BL-917 item 1: the `fix-budget` and payout `adjust` scalers on v2 clips.
4. BL-917 item 3: the Zhus Edit (MANUAL paused) money writes. It is now tied to item 1 above.
5. BL-917 nit: the `attempts` field records the maximum, not the count reached.
6. BL-920 items 1 and 5: route-only jobs, and opt-in jobs.
7. BL-922 items 1, 3, 4 and 5 (Track modal counts, `MultiDropdown` a11y, DRAFT, the `includePast` naming).
8. BL-912 (READ, before this range): the EDITOR dashboard reads views from the snapshot column `MarketplaceV2EditorEarning.views`, not the live ClipStat.
9. BL-914 (READ): three share items (submit-row zeros, stale `apidojo.ts:681` comment, `apify.ts:651`).
10. Pre-existing a11y: owner row contrast and links (BL-916 item 5); `--mp-*` dark-only (BL-919, BL-920).

---

## 11. BL-923 HANDOVER: EXACTLY WHERE IT WAS CUT, AND WHERE IT STANDS NOW

### What it was asked (READ, brief 2026-09-22 18:20:18 UTC)

**Title:** BUILD — BL-923 RUN ALONE, "the marketplace is correct and nobody can use it. Make it obvious. Phone first."

Ships to EVERYONE, not behind `isTestUser`. Publish to `reports/BL-923-clippershq-marketplace-simplicity.md`. The parts:

| part | ask |
|---|---|
| **PART 1** | investigate only |
| **PART 2** | phone-first clip card: picture, title, platform icon, ONE money line per 100,000 views, two real buttons "Post" and "Skip" that do not repeat the title, explanatory sentences deleted, no gross or maker's leg |
| **PART 3** | shorter action cards; delete "Every campaign the owner has opened appears here..." and "You are not on this campaign yet, and you do not need to be."; each campaign card gets its own picture, an icon, one large per-100k figure, one primary button, and quiet counts stating their population |
| **PART 4** | the campaign's rules in front of a clipper the first time he enters a campaign inside the marketplace. Gate POSTING only, never membership or browsing. The per-campaign side lock is untouched. A permanent quiet rules link afterwards. Campaigns with no requirements block nobody |
| **PART 5** | clip-detail walkthrough (Drive, account, post, paste the link HERE); the real time limit; the duplicate rule; a better account picker; submit path unchanged |
| **PART 6** | closed mobile drawer to 0 focusable links (BL-910 measured 34); badge treatment on the pill sections |
| **PART 7** | full proof, renders at 5 widths in every state, merge |

### PART 1, completed before the cut (READ from the transcript; DB figures re-VERIFIED today where marked)

1. **Surfaces.** 21 `.tsx` under `src/app/(app)/marketplace-v2`, 10 components in `src/components/marketplace-v2`, 17 v2 API routes. The second family is the v1 marketplace: 31 `.tsx` under `src/app/(app)/marketplace`. The `/market` rewrite is at `next.config.ts:212-213`.
2. **Campaign picture (VERIFIED).** Of 36 campaigns, 19 have `cardImageUrl` and 4 have `imageUrl`. ANGIE BROWN has a card image; the test campaign has none. Cards show no picture rather than a fabricated one.
3. **No "has read the rules" record existed.** The ordinary page's requirements checkbox (`campaigns/[id]/page.tsx:763`, `useState(false)` at line 139) writes nothing, and `campaign_accounts` has only `joinedAt`. **Consequence: a schema change.**
4. **Requirements (VERIFIED).** 16 campaigns have `requirements`, **20 do not**. The test campaign has none; ANGIE BROWN has 859 chars.
5. **Rate source.** `posterRatePer1k` in `src/lib/marketplace-v2-poster.ts` = `round2((clipperCpm ?? cpmRate) x MARKETPLACE_V2_POSTER_SHARE)`, where the share is 0.45 (`marketplace-v2-earnings.ts:62`). On screen at `CatalogueCard.tsx:180`, `detail-client.tsx:322` and `campaigns-client.tsx:151`.
6. **The 30-minute window measures from when the post goes LIVE on the platform** (the provider's publish timestamp), not from opening Drive (`clip-freshness.ts:151,179`). It fails open on provider trouble.
7. **Brief corrected.** It said eight pill sections lacked the badge treatment; it is **seven**, because BL-920 shipped the eighth.
8. **Longest names.** The longest campaign names are 28 characters (two `rv-fix-3-...` fixtures), then "BAD BITCH ANTHEM (2.50 CPM)" at 27. The longest v2 clip title is 118 characters (REJECTED); among APPROVED it is 35.

### Written into `C:\w\b923` before the cut (READ), branch `checkpoint/BL-923` from `78d12570`

* **Schema change, APPLIED TO PRODUCTION, not reversible by git.** `scripts/migrations/BL-923-campaign-rules-seen.sql`, run through `run-schema-sql.js`, creates `campaign_rules_seen`:
  * columns: `id`, `userId`, `campaignId`, `seenAt`, `source` (default `'unknown'`);
  * FKs cascade to users and campaigns;
  * unique on (`userId`, `campaignId`), plus an index on `campaignId`;
  * **rollback, by hand:** `DROP TABLE IF EXISTS campaign_rules_seen;`.
  * **VERIFIED today:** the table exists with 0 rows. Production code does not know it yet. A Prisma model was added in the worktree's `schema.prisma`.
* **Money display.** `posterRateUnrounded` feeding `posterRatePer100k`, so a 0.19 CPM campaign reads $8.55, not the $9.00 that 100 x the rounded $0.09 would give. `yourRatePer100k` was added to the payloads.
* **`src/lib/campaign-rules-seen.ts`:** `hasSeenCampaignRules`, `seenCampaignIds`, `recordCampaignRulesSeen`, `campaignRuleLines`, `campaignHasRules`, `RULES_NOT_SEEN_CODE`, `RULES_NOT_SEEN_MESSAGE`.
* **`src/app/api/campaign-rules/[campaignId]/seen/route.ts`:** POST, called from both doors.
* **A server-side posting precondition** in `src/app/api/marketplace-v2/catalogue/[id]/post/route.ts`: 409 `CAMPAIGN_RULES_NOT_SEEN`. Browsing is untouched; campaigns without rules gate nobody.
* The ordinary campaign page writes the record when the box is ticked.
* **PART 6:** both closed mobile drawers made `inert`; all eight pill sections moved onto `CountPill`.
* **Copy constants** in `marketplace-v2-copy.ts`: `V2_EARN_LABEL`, `V2_PER_100K_SUFFIX`, `V2_POST_BUTTON`, `V2_SKIP_BUTTON`, `V2_UNSKIP_BUTTON`.
* **PART 2 done:** `CatalogueCard.tsx` rebuilt.
* **`CampaignRulesPanel.tsx`:** written, not yet wired.
* **Its own disclosed mistake.** It overwrote `src/lib/campaign-rules.ts`, which is BL-602's shadow-rules evaluator. `tsc` caught it and it was restored from git. The resume session confirmed blob `006c4d1a` equals `main`. It must go in the report.

**The cut.** At 2026-09-22 18:54:36 UTC ("You've hit your weekly limit · resets Sep 26, 8pm Europe/Budapest"), just after starting PART 3.

### What its accessibility review said (READ, accessibility-lead, delivered 18:50 UTC; 87 items)

**Its five BLOCKERS:**
1. **Item 31:** the absent-picture state must stay non-interactive (not inside the card link).
2. **Item 69:** delete `RIBBON_WORDS` and every one of its 5 `statusId` `aria-describedby` references atomically.
3. **Item 77:** `mp-stagger-in` ignores reduced motion. Add the class, not `motion-reduce`.
4. **Item 78:** the Skip button's boundary must use `--border-strong` (3.48:1), not `--border-color` (1.18:1).
5. **Items 37 and 38:** gate the SUBMIT on the detail page, not the grid's Post link (an `aria-disabled` link still navigates). No native `disabled`: use `aria-disabled` plus a synchronous ref guard.

**Key HARD rules:**
* Post and Skip take unique names via `aria-labelledby` = own id + the title LINK's id, never the heading's.
* The money line is one `<p>` reading "about $9.00 per 100,000 views". No `~`, no `100K`, no truncation. `--mp-success` or bold `text-accent` at 18.667px or more.
* Keep platform WORDS (sr-only sentence built from data); the icons stay `aria-hidden`.
* One stretched anchor per card.
* The rules panel is an inline `<section>`, NOT a dialog. It is expanded on first run and collapsed behind a named button afterwards. The panel must not own its own live region.
* Steps are a real `<ol>` with `list-decimal`, outside the `<form>`.
* Account option text is "TikTok: @handle", platform first. This is a money bug if not: the same handle on two platforms would give identical names.
* A 16px font floor at every width.
* Restate the 30-minute and duplicate rules inside the form.
* Validate in DOM order.
* Use `--mp-surface-0` for text on the accent fill (5.89:1 in both themes).
* Quiet counts in `--text-quiet`, never `--text-muted` (which is white in dark mode).

**Five decisions it asked for:**
1. Is the gate "opened" or "confirmed"? `V2_RULES_CONFIRM = "I have read these rules"` ships unused.
2. Which surface owns the gate? Recommended: the detail page.
3. Does "Post" write `inProgress`? If so it cannot be a prefetching `<Link>`.
4. Campaign picture alt text.
5. Whether to keep the page-level 45 percent sentence.

**The latent light-theme failures are not live:** `toggleTheme` is wired to no control (`navbar.tsx:56`).

### What has happened since, in the LIVE resume session `339eae0a` (READ, as of 08:08:49 UTC today)

1. **08:01:46:** the resume brief arrived (it said: carry on from PART 3).
2. Confirmed the `campaign-rules.ts` restoration.
3. Trimmed the per-card rules from the list payloads, keeping them on clip detail only.
4. Took the opening DB snapshot: 0 rules rows, 0 `bl923sbx-` rows, 1,788 users, 36 campaigns, 10,334 clips (08:04:49 UTC).
5. Launched a **second** accessibility review, for PARTS 3 to 5. **It returned 6 blockers.** Their text was not read by this audit.
6. Began applying those blockers.
7. Wired PART 4 (the campaign page passes rules and the seen state from the server).
8. Started PART 5 in `detail-client.tsx`: types, the refusal branch for the 409, then the render body (money line, rules panel, ordered walkthrough).

**Worktree at 08:08:56 UTC (VERIFIED):** 13 modified files plus 4 untracked, **750 insertions and 289 deletions**, nothing committed (HEAD `78d12570`).
* Modified: `prisma/schema.prisma`, `campaigns/[id]/page.tsx`, `marketplace-v2/campaigns/[id]/page.tsx`, `campaigns-client.tsx`, `detail-client.tsx`, `catalogue-client.tsx`, `catalogue/[id]/post/route.ts`, `app-layout.tsx`, `sidebar.tsx`, `CatalogueCard.tsx`, `V2Nav.tsx`, `marketplace-v2-copy.ts`, `marketplace-v2-poster.ts`.
* Untracked: the migration, `src/app/api/campaign-rules/`, `CampaignRulesPanel.tsx`, `campaign-rules-seen.ts`.
* Scratch logs sit in `C:\bl923-sandbox` (`tsc1` to `tsc6`, `npmci`, `prisma` logs, `my-rules-seen.ts`).

### What remains, for whoever resumes or re-briefs

1. **First,** establish whether session `339eae0a` finished, is still running, or was cut again. Check: `git -C C:/w/b923 log --oneline -3`, `git ls-remote origin checkpoint/BL-923`, and whether `reports/BL-923-clippershq-marketplace-simplicity.md` exists in the reports repo.
2. If it stopped, the remaining work as of 08:08 UTC:
   * finish PART 5 (walkthrough, account picker, duplicate rule, time-limit wording "from when your post goes live");
   * finish PART 3 and PART 4 wiring checks against both reviews' blockers;
   * all of PART 7:
     * sandbox with prefix `bl923sbx-` and an opening snapshot;
     * renders at 320, 375, 414, 1280 and 1440 in every listed state;
     * the per-100k exactness proof on 5 real campaigns;
     * the no-subtraction proof;
     * the rules-gate proof (browse yes, post no, then yes, never asked twice across both doors);
     * money files by blob OID and full-population invariants;
     * both reconciliation forms and every guard;
     * the merge and a verified push;
     * the report, including before-and-after copy and the word count before and after.
3. **Standing facts the resumer must carry:**
   * the migration is already applied: do not apply it twice;
   * `campaign_rules_seen` is the only real table this round writes;
   * `main` is unchanged at `78d12570`;
   * the hooks gate was last measured at 10 of 11, not 11;
   * `--bg-page` has 0 live uses;
   * the test campaign has no requirements and no picture;
   * 20 of 36 campaigns have no requirements, and they must block nobody.
4. **If the round is abandoned instead:** the worktree can be discarded, but the production table stays until someone runs its rollback SQL. It is empty and unreferenced by deployed code, so it is harmless while it stays.
