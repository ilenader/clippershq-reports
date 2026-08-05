# BL-721 — the revival pilot: do retired clips actually come back, and is a schedule worth building

**AUDIT ONLY. READ ONLY on code, data, config and money.** Nothing revived, nothing retired, no clip flag, cron, env var or schema touched. Zero tracked source files changed (`git diff --stat -- src prisma` returns 0 lines); the only artefacts are three new read-only scripts and a results JSON. **No Apify actor ran**; the eleven BL-678 guards are untouched. **A markdown-only round cannot change tsc or the build, so neither was run and neither is claimed.**

Base `origin/main` = **`de0169bd`** (the BL-720 merge), branch `checkpoint/BL-721`, isolated worktree at the short path `C:/b721`, `node_modules` never junctioned.

**DB `now()` at probe start: 2026-08-05 18:05:39.361497+00. At final verification: 2026-08-05 18:49:04.15066+00.** Every timestamp is cast `::text` against that clock. Clipper handles and account ids are redacted to an 8-character prefix; the reports repo is PUBLIC.

### Probe budget, declared before the first call and reconciled after

| | Declared | Actual |
|---|---|---|
| Clips probed | 852 (all of them) | **852** |
| Media calls (up to 2 each: `by/code` then `by/url` on a 404) | ≤ 1,704 | 1,694 |
| Profile calls, **one per profile**, cached per account | ≤ 113 | **2** |
| Follow-up body inspection | not foreseen | 3 |
| **Total** | **≤ 1,817 = $1.817** | **1,699 = $1.699** |
| **Cap** | **$3.00** | **not reached** |

---

## THE ONE LINE

**Do NOT build BL-717's per-clip tiered schedule: the measured revival rate is 1.17%, the entire historical recovery is $12.62, and a schedule costing $13 to $22 a month forever would cost more every month than everything it could ever have recovered — but the census found something worth more than the money, which is that all ten revivals sit on just TWO accounts that came back whole, and that BL-720's path A cannot tell a deleted account from a RENAMED one.**

---

# PART 1 — the sample, and why it is a census

### It is not a sample. Every retired clip was probed.

BL-717 probed 15 clips and had to bound its conclusion at 18.1% at 95% confidence. BL-720 probed 113 accounts. **This round probed all 852 retired clips**, because at $0.001 a call the whole population cost $1.70 and fit inside a $3.00 cap. **There is no sampling error in anything below.**

### Stratification 1: by BL-720's account census

| Account state (BL-720, 2026-08-05 15:31 UTC) | Accounts | Retired clips | APPROVED | Frozen | Probed here |
|---|---|---|---|---|---|
| `RESOLVED_PUBLIC` | 68 | 468 | 312 | $2,792.66 | **all 468** |
| `ACCOUNT_NOT_FOUND` | 44 | 381 | 318 | $790.84 | **all 381** |
| `RESOLVED_PRIVATE` | 1 | 3 | 3 | $0.00 | **all 3** |
| **Total** | **113** | **852** | **633** | **$3,583.50** | **852** |

**Were the 44 account-gone clips sampled? Yes, all 381 of them, and that decision paid for itself.** The prior reasoning was that an account returning 404 cannot serve any of its posts, so probing them is waste. **That reasoning is wrong, and this census is what proved it**: 9 of the 10 revivals found are on an account whose stored username returns 404 while its media resolves 200. Had I excluded that stratum on the "obviously dead" argument, the round's single most important finding would have been missed for $0.38 of saved calls.

### Stratification 2: by time since retirement, and the hole in it

| Bucket | Clips | APPROVED | Frozen |
|---|---|---|---|
| A 0-2d | 30 | 21 | $28.61 |
| B 3-7d | 63 | 34 | $11.21 |
| C 8-16d | 45 | 33 | $35.97 |
| D 17-30d | **708** | 539 | **$3,507.71** |
| **E 31-45d** | **0** | **0** | **$0.00** |
| F 46d+ | 6 | 6 | $0.00 |

