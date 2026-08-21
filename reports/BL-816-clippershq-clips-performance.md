# BL-816 — the clips page is fast now, and not one number moved

**2026-08-21 · DB `now()` = `2026-08-21 16:21:04.700503+00` (first read) to `17:35:32.607639+00` (last) · BUILD AND MERGE.**
Base `origin/main` @ `7f97dd0f`. Branch `checkpoint/BL-816` @ `0a37bb41`. **Merged and verified pushed: `origin/main == local == 484e4d69`.** Tags `pre-BL-816`, `post-BL-816`, `pre-BL-816-merge`, `post-BL-816-merge`, all on origin. Isolated worktree `C:/w816`, a short path, `node_modules` never junctioned, **removed at the end**. Every read through `scripts/run-select.js`, every timestamp cast `::text` against DB `now()`. Handles redacted, no wallet address read or printed.

**A REDEPLOY ON RAILWAY IS REQUIRED BEFORE ANY OF THIS IS LIVE.**

> **THE HEADLINE: 334 requests and 12.4 seconds became 51 requests and 4.0 seconds, and every displayed figure is byte-identical.**
> **AND THE DIAGNOSIS WAS HALF RIGHT. The page size of 100 is real. The row count is NOT the dominant cost.**

---

## PART 0 — MEASURED FIRST, AND THE MEASUREMENT NAMES SOMETHING ELSE

### What one page load actually does

Measured in a real browser, every request recorded, at 1440px as OWNER.

| | before |
|---|---|
| total requests for ONE page load | **334** |
| of those, `/api/admin/review-evidence/<clip>` | **200** (100 distinct; doubled by React StrictMode in dev, so **100 in production**) |
| of those, `/api/admin/reviewer-note/<clip>` | **84** (42 distinct) |
| the clips list query itself | **3 requests** |
| time until every distinct request had been answered | **12,442 ms** |

**228 of the 334 requests are per-clip cards.** `ReviewEvidencePanelMount` (BL-776) is mounted on EVERY row and fetches on mount; `ReviewerNoteCard` (BL-666) is mounted on every PENDING row and does the same.

### The cost of one of those cards, at the database

`scripts/bl816-probe-queries.ts`, counting the queries Prisma actually emits:

```
/api/clips list query, limit 100 (what ships today)
    wall 377 ms | 9 queries | 1,241 ms in the database
/api/clips list query, limit 30
    wall 166 ms | 9 queries |   373 ms in the database
/api/clips totalCount
    wall  44 ms | 1 query   |    43 ms
review-evidence for ONE clip
    wall  99 ms | 3 queries |   127 ms in the database
JSON payload: limit 100 = 144 KB, limit 30 = 42 KB
```

**Three queries per clip. At 100 rows that is 300 queries and about 12.7 seconds of database time**, against 10 queries and 1.28 seconds for the list itself. **The per-row panel is 91% of the database work on the page.**

And in the browser it is worse than the database time suggests, because a browser opens six connections per origin: **measured average 12,824 ms per evidence request against roughly 300 ms in isolation.** They queue.

### Every candidate the brief named, tested rather than assumed

| candidate | verdict | the number |
|---|---|---|
| A query returning far more rows than are displayed | **NO** | the list returns exactly `limit` rows |
| Server-side N+1 (a query per clip) | **NO** | Prisma expands the nested select into a **FIXED 9 queries** at any page size |
| **A per-clip computation** | **YES, THIS IS IT** | 3 queries per row, 300 per page, 12.7 s |
| A missing index on what search filters by | **NO** | `q=a` at limit 100 measured **581 ms against 690 ms** without it. Search is not slower |
| The payload being large regardless of row count | **secondary** | 144 KB at 100, 42 KB at 30, 181 KB on the wire |
| Anything near Prisma's 5,000 ms budget | **YES, ONE THING** | `sortBy=views_desc`, below |

**So pagination alone would NOT have fixed it, and I am saying so plainly.** Cutting to 30 removes 70% of the per-row storm as a side effect, but the storm itself is the defect. The fix is batching; the page size is the smaller half.

