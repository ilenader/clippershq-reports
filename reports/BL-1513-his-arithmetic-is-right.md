# BL-1513 — His arithmetic is right, and here is exactly which part of the system disagrees with it

**Round:** BL-1513 · **Filed:** 2026-09-06 · **Cap:** $3.00

---

## What 1,000 delivered pages and 1,000 addresses now cost and take

**His arithmetic is correct and it has been pinned in the repository this round
(`docs/COST_ARITHMETIC.md`), with a test that fails if it ever drifts from the live price
constants.** Every line of it re-derived exactly: 250 calls = $0.17, 1,000 = $0.69, 2,900 =
$2.00, discovery at $0.03 per 1,000 accounts found. His design — free filter first, two paid
calls only on survivors, ~$2.00 per 1,000 delivered — is sound arithmetic on sound prices.

**The system disagrees with it in one specific place, and it is not where anyone has been
looking. It is not discovery.** Discovery is 66.7% of Instagram vendor spend and 69.5% of
TikTok's, but that is a share of a very small number: **$0.0249 on a real run.** The 15,915
accounts a run "discovers" are **read from a file for free**, not bought — 36 discovery calls
cannot buy 15,915 accounts at 22–27 per call, and the seed file on disk holds 15,971. Sizing
discovery down saves **two and a half cents per run**.

**The money is spent on pages that are never delivered.** Measured on two live metered TikTok
runs: **46.5% [38.0, 55.1] of paid calls in memes and 22.8% [17.4, 29.2] in edits land on pages
the funnel never delivers** — and measured against pages that yield an *address*, **96.9% and
95.2%**. The clock has the identical disease: 85.7% of it goes on pages later rejected.

**And on the clock, the honest answer to "10x" is no for Instagram, with arithmetic.** The free
camera's per-IP budget is ~1,036 page loads before a cooldown of at least 8.26 hours. The
physical floor is **124–216 hours per 1,000 delivered on one IP**. Ten minutes would need
23.8–41.7 loads per second; one IP delivers 0.407. **That is 59–102 IPs for a single sprint.**
TikTok's clock does reach the target — 10 to 48 minutes per 1,000 — but its *supply* does not.

**The single largest thing this round changed:** the four fields the TikTok profile purchase
exists to supply are **already present, free, at 100% fill, in the discovery payload the funnel
has already bought** — and nothing extracts them. That was the measured blocker on his "free
first, paid only on survivors" design, and it is now removed.

---

## 0. His arithmetic, pinned — and one correction that changes nothing

`docs/COST_ARITHMETIC.md` is new this round and
`tests/test_bl1513_cost_arithmetic.py` (13 checks) asserts it against
`ig_client.HIKERAPI_USD_PER_CALL` on every suite run, so it **cannot silently drift**.

| calls (Instagram @ $0.00069064) | cost | his figure |
|---:|---:|---|
| 250 | $0.1727 | $0.17 ✓ |
| 1,000 | $0.6906 | $0.69 ✓ |
| **2,900** | **$2.0029** | **$2.00 ✓** |
| 30,000 | $20.7192 | $20.72 ✓ |

**Discovery, at the measured 22–27 accounts per billed call:** $0.0256–$0.0314 per 1,000
accounts found; 60,000 accounts for $1.53–$1.88. **His $0.03 and his $1.82 both sit inside the
band.**

### The one correction

**$2.00 buys 2,900 Instagram calls, not 30,000.** He was exact through 2,000 = $1.38 and then a
decimal slipped; 30,000 calls is $20.72. **His own `2,900 = $2.00` line is right**, so he had
the number and the slip is in the restatement — and his conclusion is untouched, because what
matters is the price per *account found*, not per call.

---

## 1. Where every paid call actually lands

### The headline ratio, TikTok, both modes

Two live metered runs through the production entry point, 299 LamaTok requests, $0.19, counted
at the wrapper by the run's own counter. *Delivered* = `result["passing"]`, the pages the run
presents as wanted.

| | memes | edits |
|---|---|---|
| **paid calls on never-delivered pages** | **46.5% [38.0, 55.1]** (59/127) | **22.8% [17.4, 29.2]** (43/189) |
| per *page* rather than per call | 65.2% (43/66) | 42.0% (34/81) |
| discovery amortised over authors bought | 61.8% | 28.0% |
| **against "with an address"** | **96.9%** | **95.2%** |
| dollars on never-delivered pages | $0.0313 of $0.0928 | $0.0232 of $0.0945 |

