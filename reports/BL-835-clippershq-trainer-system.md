# BL-835: the trainer system, built

**2026-09-04 · DB `now()` = `2026-09-04 13:55:17.50755+00` (first read) to the last read recorded below · BUILD AND MERGE.**
Base `origin/main` @ `fdce6afd`. Branch `checkpoint/BL-835`. Isolated worktree `C:/w835`, a short path, `node_modules` never junctioned, **removed at the end**. Every database read through `scripts/run-select.js` or a read-only Prisma call; every timestamp cast `::text` against DB `now()`. Handles redacted; no wallet address read or printed.

BL-834 designed this and the owner answered every open question. This is the build, as he decided it, with the design not reopened.

---

## THE SHORT VERSION

**A TRAINER is a clipper the OWNER promotes, and their code IS their username.** A clipper types it, reads the trainer's pitch document, ticks a box, and from that moment the trainer takes **10 percent of what the clipper receives after the platform's nine points**, on clips posted from then on. The trainer pays the ordinary payout fee on their own share when they withdraw it.

**THE MONEY SHAPE IS THE WHOLE POINT AND IT IS NOT THE OBVIOUS ONE.** The cut is a **fourth stamped deduction on the payout row**, and `Clip.earnings` is never touched by any trainer code path. Three prior rounds paid for that lesson: BL-716 reduced a clipper's record by $60.47 and needed a manual repair, BL-824 spent a whole round encoding "recorded earnings may never fall below money already paid" for seven clippers, and BL-827 breached the same property again through a payout adjustment that scaled 40 clips.

**EIGHT THINGS IN THIS ROUND WERE NOT IN THE BRIEF AND EACH ONE WOULD HAVE BEEN A DEFECT.** They are the substance of the round and they are listed here rather than buried:

1. The owner's two sentences about the base **only agree under one reading**, and the reading is now written into the code: the base is the gross less **nine points**, so the trainer's base is $91 on $100 whether or not the clipper is referred.
2. The existing **5 percent referrer would have silently lost money** because their invitee chose a coach. They are held harmless.
3. **Two money gates would have been LOOSENED** by a smaller `finalAmount`, including BL-827's own below-paid guard.
4. **Every trained clipper's payout email would have said "This was adjusted before sending"** on a payout nobody adjusted.
5. Eligibility read from `createdAt` alone would have **misjudged every backdated owner-override clip**.
6. The accessibility review caught a **status-naming trap in this round's own design** that inverts the money.
7. The consent copy's headline was **arithmetically false**: "10 percent of what you receive" is $8.19, not $9.10.
8. The guard demo **caught a guard that could not fail**, and it was tightened before it was trusted.

---

## PART 1: THE MONEY PATH

### 1.1 The shape, and why it is the only one

`finalAmount = amount − feeAmount − expressFeeAmount − trainerCutAmount`

Four columns are added to `payout_requests` and they are the entire money footprint of the feature on that row: `trainerCutPercent`, `trainerCutAmount`, `trainerRelationshipId`, `trainerEligibleGross`. All nullable, all NULL on every row that has no trainer, so such a row is indistinguishable from a pre-BL-835 row.

**Nothing writes `Clip.earnings`, `Clip.baseEarnings` or `Clip.bonusAmount`.** Nothing imports `writeClipEarnings`. `tracking.ts` is not in the diff. That is asserted structurally, per file, by the guard suite, so a future edit cannot quietly change it.

The reason is worth restating because it is the difference between this feature and a repair round. A percentage applied to EARNINGS necessarily includes every dollar the clipper has already withdrawn and spent, because earnings are the only quantity the withdrawal gate reads and paid money has already been subtracted against them. A percentage applied to a WITHDRAWAL cannot: a payout row is written once, from a figure the clipper was shown before they pressed, and no trainer code path reads a historical payout to re-rate it. **Money already paid is untouchable by arithmetic rather than by care.**

The clipper's BALANCE is still consumed by the gross `amount` (`balance.ts` `clipperLiability = actualPaidAmount ?? amount`), which this deduction does not touch.

### 1.2 The base: nine points, and the owner's two sentences

The owner said two things about the base and they only agree under one reading:

> (A) "the trainer takes 10 percent of what the clipper receives AFTER THE PLATFORM FEE, never of the gross", with the worked example $1,000 at 9 percent leaves $910 and the trainer takes $91.
>
> (B) "the platform keeps 4 percent and the referrer takes 5, and the trainer then takes 10 percent of what remains."

(B) is the specific instruction for a referred clipper and it says the base is the gross less **nine** points: four to the platform and five to the referrer. (A) says the same for an unreferred clipper, where all nine are the platform's. So one rule satisfies both: **the base is the gross, less the platform fee, less any referrer share, and those two always sum to nine points.**

**The consequence is deliberate and it is stated on the record: the trainer's base is identical whether or not the clipper is referred.** A trainer does not earn more because their trainee happened to arrive through an invite link, and a referred clipper is not charged more than an unreferred one. Taking (A) literally for a referred clipper would have made the base $96 instead of $91 and handed the trainer 50 cents per $100 out of the clipper's pocket for a reason neither of them chose.

**Express is NOT in the base.** `TRAINER_BASE_INCLUDES_EXPRESS = false`, one switch, with the reason beside it: express is a 4 percent premium the CLIPPER chooses to buy their own money faster, and letting it shrink the trainer's earned share would charge the trainer for a service the clipper bought. That is BL-760's "picking the arithmetic that suits the payer" pointed the other way.

### 1.3 The worked examples, machine derived, every figure as gross AND cash

From `scripts/bl835-arithmetic.ts`, **28 checks, 0 failures**, exit 0. Not hand arithmetic: every figure below is printed by the shipped functions.