### The one thing near the 5,000 ms budget BL-814 was opened for

`sortBy=views_desc` at limit 100 measured **1,779 ms, 2,680 ms and 4,981 ms** across three runs.

BL-269 built it in three phases so the complex Prisma `where` is reused verbatim, and phase B binds **one parameter PER ID**. Today that is 6,918 placeholders in one statement — and **the statement text therefore changes every time a clip is created**, so Postgres parses and plans a brand-new 6,918-parameter statement on essentially every request and can never reuse a plan.

```
limit 100 offset 0
  TODAY: IN-list with 6,918 bind parameters      avg 1,439 ms   runs 4,021, 160, 137
  CANDIDATE: = ANY($1::text[]), ONE parameter    avg   129 ms   runs   131, 127, 129
  IDENTICAL PAGE AND ORDER: YES
limit 30 offset 0    IDENTICAL PAGE AND ORDER: YES
limit 30 offset 90   IDENTICAL PAGE AND ORDER: YES
```

**4,021 ms cold becomes 131 ms, and there is no cold case left because the statement text is now stable.** Over HTTP the sort went from **3,147 ms average to 866 ms**.

---

## PART 1 — THE FIX, AND WHY IT CANNOT MOVE A NUMBER

**1. One batched request for the page, instead of one per row.** Two new routes, `POST /api/admin/review-evidence/batch` and `POST /api/admin/reviewer-note/batch`, behind the identical `requireOwnerOrCapability("CLIP_VIEW")` gate, doing the identical work for a page of ids in **three queries instead of three per clip**.

**THE ACCURACY GUARANTEE IS STRUCTURAL, NOT A TEST.** The arithmetic was lifted out of the fetch, character for character, into `computeClipperHistory` and `computeViewArrival`, and the single-clip route now calls **the same two exported functions on the same rows**. There is one implementation, so there is nothing to disagree with. The proof in PART 4 is confirmation, not the mechanism.

**2. `PAGE_SIZE` 100 to 30**, which is the owner's own number. **Why 30:** below about 25 the load boundary falls inside the first screen at 1440px, so he would meet it while still reading page one; 100 is what he is complaining about. The list query falls from **377 ms to 166 ms** and its database time from **1,241 ms to 373 ms**.

**3. `= ANY($1::text[])` on the views_desc ordering**, as measured above.

**4. `?fields=summary` on two endpoints the Dashboard uses** — PART 3.

### What was REJECTED, and why

* **A cache, of any TTL.** BL-642 recommends exactly this for `/api/campaigns/spend` and is right there, because that endpoint feeds no decision. This page is where clips are approved and money moves. **Rejected: the brief forbids a stale read and so do I.**
* **A materialised or incrementally maintained aggregate for the Dashboard totals.** It drifts the moment any writer forgets it, and a drifted money figure is the bug class that has cost this platform weeks. **Rejected.**
* **A covering index carrying `earnings`.** BL-642 measured the price: `clips` runs **92.2% HOT updates**, and putting `earnings` in an index converts roughly 228,000 of them to non-HOT, taxing `writeClipEarnings` itself. **Rejected, and after the bind-parameter fix no index is needed at all.** No index was created and none is proposed.
* **Gating the evidence panel to PENDING clips only.** It would have removed information the owner sees today on APPROVED and REJECTED rows. **Rejected: that is a display change wearing a performance costume.**
* **Lazy-mounting the panel on scroll.** This was my own first design and the accessibility review rejected it in favour of batching. It buys less and costs six new hazards on money buttons. **Rejected on the review's reasoning, which was better than mine.**

### Search, filters and the count

**The count the owner sees is the TRUE total, not the loaded count**, and every filter still queries the whole set server-side. Proven in PART 4: `totalCount` reads **5,833** at limit 30 and at limit 100; four search terms and four status filters report identical totals at both page sizes.

---

