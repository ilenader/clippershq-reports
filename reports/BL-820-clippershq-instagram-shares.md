# BL-820 — Instagram was sending the share count all along, and one column now stops a zero pretending to be a measurement

**2026-08-23 · DB `now()` = `2026-08-23 20:50:00.876918+00` (first read) to `21:18:36.682372+00` (last) · BUILD AND MERGE.**
Base `origin/main` @ `a457637f`. Branch `checkpoint/BL-820` @ `d1c6aa64`. **Merged to main and verified pushed: `origin/main == local == b9a288cc`.** Tags `pre-BL-820` (`a457637f`), `post-BL-820` (`d1c6aa64`), `pre-BL-820-merge` (`a457637f`) and `post-BL-820-merge` (`b9a288cc`), all four confirmed on origin by `git ls-remote`. Isolated worktree `C:/w820`, a short path, `node_modules` never junctioned, removed at the end. Every database read through `scripts/run-select.js`; every timestamp cast `::text` against DB `now()`. Handles redacted. **No Apify actor ran and none can:** `APIFY_HARD_OFF` is a `const true`, and `apify.ts` carries the same 8 `BL-678` guard comments on both refs.

**A REDEPLOY ON RAILWAY IS REQUIRED BEFORE ANY OF THIS IS LIVE.**

> **Instagram returns `reshare_count` on every post probed and the client never looked. It is read now.** Six live posts, id-matched, before a line was written: **86,676 / 5,769 / 143 / 67 / 5**, all at the same nesting, all stored as `0`.
>
> **THREE Instagram loss points, not one.** BL-819 named the classifier and the overlay. A third was found here at `apify.ts:1607`, hardcoding `0` a **second** time while folding the overlay result into the batch map, **and that is the path that actually runs the tick**. Fixing only the classifier would have changed nothing.
>
> **The accessibility review caught a CORRECTNESS bug this round would have introduced**, not a styling one: a measured 86,676 followed by one unmeasured tick would have tripped `fraud.ts` rule #9 and **accused a real person of buying engagement because we failed to read a number**.

---

## PART 0 — THE FIELD, CONFIRMED ON A REAL RESPONSE

BL-746 disclosed that its own first four probes **on this same client** read the wrong field shape and returned nulls until corrected, and BL-686 caught this very file asserting a field was absent when it was present. **So nothing was inherited.** Six posts, through the real `fetchHikerInstagramByUrl`, captured in ONE run.

**Disclosed: 6 HikerAPI calls, roughly $0.006. No Apify actor. Nothing written.**

| clip | url shape | requested | returned | **id match** | `media_type` | `product_type` | **`reshare_count`** | `media_repost_count` | `share_count_disabled` |
|---|---|---|---|---|---|---|---|---|---|
| `cmt095se` | `/reel/` | `DcOg6OvoshY` | `DcOg6OvoshY` | **true** | 2 | clips | **86,676** | 1,738 | **false** |
| `cmsvqt6l` | `/reel/` | `DcGZEHko23J` | `DcGZEHko23J` | **true** | 2 | clips | **5,769** | 87 | **false** |
| `cmsz9mgt` | `/p/` | `DcMvGmlRZAS` | `DcMvGmlRZAS` | **true** | 2 | clips | **67** | 5 | **false** |
| `cmt58611` | `/p/` | `DcXeJuttQv2` | `DcXeJuttQv2` | **true** | 2 | clips | **143** | *absent* | **false** |
| `cmt22y0u` | `/p/` | `DcRyEHFRTdm` | `DcRyEHFRTdm` | **true** | 2 | clips | **5** | *absent* | **false** |
| **`cmt60k1v`** | `/p/` | `DcY4Xx8g1hS` | `DcY4Xx8g1hS` | **true** | 2 | clips | ***absent*** | *absent* | **false** |

### The three answers the brief asked for

**1. The key path is `media_or_ad.reshare_count`, TOP LEVEL, on every media type tried.** A recursive scan of the media object (484 to 576 keys) for anything naming a share returns eleven hits per post and only two are counts. `share_count`, `shares`, `reshare`, `repost_count` and `forward_count` are all `undefined`, which is presumably how the original "IG has no share-count concept" assertion was reached: **the field exists under a name nobody probed.**

