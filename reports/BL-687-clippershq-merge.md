# BL-687 — merge round, BL-686 onto main

## NO WRONG REFUSAL HAS BEEN OBSERVED, AND NO REFUSAL AT ALL HAS BEEN OBSERVED EITHER, SO THIS ROUND DOES NOT CLAIM THE RULE IS WORKING IN PRODUCTION. `origin/main` moved `43a4d4b1` → `765bb0e4`, verified origin==local. All the merge-side proofs hold: `apify.ts` byte-identical with all 11 BL-678 guards intact, the fail-open contract re-verified on the merged tree (ten unreadable timestamp shapes and a future-dated post all ACCEPT), the 5-minute skew tolerance present, TikTok and YouTube unchanged, the earnings invariant at 0 violations and earnings up not down. But **only three Instagram submissions have landed since the push, all three within 3.5 minutes of it and therefore almost certainly on the OLD code, and none at all in the 22 minutes since.** There is no post-deploy sample yet. The owner's own check queries are in the watch section.

**2026-07-30 · MERGE ONLY. No source file was written or edited by this round.**
**Base** `43a4d4b1` (`post-merge-BL-685`) · **Result** `765bb0e4` · **Tags** `pre-merge-BL-687` (43a4d4b1) → `post-merge-BL-687` (765bb0e4), both pushed.

---

## STEP 0 — truth, with the SHA

| branch | SHA | ancestor of main before this round? | `.ts` diff |
| --- | --- | --- | --- |
| `origin/checkpoint/BL-686` | **`19020554de116f625f354005686335e571772fcc`** | **NO, genuinely unmerged** (`git merge-base --is-ancestor` returned false) | **NON-EMPTY**: 3 `.ts` files, **433 insertions, 2 deletions** |

The `.ts` diff, before any merge, so the claim is not made from the merge result:

```
 scripts/test-bl-686-instagram-freshness.ts | 219 +++++++++++++++++++++++++++++
 src/lib/clipper-submit-core.ts             | 196 ++++++++++++++++++++++++++
 src/lib/scraper-providers/hikerapi.ts      |  20 ++-
 3 files changed, 433 insertions(+), 2 deletions(-)
```

**Nothing a live round holds was merged.** Exactly one branch was merged, `checkpoint/BL-686`, and nothing else was touched.

### The dirty main worktree, and what I did about it

**`C:/b575` holds the `main` branch and is both STALE and DIRTY:** HEAD at `91b844105a232225211835fa7da7aaf0414004ae`, far behind `43a4d4b1`, with **77 uncommitted files**. I did not touch it, did not stash it, and did not check out `main` anywhere.

Instead I created a **separate clean worktree at the short path `C:/m687`, detached at `origin/main`**, merged there, and pushed `HEAD:main`. `node_modules` was installed in place by `npm ci` and **never junctioned**. Re-checked after the push: `C:/b575` is still on `main` at `91b84410` with the same **77** dirty files, exactly as found.

**The consequence the owner should know, unchanged from BL-685:** because the push went `HEAD:main` from a detached worktree, the shared repo's LOCAL `main` ref still points at `91b84410` inside `C:/b575`. **`origin/main` is correct at `765bb0e4`**; whoever owns that worktree needs to commit or clear its 77 files and pull.

---

## The merge

`git merge --no-ff origin/checkpoint/BL-686`. **Clean, no conflicts.**

```
 BACKLOG.md                                 |  14 ++
 docs/BL-686-IG-FRESHNESS.md                | 310 +++++++++++++++++++++++++++++
 scripts/test-bl-686-instagram-freshness.ts | 219 ++++++++++++++++++++
 src/lib/clipper-submit-core.ts             | 196 ++++++++++++++++++
 src/lib/scraper-providers/hikerapi.ts      |  20 +-
 5 files changed, 757 insertions(+), 2 deletions(-)
```

**Exactly one production file changed: `src/lib/clipper-submit-core.ts`.** `hikerapi.ts` is a comment correction with zero behaviour change.

### BACKLOG, unioned and counted with `grep -c`, never piped through `head`

