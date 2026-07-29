# BL-679 (ClippersHQ) — MERGE of BL-678 (Apify off by construction) and BL-676 (the completed-campaign blank screen)

## NOTHING BROKE. After the deploy, tracking wrote 69 ClipStat rows across all three platforms with **zero views moved down on any platform**, earnings grew normally with the invariant holding on all 2,905 approved clips, submit is live on all three, and **not one Apify attempt has been logged since the push**. One thing could NOT be observed and is not claimed: no account verification has been attempted anywhere on the platform since the deploy, so verification is proven Apify-independent structurally and from the 19 successful pre-deploy verifications, not from post-deploy traffic. Rollback if ever needed: `git reset --hard pre-merge-BL-679`, or `git revert -m 1 381d080c` (Apify guard) / `git revert -m 1 fdde504f` (refusal panel) individually.

> **Filename note, per CONVENTION.md.** `reports/BL-679.md` was already taken by a different project: it is clipper-finder's *"beat-drop timestamp and mood for Instagram Reels"*, republished at that path by BL-688's citation repair. The collision check was run against `origin/main` before pushing and that file was **not** touched. This report is published beside it under the `-<project>-<slug>` suffix the convention prescribes.

**Merge commits on `main`:** `381d080c` (BL-678) then `fdde504f` (BL-676). `origin/main == local HEAD == fdde504f`, verified.
**Base** `d6373647` (`post-merge-BL-675`). **Tags** `pre-merge-BL-679` (d6373647) and `post-merge-BL-679` (fdde504f), both pushed.
**Worktree** `C:/b679`, short path, detached, `node_modules` never junctioned.
**Rollback** for BOTH: `git reset --hard pre-merge-BL-679`. For one only: `git revert -m 1 381d080c` (BL-678, the Apify guard) or `git revert -m 1 fdde504f` (BL-676, the refusal panel). They touch disjoint files, so either reverts cleanly on its own.

---

## STEP 0 — were they genuinely unmerged?

Both were, each with a non-empty `.ts` diff, and both branches' worktrees were parked and clean, meaning their rounds were finished and pushed rather than live.

| branch | SHA | `merge-base --is-ancestor` into main | commits ahead | code diff | worktree state |
| --- | --- | --- | --- | --- | --- |
| `checkpoint/BL-678` | `3940e290` | **NO**, unmerged | 1 | 5 `.ts` files, **+426 / −5** | `C:/b678`, **0** modified |
| `checkpoint/BL-676` | `d169d7db` | **NO**, unmerged | 1 | 3 `.ts`/`.tsx` files, **+351 / −6** | `C:/b676`, **0** modified |

BL-678's merge base was `d6373647`, i.e. main's own tip, so it merged with zero conflicts. BL-676's merge base was `0a69fcc4`, two merges back, so it conflicted on `BACKLOG.md` only.

**Nothing a live round held was merged.** Only those two branches entered. The three worktrees in the 676 to 678 range (`C:/b676`, `C:/b677`, `C:/b678`) each reported **0** modified tracked files, so none was mid-round. `checkpoint/BL-677` was audit-only and was not merged, because it produced no code.

**BL-676 qualified as UI only, as the brief required before merging it.** Its diff is one new component, one page, one test harness and a BACKLOG entry. It contains no API route, no query, no schema and no money path.

## The dirty main worktree, handled without touching it

`C:/b575` holds the local `main` branch and was still **dirty**: 77 tracked entries. It was left completely untouched: not checked out, not reset, not staged, not cleaned.

Both merges ran in a **fresh detached worktree at a short path**, `C:/b679`, created from `origin/main`, with `.env` and `.env.local` copied in and a real `npm ci` run. The result went up with `git push origin HEAD:main`, so the stale local `main` ref in `C:/b575` was never written. Push succeeded on attempt 1; `git fetch origin` then confirmed `origin/main == local HEAD == fdde504f`. Both tags pushed.

## Merge mechanics, one at a time with verification between

**BL-678 first.** Zero conflicts. Verified before proceeding: `apify.ts` **64 added, 0 deleted**; all five guards present; BACKLOG 100 to 101.

**BL-676 second.** One conflict, `BACKLOG.md`, both sides having appended after a shared base. Resolved as a **union, both sides kept**, by deleting only the three marker lines.

**The union, counted properly on the whole file with `wc -l`, never with `head`:**

| ref | `## BL-` entries |
| --- | --- |
| merge base `0a69fcc4` | 99 |
| `origin/main` `d6373647` (base + BL-673) | 100 |
| after the BL-678 merge | 101 |
| `checkpoint/BL-676` (base + BL-676) | 100 |
| **final merged result** | **102** |