**2. `media_repost_count` is NOT an alias and is deliberately NOT a fallback.** It is a different, smaller number (1,738 against 86,676 on the same post, a factor of 50) and it was **absent on two posts where `reshare_count` was present**. Falling back to it would silently substitute one metric for another, which is worse than reporting nothing.

**3. Nesting did not vary.** All six resolved to `media_type: 2, product_type: clips` regardless of whether the URL was `/reel/` or `/p/`, so the URL shape says nothing about the media type and the key sits in the same place either way. **No carousel appeared in the sample**, so the carousel nesting is untested and that limitation is stated rather than papered over.

### The case that decided the design

**`cmt60k1v` returned NO `reshare_count` at all, with `share_count_disabled: false`.** A low-engagement post, 209 views and 0 likes, where the field is simply not present and sharing is not disabled. **That single post proves the absent case is reachable rather than theoretical**, which is exactly what BL-748 and BL-753 needed and did not have when they fixed the same shape of defect for views.

**`share_count_disabled: true` was never observed.** It was `false` on 6 of 6, so the creator-hidden case is handled in code and **not proven live**. Stated plainly: it is written because the alternative is recording a hidden count as a measured zero, not because I saw one.

---

## PART 1 — THE FIX

### The storage problem, and the column that solves it

`ClipStat.shares` is `Int NOT NULL DEFAULT 0`. **There is no third state.** Before this round an absent share count and a genuinely unshared clip were the same stored byte on every platform, which is precisely why BL-819 could measure Instagram at zero across 142,179 snapshots without anybody noticing.

**One additive nullable column**, applied with `run-schema-sql.js` and `npx prisma generate`, **never `prisma migrate`**:

```sql
ALTER TABLE "clip_stats" ADD COLUMN IF NOT EXISTS "sharesSource" TEXT;
```

Read back from `information_schema`: `sharesSource | text | is_nullable YES | default null`. **All 267,099 existing rows take NULL**, which is the correct and honest label: no provider ever wrote them.

**Why not widen `shares` itself.** It is read by the fraud engine, eight display surfaces, the CSV export and the analytics chart. Making it nullable is an `ALTER COLUMN` on a 267k-row hot table and breaks every one of those readers. This is the `viewSource` pattern BL-748 used to separate an unknown view count from a real zero, applied to the one metric that still could not tell them apart, **without touching the value column at all.**

### Exactly what is stored, in each case

| case | `shares` | `sharesSource` | meaning |
|---|---|---|---|
| Instagram returned a count | the count | **`"reshare_count"`** | **MEASURED** |
| TikTok returned a count | the count | **`"shareCount"`** | **MEASURED** |
| the field is present and reads 0 | `0` | the key name | **MEASURED ZERO** |
| the provider omitted the key | `0` | **NULL** | **ABSENT** |
| `share_count_disabled` is true | `0` | **NULL** | **ABSENT** |
| YouTube, any snapshot | `0` | **NULL** | **ABSENT, permanently** |
| the owner types one by hand | the typed value | **`"manual"`** | **MEASURED** |

**The `?? 0` that remains is not a fabrication**, and this is the load-bearing point: the column is non-nullable so *something* must be written, and `sharesSource` is what carries the meaning. Every reader tests the source, never the value. A measured zero and an absent one are different rows.

### The three Instagram loss points

```diff
  // 1. src/lib/scraper-providers/hikerapi.ts — the classifier never looked
   const likes = numericOrUndef(media.like_count ?? media.likes_count ?? media.likes);
   const comments = numericOrUndef(media.comment_count ?? media.comments_count ?? media.comments);
+  const shareCountDisabled = media.share_count_disabled === true;
+  const sharesRaw = shareCountDisabled ? undefined : numericOrUndef(media.reshare_count);
+  const shares = sharesRaw;
+  const sharesSource = sharesRaw == null ? null : "reshare_count";
```

```diff
  // 2. the same file, the overlay the tick reads — a hardcoded 0 under a false comment
-      // shares: IG has no share-count concept on v2.
-      shares: 0,
+      shares: typeof res.shares === "number" && Number.isFinite(res.shares) && res.shares >= 0 ? res.shares : 0,
+      sharesSource: res.sharesSource ?? null,
```

