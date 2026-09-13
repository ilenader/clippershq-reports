# BL-1553 — the free Instagram bio is REAL, this machine's IP is blocked, and the cheapest lever was free all along

**Can Instagram reach $4 per 1,000 addresses, by which route, and what does it cost?**
**Yes — and the route costs $0.00, because it is one boolean that is already arriving in
every hashtag payload we already pay for.** `is_verified` is the single field this project
believed rode along for free, and it is the answer: on a labelled 1,677-account sample,
verified accounts publish an address **26.88% [20.61–34.23]** of the time against
**6.39% [5.27–7.74]** for everyone else. **The intervals do not overlap**, Fisher exact
p = 7.5e-14, and it holds in **8 of 8** testable hashtag strata. Buying *only* verified
accounts costs **$2.57 per 1,000 addresses [$2.02–$3.35]** against buying everything at
$8.27 — and against TikTok's **$4.26 [$2.99–$6.10]**. That is a **3.2x** cut for no money,
no new endpoint and no proxy. Two caveats stated up front and not buried: the filter reaches
only **30.7%** of the addresses (fine, since discovery is free, but it means more walking),
and **the size confound cannot be ruled out** — the hashtag payload carries no follower
count at all, which is precisely *why* the signal is free and also why it cannot be
controlled for. Applied instead to the harder cold-editor population behind the $44.61
headline, the same 3.2x lands near **$9.90**, not $2.57: the lever is a multiplier, and
where it lands depends on which accounts you point it at. **Separately, the free bio is not
dead** — the logged-out profile page still serves the real biography, follower count and
same-day posts, just not to this computer; from a clean exit it matched the paid API
**exactly, emoji included**. And **the $44.61 itself is not a property of Instagram**: it
rests on **six** addresses out of 361 and prices the single hardest population. On rows the
funnel already holds, the same paid call returns **$8.52 per 1,000 net-new addresses
[$4.16–$18.32]**, overlapping TikTok. What does *not* exist, and I can now say so across
the whole vendor surface rather than by sampling: a cheaper call, a bulk call, or a bio in
the discovery payload. Total spend **$0.0318** of a $0.50 cap.

---

## 1. What this project is, for a reader with no context

This system finds video editors and meme-page operators on TikTok and Instagram and collects
the email address many of them publish in their profile bio, so they can be contacted about
paid clipping work. A "bio" is the short free-text blurb on a profile. On TikTok the bio
arrives free inside the hashtag search results. On Instagram it does not: it must be bought
one profile at a time from a reseller API (HikerAPI) at **$0.00069064 per call**.

The number that matters is not the price of a call but the price of an **address**, because
most profiles do not publish one. **That ratio is the entire problem** — and it is what this
round turned out to be about.

## 2. Safety and the cap

Before any money moved:

* **Nine stores backed up**, sha256-verified, **bodies found by shape, never by a top-level
  key count** — `spend.json`'s payload is the list at `runs` (36,482 rows), `clip_seen.json`
  is a **bare list** (2,193), `tiktok_pages_seen.json` is a **dict at `pages`** (3,270). A
  reader that counts top-level keys reports **3** for that last store, which looks like
  catastrophic loss and is an artefact of the instrument.
* **All six corruption controls FIRED** on damage planted on purpose: a deleted row, a
  modified value, truncation, reordering (which the natural-key set is *provably blind* to),
  the wrapped-store shape control, and the one that matters most — **deleting one of a
  duplicated pair, where the natural-key set is provably IDENTICAL and only the
  position-qualified digest moves.**
* **The cap was proved to bind before the first call**, by lifting `Budget` out of
  `harvest_run.py` **by AST** and driving it: a funded cap allows and the meter advances **by
  the Instagram unit ($0.00069064), not TikTok's ($0.00060000), which are 15.1% apart**; a
  `$0.00` cap **raises** rather than meaning unlimited; the meter does **not** advance on a
  refusal; under **8 threads** the locked counter stops at exactly 50 of 50; and **the proof
  wrote nowhere**, verified by snapshotting the repo root.
