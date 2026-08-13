# BL-804 — the chat is gone, the report button is all that is left, and it is visible at 320 for the first time

**2026-08-13 · DB `now()` = `12:48:47.310+00` (first read) to `13:14:50.929844+00` (last) · BUILD.**
Base `origin/main` @ `d004b396`, branch `checkpoint/BL-804` @ `9d62049a`, **verified pushed** (origin == local), tags `pre-BL-804` / `post-BL-804` on origin. Isolated worktree `C:/b804`, short path, `node_modules` never junctioned, removed at the end. Every database read through `scripts/run-select.js`, every timestamp cast `::text` against DB `now()`. Handles redacted, no wallet address read or printed.

## THE FIRST LINE, AS THE BRIEF DEMANDS

> **Nobody is mid-conversation.** The newest unanswered message from a clipper is **8 days old** and the chat has been silent since; the last message of any kind was `2026-08-05 22:23:08.154`. Nobody is sitting in front of a typing indicator.
>
> **But 18 people asked something that was never answered, and 7 of them had explicitly asked for a person.** Oldest 135 days, newest 8. Removing the chat does not create that debt, it makes it permanent in that channel. **Every one of those 18 is preserved and readable by the owner at the new `/admin/chat-archive`**, and the archive marks each one in words: *"The last word here was theirs, so this one was never answered."*

## PART 0 — WHAT THE CHAT WAS DOING, MEASURED BEFORE ANYTHING WAS REMOVED

| measure | value |
|---|---|
| conversations · escalated · messages · participant rows · people | **54 · 13 · 108 · 115 · 50** |
| last message of any kind | **2026-08-05 22:23:08.154**, 8 days ago |
| conversations that contain any message at all | **37** (17 were opened and never written in) |
| last word was a **clipper's**, i.e. unanswered | **18** |
| of those, flagged `needsHumanSupport` | **7**, newest `2026-08-11` era at `2026-07-11 23:40:17.732`, oldest `2026-04-23` |
| last word was staff | 19 |

**The 18 unanswered, redacted, newest first:** `ez…_0` 8d, `ab…10` 31d, **`rh…22` 33d (asked for a person)**, `ab…10` 33d, `ri…52` 36d, `ca…zy` 43d, `th…er` 46d, `a.…23` 63d, `el…m_` 64d, `pl…56` 71d, `du…c_` 74d, **`di…33` 75d**, **`da…03` 78d**, **`se…85` 83d**, **`ze…0a` 84d**, **`ym…96` 109d**, **`ab…43` 112d**, `du…c_` 135d. The seven in bold had asked for a human.

### Everything that read the chat, named with file:line, and what happened to it

| reader | what it did | outcome |
|---|---|---|
| `src/components/chat/ChatWidget.tsx` (1,579 lines) | the whole widget | **deleted** |
| `src/app/api/chat/conversations/route.ts` | list + create conversations | **deleted** |
| `src/app/api/chat/conversations/[id]/messages/route.ts:222,280,283,348,392,403,445` | send, the **AI auto-reply**, and every `needsHumanSupport` write, set and clear | **deleted** |
| `src/app/api/chat/conversations/[id]/read/route.ts` · `campaign-chats/route.ts:119` · `unread/route.ts` · `messageable-users/route.ts` · `sse/route.ts` | read receipts, campaign threads, unread badge, recipient list, the live socket | **deleted** |
| `src/lib/chat-access.ts` (204 lines) | `canMessage`, `canAccessConversation`, `getMessageableUsers` | **deleted**, only the chat routes imported it |
| `src/lib/sse-broadcast.ts` (47 lines) | `registerSSEClient` / `unregisterSSEClient` | **deleted**, its only importer was the chat SSE route (its own comment claiming a community consumer was stale) |
| `src/components/layout/BottomNav.tsx:334-338` | `onChatTap`, the only dispatcher of `support-chat:open` | **deleted**, and see PART 3 for why it was already dead |
| **`src/app/api/admin/payouts/unpaid/notify/route.ts:94-154`** | the **`dm`** action wrote a payout reminder into a `Conversation` | **removed and refused**, see below |
| `src/app/api/admin/command-center/route.ts:4` | imported `activeSSEConnections` | **import deleted.** It had not been READ since F-PRESENCE moved the online count onto `countOnlinePresence`; the dashboard number is unchanged |
| `src/app/api/problem-reports/route.ts:7` | a comment saying it does not touch the flag | left, still true |

