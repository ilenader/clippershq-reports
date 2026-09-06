# BL-1518 — SPLIT THE TWO TIKTOK BRAINS

**Round:** BL-1518 · **Date:** 2026-09-06 · **Spend: $0.00** · **Production files changed: none**

---

## THE ANSWER, IN ONE PARAGRAPH

**Should edits run differently? Yes — and the reason is not the one anybody expected.** Edit
pages do not need different *rules*; they need a different *supply*. Measured on the funnel's
own 2,518-page TikTok history, pages found by typing "&lt;subject&gt; edit(s)" convert at **81.9%
[73.9, 87.8] (n=116)**, pages found by other search terms at **75.3% [69.9, 80.0] (n=279)**,
and pages found by meme hashtags at **55.9% [53.7, 58.0] (n=1,983)**. More decisive than the
gap is *what the rejections say*: of the edit-term rejections whose reason was recorded, **0 of
11 were content rejections** — every one was the 180-day recency wall or the view floor. In the
hashtag arm the same classifier found **10 of 50 (20.0% [11.2, 33.0])** content rejections. So
the funnel almost never rejects an edit-term page *for not being an edit page*. **His 95% claim
survives every test I could run without spending, and the honest bracket is 81.9%–100% with all
recorded evidence at the top of it.** What it costs today is **$1.19 per 1,000 delivered edit
pages** (1.77 calls/page) against **$1.47 for memes** (2.14 calls/page) — edits are *already*
the cheaper brain. The target of **$0.50 per 1,000 is 2.4× away**, and **75.7% of the edits
brain's spend is a single call** (`videos_from_handle`) bought for every walked page before any
content rule can reject it. That is the only stage large enough to close the gap, and the
existing evidence says it cannot safely be skipped — so **$0.50 is not reachable today**, and
Section 7 says what would have to be measured to reach it.

---

## 1. WHAT THIS ROUND WAS ASKED TO DO

His claim, verbatim:

> "For TikTok edits, if you type anything and then edit — Napoleon edit, football edit, history
> edit — 95% are going to be edits. It's so simple. But for memes it's a bit different. Edits
> should cost less than fifty cents per thousand good ones."

The round was to test that **non-circularly**, then build the light path it justifies. The
circular version of this test had already been run and returned **98.4%** — a tautology, because
it searched "&lt;subject&gt;edits" and then checked whether the account *name* contained "edits".
The search matched on the name; the test re-read the search. An earlier honest attempt returned
**22.7%**, median 0.205.

Seven parts were asked for. **Six were delivered, one was not** — see Section 4.

---

## 2. WHAT SHIPPED

Nothing was changed in any production file. This round shipped **instruments**, all committed:

| File | What it is |
|---|---|
| `scratch/bl1518_claim_harness.py` | The scoring spine. Wilson intervals; three instruments held apart **by construction** |
| `scratch/bl1518_instrument_b.py` | His grades, attributed to the term that found each page |
| `scratch/bl1518_instrument_a2.py` | The walked-supply denominator, from the seen store |
| `scratch/bl1518_reason_split.py` | Content-vs-business rejection classifier, with controls |
| `scratch/bl1518_cost.py` | Per-brain cost per 1,000 delivered, stage by stage |
| `scratch/bl1518_term_ledger.py` | The term engine (178 terms, 14 of his categories) + atomic ledger |
| `scratch/bl1518_capproof.py` | Cap proof driving the **shipped bytecode** of both brains |
| `tests/test_bl1518_term_ledger.py` | 6 tests, all green |

### The harness refuses rather than requests

The brief said report the instruments separately and never average them. A docstring saying
"please do not average" gets averaged by the next round, so the object has **no pooled accessor
across instruments**, and comparing two instruments raises `TypeError`. Two other guards:

- **His supplied reference accounts cannot be used as a test set.** They are edit pages *by
  construction* — he chose them because they are edit pages — so scoring the claim on them
  returns ~100% and measures his selection, not the claim. Passing one raises `ValueError`.