* `IgClient` was constructed **`metered_by_caller=True`** throughout — that autoflush shape
  was once measured booking money exactly 2x.
* **`docs/FACTS.md` was at lag +0** against a live 36,482 rows (limit +2000). No re-stamp
  needed.
* `clippershq/` was **read-only for the entire round. Not one production file was modified.**

## 3. Ground truth cost $0.00, because it was already bought

The brief authorised buying 40–60 paid profiles as ground truth. **I bought none.** BL-1551
had already paid for **80 profiles drawn from real unscoreable rows** and kept the real bio
text: **74 calls succeeded, 69 carry a bio (86.25%)**. Re-buying them would have spent the
round's entire ground-truth budget to learn something already on disk.

**And the value test searches for the VALUE, not the field name** — walking the parsed
payload and comparing normalised strings, reporting *which key* carried the bio, so a route
hiding it under an unguessed name still passes. (It was broken at first. See section 10.)

## 4. Route (a) — the API surface. Re-read live: 154 paths, and the answer is no

Fetched **live** rather than from a cached summary (`https://api.hikerapi.com/openapi.json`,
223,302 bytes, `info.version = 1.8.1`) — a vendor once went 23 → 29 paths while keeping its
version number, and the miss was worth 7.5x.

**Two facts that cost $0.00:**

* **`GET /sys/balance` is documented "free, not billed"** and returns
  `{"requests": 53999, "rate": 15, "currency": "USD", "amount": 37.3461}`. `requests` is a
  live vendor-side call meter, used below as an independent check on my own counter.
* **HikerAPI 403s the default urllib User-Agent** with `error code: 1010` — a Cloudflare bot
  fingerprint, *not* an auth failure. Identical key, four attempts:

| attempt | result |
|---|---|
| `x-access-key` header, no UA | **HTTP 403, `error code: 1010`** |
| `X-Access-Key` header, no UA | **HTTP 403, `error code: 1010`** |
| `?access_key=` query param, no UA | **HTTP 403, `error code: 1010`** |
| `x-access-key` header **plus any UA** | **HTTP 200** |

A probe written with bare `urllib` and no UA reads a live, funded, correctly-keyed account as
FORBIDDEN and concludes the key is dead.

**The vendor prices every call on the response itself:** the `x-hiker-info` header carries
`reqs`, the billable requests that response cost. That is why everything below is priced
**per bio**, not per call — the spec contains **no** price field at all (`unit`, `credit`,
`price`: **0 occurrences** in 223 KB).

### 4a. A cheaper tier? No. The shipped route is already the floor.

One ground-truth handle, value matched against its known bio:

| path | status | reqs | bytes | secs | carries the bio? |
|---|---|---:|---:|---:|---|
| `/v1/user/by/username` | 200 | **1** | 1,317 | 1.08 | **YES** — `user.biography` |
| `/v2/user/by/username` | 200 | **1** | 16,325 | 1.08 | **YES** |
| `/v1/user/by/id` | 200 | **1** | 1,317 | 0.91 | **YES** |
| `/v2/user/by/id` | 200 | **1** | 16,285 | 1.11 | **YES** |
| `/a2/user` | 200 | **2** | 200,029 | 3.35 | YES — **2x the price for the same one bio** |
| `/gql/user/about` | 200 | 1 | 113 | 1.01 | no — 113 bytes, **same price, less data** |
| `/v1/user/about` | 200 | 1 | 113 | 0.86 | no — same |
| `/gql/user/web_profile_info` | **500** | **1** | 96 | **10.16** | no — **failed after 10s and was STILL BILLED** |
| `/gql/user/by/username` | **410** | **0** | 106 | 0.08 | no — **GONE, and not billed** |
| `/gql/user/by/id` | **410** | **0** | 106 | 0.08 | no — **GONE, and not billed** |

Controls: a large institution returned 200 with a bio; a **fabricated handle returned 404 —
and was still billed 1 request.** Failures are not free.

