# BL-887 — the last build round before launch: four deferred UI and accessibility items

Merged `d0327e0`. Branch `checkpoint/BL-887` at `04a73b0c`. Tags `pre-BL-887`, `pre-merge-BL-887`,
`post-BL-887`. Merge tree `8a0a91ff` equals the branch tree, so the branch build **is** the merge build.

**Model split.** Opus decided the 33-token question, resolved the CLAUDE.md conflict, wrote every fix
and this report. One accessibility agent re-derived the defect list for `admin/payouts/page.tsx`; its
findings are marked **READ** and every one I acted on I re-read at source first and marked
**VERIFIED**. No subagent opened a database connection or edited a file.

---

## PART 0 — all four re-measured, and three figures had moved

| item | BL-883/884/885 said | measured today | moved? |
|---|---|---|---|
| dangling `aria-controls` | 262, from `page.tsx:1818` | **confirmed**, 1 unconditional site | no |
| the working counterpart | `LiabilityView.tsx:803` | **`:816`** | **yes**, BL-884's own edits shifted it |
| `--bg-page` definitions | 0 | **0** | no |
| `bg-[var(--bg-page)]` sites | 33 | **33** (a 34th mention is a BL-793 comment) | no |
| files referencing it | 26 | **16** | **yes** — BL-883's 26 counted the six ring-offset files it then fixed |
| ring-offset uses | 6, all fixed | **0** | no, the fixes hold |
| the duplicate id | `:1885` | **`:1934`** | **yes**, shifted by BL-884 |
| admin pages with no title | 43 of 43 | **43 of 43, zero with metadata** | no |
| the thirteen defects | 13 | **19** | **yes**, see PART 2 |

---

## PART 1 — the 262 dangling attributes, which were one line and two defects

**They and the duplicate id are the same defect wearing two faces**, and reading the source is what
showed it. Rows are keyed `${c.userId}-${c.campaignId}-${i}` — **one row per person AND campaign** —
while the panel opens on `expandedUserId === c.userId`, which is true on **every** row for that
person. So a clipper owed money on two campaigns produced:

- two rows each emitting `aria-controls="user-summary-<userId>"` **unconditionally** → 262 references
  to nothing whenever nothing was expanded, and
- when expanded, **two `<tr>` elements carrying the same id** → `aria-controls` and
  `aria-describedby` bind to whichever the parser met first, so on a money page a control can report
  another control's state, delivered only to screen-reader users.

**Both lines, side by side, as the round asked:**

```
broken   page.tsx:1818          aria-controls={`user-summary-${c.userId}`}
working  LiabilityView.tsx:816  aria-controls={open ? `liab-panel-${c.id}` : undefined}
```

The working pattern was copied verbatim, plus a `useId()` base so the id is unique by construction and
derived from **no data at all** — which is the solution BL-883 reached for the same class of bug.

**Proved by rendering, not by reading:** `dangling=0` and `dupIds=0` at 320, 375, 414, 1280 and 1440.

---

## PART 2 — the defects: nineteen, not thirteen

BL-883's published report preserved only three of its thirteen with line numbers, so the list was
re-derived against current source. **17 fixed, 2 deliberately left.** Two were worse than anything
previously named.

