# BL-810 — one place that answers what he owes and what is still up for grabs

**2026-08-16 · DB `now()` = `2026-08-16 13:13:54.754176+00` (first read) to `2026-08-16 14:39:08.614446+00` (last) · BUILD.**
Base `origin/main` @ `609417f4`. Branch `checkpoint/BL-810` @ `b415680e`, **verified pushed** (`safe-push` reported `VERIFIED PUSHED` and `git ls-remote` agrees: `origin/checkpoint/BL-810 == local HEAD`). Tags `pre-BL-810` (`609417f4`) and `post-BL-810` (`b415680e`) both on origin. Isolated worktree `C:/w810`, a short path, `node_modules` never junctioned, **removed at the end**.

**This is a branch round. It is NOT merged to main, and it requires a Railway REDEPLOY before it is live.** `DATABASE_URL` from `.env.local`; every database read through `scripts/run-select.js` or through the shipped module itself. Every timestamp cast `::text` against DB `now()`.

**No clip's earnings or status changed. No payout was created, modified, approved, cancelled or paid. No balance was touched. No schema change and no `prisma migrate`. No Apify actor ran and the 11 BL-678 guards are untouched.** Handles are redacted to an 8 character id prefix and no wallet address was selected or printed.

> **What shipped: `/admin/liability`. Owner only, read only, computed live on every load in 358 milliseconds. Per campaign and platform wide it states the clipper pool, what has been earned against it, what nobody has earned yet, what is owed now, what is reachable today, and what is stuck under a minimum. Every payable figure is stated TWICE, gross and cash, in separate columns. Every dollar lands in exactly one bucket and the buckets close to the cent.**

The canonical snapshot below is one read at **`2026-08-16 14:38:31.680217+00`**. Figures moved during the round because the tracking cron kept crediting live clips; that is stated rather than smoothed, and it is the strongest evidence the surface is live rather than cached.

---

## PART 0 — THE ARITHMETIC, DEFINED BEFORE ANY SCREEN

### Every figure, its definition, and the file and line behind it

| figure | what it is | where the platform decides it |
|---|---|---|
| **Clipper pool** | `(1 − lockedOwnerShare) × realBudget`, the clipper share of the budget, not the marketed total. `realBudget` is the marketed budget minus BL-630's ghost platform fee. | `clipperPoolCap`, `balance.ts:403`; `realBudgetFromFee`, `platform-fee.ts:47-71` |
| **Earned** | clipper earnings on APPROVED, not deleted, **live** clips: the pool's own spend basis. | `clipperSideSpent`, `balance.ts:405-409`; the same filter at `:311-313` |
| **Unearned** | pool minus earned, floored at zero. Identical to the platform's own headroom figure. | `clipperHeadroom`, `balance.ts:420` |
| **Requested** | sitting in a `REQUESTED`, `UNDER_REVIEW` or `APPROVED` payout row right now, valued gross. | `LOCKED_PAYOUT_STATUSES`, `balance.ts:54`; `clipperLiability`, `balance.ts:126-132` |
| **Paid** | money that has actually left: `PAID` always, `VOIDED` only when `paidAt` is set. | `isPayoutMoneyOut`, `balance.ts:117-124` |
| **Withdrawable** | earned, unpaid, and clearing that campaign's own minimum withdrawal today. | the gate at `payouts/route.ts:515` and `:686`; the minimum at `:345-346` via `resolveMinPayout`, `payout-minimum.ts:110-116` |
| **Stuck below minimum** | a positive per campaign balance that is under that campaign's own minimum. | the same comparison, `toCents(available) >= toCents(minimum)`, `payout-minimum-shared.ts:30-32` |
| **On retired videos** | owed money whose clips carry `videoUnavailable`, so the per campaign gate excludes it while the account wide clamp still counts it. | the gate's filter at `payouts/route.ts:515` against the clamp's at `:657-658` |

The shipped module is `src/lib/liability.ts`; the surface is `src/app/(app)/admin/liability/page.tsx` and `src/components/admin/LiabilityView.tsx`; the data route is `src/app/api/admin/liability/route.ts`. The harness is `scripts/bl810-verify.ts` and it calls **the same module the page calls**, so a figure that passes there cannot differ from a figure on screen.

### The clipper pool is the CLIPPER pool, and that is structural rather than careful

BL-743 cost a whole round to exactly this: a campaign named `Zhus Meme (0.20 CPM)` carries a **separate** `$0.1279` owner rate, so 1,000 views really cost `$0.3279`, and `$0.24 + $0.15` looked like an overpayment when it was the campaign working. BL-744 fixed the admin row by renaming the labels.

**`agency_earnings` is not selected anywhere in `src/lib/liability.ts`.** Proven by `grep -c`, which returns **0** for `agencyEarning`, `ownerCpm`, `agencyFee`, `clientName`, `aiKnowledge` and `marketplacePlatformEarning` across all three new files. The owner share appears only as the **derivation** of the pool, `(1 − s)`, which is what makes the pool a clipper share rather than a budget. It cannot leak into a figure it is never read into.

### Which of BL-642's two spend filters was used, stated plainly

BL-642 established that the clip side of campaign spend filters `APPROVED AND isDeleted = false AND videoUnavailable = false` while the agency side has **no filter at all**, and BL-758 measured the resulting phantom at $2,279.49 on somesome alone.

**This surface uses the CLIP side and never reads the agency side**, so BL-642's asymmetry cannot reach any figure here. That is the correct choice for this question for two reasons: the brief is clipper side only, and the agency side is owner accrual, which is a different pot.

Inside the clip side there is a second pair of filters, and it is the one that actually matters for liability. **Both are used, deliberately, because the platform uses both:**

* The **payable** basis (`videoUnavailable: false`) is what the per campaign withdrawal gate offers (`payouts/route.ts:515`) and what the pool's own spend counts (`balance.ts:405`). It drives every **per campaign** figure.
* The **lifetime** basis (no `videoUnavailable` filter) is what the account wide clamp subtracts against (`payouts/route.ts:657-658`) and what the clipper is shown as their balance. It drives every **platform** figure.

Using one for both would be wrong in one direction or the other. Their difference is not hidden: it is the **on retired videos** bucket, reported by name and by amount.

### Earned is computed from each clip's OWN stamped CPM, and it disagrees with the ledger

