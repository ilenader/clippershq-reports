# BL-737 — the owner's mobile navigation is not missing anything. It renders all 28 items and one line of JavaScript stops him scrolling to them

**2026-08-08 · READ ONLY · Base:** `main @ dd5d03f9` · **Branch:** `checkpoint/BL-737`
**Nothing was fixed. No code, config or data changed. `git status --porcelain` is 0 lines and worktree HEAD equals `origin/main`.**
**No build, `tsc` or lint run was performed and none is claimed: this round produced one markdown file, which cannot change any of them.**

---

## THE ANSWER, BEFORE THE DETAIL

**The owner's complaint is real. His diagnosis is wrong, and building to it literally would ship a diff
that changes nothing.**

Desktop and mobile render the **same component with byte-identical props and the same 28 items**. There is
**no responsive filtering of nav items anywhere**: `grep -c` for every media-query and device predicate in
`sidebar.tsx` returns **0**. Nothing is missing on mobile. Nothing is role-gated away from him either.

**Flags, Submit Clip and Completed Campaigns are RENDERED, in the DOM, on his phone**, at positions 16, 17
and 18 of 28, inside a section headed **"More"**, below the fold.

**They are unreachable because the nav cannot be scrolled by touch, and the cause is not CSS.** The CSS is
correct at every level: `sidebar.tsx:570` is `<nav className="flex-1 overflow-y-auto px-3 py-4">`, a valid
scroll container that scrolls on desktop with a wheel.

The blocker is **`app-layout.tsx:137-141`**, a document-level `touchmove` listener registered
`{ passive: false }` that calls `preventDefault()` on **every** single-finger touchmove while the drawer is
open:

```js
const onTouchMove = (e: TouchEvent) => {
  if (e.touches.length > 1) return; // allow pinch-zoom (2+ fingers) — WCAG 1.4.4
  e.preventDefault(); // block single-finger background pan (the scroll cause)
};
document.addEventListener("touchmove", onTouchMove, { passive: false });
```

It was written in BL-321 to lock the **background** page. It is attached to `document`, so every touchmove
inside the drawer bubbles to it and is cancelled too. The file's own comment states the mechanism without
noticing the consequence (`app-layout.tsx:120-122`): *"the UNCONDITIONAL single-finger `touchmove`
preventDefault, which cancels the pan gesture at its source so nothing can scroll."* **"Nothing" includes
the drawer.**

**One guard on that one handler makes all 17 unreachable surfaces reachable**, and the attribute it needs
(`data-drawer-panel`) is **already on both drawer panels**. A second, independent height defect (PART 2.6)
would still clip roughly the last two rows and should ship in the same round.

---

# PART 1 — BOTH LISTS, ENUMERATED

## 1.1 The two render sites are the same component

| | Component call | Wrapper |
|---|---|---|
| Desktop | `app-layout.tsx:824` | `app-layout.tsx:817` `"hidden lg:block ..."` plus an inline `transform` at `:818-820` |
| Mobile, OWNER (v2) | `app-layout.tsx:845` | `app-layout.tsx:843` `"fixed inset-y-0 left-0 z-30 w-[280px] lg:hidden"` |
| Mobile, other roles (v1) | `app-layout.tsx:874` | `app-layout.tsx:856` `"fixed inset-0 z-50 lg:hidden"` |

All three pass **identical props**: `role`, `isTestUser`, `reviewerCapabilities`, `canActAsClipper`. The
OWNER gets the **v2 push drawer** because `app-layout.tsx:202-206` reads
`effectiveRole === "OWNER" ... ? "v2" : "v1"`.

**There is no device-aware code inside `sidebar.tsx` at all.** `grep -c` for
`useMediaQuery|innerWidth|matchMedia|isMobile|sm:hidden|md:hidden|lg:hidden|hidden lg:|hidden md:` across
`sidebar.tsx` returns **0**. The item list is built from `role` only.

## 1.2 The side-by-side table

`ownerNav` is `sidebar.tsx:197-256`, assigned unconditionally at `sidebar.tsx:377`, plus Community injected
by JSX. Render order:

| # | Item | Route | Source file:line | Desktop | Mobile | Owner reaches it today |
|---|---|---|---|---|---|---|
| 1 | Clips | `/admin/clips` | `sidebar.tsx:200` | yes | yes | **YES** |
| 2 | Analytics | `/admin/analytics` | `sidebar.tsx:201` | yes | yes | **YES** |
| 3 | Campaigns | `/admin/campaigns` | `sidebar.tsx:202` | yes | yes | **YES** |
| 4 | Team | `/admin/team` | `sidebar.tsx:203` | yes | yes | **YES** |
| 5 | Payouts | `/admin/payouts` | `sidebar.tsx:204` | yes | yes | **YES** |
| 6 | Accounts | `/admin/accounts` | `sidebar.tsx:205` | yes | yes | **YES** |
| 7 | Community | `/community` | injected, `sidebar.tsx:625` + `:697` | yes | yes | **YES** |
| 8 | Command Center | `/admin/command-center` | `sidebar.tsx:211` | yes | yes | **YES** |
| 9 | Growth | `/admin/growth` | `sidebar.tsx:217` | yes | yes | **YES** |
| 10 | Agency Earnings | `/admin/agency-earnings` | `sidebar.tsx:218` | yes | yes | **YES** |
| 11 | Marketplace | `/marketplace/browse` | `sidebar.tsx:116`, resolved `:149` | yes | yes | **YES** |
| | **"More" heading** | | `sidebar.tsx:223`, rendered `:580-583` | yes | yes | visible |
| 12 | Dashboard | `/admin` | `sidebar.tsx:225` | yes | yes | borderline |
| 13 | Referrals | `/admin/referrals` | `sidebar.tsx:226` | yes | yes | borderline |
| 14 | Calls | `/admin/calls` | `sidebar.tsx:227` | yes | yes | **NO** |
| 15 | Clients | `/admin/clients` | `sidebar.tsx:228` | yes | yes | **NO** |
| 16 | **Flags** | `/admin/flags` | `sidebar.tsx:229` | yes | **yes** | **NO** |
| 17 | **Submit Clip** | `/admin/submit-clip` | `sidebar.tsx:230` | yes | **yes** | **NO** |
| 18 | **Completed Campaigns** | `/admin/past-campaigns` | `sidebar.tsx:231` | yes | **yes** | **NO** |
| 19 | Change referrer | `/admin/referral-override` | `sidebar.tsx:232` | yes | yes | **NO** |
| 20 | Archive | `/admin/archive` | `sidebar.tsx:233` | yes | yes | **NO** |
| 21 | AI Knowledge | `/admin/knowledge` | `sidebar.tsx:234` | yes | yes | **NO** |
| 22 | Poster Applications | `/admin/poster-applications` | `sidebar.tsx:235` | yes | yes | **NO** |
| 23 | Disputes | `/admin/marketplace/disputes` | `sidebar.tsx:236` | yes | yes | **NO** |
| 24 | Strike Config | `/admin/marketplace/strike-config` | `sidebar.tsx:237` | yes | yes | **NO** |
| 25 | Gamification | `/admin/settings` | `sidebar.tsx:238` | yes | yes | **NO** |
| 26 | Recalculate Earnings | `/admin/force-recalc` | `sidebar.tsx:239` | yes | yes | **NO** |
| 27 | Reviewer Queue | `/admin/reviewer-queue` | `sidebar.tsx:241` | yes | yes | **NO** |
| 28 | Reviewer Audit (scope) | `/admin/audit-log` | `sidebar.tsx:249` | yes | yes | **NO** |

**PRESENT ON BOTH: 28 of 28. DESKTOP ONLY: 0. MOBILE ONLY: 0.**

**Footer, worth knowing:** the two footer buttons at `sidebar.tsx:786` and `:806` ("Join our Discord",
"Download App") are gated `role !== "OWNER" && role !== "CLIENT"`. **The OWNER sees neither**, so his
sidebar ends in an empty bordered strip of about 33px (`sidebar.tsx:785`). Deliberate, and identical on
both devices.

## 1.3 The cause, per item, in the categories asked for

Only one category applies, and it applies to items 12 through 28 uniformly.

| Candidate cause | Verdict |
|---|---|
| Filtered out by a responsive condition | **NO.** `grep -c` for every device predicate in `sidebar.tsx` = **0**. Same component, same props. |
| Behind a collapsed section | **NO.** `"More"` is a plain `<p>` heading at `sidebar.tsx:580-583`. There is no disclosure state in the file: the only `useState` calls are `showInstallModal` (`:321`), `totalCommunityUnread` (`:396`), `helpRequestsCount` (`:403`) and `badgeCounts` (`:431`). **Nothing collapses.** |
| Visually clipped by an overflow rule | **NO.** The rule is `overflow-y-auto` (`sidebar.tsx:570`), a scroll container, not `overflow-hidden`. There is no `max-h-*` and no `overscroll-*` anywhere in the chain. |
| Genuinely absent on mobile | **NO.** |
| **Rendered but unreachable because the container does not scroll** | **YES. This is the whole of it.** |

