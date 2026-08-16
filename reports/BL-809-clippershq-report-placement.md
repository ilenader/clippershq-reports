# BL-809 — the report entry is a sidebar row, the owner never sees it, and past campaigns are selectable again

**Merged to main and verified pushed. `origin/main` == local at `c94dc229`.** Branch `checkpoint/BL-809` @ `c6b0eae1`, **branched from `609417f4`, which is BL-808 merged** — so BL-808's trimmed form is the base and is untouched by this round. Tags `pre-BL-809` (`609417f4`) / `post-BL-809` (`c94dc229`) on origin. Isolated worktree `C:/b809`, short path, `node_modules` never junctioned, **removed at the end**. DB `now()` from `2026-08-16 13:13:05.820+00` to `14:45:41.763+00`, every timestamp cast `::text`. Handles redacted, no wallet address read or printed.

**A REDEPLOY ON RAILWAY IS REQUIRED BEFORE ANY OF THIS IS LIVE.**

**One thing happened mid-round that you should know about:** another session merged **BL-811** (the express payout promise, 12 hours to 24) to main while I was working. My branch was based on the commit before it. The merge into current main is a real `--no-ff` merge with **one conflict, in `BACKLOG.md` only**, resolved by keeping **both** entries; BL-811 touched none of my six files. **141 render assertions were re-run on the merged tree and all 141 pass**, so what is proven below is proven on main, not only on my branch.

---

## PART 1 — IT IS A SIDEBAR ROW NOW, AND NOTHING FLOATS

**The exact label shipped: `Report a problem`.** Unchanged from the pill, because it was already the right words.

It sits **third in the sidebar footer, under `Join our Discord` and `Download App`**, and it is the same object as they are, not something that resembles them. Measured in a real browser at every width, the report row's box is **byte-equal to the Discord row** on height, width, border radius, border colour and width, background, padding, gap, font size, font weight and text colour — a single equality check across nine computed properties, asserted at 320, 375, 414, 1280 and 1440.

| measured at every width | 320 | 375 | 414 | 1280 | 1440 |
|---|---|---|---|---|---|
| CSS viewport really is the asked width | yes | yes | yes | yes | yes |
| **any floating launcher anywhere in the DOM** | **0** | **0** | **0** | **0** | **0** |
| the row's box | `207 x 54` | `207 x 54` | `207 x 54` | `207 x 54` | `207 x 54` |
| label on ONE line | 20px | 20px | 20px | 20px | 20px |
| room left to the aside's right edge | 59px | 59px | 59px | 62px | 62px |
| identical box to `Join our Discord` | yes | yes | yes | yes | yes |
| same `h-7` accent icon tile (28x28) | yes | yes | yes | yes | yes |
| in the footer, NOT inside the scrolling nav | yes | yes | yes | yes | yes |

**The label fits with room, and that was measured before it was written, not after.** BL-793 recorded that `Join our Discord` clears the 240px aside by **one pixel**. `Report a problem` is a longer string, so this was the real risk in Part 1. It fits because the row carries **no trailing element**, which returns the ~26px the Discord row spends on its `ArrowUpRight`. That absence is also correct on its own terms: the arrow means *this leaves the site* and the Download row's `+2%` is an earnings fact. This opens a dialog in place, so borrowing either would say something untrue.

**Identical on a phone and on a desktop, because it is the same component.** `<Sidebar>` is what the desktop rail and the mobile drawer both render; one row therefore appears in both. That is also why the **dialog** could not move into the sidebar with it: `<Sidebar>` mounts **twice** at once (the `hidden lg:block` desktop copy and one drawer copy), so a dialog rendered from inside it would mount twice, with duplicate ids. The state was hoisted to `app-layout` instead, `ReportProblemWidget` became `open` / `onClose` / `restoreFocus`, and it now renders **only** the dialog.

### The drawer, which was the part to be careful with

