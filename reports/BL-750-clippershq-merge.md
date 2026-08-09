# BL-750 — merging BL-748, and catching the moment both Instagram fixes went live in one table

**NO CLIP'S STORED VIEWS DROPPED. Across all 1,993 stat rows written today, `views_moved_down = 0` and `fell_to_zero = 0`. The earnings invariant is at zero violations. There is nothing to roll back.**

**Merged to main** `d169e73b` · **Was** `6ed3a50c` · **Merged** `checkpoint/BL-748` `ac083fd1` · 2026-08-09 · **Merge only**

---

# STEP 0 — TRUTH

| | |
|---|---|
| `checkpoint/BL-748` tip | **`ac083fd1`** |
| Ancestor of main before the merge | **NOT an ancestor**, genuinely unmerged |
| Merge base | **`6ed3a50c`**, which was current main, so the branch was not stale |
| Diff | **4 files, 310 insertions, 1 deletion**, non-empty |
| Commits | 1 |
| `checkpoint/BL-723` | **NOT merged**, confirmed after the merge by `merge-base --is-ancestor` |

**The tip carries the fix, checked on the tip itself:** `views: singleProbe?.value ?? null` present (**1**),
and the old `views: singleProbe?.value ?? 0` **gone** (**0**).

## The dirty worktree

`C:/b575` was **stale** (`91b84410` against main `6ed3a50c`) **and dirty** (**77 paths**). It was **not
touched**. The merge ran in a **separate clean detached worktree at `C:/m750`**, a short path, with `.env`
and `.env.local` copied and a real `npm ci`, **never a `node_modules` junction**. Re-checked after the push:
still `91b84410`, still **77** dirty paths, **exactly as found**.

---

# THE MERGE

One `--no-ff` merge against current main. **Clean, zero conflicts**, so no union resolution was required.

```
BACKLOG entries on main    132
BACKLOG entries merged     133      (132 + BL-748)
BL-748 entries present       1
conflict markers            0       in BACKLOG and tree-wide
```

Counted with `grep -c`, **never piped to `head`**. **Nothing was lost:** 129 distinct `BL-` ids on main,
130 after, **0 lost**.

**Four files changed**, none of them a money file: `BACKLOG.md`,
`scripts/test-bl-748-no-fabricated-zero.mjs`, `src/app/api/admin/hikerapi-shadow/route.ts`,
`src/lib/scraper-providers/hikerapi.ts`.

## The merge altered nothing that was reviewed

```
git diff origin/checkpoint/BL-748 HEAD -- hikerapi.ts hikerapi-shadow/route.ts test-bl-748-*.mjs  ->  0 lines
```

**Byte-identical to the reviewed tip**, so BL-748's accessibility review applies verbatim to what is now on
main. There is no new or altered code for a review to examine, and that is demonstrated rather than asserted.

---

# CONFIRMED ON THE MERGED RESULT

## By code reading

| Requirement | Evidence on the merged tree |
|---|---|
| Classifier returns null for a hidden count | `grep -c 'views: singleProbe?.value ?? null'` = **1** |
| The fabricated 0 is gone | `grep -c 'views: singleProbe?.value ?? 0'` = **0** |
| Carousel branch's existing guard intact | `grep -c 'views: usedKey === null ? null : sum'` = **1** |
| **`views <= 0` rejection at `:878` INTACT** | `grep -c 'typeof views !== "number" \|\| !Number.isFinite(views) \|\| views <= 0'` = **1** |
| BL-746's submit guard intact | `grep -c 'res?.viewSource != null ? num(res.views) : null'` = **1** |
| **No new vendor call** | `grep -c 'await fetchHikerInstagramByUrl('` = **1** |

The `views <= 0` gate mattering most: **that is what kept the defect harmless for its whole life**, and it
survives the merge unchanged.

## By harness, on the merged tree

**BL-748: 39 passed, 0 failed, exit 0.** It drives the real exported `classifyV2Media` and extracts **both**
shipped gates from source, so it cannot drift. No network call, nothing written, no submission created.

```
THE TWO ARE DISTINGUISHABLE                        null/null versus 0/play_count
TRACKING outcome is IDENTICAL, so the tick cannot change
SUBMIT outcome is IDENTICAL
SUBMIT still writes a genuine 0 (real viewSource)
clip-thumbnail.ts never reads res.views
retire-dead-clips.ts never reads res.views
```

