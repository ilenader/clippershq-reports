# BL-714 — Two clippers report money vanishing, and the owner's admin disagrees with what they see

READ-ONLY AUDIT. No code, data or money was changed. No payout was created, modified, approved or cancelled. No balance was touched. No env flag was flipped. Only `SELECT` ran (`scripts/run-select.js`, which refuses every write keyword). Handles are redacted throughout; the two accounts are **Clipper A** and **Clipper B**. No wallet address appears anywhere in this document.

Code read at `main` = `8b5aaf57` in an isolated worktree. DB read live. Every timestamp below is cast `::text` and quoted against `now()` = **2026-08-05 10:58:37.265953+00**.

---

## VERDICT (one line)

**Neither clipper has lost a dollar they were genuinely owed today; but Clipper A is being charged $60.47 against live earnings to recover an overpayment the platform created itself when a budget-capped campaign rewrote his already-paid earnings downward, and that $60.47 is a real money defect on our side, not his.**

Clipper B lost only the *display* of $10.44 he was never able to withdraw. Clipper A lost the *use* of $60.47 he genuinely earned on a second campaign.

---

## HEADLINE: THE LEADING HYPOTHESIS IS HALF RIGHT

The brief proposed that BL-698 (the `videoUnavailable` filter added to the clipper display) explains both reports because the owner's admin does not apply the same filter.

| | Verdict |
|---|---|
| Clipper B | **CONFIRMED.** B has 12 retired clips worth $10.44. The owner's surface counts them, the clipper's does not. That is exactly his $6.04-vs-$0.00 disagreement. |
| Clipper A | **REFUTED.** A has **zero** clips with `videoUnavailable = true`, on either campaign, at any time. BL-698 changed nothing for him. His cause is entirely different and previously undiagnosed. |

Two more corrections to the brief's premises, both material:

1. The filter is **not** at `api/earnings/route.ts:64`. Line 64 is `clipWhere`, which deliberately does **not** filter, so the clipper's own history and chart keep the retired clips. The split happens at **`src/app/api/earnings/route.ts:206`** (`const payableClips = clips.filter((c) => !c.videoUnavailable)`). Anyone patching line 64 would silently delete 26 clippers' clip history.
2. Clipper A **is** BL-690's over-held clipper "C-3", confirmed to the cent (same $1,894.14 paid). His situation was therefore already partly diagnosed, but the *cause* of the overpayment was not, and it is not what BL-690 assumed.

---

# PART 1 — Every number, traced to the query that produces it

## Shared machinery (file:line)

| Quantity | Where it is computed |
|---|---|
| Clipper displayed balance | `src/lib/balance.ts:156` `computeBalance`, fed from `src/app/api/earnings/route.ts:207` |
| The `videoUnavailable` display filter | `src/app/api/earnings/route.ts:206` |
| Clipper per-campaign balance | `src/lib/balance.ts:206` `computeCampaignBalances`, called at `earnings/route.ts:208` |
| Global clamp applied to the per-campaign display | `src/app/api/earnings/route.ts:259` (`Math.min(b.available, balance.available)`) |
| Withdrawal gate, per-campaign earnings basis | `src/app/api/payouts/route.ts:424` (`videoUnavailable: false`) and `:462-483` |
| Withdrawal gate, global clamp | `src/app/api/payouts/route.ts:566-589` (`:567` deliberately has **no** `videoUnavailable` filter) |
| `$10` minimum | `src/app/api/payouts/route.ts:271` |
| `9%` fee (4% if referred) | `src/app/api/payouts/route.ts:312`; arithmetic at `src/lib/payout-calc.ts:83` (`finalAmount = round2(amount − round2(amount × pct/100))`) |
| Owner per-clipper view | `src/app/api/admin/payouts/user/[id]/route.ts:87` (clips), `:170` (per-campaign unpaid), `:210` (global unpaid), `:213` (net after fee) |
| Owner unpaid list | `src/app/api/admin/payouts/unpaid/route.ts:34` (clips), `:164` (unpaid), `:172` (net) |
| Money-out / liability rules | `src/lib/balance.ts:117` `isPayoutMoneyOut`, `:126` `clipperLiability` |

The single structural fact behind everything below: **`admin/payouts/user/[id]/route.ts:87` reads `{ userId, status: "APPROVED", isDeleted: false }`. It has no `videoUnavailable` filter and no test-campaign filter. `api/earnings/route.ts:206` applies both.** The two screens sum different populations.

## Clipper A — reconciliation

Database state, all campaigns, APPROVED and not deleted:

| Campaign | Clips | Earned (all) | Earned (live only) | Earned (retired) |
|---|---|---|---|---|
| STRAENGE (PAST) | 80 | $1,833.67 | $1,833.67 | $0.00 |
| Panic Baby (ACTIVE) | 50 | $405.62 | $405.62 | $0.00 |
| **Total** | **130** | **$2,239.29** | **$2,239.29** | **$0.00** |

Marketplace creator earnings: **$0.00** (no rows). Payout history:

| Status | Amount | Campaign | Paid at (`::text`) |
|---|---|---|---|
| PAID | $1,894.14 | STRAENGE | 2026-07-07 16:09:10.717 |
| REJECTED | $1,220.00 | STRAENGE | never |
| REJECTED | $372.97 | STRAENGE | never |