**Opening the report CLOSES the drawer, and that is deliberate.** BL-321's background lock installs a document-level non-passive `touchmove` preventDefault while the drawer is open, and BL-739 narrowed its one carve-out to `[data-drawer-panel] [data-drawer-scroll]`. Leaving the drawer open under a full-screen report panel would mean **the report panel could not be scrolled by finger on a phone**, which is exactly where its send button already sits lowest.

**BL-739's guard still holds, measured rather than assumed** (375px, drawer open, real `TouchEvent`s dispatched and `defaultPrevented` read back):

```
drawer scroller overflows            447 / 325   -> the carve-out applies
touchmove INSIDE the drawer scroller  prevented = false  -> the drawer scrolls
touchmove on the page behind          prevented = true   -> the page does not move
body { overflow }                     hidden             -> the lock is intact
report row with the drawer open       207x54 @ top 530, fully on screen
```

**The row needs no scrolling to reach.** The footer is a sibling *below* `[data-drawer-scroll]`, so it is pinned to the bottom of the drawer rather than living inside the scrolling list. BL-737's 17 unreachable admin surfaces were inside that scroller; this is not. Adding a third row makes the nav shorter, which makes the scroller overflow *more* often, which engages BL-739's carve-out more often — the direction that helps.

---

## PART 2 — THE OWNER NEVER SEES IT

**Hidden by ROLE, and by withholding the callback rather than by a CSS class or a width.** `app-layout.tsx:292`:

```ts
const onReportProblem = effectiveRole === "OWNER" ? undefined : openReport;
```

and `sidebar.tsx:937` renders the row only `{onReportProblem && (...)}`. So for an owner the row is **not rendered at all** — not hidden, not `display:none`, not `aria-hidden`. It is not in the DOM, not in the accessibility tree and not a tab stop.

**Proven by grep.** Exactly one place in the repository renders that control, and it is guarded:

```
src/components/layout/sidebar.tsx:937    {onReportProblem && (
src/components/layout/sidebar.tsx:940      data-report-trigger
src/components/layout/sidebar.tsx:955      <span ...>Report a problem</span>
src/components/layout/app-layout.tsx:292  const onReportProblem = effectiveRole === "OWNER" ? undefined : openReport;
```

Every other match for the string is a comment or the dialog's own `<h2>` heading (`ReportProblemWidget.tsx:391`). There is no second entry point and no fixed-position control left.

**Proven by rendering**, on a real OWNER session at every width:

| | 320 | 375 | 414 | 1280 | 1440 |
|---|---|---|---|---|---|
| `[data-report-trigger]` in an owner's whole DOM | **0** | **0** | **0** | **0** | **0** |
| floating launcher in an owner's whole DOM | **0** | **0** | **0** | **0** | **0** |

**Why the owner: he is the person the reports arrive at.** They land in `/admin/problem-reports`, which is his. There is nobody above him to report to.

### The ADMIN and REVIEWER decision, stated and justified

**Both keep it.** A REVIEWER is still a clipper — BL-788 built the role on top of clipper surfaces and the reviewer sees the same clip pipeline a clipper does, so a reviewer hitting a fault has exactly the same thing to say. An ADMIN is the judgement call, and the answer is yes: an admin **does** have somebody to report to, namely the owner, and admins touch more of the product than anyone. The alternative — an admin who finds something broken and has no way to say so — has no upside.

**CLIENT keeps it too, and this is deliberately NOT the predicate its two neighbours use.** `Join our Discord` and `Download App` are gated `role !== "OWNER" && role !== "CLIENT"`. Copying that verbatim would have been tidier and would have **silently removed reporting from CLIENT**, which has it today (the widget mounts for every role). That was not asked for, so it was not done. The gate is `role !== "OWNER"`, one condition, one reason.

### The server did not change

**Plainly: this is a VISIBILITY change, not a permission change.** `/api/problem-reports` is untouched. It still accepts a report from anyone authenticated who can reach it, an owner included. Nothing was locked down, nothing was opened up.

---

## PART 3 — WHY PAST CAMPAIGNS COULD NOT BE SELECTED, AND WHAT CHANGED

### The cause, file:line

**`src/app/api/campaigns/route.ts:120-123`:**