- **`name_is_circular_evidence()` is called at the point of scoring**, not at the point of
  writing the report. The 98.4% figure came from code that looked reasonable line by line.

Self-test output, both guards firing:

```
guard fires: reference used as test set   ValueError
guard fires: two instruments compared     TypeError
scored 2, excluded 2 -> 50.0% [9.5, 90.5] n=2 (1/2)
UNJUDGED -- not a rejection x1, circular: name matches the term x1
```

### The term ledger is journal-first, not replace-first

His rule: *"If you use it once, don't use it again — squeeze every editor from that niche."*
The obvious implementation holds the ledger in a dict and does write-temp-then-`os.replace`.
**On Windows that rename raises whenever any process holds the destination** — an antivirus
scanner, the indexer, or one of five other rounds in flight reading the file. And the failure
is the worst available one: the save raises, walked terms go unrecorded, and the next run
re-walks and **re-pays** for them. The ledger's only purpose fails exactly under contention.

So the source of truth is an **append-only JSONL journal** (an append holds no destination and
cannot be blocked), `fsync`-ed. The compacted snapshot is cosmetic and is *allowed* to fail.
`load()` reads the journal, never the snapshot.

The test **holds the file for real** rather than mocking the raise — a mock would prove only
that the `except` clause is reachable, and would keep passing if the platform ever stopped
raising. It first asserts the platform genuinely refuses (skipping if not), then asserts the
ledger survived. **It did not skip: Windows refused the rename and both walked terms survived.**

A torn *last* line is tolerated (a crash mid-append); a torn *middle* line **raises**, because
"the file is unreadable" and "no terms have been walked" are the same zero to a naive reader
and have opposite consequences.

---

## 3. WHAT WAS MEASURED

### 3.1 The instrument that made a free test possible

`found_via` is stamped on **2,518 of 2,518 TikTok pages — 100% fill, cardinality 40**. Page
provenance is recoverable from history, so his grades can be attributed to the search term that
produced each page **without a fresh run and without spending anything**. Twenty of the forty
values are hashtags, twenty are search terms.

Search terms are safe to publish; these are the twenty, with the pages each produced:

| Search term | Pages | Edit term? |
|---|---:|---|
| amvedit | 41 | no (no space before suffix) |
| car edits | 39 | **yes** |
| movieedit | 36 | no |
| cinematicedit | 33 | no |
| velocityedit | 31 | no |
| movie edits | 29 | **yes** |
| relatable quotes | 23 | no |
| scenepack | 23 | no |
| anime edits | 22 | **yes** |
| meme compilation | 18 | no |
| motivation quotes | 16 | no |
| football edits | 16 | **yes** |
| fan edit | 14 | **yes** |
| fanedit | 12 | no |
| football quotes | 11 | no |
| relatable memes | 10 | no |
| baller quotes | 9 | no |
| sad quotes | 9 | no |
| relatable | 7 | no |
| funny edit | 7 | **yes** |

**A definition, stated because it changes the numbers.** An *edit term* here is a **search**
whose keyword ends in `edit`/`edits`. A hashtag is **not** a search term and is excluded — his
claim is about what you *type*, and `hashtag:animeedit` is a different surface with different
reach. Terms like `amvedit` and `movieedit` are excluded too: they are single tokens, not
"anything **plus** edit". That is a conservative reading and it *shrinks* the edit-term arm
from 226 pages to 127. A looser reading would raise the n and could only help the claim.

### 3.2 The three denominators — reported separately, never averaged

His claim is about **what the search returns**. The funnel records pages at two later stages,
and naming which one a number came from is the difference between an answer and a mistake.

| Denominator | Edit terms | Other search terms | Hashtags (memes) |
|---|---|---|---|
| **Delivered to a sheet** (his grades) | **96.8% [83.8, 99.4]** n=31 | 66.7% [35.4, 87.9] n=9 | — |
| **Walked** (seen store) | **81.9% [73.9, 87.8]** n=116 | 75.3% [69.9, 80.0] n=279 | 55.9% [53.7, 58.0] n=1,983 |
| **Raw search output** | **not measurable from history** | — | — |

