# BL-827 — the owner's payout figure is final, and a payout he has priced is always payable

**2026-08-24 · DB `now()` = `2026-08-24 18:17:24.250199+00` (first read) to `19:30:58.251873+00` (last) · BUILD, PAY AND MERGE.**
Base `origin/main` @ `100e8483`. Branch `checkpoint/BL-827` @ `1182e761`. **Merged and verified pushed: `origin/main == local == c49f3209`.** Tags `pre-BL-827`, `post-BL-827`, `pre-BL-827-merge`, `post-BL-827-merge`, all on origin. Isolated worktree `C:/w827`, a short path, `node_modules` never junctioned, **removed at the end**. Every read through `scripts/run-select.js`, every timestamp cast `::text` against DB `now()`. Handles redacted, **no wallet address read or printed**.

**A REDEPLOY ON RAILWAY IS REQUIRED BEFORE ANY OF THIS IS LIVE — except the payment, which is already recorded.**

> ## THE HEADLINE
> **Clipper M's payout is PAID at `$11.00` gross. He receives `$9.57`.** `paidAt = 2026-08-24 18:46:48.937`, marked paid through the real route as the real owner. Eight days of failure ended.
> **The constraint was NOT removed.** `payout_amount_positive` is byte-identical. The code stopped asking the database to store a zero; the database never stopped being right to refuse one.
> **PART 0's design question was put to the owner and he answered it.** Setting `$11.00` is a PAYMENT decision; scaling 40 clips is an EARNINGS decision, and the amount **can** be recorded without touching earnings. I recommended decoupling. **He chose to keep the cut.** So the 40 clips stay at `$25.65`, which is `$56.30` **below** money already paid, permanently. **PART 2's earnings check therefore does not pass, and this report says so rather than smoothing it.**
> **Three more defects were found on the way**, and the largest is that his own screen would have told him he received `$11.00` for a payment of `$9.57`.
> **My own first fix was wrong and the suite caught it** before it shipped.

---

## PART 0 — WHAT THE ADJUSTMENT ACTUALLY DOES, AND THE DESIGN QUESTION

### File:line, exactly

`src/app/api/admin/payouts/[id]/adjust/route.ts`. It does **both** things, in one transaction:

| # | line | what it does |
|---|---|---|
| 1 | `:161` | `ratio = actualPaidAmount / requestedAmount` — `11 / 60.27 = 0.182512…` |
| 2 | `:301-318` | per snapshot clip: `newBase = baseEarnings × ratio`, `newBonus = bonusAmount × ratio`, `newEarnings = newBase + newBonus`, written through `writeClipEarnings` |
| 3 | `:322-331` | stamps `payoutReductionRatio`, `earningsFrozenAt`, `earningsFrozenReason` on every clip |
| 4 | `:333-394` | shrinks `AgencyEarning` / `MarketplaceCreatorEarning` / `MarketplacePlatformEarning` |
| 5 | `:397-407` | writes the `PayoutAdjustment` row, including `originalEarningsSnapshot` |
| 6 | `:412-421` | sets `actualPaidAmount` on the payout and flips it to APPROVED |

So the answer to the brief's question is: **it scales per-clip earnings AND writes a separate adjustment record.** Step 6 alone is what records the payment. Steps 2 to 4 are the earnings decision riding along with it.

### THE DESIGN QUESTION, STATED PLAINLY

The owner wanted to pay `$11.00` for work he judged poor. **That is a payment decision, and it is entirely his.** Scaling 40 clips' recorded earnings by `0.1825` is a different decision about what the work was worth, and it is the one that dropped his record below money already paid and jammed the constraint.

### CAN THE AMOUNT BE RECORDED WITHOUT REWRITING PER-CLIP EARNINGS? YES, AND THE CODE ALREADY HAD THE MODE

Two independent proofs:

* **`actualPaidAmount` alone is authoritative everywhere that matters.** `clipperLiability` and `payoutLiability` (`balance.ts:126-152`) both read `actualPaidAmount ?? …` first, so stamping it makes `$11.00` the figure the balance, the gate and every display use. No clip has to move.
* **A payout-row-only path already exists.** `adjust/route.ts:186-214`, the `prrOnlyMode` branch, stamps `actualPaidAmount` and flips the status with **no per-clip shrink at all**, and it is reached today whenever every snapshot clip is already reduced. The capability was there; it was simply never the choice.