**Two structural facts the owner's proposed tiering has to survive.** 83% of the population retired on a single day, 2026-07-18, in BL-584's one-off sweep, and is now 17 days old. And **bucket E is empty**: there is not one clip in the platform between 31 and 45 days retired, and only 6 older than 45 days.

### What this census structurally CANNOT see

Named before any conclusion is drawn from it, in the spirit of BL-717 naming its own blind spot:

1. **A clip that was wrongly retired and has since been genuinely deleted.** It reads 404 today and is indistinguishable from a correct retirement. The measured rate is therefore a **lower bound**.
2. **"Came back" versus "was never gone."** Both present as a 200 today. This round cannot date a revival and the platform stores no observation history to date it from.
3. **Bucket E, days 31 to 45, has no data at all** because the population has none. Any tier boundary there is an assumption, not a measurement.
4. **It is one point in time**, not a time series. A revival that happened and reverted between 2026-07-18 and today is invisible.
5. **It cannot see forward.** BL-720 changed the verdict two hours before this probe ran, so every clip measured here was retired by the OLD logic.

---

# PART 2 — the probe, and the correction that changed the answer

All 852 clips went through **`fetchHikerInstagramByUrl`**, the same production function `retire-dead-clips.ts` calls, so "reachable" means here exactly what it means in production.

### The counter said zero. The counter was wrong, and I checked before reporting it.

The census's first summary read **`reachable: 0, idMismatch: 10`**. Reported as-is that would have been "0.00% revival rate, build nothing" — a clean answer, and the wrong one.

The 10 "mismatches" were HTTP **200** with real view counts (1,287 to 17,832). My id-match looked for the returned shortcode at `body.code`, `body.media.code` and `body.items[0].code`. The actual path in HikerAPI's `/v2` payload is **`body.media_or_ad.code`**. Dumping three of them resolved it:

```
=== clip cmqsdazl200100ppe624scsrv ===
  askedShortcode=DZ-jq7PT9Qy   http=200 via=by_code views=12588 classification=reel
  topLevelKeys=media_or_ad,status
  id-ish fields: $.media_or_ad.code=DZ-jq7PT9Qy | $.media_or_ad.pk=3926732806567220000
                 | $.media_or_ad.id=3926732806567220274_78998082609

=== clip cmrdsfiss00070pma6ymg0jpr ===
  askedShortcode=DalJzbAzTZP   http=200 views=1287
  id-ish fields: $.media_or_ad.code=DalJzbAzTZP | ...

=== clip cmrjke2mb001r0ppkofhsbzix ===
  askedShortcode=Davj5B4KLaw   http=200 views=17832
  id-ish fields: $.media_or_ad.code=Davj5B4KLaw | ...
```

**`$.media_or_ad.code` equals the asked shortcode, exactly, on every one.** These are **id-matched genuine revivals**, not wrong-post responses. The failure was in my extractor, not in the identity. **BL-550's rule still did its job**: it refused to call them revivals until the identity was actually established, and the resolution took three extra calls.

### The corrected result

| Bucket | Clips | **Revived** | **Rate** | Frozen | **Recovered (APPROVED)** |
|---|---|---|---|---|---|
| A 0-2d | 30 | 1 | **3.33%** | $28.61 | $0.64 |
| B 3-7d | 63 | 1 | **1.59%** | $11.21 | $0.00 (REJECTED clip) |
| C 8-16d | 45 | **7** | **15.56%** | $35.97 | $11.37 |
| D 17-30d | 708 | 1 | **0.14%** | $3,507.71 | $0.61 |
| E 31-45d | 0 | n/a | **no data** | $0.00 | $0.00 |
| F 46d+ | 6 | 0 | **0.00%** | $0.00 | $0.00 |
| **Total** | **852** | **10** | **1.17%** | **$3,583.50** | **$12.62** |

Also measured: **842 not_found, 0 ambiguous** (not one 5xx, 429 or timeout across 1,694 calls), **0 genuine identity mismatches**.

### The per-bucket rates do NOT justify a time-tiered schedule, because the clustering is not in time

