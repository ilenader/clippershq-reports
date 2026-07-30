# BL-685 — merge round, two branches onto main

## BOTH BRANCHES ARE ON MAIN AND VERIFIED ON ORIGIN. `origin/main` moved `fdde504f` → `43a4d4b1`, confirmed byte for byte against local HEAD. The 6 money files, `tracking.ts`, `campaign-era.ts`, `apify.ts` and `campaign-rules.ts` are all BYTE-IDENTICAL by blob OID. All 11 BL-678 Apify guards are intact and no Apify actor ran. The earnings invariant is ZERO violations across the full live population of 4,457 clips, and total earnings are $10,048.36, up $89.10 from BL-683's $9,959.26 on natural view growth, never down.

**2026-07-30 · MERGE ONLY. No source file was written or edited by this round; every line that landed came from the two branches.**
**Base** `fdde504f` (`post-merge-BL-676`) · **Result** `43a4d4b1` · **Tags** `pre-merge-BL-685` (fdde504f) → `post-merge-BL-685` (43a4d4b1), both pushed

---

## STEP 0 — truth per branch, with SHAs

| branch | SHA | ancestor of main before this round? | files in diff |
| --- | --- | --- | --- |
| `origin/checkpoint/BL-682` | `7e1bef5c1446b0944ee1f09c702964f7b11f5c19` | **NO, genuinely unmerged** (`git merge-base --is-ancestor` returned false) | **4**, non-empty |
| `origin/checkpoint/BL-683` | `1abad01352b04572d19e79f2282b69fe2a64bdb2` | **NO, genuinely unmerged** | **3**, non-empty |

Both were present on origin at fetch time and both carried exactly one commit ahead of `fdde504f`. Neither diff was empty.

**BL-682 files:** `BACKLOG.md`, `scripts/bl682-hiker-probe.ts` (new), `scripts/test-bl-682-instagram-caption.ts` (new), `src/lib/clipper-submit-core.ts`.
**BL-683 files:** `BACKLOG.md`, `scripts/bl683-clear-rejected-earnings-residue.ts` (new), `scripts/bl683-verify-population.ts` (new). **Zero source files**, exactly as its report claimed.

**Nothing a live round holds was merged.** `git branch -r` matched no remote branch for BL-686, so there was nothing to avoid; only the two named branches were merged.

