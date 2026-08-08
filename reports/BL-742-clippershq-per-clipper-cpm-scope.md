# BL-742 — a per clipper CPM is safe ONLY as a ratio preserving scale of BOTH stamps, and the retroactive half of the request should not be built

**2026-08-08 · READ ONLY · Base:** `main @ 6d906941` · **Branch:** `checkpoint/BL-742`
**Nothing was changed. No code, data, schema or money. Nothing restamped, nothing recalculated. Every query went through `scripts/run-select.js`, which refuses every write keyword. Handles are redacted to an md5 prefix. Every timestamp is cast `::text` against DB `now()`.**
**No build, `tsc` or lint run was performed and none is claimed: this round produced one markdown file, which cannot change them.**

---

# PART 6 FIRST — THE VERDICT, IN ONE LINE

**A retroactive per clipper CPM is NOT safe to build as asked, because the current code would write already earned money DOWNWARD with no guard on that path, putting 37 clipper campaign pairs below money they have already been paid and creating $1,103.41 of shortfall; the safe version is a ratio preserving per clipper rate that applies to FUTURE clips only.**

The rest of this report is the evidence, and PART 6 at the end carries the build ready spec.

---

# PART 1 — WHAT A RETROACTIVE RESTAMP ACTUALLY MEANS

## 1.1 The stamp, and everything downstream of it

The rate is frozen on the clip at submission in two columns, `prisma/schema.prisma:988-989`:

```
cpmAtSubmissionDecimal       Decimal? @db.Decimal(10, 4)   // the clipper's rate
ownerCpmAtSubmissionDecimal  Decimal? @db.Decimal(10, 4)   // the owner's rate
```

Resolution order when earnings are computed, `earnings-calc.ts:374-384`: `clipperCpmOverride` first, then
`cpmAtSubmissionDecimal`, then a live campaign lookup. **The stamp beats the campaign**, which is what makes
a per clip rate representable at all.

Everything downstream, with file:line:

| # | Downstream of the stamp | Where |
|---|---|---|
| 1 | Clip base earnings, bonus and gross | `earnings-calc.ts:374-384` then `recalculateClipEarningsBreakdown` |
| 2 | The 4 invariant fields, written only through the chokepoint | `clip-earnings-writer.ts` (`writeClipEarnings`) |
| 3 | L1 budget hard lock, throws if projected exceeds budget | `clip-earnings-writer.ts:196-240` |
| 4 | BL-167 clipper pool clamp, and BL-718's paid floor | `clip-earnings-writer.ts:361-390` |
| 5 | The owner accrual row `AgencyEarning` | `cpm-restamp.ts:198-224`, `tracking.ts:2154-2160` |
| 6 | Owner amount on the guarantee path, derived from the CAMPAIGN's `s` | `tracking.ts:2139-2155`, `earnings-calc.calculateOwnerEarningsGuaranteed` |
| 7 | Owner amount on the legacy path, derived from the CLIP's owner stamp | `tracking.ts:2157-2159` (`calculateOwnerEarnings`) |
| 8 | Per tick ratio cap on the crossing clip, which reads the CAMPAIGN's rates | `tracking.ts:2563-2568` |
| 9 | Campaign recorded spend, and therefore auto pause | `balance.ts:312-380` |
| 10 | Clipper pool cap and owner reserve cap, both from one `s` | `balance.ts:403-404` |
| 11 | Clipper available balance, and so every payout gate | `balance.ts`, `api/payouts/route.ts` |
| 12 | Already created payouts: **nothing recomputes them** | no write path; they are historical rows |
| 13 | The repair and audit tooling's ability to ever re derive the row | `owner-share-guard.ts:57-79`, `agency-monitor.ts:150-190` |
| 14 | Era boundary: **not** downstream of the stamp | `campaign-era.ts`, keyed on `createdAt` versus boundary, not on rate |

Item 12 is the one that hurts, and item 13 is the one that is permanent.

## 1.2 THE DECIDING QUESTION, TRACED RATHER THAN ASSUMED

**If a clip has already earned at $0.50 and its CPM is restamped to $0.30, what happens to the money already earned?**

Three answers were offered. **The current code does the first one: it recalculates the earnings DOWNWARD, and
writes it.** Traced, not assumed:

**Step 1. The mechanism already exists and already ships.** `src/lib/cpm-restamp.ts` (440 lines) is the
"apply to existing clips" path, wired to a real checkbox at `admin/campaigns/page.tsx:184` and `:1814`, sent
as `payload.applyToExistingClips` at `:588`, and honoured at `api/campaigns/[id]/route.ts:844`. Its own
header says it "recomputes earnings using the NEW campaign CPM (via `clipperCpmOverride` to bypass the
stamp priority in earnings-calc)".

**Step 2. It computes the new, lower figure unconditionally.** `cpm-restamp.ts:158-161`:

```ts
const newEarnings = applyPayoutReductionCap(breakdown.clipperEarnings, reductionRatio) ?? 0;
```

There is no comparison against the stored value anywhere in the file.

**Step 3. BL-538's never decrease guard does NOT cover this path.** `decideNeverDecrease`, the function that
actually blocks a decrease, is imported at exactly **two** call sites in the entire repo:

```
src/app/api/admin/force-recalc-earnings/route.ts:13
src/lib/campaign-freeze-undo.ts:84
```

`cpm-restamp.ts` imports `logAudit`, `writeClipEarnings`, `recalculateClipEarningsBreakdown`,
`calculateOwnerEarnings`, `applyPayoutReductionCap`, `getStreakBonusPercent`, `getCampaignCpmForPlatform`
and `loadConfig`. **It does not import the guard.** The brief's expectation that "BL-538's never decrease
guard should forbid it" is **false for this path**.

**Step 4. BL-718's paid floor does not catch it either, because it only fires on an increase.**
`clip-earnings-writer.ts:197-198`:

```ts
const delta = rounded.earnings - (Number(current.earnings) || 0);
if (delta > 0) {
```

The **entire** L1 budget hard lock **and** the BL-718 paid floor at `:383` live inside that `if`. The file
says so itself at `:361`: *"This clamp is reached ONLY on an increase (the whole block is inside
`if (delta > 0)`)"*. **A downward write skips every one of those protections and is written through.**

**So the answer is unambiguous: earnings are recalculated downward and persisted. There is no guard on the
path. Already created payouts are untouched, so the clipper's recorded earnings can land below cash that
has already left.** That is exactly BL-716's shape.

## 1.3 BL-716 AT SCALE, MEASURED ON LIVE DATA

BL-716 found one clipper written below what he had been paid, costing **$60.47** and needing a manual
repair. Modelling a halving of the clipper rate, computed on the same basis the withdrawal gate uses
(`APPROVED`, `isDeleted = false`, `videoUnavailable = false`; paid = `PAID`, or `VOIDED` with a non null
`paidAt`, taking `actualPaidAmount ?? amount`):

```
pairs_total                     309
pairs_with_a_payment             49
ok_today                        300
already_below_paid_today          9      (the known BL-627 over held population)
would_flip_below_if_halved       37
shortfall_created_usd        $1,103.41
earnings_erased_on_those     $1,219.78
total_erased_if_all_halved   $4,162.24
db_now = 2026-08-08 20:52:06.6991+00
```

**37 new BL-716 incidents, and $1,103.41 of shortfall.** That is **18 times the money** and **37 times the
manual repairs** of the single incident that produced BL-716.

The worst cases, redacted, ordered by shortfall created:

| clipper | campaign | clips | earned | already paid | halved to | shortfall created |
|---|---|---|---|---|---|---|
| 29961807 | bees.n.honey | 38 | $390.42 | $390.42 | $195.21 | **$195.21** |
| 8638e0d7 | somesome | 12 | $350.00 | $350.00 | $175.00 | **$175.00** |
| a92aea47 | Panic Baby | 71 | $195.98 | $195.80 | $97.99 | $97.81 |
| 4e623834 | bees.n.honey | 84 | $111.50 | $104.62 | $55.75 | $48.87 |
| f191a2b2 | STRAENGE | 24 | $94.53 | $94.53 | $47.27 | $47.26 |
| b1e30e69 | somesome | 30 | $93.18 | $93.18 | $46.59 | $46.59 |

**A single clipper, $195.21, on one campaign. Three times BL-716's entire incident.**

Note the pattern in that table: several rows have `earned` exactly equal to `paid`. Those clippers have
withdrawn everything they earned. **A clipper who has cashed out fully is maximally exposed: any downward
restamp at all puts them immediately below what they were paid**, with no clawback path and, per BL-627,
no recoverability.

Scale of a single operation: one clipper on one campaign can carry **218 clips** (`d378b5e5` on WinGram),
so a per clipper restamp is a 200 plus row write, not a handful.

## 1.4 The dangerous direction has never been exercised in production

`audit_logs` holds **17** `CPM_RESTAMP_ON_EDIT` rows, all on 2026-06-14, all from `campaign-patch`, and
**every one of them went UPWARD** (0.8 to 1.0). **Sixteen of the seventeen moved $0.00**, because those
clips had zero earnings; the seventeenth moved $0.80 to $1.00.

**The retroactive restamp has therefore never once been run downward, and has never moved more than twenty
cents of real money.** The machinery exists, but the path this request needs is effectively untested in
production.

---

# PART 2 — THE AMBIGUITY PROBLEM

## 2.1 The test that decides everything, and it is about the RATIO only

`src/lib/owner-share-guard.ts:57-79` is the shared decision (BL-563 pulled it here so the monitor and
`gamification.ts` cannot drift apart):

