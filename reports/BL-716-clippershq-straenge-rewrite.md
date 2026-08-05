# BL-716 — what rewrote a clipper's STRAENGE earnings downward on 2026-08-01, and was it correct

READ ONLY AUDIT. No code, data or money changed. Nothing recalculated, re-derived or repaired. `agency-monitor --fix` NOT run. No repair SQL executed. Only `SELECT` through `scripts/run-select.js`, which refuses every write keyword. The handle is redacted; the account is **Clipper A** (`cmqez5c2`). No wallet address appears here.

Code read at `origin/main` = `1faf072a` in an isolated worktree at `C:/b716`. DB read live. Every timestamp is cast `::text` and quoted against `now()` = **2026-08-05 11:38:46.494026+00**.

---

## VERDICT (one line)

**Yes, Clipper A is owed the $60.47: his recorded STRAENGE earnings were written below a payment already made, and the arithmetic supports $1,894.14 over $1,833.67 on every rule the platform states. But the 2026-08-01 06:31 run did not do it, wrote no earnings at all, and BL-714's Finding 4 attributes the loss to the wrong event by two weeks.**

---

## HEADLINE: THE 06:31 RUN MOVED $0.00

BL-714 read 83 STRAENGE clip rows carrying `updatedAt` at 2026-08-01 06:31 and concluded the budget ceiling had been re-applied. It had not. What ran at 06:31 wrote the fraud score, which sits ABOVE the earnings gate. Three independent proofs:

| Proof | Measurement |
|---|---|
| `fraudCheckedAt` matches `updatedAt` to the second, per second, for all 83 clips | 5,5,7,7,8,8,8,8,8,9,8,2 across 06:31:04 to 06:31:15 on both columns |
| Every non marketplace CPM_SPLIT earnings write upserts the AgencyEarning row in the SAME transaction (`tracking.ts:2764` then `:2789`) | **Zero** STRAENGE agency rows written on 2026-08-01. Last STRAENGE agency write anywhere: **2026-07-19 14:16:30.568** |
| `agency.amount × 2` equals `clip.earnings` on **111 of 111** STRAENGE clips with an agency row (s = 0.33333333, so owner = clipper × 0.5) | Clipper A: 72 of 72 exact, agency rows stamped 2026-07-14 17:51 to **2026-07-17 16:29** |

**So Clipper A's STRAENGE total has been $1,833.67 since 2026-07-17 16:29:02.696 at the latest.** BL-690, measured 2026-07-30, states the same $1,833.67 to the cent (its $1,848.32 was lifetime, that is $1,833.67 STRAENGE plus $14.65 Panic Baby, which is also the $14.65 it says he could have withdrawn). Two independent measurements, twelve days apart, identical.

---

# PART 1 — what ran at 06:31 on 2026-08-01

**The process:** the tracking cron batch, at `src/lib/tracking.ts:1819` (`db.clip.update({ fraudScore, fraudReasons, fraudCheckedAt })`), reached through `runDueTrackingJobs`. ClipStat is written above the same gate at `tracking.ts:1770/1782`; all 83 clips got a stat row inside the same minute.

**Which batch.** `cron_runs` rows near the window: 06:20:33.355, then **06:31:16.929**. The heartbeat row is inserted at the TOP of the route (`src/app/api/cron/tracking/route.ts:147`), so the 06:31:16.929 row was created 1.7s AFTER the clip writes ended at 06:31:15.2. The writing batch is therefore the one whose heartbeat is **06:20:33.355**, its Apify poll returning about ten minutes later.

**It bypassed the audit log, exactly as the 2026-07-18 sweep did in BL-638.** `audit_logs` between 05:00 and 09:00 on 2026-08-01 holds only Discord and APPROVED_CLIP rows. There is no `FORCE_RECALC_EARNINGS` row (`force-recalc-earnings/route.ts:423` always writes one), so force recalc is ruled out. There is no earnings action of any kind in `audit_logs`, ever.

**Reconstructed from timestamps, the full sequence:**

