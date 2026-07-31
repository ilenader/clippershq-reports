# BL-702 — merge round: BL-698 and BL-700 onto main

`main` moved `bbd369ae` to **`22212d26`**, verified by `git ls-remote` twice. Merge commits `754775f5` (BL-698) and `0446e29a` (BL-700), plus `22212d26` carrying only the BACKLOG entry. Tags `pre-merge-BL-702` (`bbd369ae`) and `post-merge-BL-702` (`22212d26`) are on origin.

---

## STEP 0 — truth per branch, with SHAs

| branch | SHA | on origin | ancestor of main before this round | what the diff actually contains |
|---|---|---|---|---|
| `checkpoint/BL-698` | `5ffb55f1` | yes | **no, genuinely unmerged** | **real source changes**: `src/app/api/earnings/route.ts`, `src/app/api/clips/mine/route.ts`, `src/components/clips/ClipCardNew.tsx`, `src/components/earnings/EarningsPremium.tsx`, plus four read-only `scripts/bl698-*` helpers and its BACKLOG entry |
| `checkpoint/BL-700` | `56703453` | yes | **no, genuinely unmerged** | **NOT a code change.** `git diff --name-only origin/main...origin/checkpoint/BL-700 \| grep -c "^src/"` returns **0**. BACKLOG plus three helper files: the already-applied migration SQL, an IG sound probe, a test |
| `checkpoint/BL-699` | `b1f3bb11` | yes | no | **NOT merged.** Live round, left alone |
| `checkpoint/BL-701` | `9bcbe7aa` | yes | **yes**, via `bbd369ae` | **NOT merged again.** Already on main |

**Stated plainly: BL-700 landed no code.** Its rules were applied to the database in its own round; merging its branch adds scripts and a BACKLOG entry and changes no application behaviour. BL-698 is the only branch in this round that changes what runs.

## Where the merge ran, and why not in the main worktree

`C:/b575` holds branch `main` at `91b84410`, roughly a hundred commits stale, **and** dirty with **77** entries (staged doc deletions, modified `BACKLOG.md` and `prisma/schema.prisma`). It was not touched. Re-checked at the end: still branch `main`, still `91b84410`, still 77 entries. The merge ran in a fresh detached worktree at the short path `C:/m702` with its own real `npm ci` (822 packages, exit 0). No `node_modules` junction. Pushed `HEAD:main`.

**One honest note on the push tooling.** `scripts/safe-push.mjs main` cannot be used from a detached worktree: it runs `git push origin main`, which resolves the *stale local* `main` ref (`91b84410`, checked out in `b575`), and GitHub correctly rejected it as non-fast-forward. No damage: `origin/main` is still `22212d26`. Both pushes were therefore done as `git push origin HEAD:main` followed by BL-288's own assertion, `git ls-remote origin refs/heads/main` == local HEAD, which passed both times. safe-push did push the tags successfully.

## Merges, one at a time, verified between

**BL-698 first.** One conflict, `BACKLOG.md` only, append-versus-append at the tail, resolved as a **union** keeping both entries. Verified before continuing: `TSC_EXIT=0`, `BUILD_EXIT=0`, all protected blobs unchanged.

**BL-700 second.** Same single `BACKLOG.md` conflict, same union resolution.

**BACKLOG counted with `grep -c`, never piped:** 108 entries at the merge base `f7a1a344`, **110** after BL-698, **111** after BL-700, **112** with this round's own entry, over 19809 lines. **Zero conflict markers** anywhere in the tracked tree.

## Confirmations on the merged result

**The withdrawal gate is byte-identical, which is the point of the round.** BL-698 aligns the display to the gate and must never alter it. `src/app/api/payouts/route.ts` is blob `a9c7164e973b5dc4140172a0ed01c982b0ff7f44` on `origin/main`, on `checkpoint/BL-698`, on `checkpoint/BL-700` and on the merged tree, so line 411 and the `effectiveCap` comparison at line 595 are unchanged **by construction, not by inspection**. Line 411 verbatim on both refs: `      // WHERE (matches GET handler + admin campaignAvailable math).` For the record, BL-698's own comments cite the gate as `payouts/route.ts:424` while the brief cites 411; both sit inside the same untouched block, and the file did not change either way.

**No stored earnings changed and BL-538's never-decrease guard holds.** The entire BL-698 source diff contains **0** `update`, `updateMany`, `create`, `delete` or `writeClipEarnings` calls, so nothing in this merge writes. Live, before and after the push, identical: 3675 APPROVED clips at **$10,234.47**, 6 FLAGGED at $113.50, **0 invariant violations** in every status bucket.

**The ban cascade shows suspension wording, not a missing video.** `ClipCardNew.tsx` branches on `clip.clipAccount?.status === "BANNED"` and renders *"This account is suspended, so this clip cannot be paid."* rather than the deleted-video sentence, and `clips/mine/route.ts` adds `status` to the `clipAccount` select so the branch can actually fire.

**The three REQUIRED_SOUND rules read enforcement `rank` from the database.** Read back live, read-only:

| campaign | rule | platform | enforcement |
|---|---|---|---|
| bees.n.honey | r7 | tiktok | **rank** |
| bees.n.honey | r8 | instagram | **rank** |
| Panic Baby | r9 | tiktok | **rank** |