```ts
} else if (!status && !includePast) {
  // OWNER/ADMIN with no explicit status filter: still hide PAST by default
  where.status = { not: "PAST" };
}
```

and **`src/app/(app)/admin/analytics/page.tsx:239`** asked for `?scope=manage` and nothing else — neither an explicit `status` nor `includePast=true`. So the OWNER fell into that branch on every load and PAST campaigns never reached the page.

**Only the OWNER was blocked.** The branch two lines above it (`:111`) handles `scope === "manage" && role === "ADMIN"` by setting `where.id` and never touching `where.status`, so an **admin could already pick past campaigns and the owner could not.** That is a code reading, not a measurement: the dev admin account has no assigned campaigns, so its list is empty either way and I could not observe it live. I am marking it as read rather than proved.

**Measured live before the change**, against the running server on the untouched tree:

```
OWNER ?scope=manage                     ->  5 campaigns  {ACTIVE:3, PAUSED:2}
OWNER ?scope=manage&includePast=true    -> 14 campaigns  {ACTIVE:3, PAUSED:2, PAST:9}
```

**The endpoint already supported the flag. The page simply never asked.** The fix is one query string.

### Every campaign status, before and after

`CampaignStatus` has five members (`prisma/schema.prisma:550`): `ACTIVE`, `PAUSED`, `COMPLETED`, `DRAFT`, `PAST`. `isArchived` is a **separate boolean**, not a status, which is the BL-732 distinction.

| status | rows in the database | selectable BEFORE | selectable AFTER |
|---|---|---|---|
| ACTIVE | 3 not archived, 13 archived | yes (the 3) | yes (the 3) |
| PAUSED | 2 not archived, 5 archived | yes (the 2) | yes (the 2) |
| **PAST** | **9 not archived** | **NO** | **YES** |
| COMPLETED | **0** | yes, in code | yes, in code |
| DRAFT | 0 not archived, 2 archived | yes, in code | yes, in code |
| *(archived, any status)* | **20** | no | **still no, on purpose** |

**One correction to the brief's premise, checked rather than assumed: COMPLETED was never blocked by code.** `{ not: "PAST" }` permits COMPLETED. It read as unselectable because **the database holds zero COMPLETED campaigns** — the platform marks finished campaigns `PAST`, not `COMPLETED`. So there was one real block, PAST, and it accounted for **9 of the owner's 14 non-archived campaigns**. He was seeing 5 of 14.

**Archived stays out, deliberately, and here is the number that decides it.** `?archived=true` is a separate OWNER-only mode that returns **only** archived rows, so including both would need a new parameter on a shared endpoint. More importantly, **13 of the 20 archived campaigns still carry status `ACTIVE`**, and the page's "Active campaigns" tile counts `status === "ACTIVE"` in that same list — folding them in would move that tile from **3 to 16**. A number silently changing meaning is exactly what this round must not do. If you want archived campaigns in analytics too, say so and it is its own small round.

### Nothing about any campaign's behaviour changed

The change is `analytics/page.tsx:239`, one query string on one **read**. No campaign's `status`, `isArchived`, budget, eligibility, tracking cadence, pause stamp or clip handling was written or read differently. `campaign-era.ts` and `tracking.ts` are **byte-identical by blob OID** on both refs. No schema change, no `prisma migrate`.

**The data path already covered past campaigns.** Neither `/api/admin/analytics/summary` nor `/api/admin/analytics/views-by-day` filters by campaign status at all, and the summary's `includeArchived` defaults to **true**. So a past campaign's clips were *already* inside the totals; the selector was the only thing stopping you isolating one. **A past campaign's data loads:** selecting one at 1440 renders 254 chart nodes with no error state.

### One displayed number DOES move, and you need to know before you look

With nothing selected, `displayedCampaigns` is the whole selector (`analytics/page.tsx:444-446`), and it is the **numerator of the Avg CPM tile**. Computed both ways from the same live endpoints:

```
owner spend in the numerator     $1,893.90   ->   $16,735.51
all-time approved views (denom)   36,575,069  ->   36,575,069   (unchanged)
Avg CPM tile                      $0.0518     ->   $0.4576
"Active campaigns" tile           3           ->   3           (unchanged)
```

