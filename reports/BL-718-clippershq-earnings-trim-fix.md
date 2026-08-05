# BL-718 — the paid floor: a shared pool cap could write a clipper DOWN below money already paid

**SHIPPED 2026-08-05.** Branch `checkpoint/BL-718` (`b3a92f19`), merged to `main` at **`2c74f4fb`**, verified on origin. Tags `pre-BL-718` / `pre-merge-BL-718` / `post-merge-BL-718`. Base main `1faf072a`, merged onto `8dfcddaa`. Isolated worktrees `C:/b718` and `C:/m718` (short paths, `node_modules` never junctioned). `C:/b575` was found holding `main`, 55 commits stale with 77 dirty entries, and was **left exactly as found**.

**DB `now()` at the pre-write measurement: 2026-08-05 12:32:01.786898+00. At the post-write verification: 2026-08-05 13:09:21.968115+00.** Every timestamp below is cast `::text` against that clock.

**Redaction.** The reports repo is PUBLIC. The clipper is **Clipper A**, id prefix `cmqez5c2`, the same account as BL-690's C-3, BL-714's Clipper A and BL-716's Clipper A. No handle, email or wallet address appears anywhere, not even partially.

---

## ONE LINE

**The BL-162 clipper-pool trim is the one budget path that assigns an ABSOLUTE value with no floor at the clip's stored value, and the value it assigns is derived from OTHER clippers' spend, so a full pool moves money sideways between clippers instead of capping growth. That hole exists at three call sites, one of them the L1 chokepoint every non-tracking write funnels through. All three now share one named invariant. Exactly ONE clipper was a realized victim, not eight and not two, and his $60.47 has been restored inside a raised budget with the owner mirror intact.**

---

# PART 0 — the mechanism, confirmed independently

### What `tracking.ts:2507` does, and why it trims

```
clipperPoolCap    = (1 - s) x realBudget                              tracking.ts:2486
otherClipperSpent = SUM(campaign approved live earnings) - this clip  tracking.ts:2489
clipperHeadroom   = max(clipperPoolCap - otherClipperSpent, 0)        tracking.ts:2500
if (newEarnings > clipperHeadroom) newEarnings = clipperHeadroom      tracking.ts:2507
```

The intent is a per-clip cap so the clipper pool cannot exceed `(1 - s) x budget` and the owner's guaranteed reserve survives. The defect is that `clipperHeadroom` **is not a property of this clip**. It is the pool cap minus every OTHER clipper's spend. When a shared pool is already full and another clipper's clips grow into it first, this clip's headroom drops **below its own stored value**, and because line 2507 is an absolute assignment rather than a delta, the clip is written DOWN.

**So: is the trim wrong, or correctly-timed against the wrong base?** It is **correct in purpose and wrong in base and direction**. Capping forward growth at a pool ceiling is right and must stay. Applying that ceiling as an absolute assignment, against a base that other people control, in a direction that can subtract, is the defect. The fix keeps the cap and removes only the subtraction.

**Every sibling branch already had the guard this one lacked**, which is what makes it an omission rather than a design:

| Site | Guard it already has |
|---|---|
| BL-162 delta scaler `tracking.ts:2236` | `if (newEarnings > oldClipperEarn)` — positive deltas only |
| legacy proportional cut `tracking.ts:2271` | `if (newEarnings > oldClipperEarn)` — positive deltas only |
| `proportional-cut.ts:110` | sums `Math.max(0, proposed - current)` — positives only |
| L1 budget hard-lock `clip-earnings-writer.ts:195` | fires only when `delta > 0`; the comment reads "**Decreases always pass**" |
| `remaining <= 0` branch `tracking.ts:2534` | `newEarnings = currentClipEarnings` — explicitly keeps current |
| **BL-162 pool trim `tracking.ts:2507`** | **none** |

### Why BL-538's never-decrease guard did not stop it