**The payout DM is the one that mattered.** Left alone it would have written reminders into a surface nobody can open: the owner would read "sent" and the clipper would see nothing, which is worse than the action not existing. The route now refuses it explicitly and the button is gone from `/admin/payouts`. **Proven live:**

```
POST /api/admin/payouts/unpaid/notify {"action":"dm"} as OWNER
  -> {"error":"Direct messages are no longer available. Use email or notification."} | HTTP=400
```

**Email and the in-app notification are untouched**, so the owner keeps two working ways to reach a clipper about an unpaid balance.

## PART 1 — THE HISTORY IS KEPT, IN FULL, AND READABLE

**Kept and readable by the owner. Nothing is deleted, nothing is hidden.** No table dropped, no row deleted, no destructive migration, **no schema change of any kind** and no `prisma migrate`. The three Prisma models stay in `schema.prisma` precisely so the rows stay addressable.

| measure | before | after |
|---|---|---|
| conversations · escalated · messages · participant rows · people | 54 · 13 · 108 · 115 · 50 | **identical** |
| last message | `2026-08-05 22:23:08.154` | **identical** |
| whole-table message fingerprint | `ba05c17fec2d0e17cf65db92041ac4b9` | **identical** |
| messages written during the round | — | **0** |
| conversations created during the round | — | **0** |

**Why kept rather than exported and dropped:** an export is a file that goes stale and gets lost, and dropping the tables would make the 18 unanswered questions unrecoverable at the exact moment the owner might want to answer them another way. Keeping the rows costs nothing and loses nothing.

**How the owner reads it: `/admin/chat-archive`, new, OWNER-only.** It is a **server component with no client bundle, no form, no composer, no send control and no API route behind it**, so it is read-only *by construction* rather than by discipline. Conversations sit behind a native `<details>` disclosure, because 108 messages on one page in an app shell with no skip link would otherwise be 108 tab stops. `Message.isAI` is surfaced **in words** ("Automated assistant", "Not a person"), because an AI reply carries an OWNER's `senderId` and would otherwise be attributed forever to a named human.

**Gate proven at content level, not by status code**, because a Next dev `notFound()` streams a 200 (the existing `/admin/problem-reports` behaves identically):

```
OWNER    -> heading present, 145 UTC timestamps (37 conversation stamps + 108 message stamps)
ADMIN    -> not-found page, 0 rows      REVIEWER -> not-found page, 0 rows
CLIPPER  -> not-found page, 0 rows
```

## PART 2 — THE CHAT IS GONE FROM EVERY SURFACE, PROVEN BY ASKING THE SERVER

**Ten files deleted, 3,217 lines removed.** The composer, the conversation view, the AI auto-reply and the escalation path all went with the routes that held them. **Removing it from the menu while leaving the route reachable is not removing it**, so it was proven by direct request as a CLIPPER rather than by reading code:

```
GET  /api/chat/conversations              -> 404      POST /api/chat/conversations          -> 404
GET  /api/chat/campaign-chats             -> 404      POST /api/chat/conversations/x/messages -> 404
GET  /api/chat/unread                     -> 404
GET  /api/chat/sse                        -> 404      CONTROLS, same server, same cookie:
GET  /api/chat/messageable-users          -> 404        /api/problem-reports  -> 405
GET  /api/chat/conversations/x/messages   -> 404        /api/referrals        -> 200
GET  /api/chat/conversations/x/read       -> 404        /api/campaigns        -> 200
```

