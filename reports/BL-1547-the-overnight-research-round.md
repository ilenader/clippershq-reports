# BL-1547 — the overnight research round

**The single biggest thing nobody had looked at: the funnel judges the pages it cannot contact
and contacts the pages it has never judged.** Of 17,812 rows in the lead store carrying a named
`email_source`, **13,178 — 74.0% [73.3–74.6] — carry no judgement in any of eight judgement
columns.** Four routes are **100.0% unjudged**, and the one route that is fully judged is the one
that produced no email at all. This is not a cost problem: an address already costs **$0.00365**
to discover and an *editor* address **~$0.0159**. It is a precision problem — hand-adjudicating
140 masked bios puts the editor share of delivered addresses at **22.9% [14.6–34.0]**, so roughly
**77% of what the tool delivers is not the product**, and none of it was ever assessed. The
related fact the brief called "real and unexplained" is now explained and mechanical: **publishing
an email in a TikTok bio is anti-correlated with being an editor**, on three independent
instruments with non-overlapping intervals (1.53x, 1.83x, 1.61x). **What the next round should
do:** run the $0.00 relevance gate built here over the 13,178 never-judged rows, measure what
comes out, and treat recall — not precision — as the number to improve. It costs nothing to run
because it reads a bio already bought and stored.

---

## 1. What this project is, for a reader with no context

A funnel discovers TikTok and Instagram accounts belonging to video editors ("clippers"), reads
their public bios, and extracts published email addresses into a lead store
(`master_leads.csv`, 72,971 rows). Vendors: **LamaTok** for TikTok at **$0.000600 per call**,
**HikerAPI** for Instagram at **$0.00069064 per call**. The goal, against which everything here is
judged: **more clipper email addresses, for less money, in less time, with fewer wrong ones.**

**This round shipped nothing.** `clippershq/` was read-only throughout; every write went to
`scratch/bl1547/`. Defects are named with `file:line` and left in place. Six sweeps ran in
parallel, all six returned, and every load-bearing number was re-derived a second way.

## 2. Safety, and the cap, before anything else

**Nine stores backed up, sha256-verified, bodies found BY SHAPE rather than assumed.** A backup
that counted top-level keys would have reported "3" for a store holding 3,270 rows:

| store | body found at | rows |
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
duplicated pair, deleting one leaves the natural-key **set identical** — measured, both digests
equal — so a key-set check is *provably blind*, while an **index-qualified** fingerprint moves.
C5 showed that renaming a body key collapses the shape probe from 6,196 to 5, so it cannot
silently accept a wrapper as if it were the rows.

**The spend cap was proved to bind before a cent was spent.** The shipped `Budget` class was
lifted out of `harvest_run.py` by AST — so it cannot drift from what production runs — and driven
through `LockedBudget` under **8 threads × 50 attempts** against 20 calls of headroom:

- funded budget allows, and the meter advances by exactly one unit — `spent $0.000600, calls=1`
- a `$0.00` budget raises `BudgetExceeded` on the first call
- **the meter does not advance on a refusal** — `spent $0.000000, calls=0`
- 8 threads got **exactly 20 allowed / 380 refused**; `spent $0.012000 = 20 × $0.000600`
- the unit was passed explicitly from the **named key** `api.cost_per_call_usd`
- `Budget`'s own default unit is `1e9` — it **fails closed** rather than silently pricing a
  TikTok call at the Instagram rate

**The proof wrote nothing**: `spend.json`'s md5 was identical before and after. Every live probe
later in the round was checked the same way — the tag ledger, `spend.json` and three seen stores
were byte-identical before and after each one. **Nothing latched.**

## 3. Territory 1 — fields and endpoints we pay for and never read

### The live vendor specs, re-read rather than trusted

| vendor | cached on disk | live | new paths | removed |
|---|---|---|---:|---:|
| LamaTok | 1.3.3 / 23 paths | **1.4.5 / 29 paths** | 6 | 0 |
| HikerAPI | 1.8.0 / 154 paths | **1.8.1 / 154 paths** | **0** | 0 |

The LamaTok 23→29 jump is the one a prior round already found; **the version number has since
caught up, so the "same version, more paths" trap is not currently active.** HikerAPI adding
nothing across a version bump is a genuine negative result, recorded so the next round need not
re-fetch it. *(An OpenAPI document is public and unauthenticated. This was not a billed call.)*

### The same question at endpoint level: 9 of 29 used, 20 not

Controls passed first — a known-used path (`/v1/hashtag/medias`) was found, an invented one
(`/v9/bl1547/control/never`) was not.

**Referenced by production (9):** `/sys/balance`, `/v1/hashtag/info`, `/v1/hashtag/medias`,
`/v1/media/by/url`, `/v1/media/video/download/by/id`, `/v1/user/by/username`,
`/v2/hashtag/medias`, `/v2/search`, `/v2/user/medias/by/secUid`.

**Not referenced (20).** Three look relevant to the goal, and all three are **flagged, not
recommended** — none has been priced:

- **`/v1/user/following/by/username`** and **`/v1/user/following/by/secUid`** — paginated
  following lists. This project has already refuted *suggested-profiles* and recorded that
  *following* beats it, yet **neither following endpoint is wired to anything.**
- **`/v3/user/by/username`** — the live spec's summary reads *"Userinfo By Username (incl.
  unavailable profiles)"*. That is a different capability, not a version bump.
- **`/v2/hashtag/info`** — v1 is used, v2 is not.

### The field census

Denominator: **22,937 item-level leaf rows** across 207 payload files, with the `output/`
extraction files deliberately excluded because every field in them is read by construction.
**2,764 leaf rows both vary and are unread by both grep and AST** — but 542 of those are
near-unique IDs/URLs and 190 are list-length artefacts, so the usable remainder is much smaller
than the headline.

**Controls passed both ways:** `signature` (the free TikTok bio, definitely read) was correctly
found read by 9 files via grep and 12 via AST; `zzz_bl1547_control_key` was correctly reported
unread by both. Without the positive control every zero here would be worthless.

⚠️ **The census's own caveat, carried:** "read" is matched on the **leaf key name**, so it is an
**upper bound** on readership, and dynamic accesses are unresolvable statically.

Top varying-and-unread fields:

1. **`video.has_watermark`** (TikTok) — boolean, 10/10 sampled, zero readers, *while*
   `clippershq/tiktok_finder.py`'s `play_url_of()` already reasons about watermark risk through a
   **hardcoded URL-key priority order** instead of reading the vendor's own per-item flag. This is
   a fact the code currently guesses. **n=10 on one account is far too thin — unverified.**
2. **`subtype_name_for_REST__`** (Instagram) — media-type enum, 100% fill across 16 item-groups,
   zero readers.
3. **`gen_ai_detection_method.detection_method`** (IG, 238/238) and **`c2pa_info.aigc_src`**
   (TikTok, 10/10) — AI-generated-content flags, unread on **both** platforms.
4. `user.duetSetting` / `stitchSetting` / `downloadSetting` / `openFavorite` (TikTok, 112–114/114).
5. `video_control.allow_download` / `prevent_download_type` (TikTok, 10/10).

⚠️ **My caution on that ranking, not the census's:** #2 was described as the structural analog of
the `aweme_type` win. **`aweme_type` is REFUSED in this project** — it kills 42.86% of wanted
pages and is inverted. The analog of a refused signal is not automatically a win and must be
measured in both directions before anyone acts on it.

### A spend I refused, with the arithmetic that refused it

`/v3/user/by/username` looked worth probing until the prize was sized for free. Across 73,009
harvested account rows, **8,702 (11.92%) arrive with an empty bio** and yield zero addresses;
64,307 (88.08%) have a bio, of which 3.49% carry an address. Best case, if a paid profile call
recovered a bio for *all* 8,702 at the same rate: 8,702 × $0.0006 = **$5.22** for ~304 addresses =
**$17.17 per 1,000 addresses**, against the harvester's measured **$2.47 per 1,000**. **6.9x worse
in the best case, so no probe can rescue it. $0.00 spent.**

*(88.08% bio-present is below the 91–93% the brief quotes. Flagged as a denominator discrepancy,
not a correction.)*

## 4. Territory 2 — the bio text, measured for the first time

Denominator: 73,009 account rows; **64,307 with a bio present**; 2,247 carrying an address, all
2,247 of them from a present bio. **Base rate to beat: 3.49% [3.36–3.64].**

| signal | precision | recall | n selected | verdict |
|---|---|---|---:|---|
| business-intent keyword | **23.1% [21.9–24.3]** | **50.5% [48.4–52.6]** | 4,922 | **6.6x base** |
| bio length 51–150 chars | 5–9% | — | — | weak; likely proxies "longer bio" |
| newline ≥1 / ≥2 | 5–9% | — | — | weak, same |
| currency symbol | positive | — | 238 | too thin to be load-bearing |
| linktree present | positive | — | 154 | too thin |
| caps ratio | **below base** | — | — | **refuted — a wrong keep** |
| digit ratio | **below base** | — | — | **refuted** |
| has URL | **below base** | — | — | **refuted** |

**Wrong-language elimination:** non-Latin-script bios are **6.1% of present bios (3,914/64,307)**
at an address rate of **0.4% [0.3–0.7]** against Latin's **3.9% [3.7–4.0]**. Real, but it touches
only 6% of volume — a cheap drop, not a strong bet.

**Two circularities were caught inside this finding and are worth more than the finding itself:**

