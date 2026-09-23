**Nothing unremovable, and no real row touched.** All 20 ledgered bl924sbx- ids are gone, plus the 12 rows the tick wrote for them (3 audit, 1 owner, 4 stat, 4 job). A sweep of 341 id columns and 3 address columns finds 0. Every real table is identical in count and id fingerprint at the same cut-off.

# BL-924: the third face of the Serializable conflict, the one Postgres raises at COMMIT

Base `main` @ `01043557`. Branch `checkpoint/BL-924` has `e6c0f73a` (the fix and its proofs) and `067e313e` (BACKLOG). Merge `ee732774`. Tags `pre-BL-924`, `post-BL-924`, `pre-merge-BL-924` and `post-merge-BL-924`, all pushed and verified (`safe-push`: origin == local, twice). The merge tree `a635bdba` equals the branch tree, so build #2 on the branch IS the merge build. There were no conflicts to union. `checkpoint/BL-723` is not an ancestor. Worktree `C:\w\b924` removed and verified gone. **No .tsx changed, so there was no render and no accessibility pass.**

**Model split: Opus wrote every line and read every measurement. 0 subagents; no cheaper model ran anything.** Connection cap was ONE: every script ran one statement at a time and never in parallel. No vendor call, no Apify actor: every view count was handed to the tick, and every outbound key was deleted from the proof processes.

## PART 1: the six rows, and what the error actually is
Nine `TRACKING_RECALC_FAIL` rows exist. Three are BL-917's (2026-09-20: P2034 at 13:00:53, and the aborted face at 14:01:00 and 15:00:20). **Six are the new face.** Every field of each:

| createdAt (::text) | clip | campaign | message / name / code | attempts | views | stored | proposed earnings, owner | v2 | source |
|---|---|---|---|---|---|---|---|---|---|
| 2026-09-21 17:00:56.073 | cmua7m2h | Zhus Edit cmsisj3d | TransactionWriteConflict / DriverAdapterError / null | 6 | 1789 | 0.93 | 0.93, 0.59 | no | cron |
| 2026-09-21 17:00:58.439 | cmu7ba2v | Zhus Edit | same | 6 | 883 | 0 | 0, 0 | no | cron |
| 2026-09-21 17:01:01.075 | cmua3t5p | ANGIE BROWN cmu7c01h | same | 6 | 7 | 0 | 0, 0 | yes | cron |
| 2026-09-21 18:01:01.924 | cmu9441s | ANGIE BROWN | same | 6 | 4 | 0 | 0, 0 | yes | cron |
| 2026-09-22 18:01:22.39 | cmsrngha | Zhus Edit | same | 6 | 1340 | 0.72 | 0.72, **0.46** | no | cron |
| 2026-09-22 20:00:58.573 | cmtx4efs | Zhus Edit | same | 6 | 527 | 0 | 0, 0 | no | cron |

All six carry the same stack: `DriverAdapterError: TransactionWriteConflict` at `PgTransaction.onError (adapter-pg index.js:687)`, `performIO (:682)`, `PgTransaction.executeRaw (:641)`, `transaction-manager.ts:422`. That is the transaction manager's **COMMIT**, not a statement.

**What it is, read from the installed source (adapter-pg 7.5.0 and driver-adapter-utils 7.5.0, the same in the worktree and on main):** `onError` throws `new DriverAdapterError(convertDriverError(pgError))`. For SQLSTATE `40001`, `mapDriverError` returns `{ kind: "TransactionWriteConflict" }`, merged with `{ originalCode, originalMessage }`. `DriverAdapterError`'s message is `payload.kind` when the payload has no message, and `.cause` is the payload. So the production message "TransactionWriteConflict" proves the payload's `kind`, which the adapter sets only for 40001. **A statement's conflict goes through Prisma's request handler and arrives as P2034 (face one); a COMMIT's conflict comes straight from the adapter.** It is **stabler than prose**: `name`, `cause.kind` and `cause.originalCode`.

