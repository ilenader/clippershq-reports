# BL-696 (ClippersHQ) — can the payout system pay anyone twice? The proof, re-established against the current code

## NO CLIPPER CAN BE PAID TWICE BY ANY ROUTE THE PLATFORM CONTROLS. Every scenario that could double-pay through code is blocked, and two of the blocks are hard database guarantees rather than application checks. **The one real gap is not a code gap at all: there is NO way for the owner to record a payment made by hand, because no admin path creates a payout row anywhere in the codebase.** If the owner pays someone outside the platform, the balance stays fully claimable and the clipper can request it again, legitimately, and the system will approve it. That is procedure, not code, and PART 5 says exactly what to do about it.

**2026-07-31 · AUDIT ONLY. READ ONLY on code, data and money. Nothing changed, nothing fixed, nothing built. NO payout was created, modified, approved, cancelled or paid. No balance touched, no env flag flipped, and no race or stress test was run against the live system: every concurrency question below is answered from the code and the schema.**
**Base** origin/main `46115e32` · **Branch** `checkpoint/BL-696` · **Worktree** `C:/b696` (short path, `node_modules` never junctioned)
**DB `now()` at query time: 2026-07-31 08:37:55.796343+00.** Every timestamp is cast to `::text` and read against that clock.

---

## PART 1 — every route money can leave by

**Three payout creation sites exist in `src/`, and `grep -c` over the whole tree confirms there are exactly three.** No fourth exists, and critically **there is no admin creation path at all**: `grep -c "payoutRequest.create" src/app/api/admin/` returns **0**.

| # | route | file:line | who can use it | what deducts from the balance, and when |
| --- | --- | --- | --- | --- |
| 1 | **Clipper campaign payout** | `src/app/api/payouts/route.ts:711` | the clipper, for one campaign | Nothing is "deducted" as a stored field. The balance is **derived on every read**: `available = max(earned − paidOut − locked, 0)` (`route.ts:483`). The new row enters `locked` the instant it is created with status `REQUESTED`, inside the same transaction, so the money stops being claimable immediately. |
| 2 | **Referral commission cashout** | `src/app/api/payouts/referral-request/route.ts:153` | the clipper, for referral commissions only | The commissions themselves are the ledger. Inside the same Serializable transaction the rows are re-read as `AVAILABLE` and then flipped to `PAID` with `referrerPayoutRequestId` set (`:170`). A commission consumed once cannot be consumed again. `campaignId` is `null` on these rows. |
| 3 | **`requestPayout` server action** | `src/actions/payouts.ts:50` | **NOBODY. It is dead code.** | Nothing. `grep` for importers returns **zero results**, so Next never registers it as a callable action. BL-556 guarded it anyway and it **fails closed by construction**: it has no way to supply an asset or a chain, so `validatePayoutMethod` always refuses before the `create` is reached. |

**Status transitions, the other way money state changes** (seven sites, none of which creates a row):

| file:line | what it does |
| --- | --- |
| `src/app/api/payouts/[id]/review/route.ts:230` | the owner or admin state machine: `REQUESTED → UNDER_REVIEW / APPROVED / REJECTED`, `APPROVED → PAID`, and `PAID → VOIDED` for the OWNER only |
| `src/app/api/admin/payouts/[id]/adjust/route.ts:412` | shrinks an existing payout to `actualPaidAmount` when the owner sent less than requested. **Idempotent by a UNIQUE constraint on `PayoutAdjustment.payoutRequestId`.** It cannot create a payout. |
| `src/app/api/campaigns/[id]/route.ts:925` | campaign archive bulk-voids in-flight payouts (`paidAt` stays null, money never left) |
| `src/app/api/campaigns/[id]/destroy/route.ts:92` | detaches `campaignId`, leaves the payout row and its amount intact |
| `src/app/api/calls/route.ts:277`, `src/lib/payout-reminders.ts:321` | non-money bookkeeping on existing rows |

**Manual database operations.** None can be enumerated from the code, and that is the point of PART 5. The sanctioned scripts are `run-select.js` (refuses every write keyword) and `run-schema-sql.js` (refuses DML entirely), so neither can move money. A hand-written `UPDATE` in the Supabase editor is possible and leaves no trace this audit could detect.

