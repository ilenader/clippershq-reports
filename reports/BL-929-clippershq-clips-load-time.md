UNREMOVABLE: none. The teardown deleted all 288 ledgered rows; a sweep of 341 id columns found 0 values left. No index was created and no real row was written by this round's code.
**VENDOR CALLS, DISCLOSED FIRST:** my local test servers made **483 real HikerAPI requests** (all answered HTTP 400; reel ids were fake). Sandbox clips had Instagram URLs and no stored cover, so each rendered card POSTed `/api/clips/{id}/thumbnail`, which calls HikerAPI with the real key from `.env.local`. They wrote no usage-ledger row and raised no owner alert. Found at 11:25 UTC; both servers were then restarted with every vendor key blanked (verified: `reason=hiker-http-none`, nothing leaves the machine). **BL-928's sandbox had the same shape and its report did not say so.**

# BL-929: /clips took 14 seconds on a budget desktop because its clip list crossed the wire uncompressed

Merged to main at `a2f01a4` (tags `pre-BL-929`, `post-BL-929`, `pre-merge-BL-929`, `post-merge-BL-929`). Rollback: `git reset --hard pre-merge-BL-929`. The merge tree equals the branch tree (`18c59633`). **Needs a Railway redeploy.**

**Model split:** the strongest model did every measurement, every change and this report. No cheaper model was used: the measurements overturned my own guesses twice (below), so I kept the chain unbroken. One subagent ran, the accessibility lead (review only, **READ**; the file list it cites was checked against `git diff`, **VERIFIED**). **Caps:** one Chromium, strictly sequential; renders 3 contexts at a time; database reads one connection per script; **two local servers (main and branch) during the interleaved comparisons**, every request sequential.

## PART 1: the 14 seconds, broken into parts, before naming a cause
Production builds of main, dev bypass off, the heaviest real clipper (id prefix `cmrujf29`, 968 clips, 4 campaigns), 1.6 Mbit down, 150 ms RTT, warm load, medians of 3:

| profile | first paint | ready | TTI | requests | wire | DOM nodes | largest payload |
| --- | --- | --- | --- | --- | --- | --- | --- |
| /clips 1280, 4x | 1,076 ms | 13,874 ms | 15,359 ms | 102 | 2,248.4 KB | 2,533 | `/api/clips/mine`, 2,107.4 KB |
| /clips 1280, 6x | 1,736 | 14,799 | 17,259 | 102 | 2,248.3 | 2,533 | the same |
| /clips 1440, 4x | 1,232 | 14,174 | 15,898 | 102 | 2,248.4 | 2,533 | the same |
| /clips 1440, 6x | 1,936 | 14,716 | 17,349 | 102 | 2,248.4 | 2,533 | the same |
| /campaigns 1280, 4x (control) | 1,272 | 1,630 | 2,031 | 104 | 154.4 | 923 | `/api/campaigns`, 17 KB |

**Where the 13.9 s went (1280, 4x, from Resource Timing):** shell 920 ms until the list was requested; server plus one round trip 1,640 ms; **network 10,639 ms carrying 2,156,945 bytes**; parse 25 ms (`JSON.parse` of 2.16 MB under the same throttle); render 589 ms from arrival to the first card, then 1,559 ms of long tasks to TTI. At 6x: 1,509, 1,848, 10,661, parse 50, render 821, then 2,460 ms to TTI.

**Why so many bytes.** `next start` gzips pages (`/clips` HTML arrives `Content-Encoding: gzip`) but **not App Router route-handler JSON**, and production's Railway edge adds none (its `/api/*` answers carry no encoding). Gzipped, the same list is 148,896 bytes. BL-828 recorded this route at 871.9 KB on the wire for 891,480 raw bytes and did not name it. **So this is not a regression:** the list grew from 391 to 968 clips, and it was never compressed.

**Server side, measured on its own** (six GETs per shape; every query counted and timed by a `pg` preload on the measurement server only): the unpaged list takes 1.15 to 2.07 s warm (5.35 s cold) with **8 queries**. The slowest is always the `stats` include, 635 to 1,615 ms warm (3,875 ms cold), returning **37,989 rows to keep 968**: Prisma runs `stats: { orderBy: checkedAt desc, take: 1 }` as one 968-parameter query with no limit and keeps the first row per clip in memory. The paged list takes 0.43 to 0.49 s (15 queries) and `/api/campaigns` 0.16 s. **No query is near Prisma's 5 s budget.**

