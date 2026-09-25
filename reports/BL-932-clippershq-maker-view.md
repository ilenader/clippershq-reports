# BL-932 — a maker now sees every post of his clip, and his views and money day by day

**UNREMOVABLE: none.** Teardown removed 190 sandbox rows. The sweep then found 0 prefixed values across 343 id columns, and 0 of 60 ledgered product rows remain.

**Shipped 2026-09-25.** Branch `checkpoint/BL-932` (3c6a2bb4), merged to main as 675d31a3.
Rollback: `git reset --hard pre-merge-BL-932`, then in the SQL editor `DROP TABLE IF EXISTS marketplace_v2_editor_daily;`.

**Model split.** Opus wrote every line of UI, every query, every chart's data source and this report. One subagent was used, the accessibility lead, which reviewed the changed code (READ); the render measured its claims (VERIFIED). No other subagent was used.

## Decided, not drifted: BL-882 and the owner, side by side
* **BL-882** proved no poster identity reached a maker, because BL-876 question 16 was open and an open privacy question defaults to NO.
* **The owner** answered the poster half (a poster may not see other posters: still NO, no poster surface changed) and now the maker half: YES, a maker sees who posted his clip. BL-897 had already put usernames on the money page; BL-932 extends it to the card and a Details page.

## PART 1: what existed
* **Clips page** (`editor/page.tsx:36`, `editor-client.tsx`, data `/api/marketplace-v2/clips` `route.ts:44`): two sentences, "Open in Drive" as a text link, and a Details *toggle* whose panel held only "Posts so far: N" and his note. **No details page existed.**
* **Money page** (`editor/earnings/earnings-client.tsx`, `buildV2EditorDashboard`): tiles, the campaign table with its across and down checks, BL-897's per-post list. **No chart.**
* **Where views came from:**
  the maker read `MarketplaceV2EditorEarning.views` (a snapshot written only with money); poster and owner read the newest `ClipStat` (`poster-dashboard.ts:154`, `owner-overview.ts:277`). **Live: 11 of 67 posts differed, by up to 1,465 views (3,711 in total).** The maker now reads the same `ClipStat` expression: equal on 8 of 8 posts against the owner, 6 of 6 against the poster.
* **Money history:** none existed.
  the earnings table is one row per post, overwritten each tick; the owner's "money moved" files a whole amount under its last update day. **Built:** additive `marketplace_v2_editor_daily` (one row per maker per UTC day, nullable amount, FK to users with cascade, RLS on), written by a new tick post-step `v2-maker-daily` through `v2EditorPayableWhere`. Cost: one groupBy plus one upsert per maker per tick; 8 real makers, about 2,900 rows a year. **Nothing before 2026-09-25 exists or is drawn.**

## PART 2: every post under each clip
* **The card:** "Posted N times", the 3 most viewed posts (handle, platform icon, views, "You earned $X before the fee", Watch link) at full card width, then "See all N posts".
* **Copy, before (22 words):** "Approved. Posters can see it." and "Any poster can now find this clip and post it. You earn 45 percent of every post."
* **Copy, after (12 words):** "Posters can post it now. You earn 45 percent of every post."
* **Empty state:** "Approved. Waiting for its first poster." became "Nobody has posted it yet."
* **The 6-post card at 320 px:** 1,444 px on the first render (rows beside the thumbnail wrapped a 38-character handle one letter per line); 852 px after moving rows to full width.

## PART 3: the Drive button and the Details page
* **Drive button:** `DriveButton`, 48 px, full width on phones, `--mp-surface-0` on the accent measured at 5.89 to 1, new tab said in words.
* **Details page:** `/market/editor/clips/[id]`: clip, campaign, sent and approved times, his note, and a real table (caption, scoped headers, total row) of poster, platform, when posted, views, his earnings before the fee, live post.
* **Reconciliation:** it adds up down each column, measured in the browser: 12,347+5,003+3,331+2,677+1,399+777 = 25,534, and $7.61+3.08+2.05+0+0+0.48 = $13.22.
* **Cash** is worked out once, on the total, by the payout function, because the fee is taken on what he withdraws.

## PART 4: the charts
* Both charts use `V2SeriesChart`, which wraps `AreaGradientChart`, the analytics component (BL-908). No new chart style.
* **Views each day:** comes from the recorded `ClipStat` history. Its days add up to the views total on the page: 24,420 = 24,420.
* **Money each day:** only the recorded daily rows.
  no rows: "has not started yet" in words; one day: "starts on …, the first one appears once a second day is recorded"; six sandbox days: drawn, summing to $15.05 = last row minus first.
