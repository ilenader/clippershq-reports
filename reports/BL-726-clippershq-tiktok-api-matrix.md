# BL-726 — Which TikTok API actually carries the analytics, and whether this owner can ever reach it

**THE ANSWER, IN THREE SENTENCES, BEFORE ANYTHING ELSE.** The rich fields the owner wants exist on exactly one platform, the **TikTok API for Business** at `business-api.tiktok.com`, and **nothing on the Display API at `open.tiktokapis.com` carries them**, not under any scope, not under any product. That platform requires a **separate developer registration**, and TikTok's own registration page says, verbatim: **"Currently, we are unable to onboard personal accounts or individual developers."** So the honest verdict is **(c)**: as an Individual with no registered company, the owner **cannot obtain the rich analytics at all today**, and the project as currently scoped delivers ownership proof plus basic counts, not the screen-share replacement he has been led to expect.

**2026-08-06 · AUDIT ONLY. READ ONLY.** No code, config or data change. Nothing registered, nothing submitted, no credential stored. Base `origin/main` `de0169bd`, branch `checkpoint/BL-726`, isolated worktree at the short path `C:/b726`, `node_modules` never junctioned. A markdown-only diff cannot change tsc or build, so none was run and none is claimed. Every capability claim below cites TikTok's OWN documentation with a URL; **no blog post, no third-party SDK doc and no secondary summary was used for any capability claim**, because two such sources have already contradicted the official docs in earlier rounds of this project.

---

## PART 1 — THE FIELD MATRIX

Columns: **Display API** = `open.tiktokapis.com`, documented at `developers.tiktok.com`, the platform the owner is registering a Login Kit app for. **API for Business** = `business-api.tiktok.com/open_api/v1.3`, the Accounts API, a separate platform with a separate portal.

| Metric the owner cares about | Display API (`open.tiktokapis.com`) | API for Business (`business-api.tiktok.com`) |
|---|---|---|
| **Views** | **AVAILABLE** `view_count` (int64) [1] | **AVAILABLE** `video_views` (scope `video.list`) [5] |
| **Likes** | **AVAILABLE** `like_count` (int32) [1] | **AVAILABLE** `likes` (scope `video.list`) [5] |
| **Comments** | **AVAILABLE** `comment_count` (int32) [1] | **AVAILABLE** `comments` (scope `video.list`) [5] |
| **Shares** | **AVAILABLE** `share_count` (int32) [1] | **AVAILABLE** `shares` (scope `video.list`) [5] |
| **Reach** (unique people) | **ABSENT** [1][2] | **AVAILABLE** `reach` (scope `video.list`) [5] |
| **Video duration** | **AVAILABLE** `duration` (int32, seconds) [1] | **AVAILABLE** `video_duration` (float, 3 dp) [5] |
| **Full video watched rate** | **ABSENT** [1][2] | **AVAILABLE** `full_video_watched_rate` (scope `video.insights`) [5] |
| **Average time watched** | **ABSENT** [1][2] | **AVAILABLE** `average_time_watched` (scope `video.insights`) [5] |
| **Total time watched** | **ABSENT** [1][2] | **AVAILABLE** `total_time_watched` (scope `video.insights`) [5] |
| **Impression sources** (traffic source) | **ABSENT** [1][2] | **AVAILABLE** `impression_sources` (scope `video.insights`), enum `For You`, `Follow`, `Sound`, `Personal Profile`, `Search`, `Others`, `Direct Message` [5] |
| **Audience countries** | **ABSENT** [1][2][3] | **AVAILABLE** twice: `audience_countries` per video (scope `video.insights`, max 10) [5], and per account (scope `user.insights`, **needs 100+ followers**) [6] |
| **Audience genders** | **ABSENT** [1][2][3] | **AVAILABLE** twice: `audience_genders` per video (scope `video.insights`) [5], and per account (scope `user.insights`, **needs 100+ followers**) [6] |
| **Audience activity** (hourly follower activity) | **ABSENT** [2][3] | **AVAILABLE** `audience_activity` per account (scope `user.insights`), **Business Accounts with 100+ followers only** [6] |
| **Follower count** | **AVAILABLE** `follower_count` (int64, scope `user.info.stats`) [3] | **AVAILABLE** `followers_count` (scope `user.info.stats`), plus a daily series (scope `user.insights`) [6] |
| **Profile views** | **ABSENT** [2][3] | **AVAILABLE** twice: `profile_views` per video (scope `video.insights`, **Business Accounts only**) [5], and daily per account (scope `user.insights`) [6] |

