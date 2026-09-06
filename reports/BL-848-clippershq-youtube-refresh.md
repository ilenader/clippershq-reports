# BL-848 — the 338 YouTube clips BL-846 could not reach

Round of 2026-09-06. Branch `checkpoint/BL-848`, base `da3eb5fb`, worktree `C:/w848`.

**The key works.** `YOUTUBE_API_KEY` is present in `.env.local` (39 characters) and returned real
statistics for 3 of 3 probed clips through the repo's own client. **222 of the 338 clips are refreshed,
+7,128 views found, $0.00 spent, and 0 of the 3,860 clip rows in scope were written.** Every money, status
and payout fingerprint is **byte-identical**.

## PART 0 — the key, the population, the quota

**The key was tested rather than assumed present.** BL-846 failed precisely because presence was never the
question: that round had no key at all and every clip came back null. So this probe called the production
path, `fetchYouTubeStatsBatch`, on three real clips from the population:

```
  YOUTUBE_API_KEY present: YES  (AIzaSy…, 39 chars)
    cmohwql0n0  stored     29,829  api      29831  likes 870 comments 8 shares 0
    cmp2fdf5m0  stored     29,593  api      29814  likes 324 comments 12 shares 0
    cmp3s9q980  stored     27,314  api      29703  likes 287 comments 34 shares 0
  KEY WORKS: 3 of 3 probed clips returned real statistics.
```

All three had grown, which is the point of the round.

**The population, re-derived today with the same 50-view floor BL-846 used:**

| status | YouTube clips | 50+ views | fetch set |
|---|---|---|---|
| PAST | 703 | 338 | **338** |
| COMPLETED | 0 | 0 | 0 |
| **TOTAL** | **703** | **338** | **338** |

It matches BL-846 exactly. Every YouTube clip on a finished campaign sits on a **PAST** campaign, not a
COMPLETED one, which is what BL-838 observed independently. 365 clips fall under the 50-view floor and were
never fetched. None of the 338 was already marked unavailable or deleted.

**Quota, stated rather than assumed.** `videos.list` costs **1 unit per request** regardless of how many ids
it carries, up to the 50-id maximum. So 338 clips is **7 requests, 7 units**, against a default allowance of
10,000 units a day: **0.07 percent of one day, and $0.00 in money.** The Data API has no per-call charge.
This fits comfortably and would still fit if the population were a hundred times larger.

## PART 1 — nothing could earn, proven on one clip first

**BL-844's freeze is live on this base:** `tracking.ts:2004` carries `freshCampaign?.status === "COMPLETED"`
as an arm of `campaignStatusBlocks`, alongside PAST, `isArchived` and the auto-pause arm.

**But as in BL-846 that is the second line of defence, not the first.** This run never enters `tracking.ts`.
It writes ONE `clip_stats` row per clip and issues **no `clip.update` whatsoever**, so `earnings`,
`baseEarnings`, `bonusAmount`, `status` and `videoUnavailable` are unreachable by construction. It never
calls `writeClipEarnings`, imports nothing from the six money files, and the L2 invariant middleware engages
only when one of the three invariant fields appears in a payload, which a `clipStat.create` never carries.

**The single-clip proof, before the other 337:**

| fingerprint | before | after |
|---|---|---|
| `clip_fp` (earnings, status, availability, all clips) | `3f04ab38…` | **SAME** |
| `clip_status_fp` | `e755e5ae…` | **SAME** |
| `payout_fp` | `346bb94e…` | **SAME** |
| `per_clipper_fp` | `711448cf…` | **SAME** |
| `campaign_spend_fp` | `89c33c19…` | **SAME** |
| `unavailable_clips` | 1,406 | **1,406** |
| `invariant_violations` | 0 | **0** |
| `money_out` | $7,003.89 | **unchanged** |

Only the three fields a stat refresh should move did. **Forbidden fields moved: 0.** Only then did the rest
run.

## PART 2 — YouTube's quirks respected

**Shares recorded ABSENT, never 0, on every single row.** BL-753 and BL-819 established the Data API v3
statistics resource carries **no share field at all** and that 0 of 61,400 stored YouTube snapshots ever held
one. The write shape is `shares: 0` with `sharesSource: NULL`, which is exactly what `youtube.ts:261`
already does: the NULL source is what carries the meaning. Measured on the rows written: **222 of 222 have
`sharesSource NULL` and 0 carry a non-zero share count.** Nothing was invented.

**BL-753's fix at `youtube.ts:178` is live, and I confirmed WHICH function I am on.** There are two readers
and only one is fixed:

