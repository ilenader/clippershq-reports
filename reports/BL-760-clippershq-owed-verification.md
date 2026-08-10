# BL-760 — does Clipper A genuinely deserve the $60.47, settled from first principles

**2026-08-10 · DB `now()` = `2026-08-10 16:52:10.162568+00` · AUDIT ONLY, READ ONLY.**
No code, data, schema, config or money changed. Nothing paid, restored, restamped, re-derived, retired
or revived. `agency-monitor --fix` never run. No Apify actor, no paid probe, spend $0.00. Base
`origin/main` @ `018c22ca`, isolated worktree `C:/m760`, removed at exit. Every timestamp cast `::text`
against DB `now()`. The handle is redacted and no wallet address was selected or printed.

**Clipper A** = user id prefix `cmqez5c2`. The owner can map this privately in admin.

> **This report SUPERSEDES the earlier same-day BL-760** published at `2026-08-10 16:13`. It reaches the
> same headline figure by independent arithmetic, and adds two things that file did not have: **the
> $1,894.14 was never cash** (he received $1,647.90), and the STRAENGE clipper total is **$2,636.59**,
> not $2,642.82, once `videoUnavailable` clips are excluded as CLAUDE.md requires. Neither changes the
> verdict. The earlier version remains in this repository's git history.

---

## THE ANSWER, BEFORE THE WORKING

> **Yes, Clipper A is genuinely owed it. The books are not saying he was overpaid; they are comparing a
> correct withdrawal against a record that was written DOWN afterwards.**
>
> Computed from nothing but his clips, their view histories and his own stamped CPM, **he earned
> $2,450.63 on STRAENGE and drew $1,894.14 against it.** That is not an overpayment under any reading
> of his own work.
>
> **Pay $55.03 by hand, not $60.47.** The $60.47 is a GROSS balance figure. Every dollar he has ever
> converted to cash passed through the 9% payout fee, and this one would have too. **Sending $60.47
> overpays him by $5.44.**
>
> He should separately request his **$399.64** through the platform himself. BL-719's $346.11 and
> $406.58 are stale by $53.53 and must not be used.

---

## PART 1 — WHAT HE GENUINELY EARNED, IGNORING EVERY STORED TOTAL

### The formula, read from source rather than assumed

`calculateClipperEarnings` (`earnings-calc.ts:112-212`), applied by hand in SQL:

```
if views < campaignMinViews (1,000)          -> $0.00
base  = min(views / 1000 x stampedCpm, 300)     <- cap applies to BASE ONLY (:169-181)
bonus = base x bonusPercent / 100               <- bonus may exceed the per-clip cap (:183-185)
earned = round2(base) + round2(bonus)           <- F-ROUNDING-FIX derivation (:200-202)
```

One line matters for PART 4 and is quoted rather than paraphrased: `earnings-calc.ts:187-189` says the
platform fee is **"calculated for reference but NOT subtracted... Fee is applied once at payout time,
not at earnings calculation time."** Everything in this section is therefore a GROSS figure.

### His population on STRAENGE

Campaign read from its own row, not assumed: budget **$3,000**, clipperCpm $0.50, ownerCpm $0.25,
minViews 1,000, maxPayoutPerClip $300, CPM_SPLIT, `lockedOwnerShareDecimal` 0.33333333,
`guaranteeOwnerSplit` true, `platformFeePctDecimal` NULL, `manualSpent` NULL, status **PAST**,
auto-paused `2026-08-01 06:31:33.721`.

| | |
|---|---|
| Clips, all time | **83** (80 APPROVED, 3 REJECTED) |
| `isDeleted` / `videoUnavailable` | **0 / 0** |
| Carrying `payoutReductionRatio` | **0** |
| Carrying `earningsFrozenAt` | **0** |
| Carrying `savedEarnings` (the retirement stamp) | **0** |
| Distinct clipper CPM stamps | **1**, every clip exactly `0.5000` |
| Distinct owner CPM stamps | **1**, every clip exactly `0.2500` |
| `clip_stats` rows behind them | **4,572** |
| STRAENGE last touched any field | `2026-08-05 13:37:35.466` |

