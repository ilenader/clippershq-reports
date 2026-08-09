# BL-746 — Instagram gets its first view count at submit, from a response the platform already paid for

**2026-08-09 · Base:** `main @ b5bd0651` · **Branch:** `checkpoint/BL-746` `053309f4` · **Tags:** `pre-BL-746` = `b5bd0651`, `post-BL-746` = `053309f4`
**No new vendor call. No Apify actor run. `apify.ts` and `hikerapi.ts` BYTE-IDENTICAL by blob OID, so no BL-678 guard was touched. No clip status or earnings changed, no payout touched, no schema change, no `prisma migrate`. Handles redacted; every timestamp cast `::text` against DB `now()`.**

---

## THE HEADLINE

**The count was never missing. It was being discarded.** `harvestInstagramRawMeta` already called
`fetchHikerInstagramByUrl` on every Instagram submit, for BL-682's caption and BL-686's `taken_at`, and
returned only `media`, throwing away the `views`, `likes` and `comments` the **same** `HikerResult` carried.

**One source file changed. 94 insertions, 80 of them comments. Zero new vendor calls.**

**And proving it surfaced a real defect that this very change would have made load-bearing** (PART 1.3).

---

# PART 0 — THE FIELD, CONFIRMED LIVE RATHER THAN INHERITED

BL-745 disclosed that its **first four probes printed nulls because it read the wrong field shape**, so no
field path was inherited here. Two live probes against real Instagram reels, through the **same function the
submit path calls**.

**Disclosed cost: 2 HikerAPI calls, $0.002. No Apify actor. Nothing written.**

```
── https://www.instagram.com/reel/Db0kb5Uzah1/
   httpStatus      : 200        error: none
   RESOLVED views  : 160        (typeof number)
   viewSource      : "play_count"
   classification  : "reel"     likes/comments: 2 / 0
   candidateFields : {"play_count":160,"ig_play_count":160,"content_views_count":null}
   RAW view keys present on media_or_ad: {"play_count":160,"ig_play_count":160}
   media_type      : 2          taken_at: 1786282909      latencyMs: 1387

── https://www.instagram.com/reel/Db0juF7JzJN/
   httpStatus      : 200        error: none
   RESOLVED views  : 166        (typeof number)
   viewSource      : "play_count"
   classification  : "reel"     likes/comments: 5 / 0
   candidateFields : {"play_count":166,"ig_play_count":166,"content_views_count":null}
   RAW view keys present on media_or_ad: {"play_count":166,"ig_play_count":166}
   media_type      : 2          taken_at: 1786282541      latencyMs: 688
```

## 0.1 The key path, stated explicitly

**`rawBody.media_or_ad.play_count`**, surfaced as **`HikerResult.views`** by `classifyV2Media`, with
`HikerResult.viewSource` naming the winning key. `ig_play_count` carries the same value and
`content_views_count` is null on both. The probe order is `VIEW_FIELDS` at `hikerapi.ts:457`:
`play_count`, `ig_play_count`, `view_count`, `fbid_view_count`, `video_view_count`.

**The first probed clip had been submitted 81 seconds earlier and still had zero stored stats.** That single
row is the whole defect: the count was available and nothing read it.

## 0.2 The response IS already in hand. No second call.

`clipper-submit-core.ts:486` calls `harvestInstagramRawMeta`, which at `:281` calls
`fetchHikerInstagramByUrl` **once**, for every Instagram submit, and has done since BL-682. `grep` over the
shipped file counts **exactly one awaited call**, unchanged by this round.

**So the cost of reading the count is genuinely zero.** This is the same precedent BL-686 recorded three
lines above at `:470-474`: *"BL-682 already harvests the HikerAPI media object on this exact path ... this
adds ZERO new vendor calls."*

---

# PART 0.5 — THE MEASUREMENT, RECONCILED WITH BL-745 RATHER THAN REPEATED

