# BL-834: the trainer referral system, designed before any code

**2026-09-03 · DB `now()` = `2026-09-03 21:08:36.627127+00` (first read) to `2026-09-03 21:17:28.749264+00` (last) · AUDIT AND DESIGN ONLY.**
Base `origin/main` @ `fdce6afd`. Branch `checkpoint/BL-834`. Isolated worktree `C:/w834`, a short path, `node_modules` never junctioned, **removed at the end**. Every database read through `scripts/run-select.js` (read only, refuses every write keyword); every timestamp cast `::text` against DB `now()`. Handles redacted; no wallet address read or printed. **Nothing was built. No file in `src/`, `prisma/`, `scripts/` or any config was created, edited or deleted. The whole diff is this one markdown file.**

---

## THE SHORT VERSION, BEFORE THE DETAIL

**There is exactly one shape for the 10 percent that cannot breach a single one of this platform's five hard money properties, and it is not the obvious one.** The obvious design takes 10 percent of a clipper's earnings. That design is fatal here, because `Clip.earnings` is a figure the platform has already settled in cash against, and reducing it is precisely the defect BL-716 created at $60.47 and BL-824 spent a whole round encoding against for seven clippers. The safe design never touches earnings at all. It takes the 10 percent as a **fourth deduction line on the payout row**, computed once at withdrawal, stamped on that row beside the 9 percent platform fee and the 4 percent express premium, and subtracted in exactly the same breath. The trainer is then credited through a **downstream ledger row keyed uniquely to that finished payout**, which is the shape the existing 5 percent referral commission already uses and the reason that system has never breached anything.

**Three facts from live data change how the owner should read this whole round.**

1. **The existing 5 percent referral system has paid out $0.00. Ever.** 7 commission rows have been minted in the platform's life, totalling $111.53 gross, of which $107.02 sits VOIDED and $4.51 sits AVAILABLE. Zero rows are PAID, zero cashout payouts exist, and there are zero `REFERRAL_CASHOUT_REQUESTED` audit rows. The owner is not building a second version of a working system; he is building a second version of a system whose money end has never once completed.
2. **The 5 percent comes out of the PLATFORM's pocket, not the clipper's.** A referred clipper's cash is not reduced by one cent for their inviter. The platform collects 4 percent instead of 9 and then pays the inviter 5 percent of the 96 percent, which nets the platform **minus $0.80 on every $100** of referred withdrawal. The trainer's 10 percent comes out of the CLIPPER's pocket, by the owner's own instruction. **These are two different kinds of thing and one mechanism cannot serve both.**
3. **The referral link is not permanent, and its removal has already destroyed money.** All 5 VOIDED commissions, $107.02, belong to clippers whose `referredById` is now NULL. `audit_logs` holds **67 `REFERRAL_OVERRIDE_REMOVED` rows across 67 distinct users** between `2026-05-30 19:47:12.48` and `2026-06-19 02:11:00.78`. The live copy on the referrals page says the 5 percent is earned **"forever"**. It is not.

---

# PART 1: WHAT ALREADY EXISTS, BECAUSE THIS IS THE SECOND REFERRAL SYSTEM

## 1.1 How a code is issued

| thing | fact | source |
|---|---|---|
| column | `referralCode String? @unique` | `prisma/schema.prisma:184` |
| format | **8 characters** from `ABCDEFGHJKLMNPQRSTUVWXYZ23456789` | `src/lib/referrals.ts:8-13` |
| alphabet | 32 symbols: A to Z minus **I** and **O**, digits **2 to 9** (no 0, no 1) | same |
| randomness | `Math.random()`, not `crypto` | `referrals.ts:11` |
| derived from username? | **No.** Nothing about the code is derived from the user | same |
| collisions | 5 attempts, each relying on the DB `@unique` to throw; `catch {}` is untyped so any error burns a retry; returns `null` after 5 | `referrals.ts:22-31` |
| idempotent | Yes. An existing code is returned untouched | `referrals.ts:19` |

**Issuance is LAZY, from exactly two callers.** `GET /api/referrals` mints one on page load (`src/app/api/referrals/route.ts:147`), and `PATCH /api/admin/users/[id]/reviewer-config` mints one on a REVIEWER grant (`route.ts:511-512`, non fatal by design). There is no signup time issuance. BL-799 recorded the closed loop verbatim: *"No code without the page, no page without the flag, no invitees without the code."*

**BL-799 backfilled 1,039 live code-less users** (1,009 CLIPPER, 11 REVIEWER, 19 CLIENT), 0 failures, through `scripts/bl-799-backfill-referral-codes.js` with the NULL guard in the `WHERE` clause so a concurrently minted code could never be clobbered. The ledger `scripts/bl-799-referral-code-ledger.json` (82,180 bytes, 1,039 entries) is deliberately **untracked**, because it pairs user ids with codes.

**Live today:** 1,646 users, **1,392 hold a code**, 254 do not. The 254 are the accumulation since BL-799 plus soft deleted rows.

## 1.2 How attribution is recorded

**Signup only, through a cookie, silently.**

```
/login?ref=<code>  → document.cookie = referral_code=<code>; max-age=86400; samesite=lax   (login/page.tsx:148)
/login?inv=<code>  → document.cookie = owner_referral_link=<code>                          (login/page.tsx:194)
NextAuth events.createUser → attachOwnerReferralLink first (auth.ts:1073), then attachReferral (auth.ts:1078)
```

`attachReferral` (`src/lib/referrals.ts:35-59`) writes `referredById` and refuses: an already referred user, a self referral, a `BANNED` inviter, a soft deleted inviter. The whole body is wrapped in `try / catch { return false }`, so **every failure is silent**. `attachOwnerReferralLink` (`src/lib/owner-referral.ts:64-131`) additionally refuses an inactive link, an expired link, and an inviter whose role is not `CLIPPER`, and writes an `OWNER_REFERRAL_LINK_SIGNUP_ATTRIBUTED` audit row.

**THE STRUCTURAL FACT THAT MATTERS MOST FOR THE TRAINER SYSTEM: there is no way for an existing clipper to enter a code.** Attribution happens once, at account creation, from a cookie. The owner's trainer concept requires an existing clipper to type a code and become a trainee. **That capability does not exist anywhere in this codebase and has to be built new.** It is the single largest piece of genuinely new surface in the whole feature.

## 1.3 Whether it can be lost or changed

**Yes, and only by the owner.** Every write to `referredById`, exhaustively:

| site | direction |
|---|---|
| `src/lib/referrals.ts:56` | set, at signup, never overwrites |
| `src/lib/owner-referral.ts:108` | set, at signup via `?inv=`, also sets `ownerReferralLinkId` |
| `src/app/api/admin/referral-override/route.ts:259` | **set or change** |
| `src/app/api/admin/referral-override/route.ts:377` | **clear to NULL** |
| `scripts/bl-strip-referrers-2026-06-19.ts:76` | clear, one off script |

`/api/admin/referral-override` is `assertOwner` (re-read from the DB, not the token), rate limited 30 per hour, refuses a self reference, refuses a non CLIPPER on either side, refuses a `BANNED` referrer, and runs **`wouldCreateCycle`, a chain walk up to 50 hops with a `visited` set** (`route.ts:53-71`). On change it calls `voidUnpaidLink` (`route.ts:80-96`), which flips `AVAILABLE` and `PENDING` commissions on that exact pair to `VOIDED` and **never touches `PAID`**, on a written accept-loss policy.

**Measured consequence: the removal power has been used 67 times and it has voided real money.**

| measure | value |
|---|---|
| `REFERRAL_OVERRIDE_REMOVED` audit rows | **67**, across **67 distinct users**, `2026-05-30 19:47:12.48` to `2026-06-19 02:11:00.78` |
| `REFERRAL_OVERRIDE` audit rows | 1, `2026-04-25 17:34:20.649` |
| users currently carrying `referrerOverriddenBy` | **0** |
| VOIDED commissions whose clipper now has `referredById` NULL | **5 of 5**, $107.02 |

None of those 5 clippers is a test user and none is deleted. The link was removed after the commission existed, and the commission died with it.

## 1.4 When the 5 percent is calculated, and where the money comes from

**There are two independent mechanisms on the same column, and they are not the same thing.**

### (a) The fee discount, 9 percent becomes 4 percent

`DEFAULT_PLATFORM_FEE = 9` and `DEFAULT_REFERRED_FEE = 4` at `src/lib/earnings-calc.ts:44-45`. The charge is decided **live at payout creation** from `referredById`: `src/app/api/payouts/route.ts:447`, `const feePercent = payoutUser?.referredById ? 4 : 9;`. A per clip snapshot also exists, `Clip.feePercentAtApproval` (`schema.prisma:947`), stamped at `clips/[id]/review/route.ts:763` and `:890`, but `BACKLOG.md:1297-1299` states it is **forensic only** and it does not enter the charge. Live distribution across approved clips: **4 percent on 859 clips ($3,284.00), 9 percent on 6,108 clips ($11,080.52), NULL on 443 ($1,612.50)**.

### (b) The commission, 5 percent to the inviter

Minted when the **referred** clipper's payout flips to `PAID`, in `src/app/api/payouts/[id]/review/route.ts`, block `:616-796`:

```
:766  effectivePaid = actualPaidAmount ?? finalAmount ?? amount
:770  RATE_BPS = 500
:771  commissionAmount = round2(effectivePaid * 500 / 10000)
:774  db.referralCommission.create({ ..., rateBps: 500, status: "AVAILABLE" })
```

