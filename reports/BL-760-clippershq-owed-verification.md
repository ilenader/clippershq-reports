# BL-760 — does Clipper A genuinely deserve the $60.47, settled from first principles

**2026-08-10 · DB now() = `2026-08-10 14:07:37.443084+00` · AUDIT ONLY. READ ONLY.**
No code, data, schema, config or money changed. Nothing paid, restored, restamped, re-derived, retired or revived. `agency-monitor --fix` never run. No Apify actor and no paid probe: **spend $0.00.** Base `origin/main` @ `018c22ca`, read-only worktree `C:/b758`, removed at exit. Every timestamp cast `::text` against DB `now()`. The clipper's handle is redacted throughout and no wallet address was selected or printed.

**Clipper A** = user id prefix `cmqez5c2` (`md5` short id `dfb43b`). The owner can map this privately in admin.

---

## THE ANSWER, BEFORE THE WORKING

> **Clipper A is genuinely owed the money. The books are not saying he was overpaid; they are comparing a correct payment against a record that was written down after the payment was made.**
>
> Computed from nothing but his clips, their view histories and his own stamped CPM, **Clipper A earned $2,450.61 on STRAENGE. He was paid $1,894.14. He is $556.47 short of what he actually earned**, not $60.47 over it.
>
> The reason he cannot simply be paid $2,450.61 is legitimate and I confirmed it independently: **STRAENGE's clippers collectively earned $2,642.82 against a clipper pool of $2,000.00, a genuine overshoot of $642.82.** The campaign really was oversubscribed. So the question is not *whether* he earned it, it is *who absorbs the shortfall* — and that is a policy question with two defensible answers, both of which still leave him owed money.
>
> **Pay him $55.03 by hand, not $60.47**, on top of the **$399.64** he must request through the platform himself. The $5.44 difference is the 9% payout fee, which applies to the $60.47 exactly as it would have if the defect had never happened. Paying the full $60.47 in cash overpays him by $5.44.

---

## PART 1 — WHAT HE GENUINELY EARNED, FROM FIRST PRINCIPLES

### The population

Every clip Clipper A has ever had on STRAENGE (`cmqcw7cba001k0pn1e4la5b6d`), with no exclusions:

| | |
|---|---|
| Clips, all time | **83** |
| APPROVED | **80** |
| REJECTED | 3 (all $0.00 stored, all under 1,400 views) |
| `isDeleted` | **0** |
| `videoUnavailable` | **0** |
| Carrying `payoutReductionRatio` | **0** |
| Carrying `earningsFrozenAt` | **0** |
| Carrying `savedEarnings` | **0** |
| `isOwnerOverride` | 3 |
| Distinct clipper CPM stamps | **1** — every clip at exactly `0.5000` |
| Distinct owner CPM stamps | **1** — every clip at exactly `0.2500` |
| First submitted | `2026-06-15 09:32:23.753` |
| Last submitted | `2026-07-15 11:54:25.997` |
| Last touched (any field) | `2026-08-05 13:37:35.466` |
| `clip_stats` rows behind them | **4,572** |

The stamps are not merely uniform, they are **correct**: `0.2500 / 0.5000 = 0.5`, and STRAENGE's `lockedOwnerShareDecimal = 0.33333333` gives `s/(1−s) = 0.5` exactly. There is no BL-539 stamp ambiguity anywhere in this clipper's record.

Campaign parameters used, read from the campaign row rather than assumed: budget **$3,000**, `clipperCpm` **$0.50**, `ownerCpm` **$0.25**, `minViews` **1,000**, `maxPayoutPerClip` **$300**, `pricingModel` CPM_SPLIT, `guaranteeOwnerSplit` true, `platformFeePctDecimal` NULL, `manualSpent` NULL, status PAST, auto-paused `2026-08-01 06:31:33.721`.

### The computation

Applying `calculateClipperEarnings` (`earnings-calc.ts:112-215`) by hand in SQL, clip by clip, from `clip_stats` views and the clip's own stamp: skip if views `< 1000`; `base = min(views/1000 × 0.50, 300)`; `bonus = base × bonusPercent/100`; `earnings = base + bonus`. His `bonusPercent` ranges 0 to 10 across the 80 clips.

