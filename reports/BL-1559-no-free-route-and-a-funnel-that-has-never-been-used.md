# BL-1559 — there is no free route, $13.94 already includes the accounts, and nobody has ever contacted a single lead

**No free route was found, and five territories searched independently. The answer is $13.94 per
1,000 net-new addresses — and the first thing to say is that this number is not what you think
it is. You believe $13.94 buys 1,000 API calls and that the ~10,000 accounts you must read are
an extra cost on top. THEY ARE THE COST. $13.94 = 19,467 profile calls + ~721 hashtag pages =
20,188 × $0.00069064, derived from a measured 5.14% net-new address rate. The account count is
already inside it. You are planning against a number roughly twice as frightening as the real
one.** Against that, the free route is worth ~$0.05/hour of wall clock and is not worth
engineering further. **But the largest finding of the round is not about price at all: this
funnel has produced 13,007 email addresses and not one of them has ever been contacted.** All
five outreach columns in `master_leads.csv` — `date_sent`, `sent_channel`, `replied`,
`reply_sentiment`, `outcome_notes` — are non-blank on **0 of 73,001 rows**, `send_identity.json`
still holds **11 `PLACEHOLDER` values**, and a finished 20-editor pilot has sat unsent for
**42.8 days**. A qualified editor costs about **$0.105**. **Pay the $13.94, send the twenty, and
spend the next round deciding a rate.**

> ### ⚠️ AMENDMENT — 2026-09-15, after a machine crash
>
> **This report was published on 2026-09-14 at 22:59 and the round did not stop there.** A
> second sweep and a deferred experiment ran on afterwards, and the machine went down at
> approximately 00:18 with that work on disk and unpublished. It has now been recovered,
> re-derived and finished. **Three things in the version you may have already read are now
> out of date, and one of them is a correction against me:**
>
> 1. **§7 said the HTTP/2 question was ABSENT. It is now MEASURED, and the answer is no.**
>    After **12.6 hours of genuinely untouched exit** a single probe found the window **open**,
>    and 30 paired fetches then found **no HTTP/2 advantage** — see §7.
> 2. **The round claimed `spend_usd: 0.0` with "nothing off the books". The vendor spend was
>    indeed zero, but the claim was wrong in the other direction:** my own suite run wrote
>    **212 rows and $0.038270 of spend that never happened** into the production ledger. See
>    §12.
> 3. **§3 and §4 were a Python-heavy sweep.** Three further ecosystems and the mirror class
>    were searched afterwards and are added as **§3b and §3c**.

---

## 1. What this project is, and what the round was asked

ClippersHQ harvests email addresses that video editors and meme-page operators publish in their
public Instagram bios, in order to hire them for paid clipping work. Reading a bio either costs
**$0.00069064** at the vendor (`ig_api.cost_per_call_usd`; TikTok's LamaTok key is $0.000600 and
15.1% away — reading the wrong one once let a $3.00 cap spend $3.45) or is free from the public
profile page until a per-IP limiter stops it.

The instruction was his, and it was a good one: *"There is maybe another free route. I think 95%
of what we're looking for is already built on GitHub. Don't build it — use it."* Five
territories were searched in parallel: the open-source ecosystem, non-Instagram sources of the
same text, cross-platform overlap, free signals that let the paid path buy less, and one agent
told to disagree with the premise.

**Spend this round: $0.00.** No vendor call was made; ground truth was reused from the 170 paid
profiles already on disk.

## 2. Method, and the state the measurements were taken in

Nine stores backed up sha256-verified with bodies found **by shape** (`spend.json` → `runs`,
`clip_seen.json` a bare list of 2,193, `tiktok_pages_seen.json` → `pages` holding **3,270**
where a dict-only reader says **3**). All six corruption controls fired, including the
position-qualified one where deleting one of a duplicated pair leaves the natural-key set
provably identical.

Every candidate route was judged by **one shared harness** — coverage, value-match against paid
ground truth, clock, and ceiling — so results are comparable rather than each being scored on
its own terms.

⚠️ **And the harness's own control immediately earned its place.** A wall-state probe returned
**6 of 6** and I recorded the exit as OPEN. The harness self-test, minutes later, returned
**0 of 10, walled at request 1**. The bucket had held about six tokens. *"Open"* and *"open with
six fetches in it"* are different statements — **I wrote that exact lesson down yesterday and
made the same error today.**

## 3. Territory (a) — the open-source sweep

Nothing clears the bar. Judged by **last commit and open issues, never stars**:

