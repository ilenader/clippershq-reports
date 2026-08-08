# BL-743 — the owner side restamped correctly. The reassignment is clean, and the $0.39 is what a $0.20 campaign actually costs

**FIRST LINE, because that is where the defect was to be reported if it existed: THE OWNER SIDE IS NOT ON THE SOURCE CAMPAIGN'S RATE. Both stamps moved to the destination together, in one update, inside one transaction. There is no defect in this clip.**

**2026-08-08 · READ ONLY · Base:** `main @ b5bd0651` · **Branch:** `checkpoint/BL-743`
**Nothing was changed. No code, no data, no money. Nothing recalculated, restamped, re-derived or repaired. `agency-monitor --fix` was never run. Every query went through `scripts/run-select.js`, which refuses every write keyword. The handle is redacted to an md5 prefix. Every timestamp is cast `::text` against DB `now()`.**
**No build, `tsc` or lint run was performed and none is claimed: this round produced one markdown file, which cannot change them.**

---

## THE ANSWER, BEFORE THE DETAIL

The suspicion was reasonable and the arithmetic behind it was wrong in one specific place: **a campaign's
"0.20 CPM" is the CLIPPER's rate, not the campaign's total cost per 1,000 views.** Zhus Meme also carries an
owner CPM of **$0.1279**, which accrues to the owner **in addition to** the clipper's $0.20. The real cost of
1,000 views on that campaign is **$0.3279**, not $0.20.

So $0.24 plus $0.15 is not an overpayment. **It is exactly what this campaign costs**, and both halves were
computed from the destination.

**The decisive test.** If the owner side had genuinely stayed on the source campaign (Zhus Edit, owner CPM
$0.3197), the owner figure would read **$0.38**, not $0.15. It reads $0.15, which is the destination's rate
and only the destination's rate.

---

# PART 1 — THE ARITHMETIC, EXACTLY

## 1.1 Every stored figure for clip `cmsktak4y00qf0pl402jdt3t3`

| Field | Stored value |
|---|---|
| clipper | `540fef39` (redacted) |
| campaign | **Zhus Meme (0.20 CPM)** `cmsis9csq00ew0po8gzo98vic` |
| status | APPROVED |
| latest views (`clip_stats`, 1 row) | **1,203** |
| `earnings` | **0.24** |
| `baseEarnings` | 0.24 |
| `bonusAmount` | 0 |
| `bonusPercent` | 2 |
| **`cpmAtSubmissionDecimal`** | **0.2000** |
| **`ownerCpmAtSubmissionDecimal`** | **0.1279** |
| `pricingModelAtApproval` | CPM_SPLIT |
| `minViewsAtApproval` | 1000 |
| `payoutReductionRatio` | null |
| `videoUnavailable` / `isDeleted` | false / false |
| `createdAt` | `2026-08-08 20:14:00.562` |
| `updatedAt` | `2026-08-08 21:20:42.804` |
| `reviewedAt` | `2026-08-08 21:20:42.801` |
| `db_now` | `2026-08-08 21:25:28.277515+00` |

The owner accrual is a **stored row** in `agency_earnings`:

| Field | Value |
|---|---|
| `clipId` | `cmsktak4y00qf0pl402jdt3t3` |
| **`campaignId`** | **`cmsis9csq00ew0po8gzo98vic` = Zhus Meme, the DESTINATION** |
| `amount` | **0.15** |
| `views` | 1,203 |
| `ownerUserIdAtApproval` | null |
| `createdAt` = `updatedAt` | `2026-08-08 21:20:42.837` |

## 1.2 The two campaigns, so the comparison is unambiguous

| | Zhus Edit (0.50 CPM) SOURCE | Zhus Meme (0.20 CPM) DESTINATION |
|---|---|---|
| id | `cmsisj3d800f10po8jvz526hf` | `cmsis9csq00ew0po8gzo98vic` |
| clipper CPM (Instagram) | 0.5000 | **0.2000** |
| **owner CPM (Instagram)** | **0.3197** | **0.1279** |
| `guaranteeOwnerSplit` | true | true |
| `lockedOwnerShareDecimal` (s) | 0.39002074 | **0.39005794** |

**The clip's stamps are 0.2000 and 0.1279. Those are the destination's pair, exactly. Neither is the
source's.**

