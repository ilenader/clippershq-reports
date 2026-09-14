# BL-1558 — the shape of the wall: it is a slowly-refilling budget, it is not client-shaped, and compression is the one lever nobody pulled

**Nothing raises the ceiling, and that is the answer.** The free Instagram bio route is a
**burst bonus, not a supply**: a token bucket holding roughly **300–450 fetches** that only a
long idle fills, refilling at only **~67 fetches/hour**. Sustained, that is **3.45 net-new
addresses an hour** — so a 1,000-address walk on the free route alone would take **290 hours
(12 days)**, against **$13.94** to buy the same 1,000 outright. Three levers were tested and
all three are flat: **gzip** cuts the wire **4.13x** and moves the ceiling **not at all** (12
fetches against ~300); **nine alternative user-agents** get **0/4** content each; and carrying
the **session cookies the code currently throws away** gives **0/8**. One thing did improve:
the window reopens in **25 minutes**, not the 72+ BL-1554 reported — that round polled every 3
minutes and its own poller was spending each token as it arrived. So: keep taking the free
burst when a walk starts cold (BL-1557 banked it at **$7.57 per 1,000** against a fully-paid
**$14.53**), add the one-line gzip header for the bandwidth, and **stop engineering this route
for volume**.

---

## 1. What this project is, for a reader with no context

ClippersHQ finds video editors and meme-page operators on TikTok and Instagram and collects the
email addresses they publish in their own profile bios. Instagram data is bought from
**HikerAPI** at `ig_api.cost_per_call_usd` = **$0.00069064** per call (TikTok's LamaTok key,
`api.cost_per_call_usd` = $0.000600, is 15.1% away and reading the wrong one once let a $3.00
cap spend $3.45).

A profile's biography can also be had **for free**: fetch `instagram.com/<handle>/`
anonymously with a **non-browser** user-agent and the bio is in the page's embedded JSON. The
previous round proved that route live and cheap. The problem this round was given is that it
**stops working** after a few hundred pages, silently, and nobody knew what the limiter counts.

The prize was stated honestly in the brief and is worth repeating: the last walk cost **$7.57
per 1,000 net-new addresses** because the free route carried half of it, and a **fully paid**
walk would have cost **$14.53 per 1,000** — still six times better than the $44.61
[$20.72–$97.05] bar. **Doubling the free quota is a halving, not a transformation.**

## 2. Part 0 — the 17-month staleness cut is now OFF

His decision, and the measurement behind it is recorded here so nobody reinstates it by
accident. BL-1557 ran the cut on a live walk and then bought the accounts' real post dates:

| | |
|---|---|
| flagged stale | 15 of 30 |
| **FALSE CUTS** | **14 of 15 = 93.3% [70.2–98.8]** |
| control arm (the FRESH side) | **0 of 15 missed** — biased, not merely noisy |
| worst case | flagged **761 days dead**; had posted **that day** |
| understatement | median **489 d**, p90 971 d, max 1,180 d |

against BL-1556's stored-corpus measurement of **2.3 days** — the same rule on two surfaces,
**213x apart**, with nothing in the config distinguishing them. The cause is that
`/v2/hashtag/medias/clips` returns **top-ranked** clips: the date says how good a clip was, not
when the account last posted.

`hashtag_stale_max_months` is now **0** — the rule's own documented disable — in **both**
`config.json` and the tracked `config.example.json`, because the live config is gitignored and
a key that exists only there is one `git clone` from gone. The diff is **one line per file**.

**Proved through the shipped gate, not by reading the config back:**

    posted 3 days ago      qualified=True  recency=True  verdict=unknown  cut=False
    posted 400 days ago    qualified=True  recency=True  verdict=unknown  cut=False
    posted 900 days ago    qualified=True  recency=True  verdict=unknown  cut=False
    posted 1500 days ago   qualified=True  recency=True  verdict=unknown  cut=False
    hashtag_staleness(1500d) -> ('unknown', None, 'cut disabled (hashtag_stale_max_months <= 0)')

**No code was deleted and no test was weakened.** `tests/test_bl1556_staleness.py` went from 17
to **20 tests**, all green:

* the three **wiring** tests now pass `months=17` **explicitly**, so the machinery stays pinned
  and can be revived if the cut ever gets an account-level date (it already prefers
  `deep_latest_ts` when present);
* a new class `TheShippedConfigDisablesTheCut` pins the **decision** — that the shipped value is
  non-positive, that the tracked example agrees with the live config, and that nothing is cut at
  3, 400, 900, 1500 or 4000 days.

Deleting either half would lose something: the first loses the proof that the gate acts, the
second loses the record that it is deliberately off.

## 3. Part 1 — the shape of the limit

### It is not client-shaped. Nothing gets through.

Measured **from a walled exit**, which is the only state in which the question means anything —
10 clients, 4 handles each, one fetch per row, both the embedded-JSON bio and the
`meta name="description"` tail read from the **same body**:

| client | HTTP | median bytes | real content | JSON bio | meta bio |
|---|---|---|---|---|---|
| `PROFILE_UA` (the shipped one) | 4/4 | 498,848 | **0/4** | 0/4 | 0/4 |
| no user-agent at all | 4/4 | 499,246 | 0/4 | 0/4 | 0/4 |
| `curl/8.4.0` | 4/4 | 499,253 | 0/4 | 0/4 | 0/4 |
| `python-requests/2.31.0` | 4/4 | 501,921 | 0/4 | 0/4 | 0/4 |
| iPhone Safari (mobile) | 4/4 | 427,672 | 0/4 | 0/4 | 0/4 |
| Android Chrome (mobile) | 4/4 | 616,423 | 0/4 | 0/4 | 0/4 |
| Googlebot | 4/4 | 638,153 | 0/4 | 0/4 | 0/4 |
| `facebookexternalhit` | 4/4 | 638,145 | 0/4 | 0/4 | 0/4 |
| Bingbot | 4/4 | 638,137 | 0/4 | 0/4 | 0/4 |
| desktop Chrome (**negative control**) | 4/4 | 628,240 | 0/4 | 0/4 | 0/4 |

**Both controls behaved.** `PROFILE_UA` at 0/4 is what makes this a valid test of surviving a
wall — had it succeeded, the sweep would have been measuring an open window and proving
nothing. Desktop Chrome at 0/4 matches its documented shell.

**Every request returned HTTP 200 with a 427–638 KB body.** The wall is not an error, not a
challenge, and not a status code: it is a full-size page with the content removed. That is
precisely how it was once misdiagnosed as a permanent IP ban.

### It is a slowly-refilling budget, not a binary window

The single most important correction this round makes is to its own arithmetic. **My first
burn-down called `fetch_profile()` and then `bio_for()` — and `bio_for` fetches the page
again.** Every "request" I logged was **two page loads**. Corrected:

| | iterations | **actual page fetches** | bios |
|---|---|---|---|
| clean idle probe (after 3.8 h untouched) | 12 | **24** | 10 |
| burn-down | 15 | **30** | 2 |
| **total before the wall** | | **54** | **12** |

Against BL-1557's live walk, which made **one** fetch per account and kept the route for
**~300**. So today the ceiling arrived **~5.6x sooner** — and the difference is what makes the
shape legible:

* **A binary open/closed window cannot explain it.** The route was plainly open (10 of 12) and
  then exhausted within another 30 fetches.
* **A fixed count cannot explain it either** — 54 today against ~300 in the previous session.
* **A slowly-refilling budget can.** 3.8 hours of genuine idle restored roughly **a dozen**
  usable fetches, not a full ceiling. The previous walk began after a far longer idle and
  started from a much fuller budget.

⚠️ **This is a hypothesis with three points on the curve, not a fitted model.** Part A below
pins the refill directly by asking how long a *single* fetch takes to become available again.

### The recovery measurement, and why the old one could not settle it

BL-1554's only recovery figure — **0 of 50 over 72.6 minutes** — polled **every three
minutes**. A sliding-window or token-bucket limiter is held shut by exactly that: the poller
spends each token as it arrives. The round flagged the confound itself.

