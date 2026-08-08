# BL-739 — the drawer scrolls, the background still does not, and the carve-out is deliberately narrower than the one BL-320 removed

**2026-08-08 · Base:** `main @ dd5d03f9` · **Branch:** `checkpoint/BL-739` `cde68af6` · **Tags:** `pre-BL-739` = `dd5d03f9`, `post-BL-739` = `cde68af6`
**No money, earnings, payout, clip or campaign state was touched. No API, route, query or schema change. No `prisma migrate`. Nothing was read from or written to the database this round.**

---

# PART 0 — WHAT THE GUARD PROTECTS, AND THE THING THAT ALMOST WENT WRONG

## 0.1 BL-737's fix spec was already shipped once, and deliberately torn out

**This is the finding that decided the round, and it was made before a line of code was written.**

BL-737 specified exempting `[data-drawer-panel]` from the touchmove lock, noting the attribute "already
exists on both panels". It exists **because BL-319 put it there for exactly this purpose, and BL-320
removed the carve-out that used it.**

`BACKLOG.md:2001`, BL-320's own entry:

> **Why the prior two failed:** BL-318 (CSS `overflow:hidden` on `<main>`) doesn't stop a touch-pan on a fixed overlay. **BL-319 added a `touchmove` preventDefault but carved out `[data-drawer-panel]` — that carve-out (or its target check) let the gesture through on mobile Chrome.** Both left a gap.

And BL-319's commit message, `89d080e2`:

> a document `touchmove` listener `{passive:false}` that `preventDefault()`s every touch **except inside `[data-drawer-panel]`** ... **Tagged both drawer panels with `data-drawer-panel`.**

**Shipping BL-737's spec verbatim would have handed the owner back the background-scroll bug he chased
across four consecutive rounds (BL-318, BL-319, BL-320, BL-321).** That is precisely the trade this round
was told not to make. **The guard was not deleted, and the panel-wide carve-out was not reinstated.**

## 0.2 What it is actually protecting, plainly

**The page scrolling behind the open drawer, on mobile Chrome and iOS.** Not rubber-band, not
pull-to-refresh, not the PWA shell. The specific reported defect was that dragging on the open drawer
scrolled the page underneath it.

`overflow:hidden` alone could never stop it, and BL-319 established why (`BACKLOG.md:2015`):

> on **mobile Chrome a touch-drag on the FIXED v1 drawer overlay scrolls the DOCUMENT / root scrolling element**, not `<main>`, and a single element's `overflow:hidden` cannot prevent that document-level touch-scroll. `position:fixed` overlays don't create a scroll boundary.

So cancelling the gesture at its source was the only thing that worked. That is why it is unconditional,
and it is why it must not simply be removed.

## 0.3 Why BL-319 leaked, named rather than guessed

BL-320's note hedges: *"that carve-out **(or its target check)** let the gesture through"*. Nobody had
isolated it, and BL-321's accessibility note went the other way, arguing the carve-out was
*"background-leak-neutral (a background touch never targets inside the panel)"*. Both cannot be right.

**They are both partly right, and the mechanism reconciles them.** `[data-drawer-panel]` is the **whole
panel**, which contains three things: the logo header (`sidebar.tsx:548`), the nav, and the footer strip
(`sidebar.tsx:755`). The logo and the footer have **nothing to scroll**. A pan starting on either was
exempted by the carve-out, found no local scroll container, and **chained to the document**. BL-321's
claim is true as far as it goes (a touch on the *background* never targets inside the panel) and
insufficient, because the leak did not come from background touches. It came from panel touches with
nowhere to go.

## 0.4 The carve-out shipped here closes that on three independent axes

| | BL-319 (removed by BL-320) | BL-739 (this round) |
|---|---|---|
| Scope | the **whole panel**, `[data-drawer-panel]` | **only the scroller**, `[data-drawer-panel] [data-drawer-scroll]` |
| Condition | always | **only while that scroller actually overflows** |
| Chaining at the ends | nothing | **`overscroll-contain` on the scroller** |