| ref | `^## BL-` entries |
| --- | --- |
| `origin/main` before the round | **104** |
| `checkpoint/BL-686` | 105 |
| **merged result** | **105** |

**104 + 1 = 105. The union is exact and nothing was lost.** BACKLOG auto-merged with no conflict. Spot-checked that earlier entries survived: BL-682 present, BL-683 present, BL-686 present. (BL-684 and BL-685 have no BACKLOG entry of their own by design, being an audit round and a merge round; that is their authors' choice, not a loss here.)

### Conflict markers

Repo-wide across `BACKLOG.md`, `src/`, `scripts/`, `docs/` and `prisma/`: **0 conflict markers**.

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
| `src/lib/campaign-rules.ts` | `fc91216f` | IDENTICAL |
| `src/lib/apify-hard-off.ts` | `29258a5d` | IDENTICAL |
| `src/lib/scraper-providers/apidojo.ts` | `d860cf4c` | IDENTICAL |
| `src/lib/account-profile.ts` | `44aaea8c` | IDENTICAL |
| `src/lib/verify-cascade.ts` | `69e1a9a5` | IDENTICAL |

`tracking.ts` is not in the diff.

### All 11 BL-678 guards intact, and the dead chain not revived

Counted on the merged tree with `grep -c`:

| file | guarded paths | count |
| --- | --- | --- |
| `src/lib/apify.ts` | five request builders, `BL-678 GUARD n of 5` | **5** |
| `src/lib/scraper-providers/apidojo.ts` | four exported actor functions behind one chokepoint | **4** |
| `src/lib/account-profile.ts` | `apify hard off (BL-678)` | **1** |
| `src/lib/verify-cascade.ts` | `apify hard off (BL-678)` | **1** |
| | **total** | **11** |

`export const APIFY_HARD_OFF: true = true;` is present, so no environment variable can re-enable Apify. `skipHikerOverlay: true` still appears twice in `apify.ts`, unchanged, so **the dead chain was not revived**. **No Apify actor ran at any point in this round.**

### Fail open, RE-VERIFIED on the merged tree rather than inherited

This is the whole safety of the change, so it was re-run against the merged working tree, not taken on trust from BL-686's own branch:

```
--- 2. fail open: an unreadable timestamp is ACCEPTED, never refused ---
PASS  harvest returned null (provider miss, cooldown, 404, timeout, throw) -> unknown -> ACCEPTED
PASS  harvest returned a non-object -> unknown -> ACCEPTED
PASS  media object with no taken_at at all -> unknown -> ACCEPTED
PASS  taken_at is null -> unknown -> ACCEPTED
PASS  taken_at is zero -> unknown -> ACCEPTED
PASS  taken_at is negative -> unknown -> ACCEPTED
PASS  taken_at is NaN -> unknown -> ACCEPTED
PASS  taken_at is a non-numeric string -> unknown -> ACCEPTED
PASS  taken_at is a pre-2015 unit-scale bug -> unknown -> ACCEPTED
PASS  empty media object -> unknown -> ACCEPTED
```

**Ten of ten. An absent or unreadable Instagram timestamp results in ACCEPTANCE on the merged tree.**

### The skew tolerance is present, and the boundary resolves toward accepting

`src/lib/clipper-submit-core.ts:118` → `export const IG_FRESHNESS_SKEW_TOLERANCE_MS = 5 * 60 * 1000;`

```
--- 4. the boundary: ambiguity resolves toward ACCEPTING ---
PASS  29 min (inside the advertised window) ACCEPTED
PASS  30 min (exactly the advertised window) ACCEPTED
PASS  31 min (just past the window, inside tolerance) ACCEPTED
PASS  34 min (still inside tolerance) ACCEPTED
PASS  exactly at the tolerance edge ACCEPTED (strict >, never >=)
PASS  36 min (past window + tolerance) refused
PASS  a post dated in the SERVER'S FUTURE (clock disagreement) is ACCEPTED  ageMs=-3600000
PASS  a millisecond-valued taken_at is read correctly, not multiplied
```

Plus, on the merged tree: the three outcomes stay distinguishable, and the UTC comparison is byte-identical under five timezones including `+02:00`.

### TikTok and YouTube unchanged

Their comparison line `if (diffMs > MAX_CLIP_AGE_MS) {` is present verbatim, exactly once. `evaluateInstagramFreshness` is called **exactly once**, at `clipper-submit-core.ts:432`, behind `platform === "instagram"`. No TikTok or YouTube code path was touched.

### The harness result, and the one FAIL, attributed honestly

`scripts/test-bl-686-instagram-freshness.ts` on the merged tree: **37 passed, 1 failed.**

**The single FAIL is a harness data precondition, not a behaviour defect, and the same run proves the behaviour is correct.**

```
FAIL  a real Instagram post older than the window is now identified as TOO OLD  age=8 min
```

Section 7 picks the two newest Instagram clips out of the database and asserts each is older than the window. Today the newest one was **8 minutes old**, a genuinely FRESH clip, so the function correctly returned `fresh` and the assertion's premise was false. Confirmed independently from the database, timestamps cast to `::text` against `now()`:

| DB `now()` | newest IG submit | minutes since |
| --- | --- | --- |
| 2026-07-30 15:00:19.021363+00 | 2026-07-30 14:53:38.212 | **7** |

The second clip in the same section, 75 minutes old, **did** return `too_old` and passed. So the failing line is the harness assuming "the newest clip is always stale", and **the correct reading is that a fresh clip was correctly accepted**, which is the outcome this round most wants. Nothing was changed to make it pass: this is a merge-only round, and BL-686's harness is left exactly as its author wrote it.

### The earnings invariant and the money totals

Read-only, timestamps cast to `::text` against DB `now()` = **2026-07-30 15:08:08.361191+00**:

| measure | value |
| --- | --- |
| clips | 4395 |
| **invariant violations** | **0** |
| **total earnings** | **$10,164.84** |
| APPROVED earnings | $10,051.34 |

Against BL-685's post-merge $10,048.36, that is **up $116.48 on natural view growth, never down**.

### Forward only

No migration, no data write, no backfill. `prisma migrate` was never run. The harness's own whole-population snapshot was identical before and after itself (`clips=4473 earnings=10157.82 base=9693.18 bonus=464.65 byStatus=APPROVED:3585,FLAGGED:6,PENDING:23,REJECTED:859`). **The 233 Instagram clips accepted since the 2026-07-22 cutover keep their status, earnings and payouts; nothing about them moved.**

---

## Build gates, stated honestly

| step | result |
| --- | --- |
| `npm ci` | **exit 0** (wipes the generated Prisma client) |
| `npx prisma generate` | **exit 0**, run **before** tsc |
| `npx tsc --noEmit` | **exit 0**, **0 output lines** |
| `npx eslint --version` | **v9.39.4 present**, so the hooks gate is real and not a silent no-op |
| `npm run build` | **BUILD_EXIT=0**, echoed from a captured log, **never piped through `tail`** |
| `check:prisma-bypass` | **0 violations** |
| `check:removed-fields` | **OK** |
| `lint:hooks` | **11 problems (0 errors, 11 warnings)**, at the ≤11 cap |
| static pages | **61/61** |

Both `tsc` and `next build` were actually run; neither was trusted alone.

---

## Push, verified per BL-288

```
git push origin HEAD:main     43a4d4b1..765bb0e4  HEAD -> main
local:  765bb0e4f093e941cbc89ad93e6ec4500df4ebcf
origin: 765bb0e4f093e941cbc89ad93e6ec4500df4ebcf
VERIFIED: origin/main == local HEAD
```

Tags `pre-merge-BL-687` and `post-merge-BL-687` both pushed.

**Rollback:** `git revert -m 1 765bb0e4`, or `git reset --hard pre-merge-BL-687`. **Reverting returns Instagram to accepting every clip regardless of age, which is the pre-BL-686 state, so the rollback is strictly no worse than before this round.**

---

## AFTER THE PUSH — the watch, and what it does and does not show

**Push completed at approximately 2026-07-30 15:09 UTC. Baseline taken immediately before: 1,894 Instagram clips, newest submit 2026-07-30 14:53:38.212.**

### What landed

| clip | submitted at | age at submit (provider `taken_at`) | outcome | DB status now |
| --- | --- | --- | --- | --- |
| 1 | 2026-07-30 15:09:24.444 | **UNKNOWN** (post now 404s, no timestamp readable) | accepted | REJECTED (by a human reviewer) |
| 2 | 2026-07-30 15:09:35.681 | **39 min** | accepted | APPROVED |
| 3 | 2026-07-30 15:12:46.393 | **1 min** | accepted | PENDING |

**Since 2026-07-30 15:12:46 there have been ZERO submissions on any platform**, Instagram, TikTok or YouTube, through to the last check at **2026-07-30 15:34:56**.

### Reading this honestly

**All three landed within 3.5 minutes of the push, which is inside the Railway build-and-swap window, so they almost certainly ran the OLD code.** Clip 2 is the evidence: at **39 minutes** it is past the 35 minute effective edge and would have been refused under the merged rule, yet it was accepted and subsequently approved. **That is not a defect in the rule; it is evidence the deploy had not yet taken effect one minute after the push.** Clip 1 (no readable timestamp) and clip 3 (1 minute old) would have been accepted either way.

**So there is NO post-deploy sample. This round does NOT claim the rule is working in production.** No wrong refusal has been observed, but no refusal of any kind has been observed either, and absence of evidence is not evidence here.

### One structural limitation the owner must know

**A REFUSED submission writes no row.** `processClipperSubmitLink` returns `fail(...)` before the transaction, so a clip refused as too old leaves nothing in the database at all. **The "refused as too old" count is therefore NOT measurable from the database, ever.** It exists only in the Railway application log, on the line BL-686 emits:

```
[FRESHNESS] outcome=too_old platform=instagram source=hiker-taken_at ageMs=<n> thresholdMs=1800000 toleranceMs=300000
```

### The exact queries for the owner

**Accepted Instagram submissions since the deploy** (run in the Supabase SQL editor):

```sql
SELECT now()::text AS db_now,
       "clipUrl",
       "createdAt"::text AS submitted_at,
       status
FROM clips
WHERE "isDeleted" = false
  AND lower("clipUrl") LIKE '%instagr%'
  AND "createdAt" > timestamp '2026-07-30 15:15:00'
ORDER BY "createdAt" DESC;
```

**Refusals, and the every-outcome view, in the Railway logs of the WEB service** (not the tracking cron):

```
[FRESHNESS] outcome=too_old      → refused as too old
[FRESHNESS] outcome=fresh        → verified fresh and accepted
[FRESHNESS] outcome=unknown      → could not verify, ACCEPTED (this is the fail-open path)
```

**What a WRONG refusal would look like, and what to do:** any `outcome=too_old` line whose `ageMs` is close to `2100000` (35 minutes), or a clipper reporting they were refused after submitting promptly. If that appears, roll back immediately with `git revert -m 1 765bb0e4` followed by a push, which restores accept-everything, the pre-BL-686 behaviour. An `outcome=too_old` at several hours is the rule working as designed, which is what BL-684 measured six of.

---

## Safety summary

Merge only; no source file was authored or edited by this round. The fail-open contract was **re-verified on the merged tree**, ten shapes, all accepting. The 11 BL-678 guards are intact, no Apify actor ran, and `apify.ts:2566`'s dead chain was not revived. TikTok and YouTube enforcement is unchanged. The change is forward only, with the 233 post-cutover Instagram clips untouched and no clip's status or earnings moved. The 6 money files plus `tracking.ts`, `campaign-era.ts` and `apify.ts` are byte-identical by blob OID on both refs. The refusal message ships no new copy: it reuses the exact string TikTok and YouTube already show, plain and about the clip's timing, never about the clipper. No `prisma migrate`. The dirty `C:/b575` worktree was left exactly as found. Every count comes from `grep -c`, never a pipe into `head`. NO dashes used as bullets.