## 1.3 Independently recomputed from views, stamps and the destination

**Clipper**, `earnings-calc.ts:176`, `baseEarnings = (views / 1000) * cpm`:

```
1203 / 1000 × 0.2000 = 0.24060   →  round2  →  $0.24     matches stored 0.24
```

Bonus: `bonusPercent` is 2, and 2% of 0.2406 is 0.0048, which **rounds to $0.00**. That is why
`bonusAmount` is 0 and `earnings == baseEarnings`. The invariant `earnings ≈ base + bonus` holds at $0.24.

**Owner**, the guarantee path. `tracking.ts:2139-2155` selects it because the campaign has
`guaranteeOwnerSplit = true` and a valid `s`, then calls `calculateOwnerEarningsGuaranteed`
(`earnings-calc.ts:501-509`), which is `clipperGross × (s / (1 - s))`, round2:

```
s = 0.39005794        s / (1 - s) = 0.39005794 / 0.60994206 = 0.6395011
0.24 × 0.6395011 = 0.153480   →  round2  →  $0.15          matches stored 0.15
```

**Cross-checked against the clip's own owner stamp**, the legacy formula at `earnings-calc.ts:457`,
`round2((views / 1000) * ownerCpm)`:

```
1203 / 1000 × 0.1279 = 0.153864   →  round2  →  $0.15      same answer
```

**Both formulas agree to the cent**, which is the signature of an unambiguous clip: the stamped ratio
`0.1279 / 0.2000 = 0.6395` equals the implied `s / (1 - s) = 0.6395011` well inside the 0.01 tolerance at
`owner-share-guard.ts:72`. This clip is classified `gross`, not `ambiguous`.

## 1.4 The counterfactual that settles it

Had the owner side remained on the **source** campaign's rate:

```
SOURCE owner CPM 0.3197:  1203 / 1000 × 0.3197 = 0.384595  →  $0.38
SOURCE via s:             0.24 × (0.39002074 / 0.60997926) = 0.15346  →  $0.15
```

Note both readings of "the source rate". Via the **stamp** the owner figure would be **$0.38**; it is $0.15,
so the stamp is definitively the destination's. Via the **locked share** the two campaigns' `s` values are so
close (0.39002074 versus 0.39005794) that both round to $0.15, so `s` alone cannot discriminate here. **The
stamp can, and it says destination.**

## 1.5 Reconciling the three numbers the owner read

| What he saw | Where it comes from | Correct? |
|---|---|---|
| campaign labelled **"0.20 CPM"** | the campaign NAME, a human typed string. The stored clipper CPM is 0.2000 and the stored **owner CPM is 0.1279**, which the name does not mention | the name is accurate about the clipper side and silent about the owner side |
| **Clipper $0.24** | `earnings-calc.ts:176`, 1.203 × 0.2000 | **correct** |
| **Owner $0.15** | `earnings-calc.ts:501-509` via `tracking.ts:2155`, 0.24 × s/(1-s) | **correct** |
| implied total **$0.39** | 0.24 + 0.15, a combined 0.3279 CPM × 1.203 = 0.39449 | **correct, and it is what the campaign costs** |

**The expectation that $0.20 CPM implies $0.24 total is the only thing here that is wrong.** BL-625 records
the model plainly: the calculator hands a campaign two rate numbers, `clipperCpm` and
`ownerCpm = clipperCpm × s/(1-s)`, and the owner's share is taken **on top of** the clipper's rate from real
money. $0.1279 is exactly $0.20 × 0.6395, so the pair was generated by that calculator and is internally
consistent.

---

# PART 2 — WHAT THE TRANSACTION ACTUALLY WROTE

## 2.1 The audit row, verbatim

`CLIP_CAMPAIGN_REASSIGNED`, by the **OWNER**, at **`2026-08-08 21:19:47.965`**:

```json
{"fromCampaignId":"cmsisj3d800f10po8jvz526hf","fromCampaignName":"Zhus Edit (0.50 CPM)",
 "toCampaignId":"cmsis9csq00ew0po8gzo98vic","toCampaignName":"Zhus Meme (0.20 CPM)",
 "platform":"Instagram","oldClipperCpm":0.5,"oldOwnerCpm":0.3197,
 "newClipperCpm":0.2,"newOwnerCpm":0.1279,
 "rowsRepointed":{"trackingJobs":1,"shadowDecisions":0,"notes":0,"helpRequests":0,"clientFlags":0},
 "clipCreatedAt":"2026-08-08T20:14:00.562Z"}
```

