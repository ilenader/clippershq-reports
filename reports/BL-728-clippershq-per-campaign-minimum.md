# BL-728 — The withdrawal minimum becomes a property of the campaign

**2026-08-07 · Base:** `main @ 6688bad0` · **Branch:** `checkpoint/BL-728`
**No clip's status or earnings changed. No payout was created, modified, approved or cancelled by this round. No Apify actor ran.**
**Handles are redacted to an md5 prefix throughout. No wallet address appears anywhere.**

---

# PART 0 — HOW THE MINIMUM ACTUALLY WORKED, WHICH IS NOT WHAT THE NAME SUGGESTS

## 0.1 Every site, file:line. There were FOUR, not one, and one of them is dead.

| # | Site | Kind | Status |
|---|---|---|---|
| 1 | `src/app/api/payouts/route.ts:271` — `if (amount < 10)` | The server gate | **LIVE. The only one that decides anything.** |
| 2 | `src/components/payouts/PayoutRequestFlow.tsx:280` — `else if (amt < 10)` | Field-level check, step 1 | **LIVE. The first thing a clipper hits.** |
| 3 | `src/app/(app)/payouts/page.tsx:232` — `if (amount < 10)` | Submit-time validator, step 2 | **LIVE**, reached through `submitPayoutRequest` |
| 4 | `src/app/(app)/payouts/page.tsx:1054` — static copy | Explanatory sentence | **DEAD** |

**Site 4 is unreachable and that nearly cost this round.** `page.tsx:351` declares `const useNewPayouts = true;` and the ternaries at `:488` and `:831` render `PayoutRequestFlow` unconditionally. The legacy modal at `page.tsx:856-1064`, which is where the obvious "Minimum payout is $10." sentence lives, has not been rendered to anyone since that flow shipped. **Editing only the sentence a grep finds first would have looked like a complete fix and changed nothing a clipper sees.** The accessibility review caught it; I verified it independently before acting on it.

There was **no shared constant**. The literal `10` was typed out four times.

## 0.2 Per campaign, globally, or both? **NEITHER. It was a global floor on the REQUESTED AMOUNT.**

This is the question that decides what the round even means, so here is the proof rather than an assertion.

The old check sat at `route.ts:271`. `campaignId` is not read until `route.ts:304`. **The gate ran thirty-three lines before the campaign it was supposedly about was known**, so it could not have consulted a campaign even if someone had wanted it to.

So the platform had two separate things that a casual reading conflates:

* **Availability** is genuinely per campaign, and then clamped globally. `route.ts:462-483` computes the campaign-scoped `available`; BL-187-P2 at `:485-589` clamps it to the account-wide figure with `effectiveCap = Math.min(available, globalAvailable)`; BL-692 fixed the clamp's earnings base to be lifetime-inclusive.
* **The minimum** was a campaign-agnostic floor on the number the clipper typed, sitting in front of all of that.

**Therefore "per campaign" here means exactly one thing: the floor on the requested amount becomes a property of the campaign the request is scoped to.** It does not, and must not, touch how much money exists. That distinction is why this round can be additive.

The consequence recorded in BL-693 follows directly: three clippers holding $4.09, $1.46 and $0.08 were refused **not** because a campaign said so, but because a global floor made any request they could truthfully make impossible. Measured today, that population is far larger than three (PART 4.1).

---

# PART 1 — THE SCHEMA AND THE DEFAULT

## 1.1 The column

`Campaign.minPayoutAmountDecimal  Decimal? @db.Decimal(18, 4)` (`prisma/schema.prisma:566`).

`Decimal(18,4)` deliberately matches `maxPayoutPerClipDecimal` on the same model (F-DECIMAL-PHASE-A-G2). **Money is never a Float here.** Applied with:

```sql
ALTER TABLE "campaigns" ADD COLUMN IF NOT EXISTS "minPayoutAmountDecimal" DECIMAL(18,4);
```

via `node scripts/run-schema-sql.js scripts/migrations/BL-728-campaign-min-payout.sql`, then `npx prisma generate`. **`prisma migrate` was never run.**

**Confirmed on production, read back from `information_schema`:**

| column_name | data_type | precision | scale | is_nullable | column_default |
|---|---|---|---|---|---|
| `minPayoutAmountDecimal` | numeric | 18 | 4 | **YES** | **null** |

