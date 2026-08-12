# BL-789 — the Instagram route, settled: two of the four wants exist, two do not, and no vendor can change that

**2026-08-12 · DB `now()` = `2026-08-12 13:01:15.268081+00` (first read) to `13:05:41.358478+00` (last) · AUDIT ONLY, READ ONLY.**
No code, config, schema or data change. **No account connected, no payment details entered, no paid plan started, nothing signed up for, no credential stored.** Base `origin/main` @ `72f05cec`, branch `checkpoint/BL-789`, isolated worktree `C:/bl789`, `node_modules` never junctioned, removed at the end. The main tree had zero dirty tracked files and no live round held a worktree at start. Every database read through `scripts/run-select.js`, which refuses a write keyword before connecting; every timestamp cast `::text` against DB `now()`. A markdown-only diff cannot change tsc or build, **so no build was run and none is claimed.** Five subagents ran, one per search surface rather than one per vendor, all read-only, claims reconciled against primary evidence rather than averaged.

## THE FIRST LINE, AS THE BRIEF REQUIRES

> **TWO of the owner's four wants are NOT obtainable per clip, from any vendor, at any price: audience demographics and traffic or discovery source. ONE is fully obtainable and proven in production code: watch time, `ig_reels_avg_watch_time` and `ig_reels_video_view_total_time`, in MILLISECONDS. ONE is documented by Meta and shipped in Meta's own SDKs but has NEVER been publicly observed returning a value by anyone: the skip rate, `reels_skip_rate`.**

**So the honest count is one certain, one probable, two unobtainable.** Audience demographics exist only at whole account level, never attributable to a clip, and only above 100 followers. **A retention curve does not exist for Instagram at all: Meta builds one and publishes it for Facebook video, and withholds it for Instagram.**

**Stop chasing per clip demographics and the retention curve.** Any page claiming either for Instagram is wrong, and PART 0 proves it from Meta's own reference and Meta's own SDK enums. **One long shot survives on traffic source and costs a single call to test: Meta's media breakdown enum contains a `surface_type` value that its documentation denies and that no public code has ever exercised. See PART 1's GitHub surface.**

## PART 0 — THE CEILING, SETTLED ONCE AND FOR ALL

Every vendor reads the same Meta API, so this bounds all of them.

### The complete per media metric list for REELS

From https://developers.facebook.com/docs/instagram-platform/reference/instagram-media/insights , each requiring `instagram_business_manage_insights` (Instagram Login) **or** `instagram_manage_insights` (Facebook Login):

| metric | Meta's own description | note |
|---|---|---|
| **`ig_reels_avg_watch_time`** | "The average amount of time spent playing the reel." | **no caveat** |
| **`ig_reels_video_view_total_time`** | "The total amount of time the reel was played, including any time spent replaying the reel." | in development |
| **`reels_skip_rate`** | "The percentage of views from people who skipped during the first 3 seconds of the reel." | **estimated and in development** |
| `views` | "Total number of times IG Media has been played on Instagram." | in development |
| `reach` | "Number of unique Instagram users that have seen the reel at least once." | estimated |
| `likes`, `comments`, `saved`, `shares`, `reposts` | counts | |
| `total_interactions` | likes + saves + comments + shares minus removals | in development |
| `crossposted_views`, `facebook_views` | plays aggregated across, or on, Facebook | errors if not shared to FB |
| `total_likes`, `total_comments`, `total_views` | include promoted/boosted/ad engagement | **Facebook Login path ONLY** |

