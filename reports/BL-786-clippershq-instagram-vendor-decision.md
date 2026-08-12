# BL-786 — the winner: Composio, at $0 to $29 a month, and it is the only vendor that returns skip rate

**2026-08-12 · DB `now()` = `2026-08-12 11:24:23.023627+00` · AUDIT ONLY, READ ONLY.**
No code, config, schema or data change. **No account connected, no payment details entered, no paid plan started, no free tier signed up for, nothing authorised, no credential stored.** Base `origin/main` @ `72f05cec`, branch `checkpoint/BL-786`, isolated worktree `C:/bl786`, `node_modules` never junctioned, removed at the end. Every database read through `scripts/run-select.js`. A markdown-only diff cannot change tsc or build, **so no build was run and none is claimed.** Five subagents ran in parallel, all read-only; **every load-bearing claim below was re-fetched and verified by me at the vendor's or Meta's own URL rather than accepted from a summary**, and contradictions are resolved rather than averaged. **The decision to build is the owner's and is not revisited here.**

## PART 0 — THE ANSWER

> ## **WINNER: Composio (https://composio.dev). $0 a month at the platform's real Instagram volume, or $29 a month with daily refresh. It is the ONLY vendor found that returns `reels_skip_rate` alongside `ig_reels_avg_watch_time` and `ig_reels_video_view_total_time`, because it passes Meta's own media-insights endpoint straight through instead of re-deriving it. Unlimited connected accounts, stated verbatim. Genuine Meta OAuth2 through a managed app whose default scope list already includes `instagram_business_manage_insights`.**
>
> **RUNNER-UP: PostPeer at $25 a month.** It loses on capability, not on price: `avgWatchTime` and `totalWatchTime` only, no skip rate, no demographics, and its analytics surface is missing from its own published OpenAPI spec.
>
> **The one thing standing between the winner and a decision is not on any website: whether Composio's managed Meta app has actually been GRANTED the insights scope, as opposed to merely requesting it. Composio's free tier settles that in one call, at $0, and PART 7 is the sequence.**

**This corrects BL-783 on the point that decided its verdict.** BL-783 concluded no vendor offers completion or skip rate. **That is now false: Composio documents `reels_skip_rate` explicitly.** BL-783 also placed Zernio in the "no watch time" pile; **Zernio documents `igReelsAvgWatchTime` today**, and additionally exposes `videoLength`, so a retention ratio can be computed. Both corrections are mine, verified at source, and both are stated here rather than buried.

## PART 1 — WHO HOLDS THE PASS-THROUGH

**There is NO public list of Meta Tech Providers. Meta publishes none, and verification status is visible only inside the approving business's own App Dashboard.** Checked directly: https://developers.facebook.com/docs/development/release/tech-providers/ (HTTP 200, defines the programme and lists the 34 restricted permissions, including `instagram_basic`, `instagram_business_basic` and `instagram_manage_insights`, but names no holder), https://developers.facebook.com/docs/development/release/access-verification/ and https://developers.facebook.com/docs/development/release/business-verification. The adjacent directory Meta does publish, https://www.facebook.com/business/partner-directory/, is the **Meta Business Partners** marketing programme, a different thing that never uses the words "Tech Provider", and it is login-walled to a fetcher.

**So the pool is built from first-party self-declaration.** Verbatim, from the vendor's own page:

| vendor | approval claim, quoted | serves an individual? | IG insights via creator OAuth |
|---|---|---|---|
| **Ayrshare** | **`"name":"Meta Tech Provider","networks":["Facebook","Instagram"],"status":"Approved"`** — verified by me in the page source at https://www.ayrshare.com/use-cases/digital-agencies/ | **yes**, terms require only age 18+ | yes |
| **Composio** | no Tech Provider claim; states **"Composio Managed App available"**, auth scheme **OAUTH2**, and its Instagram auth config's default scopes include **`instagram_business_manage_insights`** (https://docs.composio.dev/toolkits/instagram) | **yes**, self-serve, $0 tier | yes |
| **Mallary** | **"Meta Verified Tech Provider"** badge under "Officially Verified & Approved" | yes, 18+, $10/mo entry | yes, but **no watch time and no demographics** |
| **PostPeer** | **"PostPeer is approved for `instagram_business_basic`"** (https://www.postpeer.dev/instagram-analytics-api) and, in a collapsed FAQ answer I extracted from the same page, **"powered by the `instagram_business_manage_insights` scope that PostPeer is approved for"** | yes, $0 tier | yes |
| **Zernio** (formerly Late, `getlate.dev` now 301s here) | **Meta *Marketing* Partner** for ads only, which is not the same programme | yes, 2 accounts free, no card | yes |
| **Blotato** | none; "The Instagram approval has been done once, at the Blotato app level" | yes, 18+ | yes |
| **CreatorFlow**, **Inrō**, **ChatAutoDM**, **Cresva** | each claims Tech Provider or Access-Verified status in its own words | yes | **no public API** — proof the model works for small companies, not usable here |
| **Phyllo / InsightIQ** | no Tech Provider or Business Partner claim; only "Phyllo takes care of ... platform partnerships, app approvals" | **quote-gated**; BL-767 recorded "Company Name" as a required field to reach pricing | **DISQUALIFIED, settled this round — see the block at the end of PART 3** |

**PostPeer's approval status is now BETTER than BL-783 could establish.** BL-783 and one of this round's researchers both found only the `instagram_business_basic` claim and flagged the insights scope as an unclaimed separate review. **I extracted the collapsed FAQ answer from the same page and it does claim the insights scope.** Both statements sit on one page and PostPeer never reconciles them. The claim is now present; whether Meta granted it is still only settleable by a call.

## PART 2 — THE FIELD MATRIX

Every AVAILABLE cell carries the vendor's own URL. Meta's own reference is the first column because it is the ceiling: no vendor can return what Meta does not expose.

| field | **META** (the ceiling) | **Composio** | **PostPeer** | **Zernio** | **Ayrshare** | **Blotato** |
|---|---|---|---|---|---|---|
| average watch time | **`ig_reels_avg_watch_time`** "The average amount of time spent playing the reel" | **AVAILABLE** `ig_reels_avg_watch_time` | **AVAILABLE** `avgWatchTime` (seconds) | **AVAILABLE** `igReelsAvgWatchTime` (ms) | **AVAILABLE** `igReelsAvgWatchTimeCount` | **AVAILABLE** `watchTimeMsAvg` (ms) |
| total watch time | **`ig_reels_video_view_total_time`**, marked in development | **AVAILABLE** same name | **AVAILABLE** `totalWatchTime`, **may be null** | **AVAILABLE** `igReelsVideoViewTotalTime` (ms) | **AVAILABLE** `igReelsVideoViewTotalTimeCount` | **AVAILABLE** `viewTimeMsSum` |
| **completion / skip rate** | **`reels_skip_rate`** "The percentage of views from people who skipped during the first 3 seconds of the reel", marked estimated and in development | **AVAILABLE `reels_skip_rate`** | **ABSENT** | **ABSENT** | **ABSENT** | **ABSENT** |
| video length, for a retention ratio | not an insights metric | UNVERIFIED | ABSENT | **AVAILABLE** `videoLength`, its own doc says "combine with igReelsAvgWatchTime (ms) to estimate retention" | ABSENT | ABSENT |
| reach | `reach` | AVAILABLE | AVAILABLE | AVAILABLE | `reachCount` | `reachCount` |
| impressions | **DEPRECATED by Meta** v22.0, effective 2025-04-21 | n/a | AVAILABLE (will be null for IG) | AVAILABLE | `impressionsCount`, still listed, stale | `impressionsCount` |
| plays | **DEPRECATED**, replaced by `views` | n/a | AVAILABLE | AVAILABLE | `playsCount`, stale | `playsCount` |
| replays | **DEPRECATED** (`clips_replays_count`) | n/a | ABSENT | ABSENT | `clipsReplaysCount`, stale | ABSENT |
| saves | `saved` | AVAILABLE | AVAILABLE | AVAILABLE | `savedCount` | `savesCount` |
| shares | `shares` | AVAILABLE | AVAILABLE | AVAILABLE | `sharesCount` | `sharesCount` |
| profile visits | `profile_visits` (stories) / `profile_activity` | AVAILABLE | ABSENT | AVAILABLE | `profileVisitsCount` | `profileVisitsCount` |
| follows from post | `follows` | AVAILABLE | ABSENT | AVAILABLE | `followsCount` | `followsCount` |
| audience countries | **ACCOUNT level only**, `follower_demographics` | **AVAILABLE** via `INSTAGRAM_GET_IG_USER_INSIGHTS`, breakdowns `country`/`city`/`age`/`gender` | **ABSENT** | AVAILABLE (account level) | `audienceCountry` | **ABSENT**, "Instagram and TikTok report only the common metrics" |
| audience genders / ages | **ACCOUNT level only**, 100-follower floor | **AVAILABLE** | **ABSENT** | AVAILABLE | `audienceGenderAge` | **ABSENT** |
| follower count | `follower_count` | AVAILABLE | **ABSENT** | AVAILABLE | AVAILABLE | ABSENT |

Sources: Meta https://developers.facebook.com/docs/instagram-platform/reference/instagram-media/insights (fetched by me today, HTTP 200; the three Reels fields are present) · Composio https://docs.composio.dev/toolkits/instagram (the `INSTAGRAM_GET_IG_MEDIA_INSIGHTS` metric enum, quoted below) · PostPeer https://www.postpeer.dev/docs/analytics/get-analytics · Zernio https://docs.zernio.com/analytics/get-analytics · Ayrshare https://www.ayrshare.com/docs/apis/analytics/post · Blotato https://help.blotato.com/api/analytics/analytics-metrics.md

**Composio's metric enum, verbatim from its own docs, which is the finding of this round:**

> "COMMONLY SUPPORTED METRICS: views, reach, saved, likes, comments, shares, total_interactions, reposts. **REELS-SPECIFIC METRICS: ig_reels_video_view_total_time, ig_reels_avg_watch_time, reels_skip_rate**, facebook_views, crossposted_views."

**So the answer to the question BL-783 could not answer: COMPLETION IS OBTAINABLE.** Not as a retention curve, which exists nowhere at any price, but as `reels_skip_rate`, Meta's own estimate of the share of viewers who skipped in the first three seconds. **Only Composio surfaces it, because it is a pass-through of Meta's endpoint rather than a normalised cross-platform schema.** Meta labels it estimated and in development, so **treat it as UNVERIFIED until a live call returns a number.** The owner should stop looking for a drop-off curve; that genuinely does not exist for Instagram.

## PART 3 — PRICE, AND THE OWNER'S REAL BILL

### The pricing unit, precisely, per vendor

| vendor | unit | verbatim |
|---|---|---|
| **Composio** | **per tool call**, accounts free | "Pricing is based on the value we deliver to you — executions and resource use — **not accounts. There is no limit on the number of connected accounts you can have.**" Failed calls do not count. Free 20K calls/mo; **Pro $29/mo for 50K**; overage **$4 per 1K**; Business $599. New rates take effect **2026-08-15**, and anyone who buys before then keeps the current plan through 2026-12-31 |
| **PostPeer** | **per API call**, up to 100 posts per call, accounts unlimited | Free $0/20 credits · Starter $25/2,000 · Standard $43/6,000 · Pro $120/20,000. Team seats capped at 1/5/20/unlimited |
| **Zernio** | **per connected account per month** | First 2 free, accounts 3 to 10 **$6** each, 11 to 100 **$3** each, 101+ **$1** each, no cap, self-service |
| **Ayrshare** | **per user profile per month** (1 Instagram account = 1 profile) | $149 for 1 · $299 for 10 · $599 for 30 · $8.99 each for 31 to 100 · $3.49 each for 101 to 500 |
| **Blotato** | **per connected account tier** | Starter $29/20 · Creator $97/40 · Agency $499/100. **The 6-hour checkpoint exists ONLY on Agency**, at any scale |

**Per-connected-creator pricing is disqualified unless a tier covers hundreds.** Ayrshare and Blotato are disqualified on that rule; Zernio survives it only because its rate falls to $1 and has no cap, which is why it is costed rather than struck out.

### The owner's real volume, measured live today

| measure | value |
|---|---|
| Instagram clips, last 30 days | **1,275** |
| distinct Instagram clippers, last 30 days | **69** |
| distinct Instagram posting ACCOUNTS, last 30 days | **99** |
| Instagram approved earnings, last 30 days | **$2,290.81** |
| Instagram approved earnings, all time | $3,558.89 across 61 earning clippers |
| clips per posting account, 30 days | median **5**, mean 12.9, busiest **157**, only **2** accounts above 100 |

**Concentration, which decides how many people must say yes:**

| | top 5 | top 10 | top 25 | top 50 |
|---|---|---|---|---|
| share of Instagram EARNINGS, by clipper | **50.1%** | **69.2%** | **93.9%** | 99.8% |
| share of 30-day CLIP VOLUME, by account | 41.3% | 58.4% | **78.6%** | **92.4%** |

**The top 25 earning clippers hold 34 posting accounts between them and those accounts carry 978 of 1,275 clips, 76.7%.** That is the real onboarding target: **about 25 conversations, not 69 and not 361.**

### The bill, computed, and ranked by TOTAL cost

Composio bills per media-insights call, so its unit is the CLIP. The others bill per account or per list call, so their unit is the ACCOUNT. Both are computed from the same live numbers.

| strategy | Composio | PostPeer | Zernio | Ayrshare | Blotato |
|---|---|---|---|---|---|
| one capture per clip, 1,275 calls/mo | **$0** (free 20K) | $25 (101 calls) | $120 at 34 accounts | $599 at 25 profiles | $499 for a 6h read |
| daily refresh, top 34 accounts (76.7% of clips) | **$0** (~8,900 calls if only the first week per clip) | **$25** (1,080 credits) | **$120** | $635.96 | $499 |
| daily refresh, all 99 accounts (100%) | **$29** (38,250 calls, Pro 50K) | **$43** (3,030 credits) | **$315** | $1,228.30 | $499, capped at 100 |
| **rank by total cost** | **1** | **2** | **3** | **5** | **4** |

**Refetching costs again on every vendor that bills per call** (Composio per call, PostPeer explicitly "one credit per API call"), and **costs nothing extra on the per-account vendors**, which is the one place their model wins. **On-demand fetching is available on Composio, PostPeer, Zernio and Ayrshare** — all four expose a synchronous read the platform triggers itself. **Blotato is the exception and it is disqualifying: its endpoints "do not trigger a fresh fetch from the social platform"**, so readings arrive only on its fixed checkpoint schedule, and the 6-hour checkpoint is Agency-only and carries "a few minutes to a few hours" of deliberate jitter.

**No import cap of the bundle.social kind (5 free, 100 paid) exists on any of the four ranked above.** Composio states no account cap and bills executions; PostPeer states unlimited accounts on every tier; Zernio charges per account with no cap; Ayrshare charges per profile with no cap. **That single difference is why bundle.social's $100 plus an undisclosed raw-analytics fee is the most expensive option on this page for the least Instagram data.**

**Against $2,290.81 of monthly Instagram payouts, the winner costs 0% to 1.3%. Ayrshare would cost 26% to 54% of the money it is watching.**

### PHYLLO / InsightIQ, SETTLED AND DISQUALIFIED, because it was the biggest open candidate

BL-783 left Phyllo unresolved because it markets exactly the right fields and its documentation portal is a JavaScript shell. **It is now resolved by reading the rendered Stoplight schema, Phyllo's own Instagram availability matrix, its billing doc, its privacy policy and its end-user agreement. It fails three of the four tests.**

**TEST 1, capability: FAIL.** The `Content` object carries `engagement.additional_info.avg_watch_time_in_sec`, but that field appears **nowhere in Phyllo's own Instagram availability matrix**, which has no Reels column at all; `watch_time_in_hours` is described as "(only available for YouTube)" and returns `null` in every Instagram example response. **There is no completion rate, no skip rate and no drop-off curve in the schema.** The "Avg. Watch Time / Completion Rate / Drop-off Points" that its marketing pages promise are **Meta's** `/{ig-media-id}/insights` fields quoted in a guide, not Phyllo's response schema. It does return audience countries, cities, `gender_age_distribution`, `save_count`, `profile_visits` and `followers_gained`.

**TEST 2, pricing unit: FAIL, decisively.** Its own billing doc: "Each product has a separate activation fee", charged per connected creator account, plus "a fixed monthly fee for each product under this plan", and reconnecting a disconnected creator "will charge an activation fee for this action" again. **Per creator, per product, per month, with no dollar figure published anywhere.** The InsightIQ SaaS ladder ($199 / $299 / $899) quotes "creator connects" quotas of 0, 25 and 150, and lists **API access under Enterprise only, "Book A Call"**.

**TEST 4, consent: RED FLAG.** Its Connect SDK flow says "The creator enters credential for authentication to connect the work platform", its privacy policy says Phyllo collects "your username and password, **or a security token**", and its end-user agreement appoints Phyllo "as your agent and attorney, with full power of substitution" to "use your data and credentials to access all Platforms". Those are generic multi-platform documents and Instagram insights almost certainly do run through Graph API OAuth, **but no Phyllo page states that Instagram authorisation happens on Meta's own domain and that Phyllo never receives the password.** For the one vendor whose entire pitch is creator consent, that silence is disqualifying by itself under this round's test 4.

**Also recorded:** Phyllo holds **SOC 2 Type 1**, not Type 2; it stops refreshing engagement on content older than **90 days**; and, decisive for this use case, **"there is no way for us to go back in time and see the progression of engagement on that post"** — no historical snapshots, which is exactly what an arrival curve needs. **Stop pursuing Phyllo.**

## PART 4 — WHAT THE CLIPPER DOES

**Settled from Meta's CURRENT documentation, and it is the same for every candidate because they all ride the same two login paths:**

> "your app users must have an **Instagram professional account**" (business or creator) — https://developers.facebook.com/docs/instagram-platform/overview/
> "The Instagram API with Facebook Login **cannot access Instagram consumer accounts**." — https://developers.facebook.com/docs/instagram-platform/instagram-api-with-facebook-login
> "This API setup **does not require a Facebook Page** to be linked to the Instagram professional account." — https://developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login

**DEFINITIVE: a professional (Business or Creator) account is REQUIRED on both paths and a personal account cannot authorise at all. A linked Facebook Page is required ONLY on the Facebook Login path.**

**Per candidate:** Composio's Instagram toolkit states "Only supports Instagram Business and Creator accounts, not Instagram Personal accounts", auth scheme OAUTH2, managed app available; its default scope string is `instagram_business_basic,instagram_business_manage_messages,instagram_business_manage_comments,instagram_business_content_publish,instagram_business_manage_insights`, which is the **Instagram Login** family, so **no Facebook Page**. PostPeer states it outright: "PostPeer uses Instagram Login, so a linked Facebook Page is not required." **Neither top candidate needs a Page.**

**The taps, from Meta's own help page** (https://www.facebook.com/help/instagram/502981923235522): **6 steps in the Instagram app** to convert to professional — Profile, menu, Settings, "Switch to professional account", pick a category, Done — then **a 7th step**, authorising on Meta's own OAuth screen. The permission text a clipper sees is Meta's own consent screen listing the requested scopes; **its exact wording is UNVERIFIED because reading it requires starting a real authorisation, which this round did not do.**

**THE FUNNEL KILLER, unsoftened:** "**Professional accounts cannot be set to private.**" (https://www.facebook.com/help/instagram/138925576505882). A clipper with a private account must go public to participate.

**How many would complete it: STILL UNMEASURABLE, for the fourth round running.** `followerCount` is NULL on all **361** approved Instagram accounts and no account-type column exists in the schema, so the share already on a professional account is unknown. BL-722 priced the HikerAPI census that would settle it at about **$0.31** and it has still not been run. **No conversion estimate is offered here.** What is known is the shape of the ask: **25 people, 34 accounts, 76.7% of clip volume**, and those 25 can be asked personally.

## PART 5 — EXPIRY, LIMITS, BREAKAGE, AND THE RISK TO A CLIPPER

**Instagram fields do NOT expire the way TikTok's do. This is settled and Instagram is strictly better.** Meta: "**Metrics data is stored for up to 2 years**" for media insights, and "Data used to calculate metrics can be **delayed up to 48 hours**" (https://developers.facebook.com/docs/instagram-platform/reference/instagram-media/insights). There is no Instagram equivalent of BL-770's six-of-nine TikTok fields vanishing after 7 days of inactivity. **Capture-early-and-store is still mandatory, for a different reason: every vendor deletes or rotates its own copy** (bundle.social at 30 days, PostPeer publishes no retention policy at all), so the platform's own store must remain the durable copy.

**THE OPERATIONAL CONSTRAINT NO PRIOR ROUND MEASURED, and it shapes the build.** Meta's data is delayed up to 48 hours. Measured live on the last 30 days of Instagram clips: **the median clip is REVIEWED 2.9 hours after submission, 58.6% within 6 hours, 82.7% within 24 hours and 90.8% within 48 hours.** So for roughly four clips in five, **the review decision is already made before watch time is reliably available.** That does not stop the build; it decides the design. Watch time is a signal for the clipper's RECORD and for post-hoc review, not for the live queue, unless the owner chooses to hold Instagram reviews for two days, which he should not.

**Rate limits.** Composio: not published per plan beyond "higher rate limits" on Business; the meaningful ceiling is Meta's, below. PostPeer: **none published**, only "Rate limits depend on your plan", which is itself a finding. Zernio: not published. Ayrshare: **300 API requests per 5-minute interval per user profile**, `x-ratelimit-*` headers returned, and **1,000 429s in 24 hours auto-suspends the profile**. Underneath all of them sits Meta's own Instagram Business Use Case limit, "calls within 24 hours = 4800 × Number of Impressions", **which shrinks toward zero exactly on the low-reach accounts most likely to need checking.**

**Breakage.** Meta shut off the Instagram Basic Display API on 2024-12-04 and broke Tinder, Hinge, Day One and Discord. Meta deprecated `impressions`, `plays`, `clips_replays_count` and `ig_reels_aggregated_all_plays_count` on 2025-04-21 across all versions, **and Ayrshare's field reference still lists three of them with no deprecation marker**, acknowledging it only in a separate changelog. **A vendor's schema going stale against Meta is not hypothetical; it is the current state of at least one of these five.** The mitigation is the same one BL-773 already built: store every number the moment it arrives and never let a vendor field be the only copy.

**THE RISK TO A CLIPPER'S ACCOUNT, WITHOUT SOFTENING.** For a genuine OAuth app the realistic failure mode is app-level: Meta revokes the vendor's access and every token dies, **which breaks the platform's pipeline, not the clipper's account.** The creator can revoke at instagram.com/accounts/manage_access at any time. **The severe risk lives entirely on the other side of test 4.** Meta Platform Terms §6.a.iii: "you must not separately request or collect a Meta user's login credentials for any Meta Products." In Meta v. Voyager Labs, Meta disabled the accounts involved, reported at over 60,000; when Instagram purged inauthentic engagement from accounts using third-party tools it **forced password resets on those users** because their passwords had been shared. Instagram's own guidance is "Never share login credentials with any person or application." **If this platform ever asks a clipper for a password or a session cookie, the account at risk is the clipper's and they handed it over on this platform's prompt. None of the five ranked vendors does this, and no route that does may ever be adopted.**

## PART 6 — WHAT ALREADY EXISTS

| component | rating | evidence |
|---|---|---|
| the store, `ClipAnalyticsSnapshot` | **schema is VENDOR-AGNOSTIC**, column names are TikTok-shaped | `prisma/schema.prisma:3098-3152`; it already carries `provider` and `platform` columns, so a second vendor needs **no schema change**; but the ten analytic columns are TikTok metric names (`averageTimeWatchedSec`, `fullVideoWatchedRate`, ...) and `fullVideoWatchedRate` would hold `reels_skip_rate`'s inverse at best |
| the free arrival curve | **FULLY AGNOSTIC, 0 edits** | `src/lib/review-evidence.ts:168-236`, reads `clip_stats` with no platform predicate |
| the evidence panel | **multi-platform except ONE line** | `src/components/admin/ReviewEvidencePanel.tsx:301` short-circuits every non-TikTok platform |
| the capture | **bundle.social-SPECIFIC** | `src/lib/clip-analytics-capture.ts:348` returns `not_tiktok` and exits; `:381` sets `platformType=TIKTOK`; `ANALYTICS_FIELDS` at `:91-102` is ten TikTok metric names tested by exact key match; `MONTHLY_CAPTURE_BUDGET` at `:261` is one global counter |
| the vendor client | **bundle.social-SPECIFIC, whole file** | `src/lib/social-connect/bundle-social.ts` |
| the link store | **agnostic table, hardcoded constant** | `src/lib/social-connect/links.ts:58, 135, 222` all filter `provider: BUNDLE_PROVIDER` |
| the connect routes | **TikTok-specific paths** | `src/app/api/accounts/[id]/tiktok-link/*`, `src/app/api/tiktok-link/return/[linkId]` |

**Files referencing the vendor: 12, of which 5 are real source files** (two routes, the capture, the vendor client, the link store); the rest are generated Prisma code, probe scripts and comments. **The honest verdict: adding Instagram through a second vendor is a SECOND INTEGRATION for the connect and capture layers, and a one-line change for the free signal.** The table and the `provider` column were built for exactly this and hold up; the code around them was not.

**Every effort estimate here inherits an unproven chain: the TikTok pipeline has still never returned a single analytics field.** BL-780 applied the schema and the vendor team now resolves, and nobody has connected. **Nothing about this integration is proven end to end on any platform.**

## PART 7 — THE ANSWER, THE RUNNER-UP, AND THE STEPS

> **WINNER: Composio, $0 a month at one capture per clip and $29 a month with daily refresh, returning `ig_reels_avg_watch_time`, `ig_reels_video_view_total_time` and — uniquely — `reels_skip_rate`, plus account-level audience country, city, age and gender; and NOT returning any retention or drop-off curve, which exists nowhere at any price.**

**RUNNER-UP: PostPeer, $25 a month.** It loses on capability and on transparency, not on price: no skip rate, no demographics, no follower count, its **analytics endpoints are absent from its own published OpenAPI spec** (19 paths, none of them analytics), its counterparty is **"Jonathan Geiger D/B/A PostPeer"**, a sole proprietorship under Israeli law with no status page, no changelog, no SLA and four mutually contradictory published prices. It remains a genuine fallback because its unit and its unlimited-accounts promise are right.

**THIRD, and worth knowing: Zernio at $120 a month for 34 accounts**, the only vendor exposing `videoLength` beside watch time, from which a retention ratio can be computed. It loses on unit, not on capability.

### The ordered steps, and the free test comes FIRST

**Step 1, $0, no card, and it settles the whole question. Create a free Composio account (20,000 tool calls a month, unlimited connected accounts), connect ONE Instagram professional account the OWNER controls, and call `INSTAGRAM_GET_IG_MEDIA_INSIGHTS` with `metric=["ig_reels_avg_watch_time","reels_skip_rate","ig_reels_video_view_total_time"]` on one real Reel at least 48 hours old.** Look at exactly one thing: **are they numbers, or nulls, or a permission error?** A permission error means Composio's managed Meta app requests the insights scope but has not been granted it, which is the single unverified item in this report and the only thing that can still sink the winner. **Nothing on any website can answer this. One call can.**

**Step 2, still $0.** If step 1 returns numbers, repeat it on a clip the owner already believes was bought and one he believes was genuine. **This is the question that actually matters and no round has ever answered it: does watch time separate them?** If it does not, the owner has spent nothing and learned the thing worth learning.

**Step 3, the fallback, also $0 and no card.** If Composio's insights scope is not granted, run the same two tests on **Ayrshare's 28-day Launch trial**, which its own page states requires **no credit card** and "includes full Business plan access, including Max Pack and premium features". Ayrshare is the only candidate with an explicit **"Meta Tech Provider ... Approved"** self-declaration, so it is the most likely to work on the first try; it is disqualified for production at $599 a month, which does not matter for a 28-day read-only test.

**Step 4, the owner's own actions, none of which an agent can do:** convert one Instagram account he controls to a professional Creator account (6 taps), and decide which of the 25 top-earning clippers he asks first.

**Step 5, only after a real field has been observed:** run the **$0.31 HikerAPI census** across the 361 approved Instagram accounts to learn how many are already professional, because that number decides whether the ask is easy or hopeless, and it has now gone unrun for four rounds.

**Step 6, then and only then, write code.** The design constraint from PART 5 must be in it from the first line: **the median Instagram clip is reviewed 2.9 hours after submission and Meta's data is delayed up to 48 hours**, so watch time belongs on the clipper's record and on a post-hoc pass, not in the live review queue.

## CONTRADICTIONS, RESOLVED RATHER THAN AVERAGED

1. **BL-783: "no vendor offers completion or skip rate."** **REFUTED.** Composio documents `reels_skip_rate` in its metric enum, verified by me at https://docs.composio.dev/toolkits/instagram. BL-783 did not examine Composio.
2. **BL-783: Zernio has "zero watch-time, plays or retention."** **REFUTED for today.** `docs.zernio.com/analytics/get-analytics` documents `igReelsAvgWatchTime` and `igReelsVideoViewTotalTime` in milliseconds plus `videoLength`. Zernio is the rebrand of Late (`getlate.dev` 301s to `zernio.com`), so the two rounds may have read different products under different names; either way the current documentation is what a buyer gets.
3. **PostPeer's insights-scope approval.** One researcher and BL-783 both found only `instagram_business_basic` claimed, with insights flagged as "a separate Meta review". **I extracted the collapsed FAQ answer on the same page: "powered by the `instagram_business_manage_insights` scope that PostPeer is approved for."** Both statements are live on one page and PostPeer reconciles them nowhere. **Recorded as a self-contradiction, not resolved in PostPeer's favour.**
4. **Meta Tech Provider page availability.** One researcher reported a 404 and cautioned against BL-783's framing. **I fetched https://developers.facebook.com/docs/development/release/tech-providers/ myself: HTTP 200, and it carries BL-783's quote verbatim.** The 404 was on a different path. **BL-783's mechanism stands.**
5. **Ayrshare's Tech Provider claim.** Reported as possibly marketing prose. **I found the structured claim in the page source: `"name":"Meta Tech Provider","networks":["Facebook","Instagram"],"status":"Approved"`.** It is an explicit self-declaration, though Meta publishes nothing to check it against.
6. **Blotato's checkpoint schedule.** Previously reported as "lower tiers first read at 24 hours". **Corrected: Creator reads at 2 hours; Starter is the tier that first reads at 1 day; the 6-hour checkpoint is Agency-exclusive** and carries deliberate jitter of "a few minutes to a few hours".
7. **TikTok top-5 concentration, 71% (BL-772) against 81.8% (BL-783).** Definitions differ and neither round reconciled them. Not re-litigated here; the Instagram figures above are mine and are stated with their definitions.
8. **Watch-time units.** Meta states none. PostPeer says seconds, Zernio and Blotato say milliseconds, Ayrshare says nothing and its example payload is internally inconsistent (avg 23, total 21). **UNVERIFIED until a live call on a Reel of known length.**

## WHAT COULD NOT BE ESTABLISHED

**Nothing was exercised against any live key, so every capability claim is documentation only.** Specifically unresolved: **whether Composio's managed Meta app has been GRANTED `instagram_business_manage_insights`**, as opposed to listing it in its default scope string — the one item that decides the winner, settleable free in one call; whether `reels_skip_rate` returns a number in practice, given Meta marks it estimated and in development; the units of every vendor's watch-time field; **Phyllo's `avg_watch_time_in_sec` for Reels**, which exists in its schema but is absent from its own Instagram availability matrix, and which no longer matters because Phyllo is disqualified on pricing and consent regardless; Phyllo's raw OpenAPI file, never obtained because the Stoplight viewer exposes no spec URL; Composio's post-2026-08-15 rate card beyond the tiers quoted, which its own page says takes effect in three days; whether Meta imposes a connected-account ceiling that contradicts the "unlimited accounts" claims; the exact wording of the Meta consent screen a clipper sees; and **the share of the 361 approved Instagram accounts already on a professional account**, still unmeasurable from the schema and still unrun at $0.31.

**One observation, stated because it is unusual rather than because it changes anything:** Composio's pricing page contains text addressed to AI agents, telling them where the signup flow is and how to complete it. **I did not sign up, and no agent of this round did.** A vendor writing instructions aimed at automated readers is worth the owner knowing about before he points anything automated at it.

## SAFETY AND DISCLOSURE

READ ONLY, one document, on `checkpoint/BL-786` from `origin/main` `72f05cec`. **No code, config, schema or data change; no account connected; no payment details entered; no paid plan started; no free tier signed up for; nothing authorised; no credential stored, logged, printed or committed.** All vendor and Meta interactions were unauthenticated public documentation fetches. Every capability, pricing and terms claim carries the vendor's or Meta's own URL, and everything unexercised is marked UNVERIFIED. Eight read-only `SELECT`s ran through `scripts/run-select.js` against production, every timestamp cast `::text` against DB `now()`; no write, no money, no schema and no cron touched, and no clip status, earnings or payout changed. No handle, caption, wallet address or email appears above; clipper and account identifiers are counts only. The 6 money files, `tracking.ts` and `campaign-era.ts` are untouched: this branch's diff is exactly one markdown file. **No Apify actor was run.** Five subagents ran, all read-only, none permitted to write a file, sign up, connect an account or enter payment details; their claims are reconciled above and **every load-bearing one was re-fetched and verified by me at source**. Per-connected-creator pricing was disqualified as instructed, and no vendor whose consent flow resembles credential capture appears in the ranking. The worktree is removed. No dashes as bullets. **Nothing designed here may auto-reject a clip or be shown to a clipper: BL-518 and BL-521 stand, and BL-771's 21%-precision ceiling against a 99.2% human bar means watch time informs a person and decides nothing.**

**Rollback:** delete branch `checkpoint/BL-786`. It contains one document and touches nothing.