```ts
const impliedByLockedShare = s / (1 - s);
const stampedRatio = (args.ownerCpm as number) / (args.clipperCpm as number);
if (Math.abs(impliedByLockedShare - stampedRatio) > 0.01) {
  return { kind: "ambiguous" };
}
```

**The test is purely on the ratio of the two stamps. The absolute size of the CPMs is irrelevant to it.**

**I tested both designs against that exact tolerance, over every `s` live on the platform** (the nine values
in PART 2.3), six representative campaign CPMs including the awkward $0.9137 and $0.07, and thirteen scale
factors from 0.1 to 5.0, with both stamps rounded HALF UP to 4dp exactly as BL-625 stores them:

```
RATIO PRESERVING (scale BOTH stamps by k):
  cases = 702   failures = 0   worst drift 0.005714 against the 0.01 tolerance
  worst case: s=0.45054945, campaign CPM $0.07, k=0.1 -> stamps 0.0070 / 0.0057

CLIPPER ONLY (the naive "give this clipper a different CPM"):
  tested = 648   would become AMBIGUOUS = 648   (100.0%)
```

**Every single clipper only case becomes permanently ambiguous. Not most of them. All of them.**

The ratio preserving design passes everywhere, but note the worst case honestly: at a $0.07 campaign CPM
with `k = 0.1` the margin is only about 1.75 times the tolerance, because 4dp rounding of a
five thousandths stamp is coarse. That is a bound to enforce, not a reason to reject the design, and PART
6.2 enforces it.

That single fact answers the round's central question:

* **Scale BOTH stamps by the same factor k.** `ownerCpm/clipperCpm` is unchanged, the clip stays `gross`, it remains repairable, and **no ambiguity is created**.
* **Change the clipper stamp alone.** The ratio moves, the clip becomes **`ambiguous` permanently**, and `agency-monitor.ts:178-180` then **skips it forever**: *"SKIPPED entirely, so `--fix` can never touch them"*.

BL-539 and BL-570 priced that second outcome at **$933.94** on one campaign.

## 2.2 Every place that assumes one CPM per campaign, file:line

| # | Site | What it assumes | Survives a ratio preserving per clipper rate? |
|---|---|---|---|
| 1 | `schema.prisma:611-615` `lockedOwnerShareDecimal` | ONE `s` per campaign, locked at creation, never re stamped | **Yes.** `s` is a share, not a rate. |
| 2 | `api/campaigns/route.ts:577`, `api/campaigns/[id]/route.ts:407-418` | `s` is set once and only when currently NULL ("FIRST lock only") | **Yes**, untouched. |
| 3 | `balance.ts:403-404` `clipperPoolCap = (1-s) * realBudget`, `ownerReserveCap = s * realBudget` | one `s`; caps are DOLLAR ceilings | **Yes.** Dollars, not rates. |
| 4 | `tracking.ts:2139-2155` guarantee owner lock, `owner = clipperGross × s/(1-s)` | one `s` | **Yes, and this is the strong result.** Owner is derived from the FINAL clipper amount, so `owner/total == s` holds exactly whatever individual rates are. |
| 5 | `tracking.ts:2157-2159` legacy owner, `calculateOwnerEarnings(views, ownerCpm, base, cCpm)` | the CLIP's stamps | **Yes**, if both stamps scale. |
| 6 | **`tracking.ts:2563-2568` per tick ratio cap on the crossing clip** | **reads `clip.campaign.clipperCpm` and `clip.campaign.ownerCpm`, the CAMPAIGN rates, NOT the clip stamps** | **NO. This is a real uniformity assumption.** On the one tick where a campaign crosses its budget, the truncated split is computed from campaign rates and a custom rate is silently ignored. Bounded to the crossing clip only, and the ratio it applies is the same ratio, so it misallocates at most one clip's cents. |
| 7 | `owner-share-guard.ts:70-74` ambiguity test | stamped ratio must equal `s/(1-s)` | **Yes if the ratio is preserved. NO if only the clipper stamp moves.** This is the gate. |
| 8 | `agency-monitor.ts:178-180` | ambiguous rows are skipped forever | **Yes**, and it is the reason ratio preservation is mandatory. |
| 9 | `campaign-clipper-view.ts` fully spent rule (BL-531/535/641) | pool cap from one `s` against the marketed budget | **Yes.** It compares dollars to dollars. |
| 10 | `campaign-era.ts` | boundary is `clip.createdAt` versus a status change row | **Yes.** Not rate aware at all. |

**The answer to "does a per clipper rate break the owner share arithmetic": NO, provided the ratio is
preserved.** The guarantee path is mathematically invariant to per clip rates, because it derives the owner
from the final clipper figure rather than from a rate. Only site 6 assumes uniformity in live arithmetic,
and its blast radius is one clip on one tick.

**What a per clipper rate DOES break, if built naively, is the RE DERIVATION tooling**, not the runtime.
That is precisely BL-539's finding restated.