```diff
  // 3. src/lib/apify.ts:1607 — THE ONE THAT ACTUALLY RUNS, and BL-819 did not find it
         primaryMap.set(normalizeUrlForMatch(u), {
           views: sr.stats.views,
           likes: sr.stats.likes,
           comments: sr.stats.comments,
-          shares: 0,
+          shares: sr.stats.shares ?? 0,
+          sharesSource: sr.stats.sharesSource ?? null,
         });
```

**The third is the one that mattered.** The batch path writes 34,234 Instagram snapshots a week; fixing the classifier and the overlay alone would have left the number discarded one line later.

`shares` and `sharesSource` are carried out of all four `classifyV2Media` return branches, and `HikerResult.shares` (declared at `:71` and never assigned since the file was written) is finally populated.

### The write path, and TikTok

```diff
  // src/lib/scraper-providers/lamatok.ts, both readers — value unchanged, label new
-  const shares = pickNumber([stat?.share_count, stat?.shareCount]) ?? 0;
+  const sharesRaw = pickNumber([stat?.share_count, stat?.shareCount]);
+  const shares = sharesRaw ?? 0;
+  const sharesSource = sharesRaw == null ? null : (stat?.share_count != null ? "share_count" : "shareCount");
```

```diff
  // src/lib/clipper-submit-core.ts — BL-746's harvest already had it and threw it away
           fetchedStats = {
             views: harvested.views,
             likes: harvested.likes ?? 0,
             comments: harvested.comments ?? 0,
-            shares: 0,
+            shares: harvested.shares ?? 0,
+            sharesSource: harvested.sharesSource ?? null,
           };
```

**Zero new vendor calls**, for exactly the reason BL-746 gave: the response was already in hand and the field was being discarded. `owner-submit-core.ts:193`, `api/clips/[id]/override/route.ts:175` and `api/clips/[id]/tracking/route.ts:125` are wired the same way.

### tracking.ts IS in the diff, and here is every executable line of it

**It had to be.** `ClipStat.sharesSource` is a new per-snapshot fact and **the ClipStat write lives in this file**. There is no interception point between the provider and the create, so recording it anywhere else would mean inventing a second write path to the same row.

```diff
-  prefetchedStats?: { views: number; likes: number; comments: number; shares: number } | null,
+  prefetchedStats?: { views: number; likes: number; comments: number; shares: number; sharesSource?: string | null } | null,

-    let globalStats: Map<string, { views: number; likes: number; comments: number; shares: number } | null> | null = null;
+    let globalStats: Map<string, { views: number; likes: number; comments: number; shares: number; sharesSource?: string | null } | null> | null = null;

-          let prefetchedStats = new Map<string, { views: number; likes: number; comments: number; shares: number } | null>();
+          let prefetchedStats = new Map<string, { views: number; likes: number; comments: number; shares: number; sharesSource?: string | null } | null>();

-        select: { views: true, likes: true, comments: true, shares: true },
+        select: { views: true, likes: true, comments: true, shares: true, sharesSource: true },

+          sharesSource: stats.sharesSource ?? null,      // the manual write
+            sharesSource: stats.sharesSource ?? null,    // the cron write
```

**Six lines. Every one additive. Not one touches money.** `sharesSource` is a nullable string that no earnings expression reads: earnings are `views / 1000 x cpm` through `writeClipEarnings`, and `shares` has never been an input to any of it, which `lamatok.ts:473-474` records in its own words. `views`, `likes` and `comments` are byte-identical in both create objects. The other seven money files are byte-identical by blob OID (PART 5).

### Fail open

**Nothing here can block or slow the tick or a submit.** No call, no await and no branch was added to any request path: the field is read off a response already in hand, and every read is `numericOrUndef` or `?? null`, which cannot throw. A provider error, a malformed body, a missing key and a disabled count all produce `sharesSource: null` and the row is written exactly as it would have been.

---

## PART 2 — YOUTUBE, WHERE NO FIX EXISTS

BL-819 established that the Data API v3 `statistics` resource carries `viewCount`, `likeCount`, `favoriteCount` and `commentCount` and no share field, and that 0 of 61,400 stored YouTube snapshots have ever held one. **No fetch can be built.** `youtube.ts:261` keeps `shares: 0` and never sets a source, so every YouTube snapshot is permanently ABSENT, which is the truth.

