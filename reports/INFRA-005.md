# INFRA-005 — The dashboard frontend is built. **No backend exists yet, so what ships today is the placeholder path** — and that turned out to be the honest half worth getting right. 43 browser assertions pass. Two accessibility conflicts are yours to decide, not mine

**Date:** 2026-08-01 · **Type:** Implementation · **Spend:** **$0.0000 · 0 paid calls · 0 network requests**
`dashboard/static/{index.html,app.css,app.js}`. No backend file, no `clippershq` module touched. Claim filed via `tools/claim.py` and cleared. Committed as **`c44e6f1`** and **`fa7e257`**.

---

## What was built

The mockup, not a reinterpretation of it: **6 tabs, one visible · 10 collapsible sections · four idle funnels behind a single line · "412 / leads", never a sentence.** System font stack, no icon font, no images, and **zero external requests — asserted in the test**, not assumed. Both surviving paragraphs are intact and no third was added.

**Coded against the fixed contract** — `/api/now`, `/api/spend`, `/api/history`, `/api/files`, `/api/settings`, `/api/start`. I changed nothing about it.

## The backend does not exist yet, so the placeholder path IS the deliverable

There is no `dashboard/` server and nothing in the tree references those routes. Every endpoint 404s today. That makes the degradation path the thing that actually ships, so it got the attention:

> **Every reader is tolerant. A missing, unreachable, or differently-shaped endpoint renders a placeholder that NAMES the endpoint. It never renders a zero.**

On a spend panel that is the difference between *unknown* and *free*. `Start` ships disabled when `/api/start` does not answer, exactly as INFRA-003 requires.

**One real defect here, found by testing rather than by reading:** the Spend and Files placeholders were initially inside collapsed `<details>`, so with no backend those panels showed three em-dashes and no reason for them. The summary line now carries the state — `Other files — waiting for /api/files` — visible without expanding anything.

## Verified in a real browser, over real HTTP

**43 assertions, ALL PASS**, driven by Chromium against both servers. Highlights:

| | |
|---|---|
| 6 tabs, exactly **one** panel visible | pass |
| **10** `<details>` | pass |
| every tab renders, both live and bare | pass |
| roving tabindex `0,-1,-1,-1,-1,-1`; Arrow/Home/End | pass |
| correction row renders **−$0.1452**, not clamped | pass |
| kind conveyed by the **words** *estimated* / *correction* | pass |
| **zero external requests** | pass |
| an open `<details>` **survives a 5-second poll** | pass |
| placeholder names the endpoint on all five panels | pass |
| a failed fetch never renders `$0.00` | pass |
| no JS errors | pass |

## The accessibility review found things I would not have

I ran the specialist review the hook requires. It confirmed my own contrast finding and returned twelve further real defects. **Three were serious, and one of them I had introduced:**

**1. My 5-second poll destroyed page state.** `innerHTML = render()` collapsed every `<details>` the user had opened, reset the screen reader's virtual cursor mid-sentence, and dropped focus to `<body>`. Now an in-place update when the same funnels are still running, full re-render only when the set changes. There is a test that opens a disclosure and waits out a poll.

**2. My live region was both silent and spammy.** I had put `aria-live` on the Now panel. That panel carries `[hidden]` on five of six tabs, and `[hidden]` removes the subtree from the accessibility tree — **so a run failing while the user was on Settings would have announced nothing at all.** While visible it would have announced every changed number on every poll. Replaced by one announcer pair outside every panel, firing on state transitions only, with a monotonic gate so progress jitter cannot re-announce.

**3. The dark-mode primary button failed AA at 3.65:1.** White on `--accent #0a84ff`. The fix is not to darken `--accent` — as *text* it clears 4.5:1 by only 3.5%, so summaries and ghost buttons would drop below AA. `--accent-solid` is now a separate token: **4.93:1**.

### The contrast finding I measured myself

