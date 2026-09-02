# BL-1485 — No model ever touched an address, and the source that would prove it was never kept

**The short answer: no, the Spotify run did not invent addresses. It could not have — there is
no language model anywhere on the path that produces one. But the test that would prove it
address-by-address cannot be run on a single one of the 7,843, because the text each address
was read from was never written to disk. Provenance for 60.5% of the store is unfalsifiable.**

Read this as someone with no access to the machine and no memory of any prior round. Every
number below names its denominator. No address, local part, domain, artist name or handle
appears anywhere in this document; faults are reported as counts and as character masks.

---

## 1. Round ID, date, and what it was asked to do

**BL-1485**, 2026-09-02. Read-only. No production file was written, nothing was restored,
nothing was renamed, no vendor call was made, no process was touched.

The question, as asked: he is seeing bounces and wrong addresses, and wants to know whether
the Spotify run hallucinated the roughly four to five thousand emails it produced.

**One fact shapes everything and has to be said first: this project has never sent anything.**
Verified this round on all 72,954 rows of the lead store — `date_sent`, `sent_channel`,
`replied`, `reply_sentiment`, `bounced`, `converted`, `outcome_notes` and `touch_number` are
non-empty on **0** rows each. So no bounce he has seen came from this system. It came from his
separate sending tool. This round cannot read a bounce log and does not pretend to.

That leaves exactly one honest way to answer him: **work backwards from the addresses
themselves.** In scope: whether an address is real, where it came from, and whether it belongs
to the person it is attached to. Out of scope: anything about messaging or sending practice.

Five sub-agents ran in parallel: the extraction-path trace, the retained-payload inventory, the
join and false-merge audit, the documentation sweep, and the structural/MX work done directly.

---

## 2. What actually shipped

Nothing. This round is an audit and writes no production file. It changed no code, no config
and no document, and it deliberately did not "improve" the two rules it examined that are
already correct (the cross-dedup refusal, and the MX suppression rule).

Artifacts produced, all under `scratch/` and `reports/`:

| file | what it is |
|---|---|
| `scratch/bl1485_verbatim2.py` / `.json` | the Part 2 verbatim checker, its 15 planted controls, and the per-family split |
| `scratch/bl1485_structure2.py` / `.json` | MX, structural and duplicate counts per source family |
| `scratch/bl1485_shapes.py` / `.json` | every faulty address rendered as an identity-free character mask |
| `scratch/bl1485_gate.py` / `.json` | which clause of the project's own validator rejects which stored address |
| `scratch/bl1485_stranded.py` / `.json` | the checkpoint-to-store join that settles the stranded-address question |
| `scratch/bl1485_agentA_*` | the AST walk, the runtime spy and the regex probes |
| `scratch/bl1485_agentB_*` | the whole-repo payload inventory (12,744 rows) |
| `scratch/bl1485_agentC_docs.md` | the documentation sweep |
| `scratch/bl1485_agentD_*` | the join, false-merge and shared-inbox audit |

---

## 3. What was measured

### 3.1 Part 1 — is a language model involved at all? **No.**

This was answered with an AST walk and a runtime spy, not a grep, because a grep has been
wrong here before: a string literal matching a module stem has marked eight modules falsely
alive, and an import graph has orphaned the two live finders because the runner dispatches by
importing module names out of string literals in a table.

**The control that makes the negative mean something.** Before trusting any zero, the walker
was pointed at an edge known to be live — the Spotify finder's call into the email finder's
detector at `clippershq/spotify_finder.py:143`. The walker saw it. A deliberately false edge
(the bio parser calling back into the Spotify finder) was correctly reported absent. Only then
were the zeros read.

From eleven seeds, static reachability is **98 nodes across 14 modules**: `bio_parser`,
`dedup`, `email_finder`, `enrich_links`, `finder_common`, `google_play_finder`,
`ig_discovery`, `market_filter`, `quality_gate`, `rejection_store`, `resolve_cache`,
`role_policy`, `spotify_finder`, `writer`.

Every module in this repository that can call a language model — the free judge
(`free_judge.py:1083`), the vision judge (`thumbnail_vision.py:425`), the preflight
(`preflight.py:294`), the batch judge, the rubric reader, the layout reader, the frame reader,
the OCR path — scores **0 both in the strict static graph and in a deliberately over-inclusive
one**. The three non-zeros the over-inclusive graph produced were opened and read: two are
sleep helpers and one is a JSON load, all pure method-name collisions. The one genuine static
hit into a "judgement"-sounding function is offline Unicode-script counting. The two API
clients on the path are data APIs, not models.

A runtime spy with the HTTP library replaced by a raising tripwire drove the contact-finder
offline through all four of its routes and recorded the real call order. No model appeared in
it.

> An import-closure check was also run and returned 83 modules including the vision judge.
> **That result is garbage and is labelled as such**: the writer and the cross-dedup module
> import the control layer, which imports the whole tree. An import is not a call. It is
> recorded here because someone will run that check again and needs to know it lies.

**So: hallucination in the strict sense is impossible, and that is good news — it narrows the
hunt. The failure mode is MIS-EXTRACTION: a pattern grabbing something adjacent, truncated,
concatenated, or lifted from the wrong part of a page.**