**So eight surfaces stop implying a number.** This is BL-776's honesty applied again: it made a YouTube clip state outright that the six-hour arrival figure means nothing there.

| # | surface | file:line | before | after |
|---|---|---|---|---|
| 1 | clipper's clip card | `ClipCardNew.tsx:198-232` | `0` | **`—`** plus a spoken state and a visible legend |
| 2 | legacy clipper list | `clips/page.tsx:437` | `0` | **`—`** plus a spoken state |
| 3 | admin clip row | `admin/clips/page.tsx:1812` | `0 shares` | **`— shares`** plus a spoken state |
| 4 | tracking history, per snapshot | `tracking-modal.tsx:348` | `0` | **`—`** plus one note above the grid |
| 5 | admin archive, clip table | `admin/archive/[campaignId]/page.tsx:404` | `0` | **`—`** |
| 6 | admin archive, totals | route `:62`, `:173` | summed unmeasured zeros | **measured rows only**, with `sharesMeasuredCount` |
| 7 | client campaign table | `client/page.tsx:471` | `0` | **`—`** |
| 8 | **client "Shares" KPI tile** | `client/page.tsx:380` | a bare headline total | **measured rows only**, qualified `from N of M clips` |
| 9 | client daily breakdown | `client/page.tsx` | a silent zero column | one note naming what the column covers |
| 10 | **CSV export** | `api/admin/export/route.ts:266`, `:486`, `:436` | `0` | **`not measured`**, plus `Total Shares covers N of M approved clips` |
| 11 | **admin analytics metric** | `admin/analytics/page.tsx:116` | a selectable chart drawing a flat zero line | **removed** |

**The two states read differently to a screen reader and that is deliberate.** Both render the same glyph, because both are truthful, but the spoken text differs:

> **Instagram or TikTok, unmeasured:** *"not measured"*
> **YouTube:** *"not measured, YouTube does not publish share counts"*

"Not measured" alone implies a number may still arrive, and on YouTube that is a promise nothing can keep.

**Why the analytics metric was removed rather than annotated.** A warning cannot discharge it: the chart component carries **no role, no accessible name and no table alternative**, so a non-visual reader could never reach a caption bound to it. Worse, its `hasData` check is false when every value is zero, so Shares alone renders "No data yet" (which implies *coming*) while Shares plotted beside Views draws a genuine, convincing flat-zero line. **The metric comes back when there is enough measured Instagram history to plot; the route still serves it and nothing was deleted.**

---

## PART 3 — THE HISTORY

### Can the old zeros be distinguished now? Yes, and it cost nothing

**The column did it by existing.** All 267,099 pre-existing rows are NULL, and NULL means *nobody measured this*, which is exactly and verifiably true of every one of them.

| platform | snapshots | value > 0 | value = 0 | what the display now says about the zeros |
|---|---|---|---|---|
| instagram | 142,419 | 3 | 142,416 | **absent**, correctly: BL-819 proved no provider ever wrote one |
| youtube | 61,400 | 0 | 61,400 | **absent**, permanently, and the surface says why |
| tiktok | 63,212 | 32,937 | 30,275 | see below |

**A regression this measurement caught before it shipped.** TikTok already holds **32,937 snapshots with a correct positive share count and no label**, because TikTok has always read `shareCount` properly and only the label is new. Keying the display purely on `sharesSource` would have rendered every one of those as a dash despite holding a real number: **a new false statement rather than a fix.**

**Solved without a backfill.** The shared predicate accepts a positive value as measured too:

```ts
export function isMeasuredShare(stat) {
  if (stat.sharesSource != null) return true;
  return typeof stat.shares === "number" && stat.shares > 0;
}
```

**It cannot erase a measured zero**, which is the failure mode to avoid: the second clause only ever ADDS measured status. A zero with a source stays measured; a zero without one stays absent. **And it cannot invent one:** no code path has ever written a positive share count without reading it, because a fabricated share count is always exactly `0` on every platform and every writer. That is precisely why BL-819 could not tell the two apart before this column existed.

### A backfill: possible, and NOT worth doing. Not run.

**Spec, for its own round if the owner disagrees:**

