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

## 7. The HTTP/2 test — the one lead worth spending a window on, and it is ABSENT

PR #2730's claim is specific and falsifiable: HTTP/1.1 gets `429`, **the identical request over
HTTP/2 succeeds**, independent of account, session and IP. And it was a genuine gap here —
BL-1554 did test HTTP/2 and got 0/10, **but every Python arm that round sent a browser
user-agent**, which BL-1557 later proved always returns a shell. **HTTP/2 combined with the
non-browser `PROFILE_UA` had never been tried.**

**Run 1 — three arms, one variable at a time, 8 handles each:**

| arm | content | bio | protocol actually negotiated |
|---|---|---|---|
| A urllib HTTP/1.1 (shipped) | 0/8 [0.0–32.4] | 0/8 | HTTP/1.1 ×8 |
| B httpx HTTP/1.1 | 0/8 [0.0–32.4] | 0/8 | HTTP/1.1 ×8 |
| **C httpx HTTP/2** | 0/8 [0.0–32.4] | 0/8 | **HTTP/2 ×8 — verified** |

Arm B exists so a win for C could not be "httpx behaves differently from urllib", and the
negotiated protocol was read off `response.http_version` rather than assumed — `httpx` falls
back silently to 1.1 when h2 is unavailable, which would have made a null result meaningless.

**The instrument worked. The window did not.** All three arms were walled, so this is
**ambiguous, not a refutation** — a real HTTP/2 effect would be invisible here.

**Run 2 — the retest, designed properly and still ABSENT:**

Sized to the bucket (5 paired H1/H2 fetches on the *same* handle rather than 24 spread across
arms), waiting 45 minutes and then polling for a fresh window, with nothing else in the session
permitted to touch Instagram. Through **t+125 minutes it never reopened**:

    t+ 45.0 min  bytes=498,400  content=False
    t+ 65.0 min  bytes=497,837  content=False
    t+ 85.1 min  bytes=498,813  content=False
    t+105.1 min  bytes=505,886  content=False
    t+125.1 min  bytes=501,556  content=False

⚠️ **AND THE REASON IS PARTLY MY OWN DESIGN, WHICH IS THE POINT.** I set the poll interval to 20
minutes — **3 requests an hour — against a refill I had just measured at 2.5–5.8 an hour.** The
poller is spending tokens at roughly the rate they arrive, so the bucket can never accumulate
the ten needed for the pairs. **This is precisely the confound I criticised BL-1554 for**
(it polled every 3 minutes and concluded "no recovery in 72.6 minutes"), written into my own
harness one round after I wrote the lesson down.

**So the HTTP/2 claim is neither confirmed nor refuted here. It is ABSENT**, and the way to
settle it is a single 5-pair run after an *un-polled* overnight idle — no detector, no probe,
just the test. That is a ten-minute job for whoever picks this up, and the script
(`scratch/bl1559/bl1559_http2_retest.py`) is written; it needs only `BL1559_POLL_MIN` raised far
above the refill rate, or removed entirely in favour of a fixed long wait.

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

## 11. What did not run, reported as ABSENT

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
