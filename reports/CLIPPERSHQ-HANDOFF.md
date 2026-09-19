# CLIPPERS HQ — THE HANDOFF DOCUMENT

**Written 2026-09-19. Everything below was verified against the code or the database on that date unless it is explicitly marked UNVERIFIED.**

This exists so that a session starting today knows what nearly a thousand rounds already learned, and does not pay for the same lessons twice. Read it end to end once. It is not a product brochure and it is not a summary of reports; where a report and the code disagreed, the code won and the disagreement is written down.

Read `CLAUDE.md` in the repository root as well. This document is the context behind those rules.

---

# PART ONE — WHO AND WHAT

## The business in two minutes

Clippers HQ is a SaaS platform that connects **clippers** with **brand campaigns**. A brand or creator funds a campaign. Clippers cut short vertical videos from that brand's material and post them to their own TikTok, Instagram Reels and YouTube Shorts accounts. The platform tracks the views on each posted clip and pays the clipper a rate per thousand views.

The domain is **clipershq.com**. It has **one P**, not two. Getting this wrong has cost rounds before.

There are four roles in the system:

**OWNER** is the person who runs the business. Full access to everything, including every money figure. Referred to throughout the reports as the owner, and he reads them.

**ADMIN** manages campaigns he has been assigned. He must never see agency or owner money data.

**CLIPPER** is the ordinary user, and the great majority: 1,771 user rows exist today. He sees his own clips, his own earnings, the campaigns he has joined. He is refused `/api/admin/*` and cannot see `ownerCpm`, `agencyFee`, `clientName` or `aiKnowledge` anywhere, ever.

**CLIENT** is a read-only campaign viewer. It is designed and **not built**. Do not assume it exists.

## How money enters and leaves

Money **enters** as a campaign budget. A campaign has a `budget`, a `clipperCpm` (what the clipper earns per thousand views) and an `ownerCpm` (what the platform earns per thousand views on the same clip). When realised spend reaches the budget the campaign stops paying and auto-pauses.

Money **leaves** when a clipper requests a payout. He asks for an amount against his available balance, the platform takes a withdrawal fee, and the remainder is sent to him. The fee is the platform's revenue on the clipper side; `ownerCpm` accrual is its revenue on the campaign side.

Between those two events the money is never "held" anywhere. It is **derived** at read time from clips, views and payout rows. That is the single most important architectural fact in this document, and most of the defects in PART SIX come from somebody forgetting it and computing a figure in a new place.

## The marketplace, in one paragraph

On top of the ordinary flow sits a **marketplace**, where the work is split between two people. A **maker** (called an editor in the code) cuts a video and submits it. A **poster** takes an approved video from a catalogue and posts it on his own account. Both get paid from the same clip. This is the newest and most complex part of the platform, it went live on 18 September 2026, and PART FOUR covers it in depth because it is what the owner cares about most.

---

# PART TWO — THE ARCHITECTURE

## The stack

Next.js 14 (App Router), TypeScript, Tailwind. Supabase Postgres accessed through Prisma 7.5. NextAuth v5 with Discord OAuth. Resend for email. Apify for TikTok and YouTube view tracking, HikerAPI for the Instagram overlay. Hosted on Railway with the NIXPACKS builder, started with `npm start`. Realtime updates over SSE.

Production code imports `db` from `@/lib/db`, which is the **extended** Prisma client carrying the invariant middleware. A script that constructs `new PrismaClient` directly must carry a `// PRISMA-BYPASS-OK: <reason>` marker, and `npm run check:prisma-bypass` fails the build otherwise. This matters more than it looks: the extended client is where a whole layer of money protection lives, and a bare client silently skips it.

## How a schema change is applied, and why `prisma migrate` is never used here

**Never run `prisma migrate`. Never run `prisma migrate reset`.** Only `prisma generate`.

The reason is concrete rather than stylistic. This database carries **25 hand-written SQL migrations** that Prisma's migration history does not know about. `prisma migrate reset` would silently discard them, which in production is fatal data loss. `prisma migrate dev` would try to reconcile a drift it cannot see and propose destructive statements.

The actual procedure is: write the SQL, print it in a file under `scripts/migrations/`, print the rollback **in the same file**, and either run it through `node scripts/run-schema-sql.js` or hand it to the owner for the Supabase SQL editor. Then run `npx prisma generate`.

Two read-only and write-limited helpers exist for a session:

* `node scripts/run-select.js "<SELECT>"` — read only, refuses any write keyword. This is the correct way to check a figure.
* `node scripts/run-schema-sql.js <file|--inline "...">` — accepts only `CREATE`, `ALTER ... ADD COLUMN`, `INDEX`, `TYPE ... IF NOT EXISTS`. It refuses `DROP`, `TRUNCATE`, `DELETE`, `UPDATE`, `INSERT`, `ALTER COLUMN` and `RENAME`.

Data mutations go through `run-mutation-once.js` or the owner's own Supabase editor. Never casually.

**Row Level Security is DENY ALL by design.** `rowsecurity` is on and there are zero policies; Prisma bypasses it because it connects with `DATABASE_URL`. Never disable RLS and never add a client-side Supabase read without writing a policy first.

A hard-won corollary, from BL-841, BL-845, BL-886, BL-902 and BL-903: **a Prisma `@@unique` declaration enforces nothing at runtime.** It is a hint to Prisma's own migration engine. If the index was never created in Postgres, there is no constraint. Check `pg_indexes`. PART SIX has the three times this cost real money.

## The protected money files

Six files are load-bearing for money. On any task, their sha256 or blob OIDs must be **byte identical** before and after, unless changing one is the explicit purpose of the round:

| File | What it protects |
|---|---|
| `src/lib/clip-earnings-writer.ts` | The single chokepoint that writes a clip's earnings. Holds the L1 budget hard lock, the four-field invariant, and the three-leg marketplace sync. |
| `src/lib/earnings-calc.ts` | Every earnings and bonus formula. One definition each, imported everywhere. |
| `src/lib/balance.ts` | What a person can withdraw. Holds the paid-is-final subtraction. |
| `src/lib/tracking.ts` | The cron that turns views into money. 281 KB and the largest file in the project. |
| `src/lib/clip-earnings-invariant-middleware.ts` | The L2 middleware that refuses a write breaking the invariant. |
| `src/lib/money-decimal.ts` | Decimal handling, so cents do not drift. |

`src/lib/campaign-era.ts` is checked alongside them by most rounds and should be treated the same way.

**Verify them by git blob OID, not by working-tree sha256.** On Windows with `core.autocrlf=true`, comparing a working-tree hash against `git show origin/main:<path>` reports every text file as different. BL-899 hit this and briefly believed five identical files had changed. `git rev-parse HEAD:<path>` is the honest check.

`tracking.ts` must never appear in an unrelated diff. If it does, something went wrong.

---

# PART THREE — THE MONEY MODEL, WITH REAL NUMBERS

## The ordinary clip

```
baseEarnings = (views / 1000) × clipperCpm
bonusAmount  = baseEarnings × (bonusPercent / 100)
earnings     = baseEarnings + bonusAmount
```

The bonus percent is the sum of a level bonus, a streak bonus and a PWA bonus, **capped at 25** (`MAX_BONUS_CAP`, `earnings-calc.ts:48`). The cap is reachable: level 5 gives 20, a 90 day streak gives 10, PWA gives 2, for a raw 32 that clamps to 25. An owner **manual override** short-circuits the other three and has its own ceiling of **30** (`MANUAL_OVERRIDE_CEILING`, `earnings-calc.ts:49`).

The owner's cut on a `CPM_SPLIT` campaign accrues in parallel as an `AgencyEarning` row:

```
ownerEarnings = clipperGrossEarnings × (ownerCpm / clipperCpm)
```

Note what that is **not**: it is not a percentage share of the clip's gross. It is a ratio of two CPMs. Getting this wrong produced one of the most instructive errors in the project's history and PART FOUR walks through it with the real numbers.

