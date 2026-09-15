# BL-1560 — the hashtag hypothesis is refused, and the lever is somewhere else entirely

**Picking more specific hashtags does not get you to $5 per 1,000, because hashtag shape does
not move the address rate at all.** Measured two independent ways. On the 572 tags this project
has already paid for, SPECIFIC tags return **3.01% [2.86–3.17]** and GENERIC words return
**3.03% [2.14–4.27]** — dead level, and with the tag treated as the unit of randomisation the
difference is **+0.02 points [−1.25, +1.13]**. On a fresh interleaved Instagram walk of 21 tags
built for this question, all three arms overlap: named teams 2.65%, named players 4.66%, generic
words 3.87%. **And the 9x spread in your own five-tag table is not evidence of anything: I
simulated it, and if shape did nothing at all a spread that large appears 32.0% of the time.**
One walk in three produces it by chance. What the walk DID find is that the price is governed by
something you have not been thinking about: **in the first half of the walk 1.6% of accounts
needed a paid profile and the price was $1.11 per 1,000; in the second half 88.4% did and the
blended price was $9.86.** Same tags, same session, one hour apart. **The free bio route being
open or shut moves the price ~9x. The vocabulary moves it by nothing I can measure.** If you
want the number down, that is the lever — not "Steph Curry edit".

**What to walk next, since you asked for tags:** nothing on the basis of shape. The ranked table
in §4 is real and the top of it is worth using — `#creededit` at 16.19%, `#lakersedit` 15.62%,
`#michaeljordanedit` 12.82% — but rank them **by recorded yield, which this project now has for
572 tags**, not by whether the word is a name. And **treat a top-of-table tag as a coin-flip
until it has been walked twice**: within a single class the tags already run from 0% to 16%.

---

## 1. What this project is, for a reader with no context

ClippersHQ finds video editors and meme-page operators on TikTok and Instagram and collects the
email addresses in their bios, so a human can offer them paid clipping work. It buys data from
two vendors: **HikerAPI** for Instagram (`ig_api.cost_per_call_usd` = **$0.00069064** per call)
and **LamaTok** for TikTok (`api.cost_per_call_usd` = $0.00060000). Those two numbers are 15.1%
apart and reading the wrong one once let a $3.00 cap spend $3.45, so every Instagram figure here
is read from the named key and stated as such.

The operator's hypothesis for this round, in his words: *"Don't do warrior edit. Do Steph Curry
edit, or some basketball or football star. Cobra Kai edit is very specific and it's getting a lot
of emails. Spider-Man edit, Avengers edit. Be more specific. The hashtags are the one that is
going to make this cheaper."* The evidence offered was five tags walked in one hour spanning 9.3x.

**This round was asked to turn that into a measurement rather than confirm it.** It is refused,
and the refusal is the useful part.

## 2. Safety, money, and the cap that had to bind

| | |
|---|---|
| all nine stores backed up | sha256-verified, bodies found **by shape** |
| corruption controls | **all six fire** on damage planted on purpose |
| `spend.json` | list at `runs`, 37,966 rows |
| `clip_seen.json` | **bare list**, 2,193 |
| `tiktok_pages_seen.json` | dict at `pages`, **3,270** (a dict-only reader reports 3) |
| `master_leads.csv` | 73,001 rows × 72 columns at round start |
| unit used | `ig_api.cost_per_call_usd` = **$0.00069064**, by named key |

The backup wrapper **counts the controls in the source** rather than trusting the module's own
docstring, which says "THE FIVE CORRUPTION CONTROLS" and has six — the sixth (a wrapped store
must report its payload, not its wrapper) was added later and the comment was never updated.

**THE CAP BOUND, which is the only proof a cap works:**

    WALK OVER: CAP: REFUSED: $0.0007 for a hashtag call would take this run to $0.7003,
    over the $0.70 cap (1013 calls billed so far)

| item | calls | spend |
|---|---|---|
| the interleaved walk | 1,013 checkpointed + **1 orphaned by my own error** | $0.70031 |
| deliverability re-fetch | 71 | $0.04904 |
| **round total** | **1,085** | **$0.74935** of a $1.00 hard maximum |

