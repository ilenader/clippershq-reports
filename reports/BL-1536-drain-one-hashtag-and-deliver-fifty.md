# BL-1536 — one hashtag, fifty pages, and a stop that actually stops

**Measured 2026-09-09 against production, from `checkpoint/session-2026-07-23-full-day` at
`fb851902`. TikTok edits only — no Instagram, no memes.**
Spend cap $2.00. **Actual spend $0.1188**, counted by each run's own wrapper counter.

---

## THE PARAGRAPH AT THE TOP

**50 pages are in front of him.** They came from **ONE hashtag — `#ufcedit`** — which is
exactly what he asked to find out, and the answer to "should fifty come from one hashtag" is
**yes, on this tag, with room to spare**: the tag holds **138 distinct accounts** and the run
used 55 of them to deliver 50. It cost **$0.0846 for the delivery run** ($0.1188 including
the drain measurement and the picture scoring), **141 billed vendor requests**, and **66
minutes**. The sheet is at
`output\bl1536_sheet\` — **double-click `OPEN_BL1536_SHEET.bat`**. No port to remember; it
picks a free one and opens the browser itself.

⚠️ **"50 delivered" is not "50 he wants", and this report never pretends otherwise.** The
funnel cannot know his score in advance. 50 is the count of pages the model approved. **The
keep rate is what HIS GRADING answers**, and the sheet exists to collect it. His own marks
agree with themselves 75.6% (89.2% on obvious pages, **48.0% [30.0, 66.5] near his decision
line** — an interval spanning 50%), which bounds any *agreement* figure computed later; it
does **not** bound the one-sided keep rate this round produces.

---

## 1. THE FOUR FIXES FROM LAST ROUND

### 1.1 A run-level abort that cannot be swallowed — **and BL-1534 blamed the wrong thing**

BL-1534 asked for 5 pages and ran 16. **Its report said `discover` catches `_CapReached` per
page and continues. That is not what happened, and I published it.** The per-page handler
calls `stop.set()` and the serial walk breaks correctly. The real culprit is `_tick`:

```python
try:
    on_progress(result)
except Exception as exc:            # <-- BL-1534's stop landed HERE
    emit("  WARNING: progress checkpoint failed: ...")
```

`_CapReached` is an `Exception`, so the stop became **a warning that was printed and not
read** — the same "the log said so and nobody read it" shape this project keeps hitting.

**The fix is two parts, and both are driven:**

- **`_RunAbort(BaseException)`** — deliberately *not* an `Exception`, so no `except
  Exception` in the walk can catch it. `_tick` now re-raises it and swallows everything else,
  so a broken checkpoint still cannot kill a funded run. `_CapReached` was **not** rebased:
  `test_bl1516` asserts `issubclass(exc, Exception)` and the BL-1423 recovery depends on it.
- **`stop_after_delivered` / `stop_after_pages`** — cooperative, checked under the lock where
  the verdict is known. This is the mechanism the 50-page run uses.

**DRIVEN, as instructed: asked for 3, got exactly 3.**
`#ufcedit delivered 3 (running total 3 of 3); stopped: reached the delivered target: 3 of 3`

⚠️ **AND THE STOP WAS LIVE AT ONE OF TWO DISPATCH PATHS.** The `lanes == 1` loop tests
`stop.is_set()` per page; the pooled path is `ex.map(...)` over the whole author list, which
**dispatches every author before any of them can set the flag**. A run-level stop therefore
worked serially and did nothing at `lanes > 1`. Guarding at the top of the worker covers both
with one line. **FIX CATEGORY: GENERAL — one guard, two dispatch paths, any lane count.**

### 1.2 The post floor cannot reject anything — said out loud, **not raised**

At `MIN_TOTAL_POSTS = 1` the only input that trips `posts_below_floor` is a page reporting 0
posts *and* supplying no videos — and that page is `thin`, so it returns **UNJUDGED**, not a
`posts_floor` rejection. BL-1528's zero-refutation correctly discards a 0 that the payload's
own video list contradicts.

**Confirmed live: across 55 walked pages, `posts_floor` fired ZERO times. The only rule that
cut anything was `stale` (recency), 5 times.** So the "two automatic rejections" are, in
practice, **one**. **His floor was not touched** — he lowered it deliberately, and it is his
call. It is now stated in the report *and* visible on the sheet, because a rule the operator
believes is protecting him and which cannot fire is worse than no rule.

