# BL-832 — the Bot note is off his clip screen too, behind a second, independent switch

**2026-08-29 · DB `now()` = `2026-08-29 19:47:26.340110+00` (first read) to `20:17:14.023871+00` (last) · BUILD AND MERGE.**
Base `origin/main` @ `c54b2d60`. Branch `checkpoint/BL-832` @ `2f3323b2`. **Merged and verified pushed: `origin/main == local == 9e4a7849`.** Tags `pre-BL-832`, `post-BL-832`, `pre-merge-BL-832`, `post-merge-BL-832`, all on origin. Isolated worktree `C:/w832`, a short path, `node_modules` never junctioned, **removed at the end**. Every database read through `scripts/run-select.js`, every timestamp cast `::text` against DB `now()`. Handles redacted, no wallet address read or printed.

**A REDEPLOY ON RAILWAY IS REQUIRED BEFORE ANY OF THIS IS LIVE.**

> **TWO SWITCHES NOW, NOT ONE. `SHOW_REVIEW_EVIDENCE_PANEL` and `SHOW_BOT_NOTE_CARD`, side by side in `src/lib/review-surface.ts`, INDEPENDENT, so either block comes back alone.**
> **AND THE BRIEF'S PREMISE NEEDED CORRECTING AGAIN: 100 requests and 300 queries was the EVIDENCE PANEL before BL-816. The note card's own pre-BL-816 cost was 24 requests a page. Both were already batched.**

---

## PART 1 — HIDDEN THE SAME WAY, BEHIND ITS OWN FLAG

### The flag

**`SHOW_BOT_NOTE_CARD`**, declared immediately below `SHOW_REVIEW_EVIDENCE_PANEL` in `src/lib/review-surface.ts`, `false` by default. Two booleans, two blocks, no coupling: turning either on restores only its own card.

### The diff, in full

```
src/lib/review-surface.ts
+ export const SHOW_BOT_NOTE_CARD: boolean = false;      (with 90 lines of comment: what it turns
+   off, how to turn it back on, its two readers by name, what the card provided, and the fact that
+   the shadow recording is not affected)
~ the three stale lines saying the Bot note "was deliberately left in place" now say the opposite,
  because a comment asserting a structure that no longer exists is how this component passed a
  heading review once already

src/components/admin/ReviewEvidenceBatch.tsx
- import { SHOW_REVIEW_EVIDENCE_PANEL } from "@/lib/review-surface";
+ import { SHOW_REVIEW_EVIDENCE_PANEL, SHOW_BOT_NOTE_CARD } from "@/lib/review-surface";
- export const ReviewerNoteBatchProvider = notes.Provider;
+ export function ReviewerNoteBatchProvider({ clipIds, children }: { clipIds: string[]; children: React.ReactNode }) {
+   return (
+     <notes.Provider clipIds={SHOW_BOT_NOTE_CARD ? clipIds : NO_CLIPS}>{children}</notes.Provider>
+   );
+ }

src/components/admin/ReviewerNoteCard.tsx
+ import { SHOW_BOT_NOTE_CARD } from "@/lib/review-surface";
  useEffect(() => {
+   if (!SHOW_BOT_NOTE_CARD) return;        // the single-clip fallback never fires either
    if (batched) return;
+ if (!SHOW_BOT_NOTE_CARD) return null;     // AFTER the last hook, BEFORE the "loading" branch

scripts/bl831-render.mjs
~ two assertions that INVERT the moment this lands are flipped rather than left to fail silently
```

**That one line's placement is the whole implementation.** Above the hooks it breaks the rules of hooks and the BL-348 gate; below the two early returns every PENDING row would read "Loading bot note..." forever. The accessibility review named that trap in advance and named the line.

**`admin/clips/page.tsx` was not edited at all.** Blob OID `cf1e55c3e80f` on both refs. 10 files changed, 3 of them source, 762 insertions and 8 deletions.

### Before and after, production build, real owner session, same machine, same database, back to back

