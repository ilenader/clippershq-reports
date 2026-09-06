# BL-844 — a COMPLETED campaign reads fully spent, and can now be seen at all

Round of 2026-09-06. Branch `checkpoint/BL-844`, base `f3f44d43`, worktree `C:/w844`.

## PART 0 — FIRST LINE: YES, COMPLETED HID THE CAMPAIGN FROM CLIPPERS

**Before this round a COMPLETED campaign appeared on NO clipper surface at all.** The clipper campaign
list gates on `status in ["ACTIVE","PAUSED","PAST"]` (`api/campaigns/route.ts:120`) and COMPLETED is in
neither arm, even with `includePast`. The "Completed campaigns" strip asked for `status === "PAST"` alone
(`api/campaigns/past/route.ts:32`). BL-641 warned exactly this and chose PAST over COMPLETED for that
reason: "a hidden campaign cannot display 100% to anyone."

**AND THE RULE THE OWNER ASKED FOR WAS ALREADY BUILT.** The brief's premise that a third arm must be
added is corrected rather than repeated. BL-641 shipped `isCampaignFinishedForClippers`
(`lib/campaign-clipper-view.ts:196-199`) returning true for PAST **and COMPLETED**, so
`resolveClipperFacingSpent` has raised a COMPLETED campaign to the full marketed budget since
2026-07-23. This round therefore added no arm. It made the rule observable and closed the two things that
made moving a campaign to COMPLETED unsafe.

### Every side effect of the COMPLETED transition, with file:line