| case | GROSS requested | platform fee | express | eligible gross | trainer basis | TRAINER CUT gross | **CLIPPER CASH** | trainer fee 9% | **TRAINER CASH** | PLATFORM TAKE | cap bound |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **OWNER'S OWN EXAMPLE $1,000 standard 9%** | $1000.00 | $90.00 | $0.00 | $1000.00 | $910.00 | **$91.00** | **$819.00** | $8.19 | **$82.81** | $98.19 | no |
| $100 standard 9% | $100.00 | $9.00 | $0.00 | $100.00 | $91.00 | $9.10 | $81.90 | $0.82 | $8.28 | $9.82 | no |
| $100 standard 9% + express 4% | $100.00 | $9.00 | $4.00 | $100.00 | $91.00 | $9.10 | $77.90 | $0.82 | $8.28 | $13.82 | no |
| $100 **referred** 4% | $100.00 | $4.00 | $0.00 | $100.00 | $91.00 | $9.10 | $86.90 | $0.82 | $8.28 | $4.82 | no |
| $100 **referred** 4% + express 4% | $100.00 | $4.00 | $4.00 | $100.00 | $91.00 | $9.10 | $82.90 | $0.82 | $8.28 | $8.82 | no |
| $100 standard, HALF the earnings pre-join | $100.00 | $9.00 | $0.00 | $50.00 | $45.50 | $4.55 | $86.45 | $0.41 | $4.14 | $9.41 | no |
| $100 standard, ALL earnings pre-join | $100.00 | $9.00 | $0.00 | $0.00 | $0.00 | **$0.00** | $91.00 | $0.00 | $0.00 | $9.00 | no |
| $100 standard, lifetime cap binds | $100.00 | $9.00 | $0.00 | $5.00 | $4.55 | $0.46 | $90.54 | $0.04 | $0.42 | $9.04 | **YES** |
| $1,000 **referred** 4% + express 4%, half eligible | $1000.00 | $40.00 | $40.00 | $500.00 | $455.00 | $45.50 | $874.50 | $4.10 | $41.40 | $84.10 | no |

**The owner's own example, checked to the cent:** platform takes $90.00, leaves $910.00, trainer takes $91.00, clipper receives $819.00, trainer pays 9 percent on their own $91.00 which is $8.19, trainer receives $82.81 cash. Six assertions, all pass.

**The referrer case, checked to the cent:** the platform keeps 4 percent ($4.00), the referrer's five points are $5.00 of the base, what remains for the trainer's base is $91.00, the trainer takes $9.10, the referred clipper receives $86.90 cash, and **the trainer's base is identical to an unreferred clipper's**. The referrer still earns 5 percent of $96.00, which is $4.80, unchanged by the trainer.

**The platform's take never falls below today's**, asserted at every fee and speed combination:

| fee | express | platform take today | with a trainer | change |
|---|---|---|---|---|
| 9% | none | $9.00 | $9.82 | **+$0.82**, the trainer's own fee |
| 9% | 4% | $13.00 | $13.82 | **+$0.82** |
| 4% | none | $4.00 | $4.86 | **+$0.86** |
| 4% | 4% | $8.00 | $8.86 | **+$0.86** |

The platform's take rises in every case, by exactly the fee the trainer pays on their own withdrawal, and nothing is taken away from it.

### 1.4 How a withdrawal is split, since a payout is a dollar figure and not a set of clips

Two rules run, and both are stated because a single unexplained number on a money screen is how BL-812 happened.

**Pro rata** is the rule the clipper is told, because it is the honest and neutral one: the eligible share of a withdrawal is the eligible share of the earnings behind it. **A lifetime cap** is the safety: the running `eligibleGrossCharged` on the pairing can never exceed the in-window gross ever earned on it. Proven over twenty consecutive withdrawals: charged $300.00 of $300.00 eligible earned, never a cent past it, and the total cut equals 10 percent of the after-fee eligible gross charged to within a rounding cent.

### 1.5 The referrer is held harmless, which the brief did not ask for and the code demanded

The existing 5 percent commission's base is `actualPaidAmount ?? finalAmount ?? amount`. A fourth deduction inside `finalAmount` would have shrunk an inviter's earned money **from $4.80 to $4.30 per $100** because their invitee chose a coach, silently, with nobody told. A referrer's claim predates the trainer's, so the cut is added back at the mint. For every row written before this round and every row with no trainer, `trainerCutAmount` is null and the expression is byte-identical to before.

### 1.6 Two money gates would have been loosened, and are not

`campaignBudgetLiability` (aliased `payoutLiability`) returns `finalAmount`. A smaller `finalAmount` therefore makes two safety gates **more permissive**, by exactly the sum of trainer cuts on the campaign:

• the mark-paid balance gate in `payouts/[id]/review/route.ts`, and
• **BL-827's own below-paid guard** in `admin/payouts/[id]/adjust/route.ts`, which would have fired LESS often.

A trainer cut leaves the campaign budget exactly as the clipper's own cash does, because it goes to the trainer and not back to the platform, so the correct liability is `finalAmount + trainerCutAmount`. `payoutLiabilityWithTrainerCut` supplies it at both sites. **`balance.ts` is one of the six money files and is NOT edited**; the add-back wraps it from outside and both call sites are named in the guard suite.

### 1.7 The loudest silent failure, caught before it shipped

`email.ts:655` gates the itemised fee breakdown on `|requested − fee − xfee − amount| <= 0.01`. Without a fourth term that check fails by exactly the cut on **every** trained clipper's payout, the itemised table disappears platform wide, and each of them is told:

> This was adjusted before sending. Message us on Discord if it looks wrong.

on a payout nobody adjusted. The term is in. A row reading `Less trainer share (10%) to <name>` renders only when a share was actually taken, with the percentage **interpolated from the row and never a literal**, the same rule the platform fee line already follows because it is 9 for most people and 4 for a referred one.

---

## PART 2: WHICH CLIPS COUNT

`joinedAt` and `leftAt` are written once on the pairing row and never touched again. Eligibility is derived from the clip's own post time against them, and from nothing mutable.

**THE POST TIME IS `postedAt ?? createdAt` AND NOT `createdAt` ALONE.** `owner-submit-core.ts:284` writes `createdAt: postedAt` when the owner backdates an override submission, so on those rows `createdAt` is the backdated post time rather than the moment the row was made. Reading `createdAt` alone would be reading a figure that means two different things on two kinds of row. Both columns are written once at create and never updated, so the window is derived from immutable data on both sides.

**All four cases the owner named, proven, plus the boundaries and every other ending:**

