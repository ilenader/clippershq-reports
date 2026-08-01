# MEMEBOT-056: what this system actually produces, end to end

**Date:** 2026-08-01 · **Type:** Read-only audit · **Spend:** $0.00 · **No code changed, no paid call, no render**

Measured on `master_leads.csv`, 24,933,620 bytes, mtime 2026-08-01 22:55:07, and on a frozen copy of `clip_library/` (BL-928 was appending during the audit). Every figure below comes from the artefact a stage actually writes. Nothing is carried over from an earlier report: ~200 rounds landed today and most numbers in circulation were true when written.

Tiers: **RECEIPT** (a ledger row exists) · **MEASURED** (counted here) · **INFERRED** (derived, marked) · **UNKNOWN**.

---

## 1. THE FUNNEL — hashtag to finished video

| # | stage | count | survives from previous | of library |
|---|---|---:|---:|---:|
| 1 | hashtags configured | **20** | — | — |
| 2 | posts reachable in one full pass (20 tags × 2 pages × 30) | **1,200** | — | — |
| 3 | confirmed repost pages in master | **239** | 19.9% of posts seen | — |
| 4 | pages actually walked for clips | **172** | **72.0%** of pages | — |
| 5 | clips in library (6,326 rows → distinct) | **2,003** | ~11.6 clips/page | 100% |
| 6 | clips with a vision label | **1,984** | 99.1% | **99.1%** |
| 7 | clips the matcher matches | **286** | **14.4%** | 14.3% |
| 8 | clips passing the render gate | 1,773 | 88.5% | 88.5% |
| 9 | **RENDERABLE** (matched **and** gated) | **244** | — | **12.2%** |
| 10 | **finished videos on disk** | **32** | **13.1% of renderable** | **1.6%** |

**The funnel has one narrow point and it is not where the effort went.** Discovery, walking and labelling are all healthy — 99.1% of the library carries a vision label. **The matcher rejects 85.7% of it**, and that is a supply problem in the song store, not a matcher fault: there are four songs and three reachable moods.

```
tiers:  PARK 1,717   VISION_RULE 276   FRANCHISE_MOOD 10
moods:  hype 249     warm 34           melancholy 3      triumphant 0
```

**87% of every match routes to one mood.** `sng_0002` (triumphant) matched **zero** of 2,003 clips — its own store note predicted this ("MEMEBOT-019 found essentially NO clips in the library for this song"), and it is still true at 5× the library size. Adding songs in moods the library already has is worth more than any further matcher work.

**Stage 4 is the cheapest unclaimed gain**: 67 confirmed pages (28%) have never been walked. They are already paid for.

**Stage 10 is where it actually breaks.** Of 64 render records, **19 ok, 41 `failed:render`, 4 with no status** — a 64% failure rate, and the recorded errors are one bug:

```
ambient_bed.file='C:\Users\...\clipper finder' was requested and does not exist
ambient_bed (skipped: C:\Users\...\clipper finder not found)
```

That is the empty-bed-path defect MEMEBOT-049 flagged and left open: a clip with no song resolves `os.path.join(cwd, "")` to the **repo root** and hands the renderer a directory as its audio bed. **It is the single largest yield loss in the system.** The 13 renders produced under controlled conditions today (MEMEBOT-042's 3 + MEMEBOT-049's 10) succeeded 13/13 because every clip in those batches matched.

---

## 2. TRUE COST OF ONE FINISHED VIDEO

Ledger: **212 entries, 208 receipts, 4 labelled ESTIMATE.**

| bucket | usd | note |
|---|---:|---|
| ledger `total_spent_usd` as recorded | 9.2167 | includes the estimate rows |
| rows labelled **ESTIMATE** (excluded) | **0.9182** | back-filled by rounds costing work they did not do |
| **receipts only** | **8.2984** | |
| — of which **video pipeline** | **$4.3338** | RECEIPT |
| — of which lead-gen / other funnels | 3.9646 | different product; excluded below |

Video-pipeline receipts by stage:

| stage | usd | calls | tier |
|---|---:|---:|---|
| vision labelling (all VISION campaigns) | **3.2814** | 3,476 | RECEIPT |
| clip walk (`CLIP_LIBRARY`) | 0.5730 | 955 | RECEIPT |
| repost discovery (`REPOST_FINDER`) | 0.3666 | 611 | RECEIPT |
| render retrieval (`memebot`) | **0.0282** | 47 | RECEIPT |
| audits/probes (BL-858/864/873/918/925/897) | 0.0846 | 141 | RECEIPT |

**Two honest per-video numbers, 188× apart:**

- **Average, all-in: $4.3338 ÷ 32 = $0.135 per finished video.** This is the true historical cost and it is dominated by labelling 2,003 clips to render 32.
- **Marginal, given a labelled matched clip: $0.00072.** MEMEBOT-049's batch spent $0.0072 in retrieval for 10 videos, 1.2 calls each.

The right figure depends on the question. For "what did the 32 cost", it is $0.135. For "what does the 33rd cost", it is **under a tenth of a cent** — the library is a sunk asset with 212 renderable clips still unused.

**Corrections to figures in circulation:** the ledger now *does* carry `vision_spent_usd` ($2.1438) — BL-877's finding that no such parameter existed has been fixed since. Any per-video cost quoted before that fix under-reported by roughly 40%.

**INFERRED, not measured:** ffmpeg render CPU, EasyOCR and Silero CPU during discovery and speech classification. All local, none metered, all real. The $0.135 is a floor.

---

## 3. THROUGHPUT AND THE BINDING CONSTRAINT