- `fetchYouTubeStatsBatch` (line 141) — **the path this round uses.** BL-753 changed it to map the **whole
  entry** to `null` when YouTube omits `statistics.viewCount`, which it does as documented behaviour when an
  uploader hides the count. A null entry produces **NO ROW** here, so the clip keeps its last known value.
- `getYouTubeVideoDetails` (line 78, fabricating at line 119 with `parseInt(item.statistics?.viewCount ||
  '0', 10)`) — **still fabricates, deliberately**, and is not on this path.

**Absent stayed absent: 116 clips got no row**, and **0 rows were written with `views = 0`.** A row that
does not exist cannot be misread, which is stronger than a nullable column.

**A decrease was permitted because BL-753 proved decreases are real** — that round measured 1,245 legitimate
decreases across 650 clips and a never-decrease floor was correctly rejected, because freezing an inflated
figure means permanently paying CPM on views that no longer exist. This run saw **exactly one decrease, of
−1 view**, and wrote it. The guard against the failed-read signature, BL-753's own unbuilt recommendation to
refuse `views = 0` over a positive last value, **fired 0 times**.

**NO CLIP'S STATUS OR AVAILABILITY CHANGED.** 116 videos returned no statistics, which is what a deleted,
private or banned video looks like as well as a hidden view count, and **not one was marked unavailable.**
`videoUnavailable` is **1,406 before and 1,406 after.** BL-720 narrowed the gone verdict to two named paths
in `retire-dead-clips.ts` and nothing here touches that file or those columns, because a video unreachable
to a fetcher is not a video that does not exist and BL-818 established that such a mark removes money from a
clipper's displayed balance.

**Resumable.** One JSONL line per clip is appended to `C:/bl848/progress.jsonl` **synchronously the moment
the clip finishes and before the next batch starts**, so a kill at any point leaves a complete record. A
resumed run reads that file and skips every id in it. It proved itself: the run opened with `338 in scope, 1
already recorded, 337 to do`, correctly skipping the PART 1 clip. Across both rounds the ledger held:
**every refreshed clip has exactly one new row and not one was written twice.**

## PART 3 — nothing moved that should not

| claim | measurement |
|---|---|
| clip rows in scope written | **0 of 3,860** (`updatedAt` newer than the run start) |
| payouts created, modified, approved or cancelled | **0** |
| clips marked unavailable | **0** (1,406 before and after) |
| earnings invariant violations | **0** |
| `clip_fp`, `clip_status_fp`, `agency_fp`, `per_clipper_fp`, `campaign_spend_fp` | **all five byte-identical** |
| `payout_fp`, `money_out`, `double_open` | **identical** |

This is a cleaner result than BL-846, which had five platform fingerprints move and had to attribute all of
them to 164 clips the live cron and reviewers touched on ACTIVE campaigns during a 19-minute window. This
run took about 30 seconds, and no concurrent activity landed inside it, so **every forbidden fingerprint is
identical without needing attribution at all.**

## PART 4 — what the owner asked for

**Of the 338: 222 refreshed, 116 could not be.**

| | clips | views before | views after | growth |
|---|---|---|---|---|
| somesome | 78 | 360,278 | 364,525 | **+4,247** |
| GainzAlgo (REPOST CAMPAIGN) | 144 | 131,084 | 133,965 | **+2,881** |
| **TOTAL** | **222** | **491,362** | **498,490** | **+7,128** |

The 116 all failed for one reason: **`null_entry_no_statistics`** — YouTube returned no statistics object.
That is a deleted, private or banned video, or a video whose uploader has hidden the view count. The API
cannot tell those apart, which is exactly why none was marked gone. **Their old numbers are now the best
available and they will stay that way.**

**The biggest growers, handles redacted:**

| clip | clipper | campaign | before | after | growth |
|---|---|---|---|---|---|
| cmp3s9q980 | cmoy0ap2 | somesome | 27,314 | 29,703 | **+2,389** |
| cmpip0yjx0 | cmpiojy1 | GainzAlgo (REPOST) | 180 | 1,665 | **+1,485** (9.25x) |
| cmrgmlrop0 | cmoobbld | GainzAlgo (REPOST) | 13,975 | 14,898 | +923 |
| cmoyh28yc0 | cmoy0ap2 | somesome | 22,324 | 22,833 | +509 |
| cmp2fdf5m0 | cmoy0ap2 | somesome | 29,593 | 29,814 | +221 |
| cmp7xgkqh0 | cmp6xvap | somesome | 1,588 | 1,764 | +176 |

**Honest scale note: YouTube is small here.** The biggest jump is +2,389 views against BL-846's +618,789 on
Instagram. These are Shorts that have largely gone quiet, averaging about 32 additional views each over the
25 days since their last snapshot on 2026-08-12. The one genuinely interesting row is `cmpip0yjx0`, which
went **180 to 1,665, a 9.25x rise** after the campaign closed.