**Flags, Submit Clip and Completed Campaigns are all RENDERED BUT UNREACHABLE.** Not missing, not
role-gated, not collapsed, not clipped by an overflow rule.

## 1.4 His own list proves the items render

He reports seeing, in order: Clips, Analytics, Campaigns, Team, "Payout accounts", Community, Command
centre, Growth, Agency earnings, Marketplace dashboard, "Refer".

That is **rows 1 to 11 read top to bottom**, with "Payout accounts" being rows 5 and 6 run together, and
**"Refer" being Referrals, row 13, which lives inside the "More" section.** If "More" were collapsed or
filtered, he could not be seeing an item from inside it. His own report is the evidence that the section
renders.

**Arithmetic, offered as corroboration and stated plainly as a calculation rather than a measurement,
because no browser was run in this round.** A nav row is `px-3 py-2.5 text-[15px]` with an `h-[18px]` icon
(`sidebar.tsx:635`), about 42px, plus the `space-y-1` 4px gap, so roughly **46px of pitch**. Available
height is viewport 852 minus browser chrome about 90, minus the 64px logo header (`sidebar.tsx:548`), minus
the 33px footer strip, minus `py-4` 32, leaving about **630px, so 13 to 14 rows**. The cut lands on
Referrals. **The diagnosis in PART 2 does not depend on this arithmetic**; that rests on the handler
itself, which cancels the gesture regardless of how many rows happen to fit.

---

# PART 2 — WHY IT CANNOT SCROLL

## 2.1 The CSS is not the problem, and that matters because it is where everyone looks first

```
sidebar.tsx:546   <aside className="fixed left-0 top-0 z-40 flex h-full w-60 flex-col ...">
sidebar.tsx:570   <nav className="flex-1 overflow-y-auto px-3 py-4">
```

* **The `<nav>` can genuinely shrink.** The classic flexbox trap is that a `flex-1` child has `min-height: auto`, refuses to shrink below its content, and so its `overflow-y-auto` never engages, needing `min-h-0`. **That trap does not apply here.** Per CSS Box Sizing, a flex item's automatic minimum size is **zero** when its computed overflow in that axis is not `visible`, and this item is `overflow-y-auto`. **Adding `min-h-0` would change nothing.** This was checked specifically because it is the most common false lead.
* **No blocking rule exists anywhere in the chain.** The root is `flex h-[100dvh] ... overflow-x-hidden` (`app-layout.tsx:805`, X axis only); the v2 panel is `fixed inset-y-0 left-0 z-30 w-[280px]` (`:843`) with `overflow` unset. No `max-h-*`, no `overflow-hidden`, no `overscroll-*`.
* **`touch-action` does not save it either.** `globals.css:521-524` sets `body, main { touch-action: pan-y; }`, but `touch-action` declares which gestures are permissible and **cannot override a non-passive `touchmove` preventDefault**. `sidebar.tsx:570` sets no `touch-action` of its own.

**Proof the CSS works: the same lines scroll on desktop.** The owner reaches every item on his PC through
this exact `<nav>` with a wheel.

## 2.2 The actual blocker, file:line

**`src/components/layout/app-layout.tsx:128-148`**, the BL-321 body-scroll lock, specifically **137 to 141**:

```js
useEffect(() => {
  if (!mobileOpen) return;                                                   // :129  the ONLY gate
  body.style.overflow = "hidden";                                            // :134
  html.style.overflow = "hidden";                                            // :135
  const onTouchMove = (e: TouchEvent) => {                                   // :137
    if (e.touches.length > 1) return;                                        // :138  the ONLY guard
    e.preventDefault();                                                      // :139  everything else
  };
  document.addEventListener("touchmove", onTouchMove, { passive: false });   // :141
}, [mobileOpen]);                                                            // :148
```

Four properties combine into the bug:

1. **It is on `document`.** `touchmove` bubbles, so a drag starting on a nav link inside the drawer reaches it.
2. **There is no target test at all.** No `closest("[data-drawer-panel]")`, no scroll-container test, no bounds test. The only escape is `e.touches.length > 1`.
3. **It is `{ passive: false }`,** so the browser waits for the handler before starting any scroll; `preventDefault` cancels the pan before scrolling begins, and every subsequent move stays cancelable and is prevented too.
4. **It is live exactly while the drawer is open** (`:129`), which is exactly when the nav is on screen.