| # | defect | before | after | verified by |
|---|---|---|---|---|
| 1 | **Clipper search was KEYBOARD INOPERABLE** | `onMouseDown` with no `onClick`; Enter on a focused button dispatches `click`, never `mousedown` | `onClick` added; blur uses `relatedTarget` so the list survives focus entering it | source read at `:1580`; 2.1.1 |
| 2 | **Devalue dialog had NO focus trap, NO focus return** | passed `title={undefined}`; `modal.tsx:103` computes `manages = manageDialogSemantics ?? Boolean(title)`, so the trap at `:145` never ran while the panel asserted `role="dialog" aria-modal="true"` by hand | branch named `"Make these clips worth less"`, turning the real machinery on | `modal.tsx` read; 2.4.3, 4.1.2 |
| 3 | **Duplicate id + 262 dangling IDREFs** | see PART 1 | `useId()` base, conditional `aria-controls` | render: 0 and 0 at five widths |
| 4 | **Contrast 3.40:1** (4 sites) | `bg-accent` `#2596be` on `#ffffff` = **3.396** | `bg-accent-hover` `#1e7ea3` = **4.595 → 4.60:1**; `hover:opacity-90` → `hover:underline`, because compositing the whole control puts it back to **4.35:1** | ratios computed by hand from `globals.css` |
| 5 | **Unlabelled, keyboard-unscrollable container** `:1749` | bare `overflow-x-auto`; nine columns, so Available / Net After Fee / Actions were unreachable without a mouse | `role="region"` + `aria-label` + `tabIndex={0}` + focus ring — the 1.4.10 exception that actually applies | render: `scrollRegions=2` |
| 6 | **A live region fired a money figure on every keystroke** | `aria-live="polite"` recomputed from the amount field, so typing `12.50` announced five sentences naming figures the owner never intended | `aria-live` removed, `aria-describedby` kept, so it is read on focus | source `:3596` |
| 7 | **Main payout queue had no row headers** | 11 `scope="col"`, zero `scope="row"` | user cell is `<th scope="row">` | source; 1.3.1 |
| 8 | **Three tables with unscoped heads** | `<th>` with no `scope`, campaign cell a `<td>` | `scope="col"` on all, in both byte-identical copies | count asserted at 2 per head |
| 9 | **The disclosure was not a disclosure** | no `type`, no `aria-expanded`, no `aria-controls`, panel had no id and no heading | all four added, wrapped in `<h2>` | source `:1503` |
| 10 | **Campaign dropdown announced no state** | no `aria-expanded`, no `aria-haspopup` | both added | source `:1542` |
| 12 | **Fifty controls all named "Send email reminder"** | named only by `title`, with no clipper | `aria-label` naming the clipper | source `:1904` |
| 14 | **Bare `-` placeholders are silent, not empty** | a missing **wallet/username** read as an empty cell | `aria-hidden` dash + sr-only "No username recorded" | source |
| 15 | decorative icons without `aria-hidden` | inconsistent with ~20 siblings | added on the ones this round touched | source |
| 16 | `showAllClippers` had no `aria-pressed` | label flipped, ambiguous | `aria-pressed` + fixed sr-only label | source |
| 19 | **13 bare `•` bullets** not `aria-hidden` | against the house rule one item in the same list already followed | all 13 wrapped | count: 13 |

**Left deliberately, with counts and reasons:**

- **#11 auto-refresh cannot be paused.** The table refreshes every 15s and re-sorts on a 30s clock, so
  rows move under a reader. WCAG 2.2.2, and genuinely arguable: the "essential" exception can be
  claimed for an SLA queue. Adding a pause control changes product behaviour on a live money queue.
  **The owner's call, not a cleanup.**
- **#13 about 30 hardcoded palette colours fail 1.4.3 in the light theme.** Measured against light
  `--bg-card` `#ffffff`: amber-400 **1.67:1**, amber-300 **1.44:1**, emerald-400 **1.92:1**,
  yellow-400 **1.53:1**, red-400 **2.77:1**. Same repo-wide conflict BL-885 escalated for
  `text-accent`. Changing 30 colour sites on a money page is a visual change dressed as a bug fix,
  which is exactly what BL-883 refused for the 33 tokens.

> **Colour cannot carry state here and every fix respects that.** `--text-primary`,
> `--text-secondary` and `--text-muted` are all `#ffffff`, so every state above is said in **words**.

---

## PART 3 — the 33 tokens, decided by measurement

A real browser was asked what the declaration actually computes to:

```
background-color: var(--bg-page)   ->  rgba(0, 0, 0, 0)
background-color: transparent      ->  rgba(0, 0, 0, 0)
background-color: a REAL token     ->  rgb(24, 24, 27)
```

So the three groups the round asked for are:

| group | count |
|---|---|
| **visually identical**, and safe to change — but only to `bg-transparent` | **33** |
| **would genuinely change the look**, if given any real token | **33** |
| **cannot tell without seeing them** | **0** |

Every one of the 33 is a border-delimited inset panel or input inside a card or a modal. Today the
border draws the edge and the fill shows the card behind. Giving them `--bg-primary` would paint them
**darker than their own parent** — visible in dark, clearly visible in light where `#fafafa` sits on
`#ffffff`. That is the visual change BL-883 refused to make in one unreviewed commit, and this round
has no mandate for it either.

**All 33 across 16 files became `bg-transparent`**, which provably moves no pixel and is strictly
better than leaving them: while 33 declarations still named a token nobody had defined, anyone who
ever defined it — by copying a stylesheet or following an old note — would have repainted 33 surfaces
at once with nobody reviewing it. **The ghost token now has ZERO declarations.** The guard's ceiling
came down from **33 to 0**.

---

## PART 4 — the titles, and the rulebook conflict settled

**The rule was already not being followed.** CLAUDE.md said `Tab title: just "Clippers HQ"` while
`src/app/layout.tsx` has always shipped `"Clippers HQ — Get Paid to Clip"`.

**What the rule was for.** It sits in DOMAIN RULES beside *"One P: clipershq.com (NOT clippershq)"*
and *"Belgrade/Serbia is NEVER shown"*. Those are **brand-correctness** rules. Read that way it means
the tab must say the brand and say it correctly — it was never about forbidding a page name.

**The resolution satisfies both.** `title.template` on the root puts the brand in every tab and lets
each page name itself: **"Payouts — Clippers HQ"**. 2.4.2 is met; the brand is in every tab, correctly
spelled, with no location.

- **15 server pages** carry `export const metadata` directly.
- **26 client pages** got a sibling `layout.tsx`, because a client component cannot export metadata.
- **2 pages** already had a layout (both role gates); the title joined it rather than a second file.
- **43 of 43 covered, 43 DISTINCT titles.**

**CLAUDE.md is corrected** to state exactly what shipped, with the reason, so the next round cannot
re-derive the old answer — which is what it did with the nonexistent `--bg-page` token until BL-883
corrected it.

**And the render caught one more.** The first pass read back a bare `"Payouts"`: a plain-string title
in a layout **consumes** the parent template and passes none of its own down, so `admin/layout.tsx`
was stripping the brand from every admin page. It carries a template of its own now.

---

## PART 5 — the guards

**An eighth check could not fail, and it was this round's own.** The title check asked only *does this
page resolve to a title* and walked up to `admin/layout.tsx`, which has one — so every page passed no
matter what was deleted. It asserts **distinctness** now, which is what 2.4.2 is actually about, since
the defect was never "no title" but *43 pages sharing one*.

**And the stricter version immediately caught a real defect in this round's own work:** three titles
collided — "Archive", "Disputes" and "Users", each twice. 40 distinct across 43. Now 43 of 43.

**5 of 5 checks demonstrated failing**, one at a time, never sampled, each naming itself, tree
restored and re-verified after each: T1a (a page stops naming itself), T1b (two pages share a title),
T2 (the root stops appending the brand), T3 (the rulebook gets the old sentence back), R2 (a new
`bg-[var(--bg-page)]` is written).