**MY RECOMMENDATION WAS TO DECOUPLE THEM**, and the reason is that BL-824 has just encoded the exact invariant this breaches: recorded earnings must never fall below money already paid. A mechanism that makes an earnings decision as an unavoidable side effect of a payment decision will keep producing that state.

### THE OWNER'S ANSWER, AND WHAT IT CHANGED

**He chose to keep the earnings cut**, deliberately, when shown both outcomes with the figures. So this round did **not** restore the 40 clips, and the design change is not "always decouple" but **"never decide it silently"**: the shrink remains available and now costs one explicit, typed acknowledgement. The owner keeps the power; the system stops making the choice for him.

**One correction I owe him.** When I put the choice to him I stated that keeping the cut would leave him able to claim `$0.00`. **That was wrong. The true figure is `$7.59`**, measured from his own `/api/earnings` after the payment. BL-824's `effectivePaidOut` bounds paid money by payable earnings **per campaign**, so the `$89.54` paid on Zhus Edit is capped at that campaign's `$25.65` and does not spill onto Zhus Meme. **BL-824 is containing the owner's cut to the campaign he made it on**, which is the rule working exactly as designed. The decision itself is unaffected.

---

## PART 1 — THE OWNER'S NUMBER IS NOW FINAL AND ALWAYS PAYABLE

### The diff, and what each line does

**`src/app/api/payouts/[id]/review/route.ts` — the gate is skipped when the owner has priced the row.**

```diff
+          const ownerSetAmount =
+            txExisting.actualPaidAmount != null && Number(txExisting.actualPaidAmount) > 0;
+
-          if ((action === "APPROVED" || action === "PAID") && txExisting.campaignId) {
+          if ((action === "APPROVED" || action === "PAID") && txExisting.campaignId && !ownerSetAmount) {
```

**Why this is right rather than lenient.** The BL-18 auto-adjust exists to shrink a payout the **clipper** requested at a figure that has since gone stale. `actualPaidAmount` is not a stale request: it is a number the **owner** typed, on this row, after seeing the balance. There is nothing left to correct, and correcting it anyway is the system overruling the person whose money it is.

**WHAT IT OVERRIDES, EXACTLY:** the campaign balance gate at `:211` and the BL-18 auto-adjust at `:249`, and nothing else. Still running on this path: the transition table, the idempotency short-circuit, Serializable isolation, the P2034 retry, both audit rows, and the notification and email fan-out. **`amount` is never rewritten**, so the constraint is never approached.

**A clipper can never reach this branch.** `actualPaidAmount` is written only by `admin/payouts/[id]/adjust`, which is `requireOwner`.

**Second half — the computation stops producing a zero.**

```diff
+              if (Math.round(campaignAvailable * 100) <= 0) {
+                throw new Error(`INSUFFICIENT_BALANCE:${campaignEarned}:${campaignPaidAndLocked + existingLiability}`);
+              }
               autoAdjustRef.value = { oldAmount: …, newAmount: campaignAvailable, … };
```

`campaignAvailable` is floored at `0` by `:208`, so a payout whose campaign no longer covers what is committed on it landed here with `newAmount = 0`, and `:283` wrote it. It now falls through to the **same typed `INSUFFICIENT_BALANCE`** the non-stale case uses, which `:335-340` already renders as a **400 naming both figures** — instead of a 503 saying "please retry" at something that can never succeed.

### THE CONSTRAINT WAS NOT TOUCHED, AND MUST NOT BE

`payout_amount_positive` (`CHECK ("amount" > 0)`, `scripts/migrations/F-DB-CHECK-CONSTRAINTS.sql:23`) is **unchanged, undropped and unweakened**. It is a real protection: a payout row recording zero or less is not a payment, and a status of PAID against it would tell a clipper he had been paid nothing while closing his claim. **The database was right to refuse. What was wrong was the code asking.** The suite asserts both that the constraint is still defined and that no `DROP CONSTRAINT` appears anywhere in this diff.

---

## PART 2 — PAID, EXACTLY `$11.00`

### GROSS OR CASH: GROSS, AND THE OWNER CHOSE IT EXPLICITLY

`actualPaidAmount` sits in the **gross** position. `adjust/route.ts:1-2` says so in its first sentence — the owner reduces a payout *"from its requested **gross** to an actual paid amount"* — and `clipperLiability` substitutes it directly for `amount`, which is the gross column. The adjust route never recomputes `feeAmount`, `expressFeeAmount` or `finalAmount`.

**Put to the owner with both options costed, he chose `$11.00` gross.**