---

## PART 2 — the double-pay scenarios, proved from the code

### 1. Two requests racing for the same balance. **PREVENTED, twice over.**

**Application layer.** The whole handler runs inside `db.$transaction(..., { isolationLevel: "Serializable", timeout: 15000 })` (`src/app/api/payouts/route.ts:383` and `:738-747`). Inside it, before anything is created, `tx.payoutRequest.findFirst` refuses if any row exists for that `(userId, campaignId)` with status `REQUESTED`, `UNDER_REVIEW` or `APPROVED` (`:386-394`). Under Serializable, Postgres predicate locking makes the second transaction's read conflict with the first's insert, so one of the two aborts rather than both seeing an empty result.

**Database layer, and this is the stronger guarantee.** A partial unique index enforces the same rule independently of the application, and **it is live in production**, confirmed by reading `pg_indexes` this round:

```
uq_payout_open_per_user_campaign
  UNIQUE ON public.payout_requests ("userId","campaignId")
  WHERE status = ANY (ARRAY['REQUESTED','UNDER_REVIEW','APPROVED'])
```

Even if the Serializable check were removed tomorrow, a second open payout for the same user and campaign would fail with `P2002`, which the route maps to a friendly 409. **At most one open payout per clipper per campaign, guaranteed by the database.**

**The honest limit of that index.** Btree unique indexes treat `NULL`s as distinct, so it does **not** constrain referral cashouts, which carry `campaignId = null`. Those are protected by a different and equally sound mechanism: the commissions are re-read as `AVAILABLE` and flipped to `PAID` inside the same Serializable transaction (`referral-request/route.ts:130-175`), so the same commission cannot fund two payouts. Two concurrent referral cashouts over **different** commissions are legitimate and correctly allowed.

### 2. Earnings recomputed upward after a payout, letting the same dollars be claimed again. **PREVENTED, by the shape of the formula.**

`available = max(earned − paidOut − locked, 0)`. The already-paid amount stays subtracted forever, so when `earned` rises by `X` the claimable amount rises by exactly `X` and not a cent more. The clipper gets the **new** money, never the old money a second time. There is no snapshot to go stale: the balance is recomputed from scratch on every read and inside every gate.

### 3. A payout voided after it was already sent, returning money that already left. **PREVENTED, and this is the subtle one.**

`isPayoutMoneyOut` (`src/lib/balance.ts:117-124`) is three lines:

```ts
if (p.status === "PAID") return true;
if (p.status === "VOIDED" && p.paidAt != null) return true;
return false;
```

A **force-void of a PAID payout** keeps `paidAt`, so it still counts as money out and the dollars do **not** return to the claimable balance. A **campaign-archive bulk void** leaves `paidAt` null, so the money correctly returns, because it never left. The withdrawal gate uses this helper (`payouts/route.ts:475-479`) and so does the review path (`review/route.ts:164-178`). The two agree.

Belt and braces: voiding a PAID payout is OWNER-only (`review/route.ts:57`) and **requires a written reason** (`:76`), so the reconciliation trail cannot be lost silently.

### 4. A manual owner payment the platform is unaware of. **POSSIBLE. This is the live risk, and it is not a bug in the code.**

Nothing in the codebase can observe a bank transfer or a wallet send made outside the platform. **There is no admin route that creates a payout row**, so there is no way to tell the platform "this person has been paid". The balance therefore stays fully claimable, the clipper can request it, and every gate above will correctly approve it, because from the platform's point of view the money was never sent. **The system would not be paying twice; it would be paying once, having never been told about the first one.** PART 5 specifies the fix.

### 5. The clamp fix releasing money a manual payment already covered. **POSSIBLE, and the merge that shipped it said so in its own commit message.**

BL-692 released **$41.17 across 5 clippers**, and its merge commit carries an explicit **DOUBLE-PAY WARNING**: all five movers sit inside BL-661's stuck set, which has grown to 41 clippers and $544.74. If the owner has already paid any of that stuck money by hand, the $41.17 is claimable a second time. **This is scenario 4 wearing different clothes**: the clamp fix is correct, and the exposure exists only because a hand payment leaves no record. Nothing in the code can distinguish the two cases.