Every one of the **4,913** approved live clips is recomputed from its own `cpmAtSubmissionDecimal` on its **peak** view count, in the exact order `calculateClipperEarnings` applies at `earnings-calc.ts:135-202`: the minimum views gate, then `views ÷ 1000 × the clip's own rate`, then the per clip cap on **base before bonus**, then the bonus on the capped base, then `payoutReductionRatio` as a multiplier. Peak rather than latest because earnings ratchet and never decrease.

| | |
|---|---|
| Ledger (`Clip.earnings`, approved live) | **$12,781.33** |
| What each clip's own stamp and peak views support | **$14,767.87** |
| **Signed difference** | **−$1,986.54, an UNDER credit** |
| **Clips holding more than their own arithmetic supports** | **0 of 4,913** |

**So the recompute cannot be the bucket basis, and here is why that is a decision rather than a dodge.** The buckets have to reconcile against paid and requested, which are real stored payout rows in real dollars. If EARNED were the recompute, the identity would not close by $1,986.54 and the surface would be arithmetically wrong on its face. The ledger is what every gate enforces and what determines actual liability, so the ledger drives the buckets and **the recompute is shown beside it as a named discrepancy**, per campaign and platform wide. PART 5 covers what that gap is.

### Every dollar lands in exactly ONE bucket, proven twice over

**The platform identity, on the lifetime basis the account wide clamp uses:**

```
lifetime earned      $12,781.33
+ held above earnings    $82.12      (4 clippers, clamped to $0.00 available, no clawback)
= $12,863.45

paid                  $9,394.11
+ requested             $260.88
+ owed on the books   $3,208.46
= $12,863.45            EXACT, no residual
```

**And the owed figure splits into three, with nothing counted twice:**

```
owed on the books     $3,208.46
  withdrawable today  $2,289.22
  stuck below minimum   $509.85
  on retired videos     $409.39
                      ---------
                      $3,208.46   EXACT, no residual
```

**The per campaign identity, on the payable basis the pool uses**, holds on all 14 campaigns with a worst drift of **$0.00**:

```
earned + settled against retired = paid + requested + withdrawable + stuck
```

`settled against retired` is money already paid or requested against earnings that are no longer payable, almost always because a video was retired after a correct payment. It is **not a debt**, there is no clawback, and it exists in the partition only so the row adds up. It is labelled that way on screen.

**And the pool tiles exactly:** `clipper pool = earned + unearned` on every campaign where earned is under the pool, worst drift **$0.00**.

### The bridge between the per campaign columns and the platform figure, named rather than left as a gap

The campaign column sums to **$2,349.69** of withdrawable. The platform figure is **$2,289.22**. The difference is **exactly $60.47**, and it is not rounding: it is the account wide clamp at `payouts/route.ts:680`, `effectiveCap = min(perCampaignAvailable, globalAvailable)`, biting on one clipper (`cmqez5c2`, the standing BL-716 case). The same clamp accounts for **$0.82** of the stuck column, so the campaign stuck column sums to $510.67 against a platform $509.85. **Both bridges are printed on the page**, because a dashboard whose two views disagree by an unexplained $61.29 is worse than one that shows the arithmetic.

Total clamp bite across the platform: **$61.29 across 3 clippers**, matching BL-807's figure to the cent.

---

## PART 1 — THE FEE, SHOWN BOTH WAYS, AND A CORRECTION

**Every payable figure carries a gross and a cash twin, in separate sortable columns with separate `<th scope="col">` headers**, never a styled pair. BL-760 caught a $5.44 near overpayment and BL-763 a $7.80 one, both because a gross figure was about to be sent as cash. The two are also distinguished for a screen reader by a per cell spoken qualifier, so they can never be told apart only by position, colour, weight or opacity, which was BL-744's whole lesson.

| figure | GROSS, what leaves the clipper's balance | CASH, what the owner actually sends |
|---|---|---|
| Owed on the books | **$3,208.46** | **$2,943.26** |
| Withdrawable today | **$2,289.22** | **$2,092.91** |
| Stuck below minimum | **$509.85** | **$467.14** |
| On retired videos | $409.39 | $383.22 |
| Requested right now | $260.88 | **$233.76** |
| Paid to date | $9,394.11 | $8,585.91 |
| Stuck on frozen campaigns | $341.42 | $313.18 |

**The reduced 4 percent referred rate, and how it was handled.** The gate stamps the rate live at request time from `payouts/route.ts:403`, `referredById ? 4 : 9`. Money nobody has requested carries no stamp, so a projection is required. It is made through `calculatePayoutBreakdown` — **the same helper the real payout uses** — with the same per user input, per clipper, then summed. A projection computed by a second rule could drift from what the platform will really charge, which is the class of defect BL-688 and BL-734 each cost a round to.

It is not academic: **26 of the 153 clippers owed money are referred and hold $470.76 of the $3,208.46.**

**A correction to the accessibility review, and to a claim I nearly shipped.** The review said a reader multiplying a gross figure by 0.91 would get a number that is **too high**, and I wrote that sentence into the page before checking it. **It is backwards.** Referred clippers pay 4 percent, so their cash is *higher*, and a flat 9 percent **understates** the true cash:

```
owed gross  $3,208.46
flat 9%     $2,919.70
true cash   $2,943.26      the flat figure is $23.56 SHORT
```

The page now says that, with both numbers on screen. The genuinely dangerous confusion is the other one and it is stated first: gross and cash differ by **$265.20** on the owed total.

**Express is deliberately not projected.** BL-176's 4 percent express premium is a speed a clipper chooses at request time. Charging it against money nobody has requested would be picking the arithmetic that suits the payer, which BL-760 refused for the same reason. So: **money that already has a payout row carries that row's stored net**, express included, and money nobody has requested is projected at standard speed only. Three of the eight open rows chose express (`cmsv1ifo`, `cmsl8dbu`, `cmsq04pf`), which is why the requested bucket's effective rate reads 10.40 percent while the projected buckets read 8.27 percent. Both are correct and the page says which is which.

**A finding, reported not fixed: `finalAmount` is stale on 8 rows.** The adjust route stamps `actualPaidAmount` and never rewrites `finalAmount` (`src/app/api/admin/payouts/[id]/adjust/route.ts`), so on the 8 adjusted PAID rows the stored net does not match what was actually sent. This surface re derives those through the platform's own breakdown helper rather than reading a stale column. Reading `finalAmount` straight would have overstated cash paid by roughly $113.

