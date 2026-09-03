# BL-1493 — the answer key, audited: the ceiling is 75.8%, and nothing reads it

> **Reading this cold?** This project finds social-media pages worth contacting and extracts a
> public contact address. It does not send anything. A vision model — the "judge" — decides
> whether the operator would want a page; the operator grades pages himself on review sheets, and
> those grades are the answer key every accuracy figure is scored against.
>
> Creator handles are redacted throughout. Paths are repository-relative or use `%USERPROFILE%`.
> No port numbers appear. No address is printed anywhere, in any form.

---

## THE ANSWER, IN ONE PARAGRAPH

**The real ceiling is 75.8% [69.1, 81.5] — but it is two numbers, not one: about 93% where his
score is far from his own want-floor of 6, and about 60% where it is close.** It also decays
within a sitting, from 88% early to 67% past row 300. **And he should stop trying to improve it,
because nothing consumes it.** No production file reads his marks: `wants_page` and
`WANT_SCORE_FLOOR` appear in the mark reader and in tests and nowhere else across 161 funnel
modules, and the 46 files that import the reader are 44 analysis scripts and 2 tests — **zero in
production**. The funnel writes sheets for him to mark and never reads the marks back into a
decision. So the ceiling cannot be the binding constraint on anything, and the three things worth
stopping are: **asking him for a 1–10 score** (it reproduces at 49–54% while the same judgement
as a keep/drop reproduces at 84–88%), **tuning any model-read visual feature** (80 of 80
comparisons fail once multiplicity is handled, and the two most-quoted ones sit inside their own
noise floor), and **pricing the Instagram page funnel as an address engine** (it supplies 15.6%
of this month's addresses at $78.53 per thousand, against Spotify's 84% at $1.21). The one thing
that is real, survives correction and is measured in pixels rather than by a model: **on TikTok,
his 9s and 10s are letterboxed and his 6s and 7s are not** — 70.0% of videos barred against
38.8%, a step at score 9, absent on Instagram where the feature is saturated.

---

## 1. Round ID, date, and what it was asked to do

**BL-1493, 2026-09-03.** Read-only. **No production writes of any kind** — no store, no config,
no doc, no test, no tool, no exemplar pack. Everything written lives under `scratch/bl1493_*`.

**Vendor spend: $0.00 by the round's own call counter.** No model was called; every instrument
ran with the network poisoned before importing anything from the funnel package. The shared
ledger is deliberately **not** cited as evidence of this round's spend: one cutting model bills
per token, is counted as a free send, and never books to the ledger, so the ledger understates.

Every round for weeks has audited the machine. **Nobody had audited the answer key.**

**Campaigns fingerprint, both forms, verified at round start and again at publication:**
`8e02f8d6f6307ae8` (default serialisation) / `7a029ee5447cddd8` (compact), 5 campaigns —
unchanged, so every figure here describes the same configuration.

---

## 2. What actually shipped

**Nothing.** That is the point of the round. Defects are named with file and line and left in
place, so a later round can wire the decisions in one pass instead of re-deriving them — which is
the failure this project keeps paying for: publication stopped for 124 rounds, 107 reports exist
only on one machine, and one fix was found, lost, and re-found eight days later at the cost of
three sessions in a day.

---

## 3. What was measured

### 3.1 ⚠️ The ceiling gates nothing. This is the finding of the round.

Three independent scans, each with a firing control:

| scan | result |
|---|---|
| text scan of 161 funnel modules for `wants_page`, `WANT_SCORE_FLOOR`, `mark_reader` | **0 files each** (controls: `def ` in 160, `import` in 158 — scanner not blind) |
| AST parse of the same 161 files | 13 executable references, **all of them unrelated `.resolve` calls**; 2 string literals, **both in sheet builders on the write path** (controls: 1,210 `os` name nodes, 179 `.json` literals — walker not blind) |
| repository-wide import scan | **46 files import the mark reader: 44 in `scratch/`, 2 in `tests/`, 0 in production** |