Axis 2 is the one worth dwelling on. **BL-320's stated premise was "the menu is short and never needs to
scroll".** That was true for most roles and false for exactly one: the OWNER, at 28 items. The
`scrollHeight > clientHeight` gate means **every user whose menu fits sees behaviour byte-identical to
today**, so BL-320's premise is honoured for precisely the population it was true for, and overridden only
where it was false.

Axis 3 uses the codebase's own documented mechanism. `globals.css:178`, from BL-150:

> Scoped to html + body so individual scroll containers ... can still opt-in to their own overscroll behavior if needed via **`overscroll-behavior: contain` on the inner element**.

There was no `overscroll-*` anywhere in this chain before today.

---

# PART 1 — THE FIX

## 1.1 The full diff

```diff
--- a/src/components/layout/app-layout.tsx
+++ b/src/components/layout/app-layout.tsx
@@ -136,6 +136,26 @@
     const onTouchMove = (e: TouchEvent) => {
       if (e.touches.length > 1) return; // allow pinch-zoom (2+ fingers) — WCAG 1.4.4
+      // BL-739 — the ONE carve-out, and it is deliberately NARROWER than the one
+      // BL-319 shipped and BL-320 removed. BL-319 exempted the whole
+      // [data-drawer-panel]; BACKLOG.md:2001 records that it "let the gesture
+      // through on mobile Chrome" and BL-320 tore it out. The mechanism that
+      // explains that report: the panel also contains the logo header and the
+      // footer, which have NOTHING to scroll, so a pan starting on either was
+      // exempted and then chained to the document. This version cannot do that:
+      //   1. only the drawer's own SCROLLER is exempt, never the panel chrome;
+      //   2. only while that scroller ACTUALLY overflows, so every menu that
+      //      fits stays byte-identical to today (BL-320's "the menu is short"
+      //      premise is honoured for exactly the users it was true for);
+      //   3. the scroller carries `overscroll-contain` (sidebar.tsx), which is
+      //      the mechanism globals.css:178 already documents for inner scrollers,
+      //      so reaching its end cannot chain to the document either.
+      // Everything outside that one element is prevented exactly as before, so
+      // BL-321's background lock is untouched.
+      const scroller = (e.target as HTMLElement | null)?.closest?.(
+        "[data-drawer-panel] [data-drawer-scroll]",
+      ) as HTMLElement | null;
+      if (scroller && scroller.scrollHeight > scroller.clientHeight) return;
       e.preventDefault(); // block single-finger background pan (the scroll cause)
     };
     document.addEventListener("touchmove", onTouchMove, { passive: false });
```

```diff
--- a/src/components/layout/sidebar.tsx
+++ b/src/components/layout/sidebar.tsx
@@ -567,7 +581,15 @@
       {/* Navigation */}
-      <nav className="flex-1 overflow-y-auto px-3 py-4">
+      {/* BL-739 — this is the element the drawer's touch carve-out targets, and
+          the ONLY element it targets. `data-drawer-scroll` names it so
+          app-layout.tsx can exempt it precisely instead of exempting the whole
+          panel the way BL-319 did. `overscroll-contain` stops a pan that reaches
+          either end of this list from chaining out to the document, which is the
+          leak BL-320 reported; globals.css:178 already documents this as the way
+          an inner scroller opts into its own overscroll behaviour under BL-150's
+          `overscroll-behavior: none` on html and body. */}
+      <nav data-drawer-scroll className="flex-1 overflow-y-auto overscroll-contain px-3 py-4">
```

(The `<aside>` height change and the footer safe-area padding are PART 2.)

**2 source files, 52 insertions, 3 deletions, of which 39 insertions are explanatory comments.** The
executable change is **4 lines in `app-layout.tsx`** and **3 class or attribute edits in `sidebar.tsx`**.

## 1.2 Exactly which touches are permitted and which are still prevented

Measured, not asserted. Real Chromium, the handler extracted from the shipped source:

| Touch | Verdict | |
|---|---|---|
| One finger inside the drawer scroller | **PERMITTED** | the fix |
| One finger on the scroller element itself | **PERMITTED** | the fix |
| One finger on the drawer **logo header** | **STILL PREVENTED** | narrower than BL-319 |
| One finger on the drawer **footer** | **STILL PREVENTED** | narrower than BL-319 |
| One finger on the **page behind** | **STILL PREVENTED** | BL-321's protection, held |
| One finger on the **pushed main wrapper** | **STILL PREVENTED** | BL-321's protection, held |
| One finger in a menu that **does not overflow** | **STILL PREVENTED** | BL-320's premise, honoured |
| **Two fingers anywhere** | **PERMITTED** | pinch-zoom, WCAG 1.4.4, line untouched |

**The original protection holds outside the drawer's scroller, by construction:** the only new early
return requires `closest("[data-drawer-panel] [data-drawer-scroll]")` to match **and** that element to be
overflowing. Every other target reaches the identical `e.preventDefault()` that was there before. The
pinch-zoom line at the top is not modified.

---

# PART 2 — THE HEIGHT DEFECT

**What it was:** `sidebar.tsx:546` was `h-full` on a `position: fixed` aside, so `height:100%` resolved
against its containing block, and the two platforms resolved differently.

* **Desktop:** the wrapper at `app-layout.tsx:817` carries an inline `transform`, which makes it the containing block for fixed descendants. It is a flex child of the `h-[100dvh]` root at `:805`, so it is exactly `100dvh`. **`h-full` already meant `100dvh` there.**
* **Mobile v2:** the panel at `app-layout.tsx:843` has **no** transform, deliberately (its own comment at `:797-804` explains why). So the containing block is the **initial containing block**, which on iOS Safari and Chrome Android tracks the **large, toolbar-retracted** viewport. The drawer was therefore **taller than the visible screen**, and its last rows sat under the browser chrome permanently, somewhere the nav's own scrolling could never reach.

**What changed:** `h-full` became **`h-[100dvh]`**, the dynamic viewport, matching what the root at
`app-layout.tsx:805` already uses for this same reason.

**Plus a second, related change taken on the accessibility lead's advice:** the footer strip at
`sidebar.tsx:755` gained `pb-[max(1rem,env(safe-area-inset-bottom))]`. In **PWA standalone there is no
browser chrome at all**, so `100dvh` is the whole screen and that strip lands under the home indicator.
Padding it pushes the `flex-1` nav up by the inset. `max()` preserves the existing 16px on every device
reporting no inset, so nothing moves on Android, on desktop, or in a browser tab.

**Honest limit, stated plainly:** headless Chromium has no retracting toolbar, so the harness **cannot
reproduce the large-versus-small viewport divergence itself**. What it does prove is that the class is
applied, that the aside equals the visible viewport at all three widths, and, decisively for the shared
component, that **`h-[100dvh]` and `h-full` render the identical height inside the desktop transform
wrapper**. The mobile mechanism is read off the CSS containing-block rules and the code, and wants one
on-device confirmation.

---

# PART 3 — ALL 28 ITEMS REACHABLE

## 3.1 How this was proven

`scripts/test-bl-739-drawer-scroll.mjs`, **real Chromium**, against the app's **own compiled Tailwind**
(236,084 bytes read from `.next/static/chunks`). **The harness does not retype the fix.** It extracts the
shipped `onTouchMove` body and the shipped `<aside>` and `<nav>` classNames out of source at run time, so
it cannot drift from what ships. Scrolling is driven by **real CDP touch dispatch**
(`Input.dispatchTouchEvent`: touchStart, twelve touchMoves, touchEnd), which honours `preventDefault`
exactly as a phone does. Synthetic `TouchEvent` dispatch is used **only** for the decision table in PART
1.2, where `defaultPrevented` is precisely the question being asked.

**53 passed, 0 failed, exit 0.**

