# BL-757 — merge BL-756 (per-clip CPM override) to main

**Result: MERGED AND VERIFIED PUSHED.** main `605af18c` → **`018c22ca`**. Merge only. No override was
applied to any clip, no clip's earnings, status or stamped CPMs changed, and the count of clips
carrying an override is **0** both before and after.

## STEP 0 — truth, recorded before anything was merged

| Question | Answer |
| --- | --- |
| Was checkpoint/BL-756 on origin? | Yes, **`fca0f636f6b3958492bce8bed45f54ef07a58330`** |
| Genuinely NOT an ancestor of main? | Yes. `git merge-base --is-ancestor origin/checkpoint/BL-756 origin/main` → **NO-NOT-ANCESTOR** |
| Non-empty diff? | Yes. **14 files, 1696 insertions, 5 deletions**, one commit `fca0f636` |
| Post-review fix on the tip? | Yes. The single commit is titled "with BL-754 gaps 1 and 2 closed as part of the build"; both fixes were read on the merged tree and are present (see CONFIRM below) |
| Was BL-723 merged? | **No.** Re-asserted after the push: `origin/checkpoint/BL-723` is NOT an ancestor of the new main |
| main starting point | `605af18c` (the required "605af18c or later") |

### The dirty worktree, and how it was handled
`C:/b575` holds the `main` branch and was **DIRTY: 77 staged/modified entries** belonging to another
session (staged deletions across docs/, scripts/, public/splash/, plus modified BACKLOG.md and
prisma/schema.prisma). It was **not touched**. The primary tree
`C:/Users/Game Centar/.../ClippersHQ` was on detached HEAD `de0169bd`, behind main, with untracked
files only, so `git checkout main` was impossible there as well.

The merge was therefore done in a **separate clean worktree at a short path, `C:/m757`**, created
detached at `origin/main`, with `.env` and `.env.local` copied in and **no node_modules junction**
(`npm ci` ran natively in the worktree). Afterwards `C:/b575` was re-checked and is **exactly as
found**: HEAD `91b84410`, branch `main`, 77 dirty entries. The primary tree is still `de0169bd`.
Because `main` was checked out elsewhere and could not be moved without disturbing b575, the push was
done as `git push origin HEAD:main` with the BL-288 assertion performed explicitly (below) rather
than through `safe-push.mjs`, whose `--branch` argument would have pushed the stale local `main` ref
(`91b84410`).

### tsc baseline, recorded on a CLEAN worktree BEFORE merging
```
TSC_BASE_EXIT=0   BASE_ERR_COUNT=0
```
**0 errors.** BL-753's report of "2 pre-existing errors" was an artifact of stray files in its own
worktree, exactly as this round was warned. Every tsc number below is measured against this 0.

## THE MERGE

`git merge --no-ff origin/checkpoint/BL-756` → `MERGE_EXIT=0`, **clean, zero conflicts**, so no union
resolution was needed. Merge commit **`018c22cab303e7b122cad74da1a17319c0c61c15`**.

* **Conflict markers: 0.** `git grep -E '^(<<<<<<<|>>>>>>>)'` over the whole tree returns 0. (A looser
  pattern that also matched `^=======` returned 78, all of them ordinary markdown rules in docs, which
  is why the real-marker pattern is the one reported.)
* **BACKLOG union, counted with `grep -c` and never piped to `head`:** main **134** entries,
  BL-756 **135**, merged **135**. Entries from main missing in the merged file: **0**. Entries added:
  **1**, `## BL-756 (2026-08-09) — per-clip CPM override, with BL-754 gaps 1 and 2 closed`. Nothing
  was dropped.

## GATES — every one actually run, with its real exit code from a log

| Gate | Command | Result |
| --- | --- | --- |
| npm ci | ran FIRST, before anything else | `NPMCI_EXIT=0` |
| prisma generate | run BEFORE tsc, and again after the merge changed schema.prisma | `PRISMA_EXIT=0`, client 7.8.0 |
| tsc | `npx tsc --noEmit > tsc-merged.log` | `TSC_MERGED_EXIT=0`, **0 errors, unchanged from the recorded baseline of 0** |
| next build | `npm run build > build.log 2>&1; echo BUILD_EXIT=$?` | **`BUILD_EXIT=0`** |
| hooks gate | `npm run lint:hooks` | `HOOKS_EXIT=0` — **0 errors, 11 warnings** (limit is 11) |
| eslint present | `node_modules/.bin/eslint` | **PRESENT**, so the gate did not silently no-op |
| prebuild chain | inside build.log | `check:prisma-bypass` + `check:removed-fields` + `lint:hooks` all ran |

The build exit code was echoed from a real run, never inferred and never piped through `tail`.

## CONFIRM ON THE MERGED RESULT — by code reading and the harness, on no real clipper's clip

`scripts/bl756-harness.ts` on the merged tree: **`HARNESS_EXIT=0`, 33 passed, 0 failed.**
`scripts/bl756-live-demo.ts` was deliberately **NOT run**, because it applies a real override to a
real clip and this round is a merge.