Pooled: **32.3% [27.4, 37.6]**.

**Seven denominators, named separately** (memes / edits): discovered videos 1,191 / 422 →
discovered authors 850 / 359 → walked 66 / 81 → captured 31 / 51 → entered the judge 31 / 51 →
judged 31 / 51 → paid pages 66 / 81 → **delivered 23 / 47** → **with an address 2 / 3**.

Two things that ratio hides, reported separately rather than blended: **30.2% of memes paid
calls (55 of 182) are discovery and belong to no page at all** — by construction nothing about
a page decided them. And 2 memes / 3 edits pages bought a paid call and produced no row at all,
because the cap stopped mid-page.

### The same question on Instagram, and the answer is worse

Three live metered runs (memes x2, edits x1), 217 vendor calls and 321 vision calls, $0.1811,
counted at the wrapper. *Delivered* = the pages the run presents as wanted.

| | memes | edits | pooled |
|---|---|---|---|
| **per-page purchases only (profile + posts)** | **69.2%** [58.3, 78.4] of 78 | **68.2%** [53.4, 80.0] of 44 | **68.9%** [60.2, 76.4] of 122 |
| every page-attributable call (+ suggested) | 60.0% of 90 | 58.8% of 51 | 59.6% of 141 |
| every paid call in the run (+ discovery) | 77.2% of 158 | 64.4% of 59 | 73.7% of 217 |

⚠️ **The middle row is the flattering one and it should not be quoted.**
`/v2/user/suggested/profiles` fires *only* on a page that has already passed, so it lands on a
delivered page **by construction**, and what it buys is next run's supply rather than
information about that page. **The per-page figure is the honest one**, and on it the two modes
are indistinguishable. **$0.058 of the $0.084 spent on per-page purchases bought pages that were
never delivered.**

**Every examined Instagram page costs two calls, and the pair is ATOMIC — 39/39 and 22/22, zero
exceptions in either direction.** Nothing between the two calls has ever refused one.

**But the profile call can be deferred, and the posts call does not need it.** The posts endpoint
needs only `user_id`, and **on 61 of 61 pages that bought a profile the `user_id` was already
free on the discovery record** (independently corroborated by the page's own embedded JSON on
56 of 61). Classifying all 61 buyers by what the rule that actually decided them needed:

| class | n | verdict |
|---|---:|---|
| FREE_DECIDABLE — `creator_page` fired, every input free and byte-identical | 5 | both calls avoidable |
| POSTS_ONLY — `photo_heavy` / `stale` / `format_share` / `low_views` / `no_text` | 33 | the profile call was avoidable |
| PROFILE_NEEDED — 19 delivered (the profile carries the contact), plus `too_few_posts` | 23 | genuinely needed |

**38 of 61 (62.3% [49.7, 73.4]) did not need the profile call.** Buying posts first would have
made 79 calls instead of 122 — **35.2% fewer**.

⚠️ **A shipped comment is contradicted by measurement.** `meme_finder.py:7259-7265` states that
`judge_page` reads `full_name`, `verified`, `category` and `media_count` off the profile and
that **none of the four is available free**. Measured on 61 buyers, by sha256:

| field | free? |
|---|---|
| `user_id`, `is_private` | **free, 100%** |
| `full_name` | **free and byte-identical, 56/56** |
| `bio` | **free and byte-identical, 49/49** |
| `followers` | free 91.8%; every disagreement is a live counter moving, worst gap 0.051% |
| `verified` | **free in the payload on 96.4% of accounts but NEVER MAPPED** — a packing gap, not an availability gap |
| `category`, `media_count` | **genuinely paid-only** — 0 of 816 discovery accounts carry either |

So two of the four are free, one is free and thrown away, and only two are really bought.

**The free gate pays for itself 5.6x:** 127 pages killed before any purchase avoided 254 calls
($0.1754) for $0.0312 of vision.

⚠️ **And the free vision gate behaves completely differently between the two brains:** it killed
**73.6%** [66.2, 79.8] of memes pages against **31.2%** [18.0, 48.6] of edits pages — disjoint
intervals — so 24.5% of decided memes pages buy a profile against **68.8%** of edits pages. It is
*not* `bars_kill` (1 free-kill in 191). Three candidates remain unseparated, and I am not
guessing between them: the edits addendum, the exemplar pack (**both** brains fall back to
`PINNED_EXEMPLARS`, which is declared *tiktok*), and the wall shrinking edits' grid supply.

