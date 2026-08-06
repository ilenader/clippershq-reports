# BL-725 — The public site now shows its legal links

**Both linked pages render. Nothing is broken.** `/terms.html`, `/privacy.html` and `/cookies.html`
each return HTTP 200 with a non-empty `<h1>`, live and locally. The blocker was never a missing page.
It was that nothing on the public landing pointed at them.

**2026-08-06 · Base:** `main @ de0169bd` · **Branch:** `checkpoint/BL-725`
**One file changed. 68 lines added, 0 removed. No API, auth, money or data path touched.**

---

# PART 1 — THE REAL PATHS, VERIFIED NOT ASSUMED

## 1.1 The three pages, file:line and live status

| Page | Source file | Live URL | Live HTTP | `<h1>` measured |
|---|---|---|---|---|
| Terms of Service | `public/terms.html:26` | `https://clipershq.com/terms.html` | **200** (4,893 B) | "Terms of Service" |
| Privacy Policy | `public/privacy.html:26` | `https://clipershq.com/privacy.html` | **200** (3,737 B) | "Privacy Policy" |
| Cookie Policy | `public/cookies.html:25` | `https://clipershq.com/cookies.html` | **200** (2,538 B) | "Cookie Policy" |

All three were also served from the local production build at `http://localhost:3725/` and returned
**200**, `text/html; charset=UTF-8`, one `<h1>` each, `<html lang="en">`, and a clean h1-then-h2 outline
with no skipped levels. The sha256 of each served body matched the file on disk, so these are the real
static files and not a Next fallback.

**They are static files in `public/`, not Next routes.** That is why the footer uses plain `<a href>`
rather than `next/link`: a Link would prefetch an RSC payload that does not exist.

## 1.2 What the bare domain actually does

`src/app/page.tsx:88` redirects a logged-out visitor from `/` to `/preview`. Measured: `https://clipershq.com/`
and `https://clipershq.com/preview` return **byte-identical 179,267-byte** responses. So the page a TikTok
reviewer opens is `/preview`, and before this round it carried no legal links of any kind.

The footer that does have all three links lives in `public/clipper.html:746` and is reached only through
the iframe on `/clippers`. A reviewer typing the bare domain never saw it.

## 1.3 The live privacy page is the OLD version. State this to yourself before you submit.

BL-724 corrected the privacy policy on `checkpoint/BL-724`, and **that branch is not merged.** `origin/main`
is still `de0169bd` (BL-720). Measured against the live page right now:

| Check | Live `clipershq.com/privacy.html` |
|---|---|
| "Apify" | **present** (1 occurrence) |
| "Vercel" | **present** (1 occurrence) |
| "Railway" | absent (0) |
| "HikerAPI" | absent (0) |
| "Connecting Your TikTok Account" | absent (0) |
| Last updated | **"April 2026"** |

**So today this footer links a TikTok reviewer straight at a policy that names two processors the platform
no longer uses and does not disclose the TikTok integration at all.** That is worse than not linking it,
and it is the reason BL-724 must merge before or with this round. Both are listed in the checklist below.

---

# PART 2 — THE FOOTER

## 2.1 What was added

`src/app/preview/preview-landing.tsx:459-468`, rendered as the last child inside the shell's
`<main id="main">`, as a sibling **after** the `space-y-10` content block rather than inside it (inside,
that block's `space-y-*` sets `margin-top` on every non-first child and would collide with any margin the
footer set, resolving by stylesheet order rather than intent; as a sibling the wrapper's own
`py-8 sm:py-10` already owns the gap, so the footer carries no top margin):

```tsx
{!isLoggedIn && (
  <footer className="border-t border-[var(--border-color)] bg-[var(--bg-secondary)] px-5 py-6 sm:px-8 sm:py-8 lg:px-10">
    <ul role="list" className="flex flex-wrap items-center gap-x-6 gap-y-2">
      <li><a href="/terms.html" className={LEGAL_LINK}>Terms of Service</a></li>
      <li><a href="/privacy.html" className={LEGAL_LINK}>Privacy Policy</a></li>
      <li><a href="/cookies.html" className={LEGAL_LINK}>Cookie Policy</a></li>
    </ul>
    <p className="mt-2 text-sm text-[var(--text-muted)]">© 2026 Clippers HQ</p>
  </footer>
)}
```

plus the shared class constant at `:93-94`, hoisted next to the other module constants to match the
`NAV_ITEM_BASE` house style in `preview-shell.tsx`.

## 2.2 The labels are deliberately boring

"Terms of Service", "Privacy Policy", "Cookie Policy". No clever wording, because a reviewer scans for
exactly those words. Each string matches its destination page's own `<h1>` verbatim, and
`src/app/login/page.tsx:335,337` already uses the same two strings for the same two destinations, so the
site is now self-consistent rather than merely correct here.

