# BL-819 — the owner is right about two platforms out of three, and Instagram is returning the number we throw away

**2026-08-23 · DB `now()` = `2026-08-23 20:18:55.714673+00` (first read) to `20:25:38.812215+00` (last) · AUDIT ONLY. READ ONLY.**
No code, data or config changed. Nothing written to the database; every read through `scripts/run-select.js`, which refuses a write keyword before it connects. Every timestamp cast `::text` against DB `now()`. Base `origin/main` @ `a457637f`, branch `checkpoint/BL-819`, isolated worktree `C:/w819`, a short path, `node_modules` never junctioned, removed at the end. **No Apify actor ran and none can**: `APIFY_HARD_OFF` is a `const true` (`apify-hard-off.ts:32`), so every branch behind it is statically dead, and `apify.ts` carries its 8 `BL-678` guard comments untouched. Handles redacted; clips appear as 8 character id prefixes.

> **ONE LINE PER PLATFORM.**
> **TikTok: YES.** Shares are fetched, stored and moving. 720 of 1,351 live clips carry a positive count, 32,935 snapshots have one, the highest is 74,700, and 3 of 3 live probes matched storage.
> **Instagram: NO, and this is the finding.** Zero of 4,499 live clips, zero of 142,179 snapshots ever written by a provider. **The provider returns the number and the code never reads it.** All 3 probed reels came back with `reshare_count` at **86,676**, **37,919** and **5,769**, id-matched, each on a clip storing `shares = 0`, each with `share_count_disabled = false`.
> **YouTube: NO, and no fix exists.** The Data API v3 `statistics` object has no share field, the code says so accurately, and 0 of 61,400 snapshots have ever carried one. **The surface should stop implying it has a number.**

---

## PART 1 — MEASURED FROM THE DATABASE FIRST

### The latest stat on every live clip

`db_now = 2026-08-23 20:19:14.914209+00`, every non-deleted clip, most recent snapshot per clip.

| platform | live clips | with a stat | **shares > 0** | shares exactly 0 | likes > 0 | comments > 0 | **% shares positive** | % likes positive |
|---|---|---|---|---|---|---|---|---|
| instagram | 4,530 | 4,499 | **0** | **4,499** | 4,003 | 1,233 | **0.0%** | 89.0% |
| youtube | 1,395 | 1,395 | **0** | **1,395** | 673 | 204 | **0.0%** | 48.2% |
| tiktok | 1,353 | 1,351 | **720** | 631 | 1,233 | 584 | **53.3%** | 91.3% |

**Nothing is null, anywhere, and that is structural rather than lucky.** `ClipStat.shares` is `Int @default(0)` (`prisma/schema.prisma:1173`), non-nullable, exactly like `views`, `likes` and `comments`. **There is no third state.** An absent share count and a genuinely unshared clip are the same stored byte, on every platform, which is precisely why this could sit in production for four months without anybody noticing.

**Likes and comments work on the same clips, through the same fetch, in the same snapshot.** Instagram reads 89.0% positive likes against 0.0% positive shares. That isolates the fault to one field, not to the platform's fetch.

### Has a provider EVER written a positive Instagram or YouTube share count

| platform | snapshots ever | **snapshots with shares > 0** | max share ever | snapshots with likes > 0 | oldest | newest |
|---|---|---|---|---|---|---|
| instagram | 142,179 | **3** | 2,746 | 126,846 | 2026-04-22 19:57:55.505 | 2026-08-23 20:11:32.848 |
| tiktok | 63,203 | **32,935** | 74,700 | 59,068 | 2026-04-23 14:38:20.782 | 2026-08-23 20:11:16.362 |
| youtube | 61,400 | **0** | **0** | 30,057 | 2026-04-23 14:37:27.646 | 2026-08-12 11:55:04.66 |

**The three Instagram rows are not a provider fetch. They are the owner typing.** All three carry `isManual = true`, all three are the same clip, and all three were written in May through the manual override at `api/clips/[id]/override/route.ts:174`:

| clip | views | likes | shares | `isManual` | at (`::text`) |
|---|---|---|---|---|---|
| `cmp2hc6g` | 473 | 24,300 | 2,433 | **true** | 2026-05-12 13:32:56.502 |
| `cmp2hc6g` | 473,000 | 24,300 | 2,433 | **true** | 2026-05-12 13:33:11.553 |
| `cmp2hc6g` | 539,000 | 28,400 | 2,746 | **true** | 2026-05-13 07:21:26.282 |