**Rows:** 968 held, **30 rendered** (BL-829's windowing is intact), 61 to 89 DOM nodes per row (1,966 of 2,533), 3 images per row (its cover plus 2 shared campaign images; 33 distinct sources) and **0 API requests per row** (every cover is stored, so no thumbnail POST fires). Show more caused 1 request (an Ably token). **No per-row storm.**

**The three biggest costs, in order:**
1. **Carrying the uncompressed list:** 10.6 s.
2. **The server building it:** 1.6 to 1.9 s, most of it the 37,989-row stats query.
3. **Main-thread work after it lands:** 2.1 to 3.4 s (arrival to ready plus ready to TTI).

## PART 2: fixed, cheapest first, re-measured
**Fix 1, `src/lib/compressed-json.ts`:** the same `JSON.stringify` text, gzipped only when `Accept-Encoding` allows gzip and the body is at least 1 KB. **2,156,645 → 148,901 wire bytes; the decoded text is identical** (2,156,637 characters on both builds).
**Fix 2, `src/lib/latest-clip-stat.ts`:** the latest stat per clip, asked for as one row per clip (a LATERAL `LIMIT 1` on the existing `idx_clip_stats_clip_checkedat_desc`, one array parameter), put back in the same place.
**No index was needed or created.** Proved for every live clip: 10,260 of 10,260 identical field by field (40 have no stat either way), and the table has 0 tied `checkedAt` pairs. The 8 queries now return **1,944 rows instead of about 39,000**. Interleaved server pairs: main 1.11 to 1.39 s, branch 0.65 to 0.88 s (one outlier of 1.79 s, where the clips query itself took 1.13 s).

**Before and after, interleaved (main against branch, arm order alternating, 3 rounds, medians):**

| profile | TTI | ready | transfer phase | server phase | wire | requests | DOM |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1280, 4x | 15,085 → **5,402** | 13,538 → 3,807 | 10,684 → 1,071 | 1,572 → 924 | 2,248.4 → 286.2 KB | 102 → 101 | 2,533 → 2,533 |
| 1280, 6x | 16,622 → **8,725** | 14,497 → 5,040 | 10,658 → 1,023 | 1,622 → 788 | 2,248.4 → 297.7 | 102 → 101 | same |
| 1440, 4x | 15,369 → **5,225** | 13,706 → 3,599 | 10,628 → 1,035 | 1,683 → 915 | 2,248.4 → 286.2 | 102 → 101 | same |
| 1440, 6x | 16,383 → **8,126** | 14,352 → 4,648 | 10,729 → 1,020 | 1,639 → 697 | 2,248.4 → 319.2 | 102 → 103 | same |

* **Cold first visit, 1280 at 4x:** ready 18,731 → 7,866 ms; bytes 3,368 → 1,406 KB.
* **Worse, stated plainly:** at 6x the work after arrival grew (ready to TTI 2,138 → 3,155 ms at 1280). The list now lands while other startup work is still running; before, that work finished during the ten-second download.
* **Cost 3 was NOT fixed, and this is reported rather than shipped.** Its profile is spread across React's DOM work (`setAttribute`, `appendChild`, react-dom internals) with no single app function in charge. Every cut I could find would render less or later, which changes what the page shows.

## PART 3: the leak family
* **BL-928's owner-CPM strip, live bodies.** Production runs BL-928 (the new `/api/clips/mine/campaigns` answers its own 401 `{"campaigns":[]}`), but its own clipper body cannot be read: a minted session is refused there (401). On the same code in a local production build, as the real clipper: **0 forbidden keys** in `/api/clips/mine` unpaged (968 rows), paged and campaigns.
* **Sweep:** every non-admin API path named in client code (108 paths, 71 with GET); **67 requested as the real clipper**, 4 skipped (dev-auth, ably-token, two template paths), 0 answered 429. Counted grep (`grep -c`) of non-admin route files naming each field: ownerCpm 13, agencyFee 6, clientName 8, aiKnowledge 7, lockedOwnerShare 5, budget 21, spend 13; the live bodies decide.
* **FOUND AND FIXED:** `GET /api/campaigns?status=PAST` (and `?includePast=true`) gave **any clipper** 4 real client names, **8,237 characters of the owner's aiKnowledge**, the owner's user id on 4 campaigns, and `pricingModel` on every row. The detail route also sent `pricingModel`.
  * **Cause:** the list route spreads the Campaign row and its clipper strip (`campaign-clipper-view.ts:78`) denied 7 fields only.
  * **Fix:** `clientName`, `aiKnowledge`, `ownerUserId` and `pricingModel` added to that strip. No clipper surface reads any of them. `/api/campaigns/[id]` already dropped the first three.
  * **After:** 0 forbidden keys in 67 bodies, and 0 of those keys on the PAST URLs (the same 10 and 14 rows).
* **Cleared, by design:** `budget` and spend (shown on the campaign cards); the clipper's own 9% fee (the fee disclosure); `cpmRate` and `cpmRateDecimal` (null on all 17 live campaigns; a structural risk, listed below).

## PART 4: nothing changed except the speed
* **Sandbox** (`bl929sbx-`): opening snapshot at 10:49:25 UTC; 15 people, 7 test campaigns (one PAST carrying the sentinels), 256 clips, 0 tracking jobs.
* **Proof: 32 of 32 pass**, main against branch request by request:
  * same JSON for the real clipper in 11 shapes (every status, not-earning, each campaign, the last offset 960);
  * same JSON for 5 sandbox people;
  * gzip only when accepted, identity and `q=0` get the raw body, and a body under 1 KB is not compressed;
  * main leaks both sentinels on 2 URLs, the branch on none of 5;
  * failure paths, one person each, none 429: signed out 401, banned 401 (the session layer invalidates the token), admin 200 with `[]`, 51 ids 400.
* **Every row, interleaved, after the 11:00 tick had finished:**
  * **Real clipper:** 10 comparisons, **3,048 rows, 0 differences**, including the 941-clip campaign read to its last page. The newest stat was 11:01:16 both before (11:30) and after (11:56), and 0 responses were 429.
  * **Sandbox:** 30 comparisons, 256 rows, 0 differences.
* **Renders: 55 of 55.** Widths 320, 375, 414, 1280 and 1440, with innerWidth, URL and pan read back; states: many, few and no clips; filter open and closed; a choice kept across reload; the longest name; each status plus scope; the unscoped last page (41 of 41, focus on "That is all 41 of your clips."); /campaigns; the top bar.
* **Money files, by `git rev-parse` on the merge:** `80418a18`, `00410634`, `67c30c89`, `672d2ab3`, `61cef393`, `ef5cdae7`, all identical; `tracking.ts` is in no diff.
* **Invariants: open 7 of 7, close 13 of 16.** No overpayment (both v2 aggregates), no double pay, paid is final for both earners, never decrease (10,352 clips, 0 decreased), earnings invariant 0, no campaign over budget, ANGIE BROWN $2,700 ACTIVE. Both reconciliation forms return 0 rows.
  * **The 3 failures:** the clip earnings, agency and v2 platform fingerprints moved. **Production's 11:00 tick** raised 5 real clips by 1 to 7 cents, each 0.3 s after its new stat (11:00:52 to 11:01:03).
  * **Not mine:** my servers run no cron (`RAILWAY_NATIVE_CRON` is unset; no `[RAILWAY-CRON]` line in any log).
* **Closing snapshot:** identical except `clip_stats` +47 (that tick) and 3 CRON_DID_NOTHING owner notifications that the live watchdog re-stamped at 11:50:59 (created 2026-09-21, still present).
* **Guards and gates:** all 22 prebuild steps pass; hooks gate 0 errors, 10 warnings (eslint present); tsc 0 errors before and after; builds exit 0. No guard was touched, so none owed a failure demonstration.
* **Bundle and accessibility:** no Prisma in any /clips chunk. Accessibility lead: **PASS**; no UI file changed, and nothing left the tab order.
* **Teardown removed:** users 15, campaigns 7, clips 256, accounts 9, stat 1. It also removed what the live app wrote for sandbox people: user_lifecycle 12, notifications 1, email outcomes 1 (an owner alert fanned out to the sandbox OWNER).
* **BACKLOG:** 236 → 237. `checkpoint/BL-723` is not an ancestor.

## Also disclosed
My comparison harness stalled once: its scoped Show more pressed faster than the route's 30-a-minute limit and met 429s; it was stopped by PID and rerun paced, counting every 429 (0). The "nogzip" A/B arm was invalid (Chromium sets Accept-Encoding itself) and was dropped. Main's query counter logged nothing on the copied build, so main's query figures come from the first measurement of the identical code. notify-owner-build was not run (Resend is a vendor).

**Follow-ups (in BACKLOG):** cost 3 above; every other App Router JSON route is also uncompressed; `?fields=summary` still fetches every stat row; `cpmRate` beside `clipperCpm` would give the owner's cut by subtraction if ever set; blank vendor keys on every test server; a pre-existing copy bug ("clip waiting for reviews").

**IN ONE LINE, the throttled desktop (/clips, 1280 at 4x CPU, 1.6 Mbit, interleaved, median of 3):** TTI **15,085 → 5,402 ms**, wire **2,248.4 → 286.2 KB**, requests **102 → 101**, DOM nodes **2,533 → 2,533**.
