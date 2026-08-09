# BL-747 — merging BL-744 and BL-746, and refusing to claim a result the data does not yet show

**NO FABRICATED ZERO REACHED ClipStat. Zero new zero-view Instagram stat rows since the push, and the newest such row on the platform is still `2026-07-26 21:57:03.746`, more than two weeks old and unchanged from the pre-push baseline. There is nothing to roll back.**

**Merged to main** `6ed3a50c` · **Was** `b5bd0651` · **Merged** `checkpoint/BL-744` `a60d2f75` and `checkpoint/BL-746` `053309f4` · 2026-08-09 · **Merge only**

---

# STEP 0 — TRUTH PER BRANCH

| Branch | Tip | Ancestor of main before? | Merge base | Diff | Commits |
|---|---|---|---|---|---|
| `checkpoint/BL-744` | **`a60d2f75`** | **NOT an ancestor**, genuinely unmerged | `b5bd0651` | **6 files, 400 insertions, 27 deletions** | 1 |
| `checkpoint/BL-746` | **`053309f4`** | **NOT an ancestor**, genuinely unmerged | `b5bd0651` | **4 files, 433 insertions, 3 deletions** | 1 |
| `checkpoint/BL-723` | `22039307` | **NOT merged, deliberately** | n/a | n/a | n/a |

Both merge bases are `b5bd0651`, which was current main, so neither branch was stale.

## 0.1 Each tip carries its post-review fix, not an earlier state

**BL-744** carries the shipped labels and the dialog correction, counted on the tip itself:
`Clipper gets` / `Owner gets` / `Campaign pays` / `Clipper share` / `Total paid` present (**5 hits**), and
`Current clipper rate` / `New clipper rate` / `The clipper rate changes` present (**3 hits**).

**BL-746** carries the guard it added *after* its own review, the one that matters most:
`res?.viewSource != null ? num(res.views) : null` present (**1**), and the numeric write guard
`typeof harvested.views === "number"` present (**1**). **That is the post-review fix**, the one that stops
`hikerapi.ts:603`'s fabricated `0` reaching `ClipStat`.

## 0.2 BL-723 was not merged

`git merge-base --is-ancestor origin/checkpoint/BL-723 origin/main` returns **not an ancestor** after the
merge, confirming it stayed out. It targets `business-api` and cannot be called by the owner's Login Kit app.

## 0.3 The dirty worktree, and what was done about it

`C:/b575` was **stale** (`91b84410` against main `b5bd0651`) **and dirty** (**77 paths**). It was **not
touched**. The merge ran in a **separate clean detached worktree at `C:/m747`**, a short path, with `.env`
and `.env.local` copied and a real `npm ci`, **never a `node_modules` junction**. Re-checked after the push:
`C:/b575` is still `91b84410` with still **77** dirty paths, **exactly as found**.

---

# THE MERGES

Two `--no-ff` merges, **one at a time, verified between**, both against current main:

```
*   6ed3a50c  parents 2b22930d 053309f4   Merge BL-746
|\
| * 053309f4  parent  b5bd0651            BL-746
* | 2b22930d  parents b5bd0651 a60d2f75   Merge BL-744
|\ \
| |/
|/|
| * a60d2f75  parent  b5bd0651            BL-744
```

**BL-744 merged clean, zero conflicts.** **BL-746 conflicted on `BACKLOG.md` only**, as expected since both
branches appended an entry.

## Conflict resolution: union, both sides, nothing dropped

Two conflict regions, six marker lines, resolved by **deleting only the six markers and keeping both sides**.

```
entries on main (base)        130
entries after the union       132       (130 + BL-744 + BL-746)
BL-744 entries present          1
BL-746 entries present          1
conflict markers in BACKLOG     0
conflict markers tree-wide      0
```

Counted with `grep -c`, **never piped to `head`**.

**Proof nothing was lost, stronger than a count.** Every distinct `BL-` id present on main was checked
against the merged file: **127 unique ids on main, 129 after the merge, 0 lost.** The gap between 132
entries and 129 unique ids is pre-existing duplicate numbering, not merge damage.

