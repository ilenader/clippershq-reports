# BL-784 — the owner-submit fabricated zero: real, unfixed, 14 clips, and it corrupted no curve and no dollar

**2026-08-12 · DB `now()` = `2026-08-12 09:55:31.276961+00` · AUDIT ONLY, READ ONLY.**
No code, data or money change. **Nothing repaired, nothing recalculated, `agency-monitor --fix` never run**, no probe made, no vendor call, $0.00 spent. Base `origin/main` @ `72f05cec`, branch `checkpoint/BL-784`, isolated worktree `C:/bl784`, `node_modules` never junctioned, removed at the end. Every read through `scripts/run-select.js`, every timestamp cast `::text` against DB `now()`. Handles redacted; clips, clippers and campaigns appear as id prefixes only; no wallet address is read or printed. A markdown-only diff cannot change tsc or a build, **so no build was run and none is claimed.** The live worktree `C:/bl783` was not touched.

## THE HEADLINE, INCLUDING THE PART THAT CONTRADICTS THE BRIEF

> **The defect is real and still in the code: `owner-submit-core.ts:193` initialises views to a literal 0 and `:291` writes it unconditionally, where the clipper path gates the identical write at `clipper-submit-core.ts:661`. Fourteen clips carry that zero, across all three platforms and the whole history.**
>
> **But the harm the brief expects is NOT there, and the reason is in the algorithm. `getViewArrival` takes the LAST snapshot at or before each mark, never the first. Recomputed per clip, the 6 hour figure with the fabricated zero present and with it removed are IDENTICAL on all 14: `null` on 13 because every one is backdated so the 6 hour mark falls before any snapshot exists, and 551 views on the one that is not. ZERO clips present a corrupted curve.**
>
> **And no money moved. All 14 carry an earnings invariant delta of exactly 0.0000, every figure tracks the CURRENT view count rather than the zero, and the two apparent shortfalls are explained by documented behaviour: a $300 per-clip cap times an immutable 0.8317 payout ratio, and a campaign AUTO-paused at its budget cap on 2026-08-07.**
>
> **It is also not ongoing in practice: the audit log puts the last owner submit at 2026-07-31 14:00:41, twelve days ago, with 0 in the last 7 days. The code is unchanged and would do it again on the next failed fetch.**

## PART 1 — THE MECHANISM, EXACTLY

**The gate is not absent. There is nothing for it to test.** That is the precise finding, and it decides the fix.

```ts
// src/lib/owner-submit-core.ts
:193   let fetchedStats = { views: 0, likes: 0, comments: 0, shares: 0 };   // NON-NULL from birth
:208     const fetchOut = await fetchClipStats(clipUrl, { skipHikerOverlay: true });
:209     const realStats = fetchOut.stats;
:210     if (realStats) { fetchedStats = { ...realStats } }                  // the null test EXISTS here
:215     else console.log(`... Apify returned null ... — starting with 0`);
:218     catch -> console.log(`... Could not fetch stats ... — starting with 0`);
:291   await tx.clipStat.create({ data: { clipId: newClip.id, views: fetchedStats.views, ... } });  // UNCONDITIONAL
```

```ts
// src/lib/clipper-submit-core.ts
:406   let fetchedStats: { views: number; ... } | null = null;              // NULLABLE from birth
:537   if (fetchedStats == null && harvested && typeof harvested.views === "number") { ... }
:660   const resolvedFirstViews = fetchedStats?.views;
:661   if (resolvedFirstViews != null) { await tx.clipStat.create({ ... }) }  // GATED
```

**The difference in one sentence: the clipper path keeps `fetchedStats` nullable so a failed fetch is representable, and the owner path overwrites the failure with a zero at `:193` before anything downstream can see it.** By `:291` the information that no measurement was taken has already been destroyed. The gate is therefore **inapplicable as written**, not merely missing: there is no null left to test. The truth still exists one variable away, at `:210`'s `if (realStats)`, which is the whole reason the fix in PART 6 is small.

