# BL-829 — make the clipper app fast, starting with the one line that cost 367 people five seconds each

**Round:** BUILD. Merged to `main` at `96853d49`, verified pushed. **Requires a Railway REDEPLOY.**
**Date:** 2026-08-25. **Tags:** `pre-BL-829` / `post-BL-829` / `pre-BL-829-merge` / `post-BL-829-merge`.
**Follows:** BL-828, which measured the problem and ranked the fixes. This implements them **in that order**.

---

## The one-paragraph version

`manifest.json` sent every installed clipper app to `/dashboard`. BL-486 retired the clipper dashboard, so
that page renders `null`, fetches 871.9 KB of clips it never shows, and then redirects to `/campaigns`.
Changing one line, plus a guard for the installs that do not re-fetch the manifest, takes a cold launch on
a cheap phone from **15,772 ms and 2,285.2 KB to 11,589 ms and 1,305.3 KB**. Four more pages stopped
pulling the full clip list to add up three numbers. `/clips` kept its payload on purpose — six live figures
derive from the complete array and one of them gates a submission — and had its **render** windowed
instead, taking its DOM from 26,153 nodes to 2,371. Nothing is cached, no money figure moved, and 84
accuracy checks and 65 render assertions pass with zero failures.

---

## How the before and after were measured

**Both trees, same machine, same database, same session, back to back.** A "before" quoted from a previous
round is not a measurement of this change, so `main`'s tree was checked out in the worktree, built and
measured first; then the branch's tree was checked out, built and measured with the identical harness.

- **Production build only** — `npm run build` then `PORT=3829 npm start`. `next dev` ships roughly 5 MB of
  unsplit JavaScript per page; at a 1.6 Mbit throttle the page never renders and every paint metric comes
  back null. BL-828 discarded a whole dev pass for this reason and this round did not repeat it.
- **Real Chromium via Playwright**, driven with a real minted Auth.js session for the real heavy clipper
  (404 clips), not a dev bypass.
- **Bytes are wire bytes** — `Network.loadingFinished.encodedDataLength` from the CDP, after compression.
- **Cheap-phone profile** — `Network.emulateNetworkConditions` at 1.6 Mbit down / 750 Kbit up / 150 ms RTT
  plus `Emulation.setCPUThrottlingRate` at 4x, on a 375x812 viewport.
- **Warm, not cold** — every page is loaded twice and only the second is reported.
- **Bundle sizes are gzip level 9** over the chunks each route's `page_client-reference-manifest.js` names,
  because this project's `next build` prints no size columns. That matches BL-643/646/648/649 so the
  figures stay comparable to their 110.5 KB recharts result.

---

## PART 1 — the headline is one line

`public/manifest.json`: `"start_url": "/dashboard"` → `"start_url": "/campaigns"`.

Cold PWA launch, throttled, measured on both trees:

| | before (`main`) | after (branch) |
| --- | --- | --- |
| time to a usable `/campaigns` | **15,772 ms** | **11,589 ms** |
| wire | **2,285.2 KB** | **1,305.3 KB** |
| requests | 106 (24 API) | 98 (17 API) |
| of that, `/api/clips/mine` | 899.8 KB | **0.0 KB** |

**4,183 ms and 979.9 KB saved per cold launch, for 367 installed clippers.**

### Do the 367 existing installs receive it? Yes, and the reason is specific.

`public/sw.js` is **inert**: it caches nothing and never calls `respondWith`, so nothing on the device
serves a stale `manifest.json` — every install fetches it from the network. What iOS **does** snapshot at
install time is BL-649's launch image and the icon, which is cosmetic and unrelated to routing. An install
that has not re-fetched the manifest keeps the old `start_url` only until it next does.

**The `/dashboard` guard covers exactly that gap**, and it had to be written correctly rather than
plausibly. `providers.tsx:40` mounts `SessionProvider` with **no `session` prop**, so the client fetches
`/api/auth/session` after mount and `status` is `"loading"` on the first render. A guard written as
`!!session && role === "CLIPPER"` is therefore **FALSE at exactly the moment the mount effects fire** — it
would have read correctly and stopped nothing. The shipped guard holds while `status === "loading"` and
re-runs when the session settles, which is also why `holdFetch` is in the dependency arrays rather than
`[]`. An unauthenticated visitor is unchanged.

**Proof the redirect path is genuinely gone:** on the after build, entering at `/dashboard` costs
1,305.3 KB against 1,274.5 KB for entering at `/campaigns` — a **30.8 KB** difference, which is the
redirect document itself and nothing else. `/api/clips/mine` is **0.0 KB** on both.

