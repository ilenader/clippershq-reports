# BL-738 — merging BL-736, the pending-clip campaign reassignment
**Merged to main** `6d906941` · **Was** `dd5d03f9` · 2026-08-08 · Merge only, no source authored.
## STEP 0 — Truth
| Branch | SHA | Ancestor of main? | Diff vs main |
|---|---|---|---|
| `checkpoint/BL-736` | **`e3df141d`** | **NOT an ancestor**, genuinely unmerged | non-empty: 11 files, **1,742 insertions** |
| `checkpoint/BL-723` | `22039307` | not an ancestor, **deliberately NOT merged** | targets `business-api`, uncallable by a Login Kit app |
**The tip IS the post-a11y-fix commit.** `git log` shows `e3df141d` as the branch head with the earlier push
`08a96c58` as its **parent**, so the merge carries the fixed state. That mattered: `08a96c58` carried three blocking
accessibility defects, two of them regressions against rules this repo had already written down.
**Dirty worktree handling.** `C:/b575` was **stale** (`91b84410` against main `dd5d03f9`) **and dirty** (77 paths), so
the merge ran in a **separate clean worktree at `C:/m738`**, a short path, with `.env`/`.env.local` copied and a real
`npm ci`. **Never a `node_modules` junction.** b575 was not touched.
**No conflicts.** BACKLOG **127 → 128** by `grep -c` (never piped to `head`), exactly one BL-736 entry, **0 conflict
markers** tree-wide. The merge tree OID equals the branch tree OID, main having not advanced.
## Confirmed on the merged result, by code reading and harness, never by moving a clip
**All seven destination conditions refuse, and cannot be downgraded to warnings.** This is structural rather than a
spot-check: `evaluateDestination` pushes onto a `blocks` array and returns `allowed: blocks.length === 0`, so **all 16
push sites are refusals by construction** and there is no warn-and-continue path to soften. The era case
(`DEST_ERA_WOULD_FREEZE`) is one of them, which matters because `tracking.ts` compares `clip.createdAt` against the
**destination's** boundary and freezes earnings forever when the clip predates it, while `createdAt` cannot honestly
be rewritten.
**One atomic transaction.** Exactly **one** `db.$transaction`, containing the `SELECT ... FOR UPDATE` row lock, the
`campaignId` write, **both** CPM stamps in the same update, and the `TrackingJob` repoint. **The locked share needs no
copying at all**: `guaranteeOwnerSplit` and `lockedOwnerShareDecimal` are **campaign** columns, not clip columns, so
after the move the clip reads the destination's share because it reads the destination. That is what makes the stamp
and the share agree **by construction** rather than by convention, which is the failure BL-539 proved and BL-570
priced at $933.94.
**The null-CPM pay-cut fix survived, and I checked this one hardest.** A null `cpmAtSubmissionDecimal` falls back to
the live campaign rate inside `getEffectiveCpmForClip`, so reading the raw stamp reported "no rate", which suppressed
the pay-cut warning **and** sent the clipper the softer notification even when the move halved their pay. Both
handlers now call `getEffectiveCpmForClip`; **raw-stamp reads remaining in that route: 0.**
**The focus-trap fix reaches the dialog already live on main.** A radio group has **one** roving tab stop, so treating
the first radio as the first tab stop let Shift+Tab leave the dialog once any later option was selected; and focus
resting on the panel itself was neither "escaped" nor an end of the list, so Shift+Tab from the opening state escaped
too. **That second hole was live in BL-733's void dialog on main.** Both now import one shared `useDialogFocusTrap`:
`confirm-destructive.tsx` references it **twice** and retains **zero** remnants of its own `querySelectorAll` copy, so
no second implementation is left to drift.
**Blocked campaigns stay keyboard-reachable.** Native `disabled` on blocked options: **0**. They are a plain list
headed "Cannot be used right now" carrying their reasons, because native `disabled` removes an option from arrow-key
roving as well as the tab order and made its reason unreachable in forms mode, against this repo's own BL-556 rule.
**Every reassignment writes an audit row**, `CLIP_CAMPAIGN_REASSIGNED`, plus a clipper notification.
**BL-736's harness on the merged tree: 69 passed, 0 failed**, including each of the seven blocks exercised
individually and the live era measurement:
```
DB now = 2026-08-08 17:10:08.455896+00
21 pending clips on non-test campaigns
32 live campaigns, 8 of them PAST
2 of 32 campaigns carry an era boundary
5 of 21 pending clips would freeze if moved into SOME era-carrying campaign
```
## After the push — nothing moved
| Check | Result |
|---|---|
| Clips ever reassigned (`CLIP_CAMPAIGN_REASSIGNED` audit rows) | **0** |
| Reassignment notifications sent | **0** |
| Earnings invariant violations | **0** |
| Payout rows | **161**, unchanged; newest `updatedAt` `2026-08-08 03:29:31`, **predating this round** |
No clip's campaign, CPM or earnings changed, and no payout was created, modified, approved or cancelled.
**The stranded population reads 129 pairs / $420.29 against BL-735's 128 / $400.69, and I will not report that as
unchanged.** The merge did not cause it, on two independent grounds. **Structural:** the merge touches **no
verdict-deciding file** — `api/payouts/route.ts` (the withdrawal gate), `payout-minimum.ts`, `balance.ts`,
`earnings-calc.ts` and `campaign-clipper-view.ts` are all **absent** from its 11 changed files. The one money-adjacent
file it does touch is `cpm.ts`, and its entire diff is a **TypeScript union member** on a parameter type
(`| "reassign"`), which is erased at compile time and has **zero runtime effect**. **Measured:** **190 approved clips
were updated by the tracking cron** between `14:00:14` and `17:10:38`, the roughly four hours since BL-735 measured,
accruing $329.19 across them. Ordinary accrual creates and moves pairs across the $10 threshold in both directions.
**BL-696's no-double-pay and BL-627's no-overpayment both hold.** BL-736 touches payout creation, the 10s dedupe, the
`uq_payout_open_per_user_campaign` index and every cap **not at all**; it only ever refuses, and a refusal can block
but never grant.
## Gates, stated honestly
`npm ci` **exit 0**, 822 packages, 0 npm errors, no junction. `npx prisma generate` **exit 0**, run **before** tsc
because `npm ci` wipes the generated client. `npx tsc --noEmit` **0 errors, exit 0**. `npm run build` **exit 0**,
"Compiled successfully in 34.1s", read from a log with the exit code **echoed, never piped through `tail`** — and
worth noting because BL-736's own first build exited 1 *after* printing "Compiled successfully". BL-348 hooks gate
**0 errors, 11 warnings — at the limit of 11**, with **eslint v9.39.4 confirmed present** so the gate is not silently
a no-op. Push verified by `git ls-remote`: **origin/main == local == `6d906941`**. `safe-push.mjs` printed a **false
failure** because it cannot verify a `src:dst` refspec from a detached worktree (the BL-727 trap); `ls-remote` is the
authority and agrees.
**Money files byte-identical by blob OID on both refs:** `clip-earnings-writer` `ac5be7de`, `earnings-calc` `797e2098`,
`balance` `e887f80a`, `tracking` `83ce4bab`, `clip-earnings-invariant-middleware` `61cef393`, `money-decimal`
`ef5cdae7`, `campaign-era` `106e16ad`. No wallet address was selected or printed; handles redacted.
**Rollback:** `git revert -m 1 6d906941`. Nothing to undo in the database, since nothing was ever moved.