**So across 142,179 Instagram snapshots and 61,400 YouTube snapshots, no provider has ever produced a single non-zero share count. Not once.**

### The movement test, which is the real one

Clips with at least two snapshots in the last 7 days whose views rose between them. `db_now = 2026-08-23 20:19:41.514583+00`.

| platform | clips whose views rose | **shares also rose** | likes also rose | comments also rose | **% shares moved** | % likes moved | median view gain | median share gain | **max share gain** |
|---|---|---|---|---|---|---|---|---|---|
| instagram | 1,858 | **0** | 1,115 | 212 | **0.0%** | 60.0% | 187 | **0** | **0** |
| tiktok | 148 | 12 | 64 | 14 | 8.1% | 43.2% | 26 | 0 | **3** |
| youtube | **no rows** | | | | | | | | |

**Instagram: 1,858 clips gained views in seven days, one of them by 931,449 views, and not one share count moved by a single unit.** The maximum share gain across the entire population is exactly 0. That is not a partly-working metric; it is a constant.

**TikTok's 8.1% is not a defect.** A share is a rarer event than a view: 612 of TikTok's 1,792 snapshots in the window carry a positive count and the largest is 268. The median gain is 0 because most clips genuinely gain no shares in a week, and the maximum gain of +3 is a real observed movement. The distribution is what a working, low-frequency counter looks like.

**YouTube has no row because YouTube has no snapshots.** Over 7 days: Instagram 34,234 snapshots across 2,129 clips, TikTok 1,792 across 191, **YouTube 0 across 0**. Its newest snapshot of any kind is `2026-08-12 11:55:04.66`, **eleven days ago**, against 666 active tracking jobs. That is an adjacent finding, outside this round's subject, and it is stated in PART 6 rather than buried.

### The verdict per platform

**TikTok: WORKING.** Not a defect and not the owner's impression.
**Instagram: GENUINELY DEAD.** Zero, always, everywhere, by construction.
**YouTube: GENUINELY DEAD**, and correctly so at the provider level.

**BL-782's lesson was checked for and does not apply.** That round found a suspected regression was historical clips dragging an already-fixed figure. There is no such window here: the Instagram figure is 0 in the last 7 days, 0 in the last 30, and 0 across all 142,179 snapshots since April. There is no cutover to split on, because there was never a working period.

---

## PART 2 — THE FETCH, TRACED PER PLATFORM

### TikTok via LamaTok — correct, end to end

| step | file:line | what it does |
|---|---|---|
| provider key | live response, PART 5 | **`shareCount`**, present on 3 of 3 |
| by/url reader | **`lamatok.ts:477`** | `pickNumber([stat?.share_count, stat?.shareCount]) ?? 0` |
| by/id reader | **`lamatok.ts:296`** | identical expression |
| into the stats object | `lamatok.ts:493` and `:303` | `shares` carried verbatim |
| the tick write | **`tracking.ts:1789`** and `:1801` | `shares: stats.shares` |
| the first stat at submit | **`clipper-submit-core.ts:668`** | `shares: fetchedStats?.shares ?? 0` |

**Nothing is lost.** The apidojo TikTok twin reads the same thing four ways at `apidojo.ts:219` (`shares ?? shareCount ?? sharesCount ?? sharedCount`) and writes it at `:482` and `:748`, so the fallback would also have carried it had it been reachable.

### Instagram via HikerAPI — the loss point, named exactly

**The provider DOES return a share count.** `reshare_count`, on the same `media_or_ad` object the view count is read from, live on 3 of 3 probes (PART 5). A second field, `media_repost_count`, is present too.

**THE LOSS POINT IS `hikerapi.ts:540-541`.** The classifier extracts exactly two engagement fields and never looks for a third:

```
540:  const likes    = numericOrUndef(media.like_count ?? media.likes_count ?? media.likes);
541:  const comments = numericOrUndef(media.comment_count ?? media.comments_count ?? media.comments);
```

`grep -c` for any share extraction in that file returns **0**. `HikerResult.shares` is **declared** at `hikerapi.ts:71` as `shares?: number` and **never assigned on any branch**, which the probe confirms directly: `HikerResult.shares = undefined` on all three reels.