⚠️ **AND IT IS BOOKED, WHICH IT HAS NOT BEEN FOR THREE ROUNDS.** The walker meters at the
wrapper with its own `Budget` and never writes to `spend.json` — correct for *attributing* a
round's spend, and not the same thing as *recording* it. BL-1557 spent $0.26866 that never
reached the ledger. Measured here before booking, **the ledger delta across the entire walk was
exactly zero rows.** Both legs are now booked through `record_aux_spend` with
`ig_cost_per_call` passed **by name** (its `cost_per_call` argument defaults to LamaTok's rate,
which is how 6,642 ledger rows were once booked 13.1% cheap), and each booking was verified to
move the ledger by exactly one row of exactly the expected amount:

    rows 37,966 -> 37,967   ig_spent_usd 45.899722 -> 46.600031   (+0.700309)
    rows 37,967 -> 37,968   ig_spent_usd 46.600031 -> 46.649066   (+0.049035)

### The leak scan fired, and here is why this was published anyway

The pre-publish scan is built from **both** corpora — the lead store (12,792 addresses, 72,917
handles, *including this round's own 71*) and this round's walk rows — and every detector is
proved on a planted control before it is trusted. It reported:

    HIT  {'a real creator handle': 6}      VERDICT: NOT publishable as-is

**All six were read by hand. All six are ordinary English words** that also happen to be
somebody's handle in a corpus of 72,917: *evidence*, *basketball*, *comic*, *shows*. Every
`@` in the whole file is the endpoint marker in `<stem>edit@v2` — **not a handle** — and
**zero addresses from either corpus appear** (checked directly, not inferred). **6 of 6 false
positives.**

**And writing that paragraph raised the count from 6 to 10**, because naming the four
false-positive tokens puts four more of them in the file. A detector that fires on its own
post-mortem is matching English, not handles. The count on the published file is therefore
**10, all four distinct tokens ordinary words, still zero addresses.**

BL-1559 hit the same wall — 8 of 8 ordinary words — published correctly and *never wrote down
why*, leaving a red receipt beside a published file with no explanation. That is the half being
fixed here. The detector is deliberately **not** loosened in the same round that publishes
through it: a relaxed version would never have been tested against a real leak.

## 3. Part 1 — 572 tags, already paid for, ranked for the first time

`email_harvest_tags.json` holds **572 tags** — 489 on the plain endpoint, 83 on v2. Every one was
bought. Nobody had ranked them. Pooled across all of them: **2,247 / 73,009 = 3.08% [2.95–3.21]**.

⚠️ **THE DENOMINATOR IS NAMED, AND IT IS NOT "ACCOUNTS TOUCHED".** Read out of
`email_harvester.py:596-617` rather than assumed: the loop `continue`s on an account id already
held **before** `summary["authors"] += 1`. So `authors` counts accounts **kept** and `emails`
counts how many of those carried an address that passed the deliverability guard. That is the
same shape as the operator's own table (79 new accounts → 11 addresses).

⚠️ **AND THE LEDGER IS TIKTOK, WHICH THE BRIEF DID NOT SAY.** `email_harvester.py` constructs a
`LamaTokClient` and its own docstring reads *"This is a TikTok tool and the unit is always passed
explicitly."* The operator's five-tag walk, the $13.94 price and the $5 target are all
**Instagram**. So Part 1 is a TikTok measurement, and whether it transfers is a hypothesis — which
§6 tests, and answers *no*.

**A pooled number hides the dead tags, so they are reported first: 105 of 543 usable tags
(19.3%) returned accounts and ZERO addresses, spending 7,101 accounts for nothing.**

### His own five tags, re-walked independently, do not reproduce the 9x

| tag | his walk | this ledger | shape |
|---|---|---|---|
| `#cobrakaiedit` | 13.9% | **4.90%** (7/143) | named title |
| `#wolverineedit` | 15.4% | **3.25%** (5/154) | named character |
| `#magnetoedit` | 4.3% | **3.73%** (6/161) | named character |
| `#saulgoodmanedit` | 4.3% | **4.17%** (7/168) | named character |
| `#warrioredit` | **1.5%** | **4.35%** (6/138) | generic word |

His spread is **9.3x**. The same five tags on an independent walk of comparable depth span
**1.5x**, the rank order is scrambled, and **`#warrioredit` — his worst tag, the one he named as
the thing not to do — comes third of five here.**

## 4. Does shape predict yield? No, and here is the table that says so

Hand-classified, **not** by heuristic: a rule that called anything unfamiliar a "name" would
manufacture the finding under test, and every tag here is lowercase and unpunctuated so there is
no signal to key on anyway. All 572 were read and assigned individually; the 26 genuinely
contestable stems (`law`, `kid`, `killer`, `robin`, `bull`, `river`, `henry`, …) are listed with
their reasons in `scratch/bl1560/bl1560_shapes.py` and the contrast is re-run without them.

⚠️ **A normaliser bug hid 83 tags first time round.** It stripped a trailing `edit`/`edits` and
nothing else, so every v2 row — spelled `<stem>edit@v2` — matched nothing and fell into
UNCLASSIFIED. The endpoint marker now comes off first.

**Plain endpoint, tags with n ≥ 30:**

| shape | tags | address rate |
|---|---|---|
| **NAMED TEAM** | 24 | **5.29% [4.49–6.23]** |
| NAMED TITLE | 151 | 3.68% [3.37–4.01] |
| GENERIC WORD | 10 | 3.03% [2.14–4.27] |
| NAMED PERSON | 146 | 2.64% [2.38–2.93] |
| NAMED CHARACTER | 157 | 2.36% [2.13–2.61] |
| **SPECIFIC (all four named shapes)** | 478 | **3.01% [2.86–3.17]** |
| **GENERIC** | 10 | **3.03% [2.14–4.27]** |

**SPECIFIC vs GENERIC: the intervals overlap and the point estimates are indistinguishable.**
His hypothesis, as stated, is not supported.

**But something narrower is real, on TikTok.** Splitting the team tags by league:

| class | rate |
|---|---|
| **NBA TEAM** | **9.33% [7.61–11.39]** (85/911, 8 tags) |
| NBA PLAYER — *his "Steph Curry edit"* | 3.14% [2.60–3.80] (39 tags) |
| SOCCER CLUB | 3.05% [2.32–4.00] (16 tags) |
| GENERIC — *his "warrior edit"* | 3.03% [2.14–4.27] (10 tags) |

NBA team tags separate from **both** controls, and **leave-one-out confirms it is not one tag**:
dropping any single member leaves the lower bound between 6.57% and 8.26%, always clear of the
player arm's 3.80% ceiling.

### The three confounds, measured rather than waved at

**TAG SIZE — not the explanation.** Spearman rho of rate against accounts-per-tag is **0.070**
across 543 tags. The size quartiles are flat and non-monotonic (2.71% / 2.74% / 2.98% / 2.67%).
Median tag size is **96** for specific tags and **102** for generic ones, so shape and size are
not entangled in this corpus.

**BUCKET ORDER — this is where most of the apparent shape effect goes.** `NAMED TITLE` is mostly
film, `NAMED CHARACTER` mostly anime, `NAMED PERSON` mostly athletes, so the shape table may be
the bucket order wearing a new name. Re-derived here on the plain endpoint: FILM/TV 3.61%
[3.31–3.94], COMIC 3.45%, SPORT 3.08%, ANIME 1.87% [1.63–2.14]. **Tested WITHIN bucket, shape
stops separating**: inside FILM/TV, title vs character **overlaps**; inside COMIC, **overlaps**.
It survives only as TEAM > PERSON inside SPORT, which is the NBA finding again.

⚠️ **CLUSTERING — AND THIS CORRECTS MY OWN FIRST ANSWER.** A Wilson interval on pooled accounts
assumes the accounts are independent draws. They are not: they arrive in tags, and tags vary
enormously — `#lebronedit` and `#stephcurryedit` are the same class on the same platform in the
same session and came in at 9.6% and 1.7%. I first reported pooled intervals. Re-run as a cluster
bootstrap over tags (20,000 resamples, seed fixed at 1560), the intervals widen **1.1–1.7x**:

| contrast | difference, tag as the unit | verdict |
|---|---|---|
| NBA TEAM − NBA PLAYER | **+6.17 pts [+3.08, +9.15]**, P(≤0)=0.000 | **separates** |
| NBA TEAM − SOCCER CLUB | +6.29 pts [+3.18, +9.28], P(≤0)=0.000 | separates |
| **SPECIFIC − GENERIC** | **+0.02 pts [−1.25, +1.13]**, P(≤0)=0.488 | **does not separate** |

### And his five-tag spread needs a null before it needs an explanation

The ledger's per-tag rates already run from 0% to 16.19% **within a single class**. So: if shape
did nothing at all, how often would five tags drawn at random span 9.3x? Simulated 100,000 times,
drawing five real tag denominators and re-drawing their addresses binomially at the pooled 3.01%
so that shape *cannot* matter:

    draws where the smallest of five returned ZERO addresses : 31,158 (31.2%)
        -> an INFINITE spread, with no shape effect at all
    among the rest: median spread 3.63x, p90 6.38x, p99 9.50x

    P(spread >= 9.27x | SHAPE DOES NOTHING) = 32.0%

**A 9.3x spread across five tags is the ordinary scatter of this surface.** It needed no cause.

### One more thing the ranking says, pointing the opposite way to "be more specific"

A dead tag wastes an entire walk. **Generic words never produced one** (0 of 10, though the
interval is wide at [0.0–27.8]) and NBA teams never did either (0 of 8). **Named persons waste
17.1% of tags and 15.2% of the accounts spent on them; named characters 17.2% and 15.5%.** Being
more specific *raises* the chance a tag is a dud.

## 5. Part 2 — the candidates, and why existence was not checked separately

88 candidates across three arms, **interleaved by construction** A/B/C/A/B/C so the walker
consumes them alternating and drift cannot favour an arm: 30 NBA franchises, 30 current NBA
players (led by `stephcurry`, his own example), 28 ordinary English words (led by `warrior`, his
own example). No real-fighter tags (1.21% [0.68–2.15] across three measurements) and no
`caredit`, which he has said to leave alone.

⚠️ **Existence was NOT verified in a separate pass, deliberately.** On Instagram the existence
check and page 1 are *the same paid call*, so a separate pass pays twice for one answer. Every
name used is a real franchise, a real player or an ordinary word — none is generated, which is
the failure mode where 35 of 35 "fresh" tags returned server errors.

## 6. Part 3 — the interleaved walk, and the TikTok finding does NOT transfer

21 tags, **exactly 7 per arm**, 126 pages, 1,786 accounts kept, 574 skipped as already held
(before their bio was bought, which is the whole saving). **0 pages came back HTTP 200 with an
empty list.** Saturation was decided by body hash, never `has_more`.

**Four denominators, counted separately:** 1,013 sections · 3,018 slots · 3,018 authors ·
**2,363 distinct account ids**. Reading slots as accounts would overstate by 1.28x.

| arm | tags | addresses / accounts | rate | cluster interval |
|---|---|---|---|---|
| A NBA TEAM | 7 | 6 / 226 | 2.65% [1.22–5.67] | 2.71% [1.07–4.31] |
| B NBA PLAYER | 7 | 33 / 708 | 4.66% [3.34–6.47] | 4.46% [1.83–9.21] |
| C GENERIC | 7 | 33 / 852 | 3.87% [2.77–5.39] | 3.91% [1.66–7.52] |

    B_NBA_PLAYER minus C_GENERIC   +0.50 pts [-4.29, +5.70]  P(<=0)=0.429  DOES NOT SEPARATE
    A_NBA_TEAM   minus B_NBA_PLAYER -1.84 pts [-6.72, +1.61] P(<=0)=0.781  DOES NOT SEPARATE
    A_NBA_TEAM   minus C_GENERIC   -1.26 pts [-5.10, +1.57]  P(<=0)=0.794  DOES NOT SEPARATE

**Nothing separates.** And the TikTok NBA-team finding **inverted**: teams were the best class
there and are the *worst* arm here. On Instagram the team tags are also tiny — `#bullsedit`
returned 6 accounts, `#miamiheatedit` 4 — so even had the rate held there is no supply behind it.

**Per tag, including the five that delivered nothing:**

| tag | arm | pages | new accounts | addr | NET-NEW | stopped because |
|---|---|---|---|---|---|---|
| `#lebronedit` | player | 12 | 229 | 22 | 21 | pages exhausted |
| `#motivationedit` | generic | 12 | 199 | 12 | 12 | pages exhausted |
| `#gymedit` | generic | 2 | 42 | 7 | 7 | target reached |
| `#mindsetedit` | generic | 12 | 146 | 6 | 6 | no `next_page_id` |
| `#stephcurryedit` | player | 12 | 238 | 4 | 4 | pages exhausted |
| `#legendedit` | generic | 11 | 211 | 4 | 4 | cap reached |
| `#lukaedit` | player | 12 | 172 | 3 | 3 | pages exhausted |
| `#giannisedit` | player | 3 | 33 | 2 | 2 | no `next_page_id` |
| `#grindedit` | generic | 4 | 29 | 2 | 2 | no `next_page_id` |
| `#hustleedit` | generic | 2 | 23 | 2 | 2 | no `next_page_id` |
| `#knicksedit` | team | 7 | 68 | 2 | 2 | no `next_page_id` |
| `#lakersedit` | team | 5 | 63 | 2 | 2 | no `next_page_id` |
| `#celticsedit` | team | 2 | 23 | 1 | 1 | no `next_page_id` |
| `#durantedit` | player | 2 | 5 | 1 | 1 | no `next_page_id` |
| `#jokicedit` | player | 2 | 8 | 1 | 1 | no `next_page_id` |
| `#netsedit` | team | 3 | 12 | 1 | 1 | no `next_page_id` |
| `#bullsedit` | team | 2 | 6 | **0** | 0 | no `next_page_id` |
| `#miamiheatedit` | team | 2 | 4 | **0** | 0 | no `next_page_id` |
| `#tatumedit` | player | 3 | 23 | **0** | 0 | no `next_page_id` |
| `#warrioredit` | generic | 10 | **202** | **0** | 0 | no `next_page_id` |
| `#warriorsedit` | team | 6 | 50 | **0** | 0 | no `next_page_id` |

**5 of 21 tags delivered nothing, and they consumed 16.0% of the accounts kept.**
`#warrioredit` alone burned 202 accounts for zero — on his walk it returned 3.

## 7. Part 4 — the price, every division written out, and the finding that matters

    calls                       1,013 checkpointed + 1 orphaned      = 1,014
    spend    = 1,014 x $0.00069064                                   = $0.70031
    addresses raw                                                         72
      held, SAME handle              0   ($0 -- memory)
      held, DIFFERENT handle         1   ($0 -- duplicate)
      NET-NEW                                                             71
    $ per 1,000 NET-NEW = $0.70031 / 71 x 1000                       = $9.86

    seconds per account   median 3.37   p90 3.96        (median and tail, never a mean)

**But the blended figure is two different worlds, and the split is the round's real finding:**

| | accounts | needing a PAID profile | share | $ per 1,000 net-new |
|---|---|---|---|---|
| first half | 797 | 13 | **1.6%** | **$1.11** |
| second half | 989 | 874 | **88.4%** | — |
| blended | 1,786 | 888 | 49.7% | **$9.86** |

Same vocabulary, same session, roughly an hour apart. **The free bio route drained mid-walk, and
that alone moves the price about 9x — far more than any difference between hashtags.** The
$13.94 model assumes every account's profile is bought; when the free route serves, the accounts
cost nothing and only the hashtag pages are billed.

**Charged and empty: 77 of 888 paid profile calls = 8.67% [6.99–10.70]**, overlapping the
6.03% [3.80–9.44] prior on a denominator three times larger.

**Deliverability**, checked with the bio present (an empty bio rejects every address for
`not_a_verbatim_substring_of_the_bio`, a zero a planted control once exposed), and with both
controls separating:

| | |
|---|---|
| MX resolves | **66/71 = 93.0% [84.6–97.0]** |
| sourcing — verbatim in the account's own bio | 71/71 = 100.0% [94.9–100.0] |
| `address_ok`, both judgements | 65/71 = 91.5% [82.8–96.1] |
| role inbox (flagged, never dropped) | 0/71 |

## 8. Part 5 — the unit is editors, and the interval is the honest part

`editor_gate` fires on **16 of 71 = 22.54% [14.37–33.52]**.

    $ per 1,000 NET-NEW ADDRESSES = $0.70031 / 71 x 1000 = $9.86
    $ per 1,000 LIKELY EDITORS    = $0.70031 / 16 x 1000 = $43.77
      at the interval's edges     : $29.43 (optimistic) to $68.62 (pessimistic)

⚠️ **SAY WHAT THE INTERVAL PERMITS.** It permits anywhere from 14.4% to 33.5% of rows being
editors, which is the difference between $29 and $69 per thousand. BL-1557 measured 13.33%
[5.31–29.68] and BL-1548 measured 29.37% [27.57–31.23]; **those two do not agree and this round
does not settle them.** The gate's honest accuracy is precision 87.65% [78.74–93.15] and recall
94.67% [87.07–97.91] on n=240 — **not** 97.56%, which was one sample of 120 while a disjoint 120
of the same gate scored 79.41%. It is **not** validated here against `lead_kind` or `verdict`:
`writer.py:363-367` returns CLIPPER for any `tt:`/`ig:` source regardless of the bio and says so
in its own docstring, so two guesses agreeing would not be evidence.

By arm, and the one place the arms did differ: team 4/6 = 66.67% [30.00–90.32], generic
8/33 = 24.24% [12.83–41.02], player 4/32 = 12.50% [4.97–28.07]. **At n=6 that is a hint, not a
finding**, but it is the only signal in the round that points at doing something differently, and
it points at teams — which produced the *fewest* addresses. Worth one round's attention.

## 9. The output

**71 net-new addresses written to `master_leads.csv`**, backup re-hashed and compared *before* the
write, counts asserted with a CSV parser after it:

    rows 73,001 -> 73,072  (+71, expected +71)   OK
    cols 72 -> 72  UNCHANGED
    C0 control bytes in the new rows, checked BEFORE writing : 0
    workbook 'Emails' 2,072 -> 2,143 (+71); other sheets unchanged, read back from disk

Independently re-counted afterwards with a second parser: **73,072 rows × 72 columns.**

### The suite, and what running it costs the ledger

    FAILED -- 25 red of 480 suite(s)   (2210.7s)

**25 red, against BL-1559's 25, attributed PER SUITE NAME and never by subtracting totals:
zero newly red, zero newly green.** No production code was changed by this round; the only
edit outside `scratch/bl1560/` is the one-line backup-path fix in §10.7.

⚠️ **AND THE SUITE RUN CHARGED THE PRODUCTION LEDGER, EXACTLY AS BL-1559 MEASURED.** Snapshotted
before and after, as required:

    rows    37,968 -> 38,180        (+212)
    total   66.864337 -> 66.902607  (+0.038270)
    vision  10.710447 -> 10.748717  (+0.038270)
    ig      46.649066 -> 46.649066  (+0.000000)

**+212 rows and +$0.038270 of `free_judge_paid` spend that never happened** — the same row
count and the same amount to the cent that BL-1559 measured, which makes this an independent
reproduction rather than a repeat of the same observation. `free_judge._book_paid_call`
defaults to the production ledger and the judge tests stub `_ask` but not the booking, so no
network call is made and the ledger is charged anyway. **None of it is Instagram spend**, so it
does not touch this round's $0.74935.

## 10. WHAT I GOT WRONG

**1. I reported pooled Wilson intervals on clustered data, and they were too narrow.** Accounts
arrive in tags and tags vary enormously. The honest intervals are 1.1–1.7x wider. The headline
survived; the method did not, and I corrected it before publishing rather than after.

**2. I killed my own resume with a stray shell `&` and then misdiagnosed it.** I launched the
resume with `... &` plus a `sleep`, watched the log for 12 seconds, saw it static and concluded
the process was dead. It was merely slow. **One hashtag page was charged and the per-TAG
checkpoint could not record it**, so the true call count is 1,013 + 1. It is booked and named in
the ledger label. The 12-second window was the mistake: a walk that spends 40 seconds per page on
bio fetches looks identical to a dead one at that resolution.

**3. I read a session-scoped counter as cumulative and my first Part 3 numbers were wrong by
15x.** `walk_state.json["totals"]` is rebuilt fresh on every process start while `calls`,
`spent`, `netnew` and `tags_done` are cumulative — the same two-clocks trap `email_harvester`
documents, where a summary mixing them understated a run's cost 4.42x. Reading the live `totals`
after the resume reported **55 accounts where the truth was 852**. The fix sums the session
snapshots and **controls the sum against the per-tag counts**, which are cumulative by
construction; a mismatch is now a hard stop, not a note.

**4. `walk_rows.jsonl` carries duplicates and I published a number off it before noticing.** 106
row lines against **71 distinct account ids and 71 distinct addresses** — and the checkpoint's
cumulative `netnew` is 71, so the checkpoint was right and the row file was not. Every
second-session tag has exactly twice the rows its per-tag counter recorded, while every
first-session tag is exact. I reported "106 addresses" and a 25.47% editor rate off a denominator
that does not exist; corrected to 71 and 22.54%. **The same file was about to be written to the
lead store**, which would have put 35 duplicate rows into it. The raw file is kept as
`walk_rows_raw.jsonl` and the cause is ABSENT below — I have not explained it, only caught it.

**5. `bio_free` counts taking the free branch, not succeeding on it.** `src` is assigned
`"free_http"` before the outcome is known and only overwritten on a *successful* Chromium or paid
fallback — so a paid call that returns no bio increments `bio_free`. Any reading of "free bios"
off that counter is an overstatement; the paid-profile share here is derived from calls minus
pages instead.

**6. A stale print string sent me looking in the wrong directory.** The deliverability pass
prints `wrote scratch/bl1557/deliverability.json` while actually writing to the rebound `_HERE`.
The file was in `bl1560` all along. **A print is a claim; the file on disk is the observation.**

**7. The lead-store writer's backup check was hard-coded to another round's directory** and
refused a perfectly good write. It compared *this* round's manifest digest against
`backups_bl1557/master_leads.csv`. Fixed to read `dest` from the manifest, which every manifest
this repo has written carries — and for BL-1557 that value *is* `backups_bl1557`, so the change
is behaviour-preserving for the round that shipped it.

**8. The brief's own premise had a platform error and I nearly inherited it.** It describes "the
tag ledger" holding 489 + 83 tags while quoting Instagram economics. That ledger is TikTok. Had I
not read `email_harvester.py`'s client construction I would have compared his Instagram walk
against TikTok rates and called it a refutation.

## 11. What did not run, reported as ABSENT

* **Why `walk_rows.jsonl` duplicates.** There is exactly one `append_rows` call site, called once
  per tag, and only two walker processes ever started. The doubling is real, reproducible on
  disk, and **unexplained**. It is contained (the checkpoint is authoritative and the file is now
  deduplicated) but not understood.
* **Whether the NBA-team effect is real on TikTok at a larger n.** It is 8 tags. It survives
  clustering and leave-one-out, and it did not transfer to Instagram. One TikTok walk of fresh
  NBA team tags would settle it and this round did not have the budget.
* **What governs the free bio route's refill.** §7 shows the price swinging 9x on it, which makes
  it the most valuable unanswered question in the project — far more than hashtag choice. BL-1559
  measured a 12.6-hour idle buying ~45 fetches; this walk got ~780 free after roughly an hour.
  **Those two do not agree and I cannot reconcile them.**
* **Whether the editor-rate difference between arms is real.** 4/6 against 4/32 is a hint at n=6.
* **The 13.33% vs 29.37% editor-rate disagreement**, untouched again.

---

https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/BL-1560-the-hashtag-hypothesis-is-refused.md
