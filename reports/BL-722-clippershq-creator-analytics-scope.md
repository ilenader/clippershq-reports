# BL-722 — Official creator-authorized analytics on TikTok, Instagram and YouTube: SCOPE AND PLAN

**2026-08-06 · AUDIT ONLY. READ ONLY. NOTHING BUILT.** No code, config, schema or data change. No developer account registered, no API access requested, no credential stored, no OAuth app created. Base `origin/main` `de0169bd` (Merge BL-720), branch `checkpoint/BL-722`, isolated worktree at `C:/b722`, `node_modules` never junctioned. A markdown-only diff cannot change tsc or build, so no build was run and none is claimed.

**Every capability claim below is cited to the platform's OWN documentation with a URL.** Where a fact could not be settled from official documentation it says **UNVERIFIED** and names exactly what would settle it. Live numbers are read-only `SELECT`s on prod, timestamps cast `::text` against DB `now()` = `2026-08-06 12:47:58.183911+00`.

---

## VERDICT FIRST, IN SIX LINES

1. **TikTok authorization is ONE TIME PER ACCOUNT, and later videos appear automatically.** Confirmed structurally from TikTok's own endpoint contract (PART 1.1). This is the single fact the product design rests on and it holds.
2. **The 24 to 48 hour delay does NOT block the 30-minute submission window,** because `item_id`, `create_time`, `caption`, `share_url` and `thumbnail_url` are documented as **real-time, no latency**. Ownership, existence and exact post time are provable at submit; only the analytics numbers arrive later.
3. **Instagram does NOT require a Facebook Page.** The brief's worst-case assumption is wrong: Instagram API with Instagram Login works with no Page. It still requires a professional (Business or Creator) account and Meta App Review.
4. **YouTube gives the MOST and asks the LEAST.** Per-video audience retention curves, viewer demographics and traffic sources, with no account-type conversion demanded of the clipper.
5. **The biggest win is not in the owner's list.** OAuth replaces the bio-code verification cascade, which R-5 measured failing 326 times a month across 114 clippers, TikTok worst.
6. **Do not gate withdrawal on connection.** PART 4 states the consequences plainly rather than assuming they are acceptable.

---

## PART 0 — the live numbers this plan is sized against (measured, not assumed)

The brief's "about 2,300 clips a month across about 1,240 clippers" is a July figure (R-5, 2026-07-17) mixed with the registered-user count. Measured today:

| Fact | Value |
|---|---|
| Clips submitted, last 30 days | **1,659** (R-5 measured 2,302 in July, so volume is DOWN, not up) |
| Distinct clippers who submitted, last 30 days | **101** |
| Registered users total | **1,321** |
| Live (not user-deleted) `clip_accounts` | **915**, held by **528** users |
| Clips 30d by platform | Instagram **846** (50 clippers, 640 approved) · YouTube **452** (27, 404) · TikTok **361** (51, 254) |
| APPROVED accounts by platform | TikTok **305** (266 users) · Instagram **305** (226 users) · YouTube **265** (127 users) |
| Payout requests, last 30 days | 32 PAID / $2,740.22 · 13 REJECTED / $1,791.88 · 6 open / $525.48 |
| Payout minimum | $10 (`src/app/api/payouts/route.ts:272`) |

Two consequences. **Instagram is the busiest platform by clips (51%) but TikTok has the most active clippers (51 of 101).** And the true integration population is **305 accounts per platform at most**, not 1,240 people, which makes every rate-limit ceiling below comfortable by a wide margin.

---

## PART 1 — TIKTOK, the primary target

Source of truth throughout: the **TikTok API for Business, Accounts API** documentation (a different product from the Display API at `open.tiktokapis.com`, which the brief correctly identified). The brief is right that at least one third-party summary is wrong about these fields; they are documented, verbatim, at the URLs below.

### 1.1 Is authorization ONE TIME PER ACCOUNT or per video? ONE TIME PER ACCOUNT. Confirmed.