* The money page's tables and both of its checks are unchanged. The charts are an added section.

## PART 5: the leak sweep, against the live responses
* **The list:** 30 forbidden names (`grep -c` = 30), including the poster's earnings fields, `ownerCpm`, `agencyFee`, the owner's cut, `lockedOwnerShare`, `clientName`, `aiKnowledge`, `budget`, `spend`, CPMs and wallets. Wallet-shaped strings were searched for too.
* **Result:** 0 hits in 9 maker responses (clips route ×2, details ×5, money ×2).
  * *Correction:* the commit message says 11. That is a miscount; it is 9.
* **The sweep can fail:** run over the owner's own overview, it finds `posterGross`, `posterCash`, `posterFeePercent`, `platformLeg` and `budget`.
* **Only his own clips:** nothing of maker B in maker A's responses; A asking for B's clip gets 404. **Posters:** 4 poster routes hold no other poster's handle or post.
* **Failure paths, own user each, none a 429:** signed out 401, v2 not visible 404, banned 403, another maker's clip 404, a poster asking 404, missing clip 404.

## PART 6: proof
* **Sandbox** (prefix `bl932sbx-`, opening snapshot taken first): 13 people and 1 test campaign.
  9 posts by `createV2Post`, priced by `recomputeV2PostEarnings`, at uneven views; tracking jobs off at creation, vendor keys blanked.
* **Views and money pages:** these leave out test campaigns by design. So the campaign was made non-test and archived at the same time, in 6 windows totalling 93 s (10:32 to 10:44 UTC).
* **Final:** proof 35 of 35 (test) and 12 of 12 (flip); renders 45 of 45 at five widths, width and URL read back, states in words, pan 0.
* **Every run, including failures:**
  * The world script crashed twice before creating anything (a title length, then a `server-only` import), then passed 12 of 12.
  * First card render: 10 failures from my own wrong expectation.
  * First details render: 15 failures. This found a real defect: `TableHead` forces capitals, so handles showed in upper case.
  * First no-history render: 5 failures, from copy that named a button which was not there.
  * First money render: 13 failures. This found a real pre-existing defect: the 38-character handle made BL-897's post list pan the page 158, 103 and 64 px at 320, 375 and 414. Fixed with `break-all`.
* **Guards:** all 22 prebuild guards pass, and the hooks gate is 0 errors, 10 warnings (limit 11).
  The two guards I touched failed on demand, one break at a time, restored byte-identical: 4 of 4.
* **Money files:** the 6 money files are byte-identical by blob OID (80418a18, 00410634, 67c30c89, 672d2ab3, 61cef393, ef5cdae7), and `tracking.ts` is not in the diff.
* **Invariants:** 11 of 11 across the full population, including both reconciliation forms (0 rows each), no campaign over budget, and ANGIE BROWN at a $2,700 budget with $14.48 spent.
* **Closing snapshot:** every count identical.
  +$0.01 clip earnings, +$0.01 maker legs and one payout fingerprint moved, all from real activity *before* the sandbox existed (4 payouts PAID 09:58 to 10:11, the 10:00 tick).
* **Real rows written:** only 8 rows in the new daily table (today, $4.60 in total), written by the real writer. The cron overwrites them every tick after deploy.
* **Build:** tsc clean, `BUILD_EXIT=0` every build, merge tree equals branch tree, pushes verified, four tags, BACKLOG 238 to 239, `checkpoint/BL-723` not merged, worktree removed and confirmed gone. Accessibility review passed, nothing blocking. One database client per script, one at a time, beside the local server's pool; 5 render contexts at most. No vendor call.

## Found, not fixed (BACKLOG BL-932)
1. `TableHead`'s `normal-case` loses to its built-in `uppercase` everywhere, including the money table's total row and the chart tables.
2. A browser chunk used only by `/admin/campaigns` carries Prisma's error classes. No page from this round loads it.
3. The owner dashboard's "money moved" is a bucket by last update, not a record of money earned each day.

**A maker can now see, under each clip and on its Details page, who posted it, where, how many views each post got and what each post earned him; the money chart has real recorded history only from 2026-09-25 onward, and it says so.**
