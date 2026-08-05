# BL-719 — revert the STRAENGE budget and the $60.47 restore, keep the code fix

**SHIPPED 2026-08-05**, the same day as BL-718. Branch `checkpoint/BL-719` (`57e57347`), merged to `main` at **`78614080`**, verified on origin. Tags `pre-BL-719` / `pre-merge-BL-719` / `post-merge-BL-719`. Base main `2c74f4fb` (the BL-718 merge). Isolated worktrees `C:/b719` and `C:/m719` (short paths, `node_modules` never junctioned). `C:/b575` was found holding `main`, stale with 77 dirty entries, and was **left exactly as found**.

**DB `now()` at the pre-write check: 2026-08-05 13:34:23.988318+00. At the final verification: 2026-08-05 13:53:17.487645+00.** Every timestamp is cast `::text` against that clock.

**Redaction.** The reports repo is PUBLIC. The clipper is **Clipper A**, id prefix `cmqez5c2` — the same account as BL-690's C-3, BL-714's and BL-716's Clipper A, and BL-718's single realized victim. No handle, email or wallet address appears anywhere.

---

## ONE LINE

**The DATA is back exactly where it was before BL-718 and the CODE fix is untouched, which works only because the fix prevents the CREATION of a below-paid state without ever detecting, repairing or even observing an EXISTING one. The clipper is still owed his $60.47 and it is now recorded in a standing ledger with the procedure for paying it by hand.**

---

## What changed, and what deliberately did not

| | Kept | Reverted |
|---|---|---|
| `tracking.ts:2507` paid floor | **KEPT** | |
| `tracking.ts:2538` paid floor | **KEPT** | |
| `clip-earnings-writer.ts:354` BL-167 L1 clamp floor | **KEPT** | |
| `capButNeverBelowStored` / `capFloorDidBind` | **KEPT** | |
| STRAENGE `budget` | | **$3,100.00 back to $3,000.00** |
| 36 clips, `earnings` + `baseEarnings` | | **−$60.47 total** |
| 36 `agency_earnings` rows | | **−$30.42 total** |

**Zero source files changed this round.** The protection survives **by construction**, not by inspection: there is no `.ts` diff in which it could have been damaged.

---

# PART 0 — was a clean revert still possible?

**Yes, and it was checked before anything was touched.**

BL-718 committed its rollback **before** its write, as `scripts/migrations/BL-718-rollback.sql`, with every statement guarded on the exact AFTER value so it is a no-op if the data has drifted. Re-verified against live data:

| Check | Result |
|---|---|
| rows expected | **36** |
| clips missing | **0** |
| `earnings` still equals the post-BL-718 value | **36 of 36** |
| `baseEarnings` still equals the post-BL-718 value | **36 of 36** |
| agency rows missing | **0** |
| `agency_earnings.amount` still equals the post-BL-718 value | **36 of 36** |
| clips no longer APPROVED / deleted / retired | **0 / 0 / 0** |
| newest `updatedAt` across the 36 | **2026-08-05 13:08:55.423** — BL-718's own write |
| unwind totals implied | clipper **$60.47**, owner **$30.42** |

**Nothing had touched those rows since BL-718 wrote them**, which is exactly what the campaign's `PAST` status predicts: the cron cannot reach it. A clean revert was available, so nothing was improvised and the STOP condition never triggered.

### Correction to the brief: it was 36 clips, not 41

The brief says "all 41 clips". **The executed restore was 36 clips and 36 agency rows**, confirmed by BL-718's own `rowCount=36` twice. The number 41 was an intermediate dry-run variant BL-718 evaluated and **rejected**, because that allocation would have credited 5 zero-earning clips that carry no `agency_earnings` row, creating clips with earnings and no owner mirror. The shipped plan excluded them. Both figures appear in BL-718's working; only 36 was ever written.

---

# PART 1 and PART 2 — the write

**Executed as ONE atomic transaction, not two.** The brief frames the budget and the row unwind as separate parts, but splitting them into two commits would allow a window in which the budget is $3,000 while the rows still carry the restored values — a campaign visibly over its own ceiling. **A half-reverted money core is worse than either end state**, so both went in together, which is exactly what BL-718's pre-committed rollback file already does.

