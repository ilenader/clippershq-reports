# BL-1508 — The cost baseline: where every cent and every second goes

**Round:** BL-1508 · **Date:** 2026-09-05 · **Spend:** $0.18 across three live funnel runs,
counted by each run's own call counter at the wrapper — never a ledger delta, because
`spend.json` is shared with every live round and the Instagram client autoflushes under the
label `unattributed`.

> **Written as the project's cost baseline.** A session with no access to this machine should be
> able to read this and know where the money and the clock go. Every figure names its
> denominator, and the ones I could not measure are marked as such rather than estimated.

---

## What is actually stopping him

**The funnel is not expensive at finding, capturing or judging pages — measured end to end it
delivers a graded page for about 1.7x the target on both money and clock. What puts it 17x to
35x over is everything either side of that: it buys discovery for roughly 1,700 accounts for
every one it judges, and only about one delivered page in six to ten ever yields an email
address.** The single highest-value thing to do next is not another speed-up of the judge — that
is 13% of spend — it is to **stop buying discovery the funnel never processes, and to measure
the delivered→address conversion, which is the step nobody has ever costed.**

---

## 1. The breakdown nobody had built

Three live runs, metered from the outside by wrapping `IgClient._get`,
`LamaTokClient._get`, `free_judge._ask` and `page_capture.capture_one`. **No shipped code was
edited.** The endpoint path is the stage key, and the calling frame from the live stack
corroborates it — on Instagram the two tables map **1:1**, which is the control.

### Instagram memes — one run, 315.3 s wall, $0.0429

| stage / endpoint | calls | USD | % vendor $ | work s |
|---|---:|---:|---:|---:|
| **DISCOVERY** `/v2/hashtag/medias/clips` | 22 | 0.0152 | 40.7% | 91.8 |
| PROFILE `/v2/user/by/username` | 9 | 0.0062 | 16.7% | 13.7 |
| POSTS `/gql/user/medias` | 9 | 0.0062 | 16.7% | 25.6 |
| **DISCOVERY** `/v2/search/reels` | 7 | 0.0048 | 13.0% | 26.1 |
| **DISCOVERY** `/v2/fbsearch/accounts` | 5 | 0.0035 | 9.3% | 7.3 |
| **DISCOVERY** `/v2/user/suggested/profiles` | 2 | 0.0014 | 3.7% | 4.0 |
| **TOTAL** | **54** | **0.0373** | | **168.5** |

**Discovery is 36 of 54 calls — 66.7% of vendor spend.**

### TikTok memes — two runs, 482.5 s wall, $0.136

| stage / endpoint | calls | USD | % vendor $ | work s |
|---|---:|---:|---:|---:|
| **DISCOVERY** `/v2/search` | 73 | 0.0438 | 69.5% | 189.7 |
| PROFILE `/v1/user/by/username` | 14 | 0.0084 | 13.3% | 37.3 |
| DISCOVERY `/v1/hashtag/medias` | 9 | 0.0054 | 8.6% | 29.9 |
| DISCOVERY `/v1/hashtag/info` | 9 | 0.0054 | 8.6% | 19.6 |
| **TOTAL** (one run) | **105** | **0.0630** | | **276.6** |

**Discovery is 69.5% of vendor spend on TikTok too.** Two platforms, two vendors, same shape.

### Where the clock goes, which is a different answer from the money

| | work seconds | share of work | share of spend |
|---|---:|---:|---:|
| vision judge | 1,117.7 | **79%** | **13%** |
| vendor requests | 168.5 | 12% | 87% |
| capture (free) | 134.1 | 9% | 0% |
| **sum of stage work** | **1,420.3** | | |
| **actual wall** | **315.3** | | |

**The judge is 13% of the spend and 79% of the work — and it is already parallelised.** 32 lanes
turned 1,420 s of work into 315 s of wall, 4.5x. It does not dominate the clock because somebody
already fixed that. Capture is 2.19 s median per page on the free route.

### The two ratios the round asked for

