**Nothing unremovable.** The one sandbox clipper and its account are gone (2 ledgered ids plus 3 arrival rows the app wrote for it), and a sweep of 341 id columns and 3 address columns finds 0. **One real row was changed, on purpose: this account's `users` row** (`isTestUser`, `sessionVersion`, `updatedAt`). **Five real rows were created by my own probe and then removed by explicit id:** arrival records the app wrote for this account while I tested it as him, listed below.

# BL-926: the named test clipper account is now an ordinary clipper

Base `main` @ `103c1d3e`. Branch `checkpoint/BL-926` has `38bf02b8` (the change file, its rollback and the proofs) and `0ce22a0b` (BACKLOG). Merge `1804575d`. Tags `pre-BL-926`, `post-BL-926`, `pre-merge-BL-926` and `post-merge-BL-926`, all pushed and verified (`safe-push`, twice). The merge tree `eff06a85` equals the branch tree. `checkpoint/BL-723` is not an ancestor. Worktree `C:\w\b926` removed and verified gone. **No product code and no .tsx changed, so there was no render and no accessibility pass.**

**Model split: 100 percent Opus, 0 subagents; no cheaper model ran anything.** Every raw output was read directly. Connection cap ONE: every script ran one statement at a time and never in parallel. No vendor call, no Apify actor. The only outside reads were GETs of clipershq.com's own public JavaScript (below).

**Not alone.** A second worktree, `C:\w\b925` (`checkpoint/BL-925`), was created two minutes before this round and had 7 uncommitted files by merge time. Nothing of mine touched it. It is on the same base, so its merge will need to union BACKLOG.

## PART 1: everything the account carries
**Handle and email are ONE account:** 1 row by handle, 1 by email, 1 carrying both, 1 distinct id (`cmobu3f0…`), CLIPPER, created 2026-04-23. The handle is redacted here as `1jac…test`; the email is not printed anywhere.

Compared column by column with the **1,711 ordinary clippers** (CLIPPER, not a test user, not deleted), found by handle and never by a hardcoded id:

| what it carries | ordinary clipper | this account | verdict |
|---|---|---|---|
| role / status / isDeleted | CLIPPER / ACTIVE / false | CLIPPER / ACTIVE / false | same |
| **isTestUser** | **false (all 1,711)** | **true** | **THE TREATMENT. Removed** |
| reviewer capabilities, scope, mode, canSeeDecided, invitedOnly | none, TRIAL | none, TRIAL | same |
| canActAsClipper, bulkAddBypass, clipSubmitBypass | false | false | same |
| trainer, poster status, bans (v1 and v2), strikes, manual bonus | none | none | same |
| marketplace v2 side (`marketplaceV2Role`, per campaign work, side requests) | none for 1,675 | **none, no side chosen anywhere** | same; nothing to preserve or reset |
| sessionVersion | 0 for 1,683 | 3 | a sign-in invalidation counter; grants nothing |
| tosAcceptedAt, lastLoginAt | mostly null | set (signed in `2026-09-23 12:04:35`) | his own history; grants nothing |
| **code allow-lists naming his id** | none | **none** | `MARKETPLACE_V2_PREVIEW_USER_IDS` and `FRESHNESS_EXEMPT_USER_IDS` are both EMPTY since BL-907 |
| `AUTH_OWNER_EMAIL` (auto-promotes to OWNER at sign-in) | not his | not his | compared in memory, neither address printed |

**The id in the codebase, counted with `git grep -c`:** 4 files, 12 occurrences, **0 under `src/`**. The first family is documents: `BACKLOG.md` 1 and the BL-904 report 1. **The second family is SQL scripts:** `scripts/migrations/BL-904-remove-test-fixtures.sql` 1 (a comment), and `scripts/hide-test-accounts-still-visible.sql` 9. That second file is a one-off from June that soft-hid this account as a test account under its old handle. Nothing runs it, and a re-run would abort on its own username check. It is named in BACKLOG and left as history. **No guard and no test names this id**, so nothing behaves differently because of the change. The handle appears only in documents; the email appears nowhere.

**What it holds, which did not change:** 0 clips, $0.00 earned, 0 payouts, 1 clip account (YouTube, APPROVED), 0 campaign memberships, no marketplace activity on either version (0 v2 clips made, 0 posts, 0 poster states, 0 side requests, 0 v1 submissions).

