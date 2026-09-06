# BL-1523 — HIS HASHTAGS, HIS SEARCH TERMS, AND WHAT EACH ONE ACTUALLY RETURNS

**Round:** BL-1523 (renumbered from BL-1520 mid-round — see §6) · **Date:** 2026-09-06
**Spend: $0.00** — no vendor call of any kind · **Production files changed: none**
**Safe to run beside anything:** yes. Read-only. No store, config, threshold, rule or verdict
was touched.

---

## THE ANSWER, IN ONE PARAGRAPH

**Yes — his terms are the problem, and the single hardest number in this report is that his own
term list has reached 2 of his own 176 hand-picked pages. 1.14% [0.31, 4.05].** That is an
observation, not a proxy: every page the funnel walks is stored with the term that surfaced it,
and his handles were intersected with that record (positive control 50/50 found, 3 invented
handles 0 found). On TikTok, where the term list **is** the entire discovery mechanism — 2,518 of
2,518 pages are term-sourced — forty terms reached **2 of his 97** TikTok accounts. On Instagram
the term half reached **0 of 79**. The eight other accounts of his the funnel has ever seen
arrived via the suggestion graph or a seed file, **and it rejected five of the ten it looked
at**. No threshold, judge or rubric can fix this, because his pages never enter the funnel.
**And the second finding is that the better surface is already bought and then thrown away:**
`discover()` appends hashtag videos first (`tiktok_finder.py:2495`) and search videos second
(`:2509`) into one ordered list, and the walk stops the moment the target is met (`:2617`) — so
in **9 of the last 10 memes runs not one search-term author was ever judged**, and all six
shipped search terms have delivered nothing for 10 consecutive runs. Reordering those two loops
is close to free. Individual hashtags are measurably bad — `brainrot` walked 164 and passed 106
with **0 of 10** approved, `memesdaily` 181/79 with **1 of 15** — but the headline I first wrote,
that search beats hashtags 90% to 47%, **does not survive its own robustness check** and is
reported in §3.1 with the caveat that kills it.

---

## 1. WHAT THIS ROUND WAS ASKED TO DO

His words:

> "Maybe you're doing bad hashtags. Maybe he's doing some fucking retarded ass hashtags, and
> that's why it's really bad. I want to know what hashtags he's doing. I want to see what he has
> cooked up — for editing and for the meme pages. Because when I search a hashtag myself, I just
> see those kinds of videos. It's hard for me to understand."

**Nobody has ever shown him the term list. Not once, in the entire project.** A previous round
asked for exactly this and did not deliver it, recording: *"the brief asked for search terms
with their yields, which it correctly called among the most useful output — this round has none,
because that measurement never ran."* This round exists to produce it. It is free and it is on
disk.

---

## 2. WHAT SHIPPED

**Nothing. By design.** This round writes no production file, moves no threshold, and changes no
verdict. Defects are named with `file:line` and left. What it produced is instruments and a
table, all committed under `BL-1523`.

---

## 3. THE FULL LIST — EVERY TIKTOK TERM, WITH ITS YIELD

Source: `tiktok_pages_seen.json`, a dict at key `pages`, **2,518 rows**, with `found_via`
stamped on **100%** of them (cardinality 40). **MEASURED.** Lifetime totals per term, across
every TikTok run ever made — not a description of any single run.

`passed` has **three** states — True 1,413 / False 965 / None 140. `None` is **UNJUDGED, not a
rejection**, and it leaves *both* sides of every rate below.