**Instrument (b), the delivered row, is a lower bound on his claim and is not the claim's own
number.** It asks "did he *want* the page", not "is it an *edit page*". A genuine edit page he
does not want — too small, wrong language, no address — counts against it. Reporting 96.8% as
"his claim confirmed" would be a denominator substitution, which is the most common way this
project has published a wrong number.

**The walked row is one stage closer to raw supply but still not raw.** A page reaches the seen
store only after discovery has already dropped candidates. Raw search output is not recorded
anywhere and needs a fresh run to measure.

`passed` is **not a clean boolean** — the value census is `True 1,413 / False 965 / None 140`.
`None` is UNJUDGED, not a rejection, and it leaves **both** sides of every ratio above.

### 3.3 Why 81.9% does not refute 95% — the finding that reframes the question

The walked interval [73.9, 87.8] **excludes 95%**. Read naively, that refutes him. It does not,
because `passed` conflates two different questions:

- **Is it an edit page?** — the thing he claimed
- **Is it worth contacting?** — recency, view floor, address, size

A perfect edit page can fail the 180-day recency wall. That rejection is evidence about the
account's *activity*, not about whether the search found an edit page.

Classifying every recorded rejection reason into CONTENT versus BUSINESS:

| Supply | Rejects | CONTENT | BUSINESS | unrecorded | unclassified |
|---|---:|---:|---:|---:|---:|
| Edit terms | 21 | **0** | 11 | 10 | 0 |
| Other search terms | 69 | 0 | 0 | 69 | 0 |
| Hashtags | 875 | **10** | 40 | 823 | 2 |

Of the rejections whose reason *was* recorded:

- **Edit terms: 0.0% [0.0, 25.9] (0/11) content rejections** — 10× recency wall, 1× view floor
- **Hashtags: 20.0% [11.2, 33.0] (10/50) content rejections** — 36× recency, 10× model verdict on content, 4× view floor

**The hashtag arm is the positive control.** The CONTENT bucket is not empty by construction —
it caught 10 real content rejections on real data — so the zero in the edit-term arm is a
genuine zero and not a dead detector. The classifier was also proved on planted controls in
both directions before running, and reports UNCLASSIFIED rather than defaulting.

**So the honest bracket for his claim, on the walked denominator (n=116):**

- **Floor 81.9%** — if *every* rejection, including all 10 with no recorded reason, were a content rejection
- **Ceiling 100.0% [96.8, 100.0]** — if none were, which is what all 11 recorded reasons say
- **All recorded evidence sits at the ceiling.** 0 of 11.

**His 95% sits comfortably inside that bracket.** It is not proven to the decimal — n=116 with
10 unexplained rejections cannot do that — but nothing I measured contradicts it, and the
comparison arm (memes/hashtags, where 1 rejection in 5 *is* a content rejection) behaves exactly
as he said it would: *"for memes it's a bit different."*

### 3.4 Part 2 — every rule, measured separately for the two brains

The census result is short, and it is the answer: **the two TikTok brains differ in exactly two
places in the entire codebase.**

AST census (not text matching — a byte-window guard in this repo once went red on a comment):

```
clippershq/tiktok_finder.py -- 0 branches on the brain
clippershq/free_judge.py    -- 2 branches on the brain
     759  if mode is not None
    1101  if _scored and str(mode or "").strip().lower() == "edits"
```

1. **The search term list** (`run_mode.py`), which the module itself documents as a *supply*
   choice, not a filter: *"the mode picks WHICH TERMS ARE SEARCHED, and nothing downstream
   changes: no new gate, no new rejection, no verdict moved."*
2. **One sentence in the judge prompt** (`free_judge.py:1101`) — a caveat added to the worked
   examples warning that they were graded while he was looking for meme pages.

