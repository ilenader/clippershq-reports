# BL-822 — every number on his screen is right, and the one that would help him is $8.60 the platform will not let him take

**2026-08-24 · DB `now()` = `2026-08-24 13:20:39.025217+00` (first read) to `13:27:56.173044+00` (last) · AUDIT ONLY. READ ONLY.**
No code, data, schema, config or money changed. Nobody paid, no status touched, no balance moved, no payout created, altered, approved or cancelled. Every database access through `scripts/run-select.js`, which refuses a write keyword before it connects. Every timestamp cast `::text` against DB `now()`. Base `origin/main` @ `4ea1c139`, isolated worktree `C:/w822`, a short path, `node_modules` never junctioned, removed at the end. **No Apify actor and no paid probe of any kind: spend for this round is $0.00.**

The clipper is **Clipper A** throughout: id prefix **`cmpl310f`**, `md5` short id **`91a758`**, so the owner can map him privately in admin. His handle is redacted and no wallet address was selected or printed.

> **THE ARITHMETIC IS CORRECT AND I PROVED IT RATHER THAN ASSUMED IT.** Recomputed from his clips, their peak views and each clip's OWN stamped CPM, ignoring every stored total: **$92.14 payable and $8.60 retired, a difference of $0.00 against what is stored**, on 255 approved clips. All six displayed figures reconcile to the cent.
>
> **BUT HE IS OWED MORE THAN THE SCREEN SHOWS. The withdrawal gate would allow him $59.15 today; the screen says $50.55 and the client refuses anything above it.** The gap is **exactly $8.60**, the same $8.60 the page names in its own note, because the gate and the display compute the global clamp from **different bases**.
>
> **And the $41.59 he was paid was for work whose record has since been erased.** 23 of those clips were REJECTED on `2026-08-19` with the reason **"Video not found"**, eighteen days AFTER he was paid for them. They recompute to $46.83. So $41.59 of his current earnings on a different campaign is quietly funding old work, while the same screen promises him *"Money you were already paid stays yours."*

---

## PART 1 — ALL SIX FIGURES, RECONCILED TO THE CENT

### Each figure, traced to the query and the line that produces it

| on his screen | value | what it is | produced by |
|---|---|---|---|
| **Available for payout** | **$50.55** | `computeBalance(payableClips).available` | `balance.ts:200`, `max(approvedEarnings − paidOut − lockedInPayouts, 0)`, fed the retired-filtered array at **`earnings/route.ts:209-210`** |
| **Counted** | **$92.14** | period earnings excluding clips that no longer count | `summary.totalEarned`, **`earnings/page.tsx:157-201`** (BL-818) |
| **of $100.74 earned** | **$100.74** | the same total before the exclusion | `earnedBeforeExclusion`, **`EarningsPremium.tsx:69`** |
| **Approved** | **$92.14** | period approved, same exclusion | `summary.approvedEarnings`, same memo |
| **Paid out, before fees** | **$41.59** | the **GROSS** that came off his balance | `computeBalance.paidOut`, **`balance.ts:192-195`**, summing `clipperLiability` = `actualPaidAmount ?? amount`, **`balance.ts:126-132`** |
| **$8.60 not counted** | **$8.60** | the delta between the two balances | `unavailableClips.removedFromBalance`, **`earnings/route.ts:226`**, rendered at `EarningsPremium.tsx:264` |

Reproduced in SQL at `db_now = 2026-08-24 13:25:07.336458+00`:

```
lifetime approved, incl. retired   100.74
payable approved                    92.14
retired, excluded                    8.60
paid gross                          41.59
locked                               0.00
display available  (92.14 - 41.59)  50.55
```

### Computed independently, from views and each clip's own stamped CPM

Not read off a stored total. `calculateClipperEarnings` (`earnings-calc.ts:112-212`) applied by hand in SQL, on **peak** views because earnings ratchet and never decrease:

```
views < minViewsAtApproval                          -> 0
base  = min(peak_views / 1000 x own stamped CPM, maxPayoutPerClipAtApproval)   cap on BASE only
bonus = base x own bonusPercent / 100
earned = round2(base) + round2(bonus)
```

| his SomeSome App clips | clips | stored | **recomputed independently** | **difference** | holding more than supported |
|---|---|---|---|---|---|
| APPROVED, payable | 234 | $92.14 | **$92.14** | **$0.00** | **0** |
| APPROVED, retired | 21 | $8.60 | **$8.60** | **$0.00** | **0** |
| **approved total** | **255** | **$100.74** | **$100.74** | **$0.00** | **0** |
| PENDING | 18 | $0.00 | *would be $5.68* | | |
| REJECTED | 46 | $0.00 | *would be $16.83* | | |

