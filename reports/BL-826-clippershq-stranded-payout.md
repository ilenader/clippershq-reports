# BL-826 — the payout that cannot be completed, and the warning that caused it

**2026-08-24 · DB `now()` = `2026-08-24 17:52:31.811234+00` (first read) to `18:07:34.360498+00` (last) · AUDIT ONLY, READ ONLY.**
No code, data, schema, config or money changed. **No payout was created, modified, approved, rejected, voided, retried or paid. No balance was touched. Nothing was recalculated, restored or repaired.** Every figure comes from read-only `SELECT`s through `scripts/run-select.js`, which refuses every write keyword, with every timestamp cast `::text` against DB `now()`. Base `origin/main` @ `100e8483`, isolated worktree `C:/w826`, `node_modules` never junctioned, removed at exit.

**Redaction.** The reports repo is PUBLIC. The clipper is **Clipper M**, id prefix `cmsiyg70`, which the owner can map privately in admin. **No handle, email or wallet address appears anywhere below, not even partially.** Other clippers are 8-character id prefixes.

**A markdown-only round cannot change tsc or the build. No build was run and none is claimed.**

---

## THE ANSWER, BEFORE THE WORKING

> **The owner's CPM hypothesis is wrong, and it is provably wrong.** The campaign's rate has never changed. Its last edit was `2026-08-12 14:02:12.592`, four days BEFORE the request, and no CPM field appears in any change record. All 40 clips are stamped `0.5000`, which is the campaign's current and only clipper rate. Clips are frozen at their own stamp and do **not** recompute at a live rate.
>
> **What actually happened is that the owner adjusted the payout himself today.** At `2026-08-24 17:03:37.706` a **payout adjustment** cut this payout from `$60.27` to `$11.00`, and as a designed side effect multiplied all **40** contributing clips' earnings by **0.182512×** — permanently. His Zhus Edit earnings fell from **$140.54** to **$25.65** in that instant. The adjust succeeded. Every Mark Paid attempt since has failed.
>
> **The real error is not generic, not a timeout and not a refusal.** It is a Postgres CHECK constraint violation, recorded verbatim in the audit log five times: `new row for relation "payout_requests" violates check constraint "payout_amount_positive"`. The mark-paid path computes an auto-adjusted amount of **$0.00** and tries to write it into a column the database requires to be `> 0`. **Retrying can never succeed**, and the owner has retried five times.
>
> **And the thing that started it carries no information.** "Campaign balance may be insufficient" fires on **all nine** in-flight payouts on the platform right now, including seven where the clipper is nowhere near over-committed. Before the adjustment Clipper M had earned `$148.13`, been paid `$78.54` and had `$60.27` in flight — `$138.81` against `$148.13`, comfortably covered — and the row still said his balance may be insufficient.
>
> **What he genuinely earned, computed from nothing but his clips, their views and each clip's own stamped CPM: `$147.20`.** He has been paid `$78.54` gross / **`$71.47` cash**. The `$60.27` he requested is fully covered by his own work.
>
> ### SEND HIM `$52.44`.
>
> That is the cash figure: `$60.27` gross minus the `$5.42` platform fee minus the `$2.41` express premium. **Do not send `$60.27`** — that is gross and overpays by `$7.83`. **The payout adjustment has to be reversed first, and there is no route that reverses it.**

---

## PART 1 — THE REAL ERROR, NOT THE GENERIC ONE

### It did not have to be reproduced. The route records it.

`src/app/api/payouts/[id]/review/route.ts:313-327` writes an audit row on every retry-exhausted failure carrying the driver's own message. **Five of them exist for this payout**, so the actual error is in the database rather than only in a Railway log, and no request had to be fired to obtain it. Per the brief, **the action was not retried**.

```
audit_logs  PAYOUT_REVIEW_RETRY_EXHAUSTED  targetId cmsv1ifo7…
  2026-08-24 17:32:37.363   2026-08-24 17:32:41.567   2026-08-24 17:38:12.552
  2026-08-24 17:44:57.282   2026-08-24 17:50:25.587
  {"attemptedAction":"PAID",
   "errorMessage":"new row for relation \"payout_requests\" violates check constraint \"payout_amount_positive\"",
   "errorCode":null}
```

| | |
|---|---|
| status code the owner receives | **503** |
| error body | `{"error":"Payout review temporarily unavailable, please retry"}` |
| where that response is produced | **`src/app/api/payouts/[id]/review/route.ts:329`** |
| the server log line beside it | **`:313`** — `[PAYOUT-REVIEW] tx failed for payout <id>: new row for relation "payout_requests" violates check constraint "payout_amount_positive"` |
| the constraint | `CHECK ("amount" > 0)`, named `payout_amount_positive`, created by `scripts/migrations/F-DB-CHECK-CONSTRAINTS.sql:23` |
| the line that writes the violating value | **`src/app/api/payouts/[id]/review/route.ts:248`** |

### The full chain, with the arithmetic reproduced read-only

Inside the review transaction, for an APPROVED → PAID transition:

| # | file:line | what it computes | value for this payout |
|---|---|---|---|
| 1 | `review/route.ts:168` | `campaignEarned` — his APPROVED, not-deleted, not-unavailable clip earnings on this campaign | **$25.65** |
| 2 | `review/route.ts:186` | `campaignPaidAndLocked` — `payoutLiability` of his OTHER payouts on this campaign (`actualPaidAmount ?? finalAmount ?? amount`) | **$71.47** |
| 3 | `review/route.ts:187` | `campaignAvailable = max(25.65 − 71.47, 0)` | **$0.00** |
| 4 | `review/route.ts:189` | `existingLiability = payoutLiability(this payout)` = `actualPaidAmount` | **$11.00** |
| 5 | `review/route.ts:190` | the gate — `11.00 > 0.00` | **fires** |
| 6 | `review/route.ts:209-213` | looks for a snapshot clip with `payoutReductionRatio` set and `earningsFrozenAt > payout.createdAt` — the BL-18 "stale reduction" branch | **40 clips match** |
| 7 | `review/route.ts:228-231` | not `INSUFFICIENT_BALANCE`; instead auto-adjust `newAmount = campaignAvailable` | **$0.00** |
| 8 | `review/route.ts:248` | `...(autoAdjustRef.value !== null ? { amount: 0 } : {})` inside `tx.payoutRequest.update` | **writes `amount = 0`** |
| 9 | Postgres | `CHECK (amount > 0)` | **violation** |
| 10 | `review/route.ts:305-308` | retry only on `P2034`; this is not `P2034`, so it `break`s immediately | no retry |
| 11 | `review/route.ts:329` | **503 "temporarily unavailable, please retry"** | what the owner sees |

Reproduced independently, read-only, against the live database:

```
campaign_earned  25.65 | campaign_paid_and_locked  71.47 | existing_liability  11.00
campaign_available  0  | stale_clips_found  40 | gate_would_fire  true
```

### Which of the four it is

**None of them cleanly, and that is the point. It is a collision between an application rule and a database invariant.**

* **Not a timeout.** `errorCode` is `null`, not `P2028`, and the failure is instantaneous. BL-814's shape does not apply.
* **Not a genuine server error.** Nothing crashed, nothing was half-written, and the transaction rolled back cleanly. The payout is byte-for-byte as it was.
* **Not a legitimate refusal rendering badly either**, which is where it differs from BL-688. BL-688's throw was a deliberate control-flow refusal that the catch chain failed to recognise. Here the code is not refusing at all — **it is trying to proceed**, and the database stops it. The BL-18 branch at `:228` exists precisely to avoid refusing, and it walks straight into a constraint.
* **What it is: a permanent, deterministic failure wearing a transient message.** `503 … please retry` is wrong twice over, exactly as BL-688 described: it is factually false, and it invites a retry on a condition that can never change. Five retries are on the record.

**The 503 also swallows the reason.** The `INSUFFICIENT_BALANCE` branch at `:221` has a fully typed, explanatory 400 at `:297-301`. The auto-adjust branch that replaced it for stale-reduction cases has no such handler, so the one case with a specific cause is the one that reports nothing.

---

## PART 2 — THE OWNER'S CPM HYPOTHESIS, TESTED DIRECTLY

### The campaign's rate has never changed. Measured, not assumed.

| | |
|---|---|
| campaign | Zhus Edit (0.50 CPM), `cmsisj3d8…`, ACTIVE, not archived |
| pricing model | `CPM_SPLIT` |
| `clipperCpm` / `ownerCpm` | **0.5000** / 0.3197 |
| `cpmInstagramClipper` / `cpmTiktokClipper` | **0.5000** / **0.5000** |
| campaign row `updatedAt` | **`2026-08-12 14:02:12.475`** |
| the payout was requested | **`2026-08-16 00:01:46.711`** |

**The last change to this campaign predates the request by four days.** Its audit trail holds five `CAMPAIGN_FIELDS_CHANGED` rows, the newest at `2026-08-12 14:02:12.592`. The word "CPM" appears in them only inside the campaign's own **name** and in `pricingModel: CPM_SPLIT`; the `newCpms` field on the notification row is `null`. **No rate field appears in any change record.**

**And no per-clip override exists either.** BL-756's `cpmOverriddenAt` is `NULL` on all 68 of his clips. Every one of the 40 clips behind this payout is stamped `cpmAtSubmissionDecimal = 0.5000`, which is identical to the campaign's live rate. **There is no rate to have fallen from.**

### Do already-earned clips recompute at the live rate, or stay frozen at their stamp?

**Frozen at their own stamp, and the code is explicit about it.** Earnings resolve from `Clip.cpmAtSubmissionDecimal`, not from the campaign row, on every recompute path. **This is NOT a defect and there is nothing here to name.** The stamped rate and the live rate happen to be the same value, so the question could not have produced the loss in either direction.

### What DID reduce his earnings, to the second

```
clips.earningsFrozenReason (all 40, identical):
  "Payout adjustment 0.1825× (paid $11.00 of $60.27) on 2026-08-24"
clips.earningsFrozenAt  = 2026-08-24 17:03:37.706
clips.payoutReductionRatio = 0.182512

payout_adjustments  payoutRequestId cmsv1ifo7…
  requestedAmount 60.27 | paidAmount 11.00 | ratio 0.18251202920192466
  appliedAt 2026-08-24 17:03:43.183 | reason NULL

audit_logs  PAYOUT_ADJUSTED  2026-08-24 17:03:43.301
  {"requestedAmount":60.27,"actualPaidAmount":11,"ratio":0.18251202920192466,
   "clipsAffected":40,"reason":null}
```

