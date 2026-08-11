# BL-770 — the pilot still could not run, but the replacement question is answered without it

**NO API KEY WAS SUPPLIED, so no live fetch happened and all nine fields remain UNTESTED.** The round
brief said the owner would supply the key; `.env` and `.env.local` contain no bundle.social variable,
and per the brief I asked rather than hunting for credentials. **PART 1 is reported as unrun, not as a
pass.**

**But the owner's real question, whether this could replace LamaTok, needs no vendor key, and the
answer is no. It is also based on a premise this round found to be wrong.**

**2026-08-11 · READ ONLY on the codebase.** No code, config, schema or data changed. **Nothing was
signed up for, no payment details entered, no credential stored, no TikTok account authorized, and no
key exists to log.** Base `origin/main` @ `9d285c8c`, isolated worktree `C:/m770`, removed at exit,
`node_modules` never junctioned.

**Gates, run honestly on a tree whose only change is a BACKLOG entry:** `NPMCI_EXIT=0`, eslint
**PRESENT**, `PRISMA_EXIT=0`, `TSC_EXIT=0` with **0 errors**, **`BUILD_EXIT=0`**, hooks
`HOOKS_EXIT=0` at **0 errors, 11 warnings**. The 6 money files plus `campaign-era.ts` are
**byte-identical by blob OID** against `origin/main`; BL-678 markers 27, unchanged.

---

## THE ANSWER, BEFORE THE WORKING

> **bundle.social cannot replace LamaTok, and the saving the question assumes does not exist.**
>
> **The premise is wrong.** The brief says the owner "currently pays LamaTok per call". **He does
> not.** The repository's own cost ledger puts `lamatok-tiktok-only` in the zero-cost set, and states
> the reason in its own words: *"Both vendors bill from a prepaid request quota rather than per-call
> dollars (BL-550 measured both balances unchanged across 2,153 Hiker + 407 LamaTok requests)."*
> **Switching LamaTok off saves no per-call money, because there is none.**
>
> **And it could not be switched off anyway.** bundle.social sees only connected creators; LamaTok sees
> every clip. **Today zero clippers are connected, so switching LamaTok off would lose tracking on
> 100% of TikTok clips**, and tracking drives earnings, so those clips would simply stop earning.
>
> **The one genuinely good number:** TikTok clips are highly concentrated. **The top 10 of 42 TikTok
> clippers account for 71% of TikTok clips, and the top 20 for 88.4%.** So an analytics pilot needs a
> handful of willing clippers, not 1,240. **That is an argument for adding depth cheaply, never for
> removing LamaTok.**

---

## PART 1 — THE LIVE FETCH: NOT RUN

**No key, so no call was made.** Every one of the nine fields is **UNTESTED**. The field-survival-by-age
table, which is the deliverable that decides the capture design, **could not be produced**.