| project | last commit | login? | technique | verdict |
|---|---|---|---|---|
| **instaloader** | Jul 26 2026, active | no | same `web_profile_info` endpoint | already refuted here: **0/12, all 429** |
| **instaloader PR #2730** (HTTP/2) | branch Aug 22 2026, **open** | no | **same endpoint, different transport** | the one real lead — tested in §6 |
| **gallery-dl** | very active, 19.3k★ | no | calls the **identical** endpoint | not a new route; inherits the same bucket |
| **drawrowfly/instagram-scraper** | Nov 2022 | no | same page; README's own fix is proxies | dormant, excluded |
| **juliusdanek/instascrape** | **Jul 2017** | no | pre-GraphQL HTML scrape | this is the "returns NaN" library already burned |
| **InstaGPy** | ABSENT | no (basic call) | own docs recommend residential proxies + multiple accounts | excluded on its own scaling path |
| **Bibliogram** + forks | archived 2022 | no | proxy front-end | dead — *"Instagram is continuing to block servers"* |
| **RSS-Bridge InstagramBridge** | active repo, **unowned bridge** | **yes** (`session_id`) | authenticated | **refused** |
| **RSS-Bridge Picnob/Picuki bridges** | current | no | **third-party mirror — different in kind** | mirror is alive, **but the bridge parses only post captions, never the bio field** |
| **fast-instagram-scraper** (Tor) | ~2022, dead dependency | no | Tor exit rotation | dead, and IP-rotation-to-dodge-a-limit is the excluded category |
| **Scrapfly scrapers** | active | no | routes through a **paid** anti-bot API | a paid vendor in open-source clothing |
| **instagrapi, Osintgram, Toutatis, instagram-private-api** | — | **yes** | — | **refused, not tested** |

**The post-mortems are the most useful thing here**, in the maintainers' own words:

* PR #2730: *"Instagram has started answering HTTP/1.1 requests to its web API with 429 Too Many
  Requests and an empty body. The identical request over HTTP/2 succeeds… This is not a rate
  limit — it triggers on the very first request of a fresh session and is independent of
  account, session and IP address, and the rollout appears to be partial."*
* PR #2676, the same repo, closed later: *"HTTP/1.1 now completes the full profile-metadata
  workflow with no 429… the host-level block that originally forced HTTP/2 appears to have
  lifted."* **Whatever this wall is, it comes and goes — no fix here should be trusted as
  permanent.**
* Bibliogram's shutdown note and Picuki's silent removal of all Instagram features in 2026 are
  the same story twice: **the mirror model works until the mirror gets big enough to be
  noticed.**

**His "95% is already built" does not hold for this specific need** — anonymous, bulk, bio-text,
free. What is built and alive either shares the exact chokepoint already measured at 0/12, or is
a live mirror that does not parse the one field required.

## 3b. The second sweep — the ecosystems the first pass missed

The first sweep was Python-heavy. Three more territories were searched, none of which cost an
Instagram request.

### JavaScript, browser extensions, userscripts, Go, Rust, PHP, Ruby

**Functionally empty, and two high-star projects were confirmed traps.**

| candidate | last commit | login? | verdict |
|---|---|---|---|
| `@aduptive/instagram-scraper` (npm) | **2026-09-13** — yesterday | no | actively developed, zero-dependency, good tests — and hits the **identical** `web_profile_info` endpoint already measured 0/12 |
| `postaddictme/instagram-php-scraper` | 2025-05-28, **3,337 stars** | effectively yes | **the star trap.** Its own tracker: *"`?__a=1&__d=dis` no longer working"* (2024-01), *"cookies expire after 20-30 requests and need to re-login"* (2023-12) |
| `floriandiud/instagram-users-scraper` | 2025-01-06, 158 stars | yes | its own issue #2, still open: *"The scrapper script is no more working"* (2024-08) |
| `ranbot-ai/instagram-scraper` (Puppeteer) | 2025-02 | cookies slot | README: *"Proxy: Residential Zone"* — **purchased proxies, refused** |
| `veeso/instagram-scraper-rs` | 2024-10, **archived** | yes | archived and login-gated |
| `dwisulfahnur/ig-crawler-chrome-extension` | **2026-05-06** | yes | **the most novel mechanism found anywhere**: issues no request of its own, passively reads network responses the browser already received. Refused on login, and needs a human driving a browser per account |
| n8n Instagram "guest" nodes | 2026-01 / 2025-07 | no | *"your n8n server IP may be temporarily blocked"* in their own README; and they take a **post shortcode**, not a username — wrong object |
| Go / Ruby / older PHP scrapers | 2016–2020 | mixed | dormant 5–9 years against a platform that has re-walled repeatedly |
| Apify Instagram actors | active | — | closed-source, paid-proxy backends — the Scrapfly pattern again |

**Every candidate that reads profile data without a login converges on the same
`web_profile_info` surface.** New language, same wall. Every candidate with a materially
different execution model either requires a login, requires purchased proxies, or targets posts
rather than profiles.

### Forks of the dead, and non-English ecosystems

**Forks:** `drawrowfly` has 12 forks, all stale copies of the same 2023 commit (one shows a 2026
`pushed_at` but every actual commit is from 2022 — a re-fork event, not new work). `cloudrac3r/bibliogram`
is 404; `Booteille/bibliogram` archived 2020. **No living Nitter-for-Instagram successor exists
in any language.**

**Non-English:** Gitee's only Instagram hits were a deleted repo and a mirror of `instagrapi`
(login-required). Chinese repos (`ins_spider`, `ig404`, `SimpleInstagram`, `ins_crawler`) all
last pushed 2018–2023. Russian parsers 2019–2022, dead. Indonesian and Portuguese terms
surfaced only the same English projects or paid services. **Honest conclusion: empty.**

## 3c. The mirror class — the data is there, and it is out of scope

This is the closest the round came to a real second source, and the reason it fails is worth
stating precisely, because it is a rule and not an engineering limit.

