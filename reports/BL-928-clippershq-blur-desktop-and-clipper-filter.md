UNREMOVABLE: none. Teardown removed every sandbox row, and a sweep of 341 id columns found 0 values left.

# BL-928: blur off the card badges and the phone top bar, the star removed, the budget desktop, and a clipper campaign filter

Merged to main at `f559c0b` (tags `pre-BL-928`, `post-BL-928`, `pre-merge-BL-928`, `post-merge-BL-928`).
Rollback: `git reset --hard pre-merge-BL-928`. The merge tree equals the branch tree (`e8a20f9b`).

## Part 1: the blur
* **Removed:** the 2 px backdrop blur on the three card badges (type, flow, Completed) and `backdrop-blur-xl` on the mobile top bar.
* **Replacement:** the badges go from 60% to 75% black; the Completed badge keeps its gray. The top bar keeps its colour (`--bg-card`, the same rgb as the old glass) and is now opaque.
* **Contrast** (over a pure white photo, the worst case): white text on the badge is 10.37:1 (was about 5.7:1); fuchsia icon 5.89:1; sky icon 6.22:1; Completed about 7.6:1.
* **BottomNav.tsx is untouched:** the diff is empty and its blob `56e09e2b` is identical on main after the merge.

**The phone scroll, interleaved on one build.** The same production build serves both arms: "blurback" puts back exactly the two removed blurs at runtime. Real touch drags on /campaigns, slow network, 3 rounds with the arm order alternated. Figures are medians.

| CPU | arm | dropped | longest | p95 | compositor CPU |
| --- | --- | --- | --- | --- | --- |
| 4x | blur | 6 | 33 ms | 17 ms | 3,237 ms |
| 4x | none | 7 | 33 ms | 17 ms | 1,520 ms |
| 6x | blur | 102 | 50 ms | 33 ms | 3,187 ms |
| 6x | none | 30 | 50 ms | 17 ms | 1,479 ms |

The saving is 1.72 s at 4x and 1.71 s at 6x. The brief expected about 1.65 s of 2.2 s; the saving matches, but the blurred compositor measured about 3.2 s, not 2.2 s. At 4x the frames were already fine, so only compositor time moves. At 6x, dropped frames fall 102 to 30.

## Part 2: the favourite star
* **Speed:** removing it buys no measurable speed. BL-925 measured it as no part of the scroll cost.
* **What it stored:** only a list of campaign ids in the clipper's own browser (localStorage `clippers_hq_favorites`). Nothing was ever stored on the server.
* **Who read it:** the campaigns page sort, and `/favorites`, a page no navigation links to. The layout every clipper gets no longer reads the list; the list is left in each browser untouched.
* **What a clipper loses:** marking campaigns so they sit first in his list. Nobody else ever saw his marks.
* **Tab stops:** 4 fewer per width.

## Part 3: the budget desktop, measured before anything changed
Measured on main at 1280 and 1440, 4x and 6x CPU, slow network, 3 runs each, as the heaviest real clipper (968 clips).
* **/campaigns is fine on a throttled desktop.** At 4x: 0 dropped, p95 17 ms. At 6x: 7 to 17 dropped, p95 17 to 33 ms.
* **/clips is not.** It is ready at 14.4 to 15.1 s. The scroll drops 604 to 693 frames, with p95 83 to 133 ms and the main thread busy 13 s of a 14 s scroll pass.

**The three biggest costs:**
1. **The /clips scroll repaints on the main thread** (Layerize is 11.3 s of 13.2 s of main busy). Runtime attribution, one suspect off at a time (main busy): nothing 13.2 s, hover 13.2, card hover 13.1, clip badge blur 13.1, all animation 12.8, nav scroll listener 13.2, **opaque `<main>` 7.0 and 6.9**, forced compositing 7.3 and 7.3. The cause: at DPR 1, Chromium does not composite a transparent scroller.
2. **The unpaged `/api/clips/mine`:** 2,311 KB of the 2,450 KB warm load. **Not changed:** BL-829 kept the full array because six live figures are computed from it. It needs its own round.
3. **The 605 KB shell script** (cold /campaigns ready at 5.1 to 6.4 s). **Refused, as a separate bundle round.**

