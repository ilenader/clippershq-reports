# BL-678 (ClippersHQ) — Apify is OFF by construction: no request can be built, and no key can turn it back on

## NOTHING BROKE. Tracking, verification and submit are all confirmed working on Instagram, TikTok and YouTube, and the reason is stronger than a test: production's own ledger shows the last successful Apify call was **2026-07-24 19:03:14Z**, and those five were a LOCAL probe, so **no production ClipStat in the last five days has come from Apify**. Removing a source that has supplied nothing for five days cannot move a stored view. Rollback if ever needed: `git revert 3940e290`, or `git reset --hard pre-BL-678`.

> **Filename note, per CONVENTION.md.** `reports/BL-678.md` was already taken by a different project (clipper-finder's `/v2/track/by/id` music research). The collision check was run against `origin/main` before pushing and that file was **not** touched. This report is published beside it under the `-<project>-<slug>` suffix the convention prescribes, which the convention itself cites this agent's earlier `BL-676-clippershq-campaign-refusal.md` as precedent for.

**Branch** `checkpoint/BL-678` @ `3940e290` (pushed, `origin/checkpoint/BL-678 == local HEAD`, verified by `scripts/safe-push.mjs`).
**Base** `d6373647` (`post-merge-BL-675`). **Tags** `pre-BL-678` (d6373647) and `post-BL-678` (3940e290), both pushed.
**Worktree** `C:/b678`, short path, `node_modules` never junctioned. **DB `now()` at query time: 2026-07-29 12:34:49.242446+00.**

| file | change |
| --- | --- |
| `src/lib/apify-hard-off.ts` | NEW, the switch |
| `src/lib/apify.ts` | **+64 / −0**, five guards, nothing removed, nothing refactored |
| `src/lib/scraper-providers/apidojo.ts` | +15 / −1, one credential chokepoint covering four paths |
| `src/lib/account-profile.ts` | +13 / −2, one guard |
| `src/lib/verify-cascade.ts` | +13 / −2, one guard |
| `scripts/test-bl-678-apify-hard-off.ts` | NEW, the proof harness |
| `BACKLOG.md` | +14, the BL-678 entry |

---

## PART 1 — the hard guard

### The switch is a constant, and that is the whole design

BL-611 designed this as `APIFY_HARD_OFF=1`, an environment flag. BL-677 then measured production and made that design the wrong one. The entire risk BL-677 identified is *"somebody sets a credential while debugging something unrelated and nobody is told"*. A switch that can be flipped by setting a variable does not remove that risk, it renames it: it adds a **second** string that someone can get wrong.

So `src/lib/apify-hard-off.ts` declares:

```ts
export const APIFY_HARD_OFF: true = true;
```

Typed `true`, not `boolean`, so TypeScript itself knows the value and any future `if (!APIFY_HARD_OFF)` branch is statically dead. The module **reads no environment variable and imports nothing** (both asserted by the harness). There is no value anyone can set, in Railway or in a `.env.local`, that turns Apify back on. Re-enabling it is a code change, in a pull request, with a human reading it.

### There is NO single global chokepoint, so every one of the eleven paths is guarded

Stated plainly, because a guard that misses a path is worse than no guard. Four separate modules construct their own Apify request; there is no shared function they all pass through. What they DO share is that each reads a credential immediately beforehand, and three of the four already had a correct, already-proven "no credential means do nothing" branch right after that read.

**Group A, three credential chokepoints covering six sites, with ZERO new control flow.** `apifyCredential()` always returns null, so the branch that now runs is the branch that has already run on every call since the 2026-07-22 cutover:

| chokepoint | covers | existing branch that now fires |
| --- | --- | --- |
| `apidojo.ts:154` `getApifyToken()` | `:416`, `:557`, `:706`, `:781` (all four apidojo fetchers) | `if (!token) return null` / `return result` (empty Map) |
| `account-profile.ts:135` | `:143` | `if (!token) return { ...base, ok: false }` |
| `verify-cascade.ts:200` | `:216` | `if (!apifyToken) return { found: false, transient: true }` |

The environment read is **gone, not overridden**: `process.env.APIFY_API_KEY` and `process.env.APIFY_TOKEN` are no longer consulted anywhere in those three files, so no value set anywhere reaches them.

**Group B, five individual guards inside `apify.ts`.** Its `getApiKey()` **throws** on a missing key rather than returning null, so feeding it a null would turn one throw into another and change nothing. Each of its five request-building functions is guarded instead, with the guard placed **before** `getApiKey()` and therefore before any credential is read and before the URL on the following line exists:

| guard | function | actor | URL line it prevents |
| --- | --- | --- | --- |
| `apify.ts:254` | `fetchInstagramFallbackItem` | `apify/instagram-scraper` | `:264` |
| `apify.ts:579` | `fetchTikTokStatsLegacy` | `clockworks/tiktok-scraper` | `:587` |
| `apify.ts:796` | `fetchInstagramStatsApiScraperSingle` | `apify/instagram-api-scraper` | `:803` |
| `apify.ts:1316` | `fetchTikTokStatsBatchLegacy` | `clockworks/tiktok-scraper` | `:1340` |
| `apify.ts:1769` | `fetchInstagramStatsBatchApiScraper` | `apify/instagram-api-scraper` | `:1785` |

The harness asserts mechanically that `apify.ts` has exactly five `getApiKey()` call sites and that **every one of them** is preceded by an `APIFY_HARD_OFF` guard, so a future edit that adds a sixth unguarded site fails the test rather than silently reopening the hole.

### Fail safe, and the ONE deviation, declared loudly

Ten of the eleven guards return the site's own existing empty shape: `null`, an empty `Map`, `{ ok: false }`, `{ found: false, transient: true }`. **NULL, never 0.** That is what makes it safe: `tracking.ts` reads a null and writes **no ClipStat row at all**, so it does not overwrite views, does not store a 0 and does not flip `videoUnavailable`. A clip that would have escalated to Apify keeps its last real number and waits for HikerAPI or LamaTok on the next tick. Earnings are `(views / 1000) x cpm` off the **stored** value, so a clip that keeps its last real number keeps paying its last real amount.

**The deviation: `fetchTikTokStatsLegacy` throws instead of returning null.** The brief asked for "never throw", and this one function cannot honour it without breaking a harder rule:

* It is declared `Promise<ClipStats>`, **not nullable**, and its own header documents "throws on HTTP error, empty results, or actor error sentinel". Throwing IS its failure contract.
* Returning null would mean widening the signature and then rewriting both call sites, which is precisely the `apify.ts` refactor BL-677 ranked fourth and advised against on a money-critical file.
* Fabricating a `ClipStats` to return would mean **inventing zeros**, which is the one thing that must never happen.

So the guard raises the same failure the function already raises, one line earlier, without a credential and without a request. **Nothing new handles it.** Both call sites (`apify.ts:521` and `:542`) already wrap it in try/catch and fall through to apidojo, which is itself guarded and returns null; the final rethrow is the pre-existing throw-on-total-failure contract, caught by `tracking.ts`'s `fetchThrew` guard, which writes no row. This is byte for byte the path production has taken on every TikTok escalation since the cutover, where the invalid token produced a 401 and then this same throw. **NULL never 0 holds, and no clipper is zeroed or frozen.**

The harness confirms the outcome rather than the theory: driving the real `fetchClipStats` on a TikTok URL yields `{"threw":"apify hard off (BL-678)"}` and never a fabricated zero, and the cron batch fan-out returns without throwing at all.

---

## PART 2 — proving the six thousand daily calls stop

### The code terminates before a request is built

The harness does the opposite of hiding the key. It **sets** `APIFY_API_KEY` and `APIFY_TOKEN` to truthy fake strings before any module loads, which is exactly the state that used to make production fire thousands of requests a day, then replaces `globalThis.fetch` with a recorder that performs **no I/O whatsoever** and logs every call by hostname. It then drives the real exported entry points.

```
=== BL-678: a valid-looking Apify key is SET, and still nothing calls Apify ===
APIFY_API_KEY present=true (fake, never sent)
APIFY_TOKEN   present=true (fake, never sent)

PASS  APIFY_HARD_OFF is true
PASS  apifyCredential() is null even with both env vars SET
PASS  the switch module reads NO environment variable in code
PASS  the switch module imports nothing
PASS  the switch is a const, so no assignment can flip it
PASS  fetchApidojoTikTokSingle returns NULL (not 0, not a throw)
PASS  fetchApidojoInstagramSingle returns NULL
PASS  fetchApidojoTikTokBatch returns an EMPTY map
PASS  fetchApidojoInstagramBatch returns an EMPTY map
PASS  Instagram single returns NULL stats, never 0
PASS  the cron batch fan-out did not throw
PASS  the cron batch produced NO zero-valued stat for any clip
PASS  verify-cascade tier 2 returns { found:false, transient:true }
PASS  apify.ts has exactly 5 getApiKey() call sites  found=5
PASS  every one of them is preceded by an APIFY_HARD_OFF guard  guarded=5/5
PASS  no guard in apify.ts returns a zero-valued stat

--- 6. the total ---
  outbound attempts recorded: 0
  distinct hosts: (none)
PASS  ZERO requests to any apify.com host across the entire run, with a key SET  apify hits=0

28 passed, 0 failed
```

The runtime logs show each guard firing by name before the tier that used to call out:

```
[APIFY-HARD-OFF] skipped=fetchTikTokStatsLegacy actor=clockworks/tiktok-scraper reason=apify-permanently-disabled-BL-678
[APIFY-HARD-OFF] skipped=fetchInstagramStatsApiScraperSingle actor=apify/instagram-api-scraper reason=apify-permanently-disabled-BL-678
[APIFY-HARD-OFF] skipped=fetchTikTokStatsBatchLegacy actor=clockworks/tiktok-scraper urls=1 reason=apify-permanently-disabled-BL-678
[APIFY-HARD-OFF] skipped=fetchInstagramStatsBatchApiScraper actor=apify/instagram-api-scraper urls=1 reason=apify-permanently-disabled-BL-678
```

### The ledger query for the owner, and what it should show

**The attempt COUNT should go to ZERO. Not "stay unsuccessful": zero rows.** Today's rows are written after a real outbound HTTPS request completes with a non-ok response, so a row existing at all is proof a request was made. After this deploys, no request is made, so no row can be written.

```sql
SELECT to_char("occurredAt",'YYYY-MM-DD HH24:00') AS hour,
       COUNT(*)                                    AS attempts,
       SUM(CASE WHEN success THEN 1 ELSE 0 END)    AS successes
FROM apify_usage_entries
WHERE provider LIKE 'actor:apify%'
  AND "occurredAt" > now() - interval '24 hours'
GROUP BY 1 ORDER BY 1;
```

**Expected after deploy: zero rows returned for every hour that follows it.** Any row at all means a path was missed, and the `provider` column names which one.

### Measured baseline, and a correction to BL-677's inference

BL-677 measured 7,849 attempts since the cutover and called the rate "sharply UP". Re-measured this round against the same ledger:

| day | attempts | successes |
| --- | --- | --- |
| 2026-07-22 (from 11:12Z) | 140 | 0 |
| 2026-07-23 | 148 | 0 |
| 2026-07-24 | 194 | **5 (a LOCAL probe, not production)** |
| 2026-07-25 | 313 | 0 |
| 2026-07-26 | 643 | 0 |
| 2026-07-27 | 1984 | 0 |
| 2026-07-28 | 2854 | 0 |
| 2026-07-29 (to 12:34Z) | 1584 | 0 |

**BL-677's inference is now CONFIRMED, and by an event rather than an argument.** It suspected the Instagram thumbnail retry loop was the volume driver but could not prove it. Hourly today:

| hour (UTC) | 07 | 08 | 09 | 10 | **11** | **12** |
| --- | --- | --- | --- | --- | --- | --- |
| attempts | 205 | 321 | 248 | 276 | **8** | **3** |

The collapse from 276 an hour to 8 lands exactly when **BL-673 merged to `main` (`d6373647`) and deployed**, moving Instagram cover capture off `fetchClipStats`. So the retry loop WAS the driver, and BL-673 already removed roughly 97 percent of the volume. **What is left, three to eight an hour, is the genuine tracking escalation, and BL-678 takes that to zero.** BL-677's "$500 a month" figure was computed off the 6,000-a-day rate and should therefore be read as an upper bound that BL-673 has already reduced; the exposure is real either way, because the rate was driven by a retry loop that could return with any future coverless population.

---

## PART 3 — the local keys, and what only the owner can do

BL-677 counted **73 git worktrees on this machine, 41 of them holding a `.env.local` with a real `apify_`-prefixed key**, and traced nine post-cutover actor runs to local environments. This round runs inside one worktree and **cannot and must not** clean the owner's machine. **No key value was read, set, printed or redacted-printed anywhere in this round.**

**What the owner must do, precisely:**

1. Open the **source** `.env.local` at the repository root, find the line beginning `APIFY_API_KEY=`, and replace everything after the `=` with the single word `DISABLED`. If a line beginning `APIFY_TOKEN=` exists, do the same to it.
2. Do the same in **every worktree copy**. The worktrees are the `C:/b*`, `C:/bl*`, `C:/wt/*` and `C:/chq-*` directories that `git worktree list` prints; 41 of them currently hold a `.env.local`.
3. From then on, when a round copies `.env.local` into a new worktree, it copies the disabled value, so the problem does not regrow.
4. Do **not** set an Apify key on Railway. Production has never needed one since the cutover and now provably cannot use one.

**What the guard already does for you, and what it does not.** In code, those keys are now inert: every path that would read one either no longer reads the environment at all or returns before it does, so a worktree holding a live key can run the app, the cron and the submit path all day without an Apify request being constructed. **The gap the guard cannot close** is a script that calls Apify's REST API *directly* rather than through these modules, which is exactly how BL-665 and BL-673 each ran actors by accident. Only removing the value stops that. **Do step 1.**

---

## PART 4 — the eleven now-provably-dead call sites, and none was deleted

With every callout impossible, these are dead code. **Nothing here was deleted this round**, deliberately: BL-677 ranked deletion fourth and advised against it, and the point of the guard is to let a later round delete with proof rather than hope.

| # | file:line (request) | enclosing function | actor | tracking path? |
| --- | --- | --- | --- | --- |
| 1 | `src/lib/apify.ts:264` | `fetchInstagramFallbackItem` (`:249`) | `apify/instagram-scraper` | **YES, apify.ts** |
| 2 | `src/lib/apify.ts:587` | `fetchTikTokStatsLegacy` (`:558`) | `clockworks/tiktok-scraper` | **YES, apify.ts, and the one that throws** |
| 3 | `src/lib/apify.ts:803` | `fetchInstagramStatsApiScraperSingle` (`:787`) | `apify/instagram-api-scraper` | **YES, apify.ts, the dominant path** |
| 4 | `src/lib/apify.ts:1340` | `fetchTikTokStatsBatchLegacy` (`:1309`) | `clockworks/tiktok-scraper` | **YES, apify.ts, cron batch** |
| 5 | `src/lib/apify.ts:1785` | `fetchInstagramStatsBatchApiScraper` (`:1762`) | `apify/instagram-api-scraper` | **YES, apify.ts, cron batch rescue floor** |
| 6 | `src/lib/scraper-providers/apidojo.ts:416` | `fetchApidojoTikTokSingle` (`:410`) | `apidojo/tiktok-scraper` | yes, but outside apify.ts |
| 7 | `src/lib/scraper-providers/apidojo.ts:557` | `fetchApidojoInstagramSingle` (`:551`) | `apidojo/instagram-scraper-api` | yes, but outside apify.ts |
| 8 | `src/lib/scraper-providers/apidojo.ts:706` | `fetchApidojoTikTokBatch` (`:698`) | `apidojo/tiktok-scraper` | yes, but outside apify.ts |
| 9 | `src/lib/scraper-providers/apidojo.ts:781` | `fetchApidojoInstagramBatch` (`:766`) | `apidojo/instagram-scraper-api` | yes, but outside apify.ts |
| 10 | `src/lib/account-profile.ts:143` | `fetchInstagramProfile` (`:125`) | IG profile actor | no, display only |
| 11 | `src/lib/verify-cascade.ts:216` | `tiktokTier2` (`:190`) | `apidojo/tiktok-scraper` | no, verification tier 2 |

**Sites 1 to 5 are the ones that need the most care.** They live inside `src/lib/apify.ts`, the fetch layer the tracking cron depends on, and their null-shaped returns are precisely what `tracking.ts` relies on to keep last-known views and never store a 0. Their tier ordering, gone-counter skips and carousel quarantines are the accumulated output of BL-543, BL-550, BL-580, BL-590, BL-605 and BL-610. Deleting them means restructuring `fetchTikTokStats`, `fetchInstagramStats` and both batch fan-outs. That belongs in its own Opus round with a live regression harness, after the guard has run in production for a while, and never as a side effect of a cleanup.

**Sites 6 to 11 are the cheap ones.** They are self-contained functions in three smaller files with no tier ordering to preserve, and site 11 has never once been used (see PART 5).

---

## PART 5 — proof that nothing broke

### The decisive fact, from production's own ledger

```
successful_apify_calls_since_cutover | newest_success
                                   5 | 2026-07-24 19:03:14.224
```

Five successes since the 2026-07-22 cutover, all on 2026-07-24, and BL-677 attributed those to BL-665's **local** probe. **No production ClipStat in the last five days has come from Apify.** A source that has supplied nothing for five days cannot change a stored view when it is removed. Everything below confirms that from the other direction.

### Tracking is writing, on all three platforms, and not writing zeros

Last 24 hours:

| platform | rows written | written as 0 | written NULL | min views | max views | newest |
| --- | --- | --- | --- | --- | --- | --- |
| instagram | 1331 | **0** | 0 | 1 | 120,429 | 2026-07-29 12:10:27 |
| tiktok | 749 | 12 | 0 | 0 | 183,500 | 2026-07-29 12:10:28 |
| youtube | 437 | 24 | 0 | 0 | 830 | 2026-07-29 12:02:20 |

**The 36 zero rows were investigated rather than waved past**, because "none written as 0" was an explicit requirement:

| classification | count |
| --- | --- |
| first ever stat for that clip (a genuinely new clip with no views yet) | 17 |
| the prior value was also 0 | 12 |
| **overwrote a POSITIVE prior value** | **7** |

All seven are **YouTube**, prior views 1 or 2, `earnings = 0.00` on every one, `videoUnavailable = false`. **YouTube has never used Apify at all** (its stats come from the YouTube Data API), so this is a pre-existing, platform-specific micro-behaviour entirely outside this round's blast radius, it is not caused by this change and cannot be. It is flagged below, not fixed.

### No downward movement introduced, with the baseline for comparison

Transitions in the last 24 hours, on `main` before this deploys:

| platform | transitions | moved down | moved up | flat |
| --- | --- | --- | --- | --- |
| instagram | 951 | 2 | 818 | 131 |
| tiktok | 412 | 3 | 360 | 49 |
| youtube | 124 | 3 | 46 | 75 |

That small residue is pre-existing platform reporting jitter. **The guard cannot add to it, structurally**: a guarded path writes no row at all, and a row that is never written cannot be lower than the one before it. Re-run the same query after deploy and the down-counts should not rise.

### Verification works on all three, and is already Apify-free

Verify sources actually used, from `clip_accounts`:

| platform | source | count (7 days) | newest |
| --- | --- | --- | --- |
| Instagram | `hikerapi-ig-profile` | 37 | 2026-07-29 10:58:32 |
| TikTok | `lamatok-profile` | 13 | 2026-07-29 10:04:41 |
| TikTok | `tiktok-plain-fetch` | 2 | 2026-07-23 11:43:51 |
| YouTube | `tier-1` | 24 | 2026-07-29 10:19:10 |
| YouTube | `tier-2` | 1 | 2026-07-27 03:58:18 |

**All time**, `apify-ig-profile` was last a source on **2026-07-22 08:26**, before the cutover, and BL-612 replaced it; and **`tiktok-apidojo-profile` has never appeared as a source at all**, so guard 11 removes a tier that has never once produced a verification. 34 Instagram, 13 TikTok and 25 YouTube accounts verified successfully in the last seven days, the newest three all within two hours of this report.

### Submit is unblocked on all three

Clips created in the last seven days, newest within the hour on every platform:

| platform | submitted | newest |
| --- | --- | --- |
| instagram | 171 | 2026-07-29 12:11:17 |
| tiktok | 58 | 2026-07-29 11:32:24 |
| youtube | 39 | 2026-07-29 11:27:10 |

### Earnings baseline, unchanged and internally consistent

| approved clips | total earnings | total base | total bonus | invariant breaks |
| --- | --- | --- | --- | --- |
| 2905 | $6,250.26 | $5,991.91 | $258.36 | **0** |

`earnings ≈ baseEarnings + bonusAmount` holds on every one of the 2,905 rows. Nothing in this round writes to a clip, and the 6 money files are byte identical, so this is a baseline to compare against after deploy rather than a before-and-after.

---

## Safety and gates

| check | result |
| --- | --- |
| `npm ci` | **exit 0** |
| `npx prisma generate` | **exit 0**, run after `npm ci` and **before** `tsc` |
| `npx tsc --noEmit` | **exit 0**, log 0 lines |
| `npm run build` | **BUILD_EXIT=0**, echoed from `$?`, never piped through `tail`; "Compiled successfully in 17.1s" |
| hooks gate `lint:hooks` | **eslint present and actually executed** (`node_modules/.bin/eslint`, eslint **9.39.4**); `--max-warnings 11` → **11 problems, 0 errors, 11 warnings**, at the cap, passing |
| `check:prisma-bypass`, `check:removed-fields` | ran (prebuild) |

**Money files, blob OID against `origin/main` `d6373647`, all IDENTICAL:** `clip-earnings-writer.ts` `7aa6be48`, `earnings-calc.ts` `797e2098`, `balance.ts` `e887f80a`, **`tracking.ts` `847dcf70`**, `clip-earnings-invariant-middleware.ts` `61cef393`, `money-decimal.ts` `ef5cdae7`, `campaign-era.ts` `106e16ad`.

**`apify.ts` was not refactored and nothing was deleted from it:** `git diff --numstat` reports **64 added, 0 removed**, and a grep for removed lines in that file returns nothing.

**No Apify actor was run.** No Apify endpoint of any kind was contacted this round, free or paid: the harness stubs `fetch` and performs no I/O. **No key was read, set or printed**, and the only key values that appear anywhere are the obvious fakes the harness assigns to itself. No schema change, no `prisma migrate`, no data mutation, no clip's earnings or status touched. Live database work was read-only `SELECT`s through the sanctioned `scripts/run-select.js`, every timestamp cast to `::text` and anchored to DB `now()` = 2026-07-29 12:34:49.242446+00. No clipper handle or personal content appears. Nothing held by BL-679 was touched: it has no branch and no worktree on this machine, and this round worked only in `C:/b678`. No dashes used as bullets, in code, comments or this report.

## Flagged, not fixed

* **Seven YouTube clips wrote a 0 over a prior 1 or 2 views in the last 24 hours.** Earnings $0 on all seven, `videoUnavailable = false`, and YouTube never touches Apify, so it is unrelated to this round. Worth its own look: the question is whether the YouTube Data API genuinely reported 0 or whether a miss is being coerced.
* **BL-677's "$500 a month" should be re-derived.** It was computed from the 6,000-a-day rate that BL-673's deploy has already cut by about 97 percent. The exposure is still real, because the driver was a retry loop that any future coverless population would restart, but the headline figure is now an upper bound.
* **Deleting the eleven dead call sites** is the natural follow-up, and PART 4 is the map for it. Sites 6 to 11 are cheap; sites 1 to 5 are inside `apify.ts` and need their own round with a live regression harness.
