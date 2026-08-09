# BL-755 — BL-753 merged to main, and a correction to BL-753's own report

**VERDICT IN ONE LINE: `checkpoint/BL-753` `b556468e` was genuinely unmerged and is now on `main` at
`605af18c`, verified by `git ls-remote`. tsc was 0 errors before the merge and 0 after, the build passed with
exit 0, the harness passed 36 of 36 on the merged tree, and all 8 protected files are byte-identical by blob
OID. One correction: BL-753's report claimed 2 pre-existing tsc errors on clean `origin/main`. That claim is
WRONG, and this round disproves it.**

**2026-08-09 · MERGE ONLY.** No code was written. No data changed, no clip's earnings or status changed, no
payout touched, the 13 known zeroed clips were NOT repaired, `getYouTubeVideoDetails:86` was NOT fixed, and
no never-decrease guard was added to views. No Apify actor run. No `prisma migrate`. Handles redacted; every
timestamp cast `::text` against DB `now()`.

---

# STEP 0 — TRUTH

| check | result |
|---|---|
| `origin/main` before | **`d169e73b86b8ca490971c260bfdaeba3d4e38a16`** |
| `origin/checkpoint/BL-753` | **`b556468e7d13f4b222f8e69b1cf15f29e944174f`** |
| `merge-base --is-ancestor` BL-753 → main | **NO — genuinely unmerged** |
| diff non-empty | **YES**: 4 files, 660 insertions, 3 deletions |
| `checkpoint/BL-723` an ancestor of main | **NO — not merged, correct** |

The diff is `BACKLOG.md`, `docs/BL-753-youtube-fabricated-zero.md`, `scripts/bl753-harness.ts` and
**`src/lib/youtube.ts` as the only source file**.

## Worktree handling

**`C:/b575` was NOT touched.** It was confirmed stale at `91b84410` and dirty at **77 paths**, so per the
brief the merge ran in a separate clean worktree at a short path, **`C:/m755`**, created detached at
`origin/main`. `node_modules` was installed there by `npm ci`, **never junctioned**. The worktree was left
with `git status --porcelain` at **0 lines** before the push and is removed at the end of this round.
`C:/b575` remains exactly as found.

---

# THE TSC BASELINE, AND A CORRECTION TO BL-753

The brief asked me to record the tsc error count on main **before** merging so BL-753's reported 2
pre-existing errors would not be misattributed. Doing that produced a result BL-753 did not predict.

| run | commit | worktree | exit | errors |
|---|---|---|---|---|
| **BEFORE the merge** | `d169e73b` (clean `origin/main`) | fresh `C:/m755` | **0** | **0** |
| **AFTER the merge** | `605af18c` | fresh `C:/m755` | **0** | **0** |

**The count is unchanged, so the merge adds no error and I proceeded.** But the baseline is **0, not 2**.

BL-753's report states, as a fact about the codebase, that
`scripts/test-bl-534-era-boundary-owner-rule.ts` raises two `TS2393 Duplicate function implementation`
errors on clean `origin/main`. **That is wrong.** I re-ran tsc in BL-753's own worktree `C:/a753`, now that
the stray artifact files that round created at its root have been deleted, and at the same content it now
reports **exit 0, 0 errors**.

So the two errors were an artifact of that worktree's transient state during the baseline run, not a
property of `origin/main`. **I am not going to invent a mechanism I did not prove**: the reproducible facts
are that a worktree carrying those stray files reported 2, and that three separate clean checks (fresh
worktree on main, fresh worktree on the merge, and the original worktree after cleanup) all report 0.

**What this changes and what it does not.** It does not affect the fix, the harness, the money files or the
merge, all of which stand. It does mean BL-753's published report asserts a false fact about the repository,
and anyone who reads it will go looking for a pre-existing problem that does not exist. The `export {}` that
BL-753 added to its harness for module scope was still correct and is still needed.

---

# THE MERGE

`git merge --no-ff origin/checkpoint/BL-753` → **`MERGE_EXIT=0`**, "Merge made by the 'ort' strategy",
merge commit **`605af18c`**.

