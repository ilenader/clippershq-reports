# BL-890: let the owner see marketplace v2, and nobody else

**NOTHING IS UNREMOVABLE. The platform is byte for byte where it started: clips 10,226 before and after with an IDENTICAL clip fingerprint, campaigns 34, payouts 249 with an IDENTICAL payout fingerprint, zero rows matching `bl890sbx-`, zero carrying the sandbox marker, and `activity_events` back to the 0 rows it held before the round.** The teardown removed 72 ledger rows and then refused 36 more because their owner column held a REAL id, which is the lock working exactly as designed; those 40 remaining probe rows were deleted afterwards by an explicit list of 40 ids, never by a pattern, and the count is verified at 0. The user count moved 1,756 to 1,757 and **that was not me**: a real clipper signed up at 18:31:26 during the round, a product cuid with `isTestUser` false, while all nine of my sandbox users were deleted.

**THE MODEL SPLIT.** The strongest model decided the mechanism, wrote every line touching a gate, wrote both guards and wrote this report, reading `marketplace-flag.ts`, the navbar and the join route directly with no subagent between it and the source. One retrieval subagent on a cheaper model enumerated the gate's readers, the routes, the pages and the navigation; **its central finding was independently confirmed by me before it arrived** and every number below was re-measured.

## PART 0: the account

**THE HANDLE AND THE EMAIL ARE ONE ACCOUNT.** Counted three ways: one row by handle, one row by email, **one row carrying both**, and one distinct user id across the union. There is nothing to guess and nothing to stop for.

It is **not** the owner's own account. It is a **CLIPPER**, one of 1,757 users, created 2026-03-24, with `isTestUser` false and no marketplace role, and it is separate from the three OWNER accounts on the platform. That is why no existing mechanism reached it: the gate grants to OWNER or to test users, and it is neither.

**IT HOLDS REAL MONEY AND REAL WORK, which raises the stakes on getting this right:** 194 clips of which 178 are APPROVED, **$248.60** of clip earnings, **13 payouts totalling $991.11**, 8 clip accounts of which 6 are approved, and 6 campaign memberships. Granting a preview to an account that also earns is a different risk from granting it to an empty one, and it is the reason the mechanism below **writes nothing to that account at all**.

## PART 1: the mechanism

**HOW THE GATE WORKS TODAY.** `src/lib/marketplace-flag.ts:32-39`, three grants in order: `NEXT_PUBLIC_MARKETPLACE_ENABLED === "true"` opens it to everybody, `role === "OWNER"`, `isTestUser === true`, else false. 135 occurrences across 61 files read it, 35 of those files being the FIRST marketplace. Two navigation components hand-reimplement it (`sidebar.tsx:399`, `BottomNav.tsx:142`) for the v1 entry. `assertMarketplaceVisible` is exported and called by nothing.

**THE OPTIONS, AND WHY THE ALLOW-LIST WINS.** A per-user database column has to be read, and a read can fail, time out, return null, or be skipped by a path that forgot it. The role system means full administrative access. `isTestUser` is read in more than thirty places and CLAUDE.md makes it the gate for every new or redesigned surface, so flipping it hands one person every in-progress redesign at once, and it writes a falsehood into a column other code believes about a man with $991.11 of payouts. **An explicit allow-list of ids is one place to read, one place to revoke, and an empty list means nobody.**

**IT FAILS CLOSED BY CONSTRUCTION, and that was exercised rather than argued.** Nine shapes were put through the helper directly: null, undefined, an empty object, a user with no id, a null id, an empty id, an unknown id, the real id with one character changed, and the real id in the wrong case. **All nine were refused.** There is no query to fail because there is no query.

**IT IS SCOPED TO V2 AND NOT THE FIRST MARKETPLACE.** The shared gate covers v1 across 35 files, so widening it would have opened v1 too, which is not what was asked. All 13 v2 route files (15 handlers) and 9 v2 pages call `isMarketplaceV2VisibleForUser`, which is the shared gate OR the allow-list. **Every route and every page is gated: 15 of 15 handlers with 15 gate calls, 9 of 9 pages.** The OWNER only approval queue at `/marketplace-v2/admin` is deliberately excluded from the list, so a preview user sees the editor and poster screens and never the screen that decides what gets approved.

## PART 2: proving it is shut, which is the entire round

