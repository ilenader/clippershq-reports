# BL-776 — Mount the evidence panel, and bind the caveat to the number

**BL-773 and BL-775 were both pushed as branches and NEITHER was on main.** The analytics store and
the review panel existed only as unmerged refs. Nothing either round built was visible on the site.
This round merged both and mounted the panel. **The bundle.social ingest half remains UNVERIFIED —
it was never exercised against a live key, so the analytics card renders its absent state for every
clip today.**

---

## STEP 0 — the two branches, before merging

| branch | tip | ancestor of main? | files changed vs main |
|---|---|---|---|
| checkpoint/BL-773 | `bb1b1d5f` | NO | 6 (schema, ingest lib, route, card, tests, BACKLOG) |
| checkpoint/BL-775 | `1e7dc3d0` | NO | 4 (review-evidence lib, route, panel, BACKLOG) |

Clean-worktree baseline before either merge: `npx tsc --noEmit` exit 0, 0 errors.

BL-773 merged first, because BL-775's panel imports its card. Verified between merges.
`checkpoint/BL-723` was NOT merged.

**BACKLOG.md conflicted** (both rounds appended at the tail). Resolved as a **UNION**, stripping only
the conflict-marker lines: `grep -c '^## BL-'` = **139** (137 + 1 + 1), both `## BL-773` and
`## BL-775` present, `grep -c '<<<<<<<\|=======\|>>>>>>>'` = **0**. Nothing dropped.

---

## PART 1 — where it is mounted, and why that file

`src/app/(app)/admin/clips/page.tsx`, **line 2050**, immediately before the Actions row at 2052.

That is the owner's real review surface: the one page where a clip is actually approved or rejected.
A panel on any other page is a panel he would have to go and look for, and a measurement he has to go
and look for is one he will not look at while deciding.

Two placement decisions, both deliberate:

- **Before the controls, not after.** Measurements that render below the Approve button have already
  been skipped by the time they are read.
- **Outside the actions grid**, in its own `<div>`, not as a `col-span-2` child of it like
  `ReviewerNoteCard`. A grid child of the button row reads structurally as another control.

`ReviewEvidencePanel` now imports BL-773's `ClipAnalyticsCard`, so the two rounds are joined in the
one component rather than sitting in separate trees.

A new wrapper, `src/components/admin/ReviewEvidencePanelMount.tsx`, does the fetch. It carries **no
`aria-live` anywhere**, deliberately: the queue polls, `ReviewerNoteCard` already fetches per row,
and two polite regions per row across a poll would announce named people on a loop.

---

## PART 2 — the 6 hour figure, with the caveat welded to it

BL-775 measured the separating window at 6 hours, not 24. It also measured that **87.9% of approved
clips above 100,000 views are ALSO under 10% at 6 hours.** That is the trap: the signal fires loudly
on exactly the clips that deserve to be paid most.

A number in one element and its trap in a `<details>` below is a number that gets read alone. So the
figure and its qualifier are **one sentence**, and the qualifier is **bound to the platform**:

| platform | separation measured | the clause printed next to the number |
|---|---|---|
| Instagram | 66.4% vs 7.8% | "most approved clips above 100,000 views also show this, so on its own it is not evidence of bought views" |
| TikTok | 40.6% vs 6.3% | "separates approved from rejected only weakly, and most approved clips above 100k also show it, so treat it as a hint rather than a finding" |
| YouTube | 35.2% vs 37.5% | "the same for approved and rejected clips, so it says nothing about this clip either way" |
| anything else | not measured | "has not been measured as separating on this platform, so it says nothing about this clip either way" |

**YouTube does not separate at all** (35.2 vs 37.5 is noise), and the panel says so outright rather
than printing a figure that invites a conclusion the data does not support.

**The clip's own view count is printed in the same sentence.** A share without a denominator is not a
measurement: 0.0% of 6,725 views and 0.0% of 12 million views are not the same fact.

The `<details>` at the foot now holds **only methodology** — sample sizes, measurement dates, and what
"arrival share" means. No number lives there alone.

