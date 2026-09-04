# BL-836: the clips page says 40 pending and shows none. The count is right and the list is wrong.

**2026-09-04 · DB `now()` = `2026-09-04 17:16:50.638588+00` (first read) to `2026-09-04 17:31:30.68907+00` (last) · AUDIT ONLY.**
Base `origin/main` @ `946c9fab`. Branch `checkpoint/BL-836`. Isolated worktree `C:/w836`, a short path, `node_modules` never junctioned, **removed at the end**. **NOTHING WAS CHANGED**: no code, no data, no config, no schema. Every request in this round is a GET. Every database read through `scripts/run-select.js`, every timestamp cast `::text` against DB `now()`. Handles redacted.

> ## CLIPPERS ARE FINE. A clipper still sees every one of their own clips, including the stuck ones: `/api/clips/mine` returned **32 rows carrying 7 PENDING** for a clipper who holds 6 of the stuck ones, and `ClipsPremium.tsx:66` filters the **complete** array before `:115` windows the render, so their "In review" chip is right. **THE HARM IS THE OWNER'S ALONE, AND IT IS NOT AN INCONVENIENCE: 41 real clips have been waiting since 2026-09-01 16:00:28.052, which is 73.5 hours, and he cannot reach them.**

> **THE DASHBOARD IS RIGHT AND THE LIST IS WRONG.** The dashboard counted **47 PENDING** by direct request; the database held **47 to 48** across the same minutes. The list showed the owner **4 of 46**.
> **THE STATUS FILTER IS A CLIENT SIDE FILTER OVER 30 LOADED ROWS.** It is never sent to the server. `/api/clips` has accepted `?status=` since 2026-05-13 and the page has never used it.
> **AND THERE IS A SECOND, SHARPER DEFECT UNDERNEATH IT.** `/api/clips` returns **HTTP 200 with an empty list** when its database query throws. Proven by direct request in PART 2.

---

## PART 0: WHAT IS REALLY PENDING, FROM THE DATABASE

| | measured |
|---|---|
| `clips` rows with `status = 'PENDING'`, `isDeleted = false`, at `17:31:30` | **48** |
| of those, in a campaign that is **not archived** (what the list could ever show) | **46** |
| soft deleted PENDING fixture rows (`bl815`, `bl821`, `bl825` x3), excluded everywhere | 5 |
| oldest live PENDING, cast `::text` | **`2026-06-27 16:07:07.146`** (archived campaign) |
| oldest live PENDING in a live campaign | **`2026-06-30 04:39:23.586`**, **66.54 days** old |
| the recent backlog: PENDING since `2026-09-01 16:00:28.052` | **41 clips**, oldest **73.5 hours** |
| newest PENDING at the last read | `2026-09-04 17:29:12.889`, minutes old |

**The count moved while I measured it, and that is the point rather than noise:** live pending read 44 at `17:16`, 47 at `17:28` and 48 at `17:31`. Clips are arriving and the owner is deciding the ones he can see.

### Which campaigns they sit in

| campaign | pending | oldest, `::text` |
|---|---|---|
| Zhus Meme (0.20 CPM) | 19 | `2026-09-02 15:14:32.985` |
| Zhus Edit (0.50 CPM) | 10 | `2026-09-02 15:43:47.757` |
| SomeSome App | 8 | `2026-09-01 16:00:28.052` |
| BAD BITCH ANTHEM (2.50 CPM) | 4 | `2026-06-30 04:39:23.586` |
| BAD BITCH ANTHEM (0.50 CPM) | 1 | `2026-08-10 17:41:43.215` |
| Deja Shoe **(archived)** | 1 | `2026-06-27 16:07:07.146` |
| WinGram **(archived)** | 1 | `2026-08-05 18:33:26.087` |

### At most one of his two numbers can be right, and it is the count

**The dashboard is correct.** `/api/clips?all=true&includeArchived=true&fields=summary`, asked as the real owner on the production build, returned **8,956 rows carrying 47 PENDING**, which is the database. His "roughly 40" is that figure.

**The list is wrong.** The same server, the same session, the same minute: the page the browser actually asks for returned **30 rows carrying 4 PENDING**, and the owner's Pending chip can only show him what is inside those 30.

**HE IS SEEING 8.7 PERCENT OF HIS PENDING QUEUE.**

### And the proof he has been reviewing throughout, so this is not neglect