1. Instagram clips only, `isDeleted = false`, `status = APPROVED`, `videoUnavailable = false`. Roughly 4,400 clips, one `fetchHikerInstagramByUrl` each, about **$4.40**.
2. Write a new `ClipStat` **only** when `reshare_count` is a finite number, so `sharesSource` is non-null. **Never write a zero**, which is the same gate BL-746 shipped.
3. **Skip anything returning 404 or `MediaNotFound`**: BL-720's gone-post signal, so a missing post cannot look like a zero.
4. Write **no earnings** and touch no other column. Shares are not an earnings input.
5. Disclose the call count and respect one call per post, never a profile scan.

**And the honest recommendation is not to.** `reshare_count` is a **current** value with no history behind it. A backfill would stamp today's figure onto a clip as though it had been measured at submission, which corrupts the very signal the fix exists to restore: `fraud.ts` rule #9 compares a latest value to a peak **across a series**, and a single synthetic point cannot form one. It would buy a number that is worse than absence.

### What the owner will see, old clips against new

**A share count appearing on a clip is the fix working, not a spike.** Say so before somebody reads it as one:

* **Every Instagram clip in existence today** shows `—` for shares until its next tick after the redeploy, then shows a real number from that tick onward. Its snapshot history stays a run of dashes followed by real values, and the tracking modal states that above the grid.
* **The first real value can be large.** One probed reel carries 86,676 reshares. That is not a jump; it is the first reading of a number that was always there.
* **TikTok changes nothing.** Values and labels both already correct.
* **YouTube shows `—` forever** and the surface says why.
* **No historical figure moved.** The share sum across all 267,099 rows is identical before and after (PART 5).

---

## PART 4 — WHAT THIS RESTORES, AND A BUG IT NEARLY CREATED

### The evidence panel does not use shares, and the brief's premise needs correcting

**BL-775's `ReviewEvidencePanel` reads no share count.** `grep -c "shares"` returns **0** over the component and **0** over `api/admin/review-evidence/batch/route.ts`. Its three sections are the clipper's own rejection record, the view-arrival curve and platform analytics. BL-819 established this and it is unchanged. **This round adds nothing to that panel and builds no score, no threshold and no ratio**, which is the standing rule: BL-771 measured every computable signal under **21% precision** against a **99.2%** reviewer bar.

### But `fraud.ts` does use shares, and it was flattened

`src/lib/fraud.ts` signal **#9**, BL-264's ENGAGEMENT DROP, is classed **STRONG** and worth **25 points**, and it iterates three metrics at `:184`: likes, comments and **shares**. It is live via `tracking.ts:219`. With shares permanently zero, `peak > 0` was never satisfied on Instagram or YouTube, so **one third of a STRONG signal has never once been able to fire** on 5,752 clips, which is every Instagram and YouTube clip on the platform bar one. It produced no false accusations; it silently contributed nothing.

**Real counts switch that arm on for Instagram**, which BL-771 measured as **58% of the bought-view problem**.

### The bug the accessibility review caught, which is why the review is worth running

**Turning the arm on would have created a false accusation**, and it is a correctness defect, not a styling one:

> A clip reads **86,676** shares. One later tick hits a post whose `reshare_count` the provider omits, exactly like `cmt60k1v` in PART 0. That snapshot stores `0`. Rule #9 compares the latest value to the peak, sees a **100% fall**, clears both `DROP_PCT` (0.05) and `DROP_FLOOR_ENGAGEMENT` (3), and awards **+25 STRONG** with the reason *"real engagement rarely drops; consistent with purged/pulled fake activity"*.
>
> **A real person accused of buying engagement because we failed to read a number.** BL-518 and BL-521 forbid exactly that.

**Fixed in the same round that created the risk.** Rule #9 now filters the share series to MEASURED snapshots only, through **the same shared predicate the display uses**, so a snapshot the screen calls measured and the fraud rule calls unmeasured cannot exist. Fewer than two measured points means no comparison and the arm stays silent, which is the discipline BL-775 applied when it refused to draw a curve from under three snapshots. Likes and comments are untouched and byte-identical in behaviour.

---

## PART 5 — THE EVIDENCE

### Instagram, through `tryHikerForInstagram`, the exact function the tick calls

**Disclosed: 6 more provider calls (4 HikerAPI, 2 LamaTok), roughly $0.006. Round total 12 calls, roughly $0.012. No Apify actor. Nothing written.**