```
[stmt 1] command=BEGIN
[stmt 2] command=UPDATE rowCount=1     campaigns.budget 3100 -> 3000
[stmt 3] command=UPDATE rowCount=36    clips.earnings + clips."baseEarnings", 36 explicit ids
[stmt 4] command=UPDATE rowCount=36    agency_earnings.amount, same 36 clips
[stmt 5] command=COMMIT
```

**The exact rollback for THIS round is the already-committed `scripts/migrations/BL-718-restore.sql`**, guarded on the BEFORE values, which after this unwind match again. Re-running it re-applies the BL-718 data state precisely. **This round therefore needed no new money SQL at all**, which is the safest possible shape for a revert: the undo was written, reviewed and committed before the thing it undoes.

A per-row dry run was produced first, showing `e_now / e_target / b_now / b_target / agency_now / agency_target` and the signed delta for all 36 rows. Every current value matched BL-718's AFTER and every target matched BL-718's BEFORE.

### First attempt failed safely, and is worth recording

The first invocation exited **1** with `Cannot find module 'pg'` — the fresh worktree had no `node_modules` yet. **The script never connected, so nothing was written**, confirmed by re-reading `campaigns.budget` (still 3100) before retrying from a tree that had dependencies. A money script that dies on `require` is the harmless failure mode; it is recorded here because the exit code was checked rather than assumed.

### Nothing keyed off the old budget breaks

| Consumer | At $3,100 | At $3,000 | Verdict |
|---|---|---|---|
| `clipperPoolCap = (1 − s) × budget` | $2,066.67 | **$2,000.00**, spend $1,997.56 **inside** | fine |
| owner reserve `s × budget` | $1,033.33 | **$1,000.00**, owner $1,000.54, **$0.54 over** | **pre-existing**, see below |
| fully-spent display, `resolveClipperFacingSpent` | `Math.max(3088.99, 3100)` → 100% | `Math.max(2998.10, 3000)` → **100%** | unchanged in kind |
| clipper-facing progress bar | "$3,100 / $3,100" | **"$3,000 / $3,000"** | the honest total returns |
| L1 hard-lock `isOverBudget` | not over | **not over** ($2,998.10 of $3,000) | fine |

**The $0.54 owner overage is restored, not created.** BL-627 measured it before any of this work and named it phantom-agency rounding on flagged or retired clips inflating the unfiltered owner aggregate. Reverting faithfully puts it back; inventing a fix for it here would have been scope creep on the money core.

**On the fully-spent rule specifically:** `resolveClipperFacingSpent` returns `round2(Math.max(totalSpent, budget))`, and BL-641's arm fires **unconditionally on `status = PAST`**, independent of any spend comparison. STRAENGE is PAST, so a clipper's bar read 100% at $3,100 and reads 100% at $3,000. The two arms BL-535 and BL-641 contribute to that one `Math.max` and neither was disturbed.

---

## The question that decided whether this revert can hold

**Answered BEFORE the write, because if the answer were "yes" the revert would be pointless.**

> After the unwind, Clipper A's recorded STRAENGE earnings sit **below what he was already paid** — the exact condition BL-718's fix exists to prevent. Does the fixed code immediately re-restore it?

**NO, on four independent grounds.**

1. **`tracking.ts:3575` / `:3628`** exclude `PAST` and `COMPLETED` campaigns from the due-jobs sweep. The clips are never even selected for a tick.
2. **`campaignStatusBlocks` (`tracking.ts:1943`)** blocks the earnings path for `source === "cron" || "manual"` on `PAST`. STRAENGE is **also** `pauseSource = AUTO`, so it is blocked twice over.
3. **`gamification.ts:790`** skips every clip whose campaign has a PAID payout for that user: `if (paidCampaignIds.has(clip.campaignId)) { newTotal += clip.earnings || 0; continue; }`. Clipper A has **exactly 1 PAID payout** on STRAENGE, so his clips are skipped on the one path that has no campaign-status filter.
4. **THE STRUCTURAL GROUND, and the one that would hold even if the other three were removed.**

### What the fixed code does with an existing below-paid state versus a new one