## 2.3 The current ambiguity population, measured live

Applying `owner-share-guard`'s own test across all 13 guarantee campaigns:

| campaign | status | locked s | clips | unstamped | agree | **ambiguous** | ambiguous clipper $ |
|---|---|---|---|---|---|---|---|
| somesome | PAST | 0.32885906 | 383 | 282 | 1 | **100** | **$557.06** |
| GainzAlgo (REPOST) | PAST | 0.50000000 | 766 | 737 | 29 | 0 | $0.00 |
| bees.n.honey | PAST | 0.45054945 | 765 | 589 | 176 | 0 | $0.00 |
| Panic Baby | PAUSED | 0.33333333 | 524 | 88 | 436 | 0 | $0.00 |
| WinGram | PAUSED | 0.33333333 | 658 | 583 | 75 | 0 | $0.00 |
| STRAENGE | PAST | 0.33333333 | 140 | 131 | 9 | 0 | $0.00 |
| Zhus Meme (0.20 CPM) | ACTIVE | 0.39005794 | 109 | 0 | 109 | 0 | $0.00 |
| Zhus Edit (0.50 CPM) | ACTIVE | 0.39002074 | 49 | 0 | 49 | 0 | $0.00 |
| BAD BITCH ANTHEM (0.50) | ACTIVE | 0.39540508 | 62 | 23 | 39 | 0 | $0.00 |
| BAD BITCH ANTHEM (2.50) | ACTIVE | 0.39555126 | 35 | 22 | 13 | 0 | $0.00 |
| SomeSome | PAUSED | 0.33333333 | 16 | 0 | 16 | 0 | $0.00 |
| Deja Shoe / CROCS | PAUSED | 0.40011998 | 18 | 18 | 0 | 0 | $0.00 |
| db_now | | | | | | | 2026-08-08 20:56:13.496766+00 |

**Exactly one campaign is contaminated, somesome, and it is PAST and frozen.** Every ACTIVE campaign has
**zero** ambiguous clips. The platform is clean today. **A clipper only CPM would deliberately create the
first ambiguous rows on a LIVE campaign**, and unlike somesome's they would be permanent by design rather
than by accident, so the "only the owner can resolve it" escape hatch would never resolve.

## 2.4 The same defect already exists, latently, in a feature that shipped

`owner-submit-core.ts:190` already accepts a per clip custom rate:

```ts
if (customCpm != null && customCpm > 0) effectiveCpm = Math.min(customCpm, campaignCpm);
```

Two properties matter. First it is **downward only**: `Math.min` means the owner can never pay a clipper
MORE than the campaign rate through this path. Second, and worse, `owner-submit-core.ts:256-261` stamps the
clipper side at `effectiveCpm` while the owner side comes from
`platformCpmResolved.ownerCpm ?? campaign.ownerCpm`, **the campaign rate, unreduced**.
`enforceCpmStampInvariant` does not rescue it: `cpm.ts:212` returns immediately when the owner stamp is
already non null, so it only ever fills a NULL, it never rescales.

**So any use of `customCpm` on a guarantee campaign produces an AMBIGUOUS clip on creation.** BL-539
established that `customCpm` has never actually been used, so this is latent rather than realized, but it
is the owner's requested feature in miniature, already carrying the exact defect this report is about.

---

# PART 3 — THE BUDGET QUESTION

## 3.1 The caps are dollar ceilings, so rates cannot breach them

`balance.ts:403-404` sets `clipperPoolCap = round2((1 - s) * realBudget)` and
`ownerReserveCap = round2(s * realBudget)`, both in dollars. BL-630's ghost fee is already subtracted
before the caps are taken (`balance.ts:358-364`, `realBudgetFromFee`), and the ghost fee is then added
back into `spent` at `:375` so a fully earned pool reads as the marketed figure fully spent. **None of that
is rate aware.** A per clipper CPM changes how fast the pool drains and who drains it, never how large it is.

Three independent mechanisms bound the crossing tick, all of them dollar based and all unchanged by a per
clipper rate: the per tick truncation inside a Serializable transaction (`tracking.ts:2519-2586`), the L1
throw in `writeClipEarnings` (`clip-earnings-writer.ts:196-240`), and the BL-167 pool clamp (`:361-390`).

**So a per clipper rate cannot push a campaign over budget in the UPWARD direction.** BL-627's property
survives.

## 3.2 Live headroom, and one campaign that must be treated carefully

Computed on `balance.ts`'s exact basis (clipper side `APPROVED`, `isDeleted = false`,
**`videoUnavailable = false`**; owner side the legacy UNFILTERED agency aggregate, per the comment at
`balance.ts:333-341`):

