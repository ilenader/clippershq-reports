# BL-781 — Instagram creator analytics: the bigger problem, the weaker data, and the free signal that already covers it

**2026-08-12 · DB `now()` = `2026-08-12 08:49:32.255798+00` (first read) to `08:55:13.736943+00` (last) · AUDIT ONLY, READ ONLY.**
No code, config, schema or data change. **No account connected, no payment details entered, no paid plan started, nothing authorised.** Base `origin/main` @ `72f05cec`, branch `checkpoint/BL-781`, isolated worktree `C:/bl781`, `node_modules` never junctioned, removed at the end. Every database read through `scripts/run-select.js`, which refuses a write keyword before connecting; every timestamp cast `::text` against DB `now()`. Handles redacted throughout. A markdown-only diff cannot change tsc or build, **so no build was run and none is claimed.** Four subagents ran, all read-only, all reconciled against primary sources below rather than averaged.

## THE VERDICT, IN ONE LINE

> **Do not build Instagram analytics. Instagram's watch-time and completion data has NO documented existence at this vendor at any price, the free arrival curve already computes on 94.8% of Instagram clips today at zero cost, 82.6% of Instagram bought-view rejections were made against a clipper who already had a prior one (which the shipped review panel already shows), and the same effort spent fixing Instagram's missing first snapshot would sharpen the one signal that demonstrably works.**

**Meta's terms do NOT prohibit the owner's intended use.** Nothing here breaches them. They restrict it with four conditions, one of which the current design already violates in principle and is stated in PART 5.

## PART 1 — WHAT bundle.social RETURNS FOR INSTAGRAM

**The vendor's real OpenAPI spec exists** at `https://api.bundle.social/swagger-json` (OpenAPI 3.0.2, 114 paths), linked only from `https://info.bundle.social/llms.txt`. `GET /api/v1/analytics/post` returns **one platform-agnostic normalised schema with exactly nine numeric fields for every platform**: `impressions, impressionsUnique, views, viewsUnique, likes, dislikes, comments, shares, saves`. Everything richer lives in `raw`, which the spec types as literally `{"nullable": true}` with **no schema at all**, and which both platform pages introduce with "when enabled **for your organization**". Raw is sales-gated and off by default.

| field | Instagram | TikTok |
|---|---|---|
| reach | **AVAILABLE** `impressionsUnique` ("Called 'reach' in Instagram API") | **AVAILABLE** `reach`, raw only |
| impressions | **AVAILABLE** `impressions`, but documented as IG's *views* metric, not true impressions | **AVAILABLE** `impressions` = video views |
| plays / views | **AVAILABLE** `views` (Videos and Reels only) | **AVAILABLE** `views` |
| unique views | **ABSENT** — "Returns `0` (not provided by API)" | **AVAILABLE** `viewsUnique` |
| **average watch time** | **UNVERIFIED — no field documented anywhere** | **AVAILABLE** `average_time_watched` (raw) |
| **completion / full-video-watched rate** | **UNVERIFIED — no field documented anywhere** | **AVAILABLE** `full_video_watched_rate` (raw) |
| **total time watched** | **UNVERIFIED — no field documented anywhere** | **AVAILABLE** `total_time_watched` (raw) |
| impression sources | **UNVERIFIED — no field documented** | **AVAILABLE** `impression_sources` (raw) |
| saves | **AVAILABLE** `saves` | **ABSENT** — "Returns `0` (not provided by TikTok API)" |
| shares | **AVAILABLE** `shares`, **contradicted, see below** | **AVAILABLE** `shares` |
| comments, likes | **AVAILABLE** | **AVAILABLE** |
| profile visits | **AVAILABLE at ACCOUNT level** (`views` = profile views, 30d rolling). Per post **UNVERIFIED** | **AVAILABLE at ACCOUNT level** `metrics[].profile_views`. Per post **UNVERIFIED** |
| follows from the post | **ACCOUNT level only**, raw `demographics.follows_and_unfollows` | **ACCOUNT level only**, `metrics[].new_followers` |
| audience countries | **ACCOUNT level only** (`follower_demographics.country`) | **PER POST** `audience_countries` |
| audience genders | **ACCOUNT level only** | **PER POST** `audience_genders` |
| audience ages | **ACCOUNT level only** | **ACCOUNT level** `audience_ages` |