**The old number was wrong, and this makes it right.** The denominator already counted the past campaigns' views, because the summary endpoint has no campaign-status filter. So the tile was dividing all-campaign views into five-campaign spend. The comment at `analytics/page.tsx:440-443` says the intent was already *"ALL owner-visible campaigns... `activeCampaigns` understated effective CPM by excluding paused/past spend"* — the intent was written, the past campaigns just never arrived.

**Residual, reported and not fixed: $416.57 of archived-campaign spend is still omitted while archived views still count.** That is 2.4% of the numerator, versus the 89% that was missing before. The tile deserves its own round; this one made it much less wrong, not perfect.

### Nothing owner-facing leaked to a clipper

BL-531 holds, checked by direct request against the merged tree:

```
                summary            /api/admin/problem-reports
OWNER      ->     200                        200
ADMIN      ->     200                        403
CLIPPER    ->     403                        403
REVIEWER   ->     403                        403
```

The whole `/admin` tree is behind `admin/layout.tsx`'s server gate as well. Nothing this round added is reachable by a clipper, and no clipper-facing route was touched.

---

## PART 4 — RENDERED

BL-793's method, unchanged because it is the one that works: real Chromium, **CSS viewport set through `browser.newContext({ viewport })`** rather than `resize_window`, `next dev --webpack` because Turbopack was the render blocker, and `window.innerWidth` read back and asserted every time. **141 assertions on the merged main tree, 0 failures**, plus a separate 20-assertion pass and a 14-assertion send pass.

| rendered | 320 | 375 | 414 | 1280 | 1440 |
|---|---|---|---|---|---|
| clipper sidebar with the report row beside Discord and the app link | yes | yes | yes | yes | yes |
| the drawer, opened by the hamburger, on a phone | yes | yes | yes | n/a | n/a |
| an OWNER account with no report entry | yes | yes | yes | yes | yes |
| **the floating launcher is gone** | **yes** | **yes** | **yes** | **yes** | **yes** |
| analytics selector listing past campaigns | 14 / 9 past | 14 / 9 | 14 / 9 | 14 / 9 | 14 / 9 |
| the selector's menu fits the viewport, own scroller | yes | yes | yes | yes | yes |
| no sideways scroll | yes | yes | yes | yes | yes |

**Every width was reached. None had to be skipped.**

**Two false failures, reported rather than only the clean re-run.**

1. *"1440 focus went back to the trigger itself" FAILED* on the first pass. It was **my harness**: the selector preferred `[data-drawer-panel] [data-report-trigger]`, and at 1440 the v1 drawer is still in the DOM behind `lg:hidden`, so it clicked the copy that is `display:none`. The focus ladder then **correctly** refused to hand focus to a control inside a closed drawer and fell through to `<main>`. Re-run against the copy that is actually laid out, focus returns to the trigger.
2. *The analytics selector at 375 and 414* died on `ChunkLoadError: Loading chunk app/layout failed` — `next dev` serving and compiling under load, not a defect. Re-run alone, both pass; and the whole suite then passed at all five widths on the merged tree.

**One thing I could NOT reproduce, and I am not claiming it.** I could not make the desktop sidebar actually slide off-screen in headless Chromium — setting `main.scrollTop` and dispatching a scroll event left `useScrollNavTranslate` at 0. So rather than assert a recovery I never saw, I wrote the slid state **inline, exactly as `app-layout.tsx:838-841` writes it at full travel**, and measured the rule against it:

```
inline translateX(-248px), opacity 0  ->  the report row sits at left -232 (off-screen)
focus the report row                  ->  transform: none, opacity: 1, row at left 16
blur it                               ->  back to translateX(-248px), opacity 0
```

That is the precise question the rule answers — does a stylesheet `!important` beat React's inline transform — and it is answered, in both directions, so it is not a one-way latch.

---

## PART 5 — THE EVIDENCE