**`/a2/user` looks like the prize and is not:** **128 user objects for 2 requests**, but
**only one carries a bio** (the subject's, at `graphql.user.biography`).

### 4b. A bulk route? Exactly three in 154 paths, and none takes a user.

Enumerated across the whole surface, then each one actually called:

| path | array param | users returned | non-empty bios |
|---|---|---:|---:|
| `/gql/media/usertags` (up to 10 media ids) | `media_ids` | 11 | **0** |
| `/v2/media/comments/infos` | `media_ids` | 0 | **0** |
| `/gql/media/clips_metadata` | `media_ids` | 15 | **0** |

All three are keyed by **media id**. **There is no bulk user route at all**, so "many handles
per call" is not available on this vendor.

### 4c. Any search or list route carrying a bio? 0 of 738 user slots.

The only shape that could have reached the target — 20 bios in one call is 6.7x cheaper even
at 3x the price. **Four denominators kept separate**, because 723 slots once deduplicated to
609 distinct authors:

| path | reqs | bytes | user slots | distinct | non-empty bios |
|---|---:|---:|---:|---:|---:|
| `/v2/fbsearch/accounts` | 1 | 24,835 | 18 | 18 | **0** |
| `/v3/fbsearch/accounts` | 1 | 44,068 | 21 | 21 | **0** |
| `/v1/search/users` | 1 | 15,167 | 20 | 10 | **0** |
| `/v2/search/accounts` | 1 | 28,133 | 20 | 20 | **0** |
| `/gql/topsearch` | 1 | 534,302 | 35 | 9 | **0** |
| `/v2/fbsearch/topsearch` | 1 | 715,967 | 29 | 21 | **0** |
| `/g2/user/followers` | 1 | 18,785 | 15 | 15 | **0** |
| `/g2/user/following` | 1 | 30,415 | 23 | 23 | **0** |
| `/v2/user/suggested/profiles` | 1 | 66,263 | 74 | 74 | **0** |
| `/gql/user/related/profiles` | 1 | 41,859 | 58 | 58 | **0** |
| `/v2/user/explore/businesses/by/id` | **2** | 95,671 | 30 | 30 | **0** |
| `/v2/hashtag/medias/top` | 1 | 1,520,121 | 195 | 78 | **0** |
| `/v2/hashtag/medias/recent` | 1 | 618,359 | 101 | 61 | **0** |
| `/v1/hashtag/medias/top/chunk` | 1 | 887,113 | 99 | 71 | **0** |
| **TOTAL** | **16** | | **738** | **499** | **0** |

**The zero is controlled, and the control is the only reason it is worth anything.** The
detector was proved on five planted payloads — bio present, absent, under `signature`, empty
string, nested three deep — **and on a LIVE `/v1/user/by/username` response, where it
correctly found 1 non-empty bio under `biography`.**

## 5. Route (b) — the discovery payload, confirmed against 2,411 stored accounts

Route (a) answered this live on 395 hashtag user slots. An independent pass over **stored**
payloads answered it again at far larger scale, for $0.00:

| denominator | strict (documented hashtag containers) | broad (every discovery container) |
|---|---:|---:|
| raw media slots | 1,932 | 8,258 |
| distinct medias | 1,891 | 6,260 |
| **distinct author accounts** | **1,496** | **2,411** |
| accounts carrying `biography` | **0** | **0** |
| accounts carrying any email field | **0** | **0** |
| accounts carrying `external_url` | **0** | **0** |
| accounts carrying `follower_count` | **0** | 19 — and **none on the hashtag surface** |

**The key is absent, not empty.** `biography`, `email`, `external_url`, `category`,
`city_name`, `phone`, `address`, `website` do not appear as a key name *anywhere* among the
95 distinct leaf paths ever observed on an author object. The three containers were walked
**separately** — `medias[]` (1,923 slots), `fill_items[]` (4), `one_by_two_item.clips.items[]`
(5) — rather than letting a "biggest list" heuristic pick one.

**I verified the load-bearing half myself rather than quoting it:** 82 stored hashtag payload
files → **0** `biography` keys; the 66 stored paid `/user/by/username` dumps used as the
positive control → **65 non-empty**. The extractor is not blind; the absence is a real
property of the surface.

The 19 `follower_count` hits all come from `xdt_user_clips_graphql` or a GraphQL top-search
result — **every one requires the handle to be known already**, so it cannot help discover a
bio during a blind walk.

## 6. Route (c) — the IP question, settled: it is the IP

**Local exit (this machine, real browser UA):**

| handle | status | bytes | markers present | real display name in body? |
|---|---|---:|---|---|
| a large space agency | 200 | 625,924 | `full_name`, `is_logged_out_user_ssr`, `PolarisProfile` | **no** |
| a large geographic magazine | 200 | 625,927 | same | **no** |
| a large sportswear brand | 200 | 625,939 | same | **no** |
| **a FABRICATED handle** | **200** | **625,943** | **same** | **n/a** |

`biography`, `edge_followed_by`, `og:description`, `profile_pic_url` and `ProfilePage` are
**absent on every one**; every `<title>` is the generic `Instagram`. **A handle that cannot
exist is served the same 200 and the same ~626 KB as a real institution, and no real display
name appears anywhere** — the server never performs an account lookup. A fabricated marker
string was searched for as a control and correctly never matched.

**Remote exit (different network, different ASN), same URLs, fetched by me:**

| handle | biography | follower count | most recent post |
|---|---|---|---|
| a large geographic magazine | **served verbatim** | **268M** | **2026-09-12** |
| a large space agency | **served verbatim** | **104M** | 2026-08-19 |

Those dates are months past this model's training cutoff, ruling out reconstruction from
memory. **And the free bio is the REAL bio, not a preview:** buying the same two profiles
from the paid API (2 requests, $0.00138) returns text matching the free page **exactly,
emoji included**, with follower counts of **268,559,055** and **104,363,683** against the
page's "268M" and "104M".

**Two different failures, and the difference matters:** the **HTML page is served**, while
`instagram.com/api/v1/users/web_profile_info/?username=…` returns **HTTP 429** from the same
clean exit. The JSON API is guarded harder than the page.

**What the evidence permits.** n is small (7 handles returning content, all large public
institutions) and one institutional handle returned a bare shell remotely on two attempts.
This establishes that **the two exits are measuring different things and that a
platform-wide kill is inconsistent with live, dated, hydrated fetches.** It does **not**
certify a success rate, and **it does not establish that a clean exit serves SMALL creator
accounts** — the population that actually matters. Testing that would have meant transmitting
lead handles to a third party, which I refused.

## 7. Route (d) — THE ANSWER. One free boolean cuts the price 3.2x

The brief's arithmetic: at a 1.66% address rate you buy ~60 bios per address, so
$0.00069 × 60 = $0.042. **The price is the conversion, not the call.** So the conversion was
attacked, for **$0.00**, on a prior round's own committed, labelled walk (1,677 accounts with
a known bio state).