**THE EXACT CONDITION UNDER WHICH A 0 IS WRITTEN RATHER THAN SKIPPED:** `fetchClipStats(clipUrl, { skipHikerOverlay: true })` returns `stats === null` (every provider tier failed, the URL is dead, or the platform is unsupported by the chain) **or throws** (timeout, HTTP error, malformed body). Both land at `:215` or `:218`, both log "starting with 0", and `:291` stores that zero as a measurement. A genuine reading of 0 from a resolving provider is also written and is correct; **stored data cannot tell the two apart**, which is the second-order harm.

### How the two paths diverged, from the record

| when | what happened | did it reach the owner path? |
|---|---|---|
| 2026-06-22, **BL-211** | `owner-submit-core.ts` created as a **"PURE behavior-preserving extraction"** of the owner route so single and bulk share one money path. It inherited the route's existing `views: fetchedStats.views` shape verbatim. | The defect was carried in, not introduced. |
| 2026-07-16, **BL-543** | states the rule: *"an unresolvable or view-less clip stores NULL, never 0"*. Its own scope note lists **`owner-submit-core.ts` among the files it did not touch**, because BL-541 held them. | **No.** Explicitly out of scope. |
| 2026-07-20, **BL-605 PART 2** | fixed exactly this bug, at `clips/route.ts:1137`, replacing `views: fetchedStats?.views ?? 0` with the `if (resolvedFirstViews != null)` skip. One file, the clipper route. | **No.** The owner route was never in the diff. |
| 2026-08-09, **BL-746** | added the `viewSource != null` requirement on the clipper path so a hidden Instagram count cannot fabricate a 0. | **No.** |
| 2026-08-09, **BL-748** | fixed `hikerapi.ts:603` at source and mapped **all six callers** of that classifier. | **No, and correctly so.** The owner path calls `fetchClipStats(..., skipHikerOverlay: true)`, which routes through Apify and never touches `classifyV2Media`. It was not a missed caller; it was never a caller. |

**So this is BL-605's bug, surviving on the one submit path BL-605 did not open**, and neither BL-746 nor BL-748 could have caught it because both operate on a classifier the owner path deliberately bypasses.

### It is not the only ungated writer, and the other two matter less than they look

Every non-generated `clipStat.create` site in `src/`:

| site | gate | status |
|---|---|---|
| `src/lib/clipper-submit-core.ts:662` | **`if (resolvedFirstViews != null)`** | correct |
| `src/lib/owner-submit-core.ts:291` | **none** | **the defect, live** |
| `src/actions/clips.ts:119` | **none**, `views: fetchedStats?.views ?? 0`, the exact pre-BL-605 shape | **DEAD CODE.** `grep` finds **zero** importers of `@/actions/clips` anywhere in `src/`. A landmine, not a leak. |
| `src/app/api/marketplace/submissions/[id]/post/route.ts:723` | **none**, hardcoded `views: 0` | **NEVER FIRED.** Production holds **0** marketplace clips. It also makes no provider call at all, so its zero is a stated baseline rather than a discarded measurement. |
| `src/lib/tracking.ts` (2 sites) | money file, its own null handling, out of scope | untouched |

## PART 2 — EVERYTHING `owner-submit-core.ts` TOUCHES, AND WHY BL-782 STOPPED