**Downstream, a literal 0 is substituted twice, with a comment asserting the field does not exist:**

| file:line | code | the assertion beside it |
|---|---|---|
| **`hikerapi.ts:935-936`** | `shares: 0` | `// shares: IG has no share-count concept on v2.` |
| **`hikerapi.ts:873`** | `shares: 0` | the carousel_mixed twin, no comment |
| **`hikerapi.ts:699`** | docblock | `shares = 0 (IG has no share count concept on /v2 media)` |
| **`clipper-submit-core.ts:542`** | `shares: 0` | BL-746's first-stat harvest |
| **`owner-submit-core.ts:193`** | `shares: 0` | the initialiser BL-782 flagged, written unconditionally at `:291` |
| `apidojo.ts:681` and `:829` | `shares: 0` | `// Instagram doesn't expose share counts.` |

**The assertion is false, and this file has form.** Forty lines below the share hardcode, `hikerapi.ts:937-944` carries BL-686's correction of the previous comment in the same object: *"The old comment here claimed Hiker's v2 surface doesn't expose a parseable ISO timestamp consistently. THAT WAS WRONG, and it mattered."* **This is the same class of error, one field over, and it was verified against a real payload rather than against the code's expectation, exactly as BL-746's four wrong-shape probes require.**

The apidojo sites are currently unreachable (apidojo is imported only by `apify.ts`, which is hard off) but are named so a fix cannot leave a live copy behind.

### YouTube via the Data API — honestly absent

| step | file:line | what it does |
|---|---|---|
| the request | **`youtube.ts:29`** and **`:95`** | `part=statistics` only |
| the write | **`youtube.ts:261`** | `shares: 0,  // YouTube API doesn't expose shares` |
| the other path | `youtube.ts:119-121` | reads viewCount, likeCount, commentCount; no share read |

**The comment is accurate.** The Data API v3 `statistics` resource exposes `viewCount`, `likeCount`, `favoriteCount` and `commentCount`. There is no share count in it, and no other public YouTube endpoint returns one. **This is not a loss point; there is nothing to lose.**

### The write path, common to all three

`tracking.ts:1789` (manual) and `:1801` (the tick) both write `shares: stats.shares` unconditionally, and `ClipStat.shares` is non-nullable, so **whatever the provider layer produces is stored verbatim, including a fabricated 0**. The write is not the defect on any platform. The defect is what reaches it.

---

## PART 3 — THE FABRICATED ZERO, WHICH IS EXACTLY WHAT THIS IS

BL-748 found `hikerapi.ts:603` fabricating a 0 for a hidden Instagram view count. BL-753 found `youtube.ts:178` doing the same when YouTube omits `statistics.viewCount`. **Both were fixed for views. The same pattern is live for shares on two platforms, and on Instagram it is worse than either of them.**

| platform | is an absent share count stored as 0, as null, or skipped? | is it distinguishable from a genuine zero? |
|---|---|---|
| **instagram** | **stored as a fabricated 0**, hardcoded at `hikerapi.ts:936` and `:873` before any lookup happens | **NO** |
| **youtube** | **stored as a fabricated 0**, hardcoded at `youtube.ts:261` | **NO** |
| **tiktok** | a real read, `?? 0` only when the key is genuinely absent | **NO**, but the key is present on 3 of 3 probes |

**Instagram's is the more serious of the two, and the difference matters.** BL-748's and BL-753's fabrications fired only when the provider *withheld* a field. This one fires **unconditionally**: the literal `0` is written on every single Instagram snapshot regardless of what came back, because no code ever asks. A hidden count and a real 86,676 produce the identical stored byte.

**And it is invisible by construction, which is why nobody found it.** BL-543's rule is that an unresolvable count must be null so the clip keeps its last known value. `ClipStat.shares` cannot hold null. So the three-state distinction BL-748 restored for views (`hidden -> null`, `genuine zero -> 0 with a viewSource`) **has no equivalent for shares on any platform**. A share count stuck at exactly 0 across 4,499 Instagram clips is indistinguishable from 4,499 genuinely unshared clips, and the platform's own display renders both as `0`.

**TikTok's `?? 0` is the same latent shape and is not currently firing.** `lamatok.ts:473-474` even records the reasoning: *"likes/comments/shares are NOT the earnings driver; 0 default is fine."* That is true for money and false for evidence, which is PART 4.

