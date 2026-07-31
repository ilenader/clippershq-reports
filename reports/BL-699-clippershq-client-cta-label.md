# BL-699 (ClippersHQ) — the client CTA now says who it is for, so a clipper does not book a sales call

## THE LABEL IS `Brands: book a call`, and it uses the platform's own second-person word rather than a new one. The a11y lead rejected my first proposal ("For brands") and prescribed exact strings; I applied them verbatim. Then a SECOND, INDEPENDENT lead reviewed the shipped result cold and caught a real defect the first missed: the plate I added inherited a CSS variable that is undefined on `:root`, so under the light theme its white text would have fallen to about **1.03:1**, a hard contrast failure on the one element whose entire job is to prevent the mis-click. I verified that claim myself before acting and fixed it. Both reviews are recorded below, including where the first one was wrong.

**2026-07-31 · SHIPPED to `checkpoint/BL-699` @ `aca6974e`, verified on origin (`origin/checkpoint/BL-699 == local HEAD`, `scripts/safe-push.mjs`).**
**Base** main `f7a1a344` · **Tags** `pre-BL-699` (f7a1a344) and `post-BL-699` (aca6974e), both pushed · **Worktree** `C:/b699`, short path, `node_modules` never junctioned.
**Rollback** `git revert aca6974e`, or `git reset --hard pre-BL-699`. Reverting restores the "Launch a campaign" label and the mis-click.

**Two files changed and nothing else:** `src/app/preview/preview-landing.tsx` and `BACKLOG.md`. The real `.tsx` diff is **135 insertions, 17 deletions**, so this is a code change, not a document.

---

## PART 1 — the platform's own word for these people is BRAND

Read from `public/brands.html`, the client-facing page. The question is not which word appears most, but which word the page uses to **address the reader in the second person**.

| line | text | verdict |
| --- | --- | --- |
| `:200` | "Full-service content clipping **for brands** and creators who refuse to be ignored" | addresses the reader |
| `:308`, `:437` | "**your brand**" | addresses the reader |
| `:352` | "Ready to become **the brand** everyone's talking about?" | addresses the reader |
| `:476` | "for **brands** that refuse to be ignored" | addresses the reader |
| `:213` | "Faces and **brands** you can't escape this month" | addresses the reader |

**"brand" appears 41 times, "client" 32.** But of those 32, **only two are prose**, and both are third person about-us framing (`:445` "Most clients see measurable reach increases..."); the other 30 are CSS identifiers (`clients-item`, `clients-arrow`, `clients-headline`) and a section id. **"business", "partner" and "advertiser" appear zero times.**

**So the word is BRAND, and it was not invented for this round.** The platform's own word for the action is also already there: `:354` and `:356` label the booking as a **"strategy call"**, and the section copy at `:353` reads "**Book a free 30-minute strategy call**".

**The clinching evidence is on the clipper page itself.** The hero paragraph directly above these buttons reads:

> "Pick a campaign, post clips on TikTok, Reels or Shorts, and get paid for the views you bring. **Brands** set the budget and the CPM, and you bring the audience."

So this very page already teaches the reader that a **campaign is what they pick** and **brands are the other party**. That is precisely why "Launch a campaign" failed, and precisely why "Brands" is the tightest available disqualifier.

---

## PART 2 — the label, and why a clipper will not click it

### What shipped

**Button label:**
```
Brands: book a call
```

**Supporting line, beneath both buttons, visible at every width:**
```
Book a call is for brands. Get started is for clippers.
```
rendered with the two button names in `font-semibold`:
```jsx
<span className="font-semibold">Book a call</span> is for brands. <span className="font-semibold">Get started</span> is for clippers.
```

### Why a clipper does not click it

The label opens with the exact token the paragraph above used to name the party that is **not** the reader. "Brands:" reads as vocative direct address, not a category, so it excludes rather than merely describes. And because the label leads with the audience, **the disqualifier is delivered in the accessible name itself, before activation**, which matters because the supporting line sits after the buttons in DOM order.

**No banned vocabulary.** The label contains none of `campaign`, `start`, `get started`, `launch`, `join`, `sign up`.

### Why "For brands" was rejected, which was not the reason I expected

I proposed "For brands". The lead rejected it **unanimously across four specialists**, and not for the reason I assumed. The not-for-me signal was judged fine, because the paragraph defines the term by explicit contrast one line above ("brands do X, and you do Y"). It failed on the other half:

> "It has no verb. It names an audience, never says what the control does, and never discloses that it leaves the site for a third-party scheduler. That is SC 2.4.4 and SC 2.4.6. 'For brands' is the shape of a nav section link, which on every SaaS site means an on-site marketing page."