**It was never in this path. It was not bypassed.** `decideNeverDecrease` has exactly two callers in the whole tree: `force-recalc-earnings/route.ts:295` and `campaign-freeze-undo.ts:361`. The cron does not call it, and the guard's own header at `earnings-never-decrease.ts:26-36` says so, listing "RETROACTIVE bulk recomputes, the undo, force recalc" as its scope and explicitly excluding "the normal cron re-syncing a lapsed PWA bonus on a live clip".

The deeper answer to the brief's question: **the guard protects a per-clip value on the paths it covers, and this is a campaign-level total falling while no individual entitlement fell.** A clipper's recorded total dropped because somebody else's rose. No path the guard covers was involved.

### Is this BL-563's shared gross guard?

**No, and that guard cannot cover it.** `decideOwnerGross` (`owner-share-guard.ts`) decides which FORMULA computes the **owner** amount, returning `gross` / `ambiguous` / `not_guaranteed`. It protected STRAENGE's $173.41 of owner credit against base-only rewrites. It has no opinion about whether the clipper side may fall, and it is not consulted at `:2507`. Different quantity, different question.

### What triggers it

**Every tick that reaches the earnings path on a `guaranteeOwnerSplit` campaign with a valid `lockedOwnerShareDecimal`.** It BINDS only when the recompute exceeds headroom, which is whenever the pool is at or near cap. It is not a deploy, not a schedule, not a one-off budget event. `campaignStatusBlocks` (`tracking.ts:1935`) skips `PAST` and AUTO-paused campaigns for cron and manual sources, which is why STRAENGE is now inert and why **bees.n.honey, ACTIVE at 95.5% of its pool, was the live exposure**.

---

# PART 1 — the invariant, and where it is enforced

### The rule, in code

`src/lib/earnings-never-decrease.ts` (NOT one of the 6 money files) gains two exported functions:

* **`capButNeverBelowStored(proposedCap, storedEarnings)`** returns `proposedCap >= stored ? proposedCap : stored`. It is a **refusal to subtract**, never an increase.
* **`capFloorDidBind(proposedCap, storedEarnings)`** so every site can log loudly when the floor fires. A silent guard is one nobody can audit.

Non-finite handling mirrors `decideNeverDecrease`: a NaN cap keeps the stored value (coercing NaN to 0 would zero a clip, the worst outcome), a NaN stored value is not used as a floor because the row is already corrupt.

### Why the floor is the STORED value and not "the amount paid"

Deliberate, and stated in the file header. **Stored >= paid is the stronger property**: a payment can only ever be made against a recorded figure, so a value that never falls can never fall below a payment made earlier. Flooring at stored therefore **implies** the paid floor, at every clip, on every tick. It also needs no `payout_requests` query inside the Serializable money transaction — the hottest lock-holding path on the platform — and, critically, **it cannot create the opposite bug**: a paid-amount floor would RAISE recorded earnings to meet a payment that was wrong when it was made (an owner reduction, a retired clip). This floor raises nothing.

### The three call sites

| # | Site | Status | Realized exposure |
|---|---|---|---|
| 1 | `tracking.ts:2507` BL-162 clipper-pool trim | **FIXED** | the STRAENGE defect, $60.47 |
| 2 | `tracking.ts:2538` legacy ratio-cap (non-guarantee) | **FIXED, preventive** | $0.00 — every flag-off CPM_SPLIT campaign is PAST with $0.00 of clipper earnings (measured) |
| 3 | `clip-earnings-writer.ts:354` BL-167 L1 clamp | **FIXED** | latent, and it is the chokepoint |

Site 3 is why a money file changed. The BL-167 clamp runs only on an increase (`delta > 0`), but it clamps **to `clipperHeadroom`**, so a write asking for MORE could still land BELOW the clip's stored value once other clippers filled the pool. It is reached by review/approve, override, owner-submit, force-recalc, fix-earnings, fix-budget and payout-adjust — every non-tracking path.

### THE SAFETY PROPERTY THAT MAKES THIS SAFE

**`otherClipperSpent` already excludes this clip.** Flooring at the stored value therefore leaves campaign clipper spend at exactly `otherClipperSpent + stored`, which is the value it **already has committed**.

