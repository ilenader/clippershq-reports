# BL-861 — two payout controls, and neither of them touches a clip

**NOTHING IS UNREMOVABLE. 338 sandbox rows were created and 338 were deleted by primary key; 0 of 338 remain, verified by re-reading every row and again by a direct `LIKE 'bl861sbx-%'` sweep of `users`, `payout_requests`, `clips` and `campaigns` that returns 0, 0, 0, 0. No SQL is owed and none is offered. NO REAL PAYOUT WAS TOUCHED: zero real rows are settled and zero are priced on the live platform right now.**

**2026-09-09 · DB `now()` = `2026-09-09 08:49:44.269091+00` (first read) to `2026-09-09 09:41:46.48544+00` (last) · BUILD, PROVE, RENDER AND MERGE.**
Base `origin/main` @ `3b3c48cc`. Branch `checkpoint/BL-861` @ `a1ec2dae`. **Merged and verified pushed: `origin/main == local == a527de2d`.** Tags `pre-BL-861`, `post-BL-861`, `pre-BL-861-merge`, `post-BL-861-merge`, all on origin. Isolated worktree `C:/w861`, a short path, `node_modules` never junctioned, **removed at the end and verified gone by listing the path**. Every read through `scripts/run-select.js`, every timestamp cast `::text` against DB `now()`. Handles redacted, **no wallet address read or printed**.

**A REDEPLOY ON RAILWAY IS REQUIRED BEFORE ANY OF THIS IS LIVE.** Both controls are new routes and new UI; until the deploy runs, the owner's screen is exactly as it was.

**Collision with BL-860.** `checkpoint/BL-860` exists on origin at `fece1fe0` and is **NOT an ancestor of main**. It is a report-only branch: its entire diff against main is `reports/BL-860-clippershq-health-and-launch.md` plus BL-859 files it predates. **It touches nothing this round touches** — no payout route, no payout surface, no money file. `git worktree list` showed one tree at the start and this round worked in its own at `C:/w861`, so no shared-tree collision was possible. `checkpoint/BL-723` confirmed **NOT an ancestor of main**.

---

## THE ANSWER, BEFORE THE WORKING

> **A VOID STATE ALREADY EXISTS AND CANNOT DO EITHER JOB, AND THAT IS PART 0's REAL FINDING.** `VOIDED` is in the enum (`schema.prisma:1315`) and is reachable from `PAID` and nowhere else (`review/route.ts:72-77`). On the way, `review/route.ts:404-406` backfills `paidAt`, so `isPayoutMoneyOut` (`balance.ts:117-124`) returns true and **every reachable void counts as money out**. Voiding an unpaid request would therefore record a payment that never happened. Skip the backfill instead and `VOIDED` is in neither `LOCKED_PAYOUT_STATUSES` nor `isPayoutMoneyOut`, so the money is released and the request reappears. **Neither is the owner's outcome.** Measured: 31 VOIDED rows exist, **all 31 carry `paidAt = NULL`**, every one written by the campaign-archive cascade BL-732 caught and BL-733 deleted.
>
> **A NEW STATUS VALUE WOULD HAVE BEEN WORSE, not better.** Any new enum value sits outside `LOCKED_PAYOUT_STATUSES` and outside the partial unique index, so on day one it would have released the money and let the request reappear — the exact failure the owner asked to be rid of. Fixing that needs `balance.ts`, which is a money file.
>
> **SO THE ANSWER IS A STAMP ON AN OPEN ROW, AND IT NEEDED NOT ONE LINE OF ANY MONEY FILE.**
>
> **THE CLAIM IS EXTINGUISHED, NOT RETURNED, AND I AM SAYING SO PLAINLY.** The clipper does not get this money back. That is the whole difference from reject. **But nothing is destroyed:** `Clip.earnings` is never read or written by any settle path, so BL-538's never-decrease rule and BL-824's paid-is-final rule are *arithmetically out of reach* rather than merely respected, and Reopen releases the claim in full. The claim is **held closed, not annihilated**. An owner who closes the wrong row loses the seconds it takes to press Reopen.
>
> **PART 2 IS A PRICE ON THE PAYOUT ROW AND NEVER A REWRITE OF THE CLIPS**, which is BL-834's and BL-835's settled shape applied to the owner's own cut. **BL-826's jam cannot recur and it is proven on BL-826's exact shape**: 40 clips carrying $140.54, $78.54 already paid, a $60.27 request priced to $11.00. All 40 clips byte-identical afterwards, **Mark Paid returns 200**, and zero retry-exhausted rows where the original accumulated five.
>
> **THE GUARD WAS WATCHED FAILING.** Broken: 2 passed, **3 FAILED, exit 1**, with the closed request PAID at $40.00 and `paidAt` stamped. **The demo also caught itself being wrong** about one of its own assertions, and the label now says what was measured rather than what was predicted.
>
> **THE DAY-ONE COUNT IS ZERO AND THAT IS A FINDING, NOT AN OMISSION.** No real payout is closed and none is priced. Nothing changes for anybody at deploy; both controls are inert until the owner presses one.

---

## PART 0 — THE STATE MACHINE, MAPPED BEFORE ANYTHING WAS ADDED TO IT

### Every status, with file:line

`prisma/schema.prisma:1309-1316`:

```
1309  enum PayoutStatus {
1310    REQUESTED
1311    UNDER_REVIEW
1312    APPROVED
1313    PAID
1314    REJECTED
1315    VOIDED
1316  }
```

Column at `:1409`, `status PayoutStatus @default(REQUESTED)`.

### The transition table, and the three authorities that ignore it

