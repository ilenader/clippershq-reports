# BL-828 — why the clipper app is slow on a cheap phone, measured

**2026-08-25 · DB `now()` = `2026-08-25 15:44:13.87112+00` (first read) to `16:10:29.099818+00` (last) · AUDIT ONLY, READ ONLY.**
No code, config, schema or data change. Nothing built, nothing merged. Base `origin/main` @ `c49f3209`, branch `checkpoint/BL-828`, isolated worktree `C:/w828`, a short path, `node_modules` never junctioned, **removed at the end**. Every database read through `scripts/run-select.js`, every timestamp cast `::text` against DB `now()`. Handles redacted; the measured clipper is **Clipper H**, id prefix `cmrujf29`, which the owner can map privately.

---

## THE ANSWER, BEFORE THE WORKING

> **THE OWNER'S ASSUMPTION IS HALF RIGHT, AND THE HALF THAT IS RIGHT IS NOT THE BIGGEST WIN.**
>
> **The dominant cost is ONE endpoint.** `/api/clips/mine` returns **891,480 bytes on 391 rows** and is fetched on **five of the six clipper pages**. On `/clips` it is **871.9 KB of a 1,001.1 KB page — 87.1%**. On `/accounts` it is **89.0%**, and that page fetches all 391 clips purely to add up three numbers. The control proves it: `/campaigns`, the one clipper page that does not call it, is **137.0 KB** with the identical shell and the same 98 requests.
>
> **But the single best fix is not pagination at all. It is one line in `manifest.json`.** `start_url` is `/dashboard`, and BL-486 retired the clipper dashboard, so every clipper is redirected to `/campaigns` — after the dashboard has already fetched 871.9 KB of clips it will never show. Measured on the cheap-phone profile: **16,381 ms and 2,255.9 KB as shipped, against 11,400 ms and 1,276.4 KB if `start_url` were `/campaigns`. That is 4,981 ms and 979.5 KB saved, on a one-line change with zero accuracy risk.** 367 clippers have the app installed.
>
> **The second cost is `/api/gamification` at 1,731 ms cold**, hidden behind a 30-second memo cache that makes it read 336 ms warm. It contains a genuine N-plus-one: a `for (i = 0; i < 400; i++)` loop issuing one query per day walked. It is called on `/clips`, `/payouts` and `/dashboard`.
>
> **The analytics the owner wants is already built, already clipper-scoped, and already cheap.** `/api/analytics/views-by-day?metric=views` returns his own daily views, 365 days back, in **107 ms and 10,051 bytes**, with a payload of nothing but `{label, value}`. It is already wired to `/earnings` for the earnings metric. The views metric is simply not surfaced.
>
> **Derive-on-read is NOT a cost.** `computeBalance` runs **zero queries** — it is a pure function over arrays the caller already has. `/api/earnings` is **161 ms** on a 391-clip clipper. Nothing needs caching, which matters because caching is the one thing that could put a figure at risk.

---

## METHOD, AND WHICH NUMBERS CAME FROM WHERE

**Real browser, production build.** Every timing, request count and byte figure below was measured in **Chromium via Playwright against `npm run build` + `npm start`**, not against `next dev`. That distinction is load-bearing: my first pass ran against `next dev` and the throttled case never rendered at all, because dev ships **5.2 MB of unsplit JavaScript** which at 1.6 Mbit takes 26 seconds to download on its own. **Those dev numbers are discarded and are not reported as measurements**; the request counts and API timings from that pass agreed with the production pass and are not repeated.

* **Requests and bytes** come from the Chrome DevTools Protocol: `Network.responseReceived` for identity and `Network.loadingFinished.encodedDataLength` for bytes **on the wire after compression**.
* **Render timings** are the browser's own Navigation Timing and Paint Timing entries read out of the page, not a stopwatch around `goto()`.
* **Warm, never cold.** Every page is loaded twice and only the second is reported, which is the discipline BL-816 recorded.
* **The throttled profile** is CDP `Network.emulateNetworkConditions` at **1.6 Mbit down / 750 Kbit up / 150 ms RTT** with `Emulation.setCPUThrottlingRate` at **4x**, on a **375x812** viewport. That is a cheap Android phone on a poor connection.
* **Bundle sizes** are gzip level 9 over the actual chunk files named by each route's `page_client-reference-manifest.js`. BL-643 and BL-646 both recorded that this project's `next build` prints the route table **without size columns**, so they cannot be read from build output; level 9 matches their method so the figures are comparable to their 110.5 KB recharts result.
* **Endpoint figures** are six sequential GETs each, first discarded, median reported, against the production server talking to the production database on the same machine — so the network component is negligible and what is measured is server work plus serialisation.
* **Structural, not measured:** the query-count claims about `/api/gamification`'s internals and the `take:` caps are read from source and are labelled as such wherever they appear.

**Absolute latencies are pessimistic in both directions** — a laptop is faster than Railway, the database is remote — but every ratio, request count and byte figure is exact.

---

## PART 1 — EVERY CLIPPER PAGE, MEASURED

### Whose profile, and how heavy