1. A naive `@[\w.]+` mention regex was matching the trailing `@gmail.com` **of the address it was
   trying to predict**. 2,185 of 2,247 "mentions" were the address matching itself, producing a
   fake **99.8% recall**. Anchored on whitespace, honest recall is 17.8% at 3.9% precision —
   statistically no better than base rate.
2. The keyword list originally contained `gmail`/`outlook`, which substring-match whenever the
   address is written out. 887 of 2,247 rows (39.5%) matched *only* for that, inflating recall
   from a real **50.5%** to a fake **90.0%**.

## 5. Territory 3 — the composition premise is a denominator artefact

The brief's premise — *"8,719 of 10,164 addresses are clients, only 120 are clippers"* — was
tested and **half of it does not survive**.

- **8,719 reproduces exactly** (67.19% [66.38–67.99] of 12,977 emailed rows).
- **120 does not.** The true clipper-with-email count is **2,933** (22.60% [21.89–23.33]) — **24x
  higher**.
- The 10,164 denominator is **ledger-era-filtered** (`date_added >= 2026-07-11`) and excludes
  **2,804 of ~2,933 historical clipper rows — 95.6% — by construction.**
- **The slogan has been repeated unverified across four reports.**

**And the label cannot answer the question anyway.** `lead_kind` is **heuristic, not observed** —
verified at source, not taken on trust. `clippershq/writer.py:315-319` is a static funnel→kind map;
`clippershq/writer.py:363-367` returns `LEAD_KIND_CLIPPER` for **any** source beginning `tt:` or
`ig:`, regardless of bio content. Its own docstring says it answers *"which funnel wrote this row…
a recorded fact, not a guess about the person."* Hardcoded per-funnel constants also sit at
`clippershq/google_play_finder.py:943`, `clippershq/repost_finder.py:1595`,
`clippershq/meme_finder.py:8838`. **All named and left unchanged.**

**Classifying the new addresses from free signals only** (bio, nickname, email local part, email
domain — no paid or model calls), on 2,215 distinct new emails: **616 clipper (27.81%
[25.98–29.71]), 315 client (14.22% [12.83–15.74]), 1,284 ambiguous (57.97%)**. Of the 931
*resolved* rows, the client share is **33.83% [30.87–36.93]** — roughly **1 in 3 identifiable bios
reads as a business even though every row arrived through an "edit" hashtag**. Four agency/MCN
domains recur inside the well, 4–8 accounts each. Controls fired both ways. `followers` and
`short_drama_creator` are null on all 2,215 rows and are unusable as free signals.

**Answer to "is this tool producing clippers or clients": both, and the honest figure is that
~1 in 3 resolvable new addresses is a business — but 58% stay ambiguous, so this bounds the
question rather than settling it.**

## 6. Territory 4 — where the money and the clock actually go

The 35,210-row ledger reconciles: `sum(dollars)` = **$65.6187** against a header of $65.6175, the
1.2¢ gap traced to a stale-header artefact on one correction row. Schema: always
`ts/campaign/calls/dollars`, usually the per-vendor `*_usd` columns, and **no explicit endpoint
field** — vendor is *inferred* from which `*_usd` column is non-zero.

**Top lifetime cost centres:** MEME_FINDER (Instagram) **$22.08 / 34,272 calls**; SPOTIFY_FINDER
(Instagram) **$9.49 / 15,814**; TIKTOK_FINDER **$7.22 / 11,988**.

**A misread field, found and named.** `output/bl1542_run/summary.json` carries `calls` and
`spent_usd` that are **session-only deltas** (`clippershq/email_harvester.py:343` constructs a
fresh `LockedBudget` each session) while `accounts` and `per_tag` **in the same file** are
**cumulative across all three resumed sessions** (`clippershq/email_harvester.py:366-386`).
Reading `spent_usd = $0.5778` as the run's cost **understates it 4.42x**; the true cumulative is
**$2.5560**, confirmed against the three run logs. **Two fields in one file on different clocks.**
Correcting for it *reproduces* the published **$2.47/1,000** (fresh) and **$3.70/1,000** (re-walk)
almost exactly, and the 54.2% already-held figure reproduces exactly at **54.24%**. So the
published cost figures survive; the summary file that appears to contradict them is the thing
that is wrong.

**The "34.3% of discovery spend bought accounts decided on zero of" figure did not reproduce** for
these three runs — **0 of 611** done tags spent pages and got zero new accounts, and the closest
analogous cost (saturation-confirmation pages) is **5.7%**. That figure came from a different
funnel (the Instagram memes-mode judge, a walk-order effect) and **does not describe the TikTok
harvester.**

**82 of 555 tag-universe entries have never been walked at all**, concentrated in ANIME3 (30),
SPORT3-NBA (12) and the newer FILMS3/PL buckets (40).

### The one number nobody had: the deep endpoint on FRESH tags

Measured this round, with two live probes. **This is the only place money was spent.**

| combination | cost per 1,000 addresses | status |
|---|---|---|
| fresh tags + v1 (shallow) | **$2.47** | measured by a prior round |
| walked tags + v2 (deep) | **$3.70** | measured by a prior round |
| **fresh tags + v2 (deep)** | **$3.55 [$2.84 – $4.44]** | **measured here** |

444 billed calls, **$0.2664**, 405 pages, **3,863 accounts**, 92.1% bios present, **75 addresses =
1.94% [1.55–2.43]**. **Zero duplicate bodies across all 405 pages**, so every page was genuinely a
different request. Four tags returned HTTP 500 on `hashtag_info` and were skipped.

**Settled, and it is a negative. $2.47 is excluded by the lower bound — the deep endpoint on fresh
tags is WORSE than the shallow endpoint on fresh tags — and $3.70 sits inside the interval, so it
is indistinguishable from a deep re-walk. The answer is: do not do it.**

⚠️ **The driver is supply, not the endpoint: 9.54 accounts per billed page.** And a confound I
must name: **the 82 remaining fresh tags are fresh *because* they are the leftovers** — obscure
anime-character tags with little content. This measures deep-on-*these*-fresh-tags, not
deep-on-fresh-tags-in-general. A round wanting the clean answer needs fresh tags of comparable
size to the walked ones.

*(A first pass at n=12 addresses gave $3.90 with an interval of [$2.25–$6.80] spanning **both**
comparators and settling nothing. Widening it cost $0.27 and was worth it.)*

## 7. Territory 5 — the answer key is still disconnected, but the machinery runs

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
than assumed.

*(This project does not send. Reading a result back is in scope; sending is not. No sender, pitch,
template or send order is proposed anywhere in this round.)*

## 8. Territory 6 — the reserved agent, told to disagree

**It disagreed with the brief's priorities, and it was right.**

### The inversion is mechanical, not mysterious

Publishing an email in a TikTok bio is **anti-correlated with being an editor**, on three
independent instruments with non-overlapping intervals:

| instrument | editor-looking | not editor-looking | ratio | n |
|---|---|---|---:|---:|
| P(publishes address \| editor-looking) | 2.58% [2.19–3.04] | 3.94% [3.67–4.24] | **1.53x** | 23,690 |
| edit-named handle, tag-stratified | 5.21% [3.83–7.04] | 9.53% [9.09–10.00] | **1.83x** | 16,680 |
| the project's own `verdict` column | 39.69% [37.94–41.46] EDITOR *with* email | 63.96% [63.55–64.36] EDITOR *without* | **1.61x** | 56,467 |

**83.6% of one run's 860 addresses came from non-editors.** I re-derived the third instrument
myself, independently, with my own controls: it reproduces exactly.

**The explanation is ordinary.** People who publish a contact address are businesses and
semi-professionals. Actual clippers mostly do not publish one. The "inversion" is the funnel
discovering that fact and nobody noticing.

### The structural fact of the night

`clippershq/email_harvester.py`'s own docstring says it *"walks accounts it does not judge"*, and
it filters on deliverability only. Measured on the live store, **and independently reproduced by
me with my own controls**:

| route (`email_source`) | n | unjudged |
|---|---:|---:|
| `instagram:business-field` | 521 | **100.0%** |
| `instagram:bio-text` | 464 | **100.0%** |
| `twitch:handle-only` | 279 | **100.0%** |
| `twitch:panel` | 275 | **100.0%** |
| `spotify:none` | 5,670 | **100.0%** |
| `spotify:resolved-instagram` | 7,425 | 66.8% |
| `ig_no_email` | 1,304 | **0.0%** |
| **all named routes** | **17,812** | **74.0% [73.3–74.6]** |

**The routes that produce contactable addresses are the least judged, and the one route that is
fully judged is the one that produced no email.**

### The prototype it built, and what it actually buys

`scratch/bl1547/t6_gate.py` — a relevance gate costing **$0.00**, because it reads the bio already
bought and stored. Against 140 hand labels: **precision 96.7% [83.3–99.4], recall 65.9%
[51.1–78.1], lift 3.08x.** Precision is flagged as an **upper bound** (the gate vocabulary and the
labelling criterion overlap); **the load-bearing number is recall — 34.1% of real editors are lost
to prose the vocabulary misses.**

**Converted into the units the brief asked for, per 1,000 delivered addresses:**

| | rows | editors | purity |
|---|---:|---:|---:|
| today | 1,000 | 229 | 22.9% |
| with the gate | **156** | **151** | **96.7%** |

**78 editors lost (−34%), 844 rows removed from his review pile (−84%), purity up 4.22x.** And
the honest part: **discovery cost per editor goes UP**, from $0.0159 to $0.0242, because you still
pay for the rows you discard. **The gate does not save money. It buys purity and his time.** Since
money is not the binding constraint, that is the right trade — but the ranked list below names the
currency each item pays in.