| prebuild guard | wired | result |
|---|---|---|
| `check:prisma-bypass` | yes | 0 violations |
| `check:removed-fields` | yes | OK |
| `check:event-wiring` | yes | 0 problems |
| `check:v2-leg-sync` | yes | OK, 3 documented opt-outs |
| `check:v2-editor-balance` | yes | 19 passed, 0 failed |
| `check:paid-is-final` | yes | 14 passed, 0 failed |
| `check:payout-snapshot` | yes | 9 passed, 0 failed |
| `check:css-tokens` | yes | 3 passed, 0 failed — **ceiling now 0** |
| `check:liability-rules` | yes | 13 passed, 0 failed |
| `check:v2-strike-sites` | yes | 16 passed, 0 failed |
| `check:schema-drift` | yes | OK, 140 uniqueness constraints verified |
| **`check:page-titles`** | **yes — NEW** | **3 passed, 0 failed** |
| `lint:hooks` | yes | 0 errors, 10 warnings (ceiling 11) |

**Thirteen guards, every one wired.**

---

## PART 6 — nothing moved that should not have

**This round touched no money path**, and that is proved rather than asserted:

| | |
|---|---|
| seven protected money files | **BYTE-IDENTICAL by blob OID on both refs** |
| `prisma/schema.prisma` | **untouched**, zero diff |
| earnings invariant | **0 violations across 10,216 clips** |
| payout fingerprint | `6d48cd5b8679f61d4558b710693688aa` — **identical to the opening snapshot** |
| clip fingerprint | `83ba5402cd93c7b36fe4d52efb728a7a` — **identical to the opening snapshot** |
| sandbox rows | 1 created (a `bl887sbx-` OWNER for the render cookie), **1 of 1 removed and verified**, 0 remain |

> **ONE COUNT MOVED AND IT WAS NOT ME.** Users read 1752 at the opening snapshot and **1753** at the
> end. A **real clipper signed up at 14:29:01** during the round — a product cuid with
> `isTestUser: false`. Zero `bl887sbx-` rows remain. Saying "identical counts" would have been false.

**10 of 10 renders**, after a first pass that **failed all ten** on the title. Pan measured rather than
`scrollWidth`: **0 px at 320, 375, 414, 1280 and 1440**, with `innerWidth` and the URL read back each
time, against a production build with `DEV_AUTH_BYPASS=false` and a real minted session cookie.

---

## Everything that now stands between the owner and a real editor using the marketplace

**Nothing a round can do remains. Every item below is his decision or his click.**

1. **BL-879's visibility gates are closed.** No editor can reach the marketplace v2 surfaces until
   they are opened. *This is the first switch.*
2. **No campaign has a type set.** All 34 are `NORMAL`, so no editor can submit anywhere and no poster
   sees a catalogue. At least one must become `BOTH` or `MARKETPLACE_ONLY`. *This is the second.*
3. **A redeploy is owed.** BL-885's strike table and BL-886's index are applied to the database; the
   code that reads them, and this round's UI, ship with these merges.
4. **The strike window (90 days) and the ban length (7 days)** are one-line constants in
   `src/lib/marketplace-v2-strikes.ts`. BL-876 said the window is his call.
5. **Question 14** — whether changing a campaign's type mid-flight is blocked or grandfathered.
6. **Question 16** — whether a poster may see which other posters took the same clip.
7. **Auto-refresh on the payout queue cannot be paused** (WCAG 2.2.2, arguable). Adding a control
   changes behaviour on a live money queue. **His call.**
8. **About 30 hardcoded palette colours fail 1.4.3 in the light theme**, measured 1.44:1 to 2.77:1.
9. **`text-accent` on money figures fails 1.4.3 in the light theme repo-wide**, and CLAUDE.md mandates
   it. **A rulebook conflict and his call.**
10. **Four undeclared `ON DELETE CASCADE` foreign keys** on `channel_read_status` and
    `community_mutes`, and **ten CHECK constraints no schema can express** — found by BL-886, recorded,
    neither blocking launch.

**Closed by this round and no longer on the list:** the 262 dangling `aria-controls`, the thirteen (in
fact nineteen) `admin/payouts` defects, the 33 inert background tokens, and the missing page titles.

**Rollback:** revert the merge commit. No schema changed, no data moved and no migration ran, so the
revert is complete on its own.