The funnel writes sheets for him to mark. Nothing reads the marks back. **A ceiling on a signal
that gates nothing cannot bind anything**, and the round's own brief — which treats the ceiling as
the constraint on everything — rests on a premise that does not hold.

**And nothing has ever been checked against an outcome.** All nine consumption columns in the
master file — sent, channel, replied, sentiment, bounced, converted, notes, touch number, variant
— are **empty on all 72,956 rows**, with a firing control (a synthetic 3-row file through the
identical scanner returned 9 of 9 columns detected). No accuracy figure this project has ever
produced, *his or the filter's*, has been validated against a reply.

A related and worse case: the vision stage's verdict is **persisted nowhere** (0 of 72,956) while
being **consumed at decision time**. That stage is 14.0% of all spend and is not idle — it is
**unauditable**.

### 3.2 The ceiling: 75.8% [69.1, 81.5], n = 178

Two independent derivations agree **to the row**: one collapsing files that agree on shared
pages, one using the sitting each sheet **declares in its own data**. 135 of 178 pages graded in
two or more distinct sittings.

The second derivation needed one fix that is itself a finding: **49 rows carry a blank
provenance field in a file that stamps provenance elsewhere.** Guessing the sitting from the
filename manufactured a phantom second opinion on those 49 pages and pushed the answer to 80.8%.
Dropping blank-provenance rows rather than guessing gives 75.8%.

**All seven published figures are the same dataset under different denominators:**

| published | what it actually measured | reproduced |
|---|---|---|
| 95.6 | one opinion **per FILE** — file copies counted as second opinions | 884/927 = 95.36% [93.81, 96.54] |
| 94.1 | **every ROW**, no deduplication | 956/1014 = 94.28% [92.68, 95.55] |
| 90.6 | every row, **on INVERTED labels** | 917/1014 = 90.43% [88.47, 92.09] |
| 89.2 | re-marks **inside one file** | 327/367 = 89.10% [85.50, 91.89] |
| **77.2** | **the ceiling computation with one 150-row sheet missing** | 115/149 exactly |
| 76.0 / 75.8 | **the ceiling** | 135/178 = 75.84% [69.05, 81.54] |

**Both alleged defects confirmed.** Nine duplicate file pairs collapse, taking 927 file-unit
repeat pages down to 178 sitting-unit ones — **95.4 → 75.8, a 19.5-point drop** (the standing
claim said ~16). And 90.6 reproduces *only* with labels inverted; the same recipe on corrected
labels gives 94.3. The inversion touched **1,168 rows** — every row of that dialect sitting on a
rejection.

**77.2 is not a better number than 75.8. It is 75.8 with one file missing.**

For scale: on this corpus, **always answering "reject" is right 61.5% of the time.**

### 3.3 The ceiling is two numbers, and the middle is where every decision is made

By distance from his own stated want-floor of 6 (denominator: 309 sitting-pairs carrying a score):

| | agreement |
|---|---|
| **\|score − 6\| ≤ 1** | 28/47 = **59.6% [45.3, 72.4]** |
| \|score − 6\| = 2–3 | 64/80 = 80.0% [70.0, 87.3] |
| **\|score − 6\| ≥ 4** | 169/182 = **92.9% [88.2, 95.8]** |

**Intervals do not overlap.** By band, the ends of the scale reproduce at ~90% and the 2–4 band
at 54.1% [38.4, 69.0]. Median score where he agreed with himself: **1**. Where he disagreed:
**4**.

> He is nearly perfectly consistent about pages he obviously loves or obviously hates, and close
> to a coin on everything in between — which is exactly the population the filter exists to sort.

### 3.4 It decays within a sitting, and that is free to fix

Raw, by depth in the sheet: rows 61–120 = 93.6% [87.4, 96.9]; **rows 121+ = 76.1% [70.5, 81.0]**.