**The base is the NET CASH the referred clipper actually received, after the platform fee, after any express premium, and after any owner adjust down.** That is the single most load bearing fact for this design: **a percentage on this platform is already deliberately applied to the net, not the gross.**

**Traced to the query and reproduced on all 7 live rows.** Every source payout is `feePercent = 4`, `STANDARD`, so `finalAmount = amount × 0.96`, and the commission is 5 percent of the cash:

| source gross | source cash | actualPaidAmount | commission | check |
|---|---|---|---|---|
| 757.20 | 726.91 | 629.5200 | **31.4800** | 629.52 × 0.05 = 31.476 |
| 10.46 | 10.04 | null | **0.5000** | 10.04 × 0.05 = 0.502 |
| 310.85 | 298.42 | null | **14.9200** | 298.42 × 0.05 = 14.921 |
| 1,044.17 | 1,002.40 | null | **50.1200** | 1002.40 × 0.05 = 50.12 |
| 208.31 | 199.98 | null | **10.0000** | 199.98 × 0.05 = 9.999 |
| 53.06 | 50.94 | null | **2.5500** | 50.94 × 0.05 = 2.547 |
| 40.79 | 39.16 | null | **1.9600** | 39.16 × 0.05 = 1.958 |

### Whose pocket

**Not the clipper's.** The referred clipper's `finalAmount` is not reduced by one cent for their inviter. The commission is a fresh liability, cashed out through a **separate `PayoutRequest` with `campaignId: null` and `finalAmount: total`, no fee at all** (`payouts/referral-request/route.ts:156-165`). It never touches `Clip.earnings`, `AgencyEarning`, or any campaign budget.

**So it comes out of the platform's own share, and the platform runs a small loss on it.** On $100 of referred withdrawal: platform collects $4.00 in fee, pays $4.80 in commission, **nets minus $0.80**. Against $9.00 on the same withdrawal from a non referred clipper. That is a live arrangement the owner chose, stated here so he can see it before adding a second rate on top of it.

## 1.5 The scale of the thing he is building a second version of

| measure | value | note |
|---|---|---|
| users | **1,646** | |
| holding a referral code | **1,392** | 84.6 percent, almost all from BL-799's backfill |
| carrying a `referredById` | **188** | 11.4 percent |
| distinct referrers | **42** | |
| referred clippers with at least one APPROVED clip | **44** of 188 | 23.4 percent |
| `referral_clicks` rows | **437** | |
| commission rows ever minted | **7** | |
| **total commission ever minted** | **$111.53** | 5 VOIDED $107.02, 2 AVAILABLE $4.51 |
| commission rows `PAID` | **0** | |
| referral cashout payout rows | **0** | |
| `REFERRAL_CASHOUT_REQUESTED` audit rows | **0** | |
| **total 5 percent ever paid to a human** | **$0.00** | |
| `OwnerReferralPayment` rows, recorded by hand | **6**, **$195.80** | the only referral money that has ever reached anyone |
| `OwnerReferralLink` rows minted | **53** | 70 signups attributed |
| invitees held by the largest referrer | **28** | then 21, 17, 16, 15, 13, 8, four at 5, three at 4, two at 3, six at 2, twenty at 1 |
| real clippers | **1,590** | 27 REVIEWER, 20 CLIENT, 3 OWNER, 0 ADMIN |
| clippers who submitted a clip in the last 30 days | **117** | 92 had one approved |

**Reconciliation against the reports, so no figure floats.** BL-799 measured **6 rows and $109.57** on `2026-08-12`. Today is 7 and $111.53. The delta is exactly one AVAILABLE row of **$1.96** minted `2026-08-13 21:17:34.209`, and `109.57 + 1.96 = 111.53` to the cent. BL-788 measured **174 `referredById` edges and 36 inviters** on `2026-08-12`; BL-812 measured **178 of 1,430 users**; today it is **188 of 1,646 and 42 inviters**. The graph is growing slowly and the money end is not moving at all.

**Figures carried from the reports and NOT reproduced this round, named rather than implied:** BL-823's seven owed clippers ($121.28 gross, $110.37 cash; $122.73 and $111.69 on the day BL-824 shipped), BL-716's $60.47, BL-570's $933.94 of ambiguous owner rows, and BL-627's $142.59 realised over hold. Re-measuring any of them is outside this round's scope and each is a settled or deliberately frozen figure.

## 1.6 EXTEND IT, OR SIT BESIDE IT

**SIT BESIDE IT. Four reasons, each independently sufficient.**

1. **`ReferralCommission` permits exactly one row per source payout.** `@@unique([sourcePayoutRequestId])` at `schema.prisma:1428`. A trainer credit cannot stack alongside a referrer credit on the same payout without changing that constraint, and that constraint is the whole idempotency guarantee (a duplicate mint currently fails with P2002 and is swallowed as a no-op). Loosening it to `@@unique([sourcePayoutRequestId, referrerId])` would work, but it weakens the guard that has kept this ledger clean, on a table whose money end has never once completed.
2. **The two percentages come out of different pockets.** The 5 percent is platform cost. The 10 percent is clipper cost. The clipper's `finalAmount` must fall for one and must not fall for the other. There is no single field, single rate and single resolver that expresses both.
3. **`referredById` is set at signup only and is single valued.** Reusing it forces a clipper to choose between having an inviter and having a trainer, and provides no path for an existing clipper to opt in later.
4. **The rate resolution in the existing mint is a boolean, not a lookup.** `isOverridden` at `payouts/[id]/review/route.ts:695-763` picks 5 percent or 0 percent. A third rate does not fit that shape at all.

**Concretely, sitting beside means:** new nullable columns on `User` (`trainerId`, `trainerCode`, `trainerJoinedAt`, `isTrainer`), added additively through `scripts/run-schema-sql.js` and **never `prisma migrate`**, exactly the way BL-788 added `reviewerScopeInvitedOnly`; a new stamped pair on `PayoutRequest` (`trainerCutPercent`, `trainerCutAmount`), exactly the shape of `expressFeePercent` and `expressFeeAmount`; and a new credit table with its own unique constraint.

## 1.7 BOTH REFERRED AND TRAINED, BY DIFFERENT PEOPLE

**Structurally there is no conflict, because they are independent columns doing independent jobs.** A clipper may carry `referredById = A` and `trainerId = B` with no interference: A's claim is on the platform's share, B's claim is on the clipper's.

**Arithmetically there IS a collision, and it is real.** The referrer's 5 percent is computed on the clipper's `finalAmount`. A trainer deduction that lands inside `finalAmount` **silently shrinks the referrer's commission**:

| clipper's situation | clipper cash on $100 | referrer's 5 percent |
|---|---|---|
| referred, no trainer | $96.00 | **$4.80** |
| referred, trainer takes 10 percent of gross | $86.00 | **$4.30** |

**The referrer loses $0.50 per $100 because their invitee chose a trainer, and nobody told them.** That is not a bug the design can decide away; it is a policy question and it is **Q6**.

Three sub cases must also be refused or decided at the server rather than left to arithmetic:

• **Trainer and referrer are the same person.** Today they would be paid twice on one withdrawal, once out of the platform and once out of the clipper. Whether that is allowed is **Q7**.
• **A trainer is themselves a trainee.** `wouldCreateCycle` already exists and already walks 50 hops, which is proof multi hop chains exist in the data. Nothing currently pays beyond one hop and nothing should start to without a decision.
• **A clipper's trainer is their own invitee.** Measurable, and a collusion signal rather than a rule. **Q20**.

---

# PART 2: THE MONEY, DEFINED TO THE CENT AND STACKED IN ORDER

## 2.1 The arithmetic as the codebase actually does it today

`calculatePayoutBreakdown` (`src/lib/payout-calc.ts:55-95`), called at `payouts/route.ts:463`:

```
feeAmount        = round2(amount × feePercent / 100)         feePercent = 9, or 4 if referredById
expressFeeAmount = round2(amount × expressPct  / 100)        expressPct = 4, EXPRESS only, else 0
finalAmount      = round2(amount − feeAmount − expressFeeAmount)
```

**Both percentages are taken off the SAME GROSS base and then subtracted. Nothing compounds.** BL-812 asserted this over 380,000 combinations from $10.00 to $2,000.00 at both fee rates with **0 violations**: express is always 4 percent on top and never instead, the base fee never changes between speeds, and cash never exceeds gross.

**Verified live on all 110 PAID payouts today:**

| speed | fee | rows | gross | cash | express collected |
|---|---|---|---|---|---|
| STANDARD | 4 | 10 | $2,920.49 | $2,803.68 | none |
| STANDARD | 9 | 56 | $5,547.70 | $5,048.37 | none |
| EXPRESS | 9 | 44 | $3,765.32 | $3,275.85 | **$150.62** |

`2,920.49 × 0.04 = 116.82` against the observed `116.81` gap. `3,765.32 × 0.09 = 338.88` plus `150.62` express is `489.50` against the observed `489.47`. Both inside per row rounding.

**And the crucial asymmetry, quoted from `earnings-calc.ts:187-189`: the fee is "calculated for reference but NOT subtracted... Fee is applied once at payout time, not at earnings calculation time."** Everything on the earnings side is GROSS. The clipper's **balance is consumed by the GROSS `amount`, never by `finalAmount`** (`balance.ts:126-132`, `clipperLiability = actualPaidAmount ?? amount`). The fee is revenue taken out of the middle.