---

## PART 2 — why `/api/clips/mine` is large, and what was done about it

**Established first, not assumed.** The route returns **920,038 bytes on 404 rows** and is fetched by five
of six clipper pages. It is large because it `include`s every relation for every clip — campaign, account,
every stat row, marketplace origin and creator earning — to serve a card that renders six fields, and
because four of the five callers only want a **sum**.

Two parameters were added, **both opt-in**. An unparameterised request is byte-identical to before, proven
by the identical measured size on **both** trees:

| shape | bytes | gzip | rows |
| --- | --- | --- | --- |
| `/api/clips/mine` (unchanged default) | **920,038** | **60,807** | 404 |
| `?fields=summary` | 315,524 | 16,788 | 404 |
| `?limit=30&offset=0` | 66,416 | 4,733 | 30 |

`/dashboard`, `/accounts`, `/payouts` and `/earnings` now pass `fields=summary`.

### `/clips` deliberately does NOT paginate its fetch

Six live figures derive from the **complete** array:

1. the chip counts (`ClipsPremium.tsx:55`)
2. BL-818's not-counted roll-up (`ClipsPremium.tsx:52`)
3. `clips.length` in two places (`clips/page.tsx:297,361`)
4. **`getDailyRemaining` (`clips/page.tsx:186`), which GATES A SUBMISSION**
5. MomentumCard's `clipsEver` (`MomentumCard.tsx:70`)
6. MomentumCard's `clipsToday` (`MomentumCard.tsx:74`)

Computing (4) from thirty rows would tell a clipper he had submissions left when he did not. The
independent accessibility review reached the same conclusion from a different direction. So the page's cost
was diagnosed as **CPU, not bytes**, and the **render** was windowed at 30 rows behind a
"Show more clips (374 more)" control, with a visible "Showing 30 of 404 clips" line. Every count above is
still computed from the same complete array, by the same code, unchanged.

Result on `/clips`: payload unchanged at 1,032.6 KB, **DOM nodes 26,153 → 2,371**, **unthrottled settle
5,159 ms → 2,661 ms**.

The paginated server path **is** built and proven (below) and is left available for a follow-up round that
moves those six figures deliberately, which is a money-adjacent change and not a performance one.

### Per-page wire, unthrottled, same harness on both trees

| page | before | after |
| --- | --- | --- |
| /dashboard | 1,139.4 KB | **155.3 KB** |
| /earnings | 1,055.6 KB | **462.6 KB** |
| /payouts | 1,061.7 KB | **473.0 KB** |
| /accounts | 1,007.2 KB | **416.9 KB** |
| /clips | 1,031.8 KB | 1,032.6 KB (unchanged by design) |
| /campaigns (control, never fetched it) | 138.3 KB | 136.8 KB |

---

## PART 3 — clippers get their own views by date

`src/components/clips/ViewsOverTime.tsx`, mounted on `/clips`, collapsed by default.

**Only that clipper's data, enforced in SQL rather than by stripping a payload.**
`analytics/views-by-day/route.ts:137` appends `AND c."userId" = $n` on the clipper path, so another
clipper's rows cannot be selected at all. Proven by grep, 12 of 12 at zero in that route:

```
0  ownerCpm            0  agencyFee              0  lockedOwnerShareDecimal   0  clientName
0  ownerCpmDecimal     0  agencyFeeDecimal       0  cpmInstagramOwner         0  aiKnowledge
0  cpmTiktokOwner      0  cpmYoutubeOwner        0  budget                    0  totalSpent
```

**Loaded only when opened.** No fetch and no chart chunk until the disclosure is pressed. Verified in the
render pass: `aria-expanded="false"` on first paint at all five widths.

**BL-646's deferral is intact and was re-measured, not assumed.** The chart is imported through the same
`next/dynamic` + `ssr:false` wrapper BL-648 used. Recharts markers appear in 3 chunks on disk (110.6, 110.4
and 24.0 KB gz) and **none of them is inside any route's client entry**: `/clips` 8 chunks / 145.7 KB gz,
`/earnings` 7 / 126.7, `/campaigns` 7 / 126.3, recharts inside entry **0** for all three.

**The chart is not the data.** `area-gradient-chart.tsx` carries no role and no accessible name, so it is
`aria-hidden` and the numbers are a real `<table>` with a **visible** `<caption>`, above which sits a
**visible** summary naming the total, the date range and the best day, ending in a trend that is one of
exactly three sentences. Measured example at 320px:

> **5,223,128** views in the last 30 days, from 27 July to 25 August. Your best day was **20 August** with
> **830,726** views. Views are going up.

The `.catch(() => ChartUnavailable)` on the dynamic import is load-bearing: `next/dynamic` is
`React.lazy`, a rejected import throws to the nearest error boundary, and there is **no `error.tsx` in the
`(app)` segment** — a failed chunk on a bad connection would otherwise blank the whole clips page.

---

## PART 4 — nothing is cached

- **Zero write calls in the diff.** `grep -cE "\.(create|update|upsert|delete|createMany|updateMany|deleteMany)\("` over every added line: **0**.
- No money figure is stored, memoised or read stale. `computeBalance` is a pure function over arrays the
  caller already holds and still runs on read; BL-818's, BL-824's and BL-762's derivations all still
  recompute per request. `/api/clips/mine` keeps `export const dynamic = "force-dynamic"`.
- The only in-memory map added is `cacheRef` in the chart, holding already-fetched **view counts** for one
  mount so switching 30/90/365 and back costs nothing. It is discarded on navigation and holds no money.

---

## PART 5 — the accuracy proof

**84 checks, 0 failures**, run against the production build (`scripts/bl829-accuracy.mjs`, 80, and
`scripts/bl829-today.mjs`, 4).

- Every derived figure the four aggregate pages render is recomputed from **both** payload shapes using the
  arithmetic **lifted from the pages themselves**, and compared as **integer cents** so a floating-point
  tie cannot pass for equality: `/payouts` per-campaign earned, `/accounts` per-account views/likes/
  comments/count, `/earnings` approved / pending / total / not-counted at 15, 30, 90 and 365 days.
- The paginated pages are **stitched back into one list and compared to the unpaginated list row by row**,
  `JSON.stringify` for `JSON.stringify`, because BL-816 established that pagination fails by a row going
  missing rather than by a number moving. Row differences: **0**.
- `totalCount` is asserted **stable across every page** and equal to the unpaginated row count, and equal
  to the true per-campaign and per-status totals **at `limit=1`** — the search and totals genuinely query
  the full set.
- The **FLAGGED trap**: `clipperStatus()` masks FLAGGED to PENDING for clippers, so a naive server-side
  `status=PENDING` filter would drop rows the clipper can see. `PENDING` matches `["PENDING","FLAGGED"]`,
  asserted to return exactly the ids the client predicate selects, with **no raw FLAGGED status leaking**.
- The **marketplace-swap trap**: `notCountedTotalAll` would be wrong as a SQL `SUM(clips.earnings)`,
  because a creator must see `marketplaceCreatorEarning.amount`, not the poster's figure. The not-counted
  rows are fetched with relations and put through the same swap in JS. Asserted equal to the client
  arithmetic: **37 cents over 3 rows**.
- `todayByCampaign`, the figure that gates a submission, asserted equal to the client's own arithmetic over
  the complete array: **29 clips on one campaign**.

---

## PART 6 — the render pass

**50 shots at 320 / 375 / 414 / 1280 / 1440**, `window.innerWidth` printed beside every one:
**0 at the wrong width, 0 with horizontal overflow.** **65 assertions, 0 failures.** Surfaces: `/clips`
top, the Show more control, the list after a press, the analytics closed / open / with its table,
`/earnings`, `/payouts`, `/accounts` and `/campaigns`.

Asserted, not merely photographed, at every width:

- BL-818's not-counted line still renders on `/earnings`.
- BL-762's minimum is still explained on `/payouts`.
- Pressing Show more adds rows (30 → 60 cards).
- **Focus STAYS on the Show more button.** The accessibility review explicitly ruled out reusing BL-816's
  move-focus-to-the-first-new-row for a clipper who will press this twelve times.
- The analytics disclosure starts collapsed.
- The summary names a total and a date range in words, and the trend is one of the three sentences.
- Every day is a real table row, under a visible caption.
- **BL-739's touchmove guard holds**: `data-no-swipe` is on both new containers (the panel and the chart),
  so the global swipe handler does not eat a touch and scroll the page behind.

---

## The accessibility review ran BEFORE any UI, and it changed the design

Three of its rulings are in the shipped code:

1. **Do not paginate the `/clips` fetch** — it reached the six-figures conclusion independently.
2. **Do not move focus to the first new row** on Show more; focus stays on the button.
3. **The chart summary must be visible, not `sr-only`** — the audience is teenagers at 320px who cannot
   read a 220px gradient, and a hidden equivalent rots unseen.