**The condition for the bug is therefore: drawer open, one finger, anywhere on the page.** A two-finger
drag is the only touch input that reaches the drawer at all, which is a plausible reason the owner
concluded there was no scroll rather than a stuck scroll.

## 2.3 This is unintended, and two rounds' own comments prove it

* **`app-layout.tsx:1055-1064` (BL-318) states the contract:** *"when the mobile drawer is open we swap its overflow-y-auto to overflow-hidden to freeze the background; **only the drawer's own content scrolls**."*
* **`app-layout.tsx:120-123` (BL-321) states the mechanism:** the background is locked by *"(a) overflow:hidden on `<main>` + body + html, **and** (b) the UNCONDITIONAL single-finger touchmove preventDefault."*

**Lever (a) is already complete on its own.** `app-layout.tsx:134-135` sets `body`/`html` to
`overflow: hidden` and `:1078` swaps `<main>` to `overflow-hidden`. **Lever (b) is redundant for its stated
purpose and is precisely what breaks BL-318's contract.** The word "UNCONDITIONAL" is load-bearing, and it
is the bug.

## 2.4 The swipe handler is exonerated, but leaves a real residual

The **second** document-level `touchmove` (`app-layout.tsx:741`, the drawer swipe) does not cause this.
`app-layout.tsx:541-545` decides direction and bails out of vertical drags **before** any `preventDefault`:

```js
if (!s.decided && (Math.abs(diffX) > 10 || Math.abs(diffY) > 10)) {
  if (Math.abs(diffY) > Math.abs(diffX)) { s.tracking = false; return; } // vertical scroll
  s.decided = true;
}
if (!s.decided) return;
e.preventDefault(); // :547  only ever reached for horizontal gestures
```

**The residual, which will still bite after the primary fix.** Its opt-out test at `app-layout.tsx:497` is
`closest("[data-no-swipe], .overflow-x-auto, .overflow-x-scroll")`. The nav uses `overflow-y-auto`, which
matches none of those, and **neither panel carries `data-no-swipe`** (`:840-841`, `:870`); `sidebar.tsx`
contains no `data-no-swipe` at all. Since `:500` is `if (x < zone || mobileOpen)`, swipe tracking engages
for **every** touch starting inside the open drawer. A clean vertical drag self-releases at `:543`, but any
**diagonal** thumb drag where `|diffX| >= |diffY|` is claimed as a drawer drag and drives the wrapper. On a
long list a sloppy scroll will drag or close the drawer instead of scrolling.

This also breaches the project's own rule in `CLAUDE.md`: *"New dropdown/overlay/interactive containers get
`data-no-swipe`."*

## 2.5 A prediction the owner can test in thirty seconds, before any code is written

Because `:138` lets multi-touch through, **a TWO-finger drag inside the open drawer should scroll it today,
while a one-finger drag does not.** If that holds on his phone the diagnosis is confirmed from his side
without a deploy. Honest caveat: some browsers treat a two-finger drag as zoom rather than pan, so a
negative result would not refute the diagnosis.

## 2.6 A SECOND, INDEPENDENT DEFECT: the drawer is taller than the visible screen

This one survives the scroll fix and must ship with it.

`sidebar.tsx:546` is `position: fixed` with `h-full`, so `height: 100%` resolves against its containing
block, and the two platforms differ:

* **Desktop:** the wrapper at `app-layout.tsx:817-821` carries an **inline `transform`** (`translateX(-${sidebarOffset}px)`, added by BL-153.3). A transform makes an element the containing block for fixed descendants. That wrapper is a flex child of the `h-[100dvh]` root at `:805`, so it is exactly `100dvh` and the aside is viewport-accurate.
* **Mobile v2:** the panel at `app-layout.tsx:843` has **no transform**, correctly noted in its own comment at `:797-804`. The aside's containing block is therefore the **initial containing block**, and on iOS Safari and Android Chrome the ICB for fixed elements tracks the **large** viewport, that is the toolbar-retracted height.

**Net effect with the URL bar visible: the aside is roughly 60 to 90px taller than the visible area**, so
its bottom edge and the final nav rows sit under the browser chrome permanently. **The nav's internal
scroll cannot rescue this, because the scroller's own bottom edge is off-screen.** The root already uses
`h-[100dvh]` at `:805` for exactly this reason; the aside does not benefit because it is `fixed` and uses
`h-full`.