main's tree was built and measured first, then the branch's. Median of three warm loads each at 1440px. **Two views, deliberately**, because the card is PENDING-only and the queue is newest-first, so what it costs depends entirely on whether a PENDING row is on screen.

| VIEW A — the default queue, carrying 4 PENDING rows | BEFORE | AFTER |
|---|---|---|
| `/api/admin/reviewer-note/batch` requests | **1** | **0** |
| bytes it carried | **5,527** | **0** |
| total requests | 51 | 47 |
| total bytes on the wire | **179.2 KB** | **169.1 KB** |
| **DOM nodes** | **4,276** | **4,179** |
| settle | 2,681 ms | 2,710 ms |

| VIEW B — a pinned search returning exactly one PENDING clip | BEFORE | AFTER |
|---|---|---|
| **total requests** | **4** | **3** |
| `reviewer-note` requests | **1** (2,537 bytes) | **0** |
| total bytes on the wire | **28.9 KB** | **26.5 KB** |
| **DOM nodes** | **924** | **878** |
| database queries for the card, per load | **3** | **0** |
| database time for the card, per load | **305.4 ms** | **0 ms** |

**VIEW B is the deterministic half and it is the one to trust: byte-identical across all three runs on BOTH sides**, so exactly one request, 2.4 KB and 46 DOM nodes were removed and nothing else moved. VIEW A's totals wobble by several requests between identical loads because of the polling shell, so settle time is **not** claimed as a win in either view.

**THE BRIEF'S 100 REQUESTS AND 300 QUERIES IS THE EVIDENCE PANEL'S PRE-BL-816 FIGURE, NOT THIS CARD'S.** The note card's own pre-BL-816 cost was 24 separate requests on a 30-row page; BL-816 batched both. `scripts/bl832-probe-queries.ts` measured what remained on the four PENDING ids the provider actually sends: **3 queries and 305.4 ms**, reading 5,920 bytes of rows. So this round removes the last request, not a storm.

**Two endpoints now have no caller in the app, named rather than orphaned silently:** `POST /api/admin/reviewer-note/batch` and `GET /api/admin/reviewer-note/[clipId]`. Both are kept, both still answer the owner, and **the two still agree byte for byte**, which is the proof the hidden note layer is intact.

---

## PART 2 — PHONE AND DESKTOP, BECAUSE HE NAMED BOTH

`scripts/bl832-render.mjs`, production build, `window.innerWidth` printed beside every shot. **11 shots, 0 at the wrong width, 0 with horizontal overflow. 42 assertions, 0 failures.**

**Every width was proven on a view that actually carries a PENDING row**, reached through the queue's own server-side search, because photographing a queue of decided clips would have proven nothing about a PENDING-only card. The harness asserts that first and fails if the row is not there.

```
queue-top     320 · 375 · 414 · 1280 · 1440    measured == asked, overflow 0
pending-row   320 · 375 · 414 · 1280 · 1440    measured == asked, overflow 0
  at every width: 1 PENDING row on screen, 0 of 21 note strings rendered, 0 reviewer-note requests,
  0 headings inside any clip row, h1 "Clip Review" still present,
  Approve 1 · Reject 1 · Flag 1 still on the row
reviewer-queue 1440                            a REVIEWER sees no card and fetches none
```

**The layout holds where the card used to sit.** The PENDING row now runs Approve / Reject / Flag straight into Live / Track now / Override. Measured residue, exactly as the accessibility review predicted: **1 empty grid cell per PENDING row at every width**, the `col-span-2` wrapper at `page.tsx:2443` that page.tsx still renders, costing about **8px below 640px** and **4px above**. It has no role, no name and no content, so it is pruned from the accessibility tree: no announcement, no tab stop, no overflow. Actions grid measured 158px at 320/375/414 and 71px at 1280/1440, identical across the three phone widths because no breakpoint exists below `sm`.

---

## PART 3 — THE NOTE LAYER IS KEPT, AND WHAT IT DID IS RECORDED