**1. Ratio-preserving scaling derives the owner CPM correctly on the non-round pair.**
On BL-743's live pair, clipper **$0.20** / owner **$0.1279**, scaling the clipper to **$0.50** yields
owner **$0.3198** (0.50 × 0.1279/0.20 = 0.31975, rounded 4dp ROUND_HALF_UP), guard gap 0.0001000 of
the 0.01 tolerance. Also passing at $0.33 → $0.2110, $0.005 → $0.0032, $1.25 → $0.7994,
$12.50 → $7.9938. The owner's own rule holds: a 50/50 campaign at $0.30 each, clipper set to $0.50,
gives owner $0.50 and a guard gap of exactly 0. `per-clip-cpm.ts:219-221` runs every step in
`Prisma.Decimal`, never IEEE float, and the ratio is taken from the **original** pair, so 12
successive overrides leave a gap of 0.0000556 rather than compounding.

**2. A clip that has already earned is REFUSED server-side.** `assertForwardOnly`
(`per-clip-cpm.ts:253-285`) refuses on any non-zero `earnings`, `baseEarnings` or `bonusAmount`, and
on any existing AgencyEarning row. It is called in the POST **inside the transaction, after
`SELECT ... FOR UPDATE`** (`cpm-override/route.ts:188-207`), so the :00 UTC tick and this write
serialise instead of interleaving; the pre-flight GET check is explicitly a courtesy. DELETE is
forward-only for the same reason (`:287-294`): restoring a lower original pair on an earned clip
would write it down, which is the exact shape BL-742 measured at $1,103.41 across 37 pairs. Harness:
"a clip that has EARNED is refused", plus baseEarnings-alone, bonusAmount-alone, owner-earnings-row
and non-finite-earnings all refusing.

**3. A clip with no split to preserve is refused with a clear reason.** `NO_SPLIT_TO_PRESERVE`:
"This clip has no owner rate recorded, so there is no split to keep. Set the owner rate on the
campaign first, or leave this clip as it is." Null and zero owner stamps both hit it; a missing
clipper stamp hits `NO_CLIPPER_RATE`. Every refusal names its condition rather than saying "not
allowed".

**4. Reassignment REFUSES an overridden clip, with the reason visible before confirming AND
re-asserted inside the row lock.** The block lives in the **shared** rule set,
`campaign-reassign.ts:151-157` (`CLIP_HAS_CPM_OVERRIDE`), which `loadClipSideBlocks` feeds to the
picker, so the owner reads the reason on screen instead of hitting a 409 afterwards. It is
**independently re-asserted inside the transaction**, `reassign-campaign/route.ts:347-356`, on the
`cpmOverriddenAt` column newly added to the `SELECT ... FOR UPDATE` — which matters because the three
pre-existing in-lock assertions (status PENDING, campaignId unchanged, earnings 0) would all still
pass on an overridden clip. `cpm-restamp.ts:313` closes the other eraser declaratively, with
`cpmOverriddenAt: null` in the campaign-wide restamp's `where`, so an overridden clip is never loaded.

**5. The admin row computes and displays the owner figure from the same clip stamp.**
`admin/clips/page.tsx:1705-1735`: `stampClipper` / `stampOwner` are now hoisted **above** the owner
figure, and `ownerCpm` resolves to `stampOwner` when it is present and positive, falling back to
`campaign.ownerCpm` only for a clip with no owner stamp. Previously the figure came from the live
campaign rate while BL-744's rate line printed the clip stamp, which is the 2.5x mismatch BL-754
reopened. The two now come from one source. The "Custom rate" badge says so in words, not by colour.

**6. The 8 protected files are byte-identical by blob OID**, verified with `git show` on **both**
refs and on the merged HEAD (all three equal), and none of them appears in the diff at all:

```
clip-earnings-writer.ts             ac5be7deb061768fec800aa89aae512a56a9e065
earnings-calc.ts                    797e20985ad57475ef321afcf3cb1ea7b0d6ab84
balance.ts                          e887f80acfc70fee438e719a32a60025eda22749
tracking.ts                         83ce4babfd39a6261114465639f2eac4e23bfceb
clip-earnings-invariant-middleware  61cef39395363c31f0c902dd4c64e8c06b3e6449
money-decimal.ts                    ef5cdae757b9ad3c23380ee8b63e279f98d0b6ac
campaign-era.ts                     106e16ad75125c3b10b6949a2981d33614c69ab9
owner-share-guard.ts                b5015d902590d6e008f6075e5bea0abeb9e9271c
earnings-never-decrease.ts          c15145f51a561fa383044d9d48123234f14e9203
```
That is the 6 money files plus campaign-era.ts and owner-share-guard.ts, and earnings-never-decrease.ts
is included as a ninth for completeness. **tracking.ts is not in the diff.** No rate column was added,
which is what kept the eleven money call sites, and therefore tracking.ts, untouched.

