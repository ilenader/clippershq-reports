# BL-691 (ClippersHQ) — merge BL-689 (payout refusal stops rendering as a crash) to main

**2026-07-30 · MERGE ONLY. Merged to main at `9658675a`, verified on origin.** Base main `765bb0e4` (Merge BL-686) + `42af6f40` (checkpoint/BL-689). Tags `pre-merge-BL-691` / `post-merge-BL-691`.

**Nobody was unblocked and nothing about money moved.** Both facts are proven below by absence from the diff and by live measurement, not asserted.

---

## STEP 0 — truth, with SHAs

| question | answer |
|---|---|
| Is `checkpoint/BL-689` on origin? | **YES**, `refs/heads/checkpoint/BL-689` = **`42af6f4055b8aeee77cc43a97978c3af1fca96e3`**, exactly the SHA the brief named |
| Genuinely NOT on main? | **YES.** `git merge-base --is-ancestor 42af6f40 origin/main` → **NOT MERGED**. main was `765bb0e4` |
| Non-empty code diff? | **YES. 499 diff lines across `.ts` / `.tsx`** (counted with `grep -c`, never `head`), 6 files, 395 insertions / 14 deletions |
| Any drift since the branch was cut? | **None.** The merge base is **`765bb0e4`**, which IS `origin/main`. BL-689 was branched from the current tip, so its contribution and the merge diff are the same 6 files |
| Anything a live round holds? | **NO.** `checkpoint/BL-690` (`f7e32203`) exists on origin and was left alone; `merge-base --is-ancestor f7e32203 HEAD` → **correctly NOT merged** |
| Does it change a balance, eligibility gate or payout amount? | **NO**, proven in STEP 6 |

BL-689's contribution, which is also exactly the merge diff:

```
 BACKLOG.md                                   |  11 ++
 scripts/bl689-prove-messaging.ts             | 160 +++++++++++++++++++++++++++
 src/app/(app)/payouts/PayoutsRedesign.tsx    |  30 ++++-
 src/app/api/payouts/route.ts                 | 113 +++++++++++++++++--
 src/components/payouts/PayoutRequestFlow.tsx |  11 +-
 src/lib/payout-refusal.ts                    |  84 ++++++++++++++
 6 files changed, 395 insertions(+), 14 deletions(-)
```

**The merge introduced exactly BL-689's content and nothing else**, checked by blob OID on every file rather than by reading the diffstat:

```
SAME 57dc0e71  BACKLOG.md                                    SAME f8265b1d  src/app/api/payouts/route.ts
SAME 5e12b137  scripts/bl689-prove-messaging.ts              SAME cec06b50  src/components/payouts/PayoutRequestFlow.tsx
SAME d884baa9  src/app/(app)/payouts/PayoutsRedesign.tsx     SAME 84d5be6c  src/lib/payout-refusal.ts
```

Every one is byte-identical between `42af6f40:<f>` and the merge commit. No drift, no re-resolution, nothing introduced by the merge itself.

## The dirty main worktree, and what I did about it

**`C:/b575` holds `main` and is BOTH stale and dirty. I did not touch it.** It sits at **`91b84410`**, many merges behind the real main, with **77 dirty entries** including `M prisma/schema.prisma` and a large set of `D` deletions across `docs/`, `public/splash/` and `scripts/migrations/`. Merging there would have swept another session's staged work, including schema and migration deletions, into this merge.

So the merge was done in a **fresh, clean worktree at a short path, `C:/m691`**, created detached at `origin/main`, with its own `node_modules` from `npm ci` (**never junctioned**), and pushed with `git push origin HEAD:main`. Re-checked after the push: `C:/b575` is exactly as found, **`main @ 91b84410`, 77 dirty entries**, nothing staged, stashed or checked out by me.

## Conflicts, and the BACKLOG union

**There were none.** BL-689 was branched from the current main tip, so the merge applied cleanly with **0 unmerged paths**.

| check | before | after | verdict |
|---|---|---|---|
| `^## BL-` entries (`grep -c`, never `head`) | **105** | **106** | +1, exactly BL-689. No entry lost |
| `## BL-689` heading | 0 | 1 | added |
| Conflict markers repo-wide over `*.ts`, `*.tsx`, `*.md`, `*.json`, `*.prisma` | n/a | **0** | clean |

The merge commit has exactly two parents, `765bb0e4` and `42af6f40`.

---

## STEP 6 — confirmed on the merged result

### A refusal returns a 400 with its correct message, not a 500

The catch chain on the merged tree, in order:

```
:700   if (isPayoutRefusal(err))  ->  { error: err.message }, status: err.httpStatus     (400, or 409 for a duplicate)
:707   if (err.code === "P2002")  ->  409
:710   if (err.code === "P2034" || deadlock || could not serialize) -> 409
:714   catch-all                  ->  "Something went wrong. Please try again.", 500
```