No dashes as bullets, no emoji, no icons. The links are a real `<ul>`, not a dash-separated line.

## 2.3 Design language

Every value is an existing token, no hex was written: `--border-color`, `--bg-secondary`,
`--text-secondary`, `--text-muted`, and the `accent` focus ring. It reads as the same surface as the
header banner directly above it, which uses the identical `bg-[var(--bg-secondary)]` +
`border-[var(--border-color)]` pair (`preview-shell.tsx:160`). Horizontal padding steps
`px-5 sm:px-8 lg:px-10`, matching the hero at `preview-landing.tsx:133` exactly, so the links line up with
the hero copy and the campaign row titles at every breakpoint.

The frontend-design skill's own rule decided the approach: this is an established product with a locked
system, so the discipline that applies is content and token fidelity to the existing anchor, not the
selection of a new one. Adding a fresh aesthetic to one footer inside a live product is the hybridising
the skill calls a category error. Its §2 content rules are what shaped the copy: no filler labels, no
themed replacement for standard UI copy, no unicode glyphs as icons.

## 2.4 One measured design decision worth stating

Hover is `text-primary`, **not** the brand accent, and that is not taste. `#2596be` on the light theme's
`--bg-secondary` (`#f4f4f5`) measures **3.12:1** against the 4.5:1 that 14px `font-medium` text requires
(`--color-accent-hover` `#1e7ea3` is no better, at 4.18:1). The light theme is genuinely reachable here:
`theme-provider.tsx:26-36` restores the class from `localStorage` on every route, so a visitor who chose
light while signed in still has it after signing out. The underline does not rescue it, because that
satisfies SC 1.4.1, a different criterion from SC 1.4.3.

Consequence, stated plainly: in the dark theme `--text-secondary` and `--text-primary` are both `#ffffff`,
so hover feedback there is the underline thickness alone.

---

# PART 3 — WHAT WAS NOT TOUCHED

## 3.1 Every file changed

**One:** `src/app/preview/preview-landing.tsx`.

`git diff --stat` against `origin/main`: `1 file changed, 71 insertions(+)`. Counting only real content
lines (excluding diff headers): **68 added, 0 removed.** It is a pure addition, and `0 removed` is the
proof that nothing above it was rewritten.

## 3.2 Exactly two hunks

```
@@ -49,0 +50,46 @@ const HERO_IMAGE = "/preview-hero.jpg";
@@ -397,0 +444,25 @@ export function PreviewLanding({
```

The first inserts the comment block and `LEGAL_LINK` **before** the `Hero` function begins. The second
inserts the footer at the end of `PreviewLanding`. The entire `Hero` function, which owns the headline,
the image, both CTA buttons and BL-701's `lg:grid lg:w-fit` width constraint, is inside neither hunk.

Filtering the added lines down to executable code leaves exactly two things: the `LEGAL_LINK` string, and
the `{!isLoggedIn && (<footer>…</footer>)}` block. Everything else added is comment.

## 3.3 The hero and the CTAs, verified in the rendered output

Fetched from the running production build at `/preview`:

| Thing | Occurrences | Status |
|---|---|---|
| `Brands: book a call` (BL-699 label) | 1 | unchanged |
| `Get started` (clipper CTA label) | 1 | unchanged |
| `https://calendly.com/clipershq/30min` | 1 | **byte-identical**, still `target="_blank"` + `rel="noopener noreferrer"` |
| `Go to dashboard` (signed-in CTA) | 0 | correct: this render is signed out |

BL-701's desktop width constraint is untouched because its markup was never in the diff.

## 3.4 Signed-in surfaces are byte-identical, by construction

The footer is wrapped in `{!isLoggedIn && …}`. A signed-in user renders the identical React tree they
rendered before, because the only added executable code is inside that guard and the only other addition
is an unreferenced-when-false string constant.

This follows the precedent BL-694 set on the hero fifteen lines above: *"Signed OUT gets both; signed IN is
deliberately left BYTE-IDENTICAL to before."* A TikTok reviewer is signed out, so the footer is present for
exactly the visitor it exists for.

**Nothing else on any signed-in surface was opened, let alone edited.** `preview-shell.tsx` was read and
deliberately NOT modified, because it is shared with the other preview routes and with a parallel round.

---

# PART 4 — THE EVIDENCE

All of the following is **measured** against a real production build (`npm run build`, then `next start`),
served at `http://localhost:3725/preview` signed out, driven by Chromium 148.0.7778.96 via Playwright
1.60.0 with axe-core 4.11.1. Not inferred from source.

## 4.1 The footer renders, with both required links