`review/route.ts:72-77` (line numbers as they were on `origin/main` at `3b3c48cc`):

```ts
REQUESTED:    ["UNDER_REVIEW", "APPROVED", "REJECTED"],
UNDER_REVIEW: ["APPROVED", "REJECTED"],
APPROVED:     ["PAID", "REJECTED"],
PAID:         role === "OWNER" ? ["VOIDED"] : [],
```

`REJECTED` and `VOIDED` have no keys; both are terminal under this route.

| # | transition | who | file:line | money effect | audit | notified |
|---|---|---|---|---|---|---|
| 1 | REQUESTED → UNDER_REVIEW | OWNER | `review/route.ts:371` | none, both statuses lock the gross | `UNDER_REVIEW_PAYOUT` | **no arm** |
| 1b | REQUESTED → UNDER_REVIEW | OWNER/ADMIN, on booking a call | `api/calls/route.ts:276-280` | none | own row, `trigger: SCHEDULED_CALL_BOOKED` | no |
| 2 | REQUESTED/UNDER_REVIEW → APPROVED | OWNER | `review/route.ts:371` | none, still locked | `APPROVED_PAYOUT` | `PAYOUT_APPROVED` |
| 3 | REQUESTED/UNDER_REVIEW → APPROVED | OWNER, **via `adjust`, bypassing the table** | `adjust/route.ts:566-574` | **shrinks every funding clip by the ratio** | `PAYOUT_ADJUSTED` | `PAYOUT_ADJUSTED` (has never fired) |
| 4 | APPROVED → PAID | OWNER | `review/route.ts:371`, `paidAt` at `:389` | moves from `lockedInPayouts` to `paidOut`, bounded per campaign by `effectivePaidOut` | `PAID_PAYOUT` | `PAYOUT_PAID` + email |
| 5 | any open → REJECTED | OWNER | `review/route.ts:371` | **lock released, money returns** | `REJECTED_PAYOUT` | `PAYOUT_REJECTED` + email |
| 5b | any open → REJECTED | OWNER, **via `reject-botted`, a third authority** | `reject-botted/route.ts:331-339` | releases the lock **and rejects every clip** | `PAYOUT_REJECTED_BOTTED` | `CLIP_REJECTED` only |
| 6 | PAID → VOIDED | OWNER, reason mandatory | `review/route.ts:371`, `paidAt` backfill `:404-406` | **stays money out; balance does not move** | `FORCE_VOID_PAID_PAYOUT` | **NOTHING** |

### Does a void state already exist, and is it merely unreachable?

**It exists, it is reachable, and it is reachable only from `PAID`.** Two separate facts, and both matter.

**FACT ONE: the Void BUTTON has been rendered on REJECTED rows since BL-733 and has never once worked.** `admin/payouts/page.tsx` rendered it under `payout.status === "PAID" || payout.status === "REJECTED"`. `validTransitions` has no `REJECTED` key, so the lookup is `undefined` and `review/route.ts` returns **400 `Cannot change payout from REJECTED to VOIDED`**. Pressing it asked the owner to read a summary, type a dollar amount back, and then refused him. **This round removed that arm.**

**FACT TWO: its dialog promised the opposite of what void does.** The non-PAID body read *"The clipper keeps the money they earned; voiding only cancels this request, and their balance becomes available again so they can request it another time."* That describes the campaign-archive cascade, which BL-733 **deleted** (`campaigns/[id]/route.ts:998-1031` now counts and audits instead of writing). It described nothing reachable. **Removed with the button.**

**FACT THREE: the success toast said `"Payout voided. Balance recalculated."`** Nothing is recalculated and no balance moves — the dialog four inches above the button says so explicitly. **Now reads `"Payout voided. The record is cleared and no balance changed."`**

### Does the owner's first request need a NEW state? No, and a new state would have been actively wrong

Stated as arithmetic rather than opinion:

* **`LOCKED_PAYOUT_STATUSES` is `["REQUESTED","UNDER_REVIEW","APPROVED"]`** (`balance.ts:54`), and `lockedInPayouts` sums `clipperLiability` over exactly those (`balance.ts:311-313`).
* **`available = max(approvedEarnings − effectivePaidOut − lockedInPayouts, 0)`** (`balance.ts:320-321`).
* **`uq_payout_open_per_user_campaign`**, read live out of `pg_indexes`, is `UNIQUE ("userId","campaignId") WHERE status = ANY (ARRAY['REQUESTED','UNDER_REVIEW','APPROVED'])`.

A new status value is in **neither** list. So on the day it shipped the money would return to available, and the clipper could open a second request. **The feature would have failed at exactly the thing the owner asked for.**

Keeping the row in an open status delivers all three properties for free, and needs no money file:

| property | mechanism | why it holds |
|---|---|---|
| the money does not come back | `lockedInPayouts` at gross | the status is unchanged and still in the list |
| it does not reappear | app check `payouts/route.ts:695-716` **and** the DB partial unique index | both cover all three open statuses |
| the clipper is never told they were paid | `isPayoutMoneyOut` stays false | no `paidAt`, status not PAID or VOIDED |

---

## PART 1 — THE SETTLED OUTCOME

### What was built

Three nullable columns, applied through `scripts/run-schema-sql.js` with `ADD COLUMN IF NOT EXISTS`. **No `prisma migrate`. No index. No enum change.**

```
settledUnpaidAt      TIMESTAMP(3)
settledUnpaidById    TEXT
settledUnpaidReason  TEXT
```

`POST /api/admin/payouts/[id]/settle` — `{ reason }` closes, `{ reopen: true }` reopens. Owner only, rate limited, Serializable with every decisive condition re-read inside the snapshot.