**The fragile substring matcher is gone: `grep -c 'includes("Amount exceeds available balance")'` on the merged file returns `0`.** It was deleted, not widened, because widening a substring is how it broke.

Proven on the merged tree by the read-only harness, **17 passed, 0 failed**:

```
PASS  the OLD global message did NOT match the OLD substring matcher (this IS the bug)
PASS  so before BL-689 it fell through to the catch-all 500
PASS  GLOBAL_BALANCE_NEEDS_REVIEW is recognised by the typed guard  -> 400
PASS  GLOBAL_BALANCE_LOCKED_BY_PENDING_PAYOUT is recognised by the typed guard  -> 400
PASS  AMOUNT_EXCEEDS_GLOBAL_BALANCE is recognised by the typed guard  -> 400
PASS  AMOUNT_EXCEEDS_CAMPAIGN_BALANCE is recognised by the typed guard  -> 400
PASS  DUPLICATE_PAYOUT is recognised by the typed guard  -> 409
PASS  routing survives a total rewrite of the message (a future edit cannot re-break it)
PASS  a real Error is NOT treated as a refusal (genuine faults still 500)
PASS  a refusal can never carry a 5xx status
```

### Every throw on the payout path is matched. No orphan remains

| file:line (merged) | refusal | routed by | verdict |
|---|---|---|---|
| `payouts/route.ts:402` | `DUPLICATE_PAYOUT` | typed code → 409 | **MATCHED** |
| `payouts/route.ts:567` | `GLOBAL_BALANCE_NEEDS_REVIEW` | typed code → 400 | **MATCHED** (was the orphan) |
| `payouts/route.ts:575` | `GLOBAL_BALANCE_LOCKED_BY_PENDING_PAYOUT` | typed code → 400 | **MATCHED** |
| `payouts/route.ts:583` | `AMOUNT_EXCEEDS_GLOBAL_BALANCE` | typed code → 400 | **MATCHED** |
| `payouts/route.ts:593` | `AMOUNT_EXCEEDS_CAMPAIGN_BALANCE` | typed code → 400 | **MATCHED** |
| `payouts/[id]/review/route.ts:122` | `PAYOUT_NOT_FOUND` | exact sentinel at `:281` | **MATCHED** (owner path) |
| `payouts/[id]/review/route.ts:135` | `INVALID_TRANSITION:` | prefix at `:284` | **MATCHED** (owner path) |
| `payouts/[id]/review/route.ts:215` | `INSUFFICIENT_BALANCE:` | prefix at `:291` | **MATCHED** (owner path) |
| `payouts/[id]/review/route.ts:582` | internal diagnostic | caught locally at `:589` | never reaches the handler |
| `payouts/referral-request/route.ts:137` | `CommissionRaceError` | typed class at `:197` | **MATCHED** |

**Zero orphans on the merged tree.**

### Messaging only: the money logic is ABSENT from the diff

Scoped to **production source (`src/`)**, so the read-only proof harness and BACKLOG prose cannot flatter the result:

| grep over `git diff 765bb0e4 HEAD -- src/` | hits | meaning |
|---|---|---|
| the eligibility gate `Math.round(roundedAmount*100) > Math.round(effectiveCap*100)` | **0** | the threshold is untouched |
| `effectiveCap = ` / `globalAvailable = ` | **0** | both cap assignments are untouched |
| `GLOBAL_PAYOUT_CLAMP_ENABLED` | **0** | the clamp was not flipped |

**Stated honestly:** an unscoped grep does return three hits, and none of them is production code. One is a BACKLOG sentence quoting `effectiveCap = $0.00`, and two are inside `scripts/bl689-prove-messaging.ts`, the read-only harness, which recomputes the same arithmetic locally in order to verify it. I am naming them rather than letting a tidy zero stand unexplained.

Byte-identical by blob OID on both refs, covering every input to eligibility:

```
SAME 2ca0a2a5  src/lib/payout-clamp-flag.ts     (the clamp itself: NOT flipped)
SAME e887f80a  src/lib/balance.ts               (the balance computation)
SAME a37ff0cc  src/app/api/earnings/route.ts    (what the clipper is shown)
```

**`GLOBAL_PAYOUT_CLAMP_ENABLED` was NOT flipped**, and this matters: BL-690 proved disabling it is **not** a safe rollback, because it would let the overpaid clipper withdraw **$14.65** they are not owed.

### Nobody is unblocked

Measured live against the merged code:

| clipper | campaign available | global earned | global paid | **cap** | classification |
|---|---|---|---|---|---|
| **C-1** | $15.74 | $15.74 | $25.54 | **$0.00** | `GLOBAL_BALANCE_NEEDS_REVIEW` |
| **C-2** | $22.52 | $33.26 | $37.28 | **$0.00** | `GLOBAL_BALANCE_NEEDS_REVIEW` |
| **C-3** | $14.65 | $1,848.32 | $1,894.14 | **$0.00** | `GLOBAL_BALANCE_NEEDS_REVIEW` |