**Instagram exposes that TikTok does not:** the follower-versus-engaged audience split (two different populations, both documented), a `city` breakdown, `follows_and_unfollows` as a pair, 7- and 14-day raw windows (changelog 2026-04-13), and a working `saves`.

**THE HEADLINE, AND IT DECIDES THE ROUND: every fraud-relevant field the TikTok build was designed around — watch time, completion rate, impression source, per-post audience geography — has NO documented Instagram equivalent at any level.** The vendor's own raw-availability table says Instagram post raw exists and contains "media insights", and then **names not one field in it**. That is UNVERIFIED, not ABSENT, and it cannot be settled from documentation: it needs one real connected Instagram business account calling `/analytics/post/raw`.

**Documented versus verified.** Everything above is **DOCUMENTED ONLY**. **Not one analytics field has ever been returned by this vendor for any platform**, Instagram or TikTok, so nothing in this table is verified by a call. The only live evidence this round produced is route existence: `GET /analytics/post/bulk` answers **401** (auth gate reached, route exists) while the plural `/analytics/posts/bulk` answers **404**, identical to a nonsense control path.

**That corrects BL-770.** Its "documented but non-existent endpoint" was a path-name error on our side, not vendor overstatement. The vendor's reliability record still stands at **three defects**: BL-777's inert `teamId` (confirmed, the current spec lists no `teamId` on `/analytics/post` at all), the `postId` versus `importedPostId` exclusivity, and a new one found this round — `data-retention.md` publishes **two code samples that cannot work**, calling `getBulkPostAnalytics({teamId})` when the endpoint requires `postIds[]` + `platformType` and accepts no `teamId`.

**Unresolved contradiction, reported not averaged:** the Instagram platform page says `shares` is "Reels only"; the changelog dated **2026-03-16** says "Fixed shares tracking for all Instagram post types (previously only counted for Reels)". One is stale, probably the platform page. Do not assume either.

**What the vendor will not disclose before payment**, which is itself a finding: the price of raw-analytics enablement (every field beyond the normalised nine sits behind it), the price of ongoing refresh for imported posts ("additional platform usage fees may apply"), and the price of sub-24h refresh ("we will discuss these costs with you directly"). There is no sandbox and no sample Instagram raw response anywhere.

## PART 2 — THE ACCOUNT-TYPE FRICTION, SETTLED FROM META'S OWN CURRENT DOCS (v25.0)

**Both prior rounds were partly right and the brief mis-states BL-722.** BL-722 actually concluded a Page is NOT required; the brief attributes the opposite to it. Meta's docs settle it per login path:

> "To use the APIs, your app users must have an **Instagram professional account**. An Instagram professional account can be for a business or creator." — https://developers.facebook.com/docs/instagram-platform/overview
> "The Instagram API with Facebook Login **cannot access Instagram consumer accounts**." — https://developers.facebook.com/docs/instagram-platform/instagram-api-with-facebook-login
> "This API setup **does not require a Facebook Page** to be linked to the Instagram professional account." — https://developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login
> "If your app implements Facebook Login for Business, your app users' Instagram professional accounts **must be connected to a Facebook Page**." — overview, comparison table row: Instagram Login "x", Facebook Login "Required"

**So: Business or Creator required on both paths, personal accounts cannot authorise at all; a Facebook Page is required ONLY on the Facebook Login path.** BL-722 is right on account type and wrong on the Page; BL-767 is right on the outcome and wrong on the mechanism, because the Page requirement disappears with the **login path**, not because a vendor is in the middle. **Which path bundle.social uses is UNVERIFIED and it matters twice over:** the vendor exposes `instagramConnectionMethod: "FACEBOOK" | "INSTAGRAM"`, its Facebook flow requires picking a Page, and Meta documents `total_views`, `total_likes` and `total_comments` as **"available for Instagram API with Facebook Login only"**.

**The clipper's exact steps: 6, in the Instagram app**, from https://www.facebook.com/help/instagram/502981923235522 — Profile, More, "Below For professionals, tap Account type and tools", "Switch to professional account", choose a category, confirm. Creator is the right type ("best for public figures, content producers, artists and influencers").