---

## PART 2 — THE MINIMUM THRESHOLD, AND THE ONES WHO WILL NEVER CLEAR IT

**The two numbers side by side, platform wide:**

| | gross | cash | who |
|---|---|---|---|
| **Owed to people who CAN withdraw today** | **$2,289.22** | **$2,092.91** | nothing is blocking them; they have not pressed the button |
| **Held by people who CANNOT, because they are under a minimum** | **$509.85** | **$467.14** | **150 positions across 121 clippers** |

**Per campaign, with the count, the total, and how far the largest is from the threshold.** The largest holder matters as much as the total: one person 58 cents short is a different situation from twenty people a dollar short, which is exactly the case BL-762 found.

| campaign | state | minimum | clippers stuck | held gross | held cash | largest position | that one is short by |
|---|---|---|---|---|---|---|---|
| Zhus Edit (0.50 CPM) | ACTIVE | $20.00 | 15 | $91.84 | $84.07 | $18.75 | **$1.25** |
| Zhus Meme (0.20 CPM) | ACTIVE | $20.00 | 20 | $77.41 | $70.61 | $16.02 | $3.98 |
| **GainzAlgo (REPOST CAMPAIGN)** | PAST, **frozen** | $10.00 | 21 | $72.87 | $66.65 | $9.79 | **$0.21** |
| **somesome** | PAST, **frozen** | $10.00 | 22 | $71.85 | $65.55 | $9.63 | **$0.37** |
| **WinGram** | PAUSED and archived, **frozen** | $10.00 | 17 | $65.65 | $60.31 | $9.54 | **$0.46** |
| **bees.n.honey** | PAST, **frozen** | $10.00 | 29 | $52.76 | $48.45 | $7.03 | $2.97 |
| **Panic Baby** | PAST, **frozen** | $10.00 | 15 | $44.68 | $41.36 | $8.12 | $1.88 |
| **BAD BITCH ANTHEM (2.50 CPM)** | PAUSED, **frozen** | $10.00 | 3 | $15.75 | $14.33 | $7.44 | $2.56 |
| **BAD BITCH ANTHEM (0.50 CPM)** | PAUSED, **frozen** | $10.00 | 4 | $9.23 | $8.45 | $4.66 | $5.34 |
| **STRAENGE** | PAST, **frozen** | $10.00 | 3 | $4.52 | $4.34 | $2.37 | $7.63 |
| **SomeSome** | PAUSED and archived, **frozen** | $10.00 | 1 | $4.11 | $3.74 | $4.11 | $5.89 |
| | | | **150** | **$510.67** | | | |

The column sums to $510.67 against the platform's $509.85; the $0.82 difference is the account wide clamp, named in PART 0.

### The frozen ones, shown separately, because they will never resolve themselves

**115 of the 150 positions, held by clippers on campaigns that can NEVER accrue again, carrying $341.42 gross and $313.18 cash.** Those clippers cannot earn their way over the floor by any action available to them. Only the owner can release that money.

**Frozen is not a judgement, it is `campaignStatusBlocks` verbatim** (`tracking.ts:1939-1944`): archived, `status = PAST`, or auto paused by the budget. A campaign the owner paused **by hand** is deliberately NOT frozen, because he can lift it, which is the judgement call BL-765 made and this round keeps.

**This is larger than BL-765's figure and the reason is measurable, not drift.** BL-765 measured 93 blocked positions across 85 clippers holding $262.69 on 2026-08-10. Today it is 115 positions and $341.42. Two campaigns joined the frozen set in between: **both BAD BITCH ANTHEM campaigns auto paused on 2026-08-13** (`lastBudgetPauseAt` `10:41:07.431` and `10:41:13.568`, `pauseSource` AUTO), adding 7 positions and $24.98, and the remainder is ordinary accrual pushing more positions into the below minimum population on campaigns that were already frozen.

The remaining **35 positions, $169.25**, sit on the two ACTIVE Zhus campaigns where the clippers can still clear the threshold on their own. The page states which of the two situations each row is in, in words.

---

## PART 3 — EVERY CAMPAIGN, INCLUDING THE FINISHED ONES

**Every status is covered.** The page shows all 14 campaigns that carry any clip or any payout, whatever their state, and the 20 archived dev seed campaigns with a null budget and zero clips are excluded because a row of zeroes is filler rather than information.

| status | campaigns shown | stuck money on them |
|---|---|---|
| ACTIVE | 3 (Zhus Meme, Zhus Edit, SomeSome App) | $169.25 |
| PAUSED, not archived | 2 (both BAD BITCH ANTHEM) | $24.98 |
| PAUSED **and archived** | 3 (WinGram, SomeSome, plus CROCS and Deja Shoe at zero) | $69.76 |
| PAST | 5 (somesome, STRAENGE, Panic Baby, bees.n.honey, GainzAlgo REPOST) | $246.68 |
| COMPLETED | **0 exist on the platform today** | n/a |

**Which statuses hold stuck money, and how much: PAST holds $246.68, archived holds $69.76, PAUSED holds $24.98, ACTIVE holds $169.25.** So **$341.42 of the $510.67, exactly two thirds, sits on campaigns that are finished in one sense or another.** That is the answer to why finished campaigns had to be included.

**One thing worth the owner's attention: COMPLETED is not in `campaignStatusBlocks`.** A campaign marked COMPLETED would still accrue on the cron, unlike a PAST one. Nothing is affected today because no campaign carries that status, and it is reported rather than changed.

**The platform total and the per campaign breakdown**, sorted so the largest liability reads first (the page defaults to `owed now gross` descending and every column sorts on click):