⚠️ **Confound named and controlled**: only a large sitting can supply a deep rank. Splitting
**each sitting at its own median rank** and pooling: **early 88.2% [83.1, 92.0] vs late 76.6%
[70.3, 82.0]** — intervals still disjoint, and lower-or-equal in 6 of the 8 sittings large enough
to split. Under an independent calendar-day rule it is monotone: 100% → 88.0% [82.4, 92.0] →
79.7% [72.7, 85.3] → **67.3% [53.8, 78.5] past row 300**. Median minutes into the sitting when he
agreed: **9.7**; when he disagreed: **42.2** — a shift in the body, not a few late outliers
(p90 is 186 vs 202).

A second confound was checked and rejected: his want-rate rises with depth in four sheets and
falls in three, so depth is not a proxy for page quality.

**His entire recorded grading history is 78 minutes** — 683 rows, median inter-mark gap **3.0
seconds**. A 3-second glance at a 10-point scale is what produces the score's reproducibility, not
his taste.

### 3.5 Picture quality: direction consistent, **not confirmed**

Every cut points the same way and none separates. Pictures alike 87.1% [71.2, 94.9] vs pictures
differ 70.3% [54.2, 82.5]; blank-tile spread between a page's two pictures has median 3 when he
agreed and 6 when he disagreed. Permutation test over 20,000 shuffles: **p = 0.071**. A
handle-scramble control fired (the effect vanished), so the instrument is not manufacturing it —
but n = 68 and it does not separate. **Reported as unconfirmed.**

Coverage is the limit: only 75 of 178 repeat pages have any measured grid, and the walled/age-gate
quarantine intersects the repeat set on **one** page.

One thing the census does say on the wider corpus: his median score is 4 on grids with no blank
tiles and **2 on grids that are 9–12 tiles blank**. He is not blind to an empty picture; he is
just not consistent about it.

### 3.6 The reversal contributes essentially nothing — a controlled zero

Car, gym and motivation edits are a firm no now, reversing his own earlier 7s and 8s. That is a
changed mind, not noise, and it had to be separated out.

**It separates to nothing.** 148 of the 178 repeat pages carry a discovery keyword and **zero of
them are on a reversed subject.** The mechanism is plain: the reversal is about **edits** pages;
the repeat corpus is **meme** pages. The two superseded mark sets contribute **1 of 178** repeat
pages.

**Ceiling with the reversal: 75.8% [69.1, 81.5]. Without it: 75.7% [68.9, 81.4].**

This is a *controlled* zero, not an empty search. The boundary-safe subject rule was proved on 15
planted strings — `cartoon`, `cartooning`, `scarface`, `carousel`, `carnival`, `carpentry`,
`scarcity`, `gymnastics` must not fire; `car edit`, `cars`, `jdm`, `drift`, `gym physique
motivation` must — and it passed 15 of 15 while **the naive substring rule false-positived on 9 of
the 10 planted negatives**. Planted end-to-end into the real lookup it fired correctly, and
against real data it matched **136 real handles store-wide**. The instrument works; the overlap is
genuinely zero.

⚠️ **And the "63.3% vs 94.1%, 13 of 30" swing is not a ceiling figure at all.** It is a
*filter-accuracy* measurement on a different file, computed against a subject label that exists in
no mark file and no store. **The 94.1 in the ceiling family is a different quantity that happens
to share a value.** It should stop being quoted alongside the others.

Direction of his 43 disagreements: **21 want→reject, 13 reject→want, 9 untimed** — not the
one-way ratchet a pure changed-mind story predicts.

### 3.7 The score is the wrong instrument. This is the most actionable result.

Denominator: sitting-pairs where **both** viewings carry a 1–10 score.

| what he is asked for | reproduces (agent, n=67) | **independent re-derivation (n=37)** |
|---|---|---|
| exact 1–10 score | 49.3% [37.7, 60.9] | **54.1% [38.4, 69.0]** |
| 3 bands (1–3 / 4–6 / 7–10) | 83.6% [72.9, 90.6] | **81.1% [65.8, 90.5]** |
| **binary at 6 (his own floor)** | **88.1% [78.2, 93.8]** | **83.8% [68.9, 92.3]** |
| binary at 8 | 91.0% [81.8, 95.8] | **89.2% [75.3, 95.7]** |