**I re-derived every number below myself from the source file rather than accepting it.**

| group | addresses / accounts | rate | Wilson 95% |
|---|---:|---:|---|
| base rate (everything) | 140 / 1,677 | 8.35% | [7.12% – 9.77%] |
| **`is_verified` = True** | **43 / 160** | **26.88%** | **[20.61% – 34.23%]** |
| `is_verified` = False | 97 / 1,517 | 6.39% | [5.27% – 7.74%] |

**The intervals do not overlap.** Fisher exact **p = 7.5e-14**.

**Measured in both directions**, because a slice can convert beautifully and cover nothing:

* `P(address | verified)` = **26.88%** — 4.2x the non-verified rate.
* `P(verified | has an address)` = 43/140 = **30.71%** [23.67% – 38.79%] — the **recall**.
* Buying only verified means buying **9.5%** of the accounts to reach **30.7%** of the
  addresses.

**Priced per 1,000 addresses directly — never composed from a carry rate:**

| | $ per 1,000 addresses | Wilson 95% |
|---|---:|---|
| buy everything | $8.27 | [$7.07 – $9.70] |
| **buy ONLY `is_verified`** | **$2.57** | **[$2.02 – $3.35]** |
| TikTok, as published | $4.26 | [$2.99 – $6.10] |

**$2.57 beats TikTok's $4.26**, and the intervals barely touch ($2.99 vs $3.35).