**THE DOOR BL-889 ADDED WAS VISIBLE TO EVERY ONE OF THE 1,749 PEOPLE ON THE PLATFORM.** `navbar.tsx` rendered an account menu entry reading "Marketplace: make clips or post clips" pointing at `/marketplace-v2?change=1` **with no condition around it**: the only wrappers were "is somebody logged in" and "is the dropdown open". Following it gave a notFound, so no ACCESS leaked, but the feature's EXISTENCE did, which is the single thing 404-rather-than-403 is used for in nine other files. **G1 to G4 of the gate guard passed the entire time, because not one of them looked at the navigation.** It is now behind the same call every page makes, and G5 is the check that would have caught it.

**AND THE TAB TITLE LEAKED IT TO PEOPLE NOT EVEN SIGNED IN.** Measured on the production build: a signed out visitor opening `/marketplace-v2/campaigns` received a not-found body and a document titled **"Campaigns you can post to — Clippers HQ"**. `export const metadata` is static, so Next writes the head before the component runs and the `notFound()` inside it cannot take it back. All nine v2 pages resolve their title per request now. Measured after: a refused clipper gets the bare brand on **all nine**; the named account gets **eight real titles** and the bare brand on the owner only queue.

**BY DIRECT REQUEST, AGAINST A PRODUCTION BUILD WITH THE DEV BYPASS OFF.** An ordinary clipper, a REVIEWER, a non owner ADMIN and a signed out visitor, each with his own account so no rate limit could be mistaken for a refusal: **15 of 15 v2 API routes refused for every one of the four, 60 of 60 requests, with zero answered 429.** Every refusal is a 404 and never a 403.

**AND IN A REAL BROWSER, BECAUSE THE PAGES CANNOT BE JUDGED ANY OTHER WAY.** This app renders a splash shell and every screen's words arrive after hydration, so the served HTML is identical for an OWNER and for a stranger. My first attempt measured the fetched body and reported three pages "rendering" for everybody including owners; **that was my check being wrong, not the product**. Page containment moved into the Playwright pass: **all four strangers refused on 7 of 7 pages, seeing none of the screens' words and no title naming them.**

**BOTH GATE GUARDS, WITH THEIR REAL RESULTS.** `check:v2-flag-gate` OK at 15 handlers, 15 gate calls, 9 of 9 pages, 1 of 1 linking file gated, 1 id on the list, 0 outside readers. `check:v2-role-is-signpost` OK at 13 routes, 0 mentions of the role column, 1 writer, 13 surfaces wired. **14 prebuild guards pass**, plus the hooks gate at 0 errors and 11 warnings, at its ceiling.

**WHAT THE GUARDS CAUGHT, INCLUDING MY OWN.** G1's regex hardcoded the helper name while its failure message interpolated the constant, so check and message could disagree; it is built from the constant now. **Two of my three new checks failed to fail on their first demonstration**: G5 accepted a file that merely IMPORTED the helper after the condition had been deleted, which is exactly what a careless edit leaves; G7 scanned only `.tsx` and never looked at a `.ts` library file, which is where a second reader would live. Both fixed. **All eleven checks across both guards were then demonstrated failing one at a time, each naming itself in its own failure list, every file restored byte for byte, the guard clean again after each.**

## PART 3: what he will actually see

**ALL 34 CAMPAIGNS ARE `NORMAL`**, unchanged since BL-885 measured the same, so **every v2 screen will be empty until he changes one**. Only two campaigns on the platform are live at all: one ACTIVE and one PAUSED. **None of the six campaigns he is a member of is live**; all six are COMPLETED or PAST.

**THE MEMBERSHIP GAP WAS FIXED, NOT ONLY FOUND.** BL-889 put a `campaignAccount.upsert` inside the post transaction, so posting creates the membership. And the sharper question behind it has a reassuring answer: **joining a campaign has never required anybody's approval.** `src/app/api/campaign-accounts/route.ts:68-83` checks only that the account belongs to the caller and is APPROVED, then creates the row. So the auto-join bypasses no gate that ever existed, including on a client campaign, and grants nothing a poster could not have granted himself one click earlier.

**NO SANDBOX CLIP WAS CREATED IN PRODUCTION.** If he wants a populated view he submits a clip himself as an editor, which is the walk he wants to experience anyway.

**WHAT EACH SCREEN SAYS WHEN IT IS EMPTY, so an empty page does not read as a broken one.** The campaign list says *"No campaigns yet"* and *"The owner has not opened any campaign to the marketplace yet. When he does, it will appear here. Nothing is wrong and there is nothing for you to fix."* The editor screen says *"You have not sent a clip yet"* and, while no campaign is marketplace typed, *"No campaign is taking marketplace clips right now. Check back later."* A campaign with no approved clips says *"Nobody has had a clip approved on this campaign yet."* The two money screens show zeroes with no alarm treatment. **The door itself is never empty**: it explains what the marketplace is and asks which one he is.