| step | amount |
|---|---|
| Total views on his 80 APPROVED clips | **5,403,031** |
| Raw, uncapped, ungated: `5,403,031 / 1000 × $0.50` | **$2,701.52** |
| Less the $300 per-clip cap (1 clip at 1,500,000 views, raw $750) | **−$450.00** |
| Less the 1,000-view gate (7 clips) | **−$2.14** |
| **Base earnings, correctly capped and gated** | **$2,249.38** |
| Plus each clip's own bonus percentage | **+$201.23** |
| **= WHAT HE GENUINELY EARNED** | **$2,450.61** |

That $452.14 of cap-and-gate deduction closes the derivation BL-716 stated but never showed: it reported $2,450.55 without demonstrating how $2,701.52 of raw CPM became it. It is one clip hitting the $300 ceiling and seven clips never reaching 1,000 views, and it reconciles to the cent.

### The comparison the owner asked for

| figure | amount | what it is |
|---|---|---|
| **Genuinely earned, from views × his own stamp** | **$2,450.61** | first principles, this round, independent |
| **Paid to him** | **$1,894.14** | one PAID row, `2026-07-07 16:09:10.717` |
| **What the trim left on the record** | **$1,833.67** | current stored value |
| **What his record says today** | **$1,833.67** | unchanged since `2026-08-05 13:37:35.466` |

**The arithmetic supports $2,450.61 as what he earned, and it supports the payment.** He was paid **$556.47 less** than he earned. There is no reading of the clip data in which $1,894.14 is an overpayment against his own work. The stored $1,833.67 is not an earnings figure at all: it is what survived a pool cap.

This also independently reproduces BL-718's "$2,450.61" to the cent and BL-716's "$2,450.55" to six cents, computed from raw view rows rather than taken from either report.

### The owner's specific worry: was any clip zeroed, retired, revived, deleted or restored?

**No. Not one. This is closed with evidence, and it was the most important thing to check.**

| test | result |
|---|---|
| Clips ever marked `videoUnavailable` | **0 of 83** |
| Clips carrying `savedEarnings` (the retirement stamp) | **0 of 83** |
| Clips `isDeleted` | **0 of 83** |
| Clips whose **current views are below their all-time peak** | **0 of 83** |
| Clips whose views ever fell to 0 after being positive | **0 of 83** |
| Total view-decrease events across all 4,572 stat rows | **8** |
| Largest single decrease | **409 views**, worth **$0.20** |
| Window of every decrease | `2026-06-25 06:10:55.047` to `2026-06-26 05:21:45.141` |
| Clips involved in any decrease | **3**, all fully recovered |

Three clips do show a `0` reading, and I checked each rather than counting them: in all three the zero is the **first** `clip_stats` row, written at the submission instant itself (for example `cmqf0lft50`, submitted `2026-06-15 09:32:23.753`, first read `2026-06-15 09:32:23.789`, 36 milliseconds later, now at 596,700 views). That is a clip being registered before it has views, not a fabricated zero.

**BL-751's zeroing population and BL-748's Instagram fabrication do not touch this clipper.** BL-751's still-zero population is 13 YouTube clips across 5 other clippers, all at $0.00. His clips are Instagram, none was zeroed, and every one of them is at its all-time peak right now. **The "the trim may have been correct at the time and wrong now" hypothesis is dead: his views have only ever gone up.**

This also resolves a live conflict between the two prior reports. **BL-714 stated "zero views ever decreased"; BL-716 stated "8 decreases".** BL-716 is right and BL-714 is wrong: there were exactly 8, all in a 23-hour window in June, all recovered, $0.20 at the largest. Separately, **BL-714 gives his total views as 5,116,424 and BL-716 gives 5,403,031 for the same clipper on the same date.** I measured **5,403,031** on the 80 APPROVED clips (5,406,229 including the 3 REJECTED), so **BL-716's figure is the correct one**, and it matters because that number is the numerator of the pro-rata calculation in PART 3.

---

## PART 2 — WAS THE TRIM ENFORCING A REAL BUDGET CAP, OR WAS IT THE DEFECT?

**It was both, and separating the two is the whole answer.**

### The campaign genuinely was oversubscribed

Computed the same way, independently, for **every clipper on STRAENGE**:

| id8 | clips | recorded now | **genuinely earned** | recorded shortfall | paid |
|---|---|---|---|---|---|
| **`cmqez5c2`** (Clipper A) | 80 | $1,833.67 | **$2,450.61** | $616.94 | $1,894.14 |
| `cmq7qh6p` | 25 | $94.53 | $117.44 | $22.91 | $94.53 |
| `cmqs7gjq` | 10 | $64.84 | $65.33 | $0.49 | $64.84 |
| `cmpfozzs` | 10 | $4.15 | $4.15 | $0.00 | $0.00 |
| `cmr0k3ke` | 1 | $2.37 | $2.37 | $0.00 | $0.00 |
| `cmqxtmu6` | 1 | $0.99 | $1.61 | $0.62 | $0.00 |
| `cmqqm6m9` | 1 | $1.16 | $1.32 | $0.16 | $0.00 |
| 9 more clippers | 28 | $0.00 | $0.00 | — | $0.00 |
| **TOTAL** | **156** | **$2,001.71** | **$2,642.82** | **$641.11** | **$2,053.51** |

The totals are the SQL aggregates. Summing the rounded rows by hand gives $2,642.83 and $641.12, one cent higher in each case; that cent is rounding across 156 clips and nothing else.

| | |
|---|---|
| What STRAENGE's clippers genuinely earned | **$2,642.82** |
| What the clipper pool can pay: `(1 − 0.33333333) × $3,000` | **$2,000.00** |
| **Genuine overshoot** | **$642.82** |

**So yes: the campaign was genuinely overspent on the clipper side, by $642.82, or 32.1% of the pool.** Somebody had to absorb it, and the question really is WHO, not whether. That is a real budget cap doing a real job, and Clipper A is 92.7% of the reason the pool is oversubscribed: his own $2,450.61 alone exceeds the whole $2,000 pool.

### But the pool did not need HIS $60.47, it needed $62.18, and the trim was the wrong instrument

Here is the movement, which I reconstructed from the payout row and the current record:

| moment | Clipper A | all others | pool total | vs $2,000 cap |
|---|---|---|---|---|
| At payment, `2026-07-07 16:01:36` | $1,894.14 | $105.86 | **$2,000.00** | **exactly at cap** |
| Today | **$1,833.67** | **$168.04** | **$2,001.71** | over by $1.71 |
| Counterfactual: had he not been trimmed | $1,894.14 | $168.04 | **$2,062.18** | over by **$62.18** |

Two things follow, and they must not be collapsed into each other.

**The trim was doing necessary work.** Without it the pool would sit $62.18 over its cap today. A cap that lets the pool run 3% over is not a cap. Any claim that "the pool never needed his money" is wrong: it needed $62.18 of trimming and it took $60.47 from him.

**But the trim took it from the one person who had already been paid.** `tracking.ts:2507` read `if (newEarnings > clipperHeadroom) newEarnings = clipperHeadroom`, an absolute assignment with no floor at the clip's stored value, while every sibling branch (`tracking.ts:2236`, `:2271`) has that floor. Because `clipperHeadroom` is derived from *other* clippers' spend, the line does not cap growth, it **moves money sideways between clippers**: A fell $60.47 while the others rose $62.18 in the same window. What was withdrawn from him was not surplus he had yet to receive. It was the exact money that had already left the platform to his wallet on `2026-07-07`, and the campaign was **exactly at cap, not over it**, at the moment that payment was approved.

That is the sense in which BL-716 is right to call it a defect. The pool needed to stop growing; instead the code reached backwards through a completed, correct payment.

### The BL-563 shared gross guard is not involved

`decideOwnerGross` (`owner-share-guard.ts:57-79`) protects the owner side against stamp-versus-share ambiguity. STRAENGE has **zero ambiguous rows**: every clip's stamped ratio is exactly `0.5000`, matching `s/(1−s)` precisely. BL-563's $173.41 concerns three owner-credit clips on the owner's side of the ledger and does not bear on Clipper A's entitlement. **The guard neither blocks nor supports the payment.**

---

## PART 3 — RESOLVING THE CONTRADICTION

The three options, judged against the arithmetic rather than against the prior reports.

### (b) "The trim was correct, he was genuinely overpaid $60.47" — FALSE