The second derivation uses a different corpus (12 sheet files vs 26), a different key and no
session logic. **All four agree within overlapping intervals.**

Score-delta histogram: 0→33, 1→20, then a tail out to 8. **A body that reproduces within a point,
and a tail that does not reproduce at all.**

> **Ask him for a binary keep/drop, not a 1–10 score.** It reproduces ~30–35 points better, and
> the score's extra information is not information: 36.9% of all his scores are a `1` and 19.0%
> are a 9 or 10 — the scale is already being used as a three-way switch. If a middle is wanted,
> three bands cost ~4.5 points against binary and still beat the raw score by 30. And ask on
> **shorter sheets** — the same binary question past row 300 falls to 67.3%.

⚠️ The published "18.5%, 10 of 54" **does not reproduce**; the honest range is **32–54%**
depending on whether the bottom of the scale is counted. The direction of the claim is right and
stronger than its shape.

### 3.8 Which mark file to exclude — and it is not the one on record

| file | agrees with the pipeline | rows carrying words **he** typed |
|---|---|---|
| the `1296` FRESH100 export | **96.0%** | **0** (a reason column, empty on 100 of 100) |
| the `1257` FRESH100 export (+ a byte-identical second copy) | 97.0% | **0** — no reason field at all |
| four delivered sheets | 76.5–90.0% | 0 |
| the review-marks family | 68.9–71.2% | 26–294 |

**The file to exclude is the `1296` export.** Its joint table is the tell: 87 reject/reject, 9
want/want, 4 want→reject — **he never once wanted a page the judge rejected, 0 of 87** — and his
mark is written in the judge's own vocabulary. The `1257` export shares the surface, but for its
dialect "agreement with the pipeline" is *arithmetically identical* to "fraction he pressed GOOD",
so its 97% is evidence of a one-sided sheet, not of copying.

**Excluding both changes nothing: 134/177 = 75.7% [68.9, 81.4].**

⚠️ And the broader fact: **only 8 of 26 mark files contain a single word he typed.** The working
sheet's "why" box has never been filled — 0 non-empty of 56 present across two sheets.

### 3.9 The corpus: what 2,303 videos can and cannot answer

**Both edits cells are EMPTY, verified three ways** — every mark predates the existence of an
edits brief by **4h 46m 59s**; **0 of 9,332 mark rows on disk carry a mode field**; and the
undated sheet ids sit earlier still. They are reported empty rather than pooled into the memes
numbers.

⚠️ **A second limit, not in the brief and larger: this is not a good-versus-bad corpus.** His
marks cover 795 distinct pages, **443 of them scored below 6 — and 0 of those 443 were ever
downloaded.** Every page in the corpus scored 6–10. So the only contrast the pixels support is
*9s and 10s versus 6s and 7s among pages the filter already delivered and he already liked*.
**"What his good pages have in common against pages he rejected" is not answerable from this
corpus at all.**

**The noise floor, re-derived from 1,083 same-image repeat pairs, with κ beside it:**

| feature | full sheet | one tile |
|---|---|---|
| text placement | 75.8% [72.1, 79.2] κ .63 | 82.4% [79.0, 85.4] κ .71 |
| black bars | 67.9% [63.9, 71.7] κ .29 | 71.2% [67.2, 74.8] κ .47 |
| **cutting rhythm** | **52.6% [48.4, 56.8]** κ .32 | 77.8% [74.1, 81.1] κ .47 |
| subject spread | 75.1% [71.3, 78.5] κ .63 | 79.9% [76.3, 83.0] κ .68 |
| colour grading, as written | **3.1% [2.0, 5.0]** | 6.3% [4.5, 8.7] |