| campaign | state | clipper pool | earned | unearned | owed now gross | owed now cash | withdrawable gross | stuck gross | requested gross | paid gross |
|---|---|---|---|---|---|---|---|---|---|---|
| Panic Baby | PAST | $2,000.00 | $1,969.39 | $30.61 | **$1,113.24** | $1,013.75 | $1,068.56 | $44.68 | $46.51 | $849.06 |
| Zhus Meme (0.20 CPM) | ACTIVE | $4,879.54 | $581.43 | $4,298.11 | **$539.51** | $491.12 | $462.10 | $77.41 | $20.67 | $21.25 |
| bees.n.honey | PAST | $1,648.35 | $1,560.41 | $87.94 | **$341.39** | $313.69 | $288.63 | $52.76 | $57.58 | $1,189.48 |
| somesome | PAST | $6,543.62 | $1,967.14 | $4,576.48 | **$243.53** | $228.11 | $171.68 | $71.85 | $0.00 | $4,888.99 |
| Zhus Edit (0.50 CPM) | ACTIVE | $1,219.96 | $374.32 | $845.64 | **$169.66** | $154.88 | $77.82 | $91.84 | $126.12 | $78.54 |
| WinGram | PAUSED, archived | $3,333.33 | $267.58 | $3,065.75 | **$167.18** | $153.52 | $101.53 | $65.65 | $0.00 | $100.42 |
| GainzAlgo (REPOST) | PAST | $1,000.00 | $226.76 | $773.24 | **$141.48** | $129.08 | $68.61 | $72.87 | $0.00 | $160.89 |
| BAD BITCH ANTHEM (0.50) | PAUSED | $672.31 | $122.52 | $549.79 | **$100.55** | $91.55 | $91.32 | $9.23 | $0.00 | $21.97 |
| BAD BITCH ANTHEM (2.50) | PAUSED | $672.15 | $75.19 | $596.96 | **$35.19** | $32.02 | $19.44 | $15.75 | $10.00 | $30.00 |
| STRAENGE | PAST | $2,000.00 | $1,997.56 | $2.44 | **$4.52** | $4.34 | $0.00 | $4.52 | $0.00 | $2,053.51 |
| SomeSome | PAUSED, archived | $1,476.00 | $4.11 | $1,471.89 | **$4.11** | $3.74 | $0.00 | $4.11 | $0.00 | $0.00 |
| CROCS | PAUSED, archived | $5,398.92 | $0.00 | $5,398.92 | $0.00 | $0.00 | $0.00 | $0.00 | $0.00 | $0.00 |
| Deja Shoe | PAUSED, archived | $5,398.92 | $0.00 | $5,398.92 | $0.00 | $0.00 | $0.00 | $0.00 | $0.00 | $0.00 |
| SomeSome App | ACTIVE | $1,476.00 | $0.00 | $1,476.00 | $0.00 | $0.00 | $0.00 | $0.00 | $0.00 | $0.00 |
| **PLATFORM** | | **$37,719.10** | **$9,146.41** | **$28,572.69** | **$3,208.46** | **$2,943.26** | **$2,289.22** | **$509.85** | **$260.88** | **$9,394.11** |

**The unearned figure needed a split and got one.** $28,572.69 of the clipper pool has never been earned, but **only $6,619.75 of it is genuinely up for grabs**. The other **$21,952.94 sits on campaigns that can never accrue again**, dominated by CROCS and Deja Shoe at $5,398.92 each, which have zero clips and are both archived. Reporting one combined number would have overstated the opportunity by more than three times, so the page states both.

**Four campaigns carry no locked owner split** (Gainzalgo, Hapday, Grateful Songs, Zhus, all PAST with a manual spend figure and zero live clips), so the platform enforces **no separate clipper pool** on them at all: `balance.ts` computes `clipperPoolCap` only under the split flag. They are labelled `WHOLE_BUDGET` on the page, with a sentence saying the figure is a shared ceiling and not a clipper share. They hold no money and so do not appear in the table above.

---

## PART 4 — THE LAST VIDEO DATE, ON EVERY PAYOUT REQUEST

One line per open request, cast `::text` at the database so the value on screen is the database's own rendering and never a client timezone's opinion of it.

| payout | clipper | campaign | state | gross | cash | last video on that campaign |
|---|---|---|---|---|---|---|
| `cmsv1ifo` | `cmsiyg70` | Zhus Edit (0.50 CPM) | REQUESTED | $60.27 | $52.44 | `2026-08-16 01:49:39.203` |
| `cmq084lz` | `cmpq15k2` | bees.n.honey | **UNDER_REVIEW** | $57.58 | $52.40 | `2026-06-11 09:18:05.971` |
| `cmsnvqqn` | `cmq7qh6p` | Panic Baby | REQUESTED | $46.51 | $42.32 | `2026-08-06 13:47:27.098` |
| `cmst92ua` | `cmsm2zio` | Zhus Edit (0.50 CPM) | REQUESTED | $24.56 | $22.35 | `2026-08-14 19:49:05.714` |
| `cmsul7p1` | `cmsj74dk` | Zhus Edit (0.50 CPM) | REQUESTED | $21.00 | $19.11 | `2026-08-15 13:29:35.329` |
| `cmsl8dbu` | `cmqb6eia` | Zhus Meme (0.20 CPM) | REQUESTED | $20.67 | $17.98 | `2026-08-09 12:59:57.99` |
| `cmsuku4g` | `cmr51mba` | Zhus Edit (0.50 CPM) | REQUESTED | $20.29 | $18.46 | `2026-08-15 13:30:08.271` |
| `cmsq04pf` | `cmskdgtp` | BAD BITCH ANTHEM (2.50 CPM) | REQUESTED | $10.00 | $8.70 | `2026-08-11 12:00:31.344` |
| | | | | **$260.88** | **$233.76** | |

The date is `MAX(COALESCE(postedAt, createdAt))` over that clipper's non deleted clips on that campaign, so it is when they last put a video up, not when a row was touched.

**It answers the question it was asked to answer.** `cmsv1ifo` posted **today**, hours after requesting, so that clipper is still working. `cmq084lz` last posted on **2026-06-11**, requested on **2026-06-05**, and has been UNDER_REVIEW for **72.6 days** on a campaign that is now PAST: finished, cashing out, and waiting. That is still the oldest unresolved money item on the platform and BL-758 flagged it at 66.5 days.

---

## PART 5 — LIVE, THE COST, AND THE GAP IT DOES NOT HIDE

### Live, not cached, and the page says so

**Computed live on every request. There is no cache, no `revalidate` window, no snapshot table and no cron writer anywhere in this feature.** The page is a server component with `export const dynamic = "force-dynamic"` and reads the database at the instant it is requested. It prints the database's own `now()` and the milliseconds the computation took, so the reader never has to trust a claim about freshness.