| stage | measured rate | binding constraint |
|---|---|---|
| repost discovery | 4 tags × 6 pages ≈ **2 h**, $0.021 | **wall clock** — the account gate runs EasyOCR over 12 thumbnails per candidate, ~16 s each. A $0.25 cap is not a constraint; time is |
| clip walk | 955 calls → 2,003 clips ≈ **2.1 clips/call** | **API pages**; cheap and fast |
| vision labelling | 3,476 calls → 1,984 labels | **money** — 76% of all video-pipeline spend |
| speech classification | 1,359 of 2,003 (67.8%) | **CPU**, 0.547 s/clip (BL-848) |
| song matching | instant, local | **song-store supply** — 4 songs, 3 reachable moods |
| render | **10 videos in 8.3 min ≈ 72/hour** | ffmpeg CPU, single-threaded per clip |
| outcome loop | — | **a human step that does not exist** |

**The system can render ~72 videos/hour and has 212 unused renderable clips — about 3 hours of work already paid for.** Nothing about throughput is currently limiting; supply into the matcher is.

---

## 4. SUBSYSTEM STATUS, HONESTLY

| subsystem | status | evidence |
|---|---|---|
| Lead funnels (IG/TikTok/Spotify/Twitch/YouTube/GP) | **works** | 58,988 master rows, $3.96 of receipts |
| Repost discovery | **works with caveats** | 239 pages. Seen-cache holds 1,491 posts vs 1,200 reachable per pass — **the bank is exhausted at depth 2**; only depth or new tags yield more |
| Clip walk | **works** | 2,003 clips, 172 accounts, 6,326 rows (3.2× revisions) |
| Vision labelling | **works** | 99.1% coverage. Control signal caught **3 rows** where the model answered an unanswerable question |
| Speech classification | **works with caveats** | 67.8% `speech_frac`, 92.5% `audio_class` — a third of the library has no measured speech |
| Song matching | **built, starved** | Correct and reachable since MEMEBOT-042; 4 songs, 1 mood carries 87%, 1 song matches nothing |
| Rendering | **works with caveats** | 13/13 under controlled conditions; **41/64 historical failures**, all the empty-bed bug |
| Dashboard | **works with caveats** | Its own test suite writes the live `config.json` and destroyed a key (BL-855) |
| Outcome loop | **built, wired, receives nothing** | see below |

### The outcome loop is not unreachable — it is starved

`run_batch → bias_for → song_library.bias_map → outcome_loop.resolve/should_bias` is a complete chain. It returns `{}` and always will, because **0 of 64 render records carry any outcome data.** Nothing posts the videos and nothing writes back views. The loop is *open*, not broken, and no amount of rendering closes it.

---

## 5. BUILT WITH NO CALLER

25 modules have no production importer. Most are legitimate CLI entry points (`claim.py`, `publish_report.py`, `verify_claims.py`, `run.py`, `probe.py`, `preflight.py`, `stillness.py`, …) — invoked as `python x.py`, invisible to an import graph.

**Genuinely uncalled — no entry point and no production importer:**

| module | status |
|---|---|
| `clippershq/clip_cuts.py` | MEMEBOT-038's cut detection. Tests + scratch only |
| `clippershq/song_loudness.py` | tests + scratch only |
| `clippershq/tag_yield.py` | tests only |
| `clippershq/artist_genre_map.py` | tests only |
| `clippershq/track_id.py` | tests + scratch only |
| `clippershq/enrich.py` | nothing at all |

**Named in the brief, checked individually:**

- **`stillness.run_checked()`** — one caller, `tests/test_claims_manifest.py`. Its own docstring says it "exists for every OTHER check in this repo that must parse a program's output"; those other checks still do not use it.
- **`stillness.poll()` / `--poll`** — CLI only, no programmatic caller.
- **`vision_parse_lossy`** — declared in `CLIP_FIELDS` and **read by nothing**. The truncation marker is written and never consulted. This is the "computed then discarded at a boundary" shape, in its purest form: the value reaches disk and no consumer exists.
- **`outcome_loop`** — *not* uncalled. Wired and starved (§4).

**Caveat:** an AST walk cannot see `getattr`, config-driven dispatch or CLI subcommand tables, so this is a lower bound. Each hit above was checked by hand.

---

## 6. WHAT BREAKS AT FULL SCALE TOMORROW

1. **The empty-bed bug eats ~64% of renders.** Any clip that parks fails. At scale that is the dominant loss and it is one guard in `pick_song`.
2. **Mood collapse.** 87% of matches are `hype`, served by one song with 5 hook windows. The no-repeat rule (k=3) will exhaust rotation within 4 videos and divert everything to the LRU corpus — which is what 5 of MEMEBOT-049's 10 renders already did.
3. **Discovery returns nothing.** The seen-cache already covers 124% of one full pass. A scaled run at current settings spends money and finds no new pages.
4. **No feedback.** Every video is chosen with zero evidence about what performed. `bias_map` returns `{}` and will forever until something posts and reads back.
5. **The test suite mutates production config.** Already destroyed one key. At scale, config drifts under whoever runs the suite.
6. **Concurrency has no arbiter.** 9–13 rounds ran all day against one tree; claims are advisory, and at least three rounds queued 40+ minutes on files that were never modified.
7. **Vision cost dominates and is unbounded.** 76% of pipeline spend. Labelling scales with the library; renders do not.

---

## The one-line answer

**The system reliably produces a finished, correctly-scored, audio-verified video — 13 of 13 when the inputs are clean — and it converts only 1.6% of its library into one, because four songs cover three moods and 64% of historical renders died on a single unfixed path bug.** The expensive half is built and working. The cheap half is what is missing.