**Fixed: cost 1 only.** `<main>` now paints `--bg-primary`, the colour `<body>` and its wrapper already paint.
* **Pixel proof:** 24 views (6 clipper pages, at 375 and 1280, at the top and scrolled), each shot on one page load as shipped, with the style added, and with it removed again. Page noise was 0. 16 views were identical. 8 differed only by rasterisation rounding: at most 2 levels out of 255, except 31 pixels of at most 24 on the anti-aliased edge of one icon. No colour, text or layout changed.
* **/clips desktop, main → branch (medians of 3):** 1280 4x dropped 633 → 190, p95 83 → 17 ms, main busy 13.2 → 7.5 s; 1280 6x 693 → 297, p95 133 → 33 ms, main busy 13.2 → 10.2 s; 1440 4x 604 → 215, p95 83 → 17 ms; 1440 6x 685 → 319, p95 133 → 33 ms.
* **What got worse, stated plainly:** the longest single frame at 6x rose (167 to 217 and 233 ms). The display compositor's CPU rose (3.0 to 9.5 s at 1280 4x), because the headless software renderer now draws the frames it used to drop.
* **/campaigns desktop:** main busy during the scroll went from 1.17 to 0.53 s at 4x.
* **Final build, one confirming run:** /clips 1280 4x drops 177 with p95 17 ms.

## Part 4: the clipper campaign filter on /clips
* **The campaign list:** `GET /api/clips/mine/campaigns` derives its list from his own clips: one grouped query over the exact predicate `/api/clips/mine` pages over, then `select { id, name }`, returning `{ id, name, clipCount }`.
* **The filter:** `/api/clips/mine` takes `campaignIds` in paged mode (at most 50 ids of at most 64 characters each, otherwise 400). The order is total (createdAt, then id). It returns the true total, and adds `totalCountAllCampaigns` only when a scope applies. Chip counts come from the server over the whole scoped set.
* **The page:** the Campaign control (MultiDropdown, new opt-in `touch` prop: 44 px trigger and rows) sits outside the status group: full width above the chips on a phone, first on the chips' row on desktop. It combines with the status chips and "Show only these". The count line names the scope and the number outside it. Show more fetches the next server page, so every row is reachable. sessionStorage keeps the choice, validated against his current campaigns on restore. The control is hidden when he has clips on fewer than 2 campaigns.
* **Found and fixed by the live-body proof: a real leak, and it predates this round.** `/api/clips/mine` returns every Clip column minus a strip list, and seven owner-side columns were reaching every clipper's network tab: the owner CPM snapshot on 6,562 live clips, the owner's pre-override CPM on 52, and his pre-devaluation CPM on 51. The route now strips them. No clipper page read them; the owner reads them through `/api/clips`.
* **Also fixed, found by the renders:**
  * The open Campaign menu painted under the clip list: every `.bl418-in` child is a stacking context. The filter bar is now `relative z-10`.
  * The trigger's name lacked a space. The computed name is now "Campaign: All campaigns".

