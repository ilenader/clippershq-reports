# BL-703 — merge round: BL-699 onto main, union-resolved against BL-701

`main` moved `22212d26` to **`55e757ce`**, verified by `git ls-remote`. Tags `pre-merge-BL-703` (`22212d26`) and `post-merge-BL-703` (`55e757ce`) are on origin.

---

## STEP 0 — truth, with SHAs

`checkpoint/BL-699` = **`b1f3bb11a2e5ea2d89d0e4959b176e6f225e6545`**, on origin, and `git merge-base --is-ancestor origin/checkpoint/BL-699 origin/main` returned non-zero before this round, so it was **genuinely unmerged**. Its **code diff is non-empty**: **152 changed lines** in `src/app/preview/preview-landing.tsx`, plus `docs/BL-699-CLIENT-CTA-LABEL.md` (251 lines) and its BACKLOG entry. Nothing else was merged: every other `checkpoint/BL-70x` branch on origin (`BL-700` `56703453`, `BL-701` `9bcbe7aa`) is already an ancestor of main from earlier rounds, and no live round's branch was touched.

## Where the merge ran

`C:/b575` holds branch `main` at `91b84410`, stale by roughly a hundred commits **and** dirty with **77** entries. It was not touched, and re-checked at the end it is still branch `main`, still `91b84410`, still 77 entries. The merge ran in a fresh detached worktree at the short path `C:/m703` with its own real `npm ci` (822 packages, exit 0), no `node_modules` junction, and was pushed as `HEAD:main`. `scripts/safe-push.mjs` cannot be used for the branch from a detached worktree, because it resolves the stale local `main` ref; BL-288's own assertion was run instead, `git ls-remote origin refs/heads/main` == local HEAD, and it passed. Tags were pushed normally.

## The conflict, resolved as a union

Two conflicts. `preview-landing.tsx` was the real one and it landed exactly where expected: BL-699 branched before BL-701, so both sides rewrote the same JSX line. Main's side carried BL-701's `lg:grid lg:w-fit lg:grid-cols-2` and **no** fragment; BL-699's side carried the `<>` fragment opener and **no** `lg:` classes. Git offered them as alternatives, not a union, and the closing `</>` sits outside the conflict region, so taking either side alone would have either dropped BL-701's constraint or left an orphaned `</>` and a JSX parse error.

**The resolved region, printed verbatim** (`src/app/preview/preview-landing.tsx:298-300`), with BL-701's entire rationale comment preserved above it:

```
             and ~1200px the hero is too narrow for two full-size buttons to
             fit inside half of it at all, and there the buttons win, by the
             owner's own rule. */
          <>
          <div className="mt-4 flex items-stretch gap-3 sm:mt-7 sm:gap-4 lg:grid lg:w-fit lg:grid-cols-2">
```

Both survive: BL-699's fragment, new label, contrast fix and clarifying line, **and** BL-701's width constraint and its full provenance comment.

`BACKLOG.md` was the second conflict, an append-versus-append at the tail, resolved as a union keeping every entry. Counted with `grep -c`, never piped: **108** entries at the merge base `f7a1a344`, **112** on main, **109** on the branch, **113** after the union over 19821 lines. **Zero conflict markers** in the tracked tree.

## The longer label was RE-MEASURED, and it does not wrap

Measured in Chrome on the merged tree, real page, iframe-viewport harness with scrollbar gutters suppressed.

| viewport | nav | row display | button each | equal to | label lines | height | row right edge | hero midline | row as % of hero |
|---|---|---|---|---|---|---|---|---|---|
| 320 | hamburger | flex | **134.14** | 0.000px | 2 | 54.0 | 300.3 | 160.1 | unchanged |
| 375 | hamburger | flex | **161.78** | 0.000px | 1 | 48.0 | 355.6 | 187.8 | unchanged |
| 414 | hamburger | flex | **180.98** | 0.000px | 1 | 48.0 | 394.0 | 207.0 | unchanged |
| 1280 | inline | **grid** | **235.74** | 0.000px | **1** | 57.5 | **767.5** | 760.1 | **50.7%** |
| 1440 | inline | **grid** | **235.74** | 0.000px | **1** | 57.5 | **767.5** | 840.0 | **44.0%** |