### Two of its own claims died to controls

1. *"Deep paging is wasted"* — **survivor bias.** Tags drop out at every depth. A balanced panel
   of the 19 tags reaching page ≥120 shows yield declining 5.17%→3.57% then **plateauing flat to
   page 169**. **A hashtag never saturates.** Breadth is still cheaper, so the harvester's shallow
   stop is accidentally near-optimal — **do not "fix" it.**
2. *"Every named `email_source` has zero judged rows"* — a `verdict`-column-only artefact,
   corrected to 74.0% after sweeping all eight columns.

**Null reported:** craft-words-in-bio showed **no** gap (7.21% vs 7.49%, overlapping). Only handle
naming separates.

## 9. A prototype I built, measured, and threw away

**Question:** can 30 cheap accounts of a hashtag predict whether the whole tag is worth walking
deep? Fitted on the first 30 accounts of each tag, scored on the **rest**, with addresses stripped
from the feature text so it could not see its own answer. Three controls passed first.

| band by cheap probe signal | tags | accounts | address rate | 95% Wilson |
|---|---:|---:|---:|---|
| top third | 104 | 24,125 | **3.95%** | [3.71–4.20] |
| middle third | 104 | 17,804 | 2.48% | [2.26–2.72] |
| bottom third | 106 | 8,861 | 2.97% | [2.63–3.34] |

1.33x lift with **non-overlapping intervals** — which looks exactly like a real signal. **Spearman
rho across all 314 tags = −0.008.** Two things kill it: the bands are **non-monotonic** (the middle
third scores *below* the bottom third, impossible if the signal were real), and the rank
correlation is indistinguishable from zero. The non-overlapping intervals are an artefact of
unequal band sizes — high-probe tags are simply **bigger** tags. **Both instruments named rather
than averaged. Refuted.**

*Unverified caveat on my own instrument:* this assumed `rows.jsonl` is in fetch order so that
"first 30" is a cheap probe. If it is not page-ordered, the test measured something else.

## 10. THE RANKED LIST — by what it costs him per 1,000 ADDRESSES

**Ranked by value against the goal, with the currency each pays in named.** Most of this list pays
in **purity and his time**, not dollars, because discovery is already ~1.6¢ per editor address —
**that is the round's main conclusion about priorities.**

| # | action | pays in | measured effect per 1,000 delivered addresses | confidence |
|---|---|---|---|---|
| 1 | Run the $0.00 relevance gate over the 13,178 never-judged contactable rows | **purity + time** | 1,000 rows → **156**, purity 22.9% → **96.7%**, 844 rows he never opens | measured on n=140 labels; **recall 65.9% is the weak point** |
| 2 | Stop quoting `lead_kind` as composition | **correctness** | the "120 clippers" figure is **24x low**; true count 2,933 | measured, reproduced |
| 3 | Fix the two-clocks summary field (`email_harvester.py:343` vs `:366-386`) | **correctness** | a 4.42x cost understatement in any round that reads it | measured, reproduced |
| 4 | Wire **one** outcome column (`bounced`) via `mark_bounced_from_csv` | **makes every other number checkable** | 0 → first real feedback at ~450–500 rows | machinery exists and runs; nothing to build |
| 5 | Drop non-Latin-script bios | **dollars, small** | 6.1% of volume at 0.4% vs 3.9% address rate | measured, but only 6% of volume |
| 6 | Price `/v1/user/following/*` (unwired, 2 endpoints) | **unknown** | **not priced** — flagged only | absent, not zero |
| 7 | **Do NOT** walk fresh tags on the deep endpoint | **avoids a loss** | $3.55 [$2.84–$4.44] vs $2.47 shallow — **excluded** | measured here, $0.31 |
| 8 | **Do NOT** "fix" the harvester's shallow stop | **avoids a loss** | yield plateaus flat to page 169; breadth is cheaper | measured on a balanced panel |

**Items 7 and 8 are negative results and they are ranked deliberately.** Both would have looked
like improvements and both would have cost money.

## 11. WHAT I GOT WRONG

1. **My tag-level prototype's first table lied to me and I nearly had a finding.** Non-overlapping
   Wilson intervals and a 1.33x lift are what a real signal looks like. Only a monotonicity check
   and a second derivation exposed it as a size confound.
2. **I probed `config.json` for the Instagram unit price with a key that does not exist**
   (`instagram.hikerapi_usd_per_call`) and got `None`. Had I read `None` as "no price is
   configured" I would have published a false absence. The real key is
   **`ig_api.cost_per_call_usd` = 0.00069064**; `api.cost_per_call_usd` = 0.0006 is the TikTok
   price. I found it by censusing config keys matching `hiker|usd|cost|price|per_call` rather than
   guessing twice.
3. **My tag-universe extractor filtered on `isinstance(v, str)` when the buckets are lists**, and
   returned a universe of **zero** — exactly the shape of a silent failure. It printed ABSENT
   rather than proceeding, which is the only reason I caught it.
4. **My hashtag-id extractor guessed the envelope keys** and reported "no id" on 2 of 3 tags,
   which reads precisely like a dead endpoint. Fixed by using the harvester's own descent
   (`clippershq/email_harvester.py:414-421`) instead of my guess. **Two of my four instrument
   failures this round were me inventing a key name.**
5. **My first deep-endpoint probe was too small to decide anything** — $3.90 with an interval
   spanning both comparators. Publishing that point estimate would have been the "CONFIRMED on
   n=3" failure this project has already paid for.
6. **I disagreed with one of my own sub-agents and said so rather than averaging.** T3 called the
   brief's "1,804 addresses" a read-back bug; it is not — 1,804 is BL-1546's post-clean survivor
   count (1,870 − 66). T3's 2,215 is the pre-dedup distinct-email count across three run files.
   Different denominators, both defensible, **both named**.
7. **A latent trap I found and left:** four sites chain `ig_api.cost_per_call_usd` **or**
   `api.cost_per_call_usd` **or** `0.00069064` — `clippershq/caption_finder.py:1087`,
   `clippershq/caption_finder.py:1313`, `clippershq/control.py:3198`,
   `clippershq/control.py:3374`. The **second term is the other platform's price**, 15.1% apart.
   **All four are correct today** because the first key is set. **Reported as latent, not as a live
   bug.**

## 12. What the round cost, and what was routed where

**$0.3132 of the $1.50 budget** — every cent of it on the two deep-endpoint probes
(**$0.0468 + $0.2664 = $0.3132**, from my own counter at the wrapper, never a ledger delta,
because `api_client.py` contains no ledger writer and a concurrent round was writing
`spend.json`). **Nothing else in this round cost anything.** One probe was **refused on arithmetic
alone** before any call was made. **I never approached the $1.00 stop-spending line.**

**Routed to cheap models (Sonnet), five parallel sweeps whose raw output never entered the
expensive context:** the field census (207 files, ~195k sub-agent tokens), the bio-text
measurement (~118k), the composition classifier (~134k), the cost/clock arithmetic (~148k), the
outcomes audit (~136k). **That is roughly 730,000 tokens of mechanical measurement kept out of the
expensive context.**

**Routed to the expensive model:** the reserved contrarian sweep (~156k) — because "where is this
brief wrong" is judgement, not typing — plus, kept in the main context: the cap proof, the spec
diff, the refuted prototype, the three independent re-derivations, and this report.

**What I would route differently:** the endpoint-usage census and the `lead_kind` source check
were single commands I ran myself and should have stayed that way — they did. But the widened
deep-endpoint probe was 17 minutes of wall clock I spent watching; it should have been launched
first, in the background, alongside the six sweeps, and collected at the end.

---

## THE FULL LOG

Every attempt, in order, **including the ones that failed** — his instruction was that all of it
be in the raw file.

### 1. Checked which round ids are free, and that the reports clone exists
- **Why:** A claim must not collide with a live round, and publish_report needs the clone
- **Returned:** BL-1545 live (another session); BL-1546 published by me earlier today; ../clippershq-reports present
- **Concluded:** BL-1547 is free in both namespaces
- **Next:** File the claim
- *(2026-09-11 22:57:43)*

### 2. Filed .claims/BL-1547.json with scratch/bl1547/* and the report path
- **Why:** A claim addresses files, not sessions; 2 other rounds in flight
- **Returned:** REFUSED first time: parent dir scratch/bl1547 did not exist. Created it, re-ran with --allow-new-dir -> claimed, no path conflicts
- **Concluded:** The claim tool refuses unresolvable paths by design -- a claim that matches nobody is worse than none
- **Next:** Set up the log and the safety backups
- *(2026-09-11 22:57:43)*

### 3. Backed up 9 stores sha256-verified and planted 5 corruption controls
- **Why:** No external backup exists; a control that cannot fail cannot pass
- **Returned:** All 9 copied with matching hashes. Bodies found BY SHAPE: spend.json runs=35210, master_leads.csv=72971 rows, clip_seen BARE LIST=2193, meme_pages->pages=6196, tiktok_pages->pages=3270, spotify->playlists=1960, repost_seen dict=1715, email_harvest_tags->tags=572, config.json=173 keys. ALL FIVE CONTROLS FIRED
- **Concluded:** C4 is the load-bearing one: on a duplicated pair, the key-set check is BLIND (identical digest) and only the index-qualified fingerprint moves. C5 showed a renamed body key collapses the probe from 6196 to 5, so it cannot silently accept a wrapper
- **Next:** Cap proof before any spend; dispatch the mechanical sweeps in parallel
- *(2026-09-11 22:59:30)*