No default, no backfill, no index, no constraint, nothing altered or dropped.

## 1.2 NULL means $10, and that is what makes the round safe

`resolveMinPayout(null)` returns `PLATFORM_MIN_PAYOUT_USD`, which is `10`. Every campaign in production is NULL:

```
total = 33   non_null = 0   is_null = 33   db_now = 2026-08-07 10:34:55.878201+00
```

Re-checked at the end of the round: `campaigns_with_custom_min = 0` at `db_now = 2026-08-07 11:05:32.297986+00`.

`resolveMinPayout` is **deliberately total** — it cannot throw, and any unusable stored value falls back to $10 rather than to $0 (which would let everything through) or to an exception (which BL-688 proved gets rendered to a clipper as a crash). Proven in the harness: `0`, `-5` and `"abc"` all resolve to `10`.

## 1.3 Proof that not one campaign's behaviour changes

**Exhaustive, not sampled.** The harness compares the old gate `!(amount < 10)` against the new `toCents(amount) >= toCents(resolveMinPayout(null))` at **every one of the 2,501 cent-steps from $0.00 to $25.00**:

```
A. NULL matches the old $10 gate on all 2501 cent-steps 0.00 to 25.00 → divergences = 0
```

Plus the boundary explicitly: `$9.99` refused, `$10.00` allowed, `$10.01` allowed. There is no input on which the two rules disagree.

---

# PART 2 — THE OWNER CONTROLS

## 2.1 Create and edit, both wired, both through one validator

* **Create:** `src/app/api/campaigns/route.ts` validates `data.minPayoutAmount` and writes `minPayoutAmountDecimal` only when a value was actually chosen, so a new campaign's row is shaped identically to every pre-BL-728 row.
* **Edit:** `src/app/api/campaigns/[id]/route.ts` reads `raw.minPayoutAmount`, validates it with the **same** function, and renames it to the Decimal column so a client can never write that column directly with an unvalidated value.
* **Form:** `src/app/(app)/admin/campaigns/page.tsx` — `Minimum withdrawal ($)`, prefilled `10`, sitting beside `Min views threshold`.

**Deliberately excluded from `CAMPAIGN_FIELDS`.** That array also feeds the ADMIN `pendingEdit` branch, which stores raw values as JSON for later application; an unvalidated `minPayoutAmount` in that blob would reach Prisma as a column that does not exist. It is also an owner-level money control, not something an assigned ADMIN should propose. It is read from `raw` in the OWNER branch only.

## 2.2 The bounds, and why

| Bound | Value | Reason |
|---|---|---|
| Floor | **$1** | Not merely "not zero". `SOLANA_MIN_NET_USD` is 12 (`payout-methods.ts:38`) and the fee is 9% (4% referred), so a request under a dollar cannot produce a payout any chain will carry. The clipper would clear this gate and then be refused by `validatePayoutMethod`. **A minimum that admits requests the next gate always rejects is not a minimum, it is a trap.** |
| Ceiling | **$1,000** | A typo guard, not a business rule. It stops an owner typing `10000` when he meant `100.00` and silently freezing an entire campaign. Far above any real use (the default is $10) and far below the route's existing `amount > 100_000` ceiling, so it constrains nothing legitimate. |
| Precision | 2 decimals | Sub-cent input is **refused**, not silently rounded, so the number the owner sees stored is the number he typed. This also makes the IEEE754 edge in PART 5.4 unreachable. |
| Empty | valid | Stores NULL, resolves to $10. "Clear the box" is a first-class action, so the owner never has to know what the default is to get back to it. |

All twelve bound cases are asserted in the harness (section E), including `$0.50` refused, `$1,000.01` refused, and `$10000` refused, which is the exact typo the ceiling exists for.

## 2.3 The blast radius, shown BEFORE he confirms

`GET /api/campaigns/[id]/min-payout-impact?minimum=<usd>` — owner-only, **read only**, three aggregate reads, writes nothing at all. It cannot change a status, create a payout or move a balance, so the owner may call it as often as he likes while deciding.

**It reproduces the gate rather than inventing a second rule.** It uses the same helpers the gate uses (`clipperLiability`, `isPayoutMoneyOut`, `globalPayoutClampEnabled`) and the same BL-692 lifetime base for the clamp. A blast-radius number computed by a different rule than the gate would be worse than no number.

