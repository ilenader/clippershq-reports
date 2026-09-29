**UNREMOVABLE: none.** Disclosed side effect, removed: the sandbox budget cap test made the tick fan out 9 in app "Campaign auto-paused" notices to the three OWNER accounts (two real, one test), each naming a `BL935-SANDBOX` campaign, visible from 21:08 to about 21:29 UTC 2026-09-29, then deleted. Their 18 emails were NOT sent (the proof ran with the email key blank; each was recorded as not attempted, and those 18 records were deleted too). Only a content free "refresh your bell" ping went out with them.

# BL-935 — the owner's Submit Clip tool, extended to marketplace posts

**Date:** 2026-09-29 · **Branch:** `checkpoint/BL-935`, merged to `main` at `f8d63fa` · **Tags:** `pre-BL-935`, `pre-merge-BL-935`, `post-BL-935` · **Rollback:** `git reset --hard pre-merge-BL-935`
**Model split:** Opus wrote every line and read every measurement. Two read only accessibility reviews by a subagent (READ, then applied and VERIFIED by the render pass). No cheaper model enumerated anything; every file and route below was read directly.
**Limits kept:** one database connection at a time (every process runs `connection_limit=1`; scripts and the dev server were never up together). No paid vendor call and no Apify actor: every process ran with every vendor key blank, the new path makes no fetch at all, and every tick was driven with STUBBED stats through the real tick (`_bl163RunTrackingJobForTest`, cron shape). No `prisma migrate`. No Prisma in the browser bundle (the new component imports React, lucide and `Button` only).

## THE HEADLINE: yes, it had already happened

| clip (tail) | created (UTC) | status | views (latest) | poster holds | owner cut | maker got | maker should have (45%) |
|---|---|---|---|---|---|---|---|
| wgurtb | 2026-09-23 12:20 | APPROVED | 7,585 | $1.60 | $0.79 | $0.00 | $0.68 |
| ah6th8 | 2026-09-23 12:20 | APPROVED | 8,033 | $1.69 | $0.83 | $0.00 | $0.72 |
| slho1c | 2026-09-23 12:20 | APPROVED | 7,578 | $0.71 | $0.35 | $0.00 | $0.31 |
| wrh6hf | 2026-09-23 12:13 | PENDING | 547,187 | $0.00 | $0.00 | $0.00 | $22.16 if approved |

* All four: `OWNER_OVERRIDE_SUBMIT` audit rows, one poster (id tail y6jj), one Instagram account, on **ANGIE BROWN**, which has been MARKETPLACE_ONLY since 2026-09-18 19:58 UTC (campaign audit trail), so the tool was pointed at a marketplace campaign five days after it became one. Timestamps cast to `::text` against DB `now()` 2026-09-29 20:33 UTC.
* **Nothing has been paid out.** The poster's last PAID payout is 2026-09-18 and none of their payout requests names this campaign.
* Poster over-credit today: $4.00 held against $1.71 due under 45/45/10. Maker short: $1.71. The PENDING clip was put back to pending by the owner 30 seconds after submit; **approving it as it stands would pay the poster the whole $49.25 gross** at its $0.09 rate.
* **Who the maker is cannot be proven from data.** The four links are not any v2 post's link. The only maker whose clips this poster posted that day is the owner's own maker account: five clips made 13:36 to 13:42 and posted by this poster from the same account 13:55 to 13:58, about 90 minutes after the four submits. That pattern fits "submit clip did not work for the marketplace, so the owner made the clips and had them posted", in which case the maker's share is the owner's own. The owner decides.

## PART 1 — the existing tool, read completely

Page `src/app/(app)/admin/submit-clip/page.tsx` (admin perimeter). Routes `POST /api/clips/owner-submit` (single, `route.ts:23` `requireOwner`, 60 per hour) and `POST /api/clips/owner-submit-bulk` (up to 30, `route.ts:32` `requireOwner`, 20 per hour). Both call `validateOwnerSubmitContext` once and `processOwnerSubmitLink` per link in `src/lib/owner-submit-core.ts`. **Who: OWNER only** at the API; ADMIN and REVIEWER can open the page and are refused 403 by the routes.