Server-rendered HTML from `/preview`, counted with `grep -c`:

```
Terms of Service => 1      /terms.html   => 1
Privacy Policy   => 1      /privacy.html => 1
Cookie Policy    => 1      /cookies.html => 1
<footer          => 1      role="list"   => 2
```

The browser confirms the same: exactly **one** `<footer>` on the page at every viewport, and the ARIA
snapshot reads `list > listitem > link "Terms of Service" (/url: /terms.html)` for all three.

## 4.2 Layout at all five widths

| Viewport | Footer w x h | Footer left | Link lines | `documentElement.scrollWidth` | Horizontal overflow |
|---|---|---|---|---|---|
| **320** | 320 x 173 | 0 | 2 | 320 | none |
| **375** | 375 x 173 | 0 | 2 | 375 | none |
| **414** | 414 x 121 | 0 | 1 | 414 | none |
| **1280** | 1040 x 137 | 240 | 1 | 1280 | none |
| **1440** | 1200 x 137 | 240 | 1 | 1440 | none |

The 240px left offset at 1280 and 1440 is the shell's `w-60` sidebar, so the footer aligns with the content
column rather than sitting under the nav.

At 320 and 375 the links wrap to "Terms of Service + Privacy Policy" on line one and "Cookie Policy" on
line two, with a measured **8px** vertical gap and `intersects: false` for all three pairs, so wrapped
targets never touch. At 414 and above all three fit on one line (Cookie Policy's right edge at 356.69px,
inside the 394px content edge).

## 4.3 Tap targets

Identical at every width, because the font never changes:

| Link | Measured box | SC 2.5.8 (AA, 24x24) | SC 2.5.5 (AAA, 44x44) |
|---|---|---|---|
| Terms of Service | **109.27 x 44** | pass | pass |
| Privacy Policy | **91.13 x 44** | pass | pass |
| Cookie Policy | **88.30 x 44** | pass | pass |

Computed `min-height: 44px` with `display: inline-flex` — the declared 44px is genuinely taking effect on
the hit-tested border box, at 320, 375, 414, 1280 and 1440.

## 4.4 Contrast, as actually served

| Element | Computed colour | Ratio vs footer background | Verdict |
|---|---|---|---|
| Footer background | `rgb(15, 15, 17)` (`--bg-secondary`) | — | resolved on the footer, not inherited |
| All three links | `rgb(255, 255, 255)` | **19.15:1** | pass (4.5:1 required) |
| Copyright line | `rgb(255, 255, 255)` | **19.15:1** | pass |

Recomputed by hand from the sRGB relative-luminance formula and matching to three decimals.

## 4.5 axe-core: zero violations

Scoped to the `footer` element: **0 violations, 8 passes, 0 incomplete.** Specifically checked and clear:
`landmark-contentinfo-is-top-level` (inapplicable), `landmark-unique` (inapplicable scoped, passes
page-wide), `list` (inapplicable), `listitem` (**passes**), `link-name` (**passes**), `color-contrast`
(inapplicable scoped, passes page-wide), `region` (passes page-wide), plus
`landmark-no-duplicate-contentinfo`, `aria-allowed-role`, `aria-required-children`, `aria-roles`.

`listitem` passing is the proof the `role="list"` workaround actually works rather than merely being
present: that rule only passes when the parent's computed role really is `list`. It is needed because
Tailwind Preflight sets `list-style: none`, and WebKit strips list semantics from such lists.

## 4.6 Keyboard

29 tab stops on the page. The three footer links are presses **26, 27 and 28**, in DOM order, all
`insideFooter: true`. Press 25 is the last campaign card link, so the handoff from the campaign rail into
the footer is clean with nothing skipped. Press 29 leaves the document.

The skip link still works and is not a hash-only jump: one Tab focuses `<a href="#main">Skip to main
content</a>`, and after activation `document.activeElement` is `MAIN#main` with `scrollY` 64.

## 4.7 Build

* `eslint` present and really running: `npx eslint --version` → **v9.39.4**. The hooks gate is not silently no-opping.
* `npm ci` → exit **0**; `npx prisma generate` re-run afterwards → exit **0**, before typecheck.
* `npx tsc --noEmit` → exit **0**, `grep -c "error TS"` = **0**.
* `npm run build` → **BUILD_EXIT=0**, read from `$?` written to a log, never piped through `tail`. One `Compiled successfully`. Zero `error TS` / `Failed to compile`.
* **BL-348 hooks gate: `11 problems (0 errors, 11 warnings)`** against `--max-warnings 11`. It passes, and it passes **at the limit** — all 11 are pre-existing `react-hooks/exhaustive-deps` warnings in files this round did not touch. Stated because one new warning from any round breaks the gate.
* The diff is non-empty and real: `1 file changed, 71 insertions(+)`, hunks quoted in 3.2. This is a code change, not a document.