| clip | requested | verdict | views | **shares** | **`sharesSource`** | **state** | expected |
|---|---|---|---|---|---|---|---|
| `cmt095se` | `DcOg6OvoshY` | ok | 932,713 | **86,676** | **`"reshare_count"`** | **MEASURED** | MEASURED ✓ |
| `cmsvqt6l` | `DcGZEHko23J` | ok | 89,923 | **5,769** | **`"reshare_count"`** | **MEASURED** | MEASURED ✓ |
| `cmt22y0u` | `DcRyEHFRTdm` | ok | 6,681 | **5** | **`"reshare_count"`** | **MEASURED** | MEASURED ✓ |
| **`cmt60k1v`** | `DcY4Xx8g1hS` | ok | 211 | **0** | **`null`** | **ABSENT** | **ABSENT ✓** |

Each value matches the `reshare_count` PART 0 read off the raw body for the same code, and every code returned is the code requested. **The absent case records ABSENT and not a zero, proven on a live post rather than a synthetic one.**

### TikTok, unchanged and now labelled

| clip | http | views | shares | `sharesSource` | state |
|---|---|---|---|---|---|
| `cmrvjd71` | 200 | 8,879 | **62** | **`"shareCount"`** | MEASURED |
| `cmr7guez` | 200 | 20,700 | **11** | **`"shareCount"`** | MEASURED |

Both match what BL-819 measured and what is stored. **The value logic is byte-identical; only the label is new.**

### The one link I cannot close, stated plainly

**I did not run the tracking tick, so no Instagram clip has a STORED `sharesSource` yet, and I will not claim one does.** Running it would write `ClipStat` rows and recompute earnings, which this round's own safety rule forbids. What is proven: the provider returns the value; the production reader now surfaces it with a source; the tick write passes both through verbatim (the line is printed in PART 1); and the column exists and accepts it. **The first stored value arrives on the first tick after the Railway redeploy**, and that is the number to check.

### Nothing moved

The same query at `21:11:06` and `21:18:12`:

| | before | after |
|---|---|---|
| `clip_stats` rows | **267,099** | **267,099** |
| **sum of all `views`** | **1,513,901,587** | **1,513,901,587** |
| **sum of all `likes`** | **66,519,073** | **66,519,073** |
| **sum of all `comments`** | **497,378** | **497,378** |
| **sum of all `shares`** | **2,468,866** | **2,468,866** |
| live clips | 7,282 | 7,282 |
| **earnings invariant violations** | **0** | **0** |
| payout rows | 189 | 189 |
| newest payout `updatedAt` | `2026-08-23 13:54:54.914` | `2026-08-23 13:54:54.914` |
| newest `ClipStat.checkedAt` | `2026-08-23 21:10:47.342` | `2026-08-23 21:10:47.342` |

**No clip's views, likes, comments or shares changed. No payout was created, modified, approved, cancelled or paid.** The newest payout `updatedAt` predates the round by seven hours.

**One figure moved and it was not me.** Approved earnings read `$13,998.64` then `$13,999.71`, a `$1.07` rise. Cause, measured: **8 clips were APPROVED by the owner between `21:13:52.123` and `21:17:15.565`**, carrying exactly `$1.07` between them. No snapshot was written in the window (the newest is unchanged) and no share value moved. That is the owner working in the live admin UI concurrently, and it is reported rather than smoothed, on the same discipline BL-728 applied to three payout rows that moved during its own window.

### The money files

`git rev-parse main:<file>` against `git hash-object <working tree>`:

| file | blob OID | |
|---|---|---|
| `clip-earnings-writer.ts` | `ac5be7deb061` | **IDENTICAL** |
| `earnings-calc.ts` | `797e20985ad5` | **IDENTICAL** |
| `balance.ts` | `e887f80acfc7` | **IDENTICAL** |
| `clip-earnings-invariant-middleware.ts` | `61cef3939536` | **IDENTICAL** |
| `money-decimal.ts` | `ef5cdae757b9` | **IDENTICAL** |
| `campaign-era.ts` | `106e16ad7512` | **IDENTICAL** |
| `earnings-never-decrease.ts` | `c15145f51a56` | **IDENTICAL** |
| **`tracking.ts`** | `83ce4babfd39` → `359bcbbe22fe` | **CHANGED, six additive lines, justified in PART 1 and printed in full** |