**That asymmetry is the entire safety argument for the trainer design.** A deduction that lives only in `finalAmount` is invisible to the balance, invisible to `Clip.earnings`, and invisible to the withdrawal gate.

## 2.2 The $100 worked example, every order, every figure as gross and as cash

A clipper has earned **$100.00 gross** and requests all of it. The trainer takes 10 percent. Machine derived, `round2` at every step, exactly as `payout-calc.ts` rounds.

### Order A, 10 percent of the GROSS withdrawal

| step | figure |
|---|---|
| clipper requests, gross | **$100.00** |
| balance consumed, gross | **$100.00** (unchanged by any of this) |
| platform fee, 9 percent of gross | **minus $9.00** |
| trainer cut, 10 percent of gross | **minus $10.00** |
| **clipper receives, cash** | **$81.00** |
| trainer credited, gross | **$10.00** |
| trainer pays 9 percent on withdrawal | minus $0.90 |
| **trainer receives, cash** | **$9.10** |
| **platform receives** | **$9.90** ($9.00 plus $0.90) |

### Order B, 10 percent of what is left after the platform fee

| step | figure |
|---|---|
| gross | $100.00 |
| platform fee 9 percent | minus $9.00 |
| subtotal | $91.00 |
| trainer cut, 10 percent of $91.00 | **minus $9.10** |
| **clipper receives, cash** | **$81.90** |
| trainer gross $9.10, less 9 percent $0.82 | **trainer cash $8.28** |
| **platform receives** | **$9.82** |

### Order C, 10 percent of what is left after ALL fees, including express

| step | figure |
|---|---|
| gross | $100.00 |
| platform fee 9 percent | minus $9.00 |
| express premium 4 percent | minus $4.00 |
| subtotal | $87.00 |
| trainer cut, 10 percent of $87.00 | **minus $8.70** |
| **clipper receives, cash** | **$78.30** |
| trainer gross $8.70, less 9 percent $0.78 | **trainer cash $7.92** |
| **platform receives** | **$13.78** |

**Order A costs the clipper $0.90 more than Order B on every $100, and gives the trainer $0.82 more.** With no express, Orders B and C are identical.

### The full stack, Order A, every combination

| clipper | plat fee | express | trainer gross | **clipper cash** | trainer cash | platform net |
|---|---|---|---|---|---|---|
| not referred, standard, no trainer | $9.00 | none | none | **$91.00** | none | $9.00 |
| not referred, standard, trained | $9.00 | none | $10.00 | **$81.00** | $9.10 | $9.90 |
| not referred, EXPRESS, trained | $9.00 | $4.00 | $10.00 | **$77.00** | $9.10 | $13.90 |
| referred, standard, no trainer | $4.00 | none | none | **$96.00** | none | **minus $0.80** |
| referred, standard, trained | $4.00 | none | $10.00 | **$86.00** | $9.10 | $0.60 |
| referred, EXPRESS, trained | $4.00 | $4.00 | $10.00 | **$82.00** | $9.10 | $8.90 |

Platform net includes the referrer's fee free 5 percent commission where one applies ($4.80 when untrained, $4.30 when trained). The worst case total deduction from a clipper's gross is **23 percent** (9 plus 4 plus 10), and the best is **14 percent** (4 plus 10).

## 2.3 The owner's three stated money rules, checked one at a time

| his rule | does Order A satisfy it? |
|---|---|
| the 10 percent comes out of the CLIPPER's pocket, never the platform's | **Yes.** The clipper's cash falls from $91.00 to $81.00. The platform's take is unchanged at $9.00 plus whatever the trainer pays. |
| it must not touch the existing 9 percent | **Yes.** `feePercent` and `feeAmount` are computed and stored exactly as today. The cut is a separate stamped field, subtracted separately. |
| the trainer pays the 9 percent on their 10 percent when they withdraw | **Yes, but this DIVERGES from the only precedent.** The existing referral cashout takes **no fee at all**: `payouts/referral-request/route.ts:165`, `finalAmount: total, // commissions have no platform fee`. BL-813 found that this fee free path produced the **single exactly correct payout notification in 106 messages**, because gross equalled cash. A trainer cashout that charges 9 percent must therefore carry a fee breakdown the referral cashout has never needed. **Q8.** |

## 2.4 THE HARD QUESTIONS THIS SECTION RAISES AND DOES NOT ANSWER

These are listed here and answered nowhere in this document. They are Q3, Q4 and Q5 in PART 7.

• **Does the 10 percent apply to earnings from clips submitted BEFORE the clipper joined the trainer?** Under the withdrawal design the cut lands on a withdrawal, and a withdrawal mixes old and new clips indiscriminately, so answering "no" is not a copy change: it requires per clip attribution against a stamped `trainerJoinedAt`, a per clip eligible subtotal at request time, and a materially larger build. Answering "yes" is one line.
• **Does it apply to money already earned but not yet withdrawn?** Live figure so the owner can size it: **142 clippers hold $2,698.89 of approved, unwithdrawn earnings right now, and 26 of those are referred clippers holding $287.38.** Anyone who joins a trainer tomorrow is sitting on a balance earned entirely without one.
• **Does it stop the moment they leave, or continue on clips posted while they were trained?** "Continue" has the same per clip attribution cost as the first question, plus it requires the pairing row to survive the leaving so the stamp is still readable.

---

# PART 3: EVERY INVARIANT THIS COULD BREAK, CHECKED ONE BY ONE

**The design, stated once, precisely, because every answer below depends on it.**

1. `Clip.earnings`, `Clip.baseEarnings` and `Clip.bonusAmount` are **never written** by any trainer code path. Nothing calls `writeClipEarnings`. `tracking.ts` is not in the diff.
2. The clipper's **balance is consumed by the gross `amount`**, exactly as today, unchanged.
3. The cut is computed **once, at payout creation**, and stamped on that payout row as `trainerCutPercent` and `trainerCutAmount`, then subtracted in `calculatePayoutBreakdown`: `finalAmount = amount − feeAmount − expressFeeAmount − trainerCutAmount`.
4. The trainer's credit row is minted **only when the source payout flips to `PAID`**, keyed uniquely to `(sourcePayoutRequestId, trainerId)`.
5. **A payout row, once written, is never recomputed by any trainer code.** There is no path that walks historical payouts applying a rate.

## 3.1 BL-627, nobody can withdraw more than they earned

**Preserved, because the design does not touch the gate's arithmetic at all.** The invariant is `available = max(earned − paidOut − locked, 0)`, derived on every read at `payouts/route.ts:483`, with `effectiveCap = Math.min(available, globalAvailable)` at `:689`. Its inputs are `Clip.earnings` and `payout_requests.amount`. **The trainer path writes neither.** The cut reduces `finalAmount`, which the gate never reads.

On the trainer's own side the same property must hold and it does by construction: a trainer can only withdraw against credit rows in `AVAILABLE`, each of which is minted from a payout that has already completed, and each of which is flipped to `PAID` inside the withdrawal transaction so it cannot fund a second one.

Measured now, so the baseline is on the record: **0 invariant violations across 6,467 approved live clips** ($12,301.96 total, base $11,746.21, bonus $555.76).

## 3.2 BL-696, nobody can be paid twice

**Preserved by a unique constraint, not by care.** `@@unique([sourcePayoutRequestId, trainerId])` on the credit table makes a duplicate mint a P2002, which is the exact mechanism the existing commission already relies on and which BL-696 proved. The withdrawal must copy the referral cashout's shape verbatim: a Serializable transaction, an in transaction re-read asserting every row is still `AVAILABLE`, a sentinel race error mapped to 409, and 3 attempts with backoff on P2034 (`referral-request/route.ts:128-198`).

**ONE HOLE MUST BE NAMED RATHER THAN INHERITED SILENTLY.** `uq_payout_open_per_user_campaign` is a **partial btree unique** on `("userId","campaignId") WHERE status IN ('REQUESTED','UNDER_REVIEW','APPROVED')`. A commission cashout carries `campaignId: null`, and btree treats NULLs as distinct, so **the index does not constrain it**. BL-696 named this limit for the referral cashout. A trainer cashout inherits it exactly. It is bounded in practice, because a first request consumes every `AVAILABLE` row and leaves the second with nothing to claim, but the bound is a consequence of the ledger rather than a guarantee from the database. If the owner wants the same hard guarantee the campaign payouts have, it needs its own partial unique on `("userId") WHERE "campaignId" IS NULL AND status IN (...)`.

## 3.3 BL-824, recorded earnings may never fall below money already paid