**BL-746: 48 passed, 0 failed, exit 0**, re-run on the merged tree to confirm the submit-stat path still
behaves after BL-748 changed the value it consumes.

## All six callers handle null without throwing

| # | Caller | file:line | Behaviour with null |
|---|---|---|---|
| 1 | `tryHikerForInstagram`, TRACKING | `hikerapi.ts:878` | fails the **same** condition as 0, returns the identical `useResult:false, verdict:"transient"` |
| 2 | `clipper-submit-core.ts`, SUBMIT | guard at `:295` | already required `viewSource != null`, skips |
| 3 | `clip-thumbnail.ts` | `:309` | **never reads `.views`**, asserted by the harness |
| 4 | `retire-dead-clips.ts` | `:297` | **never reads `.views`**, asserted by the harness |
| 5 | `hikerapi-shadow` | `route.ts:251` | OWNER JSON only, null is more honest than a fabricated 0 |
| 6 | `scripts/test-bl610-carousel.ts` | `:29,47,58` | exercises the **carousel** branch, untouched |

**None throws. None relies on receiving 0.**

---

# AFTER THE PUSH — BOTH FIXES LIVE, AND THE DEPLOY BOUNDARY IS VISIBLE

Instagram clips submitted since BL-746 went live with BL-747's merge (about `14:55Z`), measured at
`db_now = 2026-08-09 16:16:30.763080+00`. **Every clip, no sampling:**

| clip | submitted | first stat at | delay | first views | max views |
|---|---|---|---|---|---|
| `cmslxgbkl08gn...` | 14:58:14.037 | 16:01:03.776 | **3,769,739ms** (63 min) | 2,247 | 2,247 |
| `cmslxu1cz08j5...` | 15:08:53.987 | 16:01:32.540 | **3,158,553ms** (53 min) | 4,270 | 4,270 |
| `cmslxwouv08ju...` | 15:10:57.751 | 16:01:05.108 | **3,007,357ms** (50 min) | 498 | 498 |
| `cmslyvoxi005f...` | 15:38:10.806 | 15:38:10.851 | **45ms** | 0 | 0 |
| `cmslyyvq6006e...` | 15:40:39.582 | 15:40:39.622 | **40ms** | 0 | 0 |
| `cmslz2ytj007u...` | 15:43:50.215 | 15:43:50.244 | **29ms** | 0 | 0 |
| `cmsm019q500ez...` | 16:10:30.653 | 16:10:30.676 | **23ms** | 0 | 0 |
| `cmsm0733a00gf...` | 16:15:01.990 | 16:15:02.038 | **48ms** | 0 | 0 |

**The deploy boundary sits between 15:10 and 15:38, and it is unmistakable.** The three clips submitted
before it got no stat at submit and waited for the 16:00 tracking tick. **The five submitted after it each
got a first stat inside the submit transaction, at 23 to 48ms**, exactly BL-748's measured 29 to 45ms.

**Summary, Instagram, since BL-746 went live:**

```
submitted                8
got a first stat         8   (100%)
within 1 minute          5   (all five post-deploy submissions)
median delay            47ms
first stat is zero       5
```

**Against BL-745's baseline of 0 of 777 within a minute and a 3,610 second median, that is the fix working.**

## The five zeros are genuine, provably

**BL-746's guard writes a first stat ONLY when `viewSource` is non-null**, so **the existence of each row is
itself proof that a real `play_count` field returned 0**. A fabricated one would have been skipped and no
row would exist. That is the property BL-748 makes structural rather than incidental.

**And it is the expected reading, not a fault.** These reels were **seconds old** at submission. The three
pre-deploy clips read 2,247, 4,270 and 498 because the tick measured them **50 to 63 minutes** later. A post
measured at T+0 genuinely has close to zero plays. **The value of BL-746 is that the clip now HAS a
measurement immediately; it is not that the number is large.**

**Stated plainly and not claimed:** all five still read 0 at `max_views`. They are PENDING on active
60-minute jobs with no `INFRA_DEFER`, so the 17:00 tick is the first opportunity for them to rise, and that
had not happened when this report was written. **A first snapshot can only ever raise a clip from nothing;
BL-543's concern is a 0 REPLACING a higher value, which cannot happen on a first stat.**