| case | eligible? |
|---|---|
| a clip posted **BEFORE** joining | **no**, never, on any later withdrawal |
| a clip posted **DURING** | **yes** |
| a clip posted **AFTER** a good-terms exit | **no** |
| a clip posted **DURING**, seen after that exit | **yes**, still charged |
| a clip at exactly `joinedAt` | yes, the boundary is inclusive at the join |
| a clip at exactly `leftAt` | no, the boundary is exclusive at the leave |
| an in-window clip under `ENDED_OWNER_WINDDOWN` | **no**, accrual stopped |
| an in-window clip under `ENDED_BAD_FAITH` | **no** |
| an in-window clip under `ENDED_TRAINER_GONE` | **no** |

**And against real clip rows, read only, nothing written.** A real clipper with 732 approved clips totalling $1,710.85:

| hypothetical join moment | eligible | total |
|---|---|---|
| before every clip | $1,710.85 | $1,710.85 |
| at the median clip | $603.41 | $1,710.85 |
| after every clip | **$0.00** | $1,710.85 |

The total is identical in all three, so the split partitions the earnings and never invents any.

---

## PART 3: THE OWNER'S CONTROLS

### 3.1 Promoting, owner only, with a typed phrase

`POST /api/admin/trainers` with `action: "PROMOTE"`, gated by `requireOwner`, on BL-833's precedent that locked campaign creation to him. The refusal names the rule rather than saying "Forbidden": **"Only the owner can manage trainers."**

**The code IS the username, lowercased**, so a clipper types a name they already know rather than an 8-character random string, and it can never be confused with a referral code at an entry field. It lives in its own `trainerCode` column with its own unique index.

**A typed phrase is required: `NEW TRAINER`.** BL-833's own test for when one is needed is whether the action "changes what a clipper is paid", and making someone a trainer does exactly that. It shares no token with `FULL AUTHORITY`, `MOVE CLIPS` or `ANY CLIPPER`, so muscle memory from a different grant cannot carry the owner through, and neither word is a live caret command in Dragon or Windows Voice Access. It is forgiving on the way in (a dictated trailing full stop, wrong case and double spaces all pass) and exact on the way out.

The pitch link must be a full `https` address or it is refused, because a clipper is asked to read it before agreeing to give away money and a broken link is a broken promise.

### 3.2 Taking it back, and why that is not the same as ending a pairing

`action: "DEMOTE"` needs no phrase, because obstructing the safe direction is a defect rather than a safeguard, a rule stated in BL-788, BL-825 and BL-833 alike.

**DEMOTE DOES NOT END ANY PAIRING**, and that separation is deliberate. Taking trainer status away stops the person being found by new clippers and stops new cuts being minted, because every accrual read refuses a pairing whose trainer no longer holds the status. What happens to their existing trainees and their pending money is a **separate decision per pairing**, because ending a pairing for bad faith and merely retiring a trainer are different things and folding them together would decide one by doing the other. The response says how many pairings were left open so the owner is never unaware of them.

The trainer code is **kept** rather than cleared, because it is the record of what every existing pairing's `codeUsed` refers to and clearing it would leave old rows pointing at nothing.

### 3.3 Selective ending, at both granularities

`POST /api/admin/trainers/end` takes `relationshipIds: string[]`. **Pass every pairing a trainer holds and it is the whole trainer; pass any subset and it is those trainees only.** There is no separate "whole trainer" verb, because one verb over an explicit list of ids cannot accidentally take in a pairing the owner did not choose, and BL-732's archive cascade is what happens when a verb decides its own scope.

**THE ENDING-STATUS TRAP, CAUGHT BY THE ACCESSIBILITY REVIEW IN THIS ROUND'S OWN DESIGN.** The button reading "good terms" must persist **`ENDED_OWNER_WINDDOWN`**, and **`ENDED_GOOD_TERMS` is the appeal-allowed status that KEEPS accruing**. They are adjacent strings that differ by one word and they do opposite things to the money. An implementer matching the button's words to the status's words produces the opposite outcome, silently, on real money. It is a named `REVOKE_STATUS` map with the reason in its own comment, and the guard suite fails if a label ever picks a status string.

| outcome | status persisted | pending money | future accrual |
|---|---|---|---|
| **GOOD TERMS** (owner winds it down) | `ENDED_OWNER_WINDDOWN` | the **trainer keeps** it and can still cash out | stops completely |
| **BAD FAITH** | `ENDED_BAD_FAITH` | **wiped and refunded to the clipper** | stops completely |
| **TRAINER GONE** | `ENDED_TRAINER_GONE` | **wiped and refunded to the clipper** | stops completely |
| appeal ALLOWED (a different verb) | `ENDED_GOOD_TERMS` | the trainer keeps it | **continues on clips posted before `leftAt`** |

**MONEY ALREADY PAID TO A TRAINER IS FINAL IN EVERY CASE**, per BL-824. A commission in status `PAID` is never touched, never refunded and never clawed back, and every such row is named in the response rather than skipped quietly.

### 3.4 A refund is a real money movement, so it is handled like one

**Snapshot before any write.** Every pairing and every commission the call would touch is read first and returned to the caller, so the owner is deciding against the same rows the write will use. Only the ids he named are read.

**The exact rollback is computed and PRINTED BEFORE the write**, to the server log and into the response, by explicit id and never by predicate, so running it can only undo what this call did. A `preview: true` mode returns it and writes nothing at all, which is proven live: after a preview the pairing is still `ACTIVE`.

**`expectedCount` and unknown ids refuse the WHOLE call** with a 409, because a pairing that ended between the dialog opening and the press must not be swept in silently, and acting on the rest of a list would be acting on a list the owner never saw.

**Both outcomes carry a typed phrase carrying the amount:** `SETTLE <amount>` and `REFUND <amount>`. Gating only the destructive one teaches the owner that typing means danger, and he then reaches for the other button when he does not want to type. The amount is the one number he has not typed and cannot derive, so typing it proves he read the figure.

**No double pay, structurally.** One `TrainerRefund` per commission, and the unique constraint on `commissionId` IS the guarantee on that path, the same way `PayoutAdjustment.payoutRequestId` is on the adjustment path. Ending the same pairing twice is refused with `ALREADY_ENDED`.