**Auto-reject is off everywhere.** `isAutoRejectLive()` is `process.env.RULES_AUTO_REJECT_LIVE === "true"` (`src/lib/auto-reject-flag.ts:20`) and the variable is absent from both `.env` and `.env.local`, so it evaluates false. `auto-reject-flag.ts` `a8ff0f7a` and `payout-clamp-flag.ts` `2ca0a2a5` are byte-identical; neither flag was flipped. No campaign rule was added or modified and the migration SQL was **not** re-run.

## AFTER THE PUSH — the number the owner will be asked about

Measured on live production after the deploy with the branch's own read-only `scripts/bl698-measure.ts`, which uses the real `computeBalance` from `balance.ts` rather than a hand-rolled SQL copy, and which sets `APIFY_API_KEY=DISABLED` so no actor can run.

> **26 clippers. $392.45 leaves displayed balances.**

BL-698 published **$392.36 across 26**. **The clipper count matches exactly. The amount is $0.09 higher**, because tracking has retired more clips in the hours between BL-698's measurement and this deploy. 29 clippers hold retired earnings at all; only 26 see a balance move. The largest single drop is **$147.61** and the smallest is **$0.08**.

**No clipper is shown a reduction covering money they were already paid.** Retired money across the platform is $42.75 recoverable plus $3,510.26 frozen = **$3,553.01**, and only $392.45 of that leaves anyone's displayed balance. The clearest case: clipper `cmp7153e` holds **$1,329.31** of retired earnings across 48 clips and sees exactly **$15.45** disappear, their entire displayed balance, because everything else was already paid out. That is the $3,553.01 near-miss avoided, confirmed on live data rather than argued. Both safety assertions PASS: **nobody's displayed balance increases, and none goes negative.**

**All eleven in-flight payout requests are unchanged in value**, queried before and after the push and identical row for row: 11 requests, `sum(amount)` **$474.19**, `sum(finalAmount)` **$423.15**. Three belong to affected clippers, and their locked amounts are untouched: `cmosj3qk` $90.00, `cmpfozzs` $22.70, `cmpl310f` $16.05. Handles are redacted to 8 characters by the scripts themselves and no wallet address was read or printed.

## Accessibility review of the BL-698 UI diff

**GO-WITH-NOTES, nothing merge-blocking.** Verified passing: both notices are real text nodes, not tooltips (SC 1.1.1, 4.1.2); the `line-through` on the earned figure is decorative only, because "$0.00 payable" and "$X.XX earned" carry the meaning in words and NVDA and JAWS announce neither `line-through` nor `<s>` (SC 1.4.1); new text measures 7.1:1 to 18.4:1 (SC 1.4.3); the explanation precedes the figures in reading order; lucide-react icon, no emoji, no dashes as bullets.

**Follow-ups, none fixed here because this round is merge-only.** (F1, highest value) the earnings-page sentence says *"Clips whose video is not available"* to everyone, so a clipper hit by the ban cascade reads a line that is false for them; the card splits the two cases and the page does not, and the API's `unavailableClips: { count, removedFromBalance }` carries no ban/video split to fix it with. (F2) *"This account is suspended"* names no handle for a clipper with several connected accounts. (F3) the enforcement branch gets no non-blaming second sentence while the deleted-video branch does. (F4) the "See which clips are affected" link measures 4.57:1 where it likely sits but 3.82:1 nearer the hero gradient's accent corner, worth a picker check on the rendered page. (F6) `globals.css` sets `--text-primary`, `--text-secondary` **and** `--text-muted` all to `#ffffff` in `.dark`, a collapsed token hierarchy that silently defeats every muted-text usage app-wide; upstream of this branch and worth its own round.

## Gates, honestly

`npm ci` **exit 0** (822 packages), then `npx prisma generate` **exit 0** before any typecheck, because `npm ci` wipes the generated client. `npx tsc --noEmit` **TSC_EXIT=0 with 0 output lines**. `npm run build` **BUILD_EXIT=0**, read from a log with the exit code echoed directly, never through a pipe. Prebuild: BYPASS detector **0 violations**, removed-fields **OK**, **hooks gate 0 errors / 11 warnings** (limit 11) with eslint **v9.39.4** confirmed present in the worktree, so the gate ran rather than silently no-opping. 61/61 static pages. One full tsc plus build after each merge.

## Safety

6 money files plus `tracking.ts`, `campaign-era.ts` and `campaign-rules.ts` **byte-identical by blob OID** on both refs: `clip-earnings-writer.ts` 7aa6be48, `earnings-calc.ts` 797e2098, `balance.ts` e887f80a, `tracking.ts` 847dcf70, `clip-earnings-invariant-middleware.ts` 61cef393, `money-decimal.ts` ef5cdae7, `campaign-era.ts` 106e16ad, `campaign-rules.ts` fc91216f. Also unchanged: `payouts/route.ts` a9c7164e, `apify.ts` **656bf4c0** so the BL-678 guards are intact and no Apify actor was run, `auto-reject-flag.ts` a8ff0f7a, `payout-clamp-flag.ts` 2ca0a2a5. No env flag flipped, no campaign rule added or modified, no `prisma migrate`, no DB write of any kind, no historical payment clawed back. Every database read was a `SELECT`. No heredocs; one shell at a time. NO dashes.

**Rollback:** `git revert -m 1 0446e29a` then `git revert -m 1 754775f5`, or `reset --hard pre-merge-BL-702`.