| campaign | status | budget | spent | headroom | pool cap | pool headroom |
|---|---|---|---|---|---|---|
| **Panic Baby** | PAUSED | $3,000.00 | **$3,000.00** | **$0.00** | $2,000.00 | small |
| BAD BITCH ANTHEM (0.50) | ACTIVE | $1,112.00 | $174.04 | $937.96 | $672.31 | $567.08 |
| BAD BITCH ANTHEM (2.50) | ACTIVE | $1,112.00 | $71.15 | $1,040.85 | $672.15 | $629.15 |
| Zhus Edit (0.50 CPM) | ACTIVE | $2,000.00 | $84.16 | $1,915.84 | $1,219.96 | $1,168.63 |
| Zhus Meme (0.20 CPM) | ACTIVE | $8,000.00 | $136.98 | $7,863.02 | $4,879.54 | $4,795.98 |
| WinGram | PAUSED | $5,000.00 | $429.51 | $4,570.49 | $3,333.33 | $3,046.68 |
| Deja Shoe / CROCS | PAUSED | $9,000.00 | $0.00 | $9,000.00 | $5,398.92 | $5,398.92 |

**No campaign is over budget. BL-627's property holds.**

**A correction I am making explicitly, because I nearly published the opposite.** A first pass that omitted
`videoUnavailable = false` from the clipper side reported Panic Baby **$40.73 OVER** budget. On the basis
the code actually uses it is **exactly $3,000.00 of $3,000.00, headroom $0.00, not over**. Retired clips
inflate the naive figure. The lesson generalises: any tooling built for this feature must use
`balance.ts`'s basis and not an approximation of it.

**Panic Baby is nevertheless the campaign to be careful with**: at exactly $0.00 headroom, any upward per
clipper rate there would be refused outright by the L1 throw at `clip-earnings-writer.ts:224-231`, which is
correct behaviour but will surface to the owner as an error rather than as a rate change.

## 3.3 The consequence the owner will not expect

On the guarantee path the owner's accrual is `clipperGross × s/(1-s)` (`tracking.ts:2155`). **So raising one
clipper's rate raises the OWNER's accrual on that clipper's clips by the same proportion, out of the same
budget.** The two pools drain together by construction.

**This means "pay this clipper more out of my share" is not expressible as a ratio preserving rate.** Paying
one clipper more without changing the owner's cut requires breaking the ratio, which is precisely what
creates permanent ambiguity. The owner should be told this plainly: a per clipper rate makes the campaign
spend faster on both sides, it does not move money from the owner to the clipper.

---

# PART 4 — WHAT THE CLIPPER EXPERIENCES

Reviewed by the accessibility lead across six specialists. Its verdict on the disclosure question was
**no ship as specified**, and the strongest evidence is not about screen readers at all.

## 4.1 The platform has already PROMISED clippers this will not happen, in writing, by email

Verified verbatim in the source, not paraphrased:

**To the clipper, `src/lib/email.ts:820`**, in the campaign update email:

> "Existing clips keep their original rates. Only new submissions earn at the updated rates."

**To the owner, `src/components/campaigns/CampaignMoneyCalculator.tsx:357`**, in the confirmation shown at
the moment he authorises a CPM change:

> "This replaces the campaign's stored budget, clipper CPM and owner CPM with the calculated values.
> Existing clips keep their own stamped CPM."

**And as an architectural guarantee, `prisma/schema.prisma:982-984`:**

> "F-CPM-FREEZE — CPMs frozen at submission time. The earnings calc reads these FIRST so a future edit to
> `campaign.cpm{Platform}Clipper` / `clipperCpm` **cannot retroactively shift any existing clip's earning
> rate**."

**All three are already false whenever `restampClipsForCampaign` runs.** The retroactive path contradicts a
documented invariant, a reassurance shown to the owner at the point of authorisation, and a promise the
platform has emailed to clippers. Building a per clipper version would not introduce that contradiction; it
would industrialise it and point it at one named person.

## 4.2 What they would actually see: a smaller number, and nothing else

**No surface in the product explains a change in earnings.** There is no rate history, no changelog, no "your
rate changed" record on any clip or campaign screen. The clipper's per clip figure and campaign total would
simply be smaller than they were yesterday.

**And the record of what they were paid would still show the old, larger world.** Payout rows are historical
and nothing recomputes them (`PayoutsRedesign.tsx:137-144`), so a clipper would see a payout for $390.42
sitting above a campaign balance that now says they earned $195.21. **That contradiction is visible, is
permanent, and has no explanation anywhere in the product.**

## 4.3 Would they be told? Today, no, and the delivery path is broken even if a message were written

The accessibility lead found four independent blockers on the notification path, each verified against the
installed dependency rather than the code comments:

1. **The toast can silently never appear.** `navbar.tsx:152-182` toasts only `notifs[0]` per refresh, and only when `sessionStorage.last_seen_notif_id` already exists. Any chattier notification arriving in the same 60 second window suppresses the money message entirely, and it never shows on a session's first refresh.
2. **The toast destroys itself under a keyboard user.** sonner 2.0.7 pauses its timer on `expanded || interacting || isDocumentHidden`, and `expanded` is set by mouse events only. `globals.css:707` freezes the visible progress bar on focus while the real dismissal timer keeps running, so the card is destroyed at 5.5 seconds (`notification-toast.tsx:180`) while appearing held. **WCAG 2.2.1 Timing Adjustable, Level A.** The accessibility comment at `notification-toast.tsx:12-24` claims a `role="status"` and `aria-atomic="true"` that sonner does not emit; the lead retracted its own earlier assessment after the dependency was read.
3. **The dollar figures are suppressed from the accessible name.** `notifications/page.tsx:526` puts an `aria-label` of title plus read state on the `<a>` wrapping the row. An author supplied name overrides content for links, so the body at `:496`, which is where the money is, never reaches a screen reader.
4. **The persistent record is undiscoverable and self clearing.** `navbar.tsx:425` is the only link to `/notifications` anywhere in the repo, with no sidebar entry; the bell at `:331` has no accessible name at zero unread; and opening it calls `markAllRead()` at `:337-343`, which clears the only "not dealt with" signal and starts the 60 day deletion clock (`api/cron/notifications-cleanup/route.ts:28,48-53`).

**And the message would not fit.** `page.tsx:483` truncates, `:496` clamps to three lines,
`notification-toast.tsx:137` clamps to two. A sentence carrying the old rate, the new rate, the clip count
and the dollar delta is cut off in all three surfaces, and no surface in the product renders it in full.
A clipper cannot be expected to recall a rate they were never able to read.

## 4.4 The blast radius reaches people who were never part of the decision

* **Referrers lose commission** they have already been credited, silently (`ReferralsRedesign.tsx:356-357`). A third party's money moves because of a deal they are not party to and will never be shown.
* **Gamification level can go backwards.** The self heal at `gamification.ts:566-581` recomputes level from lifetime earnings, against the explicit and permanent promise rendered at `ProgressPremium.tsx:460` that a level bonus "never resets".
* **A celebration toast can fire on the way down** (`MomentumCard.tsx:114-130`), congratulating a clipper during a level change caused by their pay being cut.

## 4.5 The judgement, stated as the brief requires

**A visible drop in historical earnings, with no explanation available anywhere in the product, is
indistinguishable from being robbed.** The clipper did the work, the work was accepted, the money was shown
to them, and then the number went down. From their side there is no way to tell that apart from theft,
because the product offers no evidence either way.

The platform has already reached this conclusion itself. `src/lib/notifications.ts:21-24`, written for
BL-736's far gentler PENDING only reassignment, says the clipper "must not be left to discover a changed
rate on their own, which BL-730 said **would feel like being cheated**." BL-730 and BL-736 accepted that
reasoning for clips that had earned **nothing**. This round proposes it for clips that have earned, been
withdrawn and been spent.

**Recommendation: a retroactive change should not be possible at all.** Not gated behind a confirmation, not
behind a warning, not behind an audit row. The honest design is future clips only, which is what the
platform has already promised in writing, and it needs no disclosure machinery because nothing a clipper has
already been shown ever changes.

**Reported, not fixed, and independent of this feature.** White on accent `#2596be` measures **3.40:1**
against the 4.5:1 AA bar at small sizes (`notifications/page.tsx:317`, `:326` at about 2.4:1, and the unread
bell badge at `navbar.tsx:349`), so the two elements a clipper checks when hunting for a money message are
the least legible text on the page. Separately, `globals.css:43-45` sets `--text-primary`,
`--text-secondary` and `--text-muted` **all to `#ffffff`** in dark mode, so the intended text hierarchy
carries no colour differentiation at all. Both predate this request and deserve their own round.

---

# PART 5 — THE SAFER DESIGNS, RANKED

## Option A. Per clipper per campaign rate, FUTURE clips only, ratio preserving. **RECOMMENDED.**

**What it is.** A stored per (clipper, campaign) rate multiplier `k`. At submission, both stamps are scaled:
`cpmAtSubmissionDecimal = campaignClipperCpm × k` and `ownerCpmAtSubmissionDecimal = campaignOwnerCpm × k`.
Existing clips are never touched.

**What breaks: essentially nothing.**
* The ratio is preserved exactly, so `owner-share-guard.ts:72` classifies every clip `gross`. **No ambiguous rows, ever.**
* The guarantee owner lock already produces the right owner amount with no change (`tracking.ts:2155`).
* Pool caps, budget, ghost fee and the fully spent rule are dollar based and untouched.
* No already earned money moves, so BL-538, BL-627 and BL-716 are all preserved **by construction rather than by a guard**.
* Site 6 (`tracking.ts:2563-2568`) still uses campaign rates on the crossing clip. Bounded to one clip, and worth fixing in the same round.

