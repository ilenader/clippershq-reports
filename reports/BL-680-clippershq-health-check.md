# BL-680 (ClippersHQ) — whole-site health check after a week of heavy change, and the unmerged inventory

> **Filename note, per CONVENTION.md.** `reports/BL-680.md` was already taken by a different project (clipper-finder, *"the clip-library schema, corrected"*). The collision check was run against `origin/main` before pushing and that file was **not** touched. This report is published beside it under the `-<project>-<slug>` suffix the convention prescribes.

## THE SITE IS HEALTHY. Money is sound, every flow is alive, Apify is genuinely dead, and there is NOTHING the owner still needs to merge. Two real defects were found and neither touches money: 10 REJECTED clips carry a stale `baseEarnings` residue that violates the stated invariant while paying nothing, and the Instagram half of the caption pipeline is delivering nothing at all (0 of 11 organic Instagram shadow rows carry a caption, against 7 of 8 on TikTok). Three open items grew and are listed in PART 5.

**2026-07-29 · AUDIT ONLY. READ ONLY on code, data, config and money. Nothing changed, nothing fixed, nothing built. `agency-monitor --fix` and all repair SQL never run, no owner row re-derived, no Apify key restored, NO Apify actor run.**
**Base** origin/main `fdde504f` · **Branch** `checkpoint/BL-680` · **Worktree** `C:/b680` (short path, `node_modules` never junctioned)
**DB `now()` at query time: 2026-07-29 17:41:30.072627+00.** Every timestamp below is cast to `::text` and read against that clock, never a local one.

---

## PART 0 — the unmerged inventory

**61 checkpoint branches on origin are genuinely not ancestors of `main`.** Classified by what their diff actually contains, ignoring `BACKLOG.md`:

| kind | count | meaning |
| --- | --- | --- |
| **DOCS** | 54 | audit rounds whose only output was a markdown file |
| **BACKLOG-ONLY** | 4 | `BL-437`, `BL-565`, `BL-584`, `BL-649`; nothing outside BACKLOG |
| **CODE** | 3 | `BL-351`, `BL-493`, `BL-524` |

### BL-676: MERGED. Confirmed.

**The suspicion is out of date.** `checkpoint/BL-676` @ `d169d7db` (the campaign-refusal blank-screen fix) **is** an ancestor of `main`: it was merged by BL-679 as merge commit `fdde504f`, alongside `checkpoint/BL-678` @ `3940e290` as `381d080c`. Both are on `main` and deployed. Nothing about the refusal panel or the Apify guard is outstanding.

### The three code branches, and why none of them should be merged

| branch | SHA | date | what it does | verdict |
| --- | --- | --- | --- | --- |
| `checkpoint/BL-351` | `e436f5ee` | 2026-07-11 | clip-card polish, re-hosted thumbnails, `clip-thumbnail.ts` | **SUPERSEDED.** `src/lib/clip-thumbnail.ts` and `api/clips/[id]/thumbnail/route.ts` are both on `main` already and carry the BL-350 markers. The work landed by another route. |
| `checkpoint/BL-493` | `5cbfc740` | 2026-07-14 | owner growth transparency, `/admin/growth` catalog | **SUPERSEDED, and `main` says so in writing.** `api/admin/growth/catalog/route.ts:6` on `main` reads *"BL-493 built it but it was never merged"* and BL-499 reimplemented it through `growth/catalog-preview`. Merging BL-493 would add a second, duplicate catalog. |
| `checkpoint/BL-524` | `8fc8a331` | 2026-07-16 | growth dashboard wording and truthfulness | **STALE AND DIVERGENT. Do not merge as is.** Its `admin/growth/page.tsx` carries markers up to BL-524 but not BL-573; `main`'s carries BL-573 but not BL-524. `main` is 13 days newer on that file. Merging would drag BL-573's work backwards. |

### Plainly: is there anything left to merge, and does it matter?

