# BL-797 — report a problem, one way, inside the widget that already exists

**IT IS RENDERED. Every screen below was photographed in a real Chromium at 320, 375, 414, 1280 and 1440, and I claim no screen I have not seen.** The blocker that stopped five rounds was not the dev bypass. `getSession()` reads the `dev-auth-role` cookie (`src/lib/get-session.ts:67-84`) and IS the helper every server page guard calls, so it always reached them. What was broken is `next dev` on Turbopack, which FATAL-crashes on stale junctions under `.next/dev/node_modules`. **`next dev --webpack` clears it.** Shots: `reports/BL-797-assets/`.

**2026-08-12 · DB `now()` = `2026-08-12 19:47:15.672661+00` · BUILD.** Base `main` @ `72f05cec`. Branch `checkpoint/BL-797` @ `18ef695f`, **verified pushed** (origin == local). Tags `pre-BL-797` / `post-BL-797` on origin. Worktree `C:/b797`, short path, `node_modules` never junctioned, removed at the end. Every read through `run-select.js`, every timestamp `::text`.

## THE SHAPE WAS ALREADY DECIDED, SO IT WAS NOT RE-DERIVED

BL-795 found the fact that settles it: a chat widget is already on every page for every signed-in user and is genuinely used. Re-measured today and **identical after this round**: 54 conversations, 13 `needsHumanSupport`, 108 messages, 50 distinct participants, last message `2026-08-05 22:23:08.154`. So this extends that widget. It is not a second inbox.

## PART 1 — THE CLIPPER SIDE

One entry pinned at the top of the widget list, for every role. **It must not read as a thread, so the difference is geometry, not colour**: a rounded square tile instead of the circular avatar every conversation uses, a chevron instead of a timestamp, no unread dot, no message preview, a 2px rule beneath. A tint measures 1.05:1 and is dimmer than the row's own hover state in greyscale; shape survives.

> **Report a problem** · One message, no reply. Use the chat if you need an answer.

Behind it: **one box, one button.** No categories, no priorities, no dropdowns, no uploads. The one-way promise is made **before** sending, not only after: *"This goes one way. It reaches the team, and no reply comes back here. For anything you need an answer to, use the chat."*

**The exact confirmation shipped**, replacing the form in place:

> ### Thanks for reporting this
> Your message is with the team, along with the page you were on.
> This form does not send replies. If you need an answer, use the chat instead.

No "we", no "soon", no "get back", no future tense, no ticket number, no queue position, no timer that dismisses it. A machine check on the rendered panel confirms none of `get back to you / we will / we'll / shortly / soon as` appears.

## PART 2 — CAPTURED, NOT TYPED

**Captured:** page path with the query string stripped before it leaves the browser; coarse OS family; coarse browser family; installed-app versus browser tab; viewport width; **the version the BROWSER is running alongside the version the SERVER is running**; role; `::text` timestamp; clips awaiting a decision; clips rejected in the last 30 days with the most recent date; and any per-campaign balance held below that campaign's own minimum. The version pair is new: BL-774 listed "no client version is recorded anywhere" as a thing it could not measure, which is exactly what made its stale-PWA hypothesis untestable. A real row from the render reads `App version 0.1.1, matching the server`; a seeded stale client reads the mismatch **in words**, because colour cannot carry it.

**Deliberately NOT captured, and the 21 columns are the proof:** `id, userId, body, pagePath, platform, browser, displayMode, viewportWidth, clientVersion, serverVersion, roleAtReport, pendingClipCount, recentRejectionCount, recentRejectionAt, blockedBalanceCents, blockedCampaignName, readAt, readById, resolvedAt, resolvedById, createdAt`. **No wallet address, no token, no password, no raw user agent, no query string, no email, no IP, no handle, no Discord id, no other clipper's data.** The raw UA is read for its OS and browser family and then discarded.

**Proven read-only on the two clippers who caused this feature to exist** (`scripts/bl797-capture-proof.ts`, no report created, nothing written):

| | clips awaiting a decision | rejected in 30d | most recent | balance under a minimum |
|---|---|---|---|---|
| **Clipper F (BL-774)** | 0 | **22** | 2026-08-03T17:17:11Z | none |
| **Clipper A (BL-762)** | 2 | 10 | 2026-08-11T13:22:26Z | **$16.32 on Zhus Edit (0.50 CPM)** |

BL-774 spent an entire investigation on four words and the answer was those 22 rejections. It would now arrive attached to the report.

## PART 3 — THE OWNER SIDE

`/admin/problem-reports`, OWNER-only through the same triple gate as `/admin/audit-log` (layout, then `notFound()` in the page, then `requireOwner()` in both routes). **Matched surface: `/admin/marketplace/disputes`** — its page shell, its tab row with count pills, its `rounded-xl border p-4` rows, its dashed empty state. Stat tiles adapted from `/admin/command-center`. No new visual language, no new colour.

**Grouping is by PAGE and TIME ONLY.** Consecutive reports about the same page within 6 hours are one group; further apart they are two. Nothing in `problem-report-grouping.ts` reads the words, because BL-775 measured **413 distinct free-text strings across 994 rejection reasons** and a classifier that decides two sentences mean the same thing is a way to hide the fifth report. Proven on real rows, the same page rendering as two groups nine hours apart:

```
/payouts   · 2 reports · Aug 12, 09:37 PM to 09:37 PM
/dashboard · 2 reports · Aug 12, 09:33 PM to 09:33 PM
/earnings  · 1 report  · Aug 12, 09:33 PM
/payouts   · 1 report  · Aug 12, 12:05 PM      <- same page, separate problem
```