| Time (`::text`) | Event | Source |
|---|---|---|
| 2026-08-01 06:20:33.355 | tracking batch starts | `cron_runs` |
| 06:25:59.658 | STRAENGE PAST to ACTIVE, `MANUAL_OWNER`, "Manual unpause via campaigns PATCH" | `campaign_status_changes` |
| 06:31:04.181 to 06:31:15.200 | 83 ClipStat rows plus 83 fraud score writes | `clip_stats`, `clips.fraudCheckedAt` |
| 06:31:16.929 | next tracking heartbeat | `cron_runs` |
| 06:31:33.746 | ACTIVE to PAUSED, `MANUAL_OWNER`, "Owner triggered Pause & Freeze (BL-145)" | `campaign_status_changes` |
| 06:31:33.721 / 06:31:38.144 | `campaigns.lastBudgetPauseAt` / `campaigns.updatedAt` | `campaigns` |

The 06:31:33 event is **not** an AUTO budget pause. It is the owner pressing Pause & Freeze at `src/app/api/admin/campaigns/[id]/freeze/route.ts:85`, which writes three campaign columns and, by construction, **no clip row at all**.

**Blast radius of that run: 83 clips, 9 clippers, 1 campaign, $0.00 of earnings moved.** Earnings touched: 0 clips, 0 clippers.

---

# PART 2 — how it got past the never decrease guard

Three mechanisms were on the table. The answer is the third, and it is neither of the first two.

**Not a bypassed guard.** `decideNeverDecrease` has exactly two callers in the whole tree (`grep -rn "earnings-never-decrease" src`): `src/app/api/admin/force-recalc-earnings/route.ts:13` and `src/lib/campaign-freeze-undo.ts:84`. The cron never calls it. The guard's own header says so at `src/lib/earnings-never-decrease.ts:26-36`: it covers "RETROACTIVE bulk recomputes, the undo, force recalc", and explicitly excludes "the normal cron". It was not bypassed. It was never in this path.

**Not clips excluded from the sum.** Clipper A has zero clips with `videoUnavailable`, zero deleted, zero `payoutReductionRatio`, zero `earningsFrozenAt`. His clip count went UP, from 72 at the payout to 80 now.

**The actual mechanism: `src/lib/tracking.ts:2507-2521`, the BL-162 per clip clipper pool cap, an ABSOLUTE trim with no floor at the clip's stored value.**

```
clipperPoolCap   = (1 - s) × budget                       tracking.ts:2486
otherClipperSpent= Σ campaign earnings - this clip        tracking.ts:2489
clipperHeadroom  = max(clipperPoolCap - otherClipperSpent, 0)   tracking.ts:2500
if (newEarnings > clipperHeadroom) newEarnings = clipperHeadroom   tracking.ts:2507
```

Every OTHER budget path in the same function is guarded against writing a clip down. The BL-162 delta scaler at `:2236` runs only `if (newEarnings > oldClipperEarn)`. The legacy proportional cut at `:2271` runs only `if (newEarnings > oldClipperEarn)`. `proportional-cut.ts:110` sums `Math.max(0, proposed - current)`, positives only. The L1 budget hard lock at `clip-earnings-writer.ts:152` fires only when `delta > 0` and states plainly "**Decreases always pass**". The trim at `:2507` is the one place with no such guard, and it is an absolute assignment, not a delta.

**Why that redistributes rather than merely caps.** The pool is shared. Once it is full, `clipperHeadroom` for the clip being processed equals `this clip - overshoot`. When another clipper's clips grow into the pool first, the clips processed later are trimmed to make room for them. A clipper's recorded earnings therefore fall because somebody else's rose, not because anything about his own clips changed. That is a campaign level total falling while no individual entitlement fell, and it is the third of the three mechanisms the brief named, with a different fix from the other two.

**When it fired.** The drop is bounded to **2026-07-07 16:01:36 to 2026-07-17 16:29:02**, and no audit row records it. Inside that window sits an off audit repair script: `audit_logs` holds `BUDGET_HARDLOCK_THROW` at **2026-07-16 11:54:34.759**, `campaignId` STRAENGE, `reason: "BL-525-straenge-pause-fix"`, `spent 2794.09, delta 244.48, projected 3038.57`. The clip it was thrown on **belongs to Clipper A**. In the same two minutes, 2026-07-16 11:53 to 11:54, ten agency rows were written for four OTHER STRAENGE clippers and none for Clipper A. So a script was writing this campaign's earnings, other clippers were being raised, and his clip was being refused. **I cannot date the drop more precisely than that window. The platform stores no earnings history, `savedEarnings` is 0 on all 80 of his clips, and no audit action records an earnings write. Named as unmeasurable.**