**No, and no.** Every branch carrying code is either already on `main` by another route or is older than the file it would overwrite. The other 58 are audit documents and BACKLOG notes whose value is already published in `ilenader/clippershq-reports`. **The owner has nothing to merge and nothing is at risk from leaving these branches where they are.** They are worth deleting one day purely as tidiness, and that is a preference, not a fix.

---

## PART 1 — is the money still right?

Re-measured from scratch across the **full** clip population, not inherited from BL-679.

### The earnings invariant

| status | clips | violations | max drift | total earnings |
| --- | --- | --- | --- | --- |
| APPROVED | 3488 | **0** | $0.0100 | $9,834.08 |
| PENDING | 64 | 0 | $0.0000 | $0.00 |
| FLAGGED | 6 | 0 | $0.0000 | $113.50 |
| **REJECTED** | 848 | **10** | **$17.02** | $0.00 |

**BL-679's finding is independently confirmed and widened:** it measured 2,905 APPROVED clips (its filter excluded `videoUnavailable`); across all **3,488** APPROVED clips there are still **zero** violations, with the worst drift exactly at the $0.01 tolerance boundary.

**The 10 REJECTED violations are a real defect, and they are not a money leak.** Every one has `earnings = 0.00`, which is the field that pays. What survived is the residue: `baseEarnings` totalling **$50.15** and `bonusAmount` totalling **$0.55** were not cleared when the clips were rejected, so `earnings ≈ baseEarnings + bonusAmount` fails on those rows. **Not a new regression:** the newest is `2026-07-22 16:50:30`, the oldest `2026-06-24 16:31:21`, so none of this week's changes caused it. Impact is data hygiene and any future query that trusts `baseEarnings` on a rejected row.

### Budget, the never-decrease guard, and view regressions

* **No campaign is over budget.** 17 campaigns carry spend; **0** exceed their budget, and the closest is **$1,002.44 of headroom** away from it.
* **The never-decrease guard holds.** Across all 3,488 APPROVED clips: **0** negative `earnings`, `baseEarnings` or `bonusAmount`; **0** clips whose `earnings` sits below their `savedEarnings` watermark; 100 deliberately frozen.
* **Stored views that fell to 0 from a positive prior value: 59 in 7 days**, and they carry **$0.00 of earnings between them**. 58 are YouTube clips whose prior value was **1 or 2 views**; the remaining one is a TikTok clip with a prior 531, last seen `2026-07-27 06:02:35`. **None since the 2026-07-29 deploy.** This is platform reporting jitter on effectively unwatched clips, not a measurement being destroyed.
* **Total earnings only rise.** $9,834.08 across all APPROVED clips now. During this audit window alone the figure was watched moving from $6,257.84 to $6,265.56 on the narrower `videoUnavailable = false` population, upward, with the invariant holding at both readings.

---

## PART 2 — is every flow alive?