---

## PART 4 — WHERE SHARES APPEAR, AND WHAT THEY RENDER

**Eleven surfaces render a share count. Every one of them renders `0` for Instagram and YouTube, and none of them distinguishes an unmeasured count from a measured zero.**

| # | surface | file:line | at zero or absent |
|---|---|---|---|
| 1 | clipper's clip card | **`ClipCardNew.tsx:202`** | `stat ? formatNumber(stat.shares) : "0"` — a literal `0` even with **no snapshot at all** |
| 2 | clipper's legacy clip list | `clips/page.tsx:437` | same expression, same literal `0` |
| 3 | admin clip row | **`admin/clips/page.tsx:1812`** | same expression, `0 shares` |
| 4 | tracking modal, per snapshot | `tracking-modal.tsx:348` | `formatNumber(snap.shares)` → `0` |
| 5 | admin archive, clip table | `admin/archive/[campaignId]/page.tsx:404` | `0` under a `Shares` label |
| 6 | admin archive, day table | `admin/archive/[campaignId]/page.tsx:465` | `0` |
| 7 | client campaign view, per clip | `client/page.tsx:471` | `0` |
| 8 | client campaign view, per day and total | `client/page.tsx:521`, `:531` | `0` |
| 9 | **admin analytics, a selectable metric** | `admin/analytics/page.tsx:116`, route `views-by-day/route.ts:106` | a chart that is **a flat zero line** for IG and YouTube |
| 10 | CSV export, clip rows and totals | `api/admin/export/route.ts:249`, `:266`, `:436`, `:468`, `:486` | a `Shares` column of zeros and a `Total Shares` of 0 |
| 11 | admin manual override form | `admin/clips/page.tsx:2764`, write at `api/clips/[id]/override/route.ts:174` | prefilled `"0"`; the only way a non-zero IG share has ever entered the database |

**Surface 9 is the one that will mislead the owner fastest**: selecting "Shares" in `/admin/analytics` draws a real chart from real SQL over a column that is constant zero, and nothing on it says the metric is not collected on two of three platforms.

**Surface 1 carries the defect BL-748's accessibility review already logged and deferred**: a clip with no snapshot renders a hard literal `0`, so "not measured" and "nobody shared it" are the same glyph. For shares that is now true of every Instagram clip whether or not it has a snapshot.

### The fraud evidence, corrected against the brief's premise

**BL-775's evidence panel does NOT use shares, and does not use engagement ratios at all.** `grep -c "shares"` over `ReviewEvidencePanel.tsx` returns **0**, and over `api/admin/review-evidence/batch/route.ts` returns **0**. Its three sections are the clipper's own rejection record, the view-arrival curve and platform analytics. The two `shares` hits in `review-evidence.ts` (`:198`, `:281`) are the English word in a comment about the marketplace 60/30/10 split.

**But the brief's concern is correct, one file over, and it is measurable.** `src/lib/fraud.ts` signal 9, BL-264's **ENGAGEMENT DROP**, is classed **STRONG** and worth 25 points, and it iterates exactly three metrics at `fraud.ts:181-185`:

```
{ key: "likes", label: "Likes" }, { key: "comments", label: "Comments" }, { key: "shares", label: "Shares" }
```

It is **live**: `tracking.ts:219` imports `computeFraudLevel`. The arm requires `peak > 0` (`fraud.ts:191`), so with shares permanently 0 the share arm can never fire.

| platform | clips with 2+ snapshots, signal 9 computable | **share arm structurally dead** | likes arm dead | **% share arm dead** |
|---|---|---|---|---|
| instagram | 4,396 | **4,395** | 404 | **100.0%** |
| youtube | 1,357 | **1,357** | 665 | **100.0%** |
| tiktok | 1,311 | 595 | 88 | 45.4% |

**One third of a STRONG fraud signal is switched off on 5,752 clips**, which is every Instagram and YouTube clip on the platform bar one, and the one exception is the manually overridden clip from May. BL-771 measured engagement as one of the signals separating bought views from real ones; on Instagram, which BL-771 measured as **58% of the bought-view problem**, the share arm has never once been able to fire.

**It produces no false accusations**, which is worth saying plainly: a dead counter cannot manufacture a drop. It silently contributes nothing, which is the harder failure to notice.