```
RECORDED   actualPaidAmount   $11.00   (gross)
           platform fee 9%     $0.99
           express fee  4%     $0.44
           HE RECEIVES         $9.57
```

The alternative, `$11.00` in hand, would have required writing `$12.64` — a figure he never typed. **He receives `$9.57`.**

### Snapshot and exact rollback, printed BEFORE the write

Committed at `scripts/migrations/BL-827-ROLLBACK-payout-mark-paid.sql`, taken at `2026-08-24 18:42:43.47881+00`:

```
id cmsv1ifo705wr0xqwn4r8c5to · status APPROVED · amount 60.27 · feePercent 9 · feeAmount 5.42
expressFeePercent 4 · expressFeeAmount 2.41 · finalAmount 52.44 · actualPaidAmount 11.0000
paidAt NULL · reviewedAt 2026-08-24 17:03:43.213 · reviewedById <the owner>
updatedAt 2026-08-24 17:03:43.214 · rejectionReason NULL · referral_commissions on this payout: 0
```

The rollback restores every one of those by explicit id and deletes any commission row. **Nothing else in the round is a write**, so it is the complete reversal.

### The write

Made through the **real route** as the **real owner**, via a session minted for his own id (`scripts/bl827-mint-session.mjs`, which writes nothing: the token carries only `sub` and a `lastLoginDay` marker that suppresses the `lastLoginAt` stamp). A payment record naming `dev-owner-001` would have been a lie on the ledger.

```
POST /api/payouts/cmsv1ifo705wr0xqwn4r8c5to/review  {"action":"PAID"}   as OWNER  -> 200 {"success":true}

AFTER  status PAID · paidAt 2026-08-24 18:46:48.937 · actualPaidAmount 11.0000
       amount 60.27 (UNCHANGED) · finalAmount 52.44 (UNCHANGED) · reviewedById <the owner>
```

### What he was told, and it is truthful

```
notifications  PAYOUT_PAID  2026-08-24 18:46:49.17
  "Your payout has been sent. You receive $9.57, from your $60.27 request.
   Please allow a few business days for it to arrive."
```

**Without the fix in PART 5 this would have read `$11.00`.**

### Earnings versus money paid — THE CHECK THAT DOES NOT PASS, STATED PLAINLY

| | |
|---|---|
| recorded earnings, all campaigns | **$33.24** ($25.65 Zhus Edit + $7.59 Zhus Meme) |
| paid gross, all time | **$89.54** ($78.54 + $11.00) |
| **recorded earnings below money paid by** | **$56.30** |

**PART 2 asked me to confirm his recorded earnings no longer sit below money already paid. They still do, by `$56.30`, and that is the owner's deliberate decision rather than a defect this round left behind.** The only way to satisfy that check was to restore the 40 clips from `originalEarningsSnapshot`; he was shown that option with the figures and chose the other one.

### BL-627 and BL-696, both proven holding

| property | evidence |
|---|---|
| **BL-627, no overpayment** | `available` on his own `/api/earnings` is **`$7.59`**, floored at zero and positive, not negative. Platform-wide, **0 clippers** have negative recorded earnings. The `$56.30` shortfall does **not** become a debt: BL-824's `effectivePaidOut` caps Zhus Edit's paid figure at that campaign's `$25.65`, so it cannot reach across to Zhus Meme. `paidNoLongerOffsetting` reads **`$63.89`** on his own payload — the money the rule is holding back from offsetting. |
| **BL-696, no double pay** | The payout is a single row in a terminal state: `status PAID`, `paidAt` set. `validTransitions` (`review/route.ts:59-64`) allows PAID → VOIDED and nothing else, and the idempotency short-circuit at `:134` returns 200 without a second write if the action is re-sent. It is no longer in `lockedByUser`, so the `$60.27` cannot be re-requested; his campaign balance now reads `$7.59` on Zhus Meme and `$0.00` on Zhus Edit. |
| **earnings invariant** | **0 violations** before and after. |
| **no other clipper moved** | 7 payout adjustments before and after; no clip earnings written by this round at all. |

---

## PART 3 — THE WARNING THAT FIRED ON EVERYTHING

### Why it fired universally, file:line

`src/app/api/payouts/route.ts`. The per-campaign figure at `:207-208` **correctly** subtracts the payout's own liability (`ownLiab`) before comparing. The global clamp it is then reduced by at `:189-196` **did not**: `lockedByUser` at `:192` sums every in-flight payout, this one included. So `admin/payouts/page.tsx:1349` compared a row's amount against a balance the row had **already been taken out of**.