The stamps are not just uniform, they are correct: `0.2500 / 0.5000 = 0.5`, and
`s/(1−s)` at `s = 0.33333333` is `0.5` exactly. No BL-539 stamp ambiguity anywhere in his record.

### The computation

| step | amount |
|---|---|
| Total views on his 80 APPROVED clips | **5,403,031** |
| Base, after the $300 per-clip cap and the 1,000-view gate | **$2,249.33** |
| Plus each clip's own bonus percentage | **+$201.22** |
| **= WHAT HE GENUINELY EARNED ON STRAENGE** | **$2,450.63** |

Three independent computations now agree: BL-716 said $2,450.55, BL-718 said $2,450.61, this round
measures **$2,450.63** straight from `clip_stats` rows. The 8-cent spread is per-clip rounding order
across 80 clips and nothing else. **The number is settled.**

### The comparison the owner asked for

| figure | amount | what it actually is |
|---|---|---|
| **Genuinely earned** | **$2,450.63** | first principles, this round, independent |
| **Gross drawn against his balance** | **$1,894.14** | one PAID row, `2026-07-07 16:09:10.717` |
| **Cash that actually reached him** | **$1,647.90** | see below, this is new |
| What the trim left on the record | $1,833.67 | current stored value |
| What his record says today | $1,833.67 | unchanged since `2026-08-05 13:37:35.466` |

**The arithmetic supports $2,450.63, and it supports the withdrawal.** He drew $1,894.14 against
$2,450.63 of earned value and is **$556.49 short of his own work**. There is no reading of the clip
data in which $1,894.14 is an overpayment. The stored $1,833.67 is not an earnings figure at all; it
is what a pool cap left behind.

### THE $1,894.14 WAS NEVER CASH, AND EVERY PRIOR REPORT CALLS IT "PAID"

The PAID row, read field by field:

| field | value |
|---|---|
| `amount` (gross, debited from his balance) | **$1,894.14** |
| `feePercent` / `feeAmount` | 9% / **$170.47** |
| `payoutSpeed` / `expressFeeAmount` | **EXPRESS** / **$75.77** (4%) |
| **`finalAmount`** (what left the platform) | **$1,647.90** |

`1,894.14 − 170.47 − 75.77 = 1,647.90`, exactly. Confirmed in code: `payout-calc.ts:83` computes
`finalAmount = requested − feeAmount − expressFeeAmount`, and `payouts/route.ts:403` sets the base fee
to 9% (4% if referred) with express hard-coded at 4%.

BL-714, BL-716, BL-718, BL-719, BL-758 and the earlier BL-760 all say he "was PAID $1,894.14". **He was
DEBITED $1,894.14 and RECEIVED $1,647.90.** Both are true statements about different things, and
`balance.ts:126-132` is explicit that the clipper's balance is consumed by the **gross** `amount`, never
`finalAmount`, so $1,894.14 is the correct number for the entitlement comparison above. But the
distinction is decisive for PART 4, and no prior report drew it.

### The owner's specific worry: was any clip zeroed, revived, deleted or restored?

**No. Not one. Closed with evidence, and it was the most important thing to check.**

| test, over all 4,572 stat rows | result |
|---|---|
| Clips ever `videoUnavailable` | **0 of 83** |
| Clips carrying `savedEarnings` | **0 of 83** |
| Clips `isDeleted` | **0 of 83** |
| Clips whose **current views are below their all-time peak** | **0 of 83** |
| Readings where views fell to 0 after being positive | **0** |
| View-decrease events, all time | **8** |
| Largest single decrease | **409 views**, worth **$0.20** |
| Window containing every decrease | `2026-06-25 06:10:55.047` to `2026-06-26 05:21:45.141` |
| Clips involved | **3**, all fully recovered |
| Zero readings that exist at all | **3**, and every one is that clip's FIRST reading |