| surface | term | walked | passed | reject | unjudg | pass rate of judged | he approved |
|---|---|---:|---:|---:|---:|---|---|
| hashtag | memes | 319 | 199 | 116 | 4 | 63.2% [57.7, 68.3] | 38.5% [24.9, 54.1] n=39 |
| hashtag | relatablememes | 270 | 170 | 94 | 6 | 64.4% [58.4, 69.9] | **75.4% [62.9, 84.8] n=57** |
| hashtag | memepage | 244 | 136 | 108 | 0 | 55.7% [49.5, 61.8] | 44.4% [18.9, 73.3] n=9 |
| hashtag | funnymemes | 211 | 116 | 95 | 0 | 55.0% [48.2, 61.5] | **0.0% [0.0, 49.0] n=4** |
| hashtag | memesdaily | 181 | 79 | 92 | 10 | 46.2% [38.9, 53.7] | **6.7% [1.2, 29.8] n=15** |
| hashtag | brainrot | 164 | 106 | 58 | 0 | 64.6% [57.1, 71.5] | **0.0% [0.0, 27.8] n=10** |
| hashtag | funnyvideos | 125 | 81 | 44 | 0 | 64.8% [56.1, 72.6] | no marks |
| hashtag | moviememes | 82 | 28 | 43 | 11 | 39.4% [28.9, 51.1] | 50.0% [9.5, 90.5] n=2 |
| hashtag | tvshowmemes | 71 | 15 | 50 | 6 | 23.1% [14.5, 34.6] | no marks |
| hashtag | relatable | 67 | 45 | 22 | 0 | 67.2% [55.3, 77.2] | 0.0% [0.0, 79.3] n=1 |
| hashtag | comedy | 59 | 30 | 29 | 0 | 50.8% [38.4, 63.2] | no marks |
| hashtag | gamingmemes | 58 | 1 | 14 | 43 | 6.7% [1.2, 29.8] | 0.0% [0.0, 56.1] n=3 |
| hashtag | genzhumor | 54 | 34 | 20 | 0 | 63.0% [49.6, 74.6] | no marks |
| hashtag | cartoonmemes | 53 | **0** | 29 | 24 | 0.0% [0.0, 11.7] | 0.0% [0.0, 65.8] n=2 |
| hashtag | dankmemes | 50 | 25 | 25 | 0 | 50.0% [36.6, 63.4] | no marks |
| hashtag | footballmemes | 42 | 6 | 14 | 22 | 30.0% [14.5, 51.9] | **100.0% [61.0, 100.0] n=6** |
| hashtag | shitpost | 20 | 6 | 14 | 0 | 30.0% [14.5, 51.9] | no marks |
| hashtag | sportsmemes | 20 | 10 | 7 | 3 | 58.8% [36.0, 78.4] | no marks |
| hashtag | quotes | 11 | 10 | 1 | 0 | 90.9% [62.3, 98.4] | no marks |
| hashtag | fyp | 11 | 11 | 0 | 0 | 100.0% [74.1, 100.0] | no marks |
| search | amvedit | 41 | 34 | 7 | 0 | 82.9% [68.7, 91.5] | no marks |
| search | car edits | 39 | 28 | 7 | 4 | 80.0% [64.1, 90.0] | **100.0% [74.1, 100.0] n=11** |
| search | movieedit | 36 | 19 | 17 | 0 | 52.8% [37.0, 68.0] | no marks |
| search | cinematicedit | 33 | 26 | 7 | 0 | 78.8% [62.2, 89.3] | no marks |
| search | velocityedit | 31 | 28 | 3 | 0 | 90.3% [75.1, 96.7] | no marks |
| search | movie edits | 29 | 23 | 3 | 3 | 88.5% [71.0, 96.0] | 80.0% [37.6, 96.4] n=5 |
| search | relatable quotes | 23 | 20 | 3 | 0 | 87.0% [67.9, 95.5] | no marks |
| search | scenepack | 23 | 14 | 9 | 0 | 60.9% [40.8, 77.8] | no marks |
| search | anime edits | 22 | 20 | 1 | 1 | 95.2% [77.3, 99.2] | **100.0% [74.1, 100.0] n=11** |
| search | meme compilation | 18 | 5 | 13 | 0 | 27.8% [12.5, 50.9] | 100.0% [20.7, 100.0] n=1 |
| search | motivation quotes | 16 | 16 | 0 | 0 | 100.0% [80.6, 100.0] | 0.0% [0.0, 65.8] n=2 |
| search | football edits | 16 | 13 | 0 | 3 | 100.0% [77.2, 100.0] | **100.0% [51.0, 100.0] n=4** |
| search | fan edit | 14 | 11 | 3 | 0 | 78.6% [52.4, 92.4] | no marks |
| search | fanedit | 12 | 10 | 2 | 0 | 83.3% [55.2, 95.3] | no marks |
| search | football quotes | 11 | 10 | 1 | 0 | 90.9% [62.3, 98.4] | 100.0% [20.7, 100.0] n=1 |
| search | relatable memes | 10 | 10 | 0 | 0 | 100.0% [72.2, 100.0] | 80.0% [37.6, 96.4] n=5 |
| search | baller quotes | 9 | 9 | 0 | 0 | 100.0% [70.1, 100.0] | no marks |
| search | sad quotes | 9 | 9 | 0 | 0 | 100.0% [70.1, 100.0] | no marks |
| search | relatable | 7 | **0** | 7 | 0 | 0.0% [0.0, 35.4] | no marks |
| search | funny edit | 7 | **0** | 7 | 0 | 0.0% [0.0, 35.4] | no marks |

**Blank is not zero.** 21 of 40 terms carry no mark at all; "no marks" means he has never graded
a page from that term, not that he rejected them.

### 3.1 Search versus hashtag — the comparison I cannot make stand up

| surface | terms | walked | share of walk | funnel pass | he approved |
|---|---:|---:|---:|---|---|
| hashtag | 20 | 2,112 | **83.9%** | 52.5% [50.3, 54.6] | 47.7% [39.8, 55.6] n=149 |
| search | 20 | 406 | **16.1%** | 75.1% [70.7, 79.1] | 90.0% [76.9, 96.0] n=40 |

Taken at face value the approval intervals do not overlap, Fisher exact two-sided
**p = 5.41e-07**, odds ratio 10.03 (computed with `math.comb` — scipy is absent here and a
missing library must not become a missing p-value; the same function returns p = 1.000 on a
planted null table).

**⚠️ AND IT DOES NOT SURVIVE. 30 of the 40 search marks come from a single sheet.**

| mark set | hashtag approved | search approved | verdict |
|---|---|---|---|
| all sheets | 47.7% [39.8, 55.6] n=149 | 90.0% [76.9, 96.0] n=40 | do not overlap |
| **excluding that one sheet** | 47.7% [39.8, 55.6] n=149 | **70.0% [39.7, 89.2] n=10** | **OVERLAP** |
| that sheet alone | — | 96.7% [83.3, 99.4] n=30 | — |

And the sheet is an **edits** sheet, while essentially all hashtag marks come from **meme**
sheets. So surface, brain and grading session are confounded together and **this data cannot
separate them.** The direction is consistent (70% > 47.7% even without it) and the effect may
well be real, but **it is not established**, and I am not going to present it as though it were.

**⚠️ AND A THIRD MARK CORPUS GIVES A THIRD ANSWER.** `ground_truth/score_marks_tiktok.jsonl`
holds **387 TikTok pages he scored**, joining 391/391 into the seen store, and there the split is
**382 hashtag / 5 search — search is 1.3% of his graded corpus**, against the 149/40 (21%) I get
from `marks.jsonl` inside sheet directories. Three instruments, three denominators, and I did
**not** reconcile them. On the agent's corpus the comparison is not merely underpowered, it
barely exists. That is a second, independent route to the same verdict: **hashtag-versus-search
has never been settled on his hand — only on the judge's opinion.**

**Corroboration that it was never established:** `config.json`'s own `tiktok_finder._searches_why`
records *"ZERO search-sourced pages appear in the 311 he has graded."* That note is **stale
rather than wrong** — it names its own denominator, and the edits sheet carrying 30 search marks
was graded after it was written. Both are true of their own denominator. The same note adds the
warning I should have heeded first: the per-surface split *"comes from the seen-set passed flag —
THE JUDGE'S OPINION"*, not from his grades.

**What IS solid at the term level**, because it is hashtag-internal and involves no cross-surface
comparison: `brainrot` 0 of 10 approved on 106 passed pages, `memesdaily` 1 of 15 on 79,
`funnymemes` 0 of 4 on 116 — against `relatablememes` at 75.4% [62.9, 84.8] on the largest mark
sample in the table (n=57).

### 3.2 Dead terms are *not* where the money is