Authorization is performed once by the TikTok account user against your developer app, producing an `auth_code` that you exchange for an account-scoped access token. The docs describe exactly one consent event and one revocation event, both account-level.
Source: [Accounts API Authorization](https://business-api.tiktok.com/portal/docs?id=1738083939371009) · [Authentication](https://business-api.tiktok.com/portal/docs?id=1738084387220481)

The endpoint that returns the data is account-scoped, not video-scoped:

> "Use this endpoint to get reach and engagement data for **all the public video, photo, or text posts of a TikTok account**."
> Request takes `business_id` (the `open_id` of the authorized account), `cursor`, `max_count`. `video_ids` exists only as an optional **filter**, never as a consent unit.
> Source: [Get post data of a TikTok account](https://business-api.tiktok.com/portal/docs?id=1762228421622786)

**Do videos posted AFTER authorization appear with no further consent?** Yes, and here is the honest form of the proof: TikTok never prints that sentence verbatim, so the claim is **structural, not quoted**. The endpoint lists the account's posts at call time; `cursor` defaults to "Current time as Epoch/Unix timestamp in milliseconds" and pages **backwards** from now; there is no per-video grant, no per-video consent parameter, and no documented step between publishing and listing. A video published after authorization is simply a newer post in the same account list. Reinforcing this, TikTok documents that a returning user is not even shown the consent page again: "if the TikTok account user has previously authorized the developer app for the same permissions, the permission scope review and approval page in Step 2 will be skipped."
**What would settle it beyond structure:** the one-clipper pilot in PART 7 step 1, which posts a video after authorizing and confirms it appears in the next list call. That is a 10-minute test and it is the whole reason the pilot exists.

### 1.2 The exact fields, quoted

**Endpoint** `GET https://business-api.tiktok.com/open_api/v1.3/business/video/list/`, header `Access-Token`, params `business_id`, `fields`, `filters`, `cursor`, `max_count`.

**Video level.** Requiring scope **`video.list`**: `item_id`, `media_type` (VIDEO / PHOTO), `is_ad`, `thumbnail_url`, `share_url`, `embed_url`, `caption`, `video_duration`, `likes`, `comments`, `shares`, `favorites`, `create_time`, `reach`, `video_views`.
Requiring scope **`video.insights`**: `total_time_watched`, `average_time_watched`, `full_video_watched_rate`, `new_followers`, `profile_views`, `website_clicks`, `phone_number_clicks`, `lead_submissions`, `app_download_clicks`, `email_clicks`, `address_clicks`, `video_view_retention` (array of `{second, percentage}`), `impression_sources` (array of `{impression_source, percentage}` where source is one of `For You`, `Follow`, `Sound`, `Personal Profile`, `Search`, `Others`, `Direct Message`), `audience_genders`, `audience_countries` (max 10, ISO 3166-1 alpha-2), `audience_cities` (max 10), `audience_types` (`NEW_VIEWER`, `RETURN_VIEWER`, `FOLLOWER_PERCENT`, `NON_FOLLOWER_PERCENT`), `engagement_likes` (array of `{second, percentage}`).
Response envelope also carries `cursor` and `has_more`.

**Account level.** `GET https://business-api.tiktok.com/open_api/v1.3/business/get/`, params `business_id`, `start_date`, `end_date`, `fields`. Fields: `is_business_account` (scope `user.account.type`), `profile_image` / `display_name` (`user.info.basic`), `username` (`user.info.username`), `profile_deep_link` / `bio_description` / `is_verified` (`user.info.profile`), `following_count` / `followers_count` / `total_likes` / `videos_count` (`user.info.stats`), and under `metrics` per `date` with scope `user.insights`: `video_views`, `unique_video_views`, `profile_views`, `likes`, `comments`, `shares`, `phone_number_clicks`, `lead_submissions`, `app_download_clicks`, `bio_link_clicks`, `email_clicks`, `address_clicks`, `daily_total_followers`, `daily_new_followers`, `daily_lost_followers`, `followers_count`, `audience_activity` (hourly), `engaged_audience`; plus `audience_ages`, `audience_genders`, `audience_countries`, `audience_cities`.
**Two hard limits on the account endpoint:** "The maximum supported look-back period is **60 days**", and the four follower-demographic fields plus `audience_activity` need "**at least 100 followers**".
Source: [Get profile data of a TikTok account](https://business-api.tiktok.com/portal/docs?id=1762228399168514)

### 1.3 What the clipper must actually do

| Requirement | Genuinely required? | Evidence |
|---|---|---|
| Publish at least one video | **YES** | "TikTok account owners need to first publish at least one video, then tap the 'Turn On' button on the Analytics page of their mobile TikTok app" ([video list doc](https://business-api.tiktok.com/portal/docs?id=1762228421622786)) |
| Tap "Turn On" on the Analytics page | **YES**, and it is retroactively blind: profile data before the day analytics was enabled is not retrievable ([Accounts API FAQs](https://business-api.tiktok.com/portal/docs?id=1776983576127490)) | same |
| Switch to a **Business** account | **NO, not for the metrics that matter.** | The Accounts API serves "TikTok Business Account **and** TikTok Personal Accounts" ([Accounts API overview](https://business-api.tiktok.com/portal/docs?id=1737944384433218)), and `is_business_account` returns `false` for a Personal Account. Every field ClippersHQ needs (`video_views`, `reach`, `full_video_watched_rate`, `total_time_watched`, `average_time_watched`, `impression_sources`, `audience_countries`, `audience_genders`, `video_view_retention`) is documented **Data source: TikTok Studio**. Only the **Business Analytics**-sourced fields carry "The data for this metric is only available for Business Accounts" (`unique_video_views`, `profile_views` at video level, `daily_*_followers`, `engaged_audience`, `audience_activity`) or "Verified Business Accounts" (`website_clicks`, `phone_number_clicks`, `lead_submissions`, `app_download_clicks`, `email_clicks`, `address_clicks`). ClippersHQ needs none of those. |
| A **Creator** account also works | **UNVERIFIED as a documented statement**, but strongly implied: TikTok's API docs recognise exactly two states, Business and Personal, and Creator is a sub-type of the non-Business side. **What would settle it:** one Creator-account clipper in the pilot returning non-null `reach` and `full_video_watched_rate`. |
| Is the Business switch free and reversible? | **UNVERIFIED from official docs.** TikTok's support article on switching redirects to a JavaScript-rendered FAQ page that returns no readable body to a fetcher, and the ads help-centre article does not state cost or reversibility. **What would settle it:** the owner, or one pilot clipper, switching and switching back on a real phone, which takes under a minute. **This is not on the critical path,** because 1.3 above shows the switch is not needed. |

### 1.4 Scopes, consent screen, app review, timeline

**Scopes needed:** `video.list` and `video.insights` for post data; `user.info.basic` plus `user.insights` if account-level data is wanted. The developer app must carry the **"TikTok Accounts"** permission scope. A live token's granted scopes are readable via `/tt_user/token_info/get/`.

**Consent screen:** the account holder opens the app's "TikTok account holder authorization URL", "reviews and approves the authorization request", and is redirected to a registered HTTPS redirect URL carrying `auth_code` (valid **10 minutes**, single use). Redirect URLs must be absolute HTTPS, end with `/`, carry no query string, no anchor and no port. The exact consent-screen wording is shown only as a screenshot in TikTok's docs, so the literal text is **UNVERIFIED**; what is documented is that the user reviews the permission scope, approves, and "can revoke the authorization at any time from within the TikTok app".

**App review: required, and there are now TWO gates.**
• Gate 1: create a TikTok for Business account, register as a developer, create a developer app with the scopes selected. "You have now submitted your developer application for review. The review may take **2 to 3 business days**." Each developer may hold up to five apps. Source: [Create a developer app](https://business-api.tiktok.com/portal/docs?id=1738855242728450)
• Gate 2, and this is new and load-bearing: "starting **March 20, 2026** at 00:00 (GMT+0), developers must complete the **Accounts API Access Application Form** before submitting a new developer app or requesting a scope increase that includes the 'TikTok Accounts' permission scope." This notice is repeated on the overview, the API reference, the FAQs and both insights endpoints. **No timeline is published for this form**, so the honest estimate is: 2 to 3 business days for the app itself, plus an **unbounded, UNVERIFIED** wait on the Accounts API access form. Plan for weeks, not days, and do not build a product surface that assumes approval.

**A prohibited-use clause the owner must read before any of this starts.** TikTok's own overview lists, under **Prohibited Uses of Accounts API**: "Extract reports of TikTok profiles and posts from authorized creators' accounts, and use the aggregated data to develop a **self-built affiliate influencer marketing program (such as creator discovery and ranking)**, instead of using the TikTok One platform or API." ClippersHQ is a platform that pays creators CPM for brand campaigns and ranks them. The intended use here is narrow and defensible (verifying the view count of a clip the creator submitted for payment on their own account, at their own request), and it is not creator discovery. But the boundary is real, TikTok "reserves the right to revoke a developer's Accounts API access at any time without prior notice", and the application form is where this gets judged. **The app description must describe payment verification for the creator's own submitted post, and must not describe discovery, ranking or a creator marketplace.** Getting this wrong loses the access, not just the round.

### 1.5 Rate limits, quotas, pagination, against the real volume

Documented ceilings ([Accounts API rate limits](https://business-api.tiktok.com/portal/docs?id=1738084416214017), [global rate limits](https://business-api.tiktok.com/portal/docs?id=1740029171730433)):
• **40 QPM per authorized TikTok account per endpoint.**
• **600 QPM** across all Accounts API endpoints combined at the default **Basic** app level (1,000 at every higher level).
• Global Basic: 10 QPS, 600 QPM, **864,000 QPD**. Throttling returns `"code": 40100`.
• Pagination: `max_count` default 10, **maximum 20**; `cursor` is a UTC millisecond timestamp; `has_more` drives the next page. "it is possible that the endpoint returns less than `max_count` number of videos even if `has_more` is true."

**The design against the ceiling.** The realistic worst case is every one of the **305 approved TikTok accounts** connected and polled hourly for its newest page:

| Design | Calls per day | Peak QPM if evenly spread | Against ceiling |
|---|---|---|---|
| 305 accounts, 1 page, hourly | **7,320** | ~5 | 0.8% of the 864,000 QPD Basic; ~0.9% of 600 QPM |
| 305 accounts, 1 page, every 15 minutes | **29,280** | ~20 | 3.4% of QPD; ~3.4% of QPM |
| Plus a same-hour re-check per new clip (361 clips / 30d ≈ 12/day) | +12 | negligible | negligible |

**It fits with two orders of magnitude to spare, at the default Basic level, with no rate-limit increase requested.** The per-account 40 QPM limit is never approached because a given account is called once per hour. The only pagination risk is an account with a long back catalogue where the target clip is many pages deep; that is solved by passing `cursor` set to the clip's submit time, which is exactly what the cursor is documented to do.

### 1.6 Token lifetime, refresh, revocation

| Fact | Value | Source |
|---|---|---|
| `auth_code` | **10 minutes**, single use | [Authorization](https://business-api.tiktok.com/portal/docs?id=1738083939371009) |
| Access token | **1 day** (`expires_in: 86400`) | [Authentication](https://business-api.tiktok.com/portal/docs?id=1738084387220481) |
| Refresh token | **1 year** (`refresh_token_expires_in: 31536000`) | same |
| Renewal | `POST /open_api/v1.3/tt_user/oauth2/refresh_token/` with `grant_type=refresh_token`; returns a fresh access token AND a fresh refresh token | same |
| Refresh token expiry | "the developer needs to request the user to re-authorize their application" | same |
| Revocation, by us | `POST /open_api/v1.3/tt_user/oauth2/revoke/` | same |
| Revocation, by the clipper | TikTok app: Settings and privacy > Security > Manage app permissions > select the app > Remove access | [Accounts API FAQs](https://business-api.tiktok.com/portal/docs?id=1776983576127490) |

A 1-day access token means **a daily refresh job is mandatory, not optional**. Note the refresh response returns a new `refresh_token` with a rolling `refresh_token_expires_in` (the docs' own example shows `28484364`, about 330 days), so an account refreshed regularly never hits the 1-year wall; an account left un-refreshed for a year does.

### 1.7 The two data caveats, confirmed, and what they mean for a 30-minute window

**Confirmed caveat 1, the 24 to 48 hour delay.** "There is a 24-48 hour delay for some profile level metrics." The [data latency reference table](https://business-api.tiktok.com/portal/docs?id=1746624508278786) splits the fields precisely:
• **No latency (real-time):** `item_id`, `create_time`, `thumbnail_url`, `share_url`, `embed_url`, `caption`.
• **24 to 48 hours (UTC):** `video_views`, `likes`, `comments`, `shares`, `reach`, `video_duration`, `full_video_watched_rate`, `total_time_watched`, `average_time_watched`, `impression_sources`, `audience_countries`.

**This is the most important product fact in the whole document and it is good news.** The 30-minute posting window (`MAX_CLIP_AGE_MS` in `src/lib/clip-config.ts`) exists to prove a clip was posted for this campaign, not recycled. That question is answered by `create_time`, which is **real-time**. So at submit, with zero delay, the platform can prove: this post exists, it belongs to the authorized account (the list is account-scoped, so appearing in it IS proof of ownership), it was published at exactly this UTC second, and this is its caption. The view count was never available at minute zero from any source anyway; today's tracking cron discovers it later too. **Nothing about the 30-minute window is harmed. What changes is that ownership and post time stop being inferred from a scraped page and start being stated by TikTok.**

**Confirmed caveat 2, the 7-day inactivity hole.** "If the data for the fields `reach`, `full_video_watched_rate`, `total_time_watched`, `average_time_watched`, `impression_sources`, and `audience_countries` are unavailable, the reason is usually that the video has not been active (viewed/liked/commented/shared) for more than 7 days. To retrieve the data for these fields, you can view/like/comment/share the inactive video and retry after 24 ~ 48h."
**Read the list carefully: `video_views` is NOT in it.** The money metric survives. What goes missing on a dead clip is the quality and audience detail, which is exactly the clip nobody is arguing about. Two further limits from the same note: "Post data will stop updating **365 days** after the post is published", and a post filtered for violations (music copyright is the example given) simply does not appear in the list at all, which must be treated as **fail open**, never as "the clipper deleted it" (this is the same trap BL-720 just spent a round closing on the HikerAPI 404).

---

## PART 2 — INSTAGRAM

### 2.1 Which API, and the account-type question answered bluntly

Meta offers two configurations ([Instagram Platform overview](https://developers.facebook.com/docs/instagram-platform/overview)):
• **Instagram API with Instagram Login:** serves "Instagram professional accounts with a presence on Instagram only". A linked Facebook Page is **not required**.
• **Instagram API with Facebook Login:** requires the Instagram professional account to be linked to a Facebook Page.

**The brief's fear is wrong, and this materially changes Instagram's ranking.** ClippersHQ needs insights only, so **Instagram Login is the correct choice and no Facebook Page is involved**. The friction that remains is one real step: **the clipper's Instagram account must be a professional account (Business or Creator).** Both are supported. Confirmed: "Instagram professionals — businesses and creators" ([Instagram API with Instagram Login](https://developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login)).

### 2.2 The metrics

Per-media insights ([IG Media Insights reference](https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-media/insights)). For **Reels**, which is what ClippersHQ tracks: `views`, `reach`, `likes`, `comments`, `shares`, `saved`, `total_interactions`, `reposts`, `crossposted_views`, `facebook_views`, **`ig_reels_avg_watch_time`**, **`ig_reels_video_view_total_time`**, **`reels_skip_rate`**. Permissions: `instagram_business_basic` and `instagram_business_manage_insights` (Instagram Login) or `instagram_basic`, `instagram_manage_insights`, `pages_read_engagement` (Facebook Login).

**What Instagram does NOT give at post level: audience demographics.** There is no per-media country, age or gender breakdown in the list above. Demographics exist only as account-level follower demographics. So Instagram delivers **watch time and skip rate but no per-clip audience geography**, which is a real gap versus TikTok's `audience_countries` and YouTube's `ageGroup`/`gender` filters.

**Delay:** "Data used to calculate metrics can be delayed up to **48 hours**" (same reference). Same shape as TikTok, same conclusion for the 30-minute window.

### 2.3 Tokens, review, rate limits

| Fact | Value | Source |
|---|---|---|
| App type | Meta app must be a **Business** type app | [Get started](https://developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login/get-started) |
| Authorization code | valid **1 hour**, single use | [Business Login](https://developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login/business-login) |
| Short-lived token | **1 hour** | same |
| Long-lived token | **60 days**, obtained via `grant_type=ig_exchange_token` | same |
| Refresh | `grant_type=ig_refresh_token`, and "The existing long-lived access token is at least **24 hours** old" | same |
| Expiry | "Tokens that have not been refreshed in **60 days** will expire and can no longer be refreshed" | same |
| App Review | Advanced Access required when "your app serves multiple businesses"; requires app icon 1024x1024, privacy policy URL, app category, business email, step-by-step reviewer test instructions, a screencast of the end-to-end experience per permission, and **at least 1 successful API call** per requested permission | [App Review](https://developers.facebook.com/docs/instagram-platform/app-review) |
| Review timeline | **UNVERIFIED.** Meta's app-review page states no timeline. What would settle it: submitting one. | same |
| Business Verification | **UNVERIFIED.** Not named as a requirement on the Instagram app-review page. What would settle it: the App Dashboard's own requirement checklist at submission time, which is only visible inside a real Meta app. | same |
| Rate limit | "Calls within 24 hours = **4800 * Number of Impressions**", where impressions is how often the account's content appeared on screens in the preceding 24 hours | [Rate limiting](https://developers.facebook.com/docs/graph-api/overview/rate-limiting) |

**The rate-limit formula is a genuine hazard and deserves to be said plainly.** The ceiling scales with the clipper's OWN reach. A large clipper has an effectively unlimited budget. A brand-new or low-reach clipper account, which is a meaningful share of this platform's Instagram population, has a budget that shrinks toward zero exactly when their content is not performing. A design that polls a quiet account hourly can throttle itself on the smallest accounts. The mitigation is event-driven and cheap: poll an IG account only while it has a clip inside its tracking window, and back off hard on a throttle rather than retrying.

### 2.4 How many existing Instagram clippers could realistically complete this?

The onboarding cost is now **one step, not two**: convert to a professional account (Business or Creator) inside the Instagram app, then authorize. No Facebook Page, no page creation, no page admin role.

**Honest position: this cannot be measured from our database, because ClippersHQ stores no Instagram account-type field.** `clip_accounts` holds `platform`, `username`, `profileLink`, `followerCount`, `status` and the `lastVerify*` snapshot, and nothing about professional versus personal.

**What would settle it exactly, and cheaply:** HikerAPI's profile response carries the account-type flags. A one-call-per-profile census across the **305 approved Instagram accounts** would give the real number, at the same cost profile as BL-720's 113-profile census (which cost about $0.13 for 129 probes, so roughly **$0.31** here). **That census is step 0 of any Instagram work and it should be run before a single line is written.**

**Until it runs, the only defensible estimate is a range, stated as an estimate:** clippers who chase CPM already read their own analytics, and reading Reels analytics already requires a professional account, so the already-converted share is plausibly high; but "plausibly high" is not a measurement, and a flow that half the population abandons is worse than none on the busiest platform. **Do not build Instagram on an estimate. Run the census.**

---

## PART 3 — YOUTUBE

### 3.1 What it gives, and it is more than the other two

**YouTube Analytics API** ([metrics](https://developers.google.com/youtube/analytics/metrics), [channel reports](https://developers.google.com/youtube/analytics/channel_reports)):
• Core: `views`, `engagedViews`, `estimatedMinutesWatched`, `averageViewDuration`, `likes`, `dislikes`, `comments`, `shares`, `subscribersGained`, `subscribersLost`.
• **Audience retention, at video level:** dimension `elapsedVideoTimeRatio`, metrics `audienceWatchRatio`, `relativeRetentionPerformance`, `startedWatching`, `stoppedWatching`, `totalSegmentImpressions`. Required filter: a single `video` id ("does not support the ability to specify a comma-separated list"). This is a full retention **curve**, and `relativeRetentionPerformance` compares the video against similar-length YouTube videos, which nothing on TikTok or Instagram offers.
• **Viewer demographics:** dimensions `ageGroup` and/or `gender`, metric `viewerPercentage`, filterable by `video`.
• Traffic sources and playback detail dimensions are available in the same report family.

**Plainly: YouTube offers more than TikTok and far more than Instagram,** and it is the platform ClippersHQ currently gets the least from. Today the submit path fetches only `snippet.publishedAt` plus `statistics` and does not even request `contentDetails` (BL-662), so YouTube is simultaneously the richest available source and the least used.

### 3.2 Who authorizes, scopes, review, quota, tokens, delay

**Who authorizes:** "All YouTube Analytics and YouTube Reporting API requests must be authorized by the channel or content owner that owns the requested data" ([data model](https://developers.google.com/youtube/analytics/data_model)). The clipper is the channel owner, so a standard Google OAuth consent is all that is needed. **No account-type conversion, no professional switch, no page.** This is the lowest clipper friction of the three by a wide margin.

**Scopes** ([authorization](https://developers.google.com/youtube/reporting/guides/authorization)): `https://www.googleapis.com/auth/yt-analytics.readonly` ("View YouTube Analytics reports for your YouTube content") is the only one required. `yt-analytics-monetary.readonly`, `youtube.readonly`, `youtube` and `youtubepartner` exist and are **not needed**; requesting the narrowest scope is also a stated Google verification requirement.

**Review:** `yt-analytics.readonly` is a **sensitive** scope, so the app must pass **Google OAuth app verification** before general availability. Requirements ([verification requirements](https://support.google.com/cloud/answer/13464321)): an appropriate use case, a demonstration video showing the end-to-end flow **including the consent screen with the requested scopes in English**, limited data use, and narrowest-scope justification. A **security assessment is required only for RESTRICTED scopes**, and `yt-analytics.readonly` is sensitive, not restricted, so **no annual third-party security assessment applies**. Timeline: **UNVERIFIED**, Google publishes none.

**Tokens** ([OAuth 2.0](https://developers.google.com/identity/protocols/oauth2)): refresh tokens do not expire on a fixed clock for a published app; they are invalidated when the user revokes, when unused for **six months**, or when limits are exceeded. **The trap to know before the pilot:** "A Google Cloud Platform project with an OAuth consent screen configured for an external user type and a publishing status of 'Testing' is issued a refresh token expiring in **7 days**". A pilot run in Testing status will silently break after a week and it will look like a bug.

**Quota:** the YouTube **Data** API default is "100 `search.list` calls, 100 `videos.insert` calls, and **10,000 units per day** combined for all other endpoints", a list read costing 1 unit ([getting started](https://developers.google.com/youtube/v3/getting-started)). For the **Analytics** API, "Each API request that you make counts as one unit of your API usage quota", with the numeric ceiling shown only in the project's Cloud Console: **the exact default is UNVERIFIED and would be settled by reading the Quotas panel of a real project.** Sizing: 265 approved YouTube accounts polled hourly is 6,360 calls a day, plus a per-video retention call per tracked clip; that fits inside a 10,000-unit-class budget only loosely, so YouTube is the one platform where **poll cadence must be event-driven from the start** rather than a flat hourly sweep.

**Delay:** the docs state the response "contains data up until the last day specified for which all metrics in the query are available", and do not publish a fixed number of hours. Exact delay **UNVERIFIED**; the observable behaviour is the same order as the other two and would be settled by the pilot.

---

## PART 4 — THE PRODUCT FLOW

### 4.1 The three gating options, judged

| Option | Plausible completion | What happens to a refuser | Can a refuser still earn and withdraw? |
|---|---|---|---|
| **A. Connect at account-link time** (the existing "add an account" flow becomes "add and connect") | **High for NEW accounts**, because the clipper is already mid-flow and already about to do a bio-code dance that fails 53% of the time today. **Low for the 875 accounts already approved**, who have no reason to return. Estimate, not a measurement. | Nothing. They verify by bio code as today. | **YES, unchanged.** |
| **B. Optional, with an incentive** (faster approval, a visible "verified analytics" badge, priority review, or a small CPM bonus) | **Moderate.** Reaches existing accounts, which A does not. Adoption depends entirely on the size of the incentive, and is unmeasurable in advance. | Nothing. | **YES, unchanged.** |
| **C. Required to withdraw** | **Highest raw completion, because the money forces it.** | They hit a wall holding earned money. | **NO. This is the entire problem.** |

**Recommendation: A plus B. Never C as a hard gate.**

### 4.2 Withdrawal gating is a POLICY DECISION, and here are its consequences, stated rather than assumed

The owner proposed "to withdraw, verify your account". It would work. It is also the single most dangerous thing in this document, and this platform's own recent history is the argument:

• **BL-518** removed every automatic system that could change a clip's status, on the owner's own rule that a clipper must never be punished by a machine. **BL-521** proved a clipper never sees a machine's suspicion. A withdrawal gate is a machine deciding whether a human may be paid. It is the same shape as the thing BL-518 deliberately removed.
• **BL-689** exists because three clippers holding **$52.86** hit a permanent refusal that was reported to them as "Something went wrong. Please try again", advice they could never succeed at. That was an accident. A withdrawal gate makes it a **feature**.
• **BL-698 and BL-720** together spent two rounds on the fact that a wrong machine verdict stripped **$3,583.50** of displayed balance from clippers whose posts a human could still open. The lesson learned there was that the bar for a machine blocking money must be "no human can see it", not "our provider returned an error".
• A refresh failure, a TikTok outage, a Meta throttle on a low-reach account, a revoked token, or a clipper who simply changed phones would each become a **payment block**. The failure mode of an analytics integration is normally "we fall back to the scraper". Under option C the failure mode becomes "the clipper is not paid".

**If the owner reads all of that and still wants C, these are the minimum conditions, and they are not negotiable if BL-518 and BL-521 are to keep meaning anything:**
1. **Never retroactive.** Money already earned at the moment the rule ships is withdrawable forever with no connection.
2. **A human override with a stated SLA**, reachable from the blocked screen itself, not from Discord.
3. **The gate must fail OPEN on every technical failure.** A refresh error, a 5xx, a throttle or an expired token releases the payout; only a clipper who has never connected at all is ever stopped.
4. **A measured completion rate before it becomes mandatory,** from a period where connection is optional. Shipping a gate without knowing the completion rate is shipping an unknown number of unpaid clippers.
5. **It applies at most to ONE platform at a time**, the one where the flow is proven.

### 4.3 Token storage, and the key-loss question answered properly

**First, a correction to the brief's premise.** The owner did not decline wallet encryption. `src/lib/wallet-crypto.ts` implements **AES-256-GCM** (12-byte IV, 32-byte key, 16-byte tag), `WALLET_ENC_KEY` is **live in Railway**, and BL-656 measured **81 of 133 payout rows already encrypted**. What was deferred is **dropping the plaintext column**, and BL-656 gives the exact reason: "Key loss is only catastrophic AFTER the plaintext column is dropped. That is precisely why the plaintext net must stay until the key is proven backed up."

**That reasoning does not transfer to OAuth tokens, and the difference is the whole answer.** A wallet address is **irreplaceable data**: lose it and the owner cannot pay someone. An OAuth token is **regenerable**: lose the key and the cost is one re-authorization prompt per clipper. Nothing is destroyed and no money moves. Therefore:

• **Store tokens encrypted only, with NO plaintext column and no plaintext fallback.** A plaintext fallback for a token is not a safety net, it is the leak the encryption exists to prevent. This is the opposite of the wallet decision and it is opposite for a defensible reason.
• **Use a separate key, `OAUTH_TOKEN_ENC_KEY`, not `WALLET_ENC_KEY`.** Different blast radius, different rotation cadence, and rotating one must not touch the other.
• **Key rotation is cheap here.** Rotate the key, every stored token fails to decrypt, every affected clipper is asked to reconnect once. Annoying, not catastrophic. That property is what buys the right to store no plaintext.
• **Never log a token, never return one to any API response, never put one in an error message.** The `[TAG]` logging convention must exclude these fields explicitly.
• **Store next to the account, not the user:** a `clip_account_connections` row keyed by `clipAccountId` carrying platform, provider account id (`open_id` for TikTok), encrypted access token, encrypted refresh token, both expiry timestamps, granted scopes, `connectedAt`, `lastRefreshAt`, `lastRefreshError`, `revokedAt`. Additive table, `CREATE TABLE IF NOT EXISTS`, never `prisma migrate`.

### 4.4 The refresh job, and every failure path

| Platform | Cadence needed | Why |
|---|---|---|
| TikTok | **daily**, plus refresh-on-use if older than ~20 hours | access token 1 day, refresh token 1 year rolling |
| Instagram | **every ~30 days**, and never sooner than 24 hours after the last refresh | long-lived token 60 days, minimum 24h age, dead after 60 days unrefreshed |
| YouTube | **none scheduled**; refresh on use | refresh token does not expire on a clock once published |

**Failure handling, and it must be boring:**
• A refresh failure is **not** a clipper problem until it has failed repeatedly. Record `lastRefreshError`, retry with backoff, and only after a documented number of consecutive failures mark the connection `NEEDS_RECONNECT`.
• `NEEDS_RECONNECT` produces **one** clipper-facing prompt to reconnect, worded as a reconnection request and never as suspicion (BL-521).
• **Revocation, expiry and disconnection all do exactly the same thing: the platform falls back to HikerAPI, LamaTok or the YouTube Data API, the clip keeps tracking, and the clipper keeps earning.** Nothing about a disconnected clipper's money changes, ever.
• **Does a clipper lose anything by disconnecting?** Only the badge and whatever incentive option B attaches. Not tracking, not earnings, not withdrawal. If disconnecting can cost a clipper money, the design is wrong.
• Honour revocation in both directions: call `/tt_user/oauth2/revoke/` when a clipper disconnects on our side, and delete the stored tokens the moment a refresh returns an invalid-grant, so a revoked token is never retried.

---

## PART 5 — WHAT THIS REPLACES, WHAT IT IMPROVES, WHAT IT DOES NOT TOUCH

### 5.1 Replaced outright, for connected accounts

**The analytics screenshot reader (BL-636, BL-650).** Status today: `OCR_SPACE_API_KEY` unset, **0 production screenshots ever uploaded**, **OCR image-to-text accuracy UNMEASURED**, and BL-650's own verdict is that the parsing layer is proven (43/43) while the OCR layer has never run. Official analytics makes the entire question moot for a connected account: there is no image, no OCR, no "42% read as 4%" failure mode, and no need for the owner to supply 15 to 20 ground-truth screenshots per platform per resolution to measure something. **Keep the reader for unconnected accounts; it stops being on the critical path.**

**The bio-code verification cascade, and this is the biggest win in the document.** R-5 measured **617 verify attempts producing 326 NEEDS_ADMIN escalations from 114 distinct clippers in 30 days**, TikTok worst at 212 with `cappedAtTier1` proving it has no tier-2 fallback, YouTube 108. R-5 could not price it because there is no audit action for a manual account approval and the cost lands in Discord DMs, so it is "a large user-facing failure of unproven owner cost". **An OAuth token is strictly better proof of ownership than a code in a bio**: it comes from the platform, it cannot be faked by editing a profile, it does not need a scraper, it cannot be defeated by a bot wall, and it never returns `cappedAtTier1`. This was not on the owner's list of things to replace and it is the strongest single argument for the project.

**The owner's manual screen-share calls before payout.** Replaced for connected clippers: the numbers arrive from the platform instead of from a shared screen. **Honest limit: R-5 could not price these either** (no audit action, the cost is in Discord and on calls), so the saving is real and **unquantified**. Any number put on it here would be invented.

### 5.2 Improved, not replaced

**BL-599's peer-relative bot-detection rank.** It fires on **3.2%** of clips (87 of 2,707 APPROVED evaluated) and infers "bought views" from a like-rate outside the platform-and-niche band. With official data the inference becomes an observation: `impression_sources` shows whether views came from For You, Search, Sound or Personal Profile; `audience_types` splits new versus returning and follower versus non-follower; `video_view_retention` shows whether anyone actually watched. A clip with 300k views, 0.1% likes, 95% "Others" traffic and a retention curve that dies at second one is no longer a statistical suspicion. **BL-599 stays: it is the only signal that works on the ~70% of accounts that will not be connected for a long time.** And BL-599's rule that the signal ranks and never rejects (BL-518) applies unchanged to anything built here.

**The reviewer note layer (BL-666).** It composes machine findings and blind spots for a human reviewer. Official analytics adds a class of finding that is a fact rather than an inference. It does not change that the bot decides nothing.

### 5.3 What this does NOT replace, stated so nobody plans around it

**It does not dent R-5's 14.9 owner hours a month.** That 14.9 hours (76% of measurable owner console time, 1,130 decisions, median 25 seconds each) is **judging a clip against prose campaign rules**: logo placement, card colours, edit quality. R-5 traced the root cause and it is that `requirements`, `bannedContent`, `captionRules` and `hashtagRules` are free text validated for length only, so "while a rule is prose, a human must read every clip against it". No amount of official view data reads a rule about logo placement. **R-5's single highest-value action, scoping the 4 unreviewed campaigns to the existing reviewer, is still the answer to the 14.9 hours, and this project does not compete with it.** Against the 1,659 clips of the last 30 days, this project changes how a clip's numbers and ownership are established, not how its content is judged.

**It cannot replace tracking, and it will not be able to for a long time.** HikerAPI, LamaTok and the YouTube Data API remain load-bearing for: every unconnected clipper (today that is 100% of 915 accounts); every clip on an account whose token expired or was revoked; the gone-clip retirement logic built in BL-720, which needs a public-visibility probe that no authorized-analytics endpoint answers; and the entire `clip_stats` history. **This is ADDITIVE. It is a second, better source for the accounts that opt in, running alongside the existing providers, and it can only replace a provider on the day adoption for that platform is high enough that the provider is idle. That day is not close, and no plan should be written assuming it.**

---

## PART 6 — COST AND EFFORT, HONESTLY

**API cost: $0 on all three.** TikTok publishes no per-call price for the Accounts API; Meta's Instagram Platform is free within the rate-limit formula; YouTube Data and Analytics are free within quota. **The cost of this project is engineering rounds, owner paperwork, and clipper friction, not vendor spend.** The one measurable cash cost identified anywhere in this document is roughly **$0.31** for the 305-profile HikerAPI census that would measure Instagram's real onboarding gap.

| Platform | Owner paperwork | Clipper friction | Engineering | Data value |
|---|---|---|---|---|
| **YouTube** | Google Cloud project, OAuth consent screen, verification for one sensitive scope, demo video | **Lowest.** Sign in with Google. No conversion, no switch, no Page. | **3 to 4 rounds** (OAuth flow, token store, Analytics client, retention/demographics read) | **Highest.** Retention curve, relative retention, demographics, traffic source |
| **TikTok** | TikTok for Business account, developer registration, developer app (2 to 3 business days), **Accounts API Access Application Form, timeline UNVERIFIED** | **Low.** Publish one video (already done), tap "Turn On" once, authorize once. **No Business switch needed.** | **4 to 6 rounds** (OAuth, token store, daily refresh cron, video list client, short-link to `item_id` matching, fallback logic) | **High.** Views, reach, watch time, full-watch rate, retention, traffic source, countries, viewer types |
| **Instagram** | Meta Business app, App Review with screencasts and a working API call per permission, **Business Verification UNVERIFIED** | **Medium.** Convert to a professional account inside the IG app. No Facebook Page. | **5 to 7 rounds** (OAuth, token store, 30-day refresh, insights client, and a reach-scaled rate-limit budgeter that the other two do not need) | **Lowest.** Watch time and skip rate, but **no per-post audience demographics** |

**Ranked by value per unit of effort:**
1. **YouTube.** Best data, least friction, fewest unknowns. It also fixes the platform's weakest link: today YouTube submit fetches `publishedAt` and `statistics` and nothing else.
2. **TikTok.** Second on effort, **first on strategic value**, because it carries the most active clippers (51 of 101) and because the verification cascade fails worst there (212 escalations a month, no tier-2 fallback). The Accounts API access form is the only real unknown and it is an owner action, not an engineering one, so it can start in parallel with YouTube work.
3. **Instagram, and yes, it is a poor second step despite carrying 51% of the clips.** Its per-post data is the weakest of the three (no demographics), it needs the most engineering, its rate limit shrinks precisely on the small accounts most likely to need checking, and it is the only platform where a real share of the population must change their account type before anything works at all. **Volume is not the same as value here.** Instagram should be third, and it should not start until the 305-account census says what fraction of clippers are already professional.

---

## PART 7 — THE ORDERED PLAN

Nothing in this plan is started before the owner approves it. Every step names what must be TRUE before it begins, and every step is stoppable.

**Step 0. Two owner decisions and one cheap measurement.** No code.
• **Decision A:** approve or reject the PART 4 recommendation (connect at link time plus optional incentive, never a hard withdrawal gate). If the owner wants the gate, he accepts the five conditions in 4.2 in writing first.
• **Decision B:** approve the wording of the TikTok Accounts API Access Application Form as "payment verification for the creator's own submitted post", explicitly not creator discovery or ranking (PART 1.4). Getting this wrong costs the access permanently.
• **Measurement:** run the 305-account HikerAPI professional-account census (about $0.31, read-only, one call per profile, same shape as BL-720's census). This is the only number that decides whether Instagram is ever worth building.

**Step 1. The smallest possible pilot: ONE platform, ONE clipper, no product surface.**
Prerequisite: nothing except a Google Cloud project. **Platform: YouTube**, because it needs no clipper account conversion and no third-party approval to begin.
Scope: a local script, run by hand, that authorizes exactly one consenting clipper's channel and reads `views`, `estimatedMinutesWatched`, `averageViewDuration` and one `elapsedVideoTimeRatio` retention curve for one already-submitted clip. Compare every number against what the YouTube Data API already reports for that clip.
**What it proves:** the data arrives, it matches, and the retention curve is real. **What it also catches, and this is why it is first:** the Testing-status 7-day refresh-token trap (PART 3.2), which would otherwise be discovered in production a week later disguised as a bug.
**Stop condition:** if the numbers do not reconcile with the existing tracker, stop and report. Do not build on a source that disagrees with the one already paying people.

**Step 2. Owner paperwork, in parallel with step 1, because both are queues.**
• TikTok: create the TikTok for Business account, register as developer, submit the Accounts API Access Application Form, then the developer app with `video.list`, `video.insights`, `user.info.basic` (2 to 3 business days for the app, unknown for the form).
• YouTube: submit Google OAuth verification for `yt-analytics.readonly` with the demo video.
**These are owner actions and cannot be delegated to an agent.** **STOP CONDITION: if TikTok rejects the Accounts API access, the entire TikTok branch of this plan stops.** There is no second route to these fields; the Display API at `open.tiktokapis.com` returns counters only, exactly as the brief said. In that case YouTube proceeds alone and Instagram is re-judged on the census.

**Step 3. The connection store and the refresh job. Still no clipper-facing surface.**
Prerequisites: step 1 proved the data, and at least one platform is approved.
Build: the additive `clip_account_connections` table (`CREATE TABLE IF NOT EXISTS`, never `prisma migrate`), `OAUTH_TOKEN_ENC_KEY` reusing the AES-256-GCM pattern of `src/lib/wallet-crypto.ts` with **no plaintext column**, the OAuth callback route, and the refresh cron behind `CRON_SECRET` like every other cron. Nothing reads this data yet. Nothing a clipper sees changes. The 6 money files, `tracking.ts` and `campaign-era.ts` must be byte-identical by blob OID.

**Step 4. Shadow read, owner-only, for a measured period.**
Prerequisite: step 3 shipped and at least 5 clippers connected voluntarily.
For every connected account, fetch official numbers alongside the existing provider numbers and store both. Show the owner the delta, owner-only, read-only, no action buttons, exactly the discipline BL-599 and BL-666 already follow. **Nothing decides anything.** This is the round that answers the question nobody can answer today: how far apart are the scraped number and the platform's own number, and in which direction.

**Step 5. Clipper-facing connection, behind `isTestUser`.**
Prerequisite: step 4 produced a delta the owner accepts.
The connect button appears in the account-link flow for test clippers only. Every non-test user is byte-identical to before. Accessibility review before it ships, as with every UI round here.

**Step 6. General availability, plus the incentive.**
Prerequisite: step 5 ran clean on test clippers, and the completion rate is measured rather than estimated.
Only now does option B's incentive attach, and only now is there a real completion number to decide whether option C was ever worth discussing.

**Where this plan stops, per platform:** TikTok stops at step 2 if the Accounts API access form is refused. Instagram never starts if the census says most clippers are on personal accounts. YouTube stops at step 1 if the numbers do not reconcile. **Each branch dies independently and none of them can take the money path with it, because through step 4 nothing this project builds is allowed to read or write a clip's status, earnings or payout.**

---

## What could NOT be verified, and exactly what would settle each

| Claim | Status | What settles it |
|---|---|---|
| Videos posted after authorization appear automatically | **Structurally proven, not quoted** | Pilot: authorize, post, list |
| TikTok Creator (not Business, not plain Personal) accounts return the Studio-sourced fields | **UNVERIFIED** | One Creator-account clipper in the pilot returning non-null `reach` |
| Whether the TikTok Business switch is free and reversible | **UNVERIFIED** (TikTok's support FAQ is JavaScript-rendered and returns no readable body; the ads help article omits it) | One switch and switch-back on a phone. Not on the critical path, since PART 1.3 shows the switch is unnecessary |
| Exact TikTok consent screen wording | **UNVERIFIED** (shown only as a screenshot in TikTok's docs) | Running the authorization URL once |
| TikTok Accounts API access form review timeline | **UNVERIFIED** (TikTok publishes none) | Submitting it |
| Meta App Review timeline, and whether Business Verification is required for Instagram insights | **UNVERIFIED** (Meta's app-review page states neither) | The App Dashboard's own submission checklist inside a real Meta app |
| Exact YouTube Analytics API daily quota | **UNVERIFIED** ("one unit per request"; the numeric ceiling is per-project in the Cloud Console) | Reading the Quotas panel of a real project |
| Exact YouTube Analytics data delay in hours | **UNVERIFIED** (docs describe availability, not a fixed lag) | The pilot |
| Share of the 305 Instagram accounts already on a professional account | **UNVERIFIED, and it is the deciding number for PART 2** | The ~$0.31 HikerAPI census in step 0 |
| Owner hours saved on screen-share calls | **UNPRICEABLE** (R-5: no audit action exists, cost lands in Discord) | An audit action, or the owner timing a month |

---

## Safety and disclosure

READ ONLY, one document, on branch `checkpoint/BL-722` from `origin/main` `de0169bd`. **No code, config, schema or data change. No developer account registered, no API access requested, no OAuth app created, no credential stored, no platform API called.** The only network calls made were fetches of public documentation (TikTok's own docs portal, Meta's developer docs, Google's developer docs) and of prior reports from `ilenader/clippershq-reports`; **zero calls were made to any platform data API**, so no token exists to store and no quota was consumed. Six read-only `SELECT`s ran via `scripts/run-select.js` (which refuses any write keyword) against prod on 2026-08-06, all timestamps cast `::text` against DB `now()`; **no write, no money, no schema, no config, no cron touched.** No clipper handle, caption, wallet address, email or personal string appears anywhere above. The 6 money files, `tracking.ts` and `campaign-era.ts` are untouched: this diff contains exactly one markdown file. Isolated worktree at the short path `C:/b722`, `node_modules` never junctioned; `.env.local` was copied in for the read-only SELECT runner and is confirmed gitignored, so it cannot be committed. Nothing a live round holds was touched (the `main` working tree is held by worktree `C:/b575`, and this round never checked out `main`). A markdown-only diff cannot change tsc or build, so no build was run and none is claimed. Every capability claim carries an official URL, and every unverifiable claim is marked UNVERIFIED with the exact test that would settle it. BL-518 and BL-521 are restated as non-negotiable and nothing designed here may change a clip's status or block a clipper's money. No dashes as bullets.

**Rollback:** delete branch `checkpoint/BL-722`. It contains one document and touches nothing.
