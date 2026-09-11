# BL-1547 — the overnight research round (INTERIM, half-time)

> **THIS IS AN INTERIM FILE, PUBLISHED AT ROUGHLY THE HALFWAY MARK SO A CRASH COSTS ONE HALF OF
> THE NIGHT RATHER THAN ALL OF IT.** Two of six sweeps have returned; four are still running. The
> same filename will be updated in place when the round finishes — there is one report file for
> this round and there will only ever be one. Anything below marked NOT VERIFIED stays that way
> until it is.

**The biggest thing nobody had looked at, so far: the bio text.** It is free on 88.08% of
TikTok hashtag authors and no round had ever measured it. Measured now on 64,307 present bios, a
business-intent keyword filter selects 7.65% of accounts and captures **50.5% of all
address-carrying bios** — precision 23.1% [21.9–24.3] against a base rate of 3.49% [3.36–3.64],
a **6.6x lift**. But the honest follow-up killed the obvious use of it: the bio arrives *free*
with the page you already bought, so the signal saves nothing at account level, and my attempt to
lift it to **tag** level — where the money actually is — **failed** (Spearman rho = −0.008 across
314 tags). What it is worth therefore depends on where a per-page cost sits *after* the bio is
known, which the still-running cost sweep is measuring.

---

## 1. What this project is, for a reader with no context

A funnel discovers TikTok and Instagram accounts belonging to video editors ("clippers"), reads
their public bios, and extracts published email addresses into a lead store
(`master_leads.csv`, 72,971 rows). Vendors: LamaTok for TikTok at **$0.000600 per call**,
HikerAPI for Instagram at **$0.00069064 per call**. The goal, against which everything here is
judged: **more clipper email addresses, for less money, in less time, with fewer wrong ones.**

This round **ships nothing**. `clippershq/` was read-only throughout; every write went to
`scratch/bl1547/`. Defects are named with file:line and left in place.

## 2. Safety, and the cap, before anything else

**Nine stores backed up, sha256-verified, bodies found BY SHAPE rather than assumed** — a backup
that counted top-level keys would have reported "3" for a store holding 3,270 rows:

| store | body | rows |
|---|---|---:|
| `spend.json` | dict → `runs` | 35,210 |
| `master_leads.csv` | csv | 72,971 |
| `clip_seen.json` | **bare list** | 2,193 |
| `meme_pages_seen.json` | dict → `pages` | 6,196 |
| `tiktok_pages_seen.json` | dict → `pages` | 3,270 |
| `spotify_playlists_seen.json` | dict → `playlists` | 1,960 |
| `repost_seen.json` | dict (whole) | 1,715 |
| `email_harvest_tags.json` | dict → `tags` | 572 |
| `config.json` | dict (whole) | 173 keys |

**All five corruption controls FIRED on planted damage.** The load-bearing one is C4: given a
duplicated pair, deleting one leaves the natural-key **set identical**, so a key-set check is
*provably blind* — measured, both digests equal — while an **index-qualified** fingerprint moves.
C5 showed that renaming a body key collapses the shape probe from 6,196 to 5, so it cannot
silently accept a wrapper as if it were the rows.

**The spend cap was proved to bind before a cent was spent.** The shipped `Budget` class was
lifted out of `harvest_run.py` by AST (so it cannot drift from production) and driven through
`LockedBudget` under **8 threads × 50 attempts** against 20 calls of headroom:

- funded budget allows and the meter advances by exactly one unit — `spent $0.000600, calls=1`
- a `$0.00` budget raises `BudgetExceeded` on the first call
- **the meter does not advance on a refusal** — `spent $0.000000, calls=0`
- 8 threads got **exactly 20 allowed / 380 refused**; `spent $0.012000 = 20 × $0.000600`
- the unit was passed explicitly from the **named key** `api.cost_per_call_usd`
- `Budget`'s own default unit is `1e9` — it **fails closed** rather than silently pricing a
  TikTok call at the Instagram rate

**The proof wrote nothing**: `spend.json`'s md5 was identical before and after.

## 3. Territory 1 — the vendor specs, re-read live

A version number is not a change detector, so the live specs were fetched and diffed against the
cached copies on disk. **An OpenAPI document is public and unauthenticated — this is not a billed
call and it did not touch the round's budget.**

| vendor | cached | live | new paths | removed |
|---|---|---|---:|---:|
| LamaTok | 1.3.3 / 23 paths | **1.4.5 / 29 paths** | 6 | 0 |
| HikerAPI | 1.8.0 / 154 paths | **1.8.1 / 154 paths** | **0** | 0 |

The LamaTok 23→29 jump is the one a prior round already found; the version has since caught up, so
the "same version number" trap is not currently active. **HikerAPI adding nothing across a version
bump is a genuine negative result** and is recorded so the next round need not re-fetch it.

