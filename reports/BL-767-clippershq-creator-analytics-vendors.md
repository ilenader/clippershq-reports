# BL-767 — which creator-consented TikTok analytics service actually delivers, and what it costs

**2026-08-10 · RESEARCH ONLY. READ ONLY on the codebase.**
No code, config, schema or data changed. **Nothing was signed up for, no free tier was used, no payment
details were entered anywhere, no credential was stored, and no TikTok account was authorized.** Base
`origin/main` @ `9d285c8c`, isolated worktree `C:/m767`, removed at exit, `node_modules` never
junctioned. A markdown-only diff cannot change tsc or build, so neither was run and neither is claimed.

Six vendors were researched in parallel, one dedicated agent each, plus a seventh on how the owner's
peer could have built this. **All six vendor investigations completed.** Every claim below is cited to
the vendor's own site, documentation or machine-readable API specification. No competitor blog, no
listicle and no search-engine summary was used as evidence for any capability claim, and one such
summary that contradicted a vendor's own page was caught and discarded.

---

# CORRECTION, ADDED AFTER FIRST PUBLICATION — THE ANSWER CHANGED

**The verdict below was published, and then a seventh line of research returned and overturned it. The
original text is left intact underneath so the reasoning can be audited; this block supersedes it.**

**The question was framed wrongly, by the brief and by me. It asked which of six named vendors could
front a creator's analytics. The right question was who already holds TikTok API for Business
approval, because that approval binds the APP DEVELOPER, not the end customer.** An individual with no
company cannot register for the Business API, which BL-726 proved and this round re-proved. **But an
individual can OAuth a creator into a vendor that already holds that approval, and receive the full
insights set.** None of the six named candidates is such a vendor. **Ayrshare is.**