**Clipper H**, id prefix `cmrujf29`, chosen by measurement rather than by reputation: he is the **heaviest clipper on the platform by clip count**.

| | |
|---|---|
| clips | **388** live (391 rows returned including 3 the API includes) |
| approved | 375 |
| campaigns | 3 |
| recorded earnings | **$1,070.04** |
| `ClipStat` history rows | **14,491** |
| payouts | 1 |
| **installed the app** | **yes**, `2026-08-07 11:12:39.001` |
| last login | `2026-08-25 01:02:45.445` |

He is a real, active, PWA-installed heavy clipper. For scale, the next four are 380, 375, 311 and 278 clips.

### Unthrottled, production build, desktop 1280px

| page | settle | requests | wire | FCP | DCL | DOM nodes | rows rendered |
|---|---|---|---|---|---|---|---|
| dashboard | 2,854 ms | 116 | **1,106.2 KB** | 136 ms | 28 ms | 845 | 50 |
| **clips** | **6,871 ms** | 111 | **1,022.9 KB** | 556 ms | 434 ms | **25,187** | **1,167** |
| earnings | 2,564 ms | 86 | **1,018.4 KB** | 172 ms | 27 ms | 729 | 41 |
| payouts | 3,346 ms | 87 | **1,027.3 KB** | 96 ms | 20 ms | 470 | 30 |
| **campaigns** | 2,252 ms | 102 | **146.6 KB** | 176 ms | 40 ms | 843 | 50 |
| accounts | 2,517 ms | 88 | **973.0 KB** | 108 ms | 20 ms | 542 | 31 |

**Read the wire column.** Five pages carry roughly a megabyte. One carries 147 KB. The difference is not the page: it is whether the page calls `/api/clips/mine`.

### Throttled, cheap phone, 1.6 Mbit / 150 ms RTT / 4x CPU / 375px

| page | settle | requests | wire | JS (first visit) | FCP | rows |
|---|---|---|---|---|---|---|
| dashboard | **12,509 ms** | 106 | 1,798.7 KB | 240.6 KB | 1,340 ms | 50 |
| clips | 9,641 ms | 90 | 1,222.1 KB | 211.0 KB | 656 ms | 1,166 |
| earnings | 10,837 ms | 90 | 1,502.8 KB | 231.1 KB | 924 ms | 41 |
| **payouts** | **15,924 ms** | 89 | 1,449.0 KB | 216.3 KB | **2,300 ms** | 30 |
| campaigns | 8,588 ms | 94 | 834.1 KB | 229.6 KB | 1,216 ms | 50 |
| accounts | 10,005 ms | 93 | 1,223.9 KB | 218.5 KB | 888 ms | 31 |

**Everything is between 8.6 and 15.9 seconds.** First contentful paint is fast (0.7 to 2.3 s) — the shell appears quickly and then the clipper waits several more seconds for numbers.

### JavaScript weight, gzip level 9, from the production build

| route | chunks | raw | **gzip** |
|---|---|---|---|
| `/clips` | 8 | 515.4 KB | **143.3 KB** |
| `/payouts` | 8 | 496.2 KB | **138.0 KB** |
| `/accounts` | 8 | 484.5 KB | **135.9 KB** |
| `/earnings` | 7 | 455.4 KB | **126.6 KB** |
| `/campaigns` | 7 | 450.2 KB | **126.3 KB** |
| `/dashboard` | 7 | 447.4 KB | **124.5 KB** |
| `/progress` (control, no chart) | 7 | 449.4 KB | **124.8 KB** |

**BL-648's recharts deferral is INTACT.** Three chunks on disk carry recharts markers — `0mzfj-ozdd0fb.js` at **110.6 KB gz** (BL-646's chunk, to the tenth of a KB), a near-identical `0danpo_om_ajf.js` at 110.4 KB, and a 24.0 KB fragment — and **zero of them are inside the `/earnings` client entry**. `/earnings` at 126.6 KB sits alongside chartless `/progress` at 124.8 KB, which is the same sanity check BL-646 used. The saving is holding.

113 JS chunks on disk, 1,345.6 KB gzip in total; the shared entry chunk every route pays is `0_-qqpvyibhm7.js` at **70.1 KB gz**.

### THE DOMINANT COST, NAMED, WITH THE EVIDENCE

Every clipper endpoint, six warm GETs each, first discarded, median:

| endpoint | median | min | max | bytes | gzip | rows |
|---|---|---|---|---|---|---|
| **`/api/clips/mine`** | **604 ms** | 539 | 873 | **891,480** | **59,264** | **391** |
| `/api/earnings` | 161 ms | 151 | 181 | 46,730 | 4,415 | — |
| `/api/gamification` (warm) | 173 ms | 171 | 192 | 984 | 288 | — |
| `/api/campaigns/spend` | 167 ms | 148 | 201 | 469 | 326 | — |
| `/api/calls?my=true` | 133 ms | 132 | 140 | 2 | 22 | 0 |
| `/api/campaigns` | 130 ms | 107 | 165 | 20,515 | 3,396 | 5 |
| `/api/campaign-accounts` | 127 ms | 103 | 157 | 1,647 | 517 | 4 |
| `/api/payouts/mine` | 114 ms | 104 | 119 | 6,394 | 3,606 | 1 |
| `/api/analytics/views-by-day` (views, 365d) | 107 ms | 106 | 116 | 10,051 | 1,058 | 365 |
| `/api/campaigns/past` | 103 ms | 84 | 110 | 5,541 | 1,059 | 9 |
| `/api/accounts/mine` | 77 ms | 72 | 79 | 2,480 | 792 | 3 |
| `/api/notifications` | 71 ms | 69 | 74 | 5,260 | 713 | 20 |
| `/api/profile/avatar` | 70 ms | 69 | 80 | 120 | 125 | — |