| claim | evidence |
|---|---|
| the row sits in the sidebar styled like its neighbours, phone and desktop | `207 x 54` in the 240px aside at all five widths, nine computed box properties **equal to the Discord row**, same 28x28 accent icon tile, label on one line with 59 to 62px to spare |
| **no floating launcher remains** | **0** fixed-position controls carrying the label outside `<aside>` at all five widths, for both a clipper and an owner; one grep hit for the control in the whole repo and it is the sidebar row |
| an owner sees none of it, a clipper always does | **0** `[data-report-trigger]` in an owner's DOM at 320/375/414/1280/1440; present and measured for a clipper at all five. Gate is `effectiveRole === "OWNER"` at `app-layout.tsx:292` |
| the drawer still scrolls without the page moving | scroller `447/325`; `touchmove` inside it `prevented=false`, on the body `prevented=true`; `body{overflow:hidden}` intact; the row `207x54 @ top 530` on screen |
| analytics lists past and completed campaigns and the data loads | 14 options with 9 marked `(past)` at all five widths; selecting a past campaign renders 254 chart nodes, no error state |
| no campaign behaviour changed | one query string on one read; `campaign-era.ts` and `tracking.ts` byte-identical by blob OID on both refs; no schema change, no `prisma migrate` |
| nothing owner-facing leaked to a clipper | `/api/admin/analytics/summary` **200 OWNER / 200 ADMIN / 403 CLIPPER / 403 REVIEWER**; `/api/admin/problem-reports` **200 OWNER / 403 everyone else** |
| **a report still sends, with context and the reply-free confirmation** | 2 real rows sent **from the new sidebar row** at 320 and 1440. One reads `pagePath=/earnings, viewportWidth=320, displayMode=browser-tab, roleAtReport=CLIPPER, clientVersion=0.1.1, serverVersion=0.1.1, pendingClipCount=0, recentRejectionCount=0, blockedBalanceCents=null`. Confirmation: `Thanks for reporting this`, `This form does not send replies`, the Discord link, focus on the heading, and **no match** for `we will / we'll / get back / shortly / as soon as / ticket` |
| nothing sensitive is captured | the table has **21 columns** and none is a wallet, a token, a password, an email or another clipper's data |
| the chat is still gone and the archive still owner-only | `/api/chat/{conversations,unread,sse,campaign-chats,messageable-users}` all **404** against live controls (`/api/campaigns` 200, `/api/problem-reports` 405); **0 tracked files** under `src/app/api/chat`; `/admin/chat-archive` renders its heading for **OWNER only**, not for ADMIN, CLIPPER or REVIEWER |
| BL-776 and BL-788 still work | `admin/clips/page.tsx` byte-identical by blob OID (`d1ebebe5`) on both refs, `ReviewEvidencePanelMount` still present; no reviewer file touched |
| no clip's earnings or status changed | **0 clips written by this round.** 9 PENDING clips arrived from **3 real clippers** between `13:14:35` and `14:43:06`, and 251 clips were updated by the `14:00` tracking batch. Neither is mine: this round made no clip request of any kind, and the only 2 `dev-*` clips in the database are May and June seed rows last touched `2026-06-24` |
| no payout touched | **172** rows, last write `2026-08-16 00:01:46.711` — **thirteen hours before** this round's first read at `13:13:05`. Payouts created, modified, approved or cancelled: **0** |
| the earnings invariant | **0 violations**, before and after |
| the 6 money files plus `tracking.ts` and `campaign-era.ts` | all 7 **IDENTICAL by blob OID on the branch, on the merged main, and on the base**: `clip-earnings-writer ac5be7de`, `earnings-calc 797e2098`, `balance e887f80a`, `tracking 83ce4bab`, `invariant-middleware 61cef393`, `money-decimal ef5cdae7`, `campaign-era 106e16ad`. Also identical: `apify-hard-off 29258a5d` |
| BL-678 guards | **11** references intact, `APIFY_HARD_OFF` untouched, **no Apify actor run** |