A naive 30-day window **straddles** the 2026-07-22 11:12Z cutover and reads a misleading 20.8% for
Instagram. Split at the cutover, BL-745's finding is confirmed exactly and the switch is unmistakable:

| slice | clips | within 1 min | median s | zero-stat |
|---|---|---|---|---|
| **Instagram, post-cutover** | **851** | **0 (0.0%)** | **3,659** | 57 |
| **Instagram, pre-cutover** | 1,661 | **1,636 (98.5%)** | **0** | 0 |
| TikTok, post-cutover | 198 | 178 | **0** | 1 |
| TikTok, pre-cutover | 1,053 | 994 | **0** | 0 |
| YouTube, post-cutover | 73 | 58 | **0** | 0 |
| YouTube, pre-cutover | 1,322 | 1,317 | **0** | 0 |

`db_now = 2026-08-09 13:49:39.937371+00`

**Instagram went 98.5% to 0.0% across the cutover while TikTok and YouTube held at a median of 0s on both
sides.** A switch, not a slope, exactly as BL-745 said.

---

# PART 1 — THE FIX

## 1.1 The full diff, executable lines

```diff
-async function harvestInstagramRawMeta(clipUrl: string): Promise<any | null> {
+async function harvestInstagramRawMeta(clipUrl: string): Promise<
+  { media: any; views: number | null; likes: number | null; comments: number | null } | null
+> {
   try {
     const { fetchHikerInstagramByUrl, isHikerConfigured } = await import("@/lib/scraper-providers/hikerapi");
     if (!isHikerConfigured()) return null;
     const res: any = await fetchHikerInstagramByUrl(clipUrl);
     const body = res?.rawBody;
     if (!body || typeof body !== "object") return null;
     const media = body.media_or_ad ?? body.media ?? body.data ?? null;
     if (!media || typeof media !== "object") return null;
-    return media;
+    const num = (v: any): number | null =>
+      typeof v === "number" && Number.isFinite(v) ? v : null;
+    const viewsUsable = res?.viewSource != null ? num(res.views) : null;
+    return { media, views: viewsUsable, likes: num(res.likes), comments: num(res.comments) };
   } catch (err: any) {
     console.warn(`[BL-682] instagram raw-meta harvest skipped (fail-open): ${err?.message ?? err}`);
     return null;
   }
 }
```

```diff
       if (platform === "instagram" && fetchedRawMeta == null) {
-        fetchedRawMeta = await harvestInstagramRawMeta(clipUrl);
+        const harvested = await harvestInstagramRawMeta(clipUrl);
+        fetchedRawMeta = harvested?.media ?? null;
+        if (fetchedStats == null && harvested && typeof harvested.views === "number") {
+          fetchedStats = {
+            views: harvested.views,
+            likes: harvested.likes ?? 0,
+            comments: harvested.comments ?? 0,
+            shares: 0,
+          };
+          console.log(`[BL-746] instagram first-stat from harvest: views=${harvested.views} ...`);
+        }
       }
```

The existing write at `:569-579` then fires unchanged, still guarded by `if (resolvedFirstViews != null)`.
**80 of the 94 added lines are the explanatory comments; the executable change is the 14 lines above.**

## 1.2 What happens for a post with no readable count

**The snapshot is SKIPPED. Nothing is written. BL-605's contract is untouched.**

The guard is `typeof harvested.views === "number"`. A null, an absent field, a hidden count, a string that
does not coerce, a NaN, a provider error or a thrown exception all leave `harvested.views` null, so
`fetchedStats` stays null, so `resolvedFirstViews` is null, so the `ClipStat` row is never created. **A
fabricated 0 is structurally unreachable**, which matters because `ClipStat.views` is a non-nullable `Int`
and a 0 would zero a clipper's views and freeze earnings (BL-543).

**A legitimate numeric `0`, from a post that genuinely has no plays yet, IS written.** That is correct and
is the same rule TikTok and YouTube already follow.

## 1.3 A REAL DEFECT FOUND WHILE PROVING THIS, WHICH THIS CHANGE WOULD HAVE MADE LOAD-BEARING