**DEPRECATED and gone**, v22.0, effective **21 April 2025** across all versions (https://developers.facebook.com/docs/graph-api/changelog/version22.0/): `impressions`, `plays`, `clips_replays_count`, `ig_reels_aggregated_all_plays_count`. `video_views` went in v21.0. **`views` is the single canonical replacement.** Any vendor still documenting `plays` or `impressions` for Instagram is serving stale documentation.

**Not available on REELS at all**, though they exist on FEED posts and STORIES: `profile_visits`, `follows`, `profile_activity`, `navigation`, `replies`. **So there is no per reel profile visit count and no per reel follow conversion.**

### THE DECISIVE FINDING: media insights support almost NO breakdowns

Quoted from the same reference: "You can also include the `breakdown` parameter for specific metrics to divide data into smaller sets based on the specified breakdown value." **Exactly two metrics accept one, and both are effectively Story surfaces:** `profile_activity` with `action_type`, and `navigation` with `story_navigation_action_type`.

**"No breakdowns exist for follow_type, age, gender, city, country, or source."**

That single sentence kills two of the four wants. There is no per post demographic split and no per post view source, because Meta provides no mechanism to ask for one.

### Where demographics DO live, and their limits

Account level only, https://developers.facebook.com/docs/instagram-platform/api-reference/instagram-user/insights :

• **`follower_demographics`** — "The demographic characteristics of followers, including countries, cities and gender distribution." **"Not returned if the IG User has less than 100 followers."**
• **`engaged_audience_demographics`** — **"Not returned if the IG User has less than 100 engagements during the timeframe."**
• **`reached_audience_demographics`** — same family.
• **"Demographic metrics only return the top 45 performers."**
• Account level breakdowns that DO exist: `age`, `city`, `country`, `gender`, `follow_type` (FOLLOWER, NON_FOLLOWER, UNKNOWN), `media_product_type` (AD, STORY, REEL, CAROUSEL_CONTAINER, POST, FEED), `contact_button_type`.

**The nearest thing to a traffic source anywhere in Instagram's API is the ACCOUNT level `views` metric broken down by `follow_type`**, which tells you what share of the whole account's views over a period came from non followers. **It cannot be attributed to a clip.** For a platform paying per clip, that is not a usable signal.

### THE RETENTION GRAPH QUESTION, SETTLED

BL-787 flagged that Instagram's app shows a Retention graph and a Skip Rate that might be app only. **Both halves now settled, and they land differently.**

**Skip Rate is REAL and IS in the API.** `reels_skip_rate` is listed on Meta's Instagram media insights reference under the ordinary insights permission. It is not Marketing API only and it is not app only. Meta's own caveat stands: estimated, and in development.

**The retention curve is NOT in Instagram's API, and it is not merely an omission — Meta publishes it for FACEBOOK and withholds it for Instagram.** The Facebook video insights endpoint `/{video-id}/video_insights` (https://developers.facebook.com/docs/graph-api/reference/video/video_insights/) carries all of this, and **none of it has an Instagram counterpart**:

• `total_video_retention_graph` — "The number of times your videos played at each interval as a percentage of all views. **Videos are divided into 40 equal intervals.**"
• `post_video_retention_graph` — "The percentage of times your reel was played at various timestamp segments out of the total number of plays."
• `total_video_complete_views` — a true completion count.
• `total_video_view_time_by_age_bucket_and_gender`, `total_video_views_by_age_bucket_and_gender`, `total_video_views_by_country_id`, `total_video_view_time_by_region_id` — **per video demographics.**
• `total_video_views_by_distribution_type`, `total_video_view_time_by_distribution_type` — **per video traffic source.**

**So Meta demonstrably HAS the capability, builds it, and documents it, for Facebook video. It exposes none of it for Instagram media.** The gap is Meta's deliberate product boundary, not a vendor failing and not a documentation gap. **No vendor can route around it, because there is no endpoint to call.**

### The owner's four wants, judged against the ceiling

| want | per clip? | what actually exists |
|---|---|---|
| **Watch time** | **YES, PROVEN** | `ig_reels_avg_watch_time` and `ig_reels_video_view_total_time`, per Reel, **in milliseconds**. In Meta's SDKs and in Airbyte's production connector |
| **Skip or completion rate** | **DOCUMENTED, NEVER OBSERVED** | `reels_skip_rate` per Reel, "estimated and in development", added 3 December 2025. In Meta's own SDKs; **no public source shows it returning a value, and Airbyte's production connector does not request it.** A true completion rate and a **retention curve do not exist for Instagram at any price**. A completion estimate can be DERIVED, see Zernio in PART 2 |
| **Audience demographics** | **NO** | Account level only, 100+ followers or 100+ engagements, top 45 only. Confirmed by Meta's own 23 value media enum, which contains no demographic value. **Never attributable to a clip** |
| **Traffic or discovery source** | **NO PROVEN PATH** | Documentation says no source breakdown exists. Meta's SDK media breakdown enum nonetheless contains **`surface_type`**, which **no public code has ever used and whose values are undocumented everywhere.** Account level `views` by `follow_type` is the only working relative, and it is account wide |

### One more ceiling that decides how this can be used

Meta: **"Data used to calculate metrics can be delayed up to 48 hours."** Measured against that, live, over the last 60 days: **1,834 Instagram clips reviewed, median 5.32 hours from submission to review decision, 80.6% reviewed inside 24 hours and 89.9% inside 48 hours.**

**Roughly nine in ten Instagram clips are decided before Meta guarantees the analytics have even arrived.** Connected analytics is therefore a clipper record and post hoc signal, not a review queue signal. That is a fact about what the route can be used for, not an argument about whether to build it.

## PART 4 — WHAT THE CLIPPER MUST HAVE, AND HOW MANY MUST BE PERSUADED

### Settled from Meta's current documentation, ending the disagreement between two prior rounds

> "your app users must have an **Instagram professional account**" (business or creator) — https://developers.facebook.com/docs/instagram-platform/overview/
> "The Instagram API with Facebook Login **cannot access Instagram consumer accounts**." — https://developers.facebook.com/docs/instagram-platform/instagram-api-with-facebook-login
> "This API setup **does not require a Facebook Page** to be linked to the Instagram professional account." — https://developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login
> "your app users' Instagram professional accounts **must be connected to a Facebook Page**" (Facebook Login path) — overview

**DEFINITIVE ON ACCOUNT TYPE: a professional Business or Creator account is REQUIRED on both paths. Personal accounts cannot authorise at all.** That half is settled and both prior rounds now agree.

**THE FACEBOOK PAGE HALF IS NOT SETTLED, AND THIS ROUND FOUND WHY. The documented rule is clear: a Page is required ONLY on the Facebook Login path. The problem is that insights may not actually work on the Instagram Login path.**

Evidence that `instagram_business_manage_insights` may not be grantable at all:
• It is named as required on **three** Meta reference pages (the insights guide, media insights, user insights).
• It is **absent** from the Permissions Reference, which enumerates 19 Instagram permissions and not this one; absent from the Instagram App Review permission list; absent from the Overview scope list; and **absent from the Business Login OAuth scope list, whose worked authorization URL contains no insights scope at all**.
• **`docs/permissions/reference/instagram_business_manage_insights` returns HTTP 404, while `.../instagram_manage_insights` renders fully.**
• A reply on Meta's own developer forum (thread 905237844750433) states verbatim: *"If you are using the Instagram with Facebook Login API, you must require the scopes without the '_business'. You will need `instagram_basic` and `instagram_manage_insights` instead"*, adding that **insights are not yet available via Instagram Login**. **Attribution to Meta staff could NOT be confirmed, because the forum's role badges are stripped in conversion.**
• Countervailing: thread 611040698214419 reports the permission CAN be surfaced through the dashboard at Instagram → API Setup with Instagram Login → Access App Control, and pre-loaded into a submission. A follow up poster who got it granted still hit `"Unsupported get request… cannot be loaded due to missing permissions"`. **Unresolved.**

**RESOLVED IN FAVOUR OF INSTAGRAM LOGIN, BY WORKING CODE. I record the doc evidence that pointed the other way, because I followed it for part of this round and it was wrong.**

**The resolution: `instagram_business_manage_insights` is requested as an INSTAGRAM LOGIN scope by a dozen independent production codebases**, found through GitHub's own code search: **Botpress** (`scope = "instagram_business_basic,instagram_business_manage_messages,instagram_business_content_publish,instagram_business_manage_insights,instagram_business_manage_comments"`), **Postiz**, **Oracle's developer hub** ("connect your Creator account, grant `instagram_business_basic` + `instagram_business_manage_insights`"), **simstudioai/sim**, **metorial**, **Klavis-AI**, **brightbean-studio** (whose file is literally `providers/instagram_login.py`), **diwenne/openreply**, and **restfb**, which carries it as a typed enum under `Category.INSTAGRAM_BUSINESS`. **AiToEarn** goes further and ships a runtime guard that errors with `'Missing instagram_business_manage_insights'`, which nobody writes for a scope that cannot be granted.

**So no clipper needs a Facebook Page.** The Instagram Login path carries insights, and the documentation surfaces below are gaps in Meta's docs, not gaps in Meta's capability.

**The contradicting doc evidence, recorded rather than buried, because it is what a documentation-only round would have concluded:**

**One, the permission reference page 404s, and only that one.** Fetching `https://developers.facebook.com/docs/permissions/reference/<name>` returns:

| permission | HTTP |
|---|---|
| **`instagram_business_manage_insights`** | **404** |
| `instagram_manage_insights` | 301, page renders |
| `instagram_business_basic` | 301, page renders |
| `instagram_basic` | 301, page renders |

**Two, Meta's Business Login page lists exactly four Instagram Login scopes and none of them is insights.** Fetching the page HTML directly (14,446 bytes) and extracting every `instagram_business_*` token yields **only**: `instagram_business_basic`, `instagram_business_content_publish`, `instagram_business_manage_comments`, `instagram_business_manage_messages`.

**How the contradiction resolves, and the lesson in it.** Meta's three insights reference pages say Instagram Login carries insights. Meta's permission reference 404s on the name, Meta's Instagram Login scope list omits it, Meta's App Review list omits it, and a forum reply says use Facebook Login instead. **Four documentation surfaces pointing one way; a dozen production codebases and one runtime guard pointing the other. The code wins, and the brief was right that this is the surface to search.** The Business Login page lists the four common scopes rather than all grantable ones, and the missing reference page is a missing page.

**Net for PART 4: a professional Business or Creator account is required, personal accounts cannot authorise, and NO Facebook Page is needed. Six steps in the Instagram app, then one authorisation.**

**The conversion cost, unsoftened:** "Professional accounts cannot be set to private" (https://www.facebook.com/help/instagram/138925576505882). A private clipper must go public to participate. The switch itself is 6 steps entirely inside the Instagram app (https://www.facebook.com/help/instagram/502981923235522).

**Authorisation is once, but not forever.** Meta's long lived token "is valid for 60 days", refreshable once it is at least 24 hours old, and **"Tokens that have not been refreshed in 60 days will expire and can no longer be refreshed"** (https://developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login/business-login). So "taps yes once" holds only while the platform refreshes on schedule; a clipper who goes quiet past 60 days must re authorise.

### The live population, measured today

| measure | value |
|---|---|
| Instagram clips, last 30 days | **1,273** |
| distinct Instagram clippers, last 30 days | **69** |
| distinct Instagram posting accounts, last 30 days | **99** |
| approved, non deleted Instagram accounts | **364** |
| clippers who have EVER earned on Instagram | **61** |
| Instagram approved earnings, all time | **$3,565.33** |
| newest Instagram clip at read time | 38 seconds before the query |

**Earnings concentration, and the number that matters operationally:**

| | top 5 | top 10 | top 25 |
|---|---|---|---|
| **share of Instagram earnings** | **50.1%** | **69.2%** | **93.9%** |
| **accounts those clippers posted from, last 30 days** | **8** | **17** | **33** |
| **share of last 30 days Instagram clip volume** | 24.8% | 57.1% | **76.4%** |

**The persuade list is 25 conversations covering 33 accounts, which carries 76.4% of Instagram clip volume and 93.9% of Instagram earnings. Not 69, not 99 and not 364.** This reproduces BL-786's 34 accounts at 76.7% within measurement noise.

## PART 3 — THE ROUTE NOBODY HAS PRICED: APPLYING TO META DIRECTLY

### What the refusal actually covers, precisely

BL-726 said Meta refuses individual developers. **The boundary is now exact, and it is not what BL-726 implied.** Meta's gate is not "you are one person". It is **"your business must be registered with local authorities"** (Meta Business Help Center article 1095661473946872). Meta nowhere says a company is required and nowhere excludes sole traders.

Meta's accepted document list (article 159334372093366): Certificate or Articles of Incorporation; **Business Registration or License Document**; Government Issued Business Tax Document, where **"Self-filed tax documents are not accepted"**; Business Bank Statement; Utility Bill, **"accepted only for Business Address and Phone number"**. **Every one presupposes registration with an authority, and the utility bill explicitly cannot establish the legal name. So a genuinely unregistered individual has no route. A REGISTERED SOLE TRADER is not excluded by anything Meta writes.**

**Disclosure on method, because it matters:** Meta's Business Help Center is a JavaScript shell that served title-only pages in Serbian to every direct fetch, on the plain URL, with `?id=`, with `?_rdr`, via `en-gb.facebook.com` and via `mbasic`. The article bodies above were read through a text-extraction proxy. **The content is Meta's; the retrieval was not first party.** Marked accordingly.

The one Meta-voice signal pointing the other way comes from a different product: Meta's Horizon OS developer docs say **"If you're an independent developer or a small studio without formal business registration, Admin Verification is likely the better option"** (https://developers.meta.com/horizon/resources/publish-organization-verification/). **There is no Admin Verification equivalent on the Business Suite side**, so this is suggestive, not binding.

### A DIRECT CONTRADICTION INSIDE META'S OWN HELP CENTRE, reported not averaged

**A second research surface reached a Meta help article the first could not, and it says something different.** The URL `https://m.facebook.com/help/iphone-app/243868559497297` rendered a full body listing document categories:

• **Organizations:** "Government-issued company or corporate registration"; "Company tax revenue document"; "Official articles of incorporation or association"
• **Sole proprietors:** "A government registration document" confirming sole proprietor status; "Company tax filing document"
• **Non-registered businesses/individuals:** **"Proof of ID"**, being "a valid government-issued identification with photograph, preferably passport", plus **"Proof of address"** matching the registered address and under 6 months old

**So one Meta article says verification requires being "registered with local authorities", and another Meta article publishes a document category explicitly for "non-registered businesses/individuals" needing only a passport and a proof of address.** Both are Meta's own text; they cannot both be a complete statement of the rule.

**The tie breaker, and it points against the individual route:** Meta's developer blog of 1 February 2023 states **"Individual verification will no longer be allowed for access once the business verification process is complete"**, and that apps not linked to a verified business "will have their access revoked for advanced permissions" (https://developers.facebook.com/blog/post/2023/02/01/developer-platform-requiring-business-verification-for-advanced-access/). The separate Individual Verification track, paused in 2020 and resumed in 2021, has been folded in.

**The forum shows the practical cost of that ambiguity.** Thread 2028000384724479, the most on point post found, verbatim: *"I don't have a registered company, and I dont think the form allows uploading a personal ID as a document"* — **and it has zero replies. Nobody answered him.** Elsewhere developers report an SS-4 with EIN rejected three times with no reason and no support path, one describing the process as *"a black box for me. Zero feedback"*, and one case that cycled rejected and reapplied for two months then was **approved same day on a resubmission with nothing changed.**

**Two mechanics worth knowing before trying:** Meta **auto cancels long pending verification cases**, so resubmission is required rather than optional; and **documents in a non English language require the application materials in that same language**, which matters directly for a Serbian APR rešenje.

**Honest net: the individual route is not provably closed, but it is undocumented, unanswered on Meta's own forum, and contradicted by Meta's own 2023 policy statement. The registered preduzetnik route is the one with a document category Meta names explicitly ("Sole proprietors: a government registration document"), and it costs about €21 to obtain.**

### What it costs in Serbia

**Cheapest suitable form is a preduzetnik (registered sole entrepreneur), decisively.** From the APR fee decision in force 1 January 2026: **preduzetnik registration 2,500 RSD, about €21**; a d.o.o. is 8,000 RSD, about €68, with minimum share capital of 100 RSD, about €1. Registration is statutorily decided within **5 days**; practical guidance says 3 to 5 days. APR issues a rešenje, a matični broj and a **PIB tax identification number**, and an izvod can be drawn from the public register.

**Does that satisfy Meta? On the evidence, yes.** The APR rešenje is precisely a "Business Registration or License Document issued by the relevant authorities" and the PIB certificate is a government issued business tax document rather than a self filed one. **What could NOT be established: whether any Meta reviewer has in fact accepted a Serbian preduzetnik, and whether APR's register sits inside Meta's automated lookup database.** If it does not, the flow falls to Meta's manual document upload branch, which is a supported path. **This is the single largest residual unknown, and it is a €21 experiment to resolve.**

**Ongoing cost is the real number, and it is not small.** Preduzetnik on the paušal flat rate scheme, IT activity codes 62.01/62.02 in Belgrade: roughly **35,000 to 60,000 RSD a month in tax and contributions, about €385 to €470, so €4,600 to €5,600 a year**, plus bookkeeping at 3,000 to 8,000 RSD a month, about €310 to €820 a year. **Total roughly €4,900 to €6,400 a year.** The paušal ceiling is 6,000,000 RSD, about €51,000, of annual invoiced turnover. These are secondary Serbian accounting sources; the binding figure is the tax authority's own rešenje.

### Timeline, and what rejection means

APR 3 to 5 days, then Business Verification **"may take up to 14 business days"**, then App Review, which Meta states **"typically takes us less than one week, and often takes only 2 to 3 days"**. **Realistic end to end: 3 to 8 weeks.**

**Rejection is normally per permission, not fatal.** Meta: "If we are able to test your app but cannot test functionality that requires a specific permission or feature, you will not be approved for that permission or feature", against the harsher "If we are unable to access your app to test it, your entire submission will be rejected." Resubmission is the expected path and **no Meta statement imposing a resubmission limit or cooling off period could be found**, though Meta's "After You Submit" page defeated every fetch route.

**Two costs nobody has priced before.** First, App Review demands **a screencast per permission** showing a user granting it and the app using it, plus a separate written description per permission, explicitly "Do not copy and paste." Second, the **annual Data Protection Assessment**, where "An admin of the app will be given 60 days to complete the assessment or risk losing platform access". **Whether Advanced Access alone triggers it could not be established.**

**One specific, avoidable failure mode:** a Serbian preduzetnik's legal name must incorporate the founder's personal name, so the Meta Business Portfolio must carry that exact legal name and not "Clippers HQ". Name mismatch against the verification documents is a commonly reported rejection reason.

### The comparison the owner has never been shown

| | own the integration, as a registered preduzetnik | use a vendor |
|---|---|---|
| setup cash | **about €21** at APR | **€0** |
| setup effort | 3 to 8 weeks, screencast per permission, OAuth build | signup and an API key, hours |
| recurring, year one | **about €4,900 to €6,400** tax and bookkeeping | **$0 to $1,440** depending on vendor, see PART 2 |
| per call fee to Meta | **none**, throttled not billed | not applicable |
| **name on the clipper's consent screen** | **HIS** | **the vendor's**, in front of every clipper |
| field access | whatever Meta grants him, permanently | whatever the vendor exposes, at the vendor's tier |
| vendor raises price, loses its Meta permission, or shuts down | **immune** | **total loss of the feature, with no remedy available to him** |
| annual Data Protection Assessment | **his to carry** | vendor absorbs it |

**The honest reading, and it is the thing that has never been put in front of him.** On pure cash the vendor wins: roughly €5,000 a year against $0 to $1,440. **But the comparison is contaminated in his favour, and the contamination is the point. The paušal tax is the cost of being a registered business in Serbia, not the cost of owning a Meta app.** If he would ever register anyway, for any reason, then **the marginal Meta attributable cost of owning the integration is €21 plus a few weeks of work, against a vendor dependency forever.** If he genuinely never intends to register, the true comparison is about €5,000 a year against $0 to $1,440 and the vendor wins on money while losing on control. **Which of those two situations he is in is a question only he can answer, and it decides this.**

**Is owning it outright the cleanest path? Yes, on every axis except cash, and the cash gap closes to €21 if he was ever going to register anyway.** It is the only route where his own name is on the consent screen, and the only route immune to a vendor's Meta permission lapsing and taking every clip analytic down at once.

## PART 1 — WHAT EACH SEARCH SURFACE FOUND

### SURFACE: COMPETITOR CLIPPING PLATFORMS — the most useful result of the round

Twelve platforms in this exact market were checked against their own pages, terms, privacy policies and FAQs: Whop / Content Rewards, Vyro, ClipAffiliates, Clipping.net, ClipCo, ClipReward, Cliptics, Ssemble Clip Rewards, Clipur, Lumina, TrendClips, Clipify and Clipping.io.

**THE DOMINANT PATTERN IS THAT CLIPPERS DO NOT AUTHORISE INSTAGRAM AT ALL.** Eight of the twelve verify only that the clipper owns the handle, by a one time code in the bio or a personal hashtag, and then read the **public** view count on a schedule. Four say so on their own marketing pages, as a selling point rather than an apology:

• **ClipCo**: "Connect your TikTok in one tap, or **drop a one time token in your bio for Instagram and YouTube**", and "For connected TikTok accounts we read view counts from TikTok's official API. **For everything else, our scraper checks each clip on a schedule**."
• **ClipReward**: "Verify channel control with a bio token. **We never ask for social passwords or store platform access tokens**."
• **Cliptics**: "Our infrastructure **scans Instagram Reels every 3 hours**, finds posts with the campaign hashtag on your verified accounts, and updates views and payouts automatically."
• **Clipping.net**: "verify ownership by adding a code to your bio temporarily", views "pulled straight from the source platform" every 12 hours.
• **Whop / Content Rewards**: linked accounts verify videos, and "**All submissions must come from public accounts**."

**Only ONE platform requires a real Instagram API grant: Vyro**, the best funded entrant. Its clipper terms enumerate "content views, engagement metrics, **analytics data and other metrics**", and its privacy policy points revocation at Instagram's own Apps and Websites page, which is real evidence of a genuine Meta OAuth grant rather than a bio code. **Clipur** connects but scopes it explicitly narrow: "Instagram: **Basic profile and media access**".

**NOT ONE PLATFORM IN THE ENTIRE MARKET CLAIMS WATCH TIME, RETENTION, COMPLETION RATE, AUDIENCE DEMOGRAPHICS OR TRAFFIC SOURCE.** Vyro's generic "analytics data and other metrics" is the high water mark across all twelve. **That is a real negative result, not a gap in the search, and it corroborates PART 0 from the demand side: nobody advertises these fields because for Instagram they largely do not exist.**

**Fraud detection in this market runs entirely on public signals.** Every published signal is derived from the public time series of views and engagement, and **not one is derived from connected account analytics**: ClipAffiliates names "sudden view spikes with zero engagement" and like ratio anomalies; Whop routes "spikes in views, possible botted traffic" to manual review; Cliptics claws back "bot views, engagement pod boosts, artificially inflated impressions"; Clipping.net runs viewbot detection with a 1,000 view floor. The operator of Content Rewards told Forbes that bot fraud is "**the single biggest threat**" to the model.

**One vendor claim collapsed on inspection.** ClipAffiliates advertises "direct API connections to Instagram", but its own privacy policy names **BrightData**, a scraping and proxy vendor, as the third party for social data verification. Stated as inference: the API language is marketing over a scraper.

**No clipping platform appears as a Meta Tech Provider or named Meta partner.** Meta's named launch partners for the Instagram Creator Marketplace API are Aspire, Captiv8 and CreatorIQ, all influencer marketing suites, none of them clipping marketplaces. Searched directly; negative result.

**Not found, and reported as not found:** no onboarding walkthrough showing the actual Instagram consent screen for any platform in this market could be observed, so **whose app name appears on Vyro's screen is unknown**. trendclips.io, clipifymedia.com and reach.cat returned 403; help.whop.com returned 401; YouTube walkthroughs served navigation chrome only.

**Adjacent context worth carrying:** Adam Mosseri announced that accounts mostly sharing others' content will not be recommended to non followers, which is expected to push clipping budget off Instagram toward TikTok and Shorts. Reported as secondary.

### SURFACE: THE OWNER'S OWN EXISTING VENDOR, checked because the ask is framed as "what bundle.social gives me for TikTok"

**It does not give him that for TikTok either.** bundle.social's live OpenAPI spec was fetched today (899,600 bytes, https://api.bundle.social/swagger-json) and searched: **ZERO occurrences of `average_time_watched`, `full_video_watched_rate`, `ig_reels_avg_watch_time`, `reels_skip_rate` or any watch time field, for any platform.** The normalised analytics schema is exactly nine fields, each appearing once: `impressions`, `impressionsUnique`, `views`, `viewsUnique`, `likes`, `dislikes`, `comments`, `shares`, `saves`. Four analytics routes exist: `/analytics/post`, `/post/bulk`, `/post/force` and `/post/raw`. **Everything richer lives only in `raw`, which BL-781 established is sales gated, typed with no schema, and has never returned a single observed field.**

**So the premise of the round needs correcting gently but plainly: the thing the owner wants replicated for Instagram has never actually been observed working for TikTok.** Also relevant to PART 3's table: bundle.social's **free tier does not include analytics at all**; Pro at **$100/month** is the first tier that does, and Business is $400/month.

### SURFACE: META'S OWN DEVELOPER COMMUNITY, CHANGELOG AND APP REVIEW DOCS

**The partner directory: NO USABLE DIRECTORY EXISTS, so no vendor's Tech Provider status is checkable by anyone.** Meta publishes no list of verified Tech Providers at all; the Tech Providers and Access Verification pages render fully and contain no directory or lookup. The Meta Business Partners directory root returns a hard **404**, and every search and detail path returns a login wall, with Google's indexed titles for detail pages reading literally "Log in or sign up to view." **So there is no presence or absence result for Composio, Zernio, PostPeer, Ayrshare, Blotato, Phyllo or bundle.social. Absence proves nothing here, because the directory cannot be read.** The only Meta owned mention of any of them is Phyllo in a 2021 Facebook Accelerator cohort post, which is accelerator membership, not Tech Provider verification.

**App Review requirements, quoted:** "Make at least 1 successful API call using each permission for which you are requesting advanced access. **Calls must be made within 30 days of submitting for App Review**"; "Upload a screencast showing the end to end user experience for that specific permission"; "Use English as the app UI language"; "Omit audio; our reviewers will not listen to it"; a privacy policy URL; a business email; a 1024x1024 icon; per permission usage descriptions; and reviewer login instructions that must not use personal credentials.

**The circular trap that dominates rejections.** The recurring reviewer text is **"We are not able to test requested permissions."** Thread 1418343268305761 shows the bind: a developer cannot demonstrate functionality in development mode without the permission she is applying for. Meta staff shaped answer on thread 1751720405784667: *"This usually happens when Meta hasn't yet detected a successful test API call for the specific permissions"*, then roughly 24 hours before the request option appears.

**THE MOST IMPORTANT OPERATIONAL FINDING ON THIS SURFACE, and it constrains any build.** Meta's own insights guide: **"If insights data you are requesting does not exist or is currently unavailable the API will return an empty data set instead of `0` for individual metrics."** **An empty array is therefore indistinguishable from a permission failure at the call site.** Threads 627351384669941, 764577022183278 and 988904539784780 all report insights silently going empty, the last with four developers confirming `"Instagram Insights Media API endpoint does not support the metrics: views"` on v22.0 despite the docs listing it. **Any verification logic built on this must treat empty as UNKNOWN and never as zero views.** That is exactly the present, null and absent discipline the platform's existing analytics store already enforces, and it must not be relaxed.

**A second finding that undercuts every route including owning the app.** Thread 1767291734273522, posted August 2026 and **still unanswered**: Advanced Access granted on 3 August 2026 to a verified business, yet the API still returned data only for app role holders, the developer noting *"the summary reports 14 total reactions… but the data array contains only 1 entry (a user with an admin role on the app)"*. **The grant and the behaviour change are not the same event.** That is precisely the risk the Tech Provider pass through is meant to absorb, and precisely what no readable directory lets anyone verify about any vendor.

**Changelog, dates fixed:** `reels_skip_rate` and `reposts` were **added 3 December 2025**, flagged "estimated and in development". `video_views` removed 2 October 2024. `plays`, `impressions`, `clips_replays_count` and `ig_reels_aggregated_all_plays_count` deprecated 21 January 2025 for v22.0+ and **for all versions on 21 April 2025**. `views` is the replacement and is still "in development". **Nothing Instagram related is scheduled for removal near term**; Graph v26.0 shipped 29 July 2026 and v23.0 runs to 8 October 2027. **The risk on `reels_skip_rate` is in development instability, not imminent removal.**

**A telling silence: ZERO forum threads mention `reels_skip_rate` anywhere in any search index. Not one developer post exists about it.** The one adjacent thread, 890723299272211, shows `ig_reels_avg_watch_time` and `ig_reels_video_view_total_time` breaking pagination with `"An unknown error has occurred.", "type": "OAuthException", "code": 1`, bisected to media from 2024-02-17 onward, **with no Meta reply and no resolution.**

**Whether the owner's intended use is permitted: Meta nowhere addresses it, in either direction.** No approval and no prohibition for a platform reading a creator's own insights, with consent, to verify a clip submitted for a per view payout. The nearest text is generic: Platform Terms §4.c "You may only Process Platform Data as clearly described in your privacy policy", §3.a.viii on permitted purposes, §3.a.iv barring selling or licensing Platform Data, and §3.c permitting sharing "when a User expressly directs you to share or expressly consents". **No written rule decides this. App Review reviewer discretion does.**

**Method gaps, reported rather than glossed:** Meta's forum search **renders but silently ignores the query parameter**, returning identical generic threads for every term, so all discovery had to route through external indexing. Forum **author role badges are stripped in conversion, so Meta staff attribution is unverifiable** on that surface, and two fetches of the same thread produced contradictory staff labels. Of 20 threads in the dedicated sweep, **7 have zero replies**, and essentially every useful answer came from other developers rather than from Meta.

**A THIRD first hand confirmation of the login path problem, which I ran myself.** Extracting every `instagram_*` permission named on Meta's Instagram App Review page (https://developers.facebook.com/docs/instagram-platform/app-review, 8,615 bytes) yields `instagram_manage_insights` **once** and **`instagram_business_manage_insights` not at all**, alongside `instagram_business_basic`, `instagram_business_content_publishing`, `instagram_business_manage_comments` and `instagram_business_manage_messages`. **So the permission is missing from the permissions reference (404), from the Instagram Login scope list, and from the App Review list. Three independent Meta surfaces, all saying the same thing.**

### SURFACE: REDDIT, HACKER NEWS, INDIE HACKERS AND STACK OVERFLOW

**Access reality first, because it changes how to read this.** Hacker News and Stack Overflow content were reachable. **Reddit thread BODIES AND COMMENTS WERE NOT**: reddit.com, old.reddit.com and api.reddit.com are domain blocked to the crawler, every mirror returned 403, 404 or a dead certificate, and archive.org is blocked. **For Reddit there are question titles and snippets and almost never the answers. That is a GAP, not an empty result, and the two must not be confused.** Indie Hackers search is a JavaScript shell; individual post URLs render.

**On the exact permission this project needs, the community record is essentially EMPTY, and that absence is the finding.** An exact phrase search for `"instagram_manage_insights"` across all of Reddit returned **one** result. Hacker News has **never** discussed it. **No firsthand account exists, on any of the four surfaces, of anyone submitting for either insights permission and describing the outcome.** Every detailed review story is about comments, messaging, media or login.

**What the adjacent record does establish is the SHAPE of the process, and it is brutal.** **MULTIPLE INDEPENDENT REPORTS**, five people 2021 to 2025: **14 attempts over almost 3 months**, by a former maintainer of a large part of Meta's own Graph API, for the trivial case of reading comments on his own users' posts, who concluded reviewers are "following a prefixed script to reject any applications that are NOT demonstrating a short list of predefined behaviors" and unlocked it only by **building fake UI he did not need**. Another: **12 submissions in 17 days across three separate reviews**, ranking Meta far below LinkedIn and YouTube. Another: two months, "it has taken more time than to develop the app almost." **A hard lockout exists: after 7 failed attempts, one developer was blocked from applying for 90 days**, and the support ticket form itself failed to send. One developer **completed business verification and was banned within minutes**, losing the developer account and the verified business, with appeals rejected (**SINGLE UNCORROBORATED CLAIM**, but severe).

**On the four fields, the community evidence is thinner than the documentation and points the same way as PART 0:**

• **`reels_skip_rate`: NO firsthand evidence it exists.** A direct Stack Overflow API search returned an empty result set across all of Stack Overflow; Reddit has zero hits. **Meta's changelog says it was added 3 December 2025 and Meta's reference documents it, but not one developer anywhere has publicly reported receiving a value.** Everything else asserting it is vendor marketing.
• **`ig_reels_avg_watch_time`: exactly ONE firsthand report, and it does not reconcile.** Stack Overflow 78072288 (2024, **no accepted answer**): the asker got `3755` back for a reel roughly one second long; the lone unaccepted answer says milliseconds. **Unresolved for over a year.**
• **Per post audience demographics: no evidence anywhere.** Every demographics question targets the IG User node, never a media node. **Corroborates PART 0 from the developer side.**
• **Traffic and discovery source: independently reported ABSENT, twice.** Stack Overflow 65495950, answer: "The Instagram Graph-API doesn't offer such a feature… The maximum you can do is to access the impressions metric". Stack Overflow 70251233, holding the full permission set, gets only aggregate reach. **MULTIPLE INDEPENDENT REPORTS. This is independent confirmation of PART 0's hardest conclusion.**
• Even account level demographics misbehave: Stack Overflow 76517263 got `follower_demographics` and friends back with **no `total_value` and no breakdowns array at all**.

**THREE FAILURE MODES THAT WOULD BITE A BUILD, all MULTIPLE INDEPENDENT REPORTS:**

1. **ONE BAD METRIC KILLS THE ENTIRE REQUEST.** `(#100) The Media Insights API does not support the impressions, replies metric for this media product type` took four valid Reels metrics down with it. Confirmed independently four times. **Request Reels metrics alone and branch on media type.**
2. **MEDIA POSTED BEFORE THE ACCOUNT WAS CONVERTED TO PROFESSIONAL RETURNS NO INSIGHTS, PERMANENTLY.** Stack Overflow 55268775, score 12, 5,033 views, four answers, **no accepted answer, unresolved since 2019**. Worse, Meta's error says "the *most recent* time" the account was converted, **so a creator who has flipped account type twice loses insights on everything before the last flip, and no API field exposes that date.** **For this platform that means a clipper who converts today yields nothing on any clip already submitted and paid for. Connected analytics would be forward looking only.**
3. **Organic only, and a 2 year retention wall.** Paid interactions are excluded from returned counts. **This kills historical backfill.**

**On using a vendor as the approved app: nobody on any of the four surfaces describes doing it and confirming it worked for analytics.** The strategy is implied entirely by vendor copy and never confirmed by a customer. Vendors named on HN are all self posted by their own founders. **Zero mentions anywhere on Hacker News of Phyllo, Late, Blotato, Mixpost, Publer, Metricool or Iconosquare.**

**Searched and found NOTHING, as distinct from could not reach:** `reels_skip_rate` anywhere; per post audience demographics; `navigation`, `profile_activity` or `follows_and_visits` as working media metrics; `instagram_business_manage_insights` anywhere on Stack Overflow; **any successful business verification by an unincorporated individual**; any dollar cost figure; and any Hacker News or Indie Hackers discussion of Instagram Reels watch time, retention or demographics via the API **at all**.

### SURFACE: GITHUB — the surface that settled the round

Run through Sourcegraph's unauthenticated code search, GitHub's issue search, direct raw file fetches, and GitHub's own authenticated code search which I ran myself.

**COMMITTED PAYLOADS, the strongest class of evidence, and what they prove.**

• **Watch time is REAL, and the units are settled: MILLISECONDS.** Airbyte's Reels insights fixture returns exactly eight metrics for a Reel: `comments` 7, **`ig_reels_avg_watch_time` 12549**, **`ig_reels_video_view_total_time` 30017581**, `likes` 108, `reach` 2006, `saved` 7, `shares` 1, `views` 5000, with Meta's description "The average watch time of your reel in **milliseconds**". **12,549 ms is 12.5 seconds, which is a plausible average watch on a Reel.** This is authored test data modelled on the real shape rather than a recorded cassette, so it fixes the response shape and the shipped metric set, not a live value. **It also resolves the Stack Overflow report of `3755` on a one second reel: at milliseconds that is 3.75 seconds, which means the reel was not one second long or the reader misread it. Units are milliseconds.**
• **Account level demographics are real and captured from a LIVE account.** Airbyte's `expected_records.jsonl`, recorded in CI against a real Instagram account, contains `follower_demographics` with breakdowns `city`, `country` and `age,gender`, and the mock counterpart shows the 45 city cap populated (Sydney 18, Bangalore 17, Lagos 15, New York 12). **Demographics work, at the account, exactly as PART 0 says.**
• A genuine media level `profile_activity` payload with an `action_type` breakdown resolving to `bio_link_clicked` 11, and a Story `navigation` payload (`tap_forward` 19, `tap_back` 4, `tap_exit` 1, `swipe_forward` 1). **`navigation` is within-story movement, not where a view came from.**

**THE FOUR ANSWERS.**

**1. `reels_skip_rate`: every hit is a NAME, never a VALUE.** It is in Meta's own codegen spec and in all five generated Meta SDKs, in both `InsightsResult` and `InstagramInsightsResult`; it is in Meta's own Postman collection; and one third party product (`whistlegraph/aesthetic-computer`) has shipped code that reads it, guarded `if (post.insights?.reels_skip_rate != null)` and rendering `—` when absent, with a comment dating its arrival to 2025-12-03, matching Meta's changelog exactly. **But no committed artifact anywhere proves it populates, and Airbyte's battle tested production connector does not request it at all.** So: the field is real, Meta ships it in its SDKs, one developer has coded defensively around it, **and its arrival is public knowledge while its value is not.** BL-787's claim of "committed real world values" is **overstated: there is committed real world CODE, not committed real world VALUES.**

**2. Per post audience demographics: settled NO, from Meta's own enum.** Meta's Instagram media insights metric enum is **23 values** and contains no demographic value: `comments, crossposted_views, facebook_views, follows, ig_reels_avg_watch_time, ig_reels_video_view_total_time, impressions, likes, link_clicks, navigation, profile_activity, profile_visits, reach, reels_skip_rate, replies, reposts, saved, shares, total_comments, total_interactions, total_likes, total_views, views`. The three demographics metrics appear only in the **user** insights enum block and only ever with an account id path in every fixture found.

**3. Per post traffic or discovery source: no working path, and one unexercised hint that must be reported honestly.** Meta's media level breakdown enum has exactly four values: `action_type`, `story_navigation_action_type`, `follow_type` and **`surface_type`**. **That is a contradiction with Meta's own documentation, which states "No breakdowns exist for follow_type, age, gender, city, country, or source", and it is reported rather than averaged.** But: **zero committed code anywhere passes `breakdown=surface_type`, and no enumerated `surface_type` dimension values exist in any public repository.** Every committed instance of `follow_type` is account level (`{ig-user-id}/insights/reach/day`), never per post. **So the honest position is not "impossible" but "no proven path, never publicly exercised, and returned values undocumented anywhere." If the owner wants one long shot, `breakdown=surface_type` on a Reel is it, and it costs one call to try.**

**4. Retention curve: refuted for Instagram, confirmed for Facebook, exactly as PART 0 says.** `post_video_retention_graph` appears only in Facebook Page post code across three independent repositories and **in no Instagram code path anywhere.** Instagram's only time based signals are the two aggregates.

**WHAT PRODUCTION CODE ACTUALLY REQUESTS, which is the practical ceiling.** Airbyte's connector, running against real customer accounts, requests per media type: **Reels** `comments,ig_reels_avg_watch_time,ig_reels_video_view_total_time,likes,reach,saved,shares,views`; feed video only `reach,saved`; carousel `reach,saved,shares,follows,profile_visits`; stories `reach,replies,follows,profile_visits,shares,total_interactions,views`. **Note what is absent from the Reels set: `reels_skip_rate`.**

**Two production hardened error behaviours worth copying.** Airbyte ships an explicit ignore handler for **error `2108006`, media posted before the account converted to business** — independent production confirmation of the Stack Overflow finding — and for `code 100 / subcode 33` and `code 10`, surfaced as "Check provided permissions for". Live errors quoted in issues include `(#100) The metric shares is not supported for this media type`, confirming that **metric availability varies by media type and one bad metric fails the request.**

**Self hostable projects that would work with his own Meta app, if he takes PART 3's route:** `exileum/meta-mcp` (33 Instagram tools, built around your own Meta Developer App, with per media type metric handling), `gitroomhq/postiz-app`, `inovector/mixpost`, and `airbytehq/airbyte`'s `source-instagram` as the most battle tested ingestion path.

**Explicit negatives, reported as findings:** nothing on GitHub shows a populated `reels_skip_rate`; nothing shows per media demographics; nothing shows an Instagram per post traffic source; nothing uses `breakdown=surface_type`; nothing shows an Instagram retention curve; and **no maintainer or user documents an actual Meta App Review outcome for an individual without a company.**

## PART 2 — THE CANDIDATES, MEASURED AGAINST THE CEILING

**Every field claim below was fetched by me directly from the vendor's own documentation or OpenAPI bundle, not taken from a subagent summary. Nothing was exercised against a live key, so every capability claim is DOCUMENTED ONLY and UNVERIFIED in practice.**

**No candidate's claims exceeded PART 0's ceiling.** That is itself worth stating: the vendors are honest about Instagram, and it is the owner's expectation, not their marketing, that needs adjusting. **One clarification is needed though: BL-786 and BL-787 credited Composio with "audience demographics", which is true but is ACCOUNT LEVEL, via a different tool. It is not per clip and must not be read as per clip.** Composio's own documentation confirms it: **"No per post audience demographics available. Only account level demographic insights."**

| | **Composio** | **Zernio** | **PostPeer** | **own Meta app** |
|---|---|---|---|---|
| watch time | **YES** `ig_reels_avg_watch_time`, `ig_reels_video_view_total_time` | **YES** `igReelsAvgWatchTime`, `igReelsVideoViewTotalTime`, both in ms | **YES** `avgWatchTime`, `totalWatchTime`, in seconds | **YES** |
| skip rate | **YES** `reels_skip_rate` | **NO** | **NO** | **YES** |
| completion estimate | no | **DERIVABLE**, uniquely, see below | no | derivable |
| per clip demographics | **NO** (account level only) | **NO** (account level only) | **NO** | **NO, does not exist** |
| per clip traffic source | **NO** | **NO** | **NO** | **NO, does not exist** |
| **cost at his volume** | **$0**, or **$29** if refreshing daily | **$117/mo** for 33 accounts, **$315/mo** for all 99 | **$25 to $43/mo** | **€21 once**, then Serbian tax |
| pricing unit | tool calls, 20,000/mo free | **per connected account**, graduated | credits, 1 per call, **accounts unlimited** | none, throttled not billed |
| company required | no | no | no | **YES, registration** |
| **name on consent screen** | **"Composio"** by default | **UNKNOWN**, not documented | **UNKNOWN**, not documented | **HIS** |
| genuine Meta screen | **yes**, Instagram Login | **yes**, Instagram Login default | **yes**, Instagram Login | yes |

### Composio, and the branding finding that CORRECTS BL-787

`INSTAGRAM_GET_IG_MEDIA_INSIGHTS` accepts exactly Meta's metric set, passing it through rather than normalising it away, which is why it alone carries `reels_skip_rate` (https://docs.composio.dev/toolkits/instagram). Pricing: free 20,000 tool calls a month, then **$29** for 200,000 and $0.299 per additional thousand. At 1,273 Instagram clips a month a single capture per clip is roughly 4,000 calls, comfortably inside free; a daily refresh is about 38,000 and needs the $29 tier.

**TIME SENSITIVE, AND IT UNDERMINES THE $0 HEADLINE FROM TWO PRIOR ROUNDS: Composio's pricing page currently states "Pricing will be changing on August 15th."** That is three days from this report. **Any $0 recommendation should be re confirmed after that date before it is relied upon.**

**BL-787 said Composio's consent screen cannot be rebranded. That is not correct, and the correction matters.** Composio's own custom auth documentation gives white labelling as a reason to bring your own credentials: **"Show your app name on OAuth consent screens instead of 'Composio'"** (https://docs.composio.dev/docs/custom-auth-configs). The mechanism is simply that Meta's screen names whichever Meta app is making the request. **BL-787 conflated white labelling Composio's own hosted Connect Link page, which does not change Meta's screen, with supplying your own Meta OAuth credentials, which does.**

**But the correction is circular and ends where PART 3 begins.** To put his own name on the screen through Composio he must supply his own Meta app, which requires App Review and Business Verification, which requires registration. **Composio removes the approval burden only for as long as he accepts Composio's name in front of every clipper.**

Composio also confirms the managed app's limits: bringing your own app gives **"dedicated quota"** rather than shared, and **"custom scopes"** beyond **"Composio's default approvals"** — wording that implies a fixed approved scope set on the managed app.

**THE QUESTION TWO PRIOR ROUNDS COULD NOT SETTLE, AND WHY IT CANNOT BE SETTLED FROM DOCUMENTATION AT ALL.** Whether Composio's managed Meta app actually holds `instagram_business_manage_insights` decides whether any of this works. I fetched Composio's complete documentation bundle (`llms-full.txt`, 744,892 bytes) and searched it: **ZERO occurrences of `instagram_business_manage_insights` or `instagram_manage_insights`.** Composio nowhere documents which Meta scopes its managed Instagram app requests or holds. **Only a live call settles it, which is exactly why PART 5 ends in a free test.** The one adjacent precedent remains BL-787's find, Composio's own FAQ: "If a reply to comment flow fails because the managed OAuth app does not currently have the required comment permission, use your own Meta OAuth app." **No equivalent statement exists for insights, in either direction.**

### Zernio, and the one thing it has that nobody else does

Its Instagram platform page lists only impressions, reach, likes, comments, shares, saves and views, with **no watch time at all**, which contradicts BL-787. **BL-787 was right and the platform page undersells the product.** Zernio's own full documentation bundle (`llms-full.txt`, 3,988,480 bytes) settles it verbatim:

> **`igReelsAvgWatchTime`** integer: "Instagram Reels only: average watch time per play, in milliseconds."
> **`igReelsVideoViewTotalTime`** integer: "Instagram Reels only: total watch time including replays, in milliseconds."
> **`videoDurationSeconds`** integer, null: "Video length in seconds. Currently Instagram Reels only; **combine with igReelsAvgWatchTime (ms) to estimate retention.** Null when unknown (other platforms, non video media, or **when Instagram does not expose the media URL, e.g. reels with copyrighted audio**)."

**That third field is the only genuine differentiator found anywhere in four rounds: Zernio supplies the DENOMINATOR.** Average watch time divided by video duration is a computed completion percentage, which is the closest anything gets to the completion rate Meta does not provide for Instagram. **Composio gives Meta's own skip rate; Zernio lets you compute a completion estimate. They approach the same missing metric from opposite sides, and neither is the other.**

**The caveat is Zernio's own and it is serious for this use case: `videoDurationSeconds` is null for "reels with copyrighted audio", which is a substantial share of clipping output. BL-787 flagged the null rate as unverified and it remains unverified.**

Pricing is **per connected social account, graduated**: 1 to 2 free, 3 to 10 at $6, 11 to 100 at $3, 101+ at $1 with no cap (https://zernio.com/pricing). For the 33 accounts of the top 25 clippers that is 2 free plus 8 at $6 plus 23 at $3 = **$117 a month**; for all 99 posting accounts, **$315 a month**.

**One prior unknown now settled: BL-787 could not establish whether Zernio's free tier includes analytics. It does.** Zernio's pricing page states the free tier includes **"full access to all features including scheduling, analytics, inbox, and the API"** for 1 to 2 accounts. **That makes Zernio a viable zero cost test path for one real clipper.**

### PostPeer

`avgWatchTime` and `totalWatchTime` for Reels in seconds, sourced from `source=platform` so it reads natively posted clips, 1 credit per call with up to 100 posts per call, and **unlimited connected accounts on every tier** including free. $25 for 2,000 credits, $43 for 6,000, $120 for 20,000. **No skip rate, no demographics, and it names `instagram_business_manage_insights` in its analytics documentation, which is more than Composio does.** Verified unchanged today with no announced pricing change. It remains a small single founder vendor with no published rate limits, no data retention policy and no stated legal entity.

### Ruled out on the ceiling, not on price

Any vendor promising Instagram **retention curves, per post demographics or per post traffic source is claiming something Meta does not expose**, and PART 0 is the test. Phyllo markets "Avg. Watch Time", "Completion Rate" and "Drop off Points" for Reels; **"Drop off Points" exceeds the ceiling and cannot be delivered for Instagram**, and no Phyllo page states its own API returns any of the three. Ayrshare ($149 for 1 profile to $599 for 30) and Blotato (capped at 20, 40 and 100 accounts, and only its $499 tier has a 6 hour checkpoint) both return real watch time and both remain priced or capped per connected account.

## PART 5 — THE ANSWER

### The single best route, in one line

> **COMPOSIO, at $0 a month today rising to at most $29 if he refreshes daily, returning `ig_reels_avg_watch_time` and `ig_reels_video_view_total_time` per Reel in milliseconds, `reels_skip_rate` if it populates at all, plus every public count and account level demographics, over Instagram Login so no clipper needs a Facebook Page, with "Composio" and NOT Clippers HQ on the clipper's consent screen.**

**The runner up is owning the integration outright as a registered Serbian preduzetnik: about €21 at APR, then roughly €4,900 to €6,400 a year in tax and bookkeeping, 3 to 8 weeks end to end, returning the identical fields because everyone reads the same API, with HIS name on the consent screen and no vendor able to raise his price, lose its Meta permission or shut down under him. It loses on cash and on time to first data. It wins on everything else, and the cash gap collapses to €21 if he was ever going to register a business anyway.**

**Zernio is third**, at $117 a month for the 33 accounts that matter. It loses on price and on skip rate, but it is the only route that supplies `videoDurationSeconds`, the denominator that turns average watch time into a computed completion estimate. **PostPeer is fourth** at $25 to $43, watch time only.

### The honest health warning, which two prior rounds did not carry

**One thing got BETTER during the round and two got worse.**

**BETTER: the Instagram Login path works, so no clipper needs a Facebook Page.** Four Meta documentation surfaces omit `instagram_business_manage_insights` and one of them 404s, and following the documentation alone I concluded mid round that Facebook Login was probably required. **A dozen production codebases refuted that, including Botpress, Postiz, Oracle and restfb, plus a runtime guard in AiToEarn that errors on the scope being missing.** The onboarding is therefore 6 steps in the Instagram app plus one authorisation, and no Page.

**WORSE ONE: `reels_skip_rate` has NEVER been publicly observed returning a value, by anyone, anywhere.** It is in Meta's changelog dated 3 December 2025, flagged "estimated and in development", and in all five of Meta's own SDKs. But **Stack Overflow, Reddit, Hacker News and GitHub contain zero populated values**, and **Airbyte's battle tested production connector does not request it at all** while requesting both watch time fields. **Composio is the recommended route precisely because it is the only vendor passing that metric through, so the metric that makes it the winner is the metric with the least evidence behind it.** If skip rate turns out not to populate, **Composio's advantage over Zernio and PostPeer evaporates entirely** and the choice reverts to price.

**WORSE TWO: insights do not exist for media posted before the account became professional, permanently, and this is confirmed in production code.** Airbyte ships a dedicated ignore handler for Meta error **`2108006`** for exactly this. So connected analytics is **forward looking only**: converting a clipper today yields nothing on any clip already submitted and paid for, and Meta's error text says "the most recent time" the account was converted, so a clipper who has flipped account type twice loses everything before the last flip.

**And one constraint on what it can ever be used for**, independent of all the above: Meta delays insights "up to 48 hours", while **89.9% of Instagram clips here are reviewed within 48 hours and the median is 5.32 hours.** This is a clipper record and post hoc signal, not a review queue signal.

### The ordered steps, ending in a free test before any code

**STEP 1, and it costs nothing: settle the login path and the scope grant in ONE call.** Create a Composio free account (email only, no credit card, 20,000 tool calls a month). Connect **one Instagram professional account the owner controls**, never a clipper's. Before authorising, **read the consent screen and record two things: whose name it shows, and whether an insights scope is listed at all.** Then call `INSTAGRAM_GET_IG_MEDIA_INSIGHTS` on one Reel **at least 48 hours old**, requesting **only** `ig_reels_avg_watch_time`, `ig_reels_video_view_total_time` and `reels_skip_rate`, and nothing else, because one unsupported metric fails the whole request.

**STEP 2: read the result against three outcomes, and treat them differently.**
• **Numbers come back** → the route works, the Instagram Login path is fine despite the scope lists, and the owner has his answer.
• **An explicit permission error** → Composio's managed app lacks the grant. Re test on Zernio's free tier, which includes "full access to all features including scheduling, analytics, inbox, and the API" for 1 to 2 accounts, and which would also confirm the fields independently.
• **An EMPTY ARRAY** → **this is the trap and it must not be read as a zero.** Meta's own documentation: "If insights data you are requesting does not exist or is currently unavailable the API will return an empty data set instead of `0`." Empty is indistinguishable from a permission failure at the call site. **Treat empty as UNKNOWN, never as zero views, both in the test and in any code that ever follows.**

**STEP 3: the units are MILLISECONDS, so sanity check against that.** Airbyte's fixture carries Meta's own description, "The average watch time of your reel in **milliseconds**", with a worked value of `12549`, which is 12.5 seconds. Zernio documents milliseconds and **PostPeer documents seconds, so PostPeer is converting and its numbers are not directly comparable to the others.** Divide by the reel's real duration and check the result against what the Instagram app shows for the same reel.

**STEP 3b, one free long shot while he is in there.** Meta's media breakdown enum contains **`surface_type`**, which Meta's own documentation says does not exist and which **no public code has ever called.** Add `breakdown=surface_type` to one Reel insights call. If it returns dimension values, he has the per clip discovery source that this report says is unobtainable, and that would be a genuine discovery. **If it errors, nothing is lost and the ceiling in PART 0 stands.**

**STEP 4, only if steps 1 to 3 succeed: decide the branding question, which is a business decision and not a technical one.** Composio at $0 to $29 with a vendor's name in front of every clipper, against about €21 plus a Serbian registration to put his own name there permanently. **Given that 8 of the 12 competitor platforms do not ask clippers to connect Instagram at all, an unfamiliar third party name on the consent screen is a real adoption cost, not a cosmetic one.**

**STEP 5: only then, and only for the 25 clippers who matter.** The persuade list is 33 accounts carrying 76.4% of Instagram clip volume and 93.9% of Instagram earnings. **Not 364 accounts and not 1,240 clippers.**

**One thing to re confirm before relying on any of it: Composio's pricing page currently says "Pricing will be changing on August 15th", three days from this report.**

### The clipper account suspension risk, stated plainly

**Genuine Meta OAuth carries no evidenced risk to a clipper's account.** Authorisation happens on Meta's own domain, the token is scoped, and the clipper can revoke it themselves at instagram.com in Apps and Websites. Every route recommended here is genuine OAuth. **The realistic failure is at the app level, Meta revoking a vendor's access, which breaks the platform's pipeline and not the clipper's account.**

**Credential capture is a different category and is documented, severe and must never be adopted.** Meta Platform Terms §6.a.iii: "you must not separately request or collect a Meta user's login credentials for any Meta Products." Meta disabled **over 60,000 Facebook and Instagram accounts** in the Voyager Labs action, obtained a permanent injunction against BrandTotal for harvesting authenticated sessions, and **forced password resets on users of third party tools** during an inauthentic engagement purge. Instagram tells users directly: "Never share login credentials with any person or application." **If this platform ever asks a clipper for a password or a session cookie, the account at risk is the clipper's, and they handed it over on this platform's prompt.** ClipReward advertises the opposite as a feature: "We never ask for social passwords or store platform access tokens."

**The real, non obvious risk here is a different one and it lands on the clipper's reach, not their login.** Converting to a professional account is required, and **"Professional accounts cannot be set to private"**, so a private clipper must go public to participate. Separately, Adam Mosseri has announced that accounts mostly sharing others' content will not be recommended to non followers, which is reported as pushing clipping budget off Instagram entirely. **Asking clippers to go public and convert, for a signal that is forward looking only and cannot inform 90% of review decisions, is the honest shape of what is being proposed.**

## SAFETY AND DISCLOSURE

READ ONLY, one document, on `checkpoint/BL-789` from `origin/main` `72f05cec`. **No code, config, schema or data change; no account connected; no payment details entered; no paid plan started; nothing signed up for; no credential stored, logged, printed or committed.** The only vendor and Meta interactions were unauthenticated public documentation and OpenAPI fetches. Every capability, pricing and terms claim carries a primary URL, and everything unexercised is marked UNVERIFIED. Read only `SELECT`s ran through `scripts/run-select.js` against production, every timestamp cast `::text` against DB `now()`; no write, no money, no schema, no cron touched, and no clip status, earnings or payout changed. No handle, caption, wallet address or email appears above; clipper identifiers are counts only. The 6 money files, `tracking.ts` and `campaign-era.ts` are byte identical by blob OID between `main` and this branch: this branch's diff is exactly one new markdown file. **No Apify actor was run** and no API key was logged. Five subagents ran, one per search surface, all read only, none permitted to write a file, sign up or connect an account. Worktree removed. No dashes as bullets. **Nothing here may auto reject a clip or be shown to a clipper: BL-518 and BL-521 stand.**

**Rollback:** delete branch `checkpoint/BL-789`. It contains one document and touches nothing.