`--dim` in **light mode only** fails AA: **3.51:1** on `--bg`, 3.62:1 on `--panel`. It carries the *word* half of every "number and a word", plus `.sub`, `.note`, `.meta`, `th` and `.empty` — most of the text on the page. Raised to `#6e6e73` (Apple's own `secondaryLabel`), **4.91:1**, visually indistinguishable. Dark mode already passed at 5.22:1 and is untouched.

### Also fixed, none of them visible

Form hints were absorbed into the accessible **name** of all seven controls (a wrapping `<label>` flattens its whole subtree), so `Target` was announced as *"Target Stops once this many qualified leads are found"* on every focus, unsuppressably — now explicit `label for` + `aria-describedby`. Input borders were **1.22:1** with a 1.03:1 fill, so a field read as plain text until clicked. `color-scheme` was undeclared, which meant the dark-mode `<select>` popup — the only way to choose which funnel to run — rendered light-on-black. Bar widths moved to CSSOM because **a strict CSP blocks style *attributes*** and every bar would have shipped at 0% width. Plus a `<main>` landmark, card headings, seven identically-named Download buttons disambiguated, 320px reflow, forced-colors, `<noscript>`, `type="button"`, and wheel-blur on number inputs.

**Two subtleties I would have got wrong:**
- `.row + .row`, **not** `:first-of-type` — the latter matches on *element type*, so the first injected non-row `<div>` would steal it and row 1 would gain a border it never had.
- `overflow-wrap: anywhere`, **not** `break-word` — only `anywhere` feeds the min-content size that grid and table track sizing read, so only `anywhere` actually shrinks the column.

### The progress bar went the other way

I had added `role="progressbar"` with `aria-valuenow`. It is now **`aria-hidden`**: the percentage is already text one node away, and NVDA's default progress-bar output is a *beep* — on every poll, per running funnel. The bar is a redundant visual encoding of a number that is already readable.

### `<summary>` needs nothing — and adding ARIA would break it

The disclosure state *is* announced; browsers compute it from `[open]` on the parent, and hiding the marker is purely presentational. **Adding `aria-expanded` would be an active bug** here: author ARIA overrides the native state, and with JS disabled it could never update — a visibly-open panel would announce "collapsed" forever. The requirement that the disclosures work with JS off is exactly what makes that attribute wrong.

---

## Two conflicts I did not resolve — they need your call

Both are genuine WCAG failures whose only fix is visible, and you froze the design. I am flagging, not changing.

| | issue | the fix, and what it costs |
|---|---|---|
| **1** | **The selected tab is signalled by colour alone.** `--panel` on `--bg` is **1.03:1** light, 1.23:1 dark; the 4% box-shadow is below perceptual threshold. `aria-selected` covers screen-reader users completely — this affects sighted low-vision users, who cannot tell which of six sections they are in. | a `--line-strong` ring (1px of geometry, compensated by padding) or `font-weight:600` on the selected tab (reflows the strip slightly) |
| **2** | **`<summary>` is distinguished from body text by accent colour alone** (1.4.1) — no underline, no marker, no weight change. Structurally the same failure as an unstyled link. | a CSS-drawn chevron: no image, no icon font, ~4 lines, but it is a visible mark the mockup does not have |

I did apply the forced-colors block for conflict 1, so in Windows High Contrast the selected tab is `Highlight`/`HighlightText`. That covers HCM users and leaves the normal-mode question open.

---

## Verification

| check | result |
|---|---|
| page loads at `127.0.0.1` | yes — both `8899` (mock API) and `8898` (`--bare`) |
| every tab renders | 6/6, live and bare |
| live data where ready | all five panels render the contract shapes |
| placeholders where not | all five name their endpoint; `Start` disabled |
| looks like the mockup | yes — see screenshots; `$4.46 lifetime` and 3-decimal card spend match |
| browser assertions | **43, ALL PASS** |
| zero external requests | asserted, empty |
| light and dark | both captured |

## Limits

- **Nothing was tested against a real backend**, because there is none. `scratch/infra005_mockapi.py` is a throwaway I wrote to prove the live path; if the real endpoints return different shapes, the tolerant readers will fall back to placeholders rather than crash, but the *rendering* of those shapes is unproven.
- **The endpoint contract is my best reading of INFRA-003, not an agreed schema.** I accept several key spellings per field (`spend_usd`/`spend`, `entries`/`rows`) precisely because I was guessing.
- **The MCP browser in this session could not reach this host at all** — loopback, LAN IP, `file://` and `data:` all failed, and external navigation timed out. Everything here was verified with Playwright driving Chromium directly. That is a real browser over real HTTP, but it is not the review browser, and I could not screenshot through the tool the session provides.
- **No screen reader was run.** Every accessibility claim is either a measured contrast ratio, a DOM/ARIA assertion, or specialist advice — none of it is "I heard NVDA say this".
- **The announcer is wired but barely exercised.** Only the progress-milestone path fires in testing; the failed/stopped-at-cap transitions have no backend to produce them yet.
- **`[data-theme]` is styled but nothing sets it.** There is no theme toggle; the override exists for whoever adds one.
- **The two conflicts above are unresolved**, so the page has two known 1.4.1 failures I chose not to fix unilaterally.
- **Settings has no save control.** The knobs render and are editable; nothing persists them, because `PUT /api/settings` does not exist. That is a gap, not a decision.

---

<!-- CLAIMS
file:   dashboard/static/index.html
file:   dashboard/static/app.css
file:   dashboard/static/app.js
file:   scratch/infra005_verify.py
file:   scratch/infra005_mockapi.py
-->

*The accessibility hook applied to this round — unlike the Python rounds before it, this is a real user-facing surface — so the review was run and its findings are in §"The accessibility review", including the three defects it caught that I had shipped.*