**Where it lives, all present and byte-identical by blob OID on both refs:** `ReviewerNoteCard.tsx`, `reviewer-note.ts` (`a33f4bda4319`), `campaign-rules.ts` (`006c4d1a37c6`), `api/admin/reviewer-note/[clipId]/route.ts` (`d21dec0495be`), `api/admin/reviewer-note/batch/route.ts` (`a84f423c64ae`). **One change brings it back: `SHOW_BOT_NOTE_CARD` to `true`.**

**What it provided, written into the switch's own comment so a future round finds it rather than rebuilds it:**

* **A headline and a suggestion**, one of `likely_reject`, `look_closer` or `nothing_flagged`, with a confidence, never a score.
* **A failure-mode caveat on every certain rule.** A rule was only ever called certain alongside the way it could be wrong, printed every time it fired.
* **78 of 86 production rule lines are human-only, and they were SURFACED** under "For your eyes" rather than hidden, because a note silent on them would have been silent on most of the rulebook.
* **`cannot_evaluate` was never collapsed** into a rejection, and never into human judgement either. The naive port dumped all 78 human-only lines into "What I could not see"; the composer routes them by enforcement instead.
* **The metadata-health line attributed a pipeline gap to US, not to the clip.** With every live shadow row recording `captionPresent = false`, most notes said exactly that, and saying it plainly is what stopped an empty evaluation reading as a mark against a clipper.
* **The draft reply was id-free by construction**, never quoting the evaluator reason carrying a 19-digit sound id, asserted by a `/\d{7,}/` test.

Proven by BL-666's 43 of 43 tests and live on a real PENDING clip. Auto-reject was and remains off, and BL-664 is the reason: the reviewer overturn rate is **1.54%** (2 of 130) against R-2's **11.05%** machine false-rejection rate, roughly seven times the bar.

### The shadow recording is UNAFFECTED, and that was checked rather than assumed

BL-659 made `rule_shadow_decisions` persist and BL-666 added the note columns to it. **That write lives in the SUBMIT path**, `api/clips/route.ts` inside the `after()` callback at `:1114`, **not in this card**. `api/clips/route.ts` is byte-identical at `22711a444472`, `prisma/schema.prisma` at `31c6be00dedb`. Measured: **2,685 rows before and 2,685 after, newest row unchanged at `2026-08-29 19:40:02.975`** (no submit landed in the window, so no new row was due). **This switch changes a display, not a record.**

---

## PART 4 — EVERYTHING ELSE, AND WHO ELSE LOSES IT

`scripts/bl832-verify.mjs`, production build, real minted sessions, **24 passed, 0 failed**, on a row that arrives by scrolling. Nothing mutated.

```
PASS  BL-816: the list still pages at 30 · totalCount is still the TRUE total   7,171
PASS  BL-816: the appended row is byte-identical fetched alone at its own offset
PASS  BL-736: the picker answers for an appended clip                     14 destinations
PASS  BL-736: its hard blocks still refuse, by code   CLIP_HAS_EARNINGS, CLIP_HAS_MONEY_ROWS,
      CLIP_NOT_PENDING, DEST_PAST, DEST_PAUSED, DEST_PLATFORM_NOT_ACCEPTED, SAME_CAMPAIGN
PASS  BL-736: every refused destination still carries a REASON, not just a code
PASS  BL-744: the four labelled rates are still on the OWNER's response   clipper 0.20 · owner 0.1279
PASS  BL-815: a REVIEWER without the capability is still refused          HTTP 403, GET and POST
PASS  BL-814: the review route refuses an invalid ACTION, not the caller  HTTP 400
PASS  BL-666: both note routes still answer the owner and still agree byte for byte
PASS  BL-666: the note still carries its headline and suggestion          look_closer / low
PASS  BL-666: cannot_evaluate still not collapsed   blindSpots 0 · humanChecks 7
PASS  BL-666: the draft reply, when present, still carries no raw id
PASS  BL-831: the evidence routes are still present and untouched by this round
```

