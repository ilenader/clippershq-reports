# BL-701 — the landing hero button row stops stretching once the sidebar nav appears

**Branch** `checkpoint/BL-701` from `origin/main` f7a1a344. **Files changed: exactly one**, `src/app/preview/preview-landing.tsx`, one hunk, one class string plus its rationale comment. Isolated worktree `C:/b701`, no `node_modules` junction.

---

## PART 1 — the breakpoint was found, not guessed

The owner defined the trigger behaviourally: the width at which the nav stops being three lines behind a hamburger and shows Home, Campaigns and Live Support inline. That is **Tailwind `lg`, `min-width: 64rem` = 1024px**, and it is the value the constraint now uses.

* `src/app/preview/preview-shell.tsx:141` — `<aside className="hidden w-60 shrink-0 flex-col ... lg:flex">` is the sidebar that holds the three links (`NavLinks`, `preview-shell.tsx:56`).
* `src/app/preview/preview-shell.tsx:183` — the hamburger `<button aria-label="Menu" ... lg:hidden>`.
* `node_modules/tailwindcss/theme.css:329` — `--breakpoint-lg: 64rem`. Tailwind 4.2.2, no `tailwind.config`, and `src/app/globals.css` `@theme inline` (line 3) declares no `--breakpoint-*` override, so the default stands.

Proven in the browser rather than inferred. Stepping the viewport across the boundary, the sidebar and hamburger flip in exact lockstep with `matchMedia("(min-width: 64rem)")`:

```
set 1022  mq64rem=false  aside=none  hamburger=grid
set 1023  mq64rem=false  aside=none  hamburger=grid
set 1024  mq64rem=false  aside=none  hamburger=grid
set 1025  mq64rem=true   aside=flex  hamburger=none
set 1026  mq64rem=true   aside=flex  hamburger=none
```

The flip reads at "1025" in set-width terms only because this display runs at devicePixelRatio 1.302, so a nominal 1024px box lands on 1023.74 real CSS px. The media condition itself is 64rem, and the two behaviours now change on that one condition.

## PART 2 — what changed

```
- <div className="mt-4 flex items-stretch gap-3 sm:mt-7 sm:gap-4">
+ <div className="mt-4 flex items-stretch gap-3 sm:mt-7 sm:gap-4 lg:grid lg:w-fit lg:grid-cols-2">
```

Below `lg` the row is still the same flex line. At `lg` and above it becomes a `fit-content` box with two `minmax(0,1fr)` columns. Two equal columns inside a fit-content box each resolve to the **wider** item's max-content, so the buttons stay exactly equal to each other and keep their full natural size, and it is the ROW that stops stretching. `flex-1 basis-0` simply goes inert under `display:grid`; `min-w-0` still applies and is a harmless no-op there because the `0` in `minmax(0,1fr)` already suppresses the automatic minimum size.

**Resulting desktop widths:** each button **237.83 x 57.5px**, label on one line, at 1024.51, 1100, 1280, 1440 and 1920px alike. Before the change the same buttons were 344.26 / 472.13 / 552.00px wide at 1024.51 / 1280 / 1440.

**Alignment to the hero text column: it did NOT align, deliberately, and here is why.** The h1 sits in `sm:max-w-3xl` (measured 768px) and the paragraph in `sm:max-w-2xl` (672px). Both are *wider* than half the hero at every desktop width tested (half is 520px at 1280, 600px at 1440), so aligning the row to them would push it further right, the opposite of the ask. What the row does share is the **left edge**: h1, paragraph and row all start at x=280 at 1280px, so the left side still reads as one block.