**7. No owner rate or platform economics reach any clipper-facing route.** The only clipper-adjacent
file the merge touches is `api/clips/route.ts`, and the added line puts `cpmOverriddenAt` **inside**
the existing `if (canSeeMoney)` block alongside the two CPM stamps. A CLIPPER never reaches that code
at all: `route.ts:65-94` returns **403 Forbidden** to any role that is not ADMIN, OWNER or REVIEWER,
and `canSeeMoney` additionally excludes a REVIEWER without `EARNINGS_VIEW`. The owner RATE line in
the admin row stays behind `showRates`, which requires `isOwner`. BL-531 holds.

## AFTER THE PUSH — confirmation from live data that nothing moved

Every timestamp cast `::text` against DB `now()`; handles redacted (none needed, no clip is named).

| Measure | Before push | After push |
| --- | --- | --- |
| Clips carrying an override (`cpmOverriddenAt` NOT NULL) | **0** | **0** |
| Clips with a stored original pair | 0 | 0 |
| `CLIP_CPM_OVERRIDE_SET` / `_REMOVED` audit rows | — | **0** |
| md5 over every clip's id + earnings + baseEarnings + bonusAmount + status + both CPM stamps | `5a897e944bd908ddfd9a5f1b806c41a8` over 5317 clips | **`5a897e944bd908ddfd9a5f1b806c41a8` over 5317 clips — IDENTICAL** |
| Earnings invariant violations | 0 | **0** |
| Campaigns over budget | 0 | **0** |
| payout_requests rows | 165 | **165** |
| DB now | `2026-08-10 12:28:07.538959+00` | `2026-08-10 12:30:49.597627+00` |

**The count of clips currently carrying an override is 0.** That is the expected value: this round
merged the feature and did not use it, and no owner action has occurred since.

The fingerprint being byte-identical across the push is the strongest statement available here: not
one clip's earnings, baseEarnings, bonusAmount, status, clipper stamp or owner stamp changed. One
detail stated plainly rather than smoothed over: the first snapshot query read `total_clips = 5316`
and the fingerprint query moments later read 5317, because a real clipper submitted a clip in the
seconds between them. Both fingerprints are over the same 5317 rows and match exactly.

The three support columns **already existed** in the live database, nullable, from the BL-756 build:
`cpmOverriddenAt` timestamp, `cpmOverrideOrigClipper` and `cpmOverrideOrigOwner` numeric, all
`is_nullable = YES`. **No migration was run this round and `prisma migrate` was never invoked.**

## SAFETY LEDGER

* Merge only. **No override applied to any clip.** The live demo script was not run.
* Forward-only survives: an earned clip is refused, in the pure function and again under the row lock.
* Ratio-preserving scaling of **both** stamps survives; it is the only shape that passes
  `owner-share-guard.ts:72`, and the guard compares the same two numbers before and after.
* Reassignment refuses rather than silently erasing, reason shown before confirming and re-asserted
  in the lock.
* The admin row no longer displays a rate beside a figure it did not produce.
* BL-627's no-overpayment and no-over-budget properties hold by construction: this path writes **rates
  only**, never `earnings` / `baseEarnings` / `bonusAmount`, so `writeClipEarnings` remains the sole
  money writer and no new earnings path exists. Measured: 0 over-budget campaigns, 0 invariant
  violations.
* **BL-718's paid floor is deliberately NOT wired**, and was not added. It takes `(cap, stored)` and
  belongs where a ceiling could write a clip down; this path has no cap site because it writes no
  money. What protects money already paid here is the refusal.
* **Clipper notification is deliberately NOT built.** It is recorded in BACKLOG and is not handled by
  this merge. Clippers are not told when a rate on an unearned clip of theirs changes.
* BL-723 was **not** merged, re-checked after the push.
* No Apify actor was run. BL-678 markers in `src/`: **27 before, 27 after** — unchanged.
* No `prisma migrate`. No clip status, earnings or payout touched. No dashes as bullets.

## HONEST RESIDUALS

* `MEASURED_WORST_EXISTING_GAP` is 0.004 against a 0.01 tolerance, so the true worst-case margin is
  about **2.2x**, not the "100x" BL-752 claimed. BL-754 corrected it and the code documents the
  corrected number at `per-clip-cpm.ts:78-82`. The harness asserts 0.004 + 0.0005 = 0.0045 stays
  inside.
* Everything in the CONFIRM section is established by code reading plus the 33-test harness. No
  end-to-end run against a live clip was performed this round, by design.
* The worktree `C:/m757` was left in place, matching the convention of the m### worktrees from prior
  merge rounds. `C:/b575` was left exactly as found.

## ROLLBACK

```
git revert -m 1 018c22cab303e7b122cad74da1a17319c0c61c15
```
or `git reset --hard pre-merge-BL-757` (`605af18c`). Tags `pre-merge-BL-757` and `post-merge-BL-757`
are both on origin. **No data rollback exists or is needed: this merge wrote no data.**

## PUSH VERIFICATION (BL-288)

```
local HEAD  = 018c22cab303e7b122cad74da1a17319c0c61c15
origin/main = 018c22cab303e7b122cad74da1a17319c0c61c15
VERIFIED PUSHED — origin == local
tags on origin: post-merge-BL-757 -> 018c22ca, pre-merge-BL-757 -> 605af18c
```