**Approve, Reject, Undo and Flag were proven present and reachable, never pressed.** Pressing one on a real clipper's clip moves money. Approve, Reject and Flag are photographed on the PENDING row at all five widths.

**A REVIEWER STOPS SEEING IT TOO, AND HE SHOULD KNOW THAT.** The switch is global. `CLIP_VIEW` is a **basic** reviewer capability, so every reviewer could see this card and **none can now**. Rendered as a real reviewer and confirmed: no card, and his page does not fetch it either. **The endpoint gate is unchanged and still answers him 200**; the page simply no longer asks. I kept it global for the reason the accessibility review gave: a role-conditional flag would make row structure differ by role, doubling the render proof for no gain, and reviewers work the owner's queue under his judgement. **If he wants reviewers to keep it, the constant becomes a function of the viewer's role and its two readers pass it in.**

**No clipper-facing surface changed and no clipper can see machine suspicion.** A CLIPPER is refused both note routes with **403**, and none of twelve forbidden field names (`ownerCpm`, `agencyFee`, `clientName`, `aiKnowledge`, `noteJson`, `noteText`, `noteSuggestion`, `wouldReject`, `draftReply`, `blindSpots`, `humanChecks`, `metadataHealth`) appears in his own clips payload. BL-531, BL-518 and BL-521 hold.

---

## PART 5 — THE ACCESSIBILITY REVIEW, THE GATES, AND THE MERGE

### It ran before the change, found 0 blocking items, and made the round better in three concrete ways

**It named the exact line the early return had to land on** (`ReviewerNoteCard.tsx:106`, after the last hook, before the `loading` branch), which is the difference between this working and every PENDING row reading "Loading bot note..." forever.

**It established that removing this card IMPROVES the heading tree rather than damaging it.** The `h4` at `:131` was the only heading a row ever had, and already 0-or-1 because `:107-112` returns a bare `<p>` when loading, none or error. It claimed a fourth-level subsection inside a document whose only other heading is the `h1` at `page.tsx:1451`, asserting two ancestor levels that exist nowhere, which is closer to F43 than to conformance. **1.3.1 never required headings**, 2.4.6 is vacuously satisfied, and 2.4.10 is AAA and was already unmet. The heading text was `Bot note — {campaign}`, byte-identical across several PENDING clips on one campaign, so a heading list could not distinguish rows anyway. Proven at all five widths: **0 headings inside any clip row, `h1` "Clip Review" still present.**

**It caught that BL-831's own render harness carried two assertions that invert the moment this lands** (`bl831-render.mjs:145` and `:148`, which asserted the Bot note DOES render). Both are flipped in this diff rather than left to fail silently later; BL-831's own proof is untouched, since its shot of the card rendering is in its report.

Also cleared: the card contributed **1 tab stop per PENDING row collapsed and 3 open** (the `<summary>`, the `<textarea>`, the Copy draft button), correcting the file's own comment which claimed zero; its only live region at `:223` loses its state, its writer and its trigger together, orphaning nothing, and the page-level regions at `page.tsx:1710`, `:2752` and `:2796` are untouched. Focus cannot be stranded because the flag is a module constant, so the card never mounts and no focused node is detached; BL-816's `firstNewRowRef` attaches to the row `<div>` at `page.tsx:1770`, never to card content. **No flash**, because the return fires on the first render before state settles. **Nothing becomes available nowhere else:** the note is persisted per clip in `rule_shadow_decisions`, both routes stay live, and fraud level, reasons and chips survive on the row. Only clip-specific draft wording is lost, equally for every user. **Silent removal is correct**; an sr-only trace would announce an absence on every row.

**Reported, pre-existing, deliberately NOT fixed here:** minor 1.3.1 label associations at `page.tsx:2281-2283` ("Client comment") and `:2507-2509` ("Reviewer message"); the shared `Modal` carrying no `role="dialog"`/`aria-modal`; the `EmptyState` `h3`; and two stale `h1` line numbers in comments at `ReviewEvidencePanel.tsx:161` and `ReviewerNoteCard.tsx:14`.