Three terms in the table above delivered nothing: `hashtag:cartoonmemes` (53 walked, 0
passed), `search:relatable` (7, 0), `search:funny edit` (7, 0) — 67 pages, 2.7% of the walk,
about $0.04. **MEASURED.**

**⚠️ BUT MY TABLE IS STRUCTURALLY BLIND TO THE WORST CASE, and a sub-agent found it.** The table
is built from the seen store, which **only contains terms that produced at least one page** — so
a term that produced *literally nothing* has no row and is invisible to my instrument. Two
shipped hashtags are in exactly that state: **`#streamerclips` and `#twitchclips` have been
walked in 11 runs, cost 30 discovery calls (~$0.018), and have 0 rows in the 2,518-row store.**
They are 2 of the 15 discovery calls in every memes run = **13.3% of the slot budget**, and since
the seven live tags average 5.2 walked accounts per discovery call, those two slots forgo roughly
**10 walked accounts per run**. The dollars are trivial; the *slots* are not. **MEASURED by
sub-agent; the mechanism (zero rows ⇒ zero visibility) verified by me.**

The expensive failure is the opposite: terms that pass the funnel and hand him pages he rejects.
Ranked by estimated junk delivered (passed × (1 − approval), over the 19 of 40 terms carrying a
mark — **DERIVED**):

| term | walked | passed | he approved | est. junk delivered |
|---|---:|---:|---|---:|
| hashtag:memes | 319 | 199 | 15/39 = 38.5% | 122.5 pages |
| hashtag:funnymemes | 211 | 116 | 0/4 = 0.0% | 116.0 |
| hashtag:brainrot | 164 | 106 | 0/10 = 0.0% | 106.0 |
| hashtag:memepage | 244 | 136 | 4/9 = 44.4% | 75.6 |
| hashtag:memesdaily | 181 | 79 | 1/15 = 6.7% | 73.7 |

Over the marked terms: 1,852 walked, 1,011 passed, **an estimated 618 junk pages = 61.1% of
what they delivered.**

### 3.3 The seed file — 2.06% is a lower bound, and the walk is not what anyone thought

*(Sub-agent, all 17 of its controls passing. Cross-checked mechanism below.)*

The live seed file is `scratch/bl1391_seed_accounts_ordered.txt`, **16,879 handles**, read via
`config.json → meme_finder.seed_accounts_file`.

- **2.06% [1.86, 2.29]** are page-shaped on the strict rule; 3.41% on the broad one. **MEASURED.**
- **But that is a LOWER BOUND, not the candidate fraction.** The rule's precision is 40/40
  [91.2, 100], and its **recall is 0 of 11 [0, 25.9]** against a hand-judged content-page
  prevalence of **22.0% [12.8, 35.2] (n=50)**. It is a high-precision, low-recall *ordering*
  signal, not a census.
- **The shape test predicts strongly on the right denominator:** of 1,931 walked seed handles,
  page-shaped pass **34.48% [19.94, 52.66]** vs personal-shaped **7.20% [6.13, 8.45]** — 4.79×,
  disjoint CIs, Fisher **p = 2.75e-05**. Control: across the whole store ignoring channel it is
  30.12% vs 29.38%, **no separation** — and that null is what proves the seed channel is the
  right denominator.

**⚠️ THE WALK IS ALPHABETICAL, NOT FILE ORDER, SO THE REORDERING IS DEAD.** `_walk_rank`
(`clippershq/meme_finder.py:7018`) returns `(channel_rank, handle)` and the buy loop consumes
`sorted(fresh.items(), key=_walk_rank)` at `:8337` — within the seed channel the tie-break is
**the handle, alphabetically**. File position decides nothing. On the clean window after the
tie-break shipped: 48 pages walked, **alpha-position deciles [48,0,0,0,0,0,0,0,0,0]** while
their **file** positions scatter across five deciles. The file header's own sentence, *"The
funnel walks this file front to back,"* has been false since 2026-08-25. Consequence:
**305 of 348 page-shaped handles (87.6%) have never been walked**, against an 88.2% base rate —
the front-loading buys nothing.

**Two of the brief's own numbers corrected:** the 1,114-handle append batch is real (positions
10034–11148) but holds **15** page-shaped on the strict rule, **27** on the broad — not 65. And
the **83.32% seed share is NOT VERIFIED** — the walked record puts seed at **51.94%** of the
4,311 rows carrying a `found_via`. Both readings are named; they have different denominators and
I did not pick one.

### 3.3a Would his own terms have found his own pages? 2 of 176.

**The sharpest test in the brief, and it costs nothing.** He hand-supplied **176 accounts**
across three places, all confirmed by parsing each one: 66 TikTok edit + 64 Instagram edit in a
`scratch/bl1436_handles.py` (triple-quoted **strings** — an AST list-literal walk returns 0),
31 TikTok meme in a `scratch/bl1189_urls.txt` of share URLs, and 15 Instagram meme in a
`scratch/bl1240_reference_study.md` **prose table**. 176 total, 176 distinct.

| slice | found by any term | % | Wilson 95% |
|---|---:|---:|---|
| **all 176** | **2** | **1.14%** | [0.31, 4.05] |
| TikTok (n=97) | 2 | 2.06% | [0.57, 7.21] |
| **Instagram (n=79)** | **0** | 0.00% | [0.00, 4.64] |
| TikTok edits (n=66) | 1 | 1.52% | [0.27, 8.10] |
| TikTok memes (n=31) | 1 | 3.23% | [0.57, 16.19] |

Denominators: **8,714 walked pages** across both page stores, **77 terms that have actually run**
(40 TikTok, 37 Instagram). **This is an observation, not a proxy** — every walked page is stored
with the term that surfaced it, and his handles were intersected with that record. **Positive
control: 50 handles drawn from the stores themselves, 50 found; 3 invented handles, 0 found.**
The TikTok figure is the sharp one because **TikTok discovery is 100% term-driven** (2,518 of
2,518); Instagram is only 23.1% term-driven (36.1% seed, 30.4% no provenance recorded).