**Unread count where he already looks:** in the `h1` ("5 unread") and on the sidebar badge, via a new `problemReports` slug in the existing `sidebarLastSeen` mechanism, so the count and the clear-on-entry come free and behave like every other admin badge. Photographed showing `4` and `1`. **Mark read proven by clicking it: 3 unread became 2 unread.** Reporter links to `/admin/users/dev-clipper-001`. Page ranking renders `/payouts 3 reports`, `/dashboard 2 reports`, `/earnings 1 report`.

## PART 4 — WHAT THIS IS NOT, PROVEN

The only two writes anywhere in the new code are `problemReport.create` (`api/problem-reports/route.ts:129`) and `problemReport.update` (`api/admin/problem-reports/[id]/route.ts:67`). No `Conversation`, no `Message`, no `needsHumanSupport`, no `Notification`, no email, no SSE push. Live: **notifications created in the 3 hours around the proof were 15, every one of them the owner's own CLIP_APPROVED / CLIP_REJECTED plus one growth cron, and ZERO to any of the three accounts that sent a report.** Chat counts unchanged (54 / 13 / 108 / 50). No clip, earning, payout, status or standing was touched; payout rows 167 before and after; **earnings invariant 0 violations.**

## PART 5 — THE LIMIT

**5 reports per hour per user, this endpoint only.** Chosen so somebody hitting three separate faults in one sitting is never turned away. Seven rapid posts returned **201 201 201 201 201 429 429**. In the UI the sixth renders a plain sentence, not an error, and the draft survives it:

> That is a few reports in a short time, so this one was not sent. Try again in about an hour. Nothing else on your account is affected, and you can still submit clips and request payouts as normal.

Earning, submitting and withdrawing run through different routes with their own limits and are untouched. **No report reaches another clipper:** eleven files reference the model and all eleven are this feature's; `GET /api/admin/problem-reports` as a CLIPPER returns **403**; the page returns `NEXT_HTTP_ERROR_FALLBACK;404` for a CLIPPER and renders for an OWNER. A clipper who reports is in exactly the state they were in one second earlier.

## PART 6 — ACCESSIBILITY, TWO PASSES

Design pass then code pass, both by the accessibility lead, both acted on. The load-bearing find: **the always-mounted chat panel was tab-reachable and in the accessibility tree while closed** — `opacity-0 scale-95 pointer-events-none` removes neither. An entry row that renders with no data dependency would have turned that latent bug into a guaranteed one on every page. The panel is now `inert` while closed, with focus restored to the launcher via `getClientRects()`, **not** `offsetParent`, which is null for any `position: fixed` element and would have made the restore dead code on desktop. Also: white on `#2596be` is 3.40:1, so both labelled buttons take `accent-hover` at 4.60:1; new additive token `--border-strong` because `--border-color` is 1.18:1 on a card and a text box drawn with it has no perceivable extent; `aria-disabled` with real handler guards rather than native `disabled`, which would blur the focused button mid-request; one shared polite region per surface with a 130ms clear-then-set so two identical refusals both speak; character count announced only on band crossings; **no `maxLength`**, because a silent paste truncation on a one-way form can never be discovered by the person who sent it.

## GATES, SCOPE, AND WHAT I DID NOT DO

`npx tsc --noEmit` **0 errors, exit 0** against a 0-error baseline. `npm run build` **exit 0**, echoed not piped. Hooks gate **0 errors, 11 warnings** at the ceiling, with **eslint v9.39.4 confirmed present**. The 6 money files plus `tracking.ts`, `campaign-era.ts`, `apify.ts` and `admin/clips/page.tsx` are **byte-identical by blob OID on both refs**. BL-776's evidence panel is still at `admin/clips/page.tsx:2050`; BL-788's reviewer surfaces are not in the diff. No Apify actor run. Schema additive and nullable via `generate`, never `migrate`; `problem_reports` carries **RLS on with 0 policies**, matching the other 90 public tables. Worktree removed. No dashes as bullets, no emojis, no hardcoded colours in the new UI.

**A REDEPLOY IS REQUIRED before this works in production.** The SQL is applied and the table exists, but the running server's generated Prisma client has no `problemReport` model, so `db.problemReport` is undefined there and both routes return their "Database unavailable" 500 until the next deploy. Nothing on any clipper path throws in the meantime, because the widget entry only calls the route when pressed.

**Rows I created and how to remove them.** Seven real rows, all from the four `dev-*` accounts, all already deleted: `cmsqhr9ga…`, `cmsqhle6l…`, `cmsqhlm8c…`, `cmsqhlqpx…`, `cmsqhr9pi…`, `cmsqhrmjh…`, `cmsqhsy33…`. `problem_reports` is back to **0 rows**. Re-run `node scripts/run-mutation-once.js scripts/migrations/BL-797-remove-proof-rows.sql` (`DELETE … WHERE body LIKE 'BL-797%'`) if any reappear. No user row was created; the four `dev-*` users have existed since March.

**Reported, not fixed.** `CLAUDE.md` says the tab title is just "Clippers HQ", which conflicts with WCAG 2.4.2; I did not overrule a rulebook line, so the page inherits the global title. The chat's own composer textarea is placeholder-labelled, its Send button has no accessible name, and its launcher unread badge announces a bare number: all pre-existing, all flagged, none touched, because the brief requires the existing chat to behave exactly as it does today. A hydration warning fires on `/admin/marketplace/disputes`, a page not in this diff; `/admin/problem-reports` produces **zero**. `next dev` re-evaluates server modules between spaced-out requests, which hands the in-memory limiter a fresh Map — the 429 proof is therefore seven rapid posts, and a single long-lived `next start` process does not have that property.