⚠️ **A discovery channel was bought and never looked at.** In memes mode the run paid for 12
reels + search discovery calls — **34.3% of its discovery spend** — and reached a decision on
**zero** of the accounts they bought. The walk order exhausts its page slice on hashtag pages
first, so that supply is banked and never consumed within the run.

### What decided each call, and whether a free answer came first

The order inside `discover._process`, established by AST rather than by reading:

```
:2507  free recency pre-gate      <- the ONLY free rule that sees discovery data
:2535  PAID evidence call
:2563  author["videos"] REBOUND to the paid videos
:2683  the free RULE ENGINE runs  <- twenty lines too late to have been free
:2722  free bio email
:2750  PAID profile
:2927  free cover rules
:3031  PAID model judge
```

**The free rules already exist. They simply run after the purchase.** Of pages cut *after*
paying, 16 of 41 memes and 7 of 31 edits were cut by rules whose inputs discovery already
carries.

⚠️ **The evidence call is bought to clear a floor it cannot clear.** The remainder were cut at
the evidence floor, which needs 3 videos while discovery yields 1.18–1.37 per author — so that
rule genuinely cannot be answered from discovery. **But the paid call did not answer it either:
every page cut at the floor ended holding 1 or 2 videos.** 39.1% [28.1, 51.3] of memes evidence
calls and 30.8% [21.6, 41.7] of edits ones were bought to clear a floor and came back still
under it.

⚠️ **Two free cover rules and the paid judge sit BELOW the profile purchase.** Every one of the
8 memes / 4 edits pages cut by a cover rule had already bought its profile — 24 memes and 13
edits paid calls spent on pages a rule reading *free* covers then discarded. The funnel already
proves those covers are free: it built 52 memes / 14 edits reject sheets from discovery covers
alone.

### ⚠️ The "free" picture judge is not free, and the run cap does not bind it

`free_judge.PAID_FIRST = True`. Across both runs, **89 of 89 model calls went to a paid model;
zero went to a free one.** It books through `_book_paid_call`, which sits **outside**
`tiktok_max_run_usd` — so the per-run cap the operator sets does not constrain it.

### The TikTok profile gate, re-derived — the old control was an identity

The received figure was *"1,258 of 1,258 bought profiles ended as targets, 0 later rejected"*.
**That is not a control.** `profile_bought` is a hardcoded `False` literal at four early-return
paths (`:2524, :2638, :2674, :2695`, proved by `ast.Constant`, not grep), all above the purchase
at `:2750`, and exactly one site can write `True`.

But *"unreachable by construction"* is **too strong** — a second AST pass finds five writers
between the purchase and the row write, so the off-diagonal *is* expressible today. Re-derived
by era, from 20 shipped run exports, deciding each run's era from its own export:

| era | runs | bought | rejected after buying | waste |
|---|---:|---:|---:|---:|
| nothing between the buy and the row write | 8 | 1,185 | **0** | 0.0% |
| the cover-rule block exists | 12 | 188 | 20 | 10.6% [7.0, 15.9] |
| **the picture judge actually fires** | 5 | 117 | 20 | **17.1% [11.3, 24.9]** |
| **this round's two live runs** | 2 | 80 | 12 | **15.0% [8.8, 24.4]** |

**The honest figure: the profile purchase is wasted on 15–17% of the pages it is made for.** The
old figure was *correct for the code it measured* and says nothing about today's.

⚠️ One run export was **excluded**: it carries no `billed_calls`, no `export_reason`, and its
rows carry a `_population` key — it is a hand-built pool from an older round, not a run export.
Including it would have manufactured an 11.6% figure out of superseded behaviour.

The quoted *"12.64% of rows reach the gate / 4.62% of those buy"* **could not be reproduced
under any denominator**. The reproducible reading is 55.8% of pooled rows reach the row write,
and 92.4% of those buy.

---

## 2. The fix his design needs — and it is now unblocked

**All four fields the TikTok profile purchase supplies are already in the discovery payload the
funnel has already paid for, at 100% fill, and nothing extracts them.**

| judge line | free path already in the payload | fill |
|---|---|---|
| `display name:` | `author.nickname` | **762/762 = 100%** |
| `followers:` | `authorStats.followerCount` \| `authorStatsV2.followerCount` \| `author.follower_count` | **762/762 = 100%** |
| `verified:` | `author.verified` \| `author.verification_type` | **762/762 = 100%** |
| `N posts read` | `authorStats.videoCount` \| `authorStatsV2.videoCount` \| `author.aweme_count` | **762/762 = 100%** |

