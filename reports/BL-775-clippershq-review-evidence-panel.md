# BL-775 — information for a review, not a verdict

**2026-08-11 · DB now() = `2026-08-11 14:22:52.741111+00` · BUILD.**
Base `origin/main` @ `9d285c8c`. Branch `checkpoint/BL-775` @ `4c672bd2`, **verified pushed**. Tags `pre-BL-775` and `post-BL-775` on origin. Worktree `C:/b775`, short path, no junctioned `node_modules`, removed at the end. Nothing written to the database; every read through `scripts/run-select.js`.

**No score exists anywhere in this round.** `grep` over the three new files, excluding comments, returns **0** references to `fraudScore`, `groupBy` or `percentile`.

---

## THE GOVERNING RULE, AND WHY IT HELD

BL-771 measured what a single number would be worth: against 206 clips the owner had already rejected for bought views, every computable signal came in under **21% precision** against a **99.2%** reviewer bar. R-5 measured `fraudScore` at **19.0%** rejection for score 0 and **19.5%** for score 40+, concluding verbatim **"`fraudScore` has no predictive power"**.

So this panel has no score, no percentage-likelihood, no 1-to-100, no composite, no traffic light, no badge, and no `className` computed from any value. It shows facts and the owner decides.

---

## PART 1 — THIS CLIPPER'S OWN RECORD

### Reasons are free text, and the panel says so rather than inventing a category

Measured on live data: **994 rejected clips carry 413 distinct reason strings**, 15 null and 153 blank. The audit log stores the same free text, verbatim shape:

```
{"previousStatus":"PENDING","newStatus":"REJECTED","rejectionReason":"Song is not main focus and not an edit"}
```

There is **no reason category anywhere in the schema**. R-5 reached the same conclusion independently: *"Rejection reasons confirm it, being long prose essays about logo placement and card colours."*

So the bought-views count comes from a **coarse word match**, the panel states that in plain words, and **the owner's own wording ships beside it, unedited**. He checks the words himself rather than trusting a classification nobody can validate.

### What the panel shows, on real data

| id8 | submissions | rejections | mentioning bought views | most recent |
|---|---|---|---|---|
| `cmpq1awm` | 151 | 40 | **34** | 2026-07-17 |
| `cmpoj6uo` | 84 | 26 | **23** | 2026-07-17 |
| `cms7miow` | **22** | **22** | **22** | 2026-08-03 |
| `cmppnwdw` | 33 | 21 | 18 | 2026-07-17 |
| `cmpwewuy` | 33 | 16 | 16 | 2026-07-28 |

`cms7miow` is BL-774's Clipper F: 22 of 22 clips rejected, all with the identical reason **"botted views buddy"**, in a two-minute sweep on 2026-08-03. A reviewer opening any clip of his now sees that instantly.

**Always X of Y, never a bare count.** The accessibility review was blunt about this and right: "3 rejections" is an accusation, "3 of 41 clips were rejected" is evidence.

**No cross-creator comparison.** Every figure is one clipper's own record shown to a human reviewing that same clipper's clip. There is no group-by across creators and no percentile in the code.

---

## PART 2 — THE VIEW-ARRIVAL CURVE, WHICH IS FREE AND WORKS TODAY

### The discriminating window is 6 hours, not 24

Measured across **4,496 clips**, comparing approved clips against those the owner rejected with a bought-views reason:

| cohort | platform | clips | by 6h | by 24h | by 72h |
|---|---|---|---|---|---|
| approved | Instagram | 2,159 | **66.4%** | 91.0% | 98.2% |
| rejected, bought views | Instagram | 110 | **7.8%** | 81.0% | 100.0% |
| approved | TikTok | 1,021 | **40.6%** | 79.1% | 93.6% |
| rejected, bought views | TikTok | 50 | **6.3%** | 72.9% | 99.1% |
| approved | YouTube | 1,130 | 35.2% | 86.6% | 99.8% |
| rejected, bought views | YouTube | 26 | 37.5% | 88.2% | 93.5% |

**Three findings, all new this round.**

**The 6-hour gap is large and the 24-hour gap is not.** Instagram separates 66.4 against 7.8 at six hours; by twenty-four the two are 91 and 81. BL-771 reported 78 against 31 at 24 hours on TikTok, and **my figures are not comparable to that** because BL-771 measured share of *peak* from first sighting while this measures share of *current views* from clip creation. Different denominator, different origin. I am refining the finding, not restating it.

