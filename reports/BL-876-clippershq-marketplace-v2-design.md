# BL-876 — the second marketplace, designed completely, before any code

**2026-09-16 · AUDIT AND DESIGN ONLY. NOTHING WAS BUILT.** No code, no schema, no data, no config
changed. One file added: this report. Base `origin/main` @ `8dcc0c02`. Branch `checkpoint/BL-876`.
Isolated worktree `C:\w\bl876`, a short path, `node_modules` never junctioned, **removed at the end
and verified by listing the path**.

> ## THE HEADLINE, IN FOUR SENTENCES
> **The design is buildable and its shape already exists in this codebase, but it is NOT the existing
> marketplace's shape and must not be built by copying it wholesale.** The existing marketplace is one
> submission to one slot to one post; this is one clip to many posts, and the entity that has no
> counterpart today is the approved catalogue clip that fifty people draw from.
> **The duplicate problem the owner feared does not exist.** Fifty posters posting one video produce
> fifty DIFFERENT live URLs, so every existing duplicate gate passes untouched; nothing needs
> bypassing, weakening or flagging. That is measured below, not argued.
> **The real consequence he has not addressed is not budget speed, it is CONCENTRATION plus a second
> bonus stack**, and the one thing that caps it today is the campaign budget and nothing else.
> **The single sharpest structural risk is one line:** if the editor's 45 percent and the owner's 10
> percent are not added to the campaign spend aggregate, the never-exceeded-budget invariant breaks
> silently by 55 cents in every dollar, and no test that only reads `Clip.earnings` would see it.

---

## PART 0 — HOW THIS ROUND WAS RUN, AND WHAT IT DISTURBED

### It disturbed nothing

| | |
|---|---|
| code, schema, data, config changed | **none.** Every file operation was a read |
| database connections opened | **ZERO, by this round and by every subagent** |
| **the connection cap, stated** | **ZERO concurrent, ZERO total.** No `run-select.js`, no Prisma CLI, no `psql`, no node script that connects. Fourteen subagents were each told in their own prompt that opening a database connection was forbidden, and none was given a reason to |
| why the cap is zero rather than one | BL-825 caused **four real failed reads** against the owner's live database, and BL-872 held at most 3 of 90 connections that way. This is a design round. Every question it had to answer is answerable from source, from the schema file and from prior reports, so **no figure here needed a live read and none was taken** |
| timestamps | no timestamp was read from the database, so there is nothing to cast. Where a prior report's measured figure is quoted, it is attributed to that report and to the clock that report recorded |
| vendor calls | **none.** No Apify, no HikerAPI, no LamaTok, no YouTube, no Google Drive. Cost of this round to the owner in vendor spend: **$0.00** |
| build | **not run, and none is claimed.** A markdown-only diff cannot change `tsc` |
| handles and wallets | no handle printed, no wallet address read or printed |
| counting | every count in this report comes from a `grep -c` or from a prior report's `COUNT(*)`, never from a count piped through `head` |

### The model split, and the saving

| tier | what ran there | subagents | tokens |
|---|---|---|---|
| **cheapest (Haiku)** | pure retrieval: the Prisma data model, the marketplace API routes, the marketplace UI surfaces, the duplicate check, the strike machinery, the payout deduction fields, the notification machinery, the campaign-type and clips-list inventory | **8** | **883,104** |
| **middle (Sonnet)** | non money-touching design: the poster's experience, the editor's experience, the owner's experience, the three campaign types, the Drive and thumbnail research, and the accessibility requirements | **6** | **850,305** |
| **strongest (Opus), NOT SPLIT** | the money model in PART 1, the invariant analysis in PART 7, the conversion action's money movement in PART 3, the open questions in PART 8, the build plan in PART 9, and the reconciliation of every subagent finding | **0 subagents. This orchestrator did all of it** | |

**NOTHING MONEY-TOUCHING WAS SPLIT, AND HERE IS THE ONE PLACE THAT NEEDS SAYING PLAINLY.** One Haiku
subagent was asked to INVENTORY the payout deduction fields, because locating fields is retrieval. Its
inventory was then checked line by line against source by this orchestrator, and **one of its
characterisations was wrong and is corrected in PART 1**: it described BL-866's devaluation as
multiplying `clip.earnings`, `clip.baseEarnings` and `clip.bonusAmount` permanently. That is the shape
BL-826 broke and BL-866 explicitly REJECTED. BL-866 restamps the per-clip CPM pair and never rewrites
stored earnings (`reports/BL-866-clippershq-clip-devaluation.md`, PART 0, "CHOSEN: TWO (restamp the
CPM)"). **No money conclusion anywhere in this report rests on a subagent.** Every figure in PART 1 was
derived by this orchestrator from `earnings-calc.ts`, `trainer-cut.ts`, `payout-calc.ts`,
`clip-earnings-writer.ts` and `payouts/[id]/review/route.ts` read directly.

**The saving, stated honestly. 1,733,409 tokens ran below the strongest tier**: 883,104 of file reading,
grepping and enumerating on the cheapest, and 850,305 of non money-touching design on the middle one.
**The dollar saving is NOT stated because it was not measured:** this session does not have the owner's
billed per-token rates, and inventing a figure from list prices would be exactly the kind of unsourced
number this report exists to avoid. What IS measurable is the split: **fourteen subagents, not one of
them on the strongest tier, 1.73 million tokens of work kept off it, and every money question answered by
the strongest tier with no subagent between it and the source.**

### What was read, and what was deliberately not

Read: the eleven prior reports the brief named (BL-841, BL-845, BL-847, BL-849, BL-868, BL-870, BL-871,
BL-874, BL-834, BL-835, BL-826, BL-863, BL-861, BL-864, BL-866, BL-824, BL-627, BL-696, BL-538, BL-539,
BL-763), the marketplace's models, routes, permissions and surfaces, the campaign model, the clips list
and the payout row's deduction mechanism. **BL-518 and BL-521 have no report in either repository**;
their rules were taken from `BACKLOG.md:18976-19009` where both rounds are recorded in full, and
BL-531 from `docs/BL-531-CLIPPER-POOL-DISPLAY.md`. Not read: anything unrelated to this design.

---

## PART 1 — THE MONEY MODEL

### 1.1 The order the percentages apply, and the reason it is not a choice

The owner asked which comes first, because 45 percent of gross and 45 percent of the post-fee remainder
are different numbers. **They are not, and the proof is arithmetic rather than preference.**

Two deductions are in play and both are flat percentages of the same base:

* the three-way split, 45 / 45 / 10
* the payout fee, **9 percent standard or 4 percent for a referred user**, decided at payout creation
  from `payoutUser?.referredById` (`src/app/api/payouts/route.ts:447`) and applied to the payout GROSS
  (`src/lib/payout-calc.ts:93`), never at earnings time (`earnings-calc.ts:187-189` says so in its own
  comment)

**Worked both ways on a $100.00 gross clip, both parties standard and unreferred:**

| order | editor | poster | owner |
|---|---|---|---|
| **split first, then each earner pays his own fee** | 45.00 gross, fee 4.05, **cash 40.95** | 45.00 gross, fee 4.05, **cash 40.95** | platform row 10.00 + fees 8.10 = **18.10** |
| **fee first, then split the remainder** | 45% of 91.00 = **40.95** | 45% of 91.00 = **40.95** | 10% of 91.00 = 9.10 + fee 9.00 = **18.10** |

**Identical to the cent, in every column.** `40.95 + 40.95 + 18.10 = $100.00 exactly.`

**BUT THE SECOND ORDER STOPS BEING DEFINABLE THE MOMENT THE TWO EARNERS ARE ON DIFFERENT FEE RATES, AND
THAT IS THE ARGUMENT.** The fee is a property of the WITHDRAWING USER, not of the clip. An editor who
arrived through an invite link pays 4 percent; a poster who did not pays 9. "Take the fee off the gross
first" has no single rate to take off. Worked, editor referred and poster not:

| | gross | fee | cash |
|---|---|---|---|
| editor (referred, 4%) | 45.00 | 1.80 | **43.20** |
| poster (unreferred, 9%) | 45.00 | 4.05 | **40.95** |
| owner: platform row | 10.00 | | **10.00** |
| owner: the two payout fees | | | **5.85** |
| **owner total** | | | **15.85** |

`43.20 + 40.95 + 15.85 = $100.00 exactly.`

> **SO THE ANSWER IS: SPLIT THE GROSS FIRST, 45 / 45 / 10, AND LET EACH EARNER PAY HIS OWN FEE ON HIS
> OWN WITHDRAWAL.** It is the only order that is defined for two earners, it produces identical cents to
> the other order whenever the other order is even definable, and it is byte-for-byte the shape the
> existing marketplace already uses (`calculateMarketplaceEarnings`, `earnings-calc.ts:629-691`, which
> caps the gross first and then splits). **This is not an owner decision. It is arithmetic, and it is
> the one question in the brief that answers itself.** The choice that IS his is in 1.3.

### 1.2 The residual, and why the owner's leg must be computed last

The existing marketplace computes the platform leg as a RESIDUAL, not as an independent multiplication
(`earnings-calc.ts:657-663`, F-SEC-2A-FIX). The same must hold here:

```
gross       = min((views / 1000) * cpm, maxPayoutPerClip)
editorBase  = round2(gross * 0.45)
posterBase  = round2(gross * 0.45)
platformBase = max(0, round2(round2(gross)) - editorBase - posterBase)
```

**Worked at a sub-cent boundary, gross $0.55:** `round2(0.2475) = 0.25` each, platform
`0.55 - 0.25 - 0.25 = 0.05`. Three legs sum to `$0.55` exactly. The owner's leg is 9.09 percent of that
clip rather than 10, and that is correct: the residual absorbs the drift so nothing is created and
nothing is lost. **Three independent multiplications would have produced `0.25 + 0.25 + 0.06 = $0.56`,
a cent from nowhere, on every clip landing on that boundary.** At $0.11: `0.05 + 0.05 + 0.01 = $0.11`.

### 1.3 The choice that IS the owner's: does the 10 percent REPLACE his normal cut, or ADD to it

**BL-841 measured that in the existing marketplace it REPLACES it.** `isCpmSplit = !isMarketplaceClip
&& …` at `tracking.ts:2047` and `clips/[id]/review/route.ts:520`, so **no `AgencyEarning` row is ever
written for a marketplace clip**. The owner's ordinary per-clip cut is switched off and the flat 10
percent stands in its place.

This is not an abstract preference here, it is a single boolean in the build. A v2 clip that leaves
`isMarketplaceClip = false` (which PART 2 shows it MUST, for isolation) falls into the `isCpmSplit`
branch by default and **an `AgencyEarning` row is written on top of the 10 percent unless the build
explicitly excludes it.** So the build round must make this choice deliberately, in one place, with the
owner's answer written beside it.

**What each choice earns him per $100 of gross, on a CPM_SPLIT campaign with a 33.33 percent owner
share, both earners standard:**