| gate | ordinary owner path | where / why |
|---|---|---|
| campaign status | only AUTO paused refused; manual pause, DRAFT, PAST, COMPLETED pass | core:101 |
| campaign type | **not checked (the hole)** | BL-878 left it ungated on purpose |
| test campaign | refused in override mode | core:106 |
| 30 minute window | **bypassed** | the owner's reason to use the tool |
| duplicate URL | refused, campaign scope, live rows; P2002 backstop | core:172, core:333 |
| per account unique | the partial unique on (campaign, normalized URL) applies | P2002 path |
| budget | no pre check beyond AUTO pause; money via `writeClipEarnings` (L1 lock, BL-901 row lock) | core:369 |
| account | must be the target's, APPROVED, not removed; URL platform must match | core:130, core:193 |
| person | CLIPPER, not BANNED, not deleted | core:115-117 |
| owner posting pause (v2 strikes) | **bypassed**, asserted by `check:v2-strike-sites` | "the owner acting" |
| side lock, rules seen | never met (an ordinary clip) | n/a |
| TikTok photo block | single route only (route:62); **bulk skips it** | finding 5 |

**Writes:** Clip APPROVED with `isOwnerOverride` true and CPM stamps (core:299), a first ClipStat ALWAYS, zeros when the fetch fails (core:322), an ACTIVE tracking job at the next hour (core:329), earnings through `writeClipEarnings` when views > 0 (core:369), an `AgencyEarning` row (core:380), one audit row (core:390). It calls the stats provider per link (core:239).

## PART 2 — what was built

**"What are you submitting?"** at the top of the page: Ordinary clip or Marketplace post (native radios). The marketplace form: campaign (marketplace campaigns only), poster search, then one LINE per link: the approved clip, the poster's account, the live link. Pasting several links fills several lines. Up to 30. Every line comes back created or refused with its own sentence; refused lines stay in the form with their reason and original line number.

**One path creates the post: `createV2Post`**, the function the poster's own route calls. `src/lib/owner-submit-marketplace.ts` writes nothing itself (no create, no money write, no transaction), so `marketplaceV2PostId`, `isMarketplaceClip` false, the three legs, the ACTIVE job and the membership row all come from the one place that already gets them right. A post lands **PENDING in Review**, exactly as the poster's own would; the ordinary tool's auto approval is NOT copied, because approving a v2 post outside the review route would be a second approval writer.

| gate | marketplace version | why |
|---|---|---|
| OWNER only, rate limit | applied (20 per hour) | mirror |
| campaign type | must be MARKETPLACE_ONLY or BOTH | the point |
| ended, archived | refused | createV2Post's own rule |
| AUTO paused | refused | mirror |
| 30 minute window | bypassed, so no provider call | mirror |
| person | CLIPPER, not BANNED, not deleted, can see the marketplace | mirror, plus the poster route's first gate |
| account | theirs, APPROVED, not removed, platform matches the link, campaign takes that platform | mirror |
| TikTok photo | refused | mirror of the single route |
| owner posting pause | bypassed | mirror |
| rules seen (BL-923) | bypassed: the owner acts for them; `check:v2-rules-gate` R2 still allows only the poster route to ask | decided |
| never chose a side | bypassed: since BL-903 that is a navigation preference | decided |
| **side lock, per campaign** | **refused** if the poster makes clips on this campaign, unless the owner approved their switch request for it (`hasOtherSideOnCampaign`, lifted unchanged from `checkV2Side`) | absolute |
| **maker posts own clip** | **refused** (createV2Post gate zero) | absolute |
| **duplicates** | same clip twice on ONE account refused; same clip on several of their accounts allowed; their own link twice or somebody else's link refused | absolute |
| test campaign | decided by the POSTER's own role and test flag | as their own post (BL-904) |