Measured on the funnel's own checkpoint journal — 51,151 rows, 81 runs, cross-checked two ways
that agree within 6% (25.4 h vs 27.0 h):

- **85.7% of clock is spent on pages that are later rejected.** A rejected page is 16.3x cheaper
  in clock than a kept one (1.55 s vs 25.26 s mean) — but there are **98x more of them**.
- **Share of spend on later-rejected pages cannot be measured from the ledger**, and §7 says why.
  From the runs above it is bounded: discovery (67–70%) is spent before any page is judged, so
  **at least two thirds of vendor spend is committed before rejection is even possible.**

---

## 2. Every denominator, named separately

Seven different numbers, from the Instagram walk corpus (14,280 distinct handles):

| # | denominator | count |
|---|---|---:|
| 1 | walked | 14,280 |
| 2 | entered the free judge | 2,135 |
| 3 | got a picture-judge call | 1,600 |
| 4 | reached the caption rules | 3,352 |
| 5 | **passed the filter / delivered** | **427** |
| 6 | **carries an email** | **75** |
| 7 | marked UNJUDGED — never a rejection | **9,408** |

**65.9% of walked pages are UNJUDGED**: walked, paid for in clock, and never reaching a verdict.
And **delivered (427) and with-an-address (75) differ by 5.7x**, so the same walk is
**63.1 h per 1,000 delivered** or **360 h per 1,000 addresses**. Quoting one and labelling it the
other is how $137.31 and $78.53 were each manufactured.

On the live Instagram run the chain was starker still: **discovered 15,915 → captured 50 →
judged 9 → passed 2 → addresses 0.** 14,299 pages sat in the checkpoint the run did not carry.

---

## 3. Cost and clock per 1,000, measured directly

Never composed from a carry rate; each figure is total ÷ that denominator, from the same run.

**TikTok memes, two runs pooled** (40 sheets, 4 addresses):

| per 1,000 … | $ | hours | x $2.00 | x 2.0 h |
|---|---:|---:|---:|---:|
| authors discovered | 0.08 | 0.08 | 0.04x | 0.04x |
| profiles bought | 3.89 | 3.83 | 1.9x | 1.9x |
| passed the filter | 4.54 | 4.47 | 2.3x | 2.2x |
| **sheets delivered** | **3.40** | **3.35** | **1.7x** | **1.7x** |
| **with an address** | **34.02** | **33.51** | **17.0x** | **16.8x** |

**Instagram memes, one run:** $21.45 and 43.8 h per 1,000 delivered (n=2 delivered — a count,
not a rate). **Per 1,000 addresses: undefined. Zero addresses were produced, and that is not
free — $0.0429 was spent.**

**The delivered→address step multiplies cost by 10x.** Two independent estimates of that
conversion agree: **10.0% [4.0, 23.1]** from my runs (4 of 40 sheets) and **17.6% [14.2, 21.5]**
from the walk corpus (75 of 427 delivered). Roughly **one delivered page in six to ten**.

---

## 4. The source mix, re-derived and costed

Re-derived on the corrected corpus. **The walk column reproduces almost exactly**; two things
about the old table did not survive.

| source | walked | share | delivered | delivered/walked | walked/delivered |
|---|---:|---:|---:|---:|---:|
| seed | 11,755 | 82.32% | 194 | 1.650% | 60.6 |
| hashtag | 1,650 | 11.55% | 144 | 8.727% | 11.5 |
| reels | 478 | 3.35% | 67 | 14.017% | 7.1 |
| search | 397 | 2.78% | 22 | 5.542% | 18.0 |

⚠️ **The old table's approval column had an undisclosed restriction.** It was not "pages he
graded from this source" — it was **pages he graded that the funnel had DELIVERED**. That
restriction reproduces its published hashtag `8/24` and search `14/18` exactly. Same population
today: seed 37.0%, hashtag 33.3%, reels 82.4%, search 77.8% (n=130).

⚠️ **And the old table is Instagram-only, which it never said.** TikTok writes no per-handle
checkpoint. TikTok's own walk is hashtag 83.40% (52.84% delivered) and search 16.60% (75.12%
delivered), with **zero seed and zero reels** — positive control: the same classifier returns
2,562 seed and 274 reels on other stores, so that zero is the funnel, not the instrument.

