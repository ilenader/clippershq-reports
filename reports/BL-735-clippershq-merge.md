# BL-735 — merging BL-733 and BL-734, one at a time
**Merged to main** `dd5d03f9` · **Was** `ab455ac7` · 2026-08-08 · Merge only, no source authored.
## STEP 0 — Truth per branch
| Branch | SHA | Ancestor of main? | Diff vs main |
|---|---|---|---|
| `checkpoint/BL-733` | **`429017e4`** | **NOT an ancestor**, genuinely unmerged | non-empty: 9 files, 974 insertions |
| `checkpoint/BL-734` | **`7a78feb2`** | **NOT an ancestor**, genuinely unmerged | non-empty: 5 files, 121 insertions |
| `checkpoint/BL-723` | `22039307` | not an ancestor, and **deliberately NOT merged** | targets `business-api`, uncallable by a Login Kit app |
**BL-733 was merged at its POST-A11Y-FIX tip.** `git log` shows `429017e4` as the branch head with the earlier push
`c2b6b311` as its **parent**, so the merge carries the fixed state, not the broken one. This mattered: `c2b6b311`
contained the dialog that displayed `$71.98` while demanding `71.98`, silently rejecting every attempt.
**Dirty worktree handling.** `C:/b575` was **stale** (`91b84410` against main `ab455ac7`) **and dirty** (77 paths), so
the merge ran in a **separate clean worktree at `C:/m735`**, a short path, with `.env`/`.env.local` copied and a real
`npm ci`. **Never a `node_modules` junction.** b575 was not touched and remains exactly as found.
## The two merges, one at a time
**Merge 1, BL-733 → `4e91eedd`.** No conflicts. Verified between: the merge tree OID equalled the branch tree OID
(main had not advanced), BACKLOG 125 → 126, exactly one BL-733 entry, 0 conflict markers tree-wide.
**Merge 2, BL-734 → `dd5d03f9`.** One conflict, `BACKLOG.md` only, resolved as a **UNION keeping both entries whole**:
**125 → 127 by `grep -c`** (never piped to `head`), exactly **one** BL-733 and **one** BL-734, **0 markers** anywhere
in the tree.
## Confirmed on the merged result, by reading code and never by archiving anything
**Archiving no longer voids pending payouts.** In the `DELETE` (archive) handler the only executable reference to
`payoutRequest` is a **`.count()`**; the sole other mention is a comment recording what was removed. A read cannot
cascade. The handler still deactivates tracking jobs and flips the campaign to PAUSED, so activity is still frozen,
and it now writes `pendingPayoutsLeftUntouched` to the audit log. **Nothing was archived to test this.**
**The void confirmation demands exactly what it displays.** This is the defect that shipped once, so it was checked
character for character: the summary row renders `formatCurrency(amount)` → **`"$71.98"`**, the phrase is
`Number(amount).toFixed(2)` → **`"71.98"`**, and `normalisePhrase` strips `$`, commas and whitespace before comparing,
so **both forms match**. Typing what is displayed is accepted; so is typing the hint. No mismatch survives.
**The toast region is not `aria-hidden`.** `setAttribute("aria-hidden"` appears **0 times** in the component. The
sweep that had silenced sonner's live region, so a *failed* void would have been silent to a screen reader, is gone,
and failures now render inside the dialog as a `role="alert"`.
**Every payout status change writes an audit row.** `logAudit` count per writer: review route **5**, calls route **2**,
the previously-dead server action **2**, adjust route **3**.
**All seven minimum copies resolve to the per-campaign value, including the chat auto-reply.** A grep for hardcoded
minimum copy across `src` returns exactly **one** hit, and that hit is a **comment** explaining a removal, not a live
string. The seventh copy, the pattern-matched chat fallback at `api/chat/conversations/[id]/messages/route.ts`, was
**live and clipper-facing** and asserted a flat `$10`; having no campaign context, it now states the rule and points at
the screen that knows the number rather than naming one it cannot verify.
**Both raised campaigns still store exactly `20.0000`:**
```
| camp_ref | name                 | min_stored | updated_at                  |
| 4d2c9b   | Zhus Edit (0.50 CPM) | 20.0000    | 2026-08-07 18:16:31.241     |
| 7dd820   | Zhus Meme (0.20 CPM) | 20.0000    | 2026-08-07 18:16:46.13      |
```
Both `updatedAt` values predate this round; **2 campaigns at 20.0000**, unaltered.
## After the push — live state, DB now `2026-08-08 13:18:57 +00`
**No payout status changed.** 161 payout rows and 31 VOIDED, identical before and after; newest payout `updatedAt` is
`2026-08-08 03:29:31`, which **predates the push** (13:16). **0 payouts touched** and **0 campaigns touched** since the
push. **Earnings invariant: 0 violations.**
**No clipper's withdrawal verdict flipped, and this is provable rather than merely measured.** The merge touches
**no verdict-deciding file**: `api/payouts/route.ts` (the withdrawal gate), `payout-minimum.ts` (`resolveMinPayout`),
`balance.ts`, `earnings-calc.ts` and `campaign-clipper-view.ts` are **all absent** from the merge's 13 changed files.
The resolution logic is byte-identical before and after, so it cannot return a different answer for the same row.
**The stranded population does NOT match BL-734's figure, and I will not report that it does.**
| Measurement | Pairs | Dollars |
|---|---|---|
| BL-734, 2026-08-07 ~18:16 | 118 | $338.20 |
| **This round, post-push** | **128** | **$400.69** |
**The merge did not cause it.** Two independent grounds. First, structural: the merge changed no file that decides a
verdict, and changed no data. Second, measured: **97 clips were approved between BL-734's measurement and now**, and
approved earnings stand at **$8,256.52**. Nineteen hours of ordinary accrual on ACTIVE campaigns creates new
clipper-campaign pairs and moves existing balances across the threshold in both directions. That is the whole
difference. Reporting "unchanged" would have been the comfortable answer and the false one.
**BL-696's no-double-pay and BL-627's no-overpayment both hold.** Neither branch touched payout creation, the 10s
dedupe, the `uq_payout_open_per_user_campaign` unique index or any cap. BL-733 adds only a **refusal** (a typed gate),
and a refusal can block but never grant; BL-734 is display copy.
## Gates, stated honestly
`npm ci` **exit 0**, 822 packages, 0 npm errors, no junction. `npx prisma generate` **exit 0**, run **before** tsc
because `npm ci` wipes the generated client. `npx tsc --noEmit` **0 errors, exit 0**. `npm run build` **exit 0**,
"Compiled successfully in 39.4s", read from a log with the exit code **echoed, never piped through `tail`**. BL-348
hooks gate **0 errors, 11 warnings — at the limit of 11**, with **eslint v9.39.4 confirmed present**, so the gate is
not silently a no-op. Push verified by `git ls-remote`: **origin/main == local == `dd5d03f9`**. `safe-push.mjs` printed
a **false failure** because it cannot verify a `src:dst` refspec from a detached worktree (the BL-727 trap);
`ls-remote` is the authority and it agrees.
**Money files byte-identical by blob OID on both refs:** `clip-earnings-writer` `ac5be7de`, `earnings-calc` `797e2098`,
`balance` `e887f80a`, `tracking` `83ce4bab`, `clip-earnings-invariant-middleware` `61cef393`, `money-decimal`
`ef5cdae7`, `campaign-era` `106e16ad`.
**Nothing was archived, un-archived, voided, un-voided, approved, created or cancelled, and no campaign minimum was
altered.** No wallet address was selected or printed; handles are redacted to stable refs.
**Rollback:** `git revert -m 1 dd5d03f9` for BL-734, `git revert -m 1 4e91eedd` for BL-733. Reverting BL-733
**restores the archive-to-void cascade**, so do that only with the consequence understood.