| Question | Answer today | Where |
|---|---|---|
| Clipper sees it in the campaign list | **NO, hidden** | `api/campaigns/route.ts:120` |
| Clipper sees it in the Completed strip | **NO** before this round | `api/campaigns/past/route.ts:32` |
| Clipper can open its detail page | **YES** (PAST is 403, COMPLETED has no gate) | `api/campaigns/[id]/route.ts:65,73` |
| Its spend is returned to a clipper | **YES**, already shaped to 100 percent | `api/campaigns/spend/route.ts:88,221` |
| Clipper sees their own clips on it | **YES** | `api/clips/mine/route.ts:106` filters only `isArchived` |
| Clipper sees their earnings from it | **YES**, and already treated as terminal | `api/earnings/route.ts:289` |
| Clip submission | **REFUSED already** | `lib/clipper-submit-core.ts:368` |
| Cron sweep | **EXCLUDED already** | `lib/tracking.ts:3691` inside `if (!campaignIds)` at `:3644` |
| `campaignStatusBlocks` | **COMPLETED WAS MISSING** | `lib/tracking.ts:1961` |
| Tracking jobs on transition | all set `isActive = false` | `api/campaigns/[id]/route.ts:821` |
| Structured status-audit row | **NONE.** Branches exist for PAUSED and ACTIVE only | `api/campaigns/[id]/route.ts:746,763` |
| Campaign event / notification | **NONE** | same |
| Payout cascade (BL-732's void) | **DOES NOT FIRE.** That lives in the DELETE handler, reached by archiving | `api/campaigns/[id]/route.ts:904-992` |
| Withdrawal | **UNAFFECTED.** Campaign status is never read | `api/payouts/route.ts:387` |

Nothing becomes unreachable and no money moves. The unaudited transition is **reported, not papered
over**: writing an audit row from a SQL file would claim the product did something it does not do.

## PART 1 — the rule, and both views proven independently

No arm was added. The existing trigger disjunction in `resolveClipperFacingSpent` already reads
`isCampaignFinishedForClippers(campaign) || isClipperPoolExhausted(...)`, inside the `budgetUsable`
fail-closed guard, feeding `round2(Math.max(totalSpent, budget))`.

**Through the real `/api/campaigns/spend`, same route, one role each:**

| Campaign | CLIPPER sees | OWNER sees |
|---|---|---|
| BAD BITCH ANTHEM (0.50 CPM) | **1112** | **203.02** |
| BAD BITCH ANTHEM (2.50 CPM) | **1112** | **149.82** |
| somesome (BL-641's, unchanged) | **9750** | **5345.82** |

**AN HONEST CORRECTION TO THE BRIEF'S FIGURE.** somesome's true spend is **$5,345.82** today, not the
$5,445.80 BL-641 recorded. The payable set moved as videos were retired since 2026-07-23. The clipper
figure is unchanged at $9,750.00 of $9,750.00, 100 percent.

**26 checks, 0 failures** (`scripts/bl844-verify.ts`). Eleven campaigns now read full, every one FINISHED
or EXHAUSTED and never an ordinary live one; every changed figure went UP or stayed level, so `Math.max`
holds across the population. The fail-closed guard was exercised on null, zero, negative, NaN and string
budgets: none can fabricate a full claim. ACTIVE, PAUSED and DRAFT are untouched.

## The two blockers this round had to close

**1. `campaignStatusBlocks` — ONE MONEY FILE, ONE LINE OF CODE, LOUDLY JUSTIFIED.** The gate had four
arms and COMPLETED was not among them; BL-641 and BL-732 both named the gap and neither closed it. Both
target campaigns are AUTO-paused (`pauseSource = "AUTO"`, stamped 2026-08-13) and `isAutoPausedCampaign`
requires `status === "PAUSED"`. **Moving them to COMPLETED would have REMOVED an earnings freeze that
holds today.** The cron is not the hole: the sweep excludes COMPLETED, but that exclusion sits inside
`if (!campaignIds)` (`:3644`) and a MANUAL bulk check passes `campaignIds`, skipping it while
`source === "manual"` still satisfies the conjunct — so one press of "Check Clips Now" reached the
earnings write. The full diff is 1 line of code plus 38 of comment:

```diff
       (isAutoPausedCampaign ||
         freshCampaign?.isArchived === true ||
         freshCampaign?.status === "PAST" ||
+        freshCampaign?.status === "COMPLETED" ||
         isOldWindowClip);
```

It can only ever REFUSE: skipping the earnings block leaves every column as it was, so it cannot pay a
cent more, cannot raise a stored figure and cannot lower one. No arithmetic is introduced. `force-now`
stays exempt, unchanged, as the documented revival path for a wrongly frozen clip.

**2. COMPLETED IS OVERLOADED — rejecting a DRAFT sets it.** Found by the accessibility review reading the
other writer of this status: `admin/campaigns/page.tsx:986` sends `status: "COMPLETED"` under a toast
reading "Campaign rejected." Without a guard, every campaign the owner ever REFUSED would have appeared
to clippers badged "Completed" — and at **0 percent, not 100**, because a campaign with no approved clips
never gets a key in the spend map (`spend/route.ts:88`) and so never reaches the resolver. The strip's
COMPLETED arm therefore carries `clips: { some: {} }`. PAST stays UNCONDITIONAL, so all nine PAST
campaigns are unchanged including the four with zero clips that clippers see today. **The overload itself
is reported, not changed** — whether rejection deserves its own status, or should archive instead, is the
owner's decision.

**Also fixed on the way past: a live `clientName` leak.** `campaigns/past/route.ts` selected
`clientName: true`, and `shapeCampaignsForClipper` does not strip it because `OWNER_SIDE_FIELDS`
(`campaign-clipper-view.ts:78-87`) lists the eight rate and share fields, not that one. CLAUDE.md is
explicit that `clientName` is never selected into a clipper-facing response. Pre-existing for PAST, and
widened by this round's own change, so it was fixed rather than reported. Removed from the select rather
than added to a strip list: nothing reads it (0 occurrences in `CampaignsRedesign.tsx`, one consumer at
`campaigns/page.tsx:42`), and a field never fetched cannot be re-exposed by a later shaping change.
Verified on the live response: `clientName` absent, `lockedOwnerShareDecimal` absent, 11 campaigns
returned.

## PART 2 — display only, and the fingerprints say so

Whole-population fingerprints before and after (`scripts/bl844-money-snapshot.ts`):

- **`payout_fp` byte-identical** — no payout changed state, BL-732's cascade did not fire, and both
  in-flight payouts ($91.32 and $29.44) are intact. BL-696 double-open 0, BL-824 `paid_without_stamp`
  26 unchanged (pre-existing, not a regression).
- **The two campaigns' own clip fingerprint byte-identical**, and their clipper-side spend **$213.37
  before and after, to the cent**.
- BL-627 invariant violations **0** before and after. Money-out **$7,003.89** unchanged. Budgets and
  `manualSpent` unwritten.
- **No withdrawable amount moved** and no payout became payable or unpayable: the withdrawal gate never
  reads campaign status.

**Six other fields moved and every one is attributed to live activity on OTHER campaigns:** a clipper
submitted to Zhus Meme at 18:48:41, the cron credited $0.35 of owner accrual on Zhus Edit, and one
tracking job was created for that new clip — reconciling the active-job count exactly at
8250 − 162 + 1 = **8089**.

**DISCLOSED: the round did not run alone at the database.** A concurrent session's sandbox (`bl845sbx-`)
created two campaigns at 18:49:19 and 18:53:31, which is what moved the campaign fingerprint. Both carry
`isTestCampaign = true` and this route still applies `filterTestCampaigns`, so neither can reach an
ordinary clipper at any status.

## PART 3 — the two campaigns, measured before they moved

| | 0.50 CPM | 2.50 CPM |
|---|---|---|
| Marketed budget | $1,112.00 | $1,112.00 |
| Clipper pool cap | $672.31 | $672.15 |
| Clipper-side spend | $122.73 | $90.64 |
| Owner-side spend | $80.29 | $59.18 |
| **TRUE total spend** | **$203.02** | **$149.82** |
| PENDING / FLAGGED clips | 0 / 0 | 0 / 0 |
| Payouts in flight | 1, $91.32 | 1, $29.44 |
| Clipper positions | 10 | 15 |
| Clipper-facing figure BEFORE | $203.02 of $1,112.00 | $149.82 of $1,112.00 |
| Clipper-facing figure AFTER | **$1,112.00 of $1,112.00, 100%** | **$1,112.00 of $1,112.00, 100%** |

**No STOP condition was met, and each was checked before the move rather than after.** No clip becomes
unreviewable (0 pending, 0 flagged). No clipper loses access to money: the withdrawal gate never reads
campaign status. Both campaigns were **already** AUTO-paused and frozen, so the move takes no accrual
from anybody — and the `campaignStatusBlocks` arm above keeps the freeze rather than lifting it.

25 clipper positions, of which **7 hold a positive balance under the $10 platform minimum, totalling
$25.68**. Every one was already unreachable before this round. **What changes for those seven is that the
app stops lying to them** — see PART 4.

Applied via `scripts/migrations/BL-844-COMPLETED-two-campaigns.sql`, guarded on id AND name AND expected
status: rowCount 1, 1 and 162. The rollback was written and printed FIRST
(`scripts/migrations/BL-844-ROLLBACK.sql`), restoring both rows to PAUSED / AUTO with their exact
original `lastBudgetPauseAt` and `updatedAt`, and all 162 tracking jobs to active. `manualSpent` left
NULL on both, which is BL-641's decision restated: writing 1112 there would be the hardcoded
per-campaign number BL-535 forbids, and it would override the derived rule at
`CampaignsRedesign.tsx:158`.

## PART 4 — what the clipper is told, and it is now true

BL-765's `accrueMap` (`api/earnings/route.ts:289`) is `!(PAST || COMPLETED || isArchived)`, so COMPLETED
already satisfies the finished condition. `campaignMinimumState` (`lib/below-minimum-campaigns.ts:113`)
returns `"finished"` and the row renders the shipped string at `EarningsPremium.tsx:548`:

> • campaign finished, so this balance will not grow

**This move FIXES a false promise rather than creating a confusion.** BL-765 flagged that a
PAUSED-and-not-archived campaign is deliberately treated as still able to accrue, and asked for it to be
revisited. These two were PAUSED, not archived, and AUTO-frozen — so the app was telling seven clippers
"$X to go" on money that could never grow. They are now told the truth. Confirmed on screen at all five
widths, and nothing contradicts it: a clipper who clears the minimum sees no such sentence, correctly,
because they can withdraw.

## PART 5 — evidence and merge

- **Rule applies to any campaign moved to COMPLETED**: keyed on `Campaign.status` alone, no id, no name,
  no date. 26/26 checks.
- **Clipper 100 percent vs owner true spend**: proven through the real route, both roles, table above.
- **Both existing arms unchanged**: somesome still $9,750.00 of $9,750.00 at 100 percent; nine PAST
  campaigns all still full; ACTIVE/PAUSED/DRAFT untouched; `Math.max` never lowered a figure.
- **No stored figure moved**: fingerprints above; invariant 0; no payout changed state.
- **Render: 15 shots, 120 assertions, 120 passed, 0 failed**, 0 at the wrong width, 0 with horizontal
  overflow, at 320 / 375 / 414 / 1280 / 1440, as a clipper who actually holds a blocked balance on a
  named campaign and as the owner. **The first run reported 3 reds and they were the harness:** a
  `getByText` wait failed at 320, 375 and 414 on the owner page while every content assertion on that
  identical DOM passed, because `getByText` also demands Playwright-visibility. A wait that disagrees
  with the assertion it guards is measuring the locator, so it now polls `innerText` directly. Both runs
  are recorded here rather than only the green one.

### Accessibility, four items, all implemented

The review ran before the change and returned four blocking items, one of which is not a WCAG issue and
is labelled as such (the rejected-draft overload, above).

- **A cascade inversion that penalised exactly one cohort.** `CampaignsRedesign.tsx:249` carried
  `opacity-80` alongside `motion-safe:opacity-0` and a `forwards` animation ending at `opacity: 1`. A
  filling animation sits in the animation origin and beats a normal author declaration, so the 20 percent
  knockdown reached **only readers who ask for reduced motion**, dragging the CPM figure to **3.41:1
  against 4.71:1 for everyone else** — failing 1.4.3 at 18px bold, under WCAG's 18.667px large-text
  threshold and so with no 3:1 allowance. Removed, which levels the cohorts instead of pushing everyone
  onto the worse number. `--border-strong` replaces `border-white/12` (1.36:1); the two are one fix.
- **`grayscale(1)` deletes the accent hue**, collapsing #2596be to roughly #818181, so the CPM figure and
  the percentage now use ink that survives the filter.
- **Copy at grade 9.96 asserting something false.** "Previous successful campaigns we've run." claimed
  success over a bucket with no spend floor where four of nine campaigns hold zero clips. Now "These
  campaigns have ended. You cannot submit clips to them." at grade **2.88**, which also states the one
  fact the page never gave.
- **The percentage was withheld from assistive technology.** Two equal figures spoken with identical
  prosody carry no audible equality marker, so the sr-only bar value now includes it — not worded as
  "fully spent", because a campaign with no approved clips reads 0 percent there.

Confirmed by the review and not changed: the strip's cards are correctly not links, nothing inside them
is focusable, the `tabIndex={0}` on the scroller is required rather than tidy-uppable, the badge passes
contrast across every photo it can sit on (6.77:1 to 8.39:1), and the shared word "Completed" is more
accurate for a COMPLETED campaign than for a PAST one.

### Safety

No schema change, no `prisma migrate`, no index, no Apify actor run, the 11 BL-678 guards untouched, 0
Supabase pool errors. **9 of the 10 protected files byte-identical by blob OID on both refs**; only
`tracking.ts` differs, by the one line above. `npm run build` exit 0 with the hooks gate at **0 errors
and 10 warnings** against a ceiling of 11; `tsc` exit 0 with 0 errors from a clean baseline recorded on
the untouched worktree first; eslint v9.39.4 confirmed present so the gate is a real check. BACKLOG 176
to 177, counted with `grep -c`. `checkpoint/BL-723` is not an ancestor of main.

**One slip of mine, recorded:** I wrote a `{/* */}` JSX comment into JS expression position and a `//`
comment inside a ternary branch, which broke the parse twice for 8 `TS1005`-class errors before I read
the actual failing lines instead of guessing at them.

**Requires a Railway REDEPLOY.** Until it lands the two campaigns are absent from the clipper campaign
list, which is exactly what COMPLETED does on the deployed code; the earnings wording is already correct
because that half was already live. The redeploy is what puts them into the Completed strip at 100
percent.