## No stored views moved down, anywhere

```
stat rows written today          1,993
views moved DOWN today               0
fell from above 0 to 0 today         0
db_now = 2026-08-09 16:17:13.042239+00
```

**No non-genuine stored 0 appeared**, and the earnings invariant is at **0 violations**.

---

# WHAT WAS DELIBERATELY NOT DONE

* **No backfill was run.** BL-749 recommended against one after finding 6 of 6 sampled clips permanently unresolvable, and BL-748 found nothing to repair in any case.
* **The separate 50-clip zero population was not chased**: 45 YouTube and 5 TikTok clips that fell to 0. They never touch this Instagram classifier, and BL-748 deliberately declined to attribute them. That remains its own round if the owner wants it.
* **BL-723 was not merged.**
* **No Apify actor was run**, no probe was made, **$0.00 spent**, and no submission was created for testing.

---

# GUARDS AND GATES

## Byte-identical by blob OID, merged tree against main

```
ac5be7de clip-earnings-writer   797e2098 earnings-calc   e887f80a balance   83ce4bab tracking
61cef393 clip-earnings-invariant-middleware   ef5cdae7 money-decimal   106e16ad campaign-era
656bf4c0 apify.ts
```

**All eight identical.** `apify.ts` byte-equal means **no BL-678 guard was touched**; it carries the same
**8** BL-678 comment lines on both refs. **The eleven guards are a count of guards, not of that string, so 8
is the honest measure of that grep and the blob equality is the stronger proof.**

## The tracking tick

The merged change adds no call, no await and no branch: it substitutes one value in a returned object, so
the tick's timing cannot move. **A correction on the number the brief uses:** `CLIPS_PER_TICK` is **not set
in the environment**, so the code default of **30** applies (`tracking.ts:164-178`, clamped to a 5 to 500
band), not 90. BL-197 lowered it from 60 to 30 precisely so a tick finishes inside the 300s ceiling. Either
way this merge cannot affect it.

## Gates, stated honestly

* `npm ci` **exit 0**; `npx prisma generate` **exit 0**, run **after** `npm ci` because `npm ci` wipes the generated client.
* `tsc --noEmit` **exit 0, 0 errors** (log 0 lines).
* `npm run build` **exit 0**, `✓ Compiled successfully in 50s`, read from a log with the exit code **echoed, never piped through `tail`**. `check:prisma-bypass` and `check:removed-fields` both ran in `prebuild`.
* Hooks gate **11 problems, 0 errors, 11 warnings, at the limit of 11**, with **eslint v9.39.4 confirmed present** so the gate is not silently a no-op.
* Harnesses on the merged tree: **BL-748 39/0 exit 0**, **BL-746 48/0 exit 0**.

## The push, and the same false failure worth recording again

`safe-push.mjs` printed **`PUSH FAILED`**. **It is wrong, and it is the BL-727 trap**: it cannot verify a
`src:dst` refspec from a detached worktree, so it resolved `origin/HEAD:main` to nothing. Its own push step
reported `push attempt 1/3 OK`.

**`git ls-remote` is the authority and it agrees with success**, confirmed a second way by re-fetching:

```
refs/heads/main    d169e73b86b8ca490971c260bfdaeba3d4e38a16
local merged HEAD  d169e73b86b8ca490971c260bfdaeba3d4e38a16
BL-748  MERGED        BL-723  correctly NOT merged
```

## Unchanged

No clip status or earnings changed by this merge, no payout touched, no schema change, **no `prisma
migrate`**. Platform at `16:27:44`: **4,262 approved clips, $12,016.06, 163 payout rows, 205,695 stat rows,
invariant violations 0**, identical to the pre-push reading except one further stat row from ordinary cron
accrual. **This merge writes no money and touches no money file.**

**Rollback:** `git revert -m 1 d169e73b`, or `git reset --hard 6ed3a50c`. Nothing to undo in the database.

---

# WHAT COULD NOT BE CONFIRMED

* **Whether the five zero first stats rise on the next tick.** They are PENDING on active 60-minute jobs and the 17:00 tick is the first opportunity. Re-run the per-clip query in this report after 17:00 to settle it.
* **How often Instagram genuinely hides a single video's play count.** Now handled honestly either way, but its real frequency needs a sample of live posts, and no probe was made this round.
