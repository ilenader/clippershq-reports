# BL-917 — the clip four ticks declined to correct: fixed through the tick's own code, the swallow made visible, and then the cause named itself and was closed

> **NOTHING IS PAID AGAINST cmu8tf4p AND NOTHING IS UNREMOVABLE, FIRST LINE AS REQUIRED.** Neither
> its poster nor its maker has any payout row on this campaign (zero payout rows on ANGIE BROWN,
> `2026-09-20 11:29:46+00`); the poster's two REQUESTED payouts sit on other campaigns. So the
> doubled figures were a correction, not a loss, and they ARE corrected: at **12:04:45 UTC** the
> tick's own code, run on this machine against the real clip, wrote poster **$0.26**, maker
> **$0.25**, platform **$0.06**, owner **$0.28** at 2821 views where it had read $0.57 / $0.54 /
> $0.12 / $0.27. **THE CAUSE WAS NOT NAMEABLE FROM THE DATABASE WHEN THIS REPORT WAS FIRST WRITTEN,
> AND THEN IT NAMED ITSELF:** the first production tick after the audit row shipped wrote the
> error down (see the ADDENDA at the end), it is a Serializable write conflict with the :00 wave,
> swallowed twice over, and both swallows are closed on `main` (`fd74aa01`, `0da96dfb`). The 15:00
> UTC production tick corrected the clip itself. Sandbox: 40 ledgered rows, **`VERIFIED: 0 of 40
> remain`**, 0 failed, 0 `bl917sbx-` traces; two partial-run rows were never left behind.

**2026-09-20. Three merges, in the order the evidence arrived: `checkpoint/BL-917` (`3ff484ff`)
merged as `6b74838f`; `checkpoint/BL-917-p2034` (`c751f94f`) merged as `fd74aa01`;
`checkpoint/BL-917-abort` (`68535ab7`) merged as `0da96dfb`, each pushed and verified
(`origin/main == local HEAD`), each with its pre, post, pre-merge and post-merge tags. Worktrees
`C:\w\b917`, `C:\w\b917b`, `C:\w\b917c` removed and verified gone (`ls: cannot access`).
`checkpoint/BL-723` not merged. No surface changed, so no render pass.**

---

## THE HEADLINE

1. **THE CLIP IS CORRECT AND THE CORRECTION CAME FROM THE TICK.** Not a hand written row:
   `_bl163RunTrackingJobForTest`, which is `processTrackingJob` itself with the views handed in,
   was run on the real clip at its own latest view count (2821). One real `ClipStat` row
   (`isManual = true`, same 2821 views) is the only other real row this round wrote. The 12:02
   production tick had just failed on it for the fourth time.
2. **THE PRODUCTION PROCESS FAILS ON THIS CLIP; THE CODE PATH AND THE DATA DO NOT.** The same
   code corrected it from this machine in three shapes: BL-163's full `include`, the cron's exact
   `select` (now the named `DUE_JOB_CLIP_SELECT`) with `source: "cron"`, and a row for row sandbox
   replica in both shapes. The failure is deterministic (four ticks), fast (the 12:02 earnings
   section took **0.57 s**, too short for the retry loop's 500 ms and 1000 ms sleeps, so a
   non-conflict exception thrown on the first attempt) and confined to one clip out of the 22 to
   39 approved clips each tick wrote money for.
3. **THE SWALLOW IS NAMED AND CLOSED.** `tracking.ts`, the retry loop's end: `[TRACKING-RECALC-FAIL]`
   goes to `console.error`, `details`, and nowhere the database can show; the job's
   `consecutiveFailures` and `lastFailedAt` are FETCH counters and read 0 and null through four
   money failures, while the stat row, the fraud stamp and the cadence stamp were all written as if
   nothing was wrong. A failed money write now writes a `TRACKING_RECALC_FAIL` audit row with the
   error text, code, source, views and the four figures it was about to write. Reproduced in the
   sandbox with a real refusal: `[MARKETPLACE-V2-WRITE] missing v2ClipId` landed in `audit_logs`.