---

# PART 3 — was the new number right? No. Neither is $1,833.67 defensible on any rule the platform states.

**Inputs, measured, not assumed.** Campaign: budget $3,000, CPM_SPLIT, `guaranteeOwnerSplit = true`, `lockedOwnerShareDecimal = 0.33333333`, so clipper pool cap $2,000 and owner reserve $1,000. Every one of his 80 clips carries `cpmAtSubmissionDecimal = 0.5000`, `maxPayoutPerClipAtApproval = 300` (null on 3), `minViewsAtApproval = 1000` (null on 3). BL-563's shared gross guard resolves `gross` here (ownerCpm/clipperCpm = 0.25/0.5 = 0.5 agrees with s/(1-s) = 0.5), which is why owner equals clipper × 0.5 on every row and why the agency identity above holds.

**Uncapped entitlement, computed from `clip_stats` views, stamped CPM, per clip cap and the minViews gate:**

| Moment | Clipper A clips | A views | **A uncapped gross** | Others uncapped | Pool total |
|---|---|---|---|---|---|
| 2026-07-07 16:01:36 (the payout) | 72 | 4,507,552 | **$1,962.63** | $107.10 | $2,069.73 |
| now | 80 | 5,403,031 | **$2,450.55** | $192.23 | $2,642.78 |

**What each side actually holds:**

```
2026-07-07 13:21:47  AUTO_BUDGET pause, reason states "clipper pool $2000.00 reached cap $2000.00"
2026-07-07 16:01:36  A = 1,894.14   others =   105.86   pool = 2,000.00   (A's uncapped then 1,962.63, so 1,894.14 is inside it)
now                  A = 1,833.67   others =   168.04   pool = 2,001.71

               A  -60.47
          others  +62.18
           pool   + 1.71   <-- the pool barely moved. The $60.47 moved sideways, from him to other clippers.
```

That reconciles to the cent. He did not lose money to the ceiling. He lost it to other clippers inside a fixed pool.

**Three candidate answers, all computed:**

| Rule | A's correct figure | Source of the rule |
|---|---|---|
| Ratchet, that is scaled positive deltas that never fall | **$1,894.14** | BL-534 "budget IS the deal", BL-538 never decrease, `tracking.ts:2236/2271` |
| Fresh pro rata of the $2,000 pool on today's uncapped entitlement | **$1,854.52** = 2000 × 2450.55 / 2642.78 | the fairness intent stated in `proportional-cut.ts:1-14` |
| Stored today | $1,833.67 | the database |

**$1,833.67 is below both principled figures.** It is $60.47 below the ratchet figure and $20.85 below a fresh pro rata split. There is no rule in this codebase under which it is correct. Views never fell far enough to justify it either: across 4,572 stat rows on his clips there are 8 decreases, the largest 409 views ($0.20), all in June, all recovered, and his current views are his peak.

**Answer: $1,894.14 is correct, $1,833.67 is a defect, and he is owed $60.47.** The honest qualification: the gate at `payouts/route.ts:483` proves his STRAENGE earnings were **at least** $1,894.14 at 16:01:36 on 2026-07-07, and I cannot prove they were exactly that. If he requested less than his maximum, the true figure was higher and he is owed more, never less. Even on the most conservative rule available, a fresh pro rata split, he is owed $20.85.

---

# PART 4 — who else was hit on 2026-08-01

**By the 06:31 run: nobody. Zero clippers, $0.00.** All 9 clippers whose clips it touched are listed with their unchanged totals:

| Clipper | Clips touched 06:31 | Earnings before | Earnings after | Delta | Clamp position |
|---|---|---|---|---|---|
| **Clipper A** `cmqez5c2` | 47 | $1,833.67 | $1,833.67 | **$0.00** | unchanged, $60.47 overpaid |
| `cmq7qh6p` | 22 | $94.53 | $94.53 | $0.00 | unchanged |
| `cmqs7gjq` | 3 | $64.84 | $64.84 | $0.00 | unchanged |
| `cmqjrpot` | 3 | $0.00 | $0.00 | $0.00 | unchanged |
| `cmpqgoid` | 2 | $0.00 | $0.00 | $0.00 | unchanged |
| `cmpfp1mw` | 2 | $0.00 | $0.00 | $0.00 | unchanged |
| `cmqigxs8` | 2 | $0.00 | $0.00 | $0.00 | unchanged |
| `cmqxtmu6` | 1 | $0.99 | $0.99 | $0.00 | unchanged |
| `cmraz576` | 1 | $0.00 | $0.00 | $0.00 | unchanged |
| **Total** | **83** | | | **$0.00** | |