It also corrected a premise I had relied on: **the link does not inherit that paragraph as programmatically determined link context.** The link sits in a sibling `<div>`, not inside the paragraph, so the AA "in context" escape hatch is structurally unavailable and the label has to carry the purpose essentially alone. The second lead independently confirmed this reading.

Also rejected: `Book a call` alone (zero not-for-me signal, reads as support onboarding), `Book a brand call` (invented compound, parses as a call *about* my brand), `For companies` (introduces a third word for the same party).

### Why the supporting line is worded that way

My draft was `"Want to clip and earn? Use Get started. Want clips made for your brand? Book a call."` It was rejected on three specific defects, all of which I accept:

1. **"your brand" had to go.** The possessive is exactly the self-applied creator form, so "clips made for your brand" is a question a clipper can answer *yes* to. It reintroduced the ambiguity the round exists to kill.
2. **"Use Get started" is not natural spoken English** and announces as "Use get started".
3. **The order was inverted against the DOM.** A screen reader user would hear client-then-clipper and then a sentence in the opposite order.

**Naming the buttons by name rather than by position is non-negotiable**, per both leads: "the button on the right" or "the blue one" is a direct **SC 1.3.3 Sensory Characteristics** failure, inverts under RTL, and decouples from DOM order under reflow.

---

## PART 3 — everything else from BL-694 is kept

| requirement | status | evidence |
| --- | --- | --- |
| Calendly URL byte-identical | **YES** | printed and compared below |
| opens in a new tab, correct rel | **YES** | `target="_blank"` and `rel="noopener noreferrer"` at lines 260 and 261 |
| both buttons same size, side by side | **YES** | both carry `flex-1 basis-0 min-w-0 min-h-[48px]`; row is `items-stretch` |
| client button visually dominant | **YES** | `bg-accent` (`--color-accent: #2596be`), unchanged |
| "Get started" secondary | **YES** | quieter bordered treatment, unchanged from BL-694 |
| "Get started" destination `/login`, same tab | **YES** | still `<Link href="/login">`, no `target` |
| signed-in hero byte-identical | **YES** | zero diff lines touch the `Go to dashboard` line |

### Reflow, re-verified from the CSS rather than assumed

Geometry inputs read from the code: hero container `px-5` (20px each side) with the sidebar `hidden ... lg:flex` so 0px below 1024px; row `gap-3` (12px); buttons `px-3` (12px each side) plus a 1px border each side.

| viewport | button width | text box | label behaviour |
| --- | --- | --- | --- |
| 320px | **134.0px** | 108px | wraps to 2 lines, `text-balance` breaks it as `Brands:` / `book a call` |
| 375px | **161.5px** | 135.5px | fits |
| 414px | **181.0px** | 155.0px | fits |

**The widths are unchanged from BL-694's measured 134/161.5/181** and cannot change with the label, because `flex-1 basis-0` fixes width independent of content. The longest single token is "Brands:" at roughly 48px, comfortably inside 108px, so nothing overflows.

**No truncation is structurally possible.** Verified on the button block with `grep -c`: `line-clamp` **0**, `truncate` **0**, `overflow-hidden` **0**, `whitespace-nowrap` **0**, fixed `h-[` **0**.

**Tap targets: 134 x 48+px**, clearing SC 2.5.8 AA (24x24) by more than 5x and SC 2.5.5 AAA (44x44) on both axes. `min-h-[48px]` is a floor and `items-stretch` raises the shorter button to match, so the two-line label grows the pill rather than clipping it.

The supporting line is **deliberately not gated behind `sm:`**. 320px is exactly where it is most load-bearing: the two pills are identical widths there, the arrow chip is hidden, and the labels are shortest. This audience is mobile-first, so hiding it would give mobile users less to go on than desktop.

---

## PART 4 — the evidence

### The Calendly URL, unchanged and byte-identical

```
=== SOURCE OF TRUTH: public/brands.html:354 ===
<a href="https://calendly.com/clipershq/30min" target="_blank" ... id="ctaBtn">

brands.html:354 -> [https://calendly.com/clipershq/30min]
landing page    -> [https://calendly.com/clipershq/30min]
RESULT: BYTE-IDENTICAL
```

**Verified a second time in the compiled bundle.** After `npm run build`, every Calendly URL the build emits:
```
      3 https://calendly.com/clipershq/30min
```
One distinct URL, three occurrences (SSR chunk, client chunk, source map). It was never re-typed: the string was left untouched in place.

### The new strings, in the compiled bundle