**The other project's report files were NOT touched.** The reports repo carries four relevant files: `BL-682.md` and `BL-683.md` (another project's, untouched) and `BL-682-clippershq-instagram-caption.md` and `BL-683-clippershq-rejected-earnings-residue.md` (this project's). This round wrote only its own new file.

### The dirty main worktree, and what I did about it

**`C:/b575` holds the `main` branch, and it was both STALE and DIRTY: HEAD at `91b84410` (far behind `fdde504f`) with 77 uncommitted files.** I did not touch it, did not stash it, and did not check out `main` anywhere.

Instead I created a **separate clean worktree at the short path `C:/m685`, detached at `origin/main`**, merged there, and pushed `HEAD:main`. `node_modules` was installed in place by `npm ci` and **never junctioned**. Re-checked after the push: `C:/b575` is still on `main` at `91b844105a232225211835fa7da7aaf0414004ae` with the same 77 dirty files, exactly as found.

**One consequence the owner should know:** because the push went `HEAD:main` from a detached worktree, the shared repo's LOCAL `main` ref still points at `91b84410` inside `C:/b575`. **`origin/main` is correct at `43a4d4b1`**; whoever owns that worktree needs to commit or clear its 77 files and pull. Nothing was lost and nothing was overwritten.

---

## The merges, one at a time, verified between

### Merge 1 — BL-682 → `43d3c0870f0a0f3862a1f2e0327171b26a47ba6e`

`git merge --no-ff origin/checkpoint/BL-682`. **Clean, no conflicts.** 4 files, 369 insertions, 0 deletions.
Verified immediately after: BACKLOG at 103 entries, 0 conflict markers, and all nine tracked blob OIDs unchanged.

### Merge 2 — BL-683 → `43a4d4b1e4784b92bbc87d8961c336c2edca19ef`

`git merge --no-ff origin/checkpoint/BL-683`. **One conflict, in `BACKLOG.md` only**, at lines 19687 / 19699 / 19711: both branches appended their own `## BL-` entry at the same position.

**Resolved as a UNION, both sides kept in full.** No line of either entry was dropped, shortened or reordered; only the three conflict markers were removed. Counted with `grep -c`, never piped through `head`:

| ref | `^## BL-` entries |
| --- | --- |
| `origin/main` before the round | **102** |
| `checkpoint/BL-682` | 103 |
| `checkpoint/BL-683` | 103 |
| **merged result** | **104** |

**102 + 1 + 1 = 104. The union is exact and nothing was lost.** `grep -c '^## BL-682'` = 1 and `grep -c '^## BL-683'` = 1, so both entries survived.

### Conflict-marker sweep

Repo-wide across `BACKLOG.md`, `src/`, `scripts/` and `prisma/`: **0 conflict markers**.

### Total merged diff versus pre-merge main

```
 BACKLOG.md                                       |  23 ++
 scripts/bl682-hiker-probe.ts                     | 108 ++
 scripts/bl683-clear-rejected-earnings-residue.ts | 141 ++
 scripts/bl683-verify-population.ts               |  88 ++
 scripts/test-bl-682-instagram-caption.ts         | 154 ++
 src/lib/clipper-submit-core.ts                   |  95 ++
 6 files changed, 609 insertions(+), 0 deletions(-)
```

**Exactly one source file changed in the whole round: `src/lib/clipper-submit-core.ts`, additive only, zero deletions anywhere.**

---

## CONFIRMED ON THE MERGED RESULT

### Byte-identity by blob OID, `git rev-parse` on BOTH refs

| file | blob OID | verdict |
| --- | --- | --- |
| `src/lib/clip-earnings-writer.ts` | `7aa6be48` | IDENTICAL |
| `src/lib/earnings-calc.ts` | `797e2098` | IDENTICAL |
| `src/lib/balance.ts` | `e887f80a` | IDENTICAL |
| `src/lib/tracking.ts` | `847dcf70` | IDENTICAL |
| `src/lib/clip-earnings-invariant-middleware.ts` | `61cef393` | IDENTICAL |
| `src/lib/money-decimal.ts` | `ef5cdae7` | IDENTICAL |
| `src/lib/campaign-era.ts` | `106e16ad` | IDENTICAL |
| **`src/lib/apify.ts`** | **`656bf4c0`** | **IDENTICAL** |
| **`src/lib/campaign-rules.ts`** | **`fc91216f`** | **IDENTICAL** |

`tracking.ts` is not in the diff. Both branches' central safety claim holds on the merged tree, not merely on their own branches.

### All 11 BL-678 Apify guards intact, and no actor ran

All four guard-bearing files are byte-identical to pre-merge main: `apify.ts` `656bf4c0`, `apidojo.ts` `d860cf4c`, `account-profile.ts` `44aaea8c`, `verify-cascade.ts` `69e1a9a5`. Counted with `grep -c`:

| file | guarded paths | count |
| --- | --- | --- |
| `src/lib/apify.ts` | five request builders, each labelled `BL-678 GUARD n of 5` | **5** |
| `src/lib/scraper-providers/apidojo.ts` | four exported actor functions behind the single `getApifyToken()` chokepoint | **4** |
| `src/lib/account-profile.ts` | `apify hard off (BL-678)` | **1** |
| `src/lib/verify-cascade.ts` | `apify hard off (BL-678)` | **1** |
| | **total** | **11** |

**No Apify actor ran, and it is structurally impossible for one to have.** `src/lib/apify-hard-off.ts` exports `APIFY_HARD_OFF: true` as a `const`, reading no environment variable, so no value in Railway or in any `.env.local` can re-enable Apify. The live proof run below logged **0** `[APIFY-HARD-OFF]` skip lines, meaning no guarded path was even entered, let alone crossed.

### Instagram delivers all five fields to the evaluator

`npx tsx scripts/test-bl-682-instagram-caption.ts` on the merged tree: **16 PASS, 0 FAIL** (counted with `grep -c`), exit 0.

| live Instagram clip | caption | sound id | hashtags | postedAt | duration |
| --- | --- | --- | --- | --- | --- |
| 1 | present, 1104 chars | present | 0 in this caption | present | 8s |
| 2 | present, 172 chars | present | 0 in this caption | present | 8s |
| 3 | present, 172 chars | present | 0 in this caption | present | 10s |

```
PASS  Instagram captions now reach the evaluator  3/3
PASS  Instagram sound ids now reach the evaluator  3/3
```

**Honest note on hashtags:** these three posts contain no hashtags, so `hashtags=0` is the true value, not a missing field. The plumbing is proven by the TikTok rows below, which carry `hashtags=3` through the identical field.

**Fail-open proven on all four failure shapes**, none of which threw or fabricated a value: a provider miss (null), a caption-less post, an image-only carousel, and a deleted or private body. Each records `captionPresent=false`.

### TikTok unbroken

```
clip cms78n1ss… rawPresent=true captionPresent=true captionLen=64 soundIdPresent=true hashtags=3
clip cms78ds6g… rawPresent=true captionPresent=true captionLen=64 soundIdPresent=true hashtags=3
clip cms77fdk7… rawPresent=true captionPresent=true captionLen=64 soundIdPresent=true hashtags=3
PASS  TikTok caption arrival is unbroken  3/3
```

### The earnings invariant and the money totals, live

Queried read-only against DB `now()` = **2026-07-30 10:11:57.423449+00**, timestamps cast to `::text`:

| measure | value |
| --- | --- |
| clips in the population | **4457** |
| **invariant violations** (`abs(earnings − (baseEarnings + bonusAmount)) > 0.01`) | **0** |
| max drift | **$0.0100**, inside the ±$0.01 tolerance |
| **total earnings** | **$10,048.36** |
| APPROVED earnings | $9,934.86 |
| total baseEarnings | $9,586.67 |
| total bonusAmount | $461.70 |

**Against BL-683's post-fix figures, every direction is up or flat, none down:**

| measure | BL-683 | now | delta |
| --- | --- | --- | --- |
| total earnings | $9,959.26 | **$10,048.36** | **+$89.10** |
| APPROVED earnings | $9,845.76 | $9,934.86 | +$89.10 |
| baseEarnings | $9,498.11 | $9,586.67 | +$88.56 |
| bonusAmount | $461.16 | $461.70 | +$0.54 |
| clips | 4,411 | 4,457 | +46 |

**Total earnings are unchanged apart from natural growth and never went down.** The +$89.10 is view accrual on live clips plus 46 new submissions, and it is identical on the total and the APPROVED line, which is what natural growth looks like. BL-683's cleanup holds: the invariant that stood at 10 violations is still at 0, now across 46 more clips than when it was fixed.

### Nothing rendered, nothing auto-rejected

No clip status changed and no clipper's earnings or withdrawable balance moved: the only source file in the diff is `clipper-submit-core.ts`, which never writes a status or a money column outside `writeClipEarnings`, and the BYPASS detector confirmed **0 violations including its earnings-write check**. Auto-reject remains OFF. Nothing in this round renders to a clipper.

---

## Build gates, stated honestly

Run in order, in the clean worktree, each exit code echoed by me rather than inferred, and **never piped through `tail`**:

| step | result |
| --- | --- |
| `npm ci` | **exit 0** (this wipes the generated Prisma client) |
| `npx prisma generate` | **exit 0**, "Generated Prisma Client (7.8.0)", run **before** tsc |
| `npx tsc --noEmit` | **exit 0**, **0 output lines** |
| `npx eslint --version` | **v9.39.4 present**, exit 0, so the hooks gate is real and not a silent no-op |
| `npm run build` | **BUILD_EXIT=0**, read from a captured log |
| `check:prisma-bypass` | **0 violations** across `src/` + `scripts/` (prisma-bypass + earnings-write checks) |
| `check:removed-fields` | **OK**, 693 files scanned, no residual reads |
| `lint:hooks` | **11 problems (0 errors, 11 warnings)**, at the ≤11 cap |
| static pages | **61/61** generated |

`next build` was actually run; tsc alone was not trusted. No `prisma migrate` was run at any point.

---

## Push, verified per BL-288

```
git push origin HEAD:main     fdde504f..43a4d4b1  HEAD -> main
local:  43a4d4b1e4784b92bbc87d8961c336c2edca19ef
origin: 43a4d4b1e4784b92bbc87d8961c336c2edca19ef
VERIFIED: origin/main == local HEAD
```

Tags `pre-merge-BL-685` and `post-merge-BL-685` both pushed to origin.

**Rollback:** `git revert -m 1 43a4d4b1` undoes BL-683 alone; `git revert -m 1 43d3c087` undoes BL-682 alone; `git reset --hard pre-merge-BL-685` returns main to `fdde504f` entirely. BL-683 changed no source file, so reverting it changes no behaviour at all, only the BACKLOG entry and the two scripts; the database cleanup it performed is separate and is rolled back by the per-id SQL printed in its own report.

---

## Safety summary

Merge only; no source file was authored or edited by this round. The BL-678 Apify guard was not weakened on any of its 11 paths and no Apify actor ran. No clip status changed and no clipper's earnings or withdrawable balance moved. The earnings invariant is 0 violations post-merge across all 4,457 clips. The 6 money files plus `tracking.ts` and `campaign-era.ts` are byte-identical by blob OID via `git rev-parse` on both refs, as are `apify.ts` and `campaign-rules.ts`. Nothing renders to a clipper and auto-reject stays OFF. No `prisma migrate`. The other project's `BL-682.md` and `BL-683.md` were not touched. The dirty `C:/b575` worktree was left exactly as found. Every count in this document comes from `grep -c`, never from a pipe into `head`. NO dashes used as bullets.
