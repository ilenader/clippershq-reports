# BL-782 — the Instagram first snapshot is not broken. BL-781 measured a window that straddled the fix.

**2026-08-12 · DB `now()` = `2026-08-12 09:32:48.136198+00` to `09:38:15.687091+00` · NO CODE CHANGED, DELIBERATELY.**
Base `origin/main` @ `72f05cec`, branch `checkpoint/BL-782`. Isolated worktree `C:/bl782`, short path, `node_modules` never junctioned, removed at the end. **Nothing was written to the database, no submission was created, no probe was made, no Apify actor was run, $0.00 spent.** Every read through `scripts/run-select.js`, every timestamp cast `::text` against DB `now()`. Handles redacted; clips appear as 8-character id prefixes only.

## THE HEADLINE

> **There is nothing to fix. BL-746 is working perfectly on every Instagram clip submitted since it deployed: 218 of 218, first snapshot inside the submit transaction, median 0 seconds, none missing. BL-781's 53 minute median is real and is HISTORICAL — 11 of its 14 days sit before the fix went live, and 702 of its 920 Instagram clips are pre-fix. Both reports are correct about different populations.**
>
> **But the round found a different defect, on the one submit path none of the three guards covers: the OWNER submit path writes a fabricated zero. `owner-submit-core.ts:193` initialises views to a literal 0 and `:291` writes a `ClipStat` unconditionally, so a failed provider fetch is stored as a measurement of nothing. Twelve owner-submitted Instagram clips carry exactly that, and all twelve later read four figures or more. It is reported here and NOT fixed, because it is money-adjacent and belongs in its own round.**

## PART 0 — WHY IT LOOKED LIKE 53 MINUTES

**The deploy boundary is `2026-08-09 15:38Z`**, taken from BL-750's own per-clip table (three clips submitted at 14:58, 15:08 and 15:10 got no stat at submit; five from 15:38 onward got one at 23 to 48ms). Every measurement below is split there.

### The reconciliation, last 14 days, every clip, no sampling

| platform | era | clips | no stat ever | within 1 min | within 5 min | within 1 h | median |
|---|---|---|---|---|---|---|---|
| **Instagram** | **pre BL-746** | **702** | **33** | **0** | **0** | 328 | **3,627s** |
| **Instagram** | **post BL-746** | **218** | **0** | **218 (100.0%)** | **218** | **218** | **0s** |
| TikTok | pre | 143 | 1 | 130 | 130 | 131 | 0s |
| TikTok | post | 19 | 1 | 13 | 13 | 13 | 0s |
| YouTube | pre | 35 | 0 | 33 | 33 | 33 | 0s |

**76.3% of BL-781's window was pre-fix, and the pre-fix cohort has a 3,627 second median. That is the entire 53 minutes.** Nothing regressed.

### Per day since the deploy, so the reader can see it did not decay

| day | Instagram clips | no stat | within 1 min | median |
|---|---|---|---|---|
| 2026-08-09 (from 15:38Z) | 26 | 0 | **26** | 0s |
| 2026-08-10 | 95 | 0 | **95** | 0s |
| 2026-08-11 | 80 | 0 | **80** | 0s |
| 2026-08-12 (to 09:38Z) | 17 | 0 | **17** | 0s |

### The three hypotheses, each tested rather than assumed

**1. "The fix covers only ONE submit path."** **FALSE for the two clipper paths, TRUE for the owner path.**
The single route calls `processClipperSubmitLink` at `src/app/api/clips/route.ts:832`; the batch route calls the **same** function at `src/app/api/clips/batch/route.ts:160`. One core, one guard, both paths. Proven live by shape, since a batch submit leaves several clips by one user within seconds of each other:

| shape | clips since deploy | no stat | within 1 min | median delay | worst delay |
|---|---|---|---|---|---|
| burst, the batch signature (2+ by one user inside 10s) | 22 | 0 | **22** | **29ms** | 709ms |
| solo, single submit | 196 | 0 | **196** | **40ms** | 293ms |

The **owner** path is genuinely separate: `owner-submit/route.ts` and `owner-submit-bulk/route.ts` both call `processOwnerSubmitLink` in `src/lib/owner-submit-core.ts`, which never imports `clipper-submit-core`. It is not late, because it writes its stat unconditionally. It is wrong in the other direction, which is PART 1.