* **No conflicts arose at all**, so there was nothing to union. `git grep` for `<<<<<<<`, `=======` and
  `>>>>>>>` across `src`, `scripts`, `docs`, `prisma` and `BACKLOG.md` returns **0**.
* **BACKLOG union counted with `grep -c`, not piped**: **134** `## BL-` entries on the merged tree, with the
  BL-753 entry present (`grep -c "BL-753"` = 1). Nothing was dropped, because nothing conflicted.

---

# GATES, STATED HONESTLY

| gate | result |
|---|---|
| `npm ci` | **`NPMCI_EXIT=0`**, 822 packages. Run FIRST, before anything else |
| `npx prisma generate` | **`PRISMA_EXIT=0`**, run after `npm ci` wiped the client, before tsc |
| `npx tsc --noEmit` before merge | **exit 0, 0 errors** |
| `npx tsc --noEmit` after merge | **exit 0, 0 errors — unchanged, so proceed** |
| `npm run build` | **`BUILD_EXIT=0`**, "Compiled successfully in 43s", exit code echoed from the log, never piped through `tail` |
| BL-348 hooks gate | **0 errors, 11 warnings** against `--max-warnings 11` |
| eslint present | **v9.39.4** confirmed by `npx eslint --version`, so the gate did not silently no-op |
| Harness on the merged tree | **36 passed, 0 failed, `HARNESS_EXIT=0`** |

**`package.json` and `package-lock.json` are NOT in BL-753's diff** (`grep -c` = 0), so `npm ci` was a
formality here rather than a functional necessity. It was run anyway, as instructed.

---

# CONFIRMED ON THE MERGED RESULT

## By the harness, run on the merged tree

```
PASS  vidHIDDEN UNKNOWN -> null entry (clip keeps last-known)
PASS  mB known count -> views=0 (expected 0)
PASS  hidden !== genuine-zero -> hidden=null genuineZero={"views":0,"likes":0,"comments":0,"shares":0}
PASS  deleted video still null (unchanged path) -> null
```

* **A hidden-count video yields null, not 0.** Confirmed.
* **A genuinely-zero video still records a real 0**, and the two remain **distinguishable**: one is a null
  entry, the other a `{"views":0,...}` object. Confirmed.
* **A deleted video still yields null** via the pre-existing path. Confirmed.

## By code reading on the merged tree

* **`tracking.ts` is NOT in the diff.** `git diff --name-only origin/main HEAD` returns exactly four files
  and `tracking.ts` is not among them.
* **No never-decrease guard was added to views.** A grep of the source diff for `neverDecrease`,
  `viewsNeverDecrease`, `prevViews` and `capButNeverBelow` returns **0**. BL-753 measured that such a guard
  would have blocked **1,245 legitimate decreases across 650 clips**, the largest a **723,110 view**
  Instagram correction, which would have meant paying CPM on purged views.
* **`getYouTubeVideoDetails` remains deliberately unfixed**, still reading
  `parseInt(item.statistics?.viewCount || '0', 10)` at line 119 of the merged file, with both the
  `DELIBERATELY NOT FIXED` marker and the `RESIDUAL, stated plainly` note recorded in the file.

## Protected files, by blob OID on both refs

```
IDENTICAL  ac5be7deb061  src/lib/clip-earnings-writer.ts
IDENTICAL  797e20985ad5  src/lib/earnings-calc.ts
IDENTICAL  e887f80acfc7  src/lib/balance.ts
IDENTICAL  83ce4babfd39  src/lib/tracking.ts
IDENTICAL  61cef3939536  src/lib/clip-earnings-invariant-middleware.ts
IDENTICAL  ef5cdae757b9  src/lib/money-decimal.ts
IDENTICAL  106e16ad7512  src/lib/campaign-era.ts
IDENTICAL  656bf4c0c408  src/lib/apify.ts
```

**8 of 8 identical**, checked `origin/main` against the merged `HEAD`. `apify.ts` byte-identical means its
BL-678 guard comments are intact by construction; `grep -c` confirms **8** in that file.

