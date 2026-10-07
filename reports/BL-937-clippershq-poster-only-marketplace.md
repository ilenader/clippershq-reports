# BL-937: the marketplace is poster only for clippers

**Date:** 2026-10-07 · **Type:** product change (permissions, upload token, guide, redesign) · **Spend:** $0.00 · **No paid vendor call, no Apify actor**
**Branch:** checkpoint/BL-937 · **Tags:** pre-BL-937, post-BL-937, pre-merge-BL-937, post-merge-BL-937 · **Rollback:** `git reset --hard pre-merge-BL-937` (the three schema additions are inert without the code)

Honesty tiers used below: **VERIFIED** (measured in this round by me), **READ** (a subagent reported it and I did not re-measure), **NOT DONE** (named, with why).

**UNREMOVABLE, FIRST LINE AS REQUIRED: 2 rows in `apify_usage_entries` name the deleted sandbox campaign and are KEPT ON PURPOSE.** They are production's own vendor-cost ledger: the walk's HTTP post created a tracking job after the world script had parked the others, and the **production** tracker tried to fetch that fake sandbox Instagram reel at 16:51:39 and 17:01:20 UTC (provider `none-instagram`, the chain failed, ledger worst-case estimate **$0.007 each, $0.014 total**). That breaks this round's "no paid vendor call" rule through a harness gap, not product code; deleting the rows would falsify the spend record. Everything else this round created is gone: **0 values carrying `bl937sbx-` in 684 text columns** apart from those 2.

---

## 0. Before anything: BL-936

**VERIFIED: BL-936 never ran on ClippersHQ.** No commit mentions it on any branch (`git log --all --grep=BL-936`: 0), no branch or tag carries it on origin, BACKLOG.md has 0 lines naming it, and no ClippersHQ session was live (ListAgents: the only busy peers were other projects). The reports repository holds two files numbered BL-936, and MANIFEST.tsv files both under the **leadgen** project, not this one. The database agrees: the four ordinary clips on ANGIE BROWN uploaded with the owner override on 2026-09-22 are **still ordinary** (`marketplaceV2PostId` null on all 4; 3 APPROVED, 1 PENDING). Nothing of BL-936 was performed here.

## 1. Investigation (changed nothing)

### Who holds the maker side (opening snapshot, DB now 2026-10-07 16:26:10 UTC)
Measured, handles redacted. The catch-up's numbers have moved since it was written:

| | catch-up | measured now |
|---|---|---|
| people who ever made a v2 clip | 6 | **8** (1 is an OWNER account, 7 are CLIPPERs) |
| people who ever posted | 9 | **10** |
| side choice EDITOR / POSTER | 11 / 26 | **19 / 39** |
| v2 clips | 27 | **38** (27 APPROVED, 4 PENDING, 7 REJECTED) |
| posts | 39 | **101** (101 maker legs, 101 platform legs) |
| switch requests | | **0 rows, any status** |
| open payout requests by a maker | | **0** |

The 8 makers: the owner's own account (5 approved clips, 28 posts of them, $2.87 accrued), and seven clippers holding 16, 1, 1, 2, 2 approved clips with $1.08, $0.87, $0.31, $0.28, $0.14 accrued, plus two whose only clips were rejected ($0). Total maker legs **$5.55**, platform legs $1.26. Four of the seven clipper makers have a PENDING or REJECTED clip; 4 clips are PENDING in the owner's queue, all from one clipper maker. All 38 clips are on ANGIE BROWN.

### Every place the maker side existed (counted at the base commit f8d63fae with `git grep -c`, summed per identifier)
| identifier | files | hits | after BL-937 |
|---|---|---|---|
| `marketplaceV2Role` (the side column) | 9 | 30 | 0 in code (the guard strips comments; 9 files still mention it in comments) |
| `checkV2Side` (side gate) | 5 | 9 | 5 files: the gate, the post route, the submit path, two comments; it now asks rule two only |
| `getV2RoleLock` / `getV2RoleStanding` / `setV2Role` | 2 / 7 / 6 | 7 / 13 / 12 | 0 / 0 / 0 (marketplace-v2-role.ts deleted) |
| `marketplaceV2SideRequest` (switch requests) | 3 | 7 | 0 queries (side-request lib deleted; routes answer 410) |
| `ArriveClient` (the chooser) / `V2Explainer` / `MarketplaceV2SidePanel` | 2 / 3 / 2 | 3 / 4 / 3 | 0 / 0 / 0 (files deleted) |
| `V2_ROLE_COPY` / `V2_LAST_CHANCE` / `NO_SIDE_CHOSEN` | 3 / 3 / 1 | 14 / 10 / 4 | 0 / 0 / 0 in code |
| `?change=1` (account menu door) | 3 | 4 | 0 links (1 comment) |