**No overpayment, structurally.** A refund writes no earnings row, no balance row and no payout row. The withdrawal gate reads `Clip.earnings` and payout amounts, and this route writes neither, so BL-627's property is untouched by construction rather than by checking. The refund is a record of what is owed to the clipper, settled by hand, the same shape `owner_referral_payments` uses for money that moves outside the payout system.

### 3.5 The silent-or-departed trainer rule, and its exact trigger

**Automatic, and only on facts that cannot be argued with.** A pairing accrues nothing the moment its trainer is `BANNED`, soft deleted, or no longer holds `isTrainer`. Checked in two places: at payout request time, where the pairing is filtered out before any cut is computed, and again at mint time, where the pairing is re-read rather than trusted from request time. When the mint refuses, the cut the clipper already paid is **refunded to them** rather than kept by the platform, and a commission row in status `REFUNDED` is written first so the ledger keeps its shape and the owner's hub can explain every row.

**Silence itself is never auto-acted on.** BL-834 established that off-platform coaching leaves no trace, so a trainer who coached entirely on Discord and one who did nothing are indistinguishable in platform data. Acting automatically on that would take money from someone who earned it. The owner ends it, with the measurements in front of him.

---

## PART 4: THE THREE SURFACES

### 4.1 The clipper's consent screen, quoted in full

**The draft was wrong and the accessibility review caught it.** The headline read "10 percent of what you receive", which is **arithmetically false**: you receive $81.90 and 10 percent of that is $8.19, not $9.10. The cut is 10 percent of the base. That is BL-812's defect, a figure beside a label that did not produce it, in the one sentence a clipper is agreeing to. Two more corrections came with it: "the platform takes $9" is false for a referred clipper, for whom it is $4 platform plus a $5 referrer share; and "they will not see your wallet" was false **in effect**, because the trainer's dashboard shows what they earned from each trainee and $9.10 back-solves the payout exactly.

The shipped copy, from `src/lib/trainer-copy.ts`, every string in one place so the panel and the refusals cannot drift:

> ## Join [trainer name] as your trainer
>
> [trainer name] will coach you to get more views and earn more.
> In return, your trainer takes 10% of your pay after fees.
>
> **What it costs you**
> Your trainer's 10% is worked out on your pay after fees.
> Take a $100 withdrawal. $9 comes off for fees.
> Your trainer then takes $9.10. You receive $81.90.
> The platform fee itself does not change.
> An express withdrawal costs extra. It does not change your trainer's 10%.
>
> **What it applies to**
> Only clips you post after you join.
> Clips you posted before today are never counted.
> Money you have already been paid is never touched.
>
> **Leaving**
> Leaving is not automatic. You ask the owner and the owner decides.
> Say why you want to leave and send anything that backs it up.
> Even if the owner lets you leave, you keep paying 10% on the clips you already posted.
> The owner can also end it. Then your 10% stops.
> You keep clipping the whole time you wait.
>
> **What your trainer will see**
> Your name and the day you joined.
> Every clip you post from now on, and whether it was approved or rejected.
> The reason for any rejection.
> What they earned from you.
> They will not see your email or anything from before today.
>
> ☐ I understand that my trainer takes 10% of my pay after fees.
>
> [ Join ]  [ Cancel ]

**The sentence the review insisted on is the most important one on the panel:** *"Even if the owner lets you leave, you keep paying 10% on the clips you already posted."* It is true, because `ENDED_GOOD_TERMS` is the one ending inside `STATUSES_THAT_KEEP_ACCRUING`. Without it a clipper consents believing a successful appeal ends the deduction, which is not what happens. **That is a money-truth defect rather than an interaction defect, and none of the earlier drafts had it.**

Measured: longest sentence **18 words** against a ceiling of 20, estimated Flesch-Kincaid grade **4.2** against a ceiling of 6.0, no dashes as bullets, no emoji. The guard suite asserts the word ceiling, the four load-bearing claims and the absence of dashes and emoji, so the copy cannot regress silently.

One residual simplification is flagged rather than hidden: "after fees" describes a base that, for a referred clipper, is the gross less a 4 percent platform fee **plus** a 5 point notional referrer share, and calling that 5 a "fee" is a simplification. It is far more accurate than "what you receive", the clipper sees $9 leave either way, and the figures hold for everyone.

### 4.2 The trainer's dashboard, and its hard boundary

`/trainer` and `GET /api/trainer/dashboard`, visible only to a holder of trainer status, read from the DB row and never from the session token because the token is stale right after login.

**The select lists are EXHAUSTIVE and they ARE the enforcement**, with no `include`, no spread and no rest, so a column added to a model later cannot arrive here by accident. Pairings return `id, traineeId, joinedAt, leftAt, status, traineeUsernameAtJoin, trainee.username`. Clips return seven leaves: `id, clipUrl, status, rejectionReason, postedAt, createdAt, clipAccount.platform`. Money is a `groupBy` over `trainer_commissions` where `trainerId` is the caller.

**NOTHING FROM BEFORE THE JOIN MOMENT**, judged by the same `isClipEligibleForTrainerCut` the payout path calls rather than a copy of it. **Nothing about a clipper who is not theirs:** a `traineeIds` parameter naming someone else's trainee is filtered out of an already-scoped list, so it is dropped in silence and cannot be used to probe who trains whom. **The trainee's user id is never selected at all**, so it cannot reach the response through a mapping step; clips are read one trainee at a time with the id in the `where` clause only.

`FLAGGED` is masked to `PENDING` through `clipperStatus`, so no clipper can see machine suspicion about another.

**Proven by grep over the real response bytes: 0 of 25 forbidden field names present**, including `ownerCpm`, `agencyFee`, `lockedOwnerShareDecimal`, `clientName`, `aiKnowledge`, `budget`, `campaignId`, `fraudScore`, `payoutReductionRatio`, `walletAddress`, `email`, `discordUsername`, `referredById`, `totalEarnings`, `baseEarnings` and `bonusAmount`. **No campaign name of any kind**, because campaign names on this platform carry the rate inside the name and the name IS owner economics. The same grep over the route file is clean case-insensitively including in its comments.