Two further rows, because they are the strongest screen-share replacements of all and neither exists on the Display API:

| Metric | Display API | API for Business |
|---|---|---|
| **Audience retention curve** | **ABSENT** [1][2] | **AVAILABLE** `video_view_retention`, an array of `{second, percentage}` (scope `video.insights`) [5] |
| **Viewer types** (new vs returning, follower vs non-follower) | **ABSENT** [1][2] | **AVAILABLE** `audience_types`, enum `NEW_VIEWER`, `RETURN_VIEWER`, `FOLLOWER_PERCENT`, `NON_FOLLOWER_PERCENT` (scope `video.insights`) [5] |

**Why every Display API "ABSENT" above is a hard ABSENT and not an UNVERIFIED.** Two independent official pages close it. First, the **Video Object** page is the complete queryable field set for `/v2/video/list/` and `/v2/video/query/`, and it lists exactly fifteen fields: `id`, `create_time`, `cover_image_url`, `share_url`, `video_description`, `duration`, `height`, `width`, `title`, `embed_html`, `embed_link`, `like_count`, `comment_count`, `share_count`, `view_count` [1]. There is no sixteenth. Second, and more decisively, **TikTok's own scope reference lists every scope the platform issues**, grouped as Local Service, Data Portability, Research, User Profile (`user.info.basic`, `user.info.profile`, `user.info.stats`) and Video (`video.list`, `video.publish`, `video.upload`) [2]. **There is no analytics scope, no insights scope, and nothing resembling `video.insights` anywhere on `developers.tiktok.com`.** A field with no scope to unlock it is not a field that is merely undocumented; it is a field that does not exist on that platform.

**Two other doors on `developers.tiktok.com`, both checked and both closed.**
• **Data Portability API.** Its Data Types page lists what a Posts export contains: `Date`, `Posted Video Download Link`, `Received Likes num`, `Title`, `Who can view`, `Allow comments`, `Allow stitches`, `Allow duets`, `Allow stickers`, `Allow sharing to story`, `Content disclosure`, `AI-generated content`, `Location`, `Sound`, `Add yours text`, `Alternate text`, `Number of Collections` [7]. **No views, no watch time, no retention, no traffic source, no demographics.** The only engagement figure in the whole export is `Received Likes num`. Approval also takes "3-4 weeks" and needs UX mockups [8]. It is not a route to analytics.
• **Research API.** Requires the applicant to "be independent from commercial interests" and to "conduct research on a not-for-profit or non-commercial basis", with a research proposal and evidence of ethical review, and it is open to US and Europe-based **non-profit academic institutions** [9]. A commercial SaaS platform is excluded by definition.

### The one sentence

**To replace a screen-share call the owner needs the TikTok API for Business, because a screen-share call is him looking at retention, watch time, traffic sources and audience breakdown, and every single one of those exists ONLY on `business-api.tiktok.com` and none of them exists anywhere on the Display API.**

The Display API gives what a public scraper already gives (views, likes, comments, shares, duration) plus the one thing a scraper cannot give, which is **proof that the person authorizing owns the account**. That is genuinely valuable, and PART 4 says so. It is not what the owner asked for.

---

## PART 2 — ONE APP OR TWO

### Two. Definitively. They are different platforms with different registrations.

**A `developers.tiktok.com` app cannot call `business-api.tiktok.com` endpoints.** Every layer differs:

| | Display API / Login Kit | API for Business / Accounts API |
|---|---|---|
| Portal | `developers.tiktok.com` | `business-api.tiktok.com/portal` and `ads.tiktok.com/marketing_api/apps/` [4][10] |
| Prerequisite account | a TikTok for Developers account | **a TikTok For Business account** plus **an approved developer registration** [4] |
| App credential names | `client_key` + `client_secret` [11] | `client_id` (App ID) + `client_secret` [12] |
| Token endpoint | `POST https://open.tiktokapis.com/v2/oauth/token/`, `Content-Type: application/x-www-form-urlencoded`, param `code` [11] | `POST https://business-api.tiktok.com/open_api/v1.3/tt_user/oauth2/token/`, `Content-Type: application/json`, param `auth_code` [12] |
| API auth header | `Authorization: Bearer <token>` | `Access-Token: <token>` [5] |
| Scope namespace | `user.info.basic`, `video.list` [2] | `video.list`, `video.insights`, `user.insights` **inside the "TikTok Accounts" permission** [4][5][6] |
| Authorize URL | one your app constructs | one you **copy** from My Apps > App Detail > Basic Information [4] |

TikTok's Accounts API Authorization page states the prerequisites as three separate things: "You've created a TikTok For Business account", "You've registered as a developer", and "You've created a developer app with the required scope of permissions which includes 'TikTok Accounts'" [4]. A Login Kit app satisfies none of them.

### What the second app requires, and the sentence that ends the project in its current form

TikTok's own **Register as a developer** page for the API for Business [10]:

> "Note that communication email must be a verified **company domain** email. You will be rejected if you are using a personal email or a temporary email."

> "Select the user type that best describes your company": **Technology Company**, **Direct Advertiser**, **Agency**. There is no Individual option.

> "Fill in your **company name**. Your company name should: Be a valid brand name or a legit entity name."

> "Fill in your **company website** ... Be a company website, rather than a personal website. **Currently, we are unable to onboard personal accounts or individual developers.** If you are part of a company, please use your company website."

> "You will be notified of the review result in **three business days**."

**That is TikTok stating, in its own words, on its own registration page, that an individual developer cannot register.** BL-724 established that the owner is submitting to `developers.tiktok.com` as an **Individual** precisely because organization registration there demands government-issued business documents he does not have. The API for Business registration is stricter, not looser: it demands a company name, a company website, a company-domain email, and a company user type, and it says outright that individuals are not onboarded.

**Then there are two further gates behind that one**, both of which only matter if the first is passed:
1. **The Accounts API Access Application Form**, mandatory since **2026-03-20 00:00 GMT+0** "before submitting a new developer app or requesting a scope increase that includes the 'TikTok Accounts' permission scope" [13]. TikTok publishes no timeline for it. **UNVERIFIED** how long it takes; what would settle it is submitting one.
2. **The developer app review itself, "2 to 3 business days"** [12], on top of the three business days for the developer profile [10].

### Is advertiser status or an Ads Manager account required? Precisely stated.

**Not as a documented hard prerequisite, but the platform is unambiguously built for advertisers and one of the three user types is "Direct Advertiser".** The Accounts API overview describes the product as one that "Enables **advertisers** with owned Business Accounts or Personal Accounts on TikTok to gain access to detailed analytics and insights around their follower base and video engagements", and lists among its benefits "Enabling third party partners to leverage the data for cross-platform monitoring and reporting" [13]. The prerequisite list [4] names a TikTok For Business account and a developer registration, and does **not** name an ad account or ad spend. So: **advertiser status is UNVERIFIED as a hard requirement; company status is a documented hard requirement.** What would settle the advertiser question: attempting the registration with a Technology Company user type and no ad spend. What would settle the company question: nothing, because TikTok already answered it in writing.

**And one clause the owner must read before spending a day on any of this**, from the same overview, under **Prohibited Uses of Accounts API** [13]:

> "Extract reports of TikTok profiles and posts from authorized creators' accounts, and use the aggregated data to develop a self-built **affiliate influencer marketing program (such as creator discovery and ranking)**, instead of using the TikTok One platform or API."

TikTok also states it "reserves the right to revoke a developer's Accounts API access at any time without prior notice". Clippers HQ pays creators CPM for brand campaigns. The intended use here is narrow and arguably fine (verifying the view count of a post the creator themselves submitted for payment), but this clause is judged by a human on the access form, and it is a second, independent reason the API for Business path may end in a refusal even for a company.

---

## PART 3 — WHAT BL-723 ACTUALLY BUILT, AND WHAT WOULD HAPPEN ON CAMERA

Read from the branch (`git show checkpoint/BL-723:...`). **BL-723 targets the API for Business, completely and exclusively.**

| Thing | What BL-723's code has |
|---|---|
| Base URL | `TIKTOK_BUSINESS_BASE = "https://business-api.tiktok.com/open_api/v1.3"` (`config.ts:24`) |
| Data endpoint | `GET ${BASE}/business/video/list/?business_id=...&fields=[...]` (`client.ts:71`) |
| API auth header | `{ "Access-Token": req.accessToken }` (`client.ts:80`) |
| Token endpoints | `POST /tt_user/oauth2/token/`, `/tt_user/oauth2/refresh_token/`, `/tt_user/oauth2/revoke/` (`oauth.ts:226,243,259`) |
| Token request body | JSON, `Content-Type: application/json`, fields `client_id`, `client_secret`, `grant_type`, `auth_code`, `redirect_uri` (`oauth.ts:136,226`) |
| Scopes it declares | `TIKTOK_BUSINESS_REQUIRED_SCOPES = ["video.list", "video.insights"]` (`config.ts:28`) |
| Authorize URL | not constructed; read from env `TIKTOK_BUSINESS_AUTHORIZE_URL`, because the API for Business hands you a ready-made one (`config.ts:14, 95`) |
| Redirect URL validation | enforces the API for Business's six rules including a **mandatory trailing slash** (`config.ts`) |

**Every one of those seven rows is wrong for a Login Kit app.** The host is wrong, the header is wrong (`Access-Token` instead of `Authorization: Bearer`), the token URL is wrong, the content type is wrong (`application/json` instead of `application/x-www-form-urlencoded`), the credential parameter name is wrong (`client_id` instead of `client_key`), the code parameter name is wrong (`auth_code` instead of `code`) [11], one of the two declared scopes (`video.insights`) does not exist on that platform at all [2], and the trailing-slash rule is a business-api rule that Login Kit does not impose.

### What the demo video would show

TikTok requires "At least one demo video that shows the **complete end-to-end flow** of the up-to-date integrations" and that "All selected products and scopes must be clearly demonstrated in the video" (App Review Guidelines, quoted in BL-724). Here is what would actually appear on screen if the owner deployed BL-723 as it stands and filmed it with a Login Kit app:

1. **Start route: a 503, or nothing at all.** `/api/admin/tiktok-connect/start` refuses with HTTP 503 and a list of missing env names unless all five vars are set. There is no `TIKTOK_BUSINESS_AUTHORIZE_URL` to set, because that value only exists inside a business-api app's portal page. To film anything he would have to paste a Login Kit authorize URL into a variable named for a different platform.
2. **Consent screen: this part would work.** TikTok would render the Login Kit consent screen and the user would approve. The video would look fine for about fifteen seconds.
3. **Callback: a visible HTTP 400 error page, on camera.** The callback posts the returned `code` to `business-api.tiktok.com/open_api/v1.3/tt_user/oauth2/token/` as JSON with a `client_id` and an `auth_code` field. A Login Kit app's `client_key` and `client_secret` are not credentials on that platform. The call cannot succeed. BL-723's own error handling then returns **HTTP 400 with `{"error": "Code exchange failed", ...}`**, which is what the reviewer sees.
4. **The fetch step: never reached.** The video ends at an error.