**Preserved, because the quantity BL-824 protects cannot move.** The rule is encoded once, in `src/lib/balance.ts`, as `effectivePaid(campaign) = min(paidGross(campaign), payableEarnings(campaign))`, routed through three call sites (`computeBalance`, the withdrawal gate's global clamp, and `campaigns/[id]/min-payout-impact`) and guarded by `scripts/bl824-paid-is-final.ts`, 14 checks. Both inputs are untouched: `paidGross` reads `payout_requests.amount`, which is the **gross** and is not reduced by the cut; `payableEarnings` reads `Clip.earnings`, which the trainer path never writes.

**BL-824's own honest note stands and must be repeated here rather than smoothed over:** after that fix, three clippers' recorded earnings legitimately sit **$60.47, $0.80 and $0.02 below** what they were paid, because the record was reduced later, not because they were overpaid. That is arithmetically possible today, before any trainer code exists, and the trainer design neither improves nor worsens it.

## 3.4 BL-538, the never decrease guard

**Preserved, because nothing in the trainer path is a recompute.** `decideNeverDecrease` (`src/lib/earnings-never-decrease.ts:77`) has exactly two callers, `admin/force-recalc-earnings/route.ts:13` and `campaign-freeze-undo.ts:84`, and the BL-718 paid floor `capButNeverBelowStored` (`:170-185`, `return proposed >= stored ? proposed : stored`) is wired inside `clip-earnings-writer.ts:385`. The trainer path calls none of them because it computes no clip earnings.

**And the reason BL-716 breached this must be stated, because it is the exact trap this design is shaped to avoid.** The defect was `tracking.ts:2507`, an **absolute assignment with no floor at the clip's stored value** inside a shared pool, so one clipper's recorded earnings fell $60.47 because other clippers' rose. Every sibling branch in the same function is guarded (`:2236`, `:2271`, `proportional-cut.ts:110`, `clip-earnings-writer.ts:152`, which states plainly *"Decreases always pass"*). **A trainer cut implemented as a reduction of a shared quantity would be the same defect with a different name.** A cut implemented as a stamped subtraction on a write once row cannot be.

## 3.5 BL-539 and BL-570, no stamp versus share ambiguity

**Preserved, and this is the subtlest of the five.** BL-539's finding is that a per row stamp (`clips.ownerCpmAtSubmissionDecimal / clips.cpmAtSubmissionDecimal`) disagreeing with a per campaign live constant (`campaigns.lockedOwnerShareDecimal`) makes a row **permanently ambiguous**: two defensible figures and no data able to pick between them. BL-570 measured the somesome slice at **$933.94** on 108 rows, up from BL-539's $889.03 in 28 days, and named the trigger precisely: the rows are protected only by the era boundary, and `eraExempt = true` would rewrite them silently on the first tick.

**The trainer design cannot produce that shape, because the rate has no live counterpart to disagree with.** `trainerCutPercent` is stamped on the payout row at creation and read back from that row forever. There is no campaign level trainer constant, no derived `k`, and no path that re-derives the cut from a current user column. **A stamp with nothing to disagree with cannot become ambiguous.**

**Two corollaries that must be honoured or the property is lost.** The stamped percent must be **read back and never re-derived** on any display, email or admin surface (BL-813's rule: the percentage is interpolated from the row, never written as a literal, because it is 9 for most and 4 for a referred clipper and a hardcoded literal is wrong for everyone else). And the credit row must carry its own `rateBps`, the way `ReferralCommission.rateBps` does, so a later rate change cannot reprice history.

## 3.6 THE SHARPEST RISK, STATED PLAINLY

**If the 10 percent were applied to EARNINGS rather than to a WITHDRAWAL, it would recreate the defect BL-824 just fixed for seven clippers, and it would do so for every trained clipper at once.**

The mechanism is exact. A clipper's recorded earnings are the only quantity the withdrawal gate reads, and **money already paid has already been subtracted against them**. Reduce recorded earnings by 10 percent, or clamp available balance against a trainer liability computed over lifetime earnings, and the base of that reduction necessarily includes **every dollar the clipper has already withdrawn and spent**. The record then sits below the cash, the balance clamps at $0.00, there is no clawback path, and the money is unrecoverable in both directions. BL-627 measured that realised population at **5 clippers and $142.59**, "already paid, clamped at $0, unrecoverable and NOT growing", and its own prescribed prevention is the sentence this design obeys: **"block PRR-reduce / reject on clips whose earnings already funded a PAID payout."** BL-716 wrote the rule and BL-824 encoded it: *"A payment, once made, is a floor... the trim comes off unpaid headroom first and off already paid earnings never."*

**How this design prevents it, structurally rather than by discipline, in four sentences.**

1. **The cut has no representation on the earnings side at all.** There is no column on `Clip`, no term in `earnings-calc.ts`, and no branch in `tracking.ts`. There is nothing for a cron tick, a force recalc, an era resume or a budget trim to apply it to.
2. **The cut exists only as two numbers on a `PayoutRequest` row**, and a `PayoutRequest` row is created once, at the moment the clipper presses the control, from a figure the clipper was shown before pressing.
3. **No trainer code path reads a historical payout.** The mint reads exactly one payout, the one transitioning to `PAID`, and it only ever writes a new credit row.
4. **Therefore money already paid is untouchable by arithmetic and not merely by policy.** A clipper who withdrew $500 last month and joins a trainer tomorrow pays the trainer nothing on that $500, because there is no code that could.

**One live consequence of this shape must be disclosed to the owner rather than buried: it means the trainer earns nothing on work already withdrawn, and nothing on the $2,698.89 currently sitting in 142 clippers' balances unless the owner answers Q4 "yes".** That is a real cost of the safe design and he should choose it knowingly.

## 3.7 THREE INTEGRATION HAZARDS THE BRIEF DID NOT NAME, EACH FOUND BY READING

**(a) A fourth deduction silently breaks BL-813's reconciliation gate, and the failure mode is a message telling honest clippers their payout looks wrong.** `src/lib/email.ts:651-671` renders the fee breakdown **only** when the stored parts reconcile:

```
:655  reconciles = Math.abs(breakdown.requested - fee - xfee - amount) <= 0.01
:671  else → "This was adjusted before sending. Message us on Discord if it looks wrong."
```

Add a `trainerCutAmount` that is not in that subtraction and **every trained clipper's payout email fails the check and falls back to the adjusted sentence**, on a payout that was not adjusted at all. This must be extended in the same diff. It is the single most likely thing to be missed.

**(b) The rate is stated in seven places today and none is the source of truth.** `RATE_BPS = 500` at `payouts/[id]/review/route.ts:770`, again at `referral-backfill.ts:21`, a bare `500` at `admin/payouts/[id]/adjust/route.ts:544`, a hardcoded `* 0.05` at `ReferralsRedesign.tsx:356`, and again at `admin/referrals/page.tsx:656` and `:1059`, plus `DEFAULT_REFERRAL_PERCENT = 5` at `earnings-calc.ts:50` which is display only and feeds no money write. **The trainer rate must be one exported constant, named once, and BL-821's lesson applies: one rule, not two.**

**(c) The trainer path would be the second money system on this platform with no invariant middleware.** `writeClipEarnings` carries an invariant assertion, an L1 budget hard lock that throws, the BL-167 pool clamp, the BL-718 paid floor, audit-before-throw, and fail open with alerting. The referral commission path carries **none of it**: `attachReferral` swallows every error, the mint's only guard is a P2002 catch, and the link resolution error path deliberately **pays** on failure. That asymmetry is survivable at $111.53 of lifetime exposure. At 10 percent of every trained clipper's withdrawals it is not, and the credit ledger should carry at minimum an audit row written inside the mint transaction, on BL-815's stated rule that *"a move that cannot be audited does not happen"*.

---

# PART 4: THE LEAVING PROBLEM, WHICH IS WHERE DISPUTES LIVE

## 4.1 Who decides, and what the platform must actually do

**There is a shipped dispute machine to copy, and it should be copied rather than reinvented.** `MarketplaceStrike` (`schema.prisma:2713-2746`) carries the whole lifecycle: `status` (`ACTIVE | DISPUTED | RESOLVED | EXPIRED`), `disputedAt`, `disputeThreadId`, `resolvedAt`, `resolvedById`, `resolutionNote`, plus denormalised context *"because the source submission may be deleted while the dispute history must persist"*. Its resolver is `PATCH /api/admin/marketplace/disputes/[id]/resolve`, which refuses anyone whose `role !== "OWNER"` (`route.ts:65`), takes a verdict, writes `resolutionNote`, is **idempotent on an already RESOLVED row** (`:119`), and writes an audit row `STRIKE_DISPUTE_RESOLVED` (`:336`).

**So the answer to "who decides" is: the owner, and the platform already knows how to let him.** Whether a reviewer capability could ever judge one is **Q15**.

`StrikeConfig` (`schema.prisma:2760`) is the precedent for the tunables: a singleton row `id = "default"`, a `version` counter bumped on every owner edit so instances detect staleness, and it **already carries `rejectionWindowDays Int @default(5)`**. The five day window belongs in a row of that shape, not in a constant, so the owner can change it without a deploy.

## 4.2 What evidence actually exists to judge a reason

**Field by field, what the platform can put in front of the owner today.**

| claim to judge | evidence that exists | where |
|---|---|---|
| the trainer went silent | `MarketplaceChatThread` is a **generic two user thread** (`userAId`, `userBId`, `@@unique([userAId,userBId])`, `lastMessageAt`), and `MarketplaceChatMessage` carries `senderId`, `content`, **`readAt`** and `createdAt` | `schema.prisma:2681-2711` |
| the trainer is absent entirely | `User.lastLoginAt` (throttled roughly once per UTC day) and `User.lastActiveDate` | `schema.prisma:457`, `:178` |
| no measurable progress | clip counts, the full `clip_stats` snapshot series per clip, and `Clip.earnings` from `trainerJoinedAt` forward | |
| what the owner already did | `audit_logs`, every action on the pairing | |
| what the trainer was actually paid | the credit ledger rows, each keyed to a real completed payout | |

**What does NOT exist, and must not be pretended into existence.**

• **Coaching that happened off platform leaves no trace.** Discord DMs are not readable by the platform, and CLAUDE.md's own rule treats any new bot DM as a ban risk surface. A trainer who coached entirely on Discord and a trainer who did nothing are **indistinguishable in platform data**. If the owner wants silence to be judgeable, coaching has to happen in a thread the platform can see, which is **Q22**.
• **There is no earnings history table.** BL-823 named it: *"Earnings are overwritten in place, the platform stores no earnings history."* BL-716's fix 3 asked for one three weeks earlier. So "no measurable progress" can only be computed **forward from the join date**, never reconstructed for a window before the pairing existed, and never for a period before the feature shipped.
• **There is no agreement rate precedent worth copying yet.** BL-788 deliberately refused to compute one from 10 proposals and set the standard: **no rate should be shown below 20 decided proposals.** The same restraint applies to any "trainer effectiveness" number.

## 4.3 What happens to money while a dispute is open

**On the earnings side, nothing, because there is nothing to freeze.** The cut has no representation on `Clip.earnings`, so a dispute cannot freeze, thaw, inflate or deflate anything a clipper has earned. That is the design's largest practical benefit in a dispute: **an open dispute never blocks a clipper from clipping and never touches their record.**

**On the withdrawal side there are exactly two sub cases and only one of them is settled.**

**Settled: a payout requested before the dispute opened must be honoured exactly as stamped.** Its `trainerCutAmount` was shown to the clipper before they pressed, and BL-812's finding is that a figure changing after the swipe is the defect (*"A clipper swiped expecting $30.44 and received $26.48"*). Paid is final in both directions.

**Not settled, and it is Q17: a withdrawal attempted while a dispute is open.** Three expressible options, and the third is already available in the schema shape: block the withdrawal (worst, it punishes the clipper for complaining), allow it with the cut applied (the trainer may lose the dispute afterwards and the money has gone), or allow it and mint the trainer's credit as **`PENDING` rather than `AVAILABLE`** so it is held until the verdict. `ReferralCommissionStatus` already has `PENDING` and **it currently holds 0 rows**, so "hold, do not void" is expressible today without inventing a state.

## 4.4 The cases that will actually happen

**Where existing code already answers, the answer is stated. Where it is the owner's judgement, it is deferred by number and no policy is invented.**

**1. The trainer goes silent.** The platform can **measure** it (`lastMessageAt`, unanswered message count, `readAt` gaps, `lastLoginAt`) and should surface those raw numbers on the dispute with **no verdict attached**. It cannot decide what silence is worth. **The threshold is Q11 and the definition of an answer is Q16.**

**2. The trainer is banned.** The existing referral system refuses a `BANNED` inviter **at attach time only** (`referrals.ts:51`) and does **not** revoke an existing link when the inviter is banned later. The trainer system should **stop minting new cuts the moment the trainer is banned**, because the alternative is continuing to charge a clipper for coaching from an account the platform has excluded, and that is indefensible on its face. **What happens to already accrued `AVAILABLE` credit is Q12 and is genuinely his call.**

**3. The trainer leaves or their account is soft deleted.** Copy the existing relation exactly: `referredBy` uses **`onDelete: SetNull`** (`schema.prisma:326`), so a deleted inviter's links null out and the arrangement **empties rather than widening**. BL-788 stated the principle: *"Both failure directions point the safe way."* `trainerId` must be `onDelete: SetNull` for the same reason.

**4. The clipper stops clipping entirely.** Nothing happens and nothing needs to. A cut on zero withdrawals is zero. **State plainly: no timer should void the pairing for clipper inactivity**, because the trainer's claim on work the clipper already did is exactly what the owner said must be protected, and a pairing that expires quietly would take it away without anyone deciding to.

**5. The clipper is banned.** Already answered by existing code. Every payout path runs `requireNotBanned`, so no payout is created, so no cut is stamped and no credit is minted. Nothing to decide.

**6. The trainer and the clipper are the same person, or they collude.** Self pairing must be refused **at the server, in both places**, the way the existing system refuses it twice: at attach (`referrals.ts:50`, `inviter.id === newUserId`) and again at mint (`payouts/[id]/review/route.ts:660-664`, described in code as defence in depth). Cycles must be refused with the existing **`wouldCreateCycle`** walk, 50 hops with a `visited` set, because that function already exists and its existence is proof multi hop chains are present in this data. **What cannot be detected in code is two real people agreeing to split a cut.** The measurable signals are: a trainer whose only trainee is their own referrer, a pairing created within minutes of both accounts' creation, a trainer with trainees and no message thread at all, and a trainer whose trainees share a clip account or a wallet. **What to do with a suspicious but unproven pairing is Q20.**

**7. A clipper enters a code by mistake.** This is the one case the owner has already answered, and it is what the five day window is for. Inside the window: **one press, no reason, no approval, no confirmation**, because *"obstructing the safe direction is a defect rather than a safeguard"* is stated three times across BL-788, BL-825 and BL-833. **One implementation requirement: the window must be measured from a stamped `trainerJoinedAt` on the pairing and never from `updatedAt`**, because `updatedAt` moves for unrelated reasons and would silently extend or shorten a contract.

**8. A clipper enters a second trainer's code.** Refuse at the server and **name what is in the way**, exactly as `attachReferral` refuses an already referred user (`referrals.ts:40`) and as BL-833's grant route refuses a conflicting capability while listing the keys to turn off first, on the stated grounds that *"a rule that lives in a component is not a rule."* Whether a clipper may ever hold two trainers at once is **Q7**.

---

# PART 5: WHAT EACH PERSON SEES, ALL THREE OF THEM

## 5.1 THE CLIPPER'S CONSENT SCREEN

**The standard this must meet, sourced rather than asserted.** BL-518 and BL-521 do not exist as reports (see "What could not be determined"), and their subject is fraud invisibility, not money copy. The money copy standard is written in **BL-813**, **BL-822** and **BL-762**, and it is four rules:

• **A figure must never sit beside a label that did not produce it** (BL-812, stated as a defect).
• **The label is derived from the FIELD, not the status** (BL-813's table: `You received`, `You will receive`, `You receive if approved`, `Would have received`, `Requested`).
• **Polarity lives in a word, not a sign.** `-$3.96` is announced by a screen reader as "3 dollars 96", indistinguishable from a credit, so BL-813 replaced it with **`less`**.
• **The explanation must not live behind a door the reader cannot open** (BL-762: a clipper opened a support ticket because the $20.00 minimum existed only in the gate's own string).

Plus BL-833's copy ceiling, adopted here: **Flesch Kincaid grade 6.0 or below, no sentence over 20 words**, and CLAUDE.md's rule of no dashes as bullets and no emojis.

### The wording, drafted in full

> ## Join [trainer name] as your trainer
>
> [trainer name] will coach you to get more views and earn more.
> In return, 10% of what you withdraw goes to them.
>
> **What it costs you**
> For every $100 you withdraw, $10 goes to your trainer.
> The platform fee does not change. It stays the same as today.
> You will see the exact split before you confirm any withdrawal.
> Money you have already been paid is not touched.
>
> **Leaving in the first 5 days**
> You can leave in the first 5 days for any reason.
> One press. No questions, and no cost.
>
> **Leaving after that**
> After 5 days you can still leave, but you tell us why.
> Good reasons include your trainer going quiet, or your views not growing.
> We read what you send and we decide.
> You keep clipping the whole time you wait.
>
> **Why it is not just one press**
> Your trainer works for this money. Dropping them after they helped you is not fair to them.
>
> **What your trainer will see**
> Your name, the day you joined, and how much you have earned in total.
> They will not see your wallet, your email, or your clips one by one.
>
> ☐ I understand that 10% of what I withdraw goes to my trainer.
>
> [ Join ] [ Cancel ]

**Measured against the ceiling:** longest sentence is 14 words ("Your name, the day you joined, and how much you have earned in total."). Every sentence is under 20. No dashes as bullets, no emojis, no percentage stated in more than one place, and the cost is given as a dollar figure on a round number before it is given as a percentage.

**Six things the wording does deliberately, each with its reason.**

1. **The cost is a dollar amount first.** "For every $100 you withdraw, $10 goes to your trainer" is checkable against a real withdrawal in a way "10 percent" is not.
2. **It says the platform fee does not change.** A clipper who has read anything about fees will assume a second percentage means a bigger platform bite. Saying it is unchanged is the honest reassurance and it is true.
3. **"Money you have already been paid is not touched"** is the sentence that makes this design's central safety property legible. It is also the sentence that becomes a lie if the owner answers Q4 "yes", which is why Q4 is ranked so high.
4. **It says outright that leaving after 5 days is not automatic**, and it says why in one sentence about fairness rather than in a paragraph about policy. BL-788's rule applies: *"a static claim that becomes false on a toggle is worse than no claim"*, so the claim is scoped to the window rather than stated flat.
5. **The tick box is the consent, and it names the cost, not the document.** The shipped precedent is the login click wrap: a real checkbox, `aria-label` carrying the full sentence, `aria-describedby` to the hint, `signIn()` hard returning and **focusing the checkbox** if unticked, the button on `aria-disabled` and `aria-busy` rather than native `disabled`, and `tosAcceptedAt` plus `tosVersion` persisted on the row (`login/page.tsx:141`, `:234-251`, `:322-341`). A trainer pairing should persist the same way: `trainerConsentAt` and a `trainerTermsVersion`.
6. **What the trainer will see is disclosed on the consent screen**, not discovered later. That is the difference between a contract and a surprise.

**TWO WARNINGS ABOUT THIS WORDING THAT MUST TRAVEL WITH IT.**

**First, it is written for Order A, the gross basis.** "10% of what you withdraw" is exactly true only if the cut is 10 percent of the gross withdrawal. If the owner picks Order B or C, this copy is wrong and must be rewritten to "10% of what is left after fees", with the worked figure changed from $10.00 to $9.10 or $8.70. **A figure must never sit beside a label that did not produce it.**

**Second, the referral banner is the counterexample to avoid.** Today, the only thing a referred clipper is told before signing up is one line: **"You were invited, sign up to get a reduced payout fee."** It names the benefit and never the arrangement. It does not name the inviter, does not say 5 percent of their cash will go to that inviter, and there is **no acceptance step at all**: `?ref=` goes into a cookie and `attachReferral` fires silently inside `events.createUser`. That is defensible only because the 5 percent costs the clipper nothing. **A 10 percent cut out of the clipper's own pocket cannot be attached that way, and the reason is the whole point of this section.**

## 5.2 THE TRAINER'S VIEW

**This is a new clipper visible surface showing another person's numbers, so the precedents cut both ways and both must be on the record.**

**What already exists, against the assumption that other clippers' numbers are hidden.** Two clipper facing surfaces already publish a named clipper's lifetime earnings:

• **The referrals page.** `GET /api/referrals` returns, per invitee, `{ id, username, createdAt, totalEarnings }` (`route.ts:224-228`), rendered as the invitee's username, "Joined {relative}", and verbatim **`from {formatCurrency(r.totalEarnings)} earned`** (`ReferralsRedesign.tsx:349-357`).
• **The Top earners leaderboard on `/progress`**, shown to every clipper: rank, name, view count and `formatCurrency(entry.earnings)` for the top 10 (`api/gamification/route.ts` select of `name, username, totalEarnings, totalViews`; `ProgressPremium.tsx:457-495`).

**What the restraining rounds say.** BL-833's watch page withholds *"No clipper id, name, handle or account username"* and not even the campaign **name**, because campaign names on this platform carry the rate inside the name and the name **is** owner economics. BL-788 states that seeing every pending clip **is** *"the privacy breach the brief names"* and that *"one wrongly visible clip would be a privacy breach rather than a cosmetic bug."* BL-531 strips eight owner economics fields from four clipper campaign routes with a deny list delete, and the file says in capitals that the strip **must not be reverted**.

### What a trainer MAY see about a trainee

| field | why it is defensible |
|---|---|
| `username` | the trainee typed the trainer's code and consented to being coached by a named person |
| the day they joined the trainer (`trainerJoinedAt`) | it is the start of the contract, and it is the clock on the five day window |
| **total earned, labelled as gross** | the existing referral surface already shows exactly this, and a trainer paid a percentage of it cannot verify their own credit without it. **It must carry BL-813's label**, so `Earned in total, before fees`, never a naked currency figure |
| the trainer's own credit rows on that trainee | their own money, keyed to real completed payouts |
| whether the trainee is still in the five day window | so the trainer knows the arrangement is not yet settled |
| views in total | already public on the leaderboard for the top 10, and it is the thing the trainer is coaching |

### What a trainer MUST NOT see

Enumerated, because BL-833's rule is that **an exhaustive `select` with no `include`, no spread and no rest IS the enforcement**, so a column added to `User` later cannot arrive by accident.

**The trainee's `id`** (the current referrals payload leaks it and that must not be copied), wallet address (encrypted at rest by BL-556), wallet asset or chain, email, Discord username, phone, any clip row, any clip URL (a TikTok or Instagram address contains the `@handle`), any thumbnail, **any campaign name** (BL-833: the name is the rate), any CPM or rate field, `ownerCpm`, `agencyFee`, `clientName`, `aiKnowledge`, `lockedOwnerShareDecimal`, `budget`, `fraudScore`, `fraudReasons`, `lastBotAlertScore`, the bot note, the review evidence panel, `earningsFrozenAt`, `payoutReductionRatio`, `isOwnerOverride`, any `FLAGGED` status (which `clipperStatus` masks to `PENDING`), any rejection reason, any payout row, any payout amount, `totalEarnings` unlabelled, the trainee's referrer, the trainee's other trainees, and any other trainer's trainees.

**Enforcement shape, copied from what works:** one named shaping function that is the single choke point, in the manner of `sanitizeClipForClipper` (`src/lib/clip-sanitize.ts`) and `shapeCampaignForClipper` (`src/lib/campaign-clipper-view.ts`), with the same hard rule the first of those states in its header: **never hand a raw row to a clipper.** An allow list `select`, not a deny list delete, because the deny list is the weaker of the two and only exists in `campaign-clipper-view.ts` because Prisma cannot tell a clipper request from an owner request on a shared model.

## 5.3 THE OWNER'S VIEW

**Reuse the shape that already exists.** `GET /api/referrals?admin=true`, gated by `requireOwnerOrCapability("REFERRAL_MANAGE")` (`route.ts:22`), already returns `allReferrers[]` with each referrer's `username`, `image`, `referralCode`, `referralCount`, `referralEarnings`, and a nested `referrals[]` of `{ id, username, createdAt, totalEarnings, totalViews, clipCount }`, plus `platformTotals`. A trainer hub is that payload with the trainer columns swapped in.

**What it must add, because pairings and disputes are not in that shape.** Every pairing with both names, the code used, `trainerJoinedAt` cast `::text`, whether the free window is open or closed, the dispute state and its resolution note, the credit ledger per pairing summed by status (`PENDING`, `AVAILABLE`, `PAID`, `VOIDED`), the total cut ever taken from each clipper as **both gross and cash**, the total cut ever paid to each trainer as **both gross and cash**, and every audit row on the pairing. Money is stated twice, always, because two rounds caught near overpayments from exactly that confusion: BL-763 at **$7.80** and BL-760 at **$5.44**.

---

# PART 6: THE OWNER GRANTS IT, SO SPECIFY THAT TOO

## 6.1 How he names a person, and why it cannot be a reviewer capability

**The precedent for owner only granting is exact and should be copied verbatim.** BL-833 locked campaign creation with `role !== "OWNER"` at `src/app/api/campaigns/route.ts:293-299`, message **`"Only the owner can create a campaign."`**, HTTP 403, closed at the route AND at the caller-less `"use server"` twin at `src/actions/campaigns.ts:64`, on the stated grounds that *"a `use server` export is a real network surface whether or not a component imports it."* The grant surface itself, `PATCH /api/admin/users/[id]/reviewer-config`, opens both its `GET` (`:178`) and its `PATCH` (`:201`) with `const auth = await requireOwner();`.

**But the reviewer capability system cannot carry trainer status, and this is a structural finding rather than a preference.** `hasCapability` (`src/lib/reviewer-capabilities.ts`) returns **false for any non REVIEWER** except the single BL-205 carve out for `REFERRAL_MANAGE`. A trainer is a CLIPPER. Putting a trainer key in `reviewerCapabilities` would either require widening that carve out (which BL-833 just spent a round tightening) or making every trainer a REVIEWER (which would hand them the review queue). And BL-790's finding stands as the warning: a capability written onto someone who is not a reviewer **goes stale and comes alive later**, because the demote path wipes capabilities and the promote path does not.

**So trainer status is its own additive column.** `User.isTrainer Boolean @default(false)`, applied through `scripts/run-schema-sql.js` with `ADD COLUMN IF NOT EXISTS`, re-run to prove idempotency, **never `prisma migrate`**, reversible with a single `DROP COLUMN`. That is exactly how BL-788 added `reviewerScopeInvitedOnly`, and how BL-518 added its fraud dismiss columns.

**The control:** one relabelling `<button>`, not a checkbox, on the profile card at `/admin/users/[id]`. BL-833's reason: *"A checkbox's DOM checkedness flips on activation before any handler runs, so a screen reader would announce 'checked' and then a panel would appear saying nothing had been granted."*

**A typed phrase belongs on this grant.** BL-833 states the test in its own words: `FULL AUTHORITY` needs one because it hands over the final say, and `MOVE CLIPS` and `ANY CLIPPER` need one because each **"changes what a clipper is paid."** A trainer grant changes what a clipper is paid, so it falls on the phrase side of the platform's own test. Two constraints on the phrase: it must **share no token** with `FULL AUTHORITY`, `MOVE CLIPS` or `ANY CLIPPER`, so muscle memory cannot carry someone through, and it must avoid words that are live caret commands in Dragon and Windows Voice Access, which is why `ANY CLIPPER` is not `MOVE ANY CLIP`. The exact phrase is **Q24**.

## 6.2 How the code is generated

**Reuse `generateCode()`'s alphabet and length exactly, in a separate column with its own `@unique`.**

| decision | answer | reason |
|---|---|---|
| derived from the username? | **No** | usernames are mutable, and a username in a code publishes the trainer's identity into every link and screenshot that carries it. The existing referral code is deliberately opaque |
| format | **8 characters** from `ABCDEFGHJKLMNPQRSTUVWXYZ23456789` | identical to the existing code, so it can be read aloud (no I, O, 0 or 1) and so a backfilled code is indistinguishable from a minted one, which is the property BL-799's script preserved on purpose |
| column | `User.trainerCode String? @unique` | separate from `referralCode`, so a trainer code and a referral code can never be confused for one another at the entry point |
| minted when? | **at the moment the owner grants trainer status**, inside the grant transaction | never lazily on page load, which is the mistake that gave 1,392 users a referral code they have never used |
| collisions | the existing 5 attempt loop, with the DB `@unique` as the arbiter | already proven at 1,039 writes with 0 failures and 1,356 distinct codes over 1,356 holders |

## 6.3 Revocation, and what happens to existing trainees

**Revocation exists, and it needs no confirmation.** *"Obstructing the safe direction is a defect rather than a safeguard"* is stated in BL-788, BL-825 and BL-833.

**What happens to existing trainees is the sharp part, and it is not decided here.** Three things must be separated because they are three different decisions:

1. **New cuts stop.** This one is not really a question: revoking trainer status and continuing to charge trainees would make the grant meaningless.
2. **Existing pairings.** Do they end, or do they survive with the trainer's accrued claim intact? BL-833's `CLIP_WATCH_ONLY` model is instructive: revoking a level restores what it suppressed and destroys nothing, because *"the review settings below... are kept so they are still there when you turn it off."*
3. **Accrued but unwithdrawn credit.** **The existing precedent destroys it.** `voidUnpaidLink` flips `AVAILABLE` and `PENDING` to `VOIDED`, which is why $107.02 across 5 rows is dead, and the owner has used the analogous removal 67 times. Whether the trainer system should copy that is **Q12**, and it is the single question in PART 7 most likely to produce a complaint from a real person.

## 6.4 Gating the surface to code holders only

**The requirement is a departure from the existing pattern, and the existing pattern is the reason it must be stated explicitly.** Today `/referrals` has **no gate at all** beyond a client side ADMIN redirect (`page.tsx:32-36`), `GET /api/referrals` is `requireNotBanned()` only, the sidebar link is unconditional in `clipperNavBottom` (`sidebar.tsx:132`), and BL-799 made the clipper sections unconditional for every REVIEWER too. And because `ensureReferralCode` mints on page load, **loading the page is what creates the code**. That is precisely why 1,392 users hold one and only 42 have ever invited anyone.

**The trainer surface must fail closed, in four places, and each one is load bearing.**

| layer | rule |
|---|---|
| the page | no `isTrainer` on the row, `notFound()`. Not a redirect, and not a hidden link |
| the API route | no `isTrainer`, **403**, read from the DB row and not from the session token, because BL-833 established that *"the session token may be cold"* and `requireOwnerOrCapability` loads capabilities from the DB for exactly this reason |
| the nav | link rendered only when the column is true, and never as the only gate. BL-833's finding was six checkboxes that were reachable and granted nothing, and its rule is that **a rule that lives in a component is not a rule** |
| code minting | inside the grant transaction only. **No lazy mint anywhere** |

**One more requirement that only shows up on a real screen:** nothing should be said until the session settles. BL-833 hit this exactly, because *"the role default is CLIPPER, so without that guard the owner would see the denial for a beat on every visit."*

---

# PART 7: THE OPEN QUESTIONS

**Every decision below is the owner's and none of them is answered here.** Ranked: the ones that change the whole design first, the details last. Each states the options and their consequences.

## TIER 1: these change the whole design

**Q1. Is the 10 percent taken at WITHDRAWAL or at EARNING?**
At withdrawal: the cut lives as two stamped fields on a payout row, and it is the only shape that cannot breach paid-is-final, never-decrease, or the stamp versus share property. The trainer earns nothing on work the clipper already withdrew. At earning: the cut has to reduce something on the earnings side, which puts it in the path of the cron, the budget trim, force recalc and the era boundary, and reopens the exact defect BL-716 created at $60.47 and BL-824 encoded against for seven clippers. **Every other question below assumes withdrawal. If the answer is earning, this document needs rewriting rather than extending.**

**Q2. What is the 10 percent taken OF?** Three options, on a $100 standard withdrawal:
• **10 percent of the gross withdrawal.** Trainer $10.00, clipper cash $81.00, trainer cash $9.10. Simplest to say out loud and the only version where "10% of what you withdraw" is literally true.
• **10 percent of what is left after the platform fee.** Trainer $9.10, clipper cash $81.90, trainer cash $8.28. This is what the existing 5 percent referral does, so it is the house precedent.
• **10 percent of what is left after all fees including express.** Trainer $8.70 on an express withdrawal, clipper cash $78.30. Means a clipper choosing express also reduces their trainer's cut, which the trainer did not agree to.
**The consent wording in PART 5 is written for the first option and must be rewritten for either other.**

**Q3. Does the cut apply to earnings from clips submitted BEFORE the clipper joined the trainer?**
"Yes" is one line and means the trainer is paid on work they had nothing to do with. "No" is a materially larger build: it needs per clip attribution against a stamped `trainerJoinedAt`, an eligible subtotal computed at request time, and a second figure on the withdrawal screen. There is no middle option that is cheap.

**Q4. Does the cut apply to money already earned but not yet withdrawn?**
Live size of the decision: **142 clippers hold $2,698.89 of approved, unwithdrawn earnings today; 26 of them are referred and hold $287.38.** "Yes" means the first withdrawal after joining a trainer hands them 10 percent of a balance built entirely without them, and it makes the consent line "Money you have already been paid is not touched" the only protection left. "No" requires the same per clip attribution as Q3.

**Q5. Does the cut stop the moment they leave, or continue on clips posted while they were trained?**
"Stops" is simple and means a clipper can leave on day 6 and keep everything from then on. "Continues" is the version that matches "the trainer earned it", and it requires the pairing row to survive the leaving so the stamp stays readable, plus the same per clip attribution as Q3 and Q5 combined.

**Q6. Does the trainer's cut shrink the existing referrer's 5 percent?**
The referrer's commission is 5 percent of the clipper's cash. A trainer deduction inside that cash takes the referrer from **$4.80 to $4.30 per $100**, silently. Options: let it shrink (the referrer loses money because of a decision their invitee made and nobody told them); compute the referrer's 5 percent on a pre-trainer figure (the platform's cost rises and its net on a referred trained payout goes from $0.60 to $0.10 per $100); or mint no referral commission at all on a trained clipper's payouts (the referrer loses everything on that clipper).

**Q7. May a clipper have a referrer AND a trainer, may they be the same person, and may a clipper have two trainers?**
Same person means being paid twice on one withdrawal, once out of the platform and once out of the clipper. Two trainers means 20 percent and a splitting rule. Refusing both is the default the code shape naturally produces.

## TIER 2: money mechanics

**Q8. Does the trainer pay 9 percent on their cut, or 4 percent if the trainer is themselves referred, or something else?**
The owner said 9 percent. The only precedent goes the other way: the referral cashout takes **no fee at all**, and BL-813 found that was the reason it produced the **single exactly correct payout notification out of 106**. Charging a fee here means the trainer cashout needs a fee breakdown that path has never had.

**Q9. Is there a minimum before a trainer can withdraw?** `PLATFORM_MIN_PAYOUT_USD` is **$10.00** via `resolveMinPayout`. BL-762 is the warning: a clipper below a minimum with no explanation on screen opened a support ticket about money that was never missing.

**Q10. When the owner adjusts a payout down, does the trainer's cut shrink with it?** The existing commission tracks `actualPaidAmount ?? finalAmount ?? amount`, so it does shrink. But `actualPaidAmount` is GROSS and its ratio is immutable and compounds forever with no undo.

**Q11. If a source payout is later VOIDED or REJECTED, is the trainer's credit voided?** The existing cascade voids non `PAID` rows and **accepts the loss on rows already paid to the referrer**, logged as a warning. That is a named leak in the existing design, and copying it copies the leak.

**Q12. What happens to accrued but unwithdrawn trainer credit when the owner revokes trainer status, or when a clipper wins an exit for cause?** The precedent destroys it: `voidUnpaidLink` has voided **$107.02 across 5 rows**, and the owner has used the analogous removal **67 times**. Options: void it (matches precedent, and takes money a person believes they earned); keep it (the trainer is paid for a relationship the owner has just ended); or hold it `PENDING` pending a decision, which the schema shape already supports and which currently has 0 rows.

**Q13. Can trainer status go to a REVIEWER, an ADMIN or an OWNER, or only to a CLIPPER?** The existing mint refuses an inviter whose role is not `CLIPPER` unless `canActAsClipper` is true, and BL-799 deliberately left that gate alone at **four sites** because widening it would newly pay reviewers referral money and newly email 27 people.

**Q14. Is the 10 percent fixed, or per trainer?** `ReferralCommission.rateBps` is an `Int`, so a per pairing rate is storable with no migration. A fixed rate is one sentence on the consent screen. A variable rate means the consent screen must state that trainer's number and the stamp must be read back everywhere.

## TIER 3: leaving and disputes

**Q15. Exactly how long is the free window, and measured from what?** "Roughly five days" needs a number and a clock. It should live in a singleton config row the way `StrikeConfig.rejectionWindowDays` (already 5) does, so it is changeable without a deploy, and it must be measured from a stamped `trainerJoinedAt`, never from `updatedAt`.

**Q16. Who judges an exit after the window: the owner alone, or may a capability holder judge?** The dispute precedent is OWNER only (`role !== "OWNER"` refuse). `REFERRAL_MANAGE` exists as a scoped grant and **0 users hold it**.

**Q17. What counts as "the trainer went quiet", in numbers the platform can compute?** Available signals: days since the trainer's last message in the thread, count of unanswered trainee messages, `readAt` gaps, and `lastLoginAt`. Whatever number is chosen becomes a promise on the consent screen.

**Q18. What counts as "no measurable progress", in numbers?** Available: clip count, view total, approved count and earnings from `trainerJoinedAt` forward. **It can only ever be computed forward, because there is no earnings history table.**

**Q19. What happens to a clipper's withdrawals while a dispute is open?** Block them (punishes the clipper for complaining), allow them with the cut applied (the trainer may lose and the money has gone), or allow them and hold the trainer's credit as `PENDING` until the verdict.

**Q20. How long may a dispute stay open, and what does the clipper see while they wait?** The marketplace precedent uses deadlines with tiered reminders at 12 hours, 6 hours and 1 hour, driven by a cron sweep.

**Q21. What happens the moment a trainer is banned?** Stop minting new cuts and keep accrued credit; stop and void; or nothing until the owner acts. The existing referral system does **nothing** when an inviter is banned after the fact.

**Q22. What should the platform do about a suspicious but unproven pairing?** Signals it can compute: a trainer whose only trainee is their own referrer, a pairing created minutes after both accounts, a trainer with trainees and no message thread at all, trainees sharing a clip account or wallet. Options: show the owner the signals and act only by hand; refuse the pairing at creation on the hard signals; or allow it and hold the credit.

## TIER 4: surfaces and copy

**Q23. May a trainer see a trainee's total earned figure at all?** The existing referrals page already shows an inviter exactly that, and the leaderboard shows the top 10 to everyone. BL-833 went the other way and withheld even a campaign name. If the answer is no, the trainer cannot verify their own credit.

**Q24. May a trainer message a trainee inside the platform, and is that thread the evidence of record?** If not, coaching happens on Discord where the platform cannot see it, and "the trainer went quiet" becomes unjudgeable in principle rather than merely hard.

**Q25. Is the code entry field separate from the referral code entry, or one field that accepts either?** One field is simpler for the clipper and means a mistyped referral code could enrol them with a trainer. Two fields means explaining two things.

**Q26. What is the typed phrase on the owner's grant?** It must share no token with `FULL AUTHORITY`, `MOVE CLIPS` or `ANY CLIPPER`, and must avoid words that are live caret commands in Dragon and Windows Voice Access.

**Q27. Does an existing clipper get told, unprompted, that trainers exist?** A notification or banner to 1,590 clippers about a way to give away 10 percent of their earnings is a marketing decision with a consent dimension, and `Notification.type` is free text so it costs nothing technically.

**Q28. Does the trainer see the trainee leave, and is a reason shown to them?** Showing the reason is fair to the trainer and exposes the clipper's complaint to the person they complained about.

---

# WHAT COULD NOT BE DETERMINED, NAMED RATHER THAN FUDGED

**1. BL-518, BL-521 and BL-531 have no report in the reports repository.** The tree (`git/trees/main?recursive=1`, `"truncated": false`, 1,194 paths) starts at `BL-538.md`. All three exist only as `BACKLOG.md` entries, and **two of the three are not about money copy at all**: BL-518 (`BACKLOG.md` ≈ 19000) and BL-521 (≈ 18984) are fraud invisibility rounds whose output is `src/lib/clip-sanitize.ts`. BL-531 (≈ 19064) is correctly the owner economics strip. The honest money copy standard cited in this document therefore comes from **BL-813** (the label table and the fee breakdown), **BL-822** (the "money you were already paid stays yours" contradiction) and **BL-762** (the minimum that existed only behind a support ticket), which is where the platform actually wrote it down.

**2. There is no earnings history table**, so nothing can reconstruct what a clip was worth at any past moment. BL-823 named it as unmeasurable and BL-716 asked for the row three weeks before that. The withdrawal design does not need it. **Any per clip retroactive attribution (Q3, Q4, Q5) would need it and cannot be built honestly without it.**

**3. Off platform coaching cannot be evidenced.** Discord DMs are not readable by the platform and CLAUDE.md treats any new bot DM as a ban risk surface. A trainer who coached entirely on Discord and one who did nothing are indistinguishable in platform data.

**4. Figures carried from prior reports and not reproduced here**, each named so no number in this document is unsourced: BL-823's seven owed clippers, BL-716's $60.47, BL-570's $933.94, BL-627's $142.59, BL-812's 380,000 assertion sweep, and BL-799's 1,039 backfilled codes. Each is either settled, deliberately frozen, or outside this round.

**5. `MarketplaceCreatorEarning` and `MarketplacePlatformEarning` hold 0 rows each**, so the marketplace 60/30/10 path has never written a dollar. Whether a trained clipper's marketplace earnings are in scope is undecided and is a consequence of Q1 rather than a question of its own, but it must not be assumed either way when the build round starts.

---

# REPORTED, NOT CHANGED

Found while reading. Every one is out of scope for a read only round, and CLAUDE.md's rule is to report rather than change.

**1. The live referral copy is wrong about the base, and wrong about "forever".** `ReferralsRedesign.tsx:189` reads **"Earn 5% of every referred clipper's approved earnings, forever."** and `:327-329` reads **"You earn 5% forever"** and **"You get 5% of their approved earnings, automatically."** The commission is 5 percent of the **cash the referred clipper actually received** (`actualPaidAmount ?? finalAmount ?? amount`), not of approved earnings, which are **gross and larger**. This is BL-813's gross versus cash defect, still live, on the one surface that promises a percentage. And "forever" is not true twice over: a signup through an active `OwnerReferralLink` pays **0 percent**, and the owner removing the link voids unpaid commission, which has happened **67 times** and has voided **$107.02**. The same claims also sit in the dead legacy block at `referrals/page.tsx:427`.

**2. The referral rate is stated in seven places and none is the source of truth.** `RATE_BPS = 500` at `payouts/[id]/review/route.ts:770` and `referral-backfill.ts:21`, a bare `500` at `admin/payouts/[id]/adjust/route.ts:544`, `* 0.05` hardcoded at `ReferralsRedesign.tsx:356` and `admin/referrals/page.tsx:656` and `:1059`, and `DEFAULT_REFERRAL_PERCENT = 5` at `earnings-calc.ts:50` which feeds no money write at all.

**3. `GET /api/referrals` returns the invitee's user `id`** to the referrer alongside `username` and `totalEarnings`, and `totalEarnings` is printed as a naked currency figure without BL-813's gross label.

**4. `GET /api/referrals?leaderboard=true` is gated only by `requireNotBanned()`** and returns the top 10 inviters with usernames and referral earnings. No caller was found in any `.tsx`, so the endpoint appears unreachable from the UI while remaining open to any authenticated account.

**5. The referrals surface mints a code on page load and has no role gate**, which is why 1,392 users hold a referral code and 42 have ever invited anyone.

**6. On a referred clipper's withdrawal the platform nets minus $0.80 per $100.** It collects 4 percent and pays a fee free 5 percent commission on the 96 percent. This is a live arrangement rather than a defect, and it is stated so the owner sees it before a second rate is added on top.

**7. `admin/payouts/[id]/adjust/route.ts:541-546` updates commissions in status `PENDING` only**, while the live mint creates them as `AVAILABLE`. In the normal ordering that update matches nothing. It is documented as defensive, and today there are **0 `PENDING` rows**.

**8. BL-532 is still open** and is a live clipper facing leak: `/api/campaigns` uses `include` with no select and no clipper strip, so CLIPPERs receive `clientName` and `aiKnowledge`, and `/api/campaigns/past` explicitly selects `clientName` despite a docstring claiming it avoids owner only fields.

---

# SAFETY AND PROVENANCE

**READ ONLY, and it is provable rather than asserted.** No file in `src/`, `prisma/`, `scripts/` or any config was created, edited or deleted. **The entire diff is this one markdown file.** No schema change, no `prisma generate`, no `prisma migrate`, no index created, no data mutation, no Apify actor run, no payout created, modified, approved, adjusted or cancelled, no clip's status or earnings changed, no capability granted, no user row written, no notification sent, no email sent.

**Every database read went through `scripts/run-select.js`**, which refuses every write keyword, and **every timestamp was cast `::text` against DB `now()`**. First read `2026-09-03 21:08:36.627127+00`, last read `2026-09-03 21:17:28.749264+00`.

**Baseline measured this round:** earnings invariant **0 violations** across 6,467 approved live clips, `|earnings − (baseEarnings + bonusAmount)| > 0.01`. 212 payout rows, 110 PAID. 7 referral commission rows. 1,646 users.

**The 6 money files** (`clip-earnings-writer.ts`, `earnings-calc.ts`, `balance.ts`, `tracking.ts`, `clip-earnings-invariant-middleware.ts`, `money-decimal.ts`) were **read and never opened for writing**, and none appears in the diff, which contains one markdown file.

**No build is claimed, because none was run.** A markdown only diff cannot change `tsc` or `npm run build`, and asserting a green build without running it would be the dishonesty CLAUDE.md's build rule exists to prevent.

**Method notes.** Counts by `grep -c` and by SQL `count(*)`, never piped through `head` or `tail` in a way that could truncate a count. No heredocs; files written with the file write tool. One shell at a time. Four parallel readers were used for the prior reports and the existing referral code, and their findings were **reconciled rather than averaged**: two independent derivations of the commission base agreed (`effectivePaid = actualPaidAmount ?? finalAmount ?? amount`, confirmed against all 7 live rows), and one apparent contradiction was chased to ground (5 VOIDED commissions sit on **PAID** source payouts, so they were not voided by the payout void cascade but by `voidUnpaidLink` at `admin/referral-override/route.ts:80-96`, which the 67 `REFERRAL_OVERRIDE_REMOVED` audit rows confirm).

**Handles redacted.** No wallet address was read or printed. Worktree `C:/w834`, a short path, `node_modules` never junctioned, **removed at the end**. Main was at `fdce6afd` at the first read and at the last, and both trees carried 0 tracked modifications when this round began.

---

**Nothing was built. The owner answers the questions in PART 7, and a later round builds against those answers.**
