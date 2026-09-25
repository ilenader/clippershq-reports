# BL-932 — a maker now sees every post of his clip, and his views and money day by day

**UNREMOVABLE: none.** Teardown removed 190 sandbox rows. The sweep then found 0 prefixed values across 343 id columns, and 0 of 60 ledgered product rows remain.

**Shipped 2026-09-25.** Branch `checkpoint/BL-932` (3c6a2bb4), merged to main as 675d31a3.
Rollback: `git reset --hard pre-merge-BL-932`, then in the SQL editor `DROP TABLE IF EXISTS marketplace_v2_editor_daily;`.

**Model split.** Opus wrote every line of UI, every query, every chart's data source and this report. One subagent was used, the accessibility lead, which reviewed the changed code (READ); the render measured its claims (VERIFIED). No other subagent was used.

## Decided, not drifted: BL-882 and the owner, side by side
* **BL-882** proved from the live response that no poster's identity reached a maker. Its reasoning: BL-876 question 16 was open, and an open privacy question defaults to NO.
* **The owner** answered the poster half first: a poster may not see which other posters took the same clip. That still holds, and no poster surface changed.
* **This round:** the owner has now answered the maker half with YES, a maker sees who posted his clip.
* **Earlier step:** BL-897 had already put poster usernames on the money page. BL-932 is the same rule, applied to the clip card and to a new Details page.

## PART 1: what existed
* **Clips page:** `editor/page.tsx:36` renders `editor-client.tsx`.
  * The card showed two sentences, then "Open in Drive" as a text link, then a Details *toggle*.
  * The toggle opened a panel holding only "Posts so far: N" and his note to the owner.
  * Data came from `/api/marketplace-v2/clips` (`route.ts:44`).
* **Details:** no page existed, only that panel.
* **Money page:** `editor/earnings/earnings-client.tsx`, fed by `buildV2EditorDashboard`.
  * It had count tiles, the money tiles, the campaign table (with its across and down checks) and BL-897's per-post list.
  * It had no chart.
* **Where views came from:**
  * **Maker:** `MarketplaceV2EditorEarning.views`, a snapshot the tick writes only when it writes money.
  * **Poster and owner:** the newest `ClipStat` (`poster-dashboard.ts:154`, `owner-overview.ts:277`).
  * **Measured live:** on 11 of 67 posts the maker read a different number, up to 1,465 views apart and 3,711 views in total.
  * **Now:** the maker reads the same `ClipStat` expression they do. Proven equal on 8 of 8 posts against the owner's view and 6 of 6 against the poster's.
* **Money history:** none existed.
  * The maker's earnings table holds one row per post, overwritten in place by each tick.
  * The owner dashboard's "money moved" files a post's whole current amount under the day its row last changed.
  * **Built instead:** an additive table, `marketplace_v2_editor_daily`. It has one row per maker per UTC day, the amount before the fee is nullable, and it has a foreign key to users with cascade delete. RLS is on.
  * **What writes it:** a new tracking post-step, `v2-maker-daily`. It reads his payable legs through `v2EditorPayableWhere`.
  * **Cost:** one groupBy plus one upsert per maker, each tick. There are 8 real makers today, so about 2,900 rows a year.
  * **Nothing before 2026-09-25 exists or is drawn.**

## PART 2: every post under each clip
* **What the card shows:** "Posted N times", then the 3 most viewed posts, then "See all N posts".
  * Each row has the poster's handle, a platform icon, the views, "You earned $X before the fee", and a Watch link.
  * The rows sit at full card width.
* **Copy, before (22 words):** "Approved. Posters can see it." and "Any poster can now find this clip and post it. You earn 45 percent of every post."
* **Copy, after (12 words):** "Posters can post it now. You earn 45 percent of every post."
* **Empty state:** "Approved. Waiting for its first poster." became "Nobody has posted it yet."
* **Height at 320 px, the 6-post card:**
  * First render: 1,444 px. The rows sat beside the thumbnail, so the 38-character handle wrapped one letter per line.
  * Fixed: rows moved to full card width, and the card is now 852 px.

## PART 3: the Drive button and the Details page
* **Drive button:** `DriveButton`, 48 px tall, full width on phones.
  * Text is `--mp-surface-0` on the accent, measured at 5.89 to 1 in the browser.
  * The new tab is announced in words.
* **Details page:** `/market/editor/clips/[id]` shows the clip, its campaign, when it was sent and approved, his note, and a real table of every post.
  * The table has a caption, `scope=col` and `scope=row` headers, and a total row.
  * Columns: poster, platform, when posted, views, what he earned before the fee, and the live post.
* **Reconciliation:** it adds up down each column, measured in the browser: 12,347+5,003+3,331+2,677+1,399+777 = 25,534, and $7.61+3.08+2.05+0+0+0.48 = $13.22.
* **Cash** is worked out once, on the total, by the payout function, because the fee is taken on what he withdraws.