**C-1 + C-2 = $38.26**, the two clippers genuinely owed. **C-3 is the overpaid one**, paid $1,894.14 against $1,848.32 of countable earnings, and their $14.65 campaign figure is precisely the leak BL-690 warned about. **All three still compute to `$0.00`. This round changes what they are told and nothing about what they can take.**

An eligible clipper is unaffected end to end. The platform's most recent successful request, made today at `2026-07-30T15:21:53.814Z` for $14.05, still passes the gate: `earned=$47.00 paid=$32.61 locked=$14.05 globalAvail=$0.34`.

### No payout created, modified, approved or cancelled

`payout_requests: count=144  amount=$14,123.39` — read only, unchanged. The proof script writes nothing.

### No message accuses or blames a clipper

The permanent case reads: *"Something on our side is stopping this payout, not anything you did. Your earnings are safe. Open a support ticket in our Discord and the team will fix it."* It names the cause as ours, never says "manual review" (which reads as fraud suspicion), never invites a retry on a permanent condition, and points at a support route that exists. The merge also carries the fix for an empty state that told clippers who had genuinely earned *"Earn on an approved clip to unlock a payout."*

---

## Accessibility

The lead had reviewed this exact code in BL-689 and its findings were applied. Asked to re-confirm against the merged tree, it returned an **empty MUST-FIX list for the merge** and, notably, **withdrew one of its own BL-689 findings** after checking the source:

> *"CONFIRMED — you are right, I was wrong. [...] with a global of $0.00, every per-campaign value clamps to 0, fails the `> 0` filter, and the strip renders empty. A $52.86 strip beside a $0.00 hero cannot happen on that path. My BL-689 MUST-FIX 3 was a bad finding — I read the strip in isolation and did not trace the clamp. Withdrawn."*

It verified this at `api/earnings/route.ts:218` (`Math.min(b.available, balance.available)`) and `payouts/page.tsx:214` (`if ((cb.available || 0) > 0)`). It also endorsed the two substitutions I made to its recommended copy, in particular dropping *"our team has been told"* once I confirmed nothing on that path notifies anyone: *"Copy that promises a notification which does not fire is worse than no copy at all."*

**One caveat it raised, recorded rather than actioned:** the clamp is behind a kill-switch, so if `GLOBAL_PAYOUT_CLAMP_ENABLED` were ever flipped off, raw per-campaign values would pass through and the mismatch it originally described would become reachable. That is a pre-existing property of BL-187-P2, it is not introduced here, and it is a further reason not to flip that flag.

**It also declined to certify something it could not:** running in a fresh session with no BL-689 artifacts, it said plainly it had no stored baseline and would not manufacture a comparison it did not perform, and asked me to run the blob-OID check instead. **I ran it** (the six-file table above), and it comes back clean.

---

## Gates, stated honestly

* **`npm ci` exit 0**, then **`npx prisma generate` exit 0**, in that order and **before** typecheck, so the wiped Prisma client was regenerated first.
* **`npx tsc --noEmit` exit 0**, with **0 lines** of output.
* **`npm run build` BUILD_EXIT=0**, read from a captured log and echoed directly, never piped through `tail`. `check:prisma-bypass` **0 violations across `src/` + `scripts/`**, `check:removed-fields` OK, `lint:hooks` **11 problems (0 errors, 11 warnings)** at the ≤11 cap, compiled successfully, **61/61** static pages.
* **eslint v9.39.4 present** (`npx eslint --version`), so the hooks gate is real and not a silent no-op.
* **No `prisma migrate`** was run; the merge contains no schema change of any kind.
* Counts taken with `grep -c`, never piped to `head`.

## Safety

* **6 money files + `tracking.ts` + `campaign-era.ts` BYTE-IDENTICAL by blob OID on BOTH refs**: writer `7aa6be48`, earnings-calc `797e2098`, balance `e887f80a`, tracking `847dcf70`, middleware `61cef393`, money-decimal `ef5cdae7`, campaign-era `106e16ad`. Stronger still, **none of the eight appears in the merged diff at all** (`git diff --name-only` filtered for them returns 0).
* No handle, email or wallet address appears anywhere. Clippers are C-1 / C-2 / C-3, matching BL-688's private mapping.
* **NO dashes** used as bullets.
* **Rollback:** `git revert -m 1 9658675a`, or `reset --hard pre-merge-BL-691`. **Do NOT roll back by flipping `GLOBAL_PAYOUT_CLAMP_ENABLED`**, which BL-690 proved would let the overpaid clipper withdraw $14.65.

## What is still open, and is the owner's call

Whether C-1 and C-2 should receive their **$38.26** is untouched by this round. So is the fact that the hero button is `disabled={available <= 0}`, which means the clippers most in need of an explanation are currently the ones who cannot reach the screen that would give them one. Both were flagged in BL-689 and neither is a merge concern.