`tiktok_finder._video_of` already lifts `signature`, `nickname` and `authorStats.videoCount`
from those two blocks **and stops**. `followerCount` and `verified` are in the same objects and
are discarded.

**Free vs paid on 99 paired authors, live:** display name 99/99, verified 99/99, biography
99/99, post count 98/99, followers 80/99.

⚠️ **The followers gap is a CLOCK, not a free-vs-paid property.** Reading the same free source
twice five minutes apart, followers disagrees **with itself on 15 of 38 (39.5%)** — a *higher*
rate than it disagrees with paid (21.1% on those same 38). Display name, verified and biography
moved 0/38. All 20 prompt-level misses classified: free wrong **0**, paid wrong **0**, both
defensible (different instants of a moving counter) **20**. Today's prompt is already not
reproducible on that line, with or without the purchase.

**Byte identity:** `facts` reaches the prompt through exactly one load site (AST). Driven
through the shipped judge on a real sheet: 79/99 prompts identical, **98/99 identical excluding
the live follower counter**, 10/12 full-prompt sha256 identical end to end. One-byte controls
all caught.

**Volume ceiling: zero extra requests.** The fields ride on the response the parser already
reads — same object, same call — so the ceiling is the funnel's own discovery volume, 1:1. No
degradation across 31 consecutive buckets.

**Verdict: the purchase can move.** An 8-hunk anchored patch recipe, a `--check` applier that
refuses on a rotted anchor, and an AST-driven byte verifier were produced and **deliberately
not applied** — see §6.

### Discovery sizing: the lever that is not there

⚠️ **"It buys discovery for roughly 1,700 accounts for every one it judges" is wrong about the
word BUYS**, and the difference decides whether the top recommended lever saves any money. Two
proofs sharing no mechanism:

| proof | result |
|---|---|
| **arithmetic** — 36 discovery calls at 22–27 accounts each yield **at most 972** | 15,915 is **16x impossible** |
| **the file** — `seed_accounts_file` on disk | **15,971 handles**, read free at run start |

15,971 − 15,915 = **56**, and the funnel *appends* to that file during a run, which is exactly
what the gap is.

- discovery spend on that run: **$0.0249** (genuinely 66.7% of $0.0373)
- if those accounts *had* been bought: **$0.45**
- **cutting discovery to zero saves two and a half cents per run of that size**

Accounts *entering the walk* per page judged: **1,768 : 1**. Accounts *bought* per page judged:
**at most 108 : 1**. **The supply glut is real; the spend glut on discovery is not.**

---

## 3. The clock — the physical floor, and what 10x would require

### Instagram: NOT REACHABLE, and the arithmetic says so

The free camera's wall is a **per-IP page-load budget**: ~1,036 loads, then **≥8.26 hours dark**;
1,464 loads/h in burst, **115.5 loads/h sustained**. Independently, the best 24-hour window in
this project's entire history is 2,074 loads = 86.4/h. Loads per delivered page: median 14.3,
p90 48.0.

**Physical floor: 124–216 hours per 1,000 delivered, on one IP.**

⚠️ **The published 43.8 hours cannot be reproduced — it sits 2.8x BELOW the physical floor.** It
came from a run with 50 captures and 2 delivered, and ended before the wall existed. Re-derived
with no wall model at all, 1,000 delivered needs **1.6–2.8x more Instagram page loads than this
project has made in its entire existence** (9,048 loads in 536.8 hours).

**Ten minutes needs 23.8–41.7 loads per second. One IP gives 0.407.** That is **59–102 IPs for
one sprint, and 3,153–5,513 for a repeatable cadence.** Even 10x — 4.4 hours — is **28x below
the floor**.

**The blocker, named:** the per-IP page-load budget of the free camera. `page_capture.py`
contains "proxy" **zero times** (positive control: "headless", which it really does read,
appears twice) and the browser launch takes no proxy argument. **The only route around it is
buying the grid — about $19.73 per 1,000 delivered — which converts the blocker from physics
into money.** That is the operator's call, not mine.

### TikTok: the clock reaches it, the supply does not

**10 to 48 minutes per 1,000 delivered.** No per-IP wall; it buys from a keyed vendor measured
at 432–535 profiles/min at 32 lanes, zero retries, no throttle. But at ~40 discovered authors
per delivered sheet, ten minutes would need ~40,000 authors, and search saturates at page 2
while still reporting `has_more: true`.