**`lg:max-w-[50%]` was measured and rejected.** It produces 232.07px buttons at 1280px, 5.8px short of what "Launch a campaign" needs, so the label wraps to two lines and the button grows to 65.5px tall. The owner's rule is that the buttons must not be shrunk or cramped and that only the row stops stretching, so the natural-width grid wins. **Stated plainly: at 1280px the row ends 11.5px past the hero midline, 51.1% of the hero rather than 50.0%.** From about 1303px up it is inside the left half outright (44.3% at 1440, 31.6% at 1920). Between 1024 and ~1200px the hero is too narrow for two full-size buttons to fit inside half of it at all, and there the buttons win, by the owner's own rule.

## PART 3 — measurements, BEFORE and AFTER at identical viewports

Chrome, the real page on a local build, measured in an iframe harness whose width IS the viewport CSS media queries evaluate against, with scrollbar gutters suppressed so the box matches a phone's overlay scrollbars. The harness reproduces BL-694's published figures exactly, which is what validates it. BEFORE was captured by stashing the change and re-running the identical sweep, so the two columns are the same code path at the same pixel width.

| target | achieved vw | nav | row display | button BEFORE | button AFTER | row right edge BEFORE | AFTER | hero midline |
|---|---|---|---|---|---|---|---|---|
| 320 | 320.26 | hamburger | flex to flex | **134.14** | **134.14** | 300.3 | 300.3 | 160.1 |
| 375 | 375.55 | hamburger | flex to flex | **161.78** | **161.78** | 355.6 | 355.6 | 187.8 |
| 414 | 413.95 | hamburger | flex to flex | **180.98** | **180.98** | 394.0 | 394.0 | 207.0 |
| 768 | 768.00 | hamburger | flex to flex | 344.00 | 344.00 | 736.0 | 736.0 | 384.0 |
| 1023 | 1022.98 | hamburger | flex to flex | 471.49 | 471.49 | 991.0 | 991.0 | 511.5 |
| just below lg | 1023.74 | hamburger | flex to flex | 471.88 | 471.88 | 991.8 | 991.8 | 511.9 |
| just above lg | 1024.51 | inline | flex to **grid** | 344.26 | **237.83** | 984.5 | **771.6** | 632.3 |
| 1100 | 1100.54 | inline | flex to **grid** | — | **237.83** | — | **771.6** | 670.3 |
| 1280 | 1280.26 | inline | flex to **grid** | 472.13 | **237.83** | 1240.3 | **771.6** | 760.1 |
| 1440 | 1440.00 | inline | flex to **grid** | 552.00 | **237.83** | 1400.0 | **771.6** | 840.0 |

**No mobile regression.** BL-694 published 134, 161.5 and 181px at 320, 375 and 414. Re-measured here: 134.14, 161.78, 180.98 — and critically, byte-for-byte the same numbers with and without this change, because a `lg:` variant cannot match below 1024px. The computed `display` of the row is still `flex` at all four of 320, 375, 414 and 768. The 161.78 against BL-694's 161.5 is not movement: it is the achieved viewport, 375.55 rather than 374.8, at 0.5x button width. Height is unchanged at every width (54px at 320 where the label wraps, 48px at 375 and 414, 57.5px from 640 up).

**The boundary does not jump awkwardly and nothing overlaps.** Crossing 64rem the row's right edge goes 991.8 to 771.6 and the button 471.88 to 237.83, but the label stays on ONE line and the height stays 57.5px on both sides, so no reflow of the label and no clipping. The boundary already carried a much larger discontinuity that this change did not introduce: the 240px sidebar appears there, so the hero itself steps from 1023.7px wide to 784.5px. The row moves LEFT, away from the hero `<section>`'s `overflow-hidden`, so it is strictly further from any clipping edge than before.

## PART 4 — what was NOT touched

Exactly one file, one hunk at line 208. `git status` shows `M src/app/preview/preview-landing.tsx` and nothing else.