**Bulk and budget:** lines run one at a time, so two lines for one clip and account get a sentence, not a constraint error. Each post is written at $0.00; its money arrives later through `writeClipEarnings` (L1 lock and BL-901's row lock). **A null stat:** the new path makes no fetch, so it fabricates nothing; the one zero ClipStat every v2 post carries is `createV2Post`'s own and is inherited unchanged (finding 3).

**The hole is closed:** `validateOwnerSubmitContext` now refuses MARKETPLACE_ONLY first, 409: "This is a marketplace campaign, so an ordinary clip here would pay the poster everything and the clip's maker nothing. Use Marketplace post on this page instead: pick the marketplace clip, the poster and their account, then paste the link." On the page the ordinary form blocks in place with a Switch to Marketplace post button. **BOTH is not refused** (an ordinary clip there is a clipper's own work, paid correctly as one); the page shows a note pointing to Marketplace post when the video is somebody else's clip.

**Guard `check:owner-marketplace-submit`** (in `prebuild`): O1 exactly one `createV2Post` call; O2 no writer or money call in the new files; O3 no rules seen, owner pause, freshness or stats fetch, and the side rule asked once; O4 `requireOwner` per handler; O5 the ordinary core selects `campaignType` and refuses MARKETPLACE_ONLY. **Demonstrated failing: 11 mutations on scratch copies, each refused by exactly its own check, the other four passing; the clean tree 5 of 5.** `check:v2-single-share-writers` lists no new writer, correctly: the new files never call `writeClipEarnings`.

## PART 3 — the four past clips: not rewritten, here is how

BL-885's conversion is the tool. **It has no screen** (the "Convert a clip" link on the marketplace overview opens /admin/clips, which does not call it), so it is run from the route while signed in as the owner, in the browser console on clipershq.com:

1. Preview, changes nothing: `fetch('/api/admin/clips/<CLIP_ID>/convert-to-marketplace?editorId=<MAKER_USER_ID>').then(r => r.json()).then(console.log)`
2. Convert: `fetch('/api/admin/clips/<CLIP_ID>/convert-to-marketplace', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ editorId: '<MAKER_USER_ID>', reason: 'Owner submit on a marketplace campaign, BL-935', v2ClipId: '<optional, the maker's existing clip>' }) }).then(r => r.json()).then(console.log)`
3. Undo, if needed: the same POST with `{ undo: true, reason: '...' }`.

The four are the owner override clips on ANGIE BROWN dated 2026-09-23 in Admin, Clips (ids ending wgurtb, ah6th8, slho1c, wrh6hf). Cost, from the conversion's own formula (the poster's paid floor on this campaign is $0, so it never binds):

* **wgurtb, ah6th8: extra cost $0.00.** Spend on each falls ($1.60 to $1.52, $1.69 to $1.61) because the poster's 5% bonus leaves with the 100% share; the maker is paid $0.68 and $0.72.
* **slho1c: the preview will say $0.81, and it is wrong for this clip (finding 4).** The owner lowered this clip's rate to $0.09; the conversion prices at the campaign's $0.20, the next tick at the clip's $0.09, so an hour later it settles at about $0.68 total, less than today's $0.71.
* **wrh6hf (PENDING): convert BEFORE approving, or reject it.** Approved as it stands the poster takes $49.25; converted, the tick pays $22.16 / $22.16 / $4.93 at its $0.09 rate (the preview again shows the campaign rate).
* The owner cut rows ($1.97 across the three) are left alone, as ADDS intends.

## PART 4 — proof

**Sandbox** `bl935sbx-`, test people and test campaigns only; opening snapshot at DB now 2026-09-29 20:52:37 UTC. A script refused to create due tracking jobs within five minutes of the :00 cron and parked every sandbox job in 2099 seconds after reading it back ACTIVE.

* **In process, 86 of 86** (`bl935-prove.ts`, drives `runOwnerMarketplaceBatch`, everything the route runs after its perimeter). A single owner post and a poster's own control post (`createV2Post`, the route's exact arguments) each: `marketplaceV2PostId` = the post, `isMarketplaceClip` false, PENDING, `isOwnerOverride` false, post row correct, job ACTIVE and due, three legs present summing to $0.00, membership row, one audit row on the owner's only; **equal to the control field for field.** A bulk of eight lines: 4 created (including one clip on two accounts), 4 refused, each with its sentence. **All 23 single line refusals and the 4 refused bulk lines fired with their exact words, none 429**, each path on its own poster except the two duplicate checks, which by definition reuse one poster. After approval (identical for both) and the real tick at 12,347 views and $1.37 (a gross of $16.92 that cannot split evenly): owner post and control **identical**: poster $7.61, maker $7.61, platform $1.70, sum $16.92, **AgencyEarning $7.53 written under ADDS.**
* **Budget addendum, 8 of 8** (first run 7 of 8: my assertion read the test harness's stats flag rather than the money written; corrected, re-run). Three owner bulk posts on a campaign with room each hold exactly the control's money; $73.35 of $500.00.
* **HTTP, 8 of 8** on a local dev server: no session 401, clipper 403, admin 403, owner list 200, owner post 200, unknown campaign 404, and **both ordinary owner routes answer 409 with the words on a MARKETPLACE_ONLY campaign.**
* **Render, 80 of 80** at 320, 375, 414, 1280, 1440: `innerWidth` and URL read back, pan 0 px at every width and state, the blocked form, the BOTH note, the switch (focus on its heading), four links pasted into four lines (announced), a real mixed submission through the route (2 created, 2 refused, focus on the Results heading), every control at least 44 px. The first full run caught two real defects, both fixed: focus landed on the page body after submit, and the first line's random key caused a hydration mismatch.
* **Money files byte identical by blob OID** (`git rev-parse pre-BL-935:<f>` = `HEAD:<f>`): clip-earnings-writer.ts 80418a1, earnings-calc.ts 0041063, balance.ts 67c30c8, tracking.ts dcc8d48, clip-earnings-invariant-middleware.ts 61cef39, money-decimal.ts ef5cdae. `tracking.ts` is not in the diff.
* **Invariants 11 of 11 before AND after**, full population: no overpayment on 22 budgeted campaigns, no double pay, earnings = base + bonus on 10,334 live clips, BL-824, the v2 unique indexes, **both reconciliation forms 0 rows before and 0 after** (no stored money row changed), **ANGIE BROWN $2,700 budget, $15.89 spent, intact.** Closing snapshot equals the opening one on every count except `clip_stats` +65 (the live 21:00 tick on real clips).
* **Teardown:** 195 ledger lines plus everything owned by a sandbox row; 343 id columns and every text column of rows created since 20:50 scanned: **0 remaining.** The first teardown left 29 audit rows and 6 tick audit rows (it deleted users before the rows naming them); fixed in the script and removed.
* **Build:** clean tsc baseline on `pre-BL-935` (0 errors; a first baseline was polluted by my dev server's generated types and was re-taken after clearing `.next`), branch tsc 0, `npm run build` exit 0 twice (the second on tree `5a032f8`, identical to the merge tree), 23 prebuild guards including the 11 BL-678 guards, hooks gate 0 errors and 10 warnings (unchanged). BACKLOG: 242 `## BL-` entries (241 + this one); the other 24 `## ` lines are sub-headings inside older entries, and the 482 inline BL mentions are references, not items. `checkpoint/BL-723` not merged.

## Found, not fixed (each needs its own round)

1. **The tick's budget cap truncation fails for a marketplace post on a split campaign.** Near the cap it recomputes the three legs, trips its own maker leg consistency check and rolls back, scaling up or down. It fails closed (nothing overpaid), but the post gets none of what is left, the campaign is not paused by that tick, and every OWNER receives a "Campaign auto-paused" notice quoting a spend that never landed (this round's disclosed notices). Reproduced on a poster's own post, so it is the tick's and not this path's. Not reachable today: no marketplace campaign is near its cap. Lives in `tracking.ts`; an Opus money round.
2. **BL-785's fix was never merged.** It sits on `checkpoint/BL-785`; `owner-submit-core.ts` still stores a zero first snapshot when the stats fetch fails.
3. `createV2Post` writes one zero ClipStat at posting for every v2 post, the poster's own included. Owner decision whether to skip it for all posts.
4. BL-885's conversion prices at the campaign rate while the tick uses the clip's own rate, so its preview is off for a clip whose rate was overridden.
5. The ordinary bulk owner route skips the TikTok photo block the single route applies.
6. The old ordinary form keeps its accessibility debt (an emoji in the account warning, labels that are not labels, errors by toast only). Untouched.

**4 past owner submitted clips on marketplace campaigns were paid as ordinary clips (3 approved holding $4.00, 1 pending, none paid out), and the owner can now submit marketplace posts, one link or up to 30, through the poster's own post path.**