| flow | status | evidence |
| --- | --- | --- |
| Tracking cron | **WORKING** | 9 consecutive hourly ticks, each firing at `:01`, 89 to 104 distinct clips per tick, newest `2026-07-29 17:11:28`. All three platforms in the newest tick: instagram 54, tiktok 37, youtube 7. **Zero rows written as 0** in the last four ticks. |
| CLIPS_PER_TICK = 90 | **WORKING, and proven from behaviour** | `clipsPerTick()` in `tracking.ts:160` returns **30** when the env is absent or invalid. Observed distinct clips per tick: 89, 91, 91, 98, 98, 102, 104, 104. Sustained collection three times the fall-back cap is only possible if the env value is reaching the tracking service's own process, which is exactly the question BL-633 raised. The Railway variable itself cannot be read from here, so this is inference from behaviour, but it is decisive inference. |
| Verification, Instagram | **WORKING**, probed live | HikerAPI profile read returned `ok=true` with a bio present (36 chars, redacted) and a follower count. 37 real verifications on `hikerapi-ig-profile`, newest `2026-07-29 10:58:32`. |
| Verification, TikTok | **WORKING** | 13 real verifications on `lamatok-profile`, newest `2026-07-29 10:04:41`. The live probe returned `ok=true` but no bio for the public account chosen, which is a property of that account, not a provider failure. |
| Verification, YouTube | **WORKING in production, NOT probed** | 26 real verifications on `tier-1`, newest `2026-07-29 10:19:10`. The live probe could not exercise it: this machine's `.env.local` has no `YOUTUBE_API_KEY`, so the probe returned `no YOUTUBE_API_KEY`. That is a limit of the probe, not a production fault, and it is stated rather than papered over. |
| Verification, the Apify tier | **INERT, by design** | Probed live: `tiktokTier2` returns `{ found: false, transient: true, error: "apify hard off (BL-678)" }` and starts no actor. `transient` is the correct signal, so the cascade falls through and no clipper is blocked. |
| Clip submission | **WORKING**, all three | Since `2026-07-29 13:15`: tiktok 5, youtube 2, instagram 1. Across 7 days: instagram 171, tiktok 58, youtube 39. |
| Tracking cron heartbeat | **WORKING** | `cron_runs` kind `tracking`: 71 fires in 12 hours, newest `2026-07-29 17:40:15`. |
| Lifecycle cron | **WORKING** | 48 fires in 12 hours, newest `2026-07-29 17:45:20`. |
| Watchdog | **WORKING** | 24 fires in 12 hours, newest `2026-07-29 17:30:21`. |
| retire-dead-clips | **WORKING, evidenced by effect** | It writes no `cron_runs` row, so there is no heartbeat to read. 41 clips retired in the last 7 days, newest `2026-07-29 06:03:08`, out of 770 lifetime. |
| All four on bearer-only auth | **CONFIRMED** | Live (non-comment) `x-vercel-cron` reads anywhere in `src/`: **0**. The five remaining occurrences are all comments recording the BL-658 removal. `CRON_SECRET` is referenced 4, 4, 5 and 3 times in tracking, lifecycle, watchdog and retire-dead-clips respectively. |
| Growth engine | **WORKING, well inside any cap** | `email_events` over 7 days: 4 to 10 events a day across 2 to 8 distinct users. Newest day 07-29 with 4 events to 3 users. Nothing resembling a burst. |
| Reviewer note layer | **WORKING and clipper-unreachable** | `ReviewerNoteCard` is mounted in the admin clip queue at `admin/clips/page.tsx:1908` and fetches `/api/admin/reviewer-note/[clipId]`, which is gated by `requireOwnerOrCapability("CLIP_VIEW")` under `/api/admin/*`. **208 of 222** shadow rows carry a composed `noteJson`. Re-grepped: the only readers are that admin route and the submit-path writer. No clipper-facing route reaches a note. |
| Auto-reject | **OFF** | `isAutoRejectLive()` has exactly one call site, `api/clips/route.ts:977`, where it only stamps the shadow row. **0 of 222** rows, all time, have `autoRejectLive = true`. |

### The two questions earlier rounds could not answer

**`rule_shadow_decisions` IS now recording `captionPresent` true on TikTok. BL-669's gap is closed.** Organic live-submit rows since BL-668 merged at 09:58 UTC:

| platform | rows | captionPresent | soundIdPresent | hashtags | note composed | newest |
| --- | --- | --- | --- | --- | --- | --- |
| **tiktok** | 8 | **7** | **7** | **7** | 8 | 2026-07-29 13:37:12 |
| instagram | 11 | **0** | **0** | **0** | 11 | 2026-07-29 16:41:10 |
| youtube | 3 | 0 | 0 | 0 | 3 | 2026-07-29 13:52:15 |

TikTok delivers, 7 of 8. **Instagram delivers nothing: 0 of 11.** BL-668 disclosed that it could not re-probe the Instagram key path live because Apify actor runs were forbidden, and inferred the fix from BL-665's earlier probe. That inference is now measurably wrong in practice, or the Instagram submit path is not reaching the extractor at all. This is the most substantive new finding in this audit and it is ranked in PART 6.