**So yes: the flow would visibly fail in the demo video, at the exact moment the reviewer is watching for success, and that is very close to a guaranteed rejection.** Worse, it would fail in the way most likely to be read as a broken or non-functional integration, which is one of the documented rejection reasons BL-724 catalogued.

**A second, quieter trap.** Even if the exchange somehow succeeded, the app's ticked scopes must all be demonstrated. `video.insights` is not a scope that exists on `developers.tiktok.com` [2], so it cannot be ticked and cannot be filmed. Any submission that mentions it is describing a product TikTok does not have.

**Conclusion for PART 3: BL-723's code must not be deployed or filmed as-is under a Login Kit app.** It is not "nearly right"; it points at a different platform at every layer. BL-724 was right that the architecture carries over (OAuth state machine, AES-256-GCM token encryption, connection store, refresh logic, disconnect path) and only the client and config need rewriting. That rewrite has not happened yet.

---

## PART 4 — THE HONEST VERDICT AND THE CORRECTED PATH

### The verdict is (c), and it is stated without softening

**(c) The rich analytics are NOT obtainable by this owner in his current form.** As an Individual with no registered company, no company-domain email and no company website registered to a legal entity, he cannot pass step 6 of the API for Business developer registration, because TikTok says "we are unable to onboard personal accounts or individual developers" [10]. Everything downstream (the Accounts API Access Application Form, the app review, the scopes, the endpoint) is behind that door. **This project, as it can be built today, delivers ownership proof plus basic counts. It does not deliver a screen-share replacement.**