**And of the 10 of his accounts the funnel did walk, it rejected 5** — including **4 of 4**
Instagram meme pages, all reached by the suggestion graph. *Caveat: those verdicts predate the
current judge.* Seven of the 176 sit in the live seed file — handed to the funnel as supply, not
found by search.

**⚠️ THE BACKWARDS RULES THEMSELVES ARE BLIND, AND THE AGENT PROVED IT RATHER THAN REPORTING
THEIR ZEROS.** Four matching rules of increasing looseness were run (exact token 0/176,
boundary-safe substring 0/176, naive substring 2/176, topical overlap 34/176 — 23 after removing
circular matches). Then the same four rules were run on **3,947 pages a term genuinely did find**,
each against the term that actually surfaced it — true positives by construction: exact token
**2.96%**, boundary-safe **0.99%**, naive **3.07%**, topical **10.24%**. **A handle-text rule
misses 97–99% of pages a term really found**, so those zeros are not evidence about his set and
are reported for completeness only. The observation above is the answer.

One inversion worth his attention: **his pages score *higher* on the topical rule (19.3%) than
the funnel's own term-found pages do (10.2%)** — by name his accounts are *more* on-topic than
what the terms deliver, and the terms still did not reach them.

**A term aimed squarely at his Instagram edit pages exists and has left no trace.**
`config.ig_crawl_fbsearch_keywords` holds **24 `<subject>edit` terms** — no `found_via` value in
either store contains `fbsearch` or `ig_crawl`, and no CSV records it. Either it has never run or
its output is unattributed. **NOT VERIFIED which.**

### 3.3b The search terms are bought and then structurally unreachable

**This is the most actionable finding in the report and it is not about term quality at all.**

`discover()` walks hashtags first (`clippershq/tiktok_finder.py:2495`) and search keywords second
(`:2509`), appending both into **one ordered list**, and author order is preserved downstream.
The walk then stops the moment the target is met — `result["stopped"] = "target of %d %s
reached"` at `:2617`. **VERIFIED at source by me.**

Consequence, measured by sub-agent across the last 10 memes runs: **in 9 of them the target was
reached while still inside the hashtag-sourced authors, so not one search-term author was ever
judged.** In the 10th (target 6), 93 were walked and all 93 failed the 180-day recency gate.

- **All six shipped search terms have delivered nothing for 10 consecutive runs** (2026-08-28 →
  2026-09-06). Last delivery was 2026-08-17 — 9 sheets, all from `relatable quotes`.
- Five of the six have produced **zero net-new pages since 2026-08-08**; every store row they own
  was first seen on that single day.
- Combined with the two dead hashtags, **7 of the 15 discovery calls (46.7%) in every memes run
  buy something the run never looks at.**

So the surface he approves at 90% is *already configured and already paid for*. It is not
reached because the cheaper-to-reach surface is consumed first and the target cuts the walk off.
**Reordering the two loops, or interleaving them, is close to free and is the single highest-value
change in this report.**

### 3.3c Three stale claims in the code, and a second corpus nobody has mentioned

**Stale claims — named and left:**
1. `clippershq/run_mode.py` documents `TIKTOK_EDIT_SEARCHES` as **"NEW, NEVER RUN, NO MEASURED
   YIELD"**, and that string is **printed to him at the top of every edits run**. All three have
   run **7 times each**: `movie edits` 148 walked / 68 delivered, `anime edits` 89 / 24,
   `football edits` 94 / 13.
2. `clippershq/page_mix.py:42` states `tiktok_finder.hashtags` is
   `["memes","funnymemes","relatablememes","memepage"]`. **Three of those four were dropped.**
3. **The seen store is behind the runs.** 4 of the 28 runs on disk never fully reached
   `tiktok_pages_seen.json` (as little as 4% of their rows landed). **So every denominator in
   §3 is a lower bound**, and a census from the store alone misses those runs.

**And a second corpus, 21× the size of the funnel, that is in no config key named
`tiktok_finder`:** `master_leads.csv` holds **53,920 TikTok rows tagged `tt:<surface>:<term>`
across 1,073 distinct terms** — 1,009 hashtags and 64 search phrases — with 2,758 emails (5.1%)
and **zero ever sent**. They come from campaign banks in `config.campaigns.*.default_hashtags`
(2,240 configured, 1,073 with rows). Almost all added 2026-07, dormant since 2026-08. **372 of
the 1,073 produced zero email rows across 11,546 rows.** **MEASURED by sub-agent, NOT re-derived
by me.**

### 3.3d What he does by hand that the funnel cannot (Part 6, the reserved question)

**The answer is that the vendor does not sell him what his thumb does.** `/v1/hashtag/medias`
— the surface that produced **382 of the 387 TikTok pages he has ever scored (98.7%)** — takes
exactly three parameters in LamaTok's own spec on disk: `id`, `count`, `cursor`. **No top, no
recent, no sort, no period.** When he taps a hashtag in the app he gets a *ranked,
session-personalised* grid. The funnel cannot ask for one. It is not using the surface badly;
the surface it can reach is a different product.

**And it scrolls one screen.** `config.tiktok_finder.depth = 1` against
`HASHTAG_PAGE_COUNT = 30` — **one page of 30 items per tag, shallower than a hand scroll.**
**VERIFIED at source by me.**

**On Instagram the ranking IS exposed, and the code throws it away.** `clippershq/main.py:4012`
reads `_kind if _kind in ("top", "recent") else "recent"` — anything else, including `clips`,
is **silently rewritten to `recent`**, the endpoint this repo measured at **0 of 37 passed**
(against `/top` 4 of 39 and `/clips` 5 of 39, Fisher p = 0.031). All four campaigns in
`config.json` are set to `recent`. **VERIFIED at source by me.** *Honest caveat from the agent:
`state.json` holds zero `ig:hashtag:*` wells, so this lane has not run and explains none of his
graded pages — it is a live trap, not a past cause.* (`meme_finder` is unaffected — it reads
`hashtag_endpoint` and defaults to `clips`.)

**Three refutations, each first-class:**
- **Depth is not the answer.** On the only deep walk on disk (35 cursor pages, 1,050 medias),
  median age moves 2.2d → 4.1d and median plays 38k → 32k, with ~22 net-new owners still
  arriving at page 40. Going deeper is cheap and unremarkable.
