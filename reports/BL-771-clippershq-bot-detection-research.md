# BL-771 — detecting bought views on TikTok: what the evidence actually supports

**2026-08-11 · DB now() = `2026-08-11 12:04:25.065325+00` · RESEARCH ONLY. READ ONLY.**
No code, config, schema or data change. No scoring system designed and no detector built; that is the next round's job and this round exists to tell it what is worth building. Branch `checkpoint/BL-771` at `9d285c8c` with a clean tree, worktree removed at the end. Every DB read through `scripts/run-select.js`, which refuses any write keyword before connecting.

Every claim below is either cited to a primary source with a URL, measured by me on live production data with the query stated, or explicitly marked **UNVERIFIED**.

---

## FIRST, A CORRECTION TO THE BRIEF'S SOURCES

The brief asked me to read `BL-769-clippershq-bundlesocial-pilot`, `BL-770-clippershq-bundlesocial-live`, `BL-768` and `BL-767`. **None of those exist.** `reports/BL-767.md` through `BL-770.md` are real files but belong to a different project sharing the repository; their subjects are Spotify seed playlists, junk-address sweeps, CSV export suppression and lead-pipeline gates. **There is no BundleSocial pilot anywhere in the ClippersHQ series**, and the highest ClippersHQ report before this one is BL-766.

The reports that actually carry what the brief attributed to them are **BL-726-clippershq-tiktok-api-matrix** (the definitive field list and the verbatim terms clause), **BL-723-clippershq-tiktok-analytics-pilot**, **BL-722-clippershq-creator-analytics-scope** and **BL-724-clippershq-tiktok-app-review-prep**. I read those instead. `R-5`, `BL-664`, `BL-650` and `BL-599` all exist as plain-numbered files and are genuinely ours.

One consequence matters immediately: **no TikTok API call has ever been made.** BL-723 records that the infrastructure was built and is waiting on app approval. Every analytics field discussed below is a field we could obtain, not one we have.

---

## PART 0 — THE CONSTRAINTS ANY SIGNAL MUST RESPECT

### Constraint 1: no cross-creator aggregation, verbatim

TikTok's Accounts API documentation, under Prohibited Uses:

> "Extract reports of TikTok profiles and posts from authorized creators' accounts, and use the aggregated data to develop a self-built affiliate influencer marketing program (such as creator discovery and ranking), instead of using the TikTok One platform or API."

And: *"TikTok reserves the right to revoke a developer's Accounts API access at any time without prior notice."*

**What this kills.** Any signal of the form "this clip's watch time versus the median watch time of comparable creators" is creator ranking built on aggregated authorized-creator data. **BL-599 must not be rebuilt on this data.** BL-599 is live today, fires on 3.2% of clips (87 of 2,707), and computes like-rate against peer bands grouped by platform and niche. It is lawful *only* because it runs on our own scraped view and like counts, not on API data. The moment its inputs become TikTok API fields it becomes the prohibited shape.

**What survives.** A per-clip absolute test, and a within-creator longitudinal test comparing a clipper's suspect clip against that same clipper's own earlier clips. The second is not merely permitted, it is the strongest design in the academic literature (see PART 5).

### Constraint 2: the platform's existing automated signals have no predictive power, and I re-measured both

R-5 measured `fraudScore` at 19.0% rejection for score 0 and 19.5% for score 40-plus, concluding verbatim: **"`fraudScore` has no predictive power"**. I re-derived it today on all reviewed live clips:

| fraudScore band | clips | rejected | rejection rate |
|---|---|---|---|
| 0 | 3,710 | 689 | **18.57%** |
| 1 to 19 | 831 | 92 | 11.07% |
| 20 to 39 | 550 | 112 | 20.36% |
| **40+** | 196 | 28 | **14.29%** |

The highest-score band rejects *less often* than the zero band. The difference is not significant (z ≈ 1.66, p ≈ 0.10), so the honest statement is that the bands are indistinguishable, which is R-5's conclusion reproduced eleven months later on a larger sample.

Sharper still, because it tests the score against the thing it is supposed to detect rather than against rejection in general:

| cohort | clips | mean fraudScore | median | share scoring ≥ 50 |
|---|---|---|---|---|
| human wrote "bought" or "botted" | 206 | 13.18 | 10.0 | **2.43%** |
| human approved | 4,361 | 6.93 | 0.0 | **2.41%** |

At **50**, the threshold the alerting code actually acts on, the score fires on 2.43% of clips a human called bought and 2.41% of clips a human approved. **It is uninformative at the only threshold that matters.**

**A second existing signal, not named in the brief, is worse.** `maybeAlertOwnerOfApprovedBot` (`src/lib/bot-alert.ts`, BL-264/265, silent and owner-only since BL-518) has marked **535 clips**. Of those, **49 were rejected and 486 approved: precision 9.2%**, against a base rejection rate of **18.51%**. The alerter is roughly half as likely to be right as flagging a clip at random. Its recall on the 206 human-judged bought clips is **22.3%**.

**A third, the creator-scan account scanner** (BL-336 to BL-371, live, 250 scans across 246 accounts, 65 on TikTok, most recent today, 149 credits spent) shows mean `layer1Score` of **0.0** on the five scanned accounts that later had a bought-view rejection versus **1.2** on the 241 that did not, with **zero** non-zero scores in the accused group. On this sample it is not merely uninformative, it points the wrong way. The sample is small and I will not overclaim from five accounts, but it is not evidence of value.