⚠️ **The "destroying the evidence made the instrument look better" shape is confirmed and now has
a mechanism with a number on it.** Rhythm rises 52.6% → 77.8% when the sheet is replaced by a
single frame — but over the same pairs the model's **modal share rises 0.412 → 0.745**, its answer
**entropy collapses from 1.844 to 1.166 bits**, the modal label changes from "slow" to "static",
and **chance agreement rises by +0.280 — larger than the raw agreement gain of +0.252.**
Chance-corrected, κ moves only 0.320 → 0.469. Nearly all of the apparent improvement is the model
collapsing onto a constant because one frame has no rhythm. Black bars behave the opposite way and
legitimately: modal share *falls* and κ genuinely rises.

**Model-read features: 80 comparisons, 0 survive.** Nominally 9 have a bootstrap interval clear of
zero — but a family-wise max-|z| null over 20,000 label permutations of the same 80 correlated
statistics produces **4.06 such "separations" per shuffle on average, 95th percentile 8, max 16.**
Observed: 9. The strongest single result has family-wise **p = 0.117**. **The model-read family as
a whole is indistinguishable from a label shuffle.**

**The one publishable result, and it is pixels rather than a model:** on **TikTok, memes**, his 9s
and 10s are letterboxed and his 6s and 7s are not.

| | good (9–10), n=93 | less (6–7), n=58 | family-wise p |
|---|---|---|---|
| share of videos with any bar | **70.0%** | **38.8%** | **0.0137** |
| page-median padding (shipped pixels) | **0.2272** | **0.0274** | **0.0318** |
| page-median padding (pre-resize frames) | 0.3833 | 0.1656 | 0.0691 |
| **p90 tail** | 0.2831 | 0.2472 | 0.81 — **does not separate** |

Reproduced by two independent pixel instruments and, second-derivation, by a rank correlation
across **all 193 TikTok pages**: ρ = **+0.247, permutation p = 0.0007**. **It is a step at 9, not a
gradient** — per-score medians 6: 0.020 · 7: 0.035 · 8: 0.031 · **9: 0.208 · 10: 0.259**. On
Instagram the same feature is **saturated at 1.0000 vs 1.0000** and carries nothing (ρ = −0.007).

**Every inherited figure reproduced**, including the two that were refutations: "2 of 5 videos are
a single still" → **1.50% [0.86, 2.61] / 0.93% [0.56, 1.56]**, and "47.5% already square" →
**4.38% [3.17, 6.03] / 10.31% [8.87, 11.94]**.

### 3.10 Where his addresses actually come from

| route | share of 12,938 addresses |
|---|---|
| **Spotify** (including Spotify→Instagram resolution) | **60.62% [59.77, 61.46]** |
| TikTok page funnel | 22.80% |
| Instagram page funnel | 9.59% |
| Twitch | 4.63% |
| everything else | 2.36% |

**By month it is starker.** August produced 8,247 addresses: **Spotify 83.97% [83.16, 84.75]**;
the page funnel, both platforms, **15.63% [14.86, 16.43]**.

**So: no, the page funnel is not where his emails come from.** It is a third of the lifetime file,
a sixth of the current month, and the most expensive third. Spotify buys addresses at **$1.21 per
1,000**; the shipped Instagram page funnel at **$78.53 per 1,000** — 65×.

⚠️ **And the published $137.31 is not a measurement.** It is `$3.58 ÷ 0.0261` — one dollar figure
divided by a carry rate, the "38× gap" being `1/carry` restated. It also used a **mixed
denominator**: the store holds two populations under one campaign label, and separating them
gives carry rates whose intervals are **disjoint by 12.7×**:

| population | pages | carry rate | $/1,000 addresses |
|---|---:|---|---:|
| shipped funnel | 4,240 | **3.96% [3.42, 4.59]** | **$78.53** |
| big-page harvest | 1,604 | **50.44% [47.99, 52.88]** | **$4.01** |

And carry rises monotonically with page size: **<1k followers 12.5% → 1k–10k 28.9% → 10k–100k
46.5% → 100k–250k 49.0% → 1M+ 58.1%.** Three independent instruments cluster at **$78–82**;
$137.31 should be retired.

**Approval by discovery surface reproduces to the digit**, and the surfaces are disjoint (0 of 119
graded handles carry more than one):