`paidOut` = $1,894.14 (`balance.ts:192` over `isPayoutMoneyOut`). `lockedInPayouts` = $0.00 (REJECTED is not in `LOCKED_PAYOUT_STATUSES`, `balance.ts:54`).

### The owner's four figures

| Owner reported | Reproduced | Query that produces it | Match |
|---|---|---|---|
| Total earned $2,239.29 | **$2,239.29** | `admin/payouts/user/[id]:87` → `:139` → `:189` | exact |
| Total paid out $1,894.14 | **$1,894.14** | `admin/payouts/user/[id]:162` via `clipperLiability` | exact |
| Locked $0.00 | **$0.00** | `admin/payouts/user/[id]:163` | exact |
| Unpaid $345.15 | **$345.15** | `admin/payouts/user/[id]:210`, `max(2239.29 − 1894.14 − 0, 0)` | exact |
| "$369.19 after the 9 percent fee" | **NOT REPRODUCIBLE** | see below | **finding** |

**FINDING 1: the $369.19 is not the net on $345.15.** `admin/payouts/user/[id]:213` computes `totals.netAfterFee` off the **global** unpaid: `calculatePayoutBreakdown(345.15, 9, 6).finalAmount` = **$314.09** (fee $31.06). The figure $369.19 comes from a **per-campaign row**, not the totals row: the Panic Baby row at `:173` computes `calculatePayoutBreakdown(405.62, 9, 6).finalAmount` = **$369.11** today, and $369.19 corresponds to a Panic Baby unpaid of $405.70, an 8-cent drift consistent with the screen being read minutes from now(). The owner has quoted the **global** unpaid ($345.15) alongside a **per-campaign** net ($369.19). They are computed on different bases and cannot be combined. If he pays $345.15, the clipper receives **$314.09**, not $369.19. That is a $55.10 quoting error waiting to be made.

**FINDING 2: the STRAENGE row hides the whole story.** On the same screen, STRAENGE shows `earned $1,833.67, paid $1,894.14, unpaid $0.00`, because `:170` floors at zero (`Math.max(earned − paid − locked, 0)`). The $60.47 overpayment is invisible. This is precisely why the owner concluded "STRAENGE was already paid out" and looked no further.

### The clipper's figure, and the $131.53

Clipper A reported **$213.62 available**, three days before now(). Today, every clipper-facing formula gives:

* `computeBalance.available` (`balance.ts:200`) = `max(2239.29 − 1894.14 − 0, 0)` = **$345.15**
* Panic Baby per-campaign available (`balance.ts:251`) = **$405.62**
* Panic Baby as displayed after the clamp (`earnings/route.ts:259`) = `min(405.62, 345.15)` = **$345.15**
* Withdrawal cap the gate would actually allow (`payouts/route.ts:589`) = `min(405.62, 345.15)` = **$345.15**

**$213.62 is NOT REPRODUCIBLE from today's state, and this is expected: it is a three-day-old reading of a number that has grown.** Reconstructed from `clip_stats` view snapshots (earnings scale linearly with views below the per-clip cap), Clipper A's Panic Baby earnings three days ago were ≈ **$301.95** on 564,483 views, against **$405.62** on 756,119 views now. STRAENGE was static at $1,833.67 (identical peak and latest views on all 80 clips, zero clips with a view decrease). Global available three days ago therefore ≈ `max(2135.62 − 1894.14, 0)` ≈ **$241.48**.

**The $131.53 gap is arithmetically exact and is earnings growth, not a missing filter.** $2,239.29 − $131.53 = $2,107.76, and $2,107.76 − $1,894.14 = $213.62. So his reading corresponds to a moment when his lifetime approved earnings were $2,107.76, i.e. Panic Baby at $274.09. That sits between the reconstruction at 3 days ($301.95) and earlier, and my reconstruction is only reliable back about nine days before per-clip snapshot coverage collapses. **I could not pin the exact reading moment. The platform retains no balance history and no earnings history (`savedEarnings` is 0 on every one of his clips, and there is no audit_log action for an earnings write), so the clipper's screen at report time cannot be replayed exactly. Named as an unmeasurable.**

What is *not* stale, and what he was actually complaining about:

### The $60.47 — "about $61 vanished"

```
Panic Baby available, per campaign   $405.62
Global available (the clamp)         $345.15
Difference                            $60.47   <-- "about $61"
```

This difference is **constant** and independent of how fast Panic Baby grows, because

```
clampGap = PanicBaby − (PanicBaby + STRAENGE − paid) = paid − STRAENGE
         = 1894.14 − 1833.67 = 60.47
```

Three days ago it was $301.95 − $241.48 = **$60.47**, to the cent. He is looking at a campaign that says he earned $405.62 and a cash-out screen that will only let him take $345.15, and the shortfall has not moved in days. That is the "$61".

## Clipper B — reconciliation

One campaign only (Panic Baby). 43 APPROVED, non-deleted clips.

| Basis | Amount |
|---|---|
| All approved (owner basis) | **$120.20** |
| Live only, `videoUnavailable = false` (clipper basis) | **$109.76** |
| Retired, 12 clips | **$10.44** |

Marketplace creator earnings: **$0.00**. Payouts, all PAID, all on Panic Baby:

| Amount | Requested (`::text`) | Paid at (`::text`) |
|---|---|---|
| $11.34 | 2026-07-12 16:20:21.464 | 2026-07-17 14:59:48.238 |
| $12.82 | 2026-07-19 04:02:40.225 | 2026-07-23 17:47:42.166 |
| $90.00 | 2026-07-29 13:20:23.607 | 2026-08-03 17:26:12.033 |
| **$114.16** | | |

| Figure reported | Reproduced | Query | Match |
|---|---|---|---|
| Owner: earned "$120" | **$120.20** | `admin/payouts/user/[id]:87` → `:139` | exact |
| Owner: paid "$114" | **$114.16** | `admin/payouts/user/[id]:162` | exact |
| Owner: unpaid $6.04 | **$6.04** = `max(120.20 − 114.16 − 0, 0)` | `admin/payouts/user/[id]:170` and `:210` | **exact** |
| Owner: $5.50 after the 9% fee | **$5.50** = `round2(6.04 − round2(6.04×0.09))` = `6.04 − 0.54` | `payout-calc.ts:83` | **exact** |
| Clipper: available $0.00 | **$0.00** = `max(109.76 − 114.16 − 0, 0)` | `balance.ts:200` over `earnings/route.ts:206` | **exact** |
| Clipper: earned / approved $95.67 | **NOT REPRODUCIBLE** | see below | **finding** |

**FINDING 3: $95.67 cannot be reproduced from any basis, at any reconstructable moment.** Every candidate was tested: all-approved $120.20; live-only $109.76; `baseEarnings` $119.49; live `baseEarnings` $109.08; per-account splits $112.13 and $8.07. Reconstructed live-only earnings by view snapshot run **$103.78 (9 days back) to $109.64 (1 day back)** and never approach $95.67; before 9 days the reconstruction is invalid because per-clip snapshot coverage begins. Only $1.99 of his earnings were approved within the last 2 days, so a review backlog does not close it either. **$95.67 sits roughly $8 to $14 below every figure the platform can produce. Named as unreproduced.** It does not change any conclusion: under *every* basis tested, `paid $114.16` exceeds `live earned $109.76`, so his available is $0.00 either way.

**The earned gap is $24.53, not $24.33.** The brief used the owner's rounded "$120". Against the true $120.20 the gap is $120.20 − $95.67 = **$24.53**, and it decomposes as:

```
$10.44   the videoUnavailable filter at earnings/route.ts:206   (explained)
$14.09   unreproduced (see FINDING 3)
-------
$24.53
```

## The $10 minimum and the 9% fee, applied

| | Clipper A | Clipper B |
|---|---|---|
| Max the gate would allow today (`payouts:589`) | **$345.15** | **$0.00** |
| Passes the $10 minimum (`payouts:271`) | yes | **no** |
| Net after 9% (`payout-calc:83`) | **$314.09** | n/a |
| Blocked by a pending payout | no | no |

Clipper A can request $345.15 right now and would receive $314.09. Clipper B can request nothing.

---

# PART 2 — Did money disappear, or only the display of it?

## Clipper B: only the display, with one honest qualification

Every clip of B's whose earnings stopped counting toward his available balance:

| Clip | Earnings | Stopped counting at (`::text`) | Cause | Account status |
|---|---|---|---|---|
| cmrj5qjr | $0.00 | 2026-07-18 19:10:11.545056 | video retired | APPROVED |
| cmrkr2ns | $0.68 | 2026-07-22 06:00:19.055 | video retired | APPROVED |
| cmrj5rqv | $0.80 | 2026-07-22 06:00:23.973 | video retired | APPROVED |
| cmrm5zjz | $0.89 | 2026-07-27 06:00:33.327 | video retired | APPROVED |
| cmraz1xm | $1.04 | 2026-07-30 06:00:58.618 | video retired | APPROVED |
| cmrjhpfk | $1.43 | 2026-07-30 06:01:16.464 | video retired | APPROVED |
| cms23z4o | $0.82 | 2026-07-31 06:00:07.427 | video retired | APPROVED |
| cmrkr3db | $1.04 | 2026-07-31 06:00:12.462 | video retired | APPROVED |
| cmrqmb05 | $1.11 | 2026-07-31 06:00:14.826 | video retired | APPROVED |
| cms23z4o | $1.05 | 2026-07-31 06:00:17.929 | video retired | APPROVED |
| cms23z4s | $0.68 | 2026-07-31 06:00:20.514 | video retired | APPROVED |
| cmrqmb6w | $0.90 | 2026-07-31 06:00:23.497 | video retired | APPROVED |
| | **$10.44** | | | |

**These are genuine video retirements, NOT an account-ban cascade.** BL-698 warned that `videoUnavailable` is written by two mechanisms. This audit distinguished them on three independent signatures. The ban cascade at `src/lib/clip-account-cascade.ts:182-199` writes `savedEarnings = current earnings`, sets `earnings = 0`, and deletes the AgencyEarning row. On all 12 clips: `savedEarnings = 0`, earnings preserved and non-zero on 11 of 12, and the AgencyEarning row still present on 11 of 12. Both of B's clip accounts are `APPROVED` and were never suspended, and B does not appear in any of the 8 `USER_BAN_TRACKING_CASCADE` audit rows. The retirement timestamps cluster at 06:00:xx UTC, the daily availability sweep. **B was not penalised for anything. His videos are gone from the platforms.**