**Every extraction site, with file:line and mechanism:**

| site | file:line | mechanism | stamped as |
|---|---|---|---|
| S1 | `ig_discovery.py:318-320` | **structured API field** — a cascade of public/business/contact email fields; the only guard is that the value contains an `@` | `spotify:resolved-instagram` |
| S2 | `ig_discovery.py:327` | **regex on the Instagram bio TEXT** | **also** `spotify:resolved-instagram` |
| S3 | `email_finder.py:250` | regex on the TikTok profile signature | `spotify:resolved-tiktok` |
| S4–S7 | `enrich_links.py:320`, `:323-325`, `:335`, `:338-339` | regex on raw markup, on `mailto:`, on stripped text, and on `alt=` attributes | aggregator / bio-link / website |
| G | `google_play_finder.py:50-69` | the anchored-regex final gate for every route above | — |

Assignment sites inside the Spotify contact-finder: `spotify_finder.py:416-419`, `:426-429`,
`:473-476`, `:488-491`.

**A correction to the label itself.** `spotify:resolved-instagram` carries 7,425 of the 7,843
Spotify addresses, and it covers **two different mechanisms**: the bio-regex hits at
`ig_discovery.py:327` are merged into the same list as the structured-field reads, and the
picker returns the first *personal*-looking address — so a bio-regex hit can outrank a
structured role field and still be stamped `resolved-instagram`. **The label is a claim, not
an observation of which mechanism ran.** The split is unrecoverable from the store, for the
same reason as everything else in this report: the bio was not kept.

### 3.2 Part 2 — does each address appear in its own source? **The Spotify slice cannot be asked.**

**The controls ran first, and one of them caught a defect in my own checker.** Fifteen faults
were planted into a synthetic source string and the checker had to name each one: a clean
address, a case-only difference, a truncated tail, a truncation down to the bare domain, a
local-part fragment, a glued tail, two addresses joined, a missing character, a swapped
domain, a leading junk character, an apostrophe-hyphen prefix, the bad `local[:2] + ".."`
redaction, a wholly different address, a source holding no address, and no source at all.

The first version scored **PLANTED TRUNCATED → VERBATIM**, and it was right to: a truncated
address *is* a substring of its own intact source, so a plain containment test calls the
truncation faithful — silently, in the exact direction that hides the defect being hunted. The
checker was rewritten to require a whole-token match with both boundaries checked. **13 of 13,
then 15 of 15, pass.** Without that control this round would have published a clean bill of
health for truncation.

**What counts as "the source text".** The only retained per-row free text in this store is the
`bio` column. `link_in_bio` and `website` are URLs — pointers to a source, not the source. The
resume-checkpoint payloads hold the *extracted* address, so matching against them is circular
and is excluded by construction.

**The result, per source family. Denominator: 12,960 rows carrying an address (12,674 distinct).**

| family | rows | VERBATIM | MANGLED | ABSENT | source held no address | no source retained |
|---|---:|---:|---:|---:|---:|---:|
| **Spotify** | **7,843** | 0 | 0 | 0 | 0 | **7,843 (100.000%)** |
| blank-source (the original TikTok clipper funnel) | 2,924 | 2,676 | 46 | 1 | 52 | 149 |
| Instagram page funnel | 1,140 | 6 | 1 | 0 | 98 | 1,035 |
| Twitch / Kick | 636 | 0 | 0 | 0 | 0 | 636 |
| Google Play | 213 | 0 | 0 | 0 | 0 | 213 |
| TikTok (stamped) | 115 | 0 | 0 | 0 | 0 | 115 |
| other named | 43 | 0 | 0 | 0 | 9 | 34 |
| YouTube | 29 | 0 | 0 | 0 | 0 | 29 |
| his graded sheet | 17 | 0 | 0 | 0 | 0 | 17 |
| **all** | **12,960** | 2,682 | 47 | **1** | 159 | 10,071 |

**The ABSENT bucket was split deliberately, and this matters.** A row whose retained text holds
*no address at all* tells you the address came from somewhere that was not kept — that is a
retention gap, not evidence of invention, and counting it as ABSENT would manufacture a
hallucination rate out of a storage decision. Only a row whose retained source **demonstrably
held other addresses** and does not hold this one can answer his question.

**On that denominator — 2,730 answerable rows across the whole store:**

| bucket | n | % of answerable | 95% Wilson |
|---|---:|---:|---|
| VERBATIM | 2,682 | **98.242%** | [97.68, 98.67] |
| MANGLED | 47 | 1.722% | [1.30, 2.28] |
| **ABSENT** | **1** | **0.037%** | **[0.01, 0.21]** |

**One address in 2,730 is missing from a source that held others. That is the entire
hallucination bucket in this project, and even that one has a 0.58 similarity to what the
source did hold, which is the profile of a mangling, not an invention.**

**And the Spotify slice: 7,843 of 7,843 uncheckable, 100.000% [99.95, 100.00].** Zero
verbatim, zero mangled, zero absent — because zero could be asked.