Owner earnings display as $0 when the clip is not APPROVED, or `videoUnavailable` is true, or `viewsForCalc` is below `campaign.minViews`.

## The withdrawal fee

When a clipper requests a payout:

```
feePercent = user.referredById ? 4 : 9
```

Verified at `src/app/api/payouts/route.ts:674`. An ordinary clipper pays **9 percent**; a clipper who was referred by somebody pays **4 percent**. The rate in force at approval is stamped onto the clip as `feePercentAtApproval` so a later rate change cannot rewrite history.

## Express, and the trainer cut

`calculatePayoutBreakdown` (`src/lib/payout-calc.ts:86`) takes **positional** arguments `(requestedAmount, feePercent, bonusPercent, express?, trainer?)`. Passing a named object silently ignores every field and returns `NaN`; a round lost time to exactly that.

```
feeAmount        = requestedAmount × feePercent / 100
expressFeeAmount = requestedAmount × 4 / 100        (only when express)
roomAfterFees    = max(0, requestedAmount − feeAmount − expressFeeAmount)
trainerCutAmount = min(requestedTrainerCut, roomAfterFees)
finalAmount      = requestedAmount − feeAmount − expressFeeAmount − trainerCutAmount
```

Two things follow that are easy to get backwards:

**The express premium is charged on the GROSS**, the full requested amount, not on what is left after the ordinary fee. It defaults to 4 percent and the API hard-codes 4.

**The trainer cut is taken AFTER the platform fee**, out of what remains, and is clamped so it can never exceed `roomAfterFees`. A bad input can only ever charge less than intended; it can never produce a negative payout.

`bonusAmount` in the breakdown is **display only**. The bonus is already inside `requestedAmount` because it is already inside `clip.earnings`. Do not add it again. This has been attempted.

## The invariants, by name and by what each prevents

These are not style rules. Each one is a wall somebody already walked into.

**The four-field Clip invariant.** At all times `earnings ≈ baseEarnings + bonusAmount`, within $0.01. It prevents a partial write leaving a clip whose total disagrees with its own parts, which is how a recompute silently invents or destroys money. Enforced in `clip-earnings-writer.ts` and again in the L2 middleware. Live measurement: 0 violations across 10,202 clips.

**writeClipEarnings is the only write path.** `Clip.earnings`, `Clip.baseEarnings` and `Clip.bonusAmount` may be written **only** through `writeClipEarnings` (`src/lib/clip-earnings-writer.ts`). A direct `db.clip.update` or `tx.clip.update` on those three fields is forbidden and `npm run check:prisma-bypass` fails the build on it. Other Clip fields by direct update are fine. There are **23 call sites in 15 files** that reach this one function, and they all reach the same line. It prevents the budget lock and the invariant from being bypassed by a new writer who did not know they existed.

**No overpayment.** A campaign's realised spend may never exceed its budget. Two independent mechanisms enforce it: a per-tick budget cap inside a Serializable transaction that truncates the crossing clip, and an L1 hard lock inside `writeClipEarnings` that reads committed spend and **throws**, rejecting the whole increment, if the projection exceeds the budget. Live: 0 of 21 budgeted campaigns over budget, the closest sitting $3.96 **under**.

**No double pay.** Two open payout requests on one campaign, or a clip carrying two agency earning rows, are both refused. Payout creation also dedupes within 10 seconds.

**Paid is final, with its write side.** Money already paid out is final and can never be clawed back by a later deletion, devaluation or recompute. The **read side** (BL-824) is encoded once, in `balance.ts`, as a property of how paid money is subtracted:

```
effectivePaid(campaign) = min(paidGross(campaign), payableEarnings(campaign))
available = max(0, payable − effectivePaid)
```

A payment can only ever consume the earnings of the campaign it was made against. Nothing is refunded and nothing is written. Three call sites enforce it: `computeBalance`, the withdrawal gate's global clamp in `payouts/route.ts`, and `campaigns/[id]/min-payout-impact`. The brief that commissioned it named two; the guard found the third.

The **write side** (BL-849) is the paid floor: `floorMarketplacePosterEarnings` and `floorV2EditorEarnings` hold a person's recorded earnings at his `effectivePaid` on that campaign, so a recompute cannot write a figure down below money he already has.

What breaking it costs was measured: 40 clips carrying $140.54 multiplied down to $25.65 against $78.54 already paid, after which Mark Paid jammed at $0.00 against the `payout_amount_positive` CHECK constraint, five identical failures, permanent.

**Never decrease is NOT the same rule, and confusing the two caused a real defect.** A recompute may legitimately lower a figure when views fall; 1,245 legitimate decreases across 650 clips have been measured. An early marketplace round applied a blanket never-decrease to the maker's leg, the leg **ratcheted** to $108.00 while the poster reached $54.00, and the fix was to replace it with a **paid floor**, which was the rule actually wanted. If you are about to block a decrease, ask whether you mean "never below what he has been paid" (yes) or "never below what it was" (almost certainly no).

**A third party's cut is a stamped deduction on the payout row, never a rewrite of a clip's earnings.** The trainer cut and the referral payment both work this way. A clip's earnings describe what the work earned; who receives slices of it is a property of the payout. Rewriting a clip's earnings to express somebody else's cut destroys the only record of what the work was worth, and it breaks the invariant.

## The budget, in operation

Same-campaign clips are processed **sequentially** by the tracking tick, which for a long time was the only thing preventing concurrent overspend. It was an accident of loop structure, not a constraint: there was no lock, no unique index and no database guarantee behind the comment that said so. BL-901 added a **campaign row lock inside the transaction**, and forty racing writers that had landed at $1,389.20 against a $500 budget now land at $486.22, with concurrent and sequential figures identical in every case.

At the cap the campaign auto-pauses and `lastBudgetPauseAt` is stamped. A rejected or undone clip auto-resumes it if spend falls below budget. A manual pause clears the stamp.

`payoutReductionRatio` is a **multiplier**, not a ceiling, and it is **immutable once set**. It is honoured on every recompute path. It compounds forever and has no undo.

Budget operations use Serializable isolation. Every `findMany` carries a `take:` limit (500 clips or users, 1000 earnings). Every query summing APPROVED clip earnings must include `videoUnavailable: false`.

---

# PART FOUR — THE MARKETPLACE, IN DEPTH

This is the part to read twice.

## The two sides

A **maker** (`EDITOR` in the code) cuts a video and submits it with a Google Drive link. The owner reviews it. If approved it enters a catalogue.

A **poster** browses the catalogue, takes a clip, posts it on one of his own connected accounts, and pastes the live URL back. From that moment the clip is tracked like any other and earns on views.

Both are paid from the same clip. Neither can do the other's job on the same campaign without asking.

## The side lock is PER CAMPAIGN, and it used to be platform wide

This is the single most likely thing to get wrong from reading old reports, so it is stated plainly.

There were two rules. **Rule one**, platform wide, said your side decided which action routes you could call at all. **Rule two**, per campaign, said you may not act on a campaign where you already have work on the other side.

**Rule one was DELETED.** It was the wrong fix for the complaint that produced it: the owner objected to being *shown* "Send a clip" and "Post a clip" together, which is a navigation question, and it was answered with a permission gate. The cost was exercised and was real — a maker on campaign X was refused from posting on campaign Y. Navigation still follows the person's role, so nothing the owner objected to came back.

**Rule two is now the whole rule.** You may not act on a campaign where you already have live work on the other side. This is the only thing standing between one person and posting his own clip for both halves of the money, so it is absolute.

What holds the lock, on the maker's side, is a clip in status `PENDING`, `APPROVED`, `RETIRED` or `REJECTED` (`LOCK_HOLDING_CLIP_STATUSES`). Note that **REJECTED holds it**: a refused clip no longer unlocks anybody, because the owner replaced automatic release with a request he approves himself. `WITHDRAWN` does not hold it, because taking your own work back before anybody acted on it is not an action taken on a side. On the poster's side any post of his holds it, because a post is live on a real account the moment it exists.