---

## PART 3 — no verdict, and nothing that could become one

- No score, no composite, no percentage likelihood, no colour-coded risk, no badge.
- The words *suspicious*, *likely*, *clean*, *no issues* and *nothing flagged* appear in **no
  rendered string**. The 5 grep hits for them are all source comments explaining why they are banned.
- **`fraudScore` is consumed nowhere:** 0 references across `review-evidence.ts`,
  `ReviewEvidencePanel.tsx` and `ReviewEvidencePanelMount.tsx`.
- **No `groupBy`, no `percentile`:** no clipper is ever aggregated into a peer band, so no clipper is
  ever judged by what other creators did.
- Closing line, verbatim: *"Measurements only. This does not recommend approving or rejecting. No
  score, no rating, nothing judged. The clipper sees none of this."*

---

## PART 4 — the empty panel, and when the curve is suppressed

**The curve is suppressed below 3 snapshots.** Two points cannot describe a shape, and a shape drawn
from two points is worse than no shape.

| population | clips | share |
|---|---|---|
| live clips | 5,357 | 100% |
| computable (3+ snapshots) | 5,105 | **95.3%** |
| suppressed (under 3) | 252 | **4.7%** |
| of those, zero snapshots | 39 | 0.7% |

The empty state is **one plain line naming the cause**: *"No measurements for this clip yet. It needs
more tracking snapshots before these numbers mean anything."* No heading, no icon, no colour, no
border treatment.

Never "Nothing flagged", never "Clean", never "No issues" — those are pass verdicts, and this panel
does not issue verdicts in either direction.

Two further honesty rules:

- **A fetch failure renders a DIFFERENT sentence** from an empty result. Merging them is exactly how
  a network error gets silently read as an innocent clip.
- **No loading skeleton.** A row of placeholder dashes reads as measured-and-blank.

---

## THE ACCESSIBILITY REVIEW FOUND TWO BLOCKING ITEMS, AND BOTH WERE VERDICT LEAKAGE

Both were this round's own rule turned back on it. Both are fixed, not noted.

**1. The mount asserted a fact about a named clipper that it had never looked up.** It passed
`analyticsConnected={false}`, but the review-evidence endpoint returns no analytics fields at all, so
that `false` was unconditional rather than measured. The panel's `Boolean()` collapsed *"we did not
look"* into *"he did not connect"*, and the card then printed **"This clipper has not connected one"
directly above the Reject button** — wrong, in the suspicious direction, for every clipper who has in
fact connected. Worse when `platform` was `null`: the clip may not be on TikTok at all and the panel
asserted a TikTok fact regardless. Now three states rather than two — `undefined` means **not looked
up** and renders *"Analytics were not looked up for this clip."* The mount passes nothing.

**2. Three server-side FAILURES were rendering as the innocent empty sentence.** `reason: "error"`,
`"db_unavailable"` and `"clip_not_found"` all fell through to *"it needs more tracking snapshots"* —
a cause that was never checked. `reason` was declared on the response and read nowhere. Separately,
`history.unavailable` (a read *failure*) was folded in with `submissions === 0` (a genuine
*absence*), so an unreadable clipper record also read as innocuous. Failures now take the error
sentence, and an unreadable history with no curve takes its own third sentence saying outright that
nothing was measured. Both existing strings are byte-identical; only the wrong inputs stopped
reaching them.

Cleared without change: **zero** `aria-live`, `role="status"`, `role="alert"` or `aria-busy` in
either file, and the stampede the earlier ruling feared is structurally impossible — the effect keys
on `clipId`, rows are keyed by clip id, and the 30-second poll re-renders without remounting.
Contrast **18.40:1**. Returning `null` while loading was confirmed correct rather than a gap. Two new
tab stops per row, both non-destructive disclosures, no focus stealing.

Carried forward, not fixed here: each row grows at its own settle time, pushing Approve and Reject
down under a reaching pointer. If that is ever addressed it must be a reserved `min-height` and
**never** a skeleton, which would reintroduce the measured-and-clean read.