**`hikerapi.ts:603`:**

```ts
views: singleProbe?.value ?? 0,
```

For a `media_type: 2` post whose play count Instagram **hides**, `singleProbe` is null and this returns a
hard **`0`** with `viewSource: null`.

**The CAROUSEL branch guards exactly this case and the SINGLE-VIDEO branch does not.** At `:576-583` the
carousel path returns `usedKey === null ? null : sum` with an explicit comment that returning 0 *"would zero
a clipper's views"*. The single-video path has no such guard. **BL-604 documented Instagram hiding a feed
video's view count**, so this is reachable, not theoretical.

**That 0 was harmless while nothing consumed it at submit. This round would have written it to `ClipStat`**,
producing precisely the harm BL-543 and BL-605 exist to prevent, on the first post that hit it.

**Closed by requiring `viewSource != null`** before accepting any count. `viewSource` is null in exactly the
no-key-was-read case and non-null whenever a real field produced the number, so the requirement converts the
fabricated 0 back into an honest "unknown".

**Deliberately fixed at the call site and NOT in `hikerapi.ts`.** That classifier is shared with the tracking
poll, and changing its return would move tracking behaviour for every platform, which a submit-path round
must not do. **The `hikerapi.ts:603` defect is reported, not repaired, and wants its own round.**

---

# PART 2 — FAIL OPEN, ALWAYS

**The failure behaviour is unchanged because the call and its catch are unchanged.** The harvest already
wrapped everything in `try/catch`, already warned and already returned null. Nothing new is awaited, and
every field read is on an object already proven to exist.

Proven case by case in the harness:

| Failure | Result |
|---|---|
| Harvest threw and was caught | **SKIPS**, submission succeeds, no stat |
| `HIKERAPI_KEY` not configured | **SKIPS**, submission succeeds |
| HTTP 404, 429 or 500 | **SKIPS**, submission succeeds |
| Timeout | **SKIPS**, submission succeeds |
| Body is not JSON | **SKIPS**, submission succeeds |
| Body is JSON but the media object is a string | **SKIPS** |
| `play_count` missing entirely | **SKIPS** |
| `play_count` is NaN | **SKIPS** (also unreachable: `JSON.parse` rejects `NaN`) |

**It cannot noticeably slow the submit either**, because the call it reads from was already being awaited on
this exact path. The probes measured **688ms and 1,387ms** for that already-existing call; this round adds
**zero** additional latency.

---

# PART 3 — THE BATCH CASE

**No per-row call is added, because the existing HikerAPI call is already per row.** `grep` over the shipped
file confirms **exactly ONE awaited `fetchHikerInstagramByUrl`**, unchanged.

**Rate-limit position for a 10-row batch: identical to today.** Those 10 calls already fire. No new limit is
approached that is not approached already.

**Partial failure degrades per clip, never per batch.** Each row's harvest is independent and fails open on
its own, so rows that resolve get a first stat and rows that do not get none, exactly as a mixed batch
behaves today. **No clip can be silently lost or duplicated**, because nothing about the transaction, the
dedupe, or BL-601's path was touched: the change sits entirely inside the pre-transaction metadata harvest.

---

# PART 4 — THE EXISTING ZERO-STAT CLIPS

**They do NOT recover from this fix, and they are NOT recovering on their own. A backfill is required.**

**Why this fix cannot help them:** it is on the **submit** path. These clips have already been submitted.

**Why the tick is not helping either, which BL-745 did not establish.** Every one of them carries
`cadenceReason = INFRA_DEFER`, with `checkIntervalMin` backed off to **360 or 2880 minutes** and
`lastFailedAt` set. Sampled live:

```
clip           interval  fails  cadenceReason  lastFailedAt                  nextCheckAt
cms5yt6ty...     360       0    INFRA_DEFER    2026-07-31 10:11:06.163       2026-08-09 16:00:00
cms6k1o4i...     360       0    INFRA_DEFER    2026-07-31 19:32:53.548       2026-08-11 13:00:00
cmsg1xq1p...    2880       0    INFRA_DEFER    2026-08-07 11:01:29.221       2026-08-11 11:00:00
```