**Confidence, stated honestly:** high on the containing-block mechanics, which are read directly off the
code. The exact ICB height is browser-dependent, so this wants **one on-device confirmation** before the
fix is sized. It would clip roughly the last two rows.

## 2.7 The shared drag-scroll hook is NOT the answer and must not be used here

BL-671 extracted `src/lib/use-drag-scroll.ts` for the landing carousel and the Completed campaigns row.
**It is the wrong mechanism, on four independent grounds:**

1. **It is horizontal.** It drives `scrollLeft` from `dx`. This nav needs vertical scrolling.
2. **It is mouse only.** BL-671's report states the handlers return early when `pointerType !== "mouse"`, deliberately, so touch keeps native momentum. The owner's problem is **touch**, so the hook would never execute on his device.
3. **It solves the opposite problem.** It **adds** a drag affordance where native scrolling already works. Here native scrolling is being actively **suppressed**.
4. **It would not remove the blocker.** The `preventDefault` at `:139` would still fire, and the hook does not call `stopPropagation`.

**Ordinary vertical overflow scrolling is already implemented and already correct. The right fix is to stop
cancelling it, not to build a replacement.**

---

# PART 3 — NOTHING HE NAMED IS ROLE-GATED, AND HIS PREMISE IS PARTLY MISTAKEN

**No item he named is hidden by a role or permission check.** `ownerNav` is assigned wholesale at
`sidebar.tsx:377` for `role === "OWNER"`, and all 28 entries are unconditional array members. Flags
(`:229`), Submit Clip (`:230`) and Completed Campaigns (`:231`) carry **no capability test, no flag and no
conditional of any kind.** The only conditional items in the OWNER path are Marketplace (`sidebar.tsx:335`,
where `role === "OWNER"` is itself a passing condition) and Community (`sidebar.tsx:624`,
`communityVisibleHere = isAdmin`, and `isAdmin` includes OWNER at `:322`). Both resolve visible, and he
confirms he sees both.

**Where his premise is mistaken, stated plainly:**

* **He believes mobile shows fewer items than desktop. It does not.** Both render the identical 28. The difference is how many fit and whether the list can be moved.
* **He believes the items are "missing". They are present in the DOM**, focusable, and in the tab order. A screen reader would read every one of them out. As PART 4 records, a keyboard user can already reach all 28 today.
* **His instruction, "make mobile show everything desktop shows", would produce no change if followed literally**, because mobile already renders everything desktop renders. It would ship a diff that changes nothing and leave him exactly as stuck.
* **Where he is right, and it is the important half:** he cannot reach Flags, Submit Clip or Completed Campaigns from his phone. That is real, it is a genuine operational limit, and PART 2 names the line responsible.

---

# PART 4 — WHAT ELSE IS UNREACHABLE ON A PHONE

## 4.1 Seventeen admin surfaces, all below the cut

Rows 12 to 28 of the PART 1.2 table are unreachable by touch today. Beyond the three he named that includes
**Disputes**, **Poster Applications**, **Strike Config**, **Reviewer Queue**, **Recalculate Earnings**,
**AI Knowledge**, **Archive**, **Change referrer**, **Calls**, **Clients** and **Reviewer Audit**.

**There is no second route to them on a phone.** Both alternatives fail:

* **The bottom tab bar carries five tabs only** (`BottomNav.tsx:76-82`): Clips, Analytics, Campaigns, Team, Payouts. All five are already visible in the drawer, so it adds nothing.
* **The admin dashboard links to five routes** (`admin/page.tsx`, counted with `grep -c`): `/admin/accounts`, `/admin/campaigns`, `/admin/clips`, `/admin/fraud-review`, `/admin/payouts`. **None of the seventeen.**

On a phone those seventeen are reachable **only by typing the URL**.

## 4.2 The bottom tab bar is EXONERATED

Worth recording because it is the obvious suspect and it is innocent. `BottomNav.tsx:380` is
`md:hidden fixed inset-x-0 bottom-0 z-40`, which does stack above the v2 panel's `z-30`. But
`BottomNav.tsx:354-364` (BL-310) sets `effectiveOffset = drawerOpen ? NAV_TRANSLATE_MAX : scrollOffset`,
`effectiveOpacity = drawerOpen ? 0 : navOpacity`, and `inert={navHidden || undefined}`. **While the drawer
is open the bar is translated fully off-screen, at opacity 0, and inert.** It does not cover the drawer and
needs no bottom padding to compensate. The real bottom-edge problem is PART 2.6, which is a different
mechanism entirely.

## 4.3 Accessibility defects that make the nav unreachable for other people