This was confirmed three independent ways: the `bio` column is populated on **0 of 7,843**
Spotify rows (and on 2,742 of 2,891 TikTok-route rows, so the column works); the master writer
never writes `bio` on the Spotify path; and a whole-repository walk (12,744 files inventoried,
including 109 gzipped ones that a first extension filter missed) found **27 of 4,095** stranded
addresses matching any retained text anywhere on disk — **0.66%**, all of them incidental
collisions with other funnels' corpora. The one code path that could have saved the raw
Instagram response, `ig_client.py:867`, is gated on a config flag that is `false`, and is
one-shot per endpoint per run in any case.

**The mangling shapes on the one arm we can see** (46 rows, blank-source family):

| shape | n | what it is |
|---|---:|---|
| identical but flanked in the source | 16 | the source token runs on into adjacent text |
| stored has **1 extra character glued at the start** | 14 | a neighbouring character swept into the local part |
| stored has 20–37 extra characters glued at either end | 13 | **two addresses stored in one field** |
| everything else | 3 | — |

### 3.3 Part 3a — the wrong person, and the false-merge exposure

**The join.** Two independent measures were run over the 7,843 Spotify addresses, comparing the
address's local part and domain label against the row's own display name and handles.

| | strong relation | weak | none |
|---|---:|---:|---:|
| arm A (letters only, sequence ratio) | **58.68% [57.58, 59.76]** | 7.13% | **34.18% [33.14, 35.24]** |
| arm B (digits kept, 3-gram Dice) | 56.55% | 3.24% | **40.21% [39.13, 41.30]** |

**The arms disagree by 6.0 points on the headline and neither is picked.** The disagreement is
entirely at the weak/none boundary and is caused by digits; the strong bucket is stable within
2.1 points.

**The shuffled control fired hard.** Pairing every address with a *different* row's identity
(a seeded derangement, zero fixed points) collapses strong from 58.68% to **0.18% [0.11, 0.30]**
and raises none to 92.77% — a **326-fold separation with non-overlapping intervals**. The
measure detects something real.

Address classes in the Spotify slice: free provider 4,105 (52.34%), role inbox 1,255 (16.00%),
other domain 2,483 (31.66%). A free-provider or role address legitimately shows no relation, so
the genuinely suspicious bucket is *no relation **and** not free **and** not a role inbox*:
**1,530 of 7,843 = 19.51% [18.65, 20.40]** (arm B: 1,661 = 21.18%).

**This is an upper bound on a shape, not a fault rate.** An artist's manager's address has no
textual relation to the artist and is exactly the address you want. Nothing on disk can tell
those apart.

**The false merge.** The merge key is emitted at `crossdedup.py:185-201` and consumed by a
union-find at `crossdedup.py:261-281`, which unions every component touched by any shared key —
so two rows with different handles fold the instant both emit the same address key, the first
row seen survives, and the rest are dropped as a count. The standing open issue is at
`crossdedup.py:84-114`: three artists sharing a manager were folded together and each lost its
master row. **Missing a duplicate costs one extra message; a false merge deletes a person and
reports nothing.**

The refusal that guards it, quoted from `_is_mergeable_email` at `crossdedup.py:50-81`: an
infrastructure-domain guard at `:67-72`, a `role_policy.kind(e) != "personal"` rejection at
`:73-74`, and a third-party-address rejection at `:75-80`. The shipped functions were called
rather than reimplemented.

**Measured on the live store, nothing modified.** 12,698 distinct addresses; **139 carried by
two or more rows, across 426 rows**; group size median 2, maximum 87. Of 136 groups with mixed
identities, **the rule refuses 135 and would fold 1**. Residual blast radius: **2 rows
store-wide (0.015% [0.004, 0.056]) and 0 rows in the Spotify slice (0.00% [0.00, 0.049])**; one
row would disappear.

Two things qualify that zero, and both are stated rather than buried. **Survivorship:** rows the
rule already deleted are gone, so the store cannot show past damage. **The counterfactual:**
with the refusal removed, 136 groups and 415 rows would fold and **279 rows would disappear** —
the refusal is preventing 278 of 279 today. Forward-looking exposure, rows matching the shape
that caused the original incident: **1,166 of 12,960 = 9.00% [8.52, 9.50]** store-wide, **925 of
7,843 = 11.79% [11.10, 12.53]** in the Spotify slice.

**No change to the merge rule is proposed. The refusal is correct.**

### 3.4 Part 3b — shared and role inboxes

**The prior figure of "420 of 4,433 rows — 9.47%" is identified and reproduced exactly.** It is
not a slice of the store: it is the lead set of the killed run, still on disk as the 4,433-row
export in the Spotify leads directory. Re-derived: 4,433 rows, 4,095 distinct addresses,
**82 addresses on two or more rows, 420 rows sharing = 9.4744% [8.6470, 10.3719]**, largest
group 164.

It does not hold on the current store and never claimed to: the store is post-dedup, that
export was pre-dedup. Current sharing is **426 of 12,960 rows = 3.2870% [2.9936, 3.6081]**
store-wide and **332 of 7,843 = 4.2331% [3.8094, 4.7015]** in the Spotify slice — intervals
that do not overlap 9.47%.