**The second family, asked rather than assumed.** v2 clips are created in exactly two places: `submitV2Clip` (the maker's form) and **`marketplace-v2-conversion.ts:399`** (BL-885's owner conversion, which mints a v2 clip attributed to whatever person the owner names). The second is OWNER only and an owner decision with a recorded reason, not a submission, so it is left unchanged and put to the owner below. The first marketplace (v1) has its own unrelated poster/creator model and is not touched.

**What the side actually gated, which is why removing it mattered.** `checkV2Side` refused posting with `NO_SIDE_CHOSEN` to anybody whose side column was null, so **1,787 of 1,845 people could not post a single clip until they had opened the chooser**. The poster route now asks rule two only.

### How roles are modelled, and why EDITOR is a grant
* **Primary role:** `User.role` (CLIPPER, ADMIN, OWNER, CLIENT, REVIEWER), one per person, in the session, gated by `requireOwner` / `requireRole` (120 files) and 264 inline `role === "OWNER"` comparisons. Measured: 3 OWNER, 28 REVIEWER, 0 ADMIN.
* **REVIEWER** adds capability keys (`reviewerCapabilities`, `hasCapability`); it auto grants clip approve/reject, and the reviewer-config PATCH rewrites the whole array.
* **Additive grants** ride on any role: `canActAsClipper` (1 user), `isTestUser`, `bulkAddBypass`, `clipSubmitBypass`, and REFERRAL_MANAGE riding a CLIPPER (BL-205). Owner toggled, audited, one helper.

**EDITOR is built in the additive-grant shape** (`users.marketplaceEditor`, read only by `getMarketplaceSubmitter`, written only by `setMarketplaceEditor`). A new primary role would replace CLIPPER, and 7 of the 8 makers are clippers whose dashboard, payouts and cashout hang off that role; a capability key would sit in an array that an unrelated reviewer-checklist save rewrites and that hands out approve and reject. The grant is read from the database on every request, never from the session.

## 2. Every clipper is a poster

**Server side, not a hidden tile.** One submit path, `submitMarketplaceClip` (src/lib/marketplace-submit.ts), is the only caller of `submitV2Clip`, and only two doors call it: the form route `/api/marketplace-v2/clips` and the token route `/api/marketplace-v2/upload`. It asks `getMarketplaceSubmitter` FIRST: OWNER yes, a live non-banned non-deleted person holding the EDITOR grant yes, anybody else **403 `MARKETPLACE_SUBMIT_TEAM_ONLY`** with: "Only the Clippers HQ team sends clips to the marketplace. Your job is to post them: pick a clip, post it on your page, and paste the link here to get paid." **VERIFIED by direct request** as an ordinary clipper (403, that code, those words, 0 rows written) and as an existing maker (403).

**Removed from every surface, phone and desktop:** the chooser page (/market now server-redirects a clipper to /market/campaigns and the owner to his overview), the "Change what you do" switch tile, the account menu's "Make clips or post clips", the BL-892 two-sides explainer, and both "This is the last moment you can change sides" warnings (submit form and post page). The four side routes (`/api/marketplace-v2/role`, `/side-request`, `/api/admin/marketplace-v2/role`, `/side-requests`) answer **410 `SIDE_CHOICE_RETIRED`** behind their old gates and read and write nothing.

**The old data is left alone.** `users.marketplaceV2Role` (19 EDITOR, 39 POSTER), `marketplaceV2RoleChosenAt` and `marketplace_v2_side_requests` (0 rows) are not updated, deleted or read: the guard counts **0 code readers** of either.