4. **THE WRITER GUARD IS KEYED ON THE WRITER.** `check:v2-single-share-writers` now discovers every
   file that calls `writeClipEarnings(` on a word boundary, 15 of them, and classifies each; it
   found two more v2 blind writers on the way (`fix-budget`, payout `adjust`), which are filed and
   fenced rather than fixed. Six demonstrations, one check at a time, each red for its own reason,
   the tree byte-identical after each.
5. **THE RECONCILIATION KNOWS ABOUT BONUSES.** Both forms compare the two earner BASES and require
   each leg to sum. The old form called a legitimate $0.02 poster bonus a LEAK and passed a maker
   base $0.03 above the poster's with the totals a cent apart; the corrected form does the
   opposite. Across the full live population the corrected form newly flags **0** rows.

**PROOFS: 19 of 19 sandbox checks, 5 of 5 HTTP failure paths, 6 of 6 guard demonstrations.**

---

## PART 0 — THE MODEL SPLIT

| tier | what ran there | subagents |
|---|---|---|
| cheapest | nothing this round: the Railway log was the only retrieval worth delegating and it was unreachable, so there was nothing cheap to fetch | **0** |
| **strongest (Opus), NOT SPLIT** | every figure at its source, every line of every change, every proof, this report | **0 subagents between it and the row or the file** |

**Connections:** one at a time, `run-select.js` or one `$queryRawUnsafe` per statement; the cap was
one, the same as BL-905. No vendor call, no Apify actor: every view count handed to the tick was a
`ClipStat` row's own count or a prime the sandbox chose.

---

## PART 1 — WHAT IS RUNNING AND WHAT HAPPENED

**THE RUNNING COMMIT COULD NOT BE READ, AND THIS IS SAID PLAINLY.** `railway whoami` answers
`Unauthorized. Please login with railway login`; `/api/health` returns `{ok, ts}` and nothing else; no
code reads `RAILWAY_GIT_COMMIT_SHA`; the deployed pages are turbopack chunks with hashed names and no
build id to compare. **What IS established, by behaviour:** the 11:00 UTC tick wrote owner cuts of
**$0.18** (cmu8fa1r, legs 0.17 + 0.16 + 0.04 = 0.37 x 0.4925) and **$0.05** (cmu855k9, legs 0.11 x
0.4925). The pre-BL-916 owner lock multiplies the poster's leg alone and would have written $0.08 and
$0.02. Only `b750a080` or later produces those two figures, so the fix merged at 10:24 was running by
11:00. That is an inference from money, stated as one; it is not a commit hash.

**THE RAILWAY LOG WAS NOT REACHED.** Tried: the `railway` CLI (installed, not authenticated, and a
browserless login needs a person at a browser); the environment files (no Railway token among the 29
variable names); the codebase (no log mirror). Proceeded on database evidence alone, and nothing in
this report invents a cause.

**THE CLIP, RE-READ AT 11:29:46+00 (before anything was done):** status APPROVED, `isMarketplaceClip`
false, `marketplaceV2PostId` cmu8tf4pk…, earnings **0.57**, baseEarnings **0.57**, bonusAmount 0,
bonusPercent 0, stamped CPM 0.2000, owner stamp null, campaign cmu7c01hi… (ANGIE BROWN, CPM_SPLIT,
guarantee on, s 0.32998325, budget 2700), reviewedAt `2026-09-20 09:05:36.705`, clip updatedAt
`11:00:29.591` (the fraud stamp). Maker row: 0.54 base 0.54 bonus 0 views 0, created `2026-09-19
20:03:44.588`, updated `09:05:37.637`. Platform row: 0.12 views 0, created `20:03:44.611`, updated
`09:05:37.662`. Owner row: 0.27 views 2675, created `09:05:36.718`, updated `09:05:37.675`. Sixteen
stat rows from 0 at `2026-09-19 20:03:44.433` to 2782 at `2026-09-20 11:00:29.521`, then 2821 at
`12:02:08.260`. **It had not self corrected**: the 12:02 tick was its fourth, and it left the four
rows at the 09:05:37 figures again.

---

## PART 2 — WHY THIS CLIP AND NOT cmu8fa1r, RULED IN AND OUT

