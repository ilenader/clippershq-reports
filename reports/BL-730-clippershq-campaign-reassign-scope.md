# BL-730 — Can a PENDING clip be reassigned to a different campaign, and what would it touch?

**AUDIT ONLY. READ ONLY. Nothing was built, nothing was reassigned, no code, data or money changed.**
**2026-08-07 · Base:** `main @ 6688bad0` · **Branch:** `checkpoint/BL-730` · one markdown file, no source diff.
Every DB figure is cast `::text` against DB `now()`. Only `run-select.js` was used, which refuses write keywords.

---

# THE VERDICT, IN ONE LINE

**PENDING-only campaign reassignment is SAFE TO BUILD, but ONLY as a single transaction that also restamps the CPM, repoints two dual-bound row types, and hard-blocks six destination conditions — the naive `UPDATE clips SET "campaignId"` is unsafe, and would silently pay the clipper at the wrong rate or freeze their clip forever.**

Two of those failure modes are not hypothetical. Measured today: **5 of the 8 live PENDING clips would be permanently frozen** by a move into one of the two campaigns that carry an era boundary, and **8 of 14 live campaigns are PAST**, so "moved into a campaign that can never pay" is the single most likely misclick.

---

# PART 0 — EVERYTHING BOUND TO A CAMPAIGN ON A CLIP

## 0.1 Fields on the Clip row itself

`prisma/schema.prisma`, Clip model begins line 835.

| Line | Field | On reassignment |
|---|---|---|
| 838 | `campaignId String` | **MUST CHANGE.** The FK relation at :1001 (`onDelete: Cascade`) follows it. |
| 958 | `cpmAtSubmissionDecimal Decimal? @db.Decimal(10,4)` | **MUST CHANGE (restamp).** See PART 2 — this is the heart of it. |
| 959 | `ownerCpmAtSubmissionDecimal Decimal? @db.Decimal(10,4)` | **MUST CHANGE (restamp), together with 958 or not at all.** |
| 892 | `feePercentAtApproval Float?` | **MUST NOT CHANGE.** NULL on a PENDING clip; it is stamped at approval, which has not happened. |
| 898 | `streakBonusPercentAtApproval Float?` | **MUST NOT CHANGE.** NULL while PENDING. |
| 975 | `pricingModelAtApproval String?` | **MUST NOT CHANGE.** NULL while PENDING. |
| 976 | `minViewsAtApproval Int?` | **MUST NOT CHANGE.** NULL while PENDING. |
| 977 | `maxPayoutPerClipAtApproval Decimal?` | **MUST NOT CHANGE.** NULL while PENDING. |
| 978 | `ownerUserIdAtApproval String?` | **MUST NOT CHANGE.** NULL while PENDING. |
| 964 | `ownerCpmBackfilledAt` / `ownerCpmBackfillSource` | **MUST NOT CHANGE.** Forensic audit of the BL-539-era backfill; rewriting it would destroy the record of which cohort a clip belonged to. |

**The `...AtApproval` block is exactly why PENDING is the tractable boundary.** Schema comment at :971-973 states it outright: *"PENDING/REJECTED clips have null snapshots and fall through to current campaign value"*. A PENDING clip carries no approval-time economics to reconcile. An APPROVED clip carries six, and reconciling them is a different and much harder round.

## 0.2 The two campaign-scoped uniqueness constraints. These can make the write FAIL.

| Line | Constraint | Consequence |
|---|---|---|
| 1012 | `@@unique([clipUrl, campaignId])` | If the same URL already exists in the destination campaign, the reassignment **throws a unique violation**. |
| 1017 | `uq_clip_norm_open_per_campaign` on `("campaignId","normalizedUrl")` WHERE open | Same, on the normalized URL, against any OPEN clip in the destination. |

**This is a real and likely case:** the clipper submitted to the wrong campaign, was told, and re-submitted correctly to the right one. Now both exist and the owner tries to move the first. The write fails. **The reassignment must pre-check both and refuse with a plain message**, not surface a Prisma constraint error.

## 0.3 Rows that carry BOTH `clipId` and `campaignId` — the danger set

35 models in the schema carry a `campaignId`. Nine of them **also** carry a `clipId`, which means they store the campaign **independently of the clip** and will keep pointing at the OLD campaign after a naive update. **This is the "half-belongs to two campaigns" shape.**