---

## PART 5 — worked examples on real data

| case | clip | platform | snaps | views now | by 6h | what the owner sees |
|---|---|---|---|---|---|---|
| **A. rejected for bought views** | `cmphdclf90` | TikTok | 15 | 212,900 | 0.0% | the figure, plus "separates only weakly on TikTok, treat as a hint"; history shows 2 submissions, 2 rejected, 1 of them for bought views |
| **B. the viral trap** | `cmoback380` | Instagram | 123 | 12,139,743 | 0.1% | the same low figure on a legitimate 12M-view approved clip, printed with "most approved clips above 100k also show this" — the exact case that would have been misread |
| **C. YouTube** | `cmohwql0n0` | YouTube | 77 | 29,829 | 0.0% | "the same for approved and rejected clips, so it says nothing about this clip either way" |
| **D. too few snapshots** | `cmqkwlzh70` | YouTube | 2 | 6,725 | — | no curve at all; the plain uninformative line |

Case B is the point of the whole round. Under BL-775's panel as built, that clip's 0.1% would have
read as damning. It is a 12-million-view approved clip.

---

## SAFETY — everything that did not change

**Byte-identical by blob OID, on `origin/main` AND on this ref:**

| file | blob |
|---|---|
| `clip-earnings-writer.ts` | `ac5be7deb061` |
| `earnings-calc.ts` | `797e20985ad5` |
| `balance.ts` | `e887f80acfc7` |
| `tracking.ts` | `83ce4babfd39` |
| `clip-earnings-invariant-middleware.ts` | `61cef3939536` |
| `money-decimal.ts` | `ef5cdae757b9` |
| `campaign-era.ts` | `106e16ad7512` |
| `apify.ts` | `656bf4c0c408` |

- **No Apify actor run.** `apify.ts` untouched, its 5 named BL-678 guards intact.
- **Nothing clipper-facing:** 0 hits for `review-evidence`, `ClipAnalyticsCard` or `clip-analytics`
  across the clipper API routes and page trees. The route is gated by
  `requireOwnerOrCapability("CLIP_VIEW")`.
- **Nothing automatic.** No status is written, nothing auto-rejects (BL-518), and no machine
  suspicion reaches a clipper (BL-521).
- Schema additive and nullable via `prisma generate`, never `prisma migrate`.
- No API key logged, printed or committed at any point.

**Build:** `npx tsc --noEmit` exit 0 / 0 errors. `npm run build` exit 0. Hooks gate 0 errors,
**11 warnings against the ceiling of 11** — no new warning introduced.

**Shipped:** `pre-merge-BL-776` = `9d285c8c`, `post-merge-BL-776` = `3e96698b`, both on origin.
`origin/main == local HEAD (3e96698)` verified by `safe-push`.

**After the push, nothing changed** — identical to the pre-push baseline in every column, **including
the newest `updatedAt` on the whole clips table** (`2026-08-11 16:11:38.145`), which is the strongest
available statement that this round wrote nothing at all:

| metric | value |
|---|---|
| live clips | 5,358 |
| approved / pending / rejected | 4,394 / 34 / 924 |
| retired | 892 |
| **invariant violations** | **0** |
| approved earnings | $8,642.49 |
| payout rows | 166 |

No clip status changed, no earnings changed, no payout row touched. This round writes nothing to the
database at all — it is a read-only display surface.

---

## THE HONEST RESIDUAL

**The bundle.social pipeline is UNVERIFIED.** BL-773 built the store, the ingest and the field-status
recording, but no live key was ever available, so the ingest path has never run against the real API.
`ClipAnalyticsCard` therefore renders its absent state for every clip today, and it says so rather
than showing empty rows. Until a key is supplied and one clip is ingested end to end, the analytics
half of this panel is scaffolding.

What IS live and proven on real data: the clipper's own rejection history and the view-arrival
figure, on 5,105 of 5,357 clips.

**Rollback:** `git revert -m 1 <merge>`, or `reset --hard pre-merge-BL-776`.