**The two rows I created and how they were removed.** Two `problem_reports` rows on the synthetic `dev-clipper-001` account, sent so "a report still works" could be proved against real rows. **Both deleted** by `scripts/migrations/BL-809-remove-proof-rows.sql` (`rowCount=2`, idempotent, scoped three ways: the account, the body prefix and the day). `problem_reports` is back to **7**, and **every one of them is a real user's, untouched**.

---

## GATES, HONESTLY

**Clean baseline recorded on the untouched worktree BEFORE any edit**, with `npm ci` exit 0 and `npx prisma generate` exit 0 first (and again after the merge, because BL-811 changed `schema.prisma`).

| gate | branch | merged main |
|---|---|---|
| `npx tsc --noEmit` | **exit 0, `grep -c "error TS"` = 0** | **exit 0, 0 errors** |
| `npm run build` | **`REAL_BUILD_EXIT=0`**, compiled in 31.2s | **`REAL_BUILD_EXIT_MERGED=0`**, compiled in 21.7s |
| `check:prisma-bypass` | 0 violations | 0 violations |
| `check:removed-fields` | OK across 724 files | OK across 724 files |
| **hooks gate** | **0 errors, 11 warnings** at the ceiling | **0 errors, 11 warnings** |

**Exit codes echoed by hand from a log, never piped through `tail`. eslint v9.39.4 confirmed present at `node_modules/.bin/eslint` first, so the hooks gate did not silently no-op.** Baseline was already at its 11-warning ceiling, so zero new warnings was a hard requirement and was met: the two effects added are `[open]` and `[open, restoreFocus]`, both complete, and every new callback is `useCallback` over refs and stable setters.

**BACKLOG counted with `grep -c`, never piped to `head`: 152 sections before, 154 after** (BL-811 arrived with the merge and mine is one). 21,862 lines to 21,892. `BL-809` appears once, `BL-811` once, **0 conflict markers** after the union resolution. **6 shipping files changed**, plus BACKLOG and seven throwaway scripts.

---

## ACCESSIBILITY — reviewed before any code, 12 blocking items, 8 implemented and 4 declined with reasons

The lead returned **NO-SHIP as planned** and it was right to. What changed as a result:

1. **`aria-haspopup="dialog"` and nothing else on the trigger.** **No `aria-expanded`**: that is the *disclosure* contract, and a modal does the opposite — `aria-modal="true"` hides the trigger from assistive technology, so "expanded" would only ever be true when nobody can read it, and on focus return the user would hear "collapsed" and be invited to press it again. **No `aria-controls`**: the panel is `inert` while closed, so the IDREF resolves to a subtree that is not in the accessibility tree, and threading the dialog's `useId()` through two call sites is a dangling-IDREF failure waiting to be introduced. **No `id`** in a component that mounts twice.
2. **A three-rung focus-return ladder, each rung proved by reading `document.activeElement` back** rather than by predicting focusability: the trigger that was pressed, unless it sits in a `[data-drawer-panel]` that has since closed (still focusable, but translated off-screen); then the hamburger; then **`<main tabIndex={-1}>`. Never `<body>`.** Measured: at 1440 it returns to the trigger; at 375, where the drawer has closed, it returns to the hamburger at `32x32 @ 12,12`, fully on screen.
3. **The hamburger had no accessible name at all** — an icon-only `<button>` whose only child was a lucide `<Menu>`, which lucide does not mark `aria-hidden` itself. It is now `aria-label="Menu"` with `aria-hidden` on the icon. This round put it on the critical path, so it had to be named.
4. **`[data-desktop-sidebar]:focus-within` in `globals.css`** cancels the scroll-hide. BL-804 made a point of the launcher never hiding on scroll; the desktop sidebar wrapper does exactly that with `transform` and `opacity` and nothing else, so every control in it stays focusable while invisible — **WCAG 2.4.7, not 2.4.11**, since nothing covers it. Proven in both directions above. It fixes the same pre-existing problem for `Join our Discord`, `Download App` and every nav link.
5. **`(past)` is in the VISIBLE label**, not `sr-only` and not a colour. Colour or dimming alone would be 1.4.1; an `sr-only` suffix would leave low-vision and cognitive users without it; an `aria-hidden` visual pill would put visible text outside the accessible name (2.5.3) and break voice control. Parentheses, never a dash. Only the past ones are marked.
6. **The dropdown menu had no height cap and no scroller.** 15 rows at 36px is ~560px, taller than a 320x568 phone, and `.focus()` on the roving row would have scrolled `<main>` and dragged the absolutely-positioned menu with it. Now `max-h-[min(60vh,320px)] overflow-y-auto overscroll-contain`; inert for every short-list caller.
7. **`<main>`'s bottom clearance returned to its pre-BL-804 value**, read out of `git show pre-BL-804:` rather than recomputed by eye, because under-correcting puts the last row of a page under the phone tab bar. The `scroll-padding-bottom` is **kept** and narrowed to `max-md`, where that bar actually is.
8. **`forced-colors:` outline spelled out on the new row.** A Tailwind `ring` is a `box-shadow` and Windows High Contrast erases it; today only an unlayered global rule saves these rows, which is a cascade argument rather than a guarantee.