---

# THE MERGE ALTERED NEITHER REVIEWED CHANGE

The strongest single check in this round. Diffing the merged tree against each branch tip, restricted to
that branch's own files:

```
git diff origin/checkpoint/BL-744 HEAD -- admin/clips/page.tsx admin/submit-clip/page.tsx
                                          reassign-campaign-dialog.tsx api/clips/route.ts   ->  0 lines
git diff origin/checkpoint/BL-746 HEAD -- src/lib/clipper-submit-core.ts                    ->  0 lines
```

**Both reviewed changes survive the merge byte-identically.** BL-744's accessibility approval therefore
applies verbatim to what is now on main; there is no new or altered UI for a review to examine, and that is
demonstrated rather than asserted.

---

# CONFIRMED ON THE MERGED RESULT

## The Instagram submit path, by code reading

The merged write path, executable lines only:

```ts
if (platform === "instagram" && fetchedRawMeta == null) {
  const harvested = await harvestInstagramRawMeta(clipUrl);
  fetchedRawMeta = harvested?.media ?? null;
  if (fetchedStats == null && harvested && typeof harvested.views === "number") {
    fetchedStats = { views: harvested.views, likes: harvested.likes ?? 0,
                     comments: harvested.comments ?? 0, shares: 0 };
    console.log(`[BL-746] instagram first-stat from harvest: views=${harvested.views} ...`);
  }
}
```

| Requirement | Evidence on the merged tree |
|---|---|
| First `ClipStat` from an already-present count | the block above, feeding the unchanged write |
| **No new vendor call** | `grep -c 'await fetchHikerInstagramByUrl('` = **1** |
| **`viewSource` guard present** | `grep -c 'res?.viewSource != null ? num(res.views) : null'` = **1** |
| BL-605 skip contract holds | `grep -c 'if (resolvedFirstViews != null)'` = **1** |
| Instagram only | `grep -c 'platform === "instagram" && fetchedRawMeta == null'` = **1** |
| Harvest touches no Apify path | `grep -ci apify` inside the harvest body = **0** |

**A fabricated 0 can never reach `ClipStat`, on two independent gates.** The harvest refuses any count whose
`viewSource` is null, which is exactly `hikerapi.ts:603`'s hidden-count case; and the write requires
`typeof === "number"`, so null, absent, string and NaN all skip. **A legitimate numeric `0` is still
written**, which is correct and is the rule the other platforms already follow.

## By harness, on the merged tree

**BL-746: 48 passed, 0 failed, exit 0.** It drives the real exported `classifyV2Media` and the guard
extracted from the merged source. It **creates no submission and makes no network call**. **Seven separate
assertions specifically prove `views !== 0`** on every skip case, including the hidden-count video that
produced `hikerapi.ts:603`'s fabricated zero.

**BL-744: 46 passed, 0 failed, exit 0**, in real Chromium against the merged compiled Tailwind:

```
CPM_SPLIT : Clipper gets $0.24  Owner gets $0.15  [sr-only: Clipper and owner amounts added together.]
            Campaign pays = $0.39   Rates per 1,000 views: clipper $0.20, owner $0.1279
MARKETPLACE: Clipper share $0.60  Poster share $0.30  Owner share $0.10
            [sr-only: Clipper, poster and owner shares all come out of this.]  Total paid = $1.00
```

All eight labels present exactly once; rates read from **`clip.cpmAtSubmissionDecimal` and
`clip.ownerCpmAtSubmissionDecimal`** (2 hits), the clip's own stamps, so a figure can never sit beside a
rate that did not produce it.

## TikTok and YouTube unchanged

**Structurally**: the branch is gated `platform === "instagram"`, and even inside it the write requires
`fetchedStats == null`, so a resolved stats path always wins. **Measured**: both sat at a **median of 0
seconds** to first stat on both sides of the 2026-07-22 cutover before this merge, and neither platform's
code path is in the diff.

## No owner rate reaches a clipper-facing route