⚠️ **Reels' approval ranges 66.7%–82.9% across 56 readings.** The biggest single swing is the two
label-reversed `bl1427` sheets. Reels and seed intervals stay disjoint in every reading.

### The switch, and what it buys

`meme_finder.seed_accounts_file` — set it to `""`. The read is `if seed_file:`, so an empty
string skips the block entirely; **no code change is needed and there is no
zero-means-unlimited hazard.** Driven: 15,323 seed handles with it set, **0** with it empty,
against a positive control that the ON case is non-zero.

| | walked per delivered | h per 1,000 delivered |
|---|---:|---:|
| today | 33.4 | 63.1 |
| seed off | **10.8** | **20.5** |

**3.1x better — and still 10x over the 2-hour target.** It also removes 82.3% of supply: the
other three sources have produced 2,525 accounts in the entire corpus and would need ~8.3x that
to replace seed's delivered volume. Reels has never produced a single TikTok account, and search
saturates at page 2 while still reporting `has_more: true`. **Depth is not the lever; breadth is.
This does not close the gap and must not be sold as if it does.**

---

## 5. The largest line of spend, and the largest consumer of clock

**Largest spend: DISCOVERY — 66.7% (Instagram) and 69.5% (TikTok) of vendor dollars.** Removing
it entirely is impossible; the funnel cannot judge a page it has not found. But it is being
**over-bought by orders of magnitude**: one run discovered 15,915 accounts and judged 9. Those
accounts are banked in the checkpoint rather than thrown away, so this is inventory, not pure
waste — but it is money spent now for value that 14,299 uncarried pages say is not being
consumed. **Sizing discovery to throughput is the largest single saving available, and it needs
no new capability.**

**Largest clock: the vision judge — 79% of stage work.** It is **already parallelised**: 32 lanes,
38.1 pages/min, 1,420 s of work in 315 s of wall. Further gains there are bounded by that 4.5x
already being taken.

**Second-largest clock, and the one that is pure waste: capture.** 18.0% of captures return
**zero tiles**, costing 2.55 h — **23.8% of all capture clock** — for no picture at all.

⚠️ **The Instagram clock may be physically bounded.** The wall is a per-IP *rate*: paced 28/28
succeed, back-to-back 5/76, lifting at 300 s idle, and it is one browser per lane on one IP, so
**more lanes makes it worse**. The 2-hour target needs 7.2 s per delivered address end to end.
That is not a code problem.

---

## 6. Worked backwards from $2.00 and 2 hours

The target decodes cleanly from the baseline table: 19.52 ÷ 9.8 = 1.99 and 8.21 ÷ 4.1 = 2.00,
so it is **$2.00 and 2 hours per 1,000 delivered**. Per address that is **$0.002 and 7.2 s**.

$0.002 buys **2.90 HikerAPI calls** (at $0.00069064), or 3.33 LamaTok calls, or 22.5 vision calls.

**The floor: one vendor call per walked page and nothing else.**

| walked per delivered | $ / 1,000 delivered | x $2.00 |
|---:|---:|---:|
| 60.6 (today, seed) | 41.85 | 20.9x |
| 20.7 (source lever, best case) | 14.30 | 7.1x |
| 10.0 | 6.91 | 3.5x |
| 5.0 | 3.45 | 1.7x |
| **2.9** | **2.00** | **1.0x** |

**At 2.9 walked pages per delivered — a 21x improvement on today — a single call per page exactly
exhausts the entire budget, with nothing left for capture, judging, the profile or the contacts.**
And a keeper needs at least a profile call and a contact call of its own: at 2 paid calls on the
keeper, **$0.000619 remains — 0.90 paid calls to be shared across every rejected page.** At 3, the
budget is already gone.

### Is the target reachable on this architecture?

**Not as the funnel is shaped today, and the arithmetic says so rather than my judgement.**