**Role prefixes** (head token, split on `.`, `-`, `_`, `+`): **1,678 of 12,960 = 12.95%
[12.38, 13.54]** store-wide; **1,255 of 7,843 = 16.00% [15.21, 16.83]** in the Spotify slice.
Top prefixes, store / Spotify: `info@` 815/666, `contact@` 258/158, `mgmt@` 140/132,
`hello@` 133/82, `booking@` 103/92, `management@` 94/83, `support@` 81/6.

> A second pass using a broader prefix list (adding `business@`, `mail@`, `office@`,
> `inquiries@`) put the Spotify figure at 1,437 = 18.32% [17.48, 19.19]. The gap is purely
> definitional and both numbers are given rather than one being chosen.

The shipped role classifier sees fewer, because it treats `booking@` as personal by design:
1,485 = 11.46% store-wide, 1,011 = 12.89% Spotify. **These are inboxes two people really do
share, the refusal to merge them is right, and no rule change is proposed.**

### 3.5 Part 3c — dead domains

The MX table was probed on 2026-08-30 and holds verdicts for 4,146 domains out of 4,152
probed. Its verdict vocabulary is `ok-MX` 3,991, `DEAD` 87, `noMX-Aonly` 61, `null-MX` 7.

> **A false zero of my own, caught and corrected.** The first pass counted the probe module's
> internal enum names against a table that stores short scalar strings, and reported
> **certain-dead = 0 in every single family**. The table was opened and its actual values read;
> the corrected numbers are below. A zero that matches what you expect is the one to check.

**Spotify slice, denominator 7,843:**

| verdict | rows | % | 95% Wilson |
|---|---:|---:|---|
| `ok-MX` | 7,734 | 98.610% | — |
| **certain bounce** (`DEAD` 57 + `null-MX` 6) | **63** | **0.803%** | **[0.63, 1.03]** |
| `noMX-Aonly` — an implicit MX, **not** a certain bounce | 43 | 0.548% | — |
| no verdict in the table | 3 | 0.038% | — |

Coverage on the Spotify slice: **99.962%**. The 63 certain-bounce rows sit across 58 distinct
domains. Store-wide certain-bounce: 94 rows.

**The structural oddity, noted and deliberately not fixed.** `MIN_COVERAGE_PCT = 100.0` at
`clippershq/send_suppress.py:194`, enforced at `:245`, refuses to build a send file whenever any
domain lacks a verdict — and the probe deliberately records *no* verdict for a domain that fails
to resolve, precisely so a transient failure cannot erase a known-dead verdict. Six of 4,152
probed domains therefore have no table entry, and **5 rows in the whole store carry such a
domain**. Any one of them blocks every build, and the refusal message names its own escape
hatch. Reported, not touched.

Also confirmed for the record: the refresh tool's `--from-master` flag is load-bearing. Without
it the source defaults to the send file, whose domains are already fully covered, so the bare
command reports success, changes nothing, and the gate keeps refusing.

### 3.6 Part 3d — typo'd and disposable domains

**Spotify slice, denominator 7,843: 38 rows on a domain within edit distance 1–2 of a major
free provider = 0.485% [0.35, 0.66]**, led by 12 rows one character from the largest provider.
**Disposable providers: 0 rows in every family** — checked against a 42-provider list whose
detector passed its planted positives.

Separately, and more concretely: **9 Spotify rows sit on the TLD `.con`** — the classic
one-key slip from `.com`, not a TLD at all — and **1 sits on a doubled TLD** of the form
`com` immediately followed by `com`, which is a concatenation artifact rather than a typo.

### 3.7 Part 3e — syntactically valid, structurally impossible

Every fault below was rendered as a character mask (letters → `a`, digits → `9`, everything
else verbatim, runs collapsed) so the shape is visible and the identity is not. The masker's own
controls confirm it destroys identity and preserves the fault. **This is deliberately not the
`local[:2] + ".."` redaction, which is the whole local part at two characters — and which is
itself one of the corruption mechanisms this round was hunting.**

**Spotify slice, denominator 7,843:**

| fault | rows | % | 95% Wilson |
|---|---:|---:|---|
| local part is a single character | 13 | 0.166% | [0.10, 0.28] |
| TLD is a known TLD with extra letters glued on | 10 | 0.128% | [0.07, 0.23] |
| more or fewer than one `@` | 0 | 0.000% | [0.00, 0.05] |
| bracket or quote inside the address | 0 | 0.000% | [0.00, 0.05] |
| domain is a file extension | 0 | 0.000% | [0.00, 0.05] |

Masks of the single-character locals, e.g. `a@a{15}.a{3}`, `9@a{13}.a{4}`, and one at
`a@a.a{2}` — a one-character local on a one-character domain label. Two begin with a digit.

**The blank-source family — the original TikTok clipper funnel, 2,924 rows — carries two fault
classes the Spotify slice does not:**

- **24 rows store two or more addresses in a single cell**, joined by `"; "`. The mask makes it
  unmistakable: `a{5}@a{13}.a{2}; a{14}@a{5}.a{3}`. Seventeen are blank-source, seven come from
  an Instagram crawl route, and one holds three addresses.