### Gates, honestly

`eslint` is present in the worktree, so the hooks gate is real. `npm ci` exit 0, `npx prisma generate` exit 0. No new UI was written, so the frontend-design skill's tokens are untouched: no new string, no new colour, no new class.

| gate | before any edit | after |
|---|---|---|
| `npx tsc --noEmit` | **exit 0, `grep -c "error TS"` = 0** | **exit 0, 0** |
| `npm run build` | **exit 0**, compiled in 45s | **exit 0**, compiled in 69s |
| `lint:hooks` | 0 errors, **11 warnings** | 0 errors, **11 warnings**, at the ceiling, unchanged |

Exit codes were echoed from `$?` into a log and never read through `tail`.

### Merged

| | |
|---|---|
| branch | `checkpoint/BL-832` @ **`2f3323b2`**, verified on origin by `safe-push` |
| merge commit | **`9e4a7849`**, `origin/main == local` verified by `safe-push` |
| conflicts | **none.** main never moved from `c54b2d60`, and the **merged tree OID equals the branch tree OID exactly** (`03e2e43c`) |
| BACKLOG | **168 sections before, 169 after**, `BL-832` x1, **0 conflict markers**, counted with `grep -c`, never piped to `head` |
| **`checkpoint/BL-723`** | **confirmed NOT an ancestor of main** |

---

## SAFETY

| | |
|---|---|
| the 6 money files plus `tracking.ts`, `campaign-era.ts` and `apify.ts` | **byte-identical by blob OID on BOTH refs**: `ac5be7de`, `797e2098`, `81a683c1`, `359bcbbe`, `61cef393`, `ef5cdae7`, `106e16ad`, `d66d4534` |
| `admin/clips/page.tsx`, `reviewer-note.ts`, `campaign-rules.ts`, `api/clips/route.ts`, both note routes, `prisma/schema.prisma`, `ReviewEvidencePanel.tsx` | **byte-identical on both refs** |
| schema | **no change**, no `prisma migrate`; `prisma generate` only. No index created |
| Apify | **no actor run**; `apify.ts` untouched, its BL-678 guards intact |
| payouts | **204 rows before and after, 0 with an `updatedAt` inside the round window** |
| earnings invariant | **0 violations** before and after |
| clip statuses | **8,342 clips, 6,975 approved, 16 pending, 1,345 rejected, 6 flagged, identical before and after** |
| `rule_shadow_decisions` | **2,685 rows before and after, newest row unchanged** |

**MOVED IN THE WINDOW AND NOT MINE, NAMED RATHER THAN SMOOTHED.** Approved earnings rose **$15,076.08 to $15,087.23**, $11.15. The approved count is **identical**, **0 clips were reviewed in the window**, and **zero `audit_logs` rows exist in the window at all** — no approval, no `SERVER_ERROR`, no `BUDGET_PROBE_BYPASS`. The cause is measured: **176 already-APPROVED clips took 176 new `clip_stats` snapshots**, which is the `:00` tracking cron recomputing earnings from grown view counts. My scripts pressed nothing, and the review route was called once with a deliberately invalid action that returned 400.

## WHAT COULD NOT BE MEASURED, AND WHAT I WOULD SAY NEXT

* **Production timings.** Everything was measured against a local production build pointed at the production database. The request census, the payload sizes, the DOM counts and the query counts are exact; the wall-clock settle times are not production numbers and are not claimed as any win.
* **A real screen reader.** DOM order, roles, headings, focus behaviour and tab stops are all measured; NVDA, JAWS and VoiceOver were not run.
* **The card at more than one PENDING row per width.** The pinned search returns exactly one, deliberately, so the two sides compare the same row. VIEW A covers four PENDING rows at once.
* **Next, if he wants it:** the polling shell is now comfortably the most expensive thing on this page, and `/api/accounts` still returns every column of every account to the Accounts page at 27.7 MB.
