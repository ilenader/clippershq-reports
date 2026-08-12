# BL-787 — the Instagram equivalent of bundle.social, named and ended

**2026-08-12 · DB `now()` = `2026-08-12 12:14:12.990637+00` · AUDIT ONLY, READ ONLY.**
No code, config, schema or data change. **No account connected, no payment details entered, no paid plan started, no free tier signed up for, nothing authorised, no credential stored.** Base `origin/main` @ `72f05cec`, branch `checkpoint/BL-787`, isolated worktree `C:/bl787`, `node_modules` never junctioned, removed at the end. Every database read through `scripts/run-select.js`, every timestamp cast `::text` against DB `now()`. Four subagents ran in parallel, all read-only; **every load-bearing claim was re-fetched and verified by me at Meta's or the vendor's own URL**, and contradictions are reported rather than averaged. A markdown-only diff cannot change tsc or build, **so no build was run and none is claimed.** The decision to build is the owner's and is not revisited.

## THE FIRST LINE, BECAUSE PART 0 CHANGES WHAT CAN BE ASKED FOR

> **The retention graph a creator sees in the Instagram app does NOT exist in any Meta API. No vendor can sell it, at any price, because Meta does not expose it for Instagram. What IS obtainable, and is confirmed returning real numbers, is three scalars per reel: `ig_reels_avg_watch_time`, `ig_reels_video_view_total_time`, and `reels_skip_rate`, the share of viewers who skipped in the first three seconds. Plus reach, views, likes, comments, saves, shares and reposts, and account-level audience country, city, age and gender.**
>
> **THE TOOL: Composio (https://composio.dev), at $0 a month at this platform's real Instagram volume.** Its `INSTAGRAM_GET_IG_MEDIA_INSIGHTS` passes Meta's own metric names straight through, its `INSTAGRAM_GET_IG_USER_MEDIA` lists a creator's natively-posted reels with their `permalink` so a clip URL can be matched to a media id, its managed Meta app requests `instagram_business_manage_insights` by default, connected accounts are unlimited and the free tier is 20,000 tool calls a month against the roughly 4,300 this platform would need.
>
> **RUNNER-UP: Zernio at $120 a month for 34 accounts.** It loses on cost and on unit, not on honesty: it is the best-documented vendor examined, publishes real rate limits and retention, charges nothing to refetch, and uniquely returns `videoDurationSeconds` so a retention ratio can be estimated.

## PART 0 — THE CEILING: WHAT META ACTUALLY EXPOSES

Every vendor resells this. A marketing page promising more than this table is wrong. Fetched by me today from https://developers.facebook.com/docs/instagram-platform/reference/instagram-media/insights (HTTP 200, Graph API v25.0).

**The complete REELS metric list, with Meta's own wording and caveats:**

| metric | Meta's description | caveat |
|---|---|---|
| **`ig_reels_avg_watch_time`** | "The average amount of time spent playing the reel." | **none** |
| **`ig_reels_video_view_total_time`** | "The total amount of time the reel was played, including any time spent replaying the reel." | "Metric in development." |
| **`reels_skip_rate`** | "The percentage of views from people who skipped during the first 3 seconds of the reel. This is calculcated as the number of views that skipped the reel during the first 3 seconds divided by the number of intial views." (Meta's typos) | "Metric is estimated and in development." |
| `views` | "Total number of times IG Media has been played on Instagram." | "Metric in development." |
| `reach` | "Number of unique Instagram users that have seen the reel at least once." | "Metric is estimated." |
| `likes`, `comments`, `saved`, `shares`, `reposts` | the ordinary counts | none |
| `total_interactions` | likes + saves + comments + shares, minus removals | "Metric in development." |
| `crossposted_views`, `facebook_views` | Facebook-side plays; "Throws if the media is not shared to Facebook" | none |
| `total_views`, `total_likes`, `total_comments` | across all surfaces including ads | **"Available for Instagram API with Facebook Login only."** |

**NOT available for REELS, though vendors list them:** `follows`, `profile_visits`, `profile_activity`, `link_clicks`, `navigation`, `replies` are FEED or STORY only, and `impressions` is deprecated. **So "follows from post" and "profile visits" cannot be had for a reel from anybody.** Zernio says so itself: its `follows` field is documented as "0 for reels".

**THE RETENTION CURVE: IT DOES NOT EXIST FOR INSTAGRAM.** A scan of the media-insights reference for retention, curve, drop-off or per-second breakdown returns nothing, and the only `breakdown` values Meta offers are `action_type` and `story_navigation_action_type`, neither time-based. **Meta does ship a retention graph — for Facebook Pages.** I fetched https://developers.facebook.com/docs/graph-api/reference/video/video_insights/ myself: `post_video_retention_graph`, "The percentage of times your reel was played at various timestamp segments out of the total number of plays. Most reels will start out at 100% retention and curve downward", sits on an endpoint whose scope sentence is **"Get aggregated insight metrics for videos on a Page"**, requiring `pages_manage_engagement`, `read_insights` and a Page access token. The only four occurrences of "instagram" on that page are telemetry JSON, not documentation. **Any vendor claiming Instagram retention curves is conflating this Facebook endpoint or scraping the app.**

**`reels_skip_rate` is new and real.** Meta's Instagram Platform changelog, verified by me: "**Introducing the following metrics fields for media insights: `reels_skip_rate`, `reposts`**", under the entry dated **2025-12-03**, "Applies to all versions". It needs no extra access tier beyond the ordinary insights permission.

**What "in development" means**, from Meta's own metrics-labeling definition: "Still being tested and may change as we improve our methodologies. We encourage you to use it for directional guidance, but use caution when using it for historical comparisons or strategic planning." **Meta nowhere states whether such a field returns data, null or an error** — which is why PART 0.5 exists.

**Permissions, and the third-party question settled.** The endpoint needs `instagram_business_basic` + `instagram_business_manage_insights` (Instagram Login) or `instagram_basic` + `instagram_manage_insights` + `pages_read_engagement` (Facebook Login). Meta: "**Advanced Access is the access level required if your app serves Instagram professional accounts that you don't own or manage**", and "Business Verification is required to get Advanced Access." **That is exactly why an individual goes through a vendor: the App Review and the Business Verification land on the vendor, not on the owner.**

**Account-level audience data**, from https://developers.facebook.com/docs/instagram-platform/api-reference/instagram-user/insights (fetched by me): `follower_demographics` and `engaged_audience_demographics`, each breaking down by `age`, `city`, `country`, `gender`. Both are gated: "**Not returned if the IG User has less than 100 followers**", and the engaged variant needs 100 engagements in the window. **There is no per-post audience breakdown at any price.**

**Deprecated, so a vendor still listing these has a stale field list:** `impressions`, `plays`, `clips_replays_count`, `ig_reels_aggregated_all_plays_count` (v22.0, effective 2025-04-21) and `video_views` (v21.0, effective 2025-01-08).

## PART 0.5 — PROOF THE THREE FIELDS ACTUALLY RETURN NUMBERS

Documented is not the same as populated, and this line of rounds has been burned by exactly that. **A public repository commits real Graph API output containing all three fields.** I fetched the raw file myself: https://raw.githubusercontent.com/whistlegraph/aesthetic-computer/main/xbox/live/marketing/ledger.json

| views | reach | `ig_reels_avg_watch_time` | `ig_reels_video_view_total_time` | `reels_skip_rate` |
|---|---|---|---|---|
| 1,361 | 1,073 | **7,102** | **7,550,436** | **48.1** |
| 151 | 128 | **2,618** | **335,143** | **74.8** |
| 16 | 0 | 0 | 0 | 0 |
| 0 | 0 | 0 | 0 | 0 |

**Three things make this convincing.** The fetch code in the same repository parses `row.values?.[0]?.value ?? row.total_value?.value ?? null`, so a null from Meta would have been preserved as null; it got numbers. **The arithmetic is internally consistent**: on the second row `335,143 / 128 = 2,618.3`, exactly the reported average watch time, and on the first `7,550,436 / 1,073 = 7,037.7` against a reported 7,102, within 1%. And the units settle a question every vendor answers differently: **7,102 ms is 7.1 seconds, which is a plausible reel; 7,102 seconds is not. Meta returns milliseconds.** The two zero rows were fetched about six minutes after publishing with `reach` also zero, which is Meta's documented ingestion lag rather than field unavailability.

**Still unproven, and stated plainly: nobody has shown these fields populating under ADVANCED ACCESS for an account the app does not own.** That is the standard permission-review risk, not a field-existence risk, and it is what the free test in PART 6 settles.

## PART 1 — WHAT EACH CANDIDATE RETURNS, AGAINST THAT CEILING

| field | **META ceiling** | **Composio** | **Zernio** | **PostPeer** |
|---|---|---|---|---|
| average watch time | `ig_reels_avg_watch_time` | **AVAILABLE**, Meta's own name, in the metric enum | **AVAILABLE** `igReelsAvgWatchTime` (ms) | **AVAILABLE** `avgWatchTime` (seconds) |
| total watch time | `ig_reels_video_view_total_time` | **AVAILABLE**, same name | **AVAILABLE** `igReelsVideoViewTotalTime` (ms) | **AVAILABLE** `totalWatchTime` |
| **skip rate** | `reels_skip_rate` | **AVAILABLE, the only vendor that has it** | **ABSENT** | **ABSENT** |
| retention curve | **DOES NOT EXIST** | ABSENT | ABSENT, and Zernio ships a real one for YouTube only | ABSENT |
| video duration, for a ratio | not an insights metric | UNVERIFIED | **AVAILABLE `videoDurationSeconds`**, "combine with igReelsAvgWatchTime (ms) to estimate retention" | ABSENT |
| reach, views, likes, comments, saves, shares | all present | AVAILABLE | AVAILABLE | AVAILABLE |
| profile visits (per reel) | **NOT AVAILABLE FOR REELS** | n/a | account level only | account level only (`profile_links_taps`) |
| follows from post (per reel) | **NOT AVAILABLE FOR REELS** | n/a | **`follows` documented "0 for reels"** | ABSENT per post |
| audience country / gender / age | account level, 100-follower floor | **AVAILABLE** `INSTAGRAM_GET_IG_USER_INSIGHTS` | **AVAILABLE** `/v1/analytics/instagram/demographics` | **AVAILABLE** `getInstagramDemographics` |
| follower count | `follower_count`, 100-follower floor | AVAILABLE | AVAILABLE `followersCount` | AVAILABLE `currentFollowers` |
| list a creator's NATIVE posts | n/a | **YES** `INSTAGRAM_GET_IG_USER_MEDIA`, returns `permalink` | **YES** `source=external` | **YES** `source=platform` |

Sources: https://docs.composio.dev/toolkits/instagram · https://docs.zernio.com/analytics/get-analytics · https://www.postpeer.dev/docs/analytics/get-analytics and /docs/api/analytics/*

**Contradictions against Meta's ceiling, flagged rather than repeated:** any vendor offering **per-reel profile visits or follows-from-post** is contradicting Meta's media-type column, and Zernio is the one that says so honestly. **PostPeer's marketing lists `impressions` while its own FAQ says impressions "come back as null"** — Meta deprecated the field, so the FAQ is right and the marketing page is stale. **BL-786 recorded PostPeer as having no demographics and no follower count; that was wrong and is corrected here**: both exist, on separate endpoints.

**The correction that matters most to the winner.** Composio is not an analytics vendor, it is an agent-tooling platform providing managed authentication, and **that is precisely why it has the fullest field list: it does not normalise Meta's schema into a cross-platform one, it passes Meta's metric names through.** Its metric enum, verbatim: "REELS-SPECIFIC METRICS: `ig_reels_video_view_total_time`, `ig_reels_avg_watch_time`, `reels_skip_rate`, `facebook_views`, `crossposted_views`." **Every field it offers therefore exists at Meta by construction, and it can never offer less than Meta or promise more.**

## PART 2 — WHAT THE CLIPPER DOES, AND WHETHER "TAP YES ONCE" IS TRUE

**Settled from Meta's current documentation, quoted:**

> "your app users must have an **Instagram professional account**" (business or creator) — https://developers.facebook.com/docs/instagram-platform/overview/
> "The Instagram API with Facebook Login **cannot access Instagram consumer accounts**." — .../instagram-api-with-facebook-login
> "This API setup **does not require a Facebook Page** to be linked to the Instagram professional account." — .../instagram-api-with-instagram-login

**DEFINITIVE: a Business or Creator account is required, a personal account cannot authorise at all, and a linked Facebook Page is required ONLY on the Facebook Login path.** Both top candidates use Instagram Login: Composio's own parameter documentation says "On **Instagram Login** the host follows the token (`graph.instagram.com`) and Facebook Page IDs are not resolved"; Zernio offers both and defaults to `instagram_login`, "no Facebook Page required". **So no clipper has to create a Facebook Page.** That question is closed.

**What the clipper actually does: six taps to convert, then one authorisation.** Meta's own help page (https://www.facebook.com/help/instagram/502981923235522): Profile, menu, Settings, "Switch to professional account", pick a category, Done. Then the consent screen on Meta's own domain, listing the scopes the app requests. **The unsoftened cost: "Professional accounts cannot be set to private"** (https://www.facebook.com/help/instagram/138925576505882). A private clipper must become public.

**"TAP YES ONCE" IS ONLY TRUE IF THE VENDOR REFRESHES THE TOKEN, AND THIS IS THE MOST DECISION-RELEVANT FACT IN THE ROUND.** Meta, verified by me at https://developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login/business-login: a long-lived Instagram token "is valid for **60 days**", is refreshable "for another 60 days" once it is at least 24 hours old, and — verbatim — "**Tokens that have not been refreshed in 60 days will expire and can no longer be refreshed.**"

| vendor | what it says about refresh |
|---|---|
| **Composio** | "**Built-in OAuth handling with automatic token refresh and rotation**" and "Managed authentication and token refresh" on its Instagram toolkit page. Its auth docs also define an `EXPIRED` state where "Composio cannot refresh them automatically... re-authenticate the user", with an expiry event to subscribe to. **So refresh is claimed, with an honest failure state.** |
| **Zernio** | Documents the opposite outcome explicitly: "Instagram access token expired." → "Reconnect the account. Subscribe to the `account.disconnected` webhook", and exposes `tokenStatus.expiresAt` / `needsRefresh`. **Re-authorisation is expected.** |
| **PostPeer** | Says only that it handles "token storage, refresh". No lifetime, no cadence. **UNVERIFIED.** |

**Nobody can promise "once, forever", because Meta does not allow it. What a good vendor promises is that the clipper is never asked again while they keep posting.** Composio makes that claim in writing; Zernio tells you plainly that reconnection happens; PostPeer says the least. **One caveat on Composio's claim, stated because it is not small: Meta's Instagram Login does not use the standard OAuth2 refresh grant, it uses a bespoke `grant_type=ig_refresh_token` call, and Composio's refresh statements are generic and toolkit-agnostic. No Composio page says Instagram-specific refresh is implemented.** If it is not, every clipper re-authorises every 60 days.

**WHOSE NAME THE CLIPPER SEES, which the owner should know before he asks anyone.** On Composio's managed app the consent screen reads **"Composio wants to access your account"**, not Clippers HQ. Composio's own white-labeling doc is explicit that branding the Connect Link does not change this, because "the consent screen originates from the OAuth provider, not Composio's infrastructure", and that showing your own name requires registering your own OAuth app. **A clipper is therefore asked to trust a name he has never heard of, on a screen Clippers HQ sent him to.** That is a real adoption cost and it is not fixable on the managed path.

**The real population, measured live today:**

| measure | value |
|---|---|
| Instagram clips, last 30 days | **1,269** (98.7% are `/reel/` URLs, so 1,253 carry watch time) |
| distinct Instagram clippers, last 30 days | **69** |
| distinct posting ACCOUNTS, last 30 days | **99** |
| approved Instagram accounts on the platform | **363**, held by 259 users |
| Instagram approved earnings, all time | **$3,561.69** across 61 earning clippers |

| share held by | top 5 | top 10 | top 25 |
|---|---|---|---|
| **Instagram EARNINGS** | **50.1%** | **69.2%** | **93.9%** |
| **30-day CLIP VOLUME**, by account | 41.5% | 58.6% | **78.8%** |

**So the ask is about twenty-five people, not fifty and not three hundred.** The top 25 earning clippers hold **34 posting accounts** carrying **78.8%** of Instagram clip volume.

## PART 3 — THE PRICE AT HIS VOLUME

| vendor | unit, verbatim | refetch costs again? | cap |
|---|---|---|---|
| **Composio** | **per tool call.** "Pricing is based on ... executions and resource use — **not accounts. There is no limit on the number of connected accounts you can have.**" Failed calls are not billed. Free **20,000 calls/month** on both cards. **Paid entry TODAY: $29 for 200,000 calls, overage $0.299 per 1,000. From 2026-08-15: $29 for 50,000, overage $4 per 1,000** | yes, per call | none on accounts |
| **Zernio** | **per connected account per month**, graduated: first 2 free, 3 to 10 at **$6**, 11 to 100 at **$3**, 101+ at **$1**, metered by account-days | **no, refetching is free** | none |
| **PostPeer** | **per API call**, up to 100 posts per call; Free 20 credits, Starter **$25**/2,000, Standard $43/6,000, Pro $120/20,000; unlimited accounts; monthly credits do not roll over | yes, per call | none on accounts |

**The owner's actual call volume, computed from live data.** Composio needs one media-list call per account per pass plus one insights call per clip captured. At 99 accounts and 1,269 clips a month:

| strategy | Composio calls/month | **Composio cost** | Zernio | PostPeer |
|---|---|---|---|---|
| list daily + capture each clip once at 48h | 2,970 + 1,269 = **4,239** | **$0** | $315 (99 accts) | $25 |
| list daily + capture each clip 3 times | 2,970 + 3,807 = **6,777** | **$0** | $315 | $25 to $43 |
| top 34 accounts only, list daily + 3 captures | ~1,020 + 3,000 = **4,020** | **$0** | **$120** | **$25** |
| every clip refreshed daily for 7 days | 2,970 + 8,883 = **11,853** | **$0**, still inside the free tier | $315 | $43 |

**A PRICING CORRECTION TO MY OWN FIRST PUBLICATION OF THIS REPORT, AND A DATE THAT MATTERS.** Composio runs two live pricing pages. The current card at https://composio.dev/pricing gives **$29 for 200,000 calls with $0.299 per 1,000 overage**; the card at https://composio.dev/updated-pricing, effective **2026-08-15, three days from now**, gives **$29 for 50,000 with $4 per 1,000 overage**, a **13-fold rise in marginal cost**. Composio states that "existing customers retain current plans through December 31, 2026". **None of this changes the answer, because the owner's volume sits inside the free tier on both cards.** It is recorded because a paid tier bought before the 15th is a different product from one bought after it, and because this report's first publication quoted only the future card.

**RANKED BY TOTAL COST: Composio $0, PostPeer $25, Zernio $120 at 34 accounts or $315 at all 99.** The free tier is not a teaser here; at this platform's volume it is roughly a fifth of the allowance, with headroom for a threefold increase in Instagram volume before a dollar is due. **Against $2,290 of monthly Instagram payouts, the winner costs nothing and the runner-up costs 5%.**

**What nobody discloses before payment:** Composio publishes no per-plan rate-limit numbers; PostPeer publishes no rate limits and **no data-retention policy at all**; Zernio publishes both, fully, and is the only one that does. **Zernio's own rate limits, as an example of what good disclosure looks like:** 60 requests a minute at 1 to 2 accounts, 600 at 3 to 2,000, with analytics endpoints on a one-second window and documented `Retry-After` behaviour.

## PART 4 — DOES THE DATA EXPIRE

**No. Instagram has no equivalent of TikTok's seven-day vanishing act, and this is the one place Instagram is strictly better.** Meta, on the media insights page: "Data used to calculate metrics can be **delayed up to 48 hours**" and "**Metrics data is stored for up to 2 years**." **So the capture-early-and-store design built for TikTok carries over unchanged and is still correct**, for a different reason: the vendors expire their own copies (Zernio keeps roughly 12 months of external posts, PostPeer publishes no retention policy), so the platform's own store must remain the durable copy.

**Reported, not averaged:** Meta's insights overview page says "**User Metrics data is stored for up to 90 days**" while the media insights page says two years. They plausibly scope to different objects, media versus user, but Meta reconciles them nowhere.

**The 48-hour delay is the operational constraint that shapes the build, and it is measured:** of 1,237 Instagram clips reviewed in the last 30 days, the median was reviewed **2.9 hours** after submission and **1,128 of them, 91%, within 48 hours**. **For nine clips in ten the review decision is already made before Meta's watch-time number has settled.** Watch time therefore belongs on the clipper's record and on a post-hoc pass, not in the live review queue.

## PART 5 — HOW MUCH IS ALREADY BUILT

| component | rating | evidence |
|---|---|---|
| the store `ClipAnalyticsSnapshot` | **schema VENDOR-AGNOSTIC**, column names TikTok-shaped | `prisma/schema.prisma:3098-3152`, already carries `provider` and `platform`, so no schema change is needed; but `fullVideoWatchedRate` has no Instagram equivalent and `reels_skip_rate` has no column |
| the free arrival curve | **FULLY AGNOSTIC, 0 edits** | `src/lib/review-evidence.ts:168-236`, no platform predicate |
| the evidence panel | **multi-platform except ONE line** | `src/components/admin/ReviewEvidencePanel.tsx:301` short-circuits every non-TikTok platform |
| the capture | **bundle.social-SPECIFIC** | `src/lib/clip-analytics-capture.ts:348` returns `not_tiktok`; `:381` sets `platformType=TIKTOK`; `ANALYTICS_FIELDS` at `:91-102` is ten TikTok metric names matched by exact key; `MONTHLY_CAPTURE_BUDGET` at `:261` is one global counter |
| the vendor client | **bundle.social-SPECIFIC, whole file** | `src/lib/social-connect/bundle-social.ts` |
| the link store | agnostic table, hardcoded constant | `src/lib/social-connect/links.ts`, 4 references to `BUNDLE_PROVIDER` |
| the connect routes | TikTok-specific paths | `src/app/api/accounts/[id]/tiktok-link/*`, `src/app/api/tiktok-link/return/[linkId]` |

**Nine non-generated files reference the vendor, of which five are real source files.** The honest verdict: **the table and the `provider` column were built for exactly this and hold up; the code around them is a second integration**, not an extension. The free curve needs one line.

**And the estimate inherits an unproven chain: the TikTok pipeline has still never returned a single analytics field, because no clipper has ever connected.** Nothing in this architecture is proven end to end on any platform.

## PART 6 — THE ANSWER

> **THE TOOL: Composio. $0 a month at 1,269 clips and 99 accounts, against a 20,000-call free tier it uses about a fifth of. It returns average watch time, total watch time, skip rate, reach, views, likes, comments, saves, shares and reposts per reel, plus account-level audience country, city, age and gender above 100 followers. It does NOT return a retention curve, because Meta has none for Instagram, and it cannot return per-reel profile visits or follows, because Meta does not expose those for reels either.**

**RUNNER-UP: Zernio, $120 a month for the 34 accounts that carry 78.8% of clip volume.** It lost on cost and on unit: it bills per connected account where Composio bills per call, so it charges for a clipper who posts nothing. **It wins on honesty and would be the right choice if Composio's managed app turns out not to hold the insights grant:** it publishes real rate limits and retention, refetching is free, its consent flow is fully specified with a `loginMethod` switch, and it is the only vendor with `videoDurationSeconds`, the denominator that turns watch time into an estimated retention ratio. **Its own caveat, quoted, is the reason to test it on real clips: that field is "Null when unknown ... e.g. reels with copyrighted audio", which is exactly what clipper content is.**

**PostPeer is third and should not be chosen.** Its watch-time capability rests on a permission claim its own site contradicts three ways on one page, and its analytics endpoints are still absent from its own published OpenAPI spec.

### The ordered steps, and the test comes FIRST

**Step 1, $0, and it settles the only real unknown.** Create a free Composio account, connect **one Instagram professional account the OWNER controls**, and call `INSTAGRAM_GET_IG_MEDIA_INSIGHTS` with `metric=["ig_reels_avg_watch_time","ig_reels_video_view_total_time","reels_skip_rate"]` on one real reel **at least 48 hours old**. **The question is not whether the fields exist; PART 0.5 already shows real values. The question is whether Composio's managed Meta app carries the `instagram_business_manage_insights` grant for an account it does not own.** A permission error answers it in one call.

**AND THE REASON THAT QUESTION IS SHARPER THAN IT LOOKS, in Composio's own words.** Its managed-versus-custom page frames managed auth as development-grade — "You're building and iterating" and "acceptable for internal tools and prototypes" — and its Instagram marketing page says outright: "**For production, we recommend configuring your own OAuth credentials.**" Its toolkit FAQ then documents that this exact failure has already happened on this exact toolkit for a different scope: "If a reply-to-comment flow fails because the managed OAuth app does not currently have the required comment permission, use your own Meta OAuth app with that permission configured and approved. **Composio is working on managed-app approval for the missing permission.**" There is **no equivalent statement for insights, in either direction**. Two further consequences follow: the managed app's Meta quota is **shared across every Composio customer**, with no number published; and Meta's own announcement of insights on Instagram Login states that "**Advanced access is required to request permission from any app user**", which means App Review and Business Verification — **so the documented fallback of bringing your own Meta app is the one path an individual with no registered company cannot take.** On the managed path this is a convenience; here it is the only door, and its lock is undocumented.

**Step 2, still $0.** Call `INSTAGRAM_GET_IG_USER_MEDIA` and confirm the `permalink` of a known clip matches the platform's stored `clipUrl`. **That is the whole join between this platform's data and Meta's, and if it does not match cleanly nothing else works.**

**Step 3, still $0, and it is the question worth more than the vendor choice.** Run step 1 against one clip the owner believes was bought and one he believes was genuine. **Does watch time separate them?** Five rounds have reasoned about this from documentation; two calls answer it.

**Step 4, the fallback, also $0.** If Composio's grant is missing, repeat steps 1 to 3 on **Zernio's free tier** (first two accounts free forever, no card), while confirming its one open question: whether analytics is enabled on the free band at all, since its docs bundle analytics with paid accounts.

**Step 5, the owner's own actions.** Convert one account he controls to a professional Creator account (six taps), and decide which of the top 25 clippers he asks first. **Then run the $0.31 HikerAPI census** over the 363 approved Instagram accounts to learn how many are already professional; it has been specified for four rounds and never run, and it is the number that decides whether the ask is easy or hopeless.

**Step 6, only then, write code**, with the 48-hour delay designed in from the first line.

## CONTRADICTIONS, RESOLVED RATHER THAN AVERAGED

1. **Instagram's in-app retention graph versus the API.** The app feature is real; **the API field does not exist for Instagram.** The retention graph fields live on Facebook's Page video endpoint. Anyone who told the owner otherwise was reading a Facebook page.
2. **BL-786 said PostPeer has no demographics and no follower count.** Wrong, corrected: both exist, on `/docs/api/analytics/getInstagramDemographics` and `getInstagramFollowerStats`.
3. **Zernio's duration field name.** BL-786 called it `videoLength`; it is **`videoDurationSeconds`**, and it is nullable exactly where clipper content lives, on reels with copyrighted audio.
4. **PostPeer's scope claim contradicts itself three ways on one page**: two places enumerate approval for `instagram_business_basic` (and `instagram_business_content_publish`), while a collapsed FAQ answer claims the metrics are "powered by the `instagram_business_manage_insights` scope that PostPeer is approved for". **Unresolved, and not resolved in PostPeer's favour.**
5. **PostPeer's impressions.** Marketing lists it; its own FAQ says it returns null. Meta deprecated it. The FAQ is right.
6. **"In development" as a blocker.** The label sounds fatal and empirically is not: `reels_skip_rate` returned 48.1 and 74.8 in committed output. **`ig_reels_avg_watch_time` carries no caveat at all**, which corrects the framing carried into this round.
7. **Meta's own retention conflict**, 2 years on the media insights page against 90 days on the insights overview. Different scopes, never reconciled by Meta.
8. **Watch-time units.** Meta states none; the observed values are milliseconds; Zernio and Meta agree on ms, PostPeer documents seconds and says it converts.

## WHAT COULD NOT BE ESTABLISHED

**No live API call was made and nothing was signed up for, so every vendor capability claim remains documentation plus one third party's committed output.** Specifically: whether **Composio's managed Meta app holds `instagram_business_manage_insights` at Advanced Access for accounts it does not own** — the one item that decides the winner, and free to settle; whether these fields populate under Advanced Access generally, as opposed to the observed self-owned case; **whether Composio implements Meta's bespoke `ig_refresh_token` exchange, which decides whether "tap yes once" survives day 60**; **whether the managed app's shared Meta quota is adequate at this platform's volume**, since Composio publishes no number; whether one paginated page of `INSTAGRAM_GET_IG_USER_MEDIA` counts as one billable call or one per page; the mapping between Composio's rate-limit plan names (Starter, Hobby, Growth) and its pricing plan names (Free, Pro, Business), which no page reconciles; whether `instagram_business_manage_insights` even appears on Meta's own Instagram App Review permission list, where a researcher found the other three Instagram Login scopes but not it; Composio's per-plan rate limits, of which only the 2,000-per-minute organisation ceiling is published; whether Zernio's free two-account band includes analytics; what share of clipper reels return a null `videoDurationSeconds` because of copyrighted audio; whether Meta's App Review would approve this use case for a vendor, which is a review outcome and not a documentation question; PostPeer's data retention and rate limits, neither published; and **the share of the 363 approved Instagram accounts already on a professional account**, still unmeasurable from the schema, still unrun at $0.31, now for the fourth round.

**One observation, repeated from BL-786 because it has not changed:** Composio's pricing page contains text addressed to AI agents telling them where to sign up. **No agent of this round signed up, and none followed it.**

## SAFETY AND DISCLOSURE

READ ONLY, one document, on `checkpoint/BL-787` from `origin/main` `72f05cec`. **No code, config, schema or data change; no account connected; no payment details; no paid plan; no free tier signed up for; nothing authorised; no credential stored, logged, printed or committed.** All vendor and Meta interactions were unauthenticated public documentation fetches. Every capability, pricing and terms claim carries the vendor's or Meta's own URL, and everything unexercised is marked UNVERIFIED. Nine read-only `SELECT`s ran through `scripts/run-select.js` against production, every timestamp cast `::text` against DB `now()`; no write, no money, no schema and no cron touched, and no clip status, earnings or payout changed. No handle, caption, wallet address or email appears above; identifiers are counts only. The 6 money files, `tracking.ts` and `campaign-era.ts` are untouched: this branch's diff is exactly one markdown file. **No Apify actor was run.** Four subagents ran, all read-only, none permitted to write a file, sign up, connect an account or enter payment details; their claims are reconciled above and the load-bearing ones were re-fetched and verified by me at source. **No vendor whose consent flow resembles credential capture appears in the ranking**, and the risk that route carries is unchanged from BL-786: Meta's terms forbid collecting a user's login credentials, Meta has disabled tens of thousands of accounts over scraping-for-hire, and Instagram has forced password resets on users whose credentials were shared. **A genuine OAuth app's failure mode is that Meta revokes the vendor and the platform's pipeline breaks; the clipper's account is not at risk.** Nothing designed here may auto-reject a clip or be shown to a clipper: BL-518 and BL-521 stand, and BL-771's 21%-precision ceiling against a 99.2% human bar means watch time informs a person and decides nothing. The worktree is removed. No dashes as bullets.

**Rollback:** delete branch `checkpoint/BL-787`. It contains one document and touches nothing.