`capButNeverBelowStored(cap, stored)` returns `max(cap, stored)`. It **takes two numbers**. It never reads `payout_requests`, has no notion of a payment, and **never raises a clip above the proposed cap**.

> **The fix PREVENTS THE CREATION of a below-paid state. It does NOT detect, repair, or even observe an EXISTING one.**

That asymmetry is the whole reason this revert is possible:

* **Creating one** — stored $1,894.14, headroom $1,831.96. The cap would write the clip DOWN below the payment. **Refused**; the clip keeps $1,894.14.
* **Encountering an existing one** — stored $1,833.67 (the reverted figure), same headroom $1,831.96, same recompute. The floor's reference point is now the *lower* stored value, so it holds the clip at **$1,833.67** and does not climb toward the $1,894.14 that was paid. **Left exactly as found.**

Repeated ticks are therefore a **fixed point**: tick 2 writes $1,833.67 again. The revert is stable, and the owner can hold this clipper below his payment on purpose while every other clipper keeps the protection.

---

# PART 3 — what the clipper and the owner will see

### Clipper A

| | Before this revert | After this revert |
|---|---|---|
| STRAENGE row, earned | $1,894.14 | **$1,833.67** |
| Panic Baby row, earned | $406.58 | $406.58 (unchanged) |
| Lifetime approved earnings | $2,300.72 | **$2,240.25** |
| Paid out | $1,894.14 | $1,894.14 (unchanged) |
| **Withdrawable balance** | **$406.58** | **$346.11** |

`max(2240.25 − 1894.14 − 0, 0) = 346.11`, and `min(406.58, 346.11) = 346.11`. **His withdrawable drops by exactly $60.47**, which is the global clamp charging the STRAENGE shortfall against his live Panic Baby earnings — precisely the "$61 vanished" complaint BL-714 traced. **It is back, on purpose, and he is owed it in cash instead.**

His STRAENGE campaign row still shows unpaid $0.00 either way, because `admin/payouts/user/[id]:170` floors at zero — the $60.47 overpayment stays invisible on that screen, which is the BL-714 Finding 2 trap. **That is why the ledger file below exists.**

### The owner's admin view

STRAENGE's budget reads **$3,000** again and its spend **$2,998.10**, so remaining-budget displays return to $1.90 rather than $11.01. The client is owed **$3,000**, not $3,100 — which is the entire point of this round. The clipper's admin row returns to total earned **$2,240.25**, total paid **$1,894.14**, unpaid **$346.11**.

### The note the owner keeps: `docs/OWED-MANUAL-PAYMENTS.md`

Committed to the repo as a standing ledger, because **BL-696 proved there is NO admin route anywhere in the codebase that creates a payout row**. Nothing in the system can observe a bank transfer or a wallet send made outside it, so a hand payment leaves no trace, the balance stays fully claimable, and the clipper can legitimately request it again and be approved.

**OUTSTANDING: `cmqez5c2`, STRAENGE, $60.47.**

**The safe procedure, from BL-696 PART 5, in order. The order is what stops the same dollars leaving twice:**

1. **Have the clipper raise the payout request in the platform FIRST.** The request row is what makes the money stop being claimable: it enters `locked` the instant it is created, inside the same transaction.
2. **Pay the requested amount PLUS the $60.47 against that same row.** Concretely today: he can request at most **$346.11**, so pay **$346.11 + $60.47 = $406.58**.
3. **Mark that row PAID through the normal review path.** `isPayoutMoneyOut` counts a PAID row as money out on every path at once, so the balance becomes correct everywhere with no further action.
4. **Strike the entry off the ledger**, with the date and the payout row it settled on.

**Do not simply send the money.** If you pay first and no row exists, the platform still shows it as available, he requests it, and every gate correctly approves a second payment. Nothing would be at fault and nothing would catch it.

---

# PART 4 — the code fix survived

**No source file changed**, so this is provable at the blob level rather than argued:

| File | Blob OID on `origin/main` | Same as BL-718? |
|---|---|---|
| `src/lib/tracking.ts` | `83ce4bab` | **yes** |
| `src/lib/clip-earnings-writer.ts` | `ac5be7de` | **yes** |
| `src/lib/earnings-never-decrease.ts` | `c15145f5` | **yes** |
| `src/lib/earnings-calc.ts` | `797e2098` | yes, unchanged since before BL-718 |
| `src/lib/balance.ts` | `e887f80a` | yes |
| `src/lib/clip-earnings-invariant-middleware.ts` | `61cef393` | yes |
| `src/lib/money-decimal.ts` | `ef5cdae7` | yes |
| `src/lib/campaign-era.ts` | `106e16ad` | yes |

Textually present on `origin/main`: `capButNeverBelowStored` appears **4 times** in `tracking.ts`, **2 times** in `clip-earnings-writer.ts`, and is exported **once** from `earnings-never-decrease.ts`; the `[BL-718-PAID-FLOOR]` log line appears at **2** sites in `tracking.ts` and **1** in the writer. All three call sites intact.

**BL-718's own harness re-run against current `main`: `npx tsx scripts/bl718-prove-paid-floor.ts` → 18 passed, 0 failed**, including the original budget-ceiling demonstration:

```
PASS  STRAENGE: OLD code trims BELOW the amount already paid  old=$1831.96 < paid=$1894.14 (takes $62.18)
PASS  STRAENGE: NEW code never goes below the amount already paid  new=$1894.14 >= paid=$1894.14
PASS  floor NEVER pushes campaign spend above max(already-committed, pool cap)  0 violations across 28,044 cases
PASS  bees.n.honey: once the pool fills, OLD code would take $35.00 off a clipper  old=$5.00 vs stored=$40.00
PASS  bees.n.honey: NEW code holds him at his stored value  new=$40.00
```

**New this round: `scripts/bl719-prove-revert-holds.ts` → 10 passed, 0 failed**, asserting the property this revert depends on:

```
PASS  the fix does NOT climb back to the paid amount  written=$1833.67 stays below paid=$1894.14
PASS  the fix holds the reverted value and does not go LOWER either  written=$1833.67 >= reverted stored=$1833.67
PASS  so the revert is stable: repeated ticks are a fixed point  tick 2 also writes $1833.67
PASS  capButNeverBelowStored takes exactly 2 arguments (no payout input exists)
PASS  the floor NEVER raises a value above the proposed cap
PASS  the helper can never invent the paid amount (output is always one of its inputs)  0 leaks across 24 combinations
PASS  CREATING a below-paid state is REFUSED  stored=$1894.14 kept, cap would have written $1831.96
PASS  an EXISTING below-paid state is left exactly as found  stored=$1833.67 in, $1833.67 out
PASS  the floor still bound in both cases (it is not silently inactive)
PASS  bees.n.honey is still protected after this revert  a full pool writes $40.00, not $5.00
```

**bees.n.honey, ACTIVE with 56 clippers, is exactly as protected as it was yesterday.** The revert took money out of one PAST campaign's rows; it took nothing out of the code.

---

# PART 5 — the state is clean

Every figure is a `SELECT` through `scripts/run-select.js` **after** the write, at DB `now()` = **2026-08-05 13:53:17.487645+00**.

| Claim | Evidence |
|---|---|
| STRAENGE budget is $3,000.00 | **3000** |
| Spend is back inside it | clipper $1,997.56 of pool cap **$2,000.00**; total **$2,998.10 of $3,000** |
| Clipper A's STRAENGE earnings match pre-BL-718 to the cent | **$1,833.67** |
| The owner-lock identity is intact | `agency x 2 == earnings` on **72 of 72** clips with an agency row |
| Earnings invariant, Clipper A | **0 violations** on all 80 clips |
| Earnings invariant, full population | **0 violations** across APPROVED / PENDING / REJECTED / FLAGGED |
| The 5 genuinely over-held clippers are still at $0.00 | **228 clippers**, 5 over-held totalling **$82.93**, **0 with a non-zero global cap** |
| BL-627's no-overpayment property holds | **0** clippers whose cap exceeds `lifetime earned − paid − locked` |
| The pre-BL-718 below-paid population is exactly restored | **8 rows**, Clipper A back at **$60.47**, the other seven unchanged to the cent |
| No clip status changed | the SQL touches `earnings`, `baseEarnings`, `amount`, `budget`, `updatedAt` only |
| No payout created, modified, approved or cancelled | **152 rows, $14,388.26**, newest `createdAt` **2026-08-05 07:35:56.442**, unchanged all day |