The lock is **derived, never stored**. There is no `roleLocked` column and a guard fails the build if one ever appears.

What the rule costs is stated rather than hidden: a person who has made one clip on a campaign cannot post on that campaign without asking, even for a clip somebody else made. That is deliberate, because the cheap alternative (let him post anybody's clip but not his own) would make a money rule depend on one branch being right.

## The switch request: fifty words, and the owner answers it himself

The one way past the lock is a request. `V2_SIDE_REQUEST_MIN_WORDS = 50`. He must write **at least fifty words** explaining why, and the owner approves or refuses it personally.

It is a **word** count, not a character count, because fifty characters is a sentence and the point is to make the request cost something. Words are counted as runs of non-whitespace, the way a person would count them: punctuation is not a word and a double space is not two. The reason the fifty words are asked for is shown **above** the box, not after a refusal.

The counter reads back as he types: `"31 of 50 words. 19 to go."` and then `"50 words. That is enough, you can send it."`

There are zero side requests in the database today.

## The split: 45 / 45 / 10

```
MARKETPLACE_V2_EDITOR_SHARE   = 0.45
MARKETPLACE_V2_POSTER_SHARE   = 0.45
MARKETPLACE_V2_PLATFORM_SHARE = 0.1
```

One declaration each in `src/lib/marketplace-v2-earnings.ts`. No literal `0.45` appears anywhere else in marketplace code, and a guard enforces that.

**The order is not a choice.** Split the gross 45/45/10 **first**, then each earner pays his own withdrawal fee at his own rate on his own payout row. Two reasons, both proved:

1. It produces identical cents to "fee first, then split" whenever that alternative is even definable. On a $100 gross with both earners unreferred: split first gives $45.00 − 9% = $40.95 each; fee first gives 45% of $91.00 = $40.95 each.
2. "Fee first" **stops being defined** the moment the two earners carry different fee rates, because the fee is a property of the withdrawing user and not of the clip. There is no single rate to take off the gross when the maker is referred at 4 percent and the poster is not at 9.

**The platform leg is a residual**, not a third multiplication:

```
editorBase   = min(round2(gross × 0.45), grossR)
posterBase   = min(round2(gross × 0.45), round2(grossR − editorBase))
platformBase = max(0, round2(grossR − editorBase − posterBase))
```

Three independent multiplications create money from nothing at sub-cent boundaries. At a gross of $0.55, two legs of $0.25 plus a platform leg of $0.06 sum to $0.56. The residual form gives $0.05 and the three legs sum to $0.55 exactly. The owner takes 9.09 percent of that particular clip instead of 10, and that is correct: nothing is created and nothing is lost.

The symmetry of 45/45 creates a defect that 60/30 cannot have, and it was caught by arithmetic proof rather than by review: at a gross of $0.013 both legs round **up** to a cent against a gross that rounds to a cent, and a naive `Math.max(0, …)` swallows the negative residual so the three legs sum to $0.02 against a $0.01 gross. The `min` clamps above are the fix.

## Bonuses multiply only their own earner's 45 percent

```
editorBonusAmount = round2(editorBase × (editorBonusPct / 100))
posterBonusAmount = round2(posterBase × (posterBonusPct / 100))
```

A bonus multiplies **that earner's own leg**. Never the gross, and never the other person's leg.

Bonuses sit **outside** the residual. The platform leg is computed from the base legs before any bonus exists, so no bonus is an input to it. The three legs therefore sum to the gross **plus** both bonuses: a bonus is extra money the campaign pays, not a re-carving of the gross.

A marketplace clip carries **two** bonus stacks where an ordinary clip carries one, because there are two earners with two profiles. At a 10 percent maker bonus and a 5 percent poster bonus, a $100 gross clip disburses 49.50 + 47.25 + 10.00 = **$106.75**, and the platform's slice falls from 10 percent to **9.37 percent** of what actually leaves the budget.

The 25 percent cap is **per earner, not per clip**, so one clip can carry 50 percent of bonus across both parties. There is no caller anywhere that adds the two and caps them together.

The 5 percent referral payment is **not a bonus** to either earner. It is a separate payment to the inviter.

## The ADDS decision, and the two figures the owner should know

The question: does the platform's 10 percent **ADD** to the owner's ordinary per-clip cut, or **REPLACE** it?

He answered **ADDS**, and that answer lives in exactly one place:

```
export const MARKETPLACE_V2_PLATFORM_CUT_MODE: "ADDS" | "REPLACES" = "ADDS";
export function v2AgencyEarningApplies() { return MARKETPLACE_V2_PLATFORM_CUT_MODE === "ADDS"; }
```

Read the function, never the constant, so the decision has one reader as well as one writer.

Mechanically, a marketplace clip leaves `isMarketplaceClip` **false** on purpose, so it falls into the ordinary `isCpmSplit` branch and an `AgencyEarning` row **is** written on top of the 10 percent. ADDS means letting that branch run. REPLACES would mean suppressing it, which is what the **first** marketplace does: no `AgencyEarning` row is ever written for a first-marketplace clip.

**The measured figures, on a real campaign, verified against the database on 2026-09-19:**

The campaign `Zhus Edit (0.50 CPM)` has `clipperCpm` 0.5 and `ownerCpm` 0.3197. Its `guaranteeOwnerSplit` is true with a `lockedOwnerShareDecimal` of 0.39002074.

```
ownerCpm / clipperCpm            = 0.639400
s / (1 − s)  where s = 0.39002074 = 0.639400      ← the two agree exactly
```

Per **$100 of gross**, both earners unreferred, no bonuses:

| | ADDS |
|---|---|
| maker gross / cash | $45.00 / $40.95 |
| poster gross / cash | $45.00 / $40.95 |
| platform leg | $10.00 |
| the owner's ordinary cut | **$63.94** |
| the two withdrawal fees to the owner | $8.10 |
| **the campaign spends** | **$163.94** |
| **the owner nets** | **$82.04** |

Under REPLACES the campaign spends $100.00 and the owner nets $18.10.

**ADDS does not move money from the earners to him.** Both take $45.00 gross and $40.95 cash under either option. What ADDS changes is what the **campaign pays for the same views**: $163.94 instead of $100.00. On a fixed budget that means the same budget buys proportionally fewer views and the campaign exhausts and auto-pauses sooner. That is the whole trade and it is his to make.

**Why the cut is $63.94 and not $39.00, which three reports got wrong.** The owner's cut is computed as `views/1000 × ownerCpm`, which equals `gross × (ownerCpm / clipperCpm)`. It is **not** `gross × ownerShare`. The locked share `s` of 0.39002074 is the owner's share of the **total campaign spend**, not of the clip's gross: $63.94 / $163.94 = 0.39002. Reading it as a share of the clip's gross gives $39.00, a spend of $139.00 and a net of $57.10, and three consecutive reports printed exactly that, each citing the previous one as confirmation. The header comment of `marketplace-v2-earnings.ts` still carries an illustrative $133.33 / $51.43 pair computed the same wrong way at a nominal 33.33 percent; it is explicitly flagged in the file as the other reading. **Use $163.94 and $82.04.**

## Duplicates: allowed across your own accounts, refused twice on one

**The same video on several of one person's own accounts is ALLOWED and earns on each.** This was built permissive deliberately and exercised rather than asserted.

**The same video twice on ONE account is REFUSED**, with a sentence rather than a constraint name: *"You have already posted this clip from that account. Pick another account, or a different clip."*

There are **two** guarantees behind that refusal and the reason there are two is instructive. The application branch gives the person a readable sentence. The unique index `marketplace_v2_posts_v2clipid_clipaccountid_key` on `("v2ClipId", "clipAccountId")` is the race-proof half, and it **exists in `pg_indexes` today, verified 2026-09-19**. For a period it did not, and PART SIX has what that cost.

On the submission side, the duplicate rule is scoped to the **maker**, using a content hash on the marketplace table's own `videoHash` column. The same maker sending the same file twice is refused. A **different** maker sending the same file is accepted, and cannot even be compared against the first, because `editorId` is in the `where` of the only query that can refuse. That is deliberate: a global unique on the hash would refuse an honest second submission, which "blocks real work and looks like a false accusation."

A poster pasting another poster's live URL on the same campaign is refused. A poster pasting the same URL twice to one account is refused both in the application and by a database unique.

## The three campaign types

```
enum CampaignType {
  NORMAL            // a clipper uploads his own clip. Today's behaviour, and the default.
  MARKETPLACE_ONLY  // a clipper may NOT upload his own clip. Makers submit, posters post.
  BOTH              // both entry points are open.
}
```

`campaignType` is read by **exactly one refusal**, inside `processClipperSubmitLink`, and by the display surfaces that tell a clipper which flow he is in. It is read by **no** money, earnings, payout or tracking path. Keep it that way.

This is distinct from `pricingModel`, which is `"AGENCY_FEE"` or `"CPM_SPLIT"` and is a money field.

## Strikes and bans: manual, with exactly one creation site

The marketplace strike system is **purely manual**. A strike is issued by a human, with `issuedById` required against a NOT NULL column.

There is **one creation site**, `issueV2Strike` in `src/lib/marketplace-v2-strikes.ts`. `npm run check:v2-strike-sites` counts occurrences of `marketplaceV2Strike.create` across `src/` and **fails the build at anything other than exactly one**, and fails it if that one is not in that file, and fails it if any file under `src/app/api/cron/` so much as mentions the table. It is a gate, not a convention. Verified today: one real call site.

The constants: a 90 day strike window, three strikes, and a **seven day ban** on the third, from normal posting only. `V2_BAN_MAX_DAYS` is 365.

**There is no ban flag.** The ban is `count of live strikes >= 3` computed at read time, so revoking a strike lifts the ban by construction. An earlier system had a `bannedUntil` scalar written by one cron and cleared by nothing, which is exactly the shape to avoid.

**A banned poster's money is untouched.** The leg he earned stands; only a new withdrawal is refused.

There are zero marketplace strikes in the database today.

The comparison tool that might lead a strike is the owner's own eyes. It says in its own copy, first and not in a tooltip, that it cannot tell whether two videos are the same video, that it does not score or rank, and that it only shows clips on this campaign. A previous generation of automatic strike logic misfired across three consecutive rounds, which is why new automatic penalties are the thing not to build here.

## The conversion action

An owner takes a normal clip and says it is really a maker's work, and the money follows.

This exists because **a conversion pays the maker and a strike only punishes the poster**. The maker is the person who lost money, and nothing in a three strike system ever reaches him.

It is deliberately **not** a theft feature. Nothing in the file mentions theft, decides theft or records an accusation. It records who made a video.

It writes no money code of its own. Every dollar goes through `writeMarketplaceV2Earnings` → `writeClipEarnings`, so it inherits the L1 budget lock, the four-field invariant, the three-leg sync, both paid floors and the campaign-comes-from-the-clip rule without restating any of them.

What happens to money, answered in the file rather than in a report:

* **Already earned, not yet paid:** it is re-split. The poster's recorded earnings fall from 100 percent of gross to 45 percent, the maker's 45 percent is created, the platform takes 10. Nothing is taken out of anybody's hands because nothing had left them.
* **Already paid: it stays his, absolutely, and his record stays above it too.** The paid floor holds his recorded earnings at his `effectivePaid` on that campaign.

There is an `undoConversion`, and it has a trap documented in the file: three fields that must never be set on undo, because setting any of them would have kept treating the clip as a marketplace clip, paid the poster 100 percent again, and silently reversed the conversion.

## What each of the three people sees, and must never see

**The maker** sees where his clip went: every post, who posted it, the link, that post's views, and **what that post earned him**. The poster's earnings are absent **by construction** — there is no field on that response that could be subtracted to recover them.

**The poster** sees the catalogue, his own posts and his own earnings. He does not see who else took the same clip. Three clip-facing surfaces he can reach were searched for nine taker field names and for the user ids of four other people, two of whom had posted on that very clip: none present.

**The owner** is the only one who sees all four legs together: the maker's, the poster's, the platform's 10 percent and his own ordinary cut. That screen is owner only behind a 404-before-403 gate.

**The reason printing both halves on one screen is forbidden is subtraction.** If a screen shows the gross and shows one earner's 45 percent, the other 45 percent and therefore the platform's 10 percent follow by arithmetic. Hiding a number while publishing everything it can be derived from hides nothing. This is also why the first marketplace never shows a clipper its 10 percent, and why the marketplace's 10 percent platform fee must never be shown to a non-owner: users see 60/30, the owner sees 60/30/10.

Refusals are **404, never 403**, for anything that would reveal a feature exists. A 403 tells you there is something there.

---

# PART FIVE — THE STATE OF PLAY, 19 SEPTEMBER 2026

The marketplace went live on **18 September 2026**. The owner made a real campaign `MARKETPLACE_ONLY` and ACTIVE at 19:08 UTC, and at 20:37:39 UTC a real clipper with `isTestUser` false, on no allow list, chose the maker side and submitted the platform's first ever marketplace clip.

**The launch funnel, as measured on the first day:**

| | |
|---|---|
| emailed in the launch broadcast (19:08 to 19:11) | 1,551 |
| arrived at the marketplace | 19 |
| chose a side | 15 (8 poster, 7 maker) |
| arrived and chose nothing | 4 |
| submitted a clip | 3 |
| posted a clip | 0 |

**The live state today, queried directly on 2026-09-19 at 13:04 UTC:**

| | |
|---|---|
| total users on the platform | 1,771 |
| users carrying a marketplace side | 17 |
| marketplace clips submitted | 18 (12 approved, 3 pending, 3 rejected) |
| distinct makers who have submitted | 3 |
| **posts made** | **6** |
| distinct posters who have posted | 2 |
| maker earnings accrued | $0.00 |
| platform earnings accrued | $0.00 |
| side requests | 0 |
| strikes | 0 |

**The "zero posts" figure is out of date and this document corrects it.** Six posts exist, the first at 08:25:53 UTC and the most recent at 09:58:53 UTC on 19 September. Both money legs still read $0.00 because a post earns nothing until views accrue on it, which is correct rather than broken.

**No real user has hit a single refusal.** That was established for the first live window and it took work, because the refusal table at first glance says otherwise: the rows in it were scripts, a prior sandbox, and a round's own proofs. The small-numbers rule applies regardless — below five people the owner's own panel says in words that it is too few to read a pattern into.

**Open items at the time of writing:**

* Clips sit pending and makers wait on the owner's review. This is owner action, not code.
* **Every clip thumbnail has failed. Fifteen of fifteen at the time of measurement, zero previews have ever existed.** The code predicted it might fail often; production says it fails always. Browser canvas capture has a measured 100 percent failure rate and needs a different approach.
* A burst notification undercounts, saying "3 waiting" when fourteen arrived in that window.
* **Only one of the owner's three email addresses receives anything.** The other two return `403 validation_error` because the Resend account has no verified domain. This is his manual step and no round can do it.
* The closed mobile drawer is hidden from screen readers while holding 34 focusable links, on every page of the platform. Reported, not fixed.
* The unseen-clip badge is still not built.

**Three things every round has assumed and none can yet be measured**, stated rather than guessed: whether a maker reads a rejection and resubmits; whether a poster returns from Drive on the same device; and whether the **30 minute posting window** is long enough. That window is the largest untested assumption on the platform. Its source of truth is `MAX_CLIP_AGE_MS` and `MAX_CLIP_AGE_LABEL` in `src/lib/clip-config.ts`, and it measures from the moment the video **goes live on the platform**, not from the moment the poster opens Drive. An hour spent downloading costs him nothing.

---

# PART SIX — HOW WORK IS DONE HERE

This is the section that matters most, and it is the reason this document exists.

## The shape of a round

**Investigate, then build, then prove, then merge, then report.** In that order, and the first step is not optional.

**A brief's premise is a hypothesis, not a fact.** Several rounds were briefed on a premise and measured the opposite, and every one of them was right to say so:

* A round briefed that two liability reports **understate** the platform's exposure and that the gap is growing measured that both **overstate**, by $634.18 and $724.31.
* A round briefed that a marketplace listing could oversell a campaign's daily cap found that the owner's exact case **cannot happen**, and corrected his premise. The real hole was different in kind: a listing goes stale after a later campaign edit.
* A round briefed on an alarming backlog of 512 starved tracking clips measured 3,732, and then measured that **zero** of the 4,140 overdue by a week sit on an active non-archived campaign.
* A round briefed that the disk could be cleaned to reach a target measured that the target was arithmetically unreachable and said so in the first paragraph.

Saying a plan will not work is a valid and valuable answer. Measure before you agree.

**The workflow is branch and merge**, by default, for anything non-trivial. Pre-tag, `git checkout -b checkpoint/<round>`, edit, build, commit, push the branch, build again to confirm clean, then a **separate merge round**: pre-merge tag, `git merge --no-ff`, build, push main, post-merge tag. Direct to main is for a one-line typo, a doc-only edit with zero code impact, or an emergency revert.

**The working tree is shared.** Several sessions use one repository and one HEAD. Stage and commit **only** the files your task changed, by explicit pathspec. Never sweep another session's uncommitted edits into your commit. If HEAD drifts to another branch mid-task, move your commit back onto your branch and reset the other. Use a worktree when parallel edits would collide, and put it at a **short path** — Windows `MAX_PATH` will otherwise break `npm ci`. A fresh worktree also needs `.env` and `.env.development.local` copied before anything runs.

**A push you did not verify is not done.** Use `node scripts/safe-push.mjs <branch>`, which asserts `origin == local` and retries, and run it **from the tree holding the commit** or it compares the wrong HEAD.

**Teardown sweeps everybody's leftovers, not just yours.** Removing only your own worktree is what let 99 directories and 21.7 GB pile up at the C: root over sixty rounds.

## The sandbox discipline

Rounds create real rows in a real database that real people are using. The rules exist because that is dangerous.

* **Use a prefix** on every entity you create, so your rows are identifiable by name.
* **Take an opening snapshot before you create anything.** Not after. A round that skipped this fell back to a default window and attributed **30 real users' payouts over 12 days** to itself; measured against the true round window it had created exactly **1**.
* **Record every id at creation**, and delete only those ids.
* **Account for product-written rows.** Your action causes the product to write rows you did not create. They are yours to clean up too.
* **Prove identical counts and fingerprints afterwards**, not merely "I deleted what I made."
* **Anything unremovable goes in the first line of the report**, with its ids and the SQL to remove it.

One round could not remove a directory because one of its own lingering shells held it as a working directory. It reported that the directory was empty and unregistered, that six removal attempts over thirty seconds had not cleared it, and that nothing about it was claimed clean that was not. That is the standard.

One round disturbed the owner three times by sending him real emails during proof runs, because the notification fan-out finds every OWNER row and not only the sandbox one. It said so: "The rows were removed; the emails cannot be."

## The proof discipline

**Every failure path gets its own user.** Sharing one account across checks means a rate limiter can answer for a refusal you meant to test.

**Assert that the status is not 429.** Two checks were once recorded as passes on a 429. A rate limit is neither a duplicate guard nor a ban.

**Every setup is itself a check.** If the setup silently does nothing, the assertion afterwards measures nothing. A round built a payout refusal test whose setup silently produced no payout, so the route answered **404 from an undefined id** and the round read that 404 as the refusal under test. Another wrote a check whose setup created no request at all, so "while he waits nothing changes" was green because nothing existed to change.

**Every check must state WHAT MADE IT PASS.** This is the rule that catches the rest. A proof once ran with `setViews` calling `updateMany` on clips that had no `ClipStat` row, so views stayed 0, the gross was 0, and **the whole money proof read $0.00 while every route returned 200**. Every route returned 200 and the round was measuring nothing. It now asserts the value landed.

Related, and the same disease: a round's budget proof hardcoded `true` for its bonus-ceiling check and ran with every bonus at zero. The legs came back exactly 45/45/10, and it was the implausible cleanness of that result that exposed it.

**A pass for the wrong reason is a failure.** A round reached an adjust refusal on a claim that had already been PAID, so the route answered "Cannot adjust payout in status PAID" and the check passed on a status guard rather than on the empty snapshot it meant to test. It reported that as a failure of honesty rather than of code.

**Mint nothing your own test reads.** A round minted `isTestUser: true` to reach a feature, and the filter it was testing reads that same flag, so the check was looking at a test user and correctly reported the test campaign visible. The next round did it properly: read `isTestUser` from the user's own row and never mint it.

## The guard discipline

A guard is a script wired into `prebuild` that fails the build when a rule is broken. There are **17** of them today, and they run on every build:

`check:prisma-bypass`, `check:removed-fields`, `check:event-wiring`, `check:v2-leg-sync`, `check:v2-editor-balance`, `check:paid-is-final`, `check:payout-snapshot`, `check:css-tokens`, `check:liability-rules`, `check:v2-strike-sites`, `check:schema-drift`, `check:page-titles`, `check:v2-flag-gate`, `check:v2-role-is-a-gate`, `check:v2-single-share-writers`, `check:v2-lists-are-queries`, `check:budget-lock`, plus `lint:hooks` at 0 errors and at most 11 warnings.

**A guard must be demonstrated FAILING.** Not read, not reasoned about. Break the thing it watches and watch it go red.

The rules, each of which exists because a guard shipped that could not fail:

* **One check at a time.** One round's mutation for check B3 also tripped B9, so neither was shown to fail alone.
* **Never sample; count.** Assert an exact count, not presence. "At least 2 uses of the poster floor" is a presence test wearing a number; the demonstration removed one and it stayed green. It asserts exactly 4 now, each load-bearing.
* **Each check must name itself distinctly.** One guard's demonstration matched its tag anywhere in the output, and the guard prints `G1/G2:` in its own notes, so those checks passed whether or not they fired.
* **Restore the tree after each mutation, and verify byte identity.** One demonstration read text and wrote it back, normalising CRLF to LF, so it did not restore byte for byte. It said so.
* **Match on word boundaries, never substrings.** This is the single most common failure. A guard testing `includes("syncV2LegsAfterPosterWrite")` passed when the demonstration renamed the call to `syncV2LegsAfterPosterWrite_DISABLED_FOR_DEMO`, because a substring of a longer identifier still matches. The same shape recurred with `"marketplace-v2-editor-balance"` versus `"...-balanceX"`, and with `marketplaceV2PostId` versus `marketplaceV2PostIdXX`.
* **Count in the right scope.** Two guards counted across the **whole file**, so deleting the one occurrence that mattered left the totals above their thresholds and the guard passed while the gate had gone blind.
* **Never let a comment satisfy a check.** Three guards counted prose rather than code. One refused a file that had *removed* an opt-out because the comment explaining the removal still contained the word. One reported three strike creation sites on a tree with one, counting its own documentation. A guard a comment can break gets silenced by deleting the comment.
* **Watch for CRLF.** Guard anchors written with `\n` match **zero** times against CRLF files. Three of nine checks in one round had never been demonstrated at all because their anchors were multi-line.
* **Guards must see data, not only syntax.** A guard written to catch an unguarded navigation link matched only an `href` **attribute**. The navigation declares entries as **data**, `href: "/marketplace-v2"`, so it reported one linking file and passed while the marketplace was added to the sidebar and the phone bar. Widened to `href[=:]`, it still could not cross a backtick, so a template literal `` href={`/marketplace-v2/...`} `` never matched either.
* **Never query your own hardcoded id.** See PART SEVEN.

## The honesty discipline

**Build from a log and echo the real exit code.** Piping a build to `tail` reports *tail's* exit code. One round's task runner reported exit 0 while the log said the build worker exited 1. Write the build to a file, then `echo "BUILD_EXIT=$?"` from the build itself, and read the log.

**Never trust `tsc` alone.** The Prisma client is accessed untyped in places, so the build cannot catch a column that does not exist. A round read `Clip.views`, which is not a column (views live on `ClipStat`), and only the runtime render pass caught it, in two files.

**Count with `grep -c`, never piped to `head`.** `head` truncates and the count becomes a lie. This rule is the direct cause of several enumerations in PART SEVEN being found short.

**State plainly which of your own checks failed, and which passed for the wrong reason.** Rounds here routinely report that four of their six failures were the measurement rather than the thing measured, and they report it because a round that hides them teaches the next round nothing.

**If a part could not be run, say so.** Do not imply it was. A round that changed no `.tsx` should say "no render pass was run or claimed" rather than leaving the reader to assume one.

**Do not run a build on a documentation or disk round, and do not claim one.**

## The deletion discipline

**Enumerate and classify everything before deleting any of it.** One round enumerated 99 directories at the C: root totalling 22,176 MB, classified every one, removed 85 (2,168 MB) and **left 14** (20,008 MB) because each held at least one file that existed in no repository and nowhere else on the disk.

**Prove preservation before, not after.** Another round deleted 1,614 files (9,568 MB) only after archiving 3,106 unique files, pushing the archive, and then verifying it **from origin** rather than from push output: a fresh shallow clone straight from GitHub gave the archive back byte identical by sha256.

**Act by explicit path or id, one at a time, never by wildcard.** "From a written list of 1,614 full paths, one at a time, no wildcard and no recursive directory removal."

**Re-check immediately before each action, not from a census taken an hour earlier.** Four checks ran before each unlink: the path is under a permitted root; it is still a regular file; its size still matches what was measured; its name still carries the expected suffix. For an archive, a fifth check re-listed it live.

**Print the rollback before the action.** For a schema change the rollback is printed in the migration file itself.

**Leave every unknown alone.** "Nothing was classified UNKNOWN and then deleted; everything I could not determine sits in PART 2." A failure to determine is not a determination.

**Name what would not delete rather than forcing it**, with the reason.

## What a good brief looks like, and why each part exists

The briefs used here have a consistent shape. Each part earns its place:

**An opening statement of what is known and what earlier rounds found**, with round numbers. This exists because a session has no memory and will otherwise re-derive, or worse re-break, something already settled. It also gives the round something to **disprove**, which is where the best findings come from.

**Numbered parts, each with exactly one job.** This exists because a part with two jobs gets half done twice. It also makes the verify section checkable.

**A safety section stating every constraint with the reason behind it.** The reason is the important half. A constraint without its reason gets reinterpreted by the next round as a preference and worked around. "Do not delete an editor cache" is a preference; "do not delete an editor cache because some are project state and some are regenerable and you cannot tell which from the folder name" is a constraint that survives contact.

**A build-honesty section.** This exists because the specific ways a build lies here are non-obvious and recurring: the `tail` exit code, `grep | head`, `tsc` passing on an untyped client. Stating them each time is cheaper than one more round reporting a green build that failed.

**A verify section restating what must be true at the end.** This exists so the round can check its own work against the brief's own words rather than against its memory of them, and so the reader can check the report against the same list.

**A ship line**, naming the exact path the output goes to. This exists because "publish a report" without a path produces a file nobody finds.

**An output limit.** This exists because the terminal is not the deliverable. The report is.

## The tone of a report

A round reports **what it actually found, including its own errors**. Not a summary of what it intended.

It **corrects a previous round by name** when the evidence demands it. "BL-902 named the wrong cause, and this corrects it. Verified myself. The defect and the fix in BL-902 were both real; the mechanism I named was not." That is the register.

It says plainly when **nothing is wrong**. "And the honest headline is that almost nothing is wrong. No real person hit a single refusal in thirteen hours of live use."

It distinguishes **owner action** from **code**, so the owner knows which items are waiting on him.

It is honest about **small numbers**. Below five people, say so and do not draw a trend.

It publishes a **rollback** for anything it changed.

---

# PART SEVEN — THE MISTAKES, NAMED SO THEY ARE NOT REPEATED

A rule without its scar is forgotten. Each of these is a real episode with real numbers.

## 1. Enumerations come back short

**What happened.** A round reported **eight** remaining money-writing call sites. Counted again with `grep -c`, never piped to `head`, there were **23 call sites in 15 files**, of which 18 could reach a marketplace clip. The eight was *files in one family*; there was a **second family** (`writeClipEarningsZero`, 6 more call sites in 5 more files) the earlier round had named none of.

The same round's count of agency deletion sites was **eight**; the real figure was **thirteen**, in two categories with two different safety reasons.

A round counted the shared Modal component's callers at **three**; there were **37**, and three of those already rendered their own dialog semantics, so adding semantics unconditionally would have nested two dialogs and run two focus traps against each other on every Tab.

A retrieval subagent counting balance derivations found **eleven** and missed a **twelfth** — the only load-bearing one, found by reading the route by hand. Left out, a maker's cashout would have been accepted, locked his gross into a REQUESTED row, and then thrown `INSUFFICIENT_BALANCE` on every attempt to approve it, forever. The feature would have looked complete, let him ask, and been unable to pay him.

A round auditing a scattered hardcoded value found that **both prior rounds had undercounted it**: one found four and called one of them dead, the next found a fifth and correctly called the first's "only place" claim false, and **both were still wrong — there were seven, and copies six and seven were found by neither. Copy seven was live and clipper-facing.**

That same round then nearly repeated the mistake in its own measurement, and disclosed it: a first pass with a combined `-E` alternation returned **112 hits across 14 files and silently omitted one route** through shell escaping of `\$10` — the very truncation failure the `grep -c` rule exists to prevent, arriving through a different door than `head`.

**The rule.** Count with `grep -c` and never pipe it to `head`. Then ask what the *second family* is. A count of files is not a count of call sites. Check your own pattern for escaping, because a shell can truncate a count as silently as `head` can. A count of one naming convention is not a count of the behaviour. When an enumeration feeds a decision, re-derive it from source rather than inheriting it, and say in the report how you counted.

## 2. Guards ship unable to fail

**What happened.** **Twelve** separate guard checks on this platform have been found unable to fail. Every single one was caught by **running the demonstration** rather than reading the guard.

The twelve, individually described in their own rounds: BL-835, BL-881, BL-882, BL-883, BL-884 (two in one round), BL-885, BL-887, BL-888, BL-896, and BL-898 (two more). Three of them landed in three consecutive rounds, which BL-896 says in its own words: "the third guard in three rounds to ship a check that could not fail."

**The platform's own running tally is wrong, and the way it is wrong is the same defect.** Rounds numbered themselves fifth, sixth, seventh, eighth and ninth in sequence, then BL-896 shipped one without numbering it, and BL-898 then also called itself "the tenth." The count of a defect class about undercounting was itself undercounted. Separately, the phrase "twelfth guard" does appear in the corpus and **means something else entirely** — the twelfth guard *wired into `prebuild`*. Do not read the two twelves as the same number.

The shapes, all real:

* `includes("syncV2LegsAfterPosterWrite")` passed when the call was renamed to `syncV2LegsAfterPosterWrite_DISABLED_FOR_DEMO`.
* `includes("marketplace-v2-editor-balance")` passed when an import became `"...-balanceX"`, while the file no longer imported the loader at all.
* A check skipped any file that mentioned a helper name **anywhere in it**, so replacing one of two queries with a hand-rolled filter left it green with the hand-rolled filter sitting there.
* Two checks counted across the whole file, so deleting the one occurrence that mattered left the totals above their thresholds.
* A `[^)]*` character class could not match the very line it forbade.
* A refund guard asserted a filter contained `AVAILABLE` and `PENDING`, and the regex **still matched** when `|| c.status === "PAID"` was appended to that same filter, so the one reversion that would refund money already paid to a trainer produced **zero failures**.
* A page-title guard asked only *does this page resolve to a title*, and walked up to a parent layout that has one, so **every page passed no matter what was deleted**. It asserts distinctness now, which is what the rule was always about.
* Three of nine checks had never been demonstrated at all, because their anchors were multi-line `\n` strings against CRLF files.
* A guard's demonstration matched its own tag in the guard's own printed notes.
* A guard matched only an `href=` attribute and could not see a navigation entry declared as data, then could not see one in a template literal.

**The rule.** Demonstrate every check failing, one at a time, restoring the tree between each. Match on word boundaries. Assert exact counts, not presence. Scope the count to the thing that matters. Check your anchors against CRLF. And never let the guard's own output satisfy the guard.

## 3. Unique indexes declared and never created

**What happened.** Three times.

**First:** `@@unique([submissionId, platform])` was declared on a marketplace post model with a comment asserting the index had been applied out of band. Measured against `pg_indexes`, it had **never been created**. That left the P2002 duplicate handler unreachable and allowed **two earning clips for one slot** — two concurrent posts both returned 201 and both earned. It was applied by hand a round later.

**Second:** `scheduled_calls(posterApplicationId)` was declared `@unique` and no unique index existed in Postgres. It had never been violated, so the index could be created against clean data. That sweep also established the scale: **140 declared uniqueness constraints, 1 missing**, across 1,157 compared columns.

**Third, and the worst:** `@@unique([v2ClipId, clipAccountId])` on the marketplace post table, **with a comment saying it had been applied CONCURRENTLY**. It was not in `pg_indexes` at all. `pg_indexes` on that table held the primary key, a unique on `clipId`, and three plain indexes. Nothing else.

**What it cost, exercised rather than reasoned:** one poster posted the **same clip from the same account three times and every one returned 201**. The account gate could not catch it because the URL was his own, and the URL gate could not because it matches on the normalised URL and a second link to the same video is a different URL. **Each accepted post paid a full poster leg, and paid the maker and the platform again**, so the campaign was charged three times for one piece of work.

And there is a correction on top of the correction: the round that found it reported "schema.prisma declares `@@unique` and nobody applied it." The next round verified and found **it did not declare it**. It was only ever **prose in a comment that read like a constraint**. The defect and the fix were both real; the mechanism named was not.

**The rule.** A Prisma `@@unique` enforces nothing at runtime. Before relying on any uniqueness, query `pg_indexes`. Treat a comment claiming an index was applied as an unverified claim, because twice it was false. And build the application-level branch as well as the index, so the person gets a sentence rather than a constraint name, and so a database rebuilt from the schema file by a tool that drops concurrent indexes still refuses.

## 4. Tests that test their own fixture

**What happened, case one.** An inherited check asserted "exactly one account platform-wide satisfies this exemption" while querying `WHERE id = ANY($1)` with **the literal id the test file itself declares**. It never read the real list. It would have passed with the list **empty**, and it would have passed with **a second id secretly added**, which are the only two ways that list can go wrong. Rewritten to drive the real exported predicate across all 1,766 users, it reported 0 exempt, and restoring the id was demonstrated turning **five checks red**. The old version turned none.

**Case two.** A round minted `isTestUser: true` to reach a feature, and the filter under test reads that same flag. The check was looking at a test user and correctly reported the test campaign visible. The round had **minted the very flag its own test read**.

**The rule.** A test must read production's own source of truth, not a constant it declares. Ask: would this pass if the thing it guards were empty? Would it pass if an extra entry were added? If either answer is yes, it tests nothing. And never mint the flag your assertion reads.

## 5. Proofs that pass for the wrong reason

**What happened.** A concurrency proof landed fifty posts on exactly $100.00 against a $100 budget and was read as the budget lock working. **It was not.** $100 divided evenly by that campaign's $10 per post. The lock was wrong the whole time and the evenness was hiding it. Choosing view counts so that no budget divides evenly exposed it: **40 concurrent writes against one campaign settled 40, refused 0, and spent $1,389.20 against a $500 budget.**

The real cause was that the L1 hard lock computed `delta = rounded.earnings − current.earnings`, which on a marketplace clip is **the poster's 45 percent alone**, while the balance counts all three legs. So every marketplace write was priced at 45 percent of what it would actually cost. The gap was 55 percent of every marketplace write and had existed since the marketplace could write money at all.

A first attempt at the fix **did nothing, and its own log line caught it**: it detected which Prisma client it held by the presence of `$transaction`, on the documented grounds that Prisma strips it from a transaction client. It does **not** strip it from an *extended* client's transaction client, so the guard fired on every call, the lock was **skipped 120 times**, and the re-run measured $1,389.20 unchanged.

**The rule.** When a proof passes, state what made it pass. Choose inputs that cannot divide evenly. Assert that the mechanism fired, not only that the outcome looked right. And when detecting a Prisma client type, detect by `$connect` rather than `$transaction`, and make the protection unconditional.

## 6. A failure recorded as a fact

**What happened.** A code path decided a video had been deleted by **matching the message string of a caught exception**. It is still there, at `tracking.ts:3131`: a `/not found|no results|private|removed|unavailable/i` regex run against an exception message, and it **zeroes earnings**. Matching the word `private` against an error string to decide whether to zero a person's money is not a rule anybody would write deliberately.

It is currently defanged rather than fixed, and the distinction is worth stating precisely rather than leaving as folklore: the only live string that could match it now sits behind a hard-off guard that throws a different message first, and that guard reads no environment variable, so the branch is **statically unreachable rather than merely disabled**. Measured: exactly six clips in the entire database carry a non-null `savedEarnings`, all six stamped within one second in May 2026, all six with earnings and savedEarnings of zero. No money was ever harmed by it. **It remains a loaded gun pointed at the money path and becomes reachable again the moment anybody re-enables that vendor path.**

The same class, on the Instagram side: a genuine "gone" verdict requires a 404 **and** a specific discriminator in the response body. The Instagram path never inspected the body; it ran a regex against the derived error *string*, and a second reader took the bare status. An exception message is not a fact about the world; it is a fact about what a library chose to say when something went wrong, and it changes between versions, between network conditions and between a genuine 404 and a timeout. A private account, a rate limit and a transient failure all produced the same verdict as a deleted video.

The consequence class is visible in the dead-clip cron: it marked **46 of one clipper's Instagram clips unreachable in three minutes**, moving **$256.35** out of the pool his balance is computed from and dropping his withdrawable figure from $51.99 to **$0.00**. The measured false-positive rate of that cron is **4.34 percent**. And it writes **no audit row at all**: the largest money-visible event in that clipper's history produced nothing in `audit_logs`.

**The rule.** Never derive a state from an error message. Derive it from an explicit signal, require repetition before acting (the dead-clip rule is three consecutive 404s), keep a recheck path that can reverse the verdict, and write an audit row for anything that moves money out of somebody's reach.

## 7. A list that filters only the rows it loaded

**What happened, and it hid 41 real clips from the owner for three days.** The owner's clip queue showed him **4 of 46** while his own dashboard, asked in the same minutes, counted **47 PENDING**, which is what the database held. The dashboard was right and the list was wrong.

The cause: **the status filter was a client-side filter over the 30 rows already loaded.** It was never sent to the server. The API had accepted `?status=` since May and the page had never used it. When an earlier round shrank that page from 100 rows to 30, the owner silently began seeing **8.7 percent of his pending queue and 0 percent of his flagged one, with 41 real clips unreachable for 73.5 hours.**

The same shape elsewhere, measured in one sweep: an admin payouts screen capped at `take: 200` against **221 real payout rows**; an admin user page computing the approved count, the all-time earnings tile **and the unpaid balance tile** from only the newest **50** of one clipper's **870** clips; and a poster's campaign cards counting from a `take: 2000` array **with no `orderBy` at all**, so past 2,000 rows the numbers were wrong, wrong *downward*, and not reproducible between two page loads.

A related failure of the same family: a round reported **4,968 overdue tracking jobs sitting on approved, live, earning clips**. Measured properly it was **zero** — the whole backlog sat on PAST or PAUSED campaigns. The population and the predicate had never been intersected.

**The rule.** Filter in the query, not after it. A `take:` with a client-side filter after it is a lie with a number attached, and it gets worse every time somebody tunes the page size down. If you must filter in application code, take the count from the same filtered set, never from a separate aggregate. Never order by nothing. And when you report a population, state the predicate that defines it in the same sentence.

## 8. Money computed in a new place instead of an existing derivation

**What happened.** A stamp-versus-share mismatch was measured at **$933.94** and confirmed by a second round. The cause was the same rule existing in two places and drifting apart.

**And once it reached backwards and took money people had already earned.** A feature's self-heal called `recalculateUnpaidEarnings`, which recomputed every approved unpaid clip **without the PWA bonus** and wrote the lower figure through `writeClipEarnings`. The never-below-stored guard inside that writer covers only the budget-headroom clamp, so **nothing floored the drop**, and a clipper who went quiet for two days had already-earned money reduced. The mirror of it still exists on the grant path, where a return moves already-earned money *upward*, and it was left as its own decision rather than fixed in passing.

A gentler version of the same disease cost a full audit round: an admin screen displayed the owner's amount by **recomputing it in the page** from `clip.campaign.ownerCpm`, the campaign's *current* live rate, instead of reading the stored `agency_earnings` row. After a campaign reassignment the recomputed figure disagreed with the stored one, and the owner and the round both read a correct row as a bug before anybody checked.

This is why the marketplace calculator is a separate **twin** file rather than a parameterised rewrite of the first marketplace's calculator: giving the existing function a share parameter would have put a new concern inside a function that pays real money on every tick, and a wrong default would have paid an old clip on the new split. But the one thing the twin does **not** re-implement is the bonus rule; it imports `computePartyBonusPercent` from the original, because re-implementing it would have created a second source of truth for a money rule.

The same discipline applied to a reader: a round wrote its own `where` naming a marketplace column directly, and the guard failed the build, because the thing that names that column is the predicate the reader is supposed to call. The round's own note: "My first version named it here and the guard failed the build, which is the guard working."

**The rule.** One definition, many callers. If you are about to compute a money figure, find the function that already computes it and call that. If the existing function is wrong for your case, either fix it for everybody or build a twin and say in the file why it is a twin. Never a quiet second copy.

## 9. A report's claim taken as true when the code said otherwise

**What happened.** This is the failure this whole document is written against.

**Three of four claims** a round inherited from a prior report were found not to be what shipped, on reading the files.

A retrieval subagent quoted the money writer's signature as `writeClipEarnings(db, id, { baseEarnings, bonusAmount, isApproved: true })`. **That signature does not exist.** The real one is `writeClipEarnings(tx, clipId, { earnings, baseEarnings, bonusPercent, bonusAmount }, options)`.

**Three separate retrieval subagents** read `where: { isMarketplaceClip: false }` and concluded a marketplace clip could not reach that path. A marketplace clip carries that flag **false on purpose**, so every one of those filters **selects** marketplace clips. All three were wrong the same way, in the direction that would have left money writers unprotected.

A subagent reported a navigation item was in `ownerNav`; it was not, that line was the old marketplace's item. A subagent reported an accessibility helper lived in `src/lib/url-normalize.ts`; there is no such file. A subagent reported a file's ban copy promised a third-strike ban, which was true of the *report* but the file carried a **stale header describing behaviour that had already changed**. A subagent reported the post path passes a nulled bonus config, which was literally true and whose natural conclusion was false.

And the project's own rulebook was wrong in two places: `CLAUDE.md` named `--bg-page` as a house CSS token. **It does not exist and never did** — measured at 0 definitions across 26 referencing files, silently rendering transparent, and deleting focus rings where it appeared in `ring-offset`. `CLAUDE.md` also said the tab title is just "Clippers HQ" while the root layout has always shipped "Clippers HQ — Get Paid to Clip", and taken literally the rule was a WCAG 2.4.2 failure with 43 admin pages announcing the same title.

**And this document's own instance:** three consecutive reports printed the owner's cut on a real campaign as $39.00, a spend of $139.00 and a net of $57.10, each citing the previous as confirmation. Verified against the database while writing this, the correct figures are $63.94, **$163.94** and **$82.04**. The header comment of the calculator still carries the wrong shape as an illustration.

**The rule.** For anything load-bearing, read the source yourself. A report describes what a round believed on the day it shipped; the code describes what runs. A comment is not a constraint, a schema declaration is not an index, and a subagent's summary is a lead, not a fact. Mark every relayed claim as VERIFIED or merely READ, and never let an unverified one into a document, a guard or a money path.

---

# PART EIGHT — WHAT THIS DOCUMENT DOES NOT COVER

It is a snapshot, dated **19 September 2026**, and the marketplace is four days old and changing daily. Treat every figure in PART FIVE as stale within a week and re-query it.

**Not covered here, and you must look it up:**

* The growth engine (`src/lib/growth/*`), the lifecycle cron, `EmailEvent` and `canSendMarketing`. Anything deciding who receives an email is in the always-Opus tier and has its own rules.
* The streak and level systems in detail, and the gamification surfaces.
* The tracking cron's internals: the `:00` UTC batch architecture, `checkIntervalMin`, the auto-ladder and its three stages, interval overrides, the cron heartbeat and the video-unavailability logic. Read `docs/runbooks/tracking-and-cron.md`. One rule is load-bearing enough to repeat here: **do not add a top-level `select` to the `dueJobs` findMany in `tracking.ts`**, because it breaks the auto-ladder.
* The **first** marketplace, which still exists alongside the new one, uses a **60/30/10** split, suppresses the owner's ordinary cut rather than adding it, and has its own strike, dispute and listing system. Read `docs/runbooks/marketplace-and-strikes.md`.
* The full defence stack (L1 to L4), the earnings cap and marketplace cap semantics, the live-field snapshot and the platform-fee disclosure. Read `docs/runbooks/money-and-earnings.md` and `docs/DEFENSE-STACK-ARCHITECTURE.md`.
* The deferred Float to Decimal migration, five phases, in `docs/runbooks/deferred-f020-float-to-decimal.md`.
* The full CSS and design system: the typography scale, the mobile patterns, the design skills. Read `docs/runbooks/domain-and-ui.md`. The always-on rules are in `CLAUDE.md` and are short: dark theme only, accent `#2596be`, CSS variables never hardcoded colours, lucide-react icons only, no emojis, **no dashes as bullets**, mobile-first from 375px, and `data-no-swipe` on any new overlay or the global swipe handler eats its taps.
* `BACKLOG.md` in the repository root is the standing source of truth for ideas, decisions and deferrals. It is large; append to it by shell and grep the slice you need rather than reading it whole.

**Explicitly unverified in this document:** the claim that the budget-lock defect went unnoticed for "about twenty rounds" is not stated numerically in any report. What is stated is that the gap "has existed since v2 could write money at all," and that is what PART SEVEN says instead.

**One count in PART SEVEN was corrected after the first draft and the correction is itself instructive.** This document initially said "at least ten" guards had shipped unable to fail, because the reports' own running tally stops at ten. A sweep of all 222 reports then found **twelve** individually described instances, and showed that the tally is wrong in exactly the way PART SEVEN's first entry describes: one round shipped an instance without numbering it and the next round reused the number. A document about undercounting had undercounted, from the same source, in the same direction. It is twelve.

**Two domain rules that are absolute and easy to break by accident:** the domain is **clipershq.com** with one P, and **Belgrade and Serbia are never shown on any frontend page**.

**Finally.** New or redesigned user-facing surfaces are gated behind `isTestUser` unless you are told otherwise, and every non-test user must be byte identical to before. When you are unsure which model tier a task belongs to, use the more expensive one. Correctness over cost, every time.