**Existing makers keep what they have.** Approved clips stay in the catalogue and keep earning their 45 percent: the maker leg is keyed to the clip's `editorId`, written at submission, and no money path reads the grant. Pending submissions stay in the owner's queue. A former maker sees "Clips you made" (his clips, every post of them, his maker money page and the withdraw link) with no Send button and the line: "The Clippers HQ team sends new clips now. Your clips stay up, keep earning you 45 percent of every post, and your money is right here." **VERIFIED on a real-shaped sandbox maker** (a CLIPPER with two approved clips made before the change, posts by others, $20.55 accrued through one production tick): refused a new clip; his 2 clips listed with their posts; his maker dashboard showed $20.55 earned; `/api/earnings` counted the $20.55; **his payout request for $13.13 was accepted (201)**; his leg read $20.55 before and after.

**Rule two kept, deliberately:** a person never works both halves of one campaign. A former maker cannot post on the campaign he made clips for (VERIFIED: 403 `OTHER_SIDE_ON_THIS_CAMPAIGN`, new words: "You have clips of your own on this campaign, so you cannot also post on it. You can post on any other campaign."). The switch request that used to be the way past it is retired; see the owner decisions.

**Each two-sided guard retired or replaced, deliberately.** `check:v2-role-is-a-gate` (BL-893, R1 to R8) is **replaced** by `check:v2-submit-is-team-only` (T1 to T9), mapped one for one in the guard's header: R1/R2 become T1 (zero readers and writers of the side column), R3/R4 become T3/T4/T5 (one submit path, team gate first, 404 before 403, rule two on the post route), R5 retired (no lock), R6 becomes T6 (EDITOR grant: one writer, OWNER on every handler, audited), R7/R8 kept as T9; new T2 (switch requests unread), T7 (token stored only as a hash), T8 (no console call in the token path, no session read in the token route). **Demonstrated failing one check at a time** on a scratch copy of the tree (scripts/sandbox/bl937-guard-demo.mjs): **15 separate mutations, each caught by its own check, and the unmutated copy passes (16/16)**. The other 22 prebuild guards were run unchanged and pass.

## 3. The EDITOR role
The owner grants or removes EDITOR from the person's profile (/admin/users/[id], "Marketplace editor" panel, replacing BL-893's side panel), with a required reason. `PATCH /api/admin/users/[id]/marketplace-editor` is OWNER only on both handlers; `setMarketplaceEditor` refuses an empty reason, an owner target and a deleted account, and writes the column and the audit row **in one transaction**. **VERIFIED:** no reason, 400; a clipper calling it, 403; the owner's grant writes `MKT2_EDITOR_GRANTED` naming owner, person, change GRANT, the reason and the DB's `now()::text`. Removal takes effect on the editor's **next request** (read fresh): VERIFIED, refused 403 right after removal, and his token refused by the same gate.

An editor submits through the same path. **VERIFIED:** submission 201 `WAITING`, visible in the owner's queue, approved by the owner from the queue, visible in the editor's own list; an editor who has posted on a campaign is refused sending clips to it (rule two) and allowed on another.