**Consistency, not a single slice.** The lift holds in **8 of 8** hashtag strata with enough
verified accounts to test — the stratification discipline that caught the earlier size
confound. Point-biserial correlation **0.218**.

### 7a. What this does NOT establish, stated plainly

* **The size confound cannot be ruled out, and I am not pretending otherwise.** Verified
  accounts are big accounts, and big accounts are more often businesses with a public
  contact address. **0 of 1,677 rows carry a follower count** — because the hashtag payload
  does not have one. That is exactly *why* the signal is free and exactly why it cannot be
  controlled for. Reported **ABSENT, not "no confound"**.
* The one argument against pure size-proxying is that this project has already measured a
  **follower floor to be INVERTED** (8–10-digit accounts had a *lower* median than 1–5-digit
  ones). A pure size proxy should inherit that inversion. `is_verified` does the opposite and
  lifts strongly. That is an argument, not a proof.
* **A follower signal could never be used anyway**: follower count is **0.00% free** on the
  discovery surface, so even a working one is structurally unavailable before purchase.
* **Recall is 30.7%** — the filter leaves 69.3% of addresses unbought. Since discovery is
  free this is a walking problem, not a money problem, but it is real.
* **$2.57 is this sample's base rate times the lever.** Applied to the harder cold-editor
  population behind $44.61, the same 3.2x lands near **$9.90**. **The lever is a multiplier;
  the landing point depends on the population.** Which brings us to the next section.

## 8. The $44.61 is not a property of Instagram — it is a property of the target

I re-checked BL-1552's own published block: `accounts w/ address = 6`. **The headline rests
on six events**, which is why its interval spans $20.72–$97.05.

Run the *same paid call* against a **disjoint** sample from a **different population** — the
74 already-paid profiles drawn from rows the funnel holds but cannot score:

| sample | denominator | addresses | rate | Wilson 95% |
|---|---:|---:|---:|---|
| BL-1552, cold hashtag-discovered editors | 361 bought | **6** | **1.66%** | [0.76% – 3.58%] |
| **BL-1553, rows already held but unscoreable** | **74 bought** | **22** | **29.73%** | **[20.53% – 40.93%]** |

**The intervals do not overlap** — ~18x apart.

**But 29.73% is the number a careless round publishes, and it is wrong.** This project has
already published a 92% "re-find" that was the funnel counting its own memory. So the 22 are
split three ways:

| | k | of 74 | Wilson 95% |
|---|---:|---:|---|
| bio carries an address (any) | 22 | 29.73% | [20.53% – 40.93%] |
| — already held **for this same handle** (memory, worth $0) | 13 | 17.57% | [10.56% – 27.77%] |
| — held under a **different** handle (duplicate, worth $0) | 3 | 4.05% | [1.39% – 11.25%] |
| — **NET-NEW (the only one worth money)** | **6** | **8.11%** | **[3.77% – 16.58%]** |

| | $ per 1,000 addresses | Wilson 95% |
|---|---:|---|
| counting all addresses found (the optimistic, wrong read) | $2.32 | [$1.69 – $3.36] |
| **counting only NET-NEW (the honest read)** | **$8.52** | **[$4.16 – $18.32]** |

**$8.52 is 5.2x better than $44.61 and overlaps TikTok's $4.26. And it rests on 6 net-new
events, exactly as $44.61 rests on 6.** I am not claiming Instagram is cheaper than TikTok. I
am claiming **the 10x gap is not established for the population the project actually buys.**

### 8a. A second free filter, measured in both directions — and it is HARMFUL

The obvious one is "don't buy a profile for a handle whose address we already hold":

| | n | net-new found |
|---|---:|---:|
| would be **skipped** (store already holds an address) | 40 | **6** |
| would be **kept and bought** | 34 | **0** |

**It throws away all six net-new addresses. Recall 0 of 6.** Not a saving — a 100% yield
wipe-out. The signal runs the *opposite* way to intuition (`P(net-new | store has one)` =
6/40 = 15.00% [7.06–29.07] against 0/34 = 0.00% [0.00–10.15]) — **but I am not publishing
that as a filter either, because it is partly circular and I can prove it.** The store holds
an address for those 40 *because somebody already read that bio*; the bio text was then
discarded — **master stores a bio for only 2 of the 74 rows**, which is BL-1551's nine-site
bio drop reappearing from another angle. The round **cannot separate "predicts" from
"remembers"**, and the two intervals overlap.