### The free route that is proven and unshipped

**urlebird**, 235 requests, disjoint handles, $0. An honest **HTTP 429** with a rate-dependent
onset: serial no-sleep (0.86 req/s) **dies at request 33**; **4 lanes kill it in under 5
seconds**; paced at 0.33 req/s, **120 requests clean** — and an earlier round independently ran
368 at that pace with flat yield. **It recovers in 1–15 seconds** — a token bucket, not a ban,
the opposite of Instagram's 8+ hours. Ceiling ~**1,190 requests/hour per IP**, so 1,000 pages is
50 minutes on one IP. **Bio only — never a grid.**

The positive control earned its keep: 3/3, 3/3, then **0/3 immediately after the 4-lane phase** —
which is what proves the wall is IP-wide rather than 28 coverage misses.

**Dead ends not repeated** (previously measured and refused): instaloader 0/12, insta-scrape,
Wayback 0/60, Common Crawl, Threads, 14 mirrors, Scrapling 0/20, socialblade.

---

## 4. The prices — a defect named at five constants existed at seven

BL-1496 replaced retyped Instagram prices with imports of the declared owner in **five** files.
This round found the **sixth and seventh**, by two different instruments:

| # | site | defect | found by |
|---|---|---|---|
| 6 | `harvest_accounts.USD_PER_CALL = 0.0006` | **the wrong value** — LamaTok's rate on an Instagram walk, 15.1% low | **driving the budget cap** |
| 7 | `suggest_harvest.PRICE_PER_CALL_USD = 0.00069064` | right value, retyped — the second copy that makes the next drift possible | **a regex keyed on the right value** |

⚠️ **The sixth is the default unit of the budget cap.** `harvest_run.Budget(cap)` takes
`unit=HA.USD_PER_CALL`, so **a $3.00 cap permitted 5,000 calls — $3.45 of real spend.** Driven
before the fix: 5,000 allowed. After: **4,343**.

**The trap the brief names was checked before touching either file:** one constant billing both
vendors would have inflated TikTok by 15.1% in the same edit. Both files contain **zero**
TikTok/LamaTok references and all four use sites are inside the Instagram harvest path — so this
statement is **scoped to those two files**, not a claim about the whole tree.

**Category: GENERAL** for both — one owner, so an eighth site cannot happen silently:
`tests/test_bl1513_cost_arithmetic.py` fails if any module retypes the price, with a positive
control proving the detector matches a planted assignment.

**Two instruments found two different sites, which is the argument for keeping both.**

---

## 5. Verifying the cap before the first page

Driven against the real `harvest_run.Budget.reserve`, not reasoned about:

| arm | expected | result |
|---|---|---|
| cap $1.00, first call | ALLOW | ✓ |
| cap for exactly 2 calls, 3rd call | REFUSE | ✓ `BudgetExceeded` |
| **cap $0.00, first call** | **REFUSE** | ✓ — **zero is not unlimited** |
| cap −$1.00, first call | REFUSE | ✓ |

The refusal is an **exception, not a return value** (a caller cannot ignore it by accident), and
**the meter does not advance on a refusal** — checked, because a meter that books the call it
refused reports spend that never happened.

---

## 5a. The zero-tile captures — the one pure-waste line, fixed

**Measured over 3,595 captures: 882 return zero tiles — 24.5%.** They cost **16,270.7 s of
41,100.8 s of capture clock — 39.6%** — for no picture at all. Capture is free in dollars, so
**this is a clock fix, not a cost fix**, and it is the second-largest consumer of clock after
the vision judge (which is already parallelised 4.5x and is not the bottleneck).

**The causes, counted separately because they are different facts and need different answers:**

| cause | n | what it is |
|---|---:|---|
| **private** | 392 | **PERMANENT** — never retry, never latch |
| **login wall** | 310 | a wall — **UNJUDGED, never a rejection** |
| unknown | 176 | no cause recorded |
| no reason recorded | 4 | |

A zero-tile capture is **not** a rejection. A wall, a torn download, a timeout and a private page
are four different states, and the private ones are **detectable before the capture is paid for
in clock at all** — which is where the saving is.

**Before and after, same 39 pages, same instrument:**

| | before | after |
|---|---:|---:|
| capture seconds, **median** | 9.06 | **0.84** |
| capture seconds, p90 | 12.65 | 9.00 |
| **total capture clock** | **345.4 s** | **91.5 s** |
| pages over the slow threshold | 30 | **6** |
| zero-tile pages, median | 12.41 | 0.82 |