**Instagram cover capture is WORKING. BL-675's gap is closed.** Of the **16** Instagram clips created since BL-675 merged, **16 have a cover and all 16 are Supabase-hosted**, newest `2026-07-29 17:07:55`. A live HEAD on the newest cover returned **HTTP 206 with `content-type: image/jpeg`** and real bytes (206 rather than 200 only because the probe sent a Range header to keep the transfer small). All 796 Instagram covers in the table now sit on the Supabase storage host; not one points at an expiring CDN URL.

---

## PART 3 — is Apify genuinely dead?

**Yes, on both independent sources.**

**Apify's own free run-log** (`GET /v2/actor-runs`, a metadata read; no actor started): the newest run in the account is **`2026-07-29T10:48:41Z`**, which is BL-673's second local run. **No run since**, and none at all in the 7 hours since the BL-678 guard deployed at 13:11 UTC. Against BL-677's baseline of **nine** post-cutover runs (seven from BL-665 on 07-24, two from BL-673 on 07-29), the count is **still nine. Zero new runs.** The `total: 17253` retained figure is not a lifetime counter and is not used as one, per BL-677's own correction.

**The internal ledger** (`apify_usage_entries`, `provider LIKE 'actor:apify%'`) today:

| hour (UTC) | attempts |
| --- | --- |
| 07:00 to 10:00 | 205, 321, 248, 276 |
| 11:00 | 8 |
| 12:00 | 3 |
| **13:00 (guard deployed 13:11) through 17:00** | **no rows at all** |

Since 13:11 the ledger records only the alternatives: `hikerapi-instagram-only`, `lamatok-tiktok-only`, `youtube-api-batch`, `fanout:instagram`, `fanout:tiktok`. **Not one `actor:apify*` row.**

**The honest caveat, repeated from BL-679 because it still applies:** BL-673's earlier deploy had already cut the rate from 276 an hour to 3 before the guard shipped, so the ledger alone cannot separate "the guard works" from "the traffic had already stopped". **The decisive evidence is the harness**, which sets a valid-looking key, stubs `fetch` with a no-I/O recorder, drives the real entry points and records **zero requests to any apify.com host**, 28 of 28 assertions passing on the merged tree. Re-confirmed live in this audit: with a working key present in this environment, `tiktokTier2` still returned `apify hard off (BL-678)` without starting an actor.

**No path can construct a request even with a key present.** `APIFY_HARD_OFF` is `const true`, reads no environment variable and imports nothing. All 11 request paths are guarded: five early returns in `apify.ts` before `getApiKey()`, four covered by the single `apifyCredential()` chokepoint in `apidojo.ts`, one each in `account-profile.ts` and `verify-cascade.ts`. The only surviving live `process.env.APIFY_API_KEY` read is inside `getApiKey()` itself, which all five of its callers now return before reaching.

---

## PART 4 — what the recent changes did to the numbers

| check | result |
| --- | --- |
| somesome reads 100% to clippers | **CONFIRMED.** `test-bl-641`: **19 passed, 0 failed**. A clipper sees `$9,750.00 of $9,750.00 = 100%`, live and when forced through PAST and COMPLETED. |
| the owner still sees the true figure | **CONFIRMED.** Owner and admin see `$5,370.12 of $9,750.00`, headroom **$4,379.88**. The control campaign still displays its real `$871.26` while not finished, so BL-535's property holds. |
| the daily counter counts UP | **CONFIRMED.** `MomentumCard.tsx` renders `"{n} day streak"` and `"{n} more days to a +X% streak bonus"`; the number rises as the streak grows. |
| the ghost-fee pool cap leaves NULL-fee campaigns untouched | **CONFIRMED, and it currently touches nothing at all.** All **31** campaigns, holding $53,988.00 of budget, have `platformFeePctDecimal = NULL`, which `balance.ts:304` routes down the pre-BL-630 path. The cap is shipped and inert until a fee is set on some campaign. |
| drag-scroll on both surfaces | **CONFIRMED.** `preview-campaign-row.tsx:40` and `CampaignsRedesign.tsx:25` both import `useDragScroll` from the one shared module on current `main`. |
| earnings page renders balances even if the chart chunk fails | **CONFIRMED.** `EarningsChart.tsx:3` loads its recharts body through `next/dynamic` with a `.catch` its own comment marks as *"LOAD-BEARING, NOT DEFENSIVE DRESSING"*, so a failed chart chunk cannot take the page's balances down with it. |