Proven rather than asserted: three consecutive reads during this round returned **$3,197.77**, then **$3,208.46**, then **$3,208.46** of owed money as the tracking cron credited live clips between them. A cached surface could not do that.

### Would it show the known under crediting? Yes, by name, per campaign and platform wide

BL-807 found the platform under crediting by **$1,883.92** on 2026-08-14 and that is exactly the kind of thing a dashboard is tempted to drop. **This one shows it.**

| | |
|---|---|
| Ledger, approved live clips | **$12,781.33** |
| What each clip's own stamped CPM and peak views support | **$14,767.87** |
| **The platform is UNDER crediting by** | **$1,986.54** |
| Clips holding more than their own arithmetic supports | **0 of 4,913** |

Up from BL-807's $1,883.92 two days ago, on a slightly different basis (BL-807 compared stored `baseEarnings`; this compares stored `earnings`, base plus bonus, against a recomputed base plus bonus). The direction and the conclusion are identical, and **zero clips are above their ceiling** on both measurements.

**Where it comes from, per campaign, which is the part BL-807 could not decompose and this surface makes visible on every row:**

| campaign | ledger | supported | gap | state |
|---|---|---|---|---|
| somesome | $5,401.55 | $6,441.76 | **−$1,040.21** | PAST, budget exhausted |
| STRAENGE | $2,001.71 | $2,642.86 | **−$641.15** | PAST, budget exhausted |
| bees.n.honey | $1,605.19 | $1,795.20 | **−$190.01** | PAST, budget exhausted |
| Panic Baby | $2,029.30 | $2,101.26 | **−$71.96** | PAST, budget exhausted |
| BAD BITCH ANTHEM (2.50) | $75.19 | $101.23 | −$26.04 | auto paused 08-13 |
| GainzAlgo (REPOST) | $298.46 | $305.74 | −$7.28 | PAST |
| BAD BITCH ANTHEM (0.50) | $122.82 | $128.62 | −$5.80 | auto paused 08-13 |
| everything else | | | −$2.31 combined | |

**$1,943.33 of the $1,986.54, being 97.8 percent, sits on the four PAST campaigns that hit their budget cap and stopped.** That is documented pool cap trimming: the campaign ran out of money, so the trim refused to credit further, and the clips kept accruing views. It is the system working. It is still stated, because a known gap that a dashboard quietly drops is worse than no dashboard.

### The cost, measured rather than claimed

| | |
|---|---|
| Warm server computation | **358 milliseconds**, printed on the page itself |
| Full warm page load in dev, including render | **0.83 seconds** |
| Cold, first call after a process start | 3.6 seconds, being Prisma client instantiation plus the first pooled connection, paid once at boot rather than per request |

The reads: two grouped aggregates over `clips` (4,913 approved live rows), one `findMany` over `payout_requests` (172 rows), one over `campaigns` (34 rows), one over `users`, and **one grouped scan of `clip_stats` (228,963 rows)** for the recompute. The `clip_stats` scan is the expensive half; measured against a trivial baseline it costs roughly 250 to 400 milliseconds.

**Against BL-617's margin: 4,913 approved clips today, against the roughly 50,000 at which BL-642 said to build a cache.** BL-642 measured the clip aggregate at 2.36 ms on 4,132 rows and extrapolated linearly, so the clip side of this surface is nowhere near its wall. The `clip_stats` scan grows with clip count times ticks and is the term to watch; if it becomes a problem the recompute can be moved behind its own request without touching any liability figure.

**Would it slow anything? No, and this is structural.** BL-642 proved no decision path reads a display endpoint, and the same holds here by construction: `computeLiability` is imported by exactly two files, the page and its own GET route, and by nothing in the money core. **No budget gate, cap check or eligibility rule reads this surface**, so a slow read here can never move a dollar or open a cap.

---

## PART 6 — OWNER ONLY, AND IT CHANGES NOTHING

### Owner only, three ways, proven by grep and by request

1. **The page** `notFound()`s for any role except OWNER before it reads anything (`src/app/(app)/admin/liability/page.tsx`). `notFound()` rather than a redirect, so the URL's existence is not leaked, which is the pattern the admin layout itself documents. This matters because the admin layout perimeter deliberately admits ADMIN and REVIEWER.
2. **The data route** carries `requireOwner`, the same guard `/api/admin/payouts/unpaid` uses, returning `403 {"error":"Only owners can view liability"}`.
3. **The nav entry** lives only in `ownerNav`, an array that is only assigned for `role === "OWNER"`, and it is deliberately NOT added to the capability driven nav, so a REVIEWER with any capability never sees the link.

**Measured by direct request against a running server**, the method BL-791 established:

```
CLIPPER   /admin/liability          renders the 404 view, 0 tables, 0 money strings, no nav entry
REVIEWER  /admin/liability          renders the 404 view, 0 tables, 0 money strings, no nav entry
ADMIN     /admin/liability          renders the 404 view, 0 tables, 0 money strings, no nav entry
CLIPPER   /api/admin/liability  ->  403  {"error":"Only owners can view liability"}
REVIEWER  /api/admin/liability  ->  403  {"error":"Only owners can view liability"}
ADMIN     /api/admin/liability  ->  403  {"error":"Only owners can view liability"}
OWNER     /admin/liability      ->  the full table, 15 columns, 14 rows
```

**One honest note on the status line.** The page returns HTTP **200** with the 404 view painted, rather than a 404 status, because `notFound()` inside a page whose response has already begun streaming cannot rewrite the committed status. **`/admin/agency-earnings`, an owner only page that predates this round, behaves identically**, and a genuinely missing path (`/admin/definitely-not-a-page-bl810`) returns a true 404, so the mechanism works and this is the platform's existing behaviour rather than anything BL-810 introduced. What matters for BL-531 is that **no figure is painted and no money string is in the document**, and that is measured, not argued.

**BL-531's field strip, checked by `grep -c` across all three new files:** `agencyEarning` 0, `ownerCpm` 0, `agencyFee` 0, `clientName` 0, `aiKnowledge` 0, `marketplacePlatformEarning` 0. None of those fields is selected, passed or rendered anywhere in this feature.

### It changes nothing, proven the same way