### The balance: EXTINGUISHED. Both consequences, laid out

**IF IT RETURNED (what reject does today).** The clipper sees the money back in "Available to withdraw" and requests it again; the owner refuses again; nothing is ever settled. Worse than the loop: the platform would be **displaying a withdrawable figure it has already decided it will never pay**. A balance that can never be drawn is a more dishonest thing to show somebody than a closed request.

**IF IT IS EXTINGUISHED.** The clipper loses a claim on money their clips genuinely earned. **That is a real loss and it is not dressed up as anything else.**

**RECOMMENDED AND BUILT: EXTINGUISHED**, because the owner's stated case is that the budget is spent, and because a false balance is the worse of the two lies. **But built so it cannot destroy anything:**

* `Clip.earnings` is **never read and never written** by any settle path. Asserted structurally in the suite: a grep of both new route files for `clip.update`, `writeClipEarnings`, `clip.updateMany`, `agencyEarning` and `marketplaceCreatorEarning` returns **zero matches**.
* **Explicit**: a typed confirmation, and a reason is mandatory.
* **Audited**: `PAYOUT_SETTLED_UNPAID` and `PAYOUT_SETTLE_UNPAID_REOPENED`, written **before** the notification so a message failure cannot take the forensic record with it. Each records `statusUnchanged`, so a reader of the audit trail alone can see the status was deliberately left where it was.
* **Reversible**: Reopen clears the stamp and releases the claim in full. Proven: close, then reopen, then assert the clipper's clip fingerprint is byte-identical to before the round trip.

### Closing clears any price, and that is a money decision worth naming

`clipperLiability` is `actualPaidAmount ?? amount` (`balance.ts:126-132`). A $30 request priced at $5 and then closed would have locked **$5**, handing **$25 straight back** to the clipper's available balance. The request would be closed and most of its money would have returned — precisely the outcome the control exists to prevent. **So closing clears the price and the full requested gross stays held**, and the cleared figure goes into the audit row.

### The exact copy the clipper reads

Badge: **`Closed, not paid`**. The second half is there because "Closed" beside a large dollar figure can be read as "closed because it was paid", which is the one thing this state must never be mistaken for.

Amount label: **`You asked for`**, over the **GROSS**. The accessibility review suggested reusing the existing "Would have received"; this deliberately does not, because that label names the *cash* while the figure held out of the balance is the *gross*, and the sentence below says "this request still holds that amount". The number printed and the number held have to be the same one.