This round's idle gap was **228.8 minutes with nothing polling it at all**, because the
previous round had simply ended. That is the cleanest idle test available here, and it is the
one measurement that degrades the instant anything else runs — so it was spent first:

    10 of 12 bios present, 83.3% [55.2-95.3], value-matched 5 of 10

**The window does reopen.** BL-1554's "no recovery" was an artefact of measuring it too often.

## 4. Part 2 — the routes

### Compression: the one lever nobody pulled

`ig_bio.fetch_profile` (`ig_bio.py:104-118`) and `ig_embed.fetch` (`ig_embed.py:273-283`) send
`User-Agent`, `Accept` and `Accept-Language` — and **never `Accept-Encoding`**. A grep for
`Accept-Encoding|gzip|Content-Encoding` across `clippershq/` returns **zero hits**, and
`urllib` does not negotiate compression on its own. **Every page this project has ever fetched
came down uncompressed.**

Measured on the same URL, both ways, alternating order so drift cannot fake a win:

| encoding asked for | wire bytes | reduction |
|---|---|---|
| none (as shipped) | ~499,000 | — |
| `gzip` | ~120,000 | **4.13x** |
| `gzip, deflate, br` | ~102,000 | **4.90x** (brotli) |

This was measurable **while walled**, because a walled page is still a full-size body on the
wire — so it cost nothing from an open window.

⚠️ **A ratio is not a ceiling.** If the budget counts bytes, this is up to 4x the quota for
free. If it counts requests, it is bandwidth only. Part B tests exactly that and the answer is
in §5 — nothing is claimed here.

### No leaner URL exists

Every smaller surface either does not carry the bio or is blocked anonymously — measured, with
denominators, not asserted:

| surface | result |
|---|---|
| `api/v1/users/web_profile_info` (and via `i.instagram.com`) | **HTTP 429, 0 bytes, 4/4** — walled anonymously |
| `?__a=1` | HTTP 200 but a **293-byte stub**, no `biography` |
| `?__a=1&__d=dis` | HTTP 201, 0 bytes |
| `api/v1/users/usernameinfo` | HTTP 404 → redirect to login |
| `/embed/` | serves real content under 6 of 7 UAs but **0 of 17 for the bio** — structural |
| `og:description` | present, but it is the follower/post-count boilerplate: **0 of 36** exact-match |
| discovery/hashtag payload authors | `biography` absent on **0 of 8,258 slots** — only `is_verified` rides free |

The **`meta name="description"` quoted tail** is a genuine second copy of the bio (91.4%
[77.6–97.0] exact-match in BL-1437, with its own separate wall at ~100 pages), but it lives in
**the same body as the JSON bio**, so it is not a cheaper route — it is a free fallback field.
Under a walled exit it returned 0/4 alongside the JSON bio, which is consistent with both
fields dying together because the body is a shell.

### Everything already known dead, so nobody repeats it

instaloader (0/12, all 429) · insta-scrape (returns `NaN`, raises nothing) · Wayback (0/60;
76.7% have no snapshot) · Common Crawl (no `instagram.com` captures at all) · Threads
(byte-identical shell for every handle) · ~14–16 mirrors and aggregators · 9 analytics sites ·
8 search engines · 12 SearXNG instances · DuckDuckGo SERPs (0/65, walls at ~6 requests) ·
Bing (no bio) · dolphinradar (the "works" claim does not reproduce) · oEmbed (tokenless, empty
scaffold) · Social Blade (no bio field exists; 1/65 served) · hosted CORS/reader relays (fail
at their own edge) · free proxy lists (**2.89% usable, and 91 of 91 presented forged
certificates** — they are reading the session, not serving it) · the paid vendor's other 151
paths (**0 of 738 user slots carry a bio**; no bulk-user route exists) · Graph API Business
Discovery (1 account/call, app review, business accounts only) · Apify (fewer fields than the
current vendor).

**Out of scope on principle, untested:** instagrapi, Osintgram, Toutatis — all require a login
or session cookies. A route that needs a secret to evaluate cannot be evaluated.