**So the platform has three automated fraud signals in production and not one of them beats chance.** That is the bar the next round has to clear.

### Constraint 3: the human baseline is 0.77 percent, and it sets a brutal threshold

BL-664, verbatim: **"The measured human (reviewer) overturn rate is 1.54% (2 of 130 reviewer rejections, 2026-06-01 to 2026-07-22), and 0.77% if the 6-minute misclick is excluded"**.

Read as a quality bar: of the clips a human decided to reject, roughly **one in 130** was later judged wrong. For an automated flag to be *better* than the humans it would replace, it must be wrong on fewer than 0.77% of the clips it flags. **That is a precision requirement above 99.2%.** Hold that number; PART 4 measures what we can actually achieve against it.

### Constraint 4, which the brief did not name but which decides the round

**Nothing may auto-reject and no clipper may see machine suspicion.** BL-518 removed every automatic system that could change a clip's status; BL-521 is stated verbatim in BL-722 as **"A clipper never sees a machine's suspicion."** Every signal below is therefore a ranking aid for a human reviewer, never a verdict.

---

## PART 1 — HOW BOUGHT VIEWS ACTUALLY WORK

### The counting rule is the whole economy

TikTok's own organic definition, from the API for Business documentation:

> `video_views`: "The number of times viewers watched your video post." **"Counts when playback duration >0 and the playback is the first playback in an impression session."**
> https://business-api.tiktok.com/portal/docs?id=1762228421622786