Clips submitted **2026-09-03** are **117 approved and 15 rejected, zero pending**. Clips submitted **2026-09-04** are **79 approved, 5 rejected, zero pending** at the first read. His last decision before this audit was `2026-09-04 17:10:05.479`, eleven minutes before it started, and he made **157 approvals today**. **He decides everything that lands on page one and cannot reach anything below it.** The 41 clips from 1 and 2 September fell off page one within hours and have sat there since.

---

## PART 1: THE COUNT AND THE LIST ARE DIFFERENT QUERIES, AND THREE THINGS DIVERGE

### The count

| step | `file:line` |
|---|---|
| the fetch | `src/app/(app)/admin/page.tsx:48` · `/api/clips?all=true&includeArchived=true&fields=summary` |
| the where | `src/app/api/clips/route.ts:216` · `{ isDeleted: false }` and **nothing else**. No status, no limit, no archived exclusion, no date range |
| the count | `src/app/(app)/admin/page.tsx:96` · `filteredClips.filter(c => c.status === "PENDING").length` over **every clip on the platform** |

### The list

| step | `file:line` |
|---|---|
| the fetch | `src/app/(app)/admin/clips/page.tsx:637` `fetchPage` |
| what it sends | `:647` `dateFrom` · `:648` `dateTo` · `:649` `sortBy` · `:650` `limit = PAGE_SIZE` · `:651` `offset` · `:660` `campaignId` · `:661` `campaignIds` · `:668` `q` · `:674` `botSuspected` |
| **what it never sends** | **`status`.** `filterStatuses` (`:198`) appears in `fetchPage` **once**, at `:673`, and only to set `botSuspected` |
| the page size | `:323` · `PAGE_SIZE = 30` |
| the server where | `route.ts:217` `if (status) where.status` (never reached from this page) · `:341` `if (!includeArchived) where.campaign = { isArchived: false }` · `:868` `totalCount` over the same where |
| **the status filter** | `:884` to `:913` · **a client side `clips.filter()` over the 30 rows already loaded** |
| the campaign refine | `:915` · client side, a harmless no op because `:660` already scoped the server query |
| the control | `:1569` · the Status multi select |
| the message he reads | `:1745` · **"No clips matching filters."** |

### NAME THE DIVERGENCE

**DIVERGENCE 1, and it is the whole bug. The count queries the full set; the list filters 30 rows.** The server has accepted `?status=` since `route.ts:131`, added 2026-05-13, and applies it at `:217`. The page has never sent it. Every status view is therefore a sample of the newest 30 clips rather than an answer.

**DIVERGENCE 2. The list excludes archived campaigns; the count includes them.** `route.ts:341` drops every clip whose campaign is archived because the page does not send `includeArchived`, while `admin/page.tsx:48` does send it. Measured against the same server minutes apart: `?status=PENDING` reports `totalCount` **46**; adding `includeArchived=true` reports **48**. **Two real pending clips can NEVER appear in the clips list at any offset, on any filter, on any page size.**

**DIVERGENCE 3. The sidebar badge is a third number again.** `src/lib/sidebar-badges.ts:56` counts `{ status: "PENDING", updatedAt: { gt: cutoff } }` with **no `isDeleted` filter**, so the 5 soft deleted fixture rows are inside it. Three surfaces, three populations: badge 53, dashboard 48, list 46.

### The four things the brief told me to test specifically, each tested and each NOT the cause

| candidate | verdict | the evidence |
|---|---|---|
| a default date window | **NO** | `dateFrom` / `dateTo` default to `""` (`page.tsx:259-260`) and are only sent when set (`:647-648`); `route.ts:252` applies a range only when one parsed |
| a campaign restriction | **NO** | `filterCampaigns` defaults to `[]`, nothing is sent, and when it IS set it goes **server side** (`:660`, BL-269) |
| an offset past the end | **NO** | a reset always uses `offset = 0` (`page.tsx:644`), and every page walked from offset 0 to 450 returned a full 30 rows |
| reviewer scope leaking onto the owner | **NO** | every scope block is inside `if (role === "REVIEWER")`: `route.ts:401` self exclusion, `:422` reviewable statuses, `:441` the BL-89 date cutoff, `:386` invited only. **BL-833's new `CLIP_VIEW` check sits inside that same branch**, 30 insertions, and cannot reach an OWNER |

---

## PART 2: THE INTERMITTENCY. TWO MECHANISMS, AND THE SECOND ONE IS A SILENT FAILURE

### First, the measurement, reported before the conclusion

