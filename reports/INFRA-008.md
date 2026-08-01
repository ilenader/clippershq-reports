# INFRA-008 — Both colour-alone failures closed with **zero layout shift**, and all 38 contrast pairs re-measured PASS in both modes. The backend is live and five panels render real data — after **four contract mismatches**, one of which was hiding a running clip walk behind "Nothing running"

**Date:** 2026-08-01 · **Type:** Implementation · **Spend:** **$0.0000 · 0 paid calls**
`dashboard/static/{app.css,app.js}` only. No backend file touched — `dashboard/server.py` belongs to INFRA-006, which was in flight throughout (9 other rounds were). Claim filed and cleared. Committed as **`cc4e58a`**.

---

## 1. The selected tab — a 2px underline

Was `--panel` on `--bg`: **1.03:1** light, 1.23:1 dark, with a 4%-opacity shadow below perceptual threshold. Selection was carried by hue alone.

```css
.tabs button{position:relative}                    /* on EVERY tab, not just the selected one */
.tabs button[aria-selected="true"]::after{
  content:"";position:absolute;left:14px;right:14px;bottom:5px;height:2px;
  background:var(--accent);border-radius:2px}
```

**An absolutely-positioned `::after`, not a `border-bottom`.** That choice is the whole engineering content of the fix:

- `.tabs` sets no `align-items`, so it defaults to `stretch`. A 2px border grows the selected tab from 35px to 37px, and **stretch then resizes all five unselected tabs to match** — the exact thing you said must not happen.
- The strip wraps. A border migrates 2px between flex lines as selection moves, shifting everything below it.
- On a `border-radius:980px` pill a bottom border is not a line: it renders as a crescent following the cap curve, at full 2px only at the midpoint.
- `outline-offset:2px` is measured from the border box, so the focus ring would grow with it and land 2px from the underline — two 2px accent marks reading as one thick edge.

Out of flow costs nothing in either state. **Proven, not asserted:** the test captures all six tab rectangles, moves the selection, and re-captures — every `x/y/w/h` identical to within 0.5px.

`bottom:5px` rather than 3px because with roving tabindex the focused tab is usually *also* the selected tab, so the underline and the focus ring coexist; 5px leaves 7px of clear background between them.

## 2. `<summary>` — a leading chevron

Accent-coloured text with the marker suppressed is structurally an unstyled link. Nothing on the page signalled what could be opened.

```css
summary::before{content:"";display:inline-block;width:6px;height:6px;margin-right:8px;
  vertical-align:1px;border-right:2px solid currentColor;
  border-bottom:2px solid currentColor;transform:rotate(-45deg)}
details[open]>summary::before{transform:rotate(45deg)}
```

**`content:""` is empty on purpose.** A glyph would be *appended to the accessible name* — `summary` maps to `role=button`, a name-from-content role — giving "▸Why so few?", read out as "black right-pointing small triangle" or swallowed as punctuation. An empty string emits no characters, so it touches neither the name nor the accessibility tree. The disclosure state already comes from `[open]` on the parent; **no `aria-expanded`**, which would override the native state and, with JS off, could never update.

`currentColor` rather than `var(--accent)`, so the forced-colors pass re-maps it to match its own label.

### The stroke width is load-bearing, and I got it wrong first

I shipped `1.5px` on the reasoning that a rotated stroke antialiases and 1px would fail. The test then measured the computed value: **Chromium floors a sub-pixel border to `1px` at DPR 1.** A 1px rotated stroke has ~0.5 peak coverage, degrading 4.70:1 to **~2.09:1 — a fail.** So the fix was silently not applied at the most common pixel density. **2px is the thinnest width that cannot be rounded down**, and the test now asserts the computed value rather than the declared one.

## 3. Every contrast pair, re-measured

`scratch/infra008_contrast.py` parses the tokens **out of `app.css`**, so these numbers cannot drift from the stylesheet. 19 pairs × 2 modes.

| pair | light | dark | needs |
|---|---:|---:|---|
| body text `--ink` on `--bg` | 16.28 | 19.29 | 4.5 |
| card text `--ink` on `--panel` | 16.83 | 15.63 | 4.5 |
| **the word half `--dim` on `--bg`** | **4.91** | **6.44** | 4.5 |
| **the word half `--dim` on `--panel`** | **5.07** | **5.22** | 4.5 |
| summary / link `--accent` on `--panel` | 4.70 | 4.66 | 4.5 |
| unselected tab `--dim` on `--bg` | 4.91 | 6.44 | 4.5 |
| selected tab `--ink` on `--panel` | 16.83 | 15.63 | 4.5 |
| solid button `#fff` on `--accent-solid` | 4.70 | 4.93 | 4.5 |
| ghost button `--accent` on `--panel` | 4.70 | 4.66 | 4.5 |
| estimated tag `--warn` | 5.20 | 8.28 | 4.5 |
| correction tag `--bad` | 5.44 | 4.99 | 4.5 |
| **★ selected-tab underline on `--panel`** | **4.70** | **4.66** | 3.0 |
| **★ selected-tab underline on `--bg`** | **4.54** | **5.76** | 3.0 |
| **★ summary chevron on `--panel`** | **4.70** | **4.66** | 3.0 |
| **★ summary chevron on `--bg`** | **4.54** | **5.76** | 3.0 |
| input border `--line-strong` | 3.26 | 3.20 | 3.0 |
| progress fill `--accent` on `--line` | 3.85 | 3.82 | 3.0 |
| focus ring `--accent` on `--bg` | 4.54 | 5.76 | 3.0 |
| running dot `--good` on `--panel` | 3.60 | 8.42 | 3.0 |

**38 of 38 PASS.** ★ = added this round.