## PART 4: the charts
* Both charts use `V2SeriesChart`, which wraps `AreaGradientChart`, the analytics component (BL-908). No new chart style.
* **Views each day:** comes from the recorded `ClipStat` history. Its days add up to the views total on the page: 24,420 = 24,420.
* **Money each day:** only the recorded daily rows.
  * With no rows yet, the page says so in words ("has not started yet").
  * With one day, it says "starts on …, the first one appears once a second day is recorded".
  * With six sandbox days it draws them: the drawn days sum to $15.05, which is the last row minus the first.
* The money page's tables and both of its checks are unchanged. The charts are an added section.

## PART 5: the leak sweep, against the live responses
* **The list:** 30 forbidden names (`grep -c` = 30), including the poster's earnings fields, `ownerCpm`, `agencyFee`, the owner's cut, `lockedOwnerShare`, `clientName`, `aiKnowledge`, `budget`, `spend`, CPMs and wallets. Wallet-shaped strings were searched for too.
* **Result:** 0 hits in 9 maker responses (clips route ×2, details ×5, money ×2).
  * *Correction:* the commit message says 11. That is a miscount; it is 9.
* **The sweep can fail:** run over the owner's own overview, it finds `posterGross`, `posterCash`, `posterFeePercent`, `platformLeg` and `budget`.
* **Only his own clips:** maker A's responses contain nothing of maker B's clip, and asking for B's clip returns 404. B's route holds only his own post.
* **Posters:** a poster's 4 marketplace routes contain no other poster's handle or post.
* **Failure paths, each with its own user, none a 429:**
  * signed out: 401;
  * v2 not visible: 404;
  * banned: 403;
  * another maker's clip: 404;
  * a poster asking: 404;
  * a clip that does not exist: 404.

## PART 6: proof
* **Sandbox** (prefix `bl932sbx-`, opening snapshot taken first): 13 people and 1 test campaign.
  * There were 9 posts, made by `createV2Post` and priced by `recomputeV2PostEarnings`, at views that do not divide evenly.
  * Tracking jobs were switched off at creation, and vendor keys were blanked.
* **Views and money pages:** these leave out test campaigns by design. So the campaign was made non-test and archived at the same time, in 6 windows totalling 93 s (10:32 to 10:44 UTC).
* **Final results:**
  * Test-phase proof: 35 of 35.
  * Flip-phase proof: 12 of 12.
  * Renders: 45 of 45 at 320, 375, 414, 1280 and 1440, with width and URL read back, every state checked in words, and pan 0.
* **Every run, including failures:**
  * The world script crashed twice before creating anything (a title length, then a `server-only` import), then passed 12 of 12.
  * First card render: 10 failures from my own wrong expectation.
  * First details render: 15 failures. This found a real defect: `TableHead` forces capitals, so handles showed in upper case.
  * First no-history render: 5 failures, from copy that named a button which was not there.
  * First money render: 13 failures. This found a real pre-existing defect: the 38-character handle made BL-897's post list pan the page 158, 103 and 64 px at 320, 375 and 414. Fixed with `break-all`.
* **Guards:** all 22 prebuild guards pass, and the hooks gate is 0 errors, 10 warnings (limit 11).
  * The two guards I touched failed on demand, one break at a time, with each file restored byte-identical: 4 of 4.
* **Money files:** the 6 money files are byte-identical by blob OID (80418a18, 00410634, 67c30c89, 672d2ab3, 61cef393, ef5cdae7), and `tracking.ts` is not in the diff.
* **Invariants:** 11 of 11 across the full population, including both reconciliation forms (0 rows each), no campaign over budget, and ANGIE BROWN at a $2,700 budget with $14.48 spent.
* **Closing snapshot:** every count identical.
  * Three figures moved: +$0.01 in clip earnings, +$0.01 in maker legs, and one payout fingerprint.
  * All three trace to real activity *before* the sandbox existed: 4 payouts marked PAID from 09:58 to 10:11, and the 10:00 tick.
* **Real rows written:** only 8 rows in the new daily table (today, $4.60 in total), written by the real writer. The cron overwrites them every tick after deploy.
* **Build:** tsc clean, and `BUILD_EXIT=0` on every build. The merge tree equals the branch tree.
  * Pushes to main and the branch were verified.
  * Tags: `pre-BL-932`, `post-BL-932`, `pre-merge-BL-932`, `post-merge-BL-932`.
  * BACKLOG went from 238 to 239 entries.
  * `checkpoint/BL-723` was not merged.
* **Cleanup:** the worktree was removed and `ls` confirms it is gone.
* **Accessibility review:** passed, nothing blocking.
* **Connections:** one database client per script, run one at a time, beside the local server's own pool. Render contexts were capped at 5.
* **Vendors:** no vendor call was made.

## Found, not fixed (BACKLOG BL-932)
1. `TableHead`'s `normal-case` loses to its built-in `uppercase` everywhere, including the money table's total row and the chart tables.
2. A browser chunk used only by `/admin/campaigns` carries Prisma's error classes. No page from this round loads it.
3. The owner dashboard's "money moved" is a bucket by last update, not a record of money earned each day.

**A maker can now see, under each clip and on its Details page, who posted it, where, how many views each post got and what each post earned him; the money chart has real recorded history only from 2026-09-25 onward, and it says so.**