**68 list requests against the production build as the real owner. 0 empty. 0 non 200.**

| measurement | result |
|---|---|
| the exact page the browser asks for, 20 consecutive times | **20 of 20 populated**, 30 rows each, `totalCount` 7,868 every time |
| its timings | min **306 ms**, median **357 ms**, max **1,754 ms** (the first, cold) |
| offset 240, where the backlog sits, 12 times | **12 of 12 populated**, 14 PENDING each, min **292 ms** median **330 ms** max **932 ms** |
| 36 CONCURRENT requests in three waves of 12 | **0 non 200, 0 empty but 200**, worst wave median 689 ms, max 786 ms |

**SO A TIMEOUT WAS NOT REPRODUCED, AND I AM SAYING SO PLAINLY RATHER THAN ASSERTING ONE.** Nothing is cached either: `route.ts:34` is `force-dynamic` and every fetch carries `cache: "no-store"` (`page.tsx:676`). The stale response race is already handled correctly by `reqIdRef` at `:640` and `:705`.

### MECHANISM A, which needs no failure at all and explains the whole complaint

**The queue is newest first and the backlog is 250 rows down.** Row positions of every pending clip, computed against `ORDER BY "createdAt" DESC` over live rows, and then confirmed by walking the real endpoint page by page:

```
page  1  offset   0   30 rows   PENDING  3      <- only because 3 clips arrived in the last hour
page  2  offset  30   30 rows   PENDING  0
page  3  offset  60   30 rows   PENDING  0
page  4  offset  90   30 rows   PENDING  0
page  5  offset 120   30 rows   PENDING  0
page  6  offset 150   30 rows   PENDING  0
page  7  offset 180   30 rows   PENDING  0
page  8  offset 210   30 rows   PENDING  0
page  9  offset 240   30 rows   PENDING 15      <- the backlog starts here
page 10  offset 270   30 rows   PENDING 17
page 11  offset 300   30 rows   PENDING  2
page 12  offset 330   30 rows   PENDING  1
page 13  offset 360   30 rows   PENDING  1
page 14  offset 390   30 rows   PENDING  1
page 15  offset 420   30 rows   PENDING  0
```

**EIGHT PRESSES OF "Load more" BEFORE THE FIRST STUCK CLIP APPEARS, AND SEVEN OF THOSE PAGES SHOW HIM NOTHING.** Under a Pending filter those seven pages render as an empty screen, so the honest reading of what he sees while pressing is that there is nothing there.

**And that is why it is intermittent.** A newly submitted clip lands at **row 1**. The 30 second poll (`page.tsx:854`) and the SSE `clip_updated` handler (`:860` to `:872`) both call `fetchPage("reset")`, which re fetches page one. So a clip submitted while he waits **does** appear, within a minute, exactly as he describes. Measured: at `17:22` page one carried 3 PENDING and the newest was `2026-09-04 17:19:55.843`, four minutes old. Between `2026-09-02 17:54:22.813` and the next submission there was a **46 hour stretch in which page one carried no pending clip at all**, and no amount of waiting would have produced one.

**The poll also throws him back down the ladder.** `AUTO_REFRESH_MAX_OFFSET = 100` (`:331`), and the reset fires whenever `offsetRef.current <= 100` (`:854`). Offsets **30, 60 and 90 are inside that zone**, so three of the eight presses he must make can be undone by a tick that arrives mid climb.

### MECHANISM B: A DATABASE FAILURE IS RETURNED AS A SUCCESSFUL EMPTY QUEUE

**`src/app/api/clips/route.ts:884-888`:**

```ts
} catch (err: any) {
  console.error("GET /api/clips error:", err?.message);
  return richMode
    ? NextResponse.json({ clips: [], totalCount: 0, offset, limit, hasMore: false })
    : NextResponse.json([]);
}
```

**PROVEN BY DIRECT REQUEST, not by reading.** A request whose query throws inside that try block:

```
GET /api/clips?sortBy=newest&limit=30&offset=0&status=NOTASTATUS
  -> http 200  0.348 s  {"clips":[],"totalCount":0,"offset":0,"limit":30,"hasMore":false}
  -> server log:  GET /api/clips error:            (the message is EMPTY)
```

**An HTTP 200 carrying a well formed, genuinely empty page.** The browser cannot tell it from an empty queue, and neither can the page: `admin/clips/page.tsx:706` takes the rich branch and `:718` calls `setClips(next)` with `next = []`, then `:754` sets `totalCount` to 0. **BL-215 FIX B exists precisely to stop this** ("only clear the list on a GENUINE empty result", `:750-758`) and it is bypassed, because the route manufactures a genuine looking empty result out of a failure.

