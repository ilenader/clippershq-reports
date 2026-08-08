# BL-741 — merging BL-739 and BL-740, one at a time
**Merged to main** `b5bd0651` · **Was** `6d906941` · 2026-08-08 · Merge only, no source authored.
## STEP 0 — Truth per branch
| Branch | SHA | Ancestor of main? | Diff vs main |
|---|---|---|---|
| `checkpoint/BL-739` | **`cde68af6`** | **NOT an ancestor**, genuinely unmerged | non-empty: 4 files, 538 insertions |
| `checkpoint/BL-740` | **`6edf2d17`** | **NOT an ancestor**, genuinely unmerged | non-empty: 8 files, 743 insertions |
| `checkpoint/BL-723` | `22039307` | not an ancestor, **deliberately NOT merged** | targets `business-api`, uncallable by a Login Kit app |
**Both tips carry their own a11y outcome; there is no earlier defective state to avoid.** Each branch is a **single
commit**, so no superseded state exists on either. BL-740's one commit contains the fixes for the four blocking
defects its review returned, including the regression it introduced and caught. BL-739 was **accessibility reviewed
before any UI was written**, its footer safe-area padding was taken on that advice in-round, and one item
(`app-layout.tsx:982` suppressing the mobile topbar on one surface) was filed rather than fixed.
**Dirty worktree handling.** `C:/b575` was **stale** (`91b84410` against main `6d906941`) **and dirty** (77 paths), so
both merges ran in a **separate clean worktree at `C:/m741`**, a short path, with `.env`/`.env.local` copied and a real
`npm ci`. **Never a `node_modules` junction.** b575 was not touched.
## The two merges, one at a time
**Merge 1, BL-739 → `69bbb8e4`.** One conflict, `BACKLOG.md`, unioned. **128 → 129** by `grep -c`.
**Merge 2, BL-740 → `b5bd0651`.** One conflict, `BACKLOG.md`, unioned. **129 → 130**, exactly **one** BL-739 entry and
**one** BL-740 entry, **0 conflict markers** tree-wide after each.
## Confirmed on the merged result, by code reading and harness
**The touchmove carve-out is conditional and cannot reintroduce the leak BL-320 reverted.** BL-737 proposed exempting
`[data-drawer-panel]`, which is **the exact carve-out BL-319 shipped and BL-320 tore out** for letting the gesture
through on mobile Chrome (`BACKLOG.md:2001`). The mechanism that explains the old report is that the panel also holds
the logo header and the footer, neither of which has anything to scroll, so a pan starting on either was exempted and
then chained to the document. The merged code is narrower on **three independent axes**:
```
const scroller = (e.target)?.closest?.("[data-drawer-panel] [data-drawer-scroll]");
if (scroller && scroller.scrollHeight > scroller.clientHeight) return;
```
Only the drawer's own **scroller** is exempt, never the panel chrome; only **while it actually overflows**, so every
menu that fits stays byte-identical and BL-320's "the menu is short" premise is honoured for exactly the users it was
true for; and the scroller carries **`overscroll-contain`**, which `globals.css:178` already documents as how an inner
scroller opts into its own overscroll behaviour under BL-150's `overscroll-behavior: none`. Everything outside that one
element is still prevented, so BL-321's background lock is untouched. Measured in real Chromium by the branch: **53
passed, 0 failed, background scroll 0 while the drawer scrolled 805.**
**The picker offers ACTIVE campaigns with headroom, and the seven blocks still refuse.** `CLIPPER_NOT_ON_DEST` appears
**0** times; the condition is `accountIsApproved`. Refusals remain structural: **16** `blocks.push` sites with
`allowed: blocks.length === 0`, so there is no warn-and-continue path and era-freezing, PAST, paused, spent and
platform-incompatible destinations all still refuse. The harness on the merged tree reports **70 passed, 0 failed**,
including the BL-740 positive-case guard: **10 of 10 sampled pending clips have at least one real destination, 27
clip-campaign pairs offered.**
**A clip whose OWN campaign is archived still resolves it.** `current` is now its own
`db.campaign.findUnique({ where: { id: clip.campaignId } })`; the filtered-list lookup
`campaigns.find(c => c.id === clip.campaignId)` appears **0** times. That was the regression BL-740's review caught
before it shipped, reachable on **2 pending clips** that sit on archived campaigns, which otherwise gave
"Currently on: Unknown" or a 500.
**The membership row is created inside the transaction.** Exactly **one** `campaignAccount.upsert` exists in the route
and it is **inside** `db.$transaction`, so a failed move leaves no membership row behind.
## After the push — what moved, and what did not
**Zero clips were reassigned.** `CLIP_CAMPAIGN_REASSIGNED` audit rows **0**, reassignment notifications **0**. No
clip's campaign, CPM or earnings changed by this merge. **Earnings invariant: 0 violations.** 19 archived campaigns,
unchanged. **A merge writes nothing to the database**, and that is the ground of every claim here.
**Two figures did move, and I am not going to report them as unchanged.** Both are the platform running live while I
worked, and both are fully attributed:
| Observation | Attribution |
|---|---|
| Payout rows still **161**, but newest `updatedAt` is `2026-08-08 21:06:12` | **The owner approved and paid a payout.** `audit_logs` carries `APPROVED_PAYOUT` at `21:06:10` then `PAID_PAYOUT` at `21:06:12`, through the normal review path. **A payout WAS approved and paid this evening — by the owner, not by this merge.** The brief asked me to confirm none was; the honest answer is that one was, by him |
| `campaign_accounts` **587 → 589** | Two clippers joined campaigns **self-serve**, at `18:26:25` and `20:48:24`. Neither coincides with a reassignment, since there were none. Ordinary joins, not the new transactional upsert |
Also visible: four `REJECTED_CLIP` audit rows at `20:01`, the owner reviewing clips.
**The stranded population reads 128 pairs / $400.37 against BL-738's 129 / $420.29.** It moved **down**, and not
because of this merge. **Structural:** the merge touches **no verdict-deciding file** — `api/payouts/route.ts`,
`payout-minimum.ts`, `balance.ts`, `earnings-calc.ts` and `campaign-clipper-view.ts` are all **absent** from its 11
changed files, which are two layout files, the reassignment route and library, the dialog, three scripts, a report and
BACKLOG. **Causal:** the owner paying a payout at `21:06` removes that clipper's balance from the pool, which is
exactly the kind of movement that shifts a pair across the $10 threshold. The population moving while the owner works
is the system behaving correctly.
**BL-696's no-double-pay and BL-627's no-overpayment both hold.** Neither branch touches payout creation, the 10s
dedupe, the `uq_payout_open_per_user_campaign` index or any cap.
## Gates, stated honestly
`npm ci` **exit 0**, 822 packages, 0 npm errors, no junction. `npx prisma generate` **exit 0**, run **before** tsc
because `npm ci` wipes the generated client. `npx tsc --noEmit` **0 errors, exit 0**. `npm run build` **exit 0**,
"Compiled successfully in 37.4s", read from a log with the exit code **echoed, never piped through `tail`**. BL-348
hooks gate **0 errors, 11 warnings — at the limit of 11**, with **eslint v9.39.4 confirmed present**. Push verified by
`git ls-remote`: **origin/main == local == `b5bd0651`**. `safe-push.mjs` printed a **false failure** because it cannot
verify a `src:dst` refspec from a detached worktree (the BL-727 trap); `ls-remote` is the authority and agrees.
**Money files byte-identical by blob OID on both refs:** `clip-earnings-writer` `ac5be7de`, `earnings-calc` `797e2098`,
`balance` `e887f80a`, `tracking` `83ce4bab`, `clip-earnings-invariant-middleware` `61cef393`, `money-decimal`
`ef5cdae7`, `campaign-era` `106e16ad`. No wallet address was selected or printed; handles redacted to stable refs.
**Rollback:** `git revert -m 1 b5bd0651` for BL-740, `git revert -m 1 69bbb8e4` for BL-739. Nothing to undo in the
database.
