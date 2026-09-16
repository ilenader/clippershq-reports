# BL-1566 — the F2 collapse was tag selection, and a $0 spend cap meant no cap

**Round:** BL-1566 · **Unit:** `api.cost_per_call_usd` = $0.00060000, by named key (never
`ig_api`'s $0.00069064) · **Spent:** $0.13860 of a $0.50 cap

## The paragraph

**Yes — the price collapse is reversible by walking fresh tags, and the evidence is not
close.** Nine fresh tags at p≤30 came in at **F2 = 3.274% [1.164–6.091]**, cluster-bootstrapped
over tags, against BL-1564's **0.795% [0.59–0.99]** — **non-overlapping**. The collapse was
BL-1564's **tag selection**, not the surface, and the tag list is the lever. **The next 1,000
costs $2.48 at a 30-page cap** against the $13.92 BL-1564 actually paid — a 5.6x improvement,
and better than the ~$4.01 that capping alone was projected to give. **The single biggest
thing still unexamined is not in this project's code at all: 13,007 addresses have been
collected and not one has ever been contacted**, so every rate above is a proxy for a value
nobody has measured — and 77.4% of the money ledger is a judge whose largest single line item
is a price its own author writes down as "probably LOW".

## 1. What this project is, for a reader with no context

It finds video editors on TikTok who put an email address in their bio. A paid vendor API
returns hashtag pages; each page carries up to 30 posts and the author's bio rides along
free. A dedup guard refuses accounts and addresses already held. One call = one page =
$0.00060000.

**The standing fact that outranks every price here: 13,007 addresses collected, NOT ONE EVER
CONTACTED.** All outcome columns empty on all 74,162 rows. `clippershq/outcomes.py` is 847
lines with production callers and 63 passing tests and has never written a real outcome.
This project does not send, by explicit decision, and this round did not build a sender.

## 2. Safety, money, and the cap

Ten stores backed up sha256-verified, bodies found **by shape**. **All six numbered
corruption controls fired**, counted by matching the numbered lines — `controls()` also
prints a warning and a summary, so a naive print-site count answers 8 and would pass a
threshold of 6 with two real controls deleted.

**The cap was driven before the first call** (`Budget` lifted from `harvest_run.py` by AST):
funded allows and the meter advances, $0.00 raises, the meter does not advance on a refusal,
3 funded calls allow 3 and refuse the 4th, and the proof **wrote nowhere**.

⚠️ **And the stage buckets were read from the source before booking.** BL-1565 spent its only
money and failed to book it because it passed `stage="research"`, which `validate_stage`
correctly refuses. This round drove `validate_stage("discovery")` → `'discovery'` and
`validate_stage("research")` → raises, *before* the walk. **231 of 231 calls booked.**

## 3. Part 1 — the named test, and the answer

**The draw was built so it could not smuggle the answer in.** Fresh on v2 only (no re-opened
tags — a re-opened tag's kept accounts are the pages the first pass never reached).
**Round-robin across 8 buckets**, seed-shuffled within each, **never ordered by recorded
yield** — yield carries almost nothing (r=0.009) and tag shape is refuted outright.

| tag | pages | kept | carrying an address | F2 |
|---|---|---|---|---|
| `kendricklamaredit` | 30 | 342 | 34 | 9.942% |
| `lamineyamaledit` | 30 | 290 | 8 | 2.759% |
| `rockleeedit` | 30 | 289 | 3 | 1.038% |
| `anthonyedwardsedit` | 30 | 274 | 8 | 2.920% |
| `scarfaceedit` | 30 | 213 | 5 | 2.347% |
| `reymysterioedit` | 25 | 165 | 0 | 0.000% |
| `thewireedit` | 30 | 126 | 2 | 1.587% |
| `nachtedit` | 13 | 74 | 0 | 0.000% |
| `raikkonenedit` | 3 | 13 | 0 | 0.000% |

| arm | F2 | interval |
|---|---|---|
| **BL-1566 fresh, p≤30, 9 tags** | **3.274%** | **[1.164–6.091]** |
| BL-1564 (17 tags, ~170 pages) | 0.795% | [0.59–0.99] |
| BL-1563 (75 tags, ~170 pages) | 2.195% | — |

**The intervals do not overlap.** The collapse was BL-1564's **tag selection**, not the surface. Walking fresh supply recovers the rate, and the tag list is the lever.

### 3a. The null, simulated BEFORE the spread was explained

The observed max/min F2 across the non-zero tags is **9.58x**. Under a constant rate of
3.360%, a spread that big or bigger appears **7.6% of the time**. **So the spread is not
evidence of anything**, and the one big tag does not get a story.

### 3b. What else differs between the arms — named, not assumed away

This is the rule the previous round broke: it called a comparison confound-free when the
store had grown between the two arms.

* **DEPTH** — this walk is p≤30; the comparison rounds walked to ~170. BL-1565's per-page
  curve found address-carriers flat over depth, so this should not bias F2 — **but that curve
  is one tag and the caveat stands.**
* **STORE** — this walk runs against a store ~1,000 accounts larger than BL-1564's, which
  biases F2 **downward**. So a high reading is conservative; a low reading would have been
  ambiguous between surface and store.

## 4. Part 2 — the per-page curve, nine tags instead of one

| pages | pages walked | items | items/page |
|---|---|---|---|
| 1–5 | 43 | 622 | 14.46 |
| 6–10 | 40 | 546 | 13.65 |
| 11–15 | 38 | 502 | 13.21 |
| 16–20 | 35 | 498 | 14.23 |
| 21–25 | 35 | 424 | 12.11 |
| 26–30 | 30 | 427 | 14.23 |

**Items per page is flat over pages 1–30** (14.46 → 14.23). BL-1565 measured *kept* accounts
per page falling 8.70 → 2.80 over 170 pages. **These are different quantities and are not
presented as agreeing**: the vendor keeps serving ~14 items a page, and the falling kept-count
is **deduplication**, not shrinking pages.

⚠️ **The page-log hook records `items`, not `kept`** — it fires inside the page loop before the
guard runs. So the kept-side claim is **NOT re-tested here**, and that is reported as ABSENT
rather than silently substituted.

### 4a. What share of pages return nothing — askable for the first time

The row files have always been 100% survivorship: only productive accounts are ever written,
so "which calls were wasted" had no answer on disk.

| | |
|---|---|
| pages logged | 221 |
| returned **zero items** | 3 (1.36%) |
| cost of those pages | $0.00180 of $0.13260 |
| every empty page was its tag's **last** page | yes |

**There is no scattered waste.** The only dead call is the one terminal probe per tag that
discovers the tag has ended — $0.0006 each.

## 5. The hunts

### 5a. BL-1565's wrapper-booking fix reached nothing — and it was mine

BL-1565 taught `LockedBudget` to book at the wrapper every 25 calls, **but only when a
campaign is named**. An AST sweep found **0 of 36 construction sites naming one** —
including `Harvester`, the only production caller. So the walker still booked nothing by
default, which is the exact state BL-1565 set out to fix. **A fix that is not wired is not a
fix.** Wired at the chokepoint; it booked **231 of 231 calls in this very walk**.

**Which instrument answered:** the AST. Only it can tell a construction from a mention and
read the keywords. grep returned 75 text lines over the same name — but grep is not
redundant, it is the only one that can see a name built inside a string literal.

### 5b. A declared $0 spend cap meant NO CAP

`clippershq/main.py:5547-5548` resolved two money ceilings with `config.get(k) or None`:

```
declared 0   -> None    # indistinguishable from "not set"
not declared -> None
```

So an operator who typed **0** to refuse all spend got the pre-run abort skipped and a banner
reading *"Spend cap: off"*. **This is the shape BL-1487 measured, where a declared $50
lifetime cap meant UNLIMITED** — still live on the two ceilings an operator is most likely to
actually set. Fixed by **reusing `spend_ledger.lifetime_cap_declared()`**, the presence-based
resolver BL-1487 already built, rather than writing a third implementation. Driven: declared 0
→ `(0.0, True)`, not set → `(None, False)`, malformed → `(None, False)`.

The same sweep found this shape alive across the funnel caps — `control.py:1799/2281/2768`,
`email_finder.py:643`, `twitch_finder.py:1501`, `spotify_finder.py:1041` all feed
`float(cfg.get(k, 5.0) or 0)` into `if max_run_usd and …`, so **a declared ceiling of 0 means
uncapped**. **Reported, not fixed** — each needs its own consumer audit and this round bought
one test, not six.

### 5c. The editor rate has never been measured over the accounts actually harvested

BL-1564 kept **12,326 accounts and read 10,820 bios** — and stored **88**, the ones that
carried an address. **10,732 bios were fetched, read, and thrown away.** So every editor-rate
figure this project owns is conditioned on *"and it also had an email in the bio"*, and the
rate over accounts harvested is unrecoverable from disk.

And the five priors are **not one question**. The four small ones share a denominator and an
instrument and pool to **13.21% [9.74–17.68]** — they do not disagree. The fifth, 29.37%
n=2387, measures **stored accounts already in `master_leads.csv`** — *the set every walk's
dedup guard exists to exclude*. Inventory already taken versus net-new supply are complements,
not two estimates of one rate. Holding platform and instrument fixed still splits them: stored
TikTok **31.51% [29.62–33.46]** against fresh TikTok **12.50% [7.13–21.01]**, non-overlapping.

**Fixed going forward for $0.00:** the gate verdict is now counted per **kept** account — one
boolean, no bio stored, denominator answerable forever.

### 5d. Where the money actually is

Re-derived from the ledger, not taken on report:

| campaign | rows | share |
|---|---|---|
| FREE_JUDGE | 29,921 | **77.4%** |
| SPOTIFY_FINDER | 2,799 | 7.2% |
| MEME_FINDER | 2,486 | 6.4% |

Inside FREE_JUDGE's $3.749303: `free_judge_paid_fallback` $1.524214 (measured),
`nex-n2-mini` $0.595588 (measured), and **`glm-5.3-flash` $1.629501 — flagged `estimated`,
43.5% of the judge's bill.** That price is *"DERIVED = 3 × nex's prompt rate"*, and the code's
own comment says the estimate **"is probably LOW"** (`free_judge.py:318-324`). **In a project
that quotes $/1,000 to four decimals, 2.24% of lifetime spend is a guess its author believes
under-counts.**

⚠️ **And the name is a defect.** `MAY_REJECT` and `PAID_MODELS` contain the same two model
ids, and `PAID_FIRST = True` (`free_judge.py:380`) asks the paid one first **by design**.
**The set of models allowed to cut and the set that cost money are identical — there is no
free cutter.** The spend is intended; the word "free" in the name is what is wrong, and it is
why a standing memory still reads *"the free reject gate has ZERO live models that may cut"* —
a sentence true only if "free" means "zero-cost".

### 5e. Dead things that READ LIKE SAFETY CHECKS

The sweep for values computed and never read finished after this report was first published
and the report was updated in place. **Its most valuable findings are not merely unused —
they are inert twins of guards that look live.**

**`meme_finder.py:5555` `JUDGE_RULES_NEEDING_PROFILE`.** Its own comment says it exists so
that "a rule which is in NEITHER set refuses the deferral — an unknown rule fails CLOSED".
AST: **1 store, 0 loads.** Nothing reads it. The fail-closed property is real but comes from
the *allowlist* beside it, `JUDGE_RULES_POSTS_ONLY` (1 store, **1 load**). So the comment
describes a mechanism that does not exist, next to one that does.

**`ig_client.py:804` and `api_client.py:360` `unexpected_status_count`.** The comment is
explicit about why it was added: without it "a vendor changing its refusal code would look
exactly like Instagram running out of posts — **silently, and at full price**". AST in both
clients: **2 stores, 0 loads.** The thing built to stop a silent, paid-for failure mode is
itself silent. Same shape for `unbilled_requests` and `throttled_requests`
(`ig_client.py:795-796`), whose comment promises "the run summary can say so" — it does not.

**Both instruments failed once, in opposite directions**, which is the case for running both:

| | AST | grep |
|---|---|---|
| attributes stored, never loaded | 28 | **0 — a false zero** |
| counters incremented, never branched on | 352 | **0 — a false zero** |
| module constants never referenced | 90 of 1,752 | 33 |

grep's zeros came from counting a wordlist, a shipped *copy* of the app under `output/`, and
report prose as "readers"; excluding those restored 26 findings. And the 440x over-count
reproduced exactly — `checked` returned **3,437 grep lines against 3 real sites**. In the
other direction **AST alone produced 7 false positives**, all reads via
`getattr(o, "name", …)` — including `tt_deep_calls`, which would have been reported as a
broken vendor-billing split had the text pass not shown it works.

⚠️ **VARYING-AND-UNREAD is reported separately from merely unread**: 26 attributes and 9
summary keys carry real per-run information that is computed and discarded, against 33
constants that could never have decided anything. And every verdict is an **UPPER BOUND** on
deadness — leaf-name matching cannot see a read via a runtime-assembled name.

### 5f. A column declared on 74,162 rows that nothing ever writes

`vision_verdict` is declared in `writer.py::FULL_COLUMNS` (`writer.py:78`) and `_build_row`
ends `return [rec.get(col, "") for col in FULL_COLUMNS]` (`writer.py:2135`). An AST pass finds
**0 assignments of that key anywhere in `writer.py`**; a text pass finds 2 occurrences (a
comment and the column list). **Which answered: the AST** — grep alone would have called two
mentions "present". The funnel that writes every row emits `""` by the `.get` default because
no code ever tries.

## 6. The output

* **The F2 question is closed**: fresh tags 3.274% [1.164–6.091] vs BL-1564's 0.795% [0.59–0.99].
* **$2.48 per 1,000 net-new** against $13.92.
* 56 net-new addresses are in the row file, **not written to any store** — this round's claim
  did not declare `master_leads.csv` and the scope was not widened silently.
* Four defects fixed and driven; several more reported with `file:line`.

## 7. WHAT I GOT WRONG

**I shipped a fix last round that reached nothing, and only found it because I went looking
for something else.** BL-1565's wrapper booking was correct in the module and wired to zero of
36 construction sites. I wrote it, drove it in isolation, committed it, and published a report
saying the hole was closed. It was not. **Driving a helper is not driving the path.**

**I let a bash shell eat a backslash and a set of dollar signs in the same session** — once
mangling a regex in a sweep, once corrupting prices inside a claim file. The rule "write source
with a file tool, never a shell" was already written down, and applies to *data* with dollar
signs exactly as much as to code.

**I over-trusted a shape I had just measured.** When the first three fresh tags came in at
1.7%, I said the picture was "forming" — on n=3, before the null had been simulated. The
conclusion held, but it held by luck of the data: the null test came later and could have
said the spread was noise.

## 8. What did not run, reported as ABSENT

* **`batiatusedit` returned no pages at all** — the vendor 500'd on `hashtag_info` after 2
  tries. It contributes no denominator and is excluded from the nine. **A tag that never
  returned a page is not a tag with a 0% rate.**
* **The kept-per-page shape was NOT re-tested** — the page-log hook records `items`, not
  `kept`. BL-1565's 8.70 → 2.80 still rests on one tag.
* **The depth tail beyond page 30 was not walked** this round, so nothing here speaks to it.
* **The funnel-cap zero-means-uncapped sites are reported, not fixed** — six sites, each
  needing its own consumer audit.
* **The dead-value sweep FINISHED AFTER first publication; this report was updated in place (same filename) rather than a second file being created. Its findings are section 5e.**
* **BL-1562's claim is still stale-OPEN** with its report published and no manifest. Noted,
  not touched — another round's claim.
* No outreach was sent. This project does not send.