Algebraically, with one payout in flight it fired whenever `2 × self > earned − paid` — that is, on **any request worth more than half the clipper's remaining balance**.

### It is made accurate rather than removed

```diff
       if (clampOn) {
         const gAvail = globalAvailByUser.get(payout.userId);
-        if (gAvail != null) campaignAvailable = Math.min(campaignAvailable, gAvail);
+        if (gAvail != null) {
+          const raw = globalRawByUser.get(payout.userId) ?? gAvail;
+          const gAvailExcludingSelf = Math.round(Math.max(raw + ownLiab, 0) * 100) / 100;
+          campaignAvailable = Math.min(campaignAvailable, gAvailExcludingSelf);
+        }
       }
```

**Measured across every in-flight payout, before and after:**

```
payout      clipper   send    earned   paid    locked   warn OLD   warn NEW
cmq084lzp0  cmpq15k2  52.40    59.11    0.00   57.58     FIRES      silent
cmt00abj90  cmsviqg3  20.98    25.35    0.00   22.80     FIRES      silent
cmt1isvjo0  cmst7ibi  34.50    67.15    0.00   59.96     FIRES      silent
cmt1ixetv0  cmq8csdg  15.64    18.72    0.00   17.98     FIRES      silent
cmt1um8fn0  cmst7ibi  17.66    67.15    0.00   59.96     FIRES      silent
cmt5vcthe0  cmsm2zio  74.64   142.85   53.82   85.79     FIRES      silent
cmt6rzjii0  cmt5llnl  15.63    21.73    0.00   17.97     FIRES      silent
cmt7eqn2x0  cmpl310f  85.46    98.28   41.59   98.23     FIRES      silent
cmt7l69oe0  cmqqz593  14.36    19.49    0.00   14.96     silent     silent
```

**8 of 9 → 0 of 9**, and not one of those clippers is genuinely over-committed. The clamp itself is unchanged and still binds: no figure shown to the owner can exceed what the clipper could withdraw once this payout settles.

### MY FIRST VERSION OF THIS FIX WAS WRONG, AND THE SUITE CAUGHT IT

The first attempt added `ownLiab` back to the figure **after** it had been floored at zero. Since `max(x, 0) + self` equals exactly `self` whenever `x` is negative, `self > self` is false and **an over-committed row could never warn again** — the fix would have silenced the one case the warning exists for. The check *"a genuinely over-committed payout STILL warns"* failed at `90 vs 90`. **Add back first, floor second.** That check is in the shipped suite.

### Every APPROVED-but-unpaid payout, re-measured

DB `now()` = `2026-08-24 19:17:46.154107+00`.

| payout | clipper | status | gross | speed | age past deadline |
|---|---|---|---|---|---|
| `cmq084lzp0` | `cmpq15k2` | UNDER_REVIEW | 57.58 | STANDARD | **no deadline set**, requested `2026-06-05` — **80 days** |
| `cmt00abj90` | `cmsviqg3` | REQUESTED | 22.80 | EXPRESS | **4 days 07:51:26** |
| `cmt1isvjo0` | `cmst7ibi` | REQUESTED | 39.66 | EXPRESS | **3 days 06:25:21** |
| `cmt1ixetv0` | `cmq8csdg` | REQUESTED | 17.98 | EXPRESS | **3 days 06:21:50** |
| `cmt1um8fn0` | `cmst7ibi` | REQUESTED | 20.30 | EXPRESS | **3 days 00:54:36** |
| `cmt5vcthe0` | `cmsm2zio` | REQUESTED | 85.79 | EXPRESS | **05:22:51** |
| `cmt6rzjii0` | `cmt5llnl` | REQUESTED | 17.97 | EXPRESS | not yet due |
| `cmt7eqn2x0` | `cmpl310f` | REQUESTED | 98.23 | EXPRESS | not yet due |
| `cmt7l69oe0` | `cmqqz593` | REQUESTED | 14.96 | STANDARD | not yet due |

**Clipper M's row is gone from this list — it is PAID.** **APPROVED-but-unpaid is now empty.** Five express rows are overdue plus the 80-day UNDER_REVIEW row, against BL-811's three at 2 h, 3.6 d and 7 d.

**None of the nine is in the jammed state**: none carries a stale reduction on its snapshot clips, and every one has campaign headroom. Measured individually.

### The reminder engine has still never fired