**The audit row records `newOwnerCpm: 0.1279` explicitly.** The feature knew about the owner side, wrote it,
and logged it.

## 2.2 Every field written, against BL-730's enumeration

The feature exports its own field list, `campaign-reassign.ts:324-334`:

```
Clip.campaignId · Clip.cpmAtSubmissionDecimal · Clip.ownerCpmAtSubmissionDecimal
TrackingJob.campaignId · RuleShadowDecision.campaignId · Note.campaignId
ReviewerHelpRequest.campaignId · ClientClipFlag.campaignId
AuditLog (new row) · Notification (new row, clipper)
```

All ten are in the transaction: the clip update at `route.ts:347-355`, TrackingJob at `:358-360`,
CampaignAccount upsert at `:370`, and the four repoints at `:380-383`. The audit row above confirms
`trackingJobs: 1` moved.

**The clip update writes the campaign and BOTH stamps in a single statement, deliberately**
(`route.ts:346-355`):

```ts
// 2. campaignId AND both stamps together. Writing the campaign without the
//    stamps is silent killer 2; they are one update for that reason.
await tx.clip.update({
  where: { id: clip.id },
  data: {
    campaignId: destination.id,
    cpmAtSubmissionDecimal: stamps.clipperCpm as any,
    ownerCpmAtSubmissionDecimal: stamps.ownerCpm as any,
  },
});
```

**Nothing BL-730 required is missing.** The unwritten fields are enumerated with reasons at
`campaign-reassign.ts:340-346`, and each is correct for a PENDING clip: `createdAt` is a fact and is not
rewritten (the era check is a hard block instead); the `*AtApproval` snapshots are null because a PENDING
clip has never been approved; and `earnings` / `baseEarnings` / `bonusAmount` are zero by precondition and
writable only through `writeClipEarnings`.

Both stamps come from the destination via `resolveDestinationStamps` (`campaign-reassign.ts:304-321`), which
resolves the destination's per platform pair and passes the owner side through `enforceCpmStampInvariant`
with `context: "reassign"`.

## 2.3 Stored row or live derivation? **Stored, and it never needed restamping**

The owner accrual is a **stored `agency_earnings` row**. But it was **created at approval, after the move**,
not carried across it:

```
reassigned   2026-08-08 21:19:47.965
approved     2026-08-08 21:20:45.183          (58 seconds later)
agency row   createdAt = updatedAt = 2026-08-08 21:20:42.837
```

`createdAt` equals `updatedAt`, so the row has been written exactly once, and it was written **after** the
reassignment, already pointing at the destination.

**This is structural, not luck.** The transaction re-asserts three preconditions under a row level
`SELECT ... FOR UPDATE` (`route.ts:335-345`): the clip must still be `PENDING`, its `campaignId` must be
unchanged, and **`earnings` must be exactly 0**, else it throws
`"This clip has earned money since you opened this dialog, so it was not moved."`

**A clip with any money on it cannot be reassigned at all**, so there is never a stale stored accrual to
repair. That is BL-736's PENDING only scope doing exactly the job BL-730 designed it for, and it is the
reason this round finds no defect. **Neither failure mode applies here: there is no stale stored row, and no
live derivation reading the wrong campaign.**

**A refinement that matters, because both mechanisms are in play at once.** The **money** is the stored
`agency_earnings` row. The **number on the admin screen is not that row.** It is recomputed in the page at
`admin/clips/page.tsx:1693`:

```ts
normalOwnerAmt = Math.round((viewsForCalc / 1000) * ownerCpm * 100) / 100;
```

where `ownerCpm` comes from `clip.campaign.ownerCpm`, the **current campaign's live rate**, selected at
`api/clips/route.ts:429`. So the admin row is a **live derivation** and the accrual is a **stored row**, and
they are independent.

**Here they agree at $0.15 from both directions**, which is a second, independent confirmation that the clip
really is on the destination: the live derivation reads `clip.campaign`, and if that were still Zhus Edit it
would multiply by 0.3197 and print **$0.38**. It prints $0.15. **The screen the owner was looking at is
itself evidence the reassignment worked.**