**On `--dim`:** you noted INFRA-005 measured 3.51:1. That was the *before* figure — INFRA-005 raised it to `#6e6e73` in the same round, and it measures **4.91:1 / 5.07:1** today. It is the one to keep watching, because it carries the word half of every "number and a word", but it is not currently failing.

Two notes on the criterion. **1.4.1 has no ratio of its own** — it is purely qualitative, requiring a non-colour cue to *exist*; the visibility of that cue is then policed by 1.4.11 at 3:1. And both new indicators are measured against `--panel`, because both only ever render on a panel-coloured surface; the `--bg` rows are a robustness check, and all four clear 3:1 either way.

## 4. Frozen — verified, not assumed

| | |
|---|---|
| 6 tabs, exactly one panel visible | pass |
| the 4 static disclosures intact | pass |
| idle funnels behind a single line | pass |
| paragraph count unchanged (6 `.note`, as INFRA-005 shipped) | pass |
| both safety paragraphs present | pass |
| zero external requests | pass |
| **the poll still preserves an open `<details>`** | pass |
| **the announcer is still outside every tabpanel; `#now-live` has no `aria-live`** | pass |

**One correction to my own test.** I first asserted "10 collapsible sections" against the live backend and it read 6 — correctly. Ten is a property of the *mockup's data* (two running funnels → two Details cards; three settings groups). Live there are different numbers of both. The invariant that actually holds against any data is the four static disclosures plus "everything secondary is inside one", and that is what the test now checks.

## 5. The live backend — five panels real, four mismatches fixed

Eight endpoints answer. `Now`, `History`, `Spend`, `Files` and `Settings` all render live data with **no placeholder**; `Start` is enabled; nothing is left waiting.

| endpoint | end to end? |
|---|---|
| `/api/now` | **yes** — after the `headless` fix below |
| `/api/spend` | **yes** — lifetime $4.70, correction still renders **−$0.1452** |
| `/api/history` | **yes** — legitimately empty: 0 of 154 ledger rows carry a `run_id`, exactly as INFRA-003 predicted |
| `/api/files` | **yes** — primary card + 40 decoys |
| `/api/settings` | **yes** — all **44** knobs |
| `/api/start` | **yes** — enabled; not exercised (it spends money) |
| `/api/videos` | **live but unwired** — the page shows the static "memebot is not wired" |
| `/api/health` | **live but unwired** — nothing calls it |

**The four mismatches, in order of how much they mattered:**

1. **A running clip walk was invisible.** `/api/now` reports live work in **`headless`** as well as `running`, and the page read only `running` — so it said "Nothing running" while a walk was 16 minutes in and had spent $0.19. Both are now merged through one `runningOf()`.
2. **The header disagreed with the cards.** Having fixed (1) in `renderNow` only, the header still counted the raw array and read **"0 running" above two cards saying running**. One definition now feeds both — computing it twice is what caused it.
3. **`/api/start` is POST-only.** The probe used GET, got 405, and the tolerant reader turned that into "absent" — so Start shipped **disabled against a backend that was there**. It now probes by status rather than by body.
4. **Shapes.** `settings` is a flat map of 44, not `{groups:[]}`; `files` uses `primary`/`decoys`/`download_url`; `spend` uses `rows`/`ledger_key`/`amount`, and `label` is present-but-**empty** on every ledger row, so an ordinary fallback chain returned `""` and the column rendered blank.

**The 44 knobs render as one group, kept shut.** "Nothing on screen unless asked for" holds, and the count of disclosures stays put. Curating and grouping them is INFRA-006's round, in flight as I write — I deliberately did not duplicate it.

## 6. `server.py` does not serve the frontend

`GET /` on the backend is a **404**. It exposes the eight API routes and no static files, so nothing puts the page and the API on one origin. I used `scratch/infra008_serve.py` — a static server that proxies `/api` and `/download` — to verify end to end. **That is a scratch stand-in, not the answer**; a `StaticFiles` mount in `server.py` is, and that file is INFRA-006's.

---

## Limits

- **`server.py` is not mine and I did not change it.** The proxy exists only so this round could verify; deployment still has no single-origin story.
- **`/api/start` was never exercised.** It spends money. "Enabled" means the probe says the endpoint exists, not that starting a run works.
- **`PUT /api/settings` was not exercised either** — the knobs render and are editable, nothing was saved. There is still no save control.
- **No screen reader was run.** Every claim here is a computed style, a measured ratio, or a DOM assertion.
- **The antialiasing figures (~2.09:1 at 1px, ~3.15:1 at 1.5px) are the reviewer's coverage model, not something I measured on a display.** What I measured is that Chromium computes `1.5px` as `1px`, which is what made the model decisive.
- **I nearly reported a backend encoding bug that does not exist.** My diagnostic piped `curl` into Python without `PYTHONUTF8=1`, so UTF-8 em-dashes decoded as `â€"` and I counted 31 "mojibake" strings across the API. The browser receives them correctly and the page renders a clean `—`. The fault was in my measurement, not in INFRA-004.
- **Nine rounds were in flight**, two of them in `dashboard/` and `clippershq/`. The live figures in §5 are a snapshot of a system being changed underneath the measurement.
- **`/api/videos` and `/api/health` remain unwired** — the Videos panel is still the static empty state.

---

<!-- CLAIMS
file:   dashboard/static/app.css
file:   dashboard/static/app.js
file:   scratch/infra008_verify.py
file:   scratch/infra008_contrast.py
file:   scratch/infra008_serve.py
-->

*The accessibility hook applied and the review was run. It confirmed the underline over a left border, corrected two things I had wrong — `forced-color-adjust` is inherited, so the underline needed a `HighlightText` override, and pinning the chevron to `LinkText` would have mismatched its own label since `summary` maps to `button` — and its coverage model is what caught the 1.5px rounding.*