## PART 2 — PROVEN ON A ROW THAT ARRIVED BY SCROLLING

That is where a naive pagination breaks, so it is proven there specifically. **Nothing was mutated:** no clip approved, rejected or undone.

`scripts/bl816-verify-lazy-row.mjs` — **12 passed, 0 failed:**

```
PASS  the first page renders about 30 rows, not 100          30 row containers
PASS  a real Load more button exists
PASS  pressing it appends a second page                      30 then 59
PASS  the append is announced once, with the MEASURED delta  "29 more clips loaded. Now showing 59."
PASS  the evidence panel was asked about the APPENDED rows in a SECOND batch
                                                             2 batch requests, sizes 30, 29
PASS  the second batch asked ONLY about the new rows
PASS  BL-776's evidence panel rendered ON that lazily loaded row
PASS  the appended row carries its own action controls       undo 1
PASS  a third page appends as well                           59 then 89
```

Note the announcement says **29**, not 30: the dedup added 29 rows and the announcement reports what actually arrived.

`scripts/bl816-verify-lazy-actions.mjs` — **10 passed, 0 failed**, on `cmt2y3j8a0cko0xpmqg4r0fkb` (page 3) and `cmt31lwbh0dic0xpmot3vckrg` (a PENDING clip on page 2):

```
PASS  BL-776 evidence for an appended clip is identical through the batch and the single route
PASS  BL-736's picker answers for an appended clip                    14 destinations
PASS  and its hard blocks still refuse, by code
        DEST_PAST, DEST_PAUSED, DEST_PLATFORM_NOT_ACCEPTED, SAME_CAMPAIGN
PASS  every refused destination still carries a REASON, not just a code
PASS  BL-744's four rate figures are still on the response for the OWNER
PASS  BL-815: a REVIEWER without the capability is still refused       HTTP 403
PASS  BL-815: and his POST is refused too, so nothing moved            HTTP 403
PASS  BL-814's review route is reachable and refuses an invalid action rather than the caller
        HTTP 400 {"error":"Invalid action"}
PASS  the appended clip's row is byte-identical when fetched alone at its own offset
```

**Approve, Reject and Undo were proven present and reachable, never pressed.** Pressing Approve on a real clipper's clip to demonstrate a button would have moved money, and the round forbids it. The review route is proven reachable for an appended clip by its refusing an invalid ACTION with a 400 rather than refusing the CALLER.

---

## PART 3 — THE DASHBOARD IS A DIFFERENT PROBLEM, NAMED AND FIXED

**First, the right page.** The owner's "Dashboard" is **`/admin`**, not `/dashboard` — the sidebar's OWNER entry points there, and `/dashboard` is the clipper one. I measured the wrong page first and say so.

`/admin` fetches **every clip on the platform** and **every ClipAccount row**, then aggregates them in the BROWSER to produce a clip count, a distinct-clipper count, three status counts and two sums. Measured in isolation:

| | before | after | |
|---|---|---|---|
| `/api/clips?all=true&includeArchived=true` | **10.9 s / 10.5 s**, **12,762,518 B** | **0.53 s / 0.40 s**, **1,288,875 B** | **24x faster, 90% smaller** |
| `/api/accounts` | **4.4 s**, **27,761,504 B** | **0.42 s**, **119,040 B** | **10x faster, 233x smaller** |

**It is a DIFFERENT cause from the clips page** — over-fetching plus client-side aggregation, not a per-row request storm — and it is fixed rather than half-fixed. The Dashboard reads exactly **six** fields off a clip (`id`, `userId`, `campaignId`, `status`, `earnings`, `createdAt`) and **one** off an account (`status`), counted from its source. An opt-in `?fields=summary` returns those, straight from the column, unrounded. **The client-side arithmetic is untouched**, which is what makes it accuracy-neutral by construction.

**Opt-in, so nothing else moves.** `/admin/flags` and the analytics page also pass `all=true` and both read the full clip shape; narrowing `all=true` itself would have broken them silently. **ANALYTICS WAS NOT TOUCHED**, as the owner asked.