**2. "The HikerAPI response often lacks the field, so the `viewSource` guard skips."** **FALSE, and now quantified for the first time.** If the guard fired, the clip would leave the transaction with no stat and wait for the tick. **It fired 0 times in 218 submissions (0.0%).** BL-746 and BL-750 both listed the guard's real-world frequency as unknown; it is now measured at zero over 218 consecutive Instagram submissions.

**3. "The median is historical."** **TRUE, and it is the whole answer**, per the table above.

**THE CAUSE, NAMED: `BL-781` computed a 14 day median over a population that is 76.3% pre-fix. The code at `src/lib/clipper-submit-core.ts:537` (accept the harvested count) and `:661` (write only when non-null) is doing exactly what BL-746 shipped, on every Instagram clip, at a median of 0 seconds.**

## PART 1 — FIX NOTHING, AND REPORT THE DEFECT THAT IS ACTUALLY THERE

**No code was changed. The real diff of this branch is `BACKLOG.md` plus this report, and it is non-empty and contains no source file.** Manufacturing a change to a path measured at 100% and 0ms would be worse than useless.

### The defect that IS there, evidenced, and deliberately left for its own round

```ts
// src/lib/owner-submit-core.ts:193
let fetchedStats = { views: 0, likes: 0, comments: 0, shares: 0 };
...
// :215  console.log(`[OWNER-SUBMIT] Apify returned null for ${clipUrl} ... — starting with 0`);
// :218  console.log(`[OWNER-SUBMIT] Could not fetch stats for ${clipUrl}: ${err?.message} — starting with 0`);
...
// :291  UNCONDITIONAL
await tx.clipStat.create({ data: { clipId: newClip.id, views: fetchedStats.views, ... } });
```

Compare the clipper path, which gates the identical write:

```ts
// src/lib/clipper-submit-core.ts:660-661
const resolvedFirstViews = fetchedStats?.views;
if (resolvedFirstViews != null) { await tx.clipStat.create({ ... }) }
```

**So on a provider failure the clipper path skips and the owner path stores a zero.** That is the exact harm BL-605's skip contract, BL-543's NULL-never-0 rule and BL-748's `viewSource` guard exist to prevent, on the one path none of them reaches.

**Measured, all-time, on the 103 owner-submitted clips:** 35 Instagram, 63 TikTok, 5 YouTube; **12 of the 35 Instagram clips carry a first stat of 0 views, and ALL TWELVE later read 1,000 or more.**

| id8 | clip created | first stat | first views | next stat | next views | max views |
|---|---|---|---|---|---|---|
| `cms240aw` | 2026-07-25 18:05 | 2026-07-26 18:06:20 | **0** | +55.6 min | **118,848** | 122,786 |
| `cmp2hc6g` | 2026-05-07 08:15 | 2026-05-12 10:20:22 | **0** | +192.6 min | 473 | **1,062,360** |
| `cms2c90f` | 2026-07-25 21:56 | 2026-07-26 21:57:03 | **0** | +65.2 min | 1,769 | 180,944 |

**A 24 hour old Instagram reel that reads 118,848 views 56 minutes later did not have 0 views when it was submitted.** The zero is the initialiser at `:193`, stored as though it were a reading.

**Why it is NOT fixed here.** `owner-submit-core.ts` is the auto-approve path: it calls `writeClipEarnings` and computes owner earnings in the same function, gated on `fetchedStats.views > 0` at `:320`. Changing what it writes is a money-adjacent change, and this round's mandate was a measurement. **The route has not been used since `2026-07-26 14:00`, seventeen days ago, so nothing is on fire.** The fix is one gate, mirroring `clipper-submit-core.ts:661`, plus a decision about whether a failed fetch should still auto-approve at $0. **Say the word and it ships as its own round with its own review.**

## PART 2 — EVERY GUARD PROVEN INTACT, ON MAIN, TODAY

Counted with `grep -c`, never piped to `head`:

| guard | site | count |
|---|---|---|
| classifier returns null for a hidden count | `hikerapi.ts` `views: singleProbe?.value ?? null` | **1** |
| the fabricated zero is gone | `views: singleProbe?.value ?? 0` | **0** |
| carousel branch guard | `views: usedKey === null ? null : sum` | **1** |
| tracking's `views <= 0` rejection | `hikerapi.ts` | **3** |
| BL-746 submit guard | `res?.viewSource != null ? num(res.views) : null` | **1** |
| BL-605 null write gate | `if (resolvedFirstViews != null)` | **1** |
| **awaited HikerAPI calls in the submit core** | `await fetchHikerInstagramByUrl(` | **1, unchanged. NO new vendor call by anyone.** |