Every rule, threshold, gate, paid call and picture is **byte-identical** between the brains.
There is nothing to "split" downstream because nothing downstream was ever joined. The order of
paid calls in `_process` is identical for both:

```
2585-2672  eight free early returns   (free rejections, before any spend)
2706       judge_author               (free)
2744       videos_from_handle         <-- FIRST PAID CALL, for every walked page
3267       judge_page                 (paid vision judge)
3365       profile_of                 <-- gated on is_target since BL-1516
```

### 3.5 Part 3 — what a delivered page costs, per brain

| Brain | Terms | Walked | Delivered | Calls/page | $/1,000 | Target | Gap |
|---|---:|---:|---:|---:|---:|---:|---:|
| **EDITS** (search, "&lt;subject&gt; edit(s)") | 6 | 127 | 95 | **1.77** | **$1.19** | $0.50 | **2.4×** |
| **MEMES** (hashtag supply) | 20 | 2,112 | 1,108 | **2.14** | **$1.47** | $0.50 | **2.9×** |

Stage by stage, as a share of that brain's TikTok calls:

| Stage | EDITS | MEMES | Why |
|---|---:|---:|---|
| discovery | 37.8 calls (22.5%) | 220.0 calls (9.3%) | 6.3 calls/keyword; 11 calls/hashtag |
| **`videos_from_handle`** | **127.0 (75.7%)** | **2,112.0 (89.2%)** | **1 per WALKED page, before any content rule can reject** |
| `profile_of` | 3.0 (1.8%) | 34.6 (1.5%) | only for kept pages lacking a free bio address |

**Edits are already the cheaper brain**, by 19%, entirely because they waste less: edit terms
walk 127 to deliver 95 (25% waste), hashtags walk 2,112 to deliver 1,108 (48% waste).

**$0.50 per 1,000 buys 833 TikTok calls = 0.83 calls per delivered page.** Today's edits figure
is 1.77.

### 3.6 The shipped cost estimator is wrong in both directions at once

`tiktok_finder.estimate()` is what he would consult to decide whether a run fits his budget.
Driven on 178 search terms:

- **Discovery: 6.3× LOW.** It bills 1 call per keyword, on the stated ground that *"/v2/search
  does not paginate and there is no second page to buy"*. That was refuted by BL-1469 and fixed
  **in the same file** — `videos_from_search` walks `page_id` to exhaustion at ~6.3
  calls/keyword. The comment survived the fix. On 178 terms: **178 calls estimated, 1,121
  actual — $0.566 understated.**
- **Profile: roughly 30× HIGH.** It bills "one profile per reachable author", 1:1. BL-1516 moved
  `profile_of` behind `is_target`, and the free bio address covers 96.88% of TikTok pages.

Two errors in opposite directions **partially cancel**, which is worse than one error: the total
looks defensible while no line in it is.

### 3.7 The cap was proven on both brains before anything ran

`reserve()` is a closure nested inside `run_funnel`, so the tempting probe re-types its five
lines and asserts on the copy — which measures the probe. Instead the nested code object was
lifted out of `run_funnel.__code__.co_consts` and rebuilt with `types.FunctionType` and cells I
control, so **what raises is the function the funnel actually calls**.

| Check | TikTok brain | Meme brain |
|---|---|---|
| zero cap refuses | RAISED `_CapReached` | RAISED `_CapReached` |
| refusal is an exception, not a return | yes | yes |
| **meter does not advance on refusal** | 0 → 0 | 0 → 0 |
| positive control: $2.50 still allows | allowed, metered 0 → 1 | allowed, metered 0 → 1 |
| binds at exactly the ceiling | `ok(1) → ok(2) → REFUSE@2 → REFUSE@2` | same |

**The two closures have different free variables** — TikTok reconciles through a ledger flush
(`_reconcile_unlocked`, `_flush_spend`), Instagram through the client's own receipt count
(`igc.http_requests`). A probe built for one shape would have proved a cap on one brain and
silently reported nothing on the other; the builder **refuses rather than guesses** when a free
variable is unaccounted for, which is how the difference was found.