**The tick has been failing on them for over a week and has backed itself off to two-day intervals.**

**The population churns, so a single number is misleading.** Instagram clips with zero `clip_stats`:
**57** at `13:50:36`, **42** at `14:18:54`, against BL-745's **41**. At the 13:50 reading the 57 were
**28 APPROVED, 2 PENDING, 27 REJECTED, 9 retired**, carrying **$0.00 of earnings between them**, so no money
is at stake. TikTok has exactly 1.

**NO BACKFILL WAS RUN.** Spec, for its own round:

1. Select Instagram clips with zero `clip_stats`, `isDeleted = false`, `status = APPROVED`, `videoUnavailable = false`. That is the ~28 that matter; rejected and retired clips need nothing.
2. One `fetchHikerInstagramByUrl` per clip, disclosed, at roughly $0.001 each.
3. Write a first `ClipStat` **only** when `viewSource != null` **and** views is a finite number, the same gate this round ships. Never write 0.
4. **Skip anything returning 404 or `MediaNotFound`**, which is BL-720's gone-post signal, and do not let a missing post look like a zero.
5. Write **no earnings**. Let the next tracking tick do that through the normal path.
6. Reset `cadenceReason` and `checkIntervalMin` on the clips that resolve, or they stay on the 2,880 minute ladder.

---

# PART 5 — THE EVIDENCE

## 5.1 A real Instagram clip gets a real count, traced without creating a submission

The two probed clips are **live rows with zero stored stats**. The probe drove the real provider function
and returned **160** and **166** views with `viewSource: "play_count"` (PART 0). Feeding that exact response
shape through the shipped guard writes a `ClipStat` of 160 views, 2 likes, 0 comments.

**No submission was created.** Confirmed after the fact: both probed clips still hold **0** `clip_stats`
rows at `db_now = 2026-08-09 14:18:54.137139+00`, so the probes wrote nothing.

## 5.2 An unreadable post still SKIPS rather than writing 0

`scripts/test-bl-746-first-stat.mjs`, driving the **real exported `classifyV2Media`** and the guard
**extracted from the shipped source**. **48 passed, 0 failed, exit 0.**

```
real reel (live shape)                     views 160   -> WRITES
real reel, genuine 0 play_count            views 0     -> WRITES   (correct, a real zero)
image-only carousel                        views null  -> SKIPS    (never 0)
mixed carousel, no readable child count    views null  -> SKIPS    (never 0)   the BL-604 case
mixed carousel with counts                 views 140   -> WRITES   (summed)
empty body / null body                     views null  -> SKIPS    (never 0)
numeric string "160"                       views 160   -> WRITES   (legitimate coercion)
VIDEO WITH HIDDEN COUNT                    views null  -> SKIPS    (never 0)   closes hikerapi.ts:603
NaN play_count                             views null  -> SKIPS    (never 0)
media object is a string                   views null  -> SKIPS    (never 0)
```

Every SKIP case additionally asserts `views !== 0`, so a fabricated zero is proven impossible, not assumed.

## 5.3 TikTok and YouTube unaffected

**Structurally**: the branch is `if (platform === "instagram" && fetchedRawMeta == null)`. Neither platform
can enter it. **And even inside it**, the write is gated on `fetchedStats == null`, so a resolved stats path
always wins and the harvest can never override it (asserted: a harvest of 999 views against an existing
`fetchedStats` of 123 does not write).

**Measured**: TikTok and YouTube both sit at a **median of 0 seconds** to first stat on **both sides** of the
cutover (PART 0.5). Nothing in this diff touches their path, and `apify.ts` is byte-identical.

## 5.4 No stored views moved down, no earnings changed

**Nothing was written at all.** This round created no `ClipStat`, no clip, no submission and no earning. The
only writes anywhere were to git. Total `clip_stats` rows **205,445** and approved earnings **$11,989.84** at
`14:18:54`, read after all probing.