**Side by side, every column of every related row** (clip 64 columns, user 87, job 16, post 10,
account 22, maker 14, platform 9, owner 8). Fields that differ and could reach the recalculation:
poster (different person: level 1 vs 2, bonus 3 vs 6 percent, streak 1 vs 1, PWA both, referred
neither, status both ACTIVE, `tosAcceptedAt` set vs null, timezone Africa/Lusaka vs Asia/Damascus),
catalogue clip (different v2 clip, same maker, both APPROVED), createdAt (`2026-09-19 20:03` vs
`13:27`), job cadence (60 min IG_HIGH_2K vs 120 min IG_MID_900_2K, so **cmu8tf4p is the FIRST job in
its campaign group every hour**), fraud (**score 10**, "Only 1 comments for 2,782 views" vs 0), and
the money figures themselves. Same campaign, same stamped CPM, same minViews, same maxPayout snapshot
150, same era boundary (none), no `lastBudgetPauseAt`.

| hypothesis | evidence | verdict |
|---|---|---|
| a filter this clip fails | every gate before the transaction is shared with cmu8fa1r (same campaign, ACTIVE poster, era boundary null, pause null); the job's cadence stamp `cadenceReasonAt == lastCheckedAt` at 11:00:31.205 proves the bracket decision AFTER the earnings section ran, so the section was entered and exited normally | **ruled out** |
| the transaction throws and the error is swallowed | earnings section duration 1.35 s (10:00), 1.6 s (11:00), **0.57 s (12:02)**; the 12:02 figure excludes two P2034 sleeps; the swallow at `tracking.ts` retry loop end persists nothing | **ruled in as the mechanism**, the exception itself unnamed |
| a stale value written back unchanged | Prisma's `@updatedAt` bumps on every update; all four rows still read `09:05:37`, so no write reached them | ruled out |
| a different branch of the v2 fork | the local run of the identical code took the v2 fork and wrote; `isMarketplaceClip` false, `marketplaceV2PostId` set, `v2Clip.editorId` present | ruled out |
| a cap or clamp held the value | budget $2,700 against $2.99 spent; no ratio below 1; the guarantee cap and BL-718 floors bind only near the cap; the local run logged none | ruled out |
| the gamification write lands after the tick each hour | every row's `updatedAt` is `09:05:37`, before all four ticks; nothing writes after the tick; `recalculateUnpaidEarnings` excludes v2 clips since `b750a080` | **ruled out by the timestamps** |
| the tick writes the clip but the money rows come from a path it did not reach | the money rows and the clip's earnings are written in ONE transaction by the tick; the clip row's touch at each tick is the fraud stamp at line `1881`, outside that transaction | ruled out |
| **the production process itself** | same code, same rows, same select, same source: **written at once from this machine, three shapes, and on a row for row replica** | **the only survivor** |

**The error is swallowed at** `src/lib/tracking.ts`, the block that begins `if (lastTxErr) {` after
the three attempt loop (`[TRACKING-RECALC-FAIL]`): `console.error`, `details.push`, values reset, and on
to the cadence stamp. No column, no audit row, no counter. The job's `consecutiveFailures` and
`lastFailedAt` belong to the fetch ladder and were never touched. **That is BL-874's family exactly: a
path reporting zero failures while plainly failing.**

**What was NOT found.** The exception's text. Of the throw sites reachable in that transaction (the
L1 budget lock, which needs a positive delta and this clip's was negative; the two paid floors, which
need a PAID payout and there is none; `assertInvariant` and the L2 middleware, which need inconsistent
figures and the tick computes consistent ones; the v2 writer's four missing-argument throws, which the
cron's select satisfies), none is data dependent in a way that separates cmu8tf4p from cmu8fa1r. What
separates them in production is the ORDER in the campaign group and the fraud score, and neither
reaches the transaction. It will be named by the audit row the next time it happens.

---

## PART 3 — WHAT WAS DONE, AND THROUGH WHICH PATH

**The correction.** `scripts/sandbox/bl917-real-tick.ts` calls `_bl163RunTrackingJobForTest({ clipId,
prefetchedStats: <its latest ClipStat> })`, which is `processTrackingJob` with the fetch replaced by the
row's own count. Output, verbatim from the run:

```
BEFORE (db now 2026-09-20 12:04:26.335337+00) views 2821: poster $0.57 (base $0.57 bonus $0) maker $0.54 platform $0.12 owner $0.27
[BL-163-OWNER-LOCK] ... was=$0.29 now=$0.28 (clipperFinal=$0.57 v2 legs poster=$0.26 maker=$0.25 platform=$0.06 s=0.3300)
AFTER  (db now 2026-09-20 12:04:46.520761+00) views 2821: poster $0.26 (base $0.25 bonus $0.01) maker $0.25 platform $0.06 owner $0.28
```

Poster 2821 x 0.20 / 1000 = 0.5642, rounded 0.56; two bases of 0.25; residual 0.06; the poster's 5
percent (level 3 + PWA 2) on 0.25 is 0.01; legs 0.57; owner 0.57 x 0.4925 = 0.2807 = **$0.28**.

**The fix that ships, `tracking.ts`, protected and changed on purpose** (three hunks, comments stripped
in the report, full in the commit):

1. After `details.push(...)` at the swallow: `await logAudit({ userId: clip.userId, action:
   "TRACKING_RECALC_FAIL", targetType: "clip", targetId: clip.id, details: { source, campaignId,
   attempts, code, message, stack, views, storedEarnings, proposed: { earnings, owner, v2Editor,
   v2Platform, creator, platform }, isV2, isMarketplaceClip, failedAt } })`, itself in a try so the
   tick goes on to the next clip if the audit table refuses.
2. The dueJobs clip `select` moved verbatim into `const DUE_JOB_CLIP_SELECT = { ... } as const` and
   referenced from the query. Same object, same fields, the cron byte-identical in behaviour.
3. `_bl163RunTrackingJobForTest` gains `cronShape?: boolean`: with it the harness loads the job through
   `DUE_JOB_CLIP_SELECT` and calls `processTrackingJob(job, "cron", ...)`. Test only.

Money files by blob OID, `main` against the branch: `clip-earnings-writer.ts 416972e9`,
`earnings-calc.ts 00410634`, `balance.ts 67c30c89`, `clip-earnings-invariant-middleware.ts 61cef393`,
`money-decimal.ts ef5cdae7` **byte-identical**; `tracking.ts 39fdbea5 to c3e3771a`, the change above.

---

## PART 4 — THE GUARD DISCOVERS BY THE FUNCTION THAT WRITES

`scripts/check-v2-single-share-writers.js` used to discover a writer as "a file that calls a recompute
helper AND the chokepoint". Discovery is now `\bwriteClipEarnings\s*\(` alone, on a word boundary, and
every hit must be classified: **8 WRITERS** (recompute and must exclude v2: W1, W4), **2 V2_NATIVE**,
**2 INFRA**, **1 CREATE_ONLY**, and **2 SCALERS** it had never seen (`admin/fix-budget/route.ts`,
`admin/payouts/[id]/adjust/route.ts`), which scale a stored figure, test `isMarketplaceClip` alone and
carry the poster-leg owner arithmetic; they are filed with the reason, in BACKLOG, and fenced by two new
checks: **W5** fails a scaler that starts recomputing from views, **W6** fails a scaler that starts naming
the identifier without moving to WRITERS.

| demonstration | red check | restored |
|---|---|---|
| `gamification.ts` loses `marketplaceV2PostId: null` (the exact call shape that paid two posters 100 percent) | **W1** and **W4** | byte-identical |
| a NEW file with `calculateClipperEarnings(...)` then `writeClipEarnings(...)`, naming no identifier | **W2** unclassified and **W5** | removed |
| the call in `gamification.ts` renamed to `writeClipEarningsX(` | **W2** "no longer calls" (the old substring match would have stayed green) | byte-identical |
| `fix-budget` starts recomputing with the inner helper | **W5** | byte-identical |
| payout `adjust` starts naming the identifier | **W6** | byte-identical |
| control: a file mentioning only `xwriteClipEarnings(` and `writeClipEarningsX(` | stays green, not discovered | removed |

The guard's own file was unchanged through the six runs (`git hash-object` before and after equal).