`11.00 / 60.27 = 0.1825120292…` — the ratio is exactly the adjustment. `src/app/api/admin/payouts/[id]/adjust/route.ts:123` computes `ratio = actualPaidAmount / requestedAmount` and applies it to `clip.earnings`, `baseEarnings`, `bonusAmount` and the AgencyEarning row of every contributing clip.

**Reconstructed from the ratio: those 40 clips carried `$140.54` before `17:03:37` and `$25.65` after. `$114.89` of recorded earnings was removed in one action.**

### Is this a new instance of BL-716's shape?

**Yes, and it was created today.** BL-716's finding was a trim that pushed a clipper's recorded earnings BELOW money already paid, costing `$60.47` and needing a manual repair. Here:

| | Zhus Edit |
|---|---|
| paid gross to Clipper M | **$78.54** |
| recorded earnings before the adjustment | **$140.54** — comfortably above |
| recorded earnings after the adjustment | **$25.65** — **$52.89 BELOW the gross already paid**, and **$45.82 below the `$71.47` cash** |

**BL-824 encoded the rule for exactly this**, and it does not reach here. `effectivePaidOut` is imported by `computeBalance`, by the withdrawal gate in `payouts/route.ts:713`, and by `campaigns/[id]/min-payout-impact:185`. **`payouts/[id]/review/route.ts` imports only `payoutLiability` (`:8`) and never calls it.** The mark-paid path computes its own raw `campaignPaidAndLocked` at `:186`.

**Stated fairly: applying BL-824's rule here would not have saved this payout.** `effectivePaid = min(paidGross $78.54, payableEarnings $25.65) = $25.65`, so `campaignAvailable` would still be `max(25.65 − 25.65, 0) = $0.00`, `:248` would still write `0`, and the constraint would still refuse. **The gap is real and worth closing, but it is not the blocker.**

**Two things the adjustment did that are worth naming separately.**

1. **The reduction is permanent and compounding.** `applyPayoutReductionCap` (`src/lib/earnings-calc.ts:556-578`) is a **multiplier, not a ceiling**, and `tracking.ts:1925-1955` records that the old skip-on-frozen behaviour was deliberately removed so the cap "rides on top of the standard recompute path" unconditionally. **Every future view these 40 clips earn will also be paid at 18.25%**, forever, unless something reverses the ratio.
2. **There is no route that reverses it.** `src/app/api/admin/payouts/[id]/` contains exactly two routes, `adjust` and `preview-adjustment`. There is **no undo**, and `PayoutAdjustment.payoutRequestId` is UNIQUE so the same payout cannot be re-adjusted. The owner cannot correct this from any screen.

---

## PART 3 — EVERY NUMBER ON THE ROW, RECONCILED TO THE CENT

### The stored row

```
payout_requests  cmsv1ifo705wr0xqwn4r8c5to
  status APPROVED   amount 60.27   feePercent 9   feeAmount 5.42
  expressFeePercent 4   expressFeeAmount 2.41   finalAmount 52.44
  actualPaidAmount 11.0000   payoutSpeed EXPRESS   campaign Zhus Edit (0.50 CPM)
  createdAt  2026-08-16 00:01:46.711
  deadlineAt 2026-08-16 12:01:46.604      paidAt NULL
  reviewedAt 2026-08-24 17:03:43.213      updatedAt 2026-08-24 17:03:43.214
  remindersSentCount 0   lastReminderTierSent NULL   lastReminderSentAt NULL
  clipIdsSnapshot: 40 clips
```

### Each displayed figure, traced

| on screen | what it is | value | file:line |
|---|---|---|---|
| **$60.27 requested** | `payout_requests.amount`, the GROSS the clipper typed | 60.27 | `admin/payouts/page.tsx:1340` |
| **−$5.42 fee** | 9% platform fee. He is **not** referred (`referredById` NULL), so the rate is 9 not 4. `60.27 × 0.09 = 5.4243 → 5.42` | 5.42 | `page.tsx:1341`, computed `payout-calc.ts:61-83` |
| **−$2.41 express** | 4% express premium. `60.27 × 0.04 = 2.4108 → 2.41`. Rate literal at `payouts/route.ts:427` | 2.41 | `page.tsx:1343` |
| `finalAmount` | `60.27 − 5.42 − 2.41 = 52.44` — **the cash he was due** | 52.44 | `payout-calc.ts` |
| **Send $11.00** | `actualPaidAmount ?? finalAmount ?? amount`. `actualPaidAmount` is stored as `11.0000` by the adjustment | 11.00 | **`page.tsx:1301`** |
| **"Campaign balance may be insufficient"** | fires when `(actualPaidAmount ?? finalAmount ?? amount) > campaignAvailable`; `11.00 > 0.00` | shown | **`page.tsx:1349`**, `campaignAvailable` from `payouts/route.ts:207-214` |
| **"$63.89 over earned"** | `clipperOverEarnedAmount = totalGross − earned` | 63.89 | **`page.tsx:1367`**, computed `payouts/route.ts:227-231` |