The three zeros are clips being registered before they have views, not fabricated zeros. **BL-751's
zeroing population and BL-748's fabricated-zero defect do not touch this clipper.** Every one of his
clips is at its all-time peak right now.

**The hypothesis that "the trim may have been correct at the time and wrong now" is dead. His views
have only ever gone up, so the trim can only have been more wrong at the time, never less.**

---

## PART 2 — WAS THE TRIM ENFORCING A REAL CAP, OR WAS IT THE DEFECT?

**Both, and separating the two is the entire answer.**

### The campaign genuinely was oversubscribed

Recomputed identically for every clipper on STRAENGE, excluding `videoUnavailable` clips as CLAUDE.md
requires of any earnings sum:

| id8 | clips | genuinely earned | stored now | shortfall |
|---|---|---|---|---|
| **`cmqez5c2`** (Clipper A) | 83 | **$2,450.63** | $1,833.67 | $616.96 |
| `cmq7qh6p` | 26 | $115.33 | $94.53 | $20.80 |
| `cmqs7gjq` | 10 | $65.33 | $64.84 | $0.49 |
| `cmr0k3ke` | 1 | $2.37 | $2.37 | $0.00 |
| `cmqxtmu6` | 1 | $1.61 | $0.99 | $0.62 |
| `cmqqm6m9` | 1 | $1.32 | $1.16 | $0.16 |
| `cmpfozzs` | 14 | $0.00 | $4.15 | −$4.15 |
| 14 more clippers | 33 | $0.00 | $0.00 | — |
| **TOTAL** | **179** | **$2,636.59** | **$2,001.71** | **$634.88** |

| | |
|---|---|
| What STRAENGE's clippers genuinely earned | **$2,636.59** |
| What the clipper pool can pay: `(1 − 0.33333333) × $3,000` | **$2,000.00** |
| **Genuine overshoot** | **$636.59**, or 31.8% of the pool |

**Yes: the campaign really was overspent on the clipper side, by $636.59.** Somebody has to absorb it,
so the question is genuinely WHO and not whether. Clipper A is 92.9% of the reason it is oversubscribed:
**his $2,450.63 alone exceeds the entire $2,000 pool.**

One row deserves a note rather than silence. `cmpfozzs` stores $4.15 on clips that are ALL
`videoUnavailable`, so it computes to $0.00 earned here. That is a separate, tiny, pre-existing
inconsistency and it does not bear on Clipper A.

### But the trim was still the wrong instrument, and that is not a contradiction

Read at `tracking.ts:2507`, the line was `if (newEarnings > clipperHeadroom) newEarnings = clipperHeadroom`:
an **absolute assignment with no floor at the clip's stored value**, while its sibling branches had one.
`clipperHeadroom` is derived from **other** clippers' spend, so the line does not cap growth. It moves
money sideways between clippers. The code comment now in place at `:2508-2520` says so in the
repository's own words, naming this clipper's $60.47 as the measured case.

The distinction that settles PART 3: **what it took back was not surplus he had yet to receive. It was
money that had already left the platform.** The pool stood at exactly $2,000.00 when the withdrawal was
approved on `2026-07-07`, and the trim fired afterwards, reaching backwards through a completed,
correctly-gated payment.

**The fix is live.** `capButNeverBelowStored` (`earnings-never-decrease.ts:170`) is wired at three sites
on `018c22ca`: `tracking.ts:2525` (the very line that trimmed him), `tracking.ts:2583`, and
`clip-earnings-writer.ts:383`. BL-719 reverted the data repair and the budget raise; it explicitly kept
the code. **If the identical events happened today he would not be trimmed.**

### BL-563's shared gross guard is not involved

`decideOwnerGross` (`owner-share-guard.ts`) protects the OWNER side against stamp-versus-share
ambiguity. STRAENGE has zero ambiguous rows: every stamped ratio is exactly `0.5000` and matches
`s/(1−s)` precisely. BL-563's $173.41 concerns owner-credit clips and does not bear on this clipper's
entitlement. **The guard neither blocks nor supports the payment.**