**The one real cost, and it is the likely funnel killer:** "**Professional accounts can't be set to private.** All pending follow requests will be automatically accepted when you go public." (https://www.facebook.com/help/instagram/138925576505882). A private clipper must go public to participate. Followers and content are unaffected and the switch is reversible.

### The real population, measured today

| measure | Instagram | TikTok | YouTube |
|---|---|---|---|
| clips, last 30 days | **1,267 (74.4%)** | 297 (17.4%) | 138 (8.1%) |
| distinct clippers, last 30 days | **70** | 41 | 20 |
| approved clips, last 30 days | 1,047 | 236 | 109 |
| approved earnings, last 30 days | **$2,284.94 (72.6%)** | $847.18 | $13.40 |
| approved earnings, all time | $3,551.32 | **$4,718.52** | $414.17 |
| APPROVED accounts | **399** (269 users) | 355 | — |

**Instagram is the bigger prize on volume and on current money, but not historically:** TikTok still holds more all-time approved earnings, so "Instagram is worth more" is true of the last 30 days and false of the ledger as a whole. Both figures ship here rather than the flattering one.

**Concentration, the equivalent of BL-772's top-5-at-71%:** across 150 Instagram clippers, the **top 5 hold 50.2% of Instagram earnings, the top 10 hold 69.2%, the top 20 hold 89.8%**. By 30-day clip volume the top 5 accounts carry **52.7%**, the top 10 **68.9%**, the top 20 **83.5%**. **Instagram is LESS concentrated than TikTok** (top 10 at 69.2% here against TikTok's top 10 at 71.0% of clips and top 5 at 71% of earnings), so Instagram needs more people to move the same share, not fewer.

**How many would plausibly convert: UNVERIFIED, and it is the same measurement BL-722 asked for in August and nobody has run.** `clip_accounts.followerCount` is **NULL on all 399 approved Instagram accounts**, and no account-type field exists anywhere in the schema, so the share already on a professional account cannot be computed from our data. BL-722 priced the HikerAPI census that would settle it at roughly **$0.31**. It has still not been run. **Any conversion estimate before it is a guess, and this report will not make one.**

## PART 3 — EXPIRY AND CAPS

**Instagram has NO equivalent of TikTok's 7-day vanishing window. This is the one place Instagram is strictly better.**

> "Data used to calculate metrics can be delayed up to **48 hours**." · "**Metrics data is stored for up to 2 years**." · "**Story media metrics are only available for 24 hours**." · "If insights data you are requesting does not exist or is currently unavailable, the API returns an **empty data set instead of `0`**." — https://developers.facebook.com/docs/instagram-platform/reference/instagram-media/insights
> "User Metrics data is stored for up to **90 days**." — https://developers.facebook.com/docs/instagram-platform/insights

So the six-of-nine TikTok expiry that forced the capture-early design has no Instagram counterpart at Meta's level. **The capture-early design is still mandatory, for a different reason: the VENDOR deletes all analytics, parsed and raw, at 30 days with "no backups, no recovery"** (https://info.bundle.social/api-reference/data-retention.md).

**Also settled from Meta, and it kills a whole class of feature:** demographics (`follower_demographics`, `engaged_audience_demographics`) exist **only at account level**, never per media, are "not returned if the IG User has **less than 100 followers**", and return only the "top 45" performers. **There is no "who watched this clip" on Instagram at any price.**

**Current Reels metric list, v25.0, 16 fields:** `comments, crossposted_views, facebook_views, ig_reels_avg_watch_time, ig_reels_video_view_total_time, likes, reach, reels_skip_rate, reposts, saved, shares, total_interactions, views`, plus `total_comments`/`total_likes`/`total_views` on the Facebook Login path only. **`impressions`, `plays`, `video_views` and `clips_replays_count` are all DEPRECATED** (v22.0, 2025-01-21, effective 2025-04-21; `video_views` in v21.0, 2024-10-02), replaced by the single canonical `views`. **So Meta itself exposes `ig_reels_avg_watch_time` and `reels_skip_rate`; the gap in PART 1 is the VENDOR's, not Meta's.** That is the strongest argument for going direct to Meta rather than through this vendor, and also the argument for doing neither.