It also caught two defects that would have shipped:

- `STATUS_LABEL[status].toLowerCase()` produced **"Showing 3 in review clips"**, because "In review" is a
  chip label and not an adjective. A noun map replaced it: "clip waiting for review".
- `role="status"` fires on a text **change**, so pressing Show more twice on a list whose remainder is the
  same would have announced once and then said nothing. A sequence counter appends an alternating
  **non-breaking** space — a plain space is collapsed by whitespace normalisation and would not have worked.

---

## Safety, verified

- **The 6 money files plus `tracking.ts` and `campaign-era.ts` are byte-identical by blob OID on BOTH
  refs** (`git rev-parse pre-BL-829-merge:<file>` vs `HEAD:<file>`), and `not-counted.ts` with them.
  `tracking.ts` does not appear in the merge diff: `grep -c` returns 0.
- **No schema change, no `prisma migrate`, no index created.** An index on `clips("userId", "createdAt")`
  would help the paged path if it is ever wired in; it is specified here and deliberately **not applied**.
- **No Apify actor was run.** The 11 BL-678 guards are untouched.
- **No payout created, modified, approved or cancelled; no clip's earnings or status changed.** Every
  request this round made was a GET, and the diff contains zero write calls.
- Post-merge, cast to `::text` against DB `now()`: **7,689 clips, invariant breaches 0**, 195 payout
  requests, **payout_adjustments 7** (the same figure BL-827 recorded), approved earnings **$14,193.54**
  over 6,308 approved clips. Newest clip `updatedAt` 2026-08-25 18:11:07 against `now()`
  2026-08-25 18:12:57 — that is the tracking cron writing view counts, a background job this round neither
  ran nor touched.
- Build passes on the merge: exit **0**, `✓ Compiled successfully`, **BL-348 hooks gate at 0 errors and 11
  warnings**, which is the baseline exactly. eslint was confirmed present (v9.39.4) first, because a
  missing binary makes the gate silently no-op. Every build was read from a log with its own exit code
  echoed, never piped through `tail`.
- The branch tree OID and the merge tree OID are **identical** (`e04a49b7…`), so the branch build is the
  merge build; the merge was nevertheless rebuilt from scratch on `main`.

---

## Named, not smoothed

- **The chart's own x-axis labels are month/day** (`8/19`) while the summary and the table use long dates
  (`19 August`). The chart is `aria-hidden`, so this is a sighted-only inconsistency; it comes from the
  route's existing `label` field and was left rather than changed under a performance round.
- **The additive `date` field grew the analytics payload**: `views-by-day?days=365` went from 10,051 to
  17,369 bytes (1,057 → 2,084 gzip). It is paid only when the clipper opens the section.
- **Per-page THROTTLED settle times are a single sample each and vary by seconds run to run.** On the
  throttled pass `/clips` read 9,084 ms before and 10,744 ms after, and its wire read higher after — the
  `/api/` census is identical at 21 calls on both, and the extra requests are lazily-loaded thumbnails that
  a faster page manages to finish inside the same measurement window. The byte counts, the DOM counts and
  the cold-launch figure are the numbers to trust; the throttled per-page settle is not.
- **`/api/gamification` is untouched.** BL-828 ranked it second at 1,731 ms cold with a genuine
  N-plus-one (a `for (i = 0; i < 400; i++)` loop issuing one query per day walked). It is still there.
- **The paginated `/clips` fetch is built but not wired.** That is a deliberate deferral, not an oversight.

---

## Files

```
public/manifest.json                          start_url /dashboard -> /campaigns
src/app/(app)/dashboard/page.tsx              holdFetch guard, waits for the session
src/app/(app)/accounts/page.tsx               ?fields=summary
src/app/(app)/payouts/page.tsx                ?fields=summary
src/app/(app)/earnings/page.tsx               ?fields=summary
src/app/api/clips/mine/route.ts               opt-in fields=summary and limit/offset
src/app/api/analytics/views-by-day/route.ts   additive date + meta.rowsReturned
src/components/clips/ClipsPremium.tsx         render windowing, one announcer, noun map
src/components/clips/ViewsOverTime.tsx        NEW — the clipper's own views by date
BACKLOG.md                                    BL-829 (166 -> 167 entries)
scripts/bl829-*.mjs                           9 harnesses: measure, accuracy, render, bundle
```

**Rollback:** `git revert -m 1 96853d49`, or `git reset --hard pre-BL-829-merge`.