| file:line | what it does |
|---|---|
| `:50-60` | `parseOwnerSubmitPostedAt`, rejects a future date and anything over **90 days** old |
| `:64-111` | `validateOwnerSubmitContext`: campaign exists, refuses an **AUTO-paused** campaign, refuses override on a test campaign, target must be a live non-banned CLIPPER, account owned and APPROVED |
| `:135-140` | URL sanitize (`sanitizeClipUrl`) and shape validation |
| `:144-155` | duplicate gate, **CAMPAIGN scope only** |
| `:157-164` | platform detection and the per-platform CPM allow check |
| `:166-183` | account resolve, including **creating a placeholder `clipAccount`** at `:176` when the target has none |
| `:186-190` | CPM resolve and the `customCpm` cap (`min(customCpm, campaignCpm)`) |
| **`:193`** | **`fetchedStats` initialised to zeros — the defect's origin** |
| `:200-219` | the single provider call, `skipHikerOverlay: true`, plus `platformPostedAt` for the backdate check |
| `:236-243` | **BL-541 backdate verification** against the platform's own timestamp |
| `:246-252` | `updateStreak`, then the streak snapshot read |
| `:255-262` | **CPM stamp invariant** (`enforceCpmStampInvariant`) |
| `:267-300` | **ONE transaction**: `clip.create` `:268` (status APPROVED, `isOwnerOverride: true`, `createdAt` overridden by `postedAt` at `:277`, `backdateVerifiedAt` `:285`), **`clipStat.create` `:291`**, `trackingJob.create` `:298` with the first check at the next hour |
| `:301-317` | P2002 backstop mapping a unique-constraint clash to a friendly message |
| **`:320-356`** | **THE MONEY.** `recalculateClipEarningsBreakdown` `:331`, **`writeClipEarnings` `:338`**, and the **agency earning** `:349`, all gated on **`if (fetchedStats.views > 0)` at `:320`** |
| `:359-364` | audit row, `OWNER_OVERRIDE_SUBMIT` or `OWNER_SELF_SUBMIT` |

**Why an incautious edit is expensive:** `fetchedStats` is read in **three** places, and only one of them is the snapshot. `:291` writes the stat, `:320` decides whether earnings are written at all, and `:332` and `:348` supply the view count to the earnings and agency calculations. **Any change to `:193` that makes `fetchedStats` nullable touches the money gate at `:320` in the same breath.** That is exactly why BL-782 stopped, and the PART 6 spec is written to keep the money expression byte-identical.

### Deliberate owner exemptions, which a fix must NOT remove

The file names them itself at `:13-15`: *"owner-submit (override) deliberately does NOT enforce the 30-min freshness gate and deduplicates CAMPAIGN-scope only (not user-scope) — both behaviors are preserved exactly here."*

| behaviour | verdict | evidence |
|---|---|---|
| no 30-minute freshness gate | **DELIBERATE**, and the whole point of the route: BL-704 established the batch path's freshness position and BL-709 made the owner exemption explicit; backdating up to 90 days is a feature with a `requireOwner` gate in front of it | `:13-15`, `:50-60` |
| campaign-scope dedupe only | **DELIBERATE** | `:13-15`, `:147-150` |
| auto-APPROVED with `reviewedAt` stamped at submit | **DELIBERATE** | `:276`, `:286` |
| `isOwnerOverride: true` unconditionally | **DELIBERATE and PROVENANCE ONLY** since BL-541: who pressed upload never decides money | `:273-276` |
| earnings written at submit when views resolve | **DELIBERATE** | `:320-338` |
| **first `ClipStat` written even when nothing resolved** | **DEFECT** | `:193` with `:291` |

**A fix must change exactly one of those seven rows.**

## PART 3 — THE FULL DAMAGE, ALL PLATFORMS, FULL HISTORY

Every clip whose **first** `ClipStat` is 0, split by creating path, live rows only:

| route | platform | zero first stat | later positive | later >= 1,000 | last 7 days | last 30 days | most recent |
|---|---|---|---|---|---|---|---|
| **owner-submit** | **instagram** | **12** | **12** | **12** | **0** | 11 | 2026-07-26 21:57:03 |
| **owner-submit** | tiktok | **1** | 1 | 0 | **0** | 0 | 2026-06-20 12:33:21 |
| **owner-submit** | youtube | **1** | 1 | 0 | **0** | 0 | 2026-07-06 10:32:41 |
| clipper-submit | youtube | 1,239 | 1,163 | 245 | 0 | 130 | 2026-08-02 21:45:38 |
| clipper-submit | instagram | 945 | 888 | 399 | 152 | 243 | 2026-08-12 09:16:53 |
| clipper-submit | tiktok | 497 | 437 | 167 | 8 | 68 | 2026-08-11 22:07:47 |

**BL-782's "12 of 35" widens to 14 across three platforms, out of 103 live owner-submitted clips: a 13.6% rate.** `isOwnerOverride` is a sound route marker: **102 of the 103** carry a matching `OWNER_*_SUBMIT` audit row.