> **The floor never adds a cent to a campaign. It only refuses to remove one.**

Proven in the harness over **28,044 cases** (pool cap 0 to 3000, other-spend 0 to 3000, six stored values): campaign spend after the floor never exceeds `max(already-committed, pool cap)`. **0 violations.**

Two corollaries the brief demanded:

1. **BL-627's no-overpayment property survives by construction.** The floor never raises a clip, so it cannot add to any clipper's earned side, so it cannot raise anyone's withdrawable balance. Measured after the change across all **228** clippers: **5 over-held clippers, $82.93, and 0 of them has a non-zero global cap.** All five still compute exactly $0.00.
2. **BL-690's genuinely over-held clippers are untouched.** `cmofpudr` $36.75, `cmoaejuc` $23.09, `cmq0qn2l` $14.46, `cmoal818` $7.82, `cmova7yd` $0.81 — every one still $0.00 available.

---

# PART 2 — every path that can reduce a recorded earnings value

Enumerated by grep, not by memory. **No production code writes `Clip.earnings` / `baseEarnings` / `bonusAmount` outside `writeClipEarnings`** (`grep` for `clip.update` on those fields returns only comments).

| Path | Can it push a recorded total below what was PAID? | Action |
|---|---|---|
| `tracking.ts:2507` BL-162 pool trim | **YES — the defect** | **FIXED** |
| `tracking.ts:2538` legacy ratio-cap | **YES**, same shape, $0.00 realized | **FIXED** |
| `clip-earnings-writer.ts:354` BL-167 L1 clamp | **YES**, latent, at the chokepoint | **FIXED** |
| `tracking.ts:2404` marketplace 3-way scale | Same shape | **NOT FIXED** — see below |
| `gamification.ts:906` (`remaining<=0` writes **0**) and `:912` (ratio-cap) | **NO** | see below |
| `force-recalc-earnings:295` | No — `decideNeverDecrease` ON by default | none |
| `campaign-freeze-undo.ts:361` | No — `decideNeverDecrease` | none |
| `payouts/[id]/adjust` (`payoutReductionRatio`) | Yes, **by design** — a deliberate, IMMUTABLE owner cut | none, correct |
| `clips/[id]/review` reject/zero, ban cascade | Yes, **by design** | none |
| `cpm-restamp.ts`, `owner-submit-core.ts`, `fix-budget`, `fix-earnings` | Owner/admin-triggered, all funnel through the now-floored L1 clamp | none |
| `videoUnavailable` retirement (`retire-dead-clips`) | Excludes clips from per-campaign sums, does not reduce a stored value. BL-692 already removed it from the global clamp base | none |
| era boundary / `campaignStatusBlocks` | Excludes clips from RECOMPUTE; changes no stored value | none |
| `agency-monitor --fix` | Owner rows only. **NOT RUN** | none |

### The two named, and why they were left