### EXPLAINING THE $63.89 PRECISELY

`totalGross` at `payouts/route.ts:227` is the sum of **`clipperLiability`** (`actualPaidAmount ?? amount`, `balance.ts:126-132`) over every payout of this **(clipper, campaign)** pair in `PAID / REQUESTED / UNDER_REVIEW / APPROVED`, **including this one**. `earned` at `:206` is his APPROVED, not-deleted, not-unavailable clip earnings **on this campaign only**, plus marketplace creator earnings.

```
PAID   $78.54   actualPaidAmount NULL  → clipperLiability 78.54
APPROVED $60.27 actualPaidAmount 11.00 → clipperLiability 11.00
REJECTED $22.68                        → excluded (not a liability status)
                                    totalGross = 89.54
earned on Zhus Edit                              = 25.65
                          overRaw = 89.54 − 25.65 = 63.89   ✓ exactly as displayed
```

**Is that base correct? Partly, and the wrong half is the half that matters.**

* **The `earned` side is right and is the alarm working.** `$25.65` really is all the platform now records for him on this campaign, and `$78.54` really has gone out. A clipper whose record sits below money already paid is exactly what BL-716 and BL-823 were about, and the chip is correctly refusing to hide it.
* **The `totalGross` side is quietly wrong, and it understates the problem.** It uses `clipperLiability`, which prefers `actualPaidAmount`, so this payout contributes **$11.00** rather than the **$60.27** the clipper is still claiming. Had the owner never adjusted, the same expression would read `78.54 + 60.27 − 140.54 = **−$1.73**` — **no warning at all**. So the chip did not exist before the adjustment, and the adjustment both created the overage and shrank the number describing it. **Measured against what he is actually still owed, the true figure is `89.54 → 138.81 − 25.65 = $113.16`, not `$63.89`.**
* **BL-822's two-bases problem is still present on this screen.** The over-earned chip uses `clipperLiability` (gross, `actualPaidAmount ?? amount`); the insufficient-balance line three lines above it uses `actualPaidAmount ?? finalAmount ?? amount` (`page.tsx:1349`); the per-campaign figure they are compared against uses `payoutLiability` (`actualPaidAmount ?? finalAmount ?? amount`). **Three related figures on one row, three different priority chains.** BL-824 unified the gate and the balance; the admin payouts screen was not part of that round.

### EXPLAINING THE $11.00 SEND BOX

**`$11.00` is GROSS, and the box is labelled "Send".** That is the whole hazard.

`src/app/api/admin/payouts/[id]/adjust/route.ts:1-3` states it outright: *"OWNER reduces a payout from its requested **gross** to an actual paid amount"*. `clipperLiability` then treats `actualPaidAmount` as a direct substitute for `amount`, which is the gross column. **But `page.tsx:1301` renders it under the word `Send`**, and the adjust route never recomputes `feeAmount`, `expressFeeAmount` or `finalAmount` — those still read `$5.42`, `$2.41` and `$52.44`, all computed against `$60.27`.

**If the owner sends `$11.00` he overpays by `$1.43`.** The cash on an `$11.00` gross is `11.00 − 0.99 − 0.44 = **$9.57**`. BL-760 caught the identical `$5.44` error and BL-763 caught `$7.80`; this is the same confusion at a third site.

**Is `$11.00` what the system believes he can be paid?** **No.** No system figure equals `$11.00`. It is a number a human typed: the adjust modal prefills the **requested** amount (`page.tsx:414-415`, `String(Number(payout.amount).toFixed(2))` = `60.27`), so `11.00` was entered by hand. The nearest system figure at that moment was **`$9.32`** — see below. What the system believes he can be paid **today** is `$0.00`.

### What the owner was looking at when he adjusted — reconstructed

| figure | before `17:03:37` | now |
|---|---|---|
| his global earned (APPROVED, live, all campaigns) | **$148.13** | $33.24 |
| paid gross / paid cash | $78.54 / $71.47 | unchanged |
| locked in flight (`clipperLiability`) | $60.27 | $11.00 |
| `globalAvail` (`payouts/route.ts:195`) | **$9.32** | **$0.00** |
| `campaignAvailable` raw (`:209`) | $69.07 | $0.00 |
| `campaignAvailable` **displayed** after the clamp (`:214`) | **$9.32** | **$0.00** |
| "Campaign balance may be insufficient" | **SHOWN** (`52.44 > 9.32`) | SHOWN |
| over-earned | **−$1.73 → not shown** | **$63.89 shown** |

### THE WARNING THAT STARTED THIS IS A FALSE POSITIVE, AND IT IS SYSTEMIC

`campaignAvailable` at `:207-208` correctly subtracts the payout's **own** liability (`ownLiab`) before comparing. The global clamp it is then reduced by at `:189-196` **does not** — `lockedByUser` at `:192` sums every in-flight payout **including this one**. So the row's own amount is compared against a figure that has already had the row's own amount removed from it.