**Nine refusals against three live controls**, so the 404s are the routes being gone and not the server being broken. **`grep -c "/api/chat/" build.log` on the production build manifest returns 0.** Every `needsHumanSupport` reader is named in PART 0 and every one is either deleted or a comment.

**Reported and NOT removed, because the brief describes the widget and its 54/108/50 dataset:** `/community` is a separate feature on separate models with **201 channel messages and 94 ticket messages**, and `/marketplace/messages` is buyer-and-seller negotiation on `MarketplaceMessage` / `MarketplaceChatMessage`, both currently at **0 rows**. Removing marketplace messaging would break the marketplace's own flow. **Both are the owner's next decision and neither was touched.** So the accurate statement is: **the support chat is gone; two other messaging surfaces still exist and are named here rather than quietly left.**

## PART 3 — ONE REPORT ENTRY, VISIBLE AT EVERY WIDTH

**The phone defect was worse than BL-803 found.** The launcher was `hidden md:flex`, and the fallback its own comment describes did not exist: since BL-405 the `TABS` memo has substituted the external Discord link for the chat tab for **every non-owner role**, not only test clippers, so **nothing ever dispatched `support-chat:open`** and the support chat was **unreachable on a phone entirely**, not merely hard to find.

**Where it now lives, and why.** One labelled pill, fixed bottom right, **at every width**. Not an icon-only bubble: an icon-only floating button is the most commonly misread control on a phone, and this one has to be findable by somebody who has never looked for it. It is lifted **104px** below md so it clears the phone tab bar by 20px, which is more than the 12px minimum spacing between adjacent targets, and it drops to the ordinary corner inset from md up where that bar is hidden. **It is deliberately NOT hidden on scroll** the way the tab bar is: the only support entry point disappearing on scroll direction is unrecoverable for somebody who does not scroll.

**The Discord Support tab is deliberately KEPT.** Removing the only reply-capable channel in the same round as the chat would leave a dead end, so the phone bar still shows five tabs and the fifth is still Discord. What changed there is only that the dead `"chat"` kind is gone; **the rendered bar, its accessible names and its indicator geometry are unchanged**.

**One box, one button, no categories, no priorities, no dropdowns**, writing its own `problem_reports` row exactly as BL-797 built it. **The exact confirmation shipped:**

> ### Thanks for reporting this
> Your message is with the team, along with the page you were on.
> This form does not send replies. For anything that needs an answer, ask on Discord (opens in a new tab).

and the promise is made **before** sending too: *"This form goes one way. It reaches the team, and no reply comes back here. For anything that needs an answer, ask on Discord."* **No "we", no "soon", no "get back", no future tense, no ticket number, no queue position**, machine-checked on the rendered panel.

**BL-797's context capture is retained and is now honestly disclosed.** Captured: page path with the query string stripped in the browser, coarse OS, coarse browser, installed-app versus browser tab, viewport width, client and server version, role, `::text` timestamp, clips awaiting a decision, rejections in the last 30 days with the most recent date, and any balance held below a campaign minimum. **The pre-send sentence used to name only the page, device and browser** while quietly attaching the rejection count and the blocked balance; it now names all of it, and says outright that a wallet address, a password and anybody else's information are never included. **The table has 21 columns and none of them is a wallet, a token, a password or another clipper's data.**

## PART 4 — THE OWNER'S SURFACES BOTH SURVIVE

`/admin/problem-reports` still renders, newest first, grouped by page and time, with the unread count, mark-read and the reporter link. **Proven at all five widths, and with real rows in it.** `GET /api/admin/problem-reports` is **200 for the OWNER and 403 for a CLIPPER**. Its one copy change: the description no longer says reports arrive "in the chat widget", because they do not.

**BL-776's evidence panel is untouched**: `src/app/(app)/admin/clips/page.tsx` is **byte-identical by blob OID (`d1ebebe5`) on both refs** and `ReviewEvidencePanelMount` is still there.

**The archived chat is at `/admin/chat-archive`**, linked from the owner sidebar under Problem Reports.

## PART 5 — RENDERED, AT ALL FIVE WIDTHS, 92 ASSERTIONS, 0 FAILURES