**`gamification.ts:906/912` is the same shape and is worse in three ways** — the `remaining <= 0` branch writes **0** rather than "keep current", it has **no campaign-status filter** (BL-563's finding, so it reaches PAST and AUTO-paused campaigns), and it is reachable by a **CLIPPER opening their own progress page** via `/api/gamification` and `/api/user/pwa-status`. **But it cannot breach the paid floor**, because `gamification.ts:790` skips every clip whose campaign has a PAID payout for that user:

```ts
if (paidCampaignIds.has(clip.campaignId)) { newTotal += clip.earnings || 0; continue; }
```

That is the paid-floor invariant already implemented, at campaign granularity, on that path. It can still redistribute between clippers who have **not** withdrawn — the same sideways-movement shape, outside this round's invariant. **Recorded, own round.**

**`tracking.ts:2404` marketplace 3-way scale** is the same shape. Measured: **0 marketplace clips, $0.00 of creator earnings, $0.00 of platform earnings platform-wide**, so it has no reachable victim; and flooring one of three shares without the others would break the 60/30/10 sum the split depends on. **Left alone deliberately.**

### Found, not fixed, and not silently

`tracking.ts:2534` and `gamification.ts:906` force `newEarnings` to a value while leaving `breakdown.baseEarnings` / `bonusAmount` at the recomputed figures, which can trip `assertInvariant` at write time. **Pre-existing.** The BL-718 floor makes it strictly LESS likely to fire (the forced value moves closer to the recompute), never more. Own round.

---

# PART 3 — the damage, measured, and repaired

### Eight clippers are recorded below what they were paid. Only ONE is this defect.

The raw query reproduces BL-716 exactly: **8 clippers, $144.22**. But "recorded below paid" is a symptom with several causes. Recomputing each clipper's **genuine entitlement independently** — from the latest `clip_stats` views, the clip's stamped `cpmAtSubmissionDecimal`, `minViewsAtApproval` and `maxPayoutPerClipAtApproval`, plus the clip's own `bonusPercent` — separates them:

| Clipper | Campaign | Recorded | Paid | Short | Entitlement | PRR clips | Retired | Verdict |
|---|---|---|---|---|---|---|---|---|
| **`cmqez5c2`** | **STRAENGE** | 1,833.67 | 1,894.14 | **60.47** | **2,450.61** | **0** | **0** | **THE TRIM** |
| `cmofpudr` | somesome | 1,570.58 | 1,607.33 | 36.75 | 2,175.63 | **29 of 30** | 28 | owner PRR cut + retirement |
| `cmoaejuc` | somesome | 38.80 | 61.89 | 23.09 | 80.24 | **5 of 5** | 0 | owner PRR cut |
| `cmq0qn2l` | GainzAlgo | 0.00 | 14.46 | 14.46 | n/a | n/a | n/a | zero approved clips remain |
| `cmoal818` | somesome | 4.94 | 12.76 | 7.82 | 10.52 | **9 of 9** | 5 | owner PRR cut |
| `cmova7yd` | BAD BITCH (2.50) | 29.19 | 30.00 | 0.81 | **29.23** | 0 | 0 | paid ABOVE entitlement |
| `cmp71p89` | somesome | 33.99 | 34.79 | 0.80 | 45.98 | 8 of 40 | 18 | PRR + retirement |
| `cmqmnvgs` | WinGram | 11.21 | 11.23 | 0.02 | **11.22** | 0 | 0 | paid ABOVE entitlement, 2c |

**Only `cmqez5c2` has the signature of the pool trim**: zero `payoutReductionRatio`, zero retired, zero frozen, and an entitlement of **$2,450.61** — far above both the $1,894.14 he was paid and the $1,833.67 he was left with. (That figure independently reproduces BL-716's $2,450.55 to six cents, computed from raw view rows rather than taken from it.) **The other seven are BL-627's by-design over-held group and were deliberately NOT released** — releasing them is precisely the opposite bug the brief forbids.

### The brief's bees.n.honey premise is a misreading, and it matters

The brief states "the same trim has taken $63.91 on bees.n.honey, which is ACTIVE". **It has taken $0.00.** In BL-716's table $63.91 is that campaign's remaining **HEADROOM**, not an amount removed. Measured now:

| Campaign | Status | Clipper spend | Pool cap | Used | Headroom | Clippers |
|---|---|---|---|---|---|---|
| STRAENGE | PAST | 1,997.56 | 2,000.00 | 99.9% | 2.44 | 13 |
| **bees.n.honey** | **ACTIVE** | 1,573.90 | 1,648.35 | **95.5%** | **74.45** | **56** |
| Panic Baby | ACTIVE | 1,419.94 | 2,000.00 | 71.0% | 580.06 | 34 |

**No bees.n.honey clipper is recorded below what they were paid.** It is the live EXPOSURE — 56 clippers, $74.45 of accrual from the same trim — not a victim. That distinction decides what needed repairing ($60.47, one person) versus what needed preventing (56 people).

**Platform-wide exposure: $60.47 realized, on one clipper.** The other $83.75 of the $144.22 is not this defect.

### The repair, as executed

**Owner decision, 2026-08-05: raise STRAENGE's budget FIRST, and mirror the owner rows.** That choice is what makes the repair breach nothing. STRAENGE stood at $2,998.10 of $3,000; restoring $60.47 alone would have made it the platform's first over-budget campaign and destroyed BL-627's measured "0 of ~180 over budget".

Executed via `scripts/run-mutation-once.js` on `scripts/migrations/BL-718-restore.sql`, every statement guarded on the exact BEFORE value so a second run changes 0 rows. **Rollback printed and committed BEFORE the write** as `scripts/migrations/BL-718-rollback.sql`.

```
[stmt 2] command=UPDATE rowCount=1     campaigns.budget 3000 -> 3100
[stmt 3] command=UPDATE rowCount=36    clips.earnings + clips."baseEarnings", 36 explicit ids
[stmt 4] command=UPDATE rowCount=36    agency_earnings.amount, same 36 clips
```

**How the 36 and their amounts were chosen.** Each clip's delta is its share of the clipper's total gap-to-entitlement. `earnings` and `baseEarnings` are raised by the **same** delta with `bonusAmount` untouched, so `earnings == base + bonus` holds to the cent by construction. **No clip was raised above its own independently computed entitlement: 0 of 36.** The 8 clips carrying no agency row were excluded (they hold $0.00 and only $6.75 of entitlement between them, and crediting them would have created rows with earnings and no owner mirror).

**Before and after:**

| | Before | After |
|---|---|---|
| Clipper A, STRAENGE recorded | $1,833.67 | **$1,894.14** |
| Clipper A, amount paid | $1,894.14 | $1,894.14 |
| **Shortfall** | **$60.47** | **$0.00** |
| STRAENGE clipper pool | 1,997.56 / 2,000.00 | **2,058.03 / 2,066.67** |
| STRAENGE owner reserve | 1,000.54 / 1,000.00 (over by 0.54) | **1,030.96 / 1,033.33** |
| STRAENGE total spend | 2,998.10 / 3,000 | **3,088.99 / 3,100** |

**All three are INSIDE their ceilings after the change, and the owner reserve is now inside where it was $0.54 over before.**

---

# PART 4 — proof the repair is right

Every figure below is a `SELECT` through `scripts/run-select.js` **after** the write.

| Claim | Evidence |
|---|---|
| Clipper A's recorded STRAENGE earnings now equal what he was paid | **$1,894.14 recorded vs $1,894.14 paid**, shortfall $0.00; he no longer appears in the recorded-below-paid population (8 rows to **7**) |
| His restored figure is inside what he genuinely earned | independent entitlement **$2,450.61** from views x stamped CPM x per-clip cap x minViews gate; $1,894.14 is **77.3%** of it. He gained nothing unearned |
| No clip was credited beyond its own entitlement | **0 of 36** |
| The owner-lock identity survives | `agency x 2 == earnings` on **72 of 72** clips with an agency row, exactly as before |
| Earnings invariant, Clipper A | **0 violations** on all 80 clips |
| Earnings invariant, full population | **0 violations** across APPROVED / PENDING / REJECTED / FLAGGED |
| BL-627 survives across the FULL population | **228 clippers**; 5 over-held totalling **$82.93**; **0 of them has a non-zero global cap**; 0 clippers whose cap exceeds `lifetime earned - paid - locked` |
| BL-690's over-held clippers still held at $0.00 | `cmofpudr` 36.75, `cmoaejuc` 23.09, `cmq0qn2l` 14.46, `cmoal818` 7.82, `cmova7yd` 0.81 — **all $0.00 available** |
| Platform earnings did not fall | APPROVED total **$11,235.94**, above BL-692's $10,191.26. The write only ADDED $60.47 |
| No clip status changed | the restore SQL touches `earnings`, `baseEarnings`, `updatedAt` only |
| No payout created, modified, approved or cancelled | **152 rows, $14,388.26**, newest `createdAt` **2026-08-05 07:35:56.442**, before this session's first query at 12:32:01 |
| Only the intended rows moved | exactly **36** STRAENGE clips changed since the restore. Every other clip that moved (Panic Baby 49, bees.n.honey 26, WinGram 10, BBA 1, SomeSome 1) belongs to the ordinary 10-minute cron on ACTIVE campaigns — STRAENGE is PAST, so the cron cannot reach it |

### What Clipper A will see change on his screens

* **Withdrawable balance: $345.60 becomes $406.55.** The $60.47 he has been complaining about since BL-714 is now reachable.
* **His STRAENGE campaign row: earned $1,833.67 becomes $1,894.14.** Unpaid stays $0.00 on that campaign either way, because it is now exactly settled rather than over-drawn.
* **His Panic Baby row (ACTIVE, $406.58 earned) becomes fully withdrawable.** Previously the global clamp held him to $345.60 while the campaign row showed $405+, which is the "about $61 vanished" discrepancy BL-714 traced. **That gap is now $0.00.**
* Nothing changes for any other clipper. No other row moved.

---

# PART 5 — proof it cannot recur

`npx tsx scripts/bl718-prove-paid-floor.ts` — READ-ONLY, writes nothing, runs no Apify actor, imports the **real exported helper** rather than a copy. **18 passed, 0 failed**, on the branch and again on the merge commit.

```
PASS  STRAENGE: OLD code trims BELOW the amount already paid  old=$1831.96 < paid=$1894.14 (takes $62.18)
PASS  STRAENGE: NEW code never goes below the amount already paid  new=$1894.14 >= paid=$1894.14
PASS  STRAENGE: NEW code still CAPS forward growth (no free money)  new=$1894.14 < uncapped=$2450.61
PASS  STRAENGE: the floor bound, and says so
PASS  STRAENGE: L1 invariant holds after the floor (earnings == base + bonus)
PASS  floor NEVER pushes campaign spend above max(already-committed, pool cap)  0 violations across 28,044 cases
PASS  capButNeverBelowStored never returns more than max(cap, stored)
PASS  capButNeverBelowStored(cap, stored) == cap when cap >= stored (byte-identical path)
PASS  NaN cap keeps the stored value
PASS  Infinity cap keeps the stored value
PASS  NaN stored falls through to the cap (corrupt row is not used as a floor)
PASS  null/undefined are treated as 0, never as NaN
PASS  capFloorDidBind is false on non-finite inputs
PASS  capFloorDidBind ignores sub-half-cent float noise
PASS  bees.n.honey: pool still has room, so OLD and NEW agree (no behaviour change yet)  old=$114.45 new=$114.45
PASS  bees.n.honey: once the pool fills, OLD code would take $35.00 off a clipper  old=$5.00 vs stored=$40.00
PASS  bees.n.honey: NEW code holds him at his stored value  new=$40.00
PASS  a legitimate reduction still passes through untouched (branch not entered)
```

**The budget-ceiling case specifically.** Replayed at STRAENGE's exact pinned conditions — pool cap $2,000, other clippers grown to $168.04, headroom $1,831.96, stored $1,894.14 — the old code writes $1,831.96 and takes $62.18. The new code writes $1,894.14 and takes nothing, while still capping the $2,450.61 recompute. **The exact conditions that produced the original trim no longer produce it.**

**bees.n.honey is safe.** Today the pool still has $74.45 of room, so old and new agree exactly and no clipper sees any change. Once that room is gone — 56 clippers, ACTIVE, tonight or next week — the old code would have started taking money off whoever was processed last. It now cannot. **Note honestly: the fix protects bees.n.honey from the moment `2c74f4fb` is DEPLOYED, not from the moment it was merged.**

**Last honest caveat, stated rather than buried.** The budget top-up re-opens about **$8.64** of clipper pool room on a PAST campaign. The cron cannot reach STRAENGE (`campaignStatusBlocks` covers `PAST`), but `recalculateUnpaidEarnings` has no campaign-status filter, so a STRAENGE clipper **without** a PAID payout there who opens their progress page could accrue into that room. Bounded at $8.64 and recorded in BACKLOG.

---

## Safety and gates, stated honestly

* **Money files.** 4 of the 6 plus `campaign-era.ts` **BYTE-IDENTICAL by blob OID** (`git rev-parse <ref>:<f>` vs `git hash-object`, never worktree-vs-`git show`): earnings-calc `797e2098`, balance `e887f80a`, middleware `61cef393`, money-decimal `ef5cdae7`, campaign-era `106e16ad`. **`tracking.ts` (`847dcf70` to `83ce4bab`) and `clip-earnings-writer.ts` (`7aa6be48` to `ac5be7de`) CHANGED**, both with the full diff printed and every line justified above and in the commit message. The writer had to change because it holds the BL-167 clamp, which is the same hole at the chokepoint; leaving it would have fixed the cron and left every admin path exposed.
* **Diff:** 7 files. Three source files, one read-only proof script, two SQL migrations, `BACKLOG.md`. The real `.ts` diff is non-empty (`158` insertions across the three source files) and is quoted in full in the commit.
* **No schema change, no `prisma migrate`** (only `npx prisma generate`). The only DDL-adjacent change is one `campaigns.budget` value, which is data.
* **No Apify actor ran.** The 11 BL-678 guards are untouched and were never reached; the proof harness makes no network call.
* **No clip status changed. No payout created, modified, approved or cancelled. No env flag flipped.** `GLOBAL_PAYOUT_CLAMP_ENABLED` was not touched. `agency-monitor --fix` **NOT run**. No platform-wide owner re-derive (BL-539's $933.94 untouched).
* **Gates, honest.** `npm ci` exit 0, then `npx prisma generate` exit 0 **before** typecheck. `npx tsc --noEmit` **exit 0 with 0 lines of output**. `npm run build` **BUILD_EXIT=0** read from a captured log with `echo $?`, **never piped through `tail`** — this mattered: build #1 genuinely exited **1** on a missing `NEXTAUTH_URL` in the fresh worktree while still printing "Compiled successfully", which a tail-piped read would have reported as green. Fixed by copying `.env`, not by ignoring it. BYPASS detector 0 violations, `check:removed-fields` OK, `lint:hooks` **11 problems (0 errors, 11 warnings)** at the <=11 cap with **eslint v9.39.4 confirmed executing**. Counts by `grep -c`, never `head`. Post-merge build re-run from scratch: **BUILD_EXIT=0**.
* **Accessibility:** no UI file is in the diff. No component, no JSX, no CSS, no markup, no copy string. There is nothing to review.
* **NO dashes** as bullets. No handle, email or wallet address printed.

## Rollback

```bash
git revert -m 1 2c74f4fb                 # the code
# or, to the pre-merge state:
git reset --hard pre-merge-BL-718        # 1faf072a
node scripts/run-mutation-once.js scripts/migrations/BL-718-rollback.sql   # the data
```

The data rollback restores `budget` to 3000 and all 36 clip rows and 36 agency rows to their **2026-08-05 12:32 UTC** values. It is guarded on the AFTER values, so it is a no-op if run twice or if the restore was never applied.

## What is still open

1. **`gamification.ts:906/912`** can still redistribute earnings between clippers who have not withdrawn, on any campaign including PAST ones. It cannot breach the paid floor, but it is the same sideways-movement shape. Own round.
2. **The $8.64** of re-opened pool room on STRAENGE, reachable only through `recalculateUnpaidEarnings`.
3. **The `breakdown` base/bonus inconsistency** at `tracking.ts:2534` and `gamification.ts:906`, pre-existing, now strictly less likely to fire.
4. **The other seven clippers recorded below what they were paid ($83.75)** are BL-627's by-design group. Four are deliberate owner `payoutReductionRatio` cuts, two were paid marginally above their true entitlement, one has no approved clips left. **None is owed money by this analysis**, and all seven remain correctly clamped at $0.00.