**Algebraically, with one payout in flight, the warning fires whenever `2 × self > earned − paid`, that is whenever the request exceeds half the clipper's remaining balance.** For Clipper M before the adjustment: `2 × 52.44 = 104.88 > 148.13 − 78.54 = 69.59` → fires, on a payout that was `$9.32` INSIDE his balance.

**Measured across every in-flight payout on the platform right now:**

```
payout      clipper   status        send    earned   paid    locked  globalAvail  warning
cmq084lzp0  cmpq15k2  UNDER_REVIEW  52.40    59.11    0.00   57.58     1.53       FIRES
cmsv1ifo70  cmsiyg70  APPROVED      11.00    33.24   78.54   11.00     0.00       FIRES
cmt00abj90  cmsviqg3  REQUESTED     20.98    25.35    0.00   22.80     2.55       FIRES
cmt1isvjo0  cmst7ibi  REQUESTED     34.50    67.15    0.00   59.96     7.19       FIRES
cmt1ixetv0  cmq8csdg  REQUESTED     15.64    18.72    0.00   17.98     0.74       FIRES
cmt1um8fn0  cmst7ibi  REQUESTED     17.66    67.15    0.00   59.96     7.19       FIRES
cmt5vcthe0  cmsm2zio  REQUESTED     74.64   142.85   53.82   85.79     3.24       FIRES
cmt6rzjii0  cmt5llnl  REQUESTED     15.63    21.73    0.00   17.97     3.76       FIRES
cmt7eqn2x0  cmpl310f  REQUESTED     85.46    98.28   41.59   98.23     0.00       FIRES
```

**Nine out of nine.** Not one of those clippers is genuinely over-committed. **A warning that fires on every row carries no information, and this one moved the owner to remove `$114.89` of a clipper's recorded earnings.**

### Computed independently, from views and each clip's OWN stamped CPM

Latest `clip_stats.views` per clip × `cpmAtSubmissionDecimal`, with `minViewsAtApproval` and `maxPayoutPerClip` applied, ignoring every stored total:

| campaign | approved clips | views | **independent earned** | stored now | stored before the adjustment |
|---|---|---|---|---|---|
| Zhus Edit (0.50 CPM) | 42 | 287,142 | **$139.61** | $25.65 | $140.54 |
| Zhus Meme (0.20 CPM) | 2 | 38,130 | **$7.59** | $7.59 | $7.59 |
| **total** | 44 | 325,272 | **$147.20** | **$33.24** | **$148.13** |

**The independent figure confirms the pre-adjustment record and contradicts the post-adjustment record by `$113.96`.** The `$0.93` gap between `$139.61` and `$140.54` is named rather than smoothed: my figure uses today's view counts while the stored figure was fixed at `17:03:37`, and the stored figure carries `$0.19` of bonus that a pure views × CPM calculation does not model. **11 of his 42 approved Zhus Edit clips sit below the 1,000-view minimum and correctly earn `$0.00`**, including the only two approved clips NOT in the payout snapshot (794 and 587 views).

**BL-823's shape does not apply here.** All 24 of his rejected clips were rejected on **9, 12 and 13 August**, before the request on the 16th. Nothing was rejected after payment.

---

## PART 4 — WHAT HE IS ACTUALLY OWED

### His true position

| | gross | cash |
|---|---|---|
| **genuinely earned, all time** (independent, from views × own stamps) | **$147.20** | n/a |
| earned as the platform recorded it before `17:03:37` today | $148.13 | n/a |
| earned as the platform records it now | $33.24 | n/a |
| **already paid** (one PAID row, `2026-08-15 21:10:27.238`) | **$78.54** | **$71.47** |
| remaining against genuine earnings | **$68.66** | — |
| **this request** | **$60.27** | **$52.44** |
| what remains after this request is honoured | $8.39 | — |

**Under BL-824's rule that already-paid money is final**, the `$78.54` he received is his and can never be offset. The question is only what is still owed on top, and `$147.20 − $78.54 = $68.66` gross covers the `$60.27` he asked for with `$8.39` to spare.

### So is he owed less because a rate fell?

**No. No rate fell.** The only thing that fell is a number the owner overwrote by hand today, on a screen that was showing him a warning it shows on every row.

**The honest reading, stated as the owner's call.** If the `18.25%` cut was a deliberate quality judgement, the correct figure is `$11.00` gross = **`$9.57` cash** — and the payout still cannot be completed without a code change. If it was not deliberate, and the evidence says it was not — no reason was recorded (`reason: NULL`), the owner's own account of events names a CPM change that never happened, and the trigger was a warning with a 9-out-of-9 false-positive rate — then the correct figure is the full request.

### ONE LINE

> **Send Clipper M `$52.44`.**

---

## PART 5 — HOW MANY OTHERS ARE STRANDED

### Every payout APPROVED or otherwise in flight, with its age

DB `now()` = `2026-08-24 18:00:55.291632+00`.