**A pre-existing Dashboard defect found and deliberately NOT repaired.** Its campaign filter reads `a.campaignAccounts`, which `/api/accounts` **has never returned**, so the filtered account counts are already empty today. Repairing it would CHANGE a number the owner sees, which this round may not do. It is asserted as identically-empty in both shapes and reported.

---

## PART 4 — THE SPEED, AND THEN THE ACCURACY

### Speed, same method both sides, same server, both warm

A dev server compiles each route on first request, and those 3-to-7-second compiles swamp a measurement while the owner on Railway never pays them. So both figures below are the SECOND load in the same browser, with every route already compiled, and the BEFORE was taken by stashing the diff on the same running server.

| /admin/clips as OWNER | BEFORE | AFTER |
|---|---|---|
| **time until every distinct request was answered** | **12,442 ms** | **4,042 ms** |
| **total requests** | **334** | **51** |
| review-evidence requests | 200 (100 distinct) | **0** — one batch |
| reviewer-note requests | 84 (42 distinct) | **0** — one batch |
| list query, warm, in isolation | 690 ms | **394 ms** |
| list query database time | 1,241 ms | **373 ms** |
| `sortBy=views_desc`, limit 100 | 3,147 ms avg, **4,981 ms peak** | **866 ms**, no peak |
| 51 clips of evidence | **16,062 ms** one at a time | **479 ms** batched |

**3.1x faster to ready, 6.5x fewer requests, and the 4,981 ms spike near Prisma's budget is gone.**

### Accuracy — `scripts/bl816-verify-accuracy.mjs`, 55 passed, 0 failed

Every Dashboard figure, computed by running the page's own aggregation over BOTH payloads, summed as **integer cents** so float addition order cannot move it:

```
PASS  dashboard total                  6921 vs 6921
PASS  dashboard uniqueClippers          309 vs 309
PASS  dashboard pending                  36 vs 36
PASS  dashboard approved               5700 vs 5700
PASS  dashboard flagged                   6 vs 6
PASS  dashboard rejected               1179 vs 1179
PASS  dashboard earningsCents       1389675 vs 1389675
PASS  dashboard approvedEarningsCents 1378227 vs 1378227
PASS  dashboard oldestCreatedAt / newestCreatedAt / idFingerprint   identical
PASS  ...and all eleven again WITH A CAMPAIGN SELECTED
PASS  every clip present in both payloads                  0 missing
PASS  every one of the six fields byte-equal on every clip 0 mismatched across 6,921 clips
PASS  accounts total 1295 / pending 101 / approved 1159 / rejected 35 / same id order
```

The clips list, at both page sizes:

```
PASS  four pages of 30 stitch to the same 100 ids, in the same order
PASS  every stitched row is BYTE-IDENTICAL to its limit-100 row      0 differing rows
PASS  totalCount is the TRUE total, not the loaded count             5,833 at both
PASS  search "a" 5,828 · "zh" 254 · "instagram" 3,908 · "tiktok" 1,223 — same total at both sizes
PASS  status PENDING 34 · APPROVED 4,965 · REJECTED 829 · FLAGGED 5 — same total at both sizes
PASS  views_desc: four pages of 30 stitch to the same 100 ids in the same order
PASS  views_desc: still ordered by latest-stat views     top five 12,139,743 · 2,500,000 · 1,984,334 · 1,500,000 · 1,100,000
```

The evidence panel — `scripts/bl816-verify-evidence.mjs`, **20 passed, 0 failed**, on a **51-clip sample spanning 5 campaigns and all four statuses**:

```
PASS  every clip's evidence is BYTE-IDENTICAL between the two endpoints   51/51
PASS  available · reason · platform                                       identical on all 51
PASS  history.submissions · rejections · rejectionsMentioningBoughtViews  identical on all 51
PASS  history.rejectionRatePct · mostRecentBoughtViewRejectionAt          identical on all 51
PASS  history.rawReasons · history.unavailable                            identical on all 51
PASS  arrival.viewsNow · pctBy6h · pctBy24h · pctBy72h                    identical on all 51
PASS  arrival.snapshotCount · trackedHours · unavailableReason            identical on all 51
PASS  a clip that does not exist answers identically through both paths
PASS  the batch route refuses a CLIPPER exactly as the single route does  batch 403, single 403
```