Worth logging for a later round: because the display multiplies the **campaign's live rate** rather than the
**clip's stamp**, it will drift from the stored accrual for any clip whose campaign CPM is later edited
without a restamp. That is latent today and out of scope here.

## 2.4 BL-736's locked share claim, verified

BL-736 claimed `lockedOwnerShareDecimal` needs no copying because it is a campaign column rather than a clip
column. **Verified true, and it is part of why the owner side is right.**

`lockedOwnerShareDecimal` lives on Campaign (`schema.prisma:611`); **there is no such column on Clip.** At
approval `tracking.ts:2138-2141` reads `clip.campaign.lockedOwnerShareDecimal`, and after the reassignment
`clip.campaign` **is the destination**, so the destination's `s = 0.39005794` was used. Nothing to copy,
nothing stale.

Honest note: because the two campaigns' `s` differ only at the fifth decimal, this particular clip cannot
prove which `s` was used from the money alone (PART 1.4). The claim is verified from the **schema and the
read path**, not from the arithmetic. Equally, `minViewsAtApproval = 1000` matches **both** campaigns, so
that snapshot is not evidence either way and is not offered as such.

---

# PART 3 — IS THE MONEY WRONG, OR JUST THE DISPLAY?

**The money is right. The reading of it was wrong.**

| Question | Answer |
|---|---|
| Is the clipper credited correctly? | **Yes.** $0.24 = 1.203 × $0.2000, the destination's clipper rate. |
| Is the owner accrual correct? | **Yes.** $0.15 by both the guarantee formula and the clip's own stamp, which agree. |
| Is the destination campaign's recorded spend correct? | **Yes**, on both sides. |
| Is anything over accrued? | **No.** Nothing to self correct, nothing that persists. |

**Both spend filters checked, per BL-642.** The clip side is filtered (`APPROVED`, `isDeleted = false`,
`videoUnavailable = false`, `balance.ts:312`) while the agency side used for legacy `spent` is
**unfiltered** (`balance.ts:315-317`):

| | Zhus Edit SOURCE | Zhus Meme DESTINATION |
|---|---|---|
| clip side, filtered | $52.17 across 49 approved clips | **$85.25 across 110 approved clips** |
| agency side, unfiltered | $33.34 across 30 rows | **$54.51 across 88 rows** |

This clip's $0.24 and $0.15 sit inside the destination's figures on both sides, and its single agency row
carries `campaignId` = destination. **It is attributed once, to the right campaign, on both filters.** The
source retains no trace of it.

The 110 versus 88 gap on the destination is the ordinary population difference, clips that accrue no owner
amount plus the filter asymmetry BL-642 documented, and is not specific to this clip.

**One observation, checked and dismissed as a non finding.** The agency row's `ownerUserIdAtApproval` is
null. That is correct and universal: the destination campaign has no `ownerUserId`, and **all 1,921 agency
rows on the platform have it null**. Not a defect, and not introduced here.

## 3.1 The clipper WAS told, and the message was honest

The tenth written field, the clipper notification, fired **61 milliseconds** after the audit row, to the
clip's own clipper:

| | |
|---|---|
| type | `CLIP_CAMPAIGN_REASSIGNED` |
| title | **"Your clip moved to a lower paying campaign"** |
| body | *"We moved your clip to Zhus Meme (0.20 CPM). Zhus Meme (0.20 CPM) pays $0.20 per 1,000 views instead of $0.50, so this clip will earn less than the campaign it was submitted to. Nothing you did caused this and the clip is still under review."* |
| recipient | `540fef39`, the clip's clipper |
| createdAt | `2026-08-08 21:19:48.026` |
| isRead | false |

**This is the disclosure BL-730 demanded and BL-736 built, working on its first real use.** It names the
destination, states the old and new rate, says plainly that the clip will earn less, and removes blame. It
does not say "fail", "invalid", "denied" or "rejected", so BL-518 and BL-521 hold.

**And note the asymmetry that explains this whole round.** The clipper facing message quotes **$0.20 per
1,000 views**, which is exactly right for the clipper, because $0.20 IS the clipper's rate. The admin row
shows the clipper figure and the owner figure side by side and never says they add up. **The copy written
for the clipper is unambiguous; the screen the owner reads is not.**

