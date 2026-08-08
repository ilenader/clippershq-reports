# BL-736 — pending-clip campaign reassignment, built to BL-730's spec
**Branch** `checkpoint/BL-736` · **Base** `origin/main` `dd5d03f9` · 2026-08-08
**No clip was moved.** The demonstration is a 54-check harness plus a live read-only evaluation, not a production
move. `CLIP_CAMPAIGN_REASSIGNED` audit rows: **0**. Notifications sent: **0**. Worked in a clean worktree at
`C:/b736` because `C:/b575` is stale (`91b84410`) and dirty (77 paths); b575 was left exactly as found, real `npm ci`,
never a `node_modules` junction.
## PART 1 — The seven hard blocks, plus one BL-730 named that the brief did not
Every condition **refuses** with a named reason. None is a warning. Each is demonstrated **individually** in the
harness against the real exported rule set, so no block is merely inferred from a combined failure.
| # | Block | Code | Why it must refuse |
|---|---|---|---|
| 1 | **Era boundary would freeze the clip** | `DEST_ERA_WOULD_FREEZE` | The killer. Earnings frozen forever, no error anywhere |
| 2 | Destination PAST / PAUSED / COMPLETED / DRAFT / ARCHIVED / test | `DEST_PAST` etc. | 8 of 32 campaigns are PAST, so this is the likeliest misclick |
| 3 | Destination has spent its budget | `DEST_OVER_BUDGET` | A clip landing in a spent pool cannot earn |
| 4 | Platform not accepted (RULE 1b) | `DEST_PLATFORM_NOT_ACCEPTED` | BL-615 constrained pickers to accepted platforms |
| 5 | No CPM for that platform (RULE 1c) | `DEST_NO_CPM_FOR_PLATFORM` | The restamp would resolve **NULL** and the clip is unearnable |
| 6 | Clipper's account not on the destination | `CLIPPER_NOT_ON_DEST` | The clip lands where they were never admitted |
| 7 | Clipper at the destination's daily limit | `DEST_DAILY_LIMIT_REACHED` | The move itself is what would breach it |
| **+** | **Same URL already in the destination** | `DUPLICATE_URL_IN_DEST` | **BL-730 named this and the brief did not.** Both uniqueness constraints are per-campaign, so without it the transaction throws a raw unique violation instead of a sentence |
Clip-side, enforced server-side: **PENDING only**, **zero earnings**, and **zero money rows** — because `earnings`
reading `0.00` is not by itself proof nothing has been paid, so `AgencyEarning` and `MarketplaceCreatorEarning` are
counted too. `baseEarnings` alone is enough to refuse.
**Nothing BL-730 named was left out.** Its list was: dead/spent destination, era boundary, platform, no-CPM-for-platform,
account not approved, duplicate URL, and clip not PENDING / has earnings / has money rows. All seven plus the URL
constraint are implemented above.
## PART 2 — One atomic transaction
**Isolation: READ COMMITTED (the Prisma/Postgres default) plus a row-level `SELECT ... FOR UPDATE` on the clip.**
BL-730 concluded Serializable is not required, and this is why: the only row whose concurrent mutation could
invalidate the decision is the clip itself (someone approving it, or earnings landing on it), and the lock plus a
re-assert of PENDING, campaign identity and zero earnings covers exactly that. Serializable would add
retry-on-conflict noise to a single-row write for no additional guarantee.
**A mid-transaction failure leaves nothing.** Every write is inside the same `db.$transaction`, so a throw at any
point rolls back the campaign id, both CPM stamps, the TrackingJob and every repointed row **together**. A clip
belonging to two campaigns is not a reachable state. The full evaluation runs **outside** the transaction so a
refusal is cheap; it is then **re-asserted inside** under the lock, because anything read outside can change.
**Fields written, the complete list:**
```
Clip.campaignId                     TrackingJob.campaignId          Note.campaignId
Clip.cpmAtSubmissionDecimal         RuleShadowDecision.campaignId   ReviewerHelpRequest.campaignId
Clip.ownerCpmAtSubmissionDecimal    ClientClipFlag.campaignId       AuditLog (new)   Notification (new)
```
**Deliberately NOT written, each reason kept in code so nobody "helpfully" adds one:** `Clip.createdAt` (the
submission time is a fact; rewriting it to dodge the era boundary would be a lie, which is *why* block 1 exists);
the five `*AtApproval` snapshot fields (a PENDING clip has never been approved); `ownerCpmBackfilled*` (forensic
markers); the three earnings fields (zero by precondition, writable only via `writeClipEarnings`); and
**`ReviewerAuditLog.campaignId`** — that records what a reviewer did at the time, and history is not rewritten.
**The stamp and the locked share agree by construction, which is BL-539's failure and BL-570's $933.94.** Two
reasons. The two CPMs are resolved in **one** call against the destination and written **together** through the same
`enforceCpmStampInvariant` the three submission sites use (with a new `"reassign"` context). And
`guaranteeOwnerSplit` / `lockedOwnerShareDecimal` are **campaign** columns, not clip columns, so there is nothing on
the clip to fall out of step: after the move the clip reads the destination's share because it reads the destination.
The result is the shape a clip submitted directly to the destination would have.
## PART 3 — The owner UI
The campaign name on a clip row becomes a button **only when `isOwner && clip.status === "PENDING"`**; on any other
clip it stays the plain text it has always been. The picker lists **every** campaign: eligible ones selectable with
their CPM, ineligible ones **disabled and carrying the reason**. Hiding them was rejected because 8 of 32 campaigns
are PAST, so a filtered list would hide a quarter of the page and leave the owner guessing. The confirmation shows
the current campaign, the destination, the current CPM and the new CPM, and calls out a **drop** explicitly, since a
rate change is the entire point.
## PART 4 — What the clipper sees, and the notification
Every clipper-facing surface reads the clip's **live** `campaignId` rather than a copy, so all of them follow the
move by construction: the clips list and earnings both filter on `campaignId`, the payout balance is grouped by
`campaignId` in `computeCampaignBalances`, and the reviewer queue joins the campaign live. There is no denormalised
campaign name on the clip to go stale, which is why no surface needed changing.
**The clipper IS told, per BL-730's recommendation, and the rate leads when it drops.** Non-accusatory per BL-518 and
BL-521, and it says so outright rather than leaving them to wonder:
> *"We moved your clip to Campaign B. Campaign B pays $0.20 per 1,000 views instead of $0.50, so this clip will earn
> less than the campaign it was submitted to. Nothing you did caused this and the clip is still under review."*
When the rate is equal or higher it is one plain line with no drop language.
## PART 5 — The audit row
Every move writes `CLIP_CAMPAIGN_REASSIGNED` carrying the clip id, both campaign ids **and names**, the old clipper
and owner CPMs, the new clipper and owner CPMs, the platform, the actor, the timestamp, and the count of rows
repointed. BL-732 found the archive cascade wrote none and went unnoticed for three days.
## PART 6 — Evidence
**Harness `scripts/bl736-verify.ts`: 54 passed, 0 failed.** Each block on its own:
```
PASS BLOCK era: a clip older than the destination's era boundary is REFUSED
PASS BLOCK era: it is a refusal, NOT an allow-with-warning
PASS BLOCK era: a clip NEWER than the boundary is fine
PASS BLOCK status: PAST / PAUSED / COMPLETED / DRAFT / ARCHIVED / test campaign are refused
PASS BLOCK budget / platform / cpm / membership / daily / duplicate are each refused
PASS a clip with earnings, with baseEarnings only, or with money rows at 0.00 is refused
PASS both stamps resolve from the DESTINATION   PASS the clipper stamp is NOT the source's
PASS a CPM_SPLIT destination missing the owner rate is force-stamped, never left half (BL-539)
PASS createdAt is NEVER rewritten (the era block exists BECAUSE it cannot be)
```
**Live, read-only, reproducing BL-730's own measurement months later:**
```
DB now = 2026-08-08 15:25:23.208747+00
23 pending clips on non-test campaigns
32 live campaigns, 8 of them PAST
2 of 32 campaigns carry an era boundary
5 of 23 pending clips would freeze if moved into SOME era-carrying campaign
```
BL-730 measured **5 of 8**; today it is **5 of 23** — the same five clips, against a larger pending pool. The block is
not theoretical.
**Nothing was changed.** `CLIP_CAMPAIGN_REASSIGNED` audit rows **0**, reassignment notifications **0**, so no clip
moved. **Invariant 0 violations.** 161 payout rows, unchanged; no payout created, modified, approved or cancelled.
166 clips have a recent `updatedAt`, of which 154 are APPROVED clips written by the **tracking cron** between
`14:00:14` and `15:13:23` (the :00 tick) — background accrual, not this round; my only database access was
`run-select.js`, which refuses write keywords, and a read-only harness.
**Honest limit on this evidence:** a completed legal move is proven by the harness and by reading the transaction,
**not** by executing one on production. Moving a real clipper's clip to demonstrate the feature is not reversible
without another write, so it was not done. **No real clip was touched.**
**Money files byte-identical by blob OID on both refs:** `clip-earnings-writer` `ac5be7de`, `earnings-calc`
`797e2098`, `balance` `e887f80a`, `tracking` `83ce4bab`, `clip-earnings-invariant-middleware` `61cef393`,
`money-decimal` `ef5cdae7`, `campaign-era` `106e16ad`. **`cpm.ts` changed by exactly one union member**
(`| "reassign"`), which BL-730's spec required because the reassignment is a stamping site and must pass the same
half-stamp guard; `notifications.ts` gained one union member for the new notification type. Neither is a money file.
## Accessibility — commissioned, and it had NOT returned when this shipped
An `accessibility-lead` review of the picker and confirmation was commissioned and **did not return before this
round shipped.** It is reported as **not completed**, not implied handled. That matters here because BL-733's review
came back FAIL with nine blocking defects on a dialog I believed was sound.
**What reduces the risk, and it is specific rather than hopeful:** this dialog is a deliberate mirror of
`confirm-destructive.tsx`, which passed review only *after* those nine fixes, and it demonstrably carries each of
them: `role="dialog"` + `aria-modal`, a Tab trap **with the recovery branch** for focus escaped to `<body>`,
`tabIndex={-1}` on the scrollable panel, focus restore guarded on `isConnected`, Escape gated on busy and respecting
`isComposing`, errors as `role="alert"` **inside** the dialog, `aria-busy`, a portal to `document.body`, and
**no** `aria-hidden` background sweep (0 occurrences) — the sweep being the fix that silenced the toast region last
time. Blocked options are native disabled radios whose reason sits **inside the `<label>`**, so it forms part of the
accessible name rather than being merely adjacent.
**Two defects I found and fixed myself while waiting:** a bare `$0.20` beside a campaign name was ambiguous between a
rate and a total (now carries an sr-only "per 1,000 views"), and choosing a campaign silently inserted the
rate-comparison block (now announced politely, keyed on the chosen campaign so re-selection re-announces).
**Unreviewed and disclosed:** whether ~14 disabled-with-reason radios is the right cognitive load for this decision,
and whether the confirmation fully satisfies 3.3.4 for a change that alters a clipper's pay. Both were put to the
reviewer; neither has an answer yet.
## Gates, stated honestly
`npm ci` exit 0 (822 packages, no junction). `npx prisma generate` exit 0, **before** tsc. `tsc --noEmit` **0 errors**.
**`npm run build` exited 1 on the first run** and I am not hiding it: it printed "Compiled successfully" and *then*
failed type-checking with `Failed to type check` on the harness, because `next build` type-checks `scripts/` under a
wider config than `tsc --noEmit` used. That is exactly why a build is never judged from tsc alone or from the word
"compiled". Fixed (an over-narrow inferred mock type) and the **second run exited 0**. BL-348 hooks gate **0 errors,
11 warnings — at the limit of 11**, eslint **v9.39.4 confirmed present**.