## 4.8 Money safety

Blob OID on `origin/main` compared against `HEAD` on `checkpoint/BL-725`. All seven identical:

| File | Blob OID on both refs |
|---|---|
| `src/lib/clip-earnings-writer.ts` | `ac5be7deb061768fec800aa89aae512a56a9e065` |
| `src/lib/earnings-calc.ts` | `797e20985ad57475ef321afcf3cb1ea7b0d6ab84` |
| `src/lib/balance.ts` | `e887f80acfc70fee438e719a32a60025eda22749` |
| `src/lib/tracking.ts` | `83ce4babfd39a6261114465639f2eac4e23bfceb` |
| `src/lib/clip-earnings-invariant-middleware.ts` | `61cef39395363c31f0c902dd4c64e8c06b3e6449` |
| `src/lib/money-decimal.ts` | `ef5cdae757b9ad3c23380ee8b63e279f98d0b6ac` |
| `src/lib/campaign-era.ts` | `106e16ad75125c3b10b6949a2981d33614c69ab9` |

No schema change, no `prisma migrate`, no DB write, no API/auth/data path touched. No clip's earnings,
status or payout changed. The round wrote no database query of any kind.

## 4.9 What was NOT measured, said rather than papered over

* **Page-level SC 1.4.10 is not fully proven.** `<main>` is `overflow-y-auto`, which makes its computed `overflow-x` `auto` too, so `main` rather than the document is the horizontal scroll container, and `documentElement.scrollWidth` cannot see inside it. `main.scrollWidth` was not captured. The **footer-scoped** result stands on its own: at 320 the footer is exactly 320 wide and its widest link right edge is 244.39, so the footer contributes zero overflow. The five elements the scan found extending past 320 are all campaign-carousel children inside a deliberate horizontal scroller, and none are in the footer.
* **The light theme was measured only by calculation, not in a browser.** The run was the default dark theme as served. The 3.12:1 figure in 2.4 that drove the hover decision is a computed ratio, not an observed one.
* **Hover and focus-visible states were not measured**, only the resting state.
* **My own Chrome could not reach `localhost`** (curl could, at HTTP 200 in 0.35s), so all browser measurement above came through the Playwright path instead. Three attempts across two tabs and both `localhost` and `127.0.0.1` returned `chrome-error://chromewebdata/`; rather than loop on it, the measurement was rerouted. The numbers are real; the tool that produced them is not the one first attempted.

## 4.10 Found while measuring, REPORTED not fixed

* **`meta-viewport`, moderate, SC 1.4.4 Resize Text.** The one axe violation on the unscoped page: a viewport that blocks or caps user zoom. Pre-existing, not in the footer, but it degrades the footer along with everything else for anyone who zooms. Its own ticket.
* **`--bg-page` is undefined.** It resolves to the empty string on both `documentElement` and the footer and does not appear in `globals.css`, yet `CLAUDE.md` lists it as canonical. The footer does not use it, so no impact here, but any surface that writes `bg-[var(--bg-page)]` is getting no background at all.
* **No `contentinfo` landmark exists on the page.** The footer's computed role is `sectionfooter`, because a `<footer>` inside `<main>` maps to generic. This is the correct call given `preview-shell.tsx` could not be modified, and forcing `role="contentinfo"` would trip axe's `landmark-contentinfo-is-top-level` and land screen reader users mid-document, since NVDA's and JAWS's landmark lists are flat. Residual cost, stated plainly: the legal links cannot be reached by landmark jump. They are reachable by Tab (presses 26 to 28) and by list navigation. The only fix is moving the footer out of `<main>`, which is a shell change and belongs to a round that owns the shell.

---

# WHAT TO DO NEXT

1. **[BUILD] Merge BL-724 as well as this round.** Per 1.3, the live privacy policy is still the April 2026 version naming Apify and Vercel and disclosing no TikTok integration. This footer points a reviewer directly at it. Merging this round alone makes the wrong document easier to find.
2. **[BUILD] Merge and deploy BL-725.** Then confirm the footer on the real `https://clipershq.com/` while signed out.
3. **[YOU] Register the Website URL as `https://clipershq.com`** in the TikTok developer portal. Option A from BL-724 §2.7 is now available, so the weaker iframe fallback (`/clippers`) is no longer needed.
4. **[YOU] Verify the domain** and register the Terms of Service and Privacy Policy URLs, per BL-724 §2.5.

**Rollback:** `git revert -m 1 <merge>`. The footer disappears and `preview-landing.tsx` returns to its
`origin/main` blob. Nothing else moves, because nothing else changed.