**`apify.ts` carries the same 8 `BL-678` guard comment lines on both refs**, and `APIFY_HARD_OFF` is a `const true`, so no Apify actor can run and none did.

---

## PART 6 — GATES AND MERGE

`eslint v9.39.4` confirmed present, so the hooks gate is real. `npm ci` exit 0, then `npx prisma generate` exit 0 **before** any typecheck, and again after the schema edit.

| gate | baseline, measured on this worktree before the first edit | after |
|---|---|---|
| `npx tsc --noEmit` | **exit 0**, 0 errors | **exit 0**, 0 errors |
| `npm run build` | **BUILD_BASE_EXIT=0** | **BUILD2_EXIT=0**, compiled in 30.2s |
| `lint:hooks` | **0 errors, 11 warnings** | **0 errors, 11 warnings** |
| `check:prisma-bypass` | | **0 violations** across `src/` + `scripts/` |
| `check:removed-fields` | | passed |

Exit codes were echoed from `$?` into a log immediately after each command and **never read through `tail`**. `tsc` was run eleven times during the round and genuinely failed twice, both times caught and fixed rather than papered over: once because `owner-submit-core.ts:218` assigned an object missing the new field, and once because narrowing `keyof StatSnapshot` was required after the fraud type gained a non-numeric member.

**The diff is real and non-empty: 27 files, +795 / −50.**

### Merge

| | |
|---|---|
| base | `a457637f` |
| branch | `checkpoint/BL-820` @ `d1c6aa64`, on origin with both tags |
| merge | `--no-ff` → **`b9a288cc`** |
| **merge tree OID** | **`a90e8e0c3515`** |
| **branch tree OID** | **`a90e8e0c3515`, IDENTICAL** |
| conflicts | **none**; `git grep` for conflict markers tree-wide returns **0** |
| BACKLOG | `grep -c "^## BL-"` **161 → 162**, exactly **one** BL-820 entry, never piped through `head` |
| `checkpoint/BL-723` | **NOT merged**: `git branch --contains` reports 0 |
| push | **`origin/main == local == b9a288cc`**, `safe-push` reported `VERIFIED PUSHED` and `git ls-remote` agrees |

The merge tree OID equals the branch tree OID, so the branch build IS the merge build. A post-merge build was run on main regardless.

**A REDEPLOY ON RAILWAY IS REQUIRED.** Until then the column exists and nothing writes to it.

### Accessibility

The lead reviewed the plan **before any UI was written**, coordinating four specialists, and **it changed the round.** Its six blocking items:

**B1 — trigger on `sharesSource`, never on `shares === 0`.** Already the design; confirmed.
**B2 — a second, unhandled state.** With no snapshot at all, views, likes and comments also rendered a fabricated `0`, so fixing shares alone would have produced a self-contradictory row: three hard zeros beside one honest dash, all describing the same missing snapshot. **All four cells now show the placeholder when there is no snapshot.** This is the item BL-748's own review logged and deferred.
**B3 — the em dash must never carry the meaning alone.** NVDA, JAWS and VoiceOver announce U+2014 inconsistently or not at all at default punctuation, so a bare dash reads as a broken cell. **Every site is `aria-hidden` glyph plus an `sr-only` state**, spoken BEFORE the label so a reader hears "not measured, shares" rather than the label twice, plus **one visible legend per surface** so a sighted low-vision or cognitive reader is not left with an unexplained glyph.
**B4 — two surfaces missing from my list**, the client "Shares" KPI tile and the client daily breakdown. Both handled in PART 2.
**B5 — the admin override had no provenance.** A hand-typed count now stamps `sharesSource: "manual"`, so an override cannot launder an unknown into a measured-looking figure.
**B6 — the false fraud accusation.** PART 4. **The one item the lead said it would not ship without, and it was right.**

**Colour.** `--text-quiet`, measured by the review at **7.17:1** dark and **7.73:1** light on the card, with a **2.57:1** step down from a real number in both themes so the placeholder never collapses into the value or shouts over it. Never `--text-muted`: in dark, primary, secondary and muted are all `#ffffff`, so a muted placeholder would be **1.00:1** against a real number, pixel-identical. Never the accent: 3.40:1 on the light card. **1.4.1 is satisfied because the glyph carries the meaning and colour only reinforces it.**