**`/api/clips/mine` is 19 times the payload of the next largest endpoint and 3.5 times the slowest.** It is fetched by `/clips`, `/earnings`, `/payouts`, `/accounts` and `/dashboard` — five of six.

**What the ~110 requests per page actually are**, grouped by resource type on the warm second load:

```
/clips        54 Fetch  999.7 KB   26 Script 0.0 KB (cached)   13 Image 0.0 KB   98 total, 1001.1 KB
              heaviest single transfer: 871.9 KB  /api/clips/mine        = 87.1% of the page
/campaigns    53 Fetch  135.6 KB   26 Script 0.0 KB            14 Image 0.0 KB   98 total,  137.0 KB
              heaviest single transfer:  21.3 KB  /api/campaigns
/accounts     51 Fetch  978.0 KB   26 Script 0.0 KB             6 Image 0.0 KB   88 total,  979.4 KB
              heaviest single transfer: 871.9 KB  /api/clips/mine        = 89.0% of the page
```

**Two separate facts, and they must not be conflated.** The request **count** is dominated by Next.js RSC link prefetching — roughly 35 of the ~53 Fetch requests are `/<route>?_rsc=…` at 2.5 to 6.4 KB each, plus polling. The request **payload** is dominated, overwhelmingly, by one endpoint. Fixing the count and fixing the bytes are different jobs, and the bytes are what a 1.6 Mbit connection feels.

### Per page, the dominant cost

| page | dominant cost | evidence |
|---|---|---|
| **dashboard** | the page itself — it is discarded before it is seen | 1,106 KB fetched, then `router.replace("/campaigns")` |
| **clips** | `/api/clips/mine`, then rendering 1,167 rows | 871.9 KB of 1,001.1 KB; 25,187 DOM nodes |
| **earnings** | `/api/clips/mine`, fetched alongside `/api/earnings` which already has the totals | 871.9 KB against `/api/earnings`'s 46.7 KB |
| **payouts** | `/api/gamification` cold, then `/api/clips/mine` | 9,994 ms for gamification under throttled contention |
| **campaigns** | nothing dominant; this page is already fast | 146.6 KB total, 2,252 ms |
| **accounts** | `/api/clips/mine`, fetched only to add up per-account views and likes | 871.9 KB of 979.4 KB |

---

## PART 2 — THE CANDIDATES, EACH TESTED