**Then the endpoint-level version of the unread-field question: of the 29 live LamaTok paths,
production references 9 and does not reference 20.** Controls passed first — a known-used path
(`/v1/hashtag/medias`) was found, an invented one (`/v9/bl1547/control/never`) was not.

Referenced: `/sys/balance`, `/v1/hashtag/info`, `/v1/hashtag/medias`, `/v1/media/by/url`,
`/v1/media/video/download/by/id`, `/v1/user/by/username`, `/v2/hashtag/medias`, `/v2/search`,
`/v2/user/medias/by/secUid`.

Of the 20 unreferenced, three look relevant to the goal and are **flagged, not recommended** —
none has been priced:

- **`/v1/user/following/by/username`** and **`/v1/user/following/by/secUid`** — paginated
  following lists. This project has already refuted *suggested-profiles* and recorded that
  *following* beats it, yet **neither following endpoint is wired to anything.**
- **`/v3/user/by/username`** — summary reads *"Userinfo By Username (incl. unavailable
  profiles)"*. That is a different capability, not a version bump.
- **`/v2/hashtag/info`** — v1 is used, v2 is not.

### A spend I refused, with the arithmetic that refused it

`/v3/user/by/username` looked worth probing until the prize was sized for free. Across 73,009
harvested account rows, **8,702 (11.92%) arrive with an empty bio** and yield zero addresses;
64,307 (88.08%) have a bio, of which 3.49% carry an address. Best case, if a paid profile call
recovered a bio for *all* 8,702 at the same rate: 8,702 × $0.0006 = **$5.22** for ~304 addresses =
**$17.17 per 1,000 addresses**, against the harvester's measured **$2.47 per 1,000** on fresh tags.
**6.9x worse in the best case, so no probe can rescue it.** $0.00 spent.

*(Note: 88.08% bio-present is below the 91–93% the brief quotes. Flagged as a discrepancy between
denominators, not as a correction.)*

## 4. Territory 2 — the bio text, measured for the first time

Denominator: 73,009 account rows; **64,307 with a bio present**; 2,247 carrying an address, **all
2,247 of them from a present bio**. Base rate to beat: **3.49% [3.36–3.64]**.

| signal | precision | recall | n selected | verdict |
|---|---|---|---:|---|
| business-intent keyword | **23.1% [21.9–24.3]** | **50.5% [48.4–52.6]** | 4,922 | **6.6x base** |
| bio length 51–150 chars | 5–9% | — | — | weak, likely proxies "longer bio" |
| newline ≥1 / ≥2 | 5–9% | — | — | weak, same |
| currency symbol | positive | — | 238 | too thin to be load-bearing |
| linktree present | positive | — | 154 | too thin |
| caps ratio | **below base** | — | — | **refuted — a wrong keep** |
| digit ratio | **below base** | — | — | **refuted** |
| has URL | **below base** | — | — | **refuted** |
| non-Latin script | **below base** | — | — | refuted as a keep; see below |

**Wrong-language elimination:** non-Latin-script bios are **6.1% of present bios (3,914/64,307)**
with an address rate of **0.4% [0.3–0.7]** against Latin's **3.9% [3.7–4.0]**. Real, but it only
touches 6% of volume — it justifies a cheap drop, not a strong bet.

**Two circularities were caught inside this finding and are worth more than the finding:**

1. A naive `@[\w.]+` mention regex was matching the trailing `@gmail.com` **of the address it was
   trying to predict**. 2,185 of 2,247 "mentions" were the address matching itself, producing a
   fake **99.8% recall**. Anchored on whitespace, the honest recall is 17.8% at 3.9% precision —
   statistically no better than base rate.
2. The keyword list originally contained `gmail`/`outlook`, which substring-match whenever the
   address is written out. 887 of 2,247 rows (39.5%) matched *only* for that, inflating recall
   from a real **50.5%** to a fake **90.0%**.

## 5. Territory 5 — the answer key is still disconnected, but the machinery runs

**All nine outcome columns are 0 non-empty of 72,971 rows** — `date_sent`, `sent_channel`,
`replied`, `reply_sentiment`, `bounced`, `converted`, `outcome_notes`, `touch_number`,
`message_variant` — verified with a CSV parser, never a line count.

`clippershq/outcomes.py` is **exactly 847 lines with 21 public functions**. `hasattr` is true on
all 21 and **all 21 were driven** against a 500-row sandbox copy plus synthetic send/bounce files:
everything ran, nothing raised. A module can import cleanly and still be unrunnable; this one is
not.

**Callers, by both methods, because "AST beats grep" is not universal:** a naive grep for the bare
word `outcomes` over-matched **30+ files** (`ledger.outcomes()`, a `resolve_cache` kwarg,
`editor_assignment.join_outcomes`, plain comments). A precise import-grep and an AST scan agreed
exactly: `clippershq/control.py` (4 import sites), `clippershq/run.py`,
`clippershq/outcome_loop.py`, `tools/mark_sent.py`.

