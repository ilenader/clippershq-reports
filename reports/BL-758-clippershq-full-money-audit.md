# BL-758 — the complete money audit: who is owed, who cannot reach it, and whether the arithmetic is right

**2026-08-10 · DB now() = `2026-08-10 13:26:52.075966+00` · AUDIT ONLY. READ ONLY.**
No code, data, schema, config or money changed. Nobody paid. No payout created or altered. No balance touched, nothing restamped, retired or revived. `agency-monitor --fix` never run. No platform-wide owner re-derive. No Apify actor and no paid API probe of any kind: **spend for this round is $0.00.** Base `origin/main` @ `018c22ca`, isolated worktree `C:/b758`, worktree clean at exit. Every timestamp cast `::text` against DB `now()`.

Money files unchanged by construction (blob OIDs at `018c22ca`, recorded so a later round can diff): `clip-earnings-writer.ts` `ac5be7de`, `earnings-calc.ts` `797e2098`, `balance.ts` `e887f80a`, `tracking.ts` `83ce4bab`, `clip-earnings-invariant-middleware.ts` `61cef393`, `money-decimal.ts` `ef5cdae7`, plus `campaign-era.ts` `106e16ad` and `cpm.ts` `57240872`.

Clippers are identified by two short ids so the owner can map them privately in admin and cross-reference every earlier round: **`id8`** = first 8 characters of the user id (the form BL-716 / BL-718 / BL-719 / BL-690 used) and **`md6`** = `substr(md5(userId),1,6)` (the form BL-661 / BL-695 / BL-751 used). No handle appears anywhere. No wallet address was selected, printed, or partially printed.

---

## PART 1 — THE HEADLINE

> **$830.02 is owed to clippers who cannot reach it today. It is spread across 130 clippers. The single largest individual amount is $147.61** (clipper `cmps3tgl` / `3159ac`).
>
> **A further $60.47 belongs to one clipper (`cmqez5c2` / `dfb43b`) and is not even counted in that $830.02**, because his own recorded earnings were written below money the platform had already paid him. He is the STRAENGE case of BL-716, still unpaid. **Combined, $890.49.**
>
> **$82.12 is held by 4 clippers ABOVE what they earned.** All four are correctly clamped to $0.00 available. There is no clawback and none is proposed.

Three sentences of context the owner should read before acting.

• The largest single unpaid position on the platform is **not** in that $830.02 at all. Clipper `cmr0gixm` / `11917e` has earned **$569.22**, has been paid **$20.64**, and **$545.37 of the remaining $548.58 is sitting there withdrawable right now on Panic Baby.** He has simply never pressed the button. He is not blocked by anything.

• **$427.23 of the unreachable money is the per-campaign minimum withdrawal doing exactly what it was built to do**, spread thinly over 139 (clipper, campaign) pairs. It is not a defect. The correction below to the figure the owner remembered matters more than the amount.

• **$403.61 is earnings on videos that no longer exist.** Under the owner's stated policy that a deleted video cannot be paid for, that money is **not** genuinely owed. Withholding it is the policy working.

### Platform totals, one snapshot

| | |
|---|---|
| Lifetime earned (APPROVED, live clips, recorded) | **$12,154.11** across 4,308 clips and 248 clippers |
| Of which earnings on videos now unavailable | $3,605.15 (29.7%) |
| Lifetime paid (money that has actually left) | **$8,881.01** across 85 PAID rows |
| In flight right now (requested, awaiting owner) | **$580.81** across 9 rows |
| Still owed on the books | **$3,355.22** |
| Reachable by the clipper today, unaided | **$1,944.39** |
| **Unreachable today** | **$830.02** |
| Held above earnings (no clawback) | $82.12 across 4 clippers |
| Earnings invariant `earnings = base + bonus` | **0 violations across 4,308 clips** |

The identity closes exactly, with no residual: `3,355.22 = 580.81 + 1,944.39 + 830.02`.

---

## PART 2 — EVERY CLIPPER, RECONCILED

### How this was computed, and where it does not trust a stored total

Every figure is rebuilt from the clip rows, not read off a summary. For each clipper and each campaign I recomputed, in SQL, the same arithmetic the withdrawal gate performs in code:

• **Earned** sums `Clip.earnings` over `status = APPROVED AND isDeleted = false`, per campaign. Two variants are kept apart throughout: **payable** (adds `videoUnavailable = false`, the per-campaign gate's base at `payouts/route.ts:515`) and **lifetime** (no such filter, the global clamp's base at `payouts/route.ts:658`).
• **Paid** uses the exact `isPayoutMoneyOut` rule from `balance.ts:117-124` (`PAID` always; `VOIDED` only when `paidAt` is not null) and the exact `clipperLiability` rule from `balance.ts:126-132` (`actualPaidAmount ?? amount`, GROSS, never `finalAmount`).
• **Locked** is `REQUESTED | UNDER_REVIEW | APPROVED` under the same liability rule.
• **Reachable** is `min( Σ per-campaign available that clears that campaign's own minimum , global available )`, which is `effectiveCap` as the gate computes it at `payouts/route.ts:680`, summed over the campaigns a clipper could actually file against.

**An honest limit, stated plainly.** The brief asked for a recompute from views and stamped CPMs. I did not rebuild every clip's dollar value from `clip_stats.views × cpmAtSubmissionDecimal`, and I should say why rather than imply I did. Earnings are not a pure function of current views: they pass through `payoutReductionRatio` (338 clips carry one, immutable once set), `maxPayoutPerClipAtApproval`, `minViewsAtApproval`, per-tick pool-cap trimming that depends on the state of every *other* clipper on the campaign at that tick, and BL-718's `capButNeverBelowStored` floor. A naive `views × CPM` recompute would disagree with the stored value on hundreds of clips **for correct reasons**, and reporting that disagreement as a discrepancy would be worse than not running it. What I did verify structurally is in PART 5: every clip carries its own stamp, the invariant holds on all 4,308, and no campaign is over budget.

### Nobody's paid-plus-claimable exceeds what they earned — BL-627's property, re-verified not inherited

Measured directly on all 254 clippers who have any earnings or any payout row:

• Clippers whose **paid + locked exceeds lifetime earned**: **4**, totalling **$82.12**. Every one of them computes to exactly **$0.00** available and cannot request a cent. The clamp at `balance.ts:200` and the gate's `Math.max(..., 0)` both hold.
• Clippers who could withdraw more than they earned: **0**. **BL-627's no-overpayment property holds.**

| id8 | md6 | earned | paid | held above earnings |
|---|---|---|---|---|
| `cmofpudr` | `2abe41` | $1,570.58 | $1,607.33 | **$36.75** |
| `cmoaejuc` | `f95b37` | $38.80 | $61.89 | **$23.09** |
| `cmq0qn2l` | `fa0da6` | $0.00 | $14.46 | **$14.46** |
| `cmoal818` | `7ef3f3` | $4.94 | $12.76 | **$7.82** |

This population has **shrunk**, not grown: BL-627 measured 5 clippers / $142.59, BL-696 measured 6 / $113.38, BL-719 measured 5 / $82.93, and it now reads 4 / $82.12. The mechanism is the one BL-627 named: a clip that funded a correct payment was later retired or reduced, so the earned side fell after the paid side was already fixed. None of it is recoverable and none should be chased.

### Highest earners who have NOT been paid — the owner asked for these first

