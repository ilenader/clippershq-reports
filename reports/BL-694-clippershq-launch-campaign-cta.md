# BL-694 (ClippersHQ) — a "Launch a campaign" CTA on the signed-out landing hero

## THE BOOKING LINK EXISTS AND I FOUND IT, BUT NOT WHERE A SEARCH WOULD LOOK. `grep -rn "calendly" src/` returns **nothing**, because `src/app/brands/page.tsx` is a 28-line shell that **iframes the static `public/brands.html`**. The real link lives at **`public/brands.html:354`** and is `https://calendly.com/clipershq/30min`. It is the **only distinct Calendly booking URL in the entire repo**, so there was nothing to disambiguate and no STOP was needed. Anyone auditing only `src/` would wrongly conclude the platform has no booking link at all.

**2026-07-31 · SHIPPED to `checkpoint/BL-694` @ `7f917997`, verified on origin.** Base main `46115e32`. Tags `pre-BL-694` / `post-BL-694`. **Exactly one source file changed.**

---

## ONE THING NEEDS YOUR DECISION, and it is a one-line change either way

The accessibility lead will not sign off on the hero as specified, and its reasoning is worth a minute of your time because it is about whether a clipper misreads the button.

**The problem.** The hero's headline and subline are 100% clipper copy, and the subline literally says *"Pick a campaign, post clips..."*. So the word "campaign" is already defined on that screen as **the thing a clipper picks**. Put "Launch a campaign" next to it as the loudest control and a clipper can read it as escalated clipper functionality rather than a brand sales call. On mobile this is measurably worse, because the "Get paid per view" eyebrow is hidden below 640px, so the only corrective context left is 13px text over a photograph.

**Its two fixes, either of which resolves it. Both change something you specified explicitly, so I did neither and am bringing them to you:**

1. **Point "Launch a campaign" at `/brands` instead of Calendly.** Your clients page already embeds the same Calendly widget, so the booking still happens, one honest page later. This also matches the platform's own existing vocabulary: `src/app/clippers/page.tsx:39` already has `<a href="/brands">Launch a Campaign</a>`, the exact phrase pointing at that exact destination.
2. **Or keep Calendly and rename the secondary from "Get started" to "Start clipping"**, matching `clippers/page.tsx:38` verbatim. Costs zero pixels and makes both audiences self-evident.

**I shipped neither** because you specified the Calendly destination explicitly and named the second button "Get started", and overriding either silently would be the wrong call. Everything else the lead asked for **is** applied.

---

## PART 1 — the link, and the proof it is the right one

| where | line | value |
|---|---|---|
| **clients page, primary CTA** | **`public/brands.html:354`** | `https://calendly.com/clipershq/30min` |
| clients page, inline widget | `public/brands.html:356` | same URL plus display params |
| clients page, footer "Contact" | `public/brands.html:469` | same URL |
| clipper page | `public/clipper.html:744` | same URL |
| **the new landing button** | `src/app/preview/preview-landing.tsx` | `https://calendly.com/clipershq/30min` |

```
=== distinct booking URLs repo-wide (must be exactly 1) ===
https://calendly.com/clipershq/30min

landing  src/app/preview/preview-landing.tsx : https://calendly.com/clipershq/30min
clients  public/brands.html:354              : https://calendly.com/clipershq/30min
BYTE-IDENTICAL ✓
```

The only other `calendly.com` string in the repo is `https://assets.calendly.com/assets/external/widget.js`, the embed script. That is an asset, not a destination, so the booking URL is unambiguous. Note the domain is `clipershq` with **one p**, matching the house rule, which is a further sign it is the genuine link rather than something typed from memory.

**Not hoisted into a shared constant, deliberately.** The other three uses are in **static HTML**, which cannot import a TypeScript module. A constant would therefore have exactly one consumer and would *hide* the provenance rather than share it. It is inlined with a comment naming `brands.html:354` as the source of truth, which is the thing a future reader actually needs.

---

## PART 2 — the two buttons

**Dominant, "Launch a campaign".** `bg-accent`, derived from the brand token **`--color-accent: #2596be`** at `src/app/globals.css:4` inside Tailwind v4's `@theme inline` block. No hex was guessed. Ink is the app's established `#09090b` dark-on-accent pair, measured by the lead at **5.86:1**. It carries the glow, the hover lift and the arrow chip. External, so `target="_blank" rel="noopener noreferrer"`.

**Secondary, "Get started".** Same `/login` destination, same behaviour, quieter styling only: an outlined pill with a dark translucent fill over the photo. Still obviously clickable, and nothing about it reads as disabled.