- **16 rows begin with a literal apostrophe followed by a hyphen** — the text guard a
  spreadsheet inserts when a cell begins with `-`. Two of those sixteen have `'-` as the
  *entire* local part.

**All 40 of these are undeliverable exactly as stored.**

### 3.8 The project's own validator, and what it would have caught

`bio_parser.valid_email` at `bio_parser.py:245-285` is a genuinely good gate: a typo-domain
list, an infrastructure-domain guard, local-part sanity, a TLD allowlist, and a mid-domain
gTLD check. **The Spotify structured route never calls it** — the gate on that path is the
anchored regex at `google_play_finder.py:45`.

Measured by calling the shipped function on every stored address. A clause-attributing
re-implementation was run alongside it and **disagreed with the shipped function on 0 of
12,960 rows**, so the attribution below is the real one.

| family | rejected by the project's own gate | of | % | 95% Wilson |
|---|---:|---:|---:|---|
| **Spotify** | **91** | 7,843 | **1.160%** | [0.95, 1.42] |
| Instagram page funnel | 21 | 1,140 | 1.842% | [1.21, 2.80] |
| Google Play | 8 | 213 | 3.756% | [1.92, 7.23] |
| Twitch / Kick | 8 | 636 | 1.258% | [0.64, 2.46] |
| blank-source | 6 | 2,924 | 0.205% | [0.09, 0.45] |
| everything else | 4 | 204 | — | — |
| **store-wide** | **138** | 12,960 | 1.065% | [0.90, 1.26] |

**Why the 91 Spotify rows fail:** TLD not on the project's allowlist 72, TLD length out of
range 11, **a known typo domain — a certain bounce — 7**, infrastructure domain 1.

**And two faults the gate itself misses**, each proved on a planted control:

- **Two addresses joined by a semicolon pass.** The gate returns *valid* on a planted joined
  pair, and it passes **all 24** of the live joined rows.
- **The apostrophe prefix passes.** The gate's local-part clause tests for a leading `-`, and
  the spreadsheet guard puts an apostrophe *in front of* the hyphen, so the clause never sees
  it. It catches **2 of 16** — only the two whose local part is nothing but punctuation — and
  **misses 14**.

> A control of my own was contaminated here and is reported rather than quietly dropped: the
> first planted "clean address" used a reserved example domain, which the gate correctly
> rejects as infrastructure. It read as a false negative until the domain was changed.

### 3.8b An unrelated leak, found by the commit guard refusing this round's own work

The pre-commit guard refused this round's first commit, correctly, and in doing so surfaced
something that has nothing to do with the Spotify question and matters more than most of it.

Building the clause-attribution probes above, I took the example addresses **straight out of
the validator's own docstring**, which illustrates each rejection clause with a concrete case.
The guard named two of them as living in the gitignored lead store and refused. It was right,
and the probes are now fabricated strings.

**But the docstring is the actual problem.** Running the same guard against the source file
directly: **`clippershq/bio_parser.py` carries four distinct real lead addresses in its
comments — three that live in the lead store and one that lives in the live send file.**

That file is **tracked and long since committed**. The guard inspects staged changes, so it
can only stop the next leak; addresses committed before it existed are already in git history
and stay there. This is the same shape as the two incidents the guard was built for, except
that it is in production source rather than in a scratch artifact, and it has been there long
enough that nobody looks at it.

**It cannot be fixed by editing the file** — that removes them from the working tree and
leaves every one of them in history. Naming it is what this round can do; `clippershq/` is
held by another live round and was not touched.

### 3.9 The regexes, and the one mechanism that cannot be counted

Every pattern below was measured on fabricated inputs, never on real data.

**`bio_parser.py:27`** — `[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}`

**A non-ASCII character silently truncates the local part, and the truncated result ships.** A
local part containing an accented letter is cut at that letter; what survives is a shorter,
perfectly well-formed address that passes the validator and every downstream check. A
zero-width character does the same thing invisibly. The pattern also has no left boundary
guard, so an address abutting preceding text is kept whole.

**This is the single best candidate for bounces that look like nothing is wrong**, and it is
the one mechanism this round cannot put a number on — because counting it requires the source
text, and the source text is exactly what was not kept. That is not a coincidence; it is the
same finding twice.

**`bio_parser.py:409-416`** — the obfuscation reader, case-insensitive. **It fabricates
addresses out of ordinary prose.** A sentence of the form *"<word> at <word> dot <tld>"* is
reconstructed into an address, and the TLD allowlist is the only thing standing between that
pattern and any sentence ending in a common TLD. This is the closest thing to invention in the
entire system — and it is deterministic, not a model.

**`google_play_finder.py:45`** — the final gate. Over-captures in one direction (typo domains,
infrastructure domains, bogus TLDs and leading-punctuation locals all ship because
`valid_email` is never called) and under-captures in the other: a display name, a second
address, or a trailing comma in the source field returns an empty string, which is **silent
lead loss**.

**`enrich_links.py:51-52`** — the first pattern applied to raw markup, so it inherits every
fault above plus capture from JSON blobs and tracking snippets, mitigated by four downstream
filters. Its long-run defuser at `:266-289` can re-cut a run of 128 or more characters abutting
an `@` into a synthetic local part.