This is what the books appear to say and it is the reading the owner is worried about. It is wrong, for a reason that is entirely mechanical: **the "overpayment" is measured against a number that was written down after the payment.** He was paid $1,894.14 when his record read $1,894.14 and the gate at `payouts/route.ts:483` refused anything above it. He earned $2,450.61. A payment of $1,894.14 against $2,450.61 of earned value is not an overpayment by any definition, and paying him more is not a second overpayment.

The "overpaid" reading is also **local to one campaign**. Across his whole account he has earned **$2,293.78** as recorded (or $2,754.72 uncapped) and been paid **$1,894.14**. BL-758 measured the four clippers who hold more than they earned platform-wide, and **Clipper A is not one of them.** The books do not say he was overpaid; a per-campaign slice of them does.

### (c) "Something changed since those reports" — TRUE BUT NOT DECISIVE

Something did change, and it invalidates BL-719's payment figures without touching its conclusion.

| | BL-719, `2026-08-05` | today | change |
|---|---|---|---|
| STRAENGE recorded | $1,833.67 | **$1,833.67** | **unchanged, to the cent** |
| Panic Baby recorded | $405.62 (BL-714) | **$460.11** | **+$54.49** |
| Lifetime recorded | $2,239.29 (BL-714) | **$2,293.78** | +$54.49 |
| What he can request himself | $346.11 | **$399.64** | **+$53.53** |
| Total to receive | $406.58 | **$460.11** | **+$53.53** |

His STRAENGE record has not moved since `2026-08-05 13:37:35.466` and cannot: the campaign is PAST, it carries an era boundary at `2026-08-01 06:25:59.658`, and `tracking.ts:3575` excludes PAST campaigns from the cron entirely. His Panic Baby clips have kept earning. **BL-719's $346.11 and $406.58 are stale by $53.53 and must not be used.** The $60.47 itself has not moved and will not.

### (a) "He genuinely earned it and is owed it" — TRUE, and here is the arithmetic that settles it

The pool is short $642.82. Someone absorbs it. There are exactly two defensible allocation rules and I will give both, because the honest answer is that this is a policy choice and the owner should make it knowingly.

**Rule P, pro rata.** Split the $2,000 pool in proportion to what each clipper actually earned. A's share is `$2,000 × $2,450.61 / $2,642.82` = **$1,854.54**. He was paid $1,894.14, so he sits **$39.60 above** his proportional share.

**Rule R, the ratchet.** Money already recorded and paid is never written down; growth is capped, but nothing already banked is clawed back. A keeps **$1,894.14** and the pool finishes $62.18 over cap, which the owner absorbs.

**The platform has already chosen Rule R, and it is running in production right now.** BL-718 shipped `capButNeverBelowStored` (`earnings-never-decrease.ts:170-186`), which returns `max(proposedCap, stored)`, and it is live at three cap sites: `tracking.ts:2511` (the very line that trimmed him), `tracking.ts:2563`, and `clip-earnings-writer.ts:354` (the L1 chokepoint). BL-719 reverted the *data* repair and the budget raise; it explicitly **kept the code**. Verified at `018c22ca`.

So: **if the identical events happened today, Clipper A would be held at $1,894.14 and the pool would sit $62.18 over cap.** The sole reason his record reads $1,833.67 is that the trim fired in the window `2026-07-07 16:01:36` to `2026-07-17 16:29:02`, before the floor existed. He is not being denied money because the platform decided he was not entitled to it. He is being denied it because of a code path the platform has since fixed and now forbids.

**Both rules still leave him owed money.** This is the finding that removes the risk from the owner's decision:

| rule | his STRAENGE entitlement | + Panic Baby | total entitlement | less paid $1,894.14 | still owed, gross |
|---|---|---|---|---|---|
| **Rule R (ratchet, the shipped rule)** | $1,894.14 | $460.11 | $2,354.25 | | **$460.11** |
| **Rule P (pro rata, the strictest)** | $1,854.54 | $460.11 | $2,314.65 | | **$420.51** |

He can request **$399.64** through the platform under either rule. So the hand payment is **$60.47 gross under Rule R** and **$20.87 gross under Rule P**.

**Under no defensible rule is he owed zero.** The debate is over $39.60, not over $60.47, and the floor of that debate is $20.87. **(a) is true.**