Real Chromium, **CSS viewport set through `browser.newContext({ viewport })`** rather than `resize_window`, which is what let BL-799 report success while `window.innerWidth` never moved. `window.innerWidth` was read back and asserted equal to the asked width every time.

| checked at 320 / 375 / 414 / 1280 / 1440 | result |
|---|---|
| CSS viewport really is the asked width | **5/5** |
| report launcher rendered, visible, fully inside the viewport, at least 44px tall | **5/5**, measured `167.5 x 44` at every width |
| launcher clears the phone tab bar | **5/5** |
| **NO chat launcher anywhere in the DOM** | **5/5** |
| page copy names no chat | **5/5** |
| form is one box and one send button, no dropdowns, no overflow | **5/5** |
| focus lands on the panel heading, not the textarea | **5/5** |
| the one-way promise is made before sending | **5/5** |
| owner report list renders, no sideways scroll, no longer says "chat widget" | **5/5** |
| confirmation, at **320 and 1440** by a real send | **thanks / no reply / no chat / no promise / focus moved: 5/5 each** |
| chat archive renders, **no composer and no send control**, no sideways scroll, at 320 and 1440 | **3/3 each** |

**One honest note on the render pass.** The first run reported the launcher missing at 320. It was not missing: 320 is the first width in the loop and `next dev` compiles a route on its first request, so the page had not finished rendering. The script now warms every route first and the failure did not recur. **I am reporting the false failure rather than only the clean second run.**

## PART 6 — THE EVIDENCE

| claim | evidence |
|---|---|
| no chat exists and none is reachable by URL | 9 refusals (7 GET, 2 POST) at **404** against 3 live controls; **0** `/api/chat` routes in the build manifest; 10 files deleted |
| the entry is visible and usable at 320 | measured `167.5 x 44` fully inside a real 320px viewport, panel opens, form usable, no sideways scroll |
| a report sends and confirms with no implied reply | 3 real rows created, confirmation machine-checked for "we / will / get back / shortly / soon as" |
| the context is captured | a real row reads `pagePath=/earnings, viewportWidth=320, displayMode=browser-tab, clientVersion=0.1.1, serverVersion=0.1.1, roleAtReport=CLIPPER, pendingClipCount=0, recentRejectionCount=0, blockedBalanceCents=null` |
| the owner's list still works | 200 for OWNER, 403 for CLIPPER, rendered at all five widths with real rows |
| the 108 messages are preserved and readable | fingerprint `ba05c17f…` identical; the owner's archive renders 145 UTC timestamps; every other role gets the not-found page |
| nothing that read the chat is broken | every reader named in PART 0, each deleted or updated; `tsc` **0 errors**; `BUILD_EXIT=0` |
| no clip or money change | invariant **0 violations**; **0** payouts created, modified, approved or cancelled in the round; **0** messages and **0** conversations written |

**The payout count moved from 167 to 168, and it was not this round.** The 168th row was created at **`2026-08-13 12:34:46.065`**, fourteen minutes **before** this round's first database read at `12:48:47`. Payouts touched inside the round: **0**. The single clip decision inside the round was made by the **real OWNER account** at `12:54:15.188`.

**Rows I created and how they were removed.** Three `problem_reports` rows on the synthetic `dev-clipper-001` seed account, sent so the confirmation and the owner list could be photographed with real rows instead of an empty state: `cmsrjdw7n…`, `cmsrjgoo5…`, `cmsrjgt6a…`. **All three already deleted** by `scripts/migrations/BL-804-remove-proof-rows.sql`; `problem_reports` is back to **0 rows**. No real user, clip, earning, payout or conversation was touched.

## ACCESSIBILITY