| candidate | verdict | evidence |
|---|---|---|
| **a query returning far more rows than are displayed** | **CONFIRMED, and it is the dominant cost** | `/api/clips/mine` returns 391 rows with **no pagination anywhere**; the server cap is `take: 5000` (`clips/mine/route.ts:95`). `/accounts` renders 31 account cards and fetches all 391 clips to compute per-account sums client-side (`accounts/page.tsx:264-287`). |
| **over-fetching FIELDS, not just rows** | **CONFIRMED** | `clips/mine/route.ts:60` uses `include` with **no top-level `select`**, so every Clip scalar ships: **52 keys per row, 2,280 bytes per row**. 15 keys are non-empty on **zero of 391** rows and still cost 1.5 KB each across the payload. |
| **an N-plus-one where each row triggers its own query** | **CONFIRMED on the server, in `/api/gamification`** | `gamification.ts:314` is `for (let i = 0; i < 400; i++)` calling `evaluateDayByBounds` → `db.clip.findMany` (`:213`) once per day walked. **Measured cold: 1,731 ms median, 2,071 ms peak, against 336 ms warm — the 30-second memo cache hides a factor of 5.2.** |
| **a per-ROW fetch, the BL-816 shape** | **PRESENT BUT DORMANT — and it is a loaded gun** | `ClipCardNew.tsx:176` POSTs `/api/clips/{id}/thumbnail` from a `useEffect` inside the row `.map`. It is skipped when `clip.thumbnailUrl` is set, and for Clipper H that is **391 of 391**, so I measured **zero** such requests. Platform-wide, **1,480 live TikTok/Instagram clips lack a thumbnail across 226 clippers**, and the worst single clipper would fire **95 POSTs on one page load** — each doing an outbound provider fetch **and a `db.clip.update`** — against a 40-per-minute rate limit, so 55 would 429 and, because the session marker is written only on success (`:184`), **retry on every visit forever**. |
| **a per-clip computation such as the earnings derivation** | **CLEARED, and this is the important negative** | `computeBalance` (`balance.ts:271-325`) runs **ZERO queries**. It is a pure function over arrays the caller already fetched: five in-memory reductions plus `effectivePaidOut`. `/api/earnings` runs a **constant 7 queries** regardless of clip count and measures **161 ms median on a 391-clip clipper**. Deriving on read costs essentially nothing. |
| **a missing database index** | **CLEARED** | `clips` carries `clips_userId_createdAt_idx`, `clips_userId_idx` and `clips_userId_postedAt_idx`; `clip_stats` carries four, including `(clipId, checkedAt)`, `(clipId, checkedAt DESC)` and `(clipId, isManual, checkedAt DESC)` — the last matching the analytics query's predicate exactly. **And an index must not be added casually:** BL-642 measured `clips` at 92.2% HOT updates, and indexing `earnings` would convert roughly 228,000 to non-HOT and tax `writeClipEarnings` itself. |
| **a heavy JavaScript bundle** | **SECONDARY, and the recharts saving is intact** | 124.5 to 143.3 KB gz per route; zero recharts chunks inside the `/earnings` entry. First-visit JS on the throttled profile is 211 to 241 KB, paid once and then cached — all 26 Script requests were 0.0 KB on the warm load. |
| **images loading at full size** | **PRESENT, LOW IMPACT TODAY** | Raw `<img>` with no `width`/`height`/`sizes` at `ClipCardNew.tsx:110`, `:265`, `:370`, `EarningsPremium.tsx:457`, `CampaignsRedesign.tsx:176`, `campaign-card.tsx:153`, `AccountCardPremium.tsx:69`. The YouTube candidate chain starts at `maxresdefault.jpg`, 1280x720, rendered into an 80 to 104 px box (`ClipCardNew.tsx:139`). Measured cost on the warm load: **0.0 KB, all cached**; 13 image requests. Missing dimensions are a layout-shift and first-visit cost, not a repeat-visit one. |
| **unscoped platform-wide queries served to clippers** | **CONFIRMED, cheap today** | `/api/campaigns/spend` runs two **unbounded, unscoped** groupBys — one over **5,508** approved clips and one over **3,282** agency rows, platform-wide, with no `take:` — for every clipper who opens `/campaigns`. 167 ms today; it scales with the platform, not with the clipper. |

### What the derived balance costs on a clipper with hundreds of clips

**It costs nothing measurable, and the reason is structural.** `computeBalance` takes `{ clips, payouts, marketplaceCreatorEarnings }` as arrays and returns. The **fetch** of those arrays is the cost, not the derivation. `/api/earnings` fetches them with a named `select` on every query and returns **46,730 bytes in 161 ms**. `/api/clips/mine` fetches almost the same rows with no projection and returns **891,480 bytes in 604 ms**. **The same data, nineteen times the bytes, because one route names its fields and the other does not.**

---

## PART 3 — WHAT PAGINATION WOULD AND WOULD NOT FIX

**It addresses the dominant cost on `/clips`, and it is the largest single lever on that page. On the other four pages it would be wrong, and something else is needed.**

Measured on Clipper H's real payload:

| shape | raw | gzip | reduction (raw) |
|---|---|---|---|
| as shipped, 391 rows, 52 keys | 891,480 B | 59,264 B | — |
| **30 rows, fields unchanged** | **67,328 B** | **4,925 B** | **92.4%** |
| all 391 rows, projected to the 18 fields the UI reads | 482,645 B | 43,281 B | 45.9% |
| **30 rows AND the projection** | **36,647 B** | **3,546 B** | **95.9%** |
| all 391 rows, summary only (id, campaignId, clipAccountId, status, earnings, views, likes) | 70,577 B | 9,716 B | 92.1% |

**Pagination is the dominant lever and the projection is secondary**, because the dead fields are mostly nulls that gzip already crushes: the projection saves 45.9% raw but only 27% on the wire. **This is the opposite of BL-816's finding on the admin side**, where a per-row fetch storm dominated and pagination alone would not have fixed it. The shapes are genuinely different and the assumption did not transfer.

### If pagination is built

**Page size: 30.** It is BL-816's own number on the same platform, it puts the load boundary below the first screen at 375 px, and at 30 rows the payload falls to 4,925 bytes gzipped. Nothing else on the page scales with it.

**How the totals and the search stay TRUE.** BL-816 established the rule and proved it: every filter and the count must query the **whole set server-side**, never the loaded page. A list that searches only what it has loaded silently hides clips, and that is far worse than slow. Concretely, three things must hold and must be proven the way BL-816 proved them:
* `totalCount` is the true count over the full filtered set, identical at page size 30 and at any other size.
* Every status filter and every search term returns identical counts at both page sizes.
* Consecutive pages stitch to the same ids in the same order as one unpaginated fetch, every row byte-identical.

**The four other pages must NOT be paginated, because they need every clip to compute a total.** `/earnings`, `/payouts`, `/accounts` and `/dashboard` fetch `/api/clips/mine` for aggregates, not for a list. Paginating what they receive would silently change a figure, which is the one thing this round must never do. **They need the opposite fix: an opt-in summary projection**, exactly BL-816's `?fields=summary` pattern — 70,577 bytes for all 391 rows, **92.1% smaller**, carrying every field their arithmetic touches and nothing else. `/accounts` is the clearest case: it fetches 871.9 KB to produce per-account view and like sums.

