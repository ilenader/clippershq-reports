# BL-705 — the clarifying line under the landing hero buttons, removed

Branch `checkpoint/BL-705` (`a8b09a1b`) from `origin/main` `55e757ce`, merged as `0112361e`. Isolated worktree `C:/b705`, no `node_modules` junction. **One source file changed**, `src/app/preview/preview-landing.tsx`, plus its BACKLOG entry.

---

## PART 1 — removed, wrapper and all

BL-699's line **"Book a call is for brands. Get started is for clippers."** is gone. Three things went with it, because all three existed only for it:

1. the `<p>` itself,
2. the 52-line BL-699 comment block that documented only that element,
3. the `<>` / `</>` fragment BL-699 added so the row and the paragraph could be siblings. With the paragraph gone it wrapped a single child, so it was deleted rather than left as a no-op. React fragments emit no DOM, so removing it is byte-identical in rendered output.

**The entire structural diff is five removed lines.** Filtering the diff to JSX elements returns exactly:

```
-          <>
-          <p className="mt-3 max-w-[42ch] text-pretty rounded-xl bg-[color-mix(in_srgb,#09090b_78%,transparent)] px-3 py-2 text-[12px] font-medium leading-snug text-white backdrop-blur-sm sm:mt-4 sm:max-w-2xl sm:px-4 sm:py-2.5 sm:text-sm">
-            <span className="font-semibold">Book a call</span> is for brands. <span className="font-semibold">Get started</span> is for clippers.
-          </p>
-          </>
```

**Nothing needed adjusting, and nothing was left behind.** The paragraph carried `mt-3 sm:mt-4`, a **top** margin only, so it never contributed bottom spacing; the gap under the buttons was always owned by the container's `pb-6 sm:pb-16` at line 133. Measured on the result rather than assumed: the row div is now `lastElementChild` of a **4-child** container, and the gap below it is **exactly 24.0px against `padding-bottom: 24px`** at 320, 375 and 414, and **exactly 64.0px against `padding-bottom: 64px`** at 1280 and 1440. That is the container padding and nothing else, so there is no orphaned margin and no empty gap. There is no empty element either: the trap here was real and the a11y lead named it, since line 402 carried `px-3 py-2 rounded-xl` plus a background, so emptying the `<p>` rather than deleting it would have rendered a visible plate roughly 32px tall. The hero simply shortens, which is the owner's requested outcome. The hero has **zero** horizontal overflow at every width (`scrollWidth == clientWidth`).

## PART 3 — every BL-703 figure re-measured, all unchanged

Chrome, real page on a local build, iframe-viewport harness with scrollbar gutters suppressed, the same method that reproduced BL-694's published figures.

| viewport | nav | row display | button A | button B | equal to | height | label lines | row width | row right | hero midline | row as % of hero | gap below row | container `padding-bottom` | hero overflow |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 320 | hamburger | flex | **134.14** | **134.14** | 0.000px | 54.0 | 2 | 280.27 | 300.3 | 160.1 | — | **24.0** | 24px | 0 |
| 375 | hamburger | flex | **161.78** | **161.78** | 0.000px | 48.0 | 1 | 335.57 | 355.6 | 187.8 | — | **24.0** | 24px | 0 |
| 414 | hamburger | flex | **180.98** | **180.98** | 0.000px | 48.0 | 1 | 373.97 | 394.0 | 207.0 | — | **24.0** | 24px | 0 |
| 1280 | inline | **grid** | **235.74** | **235.74** | 0.000px | 57.5 | 1 | **487.48** | **767.5** | 760.1 | **50.7%** | **64.0** | 64px | 0 |
| 1440 | inline | **grid** | **235.74** | **235.74** | 0.000px | 57.5 | 1 | **487.48** | **767.5** | 840.0 | **44.0%** | **64.0** | 64px | 0 |

Every figure matches BL-703 exactly: **235.74px at 1280 and 1440 with the row at 50.7% and 44.0% of the hero**, and **134.14 / 161.78 / 180.98px** on mobile. `rowDisplay` is `flex` below `lg` and `grid` at and above it, so BL-701's constraint is intact and still keyed to the navigation's own breakpoint. The clarifying line's element count in the rendered DOM is **0** at all five widths.

## PART 2 — everything else kept exactly

* **Labels unchanged:** "Brands: book a call" and "Get started", read back from the rendered DOM at all five widths.
* **Calendly URL byte-identical and never re-typed.** Source still `https://calendly.com/clipershq/30min`, matching `public/brands.html:354` exactly, and the compiled bundle contains exactly **one distinct** calendly string, that one. `target="_blank"` and `rel="noopener noreferrer"` confirmed in the rendered DOM.
* **"Get started" keeps `/login` and same-tab navigation:** `href` `/login`, `target` `null` at all five widths.
* **The signed-in hero is byte-identical.** The extracted `isLoggedIn ?` JSX block hashes to `a8069cbb4010c4d2edd5431ef0f87d6384669c30b014745b2ed65a1cbb5362a1` on `origin/main` and on this branch, and `git diff` shows **0** changed lines mentioning "Go to dashboard". No logged-in user sees the booking link.
* **BL-701's width constraint survives:** `lg:grid lg:w-fit lg:grid-cols-2` is still on the row div, and `git diff` shows **0** changed lines touching it.