**Reviewed by the lead before any code was written, and eleven blocking items were implemented rather than argued with.** The load-bearing ones: the launcher at `bottom-4` would have **overlapped the phone tab bar by 34px and covered its last tab at 320**; there is **no `scroll-padding-bottom` anywhere in the repo**, so a focused control at the foot of a page would scroll exactly under the launcher (2.4.11), fixed with matching bottom padding and scroll-padding on `<main>`; the global focus ring is `#2596be` and the launcher was `bg-accent`, an **accent ring on an accent button at 1.00:1** (2.4.7); the form's only two actions used `ring-white` with a white offset on a white card, **1.00:1 in light theme**; a full-screen panel had no dialog contract, now `role="dialog" aria-modal="true"` with the house trap from BL-736, whose document-level capture Escape supersedes BL-797's panel-scoped one that failed when focus sat on the launcher; the launcher stayed tabbable behind an open mobile drawer, now `inert` on `drawerOpen`; **`--bg-page` does not exist repo-wide** despite CLAUDE.md naming it, so `--bg-primary` is used; and the pre-send disclosure named the browser but not the rejection count and blocked balance, which is not consent.

**Carried across from BL-797 unchanged because they are right:** `aria-disabled` rather than native `disabled` on submit (which the trap's `tabbableWithin` correctly keeps as a tab stop); focusing the heading rather than the textarea, so the phone keyboard does not scroll the one-way sentence out of view; no `maxLength`, with the overflow named instead; the 130ms clear-then-set so two identical refusals both speak; band-crossing-only count announcements; the draft surviving a close; and clearing the text only after a confirmed 2xx.

**Two additive tokens:** `--text-danger` (`#f87171` dark, `#b91c1c` light), because the over-the-limit message was a hardcoded `text-red-400` measuring **2.77:1** on the light card. The blocked submit button now **swaps its surface instead of dropping to `opacity-40`** (2.38:1 dark, 1.73:1 light), because an `aria-disabled` control is still operable and the inactive-component exemption does not apply to it.

**Honest limit: five of the six specialist reviews had not returned when the code was written.** The lead's own eleven blocking items are all implemented and verified; anything the outstanding five raise is not in this round and is not claimed to be.

## REPORTED, NOT FIXED

• **`/community` and `/marketplace/messages`** are separate messaging surfaces, named in PART 2 with their live counts. **The owner's next decision.**
• **`src/lib/email.ts:908 sendChatReplyEmail`** still says "New message in your support chat" but is now used only by `/api/community/tickets/[id]/messages`. Changing it would alter community ticket emails, which is out of scope.
• **`ProblemReportsClient.tsx:81,90`** format dates with `toLocaleString(undefined, …)`, which produced an **intermittent hydration warning** once rows existed. Pre-existing BL-797 code, surfaced by this round's proof rows, not touched.
• **CLAUDE.md's "tab title: just Clippers HQ"** conflicts with WCAG 2.4.2 across the whole app. Pre-existing, escalated by the accessibility lead, not overruled here.

## GATES, HONESTLY

`npm ci` **exit 0**; `npx prisma generate` **exit 0** before tsc; `npx tsc --noEmit` **exit 0**, `grep -c "error TS"` = **0**; `npm run build` written to a log with the exit code echoed by hand and **never piped through `tail`**: **BUILD_EXIT=0**, "Compiled successfully in 59s". **eslint v9.39.4 confirmed present first**, so the hooks gate did not silently no-op: `check:prisma-bypass` **0 violations**, `check:removed-fields` **OK across 724 files**, `lint:hooks` **11 problems, 0 errors, 11 warnings** at the ceiling, unchanged. **23 files changed, 1,151 insertions, 3,217 deletions.** The **6 money files plus `tracking.ts`, `campaign-era.ts`, `apify-hard-off.ts`, `apify.ts`, `clipper-submit-core.ts` and `admin/clips/page.tsx` are byte-identical by blob OID on BOTH refs.** **No Apify actor run**, the 11 BL-678 guards untouched, `APIFY_HARD_OFF` still a `const true`. **No schema change.** Worktree `C:/b804` removed. No dashes as bullets, no emojis, no hardcoded colours in the new UI.

**Rollback:** `git revert -m 1 <merge>` or `git reset --hard pre-BL-804`. **Nothing in the database needs undoing.**