| Model | schema line (clipId / campaignId) | Exists on a PENDING clip today? | On reassignment |
|---|---|---|---|
| **TrackingJob** | 1115 / 1116 | **YES — 8 of 8** | **MUST REPOINT.** `clipId` is `@unique`, one job per clip. |
| **RuleShadowDecision** | 2847 / 2848 | **YES — 3 rows** | **Decide explicitly.** It is an audit of a decision made *under the old campaign's rules*. |
| **AgencyEarning** | 1047 / 1046 | No (0 rows) | Cannot exist while PENDING. **Assert zero and abort if not.** |
| **MarketplaceCreatorEarning** | 2710 / 2712 | No (0 rows) | Same. |
| **MarketplacePlatformEarning** | 2735 / 2736 | No (0 rows) | Same. |
| **Note** | 1724 / 1723 | Not measured | Owner/admin note. **Repoint or leave**, but decide. |
| **ClientClipFlag** | 1976 / 1977 | Not measured | A CLIENT of the OLD campaign flagged it. **Must NOT silently move into the new client's view.** |
| **ReviewerHelpRequest** | 1632 / 1634 | Not measured | Reviewer scope is campaign-scoped. **Repoint or close.** |
| **ReviewerAuditLog** | 1677 / 1678 | Not measured | **MUST NOT CHANGE.** It is history: the event genuinely happened under the old campaign. |

**`ClientClipFlag` is the one with a privacy edge**, not just a correctness edge: a flag written by campaign A's client, silently carried into campaign B, exposes one client's comment inside another client's surface.

## 0.4 Rows that carry `clipId` only — these follow the clip for free

`ProposedClipDecision`, `ClipSnapshotChange`, **`ClipStat`**, `MarketplaceClipPost`.