**Reported, NOT fixed, each in the BACKLOG:** `--bg-page` is used 41 times across 24 files and **defined nowhere**, mostly in `focus-visible:ring-offset-[var(--bg-page)]`, and an unresolvable `var()` invalidates the composite box-shadow and likely removes the whole focus ring (WCAG 2.4.7, Level A, unrelated to this round and worth its own); `area-gradient-chart.tsx` has zero ARIA and hardcodes `rgba(255,255,255,…)` for grid and axis ticks, invisible in the light theme; the client and archive tables have no `<caption>` and no `scope`; `admin/analytics/page.tsx:120-126` gives views and earnings the identical `#2596be`; and `globals.css` misstates two of its own measured contrast ratios.

**On the design skill:** `frontend-design` was read before any UI. Its anchor-selection step does not apply to surgical edits inside a shipped design system that CLAUDE.md already specifies to the hex, and applying it would be the hybridising the skill itself forbids. **§2, "Content is not design", is the clause that governs**, and every string added is quoted above so it can be judged rather than trusted.

---

## WHAT COULD NOT BE ESTABLISHED

* **A stored `sharesSource` on a real Instagram clip.** Only the tick can write one and running it would change data. PART 5 states exactly what is proven and what is not.
* **`share_count_disabled: true`, live.** `false` on 6 of 6. The branch is written because the alternative is recording a hidden count as a measured zero, but its real-world frequency is unknown and it was never observed.
* **The carousel nesting.** All six probed posts resolved to `media_type: 2`. A carousel reads the same top-level `reshare_count`, which is the post-level count Instagram publishes, and no carousel was in the sample.
* **Whether `reshare_count` is what the owner would call a "share".** Instagram publishes two counts on the same object and they differ by up to 50x. `reshare_count` is the larger, is present far more often, and is the one that behaves like a share count. **If the owner means the smaller `media_repost_count`, that is a one-line change and he should say so.**
* **No browser render was performed.** The clipper and client surfaces sit behind sessions I do not have, and the round's own rule forbade seeding data to reach them. The strings and states above are derived from the shipped source and the live provider responses, not from a screen I photographed, and I am not claiming otherwise.

---

## VERIFICATION

The key path was confirmed on a real probed response before a line was written, across media types, with `media_repost_count` explicitly rejected as a fallback on evidence and the absent case proven live on `cmt60k1v`. The count is extracted in `hikerapi.ts`, carried through all four classifier branches, both overlay branches, the batch fold at `apify.ts:1607` that BL-819 did not find, both LamaTok readers, both submit paths and both tick writes, with the full `tracking.ts` diff printed and loudly justified as six additive lines that touch no money. An absent count or a disabled one records ABSENT and never a fabricated zero, enforced by a nullable `sharesSource` rather than by a value test, and the stored value in every case is tabulated. Every YouTube surface now states shares are unavailable instead of rendering 0, eleven surfaces named, and the analytics metric was removed rather than annotated because the chart carries no accessible name a warning could bind to. Historical zeros are distinguishable because all 267,099 pre-existing rows are NULL, which is true of them; a backfill is specced, argued against and **not run**; and what the owner will see on old clips against new is stated so a first real count is not read as a spike. The evidence panel does not use shares and none was added, no score or threshold was built, and the fraud rule that DOES use shares was hardened against the false accusation this round would otherwise have created. Twelve probe calls totalling roughly $0.012 are disclosed, every response id-matched, **no Apify actor ran** and the BL-678 guards are intact. Every stat aggregate is identical before and after including the share sum at 2,468,866, the invariant is 0, no payout was touched, and the one moving figure is named as 8 clips the owner approved mid-round. Seven money files are byte-identical by blob OID; `tracking.ts` is the eighth and its every line is printed. Merged to main at `b9a288cc` with the merge tree OID equal to the branch tree OID, zero conflict markers, BACKLOG counted 161 to 162 by `grep -c`, `checkpoint/BL-723` excluded and proven not merged, and `origin/main == local` verified twice. `tsc` and `next build` were both actually run with their exit codes echoed directly, and the two genuine `tsc` failures during the round are disclosed. The worktree is removed. **No dashes as bullets. A Railway REDEPLOY is required.**