**The 2,681 clipper-path zeros are a different thing and must not be counted as damage.** A clip submitted inside the 30 minute posting window genuinely has ~0 views, and since BL-605 the write only fires on a non-null resolve, so a stored 0 is a real reading. Split at BL-605 (2026-07-20): **2,401 before, 280 after**. **The pre-BL-605 subset may contain fabrications and stored data cannot identify them**, because the provider response was never retained. This round puts no number on it rather than guessing.

### The fourteen, redacted

| clip | clipper | campaign | platform | fabricated 0 at | first real reading | minutes | views now | earnings |
|---|---|---|---|---|---|---|---|---|
| `cmp2hc6g` | `cmofpu` | `cmoaa7` | instagram | 2026-05-12 10:20:22 | 473 | 192.6 | **1,062,360** | $266.98 |
| `cms2c90f` | `cmn4nl` | `cmqcnz` | instagram | 2026-07-26 21:57:03 | 1,769 | 65.2 | 180,944 | $86.41 |
| `cms240aw` | `cmosj3` | `cmqcnz` | instagram | 2026-07-26 18:06:20 | **118,848** | 55.6 | 122,786 | $61.85 |
| `cms2c90c` | `cmn4nl` | `cmqcnz` | instagram | 2026-07-26 21:57:03 | 3,459 | 65.2 | 3,900 | $1.95 |
| `cms2433s` | `cmosj3` | `cmqcnz` | instagram | 2026-07-26 18:08:31 | 2,082 | 53.5 | 2,125 | $1.07 |
| `cms2c90c` | `cmn4nl` | `cmqcnz` | instagram | 2026-07-26 21:57:03 | 1,672 | 65.2 | 2,124 | $1.06 |
| `cms23z4o` | `cmosj3` | `cmqcnz` | instagram | 2026-07-26 18:05:25 | 2,048 | 56.6 | 2,077 | $1.05 |
| `cms2c90b` | `cmn4nl` | `cmqcnz` | instagram | 2026-07-26 21:57:03 | 1,644 | 65.2 | 1,731 | $0.87 |
| `cms23z4o` | `cmosj3` | `cmqcnz` | instagram | 2026-07-26 18:05:25 | 1,608 | 56.6 | 1,634 | $0.82 |
| `cms240ar` | `cmosj3` | `cmqcnz` | instagram | 2026-07-26 18:06:20 | 1,531 | 55.6 | 1,591 | $0.80 |
| `cms242ic` | `cmosj3` | `cmqcnz` | instagram | 2026-07-26 18:08:03 | 1,445 | 53.9 | 1,483 | $0.75 |
| `cms23z4s` | `cmosj3` | `cmqcnz` | instagram | 2026-07-26 18:05:25 | 1,329 | 56.6 | 1,345 | $0.68 |
| `cmqmc9f3` | `cmpqbx` | `cmqcnz` | tiktok | 2026-06-20 12:33:21 | 353 | 97.3 | 759 | $0.00 |
| `cmr92zv7` | `cmqic8` | `cmq853` | youtube | 2026-07-06 10:32:41 | 2 | 148.2 | 1 | $0.00 |

**Four clippers and three campaigns**, heavily concentrated: 11 of 14 sit in one campaign and 6 belong to one clipper. **`cms240aw` is the clearest proof of fabrication in the set: a reel already 24 hours old, stored as 0 views, reading 118,848 views 55.6 minutes later.**

### Is it ongoing?