## 3.2 Old handler versus new, per width

```
320px  OLD handler: scrollTop 0 -> 0     NEW handler: scrollTop 0 -> 585
375px  OLD handler: scrollTop 0 -> 0     NEW handler: scrollTop 0 -> 585
414px  OLD handler: scrollTop 0 -> 0     NEW handler: scrollTop 0 -> 585
```

The OLD column **is the bug**, reproduced rather than assumed.

## 3.3 How far the list scrolls, per width

```
320px  aside 667px == viewport 667px   nav: 1375px of content in 570px   scrolled 805 of 805
375px  aside 667px == viewport 667px   nav: 1375px of content in 570px   scrolled 805 of 805
414px  aside 667px == viewport 667px   nav: 1375px of content in 570px   scrolled 805 of 805
```

**The list reaches its exact end by touch alone at every width**, 805 of 805 scrollable pixels.

## 3.4 Every item, reached

All 28 were confirmed **fully inside the scroller's visible box** at some point during the touch walk, at
each of 320, 375 and 414px:

| # | Item | 320 | 375 | 414 |
|---|---|---|---|---|
| 1 to 6 | Clips, Analytics, Campaigns, Team, Payouts, Accounts | yes | yes | yes |
| 7 | Community | yes | yes | yes |
| 8 to 11 | Command Center, Growth, Agency Earnings, Marketplace | yes | yes | yes |
| 12, 13 | Dashboard, Referrals | yes | yes | yes |
| 14, 15 | Calls, Clients | yes | yes | yes |
| **16** | **Flags** | **yes** | **yes** | **yes** |
| **17** | **Submit Clip** | **yes** | **yes** | **yes** |
| **18** | **Completed Campaigns** | **yes** | **yes** | **yes** |
| 19 to 27 | Change referrer, Archive, AI Knowledge, Poster Applications, Disputes, Strike Config, Gamification, Recalculate Earnings, Reviewer Queue | yes | yes | yes |
| 28 | Reviewer Audit (scope) | yes | yes | yes |

`ALL 28 items reachable  28/28` at each width, with **Flags, Submit Clip and Completed Campaigns asserted
individually by name** because the owner named them, and the **last** row asserted separately because it is
the one the height defect was hiding.

## 3.5 The drawer scrolls and the page behind does not

Ten hard drags inside the drawer, deliberately far past its end to force any chaining, then one drag
directly over the page behind it:

```
background <main>   0 -> 0
window              0 -> 0
body                0 -> 0
documentElement     0 -> 0
the drawer          reached scrollTop 805 during those same gestures
```

**The drawer moved. Nothing behind it did.** That is the property BL-318 through BL-321 were chasing, and
it survives.

**Opening, closing and dismissing:** untouched by this round, and structurally so. The change adds one
early return inside a `touchmove` handler. `preventDefault` on **touchmove** has never blocked
`touchstart`, `touchend` or `click` (BL-320 relied on exactly this so nav links kept working), so every
open, close and dismiss path is byte-identical: the hamburger (`app-layout.tsx:996`), Escape (`:104`), the
backdrop (`:866`), the tap-shield (`:1125`), route change (`:96`) and the swipe gesture (`:492-608`) are
none of them in the diff.

---

# PART 4 — DESKTOP AND THE PWA

## 4.1 Desktop, proven rather than argued

The component is shared, so the height change was measured **both ways in the real desktop structure**: a
wrapper carrying an inline transform, exactly as `app-layout.tsx:817-821` does.

```
DESKTOP: h-[100dvh] and h-full render the SAME height inside the transform wrapper   new 900px vs old 900px
desktop aside height equals the viewport      900px vs 900px
desktop aside is still position:fixed         yes
desktop aside is still 240px wide (w-60)      240px
desktop nav still overflow-y:auto             yes
desktop nav still scrollable                  yes
desktop WHEEL scroll still works              scrollTop 0 -> 400
```