**Instagram, which BL-771 measured as 58% of the bought-view problem, shows the largest separation.** That makes this the most valuable part of the round, exactly as the brief predicted, and it needs no vendor, no connection and no analytics.

**YouTube does not separate at all**, 35.2 against 37.5. The panel says so, so a YouTube curve is never read as meaningful.

### The confound that would have made this harmful

Among **approved** clips only:

| clip size | approved clips | median % by 6h | share under 10% at 6h |
|---|---|---|---|
| under 1k views | 2,201 | 52.4% | 18.0% |
| 1k to 10k | 1,832 | 54.0% | 12.6% |
| 10k to 100k | 221 | 24.8% | 29.4% |
| **100k and above** | **58** | **0.7%** | **87.9%** |

**87.9% of the platform's biggest genuine hits had under 10% of their views at six hours** — the same shape a drip-fed purchase makes, because a clip that keeps growing for weeks always looks slow at the start. A reviewer reading a slow start as evidence of buying would flag the platform's best clips first.

**That sentence ships beside the curve, every time.** A signal whose confound lives only in a report is a trap.

### Coverage, measured

| | clips | with 3+ snapshots | computable |
|---|---|---|---|
| approved | 4,392 | 4,338 | **98.8%** |
| rejected, bought views | 189 | 184 | **97.4%** |
| other rejections | 774 | 565 | 73.0% |

Across all live clips: 5,316 of 5,355 carry at least one snapshot, 4,916 carry six or more, and 4,747 were still tracked 24 hours after submission. **A curve computed from two snapshots is noise, so the code refuses to draw one below three** and says which of three reasons applied.

---

## PART 3 — ANALYTICS, AND AN HONEST GAP

**BL-773 is not merged.** It shipped to `checkpoint/BL-773` and `ClipAnalyticsCard` does not exist on `main`. Importing it would have made this round unbuildable and would have silently coupled two unmerged branches.

So the analytics section renders **BL-773's own absence wording, kept identical** so the two can never disagree, and the integration seam is marked in the code. On the day BL-773 merges this is one import plus one element swap. I would rather disclose that than pretend the integration happened.

The absence wording is written so an unconnected clipper is never read as a suspicious one, which will matter for a long time because almost every clip is in that state.

---

## PART 4 — WHAT THE OWNER SEES

> **Information for this review**
> Three sets of information, in a fixed order so this panel looks the same every time. The order is not a ranking. No set counts for more than another. Nothing here adds up to a score, and nothing here has changed the clip.
>
> **Other clips by this clipper**
> 22 of 22 clips by this clipper were rejected (100%). 22 of 22 carry a written reason mentioning bought or botted views, most recently on 2026-08-03.
> *Rejection reasons are free text with no recorded category, so that second count comes from matching words rather than from a stored label. Your own wording is below.*
> ▸ Show 1 past rejection note you wrote (unedited, may be blunt)
>
> **When the views arrived**
> 6h — 4.1% of current total views · 24h — 61.0% · 72h — 98.2%
> *Current total 48,120 views, from 34 stored snapshots over 512 hours.*
>
> **Platform analytics**
> Analytics are captured only when a clipper connects their TikTok account. This clipper has not connected one, so there is nothing to show.
>
> ▸ Background counts from past clips. Not a test for this clip.
>
> *Information only. No score, no rating, nothing judged. No status, earnings or payout touched. The clipper sees none of this.*

*(Layout illustrative; the figures above are the shape, not a specific clip.)*

**Unavailable is stated, never omitted.** A missing row could otherwise read as a clean one, so the curve distinguishes a value from "Not reached yet" from "No snapshot recorded", and a blank is never rendered because **a blank reads as 0%, which is the strongest possible bought-views signal**.

---

## PART 5 — WHAT CANNOT HAPPEN

| check | result |
|---|---|
| `fraudScore` in new code (non-comment) | **0** |
| `groupBy` / `percentile` in new code | **0** |
| `.update(` / `.create(` / `.delete(` / `writeClipEarnings` | **0** |
| Clipper-facing route references | **0** |
| Money files + `tracking.ts` + `campaign-era.ts` | **all IDENTICAL** by blob OID |