```
count of 'Brands: book a call' in .next: 3
count of 'is for clippers'     in .next: 3
```

The only remaining occurrence of `Launch a campaign` anywhere in the file is at **line 199, inside the correction comment** that records why it changed. It is not a rendered string.

### "Get started" and the signed-in hero

```
=== the Get started button as shipped ===
<Link
  href="/login"
  ...
  Get started
</Link>

=== signed-in branch: diff lines touching "Go to dashboard" ===
0
```

The only `Get started` line in the whole diff is the **new supporting copy**. The button's own line is untouched.

### Nothing outside the hero button row changed

```
files in the round diff: 2
BACKLOG.md
src/app/preview/preview-landing.tsx
```

| file | blob OID | verdict |
| --- | --- | --- |
| `src/app/globals.css` | `e8b55860` | IDENTICAL |
| `public/brands.html` | `4b61ecce` | IDENTICAL |
| `src/app/preview/preview-shell.tsx` | `338b8420` | IDENTICAL |
| `src/lib/clip-earnings-writer.ts` | `7aa6be48` | IDENTICAL |
| `src/lib/earnings-calc.ts` | `797e2098` | IDENTICAL |
| `src/lib/balance.ts` | `e887f80a` | IDENTICAL |
| `src/lib/tracking.ts` | `847dcf70` | IDENTICAL |
| `src/lib/clip-earnings-invariant-middleware.ts` | `61cef393` | IDENTICAL |
| `src/lib/money-decimal.ts` | `ef5cdae7` | IDENTICAL |
| `src/lib/campaign-era.ts` | `106e16ad` | IDENTICAL |

No logged-in surface, navigation, API, auth or data path was touched. Read-only DB check at **DB `now()` = 2026-07-31 11:03:39.16031+00**: 4,481 clips, **earnings invariant 0 violations**, 146 payout rows. No clip earnings or status changed and no payout was created, modified, approved or cancelled. No `prisma migrate`.

### The a11y review PASSES, and here is the full record including the disagreement

**Review 1 (prescriptive).** Four specialists ran. Ruling: **CHANGES REQUIRED**, with exact strings. I applied them verbatim. Asked to confirm the shipped result, it returned:

> **PASS — ship it. No defects.**

with an independently recomputed accessible name (`Brands: book a call (opens in a new tab)`), a recomputed plate contrast of **10.53:1**, confirmation that `<section>`'s `overflow-hidden` cannot clip because the only in-flow child defines the height, and confirmation that the fragment leaves focus order byte-identical.

**Review 2 (cold, independent).** A fresh lead reviewed the shipped file without seeing the first ruling. It returned **PASS on every question a through g** and then **CHANGES REQUIRED on one CSS defect the first lead missed**, which is exactly why a second cold review was worth running.

| question | ruling |
| --- | --- |
| a. SC 2.4.4 / 2.4.6 link purpose | **PASS**, clears 2.4.9 AAA for free "precisely because it draws on zero context" |
| b. SC 2.5.3 Label in Name, accessible name | **PASS**. `sr-only` is `position:absolute` + clip, so it is not pruned and does contribute; the arrow is excluded on two grounds, so the name is viewport-invariant |
| c. SC 1.3.3 Sensory Characteristics | **PASS** |
| d. SC 1.4.3 contrast on the plate | treatment right, **token wrong**, see below |
| e. SC 3.2.4 Consistent Identification | **my code comment was wrong**, see below |
| f. SC 1.4.10 reflow, SC 2.5.8/2.5.5 targets | **PASS**, "your math checks out" |
| g. focus and reading order | **PASS**, fragment emits no DOM node |

**The defect, verified by me before acting rather than taken on trust.** The plate inherited `var(--bg-primary,#09090b)` from the secondary button. I checked: **`--bg-primary` is never declared on `:root`.** It exists only inside `.dark` (`globals.css:34`, `#09090b`) and `.light` (`:114`, `#fafafa`). A CSS `var()` fallback fires only when a property is **undefined**, never when it is **redefined**, so the `#09090b` fallback is dead code. Under `.light` the plate would composite 78% `#fafafa` and white text on it falls to about **1.03:1**.

I also verified `.light` is reachable rather than theoretical. `theme-provider.tsx:26`:
```ts
const saved = localStorage.getItem("theme") as Theme | null;
if (saved) setTheme(saved);
```
An unvalidated cast that unconditionally restores a persisted `"light"`, even though the toggle itself was removed. Any browser that toggled light before that still lands there today, signed out.