### 3.10 Part 4 — sizing it against the whole store

**Denominator: 12,960 rows carrying an address, 12,674 distinct.**

- **Spotify is 7,843 = 60.52% [59.67, 61.36] of every address in the store.**
- Of the **8,574** addresses physically read off an Instagram surface, **7,425 = 86.60%
  [85.86, 87.30]** arrived through the Spotify→Instagram resolution route. The Instagram page
  funnel's own routes contribute 1,016 (11.85%); everything else is under 1% each.
- The stamped TikTok family is 115 rows — but **the 2,924 blank-source rows are 2,850 TikTok
  and 74 Instagram**, written before the `email_source` field existed. **TikTok's real
  contribution is 3,039, not 115**, and any figure computed from `email_source` alone
  understates it by a factor of 26.

**The 4,095 stranded addresses: they were appended, and they are in the audited population.**
The killed run's checkpoint holds 43,717 records and **4,095 distinct addresses; 4,094 of them
— 99.976% — are in the store today.** Across all thirteen Spotify checkpoints, only **3**
distinct addresses ever failed to land.

**Nothing was restored.** The backup twin was located, identified and left exactly where it
is: same filename, same run id, stamped 71 minutes into a run that lasted far longer, holding
**1,870 records against the live file's 43,717 and 0 addresses against 4,095**. A restore
would have destroyed 95.7% of the run and 100% of its addresses. Both files retain their
original modification times.

### 3.11 Part 3f — stale but correct

**Not measurable from disk, and no guess is offered.** The store records when an address was
added, never when it was last valid. The Spotify slice's `date_added` runs **2026-07-22 to
2026-08-30**, all 7,843 rows dated. An address found in that window may have been abandoned
since and nothing here would show it.

### 3.12 Part 5 — the falsehood already in the docs

**The reply-rate claim.** Two prior rounds swept for this; one corrected eleven sites and the
other declared the claim refuted. **A twelfth site survived, carrying the strongest form of the
claim, and it is live production source:**

- **`clippershq/outcome_loop.py:694`** describes the 4–8% band as *"measured on this project's
  own funnel"*, three lines above the constant at `:697`. It is shipped as an expectation at
  `:665`, read back at `:805`, and **rendered in the dashboard's "expected" column**
  (`dashboard/static/app.js:1367-1374`).

**Both sweeps missed it for a mechanical reason worth keeping: the string `4-8` never appears
on that line.** The words sit above a tuple of floats, so every pattern search for
`measured.*4-8` slid straight past. The denominator behind it is **0 of 72,954**.

Twenty further live sites state the band as a target or assumption **and say so** — across
four documents and six modules — and are fine. One site,
`dashboard/static/app.js:1356`, states it as an expectation with no label either way.

**The two replies.** There are exactly two on record in this project's entire history, both
saying "send me the video". They exist only as prose in `scratch/bl1392_build_twenty.py:85-89`,
in a sentence that labels itself: **"n=2 is a hypothesis, not a finding"**. Confirmed as the
only record — 66 CSVs on disk carry an outcome column, 5 hold any non-empty value, and all 5
are test fixtures.

**The send-file row count.** The live send file holds **8,699** rows. **Eleven sites across
three documents quote 2,970** — understating by 5,729 rows, 65.9% low; the live file is 2.93×
the quoted figure. A separate set of sites quoting 2,980 is correctly reconciled in place as a
historical measurement and should be left alone. The figure 8,699 appears in **no document at
all**.

**Nothing was edited.** Seven of these are one-line corrections with no other effect; eight are
larger, because the number is a measurement denominator and rewriting it would assert a
re-measurement that never happened.

---

## 4. What was refused, and why — and the price

**The verbatim test on the Spotify slice was refused by the data, not by me.** 7,843 of 7,843
addresses have no retained source. There is no instrument that can recover it. The price is
exact: **his question cannot be answered address-by-address for 60.5% of his store, today or
ever, and the same will be true of every address that route produces tomorrow.**

**No merge-rule change.** The cross-dedup refusal correctly declines to fold shared role
inboxes, and the counterfactual shows it is preventing 278 of 279 row deletions. Improving it
was explicitly out of scope and stays out.

**No documentation edit**, including the seven one-line ones, because two rounds are live in
this tree and one of them holds `clippershq/` and `config.json`. The corrections are named with
file:line and left.

**No MX refresh.** Running it would have made a network call and changed a production file. The
table is three days old and its verdicts were read as they stand.

**Two of my own zeros were discarded after their controls failed**, and both are in the report
rather than hidden: the MX certain-dead count that read 0 in every family because I guessed the
table's value vocabulary, and the verbatim checker that scored planted truncations as faithful.
A third instrument — the import-closure graph — returned a plausible 83-module answer that is
simply wrong, and is labelled as wrong in place.

**Spend: $0.00.** No vendor call was made by this round, by its own count. The shared ledger is
not used as evidence here: it carries a round id on zero rows and has moved during rounds that
made no calls.

---

## 5. What I got wrong

