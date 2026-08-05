# BL-717 — A revival re-check schedule for retired clips, and the fetch-failure versus genuinely-gone distinction

READ-ONLY DESIGN AUDIT. No code, data or money was changed. Nothing was revived, nothing was retired, no cron was altered, no env flag was touched. Only `SELECT` ran through `scripts/run-select.js`. Fifteen live provider calls were made and every one is disclosed below with its cost. No Apify actor was run; the eleven BL-678 guards are untouched. Clipper handles are redacted.

Code read at `main` = `1faf072a` in an isolated worktree at a short path. Every timestamp is cast `::text` against `now()` = **2026-08-05 11:40:28.010763+00**.

---

## VERDICT (one line)

**No clip in the current retired population is provably wrongly marked gone, but the platform cannot tell the difference between a deleted post and one our credential merely cannot reach, so the guarantee the owner is asking for does not exist today and cannot be measured with the evidence the system records.**

---

## The one-paragraph answer to the owner

His instinct is right, and the fix he asked for is the second-most-valuable one. A retired clip is genuinely never re-checked again: the cron poll excludes it by where-clause at `tracking.ts:3556`, so the auto-restore at `tracking.ts:1726` that everyone assumes protects them is **unreachable for exactly the clips that need it**. But the deeper problem is upstream. HikerAPI's `/v2` endpoint returns HTTP 404 for a post that is *inaccessible* just as readily as for one that is *deleted*, and this module says so in its own header at `hikerapi.ts:8-9`. The retirement gate at `retire-dead-clips.ts:111` reads only that status code. So a post behind a private account, a region lock, an age gate or a temporary restriction reads as GONE while a human can still open it, and since BL-698 that verdict now silently removes money from a real person's displayed balance. Fixing the verdict costs one extra provider call per retirement. Building the revival schedule costs about 8 cents per retired clip forever. Fix the verdict first.

---

# PART 1 — What actually distinguishes gone from unreachable today

## The three writers of `videoUnavailable`, and which are live

| # | Writer | file:line | Evidence required | Earnings effect | Live today |
|---|---|---|---|---|---|
| 1 | Retirement cron | `src/lib/retire-dead-clips.ts:111-125` | one fresh HikerAPI HTTP 404 this run | **frozen**, never zeroed (earnings columns deliberately absent from the update) | **YES**, daily 06:00 UTC (`railway-cron-scheduler.ts:92`) |
| 2 | Tracking error regex | `src/lib/tracking.ts:3131` then `:3163-3175` | `/not found\|no results\|private\|removed\|unavailable/i` matched against an **error message string** | **zeroed** via `writeClipEarningsZero`, `savedEarnings` stamped, AgencyEarning row deleted | **effectively dead**, see below |
| 3 | Account-ban cascade | `src/lib/clip-account-cascade.ts:182-199` | user banned | zeroed, `savedEarnings` stamped | yes, on ban only |

**Writer 2 is the one that looks terrifying and is currently defanged, which is worth stating precisely rather than leaving as folklore.** It matches the literal word `private` against an exception message, and it zeroes money. The only string in the live fetch path that could ever match it is `"TikTok: No results returned from Apify"` at `apify.ts:611`. That line now sits **behind** BL-678 GUARD 2 at `apify.ts:579-582`, which throws `"apify hard off (BL-678)"` first, and that string matches none of the five regex alternatives. `APIFY_HARD_OFF` is a `const true` that reads no environment variable (`apify-hard-off.ts:62`), so the branch is statically unreachable rather than merely disabled. Measured confirmation: exactly **6 clips** in the entire database carry a non-null `savedEarnings`, every one stamped at **2026-05-15 11:41:13.974242 to 11:41:14.341199**, and all six had `earnings = 0` and `savedEarnings = 0`, so no money was ever harmed by this path. It has not fired in 82 days. **It is still a loaded gun pointed at the money path and it should be deleted or narrowed, but it is not what is happening now.**

So the live question reduces to one line: **`retire-dead-clips.ts:111`, `if (httpStatus === 404)`.**

## What a 404 actually means

`hikerapi.ts:8-9`, the module's own header, verbatim:

> `/v2/` returns 200 for found posts and 404 for **inaccessible/deleted**

`hikerapi.ts:782-783` repeats it at the verdict site:

> The `/v2/` endpoint returns 404 ONLY for an **inaccessible/deleted** post (documented in this module's header).

Both sentences are accurate and both concede the point. **"Inaccessible" and "deleted" are two different facts about the world and the platform records them as the same integer.** The retirement gate reads `res?.httpStatus` at `retire-dead-clips.ts:105` and nothing else: not the response body, not the account, not a second observation on a later day.

## Every case the owner asked about

Evaluated against the live path (`retire-dead-clips.ts:104-139`), where `404` retires, `200` is left alone at `:132-135`, and everything else falls to `:136-139` and is never retired.

| Case | Provider response | Reads as GONE today? | Could a human still see the post? | Verdict |
|---|---|---|---|---|
| Provider outage (5xx) | HTTP 500 | **no** (`:136` ambiguous) | yes | correct |
| Rate limit | HTTP 429 | **no** (`:136`) | yes | correct |
| Auth / balance failure | HTTP 401 / 402 | **no** (`:136`) | yes | correct |
| Network error or timeout | `httpStatus = -1` (`:107`) | **no** (`:136`) | yes | correct |
| Post genuinely deleted | 404 + `MediaNotFound` | yes | no | correct |
| Account deleted or banned by Instagram | 404 | yes | no | correct |
| **Private account** | **404** (documented "inaccessible") | **YES** | **YES, every follower** | **DEFECT** |
| **Region-locked post** | **404** from our fixed-region proxy | **YES** | **YES, anyone in the allowed region** | **DEFECT** |
| **Temporarily restricted post (takedown under appeal)** | **404** | **YES** | **YES, the poster, and everyone once the appeal lands** | **DEFECT** |
| **Age-gated post** | **404** | **YES** | **YES, any logged-in adult** | **DEFECT** |
| TikTok slideshow `by/url` 500 (BL-712) | HTTP 500, verdict `carousel` (`lamatok.ts:261`, checked before the 404 gate) | **no** | yes | correct, twice over |
| Instagram image-only carousel | HTTP 200, verdict `quarantine` (`hikerapi.ts:810`) | **no** (200 takes the `:132` revived branch) | yes | correct |

## THE DEFECT, named plainly

**`src/lib/retire-dead-clips.ts:111` treats HTTP 404 as proof of deletion, when the provider that produced it documents 404 as meaning "inaccessible OR deleted" (`src/lib/scraper-providers/hikerapi.ts:8-9`, restated at `:782-783`). Four distinct real-world states in which a human can still open the post are therefore recorded as gone, earnings are frozen, and since BL-698 (`src/app/api/earnings/route.ts:206`) the money is also removed from the clipper's displayed balance with no notice and no appeal route.**

Three things make this worse than it looks and each is separately actionable:

**1. Instagram is held to a weaker standard than TikTok, and the stronger standard is already written.** BL-559 established for TikTok that a genuine gone verdict requires `404 AND MediaNotFound in the body`, and `gone-counter.ts:26-31` records that rule. The Instagram side never inspects the body: `is404()` at `hikerapi.ts:270-272` regexes the derived error *string* `"HikerAPI HTTP 404"`, and `retire-dead-clips.ts:105` reads the bare status. **The body discriminator exists and is free.** My live probe below shows every genuine deletion returns `{"detail":"Not found ({})","exc_type":"MediaNotFound"}`, so the field is present and parseable on this exact endpoint today.

**2. The account-level discriminator exists, is already built, and is never called.** `hikerapi.ts:274+` implements `GET /v2/user/by/username`, which returns `is_private` and distinguishes `not_found` from `transient` by design (`:322-349`). `clip_accounts.username` is stored for every clip. One extra call per candidate **account** separates "this post was deleted" from "this whole account went private" with certainty. `retire-dead-clips.ts` does not import it.

**3. Retirement rests on a single observation at a single instant.** There is no second look on a later day. Every transient condition that happens to present as a 404 for ninety seconds is indistinguishable from permanent deletion.

## Why BL-698 raises the stakes

Before 2026-08-03, a wrong gone verdict froze earnings quietly and the clipper's page still showed the money. Now `earnings/route.ts:206` filters retired clips out of the displayed balance, so a wrong verdict **takes money off a real person's screen the same day**. BL-714 measured the standing consequence at **$399.86 across 28 clippers**. The verdict is now a user-visible financial action taken on the strength of one integer that the provider says is ambiguous.

---

# PART 2 — How many are wrongly retired right now

## The population

| Measure | Value |
|---|---|
| Retired clips (`videoUnavailable = true`, not deleted) | **852** |
| Instagram | **852** |
| TikTok | **0** (excluded from retirement entirely, `retire-dead-clips.ts:74`) |
| Status APPROVED | **633** |
| Frozen earnings on APPROVED retired clips | **$3,583.50** |
| Retired within 30 days | **846** |
| Retired 45+ days ago | **6** (the 2026-05-15 regex-path rows, all $0.00) |
| Clip accounts still APPROVED | **852 of 852** (not one retirement came from a ban cascade) |
| Tracking jobs still `isActive` | **845 of 852** |

Retirement history, by day:

| Day | Retired |
|---|---|
| 2026-05-15 | 6 |
| 2026-07-18 | **708** (BL-584's one-off sweep) |
| 2026-07-19 to 2026-08-05 | **138** across 17 days |

**Steady-state retirement rate: 7.67 clips per day**, measured over the 18 days since the sweep. 2026-08-04 recorded zero, which is either a genuinely empty day or a missed 06:00 UTC run; the scheduler is bell-only and deliberately not watched by the watchdog (`railway-cron-scheduler.ts:88-91`), so a missed run raises no alarm. Not measurable from the data.

## The live re-probe

**15 calls, HikerAPI only, $0.001 each (`apify-ledger.ts:214`), total cost $0.015.** No Apify actor was run. Sample: 15 retired APPROVED clips, **one per clip account**, all on APPROVED accounts, spread across retirement dates 2026-07-18 to 2026-08-05, carrying **$902.91** of frozen earnings between them (25.2% of the total at risk). The probe replicates the production path exactly: `by/code` first, `by/url` only on a 404 (`hikerapi.ts:249-267`).

Pass 1, `GET /v2/media/info/by/code`, **12 calls**:

| Frozen earnings | Retired since (`::text`) | HTTP | Body |
|---|---|---|---|
| $324.00 | 2026-07-18 19:10:11.545056 | 404 | `{"detail":"Not found ({})","exc_type":"MediaNotFound"}` |
| $266.98 | 2026-07-18 19:10:11.545056 | 404 | same |
| $110.85 | 2026-07-18 19:10:11.545056 | 404 | same |
| $92.22 | 2026-07-18 19:10:11.545056 | 404 | same |
| $23.11 | 2026-07-18 19:10:11.545056 | 404 | same |
| $20.70 | 2026-07-18 19:10:11.545056 | 404 | same |
| $12.53 | 2026-07-18 19:09:57.398719 | 404 | same |
| $10.33 | 2026-08-03 06:00:30.765 | 404 | same |
| $7.47 | 2026-07-18 19:10:11.545056 | 404 | same |
| $7.33 | 2026-07-18 19:10:11.545056 | 404 | same |
| $6.03 | 2026-08-05 06:00:33.003 | 404 | same |
| $4.43 | 2026-07-19 21:16:24.031 | 404 | same |

Pass 2, `GET /v2/media/info/by/url` on the three highest-value rows, **3 calls**: all three 404 with the same `MediaNotFound` body.

**Result: 15 of 15 confirm gone at the provider level, and every one satisfies the stricter TikTok-grade rule (404 AND `MediaNotFound`) that Instagram is not currently required to meet.**

## What that does and does not prove

**Against BL-584 and BL-661.** BL-584 re-probed 734 candidates *before* retiring and found **24 alive (3.27%)**, which is precisely why the mandatory fresh probe now exists at `retire-dead-clips.ts:101-111`. BL-661 re-probed **26 of 26 already-retired clips as genuinely dead**. My 15 of 15 is consistent with BL-661 and shows **no drift**. The 3.27% BL-584 measured was a false-positive rate *at candidate selection*, and the gate that catches it is now permanent and running daily. That number should not be quoted as a current error rate; it is the error rate of a step that no longer decides anything.

**Honest extrapolation, with the sample size stated.** 15 of 852 is a **1.76% sample**, and it was deliberately weighted toward the highest-earning clips rather than drawn at random, so it is a worst-consequence sample, not an unbiased one. Zero failures in 15 draws bounds the true wrongly-retired rate at **18.1% at 95% confidence** (`1 − 0.05^(1/15)`), not at zero. Applied to the population that is the difference between **$0 and roughly $650** of frozen earnings on up to **154 clips**. The point estimate is zero. The honest statement is that this sample cannot rule out a rate that would matter.

**The limitation that matters most, stated plainly.** *A live probe cannot answer the owner's actual question.* HikerAPI returns 404 for a private-account post and for a deleted post identically, so re-probing with the same credential can only ever confirm what the retirement gate already concluded. **Every one of these 15 clips could be sitting behind a private account, visible to every follower right now, and this probe would look exactly as it does.** Answering it requires the profile endpoint (`hikerapi.ts:274+`, `is_private`), and that would have exceeded the 15-call cap agreed for this round. **It is the single most valuable measurement still outstanding and PART 6 specifies it as step 0.**

**Money on wrongly-retired clips: $0.00 provable, up to ~$650 not excluded.** The total exposure if the gate were badly wrong is the full **$3,583.50** frozen across 633 APPROVED retired clips.

---

# PART 3 — The re-check schedule

## The gap being closed

Retired clips are excluded from the cron poll by where-clause at `tracking.ts:3554-3556` (`videoUnavailable: false`), inside `if (!campaignIds)` at `:3546`. The auto-restore at `tracking.ts:1726-1742` fires on any tick where `videoUnavailable && stats.views > 0`, but a retired clip can never reach that line on the cron path, because it was filtered out three thousand lines earlier. **The restore mechanism everyone believes protects retired clips is unreachable for retired clips.**

One channel does survive: a **targeted** run with `campaignIds` supplied skips the filter entirely, so the owner clicking "check this campaign now" does re-poll retired clips and can revive them. That is the only revival path in production today, it is manual, undocumented, and nobody knows it exists. (Edge case worth noting in the build: `campaignIds = []` is truthy, so an empty array also skips the filter at `:3546` while setting no campaign constraint at `:3513`.)

## The schedule

| Tier | Window after `videoUnavailableSince` | Cadence | Calls per clip |
|---|---|---|---|
| A | day 0 to day 30 | daily | 30 |
| B | day 30 to day 45 | every 3 days | 5 |
| C | day 45 to day 365 | every 7 days | 45.7 |
| stop | day 365 | none | none |
| | | **lifetime** | **80.7 calls = $0.081 per clip** |

## Does re-checking ever stop? Yes, at 365 days, and here is why

Continuing forever is the tempting answer and it is the wrong one, for a cost reason that compounds and a truth reason that does not.

**The cost reason.** A 7-day tier that never ends is a permanently growing liability: the tier C population only ever increases, so the daily call count rises linearly forever. At 7.67 retirements per day that is **$146 of new recurring annual cost added every year**. Five years in, the tail alone costs about **$730 a year** to keep asking questions about posts deleted in 2026. A 365-day stop makes the lifetime cost of a retired clip a **fixed 8.1 cents**, which is a number the owner can reason about, and it caps the whole programme at a constant.

**The truth reason.** The realistic revival causes are an appeal succeeding, a temporary restriction lapsing, or an account coming back from private. All three resolve in weeks or a few months. An Instagram post that has 404'd every week for a year is not coming back, and asking anyway is not diligence, it is theatre with a bill attached.

**The escape hatch.** Stopping must be recorded, not silent: stamp `revivalCheckStoppedAt` so a clip that stopped can be re-enrolled by a one-line query if the owner ever disagrees. Stopping must never mean deleting anything; the clip, its frozen earnings and its tracking job all stay exactly as they are.

## Cost at each tier

HikerAPI is **$0.001 per call** (`apify-ledger.ts:214`).

**Today's population (852 clips: 846 in tier A, 0 in tier B, 6 in tier C):**

| Tier | Clips | Calls/day | $/day |
|---|---|---|---|
| A | 846 | 846 | $0.846 |
| B | 0 | 0 | $0.000 |
| C | 6 | 0.9 | $0.001 |
| **Launch total** | **852** | **847** | **$0.85/day, $25.7/month** |

This is the peak and it is an artefact: 708 of those clips retired on the same day and all leave tier A together on 2026-08-17. It is not the steady state.

**Steady state at 7.67 retirements/day:**

| Horizon | Tier A | Tier B | Tier C | Calls/day | $/month |
|---|---|---|---|---|---|
| 3 months | 230 clips, 230 calls | 115 clips, 38 calls | ~1,197 clips, 171 calls | **439** | **$13.2** |
| 12 months | 230 clips, 230 calls | 115 clips, 38 calls | ~3,307 clips, 472 calls | **740** | **$22.2** |
| steady (with the 365-day stop) | | | | **~740** | **~$22** |

Cross-check by the per-clip lifetime figure: 2,800 retirements per year × $0.081 = **$227/year = $18.9/month**. The two methods agree within the rounding of the tier-C ramp, which is the point of computing it twice.

**An operational constraint the build must solve, not discover.** `retire-dead-clips.ts:48` paces probes at `REPROBE_DELAY_MS = 1200`, and `/api/cron/retire-dead-clips/route.ts:5` sets `maxDuration = 300`. At that pacing **one invocation fits 250 calls**. The launch-day tier A needs 846. Three options, in order of preference: raise the cadence to several slots per day with a per-slot cap and a `nextRevivalCheckAt` cursor so work resumes where it stopped; or reduce the delay after measuring the real HikerAPI ceiling (BL-540 saw a 429 in under 10 requests, but that was a burst with no pacing, and my 15 sequential calls at 1300ms saw zero 429s and a median latency of 810ms); or accept a longer drain during the first fortnight only. **Do not simply raise `maxDuration`.**

## The revival path, precisely

**Trigger.** A scheduled re-check returns HTTP 200 with a finite view count greater than zero. Nothing else revives a clip. A 200 with null or zero views is a quarantine, not a revival (`hikerapi.ts:639-643` already refuses to trust views ≤ 0, and that rule must be reused, not re-implemented).

**The write: reuse `tracking.ts:1739-1742` verbatim, do not author a second one.**
```
data: { videoUnavailable: false, videoUnavailableSince: null, savedEarnings: null }
```
Three columns. That is the entire revival write.

**Does the flag clear?** Yes, and that single write is sufficient for everything else, because every consumer keys off it: the clipper display (`earnings/route.ts:206`), the per-campaign withdrawal gate (`payouts/route.ts:424`), the campaign spend aggregate (`balance.ts:312`), and the cron poll filter (`tracking.ts:3556`).

**Does the money become withdrawable again?** Yes, automatically, with **no money write at all**. The earnings value was never destroyed for 846 of the 852: `retire-dead-clips.ts:119-125` deliberately omits the earnings columns from its update, so the stored number is intact. Clearing the flag is the whole restoration. For the 6 regex-path clips the earnings were zeroed, and `tracking.ts:1728-1738` documents the correct handling: do **not** write `savedEarnings` back, let the standard recompute rebuild all four invariant fields through `writeClipEarnings`.

**Does it resume from now, or is anything backdated? From now, and there is nothing to backdate.** Earnings are `(views / 1000) × clipperCpm` computed off the **current stored view count**, not a sum of deltas. A clip that was dead for 40 days and comes back with more views than it had simply reads its current number on the next tick and its earnings become what that number is worth. Views accrued while it was retired are therefore included automatically, without any catch-up logic. **This is the reason the design is safe, and it is also the trap: any "credit the missed period" step would be a second payment for the same views.**

**A revived clip can never be paid twice, and here is the structural reason.** `writeClipEarnings` writes an **absolute total**, never an increment (`clip-earnings-writer.ts:1-35`). A payout subtracts the full gross the clipper consumed via `clipperLiability` on the payout row (`balance.ts:126-132`), and that subtraction is permanent and independent of clip state. So a revived clip contributes its total to `globalEarned` exactly once while the prior payout remains subtracted in full. **The single prohibition: the revival path must never compute or credit a delta, a backfill or a catch-up amount. It clears a flag. It does not move money.**

**BL-538 never-decrease holds** because the revival write touches no earnings column at all, and the subsequent recompute goes through `writeClipEarnings`, which carries the guard.

**BL-543 NULL-never-0 holds** on the condition that the re-check treats every non-200 as null and **writes no ClipStat row**. A failed re-check must never write `views = 0`. This is the same contract `apify-hard-off.ts:37-49` already documents and BL-614 confirmed empirically.

**The interaction nobody has thought about, and it is live right now.** A revived clip re-enters its campaign's budget. If that campaign is at its ceiling, the L1 budget hard-lock at `clip-earnings-writer.ts:149-256` will **reject the increasing write** with `already-over-budget`. BL-714 measured exactly this state on a live campaign at $3,002.25 against a $3,000 budget. So a clip revived onto a capped campaign gets its flag cleared and its money visible again, but its earnings cannot grow, and any message shown to the clipper must not promise otherwise. **This is correct behaviour and must be documented, not patched.**

---

# PART 4 — The interaction with retirement itself

## Should K change? No, because K decides nothing

Measured on the current retired population, `consecutiveGone` at the moment of retirement:

| `consecutiveGone` | Retired clips |
|---|---|
| 0 | **647** |
| 1 to 2 | 149 |
| 3 or more | 56 |

**Seventy-six percent of every retirement the platform has ever made happened on a clip whose gone counter was zero.** They entered the candidate set through the second branch at `retire-dead-clips.ts:77` (`checkIntervalMin >= 1440`), not the counter branch at `:76`. The code says so plainly at `:64-68`: BL-588 proved the counter structurally under-fires because the Instagram gone-lookups run outside the batch that feeds it, so keying on the counter alone "would retire almost nothing".

**Therefore K=3 is not a threshold, it is a decoration.** Raising it to 5 changes nothing for 647 of 852 clips. Lowering it to 1 changes nothing either. **The fresh 404 at `:111` is the entire gate, and it is a single observation of an ambiguous integer.** Any effort spent tuning K is spent on the wrong control.

## Should the re-probe at retirement change? Yes, in three ways

1. **Require `MediaNotFound` in the body, not just status 404.** `retire-dead-clips.ts:105` reads `res?.httpStatus` alone. `HikerResult` already carries `rawBody` (`hikerapi.ts:97-100`) and it is already populated. This is the exact rule BL-559 wrote for TikTok and `gone-counter.ts:26-31` records. Cost: **zero extra calls**. It closes every case where an opaque 404 is produced by something other than a missing media object.
2. **Require two fresh 404s on separate days.** Add a `goneConfirmedAt` stamp: the first fresh 404 stamps it and retires nothing; the next day's run retires only if a second fresh 404 lands. Cost: **one extra call per retirement**, 7.67 per day, **$0.008 per day**. It eliminates every single-instant provider anomaly, and it is cheaper than the revival schedule by two orders of magnitude.
3. **Probe the account before retiring the post.** `GET /v2/user/by/username` (`hikerapi.ts:274+`) returns `is_private`. If the account is private or itself returns `not_found`, the post's 404 tells us nothing about the post and the clip must be **quarantined, not retired**. Cost: one call **per account**, not per clip, and accounts repeat heavily across a retirement batch.

## Retiring fewer beats reviving more, and it is not close

| | Fix the verdict | Build the revival schedule |
|---|---|---|
| What it fixes | a defect nameable at `retire-dead-clips.ts:111` with the provider's own documentation as evidence | a recovery rate nobody has measured |
| Cost | ~1 extra call per retirement, **$0.008/day** | **$13 to $22 per month, forever** |
| Effect on a clipper | the money never leaves their screen | the money leaves their screen, then may come back weeks later |
| Blast radius if wrong | a few clips stay in the poll one extra day | a wrongly retired clip waits up to 30 days for its first re-check |
| Measurable before shipping | yes, the profile probe answers it directly | no, requires a month of observation |

**A clip that is never wrongly retired needs no revival.** The revival schedule is a compensating control for a verdict we do not trust; the correct engineering order is to make the verdict trustworthy first and then decide how much compensation is still worth buying. There is also a fairness argument the owner will care about: BL-698 means a wrong verdict takes money off someone's screen **today** and a 30-day-tier revival gives it back **up to a month later**, and no clipper experiences that as the system working.

---

# PART 5 — The cost and the payoff, honestly

## Cost

| Item | Monthly |
|---|---|
| Revival schedule, launch fortnight | **$25.70** |
| Revival schedule, 3 months | **$13.20** |
| Revival schedule, 12 months and steady | **$22.20** |
| Verdict fix (second-day confirmation) | **$0.24** |
| Account probe at retirement | **under $0.10** |

## Payoff

**The honest answer is that the payoff is unmeasured, and my best evidence suggests it is small.**

What is known: 15 of 15 retired clips, weighted toward the highest earners and covering 25.2% of the money at risk, are gone at the provider level and satisfy the strictest verdict rule the codebase contains. BL-661 found 26 of 26 the same. **Two independent samples totalling 41 clips have produced zero revivals.**

What is not known, and cannot be inferred from anything the platform stores: **the rate at which a 404'd Instagram post comes back.** There is no historical record of a revival, because until now no mechanism existed that could observe one. The 24-of-734 figure from BL-584 is often quoted here and it does not apply: those clips were spared **before** retirement by the probe that now runs on every candidate, so that 3.27% is the false-positive rate of a step the gate already catches, not a revival rate.

If the true revival rate is the 0-of-41 point estimate, the schedule costs **$22 a month to recover nothing**. If it is 1%, the schedule recovers roughly **28 clips a year** carrying perhaps **$160** of frozen earnings, and pays for itself at about half its cost. **On the evidence available, this build does not obviously pay for itself, and I am not going to dress it up as though it does.**

Two things nonetheless argue for building it, and neither is financial:

1. **It is the only mechanism that can ever measure the rate.** Right now the platform cannot detect its own false positives at all. That is worth $22 a month independent of what it recovers.
2. **A clipper whose live video was wrongly retired currently has no route back.** Even one such case a year is a support incident, a fairness failure and, since BL-698, a visible loss of money. The cost of the schedule is roughly one-tenth of the frozen earnings on a *single* $250 clip.

**And the cheap version answers the question first.** A pilot enrolling **100 retired clips** in the daily tier for 30 days costs **$3.00 total**. If it finds zero revivals in 3,000 calls, the full schedule can be shelved with evidence rather than shipped on a hunch. **That is what I would do before writing the scheduler.**

For scale: BL-657 measured stuck money growing about **$1.15 a day**, and BL-714 measured **$399.86 across 28 clippers** that the owner's admin displays and no clipper can withdraw. **Both of those are larger, better-evidenced problems than this one, and neither costs $22 a month to address.**

---

# PART 6 — The spec and the verdict

## One line

**No clip is provably wrongly marked gone today, but the platform cannot distinguish "deleted" from "our credential cannot reach it", so it cannot honestly claim otherwise, and four real-world states in which a human can still open the post are recorded as gone at `src/lib/retire-dead-clips.ts:111`.**

## Ranking

1. **The gone-verdict fix.** Nameable defect, provider-documented, costs pennies, prevents the harm outright.
2. **The measurement pilot.** $3.00, 30 days, answers whether item 3 is worth building.
3. **The revival schedule.** Real value, honest cost, unproven payoff. Build it after the pilot reports.

## Build-ready spec

### Step 0 — MEASURE FIRST (no code, ~1 hour, ~$0.05)

Probe `GET /v2/user/by/username` (`hikerapi.ts:274+`) for the distinct clip accounts behind the 20 highest-earning retired clips. **If any account returns `is_private = true`, those clips are wrongly retired and steps 1 and 2 become urgent rather than merely correct.** This is the measurement the 15-call cap forced this round to leave undone and it should be the first thing the next round does.

### Step 1 — Tighten the verdict (highest value, smallest diff)

* `src/lib/retire-dead-clips.ts:104-111`: require `MediaNotFound` in `res.rawBody` in addition to `httpStatus === 404`. `rawBody` is already populated (`hikerapi.ts:97-100`). Anything else falls to the existing `ambiguous` branch at `:136`.
* `src/lib/retire-dead-clips.ts:111`: add the account gate: resolve `clip_accounts.username`, call the profile endpoint once per **distinct account** in the batch, and if `is_private` or `not_found`, count the clip as ambiguous and never retire it.
* **Prove:** a dry run (`?dryRun=1`, already supported at `route.ts:30`) over the same candidate set before and after, showing `confirmedGone` drops by exactly the count of body-less 404s plus private-account clips, and `retired` stays 0 in dry run. No DB write.
* **Rollback:** `git revert`. No schema change, no data change.

### Step 2 — Two-day confirmation

* Additive nullable column `TrackingJob.goneConfirmedAt` via `ALTER TABLE ADD COLUMN IF NOT EXISTS` through `scripts/run-schema-sql.js`, then `npx prisma generate` only. **Never `prisma migrate`.**
* `src/lib/retire-dead-clips.ts:111`: a fresh confirmed-gone stamps `goneConfirmedAt` and retires nothing; retire only when `goneConfirmedAt` is at least 20 hours old and this run also confirms gone.
* **Prove:** on the first run after deploy, `retired = 0` and `goneConfirmedAt` is non-null on exactly the confirmed set; on the second day, retirements resume. Earnings totals identical to the cent across both runs.
* **Rollback:** `git revert`; the column is additive and nullable so nothing needs dropping.

### Step 3 — The pilot (30 days, $3.00)

* New cron `revival-recheck`, registered in `railway-cron-scheduler.ts` alongside `retire-dead-clips` (**bell-only, not added to `JOB_NAME_TO_HEARTBEAT_KIND`**, same as `:88-91`), gated behind `RAILWAY_NATIVE_CRON` so the owner enables it deliberately (this is exactly what BL-593 had to fix retrospectively for `retire-dead-clips`).
* Additive nullable columns: `Clip.nextRevivalCheckAt`, `Clip.revivalCheckCount`, `Clip.revivalCheckStoppedAt`.
* Enroll the 100 highest-earning retired clips at daily cadence. **Log only. Revive nothing.**
* **Prove:** 30 days of `[REVIVAL-PROBE]` lines, a count of 200s, and zero writes to any Clip column other than the three new ones.

### Step 4 — The schedule (only if step 3 finds revivals)

* Tiers as specified: daily to day 30, every 3 days to day 45, every 7 days to day 365, then stamp `revivalCheckStoppedAt` and stop.
* Selection: `videoUnavailable = true`, `isDeleted = false`, `revivalCheckStoppedAt IS NULL`, `nextRevivalCheckAt <= now()`, ordered by `earnings DESC` so the money is checked first, capped per run with the cursor advanced on every probe so a truncated run resumes rather than restarts.
* Revival write: **reuse `tracking.ts:1739-1742` exactly**. Three columns. No earnings write, no delta, no backfill.
* Trigger condition: HTTP 200 **and** a finite view count greater than zero. Reuse the `hikerapi.ts:639-643` predicate; do not re-implement it.
* **Pacing:** `maxDuration = 300` at `route.ts:5` and the 1200ms delay at `retire-dead-clips.ts:48` allow 250 calls per invocation. Schedule multiple slots per day with the `nextRevivalCheckAt` cursor rather than raising `maxDuration`.
* **Prove, all mandatory:**
  * the 6 money files byte-identical by blob OID, and `tracking.ts` not in the diff;
  * `writeClipEarnings` is not called anywhere in the new code (`grep -c` the file, do not pipe to `head`);
  * on a dry run, the earnings invariant `earnings ≈ baseEarnings + bonusAmount` holds with 0 violations before and after;
  * a simulated non-200 writes **no** ClipStat row (BL-543 NULL-never-0);
  * a revived clip that carries a prior PAID payout shows its global available unchanged by the revival itself, proving no double credit;
  * a revived clip on a budget-capped campaign clears its flag and its earnings do **not** grow, with the `[F-BUDGET-HARD-LOCK]` line present.
* **Rollback:** `git revert` the cron registration first (it stops instantly), then the code. The three columns are additive and nullable; leave them. Any clip wrongly revived is re-retired by the existing daily cron on its next fresh 404, so the failure mode is self-correcting in one day.

### Step 5 — Clean up the loaded gun

* `src/lib/tracking.ts:3131`: the `/not found|no results|private|removed|unavailable/i` regex on an exception message that zeroes earnings. It has not fired since 2026-05-15 and its only live trigger string is statically unreachable behind BL-678 GUARD 2. **Delete it, or narrow it to an explicit sentinel.** Matching the word `private` against an error string to decide whether to zero a person's money is not a rule anyone would write deliberately today, and it will become reachable again the moment anyone re-enables an Apify path.

---

## Safety statement

READ ONLY. One document produced. No source file was modified, so no build was run and none is claimed; a markdown-only change cannot affect `tsc`. Nothing was revived, nothing was retired, no cron was altered, no env flag was flipped, no schema was touched. Every database statement was a `SELECT` through `scripts/run-select.js`, which refuses `insert`, `update`, `delete`, `drop`, `truncate`, `alter`, `create`, `grant` and `revoke` before connecting. **Live probes: exactly 15, all HikerAPI GET requests, one clip per clip account, 12 by/code plus 3 by/url follow-ups, $0.001 each, total $0.015, every one listed in PART 2.** No Apify actor was run and the eleven BL-678 guards were not touched or bypassed. Work was done in an isolated worktree at a short path; `node_modules` was never junctioned; the shared working tree's HEAD was not moved and nothing held by the concurrent BL-716 round was touched. Clipper handles are redacted.

**What could not be measured, stated plainly:** whether any retired clip sits behind a private, region-locked, age-gated or temporarily-restricted account that a human could still open, because that requires the profile endpoint and the 15-call cap was already spent on the media probe; the true revival rate of a 404'd Instagram post, because no mechanism has ever existed that could observe one; whether 2026-08-04's zero retirements was an empty day or a missed 06:00 UTC run, because this cron is deliberately unwatched; and the real HikerAPI sustained rate ceiling, since 15 sequential calls at 1300ms is not a load test.