**Could he ever have withdrawn that $10.44?** Partly, and the honest answer matters. The withdrawal gate at `payouts/route.ts:424` has **always** excluded `videoUnavailable` clips, so from the instant each clip was retired that clip's money was unreachable. But before its retirement each clip's earnings *were* withdrawable. His $90 request went in on 2026-07-29 13:20; eight of the twelve clips ($8.07 worth) retired **after** that, on 2026-07-30 and 2026-07-31, while that request was in flight and locking his balance. So a slice of it was theoretically reachable up to those dates. **What BL-698 changed on 2026-08-03 was not his access, which was already gone, but the number on his screen, which had been telling him he had roughly $6 he could not have.**

## Clipper A: money that genuinely stopped counting, and it is not `videoUnavailable`

**Zero of Clipper A's clips are retired.** Zero are deleted. Zero carry `payoutReductionRatio`. Zero carry `earningsFrozenAt`. Zero views ever decreased (peak views equal latest views on all 80 STRAENGE clips). His rejected clips are worthless (largest 1,335 views, all `earnings = 0`). So none of the usual suspects applies.

What actually happened:

**On 2026-07-07 16:01:36 he requested $1,894.14 against STRAENGE and it was paid at 16:09:10.717.** The withdrawal gate is the only live payout-creation path (`src/actions/payouts.ts:50` is dead and fails closed by construction, per BL-556; `payouts/referral-request/route.ts:153` is a different product). The gate at `payouts/route.ts:483,595` refuses any amount above the per-campaign available. **Therefore his STRAENGE approved-and-live earnings were at least $1,894.14 at that moment.**

**Today those same STRAENGE earnings total $1,833.67, and the 72 clips whose IDs the payout snapshotted total $1,823.10.** All 72 are still APPROVED, not deleted, not retired. Meanwhile their views rose from 4,507,552 to 5,116,424, a 13.5% increase.

**Views up, recorded earnings down.** That combination has exactly one available explanation in this codebase, and the campaign confirms it:

| STRAENGE | |
|---|---|
| Budget | $3,000.00 |
| Budget ever changed | **no** (one row in `campaign_budget_changes`, "Campaign created", 2026-06-13T19:53:55.244Z) |
| Clipper-side spend now | $2,001.71 |
| Owner-side spend now | $1,000.54 |
| **Total** | **$3,002.25 against a $3,000 budget** |
| `AUTO_PAUSED` events | 6, first 2026-07-07 15:21:47.659, last **2026-08-01 06:31:33.775** |
| `MANUAL_RESUME` | 2026-08-01 06:25:59.657 |

The campaign is pinned at its ceiling. Across all 16 clippers on it, stored earnings are $2,001.71 against an uncapped views×CPM model of $2,652.52, a **$650.81 shortfall held back by the budget**. Only 17 of Clipper A's 80 clips sit at full value; the mean ratio of stored to uncapped is **0.757**. And the whole of his STRAENGE clip set carries `updatedAt` clustered at **2026-08-01 06:31:04 to 06:31:15**, seconds before that final `AUTO_PAUSED` at 06:31:33.775. The ceiling was re-applied across the campaign in one pass, four days ago, and it landed on a clipper who had already been paid.

**FINDING 4 (the second, previously unknown defect): the campaign budget ceiling can rewrite a clipper's recorded earnings to below a payment already made, and the global clamp then charges the shortfall against a different, live campaign.** The proportional cut exists by design (`tracking.ts:1257` `F-PROPORTIONAL-CUT`, and `clip-earnings-writer.ts:152` explicitly permits decreases: *"Decreases always pass"*). Budget is the deal, and no one should argue the campaign must pay more than $3,000. But the money was already out the door, and the recovery is being taken from a **different** campaign whose budget is 73% consumed and which owes him honestly.

**Could Clipper A have withdrawn the $60.47 before it stopped counting?** He did better than that: **he was paid it.** It was inside the $1,894.14 that reached his wallet on 2026-07-07. He is not out of pocket by a cent on STRAENGE. What he has lost is access to $60.47 of **Panic Baby** money he genuinely earned, which is being consumed to recover the STRAENGE shortfall. That is materially different from B's case and it deserves a different answer.

**Not measurable:** the exact date the clamp began binding, i.e. the moment STRAENGE's recorded total first fell below $1,894.14. There is no earnings history table, `savedEarnings` is 0 on all his clips, and no audit_log action records an earnings write. The 2026-08-01 06:31 rewrite is the strongest and most recent candidate but I cannot prove it was the only one, and I will not assert what I could not measure.

---

# PART 3 — Which screen is right?

Every surface that displays a clipper's earned, paid, locked or unpaid, with the population it sums and the rules it applies.

