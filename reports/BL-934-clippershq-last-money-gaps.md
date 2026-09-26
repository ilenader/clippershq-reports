# BL-934 — the last two known money-path gaps, closed before they were reached

**Shipped 2026-09-26.** Branch `checkpoint/BL-934` (c592a5d), merged to main as 773b82e.
Rollback: `git reset --hard pre-merge-BL-934` (no schema, no SQL to undo).

**Opus wrote every line and read every measurement itself, no subagent between it and the source.** At most one database connection was held at a time. No vendor call, no Apify actor.

**Both gaps were verified still open on main before either was touched, and neither has ever caused harm.**

## Gap 1: the per-tick and approval-time committed-spend reads omitted the two v2 legs
**Measured on main.** The tick (`tracking.ts`) and the approval route (`clips/[id]/review/route.ts`) each build an inline committed-spend figure to drive per-tick truncation and auto-pause. Both summed `Clip.earnings` plus the agency and the two v1 marketplace aggregates, and both **omitted the two marketplace-v2 aggregates**. The L1 hard lock's own read, `getCampaignBudgetStatus` in `balance.ts`, always counted them, which is why nothing ever overspent (BL-877, BL-916 item 1 named this exact shape). But the inline projections saw 55 cents less per v2 dollar, so a marketplace campaign paused late and truncation ran against a figure too low.

**The fix, at one point, calling the existing derivation's own query rather than inventing a second.** `balance.ts` is a protected byte-identical file and its function uses its own db connection (it cannot be called inside the tick's serializable transaction), so each inline read is completed with the two v2 aggregates **byte-mirroring balance.ts:555-561**, on `tx`. Two companion lines keep the arithmetic correct: this clip's own v2 legs are subtracted from `otherSpent` (so its prior legs are not double-counted and it is not over-truncated), and the clip's new v2 legs join `newTotalSpent` (so a v2 clip whose fresh write crosses the budget auto-pauses on that tick, not the next). `tracking.ts`: 46 insertions, 2 deletions. **Byte-identical behaviour for any campaign with no v2 rows**, because a SUM over zero rows coalesces to 0; the two changed variables do not move. The other five money files are byte-identical by blob OID.

**Proven on values that cannot divide evenly** (budget $9.37; legs $4.11 poster, $4.11 editor, $0.91 platform), against the real `getCampaignBudgetStatus`:
* the OLD inline read was $4.11 and the L1 read $9.13 — they disagreed by exactly $5.02, the two v2 legs;
* the NEW inline read equals the L1 read, $9.13;
* truncation of a fresh $2.00 write goes from a wrong $5.26 remaining (which would let it through in full, pushing the campaign to $11.13 undetected) to the true $0.24 remaining;
* **auto-pause now fires when it should**: the old projection stayed under budget and would not pause; the new one reaches $9.37 and pauses.

## Gap 2: the two owner repair tools scaled one leg of three on a v2 clip
**Measured on main.** `fix-budget` and `payouts/[id]/adjust` scale a stored figure by a ratio. On a v2 clip they scaled the poster's leg on `Clip.earnings` and left the editor's and platform's legs at full value, because they tested `isMarketplaceClip` alone and a v2 clip carries that flag FALSE on purpose (BL-917 item 1). **Nobody was ever harmed: 0 v2 clips have ever had a reduction ratio set, so neither tool has ever run on a v2 clip.** BL-882 had already protected the editor's own payout path (its clip snapshot is an explicit empty array); the exposed path was a v2 poster's payout.

**Closed by keeping the tools OFF a v2 clip, not by teaching them the three-leg split** — a refusal cannot corrupt anything, and a v2 clip's three legs are already capped together through the chokepoint by the tick and the marketplace-v2 approval. `fix-budget` **excludes** a v2 clip from its scaling query (`marketplaceV2PostId: null`). `adjust` **refuses** a payout that includes a v2 clip, with a typed code and 400, before any write. Proven live against the running production build: the adjust route returned 400 with the typed code, and the clip's earnings and the payout row were unchanged afterward; the fix-budget query returned the v2 clip in 0 of its results.

## Guards
* **W6** in `check-v2-single-share-writers.js` was rewritten deliberately. It used to fail the moment a scaler named the v2 identifier; that made the fix impossible to express. It now asserts each scaler **names the identifier AND carries its documented v2-safety marker** (`marketplaceV2PostId: null` for fix-budget, the typed refusal code for adjust), so a scaler that goes blind again, or names the field for any other reason and then scales it, fails. Demonstrated failing both branches one at a time, each restored byte-identical.
* **`check-v2-editor-balance.js`** allow-lists were updated deliberately and its two guards agree with W6: the approval route joins the committed-spend readers (it now runs the same campaign-wide v2 aggregate as the tick and balance.ts), and the two scalers join the v2-identifier namers (they name it to exclude or refuse v2, the opposite of hand-rolling a payable filter). Both guards were observed failing before these entries were added, so they can still fail.
* All 22 prebuild guards pass; the hooks gate is 0 errors, 10 warnings.

## Safety
* **Money untouched.** The other five money files are byte-identical by blob OID; `tracking.ts` changed by design. The two scaler fixes write nothing on a v2 clip. Both reconciliation forms return 0 rows before and after — identical, because no stored money row changed.
* **Invariants:** 11 of 11 across the full population, no campaign over budget, ANGIE BROWN at a $2,700 budget.
* **No `.tsx` changed,** so no render pass was run.
* **Sandbox:** 10 prefixed rows, all ledgered, torn down; a sweep of 343 id columns found 0 remaining. No real row was touched. The snapshot's small deltas (+1 clip, +1 v2 post, a few cents) are real production activity during the run; `sbx_rows` was 0 at open and close.
* **Build & git:** tsc clean; the merge tree equals the branch tree; pushes to the branch and main were verified; tags `pre-BL-934`, `post-BL-934`, `pre-merge-BL-934`, `post-merge-BL-934`; BACKLOG 240 to 241; `checkpoint/BL-723` not merged; the worktree was removed and confirmed gone. A sandbox proof script had a type error that failed one build; it was fixed in a follow-up commit and the build is clean.

**A v2 campaign now auto-pauses the moment its true committed spend (all three legs) reaches budget, where before it counted only the poster's 45 percent and paused late; and the two owner repair tools now leave a v2 clip alone — fix-budget skips it, adjust refuses it — instead of scaling one leg of three.**