**3.8x less capture clock on the same pages, and the median page is 10.8x faster.** Median and
tail are reported separately because the tail is where the wall lives: p90 falls only 12.65 →
9.00, so **this fixes the common case and not the walled one** — and it must not be read as
having fixed the wall.

⚠️ **A denominator correction to my own first draft of this section.** I wrote that the fix
"addresses 1,060 of the zero-tile captures". **1,060 is not a count of zero-tile captures** — it
is the number of records captured by *today's* code, the corpus the projection runs over. The
correct statement: projected over those 1,060 records (4.30 h of capture), the fix recovers
**3,920 s of decode + 1,085 s of settle = 1.39 h, or 32.3% of capture clock.** Independently
corroborated by an untouched real-browser suite going **74.3 s → 27.9 s**.

**The mechanism, because it is a GENERAL fix and not a tuning:** the decode wait tested
`if (tiles.length < 6) return false` — a bound that a page with fewer than six tiles can never
satisfy. Measured on those 1,060 records: **0–5 tiles timed out 100% of the time at every count;
6+ tiles timed out 0.0%. Zero crossover.** **534 of 1,060 pages (50.4%) burned the full 8,000 ms
by construction**, and **230 pages corpus-wide had a perfectly good grid and shipped it anyway.**
Fixed by comparing against the page's own ceiling rather than a fixed 6. A second GENERAL fix
collapsed three copies of "has this page settled?" into one chokepoint — two earlier rounds had
fixed one copy and then two of three, so the classifier knew a page was a wall while the *wait*
did not (12.37 s against 8.85 s for the same wall in older wording).

**And a live paired A/B on real Instagram, $0.00, one browser on one IP, arm order shuffled:**

| | median | p90 | max | total |
|---|---:|---:|---:|---:|
| old | 2.63 | 10.17 | 13.12 | 66.4 s |
| **new** | **2.12** | **2.72** | **2.77** | **30.5 s** |

**The tail is all of it** — only 4 of 14 pages moved at all, and the ten healthy 8–12-tile pages
moved ≤0.6 s in either direction.

⚠️ **THE NO-VERDICT-MOVED CONTROL FOR CAPTURE: 0 differences on 39/39 fixture pairs and 14/14
live pairs**, across tiles, clip width, shot count, base pixels, suppressed-shot and HTTP status.
And the one genuinely unclassifiable page moved 12.48 → 12.41 s — **unchanged, which is the proof
that no new gate was added.**

⚠️ **Two fixes were deliberately NOT shipped, because both would change what the judge sees.**
Instagram's real 404 string is missing from the not-found detector, and the age gate is now
*named* but not suppressed — fixing either would remove a picture from the judge's queue, which
is a judging change wearing a bug-fix's clothes. Both are recorded in-source so they are not
"tidied" later. The age gate remains a fifth state that is photographed and judged as a profile.

⚠️ **And a false-zero the agent caught in its own first pass:** keying the population on "has a
handle" swept in a TikTok delivered-state file and produced **112 false zeros**. Excluded.

⚠️ **No judging rule was added or loosened and no threshold moved.** Capture is upstream of
judging; what changes is how long the funnel spends discovering that a page has no picture, not
what the judge then does with it.

---

## 5b. Making the cost visible forever — five fixes, all GENERAL

**The reason no per-stage figure in this project has ever existed:** spend rows carried no
`run_id`, no `stage` and no `funnel` — **0 of 26,963**, against a control showing `label` on
26,944 of the same rows. And `label` names a **module**, so `meme_finder` was one **$13.19**
bucket covering discovery, capture, the profile purchase and the contact fetch together.

| # | fix | category | proof |
|---|---|---|---|
| 1 | `run_id` + `stage` at the booking site | **GENERAL** | live production rows |
| 2 | no anonymous autoflush | **GENERAL** | raises on `unattributed` |
| 3 | Instagram profile-purchase counter | **GENERAL** | 2/2 vs an independent wire count |
| 4 | provenance sink stops overwriting measured counters | **GENERAL** | 5 negative controls |
| 5 | the crash handler | **GENERAL** | driven on a cp1252 console |