| surface | approval | share of the 14,108-handle walk |
|---|---|---:|
| reels | 82.4% [66.5, 91.7] | **3.3%** |
| search | 77.8% [54.8, 91.0] | 2.8% |
| **seed** | **38.6% [25.7, 53.4]** | **83.4%** |
| hashtag | 34.8% [18.8, 55.1] | 10.5% |

⚠️ **"No pagination" on reels is wrong about the surface and right about the caller.** The client's
own signature already takes a cursor; the single production caller never passes it and never reads
the returned cursor, while the hashtag channel in the same module *does* walk one. What is true is
that the endpoint **saturates**: measured live on the successor, page 1 gives 12 accounts, page 2
adds 7, page 3 adds **0** — pages 2 and 3 byte-identical — **while still reporting `has_more:
true`.** So vocabulary is the lever, but a second page per phrase is free money the caller
currently declines.

**Supply versus consumption: 8,699 staged addresses against zero recorded consumption**, with a
firing control. The honest statement is not "he is oversupplied" — it is that **this repository
cannot measure it**, because sending happens elsewhere and writes nothing back. No instrument here
would ever show it.

### 3.11 His own 130 hand-picked pages, run through the filter

He hand-picked and supplied 130 edit pages by URL — 66 TikTok, 64 Instagram. **They are all
wants, positive by construction**, which makes them useless as an accuracy denominator and
perfect as a disagreement test: every rejection is a rule disagreeing with him.

**Denominator:** 130 found, 130 resolvable, **128 actually run** (two Instagram pages have no post
counts; one of those is private, which is a third state and never a rejection). Captured filter
input already existed on disk, so **no vendor call was made**.

| rule | rejects, of his own picks |
|---|---|
| **recency / `stale`** (180 days) | **19 of 66 TikTok = 28.8% [19.3, 40.6]** |
| `photo_heavy` (10% photo cut) | 6–14 of 62 Instagram (9.7% [4.5, 19.5] – 22.6% [14.0, 34.4]) |
| `too_few_posts` (floor 13) | 4 of 62 Instagram = 6.5% [2.5, 15.4] |
| TikTok language | **0 of 66** — control proves the rule alive |
| green screen | **0 of 66** — max observed 0.0114 against a bar of 0.18; control proves it alive |

> **22.3% [16.0, 30.2] to 28.5% [21.4, 36.8] of the pages he personally chose are rejected by a
> free code rule before any model is consulted** — and the single biggest disagreement is
> **recency**, which throws out nearly three in ten of his own TikTok picks. Median captured-post
> age of his picks is 90 days; p90 is 316. The 19 stale calls are an **upper** bound (the
> capture kept only the first video over 4 seconds); the 47 not-stale calls are definitive, and
> the stale verdict is confirmed twice — by post timestamp and by the epoch encoded in the post
> id, agreeing 66 of 66 with worst drift 0.633 days.

**The remaining 93–101 (71.5%–77.7%) rest on a model call and are UNRESOLVED** — none was made.

⚠️ **Six rules are DEAD in shipped code, each proven by a planted control**: TikTok's talking-head
rule (its input is hard-assigned `None`), its template-overlay rule (OCR is skipped, so the text
list is always empty), its share-per-play floor (disabled by a sentinel and null config), the
operator's own rules reached from TikTok (three fields absent from the facts dict), the
short-caption floor (its minimum is 0), and Instagram's language gate (the config key is absent).

⚠️ **And the shipped config is `memes` mode on BOTH funnels** — while these 130 are *edit* pages.
The edits-mode rule suspensions are therefore not in force as configured.

⚠️ **A prior round's clean bill of health on this set was a null result.** It passed **zero posts**
to the judge and got "unjudged" 130 times. That reads like a pass and is not one.