### 6. A clip's earnings counted under two campaigns or two eras. **PREVENTED, and measured.**

* **Two campaigns: structurally impossible.** `Clip.campaignId` is a single scalar. The per-campaign gate filters `clips.filter(c => c.campaignId === campaignId)` and the global clamp sums each clip once. Measured live: **3,649 approved non-deleted clips, 3,649 distinct ids.**
* **Two eras: not a partition the payout math uses.** `grep -c` for any era reference in `src/app/api/payouts/route.ts` returns **0**. Eras govern campaign boundaries, not payout scope, so a clip cannot be claimed once per era.
* **The marketplace 30/60 split is not a double count**, and is currently moot. The creator's 60 percent lives in `marketplace_creator_earnings` and the poster's 30 percent in `Clip.earnings`, separate rows. Measured live: the table holds **0 rows**, **0 duplicate `clipId`s**, and **0 cases** where the creator and the poster are the same person. The whole surface is inert today.

---

## PART 3 — the ledger test, on live data

For all **226** clippers in the population: `lifetime earned` versus `money out + in flight`. Money out counts `PAID` plus force-voided-after-PAID, valued at `actualPaidAmount ?? amount`, which is the same basis the gate uses.

| measure | value |
| --- | --- |
| clippers in population | **226** |
| **violations (outflow + claimable exceeds earned)** | **6** |
| worst case | **$36.75** |
| **total exposure** | **$113.38** |
| lifetime earned | $10,191.26 |
| lifetime paid | $7,785.49 |
| in flight | $435.44 |

### The over-held group: GROWN by one person, SHRUNK by $29.21 in money

| | BL-627 | BL-692 | **now** |
| --- | --- | --- | --- |
| clippers | 5 | 5 | **6** |
| total | $142.59 | not restated | **$113.38** |
| worst case | not stated | $45.82 | **$36.75** |

**The count grew and the money shrank, and both readings are real.** The exposure falls because those clippers keep earning on live clips, which erodes the excess arithmetically. One new clipper entered the group, and they are not an overpayment at all (see below).

**Every one of the six computes to exactly $0.00 available**, which is what the guarantee requires:

| clipper (redacted) | earned | paid | in flight | excess | available |
| --- | --- | --- | --- | --- | --- |
| 1 | $1,570.58 | $1,607.33 | $0.00 | $36.75 | **$0.00** |
| 2 | $1,863.75 | $1,894.14 | $0.00 | $30.39 | **$0.00** |
| 3 | $38.80 | $61.89 | $0.00 | $23.09 | **$0.00** |
| 4 | $0.00 | $14.46 | $0.00 | $14.46 | **$0.00** |
| 5 | $4.94 | $12.76 | $0.00 | $7.82 | **$0.00** |
| 6 | $29.13 | $0.00 | **$30.00** | $0.87 | **$0.00** |

**Clipper 6 is a different animal and deserves naming.** Their excess is not money already paid: it is an **in-flight request of $30.00 against $29.13 of current earnings**, an $0.87 gap that opened after the request was raised, most likely a clip rejected or retired in the interval. **It is caught before it can become an overpayment:** `review/route.ts:184` re-validates on `APPROVED` and on `PAID` and **shrinks the payout down** to what is still available rather than paying the stale figure. So the guarantee holds, but the re-validation is the thing holding it, not the original gate.

**Honest scope note on that re-validation:** it uses the **per-campaign** available with a `videoUnavailable: false` filter, not the global clamp. For clipper 6 that is sufficient. It is not the same quantity BL-692 aligned the gate to, and a future round should decide whether the two should agree.

---

## PART 4 — what the recent changes did to the guarantee