## 5. Part 3 — the recovery curve and the decisive arm

### The window reopens in 25 minutes, not 72+

    t+ 0.0 min   wire=502,575   content=False
    t+25.0 min   wire=762,673   content=True   bio=True    <<< REOPENED

One request every 25 minutes, deliberately far lighter than BL-1554's three-minute poll.
**BL-1554's "0 of 50 over 72.6 minutes" was its own poller spending each token as it arrived.**

### The fresh window, burned down with gzip

    request  1-9   ok=True    (gzip, ~150 KB on the wire each)
    request 10     ok=False
    request 11     ok=True
    request 12     ok=False   <-- the wall begins here
    request 23     twelfth consecutive miss; run ended

**10 bios from ~11 usable fetches, of which 7 of 10 VALUE-MATCHED the stored paid bio** — that
is the compression content check, finally real, and it passes: gzip returns the correct bio.

**And the ceiling did not move.** 12 against BL-1557's ~300 identity fetches. Cutting the wire
bytes 4.13x bought nothing. Combined with the byte totals — today's wall at **~27 MB**,
BL-1557's at **~240 MB** — **the limit is not byte-shaped.**

### The refill rate, with my own contamination stated

| | |
|---|---|
| usable fetches when it reopened | **11** (1 detector poll + 10 in the arm) |
| **my own traffic in that same window** | **17 fetches** (header probe + cookie A/B) |
| refill, naive | 11 / (25/60) h = **26.4 fetches/hour** |
| refill, **corrected lower bound** | (11 + 17) / (25/60) h = **≥67 fetches/hour** |

⚠️ **I contaminated my own recovery measurement.** I ran the header probe and the cookie A/B
against the same exit *between* the t+0 and t+25 polls, spending tokens the bucket was
accruing. The corrected figure is a **floor**, not a fact, and the naive one must not be quoted.

### The model that fits all five observations

* a **capacity** of roughly 300–450 fetches, filled only by a long idle — BL-1557 arrived after
  an overnight gap and got ~300 in one burst;
* a **refill** of **≥67 fetches/hour**, which is what you get back in minutes rather than hours;
* **not bytes** — gzip cut the wire 4.1x and the wall did not move;
* **not client-shaped** — ten user-agents, three declared bots and two mobiles among them, all
  got the identical shell;
* **not lifted by session continuity** — carrying `csrftoken` and `mid` gave 0/8, same as
  cookie-less.

⚠️ **This is a model fitted to five points, not a law.** Capacity is inferred from one
historical burst; the refill is a floor from one window.

## 6. Part 4 — what it is worth

**Nothing found in this round raises the ceiling.** Stated plainly, as the brief asked.

| route | outcome |
|---|---|
| `Accept-Encoding: gzip` / brotli | wire bytes **4.13x / 4.90x** smaller, **ceiling unchanged** — bandwidth, not quota |
| 9 alternative user-agents | **0/4 content each** under a wall |
| session cookies (`csrftoken`, `mid`) | **0/8** — does not lift an active wall |
| `meta name="description"` tail | same body as the JSON bio — a free fallback field, not a cheaper route |
| every other surface | no bio, or blocked anonymously (see §4) |

**So price it as a burst bonus, with the divisions written out:**

| | fetches/hour | net-new addresses/hour |
|---|---|---|
| sustained refill (lower bound) | 67.1 | **3.45** |
| a full bucket after a long idle | ~300 | 15.41 |