**1 — patched BOTH locked implementations and forwarded from both wrappers.** That is the
BL-1496 trap: adding a kwarg to a wrapper whose arithmetic lives in the locked function ships a
`NameError` on every call. 21 call sites reaching a ledger writer were enumerated by AST.
**Proved on live production rows** — a peer round's run, which I never instrumented, is writing
through the patched booker right now:

```
BEFORE  {"campaign":"MEME_FINDER","label":"meme_finder","calls":1,"ig_usd":0.000691}
AFTER   { ...same..., "run_id":"meme_pages-…-a633",
                      "stage":"/v2/user/suggested/profiles", "stage_bucket":"discovery" }
```

**432 real rows now carry `run_id` across 11 run ids**, all written by other rounds.

**The stage vocabulary is a peer round's and I adopted it rather than inventing a second one:**
`stage` is the **raw endpoint path**; `stage_bucket` is one of exactly
**discovery / capture / judge / profile_contact**. The endpoint is what the money is actually
spent on, so it cannot drift from a label somebody has to remember to update — and this project
has three recorded cases of exactly that drift (`bio`/`biography`, `media_count`/`posts`,
`followers`/the renderer's spelling). `validate_stage` **raises** on a near-miss (`discover`,
`profiles`, a missing leading slash): 4/4 refused, 0 rows written. The endpoint map holds **both
vendors**, precisely because wrapping only one client is what gave a peer round a false zero.

**2 —** the `unattributed` bucket (328 rows, $2.4480, 3.96% of lifetime spend) is closed at the
point the value ENTERS: `configure_autoflush` raises on empty / `unattributed` / `unknown` /
`aux`, and the constructor supplies the constructing module as an **observation off the live
stack**, so "I don't know" is never the recorded state. `flush_spend` now writes **one row per
endpoint**, books the remainder rather than dropping it, and advances the watermark per row so a
mid-flush failure cannot re-book.

**4 —** the heartbeat kept ticking ~26 lines after the funnel's real counts were written.
Driven on shipped code: **discovered 98 → None, delivered 7 → 3** from one tick, and **0 of 77**
run records that declare the five counters carried a measured value (control: the same reader
finds `funnel` on 226 records). Now a measured counter cannot be un-measured, and a provisional
tick fills gaps but never argues with a measurement.

⚠️ **What this does NOT close: TikTok still books nothing at all.** `api_client.py` makes **zero**
calls to any booker (control: 15 other modules do). Adding a stage to the Instagram path does not
make TikTok's spend visible, and the `tt` meters keep `stage=None` deliberately — `tt_calls` is a
remainder, and a stage there would be a guess dressed as a measurement.

---

## 6. What I did NOT do, and why

* **I did not move the TikTok profile purchase, or reorder any paid call.** `tiktok_finder.py`
  and `free_judge.py` are claimed by another live round whose entire brief is that lever. The
  measurement, the fill table, the byte-identity proof and an applier that refuses on a rotted
  anchor were handed over instead. Doing it myself would have put two rounds in one file.
* **I did not re-measure the Instagram cooldown.** It would take the free camera offline for 8+
  hours for every other live round. **8.26 h therefore stands as a lower bound, and the clock
  floor is optimistic by however much the true figure exceeds it.**
* **I did not run the TikTok lane sweep** — it contends with live funnels.
* **I did not fix `meme_finder._png_area`'s silent zero** (mine, from BL-1505). The honest
  repairs change a shipped grid chooser's failure behaviour and need their own measurement.

---

## 7. What I got wrong this round

* ⚠️ **I worked under another session's round id for thirteen minutes.** I checked
  `docs/claims/` — 127 published manifests — saw no BL-1509, concluded the id was free, and
  never filed. **The live registry is `.claims/`.** A peer caught it. Everything was re-filed as
  BL-1513 and renamed; the other round's three files were identified by content and left
  untouched.
  **This is worse than a silent failure: it is a CONFIDENTLY WRONG one.** Two directories differ
  by a path segment, one is an archive and one is a live registry, neither contains a readme
  naming the other, and the archive answers a question about the *present* with a plausible,
  confident, wrong answer. **A session lands in it precisely because it did the diligence** — the
  careless session that never checks is unaffected.
* **And the same instrument fails in the opposite direction on exit:** my own finished BL-1507
  claim was still reserving two production files two hours after it published, blocking the peer
  whose round wanted them. Nothing forces a claim to be ended, and a stale claim is
  indistinguishable from a live one. Released.
* **I introduced a `NameError` in my own harness** — a variable used nineteen lines above its
  definition. `ast.parse` accepts that happily. Caught by an AST unbound-name checker, not by
  reading.