It answers: `clippersAbleNow`, `clippersStranded`, `dollarsStranded`, `clippersFreed`, `dollarsFreed`, and `requiresConfirmation`.

**Raising and lowering are treated differently, deliberately.** `handleSubmit` intercepts **only** when `editingId` is set **and** the proposed minimum is strictly greater than the one in force when the form was opened. Lowering saves straight through, because it can only ever unblock someone, and interrupting it would train the owner to click past a warning that is usually meaningless. A campaign being **created** is never interrupted: it has no clippers and therefore no blast radius.

The owner reads, for example:

> 7 clippers holding $84.20 can withdraw from this campaign right now and would no longer be able to. Their money is not lost; it stays on their balance until they reach $25.00.

Then: **"Keep the current minimum"** or **"Raise minimum to $25.00"**. Nothing is written until he picks.

---

# PART 3 — WHAT THE CLIPPER SEES

## 3.1 One sentence, produced in one place

`src/lib/payout-minimum-shared.ts` holds the message, the default and the cents conversion, with **no `server-only` and no Prisma import**, so the browser and the server gate emit the **identical sentence**. `payout-minimum.ts` re-exports it, so server callers keep one import and there is still exactly one definition.

That structure is the direct answer to BL-688: two copies of one rule drifted, a substring stopped matching, a deliberate 400 became a 500, and three clippers holding $52.86 were told to retry something that could never succeed.

## 3.2 The refusal carries all four facts, and two branches because there are two realities

> Nova Records has a $25.00 minimum withdrawal and you have $4.09 available on it. You need $20.91 more on this campaign before you can withdraw from it.

Which campaign, what the minimum is, what they have, how much more they need.

**The shortfall is measured against the BALANCE, never against what they typed.** A clipper with $4.09 who types $1 needs **$20.91** more, not $24. Computing it from the typed amount would print a number that is simply wrong, and they would hit the same wall again after earning exactly what we told them to earn. Asserted in the harness.

The second branch, when their balance already clears the minimum and they merely typed too little, says "enter $25.00 or more" — because there, retrying genuinely works. The first branch **never says "try again"**, because it cannot succeed today and inviting a retry walks them into the 3-per-hour rate limit. Both are asserted.

Harness checks on the wording: names the campaign, states the minimum, states the balance, states the correct shortfall, **contains no "try again"**, and matches none of `fail|invalid|not allowed|denied|rejected|sorry` (BL-518 / BL-521).

## 3.3 BL-689's typed mechanism, not a string match

`AMOUNT_BELOW_CAMPAIGN_MINIMUM` is a new member of the closed `PayoutRefusalCode` union. It gets its own code rather than reusing `AMOUNT_EXCEEDS_CAMPAIGN_BALANCE` because **the two say opposite things**: that one means "you asked for more than you have", this one means "you asked for less than we can send". Collapsing them would put a clipper who has plenty of money in front of a message about not having enough.

Before this round the `< 10` refusal was a bare `NextResponse.json` and never went through the typed mechanism at all. It does now. Because the new check is decided **before** the transaction and so outside the route's catch chain, I added `payoutRefusalBody(refusal, extra)` to `payout-refusal.ts` — **the one place a refusal becomes an HTTP response**. The status and the `code` on the wire come off the refusal object itself and can never disagree with it. Nothing routes on prose.

## 3.4 Shown before effort is invested, not after

* **Always-rendered hint under the amount field:** "Minimum withdrawal on Nova Records is $25.00." It is rendered unconditionally so the `aria-describedby` idref never dangles; the text changes, not the element.
* **Announced on campaign change** through the flow's **existing** polite live region: "Nova Records. $84.20 available. Minimum withdrawal $25.00." A second region was not added — two polite regions in one dialog interleave unpredictably, which that file already documents.
* **Not put in the `<option>` label.** An option's accessible name is flat text; three numbers per row is unusable on a mobile picker wheel.
* `/api/earnings` now returns `minPayout` per campaign balance, resolved server-side, so the browser never needs to know what the default is.

## 3.5 Accessibility

Reviewed by the accessibility lead **before** any UI was written, and every required change applied:

1. **Retargeted to the live component.** (PART 0.1.)
2. **Both live checks updated**, so step 1 and step 2 cannot disagree and send a clipper through a swipe-to-confirm only to refuse them after it.
3. **`aria-describedby` composed as a token list**, not replaced — a static value would have silently destroyed the existing error association. Error first, hint second.
4. **No second `<Modal>` stacked** on the campaign form. `modal.tsx:42` listens for Escape at the document level and is not stack-aware, so two open modals both close on one press and the owner would lose an unsaved form. The confirmation replaces the form body instead.
5. **The blast-radius number is an always-mounted, initially empty `role="status" aria-live="polite" aria-atomic="true"` region**, plus `aria-describedby` on the confirm button so it is re-read when focus arrives. `aria-atomic` because the sentence carries two numbers and a partial re-read would be wrong.
6. **Focus lands on the heading, not either button.** At the moment the step opens, the number that justifies confirming has not loaded — it is an async fetch. Focusing Confirm would put the destructive control under a reflex Enter *before* the information that would change the owner's mind exists, and that reflex is realistic precisely because this interrupts a save he already pressed. Confirm stays `aria-disabled` until the fetch resolves.
7. **No native `min` on the clipper's amount input.** It is `type="text"` with `inputMode="decimal"`, where `min` does nothing, and a dynamic `min` would pre-empt the existing `aria-invalid` + focus-move path. `type="number"` with a static `min` **is** used on the owner form, where it is correct.
8. **The shared `Input`'s `error` prop is not used** for the new field: it renders an unassociated, colour-only message.

**Reported, not fixed** (pre-existing, out of scope): `modal.tsx:111`'s close button has no accessible name and its icon is not `aria-hidden`, affecting every modal in the app; `modal.tsx` has no `role="dialog"`, no `aria-labelledby` and no focus trap; `payouts/page.tsx:1069` has an emoji in a modal title, against CLAUDE.md.

---

# PART 4 — THE WITHDRAWAL PATH IS UNCHANGED

## 4.1 The population, measured before anything was touched

`db_now = 2026-08-07 10:32:48.02667+00`, reproducing the gate's own arithmetic in SQL:

| | |
|---|---|
| (clipper, campaign) pairs holding money | **140** |
| Pairs that can withdraw at $10 | **29** (24 distinct clippers) |
| Pairs blocked below $10 | **111** |
| Dollars withdrawable at $10 | **$1,989.92** |
| **Dollars stranded under the $10 floor** | **$324.33** |

BL-693 found three clippers in this state. There are **111 pairs** in it. That is the size of the problem a per-campaign minimum lets the owner address.

## 4.2 Nobody who can withdraw today became unable. Full population, before and after.

140 rows captured before the schema change, 140 after, keyed by md5-redacted user and campaign.

**Verdict comparison across all 140 pairs: 0 differ.**

```
CAN      before = 29    after = 29
BLOCKED  before = 111   after = 111
VERDICTS IDENTICAL for all 140 pairs: 0 differ
```

**Seven `effective_cap` values moved, and every single one moved UP:** `+0.04, +0.72, +0.01, +6.91, +0.73, +0.06, +13.14`. Not one moved down. These are the tracking cron crediting new views in the ~33 minutes between snapshots; six of the seven are on one campaign, which is the one actively accruing. No verdict flipped, which is the property that matters.

## 4.3 The rules this round did not touch

| Property | Status |
|---|---|
| Per-campaign availability rule (`route.ts:462-483`) | **Byte-unchanged.** Not in the diff. |
| BL-187-P2 global clamp + BL-692 lifetime base (`:485-589`) | **Byte-unchanged.** Not in the diff. |
| 9% / 4% fee and `calculatePayoutBreakdown` | **Byte-unchanged.** Not in the diff. |
| `videoUnavailable: false` exclusion | **Byte-unchanged.** Every query retains it. |
| Serializable transaction | **Byte-unchanged.** The new check is deliberately **outside** it. |

The new check is placed outside the transaction on purpose: it is a read-only threshold with no race to lose, and putting it inside would lengthen a Serializable transaction that BL-696's property depends on, to buy nothing. The worst case is one request judged against a value that was correct when it was read.

## 4.4 BL-696 — no double pay. Survives.