**The closed-subject-list cost.** Both published figures reproduce exactly — **52.6% [37.3, 67.5]
Instagram and 52.7% [42.6, 62.5] TikTok** of his 9s-and-10s show a subject outside the three named
— and `tennis` is **0 of 8,571 handles**, exactly as he predicted. An independent boundary-safe
re-derivation gives 23.7%/25.8%, or 42.1%/40.9% with generic tokens dropped: **the direction
replicates on every method; the magnitude is method-dependent across 24%–53%.** On his own 130 a
closed-list rule rejects **25 of 129 = 19.4% [13.5, 27.0]**, every one classed "other" —
⚠️ **but that figure has one derivation, not two**; the second derivation disagreed and is
reported as a failure rather than averaged away.

**Car, gym and motivation reject 8 of 129 = 6.2% [3.2, 11.8] and stay rejected. That is his stated
taste, not a defect.**

⚠️ **The list was opened by a concurrent round while this one ran.** The edits rubric now reads
that the three subjects were named as *examples, not the whole list*, and that a subject outside
them is not a reason to reject. Verified live at the byte level rather than read from source, and
car/gym/motivation still reject. **Two other funnel modules also moved mid-round** (one grew 107
lines), so the line numbers above were re-derived by search at the end rather than quoted from the
start.

---

## 4. What was refused, and why

**No production file was written.** No store, config, doc, test, tool or exemplar pack was
touched. The one live listening service on this machine was left alone; nothing was killed.

**Two zeros were discarded rather than reported.** A model-read blindness sweep planted ±0.20 into
64 cells and found **2 cells blind in both directions**; their zeros are discarded. The one-sided
version of that same sweep called 9 cells blind and **was itself wrong** — a ceiling-saturated cell
needs the bump pushed the other way.

**The picture-quality result was withheld** (§3.5): direction consistent across five cuts, scramble
control fires, p = 0.071 — reported as unconfirmed rather than published.

**Text amount was not measured at all.** No OCR binary is installed and no stored artefact covers
this corpus. Reported absent rather than estimated.

**No outreach mechanics are proposed anywhere in this report.** Finding an address is lead data;
using it is not.

---

## 5. What I got wrong

**My own first instrument produced a clean silent zero.** Cross-checking the graded-pages file, I
guessed the score column name, matched none of the real ones, and reported **0 pages scoring ≥6**
in a file whose name promises exactly that. The corrected parser carries controls proving it reads
a real score and refuses both an empty cell and the string `n/a`. Had I trusted the first run I
would have published that the answer key was empty.

**A sub-agent's pad detector was blind and its own controls hid it.** Four synthetic controls
passed while the detector returned a **constant 0.0199 on 1,579 of 2,303 tiles**, including tiles
that are 68–73% letterbox. Cause: the real tiles carry ~10px of white sheet gutter, so 13 of 283
pixels in every black row break a flatness rule — **the synthetics had no gutter and validated a
branch the real data never takes.** Rebuilt with a de-gutter step and re-controlled, including
two controls built from *real* corpus tiles rather than synthetics.

**A stored "single still" flag disagrees with the pixels it describes** — 3 of 5 sampled videos
flagged still show two or more distinct signatures on re-cut tiles. The disagreement runs one way,
so **1.50% and 0.93% are upper bounds** — which only strengthens the refutation they belong to.

**Three of the brief's own inputs are wrong**, and I inherited them until I checked:
- **"~9,728 mark rows across the delivered sheet directories."** The delivered sheet directories
  hold **683 rows across 12 non-empty files** (15 exist, 3 are zero bytes). The ~9,3xx figure is
  the all-sources walk including `ground_truth/` and `scratch/` — a different denominator.
- **"448 pages he personally graded 6+."** 448 real rows (450 minus 2 section headers), but only
  **298 carry a number**; the other **150 are picks he never scored**. The 141 nines-and-tens is
  correct and is 47.3% [41.7, 53.0] **of 298**.
- **"18.5%, 10 of 54"** for score reproduction does not reproduce (§3.7).

---

## 6. Money and safety

**$0.00 spent**, by the round's own counter; no model call was made. The ledger is not cited for
this, by design.

**No store, config, or ground-truth file was read into a write path, and none was modified.** A
recent round deleted 56 rows another live round had paid for and manufactured a false finding from
the gap; this round wrote nothing outside `scratch/bl1493_*`.

