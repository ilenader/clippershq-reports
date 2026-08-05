# BL-715 — merge BL-713 to main (TikTok photo slideshows resolve their view counts)

Date 2026-08-05. Merge commit **`70e3fa4e`**, parents `8b5aaf57` (main) + `bdcec866` (checkpoint/BL-713).
**origin/main == local HEAD == 70e3fa4e**, verified by `git ls-remote` after the push. Tags
`pre-merge-BL-715` (8b5aaf57) / `post-merge-BL-715` (70e3fa4e), both pushed. Merge only: no new code was
written this round.

## STEP 0 — TRUTH, WITH SHAS

• `origin/checkpoint/BL-713` = **`bdcec8668e92136c100c8e44a792902e538e5378`**, present on origin.
• `git merge-base --is-ancestor origin/checkpoint/BL-713 origin/main` → **NOT an ancestor**: genuinely
  unmerged against `origin/main` = `8b5aaf5761cc6f34c8b1144a51e4b9f4550e5215`.
• **Non-empty `.ts` diff**, 2 TypeScript files: `src/lib/scraper-providers/lamatok.ts` (+194/-7) and
  `scripts/test-bl713-slideshow.ts` (+95, new). Four files total, the other two being `BACKLOG.md` and
  `reports/BL-713-clippershq-slideshow-fix.md`.
• **Nothing a live round holds was merged.** `git ls-remote origin "refs/heads/*BL-714*"` returned nothing,
  so BL-714 has no branch on origin and there was no docs-only candidate to consider. Exactly one branch was
  merged.

## HOW THE HELD WORKTREE WAS HANDLED

`C:/b575` holds branch `main` and was found **both stale and dirty**: HEAD `91b84410`, **55 commits behind**
`origin/main`, with **77 dirty entries** (staged modifications to `BACKLOG.md` and `prisma/schema.prisma`
plus a run of staged deletions under `docs/` and `public/splash/`). The primary tree at
`.../Desktop/ClippersHQ` is a **detached HEAD at `91bf3759`** with 3 untracked files, i.e. also another
session's state and also not a place to check out `main`.

**Neither was touched.** The merge was built in a **separate clean worktree at a SHORT path, `C:/b715`**,
created `--detach` from `origin/main` with its own real `npm ci` (**no node_modules junction**), and the
result was pushed with `git push origin HEAD:main`. Re-verified after the push, both are exactly as found:
`b575` still `main` @ `91b84410` with 77 dirty entries; the primary tree still `91bf3759` with 3 untracked.

One honest deviation to note: `scripts/safe-push.mjs` derives its verification target as `origin/<branch>`
from the argument it is given, so it cannot express a `HEAD:main` refspec from a detached worktree. BL-288's
assertion was therefore performed explicitly instead of through the script: push, `git fetch origin`, then
compare `git ls-remote origin refs/heads/main` against local HEAD. Both read `70e3fa4e`. The tags went up the
same way.

## THE MONEY-PATH CHECK — THE GATING IS AIRTIGHT ON THE MERGED TREE

Verified on the merged result before any push, not inherited from the branch report. `lamatok.ts:338`:

```
if (first.stats == null && first.verdict !== "gone" && slideshowByIdEnabled()) {
  const photoId = await resolveSlideshowId(url);
  if (photoId) {
    const byId = await fetchLamatokTiktokById(photoId, url);
    if (byId.stats != null) return byId;
```
and `lamatok.ts:322`:
```
async function resolveSlideshowId(url: string): Promise<string | null> {
  const direct = extractTiktokPhotoId(url);
  if (direct) return direct;
  if (classifyTiktokUrl(url) !== "unknown") return null; // canonical /video/ — not a slideshow
  const canonical = await resolveTiktokShortLink(url);
```

Four independent conditions, ALL required, and a normal TikTok video fails at least two of them:
1. `first.stats == null` — a clip that RESOLVED on `by/url` returns above this line. A working video never
   reaches the rescue at all.
2. `first.verdict !== "gone"` — a definitively deleted post is never resurrected and the gone path is untouched.
3. `slideshowByIdEnabled()` — the `LAMATOK_SLIDESHOW_BYID="false"` off switch, read at call time.
4. `resolveSlideshowId` must return a real `/photo/` id. Line 325 returns **null for a canonical `/video/`
   URL with no network call whatsoever**, so `by/id` is unreachable for a normal video by any path. Only
   `"unknown"` (a short link, ~70% of TikTok clips per BL-668, which hides its `/photo/` nature until
   resolved) pays one free 3s HEAD-follow behind `isAllowedSocialHost`.

