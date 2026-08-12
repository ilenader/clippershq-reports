# BL-785 — the owner-submit path now skips instead of fabricating a zero, in three lines, with the money expression untouched

**2026-08-12 · DB `now()` = `2026-08-12 10:56:41.923187+00` before, `10:58:22.707353+00` after · BUILD.**
Base `origin/main` @ `72f05cec`. Branch `checkpoint/BL-785`, carrying the fix plus the merges of `checkpoint/BL-783` and `checkpoint/BL-784`. Isolated worktree `C:/bl785`, short path, `node_modules` never junctioned, removed at the end. **No submission was created, no Apify actor run, no probe made, $0.00 spent, no schema change, no `prisma migrate`, nothing repaired.** Every database read through `scripts/run-select.js`, every timestamp cast `::text` against DB `now()`. Handles redacted; ids truncated to prefixes.

## WHAT SHIPPED

> **Three executable lines. `owner-submit-core.ts:193` destroyed the null before the write could test it, so a failed provider fetch was stored as a measurement of nothing. The null is now preserved beside the counters, set only where a provider actually answered, and tested immediately around the existing write. The create expression is byte-identical apart from its indentation, and the earnings expression is untouched by design.**
>
> **The 14 historical clips are DELIBERATELY LEFT and are not unfinished work.**
>
> **Both docs branches merged after verifying by SHA that each genuinely carries commits: `checkpoint/BL-783` at `96b0c407` and `checkpoint/BL-784` at `1bb08f35`, one commit and one report each, zero conflicts. `checkpoint/BL-723` NOT merged.**

## PART 1 — THE FIX, FULL DIFF, EVERY LINE JUSTIFIED

```diff
--- a/src/lib/owner-submit-core.ts
+++ b/src/lib/owner-submit-core.ts
@@ -191,6 +191,22 @@
     // Fetch real stats BEFORE create (route L294-308).
     let fetchedStats = { views: 0, likes: 0, comments: 0, shares: 0 };
+    // BL-785 — DID A PROVIDER ACTUALLY ANSWER? The line above initialises the
+    // counters to zero and is deliberately left alone, because three later sites
+    // read `fetchedStats.views` as a number: the earnings gate at :320 and the
+    // view arguments at :332 and :348. Making it nullable would change the money
+    // expression, so the fact that is missing is carried alongside it instead.
+    //
+    // WHY IT IS MISSING AT ALL (BL-784): a failed fetch leaves the zero above in
+    // place, and the first `ClipStat` write then stored that zero as though it
+    // were a measurement. BL-605's contract is that an unresolvable clip SKIPS
+    // the snapshot, because `ClipStat.views` is a non-nullable Int and a
+    // fabricated 0 is indistinguishable from a real one; BL-543 states the same
+    // rule as NULL never 0. The clipper path keeps its own `fetchedStats`
+    // nullable and gates on it (clipper-submit-core.ts:661); this path could not,
+    // so the null was destroyed one line before the fetch and the gate at :291
+    // had nothing to test. This flag is that null, preserved.
+    let statsResolved = false;
@@ -209,6 +225,11 @@
       if (realStats) {
         fetchedStats = { views: realStats.views, ... };
+        // BL-785 — set ONLY here, inside the existing `if (realStats)`, so it is
+        // true exactly when a provider returned a body we parsed. A genuine
+        // reading of 0 from a brand-new post sets it too, and is still written:
+        // a real zero is a measurement, only an absent one is not.
+        statsResolved = true;
         platformPostedAt = realStats.createdAt ?? null;
@@ -288,7 +309,14 @@
         });
-        await tx.clipStat.create({ data: { clipId: newClip.id, views: fetchedStats.views, likes: fetchedStats.likes, comments: fetchedStats.comments, shares: fetchedStats.shares } });
+        // BL-785 / BL-605 / BL-543 — SKIP rather than write a fabricated 0. The
+        // create itself is unchanged; only the guard is new. When no provider
+        // answered, no snapshot is written and the tracking job created three
+        // lines below takes the first real reading at the next hour, which is
+        // exactly what the clipper path does (clipper-submit-core.ts:661).
+        if (statsResolved) {
+          await tx.clipStat.create({ data: { clipId: newClip.id, views: fetchedStats.views, likes: fetchedStats.likes, comments: fetchedStats.comments, shares: fetchedStats.shares } });
+        }
         const initialInterval = getLockedIntervalFloor({ ... }) ?? 60;
```