The clip URL is a **link and never printed as text**, because a TikTok or Instagram address contains the `@handle`.

### 4.3 The owner's hub

`/admin/trainers`, narrowed to OWNER with `notFound()` because the `/admin` layout admits ADMIN and REVIEWER too. It shows every trainer with their code and pitch, every pairing grouped by trainer and multi-selectable, the appeals queue, and the refunds ledger with what is still unsettled. Money per pairing is keyed by status and never blended into one figure, because what is `AVAILABLE` can still be refunded and what is `PAID` cannot, and blending them hides the only distinction that matters.

---

## PART 5: THE FAILURE CASES, BY DIRECT REQUEST

`scripts/bl835-live-proof.ts`, **49 checks, 0 failures**, exit 0, against a running server with real minted `__Secure-authjs.session-token` sessions and the dev-auth bypass **OFF**, because a bypass session carries an empty capability list and every assertion would then pass for the wrong reason. A sanity check asserts the minted session actually resolves to the fixture before anything else runs.

| the case | what the platform does | proven |
|---|---|---|
| a code that does not exist | `TRAINER_CODE_UNKNOWN` | 400 |
| a clipper enters their own code, which is also the same-person case | `TRAINER_IS_SELF` | 400 |
| joining without ticking the box | `CONSENT_REQUIRED`, refused **by the server** | 400 |
| a valid join, code matched case-insensitively | pairing created | 200 |
| a second trainer's code while already trained | `TRAINER_ALREADY_SET` | 409, and the database holds exactly one `ACTIVE` row |
| a banned trainer | cannot be found by their code at all | `TRAINER_CODE_UNKNOWN` |
| a banned clipper | refused before any trainer logic runs | **401**, stricter than expected |
| a clipper who stops clipping, or never withdraws | nothing happens and nothing expires | 0 commission rows |
| a clipper decides their own appeal | refused | 403 |
| a clipper ends their own pairing | refused | 403 |
| a trainer loads the owner hub | refused | 403 |
| a non-trainer loads the trainer dashboard | refused | 403 |
| a signed-out request to either | refused | 401 |

**One assertion was wrong and the platform was right.** A banned clipper returns **401**, not the 403 the test expected, because a banned account's session does not resolve at all so the request never reaches a role check. That is stricter than asserted, and the assertion was corrected to match rather than the code.

**The appeal, which is the only way out:** an appeal with no real reason is refused; a clipper can ask; a second open appeal is refused rather than queued twice; the owner can refuse and **the pairing stays live with no leave moment stamped**; the owner can allow and it becomes `ENDED_GOOD_TERMS` with `leftAt` stamped, which is the one ending that keeps paying on clips already posted.

**The owner ending a pairing:** preview writes nothing and names the rollback; ending without the phrase changes nothing and names the phrase; a changed list is refused with `EXPECTED_SET_CHANGED`; an unknown id refuses the whole call; with the phrase and the right count it goes through; the second attempt is refused with `ALREADY_ENDED`.

**A payout in flight when an ending lands, and a trainer ended mid-payout,** are the same mechanism and it is stated rather than tested with real money: the cut is **stamped on the payout row at creation** and a stamped figure is never recomputed, so the clipper receives exactly the cash they were shown. At mint time the pairing is re-read; if it has been ended for bad faith or the trainer is gone, **no commission is minted and the cut is refunded to the clipper**, through the same ledger a bad-faith ending uses. Nothing is left in an ambiguous state, which is the thing BL-539 measured at $933.94 to untangle.

**The withdrawal route is unbroken for everyone who has no trainer**, which is currently every single person, and that is the highest-risk untested path in the round. `scripts/bl835-payout-regression.ts`, **6 checks, 0 failures**: a well-formed request travels all the way through the trainer resolution, the breakdown, the guard and the method check and is refused by the ordinary balance gate with *"You have $0.00 available on this campaign right now"*, with no trainer wording anywhere in a refusal that has nothing to do with one. The express path likewise. **212 payout rows before, 212 after: no payout was created by any of it.**

---

## PART 6: THE FIVE INVARIANTS, AND THE GUARD SEEN TO FAIL

### 6.1 Each invariant, and how the design preserves it

**BL-627, nobody can withdraw more than they earned.** The gate is `available = max(earned − paidOut − locked, 0)`, derived on every read, with `effectiveCap = min(available, globalAvailable)`. Its inputs are `Clip.earnings` and `payout_requests.amount`. **The trainer path writes neither.** The cut reduces `finalAmount`, which the gate never reads. On the trainer's own side the same property holds: they can only withdraw against `AVAILABLE` credit rows, each minted from a payout that already completed, each flipped to `PAID` inside the withdrawal transaction.

**BL-696, nobody can be paid twice.** `@@unique([sourcePayoutRequestId])` on `trainer_commissions` makes a duplicate mint a P2002, swallowed as the idempotent re-PAID flow exactly as the referral mint does. `@@unique([commissionId])` on `trainer_refunds` makes a duplicate refund impossible. Ending the same pairing twice is refused. **The honest limit is named:** a trainer's cashout would carry `campaignId = null`, and `uq_payout_open_per_user_campaign` is a partial btree unique that treats NULLs as distinct, so it does not constrain such a row. That is already true of the referral cashout and BL-696 named it; it is bounded in practice because a first request consumes every `AVAILABLE` row, but the bound is a consequence of the ledger rather than a database guarantee.

**BL-824, recorded earnings may never fall below money already paid.** The rule is `min(paidGross, payableEarnings)` per campaign in `balance.ts`. `paidGross` reads `amount`, which is the GROSS and is unreduced by the cut; `payableEarnings` reads `Clip.earnings`, which the trainer path never writes. **Both inputs are untouched, so the quantity the rule protects cannot move.**

**BL-538, never decrease.** `decideNeverDecrease` and `capButNeverBelowStored` have exactly their existing callers. The trainer path calls none of them because it computes no clip earnings. `tracking.ts` is byte-identical.

