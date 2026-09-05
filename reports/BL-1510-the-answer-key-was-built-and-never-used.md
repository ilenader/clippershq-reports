# BL-1510 — The answer key was built, tested and shipped. Nobody has ever handed it a file.

**Round:** BL-1510 · **Date:** 2026-09-06 · **Spend: $0.00** — no vendor call, no network
request, no DNS query, by me or by any of the three sub-agents.

---

## The answer, in one paragraph

**Yes, this funnel can be checked against reality, and the machinery to do it already exists.**
I went looking for a missing outcome recorder and found a complete one: `clippershq/outcomes.py`
is 847 lines, has production callers, passes 63 existing tests, and wrote all nine outcome
columns correctly the moment a spy drove it. It has also never written a single real outcome in
this project's history — **43 master backups covering 2,752,359 rows carry all nine outcome
columns and not one value**. There is even an ingestion path: it reads a bounce CSV *or a plain
mail log*, matches on handle or address, and refuses ambiguous keys rather than guessing. **The
smallest step is therefore not to build anything. It is for him to save one bounce report out of
the sender he already runs daily and point one existing command at it.** What that settles, and
nothing else can: **deliverability**. Until you know what fraction of addresses even arrive,
every reply rate is computed over a denominator that is wrong by an unknown amount — so bounce
data is not merely the cheaper column, it is *upstream of the reply column being interpretable at
all*. The honest counterweight is that the reply column he actually wants is far out of reach:
a usable per-brain reply rate needs **about 60 replies per arm**, which at 2% is **15,265 sends
across five funnels — more than his entire 12,967-address inventory.**

---

## 1. Round ID, date, and what it was asked to do

BL-1510, 2026-09-06. Read-only first, then at most one small write. Map what exists on the
outcome path; price what one outcome column would be worth; census the addresses; size the
false-merge exposure; then propose the smallest write-back and ship it **only if small and
safe**.

**The standing rule was honoured throughout.** `docs/NO_SEND.md`: this project produces leads
and does not contact anyone. Reading a result back is in scope; nothing about messaging is. No
sender, pitch, template, subject line or send order is proposed anywhere in this report.

Three sub-agents ran in parallel — the outcome path, the address census, the merge exposure —
and two of them derived the master row count independently and agreed.

---

## 2. What actually shipped

**One file: `tests/test_bl1510_outcome_writer.py`. No production code was changed.**

That is the correct outcome of Part 4 rather than a shortfall. The brief said to ship a column
and its writer *only if small and safe*, and otherwise to specify and stop. The writer already
exists, so there was nothing to build; what was missing was any standing proof that it works.
The new file drives the real `record_outcome` on synthetic fixtures and pins nine behaviours:
all nine columns written, the neighbouring row untouched, an unmatched key writing **nothing**
(asserted byte-identical), an **ambiguous key refused rather than guessed**, an address joining
the same way a handle does, and — separately — that the console *refuses* to print a rate when
nothing has been sent, with a control proving it *does* print once something has.

Every fixture is stamped `bl1510fixture` on a reserved `.example` domain. Nothing in it reads
the lead store. **9 tests, all 9 executed and passing** (counted, not assumed). The 63 existing
outcome tests still pass.

---

## 3. What was measured

### 3.1 The nine columns are empty, and the control fired

`date_sent`, `sent_channel`, `replied`, `reply_sentiment`, `bounced`, `converted`,
`outcome_notes`, `touch_number`, `message_variant`.

| | |
|---|---|
| rows carrying a value, each of the nine | **0 / 72,961** · Wilson 95% [0.0000, 0.0053] |
| **positive control** — same reader, same rows, ≥3 *other* non-null fields | **72,960 / 72,960** (100.000% [99.9947, 100]) |
| never non-empty **ever**: 43 master backups carrying all nine | **2,752,359 rows, zero values** [0.0000, 0.0001] |

The reader is fine. The columns are genuinely, historically empty. Fifteen *further* columns are
also 0/72,961 and are **not** outcome columns — worth knowing before anyone reads an empty
column as a defect.

### 3.2 A writer exists, works, and has simply never been driven

`clippershq/outcomes.py` — `record_outcome:605`, `apply_outcome:237`, `mark_sent_from_csv:345`,
`mark_bounced_from_csv:501`, `_rewrite_master:416`.

**Runtime spy, with its control.** Counters read zero on import; driving `record_outcome` on a
synthetic two-row fixture moved them to `record_outcome +1, apply_outcome +1,
normalize_outcome +2`, wrote **all nine columns**, and reported `matched: 1`. The spy
demonstrably fires, so the zero it reports in production is a real zero.