**I guessed the MX table's shape instead of opening it**, and published-to-myself a
certain-dead count of **0 in every single family**. It was a false zero of exactly the kind
this project has been burned by repeatedly, and the only reason it did not reach this report is
that a zero appearing in all nine families at once is not a finding, it is a smell. The real
figure is 63 rows in the Spotify slice.

**My first verbatim checker called truncation faithful.** A plain containment test scores a
truncated address as VERBATIM because the truncation is a substring of its own source. The
planted control caught it. Had I run the checker without controls, this report would have said
the mangling rate was lower than it is, in the one direction that matters.

**My first structural pass flagged legitimate long TLDs as concatenation artifacts** —
anything beginning with a common short TLD tripped it, so ordinary industry TLDs were counted
as damage. Corrected against a curated list with its own negative controls; the Spotify count
fell from 36 to 10.

**One of my planted "clean" controls used a reserved example domain**, which the project's
validator correctly rejects as infrastructure. It read as a gate failure until I looked. The
control was wrong, not the gate.

**I copied real lead addresses into a control probe.** Building the clause-attribution
instrument I lifted its examples out of the validator's own docstring, not noticing that those
examples are real addresses off the send list. The commit guard refused and named two of them.
Nothing was published or committed — the refusal happened before either — and the probes are
now fabricated. **The guard did its job and I did not do mine**, and the only reason this is a
paragraph rather than a history rewrite is that somebody built that guard after it happened
twice before.

**My role-prefix list is broader than the shipped classifier's**, which is why my Spotify
figure (18.32%) exceeds the list-based one (16.00%) and the shipped classifier's (12.89%). All
three are given; none is presented as *the* number.

**I cannot separate the two mechanisms behind the `resolved-instagram` label**, and I did not
guess. The structured-field read and the bio-regex hit are stamped identically and the
evidence that would tell them apart was discarded.

---

## 6. Money and safety

**No address, local part, domain, artist name or handle appears in this document.** Faults are
reported as counts, as rates with intervals, and as character masks in which every letter is
`a` and every digit is `9`. A mask carries the defect and cannot be reversed to a person. The
`local[:2] + ".."` redaction was deliberately not used anywhere — it is the whole local part
at two characters, and it is one of the corruption mechanisms this round set out to find.

Every instrument this round ran hashes on read and asserts on computed sets, never on
membership of a real record.

**One exception, caught by the commit guard and not by me**: a control probe in
`scratch/bl1485_gate.py` copied its example addresses out of a production docstring, two of
which are real. The guard refused the commit, nothing was published or committed with them in,
and the probes are now fabricated. See 3.8b and section 5.

**Read-only, verified:** no production file written, no config changed, no document edited, no
lead store touched, nothing restored, nothing renamed, no process killed, no vendor call made.
The backup checkpoint twin was opened for reading and left with its original modification time.

**Live-process check, done by the listening-port table and not by a command-line filter** — a
process filter here once matched its own command line and reported two live processes where
there were none. No listener on the dashboard or sheet-server ports; zero Python processes
running. Two other rounds were in flight when this one started: one 243 hours stale, and one
live on `clippershq/` and `config.json`, which this round does not touch at all.

---

## 7. What to do next — ranked, with the arithmetic

**1. Keep the source text. This is the only item that changes what can ever be known.**
Today 7,843 of 7,843 Spotify addresses are unauditable, and 10,071 of 12,960 store-wide. The
store already has a working `bio` column — the TikTok route fills it on 2,742 of 2,891 rows and
that route is 98.27% verbatim-clean *because* it can be checked. The Spotify route fills it on
0 of 7,843. **Recovers 0 addresses today; makes 100% of future ones auditable.** A raw-response
saver already exists at `ig_client.py:867` behind a config flag that is off, but it is one-shot
per endpoint per run and would not be enough on its own.

**2. Call the project's own validator at the structured gate.** `google_play_finder._pick_email`
never calls `bio_parser.valid_email`. **Removes up to 91 Spotify rows (1.160% [0.95, 1.42]) and
138 store-wide.** The unambiguous wins are the 7 on a known typo domain, the 11 with an
out-of-range TLD and the 1 infrastructure domain — **19 Spotify rows that will certainly
bounce**. The remaining 72 fail an *allowlist* clause and will include real leads on legitimate
modern TLDs, so that clause needs a look before it is switched on wholesale.

**3. Split the multi-address field.** **24 rows** hold two or more addresses in one cell joined
by `"; "`. Every one is undeliverable as stored, and the validator passes all 24 — proved on a
planted control. **Repairs 24 rows into roughly 49 usable addresses.**

**4. Strip the spreadsheet text guard.** **16 rows** begin with an apostrophe-hyphen. The
validator catches 2 and misses 14, because its clause looks for a leading hyphen and the
apostrophe sits in front of it. **Repairs 14 rows; 2 more have no recoverable local part.**

**5. Fix the non-ASCII truncation at `bio_parser.py:27`.** A local part containing an accented
or zero-width character is silently cut, and what survives is a well-formed address for a
mailbox that does not exist. **Count unknown and unknowable until item 1 is done** — which is
the argument for item 1.

