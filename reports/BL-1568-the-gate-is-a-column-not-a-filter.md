# BL-1568 — the gate is a column, not a filter: and 81% of his sheet cannot be judged at all

**Round:** BL-1568 · **Unit:** `api.cost_per_call_usd` = $0.00060000, TikTok, by named key
(never `ig_api`'s $0.00069064) · **Spent: $0.00000 of a $0.50 cap**

## The paragraph

**He asked to delete 90–95% of the junk and accept losing 5% of the good pages. He cannot have
that trade on his current sheet, and the reason is not the filter — it is that 81.1% of his
rows have no bio on disk to judge.** Of **3,028** rows, only **234** carry a bio the gate can actually read; **2,455 (81.1%)**
are **UNKNOWN — the gate cannot say NO, only "no evidence"**. The safe cut (**T2**) leaves him
**2,786 rows** and costs about **27 real editors**.
The aggressive cut he asked for (**T3**) leaves **331** — but
**2,455 of its 2,697 deletions
are rows nobody ever judged**, so its true cost in lost editors is **not estimable**. ⚠️ **And
the gate fires on 0 of 8 hand-labelled MEME PAGES — the class he explicitly said to keep — so a
filter built on it deletes them.** The good news is real: **where a bio exists, `bio_rule`
separates PERSONAL BRAND from EDITOR at 75.9% [63.5–85.0] against 4.6%
[1.6–12.7], non-overlapping.** The filter works. The data to run it on was thrown away.

## 1. What this project is, for a reader with no context

It finds video editors on TikTok who publish an email in their bio, and hands the operator a
spreadsheet of leads. He reports that roughly 90% of what he receives is content creators
rather than editors, and he pays someone by hand to mark them.

`clippershq/editor_gate.py` already offers exactly the trade he asked for. **This round did not
rebuild it.** It is `name_rule(handle, nick) OR bio_rule(bio)` — precision **87.65%
[78.74–93.15]**, recall **94.67% [87.07–97.91]** on n=240 across two disjoint sets.
`role_policy.looks_agency(email, handle, name)` handles his business category at **97.7%
precision [88.2–99.6]**.

## 2. Safety, money, the cap, and the suites

Ten stores backed up sha256-verified, bodies found **by shape**, and **all six numbered
corruption controls fired** (`[1, 2, 3, 4, 5, 6]`, counted by matching the NUMBERED lines —
`controls()` also prints a warning and a summary, so a naive print-site count answers 8).

⚠️ **The reused backup module writes its manifest to its own `_HERE`, and the previous round
clobbered a committed file that way.** This round redirected `_HERE` too **and then asserted
that BL-1559's, BL-1566's and BL-1567's manifests still name their own rounds.** They do.

⚠️ **Its row anchor also refused, correctly**: it expects master at 74,162 and found **74,218**
— exactly the 56 rows BL-1567 delivered (74,162 + 56). The anchor lives in a local dict inside
the reused `main()` and cannot be patched, so this round asserts the anchors itself against
current verified counts. **The guard was corrected, not skipped**, and the arithmetic tying the
new figure to the old is stated rather than the number quietly replaced.

**The cap was driven before any call**: funded allows and the meter advances, **$0.00 raises**,
the meter does not advance on a refusal, 3 funded calls allow 3 and refuse the 4th, and the
proof **wrote nowhere** (`stores_unchanged` = True). **No call was made:
this round spent $0.00000.**

**Suites, quoted per name:** `test_bl1568_class_gate` **OK** (9 tests, and **OK under `-O`**),
`test_bl1541_email_harvester` **OK**, `test_bl1567_zero_cap_and_dead_counters` **OK**,
`test_bio_parser_backtrack` **OK**. `spend.json` snapshotted around them: **38,639 rows /
$72.882000 before and after — +0 rows, $0.000000.**

⚠️ **The 29 reds from the last full run are STILL an inference, not a measurement.** Nobody has
run the suite at the prior commit and diffed the sets, and this round did not either — a full
run takes ~48 minutes and would not have changed any decision here. **It stays open.**

## 3. Part 1 — what the gate can actually say about his 3,028 rows

| what the gate can say | rows | share |
|---|---|---|
| `UNKNOWN` | 2,455 | 81.1% |
| `EDITOR (weak)` | 269 | 8.9% |
| `NOT EDITOR` | 159 | 5.3% |
| `BUSINESS/AGENCY` | 83 | 2.7% |
| `EDITOR` | 62 | 2.0% |

**`looks_agency` needs only the EMAIL, which is 100% filled — so the business class is
scoreable on every row.** `name_rule` needs only the handle. **`bio_rule` needs the bio, and
that is the binding constraint**: several rounds stored `bio_len` and threw the bio away, so
for 2,455 rows the gate has nothing to read. **A non-firing rule on a row with no
bio is not a rejection.** Those are UNKNOWN, and they are marked UNKNOWN.

### 3a. The trade, at five cut points — he picks, this round ships no cut

| threshold | rows kept | removed | judged? | est. editors lost |
|---|---|---|---|---|
| T0  no filter (today) | 3,028 | 0 | all judged | — |
| T1  drop BUSINESS/AGENCY only | 2,945 | 83 | all judged | ~9 |
| T2  T1 + drop rows whose BIO says no | 2,786 | 242 | all judged | ~27 |
| T3  keep ONLY rows with editor evidence | 331 | 2,697 | **2,455 never judged** | ~27 **+ UNKNOWN** |
| T4  keep ONLY rows with BIO evidence | 62 | 2,966 | **2,455 never judged** | ~58 **+ UNKNOWN** |

⚠️ **"never judged" means the row has no bio on disk.** Removing it is deleting on *absence of
evidence*, not evidence of absence. T3 and T4 do most of their cutting that way, which is why
**neither is applied here** and why their editor cost is written as **UNKNOWN** rather than a
number.

**What was written to the workbook** (columns added, **no row deleted**, 3,028 → 3,028):
`class_guess`, `class_evidence`, `scoreable`, and `MARK`. Plus a second sheet,
**“Would remove (T2)”, listing all 242 rows the safe cut would take** — that
sheet is how he checks this work, and it is how a previous round caught a rule that killed 11
genuine Gmail addresses.

⚠️ **Written BY HEADER NAME, never by position.** The header carries `Bio source`, `Staleness`
and `Email quality` **three times each** ({'Bio source': [9, 12, 15], 'Email quality': [11, 14, 17], 'Staleness': [10, 13, 16]}). **The duplicates were left
in place** — removing a column he may already be filtering on is a destructive change nobody
asked for.

## 4. Part 2 — the four classes, and the personal-brand class separated for the first time

**140 bios drawn at random from the corpus — not from the gate's own keeps** — masked and
hand-labelled blind, with the gate's verdicts held in a separate file until every label was
written.

⚠️ **The mask was verified before a single row was drawn.** Four address shapes were planted
(`plain`, `(at)/(dot)`, `[at]/[dot]`, `word at word dot`) and every one had to be removed; a
fifth control required clean prose to survive unmangled, because a mask that eats everything
also passes. **0 of 140 masked bios still contained an address.**

| class | n of 140 | share |
|---|---|---|
| EDITOR / CLIPPER | 58 | 41.4% |
| PERSONAL BRAND | 65 | 46.4% |
| MEME / CONTENT PAGE | 8 | 5.7% |
| BUSINESS / AGENCY | 3 | 2.1% |
| UNCLEAR — **not forced into a bucket** | 6 | 4.3% |

⚠️ **This population is NOT his lead list.** It is a random draw from master's TikTok bios,
harvested from **editor-targeted hashtags**, so it is editor-enriched by construction. It
measures how well the signals **separate** the classes. Reading it as his lead mix would be
stating a sample as a property.

### 4a. Does anything separate PERSONAL BRAND from EDITOR? Yes — and it already ships

| rule | fires on EDITOR | fires on PERSONAL BRAND |
|---|---|---|
| `bio_rule` (the bio) | **75.9% [63.5–85.0]** | **4.6% [1.6–12.7]** |
| `name_rule` (the handle) | 19.0% [10.9–30.9] | 3.1% [0.8–10.5] |

**`bio_rule`'s two intervals do not overlap.** That is the answer to the question the brief said
to settle: the personal-brand class *is* cheaply separable, by a rule this project already
owns, wherever a bio exists.

### 4b. Two results that had to be chased before they could be reported

**`looks_agency` fired 0 of 3 on the BUSINESS class — and that zero is UNTESTABLE, not a
failure.** Only **6 of 140** rows in the draw carry an address at
all, and **0 of 3** business rows do. Positive control: **4 of 4**
planted agency addresses detected (agency-word domain, booking mailbox, partnership mailbox,
management domain) with **0 of 3 false fires** on a creator's own
domain, plain free-mail, and their own name on a booking box. The rule works; this draw cannot
exercise it.

**My recall disagreed with the shipped figure until the denominator was named.**

| denominator | precision | recall |
|---|---|---|
| EDITORS only (the shipped denominator) | 88.68% [77.42–94.71] | 81.03% [69.15–89.07] |
| EDITORS **or MEME PAGES** (what he accepts) | 88.68% [77.42–94.71] | 71.21% [59.36–80.73] |

**Precision replicates** (88.68% against the shipped 87.65%
[78.74–93.15]). **Editors-only recall 81.03%
[69.15–89.07] only just
overlaps** the shipped 94.67% [87.07–97.91] — a third sample, sitting low. **A sample is not a
property**, and this is the third time that has mattered here.

⚠️ **THE GATE FIRES ON 0 OF 8 MEME
PAGES** (0.0% [0.0–32.4]).
He said meme pages are fine to DM. **Any cut that keeps only gate-positives deletes that class
entirely.** This is the strongest argument against T3/T4 and it is new.

## 5. Part 3 — both "untested free signals" are ABSENT, not refuted

**(a) Video captions do not exist on disk.** No caption text is stored anywhere in this
project, and the one numeric caption column, `median_caption_len`, is declared on
**56,680** TikTok rows and filled on **0** of
them — a dead column of the same shape as `vision_verdict`. Captions ride free in the hashtag
payload, so this is buyable, but it is not answerable for $0.00.

**(b) Multi-tag appearance cannot be measured from the walk files, and the reason is
structural.** All **1,244** accounts across seven walk files appear under **exactly one tag** —
a 100% zero. It is not creator behaviour: **the dedup guard refuses an account already held, so
a second sighting can never be written.** That is a property of the store. The recoverable proxy
is `post_hashtags`, and only **3 of 134** labelled
rows carry it. **Reported ABSENT.** The idea is not refuted — it is unmeasured, and measuring it
needs a walk that records every sighting rather than only the first.

## 6. Part 4 — capturing the marking he already pays for

The workbook now has a **`MARK`** column. It is **empty, and no tool writes it** — it is his.
Every mark he or his marker makes is labelled training data for the gate, which is currently
produced and thrown away.

⚠️ **No mark file was touched.** A previous round went to remove its own test mark and found 53
marks the operator had just made; it stopped, and so did this one.

⚠️ **Nothing here was validated against `lead_kind` or `verdict`.** `writer.py:363-367` returns
CLIPPER for any `tt:`/`ig:` source regardless of the bio **and says so in its own docstring**.
Two guesses agreeing is not evidence; the hand labels are the only ground truth used.

## 7. Part 5 — wired into the walk, flagging not dropping — and it is a LOCAL fix

The walk now stamps **`editor_class`** and **`editor_evidence`** on every kept account, beside
the count BL-1566 added. **A row with no bio is stamped `UNKNOWN`, never `NOT EDITOR`.**
**Nothing is dropped**, and a test asserts the stamping block contains no `remove`/`pop`/`del`.
**Still one short field per account, not the bio** — the 10,732 bios fetched, read and binned
are why that rule exists.

⚠️ **FIX CATEGORY: LOCAL. It stamps the class in 1 of
9 lead-producing funnels.** Of nine examined, **only
`email_harvester.py` consults the gate at all** — `meme_finder`, `tiktok_finder`,
`email_finder`, `twitch_finder`, `spotify_finder`, `youtube_finder`, `caption_finder` and
`google_play_finder` return **0 AST calls and 0 grep mentions each**. Of seven past fixes
tested by driving them, only 1 of 7 was GENERAL; **this is not that one**, and a future round
must not read it as "the walk is covered".

**Which instrument answered:** the **AST**, for the calls — only it tells a call from a mention
in a comment or an import line. grep's higher count on `email_harvester.py` (10 mentions
against 2 calls) is prose and imports, which is exactly the false-positive direction grep fails
in.