**BL-539 and BL-570, no stamp-versus-share ambiguity.** The trainer rate is stamped on a write-once payout row and **has no live counterpart to disagree with**. The reason somesome's 108 rows are permanently ambiguous, at a measured $933.94, is that a per-row stamp disagreed with a live campaign constant and no data could pick between them. A stamp with nothing to disagree with cannot become ambiguous. Two corollaries are honoured: the stamped percent is read back and never re-derived on any screen or email, and the commission row carries its own `rateBps` so a later rate change cannot reprice history.

### 6.2 The full-population measurement

| measure | before the round | after |
|---|---|---|
| DB `now()` | `2026-09-04 13:55:17.50755+00` | recorded per run below |
| users | 1,651 | 1,651 |
| payout rows | 212 | 212 |
| referral commission rows | 7 | 7 |
| clips | 8,996 | (unchanged by this round) |
| approved live clips | 6,440 | (unchanged) |
| approved live earnings | $12,342.04 | (unchanged) |
| **earnings invariant violations across ALL approved live clips** | **0** | **0** |
| audit rows | 26,375 | plus this round's own, named below |
| accounts holding trainer status | 0 | **0** |
| real clippers paired to a trainer | 0 | **0** |
| payouts carrying a trainer cut | 0 | **0** |
| trainer refunds | 0 | **0** |

### 6.3 The guard suite, and every guard seen to fail

`scripts/bl835-verify.ts`, **85 checks, 0 failures**, exit 0. Structural checks are extracted from the shipped source files, so **deleting a guard fails the suite rather than silently passing it**. Behavioural checks run against the real exported helpers.

`scripts/bl835-guard-demo.mjs` reverted seven shipped protections one at a time, each in the smallest way a careless future edit plausibly would, and **every one was seen to FAIL**:

```
BASELINE, nothing reverted: exit 0, 0 failed

REVERT  email.ts: drop the fourth term from the reconciliation      -> exit 1, 1 FAILED
REVERT  payout-calc.ts: stop subtracting the trainer cut            -> exit 1, 1 FAILED
REVERT  trainer-copy.ts: let the good-terms button pick the
        matching status                                             -> exit 1, 1 FAILED
REVERT  review/route.ts: stop adding the cut back at the
        mark-paid gate                                              -> exit 1, 1 FAILED
REVERT  review/route.ts: stop holding the referrer harmless         -> exit 1, 1 FAILED
REVERT  trainer-relationship.ts: read createdAt instead of
        postedAt ?? createdAt                                       -> exit 1, 2 FAILED
REVERT  end/route.ts: refund money already PAID to the trainer      -> exit 1, 1 FAILED

RESTORED, all six files IDENTICAL by sha256
FINAL, everything restored: exit 0, 0 failed
EVERY GUARD WAS SEEN TO FAIL, AND EVERY FILE IS BYTE-IDENTICAL AFTERWARDS.
```

**The demo earned its place by catching a guard that could not fail.** The refund check originally asserted that the pending filter contained `AVAILABLE` and `PENDING`, and that regex still matched when `|| c.status === "PAID"` was appended to the same filter, so the one reversion that would refund money already paid to a trainer produced **zero failures**. It now extracts the filter body and asserts `PAID` appears nowhere in it. That is exactly why BL-782 and BL-824 insist a guard be seen to fail before it is trusted, and it is the strongest single argument in this report for running the procedure rather than describing it.

**Two more guards failed on their first run for a reason worth keeping.** The check asserting that no trainer file mentions `writeClipEarnings` failed because the doc comment explaining that it never imports `writeClipEarnings` contains the words, and the phrase-collision check failed on the comment naming the three existing phrases. Rather than loosening either, the checks that ask "does this file MENTION x" now run over **code only**, with comments stripped, because a guard that could be satisfied by prose would be BL-833's defect in a new place.

---

## PART 7: WHAT WAS BUILT, AND THE PROOF

### 7.1 The schema, additive only

Applied through `scripts/run-schema-sql.js` with `ADD COLUMN IF NOT EXISTS`, **never `prisma migrate`**, then `npx prisma generate`. 35 statements, all applied, exit 0. Verified by direct query: 5 columns on `users`, 4 on `payout_requests`, 3 tables present, the partial unique index present.

• `users`: `isTrainer`, `trainerCode` (unique), `trainerPitchUrl`, `trainerPromotedAt`, `trainerPromotedById`
• `payout_requests`: `trainerCutPercent`, `trainerCutAmount`, `trainerRelationshipId`, `trainerEligibleGross`
• `trainer_relationships`, `trainer_commissions`, `trainer_refunds`
• **`uq_trainer_active_per_trainee`**, a partial unique index on `("traineeId") WHERE status = 'ACTIVE'`, which is the **database's own** guarantee of at most one live pairing per clipper rather than a check the application might skip. Prisma cannot express a partial unique, so it mirrors `uq_payout_open_per_user_campaign` exactly. Ended rows are excluded, which is what lets the history persist.

Nothing existing was altered, dropped, renamed or retyped. Every column is nullable or carries a default, so every row that existed before is valid. `scripts/migrations/BL-835-ROLLBACK-trainer-system.sql` holds the removal, deliberately not runnable through the runner, and states that reverting the code alone is the cheaper and safer half of the rollback.

### 7.2 Money file safety

Byte-identical by **blob OID** on both refs, verified with `git rev-parse main:<path>` against `git hash-object <path>`, because a working-tree sha256 fakes a CRLF mismatch on Windows:

| file | blob OID |
|---|---|
| `clip-earnings-writer.ts` | `ac5be7deb061768fec800aa89aae512a56a9e065` |
| `earnings-calc.ts` | `797e20985ad57475ef321afcf3cb1ea7b0d6ab84` |
| `balance.ts` | `81a683c1a6eddbe5aee3f746a555682d48d50469` |
| `tracking.ts` | `359bcbbe22fe97d937b4fa2515a84fdbe6f5c7e8` |
| `clip-earnings-invariant-middleware.ts` | `61cef39395363c31f0c902dd4c64e8c06b3e6449` |
| `money-decimal.ts` | `ef5cdae757b9ad3c23380ee8b63e279f98d0b6ac` |
| `campaign-era.ts` | `106e16ad75125c3b10b6949a2981d33614c69ab9` |

No Apify actor was run. The 11 BL-678 guards are untouched.

### 7.3 Nobody real was granted anything