**Three executable lines, in three hunks, and 29 insertions of which 26 are comment.** Line by line:

**1. `let statsResolved = false;`** carries the fact the initialiser destroys. **Why a flag and not a nullable `fetchedStats`:** three later sites read `fetchedStats.views` as a number — the earnings gate at `:320`, the breakdown argument at `:332` and the owner-share argument at `:348`. Making the object nullable would have rewritten all three, which is precisely the widening BL-784 said to stop at.

**2. `statsResolved = true;`** sits **inside the existing `if (realStats)` block**, added and nothing else in that block touched. It is therefore true exactly when a provider returned a body that parsed. **A genuine reading of 0 sets it and is still written**, which is the behaviour BL-605 specified: a real zero is a measurement, only an absent one is not.

**3. `if (statsResolved) { ... }`** around the existing `tx.clipStat.create`. **The create expression is byte-identical**; the harness asserts that string appears exactly once and sits inside the guard. The only textual change to that line is two spaces of indentation.

**Nothing else in the file changed**, and the diff shows it: three hunks, none inside `:320-356`, no fourth site touched. **The change did not need to widen, so it did not.**

### The contracts, proven rather than promised

| contract | how it now holds |
|---|---|
| **BL-605**, an absent count SKIPS rather than writing 0 | null stats, an absent `stats` field, and a thrown fetch all leave `statsResolved` false, so no row is created and the tracking job created three lines below takes the first real reading at the next hour |
| **BL-543**, NULL never 0 | a skip writes nothing at all; `ClipStat.views` is a non-nullable `Int`, so skipping is the only honest representation and a fabricated 0 is now unreachable on this path |
| **BL-704**, the owner freshness bypass is DELIBERATE | untouched and asserted: the header note survives, and the file contains **no** `MAX_CLIP_AGE`, **no** `clip-config` import and **no** `evaluateInstagramFreshness` reference. The 90-day backdate bound, the campaign-scope dedupe and the auto-approve are all asserted intact |

## PART 2 — THE 14 HISTORICAL CLIPS ARE DELIBERATELY LEFT

**Nothing was repaired. No `ClipStat` row was updated, deleted or backfilled, and no historical arrival curve was recomputed.** The harness additionally asserts the file gained no `clipStat.update`, no `delete`, no `deleteMany` and no raw SQL.

**Why, from BL-784's measurements rather than a preference:** all 14 read **identically** with the fabricated zero present or removed, because `getViewArrival` (`src/lib/review-evidence.ts:210-219`) takes the **last** snapshot at or before each mark rather than the first, and every affected clip is backdated so the 6 hour mark falls before any snapshot exists. All 14 sit at an earnings invariant delta of exactly **0.0000**. Repairing them would rewrite a history that has already been read, and `ClipStat` carries **no provenance column**, so nothing at repair time could tell a fabricated zero from a genuine one without also deleting real zeros from genuinely new posts.

**This is a decision, not an omission. A future round must not treat the 14 as unfinished work.** Their 626 stat rows are fingerprinted before and after in PART 4 and are byte-identical.

## PART 3 — THE MERGES

**Verified by SHA before merging, because BL-779 found a branch carrying zero commits behind a published report:**

| branch | tip | ancestor of main? | unique commits | diff |
|---|---|---|---|---|
| `checkpoint/BL-783` | `96b0c407` | **NO**, genuinely unmerged | **1** | 1 file, **294 insertions**, docs only |
| `checkpoint/BL-784` | `1bb08f35` | **NO**, genuinely unmerged | **1** | 1 file, **254 insertions**, docs only |
| `checkpoint/BL-723` | `22039307` | NO | 2 | 112 files, 2,285 insertions, **16,247 deletions** — **NOT MERGED, as instructed** |