| change | effect on no-double-pay | why |
| --- | --- | --- |
| **BL-692/693 clamp fix** ($41.17 released across 5) | **UNCHANGED in code, but it created a real-world exposure** | The property survives by construction: BL-692 changed the **earned** base to the lifetime figure the balance page has always displayed, which is the exact quantity BL-627 measures overpayment against, so the two can no longer disagree. `effectiveCap = min(available, globalAvailable)` still binds. **But the $41.17 it released is claimable, and if any of it was already paid by hand it is claimable twice.** That is scenario 5, and it is a procedure exposure, not a code regression. |
| **BL-689/691 typed refusal** | **STRENGTHENED, slightly** | `PayoutRefusal` (`src/lib/payout-refusal.ts:52`) carries an own-property discriminant `isPayoutRefusal` and a code, replacing prose matching. A refusal can no longer be mistaken for a 5xx or slip past a message comparison, so a refusal that should block a payout cannot be mis-handled into an allow. The wording and the 409 are unchanged. |
| **BL-683 stale-earnings zeroing (10 rejected clips)** | **STRENGTHENED** | Those clips carried `baseEarnings` residue while `earnings` was already 0. Zeroing the residue removed a set of rows that any future query trusting `baseEarnings` could have mistaken for claimable. It cannot have released money: the gate reads `earnings`, which was already 0 on all ten. |
| **Instagram freshness and metadata work (BL-682 and neighbours)** | **UNCHANGED** | It writes only to `rule_shadow_decisions` and never touches `Clip.earnings`, a payout row or a balance. The BL-682 fix explicitly leaves `stats` unmodified so status, earnings and payout cannot move. |

**Does any of them introduce a new way for a dollar to be claimed twice? In code, no.** The only new exposure is the $41.17 the clamp fix released, and it is only exposed through the pre-existing hand-payment gap.

---

## PART 5 — what code cannot protect, and the smallest thing that would work

**The gap, stated without softening: if the owner pays a clipper by hand, the platform does not know, and cannot know.** There is no webhook, no reconciliation import, no admin "record a payment" screen, and **no admin route anywhere that creates a payout row**. The balance stays claimable. The clipper requests it. Every gate approves it, correctly, because the platform has no record of the first payment. The money leaves twice and nothing in the system is at fault.

**Does any mechanism exist today? NO.** The closest thing is `admin/payouts/[id]/adjust`, and it does not fit: it can only shrink a payout that **already exists in the system**, which by definition is not the out-of-band case. `run-select.js` cannot write and `run-schema-sql.js` refuses DML, so the only way to record a hand payment today is a manual `UPDATE` or `INSERT` in the Supabase editor, which has no validation, no audit row, and no protection against getting the amount or the person wrong.

### What the owner must do today, with no code change

**Before paying anyone by hand, and this is the whole procedure:**

1. **Have the clipper raise the request in the platform first.** Then pay against that row and mark it `PAID` through the normal review path. This costs nothing, needs no new code, and closes the gap completely, because the payout row is what makes the money stop being claimable.
2. **If a hand payment has already been made outside the system**, it is currently invisible. Recompute BL-661's stuck table **before** paying anything from it, exactly as the BL-692 merge commit warns, and reconcile the $41.17 release against any hand payments already made to those 5 clippers.
3. **Never pay from a figure read off a report.** Every number in a report, including this one, is a snapshot; the gate recomputes on every read and is the only authority.

### The smallest mechanism that would work, specified and NOT built

**One owner-only route that creates a payout row already in `PAID` state.** Nothing more:

* `POST /api/admin/payouts/manual`, OWNER only, taking `userId`, `campaignId` (nullable), `amount`, and a **mandatory** free-text `proofNote` describing the out-of-band transfer.
* It creates a `PayoutRequest` with `status: "PAID"`, `paidAt: now()`, inside the **same Serializable transaction** and behind the **same clamp** the clipper's own route uses, so a manual entry can never exceed the clipper's true available balance and can never be entered twice for the same money.
* It writes an audit row naming the owner who entered it.

That is enough because `isPayoutMoneyOut` already counts a `PAID` row as money out on every path, so a single new row makes the balance correct everywhere at once, with no change to the balance math, no change to any money file, and no new concept in the schema. **It is roughly one route file.** It is specified here and deliberately not built, because this round is read only.

---

## PART 6 — the verdict

### ONE LINE

**The payout system cannot pay anyone twice through any route it controls, and the only way a double payment can happen is if the owner pays by hand and the platform is never told, which no code can prevent and which today has no mechanism to record.**

### Ranked