**Build cost: small.** One nullable table or column keyed on (userId, campaignId), a resolver consulted at
the three stamping sites (`clipper-submit-core.ts:557`, `owner-submit-core.ts:256`, and the marketplace
path), an owner UI, and an audit row. No migration of existing data. No recompute.

**What could go wrong at scale: very little.** The worst case is a mis typed `k` on future clips only,
correctable by changing `k` back, because nothing was restamped.

## Option B. An earning time multiplier instead of a stamp

**What it is.** Leave stamps alone; multiply at computation time in `earnings-calc`.

**What breaks.** The multiplier is not frozen, so it applies retroactively to every recompute of every
existing clip the moment it is set. **That is Option D wearing a disguise**, and it reintroduces the whole
of PART 1. It also violates the F-CPM-FREEZE principle that a clip's rate is fixed at submission, and it
leaves no per clip record of what rate was actually used, which makes disputes unanswerable.

**Build cost:** small. **Risk:** high and non obvious. **Not recommended.**

## Option C. A one off bonus or adjustment, every stamp intact

**What it is.** Pay the difference as a discrete credit rather than changing any rate.

**What breaks: nothing at all.** No stamp moves, no earnings recompute, no ambiguity, no budget change
beyond the credit itself.

**Honest caveats.** There is **no admin route anywhere that creates a payout row** (recorded in
`docs/OWED-MANUAL-PAYMENTS.md` and confirmed by BL-719), so today this is a manual payment plus a document,
not a feature. And a credit that flows through clip earnings would need to respect the pool cap, so on a
full campaign like Panic Baby it would be refused.

**Best for a one time correction, wrong as a standing arrangement.**

## Option D. The full retroactive restamp, as asked. **NOT RECOMMENDED.**

**What breaks, all of it measured above:**
1. Already earned money is rewritten downward with **no guard on the path** (PART 1.2).
2. **37 clipper campaign pairs land below money already paid, $1,103.41 of shortfall** (PART 1.3), each one a BL-716 style manual repair.
3. If only the clipper stamp moves, **every touched clip becomes permanently ambiguous, 648 of 648 cases** (PART 2.1), and the repair tooling abandons it forever, which is the $933.94 shape.
4. A clipper's historical earnings visibly drop with no explanation anywhere in the product (PART 4).
5. **It breaks a promise the platform has emailed to clippers** (`email.ts:820`), a reassurance shown to the owner at the moment he authorises (`CampaignMoneyCalculator.tsx:357`), and the documented F-CPM-FREEZE guarantee (`schema.prisma:982-984`).

**Build cost: deceptively small**, because `cpm-restamp.ts` already exists and would need only a `userId`
filter. **That is the trap.** The machinery is one filter away, which makes the dangerous thing the easy
thing.

**Scale risk: high.** One clipper on one campaign can carry **218 clips**, and the downward path has
**never been run in production** (PART 1.4).

## Ranking

| Rank | Option | Retroactive hazard | Ambiguity | Build cost | Verdict |
|---|---|---|---|---|---|
| **1** | **A. Future clips only, ratio preserving** | none | none | small | **Build this** |
| 2 | C. One off adjustment | none | none | small, but no payout route exists | Good for a single correction |
| 3 | B. Earning time multiplier | **high, hidden** | none | small | Reject |
| 4 | D. Full retroactive restamp | **$1,103.41 measured** | **permanent** | small, which is the danger | **Reject** |

**Honest answer to the question actually asked: the thing he asked for is not the thing he should build.**
He asked for past, present and future. **Present and future are safe and cheap. Past is not, and past is
the only part that carries every one of the four hazards.**

If the intent behind "past" is that the clipper should be made whole for work already done at a rate the
owner now considers too low, **Option C pays that directly, with no stamp touched and no risk at all.**
That combination, Option A going forward plus Option C for the backlog, delivers the owner's actual goal
with none of Option D's exposure.

---

# PART 6 — THE VERDICT AND THE BUILD READY SPEC

## 6.1 The verdict

**A retroactive per clipper CPM is NOT safe to build: the current code would write already earned money
downward with no guard on that path, putting 37 clipper campaign pairs below money already paid and
creating $1,103.41 of shortfall, and a clipper only rate change would make every touched clip permanently
unrepairable. A per clipper rate applying to FUTURE clips only, scaling BOTH stamps together, is safe and
carries none of those hazards.**

## 6.2 Build ready spec for Option A

**Data.** One additive nullable table, applied with `ALTER TABLE ... ADD COLUMN IF NOT EXISTS` style DDL
through `scripts/run-schema-sql.js`, **never `prisma migrate`**:

```
clipper_campaign_rates
  userId       text     not null
  campaignId   text     not null
  rateMultiplier  Decimal(10,4)  not null   -- k, the SCALE, not a CPM
  createdAt / createdBy / note
  unique (userId, campaignId)
```

