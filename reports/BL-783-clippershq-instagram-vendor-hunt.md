# BL-783 — the Instagram vendor hunt: one qualifier found, and the mechanism that explains the peer

**2026-08-12 · DB `now()` = `2026-08-12 09:44:01.147707+00` · AUDIT ONLY, READ ONLY.**
No code, config, schema or data change. **No account connected, no payment details entered, no paid plan started, no free tier signed up for, nothing authorised, no credential stored.** Base `origin/main` @ `72f05cec`, branch `checkpoint/BL-783`, isolated worktree `C:/bl783`, `node_modules` never junctioned, removed at the end. A concurrent round held `C:/bl782`; it was left exactly as found and never touched. Every database read through `scripts/run-select.js`, which refuses a write keyword before connecting. A markdown-only diff cannot change tsc or build, **so no build was run and none is claimed.** Five subagents ran in parallel, all read-only; every claim below was reconciled against the vendor's or Meta's own page, and contradictions are reported rather than averaged.

## PART 7 FIRST — THE VERDICT, IN ONE LINE

> **A qualifying vendor DOES exist — PostPeer, at $25 to $43 a month for this platform's real Instagram volume, returning `avgWatchTime` and `totalWatchTime` for Reels through Meta's own OAuth with unlimited connected accounts — but it is still NOT worth building, because it does not return completion or skip rate, the free arrival curve already computes on 96.2% of Instagram clips at zero cost, and 82.6% of Instagram bought-view rejections are already caught by a repeat-offender signal that is shipped and mounted today.**

**This is a genuine correction to BL-781, which recommended against building after checking one vendor.** BL-781 was right that bundle.social has no Instagram watch-time field. It was wrong to leave the impression that no vendor has one. **Four do** — Ayrshare, Blotato, Metricool and Databox all return real Instagram watch time, and PostPeer does so on usage pricing. **The recommendation does not change; the reason for it does.** Build refusal now rests on value, not on availability.

**If the owner wants to spend nothing and learn the one thing that matters, it is not a vendor decision.** It is Ayrshare's 28-day free trial, no credit card, on one account he controls, to see whether `igReelsAvgWatchTimeCount` actually separates a bought-view clip from a real one. **If it does not, the whole question dies and no vendor needs choosing.** Full sequence at the end of PART 6.

## PART 0 — THE FOUR TESTS, STATED BEFORE SEARCHING

A vendor qualifies only if it passes **ALL FOUR**:

**TEST 1 — RETURNS WATCH TIME AND COMPLETION**, or the nearest true Instagram equivalents (average watch time, plays, replays, retention). Public counts alone FAIL, because HikerAPI already supplies those and BL-775 proved the free arrival curve separates 66.4% against 7.8% on Instagram without any vendor.
**TEST 2 — PRICING SCALES WITH USAGE, NOT WITH CONNECTED CREATORS.** Per call, per credit, or a flat tier that does not cap connected accounts. Per-profile or per-seat FAILS however cheap the entry tier.
**TEST 3 — WORKS WITHOUT A REGISTERED COMPANY.** The owner is an individual.
**TEST 4 — CONSENT THROUGH A GENUINE PLATFORM SCREEN.** A vendor asking for an Instagram password or a session cookie is disqualified regardless of capability, because this platform would be the one asking clippers to authorise.

## PART 1 — THE MECHANISM, WHICH IS THE ROUND

### Which Instagram analytics require what approval

Meta runs two permission families, one per login path, both current. **Instagram Login** needs `instagram_business_basic` + `instagram_business_manage_insights`. **Facebook Login** needs `instagram_basic` + `instagram_manage_insights` + `pages_read_engagement`. Source: https://developers.facebook.com/docs/instagram-platform/insights/ and https://developers.facebook.com/docs/permissions

**Meta itself exposes the fields this round was hunting.** Verified directly against Meta's media insights reference, for REELS, under `instagram_business_manage_insights` (Instagram Login) OR `instagram_manage_insights` (Facebook Login) — https://developers.facebook.com/docs/instagram-platform/reference/instagram-media/insights :

• **`ig_reels_avg_watch_time`** — "The average amount of time spent playing the reel." **No caveat.**
• **`ig_reels_video_view_total_time`** — "The total amount of time the reel was played, including any time spent replaying the reel." Marked **in development**.
• **`reels_skip_rate`** — "The percentage of views from people who skipped during the first 3 seconds of the reel." Marked **estimated and in development**.

**CONTRADICTION RESOLVED, not averaged.** A community gist claimed `reels_skip_rate` was a Marketing-API-only addition. I fetched Meta's page directly: it is listed on the standard Instagram Platform media insights reference under the ordinary insights permission, not the Marketing API. **The gist is wrong.** The honest caveat is Meta's own: estimated, and in development.