**(b) becomes available the moment he has a company, and only then.** It is not exotic: a registered legal entity of any size, an email on the `clipershq.com` domain, and `clipershq.com` itself as the company website (which already satisfies TikTok's "publicly accessible, valid, functioning, fully developed and professionally presented" wording [10]). What it costs is company registration in his jurisdiction, then three business days for the developer profile, then the Accounts API Access Application Form with no published timeline, then two to three business days for the app. **UNVERIFIED:** whether TikTok would accept a newly-registered one-person company. What would settle it: registering and applying.

**(a) is false.** One Login Kit app does not give everything needed. It gives views, likes, comments, shares, duration, follower count and, crucially, verified account ownership. It gives zero of the eight fields the owner named as his reason for doing this.

### Has the owner been misled? Yes, in part, and by this line of rounds

Stated plainly, because he is about to spend money and a submission on it:

• **BL-722 (mine) got the fields right and missed the gate.** It quoted the API for Business docs correctly and gave a seven-step owner checklist beginning "create a TikTok for Business account, register as a developer". It fetched TikTok's Register-as-a-developer page and **did not read past the rate-limit section of the same download**, so the sentence "we are unable to onboard personal accounts or individual developers" was in the material BL-722 pulled and never surfaced. That is the single most consequential sentence in the entire project and it sat unread. **BL-722's PART 7 plan is wrong at step 2 for this owner** and should be treated as superseded by this document.
• **BL-723 (mine) built against a platform the owner cannot register for.** The build itself is sound and its architecture is reusable, but its target was chosen on BL-722's unchecked premise.
• **BL-724 was not wrong, and should not be blamed for this.** Its own table already listed `reach`, `full_video_watched_rate`, `total_time_watched`, `average_time_watched`, `impression_sources` and `audience_countries` as things "the second app would buy you", and it correctly identified the two platforms as genuinely separate. Its headline "One app or two? **ONE. Definitively.**" answered the narrower question "what should you submit this week", and read alone it obscures the broader one. **The correct reading of BL-724 is: one app to submit now, two platforms in reality, and the second platform is where the analytics live.**

### The corrected ordered plan, from where he actually is

**Step 1. Decide the question that governs everything else: is there a company, or will there be one?** This is not an engineering question and no round can answer it for him. Everything below forks on it.

**Step 2, on the no-company branch, and this is the honest default. Repoint BL-723 at the Display API and ship what it CAN do, described accurately.**
What that product actually is, said without inflation: **a verified-ownership and verified-counts feature.** The clipper signs in with TikTok once; from then on the platform knows, from TikTok itself rather than from a scraper, that this account belongs to this clipper, that this specific post exists, exactly when it was posted (`create_time`, real-time), and what its view count is (`view_count`). Concretely that is worth three real things this platform is currently paying for in other ways:
• It replaces the bio-code verification cascade, which R-5 measured producing **326 NEEDS_ADMIN escalations from 114 distinct clippers in 30 days**, TikTok worst at 212 with no tier-2 fallback. An OAuth grant is strictly better ownership proof than a code in a bio.
• It gives a first-party view count to check LamaTok against.
• It proves post time first-party, which is what the 30-minute freshness rule actually rests on.
**It does not replace a screen-share call, and the owner should stop expecting it to until step 4.**
Engineering: rewrite `client.ts` and `config.ts` only. Host becomes `open.tiktokapis.com`, auth becomes `Authorization: Bearer`, token endpoint becomes `POST /v2/oauth/token/` form-encoded with `client_key` and `code` [11], scopes become `user.info.basic` and `video.list` [2], and `video.insights` is deleted. Token lifetimes even match what BL-723 already assumes: access token "valid for 24 hours", refresh token "valid for 365 days", and "The returned `refresh_token` may be different than the one passed in the payload. You must use the newly-returned token" [11]. Rate limit is **600 requests per minute** on `/v2/video/list/` and on `/v2/user/info/` [14], which is far more than 305 TikTok accounts need. The OAuth state machine, the AES-256-GCM token store, the connection table, the refresh job and the disconnect path all survive untouched.

**Step 3. Only then film the demo and submit the Login Kit app**, following BL-724's checklist. **Do not film against the current BL-723 code.** The demo must show the rewritten Display API flow completing successfully, and the app must tick only `user.info.basic` and `video.list`, because every ticked scope must appear on screen.

**Step 4, on the company branch, and only after step 3 is live and approved.** Register the company. Then, in this order: a TikTok For Business account, the developer registration with the company email and `clipershq.com` as the company website (three business days), the Accounts API Access Application Form describing the use as **payout verification of a creator's own submitted post** and never as creator discovery or ranking, then the developer app with the "TikTok Accounts" permission and scopes `video.list` and `video.insights` (two to three business days). **BL-723's existing code becomes correct again at that point, unchanged**, which is the one silver lining: it is not wasted work, it is early work.

**Step 5. Where it stops.** If the company does not exist, step 4 never starts and the screen-share call stays manual. That is not a failure of the build, it is a fact about who TikTok will do business with, and it should be planned around rather than repeatedly rediscovered.

**One thing to say out loud about the other two platforms.** BL-722 ranked YouTube first on value per unit of effort, and YouTube's audience-retention curve and viewer demographics need **no company, no business registration and no account-type conversion from the clipper**: a channel owner authorizes with a standard Google OAuth consent [BL-722 PART 3]. **If the goal is genuinely to stop doing screen-share calls, YouTube is the platform where that goal is reachable by this owner today, and TikTok is the one where it is not.** That inversion is the most useful thing in this document after the registration sentence itself.

---

## Sources

| # | Page | URL |
|---|---|---|
| 1 | Video Object (the complete Display API field set) | https://developers.tiktok.com/doc/tiktok-api-v2-video-object |
| 2 | TikTok API scopes (every scope the platform issues) | https://developers.tiktok.com/doc/tiktok-api-scopes |
| 3 | Get User Info (Display API user fields and their scopes) | https://developers.tiktok.com/doc/tiktok-api-v2-get-user-info |
| 4 | Accounts API Authorization (prerequisites, portal, authorize URL) | https://business-api.tiktok.com/portal/docs?id=1738083939371009 |
| 5 | Get post data of a TikTok account (`/business/video/list/`) | https://business-api.tiktok.com/portal/docs?id=1762228421622786 |
| 6 | Get profile data of a TikTok account (`/business/get/`) | https://business-api.tiktok.com/portal/docs?id=1762228399168514 |
| 7 | Data Portability data types | https://developers.tiktok.com/doc/data-portability-data-types |
| 8 | Data Portability API, applying | https://developers.tiktok.com/doc/data-portability-api-get-started |
| 9 | Research Tools access and eligibility | https://developers.tiktok.com/products/research-api/ |
| 10 | **Register as a developer (API for Business)** | https://business-api.tiktok.com/portal/docs?id=1738855176671234 |
| 11 | User access token management (Login Kit) | https://developers.tiktok.com/doc/oauth-user-access-token-management |
| 12 | Create a developer app (API for Business) | https://business-api.tiktok.com/portal/docs?id=1738855242728450 |
| 13 | Accounts API overview (use cases, prohibited uses, access form) | https://business-api.tiktok.com/portal/docs?id=1737944384433218 |
| 14 | Rate limits (Display API v2) | https://developers.tiktok.com/doc/tiktok-api-v2-rate-limit |
| 15 | List Videos (`/v2/video/list/`) | https://developers.tiktok.com/doc/tiktok-api-v2-video-list |

**A note on how the `business-api.tiktok.com` pages were read**, because it matters for whether these citations can be checked. That portal is a JavaScript single-page app and returns only a `<title>` to a plain fetch, which is why earlier rounds of this project were tempted toward third-party summaries. Its raw markdown is served by a public unauthenticated endpoint, `business-api.tiktok.com/gateway/api/doc/client/node/get/v2/` with `identify_key`, `doc_id` and `language=ENGLISH`, and every business-api quote above was read from that source rather than from any secondary write-up. The `doc_id` values are the `id=` numbers in the URLs in the table.

---

## What is UNVERIFIED, and exactly what would settle each

| Claim | Status | What settles it |
|---|---|---|
| Whether a newly-registered one-person company would be accepted by API for Business developer registration | **UNVERIFIED** | Registering the company and applying |
| Whether advertiser status or ad spend is a de-facto requirement beyond the documented company requirement | **UNVERIFIED** (not documented as a prerequisite; the user types are all company types) | Applying as Technology Company with no ad spend |
| How long the Accounts API Access Application Form takes | **UNVERIFIED** (TikTok publishes no timeline) | Submitting one |
| Whether the prohibited-use clause on affiliate influencer marketing programs would be applied to this use case | **UNVERIFIED** (a human judgement on the form) | Submitting the form with the payout-verification framing |
| Whether the Data Portability full archive contains anything analytics-like beyond the documented Posts fields | **UNVERIFIED for the `all_data` category**; documented ABSENT for Posts and Activity | Reading a real export, which needs an approved Data Portability app |

---

## Safety and disclosure

READ ONLY. One document on branch `checkpoint/BL-726` from `origin/main` `de0169bd`. **No code, config, schema or data change. Nothing registered, nothing submitted, no credential created or stored.** Zero calls were made to any TikTok data API; the only network traffic was fetches of public documentation pages and of three prior reports from `ilenader/clippershq-reports`. No database query was run this round, so no timestamp cast was needed and none is claimed. The 6 money files, `tracking.ts` and `campaign-era.ts` are untouched: this diff contains exactly one markdown file. Isolated worktree at the short path `C:/b726`, `node_modules` never junctioned, no `.env` copied in because nothing needed to run. Nothing a live round holds was touched (BL-725 was not read, written or referenced, and the `main` working tree, held by worktree `C:/b575`, was never checked out). A markdown-only diff cannot change tsc or build, so no build was run and none is claimed. Every capability claim cites TikTok's own documentation with a URL; no blog post or third-party SDK doc was used for any capability claim. No dashes as bullets.

**Rollback:** delete branch `checkpoint/BL-726`. It contains one document and touches nothing.