**The code is unchanged** (`owner-submit-core.ts` blob OID `4cd23e30`, identical to BL-782's reading) **so the next failed fetch on this route will do it again.** In practice the route is idle: the audit log records **0 owner submits in the last 7 days**, 23 in 30 days, and the most recent at **2026-07-31 14:00:41**, twelve days ago. **The audit log is the right clock here and the clip table is not**: backdating rewrites `createdAt` at `:277`, which is why the newest affected clip reads 2026-07-26 while the route was last used on 07-31.

## PART 4 — THE SIGNAL AND THE MONEY, SEPARATELY

### THE SIGNAL: no curve is corrupted, and the reason is structural

`getViewArrival` (`src/lib/review-evidence.ts:210-219`) computes each mark as **the LAST snapshot at or before it**, not the first:

```ts
const at = (hours) => { const cutoff = clipCreatedAt + hours*3_600_000;
  if (lastSnapshot.checkedAt < cutoff) return null;      // mark never reached
  for (const s of stats) if (s.checkedAt <= cutoff) last = s.views; else break;
  return last; }                                          // null if none at or before
```

**So a fabricated 0 can only reach the 6 hour figure if it is still the newest snapshot at the 6 hour mark** — that is, only if no real reading lands in the clip's first six hours. Two things make that nearly impossible here: the owner route sets the first tracking check to the next hour (`:292-297`), and every affected clip is backdated, so the 6 hour mark falls **before** the first snapshot exists.

Recomputed per clip, the 6 hour value **as it reads today** against **as it would read had the snapshot been skipped**:

| clips | 6h with the zero present | 6h with the zero removed | corrupted? |
|---|---|---|---|
| 13 of 14 | **null** ("the mark was never reached") | **null** | **no, identical** |
| `cmqmc9f3` | **551 views** | **551 views** | **no, identical** |

**Zero of the fourteen present a corrupted curve, and none ever did.** The brief's premise that a fabricated first zero makes a clip "look like it started from nothing" is **refuted for this codebase**: it would be true of a curve read from the FIRST snapshot, and this one is read from the last-at-or-before each mark.

**Whether any has been shown on BL-776's panel is UNKNOWABLE** — no impression log exists. What is knowable is what it would render: the panel is owner-gated at `/admin/clips`, and for 13 of these it prints the "mark not reached" wording rather than a number, which is the honest empty state BL-775 designed and not a misleading zero.

**One residual, stated because it is the real cost:** the fabricated row still inflates `snapshotCount` by one, and BL-776 suppresses a curve below 3 snapshots. Three of the fourteen sit at exactly 10 snapshots and none is near the threshold, **so no clip crossed the suppression boundary because of a fabricated row.** Checked, not assumed.

### THE MONEY: nothing was affected, proven three ways

| clip | views now | earnings | base + bonus | expected from views x CPM | invariant delta |
|---|---|---|---|---|---|
| `cmp2hc6g` | 1,062,360 | $266.98 | 249.51 + 17.47 | $1,062.36 raw, **capped at $300 then x 0.8317 = $249.51** | **0.0000** |
| `cms240aw` | 122,786 | $61.85 | 61.24 + 0.61 | $61.39 | **0.0000** |
| `cms2c90f` | 180,944 | $86.41 | 86.41 + 0.00 | $90.47 | **0.0000** |
| the other 11 | — | — | — | match to the cent | **0.0000** |

**1. Every figure tracks the CURRENT view count, not the zero.** At a stamped $0.50 CPM, `cms2433s` at 2,125 views holds $1.07 and `cms23z4s` at 1,345 holds $0.68. Had the zero persisted into earnings, all fourteen would read $0.00.

**2. The two apparent shortfalls are documented behaviour, not damage.** `cmp2hc6g` carries `maxPayoutPerClipAtApproval = 300` and an immutable `payoutReductionRatio = 0.8317`; 300 x 0.8317 = **$249.51**, which is its stored base **exactly**. `cms2c90f` trails the latest reading by 4.5% because campaign `cmqcnz` has been **AUTO-paused at its budget cap since 2026-08-07 17:01:49**, which is the budget system stopping accrual as designed.

**3. The zeros are structurally incapable of costing money.** `writeClipEarnings` is called with `stats: [{ views: fetchedStats.views }]` at submit and recomputed from the **latest** reading on every tracking tick, so a first snapshot never enters an earnings calculation after the first minute. BL-538's never-decrease guard and BL-543's rule both protect a **replacement** of a higher value by 0; **a first snapshot has nothing to replace.** The two clips reading $0.00 are below the campaign's `minViews` of 1,000 (759 and 1 views), which is correct.

**The one real money consequence, and it is a timing one:** `:320`'s `if (fetchedStats.views > 0)` means a failed fetch also skips the initial `writeClipEarnings`, so the clip sits at $0.00 until the first tracking tick roughly an hour later. **Measured: every one of the fourteen recovered.** Nobody was underpaid; somebody was briefly shown a zero.

## PART 5 — WHY THE CLIPPER PATH SURVIVED

**It keeps the failure representable and the owner path does not.** `clipper-submit-core.ts:406` declares `fetchedStats` as `| null` and leaves it null until something real arrives, so `:661` has a fact to test. `owner-submit-core.ts:193` destroys that fact one line before the fetch.

**Does the owner path have a `viewSource` equivalent? No, and it does not need one.** `viewSource` is a field of the **HikerAPI** classifier result, and the owner path never calls it: `fetchClipStats(..., skipHikerOverlay: true)` routes through Apify, whose `ClipStats` interface (`apify.ts:297-305`) has no `viewSource` at all. **The equivalent signal is `fetchOut.stats === null`, which the code already computes and already branches on at `:210`.** BL-746's guard exists because the Hiker classifier could return a number that was never read from a field; Apify's chain has no such case, so a null return is the complete signal.

**So the same gate is not only possible, it is one line**, and it is strictly narrower than BL-746's because it has one failure mode to cover instead of two.

## PART 6 — TWO SPECS, KEPT APART

### A. THE CODE FIX

**Change, `src/lib/owner-submit-core.ts`:**
1. `:193` — add a sibling flag rather than making `fetchedStats` nullable: `let statsResolved = false;`
2. `:211` — inside `if (realStats)`, set `statsResolved = true;` alongside the existing assignment. Nothing else in the block changes.
3. `:291` — wrap the write: `if (statsResolved) { await tx.clipStat.create({ ... }) }`, the create itself byte-identical.

**Deliberately NOT changed:** `:320`'s `if (fetchedStats.views > 0)`, `:332` and `:348`'s view arguments, and the `fetchedStats` type. **The money expression stays byte-identical**, which is the property that makes this safe and is the reason for a flag rather than a nullable object.

**Behaviour delta, complete:** exactly one case moves. Provider resolved (including a genuine 0) writes as today. Provider returned null or threw now writes **no snapshot** instead of a zero, and the tracking job created at `:298` writes the first real one at the next hour, which is precisely what BL-605 chose for the clipper path.

**Prove before merge:**
1. `git show` blob OID equality for the **6 money files**, `tracking.ts`, `campaign-era.ts`, `apify.ts` and `clipper-submit-core.ts` on both refs.
2. **`git diff` of `owner-submit-core.ts` shows exactly 3 changed lines and none inside `:320-356`**, printed in the report.
3. A harness in the BL-746 and BL-748 shape, driving the guard extracted from the shipped source: resolved-with-views writes, **resolved-with-a-genuine-0 still writes**, null-stats skips, thrown-error skips, and every skip additionally asserts `views !== 0`.
4. **No earnings behaviour moved**: run the harness for the `:320` gate with `fetchedStats.views` at 0 and at N, asserting `writeClipEarnings` is called identically to today in both, and confirm `check:prisma-bypass` (which carries the earnings-write check) reports 0 violations.
5. Live before and after: earnings invariant at 0 violations, no `payout_requests` row touched, no clip status changed, and clip and money fingerprints identical.
6. Standard gates: `npm ci`, `prisma generate` before `tsc`, `tsc --noEmit` 0 errors, `npm run build` exit 0 read from a log, hooks gate 0 errors and 11 warnings with eslint confirmed present.

**The exemptions survive by construction:** the change touches neither the freshness bypass, the campaign-scope dedupe, the auto-approve, the `isOwnerOverride` stamp, nor the earnings gate. **Rollback:** `git revert` the commit. **Nothing to undo in the database, because the fix writes nothing and repairs nothing.**

### B. THE DATA REPAIR: DO NOT DO IT

**Recommendation: leave all 14 rows exactly as they are. No repair is safe, and none is necessary.**

**Not necessary**, because PART 4 proves the rows cost nothing: no curve is corrupted, no earnings figure is wrong, and every clip recovered a real reading within 53 to 193 minutes.

**Not safe**, on three grounds. **Deleting a row rewrites history that has already been read**: BL-782 established historical curves must remain as recorded, and `snapshotCount` and `trackedHours` are both computed from the stored series. **`ClipStat` has no provenance column**, so nothing distinguishes a fabricated 0 from a genuine 0 at repair time except an inference from the next reading, and that inference would also delete real zeros from genuinely new posts. **And the repair would be a data mutation on a money-adjacent table for zero measured benefit**, which is the worst trade in the repertoire.

**What a reviewer should see in the meantime: exactly what they see today.** For 13 of the 14 the panel already prints the "not reached" wording rather than a number, and for `cmqmc9f3` it prints 551 views, which is a real reading. **No interim UI change is warranted and none is proposed.**

**If the owner disagrees and wants the rows gone anyway**, the only defensible version is: delete a first `ClipStat` **only** where `views = 0`, `isOwnerOverride = true`, a later row is positive, and the clip is backdated by more than an hour, run through `run-mutation-once.js` with the 14 ids enumerated by hand and printed before and after. That is a specification, not a recommendation.

## PART 7 — THE VERDICT

> **The defect is live in the code and idle in practice: 14 clips ever carry a fabricated zero, 0 in the last 7 days, ZERO corrupted curves because the arrival curve reads the last snapshot before each mark rather than the first, and ZERO dollars affected with all 14 at an invariant delta of exactly 0.0000.**

**Urgency: LOW, and it should be fixed anyway.** It is a three-line change with a one-line rollback, it touches only owner-submitted clips, and BL-782's framing holds up: **it affects only the owner's own view of his own submissions.** Ranked against the platform's open work it sits below the bundle.social pipeline that has still never returned an analytics field and below anything clipper-facing, and above nothing that is currently costing money, because it is currently costing none.

**What earns it a place on the list at all is not the 14 rows. It is that the platform states a contract — an unresolvable clip stores nothing, never a zero — and one live path silently breaks it.** The next owner submit against a dead URL writes another one, and the reason it has been harmless so far is the arrival curve's shape rather than any guard.

## WHAT COULD NOT BE MEASURED

**How many of the 2,401 pre-BL-605 clipper-path zeros were fabricated.** The provider response is not retained and a genuine 0 on a freshly posted clip is indistinguishable from a discarded null in stored data. No number is offered.
**Whether any affected clip was ever actually displayed on the evidence panel.** No impression log exists.
**Whether `fetchClipStats` returned null or threw for each of the 14.** Both paths log to the console and neither is persisted, so the split between "provider chain exhausted" and "exception" is unknown; the outcome is identical either way.
**Why `cms2c90f` trails its latest reading by 4.5%** beyond the campaign being AUTO-paused at its budget cap on 2026-08-07, which this round did not trace further because it is the budget system's documented behaviour and not this defect.

## SAFETY

READ ONLY, one document, on `checkpoint/BL-784` from `origin/main` `72f05cec`. **No code, data or money change; nothing repaired, nothing recalculated, `agency-monitor --fix` never run, no probe, no vendor call, no Apify actor, $0.00 spent, no schema change, no `prisma migrate`.** Deliberate owner exemptions are separated from the defect in PART 2 and the fix spec changes exactly one of seven behaviours. The signal and money consequences are quantified independently and neither is assumed harmless: both were computed per clip. The full history across all three platforms is measured rather than inherited from BL-782's Instagram-only count. No recomputation of any historical arrival curve is proposed, and the data repair is recommended **against**. Every timestamp is cast `::text` against DB `now()`; handles are redacted, ids are truncated to prefixes, and no wallet address was read or printed. The 6 money files, `tracking.ts` and `campaign-era.ts` are untouched: this diff is one markdown file. The live worktree `C:/bl783` was not touched and this round's worktree is removed. No dashes as bullets.

**Rollback:** delete branch `checkpoint/BL-784`. It contains one document and touches nothing.