For the record, the nine fields BL-768 read from
[info.bundle.social/api-reference/platforms/tiktok.md](https://info.bundle.social/api-reference/platforms/tiktok.md),
each **UNTESTED**: `average_time_watched`, `full_video_watched_rate`, `total_time_watched`, `reach`,
`impression_sources`, `audience_genders`, `audience_countries` (video level); `audience_ages`,
`audience_cities`, and `profile_views` inside the daily `metrics` array (account level).

**`video_view_retention` remains absent from bundle.social's published payload and present on TikTok's
side**, scope `video.insights`, *"Data source: TikTok Studio"* (BL-769, TikTok doc_id
`1762228421622786`). **Whether bundle.social exposes it under another name inside the untyped `raw`
object is UNVERIFIED and can only be settled by a live call**, because its OpenAPI spec types that
field as a generic passthrough with no schema.

**What the owner must send for BL-771 to run:** the bundle.social API key, placed in `.env.local` as
`BUNDLE_SOCIAL_API_KEY`, plus confirmation that one TikTok account is connected and that **"Turn On"
has been tapped in that account's TikTok app**. **Do not paste the key into chat.**

---

## PART 2 — COULD THIS REPLACE LamaTok? NO, AND HERE IS THE ARITHMETIC

### What the tracking tick actually needs

From `lamatok.ts:303`, the tick consumes a `ClipStats` of exactly:
`{ views, likes, comments, shares, createdAt, platform }`. **bundle.social's documented TikTok post
payload carries `video_views`, `likes`, `comments`, `shares` and `create_time`, so on shape alone it
could feed the tick** for a connected creator. Shape is not the obstacle.

### The obstacle is coverage, and it is absolute

**bundle.social returns data only for accounts that have completed OAuth. LamaTok resolves any public
TikTok URL with no creator involvement at all.** That difference is not a tuning parameter.

Measured over the last 30 days:

| | |
|---|---|
| Clips, all platforms | **1,701** |
| TikTok clips | **310**, 18.2% |
| Clippers who posted a TikTok clip | **42** |
| **Clippers currently connected to bundle.social** | **0** |

**If LamaTok were switched off today, 100% of TikTok clips would lose view tracking**, and because
earnings are computed from views, those clips would stop earning. **This is a money outage, not a
degraded feature.**

**Concentration, which is the encouraging part:**

| If this many TikTok clippers connect | TikTok clips covered | TikTok clips still needing LamaTok |
|---|---|---|
| Top 5 | **55.2%** | 44.8% |
| Top 10 | **71.0%** | 29.0% |
| Top 20 | **88.4%** | 11.6% |
| Top 30 | **95.2%** | 4.8% |
| All 42 | 100% of today's cohort | **still non-zero tomorrow** |

**Even at 95% coverage LamaTok must stay**, because the residual is real clips owed real money, and
because new clippers join continuously and post before they connect anything. **There is no adoption
level at which LamaTok can be removed**, only levels at which it does less work. **And since LamaTok
bills from a quota rather than per call, doing less work saves nothing.**

### What the $100 plan actually gives him, ignoring the parts he does not want

Stripping out posting, calendar, link-in-bio and comment import, the relevant contents of **Pro at
$100/month** ([pricing](https://bundle.social/pricing)) are: **API access; unlimited connected social
accounts; analytics included with no separate metering; a 24-hour automatic analytics refresh; and
force-refresh at `teams x 5` per day** ([analytics
doc](https://info.bundle.social/api-reference/analytics.md)).

**One caveat that could matter more than the price:** analytics are **deleted after 30 days**, and
imports are capped at **100 posts per month on Pro**, with ongoing refresh for imported posts requiring
contact where *"Additional platform usage fees may apply"*. **Imported posts are the owner's actual
case**, since clippers post natively rather than through the tool, so **the 100/month import cap sits
directly under his 310 TikTok clips a month**. **UNVERIFIED whether analytics-only reads count against
that cap**, and it is the single most important commercial question for the live test.

### The honest summary

**This is additive, permanently.** It buys analytics depth on connected clippers. **It buys no saving,
removes no vendor, and reduces no bill.** Any plan that assumes otherwise is built on the per-call
premise this round disproved.

---

## PART 3 — THE CAPTURE-EARLY DESIGN, SPECIFIED

BL-769 established from TikTok's own docs that `reach`, `full_video_watched_rate`,
`total_time_watched`, `average_time_watched`, `impression_sources` and `audience_countries` become
unavailable once a clip has had **no view, like, comment or share for more than 7 days**.

**The design that follows, specified but not built:**

* **Fetch first at roughly 48 hours after submission**, which respects TikTok's own 24 to 48 hour
  latency for offline fields. Earlier than that returns nulls for the fields that matter.
* **Refresh daily while the clip is still growing**, which the vendor's automatic 24-hour cycle does
  for free without consuming force-refresh quota.
* **Stop refreshing at 7 days of flat views**, because that is the point past which the six fields
  expire anyway and further calls buy nothing.
* **Store every fetch in the platform's own tables**, additive and nullable. This is mandatory rather
  than optional: bundle.social deletes analytics after 30 days, so anything not persisted is gone.
* **Read the stored copy at payout time.** Never fetch fresh at payout, which was BL-768's design and
  is the one moment the data is least likely to exist.

**The owner's specific worry, honestly unresolved.** Does a clip that goes quiet and then suddenly
takes 100,000 views get its expired fields back? **UNVERIFIED, and it could not be tested without a
connected account.** TikTok's own wording is suggestive but not conclusive: it says that to retrieve
the fields *"you can view/like/comment/share the inactive video and retry after 24 ~ 48h"*, which
implies renewed activity **does** restore them. **If that holds, a viral revival repopulates the
fields and the capture-early design has a safety net. If it does not, the fields are lost for good.**
This is the second thing BL-771 must test.

**A trap the owner must not fall into:** TikTok's suggested remedy is to interact with the inactive
video. **The platform must never do that on clips it pays for.** Manufacturing engagement on content
being assessed for genuine engagement corrupts the measurement and would be indefensible if noticed.

**Rate limits against his volume:** 310 TikTok clips a month is about 10 a day. The 24-hour automatic
refresh covers steady state at no quota cost. Force refresh at `teams x 5` per day gives 5 a day on one
team, 15 on three, which is ample for exceptions. **The flat $100 does not hide a per-call ceiling on
analytics reads. The ceiling that does exist is the 100-post monthly import cap**, and whether it binds
here is UNVERIFIED.

---

## PART 4 — WHAT THE CLIPPER EXPERIENCES

**Not observed, because no connection was made. Everything here is documentation, marked as such.**

bundle.social documents *"Connect a TikTok creator or business account via the OAuth connect URL
flow"* ([source](https://bundle.social/tiktok-audience-demographics)). **Whether the final screen is
served by tiktok.com, and what permissions it names, is UNVERIFIED and is the third thing BL-771 must
capture**, ideally as a screenshot. It matters more than any field: an OAuth connect URL is
structurally unlike TikHub's pasted session cookie, but "unlike credential capture" is not the same as
"TikTok's own consent screen".

**The friction that is certain regardless of vendor**, from TikTok's own rules and BL-767:

* **Each creator must enable analytics themselves in the TikTok app.** The setting lives under
  **Profile, then the menu, then TikTok Studio or Creator Tools, then Analytics, then "Turn On"**.
  Exact wording varies by app version, so the owner should screenshot his own before writing
  instructions. **It cannot be done for them, and without it the endpoints return nothing.**
* **`profile_views` is Business-Account-only.**
* **Audience demographics need 100+ followers.** Many of the owner's clippers are small, so **a
  meaningful share will connect successfully and correctly see no demographics.** The product must
  present that as normal, not as an error.

**On completion likelihood, stated plainly:** this is a multi-step flow ending in an in-app settings
change most people have never opened. **Assume a low completion rate across 1,240 clippers.** The
concentration data in PART 2 is what rescues it: **the owner does not need 1,240, he needs about 10 to
cover 71% of TikTok clips**, and those ten can be asked personally.

---

## PART 5 — WHAT THE DATA COULD PROVE, WITHIN THE TERMS

BL-769 verified the line from TikTok's own docs: **per-clip, per-clipper, shown to a human reviewer is
defensible; aggregating creators into peer bands for ranking or discovery is prohibited verbatim.**
Nothing below aggregates creators, and **no scoring system is designed here.**

**Fields that would genuinely discriminate, if they arrive:**

* **`impression_sources`** is the strongest, because the buyer of views does not control attribution.
  Large views with almost no For You share is an anomaly that is hard to manufacture.
* **`average_time_watched` against video duration, and `full_video_watched_rate`.** Bought views are
  typically brief; high views with very low watch time is the classic shape.
* **`audience_countries` against the campaign's target market**, as a soft signal only, since genuine
  reach travels.

**What it cannot do, bluntly:**

* **None of it proves fraud.** It produces anomaly, and anomalous is not guilty.
* **There is no baseline, and the obvious way to build one is the prohibited one.** Knowing what a
  normal `impression_sources` mix looks like requires comparing across clippers. **That tension is
  real and unresolved**, and the only clean route is comparing a clipper against **their own** history
  rather than against peers.
* **The bar is very high.** R-5 proved the existing `fraudScore` has **zero predictive power**, and
  BL-664 measured human reviewers at a **0.77% overturn rate**. **A signal that merely looks clever is
  not an improvement on a process already working**; the test is whether it beats 0.77%.
* **Coverage is under a fifth.** TikTok is 18.2% of clips, so this can never be the main defence.

**Nothing here could auto-reject**, structurally rather than by promise: no code exists (PART 6).
BL-518 and BL-521 stand, and the constraint carried forward is that any signal **ranks for a human,
never decides, and no clipper ever sees a machine's suspicion.**

---

## PART 6 — WIRE NOTHING, PROVEN

```
grep -rIl -i 'bundle.social|bundlesocial|BUNDLE_SOCIAL' src/ prisma/ scripts/  -> 0 files
grep -rIl -i 'ayrshare'                                 src/ prisma/ scripts/  -> 0 files
```

**No vendor code exists.** Nothing touches tracking, earnings, the reviewer note, bot detection,
payouts or the submit path. No clipper-facing surface can reach what is not there. No schema change, no
`prisma migrate`, no Apify actor run.

**The 6 money files plus `campaign-era.ts` are byte-identical by blob OID** against `origin/main`.
**BL-678 markers: 27, unchanged.** No clip's earnings or status changed; no payout touched. **The only
file in this branch's diff is `BACKLOG.md`.**

---

## PART 7 — THE VERDICT

> ## **Zero of the nine fields arrived, at any clip age, because no API key was supplied. And the replacement question is settled without one: bundle.social cannot replace LamaTok at any adoption level, and the per-call saving the question assumes does not exist, because LamaTok bills from a prepaid quota. At $100 a month this is worth it only as added analytics depth on a handful of high-volume clippers, never as a substitution.**

**Where reality differs from the documentation reading, which is the pattern of this whole line of
rounds:**

* **BL-768 costed an on-demand payout-time fetch. BL-769 showed six of nine fields expire first.
  This round shows the vendor deletes everything after 30 days anyway.** Both push the same way:
  **capture early, store it yourself.**
* **The premise that LamaTok is billed per call is wrong**, and it came into the brief rather than
  from the code. **The repository's own ledger says $0 and explains why.** Any business case resting on
  that saving should be discarded.
* **A new commercial risk appeared that no prior round noticed:** the **100-post monthly import cap on
  Pro**, sitting directly under 310 TikTok clips a month. **UNVERIFIED whether analytics reads count
  against it**, and if they do, the flat $100 is not flat for this use.

**Nothing here has cost the owner anything, and that remains the point.**

### The next round, precisely

**BL-771 is the same pilot, and it needs exactly three things from the owner before it can start:**

1. **The bundle.social API key** in `.env.local` as `BUNDLE_SOCIAL_API_KEY`, not pasted into chat.
2. **One TikTok account connected**, with **"Turn On" tapped** in that account's TikTok app.
3. **Three post URLs or ids from that account**: one from the last day or two, one about a week old,
   and one over a month old.

**It should then answer four questions in one session:**

* **Which of the nine fields return real values at each of the three ages?** A documented field
  returning null is a finding, not a pass. This produces the survival-by-age table this round could
  not.
* **Does a clip that went quiet and then got fresh engagement regain its expired fields?** The owner's
  own worry, and the safety net of the capture-early design depends on it.
* **Is the consent screen served by tiktok.com, and what does it say?** One screenshot.
* **Do analytics reads count against the 100-post monthly import cap?** The commercial question.

**Stop conditions stand:** stop if fields arrive null, stop if the consent screen is not TikTok's, and
**do not propose removing LamaTok under any result**, because PART 2 settles that independently of what
the fields turn out to be.

---

## WHAT COULD NOT BE ESTABLISHED

* **All of PART 1, and the observed parts of PARTs 3 and 4**, because no key was supplied. Reported as
  unrun rather than inferred.
* **Whether `video_view_retention` hides inside the untyped `raw` object.** Its OpenAPI schema is a
  generic passthrough, so only a live call can tell.
* **Whether re-engagement restores fields expired past the 7-day window.** TikTok's own remedy wording
  implies yes; it is not stated as a guarantee.
* **Whether analytics reads count against the 100-post import cap**, which decides whether $100 is
  genuinely flat at this volume.
* **Whether bundle.social's raw TikTok payload is enabled by default on the free tier**, since its own
  page says the payload is what you get *"when enabled for your organization"*.
* **No live API call was made to any vendor**, no account was created, no payment details were entered,
  and no credential was stored or logged.