- **$2.00 per 1,000 delivered requires ~98.5% of walked pages to cost nothing at all.** Today
  discovery alone — spent before any page is judged — is two thirds of the bill.
- **2 hours per 1,000 delivered is 7.2 s per address.** Instagram's per-IP rate limit needs
  *pacing*, and adding lanes makes it worse. The measured floor is not code-bound.
- **The best single lever measured (source mix) is 3.1x**, against a gap of 17x–133x depending
  on the denominator, and it caps throughput while it does it.

**What would have to change:** the delivered→address conversion, which nobody has ever costed and
which multiplies everything by 10x; and discovery sized to throughput instead of to supply. Both
are measurable next steps. Neither is a speed-up of the judge, which is 13% of the money.

⚠️ **And the honest comparison.** Another route produces addresses at ~$1.21 per 1,000 against the
page funnel's tens of dollars. **They do not find the same people** — one finds musicians, the
other finds the clippers who do the work. Comparing them on cost per address is a category error.
What each *delivers* is the question, and that is his to answer, not mine.

---

## 7. Why no one could build this before

**Spend rows carry no `run_id`, no `stage` and no `funnel` — 0 of 26,922**, against a control
showing `label` present on 26,903 and non-zero `dollars` on 26,916 of those same rows. `label`
names a *module*, so `meme_finder` is a single $13.19 bucket covering discovery, capture, the
profile purchase and the contact fetch together. That is the whole reason every figure in this
project is a total.

**The five stage counters are null on all 74 records that declare them** — and it is **ten** blind
fields, not five. Control passed: `started_epoch`, `pid`, `target`, `cap_usd` are non-null and
non-zero on those same 74. The writer is *younger than the data* (2026-09-02/03); all 17 records
that postdate it are `status=running` with `ticks=0`, so neither setter has ever run.

**Smallest set of insertion points**, in order of value:

1. **Add `run_id` and `stage` to the row dict in `main.py:791` (and `:699`).** GENERAL — buys
   dollars *and* calls per stage for every booker at once. Patch the **locked** implementation,
   not the wrapper.
2. **Refuse to arm the Instagram autoflush without a stage label** (`ig_client.py:415`). GENERAL —
   closes the `unattributed` bucket at the point the value enters. That bucket is **328 rows,
   $2.4480, 3.96% of lifetime spend**; with unlabelled rows, **$4.22 (6.8%) is unattributable**.
3. Increment `profiles_bought` at the Instagram purchase site. LOCAL but irreplaceable — the
   Instagram profile purchase is **blind by construction**; no key exists in any form.
4. Stop `meme_finder.py:8291` overwriting `_provenance.json`. GENERAL and cheapest: the counters
   are already correct and the sink destroys them.

---

## 8. Defects found on the way, and corrections to my own work

### Found

- ⚠️ **The Instagram ledger was booked at the wrong vendor's price.** 86.3% of solo Instagram
  rows — **52,918 calls** — are booked at LamaTok's $0.00060000 instead of HikerAPI's
  $0.00069064. **Under-count $4.80: 13.1% low on those rows, 7.8% of the declared lifetime
  total.** It stopped on 2026-08-28 and every September row is correct, so the fix holds — but
  **every historical $/1,000 figure in this project is ~8% low.** Independently reproduced: an
  earlier round reported 53,313 calls / $4.83; this re-derivation gives 52,918 / $4.80.
- ⚠️ **The crash handler destroys the crash.** `control.py:89` prints at the console's default
  encoding, so **159 of 1,699 emit/print sites (9.4%) raise `UnicodeEncodeError` on a plain
  Windows console**. `meme_finder.py:7970` emits `⚠️ THE WALK CRASHED: %s` — so when my first
  Instagram run aborted, the handler itself crashed and **the message naming the cause was never
  printed**. The suite never sees this because `tests/run_all.py` sets `PYTHONUTF8=1`.
- ⚠️ **78 run records claim `status=running` with `ticks=0`, and every PID checked is dead** —
  including one 8.8 minutes old. The `dashboard/.running.json` defect at scale.