**Fixed by pinning the literal on my own element**, holding the measured **10.49:1 in every theme**:
```
bg-[color-mix(in_srgb,#09090b_78%,transparent)]
```
`#09090b` is the value this hero already hardcodes throughout (`text-[#09090b]`, `ring-offset-[#09090b]`, `bg-[#09090b]/15`), so this matches the file rather than inventing a colour.

**Scope discipline, stated plainly.** The lead's preferred fix was a `--hero-scrim` token on `:root` plus changing the secondary button too. I did **not** do that, because this round is scoped to label and copy and `globals.css` is outside the hero button row. **The secondary button still carries the same dead fallback**, inherited from BL-694 and not a regression from this round. It is flagged in BACKLOG and in the code comment for a follow-up, along with validating the persisted theme value.

**A correction to my own code comment.** I had written that the duplicate `Launch a Campaign` label was an **SC 3.2.4** failure. The cold lead corrected this, and it is right: 3.2.4 reads "Components that have **the same functionality** ... are identified consistently", so it quantifies over same-function components and does **not** prohibit one label serving two functions. That is why repeated "Read more" links are handled under 2.4.4 and never 3.2.4. **The relabel was still correct**; the live defect was **SC 2.4.4** plus observed user harm. I corrected the comment in the same commit.

**Two claims from review 1 that I verified myself rather than trusting**, both of which held:
* `public/landing/css/sections.css:766` is `#book-call #ctaBtn { display: none !important; }`, with the comment "Hide the redundant Book a Strategy Call button, Calendly is the CTA". So the label at `brands.html:354` is CSS-hidden and was never a visible precedent. The **URL** provenance is still correct; the **label** precedent was not. I corrected that comment too.
* `Launch a Campaign` does exist at `public/clipper.html:540, 584, 729` and `src/app/clippers/page.tsx:39`, all pointing at `/brands`.

**Flagged, not fixed, and deliberately so.** Both leads agree the root cause is **dominance and tab order**, not wording: the client CTA is still `bg-accent` and first in tab order on a clipper acquisition page. Review 1 ruled this does not block, because the first token a keyboard user now hears is `Brands:`, which self-filters before activation. It deserves its own round where the swap can be measured. Also held: `ExternalLink` over `ArrowRight` (SC 3.2.5, AAA, and the chip is hidden below `sm` anyway) and expanding `CPM` (SC 3.1.4, AAA, advisory).

**One residual the reviewer named rather than hid:** the plate shares its fill and `backdrop-blur-sm` with the secondary button, so there is a theoretical affordance ambiguity about whether it reads as a third control. `rounded-xl` against the buttons' `rounded-full`, no border, no hover state and no focus ring were judged sufficient differentiation. Logged as a known tradeoff, not a defect.

---

## Build gates, stated honestly

| step | result |
| --- | --- |
| `npm ci` | **exit 0** (wipes the generated Prisma client) |
| `npx prisma generate` | **exit 0**, run **before** tsc |
| `npx tsc --noEmit` | **exit 0**, **0 output lines** |
| `npx eslint --version` | **v9.39.4 present**, so the hooks gate is real and not a silent no-op |
| `npm run build` | **BUILD_EXIT=0**, echoed from a captured log, never piped through `tail` |
| `check:prisma-bypass` | **0 violations** |
| `check:removed-fields` | **OK** |
| `lint:hooks` | **11 problems (0 errors, 11 warnings)**, at the ≤11 cap, no new warning added |
| static pages | **61/61** |

Both `tsc` and `next build` were actually run, and re-run after the contrast fix; neither was trusted alone. **No heredoc was used anywhere in this round** and shells ran strictly one at a time. Every count comes from `grep -c`.

---

## Safety

Label and supporting copy only, plus the one-token contrast fix on the element this round added. The Calendly URL was left in place and never re-typed, and is byte-identical to `public/brands.html:354` by string comparison and in the compiled bundle. "Get started" keeps `/login` and its same-tab client-side navigation. The signed-in hero is byte-identical, so no logged-in user ever sees the booking link. Nothing outside the landing hero button row changed: `globals.css`, `brands.html` and `preview-shell.tsx` are byte-identical, and no logged-in surface, navigation, API, auth or data path was touched. The label uses none of `campaign`, `start`, `launch`, `join` or `sign up`. The 6 money files plus `tracking.ts` and `campaign-era.ts` are byte-identical by blob OID on both tagged refs. No clip's earnings or status changed, no payout was touched, and no `prisma migrate` was run. **The accessibility review PASSES rather than defers**, and where the two reviews disagreed the disagreement is recorded above with the claims verified independently. NO dashes used as bullets.