```
payout_requests: 192 rows · rows with remindersSentCount > 0: 0 · max(lastReminderSentAt): NULL
notifications of any PAYOUT_REMINDER_* type, ever: 0
```

Unchanged since BL-811. BL-826 named the mechanism and it stands: `runPayoutRemindersOnce` is the **last** statement in `cron/tracking/route.ts:452-453`, a route declared `maxDuration = 300`, placed after tracking work measured at 21 to 58 minutes per hourly tick. **Not fixed here; it is its own round.**

---

## PART 4 — MAKING IT IMPOSSIBLE TO JAM AGAIN

### Guard 1 — an adjustment may never create an unpayable payout

`adjust/route.ts:92-101`. The old validation accepted `>= 0`, so `$0.00` was reachable: it stamps `actualPaidAmount = 0` and flips the row to APPROVED, and nothing downstream can then complete it honestly.

```
HTTP 400  ADJUST_WOULD_BE_UNPAYABLE
"A payout cannot be adjusted to $0.00 — a payment of nothing cannot be recorded as paid.
 To pay nothing, reject the payout instead so the clipper is told why."
```

"Pay this person nothing" is a real decision and it already has a route: REJECT, which notifies him with a reason.

### Guard 2 — an adjustment may not silently push earnings below money paid

`adjust/route.ts:334-383`, a read-only pre-flight **before** the transaction opens. It measures already-paid on the campaign through the **same `payoutLiability` chain** the mark-paid gate uses, so the two cannot drift.

```
HTTP 409  ADJUST_WOULD_PUSH_EARNINGS_BELOW_PAID
  postShrinkEarnings, alreadyPaidOnCampaign  (as fields, so the dialog and the server cannot disagree)
  message: "This would cut their recorded earnings on this campaign to $X, which is below the $Y
            already paid to them on it. Money already paid stays theirs, so the record would no
            longer cover it. The payment itself is fine. What goes below is the record of what
            their clips earned, and the next payout on this campaign will be refused because of it."
```

**It is an acknowledgement, not a refusal, and that is deliberate.** The owner is entitled to decide the work was worth 18.25% of its rate — this round exists to protect that. What he must not do is decide it by accident while typing a payment figure.

### DID BL-824'S GUARD FAIL HERE? NO — IT COULD NOT HAVE CAUGHT THIS, AND THAT IS THE FINDING

**BL-824 encoded the rule on the wrong side of the ledger to catch this, and it was never able to.**

`effectivePaidOut` (`balance.ts:234`) bounds what a payment **SUBTRACTS from a balance**: `min(paidGross, payableEarnings)`. It protects the clipper's balance from being driven negative by a payment. **It never inspects an earnings WRITE.** BL-824 wired it into three derivations — `computeBalance`, the withdrawal gate at `payouts/route.ts:713`, and `campaigns/[id]/min-payout-impact:185` — and every one of them is a **read**.

The adjust route writes through `writeClipEarnings`, which enforces `earnings = base + bonus` and knows nothing about payouts at all. **So the one write in the codebase that can drive a clipper's record below his own payment history had no check on it.**

Confirmed by import: `payouts/[id]/review/route.ts:8` imports only `payoutLiability`, never `effectivePaidOut`.

**And stated fairly: applying BL-824's rule to the mark-paid gate would not have saved this payout either.** `effectivePaid = min($78.54, $25.65) = $25.65`, so `campaignAvailable` would still have been `max(25.65 − 25.65, 0) = $0.00`, `:283` would still have written zero, and the constraint would still have refused. The gap is real and worth naming; it is not the blocker.

**The lineage:** BL-716 saw the state and wrote *"a payment, once made, is a floor"* without encoding it. BL-824 encoded the balance half. **This encodes the write half.**

### The guard demonstrated FAILING, then restored

`scripts/bl827-verify.ts` — **34 passed, 0 failed.** Structural checks extract each shipped guard from its own source file, so deleting one fails the suite rather than silently passing it. Each fix was reverted to `main` and the suite re-run:

```
REVERT payouts/[id]/review/route.ts      -> 4 FAIL  (gate skip, zero refusal, notification cash, email cash)
REVERT admin/payouts/[id]/adjust/route.ts -> 5 FAIL  (unpayable guard, below-paid guard, shared liability
                                                      chain, body-only acknowledgement, owner-facing copy)
REVERT payouts/route.ts                   -> 1 FAIL  (the clamp's add-back)
RESTORED                                  -> 34 passed, 0 failed
```