| # | Surface | file:line | Population summed | `videoUnavailable` filter | Global clamp | Per-campaign gate | $10 min | 9% fee |
|---|---|---|---|---|---|---|---|---|
| 1 | Clipper earnings page (headline) | `api/earnings/route.ts:206-207` | APPROVED, not deleted, **non-test campaigns**, **live only** | **YES** | no (this *is* the global) | no | no | no |
| 2 | Clipper per-campaign / cash-out selector | `api/earnings/route.ts:208,259` | same as #1, per campaign | **YES** | **YES** (`min(perCampaign, global)`) | yes | no | no |
| 3 | Withdrawal gate, per-campaign | `api/payouts/route.ts:424,462-483` | APPROVED, not deleted, **live only**, one campaign | **YES** | n/a | **this is it** | yes `:271` | yes `:312` |
| 4 | Withdrawal gate, global clamp | `api/payouts/route.ts:566-589` | APPROVED, not deleted, **retired INCLUDED** | **NO** (deliberate, BL-692) | **this is it** | binds via `min` `:589` | yes | yes |
| 5 | Owner per-clipper summary | `api/admin/payouts/user/[id]/route.ts:87,170,210,213` | APPROVED, not deleted, **retired INCLUDED**, **test campaigns INCLUDED**, marketplace creator rows **unfiltered** | **NO** | no | per-campaign rows floored at 0 `:170` | no | net only `:213` |
| 6 | Owner unpaid list `/admin/payouts` | `api/admin/payouts/unpaid/route.ts:34,164,172` | APPROVED, not deleted, **retired INCLUDED**, **test INCLUDED**, marketplace creator **OMITTED ENTIRELY** | **NO** | headline only `:245-260` | rows floored at 0 `:164` | no | net only `:172` |
| 7 | Owner payout-request list enrichment | `api/payouts/route.ts:122,165` | APPROVED, not deleted, **live only** | **YES** | **YES** `:159-190` | yes | no | no |
| 8 | Owner campaign-archive per-clipper | `api/admin/archive/[campaignId]/route.ts:155` | APPROVED, **retired INCLUDED**, **locked NOT subtracted**, **not floored at zero** | **NO** | no | no | no | no |
| 9 | Campaign budget "spent" | `lib/balance.ts:312` | APPROVED, not deleted, **live only** | **YES** | n/a | n/a | n/a | n/a |

## Which surfaces disagree, and by how much platform-wide

**Disagreement 1 (the big one, and the one the owner will quote): #5 and #6 versus #1.** Measured across all 227 clippers with earnings:

```
Owner-side displayed unpaid, all surfaces #5/#6:   $2,811.12
Clipper-side displayed available, surface #1:      $2,411.26
Gap:                                                 $399.86   across 28 clippers
```

BL-702 measured $392.45 across 26 at the BL-698 deploy; it has since grown to $399.86 across 28 as more videos were retired. **The owner's admin is currently showing $399.86 that no clipper can withdraw and that no clipper is being shown.** If he quotes those figures to clippers or to clients, he is quoting money that does not exist as a liability. Clipper B's $6.04 is one row of that 28.

**Disagreement 2: #4 versus #1, introduced by BL-698 and not yet re-aligned.** BL-692 deliberately moved the gate's global clamp onto the lifetime basis *including* retired clips, and justified it (`payouts/route.ts:556-562`) on the grounds that the displayed balance used that same basis. BL-698 then moved the displayed balance off that basis. The justification in that comment block is now stale, and the gate is looser than the display. Measured: **4 clippers, $3.60 total**, where the gate would permit more than the clipper is shown. Small today, structurally wrong, and it will grow with every retirement.

**Disagreement 3: surface #8 has no floor and no locked subtraction.** `admin/archive/[campaignId]/route.ts:155` computes `totalEarnings − paidByUser` with no `Math.max(…, 0)` and no `locked` term. For Clipper A on STRAENGE it renders **−$60.47**. It is the only surface in the platform that shows the truth, and it does so by accident, on an archive page, as a negative number with no explanation.

**Disagreement 4: surfaces #5 and #6 disagree with each other.** #5 folds in `marketplaceCreatorEarning` rows with *no* status, deleted or availability filter at all (`user/[id]:110-116`); #6 omits marketplace creator earnings entirely. Neither matches #1, which filters those rows on `clip.status = APPROVED, isDeleted false, videoUnavailable false` and non-test campaigns (`earnings/route.ts:79-84`). Immaterial for A and B (both have zero such rows) but it is a live divergence between two owner screens.

**Which screen is right?** For "what does this clipper own and what can they take", **surface #1 is right and surfaces #5, #6 and #8 are wrong**, because #1 matches the per-campaign gate at #3 that actually decides withdrawals. For "what did this clipper historically earn", #5 is right and #1 is incomplete. The platform needs both numbers with both labels; today it has two numbers with one label.

---

# PART 4 — How many others are affected

## Cause A: the BL-698 display-rule change (deployed 2026-08-03)

All 28 clippers whose owner-side and clipper-side figures currently disagree. `retired_7d` is the earnings retired inside the last 7 days.