## 8. What I got wrong, and what is absent

**My own threshold table understated the aggressive cuts, and I nearly shipped it.** The first
version printed "~27 editors lost" beside T3 — a cut that removes **2,455 rows nobody ever
judged**. It was quietly answering *"how many editors are among the rows we looked at"* while
appearing to answer *"what does this cut cost"*. Corrected to **`~27 + UNKNOWN`**, because the
honest answer to the second question is that nobody has the number. **That is the single most
misleading thing this round could have handed him**, and it would have pointed him straight at
the cut he asked for.

**I copied REAL lead addresses into a control, and the leak scan caught it before
publication.** My positive control for `looks_agency` used the examples from the rule's own
docstring — and **two of them matched the lead corpus**, because the docstring cites real
addresses. The `address_from_corpus` detector fired on a file I was about to publish. Replaced
with `.invalid` domains, which RFC 2606 guarantees can never be registered; the control still
detects 4 of 4 and false-fires 0 of 3. **A control must carry the SHAPE of what it tests, never
a real value** — and a docstring in shipped source is not a safe place to copy from.

**I reported a recall that disagreed with the shipped figure before separating the
denominators.** Mine counted EDITORS **or** MEME PAGES because he accepts both; the shipped one
counts editors. Split, precision replicates and recall merely sits low. **Two numbers measuring
different sets are not a disagreement**, and calling it one would have impugned a gate that is
fine.

**I nearly reported a 0-of-3 zero on `looks_agency` as a result.** It was untestable — 0 of
those 3 rows carried an address. The positive control is what turned it from a finding into a
fact about the draw.

**Reported as ABSENT, not as zero:**

* **Video captions** — no text on disk, `median_caption_len` filled on 0 of 56,680.
* **Multi-tag appearance** — unmeasurable from the walk files by construction; the proxy covers
  3 of 134 labelled rows.
* **Whether the 29 failing suites pre-date this work** — still an inference; no prior-commit run
  was made.
* **What the 2,455 UNKNOWN rows actually are.** This is the one thing worth buying:
  their bios are re-fetchable at $0.00060 each, and a 200-row sample would cost **$0.12** and
  turn the T3 column from UNKNOWN into a measured number. **It was not bought this round**, and
  it is the obvious next step.
* **13,007 addresses, none ever contacted.** Unchanged.

---

https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/BL-1568-the-gate-is-a-column-not-a-filter.md