The two stamps are selected in **exactly two lines repo-wide**, `api/clips/route.ts:459-460`, inside
`if (canSeeMoney)`, on a route that 403s every non OWNER/ADMIN/REVIEWER. The clipper-facing routes select
neither:

```
api/earnings/route.ts      stamps=0  ownerCpm=0
api/campaigns/route.ts     stamps=0  ownerCpm=0
api/payouts/route.ts       stamps=0  ownerCpm=0
api/clips/mine/route.ts    stamps=0  ownerCpm=0     <- the clipper's own clips list
```

The owner **rate** is additionally gated to `isOwner`, narrower than the `isAdminOrOwner` gate on the owner
**amount**.

---

# AFTER THE PUSH — STATED PLAINLY, NOT CLAIMED

**I cannot yet confirm the fix is working in production, and I am not going to say that it is.**

Measured at `db_now = 2026-08-09 15:12:25.936230+00`, for clips created after the push at about `14:55Z`:

| | |
|---|---|
| Instagram clips submitted since the push | **3** |
| Of those, first stat within 1 minute | **0** |
| Median delay | **no stats yet** |
| TikTok or YouTube submitted since the push | 0 |

```
cmslxgbkl08gn...  APPROVED  0 stat rows  created 14:58:14.037  age 852s
cmslxu1cz08j5...  PENDING   0 stat rows  created 15:08:53.987  age 212s
cmslxwouv08ju...  PENDING   0 stat rows  created 15:10:57.751  age  88s
```

**Against BL-745's baseline this is not yet an improvement**, and the honest reading is that **the result is
unknown**, not that the fix failed. The first clip arrived three minutes after the push, almost certainly
before Railway finished building. The third arrived sixteen minutes after, which is usually enough, so this
is genuinely inconclusive rather than reassuring. Two ordinary explanations remain open and I cannot
separate them from here: the deploy may still not be serving, or the harvest may legitimately have returned
null for these three posts, which is the designed skip.

**Pre-push baseline, for the comparison when it can be made** (post-cutover slice, `db_now 14:45:52`):

| platform | clips | within 1 min | median s |
|---|---|---|---|
| **Instagram** | **859** | **0** | **3,660** |
| TikTok | 198 | 178 | **0** |
| YouTube | 73 | 58 | **0** |

## The safety property DID hold, and that is checkable now

```
Instagram stat rows with views = 0      1,563 before the push, 1,563 after      UNCHANGED
newest such row                          2026-07-26 21:57:03.746                UNCHANGED
new zero-view rows since the push        0
```

**No clipper's views were zeroed.** Whether the deploy is live or not, nothing wrote a fabricated 0, which
is the one outcome that would have required the first line of this report and a rollback.

## The exact query for the owner to re-run

```sql
SELECT ca.platform,
       count(*)                                                              AS submitted,
       SUM(CASE WHEN fs.first_stat IS NOT NULL
                 AND EXTRACT(EPOCH FROM (fs.first_stat - c."createdAt")) <= 60
                THEN 1 ELSE 0 END)                                           AS within_1_min,
       ROUND(percentile_cont(0.5) WITHIN GROUP (
         ORDER BY EXTRACT(EPOCH FROM (fs.first_stat - c."createdAt"))
       )::numeric, 0)                                                        AS median_seconds,
       SUM(CASE WHEN fs.first_views = 0 THEN 1 ELSE 0 END)                   AS FABRICATED_ZEROS,
       now()::text                                                           AS db_now
FROM clips c
JOIN clip_accounts ca ON ca.id = c."clipAccountId"
LEFT JOIN LATERAL (
  SELECT min(s."checkedAt") AS first_stat,
         (SELECT s2.views FROM clip_stats s2 WHERE s2."clipId" = c.id
          ORDER BY s2."checkedAt" ASC LIMIT 1) AS first_views
  FROM clip_stats s WHERE s."clipId" = c.id
) fs ON true
WHERE c."isDeleted" = false
  AND c."createdAt" > '2026-08-09 15:15:00+00'     -- safely after the deploy
GROUP BY ca.platform;
```