### 3.8 Part 5 — does edits need a different picture? No. But the picture is broken anyway.

**The picture is not where the money is, and that is the answer to the part as asked.** The
whole picture pipeline costs about **2.4 seconds per page and effectively $0**: cover fetch and
compose ~2.06s (12 parallel CDN fetches, the binding stage), composing 0.29s, JPEG encoding
0.04s. A cheaper picture cannot move edits from $1.19 to $0.50, because that gap is upstream in
call volume. Three corrections to what this round started with:

- **The 155×275 crop is dead**, fixed by BL-1499. `crop_to_one_cover = (not frame_strip) and
  n_tiles <= 1` — multi-tile sheets now go through `grid_b64` uncropped. Carrying the old
  figure forward would have been wrong.
- **OCR never runs on the live path.** `speech_fracs = None` is a literal at the judge call
  site, and `ocr_can_change_a_verdict(speech_fracs=None)` gates the work, so the gate is inert.
  `OCR_SECONDS_PER_PAGE = 32.9` is still pinned by `tests/test_bl1333_speed.py:225` — a pinned
  constant for a stage that does not execute. Freshly measured, if it did run it would be
  ~23.4s/page, so the pinned number is wrong *and* moot.
- **`frame_strip` is still unwired** — the one production call site never passes it.

**But measuring the picture turned up a defect worth more than the question asked.** Using a
blank-cell detector proved on planted controls (a fully flat sheet reads 12/12 blank; a
3-filled sheet reads exactly 3 filled — pixel *variance*, not darkness, because the builder
paints grey 24 and a prior detector tested grey&lt;16 and scored a fully empty sheet as 0.0 blank):

| Run | Sheets | Exactly ONE panel of 12 | All 12 panels |
|---|---:|---:|---:|
| 20260905_235818 | 70 | **53 = 75.7%** | 10.0% |
| 20260905_212810 | 63 | **34 = 54.0%** | 15.9% |
| bl1260_volume | 134 | 0 = 0.0% | 28.4% |

Pooled over the two most recent dated production runs: **87 of 133 = 65.4% [56.9, 73.1]** of
pages reached the judge carrying **one panel out of twelve**, padded onto a mostly-blank
465×992 canvas. It is **not** a universal property — the volume corpus shows 0% — so it varies
by run and the pooled figure should not be quoted as a constant.

**Why this matters more for edits than for memes, and why it belongs in this round:** a meme
page can be recognised from one still. **An edit page cannot.** What makes a page an edit page
is motion, cut rhythm and overlay text across time — precisely what a single cover frame
destroys. The judge is being asked the edits question, on three pages in five, from the one
piece of evidence that cannot answer it. This is a quality defect, not a cost one, and it is a
plausible contributor to the 75.8% [69.1, 81.5] accuracy ceiling measured in an earlier round.
**It is a hypothesis, not a measurement — I did not test whether panel count predicts judge
accuracy**, and it should be tested before anything is built on it.

### 3.9 Part 6 — the reserved question, and a refutation

One agent was given one question and deliberately no list of places to look: *what is different
about an edit page that nothing in this funnel currently measures?* Its strongest result is a
**refutation**, which is the more useful outcome.

**The "edit pages look different" hypothesis is refuted once a confound is controlled.** Pixel
colour-saturation, monochrome fraction and edge density were measured on the judge's own cover
images, 224 edit-labelled versus 1,520 hashtag-labelled TikTok pages (labels from `found_via`,
the same mechanism used throughout this round).

| | Saturation AUC | n |
|---|---:|---|
| Uncontrolled | **0.6245** | 220 / 220 |
| Restricted to capture batches holding **both** labels | **0.5464** | 96 edit / 364 meme |