**No owner figure reaches an editor, a maker or a clipper.** VERIFIED against live response bodies: the editor is refused the queue, overview, dashboard, tokens, guide setting and grant routes (401/403/404 each); **12 forbidden names** (ownerCpm, agencyFee, clientName, aiKnowledge, budget, cpmInstagramOwner, cpmTiktokOwner, cpmYoutubeOwner, lockedOwnerShareDecimal, ownerEarnings, platformEarning, spendTotal) counted as JSON keys across every non-owner body the walk received (**12 bodies**: the poster's campaigns page, the maker's clip list, maker earnings and `/api/earnings`, the editor's clip list, and as the editor `/api/campaigns/spend`, v2 campaigns, catalogue, one catalogue clip, both earnings routes and poster campaigns): **0 of each**.

The editor's maker leg is paid to his own account, as today (default; the alternative is put to the owner).

## 4. The upload token
`marketplace_upload_tokens` stores **only `sha256(value)`** (unique index), the label, the bound submitter, creator, created/expiry/revoked/last-used times and a use count. The value (`chq_mkt_` + 32 random bytes, base64url) is returned once in the create response with `Cache-Control: no-store` and never again. The owner screen "Guide and tokens" (/market/admin/setup, OWNER only, 404 for anybody else) creates (name, sends as owner or a current editor, 30/90/365 days), shows the value once in a read-only field with Copy and "you will not see this token again", lists tokens (never the value or hash) and turns one off with an inline confirm.

`POST /api/marketplace-v2/upload` (Bearer token; `campaignId`, `title`, `driveUrl`, optional `description`) reads no session, verifies by hash, applies the v2 404 gate to the bound submitter, rate limits 120/hour per address and **60/hour per token**, then calls `submitMarketplaceClip(via: "TOKEN")`: the same team gate, rule two, BL-908 folder refusal, stored Drive file id, duplicate rule, preview, and on approval the same frame job. **Token uploads always wait in the review queue**, even when bound to the owner. Every use, success or refusal, writes an audit row naming the token by its **label** with the result, status and code.

**VERIFIED:** a clipper cannot make a token (403); a token cannot be bound to a non-editor (400); the stored hash equals sha256 of the value; **the value appears in 0 rows of every text column of 5 tables that could hold it**; the owner's list carries neither value nor hash; an upload lands PENDING under the bound editor with the Drive file id stored exactly as the form stores it; the audit row carries the label and result and not the value; a folder link is refused with **the identical sentence** the form returns; the token opens **nothing else** (7 other routes, GET and POST, each 401/403/404); revoke, then the very next upload is **401 `TOKEN_REVOKED`**; expired **401 `TOKEN_EXPIRED`**; made up **401 `TOKEN_INVALID`**; none **401 `TOKEN_MISSING`**; a token bound to an editor who lost the grant is **403 `MARKETPLACE_SUBMIT_TEAM_ONLY`**; **0 occurrences of any token value in 8,814 bytes of the server's log**. No token value is printed in this report. The integration note (endpoint, headers, fields, success and every refusal, the campaign ids) is on the owner screen.

## 5. The guide
Global link: a row in the existing key/value table `gamification_config` (key `marketplace_v2_guide_url`), written only when the owner saves it; per campaign override: `campaigns.marketplaceGuideUrl`. https only, at most 500 characters (http and `javascript:` VERIFIED refused 400); an editor cannot set it (403). **If no link is set, nothing is shown.** VERIFIED: with nothing set, no card and the guide step left out of the steps; a campaign with its own link carries the quiet link on its clip page; a campaign without one carries none. The global path was proved **inside a transaction that rolls back** (the live key is never written: 0 rows before and after).

Shown prominently on arrival (/market/campaigns, where /market sends every clipper) as a card, and as a quiet "Open the page guide" link (BL-923's rules link shape, same name on both, new tab said in words) on every other clipper screen and beside the post form. The words shipped, exactly:
* Heading: "Start here: build a page that earns"
* "This guide shows you, step by step, how to set up a page that earns."
* "Follow every step before you post."
* "A page that does not follow the guide will not earn."
* Button and quiet link: "Open the page guide" (screen readers add "(opens in a new tab)")

## 6. The redesign
**Direction.** The house system rules here (dark only, #2596be, CSS variables, lucide, no dashes), so the frontend-design skill's anchors were applied as discipline rather than a new palette: content that names real information only, and one memorable move, **the numbered job rail** on every clipper screen: Read the guide, Pick a clip, Post it on your page, Paste the link here, Get paid for views (the guide step is dropped when no guide exists).

**The clipper's flow is one job:** the one line ("The Clippers HQ team makes the clips. You post them on your page and get paid for the views."), the guide, the rail, then campaigns, clips, post, paste the link, money. BL-923's simplicity and its rules gate are untouched. Tiles per person: every non-owner sees **Post a clip** and **Money**; an editor adds **Send a clip**; a former maker adds **Clips you made** (never both); the owner sees **Send a clip, Overview, Review clips, Guide and tokens**. The owner's queue, overview (its side-request section removed) and the BL-935 post tool keep working (BL-935 tool VERIFIED listing a campaign's clips).

**Accessibility.** Reviewed twice by the accessibility lead (plan: 32 points; built diff: 1 major, 5 minor, all fixed before build #2): one name for both guide links and no second one on a clip page; the steps a labelled list, not an h2 above every h1; errors take focus after they render; the token confirm keeps focus until the list reloads; the editor panel survives a failed reload. 44px targets measured on every new control (tiles, guide button 44px, editor panel, token confirm 44px). Visible focus via `V2_FOCUS` on every new control; status regions exist before any message; the token value never enters a live region. **Removed from the tab order, all intended and named:** the switch tile, the account menu entry, the chooser page, both last-moment warnings, the explainer's show/hide toggle, the side panel's controls on the profile page, the owner's side-request approve/reject buttons, and the Send button for a non-editor.

## 7. Proof
**Model split.** Opus (this session) wrote every line of the permission gate, the submit path, the EDITOR grant, the token's storage and verification, the guide setting, the money-adjacent checks, the guard, every page change and this report, with no subagent between it and the source. Subagents: one Haiku enumeration of the UI surfaces (**READ**, then re-counted by me with `git grep -c`: VERIFIED); four Sonnet render-and-review passes in parallel, one or two surfaces each, cap **4 browsers against one local server and 0 extra database connections** (their tallies **READ**, every failure re-run by me: VERIFIED); the accessibility lead three times (plan review, file sign-off, post-build diff review: findings **READ**, all fixes written by me). Connections: one local server's pool plus one script at a time, never concurrent with the server's heavy phases.

**Sandbox, prefix `bl937sbx-`, opening snapshot first** (C:/bl937-sandbox/snapshot-open.json, DB now 2026-10-07 16:26:10 UTC, taken before any sandbox row existed). Eight people, one per path: a new poster, a second poster, an existing maker, an ordinary clipper, three editors (granted, removed, rule two) and an OWNER (kept for the shortest window the walk allowed). Two MARKETPLACE_ONLY test campaigns with budgets **$333.33 and $211.17**, so no split divides evenly. The maker's money was made the production way: a post through `createV2Post`, then ONE tick through `_bl163RunTrackingJobForTest` with prefetched stats (**33,337 views → maker $20.55, poster $20.55, platform $4.57**). Setup was 4 checks, 4 passed.

**The walk, over HTTP against a local production build with every vendor, email and storage key blank, real Auth.js sessions minted only for ledger ids.** Run 1: 67 passed, 9 failed. Every failure was the harness: it read a 307 header where the app streams `NEXT_REDIRECT`, read client text the app shell draws only after hydration, used a test campaign that BL-884 deliberately makes non-withdrawable, and scanned a route that clippers reach in restricted form by design. Run 2: 74 passed, 2 failed (my payout body named USDC where only USDT is accepted, and the log path was given in a form Node could not open; that check failed honestly at 0 bytes). Both runs were torn down. **Run 3, on a fresh world: 76 passed, 0 failed.** Every refusal was asserted as its own status and never 429. For the cashout step only, the sandbox campaign was made real and **COMPLETED**, hidden from every clipper list (lists show ACTIVE and PAUSED only) and closed to posting, from **16:46:07 to 16:46:10 UTC (2.6 s)**, then put back.

**Builds and guards, all VERIFIED from logs with the real exit code.** `tsc --noEmit` 0 errors after every change (5 retired sandbox proofs of the two-sided model marked `@ts-nocheck` as records; they no longer run). **Build #1 BUILD_EXIT=0** (branch, before review fixes). **Build #2 BUILD_EXIT=0** (with the fixes). All **23 prebuild guards pass**, including the replacement guard and the hooks gate at **0 errors, 10 warnings** (the cap is 11). The 11 BL-678 guards are unchanged. Guard demonstration: **16/16**. **The six money files are byte-identical**, checked by blob OID against `pre-BL-937` (`git rev-parse <base>:<path>` = `git hash-object <path>` for all six), and none appears in the diff.

**Renders, VERIFIED** at 320, 375, 414, 1280 and 1440, viewport set on the context, `innerWidth`, URL and pan read back beside every shot. On build #2:
* poster arrival: **55/55** (no guide: 4 steps, no card; guide: card, 5 steps, new tab, copy exact, 44px button; account menu has no "Make clips or post clips")
* poster clip page: exactly one guide link, 44px, no side warning, pan 0
* former maker's "Clips you made": no Send button, note shown, 3 tiles with that one current
* his money page: **$20.55 on screen at all 5 widths**, rendered inside a 30.5 s real-and-COMPLETED window, 16:50:38 to 16:51:08 UTC
* editor screen and form: no side warning
* owner Guide and tokens: reveal focus, read-only field, Done returns focus, inline confirm focuses "Keep it" (44px both), Escape backs out
* owner profile editor panel
* owner overview: side requests gone, 4 tiles

**Two pans at 320, both PRE-EXISTING and both in BACKLOG:** the overview's campaign filter `<select>` sizes to its longest option (it panned 35px only because the sandbox campaign's name is long), and the profile page's "15 days ... 1 year" toggle. Screenshots are kept locally and not published: they show real campaign names.

**Invariants across the FULL population, after teardown: 13 passed, 0 failed.**
* nothing of this round survives; every v2 table holds its opening count (38 / 101 / 101 / 101), with 0 real rows created since
* ANGIE BROWN: $2,700 budget, $15.86 spent with both v2 aggregates
* BL-627: 22 budgeted campaigns, 0 over budget
* BL-696: 0 double pays across four tables
* earnings invariant: 10,340 live clips, 0 violations
* BL-824: 36 known pre-existing explained pairs (BL-883), 0 negative maker legs
* **both reconciliation forms: 0 rows** (leaks only, and every row with a verdict)
* the owner's test campaign is untouched
* **101 of 101 real posts' three legs byte-identical** to the opening snapshot
* **all 6 real makers hold exactly their opening legs and cents**

The reconciliation forms were run at the close, not separately at the opening. The opening state is pinned instead by the row-by-row snapshot, which matched.

**Rows touched outside the sandbox, named.**
1. Schema, additive only, through run-schema-sql.js: `users.marketplaceEditor` (default false, 0 set), `campaigns.marketplaceGuideUrl` (null everywhere), and the table `marketplace_upload_tokens`. RLS is on with 0 policies, read back. No `prisma migrate`.
2. **No real person was granted EDITOR, and the global guide key was never written** (proved inside a rollback).
3. Every sandbox editor or token submission went through the real path, which notifies every OWNER. Each of 3 runs created 1 "clips waiting" notice per real owner (3 owners): **9 notices** and 18 "not-attempted" email records, nothing sent (the server's email key was blank, "send returned false"). All were deleted by exact id by `bl937-cleanup-owner-notices.ts`, which deletes only rows that name sandbox clips. Each notice existed for minutes; whether an owner saw one in his bell is unknown.
4. Production's own "cron did nothing" alert at 16:32 also reached the then-existing sandbox owner in-app. It was deleted with him.
5. Teardown run 1 deleted 4 email records addressed to sandbox mailboxes before reading their outcome. Runs 2 and 3, which printed first, show the same shape every time: all "not-attempted". Run 1's 4 are inferred to be the same, not verified.

**Teardown:** every ledger id plus prefix sweeps. Run 3 removed:

| table | rows |
|---|---|
| audit_logs | 24 |
| activity_events | 28 |
| marketplace_upload_tokens | 11 |
| user_lifecycle | 7 |
| users | 8 |
| v2 clips | 6 |
| posts | 3 |
| maker legs | 3 |
| platform legs | 3 |
| clips | 3 |
| payout request | 1 |

The worktree, the sandbox directory, the cookies file and the server are removed. The server was stopped by its own PID taken from its port, never by name.

## Owner decisions (each built on the safe default)
1. **Who receives an editor's 45 percent maker leg?** Default built: the editor's own account, as today. Alternative: the company, which would need its own money round.
2. **Do your own clips skip review?** Default built: **yes**. A clip you send from the form goes live at once, approved by you.
3. **Do editor and upload-token clips skip review?** Default built: **no**. Both wait in Review clips, including a token bound to you.
4. **May the 7 former makers post on ANGIE BROWN?** They made clips for it. The never-both-halves rule stands, and the switch request that could lift it is retired. Default: no.
5. **Should the BL-885 conversion only name you or an editor as a converted clip's maker?** Today it can name anybody. Default: unchanged.
6. **Should the guide link be limited to Google Drive?** Default: any https link.

## What the next round must finish
Nothing is half built. Every part shipped and was proven in order. Left for later rounds, all in BACKLOG BL-937:
* the two pre-existing 320px pans
* the campaigns heading's leftover focus ring
* a sandbox-aware recipient filter for owner notices
* parking sandbox tracking jobs after the walk as well as after the world (the gap behind the $0.014)
* the stale comment at `MpFilterPills.tsx:83`

**In one line:** A new clipper now lands straight on the campaigns, under one line and the owner's guide (when set), a numbered "how it works", and Post a clip / Money tiles: he picks a clip, posts it and pastes the link, with no choice to make and no way to send clips. **All 8 existing makers kept every cent: 6 with accrued legs hold exactly their opening amounts, and 2 who were only ever rejected had none.**