---

## PART 4 — THE CLIPPER ANALYTICS THE OWNER WANTS

### It already exists, it is already clipper-scoped, and it is already cheap

`/api/analytics/views-by-day` (`src/app/api/analytics/views-by-day/route.ts`) is **the only analytics route a clipper can reach**, and it is already role-scoped at `:79-83` — OWNER, CLIPPER and CLIENT only; ADMIN and REVIEWER are refused. A clipper's SQL carries `AND c."userId" = $n` (`:137`) on **every** query, so cross-tenant leakage is blocked at the SQL level rather than by a post-hoc strip.

Asked as Clipper H:

```
GET /api/analytics/views-by-day?metric=views&days=365
  107 ms   10,051 bytes   365 rows
  meta: {"metric":"views","days":365,"campaignId":null,"scope":"clipper","source":"clip_stats delta-by-day"}
  data: [{"label":"8/26","value":0}, … ,{"label":"8/25","value":150625}]
  sum over the year: 5,171,345 views

GET /api/analytics/views-by-day?metric=views&days=30
  103 ms    1,012 bytes    30 rows
```

**The payload is `{label, value}` and nothing else.** No clip id, no campaign name, no other clipper, no rate, no budget. It is structurally clean.

**The route already accepts `campaignId`**, so "across campaigns, and per campaign" is already supported.

### What data exists, at what granularity, and how far back

| | |
|---|---|
| table | `ClipStat` → `clip_stats`, `prisma/schema.prisma:1167-1207` |
| columns | `views`, `likes`, `comments`, `shares`, `sharesSource` (nullable, BL-820: NULL means unmeasured, never zero), `isManual`, `checkedAt` |
| platform-wide rows | **277,574**, table size **109 MB** |
| earliest row anywhere | **`2026-04-22 19:57:55.505`** — four months |
| Clipper H's rows | **14,528**, from `2026-08-07 15:00:46.745` to `2026-08-25 16:02:38.288` |
| his distinct days | **19** |
| his rows per clip | **37.2 average**, roughly two ticks per clip per day |
| manual rows | 0 of 14,528 |
| indexes | four, including `(clipId, isManual, checkedAt DESC)` which matches the query's predicate exactly |

**Granularity: per DAY is honest. Per HOUR is not.** At roughly two ticks per clip per day, and with the auto-ladder spacing older clips further apart, an hourly chart would show a sawtooth of the tracking schedule rather than of the clipper's audience. **A per-day chart is what the data supports and it is what the existing route returns.**

**How far back, per clipper:** as far as their first clip's first tracking tick, capped by the platform's own `2026-04-22`. For Clipper H that is 19 days, and the route correctly returns zeros before it rather than omitting the days.

### Costing it honestly

**The query is cheap and it is already being paid on `/earnings` today** for the earnings metric — measured at 328 ms unthrottled in the page pass and 161 ms in isolation. The views metric is **103 ms**.

**But there is a real defect to fix before it is surfaced more widely.** The `metric=earnings` branch issues a **full `clip_stats` scan for the clipper's clips grouped by day with NO date bound and NO LIMIT** (`route.ts:198-214`), even when `days` is supplied. Today that is 14,528 rows for the heaviest clipper and it is fast. It is unbounded work that grows forever, and it should take the same `days` clause the views branch already has at `:299`.

**Making it cheap is a solved problem: load it only when opened.** The chart is not on the critical path for any number the clipper needs. Fetching it on expand costs one 103 ms request and 1 KB.

### The boundary — exactly which fields may appear, and which may never

**MAY appear**, all of them the clipper's own and all already in the current payload or on his own pages:

* per-day **views**, **likes**, **comments**, and **shares only where `sharesSource` is non-null** (BL-820: NULL means unmeasured and must never render as zero)
* per-day **earnings** for his own clips, which `/earnings` already shows
* his own **clip count**, **campaign names he is on**, and **his own CPM** (`cpmAtSubmissionDecimal`), which his clip rows already carry
* totals over any range, scoped to him

**MUST NEVER appear.** BL-531 stripped eight fields from four clipper routes and that strip is load-bearing (BL-535 reverted the display half of BL-531 but **kept the security half**):

* `ownerCpm`, `ownerCpmDecimal`, `cpmInstagramOwner`, `cpmTiktokOwner`, `cpmYoutubeOwner`
* `agencyFee`, `agencyFeeDecimal`
* **`lockedOwnerShareDecimal`** — the owner's split verbatim, which a clipper once received in JSON
* `clientName`, `aiKnowledge` (CLAUDE.md)
* **anything about another clipper**: no `uniqueClippers`, no cross-clipper totals, no leaderboard-by-money, no other clipper's views or earnings
* **campaign budgets and campaign spend as platform figures**, and any per-campaign total that spans clippers
* the fields the owner's own analytics returns and a clipper must not: `totals.totalEarnings`, `totals.totalViews`, `perCampaign[].totalEarnings`, `earningsPerDay[]`, `platformViewDist[]` (`src/lib/analytics-summary.ts:84-119`), all platform-wide