---

## PART 3 — RESOLVING THE CONTRADICTION

### (b) "The trim was correct, he was genuinely overpaid, paying again would be a second overpayment" — **FALSE**

The apparent overpayment is entirely mechanical: **it is measured against a number written down AFTER
the withdrawal.** He drew $1,894.14 when his record read $1,894.14 and the gate refused anything above
it. He earned $2,450.63. A $1,894.14 draw against $2,450.63 of earned value is not an overpayment, and
topping it up is not a second one.

It is also **local to one campaign**. Platform-wide he has earned $2,293.78 as recorded and drawn
$1,894.14, leaving $399.64 of headroom. **PART 5 confirms independently that he is NOT among the four
clippers who hold more than they earned.** The books do not say he was overpaid; one per-campaign slice
of them does.

### (c) "Something changed since those reports" — **TRUE, and it invalidates BL-719's numbers**

| | BL-719, `2026-08-05` | today | change |
|---|---|---|---|
| STRAENGE recorded | $1,833.67 | **$1,833.67** | **unchanged to the cent** |
| Panic Baby recorded | $406.58 | **$460.11** | **+$53.53** |
| Lifetime recorded | $2,240.25 | **$2,293.78** | +$53.53 |
| What he can request himself | $346.11 | **$399.64** | **+$53.53** |

His STRAENGE record cannot move: the campaign is PAST and `tracking.ts` excludes PAST campaigns from the
cron. His Panic Baby clips are still live and were touched today at `2026-08-10 16:11:12.788`.
**BL-719's $346.11 and $406.58 are stale by $53.53 and will keep drifting. The $60.47 itself has not
moved and will not.**

### (a) "He genuinely earned it and is owed it" — **TRUE**, and here is the arithmetic

The pool is short $636.59 and someone absorbs it. There are exactly two defensible allocation rules.

**Rule R, the ratchet.** Money already recorded and drawn is never written down. His STRAENGE
entitlement stays **$1,894.14**, the pool finishes $62.18 over its cap, and the owner absorbs it.
Owed on STRAENGE: **$1,894.14 − $1,833.67 = $60.47.**

**Rule P, strict pro rata.** Split the $2,000 pool in proportion to genuine earnings. His share is
`$2,000 × $2,450.63 / $2,636.59` = **$1,858.95**. He drew $1,894.14, so he sits **$35.19 above** his
proportional share and would be owed nothing further on STRAENGE.

**Rule R is not a preference, it is what the platform runs.** BL-718 shipped `capButNeverBelowStored`
and BL-719 kept it; it is live at three sites on `018c22ca` and verified above. Under the rule the code
enforces today, his STRAENGE figure would be $1,894.14 and the $60.47 would never have been taken.

**And the owner has already chosen Rule R knowingly.** BL-719 records his decision: do not raise the
budget, because raising it on a finished campaign means owing the client $100 more; pay the clipper by
hand instead. That is Rule R with the overshoot absorbed personally rather than billed to the client.
The policy question is not open. It was decided, and this round confirms the decision was sound.

**(a) is true.** The two rules differ by $60.47 versus $0.00 on the STRAENGE slice, and the platform's
own shipped code answers $60.47.

### Why the three reports and the books both look right

They answer different questions. BL-716, BL-718 and BL-719 assert Rule R and are correct that under it
he is owed $60.47. The books assert only that `drawn > stored` on one campaign, which is arithmetically
true and says nothing about entitlement. **The contradiction dissolves once you see that `stored` is not
a measure of what he earned. It is what a cap left behind.**

Two corrections while I am here. **BL-714 calls the $1,894.14 "an overpayment the platform created
itself"; BL-716 calls it "correct when it was made". BL-716 is right**, and BL-714's framing is what
makes the books look like they contradict the conclusion. And every report including the earlier BL-760
calls $1,894.14 the amount "paid" to him, when $1,647.90 is what he received.