Both merges `--no-ff`, **exit 0, zero conflicts**, so no union resolution was required. **BACKLOG entries: 140 before, 140 after both merges** because neither docs branch touched the file, then **141** after this round's own entry, counted with `grep -c` and never piped to `head`. **Conflict markers tree-wide: 0.** `checkpoint/BL-723` re-checked after the merges and confirmed still **not** an ancestor of HEAD.

**BL-783 corrects BL-781, and the correction is carried forward rather than buried.** A qualifying Instagram vendor **does** exist — **PostPeer at $25 to $43 a month**, returning `avgWatchTime` and `totalWatchTime` for Reels through Meta's own OAuth with unlimited connected accounts, and four vendors in total return real Instagram watch time. BL-781 was right that bundle.social has no Instagram watch-time field and **wrong to leave the impression that no vendor has one**. **The verdict does not change and now rests on value rather than availability:** no completion or skip rate, the free arrival curve already computes on **96.2%** of Instagram clips at zero cost, and **82.6%** of Instagram bought-view rejections are already caught by a repeat-offender signal that is shipped and mounted today.

**Main is not touched by this round.** The branch carries the fix and both reports; a merge round takes it to `main` with `git merge --no-ff origin/checkpoint/BL-785`.

## PART 4 — THE EVIDENCE

**No real submission was created, so nothing needs reversing.** The owner path cannot be exercised without writing a clip, an earning and an audit row, so it is proven by driving the shipped decision instead, exactly as BL-746 and BL-748 proved theirs.

**`scripts/test-bl-785-owner-submit-skip.mjs`: 41 passed, 0 failed, exit 0.** It extracts the shipped guard from source rather than retyping it, so it cannot drift; it creates no submission, makes no network call and touches no database.

```
provider returned a real count                        -> WRITES  118848
provider returned a GENUINE 0 on a brand-new post     -> WRITES  0        (correct, a real zero)
provider returned null stats (every tier failed)      -> SKIPS             ...and stores NO zero
provider returned undefined stats                     -> SKIPS             ...and stores NO zero
provider threw (timeout, HTTP error, malformed body)  -> SKIPS             ...and stores NO zero
```

**Earnings behaviour did not move, case by case.** The harness computes the pre-fix earnings decision and the shipped one over the same five outcomes and asserts they are identical:

```
earnings UNCHANGED: real count      written true->true    views 118848->118848
earnings UNCHANGED: genuine 0       written false->false  views 0->0
earnings UNCHANGED: null stats      written false->false  views 0->0
earnings UNCHANGED: undefined       written false->false  views 0->0
earnings UNCHANGED: threw           written false->false  views 0->0
```

**The clipper path is provably unchanged**, by blob OID (`clipper-submit-core.ts` `c2d13a00` on both refs), by assertion (its BL-605 gate and BL-746 `viewSource` guard each present exactly once, exactly one awaited HikerAPI call, and `statsResolved` appears nowhere in it), and by re-running its own harnesses on the fixed tree: **BL-746 48 passed 0 failed, BL-748 39 passed 0 failed**, both exit 0.

**One harness assertion failed on its first run and it was a harness bug, recorded rather than quietly corrected:** the BL-704 exemption note it looks for wraps across two comment lines in the shipped header, so a single-string match could never succeed. The assertion now matches the two fragments it actually occupies. The code was never at fault.

### Live data, before and after

