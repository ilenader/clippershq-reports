# BL-846 — one authoritative stat refresh for every clip on a finished campaign

Round of 2026-09-06. Branch `checkpoint/BL-846`, base `cfa80cb2`, worktree `C:/w846`.

**Headline: 1,648 clips refreshed, +2,201,657 views discovered, $1.53 spent, and not one clip row, one
earning, one balance, one status or one payout moved.** The database's own `updatedAt` is the witness: **0
of the 3,860 clip rows in scope were written.**

## Two premises in the brief are corrected before anything else

**1. There is no "tag resolve plus a medias call" in ClippersHQ.** The brief attributes that pattern to
BL-838. It is `/v2/hashtag/medias/clips` and it belongs to a **different project's** report that shares the
bare number `BL-732.md` in the shared reports repo. ClippersHQ tracking never resolves a tag; it looks up
one post by URL. There is no tag-resolve leg in this cost.

**2. `hikerapi.ts:603` and `youtube.ts:178` are already fixed.** The brief lists them as live fabricated
zeros. BL-748 shipped `?? 0` → `?? null` at the first and BL-782 re-verified 0 occurrences on main; BL-753
fixed the second by mapping the whole entry to `null`. What still fabricates is named at the end of this
report.

## PART 0 — counted and costed before a cent was spent

| status | platform | clips | 50+ views | already gone | **fetch set** |
|---|---|---|---|---|---|
| COMPLETED | Instagram | 31 | 29 | 2 | |
| COMPLETED | TikTok | 131 | 119 | 0 | |
| PAST | Instagram | 1,959 | 1,776 | 824 | |
| PAST | TikTok | 1,036 | 929 | 0 | |
| PAST | YouTube | 703 | 338 | 0 | |
| **TOTAL** | | **3,860** | **3,191** | 826 | **2,463** |

The owner estimated roughly 5,000 clips; the true figure before the filter is **3,860**, and **3,191** hold
50 or more views. The fetch set is **2,463** after also skipping the 826 posts already marked gone, because
BL-838 measured that a Hiker 404 costs **two** calls, so re-probing known-dead posts is the most expensive
way to learn nothing.

**Calls per clip, read from the clients rather than assumed:**

- **Instagram / HikerAPI** — `fetchHikerInstagramByUrl` probes `/v2/media/info/by/code` and, **on a 404
  only**, makes a second call to `/v2/media/info/by/url`. So **1 call live, 2 on a 404.** No backoff and no
  repeat: BL-838's words are "a call that 404s costs exactly 2, never 5." The result carries `via`, so this
  sweep **reads** the count rather than estimating it.
- **TikTok / LamaTok** — `fetchLamatokTiktokByUrl` is a three-stage chain: `by/url`, then BL-713's
  slideshow rescue via `by/id` only when stats are null and the post is not declared gone, then one retry
  on a 5xx or network failure. **1 call on the happy path, 3 worst case**, plus a free HEAD to tiktok.com
  which is not a billed vendor call.
- **YouTube / Google Data API v3** — **$0.00.** No paid vendor, `part=statistics`, batched 50 ids per
  `videos.list`, so 338 clips is 7 requests.

**Cost at BL-838's MEASURED rates, not the repo's constant.** HikerAPI **$0.00069214** and LamaTok
**$0.00060007**, each derived from that vendor's own `GET /sys/balance`. The repo's
`apify-ledger.ts:214` holds `0.001` for Hiker, which is **44.5 percent high** — confirmed independently
here, since 0.001 ÷ 0.00069214 = 1.4448.

```
  Instagram   1089 clips  1 call each = $0.7537   worst case 2 each = $1.5075
  TikTok      1036 clips  1 call each = $0.6217   worst case 3 each = $1.8650
  YouTube      338 clips     7 batched calls      $0.0000   free quota
  EXPECTED TOTAL    $1.3754
  WORST CASE TOTAL  $3.3725      gate is roughly $20 — CLEAR, proceed
```

## PART 1 — nothing could earn, proven on one clip before the sweep

BL-844's fix **is live on current main**: `campaignStatusBlocks` at `tracking.ts:1999-2004` now carries
`freshCampaign?.status === "COMPLETED"` alongside `PAST`, `isArchived` and the auto-pause arm. Every
campaign in scope is therefore frozen for both the cron and a manual run.

**But the freeze is the second line of defence here, not the first.** This sweep never enters `tracking.ts`
at all. It writes ONE `clip_stats` row per clip and issues **no `clip.update` whatsoever**, so `earnings`,
`baseEarnings`, `bonusAmount`, `status`, `videoUnavailable` and every other Clip column are unreachable by
construction. It imports nothing from the six money files and never calls `writeClipEarnings`. The L2
invariant middleware engages only when one of the three invariant fields appears in a write payload, and a
`clipStat.create` never contains one.