---

## PART 5 — THE LIVE PROBES

**Every probe went through the REAL production reader**, `fetchHikerInstagramByUrl` and `fetchLamatokTiktokByUrl`, on clips drawn from the live population, never invented. Every response was matched on the id that was requested, never on row position, which is BL-550's trap. **Nothing was written: no `ClipStat`, no clip, no database call of any kind from the probe.**

### Disclosed cost, stated accurately including my own waste

**18 provider calls: 9 HikerAPI and 9 LamaTok, roughly $0.018.** The probe makes 6 calls and **I ran it three times**, because the output is long and I read it in three slices rather than capturing it once. That is 12 calls of pure waste caused by me, it is inside the round's ~20 cap but only just, and it is reported rather than counted as 6. Every call is a single post lookup, never a profile scan, so **ONE CALL PER PROFILE is not engaged**. **No Apify actor ran and none can.**

### Instagram, HikerAPI `/v2/media/info/by/code`, 3 of 3

| clip | code requested | returned code | **id match** | http | resolved views | likes | comments | **`HikerResult.shares`** | **`reshare_count` in the raw response** | `share_count_disabled` | **stored `shares`** |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `cmt095se` | `DcOg6OvoshY` | `DcOg6OvoshY` | **true** | 200 | 931,778 | 61,833 | 144 | **undefined** | **86,676** | **false** | **0** |
| `cmss4vfy` | `Db_4ocIovOi` | `Db_4ocIovOi` | **true** | 200 | 169,843 | 11,875 | 233 | **undefined** | **37,919** | **false** | **0** |
| `cmsvqt6l` | `DcGZEHko23J` | `DcGZEHko23J` | **true** | 200 | 89,916 | 4,667 | 28 | **undefined** | **5,769** | **false** | **0** |

The media object carries 576, 484 and 566 keys respectively. A recursive scan for any key naming a share returned, on every one of the three:

```
reshare_count = 86676          <- the count
media_repost_count = 1734      <- a second, different count
share_count_disabled = false   <- the platform saying the count is NOT hidden
can_viewer_reshare = true
```

`share_count`, `shares`, `reshare`, `repost_count` and `forward_count` are all `undefined`, which is presumably how the original assertion was reached: **the field exists under a name nobody probed.**

**`share_count_disabled = false` on all three is the decisive detail.** Instagram is explicitly stating the count is available. This is not a hidden-count case like BL-748's or BL-753's; it is an unread field.

### TikTok, LamaTok, 3 of 3

| clip | http | verdict | returned media id | live shares | **stored shares** | match | live views | stored views |
|---|---|---|---|---|---|---|---|---|
| `cmrvjd71` | 200 | ok | 7665191581833563405 | **62** | 62 | **yes** | 8,879 | 8,878 |
| `cmske3jg` | 200 | ok | 7671645884962082080 | **56** | 55 | **no, +1** | 9,909 | 9,902 |
| `cmr7guez` | 200 | ok | 7658749331758927117 | **11** | 11 | **yes** | 20,700 | 20,700 |

The key is **`shareCount`**, present on all three, read by `lamatok.ts:477`.

**The one mismatch is growth, not a defect, and it is checkable.** `cmske3jg` was last polled at `2026-08-23 13:21:45.887`, seven hours before the probe; its views also rose over the same interval, 9,902 to 9,909. A clip that gained 7 views gaining 1 share is the counter working.

### YouTube: NOT PROBED, and I am not claiming otherwise

**There is no `YOUTUBE_API_KEY` in this environment.** `grep -c "^YOUTUBE_API_KEY=" .env.local` returns **0**, and a case-insensitive grep for "youtube" over the whole file returns **0**. BL-753 found the same thing on 2026-08-09 and made the same disclosure. **No live YouTube call was made and none is claimed.** The YouTube conclusion rests on three things that are checkable without a key: the request at `youtube.ts:29` asks only for `part=statistics`; the documented `statistics` resource carries no share field; and 61,400 stored snapshots have never held a non-zero value. That is inference plus history, and it is labelled as such rather than dressed up as a measurement.

---

## PART 6 — THE VERDICT AND THE FIX SPEC

### One line per platform