| Clipper | Owner sees | Clipper sees | Gap | Retired in 7d |
|---|---|---|---|---|
| cmps3tgl | $147.61 | $0.00 | $147.61 | $0.00 |
| cmponzpo | $86.48 | $26.42 | $60.06 | $0.00 |
| cmpbazci | $34.52 | $0.28 | $34.24 | $0.00 |
| cmpe951o | $34.23 | $0.00 | $34.23 | $0.00 |
| cmr1rz2j | $19.09 | $0.00 | $19.09 | $0.00 |
| cmpfp1mw | $18.52 | $0.00 | $18.52 | $0.00 |
| cmp7153e | $15.45 | $0.00 | $15.45 | $0.00 |
| cmqgqnw4 | $18.68 | $6.06 | $12.62 | $0.64 |
| cmp75zkf | $13.25 | $2.68 | $10.57 | $0.00 |
| cmpfozzs | $6.76 | $0.00 | $6.76 | $0.00 |
| **Clipper B** | **$6.04** | **$0.00** | **$6.04** | **$8.07** |
| cmp7ic4p | $4.92 | $0.00 | $4.92 | $0.00 |
| cmp5a6k0 | $5.21 | $1.45 | $3.76 | $0.00 |
| cmpfn1e5 | $4.00 | $0.88 | $3.12 | $0.00 |
| cmp5j44i | $2.99 | $0.00 | $2.99 | $0.00 |
| cmoibh57 | $2.82 | $0.00 | $2.82 | $0.00 |
| cmp48eh8 | $2.76 | $0.00 | $2.76 | $0.00 |
| cmpb8lbj | $2.42 | $0.00 | $2.42 | $0.00 |
| cmoagj49 | $6.35 | $4.23 | $2.12 | $0.00 |
| cmqv7svp | $8.60 | $6.72 | $1.88 | $1.88 |
| cmpqxvna | $15.89 | $14.38 | $1.51 | $0.00 |
| cmpl310f | $1.41 | $0.00 | $1.41 | $17.46 |
| cmq2is2j | $1.38 | $0.00 | $1.38 | $0.00 |
| cmn4nlfg | $212.65 | $211.39 | $1.26 | $1.26 |
| cmogxget | $0.96 | $0.00 | $0.96 | $0.00 |
| cmosmyqk | $1.46 | $0.52 | $0.94 | $0.00 |
| cmr1bsip | $0.34 | $0.00 | $0.34 | $10.51 |
| cmp71p89 | $0.08 | $0.00 | $0.08 | $0.00 |
| **28 clippers** | **$2,811.12** (subset) | | **$399.86** | |

**Clipper B is confirmed among BL-702's 26.** BL-698's own report names his account prefix with a $3.31 drop at deploy; today his standing gap is $6.04. **Clipper A is confirmed NOT among them, and the reason is measured, not assumed: he has zero clips with `videoUnavailable = true`.**

## Cause B: videos retired inside the 7-day window

12 clippers had 50 clips retired between 2026-07-30 06:00:52.159 and 2026-08-05 06:00:39.931, carrying $39.82. Six of those had earnings of exactly $0.00 already. The displayed balance actually lost:

| Clipper | Retired earnings 7d | Displayed before | Displayed after | Drop |
|---|---|---|---|---|
| **Clipper B** | $8.07 | $3.67 | $0.00 | **$3.67** |
| cmqv7svp | $1.88 | $8.60 | $6.72 | $1.88 |
| cmn4nlfg | $1.26 | $212.65 | $211.39 | $1.26 |
| cmqgqnw4 | $0.64 | $6.70 | $6.06 | $0.64 |
| cmr1bsip | $10.51 | $0.34 | $0.00 | $0.34 |
| cmpl310f | $17.46 | $0.00 | $0.00 | $0.00 |
| **Total** | | | | **$7.79** |

Before 2026-08-03 these retirements were invisible on the clipper display; after BL-698 they land immediately. This is the new steady state, roughly $8 per week at current rates.

## Cause C: a DIFFERENT cause, and it is a second bug

Clippers whose recorded lifetime earnings on a campaign have fallen **below** what they were already paid on that campaign. Nothing to do with `videoUnavailable`; these all use the retired-inclusive basis.

| Clipper | Campaign | Earned now | Paid | Overpaid | Campaign at budget cap | Moved inside 7d |
|---|---|---|---|---|---|---|
| **Clipper A** | STRAENGE | $1,833.67 | $1,894.14 | **$60.47** | **YES ($3,002.25 / $3,000)** | **YES, 2026-08-01 06:31:33.775** |
| cmofpudr | somesome | $1,570.58 | $1,607.33 | $36.75 | no ($8,804.53 / $9,750) | no (paused 2026-06-22) |
| cmoaejuc | somesome | $38.80 | $61.89 | $23.09 | no | no |
| cmq0qn2l | GainzAlgo (REPOST) | $0.00 | $14.46 | $14.46 | no ($594.00 / $2,000) | no (paused 2026-07-23) |
| cmoal818 | somesome | $4.94 | $12.76 | $7.82 | no | no |
| cmova7yd | BAD BITCH ANTHEM | $29.19 | $30.00 | $0.81 | no | no |
| cmp71p89 | somesome | $33.99 | $34.79 | $0.80 | no | no |
| cmqmnvgs | WinGram | $11.21 | $11.23 | $0.02 | no | no |
| **Total** | | | | **$144.22** | | |

**Clipper A is the only clipper whose decrease inside the 7-day window came from a cause other than `videoUnavailable`, and it is a second, previously unknown bug.** The other seven are older and pre-date this window; `cmofpudr` at $36.75 is the case BL-692 already verified stays correctly capped at $0.00. Note also that cmq0qn2l was banned (`USER_BAN_TRACKING_CASCADE`, 2026-06-08 16:02:27.42), which explains their $0.00 earned differently.

**What could not be measured.** The STRAENGE ceiling re-application on 2026-08-01 will have reduced recorded earnings for up to **16 clippers**, not just Clipper A ($650.81 campaign-wide against the uncapped model). Only Clipper A shows as an "overpayment" because only Clipper A had been paid. The other 15 simply watched their balance fall, and **no query can measure that decrease, because the platform stores no earnings history.** If any of them complains this week, this is why.

---

# PART 5 — Clipper B's oddity, and Clipper A's identity