**Store `k`, the multiplier, not an absolute CPM.** A multiplier preserves the ratio by construction and
cannot be typed in a way that breaks it. An absolute CPM invites exactly the clipper only edit that creates
ambiguity.

**Bounds, and one of them comes straight out of the measurement in PART 2.1.** `k` in `[0.1, 5.0]`, at most
4 decimal places, validated server side in one shared function the way `validateCampaignMinPayout` is.
**Additionally refuse any `k` whose resulting stamps would round below $0.0100 on either side.** At a $0.07
campaign CPM with `k = 0.1` the stamps become 0.0070 and 0.0057, and 4dp rounding at that magnitude eats
0.005714 of the 0.01 tolerance. The floor keeps the margin comfortable at every live `s` rather than
relying on the tolerance's last thousandth. Refuse any `k` that would make either stamp non positive.

**Resolution, at the three stamping sites only.** `clipper-submit-core.ts:557`, `owner-submit-core.ts:256`
and the marketplace submit path. Both stamps scale:

```
cpmAtSubmissionDecimal      = round4(campaignClipperCpm × k)
ownerCpmAtSubmissionDecimal = round4(campaignOwnerCpm   × k)
```

**Nothing else changes.** No earnings recompute, no restamp, no touch to `cpm-restamp.ts`.

**What must be proven before it ships:**
1. `owner-share-guard.decideOwnerGross` returns `gross`, never `ambiguous`, for every `k` in the allowed range, across the live `s` values (0.32885906, 0.33333333, 0.39002074, 0.39005794, 0.39540508, 0.39555126, 0.40011998, 0.45054945, 0.50000000). **PART 2.1 already ran this: 702 cases, 0 failures, worst drift 0.005714.** Re run it against the shipped `decideOwnerGross` rather than a reimplementation, and include the $0.0100 stamp floor so the worst case moves further inside the tolerance.
2. Zero existing clips change: the ambiguous count stays at somesome 100 and 0 everywhere else, and total approved earnings stay $11,908.81 across 4,159 clips.
3. The pool cap and L1 lock still refuse an over budget write, tested against Panic Baby at $0.00 headroom.
4. A clipper with no row behaves byte identically to today.
5. The owner is shown, before saving, that raising `k` also raises the owner accrual on that clipper's clips proportionally and drains the shared budget faster (PART 3.3).

**Fix in the same round:** `tracking.ts:2563-2568` should read the clip's stamps rather than
`clip.campaign.clipperCpm` / `ownerCpm`, so the crossing clip truncates on its own rate. One clip's worth
of cents, but it is the only live uniformity assumption and it is cheap to close while the context is loaded.

**Also in scope, because Option A makes them true again rather than false:** the two reassurance strings at
`CampaignMoneyCalculator.tsx:357` and `email.ts:820` currently promise that existing clips keep their
original rates. **Option A honours both**, so they need no edit. If the owner ever chooses Option D instead,
those two strings must be corrected in the same change, because shipping D leaves the platform telling
clippers in writing something it has just stopped doing.

**Explicitly NOT in scope:** any restamp of existing clips, any change to `cpm-restamp.ts`, any change to
`lockedOwnerShareDecimal`, and any of the 6 money files. `campaign-era.ts` is not rate aware and is not
touched. The notification delivery defects in PART 4.3 are real and should be their own round, but Option A
**needs no notification at all**, which is one of its main advantages: there is nothing to disclose because
nothing a clipper has already seen ever changes.

**Rollback:** delete the row, or set `k = 1`. Because nothing is ever restamped, **rollback is complete and
instant, and no clip's history is disturbed.** That property is the entire argument for Option A.

---

# WHAT COULD NOT BE MEASURED, STATED PLAINLY

* **Whether the owner intends the coupled owner accrual** (PART 3.3). That is a business decision, not data.
* **The exact per campaign effect of a specific `k`** on future spend rate, which depends on future view counts and cannot be projected from current rows.
* **The 37 pair model assumes a uniform halving** of every pair's earnings. A real per clipper change touches one pair, so the correct reading is the per incident column (worst case $195.21), with the 37 and $1,103.41 as the platform wide exposure if the feature were used broadly.
* **Whether the 9 pairs already below paid** would be worsened; they are excluded from the 37 because they are already in that state (BL-627 measured them at $142.59 and unrecoverable).
* **The clipper side of a downward restamp on a marketplace clip** was not modelled; `cpm-restamp.ts` excludes marketplace clips by design, so the question does not arise for that path.

**Nothing was changed by this round.** Read only SQL throughout, handles hashed to an md5 prefix, no wallet
address selected anywhere, every timestamp cast `::text` against DB `now()`. Platform baseline at
`2026-08-08 20:59:34.709274+00`: **4,159 approved clips, $11,908.81, 161 payout rows, 1,920 agency rows**,
unchanged and untouched.