---

# THE PUSH

```
[safe-push] branch HEAD:main: push attempt 1/3 OK
[safe-push] ✗ PUSH FAILED — origin/HEAD:main (none) is NOT up to date with local HEAD (605af18)
```

**That failure line is the known BL-727 false negative**: `safe-push.mjs` cannot resolve `origin/HEAD:main`
as a ref name when invoked with a `HEAD:main` refspec from a **detached** worktree, so its verification step
reads "(none)" and reports failure even though the push itself returned OK on attempt 1.

**`git ls-remote` is authoritative and it agrees with local:**

```
605af18c5c16a609a6ceca2f7b03173832e2feef	refs/heads/main
local HEAD:  605af18c5c16a609a6ceca2f7b03173832e2feef
```

**origin == local. The merge is on `main`.**

---

# AFTER THE PUSH — NOTHING REGRESSED

Baseline taken before the merge, comparison after the push. Both `::text` against DB `now()`.

| metric | before (`20:02:57.978438+00`) | after (`20:28:07.0929+00`) | verdict |
|---|---|---|---|
| earnings invariant violations | **0** | **0** | unchanged |
| the 13 known zeroed YouTube clips | **13** | **13** | **unchanged, exactly as BL-753 said** |
| clips that ever fell to zero | **50** | **50** | **no new zeroing** |
| payout rows | 164 | 164 | untouched |
| total clip earnings | $12,171.19 | $12,174.01 | **+$2.82, an increase** |
| `clip_stats` rows | 206,203 | 206,240 | +37, ordinary tick |
| newest `ClipStat.checkedAt` | 20:01:25.863 | 20:11:24.321 | tick running normally |

**No stored views moved down.** The full decrease census is **identical to BL-753's, every row**: Instagram
86 events on 18 clips with a 723,110 biggest drop, TikTok 269 on 136, YouTube 890 on 496, plus the 5 TikTok
and 46 YouTube zero-falls. **Not one new decrease and not one new zero-fall** since BL-753 measured it.

The **+$2.82** is ordinary cron accrual on ACTIVE campaigns and is an **increase**, which is the direction
that matters here: nothing was written down.

**The 13 are unchanged, which is the confirmation BL-753 asked for.** That round stated plainly they do NOT
self-heal, because the fabricated zero has already become their last-known value, so preserving last-known
preserves the wrong number. They are still at 13. **They were not repaired, deliberately.**

## Tick budget at `CLIPS_PER_TICK` 90

`clipsPerTick()` clamps to `[5, 500]`, so 90 is accepted verbatim. The merged change cannot affect the tick's
budget: no additional API call (the batch is still one `videos.list` per 50 ids), no new code path (a
hidden-count video now takes the route deleted videos already take), and no Apify slot consumed, since
`tracking.ts:3865-3869` documents that YT batch hits Google rather than Apify.

**Stated plainly: I did not execute a live 90-clip tick**, because that writes `ClipStat` rows and recomputes
earnings, which a merge-only round forbids. The claim is structural plus the harness, not a wall-clock
measurement, and I am not presenting it as one.

---

# WHAT COULD NOT BE VERIFIED

* **That the new code is running in production yet.** The push landed at roughly 20:25 UTC and the newest
  `ClipStat` is 20:11:24, so **every tick reflected in the numbers above ran on the OLD code**. The
  post-push comparison proves nothing regressed in the data, but it does **not** yet demonstrate the fix
  executing on Railway. That needs a tick after the deploy completes.
* **Live YouTube behaviour**, for the same reason BL-753 gave: there is no `YOUTUBE_API_KEY` in this
  environment, so the hidden-count response shape is proven by harness and by Google's documentation, not by
  observation.
* **The precise mechanism** behind the 2 tsc errors BL-753 reported. Disproven as a property of
  `origin/main`, but I did not establish which stray file produced them and I am not guessing.

---

# ROLLBACK

`git revert -m 1 605af18c`, or `git reset --hard d169e73b`. **No data rollback exists or is needed, because
no data was written in either BL-753 or this round.**