**`FABRICATED_ZEROS` must stay 0.** If it is ever above 0 for Instagram, roll back with
`git revert -m 1 6ed3a50c` and report it immediately: a stored 0 destroys a clipper's earnings.

---

# WHAT WAS DELIBERATELY NOT DONE

* **The 41-clip backfill was NOT run.** Those clips carry `cadenceReason = INFRA_DEFER` with intervals backed off to 360 or 2880 minutes and do not self-heal, and BL-746 spec'd the backfill for its own round.
* **`hikerapi.ts:603` was NOT repaired.** It still reads `views: singleProbe?.value ?? 0`, verbatim on the merged tree. BL-746 deliberately guarded it at the call site instead, because that classifier is shared with the tracking poll and changing its return would move tracking behaviour for every platform. **`hikerapi.ts` is byte-identical by blob OID.**
* **No Apify actor was run**, and no submission was created to test with.

---

# GUARDS AND GATES

## Byte-identical by blob OID, on the merged tree against main

```
ac5be7de clip-earnings-writer    797e2098 earnings-calc    e887f80a balance    83ce4bab tracking
61cef393 clip-earnings-invariant-middleware    ef5cdae7 money-decimal    106e16ad campaign-era
656bf4c0 apify.ts                bc51db76 hikerapi.ts
```

**All nine identical.** `apify.ts` byte-equal means **no BL-678 guard was touched**; its guard-comment lines
count **8 on main and 8 merged** (the "11 guards" figure counts guards, not string occurrences, so 8 is the
honest measure of that grep and the blob equality is the stronger proof).

**Nine files changed by the whole merge**, none of them a money file: `BACKLOG.md`, three `scripts/*.mjs`,
`admin/clips/page.tsx`, `admin/submit-clip/page.tsx`, `api/clips/route.ts`,
`reassign-campaign-dialog.tsx`, `clipper-submit-core.ts`.

## Gates, stated honestly

* `npm ci` **exit 0**; `npx prisma generate` **exit 0**, run **after** `npm ci` because `npm ci` wipes the generated client.
* `tsc --noEmit` **exit 0, 0 errors** (log 0 lines).
* `npm run build` **exit 0**, `✓ Compiled successfully in 88s`, read from a log with the exit code **echoed, never piped through `tail`**. `check:prisma-bypass` and `check:removed-fields` both ran in `prebuild`.
* Hooks gate **11 problems, 0 errors, 11 warnings, at the limit of 11**, with **eslint v9.39.4 confirmed present** so the gate is not silently a no-op.
* Harnesses on the merged tree: **BL-746 48/0 exit 0**, **BL-744 46/0 exit 0**.

## The push, and a false failure worth recording

`safe-push.mjs` printed **`PUSH FAILED`**. **It is wrong, and this is the BL-727 trap**: it cannot verify a
`src:dst` refspec from a detached worktree, so it resolved `origin/HEAD:main` to nothing. Its own push step
reported `push attempt 1/3 OK`.

**`git ls-remote` is the authority and it agrees with success:**

```
refs/heads/main   6ed3a50c2e4f3a8b7334efb487e1dc86a8e6482e
local merged HEAD 6ed3a50c2e4f3a8b7334efb487e1dc86a8e6482e
```

Confirmed a second way, by re-fetching: `origin/main` equals the merged HEAD, and both branches now report
as ancestors of main while BL-723 does not.

## Unchanged

No clip status or earnings changed by this merge, no payout touched, no schema change, **no `prisma
migrate`**. Platform at `15:13:54`: **4,260 approved clips, $12,005.04, 163 payout rows, invariant
violations 0**. The clip and earnings movement against the 14:47 reading (4,259 and $11,989.84) is ordinary
cron accrual and one new approval, not merge effect: this merge writes no money and touches no money file.

**Rollback:** `git revert -m 1 6ed3a50c` reverts BL-746 alone; `git revert -m 1 2b22930d` reverts BL-744
alone; `git reset --hard b5bd0651` reverts both. Nothing to undo in the database.