### Platform earnings: stated honestly rather than claimed exact

The brief asks that total platform earnings "match the pre-BL-718 figure exactly". **STRAENGE's own total does, to the cent: $2,998.10.** The platform-wide APPROVED total is **$11,175.65** against a pre-BL-718 **$11,175.47** — a difference of **$0.18**.

**That $0.18 is not revert residue.** It is ordinary 10-minute cron accrual on ACTIVE campaigns (Panic Baby, bees.n.honey, WinGram) across the roughly 65 minutes between the two measurements, and it is unavoidable on a live platform: the cron does not stop because a round is in progress. The revert moved exactly the 36 clips it names and the campaign it names, and both match their pre-BL-718 values precisely. Claiming an exact platform-wide match would have required either freezing the cron or misreporting.

---

## Safety and gates, stated honestly

* **Money files.** All 6 plus `campaign-era.ts` **BYTE-IDENTICAL by blob OID on both refs** (`git rev-parse <ref>:<f>`), listed in PART 4. **Zero source files changed this round**, so the BL-718 fix could not have been damaged. The diff is 3 files: `BACKLOG.md`, `docs/OWED-MANUAL-PAYMENTS.md` (new) and `scripts/bl719-prove-revert-holds.ts` (new, read-only).
* **Writes were the explicit id list only.** 36 clip ids and their 36 agency rows, plus one campaign row, every statement guarded on the exact expected value. **No broad UPDATE.** Snapshot taken and rollback identified before the write; a per-row dry run was produced first.
* **`agency-monitor --fix` NOT run. No platform-wide owner re-derive** (BL-539's $933.94 untouched). The owner rows moved only on the same 36 clips, back to their pre-BL-718 values.
* **No schema change, no `prisma migrate`** (only `npx prisma generate`). **No Apify actor ran**; the 11 BL-678 guards are untouched and both harnesses make no network call. No env flag flipped.
* **Accessibility:** no UI file is in the diff. No component, no JSX, no CSS, no markup, no copy string. Nothing to review.
* **Gates, honest.** `npm ci` exit 0, then `npx prisma generate` exit 0 **before** typecheck. `npx tsc --noEmit` **exit 0 with 0 lines of output**. `npm run build` **BUILD_EXIT=0** read from a captured log with `echo $?`, **never piped through `tail`**. `lint:hooks` **11 problems (0 errors, 11 warnings)** at the <=11 cap with **eslint v9.39.4 confirmed executing**, so the hooks gate was not a silent no-op. Counts by `grep -c`, never `head`. Post-merge build re-run from a clean `npm ci`: **BUILD_EXIT=0**. Both harnesses re-run on the merge commit: **18/18** and **10/10**.
* **NO dashes** as bullets. No handle, email or wallet address printed.

## Rollback

```bash
node scripts/run-mutation-once.js scripts/migrations/BL-718-restore.sql
```

Re-applies the BL-718 data state exactly: budget back to $3,100 and all 36 clip rows and 36 agency rows to their restored values. Guarded on the BEFORE values, so it is a no-op if run twice or if this revert was never applied. **No code rollback is needed, because no code changed.**

## What is still open

1. **The $60.47 is still owed** and will stay owed until it is paid by hand through the BL-696 procedure. `docs/OWED-MANUAL-PAYMENTS.md` is the only record; the platform cannot hold one.
2. **The wider gap BL-696 named remains**: no admin route creates a payout row, so every hand payment is invisible. BL-696 specified the smallest fix, one owner-only `POST /api/admin/payouts/manual` creating a `PAID` row behind the same clamp, and it is still not built. This round is the second time that absence has forced a manual ledger.
3. **The seven other clippers recorded below what they were paid ($83.75)** are unchanged and remain BL-627's by-design group. None is owed money by BL-718's analysis.
4. **Everything BL-718 left open** stands: `gamification.ts:906/912` can still redistribute between clippers who have not withdrawn, the marketplace 3-way scale at `tracking.ts:2404` shares the shape with $0.00 of exposure, and the `breakdown` base/bonus inconsistency at `tracking.ts:2534` is still pre-existing.