**AND THE FAILURE LEAVES NO TRACE ANYWHERE.** `SERVER_ERROR` audit rows are written by `instrumentation.ts:52`'s `onRequestError` hook, which only fires for an error that **escapes** the route. `/api/clips` catches its own, and `grep -c captureServerError src/app/api/clips/route.ts` is **0**, as it is across every route file. Measured: **27 `SERVER_ERROR` rows in 30 days and 0 of them name `/api/clips`.** So the rate at which this fires in production cannot be counted, and I am naming that as a measurement limit rather than estimating it.

**THE CONDITION THAT WOULD TRIGGER IT WAS LIVE IN PRODUCTION TODAY, AND IT IS NOT MINE.** Three `SERVER_ERROR` rows, all before my first database read at `17:16:50.638588`:

```
2026-09-04 17:12:47.048  /api/admin/sidebar-seen    "Too many database connections opened: sorry, too many clients already"
2026-09-04 17:13:43.377  /api/admin/sidebar-counts  "Too many database connections opened: remaining connection slots are reserved..."
2026-09-04 17:13:55.290  /api/admin/sidebar-counts  "(ECHECKOUTTIMEOUT) unable to check out connection from the pool after 15000ms"
```

**That is BL-814's shape and BL-816's own disclosed incident, live, on the owner's shell endpoints.** Any request that meets it on `/api/clips` blanks his entire list, tells him nothing, and recovers on the next 30 second poll. **That is the second half of "sometimes waiting a minute makes them appear."**

---

## PART 3: WHICH ROUND, DATED

**BL-816 is the round that made it bite. The defect it aggravated is older than it, and BL-816's own brief warned about exactly this.**