**Demonstrated, not read (`bl924-error-shape.ts`).** Inside one Serializable transaction on the tick's own client (`db-cron`), a temp table with a DEFERRABLE INITIALLY DEFERRED constraint trigger makes Postgres raise a real `40001` at COMMIT. The caller received **`DriverAdapterError`, message `TransactionWriteConflict`, `code` null, `cause {kind: TransactionWriteConflict, originalCode: "40001", originalMessage: "could not serialize access due to read/write dependencies among transactions"}`**. Its stack is frame for frame production's (`:687`, `:682`, `:641`, `transaction-manager.ts:422`). The commit failed, so everything rolled back; `pg_proc` and `pg_class` then show **0** of the temp objects. **`isTransactionConflict` on main (blob `5b40d49e`): false.** False as well on all six rows' shapes, both as recorded and with the adapter's `cause` restored. The catch-up round's reading was right, and it is now demonstrated.

## PART 2: was any money wrong? No.
Read `2026-09-23 10:17:47+00`. The owner cut is checked against the tick's own rule: `guaranteeOwnerSplit` is on for both campaigns, so the cut is `calculateOwnerEarningsGuaranteed(ownerCutClipperGross(...), s)`, BL-916's one definition.

| clip | today: poster (base + bonus) | maker | platform | owner | by the one definition | rewritten after the failure |
|---|---|---|---|---|---|---|
| cmua7m2h | 0.95 (0.90 + 0.05) at 1801 views | none | none | 0.61 | $0.61, **matches** | yes, 2026-09-23 05:00:28 |
| cmu7ba2v | 0.54 (0.53 + 0.01) at 1063 | none | none | 0.35 | $0.35, **matches** | yes, 05:00:27 |
| cmua3t5p (v2) | 0 at 7 views | 0 | 0 | none | $0.00 | yes, 10:00:24 |
| cmu9441s (v2) | 0 at 4 views | 0 | 0 | none | $0.00 | yes, 10:00:22 |
| **cmsrngha** | 0.72 (0.67 + 0.05) at 1340 | none | none | **0.46** | **$0.46 = 0.72 × 0.39002074 / 0.60997926, matches** | no later stat; views unchanged since |
| cmtx4efs | 0 at 527 (under the 1,000 minimum) | none | none | none | $0.00 | no later stat |

**The $0.46 owner cut is correct today.** It was last written `2026-09-19 18:02:01.797`, before the failure. The failed tick proposed exactly the stored $0.72 and $0.46, so the failure cost nothing. In all six rows the proposed figures equal what the next successful tick or the unchanged row holds.

**PAID payouts:** `cmsrngha` sits in the clip snapshot of PAID payout `cmte1wmc…`, paid `2026-09-04 20:14:23`, and its figures have not moved since, so a correct figure was paid. `cmua7m2h` (payouts paid 09-10 and 09-17) and `cmtx4efs` (08-24 and 09-01) have PAID payouts on the same person and campaign that do not name the clip. The population's paid-is-final check (below) is 0 for both earners. **No wrong figure was paid.**

**Zhus Edit cmsisj3d, PAUSED MANUAL, carrying four of the six: it IS getting money writes, and the pause is not a gate on them.** 901 approved clips, 854 active jobs, last checked `2026-09-23 10:00:20`. Of the 484 approved clips over its 1,000 view minimum, **469 have their owner row at the views of their latest check**. The 15 that do not were all last checked more than 7 days ago (logged). Owner rows were written in 38 of the last 48 hours. The hours with checks and no owner writes are hours whose rows were rewritten again later: an owner row keeps only its latest `updatedAt`, so a per-hour count cannot show an old write, and I stopped inferring from it. BL-917's two quiet ticks on 2026-09-20 cannot be re-measured from rows that have been overwritten since; nothing today is missing.

## PART 3: the fix, narrowly (`clip-earnings-writer.ts` `5b40d49e` → `80418a18`, protected and changed on purpose)