## PART 2: what the flag did, in both directions
`isTestUser` appears 215 times in 57 files under `src`; I read the 112 non-comment lines myself. Four pages hard-code `const isTestUser = true` for everybody, so they do not read him at all. **Production's own public flags were read from its shipped JavaScript**, since Next.js inlines `NEXT_PUBLIC_*` at build time:
• the bottom nav gate ships as `(t.isTestUser,!0)`, meaning always on for everyone;
• the sidebar calls `ex(j, …, !0)`, meaning **v2 is public**;
• `j = "OWNER"===e || !0===n`, meaning **the first marketplace (v1) is NOT public**, OWNER and test users only.
`/preview` is public in code (`PREVIEW_PUBLIC = true`).

**What he could reach ONLY through the flag, all of which he has now lost:**
1. **The FIRST marketplace (v1):** `/api/marketplace/browse` and `/api/marketplace/listings` answered him 200 and now 404, like every clipper. Its sidebar entry ("Marketplace (first version)") goes with it. That marketplace has no activity by anybody.
2. **The two test campaigns** ("Marketplace test campaign", ACTIVE; "Test", archived): gone from his campaign list, from both v2 campaign lists, from the v1 browse page and from `/preview`. The direct route answered 200 and now 404.
3. **The amber "TEST" badge** beside his name in the navbar.

**THE MARKETPLACE, IN ONE SENTENCE:** he keeps the NEW marketplace (v2), because production is built with it switched on for every clipper, and he loses only the OLD one (v1), which is still switched off for everyone except owners and test users.

**What it cannot unlock: nothing, because there is nothing.** He earned **$0.00** on any test campaign (0 clips anywhere). The BL-884 `CAMPAIGN_IS_TEST` refusal belongs to the campaign, not the person, so clearing the flag would not have released such money anyway.

**Newly visible anywhere? No.** No clipper-facing query excludes test USERS; every reader filters CAMPAIGNS or gates access. So clearing the flag adds him to no list he was hidden from.

## PART 3: the change
**Row snapshot before writing:** isTestUser true, sessionVersion 3, updatedAt `2026-09-23 12:04:35.626`; the other 83 columns hash to md5 `734170f0…`. **Rollback printed and written before the change**, one statement (`scripts/migrations/BL-926-untest-account-ROLLBACK.sql`):
`UPDATE users SET "isTestUser" = true, "sessionVersion" = "sessionVersion" + 1, "updatedAt" = now() WHERE id = 'cmobu3f02000a0pojvlorsdzr';`

**The write** (`scripts/migrations/BL-926-untest-account.sql`, run once through `run-mutation-once.js`) is exactly what the owner's own "Disable test user" button writes (`admin/users/[id]/route.ts`): isTestUser false, sessionVersion + 1, and updatedAt. By explicit id, never by pattern. It refuses unless the id is still that handle, CLIPPER, ACTIVE, not deleted, still a test user, with 0 clips and 0 payouts. **Result: 1 row, isTestUser false, sessionVersion 4, `2026-09-23 12:18:54.948`.**

**Row, not code, so NO deploy is needed.** `auth.ts` re-reads the row within 30 seconds of a sessionVersion change (a mismatch refreshes the session and never signs anyone out), or within 5 minutes regardless. **No treatment lived in code this time.**

**His work, money and side are identical, by fingerprint:** the 83 other row columns, clips, payouts, clip accounts, memberships, v2 made, v2 posted, poster states, side requests, v1 submissions and total earnings all hash **IDENTICAL** before and after.

## PART 4: proved ordinary by request
Local production build with production's measured flags (v2 on, v1 off, bottom nav on), dev bypass off. **Neither session carried an `isTestUser` claim or a refresh stamp**, so on every request `auth.ts` read role, status and the flag from the REAL row. Nothing I wrote was what the app read. The comparison clipper was a bl926sbx- account shaped like him (1 approved YouTube account, no clips); its flag was the column default, read back as false. **Before: 18 of 27 identical. After: 27 of 27.**

| request | him BEFORE | him AFTER | ordinary clipper |
|---|---|---|---|
| `/api/auth/session` | isTestUser true | **false** | false |
| `/api/campaigns` | 200, 5, test campaign present | **200, 4** | 200, 4 |
| `/api/campaigns/<test campaign>` | **200** | **404** | 404 |
| `/api/marketplace-v2/campaigns` | 2, test present | **1** | 1 |
| `/api/marketplace-v2/poster/campaigns` | 2, test present | **1** | 1 |
| `/api/marketplace/browse` (v1) | **200** | **404** | 404 |
| `/api/marketplace/listings` (v1) | **200** | **404** | 404 |
| `/marketplace/browse` page | test campaign in page | **absent** | absent |
| `/preview` page | test campaign in page | **absent** | absent |
| `/api/campaigns/past`, `/spend`, `/api/clips`, `/api/earnings`, v2 catalogue (and by test id), v2 role, v2 earnings, `/marketplace`, `/market`, `/market/campaigns`, `/dashboard` | same as ordinary | same | same |
| `/api/admin/users` 403, `/api/admin/clips`, `/payouts`, `/campaigns` 404, `/api/admin/sidebar-counts` 403 "Owner only" | refused | **refused** | refused |