---

# PART 4 — HOW MANY OTHER CLIPS

**Exactly one clip has ever been reassigned**, and it is this one:

```
CLIP_CAMPAIGN_REASSIGNED rows: 1     distinct clips: 1
first = latest = 2026-08-08 21:19:47.965
db_now = 2026-08-08 21:26:27.755338+00
```

**Total money affected across the whole population: $0.24 clipper and $0.15 owner, both correct.** There is
no second clip to check and no exposure to quantify.

---

# PART 5 — THE VERDICT AND WHAT TO DO

## 5.1 The verdict, one line

**The owner side restamped correctly: both stamps moved to the destination in a single update inside one
transaction, the stored owner accrual was created after the move already pointing at the destination, and
the $0.15 is the destination's rate rather than the source's.**

## 5.2 There is no code defect and no data repair

**No fix spec is offered because there is nothing to fix.** Stating that plainly is the finding. The
reassignment feature did what BL-730 specified and BL-736 built:

* both stamps written together, never one without the other;
* the whole thing in one transaction with a row lock and three re-asserted preconditions;
* a hard refusal on any clip carrying money, which is why no stored accrual could go stale;
* an audit row that records the old and new rates on **both** sides.

**No data repair is required on this clip.** Its clipper earnings, its owner accrual and its campaign
attribution are each independently correct.

## 5.3 Should the feature be paused?

**No. Do not pause it.** The feature is working. Pausing it on this evidence would remove a correct
capability because of a misread screen, and the population is a single clip whose every figure verifies.

## 5.4 What IS worth changing, and it is a display change only

The real defect this round found is that **the product let its own owner believe he had been overcharged.**
Two things combined:

1. **A campaign name carrying a rate in free text**, "Zhus Meme (0.20 CPM)", which states the clipper side and is silent about the $0.1279 owner side. The name is not derived from the stored rates and nothing keeps it honest if either rate changes.
2. **An admin row showing "Clipper" and "Owner" side by side with no indication that they are additive**, and no combined total anywhere near them.

Anyone reading that row will do the same arithmetic the owner did. **A per row combined figure, or a column
header naming the campaign's total cost per 1,000 views, would have answered the question before it was
asked.** That is a small, display only change and it belongs in its own round.

## 5.5 The display, reviewed

Reviewed by the accessibility lead with the cognitive accessibility and data table specialists. Its
conclusion is worth quoting because it reframes the whole round: **"the display is misleading enough that a
correct money system produced a false bug report, which is the expensive failure direction."**

**What is actually on screen.** `admin/clips/page.tsx:1719-1732`, the non marketplace branch, renders
exactly two things:

```
CLIPPER  $0.24        OWNER  $0.15
```

Labels at `:1721` and `:1728`, values at `:1722` and `:1729`, in one flex row at `:1696`, with identical
wrappers, identical weight and identical 10px uppercase muted labels. **That is the standard idiom for two
slices of one pot, which is precisely the wrong signal.** A grep of all 2,657 lines found **no total, no
`+`, no `=`, no heading over the pair, no tooltip and no legend** anywhere on the page.

**The second rate is in the payload and deliberately never rendered.** `api/clips/route.ts:429` selects
`ownerCpm` and the page reads it at `:1672` only to multiply by it. `clipperCpm` is not selected at all
(`route.ts:427`). **So the reader is shown two dollar figures and neither of the two rates that produced
them.**

**The campaign name is the proximate cause.** At `page.tsx:1550`, one line above the money, the row prints
`{username} · {campaign.name}`, which here is `Zhus Meme (0.20 CPM)`. That `(0.20 CPM)` is a **human typed
substring of `Campaign.name`**. It is not derived from `clipperCpm`, nothing keeps them in sync, and it does
not say whose rate it is. It supplies a confident, wrong multiplicand directly above two currency figures,
and the owner rate appears nowhere on the page for the reader to discover.

**This page is the outlier, and the codebase already does it correctly elsewhere.**
`admin/archive/[campaignId]/page.tsx:167` and `:173` render `Clipper CPM` and `Owner CPM` as separate
labelled fields with a `CPM Split` / `Agency Fee` badge at `:156-158`, and `admin/agency-earnings/page.tsx:155`
prints `Owner CPM:`. **The clips list is the only money surface that hides both rates.**

