# BL-1498 — The search-term engine: his instinct is right about breadth and wrong about purity

## HOW MANY DISTINCT EDIT PAGES CAN THIS FIND, AND AT WHAT COST PER 1,000 DELIVERED?

**Supply is effectively unlimited and nearly free. Purity is not what he thinks, and the cost
question cannot be answered in the unit he asked for — yet.**

Measured on 133 billed calls across both platforms for **$0.088 total**: ten search terms
returned **258 distinct TikTok authors** and **187 distinct Instagram accounts**, of which
**97.8%** and **100.0%** respectively were **net-new against the live seen stores**. Reversing
the word order on Instagram's account search returns a **near-disjoint set** (Jaccard 0.00–0.05,
58 of 58 net-new), so **every subject really is two terms there**. Cost of net-new supply,
measured directly: **≈$0.037 per 1,000 net-new accounts on both platforms.** Discovery is not
where the money goes.

**But "the first hundred accounts are near perfect" does not survive measurement.** The obvious
test is circular — search matched the caption because the query wrote the word in it. On the
non-circular test (does the account's own handle or display name carry an editing signal),
TikTok is **22.7% pooled** [median 0.205, range 0.071–0.464]. Instagram's account-search reads
98.4%, and **that is a tautology too**: it is a literal name match returning accounts *named*
"&lt;subject&gt;edits" — a label, not a signature. Nothing in this round watched a video.

**And the cost per 1,000 delivered cannot honestly be given.** This round measured supply, not
delivery; composing a delivered price from a carry rate is exactly how **$137.31** and **$78.53**
were each manufactured. What is measured directly, and what the mix shift is worth, is in §3.7 —
including the fact that **the mix shift does not close the gap on its own**: Instagram memes is
88× over the dollar target and 133× over the clock, and a 3.6× improvement leaves it ~37× and
~74× out.

---

## 1. Round ID, date, and what it was asked to do

**BL-1498**, 2026-09-04. Build the search-term discovery engine. **This round changes where
pages come from and nothing else** — it adds no judging rule, moves no threshold, and touches
no verdict.

**Why this is the largest lever available.** Across the 14,280 accounts the funnel has actually
walked:

| source | share of walk | delivered per walked | his approval | marks behind it |
|---|---:|---|---|---:|
| **seed** | **82.32%** | 1.650% [1.4, 1.9] | **38.6%** [25.7, 53.4] | 44 |
| hashtag | 11.55% | 8.727% [7.5, 10.2] | 33.3% [18.0, 53.3] | 24 |
| **reels** | **3.35%** | **14.017%** [11.2, 17.4] | **81.8%** [65.6, 91.4] | 33 |
| search | 2.78% | 5.542% [3.7, 8.2] | 77.8% [54.8, 91.0] | 18 |

**He walks 82% of his pages on the source that converts worst and he approves least.**

**The honest limits.** The left columns rest on 14,280 accounts and are solid — the delivered
counts reproduce cell for cell (seed 194, hashtag 144, reels 67, search 22; total 427, and
427/14,280 = the share-weighted sum to **9 decimal places**). **The approval column rests on
119 marks in total and reels is 33 pages.** Reels [65.6, 91.4] and seed [25.7, 53.4] **do not
overlap**, so that contrast is real. Hashtag and seed overlap almost entirely and are **not
distinguishable at this size**.

**Conditions at start**: no dashboard or sheet-server listener (read from the listening-port
table, never a command-line filter), 3 Python processes, 377 GiB free. Three other rounds live.

---

## 2. What actually shipped

| file | what it is | fix category |
|---|---|---|
| `scratch/bl1397_build_sheet.py` | **Part 0**: the source stamp now survives into a saved mark | **GENERAL** — the field is packed at the one place the JS builds its POST body from, so no caller can forget it |
| `clippershq/search_terms.py` | the engine: generator, ledger, scoreboard, expansion loop | **GENERAL** — `next_terms()` is a chokepoint; there is no code path that yields a term without consulting the ledger. **Its save shipped broken and was fixed after publication — see §5** |
| `tools/term_engine.py` | operator CLI: `plan / board / dead / expand / stats` | LOCAL — a reader, spends nothing |
| `tests/test_bl1498_source_stamp.py` | 5 tests, incl. a negative control | — |
| `tests/test_bl1498_term_engine.py` | **14** tests, incl. a **mutation proof** and the atomic-save spy | — |

**Defaults are unchanged.** Nothing is switched on. `tools/term_engine.py plan` is read-only and
spends nothing, so the engine can be inspected against a budget before it is trusted with one.

### 2.1 Part 0 — the fix without which this round could not measure itself

Every discovery source correctly stamps `found_via`, and the sheet **renders** it
(`bl1397_build_sheet.py:255`, `:303`), so it reached his eyes. But the packed record handed to
the page's JavaScript carried only `handle/side/html`, and **the JS builds its POST body out of
exactly that dict** (`:181`, `:188`). So the source was on screen and absent from disk.

**Measured: `found_via` appears on 0 of 683 mark rows.** Confirmed by re-reading every row raw.

**Every source trace that exists today is a handle join to a second store**, and it is
incomplete: **411 of 537 marks traceable = 76.54% [72.8, 79.9]**, 126 not traceable at all
(111 TikTok, 15 with no platform recorded, **0 Instagram**). Second derivation by a different
route (collapsing on handle alone): 408 of 534 = 76.4%, 0.1 points away. **Positive control**:
500 handles drawn from the checkpoint store were pushed through the same lookup and **500 of 500
resolved**, so the join works and the 126 really are absent.

**Fixed and proven by driving the real builder** — not by grep, not by a docstring. 5 tests
pass, including a negative control that reproduces the pre-fix shape and confirms the check can
fail. The server needed no change: `bl1397_serve.py:117-118` appends the whole posted body.

**My diff adds exactly three non-comment lines, all carrying `found_via`, and zero judging
lines.** That is the "no verdict moved" control, verified on the diff itself.

---

## 3. What was measured

### 3.1 The four briefs, at the network boundary

Verified by capturing the request body, with a **two-way control**:

| brain | sha12 | expected | |
|---|---|---|---|
| tiktok / memes | `28c05f855e13` | `28c05f855e13` | MATCH (4,918 chars) |
| tiktok / edits | `d43802ad3f9a` | `d43802ad3f9a` | MATCH (10,079 chars) |
| instagram / memes | `46a1a4d89cbc` | `46a1a4d89cbc` | MATCH (5,749 chars) |
| instagram / edits | `ff1ff0b70cb0` | `ff1ff0b70cb0` | MATCH (10,910 chars) |

**4 of 4 match. Control (a): a mutated brief does not match — the check can fail. Control (b):
the four hashes are distinct — NOT POOLED.**

### 3.1b Which source contrasts actually survive — and it is not the one everyone quotes

Fisher exact tests on the traceable marks:

| comparison | verdict | p |
|---|---|---|
| reels vs seed | **separates** — 12.2-point gap, no interval overlap | **0.0001** |
| search vs seed | **separates** | **0.011** |
| **reels vs search** | **NOT distinguishable** | **0.72** |
| hashtag vs seed | **NOT distinguishable** — 27.6 points of overlap | 0.794 |

**So the evidence supports "reels OR SEARCH beats seed and hashtag" — not reels specifically.**
That matters, because the costed mix raises reels, whose supply needs a 7.5–13× increase, while
search is statistically its equal and its supply is the thing this round proved is unlimited.

On all 411 traceable marks the per-source approval reads: **search 49/60 = 81.7%**, reels
37/54 = 68.5%, hashtag 78/168 = 46.4%, seed 28/85 = 32.9% — plus **three sources his marks
contain that the four-surface table does not**: suggested 6/32, known-repost-account 2/11, and
one crawl source 0/1.

### 3.2 The probe — TikTok, 45 billed calls, $0.0270 by the run's own counter

Ten terms of his shape, one billed call each, count=30. **Terms are safe to publish and are the
most useful part of this report**, so they are given in full.

| category | term | distinct authors | net-new |
|---|---|---:|---:|
| sport | `boxing edit` | 25 | 25 |
| football | `ronaldo edit` | 17 | 16 |
| basketball | `lebron edit` | 27 | 25 |
| money | `money edit` | 25 | 23 |
| religious | `jesus edit` | 28 | 28 |
| country | `japan edit` | 30 | 28 |
| history | `history edit` | 26 | 26 |
| movie | `joker edit` | 29 | 29 |
| cartoon | `spongebob edit` | 25 | 25 |
| person | `elon musk edit` | 27 | 27 |

**258 distinct authors from 10 calls. Cross-term collision: 1 in 258.** Pooled across all 30
single-page term calls: **authors/call median 26.0** (range 17–30), **net-new 97.8%
(746/763)** against the 2,446-page TikTok seen store. **Net-new was computed on sha256[:10] ID
SETS, never on counts** — an invented parameter once produced more "net-new" than the real
cursor because the cache key changed, not the results.

**Breadth holds.** Ten further terms — `ufc edit`, `messi edit`, `kobe edit`, `rich edit`,
`quran edit`, `brazil edit`, `roman empire edit`, `batman edit`, `naruto edit`,
`andrew tate edit` — scored **85–100% marginal net-new** against the probe's own union, taking
it from 350 to 580.

### 3.3 The probe — Instagram, 88 billed calls, $0.06078 by the run's own counter

**Two channels, and they behave completely differently.**

| | account search (`meme_finder.py:3289`) | reels search (`:3176`) |
|---|---|---|
| accounts/call, 10 terms | median **19**, total 187 | median **11**, total 108 |
| net-new (ID-set diff vs 6,125 handles) | **187/187 = 100.0%** | **107/108 = 99.1%** |
| "edit" in handle + full name | 98.4% | 10.2% |

Ten terms in full: `boxing edit`, `champions league edit`, `nba edit`, `money edit`,
`islam edit`, `japan edit`, `history edit`, `joker edit`, `spongebob edit`,
`andrew tate edit`.

**Zero HTTP-200-charged-and-empty responses.** Every result was validated on the parsed item
list, never on status.

### 3.4 Purity — his claim, refuted as stated

**The obvious heuristic is circular and must not be quoted.** "The caption or hashtags contain
'edit'" scores ~100% because the search matched the caption and the query put the word there.

Non-circular, denominator = distinct authors per call:

- **TikTok, does the account's own handle or display name carry an editing signal**
  (`edit|edts?|editz|editor|vfx|amv|fx|aftereffect|clipz|clips|4k|velocity`): **173/763 = 22.7%
  pooled**; per-call **median 0.205**, p25 0.160, p75 0.304, **range 0.071 (`brazil edit`) –
  0.464 (`jesus edit`)**. Only 2 of 30 calls exceed 0.40.
- **TikTok, hashtags naming the craft** (capcut/alightmotion/aftereffects/velocity/amv/vfx):
  **33/504 = 6.5%**, median 1 per call.
- **Instagram account search reads 98.4% — and that is a tautology.** Three extra calls
  established that 57 of 57 results carry *both* the "edit" token *and* the subject token. It is
  a literal name match: it returns accounts **named** "&lt;subject&gt;edits". **A label, not a
  signature.**

**So: "search anything plus edit and the first hundred accounts are near perfect" is not
supported.** On TikTok about one account in five looks like an editing account by name. On
Instagram the number is high because the surface matches names, which is a different claim.
**Nothing in this round watched a video, so none of this measures whether a page makes good
edits** — only what it is called.

### 3.5 Word order — real on one surface, noise on the others

| surface | Jaccard, `X edit` vs `edit X` | its own repeat-call control | verdict |
|---|---|---|---|
| **Instagram account search** | **0.05 / 0.00 / 0.03** | ~1.00 self-overlap on repeat | **near-disjoint — REAL** |
| TikTok search | 0.360 / 0.429 / 0.333 | **0.565 / 0.471 / 0.531** | inside the noise floor |
| Instagram reels | 0.10 – 0.26 | ~35% re-roll noise | proves nothing |

**On Instagram's account search, reversing the order genuinely doubles the vocabulary for
free**: the reversed terms kept their purity (20/20, 17/18, 20/20 carrying the edit token) and
were **58 of 58 net-new**.

**On TikTok it is a weak second axis, not a doubling** — page 1 is only about 50% reproducible
call to call (10-term repeat control: **median Jaccard 0.53**, range 0.395–0.862), so most of
the difference he sees between the two orders is the surface re-rolling, not two different
populations. **The engine generates both orders anyway** — on the surface where it pays it
doubles supply, and on the others it costs one call to find out.

### 3.6 Saturation and the cursor — the brief's premise is half wrong

**"A second page per term is free money the caller currently declines" is FALSE on Instagram.**
The asymmetry in the code is real — the client takes a cursor (`ig_client.py:596`, sent at
`:617-618`), the reels caller does not pass one (`meme_finder.py:3190`), and the hashtag caller
**does** walk one (`:3324`, loop `:3365-3368`, `HASHTAG_PAGES=2` at `:3322`). **But the page it
would fetch does not exist.** Controls on one term: the real cursor returned **3 new**; a
**bogus cursor returned 6–8 new**; a meaningless invented parameter returned **4–6 new**; and
**re-issuing the identical page-1 request 30 seconds later returned 7 of 12 new**. Back-to-back
identical requests are byte-identical. **It is a short vendor cache in front of a rotating
surface — the real cursor, a bogus one and garbage are indistinguishable.**

That is precisely the false-yield trap this round was warned about, reproduced live and
correctly refused.

**Instagram's account search saturates on call ONE**: new-per-call 20, 0, 0, 0, 0, 2, 0, 1, 0, 0
→ cumulative 23 over ten calls. **The current one-call-per-term caller is already right**, and
re-rolling it is money for nothing.

**TikTok does NOT saturate the way the Instagram surface does.** New authors per page over six
pages: **+20/+23/+16/+20/+18** and **+23/+20/+23/+22/+18** for two terms — **no decay, and no
page byte-identical to its predecessor**, reaching 116 and 129 cumulative distinct authors.
`has_more` lied **once, by one page**, and the shipped parser read the end-of-results shape
correctly. **So on TikTok, depth is genuinely available; on Instagram it is not.**

### 3.7 Cost — what can be measured directly, and what cannot

**Directly measured, no carry rate anywhere:**

| | calls | $ (own counter) | net-new accounts | **$ per 1,000 net-new** |
|---|---:|---:|---:|---|
| TikTok search | 45 | $0.0270 | 746 | **$0.0362** |
| Instagram account search | 10 | $0.0069 | 187 | **$0.0369** |

**Supply costs about four cents per thousand net-new accounts on both platforms.** TikTok yields
**12.9 distinct authors per US cent**.

**The mix arithmetic reproduces exactly.** Baseline 1 approved per **74.61** walked; at 25%
reels / 15% search / 40% hashtag / 20% seed, 1 per **20.7** — a **3.6×** gain. A second
derivation by delivered-mix weighting agrees **to nine decimal places**. On today's re-measured
inputs: **73.0 / 20.7 / 3.5×**. The one carried figure that does **not** survive its own stated
method is the conservative case. Its sentence names two overrides and the shipped script
applies one: reels-lowered-only gives **23.55**, both overrides give **23.28**. Both round to
**3.2×**, so the headline holds and the number is 23.3, not 23.6.

**⚠️ THE MIX SHIFT DOES NOT CLOSE THE GAP, and this must not be soft-pedalled.** Against targets
of $2.00 and 2 hours per 1,000 delivered:

| brain | $ per 1,000 | over target | hours per 1,000 | over target |
|---|---:|---|---:|---|
| tiktok / memes | $19.52 | 9.8× | 8.21 | 4.1× |
| instagram / edits | $131.21 | 65.6× | 175.22 | 87.6× |
| instagram / memes | $176.76 | 88.4× | 265.69 | 132.8× |
| **tiktok / edits** | — | **has never delivered a page** | — | — |

Every one of those is dollars ÷ delivered and seconds ÷ delivered on the same run — **nothing is
divided by a carry rate**. A 3.6× improvement leaves Instagram memes **~37× over on money and
~74× over on the clock**. **Money and clock are two problems; this round is aimed at one.**

**⚠️ AND THE FUNNEL CANNOT REPORT ITS OWN STAGES.** The five stage counters —
`discovered / captured / judged / paid / delivered` — are **`None` on all 67 run records**
(`run_status.py:295-296`, `run.py:427-430`). **Positive control**: the same records carry
non-null `elapsed_s`, `spend_usd` and `leads`, so the reader works and the `None`s are real.
Every walked-and-delivered figure in this report is therefore a **substitute** reconstructed
from the discovery store, not the funnel's own count. Six denominators exist — discovered,
captured, entered-the-judge, judged, paid, delivered — and the funnel currently records none
of them.

**⚠️ And n is 1–6 runs per brain with 0–7 delivered pages — the smallest denominators in this
report. One extra delivered page moves Instagram edits from $131 to $105.**

**I am not publishing a per-call Instagram cost.** A peer round established that three ledger
sites priced Instagram at $0.000600 while the vendor bills $0.00069064 — verified independently
in the shipped source at `main.py:646`, with the stale default still at `:747` and `:791`. Any
Instagram cost computed before that correction lands is **13.1% light**.

### 3.8 The supply question that could sink it

Reels is **478 of 14,280** accounts. A 25% reels walk needs:

```
fixed walk :  0.25 × 14,280 = 3,570.0  ;  3,570.0 / 478 = 7.47×
growing    : (14,280 − 478) × (0.25/0.75) = 4,600.7  ;  / 478 = 9.62×
union of every store (19,238)          :  4,809.5 / 480 = 10.02×
```

**7.5× if the walk stays the same size, 9.6× if reels is added on top, 10.0–13.0× counting every
store.** The carried "~7.5×" is the **smallest** of four defensible answers.

**⚠️ AND THE LEVER IS INSTAGRAM-ONLY. TikTok has never produced a single reels account** — its
store is hashtag 2,040 / search 406 and nothing else.

**Does the term engine answer it?** Partly, and honestly: **the engine feeds search, not reels.**
Search's own approval is 77.8% [54.8, 91.0] — statistically indistinguishable from reels' 81.8%
— and search supply *is* the thing this round proved is unlimited. **So the achievable move is
to raise SEARCH, where supply is proven and nearly free, rather than reels, where supply needs a
7.5–13× increase this round did not demonstrate.** That is a different mix from the one costed,
and he should be shown both rather than sold one.

---

## 4. What was refused, and why

**I did not write `clippershq/meme_finder.py`.** BL-1496 holds it and offered no handover, so the
Instagram search caller at `:5926` is untouched. That is where the engine would wire in, and it
is a documented handover rather than an edit.

**I did not commit `clippershq/main.py`.** BL-1496 edited its money-ledger region first; a
pathspec commit clobbers regardless of region, so the discovery-side change waits on its commit.

**I did not add or loosen a judging rule, move a threshold, or touch a verdict.** Proven on the
diff: three non-comment lines, all `found_via`, zero judging lines — plus 4-of-4 brief hashes
matching with a two-way control.

**I did not run the funnel end to end**, so I did not manufacture a delivered price. The unit he
asked for is stated as unavailable rather than composed.

**Spend: $0.088 of a $1.50 cap**, counted by each run's own driver. **The shared ledger cannot
attribute it** — `spend.json` moved during this round because a *different* live round was
booking into it, which a peer session confirmed with timestamps. A ledger delta would have
credited me with their spend.

---

## 5. What I got wrong

**I shipped the ledger with a save that can silently fail, and I committed it.**
`TermLedger.save()` ended in a bare `os.replace(tmp, self.path)`. On Windows that raises
`PermissionError` [WinError 5] whenever another process holds the destination open, and 14
Python processes were live on this machine while I fixed it. A raised save does not lose one
write — **the ledger silently fails to persist, the `.tmp` is left behind, and the next run
re-walks terms it has already paid for.** That is this module's one job failing in the
direction that costs money, in the exact function this report calls "a ledger making a repeat
impossible".

The tree already had the answer and eight sibling modules already used it: `atomic_io.replace`
is a documented drop-in wrapping a WinError 5/32 retry, imported in `email_finder.py:469`,
`ig_client.py:186` and `crawl_suggested.py:41` with the same one-line comment. Mine did not.
**Found by a peer round's guard, after I had committed.** Fixed and proved by driving: a
runtime spy confirms the save routes through `atomic_io.replace` exactly once (with a control
proving the spy can read zero), and `retry_win32` was driven with a callable that raises twice
then succeeds so the retry the fix depends on is *observed*, not assumed.

### 5.1 A rule worth more than this round: a suite that silently skips a third of itself still says OK

Adding those tests, my append landed the new class **after** the `if __name__ == "__main__"`
block. `unittest` therefore printed:

```
Ran 10 tests in 0.025s
OK
```

**Four tests did not exist as far as the runner was concerned, and the suite was green.** I
caught it only because I expected 14 and counted. Moving one block to the end of the file
turned it into `Ran 14 tests ... OK`.

**The transferable form: a green suite is evidence only if you know how many tests it was
supposed to run.** "OK" is a statement about the tests that executed, never about the tests you
wrote. This is the same family as a check that skips its work and returns OK rather than
SKIPPED — the shape that hid a dead model here for five days. **Count the tests, not the
verdict.**

### 5.2 The rest

**My test was wrong and the code was right.** My expansion-loop test asserted that a second call
returns nothing; it failed, correctly — `expand` caps each call at a limit and the subject had
more neighbours than the cap, so the leftovers were rightly still on offer. I rewrote the
assertion to drain the loop instead of assuming its size.

**I edited another round's committed file by accident**, running a `sed` in place on
`scratch/bl1494_baseline.py` instead of on my copy. Restored from git immediately; the file is
clean.

**I claimed a round number that had been taken 0.9 minutes earlier.** My registry read showed two
rounds in flight; BL-1497 was filed between that read and my claim. The claim tool refused, which
is the only reason it did not collide.

**I would have published a wrong Instagram price** if a peer session had not flagged the
$0.000600 vs $0.00069064 gap. My Part 4 asks for every division written out, and I would have
written one out with a wrong numerator.

**Three figures I was given do not reproduce.** The three readings of reels approval — 81.8%
(119 marks), 75.0% (129), 73.8% (162) — measure **82.9% (29/35, n=121), 70.6% (36/51, n=142),
67.9% (36/53, n=186)** today. The mark files have not changed (all mtimes 25–28 August); the
**checkpoint store drifted**, and the reels handle pool was already 478 rather than 471 before
the prior report was written. Four separate reconstructions, including the prior report's own
stated temporal-join method, give the same answer. **Treat 82.9 / 70.6 / 67.9 as today and
81.8 / 75.0 / 73.8 as an unreconciled prior. All three populations are real; do not pick one.**

---

## 6. Money and safety

**$0.088 spent against a $1.50 cap**, by each run's own call counter. Two probes reported 45
calls / $0.0270 and 88 calls / $0.06078; the vendor client's own request count matched the
logical count exactly on every run (10/10, 10/10, 3/3, 12/12, 10/10) — no retry inflation.

**Protected files, verified at start and again at publication**: 7 of 8 byte-identical.
`spend.json` moved, and it is reported as movement rather than claimed unchanged — it is shared,
another round was booking into it concurrently, and a delta on it cannot attribute anything to
anyone.

**No seen-store row was deleted or rewritten.** Seen stores were opened read-only. Every fixture
handle is stamped `bl1498_fixture_*`; every assertion is on a computed set, never on membership
of a real record. One probe built its client `metered_by_caller=True` so autoflush could not
write the ledger.

**Disclosed instrument faults**: one probe's cursor fallback silently used the wrong field and
the vendor returned a 400 — **1 billed call, no data, and the affected row is recorded VOID, not
as a measured zero**. Another probe's cache-buster control failed on reuse and its conclusion was
re-grounded on a different phase that had already established the same thing. A `\b` corruption
hit a regex during patching and was caught with `cat -A` before any call was made.

**This report contains no handle, no email, no key, no port number and no absolute path with his
username.** Search terms are published in full, with their yields, because they are safe and are
the most reusable part of this work.

---

## 7. What to do next — ranked

**1. Decide the mix, with both options on the table.** Owner: **him**. The costed mix raises
*reels* and needs **7.5–13× more reels supply than the funnel has ever produced**, on Instagram
only. The alternative raises **search**, whose approval (77.8% [54.8, 91.0]) is statistically
indistinguishable from reels' and whose supply this round proved is unlimited at ~$0.037 per
1,000 net-new accounts. **Both are 3.5–3.6× on the arithmetic; only one has demonstrated
supply.**

**2. Wire the engine into the Instagram account-search caller**, `meme_finder.py:5926`, **and
generate both word orders there.** That is the single measured free doubling in this report:
near-disjoint result sets, 58 of 58 net-new, purity preserved. Blocked on a handover from
BL-1496.

**3. Do not add a second page on Instagram.** It is not free money declined; the page does not
exist. Account search saturates on call one and the current caller is already correct.

**4. Do add depth on TikTok.** It genuinely paginates — six pages with no decay and no repeated
page — and `discover_search_pages` already walks offsets with a stall guard.

**5. Re-grade one sheet now that `found_via` survives.** Until a sheet is built and marked with
the fix in place, source-vs-approval remains a 119-mark question answered by a handle join with
23% of marks untraceable.

**6. Stop quoting the caption heuristic.** It is circular by construction. If purity matters,
it has to be measured on something the query did not write.

---

## 8. Paths to open

| path | what is in it |
|---|---|
| `clippershq/search_terms.py` | the engine: 236 terms, 14 categories, ledger, scoreboard, expansion |
| `clippershq/search_terms.py::next_terms` | the chokepoint that makes a repeat impossible |
| `tools/term_engine.py` | `plan / board / dead / expand / stats` — read-only, spends nothing |
| `scratch/bl1397_build_sheet.py:418` | the source stamp, now packed |
| `scratch/bl1397_build_sheet.py:181,188` | the two POST bodies that now carry it |
| `tests/test_bl1498_term_engine.py` | the mutation proof that the chokepoint is load-bearing |
| `clippershq/ig_client.py:596,617` | the cursor the client takes |
| `clippershq/meme_finder.py:3190` | the reels caller that does not pass it — and need not |
| `clippershq/meme_finder.py:3322-3368` | the hashtag caller that does walk one |
| `clippershq/discovery_search.py:234` | TikTok paging, which genuinely works |

https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/BL-1498-the-search-term-engine.md