### The cap, and whether $100 covers Instagram

**Instagram imports do NOT have a separate cap, and they do not consume TikTok's either.** The spec's `GET /api/v1/organization/usage/imports` returns one org-wide `limitPerSocialAccount` plus per-account `used`/`limit`/`remaining`. **Every connected account gets its own bucket of the same size**: 5 a month free, 100 on Pro at $100, 500 on Business (https://bundle.social/pricing). Adding Instagram accounts adds buckets.

Measured against the real Instagram volume, per posting account, last 30 days: **100 accounts, 1,267 clips, median 4 clips per account, mean 12.7, busiest single account 157.**

| | free (5 per account) | Pro, $100 (100 per account) |
|---|---|---|
| accounts over the cap | **41 of 100** | **2 of 100** |
| Instagram clips capturable if EVERY account connects | **346 of 1,267 (27.3%)** | **1,165 of 1,267 (91.9%)** |
| the top 5 accounts' 527 clips | **25 captured (4.7%)** | 425 captured |

**Plainly: $100 a month covers Instagram at this volume, at 91.9%, and the free tier does not cover it at all — it captures a quarter, and on the five busiest accounts it captures one clip in twenty.** Two caveats, both load-bearing. **UNVERIFIED whether an analytics-only read counts as an import** (BL-770 raised it, still unanswered, and it decides whether the flat $100 is flat). And **our own code would break this anyway**: `MONTHLY_CAPTURE_BUDGET` (`src/lib/clip-analytics-capture.ts:261`) is a **global** count of our own rows with no platform predicate (`:263-274`), defaulting to 100, so Instagram and TikTok would share one bucket that does not exist on the vendor's side.

## PART 4 — WHAT IT ADDS BEYOND THE FREE ARRIVAL CURVE. HONESTLY: VERY LITTLE

BL-775 measured the curve separating on Instagram at **66.4% of views by 6 hours for approved clips against 7.8% for bought-view rejections** (2,159 versus 110 clips), the largest separation of any platform, with **no vendor, no connection and no authorisation**. Measured fresh this round:

| | measured today |
|---|---|
| Instagram live clips with 3+ snapshots, so the curve computes | **2,601 of 2,744 = 94.8%** (approved: 2,192 of 2,210 = 99.2%) |
| Instagram clips with no snapshot at all | 38 |
| Instagram bought-view rejections | **109** of 181 platform-wide = **60.2%**, TikTok 47 = 26.0% |
| ... concentrated in | **22 clippers**; top 5 = 83 (76.1%), top 8 = 93 (85.3%) |
| ... made against a clipper who ALREADY had an earlier bought-view rejection | **90 of 109 = 82.6%** (TikTok: 37 of 47 = 78.7%) |

**That last row is the answer to the round's central question.** The single best predictor of an Instagram bought-view rejection is that the same clipper was already caught before, it costs nothing, it needs no vendor, and **it is already shipped and mounted on the review screen** (BL-775, merged at BL-776). Connected analytics would have to beat a signal that already fires correctly on more than four in five of the cases.

**What connected analytics would ADD, specifically:** `ig_reels_avg_watch_time` and `reels_skip_rate` are real fields at Meta and would be genuinely new information — a clip with 300,000 views and a 1.2-second average watch is a fact the arrival curve cannot produce. **By how much it would improve on 66.4 against 7.8: UNMEASURABLE in advance and this report will not invent a number.** No published study gives an AUC for watch-time features against purchased Instagram views; BL-771 established the same absence for TikTok.

**And it does not become a verdict regardless.** BL-771's ceiling stands: every computable signal came in **under 21% precision** against the owner's **99.2%** reviewer bar, so nothing here can auto-reject or be shown to a clipper. What analytics can do is raise the attacker's cost; what it cannot do is decide.

**The honest answer the brief asked for: on Instagram the free signal already does most of the work.** It covers 94.8% of clips today at zero cost against a connected pipeline that covers 0% today, would need 100 accounts converted and connected to reach 91.9%, and whose decisive field is not documented to exist.

**One measured defect that is worth more than the whole integration.** BL-745 found Instagram never gets a submit-time snapshot. **It is still true, and here it is re-measured over the last 14 days:**

| platform | clips 14d | first snapshot within 60s | median seconds to first snapshot | no snapshot ever |
|---|---|---|---|---|
| **Instagram** | 915 | **213 (23.3%)** | **3,201s (53.4 min)** | **33** |
| TikTok | 162 | 143 (88.3%) | **0s** | 2 |
| YouTube | 35 | 33 (94.3%) | **0s** | 0 |

**The platform where the arrival curve separates best is the only platform whose curve starts blind for the first 53 minutes.** Fixing that sharpens the exact signal that already works, on 100% of Instagram clips, with no vendor, no clipper action, no terms exposure and no monthly fee.

## PART 5 — META'S TERMS

**NOTHING THE OWNER INTENDS IS PROHIBITED. The intended use — showing a human reviewer measured facts about a clip already under review, with no auto-reject, no public score and no cross-creator ranking — is RESTRICTED WITH CONDITIONS, not banned.** Meta has **no verbatim equivalent** of TikTok's creator-discovery-and-ranking prohibition. Platform Terms and Developer Policies both **Last Updated 2026-02-03**.

Four conditions, quoted (https://developers.facebook.com/terms/):

> **3.a.viii** "Processing Platform Data for purposes other than the applicable permitted purposes set forth in Meta's Developer Docs."
> **3.a.ii** "…to make eligibility determinations about people, **including** for housing, employment, insurance, education opportunities, credit, government benefits, or immigration status."
> **3.a.v** "Processing Platform Data without valid User consent in order to build or augment user profiles for any purpose."
> **3.d.i.2.d** Delete all Platform Data "When a User requests their Platform Data be deleted or no longer has an account with you (unless the Platform Data has been aggregated, obscured, or de-identified so that it cannot be associated with a particular User…)".

Note **12's definition**: Platform Data "including data anonymized, aggregated, or **derived** from such data" — a fraud signal computed from Instagram insights **is itself Platform Data** and inherits every restriction.

**Cross-creator ranking is effectively prohibited, by inference rather than by a named clause**: it is not in either insights permission's Allowed Usage, and the permissions reference allows analytics beyond that only "through the use of **aggregated and de-identified or anonymized** information (provided such data cannot be re-identified)". A peer band traceable to a named clipper is aggregated but not de-identified. **The existing "no groupBy, no percentile" position is correct and must stay.**

**THE ONE PLACE THE CURRENT DESIGN CONFLICTS, and it is worth acting on whatever happens with Instagram.** BL-777 keeps captured snapshots after a clipper unlinks, on the ground that a snapshot is the record of a payment decision. Against Meta's terms that survives an **unlink** — the word never appears in Section 3, and 3.d.i.2.a's "legitimate business purpose" covers it — **but it does NOT survive a deletion request.** 3.d.i.2.d is an independent trigger with only two carve-outs (de-identified data, or a legal retention requirement for which 3.d.ii demands you hold proof). A snapshot tied to a named clipper qualifies for neither. **3.d.i.1 additionally requires "an easily accessible and clearly marked way" for a user to ask for deletion, and 4.b requires the privacy policy to say how.** Neither exists today.

**The largest open legal risk is UNVERIFIED and unresolved by any published text:** whether Meta reads "eligibility determinations about people" to cover deciding whether a creator gets paid for a clip. The list is prefaced "including", so it is not exhaustive. Human-review-only with no auto-reject is what keeps this away from the clause, which makes BL-518's rule a compliance control and not merely a product preference.

## PART 6 — HOW MUCH IS ALREADY BUILT

| component | rating | evidence |
|---|---|---|
| free arrival curve | **PLATFORM-AGNOSTIC, 0 edits** | `src/lib/review-evidence.ts:168-236` reads `db.clipStat` with no platform predicate; its header already names Instagram |
| `ReviewEvidencePanel` | **ALREADY MULTI-PLATFORM except ONE line** | `src/components/admin/ReviewEvidencePanel.tsx:301-302` short-circuits any non-TikTok platform; `SIX_HOUR_CLAUSE:124-133` already carries a written Instagram clause |
| link table `ClipAccountProviderLink` | **AGNOSTIC**, `platform` is a real discriminator and is read | `prisma/schema.prisma:3181`, cron filter `route.ts:77` |
| `handles.ts`, `ReviewEvidencePanelMount`, `/api/accounts/tiktok-links` body | **AGNOSTIC, 0 edits** | `handles.ts:17-19`; `Mount.tsx:39-115`; `tiktok-links/route.ts:26-30` has no platform filter at all |
| store `ClipAnalyticsSnapshot` | **TIKTOK-SHAPED columns, generic types** | `schema.prisma:3121-3132`; `platform` at `:3107` is **written and never read** (`capture.ts:416`, 0 read sites) |
| capture | **TIKTOK-SPECIFIC, 4 branch points + 10 literal field names** | `clip-analytics-capture.ts:347` hard gate returns `not_tiktok`; `:381` `platformType`; `:91-102` ten TikTok metric names against `classifyField:118-128` which tests exact keys, so Instagram's own key names would classify all ten "absent"; `:261` global budget |
| vendor client | **TIKTOK-SPECIFIC, 4 literals** | `bundle-social.ts:137, 162, 165, 196, 200` |
| routes + UI | **TIKTOK-SPECIFIC paths and copy** | `/api/tiktok-link/return/[linkId]:31`; `TikTokLinkSection.tsx` ~14 copy strings + 3 URLs; gate `AccountDetailPremium.tsx:373`; `ClipAnalyticsCard.tsx` 3 headings + 10 key lookups |

**Instagram fields with NO column in the store:** `saved`, `shares`, `follows`, `replies`, `total_interactions`, `navigation`. **Permanently null on an Instagram capture:** `fullVideoWatchedRate`, `impressionSources`, `audienceCountries`, `audienceGenders`, `audienceAges`.

**Verdict: a SECOND BUILD for connect, capture and UI — 15 files edited, roughly 35 hard-coded TikTok literals, plus one new SQL migration — and a ONE-LINE change for the free signal.** And the capture cron is registered nowhere (`src/lib/railway-cron-scheduler.ts:63-92`), so it does not run today for any platform.

**Every estimate here inherits an unproven chain. The TikTok pipeline has never returned a single analytics field**, at any clip age, from any account. BL-780 applied the schema and confirmed the vendor team now resolves, but nobody has connected. **An Instagram estimate is therefore an extension of something that has never been observed working once.**

**And the marginal value is smaller than it looks, because Instagram data already arrives with no creator authorisation at all:** `src/lib/scraper-providers/hikerapi.ts:740` returns views (probe order at `:457`), likes `:540` and comments `:541` per clip, plus follower count, bio and privacy flag per account at `:308-356`; `src/lib/apify.ts:744-766` is the fallback ladder. **A connected pipeline adds nothing to view counts.** It adds watch time, skip rate, reach, saves, profile visits and follows, of which only reach and saves are documented at this vendor.

## PART 7 — THE VERDICT, RANKED

> **Instagram is NOT worth building: the decisive field (watch time) is not documented to exist at this vendor for Instagram, the cost is $100 a month plus an undisclosed raw-analytics fee plus a second build of 15 files, and it would need roughly 10 of 150 clippers connected to reach 69% of Instagram earnings and all 100 posting accounts to reach 92% of clips — against a free signal that already computes on 94.8% of them today.**

| option | cost | what it buys | rank |
|---|---|---|---|
| **Fix Instagram's missing first snapshot** (BL-745, still live: 23.3% within 60s, median 53.4 min) | one round, no vendor, no clipper action, no terms exposure | sharpens the ONLY signal measured to separate on Instagram (66.4 vs 7.8), on 100% of Instagram clips | **1. Do this** |
| **Do nothing more** | zero | the free curve at 94.8% coverage plus per-clipper history catching 82.6% of Instagram bought-view rejections, both already shipped | **2. Perfectly defensible** |
| **Wait for the TikTok pilot to return one real field** | zero, the owner is already messaging a clipper | settles whether the vendor returns anything at all, and one connected IG business account would settle the Instagram raw question that documentation cannot | **3. The gate on everything below** |
| **Build Instagram analytics** | $100/mo + undisclosed raw fee + 15 files + a clipper conversion that makes private accounts public | watch time and skip rate **if** the vendor's undocumented IG raw payload contains them | **4. Do not start** |

**Two prior rounds recommended against building and both were right. This is a third.** If the owner wants one number before deciding anything, it is the **$0.31 HikerAPI census** BL-722 specified in August and nobody has run: how many of the 399 approved Instagram accounts are already professional. Under Instagram's conversion cost (a private account must go public), that number is the difference between a flow most clippers can complete and one most will not.

## CONTRADICTIONS, RESOLVED RATHER THAN AVERAGED

1. **BL-722 versus BL-767 on the Facebook Page.** Both partly right: no Page on the **Instagram Login** path, Page **required** on the Facebook Login path. The vendor's path is UNVERIFIED. The brief also mis-states BL-722, which concluded a Page is not required rather than that it may be.
2. **BL-770's non-existent bulk endpoint.** Refuted. The route is singular and exists (401 versus a 404 control). The path name was wrong on our side.
3. **My bought-view counts against BL-771's.** BL-771 reported 206 rejections, Instagram 58.3%. A narrow match (`bought`/`botted`) gives **128** today and a broad one (`bot`/`bought`) gives **181** with Instagram at **60.2%**. **The share reproduces; the absolute count does not**, and I have not reconciled the residual, so treat the shares as sound and the totals as match-dependent.
4. **Vendor import cap, flat versus per account.** `import-posts.md` says a flat "Free: 5 posts/month"; the pricing page says "per social account". The spec settles it: `limitPerSocialAccount`, one bucket per connected account.
5. **Instagram `shares`.** Platform page says Reels only, changelog 2026-03-16 says fixed for all post types. **Unresolved. Measure it.**
6. **Instagram is "worth more".** True on the last 30 days ($2,284.94 versus $847.18) and false all-time ($3,551.32 versus $4,718.52). Both stated.

## WHAT COULD NOT BE ESTABLISHED

**No analytics field has ever been observed from this vendor, for any platform.** Everything in PART 1 is documentation. Beyond that: the Instagram post-level raw payload shape, and therefore whether Instagram watch time is obtainable at all through this vendor; whether IG post raw carries any completion or total-watch-time metric; whether per-post IG demographics, profile visits or follows exist; whether personal IG accounts can connect (the vendor never states it either way); whether Story analytics return; whether imported IG posts get the same raw payload as native ones; whether an analytics-only read counts against the import cap; the price of raw-analytics enablement, imported-post refresh and sub-24h refresh, all three sales-gated with no public number; which login path the vendor implements; whether Meta treats a CPM payout decision as an "eligibility determination" under 3.a.ii; whether Meta construes an unlink as a deletion request; whether Creator accounts differ from Business accounts in any returned field; and **the share of our 399 approved Instagram accounts already on a professional account**, which is the deciding number and is unmeasurable from our schema because `followerCount` is NULL on all 399 and no account-type field exists.

## SAFETY AND DISCLOSURE

READ ONLY, one document, on `checkpoint/BL-781` from `origin/main` `72f05cec`. **No code, config, schema or data change; no account connected; no payment details entered; no paid plan started; nothing authorised.** No vendor write call was made: the only vendor requests were unauthenticated `GET` probes for route existence and public documentation fetches. Every capability, pricing and terms claim carries the vendor's or Meta's own URL, and everything unexercised is marked UNVERIFIED. Nine read-only `SELECT`s ran through `scripts/run-select.js` against production, every timestamp cast `::text` against DB `now()`; no write, no money, no schema, no cron touched. No handle, caption, wallet address or email appears above; clipper identifiers are counts only. The 6 money files, `tracking.ts` and `campaign-era.ts` are untouched — this branch's diff is exactly one new markdown file. No Apify actor was run and no API key was logged, printed or committed. Four subagents ran, all read-only, none permitted to write a file or connect an account, and their claims are reconciled against primary sources above with contradictions reported rather than dropped. Worktree removed. No dashes as bullets. **Nothing here may auto-reject a clip or be shown to a clipper: BL-518 and BL-521 stand, and PART 5 makes the human-review-only rule a compliance control as well as a product one.**

**Rollback:** delete branch `checkpoint/BL-781`. It contains one document and touches nothing.