**Platform wide on 2026-08-01, every campaign, from agency row writes (the same transaction as every CPM_SPLIT earnings write):** bees.n.honey 14 rows across 6 clippers, Panic Baby 9 across 3, BAD BITCH ANTHEM (2.50) 1 across 1, STRAENGE **0**. All ACTIVE campaigns well under their pool caps, all ordinary upward accrual. **Platform wide earnings movement attributable to the run under investigation: $0.00.**

**Anyone else recorded below what they have already been paid.** Recomputed independently on `isPayoutMoneyOut` semantics (`balance.ts:117`), not taken from BL-714:

| Clipper | Campaign | Campaign status | Recorded earned | Paid | Recorded below paid by |
|---|---|---|---|---|---|
| **`cmqez5c2` (Clipper A)** | STRAENGE | PAST | $1,833.67 | $1,894.14 | **$60.47** |
| `cmofpudr` | somesome | PAST | $1,570.58 | $1,607.33 | $36.75 |
| `cmoaejuc` | somesome | PAST | $38.80 | $61.89 | $23.09 |
| `cmq0qn2l` | GainzAlgo (REPOST) | PAST | $0.00 | $14.46 | $14.46 |
| `cmoal818` | somesome | PAST | $4.94 | $12.76 | $7.82 |
| `cmova7yd` | BAD BITCH ANTHEM (2.50) | ACTIVE | $29.19 | $30.00 | $0.81 |
| `cmp71p89` | somesome | PAST | $33.99 | $34.79 | $0.80 |
| `cmqmnvgs` | WinGram | ACTIVE | $11.21 | $11.23 | $0.02 |
| **8 clippers** | | | | | **$144.22** |

Five of the other seven sit on somesome and GainzAlgo, both PAST and both `guaranteeOwnerSplit` campaigns, so the same mechanism is the leading candidate for them and none of them has been asked. **Nobody lost money on 2026-08-01. Seven people besides Clipper A are carrying an unexplained shortfall that predates it.**

---

# PART 5 — is it still happening?

**Not on STRAENGE, and not tonight.** The campaign is `status = PAST`, `pauseSource = AUTO`, `lastBudgetPauseAt = 2026-08-01 06:31:33.721`. `campaignStatusBlocks` at `tracking.ts:1935` returns true on `isAutoPausedCampaign` OR `status === "PAST"`, so every cron tick skips the earnings path entirely. It cannot rewrite again unless the owner resumes it, which is precisely what he did at 06:25:59 on 2026-08-01.

**The cron itself keeps running.** `src/lib/railway-cron-scheduler.ts:63` fires tracking every 10 minutes, plus the daily 06:00 UTC `retire-dead-clips` sweep at `:92`. On a PAST campaign the only thing that will move is `fraudCheckedAt` and `updatedAt`, which is cosmetic and is exactly what created this false alarm. **Expect STRAENGE `updatedAt` to move again with no money behind it.**

**The live exposure is bees.n.honey.** Clipper pool utilisation across all 11 `guaranteeOwnerSplit` campaigns:

| Campaign | Status | Clipper spend | Clipper pool cap | Used | Headroom |
|---|---|---|---|---|---|
| **bees.n.honey** | **ACTIVE** | $1,584.44 | $1,648.35 | **96.1%** | **$63.91** |
| Panic Baby | ACTIVE | $1,460.09 | $2,000.00 | 73.0% | $539.91 |
| WinGram | ACTIVE | $286.64 | $3,333.33 | 8.6% | $3,046.69 |
| BAD BITCH ANTHEM (2.50) | ACTIVE | $35.49 | $672.15 | 5.3% | $636.66 |
| STRAENGE | PAST | $2,001.71 | $2,000.00 | 100.1% | over by $1.71 |

**bees.n.honey is $63.91 of accrual away from the same trim, on 15 clippers, and it is ACTIVE right now.** That is the answer to whether this is a one off: the STRAENGE instance is finished, the mechanism is not.

---

# PART 6 — the verdict and the fix

## One line