**It does not wrap and it does not push past the constraint. It got slightly better.** "Brands: book a call" renders **narrower** than "Launch a campaign" despite being two characters longer, because its glyphs are narrower: 235.74px per button against BL-701's 237.83px, so the row is 487.48px instead of 491.65px. At 1280 it ends 7.3px past the hero midline (50.7%) where BL-701 measured 11.5px (51.1%); at 1440 it ends 72.5px **before** the midline. Label on one line, height unchanged at 57.5px, the two buttons equal to **0.000px**, no truncation (there is no `truncate`, `line-clamp` or `whitespace-nowrap` on either control), and no collision with the pyramid, which sits at roughly 65% of the hero.

**One thing the owner should decide, stated plainly rather than shipped quietly.** The new clarifying line is a **sibling** of the button row, not inside it, so BL-701's width constraint does not apply to it. It takes `sm:max-w-2xl`, **672px**, ending at x=952 at both 1280 and 1440, which crosses the hero midline. That is the same width as the hero subline directly above it, so it is consistent with the existing hero text rather than a new outlier, and the button row itself is unaffected. If the owner wants the whole left block inside the left half, that paragraph needs its own constraint in a later round. Nothing here was changed to force it, because this round is merge-only.

**Mobile is unchanged.** 134.14 / 161.78 / 180.98px at 320 / 375 / 414, identical to BL-701's post-merge figures and to BL-694's published 134 / 161.5 / 181, with the row still computing `display: flex` below `lg`. The hero has **zero** horizontal overflow at 320: `scrollWidth == clientWidth == 320` and no overflowing descendants. The document's 339px `scrollWidth` at that width comes entirely from the pre-existing horizontally scrollable campaign carousel below the hero, proven by hiding the **whole hero** and watching it stay 339.

## The contrast fix is real, and it was verified independently

`--bg-primary` is not on `:root`; it exists only at `globals.css:34` (`.dark`, `#09090b`) and `globals.css:113` (`.light`, `#fafafa`). A CSS var fallback fires only when the property is undefined, never when it is redefined, so under `.light` the old declaration resolves to the light value.

Measured, not argued. A **fresh** element created after forcing `.light`, carrying the OLD declaration `color-mix(in srgb, var(--bg-primary,#09090b) 78%, transparent)`, computes to `color(srgb 0.980392 0.980392 0.980392 / 0.78)`, i.e. **#fafafa at 78%**. Over a worst-case white photo pixel that composites to 251.1 per channel, and white text on it lands at **1.03:1**, exactly the figure BL-699 published. The NEW pinned literal `color-mix(in srgb, #09090b 78%, transparent)` computes to #09090b at 78% in **both** themes, composites to rgb(63, 63, 65), and measures **10.51:1** with white text. So the pin holds contrast in every theme, as claimed.

**A nuance worth recording rather than glossing.** The unvalidated restore at `theme-provider.tsx:26` is exactly as described (`localStorage.getItem("theme") as Theme | null; if (saved) setTheme(saved)`, no validation, and `:34` strips the SSR `dark` class), and `/preview` has no own layout so it sits under the root `ThemeProvider` at `layout.tsx:498`. But with a stale `theme=light` in localStorage across a full reload, the /preview route **stayed `.dark`** and did not rewrite storage, which indicates the provider's effects did not run on that route in dev. The pin is correct and costs nothing either way; it is defence whose trigger I could not reproduce on this page. The **untouched** secondary "Get started" button still carries the same dead `var(--bg-primary,#09090b)` fallback, which BL-699 flags but deliberately does not fix.

## Confirmations on the merged result

* **The label reads "Brands: book a call"**, one line, with the clarifying line beneath: **"Book a call is for brands. Get started is for clippers."**, present in the rendered DOM at every width measured.
* **Calendly URL byte-identical in source AND in the compiled bundle**, never retyped. Source and `public/brands.html:354` both sha256 `dddbbec91fbececf880331cd55453d956ad642dffe6aa387dce008f732ad7894`. In `.next` the compiled output contains exactly **one distinct** calendly string, `https://calendly.com/clipershq/30min`, in `.next/static/chunks/0g5mlmu.ef~yj.js` and `.next/server/chunks/ssr/src_app_preview_preview-landing_tsx_0s83qx4._.js`. `target="_blank"` and `rel="noopener noreferrer"` confirmed in the rendered DOM.
* **"Get started" keeps `/login` and same-tab navigation:** `getStartedHref` `/login`, `getStartedTarget` `null` at every width.
* **The signed-in hero is byte-identical.** No changed line in the diff mentions "Go to dashboard" (only context lines do), and the extracted `isLoggedIn ?` JSX block hashes to `a8069cbb4010c4d2edd5431ef0f87d6384669c30b014745b2ed65a1cbb5362a1` on both `origin/main` and the merged `HEAD`. No logged-in user sees the booking link.
* **Only three files changed** against main: `BACKLOG.md`, `docs/BL-699-CLIENT-CTA-LABEL.md`, `src/app/preview/preview-landing.tsx`. No logged-in surface, API, auth or data path touched.