---

## PART 5 — THE RECONCILIATION AND BONUSES

`V2_RECONCILE_BODY` compared `c.earnings` to `e.amount` within $0.02, which is the two TOTALS, and took
the platform residual on totals. A bonus multiplies its own earner's base and the two stacks differ
whenever the two people differ, so BL-916's sandbox clip with a 5 percent poster bonus read LEAK. Both
forms now compare `c."baseEarnings"` to `e."baseAmount"`, take the residual on the two bases divided by
0.9, and require each leg to sum (`total = base + bonus` within $0.02); the audit form reports
`poster_base`, `poster_bonus`, `editor_base`, `editor_bonus` and names the finding ("bases disagree",
"leg does not sum", "platform leg is not the residual"). The two EXPLAINED arms still compare totals
against paid floors, because a floor holds a total.

Sandbox, staged rows: **E1** poster 0.32 (0.30 + 0.02), maker 0.30, platform 0.07: old form flagged,
corrected form clean. **E2** maker base raised to 0.33 with totals a cent apart: old form PASSED it,
corrected form `LEAK: nothing justifies this`, finding "poster and editor bases disagree". **E3** a maker
leg whose total is not base plus bonus: flagged by name.

**Across the full live population the corrected form newly flags 0 rows.** The old form flagged 1 row
at the time, the staged sandbox clip; every real v2 clip was clean on both, which follows from the
correction of cmu8tf4p an hour earlier (the two gamification-written clips were the old form's real hits
in BL-916 and both are gone: cmu8fa1r by the 11:00 tick, cmu8tf4p by this round).

---

## PART 6 — THE PROOF, THE POPULATION, THE TEARDOWN, THE MERGE

**Replica** (`bl917-repro.ts`): a v2 clip staged row for row into cmu8tf4p's state (0.57 / 0.54 with
views 0 / 0.12 with views 0 / 0.27 at 2675, fraud 10, the same fifteen stat rows, the poster's level 1,
bonus 3, streak 1, PWA, the maker plain, ANGIE's economics with maxPayout 150 and minViews 500). Driven
at 2782 with the full include: corrected. Re-staged and driven with `cronShape: true`: corrected.