**No admin or owner surface answers him.** One shared finding, not caused by the flag: the `/admin` PAGE answers any signed-in clipper 200 with the title "Admin — Clippers HQ" and refuses in the browser, while every admin API refuses (logged in BACKLOG). **Remaining difference: none.**

**Rows my probe caused on his real account, removed:** the app records an "arrival" when a v2 route opens, so the BEFORE probe wrote 5 `activity_events` for him (`cmue2k15…`, `cmue2k1y…`, `cmue2k3g…`, `cmue2k3m…`, `cmue2k4c…`, `12:18:20` to `12:18:24`). They were deleted by those 5 ids, with a check that they were his and inside the probe window; 0 left. The AFTER probe wrote none (arrivals are deduplicated hourly).

## PART 5: nothing else moved
• **Money files by `git rev-parse` (pre-BL-926 vs HEAD):** `clip-earnings-writer 80418a18`, `earnings-calc 00410634`, `balance 67c30c89`, `tracking 672d2ab3`, `invariant-middleware 61cef393` and `money-decimal ef5cdae7`, all IDENTICAL.
• **Invariants, full population, 16 of 16 at close:** 10,243 live clips, 0 breaches, 0 negative. 39 maker rows, 0 breaches. No double pay. 22 budgeted campaigns, 0 over (both v2 aggregates and the owner's cut counted). Paid is final: maker 0, v2 poster 0. **Never decrease: 10,335 clips, 0 decreased.** **ANGIE BROWN: $2,700.00, ACTIVE, spent $7.34.** **Both reconciliation forms: 0 rows at open and at close.** Every money fingerprint is identical. One check I inherited from BL-923 ("no real rules rows exist") failed at first because real clippers now hold 2; it was rewritten to ask whether the count moved (2 to 2), and passed.
• **Snapshot at T = `2026-09-23 12:14:40.28+00`, open against close:** users 1,789, campaigns 37, accounts 1,545, memberships 836, v2 clips 28, posts 39, poster states 81, rules rows 2, clips 10,335, activity 909, notifications 15,621 and audit 32,360, **every one identical in count and id fingerprint.**
• **Guards and builds:** build 0 on the untouched tree exit 0 (the clean baseline); tsc 0 errors; build #1 exit 0 and build #2 (committed tree) exit 0, each from a log with the exit code echoed. **All 21 prebuild guards pass, 0 FAIL lines. Hooks gate 0 errors, 10 warnings against 11**, as last measured. eslint present. BL-678's 11 guards untouched.
• **BACKLOG:** `## BL-` entries 233 → 234 (BL-723 has no heading of its own). Two follow-ups: the stale one-off SQL script, and the `/admin` page title.

## PART 6: in plain words
**What the account had:** the test user flag, which let it see the two test campaigns and the old first marketplace, and showed a "TEST" badge next to the name. Nothing else was special about it: no allow-list, no bypass, no capability.

**What it has now:** nothing extra. It answered 27 of 27 requests exactly like an ordinary clipper.

**Next time he signs in (or within 30 seconds if he is signed in now):**
• The "TEST" badge is gone.
• The test campaigns are gone.
• The sidebar shows one "Marketplace" entry, the new one; the "first version" entry is gone.
Everything else looks the same. His one YouTube account is still approved, and he has no clips or money to lose.

**Can he still reach the marketplace? Yes, the NEW one, because production is built with it switched on for every clipper; if that switch is ever turned off, he loses it too, because he is now an ordinary clipper.**

**To put it back, in one action:** run `scripts/migrations/BL-926-untest-account-ROLLBACK.sql` (or press "Enable test user" on his row in the admin users screen). No deploy is needed either way.

**Money that remains unreachable: none.** He has earned $0.00 anywhere, so nothing sits on a test campaign.

**Mistakes of mine, disclosed:** my first closing run failed one inherited check whose premise was out of date (above). My comparison script first named a `community_channels` table that does not exist; it was read from the schema and corrected before any run.
