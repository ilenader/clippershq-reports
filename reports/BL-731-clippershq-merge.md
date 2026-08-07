# BL-731 — merging the per-campaign withdrawal minimum, without moving anyone's verdict
**Merged to main** `ab455ac7` · **Was** `2ceb2eef` · **Merged** `checkpoint/BL-728` `fa037fa2` · 2026-08-07 · **Merge only**
## 0. Truth
`checkpoint/BL-728` = **`fa037fa2`** on origin. `git merge-base --is-ancestor` → **NOT an ancestor** of main
`2ceb2eef`, so genuinely unmerged. Merge base `6688bad0`. Diff **non-empty**: 18 files, **1711 insertions**, 1 commit.
**`checkpoint/BL-723` (`22039307`) was NOT merged** and is confirmed still not an ancestor — it targets
`business-api` and cannot be called by the owner's Login Kit app.
**Dirty worktree handling:** `C:/b575` was **both stale** (`91b84410` vs main `2ceb2eef`) **and dirty** (77 paths), so
the merge ran in a **separate clean worktree at `C:/m731`**, a short path, with `.env`/`.env.local` copied and a real
`npm ci` — **never a `node_modules` junction**. Re-checked after the push: b575 still `91b84410`, still 77 paths,
**exactly as found**.
## 1. The risk that governed this merge — 0 verdicts moved
Re-verified **on the merged tree**, not inherited from the branch. Both rules were computed **side by side on the
same live rows**: OLD = flat $10 floor; NEW = `resolveMinPayout(campaigns.minPayoutAmountDecimal)`, mirrored in SQL
as `NULL or <= 0 → 10, else the value`. All clipper-campaign pairs with a positive effective cap:
```
pairs_total can_old can_new blocked_old blocked_new verdicts_flipped newly_unable minimum_differs
   142        27      27       115          115            0              0              0
```
**0 flipped. 0 newly unable.** `minimum_differs = 0` because **all 33 campaigns hold NULL**, so NULL resolving to $10
is not an assertion here, it is a measurement. Nobody who can withdraw today became unable. No STOP was required.
## 2. What the $10 actually was, confirmed on the merged tree
Never per-campaign: a **global floor on the typed amount**, written as the literal `10` in **four** places with **no
shared constant**. Sites 1 (`api/payouts/route.ts`, the only gate that decides anything), 2
(`PayoutRequestFlow.tsx`, the first thing a clipper hits) and 3 (`payouts/page.tsx` submit validator) now **all** read
the per-campaign value via `resolveMinPayout` and share one message builder in `payout-minimum-shared.ts`, so they
cannot drift. Verified by diff: **exactly three live `< 10` gates were removed** and **no `< 10` comparison survives
in executable code** — the three remaining matches are explanatory comments.
## 3. TWO CORRECTIONS. The brief overstates what shipped.
**Site 4 does NOT read the per-campaign value.** It is the static sentence at `payouts/page.tsx:1081`, inside the
`useNewPayouts ? new : legacy` **else** branch, while `useNewPayouts` is an unconditional `const … = true` at `:378`.
It is **unreachable**. BL-728 left it deliberately and said so; deleting a legacy modal is a bigger change than a
withdrawal-gate round should carry. Being dead, it cannot drift into a clipper's view — but the brief's expectation
that all four now read the per-campaign value **is not what shipped**, and I will not report it as though it were.
**A FIFTH copy exists, and it is LIVE.** `help/help-redesigned.tsx:72` reads *"Minimum payout is $10 per campaign."*,
rendered by `help/page.tsx`, clipper-facing. **BL-728's report claims the dead sentence "is now the only place in the
repo where that literal still appears in copy" — that claim is false.** It **gates nothing** and is still accurate
today because every campaign is NULL, but it becomes wrong for that campaign the moment the owner sets any minimum
other than $10. Not fixed here: this is a merge. It wants its own round, together with site 4.
## 4. Unchanged, proven by enumerating every removed line
Only **14 source lines** were removed across the entire merge, and each is one of the three live gates, its replaced
copy, or a type/select widening. The **per-campaign availability rule**, the **global clamp**, the **9%/4% fee** and
the **`videoUnavailable` exclusion** have **no removed or altered line**; the only additions touching them are a
comment and two new **read-only** aggregates that themselves carry `videoUnavailable: false`.
Nothing in payout creation, the 10s dedupe or the cap was touched, so **BL-696's no-double-pay** and **BL-627's
no-overpayment** survive **by construction**: this round adds a **refusal**, and a refusal can only block, never grant.
**Money files byte-identical by blob OID on main, on the branch, AND on the merged commit:**
```
ac5be7de clip-earnings-writer  797e2098 earnings-calc  e887f80a balance  83ce4bab tracking
61cef393 clip-earnings-invariant-middleware  ef5cdae7 money-decimal  106e16ad campaign-era
```
## 5. Conflicts — both unioned, both sides kept
Two, both because BL-729 had touched the same files. **`BACKLOG.md`**: 123 shared + BL-728 + BL-729 = **125 by
`grep -c`** (never piped to `head`), **one each** of BL-728 and BL-729, **0 markers**. **`admin/campaigns/page.tsx`**
`openEdit`: BL-729's `setTypeLabelError(false)` **and** BL-728's five minimum-state resets both kept, neither dropped.
**0 conflict markers anywhere in the tree**, re-checked on the committed merge.
## 6. Schema — confirmed, not re-applied
`campaigns.minPayoutAmountDecimal numeric(18,4)`, `is_nullable=YES`, no default, **already on prod**. Confirmed
against `information_schema` and **not re-run**. **No `prisma migrate`.** `npx prisma generate` only, run **after**
`npm ci` because `npm ci` wipes the generated client; the client was then confirmed to carry the column.
## 7. Gates, stated honestly
`npm ci` **exit 0**, 822 packages, no junction. `prisma generate` **exit 0**. `tsc --noEmit` **0 errors, exit 0**.
`npm run build` **exit 0**, "Compiled successfully", read from a log with the exit code **echoed, never piped**.
Hooks gate **0 errors, 11 warnings — at the limit of 11**, with **eslint v9.39.4 confirmed present** so the gate is
not silently a no-op. Push verified by `git ls-remote`: **origin/main == local == `ab455ac7`**. `safe-push.mjs`
printed a **false failure** — it cannot verify a `src:dst` refspec from a detached worktree (the BL-727 trap);
`ls-remote` is the authority and it agrees.
## 8. THE NUMBER THE OWNER WILL BE ASKED ABOUT
Re-measured on live data **after** the push: **115 clipper-campaign pairs holding $332.00 are stranded under the
floor.** BL-728 reported **111 pairs / $324.33**; BL-693 had found only three.
**This merge did not change that number.** The proof is in §1: old and new rules were evaluated on the *same* rows
and returned identical verdicts, with `minimum_differs = 0`. The gap from BL-728's figure (**+4 pairs, +$7.67**) is
ordinary data drift between their measurement and now — earnings accrued, payouts moved — **not merge effect**. The
pre-push and post-push runs are byte-identical. If those clippers message the owner, the answer is that they were
already below the floor before this shipped, and nothing here moved them.
## 9. STILL UNVERIFIED — do not read this merge as evidence
The owner's **blast-radius confirmation dialog**, the one that tells him how many clippers a raise would strand, has
**not been exercised by click-through** — not by BL-728, not by this round. Its route and arithmetic exist and
typecheck; **nobody has pressed the button.** It remains untested end to end.
## 10. What did not change
**No campaign minimum was raised or lowered** — all 33 still NULL, `minimums_set = 0`. No clip status or earnings
changed and **no payout was created, modified, approved or cancelled**: 157 payout rows, 3,370 approved clips,
$7,880.46, **invariant 0 violations**. Read-only SQL throughout; handles hashed, **no wallet address selected
anywhere**.
**Rollback:** `git revert -m 1 ab455ac7`. The column may stay — nullable, all NULL, unread by the reverted code.
