# BL-732 — did archiving WinGram auto-void pending payouts? Yes. Read-only audit.
**ONE LINE: archiving caused it. $82.13 was voided from 2 clippers, and $165.77 is owed to 20 clippers on WinGram.**
Audited at `ab455ac7`, DB now `2026-08-07 15:36:28 +00`. **Nothing was changed** — no payout status, balance, archive
state or campaign. Read-only SQL only. Handles redacted to stable refs the owner can map privately; **no wallet address
was selected or printed, not even partially.**
## PART 1 — The owner's hypothesis is CORRECT, and the code says so plainly
The archive action is the `DELETE` handler at `src/app/api/campaigns/[id]/route.ts:904-992`. **All six side effects:**
`933-941` campaign `isArchived=true` + `archivedAt` + `archivedById` + `status → PAUSED`; `942-954` `recordStatusChange`
audit row; `957-960` **all tracking jobs deactivated**; **`964-967` `payoutRequest.updateMany` → `status:"VOIDED"`,
`rejectionReason:"Campaign archived"` for every `REQUESTED`/`UNDER_REVIEW`/`APPROVED` row**; `976` listings pause; `981`
`logCampaignEvent(ARCHIVED)`. It does **not** touch clip statuses, clip earnings or balances: **0 clips** on WinGram have
an `updatedAt` in the archive window.
**The timestamps close it, cast to `::text`:**
```
campaigns.archivedAt           2026-08-07 10:26:34.832   (WinGram, camp CA-1)
payout PR-1 ($71.98) updatedAt 2026-08-07 10:26:35.219   reason "Campaign archived"
payout PR-2 ($10.15) updatedAt 2026-08-07 10:26:35.219   reason "Campaign archived"
campaign_events ARCHIVED       2026-08-07 10:26:35.298
```
**387 ms** after the archive, and the two payouts share an `updatedAt` **identical to the millisecond** — the signature
of one `updateMany`, not two clicks. The `rejectionReason` is the exact literal at `route.ts:966`. **Same operation.**
**No human clicked void.** The deliberate path (`payouts/[id]/review/route.ts`) imports `logAudit` and
`createNotification` and writes audit rows at `:309`, `:332`, `:349`. **`audit_logs` has NO entry for either void.** The
archive path writes **no per-payout audit row and no notification** — its only trace is a `console.log` at `:969`. **The
clippers were never told, and neither was the owner.** **Correction:** the void was **~5 hours ago**, not 3 days; the
**request** was created `2026-08-03 22:52:01` (~3.7 days ago), which is almost certainly the date he remembers.
## PART 2 — The blast radius
**Every payout ever voided by archiving, platform-wide** (`rejectionReason='Campaign archived'`, all 3 rows in existence):
| Payout | Clipper | Campaign | Amount | Voided at | Status now |
|---|---|---|---|---|---|
| PR-1 | CL-1 | WinGram | **$71.98** | 2026-08-07 10:26:35.219 | VOIDED, `paidAt` NULL |
| PR-2 | CL-2 | WinGram | **$10.15** | 2026-08-07 10:26:35.219 | VOIDED, `paidAt` NULL |
| PR-3 | CL-3 | *(campaign row gone)* | $27.81 | 2026-04-22 18:15:45 | VOIDED, April test-data era |
**Live damage: 2 payouts, $82.13, 2 clippers, all on WinGram.** The other archived campaigns (Deja Shoe, CROCS, Test)
voided nothing; nothing was pending when they were archived. Of 31 VOIDED rows platform-wide ($1,899.82), 26 are the
April 2026 reset era with an empty reason and 2 a labelled test cleanup.
**Every clipper who earned on WinGram.** 21 clippers, earned **$267.58**, paid **$100.42**, **owed now $165.77**.
**CAN REQUEST TODAY — act on these three ($101.53):**
| Clipper | Earned | Paid | Available | Can request NOW |
|---|---|---|---|---|
| **CL-1** (the reported one) | 73.23 | 0.00 | **73.23** | **YES** |
| CL-4 | 16.28 | 0.00 | 16.28 | **YES** |
| **CL-2** | 12.02 | 0.00 | **12.02** | **YES** |
**BLOCKED under the $10 minimum, 17 clippers, $64.24** as `ref earned/paid/available`:
```
CL-5  9.54/0/9.54    CL-6  9.42/0/9.42    CL-7  9.37/0/9.37    CL-8  6.62/0/6.62
CL-9  6.43/0/6.43    CL-10 4.70/0/4.70    CL-11 23.85/20.64/3.21  CL-12 4.09/0/2.68
CL-13 2.26/0/2.26    CL-14 2.15/0/2.15    CL-15 1.56/0/1.56    CL-16 1.32/0/1.32
CL-17 1.24/0/1.24    CL-18 1.20/0/1.20    CL-19 1.08/0/1.08    CL-20 1.08/0/1.08
CL-21 68.93/68.55/0.38     CL-22 11.21/11.23/0.00 (already paid, nothing owed)
```
**TOTAL OWED: $165.77 across 20 clippers with a positive balance.** Only **3 ($101.53) can request today**;
**17 holding $64.24 sit under the $10 minimum.**
## PART 3 — What archiving does to a clipper, and the ongoing defect
**Visibility: gone.** `campaigns/route.ts:108` sets `isArchived: false` on every live clipper view and
`campaigns/past/route.ts:32` requires it too, so an archived campaign disappears from **both** the active list **and**
BL-651's Completed row. The clipper cannot open it or see its details.
**Earnings and payouts: still fully visible and still requestable** — the load-bearing good news.
`api/earnings/route.ts:64` filters only `isTestCampaign: false`; the balance enrichment at `:238-239` filters nothing;
and the payout `POST` checks only that the campaign **exists** (`payouts/route.ts:338-344`), with **no `isArchived`
check anywhere in the withdrawal gate**. Confirmed live: CL-1 shows $73.23 available and **can request right now**.
**Against BL-641's finding:** PAST stays visible and is an unconditional arm of `campaignStatusBlocks`. COMPLETED hides
the campaign **and** is missing from `campaignStatusBlocks`. **ARCHIVED hides the campaign but IS in
`campaignStatusBlocks` (`tracking.ts:1941`, `freshCampaign?.isArchived === true`), so it does NOT share COMPLETED's
gap.** Earnings accrual correctly stops.
**THE ONGOING DEFECT, named plainly.** Archiving does **not** make earned money unrequestable, so it is not the
catastrophe it could have been. But archiving **permanently freezes accrual** (1,047 tracking jobs deactivated, **0 still
active**), and a frozen balance below $10 can **never grow to reach the minimum**. **$64.24 belonging to 17 clippers on
WinGram is permanently unreachable through the normal flow** — stuck not by the void but by a frozen campaign plus a
floor it can no longer climb. It will recur on **every** future archive. Cousin of BL-695's Bucket 2 and BL-731.
## PART 4 — The void did NOT strand the money
`balance.ts:122` counts a VOIDED payout as money-out **only when `paidAt` is not null**. **Both rows have `paidAt`
NULL**, so neither is money-out and the full amount **returned to available**. Proven live: CL-1 $73.23 against a $71.98
void, CL-2 $12.02 against a $10.15 void; both exceed what they lost, because a little accrued between request and
archive. **Nothing needs repairing before they are paid.**
**The $6.48 is not a shortfall and the void did not cause it.** It is the stored fee on the row itself: PR-1 gross
`71.98`, `feeAmount 6.48`, `feePercent 9`, `finalAmount 65.50` (PR-2: `10.15 / 0.91 / 9 / 8.83`). $71.98 − 9% =
**$65.50 exactly**. The admin row shows the **net the clipper receives** beside the **gross requested**. Both fields were
stamped at request creation on 2026-08-03, **four days before the void**, so the gap **predates the void entirely**. A
labelling matter, not missing money.
## PART 5 — The safe path to paying everyone, with no double-pay
**Archiving does NOT block a fresh request, so nothing has to be un-archived.** Proven three ways: the withdrawal gate
has no archive check, the balance still appears, and CL-1 reads `can_request_now = YES`.
The DB carries `uq_payout_open_per_user_campaign`, a **unique partial index on `(userId, campaignId)` where status is
`REQUESTED`/`UNDER_REVIEW`/`APPROVED`**. A VOIDED row does **not** occupy that slot, so a new request is accepted, and at
most **one open request per clipper per campaign** can exist. That index is what makes the procedure provably safe.
**Ordered procedure for the 3 clippers who can request today (CL-1, CL-2, CL-4, $101.53):**
1. Tell each clipper their earlier request was voided by an archive and to **submit it again** on the payouts page.
2. Confirm exactly one open row exists for that clipper on WinGram, and that its **gross** matches their available.
3. Pay against **that row**, then mark it **PAID** through the normal review path so `paidAt` is stamped.
4. Never pay from this report's table. It is a snapshot; the live gate is the only authority.
**Do NOT pay by hand first.** BL-696 established **no admin path can create a payout row** (`payoutRequest.create`
appears 0 times under `api/admin/`), so a hand payment is invisible to the platform and the balance stays fully
claimable — the clipper could then request the same money again and be paid twice. **The clipper must request first.**
**For the 17 clippers holding $64.24 under the minimum:** they cannot request at all, and accrual is frozen so they
never will. The clean release is **BL-728's per-campaign minimum, merged in BL-731**: WinGram's
`minPayoutAmountDecimal` is currently NULL (so $10). Lowering it for this one archived campaign lets them request
normally and be paid through the same safe path. That is a deliberate owner decision; this round changed nothing.
## PART 6 — Two fix specs, nothing built
**SPEC 1 — archiving must never void a pending payout.** Delete `payoutRequest.updateMany` at
`src/app/api/campaigns/[id]/route.ts:964-967` outright. Archiving should do **nothing** to pending payouts: leave them
`REQUESTED`/`UNDER_REVIEW`/`APPROVED` so the owner reviews and pays them normally. Archiving freezes **activity**, and
the other five side effects already do that (tracking stops, accrual stops via `campaignStatusBlocks`, listings pause).
A pending payout is not activity, it is **a debt already owed**. If a signal is wanted, add a campaign flag the payout
queue displays, never a status write. Whatever replaces it must write a per-payout `logAudit` row, since a bulk void
leaves no durable record today.
**SPEC 2 — voiding must require a typed confirmation.** The void in `payouts/[id]/review/route.ts` is a single click.
Require the admin to **type the payout amount** (or the word VOID) into a field echoed with the clipper's redacted ref
and the amount, button disabled until it matches exactly. Force-voiding a **PAID** payout (`review/route.ts:59`,
`isForceVoidOfPaid`) is the most dangerous, because BL-696 proved money does **not** return; it needs a stronger phrase
and its own warning. **The same guard belongs on:** campaign **archive** itself (a `DELETE` route with no confirmation
that, until Spec 1 lands, silently voids money), **freeze/unfreeze**, and any bulk clip **reject or retire**.
## What could not be measured
Whether the owner saw a warning before archiving (the confirmation is client-side, no server trace); whether either
clipper noticed, since no notification was sent; and the third April void (PR-3), unattributable because its campaign
row no longer exists (test-data era, its clipper has no live balance).