---

## PART 4 — WHAT HE SHOULD BE PAID TODAY, EXACTLY

### His position at `2026-08-10 16:52:10.162568+00`

| | amount |
|---|---|
| Genuinely earned, STRAENGE, first principles | **$2,450.63** |
| Recorded, STRAENGE (frozen, PAST campaign) | $1,833.67 |
| Recorded, Panic Baby (live, PAUSED, still growing) | $460.11 |
| **Recorded lifetime, APPROVED live clips** | **$2,293.78** |
| Gross drawn (one PAID row) | $1,894.14 |
| Cash actually received | $1,647.90 |
| **Withdrawable today** | **$399.64** |
| Visible but unwithdrawable | **$60.47** |
| Open payout requests | **0** |

`$2,293.78 − $1,894.14 = $399.64.` Had the trim never fired, lifetime would read $2,354.25 and
withdrawable would be **$460.11**. `$460.11 − $399.64 = $60.47` exactly. **The $60.47 is real, it is
precisely the amount his withdrawable balance is depressed by, and it reconciles to the cent.**

### The 9% fee, which is where the money is

**The $60.47 is a GROSS balance figure, not cash.** Confirming from source: `earnings-calc.ts:187-189`
states the fee is not subtracted at earnings time and is "applied once at payout time";
`payout-calc.ts:83` then deducts it. Every dollar he has ever converted to cash went through that
deduction, including on the very payment at issue.

The counterfactual, done properly:

| | gross | fee 9% | cash |
|---|---|---|---|
| What he would have requested had the trim never fired | $460.11 | $41.41 | **$418.70** |
| What he can request today | $399.64 | $35.97 | **$363.67** |
| **Difference, which is what he is actually short in CASH** | $60.47 | $5.44 | **$55.03** |

**Send $55.03. Sending $60.47 overpays by $5.44.** That is the fee the platform would have kept and
which the owner would otherwise be handing over as well as forgoing.

A strict reading would go further: he chose EXPRESS on his only paid request, at an extra 4%, which
would make the figure `$60.47 × 0.87 = $52.61`. **I do not recommend $52.61.** Express is a premium for
speed, a hand payment is not express, and charging him for a service he is not receiving would be
picking the arithmetic that suits the payer. **$55.03 is the fee-neutral figure.**

If the owner prefers not to charge his own clipper a processing fee on money a platform defect withheld,
$60.47 is a defensible act of goodwill. It is a $5.44 decision and he should make it knowingly rather
than by accident.

### The single number

> **Pay $55.03 by hand. Separately, he should request his $399.64 through the platform himself, which
> nets him $363.67 at standard speed. Total cash to him: $418.70.**

**$399.64 is a moving number.** Panic Baby is live and was touched today; his balance grows without
anyone doing anything. **The $60.47 and the $55.03 are fixed** and will not move, because STRAENGE is
PAST and excluded from the cron. Re-read the requestable figure at the moment of payment; do not re-read
the $55.03.

---

## PART 5 — THE OTHER OVER-HELD CLIPPERS

Reproduced independently using the global clamp's own base (`payouts/route.ts:658`: APPROVED,
`isDeleted = false`, **no** `videoUnavailable` filter) and `balance.ts:126-132`'s liability rule
(`actualPaidAmount ?? amount`, gross):

| id8 | lifetime earned | paid + locked, gross | held above earnings | cause |
|---|---|---|---|---|
| `cmofpudr` | $1,570.58 | $1,607.33 | **$36.75** | 32 of 34 clips now `videoUnavailable`, $1,462.20 of earnings sits on them, 29 carry `payoutReductionRatio` |
| `cmoaejuc` | $38.80 | $61.89 | **$23.09** | 0 retired, but **5 of 5 approved clips carry `payoutReductionRatio`**, an immutable deliberate cut applied after payment |
| `cmq0qn2l` | $0.00 | $14.46 | **$14.46** | its single clip is now `videoUnavailable` and no longer APPROVED |
| `cmoal818` | $4.94 | $12.76 | **$7.82** | 6 of 13 retired, all remaining earnings sit on retired clips, 9 carry `payoutReductionRatio` |
| **TOTAL** | | | **$82.12** | |