---

## PART 5 — WHAT THE CLIPPER SEES

### A defect found here, and it was the biggest one

`actualPaidAmount` is a **gross** figure. **Four surfaces rendered it as cash:**

| surface | file:line | said | should say |
|---|---|---|---|
| PAID notification | `review/route.ts:530` | `$11.00` | `$9.57` |
| PAID email | `review/route.ts:601` | `$11.00` | `$9.57` |
| his payout **card** | `PayoutsRedesign.tsx:128`, under the words **"You received"** | `$11.00` | `$9.57` |
| his payout **table** | `payouts/page.tsx:643` | `$11.00` | `$9.57` |

BL-813's own comment on the card asserts `actualPaidAmount` is *"the cash sent"*. **It is not**, and the adjust route's first sentence says the opposite. **This is BL-812's defect surviving on the one branch BL-812 did not reach**, and it is the same class BL-760 caught at `$5.44` and BL-763 at `$7.80`.

All four now re-derive through `calculatePayoutBreakdown` — the same helper that produced the row — so one number appears everywhere. Nothing stored changes.

### What his screens read now, rendered and seen

**Payout history, on his own account:**

> Zhus Edit (0.50 CPM) · Aug 16, 2026 · **Paid**
> **YOU RECEIVED**
> **$9.57**
> From your $60.27 request. **The owner set this payout to $11.00, and fees came off that.** · EXPRESS

**Is the difference explained, or does it just appear as a smaller number?** It is explained now, and it was not before. The old note read only *"From your $60.27 request"*, which left a `$50.70` gap with two causes — the owner set a smaller amount, **and** fees came off that — and named neither. The sentence now names both, and BL-813's `showBreakdown` still stays off on adjusted rows because `finalAmount` there is stale.

**Earnings page:** `AVAILABLE TO WITHDRAW $7.59`, with Zhus Meme showing *"$7.59 of $20.00 minimum, $12.41 to go"*. Zhus Edit no longer appears as withdrawable.

**Nothing contradicts BL-818's promise.** *"Money you were already paid stays yours, and it is never taken out of what you earn later"* is exactly what the `$7.59` demonstrates: `$89.54` of paid money sits against `$25.65` of recorded Zhus Edit earnings, and **none of the difference is charged against his Zhus Meme money.** `paidNoLongerOffsetting` reads `$63.89` on his own payload.

**His 40 clips display `$25.65`**, matching the owner's decision exactly, with `earningsFrozenReason` reading *"Payout adjustment 0.1825× (paid $11.00 of $60.27) on 2026-08-24"*.

### He was never told his earnings were cut, and that is on the record

**Zero `PAYOUT_ADJUSTED` notifications exist platform-wide, ever.** `notifyPayoutAdjusted` has never fired for anyone. He learned of the reduction only from the PAID notification's `$60.27` reference. **Reported, not fixed** — sending it now, eight days late and after the fact, is a decision for the owner rather than a bug fix.

### A sentence the owner can send

> Hi — your payout has gone out. You received $9.57. I set this payout to $11.00 rather than the $60.27 you requested, and the 9% platform fee and the 4% express fee came off that. Sorry it took so long to reach you; that part was a problem on our side, not anything to do with you.

It states what happened and who did it, invents no policy, and does not imply he did anything wrong.

---

## PART 6 — THE EVIDENCE

| claim | evidence |
|---|---|
| the `$11.00` payout is recorded as PAID | `status PAID`, `paidAt 2026-08-24 18:46:48.937`, `actualPaidAmount 11.0000`, `reviewedById` the owner's own id, `amount` unchanged at `60.27` |
| his recorded earnings are no longer below money paid | **THEY STILL ARE, by `$56.30`, by the owner's explicit choice.** Stated rather than smoothed |
| BL-627 no-overpayment holds | `available $7.59`, positive; 0 clippers platform-wide with negative recorded earnings |
| BL-696 no-double-pay holds | terminal PAID; only PAID → VOIDED permitted; idempotent re-send returns 200 with no second write; no longer in `lockedByUser` |
| no other clipper's earnings or balance moved | no clip earnings written by this round at all; `payout_adjustments` 7 before and after |
| the eight other in-flight payouts are unaffected | all nine re-measured; none jammed; APPROVED-but-unpaid is now empty |
| the universal warning is fixed | 8 of 9 → **0 of 9**, and a genuinely over-committed row still warns |
| the new guard demonstrated failing and restored | three reverts producing 4, 5 and 1 failures, then **34 passed, 0 failed** |
| the earnings invariant | **0 violations** throughout |
| `payout_amount_positive` | **untouched**; asserted still defined and never dropped |
| the 6 money files, `tracking.ts`, `campaign-era.ts` | **byte-identical by blob OID on BOTH refs**: `ac5be7de`, `797e2098`, `81a683c1`, `359bcbbe`, `61cef393`, `ef5cdae7`, `106e16ad` |
| schema | **no change**, no `prisma migrate`; `prisma generate` only |
| Apify | **no actor run**; the 11 BL-678 guards untouched |