> **This request is closed. No money will be sent for it. Your clip earnings have not changed. This request still holds that amount, so it does not show in Available to withdraw.**
>
> **Reason:** *(the owner's own words, verbatim)*
>
> **If you think this is wrong, ask the team in our Discord.**

**The third sentence is the one most versions of this would leave out and it is the one that must be there.** Without it the clipper reads that their earnings are unchanged, looks at the hero four inches above, finds the money missing, and has been told two things that cannot both be true. Both **are** true, and the missing link is that the closed request is still holding it. "Available to withdraw" is quoted verbatim from the hero caption on the same screen, so the claim is checkable without leaving the page.

**No sentence has the person as its subject.** Nobody is told they did anything. No verdict word appears. Longest sentence: 15 words.

**One reason field, shown to both.** The owner's dialog labels it *"Why is it closed? The clipper reads exactly what you write here."* There is no private half that can leak later. This follows the REJECTED precedent, where `rejectionReason` is already rendered to the clipper verbatim.

### It does not reappear, guaranteed at two layers and measured

```
clipper requests the same campaign again, immediately after being closed
  -> 409  "You already have a pending payout for this campaign."
  open payouts for that (clipper, campaign) = 1
```

Application layer `payouts/route.ts:695-716`, database layer `uq_payout_open_per_user_campaign`. Neither is new; both work because the row keeps an open status.

### A closed request is inert. Every route that could move it now refuses it

Four routes can move a payout, and **all four** were closed off. Measured, each a real HTTP request:

```
review  APPROVED      -> 409 PAYOUT_SETTLED_UNPAID
review  PAID          -> 409 PAYOUT_SETTLED_UNPAID
review  REJECTED      -> 409 PAYOUT_SETTLED_UNPAID
review  UNDER_REVIEW  -> 409 PAYOUT_SETTLED_UNPAID
price                 -> 409 PAYOUT_SETTLED_UNPAID
settle (again)        -> 409 ALREADY_SETTLED
adjust                -> 409 PAYOUT_SETTLED_UNPAID
reject-botted         -> 409 PAYOUT_SETTLED_UNPAID
```

The last two matter most. `adjust` and `reject-botted` each write status **without consulting the transition table**, and each also writes `Clip.earnings`. Without their guards, a closed request's clips could have been cut or rejected behind a decision the owner had already finished with.

**THE REVIEW GUARD SITS AHEAD OF THE TRANSITION TABLE, AND THE SANDBOX IS WHY.** The first run caught PAID on a closed REQUESTED row being refused by the table instead, with *"Cannot change payout from REQUESTED to PAID"*. True, and useless: the owner's real obstacle is the closure he made, and whether he also picked an action the table would have refused anyway is not the interesting fact about that row. **The guard that names the real reason, and the way back, goes first.**

### The clipper is told, and no closure of any kind has ever done that

`PAYOUT_CLOSED` and `PAYOUT_REOPENED`. `Notification.type` is a free-form String column, so no migration.

**BL-763 ranked this FIRST among its fixes and it has never been built.** `review/route.ts` has arms for APPROVED, REJECTED and PAID and **no arm for VOIDED**, so when the archive cascade silently voided two clippers' payouts the platform told neither of them anything. BL-763's own sentence about the six days that followed is *"The only reason six days have passed is that nobody ever told them."*

**A BANNED CLIPPER IS STILL NOT TOLD, AND THAT IS REPORTED RATHER THAN HIDDEN.** `createNotification` (`notifications.ts:540-543`) skips banned users outright, on the stated grounds that they cannot open the app to read one. Asserted in the suite as its own check with the reason named. **Not changed:** widening that gate is a policy decision about every notification type on the platform, not a payout decision.

**This is the round's own correction to itself.** The first suite run used a BANNED account for the closure path and the two notification checks failed. That was the **suite** being wrong, not the feature. The fixture now closes an ACTIVE clipper's request, and the banned case is asserted separately.

---

## PART 2 — ADJUST WITHOUT PAYING, AND RE-ADJUST FREELY

### It is a stamped price on the payout row. Nothing else

`POST /api/admin/payouts/[id]/price` writes `actualPaidAmount`, `priceSetAt`, `priceSetById`, `priceSetReason`, and **stops**.

> **NO** clip is written. **NO** `AgencyEarning`, `MarketplaceCreatorEarning` or `MarketplacePlatformEarning` is written. **NO** `PayoutAdjustment` row is created. **NO** status is changed. **NO** notification is sent. **NO** money moves.

**Because it creates nothing unique, it repeats.** The adjust route cannot: `PayoutAdjustment.payoutRequestId` is `@unique` (`schema.prisma:1459`) and the model's own comment says *"Unique on payoutRequestId so applying twice is impossible."* Measured, three prices on one row:

```
$20.00 gross -> cash $18.20   200   previousGross null
$12.50 gross -> cash ...      200   previousGross 20
$5.00  gross -> cash ...      200   previousGross 12.5
status after three prices: REQUESTED, unchanged
amount after three prices:  $30.00, unchanged
clip fingerprint:           IDENTICAL to before the first price
payout_adjustments rows:    0
PAYOUT_PRICE_SET audit rows: 3
```

### Why `actualPaidAmount` and not a new column

Costed and rejected. A new `adjustedAmount` would have to be preferred by `clipperLiability` and `campaignBudgetLiability` — **both in `balance.ts`, a money file** — plus `payoutLiabilityWithTrainerCut`, `mintableTrainerCutAmount`, the BL-827 `ownerSetAmount` gate skip, `tax-1099.ts`, and roughly **twenty separate Prisma `select` sites**. A missed select is invisible: the field reads `undefined`, falls through to `amount`, and **silently reverses the adjustment on that one surface**. `actualPaidAmount` is already the stamped price, already authoritative in every chain, and already made final at mark-paid by BL-827. **Reusing it costs zero money-file changes.**

The consequence is that the column now has **two producers**, and the schema comment that said *"When set, a PayoutAdjustment row exists"* was true only while `adjust` was the only writer. It is corrected in place: **the test for "were this payout's clip earnings cut?" is the `PayoutAdjustment` row, never the presence of `actualPaidAmount`.**

### THE JAM CANNOT RECUR — BL-826's exact scenario, reproduced

Rebuilt to the cent: **40 clips carrying $140.54**, a **$78.54 PAID** payout already against them on the same campaign, an open request for **$60.27** priced down to **$11.00**.

```
40 clips carrying $140.40, against $78.54 already PAID on the same campaign
price to $11.00                                        200
ALL 40 CLIPS BYTE-IDENTICAL. Nothing multiplied by 0.1825
recorded earnings $140.40 against $78.54 paid          never falls below
approve                                                200
MARK PAID                                              200   <-- BL-826 got 503, five times
paid row: status PAID, amount $60.27 (> 0), actualPaidAmount $11.00
PAYOUT_REVIEW_RETRY_EXHAUSTED rows for this payout:    0     <-- BL-826 accumulated 5
payout_amount_positive still defined in pg_constraint: 1
```

**Three independent reasons it cannot come back**, any one sufficient:

1. No clip is written, so no `payoutReductionRatio` is ever stamped, so the BL-18 stale-reduction branch has nothing to find.
2. BL-827's `ownerSetAmount` skip sees the price and bypasses the campaign balance gate, so the auto-adjust is never reached.
3. **`amount` is never rewritten**, so `payout_amount_positive` is never approached. **The constraint was not dropped and not weakened.**

### GROSS OR CASH, and what the clipper actually receives

**`actualPaidAmount` IS A GROSS FIGURE.** `adjust/route.ts:1-3` says so in its first sentence and `clipperLiability` substitutes it directly for `amount`, which is the gross column. The adjust route never recomputes `feeAmount`, `expressFeeAmount` or `finalAmount`, and neither does this one, so **the cash the clipper receives lives in no stored column**.

It is derived once, through `calculatePayoutBreakdown` — the same helper that produced the row:

```
cash = A − round2(A × feePercent/100) − round2(A × expressPercent/100) − min(scaledTrainerCut, room)
```

`feePercent` is per row (9, or **4** for a referred clipper), the express premium exists only on EXPRESS rows, and the trainer cut is a **fourth** term. The accessibility review refused a hand-computed figure outright and three specialists independently confirmed why. **BL-760 caught a $5.44 near-overpayment and BL-763 a $7.80 one from exactly this confusion, and BL-827 found four live surfaces printing the gross under the words "You received".**

The route's response returns `cash` beside `gross`, the dialog shows both, and **the typed confirmation phrase is the CASH** — see below.

### The audit row on every change

`PAYOUT_PRICE_SET` (and `PAYOUT_PRICE_CLEARED`), carrying `requestedGross`, `previousGross`, `newGross`, `cashAfter`, `reason`, `statusUnchanged` and an ISO timestamp; the row's `createdAt` was read back cast `::text` beside DB `now()`. **BL-732 is why it is not optional and why it is written first**: a status change once voided two payouts, took $82.13 from two clippers, wrote no audit row and no notification, and went unnoticed for three days.

**Exactly one audit row per ACCEPTED price, proven under contention.** Two owner sessions pricing the same row simultaneously produced one 200 and one refusal, one stored figure, and **one** audit row. A refused attempt writes nothing at all, which is what makes the trail a record of what happened rather than of what was tried.

### A P2034 retry was added because the sandbox asked for it

The first concurrency run returned 200/409: one committed, the other lost the Serializable race and was refused outright. Safe, and worse than it needed to be, because `review` and `adjust` both retry that condition. The price route now retries it three times with the same backoff, re-reading every condition inside each new snapshot.

---

## PART 3 — WHAT THE CLIPPER SEES WHILE IT IS PRICED BUT UNPAID

### The decision: THEY SEE IT IMMEDIATELY. Justified

**Hiding it is the worse lie.** The moment the owner stamps a figure, `clipperLiability` reads it, so **the clipper's available balance has already moved**. Showing the old figure on the payout card while the balance reflects the new one is exactly the two-bases contradiction BL-822 found between the gate and the display, and BL-813 found across four surfaces. Showing a number that changes three times is a real cost; showing a card that contradicts the balance on the same page is BL-822 again.

So the figure is shown the moment it is set, and **the sentence says plainly that it is not final**:

> **You asked for $757.20. The owner set this payout to $264.00, and fees come off that. Nothing has been sent yet. Your clip earnings have not changed. The rest of your request is no longer held for this payout.**
>
> **Reason:** *(the owner's words, if he gave any)*

**The last sentence is deliberately NOT "is back in Available to withdraw"**, a correction from the accessibility review that matters: `available` is floored at zero (`balance.ts:321`) and is reduced by everything else in flight, so for some clippers the released difference will not appear there at all and the stronger sentence would be **false for them**. "No longer held for this payout" is true for every clipper without exception.

### A LIVE DEFECT THIS ROUND WOULD HAVE TRIGGERED, CAUGHT BEFORE IT SHIPPED

`PayoutsRedesign.tsx:199-201` chose the words **"You received"** whenever `actualPaidAmount` was non-null:

```ts
payout.actualPaidAmount != null ? "You received" : ...
```

That was safe while the **only** producer of that column was the adjust route, which flips the row toward payment on its way. **This round's price control writes the same column with nothing sent.** A clipper whose request the owner had merely priced would have read **"You received $264.00"** about money still in the owner's wallet. That is the fifth round of this same confusion after BL-760, BL-763, BL-812 and BL-827 — **and the first one caught before it reached anybody.**

The test for "was this paid" is now the payment and nothing else (`payoutWasActuallyPaid`: `status === "PAID" || paidAt != null`). BL-813's rule that the label derives from the FIELD first is preserved exactly, and the 10 legacy rows with a null `finalAmount` still read "Requested".

### Nothing on the clipper's screen contradicts anything else

Three further contradictions were found and closed on the same surface:

| what it said | why it was wrong | now |
|---|---|---|
| badge **"Approved"**, icon `Send`, label **"You will receive"** on a closed row | closing leaves the status alone by design, so the card read the status and promised money the platform had decided never to send | the closure is read **first** and overrides badge, icon, label and explanation |
| hero **"$757.20 in queue"** under a `Clock` | `lockedInPayouts` counts closed rows, so money queued for nothing was called a queue | split into `… in queue` and a separate `… held by a closed request` line with a `Ban` icon, because both halves are true and the clipper needs both |
| the no-balance sentence *"If that looks wrong, open a support ticket in our Discord"* | **this is BL-762's defect verbatim** — the exact sentence that sent a real clipper to support for an answer the screen already had | a closed-request branch names the figure and points at the card below |

The verification-call control is also removed from a closed card: it would have written a real `ScheduledCall` row for a payment that will never happen. **Removed rather than disabled**, because a disabled control still tells somebody the option exists.

---

## PART 4 — THE INVARIANTS, PROVEN ACROSS THE FULL POPULATION

Measured platform-wide, not only on the rows this round touched.

```
BL-538, the earnings invariant, clips violating earnings = base + bonus      0
BL-627, no overpayment, clips carrying negative earnings                     0
                        payout rows with amount <= 0                         0
BL-696, no double pay,  duplicate open (user, campaign) pairs                0
closed rows outside REQUESTED / UNDER_REVIEW / APPROVED                      0
closed rows still carrying a price                                           0
closed rows marked paid                                                      0
sandbox (clipper, campaign) pairs whose record sits below money paid         0
```

**BL-824 paid-is-final, and BL-849's write side.** Both hold structurally rather than by discipline: neither new route contains a clip write of any kind, asserted by extracting the source of both files and matching for `clip.update`, `writeClipEarnings`, `clip.updateMany`, `agencyEarning` and `marketplaceCreatorEarning` — **zero matches**. `effectivePaidOut` and the marketplace floor are untouched and unreachable from here.

**The rule that recorded earnings may never fall below money already paid.** Across the whole platform there are pairs in that state today — the historical population BL-716, BL-823 and BL-824 documented and BL-827 knowingly added one to. **Not one of them was created by this round**, and it is arithmetically impossible for either control to create one, because neither reads or writes `Clip.earnings`.

**The two lists that must never drift.** `OPEN_PAYOUT_STATUSES` in the new shared module is asserted **identical to `LOCKED_PAYOUT_STATUSES` extracted from `balance.ts` source**, and the live `uq_payout_open_per_user_campaign` definition is read out of `pg_indexes` and asserted to cover exactly those three. `balance.ts` is a money file, is never imported by the new module, and the suite checks the two agree rather than trusting a comment.

### THE GUARD, DEMONSTRATED FAILING

`scripts/sandbox/bl861-guard-demo.ts`. The property: **a closed request cannot be paid.** The fixture takes the row to APPROVED first, so the transition table would happily allow PAID and the guard is the only thing in the way.

```
MODE=intact     5 passed, 0 failed   exit 0
MODE=broken     2 passed, 3 FAILED   exit 1
MODE=restored   5 passed, 0 failed   exit 0

review/route.ts blob OID before: 67cf3da2b14bf787ba13bd06e80c15ef1d1da981
review/route.ts blob OID after:  67cf3da2b14bf787ba13bd06e80c15ef1d1da981   IDENTICAL
```

**Both halves of the guard were disabled**, the pre-transaction refusal and the re-read inside the Serializable snapshot, because removing only one would have left the other carrying the property. The broken run printed the figures:

```
FAIL  Mark Paid on a CLOSED request is refused
      status=200 code=(none)
FAIL  the closed request is STILL NOT PAID
      status=PAID paidAt=2026-09-09 09:24:50.926 amount=$40
      WITH THE GUARD REMOVED THIS ROW IS PAID: $40 leaves for a request the owner
      closed, and the clipper is sent a PAYOUT_PAID notification for it.
```

**THE NEGATIVE CASE, so the guard is shown not to over-fire:** an ordinary open request is still approved and paid normally with the guard in place. A guard that refused everything would pass the first case and be useless.

**THE ISOLATION ASSERTION, AND THE DEMO'S CORRECTION OF ITSELF.** Two candidates were labelled as belonging to other invariants. **The broken run decided between them and one label was wrong.**

* *"the clipper still cannot open a second request"* was written claiming it would pass in the broken run. **It failed**, at `open rows = 0`, because paying the closed request moved it out of the open statuses altogether. It is **not** independent of this guard, and the label now says so.
* *"no clip was touched by any of it"* **passed in the broken run** while two others failed. That is the real isolation assertion: it is carried by the structure of both controls, not by this guard.

Both labels now state what was measured rather than what was predicted. **An assertion nobody has watched fail cannot be classified by reading it, which is the entire reason BL-1530 requires the broken run.**

---

## PART 5 — EVERY FAILURE PATH, IN THE SANDBOX

`scripts/sandbox/bl861-prove.ts` under `SANDBOX_ROUND=bl861`: same ledger, same four locks, same destroyer, its own prefix and its own confirmation variable. **71 checks, 0 failed.** Every one a real HTTP request against a **production build** on port 3861 with `DEV_AUTH_BYPASS=false` and real minted Auth.js cookies. `refusal.ts` ran first: **21 passed, 0 failed.**

| the brief's case | result |
|---|---|
| adjust, then adjust again, then pay | three prices then PAID, all 200 |
| adjust to zero | **400 `PRICE_WOULD_BE_UNPAYABLE`** |
| adjust above the requested amount | **400 `PRICE_ABOVE_REQUEST`** |
| a negative amount | **400** |
| adjust a payout already paid | **400 `PAYOUT_NOT_OPEN`** |
| adjust one already settled | **409 `PAYOUT_SETTLED_UNPAID`** |
| settle one already paid | **400 `PAYOUT_NOT_OPEN`**, paid is final |
| settle one already rejected | **400 `PAYOUT_NOT_OPEN`** |
| settle with no reason | **400 `SETTLE_REASON_REQUIRED`** |
| a banned payee | approve **409 `PAYEE_NOT_IN_GOOD_STANDING`** (BL-849's gate intact); price and close both **200**, deliberately |
| a clipper who requests again immediately after being settled | **409**, one open row remains |
| two owners at once, pricing | one 200 one refusal, one stored figure, one audit row |
| two owners at once, closing | **exactly one closure** |
| BL-826's exact 40-clip scenario | **Mark Paid 200**, 40 clips byte-identical, 0 retry-exhausted rows |
| a CLIPPER trying either control | **403** on both |

**Why a banned payee CAN be priced and closed, stated rather than buried.** Pricing moves no money and changes no status; closing pays nobody. The payment itself is still stopped by BL-849's gate. Refusing here would block bookkeeping without protecting anything.

### The ledger, the teardown, and the census

```
338 rows recorded in C:/bl861-sandbox/ledger.jsonl
  payout_requests   32      clips           152      clip_accounts  22
  notifications     35      audit_logs       55      campaigns      12
  users             30
338 deleted, 0 already gone, 0 FAILED
VERIFIED: 0 of 338 recorded rows remain.
```

**Product-written rows were ADOPTED, never pattern-matched.** `bl861-adopt.ts` records each notification and audit row with the **column** that identifies its owner and the sandbox id that column must hold; the destroyer re-reads the row and refuses unless the database itself confirms it. **35 notifications and 55 audit rows** adopted this way. `audit_logs_userId_fkey` was verified `confdeltype = n` (SET NULL) **before any user was deleted**, because with CASCADE the round would have erased the evidence of its own actions.

**`verify-gone.ts`: 50 checks, 50 passed, 0 failed.** All three real fingerprints byte-identical:

```
real payout fingerprint   562d83eda6a97f2430c6db00a18be809  ->  identical
real user fingerprint     1cf3365721752817b4d5bb804f1dc3f4  ->  identical
real clip status f/print  2fac92f63f1c29bb876142e51eadf04a  ->  identical
earnings invariant violations   0  ->  0
```

**Counts that moved are attributed, not excused.** `clips 9782 → 9785`, `clip_stats 358320 → 358340`, `tracking_jobs 9743 → 9746`, `approved_earnings 14130.72 → 14130.89`. The tool's own census of the window: **3 clips submitted by 3 real clippers, 20 view snapshots written by the cron, 0 real signups, 0 payouts created.** That is live traffic during a 27-minute window and none of it is the sandbox. A final direct sweep confirms it: `LIKE 'bl861sbx-%'` returns **0 users, 0 payouts, 0 clips, 0 campaigns**.

**No Apify actor was run**, the 11 BL-678 guards are untouched, and every sandbox campaign carried every CPM column set so the null-CPM branch that notifies every real owner could not fire. **Zero Supabase pool errors**; the server was stopped before teardown.

---

## PART 6 — RENDER, AND THE MERGE

### 30 shots, 290 assertions, 290 passed, 0 failed

BL-793's method unchanged: the viewport set on the **context**, `window.innerWidth` read back and printed beside every shot, horizontal overflow measured on every shot, real minted cookies against a production build with the dev bypass off, and the splash lifting asserted as the postcondition for "the screen is on screen".

```
owner-row        320 375 414 1280 1440
close-stage      320 375 414 1280 1440
close-confirm    320 375 414 1280 1440
price-stage      320 375 414 1280 1440
price-confirm    320 375 414 1280 1440
clipper-states   320 375 414 1280 1440

0 at the wrong width, 0 with horizontal overflow, splash lifted on all 30
```

**The confirmations are photographed from the REAL dialogs, not mocks.** The render opens both staging modals, fills them, and advances to the typed-phrase step. **It never presses a confirmation.** `bl861-render-verify.ts` proves it afterwards against the fixture ids: the row whose Close dialog was opened and typed into is **still open and still unpriced**, the priced row's figure is untouched at $264.00, the closed row is still closed and still unpaid, and `payout_adjustments` is **9** platform-wide, unchanged from the opening snapshot.

**TWO RENDER FAILURES ON THE FIRST PASS, AND WHAT THEY WERE.** Reported rather than smoothed:

1. **The harness clicked a REAL payout row.** `getByRole("button").first()` landed on a real clipper's $25.09 request, because the admin table lists every payout on the platform and the sandbox rows sit below them. **Nothing was written** — opening a dialog and typing sends no request, and the confirmation was never pressed — and the refusal it produced was *correct* (`"That is more than the $25.09 they asked for. A payout can be priced down, never up."`). It should not have been reachable at all. Every click is now scoped to a row filtered by the sandbox clipper's username.
2. **A "no dash as a bullet" check matched a real table's empty cell** (`\t-\tfishy_40`), not any new copy. The assertions are now scoped to the open dialog's own text. **Loosening the dash rule would have been the wrong fix.**

### The confirmations, and the accessibility review that shaped them

**The review returned NO-SHIP with nine blockers before any UI was written, and every one changed the work.** Both confirmations are `ConfirmDestructive`, never the shared `Modal`: for OWNER the app layout puts a `transform` on the sidebar wrapper, which becomes the containing block for `position: fixed`, so a scrim inside the shared Modal **does not cover the page and the sidebar stays clickable**. That is 100 percent of this surface's users. `ConfirmDestructive` portals to `document.body` and has `role`, `aria-modal`, an accessible name, a focus trap and `data-no-swipe` already.

**Each control is two steps, and the split is the point.** The owner types in a **staging** dialog; the figure is then **frozen** into the confirmation, which reads only from there. BL-827 found the alternative failing: an acknowledgement given for $11.00 could be reused after the field was edited to $5.00, authorising a figure whose consequences had never been computed. Going back to edit **discards** the confirmation.

**The typed phrases, and why each is what it is:**

| control | phrase | why |
|---|---|---|
| close | **`close 320.50`** | a word prefix, because the Void dialog on the same page already asks for a bare dollar amount and two dialogs sharing a motor action is how a confirmation becomes muscle memory |
| reopen | **`reopen 320.50`** | `tone="neutral"`: it gives money back, so it is confirmed but not dressed as a destruction |
| price | **`pay 36.40`** | **the CASH, not the gross.** He typed the gross a moment ago, so retyping it proves nothing. The cash is the figure he has **not** typed and cannot derive in his head, so it can only come from reading the row above the input, and it is the number that actually lands in somebody's wallet |

**One live region, not two.** No toast beside an open dialog: sonner's region is `aria-live="polite"` at body level, so writing both puts two live mutations in one commit and a screen-reader user hears the same refusal twice in two wordings. **The void dialog was still doing that and is fixed.** Every error is keyed on an attempt counter (`errorSeq`), because `role="alert"` announces on **insertion** and a second identical failure is otherwise silent — the adjust dialog had this since BL-827; **the void dialog did not, and now does**.

**Colour carries nothing.** `--text-primary`, `--text-secondary` and `--text-muted` are **all `#ffffff`**, and emerald-400 against red-400 measures **1.44:1**, so a warning and good news are the same colour on this platform. Every consequence is in words. New code uses `--text-danger`, never the hardcoded `red-400`, which measures **2.77:1 in the light theme** that the navbar toggle makes reachable.

### The merge

| | |
|---|---|
| clean `tsc` baseline on the **untouched** worktree, before any edit | `npm ci` exit **0**, `npx prisma generate` exit **0** (before tsc, because `npm ci` wipes the client), `npx tsc --noEmit` exit **0**, `grep -c "error TS"` = **0** |
| branch | `checkpoint/BL-861` @ **`a1ec2dae`**, VERIFIED on origin by `safe-push` |
| merge commit | **`a527de2d`**, `origin/main` verified by `safe-push` |
| conflicts | **none.** Main never moved from `3b3c48cc`, and the **merged tree OID equals the branch tree OID exactly** (`5feb428c`), so the branch's green build IS the merge's build |
| BACKLOG | **186 sections before, 187 after**, `BL-861` once, **0 conflict markers**, counted with `grep -c` and **never piped through `head`** |
| **`checkpoint/BL-723`** | **confirmed NOT an ancestor of main** |
| worktree `C:/w861` | **removed, and verified gone by listing the path** (`No such file or directory`) |

---

## GATES, HONESTLY

* **eslint confirmed present**, `v9.39.4`, so the hooks gate is a real check and not a silent no-op.
* `npx tsc --noEmit` exit **0**, `grep -c "error TS"` = **0**, run six times, the first on the **untouched** worktree so no error could be misattributed.
* `npm run build` **five times**, each written to a log with the exit code **echoed by hand** and **never piped through `tail`**: `BUILD1_EXIT=0`, `BUILD2_EXIT=0`, `GD_BUILD_broken_EXIT=0`, `GD_BUILD_restored_EXIT=0`, `BUILD3_EXIT=0` (post-commit). Prebuild clean every time: `check:prisma-bypass` **0 violations**, `check:removed-fields` **OK**, `check:event-wiring` **0 problems**, hooks gate **10 problems (0 errors, 10 warnings)** — **one BELOW the 11 ceiling, with zero added**.
* **No heredocs.** One shell at a time. Counted with `grep -c` and explicit `count(*)`, never through `head`.
* **The 6 money files plus `tracking.ts` and `campaign-era.ts`, byte-identical BY BLOB OID on BOTH refs** (`origin/main` and `pre-BL-861`):

```
ac5be7de  clip-earnings-writer.ts     797e2098  earnings-calc.ts
81a683c1  balance.ts                  9563a4fc  tracking.ts
61cef393  clip-earnings-invariant-middleware.ts
ef5cdae7  money-decimal.ts            106e16ad  campaign-era.ts
```

* **Schema:** six additive nullable columns via `run-schema-sql.js` with `ADD COLUMN IF NOT EXISTS`; `prisma generate` only, **never `prisma migrate`**. Rollback SQL is printed in `scripts/migrations/BL-861-PAYOUT-CONTROLS.sql` and dropping the six columns returns every row to its pre-round behaviour, because no other column was written.
* **The day-one count is ZERO.** 0 real payouts closed, 0 real payouts priced, 0 real payouts touched in any way.

---

## WHAT I GOT WRONG, AND WHAT COULD NOT BE PROVEN

* **The guard demo predicted one of its own assertions would pass in the broken run. It failed.** The label is corrected against the measurement and the wrong prediction is kept in the file, because that is the useful part.
* **The first proof run used a BANNED clipper for the notification path and reported two failures.** The suite was wrong, not the feature; `createNotification` skips banned users by existing policy. Restructured, and the banned case is now its own asserted finding.
* **The first render pass reached a real payout row.** Nothing was written and the refusal was correct, but it should not have been reachable. Scoped.
* **A real screen reader was not run.** DOM order, roles, accessible names, focus behaviour, the phrase gates and the disabled-until-typed state are measured; NVDA, JAWS and VoiceOver were not.
* **Nothing was verified against production over HTTP.** Every request ran locally against the merged tree, pointed at the production database.
* **`--bg-page` was fixed at ONE site**, the money table's header on the payouts page. The other **41** sites are untouched, and `CLAUDE.md` and `docs/runbooks/domain-and-ui.md` both still list it as a canonical token. **The rulebook is generating the bug** and that is its own round.
* **The payout reminder engine has still never fired** for any of the platform's payout rows. Closed requests are now excluded from its candidate query, which is a guard against the day it is fixed rather than a repair of anything live.
* **`notifyPayoutAdjusted` has still never fired for anyone**, so no clipper has ever been told an adjustment reduced their earnings.
* **`api/calls/route.ts:277`** still moves a payout REQUESTED to UNDER_REVIEW without reading the closure. Harmless today, because both statuses hold the money identically and neither pays anybody. Reported.
* **Whether the owner will use either control** is not something a round can prove. Both are inert until he presses one.

---

## SAFETY

Worked in an isolated worktree at `C:/w861`, a short path, `node_modules` installed there and **never junctioned**, **removed at the end and verified gone by listing the path**. Every database read through `scripts/run-select.js`, which refuses every write keyword; every timestamp cast `::text` against DB `now()`. **No wallet address was read or printed**, and the sandbox used a synthetic address belonging to nobody that appears in no output. Handles are redacted; no real clipper is named anywhere above. **No real payout was created, modified, approved, rejected, priced, closed, voided, retried or paid.** The 6 money files plus `tracking.ts` and `campaign-era.ts` are byte-identical by blob OID on both refs. **No `prisma migrate`**, no index, no enum change; six additive nullable columns with printed rollback SQL. **No Apify actor run**; the 11 BL-678 guards untouched. Zero Supabase pool errors; the production server was stopped by PID on its own port, never by image name, and stopped before teardown. **338 sandbox rows created, 338 deleted, 0 remaining**, verified twice by two independent methods. No heredocs. One shell at a time. Counts with `grep -c`, never piped to `head`. No dashes as bullets, no emoji in any new copy.