**Seventeen figures, compared one at a time, so a failure would have named which number moved.** None did.

---

## PART 5 — RENDERED, AT FIVE WIDTHS, WITH THE VIEWPORT MEASURED

`window.innerWidth` is printed beside every shot, because a prior round claimed four widths the browser never rendered. **20 shots of the queue plus 5 of the end-of-list state, ALL at the asked width.**

```
queue-top / load-more-control / after-scroll-load / after-more-presses
  320 · 375 · 414 · 1280 · 1440    measured == asked, every one
end-of-list  320 · 375 · 414 · 1280 · 1440   measured == asked, every one
```

**Scroll-to-load works on a phone**, driven by a real scroll rather than a button, at every width: `30 rows then 60` at 320 and 375, `30 then 90` at 414, 1280 and 1440.

**Loading more is obvious rather than looking like the list has ended, and the two are different ELEMENT TYPES, not different colours** — `--text-primary`, `--text-secondary` and `--text-muted` are all `#ffffff` in this theme, so a colour difference would be no difference. Seen at 375px: more-to-come is a bordered accent pill reading **"Load more clips"**, which becomes **"Loading more clips"** while in flight; the end of the list is inert prose beneath a visible `--border-strong` rule reading **"That is the end of the list. You are seeing the only clip that matches."**

**BL-739's drawer guard holds, probed with the drawer actually OPEN.** The first probe fired with it closed and proved nothing, so it was redone:

```
PASS  with the drawer CLOSED the page scrolls normally                    defaultPrevented=false
PASS  with the drawer OPEN the single-finger touchmove is prevented       defaultPrevented=true
```

`app-layout.tsx` is **byte-identical by blob OID** (`85f8aa1a`), so the guard could not have been changed; the probe is there so the claim rests on a measurement.

---

## THE ACCESSIBILITY REVIEW CHANGED THE DESIGN, NOT JUST THE DETAILS

Run before any UI was written, lead plus six specialists.

**It rejected my Change B outright and was right.** I proposed lazy-mounting the evidence panel on visibility. Two specialists independently reached the same conclusion: **batch the endpoint instead.** Batching removes more work (100 requests to 1, ~150 queries to 3), keeps the panel eagerly mounted, and needs **zero** new accessibility mitigations, where deferral would have created six new hazards next to the Approve and Reject buttons — including find-in-page failing *self-sealingly*, because a React `null` contributes no text, so nothing matches, so nothing scrolls, so the observer never fires, so a reviewer sweeping for "Could not load measurements" would get zero hits and read it as zero failures. **That is what shipped.**

**Five blocking items, all implemented:**

1. **The observer can stall PERMANENTLY.** With a client-side filter active a page of 30 can yield zero visible rows; the sentinel never moves, no threshold is crossed, and its effect deps never change, so no further callback is ever delivered. At 100 that was rare; at 30 it is routine. **A real Load more button is the deterministic escape**, and it is also the only way to operate this 231 times without a scroll gesture. It comes FIRST, with a 1px `aria-hidden` sentinel below it.
2. **`loadingMoreRef` was read during render.** It is a ref: mutating it schedules no render, and it is cleared in a `finally` that runs before the `setClips` batch flushes, so `"Loading more..."` was **unreachable**. A `loadingMore` STATE now backs the label; the ref stays as the synchronous pre-await race guard. The 375px render shows the label reading "Loading more clips", which it could never do before.
3. **The terminal block unmounted and destroyed focus.** The sentinel and the end-of-list line were mutually exclusive, so the moment the last page landed the element holding focus vanished and focus fell to `<body>`, thousands of rows above where the owner was. **One persistent wrapper now, `min-h-[104px]`, contents swapped, and `aria-disabled` rather than `disabled`** because `disabled` blurs the focused element and reintroduces the same failure.
4. **No append announcement.** A persistently mounted, empty, page-level `role="status"` now carries the **measured** delta and the running total, debounced 500 ms, written **only** from the append branch. It does not reopen what BL-776 closed: it is page-level, it carries a count rather than a person, and nothing announces on a filter change, on the poll or on first load.
5. **Target size.** `py-8` is wrapper padding and gave the control nothing; the button carries `min-h-[44px] px-5` and **no `focus:` utilities**, so the global `*:focus-visible` indicator survives.