The C bucket's 15.56% looks like a strong argument for frequent early re-checks. It is not, and the reason is decisive:

> **All 10 revivals sit on just TWO accounts, and both came back WHOLE.**

| Account | Retired clips | Revived | Still gone | Recovered | Account probe today |
|---|---|---|---|---|---|
| `cmqgr2yt` | 9 | **9** | **0** | **$12.62** | **`not_found`** |
| `cmqyvvzg` | 1 | **1** | **0** | $0.00 (REJECTED) | `public` |

Account `cmqgr2yt`'s nine clips were retired across **three separate cron runs** spanning 16 days (2026-07-18 19:09:57, seven at 2026-07-25 06:00:03 to 06:01:44, and 2026-08-03 06:01:14), as each clip's poll cadence brought it into the candidate set. They did not fail together and they did not come back one at a time. **The account went unreachable, its clips were retired one by one as they were noticed, and then the account came back and every single one resolved.**

**So the C bucket's 15.56% is not a property of "8 to 16 days after retirement". It is one account's clips happening to have been retired in that window.** A tier design built on that number would be fitting a schedule to a coincidence. **The event is account-shaped, not clip-shaped, and not time-shaped.**

### Why those accounts read `not_found` while their posts resolve

Nine of the ten revived clips are on an account whose **stored username returns HTTP 404** on `/v2/user/by/username` while **its media returns 200**. An account cannot serve posts and simultaneously not exist. The parsimonious reading is that **the clipper renamed their Instagram account**: `clip_accounts.username` is now stale, so the profile lookup 404s, while the posts are perfectly alive under the new handle.

**This is the round's most consequential finding and it is about BL-720, not about revival.** See PART 4.

---

# PART 3 — what it would actually recover

### The money, in full

**$12.62.** That is every dollar of APPROVED earnings on every reachable clip in the entire retired population, accumulated over roughly three months. Nine approved clips at an average of **$1.40** each. The tenth revived clip is `REJECTED` and earns nothing whatever happens to it.

Against **$3,583.50** frozen in total, the recoverable share is **0.35%**.

### Would they resume earning? For most of the population, NO, and this is not about revival at all

| Campaign | Status | Retired clips | Frozen | Can a revived clip earn again? |
|---|---|---|---|---|
| somesome | **PAST** | 436 | **$3,434.41** | **No** |
| GainzAlgo (REPOST) | **PAST** | 185 | $71.70 | **No** |
| STRAENGE | **PAST** | 23 | $4.15 | **No** |
| Panic Baby | ACTIVE | 49 | $40.73 | yes |
| WinGram | ACTIVE | 108 | $19.07 | yes |
| bees.n.honey | ACTIVE | 49 | $13.14 | yes, but see below |
| BAD BITCH ANTHEM (0.50) | ACTIVE | 1 | $0.30 | yes |
| SomeSome | ACTIVE | 1 | $0.00 | yes |

**644 of 852 retired clips, carrying $3,510.26 or 97.9% of all frozen money, sit on PAST campaigns.** `campaignStatusBlocks` (`tracking.ts:1943`) blocks the earnings path for cron and manual on PAST, and the due-jobs query excludes PAST campaigns outright (`tracking.ts:3575`). **A perfect revival would not earn them one further cent.**

What a revival WOULD do for them is restore **visibility and withdrawability**, which is a real and separate thing: `earnings/route.ts:206` (BL-698 display) and `payouts/route.ts:424` (the per-campaign gate) both exclude retired clips, so that money is currently hidden and unwithdrawable. That is worth having. It is just not "starts earning again", and the owner's framing should be corrected on that point.

**Two further constraints on even that.** BL-657 proved the pool cap **excludes** retired clips, so reviving one puts its earnings back into `spent`; on bees.n.honey ($1,585.17 of a $1,648.35 pool) and STRAENGE ($1,997.56 of $2,000.00) the L1 hard lock would then refuse any increasing write. And BL-627 and BL-539 are explicit that **somesome must stay frozen**, which is 96% of the frozen money on its own.