### 1.3 The hand rules — **decided, and the obvious revival would have been wrong**

`free_judge.his_rules_say` reads `views`, `video_count` and `posted_at_least_days`.
`facts_for_author` computes all three. `his_rules_for_author` joins them — and **has zero
production callers** (AST, not grep). `facts_for_author`'s only caller *is* that dead
function. So his "really important" rule has never run on any page.

⚠️ **`his_rules_say` returns `"BAD"`. It REJECTS.** Wiring it in would have created **three
new automatic rejections** — the exact opposite of what BL-1534 landed at his instruction.
So the three fields are revived as **facts the model weighs**, and `his_rules_say` stays
uncalled. `facts_block` now renders them, with the honest wording for the one that is a floor:

> `it posted at least as recently as 3.5 days ago (a FLOOR from the tag-matched post, not the
> account's newest — it understates recency)`

Measured on 18 authors, that field coincided with the account's true newest post on **2 of
18**, median understatement **9.1 days**, worst case **222**. Printing it as "last posted N
days ago" would be a false statement about the page.

**SHIPPED OFF BY DEFAULT** (`hand_rule_facts=False`) — adding fields to the prompt is a
judging change and this round scored the picture, not this. A committed test fails if the
switch disappears or flips, so a fourth round cannot rediscover the same fiction.

### 1.4 The three picture defects — **verified, not re-fixed**

| Defect | State |
|---|---|
| `or ""` collapse of an undecodable video | **FIXED** — the OCR path uses `_drawn_line_of`; failures append `None` (a REFUSAL) |
| `play_url_of` ranks watermarked `download_addr` | **FIXED** — `download_addr` is last (offset 321 vs `play_addr` 267) |
| `HERO_T_DEFAULT` is read | **FIXED** — `frame_times(5.0,"scaled:6") = [1.7, 2.3, …]`, first sample 1.7 s |

⚠️ **My first check on defect 1 produced a FALSE POSITIVE.** A crude `or ""` string search hit
three lines; reading them showed all three are URL fallbacks and an id default, not the OCR
collapse. Caught before it reached this report.

---

## 2. DRAINING ONE HASHTAG — HIS ACTUAL INSTRUCTION

**`#ufcedit`, walked to exhaustion. Measured PER PAGE, BY ACCOUNT ID, never by a count.**

| page | items | accounts | net-new (walk) | net-new (disk) | note |
|---:|---:|---:|---:|---:|---|
| 0 | 29 | 24 | **24** | 17 | |
| 1 | 29 | 27 | **24** | 24 | |
| 2 | 30 | 28 | **25** | 23 | |
| 3 | 30 | 29 | **22** | 24 | |
| 4 | 30 | 30 | **21** | 23 | |
| 5 | 25 | 24 | **19** | 21 | |
| 6 | 4 | 4 | **3** | 3 | supply running out |
| 7 | 0 | 0 | **0** | 0 | **empty — exhausted** |

**138 distinct accounts. 9 billed requests. $0.0054.**

**THE ANSWER TO HIS QUESTION: the tag saturates at page 7, and it does not taper — it runs
out.** Net-new held between 19 and 25 per page for six straight pages and then fell off a
cliff (3, then 0). There is no long tail of diminishing returns to mine; the supply simply
ends. **Nothing was byte-identical to a previous page**, and net-new was computed from the
IDs themselves, so a bogus cursor returning a fresh cache key could not have inflated it.

**Stopped on SATURATION, never on `has_more`** — one surface once reported `has_more: true`
on 7 of 7 pages while pages 3 and 4 came back byte-identical to page 2.

**138 is not 200–300.** His hand-count expectation is roughly **2× what this endpoint yields
for this tag**. It *is* about 2× the 70 previously measured for `ufc`, so the suffix form and
deeper paging did help — but one tag on `/v1/hashtag/medias` tops out near 140 accounts.

### The paging census — both instruments, and which answered

| Question | Instrument | Answer |
|---|---|---|
| Where does hashtag paging happen? | **AST** | `hashtag_medias` defined once, called at 2 sites; `_hashtag_medias` at 2 |
| Does the endpoint page? | direct read | `cursor` only — **no `page_id`** on this endpoint; `count` default **30** |
| Is `term_engine` running? | **AST imports** | **ZERO module importers.** The drain was done DIRECTLY, not through it |
| `search_terms` hits | **grep** | 58 here, **every one the config key** — the module-name trap |