**The single-clip proof, on the largest clip in scope.** Clip `cmoback380` (Instagram, somesome) rose
**12,139,743 → 12,758,532, a jump of +618,789 views on a settled clip** — precisely the risk case.

| fingerprint | before | after |
|---|---|---|
| `clip_fp` (earnings, status, availability, all clips) | `717e6407…` | **`717e6407…` SAME** |
| `payout_fp` | `346bb94e…` | **SAME** |
| `per_clipper_fp` (approved earnings per clipper) | `e1badac9…` | **SAME** |
| `campaign_spend_fp` | `0bef0bab…` | **SAME** |
| `invariant_violations` | 0 | **0** |
| `money_out` | $7,003.89 | **unchanged** |

Only three things moved, and all three are what a stat refresh is supposed to move: `clip_stats_rows`
345,539 → 345,540, `manual_stat_rows` 418 → 419, and total views +618,789. **Money fields moved: 0.** The
sweep was cleared to proceed.

## PART 2 — how it ran

**Concurrency: Instagram 8, TikTok 5, YouTube batched 50.** Both vendors report `rate: 15` in their own
balance payload, which is the requests-per-second ceiling, and the repo's own semaphore sits exactly there
(`HIKER_GLOBAL_CONCURRENCY = 15`, `apify.ts:1467`). This sweep ran **deliberately below the cap** because
the live tracking cron is calling Hiker at the same time, measured by BL-838 at 274.5 calls an hour. Taking
the whole ceiling would starve the cron that serves live campaigns in order to speed up a historical
backfill. **Zero profile calls were made** — every lookup is a single media-by-URL call.

**The database pool was never stressed.** BL-825 caused four failed reads for the real owner by exhausting
it. This sweep opens one Prisma client, reads its entire work list in **one** query up front, and then
performs a single-row `clipStat.create` per clip, so DB concurrency never exceeds the fetch concurrency of
8. **0 pool errors.**

**Resumable, and it cannot double-charge.** Every clip appends one JSONL line to `C:/bl846/progress.jsonl`
**synchronously, the instant it finishes and before the next call starts**, so a kill at any moment leaves a
complete record of what was already paid for. A resumed run reads that file and skips every id in it. The
sweep proved this in practice: it began with `2463 in scope, 1 already recorded, 2462 to do`, correctly
skipping the PART 1 clip.

**Skipping was done in the SQL, so a skipped clip never costs a call:** under 50 views, `videoUnavailable`,
and `isDeleted` are all excluded in the `WHERE`.

## PART 3 — written honestly

**Absent is absent and never 0, in the strongest available form: no row at all.** When a provider returned
no usable view count this sweep wrote **nothing** for that clip. A row that does not exist cannot be
misread, which is stronger than a nullable column. 815 clips got no row.

**Instagram shares came through all three of BL-820's loss points, proven end to end.** The very first clip
returned `shares 126298, sharesSource reshare_count`. Across the sweep: **489 Instagram rows measured with
`reshare_count` and 397 honestly ABSENT** (`sharesSource NULL`), 173,563 shares in total. If any of the
three loss points were still hardcoding `0` — the classifier, the overlay, or the decisive one at
`apify.ts:1607` — the measured count would be 0.

**YouTube shares recorded ABSENT, never zero.** Per BL-753 the Data API v3 statistics resource has no share
field and 0 of 61,400 stored YouTube snapshots ever held one. The write shape is `shares: 0` with
`sharesSource: NULL`, which is exactly what `youtube.ts:261` already does: the NULL source is what carries
the meaning.

| platform | rows | shares measured | shares ABSENT | total shares |
|---|---|---|---|---|
| Instagram | 886 | 489 | 397 | 173,563 |
| TikTok | 762 | 762 | 0 | 44,786 |

**Decreases are permitted, because BL-753 proved they are real.** That round measured **1,245 legitimate
decreases across 650 clips**, including a 723,110-view Instagram correction, and a never-decrease floor was
correctly rejected because freezing an inflated figure means permanently paying CPM on views that no longer
exist. This sweep therefore writes a genuine decrease. It saw exactly **one**, of **−1 view**.

**One guard was added, and it is BL-753's own recommendation which that round specced and did not build:**
refuse to write `views = 0` over a clip whose last stored value was greater than 0. BL-753's census showed
the discriminator is the **destination, not the direction** — real corrections land above zero at an 8.9 to
49.2 percent average fall, while fabrications land on exactly 0 from a positive value. **It fired 0 times**,
which is the right outcome and not a wasted guard: it is the difference between a failed read and a real
reading, and it cost nothing to be certain.