## Is Clipper B paid more than he earned? Only on one basis, and it is the display basis

```
Paid                              $114.16
Live earned  (clipper display)    $109.76   -> paid exceeds earned by $4.40
Lifetime earned (owner, actual)   $120.20   -> earned exceeds paid by $6.04
```

**His payouts are legitimate and no error occurred.** Every one of the three payouts was requested and approved while the funding clips were live, and the gate at `payouts/route.ts:424` refused everything else. The apparent overpayment is created *by the display basis*, not by any payment. He is not in BL-627's over-held group and not in BL-690's list (C-1 `cmpl310f`, C-2 `cmpfozzs`, C-3 = Clipper A). Nothing should be clawed back and nothing should be adjusted.

## Is the owner's $6.04 real money owed?

**No. It is an artefact.** The whole of it, and more, is retired-video earnings the clipper can never reach:

```
Owner's unpaid                                     $6.04
Retired-clip earnings inside that figure          $10.44
Reachable remainder                               $0.00   (floored)
```

Every path is closed: the per-campaign gate (`payouts:424`) excludes the retired clips, giving `max(109.76 − 114.16, 0) = $0.00`; the global clamp (`payouts:589`) takes `min(0.00, 6.04) = $0.00`; and the $10 minimum (`payouts:271`) would refuse it even if it were reachable. **If the owner pays $6.04 he is paying, out of pocket, for videos that no longer exist.** That may still be a decision he wants to make as goodwill, but it is a gift, not a settlement, and it should be recorded as one so this audit's successor does not read it as a debt paid.

## Is Clipper A the same account as BL-690's over-held clipper?

**Yes, confirmed to the cent.** BL-690's C-3 was paid $1,894.14 against $1,848.32 earned, overpaid $45.82, and was described as having *"no retired clips whatsoever"*. Clipper A's single PAID payout is $1,894.14, and he still has zero retired clips today. The account prefix in BL-690's published table matches.

Two things have changed since BL-690, and both matter:

1. **The overpayment grew from $45.82 to $60.47** while BL-690 attributed it to nothing in particular. BL-690's stated lifetime earned of $1,848.32 versus today's $2,239.29 is Panic Baby growth; the STRAENGE side has moved the other way. BL-690's conclusion, *"C-3 is not a victim of the asymmetry, he has no retired clips whatsoever"*, was correct about the asymmetry and, understandably, stopped there. It did not ask **why** a clipper with no retired clips was overpaid at all. This audit answers that: the budget ceiling rewrote his paid-for earnings downward.
2. **BL-690's recommended fix does not help him.** Option D (adopted as BL-692) changed the clamp's earnings base to lifetime-including-retired. Clipper A has no retired clips, so his base did not move by a cent, and BL-692 explicitly and correctly verified that overpaid clippers stay at $0.00. His $60.47 is untouched by every round since.

---

# PART 6 — The verdict, written for the owner to send

## One line

**Neither clipper is missing money they were owed today, but Clipper A is having $60.47 of live, genuinely-earned campaign money withheld to recover an overpayment the platform created itself, and that is ours to fix, not his.**

## Message for Clipper A (paste as-is)

> Hi, thanks for flagging this and sorry it took a few days.
>
> I looked at your account properly. Nothing has been taken from you and nothing has been lost. Here is exactly what is going on.
>
> Back on 7 July you cashed out $1,894.14 from STRAENGE, and that was paid to you in full. Since then, STRAENGE has reached its total budget of $3,000. When a campaign reaches its budget, the pool stops growing and everyone's recorded earnings on it get fitted back inside what the campaign actually has. That happened again on 1 August, and it pushed your recorded STRAENGE total down to $1,833.67, which is about $60 less than we had already paid you.
>
> You keep every cent of that payment. That is not in question.
>
> What is happening now is that our system is quietly taking that $60 difference off what you can withdraw from Panic Baby. So Panic Baby shows you $405.62 earned, but the cash-out screen only lets you take $345.15, and that $60 gap is the bit that looks like it vanished. Your maths was right and the number really is stuck.
>
> That is our problem, not yours. It came from how we handle a campaign hitting its budget after someone has already been paid, and you did nothing wrong. Your Panic Baby earnings are real and they are still growing.
>
> Right now you can withdraw $345.15, which comes to $314.09 after the 9% payout fee. I am also looking at whether the remaining $60.47 should be released to you rather than held back, and I will come back to you on that either way rather than leaving it sitting there.

## Message for Clipper B (paste as-is)

> Hi, thanks for the message and sorry for the confusion.
>
> I checked your account. Nothing has been taken from you, and you have not been penalised for anything.
>
> Twelve of your clips have had their videos come down from the platforms, spread across 18 to 31 July. When a video is no longer online we cannot bill the client for it, so those earnings stop counting toward what you can cash out. That has always been the rule at the cash-out step. The problem was that your earnings page was still adding those clips into the balance it showed you, so the page was showing you roughly $6 that the cash-out screen was never going to release. We fixed the page on 3 August so the two agree, and that is why your balance appeared to drop. The money did not go anywhere, because it was never reachable in the first place. That was our display being wrong, not your earnings changing.
>
> Your three payouts, $11.34, $12.82 and $90.00, were all paid correctly and in full. Nothing there is affected and nothing is being taken back.
>
> On the earnings figures: your live clips currently sit at $109.76 and you have been paid $114.16, which is why the available balance reads $0.00. Your clips that are still up are still earning, so that will move again as views come in.
>
> Two honest notes. Your account still shows about $6 on my side, and that is our admin screen counting the taken-down videos when it should not. I am fixing that screen. And the $95.67 you quoted does not match any figure I can find in our system, so if you can send me a screenshot I would like to see exactly which number you were reading, because if a screen is showing something wrong I want to know.