The uncontrolled figure looked promising; the edit and meme samples had simply been captured in
**different batches under different pipeline settings**. Restricting to the two capture
directories that hold both labels collapses it to a coin flip, and every other pixel feature
sits in 0.42–0.60 — the same flat band this project has already learned to distrust. The
detectors were validated first on planted synthetic controls where they separate cleanly
(saturation 148.8 vs 0.0; monochrome fraction 0.003 vs 1.0), **so the flat real-world result is
a genuine absence of signal rather than a broken instrument.**

**What it found instead is structural, and it has never been extracted.** `aweme_type` is
TikTok's own video-versus-photo-carousel flag, 100% filled on 2,020 sampled videos in an earlier
census. It appears **nowhere in any `clippershq/*.py`** — verified independently. `_video_of`
does not read it. **A photo-mode post cannot be a video edit by definition**, so this is a
non-circular structural signal — it does not depend on the search term, the account name, or a
model's opinion — and nothing has ever looked at it.

`duration` fares similarly: extracted into the video record at `tiktok_finder.py:374-375` at
100% fill, and read back by nothing in the finder path. It arrives from the vendor and
dead-ends. (Other files mention `duration`, but those are the clip-editing subsystem's unrelated
`duration_s`.)

**Why the question could not be closed, stated rather than papered over:** **zero of the 321
edit-term-discovered TikTok pages have a retained raw vendor payload anywhere on disk** — only
their cover images survive. And every prior video-level measurement in this project was run on
meme-labelled pages: of one earlier round's 105 captured handles, 26 are still in the seen store
and **all 26 are hashtag-labelled, none edit-labelled**. So the `aweme_type` question *for edit
pages specifically* has never been measured by anyone, and a no-network round cannot fetch what
it needs to close it.

### 3.10 Safety state

Backup of 8 files (config, ledger, lead store, all five seen stores), every one sha256 MATCH,
path built from **one** round constant. Corruption control: one flipped bit → detected.
Seen-store bodies found **by shape**, not by key name — `clip_seen.json` is a **list at root**
(2,193 rows), `meme_pages_seen.json` a dict at `pages` (6,196), the ledger a **list** at `runs`
(22,635). A dict-only helper reads the list-shaped ones as zero.

---

## 4. WHAT WAS REFUSED, AND WHY

**One of the seven parts was not delivered, and two instruments within Part 1 were not run.** Six sub-agents were dispatched in parallel and
**all six were killed mid-flight by a session rate limit**; two were re-dispatched and their
results are in Section 8 if they returned. What is missing:

- **Part 1, instrument (a) — the judge on a fresh sheet with the edits brief. NOT RUN.** This
  would have been the only instrument to ask "is this an edit page" directly rather than
  inferring it from his grades or the funnel's verdicts. It requires spending; **$0.00 was
  spent this round**, so it is absent, not zero.
- **Part 1, instrument (c) — resemblance to his hand-supplied edit accounts. NOT RUN.**
- **Part 5 — whether edits needs a different picture. DELIVERED** (Section 3.8), on a
  re-dispatched agent, with its headline independently re-measured by me before it was believed.
  Its summary named one run; measuring three showed the figure is **corpus-dependent** (75.7%,
  54.0%, 0.0%), which the single-run summary did not carry.
- **Part 6 — the reserved question. DELIVERED** (Section 3.9), and its headline is a
  refutation. What it could not close is named there: the raw vendor payloads for edit-term
  pages do not exist on disk.
- **Part 7 — BEFORE and AFTER for both brains. NOT RUN.** This is the fourth consecutive
  attempt at the edits AFTER measurement that has not completed.

**The raw-search denominator — the one his claim is literally about — remains unmeasured.**
Everything in Section 3 is measured one or two filtering stages downstream of it. This is stated
plainly rather than papered over, because the temptation to present 96.8% as "his claim
confirmed" is exactly the denominator substitution this round was built to avoid.

I also **did not** add or loosen any judging rule, move any threshold, or change any production
file. `free_judge.py` was registered to this round and **lent to a concurrent round** (BL-1519,
which is shipping a free judge model) for a bounded window, with the handover recorded on the
pipe; I read it but did not edit it.