### The projection, against BL-717's price

| | Figure |
|---|---|
| Retirement rate (BL-717, re-confirmed: 138 clips over 18 days) | **7.67/day = 230/month** |
| Measured revival rate | **1.17%** |
| Revived clips per month | **~2.7** |
| Average recovered per revived approved clip | **$1.40** |
| **Recovered per month** | **~$3.78** |
| **BL-717's schedule cost** | **$13 to $22 per month, forever** |
| **Net** | **minus $9 to minus $18 per month** |

**The schedule costs more every single month than the entire historical recovery of $12.62.** It would pay for itself in month one only if the revival rate were roughly four times higher than measured, on a census with no sampling error.

### Does the measured rate even apply to the post-BL-720 world? Largely NO, and here is the honest answer

**Every clip in this census was retired by the OLD logic**, which retired on a bare 404. BL-720 shipped two hours before this probe ran. Three separate effects, and they do not all point the same way:

**Effect 1, the pool shrinks.** BL-720 requires `MediaNotFound` in the body, an id-matched non-private account, and on the public-account path a 36h persistence wait. Every wrongly-retired clip that the old gate produced from a transient 404 will now simply never be retired. **The future revival pool is strictly smaller than the historical one**, so 1.17% is an **upper bound** on the post-BL-720 rate, and the true forward rate is lower.

**Effect 2, and it cuts the other way.** Would BL-720 have saved these ten? **On a fresh probe today, yes** — all ten return 200, and BL-720's gate short-circuits on a 200 before it ever consults the account. **At their retirement moment, probably not.** Nine sit on an account whose username 404s; if it 404'd then too, BL-720's **path A retires immediately with no persistence wait**. So BL-720 narrows the verdict but does **not** close the specific hole that produced 9 of these 10.

**Effect 3.** BL-720 does nothing about re-checking. Retired clips are still excluded from the poll, so the platform will still never notice a clip that comes back.

**Net: the pilot is measuring a problem that BL-720 has mostly, but not entirely, fixed upstream — and the part it did not fix is a defect in BL-720 itself rather than an argument for a revival schedule.**

---

# PART 4 — the other half of the cost, and a defect this census exposed

### What building it would require

`tracking.ts:3593` sets `videoUnavailable: false` inside `if (!campaignIds)` at `:3583`, so retired clips never enter the cron poll and the auto-restore at `tracking.ts:1729-1746` is unreachable for exactly the clips that need it. **845 of the 852 retired clips still have an `isActive` tracking job** (average `checkIntervalMin` 4,384), so the jobs are alive and only the where-clause holds them out.

| Option | What it touches | Effort | Risk |
|---|---|---|---|
| **(a) New dedicated revival cron** — a route plus a lib modelled on `retire-dead-clips.ts`, one additive nullable `nextRevivalCheckAt` cursor, one scheduler entry | **`tracking.ts` NOT AT ALL** | comparable to `retire-dead-clips.ts` (158 lines pre-BL-720) | **LOW.** Writes three non-money columns on clips currently earning nothing |
| **(b) Relax the exclusion at `tracking.ts:3593`** | **the candidate selection of the cron that writes every clipper's earnings**, in a money file | small diff, large blast radius | **HIGH and asymmetric.** A mistake changes which clips the earnings loop processes platform-wide on every tick, and it re-admits 845 clips at a 4,384-minute cadence, which is precisely the Apify cost problem BL-584 and BL-590 fixed |
| **(c) Reuse the existing targeted path** — a run with `campaignIds` supplied skips the filter at `:3583` | nothing | **zero code, works today** | none, but it is manual, undocumented, per-campaign not per-clip, and re-polls every clip in the campaign |

**If anything is built, it must be (a). Option (b) should be refused outright**: `tracking.ts` is one of the six money files, and no revival feature justifies touching the earnings loop's candidate selection.

### What a revival must do on success