* **Write verbs in the new files: 0.** `grep -cE "\.(create|update|updateMany|delete|deleteMany|upsert|createMany)\(|\$transaction|writeClipEarnings"` returns **0** for all four files.
* **HTTP verbs exported by the route: GET only.** There is no POST, PATCH, PUT or DELETE handler in the file.
* **The rendered page offers no action.** Measured out of the DOM at all five widths, scoped to `<main>`: **0 forms, 0 inputs, 0 links, 28 buttons — and all 28 are the 14 column sorts and the 14 per campaign breakdown toggles.** Every button's accessible name was read back and printed. There is no recalculate, no repair, no approve, no pay and no adjust anywhere on the surface.
* **No `agency-monitor --fix`, no owner re derive, no restamp, no retire, no revive.**

---

## PART 7 — PROVED ON REAL DATA

### Four campaigns in full, including three finished ones, with every bucket closing

**somesome (PAST, frozen, budget exhausted).** The hardest case on the platform, because far more has been paid out than is currently payable:

```
earned (live clips)          $1,967.14
+ settled against retired    $3,165.38
= $5,132.52

paid                         $4,888.99
+ requested                      $0.00
+ withdrawable                 $171.68
+ stuck below minimum           $71.85
= $5,132.52                  EXACT
```

Its clipper pool is $6,543.62, of which $1,967.14 is earned and $4,576.48 never was: `1,967.14 + 4,576.48 = 6,543.62` exactly. It holds $3,434.41 of earnings on retired videos, which is the whole explanation for the $3,165.38. **Nothing is double counted:** the retired earnings sit outside the pool arithmetic because `clipperSideSpent` excludes them, exactly as the platform does.

**Panic Baby (PAST, frozen).**

```
earned $1,969.39 + settled $39.42 = $2,008.81
paid $849.06 + requested $46.51 + withdrawable $1,068.56 + stuck $44.68 = $2,008.81   EXACT
pool $2,000.00 = earned $1,969.39 + unearned $30.61                                   EXACT
```

15 clippers hold $44.68 gross and $41.36 cash under its $10.00 minimum; the largest is $8.12, **$1.88 short**, and the campaign can never accrue again, so that person cannot close the gap themselves.

**WinGram (PAUSED and archived, frozen).**

```
earned $267.58 + settled $0.02 = $267.60
paid $100.42 + requested $0.00 + withdrawable $101.53 + stuck $65.65 = $267.60        EXACT
```

17 clippers hold $65.65 gross and $60.31 cash, **reproducing BL-763's and BL-765's figure to the cent**, and the largest is **46 cents** from the threshold.

**Zhus Edit (0.50 CPM), ACTIVE, for contrast.**

```
earned $374.32 + settled $0.00 = $374.32
paid $78.54 + requested $126.12 + withdrawable $77.82 + stuck $91.84 = $374.32        EXACT
```

15 clippers hold $91.84 under its $20.00 minimum, the largest **$1.25 short** — but this campaign is still earning, so that clipper can clear it without anybody doing anything.

**The harness that proves all of it: `scripts/bl810-verify.ts`, 20 assertions, 0 failures, exit 0.** It calls the same module the page calls, so a figure that passes there is the figure on screen.

### Reconciled against the earlier measurements

| measure | BL-758 (08-10 13:26) | BL-807 (08-14 20:01) | **BL-810 (08-16 14:38)** |
|---|---|---|---|
| Owed on the books | $3,355.22 | $3,329.00 | **$3,208.46** |
| Withdrawable | $1,944.39 | $2,206.13 | **$2,289.22** |
| **Unreachable** | **$830.02 across 130 clippers** | $874.56 across 133 | **$919.24 across 138** |
| of which on retired videos | $403.61 | $404.21 | **$409.39** |
| of which below a minimum | $426.41 | $470.35 | **$509.85** |
| Below minimum pairs | 139 | 142 | **150** |
| Held above earnings | $82.12 / 4 clippers | $82.12 / 4 | **$82.12 / 4, unchanged** |
| Clips above their own ceiling | not run | 0 | **0** |

**BL-758's $830.02 across 130 clippers reconciles to today's $919.24 across 138 as ordinary activity, and the difference is decomposed rather than waved at.** Over 6.05 days it grew by **$89.22**, of which **$83.44 is the below minimum bucket** and only **$5.78** is retired video. That is exactly the split BL-758 predicted when it called the below minimum population "the fastest growing bucket in this report".

**BL-735's 128 pairs at $400.69** (2026-08-08 13:18) reconciles the same way: **+22 pairs and +$109.16 over 8.05 days**, being 2.7 pairs and $13.56 a day. BL-758 measured the rate at 5.25 pairs and $22 a day over the preceding four days, so the rate has moderated but has still never once gone down:

```
111 / $324.33  (BL-728, 08-07)
115 / $332.00  (BL-731)
118 / $338.20  (BL-734, 08-07)
128 / $400.69  (BL-735, 08-08)
139 / $426.41  (BL-758, 08-10)
142 / $470.35  (BL-807, 08-14)
150 / $509.85  (BL-810, 08-16)
```

Two campaigns joining the frozen set on 08-13 is the one discontinuity, and it moved $24.98 from "can still clear it" to "never will".

### Rendered at all five widths, measured rather than eyeballed

`next dev --webpack` with `.env.development.local` present, real Chromium, the OWNER dev cookie. **67 assertions, 0 failures, exit 0.** Every screen in this section was seen.

| width | page h-scroll | table columns | body rows | row headers | non-none `aria-sort` | scroll region | forms | inputs |
|---|---|---|---|---|---|---|---|---|
| **320** | none (320 vs 320) | 15 | 14 | 14 | exactly 1 | labelled, `tabindex=0` | 0 | 0 |
| **375** | none (375 vs 375) | 15 | 14 | 14 | exactly 1 | labelled, `tabindex=0` | 0 | 0 |
| **414** | none (414 vs 414) | 15 | 14 | 14 | exactly 1 | labelled, `tabindex=0` | 0 | 0 |
| **1280** | none (1280 vs 1280) | 15 | 14 | 14 | exactly 1 | labelled, `tabindex=0` | 0 | 0 |
| **1440** | none (1440 vs 1440) | 15 | 14 | 14 | exactly 1 | labelled, `tabindex=0` | 0 | 0 |

The table itself is 1,808 to 2,056 pixels wide and scrolls **inside its own labelled keyboard region**; the page never scrolls sideways at any width. Data tables are explicitly exempt from 1.4.10 and horizontal scroll inside a focusable region is conforming.