### The complete picture across all three platforms

| platform | clips refreshed | round |
|---|---|---|
| Instagram | 886 | BL-846 |
| TikTok | 762 | BL-846 |
| YouTube | 222 | BL-848 |
| **TOTAL** | **1,870** | |

**Total views across every finished campaign: 55,979,673 → 58,188,458, up 2,208,785.** Total spent across
both rounds: **$1.5305** — $0.9088 HikerAPI, $0.6217 LamaTok, $0.00 YouTube.

**And the whole scope reconciles exactly**, 1,870 + 669 + 728 + 593 = 3,860:

| outcome | clips | why |
|---|---|---|
| **refreshed** | **1,870** | |
| never fetched, under the 50-view floor | 669 | the owner's own filter |
| never fetched, already marked gone or deleted | 728 | a Hiker 404 costs two calls to learn nothing |
| fetched but no usable answer | 593 | 258 TikTok MediaNotFound, 203 Instagram unclassifiable, 116 YouTube null, 9 timeouts, 3 private, 3 LamaTok 500, 1 malformed URL |

## PART 5 — the standing gap, stated and NOT changed

The cron **does** exclude PAST campaigns: the due-jobs `where` at `tracking.ts:3691` carries
`status: { notIn: ["PAST","PAUSED","COMPLETED","DRAFT"] }`, so nothing on a finished campaign is ever
polled. **These 222 clips will go stale again the moment they keep growing.** Nothing in this round changes
that, as instructed.

**My position: the exclusion is correct for money and wrong for the owner's stated purpose, and the fix is
not the cron.**

- **Correct for money.** Earnings on these campaigns are frozen, so polling buys no accuracy in any figure
  anyone is paid on. Turning the cron loose on 2,463 finished clips would add a permanent recurring vendor
  bill for numbers that can never change a payout.
- **Wrong for the purpose.** The owner wants true historical numbers, which is why both of these rounds
  exist, and a clip that goes viral after a campaign closes is otherwise invisible forever. `cmpip0yjx0`
  rising 9.25x is precisely the case that would never have surfaced.
- **The resolution already exists and it is these two scripts.** A full pass costs **$1.53 measured**, so an
  on-request or quarterly run gives him true numbers with no permanent commitment and no change to the money
  path. For comparison, BL-838 measured the current live tracking bill at **$146.73 a month**.

**What each cadence would cost, if he ever wants it recurring:** weekly **$6.63 a month** (4.5 percent of
the current bill), monthly **$1.53**, quarterly **$0.51**. YouTube is free at every cadence, so a
YouTube-only refresh is **$0.00 however often it runs** — that one could reasonably be scheduled without
any cost argument at all.

## Safety

**No source file was modified.** This round adds two scripts and this report, and carries BL-846's four
scripts and its record forward by merging `checkpoint/BL-846`, which had never been merged and would
otherwise have been lost. The 6 money files plus `tracking.ts`, `campaign-era.ts`, `payout-calc.ts`,
`apify.ts` and `prisma/schema.prisma` are **byte-identical by blob OID on both refs**. No schema change, no
`prisma migrate`, **no Apify actor run**, the 11 BL-678 guards untouched, 0 Supabase pool errors, no wallet
address read, every timestamp cast to `::text` against the database's own `now()`.

**The database pool was never stressed.** One Prisma client, one query for the whole work list, then batched
reads of 50 and one single-row create per clip, so DB concurrency never exceeded 1. BL-825 once cost the real
owner four failed reads by exhausting it.

**One BACKLOG conflict, resolved as a UNION.** Merging BL-846 collided with BL-845 at the end of
`BACKLOG.md`; both entries are kept in round order and neither side was dropped. Counted with `grep -c`:
main held **178**, BL-846's branch also held 178 (the same count, different last entry, which is exactly why
they conflicted), the union produced **179**, and this round's own entry makes **180**.

**Disclosed: a peer round is live.** `checkpoint/BL-847` holds a worktree at `C:/w847` on the same base. This
round touched no file it could plausibly want and never left its own worktree.

**No UI was touched**, so no accessibility review was warranted: this round adds scripts and a report and
changes no component, page or copy.

**No redeploy required.** No shipped code changed.

**Rollback:** the 222 `clip_stats` rows are additive history and nothing reads them as money.
`DELETE FROM clip_stats WHERE "isManual" = true AND "checkedAt" >= '2026-09-06 21:02:00';` restores the
older, staler figures, which is almost certainly not what anybody wants.