Two distinct stamped CPMs across his approved clips, no clip carries a `payoutReductionRatio`, and **not one clip holds more than its own views and rate support.** The pending and rejected rows are correctly $0.00.

**`273 clips` in the brief is exactly right and worth naming:** it is his APPROVED plus PENDING count on SomeSome App, 255 + 18. He has 319 in total there, 46 of them rejected.

### The $8.60 exclusion names real clips, and the subtraction closes

**21 real approved clips carrying $8.60**, every one `videoUnavailable = true`, stamped `2026-07-18 19:09:41.778551` and `19:10:11.545056`. The subtraction closes exactly:

> **$100.74 − $8.60 = $92.14.** ✓

This is BL-818's own tile doing precisely what it shipped to do, and BL-819 independently listed this clipper at `$8.60 gross, $7.83 cash` in its retired-video table. **Three separate measurements agree.**

### Is $92.14 − $41.59 = $50.55 the real derivation, or a coincidence?

**It is the real derivation.** `computeBalance` at `balance.ts:200` is literally `approvedEarnings − paidOut − lockedInPayouts`, floored at zero, and his locked is $0.00. It is not two unrelated figures that happen to subtract.

**But the two operands come from different campaigns, and that is the whole story of this round.**

| | where it comes from |
|---|---|
| the **$92.14** | **entirely SomeSome App**, ACTIVE, 255 approved clips, $0.00 ever paid on it |
| the **$41.59** | **entirely somesome ($25.54) and Panic Baby ($16.05)**, both PAST, both now holding $0.00 of recorded earnings |

`computeBalance` is a single account-wide subtraction, so **money he was paid for old work on two finished campaigns is being deducted from new work on a third.** That is by design (BL-140: the clipper consumes the full gross from their claimable balance) and it is invisible on screen.

---

## PART 2 — THE FIGURE MOST LIKELY TO BE WRONG, AND WHAT HE ACTUALLY RECEIVED

### $41.59 is the GROSS. He received $37.21 in cash.

Both payout rows, field by field:

| payout | campaign | gross | fee % | platform fee | express % | express fee | **cash received** | paid at (`::text`) |
|---|---|---|---|---|---|---|---|---|
| `cmq5jtla` | somesome | $25.54 | **9** | $2.30 | none | none | **$23.24** | `2026-06-24 16:09:02.602` |
| `cms8shrg` | Panic Baby | $16.05 | **9** | $1.44 | **4** | **$0.64** | **$13.97** | `2026-08-01 12:01:18.695` |
| | **total** | **$41.59** | | **$3.74** | | **$0.64** | **$37.21** | |

**He is NOT referred**, so the standard 9% applies and not BL-812's reduced 4%; `feePercent = 9` is stored on both rows, and `referredById` is null on his user row. **BL-763's 4% express premium IS present**, on the Panic Baby payout, which is exactly the fee BL-732 missed and BL-763 caught.

> **STATED PLAINLY: the screen says $41.59 came off his balance. $37.21 reached his wallet. The difference is $4.38 of fees.**

**So yes, that is part of the misunderstanding, and it is arithmetically real.** His available balance is computed correctly against the **gross** $41.59, because gross is what leaves a balance, while he is mentally comparing it against the **$37.21** that landed. A clipper doing his own sum from what he received would expect $92.14 − $37.21 = $54.93 and find $50.55, a $4.38 shortfall he cannot explain.

### BL-813's fix IS live for him

His screen reads **"paid out before fees"**. That string was shipped by BL-813 and is at **`EarningsPremium.tsx:361`**, `label: "Paid out, before fees"`. Before BL-813 the same tile read a bare **"Paid out"** over the same gross figure.

**So the screenshot POSTDATES the BL-813 redeploy, and BL-818's is live too**, proven by the same method: the **"Counted"** tile with its **"of $100.74 earned"** sub-line is BL-818's, at `EarningsPremium.tsx:358` and `:368-370`, and the **$8.60** note is at `:264`. **All three fixes are on his screen.** The label is honest; the figure beneath it is still the gross, which BL-813 deliberately chose over changing the number.

---

## PART 3 — HIS TRUE POSITION