**Identical size by construction, not by luck.** Both are `flex-1 basis-0 min-w-0` inside `items-stretch`, so each lands on exactly `(container − gap) / 2` regardless of label length, and both share a height even when the longer label wraps.

**The blue only, no second accent.** One accent colour, per the house rule.

---

## PART 3 — mobile, computed

Side by side at **every** width. **Not stacked**, and the reason changed during the round: I first planned to stack below 640px because the hero is a deliberately short `min-h-[28vh]` band (BL-396 cut it from 42vh at your request). The lead measured the rendered box and corrected me: the content already exceeds that floor, the section has no fixed height, so stacking would not clip anything, it would simply grow the hero by about 18%. It then endorsed side by side for a better reason: two equal-width buttons read as *"two paths, pick the one that is you"*, whereas a stacked pair reads as *"do this, or failing that, do that"*, which is the exact misleading dominance the label question is about.

Container `px-5` (40px), row `gap-3` (12px), so each button is `(W − 52) / 2`:

| viewport | width per button | height | verdict |
|---|---|---|---|
| **320px** | **134px** | 48px, or ~52px if the longer label wraps to two lines | fits, no overflow |
| **375px** | **161.5px** | 48px | comfortable |
| **414px** | **181px** | 48px | comfortable |

**`min-w-0` is the class doing the real work.** A flex item defaults to `min-width: auto` and cannot shrink below its min-content width, so without it the row would exceed 280px at 320px and produce horizontal scroll (SC 1.4.10 Reflow). With it, both land on the computed width and the label wraps instead.

**Tap targets:** 134x48 at the narrowest clears SC 2.5.8 Minimum (24x24) by over five times and SC 2.5.5 Enhanced (44x44) comfortably. `gap-3` rather than `gap-2` on the lead's advice, because two adjacent thumb targets where one mis-tap throws you off-site into a new tab are worth the extra 4px.

**Wrapping is accepted, not fought.** At 320px "Launch a campaign" needs about 139px against 134px available, so it wraps to two lines. `min-h-[48px]` plus `leading-tight` plus `items-stretch` absorbs that, and `text-balance` makes it break as "Launch a / campaign" rather than orphaning a word. I did **not** drop to `text-xs`: BL-393 deliberately raised mobile text to 13px for legibility and an interactive label should not be smaller than the body copy around it. No `whitespace-nowrap`, no `truncate`, no fixed `h-12`, all of which would break SC 1.4.12 Text Spacing.

**Honest limit:** these widths are computed from the shipped classes and the container padding, deterministically. **I did not render them in a browser.** The arithmetic is exact because `flex-1 basis-0 min-w-0` forces the widths; the only variable is how many lines the label wraps to, which `min-h` and `items-stretch` absorb by design.

---

## PART 4 — every file touched

**One.** `src/app/preview/preview-landing.tsx`, the hero button row.

```
$ git diff --name-only pre-BL-694
src/app/preview/preview-landing.tsx
```

Nothing else. No other page, no navigation, no logged-in surface, no API, auth or data path, no component library. **`globals.css` is byte-identical (`e8b55860`)**: the lead recommended adding a `--bg-on-photo` token there, and I implemented the same value as the single-file `color-mix(in_srgb,var(--bg-primary,#09090b)_78%,transparent)` form precisely so this round would stay in one file, as you asked.

**A logged-in user's hero is byte-identical to before.** The client CTA renders only when signed out, so the signed-in branch keeps the same single "Go to dashboard" button with the same classes. This is both what you asked for ("signed-out landing page") and the lead's SHOULD-FIX 8, which warned that an authenticated clipper would otherwise get an off-site sales booking as their dominant, first-in-tab-order action.

---

## PART 5 — evidence

| claim | evidence |
|---|---|
| Calendly URL byte-identical to the clients page | `BYTE-IDENTICAL ✓`, both file:line above; exactly **1** distinct booking URL repo-wide |
| side by side, equal size | `flex-1 basis-0 min-w-0` + `items-stretch`, all four compiled into the bundle |
| new button dominant | `bg-accent` from the token, ink at 5.86:1, glow + chip; secondary is outlined |
| opens in a new tab correctly | `target="_blank" rel="noopener noreferrer"` plus an `sr-only` " (opens in a new tab)" |
| "Get started" unchanged | still `<Link href="/login">`, destination and behaviour untouched |
| reflow at 320 / 375 / 414 | 134px / 161.5px / 181px per button, no overflow |
| nothing else changed | one file in `git diff --name-only`; `globals.css` byte-identical |

**The critical utilities really compiled** (checked in the emitted CSS bundle, not assumed):