**It corrected four of my premises, and I was wrong on all four.** Screen-reader users CAN trigger an IntersectionObserver (browse-mode cursor movement scrolls the container). The sentinel's `rootMargin: 200px` **has never worked**, because the target sits inside an `overflow-y-auto` `<main>` and intermediate clip rects are applied unexpanded. The panel's empty sentence is **three lines at 375px**, not one. And the 306 requests included StrictMode's doubling, so production is ~100.

**Also actioned:** `AUTO_REFRESH_MAX_OFFSET` decoupled from `PAGE_SIZE`, so shrinking the page did not silently shrink the self-refreshing zone from 100 rows to 30; and `ReviewerNoteCard`'s header comment corrected, which claimed an `h4` sat "under the row's h3" when the page has exactly one heading and `note.headline` is a `<p>`. **The heading skip itself is pre-existing and filed, not repaired here** — the fix is an `sr-only h2` per row and that is its own change.

**Reported, not fixed:** the heading vacuum (one `h1` for N rows); `--bg-page` referenced in `ReviewerNoteCard` while `globals.css` defines `--bg-primary`; no skip link in the app shell; `Button` emitting no `aria-busy` while loading.

---

## MERGED AND PUSHED

| | |
|---|---|
| clean `tsc` baseline on the untouched worktree, **before any edit** | `npm ci` exit **0**, `npx prisma generate` exit **0**, `npx tsc --noEmit` exit **0**, `grep -c "error TS"` = **0** |
| branch | `checkpoint/BL-816` @ **`0a37bb41`**, VERIFIED on origin |
| merge commit | **`484e4d69`**, `origin/main` verified by `git ls-remote` |
| conflicts | **none**; main never moved from `7f97dd0f`, and the **merged tree OID equals the branch tree OID exactly** (`1d466db3`) |
| BACKLOG | **159 sections before, 160 after**, `BL-816` x1, **0 conflict markers**, counted with `grep -c`, never piped to `head` |
| **`checkpoint/BL-723`** | **confirmed NOT an ancestor of main** |
| files | 22 changed, **10 of them source** |
| worktree `C:/w816` | **removed**, 0 node processes left behind |

**Ten source files is above the five-file threshold**, so the plan is stated rather than assumed: two batch routes, one shared provider, the two card components that read from it, the shared library the arithmetic moved into, the clips page, the clips API, the accounts API and the Dashboard page.

> **A REDEPLOY ON RAILWAY IS REQUIRED.** Main carries the fix; production still loads 100 rows and fires a request per row.

---

## SAFETY

| | |
|---|---|
| the 6 money files plus `tracking.ts`, `campaign-era.ts`, `apify.ts`, `payout-calc.ts`, `cpm.ts`, **`campaign-reassign.ts`**, **`app-layout.tsx`** and **`ReviewEvidencePanel.tsx`** | **byte-identical by blob OID on BOTH refs**: `ac5be7de`, `797e2098`, `e887f80a`, `83ce4bab`, `61cef393`, `ef5cdae7`, `106e16ad`, `656bf4c0`, `029834b4`, `57240872`, `3e513702`, `85f8aa1a`, `dd97601e` |
| schema | **no change**, no `prisma migrate`; `prisma generate` only |
| indexes | **none created.** The one that would have helped was made unnecessary by the bind-parameter fix, and BL-642's HOT-update tax stands as the reason not to add one anyway |
| payouts | **187 rows, fingerprint `fce9ee20…` identical, 0 with an `updatedAt` inside the round window** |
| earnings invariant | **0 violations** before and after |
| clip status or earnings changed by this round | **none.** Clips 6,985 to 7,015 and approved earnings $10,175.84 to $10,180.03 are live submissions and the tracking cron |
| Apify | **no actor run**; the 11 BL-678 guards untouched |