| id8 | md6 | earned | paid | in flight | still owed | **can withdraw today** | blocked |
|---|---|---|---|---|---|---|---|
| `cmr0gixm` | `11917e` | $569.22 | $20.64 | $0.00 | **$548.58** | **$545.37** (Panic Baby) | $3.21 |
| `cmqez5c2` | `dfb43b` | $2,293.78 | $1,894.14 | $0.00 | **$399.64** | **$399.64** (Panic Baby) | see PART 4 |
| `cmryxhyv` | `1e0ce1` | $246.96 | $0.00 | **$246.96** | $246.96 | $0.00 | in flight, owner action |
| `cmpqrt6u` | `15f743` | $210.80 | $0.00 | $0.00 | **$210.80** | **$210.80** (bees.n.honey) | nothing |
| `cmps3tgl` | `3159ac` | $147.61 | $0.00 | $0.00 | **$147.61** | **$0.00** | every clip retired |
| `cmq7qh6p` | `f191a2` | $240.24 | $112.00 | $0.00 | **$128.24** | **$119.74** | $8.50 |
| `cmsiyg70` | `565879` | $111.58 | $0.00 | $78.54 | $111.58 | **$33.04** | nothing |
| `cmrujf29` | `143d15` | $105.05 | $0.00 | $0.00 | **$105.05** | **$105.05** (Zhus Meme) | nothing |
| `cmryam5j` | `5e1e62` | $102.88 | $0.00 | $102.88 | $102.88 | $0.00 | in flight, owner action |
| `cmovgvov` | `951ba8` | $88.29 | $0.00 | $0.00 | **$88.29** | **$88.29** (BAD BITCH 0.50) | nothing |
| `cmponzpo` | `20d221` | $86.48 | $0.00 | $0.00 | **$86.48** | **$26.42** | $60.06 retired |
| `cmpoj6uo` | `62cdaa` | $136.25 | $53.06 | $40.79 | $83.19 | **$41.96** | $0.44 |
| `cmpq1awm` | `fa9808` | $51.60 | $0.00 | $0.00 | **$51.60** | **$51.60** (bees.n.honey) | nothing |
| `cmpq0od6` | `003014` | $51.37 | $0.00 | $0.00 | **$51.37** | **$51.37** (somesome) | nothing |
| `cmqs7gjq` | `f23055` | $116.75 | $64.84 | $0.00 | $51.91 | **$51.91** (Panic Baby) | nothing |

**The single most useful sentence in this report:** of the top fifteen unpaid positions, **eight are not blocked by anything at all.** `cmr0gixm`, `cmpqrt6u`, `cmrujf29`, `cmovgvov`, `cmpq1awm`, `cmpq0od6`, `cmqs7gjq` and `cmsiyg70` between them hold **$1,137.43 that they can request themselves today** and have not. That is 58% of everything reachable on the platform. It is a prompting problem, not a money problem, and it is the cheapest thing on this list to fix.

The full ordered table of all 130 clippers with unreachable money is PART 8.

---

## PART 3 — EVERY REASON MONEY IS UNREACHABLE, CLASSIFIED WITH NO OVERLAP

The partition below is a **strict waterfall over the same dollar**, so nothing is counted twice and nothing escapes. Starting from what a clipper is owed, each dollar falls into exactly one of five states, and they sum to the total by construction rather than by luck:

```
owed on the books                 $3,355.22
  minus in flight (owner action)  $  580.81   →  requested, awaiting the owner
  minus reachable today           $1,944.39   →  the clipper can press the button now
  = UNREACHABLE                   $  830.02
        of which
        bucket A  retired-video    $  403.61
        bucket B  below minimum    $  426.41
        bucket C  global clamp     $    0.00   (see the note below)
```

`580.81 + 1,944.39 + 830.02 = 3,355.22` exactly, and `403.61 + 426.41 = 830.02` exactly.

### Bucket A — earnings on videos that no longer exist: **$403.61**

**What it is.** `Clip.videoUnavailable = true` removes a clip from the withdrawal gate (`payouts/route.ts:515`) and, since BL-698, from the displayed balance too (`earnings/route.ts:206`). Platform-wide the retired clips carry **$3,605.15**, but only **$403.61** is money a clipper has neither been paid nor can reach: the rest was already paid out while the videos were live, and `computeBalance` floors at zero. This is precisely the distinction BL-698 got right the second time and it is why the number is $403.61 and not $3,605.15.

**Is it genuinely owed?** Under the owner's stated policy that a deleted video cannot be paid for: **no.** This bucket is the policy working as intended. Two honest qualifications:

1. **$3,545.05 of the $3,605.15 sits on PAST campaigns**, where `campaignStatusBlocks` (`tracking.ts:1943`) would block earnings even if every video came back. Only **$0.30 sits on an ACTIVE campaign.** Nothing here is recoverable by any mechanism.
2. BL-720 narrowed the gone-verdict so a private, region-locked or age-gated post can no longer be mistaken for a deleted one, but it closed that **going forward only**. BL-720's own census found **$2,792.66 of frozen earnings on 468 clips belonging to accounts that resolve as public**, which cannot be retroactively separated from correct retirements. That is a genuine residual uncertainty and it is disclosed, not resolved.

Largest holders: `cmps3tgl`/`3159ac` $147.61 (his entire balance), `cmponzpo`/`20d221` $60.06, `cmpbazci`/`71108c` $34.24, `cmpe951o`/`5185f3` $34.23, `cmr1rz2j`/`57560a` $19.09, `cmpfp1mw`/`c865a9` $18.52, `cmp7153e`/`3a8763` $15.45.

### Bucket B — below the per-campaign minimum withdrawal: **$426.41**

**139 (clipper, campaign) pairs** across **112 clippers**, of which **$262.69 sits on campaigns that are PAST or archived** and therefore will never grow past the floor on its own.

**A correction the owner should have.** The brief cited BL-728 as measuring "128 pairs and $400.69, rising". **Neither figure appears in any report.** I searched BL-728 and BL-734 for both literals; both are absent. The real series is `111 pairs / $324.33` (BL-728) → `115 / $332.00` (BL-731) → `118 / $338.20` (BL-734) → **`139 / $426.41` today.** So the direction the owner remembered is right and the trend is real: it has grown by **21 pairs and $88.21 since BL-734**, four days ago. The rate is meaningful, not noise, and it is the fastest-growing bucket in this report.