Reviewed by the accessibility lead against the shipped code, read-only. These are **separate from the touch
bug** and several are more severe.

| ID | Severity | File:line | Finding | Criterion |
|---|---|---|---|---|
| **A1** | CRITICAL | `app-layout.tsx:137-141` | The touch bug itself. About 17 of 28 destinations clipped with loss of function at a mobile viewport. | **1.4.10 Reflow (AA)** |
| **A2** | CRITICAL | `app-layout.tsx:842` | `aria-hidden={!mobileOpen}` sits on a panel that is **always mounted and displayed** below `lg`. When closed it is `aria-hidden="true"` while all ~30 `<Link>`s stay in the tab order. A keyboard or switch user tabs through 30 invisible links in silence. In-repo precedent for the fix: `BottomNav.tsx:361-364` already uses the native `inert` prop for exactly this. | **4.1.2 (A)** |
| **A3** | CRITICAL | `app-layout.tsx:996-998` | The hamburger is a `<button>` whose only child is `<Menu className="h-5 w-5" />`. lucide emits a bare `<svg>` with no `aria-hidden`, no `<title>`, no `role`, so the accessible name is **empty** and a screen reader announces only "button". **This is the sole entry point to the entire admin nav on a phone.** Same defect on the v1 close button at `:875-882`. | **4.1.2 (A)** |
| **A4** | MAJOR | `app-layout.tsx:996` | No `aria-expanded`, no `aria-controls`. A grep of the whole file returns zero `aria-expanded`, `aria-controls`, `aria-label`, `role` or `inert`. | **4.1.2 (A)** |
| **A5** | MAJOR | `app-layout.tsx:98-108` | No focus management at all: **no `.focus()` call anywhere in the file**. Opening does not move focus in; Tab walks straight out into the covered main; none of the four close paths (Escape `:104`, backdrop `:866`, shield `:1125`, route change `:96`) returns focus to the hamburger. The drawer installs a click-blocking shield at `:1121-1128`, so it behaves modally for pointer users and must for keyboard users too. Acknowledged as deferred in the comment at `:99-100`. | **2.4.3 (A)** |
| **A6** | MAJOR | `app-layout.tsx:1072-1080` | `<main>` gets `overflow-hidden` but no `inert` and no `aria-hidden`, so everything behind the dim shield stays focusable and readable. | **2.4.3 (A)** |
| **M6** | MINOR | `sidebar.tsx:570` | **No scroll affordance.** Overlay scrollbars on mobile, no fade, shadow or "more below" cue at the cut line. Nothing signals that content continues, which is a genuine contributor to the owner reporting items as *missing* rather than as *needing a scroll*. | 1.3.1 |
| **M5** | MINOR | `sidebar.tsx:785` | No `env(safe-area-inset-bottom)` on the drawer bottom, unlike `<main>` at `app-layout.tsx:1078-1079`. On a home-indicator iPhone the last ~34px falls in the gesture area, and for OWNER what lands there is the final nav row. | 2.5.8 |
| **M4** | MINOR | `app-layout.tsx:843` vs `sidebar.tsx:546` | Panel is `w-[280px]` and the wrapper translates by `V2_PANEL_W = 280` (`:430`), but the aside is `w-60` = 240px. 40px of the revealed strip is empty background. Cosmetic today; any future hit-testing that trusts the panel box is off by 40px. | n/a |

**Stated precisely so it is not over-claimed: the off-screen items ARE keyboard reachable.** They are in
the DOM and in the tab order, and because `sidebar.tsx:570` is a real scroll container, focusing an
off-screen link scrolls it into view automatically. **SC 2.1.1 Keyboard passes.** The failure is
specifically pointer and touch, which is why **1.4.10 Reflow** is the right citation for A1 rather than
2.1.1.

**Touch targets all pass SC 2.5.8 (24x24) and all miss the 44px platform guideline (2.5.5 AAA):** nav links
about 42px (`sidebar.tsx:635`), hamburger 32x32 (`app-layout.tsx:996`), v1 close 36x36 (`:878`). The
hamburger is worth raising to 44px given it is the only way into the admin nav on a phone.

**No duplicate-landmark issue:** both asides are always in the DOM, but `:817` (`hidden lg:block`) and
`:843` (`lg:hidden`) use `display:none`, so only one is ever in the accessibility tree. Separately the
`<nav>` at `sidebar.tsx:570` has no `aria-label`, a MINOR 1.3.1 finding once BottomNav's own `<nav>` is
present.