1. **Clear the flag** with the exact three-column write already at `tracking.ts:1743-1746` — `videoUnavailable: false, videoUnavailableSince: null, savedEarnings: null`. **Reuse it; do not author a second one.**
2. **Also clear `goneEvidenceFirstAt`** (new in BL-720), or a revived clip carries stale gone evidence into its next retirement evaluation and skips the persistence wait.
3. **Resume tracking:** automatic, the poll filter keys off the flag.
4. **Restore withdrawability:** automatic, and **with no money write at all**. `earnings/route.ts:206` and `payouts/route.ts:424` key off the same flag, and `retire-dead-clips.ts` deliberately omits the earnings columns from its update, so the stored value was never destroyed.
5. **Resume earning from NOW, never paying twice.** This is structural, not a rule to remember: earnings are `(views / 1000) x cpm` computed off the **current stored view count**, not a sum of deltas, so a clip that was dead for 40 days simply reads its current number on the next tick. `writeClipEarnings` writes an **absolute total**, and a payout permanently subtracts via `clipperLiability` on the payout row, so a revived clip contributes its total exactly once while the prior payout stays subtracted in full. **The single prohibition: the revival path must never compute or credit a delta, a backfill or a catch-up amount. It clears a flag. It does not move money.**
6. **BL-538 never-decrease holds** because the revival write touches no earnings column at all, and the later recompute goes through `writeClipEarnings`, which carries the guard.
7. **BL-543 NULL-never-0 holds** on the condition that a failed re-check writes **no `ClipStat` row** and never `views = 0`.

### THE DEFECT THIS CENSUS FOUND IN BL-720

**BL-720's PATH A retires immediately, with no persistence wait, when `/v2/user/by/username` returns `not_found`, on the reasoning that "the whole account is gone from Instagram, so no human can reach any post on it." This census measured an account for which that reasoning is false.**

Account `cmqgr2yt`: stored username returns **404**, and nine of its posts return **200 with live view counts**. An account cannot serve posts and not exist. **`account not_found` does not mean the account is gone. It can equally mean the clipper renamed it**, leaving `clip_accounts.username` stale.

**How exposed is BL-720 today?** Narrowly, because ordering saves it: the gate checks the media first and returns `keep/alive` on a 200 before the account is ever consulted. So a renamed account whose posts resolve is safe. **The live hole is the combination**: a renamed account **plus** a post that 404s for an unrelated reason, such as the very temporary restriction the 36h wait exists to outlast. That combination retires immediately via path A **with no wait at all**.

**The fix is cheap and belongs in its own round:** before trusting `not_found` on the account, require that **no other clip on the same account resolved 200 in the same run**. The retirement cron already probes clips grouped by account and already caches the account verdict, so the evidence is in hand and the check costs nothing. Failing that, demote path A to the same 36h persistence as path B, which costs one extra day on genuinely dead accounts and closes the hole entirely.

**I am reporting this against a round I shipped two hours ago.** It does not invalidate BL-720 — the private-account fix, the `MediaNotFound` requirement and the fail-open behaviour on every transient are all intact and all still correct — but path A's evidence is weaker than that report claimed, and the correction belongs on the record.

---

# PART 5 — the verdict

## ONE LINE

**Do not build it: the revival rate is 1.17%, the entire historical recovery is $12.62 on nine clips averaging $1.40, all of it on two accounts that came back whole, and BL-717's $13 to $22 a month schedule would cost more every month than everything it could ever have recovered.**

### The numbers behind that, plainly

| | |
|---|---|
| Clips probed | **852, a census, no sampling error** |
| Revived | **10 (1.17%)**, on **2 accounts** |
| Recovered, APPROVED | **$12.62** |
| Frozen in total | $3,583.50 (**0.35% recoverable**) |
| Of which on PAST campaigns that can never earn again | **97.9%** |
| Projected monthly recovery | **~$3.78** |
| BL-717's monthly cost | **$13 to $22, forever** |
| **Net** | **minus $9 to minus $18 per month** |

**The build is not justified by the numbers, and I am not going to justify it anyway.** BL-717 was right to demand this pilot before anything was built, and right to price it: the pilot cost $1.70 and saved a $13-to-$22-a-month commitment.