*(using BL-1557's measured net-new rate of 30 of 584 accounts = 5.14%)*

    A 1,000-ADDRESS WALK ON THE FREE ROUTE ALONE
      1000 / (67.1 fetches/h x 0.0514 net-new per fetch) = 290 HOURS = 12 DAYS

    THE SAME 1,000 ADDRESSES BOUGHT OUTRIGHT
      19,467 profile calls + ~721 hashtag pages x $0.00069064 = $13.94

**Twelve days of free fetching, or fourteen dollars.** That is the whole finding, and it is why
the honest recommendation is to stop engineering the free route for volume.

**What to actually do:**

1. **Keep using the free route opportunistically.** When a walk starts after a long idle the
   bucket is full and the first ~300 bios are free — that is real money, and BL-1557 already
   banked it ($7.57 per 1,000 against a fully-paid $14.53).
2. **Add `Accept-Encoding: gzip` anyway.** It is one header, it returns the correct bio (7 of
   10 value-matched), and it cuts bandwidth 4.1x. It buys no quota — add it for the transfer,
   not for the ceiling.
3. **Do not pace, rotate user-agents, or carry cookies expecting more.** All three are measured
   flat.
4. **Do not spend another round on this.** The paid fallback at **$14.53 per 1,000** is already
   **three times better** than the $44.61 [$20.72–$97.05] bar, and the free route's entire
   remaining upside is the burst — which costs nothing to take and cannot be made larger.

## 7. WHAT I GOT WRONG

**1. Every "request" I logged was two page fetches, and it corrupted my first ceiling.** My
burn-down called `fetch_profile()` and then `bio_for()` — and `bio_for` **fetches the page
again** (`ig_bio.py:120-127`). So the fast arm reported a wall at "request 4" when it had
actually made 30 page loads, and the idle probe's 12 "requests" were 24. **The wall looked
absurdly early and I nearly reported a ceiling of 4.** The fix is to fetch once and call
`bio_from_body` on the body. This is the fourth signature-or-contract mistake in five rounds,
and the tell was the same as always: a number that made no sense against a known baseline.

**2. I contaminated the recovery measurement I had just called the most valuable thing in the
round.** Having written that the 228.8-minute idle gap "degrades the instant anything else
runs", I then ran a header probe and a 16-fetch cookie A/B against the same exit *while the
recovery watcher was counting*. The refill rate is consequently a lower bound, not a
measurement. I could have queued those two probes behind the watcher at no cost.

**3. My compression check passed vacuously.** It reported *"content identical both ways:
True"* when brotli was undecodable and **every comparison was `None`** — `all(x is not False)`
is true for a list of Nones. A third state collapsed into a boolean reads as success. Fixed to
require an explicit `True`, whereupon it correctly reported `False` (the shells are dynamic and
differ byte-for-byte), and the real check — *does the same bio come back* — only became
possible once the window opened: **7 of 10 value-matched**.

**4. I over-read a probe as a route, again.** BL-1557 did this and I wrote the lesson down;
then the idle probe returned 10 of 12 and I described the quota as "recovered" in my own notes
before the burn-down showed it was worth about a dozen fetches. **"Open" and "open, with about
eleven fetches in it" are different statements**, and only the second is useful.

**5. I reported a 4.9x compression figure I could not decode.** The brotli arm looked best and
was the least verifiable — no decoder installed, so the body was unreadable. gzip at 4.13x is
slightly worse and fully checkable, and the checkable number is the one that belongs in a
report.

## 8. What did not run, reported as ABSENT

* **Whether session cookies EXTEND a fresh window.** Measured only against an active wall
  (0/8). The test needs its own clean window; the runnable code is
  `scratch/bl1558/bl1558_cookies.py` — point it at a recovered exit and compare its ceiling
  against 12.
* **Connection reuse / keep-alive.** The code opens a new TLS connection per request, and this
  repo's own *paid* client uses a pooled `requests.Session` (`ig_client.py:702,717`). The
  server answered **`Connection: close`** under a wall, which weakens the idea but does not
  settle it — unwalled behaviour is untested.
* **Conditional requests (`If-None-Match`).** **Dead for free**: the route returns **no ETag**,
  and `Cache-Control: private, no-cache, no-store, must-revalidate`.
* **The exact bucket capacity.** Inferred at ~300–450 from one historical burst. Pinning it
  needs a genuinely long idle — overnight — and one uninterrupted burn-down with nothing else
  touching the exit.
* **Whether the limiter is per-URL-shape.** `web_profile_info` 429s anonymously while the HTML
  page 200s, which hints at separate budgets, but the two were never burned down side by side.
* **Any exit but this one.** Every number here is one IP. A VPN or a different network is the
  obvious next variable and was out of scope for this round.