**Both harnesses re-run on main today**, driving the real exported `classifyV2Media` and gates extracted from the shipped source, with no network call and nothing written:

```
scripts/test-bl-746-first-stat.mjs        48 passed, 0 failed   H746_EXIT=0
scripts/test-bl-748-no-fabricated-zero.mjs 39 passed, 0 failed  H748_EXIT=0
```

**Submit never blocks, throws or slows.** `harvestInstagramRawMeta` (`clipper-submit-core.ts:277-320`) wraps everything in `try/catch`, returns null on any failure, and reads only from a response the path already awaited for BL-682's caption and BL-686's `taken_at`, so **zero latency is added**. The harness proves all eight failure modes end in SKIP with the submission still succeeding: harvest threw, key unconfigured, HTTP 404/429/500, timeout, non-JSON body, media object is a string, `play_count` absent, `play_count` NaN. **Live corroboration: 0 of 218 submissions failed and 0 skipped.**

## PART 3 — WHAT THE LANDED FIX DID TO THE SIGNAL

BL-775 measured the arrival curve separating best on Instagram, **66.4% of views by 6 hours for approved clips against 7.8% for bought-view rejections**. The curve is read from the stored snapshot series, so the value of a first snapshot at T+0 is that the series has a measured origin instead of an assumed one.

| Instagram, last 14 days | pre BL-746 | post BL-746 |
|---|---|---|
| clips | 702 | 218 |
| **blind for the whole first hour (no snapshot)** | **374 (53.3%)** | **0 (0.0%)** |
| **REVIEWED inside that first hour with nothing to read** | **168** | **0** |
| clips with no snapshot at all | 33 | **0** |
| mean snapshots inside the first 6 hours (clips 24h+ old) | 4.07 | **4.80** |
| share with 3+ snapshots by 6 hours (clips 24h+ old) | 92.9% | 89.4% |

**The honest reading, including the row that does not flatter the fix.** More than half of Instagram clips used to have no measurement whatsoever during their first hour, and **168 of them were reviewed in that window with a blank where the curve should be**. That is now zero. But the **3-or-more-snapshots-by-6-hours rate did not rise** — 89.4% post against 92.9% pre — because that rate is set by the tracking ladder, not by the submit write. **This round does not attribute that difference to anything; it is stated because a report that only prints its improvements is not a measurement.**

**The 6 hour reading itself is not made more accurate by this fix**, because the 6 hour snapshot was already being taken by the hourly tick. What changes is the **start** of the curve: a clip's first hour is now measured rather than absent, and a reviewer opening a clip in its first hour sees a real number instead of nothing.

**HISTORICAL CURVES ARE UNTOUCHED.** Nothing was recomputed, backfilled, migrated or rewritten. This round wrote **nothing** to the database. The 33 pre-fix Instagram clips with no snapshot still have none, and their curve stays suppressed by BL-776's 3-snapshot rule, which is the honest empty state working as designed rather than a gap to paper over.

## PART 4 — THE EVIDENCE

**Per path, since the deploy.** Single: 196 clips, all within a minute, median **40ms**, worst 293ms. Batch: 22 clips, all within a minute, median **29ms**, worst 709ms. **Owner: no owner clip has been submitted for 17 days**, so no post-deploy owner evidence exists; its behaviour is established structurally at `owner-submit-core.ts:291` and historically by the 12 fabricated zeros above.

**Id-matched, from BL-750's own post-deploy table and reproduced by today's per-day counts:** `cmslyvoxi` 45ms, `cmslyyvq6` 40ms, `cmslz2ytj` 29ms, `cmsm019q5` 23ms, `cmsm0733a` 48ms. Every Instagram clip since has matched that shape.

**An unreadable post still SKIPS rather than writing 0:** proven by the two harnesses today (`VIDEO WITH HIDDEN COUNT -> SKIPS`, `mixed carousel with no readable child count -> SKIPS`, `NaN -> SKIPS`, each additionally asserting `views !== 0`), and by the structural fact that `fetchedStats` stays null so `:661` never fires.