**The height change is a measured no-op on desktop**, because the transform wrapper already made `h-full`
resolve to `100dvh` there.

**The touchmove change cannot reach desktop at all, structurally rather than by judgement:** the effect is
gated on `mobileOpen` (`app-layout.tsx:129`), the only control that sets it is `lg:hidden`, and **a wheel
never fires `touchmove`**. The last line above is the direct evidence: desktop scrolling is a wheel path
and it still works.

## 4.2 The PWA, and everything that relied on the guard

**What relied on the guard was one thing: the background scroll lock while the drawer is open.** It is
named in PART 0.2, and PART 3.5 proves it still holds, including under drags deliberately pushed past the
scroller's end.

**The launch experience is not affected, and here is why rather than an assurance.** The guard is
installed inside `useEffect(..., [mobileOpen])` with `if (!mobileOpen) return` as its first line
(`app-layout.tsx:129`). It **does not exist** unless the drawer is open. It cannot participate in launch,
in the splash screen, in hydration, or in any first paint. The round adds no import, no state, no effect
and no render-path branch, so there is no new work at startup. **Ordinary page scrolling with the drawer
closed is byte-identical**: with `mobileOpen` false there is no listener on `document` at all.

**No modal or overlay relied on it.** `modal.tsx` has its own handling and is not in the diff; the
`PWAInstallPopup`, the voice-call banner and the notification toasts are untouched. Nothing else in the
repo references the listener, which is a closure created and destroyed inside that one effect.

**Where the PWA is genuinely affected, it is affected for the better.** In standalone there is no browser
chrome, so `100dvh` equals the full screen, which is exactly why the safe-area padding in PART 2 was taken
in this round rather than deferred: without it the final nav row would sit under the home indicator.

---

# PART 5 — THE EVIDENCE

| Claim | Where |
|---|---|
| Full diff of both changes | PART 1.1 and PART 2, and the commit |
| Permitted versus still-prevented touches | PART 1.2, eight measured cases |
| Original protection still holds outside the drawer | PART 1.2 and PART 3.5 |
| All 28 items reachable at 320, 375 and 414 | PART 3.4, `28/28` at each width |
| Flags, Submit Clip, Completed Campaigns | PART 3.4, asserted individually by name |
| Drawer opens, scrolls, closes | PART 3.5 |
| Page behind does not scroll while the drawer does | PART 3.5, four counters all `0 -> 0` |
| Desktop unchanged | PART 4.1, including old-versus-new height measured side by side |
| PWA and anything relying on the guard | PART 4.2 |
| No money, clip or payout state touched | below |

## 5.1 Nothing near the money

**No database access of any kind this round**: no query was written, read or run, and no script touched
`run-select.js`. **No API route, no query, no schema, no `prisma migrate`.** No clip, campaign, payout,
earning or balance code path is in the diff. The two files changed are a layout component and a navigation
component.

Money files, working tree `git hash-object` against the `origin/main` blob OID, all **IDENTICAL**:

```
ac5be7de clip-earnings-writer   797e2098 earnings-calc   e887f80a balance   83ce4bab tracking
61cef393 clip-earnings-invariant-middleware   ef5cdae7 money-decimal   106e16ad campaign-era
```

`tracking.ts` does not appear in the diff.

## 5.2 Gates, stated honestly

* `npm ci` **exit 0**; `npx prisma generate` **exit 0**, run after it because `npm ci` wipes the client. Isolated worktree at `C:/b739`, a short path, `.env` and `.env.local` copied, **no `node_modules` junction**.
* `tsc --noEmit` **exit 0, 0 errors** (log was 0 lines).
* `npm run build` **exit 0 pre-commit and exit 0 post-commit**, `✓ Compiled successfully` both times, read from a log with the exit code **echoed, never piped through `tail`**.
* Hooks gate **11 problems, 0 errors, 11 warnings, at the limit of 11**, with **eslint v9.39.4 confirmed present** so the gate is not silently a no-op. `check:prisma-bypass` and `check:removed-fields` both ran and passed as part of `prebuild`.
* Harness **53 passed, 0 failed, exit 0**.
* Push **verified**: `safe-push.mjs` reported `VERIFIED PUSHED`, and `git ls-remote` independently agrees.

