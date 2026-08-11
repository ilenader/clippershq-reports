# BL-768 — is there a usage-priced vendor with creator-consented TikTok depth?

**2026-08-11 · RESEARCH ONLY. READ ONLY on the codebase.**
No code, config, schema or data changed. **Nothing was signed up for, no free tier was used, no payment
details were entered, no credential stored, and no TikTok account authorized.** Base `origin/main`
@ `9d285c8c`, isolated worktree `C:/m768`, removed at exit, `node_modules` never junctioned. A
markdown-only diff cannot change tsc or build, so neither was run and neither is claimed.

Five agents researched in parallel. Four returned; the fifth (TikTok partner directories) did not and
is reported as incomplete rather than filled in. Every claim is cited to the vendor's own page or its
machine-readable specification.

---

## THE ANSWER, BEFORE THE WORKING

> **No vendor is confirmed to qualify. The market splits cleanly and the split is the finding:
> consented-OAuth vendors price per connected profile, and usage-priced vendors are scrapers serving
> public handles. Nothing sits in both boxes.**
>
> **One candidate breaks the pricing wall and deserves a free test: [bundle.social](https://bundle.social).
> Unlimited connected accounts on a flat $100/month, plus a free tier with 3 accounts and no card.**
> That passes the pricing test outright, which nothing else does.
>
> **But its own API reference lists only counts for TikTok**, while a marketing page claims audience
> demographics and watch time. **That contradiction is unresolved and points the wrong way**, so it is
> reported as a lead to test, not a recommendation.
>
> **The honest position: the owner cannot buy what he wants on a per-call basis today.** The realistic
> options are a free bundle.social test that probably disappoints, Ayrshare's per-profile pricing for
> a deliberately small subset, or keeping the screen-share call. PART 4 costs all three.
>
> **One measured fact reshapes the economics entirely: only 14 clippers who requested a payout in the
> last 30 days had any TikTok clips at all, and they posted 117 between them.** The on-demand design is
> not merely cheaper than polling, it is a different order of problem.

---

## PART 0 — THE THREE TESTS, STATED BEFORE SEARCHING

1. **PRICING SCALES WITH USAGE, NOT CONNECTED CREATORS.** Per call, per request, per credit, or a flat
   tier that does not cap connected accounts. **Per-profile or per-seat is disqualified however cheap
   the entry tier**, because hundreds of creators must connect.
2. **RETURNS CREATOR-PANEL DATA**, not public counts. BL-767 established public counts are worthless
   because LamaTok supplies them free.
3. **WORKS WITHOUT THE OWNER HAVING A REGISTERED COMPANY.** A required "company name" field on the only
   route to pricing, or a mandatory sales call, counts as a failure.

---

## PART 1 — THE FIELD, WITH FAILURES KEPT SHORT

### Failed test 1, priced per profile, per seat or per data source

| Vendor | Model | Pricing URL |
|---|---|---|
| **Ayrshare** | The baseline that has the data. $149/mo for ONE profile, $299/10, $599/30 | [pricing](https://www.ayrshare.com/pricing/) |
| Upload-Post | Profile-capped: Free 2, $24/5, $50/25, $147/75, $438/225 | [llms-full.txt](https://www.upload-post.com/llms-full.txt) |
| Blotato | Account-capped: $29/20, $97/40, $499 agency | [pricing](https://blotato.com/pricing) |
| Postiz (cloud) | Per channel: $29/5, $39/10, $49/30, $99/100 | [pricing](https://postiz.com/pricing) |
| social-api.ai | Profile-capped: Free 2, $29/10, $109/50, $349/200 | [social-api.ai](https://social-api.ai/) |
| Databox | Per data source and seat. Notably **does** document TikTok `total full video watched rate by video` and `total average view time`, proving the fields are resellable | databox.com |
| Dataslayer.ai | Tiers gate connectors, users and accounts per connector | dataslayer.ai |
| Windsor.ai | Tiers gate data sources and connected accounts, $23 to $598 | windsor.ai |
| **InsightIQ / Phyllo** | Quote-only, **"Company Name" required** on the only route to pricing. Fails tests 1 and 3, and BL-767 proved it fails test 2 for TikTok | [pricing](https://www.getphyllo.com/pricing) |

**InsightIQ is confirmed to be Phyllo's rebrand**, not a new option: `docs.insightiq.ai` and
`docs.getphyllo.com` serve the **same Stoplight project id `18203562583`**, and the InsightIQ copy still
carries Phyllo-authored body text verbatim. The rebrand did not fork the docs, so BL-767's finding
carries over: TikTok reads `audience.is_supported: false` while Instagram reads `true`.

### Late API and Zernio are ONE company, and the case is instructive

**`getlate.dev` 301-redirects to `zernio.com`.** They are the same vendor rebranded, not two candidates.

**Test 1 FAIL, but not for the reason expected.** Its own rate card
([pricing.md](https://zernio.com/pricing.md)) says: *"You pay per connected social account, per month…
Connect a customer's Instagram and TikTok and that's 2 accounts."* Tiers: 1 to 2 free, **3 to 10 at
$6/month each, 11 to 100 at $3, 101+ at $1**. Its own worked examples give **100 accounts = $318/month
and 1,000 accounts = $1,218/month.**

**That deserves an honest note, because it partly undermines the round's own framing.** Per-profile
pricing is not inherently unaffordable; **Zernio's per-profile rate is roughly a fiftieth of
Ayrshare's.** Had a vendor with the data priced like this, 300 clippers would have cost about
$800/month and the whole question would be settled. **The disqualifying property is Ayrshare's price
level, not the per-profile model as such.** The owner should keep that in mind if he ever negotiates.

**Test 2 FAIL, fatally.** Zernio's complete TikTok analytics table is **Likes, Comments, Shares, Views**
plus `follower_count`, `following_count`, `likes_count`, `video_count`
([docs](https://docs.zernio.com/platforms/tiktok)). **Zero of the ten fields.** It holds Display API
scopes only (`user.info.basic`, `user.info.stats`, `video.list`, `video.publish`), not
`video.insights`. Consent is genuine TikTok OAuth with no credential capture, which is to its credit
and does not save it.

**And it publishes a false capability claim, which is itself the finding.** Verbatim from its docs:

> *"The deep metrics that live in TikTok Studio are NOT available on any public TikTok API, **even for
> Business accounts**: profile_views / account-level impressions / reach / … video watch time, average
> watch time, full-watched rate / impression_sources … **There is no public API workaround.**"*

**That is false**, and it was refuted against TikTok's own documentation on `business-api.tiktok.com`,
which documents `video_view_retention` (with `second` and `percentage` sub-fields),
`average_time_watched`, `total_time_watched`, `full_video_watched_rate`, `impression_sources` (enum
`For You`, `Follow`, `Sound`, `Personal Profile`, `Search`, `Others`, `Direct Message`),
`audience_countries`, `audience_genders`, `reach`, `profile_views` and `audience_ages`. **Ayrshare
ships exactly these fields, so the claim is disproved by a competitor's shipping product.** Treat *"no
public API workaround"* as a roadmap statement rather than a technical one: a vendor that believes the
data is impossible will not build it next quarter either.

**One new gate worth recording.** Since **2026-03-20** TikTok requires an Accounts API Access
Application Form for any new app requesting the TikTok Accounts scope. **UNVERIFIED** against TikTok's
own page this round, but if accurate it raises the barrier for any future vendor entering this space,
which makes the current thin field less likely to improve on its own.

### Failed test 2, usage-priced but public counts only

**Modash** is the important one because it genuinely passes test 1 on unit. Its per-endpoint credit
costs are published in its own spec (influencer report 1 credit, search 0.01/result, raw profile
0.025). **It fails test 2 decisively:** a grep of both OpenAPI bundles (741 KB,
[discovery.yaml](https://docs.modash.io/_bundle/products/discovery_api/openapi_doc/discovery.yaml),
[raw.yaml](https://docs.modash.io/_bundle/products/raw_api/openapi_doc/raw.yaml)) returns **zero
matches** for `retention`, `watchTime`, `averageWatch`, `fullVideo`, `completionRate`,
`impressionSource`, `trafficSource`, `profileViews`. Its demographics are weight-thresholded estimates
over a crawled index, and **there is no OAuth anywhere in either spec** — auth is a static bearer token
belonging to the customer, so Modash never touches a creator's account and structurally cannot return
panel data. Dollars per credit are **UNVERIFIED** and API access is gated behind "contact our team".

Also failing test 2, all public-handle scrapers with no consent flow, several surfaced only on
comparison pages and **UNVERIFIED**: Social Fetch, SocialCrawl, Data365, Xpoz, keyapi.ai, TikLiveAPI,
plus BL-767's EnsembleData, SociaVault, ScrapeCreators and TikHub.

### Failed test 3, self-hosted but you must be the developer

**Mixpost** is the cleanest test-1 pass in the entire field: self-hosted, one-time $299,
**"unlimited social accounts"**, no monthly fee ([pricing](https://mixpost.app/pricing)). **It fails
tests 2 and 3.** Its TikTok setup doc requires the user to supply their own client key and secret from
a TikTok developer app, and directs them to **Login Kit and the Content Posting API only**
([docs](https://docs.mixpost.app/services/social/tik-tok/)) — the products that return counts. Postiz
self-hosted is identical: own app, scopes `user.info.basic, video.create, video.publish, video.upload,
user.info.profile` ([docs](https://docs.postiz.com/providers/tiktok)).

**This is the single most clarifying result in the round.** Self-hosting does not merely put the owner
back at the company wall BL-726 found; **it routes him to a product set that would not return the
analytics even if he cleared it.** The Business API is a separate platform, and no self-hosted tool
reaches it.

---

## PART 2 — THE ONE CANDIDATE THAT PASSES THE PRICING TEST

### bundle.social

| Test | Verdict |
|---|---|
| **1. Usage-priced, not per creator** | **PASS, outright.** "Unlimited social accounts" on every paid tier |
| **2. Creator-panel depth** | **UNRESOLVED, and the evidence points the wrong way.** See below |
| **3. No registered company** | **LIKELY PASS.** Free tier needs no payment details; no company requirement stated. Marked UNVERIFIED |

**Pricing** ([pricing](https://bundle.social/pricing)): **Free** $0, 20 posts/month, **3 social
accounts, no payment details required**. **Pro $100/month**, 10,000 posts/month, **unlimited social
accounts**, 14-day trial. **Business $400/month**, 100,000 posts/month, unlimited accounts. Analytics
are included in all tiers with **no separate metering**. The only usage-metered item is X/Twitter
posting at $0.015 per post. **The unit is posts and storage, never connected accounts.**

**Consent flow:** "Connect a TikTok creator or business account via the OAuth connect URL flow"
([source](https://bundle.social/tiktok-audience-demographics)). **Whether that terminates at TikTok's
own consent screen is UNVERIFIED**, though an OAuth connect URL is not credential capture and is a
different class from TikHub's pasted session cookie. Authorization is per account, with later posts
appearing automatically.

**Rate limits and refresh, which matter more than price here**
([analytics doc](https://info.bundle.social/api-reference/analytics.md)):

* **"Analytics are automatically refreshed every 24 hours."**
* On-demand refresh exists (`force-refresh-social-account-analytics`, `force-refresh-post-analytics`)
  but is **strictly metered: "Maximum force refresh requests per day = number of teams x 5"**, 429 on
  exceeding.
* **Data is deleted after 30 days.** "If you need analytics from 3 months ago and you didn't save them,
  we can't help you." Anything the owner wants to keep, he must store himself.

### The contradiction, resolved as far as the evidence allows

**The marketing page claims panel depth.**
[bundle.social/tiktok-audience-demographics](https://bundle.social/tiktok-audience-demographics) lists
"Age group splits", "Gender distribution", "Top cities", "Top countries", "Watch time by day" and
"Video-level metrics", via `GET /api/v1/analytics/social-account/raw?teamId=…&platformType=TIKTOK`.

**The API reference lists only counts.** The same site's analytics documentation states TikTok's
available metrics are **"Profile: impressions, views, likes, comments, followers, following"** and
**"Posts: impressions, views, likes, comments, shares"**. **No retention, no average watch time, no
full-video-watched rate, no traffic sources, no profile views.**

**The raw endpoint's payload is undocumented.** Its OpenAPI schema declares the field as
`raw: nullable: true` with **no TikTok example and no field list**
([doc](https://info.bundle.social/api-reference/client/analytics/get-social-account-analytics-raw.md)).

**So the demographics claim exists on a marketing page and nowhere in the specification.** That is
precisely the pattern that made Phyllo look qualified until its spec was pulled, and BL-767 was written
because two rounds before it trusted marketing over references. **I am not repeating that.** The claim
is a lead, and the free tier is how to settle it.

### Post for Me, the runner-up on pricing

$10/month for 1,000 successful posts with **"unlimited social accounts"**
([pricing](https://www.postforme.dev/pricing)), so it passes test 1. **Analytics are described only as
"Analytics for social posts"** with no field list, and its homepage mentions views, likes, shares and
engagement, which is public-counts depth. **Test 2 UNVERIFIED and unlikely.** No free tier.

---

## PART 3 — THE OWNER'S REAL COST, COMPUTED HIS WAY

### Assumptions, measured rather than assumed where possible

Measured from live data at `2026-08-11 09:13:46 UTC`:

| | Brief's assumption | **Measured** |
|---|---|---|
| Clips per month | ~2,300 | **1,700** |
| TikTok share | 18.6% | **18.3%**, 311 clips |
| Clippers posting TikTok in 30 days | — | **42** |
| **Clippers requesting a payout in 30 days** | — | **33** |
| **Of those, how many had TikTok clips** | — | **14** |
| **Their TikTok clips in 30 days** | — | **117** |

**The last two rows are the whole of PART 3.** A payout-time fetch does not touch 430 clips or 300
creators. **It touches 14 clippers and 117 clips a month.**

### On-demand at payout versus continuous polling

| Design | Calls per month | bundle.social | Ayrshare |
|---|---|---|---|
| **On-demand at payout** | **117 fetches, ~4/day** | **$100/month flat** | Needs those 14 clippers connected as profiles |
| Continuous polling at the 10-minute tick | 311 clips x 4,320 ticks = **1,343,520** | **STRUCTURALLY IMPOSSIBLE**, see below | Per-profile, so polling is free of extra charge but rate limits are UNVERIFIED |

**Continuous polling is not expensive on bundle.social, it is impossible.** The force-refresh quota is
`teams x 5` per day, so a single team gets **150 refreshes a month** against the 1.34 million a 10-minute
tick would demand. The only other cadence is the automatic 24-hour refresh. **The product cannot poll,
and that happens to fit the owner's stated design exactly.**

**Does refetching the same clip an hour later cost again?** **No, not in money.** Nothing is billed per
analytics call. It consumes one unit of the `teams x 5` daily force-refresh quota; without a force
refresh the second call returns the same value the 24-hour cycle last wrote, at no cost. **At 117
fetches a month the quota is comfortable with one team and generous with three.**

### Cost at 50, 150 and 300 connected clippers

| Connected clippers | **bundle.social** | **Ayrshare** |
|---|---|---|
| 50 | **$100/month** | $599 + 20 x $8.99 = **~$779/month** |
| 150 | **$100/month** | $599 + 70 x $8.99 + 50 x lower tier ≈ **$1,400 to $1,600/month** |
| 300 | **$100/month** | Enterprise, **unpriced** |

**bundle.social's line is flat because connected accounts are free.** That is the entire reason it is
in this report, and it is what the owner asked for. **The catch is that the flat line may be buying
public counts**, in which case $100/month buys what LamaTok already gives free.

---

## PART 4 — WHAT IF NOTHING QUALIFIES, WHICH IS THE LIKELY CASE

**Stated plainly, because three prior rounds softened this question into a weak recommendation.**

**No vendor is confirmed to meet all three tests.** bundle.social passes 1 and probably 3, and its own
API reference argues against 2. Everything else fails on pricing model or on depth. **The honest
alternatives, with true costs:**

**Option A, the free test, $0.** Sign up for bundle.social's free tier (3 accounts, no card), connect
one TikTok account the owner controls, call the raw analytics endpoint and read what actually arrives.
**Costs nothing, resolves the only open question in this report, and is strictly better than any
further reading.** If demographics and watch time arrive, the answer is $100/month flat for unlimited
clippers and the product is affordable. If only counts arrive, the vendor is out and the owner has lost
an afternoon rather than a month.

**Option B, Ayrshare for a deliberate subset.** Ayrshare is the only vendor BL-767 verified returns
`videoViewRetention`, `averageTimeWatched`, `fullVideoWatchedRate`, `impressionSources`, `reach`,
`audienceCountries` and `audienceGenders`. It is unaffordable for everyone, **but it does not have to
be everyone.** Only 14 payout-requesting clippers had TikTok clips last month. Connecting the clippers
who request the largest payouts, say 30, costs **$599/month on the Business tier** with the profiles
included. Over 90 days the distinct requester population was 72, so a 30-profile ceiling would need
rotation or would cover roughly the top half. **This is the only option that certainly delivers the
retention curve.** Whether $599/month is worth it for 18.3% of clip volume is the owner's call, and the
honest framing is that it buys scrutiny of large payouts, not platform-wide analytics.

**Option B2, negotiate on the per-profile axis rather than abandoning it.** Zernio's rate card shows
per-account pricing at **$3/account from 11 to 100 and $1 above 100**, roughly a fiftieth of Ayrshare's.
Ayrshare's Enterprise tier above 300 profiles is unpriced. **The owner has never asked what 300
profiles actually costs**, and the round's own framing assumed per-profile is fatal when the evidence
shows only that Ayrshare's list price is high. **One email to Ayrshare sales asking for a 300-profile
quote costs nothing and could collapse this entire problem.** It is the one action here with a large
upside and no downside beyond a sales conversation.

**Option C, build nothing and keep human review.** Free. BL-664 measured reviewers at a **0.77% overturn
rate**, which is very good, and R-5 proved the existing `fraudScore` has **zero predictive power**. **The
current process is not failing.** The case for spending anything here is that a screen-share call does
not scale, not that review quality is poor.

**No failing vendor is recommended to have an answer.** Modash, Mixpost, Post for Me, Upload-Post,
Blotato, Postiz, InsightIQ and the scrapers are all out, each for a stated reason.

---

## PART 5 — THE VERDICT

> ## **No usage-priced vendor with creator-consented TikTok depth is confirmed to exist. The one candidate that breaks the per-creator pricing wall is bundle.social at a flat $100/month for unlimited accounts, but its own API reference documents only counts for TikTok while its marketing claims demographics, so it is a free test rather than a recommendation. If it disappoints, the real choice is Ayrshare at $599/month for a subset of about 30 clippers, or keeping the screen-share call.**

### Ranked

1. **bundle.social** — the only vendor whose price does not scale with creators, and the only one with a
   free tier that can settle its own question. Ranked first **because the test is free**, not because
   the capability is proven. Its API reference points the wrong way and that is stated, not buried.
2. **Ayrshare** — fails the pricing test and therefore fails the round's brief, but it is the only
   vendor with **verified** retention, watch time and impression sources. Ranked second because a
   subset deployment is a real, costed option that certainly works.
3. **Post for Me** — passes on pricing at $10/month with unlimited accounts, but analytics depth is
   undocumented and probably counts. Worth ten minutes only if bundle.social fails.
4. **Modash** — usage-priced and well documented, but its own specs prove it has no panel fields and no
   OAuth. Out.
5. **Mixpost** — the best pricing model in the field, one-time $299 and unlimited accounts, and it
   cannot reach the Business API. Out, and instructive about why self-hosting is a dead end.
6. Everything else — per-profile pricing or public-handle scraping. Out.

### The smallest next step, and exactly what the owner must do

**This is a $0 test and it should happen before any further research.** BL-767 warned that every prior
round on this topic failed by reasoning from documentation instead of running it, and this round has
now produced a second marketing-versus-reference contradiction that only execution can settle.

1. Go to **bundle.social** and create a **free account**. It allows 3 social accounts and **requires no
   payment details**. Use any email; nothing here needs the platform's identity.
2. Connect **one TikTok account the owner controls**, never a clipper's, through the OAuth connect URL.
   Note what the consent screen actually says and whether it is TikTok's own, which is currently
   UNVERIFIED and matters for whether clippers can be asked to use it.
3. Post or pick an existing video on that account, wait **24 hours** for the automatic refresh, then
   call `GET /api/v1/analytics/social-account/raw?teamId=…&platformType=TIKTOK` and the post analytics
   endpoint.
4. **Read the raw payload and answer one question: are audience age, gender, countries and any watch
   time present, or only impressions, views, likes, comments and shares?** That single response decides
   whether this vendor is a $100/month solution or a duplicate of what he already has free.
5. If it disappoints, **do not research further.** Go to Option B or B2 and decide whether $599/month
   for about 30 connected clippers is worth it, or stay with human review.

**Do these two in parallel, since neither blocks the other and both are free:** the bundle.social test
above, and **one email to Ayrshare asking what 300 connected profiles costs.** Between them they close
every open question in this report.

---

## WHAT COULD NOT BE ESTABLISHED

* **bundle.social's actual TikTok fields**, which is the entire open question. The marketing page and
  the API reference disagree, and the raw endpoint's payload is `nullable` with no example. **Only the
  free test resolves it.**
* **Whether bundle.social's OAuth terminates at TikTok's own consent screen.** An "OAuth connect URL"
  is not credential capture, but the screen was not observed.
* **The fifth agent, on TikTok's published partner directories, did not return.** Its question was
  whether any Business API approval-holder prices per call. The forum sweep answered it indirectly and
  negatively: consented-OAuth vendors price per profile or per data source, and per-call vendors are
  scrapers. **Treat that as well-evidenced but not exhaustive.** One partial signal: TikTok's
  `partners.tiktok.com` directory appears to cover ads, measurement and MMM partners rather than the
  organic creator-analytics lane, so it is probably not the route to an approval-holder list.
* **Modash's dollars per credit** and whether its signup requires a company. Its access is gated behind
  "contact our team" regardless, and it fails test 2, so this does not change the verdict.
* **InsightIQ's current spec.** Confirmed to be the same Stoplight project as Phyllo's, so BL-767's
  `audience.is_supported: false` finding for TikTok almost certainly still holds, but the spec itself
  was not re-pulled this round. Marked UNVERIFIED rather than asserted.
* **Whether any vendor privately holds Business API approval not reflected in its public docs.** No
  sales calls were made, nothing was signed up for, no payment details were entered anywhere.