---

## 5. WHAT I GOT WRONG

- **I built the atomicity guard and then wrote the bug it guards against, in the same
  function.** `snapshot()` wrote its temp file with `io.open(...).write(...)`, leaving the
  handle open — relying on CPython refcounting to close it before `os.replace` renamed *that
  very file*. It works today. It is the same class of defect the function exists to survive,
  self-inflicted on the source instead of the destination. Caught by a `ResourceWarning` in the
  test output, not by reading. Fixed with `with`.
- **My first read of the walked pass rate (81.9%, interval excluding 95%) looked like a
  refutation of his claim, and I nearly reported it as one.** It was a denominator error inside
  a single word: `passed`. Splitting the rejection reasons reversed the reading entirely. Had I
  published the first number, I would have told him his claim was wrong on evidence that says
  the opposite.
- **My AST scan of `_process` showed no `return` between `judge_page` and `profile_of` and I
  briefly read that as "the funnel profiles rejected pages".** Reading the source showed
  BL-1516 had already gated it on `is_target`. The absence of a `return` is not the absence of
  a gate; I was pattern-matching on a shape instead of reading the code.
- **Six sub-agents dispatched at once, all lost to one rate limit.** Everything in this report
  I measured directly afterwards. The parallelism bought nothing and cost the round three parts.
- Two console crashes on `cp1252` for emitting `⚠️`, and one heredoc failure, both mine.

---

## 6. MONEY AND SAFETY

**Spend: $0.00.** No vendor call of any kind was made. Every number in Section 3 comes from
files already on disk. The cap was proven to bind *before* any of this, on both brains, as
Section 3.7 records — the proof was done first even though nothing was ultimately spent.

The ledger was read, never written; no ledger delta was used to attribute anything, because
`spend.json` is shared across concurrent rounds and gained rows from peers during this one.

Backups verified as in Section 3.8. No production file was modified. No process was killed. No
handle, address, key, port or absolute path appears in this report; every detector that asserts
so was proved on a planted control before the scan, and the file was asserted free of C0 control
bytes **before** writing.

---

## 7. WHAT HE SHOULD DO NEXT — RANKED, BY DOLLARS AND HOURS PER 1,000 DELIVERED

**1. Move edits supply from hashtags to search terms. Saves $0.28 per 1,000 and rejects less of
what he wants.** Already true in the data: edit-term supply converts at 81.9% versus 55.9% for
hashtags, and **0 of 11** of its recorded rejections are content rejections versus **10 of 50**.
This costs nothing to adopt — it is a term list, and `run_mode.py` already implements the
switch. *Measured.*

**2. Record a reason on every rejection. Costs nothing; unblocks everything below it.** Reasons
are recorded on **8.1%** of rows — 10 of 21 edit-term rejections and **823 of 875** hashtag
rejections say nothing at all. The entire content-versus-business finding rests on 11 rows and
50 rows because that is all there is. Every cost question below needs this. *Measured gap.*

**3. Measure the raw-search denominator with one bounded fresh run.** This is the only way to
test the claim he actually made. The term engine and its atomic ledger are built, tested and
committed; 178 terms across his 14 categories are ready to walk. At 6.3 calls/keyword this is
~$0.67 of discovery for the full sweep. *Not yet run.*

**4. Do not pursue "skip `videos_from_handle`" without measuring it first — the arithmetic is
seductive and the evidence is against it.** It is 75.7% of the edits brain's spend, and skipping
it is the only lever big enough to reach $0.50:

| Skip rate | Calls/page | $/1,000 |
|---:|---:|---:|
| 25% | 1.43 | $0.99 |
| 50% | 1.10 | $0.79 |
| 75% | 0.76 | $0.59 |
| 100% | 0.43 | **$0.39** |