### 4. Dispatched 6 sub-agents: T1 unread fields, T2 bio text, T3 composition, T4 money/clock, T5 outcomes, T6 reserved contrarian
- **Why:** Six independent mechanical sweeps; routing them to cheap models keeps their raw output out of the expensive context. A prior round kept 127,267 tokens out this way
- **Returned:** All six launched. T1-T5 on Sonnet (mechanical measurement), T6 on Opus (judgement, told to disagree with the brief)
- **Concluded:** Each was told to checkpoint to its own scratch/bl1547/T*.md file the moment findings exist, because sub-agents have died on rate limits in four rounds running
- **Next:** Do the cap proof myself while they run
- *(2026-09-11 23:01:44)*

### 5. Cap proof: lifted the SHIPPED Budget by AST and drove LockedBudget under 8 threads x 50 attempts
- **Why:** Prove the cap binds BEFORE spending anything; a refusal that still bills is worse than no cap
- **Returned:** ALL PASS. funded allows and meter advances one unit; 0.00 raises BudgetExceeded; METER DOES NOT ADVANCE ON A REFUSAL (spent 0.000000 calls=0); 8 threads got exactly 20 allowed / 380 refused against 20 calls of headroom; spent 0.012000 = 20 x 0.000600 exactly. spend.json md5 UNCHANGED
- **Concluded:** The cap binds under concurrency and the proof wrote nothing. TikTok unit 0.000600 confirmed from the NAMED key api.cost_per_call_usd; Budget's own default is 1e9, which fails closed rather than silently pricing a TikTok call at the Instagram rate
- **Next:** Find where the Instagram unit price actually lives -- my probed key returned None
- *(2026-09-11 23:02:52)*

### 6. Probed config for the Instagram unit price using key instagram.hikerapi_usd_per_call
- **Why:** The cap proof passes the unit explicitly and I wanted both platform units from named keys
- **Returned:** Returned None. The real key is ig_api.cost_per_call_usd = 0.00069064; api.cost_per_call_usd = 0.0006 is the TikTok/LamaTok price
- **Concluded:** MY OWN INSTRUMENT ERROR, and exactly the class this project keeps being burned by: a wrong key name returned None and if I had read None as 'no price is configured' I would have published a false absence. Found it by censusing config keys matching hiker/usd/cost/price/per_call instead of guessing again
- **Next:** Check whether anything READS the wrong one of those two keys
- *(2026-09-11 23:03:30)*

### 7. Checked the four sites that chain ig_api.cost_per_call_usd OR api.cost_per_call_usd OR 0.00069064
- **Why:** The second term of that or-chain is the OTHER PLATFORM's price (0.0006 TikTok vs 0.00069064 Instagram, 15.1% apart)
- **Returned:** caption_finder.py:1087, caption_finder.py:1313, control.py:3198, control.py:3374. All four read ig_api first, and ig_api.cost_per_call_usd IS set to 0.00069064, so all four are CORRECT TODAY
- **Concluded:** LATENT, NOT LIVE. Reporting it as latent rather than as a bug -- the instrument saw a dangerous fallback, not a current mispricing. If ig_api.cost_per_call_usd is ever removed or zeroed, four Instagram sites silently price at the TikTok rate and under-report by 15.1%, which is the exact failure config.json's own note records costing a 3.00 cap 3.45
- **Next:** Left in place per the sandbox rule. Move to the live vendor spec re-read
- *(2026-09-11 23:03:30)*

### 8. Fetched the LIVE LamaTok and HikerAPI OpenAPI specs and diffed against the cached copies
- **Why:** The brief: a vendor went 23 to 29 paths keeping the same version number, and the miss was worth 7.5x. A version number is not a change detector. NOTE: an openapi.json is public and unauthenticated -- this is NOT a billed call and the 1.50 budget is untouched
- **Returned:** LamaTok LIVE 1.4.5 / 29 paths vs cached 1.3.3 / 23 -- the 6 known new paths, version DID move this time. HikerAPI LIVE 1.8.1 / 154 paths vs cached 1.8.0 / 154 -- version moved, ZERO new or removed paths
- **Concluded:** The 23-to-29 jump is already known and the version has since caught up. HikerAPI adding nothing is a genuine negative result and worth recording so the next round does not re-fetch it
- **Next:** Census which of the 29 live paths production actually calls
- *(2026-09-11 23:04:54)*

### 9. Censused all 29 live LamaTok paths against every clippershq/*.py source, with two controls
- **Why:** A spec path that exists but is never called is the Territory 1 question at endpoint level, not field level
- **Returned:** CONTROLS PASSED: known-used /v1/hashtag/medias found=True, invented /v9/bl1547/control/never found=False. Result: 9 of 29 referenced, 20 NOT referenced. Of the 6 new-in-1.4.5 paths only /v2/user/medias/by/secUid is used
- **Concluded:** 20 unreferenced endpoints. The ones that look relevant to the goal: /v1/user/following/by/username and /by/secUid (memory records that FOLLOWING beats suggested-profiles, and suggested is refuted -- yet neither following endpoint is wired), /v3/user/by/username (a newer profile lookup nobody calls), and /v2/hashtag/info (v1 is used, v2 is not)
- **Next:** Pull the live spec's schema for the unreferenced paths to see what they return and what they would cost
- *(2026-09-11 23:04:55)*

### 10. T2: measured 18 free bio-text signals (email-intent keywords, URL/linktree, @mentions, emoji/caps/digit ratios, length buckets, script) for precision/recall against has-email on 64307 present-bio rows across bl1541/1542/1544 run files
- **Why:** the bio rides free on hashtag-route authors and nobody had measured what the TEXT predicts; needed denominators, Wilson CIs both directions, and a positive control before trusting any zero
- **Returned:** base rate 3.49% [3.36-3.64] address|bio-present, n=64307; best real signal is email_intent_kw at 23.1% precision / 50.5% recall (n=4922) AFTER removing gmail/outlook from the keyword list; caught TWO circularities: naive @mention regex read the email's own @domain.com tail (99.8% fake recall, fixed to 17.8% real), and gmail/outlook as intent keywords matched the address's own domain substring (inflated 90.0% recall down to true 50.5%); non-Latin script is 6.1% of present bios with address rate 0.4% [0.3-0.7] vs Latin 3.9% [3.7-4.0] -- refutes non-Latin as a keep signal but confirms it as a cheap drop; len_bucket 51-150 chars and newline>=1 mildly promising (5-9% precision) but weak lift; caps_ratio, digit_ratio, has_url, nonlatin_script are NEGATIVE signals (select worse than base rate)
- **Concluded:** the ONLY strong free bio-text signal for address-presence is solicitation-keyword language (email/business/booking/collab/contact/agency etc, NOT provider names), catching half of all address-carrying bios at 6.6x the base rate; bio length and newline count are weak proxies for the same thing (longer bios with structure); script/language elimination is real but small (6.1% of volume) and only justifies a cheap drop, not a keep bet
- **Next:** T2_bio_text.md written to scratch/bl1547/T2_bio_text.md; next territory should NOT reuse the naive @mention or provider-domain-keyword patterns without the whitespace-anchor / domain-word fixes documented in sections 2a/2b
- *(2026-09-11 23:05:24)*

### 11. Measured how many harvested accounts arrive with NO usable bio, to size the prize for /v3/user/by/username (incl. unavailable profiles) before probing it
- **Why:** That endpoint is unreferenced by production and claims to reach profiles v1 cannot. If the funnel loses lots of accounts to empty bios it could be worth wiring
- **Returned:** Denominator 73,009 account rows across the three harvester runs. bio_state present 64,307 (88.08%), of which 3.49% carry an address. bio_state empty 8,702 (11.92%), of which 0 carry an address. private flag True on only 3 rows
- **Concluded:** PRIZE IS BOUNDED AND THE ARITHMETIC REFUSES THE PROBE. Best case, if a paid profile call recovered a bio for ALL 8,702 at the same 3.49% rate: 8,702 x 0.0006 = 5.22 USD for ~304 addresses = 17.17 USD per 1,000 addresses, against the harvester's measured 2.47 per 1,000 on fresh tags. That is 6.9x WORSE in the best case, so no probe can rescue it
- **Next:** REFUSED THE SPEND ON ARITHMETIC ALONE -- 0.00 spent here. Note the 88.08% bio-present rate is below the 91-93% the brief quotes; flag as a discrepancy, not a correction, since the denominators may differ
- *(2026-09-11 23:05:55)*

### 12. T2 sub-agent returned: bio-text signals measured both ways on 64,307 present bios
- **Why:** The bio text has never been measured and it is free on 88% of hashtag authors
- **Returned:** Base rate 3.49% [3.36-3.64]. Best signal email_intent_kw: precision 23.1% [21.9-24.3], recall 50.5% [48.4-52.6], n=4,922 selected -- 6.6x base. Refuted: caps-ratio, digit-ratio, has_url, non-Latin script all select WORSE than base. Non-Latin bios 6.1% of volume at 0.4% [0.3-0.7] address rate vs Latin 3.9%
- **Concluded:** T2 caught TWO circularities in its own instrument before reporting: (1) a naive @mention regex was matching the trailing @gmail.com of the address it was trying to predict -- 2,185 of 2,247 'mentions' were the address matching itself, a fake 99.8% recall; (2) the keyword list contained 'gmail'/'outlook', which substring-match whenever the address is written out -- 887 of 2,247 rows matched only for that, inflating recall from a real 50.5% to a fake 90.0%
- **Next:** The signal is real but the bio is ALREADY FREE, so it saves nothing in the harvester where extraction is free too. Test whether it predicts at TAG level, which would turn a free signal into a spend-allocation decision
- *(2026-09-11 23:06:27)*