The live partial unique index is present and unmodified:

```
uq_payout_open_per_user_campaign
  ON public.payout_requests USING btree ("userId", "campaignId")
  WHERE (status = ANY (ARRAY['REQUESTED','UNDER_REVIEW','APPROVED']))
```

This round adds no payout write path and does not touch the transaction or the duplicate check.

## 4.5 BL-627 — nobody withdraws more than they earned. Survives, measured.

Across the full user population at `db_now = 2026-08-07 11:06:08.931317+00`:

| | |
|---|---|
| Clippers paid more than lifetime earnings | **4** |
| Largest over-hold | **$36.75** |
| **Users whose computed available is negative** | **0** |

Every over-held clipper still floors at exactly $0.00, which is BL-627's property. This round changes no term in that subtraction.

---

# PART 5 — THE EVIDENCE

## 5.1 Harness: 48 passed, 0 failed

`npx tsx scripts/bl728-verify.ts` → exit 0. Pure functions, no DB connection, no payout created.

| Claim | Evidence |
|---|---|
| **NULL behaves exactly as $10** | 0 divergences across all 2,501 cent-steps $0.00 to $25.00; `$9.99` refused, `$10.00` allowed |
| **A higher minimum refuses below it** | min $25 refuses $24.99 and refuses $10 (which the default allows); min $12.50 refuses $12.49, allows $12.50 |
| **A lower minimum allows accordingly** | min $1 allows $4.09, which the $10 default blocks; min $5 allows $5 where the default refuses |
| **BL-693's exact clippers** | $4.09, $1.46 and $0.08 all still blocked at the default; $4.09 and $1.46 released at a $1 minimum, $0.08 correctly still not |
| **Message content** | names the campaign, the minimum, the balance, and the **$20.91** shortfall computed against the balance |
| **Tone** | no "try again" on the permanent branch; matches none of `fail\|invalid\|not allowed\|denied\|rejected\|sorry` |
| **Bounds** | $0.50 refused, $0 refused, $1 accepted, $1,000 accepted, $1,000.01 refused, $10000 refused, empty and null valid |

## 5.2 The owner sees the blast radius before confirming

`handleSubmit` returns early on a detected raise and writes nothing. The confirmation step renders in place, the impact fetch fills an initially-empty live region, and Confirm is `aria-disabled` until it resolves. Only `setMinPayConfirmed(true)` allows the save to proceed, and it is reset on every `openEdit` so an approval can never carry to a different campaign.

**Not exercised against a live campaign, and I am not claiming it was.** Doing so would require raising a real minimum on production and stranding real clippers to observe it. The route's arithmetic is the same arithmetic PART 4.1 ran against the full population and matched, and the interception logic is asserted by the build; the end-to-end owner click-through is **UNVERIFIED** and is the first thing to try on a test campaign after merge.

## 5.3 Nothing was touched

| Check | Result |
|---|---|
| Earnings invariant violations | **0** (before and after) |
| Payout rows | 155, newest created `2026-08-06 01:05:03.441` — **before this round began** |
| Payouts created / modified / approved / cancelled **by this round** | **0** |
| Campaigns with a custom minimum | **0** |
| Approved clips | 3,939, unchanged |
| Apify actors run | **0**; the 11 BL-678 guards are untouched |
| DB writes by this round | **exactly one**: `ALTER TABLE ADD COLUMN IF NOT EXISTS`. Everything else went through `run-select.js`, which refuses write keywords. |

**Disclosed honestly: three payout rows DID change during the round window, and none of it was me.** One went to `PAID` at `2026-08-07 10:58:29.819` ($50 gross, $43.50 net) and two were `VOIDED` at `10:26:35.219` (before my first query at `10:32:48`). Production runs `main`; my code never left the worktree, and `run-select.js` cannot write. This is the owner working in the live admin UI concurrently with the round. It is recorded because "no payout was touched" would otherwise be checkable and look false.

## 5.4 One honest edge, recorded rather than hidden

`toCents(1.005)` returns **100, not 101**, because `1.005 * 100` is `100.49999999999999` in IEEE754. This is a property of every `Math.round(x * 100)` in this codebase, including the pre-existing ones in the payout gate.