99 + BL-673 + BL-678 + BL-676 = 102. `BL-673`, `BL-676` and `BL-678` each appear exactly once.

**No `$2` capture-group corruption.** Counted as occurrences across the whole file, not lines and not truncated: **112** on the merged result, **112** on the pre-merge HEAD and **112** on `checkpoint/BL-676`. Identical on every ref, so none was introduced or lost.

**Conflict markers on the merged tree: 0**, grepped across `*.ts`, `*.tsx`, `*.md`, `*.prisma` and `*.json`, and `git diff --diff-filter=U` is empty.

**No schema change and no `prisma migrate`.** `prisma/schema.prisma` is not in the diff. `npx prisma generate` was still run after `npm ci` and before `tsc`, because `npm ci` wipes the generated client.

---

## Confirmed on the MERGED result

### All eleven Apify request paths are guarded

Counted on the merged tree, not inherited from BL-678's report:

| guard mechanism | file:line | paths covered |
| --- | --- | --- |
| `if (APIFY_HARD_OFF)` early return | `apify.ts:254`, `:579`, `:796`, `:1316`, `:1769` | **5** |
| `apifyCredential()` chokepoint | `apidojo.ts:139` | **4** (all four `await fetch(actorRunUrl…)` sites) |
| `apifyCredential()` | `account-profile.ts:136` | **1** |
| `apifyCredential()` | `verify-cascade.ts:203` | **1** |
| | | **11** |

`apify.ts` has exactly **5** `getApiKey()` call sites and the harness asserts **5 of 5** are preceded by a guard, so a future sixth unguarded site fails the test rather than silently reopening the hole.

### `apify.ts` shows additions and ZERO deletions

`git diff --numstat d6373647 fdde504f -- src/lib/apify.ts` returns **`64  0`**, and grepping the diff for removed lines in that file returns nothing at all. Nothing was refactored and nothing was removed from the money-critical tracking path, exactly as BL-677 warned.

### The guard is unconditional and not re-enablable by any environment variable

`src/lib/apify-hard-off.ts:62` reads `export const APIFY_HARD_OFF: true = true;`. Typed `true` rather than `boolean`, so TypeScript itself knows the value. The module reads no environment variable in code and imports nothing, both asserted by the harness. The **only** surviving live `process.env.APIFY_API_KEY` read anywhere in `src/` is `apify.ts:163` inside `getApiKey()`, which is now unreachable because all five of its callers return before it.

### Every guarded path returns NULL never 0, with the one documented exception

| guard | returns |
| --- | --- |
| `apify.ts:254` `fetchInstagramFallbackItem` | `null` |
| `apify.ts:579` `fetchTikTokStatsLegacy` | **throws** `apify hard off (BL-678)` |
| `apify.ts:796` `fetchInstagramStatsApiScraperSingle` | `null` |
| `apify.ts:1316` `fetchTikTokStatsBatchLegacy` | `new Map()` |
| `apify.ts:1769` `fetchInstagramStatsBatchApiScraper` | `new Map()` |
| `apidojo.ts` x4 | `null` / empty `Map` via the existing `if (!token)` branches |
| `account-profile.ts` | `{ ok: false }` |
| `verify-cascade.ts` | `{ found: false, transient: true }` |

Grepping the merged `apify.ts` for a zero-valued stat inside any guard returns **0**, and counting `throw new Error` inside guards returns **exactly 1**, which is the declared case. That one is safe because nothing new handles it: `fetchTikTokStatsLegacy` is declared `Promise<ClipStats>` and its own header documents that it throws, both call sites already wrap it in try/catch, and the final rethrow lands on `tracking.ts`'s pre-existing `fetchThrew` guard which writes **no** ClipStat row. Returning null would have meant widening the signature and rewriting both call sites, the very refactor BL-677 advised against; fabricating a `ClipStats` would have meant inventing zeros.

### Both proof harnesses re-run on the merged tree

| harness | result |
| --- | --- |
| `scripts/test-bl-678-apify-hard-off.ts` | **28 passed, 0 failed** |
| `scripts/test-bl-676-campaign-refusal.ts` | **44 passed, 0 failed** |

The BL-678 harness deliberately **sets** a valid-looking `APIFY_API_KEY` and `APIFY_TOKEN`, stubs `globalThis.fetch` with a recorder that performs no I/O, drives the real entry points, and records:

```
PASS  apidojo made ZERO requests to apify.com  hits=0
PASS  apify.ts made ZERO requests to apify.com  hits=0
PASS  the two profile/verify sites made ZERO requests to apify.com  hits=0
PASS  apify.ts has exactly 5 getApiKey() call sites  found=5
PASS  every one of them is preceded by an APIFY_HARD_OFF guard  guarded=5/5
PASS  no guard in apify.ts returns a zero-valued stat
PASS  ZERO requests to any apify.com host across the entire run, with a key SET  apify hits=0
```

**No Apify actor was run at any point in this round, and no key was read, set or printed.** The only key values that exist anywhere are the obvious fakes the harness assigns to itself, and they are never sent because `fetch` is stubbed.

## Gates, honestly

| gate | result |
| --- | --- |
| `npm ci` | **exit 0** |
| `npx prisma generate` | **exit 0**, run after `npm ci` and **before** `tsc` |
| `npx tsc --noEmit` | **exit 0**, log 0 lines |
| `npm run build` | **BUILD_EXIT=0**, echoed from `$?`, never piped through `tail`; "Compiled successfully in 17.4s" |
| hooks gate `lint:hooks` | **eslint present and actually executed** (`node_modules/.bin/eslint`, eslint **9.39.4**); `--max-warnings 11` → **11 problems, 0 errors, 11 warnings**, at the cap, passing |
| `check:prisma-bypass`, `check:removed-fields` | ran (prebuild) |

## Money files and the ring-fenced files, blob OID on BOTH refs

`git rev-parse <ref>:<path>` on `d6373647` and on the merged `fdde504f`. All **IDENTICAL**:

| file | blob |
| --- | --- |
| `src/lib/clip-earnings-writer.ts` | `7aa6be48` |
| `src/lib/earnings-calc.ts` | `797e2098` |
| `src/lib/balance.ts` | `e887f80a` |
| `src/lib/tracking.ts` | `847dcf70` |
| `src/lib/clip-earnings-invariant-middleware.ts` | `61cef393` |
| `src/lib/money-decimal.ts` | `ef5cdae7` |
| `src/lib/campaign-era.ts` | `106e16ad` |
| `src/app/api/campaigns/[id]/route.ts` (BL-676's ring fence) | `8542fc04` |
| `src/app/(app)/campaigns/CampaignsRedesign.tsx` (completed cards stay non-clickable) | `1c1fc6f0` |

---

## AFTER THE PUSH — proving nothing broke, on live production data

Pushed **13:11 UTC**. Every figure below is read after that, and the tracking evidence is taken from the **14:00 UTC batch**, which started 49 minutes after the push and is therefore unambiguously post deploy. All reads were read-only `SELECT`s with timestamps cast to `::text`, anchored against DB `now()`.

### Apify attempts: zero, and the honest caveat about what that proves

```
attempts_since_push | newest
                  0 | (none)
```

**Not one Apify request has been logged since the push.** The 13:00 and 14:00 hours have no rows at all.

**The caveat, stated rather than glossed:** BL-673's earlier deploy had already collapsed the rate from 276 an hour at 10:00 to 8 at 11:00 and 3 at 12:00, and the 13:00 hour was already empty when checked at 13:16, before the guard could have taken effect. So the ledger on its own cannot separate "the guard works" from "the traffic had already stopped". **The decisive evidence is the harness, not the ledger:** it sets a valid-looking key, stubs `fetch` with a recorder, drives the real entry points on the merged tree and records **zero requests to any apify.com host**. The ledger corroborates in production; it does not carry the proof alone.

| hour (UTC) | attempts | successes |
| --- | --- | --- |
| 09:00 | 242 | 0 |
| 10:00 | 276 | 0 |
| 11:00 | 8 | 0 |
| 12:00 | 3 | 0 |
| **13:00 (push at 13:11)** | **0** | 0 |
| **14:00** | **0** | 0 |

### The ledger query for the owner

**The attempt COUNT must go to ZERO, not merely stay unsuccessful.** A row here is written only after a real outbound HTTPS request completes with a non-ok response, so a row existing at all is proof a request was made. With the guard in place no request is made, so no row can be written.

```sql
SELECT to_char(date_trunc('hour', "occurredAt"), 'YYYY-MM-DD HH24:00') AS hour,
       COUNT(*)                                 AS attempts,
       SUM(CASE WHEN success THEN 1 ELSE 0 END) AS successes
FROM apify_usage_entries
WHERE provider LIKE 'actor:apify%'
  AND "occurredAt" > now() - interval '24 hours'
GROUP BY 1 ORDER BY 1;
```

**Expected: zero rows returned for every hour after 2026-07-29 13:15 UTC.** Any row at all means a path was missed, and the `provider` column names which one.

### Tracking still writes, on all three platforms, and wrote no regressive zero

ClipStat rows written from 13:30 UTC onward, i.e. the 14:00 batch:

| platform | rows written | written as 0 | written NULL | min views | max views | newest |
| --- | --- | --- | --- | --- | --- | --- |
| instagram | 44 | 0 | 0 | 115 | 68,439 | 2026-07-29 14:02:28 |
| tiktok | 20 | 1 | 0 | 0 | 184,200 | 2026-07-29 14:02:29 |
| youtube | 5 | 1 | 0 | 0 | 742 | 2026-07-29 14:02:15 |

**The two zero rows were classified rather than waved past**, because "none written as 0" was an explicit requirement. Both are the **first ever stat** for a brand new PENDING clip with no prior row of any kind, aged 27 and 23 minutes, `earnings = 0.00` on both. **Zero rows overwrote a positive value.** A genuinely new clip that has not been watched yet legitimately reads 0, and that is a different event from a measurement being lost.

### No stored views moved down, on any platform

| platform | transitions | **moved down** | moved up | flat |
| --- | --- | --- | --- | --- |
| instagram | 43 | **0** | 38 | 5 |
| tiktok | 15 | **0** | 12 | 3 |
| youtube | 4 | **0** | 1 | 3 |

Structurally this is what the guard guarantees: a guarded path writes **no row at all**, and a row that is never written cannot be lower than the one before it.

### Earnings unchanged, and growing normally

| reading | approved clips | total earnings | total base | total bonus | invariant breaks |
| --- | --- | --- | --- | --- | --- |
| 13:09 UTC, before the push | 2905 | $6,257.84 | $5,999.32 | $258.53 | **0** |
| 14:04 UTC, after the deploy | 2905 | $6,265.56 | $6,006.91 | $258.66 | **0** |

Same clip count, and `earnings ≈ baseEarnings + bonusAmount` holds on every one of the 2,905 rows in both readings. The **+$7.72** is ordinary growth from views rising during the 14:00 tick, which is the correct behaviour: the money path is untouched and still crediting. Across all 3,488 approved clips there is **not one negative** `earnings` or `baseEarnings`.

### Submit is unblocked on all three platforms, live and post deploy

| platform | submitted since 13:15 | newest |
| --- | --- | --- |
| tiktok | 5 | 2026-07-29 13:37:12 |
| youtube | 2 | 2026-07-29 13:52:14 |
| instagram | 1 | 2026-07-29 13:56:59 |

Eight real clipper submissions across all three platforms after the deploy, the newest seven minutes before this check.

### Verification: proven Apify-independent, but NOT observed post deploy

**Stated plainly because it is the one thing this round could not watch happen: no account verification has been attempted anywhere on the platform since 13:15 UTC**, so there is no post-deploy verification event to point at. Nobody tried. What IS established:

* **The guarded tier has never once been used.** Across the whole table, all time, `lastVerifySource` has never held `tiktok-apidojo-profile`. Guard 11 removes a tier that has never produced a single verification.
* **Instagram already moved off Apify before this round.** `apify-ig-profile` was last a source on **2026-07-22 08:26**, before the cutover, and every Instagram verification since runs on `hikerapi-ig-profile` (37 of them).
* **All three platforms verified successfully in the last 24 hours**, every one on a non-Apify source: Instagram 6, TikTok 5, YouTube 8, newest at 10:58, 10:04 and 10:19 UTC respectively, on `hikerapi-ig-profile`, `lamatok-profile` and `tier-1`.
* **The merged code was exercised directly.** The harness drives `verify-cascade`'s TikTok tier 2 on the merged tree and it returns `{ found: false, transient: true }` while making zero Apify requests. `transient` is the correct signal and the pre-existing one: the cascade falls through to its next tier or refunds the slot, so a clipper is never blocked.

The next verification attempt on any platform will confirm it in traffic. Nothing suggests it will fail, and nothing here claims it has been observed.

---

## Safety

Merge only. No file was authored this round beyond the BACKLOG union resolution. No schema change, no `prisma migrate`, no data mutation, no clip's earnings or status touched. **No Apify actor was run and no Apify endpoint of any kind was contacted**, free or paid. **No key was read, set or printed.** Live database work was read-only `SELECT`s through the sanctioned `scripts/run-select.js`, every timestamp cast to `::text` and anchored to DB `now()`. No clipper handle or personal content appears. `C:/b575` was left untouched. Nothing held by a live round was merged. No dashes used as bullets, in code, commit messages or this report.
