# BL-749 — the zero-stat clips: who they are, why, and what they actually cost
**Audited at** `6ed3a50c` · 2026-08-09 · **READ ONLY.** Nothing backfilled, rescheduled or written; no TrackingJob
touched. No Apify actor run; the 11 BL-678 guards untouched. **11 HikerAPI calls disclosed, ~$0.011**, cap 25.
Kept clear of `hikerapi.ts`, which BL-748 holds.
## ONE LINE VERDICT
**Of 52 zero-stat clips only 21 are APPROVED, 10 of those self-heal within the hour, the other 11 are genuinely
unresolvable (deleted posts and image-only carousels with no view count in existence), the estimated money at stake
is roughly $10 to $25, and the backoff does NOT need fixing because it is already capped — so I recommend AGAINST a
manual backfill.**
## The finding that reframes everything: the population is CLOSED
BL-746 merged at `2026-08-09 14:42:28Z`. It deployed **between `15:10:57Z` and `15:38:10Z`**, and it works:
```
2026-08-09 15:10:57  ZERO STATS   <-- last clip on the old code
2026-08-09 15:38:10  delay 0s     <-- first clip on the new code
2026-08-09 15:40:39  delay 0s
2026-08-09 15:43:50  delay 0s
```
Every Instagram clip submitted since is getting its stat **at submit**. The population stopped growing at
`15:10:57Z`. It is a finite historical backlog, not a leak.
**Today's figure is 52, not 41.** It grew from BL-745's 41 because the deploy landed hours after that measurement,
not because the problem worsened.
## PART 1 — Who they are
| Group | Clips | INFRA_DEFER | Money at stake |
|---|---|---|---|
| **APPROVED, `/reel/`** | **13** | 0 | 10 self-heal today; 3 are deleted posts |
| **APPROVED, `/p/`** | **7** | 6 | Image-only carousels: no view count exists |
| **APPROVED, TikTok** | **1** | 1 | Not probed, see gaps |
| REJECTED | 28 | 0 | **None.** A rejected clip earns nothing regardless |
| PENDING | 3 | 0 | None yet |
**They are not one cause.** They cluster into three, and the clustering is what makes the answer actionable:
**Cluster A, 10 APPROVED reels submitted today between 14:42 and 15:10**, all `nextCheckAt 16:00`, interval 60, no
INFRA_DEFER. These are **not stuck at all**. They are in the ordinary 30-to-90-minute window before a clip's first
tick, and BL-746's deploy landed minutes too late for them. They will have stats at the 16:00 tick.
**Cluster B, 3 APPROVED reels genuinely old** (12.0, 7.2 and 6.6 days), on Panic Baby (PAUSED) and bees.n.honey
(PAST). Their `nextCheckAt` is in the **past** (`2026-07-29`, `2026-08-03`) and has not been honoured, because the
tick does not poll clips on PAUSED or PAST campaigns. **Their stranding has nothing to do with INFRA_DEFER.**
**Cluster C, 7 APPROVED `/p/` posts on SomeSome (PAUSED)**, 6 carrying INFRA_DEFER at 360 min, stuck 10 to 11 days.
**Per-clipper exposure on APPROVED clips (9 clippers):** `70aa2a` 5 clips / 11.2 days, `d378b5` 4 / today,
`299618` 3 / today, `143d15` 2 / today, `a92aea` 2 / 12.0 days, `f191a2` 2 / 4.1 days, `62cdaa` 1 / 6.6 days,
`7d87a2` 1 / 10.7 days, `e047e1` 1 / today.
## PART 2 — Why they are stuck, and the hypothesised defect that does NOT exist
**INFRA_DEFER is `tracking.ts:1499-1518`.** It fires when a tick's failure classifies as `infra`. It deliberately
does **not** increment `consecutiveFailures`, never reaches the 72h dead-link rung and never bells the owner.
**The backoff is BOUNDED, and the brief's hypothesis is disproven.** `tracking.ts:1502`:
```ts
const backoffBase = !prevInfraDefer ? 60 : (curInterval < 180 ? 180 : 360);
```
It escalates **60 → 180 → 360 minutes and caps there**. It never backs off to effectively never; a clip retries
every 6 hours indefinitely, and the next success recomputes normal cadence. **There is no unbounded-backoff defect
to fix.** The longer intervals visible in the data (2880, 7200) come from `resolveFailureCadence` applying campaign
and clip status, and a 7200-minute cadence on a **REJECTED** clip is correct, not a bug.
**So why are they stuck? Three different reasons, established per clip rather than assumed:**
| Cluster | Real cause |
|---|---|
| A | **Nothing is wrong.** Pre-first-tick window; BL-746 arrived minutes late |
| B | **The campaign is PAUSED or PAST**, so the tick does not poll them. Not INFRA_DEFER |
| C | **The provider legitimately has no count to give** (see PART 3) |
## PART 3 — Are they fetchable now? Probed, and the answer differs by cluster
Eleven calls, every one matched by **id, never by row** (the BL-550 trap): the probe prints the requested shortcode
against the returned one, so a response for a different post is visible rather than assumed.
**Cluster A, 5 recent reels — ALL RECOVERABLE:**
```
[6d74db] ID-MATCH views=243  viewSource=play_count class=reel mediaType=2  BL746_WOULD_ACCEPT=true
[824744] ID-MATCH views=2544 viewSource=play_count class=reel mediaType=2  BL746_WOULD_ACCEPT=true
[d1c306] ID-MATCH views=2114 viewSource=play_count class=reel mediaType=2  BL746_WOULD_ACCEPT=true
[4efcff] ID-MATCH views=131  viewSource=play_count class=reel mediaType=2  BL746_WOULD_ACCEPT=true
[2b1d2a] ID-MATCH views=649  viewSource=play_count class=reel mediaType=2  BL746_WOULD_ACCEPT=true
```
**A hypothesis of mine, tested and DISPROVEN.** I suspected BL-746's own `viewSource != null` guard was refusing
these, since `hikerapi.ts:603` returns a fabricated 0 with a null viewSource for a `media_type 2` post. Every one
came back `viewSource=play_count` and `BL746_WOULD_ACCEPT=true`. The guard is not implicated; these were simply
submitted before the deploy.
**Cluster B, 3 old reels — ALL GONE:**
```
[f71e33] HTTP 404 {"exc_type":"MediaNotFound"}
[1cb175] HTTP 404 {"exc_type":"MediaNotFound"}
[614633] HTTP 404 {"exc_type":"MediaNotFound"}
```
**Cluster C, 3 `/p/` posts — NO COUNT EXISTS:**
```
[616424] ID-MATCH views=null viewSource=NULL class=carousel_image_only mediaType=8
[869150] ID-MATCH views=null viewSource=NULL class=carousel_image_only mediaType=8
[baaf3a] ID-MATCH views=null viewSource=NULL class=carousel_image_only mediaType=8
```
**These are image-only carousels.** They contain no video, so Instagram has no play count to report and never will.
`views=null` is the **correct** answer, and BL-543's NULL-never-0 rule is doing exactly its job. A backfill cannot
fix them because there is nothing to fetch.
**So the population is NOT uniformly recoverable:** 5 of 5 recent reels resolve; 6 of 6 older clips do not, for two
legitimate and permanent reasons.
## PART 4 — What it costs the clippers, ESTIMATED not measured
**These figures are an ESTIMATE.** They are the median earnings of comparable APPROVED clips on the same campaign,
not a measurement of what these clips would have done.
| Campaign | Median earnings per APPROVED clip | Affected APPROVED clips |
|---|---|---|
| Zhus Edit (0.50 CPM) | $1.43 | 4 |
| Zhus Meme (0.20 CPM) | $0.39 | 6 |
| Panic Baby | $0.99 | 2 |
| bees.n.honey | $1.10 | 1 |
| SomeSome | $4.11 (n=1, unreliable) | 8 |
**Estimated total exposure: roughly $10 to $25**, and materially less than that is actually owed, because:
**Cluster A (10 clips, ~$6 estimated) is not lost at all** — those clips get their stats at the next tick and will
earn normally. The only cost is a few hours of delay.
**Cluster B (3 clips) has deleted posts.** Under BL-720's rule a clip whose post no human can see is retired; these
would earn nothing whether or not a stat had been recorded.
**Cluster C (7 clips) are image-only carousels with no views in existence.** On a views-based CPM, a post with no
views legitimately earns nothing. The absence of a stat is not what is costing these clippers; the absence of video
views is.
**So the framing "clippers earning nothing because no view count was recorded" is largely not borne out.** For most
of this population the missing stat is a *symptom* of there being nothing to count, not the *cause* of lost money.
The genuine grievance is narrow: at most a handful of dollars, concentrated in `70aa2a` (5 carousel clips, 11.2 days)
and `a92aea` (2 clips, 12.0 days).
**Support contact and short payouts: NOT determinable from the data available to this round.** I found no field
linking a support message or a payout shortfall to a specific clip, and I will not infer one.
## PART 5 — The backfill spec, and why I recommend against running it
**Which clips would even qualify:** only Cluster B and C, 10 APPROVED clips, since Cluster A self-heals. **Of those
10, probing says 6 of 6 sampled are permanently unresolvable.** A backfill would spend calls to learn what the probes
already established.
Were one built anyway, it must:
**Write NULL, never 0.** `hikerapi.ts:603` still returns `views: singleProbe?.value ?? 0` with a null `viewSource`
for a `media_type 2` post; BL-746 fixed this at its own call site and deliberately left the shared classifier alone.
A backfill must apply the same guard: **accept a count only when `viewSource != null`**, or it will write a
fabricated 0 and zero a clipper's views, which is the precise harm BL-543 and BL-605 exist to prevent.
**Skip genuinely-gone posts.** A 404 `MediaNotFound` must be recorded as gone, not retried and not revived.
**Skip image-only carousels.** `carousel_image_only` / `media_type 8` has no count; writing anything is fabrication.
**Never touch a healthy clip.** Scope strictly to clips with **zero** ClipStat rows.
**Rate and cost:** 10 clips, one call each, sequential, one call per profile. **$0.010, runtime under a minute.**
**Rollback:** delete the ClipStat rows it created, identifiable by their `checkedAt`.
**Does the backoff need fixing first? No.** It is capped at 360 minutes and retries forever. The thing that actually
strands Cluster B is that **PAUSED and PAST campaigns are not polled**, which is deliberate and correct behaviour, not
a defect to repair.
## PART 6 — Verdict and ranking
**10 of 21 APPROVED clips resolve themselves within the hour; 11 are permanently unresolvable for legitimate reasons;
estimated money at stake is roughly $10 to $25; and the backoff does NOT need fixing because it is already bounded at
360 minutes.**
**Recommended: do nothing beyond watching one tick.** Confirm at the next hourly tick that Cluster A picked up its
stats. That single observation resolves half the population at zero cost and zero risk.