## 9. What a clean exit would have to cost, and the clock

At 1.66% you need **60,167 fetches per 1,000 addresses**; at 8.11%, **12,330**.

| | must cost under, per fetch |
|---|---|
| to reach TikTok's $4.26 (at 1.66%) | **$0.0000708** |
| to merely beat $44.61 (at 1.66%) | $0.00074 |

The page is **~626 KB measured**, so at 1.66% that is **35.9 GB per 1,000 addresses** — a
per-GB proxy must come in under **$0.1186/GB**, far below market. **But the JSON endpoint
carries the same bio in roughly a twelfth of the bytes**, moving the break-even to
**~$1.48/GB**, which *is* inside market range. A flat-rate per-IP proxy turns entirely on one
number this round **did not measure and reports as ABSENT: fetches per IP before a block.**
At 1,000/day and $1/IP/month the arithmetic lands near $2.01 per 1,000; at 200/day, near
$10.03. **That spread is the whole question.**

**The clock, measured, never a mean.** Instagram runs 1.4897 s/account → **~24.9 hours per
1,000 addresses** (re-derived independently here from the fetch count, agreeing with the
published figure). TikTok is **~4.1 h**. Instagram's wall is per-IP so it does not
parallelise on one host — **N clean exits divide the clock by N**, so a proxy fixes the clock
as a side effect of fixing the block.

## 10. And a finding that outranks every route above

**0 of 72,971 lead rows carry any outcome.** `date_sent`, `replied`, `bounced`, `converted`
are empty on every row — verified with a positive control on the same pass (`email` reads on
12,977 rows, `platform` on all 72,971, so the reader is not blind).

**Cost-per-address is dominating a decision it is not competent to make alone.** Whether
$44.61 is expensive depends on what an Instagram address is *worth*, and this project cannot
currently answer that for either platform. Two measured facts sharpen it:

* **Only 10.7%** of the 9,544 Instagram addresses on disk came from an `instagram:*` source.
  **82.1% came from Spotify resolution.** The profile call this round set out to cheapen
  produced roughly **1 Instagram address in 10**.
* **The products do not substitute.** `meme_page` is **74.5% Instagram** (1,423 of 1,909);
  `clipper` is **98.5% TikTok** (54,993 of 55,829); `client` is **96.9% Instagram** (14,699
  of 15,173). "Just use TikTok" would kill the meme-page and client lines.

## 11. WHAT I GOT WRONG

**1. My value detector was broken, and it would have reported "no route carries the bio" for
all 154 endpoints.** The first version searched the normalised bio inside the **raw response
body**. The ground-truth bio contains a newline and an emoji; in raw JSON those are escaped
sequences — a literal backslash-n and a backslash-u surrogate pair — so the needle could
never match. It returned **`value=False` on `/v1/user/by/username`**, the shipped route that
demonstrably carries the bio and the very route that bio was bought from. **I caught it only
because I checked the one endpoint whose answer I already knew.** Had I probed the exotic
endpoints first and stopped at a tidy row of zeros, this report would have announced that
Instagram's entire API had stopped returning biographies. Fixed to compare against the
**parsed** structure, proved on planted source, re-run.

**2. I made the exact field-name mistake this brief warns about — inside the script written
to check somebody else's work.** Verifying the `is_verified` lift, I asked rows for
`is_verified` and `follower_count`. The columns are **`verified`** and **`followers`**. Every
subgroup came back `0/0` and my checker printed a clean, confident **0.00%** — a false zero
that would have "refuted" the single most valuable finding of the round. **What exposed it
was that the base rate matched exactly (140/1677) while the subgroups were empty**: a
denominator that agrees while its subgroups vanish means the *grouping key* is wrong, not the
data. Three one-word field-name mismatches have cost this project months each; this is the
fourth, and it took about ninety seconds to make.