**Production callers** (tests and scratch excluded): the interactive `[o]` menu at four sites in
`control.py`, `run.py:946` (`--mark-bounced`, **dry-run by default**), and `tools/mark_sent.py:44`.
**No funnel calls it.** The finders and the writer carry the columns through blank.

**So the gap is a missing operator step, not missing code.** That is a very different problem
from the one the brief anticipated, and a far cheaper one.

### 3.3 The import graph, and the gate that had to go green first

This repo has burned two previous import graphs — one orphaned both live finders because the
runner dispatches funnels from **string literals in a dispatch table**, another missed the
**PEP-420 bare sibling imports** and orphaned seven more modules. So the graph built here
resolves four edge kinds, including string constants matching a module stem, and was **validated
before any zero was allowed out**: all three known-live modules came back alive, with both
import and string edges. Only then: **60 of 209 production modules have no production importer**
— untriaged, and the repo's own sweep tool documents that many orphans are refusals by design.

### 3.4 The join key: there is no row id

| candidate | non-null | distinct | note |
|---|---:|---:|---|
| handle | 72,960 | **72,945** | 15 duplicates |
| address | 12,966 | — | **286 duplicate rows** |
| a secondary uid | 55,752 | — | 17,208 blank |
| run id | — | **32** | a run id, not a row id |

The real join is `build_key_index:274`, which normalises handle / second-platform handle /
address and — carefully — indexes **both the raw cell and the exporter-repaired address form**.
**Ambiguous keys are refused, not guessed.** What is missing is an opaque per-row id that would
survive a handle rename or an address repair.

### 3.5 The sender ingestion point exists, and is file-only

`read_bounce_keys:458` accepts a bounce CSV **or any plain text mail log**, scanning it for
addresses; `mark_bounced_from_csv:501` stamps the rows and reports `not_marked_sent` separately
rather than silently. Driven by `run.py --mark-bounced <file> [--apply]`, `tools/mark_sent.py`,
and the `[o]` menu.

**Absent:** no mailbox reader, no mail-service webhook or API client, no scheduled ingestion.
Every path needs a human to hand it a file, and nobody ever has.

### 3.6 The invented reply rate: 107 sites, not five — and only one that matters