| payout | clipper | status | gross | cash | speed | campaign | age past deadline |
|---|---|---|---|---|---|---|---|
| `cmq084lzp0` | `cmpq15k2` | UNDER_REVIEW | 57.58 | 52.40 | STANDARD | bees.n.honey | **no deadline set**, requested `2026-06-05 01:06:42.901` — **80 days** |
| **`cmsv1ifo70`** | **`cmsiyg70`** | **APPROVED** | 60.27 | 52.44 | EXPRESS | Zhus Edit | **8 days 05:59:08** |
| `cmt00abj90` | `cmsviqg3` | REQUESTED | 22.80 | 20.98 | EXPRESS | Zhus Edit | **4 days 06:34:36** |
| `cmt1isvjo0` | `cmst7ibi` | REQUESTED | 39.66 | 34.50 | EXPRESS | Zhus Edit | **3 days 05:08:31** |
| `cmt1ixetv0` | `cmq8csdg` | REQUESTED | 17.98 | 15.64 | EXPRESS | SomeSome App | **3 days 05:04:59** |
| `cmt1um8fn0` | `cmst7ibi` | REQUESTED | 20.30 | 17.66 | EXPRESS | Zhus Meme | **2 days 23:37:45** |
| `cmt5vcthe0` | `cmsm2zio` | REQUESTED | 85.79 | 74.64 | EXPRESS | Zhus Meme | **04:06:00** |
| `cmt6rzjii0` | `cmt5llnl` | REQUESTED | 17.97 | 15.63 | EXPRESS | SomeSome App | not yet due (11 h left) |
| `cmt7eqn2x0` | `cmpl310f` | REQUESTED | 98.23 | 85.46 | EXPRESS | SomeSome App | not yet due (21 h left) |