**DECLINED, with reasons, all pre-existing:**

• **`inert` on the closed drawer, and moving focus into the drawer on open.** These are the drawer's roughly 22 stranded tab stops. They affect every nav row equally, they long predate this round, and adding `inert` would convert the `/campaigns/[id]` gap below from *reachable but off-screen* into a hard Level A failure. They belong to a drawer round, with focus restoration, not to this one.
• **The light-theme selected-option contrast** in the dropdown (`#2596be` on `bg-accent/5` measures 3.22:1). Pre-existing, in a shared component with many callers, and CLAUDE.md specifies dark theme only. Multiplied by this change, so worth its own fix.
• **The empty footer strip an owner now sees.** Engages no criterion — no role, no name, nothing announced. Purely visual, and pre-existing.
• Contrast and target size on the new row needed no change: the label measures **18.40:1** dark and **19.90:1** light, the row is **54px** tall against 2.5.8's 24px and 2.5.5's 44px, and the accent focus ring reads **5.64:1** dark / **3.09:1** light against the 3.0 bar.

---

## THE ONE REAL LOSS, AND IT IS YOUR CALL

**On `/campaigns/[id]` at phone width there is now no visible way to open the report.** That route suppresses the whole top bar (`app-layout.tsx:1002`) and `BottomNav` suppresses itself on the same regex, so there is **no hamburger**, and the drawer opens there by **left-edge swipe only**. The floating pill was `position: fixed` and route-independent, so it covered that route; the sidebar row cannot.

I did not fix it, and I want to be exact about why. The accessibility lead's position is that a Level A regression you authored cannot be filed as a known residual, and it recommended keeping a fixed launcher on that one route. **Your instruction was to remove the floating entry entirely so nothing hovers over the page**, and a launcher that reappears on campaign detail pages is that instruction half-followed. So it is reported instead, with the two-line fix available the moment you want it.

Two things soften it: the drawer is still openable by swipe, which is the ordinary phone gesture there, and the drawer's rows are still in the tab order (that is the pre-existing defect above, working in your favour here). Neither makes it good.

---

## WHAT YOU DO NOW

1. **REDEPLOY ON RAILWAY.** Main carries all of this; production does not. Nothing above is live until the redeploy — and production is still older than BL-804, so the chat is still live there.
2. **Look at Avg CPM on `/admin/analytics` after the redeploy.** It goes from **$0.05 to $0.46**. Nothing broke; the old figure was dividing all-campaign views into five-campaign spend. Tell me if you want the archived campaigns' $416.57 folded in as well and the tile made exactly right.
3. **Decide on `/campaigns/[id]` on a phone.** Either accept that reporting there needs a swipe to open the menu, or say the word and the fixed launcher comes back on that one route.
4. **Decide whether archived campaigns belong in the analytics selector.** Twenty campaigns, and it moves the "Active campaigns" tile from 3 to 16 unless that tile is fixed in the same round.

**Rollback:** `git revert -m 1 c94dc229` or `git reset --hard pre-BL-809`. **Nothing in the database needs undoing.**