### Rendered at all five widths, with the viewport MEASURED

**20 shots, every one at the asked width**, `window.innerWidth` printed beside each. Rendered as the **real owner** and the **real clipper** through minted sessions with the dev bypass off, because `app-layout.tsx:314` makes the shell ignore a real session while the bypass is on.

```
payouts-list          320 375 414 1280 1440
adjust-modal          320 375 414 1280 1440
below-paid-confirm    320 375 414 1280 1440
clipper-payout-card   320 375 414 1280 1440
ALL 20 SHOTS AT THE ASKED WIDTH. No horizontal overflow anywhere.
```

**The confirmation is photographed from a REAL 409, not a mock.** The guard returns before the transaction opens, so a refused adjustment writes nothing: all 15 refusals across the render pass left `payout_adjustments` at 7. Read at 320: the AlertTriangle heading *"Cut their recorded earnings below what they were paid?"*, the server's own sentence naming `$16.63` and `$46.83`, the three-row comparison, *"Type **below 46.83** to enable the button"*, Cancel and *"Cut earnings anyway"*.

The PNGs are deliberately **not committed** — the clipper's card carries his wallet address — and the harnesses that regenerate them are.

### Merged and pushed

| | |
|---|---|
| clean `tsc` baseline on the untouched worktree, **before any edit** | `npm ci` exit **0**, `npx prisma generate` exit **0** (before tsc, because `npm ci` wipes the client), `npx tsc --noEmit` exit **0**, `grep -c "error TS"` = **0** |
| branch | `checkpoint/BL-827` @ **`1182e761`**, VERIFIED on origin by `safe-push` |
| merge commit | **`c49f3209`**, `origin/main` verified by `safe-push` |
| conflicts | **none**; main never moved from `100e8483`, and the **merged tree OID equals the branch tree OID exactly** (`4bbfb70b`), so the branch's green build IS the merge's build |
| BACKLOG | **165 sections before, 166 after**, `BL-827` ×2, **0 conflict markers**, counted with `grep -c` and never piped to `head` |
| **`checkpoint/BL-723`** | **confirmed NOT an ancestor of main** |
| files | 7 source files, 4 harness scripts, 1 rollback SQL |
| worktree `C:/w827` | **removed**, 0 node processes left behind |

---

## THE ACCESSIBILITY REVIEW, RUN BEFORE ANY UI WAS WRITTEN

The lead and four specialists reviewed the **design**, and it changed the work rather than decorating it.

**The acknowledgement was NOT allowed inside the adjust modal**, on six measured facts about the shared `Modal`: no `role="dialog"`, no `aria-modal`, no accessible name, **no focus trap so Tab reaches other rows' Void and Reject buttons**, no `data-no-swipe` so a mobile drag translates it 280px away, and — for OWNER specifically — `app-layout.tsx:1051-1055` gives the sidebar wrapper a `transform`, making it the containing block for `position: fixed`, **so the scrim does not cover the page and the sidebar stays clickable**. This surface is owner-only, so 100% of its users hit that. It is `ConfirmDestructive` instead, which portals to `document.body` and already has all of it.

**It found a real bug in that shared component.** `confirm-destructive.tsx:129` returned focus to any node still `isConnected` — and `document.body` always is, while `body.focus()` is a silent no-op. Since `button.tsx:50` sets a **native** `disabled` while loading, the focused Apply button drops focus to `<body>` before the dialog even opens, so the captured return target was the body and cancelling stranded the owner at the top of an untrapped document. **The Void call site has been masking this** because its trigger is genuinely detached by then. Both fixed: `<body>` and `<html>` are rejected as return targets, and focus is parked on the modal panel before the button disables itself.