| measure | before `10:56:41Z` | after `10:58:22Z` |
|---|---|---|
| clips total | 5,498 | 5,498 |
| **earnings invariant violations** | **0** | **0** |
| approved earnings, `videoUnavailable = false` | **$8,688.38** | **$8,688.38** |
| payout rows / payout fingerprint | 166 / `05defdbc...` | 166 / **`05defdbc...` identical** |
| `clip_stats` rows | **214,439** | **214,439** |
| **the 14 affected clips: stat rows / series fingerprint** | **626 / `8c14f782a85a7b8a8d1978b96dbf465f`** | **626 / `8c14f782a85a7b8a8d1978b96dbf465f` identical** |

**The one honest difference, and it is not this round.** APPROVED moved 4,429 to 4,432 and the clip money fingerprint changed, because **a human reviewer approved three clips while the round was running**: `cmspvvh9` at `10:56:42.896`, `cmspvvk6` at `10:57:49.251` and `cmspvvmx` at `10:58:07.715`, all by reviewer `cmnd5t`, all clipper submissions with `isOwnerOverride = false` and $0.00 earnings so far. **This round performed zero database writes of any kind** — `run-select.js` refuses a write keyword before connecting, and the only writes anywhere were to git — and **approved earnings, the payout fingerprint, the total stat-row count and the 14 clips' series are all identical across the same window**, which is what a round that wrote nothing looks like.

## GATES AND GUARDS

`npm ci` **exit 0**; `npx prisma generate` **exit 0**, run before tsc because `npm ci` wipes the generated client; `npx tsc --noEmit` **exit 0, 0 errors** against a baseline of 0 on the same tree; `npm run build` written to a log with the exit code echoed by hand and **never piped through `tail`**: **BUILD_EXIT=0** pre-commit and **exit 0** post-commit, "Compiled successfully". **eslint confirmed present** at `node_modules/.bin/eslint`, so the hooks gate is not a silent no-op: `check:prisma-bypass` **0 violations across src/ and scripts/, including its earnings-write check**, `check:removed-fields` **OK across 724 files**, `lint:hooks` **11 problems, 0 errors, 11 warnings** against `--max-warnings 11`, unchanged and at the ceiling.

**Byte-identical by blob OID on `origin/main` and on `checkpoint/BL-785`:** `clip-earnings-writer.ts` `ac5be7de`, `earnings-calc.ts` `797e2098`, `balance.ts` `e887f80a`, `tracking.ts` `83ce4bab`, `clip-earnings-invariant-middleware.ts` `61cef393`, `money-decimal.ts` `ef5cdae7`, `campaign-era.ts` `106e16ad`, `apify.ts` `656bf4c0`, `hikerapi.ts` `852cbaf0`, `clipper-submit-core.ts` `c2d13a00`. **The one intended change is `owner-submit-core.ts` `4cd23e30` to `e6c8de24`.** `apify.ts` byte-equality means **no BL-678 guard was touched** and **no Apify actor was run**.

## WHAT WAS NOT DONE, AND WHAT IS STILL OPEN

**Not done, deliberately:** no repair of the 14 (PART 2); no change to `:320`'s earnings gate, so an owner submit whose fetch fails still auto-approves at $0.00 until the first tracking tick roughly an hour later, which BL-784 measured as recovering on all 14 and which is a product question rather than a defect; `checkpoint/BL-723` not merged; main not touched.

**Still open, carried forward from BL-784 rather than silently dropped:** `src/actions/clips.ts:119` holds the exact pre-BL-605 `views: fetchedStats?.views ?? 0` shape and is **dead code with zero importers**, and the marketplace route writes a hardcoded `views: 0` at `submissions/[id]/post/route.ts:723` but **production holds 0 marketplace clips**. Neither can fabricate anything today; both are landmines if wired up, and neither was touched by this round because neither is the defect it was sent to fix.

**Not provable here:** that the fix behaves correctly against a live failing provider, because that needs a real owner submission against a dead URL, which this round is forbidden to create. The decision is proven by driving the shipped guard over every outcome, which is the same standard BL-746 and BL-748 met.

**Rollback:** `git revert` the fix commit `84a96670`, or `git reset --hard pre-BL-785`. **Nothing to undo in the database**, because the fix writes nothing and repairs nothing.