## 4.4 Six admin surfaces with no navigation entry at all, on EITHER device

Enumerating all 37 `page.tsx` files under `src/app/(app)/admin` against `sidebar.tsx`, then checking every
remaining route for an in-app link anywhere in `src/`:

| Route | In sidebar | Linked from anywhere in the app |
|---|---|---|
| `/admin/fraud-review` | no | **only** `admin/page.tsx` |
| `/admin/announcements` | no | **0 files** |
| `/admin/health` | no | **0 files** |
| `/admin/users` | no | **0 files** |
| `/admin/reset-data` | no | **0 files** |
| `/admin/referrals/commissions` | no | **0 files** |
| `/admin/help-requests` | no | **0 files**, deliberate: retired by BL-96 (`sidebar.tsx:250-255`), redirects to `/admin/clips` |

Excluded as legitimate detail pages reached from a parent: `/admin/archive/[campaignId]`,
`/admin/creator-scan/[accountId]`, `/admin/marketplace/disputes/[id]`, `/admin/users/[id]`.

**These are genuinely absent, not merely unreachable, and they are absent on desktop too.** They are
therefore **not** part of the owner's complaint and must not be conflated with it. `/admin/reset-data` is
almost certainly hidden on purpose. `/admin/health`, `/admin/users`, `/admin/announcements` and
`/admin/referrals/commissions` look like genuine oversights.

---

# PART 5 — THE FIX SPEC

## 5.1 Honest headline

**FIX 1 alone makes all seventeen unreachable surfaces reachable.** It is two lines. **FIX 2 is required in
the same round**, or the last two rows stay under the browser chrome and the fix will read as incomplete at
exactly the moment he scrolls to the end. Everything after that is real but separable.

## FIX 1 — exempt the drawer from the body-lock preventDefault (THE fix)

**File:line:** `src/components/layout/app-layout.tsx:137-141`.

```js
const onTouchMove = (e: TouchEvent) => {
  if (e.touches.length > 1) return;                      // unchanged, WCAG 1.4.4
  const t = e.target as HTMLElement | null;
  if (t?.closest?.("[data-drawer-panel]")) return;       // NEW: the drawer scrolls itself
  e.preventDefault();
};
```

**Why this selector:** `data-drawer-panel` is **already on both panels** and needs no new markup, at
`app-layout.tsx:841` (v2, beside `data-v2-panel` at `:840`) and `:870` (v1). **One guard fixes both drawer
variants**, so clippers, reviewers, admins and clients get it for free.

**Why `e.target` is the correct thing to test:** touch events retarget to the element the touch **started**
on and keep that target for the whole gesture. A drag beginning on a nav link and travelling outside the
drawer still reports the nav link, so the guard follows the finger and cannot be defeated by dragging past
the panel edge.

**What must be proven:**

1. At 375x667 and 390x844, drawer open, a **one-finger** vertical drag scrolls the nav, and **Flags, Submit Clip, Completed Campaigns** and the final item **Reviewer Audit (scope)** are reachable and tappable.
2. **The background still does not scroll** when the finger starts on the backdrop, the tap-to-close shield or the pushed main. This is the BL-321 property and the only thing this change could regress.
3. **BL-321 itself does not return:** after open and close, the page is not shifted up and content is not hidden under the mobile top bar. Test on mobile Chrome, where BL-320 originally broke.
4. Pinch-zoom still works (`:138` untouched).
5. The **v1** drawer on a non-OWNER account also scrolls, confirming the shared selector.
6. A **tap** still navigates and closes the drawer; a drag must not fire a navigation.
7. Desktop unchanged.

**Desktop risk: none, and structurally so rather than by judgement.** The effect is gated on `mobileOpen`
(`:129`), the toggle that sets it is `lg:hidden`, and `touchmove` does not fire from a mouse. **This fix
does not edit `sidebar.tsx` at all**, so the shared component cannot change. That is the reason to fix it
in `app-layout.tsx`.

**Rollback:** delete the two added lines. Additive and self-contained.

## FIX 2 — make the drawer exactly as tall as the visible screen

**File:line:** `sidebar.tsx:546`, the `h-full` on a `position: fixed` aside. See PART 2.6.

**Change:** give the aside a viewport-correct height on mobile, `h-[100dvh]` rather than `h-full`, or give
the v2 panel wrapper (`app-layout.tsx:843`) its own containing block so `h-full` resolves against a
`dvh`-sized box the way it already does on desktop. **Prefer whichever is confirmed on device**; the two
are not equivalent and the panel is `fixed` too, so it has the same exposure.

