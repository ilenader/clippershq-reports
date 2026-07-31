# BL-692 (ClippersHQ) — the balance clamp asymmetry, fixed: the gate now agrees with the balance we already display

## THE FIX IS NINE LINES, AND THE REASON IT COULD BE THAT SMALL IS THE FINDING. `/api/earnings` has never filtered retired clips out of the balance it shows a clipper, so the DISPLAYED global balance already used lifetime earnings. The withdrawal gate was the only side excluding them. This does not invent a new rule, it makes enforcement match the number the platform already publishes. Five clippers gain $41.17, two of them genuinely owed $38.74 on clips that are live right now, and every one of the five clippers who is over their lifetime earnings still computes to exactly $0.00.

**2026-07-31 · SHIPPED to `checkpoint/BL-692` @ `c7bfddad`, verified on origin.** Base main `9658675a`. Tags `pre-BL-692` / `post-BL-692`. **DB `now()` at measurement: 2026-07-31 08:03:29.753586+00.** Every timestamp below is `::text` against that clock.

**Redaction.** The reports repo is PUBLIC. Clippers appear as an 8-character id prefix plus BL-661's own `substr(md5(userId),1,6)` short id so the owner can reconcile the two tables privately. No handle, email or wallet address appears anywhere.

**No payout was created, modified, approved or cancelled. No balance was written. No clip status or earnings changed. `GLOBAL_PAYOUT_CLAMP_ENABLED` was NOT flipped. No Apify actor ran.**

---

## PART 0 — the population, re-measured now, and it HAS grown

| id | bl661 | lifetime | live | retired | paid | campAvail | **cap NOW** | **cap AFTER** | delta | retired at (`::text`) |
|---|---|---|---|---|---|---|---|---|---|---|
| `cmpfozzs` | `540fef` | 65.57 | 33.44 | 32.13 (57) | 37.28 | 22.70 | **0.00** | **22.70** | **+22.70** | 2026-07-16 11:54:40.286 |
| `cmpl310f` | `91a758` | 42.19 | 16.65 | 25.54 (21) | 25.54 | 16.04 | **0.00** | **16.04** | **+16.04** | 2026-06-24 16:33:46.556 |
| `cmp75zkf` | `70aa2a` | 23.56 | 12.99 | 10.57 (32) | 10.31 | 4.09 | 2.68 | 4.09 | +1.41 | 2026-07-30 06:01:19.473 |
| `cmosmyqk` | `bc64d4` | 994.82 | 993.88 | 0.94 (1) | 993.36 | 1.46 | 0.52 | 1.46 | +0.94 | 2026-07-02 11:30:31.32 |
| `cmp71p89` | `9d81d0` | 56.77 | 48.33 | 8.44 (22) | 56.69 | 0.88 | 0.00 | 0.08 | +0.08 | 2026-07-24 06:00:02.882 |
| | | | | | | | | | **+$41.17** | |

**Against BL-690: 5 clippers and +$40.69 becomes 5 clippers and +$41.17.** The two genuinely owed have grown from **$38.26** to **$38.74** ($22.70 + $16.04). Same people, slightly more money, because both are still clipping on live campaigns.

**Growth rate.** BL-690 measured newly retired approved earnings at roughly **$3.31 a day** under the daily cron since the 2026-07-18 bulk event. The population itself is stable at five; what moves is the amount, which grew about **$0.48 in a day**. Entry requires a coincidence, being paid and then having those specific clips retired while still earning elsewhere, which is why this grows far more slowly than BL-661's phantom.

**A new clipper reported the same block, and the brief was right to demand a re-measure, but the answer is not a sixth person.** The five are the same five BL-690 found. What changed is that `cmp75zkf`'s clips were retired on **2026-07-30**, one day before this round, so their $1.41 is brand new. Anyone reporting the block now is one of these five.

### Genuinely OWED versus correctly BLOCKED

Applying BL-690's test, a clipper with zero retired clips who was paid more than they earned is the clamp working:

| id | lifetime earned | paid | over by | retired clips | cap NOW | cap AFTER | verdict |
|---|---|---|---|---|---|---|---|
| `cmofpudr` | 1,570.58 | 1,607.33 | **36.75** | 28 | 0.00 | **0.00** | correctly blocked |
| `cmqez5c2` (BL-690's C-3) | 1,863.75 | 1,894.14 | **30.39** | **0** | 0.00 | **0.00** | correctly blocked |
| `cmoaejuc` | 38.80 | 61.89 | **23.09** | 0 | 0.00 | **0.00** | correctly blocked |
| `cmoal818` | 4.94 | 12.76 | **7.82** | 5 | 0.00 | **0.00** | correctly blocked |

**BL-690's C-3 is still correctly blocked and is no longer the largest.** He was $45.82 over; he is now **$30.39** over, because he keeps earning and the gap closes. `cmofpudr` is now the largest at $36.75. The over-held group totals **$98.92** across five (the four above plus `cmova7yd`, whose $30.00 in-flight LOCKED payout slightly exceeds $29.13 of lifetime earnings, a pending-request case rather than an overpayment). BL-690 measured $127.94; it is shrinking exactly as BL-627 predicted, and none of it is recoverable by design.

---

## PART 1 — the fix, every line justified

### The full code diff. Nine lines, all inside the clamp

```diff
       if (clampOn) {
-        const globalCreatorAgg = await tx.marketplaceCreatorEarning.aggregate({
+        const globalLifetimeAgg = await tx.clip.aggregate({
+          where: { userId, isDeleted: false, status: "APPROVED" }, // deliberately NO videoUnavailable filter
+          _sum: { earnings: true },
+        });
+        const globalCreatorAgg = await tx.marketplaceCreatorEarning.aggregate({
           where: {
             creatorId: userId,
-            clip: { isDeleted: false, status: "APPROVED", videoUnavailable: false },
+            clip: { isDeleted: false, status: "APPROVED" },
           },
           _sum: { amount: true },
         });
         const globalCreatorEarned = Number(globalCreatorAgg._sum.amount ?? 0);
-        globalEarned = clips.reduce((s: number, c: any) => s + (c.earnings || 0), 0) + globalCreatorEarned;
+        globalEarned = Number(globalLifetimeAgg._sum.earnings ?? 0) + globalCreatorEarned;
```

Line by line:

* **`globalLifetimeAgg`, new.** Sums `Clip.earnings` for the user across every APPROVED, non-deleted clip **with no `videoUnavailable` filter**. This is the lifetime base. It is an aggregate rather than a reuse of the `clips` array precisely because that array must keep its filter for the per-campaign rule.
* **`clip: { ... videoUnavailable: false }` removed from the creator aggregate.** Same reasoning: a creator's 60% share was earned while the clip was live, and retiring it later must not retroactively un-earn money already paid against it. Leaving this filter would have reproduced the identical asymmetry for marketplace creators.
* **`globalEarned` now reads the aggregates instead of `clips.reduce(...)`.** This is the single line that changes the meaning. Nothing else in the clamp moves: `globalPaid`, `globalLocked`, the `Math.max(... , 0)` floor, `globalAvailable` and `effectiveCap = Math.min(available, globalAvailable)` are all byte-identical.

Everything else in the diff is comment, including a correction to a comment that had been **wrong since BL-187-P2**: it claimed the clamp was *"identical to computeBalance.available"* while sourcing the earned side from the retired-excluding array. It never was. That untrue comment is very likely why the asymmetry went unnoticed for six weeks.

### Why this base, and why it needs no clip attribution

It is **the same quantity BL-627 uses to define overpayment**. An overpaid clipper has `paid > lifetimeEarned`, so `lifetimeEarned − paid − locked` is negative and still floors to $0.00. **The no-overpayment property is preserved by construction, not by luck.**

BL-690's alternative (a), excluding already-paid amounts on retired clips by attribution, would need `payout_requests.clipIdsSnapshot`, which covers only **61 of 68 PAID rows**. Seven PAID payouts carry no snapshot and cannot be attributed at all, so that rule would behave differently for clippers depending on when their payout was created. **This rule reads no snapshot and treats every clipper identically regardless of payout vintage.**

### The two rules now agree, and the agreement is correct rather than loosened

**The per-campaign rule is byte-identical.** Its clips query and its `available` assignment do not appear in the diff (grep returns 0). It still excludes retired clips, and `effectiveCap = Math.min(available, globalAvailable)` keeps it binding.

**So retired earnings are never released.** On a campaign whose clips are all retired the per-campaign figure stays $0.00 and the minimum is still $0.00. A clipper can only ever reach **live earnings on a live campaign**. That is exactly why the blast radius is **$41.17** and not BL-661's **$544.74**, and why the three small movers gain $1.41, $0.94 and $0.08 rather than their full stuck amounts of $10.57, $0.94 and $0.08.

### The finding that made this one-sided

`/api/earnings` builds its balance from `clipWhere` at **`api/earnings/route.ts:64`**:

```ts
const clipWhere: any = { userId: session.user.id, isDeleted: false, campaign: { isTestCampaign: false } };
```

**There is no `videoUnavailable` filter.** `computeBalance` does not apply one either; it filters only on `status === "APPROVED"`. So the balance shown on `/earnings` has **always** used lifetime-including-retired. The gate was the sole outlier.

Two consequences worth stating. First, this is not a new rule: it is the gate catching up to the published figure. Second, **`balance.ts` did not need to change and is byte-identical (`e887f80a`)**, because it never applied the filter, its callers did. A money file stayed untouched on a money-meaning change.

---

## PART 2 — nobody gains a cent they did not earn, across all 220 clippers

**A note on how this is tested, because the obvious test is wrong.** "paid + locked + cap ≤ lifetime earned" fails for an already-overpaid clipper no matter what the cap is, since `paid` alone exceeds lifetime earnings. That pre-existing excess is BL-627's over-held condition, unrecoverable by design and not caused here. My first run reported two failures for exactly this reason; the test was mis-specified and I corrected it rather than the code. The properties that actually matter:

```
clippers already over their lifetime earnings BEFORE this change: 5
  cmova7yd  lifetime=29.13   paid=0.00     locked=30.00  capNOW=0.00 capAFTER=0.00  excess 0.87  -> 0.87
  cmoal818  lifetime=4.94    paid=12.76    locked=0.00   capNOW=0.00 capAFTER=0.00  excess 7.82  -> 7.82
  cmofpudr  lifetime=1570.58 paid=1607.33  locked=0.00   capNOW=0.00 capAFTER=0.00  excess 36.75 -> 36.75
  cmoaejuc  lifetime=38.80   paid=61.89    locked=0.00   capNOW=0.00 capAFTER=0.00  excess 23.09 -> 23.09
  cmqez5c2  lifetime=1863.75 paid=1894.14  locked=0.00   capNOW=0.00 capAFTER=0.00  excess 30.39 -> 30.39

PASS  the over-lifetime set does not grow (5 before)  after=5
PASS  NO already-over-lifetime clipper's excess increases by a cent  worsened=0
PASS  AFTER: no cap exceeds (lifetime earned - paid - locked)  violations=0
PASS  AFTER: every clipper who moves gains only money they earned
PASS  AFTER: nobody's cap DECREASES (this change can only ever raise)
```

**Every excess is unchanged to the cent. Every one of the five stays at exactly $0.00.**

### The overpaid clipper, explicitly

**`cmqez5c2`, BL-690's C-3: lifetime earned $1,863.75, paid $1,894.14, over by $30.39, zero retired clips.**

`max(1863.75 − 1894.14 − 0, 0) = 0`. His per-campaign figure on Panic Baby is unchanged and `min(campAvail, 0) = 0`. **He computes to $0.00 before and after. If this change had given him a cent I would have stopped and reported instead of shipping, and it does not.**

### Every clipper whose balance moves, and that it is money they earned

The five in PART 0, totalling **$41.17**. Each gain is bounded by `lifetime earned − paid − locked`, so by definition it is money they earned and have not been paid. The two material ones sit on **live, approved, still-playing clips**: `cmpfozzs` on bees.n.honey (ACTIVE) and `cmpl310f` on Panic Baby (ACTIVE). Per BL-690, those earnings are **still counted in their campaigns' spend**, so paying them releases money the budget already reserves and creates no new spend.

---

## PART 3 — THE DOUBLE-PAY TRAP. READ THIS BEFORE PAYING ANYTHING FROM BL-661

**BL-661's stuck set is now 41 clippers and $544.74**, up from BL-690's 26 and $390.60.

**ALL FIVE CLIPPERS WHO GAIN FROM THIS FIX ARE INSIDE THAT SET.**

| id | bl661 | BL-661 stuck today | BL-692 releases | still stuck after |
|---|---|---|---|---|
| `cmpfozzs` | `540fef` | **$28.29** | **$22.70** | $5.59 |
| `cmpl310f` | `91a758` | **$16.65** | **$16.04** | $0.61 |
| `cmp75zkf` | `70aa2a` | **$10.57** | **$1.41** | $9.16 |
| `cmosmyqk` | `bc64d4` | **$0.94** | **$0.94** | $0.00 |
| `cmp71p89` | `9d81d0` | **$0.08** | **$0.08** | $0.00 |
| **TOTAL** | | **$56.53** | **$41.17** | $15.36 |

**Stated plainly: if BL-661's table is paid manually as it is computed today AND this fix deploys, these five clippers receive $41.17 twice.** BL-661 defines stuck as what the earnings page shows minus what the gate offers; raising what the gate offers shrinks that figure by exactly the same amount.

**BL-661's table MUST be recomputed after this deploys, before any manual payment is made from it.** No payment was made in this round and that table was not touched.

---

## PART 4 — the rollback, and why NOT the env switch

**Do NOT roll back with `GLOBAL_PAYOUT_CLAMP_ENABLED`.** BL-690 proved it is not a rollback at all: turning the clamp off removes the overpayment block **entirely**, releasing over-held clippers up to their per-campaign figures. That is strictly worse than the bug being fixed, and it destroys BL-627's property. The warning is now written into the code beside the flag so the next reader cannot reach for it by mistake.

**The real rollback:**

```bash
git revert -m 1 <merge commit>      # after this is merged to main
# or, before merge:
git reset --hard pre-BL-692          # 9658675a
```

**What it restores:** the clamp's earnings base returns to the retired-EXCLUDING `clips` array, `globalEarned` reverts to `clips.reduce(...)`, and the creator aggregate regains its `videoUnavailable: false`. The five clippers return to their previous caps ($0.00, $0.00, $2.68, $0.52, $0.00) and BL-689's honest refusal message resumes firing for them.

**How to confirm it took**, without touching money:

```bash
git show HEAD:src/app/api/payouts/route.ts | grep -c "globalLifetimeAgg"   # 0 after a successful revert
npx tsx scripts/bl692-measure-clamp.ts                                      # capNOW == capAFTER for all five
```

The measurement script is a pure simulation and reads the database only, so it is safe to run at any time, before or after either direction.

---

## PART 5 — end to end

| claim | evidence |
|---|---|
| every owed clipper can withdraw exactly what they earned, no more | `AFTER: no cap exceeds (lifetime earned − paid − locked)`, **0 violations** across 220 clippers |
| the overpaid clipper still computes to $0.00 | `cmqez5c2` $1,863.75 earned vs $1,894.14 paid, cap **$0.00 → $0.00**; all five over-held unchanged |
| no lifetime total exceeds lifetime earnings | over-lifetime set **5 before, 5 after**; **0 worsened**; no excess grows by a cent |
| earnings invariant, full population | APPROVED 3,657 · PENDING 5 · REJECTED 871 · FLAGGED 6, **0 violations in every status** |
| platform earnings unchanged or higher | APPROVED total **$10,191.26**, above BL-683's $9,845.76. Never lower |
| no clip's status changed | no write path was executed; the round's only DB access is `SELECT` |
| no payout created, modified or cancelled | **144 rows, $14,123.39, newest still 2026-07-30 15:21:53.814** |
| the per-campaign rule is untouched | its clips query and `available` assignment return **0 hits** in the diff |

### What the affected clippers will experience

**Their displayed balance does not change at all.** It already showed the correct figure; that was the whole problem. What changes is that the gate now honours it.

The accessibility lead confirmed the mechanics: the hero button is `disabled={available <= 0}` reading the **displayed** global (`PayoutsRedesign.tsx:181, :212`), so **these clippers were never blocked at the button** and could already open the flow. It raised a fair caveat, that a clipper whose positive global came entirely from retired clips would have an empty campaign picker and be stopped client-side with "Please select a campaign" before ever reaching the server. **I checked, and it does not apply here: both material clippers have three campaigns showing a positive balance.** So they were reaching the server, receiving BL-689's honest refusal, and after this they will simply succeed.

Concretely: `cmpfozzs` can request up to **$22.70** on bees.n.honey and `cmpl310f` up to **$16.04** on Panic Baby, both on live clips they earned, and the three smaller movers gain $1.41, $0.94 and $0.08. The lead also confirmed there is no stale-error hazard on the success path: `submitError` is cleared at the top of every attempt and its `role="alert"` unmounts when the step flips to success.

**a11y verdict: nothing to review.** No component, no JSX, no CSS, no markup.

---

## Safety and gates, stated honestly

* **6 money files + `tracking.ts` + `campaign-era.ts` BYTE-IDENTICAL by blob OID** on both refs: writer `7aa6be48`, earnings-calc `797e2098`, **balance `e887f80a`**, tracking `847dcf70`, middleware `61cef393`, money-decimal `ef5cdae7`, campaign-era `106e16ad`. Also byte-identical: `payout-clamp-flag.ts` `2ca0a2a5` (the flag was NOT flipped) and `api/earnings/route.ts` `a37ff0cc`.
* **Diff:** 3 files. One source file (`src/app/api/payouts/route.ts`), one new read-only script, plus `BACKLOG.md`. The real `.ts` diff is non-empty and quoted in full above. **No schema change, no `prisma migrate`, no data write of any kind.**
* **Gates, honest.** `npm ci` exit 0, then `npx prisma generate` exit 0 **before** typecheck. `npx tsc --noEmit` **exit 0 with 0 lines of output**. `npm run build` **BUILD_EXIT=0** read from a captured log, never piped through `tail`: BYPASS detector **0 violations across `src/` + `scripts/`** including its earnings-write check, `check:removed-fields` OK, `lint:hooks` **11 problems (0 errors, 11 warnings)** at the ≤11 cap with **eslint v9.39.4 present**. Compiled 61/61 pages. Counts by `grep -c`, never `head`.
* **No Apify actor ran**; the measurement script forces `APIFY_API_KEY=DISABLED` in-process, so the 11 BL-678 guards are untouched and unreachable from here.
* **NO dashes** as bullets. No handle, email or wallet address printed. Isolated worktree at the short path `C:/b692`, `node_modules` never junctioned.

## What is still open

1. **Recompute BL-661's table before paying a cent from it.** This is the one action that must happen and it is not optional.
2. **The $15.36 that stays stuck** for these five after the fix, and the wider $544.74, is genuinely retired-clip money and remains BL-657's separate question.
3. **The five over-held clippers, $98.92**, remain unrecoverable by design. Nothing here changes that and nothing should.