**The disclosure, exercised for real at 375px:** rows went 14 to 15, `aria-expanded` went `false` to `true`, the extra row's `colSpan` is **15**, matching the real column count exactly, and there are **0 dangling `aria-controls` idrefs** because none is emitted.

**A defect found by rendering, and fixed.** The breakdown cell is as wide as the table, so its prose was laid out at 1,808 pixels and could only be read by scrolling sideways. The panel is now `sticky left-0` with a width cap: measured **272px at left 17 in a 320px viewport**, 327px at 375, and 621px at 1440. That was invisible in the markup and only a real render caught it.

**Sorting, exercised:** clicking `Paid gross` reordered the first row from `Panic Baby` to `somesome`, the status region announced *"Sorted by paid gross, highest first."*, and exactly one column reported `aria-sort` afterwards.

**A copy defect found by reading the DOM back, and fixed.** The stuck sentence rendered as `$41.36cash` because a JSX whitespace boundary collapsed. It now reads `$44.68 gross, $41.36 cash`. It would not have been caught by looking at the source.

### Nothing was changed

| check | result |
|---|---|
| Earnings invariant `earnings = base + bonus` | **0 violations** |
| Clips whose earnings or status this round changed | **0** |
| Payouts created, modified, approved, cancelled or paid | **0** |
| Schema changes | **0**; no `prisma migrate`, `prisma generate` only |
| Apify actors run | **0**; the 11 BL-678 guards untouched |
| The 6 money files plus `tracking.ts` and `campaign-era.ts` | **byte identical by blob OID on both refs** |

Blob OIDs, `git rev-parse main:<path>` against `git hash-object` in the worktree, all **IDENTICAL**: `clip-earnings-writer.ts` `ac5be7de`, `earnings-calc.ts` `797e2098`, `balance.ts` `e887f80a`, `tracking.ts` `83ce4bab`, `clip-earnings-invariant-middleware.ts` `61cef393`, `money-decimal.ts` `ef5cdae7`, `campaign-era.ts` `106e16ad`.

**One write happened in the path and it is disclosed rather than hidden.** The dev auth bypass calls `db.user.upsert` on `dev-owner-001` with `update: {}` on every render (`get-session.ts`). That is a no op on a synthetic row that has existed since 2026-03-24, it is the bypass's own behaviour and not this round's code, and no real user row was touched.

---

## THE ACCESSIBILITY REVIEW, AND WHERE I OVERRULED IT

Reviewed by the accessibility lead with five specialists **before any UI was written**. It returned GO on the concept and NO GO on four decisions. **All ten blocking items are implemented.**

1. **Route inside the `(app)` group** so the admin layout, sidebar and role gate all apply.
2. **Gross and cash are separate `<th scope="col">` columns**, each independently sortable. Never a styled pair, never distinguished by colour, weight, opacity or position.
3. **A visible sentence stating that cash cannot be reproduced by multiplying a gross figure**, with both numbers on screen. Corrected on direction, see PART 1.
4. **A per cell `sr-only` qualifier** on every gross and cash figure, because browse mode does not re announce column headers. The digits are `aria-hidden` behind one spoken sentence carrying the qualifier rather than the column name, so table navigation mode does not read the same word twice. No `/` anywhere, since NVDA skips it at default punctuation.
5. **No `<details>`.** It cannot span table rows: the content model forbids it and browsers foster parent it out of the `<tbody>`. A `<button aria-expanded>` plus a conditionally rendered `<tr><td colSpan={15}>` instead, with **no `aria-controls`**, because a dangling idref on a conditionally rendered target is an axe violation.
6. **Nothing is keyed by array index.** The table sorts, so `key={campaign.id}` and `openId: string | null`. This is the one item on the list that could have produced a wrong money reading.
7. **No `--bg-page` and no `ring-offset-*` anywhere.** That token is undefined repo wide and resolves to `#ffffff` through the registered `@property` initial value, painting a white halo. The global focus outline at `globals.css:222` is already correct in both themes.
8. **`badge.tsx` is not reused.** Its five variants measure 1.47:1 to 2.51:1 in the light theme and `PAST` is not even in its union. A new neutral chip carries the state **in the word**, bordered with `--border-strong` (3.48:1 dark, 3.42:1 light), so 1.4.1 is satisfied by construction rather than by a palette that has to be re measured. Sentence case in the DOM with the visual uppercase done in CSS, since `text-transform` does not reach the accessibility tree and literal caps invite initialism spelling.
9. **`text-accent` carries no small text meaning.** Measured 3.40:1 on the light card. It is used only on the four 24px headline figures and on `aria-hidden` icons, where the 3:1 non text bar applies.
10. **`role="list"` on the payout list**, because Tailwind v4's Preflight strips list semantics in WebKit.

**Six new paired colour tokens** were added to `globals.css` following the additive pattern BL-797 and BL-804 established, one dark and one light value each, every one clearing 3:1 against `--bg-card` in its own theme. Measured by `scripts/bl810-contrast.mjs`, which exits 0:

```
paid          #8b949e dark 5.98:1   #4d5560 light 7.54:1
requested     #d29922 dark 7.29:1   #8a6100 light 5.54:1
withdrawable  #2596be dark 5.42:1   #1b6f8f light 5.65:1
stuck         #f0883e dark 7.27:1   #a24c00 light 5.88:1
retired       #a371f7 dark 5.49:1   #6b32c9 light 7.18:1
unearned      #6e7681 dark 4.01:1   #767f8b light 4.05:1
```

**The review's ruling on the proof bar is adopted in full and is worth recording, because it corrects a requirement that cannot be met.** Chaining 3:1 between six ADJACENT segments needs a 243:1 luminance span and sRGB stops at 21:1, so it is arithmetically impossible. Separation between neighbours is a **1px `--bg-card` hairline** instead, each segment clears 3:1 against the card on its own, and the whole bar is `aria-hidden` because every figure it draws is stated as text beside it. Neither `progressbar` nor `meter` fits a partition: there is no single `aria-valuenow`, and both are children presentational in ARIA 1.2, which would erase every segment anyway.

**Where I overruled it, once.** The review recommended exporting a page title to fix WCAG 2.4.2, since the tab would otherwise inherit the marketing title. It is right about the criterion. **CLAUDE.md states the tab title is just "Clippers HQ"**, and a standing rule is not mine to overturn inside a feature round. No title is exported; the page identifies itself with an `h1`. **The conflict is the owner's to settle** and is recorded here rather than resolved quietly.