**What must be proven:** with the URL bar visible on iOS Safari and Android Chrome, the aside's bottom edge
and the final nav row are inside the visible area; and desktop is byte-identical at `lg` and above, since
this **does** edit the shared component.

**Rollback:** restore `h-full`.

## FIX 3 — stop diagonal drags being stolen by the swipe handler

**File:line:** add `data-no-swipe` to the `<nav>` at `sidebar.tsx:570`. See PART 2.4.

**Deliberately the `<nav>` and not the `<aside>`:** putting it on the aside would also disable swipe-to-close
from inside the drawer, which is a feature. Scoping it to the scroller keeps both behaviours. Also brings
the file into line with `CLAUDE.md`'s own rule.

**What must be proven:** a diagonal thumb drag scrolls rather than dragging the drawer; swipe-to-close from
the drawer's non-nav areas still works.

## FIX 4 — the accessibility set (A2, A3, A5), separable but cheap

**A3 first and on its own if nothing else is taken:** one `aria-label` on
`app-layout.tsx:996` and `aria-hidden="true"` on the icon. **The only entry point to the admin nav on a
phone currently announces as an unnamed "button".** A2 is a swap from `aria-hidden` to the native `inert`
prop, with `BottomNav.tsx:361-364` as the in-repo pattern. A5 is a genuine piece of work and can be its own
round.

## FIX 5 — a scroll affordance (M6), and the safe-area inset (M5)

Low cost, high value for this specific owner: a fade or shadow at the cut line would have told him there
was something to scroll to, which is the misunderstanding that produced this ticket.

## FIX 6 — a different round: the six surfaces with no nav entry (PART 4.4)

Absent on **both** devices, so not this bug. **Do not bundle it with the scroll fix**, because adding items
to a list that could not be scrolled is how this confusion started.

## 5.2 Ranking

| Rank | Fix | File:line | Effort | Effect |
|---|---|---|---|---|
| **1** | Exempt the drawer from the touch lock | `app-layout.tsx:137-141` | 2 lines | **Makes all 17 unreachable surfaces reachable. This is the fix.** |
| **2** | Viewport-correct drawer height | `sidebar.tsx:546` | 1 class | Recovers the last ~2 rows; without it FIX 1 looks incomplete at the end |
| **3** | `data-no-swipe` on the scroller | `sidebar.tsx:570` | 1 attribute | Stops diagonal drags stealing the scroll |
| **4** | Hamburger accessible name | `app-layout.tsx:996` | 2 attributes | The only phone entry to admin nav stops being unnamed |
| 5 | `inert` instead of `aria-hidden`; focus management | `app-layout.tsx:842`, `:98-108` | small, then a round | 30 silent tab stops; modal focus contract |
| 6 | Scroll affordance and safe-area inset | `sidebar.tsx:570`, `:785` | small | Signals there is more; clears the gesture bar |
| 7 | Nav entries for the six unlisted routes | design call | n/a | Unrelated to this bug, affects both devices |

**Is one small scroll change nearly all of it? Yes, with one honest qualification.** FIX 1 is two lines and
converts 17 unreachable admin surfaces into reachable ones, which is the entire substance of the owner's
complaint. But it is **not** sufficient on its own: FIX 2 addresses a genuinely independent defect that
would still hide the last rows, and the two should ship together and be tested together.

**What must NOT be done:** do not add, remove or reorder nav items, and do not build a mobile-specific nav
list. **Mobile already renders everything desktop renders**, so any change to `ownerNav` would fix a
problem that does not exist while leaving the real one in place.

---

# WHAT THIS ROUND DID NOT DO

**Nothing was changed.** `git status --porcelain` returns **0 lines**; worktree HEAD equals `origin/main` at
`dd5d03f9`. No code, no config, no data, no schema. **No build, `tsc` or lint run was performed and none is
claimed** — this round produced one markdown file, which cannot affect them. Nothing held by the live BL-736
round (the clips and campaign path) was touched: the files read here are `app-layout.tsx`, `sidebar.tsx`,
`BottomNav.tsx` and `admin/page.tsx`, and all reads were read-only.

**Not measured in a browser, and said plainly:** the row-height and cut-point arithmetic in PART 1.4 is
calculated from the Tailwind classes, not rendered. PART 2.6's exact clipped height is browser-dependent
and wants one on-device confirmation. **Neither qualification affects the PART 2 diagnosis**, which is read
directly off `app-layout.tsx:137-141`.
