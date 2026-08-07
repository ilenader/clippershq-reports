# BL-733 — archiving stops voiding pending payouts, and the void action gets a typed guard
**Branch** `checkpoint/BL-733` · **Base** `origin/main` `ab455ac7` · 2026-08-07 · The fix for what BL-732 proved.
**ONE LINE: the cascade is gone, the void now needs the amount typed back, and every payout status change writes an
audit row.** Worked in a clean worktree at `C:/b733` because `C:/b575` was stale (`91b84410`) and dirty (77 paths);
b575 was left exactly as found. Real `npm ci`, never a `node_modules` junction.
## PART 1 — The cascade is removed
`src/app/api/campaigns/[id]/route.ts:964-967`, the full diff:
```diff
-      // Void all pending payouts for this campaign
-      const voided = await db.payoutRequest.updateMany({
+      const pendingLeftAlone = await db.payoutRequest.count({
         where: { campaignId: id, status: { in: ["REQUESTED", "UNDER_REVIEW", "APPROVED"] } },
-        data: { status: "VOIDED", rejectionReason: "Campaign archived" },
       });
-      if (voided.count > 0) {
-        console.log(`[ARCHIVE] Voided ${voided.count} pending payouts for campaign ${id}`);
-      }
```
A `count()` replaces the `updateMany` because **a read cannot cascade**, and the number it returns is written to an
audit row, so the archive now states on the record how many pending payouts it **left alone**. The removed lines are
quoted in a comment at the site so nobody re-adds them; the harness strips comments before asserting, or it would match
that explanation and report a defect that does not exist.
**What archiving SHOULD do to a pending payout: nothing.** The money was earned **before** the archive. Archiving is
the owner ending a campaign, not a statement about a debt already owed, and a pending payout **is** a debt already
owed. Archiving still freezes **activity**, the owner's actual rule, and the remaining side effects deliver that in
full: the campaign flips to PAUSED, every tracking job is deactivated, accrual stops via `campaignStatusBlocks`, and
marketplace listings pause.
**The void was also an illegal transition**, which should have made it impossible. The state machine at
`payouts/[id]/review/route.ts:56` permits `VOIDED` **only from `PAID`, and only for OWNER**. The bulk write reached
`VOIDED` from `REQUESTED`, `UNDER_REVIEW` and `APPROVED` — three statuses that machine does not allow. It never
consulted it.
**A pending payout on an archived campaign is still fully payable and still freshly requestable**, proved by absence:
`isArchived` appears **0 times** in the withdrawal gate (`api/payouts/route.ts`), **0 times** in the review route that
approves and pays, and **0 times** in the adjust route. Nothing to fix; archiving blocks no payout path.
**No other status transition carries this.** Checked, not assumed: `freeze` (PAUSED), `unfreeze`, `past-create` (PAST)
and `restore` contain **zero** references to `payoutRequest`. Only `destroy` touches payouts, nulling the FK inside an
explicit hard-delete transaction **without changing any status**, so a payout survives with its money intact and merely
loses its campaign link. Named, not silent, and left alone.
## PART 2 — The void now needs a typed confirmation
New component `src/components/ui/confirm-destructive.tsx`. It shows the **clipper, the amount and the campaign**, and
the phrase the owner must type is **the payout's own amount**, read off that summary. A fixed word like `VOID` becomes
muscle memory and proves nothing; an amount has to be read, which means the summary has to be read. The write moved out
of `handleVoid` (which now only opens the dialog) into `confirmVoid`, so opening it can no longer void anything.
It deliberately does **not** reuse the shared `Modal`, which has no `role="dialog"`, no `aria-modal`, no focus trap and
no focus return (pre-existing, recorded in BL-729 and BL-732). A dialog whose whole job is to stand between the owner
and destroying money is the wrong place to inherit those gaps, so it implements them itself and portals to
`document.body`. Modality is carried by `aria-modal` plus a focus trap with a recovery branch; there is deliberately
**no** `aria-hidden` sweep of the background, and the accessibility section below explains why my own attempt at one
was the wrong answer.
| Action | file:line | Was | Now |
|---|---|---|---|
| **Void a payout** | `admin/payouts/page.tsx:562` | `confirm()` | **Typed: the amount** |
| **Delete a clip** | `admin/clips/page.tsx:944` | `confirm()` | **Typed: a 6-char confirm code** |
| **Recalculate a clip's earnings** | `admin/clips/page.tsx:989` | `confirm()` | **Typed: a 6-char confirm code** |
| Bulk recalc `all` / Reset data | `force-recalc:100`, `reset-data:58` | **already typed** (`RECALC ALL`, `RESET`) | left |
| Fraud review: stop counting / leave / reject | `admin/fraud-review/page.tsx:256-266` | `confirm()`+`prompt()` | left |
| Freeze campaign / platform toggle | `admin/campaigns/page.tsx:669`, `:1741` | `confirm()` | left |
| Delete referral payment record | `admin/referrals/page.tsx:343` | `confirm()` | **left, but flagged** |
| Knowledge Q&A, team delete, link revoke, unban | four sites | `confirm()` | left, not money |
**Guarded: the three that move a clipper's money.** Deleting a clip destroys the earnings recorded against it;
per-clip recalculation ignores the submission-time CPM freeze, so a settled payout can move up **or down**.
**Left, with reasons.** Bulk recalc `all` and `reset-data` **already carry typed confirmations**, so the most
destructive modes are covered. Fraud-review's "stop counting" is explicitly **reversible** with an undo list, takes
back nothing already paid, and already names the clip, clipper and consequence; converting an inline three-branch
`confirm`/`prompt` flow on a fraud surface is larger than this round should carry. Campaign freeze is reversible and
says clippers can still cash out. The platform toggle blocks only **new** submissions while existing clips keep paying.
**Flagged for its own round:** `admin/referrals/page.tsx:343` deletes the record that a referral payment happened.
Erasing it could permit a **double-pay**, making it money-destructive by omission rather than commission. It deserves
the same gate; it is out of scope here and is recorded rather than quietly skipped.
## PART 3 — Every payout status change is now on the record
Recorded via `logAudit` into `audit_logs`: the **actor** (`userId`), the **action** (`VOIDED_PAYOUT`,
`FORCE_VOID_PAID_PAYOUT`, `APPROVED_PAYOUT`, `PAID_PAYOUT`, `REJECTED_PAYOUT`, `UNDER_REVIEW_PAYOUT`), the **target**
(`targetType`/`targetId`), the **timestamp**, and details carrying **from-status, to-status and the trigger**.
**Two gaps found and closed.** `api/calls/route.ts:277` moved a payout `REQUESTED → UNDER_REVIEW` when a call was
booked, **live, with no audit row at all**. And `src/actions/payouts.ts` `reviewPayout` is **dead code** that nothing
imports, yet it could set **any** status including `VOIDED`, **from an ADMIN**, with **no state machine and no audit**;
it now refuses `VOIDED` outright and audits everything else. BL-728's lesson applied: the unreachable copy bites later.
The archive itself now writes `CAMPAIGN_ARCHIVED` with `trackingJobsDeactivated` and `pendingPayoutsLeftUntouched`.
That action had **0 rows** in `audit_logs` before this round, which is exactly why BL-732's cascade was invisible.
**Is the clipper told? NO, and this round did not change that.** Stated plainly rather than implied. The review route
notifies on `APPROVED`, `REJECTED` and `PAID` (`review/route.ts:430-446`) and **has no branch for `VOIDED`**. The
cascade that made this urgent is gone, so nothing vanishes silently any more, but a **deliberate** owner void still
reaches the clipper as a status change they must notice themselves. **Notification is OUT OF SCOPE for this round**
and wants its own, under BL-518 and BL-521's plain, non-accusatory rule.
## PART 4 — The two already-voided payouts, untouched
Nothing was un-voided, approved, paid or altered. Confirmed live (DB now `2026-08-07 18:54:55 +00`):
| Clipper | Voided amount | WinGram available now | Open requests | Can request NOW |
|---|---|---|---|---|
| CL-1 | $71.98 | **$73.23** | **0** | **YES** |
| CL-2 | $10.15 | **$12.02** | **0** | **YES** |
Both hold **more** than was voided, because a little accrued between the request and the archive. **0 open requests**
matters: `uq_payout_open_per_user_campaign` is a unique partial index on `(userId, campaignId)` for
`REQUESTED`/`UNDER_REVIEW`/`APPROVED`, so an empty slot means a fresh request is accepted, and at most one open request
per clipper per campaign can ever exist.
**The safe procedure, provably unable to double-pay:** (1) tell each clipper their earlier request was voided by an
archive and ask them to **submit it again**; (2) confirm exactly **one** open row exists for that clipper on that
campaign and its gross matches their available; (3) pay against **that row**, then mark it **PAID** through the normal
review path so `paidAt` is stamped; (4) never pay from this table, it is a snapshot and the live gate is the authority.
**Do not pay by hand first.** BL-696 established **no admin path can create a payout row**, so a hand payment is
invisible and the balance stays fully claimable — the clipper could request the same money again and be paid twice.
## PART 5 — Evidence
Harness `scripts/bl733-verify.ts`: **60 passed, 0 failed**. The archive half is a **static** proof over the source,
deliberately: the claim is a negative (the write does not exist), the brief forbids archiving a real campaign, and
there is no safe throwaway archive on a production database.
```
PASS archive contains NO payoutRequest.updateMany   PASS archive: NO VOIDED literal in executable code
PASS archive touches payoutRequest ONLY via count (found: payoutRequest.count)
PASS archive still deactivates tracking jobs (activity IS still frozen)
PASS freeze (PAUSED) / unfreeze / past-create (PAST) / restore do not write payout_requests
PASS the withdrawal gate / review route / adjust route never read isArchived
PASS calls route (REQUESTED to UNDER_REVIEW) now audits   PASS the dead server action refuses VOIDED outright
PASS the dialog shows the CLIPPER / the AMOUNT / the CAMPAIGN
PASS the phrase to type is the payout's own amount   PASS the write only happens in confirmVoid, not on open
PASS it PORTALS to document.body   PASS the rest of the document is hidden from AT while it is open
```
**Nothing was altered.** 158 payout rows and 31 VOIDED, both unchanged; newest payout `updatedAt` is
`2026-08-07 15:12:04`, predating this round and belonging to an unrelated live request. **0 payouts touched** and **0
campaigns archived** since this round began. 3,394 approved clips, $8,189.29, **invariant 0 violations**. 19 archived
campaigns, unchanged. No wallet address selected or printed; handles redacted to stable refs.
**Money files byte-identical by blob OID on both refs:** `clip-earnings-writer` `ac5be7de`, `earnings-calc` `797e2098`,
`balance` `e887f80a`, `tracking` `83ce4bab`, `clip-earnings-invariant-middleware` `61cef393`, `money-decimal`
`ef5cdae7`, `campaign-era` `106e16ad`.
## Gates, stated honestly
`npm ci` exit 0 (822 packages, no junction). `npx prisma generate` exit 0, run **before** tsc because `npm ci` wipes the
client. `tsc --noEmit` **0 errors, exit 0**. `npm run build` **exit 0**, "Compiled successfully", read from a log with
the exit code echoed, never piped. BL-348 hooks gate **0 errors, 11 warnings — at the limit of 11**, with **eslint
v9.39.4 confirmed present** so the gate is not silently a no-op. 5 files modified, 2 added.
## Accessibility — the review returned FAIL, and it was right
The `accessibility-lead` review landed **after** the first push and returned **FAIL with nine blocking defects**. All
nine are fixed and pinned by 15 new harness checks. It is recorded here because a round that hid this would be worth
less than the code it shipped.
**What it caught that I had wrong:**
| # | Defect | Fix |
|---|---|---|
| D7 | **The worst one, and self-inflicted.** The summary rendered `formatCurrency` → `"$71.98"` while the phrase demanded `"71.98"`. **Typing exactly what the dialog told you to read was rejected**, silently, for every payout | comparison normalises `$`, `,` and spaces |
| D1 | Focus reaches `<body>` routinely (backdrop click, disabled button), and from there Tab walked **out of the dialog** into the admin table behind the scrim | recovery branch when focus escapes the panel, plus `tabIndex={-1}` on it |
| D2 | The confirm button **disabled itself under the user's own focus** on every confirm, triggering D1 | focus moves to the panel before `onConfirm()` |
| D3/D4/D5 | My own `aria-hidden` background sweep hid **focusable** containers (axe `aria-hidden-focus`) and, because sonner renders under `<body>`, **silenced the only channel reporting a failed void** | sweep **deleted**; `aria-modal` is ARIA 1.2's replacement for it |
| D6 | Focus was returned to a **detached** node, since both call sites remove the row as they close | restore guarded on `isConnected` |
| D8 | A wrong phrase was indistinguishable from an unfinished one | `aria-invalid` + a visible mismatch message; empty is not an error |
| D9 | Escape looked like it cancelled a request it **cannot** stop | Escape refused while busy; `isComposing` respected |
Also fixed from its advisories: failures now render **inside** the dialog (`role="alert"`), the summary used
`--bg-page` which is **undefined repo-wide** and computed to transparent (now `--bg-input`), the input border was
1.18:1 against the card (1.4.11), `aria-busy` is exposed, and the clip dialogs asked for a **25-character cuid** —
a genuine COGA barrier containing every dyslexia-hostile pair, whose rational escape is copy-paste, which defeats the
gate entirely. They now ask for a **6-character confirm code** shown as its own row.
**It also validated the portal**, which I had added mid-review on my own reading: for OWNER the layout wrapper carries
`transform: translateX(0)`, and a non-`none` transform becomes the containing block for `position: fixed`, so the
in-tree dialog resolved `inset-0` against a box starting after the sidebar and sat inside a lower stacking context,
with `ChatWidget` painting **above** it. Every user who can reach a destructive action is exactly the user who hit it.
**Correction to the review itself:** it reports the portal and sweep as an unauthorised edit by a specialist agent
mid-review. They were mine, made deliberately while it ran. **Passing throughout:** dialog semantics and IDREFs,
`<dl>` structure, the `role="status"` region, label association, icon and danger-button contrast, and **WCAG 3.3.4
Error Prevention (Financial)**, which these three actions now satisfy properly where `window.confirm()` could not show
which clipper or which amount. **Disclosed residual:** typing a phrase is a deliberate cognitive load. That is the
point of the guard, and it is still a real cost for an owner who voids often.