**3. I claimed `/sys/balance` was an independent derivation of the unit price. It is not.**
At round start `amount / requests` = 37.3461 / 53999 = **$0.00069161**, within **0.14%** of
the configured $0.00069064 — which I wrote up as a second meter. Then 44 requests were spent:
**`requests` moved by exactly 44 and `amount` did not move at all.** The ratio drifts, and a
round pricing a new endpoint by watching `amount` would have measured **$0.00 for everything
and concluded every endpoint was free.** It *corroborates* the unit; it does not derive it.

**4. A sub-agent reported the local shells were "byte-identical". They are not.** All six
bodies have **distinct sha256 digests**, sizes 625,924–626,413 — per-request nonces differ.
The claim that survives checking is stronger and more specific: they are
**content-identical** — no display name, no bio, no follower count, generic `<title>`, and a
handle that cannot exist gets the same response. I only found this by re-running it myself.

**5. I printed "TikTok: 0.0 hours per 1,000 addresses" from a fetch count I invented.** I
divided by a denominator made up on the spot rather than measured. Retracted in the same run,
replaced with the measured 4.1 h, and the Instagram figure re-derived as a check.

**6. My leak scanner reported a detector BLIND and I nearly weakened the detector to fix it.**
The truth was that **all 80 corpus-A handles are already committed at HEAD** (13 of 13 long
candidates, 40 of the top 40 by length), so the lenient detector — which skips anything
already at HEAD *by design* — correctly had **nothing in scope**. "Blind" and "no control in
scope" are different states. It now reports **ABSENT with the reason**, and the gate rests on
the **strict** public detector, which has no HEAD exclusion and whose own control fires.

**7. I spent the first half of the round on the wrong question, and it was the brief's first
guess as much as mine.** The endpoint hunt was thorough and returned a clean, complete,
well-controlled **no**. The answer was a boolean already arriving in payloads this project
has been paying for and discarding.

## 12. What the round cost

| | |
|---|---|
| **my own counter at the wrapper** (summing vendor `x-hiker-info` receipts) | **46 billable requests · $0.031769** |
| the free `/sys/balance` request delta (independent) | 44 requests · $0.030388 |
| ground truth | **$0.00 — reused BL-1551's 80 paid profiles** |
| routes (b) and (d), every control, every figure in sections 7, 8 and 10 | **$0.00** |
| cap | stop at $0.30, hard $0.50 — **finished at 10.6% of the stop** |

**The round reports the HIGHER of the two counters.** The 2-request gap is responses whose
receipt said `reqs=1` while the vendor pool was not decremented — the 404 fabricated-handle
control is exactly that shape. **Attribution is by my own counter at the wrapper, never a
ledger delta**, because a concurrent funnel writes to `spend.json`.

## 13. What I would do next, in order

1. **Turn on the `is_verified` filter.** It is free, it is already in the payload, it is
   3.2x, and the only thing it costs is recall — which free discovery can absorb.
2. **Stop quoting $44.61 as Instagram's price.** It prices cold hashtag-discovered editors
   and rests on six events. Quote the population with the number, always.
3. **Record outcomes on ~200 already-sent leads, split by platform.** $0.00, machinery
   already wired, and it settles what this whole round is a proxy for. Above every scraping
   route including the ones found here.
4. **Buy one datacentre proxy and measure two numbers**: fetches per IP per day before a
   block, and whether a clean exit serves *small* creator accounts as well as institutions.
   Those decide whether the free page route is worth $2 or $10 per 1,000.
5. **Do not build the "already held" filter.** Measured, it destroys 100% of net-new yield.

## 14. What did not run, reported as ABSENT

* **Whether a clean exit serves small creator accounts.** Not measured. The single most
  important open question about the free page route.
* **Fetches per IP before a block.** Not measured; requires buying proxies.
* **A size-controlled version of the `is_verified` lift.** Structurally impossible on the
  free surface — it carries no follower count. Reported as absent, not as "no confound".
* **The three already-refuted signals** (caps ratio, digit ratio, has-URL; the follower
  floor; the 1.33x size-confounded lift) were deliberately **not re-run**, per the brief.