**The one instruction that could not be honoured, stated plainly.** The round asked that BL-699's pinned contrast literal survive. It cannot: `bg-[color-mix(in_srgb,#09090b_78%,transparent)]` was an attribute **of the deleted `<p>` and of no other element**, so the protection left with the element it protected. The a11y lead confirmed independently that no surviving element loses any contrast it currently has, and that the only way to "keep" the literal would be to re-key the secondary button's background, a visual change to a surviving control and outside a removal-only round. This is a clean return to the pre-BL-699 state, not a regression. The count of at-risk elements is unchanged.

**The live SC 1.4.3 risk is now in BACKLOG, recorded before its only documentation was deleted** (a11y-lead Finding B, actioned). The deleted comment block was the sole written record of a defect on a **surviving** element: the secondary "Get started" `Link` keys its fill to `var(--bg-primary,#09090b)`, and that fallback is dead code because `--bg-primary` is never declared on `:root`, only inside `.dark` (`globals.css:34`, #09090b) and `.light` (`:114`, #fafafa). A CSS var fallback fires only when the property is **undefined**, never when it is redefined, so under `.light` that pill composites 78% #fafafa and white text on it falls to about **1.03:1**. It predates BL-699 and this round neither creates nor deepens it. Durable fix, for its own round: a `--hero-scrim` token on `:root` plus validating the persisted theme value at `theme-provider.tsx:26`.

## PART 4 — evidence

* **Clean removal, no leftover element or gap:** clarifying-text elements in the rendered DOM = **0**; `<>` and `</>` occurrences in the file = **0**; empty `<p></p>` = **0**; the pinned literal = **0** occurrences, gone with its element. The row is `lastElementChild` and the gap below it equals the container's `padding-bottom` to the pixel at every width. In the compiled output the sentence survives **only** inside `.next/server/chunks/ssr/…preview-landing…js.map`, the sourcemap, because the replacement comment quotes what was removed; it appears in **no** executable chunk and **no** rendered page.
* **Labels, URL and destinations unchanged:** `git diff` changed-line counts are **0** for the Calendly URL, **0** for the row div's `lg:grid lg:w-fit`, **0** for either label, and **0** for "Go to dashboard".
* **Contrast literal and width constraint:** the width constraint survives verbatim; the contrast literal necessarily did not, for the reason given above, with the a11y lead's confirmation that nothing surviving is worse off.
* **Signed-in hero:** identical sha256 on both refs, quoted above.
* **Measurements:** the five-width table above matches BL-703 figure for figure.
* **Nothing else changed:** the merged diff against `origin/main` is two files, `BACKLOG.md` and `src/app/preview/preview-landing.tsx`, 26 insertions and 58 deletions. No logged-in surface, navigation, API, auth or data path touched. Nothing held by BL-704 touched.

## Accessibility review

**GO-WITH-NOTES, nothing merge-blocking, and the lead corrected its own earlier review.** BL-699's disambiguator had **no `id`**, and there is **no `aria-describedby` or `aria-labelledby` anywhere** in the file, so the paragraph was never in either control's accessible name or description; as a separate paragraph containing no link it was never "programmatically determined link context" either. It therefore was never what satisfied SC 2.4.4, and the lead withdrew that claim from its BL-699 review.

**No success criterion moves from pass to fail.** SC 2.4.4 stands on the two labels before and after, and both pass. SC 1.3.1 never depended on it, because after BL-699 the audience split is carried in the **label text itself** ("Brands: …") rather than by position, colour or prominence, so there is no presentation-only relationship left needing a text equivalent. SC 1.3.3 trivially improves, since that sentence was the only element in the block that could ever have referenced controls by position. The honest loss is **one sentence of linear reading order**, a cognitive supporting affordance, not an AA criterion; the mis-click defect BL-699 was chasing was fixed by the **label**, which stays. Removal is a **literal no-op** for links-list and rotor navigation, because a `<p>` never appeared there. The accessible name is still `Brands: book a call (opens in a new tab)` with the visible text leading, so SC 2.5.3 holds; the two labels share **zero** tokens, so there is no near-identical-text ambiguity. No import becomes unused (`ArrowRight`, `Link`, `useState` all still used), no orphaned `sr-only`, no dangling `id`. The lead explicitly advised **against** folding audience text into the labels via `sr-only` as compensation, since both labels already carry their purpose and it would be verbosity a rotor user pays for on every pass.

## Gates, honestly

`npm ci` **exit 0**, then `npx prisma generate` **exit 0** before any typecheck, because `npm ci` wipes the generated client. `npx tsc --noEmit` **TSC_EXIT=0 with 0 output lines**. `npm run build` **BUILD_EXIT=0** on the branch and again on the merged tree, read from a log with the exit code echoed directly, never through a pipe. Prebuild: BYPASS detector **0 violations**, removed-fields **OK**, **hooks gate 0 errors / 11 warnings** (limit 11) with eslint **v9.39.4** confirmed present in the worktree so the gate ran rather than silently no-opping. 61/61 static pages. The `.tsx` diff was confirmed non-empty before any claim was made: 15 insertions, 58 deletions in that file alone.

## Safety

6 money files plus `tracking.ts` and `campaign-era.ts` **byte-identical by blob OID** on both refs: `clip-earnings-writer.ts` 7aa6be48, `earnings-calc.ts` 797e2098, `balance.ts` e887f80a, `tracking.ts` 847dcf70, `clip-earnings-invariant-middleware.ts` 61cef393, `money-decimal.ts` ef5cdae7, `campaign-era.ts` 106e16ad. No clip earnings or status changed, no payout touched, no DB write of any kind, no `prisma migrate`. No heredocs; one shell at a time. NO dashes.

**Rollback:** `git revert -m 1 0112361e`, or `reset --hard pre-merge-BL-705`.