* **My first before/after harness wrote to the real seen store**, which would have let the BEFORE
  run poison its own AFTER by marking every page it walked. Redirected to copies. No row was
  removed from any store — verified by **row key sets** against the round-start backup, with a
  control proving the comparison can detect a removal.
* **I guessed at `estimate()`'s internals twice** while repairing a test, and was wrong both
  times (`usd` is priced off the *fractional* call count, not `billed_calls`, which is a
  ceiling). Fixed by reading the function instead of paraphrasing it.
* ⚠️ **A record correction, because a sub-agent flagged an unexplained write and it deserves a
  plain answer: I applied the `control.py` patch myself.** Its own script printed "NOT APPLIED"
  and gated on a `--apply` flag precisely because a concurrent round had pinned that file; I
  relayed the diff to both rounds, both replied "LAND IT", and I then ran `--apply`
  deliberately. `git diff` equals the prepared patch exactly — 65 lines added, 1 removed, none
  present that are not in the patch. There was no third-party write and no mystery.
* **My first backup helper read a 2,193-row store as 0 and a 26,947-row ledger as 8**, because it
  searched only for dict bodies and both are **lists**. That is the exact failure the safety rule
  warns about, reproduced inside the checker meant to prevent it.

---

## 8. The suite, and spending

### The suite

No peer suite run was live, so the full suite was attempted in slices.
**90 suites run, 1 failure in those slices** (three pre-existing reds in total across the round), and I **re-derived** that red rather than inheriting a count:

`test_bl1307_veto_refused` — caused by an untracked `scratch/bl1441_ast_sink_tests.json` dated
**30 August**, which predates this round by a week. It has been red in every full run since at
least BL-1440. Not caused by anything here.

**Two further pre-existing reds were found by sub-agents and are named rather than folded into a
count:** `test_bl1359_ig_cost_fixes` and `test_bl1389_no_caller`. Both were verified red
**before** any change by restoring the pre-patch file and re-running — not assumed.

Additionally the sub-agents ran their own affected families green: ledger 53, funnel 833, caps
30, vendor 21, `run_` 123, headless 47, panels 28, spend 8, status 5, plus the new
`test_bl1513_cost_arithmetic` at 13 and the repaired `test_harvest_accounts` at 36.

⚠️ **Stated plainly rather than implied: this is not the whole suite.** 444 suites exist and a
full serial run takes 44 minutes against a 10-minute execution ceiling, so ~90 were run directly
plus the families above. **I am not claiming a green suite; I am claiming 90 suites and nine
families with one pre-existing red.**

⚠️ **And one red is reported that a sub-agent found and could not have caused:**
`tests/test_bl1359_ig_cost_fixes.py` is red because a **byte-window guard** slices
`meme_finder.py` and misses `stats["judge_batches_pages"]`, which **is** present twice. That
file is byte-identical to HEAD and the test reads only it. This is the fourth byte-window guard
in this repo to go red on correct code; the standing repair is to rewrite it as AST.

### Spending — $0.5034 of a $3.00 cap

Every figure is the run's **own in-process counter**, taken at the wrapper before the request.
**No ledger delta was used as a meter** — `spend.json` is shared and gained ~1,400 rows from
peer rounds while this one ran.

| source | vendor | calls | USD |
|---|---|---:|---:|
| TikTok paid-call audit | LamaTok | 299 | 0.1794 |
| TikTok model judge | model | 89 | 0.0079 |
| Instagram paid-call audit | HikerAPI | 217 | 0.1499 |
| Instagram vision | model | 321 | 0.0312 |
| free-field proof | LamaTok | 155 | 0.0930 |
| clock floor | — | 0 | 0.0000 |
| my two before-runs | LamaTok | 70 | 0.0420 |
| **TOTAL** | | | **0.5034** |

**Booked explicitly**, because `clippershq/api_client.py` contains **no booking of any kind** —
every LamaTok request any round has ever made was invisible to the ledger:

```
BOOKED: 524 LamaTok calls x $0.000600 = $0.3144 under campaign BL-1513
rows before 27,756 -> after 27,757    added: 1    mine: 1
```

⚠️ **Only the LamaTok calls are booked here.** The HikerAPI and model calls are booked by their
own clients; re-booking them would inflate the ledger by exactly the amount this round exists to
make visible. The safety check is **the row** — one row carrying my campaign and my call count —
never the file total, which a concurrent peer write would break.