**No existing clip's stored views can move down by construction**: the change only ever **creates** a first
snapshot for a clip that has none, and only inside the submit transaction for a brand-new clip.

## 5.5 Submit still succeeds when the provider fails

PART 2's table, all eight failure modes proven in the harness.

## 5.6 Byte-identity

```
IDENTICAL  clip-earnings-writer   earnings-calc   balance   tracking
IDENTICAL  clip-earnings-invariant-middleware   money-decimal   campaign-era
IDENTICAL  apify.ts               hikerapi.ts
```

**`apify.ts` byte-identical means no BL-678 guard was touched**, and the harness separately asserts the
harvest function body **references no Apify path at all**. **No Apify actor was run.**

## 5.7 Gates, stated honestly

* `npm ci` **exit 0**, `npx prisma generate` **exit 0**, run after it because `npm ci` wipes the client. Clean worktree at `C:/b746`, short path, `.env`/`.env.local` copied, **no `node_modules` junction**.
* `tsc --noEmit` **exit 0, 0 errors** (log 0 lines).
* `npm run build` **exit 0 pre-commit and exit 0 post-commit**, `✓ Compiled successfully`, read from a log with the exit code **echoed, never piped through `tail`**.
* Hooks gate **11 problems, 0 errors, 11 warnings, at the limit of 11**, **eslint v9.39.4 confirmed present**.
* Harness **48/0, exit 0**.
* Push **verified**: `safe-push.mjs` `VERIFIED PUSHED`, `git ls-remote` agrees, `pre-BL-746` on the true base `b5bd0651` (equals `HEAD~1`).
* **`C:/b575` left exactly as found**: `91b84410`, 77 dirty paths, re-checked after the push. It was stale and dirty, so a separate clean worktree was used.

## 5.8 No UI change, confirmed rather than assumed

The accessibility review found `ClipCardNew.tsx:195` already renders
`stat ? formatNumber(stat.views) : "0"` and simply takes the truthy path, and that
`likes`/`comments`/`shares` are non-nullable `Int @default(0)` so a views-carrying snapshot cannot produce
`null` or `NaN` in those cells.

**It also found the current state is worse than I had assumed.** A clip with no snapshot renders a **hard
literal `0`**, not a dash or a skeleton, so an Instagram clipper **cannot distinguish "we have not measured
yet" from "nobody watched your video"**. The identical glyph is emitted for both, for up to an hour, while
TikTok and YouTube show the truth within a second in identical chrome. **No clipper-facing copy promises a
delay**; several already promise immediacy (`SubmitClipPremium.tsx:352`, `clips/page.tsx:254`).

Its one second-order note was actioned: carrying `likes` and `comments` from the same response, rather than
views alone, avoids diluting the `accounts/page.tsx:199-213` health ratio that a views-only snapshot would
have skewed.

---

# WHAT SHIPPED

`src/lib/clipper-submit-core.ts` only, plus `scripts/test-bl-746-first-stat.mjs` and
`scripts/bl746-probe.mjs` and the `BACKLOG.md` entry. **4 files, 433 insertions, 3 deletions**; the
executable source change is **14 lines**.

**Rollback:** `git revert -m 1 <merge>`, or `git reset --hard pre-BL-746`. **Nothing to undo in the
database.**

**Not merged to main.** This is a branch round; the merge is its own step.

---

# WHAT COULD NOT BE MEASURED

* **Whether the provider has indexed a post at the exact instant of submission.** The nearest evidence is the probed clip that was **81 seconds** old and returned 160 views. Proving T+0 would require creating a real submission, which this round forbids.
* **Whether `within_1_min` for Instagram actually moves off 0 in production.** That needs real submissions after this merges, and is the single number to re-measure next.
* **How often `hikerapi.ts:603`'s hidden-count case actually fires.** It is now safely skipped, but its frequency is unknown and would need a sample of live video posts to establish.