**Yes. Clipper A is owed his $60.47 back, because $1,833.67 is below both the never decrease figure of $1,894.14 and a fresh pro rata figure of $1,854.52, and the payment he is being charged against was correct when it was made.**

## Ranked fix

**1. Money defect, the real one. `src/lib/tracking.ts:2507`.** Add the floor that every sibling branch already has:
`if (newEarnings > clipperHeadroom) newEarnings = Math.max(clipperHeadroom, currentClipEarnings)`, applied to `baseEarnings` and `bonusAmount` in the same breath so the L1 invariant at `clip-earnings-writer.ts` holds. **What must be proven:** on a read only dry run over bees.n.honey and STRAENGE, zero clips compute a lower value than they store, and the campaign totals do not exceed `clipperPoolCap` by more than they already do. The pool can end a few dollars over its cap, and that is the correct trade: the ceiling is the owner's money, the trim is the clipper's, and only one of the two was ever promised to a person. **Rollback:** revert the one commit, no data written. **Blast radius today: 1 clipper, $60.47, plus up to 7 older cases totalling $83.75 on the same shape.**

**2. Release the $60.47, as a correction and not a gift.** `src/app/api/payouts/route.ts:566-589` and `src/app/api/earnings/route.ts:259`. Do NOT disable `GLOBAL_PAYOUT_CLAMP_ENABLED`: BL-690 measured that turning it off releases the four other over held clippers too. The correct shape is BL-714's, a per payout `earnedAtPaymentSnapshot` clamped as `max(lifetimeEarned, Σ earnedAtPayment)`, which for him restores $1,894.14 as the floor and leaves the clamp doing its job for everybody else. **What must be proven:** each of the other four over held clippers still computes $0.00 global available, the BL-627 property BL-692 was gated on. **Rollback:** the snapshot column is additive; drop the clamp change and the column goes unread.

**3. Write an earnings history row.** `src/lib/clip-earnings-writer.ts`, additive, append only, on every call. Every unanswerable question in BL-714 and in this report failed on its absence, and this round only closed the ones it did because `agency_earnings.updatedAt` happened to act as an accidental shadow ledger. That accident will not survive the next schema change.

**4. Correct BL-714's Finding 4 in the record.** It names the 2026-08-01 06:31 run as the cause. Left standing, the next round will patch a fraud score writer.

## When recorded earnings fall below money already paid, what the rule SHOULD be

Charging a past overpayment against a different campaign's live money is defensible **only when the original figure was genuinely wrong at the moment it was paid**. Here it was not: $1,894.14 sat inside his uncapped entitlement of $1,962.63 and inside a pool the campaign had already reserved. So the rule should be:

**A payment, once made, is a floor.** The budget ceiling may stop earnings growing, which is BL-534's rule and nobody should argue with it, but it may never rewrite a figure the platform has already settled in cash. Where a shared pool must be trimmed, the trim comes off unpaid headroom first and off already paid earnings never. If that means a campaign finishes a few dollars over its ceiling, the overrun is the owner's cost of having paid early, which is the correct place for it. The only case where a clawback against live money is legitimate is a payment that was wrong when it was made, and that case should be recorded as an explicit adjustment with a reason, not applied silently by a `Math.min` on a cash out screen.

---

## Safety statement

READ ONLY. One document produced. No source file modified, so no build was run and none is claimed; a markdown only change cannot affect `tsc`. Nothing recalculated, re-derived or repaired. `agency-monitor --fix` NOT run. No repair SQL executed. No payout created, modified, approved, rejected or cancelled. No balance, clip status, earnings field, schema or env flag touched. Every statement was a `SELECT` through `scripts/run-select.js`. Every figure in PART 3 was computed independently from `clip_stats` views, stamped CPMs, the per clip cap and the minViews gate, not read from either disputed stored value. Work was done in an isolated worktree at `C:/b716`; `node_modules` was never junctioned; the shared tree's HEAD was not moved and nothing held by the concurrent BL-715 or BL-717 rounds was touched. The handle is redacted and no wallet address appears.

**Stated plainly, what could not be measured:** the exact moment the $60.47 was written off, beyond the window 2026-07-07 16:01:36 to 2026-07-17 16:29:02; whether $1,894.14 was exactly his stored total at the payout or merely a floor the gate proves; and whether the other seven clippers recorded below their payments lost their money to the same trim, which would need the same window reconstructed on somesome and GainzAlgo.