**Process identity came from the listening-port table, never a command-line match** — a filter here
once matched its own command line. One local service was listening throughout and was left
running.

**No address appears in this report in any form**, not even redacted. Address-bearing work reported
counts and aggregate domains only. Of the 448 graded pages, **40 carry an address (8.9%)** and
**399 of 448 (89.1%) are reachable only by direct message** — his best pages overwhelmingly have no
address to find.

---

## 7. What to do next — ranked, with the arithmetic

1. **Decide whether his marks should gate anything.** They currently gate nothing (§3.1). Either
   wire them into a decision — at which point the 75.8% ceiling starts to matter — or stop
   producing review sheets on the theory that they improve the filter. Right now the sheets cost
   his time and change no output. **This is the only item that changes what every other number in
   this report is worth.**
2. **Replace the 1–10 score with a keep/drop.** Reproducibility 49–54% → 84–88%, measured two ways
   on two corpora (§3.7). Costs one sheet change; buys ~30 points of answer-key quality.
3. **Cap sheets at ~150 marks.** Agreement runs 88% early and 67% past row 300 (§3.4). Free.
4. **Record one outcome column.** Nine exist and all are empty on 72,956 rows (§3.1). Until one is
   filled, no accuracy figure here — his or the machine's — has ever been checked against reality.
5. **Stop tuning model-read visual features.** 80 of 80 fail family-wise correction; rhythm and
   colour grading sit at 52.6% and 3.1% self-agreement (§3.9). Measure letterboxing **in pixels**
   instead — it is the one thing that survives, and it is free and deterministic.
6. **Look at the recency rule before any other filter change.** It rejects **28.8% [19.3, 40.6] of
   the TikTok pages he chose by hand** (§3.11) — the largest single disagreement between the
   machine and the operator that this project has measured, and it is a free code rule with one
   number in it. His own picks have a median captured-post age of 90 days against a 180-day bar,
   so the rule is not obviously wrong; but a rule that discards three in ten of his personal
   picks deserves a decision rather than a default.
7. **Delete or repair the six dead rules** (§3.11). Each has an input that is hard-assigned
   `None`, a skipped OCR step, a disabling sentinel, an absent config key or a zero threshold.
   They cost nothing to run and make the rule inventory a fiction.
8. **If address volume is the goal, page size is the lever**, not page count: carry runs 12.5% at
   <1k followers to 58.1% at 1M+, and the big-page harvest converted at **50.4% against the shipped
   funnel's 3.96%** (§3.10).
9. **Pass the cursor on the reels call.** The parameter already exists and is never supplied; the
   surface saturates at ~19 accounts per query, so the gain is bounded — but a second page per
   phrase costs one billed request and is currently declined for free.
10. **Retire $137.31.** It is a division, not a measurement, and it used a mixed denominator
   (§3.10). The defensible figure for the shipped funnel is **$78.53 per 1,000 addresses**.

---

## 8. Paths to open

| what | where |
|---|---|
| the marks-gate-nothing verification | `scratch\bl1493_marks_are_writeonly.json` |
| the ceiling, all recipes and decompositions | `scratch\bl1493_ceiling_ALL.json` |
| the independent score-vs-verdict cross-check | `scratch\bl1493_scorevsverdict_crosscheck.json` |
| the graded-pages cross-check (448 / 298 / 141) | `scratch\bl1493_gradedcsv_crosscheck.json` |
| corpus measurements, noise floors, permutation nulls | `scratch\bl1493_corpus_*` |
| the economics and route attribution | `scratch\bl1493_economics_*` |
| the free-range findings | `scratch\bl1493_free_*` |
| the only correct reader for his marks | `tools\mark_reader.py` |

**Defects named and deliberately left in place:** the outcome-marking entry point that has never
run; the vision verdict consumed at decision time and persisted nowhere; the graded-pages export
that mixes 150 unscored picks into a file whose name promises scores of 6 and above; and five
modules pricing calls 13.1% below the rate the client actually charges.
