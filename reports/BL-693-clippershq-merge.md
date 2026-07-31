# BL-693 (ClippersHQ) — merge BL-692 (balance clamp asymmetry) to main

## TWO OF THE FIVE CAN NOW WITHDRAW, AND THREE STILL CANNOT. `cmpfozzs` can request **$22.70** and `cmpl310f` **$16.04**, both immediately. The other three are still refused, but for an ordinary and correct reason and NOT the asymmetry: their released balances are **$4.09**, **$1.46** and **$0.08**, all under the platform's **$10 minimum** (`payouts/route.ts:271`), so they receive the clean "You need at least $10 to request a payout." rather than anything to do with the clamp. **$38.74 of the $41.17 is now reachable; the remaining $2.43 is reachable in principle and simply too small to request.**

**2026-07-31 · Merged to main at `46115e32`, verified on origin.** Base main `9658675a` (Merge BL-689) + `c7bfddad` (checkpoint/BL-692). Tags `pre-merge-BL-693` / `post-merge-BL-693`. **DB `now()` at verification: 2026-07-31 08:22:51.08215+00.** Every timestamp is `::text` against that clock.

**Redaction.** The reports repo is PUBLIC. Clippers are an 8-character id prefix plus BL-661's `substr(md5(userId),1,6)` short id for private reconciliation. No handle, email or wallet address appears anywhere.

---

# PART X — READ THIS BEFORE PAYING ANYTHING FROM BL-661

**BL-661's stuck set, re-measured on the merged tree: 41 clippers and $544.77.** It was **24 clippers and $390.60** when BL-661 first measured it, and $544.74 an hour before this merge. It is growing under the daily retirement cron.

**ALL FIVE CLIPPERS RELEASED BY THIS MERGE SIT INSIDE THAT SET.**

| id | bl661 | BL-661 stuck today | released by this merge | still stuck after |
|---|---|---|---|---|
| `cmpfozzs` | `540fef` | **$28.29** | **$22.70** | $5.59 |
| `cmpl310f` | `91a758` | **$16.65** | **$16.04** | $0.61 |
| `cmp75zkf` | `70aa2a` | **$10.57** | **$1.41** | $9.16 |
| `cmosmyqk` | `bc64d4` | **$0.94** | **$0.94** | $0.00 |
| `cmp71p89` | `9d81d0` | **$0.08** | **$0.08** | $0.00 |
| **TOTAL** | | **$56.53** | **$41.17** | **$15.36** |

**BL-661's table MUST be recomputed before any manual payment is made from it, or $41.17 gets paid twice.** BL-661 defines stuck as what the earnings page shows minus what the gate offers; this merge raises what the gate offers, so that figure shrinks by exactly the same amount. Paying the table as it stands today, on top of this deploy, pays these five clippers the same dollars through both routes.

**No payment was made in this round and BL-661's table was not modified. It was only re-measured.**

---

## STEP 0 — truth, with SHAs

| question | answer |
|---|---|
| Is `checkpoint/BL-692` on origin? | **YES**, `refs/heads/checkpoint/BL-692` = **`c7bfddaddc5f6723d1449a9cdd586a8772f0493a`** |
| Genuinely NOT on main? | **YES.** `git merge-base --is-ancestor c7bfddad origin/main` → **NOT MERGED**. main was `9658675a` |
| Non-empty code diff? | **YES. 305 diff lines under `.ts`**, of which **8 are non-comment code lines in `src/`** (counted with `grep -c`, never `head`). 3 files, 280 insertions / 7 deletions |
| Drift since the branch was cut? | **None.** The merge base is `9658675a`, which IS `origin/main` |
| Anything a live round holds? | **NO.** No `checkpoint/BL-693` or later branch exists on origin at all |

## The dirty main worktree

**`C:/b575` holds `main` at `91b84410` with 77 dirty entries. I did not touch it.** It is many merges behind and carries another session's staged work including `prisma/schema.prisma` and deletions across `docs/`, `public/splash/` and `scripts/migrations/`. The merge was done in a fresh clean worktree at the short path **`C:/m693`**, detached at `origin/main`, with its own `node_modules` from `npm ci` (**never junctioned**), pushed with `git push origin HEAD:main`. Re-checked after the push: `C:/b575` is exactly as found, **`main @ 91b84410`, 77 dirty entries**.

## Conflicts and the BACKLOG union

**None.** BL-692 was branched from the current main tip, so the merge applied cleanly with **0 unmerged paths**.

| check | before | after | verdict |
|---|---|---|---|
| `^## BL-` entries (`grep -c`) | **106** | **107** | +1, exactly BL-692 |
| `## BL-692` heading | 0 | 1 | added |
| Conflict markers over `*.ts`, `*.tsx`, `*.md`, `*.json`, `*.prisma` | n/a | **0** | clean |