**The acknowledgement is not a stored flag, and the review named the failure precisely.** Refused at `$11.00`, acknowledged, then the field edited to `$5.00` and Apply pressed again would have written a **permanent earnings cut authorised by consent given for a different number**, whose post-shrink figure was never computed or shown. It is constructed inside the confirm handler and nowhere else, and the dialog closes the moment the amount moves away from the one it described.

**No toast on the 409.** sonner's region is `aria-live="polite"` at body level; a toast beside the dialog would put two live mutations in one commit and the owner would hear the same refusal twice in two wordings. The dialog taking focus, with its title and body read on that focus event, **is** the announcement. And the in-dialog alert is now keyed on an attempt counter, because `role="alert"` fires on insertion and a second identical failure was silent.

**The refusal copy was split in two.** The original ended with *"Send acknowledgeEarningsBelowPaid to do it anyway"* — an API contract note rendered to an owner who cannot act on it. `message` is what a person reads; `error` keeps the developer sentence.

**The typed phrase is `below 46.83`, not a bare amount.** The already-paid figure is the one number in this flow the owner has not typed and cannot derive, so it can only come from reading the comparison — and the word prefix stops it becoming the same motor action as the Void dialog on the same page, which also asks for a bare dollar amount.

**Two sibling defects fixed because they are the immediate neighbour.** Both over-earned chips rendered a literal `U+26A0`, which is `Extended_Pictographic=Yes` — an emoji by Unicode property, breaking two house rules, and NVDA at default verbosity often announces **nothing** for it. And each hid its only explanation in a `title` on a non-focusable `<p>`: unreachable by keyboard, unreachable by touch, usually unannounced — the exact pattern a comment four lines above already rejected. Both now lead with the verb, because `--text-primary`, `--text-secondary` and `--text-muted` are **all `#ffffff`** and the amber sits **1.13:1** from the emerald bonus figure directly above it, so for a red-green colour-deficient owner the warning and the good news were the same colour.

**Reported, NOT fixed:** the insufficient-balance warning is now accurate but still sits in column 3 of 10 behind two `overflow-x-auto` containers with no header tally and no filter, so a rarely-firing warning is nearly invisible — a header chip plus a filter is its own round. `--bg-page` is used 41 times across `src/` and **defined nowhere**, which silently kills focus rings that offset against it. Fixing `Modal` itself is a 37-surface blast radius that does not belong in a money round.

---

## GATES, HONESTLY

* **eslint confirmed present**, `v9.39.4`, so the hooks gate is a real check and not a silent no-op.
* `npx tsc --noEmit` exit **0**, `grep -c "error TS"` = **0**, run ten times across the round, the first on the **untouched** worktree so no error could be misattributed.
* `npm run build` **three times**, each written to a log with the exit code echoed by hand and **never piped through `tail`**: **`BUILD1_EXIT=0`**, **`BUILD2_EXIT=0`**, **`BUILD3_EXIT=0`** (the last post-commit). Prebuild clean every time: `check:prisma-bypass` **0 violations**, `check:removed-fields` **OK**, hooks gate **11 problems (0 errors, 11 warnings)** — at the ceiling with **zero added**.
* `scripts/bl827-verify.ts`: **34 passed, 0 failed**, and demonstrated failing three separate ways.
* Counted with `grep -c` and explicit `count(*)`, **never piped through `head`**. One shell at a time.
* **Zero Supabase pool errors** across both dev-server runs (`grep -ci "Too many database connections"` = 0 on each log). Each server was stopped between phases.
* **A document is not a code change**: the real diff is 7 source files, 447 insertions, verified non-empty by `git diff --stat` before anything was claimed.

---

## WHAT COULD NOT BE PROVEN, AND WHAT I GOT WRONG

* **I told the owner keeping the cut would leave the clipper able to claim `$0.00`. The true figure is `$7.59`.** BL-824 bounds paid money per campaign, so the cut does not reach his Zhus Meme balance. The decision is unaffected; the figure I gave was wrong and is corrected here.
* **Whether the `$11.00` has actually left the owner's wallet is unknown from here.** The platform now records the payment. If the funds have not been sent, they must be.
* **Nothing was verified against production over HTTP.** Every request ran locally against the merged tree, pointed at the production database.
* **A real screen reader was not run.** DOM order, roles, focus behaviour and the phrase gate are measured; NVDA, JAWS and VoiceOver were not.
* **The reminder engine was not fixed** and has still never fired, on any of the 192 payout rows.
* **`notifyPayoutAdjusted` has never fired for anyone**, so no clipper has ever been told their earnings were reduced by an adjustment. Reported, not fixed.