**One correction made and verified, disclosed rather than buried:** `origin/main` advanced from `dd5d03f9`
to `6d906941` (BL-736 merging) between the fetch and the tagging, so `pre-BL-739` was first created
pointing at the moved main. It was repointed to this branch's **true base** `dd5d03f9` and force-updated on
the remote; `ls-remote` confirms `dd5d03f9`. **BL-736 touched neither of this round's two files** (`git
diff --name-only` across that range returns 0 for both), so the merge is conflict-free on these paths.

## 5.3 Accessibility

Reviewed by the accessibility lead **before any UI was written**, coordinating the modal and
keyboard-navigation specialists.

**Its recommendation was overruled on one point, and that was the whole round.** Both specialists
independently endorsed `closest("[data-drawer-panel]")`, the panel-wide selector, one of them calling it
"safe for both variants, regresses nothing". Neither had been given `BACKLOG.md:2001`. Presented with it,
the lead reversed and confirmed the scroller-scoped selector with the `scrollHeight > clientHeight` test.
**Both were reasoning correctly from the components; the constraint lived in the history.**

Applied from the review: the safe-area padding taken in this round rather than deferred, on the PWA
argument in PART 4.2. Confirmed by the review: pinch-zoom preserved (SC 1.4.4); both changes are
focus-neutral and make nothing worse for focus, `aria-hidden` or the hamburger; the height change improves
where the focus ring comes to rest for the last nav item. Corrected by the review: **lucide already emits
`aria-hidden` on its icons**, so no icon change was needed.

**Deliberately not taken, and the reasoning matters:** BL-737's FIX 3, `data-no-swipe` on the nav. It
would stop diagonal drags being claimed by the swipe handler, but it also **kills swipe-to-close across
roughly 80% of the drawer's area**. That is a larger and more noticeable regression than an occasional
diagonal drag, and the swipe handler already yields to any predominantly-vertical gesture
(`app-layout.tsx:543`). **Trading one annoyance for another is what this round was told not to do.**

**Filed, not fixed**, all pre-existing and none touched by this diff: `app-layout.tsx:982` suppresses the
entire mobile topbar on `/campaigns/[id]` and the hamburger at `:996` lives inside it, so on a campaign
detail page a mobile keyboard or switch-control user has **no way to open navigation at all** (**SC 2.1.1,
Level A**, and stricter than anything in the drawer); the hamburger has no accessible name; `aria-hidden`
sits on an always-mounted panel holding about 30 focusable links (`:842`, with `BottomNav.tsx:364`'s
`inert` as the in-repo pattern); there is no focus management on open or close;
`use-scroll-nav-translate.ts:96-107` can leave the desktop sidebar resting fully hidden yet focusable (SC
2.4.7); and the authenticated app has no skip link.

## 5.4 A note on the design skill

The `frontend-design` skill was read as instructed. **No anchor was picked, deliberately.** This round
changes a touch-event condition, one height class, one attribute and one padding token. It introduces no
new visual surface, no new strings and no new components, so there is nothing for an anchor to govern, and
committing to one would have meant redesigning the drawer, which directly contradicts PART 4's requirement
to prove desktop and mobile unchanged. The existing design system stands untouched.

---

# WHAT SHIPPED

`app-layout.tsx`, `sidebar.tsx`, plus `scripts/test-bl-739-drawer-scroll.mjs` and the `BACKLOG.md` entry.
**2 source files, 52 insertions, 3 deletions**, 39 of those insertions being comments.

**Rollback:** `git revert -m 1 <merge>`, or `git reset --hard pre-BL-739`. **Nothing to undo in the
database.**

**Not merged to main.** This is a branch round; the merge is its own step, and `main` has since moved to
`6d906941` with no overlap on these two files.
