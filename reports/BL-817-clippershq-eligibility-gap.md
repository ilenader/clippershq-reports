# BL-817 — the $5.56 a clipper cannot see, and the 27 clippers behind him

**FIRST LINE, because the brief said a widespread mismatch belongs here: THIS IS NOT ONE MAN'S CONFUSION. 27 clippers see 40 campaign rows today whose two figures do not agree, $2,908.06 of absolute disagreement, and 13 of them see the disagreement sitting directly above a "to go" line that does not account for it. Clipper K is the one who wrote in.**

**2026-08-23 · DB `now()` = `2026-08-23 12:44:45.419568+00` (first read) to `2026-08-23 12:57:51.950845+00` (last) · AUDIT ONLY. READ ONLY.**
No code, data, schema, config or money changed. Nobody paid, no status touched, no balance moved, no payout created, altered, approved or cancelled. Every database access went through `scripts/run-select.js`, which refuses any write keyword before it connects. Every timestamp cast `::text` against DB `now()`. Base `origin/main` @ `484e4d69`, isolated worktree `C:/w817`, a short path, `node_modules` never junctioned, removed at the end of the round. The 6 money files were read and not written; nothing in this round can touch them, because nothing in this round writes.

The clipper is **Clipper K** throughout: id prefix **`cmrl046b`**, `md5` short id **`299618`**, so the owner can map him privately in admin. His handle is redacted and no wallet address was selected or printed.

---

## PART 1 — THE $5.56, TO THE CENT

**Both numbers are right. They measure different things, and nothing on his screen says so.**

| what he sees | value at complaint | value now | where it is produced |
|---|---|---|---|
| the bold figure on the Zhus Edit row | **$24.86** | **$26.67** | `byCampaign.earned`, `EarningsPremium.tsx:88-101`, rendered at `:373` |
| the line under it | **$19.30 of $20.00 minimum • $0.70 to go** | *(no line: he now clears it)* | `balanceOnCampaign(c.row)`, `EarningsPremium.tsx:396` |
| **difference** | **$5.56** | **$5.56** | three retired videos |

### The two queries, traced

**$24.86 comes from `/api/clips/mine`.** The `where` at `clips/mine/route.ts:47-54` filters `isDeleted: false` and `campaign.isArchived: false` and **nothing else**. There is no status filter and, decisively, **no `videoUnavailable` filter**. `EarningsPremium.tsx:88-101` then sums `c.earnings` over every clip whose clipper-facing status is `APPROVED` or `PENDING` and whose `createdAt` falls inside the timeframe. A clip whose video has since disappeared is still in that sum.

**$19.30 comes from `/api/earnings`.** `earnings/route.ts:209` builds `payableClips = clips.filter(c => !c.videoUnavailable)` and passes **that** array to `computeCampaignBalances` (`balance.ts:206-252`), which sums only `status === "APPROVED"` and subtracts paid and locked (`balance.ts:251`). The result is republished as `campaignBalance` at `earnings/route.ts:312` and read back by `balanceOnCampaign` at `below-minimum-campaigns.ts:96-99`.

**So one figure counts retired videos and the other does not. That single difference is the whole $5.56.**

### His three retired clips, named

| clip | earnings | `videoUnavailableSince` (`::text`) | last views seen |
|---|---|---|---|
| `cmsqcg25` | **$2.16** | `2026-08-18 06:00:48.573` | 4,076 at `2026-08-15 08:01:27.739` |
| `cmsrj6lt` | **$0.77** | `2026-08-19 06:00:41.651` | 1,449 at `2026-08-15 10:11:20.484` |
| `cmsrk60z` | **$2.63** | `2026-08-22 06:03:29.529` | 4,914 at `2026-08-19 03:20:51.170` |
| | **$5.56** | | |

### Every other candidate, tested rather than assumed