---

## PART 5 — the open items, re-measured

| item | prior | now | verdict |
| --- | --- | --- | --- |
| Visible-but-unwithdrawable (BL-661's $390.60 across 24 clippers) | 24 clippers, 323 gone clips, $1,774.74 raw | **28 clippers, 468 gone clips, $3,543.68 raw** | **GROWN.** +4 clippers and +145 gone clips in five days, roughly +45% on the clip count. **The exact payable figure was NOT re-derived**, because reproducing it requires replicating `computeBalance`'s paid-and-locked subtraction per clipper and an approximation would be worse than saying so. The underlying population has clearly grown, therefore so has the stuck total. |
| Post-withdrawal over-hold (BL-627's $142.59 across 5) | 5 clippers, $142.59 | **could not be reproduced** | **UNRESOLVED MEASUREMENT.** Gross PAID versus lifetime APPROVED earnings gives **12 clippers, $1,103.36**, which does not reconcile to either of BL-627's two published figures ($142.59 all-time, or $3,285.21 approved-live). The most likely cause is a definitional difference: BL-627's all-time basis may include clips no longer in the table, and it may have compared net rather than gross. **Stated as unreproduced rather than reported as an eightfold growth**, which would be an artefact of my definition, not a fact. |
| Stale UNDER_REVIEW payouts | 3, aged 24 to 47 days | **3, $166.45, oldest now 55 days** (`2026-06-05 01:06:42`) | **UNCHANGED in count, GROWN in age.** Still reserved and unpaid, so no money moved. Ops backlog. |
| FLAGGED phantom | 6 clips, $113.50 clipper + $92.17 owner | **6 clips, $113.50 clipper** | **UNCHANGED.** Exact to the cent. The clipper side is still bucketed out of withdrawable balance. The $92.17 owner side sits on agency rows this audit did not re-derive, deliberately, because re-deriving owner rows was forbidden. |
| force-recalc raw-campaign caps bug | live, latent | **still live** | **UNCHANGED.** Admin-manual path only. |
| PWA predicate mismatch | live, latent | **still live** | **UNCHANGED.** Latent. |
| 52 unencrypted wallet rows | 52, owner declined the backfill | **exactly 52 plaintext-only, 88 encrypted, 140 total** | **UNCHANGED, and the forward path works.** New rows are being encrypted: the newest row overall is `2026-07-29 16:37:34`, and the plaintext count has not moved. The owner's decision stands and is not eroding. |

---

## PART 6 — the verdict

### ONE LINE

**The site is healthy: money is provably sound, every flow is alive, Apify is dead on two independent sources, nothing needs merging, and the only new defects are an Instagram caption pipeline that delivers nothing and ten rejected clips carrying a harmless stale residue.**

### MUST BE FIXED

| # | finding | impact | confidence | next step |
| --- | --- | --- | --- | --- |
| 1 | **Instagram captions and sound ids reach the evaluator 0 times out of 11** organic shadow rows since BL-668, against 7 of 8 on TikTok | the reviewer note is blind on the platform with the most submissions (171 in 7 days versus 58 TikTok); no money effect | **high**, measured on organic rows | trace whether the IG submit path reaches `extractClipMetadata` at all, then re-probe the `musicInfo.audio_id` key path that BL-668 could only infer |
| 2 | **3 UNDER_REVIEW payouts now 55 days old**, $166.45 | clipper money reserved and unpaid for nearly two months | **high** | ops: process or void |
| 3 | **Visible-but-unwithdrawable grew to 28 clippers and 468 gone clips** | clippers see more than the withdrawal page will release, and the gap widens weekly | **high** on the growth, **not measured** on the exact dollar figure | decide the gone-clip display rule; the two screens disagree by design |

### CAN WAIT

| # | finding | impact | confidence | next step |
| --- | --- | --- | --- | --- |
| 4 | 10 REJECTED clips violate the earnings invariant ($50.15 base, $0.55 bonus residue, all with `earnings = 0`) | none on payouts; pollutes any query trusting `baseEarnings` on a rejected row | **high** | clear base and bonus on rejection, or document the residue |
| 5 | 58 YouTube clips wrote a 0 over a prior 1 or 2 views in 7 days | none, $0 earnings on all | **high** | decide whether the YouTube API genuinely reported 0 or a miss is being coerced |
| 6 | force-recalc raw-campaign caps bug, PWA predicate mismatch | latent mis-pricing on an admin-manual recompute | **high**, carried from BL-617 | build a `campaignForCalc` snapshot before recompute |
| 7 | $92.17 FLAGGED owner phantom | owner over-accrued | **high**, unchanged | owner ruling on flagged-clip policy |
| 8 | 52 plaintext wallet rows | legacy exposure, not growing | **high** | none; the owner declined, and new rows are encrypted |
| 9 | 61 unmerged branches | none | **high** | optional tidy-up; nothing to merge |

### What could NOT be verified, and why

* **YouTube verification was not probed live**, because this machine's `.env.local` carries no `YOUTUBE_API_KEY`. Production's 26 successful `tier-1` verifications, newest `2026-07-29 10:19:10`, are the evidence instead.
* **`CLIPS_PER_TICK` was not read from Railway.** The environment cannot be read from here. The conclusion rests on behaviour: sustained collection of 89 to 104 clips per tick against a 30-clip fall-back.
* **BL-627's $142.59 over-hold could not be reproduced** under any definition I could reconstruct from the published report. Reported as unreproduced, not as grown.
* **The exact $390.60 payable figure was not re-derived**, because it needs `computeBalance` replicated per clipper.
* **The $92.17 FLAGGED owner phantom was not re-measured**, because re-deriving owner rows was explicitly forbidden this round.

---

## Safety and probe disclosure

READ ONLY. One document. No code, data, schema, config or money change; nothing fixed, nothing built, and **no build is claimed** because a markdown-only diff cannot change tsc or the build. `agency-monitor --fix` and all repair SQL were never run. No owner row was re-derived. No Apify key was restored, set or printed. **NO Apify actor was run.**

**Every probe, disclosed with its cost:**

| probe | calls | cost |
| --- | --- | --- |
| Apify `GET /v2/actor-runs` | 1 | free metadata read, no actor started |
| Apify `GET /v2/users/me/usage/monthly` | 1 | free; returned an unexpected shape and its figures were therefore NOT used |
| HikerAPI profile read, one public non-clipper account | 1 | one profile call |
| LamaTok profile read, one public non-clipper account | 1 | one profile call |
| `verify-cascade` TikTok tier 2 and YouTube tier 2 | 1 each | no network: the Apify tier is guarded, the YouTube tier returned before calling |
| HTTP HEAD on one Supabase-hosted cover, ranged to 2 KB | 1 | free |
| `test-bl-641-finished-campaign-display.ts` | 1 run | read-only DB, no provider calls |
| read-only DB `SELECT`s via `scripts/run-select.js` | ~30 | free |

**ONE CALL PER PROFILE was respected.** The two profile probes used well known public accounts, deliberately not any clipper's account, so no real user was probed. No clipper handle, email or caption appears anywhere in this document; the one bio read is reported as a character count. Counting was done with `grep -c` and `wc -l` on whole files, never through `head`. Nothing held by a live round was touched. NO dashes used as bullets.