**`ClipStat` has no `campaignId`** (verified by parsing every model body, not by grep — a naive grep hits `TrackingJob`'s field on the next line and reports a false positive). Its 163 rows on today's pending clips need no action: they are view history for a URL, and the URL does not change.

## 0.5 Derived values with no column of their own

| Thing | Where | On reassignment |
|---|---|---|
| **Era boundary** | `campaign-era.ts:85-108`, applied at `tracking.ts:1883` | **Recomputed automatically from the new `campaignId` — and that is the danger, not the safety.** PART 3.5. |
| **Daily submission count** | `clipper-submit-core.ts:326-331` | Counts `clips WHERE userId + campaignId + createdAt >= startOfDay`. **The moved clip retroactively joins the destination's count for its original submission day.** |
| **Campaign spend / pool cap** | `balance.ts:261-263, 384-398` | Derived from APPROVED clips. A PENDING clip contributes nothing, so no spend moves at reassignment time. |
| **Live CPM fallback** | `cpm.ts:160-182` | Only reached when the frozen stamp is NULL. It is not, so it does not save you. PART 2. |

---

# PART 1 — DOES PENDING GENUINELY MAKE THIS TRACTABLE? YES ON MONEY, NO ON ROWS.

Measured at `db_now = 2026-08-07 11:58:34.969008+00`, and again at `11:58:47.401696+00` (a clip was submitted between the two, so the count moves 7 to 8 — the platform is live).

## 1.1 Money: clean. No finding.

| Check on PENDING, not deleted | Result |
|---|---|
| Clips | 7 (then 8) |
| **Non-zero `earnings`** | **0** |
| **Non-zero `baseEarnings`** | **0** |
| **Non-zero `bonusAmount`** | **0** |
| Sum of `earnings` | **$0.00** |
| `AgencyEarning` rows | **0** |
| `MarketplaceCreatorEarning` rows | **0** |
| Oldest pending | 2026-06-27 16:07:07.146 |

**No pending clip has non-zero earnings, so there is no finding to raise here.** No accrual, no payout exposure, no spend contribution. The oldest pending clip is six weeks old and still at zero, which confirms the property holds over time rather than only for fresh submissions.

## 1.2 Rows: NOT clean. Pending clips already carry state.

| Attached to the 8 pending clips | Count |
|---|---|
| **ClipStat rows** | **163**, across 6 of the 8 clips |
| **TrackingJob rows** | **8** — every pending clip has one |
| **RuleShadowDecision rows** | **3** |

**So "PENDING means nothing has happened yet" is false.** Tracking starts at submission (`actions/clips.ts:118+` creates the ClipStat and the job inside the same transaction as the clip). A pending clip has been polled, has view history, and has a live cron job pointing at a campaign.

* **ClipStat: no action needed.** No `campaignId`, and views are a property of the URL.
* **TrackingJob: MUST be repointed in the same transaction.** Leaving it is an orphan pointing at the old campaign, and `tracking.ts` reads era and budget context from the job's campaign.
* **RuleShadowDecision: decide explicitly, do not ignore.** BL-659 created it to measure the false-rejection rate of the auto-reject shadow. Repointing it silently corrupts that measurement by attributing campaign A's decision to campaign B. **Recommendation: leave it pointing at the old campaign and add a `reassignedFromCampaignId` marker, or exclude reassigned clips from the shadow denominator.** It is an audit table, not live state.

## 1.3 Verdict on the boundary

**PENDING is the right boundary, and it is right for a specific reason: the six `...AtApproval` snapshot fields are all NULL.** That is what removes the hard part. But PENDING does **not** mean "no attached rows", and any spec written on that assumption ships an orphaned tracking job.

---

# PART 2 — THE STAMPED CPM. THIS IS WHERE IT GOES WRONG SILENTLY.

## 2.1 The precedence that makes a naive move pay the wrong rate

`src/lib/cpm.ts:178-181`:

```ts
return {
  clipperCpm: clipperOverride ?? frozenClipper ?? live.clipperCpm,
  ownerCpm:   ownerOverride   ?? frozenOwner   ?? live.ownerCpm,
};
```

**The frozen stamp BEATS the live campaign CPM.** `frozenClipper` is `clip.cpmAtSubmissionDecimal`, stamped at submission and non-NULL on every normally-submitted clip.

**Therefore: move a clip from a $0.50 campaign into a $0.20 campaign without restamping, and it sits in the new campaign and earns $0.50.** No error, no warning, no log. The clipper is overpaid, the destination campaign's budget drains at a rate its own configuration does not explain, and the row is exactly the "permanently ambiguous" shape BL-539 identified: a stamp that disagrees with its campaign.

The reverse is worse for the clipper: $0.20 into $0.50 keeps paying $0.20 while every surface shows the campaign at $0.50.

**Restamping is not optional. It is the whole feature.**

## 2.2 How the stamp is set at submission — THREE sites, not one

| # | Resolve | Enforce | Write |
|---|---|---|---|
| 1 | `src/actions/clips.ts:99-101` | none | `:114-115` |
| 2 | `src/lib/clipper-submit-core.ts:544-546` | `:547-549` | `:557` |
| 3 | `src/lib/owner-submit-core.ts:256-260` | `:257-260` | `:287` |

All three call the same resolver, `getCampaignCpmForPlatform(campaign, platform)` (`cpm.ts`), which **is** cleanly reusable. Two of the three then call `enforceCpmStampInvariant` (`cpm.ts:195-224`).

**Can the path be reused for a restamp? Partly, and the gap is precise.**

* `getCampaignCpmForPlatform` — **reuse directly.** Pure, takes campaign + platform, no submit coupling.
* `enforceCpmStampInvariant` — **reuse, with a one-word change.** Its `context` parameter is a closed union `"regular-submit" | "owner-submit" | "marketplace-submit"` (`cpm.ts:201`). A restamp needs `"reassign"` added. Because the union is closed, forgetting it is a **TypeScript error at the call site**, not a silent miss. That is the good news.
* The write itself — **there is no shared write helper.** Each of the three sites inlines its own `tx.clip.create({ data: { cpmAtSubmissionDecimal, ownerCpmAtSubmissionDecimal } })`. A restamp is a fourth inlined write.

**Recommendation: extract one `resolveStampForCampaign(campaign, platform, context)` returning `{ clipperCpm, ownerCpm }`, used by the restamp, and leave the three existing submit sites alone in this round.** Refactoring three live submit paths to prove a fourth is correct is a larger and riskier change than the feature.

## 2.3 What a half-completed restamp produces

**Exactly BL-539's ambiguous row.** The concrete half-states:

1. `campaignId` moved, CPM not restamped → wrong rate, silent. (2.1.)
2. Clipper CPM restamped, owner CPM not → on a `CPM_SPLIT` campaign this is the asymmetry `enforceCpmStampInvariant` exists to catch. Uncaught, the owner's share is computed from the OLD campaign's split against the NEW campaign's budget. BL-570 measured $933.94 of related exposure.
3. CPM restamped, `campaignId` write failed → the clip stays in the old campaign paying the *destination's* rate. The worst of the three, because the clip looks untouched.

**All three are prevented by one thing and only one thing: a single transaction.** PART 5.

## 2.4 Differing fee structures and locked shares between source and destination

* **BL-630 ghost platform fee.** `platformFeePct` is a campaign column, read by the pool cap at `balance.ts:303-307`. It is **not** stamped on the clip and is immutable after campaign creation. A reassigned clip therefore inherits the destination's fee automatically and correctly, **with no clip-side field to update**. This one is safe by construction.
* **BL-625 derived per-platform CPMs.** `getCampaignCpmForPlatform` resolves `cpm{Platform}Clipper` first and falls back to legacy `clipperCpm`/`cpmRate`. **The restamp must resolve against the DESTINATION campaign and the CLIP'S OWN platform.** If the destination has no CPM for that platform, the resolved stamp is NULL and the clip becomes unearnable. Submit blocks this at `clipper-submit-core.ts:343+` (RULE 1c); **reassignment must block it too.**
* **Locked owner share.** `guaranteeOwnerSplit` + `lockedOwnerShareDecimal` (`balance.ts:384-398`) are campaign properties, not clip properties. A clip moving from a non-guaranteed campaign into a guaranteed one lands inside the destination's pool cap automatically. **Correct by construction**, but it means the destination's clipper pool now has one more claimant, which is a budget question (PART 3.4), not a stamping question.

---

# PART 3 — THE CAMPAIGN-SCOPED GATES A REASSIGNMENT BYPASSES

Submission runs a gate at `src/lib/clipper-submit-core.ts:303-345`. **A reassignment enters a campaign through the back door and passes none of it.** Each below is that gate's own rule, restated as a reassignment decision.

## 3.1 Daily submission limit — **WARN, do not block**

`clipper-submit-core.ts:322-331`. `maxPerDay = ClipLimitOverride.maxClipsPerDay ?? campaign.maxClipsPerUserPerDay ?? 3`, counted over `(userId, campaignId, createdAt >= startOfDay)`.

The moved clip retroactively joins the destination's count **for its original submission day**, which may be weeks ago. It can push a historical day over its cap, which nothing re-reads and nothing can act on.

**Blocking would punish the clipper for the owner's correction.** The clip already exists and the daily cap exists to throttle *new* submissions. **Warn the owner that the destination cap is already met today, and proceed.**

## 3.2 Per-campaign minimum withdrawal (BL-728) — **WARN**

BL-728 made the withdrawal minimum settable per campaign. It is a floor on the amount requested, not on eligibility, and it does not touch the clip. **But a clip moving into a campaign with a $50 minimum, when the clipper holds $12 there, is work they cannot cash out for a long time.** The owner should see the destination's minimum on the confirmation. No block.

## 3.3 Campaign eligibility — **BLOCK**

Campaign membership runs through `CampaignAccount` (`@@unique([clipAccountId, campaignId])`) and `CampaignAdmin`. **If the clipper's account is not approved on the destination, the clip lands somewhere they were never admitted.** They may not even be able to see it. Block, and tell the owner to approve the account first.

## 3.4 Destination budget and pool cap — **WARN, do not block**

`clipper-submit-core.ts:318-320` refuses a *new* submission into an over-budget campaign. A PENDING clip contributes **$0.00** to spend (PART 1.1), so reassignment moves no money and cannot push a budget over on its own.

The exposure is deferred: on approval, the clip begins earning against the destination's budget and pool cap. **That is the destination's L1 budget hard-lock's job**, and it already handles it: at cap the campaign auto-pauses. **Warn with the destination's remaining budget; block only in the fully-spent case, which 3.5 covers anyway.**

## 3.5 Destination status and the ERA BOUNDARY — **BLOCK. This is the finding.**

`tracking.ts:1883-1893`:

```ts
const budgetWindowStart = await getCampaignEraBoundary(clip.campaignId);
const isOldWindowClip = !!(budgetWindowStart && clip.createdAt &&
  new Date(clip.createdAt).getTime() < new Date(budgetWindowStart).getTime());
```

**Reassignment changes `campaignId`. It does NOT change `createdAt`.** So the clip's original submission time is compared against the DESTINATION campaign's era boundary. A clip created before the destination's last AUTO-pause-to-resume is **instantly and permanently `isOldWindowClip`: views keep tracking, earnings are frozen forever.** No error. The clipper watches views climb and money never move.

**Measured, not hypothetical**, at `db_now = 2026-08-07 11:59:03.36006+00`:

| | |
|---|---|
| Campaigns carrying an era boundary | **2** of 14 live |
| **Pending clips that would freeze if moved into one** | **5 of 8** |

And the destination-status distribution at `11:59:14.651735+00`:

| Status | Count |
|---|---|
| **PAST** | **8** |
| ACTIVE | 5 |
| PAUSED | 1 |

**8 of 14 live campaigns are PAST.** A picker listing every campaign makes the most likely misclick the one that renders the clipper's work permanently unearnable.

**BLOCK: PAST, COMPLETED, archived, fully-spent, and any destination whose era boundary is later than the clip's `createdAt`.** The last is the non-obvious one and the one a build round will miss.

**PAUSED: warn, do not block.** A manual pause is reversible and is a normal state for a campaign the owner is actively managing.

## 3.6 Platform compatibility (BL-615) — **BLOCK**

Two separate rules at submit, and both must be re-run:

* `clipper-submit-core.ts:338-342` (RULE 1b): the URL's platform must be in `campaign.platform` (a comma-separated list, matched case-insensitively). **A TikTok clip moved into an Instagram-only campaign is invalid.**
* `clipper-submit-core.ts:343+` (RULE 1c): the destination must have a **CPM set for that platform**. Without it the restamp resolves NULL and the clip is unearnable — a second, quieter way to destroy the clipper's work.

Only 1 of 5 ACTIVE campaigns is single-platform, so most moves will pass. **The block still has to exist**, because the case that fails is the one that silently costs a clipper everything.

## 3.7 Summary

| Gate | Decision |
|---|---|
| Destination is PAST / COMPLETED / archived / fully spent | **BLOCK** |
| Destination era boundary is later than `clip.createdAt` | **BLOCK** |
| Clip platform not accepted by destination | **BLOCK** |
| Destination has no CPM for the clip's platform | **BLOCK** |
| Clipper's account not approved on destination | **BLOCK** |
| URL already exists in destination (either unique constraint) | **BLOCK** |
| Clip is not PENDING, or has non-zero earnings, or has any Agency / Marketplace earning row | **BLOCK** |
| Destination is PAUSED | WARN |
| Destination daily cap already met | WARN |
| Destination budget nearly exhausted | WARN |
| Destination CPM is lower than the source | **WARN, prominently** |
| Destination minimum withdrawal is higher | WARN |

---

# PART 4 — WHAT THE CLIPPER EXPERIENCES

## 4.1 What visibly changes

The clip's campaign name and thumbnail on `/clips`; which campaign it is grouped under on `/earnings`; the CPM shown against it; and, once approved, the rate it earns at. Their submission history now shows a clip they submitted to campaign A sitting under campaign B.

## 4.2 Should they be told? **Yes, and the rate is the reason.**

The owner's intent is benign, but **a clip moving from a fifty-cent campaign to a twenty-cent one halves what the clipper expected to earn.** Discovering that silently, after the fact, does not read as a correction. It reads as being cheated, and it is the exact trust failure BL-518 and BL-521 were written about.

**Recommendation: notify on every reassignment, and lead with the rate when it drops.**

Draft, in the plain non-accusatory register those rounds set:

> **Your clip was moved to the right campaign**
> You submitted this clip to Campaign A, and it fits Campaign B, so we moved it across for you. Nothing you did was wrong and your clip is still in review.
> Campaign B pays **$0.20 per 1,000 views** instead of $0.50, so this clip will earn less than the campaign you submitted it to. If that is not what you wanted, reply here and we will sort it out.

Three properties matter. It names the cause and locates it with **us**. It states the rate change as a **fact before** the clipper can discover it. It offers a route back, because the owner may have moved the wrong clip.

**When the rate is equal or higher, the notification can be one line and cheerful.** When it drops, the drop is the headline.

**Do not notify silently-never.** A reassignment the clipper only discovers from a smaller payout is a support ticket that starts from mistrust.

## 4.3 Platform compatibility, restated as clipper experience

Covered in 3.6 as a block. Stated here because it is the clipper's account and URL that become invalid: if a move is allowed into a campaign that does not accept their platform, the clip is not merely mispriced, it is **unpostable and unearnable**, and they were never told why.

---

# PART 5 — FAILURE MODES, WORST FIRST

| # | Failure | Why it is this bad | Prevented by |
|---|---|---|---|
| **1** | **Clip frozen forever by the destination's era boundary** | Silent. Views climb, earnings never move, no error anywhere. `createdAt` is not changed by the move, so it can never resolve itself. 5 of 8 pending clips are exposed today. | **BLOCK** on `era boundary > clip.createdAt` (3.5). This is the check a build round will forget. |
| **2** | **Moved but not restamped: earns at the old campaign's rate** | Silent, and it is money. `frozen ?? live` means the stale stamp wins (`cpm.ts:178-181`). Produces BL-539's permanently ambiguous row. | Restamp **inside the same transaction**; assert post-write that the stamp equals the destination's resolved CPM. |
| **3** | **Half-restamp: clipper CPM moved, owner CPM not** | On `CPM_SPLIT`, the owner's share is computed from the old split against the new budget. BL-570 measured $933.94 of related exposure. | `enforceCpmStampInvariant` (`cpm.ts:195`) with a new `"reassign"` context. Closed union, so omitting it is a compile error. |
| **4** | **Restamped but `campaignId` write failed** | Worst to diagnose: the clip looks untouched in the old campaign but now pays the destination's rate. | Single transaction. Nothing else prevents it. |
| **5** | **Moved into a PAST or fully-spent campaign** | The clipper's work is permanently unearnable. 8 of 14 live campaigns are PAST, so this is the most likely misclick. | **BLOCK** on status and on spend-vs-budget. |
| **6** | **Moved into a campaign with no CPM for that platform** | Restamp resolves NULL, clip unearnable. Quieter than #5 because the campaign looks healthy. | **BLOCK**, re-running RULE 1c (`clipper-submit-core.ts:343+`). |
| **7** | **Orphaned TrackingJob** | The job keeps the old `campaignId`, so tracking reads the wrong campaign's era and budget context. All 8 pending clips have one. | Repoint `TrackingJob.campaignId` in the same transaction. |
| **8** | **Unique-constraint violation on write** | The clipper re-submitted correctly, so the URL exists in the destination. A raw Prisma error reaches the owner. | Pre-check `@@unique([clipUrl, campaignId])` (:1012) and `uq_clip_norm_open_per_campaign` (:1017); refuse with a plain message. |
| **9** | **`ClientClipFlag` carried into the destination** | Campaign A's client comment becomes visible inside campaign B's client surface. A privacy edge, not just a correctness one. | Decide explicitly: leave pointing at the old campaign, or clear. Never carry silently. |
| **10** | **`RuleShadowDecision` repointed, corrupting BL-659's measurement** | The false-rejection rate is attributed to the wrong campaign. 3 rows exist today. | Leave it, and exclude reassigned clips from the denominator. |
| **11** | **Double-counting across both campaigns** | Would be severe, but **structurally hard here**: `campaignId` is a single scalar, not a join table, so a clip cannot be in two campaigns at once. Attached money rows (`AgencyEarning`, marketplace) are all `clipId @unique`. | Assert zero money rows before the write; the schema does the rest. |
| **12** | **Clipper sees a silent rate cut** | Not a data bug. It is the trust failure. | Notify, leading with the rate drop (PART 4.2). |

## 5.1 Atomicity

**It must be one transaction.** Failure modes 2, 3, 4 and 7 are all half-completions, and there is no compensating action for any of them because the clip looks plausible in every half-state.

**Recommended shape:** a single `db.$transaction` performing, in order: (1) re-read the clip `FOR UPDATE` and re-assert PENDING + zero earnings + zero money rows, because the gate was evaluated against a read that is now stale; (2) write `campaignId` + both CPM stamps together; (3) repoint `TrackingJob.campaignId`; (4) write an audit row recording source campaign, destination campaign, old stamps and new stamps.

**Serializable is not required.** No read-modify-write on a shared counter is involved, unlike the payout path BL-696 protects. The default isolation plus a row-level re-read is sufficient, and it avoids lengthening a transaction class that money paths depend on.

**Rollback if it fails midway: the transaction aborts and nothing changed.** That is the entire point of the single transaction. The audit row from step 4 is what makes a *deliberate* reversal possible afterwards: it stores the old stamps, so an undo is another reassignment back with the recorded values, not a guess.

---

# PART 6 — THE BUILD SPEC

**One line: PENDING-only campaign reassignment is safe to build as a single transaction that restamps the CPM, repoints the TrackingJob, and hard-blocks seven destination conditions; it is unsafe as anything less.**

## 6.1 Fields written, and only these

| Target | file:line today | Write |
|---|---|---|
| `Clip.campaignId` | `schema.prisma:838` | destination id |
| `Clip.cpmAtSubmissionDecimal` | `schema.prisma:958` | `getCampaignCpmForPlatform(destination, clip.platform).clipperCpm` |
| `Clip.ownerCpmAtSubmissionDecimal` | `schema.prisma:959` | same resolver's `ownerCpm`, passed through `enforceCpmStampInvariant` with a new `"reassign"` context (`cpm.ts:195-224`) |
| `TrackingJob.campaignId` | `schema.prisma:1116` | destination id |
| New audit row | new table | clipId, from, to, old stamps, new stamps, actor, timestamp |

**Explicitly NOT written:** every `...AtApproval` field (`:892, :898, :975-978`) — all NULL while PENDING; `ownerCpmBackfilled*` (`:964`) — forensic history; `createdAt` — see 6.4; `ClipStat` — no `campaignId`; `ReviewerAuditLog` — history.

## 6.2 Blocks and warnings

Exactly the table in 3.7. The seven blocks are the feature; the warnings are the confirmation screen.

## 6.3 What the clipper sees

A notification on every reassignment, **leading with the rate when it drops** (4.2 draft). Plain, non-accusatory, offering a route back.

## 6.4 The one thing that is unsafe even for PENDING clips, named plainly

**The era boundary compares `clip.createdAt` against the DESTINATION campaign's boundary, and `createdAt` is not something a reassignment may honestly rewrite.**

Rewriting it to "now" would unfreeze the clip but would also falsify the submission record, reset the daily-limit window, and break every "old window" audit that depends on it. **So the only safe answer is to BLOCK the move**, which means some legitimate corrections are simply not available: if the destination has an era boundary later than the clip's submission, the owner cannot move it there at all, and must reject the clip and ask the clipper to resubmit.

**That limitation should be stated to the owner in the UI rather than hidden**, because "why can I not move this one" will otherwise become a support question about his own tool.

## 6.5 Proofs required before merge

1. Reassign a PENDING test clip between two test campaigns with **different** CPMs; assert the stamp equals the destination's resolved CPM and that computed earnings on approval use the new rate.
2. Assert `TrackingJob.campaignId` moved with the clip, and that no row anywhere still carries the old campaign except `ReviewerAuditLog` and (by decision) `RuleShadowDecision`.
3. Force a mid-transaction failure and assert **nothing** changed: `campaignId`, both stamps and the job all original.
4. Attempt every one of the seven blocked cases and assert each refuses with a plain message, **including the era-boundary case**, which today would affect 5 of 8 pending clips.
5. Attempt a reassignment into a campaign already holding the same URL and assert a plain refusal, not a Prisma constraint error.
6. Full-population before-and-after: no clip's earnings, status or campaign changed except the one under test; earnings invariant 0 violations.
7. The 6 money files, `tracking.ts` and `campaign-era.ts` byte-identical by blob OID. **Nothing in this spec requires editing any of them.**

## 6.6 Rollback

`git revert -m 1 <merge>` removes the ability to reassign. **Clips already reassigned stay reassigned**, which is correct: they were moved deliberately and their stamps are consistent with where they now live. The audit row from 6.1 is what makes a deliberate reversal possible, by replaying the recorded old values.

---

# WHAT COULD NOT BE MEASURED

* **`Note`, `ClientClipFlag`, `ReviewerHelpRequest` counts on pending clips were not queried.** The three high-volume attachments were (ClipStat 163, TrackingJob 8, RuleShadowDecision 3). These three are lower-volume and their handling is a decision rather than a measurement, but **the build round should count them before writing the transaction**.
* **No reassignment was performed**, so every claim about the resulting state is derived from the code paths cited, not observed. That is the intended limit of an audit-only round.
* **The `_enf` / `_enforce_OS` wrappers at the three stamp sites were read at their call sites, not line-by-line through every branch.** `enforceCpmStampInvariant` itself was read in full (`cpm.ts:195-224`).
* **The accessibility review was not run**, because this round writes one markdown file and no UI. The reassignment UI is a build-round concern and **must** be reviewed then: it is a destructive, consequential confirmation with an async impact check, which is exactly the shape BL-728 found traps in (a document-level non-stack-aware Escape, and focus landing on a destructive control before its justifying number has loaded).