## Accessibility review

**GO-WITH-NOTES.** Its one merge-blocking item was the conflict itself, that a naive resolution either drops BL-701's grid or orphans the `</>`; that is precisely how it was hand-resolved, and the build confirms it. Verified passing: accessible name computes to `Brands: book a call (opens in a new tab)` with the visible label at character 0, so **SC 2.5.3** passes on the stronger "starts with" test; the sr-only new-tab span survived and `.sr-only` is not overridden in `globals.css`; **SC 1.3.1** passes via the "available in text" disjunct because the sentence names both controls **by name**, never by position or colour; **SC 1.3.2** passes since DOM order equals visual order; **SC 2.4.4** passes and the author's structural claim is right, the `<p>` is a sibling not an ancestor so it is not programmatic link context and the label carries purpose alone. It explicitly warns **not** to cite SC 3.3.2 (no form control in the block) and recommends **not** adding `aria-describedby`, since iOS VoiceOver treats it as a hint that is commonly toggled off and it would replay a 12-word sentence on both controls. Focus rings, `forced-colors:`, `contrast-more:`, `min-h-[48px]`, `min-w-0 flex-1 basis-0`, `items-stretch` and `motion-safe:` are all intact; focus indicator measures 19.90:1 ring against offset in both themes. House rules pass: no dashes as bullets, no emoji in any UI string, `lucide-react` only, and the pinned literal is judged justified because the var **is** the defect and #09090b is what this hero already hardcodes.

**Follow-ups recorded, none merge-blocking:** (a) the `.light` contrast cluster on the untouched "Get started" button, its `hover:` and `contrast-more:` branches and its `border-white/80`, all one root cause fixable with a `--hero-scrim` token on `:root` plus validating the persisted theme value; (b) "Get started" carries no audience in its accessible name, so it reads as a bare generic name in a links list where the clarifying paragraph is unreachable; (c) the paragraph says "Book a call" while the control is "Brands: book a call", a near-miss rather than a clean match, and it should **not** be fixed by shortening the label back.

## Gates, honestly

`npm ci` **exit 0**, then `npx prisma generate` **exit 0** before any typecheck because `npm ci` wipes the generated client. `npx tsc --noEmit` **TSC_EXIT=0 with 0 output lines**. `npm run build` **BUILD_EXIT=0**, read from a log with the exit code echoed directly, never through a pipe. Prebuild: BYPASS detector **0 violations**, removed-fields **OK**, **hooks gate 0 errors / 11 warnings** (limit 11) with eslint **v9.39.4** confirmed present in the worktree so the gate ran rather than silently no-opping. 61/61 static pages.

## Safety

6 money files plus `tracking.ts`, `campaign-era.ts` and `campaign-rules.ts` **byte-identical by blob OID** on both refs: `clip-earnings-writer.ts` 7aa6be48, `earnings-calc.ts` 797e2098, `balance.ts` e887f80a, `tracking.ts` 847dcf70, `clip-earnings-invariant-middleware.ts` 61cef393, `money-decimal.ts` ef5cdae7, `campaign-era.ts` 106e16ad, `campaign-rules.ts` fc91216f. Also unchanged: `payouts/route.ts` a9c7164e, `auto-reject-flag.ts` a8ff0f7a, `payout-clamp-flag.ts` 2ca0a2a5, so neither `GLOBAL_PAYOUT_CLAMP_ENABLED` nor `RULES_AUTO_REJECT_LIVE` was flipped. No clip earnings or status changed, no payout touched, no DB write of any kind, no `prisma migrate`. No heredocs; one shell at a time. NO dashes.

**Rollback:** `git revert -m 1 55e757ce`, or `reset --hard pre-merge-BL-703`.