- **`OCR_SECONDS_PER_PAGE = 32.9` still ships and is pinned** by `tests/test_bl1333_speed.py:225`.
  BL-1504 measured the real figure and wrote it into the *comment beside the constant*, not the
  constant. The operator-facing line at `:3903` still prints the old number. See below — my first
  statement of the size of this error was itself wrong.

### Verified so nobody re-pulls a pulled lever

- **"Profile purchase waste is zero"** — arithmetic reproduces exactly (1,258/1,258/0, n=2,447),
  but `profile_bought: False` is a **hardcoded literal on four early-return paths**, so the
  off-diagonal cell is unreachable by construction. **The control is a structural identity, not a
  measurement.**
- **"The slow model was two models fused"** — confirmed, nemotron is never asked (control passed:
  `FREE_TRIES=99` makes it appear). But the production cutter is **nex-n2-mini at 91.4%**, not glm
  at 88.1%, and it made all 108 drops on the 200-page run. "Two calls per row" explains ~2.1x of
  the 5.6x; the rest is a **selection effect**, not a denominator.
- **"A 45 s time-box costs zero cuts"** — confirmed (157 cuts, max 43.84 s), but **40 s already
  costs 3 cuts, so the margin is 1.16 s**, and the shipped code records **no per-call latency at
  all**.
- **"Decoding buys nothing"** — **already pulled** (`ocr_ran` true 0 times across 5,835 files).
  But **"ONE consuming rule" is refuted**: the decode also feeds `template_overlay`, a
  speech-*independent* rule, so the guard's own docstring is stale.
- **"3.70x, zero production importers"** — the two halves name **different modules**. There are
  **three** extractors; the 3.70x measured `frame_text.extract_frames`, which has **5 production
  importers**. Re-measured independently: 3.58x / 4.74x median, 166 of 168 frames pixel-identical.

### Corrections to my own work this round

- **I said the mark corpus had grown to 15 files / 819 rows / 620 pages. It has not** — it is
  **12 / 683 / 535, unchanged**. My filter was `endswith("marks.jsonl")`, which also matched three
  differently-named files (+136 rows). The trap: there really *are* 15 files named `marks.jsonl`
  (three zero bytes, leaving 12), so **both the right and wrong sets total 15**. A count check
  alone would never have caught it.
- **I said the OCR constant overstates by 7.2x. It is ~2.6x.** `32.9` is decode **+ OCR**;
  BL-1504's `4.59` is decode **only**. I compared them directly — **the same unit mistake the
  comment I was criticising had made.** Measured like for like: decode-only 3.09 s, decode+OCR
  10.86–14.59 s, so 32.9 ÷ ~12.7 = 2.6x.
- **My meter reported 0 vendor calls on the first TikTok run while the funnel's own counter
  reported 115 billed.** TikTok bills through `LamaTokClient`, not `IgClient`. A zero whose
  control failed is not a measurement; the meter was fixed and the second run agreed with the
  funnel's counter exactly.
- **My meter lost two paid runs' artefacts to a formatting bug** in the code that *displays* the
  results — it keyed the seconds column off the heading text. Now indexed by row shape, and the
  artefact is written **before** anything is printed.

### Controls and test state

The meter is a **pass-through**: driven, the inner function is called exactly once and the return
value is unchanged. **All four brief hashes are identical before, during and after metering** and
equal the values BL-1503 pinned — no verdict moved. The cap was proven to bind **before the first
page**: explicit zero refuses, absent key refuses, declared lifetime ceiling of zero refuses,
malformed fails closed, and a positive control returns 2.0.

**Seen stores verified by row key sets, with the body found BY SHAPE, not by key name** — the
spotify store reads **1,902 rows**, the value a name-based helper once reported as 3.

**I did not run the full suite:** peer rounds were active in the tree throughout. The families I
touched are unchanged — this round edited **no shipped code at all**, which is the strongest
statement available about verdict movement.

---

*Every number here can be re-run from `scratch/bl1508_*`: the stage meter, the two funnel
drivers, the checkpoint, and the three sub-agent censuses.*