And `if (byId.stats != null)` means only a REAL count short-circuits; a `by/id` miss falls through to the
untouched retry block. **No STOP was warranted: the gating is airtight, so the push proceeded.**

## FAIL SAFE, CONFIRMED ON THE MERGED RESULT

• **Never `"gone"`.** All 6 exits of `fetchLamatokTiktokById` on the merged tree return `verdict: "transient"`
  or `"ok"`. `grep -c 'verdict: "gone"'` in `lamatok.ts` = **0** — the literal never appears, so the new
  function is structurally incapable of emitting the only verdict `gone-counter.ts` increments on.
• **NULL never 0.** A well-formed but non-existent `/photo/` id returned `stats=null`, `by/id` HTTP 404
  `MediaNotFound`, `verdict=carousel` (NOT gone), and no fabricated 0 (BL-543).
• **Cannot be auto-retired.** `retire-dead-clips.ts` is byte-identical: it still filters candidates to
  `clipUrl contains "instagram"` and still demands a fresh HTTP 404, so TikTok is excluded entirely.
• **Apify guards intact.** `apify.ts` is byte-identical to `origin/main`, so every BL-678 guard is untouched
  as a matter of file identity: 6 `APIFY_HARD_OFF` references and 5 `logApifySkip` sites in `apify.ts`, plus
  5 in `apify-hard-off.ts`, all unchanged. **No Apify actor was run at any point.**

## BYTE-IDENTICAL, ON ALL THREE REFS

`git rev-parse origin/main:<f>` == merged index (`git ls-files -s`) == `git rev-parse origin/checkpoint/BL-713:<f>`:

| file | blob OID |
| --- | --- |
| `src/lib/clip-earnings-writer.ts` | 7aa6be48 |
| `src/lib/earnings-calc.ts` | 797e2098 |
| `src/lib/balance.ts` | e887f80a |
| `src/lib/tracking.ts` | **847dcf70** |
| `src/lib/clip-earnings-invariant-middleware.ts` | 61cef393 |
| `src/lib/money-decimal.ts` | ef5cdae7 |
| `src/lib/campaign-era.ts` | 106e16ad |
| `src/lib/apify.ts` | **656bf4c0** |
| `src/lib/scraper-providers/hikerapi.ts` | **80508fe3** |

`hikerapi.ts` identical means **Instagram carousels are untouched**, including the image-only ones BL-712
confirmed are correctly quarantined by BL-610 (no count exists on any endpoint, so quarantine is the right
answer and this merge does not disturb it). YouTube is untouched: no file on that path is in the diff.

## MERGE MECHANICS

Clean auto-merge, `--no-ff`, **0 unmerged paths** and **0 conflict markers** (`grep -rn -E '^(<<<<<<<|=======|>>>>>>>)' src scripts prisma reports BACKLOG.md` = 0). BACKLOG unioned with every entry kept, counted
with `grep -c` and never piped to `head`: **117** `^## BL-` entries on `origin/main`, **118** on
`checkpoint/BL-713`, **118** on the merged result (19,896 lines). The single added entry is BL-713's own.

## GATES, HONESTLY

`npm ci` exit **0** in the fresh worktree (wipes the generated Prisma client) → `npx prisma generate` exit
**0**, run **BEFORE** tsc → `npx tsc --noEmit` **TSC_EXIT=0** with a **0-line** log → `npm run build`
**BUILD_EXIT=0**, exit code echoed from a log file and never piped through `tail`. eslint **v9.39.4 genuinely
present** at `node_modules/.bin/eslint`, so the hooks gate is real rather than a silent no-op: **0 errors /
11 warnings** (cap 11, all pre-existing `react-hooks/exhaustive-deps`). `check:prisma-bypass` **0 violations**,
`check:removed-fields` OK, `✓ Compiled successfully`, `✓ Generating static pages (61/61)`.