**TikTok: shares ARE tracked today, correctly, from `shareCount` at `lamatok.ts:477`, and 3 of 3 probes matched storage.**
**Instagram: shares are NOT tracked, the provider returns `reshare_count` on every reel probed, and `hikerapi.ts:540-541` never reads it.**
**YouTube: shares are NOT tracked and CANNOT be, because the Data API exposes no share count; there is no fix and the surface should stop implying there is a number.**

### FIX SPEC, in dependency order. NONE OF IT WAS PERFORMED.

**A. Instagram, read the field. The whole defect is one missing extraction.**

1. `hikerapi.ts:540-541` — add a sibling to the likes and comments reads:
   `const shares = numericOrUndef(media.reshare_count ?? media.media_repost_count);`
   Probe order matters and `reshare_count` must come first: both were present on all three reels and they are **different numbers** (86,676 against 1,734 on `cmt095se`), so they are not aliases and picking the wrong one would understate by ~50x.
2. `hikerapi.ts:556`, `:585`, `:644`, `:659` — carry `shares` out of each branch beside `likes`, populating the `HikerResult.shares` field that has been declared and unassigned at `:71` since the file was written.
3. **`hikerapi.ts:936` and `:873` — replace the literal `0` with the read value**, and delete the three assertions at `:699`, `:936` and `apidojo.ts:681` that say Instagram has no share count. They are false and they are what stopped anyone looking.
4. `clipper-submit-core.ts:542` and `owner-submit-core.ts:193` — the same substitution on both submit paths, or the first snapshot of every new clip re-introduces the zero.
5. `apidojo.ts:681` and `:829` — currently unreachable behind `APIFY_HARD_OFF`, fix anyway so a future re-enable cannot restore the bug.

**B. YouTube, stop implying a number exists.** No fetch fix is possible. The honest change is at the display layer: the eleven surfaces in PART 4 should render **"not collected"** rather than **`0`** where the platform cannot supply one. The `Shares` option in `/admin/analytics` (`admin/analytics/page.tsx:116`) should either be removed or annotated per platform, because a flat zero line drawn from real SQL is the most convincing wrong answer on the list.

**C. The structural gap underneath both.** `ClipStat.shares` is non-nullable (`schema.prisma:1173`), so "not measured" can never be stored. Until that changes, no fix can make an Instagram zero mean anything, and the same blind spot applies to `likes` and `comments`. **This is a schema change on a 266,000 row hot table and it should not be bundled with A.**

### What must be proven before A ships

* **`reshare_count` id-matched on 50+ live reels** with zero mismatches, and the `reshare_count` against `media_repost_count` divergence characterised on all of them, so the right field is chosen on evidence rather than on three samples.
* **A hidden count is distinguishable from a real zero**, the BL-748 property: a reel with `share_count_disabled = true` must not produce a fabricated 0. Given the non-nullable column, the only honest options today are to skip the write or to carry a `shareSource` field the way `viewSource` already works.
* **No stored view, like or comment moves.** The change touches an object the tracking tick writes, so the other three fields must be asserted byte-identical on a sample before and after.
* **The tick budget is unchanged**: the field is read from a response already in hand, so no additional call, exactly as BL-746 established for the caption harvest.

### Historical repair: none is possible, and counting starts from now

**The data was never fetched, so there is nothing to recover.** Instagram's `reshare_count` is a **current** value with no history behind it: a backfill today would stamp every one of 4,499 clips with its August share count as though it had been measured at submission, which would corrupt the very signal the fix exists to restore. **Signal 9 compares a latest value to a peak across the series**, and a single synthetic point cannot form a series.

**So: no repair, and the first honest share reading for any Instagram clip is the first tick after the fix deploys.** A backfill would cost roughly 4,499 HikerAPI calls (~$4.50) and buy a number that is worse than absence. **I recommend against it.**

**No money is affected by any of this.** Shares are not an earnings input: `earnings = views / 1000 × cpm`, and `lamatok.ts:473-474` records that likes, comments and shares are deliberately not the earnings driver. **No clipper has been underpaid or overpaid by a cent because of this defect.** What it costs is evidence.

### Rollback

Each item in A is a single-file, additive read with no schema change and no data write. `git revert` the commit, or reset to the round's pre-tag. **Nothing to undo in the database**, because a reverted fix simply resumes writing the zero it writes today.

---

## AN ADJACENT FINDING, OUTSIDE THIS ROUND