**NO CLIP'S STATUS OR AVAILABILITY CHANGED, AT ALL.** BL-720 narrowed the gone verdict to two named paths
in `retire-dead-clips.ts`, and nothing here touches that file or those columns. **258 TikTok posts returned
a hard `MediaNotFound` 404 and 3 returned `PrivateAccount`, and not one was marked gone** — because BL-720's
principle is that a video unreachable to a fetcher is not a video that does not exist, and a private
account's post is visible to every follower. `videoUnavailable` count: **1,406 before, 1,406 after.**

## PART 4 — what moved, and what did not

**The load-bearing proof, from the database's own witness:**

| claim | measurement |
|---|---|
| clip rows in scope written | **0 of 3,860** (`updatedAt` newer than the sweep start) |
| payouts created, modified, approved or cancelled | **0** |
| clips marked unavailable | **0** (1,406 before and after) |
| earnings invariant violations | **0** |
| `payout_fp` | **byte-identical** |
| `money_out` | **$7,003.89, unchanged** |

**Five platform-wide fingerprints DID move, and every one is attributed rather than waved at.** `clip_fp`,
`clip_status_fp`, `agency_fp`, `per_clipper_fp` and `campaign_spend_fp` all changed over the 19-minute
window. The cause is measured: **164 clips were updated in that window and every single one is on an ACTIVE
campaign** — the live tracking cron crediting earnings and reviewers approving clips, which is their job.
**Zero were on a COMPLETED or PAST campaign.** The single-clip proof had already established that a
`clipStat` write alone leaves `clip_fp` untouched, so the movement cannot be this sweep's.

**What this sweep did change:** 1,648 `clip_stats` rows written, all `isManual: true`. That flag is
deliberate: `tracking.ts` compares cadence and velocity over `isManual: false` rows only (`:432`, `:529`,
`:729`, `:973`, `:1126`) and `earnings-by-day-projection.ts` does the same, so a one-off owner sweep marked
false would be read as a cron cadence reading and would perturb the auto-ladder and the day projection.

**Real spend against the estimate.** Counted: **1,313 Hiker calls ($0.9088) and 1,036 LamaTok calls
($0.6217) = $1.5305**, against a PART 0 estimate of $1.3754 and a worst case of $3.3725. The overshoot is
Instagram 404s costing their documented second call. YouTube cost **$0.00**.

**And an empirical answer to a question BL-838 explicitly left unverified.** BL-838 flagged "whether a
failed call is billed" as an unverified assertion its retry design depends on. Reading LamaTok's own meter
across a bracketed window of roughly 936 TikTok attempts showed **860 billed requests** — fewer requests
than attempts, by close to the 404 count. That is consistent with failed LamaTok calls **not** being
billed. Stated as an observation with its limits, not a proof: I have no pre-Instagram baseline, so
HikerAPI's 404 billing remains open.

## PART 5 — the owner's actual question: true historical numbers

| status | refreshed / clips | views before | views after | difference |
|---|---|---|---|---|
| PAST | 220 / 953 | 28,425,798 | 29,535,803 | **+1,110,005** |
| PAST | 475 / 618 | 4,600,498 | 5,162,131 | **+561,633** |
| PAST | 567 / 909 | 4,928,902 | 5,352,943 | **+424,041** |
| PAST | 117 / 179 | 5,823,791 | 5,926,312 | **+102,521** |
| PAST | 164 / 1,039 | 11,764,109 | 11,767,273 | +3,164 |
| COMPLETED | 61 / 92 | 359,806 | 360,060 | +254 |
| COMPLETED | 44 / 70 | 76,769 | 76,808 | +39 |
| **TOTAL** | **1,648 / 3,860** | **55,979,673** | **58,181,330** | **+2,201,657** |

In campaign order those rows are somesome, Panic Baby, bees.n.honey, STRAENGE, GainzAlgo (REPOST CAMPAIGN),
BAD BITCH ANTHEM (0.50 CPM) and BAD BITCH ANTHEM (2.50 CPM).

**Yes, things quietly went viral. The twelve biggest growers, handles redacted:**