**The recommended change, display only and touching none of the six money files:** relabel `:1721` and
`:1728` to **CLIPPER GETS** and **OWNER GETS**, add a third cell **BUDGET PAYS** carrying the sum, put one
muted 12px line beneath the group reading **"Two separate rates. The campaign budget pays both."**, and add a
chip beside the campaign name at `:1550` reading **TWO RATES** for CPM_SPLIT (not the raw enum `CPM SPLIT`,
whose meaning this incident proved is not obvious). The stronger version adds `clipperCpm` to the select at
`route.ts:427` and prints **"Rates per 1,000 views: clipper $0.20, owner $0.13. Total $0.33."**, which makes
the free text suffix in the campaign name redundant and removes the drift risk entirely.

**A separate money display defect, found incidentally, and I verified it directly.** `page.tsx:1664-1666`:

```ts
const DASH = "—";
const fmtOrDash = (v) => typeof v === "number" && v > 0 ? formatCurrency(v) : DASH;
```

The comment immediately above at `:1659-1661` says the dash keeps the row *"honest about 'not yet computed'
vs 'really earned $0'"*. **The code does the opposite: `v > 0` renders the identical dash for a genuine
computed `$0.00` and for `null`, so `formatCurrency(0)` is unreachable and the two states it claims to
separate are merged.** A clip zeroed by the `minViews` guard at `:1685-1691` is indistinguishable on screen
from one awaiting its first tick. **Its own round; it is display path only and touches no money file.**

**Accessibility findings on the same block, reported not fixed:** the label and value are sibling spans tied
only by adjacency with no table, no `<dl>` and no headers, and the `inline-flex` wrapper blockifies both
children so swipe navigation announces `Clipper` and `$0.24` as two unlinked stops (**1.3.1, major**); the
em dash glyph is silent at default screen reader verbosity, so an uncomputed card announces as
`Clipper Poster Owner` with no values at all (**1.3.1, major**); the clip list is a bare div with no list
semantics and each card has no role, label or heading (**1.3.1, major**). **Passing and recorded so an
automated sweep does not re flag them:** colour is **not** the sole differentiator (`text-accent` versus
`text-emerald-400` are decorative, each figure carries a text label, so **do not** replace the labels with
colour or icons), and the 10px muted labels measure about **19:1** on `--bg-card`.

**One disagreement between specialists, recorded with attribution.** Cognitive accessibility ruled the
missing additivity a **1.3.1 pass**, since nothing is conveyed visually either and so there is no
presentation to code gap; the data table specialist ruled the label and value pairing a **1.3.1 major
fail**, since that relationship *is* conveyed visually and is not programmatic. Both are right about
different relationships. **The additivity gap is a content defect that WCAG does not cover and a reading
level audit would score clean, which is exactly why it shipped and exactly why it cost a false bug report.**

---

# WHAT COULD NOT BE ESTABLISHED, STATED PLAINLY

* **Which campaign's `s` was used cannot be proven from this clip's money**, because Zhus Edit and Zhus Meme differ only at the fifth decimal (0.39002074 versus 0.39005794) and both round to $0.15. The destination's use is established from the schema and the read path (PART 2.4), not from arithmetic.
* **`minViewsAtApproval = 1000` matches both campaigns**, so it is not evidence of which campaign the approval snapshot came from, and it is not presented as such.
* **The clip has a single `clip_stats` row** (1,203 views at `2026-08-08 21:01:03.839`), so there is no view history to confirm the figures move correctly over time. The next tracking tick will be the first observation of that.
* **Whether the owner intends a campaign name to carry the clipper rate** is a product decision, not something data can answer.

**Nothing was changed by this round.** Read only SQL throughout, handle hashed to an md5 prefix, no wallet
address selected anywhere, every timestamp cast `::text` against DB `now()`. `agency-monitor --fix` was
never run. No clip, campaign, earning, agency or payout row was written.

Platform baseline at `2026-08-08 21:33:05.776926+00`: **4,160 approved clips, $11,913.50, 1,921 agency rows,
161 payout rows, invariant violations 0.** Untouched.