### If the owner wants revival anyway, the tier design the data justifies is NOT the proposed one

The owner proposed daily to day 30, every 3 days to day 45, then every 7 days to day 365. **The measured data does not support any of those boundaries**, for three reasons: the E bucket (31 to 45 days) contains zero clips so its boundary is untestable; the F bucket (46+ days) shows 0 of 6; and the apparent 15.56% peak in the C bucket is one account's retirement dates, not a time effect.

**What the data does support is an account-level re-check, not a clip-level one.** All 10 revivals were on 2 accounts, and both came back completely. A per-account probe would have caught **10 of 10** revivals for **one call per account**:

| | Per-clip (BL-717) | **Per-account (what the data supports)** |
|---|---|---|
| Unit | 852 clips | **113 accounts** |
| Daily cost | $0.85/day at launch | **$0.113/day** |
| Monthly cost | **$13 to $22** | **~$3.39** |
| Would have caught these 10 | yes | **yes, all 10** |
| Lifetime cost per retired clip | $0.081 | **~$0.011** |

That version costs **$3.39/month against ~$3.78/month recovered**, which is roughly break-even rather than a guaranteed loss. **It is still not a compelling investment**, and I would not build it for the money either. The honest argument for it is not revenue: it is that a clipper whose account comes back should not have to notice, ask, and be told the platform stopped looking. If the owner values that, the account-level version is the one to build, and it is a quarter the price of what was proposed.

**Cheapest option of all, and it needs no code:** BL-720's retirement cron **already fetches account state**, one call per account per run. Recording a `not_found` account that later resolves would surface exactly this event as a by-product of work already being paid for. That is where a revival trigger belongs, if anywhere.

### Recommended order

1. **Fix BL-720's path A rename hole.** Free, small, and it prevents a class of wrong retirement the 36h wait was specifically designed to catch. **Higher value than anything in this report.**
2. **Do not build BL-717's per-clip schedule.**
3. **Consider the account-level re-check only if the owner values the fairness, not the money.**
4. **Correct the framing:** for 97.9% of frozen money a revival restores **visibility and withdrawability**, never future earning, because the campaigns are PAST.

---

## Safety statement

**READ ONLY. One document.** No code, data, config, schema, cron, env flag or money changed. **Nothing revived, nothing retired**, no clip flag altered. Verified after the probe at DB `now()` = 2026-08-05 18:49:04: retired clips **852**, frozen **$3,583.50**, `goneEvidenceFirstAt` non-null **0** — all identical to the pre-probe values, because every script executed `SELECT` only and the provider calls are reads. `git diff --stat -- src prisma` returns **0 lines**; the working tree carries only three new read-only scripts, a log and a results JSON.

**Probes: 1,699 HikerAPI calls, $1.699, against a declared $3.00 cap, every call disclosed and reconciled in the table above.** One call per profile, cached per account, **2 profile calls actually spent**. **No Apify actor ran** and the eleven BL-678 guards are untouched. Every reachable clip was **id-matched by shortcode** against the request per BL-550, and the one place the match initially failed was investigated to root cause rather than reported as a result.

Nothing held by a concurrent round was touched; this round worked in its own worktree on `checkpoint/BL-721`. **A markdown-only round cannot change tsc or the build, so neither was run and neither is claimed.** Clipper handles and account ids are redacted; no wallet address appears. **NO dashes** as bullets.

## What could not be measured

The measured 1.17% is a **lower bound**, because a clip wrongly retired and since genuinely deleted is indistinguishable from a correct retirement today. **When** the ten came back cannot be dated: the platform stores no observation history and both "came back" and "was never gone" present identically. **Bucket E, days 31 to 45, has no data because the population has none**, so any tier boundary there is an assumption. And the rename hypothesis for account `cmqgr2yt` is the parsimonious reading of "username 404s, posts resolve 200", not a directly confirmed fact: confirming it would require finding the account's new handle, which no endpoint the platform uses can do from a stale username.