| | gross | cash |
|---|---|---|
| lifetime approved earnings, including retired clips | **$100.74** | |
| payable approved earnings | **$92.14** | |
| excluded because the video is gone | $8.60 | |
| **paid to date** | **$41.59** | **$37.21** |
| locked in a pending request | **$0.00** | $0.00 |
| below a campaign minimum | **$0.00** | |
| **withdrawable through the app today** | **$50.55** | **$46.00** after the 9% fee |
| **withdrawable at the server gate** | **$59.15** | **$53.83** after the 9% fee |

**Nothing is below a minimum.** SomeSome App carries a **$15.00** minimum (the owner's own raise) and his $50.55 clears it, so his row is `ready` and the request button is enabled.

**Nothing is locked.** He has no open payout request.

**The global clamp IS binding, and it binds at two different values.** His per-campaign availability on SomeSome App is the full **$92.14** (`payouts/route.ts:362` and `:524`, payable base). What limits him is `effectiveCap = min(perCampaign, globalAvailable)` at `payouts/route.ts:689`:

| | base used | global available | effective cap |
|---|---|---|---|
| **the withdrawal gate** | **lifetime**, `status: "APPROVED"` with **deliberately NO `videoUnavailable` filter** (`payouts/route.ts:666-668`) | **$59.15** | **$59.15** |
| **the screen** | **payable**, `payableClips` filtered at `earnings/route.ts:209` | **$50.55** | **$50.55** |
| | | | **gap $8.60** |

**The $8.60 the note names is exactly the amount the gate would release and the screen will not.** `removedFromBalance` at `earnings/route.ts:226` is literally `balanceBefore.available − balance.available`, which is `59.15 − 50.55`. The figure printed to explain the exclusion IS the size of the discrepancy.

**And he cannot reach it, because the client refuses first.** `payouts/page.tsx:289` returns *"Amount exceeds available balance"* and `PayoutRequestFlow.tsx:331` returns *"That is more than your $50.55 available"*, both comparing against the clamped display figure. So the server would accept $59.15 and the browser will not send it.

**A stale comment worth reporting.** `payouts/route.ts:655-662` justifies the lifetime base by saying *"the balance on /earnings comes from computeBalance over a clips query that has NO `videoUnavailable` filter, so the DISPLAYED global balance has always used this lifetime base."* That was true when BL-692 wrote it. **BL-698 changed it**, and the comment has been wrong ever since. BL-765 recorded the resulting asymmetry and routed around it rather than closing it; this is what it costs one clipper.

### The campaign-status question, and a correction to the brief

**No campaign status touches his balance, and that is verified rather than assumed.** `grep -c` for any campaign-status reference in `payouts/route.ts` returns **0**, and BL-641 recorded the same for `api/earnings` and `balance.ts`: *"Balances / withdrawals: Zero references to campaign status."*

**And the campaign BL-641 moved to PAST is `somesome`, not `SomeSome App`.** They are two different campaigns and the distinction matters here:

| campaign | status | his clips | his balance |
|---|---|---|---|
| **SomeSome App** | **ACTIVE**, min payout **$15.00** | 319, of which 273 not rejected | **$92.14** |
| `somesome` | PAST | 28, all now $0.00 | $0.00, and $25.54 paid |

**His 273 clips are on the ACTIVE campaign.** The PAST one holds nothing. BL-641's 100 percent display affects what he sees on `/campaigns` and not one figure on his earnings screen.

### What actually removed the $41.59 from his record

This is the part no screen shows and it is the substance of his complaint.

| campaign | paid | when paid | what happened to the clips | when | their record now |
|---|---|---|---|---|---|
| somesome | $25.54 | `2026-06-24` | 7 approved clips **retired**, earnings zeroed | `2026-07-18 19:09` | **$0.00** |
| Panic Baby | $16.05 | `2026-08-01` | 8 clips **REJECTED**, reason **"Video not found"** | **`2026-08-19 14:55`** | **$0.00** |

**The Panic Baby clips were rejected eighteen days AFTER he was paid for them, and the stated reason is that the video is missing, not that the work was bad.** A bulk sweep on `2026-08-19` between `14:55:00.052` and `15:07:47.111` rejected **23 of his clips** across the two campaigns, 20 of them with the exact reason **"Video not found"** and 3 with **"Video not found — manual review needed"**. Every one of them already carried `videoUnavailable = true`.

**Recomputed from their own views and stamped CPMs, those 29 rejected clips are worth $46.83.** He was paid $41.59 gross against them, which is less than they supported, so **the payment was correct when it was made.**

> **So the entire $41.59 is now being charged against earnings that did not fund it**, and the reason his old earnings vanished is the same reason BL-698 exists: the videos are gone.
>
> **The screen's own note says *"Money you were already paid stays yours."* The arithmetic underneath it takes $41.59 of that money back out of his new work.** Those two statements cannot both be true, and they sit four inches apart.

**Stated fairly: this is not a formula bug.** BL-627's no-overpayment property requires that a clipper cannot draw more, lifetime, than they lifetime-earned, and BL-758 measured 4 clippers already clamped to $0.00 by it holding $82.12 (re-measured today: **still exactly 4 clippers and $82.12**). For those four the offset is invisible, because they have nothing new to take it from. **Clipper A is what it looks like when the clipper earns again: it becomes a real, silent deduction.**

### ONE LINE

> **He can withdraw $50.55 through the app today, which is $46.00 in cash; the server gate would allow $59.15, so the screen and the client understate his position by exactly $8.60, and no part of the remaining $41.59 is reachable because it was already paid to him in June and August.**

---

## PART 4 — HOW MANY OTHERS SEE THIS

Measured at `db_now = 2026-08-24 13:26:09.987781+00`, reproducing what the earnings page actually renders.

### BL-817's metric, re-measured, and what BL-818 moved

| | rows | clippers | absolute gap |
|---|---|---|---|
| **BL-817, 2026-08-23** | 40 | 27 | $2,908.06 |
| **the same metric today** | **39** | **27** | **$2,869.10** |
| **the metric BL-818 actually changed** (the COUNTED figure the row now shows, against the balance) | **31** | **23** | **$2,792.96** |
| **BL-818's reduction** | **8 rows** | **4 clippers** | **$76.14** |

**BL-818 fixed its own cause and nothing more, which is exactly what it claimed.** It predicted it would "fully reconcile 9 rows worth $46.65"; measured a day later across ordinary drift it removed 8 rows and $76.14. **The residual is not what BL-818 was for.**

### The residual is almost entirely already-paid money, which is Clipper A's cause

**29 of the 31 remaining rows disagree because money was already paid or is locked**, carrying **$2,995.23**. That is 94% of the rows and it is the cause nothing on screen explains.

### The wider population

| | clippers | dollars |
|---|---|---|
| clippers with current earnings AND a past payment | **51** | **$8,849.69** of gross silently offsetting |
| of those, still holding a positive withdrawable balance | **37** | |
| **clippers the gate would allow MORE than the screen shows** | **24** | **$274.12**, largest single gap **$65.24** |
| clippers paid above lifetime earned, clamped to $0.00 | 4 | $82.12 |

> **So this is not one man's confusion. 51 clippers have a past payment quietly reducing a balance they earned somewhere else, and 24 clippers are being shown less than the platform itself would pay them.**

The 4 clippers at $82.12 reproduce BL-758's figure to the cent, fourteen days later, which is a useful check that this measurement and that one agree.

---

## PART 5 — WHAT THE SCREEN FAILS TO SAY

**The page performs the subtraction and never names it.** Searched for any rendered string relating the paid figure to the available figure: the only three matches for *"already been paid"*, *"comes off"*, *"minus"* or *"less "* in `EarningsPremium.tsx` are at lines **168, 285 and 477**, and **all three are code comments.** Not one is a string a clipper can read.

What he actually sees, in order down the page:

> **Available for payout** · **$50.55** · *All time balance*
> *$8.60 of your earnings is not counted in this balance, because those clips are no longer earning. Money you were already paid stays yours. Your other clips keep earning as normal.*
>
> **COUNTED** $92.14 · *of $100.74 earned* — **APPROVED** $92.14 — **PAID OUT, BEFORE FEES** $41.59

**BL-818 made one subtraction close on screen and this is a different one.** BL-818's line answers *"why is counted lower than earned"*: `$100.74 earned, $8.60 of it on 21 clips that are no longer earning`. **Nothing answers "why is available lower than counted", and that step is $41.59, nearly five times larger than the one that is explained.**

The three tiles sit side by side and invite exactly the wrong reading: `Counted $92.14`, `Approved $92.14`, `Paid out $41.59`, with `$50.55` in the hero above them. **Every ingredient of the sum is on screen and the sum itself is not.** A clipper who can see $92.14 and $41.59 and $50.55 and is never told they are one sentence will do what this one did.

> **NAMED AS THE DEFECT: the display fails to explain itself, and that is true regardless of the arithmetic being right.** It is the identical shape to BL-817 and BL-762, both of which happened for the same reason, and it is the third time.

**And it is worse than silent here, because the page makes a promise the arithmetic breaks.** The note says *"Money you were already paid stays yours"* six lines above a figure that has had $41.59 of already-paid money removed from it, $41.59 that was earned on clips the platform has since erased.

---

## PART 6 — THE VERDICT, THE REPLY, AND THE FIX SPEC

> **ONE LINE: he is owed $8.60 more than his screen shows and the app will not let him take it; every other number is correct, and the $41.59 he cannot see is money already in his wallet since June and August.**

### The reply the owner can send him

> Hey, thanks for writing in and sorry it looked wrong. Every number on that screen is real, but the page never shows you how they join up, so here it is.
>
> **You have earned $100.74 on SomeSome App.** That is your 255 approved clips, and I checked every one of them against its own views and its own rate.
>
> **$8.60 of that is on 21 clips whose videos are no longer reachable**, so the platform stops counting them. That leaves **$92.14**, which is the "Counted" figure.
>
> **You have already been paid $41.59 of your earnings**, in two payouts: **$25.54** in June and **$16.05** on the 1st of August. Those came off your balance, which is why what is left to take is **$92.14 minus $41.59, or $50.55**. That step is not written anywhere on the page and it should be. That is on us.
>
> One thing worth knowing, because the wording is confusing: the **$41.59** is the amount before fees. What actually reached your wallet was **$37.21**, after the 9% platform fee and a 4% express fee on the August one because you chose express. If you were doing the sum from what you received, you would be about $4.38 out, and that is why.
>
> **You can request a payout right now.** $50.55 is above the $15.00 minimum on SomeSome App. After the 9% fee that comes to about **$46.00**.
>
> **And you are right that something is short.** There is a gap of exactly **$8.60** between what the page offers you and what our own payout check would allow, caused by the two counting those retired clips differently. I am fixing that. If you want the $8.60 now, tell me and I will handle it by hand.

Threshold and mechanism only, no judgement, nothing implying he did anything wrong, and it does not invite a retry that would fail. BL-518 and BL-521.

### The fix spec, and NEITHER was performed

**A. A GENUINE CALCULATION DEFECT. There is one, and it is worth $274.12 across 24 clippers.**

The gate and the display compute the global clamp from different bases, so the platform shows a smaller number than it would honour.

| # | site | file:line | change |
|---|---|---|---|
| **A1** | the two bases | **`payouts/route.ts:666-668`** against **`earnings/route.ts:209`** | pick ONE. The gate uses lifetime (`status: "APPROVED"`, no `videoUnavailable` filter); the display uses payable. **They must not differ**, and whichever is chosen the other has to follow in the same commit. |
| **A2** | the stale justification | **`payouts/route.ts:655-662`** | its comment asserts the display already uses the lifetime base. BL-698 made that false and it has misled every reader since, including BL-765, which routed around the asymmetry rather than closing it. |
| **A3** | the client ceiling | `payouts/page.tsx:289`, `PayoutRequestFlow.tsx:331` | both refuse above the display figure, so today the client is the real limit and the server's answer never gets tested. Whatever A1 decides, this must read the same number. |

**Which base is right is a MONEY decision and not mine to take.** Lifetime pays a clipper for a video that is gone, which contradicts the owner's stated policy. Payable is stricter and is what the screen already shows. **The one option that is definitely wrong is leaving them different.** This needs its own round, with the 24 clippers and the $274.12 measured before and after.

**B. A DISPLAY THAT FAILS TO EXPLAIN ITSELF. This is the higher-value fix.**

| # | site | file:line | change |
|---|---|---|---|
| **B1** | the hero | `EarningsPremium.tsx:220-230` | under `$50.55`, one line closing the subtraction the page already has every part of: **`$92.14 counted, less $41.59 you have already been paid.`** It needs no new data: `summary.paidOut` and `summary.approvedEarnings` are both in the same component. |
| **B2** | the paid tile | `EarningsPremium.tsx:361` | it says `Paid out, before fees` and never says what the fees were. Add the cash beneath it the way BL-818 added `of $X earned`: **`$37.21 reached you`**. `finalAmount` is already on every payout row, so this is a read, not a computation. |
| **B3** | the spoken sentence | the hero has none | every figure in the hero is visible-only. The subtraction must be said once for a screen reader, in the same clause order as B1. |
| **B4** | the contradiction | `EarningsPremium.tsx:264` | *"Money you were already paid stays yours"* sits above a balance that has $41.59 of already-paid money removed. Once B1 ships, the sentence stops reading as a contradiction, because the reader can see where it went. **B1 must land before or with B2, or B2 makes it worse.** |

**Higher value: B1.** It is one sentence, needs no new query, no schema change and no money decision, and it closes the exact gap that produced this ticket, BL-817's and BL-762's. **A is worth $274.12 and needs a policy call; B is worth not having this conversation a fourth time.**

**Neither was performed. This round changed nothing.**

---

## WHAT COULD NOT BE MEASURED

* **What his somesome and Panic Baby clips were worth at the moment he was paid.** Earnings are overwritten in place and rejected clips are zeroed, so no historical figure survives. The $46.83 is a reconstruction from each clip's peak views and its own stamped CPM, which is a lower bound on what was there in June and August and is labelled as a reconstruction rather than a reading.
* **Whether the 23 "Video not found" rejections on 2026-08-19 were the owner's judgement or a sweep.** The reason string is identical across 20 of them inside thirteen minutes, which reads as a sweep, but the audit trail was not opened; that is its own question and it was not this round's.
* **Whether he would actually be paid $59.15 if the client allowed it.** The gate's arithmetic is read from source and reproduced in SQL, not exercised, because exercising it would create a real payout request.
* **No browser render was performed.** The figures quoted as "his screen" are derived from live database values passed through the same functions the shipped components call, and from reading those components line by line. It is a derivation, not a photograph, and it should be read as one.
* **No build was run and none is claimed.** This round changed one markdown file in the reports repository and cannot affect `tsc` or `next build`.

---

## ACCESSIBILITY

**No UI code was written or edited.** This is an audit and its only artefact is this document, so there is no component, markup or user-facing string to review. Two presentation defects are nonetheless reported above and belong to whichever round performs the fix: the hero carries no spoken sentence for any of its figures (B3), and the three stat tiles present the ingredients of a subtraction with no programmatic or visible relationship between them (B1).

---

## VERIFICATION

Read only throughout: no code, data, config or money changed, nobody paid, no status or balance touched, and every read through `scripts/run-select.js`. All six displayed figures are reconciled to the cent and traced to the query and file:line that produce them, and his earnings are recomputed **independently** from clips, peak views and each clip's own stamped CPM at **$92.14 payable and $8.60 retired against $92.14 and $8.60 stored, a difference of $0.00 on 255 clips with 0 holding more than their own views support**. `$100.74 − $8.60 = $92.14` and `$92.14 − $41.59 = $50.55` are both confirmed, and the second is shown to be the real derivation at `balance.ts:200` rather than a coincidence, while naming that its two operands come from different campaigns. The $8.60 exclusion is traced to 21 real clips retired on `2026-07-18`. **Both gross and cash are stated for every figure**: paid $41.59 gross against **$37.21 cash**, fees itemised at $2.30, $1.44 and BL-763's $0.64 express premium, with `feePercent = 9` read off both rows and `referredById` null. **BL-813's and BL-818's fixes are proven LIVE for him** by the shipped label strings at `EarningsPremium.tsx:358`, `:361` and `:264`. His true position is stated in full including the finding that **the gate would allow $59.15 against the screen's $50.55, a gap of exactly $8.60**, that the client refuses it first, and that no campaign status touches any of it, correcting the brief's premise that his campaign is PAST. The population is re-measured against BL-817's 27 clippers and $2,908.06, showing BL-818 removed 8 rows, 4 clippers and $76.14 and that **29 of the 31 remaining rows are already-paid money**, alongside 51 clippers carrying $8,849.69 of silent offset and 24 clippers shown less than the gate allows. The unexplaining display is named as the defect with the proof that all three near-matching strings are code comments. The verdict is one line, the reply is plain and non-accusatory, and the fix spec separates a real calculation defect worth $274.12 from a display that fails to explain itself, names B1 as the higher-value fix, and **performs neither**. Every timestamp cast `::text` against DB `now()`; the earnings invariant is **0 violations**, payout rows **190** with the newest `updatedAt` at `2026-08-24 05:08:22.794`, eight hours before this round's first read. Handle redacted, no wallet address printed, spend $0.00, no Apify actor. The worktree at `C:/w822` is removed. **No dashes as bullets.**