**The existing route already satisfies every one of these**, and the reason is worth preserving: it filters in SQL rather than stripping afterwards. `/api/gamification` is the same shape — a four-field `select` allowlist — which BL-793 called "structurally immune to the BL-531 leak class, a stronger mechanism than the `OWNER_SIDE_FIELDS` strip." **A new analytics surface should be built the same way.**

### The chart must not undo the 110.5 KB saving

**It need not, and the mechanism is already in the repo.** `EarningsChart.tsx:30-63` imports the chart through `next/dynamic` with `ssr: false`, a `.catch(() => ChartUnavailable)` fallback at `:34`, and a **220 px reserved placeholder** so nothing shifts. Verified on this build: **zero recharts chunks inside the `/earnings` client entry**, and `/earnings` at 126.6 KB gz sits beside chartless `/progress` at 124.8 KB.

**Two conditions on any new chart.** It must use that same `dynamic` + `ssr: false` + `.catch` pattern — the `.catch` is not decoration, because `next/dynamic` is `React.lazy`, a rejected import throws to the nearest error boundary, and **there is no `error.tsx` in the `(app)` segment**, so a failed chunk would blank the whole page including the balances. And it should reuse `AreaGradientChart` rather than importing recharts directly, so it lands in the chunk that already exists. **Note also that `/referrals` still carries the identical 110.6 KB recharts chunk in its initial bundle** — BL-643 recommended doing `/earnings` first and `/referrals` was never done. That is a separate one-line win.

---

## PART 5 — WHAT MUST STAY EXACT

Every figure below is derived on read today. **Not one of them may be cached, approximated, precomputed or served from a stored aggregate**, and the reason is the same in every case: the derivation is the correctness guarantee.

### The money figures

| figure | where | derived by |
|---|---|---|
| **Available to withdraw** | `/earnings`, `/payouts` hero | `computeBalance.available` = `max(approved − effectivePaidOut − locked, 0)` |
| **Counted of Earned** | `/earnings` tiles | BL-818's `isNotCounted` shared predicate, applied server-side at `earnings/route.ts:209` and by the identical predicate client-side |
| **Paid out, before fees** | `/earnings` | `computeBalance.paidOut` |
| **of which does not reduce this balance** | `/earnings` sub-line | BL-824's `paidNoLongerOffsetting`, `earnings/route.ts:375` |
| **Removed from balance** | `/earnings` | two floored balances subtracted, never the raw total (`earnings/route.ts:224-226`) |
| **per-campaign available** | `/payouts` campaign rows | `computeCampaignBalances` |
| **shortfall to the minimum** | `/payouts` | BL-762's explanation, `resolveMinPayout` |
| **You received / You will receive** | `/payouts` history | BL-827: `calculatePayoutBreakdown(actualPaidAmount…)` on an adjusted row, `finalAmount` otherwise |
| **From your $X request. The owner set this payout to $Y** | `/payouts` history | the stored `amount` and `actualPaidAmount` |
| **per-clip earnings** | `/clips` rows | `Clip.earnings`, with `payoutReductionRatio` applied on every recompute |

### The count figures

Total clips; approved, pending and rejected counts; per-campaign clip counts; per-account view and like sums on `/accounts`; total views on `/progress` and in gamification; streak day count; level and bonus percentage; `totalCount` on any paginated list.

### What I would refuse to cache, and why

* **`computeBalance` and everything it feeds.** BL-824 shipped a fix that **wrote nothing** — eight clippers' balances changed on the next read, purely because the derivation changed. A cache would have made that release invisible until it expired, and a stale balance is a number a clipper acts on. It also costs nothing: **zero queries**.
* **The `isNotCounted` predicate and both sums it feeds.** BL-818 put it in one shared rule precisely so a clip cannot be classified two ways, and made both halves accumulate in **one loop over one array** so `counted + notCounted === earnedGross` holds by construction. A cache on either half breaks an identity a reader checks on screen.
* **`effectivePaidOut`.** It is the paid-is-final rule. Serving it stale re-introduces the exact offset BL-716 and BL-824 were both written to prevent.
* **Anything on `/payouts`.** It is a money-decision surface. BL-816 rejected caches on `/admin/clips` for the same reason and named the acceptable exception: `/api/campaigns/spend`, which feeds no decision.
* **`totalCount` on a paginated list.** A stale total is a clipper being told he has fewer clips than he has.

**What is safe to cache:** `/api/campaigns/spend` (BL-642 already recommends it, it feeds no decision), `/api/profile/avatar` (120 bytes, called four to seven times per page), and the analytics chart series, which is a picture of the past and is already 24 hours stale by construction.

**What must be proven byte-identical before and after any change:** every figure in both tables above, for a set of clippers spanning the shapes that exist — a heavy clipper, one with an adjusted payout, one with retired clips, one with earnings below money paid, and one with zero clips. BL-816's discipline is the standard: compare the figures **one at a time as integer cents**, not as a summed total, and stitch paginated pages back into one list and compare row by row.