Every fixture was a synthetic `isTestUser` account created and removed inside the same run. The acting owner was the `isTestUser` owner account rather than the real one, **so no audit row claims the real owner did something he did not**. Afterwards, and measured: **0 accounts hold trainer status, 0 real clippers are paired, 0 payouts carry a trainer cut, 0 refunds exist.**

**To reverse anything, if it is ever granted:** press the relabelled control on the trainer's row in `/admin/trainers` to take trainer status back, which needs no phrase. Ending an individual pairing is a separate, deliberate act with its own typed phrase and its own printed rollback.

---

## WHAT COULD NOT BE DETERMINED, AND WHAT IS REPORTED NOT CHANGED

**Named rather than smoothed.**

1. **The money arithmetic is proven on the pure functions and NOT by creating a real payout.** Proving it end to end would mean fabricating clip earnings and creating a real payout row on a real campaign, and a round that moves real money to prove it can move real money has failed before it started. The arithmetic is proven by 28 plus 85 checks against the shipped exported functions, the eligibility split is proven against real clip rows read only, and the route is proven to run end to end without throwing.
2. **THE AUDIT TABLE'S FOREIGN KEY CASCADES, WHILE THE SCHEMA SAYS IT DOES NOT. This is the sharpest thing this round found and it has nothing to do with the trainer feature.** `prisma/schema.prisma` declares `AuditLog.userId` with `onDelete: SetNull` and its own comment names the intent `F-AUDIT-NO-CASCADE`. The live database says:

   ```
   audit_logs_userId_fkey    delete_rule = CASCADE
   ```

   **So deleting a user DELETES their audit history rather than orphaning it**, which is the opposite of what that feature tag intends and the opposite of what a reader of the schema would believe.

   It was found because two of this round's own audit actions, `TRAINER_PAIRING_CREATED` and `TRAINER_APPEAL_OPENED`, were absent from the database at the end of the round while the four owner-written ones were present. `scripts/bl835-audit-cascade-finding.ts` proves both halves, **6 checks, 0 failures**: the rows ARE written and exist while the user does, and removing the user deletes them. So the trainer routes audit correctly and the fixtures took their own history with them.

   **Reported, not changed.** Altering a foreign key on the audit table is a live-schema change with its own blast radius and belongs in its own round. But the owner should know that today, deleting any user erases what they did.

3. **`bl833-watch-only` is still in the database.** BL-833's report says the fixture was removed at the end; the row is present, created `2026-09-01 18:02:10.45`, `isTestUser` true, REVIEWER, holding `CLIP_WATCH_ONLY`. Reported, not changed: removing another round's fixture is not this round's business.
3. **The four `calculatePayoutBreakdown` calls in the two admin unpaid routes project no trainer cut**, exactly as they project no express premium today. That follows the existing policy in `liability.ts`'s `cashFor`, which omits express deliberately. It means the owner's "what we still owe" projection is a pre-trainer figure. Reported so it is a choice rather than an oversight.
4. **The admin Send figure on an owner-adjusted row is still un-derived**, so it shows the gross the owner set with no fee, no express and now no trainer share taken off. That is BL-827's defect surviving on the admin side, which BL-827 fixed only on the clipper card. Pre-existing, outside this brief, not touched.
5. **The pre-existing fee rows still carry a bare hyphen** at `PayoutRequestFlow.tsx`, `payouts/page.tsx` and `admin/payouts/page.tsx`, which a screen reader announces as a credit. The new trainer rows use `aria-hidden` on the minus with an `sr-only` "less". Fixing the older rows is a one-word change per row and is reported rather than swept into this diff.
6. **`referrals/page.tsx:395-401` has an unnamed money checkbox and `:374-381` six `<th>` without `scope`.** That block is dead code, unreachable because `isTest = true` at `:183`. Reported, not fixed.

---

## BUILD AND MERGE

Recorded honestly, with exit codes echoed by hand and never read through a pipe.

• **Clean tsc baseline on the UNTOUCHED worktree before any edit: exit 0, `grep -c "error TS"` = 0.**
• **eslint v9.39.4 confirmed present**, so the BL-348 hooks gate is a real check and not a silent no-op.
• **Hooks gate baseline: exit 0, 0 errors, 11 warnings**, which is the ceiling. **At the end: exit 0, 0 errors, 11 warnings. Zero added.**
• **`npx tsc --noEmit` at the end: exit 0, `grep -c "error TS"` = 0.**

**THE FIRST BUILD FAILED AND IT IS RECORDED RATHER THAN QUIETLY RETRIED.** `npm run build` written to a log with the exit code echoed by hand and never read through a pipe:

```
BUILD 1: BUILD_EXIT=1
  ✓ Compiled successfully in 34.8s
  Running TypeScript ...
  Failed to type check.
  ./scripts/bl835-render.ts:49:7
  Type error: Variable 'shots' implicitly has type 'any[]' in some locations
             where its type cannot be determined.
BUILD 2, after typing the render harness: BUILD_EXIT=0, 0 errors
```

**That is exactly why the honesty note says never to trust `tsc` alone.** `npx tsc --noEmit` returned **exit 0 with 0 errors** on the same tree that `next build` refused, because the build's TypeScript step runs against a stricter configuration. A round that had stopped at a green `tsc` would have pushed a tree that does not build.

### The render pass, and why it moved to a production build

**Final: 17 shots, 0 at the wrong width, 0 with horizontal overflow, 39 assertions passed, 0 failed, exit 0**, against the **production build** (`npm run build` then `npx next start -p 3835`) with `DEV_AUTH_BYPASS=false`, real minted `__Secure-authjs.session-token` sessions, and the viewport set on the Playwright **CONTEXT** with `window.innerWidth` measured and printed beside every shot.

**Four earlier runs against `next dev` failed six, then five, then four, then five assertions, AT DIFFERENT WIDTHS EACH TIME, and that is reported rather than tuned away.** A diagnostic run proved every heading present, visible and correct at every width when given eight seconds, so the failures were on-demand compilation and not defects. Three harness corrections came out of it and each one is a real improvement:

1. **The `networkidle` wait was removed.** The app shell polls forever so it never goes idle; waiting on it burned sixty seconds and then handed a still-mounting page to the real wait.
2. **The wait is for the exact text the assertion is about**, not for a proxy element, so a timeout fails honestly instead of passing on a lucky frame.
3. **The heading assertion reads ALL `h1` texts, not the first element.** The shell mounts navigation twice, a desktop rail and a mobile drawer, so at desktop widths an earlier empty `h1` existed and `querySelector("h1")` was returning it. **That was a real harness defect and it would have kept flaking forever.**

On the production build the run was clean first time, which is the confirmation that the cause was the dev server rather than the pages.

| surface | widths | result |
|---|---|---|
| `/referrals`, the clipper's trainer block, not yet trained | 320, 375, 414, 1280, 1440 | 5 shots, the block on screen at every width, no login bounce |
| `/trainer`, as a trainer | 320, 375, 414, 1280, 1440 | 5 shots, `h1 = "Your trainees"`, **0 of 8 owner-economics names in the rendered text** |
| `/trainer` perimeter, as a plain clipper | 1280 | the app's own "could not be found" on the rendered DOM |
| `/admin/trainers`, as the owner | 320, 375, 414, 1280, 1440 | 5 shots, `h1 = "Trainers"` |
| `/admin/trainers` perimeter, as a clipper | 1280 | the app's own "could not be found" on the rendered DOM |

**The measurement limit is named rather than fudged:** `notFound()` called from a dynamic layout returns **HTTP 200 with a 404 body**, and every page here is a client component whose text is absent from the server HTML, so a page perimeter **cannot** be proven by status code. Both perimeters are proven on the rendered DOM in a real browser instead.

**Screenshots are written to `C:/w835/renders` and are deliberately not committed**, since the harness that regenerates them is committed and the shots carry fixture usernames. The 17 files are `s1-consent-untrained-{320,375,414,1280,1440}.png`, `s2-trainer-dashboard-{…}.png`, `s2-perimeter-notfound-1280.png`, `s3-owner-hub-{…}.png` and `s3-perimeter-notfound-1280.png`.

### Every proof, re-run against the production build

| suite | result |
|---|---|
| `scripts/bl835-arithmetic.ts` | **28 checks, 0 failures**, exit 0 |
| `scripts/bl835-verify.ts` | **85 checks, 0 failures**, exit 0 |
| `scripts/bl835-guard-demo.mjs` | 7 reversions, **every one seen to FAIL**, all restored byte-identical, exit 0 |
| `scripts/bl835-live-proof.ts` | **49 checks, 0 failures**, exit 0, on the production build |
| `scripts/bl835-payout-regression.ts` | **6 checks, 0 failures**, exit 0, **212 payout rows before and after** |
| `scripts/bl835-audit-cascade-finding.ts` | **6 checks, 0 failures**, exit 0 |
| `scripts/bl835-render.ts` | **39 assertions, 0 failures**, 17 shots, exit 0 |

**Zero Supabase pool errors** across the dev-server and production-server runs (`grep -ci "too many database connections"` = 0).

### The audit rows this round wrote, all accounted for

10 rows, every one written by the `isTestUser` owner on synthetic fixtures across two live-proof runs: **4 `TRAINER_STATUS_GIVEN`, 2 `TRAINER_APPEAL_REFUSED`, 2 `TRAINER_APPEAL_ALLOWED`, 2 `TRAINER_PAIRING_ENDED_BAD_FAITH`**, between `2026-09-04 14:31:58.815` and `14:32:40.292`. `TRAINER_PAIRING_CREATED` and `TRAINER_APPEAL_OPENED` were written too and then **cascaded away with their fixtures**, which is the pre-existing audit defect named above.

**Two user rows appeared in the window and they are NOT mine.** `farmaandhillon7` at `2026-09-04 14:21:47.249` and one other at `14:42:44.333`, both `isTestUser = false` and `isTrainer = false`: real signups, live platform traffic during the round, named rather than smoothed into a count.

---

## THE MERGE

| item | value |
|---|---|
| base `origin/main` before | `fdce6afd` |
| branch `checkpoint/BL-835` | `e22e5075` |
| merge commit on main | `47358431` |
| **merged tree OID** | **`ecb0e0225b2609bfb9b980f21abe29d7189482d4`** |
| **branch tree OID** | **`ecb0e0225b2609bfb9b980f21abe29d7189482d4`** |
| verified pushed | `origin/main == local == 47358431` |
| tags on origin | `pre-BL-835`, `post-BL-835`, `pre-merge-BL-835`, `post-merge-BL-835` |

**The merged tree OID equals the branch tree OID exactly, so the branch's green build IS the merge's build.** Main never moved from `fdce6afd` between the baseline read and the merge, so there were no conflicts to union. `git grep` over every tracked `.ts`, `.tsx`, `.md`, `.prisma` and `.sql` file at HEAD returns **0 files carrying a conflict marker**. `BACKLOG.md` went **170 to 171** sections, counted with `grep -c` and never piped through `head`. **`checkpoint/BL-723` confirmed NOT an ancestor of main.**

**Builds, with the exit code echoed by hand and never read through a pipe:**

| run | result |
|---|---|
| tsc baseline, untouched worktree, before any edit | exit 0, 0 errors |
| `npm run build` attempt 1 | **exit 1**, `Failed to type check` on `scripts/bl835-render.ts` |
| `npm run build` attempt 2, pre-commit | **exit 0**, 0 errors |
| `npm run build` post-commit | **exit 0**, 0 errors |
| `npm run lint:hooks` | exit 0, **0 errors, 11 warnings**, the ceiling, zero added |
| `npm run check:prisma-bypass` | **0 violations** across `src/` and `scripts/` |
| `npx tsc --noEmit` final | exit 0, 0 errors |

**Requires a Railway REDEPLOY.**

**Rollback:** `git revert -m 1 47358431`, or `git reset --hard pre-merge-BL-835`. The schema is additive and every new column is nullable or defaulted, so reverting the code alone stops all of it being read or written and needs no data repair; `scripts/migrations/BL-835-ROLLBACK-trainer-system.sql` holds the by-hand removal if the columns are ever to come out.

**The worktree `C:/w835` was removed after the merge.** `node_modules` was never junctioned into it.