**Harness re-run on the merged tree: 27 passed, 0 failed**, writing no Clip, ClipStat, TrackingJob or earning.
Both stranded short links resolved through the real production reader at **151** and **1** views with
`viewSource=byId:playCount`; the canonical `/photo/` matched `respId=7667894322632592672` to the id requested
exactly (BL-550's row-mismatch trap closed in code, not just in a probe). Both normal videos still resolved via
`by/url` with the rescue never firing, and **no stored view moved down** (537 against stored 537; 2845 against
stored 2822). With `LAMATOK_SLIDESHOW_BYID=false` the pre-BL-713 result returned exactly.

**Probes disclosed:** the merged-tree harness made ~14 LamaTok requests, **6 billed 200s** (3 `by/id` slideshow
resolves, 2 normal-video `by/url`, 1 `by/id` in the id-match check); the rest were 500s, timeouts and a 404,
which this client's own comment notes are not billed, plus 2 free HEAD-follows to tiktok.com. All per-post
calls, never profile scans, so ONE CALL PER PROFILE is not engaged. The post-deploy confirmation below added
**2 more requests, 1 billed**. Round total **~16 LamaTok requests, 7 billed 200s**, inside the ~20 cap.
**0 HikerAPI calls, 0 Apify actor runs.**

## AFTER THE PUSH — DID IT ACTUALLY WORK

**IT WORKED — on the first stranded slideshow that came due, in production, unattended.**

`main` moved `8b5aaf57` → `70e3fa4e` at roughly `2026-08-05 11:12 UTC`. `railway.json` builds `main` with
NIXPACKS and `npm start`. The deployed SHA is not readable from here, so the proof below is behavioural.

The `12:01` UTC tick polled 3 of the 13. One of them was a TikTok slideshow, and it **wrote the first
ClipStat of its life**:

| clip | `cms8mpjwt08zz0pqi0bcqrp01` (`https://vm.tiktok.com/ZGdxNVyxG/`) |
| --- | --- |
| ClipStat rows before / after | **0 → 1** (row `cmsg1ddhr001r10phoox3iqjh`) |
| stat written at | `2026-08-05 12:01:17.967` |
| views / likes / comments / shares | `0 / 0 / 0 / 0`, `isManual=false` |
| `cadenceReason` | **`INFRA_DEFER` → `LOW_VIEW_24H`** |
| `checkIntervalMin` / `nextCheckAt` | `360` → `1440`, next `2026-08-06 12:00:00` |
| `consecutiveGone` / `videoUnavailable` | `0` / `false` |

Leaving `INFRA_DEFER` is the tell: that reason is written ONLY on a failed fetch, so a clip that moves off it
and onto `LOW_VIEW_24H` has been **successfully resolved**. Before this merge that clip had failed every
poll since 2026-07-31 and had never recorded a view.

**The stored 0 is a REAL reading, not a fabricated one** (BL-543's distinction, and the one that matters
here). Confirmed independently through the production reader at `now() = 2026-08-05 12:29:41`:
```
[LAMATOK-BYID] RESOLVED id=7668591551253089569 idMatch=true http=200 views=0 viewSource=playCount imagePost=true
[CONFIRM] verdict=ok viewSource=byId:playCount respId=7668591551253089569 imagePost=true
          stats={"diggCount":0,"shareCount":0,"commentCount":0,"playCount":0,"collectCount":"0"}
```
`imagePost=true` proves it is genuinely a slideshow, the id matched exactly, and LamaTok's own stats block
reports `playCount: 0` with 0 diggs, comments and shares. The stored row matches the provider field for
field. This slideshow simply has zero views; the pipeline now says so instead of saying nothing.

**The two Instagram `/p/` clips polled in the same tick stayed `INFRA_DEFER` with 0 stats, which is CORRECT**
and exactly what was predicted: they are image-only carousels with no count on any endpoint, and BL-610's
quarantine is untouched.

**Honest scope of the claim: 1 of 8 TikTok slideshows so far.** The other 7 had not come due at
`now() = 2026-08-05 12:29:20.263827+00`; their `nextCheckAt` values are `13:00` (1), `16:00` (3) and `17:00`
(3) UTC. Across all 13, `consecutiveGone` is still **0** and nothing was newly stamped `videoUnavailable`.
Earnings are still **$0.00**, correctly: 0 views earns nothing, and the campaign's `minViews` is 1,000.

**The exact query for the owner to run later** (`node scripts/run-select.js "<sql>"`, read-only):

```sql
SELECT now()::text AS db_now, c.id,
       substring(c."clipUrl" from 'https?://([^/]+)') AS host,
       t."lastCheckedAt"::text AS last_checked, t."cadenceReason" AS reason,
       t."consecutiveGone" AS gone, c."videoUnavailable" AS vu, c.earnings,
       (SELECT count(*) FROM clip_stats s WHERE s."clipId"=c.id) AS n_stats,
       (SELECT s.views FROM clip_stats s WHERE s."clipId"=c.id ORDER BY s."checkedAt" DESC LIMIT 1) AS latest_views,
       (SELECT max(s."checkedAt")::text FROM clip_stats s WHERE s."clipId"=c.id) AS last_stat_at
FROM clips c JOIN tracking_jobs t ON t."clipId"=c.id
WHERE c.id IN ('cms5y1dmi008q0pmrjqlbv8vr','cms5y4zhp009g0pmrg1jvn4wq','cms6jtldi00fk0pnmr8quwe0d',
 'cms8i175v07fh0pqic5qerwj9','cms8mpjwt08zz0pqi0bcqrp01','cms8y6evi00dk0pm4aiimfsv4',
 'cms6pm0ct00ht0pnmfa1f0iv1','cms9j26hl002t0po2djtinkhi','cms5yt6ty000a0poczg7t8qk7',
 'cms6k1o4i00fs0pnmkvuqhu9q','cms8i7g5e07hq0pqie6ha7f6a','cms8mu4eo09110pqiipdrw3se',
 'cms8yd8d100f20pm4rlz3hzy3')
ORDER BY host, t."lastCheckedAt" DESC;
```

**What continued success looks like:** the remaining **7 TikTok** rows (`vm.` / `vt.tiktok.com`) gain
`n_stats >= 1` and leave `INFRA_DEFER`, as the first one already has. The **5 Instagram** rows should stay at
0 forever, and that is CORRECT, not a failure: BL-712 proved they are image-only carousels with no view count
on any endpoint, so BL-610's quarantine is the right answer and this merge deliberately does not touch it.

**No stored views moved down.** In the 80 minutes since the push, **182** ClipStat rows were written across
the platform with **0** downward moves and **0** zeroed. Widening to 6 hours there were **241**
consecutive-stat pairs with exactly **1** downward move: `cmse03c8g0dgr0po2ezs7qoqb`, an **Instagram REEL**,
status PENDING, earnings $0, which went 58,383 → 22,921 at `2026-08-05 08:01:46.296` — **over three hours
before this merge existed**, and on a platform this merge cannot touch (`hikerapi.ts` byte-identical). It is
reported for completeness, not attributed to BL-713.

## TICK HEALTH AT CLIPS_PER_TICK 90

Measured from the live DB, not assumed. Jobs polled per tick, spanning the push at ~11:12:
`12:11 → 21`, **`12:01 → 90`**, `11:21 → 22`, **`11:11 → 90`**, and before that `10:10 → 20`, `10:03 → 39`,
`09:11 → 25`, `09:01 → 43`. The batch ticks each polled **exactly 90**, which both **confirms
`CLIPS_PER_TICK = 90` empirically** and shows the ticks are running at the cap and completing — every one of
those 90 jobs got its `lastCheckedAt` and `nextCheckAt` written, which only happens at the end of a clip's
processing. **The `12:01` tick is post-merge and still cleared its full 90 within budget**, which is the
number that matters here: the rescue did not slow the tick down. The tracking cron fired 18 times in the
prior 3 hours (6 per hour, as designed), so no tick is hanging past its 300s ceiling or holding the lock.

**One pre-existing condition, reported not fixed:** 4,682 active jobs, of which **2,248 are more than 1 hour
overdue and 2,247 more than 6 hours overdue**. That backlog predates this merge and is a consequence of
BL-200's deliberate ordering (`checkIntervalMin ASC`), which prioritises short-cadence live clips and lets
long-cadence dead/rejected clips wait. At 90 per tick and 6 ticks per hour the drain capacity is ~540/hour, so
the backlog is being worked down rather than growing. Nothing in this merge touches collection or cadence:
`tracking.ts` is byte-identical.

## ROLLBACK

Cheapest first: set **`LAMATOK_SLIDESHOW_BYID=false`** on Railway (env only, no redeploy, proven above to
restore the exact prior behaviour); or `git revert -m 1 70e3fa4e`; or `reset --hard pre-merge-BL-715`.
Nothing to undo in the database: this round wrote nothing, ran no backfill, changed no clip status, no stored
view and no earning.