**Test verdicts, quoted verbatim from the project's own runner (`tests/run_all.py`):**

```
ALL GREEN -- 6/6 suites passed, 176 checks   (18.6s)   [-k outcome]
ALL GREEN -- 1/1 suites passed, 16 checks    (0.5s)    [-k touch_number]
```

**Two of the brief's own numbers did not survive checking.** The "63 passing tests" figure could
not be traced to any report and does not match — the four suites that actually `import outcomes`
carry **88 checks**. And "±2 points at n=469" is exact only at p=0.05; **the same n gives ±4.5
points at p=0.5**.

**Smallest write-back:** `bounced`, fed from an existing bounce/NDR export through the
already-built, already-tested `mark_bounced_from_csv`. **Nothing new needs building.** Order of
magnitude ~450–500 recorded rows, with the true interval recomputed once real data exists rather
than assumed. *(This project does not send. Reading a result back is in scope; sending is not, and
no sender, pitch, template or send order is proposed anywhere in this round.)*

## 6. A prototype I built, measured, and threw away

**Question:** can 30 cheap accounts of a hashtag predict whether the whole tag is worth walking
deep? That would be the cheapest path from a hashtag to an *address* rather than to a *page*.

Fitted on the first 30 accounts of each tag, scored on the **rest** of that tag, with addresses
stripped from the feature text so it could not see its own answer. Three controls passed first.

| band by cheap probe signal | tags | accounts | address rate | 95% Wilson |
|---|---:|---:|---:|---|
| top third | 104 | 24,125 | **3.95%** | [3.71 – 4.20] |
| middle third | 104 | 17,804 | 2.48% | [2.26 – 2.72] |
| bottom third | 106 | 8,861 | 2.97% | [2.63 – 3.34] |

Top/bottom lift 1.33x with **non-overlapping intervals** — which looks like a real separation and
is not. **Spearman rho across all 314 tags = −0.008.** Two things kill it: the bands are
**non-monotonic** (the middle third scores *below* the bottom third, which cannot happen if the
signal is real), and the rank correlation is indistinguishable from zero. The non-overlapping
intervals are an artefact of unequal band sizes — high-probe tags are simply **bigger** tags, so
this is a size confound.

**Both instruments are named rather than averaged. The prototype is refuted.**

*Caveat on my own instrument, unverified:* this assumed `rows.jsonl` is in fetch order so that
"first 30" is a cheap probe. If it is not page-ordered, the probe is not cheap and the test
measured something else.

## 7. What I got wrong (interim)

1. **My tag-level prototype's first table lied to me** and I nearly had a finding. Non-overlapping
   Wilson intervals and a 1.33x lift are exactly what a real signal looks like. Only the
   monotonicity check and a second derivation exposed it.
2. **I probed `config.json` for the Instagram unit price with a key that does not exist**
   (`instagram.hikerapi_usd_per_call`) and got `None`. Had I read `None` as "no price is
   configured" I would have published a false absence. The real key is
   **`ig_api.cost_per_call_usd` = 0.00069064**; `api.cost_per_call_usd` = 0.0006 is the
   TikTok/LamaTok price. I found it by censusing config keys matching `hiker|usd|cost|price|per_call`
   instead of guessing a second time.
3. **A latent trap I found while doing it, named and left:** four sites chain
   `ig_api.cost_per_call_usd` **or** `api.cost_per_call_usd` **or** `0.00069064` —
   `clippershq/caption_finder.py:1087`, `clippershq/caption_finder.py:1313`,
   `clippershq/control.py:3198`, `clippershq/control.py:3374`. The **second term of that chain is
   the other platform's price**, 15.1% apart. All four are **correct today** because the first key
   is set. If it is ever removed or zeroed, four Instagram sites silently bill at the TikTok rate —
   the exact failure `config.json`'s own note records costing a $3.00 cap $3.45. **Reported as
   latent, not as a live bug.**

## 8. Spend and routing so far

**$0.00 of the $1.50 budget spent.** Every number above came from files already on disk or from
two unauthenticated public spec documents. One probe was **refused on arithmetic alone** before
any call was made.

Routed to cheap models (Sonnet): the field census, the bio-text measurement, the composition
classifier, the cost/clock arithmetic, the outcomes audit — five mechanical sweeps whose raw output
never entered the expensive context. The contrarian sweep went to the expensive model because it
is judgement. Kept in the expensive context: the cap proof, the spec diff, the refuted prototype,
and this report.

## Still running at half-time

Territory 1 (unread field census), Territory 3 (clipper/client composition), Territory 4 (money
and clock), Territory 6 (the reserved contrarian). **These are ABSENT from this file, not zero.**

---

## The log so far

The full attempt-by-attempt log — including the failures, which are the point — is appended to the
final version of this file. At half-time it stands at 16 entries.