**Reported, not fixed, all pre existing and none introduced here.** The viewport meta at `layout.tsx:130` ships `maximum-scale=1, user-scalable=no`, a 1.4.4 failure whose iOS input zoom defence is already handled independently at `globals.css:259`, so the pair is redundant. `<main>` at `app-layout.tsx:1092` has no `id` and is not focusable, so no page can offer a working skip link. Both belong in their own rounds against those files.

**No landmarks were added.** `app-layout.tsx` already renders `<main>`, and four named regions would bury it in the rotor. Headings carry the structure: one `h1`, one `h2` per section.

**Zero new eslint warnings, which was a hard requirement.** The BL-348 hooks gate runs at `--max-warnings 11` and was already at exactly 11. Sorting is `useState` plus an inline sort at 14 rows, and the sort announcement is set in the click handler rather than in an effect, so no new dependency array exists to trip `exhaustive-deps`. **The gate reads 11 problems, 0 errors, 11 warnings, unchanged.**

---

## GATES, STATED HONESTLY

* `npm ci` **exit 0**. `npx prisma generate` **exit 0**, run after `npm ci` because `npm ci` wipes the generated client, and before any typecheck.
* **`eslint` confirmed present**, `npx eslint --version` reports **v9.39.4**, so the hooks gate is a real check and not a silent no op.
* `npx tsc --noEmit` **exit 0**, `grep -c "error TS"` = **0**.
* `npm run build` **BUILD_EXIT=0**, read from a log with the exit code echoed directly and **never piped through `tail`**. `prebuild` ran in full: `check:prisma-bypass` **0 violations** including its earnings write check, `check:removed-fields` **OK across 728 files**, `lint:hooks` **11 problems, 0 errors, 11 warnings against a ceiling of 11**. `✓ Compiled successfully`.
* **No clean baseline was captured before the first edit, and rather than pretend otherwise: there was no error to attribute.** `tsc` returned 0 errors on the changed tree, so no failure needed a baseline to explain it.
* `scripts/bl810-verify.ts` **20 passed, 0 failed, exit 0**. `scripts/bl810-contrast.mjs` **exit 0**. `scripts/bl810-render.mjs` **67 passed, 0 failed, exit 0**.
* Counting done with `grep -c` and **never piped through `head`**. No heredocs were used for SQL; every statement was passed directly to `run-select.js` or lives inside the shipped module. The BACKLOG entry was appended with a single non indented heredoc, disclosed here because a rule followed everywhere except once is worth naming; entry count verified **152 before, 153 after**, with exactly one BL-810 entry and no conflict markers.

---

## WHAT COULD NOT BE MEASURED, AND WHY

Stated plainly, because a gap presented as a result is worse than a gap.

* **Whether the $1,986.54 under credit can be attributed tick by tick.** There is no pool cap audit trail, so it can be attributed to budget exhausted campaigns (97.8 percent) and shown per campaign, but not decomposed further from stored state. BL-807 hit the same wall and it has not moved.
* **Whether this page is owner only in PRODUCTION.** Every role probe above ran against a local server with the dev auth bypass. The gates are the same code that runs in production (`requireOwner`, `getSession`, `ownerNav`), and BL-791 proved the identical `requireOwner` pattern returns 403 by direct request, but no authenticated request was made against clipershq.com and none is claimed.
* **Whether a real screen reader speaks the gross and cash cells as intended.** The markup is measured, the `sr-only` text is read back out of the DOM, and the aria attributes are asserted. NVDA, JAWS and VoiceOver were not run.
* **Whether COMPLETED campaigns behave as the owner expects.** None exists, so the observation that COMPLETED is absent from `campaignStatusBlocks` is read from source and not from data.
* **The exact clipper behind each redacted id.** Handles are deliberately not selected. The owner can map every 8 character prefix privately in admin.

---

## WHAT IS WAITING ON THE OWNER, FROM THIS SURFACE

Three decisions, all of them now backed by a number he can re read at any moment.

1. **$341.42 gross, $313.18 cash, held by clippers on campaigns that can never accrue again.** 115 positions. They cannot earn their way over the floor by any action available to them, and four of those campaigns have somebody sitting within 50 cents of the threshold. Only a policy can release this: a sweep payout, a lower floor on dead campaigns, or an explicit written forfeiture. It has grown at every single measurement since BL-728.
2. **$2,289.22 gross, $2,092.91 cash, that clippers can withdraw today and have not.** Nothing is blocking them. It is the cheapest item on the list and it costs a message.
3. **The 72.6 day payout, `cmq084lz`.** $57.58 gross, $52.40 cash, UNDER_REVIEW since 2026-06-05, on a campaign that is now PAST, held by a clipper who last posted on 2026-06-11 and has never been paid a dollar. BL-758 flagged it at 66.5 days.

---

## VERIFICATION AND SAFETY

Display and read only. Four new files (`src/lib/liability.ts`, `src/app/api/admin/liability/route.ts`, `src/app/(app)/admin/liability/page.tsx`, `src/components/admin/LiabilityView.tsx`), two edited (`src/app/globals.css` additive tokens, `src/components/layout/sidebar.tsx` one nav entry), plus four scripts and the BACKLOG entry.

**No clip's earnings or status changed. No payout was created, modified, approved, cancelled or paid. No balance was touched, nothing was restamped, retired or revived. `agency-monitor --fix` was never run. No platform wide owner re derive. No Apify actor and no paid probe: spend for this round is $0.00.** No schema change and no `prisma migrate`; `prisma generate` only. The earnings invariant reads **0 violations**.

Every figure on the surface traces to the query that produces it, and the harness that asserts them calls the same module the page calls, so there is one implementation and no second copy to drift. Every timestamp is cast `::text` against DB `now()`. Handles are redacted to an 8 character prefix and **no wallet address was selected, printed or partially printed**. The 6 money files plus `tracking.ts` and `campaign-era.ts` are byte identical by blob OID on both refs. **NO dashes as bullets.** The worktree `C:/w810` was removed.

**Rollback:** `git revert -m 1 <merge>` or `git reset --hard pre-BL-810`. **Nothing in the database needs undoing**, because the feature only reads.