| candidate | contribution | how it was tested |
|---|---|---|
| **earnings on `videoUnavailable` clips (BL-698)** | **+$5.56** | the three clips above, summed individually |
| already requested or locked in a pending payout | **$0.00** | he has **zero** open payout rows on Zhus Edit; `paid = 0`, `locked = 0` |
| the BL-187-P2 global clamp | **$0.00** | his global available is **$99.10**; `min(21.11, 99.10) = 21.11`, so the clamp never binds. The gate's own clamp base (lifetime, `payouts/route.ts:667`) is looser still at **$107.58** |
| BL-765's per-campaign clamp | **$0.00** | same measurement. `available` and `campaignBalance` are equal for him on every campaign |
| REJECTED clips counted on one side | **$0.00** | he has 4 REJECTED clips on this campaign and **all four carry `earnings = 0`**, including two with real views (1,434 and 1,347) |
| gross versus cash (BL-813) | **$0.00** | neither figure passes through a fee. The 9% appears only at payout time, and `Paid out, before fees` is a separate tile |
| the "This period" timeframe scope | **$0.00** | all 27 of his Zhus Edit clips were created between `2026-08-12 13:44:17.445` and `2026-08-21 16:58:49.142`, inside both the 30 day desktop default and the 15 day mobile default. Earned is $26.67 at 15, 30 and all time |
| rounding | **$0.00** | `26.67 − 21.11 = 5.56` exactly; both sides `round2` |

### Summed independently from views and each clip's own stamped CPM

Not read off a stored total. For each of his 23 APPROVED clips I took the latest `clip_stats.views`, multiplied by that clip's **own** `cpmAtSubmissionDecimal` (all 23 stamped `0.5000`), applied that clip's own `minViewsAtApproval` (1,000) and its own `bonusPercent` (6, 7 or 8 by streak level):

`base = round(views ÷ 1000 × 0.50, 2)` and `earnings = base + round(base × pct ÷ 100, 2)`

Summed: **base $24.92 + bonus $1.75 = $26.67**, matching the stored total to the cent, and the earnings invariant `earnings ≈ base + bonus` holds on **all 300 of his clips, 0 violations**. Four clips with 135, 169, 233 and 472 views correctly earn **$0.00**, because they are under the 1,000 view floor.

**One clip disagrees by one cent and I am naming it rather than smoothing it.** `cmt36wdm` shows 3,352 views at `2026-08-23 05:21:41.441`, which recomputes to $1.68 base against a stored $1.67. That is a stats row newer than the last earnings write, not a defect, and it is the entire residual in a $26.67 total.

### Which number is right

**Both. Neither is wrong.** $26.67 is what his clips have earned. $21.11 is what the platform will pay for, because three of those videos are no longer there and the withdrawal gate has excluded retired clips since long before any of this (`payouts/route.ts:362`, `:524`). **The defect is not in either number. It is that the screen prints them two centimetres apart and reconciles them nowhere.**

---

## PART 2 — HE WAS RIGHT, AND THE GAP IS NOT WHAT BLOCKED HIM

**He said he believed he had already passed $20.00. He had. Twice.**

Reconstructed at three hour resolution from `clip_stats` views × each clip's own stamped CPM, calibrated against today's live figures ($21.12 reconstructed against $21.11 stored, a one cent residual):

| moment (UTC, `::text`) | earned shown | eligibility | gap | versus the $20.00 minimum |
|---|---|---|---|---|
| `2026-08-17 00:00` | $16.01 | $16.01 | $0.00 | below |
| `2026-08-18 09:00` | $19.89 | $17.73 | $2.16 | below · **`cmsqcg25` retired at 06:00:48** |
| `2026-08-19 00:00` | $22.71 | **$20.55** | $2.16 | **CLEARS** |
| `2026-08-19 09:00` | $22.87 | $19.94 | $2.93 | below · **`cmsrj6lt` retired at 06:00:41** |
| `2026-08-20 00:00` → `2026-08-22 06:00` | $22.93 → $24.85 | **$20.00 → $21.92** | $2.93 | **CLEARS, for 54 hours** |
| `2026-08-22 09:00` | $24.85 | $19.29 | $5.56 | below · **`cmsrk60z` retired at 06:03:29** |
| **`2026-08-22 12:00`** | **$24.86** | **$19.30** | **$5.56** | **below · this is the screen he complained about** |
| `2026-08-22 21:00` | $26.67 | $21.11 | $5.56 | **CLEARS** |
| `2026-08-23 12:00` | $26.68 | $21.12 | $5.56 | **CLEARS** |