**It cannot reach a decision here**, which is why it is recorded rather than fixed in this round: a stored minimum can never carry a third decimal (`validateCampaignMinPayout` refuses it, asserted), and a requested amount is already rounded to whole cents before the comparison. Both sides are exact 2-decimal values, where `toCents` is exact — asserted across all 5,001 values from $0.00 to $50.00, 0 bad. The harness asserts the **true** value of 100; a test asserting 101 would be asserting a bug we do not have.

## 5.5 Build

* `npm ci` → exit **0** (first). `npx prisma generate` → exit **0**, explicitly after `npm ci` and **before** `tsc`.
* `eslint` genuinely present: `npx eslint --version` → **v9.39.4**. The hooks gate is not silently no-opping.
* `npx tsc --noEmit` → exit **0**, `grep -c "error TS"` = **0**. It did **not** pass first time: 4 real errors (a wrong Prisma import path and a state variable named `saving` that is actually `submitting`), fixed, re-run clean.
* `npm run build` → **BUILD_EXIT=0**, read from `$?` written to a log, never piped through `tail`. One `Compiled successfully`; `grep -cE 'error TS|Failed to compile'` = **0**.
* **BL-348 hooks gate: `11 problems (0 errors, 11 warnings)`** against `--max-warnings 11`. It passes **exactly at the limit**. The one `useEffect` this round adds carries an `eslint-disable-next-line react-hooks/exhaustive-deps` with a stated reason (re-running on `handleSubmit`'s identity would fire the save twice); without it the gate would have gone to 12 and failed.
* The diff is real, not a document: **9 files modified, 5 added**.

## 5.6 Money files

Blob OID on `origin/main` vs the working tree. All seven identical, none in the diff:

| File | Blob OID on both refs |
|---|---|
| `src/lib/clip-earnings-writer.ts` | `ac5be7deb061768fec800aa89aae512a56a9e065` |
| `src/lib/earnings-calc.ts` | `797e20985ad57475ef321afcf3cb1ea7b0d6ab84` |
| `src/lib/balance.ts` | `e887f80acfc70fee438e719a32a60025eda22749` |
| `src/lib/tracking.ts` | `83ce4babfd39a6261114465639f2eac4e23bfceb` |
| `src/lib/clip-earnings-invariant-middleware.ts` | `61cef39395363c31f0c902dd4c64e8c06b3e6449` |
| `src/lib/money-decimal.ts` | `ef5cdae757b9ad3c23380ee8b63e279f98d0b6ac` |
| `src/lib/campaign-era.ts` | `106e16ad75125c3b10b6949a2981d33614c69ab9` |

## 5.7 Files

**Modified (9):** `prisma/schema.prisma`, `src/app/api/payouts/route.ts`, `src/app/api/earnings/route.ts`, `src/app/api/campaigns/route.ts`, `src/app/api/campaigns/[id]/route.ts`, `src/lib/payout-refusal.ts`, `src/components/payouts/PayoutRequestFlow.tsx`, `src/app/(app)/payouts/page.tsx`, `src/app/(app)/admin/campaigns/page.tsx`

**Added (5):** `src/lib/payout-minimum.ts`, `src/lib/payout-minimum-shared.ts`, `src/app/api/campaigns/[id]/min-payout-impact/route.ts`, `scripts/migrations/BL-728-campaign-min-payout.sql`, `scripts/bl728-verify.ts` (plus the two baseline `.sql` files)

---

# WHAT IS NOT DONE

1. **The owner's confirmation flow is not exercised end to end** (5.2). Try it on a test campaign first.
2. **The column is applied to production but no campaign uses it.** Nothing changes for anyone until the owner sets a value. That is the intended deploy state.
3. **`page.tsx:856-1064` is still dead code.** I did not delete it: that is a separate, larger change and deleting a legacy modal is not something to bundle into a round that touches the withdrawal gate. Its dead `$10` sentence is now the only place in the repo where that literal still appears in copy. **Worth its own round.**
4. **The three pre-existing `modal.tsx` accessibility defects** in 3.5, which affect every modal in the app.

**Rollback:** `git revert -m 1 <merge>`. The column can be left in place — it is nullable, unread by the reverted code, and every row is NULL. If you want it gone: `ALTER TABLE "campaigns" DROP COLUMN IF EXISTS "minPayoutAmountDecimal";` after the code revert.