**There is no minimum duration.** Any nonzero playback counts. This single sentence determines everything: a purchased view costs the seller effectively **zero watch time**, so an operation optimising for the view counter produces near-floor `average_time_watched` and near-zero `total_time_watched`. It also explains why fraud is engineered precisely to the counting rule elsewhere: on YouTube, where the threshold is 30 seconds, Kuchhal and Li found view-fraud services force viewers to watch **exactly ≥30 seconds** ([WWW 2022](https://faculty.cc.gatech.edu/~frankli/papers/kuchhal-www2022.pdf)).

TikTok maintains **three different counters** and pays on the strictest. Creator Rewards "Qualified Views" require a From You feed impression, **≥5 seconds watched**, uniqueness, an eligible country, and explicitly exclude fraudulent, paid, promoted and artificial views ([TikTok Creator Academy](https://www.tiktok.com/creator-academy/article/monetization-creativity-program-qualified-view)). The precedent that public and paid counters are policed differently is measured: on YouTube the public counter discarded ~93% of injected fake views while the **monetised counter accepted 82% of them** (Marciel et al., [WWW 2016](https://arxiv.org/abs/1507.08874)).

**ClippersHQ pays on the public counter, which is the loosest number TikTok publishes and the one TikTok itself declines to pay on.**

### The delivery mechanisms, and what each leaves in analytics

**Request-level view bots.** Public open-source implementations issue HTTP requests against TikTok or booster endpoints with a view-count parameter, explicitly "no selenium" ([xtekky/TikTok-ViewBot](https://github.com/xtekky/TikTok-ViewBot), [Zefoy bots](https://github.com/plowside/Zefoy_TIKTOK_BOT)). No app process, no rendering, no audio, no logged-in account, **no watch duration at all**. Every seller page confirms the shape: no password or login required, only the video URL. This is the cheapest and therefore commonest class.

**Emulator farms.** Practitioner forums claim TikTok flags emulated environments regardless of behaviour. Self-reported, contradictory between threads, no measurement. **UNVERIFIED.**

**Real-device farms.** Documented by police actions and a breach: Thailand 2017, 476 phones and ~347,200 SIM cards ([SCMP](https://www.scmp.com/news/asia/southeast-asia/article/2098167/thai-police-raid-wechat-click-farm)); Brazil, December 2025, 300+ wall-mounted phones autoplaying to inflate YouTube views; and the a16z-backed Doublespeed, where a breach exposed **1,000+ smartphones and 400+ TikTok accounts** ([404 Media, Dec 2025](https://www.404media.co/hack-reveals-the-a16z-backed-phone-farm-flooding-tiktok-with-ai-influencers/)). Genuine app on genuine hardware with a real sensor surface and a live audio path. **This is the class that is hardest to separate from organic, and it is the expensive one.**

**Incentivised humans.** Crowdturfing routes tasks to worker pools at **$0.20 to $1 per task** (Wang et al., [WWW 2012](https://arxiv.org/abs/1111.5654)). TikTok ran its own version: TikTok Lite Rewards paid points for watching, and the European Commission opened DSA proceedings in April 2024, with TikTok committing to permanent EU withdrawal ([EC](https://digital-strategy.ec.europa.eu/en/news/commission-opens-proceedings-against-tiktok-under-dsa-regarding-launch-tiktok-lite-france-and-spain)). Real humans, real devices, real watch time. **No analytics signal separates a paid human viewer from an unpaid one.**

**Proxied sessions.** The 911 S5 botnet sold **~19 million residential exit IPs across 190+ countries, including 613,841 US IPs** ([FBI IC3](https://www.ic3.gov/PSA/2024/PSA240529)). The FBI's 2026 advisory states buyers "can choose which country they would like the IP address from, **down to the city and state**" ([IC3, Mar 2026](https://www.ic3.gov/PSA/2026/PSA260312)). Academic measurement puts the market at 6M+ residential IPs across 230+ countries, largely on compromised hosts (Mi et al., [IEEE S&P 2019](https://www-users.cse.umn.edu/~fengqian/paper/rpaas_sp19.pdf)).

**Ads arbitrage.** Mechanically available: TikTok's video-views objective buys plays and Spark Ads attribute the resulting engagement to the underlying organic post. So a seller could lawfully inflate the public counter with genuine TikTok-served impressions. **I found no published investigation documenting any reseller actually doing this. UNVERIFIED**, and worth noting that TikTok's own Qualified Views excludes paid and promoted views, so this route inflates the public number while being excluded from TikTok's payout basis.

### Prices, and what the ladder tells a reviewer

| service | price per 1,000 | source |
|---|---|---|
| TikTok views, generic | **below €0.09** | [IMDEA, Computers & Security 2022](https://networks.imdea.org/a-study-analyses-fake-interaction-services-on-social-media/), 86 SMM panels, 2.8M service entries |
| TikTok views, generic | **$1.40** (cheapest of five platforms) | [Surfshark, Aug 2026](https://surfshark.com/research/chart/fake-engagement-on-social-media) |
| TikTok views, geo-targeted | **$0.27** vs **$15.00** | socialfansgeek vs socialnovo, same week |
| TikTok shares | $68 | Surfshark |
| TikTok comments | **$140** | Surfshark |

Two things follow. **The geo-targeted price is contested by a factor of 55** between two vendors selling a nominally identical product in the same week; at least one is not doing what it claims. And **comments cost roughly 100 times what views cost**, because a view needs no account at all, a like needs an account, a comment needs an account that can pass text review, and a follower needs an account that persists. **That price ladder is why ratio structure discriminates better than any absolute count.**

### "High retention" does not mean what a reviewer would assume

Every vendor read advertises retention as **durability of the counter**, not watch time: "Permanent Count", 30-day refill "if your view count drops significantly", replacement in 1 to 5 days. **A refill guarantee is a vendor admitting that platforms delete purchased views.** No primary source gives a price premium or a measured watch-time percentage for "high retention" TikTok views; every circulating figure is affiliate-blog marketing. **UNVERIFIED.**

### Pods, likes, comments and followers leave different traces

Pods are **real logged-in humans acting manually**, which is why they evade bot-shaped detection; measured pod participation produced a mean **5× increase in comments** and ≥2× interaction lift on the same users' non-pod control posts (Weerasinghe et al., [WWW 2020](https://dl.acm.org/doi/10.1145/3366423.3380256)). Like farms split into a bursty class (**700+ likes in four hours**) and a stealthy class that deliberately drip-feeds and evaded Facebook's detection (De Cristofaro et al., [IMC 2014](https://arxiv.org/abs/1409.2097)). Purchased followers carry an account-level signature, high unfollow entropy, that views cannot.

### TikTok's own enforcement, and a conspicuous absence

TikTok reports preventing **36B+ fake likes** and removing 379M+ more, preventing 15B+ fake follow requests and removing 207M+ fake followers in H1 2024 ([TikTok Newsroom](https://newsroom.tiktok.com/en-eu/how-tiktok-counters-deceptive-behaviour)). **TikTok publishes no fake-view figure at all.** Likes, follows, followers, accounts and videos are covered; views are absent from the transparency series. For a company that pays per view, that absence is itself the finding.

Independent measurement disagrees with the implied efficacy: NATO StratCom spent €279, bought **114,061 engagements including 93,009 views**, and found **92% still live after four weeks**, with purchased views persisting longest ([StratCom](https://stratcomcoe.org/publications/download/Social-media-manipulation-2021_2022-F.pdf); named-org research, not peer-reviewed).

---

## PART 2 — THE SIGNALS, RANKED BY EVASION COST

**I tested every signal computable from what we hold today against 206 human "bought" labels.** The labels are weak (they are one reviewer's judgement, and BL-664's 0.77% measures consistency, not correctness), and I say so rather than dressing them up as ground truth. But they are the only labels that exist, and the results are unambiguous.

### What we actually hold: nothing

A column scan of `clips` and `clip_stats` for anything matching duration, watch, retention, reach, impression, audience or country returns **0**. We store views, likes, comments and shares over time, and nothing else. Every richer field below would be new.

### Measured performance of every count-only signal

Population: TikTok clips, approved versus rejected-with-a-bought-views reason.

| signal | operating point | recall | false-positive rate | **precision** |
|---|---|---|---|---|
| `fraudScore` (live) | ≥ 50 | 2.4% | 2.4% | ~ base rate |
| bot alerter (live) | fires | 22.3% | — | **9.2%** |
| like-rate | < 1.0% | 23.7% | 13.5% | **20.0%** |
| like-rate | < 2.0% | 50.0% | 28.1% | **20.2%** |
| like-rate | < 3.0% | 65.8% | 39.7% | 19.1% |
| late fill (< 20% of peak by 24h) | | 61.1% | 39.0% | **13.8%** |
| late fill (< 30%) | | 69.4% | 46.4% | 13.3% |
| view retraction | any | **0.0%** | 12.9% | **0.0%** |
| payout-ceiling clustering | ≥ 90% of cap | **0.0%** | 0.3% | **0.0%** |

**The required precision is 99.2%. The best achieved is 20.2%. Every count-only signal is roughly two orders of magnitude short.**

### Two literature-endorsed signals that fail here, and why that matters

**Retroactive view correction fails.** This is the strongest signal in the published literature and the one I most expected to work, because it needs nothing but a polled counter, which we already have. Castaldo et al. ([Scientific Reports 2024](https://www.nature.com/articles/s41598-024-63649-w)) built an entire peer-reviewed study on it: across 270,133 YouTube videos, **78.5% received view corrections**, arriving in batches, with **90% of corrections after a video had already accrued 80% of its final views**. Kuchhal and Li independently found the median fraud-promoted video went **net-negative within a week**.

Measured on our TikTok clips: **zero of the 60 human-labelled bought clips show any retraction**, against 12.9% of approved clips. The signal does not fire on the population it is supposed to catch, and part of the 12.9% is our own scraper noise (BL-751 and BL-753 documented a fabricated-zero defect producing exactly this shape). **The literature is YouTube-centric, and on this evidence TikTok does not retract the way YouTube does.** That is a genuinely useful negative and it is the reason this round exists.

**Payout-ceiling clustering fails.** The best practitioner account I found is Peter Claridge on running a Whop clipping campaign: **$1,500 spent, ~845,000 views, assessed as "99.999% bot views"**, with the tell being structural rather than statistical, verbatim: *"every video coincidentally hits the EXACT amount of views needed to get the maximum payout per video. And then? The views just stop."* When he cut the cap from $100 to $25, *"suddenly none of the videos got more than 30k views"* ([peterclaridge.com, Sep 2025](https://peterclaridge.com/should-you-use-whop-com-to-promote-your-saas-product)).

Measured here: the median clip needs **500,000 views** to reach its per-clip cap, and **0.3% of approved clips and 0.0% of bought-labelled clips** get within 90% of it. **Our caps are set so far above achievable performance that they exert no gravity at all.** The tell is real; it does not apply to us. It would apply instantly if the owner ever lowered per-clip caps to a level clips actually reach, and that is worth knowing before he does.

### The one shape that did separate, and its evasion cost

The velocity shape separates, in the **opposite direction to the folklore**:

| | approved (n=1,017) | rejected as bought (n=57) |
|---|---|---|
| median % of peak reached by 24h | **78.1%** | **31.0%** |
| median % of peak reached by 72h | 92.5% | **98.4%** |
| still climbing (<50% of peak) after 24h | 31.0% | **54.4%** |

Organic clips are **front-loaded with a long thin tail**. The bought-labelled clips arrive **late and then finish hard**: a third of their views by 24 hours, essentially all of them by 72. That is the signature of **drip-fed delivery over a fixed window**, and it matches the supply side exactly, where one vendor offers **six selectable delivery speeds from ASAP to 192 hours**.

**Evasion cost: near zero.** The vendor already sells the knob. De Cristofaro et al. measured stealthy farms deliberately drip-feeding to mimic ad campaigns and evading detection while crude farms were terminated. A buyer defeats this by choosing a different delivery speed, at no extra cost. **It has a real effect size and no evasion cost, which is why its precision is 13.8%.**

### The signals we cannot compute yet, ranked by evasion cost

These require the API for Business. I rank them by what a buyer would have to pay to defeat them, which is the ranking the brief asked for.

**1. Watch time per view. Highest evasion cost.**
`total_time_watched` is the only unambiguous absolute TikTok exposes, documented as "The amount of time viewers spent watching your video post, in seconds." Because a view counts at playback >0 with **no minimum**, a cheap purchased view contributes a view and almost no seconds. To defeat it a buyer must make each fake viewer actually watch, which converts the cheapest class of supply (request-level bots, sub-$1.40 per 1,000) into the most expensive (real devices or paid humans at **$0.20 to $1 per task**). **That is a 100× to 700× cost increase, and it is the only signal in this report with that property.**
Caveat, and it is important: **no published study reports an AUC for watch-time features against purchased TikTok views. UNVERIFIED as a calibrated detector; sound as a mechanism.**

**2. Impression-source mix. High evasion cost, unmeasured.**
Enum values are exactly `For You`, `Follow`, `Sound`, `Personal Profile`, `Search`, `Others`, `Direct Message`. Purchased traffic cannot plausibly be attributed to For You at scale, because For You placement is TikTok's own ranking decision and not something a seller can buy. **TikTok publishes no definition of any individual enum value and no benchmark distribution**, so any "organic videos get 70 to 90% For You" figure is third-party and must not be hard-coded. **UNVERIFIED for TikTok.**

**3. Second-by-second retention curve. High evasion cost.**
`video_view_retention` returns `{second, percentage}`. A farm that watches a fixed duration produces a cliff at that second; Kuchhal and Li showed fraud is engineered exactly to the counting threshold, so the cliff is where the rule is. Defeating it requires randomised watch durations per session, which is achievable but requires the expensive supply class.

**4. Views per reached person.** `video_views / reach` needs no guessed denominator. TikTok publishes no bound on it. Cheap to compute, unmeasured.

**5. Audience geography. Lowest evasion cost of the API fields.** See PART 3.

### Two traps in the fields themselves

**The denominators of `average_time_watched` and `full_video_watched_rate` are undocumented.** TikTok says only "The average time viewers spent watching your video post" and "The percentage of viewers who finish watching your video post". Whether the denominator is views, reach, unique viewers or impressions is **not stated anywhere**. A signal built on a guessed denominator is worthless. **Build on `total_time_watched`, which is an unambiguous absolute.**

**`video_views` mixes organic and paid.** Verbatim: "represents a total metric, encompassing both organic and paid activities." The only marker is `is_ad`, which flags "being used in an ad", not "was boosted". **A clipper who runs TikTok Promote on his own clip inflates the number we pay on, and the API will not cleanly tell us.**

**And a null trap.** If a video has been inactive for more than 7 days, `reach`, `full_video_watched_rate`, `total_time_watched`, `average_time_watched`, `impression_sources` and `audience_countries` all return **unavailable**. A rule reading null as zero fires on every stale clip. The MRC standard says this explicitly for the ad industry: missing data must be classed **unmeasurable, not invalid**.

---

## PART 3 — THE US-TARGETED CASE

The owner's specific fear is a clipper who buys US-geotargeted views so that `audience_countries` looks legitimate. Here is the honest answer.

### The geography is a bundle, and a proxy buys one element of it

TikTok's own US privacy policy states it derives location from:

> "Location information about your approximate location based on your device and network information, such as **SIM card region, IP address, and device system settings**."
> https://www.tiktok.com/legal/page/us/privacy-policy/en

A residential proxy controls the **IP address**. It does not control the SIM card region or the device system locale, which are set on the handset. A US-exit proxy in front of a device farm carrying non-US SIMs and non-US locales is **internally inconsistent by construction**. Whether TikTok resolves that inconsistency toward the IP or toward the device is not documented, and **we cannot see any of these fields anyway** — we would see only the resulting country percentages.

### The one controlled experiment says the geo claim is often not honoured at all

De Cristofaro et al. ran honeypot pages and bought likes with a US-only request. One farm delivered likers **"based in Turkey, regardless of whether we requested a US-only campaign"**, while legitimate Facebook ad campaigns delivered **87 to 99.8% of likes from the intended region** ([IMC 2014](https://arxiv.org/abs/1409.2097), extended [TOPS 2017](https://arxiv.org/abs/1707.00190)).

The same work found fake-account prevalence is **lower in the US and UK and higher in developing markets**, which is precisely why a "US views" order is the order most likely to be filled out of region. The $55-fold price disagreement between two geo-targeting vendors in the same week points the same way: the cheap end is almost certainly not doing what the expensive end claims.

**This is a 2014 Facebook result. No published experiment has purchased geo-targeted TikTok views and measured the resulting audience-territory breakdown. UNVERIFIED for TikTok in 2026, and it is the single most obvious experiment for this platform to run in-house.**

### What still gives away a US-targeted buyer, and what does not

**Survives a well-funded buyer: nothing, with one qualification.**

**Watch time does not survive money, it survives *cheapness*.** The reason watch time works is that the cheap supply class cannot produce it. A buyer who pays for real devices or paid humans in the United States produces genuine US IPs, genuine US SIMs, genuine US locales, genuine For You-adjacent behaviour if the accounts are aged, and genuine seconds watched. **At that point the analytics are not lying: the views really were delivered by real people in the United States who really watched.** There is no field left that separates a paid American viewer from an unpaid one.

**So the truthful answer to the owner's sharpest question is: a sufficiently expensive US-targeted purchase is undetectable from analytics alone, and this platform should not promise itself otherwise.** What the signals do is raise the price. The cheap attack (sub-$1.40 per 1,000, no watch time, wrong geography half the time) is catchable. The expensive attack (real US devices or paid US humans at $0.20 to $1 per action, three orders of magnitude dearer) is not, and it is also no longer economic against a CPM-based payout unless the CPM exceeds the cost of the fraud.

**That last clause is the actual defence, and it is commercial rather than technical.** At a clipper CPM of $0.50, one thousand purchased views earn $0.50. Cheap bot views cost $0.09 to $1.40 per thousand, so the trade is marginal to profitable. Paid-human views cost $200 to $1,000 per thousand. **The economics already forbid the sophisticated attack; only the cheap one pays, and the cheap one is the one watch time catches.**

**What partially survives:** a mismatch between a clip's US audience and the creator's *own* normal audience, computed within that one creator across their own clips. That is permitted under Constraint 1, needs no peer corpus, and is the design the literature endorses. It is defeated by a buyer who targets consistently from the first clip, and it cannot distinguish a clipper who legitimately grew a US audience.

**What does not survive at all:** engagement rate against "normal US behaviour" (requires a cross-creator corpus, prohibited), and view-velocity shape (the vendor sells the delivery-speed knob).

---

## PART 4 — WHAT THE DATA CANNOT PROVE

### The false-positive traps, each of which looks bought

**A genuinely viral clip.** Castaldo et al. found corrections land on 78.5% of videos and that videos corrected *later* ended up **3× more popular** — the anomaly correlates with success. Any rule keyed on "unusual growth" punishes the best clippers first.

**A clip the creator promoted with their own paid ads.** `video_views` explicitly mixes organic and paid, and `is_ad` does not reliably mark it. This is indistinguishable from bought views on every count-based signal.

**A niche or non-English audience.** Aspire is the only vendor that publishes its own false-positive causes, and they are: **audience outside the US, a creator who travels, low story impressions** ([Aspire help](https://help.aspireiq.com/en/articles/6027302-what-is-audience-authenticity)). Our reviewers' existing heuristic is exactly this shape: a live rejection reason reads *"botted and bad audience at least 40% first world countries"*. **The current human method rejects on geography, which is the one signal a US-targeting buyer defeats and the one that most punishes honest clippers with non-Western audiences.**

**A clipper whose audience genuinely is US-based.** Unfalsifiable from analytics.

**A short clip with naturally high completion.** Completion rate is mechanically inverse to duration and TikTok publishes no benchmark by length, so any fixed threshold penalises short clips or excuses long ones.

**A stale clip.** Six analytics fields go unavailable after 7 days of inactivity. Read as zero, they look like total fraud.

### What false-positive rate would make automation worse than humans

The human baseline is **0.77% of rejections later judged wrong**. An automated flag beats it only at **precision above 99.2%**.

Measured on our own data, at the best available operating point, **precision is 20.2%**. Four out of every five clips the best count-only signal flags are clips a human approved. **The best signal we can compute today is about 99 times short of the bar.**

### In honest clippers wrongly accused per month

Volume, measured today rather than taken from the brief: **1,703 clips in the last 30 days**, of which **306 are TikTok** and **144 exceed 2,000 views**. The brief's ~2,300 figure is July's and is stale by roughly 26%.

| rule | false-positive rate | honest TikTok clips wrongly flagged per month |
|---|---|---|
| like-rate < 2.0% | 28.1% | **≈ 40** |
| late fill < 20% by 24h | 39.0% | **≈ 56** |

**Forty to fifty-six honest clippers accused every month, against a human process that errs roughly once per 130 rejections.** If either rule auto-rejected, it would be a catastrophe; BL-518 already forbids that. Even as a *ranking* aid, a queue where four in five entries are innocent will be ignored within a fortnight, which is how the existing bot alerter came to have 535 marks and 9.2% precision.

**One thing the data does prove, and it is the most actionable finding in the round.** Bought-view rejections are **206 across 991 total rejections, 20.79%**, the largest identifiable category, spanning **40 clippers**, still happening (most recent this morning). But they are **highly concentrated: 8 clippers account for 149 of the 206, or 72.3%**, and 18 clippers were accused exactly once. **This is a repeat-offender problem, not a diffuse one**, and per-clipper history is computable today from our own data with no API, no vendor and no new field.

And a scoping fact the brief did not anticipate: **Instagram is 58.3% of the bought-view problem** (120 rejections, 24 clippers) against TikTok's 29.1% (60 rejections, 13 clippers). TikTok is only **18% of submissions**. A perfect TikTok detector addresses under a third of the measured problem.

---

## PART 5 — WHAT OTHERS HAVE ACTUALLY BUILT

### The influencer-vetting sector publishes nothing checkable

I examined HypeAuditor, Modash, Traackr, Upfluence, CreatorIQ, Later/Mavrck and Aspire. **Zero of the seven publish a feature list with weights, a threshold, a labelled test set, or a false-positive rate.**

HypeAuditor's anchor claim, "detect 95.5% of all known fraud activity with a mean error rate of 0.73%" ([methodology page](https://hypeauditor.com/collect-analyze-influencer-data/)), has no test set, no labelling protocol, no confusion matrix and no independent reproduction. Note the tautology: 95.5% of all **known** fraud. **UNVERIFIED, and unfalsifiable by construction.** Traackr is not an independent second opinion; its Audience Quality is built in partnership with HypeAuditor and reuses the same score.

The two useful exceptions are honest about their limits. **Modash** publishes base rates (20 to 30% fake for large creators, 10 to 20% under 50K) and the hard constraint that private follower lists make calculation impossible. **Aspire** publishes its false-positive causes and states plainly: *"manually vetting is still important and should ultimately be the basis of your decision."*

### The advertising industry has a real published standard, and its design choices all transfer

The **MRC Invalid Traffic Detection and Filtration Standards Addendum** ([PDF](https://mediaratingcouncil.org/sites/default/files/Standards/IVT%20Addendum%20Update%20062520.pdf)) is the document this round was looking for.

It splits **GIVT**, "traffic identified through routine means of filtration executed through application of lists or with other standardized parameter checks", from **SIVT**, which "require advanced analytics, multi-point corroboration/coordination, **significant human intervention**". **Human review is written into the definition of the sophisticated class.** It requires that "empirical evidence shall exist supporting specific invalid traffic detection parameters" plus "identification/internal reporting of false positives and negatives", sets **5% as the materiality threshold** for false positives, and mandates disclosure of **"decision rates"**, the share of impressions where enough signal existed to decide at all. The [2024 interim update](https://mediaratingcouncil.org/sites/default/files/Standards/2024_IVT_Interim_Updates_FINAL.pdf) instructs measurers to "take care to not erroneously invalidate traffic with missing information ... and instead consider this **unmeasurable** for IVT."

The MRC's own April 2025 statement is blunt: on determining SIVT, **"it's impossible to determine this with evolving sophistication of IVT techniques"** and **"It's very likely a material amount of SIVT goes undetected."** It also notes the standards **discourage** pre-bid blocking, preferring retrospective correction.

**So the consensus is not that everything is probabilistic. It is that list-matching is definitive and everything beyond list-matching is probabilistic, human-reviewed, and corrected after the fact rather than blocked up front.** That distinction should carry the next round's design.

### The academic position

Detection accuracy is high **only where viewer-level data exists**: 0.99 AUC on Twitter follower features (Cresci et al., [DSS 2015](https://arxiv.org/abs/1509.04098)), 0.99 AUC on IP-entropy at Tencent, >99% precision on lockstep graph clustering (SynchroTrap, [CCS 2014](https://users.cs.duke.edu/~xwy/publications/SynchroTrap-ccs14.pdf)). **We have none of that and never will**, because creator analytics expose aggregates, not viewers.

Two cautions are directly on point. **LOBO** ([ACSAC 2018](https://arxiv.org/abs/1809.09684)) found a classifier scoring >97% in-distribution **failed to generalise to unseen bot classes**. Rauchfleisch and Kaiser ([PLOS ONE 2020](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0241045)) showed Botometer is threshold-sensitive and language-dependent, with studies "unknowingly counting a high number of human users as bots". Cresci et al. ([arXiv 2023](https://arxiv.org/abs/2303.17251)) names the reasons vendor accuracy figures are untrustworthy: information leakage, overfitting to evaluation datasets, structurally biased datasets, and recommends pivoting from classifying accounts to **detecting coordinated behaviour**.

**There is no peer-reviewed TikTok view-fraud detection study, no public TikTok bot-detection tool, and no labelled TikTok purchased-view dataset.** Multiple 2024 to 2025 papers state this explicitly. **This is established by absence, and it means nobody has solved the problem this round is about.**

### The one design in the literature that fits our constraints exactly

**The Pod People** (Weerasinghe et al., [WWW 2020](https://dl.acm.org/doi/10.1145/3366423.3380256)) analysed 1.8M Instagram posts and 432 Telegram pods, and its causal design compares **a creator's manipulated posts against that same creator's own control posts**, reaching AUC 0.94 for comment-and-like pods. **No peer corpus, no viewer identities.** That is precisely the shape TikTok's terms permit and precisely the data we would have.

### When these systems are wrong

Adalytics (March 2025) found ads served to bots that **declare themselves** in their user agent and appear on the IAB and TAG lists: URLScan.io bots classified as human 77% of the time. **The dominant industry response to independent testing was legal and PR rather than data**: DoubleVerify published rebuttals and a watchdog was threatened with a defamation suit.

And the gap that matters most to a platform that pays people: **no influencer-vetting vendor publishes a false-positive rate, a dispute process, or a creator-facing appeal.** YouTube, by contrast, runs a formal invalid-activity appeal, withholds earnings and adjusts analytics retroactively, but **does not tell the creator which views were judged invalid** ([YouTube Help](https://support.google.com/youtube/answer/14340193)).

---

## PART 6 — THE VERDICT

### Ranking every signal by evasion cost against implementation cost

| signal | evasion cost | implementation cost | measured or projected value | verdict |
|---|---|---|---|---|
| **Watch time per view** (`total_time_watched / video_views`) | **Very high**: converts $1.40/1,000 supply into $200 to $1,000/1,000 | High: needs API for Business, needs a registered company | Mechanism established by TikTok's own view definition; **no published AUC** | **Build, when the API is reachable** |
| **Per-clipper history** (prior bought-view rejections) | High: requires a fresh account and losing all standing | **Zero**: our own data, today | 8 clippers = **72.3%** of all 206 accusations | **Build first. Cheapest and best evidenced** |
| **Second-by-second retention curve** | High: needs randomised per-session durations | High: API for Business | Mechanism established; UNVERIFIED for TikTok | Build after watch time |
| **Impression-source mix** | High: For You placement cannot be bought | Medium once the API is live | UNVERIFIED, no published benchmark | Build as reviewer context, never as a threshold |
| **Views per reached person** | Medium | Low once the API is live | Unmeasured | Cheap addition |
| **Within-creator audience shift** | Medium: defeated by consistent targeting | Medium | Endorsed design (Pod People); unmeasured here | Worth a pilot |
| **View-velocity shape** | **Near zero**: vendors sell the delivery-speed knob | Zero: our own data | Real effect size, **13.8% precision** | **Reviewer context only. Never a rule** |
| **Like-rate versus peers** (BL-599, live) | Low | Already built | **20.2% precision** | **Do not extend to API data. Prohibited by the terms** |
| **`fraudScore`** | n/a | Already built | **Indistinguishable from chance** | **Retire or ignore** |
| **Bot alerter** | n/a | Already built | **9.2% precision, below base rate** | **Retire or ignore** |
| **View retraction** | n/a | Zero | **0% recall here** | **Theatre on TikTok** |
| **Payout-ceiling clustering** | n/a | Zero | **0% at our cap levels** | **Theatre, unless caps drop** |

### What a reviewer should see per clip, and it is not a score

Three of our automated scores are already indistinguishable from chance. **A fourth number will be ignored.** What a human needs is the handful of facts that let them decide in seconds, each shown as a raw figure with its comparison, and each honestly labelled when unavailable.

> **This clipper.** 3 previous clips rejected for bought views, most recent 6 days ago. *(Or: no previous bought-view rejections.)*
> **Watch time.** 1.2 seconds average across 48,000 views, against 9.4 seconds on this clipper's own last ten clips. *(Unavailable until the API is live.)*
> **Where the views came from.** For You 11%, Search 2%, Others 87%, against For You 74% on this clipper's own last ten clips.
> **Shape.** 31% of final views in the first 24 hours, then 98% by 72 hours, then nothing.
> **Engagement.** 0.4% like-rate, against 4.7% on this clipper's own last ten clips.
> **Audience.** United States 91%, against United States 12% on this clipper's own last ten clips.

Every comparison is **against that clipper's own history**, never against other creators. That satisfies TikTok's prohibition by construction, matches the one academic design that fits our data, and gives a reviewer something a peer percentile never could: a claim about a specific person that they can act on.

Where a field is unavailable it must say **"not available"** and never zero, per the MRC rule that missing data is unmeasurable rather than invalid. And per BL-518 and BL-521, none of it may change a status and none of it may ever be shown to a clipper.

### What the next round should build, grounded only in what this round proved

**1. Per-clipper bought-view history on the review screen.** Zero new data, zero API, zero terms risk. It is the only signal here with strong measured support: **72.3% of accusations concentrate on 8 clippers**. Build this first and it may be most of the answer.

**2. Complete the TikTok API for Business application, and treat it as the gate on everything else.** Watch time is the only signal in this report with a large evasion cost, and every path to it runs through an API that **cannot onboard individual developers**: verbatim, *"Currently, we are unable to onboard personal accounts or individual developers. If you are part of a company, please use your company website."* Until that is done, no watch-time signal exists at any price. Note also BL-723's finding that the analytics fields carry a **24 to 48 hour delay**, so a same-day payout can never see them.

**3. Run the experiment nobody has published.** Buy a small quantity of US-geo-targeted TikTok views against a control clip on an account we own, and measure what `audience_countries`, `total_time_watched` and `impression_sources` actually return. The 2014 Facebook finding that a US-only order was filled from Turkey is the closest evidence in existence and it is twelve years old and on another platform. **This is a few hundred dollars and it would settle the owner's sharpest question with our own data rather than an analogy.**

**4. Consider settling late rather than detecting harder.** Both the MRC standard and every published removal study point the same way: correct financially after the fact rather than block up front. Whop reportedly added a 24-hour payout delay after its own botting controversy. This is a commercial lever, it needs no detector, and it deserves its own round.

**5. Do not extend BL-599's peer bands to API data.** It is live and lawful on our own scraped counts. On API data it is the prohibited shape, and the penalty is revocation "at any time without prior notice".

**6. Build nothing that auto-rejects, and show a clipper nothing.** Three existing signals score at or below chance. A fourth, presented as a verdict, would wrongly accuse **40 to 56 honest clippers a month** at the precision we can actually achieve.

### The honest bottom line

**The cheap attack is catchable and the expensive one is not.** Watch time raises the attacker's cost by two to three orders of magnitude, which is the best any of this can do, and it is enough because a $0.50 CPM does not pay for $200-per-thousand human views. A well-funded buyer purchasing genuine US attention is invisible to analytics, and this platform should plan on that rather than hope otherwise. Meanwhile the largest measured slice of the problem sits on **Instagram**, not TikTok, and the most reliable predictor of a bought-view clip is **which clipper submitted it**.

---

## WHAT COULD NOT BE MEASURED, AND WHY

• **No TikTok analytics field has ever been retrieved.** BL-723 built the infrastructure and no API call has been made. Everything in PART 2's second table is projected from documented field semantics, not measured.
• **The labels are human judgements, not ground truth.** All precision and recall figures use "a reviewer wrote bought or botted in the rejection reason" as truth. BL-664's 0.77% measures reviewer *consistency*, not correctness. If reviewers systematically miss a class of fraud, every recall figure here is optimistic.
• **The velocity comparison carries a tracking confounder.** Rejected clips are forced to a 48-hour polling interval, so their series are sparser (29.4 readings against 53.0) and shorter (16.5 days against 30.7). I required a real post-`t0` reading inside each window, which removes the coverage question for the 24-hour figure; the "stops dead after 72 hours" comparison remains confounded by the shorter window and I have not claimed it.
• **The creator-scan result rests on five accused accounts.** Too small to conclude anything beyond "not evidence of value".
• **Whether geo-targeted purchased TikTok views look identical to organic US traffic is unresolved anywhere in the published literature.** The nearest evidence is a 2014 Facebook honeypot. Recommendation 3 exists to close it.
• **No published AUC exists for watch-time or impression-source features against purchased TikTok views.** The mechanism is sound and the calibration is unknown.
• **`average_time_watched` and `full_video_watched_rate` have undocumented denominators**, so any ratio built on them is a guess.

---

## VERIFICATION

Read only throughout, including all five subagents; no code, config, schema or data changed and no detector or scoring system was designed. Every claim is cited to a primary source with a URL, measured by me on live data with the query stated, or marked UNVERIFIED. The three constraints are stated and applied: TikTok's prohibition on aggregating authorized creators' data is quoted verbatim and rules out extending BL-599's peer bands to API data, every proposed signal is computable from one creator's own clip or that creator's own history, `fraudScore`'s zero predictive power is independently re-derived (18.57% against 14.29%, not significant) and a second and third existing signal are shown to be no better, and BL-664's 0.77% is converted into the 99.2% precision bar that the best available signal misses by a factor of about 99. Contradictions between sources were resolved rather than averaged: the brief's four source reports do not exist and the correct ones are named; the literature's strongest signal is shown by measurement not to transfer to TikTok; the practitioner's payout-ceiling tell is shown not to apply at our cap levels; and the folklore that bought views arrive in a spike is contradicted by our own data, which shows the opposite shape. The worktree is removed. No dashes as bullets.