The reconstruction lands on **$24.86 and $19.30** at `2026-08-22 12:00`, the owner's two reported figures, to the cent, from views and stamped CPMs alone.

**So the gap has grown, in three steps, and it has never shrunk.** $0.00, then $2.16, then $2.93, then $5.56. It is a ratchet: a retired clip's earnings freeze and the exclusion is permanent unless the video comes back.

**But the gap is not the thing that blocked him, and this matters.** He crossed $20.00 on `2026-08-19`, was pushed back under six hours later by a $0.77 retirement, crossed again and held it for 54 hours, and was pushed back under on `2026-08-22 06:03` by a $2.63 retirement. He wrote in during that third window. **He was not wrong about having passed the line. He had passed it, and a deleted video moved it back under him while he was not looking.**

### Is it structural

**No, and this is the honest answer rather than the dramatic one.** BL-765 found 93 of 139 blocked positions on campaigns that can never accrue again. **Clipper K is not in that population.** Zhus Edit is `ACTIVE` and not archived, `canAccrue` is true, and his balance grew from $16.01 to $21.12 in six and a half days, about **$0.79 per day net of retirements** against **$1.64 per day gross**.

**As of `2026-08-23 12:57:51+00` his Zhus Edit balance is $21.11 against a $20.00 minimum. He needs $0.00 more. He can request a payout on it today.**

**What IS structural is the $5.56 itself.** The daily sweep excludes retired clips at the where clause (`tracking.ts:3593`, `videoUnavailable: false`), so nothing automatic will ever re poll them, and `/api/admin/clips/[id]/track-now` refuses them outright at `:174-177` with `VIDEO_UNAVAILABLE`. **The one route back is `/api/admin/clips/[id]/force-now`, which allows them deliberately (`:153`, "revival path"); if views return, `tracking.ts:1730-1747` clears the flag and recomputes through `writeClipEarnings`.** Three clips, one owner click each. Nothing in this round pressed it.

---

## PART 3 — IT IS NOT ONE CLIPPER

Measured across the whole live population at `2026-08-23 12:52:14.927536+00`, reproducing exactly what the earnings page renders: a campaign row exists for every clipper with `APPROVED` or `PENDING` clips created in the last 30 days on a non archived, non test campaign summing above zero.

| | rows | clippers | absolute disagreement |
|---|---|---|---|
| campaign rows rendered | 87 | 56 | |
| **rows where the two figures disagree** | **40** | **27** | **$2,908.06** |
| of those, rows also showing the "to go" reminder | **19** | **13** | **$1,301.43** |

### Causes, and the decomposition closes exactly

`earned − eligibility = retired + pending − outside the window + paid + locked`, and the components sum to the measured net of **$2,763.52** with **no residual**:

| cause | all 40 rows | the 19 reminder rows |
|---|---|---|
| **already paid out** | **+$2,697.66** | **+$1,146.26** |
| locked in a pending payout | +$287.91 | +$247.13 |
| **earnings on retired videos (Clipper K's cause)** | **+$85.85** | **+$15.51** |
| clips older than the 30 day window | −$307.90 | −$107.47 |
| PENDING or FLAGGED clips | $0.00 | $0.00 |
| **net** | **+$2,763.52** | **+$1,301.43** |

**Clipper K's cause is the minority one.** The dominant reason a clipper sees two numbers that disagree is that **he has already been paid** and the earned figure never says so. The worst rows, redacted:

| id8 | md6 | earned shown | eligibility | gap | dominant cause | reminder |
|---|---|---|---|---|---|---|
| `cmrujf29` | `143d15` | $949.30 | $457.39 | $491.91 | paid $491.54 | no |
| `cmqez5c2` | `dfb43b` | $460.11 | $60.47 | $399.64 | paid $399.64 | **yes** |
| **`cmrl046b`** | **`299618`** | **$390.42** | **$0.00** | **$390.42** | paid $390.42 | no |
| `cmn4nlfg` | `a92aea` | $196.94 | $0.18 | $196.76 | paid $195.80 | **yes** |
| `cmsiyg70` | `565879` | $140.48 | $1.67 | $138.81 | paid $78.54, locked $60.27 | **yes** |
| `cmovgvov` | `951ba8` | $28.56 | **$91.32** | **−$62.76** | $62.76 outside the window | no |

**Clipper K appears in that table for a second campaign.** His bees.n.honey row reads **$390.42 earned** against a balance of **$0.00**, with nothing on the row saying he was paid every cent of it on `2026-08-01` and `2026-08-07`. He sees three campaign rows and two of them disagree.

`cmovgvov` is the case that proves this is a display defect rather than a money one: his balance is **larger** than his earned figure, because $62.76 of his clips are older than the 30 day window.

### Against the earlier measurements

| | pairs | clippers | dollars |
|---|---|---|---|
| below the campaign minimum, BL-728 → BL-735 → BL-758 | 111 → 128 → 139 | | $324.33 → **$400.69** → $426.41 |
| **below the campaign minimum, today** | **159** | **125** | **$551.62** |
| of which on a campaign that can never accrue again | 107 | | $314.84 |
| **unreachable in total, BL-758 → today** | | 130 → **143** | $830.02 → **$989.83** |

Both are still rising, at roughly the rate BL-758 recorded. A **third** campaign now carries a custom minimum: `SomeSome App` at $15.0000, alongside the two Zhus campaigns at $20.0000.

**This mismatch is NOT a subset of either.** Only **$85.85** of the $2,908.06 is money anybody is being kept from; **$2,985.57** of it (paid plus locked) is money that has already moved or is already requested. It is a new and different finding: **a display disagreement, not blocked money.**

**Stated plainly as a limitation:** the two unreachable buckets, retired video **$492.19** and below minimum **$551.62**, sum to $1,043.81 against a strict waterfall total of **$989.83**. The $53.98 overlap is the clamp asymmetry BL-765 named (the gate clamps on the lifetime base including retired money while the display clamps on the payable base); recomputing with the display's base accounts for $28.92 of it and leaves **$25.06 I did not decompose further**. I am naming it rather than rounding it away.

---

## PART 4 — WHAT HIS SCREEN LITERALLY SAID, AND WHY HE WROTE IN

Reconstructed from the live payload and the shipped components, at `2026-08-22 12:00` UTC:

> **Available for payout**
> **$84.42**
> All time balance
>
> *Clips whose video is not available cannot be paid, so they are not counted in this balance. Money you were already paid stays yours. Your other clips keep earning as normal.* → *See which clips are affected*
>
> *$19.30 of this is on a campaign that is under the minimum withdrawal so far. Each campaign sets its own.* → *See what each campaign still needs*
>
> **Earnings by campaign** · *This period*
> bees.n.honey · 68 clips · **$401.40**
> Zhus Meme (0.20 CPM) · 199 clips · **$89.48**
> **Zhus Edit (0.50 CPM) · 23 clips · $24.86**
> **│ $19.30 of $20.00 minimum • $0.70 to go**

**Four figures for one campaign and no arithmetic between any of them.** $84.42, $24.86, $19.30, $0.70. The BL-698 sentence that would explain the difference **does render for him** (his `removedFromBalance` is $8.48, above the zero gate at `EarningsPremium.tsx:180`), but it sits **in the hero, attached to the global balance, 400 pixels above the row it explains, and it names no amount**. It cannot connect $24.86 to $19.30 because it never mentions either.

The `sr-only` sentence at `:411-419` is no better. A screen reader hears *"23 clips, $24.86 earned in the period shown. This campaign has a $20.00 minimum withdrawal and you have $19.30 available on it. You need $0.70 more."* Both clauses correctly name their own scope, which is BL-765's fix and it works, **and it still does not say where the other $5.56 went**, because the scope is not what is missing. In his case the two scopes are identical: every one of his 27 clips is inside both the 15 day and the 30 day window.

**The payouts page is clean and is not the problem.** `PayoutsRedesign.tsx:437-470` renders balance, minimum and shortfall and never shows an earned figure, so the two numbers never meet there.

**This is the real defect. The arithmetic is sound and the display fails to explain itself.** BL-762 was written because a clipper opened a support ticket over an unexplained $0.00. BL-765 was written because BL-762's explanation never rendered for the man it was for. **BL-817 is the same class again, one layer out: the explanation renders, and it is not next to the numbers it explains.**

---

## PART 5 — WHAT HE IS ACTUALLY OWED

Computed independently from clip rows, never from a stored summary. `2026-08-23 12:57:51+00`.

| | |
|---|---|
| lifetime approved earnings, all campaigns | **$519.25** across 300 clips |
| of which on videos that no longer exist | **$8.48** across 44 clips |
| **payable lifetime earnings** | **$510.77** |
| **paid to date, GROSS off his balance** | **$411.67** across 3 payouts |
| **paid to date, CASH he actually received** | **$372.62** |
| in flight right now | **$0.00** |
| earnings invariant violations | **0 of 300** |

**Per campaign, right now:**

| campaign | status | earned | payable | paid | **balance** | minimum | verdict |
|---|---|---|---|---|---|---|---|
| Zhus Meme (0.20 CPM) | ACTIVE | $102.16 | $99.24 | $21.25 | **$77.99** | $20.00 | **can withdraw** |
| **Zhus Edit (0.50 CPM)** | ACTIVE | $26.67 | $21.11 | $0.00 | **$21.11** | $20.00 | **can withdraw** |
| bees.n.honey | PAST | $390.42 | $390.42 | $390.42 | $0.00 | $10.00 | fully paid |

**Withdrawable today, GROSS $99.10. CASH after the 9% platform fee, $90.18.** He is not referred, so the fee is 9 and not 4 (`payouts/route.ts:405`). Per campaign, exactly as `calculatePayoutBreakdown` computes it (`payout-calc.ts:61,83`): Zhus Meme **$77.99 gross, $7.02 fee, $70.97 cash**; Zhus Edit **$21.11 gross, $1.90 fee, $19.21 cash**. Both clear `SOLANA_MIN_NET_USD` of $12, so either chain works. Express would add a further 4%.

**He can request a payout today, on both campaigns.** Nothing blocks him: role CLIPPER, no marketplace ban, no open payout row, and the global clamp is not binding.

**His payout history: three requests, all PAID, none ever rejected, voided or adjusted.**

| campaign | gross | fee | express | cash | requested (`::text`) | paid (`::text`) |
|---|---|---|---|---|---|---|
| bees.n.honey | $50.00 | $4.50 | $2.00 | **$43.50** | `2026-07-30 14:20:38.043` | `2026-08-01 11:10:51.892` |
| bees.n.honey | $340.42 | $30.64 | none | **$309.78** | `2026-08-06 01:05:03.441` | `2026-08-07 12:17:20.820` |
| Zhus Meme (0.20 CPM) | $21.25 | $1.91 | none | **$19.34** | `2026-08-09 17:13:35.341` | `2026-08-13 20:34:37.016` |

**He already knows how to withdraw and has done it three times, most recently under the $20.00 minimum on the other Zhus campaign.** That is the sharpest fact in this report: **he has been sitting on $77.99 of withdrawable money on Zhus Meme the entire time he was writing in about $0.70 on Zhus Edit.** His screen offers no reason to notice, because the row that can be withdrawn is the one carrying no message at all.

---

## PART 6 — THE VERDICT, THE REPLY, AND THE FIX SPEC

**The platform is calculating correctly to the cent, Clipper K is owed nothing he cannot reach, and $5.56 of his earnings will never be payable because three of his videos are gone.**

### The reply the owner can send

> Hey, thanks for flagging this and sorry it looked broken.
>
> Both numbers on your screen are real, they just measure two different things, and the page does a poor job of saying so.
>
> The **$24.86** is everything your Zhus Edit clips have earned. The **$19.30** is the part we can actually pay you for. Three of those clips are on videos that are no longer available on the platform they were posted to, and those three add up to **$5.56**. We cannot bill for a video that is not there, so they come out of the payable side. Nothing was taken from you and nothing was a penalty, and every dollar we have already sent you stays yours.
>
> You are also right that you had passed $20. You crossed it on the 19th and you were over it again for most of the 20th and 21st. On the morning of the 22nd one more video went unavailable, $2.63 came off the payable side, and that dropped you to $19.30. That is why it kept feeling like it moved away from you.
>
> **Good news: you are over it again.** Right now you have **$21.11** on Zhus Edit, above the $20.00 minimum, so you can request that one today. You also have **$77.99** sitting ready on Zhus Meme, well over its minimum, which you can request right now as well. Together that is **$99.10**, which comes to **$90.18** after the 9% fee.
>
> I am going to have the page state this properly so nobody has to ask. If you want, send me the three clip links and I will re check whether the videos are back, and if they are, the earnings come straight back on.

Threshold and mechanism only, no judgement, no implication he did anything wrong, and nothing that invites a retry that cannot succeed. BL-518 and BL-521.

### The fix spec, and neither was performed

**A. A calculation defect. There is none.** Every figure reproduces from views and stamped CPMs. Invariant 0 across all 300 of his clips and 0 across the platform. The gate, the clamp, the fee and the minimum all behave exactly as written. **Nothing to fix here, and the round should not invent one.**

**B. A display that does not explain itself. This is the whole finding, and it is the higher value fix by a wide margin,** because it is the one that stops the next ticket, and because 27 clippers are standing behind Clipper K holding 40 rows of it.

| # | site | change |
|---|---|---|
| **B1** | `EarningsPremium.tsx:373` | the row's bold figure is `byCampaign.earned` and carries no label at all. Label it in words, the way BL-813 labelled the payout card: **`Earned this period`**. A bare number beside a different bare number is the defect in one line. |
| **B2** | `EarningsPremium.tsx:388-405` | when `earned` and `balanceOnCampaign(row)` differ, print **one reconciling clause** on the row, built from figures `/api/earnings` already returns. For Clipper K: `$26.67 earned, less $5.56 on videos that are no longer available, leaves $21.11 toward the $20.00 minimum.` The retired amount must be **per campaign**, which the payload does not carry yet (see B4). |
| **B3** | `EarningsPremium.tsx:396,412-419` | the visible reminder is `aria-hidden` and the `sr-only` sentence states both figures without reconciling them. Whatever B2 adds must land in **both**, or a screen reader user is left exactly where he started. |
| **B4** | `earnings/route.ts:224-226, 292-316` | `unavailableClips.removedFromBalance` is a single **global** number, which is why the hero note cannot be attached to a row. Add a **per campaign** `removedFromBalance` to `enrichedBalances`, computed the same way (`computeCampaignBalances(clips)` minus `computeCampaignBalances(payableClips)`). Additive, display only, decides no money. |
| **B5** | `EarningsPremium.tsx:373` | a fully paid campaign row (his bees.n.honey, **$390.42 against $0.00**) is the largest single instance of this defect on the platform, at $2,697.66 across 40 rows. It needs the same treatment: `less $390.42 already paid out`. |
| **B6** | `EarningsPremium.tsx:331` | `This period` is an 11px muted string in the card header and it is the only thing distinguishing a period scoped figure from an all time one. It carried none of the weight for Clipper K, whose scopes are identical, and it will not carry it for `cmovgvov`, whose balance is **larger** than his earned figure. Say it on the row, not in the header. |

**Higher value: B1, B2 and B4 together.** B1 alone stops the number being anonymous; B2 is the sentence that answers the question; B4 is the only thing that makes B2 possible without a second query. Nothing here touches a gate, a minimum, a balance or a money file, and no clipper becomes newly able or unable to withdraw.

**Reported, not fixed, and out of this round's scope:** `EarningsPremium.tsx:181-185` still hardcodes `bg-white/[0.04]` and `text-white/80` for the BL-698 note, which BL-762 and BL-765 both recorded as white on white in the live light theme. It is now the sentence that would carry B2's meaning, so it should be tokenised before it is leant on.

---

## WHAT COULD NOT BE MEASURED, STATED PLAINLY

• **I ran no browser and captured no screenshot.** The clipper earnings page sits behind a Discord OAuth session I do not have. PART 4's rendering is derived from live database values passed through the same functions the shipped components call, and from reading the components line by line. It is a derivation, not a photograph, and it should be read as one.
• **The historical series in PART 2 is a reconstruction.** Stored earnings are overwritten in place, so no historical earnings figure exists to read. It is rebuilt from `clip_stats` views × each clip's own stamped CPM, bonus percent and view floor. It calibrates against today's live figures to **$0.01 on Zhus Edit** and **$0.04 on Zhus Meme**, which is why I trust it for both, and it **overshoots bees.n.honey by $10.98** ($401.40 reconstructed against $390.42 stored), because that is a finished campaign carrying pool trims and frozen earnings that views alone cannot reproduce. **No bees.n.honey reconstruction is used for any conclusion.**
• **$25.06 of the bucket overlap in PART 3 is unattributed.** Named above rather than absorbed.
• **The three retired videos were not checked against the platforms they were posted to.** No Apify actor ran, no paid API was called, and spend for this round is **$0.00**. Whether those videos are genuinely gone or merely private, region locked or age gated is exactly the ambiguity BL-720 narrowed going forward and could not resolve backwards. **Only `force-now` can answer it, and I did not press it.**

---

## VERIFICATION

Read only throughout. No code, data, schema, config or money changed; nobody was paid; no clip status, balance, earnings value or payout row was touched; every read went through `scripts/run-select.js`, which refuses any write keyword before connecting; every timestamp cast `::text` against DB `now()`. The $5.56 is explained to the cent and both figures traced to the query and the file:line that produce them, with `videoUnavailable`, locked payout amounts, the global clamp, BL-765's per campaign clamp, REJECTED clips, gross versus cash and rounding each tested explicitly and each returning its measured contribution rather than an assumption. His 23 APPROVED Zhus Edit clips were summed independently from `clip_stats` views and each clip's own stamped `0.5000` CPM, own `bonusPercent` and own 1,000 view floor, reproducing $26.67 with a single one cent residual that is named. Both figures are correct and measure different things, and that is stated. The 30 day series is charted at three hour resolution, cast `::text`, and lands on the owner's exact $24.86 and $19.30 at `2026-08-22 12:00`; the gap is a permanent ratchet and the block is not, and he clears the minimum today with $21.11 against $20.00. The platform wide measurement is in the first line: **40 rows, 27 clippers, $2,908.06**, with the cause decomposition closing to $0.00 residual, and re measured against 128 pairs / $400.69 (now 159 / $551.62) and $830.02 / 130 clippers (now $989.83 / 143). What his screen renders is quoted and the unexplaining display is named as the real defect. His independently computed earnings, paid, and withdrawable **gross $99.10 and cash $90.18** are all stated, along with three PAID payouts and no refusals. The verdict is one line, the reply is plain and non accusatory, and the fix spec separates a calculation defect (there is none) from a display that fails to explain itself (there is), names B1 + B2 + B4 as the higher value fix, and **performs neither**. The handle is redacted, no wallet address was selected or printed, the worktree at `C:/w817` is removed, and no build was run because this round contains no code. **No dashes as bullets.**