---

## DISCLOSED, BECAUSE MY OWN WORK CAUSED IT

**MY DEV SERVER EXHAUSTED THE DATABASE CONNECTION POOL AND IT REACHED THE OWNER'S LIVE SESSION.**

**Nine `SERVER_ERROR` rows on his account between `17:08:42` and `17:13:17`** — four on `/api/admin/sidebar-counts`, two on `/api/admin/sidebar-seen`, two on `/api/profile/avatar`, one on `/api/earnings` — seven of them naming a connection failure. At one point even a read-only `SELECT` was refused with *"remaining connection slots are reserved for roles with the SUPERUSER attribute"*.

**And one `BUDGET_PROBE_BYPASS` at `17:17:42` on clip `cmt36xkgp0epr0xpmguka1rrd`**, carrying the expired-interactive-transaction error — **the exact shape BL-814 was opened for**, on the owner's own account, in my window.

**That transaction rolled back completely, verified rather than assumed:** the clip reads `PENDING`, earnings `0`, base `0`, bonus `0`, invariant gap `0`, and `updatedAt 2026-08-21 16:55:43.921`, which is **before** the failure. Nothing was left half-written, which is precisely what BL-814's single transaction guarantees.

**Why it happened.** Production alone sits at **62 open connections** (measured with my server dead), and the app's pool is `max: 48` per process, so a second pool on the same database is what pushed it over. **Measurement timings taken inside that window were discarded rather than reported**, which is why the before/after figures in PART 4 were re-taken on a healthy pool with the diff stashed and unstashed on the same server.

**Also in the window and NOT mine:** two `APPROVED_CLIP` rows at `17:07:00` and `17:14:28`, the owner working in production, and two Discord rows from live traffic. Every one of the fourteen audit rows in the window is accounted for.

---

## WHAT COULD NOT BE MEASURED, AND WHY

* **Production timings.** Everything was measured against a local dev server pointed at the production database. A dev server compiles routes on first request and serves unminified bundles, so the ABSOLUTE numbers are pessimistic on both sides; the BEFORE and AFTER were taken with the same method on the same server so the RATIO is sound, and the request counts and payload sizes are exact regardless.
* **The StrictMode doubling in production.** Dev fires each row's effect twice. Production fires it once, so the real BEFORE is ~100 evidence requests rather than 200. Stated rather than smoothed over.
* **A real screen reader.** DOM order, roles, the live region, focus behaviour and the target sizes are all measured; NVDA, JAWS and VoiceOver were not run.
* **The clipper Dashboard at `/dashboard`.** Measured at **4,492 ms ready with 55 requests and no dominant endpoint**, but it is not the page the owner calls his Dashboard and it was left alone.
* **The end of the unfiltered queue.** 5,833 clips at 30 a page cannot be reached, so the end-of-list state was rendered by filtering to a single match.

---

## WHAT THE OWNER SHOULD KNOW NEXT

1. **The page size is one constant.** `PAGE_SIZE` in `admin/clips/page.tsx` is 30 and can be 20 or 50 with no other change; the request storm no longer scales with it.
2. **The shell is now the slowest thing on the page**, not the clips: `/api/admin/sidebar-counts`, `/api/notifications` and `/api/community/*` are the top four in the AFTER measurement, each polling every 30 seconds. That is the next round if he wants more.
3. **`/api/accounts` still returns every column of every account** to the Accounts page itself, at 27.7 MB. Only the Dashboard was narrowed. That page deserves the same treatment.