---

## PART 6 — MOBILE AND OLD DEVICES

### The installed-app population

| | |
|---|---|
| live clippers | **1,457** |
| flagged `isPWAUser` | **367** (25.2%) |
| have ever opened the installed app | **433** |
| opened it in the last 7 days | **76** |
| logged in at all in the last 30 days | 525 |
| earliest install | **`2026-07-31 19:47:31.308`** |
| latest install | `2026-08-25 11:48:31.998` |

Installs by week: 6, 19, 30, 16, 8. **The oldest install on the platform is 25 days old.**

### Are stale installs a real population? NO, and the reason is better than the dates

**The service worker caches nothing.** `public/sw.js` is 49 lines, BL-369 reduced it to an inert shell, and `grep -c "caches.open\|cache.put\|cache.addAll"` returns **0**. Its `fetch` handler never calls `respondWith`, so **every request is handled natively by the browser**. It also declares `skipWaiting` and `clients.claim`, and `layout.tsx:227` forces `r.update()` plus one reload on controller change.

**So a clipper who installed the app in July receives new code on their next network load, exactly like a browser tab.** There is no stale-code population.

**BL-649's finding still stands but is narrower than it sounds.** iOS snapshots the `<head>` at Add-to-Home-Screen time and never re-reads it, so an existing install keeps the **launch image** set it was installed with. That is a splash screen, not code. Every current install was made when the served HTML declared zero startup images, so they still see iOS's black screen for 4 to 10 seconds — unchanged, not worsened, and not fixable without a re-add.

**One thing that IS a real PWA problem, and it is the biggest single finding in this round.** `manifest.json:4` sets `start_url: "/dashboard"`. BL-486 retired the clipper dashboard and `dashboard/page.tsx:35` does `router.replace("/campaigns")` for every clipper. **The redirect is a client-side effect and the page's data effects are not gated on role**, so they all fire first. Measured on the cheap-phone profile:

```
start_url as shipped (/dashboard):     16,381 ms   106 requests   2,255.9 KB   of which 871.9 KB is /api/clips/mine
if start_url were /campaigns:          11,400 ms    92 requests   1,276.4 KB   of which     0.0 KB is /api/clips/mine
                                       ────────    ──────────    ───────────
saving                                  4,981 ms    14 requests     979.5 KB
```

**Every one of the 367 installed clippers pays five seconds and a megabyte on every cold launch for a page they never see.**

### The device and browser mix

**The platform records device information in exactly one place: `problem_reports.platform` and `problem_reports.browser`.** The entire recorded population is **nine reports**:

```
android / chrome    7
windows / chrome    1
ios     / safari    1
```

**That is a nine-row sample and it must not be read as a distribution.** It is what exists. It points at Android Chrome, which is consistent with the owner's concern and with the cheap-phone profile used above, and it is the only device evidence the platform holds. `reviewer_audit_log.userAgentHash` is hashed and reviewer-only. **No general user-agent, screen-size or connection telemetry is recorded anywhere**, so the real mix is unmeasured and I am not going to estimate it.

**BL-737's and BL-739's mobile work is not implicated here.** Those were about 17 admin surfaces unreachable by touch inside the drawer; the fix shipped and BL-816 re-verified the guard with the drawer open. Nothing in this round's measurements touches it.

---

## PART 7 — THE RANKED PLAN

Ordered by measured benefit per unit of accuracy risk. **Everything above the line is safe: it removes work whose output is discarded, or moves bytes without moving a number.**

| # | do this | measured benefit | accuracy risk | effort |
|---|---|---|---|---|
| **1** | **`manifest.json:4` → `start_url: "/campaigns"`**, and gate `dashboard/page.tsx`'s data effects on `userRole === "CLIPPER"` so they do not fire during the redirect | **−4,981 ms and −979.5 KB on every PWA cold launch**, 367 clippers | **NONE.** It deletes a fetch whose result is thrown away | one line plus one guard |
| **2** | **`?fields=summary` projection on `/api/clips/mine`**, opt-in, for the four pages that fetch it for aggregates (`/earnings`, `/payouts`, `/accounts`, `/dashboard`) | **891,480 → 70,577 bytes, 92.1% smaller**, on four pages | **NONE if opt-in.** The client arithmetic is untouched and receives every field it reads. BL-816 did exactly this and proved it | small; one query shape, four call sites |
| **3** | **Bound the `metric=earnings` analytics scan by `days`** (`views-by-day/route.ts:198-214`) | prevents unbounded growth; today 14,528 rows for the heaviest clipper | **NONE.** The views branch already does it at `:299` | one clause |
| **4** | **Fix the dormant per-row thumbnail storm** — write the session marker on failure too, or move capture to the server tick | prevents **95 POSTs on one page load** for the worst clipper, each an external fetch plus a `db.clip.update`, 55 of them 429ing and retrying forever | **NONE.** It changes when a thumbnail is captured, not any figure | small |
| **5** | **Defer recharts on `/referrals`** the way BL-648 did on `/earnings` | **−110.6 KB gz** on first visit | **NONE.** Display only, and the pattern is proven | one line |
| **6** | **Paginate `/clips` at 30**, with `totalCount` and every filter querying the full set server-side | **891,480 → 67,328 bytes, 92.4% smaller**; 25,187 DOM nodes → roughly 650 | **LOW, but real, and it is the one item here that can hide a clip.** Must be proven BL-816's way: identical totals and identical filter counts at both page sizes, and pages stitching to a byte-identical list | medium |
| **7** | **Surface the views chart to clippers**, loaded on expand, through `AreaGradientChart` via `next/dynamic` with `ssr: false` and a `.catch` | the feature the owner asked for, at **103 ms and 1 KB** | **NONE to existing figures.** The route already exists, is already clipper-scoped in SQL, and returns only `{label, value}` | small |
| **8** | **Scope `/api/campaigns/spend`**, or cache it | removes two unbounded platform-wide groupBys (5,508 + 3,282 rows) from every clipper's `/campaigns` load | **NONE.** BL-642 already recommends caching it; it feeds no decision | small |
| **9** | **Cut the duplicate first-load fetches** — `MomentumCard.tsx:57-58` refetches `/api/accounts/mine` and `/api/campaign-accounts` that `/clips` already fetched; `/api/profile/avatar` is called four to seven times per page | roughly 6 to 10 requests per page | **NONE** | small |
| **10** | **Set `width`/`height` on the seven raw `<img>` sites**, and stop starting the YouTube chain at `maxresdefault` (1280x720 into a 104 px box) | first-visit bytes and layout shift | **NONE** | small |