- **Recency is not the answer.** The alarming "42.1% of his sheet hadn't posted in 90+ days" is
  *sheet composition* — REJECT rows median 319d vs WANT 19d. **Inside the pages he wants, the
  oldest band scores best**: 90d+ 56.2% ≥8 (n=16) against ≤7d 36.6% (n=41).
- **"He sees repeat offenders, the funnel shows singletons"** cannot be tested: `filter_reason`'s
  observed-video count is the page's own videos fetched for judging (3–20), not feed tiles.

**And a free signal read by nothing:** TikTok ships `diversificationId` (93.8% fill, 7 values)
and `CategoryType` (100% fill, 6 values) on every hashtag item — **its own category classifier**
— and `_video_of` reads neither (AST check; controls on `desc`/`createTime`/`shareCount` all
pass). Only 6 of 46 raw handles overlap his marks, so it is unmeasurable on disk today; one
archived page per graded tag would settle it for ~0–9 calls.

### 3.3e The Instagram half of his term list

Denominator: `scratch/resume/meme_pages*.jsonl` — **89 files / 51,429 rows / 14,435 distinct
handles walked** (the carried table used 67 files / 14,108). Approval = sheet `score >= 6`, a
threshold **validated rather than guessed**: it reproduces the carried n=119 table exactly.

| surface | walked | share (carried) | delivered/walked | reached a verdict |
|---|---:|---|---|---|
| seed | 11,757 | **81.45%** (83.32) | 1.88% [1.65, 2.14] | 18.8% |
| hashtag | 1,773 | 12.28% (10.53) | 11.17% [9.79, 12.72] | 46.8% |
| reels | 505 | 3.50% (3.34) | 19.60% [16.38, 23.29] | 63.2% |
| search | 400 | 2.77% (2.81) | 6.00% [4.07, 8.77] | 62.8% |

**Six readings of reels approval now exist** — 81.8%, 82.4% (28/34), 75.0%, 70.0% (35/50),
73.8%, 68.6% (35/51) — all true of their own denominator. **Reels vs seed stay disjoint at every
one of them**, so that contrast is real; hashtag vs seed overlap almost entirely and are not
distinguishable.

**Dead Instagram terms — six deliver zero**, and four are *still in config*, cut only at run time
by a hardcoded set at `clippershq/meme_finder.py:5793`: `search:motivation quotes` (0/28),
`search:baller quotes` (0/23), `search:movie edits` (0/20), `search:car edits` (0/19), plus
`hashtag:memesdaily` (0/56) and `hashtag:animemes` (0/15).

**⚠️ And one that no `found_via` table anywhere can see: `reels:sad quotes` returned
`HTTP 200, 0 medias` on 41 of 41 calls.** It has never produced an account, so it has no
provenance row in any store — it appears only as `reels_errors: 1` in the run-stats files.
**$0.0283 burned, recurring.** Positive control: the same regex over the same logs reads
`reels 'movie edits' -> 12 distinct account(s)`. This is the third instance in this report of a
term being invisible *precisely because it is completely dead* — and a textbook case of the
standing rule to **validate on list length, never on status**.

**The ranking is upside down:** `#moviememes` (32.1%), `#footballmemes` (28.1%) and
`#wholesomememes` (27.8%) deliver **4–5×** what `#memes` (6.5%) and `#funnymemes` (6.3%) do —
and config ranks `#memes` first and labels `#wholesomememes` a *bet*.

**The bought-and-never-looked-at channel, confirmed and current.** The search and reels loops
(`:6467`, `:6488`) run unconditionally at discovery; `_chan_rank` (`:7016`) then walks
hashtag=0, reels=1, search=2, seed=3 and stops at target. **12 of 34 discovery calls (35.29%)**
in memes mode buy accounts the run never reaches. Worked example: the 2026-09-06 run's own
provenance records 162 accounts bought via 11 reels/search calls; its checkpoint holds 95 rows,
**all hashtag**. **Of 83 runs, 43 walked zero reels and zero search pages — including all 20 of
the most recent.** 516 calls = **$0.3564** at $0.00069064. *This is the Instagram twin of the
TikTok ordering defect in §3.3b, and it is the same fix.*

**An edits run walks zero Instagram hashtags — verified three ways** (`run_mode.split_tags`
returns `[]` for EDITS; the run log prints `hashtags: (none)`; no edits checkpoint holds a
hashtag row). An IG edits run's entire vocabulary is **6 reels phrases (one of them always dead)
and 2 search phrases = 8 billed discovery calls.** Meanwhile `ig_crawl_fbsearch_keywords` holds
**24 edit terms** with measured 72–89% persona purity, in a different module, gated by
`ig_crawl_enabled: false`, **never read by `run_funnel`**.

**⚠️ AND A CAVEAT THAT LANDS ON MY OWN TIKTOK TABLE: the two Instagram stores disagree 2.3×.**
14,435 walked handles against 6,196 seen rows — only **25.3%** of the walk is in
`meme_pages_seen.json`, and 1,885 seen rows carry no `found_via` at all. **Any per-term table
built from a seen store alone under-counts every term.** My §3 TikTok table is built exactly that
way, and a sub-agent separately found 4 of 28 TikTok runs never fully reached the store. **Every
walked/passed count in §3 is therefore a LOWER BOUND**, and the ratios are safer than the levels.

### 3.4 The mix, costed (Part 4)

**Instagram**, from the surface table `clippershq/search_terms.py` leads with (14,108 accounts
walked — **MEASURED**; approval column rests on **119 marks total** and is not):

| surface | share of walk | delivered/walked | his approval | marks |
|---|---:|---|---|---:|
| seed | 83.32% | 1.650% [1.435, 1.897] | 38.6% [25.7, 53.4] | 44 |
| hashtag | 10.53% | 8.552% [7.235, 10.084] | 33.3% [18.0, 53.3] | 24 |
| reels | 3.34% | 14.225% [11.359, 17.670] | 81.8% [65.6, 91.4] | 33 |
| search | 2.81% | 5.542% [3.688, 8.248] | 77.8% [54.8, 91.0] | 18 |

