# BL-745 — why are views not fetched the moment a clip is submitted?
**Audited at** `b5bd0651` · 2026-08-09 · **READ ONLY.** No code, config or data changed. No submission created.
No Apify actor run; the 11 BL-678 guards untouched. **10 HikerAPI calls disclosed, ~$0.010**, against a cap of 20.
## ONE LINE VERDICT
**The owner is right, but only about Instagram: 0 of 777 Instagram clips in 14 days got a stat within a minute
(median 3,610s), while TikTok and YouTube both sit at a median of 0s — and killing Apify is exactly what did it.**
## PART 1 — What actually happens at submit, traced
**A provider call IS made at submit.** `clipper-submit-core.ts:375` calls `fetchClipFreshnessWithRetry(clipUrl,
platform)` for all three platforms, and `:408` captures `views, likes, comments, shares` from it. The owner's premise
that nothing is fetched is not what the code does.
**A first ClipStat IS written at submit, unless views is null.** `:569-579`, inside the same transaction as the clip:
```ts
const resolvedFirstViews = fetchedStats?.views;
if (resolvedFirstViews != null) { await tx.clipStat.create({ ... }); }
```
That is BL-605/BL-543: `ClipStat.views` is a non-nullable Int, so rather than fabricate a 0 (which would zero the
clipper's views and freeze earnings) the snapshot is **skipped**. **How often the skip actually fires, measured over
14 days:** Instagram **100%** (0 of 777 written), YouTube **21%**, TikTok **9%**.
**`nextCheckAt` is the top of the NEXT hour**, pushed a further hour if that is under 30 minutes away
(`:581-588`). So a clip whose first snapshot was skipped waits **30 to 90 minutes**. The measured Instagram median of
**3,610s (60.2 min)** matches that schedule exactly, which is itself confirmation that Instagram never gets the submit
write and always waits for the tick.
## PART 2 — The measurement, which is the deliverable
Clips submitted in the last 14 days, non-test campaigns:
| Platform | Clips | ≤1 min | ≤5 min | ≤1 hour | Zero stats ever | Median | Worst |
|---|---|---|---|---|---|---|---|
| **Instagram** | 777 | **0** | **0** | 366 | **39** | **3,610s** | 481,554s |
| TikTok | 171 | 155 | 155 | 158 | 1 | **0s** | 624,666s |
| YouTube | 71 | 56 | 56 | 62 | 0 | **0s** | 468,894s |
**Single versus batch is NOT the variable.** Instagram fails identically either way (0 of 302 batch, 0 of 477 single;
medians 3,484s and 3,709s), and TikTok batch is **75 of 75** inside a minute. Bulk submission is not the problem.
**BL-712's zero-stat population re-measured post-BL-713: it was NOT resolved and it is still growing.** 41 clips now
have zero ClipStat rows ever, 11 of them APPROVED (BL-712 counted 13). **40 of 41 are Instagram, and 41 of 41 were
submitted after the cutover**, the oldest on 2026-07-25. BL-713's slideshow fix addressed a different mechanism; this
population has a different cause.
**Where the owner's perception is wrong:** TikTok and YouTube already do exactly what he wants, at a median of zero
seconds. Any fix should be scoped to Instagram rather than applied to all three.
## PART 3 — Did killing Apify cause it? Yes, and the cliff is unmistakable
Delay split at the cutover, `2026-07-22 11:12Z`:
| Platform | Era | Clips | ≤1 min | % ≤1 min | Median | Zero stats |
|---|---|---|---|---|---|---|
| **Instagram** | BEFORE | 669 | 648 | **96.9%** | 0s | 0 |
| **Instagram** | AFTER | 828 | **0** | **0.0%** | **3,656s** | 40 |
| TikTok | BEFORE | 500 | 486 | 97.2% | 0s | 0 |
| TikTok | AFTER | 198 | 178 | 89.9% | 0s | 1 |
| YouTube | BEFORE | 910 | 908 | 99.8% | 0s | 0 |
| YouTube | AFTER | 73 | 58 | 79.5% | 0s | 0 |
**96.9% to 0.0% is a switch being thrown, not a degradation.** TikTok and YouTube keep a median of 0s across the
boundary.
**And it is the same shape BL-673 and BL-682 found.** `fetchClipFreshnessWithRetry` calls `fetchClipStats` with
`{ skipHikerOverlay: true }` (`apify.ts:2561`), added by BL-137 so Instagram could read a parseable `createdAt` for
the 30 minute gate. That flag makes `apify.ts:2383`'s overlay block false, so **no HikerAPI call is made on this
path**, and control falls to `fetchInstagramStats` whose tiers all return null behind BL-678 GUARD 3
(`apify.ts:796`). A code path that reads as platform-agnostic depended on Apify for Instagram alone.
## PART 4 — Can a count actually be fetched at submit? For Instagram, YES, provably
Probed live on four Instagram clips that have **zero ClipStat rows**, one of them submitted **one second** before the
query that found it:
```
[Db0aiMMIz25] views=140  likes=4  class=reel via=by_code viewSource=play_count
[Db0ZcZZofoo] views=162  likes=7  class=reel via=by_code viewSource=play_count
[Db0YVQuI7Kb] views=403  likes=12 class=reel via=by_code viewSource=play_count
[Db0X_x8Scgi] views=1136 likes=3  class=reel via=by_code viewSource=play_count
```
**The data was available the whole time. The submit path simply did not ask.** A second probe minutes later returned
155 and 480 for the first and third, so these are live, growing counts on genuinely fresh posts, not cached values.
**Honest correction on my own probing:** the first four calls printed all-nulls because I read `r.stats.views` while
`fetchHikerInstagramByUrl` returns `views` at the **top level**. That run measured my bug, not the provider; it is
discarded and its 4 calls are still counted in the 10 disclosed.
**One thing the overlay does NOT give:** `tryHikerForInstagram` returned `useResult=true` with views but
**`createdAt=null`**, so BL-137's original reason for skipping it still stands. You cannot simply un-skip the overlay
and get both. TikTok and YouTube need no probe: their own median of 0s proves availability.
## PART 5 — Cost, risk, and the batch case
**Measured volume, last 30 days:** Instagram **1,075**, TikTok 330, YouTube 262 — **1,667 a month**, not 2,300.
**HikerAPI costs exactly $0.001 per call** (40,452 calls, $40.45, derived from `apify_usage_entries`).
**The added cost is ZERO, and this is the finding that changes the spec.** `harvestInstagramRawMeta`
(`clipper-submit-core.ts:252-267`) **already calls `fetchHikerInstagramByUrl` at submit for every Instagram clip**
(`:454`), for BL-682's caption rescue and BL-686's `taken_at` freshness check. That response **already contains
`views`**, and the function throws it away by returning only the media object. Reading it costs **no new vendor call**.
BL-686 set this precedent explicitly in a comment at `:470-474`: *"BL-682 already harvests the HikerAPI media object
on this exact path, three lines above ... this adds ZERO new vendor calls."*
**Risk is near zero for the same reason.** The call already exists and **already fails open** (`:262-266`, catch,
warn, return null), so the submit path's failure behaviour is unchanged. Nothing new can block or throw. The
`if (resolvedFirstViews != null)` guard at `:570` already enforces **NULL never 0** per BL-543, and it stays.
**Batch is a non-issue**: a 10-row bulk submission already fires those 10 Hiker calls today. Nothing is added, so no
rate limit is approached that is not approached already, and partial failure already degrades per-clip rather than
per-batch, since each clip's harvest is independent and fails open on its own.
## PART 6 — Spec, and the honest ranking against the simpler option
**Option A, recommended — read the views already in hand.** `harvestInstagramRawMeta`
(`clipper-submit-core.ts:252`) returns only `media`; change it to also return the `views`/`likes`/`comments` the
same `HikerResult` already carries. At `:454`, when `fetchedStats` is null and the harvest produced a numeric view
count, populate `fetchedStats` from it. The existing write at `:569-579` then fires unchanged.
**Synchronous, because the call is already synchronous on this path** — no background job, no new failure mode.
**Fails open by construction:** unchanged catch at `:262`; if the harvest returns null, `fetchedStats` stays null,
the snapshot is skipped exactly as today, and the tick still covers it. **Cost $0. New vendor calls: 0.**
**What must be proven before shipping:** that a numeric view count reaches `ClipStat` for a real Instagram submission;
that a null harvest still skips rather than writing 0 (BL-543); that TikTok and YouTube are byte-identical, since
neither goes near this branch; that the 11 BL-678 guards and `apify.ts` are untouched; and that
`within_1_min` for Instagram moves off 0 on live data afterwards. **Rollback:** revert one file.
**Against the simpler option, ranked honestly.** Shortening the first `nextCheckAt` (`:582-585`) from the top of the
next hour to, say, 5 minutes is genuinely attractive: it adds **no** provider dependency, and it does not even add
calls, since it moves the first poll earlier rather than creating one. It would cut the Instagram median from ~60
minutes to ~5. **But it does not deliver what was asked** (stats visible immediately), it leaves the 41 zero-stat
clips unexplained, and it treats a symptom whose cause is a discarded field.
**Since Option A costs nothing, adds no call and reuses an already-fail-open call, it is strictly better here, and
I am not recommending the simpler option on this occasion.** Doing the `nextCheckAt` shortening as well is a cheap
belt-and-braces for the residual case where the harvest fails open, and is worth taking as a second, separate change.
## What could not be measured
Whether Instagram's provider had indexed each post at the exact instant of submission: the probes ran minutes to
hours after, and re-probing at true T+0 would require creating a submission, which this round forbids. The four
clips probed were between 1 second and 20 minutes old at submission and all returned counts, which is strong but not
identical evidence. Handles are redacted; no wallet address was selected or printed.