## Part 5: proofs
* **Sandbox** (`bl928sbx-`): opening snapshot at DB `now()` 2026-09-23 21:15:16 UTC; 15 people, 6 test campaigns, 256 clips, 0 tracking jobs.
* **Proof: 42 of 42 checks pass**, each against independent SQL, every response checked not to be 429. The campaign list for 1, many and 0 campaigns excludes archived, deleted-only and other clippers' campaigns. True totals, every row reached once in DB order, a createdAt tie across the 30-row page boundary split by id. Status and not-earning filters within a scope. Unscoped responses carry no scope keys.
  * Failure paths, one person each: a foreign campaign id gives 0 and reveals nothing; 51 ids give 400, 50 give 200; a 65-character id gives 400, 64 gives 200; signed out gives 401; a banned person gives 401 (the session layer invalidates a banned token before the route's 403); a non-clipper gets 200 with nothing.
* **No leak, by grep and by live body.** Grep: the new route has 0 forbidden names in code and selects only `{ id, name }`. Sandbox bodies: no budget, spend, ownerCpm, agencyFee, clientName, aiKnowledge, owner-side column, sentinel value, or other clipper's clip. The real 968-clip clipper: 0 forbidden keys in the unpaged, paged and campaign bodies; his 4 campaigns sum to 968.
* **Renders: 50 of 50.** Five widths (320, 375, 414, 1280, 1440), 3 at a time, one person per width. The first pass shared one person and hit that route's 30-a-minute limit, so it was redone.
  * States covered: one campaign, many, none; filter open and closed; the longest name (truncated, no pan); a choice kept across reload; 35 rows reached; status plus scope; /campaigns with no star and solid badges; the top bar opaque over scrolled cards.
  * Every shot read back the URL and innerWidth, and measured pan 0.
* **Unchanged text:** 280 comparisons, before (main) against after, as the real clipper.
  * All text is identical once relative times are normalised: headings, status, paragraphs, chips and cards, on /campaigns and /clips.
  * The tab order differs only by the 4 removed stars. On phones the walk also reached the bottom nav. That was the walk's timing, not the page: on one build, a fast walk reaches the nav and a walk pausing 400 ms per Tab finds it hidden and inert.
* **Money files: identical by blob OID on main after the merge.** clip-earnings-writer `80418a18`, earnings-calc `00410634`, balance `67c30c89`, tracking `672d2ab3`, invariant middleware `61cef393`, money-decimal `ef5cdae7`.
* **Invariants: open 7 of 7, close 16 of 16.** No overpayment (both v2 aggregates counted), no double pay, paid is final for the maker and the v2 poster. Never decrease: 10,346 clips, 0 decreased. Earnings invariant: 0 breaches. No campaign over budget. ANGIE BROWN: $2,700, ACTIVE, $17.50 spent. Both reconciliation forms return 0 rows; every money fingerprint is identical at open and close.
* **Closing snapshot:** identical to the opening one except notifications, where 15,697 real rows became 15,694. Nothing was deleted: the live watchdog re-stamped `createdAt` on 3 existing CRON_DID_NOTHING owner rows (their ids date from 2026-09-21), which moved them out of the "created before T" set.
* **Guards:** every prebuild guard passes, including check:css-tokens and check:clips-list-scope. The hooks gate has 0 errors and 10 warnings. No guard file was touched, so there was no failure to demonstrate.
* **tsc:** 0 errors. No Prisma chunk is loaded by /clips, /campaigns or the layout. One pre-existing chunk carrying Prisma's error classes is used only by /admin/campaigns.
* **a11y:** the accessibility lead listed 8 blockers, then 2 more after the first pass; all are fixed, and its final review is a PASS. Its contrast numbers were checked here by arithmetic.
* **Teardown removed:** users 15, campaigns 6, clips 256, clip_accounts 9, clip_stats 1, notifications 2, user_lifecycle 7, email_send_outcomes 2.
* **BACKLOG:** 235 to 236 entries. `checkpoint/BL-723` is not an ancestor of main and was not merged.

## Disclosed
* **A rule breach:** one stray heredoc command (no-op, no write) was run and stopped.
* **Live alerts reached the sandbox OWNER:** production's owner-alert fan-out addressed 2 alerts to its `.invalid` address. The rows were removed by the teardown; their outcome was not recorded first.
* **A process stopped:** a stopped attribution loop kept one child running; it was ended by PID.
* **Build timing:** the phone A/B and the desktop profile ran on the build before the route strip and the z-index fix. Neither touches /campaigns. The final build was re-measured once.
* **notify-owner-build was not run.** It sends email through Resend, a vendor call this brief forbids; BL-925 made the same call.
* **Model split:** every UI line, clipper-facing query and this report were written by the strongest model. The accessibility lead reviewed only (READ); every measurement and render was run and read here (VERIFIED).