| clip | clipper | platform | before | after | growth | campaign |
|---|---|---|---|---|---|---|
| cmoback380 | cmoafodb | Instagram | 12,139,743 | 12,758,532 | **+618,789** | somesome |
| cmpgrurxc0 | cmoyq9m9 | Instagram | 1,984,334 | 2,451,120 | **+466,786** | somesome |
| cmschqo9h0 | cmrl046b | Instagram | 63,580 | 246,336 | **+182,756** | bees.n.honey |
| cms9bkzj00 | cmrl046b | Instagram | 49,042 | 166,615 | +117,573 | bees.n.honey |
| cms19nrds0 | cmryam5j | Instagram | 110,035 | 226,255 | +116,220 | Panic Baby |
| cms8smpun0 | cmqez5c2 | TikTok | 320,900 | 417,200 | +96,300 | Panic Baby |
| cmseu58da0 | cmrl046b | Instagram | 8,869 | 95,706 | **+86,837** | bees.n.honey |
| cms2c90fk0 | cmn4nlfg | Instagram | 180,944 | 235,670 | +54,726 | Panic Baby |
| cmr0bj5y30 | cmqez5c2 | TikTok | 201,800 | 251,500 | +49,700 | STRAENGE |
| cms7wq3dk0 | cmr0gixm | Instagram | 259,306 | 290,707 | +31,401 | Panic Baby |
| cms2iisc80 | cmryam5j | Instagram | 69,458 | 96,609 | +27,151 | Panic Baby |
| cms4xxqly0 | cmqgqnw4 | Instagram | 102,030 | 118,674 | +16,644 | Panic Baby |

One clipper, `cmrl046b`, holds three of the top seven on bees.n.honey, including a clip that went from 8,869
to 95,706 — a **10.8x** rise after the campaign finished.

### 815 clips could not be refreshed, and the reasons are not equal

| count | reason | are the old numbers now the best available? |
|---|---|---|
| **338** | **`yt_null` — `YOUTUBE_API_KEY` is not in the environment** | **No. This third of the sweep did not happen.** |
| 258 | TikTok `MediaNotFound` 404 | Yes. Genuinely gone; not marked gone, per BL-720 |
| 203 | Instagram answered but the classifier found no view count | Yes, and their last real reading stands |
| 9 | timeout | Yes; a resumed run would retry these |
| 3 | `PrivateAccount` 403 | Yes. The post exists and its followers can see it |
| 3 | LamaTok 500 | Yes; transient |
| 1 | not a media URL | Yes; the stored URL is malformed |

**The YouTube failure is mine to disclose plainly rather than count as 338 unreachable videos.** `.env.local`
and `.env` contain **zero** occurrences of `YOUTUBE_API_KEY`, and `fetchYouTubeStatsBatch` logs
"YOUTUBE_API_KEY not set" and marks every clip null — it did so exactly **7 times**, once per batch of 50.
The key evidently lives only in Railway. **Two consequences the owner needs:** those 338 clips still carry
their old numbers, whose newest snapshot BL-838 dated to 2026-08-12; and the tracking cron will **never**
refresh them either, because the due-jobs sweep excludes PAST campaigns. Supplying `YOUTUBE_API_KEY`
locally and re-running `npx tsx scripts/bl846-refresh.ts run` would finish them at **$0.00**, and the
resumable ledger means the 1,648 already done are not re-fetched or re-billed.

## Still fabricating, reported not changed

Two sites survive and neither is in this sweep's path: `youtube.ts:86` (`getYouTubeVideoDetails`)
deliberately still fabricates a 0 on the freshness path, and `owner-submit-core.ts:193` plus its
unconditional write at `:291` still do, on a route unused since 2026-07-26 which BL-782 measured writing a
first stat of 0 views for 12 of 35 owner-submitted Instagram clips that all later read 1,000+. Also
structural: `ClipStat.likes` and `ClipStat.comments` are `Int NOT NULL DEFAULT 0` with **no source column**,
so unlike `views` and `shares` they still cannot distinguish absent from a real zero. This sweep writes
what the provider returned and cannot fix that.

## Safety

**No source file was modified.** `git status` shows zero tracked source changes; this round adds four
scripts and this report. The 6 money files plus `tracking.ts`, `campaign-era.ts`, `payout-calc.ts`,
`apify.ts` and `prisma/schema.prisma` are **byte-identical by blob OID** against the branch base. No schema
change, no `prisma migrate`, **no Apify actor run**, the 11 BL-678 guards untouched, 0 Supabase pool errors,
no wallet address read, every timestamp cast to `::text` against the database's own `now()`.

**Disclosed: this round did not run alone.** A peer session merged BL-845 to main mid-round, advancing it
from `cfa80cb2` to `da3eb5fb` and changing `prisma/schema.prisma` there. My worktree is unmodified against
its own base, so the schema difference is that peer's and not mine. The live tracking cron also ran
throughout, which is the attributed cause of the five moved platform fingerprints.

**No UI was touched**, so no accessibility review was warranted: the round adds scripts and a report and
changes no component, page or copy.