But the call exists because `/v2/search` returns only ~10 of an account's own videos and the
evidence floor is 3. BL-1338 measured that the search-supplied count is **noise** — *"the same
query on the same account returned 2 videos at 18:00 and 8 at 21:16 the same day"* — and that
cutting on it threw away **69 of 363 pages**, of which re-fetching made 45 judgeable and 7 were
pages he wanted. **Gating on a noisy count re-creates a defect that has already been measured
and removed once.** The honest position: the lever is sized, its feasibility is unmeasured, and
$0.50 is **not reachable today**.

**5. Test whether the one-panel sheets are costing accuracy — before building anything on
it.** In the two most recent dated runs, **65.4% [56.9, 73.1] (87/133)** of pages reached the
judge with **one panel of twelve** on a mostly-blank canvas. A meme page can be recognised from
one still; an edit page is defined by motion and cut rhythm, which a single cover destroys. This
costs no money to investigate — the sheets are on disk and the judge verdicts are recorded — and
if panel count does predict judge error it is a bigger lever on his 75.8% accuracy ceiling than
anything in this list. **Stated as a hypothesis: I did not measure it.** *Unmeasured.*

**6. Extract `aweme_type` — TikTok's own video-vs-photo flag, 100% filled, never read.** It
appears nowhere in the codebase. A photo-mode post cannot be a video edit *by definition*, so
this is a structural, non-circular signal that costs nothing extra to collect — it is already in
payloads being paid for and thrown away. It has never been measured for edit pages because no
raw payload for an edit-term page was ever retained. *Unmeasured; free to start collecting.*

**7. Fix the cost estimator, or stop consulting it.** It is 6.3× low on discovery and ~30× high
on profiles, and the errors partially cancel. Its discovery line still states as fact a claim
refuted and fixed in the same file. *Measured.*

**On his target:** edits cost **$1.19 per 1,000** today, **2.4× his $0.50**. Items 1 and 2 do not
close that gap — item 1 improves quality at roughly constant cost. Only item 4 closes it, and
item 4 is currently blocked on a measurement nobody has taken. **He should be told $0.50 is not
reachable this week, and that $1.19 is already better than the meme brain's $1.47.**

---

## 8. WHERE THE FILES ARE

All committed to the working repo under `BL-1518`:

| Path | Contents |
|---|---|
| `scratch/bl1518_claim_harness.py` | Wilson intervals; the three-instrument spine with its refusals |
| `scratch/bl1518_instrument_b.py` | His grades by term · `bl1518_instrument_b.json` |
| `scratch/bl1518_instrument_a2.py` | Walked-supply rates · `bl1518_instrument_a2.json` |
| `scratch/bl1518_reason_split.py` | Content-vs-business classifier · `bl1518_reason_split.json` |
| `scratch/bl1518_cost.py` | Per-brain cost model · `bl1518_cost.json` |
| `scratch/bl1518_term_ledger.py` | 178 terms, 14 categories, append-only journal ledger |
| `scratch/bl1518_capproof.py` | Cap proof against the shipped bytecode of both brains |
| `scratch/bl1518_a6_reserved.json` | Pixel-feature AUCs before and after the batch control; the unextracted-field census |
| `scratch/bl1518_a5_picture.json` | Picture cost split, blank-panel census, crop/OCR/strip verification |
| `scratch/bl1518_safety.py` | Backups, corruption control, row-keys-by-shape baseline |
| `tests/test_bl1518_term_ledger.py` | 6 tests, all green, including the real held-file test |

**Reproducing the headline numbers** (no network, no spend, nothing written outside `scratch/`):

```
PYTHONIOENCODING=utf-8 python scratch/bl1518_instrument_a2.py    # the three denominators
PYTHONIOENCODING=utf-8 python scratch/bl1518_reason_split.py     # content vs business
PYTHONIOENCODING=utf-8 python scratch/bl1518_cost.py             # cost per 1,000, per brain
```

`PYTHONIOENCODING=utf-8` is required: the default console encoding here is `cp1252` and any
script emitting a warning glyph dies on it.