**Never more than 30 per call** — `HASHTAG_PAGE_COUNT = 30`, and 40/50/100 have never been
granted (HTTP 400 on hashtags, 422 naming the limit on search). **Paging is the lever.**

⚠️ **`meme_finder.py:3305` is `accounts_from_search_reels` — REELS / fbsearch, i.e.
INSTAGRAM.** The suspected "second identical hole" is real and unpaged, but it is out of this
round's TikTok-only scope. Named, not touched.

**Hashtags used: 1.** `#ufcedit` alone reached 50 delivered; `movieedit`, `animeedit`,
`footballedit`, `caredit`, `gymedit`, `nbaedit` and `f1edit` were never opened.

---

## 3. THE RUN — 50 DELIVERED

`mode: edits`, resolved and driven: `run_mode.resolve('edits') -> ('edits','config')`.
Hashtags only, `searches=()`. Entry point asserted **not** under `tests/`; client asserted a
live `LamaTokClient`. **Every page fsynced before the next one started.**

| | |
|---|---|
| pages walked (rows that reached a verdict) | **55** |
| **DELIVERED** (`is_target` — the **`passing`** counter, **never `leads`**) | **50** |
| rejected | 5 |
| unjudged | 0 |
| delivery rate | **90.9% [80.4, 96.1]**, denominator 55 |

**I used `passing`, not `leads`.** `leads` is delivered AND has an email AND is new to master
— three conditions — and reading it as "delivered" once overstated a brain's price by 5.00×.

### Cost and clock

| Measure | Value |
|---|---|
| billed vendor requests | **141** |
| spend | **$0.0846** |
| pages walked per delivered | **1.10** |
| paid calls per delivered | **2.82** |
| **$ per 1,000 delivered** | **$1.69** |
| seconds per page — **MEDIAN** | **53.7 s** |
| seconds per page — **p90 / p99 / max** | **168.5 / 279.9 / 279.9 s** |
| wall clock | 66.0 min → 79.2 s per delivered |

The mean (72.0 s) is given only beside the median, never instead of it: the tail is **3.1×**
the median and that is where the run's time actually goes.

### What fired, and what did not

- **Rules that cut: `stale` only, 5 times.** `posts_floor` 0. Everything else annotates.
- **Annotated rules spoke on 2 of 55 (3.6% [1.0, 12.3])** — both `not_english`, **both
  delivered TARGET**. Under the old code both would have been rejected outright.
- **The model's own sentence: 46 of 55 = 83.6% [71.7, 91.1].**
- **Rejections carrying the model's sentence: 0 of 5 [0.0, 43.4]** — and that is **correct,
  not a defect**: all 5 were recency cuts, which happen *before* any model call. There is no
  model sentence to carry because no model was asked. Stated rather than left to look like a
  regression.
- **No account was seen twice.** Every row is a distinct account.
- **OCR honesty held**: `ocr_measured` False on all 50 judged rows, `has_on_screen_text`
  `None` on all 55. The sheet says **NOT MEASURED**, never "no on-screen text".

### The watcher

A cheap-model watcher read the log as it grew, checking five anomaly classes over 18 rows: a
paid call on a page that then died · time spent on a page that produced nothing · a model
sentence contradicting the page's own facts · the same account twice · a rule firing on an
absent field. **All five: none.** It also reported the run had "halted" at 18 — **it had not**;
that was the watcher's own 25-minute window expiring. I verified before repeating it.

---

## 4. A DEFECT THE ROUND FOUND: 7 OF 50 PICTURES WERE CROPPED

Every contact sheet is built **465×992**. Most are encoded by `grid_b64` and arrive
**356×760** — a *proportional downscale*, no content lost. But **7 of 50** went through
`tile_b64` (their recorded `sheet_tiles` was ≤ 1), which crops height to `465 × 16/9 = 827`
before resizing, and arrive **427×760**:

> **the bottom 165 px of the sheet — 16.6% of its height, 29.6% of its area — never reached
> the model. And 2 of those 7 pages were REJECTED on that partial evidence.** On TikTok a
> rejection is final, so a wrong one compounds forever.

⚠️ **I nearly reported this as a 58.7% loss on every row.** My first size metric was an
area ratio, which cannot tell a downscale from a crop. The discriminator is the **aspect
ratio**: a resize preserves w/h (0.766 / 0.766), a crop does not (0.918 / 0.766). Only after
adding that did the real defect separate from the 43 harmless resizes.