### 13. T5: csv.DictReader fill count on 9 outcome cols vs 72,971 rows; read+AST scan outcomes.py callers; sandbox-drove every public helper; ran the 4 outcomes-importing test suites via tests/run_all.py; Wilson-checked the n=469 bounce claim
- **Why:** verify the answer-key-nobody-connected claim before anyone cites a bounce/reply figure as real
- **Returned:** 9/9 columns 0 non-empty of 72,971 (matches tools/mark_sent.py's own earlier 72,950 docstring finding); outcomes.py is 847 real lines, 21 public fns, all hasattr-true and all driven clean in a sandbox with zero exceptions; production callers = control.py(4 sites)+run.py+outcome_loop.py+tools/mark_sent.py, confirmed by both precise-grep and AST (naive grep over-matched 30+ files on the bare word 'outcomes'); tests/run_all.py -k outcome and -k touch_number both printed ALL GREEN, 88 total checks across the 4 outcomes-importing suites (not the briefed 63 -- untraceable to any report); Wilson interval at p=0.05,n=469 = +-2.00pts exactly, matching BL-1510's claim, but the same n gives +-4.5pts at p=0.5
- **Concluded:** the write path is complete, tested, callable, and has written ZERO real rows in production; the gap was never code, it is that nothing has ever been sent; bounced is the correct smallest write-back because it is mechanical, bulk, and upstream of every reply/convert rate's denominator
- **Next:** an operator feeds one real bounce/NDR report through the already-built mark_bounced_from_csv (dry_run first) once an actual send exists; do not build anything new; recompute the CI width once real bounce data lands instead of trusting the 5% assumption
- *(2026-09-11 23:07:04)*

### 14. PROTOTYPE, REFUTED: can 30 cheap accounts of a hashtag predict whether the whole tag is worth walking deep? Fitted on the first 30 accounts of each tag, scored on the REST, addresses stripped from the feature text so it cannot see its own answer
- **Why:** T2's bio signal is 6.6x at ACCOUNT level, but the bio is already free and you cannot un-buy an account inside a page you already paid for. The unit that costs money is the PAGE and the decision that costs money is walk-deeper-or-stop. Tag-level prediction would be the cheapest path from a hashtag to an ADDRESS
- **Returned:** 3 controls passed (intent fires on business language, silent on an ordinary bio, and blind to a planted address). 314 tags with >=90 accounts. Bands by probe signal: top third 3.95% [3.71-4.20], middle 2.48% [2.26-2.72], bottom 2.97% [2.63-3.34]. Top/bottom lift 1.33x with NON-OVERLAPPING intervals. BUT Spearman rho across all 314 tags = -0.008
- **Concluded:** REFUTED, AND MY FIRST TABLE LIED TO ME. Two things kill it: the bands are NON-MONOTONIC (middle third scores BELOW the bottom third, which cannot happen if the signal is real), and the rank correlation is indistinguishable from zero. The non-overlapping Wilson intervals are an artefact of unequal band sizes (24,125 accounts in the top band vs 8,861 in the bottom) -- high-probe tags are simply BIGGER tags, so this is a size confound, not a signal
- **Next:** Naming both instruments rather than averaging, per the rule. CAVEAT ON MY OWN INSTRUMENT: I assumed rows.jsonl is in fetch order so that 'first 30' is a cheap probe. If it is not page-ordered, the probe is not cheap and the test is measuring something else -- unverified, and I am marking it so
- *(2026-09-11 23:07:34)*

### 15. T5 sub-agent: verified the nine outcome columns, drove outcomes.py, and found its callers two ways
- **Why:** No accuracy or bounce figure this project has published has ever been checked against a real result
- **Returned:** All nine columns 0 non-empty of 72,971 rows, verified with csv.DictReader and never a line count. outcomes.py is exactly 847 lines, 21 public functions, hasattr true on all 21, and ALL 21 DRIVEN successfully against a 500-row sandbox copy plus synthetic send/bounce files -- nothing broke, no NameError. Callers: control.py (4 import sites), run.py, outcome_loop.py, tools/mark_sent.py
- **Concluded:** The machinery is not merely present, it RUNS. A module can import cleanly and still be unrunnable; this one is not. GREP OVER-MATCHED 30+ files on the bare word 'outcomes' (ledger.outcomes(), a resolve_cache kwarg, editor_assignment.join_outcomes, comments); a precise import-grep and the AST scan agreed exactly. Both methods named, per the rule
- **Next:** T5 also checked two of the brief's own numbers: the '63 passing tests' figure could not be traced to any report and does not match (88 checks across the 4 suites that import outcomes), and BL-1510's plus-or-minus 2 points at n=469 is exact only at p=0.05 -- the same n gives plus-or-minus 4.5 points at p=0.5
- *(2026-09-11 23:07:53)*

### 16. Quoted the test runner's own verdict lines verbatim rather than counting
- **Why:** A round once published 189 passed / 14 red from a partial log when the finished run said 310/20, and another computed a verdict as 28 minus 3
- **Returned:** ALL GREEN -- 6/6 suites passed, 176 checks (18.6s) [-k outcome] and ALL GREEN -- 1/1 suites passed, 16 checks (0.5s) [-k touch_number]
- **Concluded:** Both verdict lines are the runner's own output, from tests/run_all.py which is the project's real runner, not unittest discover
- **Next:** Publish the interim report soon; T1, T3, T4, T6 still running
- *(2026-09-11 23:07:53)*

### 17. Territory 3: censused lead_kind on master_leads.csv (72,971 rows/12,977 w/ email), reproduced the 8,719/10,164 chain arithmetically, built a free-signal bio classifier for the 2,215 new TikTok addresses in bl1541/1542/1544 rows.jsonl, joined against master, ran positive controls, and grepped writer.py/*_finder.py for every lead_kind assignment site
- **Why:** The brief cited 8,719 clients / 120 clippers of 10,164 and a labelled corpus of 1,804; both numbers needed reproduction or correction before use, and lead_kind's trustworthiness (observed vs heuristic) gates whether the whole composition question is even measurable
- **Returned:** 8,719 reproduces exactly (rows-with-email, lead_kind=client). 120 does NOT reproduce as current clipper-with-email count (actual: 2,933, 24x higher) -- 10,164 = 8,719+1,291(meme_page)+120(clipper)+34(blank), a LEDGER-ERA-FILTERED (date_added>=2026-07-11) row count that excludes 2,804 of ~2,933 historical clipper rows (95.6%) by construction, so the ratio is a denominator artifact; BL-1526 already found the honest era figure is 108 not 120 (a live bug in meme_finder.py:8838/tiktok_finder.py:3792 adds +12). Whole-corpus composition is actually clipper 22.60% [21.89,23.33] Wilson95 of 12,977 addressed rows, client 67.19%. The brief's '1,804' new-address figure does not exist as a real dataset -- BL-1545 itself flagged it as a workbook read-back bug (should be 1,870) and rebuilt from source; I used the reproducible 2,215 distinct emails across bl1541/1542/1544 rows.jsonl instead. followers and short_drama_creator are null/empty on all 2,215 rows (unusable free signals). My bio+nickname+email-local-part+domain classifier: 616 clipper (27.81% [25.98,29.71]), 315 client (14.22% [12.83,15.74]), 1,284 ambiguous (57.97%); of 931 resolved rows client share is 33.83% [30.87,36.93]. Join against master on normalised email returned a sane 381/2,215 (17.2%) overlap (not a 0-row wrong-column-name join); of those, master lead_kind is 94.0% clipper, 5.5% meme_page, 0.5% client (n=2, too few to validate client precision). Against provenance-labelled clipper truth (n=358): classifier said clipper 44.1%, client 6.1% (false-client), ambiguous 49.7% (a low-false-positive/high-miss trade-off). Both positive controls fired: hand-made clipper bio -> clipper (score 7-0), hand-made agency bio -> client (score 0-10). Grepped writer.py/meme_finder.py/repost_finder.py/google_play_finder.py/email_finder.py: lead_kind is set EITHER as a hardcoded per-funnel constant at write time (meme_finder.py:8838, repost_finder.py:1595, google_play_finder.py:943) OR backfilled by writer.py:343-368's lead_kind_from_source(), a static source-to-kind lookup (writer.py:315-319) that defaults ANY tt:/ig: hashtag crawl to clipper regardless of bio content (writer.py:365-366). It is HEURISTIC PROVENANCE, never an observation of the account -- writer.py's own docstring at line 349 says so explicitly. My classifier found real agencies/MCNs (spadegroup.io x8, forevermusicgroup.com x5, payperclip.io x4, viralnationtalent.com x4) sitting inside the clipper-labelled edit-hashtag well, direct current evidence the label and the content disagree
- **Concluded:** lead_kind measures which funnel/tag found a row, not what the account is, so 8,719-vs-120 (or even 8,719-vs-2,933) cannot be read as ground truth on clipper-vs-client composition without a content-level check; my free-signal classifier is that first check and it is deliberately conservative (58% ambiguous) rather than confident. The four-report repetition of '8,719 of 10,164... only 120 are clippers' (BL-1541/1542/1544/1545) is a stale, un-re-derived slogan mixing a whole-corpus count with an era-filtered, five-step-reconstructed one -- both halves need restating together or not at all
- **Next:** Written to scratch/bl1547/T3_composition.md; a future round could tune the classifier thresholds against a genuinely independent human-labelled sample (none exists yet for clipper-vs-client identity, only for page-quality grading) and should treat the 58% ambiguous bucket as the next lever, not the 14% resolved-client rate, since ambiguous almost certainly hides more clients the keyword list missed
- *(2026-09-11 23:10:30)*

### 18. Published the INTERIM report at half-time to the same filename it will keep
- **Why:** An agent once died at the words 'Now writing the report'. Publishing half the night beats losing all of it. Same filename so the round never has two report files
- **Returned:** Secret scan PASS, pushed. FACTS guard OK (ledger lag +922 against a 2000 limit). Leak scan CLEAN across 8 staged files, corpus built from master's 12,691 addresses and 74,160 handles, all four detectors proved on planted controls first
- **Concluded:** Interim is safe on the public repo. The four still-running sweeps are named ABSENT in it, never zero
- **Next:** Continue with the remaining territories while T1/T3/T4/T6 finish
- *(2026-09-11 23:10:38)*

### 19. Territory 4: censused spend.json (35210 rows, 84 campaigns), reconciled header vs sum(dollars)/vendor sums as positive control, priced TIKTOK_FINDER and MEME_FINDER unit rates, traced the IG 0.0006-vs-0.00069064 mispricing to a date (2026-08-26 fix), diffed output/bl1541-1542-1544 summary.json against their own run logs and email_harvester.py's Harvester.__init__/_load_checkpoint, and diffed email_harvest_tags.json's 572 keys against bl1542_tags.all_tags()'s live 555-tag universe
- **Why:** BL-1547 T4 assignment: verify the published TikTok/IG per-1000 cost figures, the 54.2%-held re-walk figure, and the 34.3% discovery-waste figure, and hunt for any field read as something it is not (the leads-field precedent)
- **Returned:** MEASURED: TikTok 0.0006/call exact (710/710); IG billed at the WRONG 0.0006 rate on 52918/72271 calls (73.2%) from 2026-07-11 to 2026-08-26, understating lifetime IG spend ~4.80 dollars -- corroborates the BL-1502/ig_client.py:397-404 fix rather than finding something new. NEW FINDING: output/bl1542_run/summary.json's calls/spent_usd (bl1542_run.py:244, from h.budget which email_harvester.py:343 constructs FRESH per session) are session-only while accounts/per_tag (bl1542_run.py:170-171, from h.rows/h.per_tag which email_harvester.py:366-386 reloads CUMULATIVELY from checkpoint) are cumulative across all 3 resumed sessions -- reading spent_usd=0.5778 as the run's true cost understates it 4.42x (true 0.9564+1.0218+0.5778=2.5560, from run.log/run2.log/run3.log). Using the corrected 2.5560 reproduces the published 2.47/1000 fresh-address figure (2.479/1000); the 3.70/1000 re-walk figure reproduces as 3.703/1000 using bl1544's deliverability.pass=756 as denominator. 54.2%-held reproduced exactly (54.24%, guard block arithmetic). 34.3% discovery-waste NOT reproduced / REFUTED for these 3 runs: 0 of 611 done tags across bl1541/1542/1544 spent pages and got zero new_authors; the nearest analogous cost (saturation confirmation pages) is only 5.7% combined -- the mechanism BL-1513 measured (walk-order exhausting budget before judging) does not exist in this tag-walk harvester. leads-field misread checked and absent: 0 of 35210 spend rows and 0 of 3 summaries carry a leads key. Fresh-tag inventory: 82 of 555 current-universe tags never walked at all (base or @v2), concentrated in ANIME3 (30), SPORT3 NBA names (12), newer FILMS3/PL tags (40); 398 base-only; 75 walked both base and @v2.
- **Concluded:** The published TikTok/IG unit prices and the 2.47/3.70/54.2% figures all reproduce under a SECOND, independent derivation once the session-vs-cumulative field trap in bl1542's summary.json is corrected for -- so those figures stand. The 34.3% waste figure is real for the run it was measured on but does not generalize to this harvester; it should not be quoted against bl1541/1542/1544. The historical IG mispricing (0.0006 vs 0.00069064) is a known, already-fixed bug (BL-1502) whose dollar cost (~4.80 lifetime) had not previously been quantified from the ledger.
- **Next:** If a future round trusts any output/*_run/summary.json spent_usd/calls field from a resumable harvester, cross-check it against that run's own run*.log lines before quoting a per-1000 cost -- the field silently resets every resume while accounts/per_tag do not. The 82 never-walked tags are ready to spend on without re-paying for anything.
- *(2026-09-11 23:10:57)*

### 20. T3 sub-agent: censused lead_kind in master and tried to reproduce the brief's '8,719 of 10,164 are clients, only 120 are clippers'
- **Why:** Every cost-per-address figure this project publishes is supposedly the price of a client. That premise decides what the whole operation is worth
- **Returned:** 8,719 clients REPRODUCES EXACTLY (67.19% [66.38,67.99] of 12,977 emailed rows). 120 DOES NOT: the true clipper-with-email count is 2,933 (22.60% [21.89,23.33]), 24x higher. The 10,164 denominator is LEDGER-ERA-FILTERED (date_added >= 2026-07-11) and excludes 2,804 of ~2,933 historical clipper rows -- 95.6% -- by construction
- **Concluded:** THE BRIEF'S HEADLINE PREMISE IS A DENOMINATOR ARTEFACT. 10,164 = 8,719 + 1,291 + 120 + 34 only under an era filter that deletes almost every clipper. The slogan has been repeated unverified across FOUR reports (BL-1541, 1542, 1544, 1545)
- **Next:** Check whether lead_kind is even an observation
- *(2026-09-11 23:11:32)*

### 21. T3: traced where lead_kind is actually assigned
- **Why:** If the label is a heuristic then the 8,719/2,933 split measures the heuristic, not reality
- **Returned:** It is set either as a hardcoded per-funnel constant (google_play_finder.py:943, repost_finder.py:1595, meme_finder.py:8838) or backfilled by writer.py:343-368 lead_kind_from_source(), a static lookup at writer.py:315-319 that defaults ANY tt:/ig: hashtag crawl to clipper regardless of bio content (writer.py:365-366). writer.py:349's own docstring says so
- **Concluded:** lead_kind IS HEURISTIC, NOT OBSERVED. It records WHICH FUNNEL FOUND A ROW, never what the account is. So neither the 8,719 nor the 2,933 is evidence about composition -- both are evidence about provenance. Named with file:line and LEFT, per the sandbox rule
- **Next:** Classify the new addresses from the bio text instead, which is at least about the account
- *(2026-09-11 23:11:32)*

### 22. T3: classified the new addresses from free signals only (bio, nickname, email local part, email domain)
- **Why:** The new addresses had never been classified at all, and lead_kind cannot answer it
- **Returned:** Of 2,215 distinct new emails: 616 clipper (27.81% [25.98,29.71]), 315 client (14.22% [12.83,15.74]), 1,284 ambiguous (57.97%). Of the 931 RESOLVED rows, client share is 33.83% [30.87,36.93]. Four agency/MCN domains appear repeatedly inside the well (4 to 8 accounts each). Controls fired both ways: a hand-made clipper bio scored 7-0 clipper, a hand-made agency bio 0-10 client. followers and short_drama_creator are null on all 2,215 rows and are unusable
- **Concluded:** Roughly 1 in 3 identifiable bios reads as a business even though every row arrived through an EDIT hashtag. But 58% stay ambiguous, so this bounds rather than settles the composition question
- **Next:** T3 also disputed the brief's 1,804 figure as a workbook read-back bug; I disagree -- 1,804 is BL-1546's post-clean survivor count (1,870 minus 66) and is correct. T3's 2,215 is the pre-dedup distinct-email count across the three run files. Different denominators, both defensible, naming both
- *(2026-09-11 23:11:32)*

### 23. T4 sub-agent: censused the 35,210-row spend ledger and tried to reproduce three published figures
- **Why:** Every cost figure this project quotes rests on this ledger and nobody had re-derived them
- **Returned:** Ledger schema: always ts/campaign/calls/dollars, usually the per-vendor *_usd columns, and NO explicit endpoint field -- vendor is INFERRED from which *_usd column is non-zero. Positive control passed: sum(dollars)=65.6187 vs header 65.6175, the 1.2 cent gap traced to a stale-header artefact on one correction row. Top lifetime cost centres: MEME_FINDER 22.08 over 34,272 calls, SPOTIFY_FINDER 9.49 over 15,814, TIKTOK_FINDER 7.22 over 11,988
- **Concluded:** The ledger reconciles. 82 of 555 tag-universe entries have NEVER been walked at all, concentrated in ANIME3 (30), SPORT3-NBA (12) and the newer FILMS3/PL buckets (40)
- **Next:** Use those 82 for the deep-endpoint-on-fresh-tags probe
- *(2026-09-11 23:12:07)*

### 24. T4: tested the brief's claim that 34.3% of a run's discovery spend bought accounts the run decided on zero of
- **Why:** A round measured it once and it has been quoted since
- **Returned:** NOT REPRODUCED for bl1541/1542/1544. ZERO of 611 done tags spent pages and got zero new accounts. The closest analogous cost, saturation-confirmation pages, is 5.7% combined
- **Concluded:** The 34.3% figure came from a DIFFERENT funnel (the Instagram memes-mode judge, a walk-order effect) and does not describe the TikTok harvester. Quoting it against the harvester would be wrong
- **Next:** Report it as refuted-in-this-context rather than refuted outright
- *(2026-09-11 23:12:07)*

### 25. T4: found a live MISREAD FIELD inside one summary file
- **Why:** The brief warned that 'leads' had been read as 'delivered' and overstated a price 5.00x, and asked whether other fields are read as something they are not
- **Returned:** output/bl1542_run/summary.json carries calls and spent_usd that are SESSION-ONLY deltas (email_harvester.py:343 builds a fresh LockedBudget each session) while accounts and per_tag IN THE SAME FILE are CUMULATIVE across all three resumed sessions (email_harvester.py:366-386, _load_checkpoint). Reading spent_usd=0.5778 as the run's cost understates it 4.42x; the true cumulative is 2.5560, confirmed against run.log, run2.log and run3.log
- **Concluded:** TWO FIELDS IN ONE FILE ON DIFFERENT CLOCKS. Correcting for it REPRODUCES the published 2.47 per 1,000 fresh and 3.70 per 1,000 re-walk almost exactly, and the 54.2% already-held figure reproduces exactly at 54.24%. Named with file:line and LEFT unfixed per the sandbox rule
- **Next:** The published cost figures survive; the summary file that appears to contradict them is the thing that is wrong
- *(2026-09-11 23:12:07)*

### 26. T6 RESERVED: priced page depth, then tested whether harvested ADDRESSES belong to clippers at all (3 instruments + 140 hand-adjudicated masked bios), then swept master_leads.csv for a relevance judgement on address rows
- **Why:** The brief prioritises cost accounting; cost is already $0.00365/address MEASURED, so I went after the unmeasured axis -- PRECISION. email_harvester.py says in its own docstring it 'walks accounts it does not judge'
- **Returned:** THE INVERSION IS MECHANICAL, not unexplained: P(publishes address | editor-looking)=2.58%% [2.19,3.04] vs 3.94%% [3.67,4.24] non-editor, n=23,690, NON-OVERLAPPING -- a non-editor is 1.53x more likely to hand you an address. Tag-stratified handle control 5.21%% vs 9.53%% (1.83x, n=16,680). Project's OWN verdict column on master: 39.69%% vs 63.96%% EDITOR (1.61x, n=56,467). Hand adjudication: only 22.9%% [14.6,34.0] of harvested addresses show ANY editor evidence (but that 140-item diff OVERLAPS -- reported as a level, not a difference). LIVE DEFECT: 13,178 of 17,812 named-email_source rows in master (74.0%%) carry NO judgement in ANY of 8 columns; tiktok:bio-text/instagram:bio-text/instagram:business-field are 0.0%% judged. Free gate prototype: precision 96.7%% (UPPER BOUND, shared vocabulary), recall 65.9%%, lift 3.08x, cost $0.00
- **Concluded:** The funnel judges the pages it cannot contact and contacts the pages it has never judged. Cost is solved; precision was never measured. TWO OF MY OWN CLAIMS DIED TO CONTROLS: (1) 'deep paging is wasted' was survivor bias -- balanced panel of the 19 tags reaching page>=120 shows the yield PLATEAUS at ~3.5%% from page 40 to 169, a hashtag never saturates, and the shallow stop is accidentally near-optimal so do NOT fix it; (2) 'every named email_source has ZERO judged rows' was a verdict-column-only artifact, corrected to 74.0%% after sweeping all 8 judgement columns. Craft-words-in-bio showed NO gap (overlapping) -- only handle naming separates
- **Next:** Raise the gate's RECALL (34.1%% of real editors lost to prose the vocabulary misses); join relevance to the contactable half of master before buying more addresses
- *(2026-09-11 23:12:19)*

### 27. T6 reserved agent: EXPLAINED the score inversion the brief called real and unexplained
- **Why:** The brief said it may be the most important fact in the project and left it open
- **Returned:** Publishing an email in a TikTok bio is ANTI-CORRELATED with being an editor, on three independent instruments with non-overlapping intervals. (1) P(publishes address | editor-looking) 2.58% [2.19,3.04] vs 3.94% [3.67,4.24] for non-editors, n=23,690 -- a NON-editor is 1.53x likelier to hand you an address, and 83.6% of the run's 860 addresses came from non-editors. (2) Edit-named handle, tag-stratified, n=16,680: 5.21% [3.83,7.04] vs 9.53% [9.09,10.00], 1.83x. (3) The project's OWN verdict column on master, n=56,467: 39.69% EDITOR among email rows vs 63.96% without, 1.61x
- **Concluded:** THE INVERSION IS MECHANICAL, NOT MYSTERIOUS. People who publish a contact address are businesses and semi-professionals; actual clippers mostly do not. Three instruments, three denominators, same direction
- **Next:** This reframes the round: the constraint is PRECISION, not cost
- *(2026-09-11 23:13:24)*

### 28. T6: measured how much of the contactable store has ever been judged at all
- **Why:** email_harvester.py's own docstring says it 'walks accounts it does not judge'
- **Returned:** 13,178 of 17,812 rows with a named email_source -- 74.0% -- carry NO judgement in ANY of eight judgement columns (editor_pct, verdict, editor_signals, intent_score, quality_score, quality_note, niche, theme_match). The tiktok:bio-text, instagram:bio-text and instagram:business-field routes are 0.0% judged
- **Concluded:** THE FUNNEL JUDGES THE PAGES IT CANNOT CONTACT AND CONTACTS THE PAGES IT HAS NEVER JUDGED. That is the single structural fact of the night
- **Next:** T6 also corrected its own first version of this claim: 'every named email_source has zero judged rows' was a verdict-column-only artefact, fixed to 74.0% after sweeping all eight columns
- *(2026-09-11 23:13:24)*

### 29. T6: priced the real constraint and built a zero-cost relevance gate
- **Why:** If cost is already trivial then the brief's cost-accounting emphasis is mis-prioritised
- **Returned:** BL-1544 MEASURED 4,666 calls, 2.7996 USD, 767 net-new addresses = 0.00365 USD each. Hand-adjudicating 140 masked bios puts editor precision at 22.9% [14.6,34.0], so an EDITOR address costs 0.0159 USD (DERIVED). The gate it built, t6_gate.py, costs 0.00 because it reads the bio already bought: precision 96.7% [83.3,99.4], recall 65.9% [51.1,78.1], lift 3.08x
- **Concluded:** MONEY IS NOT THE CONSTRAINT. Precision is. T6 flags its own precision figure as an UPPER BOUND because the gate vocabulary and its labelling criterion overlap -- the load-bearing number is the 65.9% recall, i.e. a third of real editors are lost to prose the vocabulary misses
- **Next:** T6 killed two of its own claims with controls: 'deep paging is wasted' was SURVIVOR BIAS (a balanced panel of the 19 tags reaching page 120+ shows yield declining 5.17% to 3.57% then PLATEAUING FLAT to page 169 -- a hashtag never saturates, and the harvester's shallow stop is accidentally near-optimal, DO NOT FIX IT); and craft-words-in-bio showed NO gap (7.21% vs 7.49%, overlapping)
- *(2026-09-11 23:13:24)*

### 30. Censused 207 on-disk vendor payload files (_probe_samples + bl1448_paid_payloads + 6 output/ files) by os.walk, flattened item-level leaf paths per merged endpoint-family group, cross-checked every leaf key name against clippershq/*.py with grep+AST
- **Why:** Territory 1: find fields the funnel pays for and never reads, ranked by fill-rate x distinct-value count, with mandatory positive/negative controls
- **Returned:** 22,937 item-level leaf rows outside STATE files; 2,764 vary-and-are-unread; controls both passed (signature seen read in 9 grep/12 ast files, planted zzz_bl1547_control_key correctly unread); top find is TikTok video.has_watermark (10/10 items, bool, zero readers) sitting unread right next to tiktok_finder.py play_url_of()'s hardcoded watermark-avoidance heuristic (BL-1526), plus IG subtype_name_for_REST__ (100% fill, 3-way enum XDTClipsMedia/XDTFeedMedia/XDTCarouselContainerMedia) as the IG analog of the aweme_type win
- **Concluded:** Both platforms carry free structural/flag fields the funnel already reasons about heuristically (watermark risk, video vs carousel) instead of reading the vendor's own answer; has_watermark is thin (n=10, one TikHub account, absent from the 3 LamaTok-family samples checked)
- **Next:** Hand off T1_unread_fields.md to whoever owns tiktok_finder.py play_url_of() and the IG media-type gate; if pursued, refresh has_watermark to 3+ TikHub accounts per this repo's own probe-sample rule before hard-coding on it
- *(2026-09-11 23:18:05)*

### 31. SPEND 1: probed the deep endpoint /v2/hashtag/medias on FRESH never-walked tags -- the one combination nobody has priced
- **Why:** Measured already: fresh+v1 = 2.47 per 1,000 addresses; rewalk+v2 = 3.70 because 54.24% of every page is accounts already held. Deep depth WITHOUT the duplicate freight had never been run and nothing on disk can answer it
- **Returned:** TWO INSTRUMENT FAILURES FIRST. (a) My tag-universe extractor filtered on isinstance(v,str) but the buckets are LISTS -- universe came back 0, which is exactly the shape of a silent failure; it printed ABSENT rather than proceeding, which is the only reason I caught it. (b) My hashtag-id extractor checked only the top level and 'data' and got 'no id' on 2 of 3 tags, reading exactly like a dead endpoint -- fixed by using the harvester's own descent at email_harvester.py:414-421 through challengeInfo/challenge/data/response
- **Concluded:** After both fixes: 78 calls, 0.0468 USD, 70 pages, 667 accounts, 94.3% bios present, 12 addresses = 1.80% [1.03-3.12]. Cost 3.90 per 1,000 addresses. ONE tag 500'd on hashtag_info and was skipped. ZERO duplicate bodies, so all 70 pages were genuinely different requests
- **Next:** NOT SETTLED AT n=12. The interval on the cost is 2.25 to 6.80 and SPANS BOTH comparators, so this does not establish that deep-on-fresh is worse. Widening it is cheap -- doing that rather than publishing a point estimate that cannot carry weight
- *(2026-09-11 23:20:11)*

### 32. T1 sub-agent: censused item-level fields across 207 payload files and cross-checked every leaf key against production by grep AND AST
- **Why:** This hunt has paid off six times and every win was sitting in data already bought
- **Returned:** Denominator 22,937 item-level leaf rows outside the output/ extraction files -- those were EXCLUDED because they are post-extraction and every field in them is read by construction. 2,764 rows both VARY and are unread by BOTH methods; 542 of those are near-unique IDs/URLs and 190 are list-length signals, so the usable remainder is smaller than the headline
- **Concluded:** CONTROLS PASSED BOTH WAYS: positive control 'signature' correctly found read (9 files by grep, 12 by AST, including tiktok_finder.py and ig_bio.py); negative control 'zzz_bl1547_control_key' correctly reported unread by both. Without the positive control every zero here would be worthless
- **Next:** Carry the census's own caveat into the report: 'read' is matched on the LEAF KEY NAME, so it is an UPPER BOUND on readership
- *(2026-09-11 23:30:42)*

### 33. T1: ranked the varying-and-unread fields
- **Why:** A constant field cannot decide anything, so only varying-and-unread counts
- **Returned:** Top 5: (1) video.has_watermark, TikTok/TikHub bool, 10/10 sampled, zero readers -- while tiktok_finder.py's play_url_of() already reasons about watermark risk through a HARDCODED URL-key priority order instead of reading the vendor's own per-item flag. (2) subtype_name_for_REST__, Instagram media-type enum, 100% fill across 16 item-groups, zero readers. (3) gen_ai_detection_method.detection_method (IG 238/238, 3 values) and c2pa_info.aigc_src (TikTok 10/10) -- AI-generated-content flags, unread on BOTH platforms. (4) user.duetSetting/stitchSetting/downloadSetting/openFavorite (TikTok, 112-114 of 114). (5) video_control.allow_download / prevent_download_type (TikTok 10/10)
- **Concluded:** MY CAUTION ON T1's RANKING, not T1's: it calls #2 the structural analog of the aweme_type win, but aweme_type is REFUSED in this project -- it kills 42.86% of wanted pages and is inverted. The analog of a refused signal is not automatically a win and must be measured in both directions before anyone acts on it
- **Next:** has_watermark is the interesting one because it is a vendor fact the code currently GUESSES, but n=10 on one account is far too thin -- flag as unverified
- *(2026-09-11 23:30:42)*

### 34. RE-DERIVED T6's load-bearing claim myself, with my own controls, rather than trusting it
- **Why:** It is the structural fact of the night and the top of the ranked list depends on it
- **Returned:** REPRODUCES EXACTLY: 13,178 of 17,812 rows with a named email_source carry no judgement in any of the eight columns = 74.0% [73.3-74.6]. My controls fired (verdict column shows 56,467 filled; an invented column shows 0). The route split is sharper than the headline: instagram:business-field 100.0% unjudged, instagram:bio-text 100.0%, twitch:handle-only 100.0%, twitch:panel 100.0%, spotify:none 100.0%, spotify:resolved-instagram 66.8% -- while ig_no_email is 0.0% unjudged, i.e. fully judged
- **Concluded:** THE ROUTES THAT PRODUCE CONTACTABLE ADDRESSES ARE THE LEAST JUDGED, and the one route that is fully judged is the one that produced NO email. Two independent instruments, same number
- **Next:** Wait on the widened deep-endpoint probe, then write the final report
- *(2026-09-11 23:31:20)*

### 35. Re-derived T6's THIRD inversion instrument myself off master's own verdict column
- **Why:** The inversion is the headline explanation of the night and it should not rest on one agent's arithmetic
- **Returned:** REPRODUCES EXACTLY. n=56,467 rows with a non-empty verdict. Rows WITH an email are 39.69% EDITOR [37.94-41.46]; rows with NO email are 63.96% EDITOR [63.55-64.36]. Ratio 1.61x. The intervals do not come close to overlapping
- **Concluded:** Confirmed on the project's OWN label, independently of T6's two bio-derived instruments. Three instruments, three denominators, same direction: publishing a contact address is anti-correlated with looking like an editor
- **Next:** Check the widened probe
- *(2026-09-11 23:31:52)*

### 36. Converted T6's gate into the units the brief asked for -- dollars and hours per 1,000 ADDRESSES, not per 1,000 pages
- **Why:** A ranked list must be ranked by what it costs him, and 'lift 3.08x' is not a cost
- **Returned:** Per 1,000 delivered addresses: today 1,000 rows containing 229 editors at 22.9% purity. Gated: 156 rows containing 151 editors at 96.7% purity. 78 editors lost (-34%), 844 rows removed from his review pile (-84%), purity up 4.22x. Discovery cost per EDITOR goes UP, from 0.0159 to 0.0242, because you still pay for the rows you discard
- **Concluded:** THE GATE DOES NOT SAVE MONEY AND I WILL NOT RANK IT AS IF IT DOES. It costs 0.00 to run and it buys PURITY and his TIME, not dollars. Since T6 measured that money is not the binding constraint (an editor address already costs 1.6 cents) that is the right trade -- but the ranked list must say which currency it pays in
- **Next:** Also sized the unjudged pile in the same units: the 13,178 never-judged contactable rows contain roughly 3,018 editors and 10,160 rows that are not the product, none of it ever assessed
- *(2026-09-11 23:32:31)*

### 37. Verified T3's lead_kind claim by reading writer.py myself rather than trusting the agent
- **Why:** The whole clipper-versus-client premise rests on whether that column is an observation
- **Returned:** CONFIRMED AT SOURCE. writer.py:315-319 is a static funnel-to-kind map (spotify_finder/twitch_finder/google_play/youtube_finder -> CLIENT, repost_finder -> CLIPPER). writer.py:363-367 returns LEAD_KIND_CLIPPER for ANY source starting tt: or ig: or containing no colon, regardless of bio content. The function's own docstring says it answers 'which funnel wrote this row... a recorded fact, not a guess about the person'
- **Concluded:** lead_kind IS PROVENANCE, NOT IDENTITY, and the code says so in plain English. So the brief's '8,719 clients vs 120 clippers' is not a fact about who is in the store -- it is a fact about which funnel wrote each row, under a denominator that also filters out 95.6% of historical clipper rows by date
- **Next:** Named with file:line and LEFT UNCHANGED per the sandbox rule. Nothing in clippershq was edited this round
- *(2026-09-11 23:33:00)*

### 38. SPEND 2: widened the deep-on-fresh probe from 8 tags to 34 to get an interval that can decide
- **Why:** The n=12 version gave 3.90 with an interval spanning BOTH comparators, which settles nothing. Widening cost 0.27
- **Returned:** 444 calls, 0.2664 USD, 405 pages, 3,863 accounts, 92.1% bios present, 75 addresses = 1.94% [1.55-2.43]. COST 3.55 per 1,000 addresses [2.84-4.44]. ZERO duplicate bodies across all 405 pages. Four tags 500'd on hashtag_info and were skipped
- **Concluded:** SETTLED, AND IT IS A NEGATIVE. 2.47 (fresh+v1) is EXCLUDED by the lower bound, so the deep endpoint on fresh tags is WORSE than the shallow endpoint on fresh tags. 3.70 (rewalk+v2) sits inside the interval, so deep-on-fresh is INDISTINGUISHABLE from a deep re-walk. The brief called this the most valuable number available; it is worth having and the answer is DO NOT DO IT
- **Next:** THE DRIVER IS SUPPLY, NOT THE ENDPOINT: 9.54 accounts per billed page. CONFOUND I MUST NAME -- the 82 remaining fresh tags are fresh BECAUSE they are the leftovers, obscure anime-character tags with little content. This measures deep-on-THESE-fresh-tags, not deep-on-fresh-tags-in-general, and a next round wanting the clean answer needs fresh tags of comparable size to the walked ones
- *(2026-09-11 23:41:12)*

### 39. Caught my own leak scan using the WRONG CORPUS and re-ran it against the right one
- **Why:** My scan was built from master's 12,691 addresses. But only 381 of the 2,215 newly harvested addresses are in master, so a real new address in a committed file would have read as CLEAN
- **Returned:** T3_composition.md carries 2 email-shaped literals, REAL=0 against master. Rebuilt the corpus from the three run files (2,215 harvested addresses, the ones master does NOT contain), proved membership on a known member first, and re-checked: BOTH literals are absent from that corpus too
- **Concluded:** They are synthetic fixtures and safe. But the first scan was a FALSE ABSENCE WAITING TO HAPPEN and the brief warned about exactly this -- a scan built from the wrong corpus was once blind to a lead-store address and only the pre-commit guard stopped it
- **Next:** Commit and publish
- *(2026-09-11 23:44:46)*

### 40. Committed the round and refreshed the log embedded in the report
- **Why:** The report was assembled at 38 entries and the leak-corpus check became #39; the published log must be the complete one
- **Returned:** Report re-assembled with every entry, C0 assertion re-run BEFORE the write, leak scan re-run after the last edit
- **Concluded:** Publishing with --update to the SAME filename the interim used, so this round has exactly one report file
- **Next:** Verify CDN against the remote blob as the last action
- *(2026-09-11 23:45:06)*