| round | merged | did it touch `admin/clips/page.tsx` or `api/clips/route.ts`? |
|---|---|---|
| `8e29f9c8` F-OWNER-CLIPS-FILTERS-SERVER | **2026-05-13** | **yes.** Introduced `PAGE_SIZE = 100` (from the API's `take: 500` default), `richMode`, and the swallow to empty catch. **Both defects are born here** |
| **BL-816** `0a37bb41` / merge `484e4d69` | **2026-08-21** | **yes.** `PAGE_SIZE` **100 to 30** at `page.tsx:323`. Nothing else in this diff touches the filter |
| BL-829 `96853d49` | 2026-08-25 | **no.** Neither file appears in the diff |
| BL-831 `c54b2d60` | 2026-08-29 | **no.** Its own report records `admin/clips/page.tsx` byte identical at `cf1e55c3e80f` |
| BL-832 `9e4a7849` | 2026-08-29 | **no.** Same blob OID recorded again |
| BL-833 `6d13c989` / merge `fdce6afd` | 2026-09-01 | `route.ts` **only**, 30 insertions, **entirely inside `if (role === "REVIEWER")`**. No owner effect |
| BL-835 `946c9fab` | 2026-09-04 | **no.** 0 of 40 changed files are under `admin/clips` or `api/clips` |

### Why 2026-05-13 was survivable and 2026-08-21 was not: the volume, measured

| | clips per day | how long a clip stays inside the visible window |
|---|---|---|
| 2026-05-13 to 2026-05-27, window 100 | **20.8 / day** | **4.8 days** |
| last 14 days, window 100 (what BL-816 removed) | **134.8 / day** (min 49, max 186) | **17.8 hours** |
| last 14 days, window 30 (what ships today) | **134.8 / day** | **5.3 hours** |

**BL-816 cut the owner's reach from a working day to one evening.** A clip he does not decide within about five hours is gone from every status view until he presses Load more eight times. The 41 stuck clips all crossed that boundary within hours of arriving on 1 and 2 September, and the oldest of them has now been unreachable for **73.5 hours**.

**BL-816's brief said this would happen.** It also carried a fix for the search half of it, and that half is still correct: search and totals genuinely query the full set, proven again in PART 4. The status filter was left client side on the written grounds that it "refines a small, already loaded set" (`page.tsx:1774-1779`). **That sentence was true at 500 rows, questionable at 100, and false at 30.**

---

## PART 4: WHAT ELSE IS HIDDEN

### Every status the owner can tick, measured against the truth

| chip | what the page shows him | the true total | he is shown |
|---|---|---|---|
| **Pending** | **4** | **46** | **8.7%** |
| **Flagged** | **0** | **5** | **0.0%** |
| Approved | 23 | 6,824 | 0.3% |
| Rejected | 3 | 994 | 0.3% |

**FLAGGED IS THE WORST OF THEM AND IT IS AT ZERO.** Five clips carry the fraud flagged status and **not one is inside the newest 30**, so the Flagged view is an empty screen that reads as "nothing is flagged". `page.tsx:904` also folds FLAGGED into the Pending chip, so both of the owner's two paths to a flagged clip are empty.

Approved and Rejected are the same defect, and the reason he has not noticed them is that the newest 30 rows are mostly approved, so those chips look plausible. They are not: the count under the list already tells him so, at `page.tsx:2737`, in a sentence he was never meant to need.

> *"The server found 7,868 before the filters on this page were applied."*

### BL-816's requirement still holds: search and totals ARE the full set

| | `limit=1` | `limit=100` | equal |
|---|---|---|---|
| `totalCount`, unfiltered | 7,868 | 7,868 | yes |
| `q=a` | 7,864 | 7,864 | yes |
| `q=zh` | 389 | 389 | yes |
| `q=tiktok` | 1,315 | 1,315 | yes |
| `q=instagram` | 5,852 | 5,852 | yes |
| `q=youtube` | 688 | 688 | yes |

**Search reaches a stuck clip.** Pasting a stuck clip's own URL fragment returned exactly **1 row, `totalCount` 1, status PENDING**. So does the campaign filter, because BL-269 made it server side:

| campaign selected | PENDING on ITS page 1 | true pending in it |
|---|---|---|
| Zhus Edit (0.50 CPM) | **10** | 10 |
| SomeSome App | 3 | 11 |
| Zhus Meme (0.20 CPM) | 1 | 20 |
| BAD BITCH ANTHEM (2.50 CPM) | 1 | 4 |

**THOSE ARE THE TWO WORKAROUNDS UNTIL THIS IS FIXED:** select a campaign, which narrows the server query, or paste a clip URL. Neither reaches the two clips in archived campaigns.

### The clipper facing list, checked because BL-829 changed it

**Clippers can see their own clips and nothing is hidden from them.** `/api/clips/mine` returned **32 rows carrying 7 PENDING** for a real clipper holding 6 of the stuck ones, and `?fields=summary` returned the same 32 and the same 7. BL-829 windowed the **render**, not the data: `ClipsPremium.tsx:66-69` computes `visible` from the **complete** array and `:115` slices only what is drawn, so the four chip counts at `:56` and the submission gate at `clips/page.tsx:186` still read every row. **The owner's defect is the opposite choice made on the other page.**

**One thing they share, and it should be fixed with it:** `src/app/api/clips/mine/route.ts:422-423` carries the **same** swallow to empty catch. A pool failure blanks a clipper's own clips page and tells them nothing either.

---

## PART 5: THE VERDICT, AND THE FIX

> **THE OWNER'S STATUS FILTER IS A CLIENT SIDE FILTER OVER THE 30 ROWS ON SCREEN AND HAS NEVER BEEN SENT TO THE SERVER, SO SINCE BL-816 SHRANK THAT PAGE FROM 100 ROWS TO 30 ON 2026-08-21 HE HAS BEEN SHOWN 8.7 PERCENT OF HIS PENDING QUEUE AND 0 PERCENT OF HIS FLAGGED ONE, WITH 41 REAL CLIPS UNREACHABLE FOR 73.5 HOURS.**

### The fix, four changes, none of which costs a measured performance gain

**1. Send the status filter to the server.** `admin/clips/page.tsx:637` `fetchPage`, beside `:660`: send the selected real statuses as a CSV, folding FLAGGED in whenever PENDING is selected so `:904`'s rule moves with it. `api/clips/route.ts`, beside the `campaignIds` block at `:228`: accept `statuses` and set `where.status = { in: [...] }`. Leave the client refine at `:884` in place as a no op, **exactly the shape BL-269 used for campaigns**, so nothing else on the page has to move. The three virtual chips (`HELP_REQUESTED`, `CLIENT_FLAGGED`, `BOT_SUSPECTED`) stay client side or keep their existing server flags; they are OR combined and must not narrow the server query.

**2. Stop the catch lying.** `api/clips/route.ts:884-888`: return **503 with `{ error: ... }`** instead of an empty page, and call `captureServerError` so the failure reaches `audit_logs` like every other route's does. The page already handles this correctly and **preserves the rows it has** (`page.tsx:756-770`). Apply the same change to `api/clips/mine/route.ts:422-423`.

**3. Decide the archived question, because two numbers currently mean different things.** Either send `includeArchived` on the owner's list, or drop archived clips from the dashboard count. **This is the owner's call, not mine**, and it is 2 clips today. It is named rather than chosen.

**4. `sidebar-badges.ts:56`: add `isDeleted: false`,** so the badge stops counting 5 soft deleted test fixtures.

### What must be proven before it is accepted

* The Pending chip's rendered row count equals `totalCount` for that narrowing, **at page size 30 and at 100**, and the same for Flagged, Approved and Rejected. Flagged must return **5**.
* The 41 stuck clips are reachable **on page one** under the Pending filter, by id.
* Stitched pages under a status filter equal the unfiltered set row for row, the BL-816 and BL-829 method, because pagination fails by a row going missing.
* A forced database failure returns a **non 200** and the list **keeps its rows**, with an audit row written.
* Search totals unchanged at `limit=1` and `limit=100` for the five terms above; the campaign filter unchanged; `/api/clips/mine` unchanged.
* The 6 money files plus `tracking.ts` byte identical by blob OID. **No clip approved, rejected or undone by the fixing round.**

### The trade off, stated rather than chosen silently

**There is no trade off against BL-816 or BL-829, and I want to be exact about why.** Sending the status filter **narrows** the `WHERE`, so the query gets cheaper rather than dearer: `?status=PENDING` measured **298 ms** against **293 ms** unfiltered, and `?status=FLAGGED` returned all 5 rows in one page. **No page size change is needed and none is proposed**, so BL-816's 334 requests to 51 and 12.4 s to 4.0 s stand untouched, as does BL-829's 26,153 DOM nodes to 2,371. The 503 change costs one audit write on a request that already failed.

**If an index is later wanted for `clips(status, "createdAt")`, measure first.** BL-642's HOT update tax is an argument about putting **`earnings`** in an index and does not automatically apply to `status`, but `clips` runs 92.2% HOT updates and that is not a thing to spend on a guess. The measured 298 ms says none is needed today.

**The one thing that WOULD cost the performance gain is raising `PAGE_SIZE` back to 100**, and it should not be done: it would buy 17.8 hours of reach instead of 5.3 and would still hide the rest. **Accuracy is bought here by asking the server the right question, not by loading more rows.**

### Rollback

All four changes are local and additive. `git revert -m 1 <merge>`, or `git reset --hard pre-BL-836`. **Nothing in the database to undo**, because nothing is written.

**NO FIX WAS PERFORMED. This round changed nothing.**

---

## SAFETY AND WHAT COULD NOT BE MEASURED

| | |
|---|---|
| changes made | **none.** No code, data, config or schema. `git status` in the worktree shows only the three probe scripts and this report |
| requests made | **every one a GET.** No approve, reject, flag, undo, track now or POST of any kind |
| clips, payouts, earnings | **nothing created, modified or deleted by this round** |
| the 6 money files, `tracking.ts` | **not read into any diff and not touched** |
| server | a local production build (`npm run build` exit **0**, `grep -c "error TS"` = **0**, hooks gate **0 errors and 11 warnings** at the ceiling) on port 3836 with `DEV_AUTH_BYPASS=false`, real minted Auth.js sessions, **stopped at the end** |
| worktree `C:/w836` | **removed** |

**WHAT COULD NOT BE MEASURED, AND IT MATTERS:**

* **How often MECHANISM B actually fires in production.** It writes no audit row, no Sentry event and an empty log line. It cannot be counted from here, only from a fix that starts recording it. **That is the strongest single reason to make change 2 even though change 1 is the bigger bug.**
* **Production timings.** Everything was measured against a local production build pointed at the production database. The request census, the row counts and the `totalCount` figures are exact; the wall clock numbers are local.
* **The failure in a real browser.** The list, the count and the empty result are proven at the endpoint the browser calls, with the page's exact parameters and the page's own filter logic read line by line. A screenshot of the empty screen was not taken.
* **A moving target.** Live traffic changed the pending count three times during the audit (44, 47, 48). Every figure carries the read that produced it.

**THE POOL PRESSURE AT `17:12` TO `17:13` IS NOT MINE.** It precedes my first database read at `17:16:50.638588`. My own reads were short and sequential and the local server ran for roughly nine minutes.