**Two instruments, two counts, both named rather than averaged:** the sheet builder
re-derived the encoding for its 50 chosen rows and found **7 cropped**; the live run's own
prompt-evidence capture recorded **5** `single_video=True` deliveries across its 50 judge
calls. The two cover slightly different row subsets (the builder took 50 of 55 rows,
interleaved). Both are reported.

**NOT FIXED THIS ROUND, deliberately.** Changing the encoder now would alter judging after
the fact on pages already judged, and I could not re-score them. It is the top item for the
next round, and the crop is **visible to him on the affected cards** ("427×760 — CROPPED --
content was removed").

---

## 5. THE HERO PICTURE, SCORED PAIRED — AND IT DID NOT WIN

Same pages, same brief, same exemplars, same facts, **only the picture changing**, both arms
judged in the same process.

| | cover sheet | hero |
|---|---|---|
| GOOD / MAYBE / **BAD** | 4 / 8 / **0** | 5 / 7 / **0** |
| rejects | 0.0% [0.0, 24.3] | 0.0% [0.0, 24.3] |
| seconds — **median** | 29.36 | **22.72** |
| seconds — **p90** | **49.10** | 76.60 |
| **delivered, from the request body** | 356×760 — whole image, downscaled | **654×760 — 100.0%** |

**Denominator: 12 pairs, both arms judged, 0 dropped.** The two pictures **agree on 9 of 12 =
75.0% [46.8, 91.1]**. Three moved: `GOOD→MAYBE`, `MAYBE→GOOD`, `MAYBE→GOOD` — net +1 GOOD for
the hero.

**VERDICT: INCONCLUSIVE. IT STAYS OFF.** Neither arm rejected a single page, so the
kills-of-wanted-pages comparison the brief asked for **has no signal to measure** — both
upper bounds are 24.3% and they are identical. n=12 cannot separate them. The hero is
*faster at the median* and *slower at the tail*, and it demonstrably delivers 100% of a
purpose-built picture against a downscale of a cover sheet. None of that is a win on his
marks, and **it did not win, so it is not turned on.**

⚠️ **His "one big, three small" is still refused by default and the refusal is still
correct**: `hero_geometry(3)` puts each small at **139 px** against a **155 px** judge floor;
`n_small=2` gives **208 px**. A tile nobody can read is not evidence.

**Nothing in the hero path took a page away**: a hero that will not build is UNJUDGED for that
arm and the pair is dropped, never scored as a rejection.

---

## 6. THE SHEET

**50 rows, interleaved, accepts and rejects, KEEP / MAYBE / DROP.** Opened in a real browser
from the `.bat`, round trip proved, test mark deleted.

Every row carries: **the exact image the model saw with its delivered pixel size** · the
model's verdict and confidence · **the model's own sentence in plain words** · **the number
against its threshold** · every note the free rules wrote · the tag it came from ·
**mode/platform/lane stamped at write time** · the email and its source · and **UNJUDGED as a
visible third state, never rendered as REJECTED**.

A real rejected card reads:

> **#32 REJECTED by the funnel** · model: – · #ufcedit
> the model returned no sentence for this page
> **newest post is 634 days old by the wall clock, past the 180-day cut — this cut cost 6 of
> his 37 wanted pages on BL-1298**

**The builder REFUSES a row without an image from THIS RUN, of THAT page — a hard refusal,
never a fallback.** Three conditions, all required: the file exists, it sits under this run's
sheet directory, and its mtime is at or after the run's start. A builder once fell back to an
unfiltered image search and served him pictures 12–13 days old from other rounds, **including
an Instagram login form he scored 10**. On this build: **55 of 55 rows passed, 0 refused.**

**Round trip, proved from the browser:** clicked KEEP on row 1 → `marks.jsonl` on disk carried
`{"call":"KEEP","row":1,…,"mode":"edits","platform":"tiktok","lane":"hashtag"}` → reloaded →
header read *"graded 1 of 3 · keep 1"* and *"1 mark(s) already on disk"*. **Then the test mark
was deleted** — a probe row once landed in his ground truth. Console: **clean, zero messages.**

**Mechanics, all of them:** rows **inline** (the browser refuses `fetch` on local files by
scheme) · pictures copied in and referenced relatively · **`ThreadingHTTPServer`** (a
single-threaded server once queued the browser's parallel connections and hung ten seconds
while an HTTP test reported it working) · **every path quoted in the `.bat`** · marks
**fsynced before the response says `ok`**, so the receipt cannot claim a save that is not on
disk · a **blocking red banner** at load if the marks file cannot be read · a **CLEAR button
per card** · **zero C0 control bytes asserted before writing** · both scripts syntax-checked
(`node --check`, `py_compile`).

**Mode survives resolution**: the server merges a later mark forward, so a mode-less row can
never erase a stamped one. 2,323 raw rows once carried a mode and **zero** pages resolved with
one, under last-keystroke-wins.

### Accessibility

An accessibility review measured the key map on two engines. Applied: the grade control is a
native `fieldset`/`legend` **radio group** (exclusive choice, native keyboard semantics, no
ARIA faking what HTML already does); the receipt is `role="status"` (polite) and the failure
banner `role="alert"` (assertive, takes focus); UNJUDGED vs REJECTED is distinguished **by
text, never colour alone**; K/M/D shortcuts **now gate on `!ctrlKey && !metaKey && !altKey`**
— without it **Ctrl+D graded the card *and* bookmarked the page**, a real bug the review
caught. Space, PageUp/PageDown, Home/End and the wheel are deliberately left unbound: measured
alive on both engines, and Space is his page-down.

**Not done, and named:** a screen-reader operator in browse mode would lose K/M/D, because
single letters are NVDA quick-nav commands and a card shell does not force focus mode. Fixing
that means making the card a real widget (`role="radiogroup"` with `aria-activedescendant`).
That is a redesign, not a tweak, and the right trigger is the tool gaining a non-sighted user.

---

## 7. WHAT YOU GOT WRONG

**1. I published a wrong root cause last round, and this round found it.** BL-1534's report
says `discover` catches `_CapReached` per page. It does not — `_tick`'s `except Exception`
swallowed the stop. I diagnosed from the shape of the code instead of driving it, and the
warning that would have told me was printed and unread.

**2. My paired hero harness failed 14 of 14 and the failure was mine, not the hero's.** I
drew the pair's videos from the hashtag lane. **Measured: 0 of 30 hashtag items carry `_raw`
or `play_url`** — the normaliser keeps cover/desc/views and drops the play address, so
`hero_for_video` had no file to open. The live funnel uses the account's *own* videos, which
is why BL-1534 built a hero on 15 of 16. Re-pointed at `videos_from_handle`: **12 of 12
built.** The instrument correctly refused to report the first run as a zero — *"NO SCORED
PAIRS — this measured NOTHING"* — which is the only reason it did not become a false finding.

**3. I nearly reported a 58.7% picture loss on every row.** An area ratio cannot tell a
downscale from a crop. Adding the aspect-ratio discriminator turned one wrong headline into
one real defect (7 genuinely cropped) and 43 harmless resizes.

**4. My first `or ""` check produced a false positive** on an already-fixed defect. A crude
substring search hit URL fallbacks; reading the lines settled it.

**5. I guessed at a counter that does not exist.** I wrote `result.get("processed") or
result.get("walked") or 0` for the page budget — **neither key is in the result dict**. A
`.get()` on an absent key is a silent zero that would have made `stop_after_pages` fire never.
Checked against the literal declaration and replaced with `len(rows)`.

**6. I trusted a launcher's exit code for about a minute.** `start "" "…​.bat"` returned 0
with **no python listening** — the exact "the launcher returned 0" trap. Caught by checking
the listening-port table for a python owner rather than believing the return code.

**7. The watcher told me the run had halted. It had not.** Its 25-minute window had expired.
A sub-agent's report is a claim; I checked the log was still growing before repeating it.

---

## 8. TESTS, SAFETY, AND ROUTING

**265 of 266 green** in the blast radius. The one red —
`test_bl1516_paid_call_ordering` — **was already red before this round**: it is FAIL in
BL-1534's full-suite log *and* in that round's pre-existing baseline. My change inserts a
guard at the top of `_process` and cannot reorder statements relative to one another.
**I did not subtract two runner totals**; attribution is per-suite-name against the
pre-round state.

**The new test file** uses `raise`, never `assert` (`python -O` strips an assert and would
disarm a guard silently), **parses its own source** and fails on any `ast.Assert`, and carries
**a planted control proving the detector can see one**. Everything structural is located by
parsing, with a control asserting the probe found something — **no byte-window guards**.

**Safety.** All 8 files backed up (config, spend, master, **all five** seen stores),
sha256-verified, path from one round constant. Bodies found **by shape**: `spend.json` is a
list at `runs` (**31,933 rows**), `clip_seen.json` a bare list (**2,193**). **Both corruption
controls fired**, including the one that matters:

> `spend.json` holds **31,933 rows under 26,026 distinct natural keys**. Deleting row #2279 —
> one of a duplicated pair — left the natural-key set **IDENTICAL** while the
> **index-qualified fingerprint CHANGED**. The blind instrument saw nothing.

**The cap binds.** `reserve()`'s real source was lifted by AST and driven: a funded $2.00 cap
**allows** and the meter advances (3,333 requests); the ceiling **raises**; **$0.00 raises**;
and **the meter does not advance on either refusal**. `spend.json` was **byte-identical across
the whole proof** — the proof wrote nowhere.

**The commit was refused once, correctly, and `--no-verify` was not used.** This round's
spend pushed the ledger past the +2000 row-lag bound, so `docs/FACTS.md` stamped **n=29,970
against a live 32,042** and the pre-commit guard refused: *"a canonical file that is allowed
to rot launders a stale number into an authoritative one."* Re-stamped from **one read**
(the ledger is live and peer rounds bill into it, so five separate reads would stamp five
mutually inconsistent numbers).

⚠️ **AND RE-STAMPING IT FOUND A THIRD TOTAL THAT DISAGREES.** The header `total_spent_usd`
and the sum of the five typed category columns agree **exactly** at **$64.882417**. The
per-row **`dollars`** column — which is what the guard's `lifetime_total_usd` actually reads
— sums to **$64.883617**, **$0.001200 higher**. That is the known shape that `dollars` is
*not* the category sum: at least one row carries a `dollars` value its own category columns
do not account for. **All three are now recorded in FACTS.md rather than reconciled**, because
averaging two instruments hides whichever one is wrong. My own first pass stamped the
`dollars` figure into the "GRAND TOTAL (typed columns)" row, which would have made the file
self-contradicting; the guard caught it.

**Ports.** The listening-port table was checked before every write under `clippershq/` and
immediately before the live run. `dashboard/.running.json` still names a pid and a port and
**still lies**; it was not consulted. No python process was killed.

**Config secrets.** Named keys only. BL-1534 dumped a live vendor key into its own scratch
output by printing the whole file; that did not happen here.

### What I routed where

| Work | Model | What it saved |
|---|---|---|
| Paging / import census across `clippershq/` | **Haiku** | **60,605 tokens**, 66 tool calls of grep and file dumps |
| Live run watcher, 5 anomaly classes | **Haiku** | **66,662 tokens**, 19 polling calls over 28 minutes |
| Accessibility review of the sheet | specialist agent | **384,379 tokens** — measured two engines across 21 control cases |
| Everything else | this model | rule semantics, the crop-vs-downscale distinction, the paired design, every number's meaning |

**127,267 tokens of mechanical output** stayed out of the expensive context on the two Haiku
tasks. **No sub-agent was spawned for anything one command answers** — the drain, the cap
proof, the stats and the defect analysis were all single commands here.

⚠️ **And a sub-agent's report is a claim.** I verified both load-bearing census claims myself
before relying on them (`meme_finder:3305` is Instagram; `term_engine` has zero AST importers)
and I checked the watcher's "halted" claim before repeating it — it was wrong.

---

## 9. WHAT THE NEXT ROUND SHOULD DO

1. **Fix the crop.** 7 of 50 pictures lost their bottom 29.6% and 2 of those pages were
   rejected on it. `tile_b64` crops a tall sheet to 16:9 whenever `tiles ≤ 1`.
2. **Get his grading back** and compute the real keep rate. Everything above is a delivery
   count; only his marks turn it into a yield.
3. **Open a second tag.** `#ufcedit` is drained at 138 accounts and his rule is "use it once,
   never again." `movieedit` showed 149 authors in 6 pages and is the obvious next.
4. **Re-score the hero at n ≈ 60**, or on pages where the two arms actually disagree — at
   n=12 with zero rejections in either arm the comparison has no power.
5. **Decide `hand_rule_facts`.** The switch is built and off; scoring it paired is one run.

---

*Round BL-1536. Claim filed in `.claims/BL-1536.json` and ended on completion. Backups in
`backups_bl1536_20260909/`, sha256-verified, both corruption controls fired.*