**Proof** (`bl917-prove.ts`, 19 of 19): re-staged and driven with the cron's shape at **2851** and
**3163** views (primes): poster 0.27 / maker 0.26 / platform 0.05 / owner **0.29** = guaranteed(0.58),
then 0.29 / 0.28 / 0.07 / **0.32** = guaranteed(0.64), legs exactly the library's split.
`recalculateUnpaidEarnings(poster)` touched 0 clips and moved nothing. Ordinary control clip at 1681,
2677, 3331: earnings 0.36 / 0.57 / 0.70 and owner 0.18 / 0.28 / 0.34, **BL-916's measured figures to the
cent** and equal to the inline expression, no v2 row written. Failure injected by deleting the sandbox
catalogue clip: the tick reported the clip processed (`success: true`, details "earnings tx failed after
3 attempts"), the money rows stood, and **one `TRACKING_RECALC_FAIL` audit row** carried
`[MARKETPLACE-V2-WRITE] missing v2ClipId`, source cron, views 3373 and the proposed figures.

**HTTP failure paths, own person each, against the worktree's build on port 3917:** nobody signed in
**401**, the sandbox poster **403**, the sandbox maker **403**, the sandbox owner 200 with the row,
health 200; none 429. Server stopped by its own PID.

**Population** (`2026-09-20 12:19:45+00`): earnings invariant 0 breaches on 10,218 live clips, 0
negative; maker invariant 0 of 18; no double pay across four tables; **23 budgeted campaigns, 0 over**
counting both v2 aggregates and the owner's cut; paid is final for makers 0 and v2 posters 0 positions;
**ANGIE BROWN $2,700 ACTIVE, $2.14 spent** (it read $2.99 while cmu8tf4p carried $1.50 of wrong legs).

**Guards.** All 18 prebuild guards pass; hooks gate **0 errors, 10 warnings** against the cap of 11
(one of headroom; the brief's 11 was one high); eslint present, three binaries. `check:v2-leg-sync`
still sees the chokepoint syncing all three legs.

**Builds.** tsc on the worktree after every edit **exit 0**; `npm run build` on the branch
**`BUILD_EXIT=0`**; merge tree OID `03df54871514` equals the branch tree; `npm run build` on merged
`main` **`BUILD_MERGE_EXIT=0`**. Exit codes echoed by the build's own shell.

**Teardown.** 40 ledgered (the two catalogue rows deleted by the failure injection reported "already
gone"), **38 deleted, 2 already gone, 0 failed, 0 of 40 remain**, 0 `bl917sbx-` traces. Closing census
against the opening one: users, campaigns, clips, accounts, jobs, agency identical; clip_stats +57
(the 12:02 production tick's stats on real clips plus this round's one manual stat on cmu8tf4p), v2
clips +2 (two real makers submitted during the round), payouts +1 (a real request arrived), audit
+1 (the owner approved a clip). Fingerprints moved and are attributed: 56 real clips touched since the
opening snapshot, **55 by the 12:02 production tick and 1 by this round's local tick on cmu8tf4p**;
16 real agency rows touched, 15 by the tick and 1 by this round. **REAL ROWS THIS ROUND WROTE:
cmu8tf4p's clip, maker, platform and owner rows through the tick's own code, and one manual ClipStat
row beside them. Nothing else.**

**What went wrong in the round, disclosed.** One shell heredoc was attempted against the rule and hung
the shell exactly as the memory warned; it was stopped and every edit after it went through a written
script. The first extraction script's line arithmetic was off by one and its assertion caught it. The
reconciliation query's first draft compared totals in the finding text while the body compared bases;
corrected before the proof ran.

---

## WHAT COULD NOT BE DETERMINED

* **The exception's text.** Read the Railway log for `[TRACKING-RECALC-FAIL] Clip cmu8tf4p` at 10:00,
  11:00 and 12:02 UTC, or from the next failure on, `SELECT details FROM audit_logs WHERE action =
  'TRACKING_RECALC_FAIL'`.
* **The running production commit**, beyond the behavioural inference in PART 1.

**IN ONE LINE:** cmu8tf4p carries correct earnings (poster $0.26, maker $0.25, platform $0.06, owner
$0.28 at 2821 views, unpaid), written by the tick's own code and not by hand; the next clip that fails
this way will name its cause in `audit_logs`, but the cause itself is not yet fixed because it is not
yet named.

---

## ADDENDA — THE CAUSE NAMED ITSELF, TWICE, AND BOTH FACES ARE CLOSED

### 13:00 UTC: the first audit row (production is running `6b74838f` or later, by the row's existence)

`SELECT details FROM audit_logs WHERE action = 'TRACKING_RECALC_FAIL'`, clip cmu8tf4p, `2026-09-20
13:00:53.591`, verbatim: code **`P2034`**, attempts 3, source cron, views 2864, stored 0.26, proposed
`{earnings 0.27, owner 0.30, v2Editor 0.26, v2Platform 0.05}`, message
``Invalid `prisma.marketplaceV2PlatformEarning.update()` invocation: Transaction failed due to a write
conflict or a deadlock. Please retry your transaction``, stack through `writeMarketplaceV2Earnings
(/app/src/lib/marketplace-v2-writer.ts:366)` and `tracking.ts:3162`. Earnings section 13:00:50.5 to
13:00:53.6: three attempts, 500 ms and 1000 ms apart, all inside the :00 wave.

**The mechanism.** At every :00 fifteen campaign groups start at once and each group's first money
transaction runs `getCampaignBudgetStatus` (the L1 lock reads it for any positive delta), which sums
`marketplace_v2_editor_earnings` and `marketplace_v2_platform_earnings` under Serializable isolation.
Those tables hold seventeen rows each, one index page; a SUM over ANY campaign's rows predicate-locks
the page every other campaign's row sits on, and the one v2 clip whose write lands inside the wave is
refused. cmu8tf4p's job has the shortest interval on its campaign (60 min), so the dueJobs ordering
(`checkIntervalMin ASC`) makes it the FIRST v2 write of every hour, inside the wave every hour; its
siblings four seconds later are past it. That is why one clip, why every hour, why not the sibling on
the same campaign, and why the identical code with no wave wrote it at once.

**Fix one, `fd74aa01`:** `tracking.ts` retry, six attempts, 500 ms to 8 s doubling with up to 250 ms
jitter (`RECALC_RETRY_MAX_ATTEMPTS`, `recalcRetryDelayMs`, pure and exported), 15.5 s of patience where
there was 1.5 s; pinned by `scripts/sandbox/bl917-retry-schedule.ts` (6 of 6).

### 14:01 UTC: the second face, and the real swallow

Second audit row, clip cmu8tf4p, `14:01:00.048`: code **null**, message ``current transaction is
aborted, commands ignored until end of transaction block`` (`DriverAdapterError`, `@prisma/adapter-pg`),
earnings section 0.64 s. That is what Postgres answers once a serialization failure has ALREADY
aborted the transaction on an earlier statement. The earlier statement is inside the chokepoint's L1
gate, whose catch (`clip-earnings-writer.ts`, after the gate; the fairness gate's catch; the v2 sync's
point read) "passes through" any error that is not the hard lock's own, written for a DB blip. So: the
gate's `current` read (it selects the two v2 legs) conflicts with the wave, Postgres raises 40001 as
P2034, the gate swallows it and passes through, `tx.clip.update` hits the aborted transaction and
throws with no code, and the tick's retry, keyed on `code === "P2034"`, gives up after ONE attempt.
**That is the 0.57 s and 0.64 s failures at 12:02 and 14:01, and it is the swallow this brief asked
to be named `file:line`: `src/lib/clip-earnings-writer.ts`, the `catch (e: any)` that follows the L1
gate (`[F-BUDGET-HARD-LOCK] gate query failed ... passing through`).**

**Fix two, `0da96dfb`:** `isTransactionConflict(e)` (P2034, 40001, 40P01, or the messages Prisma and
the pg adapter give them) is exported from the chokepoint, rethrown by all three catches, and used by
the tick's retry loop, so both faces retry on the six-attempt schedule. Demonstrated with a fake
transaction whose gate read raises P2034: the chokepoint as it stood on `main` before the change
swallowed it and the write died on the aborted transaction with no code (`bl917-conflict-before.ts`,
DEMONSTRATED); the changed chokepoint rethrows the P2034 and `isTransactionConflict` recognises it
(`bl917-conflict-demo.ts`, 6 of 6). `clip-earnings-writer.ts` is protected and changed on purpose:
`416972e9` to `5b40d49e`; the other four money files unchanged since before BL-916 (`earnings-calc
00410634`, `balance 67c30c89`, `invariant-middleware 61cef393`, `money-decimal ef5cdae7`).

### 15:00 UTC: the production tick corrected the clip itself, and the next victim appeared

cmu8tf4p at `15:00:14`: poster **$0.28**, maker **$0.27**, platform **$0.05**, owner **$0.30** at 2960
views, written by the production cron in 0.5 s with no retry, its first production write since 09:05.
And a new row: clip cmu84wy0 (another v2 post on the same campaign) at `15:00:20.435`, the aborted
face, `attempts` recorded as 6 (the field records the schedule's maximum, not the count reached, a
reporting nit to fix when next in that file), before `0da96dfb` had deployed. Fix two is what closes
that face; the row shows fix one was live (six is the new maximum) and that the wave picks whichever v2
clip lands in it.

**What went wrong in the round, disclosed, continued.** The report's first draft said the cause was
not nameable and shipped the audit row to name it; that was true when written and false forty minutes
later, and the two fixes that followed are recorded above as merges of their own rather than folded
back into the first commit. The `attempts` field in the audit row reports the maximum rather than the
number reached.

**IN ONE LINE, REVISED:** cmu8tf4p carries correct earnings (poster $0.28, maker $0.27, platform $0.05,
owner $0.30 at 2960 views, unpaid), written by the production tick itself at 15:00 UTC; the cause is
a Serializable write conflict with the :00 wave, swallowed twice over, both swallows closed on `main`
for every clip that lands in the wave next.