## Ranked fix list

**Money defects (a clipper is being denied money they genuinely earned):**

1. **Clipper A's $60.47, and the mechanism behind it.** `src/app/api/payouts/route.ts:566-589` and `src/app/api/earnings/route.ts:259`. The global clamp subtracts a payment in full while the earnings that justified it can be rewritten downward afterwards by the campaign budget ceiling. **Which surface should change: the clamp.** It should net against what was *earned at the time of payment*, not against a figure the ceiling can retroactively shrink. The cheapest correct shape is to record a per-payout `earnedAtPaymentSnapshot` and clamp against `max(lifetimeEarned, Σ earnedAtPayment)`. Do **not** simply disable `GLOBAL_PAYOUT_CLAMP_ENABLED`: BL-690 already established that turning it off removes overpayment protection entirely. Owner decision required, because releasing the $60.47 means Panic Baby funds a STRAENGE shortfall. Blast radius today: **1 clipper, $60.47**, with 7 older cases totalling $83.75 that would need the same policy call.
2. **No earnings history exists.** There is no table, and `savedEarnings` is only written on the freeze paths. Every question in this audit that could not be answered failed on this. An append-only `clip_earnings_history` row on each `writeClipEarnings` call would have made both of these reports a ten-minute lookup. **Which surface should change: `src/lib/clip-earnings-writer.ts`, additively.**
3. **Up to 15 other STRAENGE clippers saw an unmeasurable decrease on 2026-08-01.** No fix, but they should be expected, and item 2 is what prevents the next one being unmeasurable too.

**Display disagreements (nobody is owed money, but the screens contradict each other):**

4. **$399.86 across 28 clippers: the owner's admin shows unpaid money no clipper can withdraw.** `src/app/api/admin/payouts/user/[id]/route.ts:87` and `src/app/api/admin/payouts/unpaid/route.ts:34`. **Which surface should change: the two admin routes.** They should either apply `videoUnavailable: false` to match the gate, or, better, return both figures with distinct labels ("lifetime earned" and "payable now") so the historical number is not lost. This is the highest-value fix by count of people affected, because these are the figures the owner quotes to clippers and to clients. Includes Clipper B's $6.04.
5. **The netAfterFee trap on the per-clipper screen.** `src/app/api/admin/payouts/user/[id]/route.ts:173` versus `:213`. The totals row nets off the global unpaid, the campaign rows net off the unclamped per-campaign unpaid, and both render as "after fee". That is how "$345.15 unpaid" and "$369.19 after the 9% fee" ended up in the same sentence when the true net on $345.15 is $314.09. **Which surface should change: the UI at `src/app/(app)/admin/payouts/page.tsx:928-930`,** which should label the per-campaign net as per-campaign or suppress it when a global clamp is binding.
6. **The gate is now looser than the display.** `src/app/api/payouts/route.ts:566-589` (retired included) versus `src/app/api/earnings/route.ts:206` (retired excluded). BL-692's justifying comment at `payouts/route.ts:556-562` cites the pre-BL-698 display and is now factually stale. 4 clippers, $3.60. **Which surface should change: neither number yet, but the comment must be corrected before it misleads the next round.**
7. **The archive view can render a negative unpaid.** `src/app/api/admin/archive/[campaignId]/route.ts:155` has no zero floor and does not subtract locked. It currently renders **−$60.47** for Clipper A. **Which surface should change: the archive route,** though note it is the only place the truth is visible, so give it a label rather than a floor.
8. **Two owner surfaces disagree on marketplace creator earnings.** `admin/payouts/user/[id]:110-116` includes them unfiltered; `admin/payouts/unpaid` omits them. Zero impact on A and B; will bite the first marketplace creator with a retired clip.

**Unresolved question, flagged not answered:**

9. **Clipper B's $95.67 matches no figure the platform can produce**, and sits $8 to $14 below every reconstructable value. Ask him for a screenshot before assuming it was a stale reading.

---

## Safety statement

READ ONLY. One document produced. No source file was modified, so no build was run and none is claimed; a markdown-only change cannot affect `tsc`. No payout was created, modified, approved, rejected or cancelled. No balance, clip status, earnings field or env flag was touched. Every DB statement was a `SELECT` through `scripts/run-select.js`, which rejects `insert`, `update`, `delete`, `drop`, `truncate`, `alter`, `create`, `grant` and `revoke` before it connects. Work was done in an isolated worktree at a short path; `node_modules` was never junctioned; the shared working tree's HEAD was not moved and nothing held by the concurrent BL-713 round was touched. Both handles are redacted and no wallet address appears in this document.

**Stated plainly, what could not be measured:** Clipper A's $213.62 and Clipper B's $95.67 (no balance or earnings history exists to replay either screen); the exact date the global clamp began binding on Clipper A; the size of the 2026-08-01 STRAENGE decrease for the other 15 clippers on that campaign; and whether the 2026-08-01 rewrite was the only one that lowered Clipper A's recorded earnings, or merely the most recent.