**Verified directly from Ayrshare's own API documentation, not from the agent's summary and not from
any blog** ([analytics/post](https://www.ayrshare.com/docs/apis/analytics/post)). Documented as
returned for TikTok:

| The owner's wish list | Ayrshare field | Status |
|---|---|---|
| Average watch time | `averageTimeWatched` | **DOCUMENTED** |
| Full-video watched rate | `fullVideoWatchedRate` | **DOCUMENTED** |
| **Retention curve** | **`videoViewRetention`**, array of second/percentage | **DOCUMENTED** |
| Traffic / impression sources | `impressionSources` | **DOCUMENTED** |
| Reach | `reach` | **DOCUMENTED** |
| Audience countries | `audienceCountries` | **DOCUMENTED** |
| Audience gender | `audienceGenders` | **DOCUMENTED** |
| Total watch time | — | **not listed** |
| Audience age | — | **not listed** |
| Profile views | — | **not listed** |

**That is seven of ten, including every one of the four this report had called flatly unobtainable, and
including the retention curve itself.** Prerequisites, in Ayrshare's own words: the creator must
publish at least one video, **tap "Turn On" on the Analytics page of their TikTok mobile app**, and
have **100 followers** for the extra viewer insights. Fields appear **24 to 48 hours after posting**.

**And the consent problem dissolves.** Ayrshare is an approved TikTok API for Business partner, so
authorization runs through TikTok's official OAuth: a scoped token, revocable by the clipper from
TikTok's own settings, **no session cookie, no password, and no terms-of-service exposure.** The flow
is a JWT-generated linking URL the clipper opens, then links their account
([JWT docs](https://www.ayrshare.com/docs/apis/profiles/generate-jwt)). **This is the one thing this
report said no vendor offered, and it is the reason everything below is superseded.**

**Pricing** ([pricing](https://www.ayrshare.com/pricing/)): Premium $149/mo (1 profile), **Launch
$299/mo (10 profiles, 28-day free trial, no credit card)**, Business $599/mo (30 profiles, scaling to
300 at $8.99 per extra profile for 31 to 100, declining to $1.99 at 500+), Enterprise above 300.
**For the 43 clippers who actually post TikTok clips: roughly $716/month** (Business plus 13 extra
profiles). Far dearer than TikHub's $9.60, and legitimate rather than credential-harvesting.

**REVISED VERDICT: test Ayrshare on its free 28-day Launch trial before doing anything else.** It is
the only route found that returns the retention curve, needs no company, and asks the clipper for
nothing beyond a genuine TikTok OAuth approval. **Do not adopt TikAPI or TikHub. Do not build anything
until the trial returns real fields for one real clip.**

**What is still UNVERIFIED and matters:** that the final authorization screen is TikTok's own rather
than an Ayrshare-hosted one (strongly implied by the Business API partnership, not directly observed);
whether Ayrshare requires the CUSTOMER to be a registered company (its pricing page does not say); and
whether the **"Turn On" step in each clipper's TikTok app** is a fatal adoption obstacle, since it
cannot be done for them and most will not know it exists. **The 100-follower threshold will also
exclude some clippers outright.**

**Everything in PART 6 about scale still stands and still constrains this.** TikTok remains 18.6% of
clip volume from 43 active clippers. **Ayrshare changes what is technically obtainable. It does not
change that seven clips in ten are Instagram and YouTube**, where the screen-share call remains.

---

## THE ORIGINAL ANSWER, NOW SUPERSEDED

> **Do not build this. None of the six delivers what the owner asked for, and the two that come closest
> both require his clippers to hand a third party a live TikTok session credential.**
>
> **Average watch time, total watch time, the retention curve, traffic sources, reach and profile views
> are not obtainable for a clipper's VIDEOS from any of the six.** That is the third consecutive round
> to reach a negative answer on this question, and it is now settled from vendor API specifications
> rather than from marketing pages.
>
> Three vendors are pure scrapers returning **exactly the public counts LamaTok already gives free**.
> A fourth, Phyllo, **explicitly switches audience data OFF for TikTok in its own API spec** while
> leaving it on for Instagram. The two that return real creator-panel data do so only partially:
> **TikHub** has completion rate and audience age/gender/country for **TikTok Shop accounts only, via a
> pasted session cookie**; **TikAPI** has watch time, audience demographics and traffic sources **for
> LIVE STREAMS only**, with the video-level equivalent completely undocumented.
>
> **TikAPI is also capped at 100 connected TikTok accounts on its top public tier.** The owner needs
> ~300. That alone puts him in unpriced Enterprise territory.
>
> **And the prize is smaller than assumed.** Measured live this round: **TikTok is 18.6% of clip
> volume** (320 of 1,722 clips in 30 days) from **43 active clippers**. Instagram is 69.7%. Even a
> perfect TikTok integration leaves the screen-share call in place for seven clips in ten.

---

## PART 1 — THE FIELD MATRIX

**The baseline that makes a vendor worthless.** Read from `lamatok.ts` on current main, the owner
already gets, free: `play_count`, `digg_count`, `comment_count`, `share_count`, `create_time`.

**The target.** BL-726 established these live only on `business-api.tiktok.com`: `video_view_retention`
(array of `{second, percentage}`), `audience_countries`, `audience_genders`, `audience_activity`,
`audience_types`, under scopes `video.insights` / `user.insights`.

**I re-verified TikTok's own position from primary sources rather than inheriting it:**

* [TikTok API scopes](https://developers.tiktok.com/doc/tiktok-api-scopes/) — the complete issued scope
  list is `local.*`, `portability.*`, `research.*`, `user.info.basic`, `user.info.profile`,
  `user.info.stats`, `video.list`, `video.publish`, `video.upload`. **No analytics scope, no insights
  scope, nothing resembling `video.insights`.**
* [Video Object](https://developers.tiktok.com/doc/tiktok-api-v2-video-object/) — exactly **15**
  queryable fields, ending at `like_count`, `comment_count`, `share_count`, `view_count`. **No
  sixteenth.**

BL-726 confirmed twice, independently. Now the vendors, for a clipper's VIDEOS.

| Metric | TikHub | TikAPI | Phyllo | ScrapeCreators | SociaVault | EnsembleData |
|---|---|---|---|---|---|---|
| Views | ✅ `vv_cnt` | ✅ `vv_history[]` | ✅ `engagement.view_count` | ✅ `play_count` | ✅ `play_count` | ✅ `play_count` |
| Likes | ✅ `like_cnt` | ✅ `like_history[]` | ✅ `like_count` | ✅ `digg_count` | ✅ `digg_count` | ✅ `digg_count` |
| Comments | ✅ `comment_cnt` | ✅ `comment_history[]` | ✅ `comment_count` | ✅ `comment_count` | ✅ `comment_count` | ✅ `comment_count` |
| Shares | ✅ `share_cnt` | ✅ `share_history[]` | ⚠️ `share_count` null in every example | ✅ `share_count` | ✅ `share_count` | ✅ `share_count` |
| Follower count | ✅ `follower_count` | ✅ `follower_num` | ✅ `reputation.follower_count` | ✅ `followerCount` | ✅ `followerCount` | ✅ `followerCount` |
| Post timestamp | ✅ `publish_time` | ✅ `createTime` | ✅ `published_at` | ✅ `create_time` | ✅ `create_time` | ✅ `create_time` |
| **Full-video watched rate** | ✅ **`video_completion_rate`** | ⚠️ `video_finish_rate_history_7d` **null in vendor's own example** | ABSENT | ABSENT | ABSENT | ABSENT |
| **Audience countries** | ✅ **`follower_regions`** | LIVE ONLY | **ABSENT, switched off** | ⚠️ `audienceLocations[]` | ⚠️ `audienceLocations[]` | ABSENT |
| **Audience gender** | ✅ **`follower_genders`** | LIVE ONLY | **ABSENT, switched off** | ABSENT | ABSENT | ABSENT |
| **Audience age** | ✅ **`follower_ages`** | LIVE ONLY | **ABSENT, switched off** | ABSENT | ABSENT | ABSENT |
| **Average watch time** | **ABSENT** | LIVE ONLY | ABSENT | ABSENT | ABSENT | ABSENT |
| **Total watch time** | **ABSENT** | LIVE ONLY | ⚠️ `watch_time_in_hours` null for TikTok | ABSENT | ABSENT | ABSENT |
| **Retention curve** | **ABSENT** | **ABSENT** | ABSENT | ABSENT | ABSENT | ABSENT |
| **Traffic / impression sources** | **ABSENT** | LIVE ONLY | ABSENT | ABSENT | ABSENT | ABSENT |
| **Reach** | **ABSENT** | **ABSENT** | UNVERIFIED, no TikTok example | ABSENT | ABSENT | ABSENT |
| **Profile views** | **ABSENT** | ⚠️ `pv_history[]`, undocumented | ABSENT for TikTok | ABSENT | ABSENT | ABSENT |

Sources: TikHub [openapi.json](https://api.tikhub.io/openapi.json), [Creator API](https://api.tikhub.io/#/TikTok-Creator-API) · TikAPI [documentation](https://tikapi.io/documentation/#tag/Profile/operation/user.analytics), [live analytics](https://tikapi.io/documentation/#tag/Live/operation/user.live.analytics) · Phyllo [OpenAPI spec](https://docs.getphyllo.com/api/v1/projects/tryphyllo/api-reference/nodes/reference/openapi.v1.yml), rendered at [API reference](https://docs.getphyllo.com/docs/api-reference/api/ref) · ScrapeCreators [video](https://docs.scrapecreators.com/v2/tiktok/video/), [audience](https://docs.scrapecreators.com/v1/tiktok/user/audience/) · SociaVault [videos](https://docs.sociavault.com/api-reference/tiktok/videos), [demographics](https://docs.sociavault.com/api-reference/tiktok/demographics) · EnsembleData [API docs](https://ensembledata.com/apis/docs).

### The group split, stated plainly

**GROUP A, only public counts LamaTok already gives free. Worthless here however cheap:**
**EnsembleData, SociaVault, ScrapeCreators, and Phyllo.**

Not impressionistic. EnsembleData's complete 9.77 MB API reference searched end-to-end: `watch_time`
**0** occurrences, `retention` **0**, `traffic_source` **0**, `impression_source` **0**,
`profile_view` **0**, `demograph` **0**. ScrapeCreators' [llms.txt](https://docs.scrapecreators.com/llms.txt)
index: **zero** matches for insights, analytics, watch time, retention, impression, reach, profile
views across the whole catalogue.

**GROUP B, partial genuine creator-panel data: TikHub and TikAPI.** Neither covers the owner's actual
list for videos, and both cost a session credential.

### Phyllo is the most instructive result in the report

Phyllo's documentation is a client-side SPA that returns only page titles to a fetcher, **which is very
likely how earlier rounds produced confident wrong answers by falling back on its marketing pages.**
Pulling the raw machine-readable spec (824 KB, 21,163 lines) settles it:

In the documented `GET /v1/work-platforms` response, **TikTok** carries:

```
identity:   {is_supported: true,  audience: {is_supported: false}}
engagement: {is_supported: true,  audience: {is_supported: false}}
```

while **Instagram** in the same list carries `identity.audience.is_supported: true`. **Phyllo's
audience-demographics product is real, and TikTok is explicitly excluded from it.** That is the
"exists but not for TikTok" case, proven from the vendor's own spec.

Where do the TikTok demographics in Phyllo's marketing come from? A **different product**:
`POST /v1/social/creators/profiles/analytics`, whose own description reads *"Get analytics for
creator's profile using publicly available data based on their username or link."* It sits under the
Creator Discovery tag, needs no creator consent, and is inference over public data. **It is not the
creator's panel.**

And `watch_time_in_hours` does exist on the generic engagement object, but is populated only in the
**YouTube** example and is `null` in the TikTok one. A grep of all 21,163 lines for
`watch_time|average_view|view_duration|retention|full_video|impression|traffic_source|reach|profile_view`
finds **no average watch time, no full-video-watched rate and no retention curve for any platform at
all.**

**The contradiction I set out to resolve is resolved: the marketing overstates the API reference, and
the demographics are public inference. There is no evidence Phyllo resells TikTok API for Business
analytics.** Its "official TikTok partner" claim is UNVERIFIED as to what access it actually confers.

### Two traps that would have produced a wrong recommendation

**ScrapeCreators sells a "Get Age and Gender" endpoint**, described verbatim as *"Detect age and gender
of a creator using AI analysis of profile image."* That is **the creator's own** age and gender guessed
from their profile picture, not audience demographics. Name-matching would have marked two cells
AVAILABLE that are ABSENT.

**SociaVault's "demographics" endpoint is inference.** Its own blog concedes: *"TikTok's native
analytics are only available to account owners. SociaVault provides third-party demographic analysis
for any public profile"* ([source](https://sociavault.com/blog/tiktok-demographics-api)). A
search-engine summary encountered during research claimed the opposite, that it *"pulls from TikTok's
own analytics… as accurate as what the creator sees in their own dashboard."* **Contradicted by the
vendor's own page and discarded.** That is precisely the class of source that produced the earlier
wrong answers.

**Reconciliation note.** ScrapeCreators and SociaVault expose `audienceLocations[]` with identical
fields (`country`, `countryCode`, `count`, `percentage`) at an identical **26 credits**, and neither
documents provenance. Two vendors shipping a byte-identical schema at an identical price strongly
suggests one shared upstream. **That is inference, marked UNVERIFIED**, but the owner should not treat
them as corroborating each other.

---

## PART 2 — THE CONSENT MODEL

| Service | What the clipper does | One-time? | Genuine TikTok screen? |
|---|---|---|---|
| **EnsembleData** | **Nothing.** *"You don't need a TikTok account to use our API"* | n/a | **No consent model at all** |
| **ScrapeCreators** | **Nothing.** Vendor API key, pass a handle | n/a | **No consent model at all** |
| **SociaVault** | **Nothing.** `X-API-Key`, bare `handle` | n/a | **No consent model at all** |
| **TikHub** | **Pastes their live TikTok session cookie** | Until logout or expiry | **NO. No screen at all. Raw credential handover** |
| **TikAPI** | Lands on a **TikAPI-hosted** page, ticks TikAPI's ToS, **scans a QR in the real TikTok app**, approves a TikAPI-hosted scope list | One-time per account; videos automatic. Expires if the TikTok session dies or after **1 month of inactivity** | **NO, but no password or cookie is ever typed.** Approval happens inside the genuine TikTok app |
| **Phyllo** | Phyllo-hosted Connect SDK screen; `tokenExpired` callback exists so reconnection is required | Not permanent | **UNVERIFIED** |

### The trust question, answered without softening

**Three of the six have no consent model at all**, which is architecturally decisive rather than
convenient: a scraper sees only what a logged-out visitor sees, and a creator's analytics panel is
never rendered logged-out. **Consent buys nothing from them because there is no channel through which
consent could unlock anything.**

**TikHub works by pure credential capture.** In its own words on
[tikhub.io/tiktok-api](https://tikhub.io/tiktok-api): *"Creator API endpoints are POST and require the
creator account's own login cookie"*, and it markets the missing safeguard as a feature, *"with no app
review and **no OAuth flow**"*. A scan of its 985-endpoint spec returns **zero** occurrences of
`oauth`, `open.tiktokapis` or `developers.tiktok`. Its endpoints also accept a `proxy` parameter, so
requests are replayed from infrastructure the clipper never sees.

**TikAPI is meaningfully better on flow and identical on outcome, and this distinction matters.**
Its `authorizationUrl` is `https://tikapi.io/account/authorize` — TikAPI's domain, and it says so:
*"TikAPI is using a custom implementation of OAuth 2.0 specification."* The page is headed **"Login
with TikAPI"**. But the actual approval is a **QR code scanned and confirmed inside the creator's real
TikTok app**, so **no password and no cookie is ever typed into a TikAPI form**. That is a genuinely
safer user experience than TikHub's paste-your-cookie.

**The end state is nevertheless the same class of secret**, and TikAPI states it plainly in its own
[privacy policy](https://tikapi.io/privacy): *"When an account is logged in for the first time on our
OAuth platform: basic profile information and **the account's session cookies** are securely stored on
our database."* So a third party holds a full TikTok account session, and the `view_analytics` scope
the clipper approves is **enforced by TikAPI, not by TikTok**. A clipper granting "view analytics" is
trusting TikAPI's own gate. There is no TikTok-side scope, no TikTok-side revocation, and no audit
trail on TikTok's side.

**In plain terms: a TikTok session cookie is not a scoped analytics token. It is a bearer credential
for the whole account** — post, delete, DM, change settings. Some clippers will refuse, and they will
be right to. **ClippersHQ would be the party asking.**

---

## PART 3 — PRICING, AND THE OWNER'S ACTUAL BILL

### The assumptions, corrected against live data

Measured at `2026-08-10 21:28 UTC`:

| Assumption in the brief | Measured reality |
|---|---|
| ~1,240 clippers | **1,322** CLIPPER accounts |
| ~2,300 clips/month | **1,722** clips in the last 30 days |
| (not stated) | **Only 320 are TikTok — 18.6%.** Instagram 1,201 (69.7%), YouTube 201 (11.7%) |
| ~300 connect | **271 clippers hold an approved TikTok account; only 43 posted a TikTok clip in 30 days** |
| 10-minute tick | 144 ticks/day, 4,320/month; 4,168 active tracking jobs across all platforms |

**300 connections is close to the ceiling, not a conservative estimate.**

### The pricing models

| Service | Model | Rate | Free tier without a card |
|---|---|---|---|
| **TikAPI** | **Flat monthly tier**, gated on requests/day **and connected-account count** and bandwidth | Starter **$29** (300 req/day, **5 accounts**), Pro **$79** (2,000/day, **30 accounts**), Business **$189** (10,000/day, **100 accounts**). Extra bandwidth $12 to $15/GB | **No free tier.** 5-day Starter trial; card requirement **UNVERIFIED** |
| **TikHub** | Pay per request | Creator endpoints **$0.001 flat, `allow_discount: 0`** → **$1.00/1k** | **Yes**, ~50 requests, email only |
| **ScrapeCreators** | Credit packs, never expire | $1.88/1k (Freelance $47) or $0.99/1k (Business $497). **Audience endpoint 26 credits → $48.88/1k or $25.74/1k** | **Yes**, 100 credits, "no credit card required" |
| **SociaVault** | One-time credit packs | $0.0048 to $0.0020/credit. **Demographics 26 credits** | **Yes**, 50 credits, no card |
| **EnsembleData** | Daily unit allowance, monthly | Wood $100/mo to Platinum $1,400/mo. TikTok post info 2 units → ~$1.87 to $2.67/1k | **Yes**, 50 units/day, no card |
| **Phyllo** | **Quote only, gated behind sales.** [Pricing page](https://www.getphyllo.com/pricing) publishes no figures | none published | **None.** "Company Name" is a **required field** on the only route to pricing |

### Per account, per video, or per refresh?

**Per refresh**, and that is the expensive answer. TikHub states explicitly that *"every request returns
fresh, real-time data and is billed independently, even with identical parameters."* ScrapeCreators is
the exception, offering free cache hits. TikAPI is different again: it bills a **flat tier**, so
refresh frequency is capped by requests/day rather than metered.

**Refreshing every TikTok clip on every 10-minute tick would be ruinous:**

```
320 TikTok clips x 4,320 ticks/month = 1,382,400 calls/month
TikHub at $1.00/1k                   = $1,382 / month
TikAPI                                = 46,080 req/day, 4.6x over the top tier's 10,000/day cap
```

**$1,382/month is roughly 46% of a whole campaign budget spent on analytics refreshes**, and it breaks
TikAPI's plan limits outright.

### The sane cadence, and the real bill

**Retention, completion rate and audience demographics are daily-granularity data. They do not move
minute to minute and TikTok does not update them faster.** A once-daily refresh loses nothing.

```
320 TikTok clips x 30 days = 9,600 calls/month  =  320 requests/day
```

| Service | Once-daily bill | Blocking constraint |
|---|---|---|
| **TikHub** | **$9.60/month** | Shop accounts only; session cookie |
| **TikAPI** | **$79/month** (Pro, 2,000 req/day covers 320) | **Account cap: Pro allows 30, Business 100. Owner needs ~300 → Enterprise, unpriced** |
| ScrapeCreators (audience, 300 accounts daily) | ~$233 to $440/month | Buys audience countries only |
| SociaVault (demographics, 300 accounts daily) | ~$468 to $621/month | Same one field, dearer |
| EnsembleData | ~$100/month | Buys nothing he lacks |
| Phyllo | Unknown | Company required to obtain a quote |

**Ranked on cost for data he does not already have:** TikHub $9.60, TikAPI $79 plus an Enterprise
negotiation, then a steep cliff to $233 to $621 for a single field of unverified provenance.

**Cost is not the obstacle. TikHub is astonishingly cheap and TikAPI is affordable. The obstacles are
the session credential, the account cap and the missing fields.**

### The TikAPI account cap, which is decisive and easy to miss

Every TikAPI tier's marketing bullet reads **"Unlimited OAuth Users"**, yet the same public JSON record
behind that page carries `tiktok_account_limit: 5 / 30 / 100`, and the customer dashboard code
references `extra_tiktok_accounts_fee`. **Connected accounts are capped and overage-billed, not
unlimited.** The owner needs roughly 300. **The top public tier allows 100.** The overage rate is not
published, so **his real TikAPI cost is unknown and requires a sales conversation** — the same barrier
Phyllo has, arrived at from a different direction.

---

## PART 4 — THE LIVE TEST, AND WHY IT WAS NOT RUN

**No free tier was used and nothing was signed up for.** Four vendors offer genuine email-only, no-card
free tiers: TikHub (~50 requests plus $0.05 credit), ScrapeCreators (100 credits), SociaVault (50
credits), EnsembleData (50 units/day). TikAPI offers only a 5-day Starter trial that redirects to
Stripe. Phyllo publishes nothing.

**The test that would settle the remaining question cannot be run without committing the error under
investigation.** The free tiers only expose public endpoints, which are not in doubt. The endpoints
that matter — TikHub's `get_video_detailed_stats` and `get_video_audience_stats`, TikAPI's
`/creator/analytics/video` and `/creator/analytics/followers` — **all require a live TikTok session**,
obtained either by pasting a cookie or by authorizing a real account. Both were explicitly forbidden,
and both are the exact risk PART 5 describes. **A test that requires doing the thing the report advises
against is not a test worth running.**

So, stated honestly: **all field-level findings rest on vendor documentation, and for EnsembleData,
TikHub and Phyllo on their complete machine-readable API specifications.** Absence is strongly
evidenced by exhaustive search of those specs. It is documentary, not empirical, and is labelled so.

**A finding about what can be known before paying:** four vendors publish complete field-level docs and
free credits, so a buyer can verify nearly everything for $0. **Phyllo publishes no pricing at all and
requires a company name to request it.** TikAPI publishes tiers but hides the overage rate that would
actually govern the owner's bill. **For an individual with no company, two of the six cannot be costed
before committing to a sales conversation.**

---

## PART 5 — THE RISKS, NOT SOFTENED

**1. Could a clipper's account be suspended? Yes, and ClippersHQ would be the party that asked.**
Both viable vendors end up holding a live TikTok session replayed from third-party infrastructure,
which is exactly the pattern platform anti-abuse systems exist to detect. **Neither vendor makes any
statement that connecting is safe.** TikAPI's ToS says only that it *"has endeavoured to ensure our
products and services adhere as closely as possible"* to TikTok's terms — an effort statement, not a
compliance claim — and its legality article addresses **scraping** legality, not creator account
safety. TikHub warns its own Shop endpoints *"can be briefly unstable and usually recover within 2–3
hours"*, the signature of a cat-and-mouse relationship. ScrapeCreators calls TikTok enforcement *"The
Wild Card"*, *"inconsistent"*.

**The realistic worst case is not that the data stops. It is that a clipper loses the account their
income depends on, because ClippersHQ told them to connect it.** No data quality justifies that.

**2. Silent breakage is near-certain, and this project has been burned twice.** HikerAPI and LamaTok
paths both broke silently before. Every vendor here is unofficial, with no contractual data rights and
no SLA recourse. TikHub already carries deprecation notices retiring Shop endpoint series. **Any
integration must fail loudly and must never become a payment dependency; LamaTok stays the source of
truth for money.**

**3. Terms of service: the risk is contractually pushed onto the owner.** ScrapeCreators: *"You are
solely responsible for ensuring your use of the Service complies with the terms, policies, and laws
applicable to the websites you access"*, liability capped at 12 months of fees. EnsembleData is
Singapore-governed with an indemnification obligation on the buyer. TikAPI: *"TikAPI is an unofficial
API, it is in no way endorsed or affiliated to the TikTok or ByteDance."* **Every one of them has
written its terms so that if TikTok objects, it is the owner's problem.**

**4. Data residency and the privacy policy.** Clipper analytics and, for both viable vendors, **session
credentials** would leave the platform's infrastructure. TikHub is China-oriented: its spec ships a
mainland mirror because *"api.tikhub.io 在中国大陆被长城防火墙拦截"*, docs are Chinese-first, Alipay is a
headline payment method, **no legal entity or country is stated anywhere reachable, and its ToS and
privacy policy are JavaScript shells returning no readable text.** BL-724 already had to correct this
platform's privacy policy once for naming providers that were no longer true. **A policy naming a
vendor whose own terms cannot be read is not one the owner should sign his clippers up to.**

**5. Vendor durability is poor across the board.** TikAPI is the strongest, founded 2021, but presents a
single named founder and publishes no headcount. SociaVault is a ~13-month-old Delaware C-Corp at a
mail-forwarding address **with no changelog entry since 2026-02-23**, six months of silence for a
product that decays as TikTok changes. ScrapeCreators is "Web Scraping Guy LLC", a self-described
*"small global team"*. EnsembleData is a 2–10 person unfunded Singapore company. TikHub names no entity
at all. **Routing 1,240 clippers through any of these routes them through an operation that may not
exist in a year.**

---

## PART 6 — WHAT IT WOULD REPLACE, AND WHAT IT WOULD NOT

### What it could replace, if adoption were high

* **The screenshot reader (BL-650).** Genuinely redundant for connected TikTok accounts. It is already
  inert, its OCR key unset, and its image-to-text accuracy **UNMEASURED** by BL-650's own admission.
  Real API fields beat OCR of a screenshot. **But only for TikTok, and only for connected clippers.**
* **Manual screen-share calls, partially.** TikHub's completion rate and audience splits are real
  evidence. **But the owner opens those calls to see retention and traffic sources, and for videos
  neither is obtainable from any vendor.** The call gets shorter, not eliminated.
* **BL-599's peer-relative bot rank, partially.** It fires at 3.2% and infers from public
  like-to-view ratios; real audience demographics would be stronger. **But BL-599 covers every platform
  and every clipper, so it stays.**
* **Part of the reviewer note layer**, where notes record numbers read off a screenshot.

### What it does not replace, which is most of it

**TikTok is 18.6% of clip volume.** Instagram is 69.7%, YouTube 11.7%. HikerAPI and LamaTok carry all
of it and must continue to. **This is additive, permanently, unless the platform mix changes.**

### The adoption arithmetic

* **43 clippers** posted a TikTok clip in 30 days. **271** hold an approved TikTok account.
* At 300 connections covering the 43 active TikTok posters, the ceiling is **18.6% of clips**.
* **Below roughly 50% adoption among active TikTok posters this is a side channel**: fewer than 22
  clippers, under 10% of clips, and a screen-share for everyone else.
* **It becomes transformative only if TikTok grows to a majority of volume AND adoption exceeds ~70%.**
  Neither is true and neither is close.

**Even a perfect integration leaves the owner doing exactly what he does now for seven clips in ten.**
That, more than the pricing, is the argument against building this at all.

---

## PART 7 — THE VERDICT AND THE PLAN

> ## **Use none of them, and do not ask clippers to connect a TikTok account through any third party. For a clipper's VIDEOS, average watch time, retention, traffic sources, reach and profile views are not obtainable from any of the six, and the two vendors that return partial creator data both end up holding a full TikTok session credential.**

### Ranked, with the reason each sits where it does

1. **TikAPI** — the best of a bad field, and the only one worth another hour. Real creator analytics
   **for live streams** (watch time, audience age/gender/region, traffic sources), a QR-in-the-real-app
   flow where no password or cookie is typed, a named founder since 2021, and honest $29/$79/$189
   tiers. **Held back by three things:** video-level analytics are undocumented, its own example value
   for `video_finish_rate_history_7d` is `null`, it stores session cookies, and **its top public tier
   caps at 100 connected accounts when the owner needs ~300.**
2. **TikHub** — the only vendor with confirmed per-video completion rate and audience demographics, at
   $9.60/month. **Disqualified by consent model, not capability**: raw session-cookie paste, Shop
   accounts only, unreadable ToS, no named legal entity.
3. **Phyllo** — official-API-based and therefore capped at public counts. **Its own spec switches
   audience data OFF for TikTok.** Company name required to see any price.
4. **ScrapeCreators** — public counts plus audience countries at $25 to $49 per 1,000 audience calls.
   One field off a fourteen-field list, expensively.
5. **SociaVault** — the same single field, dearer, 13 months old, six months without a changelog entry.
6. **EnsembleData** — the cleanest scraper of the four, and buys the owner nothing he lacks.

### THE PLAN, REPLACED BY THE CORRECTION AT THE TOP

**The plan below was written before Ayrshare was found. Use this one instead.**

**Step 1, free, this week: start the Ayrshare Launch 28-day trial** (no credit card) and connect **one
TikTok account the owner controls**, never a clipper's. Post a clip, wait 48 hours, call
`/analytics/post` and check whether `videoViewRetention`, `averageTimeWatched`, `impressionSources`
and `audienceCountries` actually arrive with values rather than nulls. **That single test costs
nothing and settles the entire question.** Every prior round on this topic failed by reasoning from
documentation instead of doing this.

**Step 2, the diagnostic question for the peer**, which is now sharper: *does his tool show a retention
GRAPH, or just a set of numbers?* **A graph at one-second granularity means he is using cookies** and
the credential and terms-of-service problems in PART 5 all apply to him. **Numbers, or a coarse
retention array, means he is on an Ayrshare-class reseller** and the owner can simply do the same.

**Step 3, only if step 1 returns real values: a two-clipper pilot** on the same trial. Pick clippers
who will tolerate friction, walk them through the **"Turn On" step in their own TikTok app**, and
measure how long it takes and how many give up. **That step is the likeliest killer and cannot be done
for them.**

**Step 4, stop conditions, written down now.**

* **Stop if the trial returns nulls** where the docs promise fields. The docs are a claim; the trial is
  the evidence.
* **Stop if fewer than half of the pilot clippers complete "Turn On" unaided.** At 43 active TikTok
  clippers there is no headroom for a flow most abandon.
* **Stop if Ayrshare requires a registered company**, which is UNVERIFIED and would reproduce exactly
  the wall BL-726 hit.
* **Stop if the cost lands above roughly $716/month** without the coverage justifying it, remembering
  that this buys analytics for 18.6% of clip volume.

**What must NOT happen:** adopting TikHub or TikAPI. Both end with a third party holding a full TikTok
session for the owner's clippers, and an official OAuth route now demonstrably exists.

### The superseded plan, kept for audit

**Step 1, before any code: ask the peer one question.** *What exactly does your clipper see when they
connect, and what data do you actually get back?* **He has a working system; one screenshot of that
consent screen answers what a full round of vendor research could not.** This round proves the peer is
not using TikTok's own APIs (no analytics scope exists, verified twice from primary sources) and not
using any of the four scrapers (no consent model exists at all). **So he is using session-credential
capture, or he has a company, or what he built is less than it appears.** Which one decides everything,
and it costs one message.

**Step 2, the one cheap decisive test, only if step 1 does not already end it.** **$29 for one month of
TikAPI Starter, authorized against a burner TikTok account the owner controls — never a clipper's.**
Call `/creator/analytics/video?media_id=...` and `/creator/analytics/followers` and diff the actual
JSON against the metric list. **That single test resolves the only genuine open question in this
report.** Do not skip to a rollout on the strength of documentation; the schema for those two types is
not published, and the last two rounds were lost to exactly that kind of inference.

**Step 3, the stop conditions, written down now so they are not negotiated away later.**

* **Stop if the TikAPI video test returns counts plus a null finish rate.** That is not a screen-share
  replacement, and the owner has been promised one twice already.
* **Stop if any flow requires a clipper to paste a cookie, a password, or anything other than an
  approval inside their own TikTok app.** This is the hard line. It applies to TikHub today.
* **Stop if the connected-account price above 100 is not disclosed in writing.** An unpriced dependency
  for 300 clippers is not a plan.
* **Stop if fewer than 20 of the 43 active TikTok clippers complete the flow in the first month**,
  because below that it costs more to maintain than the calls it saves.

### Said plainly, because two prior rounds were confidently wrong

**BL-722 said the fields were reachable and was wrong, having missed the sentence saying TikTok does not
onboard individuals. BL-726 corrected it and was right. This round confirms BL-726 from TikTok's own
primary sources and extends it: the third-party route does not rescue the project either.**

**For a clipper's videos, average watch time, total watch time, the retention curve, traffic sources,
reach and profile views are not obtainable by this owner from any examined source.** The partial
exceptions are real and must not be oversold: TikHub returns completion rate and audience demographics
for Shop accounts at the price of a credential no platform should request, and TikAPI returns the full
set **for live streams only**, with the video equivalent undocumented and its one retention-shaped
field null in the vendor's own example.

**The screen-share call cannot be replaced today.** At best it becomes shorter for under a fifth of
clips, and only by asking clippers for something they would be right to refuse.

---

## WHAT COULD NOT BE ESTABLISHED

Stated prominently, because a gap reported as a gap is worth more here than a confident guess.

* **What TikAPI's `/creator/analytics/{type}` returns for `type=video` and `type=followers`.** All five
  types share one documented `$ref` schema reflecting `overview`. **This is the single most
  consequential unknown in the report and step 2 exists solely to close it.**
* **Whether `video_finish_rate_history_7d` ever returns a value.** It is `null` in TikAPI's own example,
  as are all seven `video_*_history_7d` fields.
* **Whether `pv_history` means profile views.** TikAPI publishes no field descriptions at all, so the
  reading is inference and is marked UNVERIFIED rather than tabulated as available.
* **TikAPI's per-account overage fee above 5/30/100, and any Enterprise price for ~300 accounts.**
* **Whether either vendor's analytics work for a plain personal TikTok account**, versus Creator or
  Business. TikHub documents Shop-gating on most creator endpoints; TikAPI says "business or creator
  accounts". **Most clippers are plain personal accounts, so this could invalidate both regardless of
  everything else.**
* **Whether the TikAPI 5-day trial or Phyllo sandbox can start without a card.** Confirming required
  completing a signup, which was out of scope.
* **How the peer actually did it: UNRESOLVED.** That agent did not return. What this round can say is
  what he did **not** do: not the Display API, and not any of the four scrapers. Step 1 resolves it in
  one message and no further research substitutes for that.
* **No live API call was made against any vendor**, so all field-level findings are documentary.
* **`audienceLocations` provenance** at ScrapeCreators and SociaVault is undocumented by both; the
  shared-upstream reading is explicitly UNVERIFIED.
* **TikHub's legal entity, jurisdiction, ToS and privacy policy could not be read at all** — the pages
  are JavaScript shells returning no text. For a vendor that would hold clipper credentials, that is
  not a minor gap.
* **Phyllo's TikTok finding comes from the documented example** in its current published spec, which
  carries 2021 timestamps. It is the vendor's own current reference, but a live `/v1/work-platforms`
  call would be the ideal cross-check and needs credentials.