Two campaigns now carry a non-default minimum of **$20.00** (`Zhus Edit (0.50 CPM)` and `Zhus Meme (0.20 CPM)`, the owner's own raises verified in BL-734). All other 31 campaigns store NULL and resolve to the $10 platform default via `resolveMinPayout` (`payout-minimum.ts:113`).

**Is it genuinely owed?** **Yes, every cent of it.** This is money earned on live videos that the platform is holding purely because the amount is small. It is not a deleted-video case and the owner's policy does not touch it. It is a deliberate product rule, but the clipper is owed the money and, on a finished campaign, has no path to ever clear the floor.

### Bucket C — the global clamp: **$0.00 inside the waterfall, $60.47 outside it**

The clamp binds on **exactly one clipper**, `cmqez5c2` / `dfb43b`, for **exactly $60.47**. It contributes **$0.00** to the $830.02 above, and the reason is worth stating carefully because it is the single most misleading number in this whole audit.

His per-campaign availability on Panic Baby is **$460.11**. His global available is **$399.64**, because `globalEarned − globalPaid = 2,293.78 − 1,894.14`. `effectiveCap = min(460.11, 399.64) = 399.64`, so the clamp withholds $60.47. The clamp is **behaving correctly given the numbers it is fed.** The numbers are what is wrong: BL-716 proved his STRAENGE earnings were written **down** to $1,833.67 from a ratchet floor of $1,894.14 by the unfloored pool trim, so his recorded lifetime earnings understate reality by $60.47. Because the shortfall lives in `earned`, not in a gate, it never appears as "owed" in any balance-derived measure. It has to be added by hand, and it is why the PART 1 headline states it separately rather than folding it in.

Full detail in PART 4.

### The two buckets the brief expected that measure $0.00 today, and why

**The archive cascade — $0.00 currently unreachable, and both clippers can self-serve.** BL-732's two voided payouts are still in the table, both still `VOIDED`, both still `paidAt` NULL, both stamped with the identical cascade signature `2026-08-07 10:26:35.219`, both carrying `rejectionReason = "Campaign archived"`:

| id8 | md6 | voided | campaign | position today | can request now |
|---|---|---|---|---|---|
| `cmq7qh6p` | `f191a2` | $71.98 | WinGram | **$73.23** available on WinGram | **YES** |
| `cmrq9r65` | `69f532` | $10.15 | WinGram | **$12.02** available on WinGram | **YES** |

Because `paidAt` is NULL, `isPayoutMoneyOut` correctly reads neither as money-out, so the full amount returned to available. Neither has requested again and neither has been paid. **Neither is stuck.** BL-733 removed the cascade forward (the `updateMany` at `campaigns/[id]/route.ts:963-996` is now a `count()`, verified present at `018c22ca`) but deliberately repaired nothing, which turned out to be the right call: nothing needed repair.

**Frozen-campaign stranding — a real condition, but not a separate dollar.** Money on a PAST or archived campaign is still withdrawable if it clears the minimum; what freezing removes is the ability to *grow*. So this is a cross-cut of buckets A and B, not a sixth bucket, and adding it would double-count. Measured as a cross-cut: **$262.69 of the below-minimum money and $3,545.05 of the retired money sit on campaigns that can never accrue again.** For the below-minimum $262.69 this is decisive, because those clippers cannot earn their way over the floor and only the owner can release them.

### Anything else I found

**Nothing else reaches a clipper's pocket.** Four adjacent categories were checked and are reported here for completeness rather than as part of the headline:

• **FLAGGED clips: $113.50 on 3 clips, all on bees.n.honey**, held by `cmpqrt6u`/`15f743` ($56.20), `cmpu64wk`/`f66b96` ($45.90) and `cmoso5zv`/`7b1543` ($11.40). Not APPROVED, so not owed, but the clipper sees them behind a PENDING facade. They were last touched 4 to 6 days ago and have been in this state since late May / early June. `cmpqrt6u` is also the fourth-largest never-paid clipper in PART 2, which makes his case worth a single decision covering both.
• **Marketplace: 0 rows, 0 clips.** `marketplace_creator_earnings` is empty and no clip carries `isMarketplaceClip`. The 60/30/10 split is untested in production and carries no money.
• **Test campaigns: 0 clips, 0 payouts.** The `isTestCampaign` asymmetry described in PART 7 is latent with zero exposure today.
• **Referral cashouts: 0 live rows.** All 31 payout rows with a NULL `campaignId` are VOIDED or REJECTED historical rows.

---

## PART 4 — THE TWO KNOWN CASES, RESOLVED

### Case 1 — the STRAENGE trim, `cmqez5c2` / `dfb43b`: still outstanding, still exactly $60.47

**Confirmed from live data at `2026-08-10 13:26:52+00`:**

| | |
|---|---|
| STRAENGE, 80 clips, recorded earnings | **$1,833.67** |
| STRAENGE, paid to him | **$1,894.14** |
| Recorded below paid by | **$60.47** — unchanged to the cent since BL-719 reverted the restore |
| Panic Baby, 75 clips, earned | $460.11 |
| Panic Baby, paid | $0.00 |
| Lifetime earned / paid | $2,293.78 / $1,894.14 |
| **Global available = what he can request himself today** | **$399.64** |
| **Total he should receive** | **$460.11** |

BL-719's revert holds perfectly: the data is back where it was, and the code fix (`capButNeverBelowStored` at `tracking.ts:2511`, `tracking.ts:2563` and `clip-earnings-writer.ts:354`) is still in place. The fix is structurally incapable of re-creating the restore, for the reason BL-719 gave: `capButNeverBelowStored` returns `max(cap, stored)` over two numbers, so it prevents the *creation* of a below-paid state and cannot detect, repair or even observe an existing one. Repeated ticks are a fixed point. Independently, STRAENGE is PAST and now also carries an era boundary at `2026-08-01 06:25:59.658`, so the cron does not reach these clips at all.

**Exact amount payable today: $460.11**, being **$399.64 he can request himself** plus **$60.47 added by hand**. Note this has moved since BL-719 recorded "$346.11 available": his Panic Baby clips have kept earning, so the self-service portion has grown by $53.53. The $60.47 has not moved and will not.

**The safe procedure, given BL-696's proof.** BL-696 established, and I re-verified at `018c22ca`, that **no admin route can create a payout row**: `payoutRequest.create` appears in exactly three places in `src/` (`payouts/route.ts:802`, `payouts/referral-request/route.ts:153`, and the dead, unimported `src/actions/payouts.ts:50`), none of them under `src/app/api/admin/`, and no route sets `status: "PAID"` except the review route acting on an existing APPROVED row. A hand payment therefore leaves no trace and the same money stays claimable.

The order, which must not be varied:

1. **Ask him to raise the payout request in the platform first**, on Panic Baby, for the full amount the gate offers him (**$399.64** today; recompute at the moment, never from this table).
2. **Pay $399.64 + $60.47 = $460.11** against that single row.
3. **Mark that row PAID through the normal review path**, so `paidAt` is stamped and `isPayoutMoneyOut` counts the full gross against his balance.
4. **Strike the entry in `docs/OWED-MANUAL-PAYMENTS.md`** with the settlement date and the payout row id.

**Do not pay the $60.47 first and separately.** It would be invisible to every balance calculation, his displayed balance would not fall, and he could request it again next month. That is BL-696's scenario 4 and it is the one failure mode this platform genuinely cannot defend against.

### Case 2 — the archive cascade: both clippers resolved, neither paid, neither stuck

Answered in full in PART 3. In one line: **neither `cmq7qh6p` nor `cmrq9r65` has requested again or been paid, both have MORE available now than was voided ($73.23 vs $71.98 and $12.02 vs $10.15), and both can request today with no owner action needed.** The correct step is a message, not a payment.

### The full WinGram position, against BL-732's measurement

| | BL-732 (2026-08-07) | today | change |
|---|---|---|---|
| Total owed | $165.77 | **$167.18** | +$1.41 |
| Clippers with a positive balance | 20 | **20** | unchanged |
| Can request today | 3, **$101.53** | 3, **$101.53** | unchanged |
| Blocked below the $10 minimum | 17, $64.24 | **17, $65.65** | +$1.41 |

The three who can act are `cmq7qh6p`/`f191a2` **$73.23**, `cmponzpo`/`20d221` **$16.28** and `cmrq9r65`/`69f532` **$12.02**. BL-732's finding that archiving does not block a fresh request is confirmed live: WinGram is `isArchived = true`, `archivedAt 2026-08-07 10:26:34.832`, and all three read as requestable. The 17 blocked clippers are the clearest case in this report of money that is genuinely owed and permanently unreachable through the product: WinGram is archived and PAUSED, so none of them can earn their way over $10.

---

## PART 5 — IS THE MATH ITSELF RIGHT

### Does every clip earn off its own stamped CPM, and do the two stamps agree with the locked share?

**Clipper side: yes, without exception.** Of 4,308 APPROVED live clips, **0 have a null `cpmAtSubmissionDecimal` and 0 have a non-positive one.** Every clip carries its own clipper rate.

**Owner side: no, and this is the largest structural finding in PART 5.** **2,972 of 4,308 clips (69.0%) have a NULL or zero `ownerCpmAtSubmissionDecimal`.** `resolveClipCpms` (`cpm.ts:160-182`) resolves the two sides **independently**, so those clips read the **live** `campaign.ownerCpm` on every tick rather than a frozen rate. If an owner rate is edited mid-campaign, 69% of clips silently re-price on the owner side while the clipper side stays frozen. Nothing has moved this and no clipper is affected, but it is the exact mechanism that produced BL-539's ambiguity.

**Stamp versus locked share.** Comparing `ownerCpm / clipperCpm` against `s / (1 − s)` at BL-563's 0.01 tolerance, on every clip that has both stamps:

| campaign | clips | ambiguous | clipper earnings on ambiguous rows |
|---|---|---|---|
| somesome | 723 | **179** | **$2,298.55** |
| every other campaign | 3,585 | **0** | $0.00 |

**179 clips, on somesome alone, and nowhere else.** That is unchanged from BL-617's "179 of 726", so the population has not grown. This is BL-539 / BL-570's exposure and the owner-side figure attached to it was **$933.94**. It remains a do-not-touch: those rows carry a stamp from the 1.00 era against a `lockedOwnerShareDecimal` of 0.32885906 today, and only the owner can say which rate governs a clip submitted under the old deal. **No platform-wide owner re-derive was run.**

There is a real inconsistency underneath it, which no prior round has stated this directly: `decideOwnerGross` (`owner-share-guard.ts:57-79`) returns `ambiguous` for these rows and three callers correctly refuse to act, but the **cron path does not consult it at all** — `tracking.ts:2613-2638` re-derives the owner amount from `s` alone and discards the stamped ratio. Those two behaviours cannot both be right for the same row. It is inert today only because somesome is PAST and carries an era boundary.

### Do bonuses sit inside the pool cap, now that per-clip CPM overrides exist?

**Inside, and verified two ways.**

Structurally, `newEarnings` at every cap site is the **gross** (base + bonus), so the bonus is inside the value being capped: `tracking.ts:2511` (BL-162 pool trim, which trims bonus first at `:2534-2535`), `tracking.ts:2563` (legacy ratio cap) and `clip-earnings-writer.ts:354` (the BL-167 L1 chokepoint, where `requestedGross = rounded.earnings`). Per-clip caps behave differently and correctly: `maxPayoutPerClip` caps **base before** bonus (`earnings-calc.ts:169-181`), which is deliberate and documented.

Measured, per campaign, clipper-side spend against the clipper pool cap:

| campaign | base | bonus | clipper-side spend | pool cap | headroom |
|---|---|---|---|---|---|
| somesome | $5,126.41 | $275.14 | $1,967.14 | $6,543.62 | $4,576.48 |
| STRAENGE | $1,849.65 | $152.06 | $1,997.56 | $2,000.00 | **$2.44** |
| Panic Baby | $1,982.14 | $45.88 | $1,987.29 | $2,000.00 | **$12.71** |
| bees.n.honey | $1,566.89 | $38.31 | $1,570.40 | $1,648.35 | **$77.95** |
| all others | — | — | — | — | comfortable |

**No pool is breached.** Total bonus platform-wide is $530.72 and all of it is inside. `capButNeverBelowStored` can leave a clip above its cap by refusing to subtract, which is deliberate and logged, but it never *raises* a clip and never adds a cent to a campaign.

**As for BL-756's per-clip overrides: zero clips carry one.** `cpmOverriddenAt` is non-null on **0 of 4,308** clips. The feature shipped, was demonstrated and fully reversed, and has not been used. The overshoot question is therefore currently unexercised, not proven safe by production evidence, and I will not claim otherwise. What is proven is that the override writes rates and never money, refuses any clip with earnings, and scales both stamps by the same ratio, so `owner-share-guard.ts:72` returns an identical verdict before and after.

### Does any campaign exceed its budget?

**No. Zero campaigns of 33.** BL-627's property holds. But the margin is now thinner than it has ever been:

| campaign | budget | spend | remaining |
|---|---|---|---|
| **Panic Baby** | $3,000 | **$3,000.00** | **$0.00** |
| STRAENGE | $3,000 | $2,998.10 | $1.90 |
| bees.n.honey | $3,000 | $2,978.35 | $21.65 |

**Panic Baby is exactly at its budget, to the cent, with zero remaining**, and it auto-paused at `2026-08-07 17:01:49.512`. It is also the campaign carrying the two largest live withdrawable balances in this report ($545.37 and $399.64). That combination deserves the owner's attention: the campaign is finished in budget terms while $1,000+ of clipper money still sits on it.

### Does the ghost fee still leave NULL-fee campaigns untouched?

**Yes, on every campaign.** `platformFeePctDecimal` is **NULL on all 33 campaigns** — no fee has ever been set. `realBudgetFromFee` (`platform-fee.ts:51-54`) returns `{ ghostFee: 0, realBudget: b }` on the NULL branch with `b` as the raw unmodified number, never round-tripped through Decimal. BL-630's byte-identical promise holds by construction and is untested in production only because the feature has never been used.

### Are the clip-side and agency-side spend sums still inconsistent?

**Yes, and the gap has grown.** BL-642's finding stands: the clip side filters `APPROVED AND isDeleted = false AND videoUnavailable = false` while the agency side has **no filter at all**.

| campaign | agency, unfiltered | agency, on live approved clips | phantom |
|---|---|---|---|
| somesome | $3,402.98 | $1,123.49 | **$2,279.49** |
| GainzAlgo (REPOST) | $295.54 | $224.19 | $71.35 |
| bees.n.honey | $1,407.95 | $1,287.29 | $120.66 |
| Panic Baby | $1,012.71 | $992.41 | $20.30 |

This is owner-side only and errs safe (it inflates `spent`, so a campaign auto-pauses early rather than overspending). But it has a consequence nobody has named: **the owner's accrued agency total now exceeds his own locked owner reserve on four campaigns** — somesome by **$196.60**, bees.n.honey by **$56.30**, Panic Baby by **$12.71**, STRAENGE by **$0.54**, **$266.15 in total**. No clipper is affected by a cent of it.

### Is the 9% fee taken exactly once, on the correct base, across all three payout paths?

**Yes.** Across all 165 payout rows:

• **0 rows** where `finalAmount > amount`. **0 rows** where `feeAmount` disagrees with `amount × feePercent / 100`. **0 rows** with a fee percentage other than 4 or 9.
• Fee arithmetic lives in exactly one place, `payout-calc.ts:61-83`: `feeAmount = round2(amount × pct/100)`, `finalAmount = amount − feeAmount − expressFeeAmount`. The review route, the adjust route and every display read the **stored** values and never recompute, so no second deduction exists.
• Path 2 (referral cashout) takes **no fee at all** by design (`finalAmount = amount`), and has 0 live rows.
• Path 3 is dead code with 0 importers and fails closed because it cannot supply an asset or chain.

**7 rows do fail the `finalAmount = amount − fee − express` identity**, all of them `VOIDED`, all from **2026-04-01 / 04-02**, all belonging to a single user (`cmnd5tai`), and all computed under an older formula that **added** the bonus (`finalAmount = amount − fee + bonus`). No money left the platform on any of them. **Historical, $0.00 impact, no action.**

**One new finding on the fee, owner-side.** **8 PAID payouts totalling $2,826.64 gross carry `feePercent = 4` while the user has no `referredById` today and no `referrerOverriddenAt` stamp.** They belong to 6 real non-test CLIPPERs and span 2026-04-29 to 2026-06-15. `feePercent` is stamped live at request time from `payouts/route.ts:403`, so the referral link existed then and has since been removed with no audit trail. **The platform collected $113.07 in fees where the 9% rate would have yielded $254.40, a shortfall of $141.33.** No clipper was overcharged — the count of rows where a referred user paid 9% is **0** — so this costs the owner, never a clipper. Historical; I am not proposing a retroactive re-charge.

---

## PART 6 — THE REVIVAL QUESTION

### What happens today if a retired clip's video comes back

**Nothing notices. The clip is frozen permanently.**

Verified in the source at `018c22ca`, not inherited from BL-717. The auto-restore lives at `tracking.ts:1730` and fires on `videoUnavailable && stats.views > 0`. The cron's due-jobs where-clause, inside the `if (!campaignIds)` branch, sets `where.clip = { isDeleted: false, videoUnavailable: false, ... }` at **`tracking.ts:3593`**. A retired clip is filtered out roughly 1,860 lines before it could ever reach the restore. **The restore is unreachable for exactly the clips that need it.** The only path that reaches them is an owner manually running a targeted campaign re-check, which is undocumented and which nobody has run.

**This is not theoretical, and here is the proof.** BL-721 probed all 852 retired clips on 2026-08-05 and found 10 whose videos were live again, concentrated on two accounts. Five days later:

| account (first 8) | retired clips still flagged | approved | frozen earnings |
|---|---|---|---|
| `cmqgr2yt` | **9** | **9** | **$12.62** |
| `cmqyvvzg` | **1** | 0 | $0.00 |

**All ten are still marked gone, carrying BL-721's exact $12.62, five days after the platform measured that their videos had returned.** That is the answer to the owner's question, demonstrated rather than argued.

### Re-measuring the rate and the money, now that BL-720 has narrowed the verdict

I did **not** run a fresh probe: that would cost money and the brief forbids paid actor runs, so no revival rate was re-measured live and I will not present one as if it were. What I did measure is what has changed in the population since BL-721, which is enough to answer the build question:

| | BL-721 (2026-08-05) | today | change |
|---|---|---|---|
| Retired clips | 852 | **889** | **+37 in 5 days (7.4/day)** |
| Approved among them | 633 | **666** | +33 |
| Frozen earnings | $3,583.50 | **$3,605.15** | **+$21.65** |
| Clips waiting out BL-720's 36h persistence test | n/a | **36** | new column live and working |
| Frozen money on PAST campaigns | $3,510.26 (97.9%) | **$3,545.05 (98.3%)** | still the whole picture |
| Frozen money on ACTIVE campaigns | $72.24 | **$0.30** | collapsed |

**BL-720's narrowing has not changed the picture, and the one number that moved makes the case against building weaker, not stronger.** Retirements are running at 7.4/day against BL-721's 7.67/day, essentially unchanged. Applying BL-721's censused 1.17% rate to that flow gives roughly **2.6 revivals a month worth roughly $3.70** — an ESTIMATE, carried forward from BL-721's census and explicitly not re-measured here — against BL-717's $13 to $22 a month for a per-clip schedule. And the recoverable-money side has collapsed: **$0.30 of frozen earnings now sits on an ACTIVE campaign, down from $72.24.** 98.3% of the frozen money is on PAST campaigns where `campaignStatusBlocks` (`tracking.ts:1943`) means a perfect revival restores visibility and withdrawability but **not one further cent of earning**.

### The honest recommendation

**Still do not build the per-clip tiered schedule.** BL-721's arithmetic has not moved and the recoverable slice has shrunk by two orders of magnitude. But BL-721's own alternative deserves promoting, because the case for it is now clearer than the case against:

**Re-check by ACCOUNT, not by clip.** The 889 retired clips sit on roughly 113 accounts. One profile call per account per day is about **$0.113/day, roughly $3.39/month** — a quarter of the per-clip cost — and it would have caught all ten of BL-721's revivals, because both revived accounts came back whole. At $3.39/month against ~$3.70/month of expected recovery it still does not clearly pay for itself in dollars, and I am not going to dress that up. **The reason to do it is not the money. It is that ten clips are provably visible to the public right now while the platform tells their clippers the videos are gone, and that will keep happening.**

The minimum honest fix, if the owner wants to spend nothing: **document the manual targeted campaign re-check** so that when a clipper writes in saying "my video is back", somebody can act. Today there is no such path a support person could follow.

---

## PART 7 — WHAT NOBODY HAS LOOKED AT

Seven categories checked. Four are clean and I say so rather than inventing a finding; three produced something new.

**NEW — the referral fee shortfall: $141.33, owner-side, historical.** Full detail in PART 5. 8 PAID payouts at 4% where the user has no referrer today. Costs the owner, never a clipper. **Live in the sense that the mechanism still exists** (removing a referral link leaves stamped 4% rows behind with no audit trail), but the exposure is bounded and historical.

**NEW — the owner's accrual exceeds his own locked reserve on 4 campaigns: $266.15.** somesome $196.60, bees.n.honey $56.30, Panic Baby $12.71, STRAENGE $0.54. Caused by BL-642's unfiltered agency-side sum retaining rows on retired and rejected clips. **Live.** No clipper money involved and it errs in the safe direction, but the owner's reserve is a stated guarantee and it is currently overstated.

**NEW — the withdrawal gate does not exclude test campaigns while the display does.** `earnings/route.ts:64` filters `campaign: { isTestCampaign: false }`; the gate's clips query at `payouts/route.ts:515` and the global clamp's aggregate at `payouts/route.ts:658` have no such filter. A clip on a test campaign would be invisible in the balance yet spendable through the gate. **Latent, $0.00 today:** 0 clips and 0 payouts exist on the single `isTestCampaign` campaign. It costs nothing to leave and nothing to fix; it should simply be known before someone creates a test campaign with clips on it.

**The 50 zeroed-view clips (BL-751) — closed, $0.00, no clipper affected.** Measured directly: today **13 clips** have a latest stored view count of 0 after a positive peak. All 13 are **YouTube**, all **APPROVED**, across **5 clippers**, carrying **$0.00** of earnings, with a **biggest-ever peak of 2 views** — far below every campaign's 1,000-view minimum. The 5 TikTok events and 32 recovered YouTube clips have all recovered. This matches BL-751 and BL-753 exactly. BL-753 fixed the fabrication forward at `youtube.ts:178` and correctly declined to repair the data. **BL-751's residual unknowns remain unclosed** and cannot be closed here: per-event attribution is impossible because no provider response was logged, and confirming the hidden-count mechanism needs a `YOUTUBE_API_KEY` that is not in this environment. **No money rests on either.**

**Campaigns that changed status mid-life — measured, and covered by PAST.** **5 era boundaries exist on 2 campaigns**, none `eraExempt`: somesome (4, latest `2026-06-22 03:07:29.621`) and **STRAENGE (1, `2026-08-01 06:25:59.658` — new since BL-617 and created the same morning as the budget-cap event of BL-714/BL-716)**. Clips created before their boundary: somesome 719 clips / $5,395.05 / 69 clippers, STRAENGE 156 clips / $2,001.71 / 16 clippers. **Both campaigns are PAST**, so `campaignStatusBlocks` already freezes them and the era boundary adds no exposure beyond that today. It would matter instantly if either were reactivated, which is BL-570's standing warning about the "keep existing earning" checkbox and its silent −$933.94.

**Banned or suspended clippers — clean, $0.00.** There is no global ban column on `users`; the only ban fields are marketplace-scoped, and **0 users carry `marketplaceBannedUntil` or `clipperMarketplaceBannedUntil`.** On the account side, **all 4,308 approved live clips sit on `APPROVED` clip accounts** — none on the 32 REJECTED accounts. No money is trapped behind an enforcement action.

**Reassigned and override-carrying clips — clean.** **1 clip has been reassigned** (`cmsktak4y`, Zhus Edit → Zhus Meme, `2026-08-08 21:19:47.965`), and it was done correctly: both stamps were restamped together, clipper $0.50 → $0.20 and owner $0.3197 → $0.1279, preserving the ratio to within rounding of the destination's `s/(1−s) = 0.63949`. It now holds $0.41. **0 clips carry a per-clip CPM override.**

**The 3 stale UNDER_REVIEW payouts — now 1, and it is not a test.** BL-708 measured 3 rows / $147.12 / oldest `2026-06-05 01:06:42.901`. Today there is **exactly 1 UNDER_REVIEW row left, and it is that same oldest one**: clipper `cmpq15k2` / `7b86e2`, **$57.58 gross / $52.40 net**, on bees.n.honey, created `2026-06-05 01:06:42.901`, now **66.5 days old**. The other two have been resolved. He is **not** a test user (`isTestUser = false`, role CLIPPER) and this is his only payout — he has been paid **$0.00** lifetime against **$59.11** earned. **This is a real person who has been waiting sixty-six days.** It is the single most embarrassing row in the database and it costs $57.58 to close.

---

## PART 8 — THE ACTION LIST

### A. What to do first, in order, and what each costs

| # | action | who | amount | why |
|---|---|---|---|---|
| 1 | **Pay the 66-day UNDER_REVIEW row** | `cmpq15k2` / `7b86e2` | **$57.58** | Waiting since 2026-06-05. Not a test user. One click. |
| 2 | **Settle the STRAENGE case** per the 4-step procedure in PART 4 | `cmqez5c2` / `dfb43b` | **$460.11** ($399.64 self-service + **$60.47 by hand**) | The only clipper harmed by a proven code defect. Order matters. |
| 3 | **Clear the 8 in-flight requests** | 8 clippers | **$523.23** | Money already requested and sitting. |
| 4 | **Message the 8 clippers holding $1,137.43 they can already withdraw** | see below | **$0.00 to you** | The cheapest win in this report. |
| 5 | **Message the 2 archive-cascade clippers** | `cmq7qh6p`, `cmrq9r65` | **$0.00 to you** | Both can request; neither knows. |
| 6 | **Decide the 17 WinGram clippers under the minimum** | 17 clippers | **$65.65** | Archived + PAUSED. They can never clear $10. Only you can release them. |
| 7 | **Decide the 3 FLAGGED bees.n.honey clips** | 3 clippers | **$113.50** | Approve or reject. In limbo since May/June. |

**Action 4, itemised — clippers who can withdraw today and simply have not:**

| id8 | md6 | withdrawable now | on |
|---|---|---|---|
| `cmr0gixm` | `11917e` | **$545.37** | Panic Baby |
| `cmpqrt6u` | `15f743` | **$210.80** | bees.n.honey |
| `cmrujf29` | `143d15` | **$105.05** | Zhus Meme |
| `cmovgvov` | `951ba8` | **$88.29** | BAD BITCH ANTHEM (0.50) |
| `cmpq1awm` | `fa9808` | **$51.60** | bees.n.honey |
| `cmpq0od6` | `003014` | **$51.37** | somesome |
| `cmqs7gjq` | `f23055` | **$51.91** | Panic Baby |
| `cmsiyg70` | `565879` | **$33.04** | Zhus Edit |
| | | **$1,137.43** | |

### B. Every clipper with unreachable money, ordered by amount

Reason codes: **R** retired video (owner policy: not owed) · **M** below the campaign minimum (owed) · **C** global clamp / recorded below paid (owed). "Self-serve" is whether the clipper can act alone today.

| id8 | md6 | owed | can get now | **cannot reach** | reason | self-serve | exact safe step |
|---|---|---|---|---|---|---|---|
| `cmps3tgl` | `3159ac` | $147.61 | $0.00 | **$147.61** | R $147.61 | no | Policy call. Every clip is a deleted video. Not owed under stated policy. |
| `cmqez5c2` | `dfb43b` | $399.64 | $399.64 | **$60.47** | C $60.47 | partly | PART 4 procedure. Request first, then pay $460.11 against that row. |
| `cmponzpo` | `20d221` | $86.48 | $26.42 | **$60.06** | R $60.06 | partly | Ask him to withdraw $26.42 (WinGram $16.28 + bees.n.honey $10.14). Rest is retired. |
| `cmpbazci` | `71108c` | $34.52 | $0.00 | **$34.52** | R $34.24, M $0.28 | no | Retired-video policy call. |
| `cmpe951o` | `5185f3` | $34.23 | $0.00 | **$34.23** | R $34.23 | no | Retired-video policy call. |
| `cmqb6eia` | `9f5e0f` | $42.68 | $0.00 | **$22.01** | M $22.01 | no | Split under two $20 minimums. Owner release or wait. |
| `cmqgqnw4` | `64d4a4` | $20.64 | $0.00 | **$20.64** | R $12.62, M $8.02 | no | Mixed. $8.02 owed, $12.62 retired. |
| `cmpfozzs` | `540fef` | $19.76 | $0.00 | **$19.76** | M $12.46, R $7.30 | no | $12.46 genuinely owed, under the $20 Zhus minimums. |
| `cmr1rz2j` | `57560a` | $19.09 | $0.00 | **$19.09** | R $19.09 | no | All 6 WinGram clips retired. Policy call. |
| `cmpfp1mw` | `c865a9` | $18.52 | $0.00 | **$18.52** | R $18.52 | no | Retired-video policy call. |
| `cmp7153e` | `3a8763` | $15.45 | $0.00 | **$15.45** | R $15.45 | no | Paid $1,313.86 of $1,329.31 already. Residual is retired. |
| `cmoyq9m9` | `ace055` | $14.17 | $0.00 | **$14.17** | M $14.17 | no | somesome + WinGram, both frozen. Owed, unreachable forever. |
| `cmpiiy8o` | `35ad30` | $13.40 | $0.00 | **$13.40** | M $13.40 | no | Three frozen campaigns. Owed, unreachable forever. |
| `cmp75zkf` | `70aa2a` | $13.25 | $0.00 | **$13.25** | R $7.71, M $5.54 | no | $5.54 owed on frozen campaigns. |
| `cmsiyrnw` | `a02849` | $13.08 | $0.00 | **$13.08** | M $13.08 | no | Zhus Edit, $20 minimum. Will clear if he keeps posting. |
| `cmrng806` | `a0f7fd` | $13.02 | $0.00 | **$13.02** | M $13.02 | no | Split bees.n.honey + Zhus Meme. |
| `cmpbl72e` | `e1f286` | $10.94 | $0.00 | **$10.94** | M $10.94 | no | Frozen campaigns. Owed, unreachable forever. |
| `cmoaepan` | `6b0d58` | $10.92 | $0.00 | **$10.92** | M $10.92 | no | Frozen campaigns. Owed, unreachable forever. |
| `cmqic2kl` | `a9cc30` | $9.54 | $0.00 | **$9.54** | M $9.54 | no | WinGram, archived. Owed, unreachable forever. |
| `cmqqz593` | `52760f` | $9.42 | $0.00 | **$9.42** | M $9.42 | no | WinGram, archived. Owed, unreachable forever. |
| `cmruxjk5` | `7b9418` | $9.34 | $0.00 | **$9.34** | M $9.34 | no | Zhus, $20 minimum. Will clear if he keeps posting. |
| `cmqv45j2` | `4c95d9` | $9.01 | $0.00 | **$9.01** | M $9.01 | no | GainzAlgo REPOST, PAST. Owed, unreachable forever. |
| `cmqv7svp` | `4e6238` | $8.76 | $0.00 | **$8.76** | R $8.76 | no | Retired-video policy call. |
| `cms54yls` | `d86720` | $8.74 | $0.00 | **$8.74** | M $8.74 | no | Split across three campaigns. |
| `cmq7qh6p` | `f191a2` | $128.24 | $119.74 | **$8.50** | M $8.50 | **yes** | **Message him: $73.23 WinGram + $46.51 Panic Baby available now.** |
| `cmn4nlfg` | `a92aea` | $31.14 | $22.82 | **$8.32** | M $7.06, R $1.26 | **yes** | Ask him to withdraw $22.82 on Zhus Meme. |
| `cmqc7rrz` | `6aedd4` | $7.79 | $0.00 | **$7.79** | M $7.79 | no | GainzAlgo + WinGram, both frozen. |
| `cmp0zwli` | `9cbad3` | $7.65 | $0.00 | **$7.65** | M $7.65 | no | bees.n.honey + Panic Baby. |
| `cmpqbxfe` | `43f88e` | $7.62 | $0.00 | **$7.62** | M $7.62 | no | Panic Baby, at budget. |
| `cmo8rywy` | `6bc9ba` | $7.25 | $0.00 | **$7.25** | M $7.25 | no | somesome, PAST. Owed, unreachable forever. |
| `cmr51mba` | `b0616e` | $7.24 | $0.00 | **$7.24** | M $7.24 | no | Zhus, $20 minimum. |
| `cmqjruwb` | `b99870` | $7.03 | $0.00 | **$7.03** | M $7.03 | no | bees.n.honey, PAST. Owed, unreachable forever. |
| `cmskdgtp` | `061707` | $7.01 | $0.00 | **$7.01** | M $7.01 | no | BAD BITCH ANTHEM (2.50), ACTIVE. Will clear. |
| `cmqknpjz` | `eb397a` | $6.62 | $0.00 | **$6.62** | M $6.62 | no | WinGram, archived. Owed, unreachable forever. |
| `cms0lou5` | `645a6c` | $6.43 | $0.00 | **$6.43** | M $6.43 | no | WinGram, archived. Owed, unreachable forever. |
| `cmoagj49` | `2b623c` | $6.35 | $0.00 | **$6.35** | M $4.23, R $2.12 | no | somesome, PAST. |
| `cmosj3qk` | `99635c` | $6.25 | $0.00 | **$6.25** | R $6.25 | no | Retired-video policy call. |
| `cmqmnvgs` | `f9cf0b` | $5.82 | $0.00 | **$5.84** | M $5.84 | no | GainzAlgo REPOST, PAST. |
| `cmqpkfgv` | `f20eec` | $5.54 | $0.00 | **$5.54** | M $5.54 | no | GainzAlgo REPOST, PAST. |
| `cmp5uqwn` | `444689` | $5.46 | $0.00 | **$5.46** | M $5.46 | no | somesome, PAST. |
| `cmp5a6k0` | `b1865e` | $5.23 | $0.00 | **$5.23** | R $3.76, M $1.47 | no | Mixed. |
| `cmp7ic4p` | `aaebb6` | $4.92 | $0.00 | **$4.92** | R $4.92 | no | Retired-video policy call. |
| `cmqjc73w` | `66e3e8` | $4.70 | $0.00 | **$4.70** | M $4.70 | no | WinGram, archived. |
| `cmsj74dk` | `ca1427` | $4.43 | $0.00 | **$4.43** | M $4.43 | no | Zhus, $20 minimum. Will clear. |
| `cmpp3jgm` | `ff3ac9` | $16.24 | $0.00 | **$4.10** | M $4.10 | no | $12.14 already in flight. |
| `cmrubt9k` | `edf4ed` | $29.71 | $26.89 | **$2.82** | M $2.82 | **yes** | Ask him to withdraw $26.89. |
| `cmrl046b` | `299618` | $23.86 | $0.00 | **$2.61** | M $2.61 | no | $21.25 already in flight. |
| `cmr0gixm` | `11917e` | $548.58 | $545.37 | **$3.21** | M $3.21 | **yes** | **Message him. Largest unpaid position on the platform.** |
| `cmpqxvna` | `ed443f` | $15.89 | $14.38 | **$1.51** | R $1.51 | **yes** | Ask him to withdraw $14.38 on somesome. |
| `cmpd4ltb` | `f18de2` | $18.07 | $16.72 | **$1.35** | M $1.35 | **yes** | Ask him to withdraw $16.72 on somesome. |
| `cmpq15k2` | `7b86e2` | $59.11 | $0.00 | **$1.53** | M $1.53 | no | **His $57.58 is the 66-day UNDER_REVIEW row. Act on that.** |
| `cmpoj6uo` | `62cdaa` | $83.19 | $41.96 | **$0.44** | M $0.44 | **yes** | Ask him to withdraw $41.96 on somesome. |
| **79 more clippers** | | | | **$146.79** | almost all M | mostly no | **$4.43 or less each**, median well under $2. Nothing individually actionable; this tail only clears through the minimum-release decision in fix 1. |
| **130 clippers** | | | | **TOTAL $830.02** | | | |

The 51 rows above carry **$683.23 of the $830.02**. `cmqez5c2`'s $60.47 is listed for completeness but is **not** part of the $830.02, for the reason given in PART 3 bucket C: it is missing from his recorded earnings rather than blocked by a gate.

### C. The systemic fix list. Every fix is specified. NONE was performed.

**Fix before it grows.**

1. **The below-minimum population, now growing measurably.** 139 pairs / $426.41, up **21 pairs and $88.21 in the four days since BL-734**, with **$262.69 on campaigns that can never accrue again**. This is the only bucket with a demonstrated growth rate. Spec: an owner-only sweep that identifies (clipper, campaign) pairs on PAST or archived campaigns holding a positive balance below that campaign's minimum, and releases them as a single payout per clipper aggregated **across** campaigns rather than per campaign. The gate is per-campaign by construction (`payouts/route.ts:515`), so this needs a new deliberate path, not a threshold tweak. It must go through `payoutRequest.create` so `paidAt` is stamped and the balance actually falls; a hand transfer would leave the money claimable. **Own round, with snapshots and printed rollback.**

2. **The platform cannot record a payment made by hand.** BL-696 proved it and I re-verified it: `payoutRequest.create` exists at exactly three sites, none under `src/app/api/admin/`. This is the single highest-severity structural gap in the money system, because it is the only way a double payment can occur, and it blocks fixes 1 and 6 above. Spec, as BL-696 drafted it and I would not change: `POST /api/admin/payouts/manual`, OWNER-only, Serializable, taking `userId`, nullable `campaignId`, `amount`, **mandatory `proofNote`**; creates a PayoutRequest with `status: "PAID"` and `paidAt: now()`, subject to the same clamp as every other path, writing an audit row naming the entering owner. **Own round.**

3. **The unfloored cap sites are fixed; the underlying asymmetry is not.** BL-718's `capButNeverBelowStored` prevents a *new* below-paid state at all three sites, but it cannot see an existing one, which is why `cmqez5c2` is still $60.47 short and why **6 clippers currently sit recorded-below-paid** (`cmqez5c2` $60.47, `cmofpudr` $36.75, `cmoaejuc` $23.09, `cmoal818` $7.82, `cmp71p89` $0.80, `cmqmnvgs` $0.02). Spec, as BL-714 proposed: record `earnedAtPaymentSnapshot` on each payout at creation, and clamp against `max(lifetimeEarned, Σ earnedAtPayment)`. This makes the defect self-healing instead of needing a hand payment every time. **Own round.**

**Can wait.**

4. **The owner-side stamp gap.** 2,972 of 4,308 clips have no `ownerCpmAtSubmissionDecimal` and re-price off the live rate every tick. Spec: backfill the owner stamp from `campaign.ownerCpm` at the clip's own era, using `enforceCpmStampInvariant`'s existing force-stamp branch (`cpm.ts:207-229`). **Do not** touch the 179 somesome clips whose stamps already disagree with the locked share — those are BL-539's ambiguous rows and re-deriving them platform-wide costs $933.94.

5. **The cron ignores `decideOwnerGross`.** `tracking.ts:2613-2638` re-derives the owner amount from `s` alone while three other callers refuse to act on the same rows. Inert today because both affected campaigns are PAST. Spec: route the cron through the same guard, and treat `ambiguous` as "leave the stored value alone". **Must be done before somesome or STRAENGE is ever reactivated.**

6. **The agency-side spend filter.** BL-642's asymmetry now puts owner accrual **$266.15 above the locked owner reserve** across four campaigns. Spec: add `clip: { isDeleted: false, status: "APPROVED", videoUnavailable: false }` to the agency aggregate on the display path only — the cap math already uses the filtered `ownerAggApproved` (`balance.ts:349-352`). Owner-facing only; no clipper figure moves.

7. **The test-campaign gate asymmetry.** Add `campaign: { isTestCampaign: false }` to `payouts/route.ts:515` and `:658`. Two lines, $0.00 exposure today, do it whenever something else touches that file.

8. **Account-level revival re-checking, or at minimum documentation.** PART 6. ~$3.39/month for the account-level sweep; $0 to simply write down the manual targeted re-check so support can act when a clipper reports a returned video.

9. **`tracking.ts:3131`'s regex remains a loaded gun.** `/not found|no results|private|removed|unavailable/i` on an exception message still routes to `writeClipEarningsZero`. Statically unreachable behind BL-678's `APIFY_HARD_OFF`, and 6 clips carry `savedEarnings` at $0.00, so nothing has been harmed. It should be deleted or narrowed rather than left pointed at the money path.

---

## WHAT COULD NOT BE MEASURED, AND WHY

Stated plainly, because a gap presented as a result is worse than a gap.

• **A per-clip recompute from views × stamped CPM was not performed.** Reasoned in PART 2: earnings pass through `payoutReductionRatio`, per-clip caps, minimum-view gates and cross-clipper pool trimming, so a naive recompute would disagree for correct reasons on hundreds of clips. What was verified instead: 0 null or non-positive clipper stamps on 4,308 clips, 0 invariant violations, and 0 campaigns over budget.
• **The revival rate was not re-measured live.** A fresh census would need ~889 paid API calls. BL-721's 1.17% is carried forward and every number derived from it is labelled an **ESTIMATE**. What was measured without spending anything: the population grew 852 → 889, and BL-721's ten identified revivals are demonstrably still frozen.
• **The 5 TikTok zeroed-view events and per-event attribution for the 45 YouTube ones remain unattributed.** No provider response was logged at the time and there is no `YOUTUBE_API_KEY` in this environment. Both are closed on money ($0.00) and open on cause.
• **Whether the 179 ambiguous somesome rows should honour the clip's stamped era rate or the campaign's locked share is not a measurement question.** BL-539 priced the two answers $119.39 apart on somesome alone. Only the owner can decide it.
• **The $141.33 referral-fee shortfall cannot be attributed to a cause.** `referredById` has no history table and `referrerOverriddenAt` is null on all 6 users, so I can state the shortfall exists but not why the links were removed.
• **Whether the 468 public-account retired clips carrying $2,792.66 were correctly retired cannot be determined retroactively.** BL-720 closed the private-account case definitively and covers region-lock and age-gate going forward only. This is a disclosed residual, not an open action.

---

## VERIFICATION

Read-only throughout, including every subagent. All 9 subagents were instructed READ ONLY and none held write tools on the database. **Three subagent contradictions were found and resolved rather than averaged or dropped:** (1) five subagents initially read `reports/BL-###.md` paths that belong to a **different project** sharing the repository — caught by cross-checking against the repository tree, and every ClippersHQ figure in this report comes from a re-fetch of the correctly suffixed `BL-###-clippershq-*.md` files; (2) BL-716 says 7 other below-paid clippers and BL-718 says 8 on the same $144.22 — resolved by measuring live, which returns **6 today** including `cmqez5c2`; (3) the brief's "128 pairs / $400.69" for the below-minimum population appears in **no report** — resolved by re-measuring, which gives **139 pairs / $426.41** and confirms the rising trend the owner remembered.

Every dollar in PART 3 falls into exactly one bucket, and the partition closes to the cent against the headline with no residual: `580.81 + 1,944.39 + 403.61 + 426.41 = 3,355.22`. BL-627's no-overpayment property and the no-campaign-over-budget property were both **re-verified on live data**, not inherited. Every figure was recomputed from clip rows, payout rows and stamped CPMs using the gate's own arithmetic rather than read off a stored total. Timestamps cast `::text` against DB `now()` throughout. Handles redacted, no wallet address selected or printed. `agency-monitor --fix` not run, no platform-wide owner re-derive, no Apify actor, no paid probe, **$0.00 spend**. No build was run and none is claimed: this round changed no TypeScript.

**Nothing was changed. 4,308 approved clips, 165 payout rows, 33 campaigns and $12,154.11 of recorded earnings are exactly as they were found.**