Merge parents: exactly `9658675a` and `c7bfddad`.

---

## THE GOVERNING RULE, re-verified on the MERGED tree

**Not inherited from the branch. The measurement was re-run against the merged worktree: 9 passed, 0 failed.**

### All five over-held clippers still compute to exactly $0.00

```
clippers already over their lifetime earnings: 5
  cmova7yd  lifetime=29.13    paid=0.00     locked=30.00  capNOW=0.00 capAFTER=0.00  excess 0.87  -> 0.87
  cmoal818  lifetime=4.94     paid=12.76    locked=0.00   capNOW=0.00 capAFTER=0.00  excess 7.82  -> 7.82
  cmofpudr  lifetime=1570.58  paid=1607.33  locked=0.00   capNOW=0.00 capAFTER=0.00  excess 36.75 -> 36.75
  cmoaejuc  lifetime=38.80    paid=61.89    locked=0.00   capNOW=0.00 capAFTER=0.00  excess 23.09 -> 23.09
  cmqez5c2  lifetime=1863.75  paid=1894.14  locked=0.00   capNOW=0.00 capAFTER=0.00  excess 30.39 -> 30.39

PASS  the over-lifetime set does not grow (5 before)  after=5
PASS  NO already-over-lifetime clipper's excess increases by a cent  worsened=0
PASS  AFTER: no cap exceeds (lifetime earned - paid - locked)  violations=0
PASS  AFTER: every clipper who moves gains only money they earned
PASS  AFTER: nobody's cap DECREASES (this change can only ever raise)
```

**Every excess is unchanged to the cent.** BL-690's C-3 (`cmqez5c2`) is now $30.39 over, down from $45.82 because he keeps earning, has **zero retired clips**, and computes to **$0.00** before and after. `cmofpudr` is now the largest at $36.75 over and likewise stays at $0.00.

**No clipper's lifetime payouts plus balance exceeds their lifetime earnings anywhere in the 220-clipper population** (`no cap exceeds lifetime earned − paid − locked`, **0 violations**). BL-627's no-overpayment property survives **by construction**, because the new clamp base is the exact quantity BL-627 measures overpayment against.

**Nothing failed, so nothing was stopped. Had any of it failed I would have reported instead of pushing.**

### The shipped rule really is the rule that was measured

The measurement simulates the rule rather than importing it, so I checked the correspondence on the merged file:

```
route.ts:566-569   tx.clip.aggregate  where: { userId, isDeleted: false, status: "APPROVED" }   _sum: earnings
script:60-61       db.clip.findMany   where: { userId, isDeleted: false, status: "APPROVED" }   summed in full
route.ts:581       globalEarned = Number(globalLifetimeAgg._sum.earnings ?? 0) + globalCreatorEarned
```

Identical where-clauses. And the **per-campaign** creator aggregate at `route.ts:454` still carries `videoUnavailable: false`, confirming only the global side changed.

---

## STEP 6 — confirmed on the merged result

| check | result |
|---|---|
| **`balance.ts` byte-identical** | **`e887f80acfc70fee438e719a32a60025eda22749`**, unchanged |
| 5 genuinely-owed clippers compute a positive balance | yes, matching their live-clip earnings: $22.70, $16.04, $4.09, $1.46, $0.08 |
| 5 over-held clippers still $0.00 | yes, all five, excesses unchanged |
| earnings invariant, full population | APPROVED 3,657 · PENDING 5 · REJECTED 871 · FLAGGED 6, **0 violations in every status** |
| platform earnings unchanged or higher | APPROVED total **$10,191.26**, above BL-683's $9,845.76. Never lower |
| no clip's status changed | no write path executed; the round's only DB access is `SELECT` |
| no payout created, modified, approved or cancelled | **144 rows, $14,123.39, newest still 2026-07-30 15:21:53.814** |

**Byte-identical by blob OID on both refs:** the 6 money files plus `tracking.ts` and `campaign-era.ts` (writer `7aa6be48`, earnings-calc `797e2098`, **balance `e887f80a`**, tracking `847dcf70`, middleware `61cef393`, money-decimal `ef5cdae7`, campaign-era `106e16ad`), and additionally `payout-clamp-flag.ts` `2ca0a2a5` (the flag was **not** flipped), `api/earnings/route.ts` `a37ff0cc`, and **`apify.ts` `656bf4c0`, so the 11 BL-678 guards are intact and no Apify actor ran**.

---

## AFTER THE PUSH — is the unblock real? Traced, not created

**No payout was created. This is a trace of the gate on the merged code, per clipper, on their best campaign.**