```diff
@@ -161,6 +161,17 @@ function r2(n: number): number {
 export function isTransactionConflict(e: any): boolean {
   const code = String(e?.code ?? e?.cause?.code ?? e?.meta?.code ?? "");
   if (code === "P2034" || code === "40001" || code === "40P01") return true;
+  // BL-924 — THE THIRD FACE: the conflict raised by COMMIT. A statement's
+  // conflict reaches the caller as Prisma's P2034, but Postgres can also refuse
+  // the COMMIT itself, and that error comes straight from @prisma/adapter-pg as
+  // a DriverAdapterError whose message is its `cause.kind`, with no `code`
+  // anywhere: `cause` is `{ kind: "TransactionWriteConflict", originalCode:
+  // "40001", originalMessage }`. Six production ticks gave up on it after one
+  // attempt. Matched on the adapter's own structure, never on the message.
+  if (
+    e?.name === "DriverAdapterError" &&
+    (e?.cause?.kind === "TransactionWriteConflict" || e?.cause?.originalCode === "40001")
+  ) return true;
   const msg = String(e?.message ?? "");
```
**Every line.** The seven comment lines say which face this is, where it comes from, and why the match is structural. `e?.name === "DriverAdapterError"` restricts the new test to the adapter's own error class, the same test the adapter uses in `isDriverAdapterError`. The class is not imported, so no Prisma module enters this file or any browser bundle. `cause.kind === "TransactionWriteConflict"` is Prisma's own name for SQLSTATE 40001. `cause.originalCode === "40001"` is the SQLSTATE itself. Either suffices, so one renamed field in a future adapter version cannot silently reopen this. `return true` sends it down the path P2034 already takes.

**It matches:** only a `DriverAdapterError` carrying Postgres 40001. **It deliberately does not match:** any other adapter kind (unique, null, foreign key, too many connections, `postgres` with another code); a plain Error whose message is or contains "TransactionWriteConflict" (no message test was added); an object with that `cause.kind` under another name. Eight such cases are demonstrated false below. A retry on a non-conflict repeats a money transaction six times over 15.5 s; this condition cannot cause one.

**All three catches rethrow it (`bl924-catches.ts`).** The planted error was the real class with the payload Postgres produced, thrown at each read in turn. **On main, 0 of 3:** each catch swallowed it, and the write then died on "current transaction is aborted". Main's retry does recognise that message (BL-917's second face), so a conflict inside a gate was never the lost case: the COMMIT was. **After, 3 of 3:** the L1 budget gate, the fairness gate and the v2 point read each rethrow the planted object itself (`===`), and the retry sees a conflict.

**The attempts nit is NOT one line, so it is named and not fixed.** The loop's counter is block-scoped inside the `for`, so recording it needs a declaration, an assignment and the read, in `tracking.ts`, a second protected money file. D1 below shows why it matters: main made ONE attempt and the row says 6.

## PART 4: demonstrations
• **The predicate:** see PART 1. On the real COMMIT error: main **false**, after **true**. On the six rows with the adapter's `cause`: 6 false, then 6 true. Eight non-conflicts, all false before and after: a real 23505 and a real 22P02 from Postgres (P2010), adapter kinds UniqueConstraintViolation, TooManyConnections and `postgres` 25P01, a plain Error "TransactionWriteConflict", a `cause.kind` under another name, and "NotATransactionWriteConflictReally". The last two show that a match on the name, or on a substring of it, was not taken.
• **The real tick's retry (`bl924-retry.ts`).** `processTrackingJob`, cron shape, no fetch; its `$transaction` is wrapped so the first K Serializable calls reject with the real error class. Each case has its own person, campaign, account and clip, CPM 0.37, prime views.

| case | writer | injected | Serializable attempts | real waits | result | what made it pass |
|---|---|---|---|---|---|---|
| D1 | **main** 5b40d49e | 2 conflicts | **1** | none | $0.00, audit row "TransactionWriteConflict", code null, **attempts 6** | a second attempt would have committed; main gave up, **production's exact signature** |
| D2 | fix 80418a18 | 3 conflicts | **4** | 630, 1,122, 2,208 ms | **$1.17** = 3163 × 0.37 / 1000 = 1.17031, owner written, no audit row | the real commit on attempt 4 |
| D3 | fix | UniqueConstraintViolation every time | **1** | none | $0.00, recorded, 1,267 ms end to end | **a non-conflict still fails fast** |
| D4 | fix | conflict every time | **6** | 739, 1,201, 2,039, 4,047, 8,137 ms | $0.00, recorded | the whole schedule, 16.2 s of waits, then gives up |

Each wait sits inside the schedule's window (the delay plus up to 250 ms of jitter, plus 150 ms allowed for the attempt). Setups were checks too: the right blob on disk for each case, the payload is Postgres's own, and the clip starts at $0.00. 28 of 28. **No HTTP path changed and no route was called, so there is no 429 to assert.**
• **Guards:** none was touched and none added (the brief asked for one condition). Every prebuild guard passes; see PART 5.

## PART 5: proof and merge
• **Invariants, full population, open `10:23:08+00` and close `10:26:01+00`, 16 of 16:** 10,242 live clips, 0 earnings-invariant breaches, 0 negative. 39 v2 maker rows, 0 breaches. No double pay (agency 0, maker 0, platform 0, posts 0). 21 budgeted campaigns, **0 over** counting both v2 aggregates and the owner's cut. Paid is final: maker 0, v2 poster 0. **Never decrease: 10,334 real clips compared, 0 decreased.** **ANGIE BROWN: one row, $2,700.00, ACTIVE, spent $7.30.** **Both reconciliation forms return 0 rows at open and 0 at close, so there is nothing to explain.** Every money fingerprint is identical: clip earnings, clip status, campaign state, agency, v2 maker, v2 platform, payouts.
• **The other money files by `git rev-parse` (pre-BL-924 vs HEAD):** `earnings-calc 00410634`, `balance 67c30c89`, `tracking 672d2ab3`, `invariant-middleware 61cef393` and `money-decimal ef5cdae7`, all **IDENTICAL**. The only change is the writer, above.
• **Guards and builds:** baseline tsc on main's tree 0 errors (exit 0); on the branch 0 (exit 0). Build #1 exit 0 and build #2 (committed tree) exit 0, from logs with the exit code echoed. **All 21 prebuild guards pass**, including `check:cron-wiring`, `check:css-tokens`, `check:page-titles`, `check:v2-single-share-writers`, `check:budget-lock` and `check:v2-rules-gate`: 32 PASS lines, 0 FAIL. **Hooks gate 0 errors, 10 warnings against the cap of 11** (the last measure was 10 of 11, confirmed); eslint is present. The 11 BL-678 guards are untouched. `check:prisma-bypass` passes (the proofs use `db` and `db-cron`, never a new client).
• **Teardown:** opening snapshot at T = `2026-09-23 10:23:02.38+00`. Closing at the same T: users 1,788, campaigns 36, accounts 1,544, campaign accounts 836, v2 clips 27, posts 39, poster states 81, rules rows 0, clips 10,334, activity 890, notifications 15,617 and audit 32,324, **every one identical in count and id fingerprint**. **Real rows written: none.**
• **BACKLOG:** BL-924 appended; `## BL-` entries 232 → 233 (BL-723 has no heading, so excluding it changes nothing). Four follow-ups: the attempts nit, and recording `cause` in the audit row; **eleven other Serializable retry sites test `code === "P2034"` alone and will not retry this same COMMIT face**; the "P2034" wording of the tick's log line; the 15 Zhus Edit rows last checked over a week ago.

**Mistakes of mine, disclosed.** I used shell heredocs twice for small script edits, against the brief; no harm, and every later edit went through the edit tool. My first two PART 2 queries guessed column names (`details->>` on a text column, `clips.views`), both refused by Postgres, then read and corrected. One merge command chained `git rev-parse --short` on two revisions, which failed before anything was tagged or merged; redone step by step. The per-hour owner-write count first looked like evidence of missed writes; it cannot show an overwritten hour, and the conclusion rests on the latest-check test instead.

**IN ONE LINE: a TransactionWriteConflict raised at COMMIT is now retried on the six-attempt schedule (demonstrated false on main, true after, retried and committed on the real tick), and no real money was ever wrong: all six clips match the tick's own rule today, the $0.46 owner cut included, and nothing wrong was paid.**