**So the gap BL-781 found is the VENDOR's, not Meta's.** `impressions`, `plays`, `clips_replays_count` and `ig_reels_aggregated_all_plays_count` are all DEPRECATED (v22.0, effective 21 April 2025, https://developers.facebook.com/docs/graph-api/changelog/version22.0/), replaced by the single canonical `views`.

### THE PASS-THROUGH QUESTION: PERMITTED, AND CONDITIONAL ON THE VENDOR

**BL-767's insight transfers to Instagram, and Meta has a NAMED PROGRAM for it.** From https://developers.facebook.com/docs/development/release/tech-providers/ :

> "Tech providers are businesses that have a legitimate need to access business data owned by other businesses in order to provide services or functionality to those businesses."

Once the business is verified, "any apps claimed by the business can then be used by other businesses." Apps cannot receive restricted permissions "unless the business has been verified as a Tech Provider **or the person using the app has a role on the app itself**." `instagram_basic`, `instagram_business_basic` and `instagram_manage_insights` are all on that restricted list.

Platform Terms (https://developers.facebook.com/terms/) bind the **Tech Provider**, defined as "a Developer of an App whose primary purpose is to enable Users thereof to access and use Platform or Platform Data". Section 5.b.ii.1 requires processing "on behalf of and at the direction of your Client"; 5.b.ii.4.a permits sharing "with your applicable Client, so long as you first contractually prohibit such Client" from violating the terms; 5.b.ii.2 requires each Client's data be kept separate.

**Verdict: PERMITTED. Every condition attaches to the VENDOR, none to the vendor's customer.** No Meta rule was found requiring each business to have its own app, and no prohibition on one app serving many unrelated businesses. **An individual with no registered company needs no Meta app, no App Review and no Business Verification if they consume through a verified Tech Provider.** The company requirement lands on the vendor. This is the designed path, not a loophole.

**Do not confuse "Service Provider" with "Client".** In Meta's terms a Service Provider is the vendor's own subcontractor; the arrows run in opposite directions.

### THE SECOND MECHANISM, WHICH PROBABLY EXPLAINS THE PEER

**Standard Access reads insights for accounts holding a role on the app, with NO App Review and NO Business Verification.** Meta states it twice, positively and negatively:

> "Permissions with Standard Access can only be requested from app users who have a role on the requesting app." · "Business, Consumer, and Gaming apps are automatically approved for Standard Access for all permissions." · "Business Verification is required to get Advanced Access." — https://developers.facebook.com/docs/graph-api/overview/access-levels
> "If your app will only be used by app users who have a role on the app itself, App Review is not required." — https://developers.facebook.com/docs/apps/review

Capacity, verified directly at https://developers.facebook.com/docs/development/build-and-test/app-roles/ : **"Most apps, not linked, can have up to 50 testers."** An app linked to a Business Manager with Business Verification "can have up to a combined total of 500 analytics users and testers." Testers "can grant the app any permission while it is in development, and all features are active."

**One corroborating account from an individual**, labelled SINGLE CORROBORATED CLAIM: a solo developer on Indie Hackers (https://www.indiehackers.com/post/instagram-basic-api-and-business-verification-36425eedb0) says business verification "Nope. Needs a company", then describes his own workaround: "for myself, I've made myself a beta tester which means it works even without the verification."

**THIS IS ALMOST CERTAINLY WHAT THE PEER IS DOING, AND IT DOES NOT TRANSFER TO THIS PLATFORM.** Meta's own app-roles page carries a restriction that must not be glossed:

> "You may only add a person as a Tester to your app if they are your employee **or you have an agreement with them which establishes that they are acting on your behalf as a tester of your app**."

Clippers are not employees and are not acting on the platform's behalf as testers; they are independent creators submitting their own work. The same page also notes that regular Testers require a Meta Developer Account, which is per-clipper friction far beyond a professional-account switch. **The tester route is legitimate at the scale of a person testing their own thing. Used as a production mechanism for 100 unrelated creators it is a terms problem and an adoption problem, and this report does not recommend it.**

### Candidates found, and the FIRST test each fails

**PASSES ALL FOUR: PostPeer** (https://www.postpeer.dev). Detailed in PART 2.

**FAILS TEST 1 (no watch time or completion):** bundle.social (no documented Instagram watch-time field at any plan level, BL-781) · HikerAPI (public counts; its lone `GET /v1/media/insight` takes only `media_id`, has no owner-authorisation parameter and is architecturally owner-session-gated, UNVERIFIED and implausible) · Apify Instagram Scraper and every analytics actor examined (Apify's own page: "scrapes public data, so it gets the same counts Instagram shows a visitor who isn't signed in") · **Upload-Post** (followers, reach, views, impressions, profileViews, likes, comments, shares, saves, demographics; no duration field) · **Postiz** (impressions, likes, comments, shares, engagement; its public API documents no analytics endpoint at all) · **Zernio** (impressions, reach, likes, comments, shares, saves, views; zero watch-time, plays or retention) · **social-api.ai** (post metrics are exactly comments, likes, saves, shares) · **Publer** (tops out at `video_views`, a public count) · **Modash** (its own doc: "Instagram Raw Data API allows you to get public data anonymously from Instagram", so it independently fails test 4 too, having no OAuth at all) · Outstand (impressions, reach, likes, comments, saves, shares, views, engagement_rate only, despite requesting the insights scope) · Mallary.ai · Data365 · EnsembleData · SociaVault · ScrapeCreators · Netrows · SocialKit · Crowdfire · Elfsight · Unipile · Nango · Phantombuster · the RapidAPI Instagram analytics family.

**FAILS TEST 2 (priced or capped by connected account) — and THREE of these do return real Instagram watch time:**

• **Ayrshare — the most transparent vendor examined, and it fails only on price.** Its post-analytics reference documents `igReelsAvgWatchTimeCount` ("The average amount of time spent playing the reel") and `igReelsVideoViewTotalTimeCount` (https://www.ayrshare.com/docs/apis/analytics/post). Re-verified against today's published table (https://www.ayrshare.com/pricing/): $149/mo for 1 profile, $299 for 10, $599 for 30, then $8.99 each for 31 to 100, $3.49 for 101 to 500. **300 profiles = $599 + (70 × $8.99) + (200 × $3.49) = $1,926.30/month, matching BL-768 exactly. The pricing has not moved in either direction.** No usage or per-call plan exists and there is no free tier, though there is a **28-day free trial on the Launch plan with no credit card**.
• **Blotato — the closest near-miss on capability.** Returns `watchTimeMsAvg` ("Average watch time, milliseconds") and `viewTimeMsSum` (https://help.blotato.com/api/analytics/analytics-metrics.md). Fails test 2 on hard per-tier account caps: Starter $29/20 accounts, Creator $97/40, Agency $499/100, and above 100 there is no published price at all. **Two further disqualifiers for this use case:** analytics are fixed snapshots and the endpoints "do not trigger a fresh fetch from the social platform", so on-demand fetching is impossible; and **only the $499/month Agency tier has a 6-hour checkpoint**, which is precisely BL-775's separating window. Starter's first reading lands at 24 hours.
• **Metricool** — surfaces Reels average watch time, total watch time and retention in-product, but the API is gated to a per-brand Advanced plan from €54/mo (https://metricool.com/pricing/) and no vendor page maps those metrics to an API response.
• **Databox** — exposes "Reel Average Watch Time by Reel", so its rejection stands on pricing only, not on the metric (https://databox.com/metric-library/metrics/instagram-business/reel-average-watch-time-by-reel).
• **Phyllo / InsightIQ** — markets "Avg. Watch Time", "Completion Rate" and "Drop-off Points" for Reels and claims to remove the approval burden entirely ("No app review required — Phyllo handles approvals"). **But no Phyllo page states its own API returns those fields**: its Instagram page lists only likes, comments, followers and "views and engagement on reels", and its reels blog attributes the watch-time field to *Meta's* API rather than Phyllo's schema. Pricing is quote-only across three mutually incompatible vendor pages. **UNVERIFIED on capability and on price.**
• Also failing on price or seats: Iconosquare (per profile AND per seat), Socialinsider, Shortimize, Buffer, Hootsuite, Sprout Social, Brandwatch, Dataslayer.ai, Windsor.ai. **Mixpost would have PASSED test 2** ($299 one-time, unlimited accounts) but fails test 1 on capability and test 3 independently, its own guide stating "Facebook Business Verification is required".

**FAILS TEST 4 (credential or session capture):** instagrapi and every private-API wrapper (`Client().login(USERNAME, PASSWORD)` or a pasted `sessionid`; and note its documented insights carry **no watch time and no retention anyway**, so this route could not be the peer's) · the Apify cookie-paste actor family (Instagram Following Scraper, Stories Scraper, Story By Cookies, Instagram Cookies, Search Users by Cookies).

**FAILS TEST 3 (registered company): Meta direct.** The fields are free and the consent screen is Meta's own, but serving clippers who hold no role on the app requires Advanced Access, which requires App Review **and** Business Verification, which Meta frames as verifying "your identity as a business entity".

**Structural reason the hunt kept failing, worth stating:** aggregators normalise to a lowest-common-denominator schema across ten platforms, and watch time exists on almost none of them, so it gets dropped. And no scraper can ever supply it, because **Instagram never renders watch time to anyone but the account owner**. Any vendor returning it is either using OAuth or holding the creator's session.

## PART 2 — THE QUALIFYING VENDOR, IN DEPTH

**PostPeer** (https://www.postpeer.dev). Every claim below was fetched by me directly from PostPeer's own pages, not taken from a subagent summary. **Nothing was exercised against a live key: no signup, no OAuth, no call. Every capability claim is DOCUMENTED ONLY and UNVERIFIED in practice.**

### Instagram fields

| field | status | note |
|---|---|---|
| **`avgWatchTime`** | **AVAILABLE** | "Instagram Reels only, in seconds… the average watch time per view". Maps to Meta's `ig_reels_avg_watch_time` |
| **`totalWatchTime`** | **AVAILABLE, may be null** | "the total watch time including replays (Meta flags this one as 'in development,' so it can be `null`)" |
| **completion / `reels_skip_rate`** | **ABSENT** | Exists at Meta; PostPeer does not surface it. This is the honest hole in test 1 |
| retention curve / drop-off | **ABSENT** | No such field |
| `reach`, `likes`, `comments`, `shares`, `saves`, `views`, `impressions`, `clicks`, `engagementRate` | AVAILABLE | Public-grade, already free via HikerAPI |

Source: https://www.postpeer.dev/docs/analytics/get-analytics and https://www.postpeer.dev/docs/api/analytics/getAnalytics

**It works on NATIVELY posted clips, which is the whole use case.** PostPeer's own doc: "Set `source=platform` with `accountId` to fetch recent posts directly from the platform — **including posts not published through PostPeer**." `source=postpeer` means "posts published via PostPeer, stored in our DB"; `source=platform` means "fetched directly from the connected platform account". Clippers post natively, so `source=platform` is the mode that matters and it is documented.

### Pricing unit and cost per 1,000 calls

**Credits. 1 credit per API CALL, not per post**, and a single call returns up to 100 posts. "One credit per API call, whether you fetch one post or a paginated list." **Connected accounts are UNLIMITED on every tier including free** (https://www.postpeer.dev/pricing):

| tier | $/month | credits | **cost per 1,000 calls** |
|---|---|---|---|
| Free | $0 | 20 | n/a |
| Starter | $25 | 2,000 | **$12.50** |
| Standard | $43 | 6,000 | **$7.17** |
| Pro | $120 | 20,000 | **$6.00** |

**PRICING CONTRADICTION, REPORTED NOT AVERAGED:** PostPeer's own blog quotes "$8.50 per 1,000 posts on Starter" and elsewhere $19/4,000 and $17/2,000, none of which reconciles with the pricing page's $25/2,000. Its authentication doc says "paid plans start at $19/month". **Trust the pricing page and re-confirm before paying.** Credit packs "never expire".

### Consent, authorisation, limits, expiry

**Consent flow: GENUINE META SCREEN.** `GET https://api.postpeer.dev/v1/connect/instagram` returns an Instagram authorization URL; the creator authorises on Meta's own domain (`https://www.instagram.com/oauth/authorize`) and PostPeer's callback exchanges the token. No credential capture, no cookie paste anywhere in the flow. **It uses Instagram Login, so no Facebook Page is required**: "PostPeer uses Instagram Login, so a linked Facebook Page is not required" (https://www.postpeer.dev/docs/platforms/instagram). Professional Business or Creator account required; personal accounts excluded. The analytics doc names the scope: **`instagram_business_manage_insights`**.

**Is authorisation one-time? NO, and this matters.** Meta's Instagram Login long-lived token lasts **60 days** and must be refreshed while still valid. PostPeer says it handles "token storage, refresh" but **UNVERIFIED**. A clipper who goes quiet for 60 days silently drops off and must re-authorise.

**Rate limits: NOT PUBLISHED.** PostPeer states only "Rate limits depend on your plan. We respect each platform's native rate limits" with no numbers (https://www.postpeer.dev/docs/authentication). **That is itself a finding.** Meta's own floor applies underneath: Instagram Business Use Case allows "calls within 24 hours = 4800 * Number of Impressions" (https://developers.facebook.com/docs/instagram-platform/overview). **Note the trap: a low-impression clipper has a proportionally tiny quota.**

**Do fields expire? NO 7-day vanishing, unlike TikTok. This is settled and Instagram is strictly better.** Meta: "Metrics data is stored for up to 2 years" for media insights, and "Data used to calculate metrics can be delayed up to 48 hours" (https://developers.facebook.com/docs/instagram-platform/reference/instagram-media/insights). **CONTRADICTION, reported:** Meta's insights guide states user-level metrics persist only 90 days; the two pages describe different scopes and Meta reconciles them nowhere. PostPeer publishes **no data-retention policy at all**, which is worse than bundle.social's documented 30 days.

### What PostPeer will not disclose, and the durability risk, stated plainly

**No legal entity is named anywhere** (only "© 2026 PostPeer" and a founder named Jonathan). **It does not disclose whether it holds Meta App Review approval, Advanced Access, or Tech Provider verification** — and per PART 1 that is the single thing the whole arrangement depends on. Meta: until a business is verified, "app users from other Businesses will be unable to grant these apps permissions and **all features will be inactive**." **If PostPeer lacks Tech Provider verification, the connect flow fails silently for every clipper — the exact shape of bundle.social's "no team" inertness that BL-777 discovered the hard way.** Rate limits undisclosed, retention policy absent, published prices mutually inconsistent, and 7 Trustpilot reviews. **This is a small, young, single-founder vendor and the report will not dress that up.**

### THE STRUCTURAL COUNTER-ARGUMENT, AND WHY PostPeer STILL STANDS

**Two of the five research angles concluded independently that NO vendor passes all four tests, and their reasoning deserves to be stated rather than buried.** The argument is that Instagram watch time is never public, so any vendor returning it must hold an OAuth connection per creator; that connection is the vendor's real cost; therefore **tests 1 and 2 are in tension by construction** and every capable vendor prices or caps by connected account. Ayrshare, Blotato, Metricool, Databox and Phyllo all fit that pattern exactly.

**PostPeer is the counter-example, and I verified it at source rather than accepting any summary.** Its pricing page states "Unlimited Connected Accounts" on **every** tier including free, and its billing unit is the API call, not the connection. **I therefore do not adopt the structural claim as a law.** But it is a legitimate reason for suspicion, and the honest reading is one of three: PostPeer has a genuinely different cost structure, or it has not yet hit the scale where connection cost bites and its pricing will change, or the watch-time field does not populate in practice. **Only the free test below distinguishes them.** Where my own research angles disagreed, both positions are recorded here and neither was averaged away.

### WHAT VENDORS WILL NOT DISCLOSE BEFORE PAYMENT, which is itself a finding

• **PostPeer:** rate limits, data-retention policy, legal entity, and Meta approval status. Its three published prices contradict each other.
• **Blotato:** any price above 100 connected accounts (in-app chat only), analytics-endpoint rate limits, and snapshot retention. **Worse, generating an API key "ends your free trial immediately" and starts a paid subscription, so the analytics endpoint cannot be evaluated without paying.**
• **Phyllo / InsightIQ:** no API pricing unit anywhere, and the API reference is a JavaScript-only viewer that serves an empty shell to any non-browser fetch, so the Instagram field list is effectively unreadable before purchase.
• **Modash:** Raw API access is gated behind sales, annual contracts only, "we don't offer any monthly or pay-as-you-go plans".
• **Metricool:** its own help page admits "Some Metricool API endpoints are not listed in the PDF documentation" and tells customers to find them by "inspecting your browser". **A vendor instructing you to reverse-engineer its API from devtools is the finding.**
• **Iconosquare:** no public API reference exists at all.
• **bundle.social** (BL-781, unchanged): the price of raw-analytics enablement, of imported-post refresh, and of sub-24h refresh, all three sales-gated with no public number.
• **Ayrshare is the exception and deserves the credit:** its full Instagram field list, every price and every per-profile increment are public. Only the Max Pack's numeric limits and Enterprise pricing are withheld.

## PART 3 — THE ACCOUNT-TYPE QUESTION, SETTLED

**Settled from Meta's current documentation, and it agrees with BL-781 while correcting the brief's attribution to BL-722.**

> "your app users must have an **Instagram professional account**" (business or creator) — https://developers.facebook.com/docs/instagram-platform/overview/
> "The Instagram API with Facebook Login **cannot access Instagram consumer accounts**." — https://developers.facebook.com/docs/instagram-platform/instagram-api-with-facebook-login
> "This API setup **does not require a Facebook Page** to be linked to the Instagram professional account." — https://developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login
> "your app users' Instagram professional accounts **must be connected to a Facebook Page**" (Facebook Login path) — overview

**DEFINITIVE: a professional (Business or Creator) account is REQUIRED on both paths. Personal accounts CANNOT authorise at all. A Facebook Page is REQUIRED ONLY on the Facebook Login path.** PostPeer uses Instagram Login, **so no Facebook Page is needed here.**

**Exactly what a clipper must do: 6 steps, entirely in the Instagram mobile app**, confirmed at https://www.facebook.com/help/instagram/502981923235522 . Profile, menu, settings, "Switch to professional account", choose a category and contact details, Done. Creator is the right type. Then a 7th step for this integration: authorise on Meta's own OAuth screen.

**THE FUNNEL KILLER, unsoftened.** Confirmed verbatim at https://www.facebook.com/help/instagram/138925576505882 : **"Professional accounts cannot be set to private."** A private clipper must make their account public to participate. That page does not address reversibility or pending follow requests; BL-781 cited both from the same source and I could not re-confirm them today, so treat only the private-account rule as verified.

## PART 4 — THE OWNER'S REAL COST AND THE REAL POPULATION

Measured live, DB `now() = 2026-08-12 09:44:01+00`, Instagram identified by joining `clips` to `clip_accounts.platform`:

| measure | value |
|---|---|
| Instagram clips, last 30 days | **1,274** |
| distinct Instagram clippers, last 30 days | **70** |
| distinct Instagram POSTING ACCOUNTS, last 30 days | **100** |
| approved Instagram clips, last 30 days | 1,048 |
| Instagram approved earnings, all time | **$3,553.61** |
| clippers who have EVER earned on Instagram | **61** |
| approved, non-deleted Instagram accounts | **361** |
| those with a known `followerCount` | **0** |
| clips per posting account, 30d | median **4.5**, mean **12.7**, busiest **157**, only **2** accounts above 100 |

### Concentration, against BL-772's TikTok benchmark

| | top 5 | top 10 | top 25 | top 50 |
|---|---|---|---|---|
| **Instagram earnings** | **50.2%** | **69.2%** | **94.0%** | **99.8%** |
| **TikTok earnings** (measured today) | **81.8%** | 89.9% | 98.2% | — |
| Instagram 30d clip volume, by account | — | — | 78.6% | **92.4%** |

**CONTRADICTION WITH BL-772, REPORTED NOT AVERAGED.** BL-772 put the TikTok top 5 at **71%** of TikTok earnings; measuring today over all-time approved clips with `videoUnavailable = false` and earnings above zero, across 55 earning TikTok clippers, I get **81.8%**. The definitions differ and I have not reconciled them. **The direction is identical and is what matters: Instagram is far LESS concentrated than TikTok**, so Instagram needs many more people connected to move the same share of money.

### The cost, computed

The fetch shape is `source=platform` + `accountId`, up to 100 posts per call, **1 credit per call**. At a median 4.5 clips per account per month, **one call covers one account's month**, so a full pass over every connected account costs **1 credit per account**.

| strategy | credits/month | **tier needed** | **$/month** |
|---|---|---|---|
| all 100 accounts, one pass a month | 100 | Starter | **$25** |
| all 100 accounts, refreshed daily | 3,000 | Standard | **$43** |
| all 100 accounts, every 6 hours | 12,000 | Pro | **$120** |
| **top 50 accounts (92.4% of clips), daily** | **1,500** | **Starter** | **$25** |
| top 25 accounts (78.6% of clips), daily | 750 | Starter | **$25** |

**Against bundle.social's $100/month plus an undisclosed raw-analytics fee plus per-account import caps, PostPeer at $25 to $43 covering the whole Instagram footprint is between a half and a quarter of the price, with no per-account cap at all.** That is the real finding of PART 4.

**On-demand fetching is possible**: the analytics endpoint is a synchronous GET the platform calls whenever it wants, with `fromDate`/`toDate`, `sortBy` and pagination. There is no vendor-imposed sync cadence. **Refetching the same post COSTS AGAIN**, at 1 credit per call, every time.

**The population number that still has not been measured, for the third round running:** `followerCount` is NULL on all 361 approved Instagram accounts and no account-type column exists anywhere in the schema, so **the share of clippers already on a professional account remains unknown.** BL-722 priced the HikerAPI census that would settle it at roughly **$0.31** in August. It has still not been run. **Any conversion estimate before that number is a guess, and this report will not make one.**

## PART 5 — WHAT IT ADDS BEYOND FREE. HONESTLY: LITTLE THAT CHANGES A DECISION

Measured fresh today, on live Instagram clips with `videoUnavailable = false`:

| | measured today | BL-781 |
|---|---|---|
| Instagram live clips where the arrival curve computes (3+ snapshots) | **1,788 of 1,859 = 96.2%** | 94.8% |
| approved Instagram clips where it computes | **1,528 of 1,537 = 99.4%** | 99.2% |
| Instagram clips with no snapshot at all | **28** | 38 |
| Instagram bought-view rejections | **109 of 181 platform-wide = 60.2%** | identical |
| ... across distinct clippers | **22** | identical |
| ... **made against a clipper who ALREADY had an earlier one** | **90 of 109 = 82.6%** | **identical** |

**The absolute clip counts differ from BL-781 because my "live" definition filters `videoUnavailable` and joins platform through `clip_accounts`; the shares reproduce and the repeat-offender figure reproduces exactly.** Same discipline BL-781 applied to its own count discrepancy: treat the shares as sound and the totals as definition-dependent.

**The answer the brief asked for.** BL-775 measured the free curve separating **66.4% of views by 6 hours for approved Instagram clips against 7.8% for bought-view rejections**, the largest separation of any platform, with no vendor, no connection and no authorisation. On top of that, **the single best predictor of an Instagram bought-view rejection is that the same clipper was already caught before, at 82.6%, and it is already shipped and mounted on the review screen** (BL-775, merged at BL-776).

**What `avgWatchTime` would genuinely ADD:** a clip with 300,000 views and a 1.2-second average watch is a fact the arrival curve cannot produce. That is real, new information and this report will not pretend otherwise. **By how much it would improve on 66.4 against 7.8: UNMEASURABLE in advance, and no number will be invented here.** No published study gives an AUC for watch-time features against purchased Instagram views.

**Three things blunt it further.** First, **PostPeer does not return completion or skip rate**, so the half of the brief's test 1 that measures whether people finished the video is not available from the one qualifying vendor. Second, **BL-771's ceiling stands**: every computable signal measured under **21% precision** against the owner's **99.2%** reviewer accuracy, so **nothing here becomes a verdict**, cannot auto-reject, and cannot be shown to a clipper. Third, coverage: the free signal computes on **96.2% of Instagram clips today**, against a connected pipeline that covers **0%** and would need every one of 100 posting accounts converted to professional, made public, and individually authorised to reach 92.4%.

**One measured defect is worth more than the whole integration.** Re-verified today over 14 days:

| platform | clips 14d | first snapshot within 60s | median seconds to first snapshot | no snapshot ever |
|---|---|---|---|---|
| **Instagram** | 921 | **23.9%** | **3,161s (52.7 min)** | **33** |
| TikTok | 162 | 88.3% | **0s** | 2 |
| YouTube | 35 | 94.3% | **0s** | 0 |

**The platform where the arrival curve separates best is the only one whose curve starts blind for the first 53 minutes.** Fixing that sharpens the exact signal that already works, on 100% of Instagram clips, with no vendor, no clipper action, no terms exposure and no monthly fee.

## PART 6 — THE TERMS, AND THE RISK TO A CLIPPER'S ACCOUNT

**Meta's terms do not prohibit the owner's intended use.** BL-781 established this against Platform Terms and Developer Policies (both Last Updated 2026-02-03) and nothing found this round contradicts it. The four conditions it identified still bind: permitted-purpose only (3.a.viii), no eligibility determinations about people (3.a.ii), no profile-building without consent (3.a.v), and deletion on user request (3.d.i.2.d). Derived data is itself Platform Data under Note 12, so a fraud signal computed from insights inherits every restriction. **The "no groupBy, no percentile" position remains correct and must stay.**

**For PostPeer specifically, two things change.** First, PostPeer **pushes platform-compliance liability onto the owner**: "By using PostPeer to access these platforms, you agree to be bound by each platform's own terms of service" (https://www.postpeer.dev/terms). That is the same pattern BL-767 flagged as a risk. Second, PostPeer **imposes no company, entity, VAT or tax requirement** and its terms address "the person", which is how it passes test 3 — **by absence of a barrier rather than by an affirmative statement, so it is UNVERIFIED until a signup is attempted.**

**THE ACCOUNT-SUSPENSION RISK TO CLIPPERS, WITHOUT SOFTENING.**

**Genuine OAuth apps: no comparable enforcement was found.** Authorisation happens on Instagram's own domain, the token is scoped, and the creator can revoke it themselves at instagram.com/accounts/manage_access. The realistic failure mode is app-level — Meta revoking PostPeer's access, invalidating tokens — **which breaks the platform's pipeline, not the clipper's account.** Claims to the contrary came only from SEO-grade marketing blogs and are not treated as fact here.

**Credential capture and session replay: the risk is real, documented and severe, and it is the reason test 4 exists.** Meta Platform Terms §6.a.iii: "you must not separately request or collect a Meta user's login credentials for any Meta Products". Meta enforces "at any time… with or without notice". In Meta v. Voyager Labs, Meta "disabled Voyager's accounts" (https://about.fb.com/news/2023/01/leading-the-fight-against-scraping-for-hire/), reported as **over 60,000 Facebook and Instagram accounts disabled**. Meta v. BrandTotal, whose product harvested users' authenticated sessions, ended in a permanent injunction. When Instagram purged inauthentic engagement from accounts using third-party tools, it **forced password resets on those users** precisely because their passwords had been shared (https://www.nbcnews.com/tech/tech-news/instagram-crack-down-fake-likes-followers-n938131). Instagram's own guidance to users is "Never share login credentials with any person or application" (https://www.facebook.com/help/instagram/588549329146493).

**Stated plainly: if this platform ever asks a clipper for an Instagram password or a session cookie, the account at risk is the clipper's, and they handed it over on this platform's prompt. That is a reputational and legal surface, not a technical one. PostPeer does not do this, and no route that does may ever be adopted.**

**A separate, real platform risk:** Meta shut off the Instagram Basic Display API on 4 December 2024, breaking Tinder, Hinge, Day One and Discord integrations. **Meta kills API surfaces with little notice, and that risk lands on the owner, not on the clippers.**

## THE SMALLEST FREE-TIER TEST THAT WOULD SETTLE IT

**Four rounds on the TikTok equivalent failed by reasoning from documentation, and that pipeline has still never returned a single field. Do not repeat it.** There are two separate questions and they should be settled in this order, both at **$0 with no card**:

**TEST A, and it is the one that actually matters: IS INSTAGRAM WATCH TIME WORTH ANYTHING?** Use **Ayrshare's 28-day free trial on the Launch plan, no credit card required**, connect one Instagram professional account the owner controls, and read `igReelsAvgWatchTimeCount` on a handful of Reels at least 48 hours old. Ayrshare has the most transparent documentation of any vendor examined and the field is unambiguously specified, so this settles **whether the number exists and whether it separates a bought-view clip from a real one** without committing to any vendor. **If watch time turns out not to separate, the entire question dies here and no vendor needs choosing.** Ayrshare's price disqualifies it for production, which does not matter for a 28-day read-only test.

**TEST B, only if Test A shows the signal is real: CAN PostPeer ACTUALLY DELIVER IT CHEAPLY?** Create a PostPeer free account (email only, "No credit card required", 20 credits), read the OAuth consent screen's scope list **before authorising** to confirm `instagram_business_manage_insights` is requested, then connect the same owner-controlled account and call `GET /v1/analytics?source=platform&accountId=…`. **Look at one thing: is `avgWatchTime` a number, or null?** This simultaneously answers whether PostPeer holds the Meta approval the whole arrangement depends on, because an unverified vendor's connect flow fails at the authorise step.

**Neither test was performed this round: the brief forbade connecting any account, and nothing was signed up for.** Use an account the owner controls, never a clipper's, for both.

## CONTRADICTIONS, RESOLVED RATHER THAN AVERAGED

1. **`reels_skip_rate`, Marketing API only or not.** A community gist said Marketing API only; **Meta's own media insights page lists it under the ordinary insights permission.** The gist is wrong. Meta's caveat stands: estimated, in development.
2. **BL-781's "no vendor has Instagram watch time".** Refuted. BL-781 checked one vendor. Ayrshare (`igReelsAvgWatchTimeCount`), Metricool, Databox and PostPeer all surface it; only PostPeer also passes the pricing test.
3. **PostPeer's own prices disagree.** Pricing page $25/2,000; blog $8.50 per 1,000 and $19/4,000; auth doc "plans start at $19/month". Unresolved. Trust the pricing page, re-confirm before paying.
4. **TikTok top-5 concentration.** BL-772 says 71%; measured today, 81.8%. Definitions differ, unreconciled. The direction (Instagram far less concentrated) is unaffected.
5. **Instagram data retention.** Media insights page says 2 years; the insights guide says 90 days for user metrics. Different scopes, never reconciled by Meta.
6. **Free-curve coverage.** 96.2% here against BL-781's 94.8%, from a different "live clip" definition. Shares sound, totals definition-dependent.
7. **`instagram_business_manage_insights` grantability.** Required by three Meta reference pages, absent from Meta's own permissions reference and from every published scope list. Unresolved without a live call. **This is one more reason the free test matters.**
8. **Watch-time units.** Meta is reported to return `ig_reels_avg_watch_time` in milliseconds; PostPeer documents seconds and says it converts; Blotato documents milliseconds explicitly. UNVERIFIED.
9. **MY OWN RESEARCH ANGLES DISAGREED, and both positions are kept.** Two of five concluded no vendor passes all four tests, on the structural argument that watch time requires a per-creator OAuth connection whose cost forces per-account pricing. A third found PostPeer, whose published unit is the API call with unlimited connected accounts. **I verified PostPeer's pricing page and field documentation myself rather than siding by vote.** The structural argument is recorded in PART 2 as a reason for suspicion, not as a refutation.
10. **Ayrshare documents three fields Meta deleted.** Its current reference still lists `playsCount`, `clipsReplaysCount` and `igReelsAggregatedAllPlaysCount` for Instagram, all deprecated by Meta on 21 April 2025 across all versions. Either the documentation is stale or Ayrshare backfills them by other means. **UNVERIFIED which. Treat those three as dead; the two watch-time fields are the ones Meta still lists as live.**
11. **Ayrshare's marketing page UNDERSELLS its own API.** The analytics marketing page lists Instagram as likes, comments, impressions, videoViews and saves, never mentioning watch time, and reserves retention curves for TikTok. A buyer reading only the marketing page would wrongly conclude Instagram watch time is absent. **The reference page is both more capable and more accurate.** This is the mirror image of the bundle.social contradiction BL-768 found, where marketing overclaimed against the reference.
12. **Phyllo publishes three incompatible pricing stories** across its own pages: "Usage-based pricing" on the Instagram page, "Get a Quote" with no unit on the pricing page, and SaaS tiers of $199/$299/$899 on insightiq.ai. None states an API unit.

## WHAT COULD NOT BE ESTABLISHED

**Nothing was exercised against any live key, so every capability claim here is documentation only.** Beyond that: whether PostPeer holds Meta Tech Provider verification or App Review approval, which decides whether its connect flow works at all; whether PostPeer actually refreshes the 60-day token; its rate limits and data-retention policy, neither published; whether an unincorporated individual can complete Meta Business Verification (Meta's document-list page is JS-rendered and could not be read from the primary source, and its title, "Which Documents are Required for Incorporated and/or Registered Business Entities", is itself only suggestive); whether Meta treats a CPM payout decision as an "eligibility determination" under 3.a.ii; whether Meta construes an unlink as a deletion request; and **the share of the 361 approved Instagram accounts already on a professional account**, which is the deciding adoption number, remains unmeasurable from the schema and unrun at $0.31 for the third round running.

**Reddit and Stack Overflow returned hard 400s to the research crawler**, so the community sweep drew on Meta's developer forum, Hacker News, GitHub, Indie Hackers and vendor docs instead. That is a genuine gap in PART 1's community coverage and it is stated rather than papered over.

## SAFETY AND DISCLOSURE

READ ONLY, one document, on `checkpoint/BL-783` from `origin/main` `72f05cec`. **No code, config, schema or data change; no account connected; no payment details entered; no paid plan started; no free tier signed up for; nothing authorised; no credential stored, logged, printed or committed.** The only vendor and Meta interactions were unauthenticated public documentation fetches. Every capability, pricing and terms claim carries the vendor's or Meta's own URL, and everything unexercised is marked UNVERIFIED. Twelve read-only `SELECT`s ran through `scripts/run-select.js` against production; no write, no money, no schema, no cron touched, and no clip status, earnings or payout was read for modification or changed. No handle, caption, wallet address or email appears above; clipper identifiers are counts only. The 6 money files, `tracking.ts` and `campaign-era.ts` are untouched: this branch's diff is exactly one new markdown file. **No Apify actor was run** and the BL-678 guards were not approached. Five subagents ran, all read-only, none permitted to write a file, sign up or connect an account; their claims are reconciled against primary sources above, and the load-bearing ones (PostPeer's fields, pricing, consent flow, native-post support, terms; Meta's Reels metric list, tester ceiling, account type and conversion steps) were **re-fetched and verified by me directly rather than accepted from a summary.** The concurrent worktree at `C:/bl782` was left exactly as found. Worktree `C:/bl783` removed. No dashes as bullets. **Nothing here may auto-reject a clip or be shown to a clipper: BL-518 and BL-521 stand.**

**Rollback:** delete branch `checkpoint/BL-783`. It contains one document and touches nothing.