| id | global after | campaign available | **effective cap** | outcome |
|---|---|---|---|---|
| `cmpfozzs` | $28.29 | $22.70 | **$22.70** | **SUCCEEDS**, can request up to $22.70 |
| `cmpl310f` | $16.65 | $16.04 | **$16.04** | **SUCCEEDS**, can request up to $16.04 |
| `cmp75zkf` | $13.25 | $4.09 | $4.09 | **still refused**, below the $10 minimum |
| `cmosmyqk` | $1.46 | $1.46 | $1.46 | **still refused**, below the $10 minimum |
| `cmp71p89` | $0.08 | $0.88 | $0.08 | **still refused**, below the $10 minimum |

**The three refusals are the ordinary `payouts/route.ts:271` minimum, "You need at least $10 to request a payout."** That is a clean 400 with a true, actionable message, and it is emphatically **not** BL-689's `GLOBAL_BALANCE_NEEDS_REVIEW`, which no longer fires for any of the five. Their money is no longer stuck behind a contradiction; it is simply below the threshold, exactly as it would be for any clipper with $4 of earnings, and it will become requestable as they keep clipping.

**The button was already enabled and stays enabled.** The accessibility lead re-confirmed on the merged tree that the hero reads `earnings?.available` directly (`PayoutsRedesign.tsx:181`, rendered at `:201`, button at `:212`), which is the **displayed** global. Since the display always used the lifetime base, these clippers were never blocked at the button and their displayed number does not move. Nor did they ever see BL-689's empty-state sentence, which renders only when `available <= 0`.

**One boundary the lead flagged, and it is worth stating precisely:** the amount is validated against the **per-campaign** figure (`PayoutRequestFlow.tsx:281`), not the hero total. So "they can now withdraw" means **within one campaign**, which is exactly how the table above is scoped. Nobody can request the full hero figure in a single request, and this merge does not change that.

**On the success path there is no surprise for a repeatedly-refused clipper:** `submitError` is cleared at the top of every attempt (`:320`), the `role="alert"` refusal lives only on the speed step and unmounts on advance (`:682-684`), focus moves to the "You did it" heading (`:165-169`, `:410`), and the arrival-timing line is routed through the persistent polite region (`:351`) as well as `role="status"` (`:739`).

**Accessibility verdict on the merge itself: nothing in scope.** No `.tsx`, no markup, no CSS, no ARIA. The lead also said plainly that it holds no baseline from BL-692 and would not manufacture a diff against a round it cannot recall, so point 1 above is carried on my verification for the legacy path, not re-confirmed on its own.

**Production is up** (`clipershq.com` answers 307 to the auth redirect). `/api/health` carries no commit marker, so I cannot prove from outside which SHA Railway currently has live; the deploy is inferred from the verified push, not observed.

---

## Rollback

**Do NOT use `GLOBAL_PAYOUT_CLAMP_ENABLED`.** BL-690 proved it is not a rollback: disabling the clamp removes the overpayment block entirely and would release over-held clippers against per-campaign figures they are not owed, which is strictly worse than the bug this fixes. That warning now sits in the code beside the flag.

```bash
git revert -m 1 46115e32          # the merge
# or
git reset --hard pre-merge-BL-693 # 9658675a
```

**What it restores:** the clamp's earnings base returns to the retired-excluding `clips` array, and the five clippers return to caps of $0.00, $0.00, $2.68, $0.52 and $0.00.

**Confirm it took**, without touching money:

```bash
git show HEAD:src/app/api/payouts/route.ts | grep -c "globalLifetimeAgg"   # 0 after a successful revert
npx tsx scripts/bl692-measure-clamp.ts                                      # capNOW == capAFTER for all five
```

---

## Gates, stated honestly

* **`npm ci` exit 0**, then **`npx prisma generate` exit 0**, in that order and **before** typecheck.
* **`npx tsc --noEmit` exit 0**, with **0 lines** of output.
* **`npm run build` BUILD_EXIT=0**, read from a captured log and echoed directly, never piped through `tail`. `check:prisma-bypass` **0 violations across `src/` + `scripts/`** including its earnings-write check, `check:removed-fields` OK, `lint:hooks` **11 problems (0 errors, 11 warnings)** at the ≤11 cap, compiled successfully, **61/61** static pages.
* **eslint v9.39.4 present**, so the hooks gate is real and not a silent no-op.
* **No `prisma migrate`**; the merge contains no schema change.
* Counts by `grep -c`, never `head`. **NO dashes** as bullets.

## What is still open

1. **Recompute BL-661's table before paying a cent from it.** This is not optional and it is the single most important line in this report.
2. **The $15.36 that stays stuck** for these five, and the wider $544.77, is genuinely retired-clip money and remains BL-657's separate question.
3. **The five over-held clippers, $98.92 in total**, remain unrecoverable by design. Nothing here changes that and nothing should.