* **Calendly URL byte-identical and never retyped:** it is not in the diff at all (`git diff | grep -c calendly` = 0). On disk at line 254 it is `https://calendly.com/clipershq/30min`, which matches `public/brands.html:354` exactly. `target="_blank"` and `rel="noopener noreferrer"` confirmed live in the rendered DOM at every width measured.
* **"Get started"** keeps `/login` and same-tab `next/link` navigation.
* **The signed-in hero is byte-identical:** the `isLoggedIn` branch is not in the diff (`git diff | grep -c "Go to dashboard"` = 0). No logged-in user sees the booking link.
* Labels, destinations, behaviour, colours, copy, the hero imagery and every other section: untouched. No navigation behaviour, API, auth or data path touched. No dashes as bullets.

## PART 5 — evidence

* **Breakpoints match:** constraint `lg:` on `preview-landing.tsx:248`; nav `lg:flex` on `preview-shell.tsx:141` and `lg:hidden` on `preview-shell.tsx:183`; both are `min-width: 64rem` from `tailwindcss/theme.css:329`. The matchMedia lockstep table is in PART 1.
* **Left half at 1280 and 1440:** row right edge 771.6 against midlines 760.1 and 840.0, so 51.1% and 44.3% of the hero. Rendered against a drawn midline the right half is visually clear of the row at both; at 1440 the row ends 68.4px before the midline. The 11.5px overshoot at 1280 is stated in PART 2 rather than hidden.
* **Mobile unchanged:** the three phone rows of the PART 3 table are identical in both columns.
* **Boundary clean:** 1023.74 and 1024.51 both give a one-line label and a 57.5px tall button; no wrap, no overlap, no clipping.
* **Equal size and click targets:** the BEFORE/AFTER sweep records `|widthA - widthB|` = **0.000px** at every desktop width. 237.83 x 57.5 clears SC 2.5.8 (24x24) by 9.9x by 2.4x and SC 2.5.5 AAA (44x44) by 5.4x by 1.3x. The narrowest case anywhere, 134.14 x 54 at 320px, also clears AAA.
* **a11y-lead: GO.** Verdict on the exact diff, with keyboard-navigator and contrast-master both clean. Confirmed: no DOM, focus or accessibility-tree change (no `order-*`, `grid-flow-dense`, `col-start` or RTL anywhere in `src/app/preview`, and two items auto-place into columns 1 and 2 in DOM order); Reflow SC 1.4.10 safe because `lg` never matches at a 320px viewport and 400% zoom of 1280 lands at 640; `items-stretch` keeps equal heights under grid because both items share one auto-sized row track; and at 200% text zoom `fit-content` clamps at the 960px stretch size and reproduces today's pre-edit outcome exactly. Its one finding was documentation-only, that the existing "equal BY CONSTRUCTION" comment no longer describes the >=1024px path; applied in the comment now in the file.

## Gates, honestly

`npm run build` **BUILD_EXIT=0**. `npx tsc --noEmit` **TSC_EXIT=0**. Prebuild gates: prisma-bypass check pass, removed-fields check pass, **BL-348 hooks gate 0 errors / 11 warnings** (limit 11) with eslint **v9.39.4** actually present in the worktree, so the gate ran rather than silently no-opping. `npm ci` wiped the generated Prisma client, so `npx prisma generate` was run before any typecheck. Build read from a log file with the exit code echoed directly, never through a pipe.

## Safety

6 money files plus `tracking.ts` and `campaign-era.ts` **byte-identical by blob OID** on `origin/main`, on `HEAD` and in the working tree: `clip-earnings-writer.ts` 7aa6be48, `earnings-calc.ts` 797e2098, `balance.ts` e887f80a, `tracking.ts` 847dcf70, `clip-earnings-invariant-middleware.ts` 61cef393, `money-decimal.ts` ef5cdae7, `campaign-era.ts` 106e16ad. No clip earnings or status changed, no payout created, modified, approved or cancelled, no DB write of any kind, no `prisma migrate`. Nothing held by BL-698, BL-699 or BL-700 was touched.

**Rollback:** `git revert -m 1 <merge>`, or `reset --hard pre-merge-BL-701`.