**The prediction, stated so it can be falsified rather than hedged.** At `2026-08-09 15:55:38Z` Cluster A was
exactly **10 clips with 0 stats**. If this report is right, all 10 have stats shortly after the **16:00Z** tick and
the APPROVED zero-stat count falls from 21 to 11. If they do not, this report is wrong and the tick path needs the
same treatment the submit path just received.
**Recommended against: a manual backfill.** It would target 10 clips of which the probes say 6 of 6 cannot be
resolved at all, for an estimated few dollars, while carrying the live risk of writing a fabricated 0 through
`hikerapi.ts:603` into a clipper's earnings.
**Worth doing separately, and larger than this round:** decide the product question these clips actually expose,
which is what an **image-only Instagram carousel** should do on a views-based CPM campaign. Seven APPROVED clips are
sitting in that gap. They are not broken; they are unanswered.
## What could not be measured
The one APPROVED TikTok clip (`83e7da`, 10.7 days, INFRA_DEFER) was **not probed**: it needs the LamaTok client
rather than Hiker, and one clip did not justify a second provider path inside this round's cap. It is likely the
BL-712 slideshow class but I did not verify that and am not asserting it. Whether any affected clipper contacted
support or was short-paid is not determinable from the schema. Handles are redacted; no wallet address was selected
or printed.