**This reproduces BL-758's "$82.12 across 4 clippers" to the cent, from a clean rebuild.**

**Clipper A is NOT among them, and this is the decisive check.** He holds $399.64 BELOW his earnings,
not above. He appears in an over-held list only if you slice to STRAENGE alone and ignore Panic Baby.

**None of the four is in Clipper A's position, and none should be paid alongside him.** Every one is the
BL-627 mechanism: a clip that funded a correct payment was later **retired or deliberately reduced**, so
the earned side fell after the paid side was fixed. **None is on STRAENGE. None carries the
`tracking.ts:2507` trim signature.** Clipper A is categorically different: all 83 clips live, all
APPROVED, none retired, none reduced, none frozen, every one at its all-time view peak.

There is no clawback here and none is proposed. The population has shrunk over time, not grown: BL-627
measured 5 at $142.59, BL-696 6 at $113.38, BL-719 5 at $82.93, and it now reads **4 at $82.12**.

---

## PART 6 — THE VERDICT

> ## **Clipper A IS genuinely owed the $60.47. Pay him $55.03 by hand today, being the $60.47 less the 9% payout fee it would have carried, and let him request his $399.64 through the platform separately.**

He earned $2,450.63 on STRAENGE and drew $1,894.14. He is not overpaid on any honest reading, and the
$60.47 is exactly the amount a defect at `tracking.ts:2507` removed from his withdrawable balance after
the money had already left the platform. The defect is fixed and live; the campaign really was
oversubscribed by $636.59; the owner already decided in BL-719 to absorb that himself rather than bill
the client. **The three prior reports are right that he is owed. They are wrong only about the amount,
because $60.47 is gross and cash is $55.03.**

The data settles this. Nothing here is a guess and nothing turns on an unverifiable assumption.

### The safe hand-payment procedure

BL-696 established that the platform cannot record a hand payment, so any balance paid outside it stays
claimable and can be requested a second time. **That risk does not apply here, for a specific reason
worth stating: BL-719 reverted the restore, so the $60.47 is NOT sitting in his balance. It is
unwithdrawable. Paying it in cash cannot be double-claimed because there is nothing to claim.**

1. **Do NOT restore the $60.47 to his balance, before or after paying.** Restoring it and then paying by
   hand is exactly the double-pay BL-696 documented, and it would also push STRAENGE $62.18 over its
   $3,000 budget, which is what BL-718 did and BL-719 undid.
2. **Do NOT raise the STRAENGE budget.** The owner already rejected this in BL-719 because it means
   owing the client $100 more on a finished campaign.
3. **Send $55.03** to the wallet on file, outside the platform.
4. **Record it in `docs/OWED-MANUAL-PAYMENTS.md`** as settled, with the date, the amount, and a note
   that it discharges the BL-716 STRAENGE trim in full. The file currently records $60.47 outstanding;
   it should be amended to $55.03 with the fee reasoning, so no future round pays the difference again.
5. **Tell him separately to request his $399.64**, and expect that figure to have grown by the time he
   does. It is ordinary Panic Baby accrual and it is his.
6. **Do not run `agency-monitor --fix`, any restamp, or any re-derive on STRAENGE.** The campaign is
   PAST and frozen; every figure above depends on it staying that way.

### What would change this answer

Nothing in the current data. It would change only if the owner chose strict pro rata over the ratchet,
which would make the hand payment $0.00 and leave him $35.19 above his proportional share. **He has
already chosen otherwise, in BL-719, in writing.** If he wants to revisit that, the number to revisit is
$60.47 versus $0.00 on the STRAENGE slice, and it should be a deliberate reversal rather than a drift.