**YouTube tracking has been dormant for eleven days.** Its newest snapshot of any kind is `2026-08-12 11:55:04.66`, against **666 active tracking jobs** on non-deleted clips whose `trackingJob.lastCheckedAt` peaks at `2026-07-26 12:10:13.071`. Instagram and TikTok were both polled within the last ten minutes of this round. **This is not a share problem and this round did not investigate it**, but it is why YouTube produced no row in the movement table, and it means no YouTube metric of any kind is currently updating. It deserves its own round.

---

## WHAT COULD NOT BE MEASURED

* **YouTube, live.** No API key exists in this environment, so no request was made and none is claimed. PART 5 states exactly what the conclusion rests on instead.
* **Whether `reshare_count` is a share count or a repost count.** Instagram exposes both on the same object and they differ by roughly 50x. Three samples establish that the field exists and is populated; they do not establish which of the two the owner would call a share. **That decision belongs to him and it must be made before the fix picks a field.**
* **How often Instagram sets `share_count_disabled = true`.** It was `false` on 3 of 3, so the hidden-count case was never observed and its frequency is unknown. It is the case the fix must handle without fabricating a zero.
* **Whether the 631 TikTok clips storing exactly 0 are genuine zeros or absent keys.** `shareCount` was present on 3 of 3 probes, but the `?? 0` at `lamatok.ts:477` makes the two indistinguishable in storage, so this cannot be settled from the database. It is the same non-nullable-column blind spot as PART 3.
* **No build was run and none is claimed.** This round changed one markdown file, in the reports repository, and cannot affect `tsc` or `next build`.

---

## ACCESSIBILITY

**No UI code was written or edited.** This round is an audit and its only artefact is this document, so there is no component, template, markup or user-facing string to review. Two pre-existing presentation defects are nonetheless reported above and belong to whichever round performs the fix: the literal `0` rendered for an unmeasured count on surfaces 1 through 8 and 10, which BL-748's own review already logged and deferred, and the selectable "Shares" analytics metric that draws a flat zero line with no indication the metric is uncollected on two of three platforms.

---

## VERIFICATION

Read only throughout: no code, data or config changed, nothing written to the database, every read through `scripts/run-select.js`, every timestamp cast `::text` against DB `now()`. PART 1 reports per platform how many live clips carry a share count above zero, exactly zero or no stat at all, alongside likes and comments on the same clips and through the same fetch, and measures movement across 7 days for every clip whose views rose, finding **1,858 Instagram clips gaining views with a maximum share gain of exactly 0** against TikTok's 12 of 148 moving; the owner's impression is confirmed for Instagram and YouTube and **corrected for TikTok, where shares work**. PART 2 traces the fetch per platform with file:line and names the loss point precisely: `hikerapi.ts:540-541` extracts likes and comments and never looks for a share field, `HikerResult.shares` at `:71` is declared and never assigned, and the literal `0` is substituted at `:936`, `:873`, `clipper-submit-core.ts:542` and `owner-submit-core.ts:193`. PART 3 establishes that an absent share count is stored as a **fabricated 0** on Instagram and YouTube, that `ClipStat.shares` is non-nullable so no third state exists on any platform, and that Instagram's fabrication is unconditional rather than conditional on a withheld field, which is worse than the two view-side cases BL-748 and BL-753 fixed. PART 4 enumerates eleven surfaces with what each renders, and corrects the brief's premise: BL-775's evidence panel does not read shares at all, but `fraud.ts` signal 9 does, it is live via `tracking.ts:219`, and its share arm is **structurally dead on 4,395 of 4,396 Instagram clips and 1,357 of 1,357 YouTube clips**. PART 5 probed 3 clips per platform through the real production readers with every id matched, found **`reshare_count` at 86,676, 37,919 and 5,769 with `share_count_disabled = false` on 3 of 3 Instagram reels storing zero**, matched TikTok storage on 3 of 3 with the single divergence explained as seven hours of growth, and discloses **18 provider calls of which 12 were my own waste from re-running the probe to read its output**. PART 6 gives a one line verdict per platform, a fix spec with file:line, what must be proven, the rollback, and states plainly that YouTube exposes no share count so no fix exists and that **no historical repair is possible or advisable, so counting starts from now**. No fix was performed. No Apify actor ran and none can. The worktree is removed. Handles redacted. **No dashes as bullets.**