**6. Probe the six domains with no MX verdict.** 5 stored rows carry one, and
`MIN_COVERAGE_PCT = 100.0` means any single one of them refuses every send-file build. The rule
is right and should not be relaxed; the table just needs those six. Separately, **63 Spotify
rows (0.803% [0.63, 1.03]) and 94 store-wide already have a certain-bounce verdict** and the
suppression layer will drop them the moment it is allowed to run.

**7. Correct `clippershq/outcome_loop.py:694`.** One comment line calls the 4–8% band
"measured on this project's own funnel" against a denominator of 0 of 72,954, and it renders on
the dashboard. **Removes 0 addresses; removes one false claim from live source.** Then the six
other one-line numeric corrections, of which the send-file count at 2,970 against a live 8,699
is the largest.

**8. Decide what to do about the four real addresses committed in `clippershq/bio_parser.py`.**
Three live in the lead store, one in the live send file, all four in the source comments of a
tracked file, all four already in git history. **Removes 0 addresses from the store and 4 from
the public-facing risk surface, but only via a history rewrite** — editing the file cleans the
working tree and changes nothing about what is already committed. It needs a decision, not a
patch, which is why it is listed rather than done.

**9. Decide what to do about role inboxes, which are not a bug.** 16.00% [15.21, 16.83] of
Spotify addresses are role inboxes and 19.51% [18.65, 20.40] have no textual relation to the
artist and are not free-provider addresses. **These do not bounce. They land on the wrong
desk**, which is invisible in every metric this project has. Nothing here says they are wrong;
the number is given so the decision can be made deliberately.

---

## 8. Paths to open

| path | what is in it |
|---|---|
| `clippershq/ig_discovery.py:318-320`, `:327` | the two mechanisms behind one label — the structured field cascade and the bio regex |
| `clippershq/bio_parser.py:27` | the pattern that truncates a local part at the first non-ASCII character |
| `clippershq/bio_parser.py:409-416` | the obfuscation reader that builds addresses out of prose |
| `clippershq/bio_parser.py:245-285` | `valid_email` — the good gate the Spotify route never calls |
| `clippershq/bio_parser.py:263-265` | four real lead addresses in a tracked source comment, already in git history |
| `clippershq/google_play_finder.py:45-69` | the gate the Spotify route uses instead |
| `clippershq/enrich_links.py:320-339`, `:266-289` | the markup-scraping patterns and the long-run defuser |
| `clippershq/crossdedup.py:50-81`, `:185-201`, `:261-281` | the refusal, the merge key, the union-find |
| `clippershq/crossdedup.py:84-114` | the standing open issue on false merges |
| `clippershq/send_suppress.py:194`, `:245` | `MIN_COVERAGE_PCT = 100.0` and where it refuses |
| `clippershq/ig_client.py:867` | the raw-response saver, gated off |
| `clippershq/outcome_loop.py:694`, `:697` | the surviving "measured" reply-rate claim |
| `scratch/bl1392_build_twenty.py:85-89` | the only record of the two replies, self-labelled as a hypothesis |
| `scratch/bl1485_verbatim2.py` | the Part 2 checker and its 15 planted controls |
| `scratch/bl1485_gate.py` | the clause-level attribution of every gate rejection |
| `scratch/bl1485_stranded.py` | the checkpoint-to-store join |

---

## The plain answer

**Did the Spotify run invent addresses? No.** There is no language model anywhere on the path
that produces one, proved by an AST walk with a positive control on a known-live edge, a
negative control on a known-false edge, and a runtime spy with the network stubbed out. Every
address is either a regex hit on text or a copy of a structured API field. Across the whole
store, on the 2,730 rows where the question can be asked at all, **one address in 2,730 —
0.037% [0.01, 0.21]** — is missing from a source that held others, and that one is 0.58 similar
to what the source did hold.

**But nobody can prove it for the Spotify addresses specifically, and nobody ever will.** The
text each of the 7,843 was read from was never written to disk. That is the finding of this
round, and it is a bigger problem than the one he asked about.

**What is actually causing the bounces**, in order of certainty:

- **63 Spotify addresses (0.803%)** sit on a domain that certainly bounces — the MX table
  already knows, and the suppression layer is being blocked by a coverage gate over 6 unprobed
  domains.
- **91 Spotify addresses (1.160%)** fail the project's own validator, which the Spotify route
  does not call: 7 on known typo domains, 9 on the `.con` TLD, 11 with an impossible TLD.
- **40 addresses store-wide are undeliverable exactly as stored** — 24 holding two addresses in
  one cell, 16 carrying a spreadsheet's apostrophe — and the validator passes 38 of the 40.
- **And the one that cannot be counted**: a pattern that silently truncates a local part at the
  first accented or zero-width character, producing an address that looks perfect and belongs
  to nobody. It cannot be counted because the source is gone, which is the same finding again.

None of this is invention. All of it is mis-extraction, and every piece of it is fixable.

<!-- CLAIMS
file:   reports/BL-1485-did-the-spotify-run-invent-addresses.md
const:  clippershq/send_suppress.py::MIN_COVERAGE_PCT
func:   clippershq/bio_parser.py::valid_email
func:   clippershq/crossdedup.py::_is_mergeable_email
-->

https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/BL-1485-did-the-spotify-run-invent-addresses.md