**TikTok and YouTube unaffected, stated honestly rather than flattered.** Both sit at a **median of 0s** on both sides of the boundary. TikTok is not perfect and never was: **36 of 42 within a minute over 7 days, 1 with no stat**, the same pattern pre-fix (130 of 143). YouTube 33 of 35, median 0s. **No Instagram code path can reach either**: the branch is `if (platform === "instagram" && fetchedRawMeta == null)`, and `apify.ts` and `hikerapi.ts` are byte-identical by blob OID.

**No stored views moved down because of this round, because this round wrote nothing.** In the last 24 hours **4 of 3,164** stat rows moved down, all Instagram, all written by the ordinary `:01` tracking tick, **none to zero**: `cmsorzaa` 592 to 393, `cmsoj2mh` 4,734 to 4,719 and 5,085 to 5,070, `cmsmn8es` 384 to 381. **Earnings invariant: 0 violations.** No clip status, earnings or payout changed.

**Re-measured median per path, before and after:** Instagram single and batch **3,627s to 0s**; TikTok **0s to 0s**; YouTube **0s to 0s**; owner path unchanged and unused.

## GATES, HONESTLY

`npm ci` **exit 0**; `npx prisma generate` **exit 0**, run before tsc because `npm ci` wipes the generated client; `npx tsc --noEmit` **exit 0, 0 errors**; `npm run build` written to a log with the exit code echoed by hand and **never piped through `tail`**: **BUILD_EXIT=0**, "Compiled successfully in 44s". **eslint confirmed present** at `node_modules/.bin/eslint`, so the hooks gate is not a silent no-op: `check:prisma-bypass` **0 violations**, `check:removed-fields` **OK across 724 files**, `lint:hooks` **11 problems, 0 errors, 11 warnings** against `--max-warnings 11`, unchanged and at the ceiling. **A document cannot change tsc or a build, and both were run anyway, on a real `npm ci` in the worktree, so the claim is measured rather than assumed.**

**Byte-identical by blob OID on `main` and on `checkpoint/BL-782`:** `clip-earnings-writer.ts` `ac5be7de`, `earnings-calc.ts` `797e2098`, `balance.ts` `e887f80a`, `tracking.ts` `83ce4bab`, `clip-earnings-invariant-middleware.ts` `61cef393`, `money-decimal.ts` `ef5cdae7`, `campaign-era.ts` `106e16ad`, `apify.ts` `656bf4c0`, `hikerapi.ts` `852cbaf0`, `clipper-submit-core.ts` `c2d13a00`, `owner-submit-core.ts` `4cd23e30`. **No source file was changed at all.** `apify.ts` byte-equality means no BL-678 guard was touched (it carries the same 8 `BL-678` comment lines on both refs; the blob equality is the stronger proof), and **no Apify actor was run**.

## SAFETY AND WHAT COULD NOT BE ESTABLISHED

**No new vendor call was added, because no code was added.** The submit core still holds exactly **one** awaited HikerAPI call. **No probe was made this round and $0.00 was spent**, so the one-call-per-profile rule was not approached; nothing was submitted for testing and no clip was created. BL-605's skip contract, BL-543's NULL-never-0 rule and BL-748's `viewSource` guard are all proven present by count and by two harnesses. Historical curves are untouched. TikTok and YouTube are proven unaffected. No clipper's earnings changed. No schema change and no `prisma migrate`. The worktree is removed. No dashes as bullets.

**Not established:** whether the `viewSource` skip guard ever fires in production, since it has now gone 218 consecutive Instagram submissions without firing — 0.0% is a measurement of this window, not a proof that Instagram never hides a count. **Why 89.4% of post-fix Instagram clips reach 3 snapshots by 6 hours against 92.9% before** — the ladder, not the submit write, sets that, and this round did not investigate it. **Whether the owner path's 12 fabricated zeros cost anyone money** — they did not move any stored view count down and the tick recovered every one within roughly an hour, but the clips were auto-approved at $0 earnings in the interval, and this round did not trace the earnings recomputation for each of the twelve. **Whether TikTok's 6-in-42 late first stats have a single cause** — its median is 0s and the pattern predates every Instagram change, so it was measured and left alone.

**Rollback:** `git revert` this commit. It contains two documents and no code, so there is nothing in the database or the running system to undo.