| | his platform row | his ordinary cut | the two payout fees | **his total** | what the campaign spends |
|---|---|---|---|---|---|
| **REPLACES** (the existing marketplace's behaviour) | 10.00 | 0.00 | 8.10 | **$18.10** | $100.00 |
| **ADDS** (10 percent on top of the ordinary split) | 10.00 | 33.33 | 8.10 | **$51.43** | $133.33 |

**The second row is the one to read twice.** Adding does not move money from the earners to the owner;
it makes the CAMPAIGN pay more for the same views, because the ordinary owner cut is priced on top of
the clipper CPM rather than out of it. On an `AGENCY_FEE` campaign the arithmetic differs again. **This
is question 1 in PART 8 and it is not answered here.**

### 1.4 Every other deduction, stacked, and proved to sum

All of these sit on the WITHDRAWAL, after the split, and each applies to whichever earner is
withdrawing. Order and base, quoted from source:

1. **Platform fee.** `feePercent = referredById ? 4 : 9` (`payouts/route.ts:447`);
   `feeAmount = round2(requestedAmount * feePercent / 100)` (`payout-calc.ts:93`). Base is the payout
   GROSS.
2. **Express premium, 4 percent, BL-763.** `expressFeeAmount = round2(requestedAmount * 4 / 100)`
   (`payout-calc.ts:104-106`). **Base is the GROSS, and BL-863 is the authority**, recorded verbatim in
   `payout-calc.ts:183-187`: *"The express premium is charged on the GROSS: 4% of $100 is $4.00, not 4%
   of $91.00 which would be $3.64."* Verified by BL-863 against all 82 real EXPRESS rows.
3. **Trainer cut, 10 percent, BL-835.** `TRAINER_CUT_PERCENT = 10` (`trainer-cut.ts:131`). Base stated
   in that file's own header: *"the trainer's base is the gross, less the platform fee, less any
   referrer share, and those two always sum to nine points"*, so **base = gross x 0.91 whether or not
   the clipper is referred**. Express is deliberately excluded
   (`TRAINER_BASE_INCLUDES_EXPRESS = false`). Clamped to `roomAfterFees` (`payout-calc.ts:121-122`).
4. **`finalAmount = round2(amount - feeAmount - expressFeeAmount - trainerCutAmount)`**
   (`payout-calc.ts:129`).
5. **Referral commission, 5 percent, minted at PAID**, on `(actualPaidAmount ?? finalAmount) +
   trainerCutAmount` (`payouts/[id]/review/route.ts:1004-1018`), which is BL-835 holding the referrer
   harmless from the trainer. It is paid out of the platform's side, not out of the earner's.
6. **BL-866 devaluation.** **It does not appear in this stack at all, and the subagent inventory that
   said it multiplies stored earnings is corrected here.** BL-866 RESTAMPS the per-clip CPM pair
   (`devaluedRatio`, `devaluedPrevClipper`, `devaluedPrevOwner`, `schema.prisma:1113-1117`),
   ratio-preserving via `decidePerClipCpmPair`, and clamps at a floor equal to money already paid,
   stating the clamp loudly. It changes the RATE a clip earns at, forward, and the next tick recomputes
   from total views. **On a v2 clip that rate feeds all three legs at once, which is PART 7's problem,
   not PART 1's.**

**The full stack, on the poster's $45.00 leg of a $100 clip. Poster referred, express bought, trainer
engaged. Every step shown:**

| step | arithmetic | result |
|---|---|---|
| his gross leg | `round2(100.00 * 0.45)` | **$45.00** |
| platform fee, 4 percent referred | `round2(45.00 * 4 / 100)` | $1.80 |
| express premium, 4 percent of GROSS | `round2(45.00 * 4 / 100)` | $1.80 |
| trainer base | `45.00 * 0.91` | $40.95 |
| trainer cut, 10 percent, room `45.00 - 1.80 - 1.80 = 41.40` | `round2(4.095)` clamped to 41.40 | $4.10 |
| **finalAmount** | `45.00 - 1.80 - 1.80 - 4.10` | **$37.30 cash** |
| referrer, 5 percent of `37.30 + 4.10` | `round2(41.40 * 0.05)` | $2.07 |
| trainer's own withdrawal, 9 percent on his $4.10 (`trainerCashFromCut`, `trainer-cut.ts:590-599`) | `4.10 - 0.37` | trainer cash $3.73 |

**Reconciled against the poster's $45.00 leg:** `37.30 (poster) + 2.07 (referrer) + 3.73 (trainer) +
1.90 (owner: 1.80 fee + 1.80 express - 2.07 referrer + 0.37 trainer's fee) = $45.00 exactly.` Nothing
created, nothing lost, no dollar deducted twice.

### 1.5 Who pays the withdrawal fee, with two earners on one clip

**Each earner pays his own, on his own withdrawal, at his own rate. Neither pays any part of the
other's.** The fee is stamped per payout row at creation from the requesting user's `referredById`
(`payouts/route.ts:447`), and a payout row belongs to exactly one user.

Three consequences worth stating:

* **The owner collects the fee twice per clip instead of once**, and it comes to exactly the same
  money: 9 percent of $45 twice is $8.10, which is 9 percent of the $90 distributed. He is neither
  better nor worse off per dollar.
* **The number of payout rows rises by one per editor per campaign.** Every payout control BL-861 and
  BL-864 built (price-down, settle-unpaid, the sent-to-admin marker) is a MANUAL per-row action. Editors
  are few and posters many, so the added load is modest, but it is not zero and it is real work.
* **A referral commission taken on a marketplace withdrawal carries NO platform fee of its own**
  (`payouts/referral-request/route.ts:165`, quoted: `finalAmount: total, // commissions have no platform
  fee`). That is existing behaviour and it is unchanged by this design.

### 1.6 THE MULTIPLIER NOBODY HAS STATED OUT LOUD

Fifty posters post one editor's clip. That clip produces **fifty earning `Clip` rows against one
campaign budget**, and fifty editor-earning rows all pointing at one person.

**Worked. Campaign budget $5,000. Clipper-facing CPM $1.00. Each of fifty posts reaches 100,000 views.**

| | |
|---|---|
| gross per post | `(100000 / 1000) * 1.00` = **$100.00** |
| gross across fifty posts | **$5,000.00 — the entire budget, from ONE editor's single clip** |
| the editor's take | `50 * 45.00` = **$2,250.00 gross, $2,047.50 cash**, for one piece of work made once |
| each poster's take | $45.00 gross, $40.95 cash |
| the owner's take | $500.00 platform + $405.00 in fees = **$905.00** |

**THE HONEST CORRECTION FIRST, BECAUSE THE OWNER'S FEAR IS AIMED SLIGHTLY OFF TARGET.** Fifty posters do
**not** drain the budget fifty times faster **per view**. The campaign pays the same CPM per thousand
views whichever flow produced them: fifty clippers each making their own clip and each reaching 100,000
views also spends exactly $5,000. **What the multiplier actually changes is three things, and each one
is real:**

1. **WALL-CLOCK SPEED, because good creative replicates.** Fifty posters pushing one PROVEN clip will
   generate more total views, sooner, than fifty posters each gambling on their own. The budget does
   empty faster, not because the rate changed but because the views arrive faster. Nothing in the
   platform models that, and nothing needs to; it is the feature working.
2. **A GENUINE PER-VIEW INCREASE, AND THIS ONE IS ARITHMETIC.** Bonuses are added ON TOP of each
   party's share, computed against that party's own profile, and the platform's leg gets none
   (`earnings-calc.ts:667-668` in the existing marketplace's twin). **A v2 clip carries TWO bonus
   stacks where a normal clip carries one.** At a 10 percent editor bonus and a 5 percent poster bonus,
   a $100 gross clip disburses `49.50 + 47.25 + 10.00 = $106.75`. **The campaign pays 6.75 percent more
   per view than the same views bought through a normal clip, and the owner's slice falls from 10
   percent to 9.37 percent of what actually leaves.** BL-841 found this exact defect in the existing
   marketplace and recorded that *"nobody appears to have written down that the marketplace doubles
   it"*. **It is now written down twice.** It is not a loss and not an overpay; it is simply not what
   45 / 45 / 10 describes, and the owner should know the real number before he prices a campaign.
3. **CONCENTRATION.** One editor can capture an unbounded share of one campaign's budget. In the worked
   example he takes 45 percent of the whole thing. Nothing in the platform limits that today.

**DOES BL-627's NEVER-EXCEEDED BUDGET INVARIANT STILL HOLD? YES, CONDITIONALLY, AND THE CONDITION IS
ONE LINE OF CODE.** BL-627 proved no clipper can be paid past a campaign's budget going forward, via
per-tick truncation inside a Serializable transaction (`tracking.ts:2335-2534`), the L1 hard lock in
`writeClipEarnings` which reads COMMITTED spend and throws (`clip-earnings-writer.ts:199-257`,
`:215-247`), and per-campaign SEQUENTIAL tracking so there is no same-campaign concurrency. All three
survive fifty posts unchanged, because fifty posts are fifty ordinary `Clip` rows on one campaign and
the engine already handles many clips on one campaign.

**The condition:** `spent` in `getCampaignBudgetStatus` (`balance.ts:487-497`) must include the v2
editor and platform aggregates, exactly as BL-627 recorded it already including *"clip earnings +
CPM_SPLIT owner agg + marketplace creator/platform"*. **If the two new aggregates are not added there,
55 cents in every v2 dollar is invisible to the budget lock, a $5,000 campaign distributes $11,111
before it pauses, and every test that reads `Clip.earnings` passes.** This is the single line PART 7
calls the sharpest structural risk, and it is stated here because it belongs to the money model first.

**WHAT CAPS A SINGLE POPULAR CLIP DRAINING A CAMPAIGN IN A DAY? MEASURED, AND THE ANSWER IS
UNCOMFORTABLE.**

| existing cap | does it cap the multiplier | why |
|---|---|---|
| `campaign.budget` + L1 hard lock + auto-pause | **YES, on the total** | Total spend cannot exceed budget and the campaign auto-pauses at the cap (`lastBudgetPauseAt`). Conditional on the aggregate fix above |
| `campaign.maxPayoutPerClip` | **partly** | Caps the GROSS of each post, so fifty posts cost at most fifty caps. It bounds the per-post size, not the post count |
| `campaign.maxClipsPerUserPerDay` (`schema.prisma:685`) | **NO** | Per user per day. Fifty different posters each posting once are entirely unaffected |
| `MarketplacePosterListing.maxEarningsPerCreatorUsd` (the Y2 cap, `clip-earnings-writer.ts:507-535`, BL-299) | **NO, AND THIS IS THE GAP** | It caps one creator's total earnings on one LISTING. **v2 has no listing**, so this cap has no v2 counterpart unless one is built. It is the nearest existing thing to "cap one editor's share" and it does not reach |
| anything capping posts per clip | **DOES NOT EXIST** | grep finds no such concept anywhere |

> **SO: THE CAMPAIGN BUDGET CAPS THE TOTAL AND NOTHING CAPS THE CONCENTRATION OR THE SPEED.** Whether
> that is intended is question 3 in PART 8. The three shapes a cap could take (a posts-per-clip limit,
> a per-editor share-of-budget cap modelled on Y2, or neither) are laid out there, unanswered.

### 1.7 Every figure in this part, gross and cash, in one table

$100.00 gross clip, both earners standard and unreferred, no express, no trainer, no bonuses:

| party | gross | deduction | **cash** |
|---|---|---|---|
| editor | $45.00 | 9% fee = $4.05 | **$40.95** |
| poster | $45.00 | 9% fee = $4.05 | **$40.95** |
| owner, platform leg | $10.00 | none | **$10.00** |
| owner, the two payout fees | | | **$8.10** |
| **owner total** | | | **$18.10** |
| **sum** | | | **$100.00** |

Same clip, both earners referred: fees 4 percent, referrers take 5 percent of net.
Editor cash **$43.20**, poster cash **$43.20**, referrers **$4.32**, owner **$9.28**. Sum **$100.00**.

Same clip, editor 10 percent bonus and poster 5 percent bonus: the campaign disburses **$106.75**, the
editor's gross is $49.50, the poster's $47.25, the owner's leg stays $10.00.

---

## PART 2 — THE DATA MODEL, WHICH IS STRUCTURALLY DIFFERENT

### 2.1 The shape difference, stated before the entities

**The existing marketplace is ONE SUBMISSION to ONE SLOT to ONE POST.** A creator sends a Drive link to
a specific poster's listing, that poster approves or rejects it, and that poster posts it. The
submission is addressed to a person from the moment it is made, and its capacity is a daily slot count
on that person's listing (`MarketplacePosterListing.dailySlotCount`, `schema.prisma:2765`).

**This is ONE CLIP to MANY POSTS, and it is addressed to nobody.** The editor submits to the OWNER, not
to a poster. Once approved it becomes a catalogue item that any number of posters may draw from. **There
is no entity in the existing schema that means "an approved thing many people may take".** That is the
gap, and it is the one genuinely new model.

### 2.2 The four entities

**1. `MarketplaceV2Clip` — the editor's submission, which becomes the approved catalogue clip.**
One row, two lifecycle halves. It is the submission while PENDING and the catalogue item once APPROVED.

| field | why |
|---|---|
| `id`, `editorId` (User), `campaignId` (Campaign) | who made it, what it is for |
| `driveUrl` (Text), `driveFileId`, `videoHash` | the link the editor pasted, the canonical file id from `extractDriveFileId` (`video-hash.ts:60-74`), and the hash for the OWNER-side "this editor sent the same file twice" check only. **Never read by any poster path** |
| `title`, `description` | what the poster reads on the card |
| `thumbnailUrl` (nullable), `thumbnailSource`, `thumbnailFailedAt`, `thumbnailFailedReason` | PART 5. A failure is recorded as a failure, never as a fact about the video (BL-874) |
| `status` PENDING / APPROVED / REJECTED / WITHDRAWN / RETIRED | RETIRED is the owner pulling an approved clip out of the catalogue without touching money already earned |
| `approvedAt`, `approvedById`, `rejectedAt`, `rejectionReason`, `improvementNote` | the owner's words, shown verbatim to the editor |
| `postCount` (Int, default 0) | a denormalised counter, reconcilable from `MarketplaceV2Post`, never authoritative for money |
| `createdAt`, `updatedAt` | |

Indexes: `[campaignId, status]`, `[editorId, status]`, `[status, approvedAt DESC]`.

**2. `MarketplaceV2Post` — one poster's post of one approved clip.**

| field | why |
|---|---|
| `id`, `v2ClipId`, `posterId`, `clipAccountId`, `platform` | who posted it, from which connected account, where |
| `clipId` **@unique** (FK `Clip`) | the earning clip this post created. One post, one clip, enforced by the database |
| `postUrl`, `normalizedUrl`, `postedAt` | the live URL the poster pasted, normalised by the existing `normalizeClipUrlForMatch` (`sanitize-url.ts:66-76`) |

Unique constraints: **`clipId` unique** always. **A second unique on `[v2ClipId, clipAccountId]` is the
implementation of open question 11** (may a poster post the same clip to several of his own accounts). If
the answer is no, that index is the enforcement; if yes, it is omitted and only `clipId` stands. **Do not
add `[v2ClipId, posterId]`**: that would forbid multi-account posting by construction and pre-empt his
decision. BL-845 had to apply a missing unique index by hand after BL-841 found it declared and never
created; **whichever index is chosen here must be applied with `CREATE UNIQUE INDEX CONCURRENTLY` as its
own single statement and verified in `pg_indexes`, because Prisma's `@@unique` enforces nothing at
runtime** (BL-841 item 1, BL-845 section 1).

**3. The earning `Clip` — an ordinary row, and deliberately ordinary.**
`userId` is the **POSTER**. `earnings` / `baseEarnings` / `bonusAmount` hold the **POSTER'S 45 percent**,
written only through `writeClipEarnings`. This is the same choice the existing marketplace made, where
`Clip.earnings` holds the poster's 30 percent (BL-841, PART 2). Making the poster the clip's user is what
lets every existing machine work untouched: the tracking ladder, the review queue, the payout gate, the
balance derivation, the streak, the strike-free rejection counters.

**Two fields decide whether this design is safe, and they are the whole of the isolation story:**

* **a NEW nullable `marketplaceV2PostId`**, never `marketplaceSubmissionId` (`schema.prisma:1083`),
  which belongs to the existing marketplace and is read by its cascades
* **`isMarketplaceClip` MUST STAY `false`** (`schema.prisma:1084`). **This is the single most dangerous
  line in the build.** Setting it true makes every existing branch fire and apply 60 / 30 / 10 to a v2
  clip: `isCpmSplit = !isMarketplaceClip && …` (`tracking.ts:2047`, `clips/[id]/review/route.ts:520`),
  the two 60/30/10 writers (`tracking.ts:2099`, `review/route.ts:526`), and the marketplace cascades.
  **A v2 clip that carries that flag is silently paid on the wrong split.**

Leaving it false has a consequence that must be handled on purpose rather than by accident: the clip
then falls into the ordinary `isCpmSplit` branch and **an `AgencyEarning` row is written**, which is the
owner's ordinary cut. **That is exactly the replaces-versus-adds choice from PART 1.3, expressed as one
boolean.** Whichever the owner picks, the build must write his answer down beside that branch.

**4. `MarketplaceV2EditorEarning` and `MarketplaceV2PlatformEarning` — the other two legs.**
Field-for-field mirrors of `MarketplaceCreatorEarning` (`schema.prisma:3181-3205`) and
`MarketplacePlatformEarning` (`schema.prisma:3206-3227`): `clipId` @unique, party id, `campaignId`,
`amount`, `baseAmount`, `bonusPercent`, `bonusAmount`, `savedAmount`, `views`, timestamps.

**Why mirrors and not reuse, which is the sharpest reuse decision in the design.** Writing v2 rows into
`MarketplaceCreatorEarning` would put them inside every query that already reads it: the spend aggregate,
`effectivePaidOut` (`balance.ts:234-258`), the withdrawal gate (`payouts/route.ts:852`), and **the
existing marketplace's cascades** (`marketplace-cascades.ts`), which delete and rewrite those rows on
submission state changes that a v2 clip will never have. Half of that is what we want and half is
catastrophic. **New tables make the isolation total and the participation explicit: each aggregate that
must see v2 money is extended by hand, one at a time, and nothing else can reach it.** The four that
must be extended are named in PART 7.

### 2.3 How they relate

```
MarketplaceV2Clip (editor, campaign, APPROVED)
      |
      +--< MarketplaceV2Post (poster A) --1:1--> Clip (userId = poster A, earnings = 45%)
      |                                            |--1:1--> MarketplaceV2EditorEarning (editorId)
      |                                            \--1:1--> MarketplaceV2PlatformEarning
      +--< MarketplaceV2Post (poster B) --1:1--> Clip (userId = poster B, earnings = 45%)
      |                                            |--1:1--> MarketplaceV2EditorEarning (editorId)
      |                                            \--1:1--> MarketplaceV2PlatformEarning
      +--< ... fifty more
```

One editor row, N post rows, N clips, N editor-earning rows all keyed to the same person, N platform
rows. **The editor's total is a SUM over N rows, never a single figure, and never stored on the
`MarketplaceV2Clip`.** A stored total is a second source of truth and BL-539 measured what a second
source of truth costs: a stamp-versus-share mismatch at $933.94.

### 2.4 What carries over unchanged, what carries over modified, what must be new

**UNCHANGED, reused as it stands:**

| thing | `file:line` |
|---|---|
| `writeClipEarnings`, the only allowed writer of the four invariant fields | `src/lib/clip-earnings-writer.ts` |
| the L1 budget hard lock and the BL-167 pool clamp inside it | `clip-earnings-writer.ts:199-257`, `:311-382` |
| `normalizeClipUrlForMatch` | `src/lib/sanitize-url.ts:66-76` |
| `sanitizeClipUrl` at the submit entry points | `src/lib/sanitize-url.ts` |
| `extractDriveFileId` and `normalizeForHashing` (BL-868's Drive fix) | `src/lib/video-hash.ts:60-74`, `:76-87` |
| the tracking ladder, the :00 batch, `checkIntervalMin`, the cadence rules | `src/lib/tracking.ts` |
| the balance derivation and BL-824's paid-is-final bound | `src/lib/balance.ts:234-258` |
| the payout request, review and fee machinery | `payouts/route.ts`, `payout-calc.ts` |
| `createNotification` and the notification model | `src/lib/notifications.ts:528-636`, `schema.prisma:850-870` |
| the ban check contract, `checkBanStatus` on every route | every route |
| the design components: `MpPageShell`, `MpKpiStrip`, `MpEmptyState`, `MpBanner`, `MpFilterPills`, `PlatformPill`, `PlatformSquircle`, the Avatar fallback chain | `src/components/marketplace/*` |
| the dual-name render the owner asked for. **IT ALREADY EXISTS** | `src/app/(app)/admin/clips/page.tsx:2056-2074` renders "Posted by" and "Created by", both links to `/admin/users/[id]` |

**MODIFIED, a variant of something that exists:**

| thing | `file:line` | the change |
|---|---|---|
| `calculateMarketplaceEarnings` | `src/lib/earnings-calc.ts:629-691` | a v2 twin at 45/45/10 with the platform leg as the residual. **A twin, not a parameterised rewrite**: the existing function is called from the two live writers and must not change shape |
| the three share constants | `earnings-calc.ts:584-586` | three new constants beside them, one declaration each |
| `MpStatusBadge` | `src/components/marketplace/MpStatusBadge.tsx:70-72` | new state words. Its five statuses do not match v2's |
| `MpBrowseCard` | `src/components/marketplace/MpBrowseCard.tsx:84-86` | a v2 card. Same glass-card wrapper, different contents and a per-card state marker |
| `MpSubmissionRow` | `src/components/marketplace/MpSubmissionRow.tsx` | a v2 row for the editor's own list |
| the campaign create and edit form | `src/app/(app)/admin/campaigns/page.tsx:65-109` | one new field, the campaign type (PART 3) |
| `getCampaignBudgetStatus` spend aggregate | `src/lib/balance.ts:487-497` | **two new terms. PART 7 risk 1** |
| the admin clips list | `admin/clips/page.tsx:2056-2074` | extend the existing dual-name branch to a v2 clip |

**NEW, with no existing counterpart:**

1. The four models in 2.2.
2. The editor submit route, the owner approve and reject routes, the poster post route, the browse route,
   the skip and unskip routes.
3. The v2 earnings writer, which must call `writeClipEarnings` for the poster leg and write the other two
   legs in the same transaction.
4. The thumbnail path (PART 5).
5. The catalogue itself. **There is no "many people may take this" concept anywhere in the codebase**,
   and grep finds no skip, hide or dismiss affordance on any list in the product
   (the closest is a dismissible Discord banner, `src/components/marketplace/DiscordConnectBanner.tsx`).

### 2.5 PROOF THE EXISTING MARKETPLACE IS UNAFFECTED

**What the two systems SHARE**, and every one of these is shared by the existing marketplace with the
ordinary clip flow already, so sharing them adds no new coupling:

`Clip`, `User`, `Campaign`, `ClipAccount`, `writeClipEarnings`, `tracking.ts`, `balance.ts`, the payout
tables and routes, `Notification`, `AuditLog`, the design components, the ban check.

**What the two systems DO NOT SHARE. This is the list that makes the claim provable:**

* **No v2 row is ever written into any `Marketplace*` table.** Not `MarketplacePosterListing`, not
  `MarketplaceSubmission`, not `MarketplaceClipPost`, not `MarketplaceCreatorEarning`, not
  `MarketplacePlatformEarning`, not `MarketplaceVideoHash`, not `MarketplaceStrike`, not the chat,
  ratings or favourites tables.
* **`isMarketplaceClip` stays `false` on every v2 clip**, so every branch keyed on it
  (`tracking.ts:2047`, `review/route.ts:520`, `:526`, `tracking.ts:2099`, the cascades) sees nothing new.
* **No route under `/api/marketplace/**` is called by any v2 path**, and no v2 route is placed under that
  tree. A separate tree keeps the 326 4xx returns BL-870 counted under `/api/marketplace/` unchanged.
* **`MarketplaceVideoHash` is not written**, so its global `@unique` on `hash` (`schema.prisma:3159`)
  cannot collide a v2 submission against a v1 one, in either direction.
* The existing marketplace's own defects and fixes (BL-845's index, BL-847's Instagram path, BL-849's
  floor, BL-868's Drive hash, BL-871's clamp) are untouched, because none of that code is called.

**THE ONE REAL COUPLING, NAMED RATHER THAN HIDDEN: the campaign budget.** If a campaign ever carries both
marketplaces at once, both draw on one `campaign.budget` and one `spent` aggregate, and one can pause the
other. That is inherent to a shared budget and it is not a defect, but it is a fact the owner should know
before he enables both on one campaign. **It is also an argument for the campaign type in PART 3 being
the thing that decides which marketplace a campaign carries.**

### 2.6 THE DUPLICATE RULE, AND THE FINDING THAT CHANGES THE JOB

The brief says the duplicate check must be bypassed for v2 without weakening it elsewhere.
**Measured, it does not need bypassing at all, because it never fires.**

**Every duplicate gate in the product, counted and located:**

| # | gate | `file:line` | keyed on | scope |
|---|---|---|---|---|
| 1 | clipper submit, campaign gate | `src/lib/clipper-submit-core.ts:636-641` | `normalizedUrl` | `campaignId` + status in PENDING/APPROVED + not deleted |
| 2 | clipper submit, cross-campaign gate | `clipper-submit-core.ts:636-641` | `normalizedUrl` | `userId` across campaigns |
| 3 | owner submit | `src/lib/owner-submit-core.ts:144-156` | `normalizedUrl` | `campaignId` |
| 4 | marketplace submission, exact link | `src/app/api/marketplace/submissions/route.ts:411-431` | exact `driveUrl` | `creatorId` |
| 5 | marketplace submission, content hash (BL-868) | `submissions/route.ts:517-544` | `videoHash` | `creatorId`, scoped per campaign or site-wide by `campaign.allowContentReuse` (`schema.prisma:781`) |
| 6 | marketplace post | `src/app/api/marketplace/submissions/[id]/post/route.ts:914-952` | `normalizedUrl` | `campaignId` |
| DB | partial unique index, the backstop | `schema.prisma:1154-1163`, applied by `scripts/migrations/BL-239-CLIP-NORM-UNIQUE.sql` | `(campaignId, normalizedUrl)` | `WHERE isDeleted=false AND status IN ('PENDING','APPROVED')` |
| DB | full unique | `schema.prisma:1153` | `(clipUrl, campaignId)` | all rows |
| DB | global unique | `schema.prisma:3159` | `MarketplaceVideoHash.hash` | platform-wide |

> **THE FINDING: FIFTY POSTERS POSTING ONE VIDEO PRODUCE FIFTY DIFFERENT LIVE URLs.** Every gate above
> that could block them is keyed on `normalizedUrl`, which is derived from the POSTED URL, and each
> poster's own TikTok, Reels or Shorts post has its own. **Gates 1, 2, 3 and 6 and both `Clip`-level
> database indexes pass naturally, fifty times out of fifty, with no flag, no branch and no exception.**
> The owner's fear is aimed at a collision that does not occur.

**The two gates that COULD bite, and what to do about each:**

* **Gate 5, the content hash, is scoped to `creatorId`.** In v2 the editor submits once, so it cannot
  fire for a poster. It would fire only if the SAME editor submitted the same Drive file twice, which is
  a check worth keeping. **Keep it, scoped to the v2 table and the v2 editor, on the v2 row's own
  `videoHash` column.** Do not write `MarketplaceVideoHash`.
* **`MarketplaceVideoHash.hash` is globally unique.** If v2 wrote into it, the second editor anywhere to
  submit a file already recorded by the existing marketplace would be refused, and BL-868 showed exactly
  how painful a false duplicate is: *"An honest second submission was refused as a duplicate. This is the
  worse of the two, because it blocks real work and looks like a false accusation."* **v2 stores its
  hash on its own row with its own index and never touches that table.**

**The two cases where a gate SHOULD fire, and does, correctly:**

* One poster pasting ANOTHER poster's live URL. Gate 6's twin in the v2 post path refuses it, campaign
  scoped, and that is a protection worth having.
* One poster posting the same v2 clip twice to the SAME account. Same live URL, refused by
  `uq_clip_norm_open_per_campaign`. Correct.

> **SO THE SMALLEST CHANGE IS NO CHANGE.** v2 simply does not route through
> `/api/marketplace/submissions` (which carries gates 4 and 5) and does not write
> `MarketplaceVideoHash`. **Nothing is weakened for the existing marketplace, nothing is weakened for
> normal clips, and no bypass flag exists to be set wrongly later.** A subagent proposed three schemes
> involving new `allowContentReuseV2` flags and version branching; **all three are unnecessary and each
> would have added a switch that could be flipped the wrong way. That finding is reconciled here, not
> averaged.**

---

## PART 3 — THE THREE CAMPAIGN TYPES, AND THE THEFT PROBLEM BETWEEN THEM

### 3.1 What exists today, measured

**No field on `Campaign` expresses a type.** The full model is `schema.prisma:596-825` and every field was
enumerated; the three that look like a type are not one:

* `typeLabel` (`schema.prisma:701`) is a cosmetic card label ("Song", "App"), and its own comment says it
  is *"DISPLAY ONLY... read by no money, earnings, payout, eligibility or campaign-status path."*
* `pricingModel` (`:602`) decides how money is computed for a clip that already exists, not who may make
  one.
* `monetizationType` (`:603`) is marked "Legacy field" in the schema itself.

**Marketplace participation is expressed by the EXISTENCE OF A LISTING ROW**, not by a campaign flag: a
campaign becomes marketplace-available when somebody POSTs `/api/marketplace/listings` and a
`MarketplacePosterListing` pointing at it is created. Visibility is a GLOBAL environment flag,
`NEXT_PUBLIC_MARKETPLACE_ENABLED` (`src/lib/marketplace-flag.ts:31`), never per campaign.

> **SO EVERY CAMPAIGN ON THE PLATFORM IS ALREADY, STRUCTURALLY, AN UNRESTRICTED "BOTH": nothing stops a
> clipper submitting a normal clip to a campaign that also carries marketplace listings.** That is the
> confusion vector the brief names, and it is already live, just without an editor-and-poster split to
> make it profitable.

**And a clipper currently sees NOTHING that tells him which flow he is in.** The campaign detail page,
`src/app/(app)/campaigns/[id]/page.tsx`, contains **zero** occurrences of the word "marketplace" across
its 1,065 lines. Its only call to action is "Submit a Clip" (`:959`, `:1057`), gated on
`status === "ACTIVE"` and a connected account (`:954-966`). The marketplace lives on a structurally
separate page tree under `/marketplace` and nothing links the two.

### 3.2 How the type should be expressed

**Three options, and only one of them cannot express a nonsensical state.**

| option | consequence for the roughly 180 existing campaigns | can express an invalid state |
|---|---|---|
| **A. one enum, `campaignType NORMAL / MARKETPLACE_ONLY / BOTH`, NOT NULL DEFAULT `NORMAL`** | **every existing campaign is `NORMAL` on the day the column lands, with no backfill script and no NULL to fall through an unhandled branch.** `ALTER TABLE ... ADD COLUMN ... DEFAULT 'NORMAL' NOT NULL` via `scripts/run-schema-sql.js`, never `prisma migrate` | **no** |
| B. two booleans, `allowNormalClips` / `allowMarketplaceV2Clips` | needs a backfill decision per campaign, and every read site is an `if`/`if` pair that can drift apart | **yes**: `false / false` is a campaign nobody may submit to |
| C. derived from whether v2 clips exist | not settable in advance, so an owner cannot launch a MARKETPLACE ONLY campaign before its first clip, and it silently flips the moment one test row is created | n/a, and it is not auditable |

**RECOMMENDATION: option A**, and this reconciles a subagent finding rather than repeating it. That
subagent recommended A but attached a one-time `UPDATE campaigns SET campaignType='BOTH' WHERE id IN
(SELECT campaignId FROM marketplace_poster_listings)` and flagged the row count as an unanswered
question. **That backfill is not needed and should not be run.** The new field governs **normal versus v2
only**. The EXISTING marketplace stays governed by its listing rows exactly as it is today, which is the
whole point of PART 2.5. A campaign that carries a v1 listing and a `NORMAL` type keeps behaving in every
respect exactly as it does now. **No backfill, no count, no risk, and one fewer open question.**

### 3.3 Who may do what, per type

| action | NORMAL | MARKETPLACE ONLY | BOTH |
|---|---|---|---|
| a clipper submits his own clip | **yes**, exactly as today | **no** | **yes** |
| an editor submits a clip for approval | no | **yes** | **yes** |
| a poster posts an approved v2 clip | no | **yes** | **yes** |
| an editor posts a v2 clip that is not his own | no | **open question 6** | **open question 6** |
| an editor posts HIS OWN v2 clip and takes both cuts | no | **open question 4** | **open question 4** |
| the existing v1 marketplace, if the campaign has listings | unchanged | unchanged | unchanged |

**The last row is the one that makes the design safe. The type field never touches the existing
marketplace.**

### 3.4 MARKETPLACE ONLY: what is forbidden, and what each person sees

**Exactly one thing is forbidden: submitting a clip you made yourself, through the normal flow.**

**Where the refusal goes: ONE place, not two.** `src/app/api/clips/route.ts:1197` and
`src/app/api/clips/batch/route.ts:194` both delegate to `processClipperSubmitLink`
(`src/lib/clipper-submit-core.ts`). **The check belongs inside that core**, beside the existing
campaign-status refusals (the `PAST` check at `:371` and `PAUSED` at `:372`), which also means
`campaignType` must be added to the `select` at `:360-367` for the check to see it. Putting it in the two
routes instead is how BL-824 described the failure it was fixing: *"A patch at either site would have
left the other wrong."*

**Verbatim refusal copy**, written for a fifteen year old, explaining the rule and never accusing, per
BL-518 and BL-521 (`BACKLOG.md:18984`, `:19000`):

> **You cannot upload your own clip to this campaign.**
> This one works through the marketplace. Go to the marketplace, pick a clip an editor already made,
> post it to your account, and paste the link there. You earn 45 percent of what your post makes.

**The same words serve an editor who tries the wrong door**, and that is deliberate rather than lazy:
`clipper-submit-core.ts` has no concept of an editor or a poster and cannot tell the two apart, and the
copy never needs to, because it points at the right door instead of judging who knocked.

**The owner override path is a separate decision.** `clips/owner-submit/route.ts:22` delegates to
`validateOwnerSubmitContext` (`src/lib/owner-submit-core.ts:65-115`), which checks only AUTO-paused
(`:79-82`) and test-campaign-in-override-mode (`:83-85`) and has **no campaign-status gate at all**,
unlike the clipper path. Whether MARKETPLACE ONLY should reach it is **open question 23**; this report's
view is that it should not, because the owner blocking himself helps nobody.

### 3.5 BOTH: how a clip's type is decided, and the confusion that IS the theft vector

**The type is decided BY WHICH BUTTON HE PRESSED, and by nothing else.** A normal clip is created by
`processClipperSubmitLink` (`clipper-submit-core.ts:653-694`), which never sets any marketplace field. A
v2 clip is created by the v2 post route. **No property of the URL, the account or the video decides it.**

**So yes, a clipper can be genuinely confused, and the interface today guarantees it**: the campaign page
shows one button, "Submit a Clip", and says nothing about a second way to earn on the same campaign.

**The interface that makes the choice unmissable.** On a BOTH campaign, two distinct cards, each stating
what it pays and what it needs, side by side above any form:

> **Make your own clip**
> You film or edit it yourself and post it to your account. You keep the full clipper rate.
>
> **Post a clip someone else made**
> An editor already made it. You post it to your account and paste the link. You earn 45 percent and the
> editor earns 45 percent.

**The point of no return is clip creation, and that is not a new rule.** `processClipperSubmitLink`
stamps `cpmAtSubmissionDecimal` and `ownerCpmAtSubmissionDecimal` inside the same transaction that
creates the row (`clipper-submit-core.ts:643-658`, F-CPM-FREEZE). A clip's economic identity is already
frozen at creation, so its flow identity freezes there too. **Retroactively flipping a clip between the
two flows means unwinding and restamping money fields, which is the conversion action in 3.10 and is why
that action is designed at payout length rather than as a toggle.**

### 3.6 What the campaign card and detail page must show

**NORMAL:** unchanged, no new copy.

**MARKETPLACE ONLY:**
* card badge, in the existing `TypeBadge` slot (`CampaignsRedesign.tsx:54-75`, placed at `:189`):
  **"Marketplace only"**
* detail page, above any button: **"This campaign only works through the marketplace. You cannot upload
  your own clip here."**

**BOTH:**
* card badge: **"Two ways to earn"**, deliberately worded so it can never be misread as the other badge
* detail page, above the two cards in 3.5: **"You can make your own clip, or post a clip someone else
  made. Pick one below."**

**Every surface that lists campaigns and needs a badge or filter:**

| surface | `file:line` |
|---|---|
| the clipper campaign grid (the only card every clipper actually sees) | `src/app/(app)/campaigns/CampaignsRedesign.tsx:189`, filter at `:511-522` |
| the campaign detail page | `src/app/(app)/campaigns/[id]/page.tsx:959`, `:1057` |
| the owner's campaign management list | `src/app/(app)/admin/campaigns/page.tsx`, exact row-render line **not determined**, the file is 2,436 lines and was not read in full |
| `src/app/(app)/community/page.tsx` and `src/app/(app)/client/campaigns/page.tsx` | matched a campaign-listing grep; **whether either audience needs the badge was not determined** |

**Note:** the existing `TypeBadge` slot is currently occupied by the cosmetic `typeLabel`, and the
existing "Song / App / All" filter (`CampaignsRedesign.tsx:511-522`) filters on that label, not on a
mode. **The two badges must coexist or be combined, and the type filter is a second control.**

### 3.7 What happens when the type changes while clips are in flight

The enum lives on `Campaign` and touches no `Clip` row, so nothing in flight changes by itself.

* **NORMAL to MARKETPLACE ONLY** with normal clips already tracking: those clips keep tracking and keep
  earning; only NEW submissions are refused.
* **MARKETPLACE ONLY to NORMAL** with approved v2 clips in the catalogue: the symmetric question, and the
  sharper one, because an editor's approved clip may have posters mid-flow on it.
* **Either to BOTH** is safe by construction: it only adds an entry point.
* **BOTH to either single type** reduces to one of the first two.

**Whether a type change should be blocked outright while work is in flight, or always allowed with
in-flight work grandfathered, is open question 14.** This report's view is that grandfathering is the
only option that touches no money path, but the choice is his.

---

### 3.8 THE THEFT PROBLEM, AND WHY THE PLATFORM'S ONE EXISTING DETECTOR DOES NOT REACH IT

A poster takes an editor's approved clip, posts it from his own account, and submits it as an ordinary
NORMAL clip, keeping 100 percent instead of 45.

**What the platform can see: nothing, and that is settled rather than argued.** BL-871 established it:
`Clip` carries `marketplaceSubmissionId` and `isMarketplaceClip` and both are written **only** by the
marketplace post path; the ordinary submit route contains zero marketplace references, and
`clips/owner-submit/route.ts` has a `grep -c` of **0**. **The stolen clip is created with no link to
anything.**

**And no hash will change that.** BL-871 priced four content-matching options and recommended against all
four. The reasons are structural, not budgetary: TikTok and Instagram transcode on upload so not one byte
survives, and a cryptographic hash of a transcoded file is not "close", it is an unrelated number; and
perceptual or audio fingerprinting fails in the opposite direction, because **every clipper on this
platform clips the same source footage and uses the same trending sound on purpose, so two honest
clippers produce near-identical fingerprints**. BL-771 measured the best computable signal on this
platform at **20.2 percent precision against a requirement above 99.2 percent**. **Do not build a
detector. The owner has already paid for that answer twice.**

> **AND HERE IS THE PART THAT IS NEW TO THIS DESIGN, WHICH NO PRIOR ROUND COULD HAVE SEEN.**
> BL-871's escape hatch was a reframe: *"the theft case and the poster who never posts are the same
> event"*, because in the existing marketplace a submission is ADDRESSED to one poster, so "accepted and
> never posted" is a single indexed query and is 100 percent accurate about the signature.
> **THAT REFRAME DOES NOT CARRY OVER.** In v2 nobody accepts anything. Every approved clip is visible to
> every poster and posting is entirely voluntary, so "did not post" is the normal case for almost every
> poster and every clip. **There is no footprint. The signature BL-871 relied on does not exist here,
> and a build round that assumes it does will build a list of innocent people.**

**So detection is human, with no mechanical assistance, and the honest levers are two:**

1. **The editor is the detector.** He knows his own work on sight, and he has the strongest possible
   motive to look. Give him a "this is my clip" report on any normal clip he can see, routed to the owner
   as EVIDENCE, never as a verdict. This is the cheapest real signal on the platform and it costs one
   button and one queue.
2. **The owner's eye**, supported by putting the two things side by side. PART 6 specifies that surface.

**Both are evidence for a human. Neither may auto-act.** BL-771's rule applies unchanged: *"Nothing may
auto-reject and no clipper may see machine suspicion."*

### 3.9 THE STRIKE SYSTEM: HUMAN ISSUED ONLY, AND THE HISTORY THAT DEMANDS IT

**The history, stated because it is the whole argument.** Three rounds each worked the strike path and
each found the previous one wrong:

* **BL-845** found that a poster could be struck because **our own fetch failed**, and added
  `verifyFailedAt` and `verifyFailedReason` so a failure we caused writes no strike.
* **BL-847** found a bug inside BL-845's own fix: the no-strike branch was entered on
  `activeBan || couldNotConfirm` but the `continue` that ended the iteration sat inside a branch testing
  `activeBan` **alone**. **For the exact case BL-845 was written for, execution fell straight through**,
  wrote an audit row saying `MARKETPLACE_STRIKE_ISSUED` for a strike that was never created, and told the
  poster *"A strike has been issued"*. The ban count stayed honest and **the message lied.**
* **BL-849** found the NEW entrance **BL-847 had opened with its own settle gate**: that gate refused the
  POSTER because the LISTING was full, and twenty four hours later the sweep struck him for a deadline
  that very line had stopped him meeting.
* **BL-871** corrected the attribution the brief inherited: it was BL-845, not BL-849, that found the
  original defect, and it counted the real strike-creation sites at **five** (`grep -c` = 5), of which
  **one is human** (`admin/users/[id]/marketplace-ban/route.ts:183`, `OWNER_ISSUED`), **two are automatic
  and live** (`excessive-rejections.ts:207`, `marketplace-timers.ts:252`) and **two are dead**, gated off
  by `ISSUE_CREATOR_POST_DEADLINE_STRIKES = false` (`expire-deadlines/route.ts:74`, checked at `:269`).

**Six, then five, then a seventh, with the seventh opened by the round that was closing them.**

> ### THE SPECIFICATION, AND EVERY LINE OF IT IS A REACTION TO THAT HISTORY
>
> **1. HUMAN ISSUED ONLY. There is exactly one creation site and it is an OWNER route.** No cron may
> create a v2 strike. No fetch result may create one. No count may create one. No threshold may create
> one. **`grep -c` for the v2 strike create must return 1, forever, and that number belongs in a test.**
>
> **2. It is a NEW model, `MarketplaceV2Strike`, and it does NOT reuse `MarketplaceStrike`.** Two
> reasons, both hard. First, `isUserMarketplaceBanned` (`src/lib/marketplace-ban.ts:107-152`) derives a
> MARKETPLACE ban by MAX over live `MarketplaceStrike` rows, and the owner's penalty here is a ban from
> **normal posting**, which is the opposite surface. Second, reusing the table would let
> `excessive-rejections.ts:207` and `marketplace-timers.ts:252`, both automatic, contribute rows to a
> count that must be human-only. **A shared table is a shared automatic entrance.**
>
> **3. The ban is derived live from rows, never from a scalar.** BL-841 item 10 measured what a scalar
> costs: `User.clipperMarketplaceBannedUntil` is written by `expire-deadlines/route.ts:387` and **cleared
> by nothing**, so a ban from that source has no reversal path in the product at all. **v2 writes no ban
> scalar. The ban is `count of live strikes >= 3`, computed at read time.**
>
> **4. Expiry is derived at read time, not by a cron.** BL-841 measured that `decay-strikes` is
> registered at `railway-cron-scheduler.ts:81`, writes a heartbeat on completion, and has **zero rows in
> `cron_runs`**: it has never run, so **strikes have never decayed on this platform**. A design that
> depends on a cron that has never fired is a design that does not expire. **Derive it:
> `live = strikes WHERE revokedAt IS NULL AND createdAt > now() - window`.** The window length is the
> owner's, not this round's.
>
> **5. Evidence is required, and stored.** The route refuses without a free-text reason and at least one
> linked clip id. The row keeps `reason`, `evidenceClipIds`, `v2ClipId` (the editor's clip it is said to
> be), `issuedById`, `issuedAt`, and a denormalised copy of the campaign name and clip URL so the row
> survives deletion, exactly as `MarketplaceStrike` already does (`schema.prisma:3085-3131`).
>
> **6. Reversible, by one route, and it lifts on the next read.** `revokedAt`, `revokedById`,
> `revokeReason`. Because the ban is derived, revoking the row lifts the ban immediately with no scalar
> to remember. The existing dispute resolver proves the pattern works
> (`admin/marketplace/disputes/[id]/resolve`, verdicts `UPHELD | REMOVED | REDUCED`).
>
> **7. Where the ban is enforced: ONE chokepoint, not two call sites.** Normal submission reaches
> `processClipperSubmitLink` (`src/lib/clipper-submit-core.ts`) from **both**
> `src/app/api/clips/route.ts:1197` and `src/app/api/clips/batch/route.ts:194`. **The check goes inside
> the core, not in the two routes**, which is BL-824's own lesson: *"A patch at either site would have
> left the other wrong."* `clips/owner-submit/route.ts:22` is deliberately NOT gated: an owner override
> is the owner acting, and blocking himself helps nobody.
>
> **8. The ban is from NORMAL posting only.** A struck poster may still post marketplace clips, still
> earns on clips already live, and still withdraws. **Money already earned is never touched by a strike.**

**What the clipper sees at each stage.** Written for a fifteen year old, no blame, no machine suspicion,
no dashes, no emojis. BL-518 and BL-521 are the authority (`BACKLOG.md:18984`, `:19000`): a clipper must
never see fraud hints, a FLAGGED status or anything that reads as an accusation, and a failure must never
be reported as an accusation.

* **Strike 1, and it must warn explicitly.**
  Title: `First warning about marketplace clips`
  Body: `A clip you posted was made by another editor and submitted as your own work. When you post
  someone else's marketplace clip, post it through the marketplace so the editor gets paid too. This is
  warning one of three. A second warning follows if it happens again, and a third stops you posting your
  own clips for seven days. Nothing has been taken from your earnings.`
* **Strike 2.**
  Title: `Second warning about marketplace clips`
  Body: `This is warning two of three. One more and you will not be able to post your own clips for seven
  days. Marketplace clips belong to the editor who made them, and you still earn 45 percent when you post
  them the right way. Nothing has been taken from your earnings.`
* **Strike 3.**
  Title: `You cannot post your own clips for seven days`
  Body: `This is warning three. From now until [date] you cannot submit your own clips. You can still post
  marketplace clips and you still earn on everything already live. Your earnings are untouched. If you
  think this is wrong, reply in Discord and the owner will look at it again.`
* **On revoke.**
  Title: `A warning was removed`
  Body: `The owner looked again and removed one of your warnings. Nothing was counted against you.`

**The refusal a banned poster sees at submit**, once, at the chokepoint:
`You cannot submit your own clips right now. This lifts on [date]. You can still post marketplace clips
and you still earn on everything already live.`

### 3.10 THE CONVERSION ACTION, WHICH IS A MONEY MOVEMENT BETWEEN TWO REAL PEOPLE

**What it is.** The owner takes a NORMAL clip, decides it is really an editor's work, and converts it
into a v2 clip attributed to that editor. The poster keeps the post and the views (he really did post it
from his own account), but the clip's SPLIT changes: from 100 percent of the clipper rate to 45 percent
of gross, with 45 percent created for the editor and 10 percent for the platform.

**It must be designed with payout-level care, and the three rules it collides with are all measured.**

**Rule 1, BL-824 paid-is-final.** *"Money already PAID OUT is final and can never be clawed back by a
later video deletion. If the clipper was ALREADY PAID for that work it stays theirs and must NOT offset
anything they earn afterwards."* Encoded as `effectivePaid(campaign) = min(paidGross, payableEarnings)`
(`balance.ts:234-258`).

**Rule 2, BL-849's write side.** BL-824 is a READ-side rule. Nothing stopped the stored row being
overwritten to zero after the creator had been paid for it, which destroys the RECORD rather than the
money, and a destroyed record is not harmless: the earner's own page reads $0.00 on a campaign he was
genuinely paid for, and the owner's two lifetime liability screens deliberately do not apply the bound
(`balance.ts:197-201`), so his books disagree with what he actually paid.

**Rule 3, BL-826's measurement of what breaking it costs.** 40 clips carrying $140.54 were multiplied
down to $25.65 against $78.54 already paid. Mark Paid then jammed at $0.00 against the
`payout_amount_positive` CHECK constraint: **five identical failures, permanent.**

> ### THE SPECIFICATION
>
> **A. The editor's leg is CREATED, and that half is easy and safe.** Nothing has ever been paid on it, so
> a new `MarketplaceV2EditorEarning` row is an ordinary creation with no floor to respect and no history
> to contradict. **This is the marketplace shape, not the trainer shape, and it is correct here:** the
> editor's 45 percent is not a third party's cut out of the poster's money, it is a second party's own
> earning created from the same gross. BL-841 drew that line for the existing marketplace and it holds.
>
> **B. The poster's leg is REDUCED, and every guard in the platform applies to that half.**
> * It is written **only** through `writeClipEarnings`. Never a direct `clip.update` on the four
>   invariant fields.
> * It is a DECREASE, so it must pass `src/lib/earnings-never-decrease.ts` with an **explicit,
>   audited `allowDecrease: true`**, not silently. BL-538 put that guard in committed code after BL-528
>   found it living only in an uncommitted script.
> * **It CLAMPS AT THE PAID FLOOR AND SAYS SO LOUDLY.** The poster's recorded earnings on that campaign
>   may never go below his `effectivePaid`. This is BL-866's shape verbatim: the owner's screen receives
>   `requestedRatio`, `effectiveRatio`, `clamped` and the floor itself, and shows all four. A silent
>   clamp is worse than either outcome, because the owner believes he re-split the clip and he did not.
> * A position already below its paid floor is **REFUSED, not deepened**, with every proposal stripped
>   from the response. Returning figures beside a refusal puts numbers on screen that look like a plan
>   and are not one.
>
> **C. One Serializable transaction, one audit row, a blast-radius preview, and an undo.** The preview
> shows the clips, the people and the dollars **before** acting and is **produced by the same code that
> then executes**, which is BL-538's undo-freeze pattern and the reason that round was safe.
>
> **D. It is OWNER only, and it is never automatic.** No cron converts anything. No detector converts
> anything. It is a button a human presses after looking at a video.

**WHAT HAPPENS TO MONEY ALREADY PAID TO THE THIEF. Stated plainly: NOTHING CAN RECOVER IT, and any
design that claims otherwise is breaking BL-824.** The clamp means the paid portion stays his, and it
must not offset anything he earns later. That leaves three honest shapes and **all three are the owner's
decision, not this round's** (question 12 in PART 8):

1. **Forward only.** The conversion re-splits only what has not been paid. The editor earns from the
   conversion forward. Cheapest, safest, and the editor is under-compensated for the paid window.
2. **The platform covers the gap.** The owner pays the editor the 45 percent of the already-paid portion
   out of his own 10 percent and his fee income. The editor is made whole, the poster keeps what he was
   paid, and the cost lands on the only party who chose to run the conversion.
3. **The clamp is the answer.** Whatever the floor frees goes to the editor and no more. Simplest to
   build, hardest to explain to the editor.

**RECOMMENDATION: BUILD BOTH, IN THIS ORDER, AND THE ORDER IS THE POINT.**

**Conversion first, strike second, and the strike only on repeats.** The reasoning:

* **Conversion fixes the money; a strike only punishes.** The editor's complaint is that he was not paid.
  A strike does not pay him. Conversion does, for everything not already withdrawn.
* **The first offence is often confusion, not theft.** Section 3.5 shows that on a BOTH campaign a
  clipper can genuinely not know which flow he is in, and **that confusion IS the theft vector even
  without bad intent.** Striking a confused person on the first event is how a platform loses honest
  clippers, and the first-strike copy above is written on the assumption that it is a warning rather
  than a verdict.
* **Conversion is self-limiting and strikes accumulate.** A conversion touches one clip. A strike
  reaches a seven day ban, and given the history in 3.9, penalties on this platform have a record of
  reaching people they were not aimed at.
* **The one thing conversion cannot do is deter.** A poster who is only ever re-split loses nothing by
  trying. That is the argument for the strike, and it is a real one.

**So: conversion as the standard remedy and available generally as the owner asked, the strike reserved
for a repeat after a conversion has already been explained to the person. Which of the two he actually
wants, and whether the strike needs a conversion first, is his call and is question 5 in PART 8.**

---

## PART 4 — THE POSTER'S EXPERIENCE

### 4.0 COLOUR CARRIES NOTHING HERE, AND EVERY STATE IS SAID IN WORDS

**Measured, and the brief's attribution is correct.** `reports/BL-864-clippershq-sent-to-admin-marker.md`
line 35: *"The two states, in words, because colour carries nothing here. All three text tokens are
`#ffffff` and emerald against red measures 1.44:1."* The same finding is recorded independently at
`BACKLOG.md:22268` under BL-827. A subagent believed the citation was wrong and it is not; both rounds
record it and BL-864 carries the measurement.

Confirmed again this round in source: `--text-primary`, `--text-secondary` and `--text-muted` are all
`#ffffff` (`src/app/globals.css:72-74`, with an explicit comment acknowledging it at `:95-99`). The
marketplace-scoped tokens do differ from one another (`--mp-text-primary` `#ededee`,
`--mp-text-secondary` `#a1a1a8`, `--mp-text-muted` `#909099`, `:113-120`), **but the existing status
system still carries meaning by hue alone**: `MpStatusBadge.tsx:50-82` and `MpStatusGlyph.tsx:23-38`
differ only by `--mp-warning` / `--mp-info` / `--mp-success` / `--mp-danger`, and `MpDeadline.tsx:78-90`
has three urgency levels distinguished by colour and nothing else.

> **SO: EVERY STATE IN THIS DESIGN CARRIES AN EXPLICIT WORD, ON SCREEN, ALWAYS. Colour is reinforcement
> and never the signal. Three of the existing marketplace components therefore cannot be reused as they
> stand, and that is said plainly in 4.6 rather than discovered in a build round.**

### 4.1 The three states

All three live on one element: a full-width status ribbon docked under the card thumbnail, above the
name. **Every card always shows exactly one ribbon.** There is no blank state, because a blank card reads
as less urgent than a labelled one and "not yet posted" must be the loudest thing on the screen.

Each state is told apart **three independent ways at once**: the words differ, the lucide icon differs,
and the fill treatment differs. The third channel is what makes it legible to someone who cannot separate
emerald from red at 1.44 to 1.

| state | the WORDS on screen | icon | treatment |
|---|---|---|---|
| **NOT YET POSTED** | **"Not posted yet. You can still earn 45 percent."** | `CircleDollarSign` | **solid accent fill**, full bleed, bold. The ONLY state with a solid fill, on purpose |
| **POSTED** | **"You posted this. It is live."** | `CheckCircle2` (already the POSTED symbol at `MpStatusGlyph.tsx:30-32`, so it stays learned) | `--mp-surface-2` with a 4px accent left border. No pulse, no animation. Past tense should not compete |
| **SKIPPED** | **"You skipped this. Tap to change your mind."** | `SkipForward` | outline only, 1px, the quietest of the three, **and the whole ribbon is a real button**, not a badge |

**Skip must never read as a dead end.** The words and the fact that it is tappable are what keep it
reversible in the interface, not only in the database.

**The accessibility shape, which is a requirement rather than a nicety:**
* the card is a native `<article>` (matching `MpBrowseCard.tsx:84`) named by `aria-labelledby` pointing at
  a real `<h3>`. **The campaign name renders as a plain `<p>` today (`MpBrowseCard.tsx:142`) and must
  become a heading**, so the card has an identity independent of its state.
* the state word sits in its own `<p id="v2-card-status-{id}">`, and `aria-describedby` is set on the
  `<article>` **and on every focusable control inside it**, because a description on an ancestor is not
  picked up when the child is focused.
* every action button carries `aria-label="{visible text}: {clip name}"`. Without it a screen reader's
  buttons list reads twenty identical "Post this clip" entries. **The existing "View details" link has
  exactly that defect today (`MpBrowseCard.tsx:175-180`).**
* on POSTED the primary control is NOT a disabled button. A disabled control drops out of the tab order
  with no explanation. It becomes a non-interactive `<span aria-hidden="true">` beside the status text,
  and the Skip button is not rendered at all rather than rendered disabled.
* posting removes the element holding focus, so focus moves programmatically to "View your post" and the
  live region announces.

### 4.2 Every button and empty state, verbatim

Simple words for a fifteen year old. No dashes, no emojis.

**Card actions:**
* not yet posted: **"Post this clip"**
* posted: **"View your post"**, secondary style, because there is nothing left to do
* skipped: **"Post it after all"**

**Clip detail screen:**
* **"Open in Google Drive"** (new tab)
* **"I posted it. Submit the link."**
* **"Skip this clip"**, secondary, always visible, never hidden
* **"Not now, I will decide later"**, which dismisses without recording a skip

**Submit the link:**
* label: **"Paste the link to your post"**
* placeholder: **"Paste your TikTok, Instagram or YouTube link here"**
* helper: **"This has to be the real link people can click, not a screenshot."**
* button: **"Submit my post"**
* success: **"Your post is in. You will start earning as it gets views."**
* bad link: **"That does not look like a real link. Copy it straight from the app."**
* network: **"Something went wrong sending this. Check your connection and try again."**

**Empty states**, built on `MpEmptyState.tsx:17-49`:
* nothing yet: **"No clips to post yet"** / *"Check back soon. New clips show up here as soon as the
  owner approves them."*
* all handled: **"You are all caught up"** / *"Every clip has a post or a skip on it. Come back later for
  new ones."*
* a filtered tab: **"Nothing here yet"** / *"Post a clip and it will show up in this tab."*
* **load failure, and it must be distinguishable from an empty list** (the existing browse client already
  gets this right at `browse-client.tsx:254-270`): **"Could not load your clips"** / *"Something went
  wrong. Try again."* / button **"Try again"**

**Live region wording**, one shared `<div role="status" aria-live="polite" aria-atomic="true">` for the
whole grid, mounted once outside the list and never one per card:
* **"Clip skipped."** / **"Clip unskipped. Ready to post."** / **"Could not skip this clip. Try again."**
/ **"Could not unskip this clip. Try again."**
All four `polite`, none `assertive`. Debounce around 400 to 500 milliseconds after the call resolves, and
clear the text before writing so an identical repeated string still registers as a change.

### 4.3 The posting flow, and every place he can lose his place

| # | step | where he can lose his place | how the interface holds it |
|---|---|---|---|
| 1 | opens the marketplace, sees the list defaulting to "Not posted" | none, this is the anchor | |
| 2 | taps a card, goes to the clip detail screen | a reload or a bookmark could dump him back to the grid | **the detail screen is a REAL URL**, `/marketplace/clips/[id]`, never a modal-only state. The existing product already does this for listings (`MpBrowseCard.tsx:176`) |
| 3 | taps "Open in Google Drive" and **LEAVES THE SITE** | **loss point 1** | the link opens in a **new tab**, `target="_blank" rel="noopener"`, never a same-tab navigation, so the ClippersHQ tab is still sitting there untouched. On that tap the server records that this clip is **in progress for him** |
| 4 | downloads in Drive, switches to TikTok or Instagram or YouTube to post | **loss point 2**, an operating-system app switch the web app cannot see | nothing to mitigate directly. The point of the step 3 write is that it does not matter which app he went through or for how long |
| 5 | comes back: a different device, an hour later, or his phone killed the tab | **loss points 3, 4 and 5** | all three get the same fix. **In-progress lives on the SERVER against his user id and the clip id, never in `localStorage`**, which would not survive a device change and which the platform's own guidance treats as unreliable. The grid then shows a **"Continue posting: [clip name]"** banner pinned above it, the detail URL re-renders in the ready-to-submit state on a cold load, and a desktop session shows the identical banner |
| 6 | submits the live URL | a bad paste, a duplicate | validated client-side in the shape already used at `post-clip-modal.tsx:49-56`, then server-side |

> **AND ONE HARD RULE ABOUT THAT IN-PROGRESS FLAG, BECAUSE THIS PLATFORM HAS A HISTORY.**
> The flag exists **only** to hold the poster's place. **It must never be evidence of anything.** It is
> exactly the shape a future round would be tempted to read as "he took it and never posted it", which
> is the signature BL-871 relied on in the existing marketplace and which PART 3.8 shows does not exist
> here. **A poster who opens a Drive link and changes his mind has done nothing wrong, and the record of
> him opening it must never reach a strike, a count, a queue or a screen that implies suspicion.** Given
> that three consecutive rounds each struck somebody the previous round meant to protect, this belongs in
> the column comment, not only in this report.

**ONE THING THAT COULD BREAK THIS FLOW ENTIRELY, AND IT IS AN OPEN QUESTION RATHER THAN A DESIGN
CHOICE.** The existing product requires a clip's live URL to reach the server within `MAX_CLIP_AGE_LABEL`
= **"30 minutes"** of the post going live (`src/lib/clip-config.ts:13-20`), and BL-841 measured that once
that window closes the same URL is refused **permanently**, by a different branch, even after everything
recovers. **A poster who leaves for Drive, downloads a 30MB file, posts it and comes back an hour later
would be refused with no warning anywhere in this flow.** If that rule applies to v2, the countdown must
be visible **before he leaves for Drive**, not only at submission. This is open question 24 and the
interface must be built ready to show a countdown either way.

### 4.4 What he sees about money

**Shown:**
* his own rate on this clip: **"You earn about $X.XX per 1,000 views"**, computed **server side** as the
  45 percent share already applied, never a raw CPM. This is the existing contract: `browse/route.ts:437`
  calls `computePayoutShape(rawCampaign, platforms, "creator")` and `:428-456` strips the raw campaign CPM
  fields before the response leaves, and `MpBrowseCard.tsx:155-165` renders only the pre-shared figure.
* what it means on a clip that has already earned for other posters: **nothing about their money, and
  everything about his own.** His 45 percent is of **his own post's views only**. A clip that has made
  another poster $400 makes him exactly $0 until his own post gets views, and the copy should say so
  plainly rather than leave it to be assumed: *"You earn 45 percent of what YOUR post makes. What other
  people's posts made does not change yours."*
* his own running totals, on an `MpKpiStrip` (`MpKpiStrip.tsx:20-30`).

**Never shown, and each of these has an existing enforcement site:**
* campaign budget or remaining spend. **This is the one leak BL-841 found in the existing marketplace**
  (item 7: `budgetWarning` with `remainingUsd` shipped to every viewer with no role gate,
  `listings/[id]/route.ts:388-400`, rendered at `TrustBadges.tsx:102-120`). **v2 must not repeat it.**
* the owner's 10 percent, or any figure it can be derived from. BL-841 item 6 measured that the existing
  marketplace's own marketing copy defeats its field protection by naming both halves on one screen
  (`apply-client.tsx:298-299`). **v2's copy says "you earn 45 percent" and must never also print the
  editor's 45, or one subtraction yields the 10.**
* the editor's earnings, any other poster's earnings, `ownerCpm`, `agencyFee`, `clientName`,
  `aiKnowledge`.

**Genuinely undecided and not answered here:** whether to show an aggregate such as "posted 6 times so
far". It is not one person's money, but it is another user's activity, and it changes the whole feel of
the surface from no-pressure to scarcity. **Open question 25.**

### 4.5 The ordering, and why

**Recommendation: a status tab bar defaulting to "Not posted", reusing `MpFilterPills`
(`MpFilterPills.tsx:28-77`), with tabs "Not posted (N)", "Posted (N)", "Skipped (N)" and "All". Within
the active tab, newest approved first.**

Against the owner's stated goal that a poster sees instantly what he has not yet posted:

* **newest first with no filter** loses it the moment the list has volume: unposted clips get buried
  under a growing column of posted ones and "instant" becomes "scroll and scan".
* **unposted-first sort in one flat list** is close, but it only reads as sorted if you trust the ribbon
  on every card, which is the colour problem at list level, and it still shows him rows with nothing left
  to do before he has finished the ones that matter.
* **a grouped layout with headers** solves instant but costs vertical space at 375px: he would scroll past
  every posted clip to check whether more unposted ones sit below, unless "Not posted" always renders
  first and fully expanded, which is the tabbed default with a softer boundary.
* **platform or campaign filters as the primary axis** do not address the goal at all. The question is
  "what have I not posted", not "what is on TikTok".

### 4.6 Mobile at 375px, concretely

Single column, matching the existing grid's own mobile-first breakpoints (`browse-client.tsx:305`, two
columns only at `sm`, three at `xl`). One card, top to bottom:

| element | size |
|---|---|
| thumbnail, `aspect-video` | roughly 343 x 193 px at 375 wide |
| **status ribbon**, full width, one line plus icon | roughly 36 to 40 px |
| clip name, `line-clamp-2` | roughly 40 px |
| platform pills, wrapped row | roughly 28 px |
| "You earn" line | roughly 24 px |
| primary button, full width | **48 px**, above the 44 px floor |
| **rough card height** | **420 to 450 px** |

That is taller than the existing `MpBrowseCard`, which has no ribbon, so **a single column is the only
sane layout at this width**; two columns would put a ribbon and a money line into a 160px card.

**Touch targets:** 44 x 44 CSS px minimum for "Post this clip" and Skip, which is well above the WCAG
2.5.8 floor of 24 x 24 and deliberately so, since these are adjacent actions with opposite consequences.
**Minimum 8px gap between them**, and prefer stacking over two small side-by-side buttons.

**Focus ring:** the global default (`globals.css:272-275`, `outline: 2px solid #2596be`) computes to
roughly **5.5:1** against `--bg-card` and passes, though it hardcodes the hex where `--color-accent`
already holds the identical value at `:4`. **The marketplace-scoped overrides FAIL and must not be
inherited by the new surface:** `.mp-focus-soft` (`:480-483`, 30 percent opacity) computes to roughly
**1.54:1** and the broad `.mp-section` / `.mp-glass-*` rule (`:494-501`, 35 percent opacity, 1px)
to roughly **1.69:1**, failing both the 3:1 contrast and the 2px thickness minimum. **Those two rules
currently govern every interactive element on the existing marketplace**, and they are the same failure
class as BL-864's 1.44 to 1. v2 defines `--mp-focus-ring: var(--color-accent)` and uses
`outline: 2px solid var(--mp-focus-ring); outline-offset: 2px;`.

**`data-no-swipe`:** the global swipe handler is at `src/components/layout/app-layout.tsx:646`. The grid,
the cards and the list do **not** need it, because every action here is a tap and not a gesture. **Any new
dropdown, filter popover or overlay does**, on its own container.

### 4.7 What carries over

**Unchanged:** `MpPageShell`, `MpCommandBar`, `MpFilterPills`, `MpEmptyState`, `MpKpiStrip`,
`SkeletonCardGrid` (`src/components/ui/skeleton-card.tsx:60`), `Button`, `Modal`, `Input`,
`PlatformPill`, `PlatformSquircle`, `toast`.

**A variant:** `MpBrowseCard` (`MpBrowseCard.tsx:32-184`) has the right DNA but its poster-identity block
(`:124-139`), favourite star (`:111-120`) and slots-left chip (`:45-47`, `:167-172`) all belong to the
per-listing model and have no meaning for a clip anyone may post. `post-clip-modal.tsx:83-320` is the
closest thing to "submit the live URL" but is built around a listing's multi-platform `postedPlatforms`
array (`:98-108`); a single-URL variant is needed, keeping its deadline messaging (`:290-302`) if the
30-minute rule applies.

**Cannot be reused as they stand, for the reason in 4.0:** `MpStatusBadge`, `MpStatusGlyph` (which also
renders bare lucide icons with **no `aria-hidden`** anywhere, against this product's own rule, so reusing
it double-announces), and `MpDeadline` (three urgency levels by colour alone, `:78-90`).

**New:** the word-first three-way ribbon, the skip action and its reversal (**there is no skip, hide or
dismiss concept anywhere in this product** except a dismissible Discord banner), the clip detail screen,
and the server-side in-progress flag with its resume banner.

---

## PART 5 — THE EDITOR'S EXPERIENCE

### 5.1 The submission form

Modelled directly on `src/components/marketplace/SubmitClipModal.tsx`, which already does this job for a
Drive link and is the literal template. Fields, top to bottom:

**1. The Drive link. Required.**
* label **"Drive link *"**, placeholder `https://drive.google.com/file/d/...` (`SubmitClipModal.tsx:240-241`)
* validation mirrors `isValidDriveUrl` (`SubmitClipModal.tsx:55-69`): parses as a URL, protocol is http or
  https, host is `drive.google.com`, `*.drive.google.com`, `docs.google.com` or `*.docs.google.com`
* empty: **"Drive link is required."**
* wrong shape or host: **"That needs to be a Google Drive link. Copy it from Drive with the Share
  button."**
* `autocomplete="url"`
* a `<details>` block, closed by default, exact pattern from `:245-257`, summary **"How to share your
  video"**, then numbered steps: 1. Upload your video to Google Drive. 2. Right click the file, choose
  Share, set it to "Anyone with the link", Viewer. 3. Copy the link and paste it above.
  Footnote: **"Best results: an MP4 file, vertical, under 100MB. Once the owner approves it, any poster
  can download it and post it."**

**2. A title. Required.** One line, so a poster's card has a name and a screen reader has a heading.

**3. Notes for the owner. Optional.** `Textarea`, placeholder **"Anything the owner should know about
this clip"**, 2,000 characters with a live counter, same pattern as `:319-330`.

**No platform checkboxes.** They exist in the old form because a CLIPPER picks which of a poster's
accounts to target. An editor targets nobody.

**Submit button: "Submit clip"** (`:354`), disabled via `aria-disabled` rather than the native attribute
so it stays keyboard reachable (`:350-352`), with the blocking reason in a
`role="status" aria-live="polite"` paragraph above the button row (`:338-341`), not a toast, so the reason
is readable without dismissing anything.

**On success:** toast **"Clip submitted. Waiting for review."**, the modal closes, the list refreshes.

**Errors reused verbatim:** 409 duplicate, server message with a fallback (`:186-197`); 429 **"Too many
requests, wait a bit."** (`:199-200`); generic **"Could not submit clip. Please try again."**
(`:203-210`); network **"Network error. Please try again."** (`:211-212`).

**Accessibility, required rather than optional:** every field gets a visible `<label htmlFor>`, required
fields get `required` plus `aria-required="true"` with one line above the form saying *"Fields marked
with * are required."* The error pattern is already correct in
`src/components/ui/textarea.tsx:30-31, 42-48, 62-66` (generated id, `aria-invalid`, merged
`aria-describedby`, error in its own `<p id="{id}-error">`) and should be copied, not re-invented.
Validate on blur and on submit, never on keystroke, and re-validate on change once an error has shown.
On a multi-error submit, add a focus-moved error summary with `role="alert"`, a count and links to each
field. **Moving focus to that summary is the step most often skipped and belongs in the acceptance test.**

### 5.2 The three states, in words

Per PART 4.0, every state reads in words. No state is a coloured dot.

**PENDING**
* headline **"Waiting for review"**
* body **"The owner has not looked at this yet. Nobody can see it until it is approved."**
* underneath, **"Submitted {relative time}"**, using `formatRelative` (`my-submissions-client.tsx:15`)
* **no time estimate.** Nothing in this product forecasts a moderation queue, the depth of the owner's
  queue is unknowable to the editor, and a promised window is a claim the interface cannot keep.

**APPROVED**
* headline **"Approved. Posters can see it."**
* body **"Any poster can now find this clip and post it. You earn 45 percent of every post."**
* the clip moves out of the waiting section into his active list

**REJECTED**
* headline **"Not approved"**, paired with the reason so the word is not doing the whole job alone
* the owner's words **verbatim, unmodified, unsummarised**, under a heading reading
  **"Why it was not approved"**
* if the owner filled the optional improvement note, a second separate line headed **"What to change"**,
  which reads as help rather than a second verdict
* action: **"Send a fixed version"**, which opens the form empty. **A rejected Drive link should not be
  silently reused**; he should paste a link to the corrected file.

**An accessibility requirement the existing product currently fails, recorded here so a build round does
not inherit it.** At `MpSubmissionRow.tsx:579-594` the "Rejection reason" label is a plain `<p>`, tied
programmatically to nothing, and the "Details" toggle at `:488-498` has `aria-expanded` with **no
`aria-controls`** and a panel with **no `id`**. With several rejected rows on screen a screen reader user
cannot tell which clip a reason belongs to. **v2 pairs the toggle and panel by id, and makes the reason
heading name its clip:** `<h3 id="rejection-{id}">Why "{clip title}" was not approved</h3>` with
`aria-labelledby` on the reason paragraph.

### 5.3 His dashboard

**Summary strip**, on the existing `MpKpiStrip` (`MpKpiStrip.tsx:20-30`), which is already
`grid-cols-2 gap-4 md:grid-cols-4` (`:36`) and therefore already correct at 375px as a two by two:

1. **Clips submitted**
2. **Approved and live**
3. **Total posts**, summed across every approved clip. **This is the number that makes "45 percent of
   every post" legible at a glance.**
4. **Total earnings**, his 45 percent summed across every post of every clip, in the big-number treatment
   the dashboard already uses (`dashboard/page.tsx:432-441`)

Below the strip, as a secondary line rather than a fourth tile, **"Views across all posts"**. Keeping it
off the tile row avoids conflating "how many people posted it" with "how much it was watched", which are
different signals to an editor deciding what to make next.

**Per clip row:** thumbnail or title, the state word, **"Posted by N posters"**, **"Views: N"**,
**"Earned: $X.XX"**, and the submitted date as relative time.

**The empty state that actually matters: an APPROVED clip nobody has posted yet.** This is not the
zero-clips empty state. The clip passed the only gate it faces. Copy: **"Approved. Waiting for its first
poster."** and render the numbers exactly as any other value, `$0.00` and `0 views`, with no alarm
treatment. **Zero here is a legitimate, expected, temporary state and not an error**, which is the same
principle BL-531 applied to a pool reading "Full".

### 5.4 What he must not see

| field or data | why | where the product already strips it |
|---|---|---|
| `clientName`, `aiKnowledge` | CLAUDE.md, verbatim: never selected into any clipper-facing response | `src/app/api/campaigns/[id]/route.ts` strips both (BL-531). **Warning, not a precedent to copy:** `/api/campaigns` (the list) still does NOT strip them for a CLIPPER, logged as **BL-532, STATUS: TODO** at `BACKLOG.md:19078`. **That is the exact mistake v2's routes must avoid: an `include` with no explicit `select` leaks what a sibling route already blocks.** v2's editor routes use an explicit allow-list `select` |
| `ownerCpm`, the per-platform owner CPMs, `agencyFee`, `lockedOwnerShareDecimal` | CLAUDE.md, and the owner's split must never be derivable | `src/lib/campaign-clipper-view.ts`, applied at four routes (BL-531) |
| any raw rate he could back-solve a cut from | the same rule inside the existing marketplace | `marketplace/submissions/route.ts:1073-1075` applies `stripSubmissionCpm` to every row, with the comment *"so the creator can't derive the 10% from My Submissions"*. The per-post figure it DOES show (`:1051-1053`) is the creator's **share already applied**. **v2 shows the editor's 45 percent pre-multiplied, never a rate** |
| another editor's clips or earnings | ordinary tenant isolation | `marketplace/submissions/route.ts:984`, `where: { creatorId: session.user.id }`, scoped **at the query** and never filtered client side |
| a poster's email, Discord id, wallet, payout history or balance | no rule anywhere permits surfacing a counterparty's contact or financial identity | `marketplace/submissions/route.ts:245`, `:921`: the poster's `email` is selected **only inside the server-side query that addresses a notification**, and the response shape at `:994-1075` carries only `username` and the two rating aggregates. **That "select it for server use, never place it in the response shape" split is the pattern v2 must follow** |
| campaign budgets, owner economics, the owner's 10 percent | BL-841 item 7 measured this leaking in the existing marketplace to every viewer with no role gate | `listings/[id]/route.ts:388-400`, rendered at `TrustBadges.tsx:102-120`. **The one thing in the existing marketplace v2 must be careful NOT to copy** |

### 5.5 Should he see WHICH posters posted his clip

**For:** it closes the loop the way "Posted by @username" already does on the existing creator view
(`my-submissions-client.tsx:189-190`), makes "45 percent of every post" feel earned rather than abstract,
and tells him what kind of poster picks up his work.

**Against:** a poster is a counterpart he has no relationship with, unlike the existing marketplace where
the two explicitly transact per listing. The platform's stance everywhere else is to strip identity to
the minimum the surface needs. And naming which accounts posted a given clip opens a **poster-side**
privacy surface, which is not the editor's to open.

**Not decided. Open question 16.** The dashboard above uses only the aggregate count precisely so a named
list can be added later without changing the summary layer.

### 5.6 Mobile at 375px

The `Modal` (`src/components/ui/modal.tsx`) is already edge to edge at this width with the sticky bottom
action bar from `SubmitClipModal.tsx:332-357` (`-mx-6 px-6` bleeds the border full width, buttons pinned
above the keyboard). Single column field stack, nothing side by side. The KPI strip renders two up. The
per-clip list is a stacked `divide-y` of single-column rows, not a table, matching
`my-submissions-client.tsx:343-362`. Primary actions stay at or above 44px
(`dashboard/page.tsx:375`, `min-h-[44px]`).

### 5.7 THE THUMBNAIL, AND THE DRIVE QUESTION

**What already exists, measured.** `extractDriveFileId` (`src/lib/video-hash.ts:60-74`) recognises exactly
two id-bearing shapes, gated on host at `:62`: the path form `/file/d/<ID>/` via the regex at `:66`, and
any `?id=<ID>` via `u.searchParams.get("id")` at `:70`, which covers `/open?id=`, `/uc?id=` and
`/thumbnail?id=` (named in the comment at `:69`). Anything else falls through to generic
`hostname + pathname` hashing at `:83`.

**Three independent copies of a much weaker check** decide what is even accepted as a Drive URL, and none
requires an extractable file id, only a matching host: `marketplace/submissions/route.ts:57-71`,
`marketplace/submissions/[id]/route.ts:24-38`, and `SubmitClipModal.tsx:55-71`. All three accept
`docs.google.com`, which is not a video host. **That is an existing gap, reported and not changed.**

**BL-868 measured the link problem and it is worth restating**, because it is the single most expensive
Drive lesson this platform has: `/open?id=<FILE_1>` and `/open?id=<FILE_2>`, two completely different
files, **hashed identically**, because `drive.google.com/open` was the entire normalised string. *"An
honest second submission was refused as a duplicate. This is the worse of the two, because it blocks real
work and looks like a false accusation."* BL-868 fixed it; **v2 must use the fixed function and never
re-implement the normalisation.**

**Ask the editor for the `/file/d/<ID>/view` form.** The id sits in the path so a human can verify it at a
glance, it was never the form that collided, and it matches `video-hash.ts:66` directly. The `?id=` forms
are handled and are not unsafe, only less legible.

**CAN THE PRODUCT TELL WHETHER A LINK IS ACTUALLY SHARED? MEASURED: NO, AND IT DOES NOT TRY.** All three
validators check host and protocol only. **Nothing in `src`, `scripts` or `prisma` calls the Google Drive
API, fetches a Drive URL, or checks sharing status**; the only Google API calls in the repo are YouTube
Data API v3 (`src/lib/youtube.ts:29`, `:95`, `:182`, `src/lib/verify-cascade.ts:364-388`). A link to a
private file passes validation exactly like a public one, and **the first thing that discovers it is the
owner clicking it in the approval queue.** That is acceptable, because a human is the next step anyway.

**CAN A FIRST FRAME BE EXTRACTED WITHOUT STORING THE VIDEO? Three routes, priced.**

| route | what it needs | cost | failure modes | verdict |
|---|---|---|---|---|
| **A. Drive's official `files.get?fields=thumbnailLink`** | a Google Cloud project, the Drive API enabled, and an API key (sufficient for a link-shared file per Google's own reference) | **no per-call fee**, within the standard project quota | **the link is short lived, "typically on the order of hours", and CORS blocked**, so the bytes must be re-hosted immediately. A new secret to provision and rotate. Returns nothing for a file the key cannot reach, including one the editor has not finished sharing | **viable, sanctioned, and the only documented mechanism** |
| **A'. the undocumented `drive.google.com/thumbnail?id=<ID>&sz=w<N>`** | nothing | **$0** | **NOT DOCUMENTED by Google anywhere**, so it can change or be rate limited with no notice. Its current behaviour for a private file was **not verified** in this round | cheapest if durable, least trustworthy for the same reason |
| **B. server-side HTTP Range plus ffmpeg** | **a new dependency and a new runtime.** `package.json` has **no** `ffmpeg`, `fluent-ffmpeg` or any video library; the only image library is `sharp ^0.34.5`, which cannot decode video. The build is NIXPACKS on Railway and nothing in the repo makes an `ffmpeg` binary available | infrastructure plus engineering | if the source MP4's `moov` atom is at the FRONT the first frame is a few hundred KB away; if it is at the END, which is common from Premiere, DaVinci and Final Cut without "fast start", the code must fetch near the end of the file first. Whether Drive's consumer endpoints honour Range at all was **not verified** | **most expensive and most fragile, for a first frame. Recommend against** |
| **C. browser-side canvas capture at submission** | nothing new on the server | **$0**, no ffmpeg, no API key | only works at the moment of submission, with nothing to re-derive later since the video is deliberately never stored. Depends on the editor's browser loading the video cross-origin from Drive, and on his connection holding | **cheapest to run, and the upload destination already exists**: `src/app/api/upload/route.ts` takes JPEG, PNG, WebP and GIF up to 5MB validated by magic bytes, and `src/lib/clip-thumbnail.ts` already proves the Supabase re-host pattern |

**WHEN EXTRACTION FAILS.** The product's own rule is already written down and must be followed:
`clip-thumbnail.ts:289-293` states *"FAIL SAFE, always... A missing preview is cosmetic; a throw on the
submit path is not"*, and every failure returns a `reason` string with `url: null`
(`clip-thumbnail.ts:47-55`) rather than a claim about the source.

> **A THUMBNAIL FAILURE IS NEVER RECORDED AS A FACT ABOUT THE VIDEO.** BL-874 established that a fetch
> failure can never be recorded as a deletion, and BL-845's `verifyFailedAt` and `verifyFailedReason` on
> `MarketplaceSubmission` exist to keep "we could not confirm" separate from "this is gone". **A clip with
> no thumbnail stays fully usable:** the poster still gets the link, still downloads, still posts, and
> nothing about payability, catalogue visibility or anyone's standing may key off whether a thumbnail
> exists. The editor sees a placeholder, never a message implying his video is missing or invalid.

**DRIVE ONLY VERSUS ON-SITE PREVIEW, with real numbers.** Assumption stated plainly: a 30 to 60 second
vertical clip at reasonable quality is **roughly 30MB**. That is an estimate; no sample file exists in
this repo to measure. Supabase figures are from its current published pricing, fetched this round, not
from the repo: Pro at $25 per month includes 100GB storage and 250GB standard egress, then $0.0213 per GB
storage, $0.09 per GB standard egress, $0.03 per GB cached.

| clips | storage | **storage cost** | egress at 50 downloads each | **bandwidth cost** |
|---|---|---|---|---|
| 100 | 3GB | **$0**, inside the 100GB included | 150GB | **$0**, inside the 250GB included |
| 1,000 | 30GB | **$0** | 1,500GB | **about $112.50 a month** standard, about $37.50 if cached |
| 10,000 | 300GB | **about $4.26 a month** | 15,000GB | **about $1,327.50 a month** standard, about $442.50 if cached |

**Storage is nearly free at every scale. BANDWIDTH IS THE COST, and it multiplies by downloads per clip,
which is precisely what this design is built to maximise.**

**Drive only costs the platform $0 directly**, because Google absorbs both the storage and every
download on the editor's own quota. What it costs instead: the editor can delete or unshare the file at
any moment with no notice; a personal Drive account carries an undocumented "too many users have viewed
or downloaded this file recently" throttle whose threshold Google does not publish; and a file above
roughly 25MB commonly shows Drive's "cannot scan for viruses" interstitial before download, which at a
30MB clip would apply to most submissions.

> **RECOMMENDATION: BUILD THE THUMBNAIL AND LEAVE THE VIDEO ON DRIVE. RECOMMEND AGAINST ON-SITE VIDEO
> HOSTING FOR THE PILOT.** Thumbnails are a handful of small JPEGs and are effectively free at any scale
> in that table. On-site video is the expensive option exactly at the scale a working marketplace wants,
> and it buys one thing: removing the broken-link risk. **That is not worth $1,327 a month at 10,000
> clips, and it matches the owner's own lean.** Of the three extraction routes, **C (browser canvas) is
> the recommendation for the pilot** because it needs no new secret, no new dependency and no new
> runtime, with **A (the official Drive API) as the upgrade** if retroactive backfill turns out to matter.

**What to store about the Drive file:**
* the raw pasted link, exactly as submitted
* **the canonical file id as its own column**, derived once with `extractDriveFileId`. Measured: **no such
  column exists today**; grepping `driveFileId` across `src`, `scripts` and `prisma` returns only the
  function name itself at `video-hash.ts:60`. Storing it means the thumbnail path and the duplicate hash
  key off one derivation instead of two that can drift
* **the thumbnail as OUR OWN re-hosted bytes**, never a hotlink, per `clip-thumbnail.ts:6-10` and `:28`:
  provider thumbnail URLs expire and are unstable, so *"the URL we STORE must always be our own copy"*
* re-checking that the file still exists: **yes, but it may only ever downgrade to "cannot confirm"**,
  never to "confirmed deleted", unless Drive returns a clean positive not-found. It needs its own cron or
  route and **must not be folded into `tracking.ts`**, whose `dueJobs` query CLAUDE.md forbids adding a
  top-level `select` to.

**What could NOT be determined, stated plainly:** the current behaviour of the undocumented
`drive.google.com/thumbnail?id=` and `uc?export=download` endpoints for a private versus a link-shared
file; whether Drive's consumer download endpoints honour HTTP Range; the numeric threshold of Drive's
download throttle; whether Supabase's CDN would cache-hit repeated downloads in this project's bucket,
which changes the bandwidth column by a factor of three; whether editors will use personal Gmail Drive
(15GB free) or a Workspace tier; and whether an `ffmpeg` binary can be built into this project's actual
NIXPACKS image. **None of these was guessed at and presented as measured.**

---

## PART 6 — THE OWNER'S EXPERIENCE

### 6.1 The approval queue

**The row.** Modelled on `MpSubmissionRow.tsx:11-18`, whose own comment documents the layout
`[Glyph] [Identity + pills] [Drive link] [Deadline] [Actions]` with a second line carrying a status verb
and relative time. For this queue: **the editor's clickable name, the clip title, the campaign name, the
age of the submission as relative time** (`formatRelative`, `MpSubmissionRow.tsx:37`, `:324`). **No poster
name on this row**, because nobody has posted anything yet.

**How he watches the video, and this is a measured fact rather than a design preference.**
**Nothing in this codebase plays a Drive video inline, anywhere.** Every Drive surface renders an
`ExternalLink` anchor with `target="_blank"` and lets Drive's own viewer do the playback:
`MpSubmissionRow.tsx:458-466` and `admin/clips/page.tsx:2229-2238`. **Follow that pattern. Do not build
this product's first inline video player for this feature**, which would be new surface with no precedent
and no proof it survives every Drive sharing-permission edge case.

**Approve.** One tap for the OWNER. The existing clips page gates a two-tap "Confirm approve?" behind
`isReviewer` only (`admin/clips/page.tsx:1144-1166`); the OWNER stays one tap. An **optional** note to the
editor is fine, mirroring the existing approve-comment modal (`:3181-3213`), and should not be required.

**Reject. Always a modal, never one tap.** The clips page marks this deliberate:
*"Reject path is intentionally NOT gated (owner spec)"* (`admin/clips/page.tsx:477`, modal at
`:2735-2740`).

**THE REJECT REASON, AND THE TWO EXISTING PRECEDENTS DISAGREE WITH EACH OTHER.**

| | clips page (`admin/clips/page.tsx:3124-3172`) | marketplace incoming (`marketplace/incoming/reject-modal.tsx`) |
|---|---|---|
| required | **no.** The button is never disabled and the server writes `reason \|\| null` (`:1329`) | **yes**, `reasonValid = length > 0 && <= MAX_REASON` (`:68`), submit disabled otherwise |
| cap | **none anywhere on the field** | **1,000** (`MAX_REASON`, `:8`) |
| presets | 6 chips (`rejectionExamples`, `:1649`) that **overwrite typed text with no confirmation** | 5 chips that **ask before overwriting** (`:138-146`) |
| improvement note | no | **yes**, separate and optional, 1,000 characters |

> **TAKE THE MARKETPLACE ONE, NOT THE CLIPS ONE.** An editor whose living is 45 percent of every future
> post on that clip cannot act on a rejection with no reason. **Reason required, capped at 1,000
> characters, presets that confirm before overwriting, plus the separate optional improvement note.**

**Verbatim copy**, adapted minimally from the shipped strings:
* label: **"Why it is not approved *"**
* placeholder: **"Explain what is wrong. The editor will read this exactly as you type it."**
* presets, adapted from `REJECT_TEMPLATES` (`reject-modal.tsx:15-21`): **"Does not match the campaign"**,
  **"Quality is too low, please redo it"**, **"Wrong format or size"**, **"Caption or hashtags do not
  match the rules"**, **"Too close to a clip already approved"**
* optional note: **"What to change (optional)"**, placeholder **"Tell him how to get it approved next
  time."**

**After acting.** No confirmation screen. `toast.success` and the row updates in place, optimistically,
then leaves the pending filter, **with the scroll position and the search state kept**. The existing
clips page explicitly refuses to re-fetch for exactly this reason (`admin/clips/page.tsx:1317-1330`).

**Undo.** The existing clips-page pattern verbatim: a plain one-tap non-modal **"Undo"** with the
`RotateCcw` icon on both approved and rejected rows (`admin/clips/page.tsx:2755`, `:2761`). **One
difference must be spelled out:** undoing an approval here pulls the clip **back out of the catalogue**,
which is a stronger effect than undoing an ordinary clip approval, and the copy should say so:
**"This will hide the clip from every poster again."** What happens to posts already made under that
approval is a money question and belongs to the conversion machinery in PART 3.10, not to an undo button.

**The reject modal's accessibility, and the existing shared `Modal` DOES NOT MEET IT. Measured, by reading
`src/components/ui/modal.tsx` in full:**
* `:53` and `:72`: the backdrop and the panel are plain `<div>` elements. **No `role`, no `aria-modal`,
  anywhere in the file.**
* `:106-110`: the title is an `<h2>` **with no `id`**, so `aria-labelledby` has nothing to point at.
* `:42-48`: Escape closes via a bare `document.addEventListener`, functional but not part of any dialog
  semantics.
* **No `useRef`, no `.focus()` call, no Tab interception anywhere in the file. There is no focus trap and
  no focus return to the trigger.**
* `:71`'s comment, *"Clicking outside does NOT close the modal"*, already matches the right behaviour and
  should be kept.

Both existing callers (`marketplace/incoming/reject-modal.tsx:112` and
`marketplace/admin/marketplace-admin-client.tsx:568`) drive it from plain boolean state with no
trigger-ref capture, so there is no compensating logic at the call sites either, and
`src/components/ui/confirm-modal.tsx:33` is a thin wrapper over the same thing.
**The fix belongs in `modal.tsx` itself or in a new dialog primitive, so the new reject dialog and both
existing ones inherit it together.** Requirements: focus trapped in the dialog with Tab and Shift Tab
wrapping, initial focus on the reason textarea and never on the destructive button, **focus returned to
the exact row button that opened it** and to the next row's equivalent action if that row is gone,
Escape following the same return path, `role="dialog"` with `aria-modal="true"` and `aria-labelledby`
pointing at the title's own id, and `data-no-swipe` on the modal root because it is a real overlay near
the left edge where the global handler at `src/components/layout/app-layout.tsx:646` lives.

### 6.2 The clips list with both names

> **THE OWNER'S REQUIREMENT ALREADY EXISTS IN SHIPPED CODE, AND IT IS THE PATTERN TO EXTEND RATHER THAN
> INVENT.** `src/app/(app)/admin/clips/page.tsx:2056-2070` already renders, for a marketplace clip:
> `Posted by @{clip.user.username}` linking to `/admin/users/${clip.userId}`, then
> `· Created by @{submission.creator.username}` linking to `/admin/users/${submission.creatorId}`.

**And it already satisfies the colour rule, which is worth noticing because it was not obvious.** Both
names render **identically**, `font-semibold text-accent`. **Nothing about the colour distinguishes
them.** What distinguishes them is the **preceding label word in muted grey**, "Posted by" versus
"· Created by". That is exactly the right construction under BL-864, and v2 should reuse
**"Created by" verbatim** rather than invent a new word, since it is already shipped and already reads
correctly.

**Where each links:** `/admin/users/[id]`, the existing owner user-detail page. **No new destination is
needed.**

**The field rendered is `user.username`, not a Discord tag.** `username` and `discordId` are two distinct
separately searchable fields (`admin/clips/page.tsx:255`, `:1766`), and **the Discord id is never
rendered** in this file or in `ReviewMetaBlock` (`src/components/admin/ReviewMetaBlock.tsx:106-108`, whose
comment says the Discord tag and raw id were deliberately removed from the rendered name). **v2 shows
`username`. It must not start printing Discord ids.**

**On an ordinary clip with no editor**, the existing `else` branch renders a single unlabelled name
(`:2072`). **A v2 clip degrades to exactly that, unchanged**, which is the correct behaviour and needs no
work.

**Accessibility for two links on one row**, which has no precedent in this codebase because only one
identity renders per row today: the visible text stays `@{username}`, and each link carries
`aria-label="Editor: @{username}"` or `aria-label="Poster: @{username}"`. **The label must contain the
visible text verbatim** (WCAG 2.5.3) or a speech-input "click username" stops matching. A visually hidden
prefix span is an equally valid technique; pick one and use it for both, never mixed.

**What the owner's clips list renders today, in order, so a v2 row can slot in without disturbing it:**
identity block with the dual-name branch (`:2056-2074`), marketplace badge (`:2075`), trust score, owner
only (`:2078-2082`), platform icon, account handle and campaign name with the reassign button on PENDING
rows (`:2091-2131`), fraud and status badges (`:2172-2194`), client comment chip (`:2200-2216`), "Open
clip" (`:2221`) and "Original drive" on marketplace clips (`:2229-2238`), the stat chips (`:2240-2251`),
the cadence badge (`:2252-2262`), the money breakdown gated on `isAdminOrOwner` (`:2285`), the evidence
panel (`:2679`), the action row (`:2696-2762`), and the review meta block (`:2775-2786`).

### 6.3 Notifications

**The ordinary clip decision, measured, so the two new ones can match it exactly:**

| | in-app | email |
|---|---|---|
| **approved** | `createNotification(userId, "CLIP_APPROVED", "Clip approved!", "Your clip has been approved and earnings have been calculated.")`, `clips/[id]/review/route.ts:1239`. **A marketplace creator already gets a distinct body**: *"Your marketplace clip was approved — your earnings have started."* (`:1244`) | `sendClipApproved(email, campaign, earnings, comment)` (`:1250`), subject **"Your clip was approved"** (`src/lib/email.ts:565-577`). Fired only `if (clip.user?.email)` (`:1246`) |
| **rejected** | `createNotification(userId, "CLIP_REJECTED", "Clip rejected", reason ? \`Reason: ${reason}\` : "Your clip was rejected. Check the reason and try again.")`, `:1399` | `sendClipRejected(email, campaign, reason, {...})` (`:1488`), subject **"Clip update"**, reason in a callout (`email.ts:583-608`) |

Both channels fire together, in-app first, both fire and forget (`.catch(() => {})`). **Neither is subject
to `canSendMarketing`**, because both are transactional, and that is correct and must stay so.

**The two new ones, verbatim:**

* **in-app, approved:** title **"Clip approved!"**, body **"Your marketplace clip was approved. Posters
  can see it now and you earn 45 percent of every post."**
* **in-app, rejected:** title **"Clip not approved"**, body **"Reason: {the owner's words}"**. Because the
  reason is required in 6.1, this branch is always taken and the fallback string never renders.
* **email, approved:** subject **"Your clip was approved"**, same structure as `sendClipApproved`.
  **The earnings line will legitimately be zero**, because the editor's 45 percent does not exist until a
  poster posts, and that is an existing conditional in the template rather than new work.
* **email, rejected:** subject **"Clip update"**, the required reason in the callout.

**One thing the owner should decide rather than have decided for him.** He asked for the same shape as an
ordinary clip decision, and reusing the literal `"CLIP_APPROVED"` and `"CLIP_REJECTED"` type strings gives
him exactly that. **The consequence is that in the editor's own feed these are indistinguishable from an
ordinary clip decision except by their wording**, and both route to `/clips` today
(`src/components/layout/notif-href.ts:133-140`), which is the wrong destination for an editor submission.
**At minimum the deep link needs a v2 destination. Whether the type string should differ too is open
question 26.**

**One existing hazard worth recording.** The rejection reason is stored verbatim with **no validation and
no length cap on the clips path** (`clips/[id]/review/route.ts:62`, `:1334`) and is passed straight into
the notification body at `:1399`. Email template escaping neutralises HTML on that leg. **v2's 1,000
character cap from 6.1 closes the length half of this on its own surface.**

### 6.4 What he needs to spot theft by eye

**Nothing automatic, and PART 3.8 gives the full reasoning.** No similarity score, no hash comparison, no
"possible theft" flag, no queue ranked by suspicion. All three are content matching under another name and
BL-871 priced and rejected the whole family, with BL-771's 20.2 percent precision against a 99.2 percent
requirement as the measurement.

**What to build instead is cheap, human, and shaped like something already shipped.**

**1. One link, from a suspicious ordinary clip into the catalogue, filtered to the same campaign.**
On a normal clip row in `/admin/clips`, a one-tap **"Compare to catalogue"** opening the v2 catalogue
filtered by that clip's `campaignId` in a new tab. Nothing computed, nothing matched: the posted video is
already one tab away via "Open clip", and this puts every approved editor video for that campaign in the
next one. **This is the existing "Original drive" link pattern (`admin/clips/page.tsx:2229-2238`)
generalised from "this clip's own submission" to "this campaign's whole catalogue", with zero new
infrastructure.**

**2. Beside each catalogue entry, the facts he already needs anyway:** the editor's name, the submission
date, **which accounts have posted it, and how many times.** If he is looking at a suspicious clip from
account X on campaign Y, he glances at Y's catalogue, sees "editor Z's video, posted by A, B and C", and
notices by eye that **X is conspicuously absent from that list while running very similar footage.**
**That absence is the signal, and it is a fact he has to look at anyway rather than a new computed
score.**

**3. The editor's own report, from PART 3.8.** He knows his work on sight and has the strongest motive to
look. It arrives as evidence in the same place, never as a verdict, and never as anything a clipper can
see.

**At 375px there is no side by side.** He opens the catalogue link, looks, switches back. That is one tap
each way, the same as any external link today, and the surface should not be designed assuming a split
screen.

### 6.5 What an ADMIN must not see

* **The owner's 10 percent and the total, gated on `isOwner` and NOT on `isAdminOrOwner`.** The existing
  marketplace block does exactly this at `admin/clips/page.tsx:2435`, with a comment worth quoting:
  *"BOTH of these are owner only... a gate that can be undone by arithmetic is not a gate"* (`:2429-2433`).
  **An ADMIN sees the editor's 45 and the poster's 45, never the owner's 10 and never the total.**
  **BL-841 item 8 measured the existing marketplace failing exactly this**, because its "Owner share" row
  is gated on `isMkt` rather than `isOwner` while its CPM_SPLIT neighbour four lines above is gated
  correctly. **Do not copy that line.**
* **Rates stay owner only even where a computed dollar figure is shown wider** (`showRates`, `:2403`).
* `clientName`, `aiKnowledge`, `ownerCpm`, `agencyFee`: never in any clipper-facing response, and the same
  rule reaches any new campaign context shown in the approval queue.
* **The approval queue itself is probably an OWNER page, not an ADMIN one.** The existing marketplace
  admin dashboard is hard gated `if (user?.role !== "OWNER") notFound()`
  (`src/app/(app)/marketplace/admin/page.tsx:21-22`) with the comment *"Even when the marketplace launches
  publicly... the admin queue stays locked to OWNER."* The brief says only "the owner approves" and never
  mentions ADMIN. **Whether an ADMIN may see the queue at all is open question 27, not assumed here.**

---

## PART 7 — EVERY INVARIANT THIS THREATENS, CHECKED ONE BY ONE

> ### THE SHARPEST RISK, STATED FIRST AND PLAINLY
> **With two earners on one clip, an error does not cost one person, it costs two, and a rounding error
> repeats once per post.** A cent misallocated on a clip that fifty people posted is fifty cents, and the
> editor's leg has **no invariant middleware guarding it at all**, exactly as BL-841 found for the
> existing marketplace's two tables (item 14: *"No invariant middleware guards either marketplace
> table"*). The L2 middleware and the L1 hard lock both watch `Clip.earnings`. **Fifty-five cents in
> every v2 dollar lives somewhere nothing is watching**, unless this design puts a guard there on
> purpose. Every requirement below exists because of that sentence.

### 7.1 BL-627: no overpayment, and the budget is never exceeded

**How it is threatened.** The fifty-posters multiplier is the hardest stress on this invariant in the
platform's history: one campaign, one clip, fifty concurrent earning rows, and 55 cents of every dollar
living outside `Clip.earnings`.

**What survives untouched.** BL-627 proved three independent mechanisms and all three are intact:
per-tick truncation inside a Serializable transaction (`tracking.ts:2335-2534`), the L1 hard lock in
`writeClipEarnings` which reads COMMITTED spend and THROWS on `projected > budget`
(`clip-earnings-writer.ts:199-257`), and **per-campaign SEQUENTIAL tracking**, so fifty posts on one
campaign are processed one after another and there is no same-campaign concurrency to lose a race to.
Fifty posts are fifty ordinary clips on one campaign, and the engine already handles that shape.

**THE ONE REQUIREMENT, AND IT IS THE SHARPEST STRUCTURAL RISK IN THE DESIGN.**
`getCampaignBudgetStatus` computes `spent` at `src/lib/balance.ts:487-497`, and BL-627 recorded what it
already sums: *"clip earnings + CPM_SPLIT owner agg + marketplace creator/platform"*. **The two new v2
aggregates must be added there.**

If they are not:

| | |
|---|---|
| what the lock sees per v2 dollar | 45 cents (the poster's leg, through `Clip.earnings`) |
| what actually leaves the budget | 100 cents |
| a $5,000 campaign pauses after distributing | **$11,111** |
| what a test reading `Clip.earnings` would show | **everything correct** |

**It is one line, it is silent when wrong, and no existing test would catch it.** It belongs in the
build plan's first round, not its last.

**A second requirement, subtler.** The L1 lock computes `projected = status.spent + delta`
(`clip-earnings-writer.ts:238`). On a v2 clip the `delta` handed to it must be the **full gross**, not
the poster's 45 percent, or the projection under-counts every increment by 55 percent. BL-841 found the
neighbouring shape already broken in the existing marketplace (item 3: the budget scale-down floors three
legs and then passes the UNSCALED poster base to `writeClipEarnings`, so `assertInvariant` throws above
$0.01 drift). **Do not copy that call site. Read BL-841 item 3 before writing it.**

**An operational note that is not an invariant but will be felt.** The due-jobs query is ordered
`checkIntervalMin ASC` under a 200-call-per-tick cap (`tracking.ts:3611`, BL-200, explained in BL-538).
Fifty posts of one viral clip are fifty tracking jobs competing for that cap. Nothing breaks; the ladder
simply has more to do.

**VERDICT: HOLDS, conditional on one line in `balance.ts` and one argument at the `writeClipEarnings`
call site.**

### 7.2 BL-696: nobody can be paid twice

**How it is threatened in a new way.** One clip now funds two people, so the question is no longer only
"can one person be paid twice for one clip" but "can one clip's gross be paid out twice in total".

**How the design preserves it.** The two legs live in **different tables keyed to different user ids**,
which is the same construction BL-841 verified for the existing marketplace: *"the creator's 60 and the
poster's 30 live in different tables joined to different user ids"*. The poster's leg is
`Clip.earnings` where `Clip.userId = poster`. The editor's leg is `MarketplaceV2EditorEarning` where
`editorId = editor`. **No query can reach both as one person's money unless the person IS both**, and
the partial unique index `uq_payout_open_per_user_campaign` still allows exactly one open payout per
(user, campaign).

**THE NEW CASE, AND IT IS REAL: the editor who posts his own clip** (open question 4). If he is allowed
to, his 45 percent as editor and his 45 percent as poster are two rows, same user, same clip. **That is
not a double payment, it is two legitimate legs**, and the balance derivation must sum them without
double-counting the gross. **Requirement: the editor aggregate and the `Clip.earnings` aggregate must be
disjoint by construction and summed additively, never one derived from the other.** If instead the
editor total were derived as "gross minus poster minus platform", a self-posting editor would be counted
twice and the invariant would break on exactly the case the owner is most likely to try first.

**BL-696's one real gap is unchanged and is not made worse:** there is still no admin path that records a
payment made by hand, so a payment outside the platform leaves the balance fully claimable. That is
procedure, not code, and v2 neither helps nor harms it.

**VERDICT: HOLDS, with one explicit requirement about how the two aggregates are summed.**

### 7.3 BL-824 paid-is-final, with BL-849's write side: THE CONVERSION THREATENS THIS DIRECTLY

This is the only invariant in the list that a feature in this design actively pushes against, and PART
3.10 specifies the whole guard. Restated here as the invariant check:

* **The read side is already safe.** `effectivePaid = min(paidGross, payableEarnings)`
  (`balance.ts:234-258`) means a payment can only ever consume the earnings of the campaign it was made
  against. A poster whose recorded earnings collapse after conversion is not clawed back and does not go
  negative. BL-849 proved this deliberately, with the marketplace floor switched off:
  *"available is floored at zero, never negative."*
* **The write side is what the conversion must add.** The poster's reduced figure is CLAMPED at his
  `effectivePaid` on that campaign and the clamp is stated on the owner's screen with all four figures
  (requested, effective, clamped, floor), which is BL-866's shape.
* **A position already below its floor is REFUSED, not deepened**, with every proposal stripped from
  the response.
* **The cost of getting this wrong is measured, not hypothetical:** BL-826's 40 clips, $140.54 pushed to
  $25.65 against $78.54 paid, Mark Paid jammed at $0.00 against `payout_amount_positive`, **five
  identical permanent failures**.

**VERDICT: HOLDS ONLY IF THE CONVERSION IS BUILT AS SPECIFIED. This is the one place in the design where
a careless build round produces BL-826 again.**

### 7.4 BL-538: earnings never decrease

**How it is threatened.** Three v2 paths can decrease a recorded figure: the conversion, a devaluation
applied to a v2 clip, and a budget scale-down at approval.

**How the design preserves it.** The poster's leg passes `src/lib/earnings-never-decrease.ts`, in
committed code, which BL-538 put there after BL-528 found the guard living only in an uncommitted
script. A decrease requires an explicit `allowDecrease: true`, and **blocked writes surface in the
response and in the audit, never silently**.

**THE GAP, AND IT IS NEW: that guard protects `Clip.earnings` and nothing else.** The editor's leg and
the platform leg have no such guard, and neither does the existing marketplace's equivalent
(BL-841 item 14). **Requirement: the v2 editor earning needs its own never-decrease guard and its own
audit, or the 45 percent that belongs to the person who did the creative work is the least protected
money on the platform.**

**VERDICT: HOLDS for the poster's leg today. DOES NOT HOLD for the editor's leg unless built.**

### 7.5 BL-539: a stamp-versus-share mismatch creates permanently ambiguous rows

**Measured once at $933.94** (BL-539, confirmed by BL-570 and BL-627 risk 5: *"somesome stamp-vs-share:
179 of 726 owner rows disagree by more than 0.02"*, frozen deliberately because re-deriving would cost
the owner).

**How it is threatened.** Three parties instead of two means three stamps that can disagree with three
shares, and the ambiguity surface grows rather than adds.

**How the design preserves it, and it is cheap.** The platform leg is a **RESIDUAL**, never an
independent multiplication:
`platformBase = round2(round2(gross)) - editorBase - posterBase` (PART 1.2). The three legs then sum to
`round2(gross)` at every price including sub-cent boundaries, **by construction rather than by
agreement**, so there is no share for a stamp to disagree with. This is F-SEC-2A-FIX's shape
(`earnings-calc.ts:657-663`) applied to a third party.

**THE ONE PLACE IT IS STILL AT RISK: BL-866's devaluation.** Devaluing restamps the per-clip CPM pair
(`devaluedRatio`, `devaluedPrevClipper`, `devaluedPrevOwner`, `schema.prisma:1113-1117`) via
`decidePerClipCpmPair`, which is ratio-preserving **across two parties**. A v2 clip has three reading the
same pair. **Requirement: either exclude v2 clips from the devaluation path explicitly and say so on the
owner's screen, or extend `decidePerClipCpmPair` to preserve 45/45/10. Doing neither produces exactly the
ambiguous rows BL-539 measured, on a new surface.** BL-866's own warning applies with full force here:
*"Restamping is NOT retroactively inert... a CPM restamp reaches BL-826's destination one tick later,
through the sanctioned writer."*

**VERDICT: HOLDS for the ordinary path by construction. AT RISK on the devaluation path until a decision
is written down.**

### 7.6 A third party's cut is a STAMPED DEDUCTION ON THE PAYOUT ROW, never a rewrite of `Clip.earnings`

**Established by BL-834 and stated in `trainer-cut.ts:11-42`:** *"NOTHING IN THIS FILE, OR IN ANY FILE
THAT CALLS IT, MAY WRITE `Clip.earnings`, `Clip.baseEarnings` or `Clip.bonusAmount`... A percentage
applied to EARNINGS necessarily includes every dollar the clipper has already withdrawn and spent."*
**BL-826 proved the cost of breaking it**, quantified in 7.3.

**DOES THIS DESIGN VIOLATE IT? NO, AND THE DISTINCTION MATTERS MORE THAN THE ANSWER.**

The editor's 45 percent **is not a third party's cut**. It is a second party's own earning, created at
the same instant as the poster's, from the same gross, **before anybody can have been paid**. There is
nothing already withdrawn to re-rate. BL-841 drew this line for the existing marketplace and it is worth
quoting because it is the whole justification: *"The marketplace does not have that problem: it splits
at the moment the money is created, before anyone can have been paid, so there is nothing already
withdrawn to re-rate. The stamped shape was the right answer to a different question."*

**So v2 correctly follows the MARKETPLACE shape (split at creation) and not the TRAINER shape (stamp at
withdrawal), and the rule is satisfied rather than bypassed.**

**BUT THE CONVERSION ACTION SITS ON THE OTHER SIDE OF THAT LINE, AND THIS IS THE SHARPEST DISTINCTION IN
THE REPORT.** A conversion happens AFTER money may already have been paid. Half of it is a creation (the
editor's new row, safe, nothing paid on it) and half of it is a reduction of a figure that may already
have funded a withdrawal, which is exactly the situation the rule exists for. **So the conversion's
reduction half must carry the trainer path's discipline: a floor at money already paid, an explicit
audited decrease, a stated clamp, and an undo.** That is PART 3.10, and it is why that section is written
at payout length rather than feature length.

**VERDICT: HOLDS. The ordinary path is the right shape for the right reason; the conversion is the one
place the rule bites and it is designed for.**

### 7.7 The earnings invariant itself

`earnings = baseEarnings + bonusAmount` to within $0.01, enforced by `assertInvariant` inside
`writeClipEarnings` and by the L2 middleware (`clip-earnings-invariant-middleware.ts`). BL-627 measured
it holding on 2,748 of 2,748 live approved clips with a net drift of **minus one cent**, collectively
under-credited.

**On a v2 clip it is unchanged for the poster's leg**, because that leg goes through the same writer
with the same fields. **It has no counterpart on the editor's leg**, where `amount`, `baseAmount` and
`bonusAmount` are three unguarded floats on a table no middleware watches. BL-841 item 14 already found
the failure mode on the existing twin: *"Freeze zeroes `baseAmount` and `bonusAmount`; restore puts back
only `amount`"*, producing a row reading `amount = X, base = 0` until the next tick healed it.

**Requirement: the same invariant, asserted on the editor's row, in the same transaction.** It is three
lines and it is the difference between the editor's money being guarded and merely being stored.

### 7.8 The six money files

**Untouched by this round, and the build rounds should expect to touch at most two.**
`clip-earnings-writer.ts` and `earnings-calc.ts` are the only two a correct v2 build has any reason to
open, and `earnings-calc.ts` should gain a **twin function beside** `calculateMarketplaceEarnings`
rather than any change to it. **`tracking.ts` must not appear in a v2 diff except where a v2 clip's tick
is handled, and if it does appear the round must justify it line by line.** `balance.ts`,
`money-decimal.ts` and `clip-earnings-invariant-middleware.ts` need no v2 change except the single
`spent` term in 7.1.

---

## PART 8 — THE OPEN QUESTIONS, WHICH ARE THIS ROUND'S REAL OUTPUT

**NONE OF THESE IS ANSWERED HERE, AND NO POLICY THE OWNER HAS NOT STATED IS INVENTED ANYWHERE IN THIS
REPORT.** Where a question has a measured fact attached, the fact is given so the decision is cheap. The
decision is still his. Ranked: the ones that change the whole design first.

### TIER 1 — these change the shape of the thing. Answer these before a line is written.

**1. Does the owner's 10 percent REPLACE his ordinary cut, or ADD to it?**
Options and what each earns him per $100 of gross on a CPM_SPLIT campaign at a 33.33 percent owner
share, both earners standard:
* **REPLACES**, which is what the existing marketplace does (`tracking.ts:2047`, `review/route.ts:520`,
  no `AgencyEarning` row is written for a marketplace clip): **he nets $18.10** and the campaign spends
  $100.00.
* **ADDS**: **he nets $51.43** and the campaign spends $133.33 for the same views.
Consequence: this is one boolean in the build and it must be written down beside the branch. Adding does
not move money from the earners to him, it makes the campaign pay more per view.

**2. Is the concentration intended? One editor can take 45 percent of an entire campaign budget from one
clip.**
Worked in PART 1.6: a $5,000 campaign, one clip, fifty posts of 100,000 views each, and the editor takes
**$2,250 gross / $2,047.50 cash** for one piece of work made once.
Options: intended and celebrated; intended but capped; not intended.

**3. What caps a single popular clip, if anything?**
Measured: the campaign budget caps the TOTAL and **nothing caps the concentration or the speed**.
`maxClipsPerUserPerDay` is per user per day and does not reach. The nearest existing thing, the Y2 cap
`maxEarningsPerCreatorUsd` (`clip-earnings-writer.ts:507-535`, BL-299), lives on a marketplace LISTING
and v2 has no listing.
Options: (a) a hard limit on posts per approved clip; (b) a per-editor share-of-budget cap, a Y2
equivalent; (c) a per-editor per-campaign dollar cap; (d) nothing, the budget is the only limit.

**4. May an editor also post his own clip and take both cuts, 90 percent of one post?**
Consequence: PART 7.2 shows this is not a double payment and is safe, **provided the two aggregates are
summed additively rather than one derived from the other**. If it is forbidden, the forbidding is one
check. If it is allowed, it is the case most likely to be tried first and the balance derivation must be
proven on it before launch.

**5. Strikes, the conversion, or both?**
This report recommends **both, conversion first and the strike reserved for a repeat**, and gives the
reasoning in PART 3.10. **The choice is left open.** Sub-question: must a conversion have happened, and
been explained to the person, before a strike may be issued at all?

**6. Does a MARKETPLACE ONLY campaign forbid editors from POSTING entirely, or only from posting their
OWN work?**
Three readings, and they produce three different products:
* an editor may never post on that campaign at all;
* an editor may post any clip except his own;
* an editor may post anything, the role is not exclusive and "editor" is just what he did last.
Consequence: this decides whether "editor" and "poster" are ROLES on a user or simply two things any
clipper can do. **That is a data-model decision disguised as a policy one, which is why it is in tier 1.**

### TIER 2 — these change money or a rule, but not the architecture.

**7. Confirm the split order: 45/45/10 on the gross.**
**This one has an arithmetic answer and the report asks only that he confirm it.** Both readings produce
IDENTICAL cents whenever the second is definable (PART 1.1: $40.95 / $40.95 / $18.10 either way), and the
"fee first" reading becomes undefined the moment the two earners are on different fee rates, because the
fee belongs to the withdrawing user and not to the clip.

**8. Is a v2 clip meant to carry TWO bonus stacks? He has not addressed this and it is a real per-view
cost.**
Measured shape (`earnings-calc.ts:667-668` on the existing twin): each party's bonus is computed against
their own profile and added ON TOP of their share, and the platform's leg gets none. At a 10 percent
editor bonus and a 5 percent poster bonus, a $100 gross clip disburses **$106.75** and his slice falls
from 10 percent to **9.37 percent** of what actually leaves the budget.
Options: both stacks (as today, and as the existing marketplace already does); one stack, on the poster
only; one stack, split; no bonuses on v2 clips at all.

**9. Is the editor's 45 percent forever, or time-limited?**
Options: forever, for as long as any post of that clip earns; a fixed window from approval; until the
campaign ends; until the editor leaves the platform.
Consequence: a forever cut means a single good clip is an annuity, which may be exactly what he wants or
exactly what he does not.

**10. What happens to the editor's cut when a POST is rejected?**
Options: the editor's row for that post is deleted with the poster's, atomically, which is what the
existing marketplace does on reject and undo; the editor keeps it because the fault was the poster's;
the editor keeps it only if the rejection reason is poster-side.
Consequence: option two means a poster can be rejected and the editor still paid out of the budget, which
is defensible and is new behaviour on this platform.

**11. May a poster post the same clip to several of HIS OWN accounts?**
Measured: today nothing stops it. Fifty posts from fifty accounts and five posts from one person's five
accounts look identical to every duplicate gate, because each post has its own live URL (PART 2.6).
Consequence: this is one unique index, `[v2ClipId, clipAccountId]`, and the answer decides whether it
exists. **Do not build `[v2ClipId, posterId]`, which would pre-empt the answer.**

**12. What happens to money already PAID to a thief when a clip is converted?**
BL-824 is absolute: paid money is final and may not be clawed back or offset. So the honest options are
the three in PART 3.10: forward only; the platform covers the gap out of its own cut; or whatever the paid
floor frees goes to the editor and no more.

**13. Does a v2 clip participate in BL-866's devaluation at all?**
Measured risk in PART 7.5: `decidePerClipCpmPair` is ratio-preserving across TWO parties and a v2 clip
has three reading the same pair.
Options: exclude v2 clips explicitly and say so on the owner's screen; extend the pair logic to preserve
45/45/10; leave it and accept BL-539's ambiguous rows, which is the one option this report would argue
against.

**14. What happens to a campaign whose TYPE is changed by the owner while clips are in flight?**
Options: the change applies only to new submissions; it applies to everything including pending ones; or
the type is immutable once a campaign has clips.

### TIER 3 — product decisions the build needs but which do not change the money.

**15. Drive only, or an on-site preview?** PART 5 prices both. He is leaning toward Drive.
**16. Does the editor see WHICH posters posted his clip, or only a count?** Both arguments are in PART 5.
**17. Does an APPROVED clip ever expire from the catalogue,** or can it be posted indefinitely?
**18. Is there a cap on how many submissions an editor may have PENDING at once?**
**19. How long is the strike window** before a strike stops counting? The existing marketplace uses 30
days, but **its decay cron has never run**, so there is no lived precedent on this platform.
**20. Is a resubmitted clip a NEW row or a revision of the rejected one?** This decides whether the owner
sees the history of attempts.
**21. Does the editor see which CAMPAIGN a clip is for, and under what name?** `clientName` must never be
shown (CLAUDE.md), but the campaign's public name may be fine.
**22. Is "Total earnings" on the editor's dashboard accrued or already paid?** This changes the word on
the tile from "Earned" to "Available" and they mean different things.
**23. Should MARKETPLACE ONLY also block the OWNER OVERRIDE submit path?** `owner-submit-core.ts:65-115`
has no campaign-status gate at all today, unlike the clipper path. This report's view is that it should
not be gated, because the owner blocking himself helps nobody.
**24. Does the 30 minute posting window apply to v2?** `MAX_CLIP_AGE_LABEL` is "30 minutes"
(`src/lib/clip-config.ts:13-20`), and BL-841 measured that once it closes the same URL is refused
**permanently**. **A poster who leaves for Drive, downloads 30MB, posts and comes back an hour later
would be refused with no warning anywhere in the flow.** If it applies, the countdown has to be visible
BEFORE he leaves for Drive. **This is the single most likely thing to make v2 feel broken on day one.**
**25. May a poster see an aggregate such as "posted 6 times so far"?** It is not one person's money, but
it is another user's activity, and it turns a no-pressure surface into a scarcity one.
**26. Should the editor's approval and rejection notifications use the SAME type strings as an ordinary
clip decision?** He asked for the same shape, and reusing `"CLIP_APPROVED"` and `"CLIP_REJECTED"` gives
exactly that, at the cost of being indistinguishable in his feed. Either way the **deep link needs a v2
destination**: both types route to `/clips` today (`notif-href.ts:133-140`), which is wrong for an editor.
**27. May an ADMIN see the editor approval queue at all**, not merely be blocked from its money figures?
The existing marketplace admin dashboard is hard gated `role !== "OWNER" -> notFound()`
(`marketplace/admin/page.tsx:21-22`), and the brief names only the owner.

---

## PART 9 — THE BUILD PLAN

### How many rounds, honestly

**Eight rounds minimum, and ten is the realistic number once merges are counted.** That is not padding.
**BL-798 and BL-843 both ran out of session room on smaller work than this**, and this design adds four
Prisma models, roughly a dozen routes, three new user-facing surfaces, a money writer, a conversion
action and a penalty system, in a codebase where the money path has needed three successive rounds to
close one strike hole.

**The ordering rule applied throughout: after every round, the system is in a state that could stay that
way forever without being broken or half-built.** Each round below states what is true if the owner stops
there.

### The rounds

**ROUND 1 — THE FOUNDATION, AND IT IS DELIBERATELY INERT.**
Additive nullable schema only: the four v2 models, the `marketplaceV2PostId` column on `Clip`, and the
campaign type field defaulting to the value that keeps every existing campaign identical. Plus **the one
line in `balance.ts:487-497` that adds the two v2 aggregates to `spent`.**
*Why the riskiest line ships first:* with zero v2 rows, `SUM` over the new tables is provably `0`, so the
change is a demonstrable no-op and can be proven by the aggregate being byte-identical before and after.
**Shipping it later, with money already flowing, is how PART 7.1 becomes a real defect.**
*If you stop here:* nothing changed. No surface, no route, no behaviour. Every existing campaign, clip
and payout is untouched.

**ROUND 2 — THE EDITOR SUBMITS AND THE OWNER DECIDES. NO MONEY MOVES.**
The editor submission form and route, the owner's approval queue, approve and reject with the owner's
verbatim reason, and the two notifications matching the ordinary clip decision shape exactly. Gated to
test users.
*If you stop here:* editors can submit and the owner can approve. An approved clip sits in a catalogue
nobody can post from. Nothing earns. No money code has been touched.

**ROUND 3 — THE MONEY WRITER, BUILT AND PROVEN, AND UNREACHABLE.**
The 45/45/10 twin beside `calculateMarketplaceEarnings`, the v2 earnings writer that calls
`writeClipEarnings` for the poster leg and writes the other two legs in the same transaction, the
invariant assertion on the editor row, and the never-decrease guard on it.
Proven in the sandbox harness the marketplace rounds already use: every row prefixed, ledgered, torn down
by primary key, with a closing census equal to the opening one. **No production route calls it.**
*If you stop here:* a tested money path exists that nothing can reach.

**ROUND 4 — THE POSTER POSTS, TEST USERS ONLY. THIS IS THE FIRST ROUND WHERE MONEY MOVES.**
The browse grid, the three states in words, skip and unskip, the post route, and the unique index applied
with `CREATE UNIQUE INDEX CONCURRENTLY` as its own single statement and verified in `pg_indexes` rather
than in the schema file.
*If you stop here:* the whole loop works for test users and is invisible to everybody else.

**ROUND 5 — THE CAMPAIGN TYPES.**
The type on the campaign form, the gates on the two normal submit entry points via the single chokepoint
in `processClipperSubmitLink`, the refusal copy, and the badges that tell a clipper which flow he is in
before he starts work.
*If you stop here:* campaigns can be typed and the rules are enforced, still behind the test-user gate.

**ROUND 6 — THE THUMBNAILS AND THE POLISH, THEN THE FLAG FLIP.**
The thumbnail path with its failure fallback, the accessibility requirements applied, the mobile pass at
375px, and only then the flag that opens it to real editors and posters.
*If you stop here:* the product is live and complete for its stated purpose. **Everything after this is a
remedy for a problem that has not happened yet, which is why it comes after.**

**ROUND 7 — THE EDITOR'S REPORT AND THE OWNER'S EYE.**
The editor's "this is my clip" button, the owner's side-by-side surface for judging it, and the evidence
queue. Reads and lists only. **Nothing auto-acts and nothing penalises.**
*If you stop here:* the owner can see suspected theft and has no lever yet. That is a strictly better
position than today and it is safe to sit in indefinitely.

**ROUND 8 — THE CONVERSION ACTION.**
Built at payout length: the paid floor, the stated clamp with all four figures, the explicit audited
decrease, the blast-radius preview produced by the code that executes, one Serializable transaction, one
audit row, and an undo. Owner only, never automatic.
*If you stop here:* the owner can make an editor whole. There is no penalty system, which is a deliberate
and defensible place to stop.

**ROUND 9 — THE STRIKE SYSTEM, LAST, AND ON PURPOSE.**
One creation site, owner only, evidence required, ban derived live from rows, expiry derived at read
time, revocable, enforced at the one chokepoint. **It is last because three rounds in a row have each
found the previous round's strike fix wrong, and because a penalty built before the remedy is a penalty
built before anyone knows what the real failure mode looks like.**

**ROUND 10 — THE MERGE AND THE PROOF.**
The population measured, the invariants re-proven across the live set, the six money files verified
byte-identical by blob OID, and the whole thing recorded.

### Two things to recommend against

**Do not build content fingerprinting, hashing or any automatic theft detector.** BL-871 priced four
options and recommended against all four; BL-771 measured the best computable signal on this platform at
20.2 percent precision against a requirement above 99.2 percent. **The owner has already paid for this
answer twice and it has not changed.**

**Do not build a "poster who never posted" list for v2.** It is BL-871's own recommendation and it is the
right one for the EXISTING marketplace, where a submission is addressed to one person. **In v2 nobody
accepts anything and not posting is the normal case for almost every poster and every clip, so that list
would be a list of innocent people.** This is the one prior recommendation that does not carry over, and
the build round that assumes it does will waste a round and produce a queue nobody can use.

---

## RECONCILED, NOT AVERAGED

Fourteen subagents ran on different areas and four of their findings are **corrected** here rather than
repeated:

1. **The duplicate check.** A subagent proposed three schemes for letting v2 allow duplicates, each with a
   new `allowContentReuseV2` flag or a version branch. **All three are unnecessary.** Fifty posters
   produce fifty different live URLs, so every `normalizedUrl` gate passes naturally (PART 2.6). Each of
   those schemes would have added a switch that a later round could flip the wrong way.
2. **BL-866's devaluation.** A subagent described it as multiplying `clip.earnings`, `clip.baseEarnings`
   and `clip.bonusAmount` permanently. **That is the shape BL-826 broke and BL-866 explicitly rejected.**
   BL-866 restamps the per-clip CPM pair, ratio-preserving, and clamps at a floor equal to money already
   paid (PART 1.4, item 6).
3. **The campaign-type backfill.** A subagent recommended the right column and attached a one-time
   `UPDATE` for campaigns that already carry marketplace listings, flagging the row count as an
   unanswerable question. **No backfill is needed**, because the new field governs normal versus v2 only
   and the existing marketplace stays governed by its listing rows (PART 3.2). One fewer open question.
4. **The "colour carries nothing" citation.** A subagent believed the brief had misattributed it and that
   the sentence lives in BL-827. **The brief is correct.** BL-864's report carries it at line 35 with the
   1.44:1 measurement; BL-827 records the same fact independently at `BACKLOG.md:22268`. Both are true.

**And one thing this report corrects about a PRIOR ROUND'S recommendation, which matters more than any of
the four above.** BL-871's reframe, *"the theft case and the poster who never posts are the same event"*,
is right for the existing marketplace and **does not carry over to v2**, because nobody accepts anything
in v2 and not posting is the normal case. A build round that inherits that recommendation will produce a
list of innocent people. **PART 3.8 states it; PART 9 recommends against building it.**

---

## SAFETY

| | |
|---|---|
| changes made | **none.** No code, schema, data or config. Nothing created, nothing deleted. The only file added is this report |
| database connections | **ZERO, by this round and by all fourteen subagents.** The cap was stated before any work began and no figure here needed a live read |
| requests | every file operation a read. No POST, no PATCH, no DELETE, no vendor call, no Apify actor, no HikerAPI call, no Drive call |
| vendor spend | **$0.00** |
| money | no clip, payout, earning, campaign or user created, modified or deleted. The six money files were READ and not edited |
| the existing 60/30/10 marketplace | **provably unaffected. PART 2.5 lists what is shared and what is not**, by table, by flag and by route tree. Not one v2 row ever enters a `Marketplace*` table, `isMarketplaceClip` stays false on every v2 clip, and no route under `/api/marketplace/**` is called |
| the duplicate check | **not weakened anywhere.** PART 2.6 shows it does not need bypassing, so nothing is bypassed and no flag is introduced |
| the strike system | **specified as HUMAN ISSUED ONLY**, one creation site, never a cron, never a count, never a fetch result, with `grep -c` = 1 named as a test |
| the conversion action | **specified at payout length**, with the paid floor, the stated clamp, the explicit audited decrease, the blast-radius preview and the undo |
| build | **not run, and none is claimed.** A markdown-only diff cannot change `tsc` |
| handles and wallets | no handle printed, no wallet address read or printed |
| timestamps | none read from the database, so none to cast. Every quoted figure is attributed to the report that measured it |
| counting | every count from a `grep -c` or a prior report's `COUNT(*)`, never from a count piped through `head` |
| worktree `C:\w\bl876` | **removed at the end and verified by listing the path** |

### MEASURED VERSUS STRUCTURAL

**Measured this round, from source:** the split arithmetic in `earnings-calc.ts:584-691`; the deduction
stack in `payout-calc.ts:93-129`; the trainer base rule quoted from `trainer-cut.ts`'s own header; the L1
lock's spend read at `clip-earnings-writer.ts:162-247`; the referrer base at
`payouts/[id]/review/route.ts:1004-1018`; the absence of any campaign type field across
`schema.prisma:596-825`; the six duplicate gates and both `Clip` indexes; the five strike creation sites;
the dual-name render at `admin/clips/page.tsx:2056-2070`; the three colour tokens at `globals.css:72-74`
and the two failing focus rings at `:480-501`; the absence of any dialog semantics in
`src/components/ui/modal.tsx`; the absence of `ffmpeg` and of any `driveFileId` column.

**Quoted from prior rounds, measured there and not re-measured here:** every population figure, every
dollar figure attributed to BL-539, BL-570, BL-627, BL-696, BL-763, BL-824, BL-826, BL-841, BL-845,
BL-847, BL-849, BL-863, BL-866, BL-868, BL-870, BL-871 and BL-874.

**Structural only, and labelled as such where it appears:** the fifty-posters worked example, which is an
illustration at chosen numbers and not a forecast; the 30MB clip size behind the bandwidth table; the
Supabase prices, taken from its published page and not from an invoice; and every statement about Google
Drive API behaviour, which is separated in PART 5.7 into what is documented, what is undocumented, and
what could not be verified.

**Helpers this report's own reasoning depends on were checked to read real values**, because a prior
round's proof passed on a helper returning zero for everyone: `calculateMarketplaceEarnings` was read in
full and its residual arithmetic traced by hand at three grosses; `getCampaignBudgetStatus`'s
participation in the L1 lock was traced to `clip-earnings-writer.ts:215-247` rather than assumed; and the
`isCpmSplit` branch was read at both of its sites rather than at one.

### WHAT COULD NOT BE DETERMINED

* The exact row-render line of `src/app/(app)/admin/campaigns/page.tsx`, which is 2,436 lines and was not
  read in full. It needs a type column and the line was not pinned.
* Whether `community/page.tsx` and `client/campaigns/page.tsx` need a campaign type badge. Both matched a
  campaign-listing grep and neither was opened.
* Everything in PART 5.7's final paragraph about Google Drive: the undocumented thumbnail and download
  endpoints, Range support, the download throttle threshold, Supabase CDN cache behaviour for this
  bucket, and whether `ffmpeg` can be built into this project's NIXPACKS image.
* Whether the existing marketplace is still dormant. BL-841 measured zero submissions, zero posts and
  $0.00 ever moved, and six later rounds ran sandboxes against it and tore every row down, **but no live
  read was taken this round, by design**, so the current population is stated as unknown rather than
  assumed unchanged.
* The live value of `NEXT_PUBLIC_MARKETPLACE_ENABLED` and the `RAILWAY_NATIVE_CRON` allowlist, neither of
  which was read, both of which BL-841 also listed as undetermined.

**PERFORM NO FIX. NOTHING IN THIS ROUND WAS CHANGED.**