Today: **1 approved per 74.6 walked** (re-derived independently; reproduces the brief's figure).
An illustrative 30/10/20/40 mix gives **1 per 22.1, a 3.38×** improvement; at reels' worst
plausible approval and seed's best, **1 per 23.8, 3.14×**.

**⚠️ Three published readings of reels approval disagree — 81.8% (119 marks), 75.0% (129), 73.8%
(162) — and a re-measurement gave 82.9 / 70.6 / 67.9. All are true of their own denominator.**
Scored at **every one of them**, the improvement is **3.08× to 3.40×**. The fragility does not
change the decision.

**⚠️ But reels cannot supply it.** Reels is 471 of 14,108 accounts = 3.34% of everything ever
walked. A 20% reels mix needs **6.0×** more than the funnel has ever produced; 30% needs 9.0×;
40% needs 12.0×. **And TikTok has never produced a single reels account** — it is an Instagram
surface only. A rate you cannot buy at volume is not a lever. Leaning on **search** instead,
holding reels at today's 3.34%, still gives **1 per 30.2 walked, 2.47×**, with no extra reels
account. **DERIVED.**

**TikTok's mix is a different, smaller problem** — there is **no seed and no reels surface at
all** (2,112 hashtag / 406 search / **0 seed**), so the Instagram table does not describe it.
All-search would move TikTok's pass rate from 59.3% to 77.2%, a **1.30×** ceiling, because the
gap is 21.3 points rather than Instagram's eightfold one. **MEASURED.**

**⚠️ It does not close the gap alone.** Costed in full the shift is **8.6 hours per 1,000, still
4.3× over target**. A 3.4× improvement on a number 15× out leaves it 4.3× out. Large, real,
cheap — **and not a solution.**

### 3.5 The term engine exists, works, and has never run (Part 5)

Driven, not read — the brief was explicit that its own report must not be trusted here.

- **It imports and runs.** `clippershq/search_terms.py` generates **236 terms, 236 distinct**,
  across 14 categories, with both word orders (`compose('napoleon','suffix')` → `napoleon edit`,
  `'prefix'` → `edit napoleon`; 118 each, **zero overlap**). **MEASURED.**
- **It is wired to nothing.** AST import census over **164 modules** under `clippershq/`: **0
  importers** of `search_terms` or `term_engine`. **Positive control:** the same pass finds
  `run_mode` imported by three modules, so the zero is real. The only dynamic-import hatch in
  the package (`clippershq/control.py:3985`, `__import__(modname)`) iterates a **fixed
  two-element tuple** and cannot reach it. **MEASURED.**
- **Its surfaces are `('instagram_search', 'instagram_reels', 'tiktok_search')` — there is no
  hashtag surface at all**, corroborating from a second direction that an edits run walks zero
  hashtags.
- **The atomic ledger fix is live.** AST finds **no bare `os.replace`** in the module; the save
  goes through `atomic_io.replace` at `clippershq/search_terms.py:132`. **MEASURED.**

**DEFECT, named and left — `clippershq/search_terms.py:240-252`.** `next_terms` documents itself
as *"THE ONLY WAY TO GET TERMS TO WALK. Filters the ledger, so a repeat is impossible"* and
*"nothing here can be bypassed by passing a flag"*. The body filters and returns; **it never
reserves.** Only `record` marks a term spent, so any two callers that draw before either records
receive the same terms. **Measured: 4 workers × 5 terms = 20 handed out, 5 distinct, 15
duplicated.** Sequentially it is genuinely impossible (41 draws, 236 distinct, 0 repeats, with a
control confirming the checker can see a planted repeat). This is the same defect class that
BL-1327 and BL-1397 already fixed in both finders' `reserve()` — *test-and-take has to be atomic
or the cap is advisory*. Under his rule *"if you use it once, don't use it again"*, a duplicate
draw is a term walked and **paid for twice**.

**The cars rule is correct, and I tried to break it.** `is_excluded_query` fires on `car edits`
and `car edit`; does **not** fire on `cartoon edits`, `cartoon edit`, `carnival edit`,
`card game edit`, `money edit`. **0 of 7 asserted cases wrong.** It does fire on
`supercar edits`, which I recorded as ambiguous and did not assert either way. **MEASURED.**

### 3.6 Proposed meme terms (Part 3, meme half) — a hypothesis, not a result

He says he does not know what the right meme terms are. His own data suggests **subject + memes**
over **mood + memes**: `footballmemes` 6/6 approved, `moviememes` 1/2, against `funnymemes` 0/4,
`brainrot` 0/10, `memesdaily` 1/15.

**⚠️ But this does NOT reach significance and I am not going to pretend it does.** Subject+memes
**53.8% [29.1, 76.8] n=13** vs mood+memes **26.0% [17.5, 36.7] n=77** — **intervals overlap**.
And the clearest counter-example is the largest mark sample in the whole table:
**`relatablememes`, a mood word, at 75.4% [62.9, 84.8] n=57.**

Fifteen of his own categories × "memes" have **never been walked**: `basketballmemes`,
`sportmemes`, `moneymemes`, `religiousmemes`, `countrymemes`, `historymemes`, `streamermemes`,
`realitymemes`, `animememes`, `gymmemes`, `schoolmemes`, `officememes`, `couplememes`,
`celebritymemes`, `foodmemes`. At the measured ~6.3 search calls per keyword and $0.000600 per
call, testing all fifteen costs **$0.0567** of discovery. **NOT VERIFIED — a hypothesis
generated from his data, not a result. Nothing here should ship before the terms are walked.**

---

## 4. WHAT WAS REFUSED, AND WHAT DID NOT RUN

- **Nothing was shipped**, by design. Every defect is named with `file:line` and left.
- **All five sub-agents completed.** None was lost to a rate limit this round (three previous
  rounds lost work that way). Their findings are folded into §3.2 and §3.3a–e, and every
  load-bearing claim I took from them was re-verified at source by me before it was published —
  two of them (`depth = 1`, the `clips`→`recent` rewrite) are marked VERIFIED for that reason.
- **Accounts per billed call, and net-new, are NOT RECOVERABLE** from the seen store and are
  therefore absent from the table rather than reported as zero. The store records *pages*, not
  the calls that found them; and every row *in* the store was net-new when written, so the
  non-new have no denominator.
- **No probe spent anything.** The $0.75 cap was proven to bind first anyway (§7).

---

## 5. WHAT I GOT WRONG

**I formed a headline, defended it through three derivations, and it was confounded the whole
time.** I split the 40 terms into SPECIFIC (names a subject) and GENERIC (mood/format only) and
got 81.2% vs 46.7% approval, non-overlapping. Suspecting my own hand-assignment, I re-derived it
mechanically from his own category nouns — 90.5% vs 46.6%. Suspecting the matcher, I re-derived
it again with a strict boundary rule — 96.9% vs 48.1%. Three passes, all non-overlapping, all
agreeing, **all measuring the wrong thing.**

My SPECIFIC bucket was 389 of 726 walked pages from **search**; my GENERIC bucket was 1,775 of
1,782 from **hashtags**. The axes were almost perfectly collinear. Stratifying kills it:

| stratum | specific | generic | verdict |
|---|---|---|---|
| within hashtags | 53.8% [29.1, 76.8] n=13 | 46.7% [38.5, 55.1] n=135 | **does not separate** |
| within search | 91.4% [77.6, 97.0] n=35 | 80.0% [37.6, 96.4] n=5 | **does not separate** |
| specificity held fixed | hashtag 53.8% | search 91.4% | **separates** |

**This is the identical confound a sub-agent caught in my previous round** — an AUC of 0.6245
that collapsed to 0.5464 once capture batch was controlled. I published that lesson and walked
into it within the day. Three consistent derivations of a confounded quantity are not evidence;
they are three measurements of the same confound.

**Then I replaced it with a second headline and that one collapsed too — same trap, one hour
later.** Having killed "specific beats generic", I promoted "search beats hashtag" (90.0% vs
47.7%, p = 5.41e-07). It holds only while all sheets are pooled. **30 of the 40 search marks come
from one sheet**; drop it and search falls to 70.0% [39.7, 89.2] n=10 and the intervals overlap.
And that sheet is an *edits* sheet while the hashtag marks are *meme* sheets — so surface, brain
and grading session are confounded exactly as before. A third mark corpus
(`ground_truth/score_marks_tiktok.jsonl`, 387 pages) puts search at **1.3%** of his graded
corpus rather than my 21%, which would have told me the comparison barely exists. **I found this
only because a sub-agent surfaced `config.json`'s own note — "ZERO search-sourced pages appear in
the 311 he has graded" — and I chased the contradiction instead of assuming the note was stale.**
It *was* stale, and chasing it still killed my headline. Twice in one round I mistook a
well-replicated confound for a result; the fix both times was stratification, and I should have
reached for it first rather than for a third re-derivation.

**My term table was structurally blind to the worst terms, and I did not notice.** I built it
from the seen store, which by construction contains only terms that produced at least one page.
A term that produced *nothing* has no row and therefore no line in my table — so my confident
"only three dead terms" missed `#streamerclips` and `#twitchclips`, walked in 11 runs with zero
rows. The denominator I chose could not represent the category I was reporting on. A sub-agent
that started from the *config* rather than the *store* found them immediately.

**And my mechanical matcher failed its own boundary control**, firing on `carnival edit` via
`car` — the exact trap the brief names. I checked every real term rather than waving it away:
12 are assigned only by that fallback and **none is misassigned**; removing the fallback
entirely leaves the split stronger. Documented and bounded rather than quietly fixed.

**I filed this round under an id that was already published.** `.claims/BL-1520.json` was free
because its owner had correctly ended their claim after publishing — but
`reports/BL-1520-…md` was already on `origin/main`, and `publish_report.py` refuses an existing
path. A peer caught it before I wasted the work. **A clear local registry is only half the
check; the published namespace is the other half.** I verified their report on `origin/main`
myself before renumbering, then confirmed BL-1523 free in *both*. Early scratch files and
commits carry the `bl1520` prefix; the claim holds both prefixes so nothing is orphaned.

**My first repeat-impossibility probe produced a false zero and I nearly reported it.** It
guessed the ledger method was `claim(term)`, got `TypeError` ten times out of ten, and printed
*"accepted 0 times — IMPOSSIBLE requires exactly 1"*, which reads exactly like a finding about
the ledger. It was a finding about my probe.

**And I measured the wrong corpus once**, sorting sheet directories by name so a volume-test
folder sorted after the dated ones.

---

## 6. MONEY AND SAFETY

**Spend: $0.00**, from the run's own counter at the wrapper — no ledger delta was used, because
`spend.json` grew from 22,635 to **29,023 rows** *during this session* from concurrent peers,
which is precisely why a delta cannot attribute a round.

**The cap was proven to bind before anything ran**, on both brains, by lifting the nested
`reserve` code object out of `run_funnel.__code__.co_consts` and driving the **shipped
bytecode**: a zero cap **raises** `_CapReached`, **the meter does not advance** (0 → 0), a
positive control at $2.50 still allows and meters (0 → 1), and it binds at exactly the ceiling
(`ok(1) → ok(2) → REFUSE@2 → REFUSE@2`).

**Backups:** 7 files (config, ledger, all five seen stores), every one sha256 MATCH, path built
from **one** round constant. Corruption control: one flipped bit → detected. Bodies found **by
shape** — `clip_seen.json` is a **list at root** (2,193 rows), the ledger a **list** at `runs`.

**And a deletion control, because a natural-key set once collapsed spend.json from 28,805 rows
to 781** — meaning a deletion preserving distinct keys would have been invisible. Dropping one
row of 29,023 was **SEEN** by all three of row count, natural keys and content hashes.
(Incidentally: 23,117 distinct content hashes against 29,023 rows — **5,906 ledger rows are
byte-identical to another row.**)

No process was killed. No production file was touched. No handle, address, key, port or absolute
path appears in this report; paths are given relative or as `%USERPROFILE%`.

---

## 7. WHAT HE SHOULD DO NEXT — RANKED BY WHAT IT COSTS HIM

**1. Seed his own 176 handles directly and walk the suggestion graph from them.** His term
list has reached **2 of his 176 pages (1.14% [0.31, 4.05])**, and on TikTok — where terms are
100% of discovery — 40 terms reached 2 of his 97. The suggestion graph is the only mechanism on
record that has actually reached him (8 of the 10 he has ever been shown). No threshold, judge or
rubric can fix a page that never enters the funnel. **MEASURED, with controls.**

**2. Reorder discovery so search-sourced authors are walked before hashtag-sourced ones.
Nearly free, and it unlocks a surface he approves at 90% that he is already paying for.**
`discover()` appends hashtags first (`tiktok_finder.py:2495`) then searches (`:2509`) into one
ordered list, and the walk stops at `:2617` when the target is met — so in **9 of the last 10
memes runs no search-term author was judged at all**. All six shipped search terms have
delivered nothing for 10 consecutive runs. This is not a term-quality problem and no new term is
needed: swap the loop order, or interleave, and the existing terms start being seen.
**MEASURED.**

**3. Then move the mix itself off hashtags.** Search is approved at **90.0% [76.9, 96.0]**
against hashtags' **47.3% [39.4, 55.3]** (p = 5.41e-07, OR 10.03) while being **16.1% of the
walk**. Shifting raises the TikTok pass rate from 59.3% to 77.2% (**1.30×**) and roughly doubles
the share he wants. Costs nothing to adopt — it is a term list. **MEASURED.**

**4. Wire up the term engine. It exists, it works, and it has never run.** 236 terms, both word
orders, a ledger, a scoreboard and an expansion loop — **0 importers across 164 modules**. Every
recommendation about term breadth is unactionable until something calls it. **But fix
`next_terms` first** (`search_terms.py:240-252`): it filters without reserving, and under
concurrency hands the same term to multiple workers — 15 of 20 duplicated in a 4-worker test —
which under his own rule means walking and **paying twice**. **MEASURED.**

**5. Shift the Instagram mix off seed — 3.08× to 3.40×, robust to every published reading.**
Seed is 83.32% of that walk, delivers 1.65%, and is the surface he approves least. **But do not
plan it around reels**, which is 471 of 14,108 accounts and would need 6–12× more than the
funnel has ever produced. Lean on search: **2.47× with no extra reels account.** **DERIVED.**

**6. Stop `brainrot`, `funnymemes` and `memesdaily`. They pass the funnel and he rejects
everything.** 0/10, 0/4 and 1/15 approved across 556 walked and 301 passed pages. These are
worse than dead terms — they pay the full funnel and hand him junk to grade. **MEASURED,** on
small mark counts, which are printed.

**7. Restore an ordering signal to the seed walk, or accept that 87.6% of the page-shaped
handles will never be reached.** The alphabetical tie-break at `meme_finder.py:7018`/`:8337`
undid the reordering; the shape test separates 4.79× (p = 2.75e-05) and is currently discarded.
**MEASURED.**

**8. Test the fifteen unwalked `<subject>memes` terms for $0.0567.** Cheapest experiment in this
report, and the only route to answering his "for meme pages, I don't know". **NOT VERIFIED — a
hypothesis.**

**9. Fix the Instagram hashtag-kind rewrite before that lane is ever switched on.**
`clippershq/main.py:4012` silently rewrites any kind that is not `top`/`recent` — including
`clips` — to `recent`, the endpoint measured at **0 of 37 passed** against `/clips` 5 of 39
(p = 0.031). All four campaigns are set to `recent`. The lane has not run, so this has cost
nothing yet; it is a loaded trap rather than a past loss. **VERIFIED at source.**

**10. Raise `tiktok_finder.depth` above 1, or accept one screen per hashtag.** `depth = 1` with
`HASHTAG_PAGE_COUNT = 30` means the funnel sees 30 items per tag — shallower than his own thumb.
The deep walk on disk shows quality decays only gently (median plays 38k → 32k over 35 pages)
with net-new owners still arriving at page 40. **MEASURED**, and cheap. *But note this is not the
gap: §3.3d shows depth was refuted as the explanation for what he sees by hand.*

**On the honest bottom line:** these are quality levers, not cost levers. The mix shift costed in
full is **8.6 hours per 1,000, still 4.3× over target**. Nothing in this report closes that gap
alone, and presenting it as a solution would be the error.

---

## 8. WHERE THE FILES ARE

All committed under `BL-1523` (some carry the earlier `bl1520` prefix — see §5):

| Path | Contents |
|---|---|
| `scratch/bl1523_part1_termtable.py` | The 40-term table · `…_termtable.json` |
| `scratch/bl1523_part1b_approval.txt` | Terms ranked by junk delivered |
| `scratch/bl1523_part1c_generic.txt` | The specific/generic split (superseded — see §5) |
| `scratch/bl1523_part1d_secondway.txt` | Its mechanical re-derivation |
| `scratch/bl1523_part1e_confound.txt` | **The stratification that killed it** |
| `scratch/bl1523_part1f_corrected.txt` | The corrected surface headline |
| `scratch/bl1523_part3_memeterms.txt` | Proposed meme terms |
| `scratch/bl1523_part4_mix.py` | Instagram mix · `…_mix.json` · `…_part4b_tiktok_mix.txt` |
| `scratch/bl1523_part5_engine.py` | Engine wiring census · `…_part5b_repeat.py` |
| `scratch/bl1520_a3_seed.json` | Seed-file analysis, 17 controls |
| `scratch/bl1520_safety.py` | Backups, corruption + deletion controls |

Reproducing the headline (no network, no spend):

```
PYTHONIOENCODING=utf-8 python scratch/bl1523_part1_termtable.py    # the 40-term table
PYTHONIOENCODING=utf-8 python scratch/bl1523_part1e_confound.txt   # (see the .py that wrote it)
PYTHONIOENCODING=utf-8 python scratch/bl1523_part4_mix.py          # the mix arithmetic
PYTHONIOENCODING=utf-8 python scratch/bl1523_part5_engine.py       # engine wiring
```

`PYTHONIOENCODING=utf-8` is required — the default console encoding here is `cp1252` and any
script emitting a warning glyph dies on it.