**Six express payouts are overdue, plus one UNDER_REVIEW row 80 days old with no deadline at all** (BL-680's stale class, still there). Against BL-811's three cases at 2 h, 3.6 d and 7 d, the population has **doubled and aged**: the worst is now 8 d 6 h. `$260.85` of cash is past its promise.

**Clipper M's row shows a 12-hour deadline** (`00:01:46 → 12:01:46`) because it was created on 16 August, the same day BL-811 moved the express promise from 12 h to 24 h. Every later express row carries 24 h. Not a defect; noted so the age is read correctly.

### Would the others hit the same failure? No.

The failure needs a **stale reduction** on the snapshot clips AND `existingLiability > campaignAvailable`. Tested against all nine:

```
payout      stale_clips  campaign_earned  others_liability  self   would fail?
cmq084lzp0       0            59.11            0.00        52.40      no
cmsv1ifo70      40            25.65           71.47        11.00     YES
cmt00abj90       0            22.80            0.00        20.98      no
cmt1isvjo0       0            39.79            0.00        34.50      no
cmt1ixetv0       0            17.98            0.00        15.64      no
cmt1um8fn0       0            27.36            0.00        17.66      no
cmt5vcthe0       0           142.85           46.83        74.64      no
cmt6rzjii0       0            21.73            0.00        15.63      no
cmt7eqn2x0       0            98.28            0.00        85.46      no
```

**One stranded row.** The other eight are simply waiting for the owner.

**And the adjust flow is not chronically broken.** Seven payout adjustments have ever been applied, `2026-05-20` to today. **Six reached PAID**, several within seconds. Clipper M's is the only one that has ever stuck, because he is the only one whose post-adjustment campaign earnings landed **below money already paid on that same campaign**.

### THE REMINDER ENGINE HAS STILL NEVER FIRED — and this round names why

```
payout_requests: 191 rows
  rows with remindersSentCount > 0 : 0
  rows with lastReminderSentAt set : 0
  max(lastReminderSentAt)          : NULL
notifications of any PAYOUT_REMINDER_* type, ever : 0
```

**Unchanged since BL-811, roughly ten weeks after BL-179 shipped it.**

**The mechanism, and it is not a missing wire.** `runPayoutRemindersOnce` **is** called, at `src/app/api/cron/tracking/route.ts:452-453`. Its candidate query (`payout-reminders.ts:252-262`) would match **8 of the 9 rows above**, and OWNER recipients exist. Only two guards sit before it in the handler, both auth (`:59`, `:64`).

**But it is the LAST statement in a route declared `export const maxDuration = 300` (`cron/tracking/route.ts:33`), placed after all tracking work — and tracking work takes far longer than 300 seconds.** Measured from `clip_stats.checkedAt` over the last eight hourly ticks:

```
hour (UTC)   stats written   first write   last write   span
10:00            157          10:10:24     10:57:13    00:46:48
11:00            217          11:01:10     11:30:01    00:28:51
12:00            271          12:01:13     12:45:09    00:43:55
13:00            232          13:00:43     13:35:04    00:34:21
14:00            255          14:00:41     14:21:36    00:20:55
15:00            229          15:01:09     15:40:41    00:39:32
16:00            287          16:00:24     16:58:21    00:57:57
17:00            250          17:01:09     17:59:24    00:58:15
```

**Every tick runs 21 to 58 minutes against a 5-minute cap.** The sweep at `:452` is not reached. **That is the leading explanation and it is consistent with every measurement available from here.** It is not proven: `PAYOUT_REMINDERS_ENABLED` is a Railway environment variable and the web-service log is not readable from this position, so a kill-switch set to `false` cannot be excluded. **Either way, no reminder has ever reached the owner, and he was not pinged about any of the six overdue rows above.**

### Every clipper carrying an over-earned figure

23 (clipper, campaign) pairs where gross commitment exceeds recorded earnings, redacted:

| clipper | campaign | total gross | earned | **over earned** | in flight? |
|---|---|---|---|---|---|
| `cmofpudr` | somesome | 1,607.33 | 108.38 | **1,498.95** | no |
| `cmp7153e` | somesome | 1,313.86 | 0.00 | **1,313.86** | no |
| `cmpl1dds` | somesome | 264.00 | 0.00 | **264.00** | no |
| **`cmsiyg70`** | **Zhus Edit** | **89.54** | **25.65** | **63.89** | **YES** |
| `cmqez5c2` | STRAENGE | 1,894.14 | 1,833.67 | **60.47** | no — BL-716's clipper, unchanged |
| `cmr1rz2j` | GainzAlgo (REPOST) | 31.75 | 0.00 | 31.75 | no |
| `cmpfozzs` | GainzAlgo (REPOST) | 26.54 | 0.00 | 26.54 | no |
| `cmpl310f` | somesome | 25.54 | 0.00 | 25.54 | no — BL-688's C-1 |
| `cmoaejuc` | somesome | 61.89 | 38.80 | 23.09 | no |
| `cmrng806` | Panic Baby | 76.83 | 57.65 | 19.18 | no |
| `cmp7ic4p` | somesome | 17.00 | 0.00 | 17.00 | no |
| `cmpl310f` | Panic Baby | 16.05 | 0.00 | 16.05 | no |
| `cmq0qn2l` | GainzAlgo (REPOST) | 14.46 | 0.00 | 14.46 | no |
| `cmoal818` | somesome | 12.76 | 0.00 | 12.76 | no |
| `cmpfozzs` | bees.n.honey | 33.44 | 21.18 | 12.26 | no |
| `cmr1bsip` | bees.n.honey | 10.17 | 0.00 | 10.17 | no |
| `cmp71p89` | somesome | 34.79 | 25.55 | 9.24 | no |
| `cmqv7svp` | bees.n.honey | 104.62 | 99.01 | 5.61 | no |
| `cmosj3qk` | Panic Baby | 114.16 | 109.97 | 4.19 | no |
| `cmp75zkf` | GainzAlgo (REPOST) | 10.31 | 7.45 | 2.86 | no |
| `cmpmuwfh` | somesome | 20.61 | 19.65 | 0.96 | no |
| `cmosmyqk` | somesome | 993.36 | 992.42 | 0.94 | no |
| `cmqmnvgs` | WinGram | 11.23 | 11.21 | 0.02 | no |

**22 of the 23 are historical**, on finished campaigns, informational chips on PAID rows — the population BL-824's paid-is-final rule addresses. **Clipper M is the only clipper whose over-earned warning sits on a payout that still has to be completed, and the only one whose overage was created today.**

---

## PART 6 — THE VERDICT AND THE FIX SPEC

### ONE LINE

> **This payout cannot be completed because a payout adjustment the owner applied today cut this clipper's recorded earnings to `$25.65` — below the `$78.54` already paid him — so the mark-paid path computes an auto-adjusted amount of `$0.00` and the database refuses to store a payout amount of zero; today the owner should pay him `$52.44` and stop clicking Mark Paid, because it can never succeed.**

### Today, without a deploy

**Nothing on any screen can fix this.** There is no undo for a payout adjustment, and Mark Paid is a permanent failure. What the owner can do today:

1. **Send `$52.44`.** That is the cash he is owed on his own work. **Not `$60.27`** (gross, overpays by `$7.83`), **not `$11.00`** (gross, and wrong), **not `$9.57`** unless the 18.25% cut was deliberate.
2. **Do not click Mark Paid again.** Five identical failures are already on the record; the sixth will be identical.
3. **Leave the row alone otherwise.** Rejecting it would tell him his request was declined, which is untrue, and would release his other `$7.59` into a balance that still reads `$0.00`.
4. **Treat the other eight in-flight payouts as normal.** None of them will hit this, and six are past their promise.

**Whether a hand payment is safe here, and it is, unlike BL-763.** The `$60.27` row stays APPROVED, which keeps it inside `lockedByUser` (`payouts/route.ts:192`), so his available balance stays `$0.00` and the same money cannot be requested a second time while it sits there. The reconciliation still has to happen once the fix ships.

### The fix spec — three items, none performed

**1. THE DEFECT. Never write a zero payout amount. `src/app/api/payouts/[id]/review/route.ts:228-231` and `:248`.**
`newAmount: campaignAvailable` can be `0`, and `:248` writes it into a column constrained `> 0`. Guard it: when `campaignAvailable` rounds to zero the auto-adjust is not a valid outcome and the branch must fall through to the typed `INSUFFICIENT_BALANCE` throw at `:221`, which already has an explanatory 400 at `:297-301`. **Must be proven:** the 503 becomes a 400 naming the campaign earnings and the committed total; the non-zero auto-adjust path is unchanged on the six adjustments that already completed; `P2034` still retries; a genuine exception still reaches the 503. **Rollback:** revert the guard; behaviour returns to today's, which is a permanent 503. **Money risk: none — this changes only which refusal is produced, never an amount.**

**2. THE DEFECT THAT CAUSED IT. The insufficient-balance warning is a 9-of-9 false positive. `src/app/api/payouts/route.ts:189-196` and `:214`, rendered at `admin/payouts/page.tsx:1349`.**
`campaignAvailable` at `:207-208` subtracts the payout's own liability; the global clamp it is reduced by at `:195` does not, so every row is compared against a number that already excludes it. Subtract the row's own liability from the global figure before clamping, exactly as `:207` already does per campaign. **Must be proven:** the warning stops firing on all nine rows above and still fires on a constructed genuinely-over-committed case; no `campaignAvailable` figure goes UP for any clipper who is truly over-committed; the withdrawal gate at `payouts/route.ts:713` is **not** in the diff. **Rollback:** `GLOBAL_PAYOUT_CLAMP_ENABLED=false` already exists as an env kill switch (`src/lib/payout-clamp-flag.ts:13`). **This is the item I would ship first.** It is the only one that prevents a repeat.

**3. A REFUSAL RENDERING BADLY, not a defect. `review/route.ts:329`.**
`503 … please retry` is the wrong shell for every non-`P2034` failure, because none of them is transient. Route on the error the way BL-689's `PayoutRefusal` type routes the withdrawal gate, so a constraint violation reads as a permanent, named refusal. **Must be proven:** genuine serialization conflicts still retry and still 503.

**Also worth deciding, and not a code fix.** There is **no undo for a payout adjustment**, and the ratio is a permanent multiplier on all future earnings (`earnings-calc.ts:556-578`, `tracking.ts:1925-1955`). Clipper M's 40 clips will pay 18.25% forever. A reversal path, or at minimum a typed confirmation on the adjust modal stating that the cut is permanent and irreversible, belongs on the backlog.

**And one gap named without a recommendation.** `payouts/[id]/review/route.ts` does not import `effectivePaidOut`, so BL-824's paid-is-final rule does not reach the mark-paid path. **It would not have saved this payout** (the arithmetic is shown in PART 2), so closing it is correctness housekeeping rather than a remedy, and it touches a money path.

### Historical repair

**None is needed for anyone else.** The 22 other over-earned pairs are historical and are what BL-824 addressed. **One repair is needed for Clipper M**, and it is the reversal of today's adjustment: restoring `payoutReductionRatio` to `NULL`, `earningsFrozenAt`/`earningsFrozenReason` to `NULL`, and each of the 40 clips' `earnings`/`baseEarnings`/`bonusAmount` to the values in `payout_adjustments.originalEarningsSnapshot`, which the adjust route stored for exactly this purpose. **That is a money write through `writeClipEarnings` and it is NOT this round's to make. It has not been performed and no SQL for it was executed.**

### What could not be measured

* **Whether `PAYOUT_REMINDERS_ENABLED` is set to `false` in Railway.** Not readable from here. The 300-second cap against 21-to-58-minute ticks is the leading explanation, not a proof.
* **Whether the deployed build includes BL-824.** BL-821's route answers `401` on production so the live build is at least 2026-08-23, but BL-824 added no route and cannot be probed unauthenticated. It does not change this verdict: the mark-paid path never calls `effectivePaidOut` in either version.
* **Why `$11.00` specifically.** The modal prefills `$60.27`, so a human typed it. The nearest system figure at that moment was `$9.32`. The `reason` field is `NULL`.
* **The Railway web-service log.** Not readable. The `errorMessage` in `audit_logs` is the same string the log line at `:313` carries, so nothing was lost.

---

## A REPLY THE OWNER CAN SEND

> Hi — thanks for your patience on this, and sorry it has taken this long.
>
> Your payout has been sitting because of a problem on our side, not anything to do with your clips or your account. When we went to send it, our system hit an error that stopped the payment going out, and it kept hitting the same error each time we tried. That is our bug and we are fixing it.
>
> Your clips are fine. Nothing you did caused this, nothing is under review, and your work is all still counted.
>
> We are sending you $52.44 now. That is your $60.27 request less the 9% platform fee and the 4% express fee, which is what you agreed to when you chose express.
>
> You may see some odd numbers on your earnings page for a short while, including a balance that looks lower than it should. That is part of the same problem and we are correcting it. It does not change what you are owed.
>
> Thanks for sticking with us, and sorry again for the wait.

---

## SAFETY

READ ONLY. One document. **No code, data, schema, config or money change. No payout created, modified, approved, rejected, voided, retried or paid. No balance touched. Nothing recalculated, restored or repaired. The failing action was NOT retried** — the real error was read out of `audit_logs`, where the route itself records it. Every figure comes from `SELECT` through `scripts/run-select.js`, every timestamp cast `::text` against DB `now()`. **No handle, email or wallet address appears anywhere, not even partially**; the clipper is Clipper M with an 8-character id prefix the owner can map privately. Worked in an isolated worktree at `C:/w826` on `checkpoint/BL-826`, removed at exit; `node_modules` never junctioned. **Another round (BL-825) merged to `main` during this session and moved it from `e5a1846a` to `100e8483`; nothing it holds was touched, and every line number above was re-verified at `100e8483`.** A markdown-only diff cannot change tsc or the build, so **no build was run and none is claimed**. Counts taken with `grep -c` and explicit `count(*)`, never piped through `head`. No heredocs. One shell at a time. No dashes as bullets.