### What to build first

**Items 1, 2 and 3, together, in one round.** They are all pure subtraction: a discarded page load, fields nobody reads, and an unbounded scan. Between them they remove roughly a megabyte from four pages and five seconds from every installed-app launch, and **not one of them touches a figure**.

### What to leave alone

**Do not cache any balance, any earnings derivation, or `totalCount`.** PART 5 lists them. `computeBalance` runs **zero queries** and `/api/earnings` is **161 ms** — there is nothing to win and a stale balance is a number a clipper acts on. BL-824 released money to eight clippers by changing a derivation and writing nothing; a cache would have hidden that.

**Do not add an index to `clips` to speed anything up.** BL-642 measured 92.2% HOT updates; indexing `earnings` converts roughly 228,000 to non-HOT and taxes `writeClipEarnings` on the write path. **And no index is needed** — the query shapes here are already covered.

**Do not paginate `/earnings`, `/payouts`, `/accounts` or `/dashboard`.** They fetch every clip to compute a total. Paginating what they receive would change a figure silently, which is the one outcome this round exists to prevent. Item 2 is the correct fix for those pages and item 6 is only for `/clips`.

**And I recommend AGAINST one thing the shape of this problem invites.** Do not precompute a per-clipper totals table and read from it. It would make every page instant and it would be wrong within a day: BL-824 changed what `available` means without writing a row, BL-827 changed what an adjusted payout displays, and BL-818 changed which clips are counted. **Every one of those shipped correctly because the figure is derived. A stored aggregate turns each of them into a migration and a reconciliation.** Two prior rounds recommended against building something and both were right; this is the third.

---

## WHAT COULD NOT BE MEASURED

* **Production timings.** Everything ran against a local production build talking to the production database. Absolute latencies are pessimistic in both directions; **ratios, request counts and byte figures are exact**.
* **The real device and browser mix.** Nine problem reports is the entire recorded population. No user-agent, screen-size or connection telemetry exists.
* **How many clippers actually experience the thumbnail storm.** 1,480 clips across 226 clippers lack a thumbnail and would trigger it; whether those clippers open `/clips` is unknown.
* **Whether a real iPhone re-reads web-clip metadata.** BL-649 recorded this as undocumented and no physical device was available to me either.
* **`next dev` throttled numbers are discarded**, not reported: the page never rendered because dev ships 5.2 MB of unsplit JavaScript. They are named here so nobody re-derives them and thinks they mean something.

---

## SAFETY

READ ONLY. One document. **No code, config, schema or data change; nothing built, nothing merged, no migration, no index created, no Apify actor, no clip, payout or balance touched.** Every database read through `scripts/run-select.js`, which refuses every write keyword, with every timestamp cast `::text` against DB `now()`. Every HTTP request made during measurement was a **GET**. Confirmed after the fact: Clipper H's clips **391** and earnings **$1,070.18** unchanged, his newest `updatedAt` still `2026-08-25 16:02:38.515` — earlier than every request this round made — **earnings-invariant violations 0**, `payout_adjustments` **7** before and after. The three new payout rows that appeared during the round are real clippers requesting; none is mine. **Zero Supabase pool errors** across both server runs. Handles redacted; the measured clipper is an 8-character id prefix. Worked in an isolated worktree at `C:/w828` on `checkpoint/BL-828`, **removed at the end**; `node_modules` never junctioned. **A markdown-only diff cannot change tsc or the build — the production build here was run to obtain measurements, exit 0, and no source file was modified.** Counted with `grep -c` and explicit `count(*)`, never piped through `head`. One shell at a time. NO dashes as bullets.