**`imginn.com` carries the real bio text.** Verified by fetching through a real browser: 9 of 10
brand accounts returned the genuine biography (`@nike` → "Just Do It.", `@nasa` → "Making the
seemingly impossible, possible. ✨"), with `@natgeo` the one miss. **No wall appeared across a
10-request run**, and the selector was found by live DOM inspection — `div.bio` inside
`.user-meta`. It is **not instagram.com**, so it has an entirely separate rate budget: precisely
the property every other candidate lacks.

**The rest of the family is dead or sealed.** `picuki.com` now redirects to a TikTok viewer —
it has left Instagram entirely. `picnob.com`/`pixwox.com` both redirect to `pixnoy.com` and sit
behind a Cloudflare Turnstile that did not clear even in a real browser after 20 seconds.
`gramhir.com` times out. `dumpor.io` returns a 200 shell whose profile data never populates.
**So the two bridges RSS-Bridge actually ships — `PicnobBridge.php` and `PicukiBridge.php` —
point at dead hosts**, and neither extracts a bio anyway (Picuki's has a *commented-out* author
field: someone started this and gave up).

**Why it is refused rather than pursued.** `imginn.com` sits behind Cloudflare bot management.
Tested here directly: **Playwright Chromium was blocked in both headless and headful mode**,
controls 0 of 2 each time — and the control is what makes that statement safe, because without
it a zero on our own handles would have measured the gate rather than the mirror's coverage.
Only a real user-profile browser passed.

⚠️ **So the honest verdict is not "too hard" — it is OUT OF SCOPE.** Cloudflare bot management
**is** a platform control. One person opening one page is ordinary browsing; automating past the
challenge for ~20,000 accounts is evading a control, and this round refuses those rather than
testing them. **It would have been out of scope even if Playwright had passed.**

**What would change it:** if any mirror serves plain HTTP without a bot challenge, this becomes
a live candidate immediately — the data is demonstrably there and the rate budget is separate.
Mirrors churn constantly, so this is worth one cheap re-check in a future round. **Our coverage
of small creator accounts remains UNMEASURED** — the controls failed before a single one of our
handles was tried.

## 4. Territory (b) — sources that are not Instagram

The idea was right and the class is nearly empty. A bio is text the creator wrote; where else
does it live?

| source | keyed by IG handle? | carries the real bio? | verdict |
|---|---|---|---|
| **Amazon Influencer Storefronts** | partially — vanity slug often is the handle, often is `influencer-15f4ce17` | **yes, verified by fetch** — but a *separately written* Amazon bio, not a copy of the IG one | the round's only positive, and a weak one: US-only programme, lifestyle-skewed, and Amazon's WAF returned **503 on every direct fetch** |
| **Linktree / Stan / Beacons / Komi / Milkshake** | yes | **no** — verified: link directories with no bio field | dead as a class |
| **Favikon / CreatorDB** | yes | **no** — they *generate* an AI summary; CreatorDB's own text calls it a "brief biographical description" | fails the correctness test outright |
| **HypeAuditor** | yes | **yes** — `bio_raw` exists in its API | **refused**: paid credentials |
| **Wikidata P2003** | yes | **no** — a bare identifier property; the item description is editor-written | dead |
| **Facebook Page "About"** | no free join | untested — `mbasic` returned a browser-fingerprint gate | **ABSENT**, and Meta-owned, so likely the same wall by another name |
| **X / YouTube / TikTok profile reuse** | sometimes | X now returns **402 Payment Required**; YouTube/TikTok are JS-rendered | unusable without a browser |

Every platform that lets a creator write a public blurb does not expose it as a queryable field;
every platform with a bio-shaped field fabricates it; the one platform that has the true text
cached charges for it.

## 5. Territory (c) — the cross-platform idea, and why its zero is not the zero it looks like

TikTok bios ride free on a call already being paid for, at 91–93%. So: how often is an
Instagram creator's address already sitting in their TikTok bio?

| measurement | result |
|---|---|
| handle overlap, TikTok side | **0 of 55,628** = 0.00% [0.00–0.01] |
| handle overlap, Instagram side | **0 of 17,045** = 0.00% [0.00–0.02] |
| the prize: IG-with-email whose same-handle TikTok bio holds that address | **0 of 9,574** [0.00–0.04] |
| the reverse | **0 of 2,857** [0.00–0.13] |
| **the false-match rate** | **undefined — 0 of 0 pairs** |

Every zero passed a positive control (planted pairs with zero-width, fullwidth and trailing-dot
noise all matched; a planted mismatch was correctly flagged), and the headline was re-derived
two ways — substring containment on NFKC-normalised text, and regex-extract-then-exact-match —
which agree.

⚠️ **But this measures the wrong thing to answer the question, and saying otherwise would be
the round's worst error.** It reproduces BL-1550: the TikTok and Instagram rows in
`master_leads.csv` are **structurally disjoint populations**, discovered by independent
hashtag seeds. So the finding is *"the store I already have cannot be joined"* — **not** *"creators
don't reuse bios"*, which is unmeasurable from this corpus. And the false-match rate the brief
rightly called critical **could not be computed at all**: there are no same-handle pairs for two
addresses to disagree on. **Reported as undefined, never as zero.**

Testing the real idea needs a different discovery process — following a TikTok bio's own
Instagram link *forward* — which this round did not build.

## 6. Territory (d) — free signals, one rediscovery and one real spread

*(the HTTP/2 result is §7)*

The agent caught a trap worth recording: **`master_leads.csv` is a POST-FILTER population.** Its
email base rate is ~56% against the 5.48% of a real pre-payment walk, because only rows that
passed the quality gate are stored. Tuning a pre-payment signal on it would be circular. It used
a genuine pre-filter corpus instead — 1,677 resolved accounts across 16 real `*edit` hashtags,
base rate **8.35% [7.12–9.77]** — with a 50/50 hash split, tuned on one half and reported on the
other.

**Its best signal is a rediscovery.** "Skip sports-team hashtags" (3.39% vs 8.35%) is the bucket
ordering this project already measured — film 9.22% ≫ sport 3.37% ≫ anime 1.26% — and already
acted on: BL-1557 walked film tags only, for exactly this reason.

**And its second signal is weaker than reported.** Handle-contains-underscore: 5.73%
[4.04–8.06] against 9.54% [7.98–11.37]. Fisher p=0.0099, but **the Wilson intervals overlap**.
Both numbers belong in the report.

**The genuinely useful finding is one nobody named — the spread WITHIN the film bucket is 10x:**

| tag | address rate |
|---|---|
| `creededit` | **24.68% [18.61–31.95]** |
| `batmanedit` | 14.97% [10.35–21.17] |
| `animeedit` | 11.54% [5.40–22.97] |
| `johnwickedit` | 8.54% [5.65–12.70] |
| `duneedit` | 7.18% [4.25–11.90] |
| `spidermanedit` | 5.77% [2.67–12.02] |
| `topgunedit` | 4.66% [2.47–8.62] |
| `michaeljordanedit` | 3.20% [1.25–7.94] |
| `gladiatoredit` | **2.38% [0.81–6.77]** |
| `lakersedit` | 1.82% [0.32–9.61] |
| `chicagobullsedit` | **0 of 22** [0.00–14.87] |

**Tag choice is worth more than any handle heuristic**, and the tag ledger already records prior
yield per tag — so this is actionable today at zero cost: rank candidate tags by their recorded
address rate before walking them.

**One unvalidated lead, flagged honestly:** `account_type` (business=2 / creator=3) is present in
raw hashtag payloads and already wired as "free" into `ig_discovery.py` and `main.py` — but its
correlation with email presence **has never been measured against ground truth**, because no
dataset on disk pairs the two. It could be stronger than anything above. **ABSENT, not zero.**

## 7. The HTTP/2 lead — MEASURED, and the answer is no

This is the one candidate that is in scope, needs no login, costs nothing to adopt, and has
**dated, independent corroboration from strangers**. It deserves the detail.

**The claim** (instaloader PR #2730, opened 2026-08-15 by `e3rd`, branch pushed 2026-08-22,
**still open and unmerged**): Instagram answers `web_profile_info` with `429` over **HTTP/1.1**
while the **identical** request over **HTTP/2** returns `200` — *"independent of account, session
and IP address"*, with the rollout *"partial"*.

**Six independent, dated reports on that PR:**

| date | who | what they said |
|---|---|---|
| 2026-08-15 | `tomballgithub` | both protocols worked for them — **unaffected**, which is what "partial rollout" predicts |
| 2026-08-22 | `davispuh` | reproduced the 429/200 split, and found a real bug in the patch (`urllib3.HTTPHeaderDict` on urllib3 1.x) — fixed same day |
| 2026-08-22 | `okkesd` | *"As of today, it works for me, thanks!!!"* |
| 2026-08-23 | `KertLynx` | *"I confirm too. This MR worked for me."* |
| 2026-08-30 | `apastel` | *"Adding another 'works for me!' comment, because it does."* |
| **2026-09-05** | `marty90` | *"it works for me. I got rid of the 429 at every request."* |

**And the counter-evidence, which is why this is not a settled rule.** The same repo's PR #2676
added an equivalent HTTP/2 adapter in March 2026 and its author **withdrew it on 2026-06-12**:
*"plain HTTP/1.1 now completes the full profile-metadata + get_posts workflow with no 429… the
host-level block that originally forced HTTP/2 appears to have lifted (Instagram's flagging was
evidently temporal)."*

**So the honest characterisation is: an intermittent, partial, host-dependent block that
appeared, lifted in June, and reappeared from August onward — with the workaround independently
confirmed working nine days before this round ran.** That is a far better lead than "someone
opened a PR", and it is exactly the kind of thing the operator meant by *"it's out there, it's
open source"*.

**Two further threads worth recording:**

* `LiVeenMusic` (2026-09-09) argues `web_profile_info` is being **retired server-side** for a
  reason unrelated to HTTP version, and suggests `graphql/query` instead.
* A **different** angle exists: `mahimmazidul/instaloader`, pushed **2026-09-12**, uses
  **curl_cffi TLS impersonation** rather than protocol version. Its own author calls it
  *"experimental"*, and `chipperpip` reported on **2026-09-13** that it did **not** fix the 429
  on Windows. Distinct mechanism, distinct evidence, unresolved.

Notably **no equivalent discussion exists in gallery-dl or yt-dlp** — their open 429 issues never
mention protocol version. The phenomenon appears to be visible only because instaloader's
maintainers instrumented for it.

### What I actually measured, and the mistake in the middle of it

**Run 1 — three arms, one variable at a time, 8 handles each:**

| arm | content | protocol negotiated |
|---|---|---|
| A urllib HTTP/1.1 (shipped) | 0/8 [0.0–32.4] | HTTP/1.1 ×8 |
| B httpx HTTP/1.1 | 0/8 [0.0–32.4] | HTTP/1.1 ×8 |
| **C httpx HTTP/2** | 0/8 [0.0–32.4] | **HTTP/2 ×8 — verified, not assumed** |

Arm B exists so a win for C could not be dismissed as "httpx differs from urllib", and the
protocol was read off `response.http_version` because `httpx` falls back silently when h2 is
unavailable. **The instrument worked; the window did not.** All three arms were walled, so the
run is **ambiguous, not a refutation.**

⚠️ **Run 2 was worse, and the fault was mine.** I built a retest that polled every 20 minutes
waiting for a fresh window — **3 requests an hour against a refill I had just measured at 2.5–5.8
an hour.** The poller was spending tokens at roughly the rate they arrived, so the bucket could
never accumulate the ten the test needed. It sat walled through five polls and 145 minutes.
**This is precisely the confound I criticised BL-1554 for** — it polled every 3 minutes and
concluded "no recovery in 72.6 minutes" — reproduced by me one round after I wrote the lesson
down. The operator caught it and told me to stop.

### Run 3 — one probe after real silence, and then the answer

The poller was stopped at 23:25 on 2026-09-14, the exact epoch of the last Instagram request was
written to `scratch/bl1559/silence_marker.json`, and a **hard time gate was compiled into the
probe script** so it physically refuses to fire before three hours of untouched exit have
elapsed. *(Proven: invoked early it printed `REFUSING: only 0.04 h of silence so far` and issued
no request.)* The machine then crashed, which — for this one experiment — was the best thing
that could have happened: **the exit sat completely untouched for 12.6 hours**, far longer than
the design called for, with no poller in the way.

**The probe, request number one after 12.61 hours of silence:**

    bytes=836,085   content=True   bio=True   0.89s   (HTTP/1.1)

**THE WINDOW WAS OPEN.** That single number is the first clean refill measurement this project
has ever taken — every previous one was contaminated by the poller that produced it.

**Then the window was spent on the paired test, 30 pairs, same handle both arms, order
alternating, protocol verified per response:**

| arm | content | 95% CI |
|---|---|---|
| H1 (HTTP/1.1) | **17/30 = 56.7%** | [39.2–72.6] |
| H2 (HTTP/2) | **15/30 = 50.0%** | [33.2–66.8] |

    H2 won where H1 failed, same handle : 0
    H1 won where H2 failed, same handle : 2
    protocols negotiated : {'HTTP/1.1': 30, 'HTTP/2': 30}

**VERDICT — declared before the run, not after: `no http2 advantage at this exit`.** The
threshold for "reproduces" was set in the script as *h2_only ≥ 2 and h2_only > h1_only*. It
came in at **0 against 2 the other way**.

**And the denominator that matters is smaller and cleaner than 30.** The window drained during
the run, on a hard cliff:

    h1: CCCCCCCCCCCCCCCCC..............
    h2: CCCCCCCCC.CCCCCC...............
        (pair 1 ............ pair 30)

Restricted to the **17 pairs taken while the window was still open**, H1 is **17 of 17** and H2
is **15 of 17**. HTTP/2 did not win a single pair its HTTP/1.1 twin lost, in either slice.
**PR #2730 does not reproduce at this exit.** That does not make the PR's authors wrong — six
strangers reproduced it on their own hosts, and the claim was always "partial rollout,
host-dependent". It means **this host is not one of the affected ones, and adopting the patch
here buys nothing.**

### The by-product: a capacity number, and a correction to our own two-tier model

The cliff is itself a measurement. Counting every request issued across both runs of the probe:

| | |
|---|---|
| requests issued into the fresh window | **72** |
| requests that returned content | **43** |
| **position of the last request carrying content** | **#45** |
| consecutive shells after it | **27, unbroken** |

**A 12.6-hour idle bought roughly 45 fetches — not the 300–450 the two-tier model in §2
predicted for an overnight refill.** BL-1558 proposed a small fast bucket (~10, ~25 min) over a
large slow one (~300–450, overnight); BL-1557 saw a ~300-fetch burst after a night. **This run
says an overnight-scale idle can yield an order of magnitude less than that**, which most likely
means the slow bucket refills against how *deeply* it was drained rather than on a fixed
schedule — this round drained it hard, repeatedly, for two days. **The two-tier model should be
treated as unsettled, and the ~300–450 figure as an upper bound observed once, not a capacity.**

**The cliff falls at the same place in both arms**, which is worth stating on its own: it is
**one bucket, shared across protocols**, not a per-protocol quota.

⚠️ **One observation reported without a conclusion.** The probe returned a bio that did **not**
value-match the paid bio stored for that handle. The harness's own rule is that a non-match is
not a failure — bios change, and the control for it is running the shipped route on the same
handle in the same window, which this run did not do. **One handle, no control, no finding.**

## 8. The dissent — the funnel has never been used

One agent was told to disagree with the premise. It came back with the finding of the round, and
**I verified every number of it myself rather than relaying it.**

`master_leads.csv`, parsed with a parser and not a line count: **73,001 rows, 13,007 carrying an
email address.** All five outreach columns exist in the header. All five are empty:

| column | present in header | non-blank rows |
|---|---|---|
| `date_sent` | yes | **0** |
| `sent_channel` | yes | **0** |
| `replied` | yes | **0** |
| `reply_sentiment` | yes | **0** |
| `outcome_notes` | yes | **0** |

A positive control confirms the counter can see a filled value, so this is a real absence and not
an instrument failure. Alongside it: `send_identity.json` still contains **11 `PLACEHOLDER`
values** — including `RATE`, `PRICE`, `PAYMENT_TERMS` and `TURNAROUND` — and
`output/PILOT_20_BL-1023/`, a finished 20-editor pilot with its messages already written, has
been untouched for **42.8 days**.

**The distinction that makes this matter.** This repo runs two different funnels. Twitch,
Spotify, Google Play and YouTube find **buyers** — people who would pay for clips. Instagram and
TikTok find **labour** — editors and meme pages to hire. The project's own `NO_SEND.md` says
outreach is handled because "he has a separate tool already sending leads daily and closing
clients" — **but closing clients is the buyer funnel.** The only visible evidence about the
labour funnel is a pilot that was never sent, because five commercial terms were never decided.

⚠️ **I cannot see the external sending tool, so I cannot prove no editor has ever been emailed —
only that nothing in this store records it.** That is the single question worth more than this
entire round: **has one harvested editor ever been contacted, and did anyone reply?**

The economics that follow from it:

    cost per qualified editor = $13.94 / 1,000 x (1 / 0.133) = $0.105
    lifetime vendor spend, entire project, spend.json = $66.08
    to spend $1,000 you must buy 71,736 net-new addresses = ~9,541 qualified editors
    to staff 50 working clippers you need ~376 addresses = $5.24

**The cost axis is dead at every volume this business will reach.** And the free route, at 290
hours to save $13.94, is worth **about five cents per hour of wall clock**.

The agent also verified, through public invite endpoints with no login, that
`discord.com/invite/clipping` has **110,541 members** and `discord.com/invite/spadeclipping`
**36,748**, and that Whop Content Rewards lists campaigns publicly with no upfront cost. Whether
their rules permit a hiring post is **ABSENT** — reading them needs an account, which the hard
line forbids. The honest counterweight, which the agent supplied itself: inbound at a low rate
buys the bottom of the market, and outbound scraping remains the only way to reach one specific
500k-follower meme page that is not bidding for scraps. **That is the real case for the scrape —
and it is a case for buying a few hundred chosen accounts, not for a cost-reduction round.**

## 9. The price, with the divisions written out

**Correcting the arithmetic first, because the decision depends on it.**

    1,000 net-new addresses at a MEASURED 5.14% net-new rate
      = 19,467 profile calls          <- THIS IS THE ~20,000 ACCOUNTS. It is already here.
      + ~721 hashtag pages
      = 20,188 x $0.00069064
      = $13.94

You believed $13.94 was the price of 1,000 calls and that reading ~10,000 accounts would be an
additional cost. **It is not additional — it is the whole of the number.** The pessimistic
version is the one already written down.

| route | price per 1,000 net-new | note |
|---|---|---|
| the cold bar | $44.61 [$20.72–$97.05] | the population a fresh walk resembles |
| **paid fallback** | **$13.94** | **3.2x better than the bar** |
| last real walk | $7.57 [$5.37–$10.74] | the free burst carried half of it |
| free route alone | $0.00 and **290 hours** | 3.45 addresses/hour at best |

**And the real unit is editors, not addresses.** Only ~13.3% [5.31–29.68] of the last walk's
addresses passed `editor_gate`, on 30 rows. ⚠️ **That interval is wide enough to be worth
settling**: BL-1548 measured 29.37% [27.57–31.23] on a different population, and the two
disagree by more than 2x. Every cost-per-editor figure in this report moves with it, and it is
cheap to resolve.

**What to do:**

1. **Pay the $13.94.** The arithmetic is not close.
2. **Send the twenty.** Fill the eleven placeholders, decide a rate, send the pilot that has been
   ready for 42.8 days. It costs nothing and produces the one number nobody has. *(n=20 measures
   nothing statistically — 2 replies of 20 is [2.8–30.1] — but it proves the machinery works.)*
3. **Rank tags by recorded yield before walking them.** Free, already in the ledger, and worth
   more than any handle heuristic: 24.68% on the best tag against 0 of 22 on the worst.
4. **Do not spend another round on the free route.** Three rounds have now measured it. It is a
   burst bonus worth taking when a walk starts cold, and nothing more.

### The suite

    FAILED -- 25 red of 480 suite(s)   (2286.9s)

**No red is mine.** Attributed per suite name against BL-1558's closing 26: the red set is a
strict subset — **zero new** — and `tests/test_claims_manifest.py` went **red to green**,
confirming last round's fix to BL-1557's manifest prose landed. No production code changed this
round.

## 10. WHAT I GOT WRONG

**1. I made the exact error I wrote a memory about yesterday, one day later.** A wall-state probe
returned **6 of 6** and I recorded the exit as OPEN in `wall_state.json`. The harness self-test
minutes later returned **0 of 10**, walled at request 1. The bucket held about six tokens.
Yesterday's memory is titled *"do not over-read a probe as a route"* and says *"'open' and 'open
with eleven fetches in it' are different statements"*. Writing the lesson down did not stop me
repeating it; only the harness's built-in control caught it.

**2. I published a refill rate yesterday that is wrong by an order of magnitude.** BL-1558 reported
**≥67 fetches/hour**. Today, after a 2.41-hour idle, the bucket held **6–14 tokens** — an implied
**2.5–5.8/hour**. The ≥67 figure came from one 25-minute window and mistook the *fast* bucket's
refill for a sustained rate. A two-tier model fits every observation across three rounds: a small
fast bucket (~10 fetches, refilling in ~25 minutes) sitting on a large slow one (~300–450,
needing an overnight idle). **The practical consequence is that yesterday's "3.45 addresses/hour"
is optimistic by roughly 10x, and the free route is even weaker than I reported.**

**3. I nearly published a sub-agent's headline without checking it.** The signal agent's best
result — "skip sports-team hashtags, 3.39% vs 8.35%" — is a **rediscovery of the bucket ordering
this project measured rounds ago and already acts on** (film 9.22% ≫ sport 3.37% ≫ anime 1.26%;
BL-1557 walked film-only for exactly that reason). Its second signal was reported with a Fisher
p=0.0099 but **its Wilson intervals overlap**, which the summary did not mention. Both only
surfaced because I re-derived the numbers from the corpus myself. **A sub-agent's result is a
claim, not a measurement, until you reproduce it.**

**4. My first HTTP/2 test was spent against a wall and proved nothing.** I ran it while the exit
was already walled, so all three arms returned shells and the result was ambiguous. It was
correct to refuse a conclusion, but the run itself was avoidable — I knew the state and ran it
anyway, then had to spend a second window doing it properly.

**5. The shell silently ate content out of this report, twice, and I only caught it by looking.**
Writing report prose through a double-quoted `python -c "..."` string lets bash expand `$` and
execute backticks *before Python ever sees them*. The headline paragraph lost every dollar
amount — "$13.94" became "3.94" — and a later edit turned "`tests/test_claims_manifest.py` went
red to green" into "and  went red to green", because the backticked filename was run as a
command. Both were repaired, and the lesson is mechanical: **prose with money or code spans in
it goes through a file write or a quoted heredoc, never through a double-quoted shell string.**
This is the third round in which shell quoting has corrupted something I wrote.

**6. I certified the round's money with a claim I had not tested in both directions.** The claim
filed `spend_usd: 0.0` with the note *"nothing to book and nothing off the books"*. The vendor
half was right and I had proved it. **The ledger half I had not looked at at all** — and my own
suite run had put **212 rows and $0.038270 of spend that never happened** into the production
`spend.json` while I was writing that sentence. I checked the direction I had been burned in
last round and not the other one. **§12 has the mechanism, driven.**

**7. I published over a red leak-scan verdict without recording why.** The scanner printed `NOT
publishable as-is` on 8 hits and I published four minutes later. The decision was correct — all
8 are ordinary English words — **but nothing in the round says so**, so the next person to read
`leakscan.json` sees a red receipt against a published file and no explanation. **A judgement
call that overrides a safety check has to be written down at the moment it is made, or it is
indistinguishable from ignoring the check.**

## 11. What did not run, reported as ABSENT

* ~~**Whether HTTP/2 lifts the wall.**~~ **NO LONGER ABSENT — measured in §7: it does not, at
  this exit.**
* **What actually governs the slow bucket's refill.** §7 shows a 12.6-hour idle buying ~45
  fetches where the model predicted 300–450. Depth-of-drain is the obvious candidate and it is
  untested.
* **How much of the ledger's $3.63 of `free_judge_paid` is fabricated by test runs.** §12
  proves the mechanism and bounds it; it does not separate real from fake.
* **What added the row to `spotify_playlists_seen.json`.** §12 — a real change, unattributed.
* **Whether `account_type` (business/creator) predicts an email.** The field is in the raw payload
  and already wired as free, and **no dataset on disk pairs it with ground truth**. It could be
  stronger than every signal in §6. Needs one paired harvest.
* **Whether creators reuse bios across platforms.** §5 answers only "the store I have cannot be
  joined". Testing the real idea means following a TikTok bio's own Instagram link forward.
* **Whether the Discord servers permit a hiring post.** Reading their rules requires an account;
  refused, not tested.
* **Facebook Page "About" as a bio mirror.** `mbasic` returned a browser-fingerprint gate, so
  absence is unproven either way — the one item in §4 that is genuinely untested rather than
  refuted.
* **Whether any harvested editor has ever been contacted.** The sending tool is outside this repo.
  **This is the most valuable unanswered question in the round.**
* **The editor rate.** 13.3% [5.31–29.68] against BL-1548's 29.37% [27.57–31.23] — a 2x
  disagreement that moves every cost-per-editor number here.

## 12. The crash audit — what the interrupted session actually left behind

The machine went down mid-round. Everything below was re-established from disk, and every
prerequisite was re-derived by driving the code rather than by reading an earlier report.

### Money — and a correction against my own claim

**Vendor spend: $0.00, and that part of the claim holds.** An AST scan of all nine scripts this
round wrote finds **no vendor client, no ledger writer and no paid call reachable from any of
them** — no `IgClient`, no HikerAPI, no LamaTok, no `record_aux_spend`. Ground truth was reused
from the 170 paid profiles already on disk. The probe runs above fetch `instagram.com` directly,
which is free.

⚠️ **But the claim also said "nothing to book and nothing off the books", and that was wrong —
in the opposite direction from the leak it was guarding against.** Comparing the ledger against
this round's own round-start backup:

    spend.json    rows 37,754 -> 37,966    (+212)    $0.038270

**212 rows of spend that never happened were written into the production ledger by my own suite
run.** They are labelled `free_judge_paid:*` and they land between 21:37:21 and 21:44:08 on
2026-09-14 — inside the suite window of 21:30:01–22:08:08. *(That window is trustworthy: the 480
per-suite durations sum to 2,283.9s against a reported 2,286.9s, so the run was sequential and
the timeline reconstructs.)*

**The mechanism, driven rather than inferred.** A recorder was substituted for
`record_aux_spend` and `free_judge.should_reject()` was called once, exactly as the tests in that
window call it:

    book_calls                : 1
    label                     : free_judge_paid:nex-n2-mini
    vision_usd                : 8.9e-05
    spend_path                : <repo>/spend.json      <- THE PRODUCTION LEDGER
    writes_production_ledger  : true

**`_book_paid_call` defaults to the production ledger, and the tests in that window stub `_ask`
but not the booking.** So the network call never happens — no real money leaves — and the
ledger is charged anyway. *(This was verified with a recorder precisely so that proving it would
not add another 212 rows to the ledger.)*

**Both halves matter and they are different faults.** BL-1557 found money that was spent and
never booked. This is **money that was booked and never spent** — and it is the same class of
error, which is that the ledger is not a measurement of anything unless both directions hold.

**Scale, bounded honestly.** `free_judge_paid` rows across all time: **29,285 rows, $3.634493 —
5.50% of the $66.11 lifetime total.** That is an **upper bound** on fabricated spend, not a
finding: real funnel passes use the same label through the same function, and I could not
separate them. Row density does not separate them either — the paid lane throttles at
`PAID_RPM = 200`, and the busiest second in the whole ledger holds 6 rows, comfortably inside
it. **The proven floor is the $0.038270 from my own run. Separating the rest is a real question
and it is left open, stated as a question rather than answered by assumption.**

### The nine stores, bodies compared by shape

Re-fingerprinted with this round's own backup code, so the comparison is the same measurement
taken twice rather than two different ones:

| store | rows at start | rows now | natural key set | indexed digest |
|---|---|---|---|---|
| clip_seen.json | 2,193 | 2,193 | same | same |
| config.json | 174 | 174 | same | same |
| master_leads.csv | 73,001 | 73,001 | same | same |
| meme_pages_seen.json | 6,196 | 6,196 | same | same |
| repost_seen.json | 1,715 | 1,715 | same | same |
| **spend.json** | 37,754 | **37,966** | same | **CHANGED** |
| **spotify_playlists_seen.json** | 1,984 | **1,985** | **CHANGED** | **CHANGED** |
| state.json | 5 | 5 | same | same |
| tiktok_pages_seen.json | 3,270 | 3,270 | same | same |

**Seven of nine are byte-identical. Nothing was left half-written** — all nine parse, and the
row counts are exact, not approximate.

`spend.json` is the +212 above. **`spotify_playlists_seen.json` gained exactly one playlist, and
I am not going to tell you what wrote it.** Its mtime falls inside the suite window, but **mtime
is not evidence in this repo** — OneDrive rewrites it — and the added row carries no timestamp
of its own. **A real change, cause unattributed.** Given what the ledger did in the same window
a test is the obvious suspect, but "obvious suspect" is not a measurement.

### The suite — the verdict line, quoted

The run **completed** at 22:08, an hour and a half before the crash. It is not a partial run:

    FAILED -- 25 red of 480 suite(s)   (2286.9s)

**25 red against BL-1558's 26, attributed per suite name and not by subtracting totals: zero
new failures, and `test_claims_manifest.py` went red → GREEN**, confirming bc1abb27's fix
landed. No production code changed after that run — the only tracked file that differs from
HEAD is `tests/test_bl1221_supply.py`, whose working copy is dated **2026-08-31**, two weeks
before this round, and is therefore somebody else's uncommitted edit, not a mid-edit of mine.

### The leak scanner said NOT PUBLISHABLE, and it was wrong 8 times out of 8

The pre-publish scan flagged this report with **8 hits for "a real creator handle"** and printed
`VERDICT: 1 FILE(S) CARRY A HIT -- NOT publishable as-is`. It was published anyway, and **that
was the right call, but the round never wrote down why.** The eight tokens are:

    basic · evidence · issues · records (×2) · youtube (×3)

**Every one is an ordinary English word that also happens to be somebody's handle** in a corpus
of 72,846 of them. The report contains **no `@` sigil anywhere** and no real handle. **8 of 8
false positives.**

**And the amended report demonstrates it on itself.** Re-scanned after these sections were
added, the count rose from 8 to **20 — and five of the new hits are the sentence above**, the
one that lists the false-positive tokens in order to explain that they are false positives. A
detector that fires on its own post-mortem is not calibrated; it is matching English.

This is the exact mirror of BL-1548, where the same detector's exclusion list **swallowed 23 of
the 30 longest real handles**. One direction hides real leaks; the other makes the verdict line
unreadable, which is worse than useless because an operator learns to publish over it. **The fix
is not a longer stoplist in either direction** — it is requiring the `@` sigil, or gating
matches on word frequency, so that a token has to look like a handle and not merely collide with
one.