### Why the three prior reports and the books both look right

They are answering different questions and neither is lying. BL-716, BL-718 and BL-719 assert Rule R and are correct that under it he is owed $60.47. The books assert only that `paid > stored` on one campaign, which is arithmetically true and says nothing about entitlement. The contradiction dissolves once you notice **`stored` is not a measure of what he earned.** It is what a cap left behind.

One correction to the prior reports while I am here. **BL-714 calls the $1,894.14 "an overpayment the platform created itself"; BL-716 calls the same payment "correct when it was made".** BL-716 is right. The payment was made when the pool stood at exactly $2,000.00 and his record read $1,894.14; the gate approved it correctly on committed state. Calling it an overpayment is what makes the books look like they contradict the conclusion. Separately, **BL-714 attributed the loss to the `2026-08-01 06:31` run at `tracking.ts:1257`, and BL-716 disproved that** by showing the run wrote $0.00 of earnings platform-wide. BL-714 was wrong by roughly two weeks on cause. Its $60.47 figure survives; its explanation does not.

---

## PART 4 — WHAT HE SHOULD BE PAID TODAY, EXACTLY

### His position, at `2026-08-10 14:07:37.443084+00`

| | |
|---|---|
| **Genuinely earned, first principles** | STRAENGE **$2,450.61** + Panic Baby **$462.98** = **$2,913.59** |
| **Recorded** (what the platform's own books hold) | STRAENGE $1,833.67 + Panic Baby $460.11 = **$2,293.78** |
| **Paid** (gross consumed from balance) | **$1,894.14** |
| **Received on chain** | **$1,647.90** (9% fee $170.47 + 4% EXPRESS $75.77) |
| **Pending payout requests** | **none** — $0.00 locked |
| **Currently withdrawable** (`effectiveCap`) | **$399.64** |
| **Visible but unwithdrawable** | **$60.47** — Panic Baby money the global clamp is consuming to recover the STRAENGE shortfall |
| Per-campaign available on Panic Baby | $460.11 |
| Global available (the binding constraint) | $399.64 |

His Panic Baby money is uncontested and I checked it rather than assuming: his Panic Baby clips earn **$462.98** by first principles against **$460.11** recorded, so his record there is $2.87 **under** what he earned, not inflated. Panic Baby's clipper pool is not breached (live spend $1,987.29 against a $2,000 cap). **There is no second pool dispute hiding underneath the first.**

### BL-719's two figures, verified against today

**Both are stale and both are too low.** BL-719 recorded "request $346.11, pay $406.58". Today the correct pair is **request $399.64, pay $460.11**, because his Panic Baby clips earned another $54.49 in the five days since. Using BL-719's numbers would underpay him by $53.53.

### The fee, which is where a naive payment goes wrong

Clipper A is **not referred** (`referredById` is null, and his PAID row is stamped `feePercent = 9`), so the standard **9%** applies. This matters more than it looks.

**The $60.47 is a GROSS balance figure, not a cash figure.** It is the amount of *balance* the clamp is withholding. Had the defect never happened, that balance would have gone out through the normal flow and the platform would have taken 9% of it, exactly as it took 9% of everything else he has ever withdrawn.

| | counterfactual: defect never happened | actual: request $399.64 + hand payment |
|---|---|---|
| Gross requested | $460.11 | $399.64 |
| 9% fee | $41.41 | $35.97 |
| Net sent on chain | **$418.70** | $363.67 |
| Hand payment needed to match | | **$55.03** |
| **Total he receives** | **$418.70** | **$418.70** |

`$60.47 × 0.91 = $55.03`, and `$363.67 + $55.03 = $418.70` exactly. **Paying the full $60.47 in cash gives him $424.14, which is $5.44 more than he would ever have received had the defect not occurred.** That is a real overpayment, small but of exactly the kind the owner said he cannot claw back.

If he chooses EXPRESS, as he has on all three of his requests, the total deduction is 13% and the hand payment becomes **$60.47 × 0.87 = $52.61** (counterfactual net $400.30, request net $347.69).

### The single number to send

> **Ask him to request $399.64 on Panic Baby at STANDARD speed. Pay him $399.64 through the platform, then send $55.03 by hand. He receives $418.70 in total, which is to the cent what he would have received if the trim had never touched him.**

If the owner prefers to absorb the fee on the corrective portion as a goodwill gesture, the figure is **$60.47** and he receives **$424.14**. That is a deliberate $5.44 gift, not a correction, and it should be recorded as such. **My recommendation is $55.03**, because the brief is explicit that overpaying is worse than underpaying and $55.03 is the number that makes him exactly whole.

---

## PART 5 — THE OTHER FOUR

**Clipper A is NOT among BL-758's four clippers holding $82.12 above their earnings.** I re-verified this rather than citing it: his lifetime recorded earnings are $2,293.78 against $1,894.14 paid, so he is $399.64 *under*, not over. His excess exists only inside one campaign.

Each of the four, computed the same way, from views × stamped CPM:

| id8 | campaign | clips | retired | PRR clips | recorded | **earned (views × stamp)** | paid | excess | **cause** |
|---|---|---|---|---|---|---|---|---|---|
| `cmofpudr` | somesome | 30 | **28** | 29 | $1,570.58 | $2,175.63 | $1,607.33 | $36.75 | **Retirement.** His clips went dark after he was paid. Under the owner's stated policy a deleted video cannot be paid for, so his record fell below a payment that was correct when made. |
| `cmoaejuc` | somesome | 5 | 0 | **5 of 5** | $38.80 | $80.24 | $61.89 | $23.09 | **`payoutReductionRatio` 0.8317.** A deliberate, immutable 16.83% owner cut applied after payment. Not a defect. |
| `cmq0qn2l` | GainzAlgo (REPOST) | **0** | 0 | 0 | $0.00 | $0.00 | $14.46 | $14.46 | **No clips at all.** Every clip that justified his payment was rejected or removed afterwards. A genuine historical overpayment. |
| `cmoal818` | somesome | 9 | **5** | **9 of 9** | $4.94 | $10.52 | $12.76 | $7.82 | **Retirement plus PRR.** After the 0.8317 ratio his entitlement is about $8.75 against $12.76 paid, so he is the only one genuinely paid above what he earned. |

**None of the four shares Clipper A's signature, and the owner can pay him without creating an obligation to any of them.** A's signature is unique and every element of it is checkable: **zero retired clips, zero PRR clips, zero deleted clips, zero view decreases, every clip at its all-time peak**, and a raw entitlement ($2,450.61) that exceeds what he was paid by $556.47. His record was reduced by a **pool cap** alone. The other four were reduced by **deleted videos** (`cmofpudr`, `cmoal818`), by a **deliberate owner ratio** (`cmoaejuc`, `cmoal818`), or by **losing every clip** (`cmq0qn2l`) — three causes the owner chose or the policy requires, none of them a defect.

Two of the four do sit below their raw entitlement (`cmofpudr` by $568.30, `cmoaejuc` by $18.35), and I will not pretend otherwise. But those gaps are the deleted-video policy and the immutable `payoutReductionRatio` doing what they were built to do, on money the owner deliberately withheld. They are not the same claim and paying A does not open them.

---

## PART 6 — THE VERDICT

> **YES: Clipper A is genuinely owed the money, because he earned $2,450.61 on STRAENGE and was paid $1,894.14, and pay him $55.03 by hand on top of the $399.64 he must request himself, being $60.47 of withheld balance less the 9% fee he would have paid on it anyway.**

Three prior reports said he is owed $60.47 and they were right about the entitlement and wrong only about the fee. The books never said he was overpaid; they said `paid > stored` on one campaign, which is true and is not the same thing. **The data settles this. I am not guessing and I do not need anything further.**

The one honest caveat, stated because the owner should know it rather than because it changes the answer: the $60.47 rests on the **ratchet** rule, which is the rule the platform's own live code now enforces at three cap sites. Under the strictest alternative, a pro-rata split of the oversubscribed pool, the figure would be **$20.87 gross / $18.99 net** instead. **The range of defensible answers is $18.99 to $55.03 net. Zero is not in it.** I recommend $55.03 because `capButNeverBelowStored` is shipped, live and unambiguous about which rule this platform follows, and because the alternative charges a clipper for a defect the platform introduced and has since fixed.

Where the money comes from should also be said plainly: **STRAENGE's budget cannot cover it.** Restoring the record would put the campaign at $3,088.99 against a $3,000 budget, which is exactly why BL-718 had to raise the budget and why BL-719 reverted it. The $55.03 is the owner absorbing, out of pocket, the gap between what STRAENGE's clippers earned ($2,642.82) and what its clipper pool could pay ($2,000.00). It is not a budget operation and it breaches nothing.

### The safe payment procedure

BL-696 established, and BL-758 re-verified at `018c22ca`, that **no admin route can create a payout row**: `payoutRequest.create` exists at exactly three sites, none under `src/app/api/admin/`. A hand payment therefore leaves no trace, his displayed balance does not fall, and the same money stays claimable. **Order matters and must not be varied.**

1. **Ask him to raise the payout request in the platform first**, on Panic Baby, at **STANDARD** speed, for the full amount the gate offers. It reads **$399.64** today; **recompute at the moment of payment, never from this report.** His Panic Baby clips are still earning and the figure will have grown.
2. **Pay the requested amount through the normal flow** and **mark that row PAID through the review path**, so `paidAt` is stamped and `isPayoutMoneyOut` (`balance.ts:117-124`) counts the full gross against his balance. This is the step that makes the money stop being claimable.
3. **Only then send the $55.03 separately, by hand.** Never before, and never bundled into the row's amount: inflating the row would consume Panic Baby budget for money that is not Panic Baby earnings.
4. **Strike the entry in `docs/OWED-MANUAL-PAYMENTS.md`** with the settlement date, the payout row id and the amount actually sent, noting that $55.03 was paid net of the 9% fee against a $60.47 gross entitlement so a future round does not read it as a $5.44 shortfall.
5. **Do not pay the $55.03 first.** It is invisible to every balance calculation, his displayed balance will not fall, and he can request it again next month. That is BL-696's scenario 4 and it is the one failure mode this platform cannot defend against.

If the owner wants a durable fix rather than a repeat of this round, BL-758's fix 2 is the answer: an OWNER-only `POST /api/admin/payouts/manual` that records a hand payment as a real PAID row. Until it exists, every correction like this one is a hand payment that the platform cannot see.

---

## WHAT COULD NOT BE MEASURED

• **The exact moment the $60.47 was written off.** No earnings-history table exists and `savedEarnings` is null on all 83 clips, so the loss can only be bounded to the window `2026-07-07 16:01:36` to `2026-07-17 16:29:02`. This does not affect the entitlement, which is computed from current views.
• **Whether he requested his full maximum on `2026-07-07`.** The gate refuses anything above the per-campaign available, so $1,894.14 is a proven **floor** on what his record held at `16:01:36`, not necessarily the exact value. If he asked for less than his maximum, his true entitlement was higher and he is owed more, never less.
• **Which allocation rule the owner intends.** This is a decision, not a measurement. Both are priced above.

---

## VERIFICATION

Read-only throughout, including the one subagent used, which held WebFetch only and no database or write access. **One subagent conclusion was rejected rather than repeated:** it reported that "the pool never needed his $60.47 to stay under cap" because the pool ended $1.71 over. That is wrong, and the counterfactual proves it: without the trim the pool would stand at $2,062.18, or $62.18 over cap. The trim was doing necessary work; its defect was taking the money from a completed payment rather than from future growth. **Two conflicts between prior reports were resolved against live data rather than averaged:** BL-714's "zero views ever decreased" versus BL-716's "8 decreases" (BL-716 correct: 8 events, largest 409 views, all recovered), and BL-714's 5,116,424 views versus BL-716's 5,403,031 (BL-716 correct, and it is the numerator of the pro-rata figure).

Every figure was computed independently from `clips`, `clip_stats` and `cpmAtSubmissionDecimal`, applying `earnings-calc.ts`'s own formula in SQL, and no stored total or prior report's conclusion was taken on trust. The independent entitlement reproduces BL-718's $2,450.61 to the cent and BL-716's $2,642.78 campaign total to four cents, from raw view rows. Timestamps cast `::text` against DB `now()`. Handle redacted, no wallet address selected or printed. No build was run and none is claimed: this round changed no TypeScript.

**Nothing was changed. 83 clips, 3 payout rows, one campaign and $1,833.67 of recorded earnings are exactly as they were found.**