## PART 4: revoking it, and opening it wider

**TO REVOKE, IN ONE ACTION:** delete the one id line from `MARKETPLACE_V2_PREVIEW_USER_IDS` in `src/lib/marketplace-flag.ts` and redeploy. There is no row to undo, because **this round wrote nothing to his account**, verified after the fact: still a CLIPPER, still not a test user, still no marketplace role.

**WHAT HAPPENS TO WORK HE DID UNDER THE PREVIEW.** Nothing is deleted or reversed. A clip he submitted as an editor stays PENDING or APPROVED exactly as it was; if it was approved and somebody posted it, **his 45 percent keeps accruing**, because the editor leg is keyed to the CLIP and not to what the person may currently see. He simply stops being able to open the screens. Approving his own submission needs his OWNER account, which the preview does not grant.

**TO OPEN IT TO MORE PEOPLE LATER: the same mechanism.** Add their ids to the same array for a handful of named people, or, when it is time for everybody, set `NEXT_PUBLIC_MARKETPLACE_ENABLED` to `"true"`, which is the single switch that opens it platform wide without touching the list.

## PART 5: nothing else moved

- **All seven protected money files byte identical by blob OID** against the pre-round commit, plus `marketplace-v2-earnings.ts`, `marketplace-v2-writer.ts`, `marketplace-v2-sync.ts` and `marketplace-v2-poster.ts`.
- **NOT ONE CLIP CHANGED**: the fingerprint is md5 over every clip's id, earnings and status across 10,226 clips and it is identical before and after. **No payout** created, modified, approved or cancelled; 249 before and after with an identical fingerprint. No v2 row created anywhere; no person gained a marketplace role.
- **Every invariant across the full population**: earnings invariant 0 violations, no negative money on clips, editor legs or payouts, one editor leg per clip. **Both reconciliation forms clean before and after**, 0 leaks and 0 out of balance each time.
- **The one row I changed on the named account is none.** The grant is a source line, so the rollback is deleting that line rather than a SQL statement; the only SQL this round ran against production was the explicit 40 id delete of my own probe rows, printed before it ran.
- **25 of 25 renders** as the named account across the five screens at 320, 375, 414, 1280 and 1440: URL read back, `innerWidth` read back, **the pan measured at 0 pixels at every width**, one `h1` each, 0 dangling `aria-controls`, 0 duplicate ids, 0 controls white on accent, 0 unscoped table headers, 0 `var(--bg-page)`.
- **The proof ran three times.** Run 1 failed on two of my own checks, run 2 on one more, run 3 clean at 25 of 25. Every one of those failures was my measurement and not the product, and each is named above.

---

# WHAT TO DO NEXT, IN ORDER

1. **Redeploy.** The grant is in the code, so nothing happens until the new build is live. Nothing else needs flipping: leave `NEXT_PUBLIC_MARKETPLACE_ENABLED` alone.
2. **Sign in as your clipper account**, the one on the handle you named. Not your owner account.
3. **Open the account menu in the top right.** You will see a new entry, **"Marketplace: make clips or post clips"**. Nobody else on the platform can see that entry. Follow it, or go straight to **`/marketplace-v2`**.
4. **What you will see there:** a short explanation of what the marketplace is, then "Which one are you?" with two choices, "I make clips" and "I post clips", each saying what you do and that you earn 45 percent. Pick one; you get a confirmation that says you can change it any time. You can change it from that same menu entry whenever you like, and it never affects money.
5. **Expect every other screen to be empty, because it will be.** There are 34 campaigns and every one of them is still "Normal". Until you change one, the campaign list will say "No campaigns yet" and tell you nothing is wrong.
6. **To make it show something:** open one of the two campaigns that are actually live, set its type to **"Two ways to earn"**, and reload. It will appear in the campaign list with what it pays. You do not need to join it; posting joins you automatically, and joining never needed approval anyway.
7. **To see the whole thing end to end:** submit a clip as an editor from your clipper account, then approve it from your **owner** account (the approval queue is owner only on purpose), then post it from your clipper account and paste the link. That is the complete loop.
8. **To take it away again:** tell me, and one line comes out of one file. Nothing you did in the meantime is lost.
