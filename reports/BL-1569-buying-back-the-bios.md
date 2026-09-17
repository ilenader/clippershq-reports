# BL-1569 — buying back the bios, and the "safe" cut deletes the class he said to keep

**Round:** BL-1569 · **Unit:** `api.cost_per_call_usd` = $0.00060000, TikTok, by named key
(never `ig_api`'s $0.00069064) · **Spent: $1.63320 of a $3.00 cap, 2,722 calls**

## The paragraph

**The bios came back, and his sheet is judgeable for the first time.** Of 3,028 rows,
**2,836 (93.7%) can now be classified**
against 573 (18.9%) before — the re-fetch returned a bio on **93.8%** of the accounts
it was asked for. **But the trade he asked for -- 90-95% of the junk gone for 5% of the good
pages -- IS NOT AVAILABLE AT ANY CUT.** Removing 71% of the sheet (T2) costs
**~255 real editors [164-384]**, which is about **29% of the editors he has**, not 5%. ⚠️ **But the headline is a correction to my
own last round: T2 — the cut I called "safe" — removes 13 of 14 hand-labelled MEME PAGES,
92.9% [68.5–98.7].** He said explicitly that a meme page is fine to DM. **Only T1, which keys on
the ADDRESS and never on the bio, leaves that class intact.** A pre-specified meme rule was
built and **refused on measurement** (precision 80%
[38–96], recall
29% [12–55]).
And the 29 failing suites, deferred three times, are **settled: 0 are regressions from this
work.**

## 1. What this project is, for a reader with no context

It finds video editors on TikTok who publish an email in their bio and hands the operator a
spreadsheet of leads. He reports most of what he receives is content creators rather than
editors, and pays someone by hand to mark them.

The filter already existed and was measured. What blocked it was that **earlier rounds stored
`bio_len` and threw the bio text away**, so the gate could not judge 81.1% of his sheet. This
round bought the bios back at $0.00060 each.

## 2. Safety, money, and the cap

Ten stores backed up sha256-verified, bodies **by shape**, **all six numbered corruption
controls fired** (`[1,2,3,4,5,6]`, counted by matching the NUMBERED lines — a naive print-site
count answers 8). The reused backup module writes its manifest to its own `_HERE`, so `_HERE`
was redirected **and BL-1559's, BL-1566's, BL-1567's and BL-1568's manifests were asserted to
still name their own rounds.** They do.

Its row anchor is stale (expects 74,162, master holds 74,218 = 74,162 + BL-1567's 56); this
round asserts the anchors itself against current verified counts. **The guard was corrected,
not skipped.**

**The cap was driven before the first call**: funded allows and the meter advances, **$0.00
raises**, the meter does not advance on a refusal, 3 funded calls allow 3 and refuse the 4th,
and the proof **wrote nowhere** (`stores_unchanged` = True).
**Spent $1.63320 of $3.00** across 2,722 calls, booked under one campaign at
stage `/v1/user/by/username` — the endpoint path, which `validate_stage` accepts and which names
what the vendor actually charged for.

## 3. Part 1 — the buy-back

⚠️ **THE READER WAS PROVED BEFORE THE MONEY WAS SPENT.** The bio field is `signature`, not
`biography`, and a probe searching the wrong name once reported 0 of 25 where the truth was
86.2% *and was believed*. One call was made against a handle whose bio was already on disk.
`signature` was present and the extractor read bio from it — **but the value did
not match the stored bio.** That is **drift, not a reader failure**: bios change. Reported as
what it is rather than dressed up as a clean match.

**SAMPLE FIRST, THEN RE-PRICE.** 200 rows at $0.12 returned a bio on **190 (95.0%)**. That
re-priced the remaining 2,522 at **~$1.51**, inside the $3.00 cap, so the rest was bought. The
full run came in at **93.8%** recovery -- 1.2 points below the sample, which is what a
200-row estimate is worth and why the sample was taken rather than assumed.

| fetch outcome | n | share |
|---|---|---|
| `bio` | 2,552 | 93.8% |
| `fetch_failed` | 139 | 5.1% |
| `empty_bio` | 31 | 1.1% |

⚠️ **A FAILED FETCH IS `UNKNOWN`, NEVER "NO BIO".** A not-found/private/deleted account, an
empty-but-served profile and a torn response are different things and none of them means the
person has no bio. Each is recorded by name above. **Validation was on CONTENT, never status** —
this vendor returns HTTP 200 with the list absent, and five of six parameter variants once
returned HTTP 200, charged and empty.

### 3a. The bios are STORED this time

**10,732 bios were once fetched, read and binned. That is why this round existed, so the
bought ones are written down.** 1,020 bios went into master's `bio` column
and **51,815 rows were given a class** by the one shared classifier.
74,218 rows in, 74,218 out, header still `ok`, **zero C0 control bytes
asserted BEFORE the write**, and the write aborts if master changes underneath.

⚠️ **AN EXISTING BIO IS NEVER OVERWRITTEN** (0 were). A stored
bio was captured at harvest time; this one is a later re-fetch, and clobbering the older one
destroys the only record of what the account said when it was found.

⚠️ **AND ONLY 1,020 OF THE 2,552 BOUGHT BIOS COULD BE STORED
IN MASTER**, because only about half his workbook handles exist in master at all -- the 94%
master/workbook divergence BL-1564 measured. The rest live in this round's fetch checkpoint,
which is on disk but **gitignored because it carries bios and handles**. If that file is lost,
that part of the $1.63 is lost with it. Named as a gap, not papered over.

### 3b. What his sheet looks like now

| class | rows | share |
|---|---|---|
| `NOT EDITOR` | 2,073 | 68.5% |
| `EDITOR` | 680 | 22.5% |
| `UNKNOWN` | 192 | 6.3% |
| `BUSINESS/AGENCY` | 83 | 2.7% |

### 3c. The trade, re-priced — the cost is a number now

| threshold | kept | removed | **real editors lost** | **meme pages lost** |
|---|---|---|---|---|
| T1  drop BUSINESS/AGENCY only | 2,945 | 83 | ~1 [0–4] | n/a |
| T2  T1 + drop rows whose BIO says no | 872 | 2,156 | ~255 [164–384] | ~183 [109–302] |
| T3  keep ONLY rows with editor evidence | 680 | 2,348 | ~255 [164–384] **+192 unjudged** | ~183 [109–302] |

⚠️ **THE MEME COLUMN IS NEW AND IT CHANGES THE RECOMMENDATION.** BL-1568 called T2 the safe
cut. Measured on 14 hand-labelled meme pages, **T2 removes 13 of them (92.9% [68.5–98.7])**,
because a meme bio shows no editor evidence and T2 drops exactly those. **T1 is the only cut
that leaves the class intact**, because `looks_agency` keys on the address and never reads the
bio.

## 4. Part 2 — the meme-page hole, on n=14 instead of 8

260 bios hand-labelled blind across **two disjoint random draws** (BL-1568's 140 plus 120 more;
the sampler excluded every row already drawn, because re-labelling inflates n without adding
information). The mask was verified on four planted address shapes plus a clean-prose control
before a single row was drawn, and **0 of 260 masked bios still contained an address**.

| class | n of 260 | share |
|---|---|---|
| EDITOR / CLIPPER | 109 | 41.9% |
| PERSONAL BRAND | 120 | 46.2% |
| MEME / CONTENT PAGE | 14 | 5.4% |
| BUSINESS / AGENCY | 4 | 1.5% |
| UNCLEAR — **not forced** | 13 | 5.0% |

**The gate fires on 1 of 14 meme pages —
7.1% [1.3–31.5]** against
BL-1568's 0 of 8 [0.0–32.4]. The hole is confirmed with the interval halved.

**And the separation that does work, re-measured:** `bio_rule` fires on **78.0% [69.3–84.7]** of
EDITORS against **2.5% [0.9–7.1]** of PERSONAL BRANDS — non-overlapping, and tighter than
BL-1568's 75.9% / 4.6%. Precision **91.00% [83.77–95.19]** on editors-only, which replicates the
shipped 87.65% [78.74–93.15]. **The gate's recall has now read 94.67%, 79.41%, 81.03% and
83.49% on four samples. A sample is not a property.**

### 4a. A meme rule was built and refused

The rule was **pre-specified from the class definition** — a topic plus a posting habit, with no
craft claim and no self-reference — and deliberately **not fitted to these 14 rows**, because
fitting a keyword list to 14 examples and scoring it on the same 14 measures memorisation.

**Precision 80% [38–96],
recall 29% [12–55]
on 14 meme pages. VERDICT: DO NOT SHIP.** A filter that
costs money and does not work is worse than none. **The operational answer is not a rule: it is
T1**, which never reads the bio and therefore cannot delete a meme page.

## 5. Part 3 — wired GENERAL, at two chokepoints

**ONE IMPLEMENTATION: `editor_gate.classify(handle, nick, bio) -> (class, evidence)`.** Not an
if/elif pasted into each assembler — four copies of one rule is how three of them drift.

**There are exactly three places a lead row is assembled**, and all three call it:

| site | what reaches it |
|---|---|
| `writer._build_row` | the 6 funnels that write through the Writer |
| `crossdedup.append_leads` | `meme_finder` and `tiktok_finder`, which each carry a private `_append_to_master` and never touch the writer |
| `email_harvester` walk loop | the hashtag walk |

**FIX CATEGORY: GENERAL.** Before this round the stamp lived in 1 of 9 funnels and the other
eight returned 0 AST calls and 0 grep mentions each.

⚠️ **THE SITE COUNT ITSELF NEEDED BOTH INSTRUMENTS.** A bare leaf-name count of `classify`
answered **34** — `send_suppress.py` alone has 15 unrelated `classify()` methods. Counting only
calls whose base is a gate alias gives **3**. That is the AST false-positive direction, and it
is why the number quoted above is 3 and not 34.

⚠️ **AND "THE MODULE IMPORTS" IS NOT PROOF.** A name looked up only when a function runs raises
`NameError` while the module imports cleanly, so the suite parses every call site and asserts
the base name is bound **in that function's own scope** — with the checker proved first on
planted bound *and* unbound source.

### 5a. Master had to be migrated, and why that was unavoidable

`_build_row` emits `[rec.get(col, "") for col in FULL_COLUMNS]`, so **a key stamped into `rec`
but absent from that list is silently dropped** — computed, then binned, which is the exact
dead-value shape this project keeps finding. So the columns had to be added, and
`master_header_status()` compares the on-disk header **exactly** to `FULL_COLUMNS`.

Migrated 74,218 → 74,218 rows, all previously [72] wide
and now 74, header back to `'ok'`,
**0 rows the wrong width**. Every existing row got an **empty**
value, never a guess: the class is forward-only by construction, exactly as `run_id` is blank on
92.1% of rows and was never backfilled.

### 5b. The zero-means-uncapped disagreement, reconciled

`effective_run_cap`'s docstring said 0.0 means *no budget*; the finders read 0.0 as
**unlimited**, so an operator typing 0 got an unbounded run. **One sentinel now: `None` = no cap,
`0.0` = spend nothing.** Changed across **11
truthiness sites and 5 signature
defaults** in 5 finders, plus `caption_finder`'s resolver, which turned both an absent key and a
declared 0 into 0.0. **0 truthiness sites survive.**

⚠️ **This changes behaviour for an unconfigured caller, deliberately**: a funnel whose cap key is
absent previously ran unlimited and now halts. That is this project's own stated rule — *"a
forgotten cap must mean no run"* — and it is the safe direction for a money path. All cap suites
stay green.

### 5c. Captions are captured now

`median_caption_len` was declared on 56,680 rows and filled on **0**. The caption rides in the
same hashtag payload as the bio, free, and was being discarded. The walk now records `caption`
and `caption_len` per account — **and an absent item is `None`, never 0**, because a length of 0
would claim a measurement never taken. **This round does not test captions; it stops the next
round being unable to.**

## 6. Part 4 — the deeper research

**What else is stored and never read.** Of master's 74 columns, **25
are declared and filled on ZERO rows** — including all nine outreach columns (`date_sent`,
`replied`, `bounced`, `converted`…), which is the 13,007-addresses-never-contacted fact showing
up in the schema, plus `vision_verdict`, `vision_confidence`, `median_caption_len` and seven
per-post fractions. **2 more are filled but constant** and
therefore cannot decide anything.

⚠️ **THE FIRST RUN OF THIS CENSUS REPORTED "0 VARYING-AND-UNREAD" AND THAT WAS AN INSTRUMENT
FAILURE.** Every column name appears inside `FULL_COLUMNS` in `writer.py`, so **the declaration
itself was counting as a reader** and no column could ever score zero — the same mistake grep
made when it counted a wordlist and report prose as readers. With the declaration excised and a
planted control proving the detector can still reach zero, the real answer is
**1: `twitch_login`**, filled on 260 rows with 50+ distinct values
and no production reader found by name. **An upper bound on deadness** — a column read through a
runtime-assembled name is invisible to leaf-name matching.

**Multi-tag appearance stays UNMEASURED, not refuted.** All 1,244 accounts across seven walk
files appear under exactly one tag, and that 100% zero is **structural**: the dedup guard refuses
an account already held, so a second sighting can never be written. The proxy `post_hashtags`
covers 3 of 134 labelled rows. Settling it needs a walk that records every sighting.

## 7. The 29 reds, settled — deferred three times, answered here

The suite was run at **2df05e28**, the commit before BL-1567's first code change, in an isolated
worktree with the ten gitignored stores copied in. Prior commit: **383 PASS /
71 FAIL / 9,145 checks**. HEAD run: **453 PASS / 29
FAIL / 10,345 checks**.

* **25 of 29 fail at BOTH commits** — they cannot have
  been introduced by anything after 2df05e28.
* **4 differ**, and each was chased individually:
  `test_run_id_isolation` and `test_enrich_concurrent` **pass on re-run at HEAD** (transient —
  the original run reported 16 rounds in flight editing the tree); `test_bl1307_veto_refused`
  fails on a **scratch artefact from another round** that the worktree does not carry; and
  `test_send_list_rebuild` compares a **cached metadata figure (72,950) against the live master
  count (74,218)** — stale data, not code.

**CODE REGRESSIONS ATTRIBUTABLE TO THIS WORK: 0.**

⚠️ **What is NOT claimed:** that the prior commit's 71 failures are all real. The
worktree is not the live tree, so failures seen only there may be environmental. **The
settlement rests on the direction that confound cannot touch** — failing at both commits — plus
four individually chased exceptions.

## 8. What I got wrong, and what is absent

**I BOOKED MY OWN SPEND INTO THE WRONG VENDOR COLUMN, AT THE WRONG PRICE, AND THE LEDGER
SAID I SPENT MORE THAN I DID.** `record_aux_spend` takes separate `ig_calls` and `tt_calls`. I
passed 2,723 **TikTok** calls as `ig_calls`, so LamaTok spend landed in the HikerAPI column —
**and was priced at the Instagram rate, $0.00069064 instead of $0.00060000**, because the booker
uses `ig_cost_per_call` for `ig_calls` and ignored the `cost_per_call` I passed. The ledger
recorded **$1.880613 against $1.633800 actually spent**: $0.246813 of phantom spend, with
`tt_calls` left at 0 so the call counts vanished too.

**Over-booking is not the harmless direction.** A cap is enforced against the ledger, so phantom
spend silently shrinks every future run's budget — it is the mirror of the off-the-books leak
this project has chased for rounds, and it was found only because re-stamping `FACTS.md` forced
me to look at the vendor split. Corrected on this round's three rows only: column moved, price
corrected, `tt_calls` restored to 1/200/2,522, and the stored header total re-derived from the
rows (it still carried $0.245613 of the phantom). Row count unchanged at 38,642.

**And I put an absolute path with the operator's username into a file bound for the public
repo.** The leak scan's `abs_user_path` detector caught it in `bl1569_suite_diff.py`. A path
under a home directory is personal data in exactly the way a handle is. Now derived from the
environment.

**I broke my own rule twice in one round, and it cost two broken files.** I patched production
source through a bash heredoc; the shell ate a `\n` escape, and the second attempt died on
nested triple quotes. **"Write source with a file tool, never a shell heredoc"** exists for
exactly this, and I re-learned it by writing a syntax error into a working module twice. Both
patches were redone as real scripts.

**My column census returned a clean 100% zero that was pure artefact.** "0 varying-and-unread"
was the `FULL_COLUMNS` declaration counting itself as a reader. The 100%-zero rule caught it;
without it I would have published "nothing else is being thrown away" from a detector that
could not return anything else.

**A BL-1568 test failed on correct code and I had to rewrite it.** It pinned the literals
`UNKNOWN` and `NOT EDITOR` inside `email_harvester.py`; moving the one implementation into
`editor_gate.classify` correctly removed them, and the test went red on a refactor that improved
the thing it guarded. **A test that pins WHERE a string lives measures the layout, not the
behaviour.** Rewritten to drive the function.

**And the reader proof did not prove what I designed it to.** I searched the live payload for
the *exact stored bio* and it was not there — because bios drift. The reader was fine; the test
was wrong. Reported as drift rather than quietly re-run until it matched.

**Reported as ABSENT, not as zero:**

* **Whether captions separate the classes** — captured this round, untested. Deliberate.
* **Multi-tag appearance** — unmeasurable from the walk files by construction.
* **The 192 rows still unjudged**: 139
  accounts are gone (not found / private / deleted) and 31 genuinely
  have no bio. **No further spend recovers those.**
* **The meme class cannot be filtered for**, and this round refused to ship a rule that pretends
  otherwise.
* **13,007 addresses, none ever contacted.** Unchanged, and still the largest open question.

---

https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/BL-1569-buying-back-the-bios.md