```
.min-w-0          -> min-width:calc(var(--spacing) * 0)
.flex-1           -> flex:1
.basis-0          -> flex-basis:calc(var(--spacing) * 0)
.items-stretch    -> align-items:stretch
.text-balance     -> text-wrap:balance
.border-white/80  -> border-color:#fffc
color-mix(in srgb,var(--bg-primary,#09090b) 78%,transparent)
border-color:var(--color-accent)
min-height:48px   ·   forced-colors ×3   ·   contrast-more ×3
```

---

## The accessibility review, and what it changed

**It ran before any UI was written**, and it materially changed what shipped. Six of its seven must-fixes are applied.

**It killed my first secondary button outright.** I proposed `border-white/70 bg-black/40 text-white`. It swept all 256 luminances plus 4,000 random colours and found that over a white photo pixel the white label composites to **2.85:1** against a 4.5:1 bar, and that an adversarial mid-grey around `#707070` sits between a light border and a dark fill and defeats **both at once** at **2.21:1**. Shipped instead: a **78%** fill, worst case **10.49:1**, with `border-white/80` holding **3.30:1** on one edge against any possible pixel.

Also applied on its instruction:

* **`min-w-0`** on both, without which 320px overflows (SC 1.4.10).
* **The arrow chip moved to the primary and hidden below `sm`.** At 320px the chip plus its gap would eat 36px of a 134px button. Keeping it on the demoted button would also have inverted the hierarchy, since a directional chip is a strong affordance.
* **`sr-only` span, not `aria-label`,** for the new-tab warning, matching `preview-shell.tsx:90` exactly (leading space, no trailing space). This keeps the visible text leading the accessible name, so SC 2.5.3 Label in Name passes structurally rather than by manual duplication.
* **`ring-white` instead of `ring-white/90`.** The 10% transparency made the ring's rendered colour photo-dependent for no benefit.
* **`border-accent` on the primary and `forced-colors:` outlines on both.** In Tailwind **v4** `outline-none` emits `outline-style: none`, unlike v3 which emitted a transparent outline that Windows High Contrast forced visible. Combined with a box-shadow ring that forced-colors suppresses, a keyboard user in a contrast theme could have had **no focus indicator at all**.
* **`contrast-more:` opaque fallbacks** on the translucent secondary.
* **The `var()` fallback inside `color-mix` is load-bearing**, not decoration: `--bg-primary` lives in the `.dark` block rather than `:root`, and an invalid var inside a `/` modifier invalidates the entire declaration, which would drop the fill to transparent and leave white text on the bare photo at 1.00:1.

**It also corrected two of my own premises**, which is worth recording: the 28vh floor is already exceeded so stacking would not have clipped anything, and the existing button is already 48px tall on mobile, so `min-h-[48px]` is a no-op on it and does real work only on the new button.

**The one it will not sign off on is the label question at the top of this report**, which is yours to decide. It was explicit that it did not want this papered over in `sr-only` text, since that would make the link more honest to blind users than to sighted ones.

Two things it flagged as **outside this round**: the BL-380 headline text-shadow remains an unmeasurable contrast exception (these buttons will now be more legible than the headline above them, which is the right ordering but does not repair the headline), and "CPM" is never expanded in copy aimed at a new clipper.

---

## Gates, stated honestly

* **`npm ci` exit 0**, then **`npx prisma generate` exit 0**, in that order and before typecheck.
* **`npx tsc --noEmit` exit 0**, **0 lines** of output.
* **`npm run build` BUILD_EXIT=0**, read from a captured log and echoed directly, never piped through `tail`. BYPASS detector **0 violations**, `check:removed-fields` OK, `lint:hooks` **11 problems (0 errors, 11 warnings)** at the ≤11 cap, compiled successfully, **61/61** pages.
* **eslint v9.39.4 present**, so the hooks gate is real.
* The real `.tsx` diff is non-empty and quoted throughout. Counts by `grep -c`, never `head`.
* **6 money files + `tracking.ts` + `campaign-era.ts` byte-identical by blob OID:** writer `7aa6be48`, earnings-calc `797e2098`, balance `e887f80a`, tracking `847dcf70`, middleware `61cef393`, money-decimal `ef5cdae7`, campaign-era `106e16ad`. No clip earnings or status touched; no API, auth or data path in the diff.
* **NO dashes** as bullets. Isolated worktree at the short path `C:/b694`, `node_modules` never junctioned. Nothing held by BL-693 was touched.
* **A note on the design skill:** the brief named `/mnt/skills/public/frontend-design/SKILL.md`, which **does not exist on this machine**. I used the project's installed `design-taste-frontend` skill instead, plus the house rules in CLAUDE.md, and I am stating the substitution rather than claiming to have read a file I could not open.

**Rollback:** `git revert 7f917997`, or `reset --hard pre-BL-694`.