The brief said "4-8%" appears in five places. **It appears in 107 — 14 live, 93 historical.**
That is a correction in the unhelpful direction, so the useful finding is the breakdown:
**13 of the 14 live sites explicitly disclaim it** ("an ASSUMPTION, not a measurement", "IF the
rate were"). The Python sites are scrupulous about it.

**The one place it is presented without a disclaimer is the operator-facing panel**, which
renders an **"expected"** column computing 4-8% of the send count as a target. I nearly reported
the panel for a different and wrong reason — see §5.

**The n=2 sentence lives at `scratch/bl1392_build_twenty.py:85-89`**: *"The only evidence this
project has is TWO replies, both saying 'send me the video'… n=2 is a hypothesis, not a finding,
and twenty sends cannot promote it to one."* It is restated in shipped code at two further
sites. It exists only as prose — **no JSON, CSV or row anywhere records a reply.**

### 3.7 What one outcome column is worth

**A reply rate needs about 60 replies per arm, at any true rate.** That invariant is the whole
answer:

| true reply rate | n for ±2 points | **n for ±25% relative** | replies needed |
|---|---:|---:|---:|
| 1% | 150 | **6,173** | 61.7 |
| 2% | 223 | **3,053** | 61.1 |
| 4% | 386 | **1,493** | 59.7 |
| 8% | 713 | **713** | 57.0 |

The ±2-point column is a trap: at a true 1%, n=150 gives an interval containing zero. **Per
brain, five funnels at 2% needs 15,265 sends — more than the entire 12,967-address inventory.**

**His volume cannot be determined from disk, and I will not guess it.** No send is recorded
anywhere. Discovery *is* measurable and bounds sends from above: 4,682 addresses in July,
8,247 in August. Even assuming he mails 100% of discovery, a per-funnel reply rate is a
multi-quarter proposition.

**A bounce is a different ask entirely.** It is mechanical, arrives in bulk, and is volunteered
by the world without anyone choosing to reply. A 5% bounce rate reaches ±2 points at **n=469**.

### 3.8 The address census

**Snapshot discipline first:** `master_leads.csv` is live — two consecutive reads returned
72,960 then 72,961 rows, because another process appends while you read. Every figure below is
against one in-memory snapshot with a recorded hash.

| | |
|---|---|
| rows carrying an address | **12,967 of 72,961 = 17.77% [17.50, 18.05]** |
| distinct normalised addresses | 12,705 |
| date range | **2026-06-30 → 2026-09-05**, 0 blank, 0 unparseable; 78.5% written in July |

**MX — the flag is load-bearing, exactly as the brief said.** The bare refresh command reads a
previously-built send file; the flag `--from-master` reads the real current set.

| population | domains | uncovered | coverage | gate |
|---|---:|---:|---:|---|
| bare-command default (send file) | 2,252 | 2 | 99.911% [99.68, 99.98] | **REFUSES** |
| real current (master) | 4,155 | 9 | 99.783% [99.59, 99.89] | **REFUSES** |

**A bare refresh cannot see 1,903 of 4,155 master domains — 45.80% [44.29, 47.32].** All
refusals are coverage below a 100.0% floor, not staleness (the table is 6 days old against a
7-day limit). By set arithmetic, `--from-master` would close all nine gaps; a bare refresh
closes at most two. **No probe was run — this round makes no network call.**

**Structurally impossible addresses are almost entirely absent.** Denominator 12,967 addressed
rows; every mechanism counted separately, and **every zero carries a control that fired**:

| mechanism | rows | rate |
|---|---:|---|
| local part ≤ 2 characters | **145** | 1.118% [0.951, 1.314] |
| local part exactly 1 character | 15 | 0.116% [0.070, 0.191] |
| starts with punctuation | 16 | 0.123% |
| consecutive dots / trailing dot | 1 / 1 | 0.008% each |
| empty local · domain with no dot · ends in punctuation · whitespace · control char · non-ASCII · leading dot · doubled TLD · more than one `@` · concatenated pair · invalid TLD shape | **0** | each [0.000, 0.030] |

Two findings that need words rather than a number. **The 16 leading-punctuation rows are all a
spreadsheet formula-guard apostrophe** — an artefact of storage, not of extraction. And **the
short local parts are largely real**: 0 of 145 are on free webmail, all 145 are on custom
domains, 141 of 143 appear exactly once, and 143 of 145 trip no other defect. A one- or
two-letter mailbox on your own domain is an ordinary thing to have.

**Typo'd and disposable:** 9 rows on the shipped known-typo list (0.069%), 33 at edit distance
1-2 from a major provider (0.255% [0.181, 0.357]), and **0 on any well-known disposable
provider** — with the control firing, and with the honest caveat that the reference list is 83
providers, so this is "none of the well-known ones", not "none in the world".

**Shared and role inboxes — and the refusal is correct.** 424 of 12,967 rows sit on a shared
address (3.270% [2.977, 3.590]) across 138 addresses. Calling the *shipped* rule rather than a
reimplementation: **it refuses 135 of 138 = 97.83% [93.80, 99.26]**. And the reason matters —
**role status is not the main cause**: the agency/management check refuses 96, role-or-weak 34.
**The rule was not modified, not worked around, and not proposed for modification.**

### 3.9 The false-merge exposure

The identity key is **the whole address, verbatim**, under a transitive union-find: one shared
string means one human. The guard meant to catch a manager's inbox is **word-list bound** — it
knows `booking@` and the words *talent* and *management*. **A management company with an
ordinary name and a first-name mailbox is indistinguishable from an artist's own domain**, and
the module's own self-test asserts that exact shape is one person. The failing case is
structurally identical to the passing fixture.

**The loser is not written anywhere.** Handle, display name, followers, country and URL are
discarded in memory; only two fields change on the survivor. Reproduced on synthetic fixtures:
*appended 0, merged 1, losing handle survives nowhere.*

| | |
|---|---|
| duplicates still in master (merges not yet performed) | 6 humans / 11 extra rows |
| **keys with the shared-manager shape** | **1,277 of 10,094 = 12.65% [12.02, 13.31]** |
| master rows those sit on | 1,272 = **9.81% [9.31, 10.33]** of addressed rows |
| concentration — domains carrying ≥2 risky keys | 121 (334 keys); one carries **9** |
| recorded merges that landed on a risky key | **20 of 101 = 19.80% [13.20, 28.62]** |
| agency-shaped keys admitted anyway via an owner-token escape | 372 of 10,094 |

**There is no audit trail, and that was proved rather than assumed.** For a same-funnel merge:
no absorbed identity recorded, **no backup**, no log line, and the master bytes are identical.
One sweep recorded 2,781 offered → 810 appended, **1,971 merged** — printed to a console and
written nowhere. Sharpest detail: **the three deletions named in the standing comment were all
same-funnel, so they are not among the 101 recorded merges and never could have been.**

**One bypass worth naming:** a second dedup layer keys on raw addresses with no role filter at
all, and was driven to confirm it — two different handles sharing a role inbox come back as
duplicates. It accepts exactly what the careful rule refuses.

### 3.10 A missing outcome that reads as a measured zero

`_rate` returns `0.0` when its denominator is zero, so "we have never sent" and "we sent and
nobody replied" produce the same number. Five further sites turn a blank cell into `False`, and
the master rewrite coerces `None` to `""` on every pass — so the None discipline has to be
enforced **on read, never on write**.

**Nothing user-facing currently lies about it:** both the console and the panel short-circuit to
"nothing marked sent yet" before rendering. The raw stats dict does not, and that is pinned as a
defect by the new test rather than endorsed as a contract.

---

## 4. What was refused, and why

* **Building an outcome writer.** One exists, works, and ships. Building a second would have looked like progress.
* **Changing `_rate` to return `None`.** Correct in principle, but it has a panel consumer and an existing test asserting `0.0`. That is a behaviour change, and this round's own instruction was to specify rather than ship it.
* **"Improving" the merge rule.** Explicitly out of bounds, and the refusal is right.
* **Any live MX or DNS probe.** $0.00 and no network. File-versus-file only, and said so.
* **Attributing his reported bounces to the structural defects.** Every mechanism is ≤1.12% and most are exactly 0. Nothing in the store records a bounce, so no bounce can be attributed from disk at all. The supportable candidates are the 9 uncovered domains and the 94 dead/null-MX entries the table already holds.
* **Guessing his send volume.** Not determinable from disk. Discovery bounds it from above; that is all.
* **Backfilling anything into the 72,961 rows.** No guess was written.

---

## 5. What I got wrong, and what the brief got wrong

**Mine:**

* **I nearly published the wrong half of the panel finding.** I had it as rendering a false 0% reply rate. It does not — it already short-circuits to "Nothing marked sent yet". The real defect is one step over: an **"expected 4-8%"** column shown with no note that the figure was never measured here. I checked before writing, and only just.
* **A sub-agent's framing needed correcting too** — it named the panel comment as "the one un-disclaimed live site the operator sees". The comment is a comment; the operator-visible artefact is the expected column. Same conclusion, different object.
* **My own instrument was inflating a published number.** `mark_reader.self_consistency` groups on `(platform, handle)` — the unstable key I fixed in `resolve()` last round but did not fix in its sibling. Stabilising it moves the ceiling **93.9% [91.9, 95.4] → 91.8% [89.5, 93.6]** page-level and **92.6% → 89.0%** pair-level, because **281 pairs straddling the split were never compared**. My first hypothesis for the mechanism — that whole repeat pages were being dropped — measured **0** and was wrong; the pairs were the mechanism. It has 8 external callers, **all in `scratch/`**, so it cost past rounds' analyses and nothing shipped. **The 75.6% sittings ceiling is unaffected** — that comes from the sibling function, which already fixes the key.
* Two sub-agent matchers were **caught lying by their own controls and discarded before publication** — one reported 151 false positives (1.19%) by matching a two-letter sequence inside an ordinary surname. Those numbers never reached this report, which is the system working.
* **My leak check reported four artefacts clean and there were five.** The fifth carried 2 real addresses and the pre-commit guard caught it — see §6. I had applied the round's own "prove the zero" rule to my detectors and not to my *file list*, which is the same error one rung up.
* **My first handle-leak detector flagged two false positives**, both ordinary English nouns in my own prose that happen to also be somebody's handle. Narrowing the rule then risked narrowing it to nothing, so the fix came with a control that plants a *real* distinctive handle into a copy of the report and confirms it is still caught.

**The brief's:**

* **"72,956 rows / ~12,956 addressed"** → **72,961 / 12,967**, derived independently by two agents. The store grows while you read it.
* **"4-8% appears in five places"** → **107 sites** (14 live). And 13 of the 14 live ones already disclaim it.
* **"MX 92.52% → 99.85%"** → a snapshot from six days ago on a smaller store. Today: **99.783% master / 99.911% send file**. The *mechanism* the brief describes is confirmed exactly.
* **"The stale file's domains are already 100% covered"** → **99.911%**, two missing. The substance holds: a bare refresh closes at most 2 of the 9 gaps.
* **"420 of 4,433 rows share an address, 9.47%"** → not a slice of this store at all; it is a killed run's pre-dedup export. The live figure is **3.270% [2.977, 3.590]**, and **the intervals do not overlap**.
* **"The merge refuses 69 of 72"** → the shape reproduces and is stronger: **135 of 138**.
* **"83 of 8,198 short local parts"** → an August snapshot, and **8,198 was ROWS carrying an address, not distinct addresses** — three places in the project call it "addresses" and are wrong. Live: **145 of 12,967**.
* **"11 car-edit pages" is not this round's, but the same pattern holds throughout:** figures handed down in briefs here are usually directionally right and numerically stale.
* **The brief's premise that the outcome path is unbuilt.** It is built. That is the round's headline and it inverts the framing.

---

## 6. Money and safety

**$0.00.** No vendor call, no network request, no DNS query — by me or by any of the three
sub-agents. Verified by each agent independently and by the run's own accounting, not by a
ledger delta (`spend.json` is shared and moved during the round because other rounds are live).

**Addresses.** No address, local part, or row-bearing domain appears anywhere in this report.
Role **prefix categories** are published as shapes; the addresses behind them are not.

**And my own leak check missed a file — the commit guard caught it.** I byte-scanned the four
agent JSON artefacts and reported them clean, which they were. There was a fifth artefact: a
157 KB raw grep-hits file, and it carried **2 real addresses** from the lead store. The
pre-commit guard refused the commit and named the file. I did not use `--no-verify`; the two
values were replaced with a salt-free hash carrying **no local part and no domain**, the file
re-verified at 0, and only then was it committed. The lesson is the round's own rule turned on
me: *a scan that reports "all four files clean" has only proved something about the four files
it looked at.* The guard was the control I did not run myself.

**A defect found while fixing that: the shipped redaction helper is unsafe on short local
parts.** `write_point_guard.redact()` renders an address as `local[:2] + "**@" + true_domain`.
For a local part of one or two characters, `local[:2]` **is the entire local part**, so the
"redacted" output is the complete address. Demonstrated on synthetics: a two-character local
comes back whole, a nine-character one does not. Agent B measured **145 rows whose local part
is ≤ 2 characters**, so this is live, and it is the exact redaction form this round's brief
names as forbidden. Not changed here — it is a shared helper and another round holds files
near it — but it is ranked below.

**Concurrency.** Three other rounds were live throughout. The seen stores **only grew** (+38 and
+3 rows) and no row key was lost. Seven `clippershq/` files and the dashboard state are dirty in
the working tree — **those are other rounds' writes; this round changed no file under
`clippershq/`, `dashboard/`, or `tools/`.** The commit is by explicit path.

**Tests.** 9 new, all 9 executed. 63 existing outcome tests pass. No judging rule was added or
loosened, no threshold moved, and no verdict can move — no production code was changed at all.

---

## 7. What to do next — ranked

1. **Save one bounce report from the sender and run the existing command.** `run.py --mark-bounced <file> --apply`. It already validates, refuses ambiguous keys, and flags rows lacking a send date. This is the entire ask, and it is one file plus one command.
2. **Record `date_sent` alongside it.** A bounce with no send date is unattributable; the tool already reports those separately rather than silently.
3. **Fix the "expected 4-8%" column** to say what the Python already says — that it is an outside rule of thumb, never measured here. It is the only place the invented figure is presented as fact to the person making decisions.
4. **Give the merge an audit trail before it runs again.** Not a rule change — just recording what was absorbed. 1,277 keys carry the shared-manager shape and a wrong merge currently deletes a person and reports nothing.
5. **Use `--from-master` on every MX refresh.** The bare command cannot see 45.8% of the live domains and will keep reporting success while the gate keeps refusing.
6. **Fix `write_point_guard.redact()` for short local parts.** It keeps `local[:2]`, which for a one- or two-character mailbox is the whole thing, so the "redacted" form is the complete address — on 145 live rows. Every report that has used this helper should be re-checked. Small, mechanical, and it is the difference between a redaction and a disclosure.
7. **Treat the reply column as a slow accumulator, not a metric.** Report it blended until an arm reaches ~60 replies. Per-brain reply rates are multi-quarter at his volume, and publishing one earlier would be noise with a decimal point.

---

## 8. Paths to open

* `tests/test_bl1510_outcome_writer.py` — the round's only write; 9 tests pinning the writer that already exists
* `clippershq/outcomes.py` — the recorder, the ingestion path, and the zero-denominator hole
* `scratch/bl1510_agentA_outcomes.md` — the nine columns, the spy, the validated import graph, every "4-8%" site
* `scratch/bl1510_agentB_addresses.md` — the address census, 17 mechanisms with 34 controls, and the two matchers discarded for lying
* `scratch/bl1510_agentC_merge.md` — the false-merge mechanism, the exposure, and the n-needed arithmetic
* `scratch/bl1510_ceiling_key.py` — the consistency-ceiling key finding and its second derivation
* `docs/NO_SEND.md` — the standing rule this round stayed inside

https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/BL-1510-the-answer-key-was-built-and-never-used.md