The read route enforces `requireOwnerOrCapability("CLIP_VIEW")` **server-side before a byte is returned**, matching BL-666's gate, because a render-only gate leaks through the network tab. Every mention of `fraudScore` or peer bands in the diff is prose in a comment explaining why they are not used.

---

## PART 6 — PROVEN ON REAL DATA, AND WHAT IS NOT

**Proven with real production data:** the clipper-history figures in PART 1 (five real clippers, including BL-774's Clipper F reproduced exactly); the velocity cohort table across 4,496 clips and all three platforms; the size confound across 4,312 approved clips; snapshot coverage; that reasons are 413 distinct free-text strings; and that no clip's status or earnings changed, with the **earnings invariant at 0 violations**.

**Proven structurally only:** that the panel renders. **No browser render was performed** — the admin queue needs an owner login I do not have, so the component's visual layout is unverified. Same honest limit as BL-762, BL-765 and BL-773.

**Not yet wired into the queue page.** The component and its route exist and build; mounting it as a sibling of `ReviewerNoteCard` in the 2,807-line queue page is deliberately left as the next step, so this round ships the computation and the component without editing a file three other rounds are queued against.

### Gates

`eslint` present, so the hooks gate is real. `npx prisma generate` ran after `npm ci`.

| gate | result |
|---|---|
| `npx tsc --noEmit` | **exit 0**, 0 errors |
| `npm run build` | **exit 0**, compiled in 31.2s |
| `lint:hooks` | **0 errors, 11 warnings**, at the ceiling, unchanged |

Diff is real: 4 files, 3 new.

### Accessibility

Reviewed by the lead with four specialists. **The review landed after a first draft was written and caused a substantial rewrite**, which I state plainly rather than implying the sequence was cleaner than it was. Blocking items applied:

• Title changed from "Evidence for review" to **"Information for this review"** — the original was prosecutorial in a UI a human reads before deciding a person's pay.
• Section renamed from "this clipper's record" to **"Other clips by this clipper"** — "history" reads as priors.
• **X of Y everywhere**, never a bare count.
• **The order is disclaimed in words**, because an unstated order is read as a ranking and the reader invents a rationale nobody can correct.
• Curve is a **`<dl>`, not a table** — one variable at three points is a description list, and a table costs roughly eight announcements against three on every row of a long queue.
• **Three distinct missing states**, never a blank or a dash.
• Population line carries **both numbers, the overlap, the date, the sample size and "This clip has not been scored"**, behind a `<details>` at the foot. One number alone would be a threshold.
• Quoted notes in **`<figure>` + `<blockquote>` + `<figcaption>`** with an `sr-only` lead-in **inside** the quote and **before** the text, because a `figcaption` comes after and a screen-reader user would otherwise hear the accusation before learning who wrote it. Shown in full, never truncated, never masked.
• Control and bidi characters stripped **by code point**, because a bidi override inside one note can visually reverse the surrounding trusted text and make one clipper's words appear to belong to another row.
• **No `aria-live`, `role="status"` or `role="alert"`** anywhere. The queue polls, and a live region would re-announce accusations about a named person on every tick.
• Tokens only, **no valence colour**, no badge, no bar, no gauge, no emphasis keyed to magnitude. `headingLevel` prop defaulting to 4.

**Disclosed, pre-existing, not fixed:** the queue page has one `h1` at line 1231 and no row `h3`, so this panel and `ReviewerNoteCard` both sit at `h4` under an `h1`; the `headingLevel` prop makes the future re-level one edit. `ReviewerNoteCard` also references `--bg-page`, undefined anywhere and resolving to transparent.

---

## VERIFICATION

No score, percentage-likelihood or composite is computed or displayed, and `fraudScore` has 0 non-comment references. Nothing auto-rejects, auto-flags or changes status: 0 write calls in the new code. Nothing reaches a clipper: 0 references from clipper routes, and the gate is server-side. Nothing aggregates creators: 0 group-by or percentile, every figure one clipper's own record. Rejection reasons are surfaced from real stored free text with the classification caveat printed and the raw wording shown. Unavailable signals are stated, never omitted, and a blank is never rendered where a zero could be inferred. The absence of analytics is BL-773's own non-suspicious wording. The 6 money files plus `tracking.ts` and `campaign-era.ts` are byte-identical by blob OID. No API key was logged, printed or committed; no Apify actor ran. What is proven on real data and what is structural are separated above. The worktree is removed. No dashes as bullets.