| # | risk | prevented by | exposure | status | fix |
| --- | --- | --- | --- | --- | --- |
| 1 | **Hand payment outside the platform, never recorded** | **PROCEDURE ONLY** | **up to $544.74**, the BL-661 stuck set, of which **$41.17** is newly released by BL-692 | **POSSIBLE** | require the request to exist before paying; or build the one manual-payout route in PART 5 |
| 2 | The clamp fix releasing money a hand payment already covered | **PROCEDURE ONLY** | **$41.17 across 5 clippers** | **POSSIBLE**, and it is risk 1 in another form | recompute BL-661's table before paying a cent of it |
| 3 | The guarantee depends on an env flag | **CODE, while the flag is not set to off** | the whole global clamp | **UNPROVEN in production**: `GLOBAL_PAYOUT_CLAMP_ENABLED` defaults to ON when unset and is not set in any local env, but Railway cannot be read from here. BL-690 proved OFF removes the overpayment block | never set it; consider removing the off branch entirely |
| 4 | In-flight request exceeding current earnings (clipper 6, $0.87) | **CODE** | $0.87 today | **PROVEN IMPOSSIBLE to become an overpayment**: `review/route.ts:184` re-validates and shrinks on approval | consider aligning that re-validation with the global clamp |
| 5 | Two requests racing | **CODE, twice** | none | **PROVEN IMPOSSIBLE**: Serializable transaction plus the live partial unique index `uq_payout_open_per_user_campaign` | none |
| 6 | Earnings recomputed upward after a payout | **CODE** | none | **PROVEN IMPOSSIBLE**: `earned − paidOut − locked` keeps the paid amount subtracted forever | none |
| 7 | Void of an already-sent payout returning the money | **CODE** | none | **PROVEN IMPOSSIBLE**: `isPayoutMoneyOut` counts `VOIDED` with `paidAt` as money out, on both the gate and the review path | none |
| 8 | A clip counted under two campaigns or two eras | **CODE plus schema** | none | **PROVEN IMPOSSIBLE**: 3,649 approved clips, 3,649 distinct ids, `campaignId` is scalar, no era filter in the payout math | none |
| 9 | Marketplace 30/60 double count | **CODE** | none | **PROVEN IMPOSSIBLE and currently inert**: separate tables, and the creator table holds 0 rows | none |
| 10 | The dead `requestPayout` server action | **CODE** | none | **PROVEN IMPOSSIBLE**: no importers, and it fails closed on `validatePayoutMethod` | delete it one day |

### What could NOT be measured, and why

* **Whether `GLOBAL_PAYOUT_CLAMP_ENABLED` is set in production.** Railway's environment cannot be read from here. The code defaults to ON when the variable is absent, and it is absent from every local env file, but that is not proof about production.
* **Whether any hand payment has actually been made.** By definition it leaves no trace in the database, so this audit can bound the exposure but cannot say whether any of it has been realised. Only the owner knows.
* **Manual database edits.** A hand-written `UPDATE` in the Supabase editor would be indistinguishable from normal data here. No evidence of one was found, and no evidence is not the same as none happened.

---

## Safety

READ ONLY. One document. No code, data, schema, config or money change. **No payout was created, modified, approved, cancelled or paid; no balance was touched; no env flag was flipped.** No race, stress or load test was run against the live system: every concurrency answer above is reasoned from the transaction isolation level, the in-transaction duplicate check and the live partial unique index read from `pg_indexes`. Live work was limited to read-only `SELECT`s through the sanctioned `scripts/run-select.js`, with every timestamp cast to `::text` and anchored to DB `now()` = 2026-07-31 08:37:55.796343+00. **Clipper handles are redacted to `clipper-1` through `clipper-6`, and no wallet address, email or handle appears anywhere in this document**, which matters because the reports repository is public. Counting was done with `grep -c` and never through `head`. **What is prevented by CODE and what depends on the owner following a PROCEDURE are labelled separately in every table**, because conflating them is exactly how a real double payment happens. A markdown-only diff cannot change tsc or the build, so **no build was run and none is claimed**. Nothing held by BL-694 or BL-695 was touched; this round worked only in `C:/b696`. NO dashes used as bullets.
