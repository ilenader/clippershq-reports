# BL-1571 — a name does identify a creator, and it is still worth nothing

**Round:** BL-1571 · **Unit:** `api.cost_per_call_usd` = $0.00060000, TikTok, by named key ·
**Spent: $0.00000 of a $0.20 cap. No vendor call was made.** · Investigate only: no production
module, no threshold, no row changed.

## The paragraph

**Nothing new beats the cut that already exists, and the cut that already exists now passes the
bar you just set.** You told me the objective changed: *"I don't care if a few meme pages get
in. The only thing I care about is that there isn't a creator."* Under that objective the
answer is the bio-only craft cut — **keep only accounts whose bio says they edit** — which
removes **117 of 120 creators, 97.5% [92.9–99.1]**, for **24 of 109 editors, 22.0%
[15.3–30.7]**, and what it keeps is **96.6% [90.5–98.8] real editors**. Your name idea is real
and it is measured: a personal name in the display name fires on **7.5% [4.0–13.6]** of
creators and on **0 of 109 editors [0.0–3.4]**, and a lifestyle topic fires on **5.0%
[2.3–10.5]** of creators and again **0 of 109 editors**. Both are clean. Both are also
redundant: **of the 3 creators that survive the craft cut, the name rules catch 0**, and all 14
creators they do catch were already removed. Stacking them on top changes not one row. **So
adopt the craft cut and ship none of this.** The catch is not in the signal, it is in the
inventory: the craft cut needs a bio, **68.1% of your addressed rows do not have one**, and the
one signal that does not need a bio has never been measured on the platform where you would use
it.

## 1. What this project is, for a reader with no context

The project finds video editors on TikTok and Instagram who publish a contact address, so they
can be offered clipping work. A hashtag walk collects accounts, the ones with an address become
leads, and a workbook of ~3,000 of them is the deliverable. The recurring problem is precision:
most rows that carry an address are not editors. Earlier rounds tried to keep meme pages while
cutting the rest. **This round is the first under a changed objective** — creators out at almost
any cost, meme pages welcome — and it re-prices every cut against it, including one this
project previously refused.

## 2. Safety, money, and the cap

No vendor call was made, so nothing was spent and the cap was never exercised. `cap_proof.json`
was written to disk before any sentence here was written about it — a previous round published
the claim that its cap held while the file did not exist. `master_leads.csv` was opened read-only
and is byte-identical. No mark file and no `MARK` column was touched. No handle, address or
unmasked bio appears anywhere in this report; the leak scanner ran lean (the full one was killed
for low memory mid-scan in a previous round, and a partial scan is not a scan).

## 3. The three signals, pre-specified, then measured in four directions

The rules were written from your description before any rate was computed:
`first.last` / `firstNN` / a bare given name in the **email local part**; `"i am <Name>"` /
`"<First> <Last>"` / a bare given name in the **display name**; self-care, travel, finance,
fitness, faith, beauty, motherhood and eleven more topics in the **bio**.

Two things limit what can be claimed and are stated rather than buried. **There is no name
dataset in this repo** — `scratch/infra034_names.txt` is a directory listing and
`bl1528_agentB_09_rule_names.json` holds rule names — so the 291-name list is written from
general knowledge and **a name missing from it is a miss**. Every list-dependent rate below is a
**floor, not an estimate**. That is why the structural shapes are preferred wherever they work:
a shape cannot be absent from a vocabulary. And **a real editor can use their own name** — that
is the obvious confound, and the measurement decides it, not the intuition.

| signal | EDITOR (n=109) | **CREATOR** (n=120) | MEME (n=14) | BUSINESS (n=4) |
|---|---|---|---|---|
| **name in the display name** | **0 — 0.0% [0.0–3.4]** | **9 — 7.5% [4.0–13.6]** | 1 — 7.1% | 1 — 25.0% |
| **lifestyle topic in the bio** | **0 — 0.0% [0.0–3.4]** | 6 — 5.0% [2.3–10.5] | 0 — 0.0% | 0 — 0.0% |
| the existing `name_rule` (the bar) | 20 — 18.3% [12.2–26.7] | 4 — 3.3% [1.3–8.3] | 1 — 7.1% | 1 — 25.0% |
| the craft rule `bio_rule`, for reference | 85 — 78.0% [69.3–84.7] | 3 — 2.5% [0.9–7.1] | 0 — 0.0% | 0 — 0.0% |

**Your intuition is confirmed on the axis you care about.** As a *creator* detector the new
nickname rule beats the existing `name_rule` on both axes at once — it fires on more creators
(7.5% vs 3.3%) and on **zero** editors instead of 18.3%. The two zeros are real, not inert: the
planted controls fire, and one of them caught a genuine bug before any rate was measured (the
`"i am <Name>"` pattern could not match a capital `I`; the fix is scoped `(?i:...)` so the
prefix is case-blind while the name stays case-sensitive). **But 7.5% is a rounding error next
to 97.5%,** and section 5 shows why it does not add to it.

### 3a. Part 1 — the email local part could not be tested properly, and that is the finding

**Only 14 of the 247 labelled rows carry an address at all.** A four-direction table on 14 rows
is not a measurement, so the address rule is reported here as **untestable on the labels** —
untestable, not false. Measured instead on your 3,028-row sheet, against `class_guess`, which is
**a weak proxy and not a label** (it is the gate's own answer, so agreement with it is not
independent evidence):

| class_guess (**WEAK PROXY**) | rows | rule fires | rate |
|---|---|---|---|
| NOT EDITOR | 2,073 | 163 | **7.86% [6.78–9.10]** |
| EDITOR | 680 | 22 | **3.24% [2.15–4.85]** |
| UNKNOWN | 192 | 16 | 8.33% [5.19–13.11] |
| BUSINESS/AGENCY | 83 | 12 | 14.46% [8.47–23.59] |

The separation points the right way and is about **2.4x** — real but small, and measured against
a proxy that is not independent. Shapes that fired: `first.last` 191, bare given name 22. Note
the highest rate is **BUSINESS/AGENCY**, which is a person's name on a company inbox — the rule
cannot tell a creator from an agent.

## 4. Part 4 — captions are ABSENT, with the coverage stated

**0 of 1,350 walk rows on disk carry a caption, and `median_caption_len` is filled on 0 of
74,218 master rows.** The capture shipped in BL-1569 and **no walk has run since**, so there is
nothing to measure. This is an absence, not a refutation. Answering it costs ~30 pages ≈
**$0.018** for ~400 accounts with both a caption and a bio. **Not bought** — the craft cut
already removes 97.5% of creators, so a caption signal would have to beat that, and this round's
own new signals could not improve on it by a single row.

## 5. The whole point — every cut re-priced against your new objective

Ordered by **creators removed** first, **editors lost** second, **meme pages ignored**.

| cut | keeps | **CREATORS REMOVED** | EDITORS LOST | meme lost | purity of what it keeps |
|---|---|---|---|---|---|
| **A — keep only "says EDITING"** | 88 | **117/120 · 97.5% [92.9–99.1]** | 24/109 · 22.0% [15.3–30.7] | 14/14 | **96.6% [90.5–98.8]** |
| B — keep gate-positives (bio OR handle) | 100 | 113/120 · 94.2% [88.4–97.1] | 18/109 · 16.5% [10.7–24.6] | 13/14 | 91.0% [83.8–95.2] |
| **C — A, then also drop "announces a person"** | 88 | **117/120 · 97.5% [92.9–99.1]** | 24/109 · 22.0% [15.3–30.7] | 14/14 | 96.6% [90.5–98.8] |
| D — drop "announces a person" only | 231 | 14/120 · 11.7% [7.1–18.6] | **0/109 · 0.0% [0.0–3.4]** | 1/14 | 47.2% [40.8–53.6] |

**Cut C is identical to cut A in every column, and that is the result of this round.** Adding
both new rules on top of the craft cut changes nothing, because **of the 3 creators that survive
cut A, the new rules catch 0**, and the 14 creators they do catch were already removed by A. The
zero is not an inert rule — the controls fire, and those 3 rows simply do not announce a person.

Cut D is the honest version of your idea standing alone: **it is free of risk and nearly free of
effect.** Zero editors lost is a genuine result, but 11.7% of creators removed leaves what it
keeps at 47.2% purity — barely better than the coin-flip you have now.

**⚠️ Note what cut A costs, because it is the thing you previously refused:** it removes **14 of
14 meme pages**. Under your old objective that was disqualifying. Under the one you just stated
it is not a cost at all. I am not quietly reinstating it — I am telling you plainly that the
cut you need already exists, and that the only thing standing between you and it was a
requirement you have now withdrawn.

**⚠️ And the population caveat rides with every number above:** the 247 labels are a random draw
from master's TikTok bios harvested from **editor-targeted hashtags** — 41.9% EDITOR,
editor-enriched by construction. **They measure separation, not your lead mix.**

## 6. ⚠️ The trap in applying cut A — do not let this one through

Cut A is "keep only rows whose bio says editing". **A row with no bio has no bio hit, so a naive
application deletes it.** The gate calls those rows UNKNOWN, never "NOT EDITOR", and the
distinction is the whole ballgame:

- addressed rows in master: **14,224**
- of those, **judgeable** (have a bio): **4,539 — 31.9%**
- of those, **UNKNOWN** (no bio): **9,685 — 68.1%**

**A naive cut A would discard 9,685 addressed rows nobody has judged — 68.1% of your mailable
inventory — on no evidence at all.** The 22.0% editor loss measured above **is conditioned on
having a bio**; it says nothing about these rows. **Cut A must be applied only to rows that have
a bio, and UNKNOWN must be a hold, not a cut.** (This is the same error a threshold table in
BL-1568 made and had to be corrected for.)

Applied correctly to your 3,028-row workbook: **keeps 680, cuts 2,156, holds 192** pending a bio.

## 7. Instagram — the rules transfer for free, the inventory does not

| platform | rows | with bio | **ADDRESSED** | + bio too | **JUDGEABLE** |
|---|---|---|---|---|---|
| tiktok | 56,680 | 50,998 | 4,158 | 3,961 | **95.3%** |
| **instagram** | 17,210 | 817 | **9,739** | 578 | **5.9%** |
| google_play | 213 | 0 | 213 | 0 | 0.0% |
| twitch | 100 | 0 | 99 | 0 | 0.0% |

The rules are pure text, so they transfer at no cost and need no new code path. **The blocker is
coverage, and it inverts the platform you would expect.** Instagram holds **9,739 of the 14,224
addressed rows — 68.5%, the majority of everything you would mail** — and only 578 of them carry
a bio. **The cut you should adopt is blind on 94.1% of your addressed Instagram rows.** TikTok is
the mirror image: 95.3% judgeable. Buying the 9,161 missing Instagram bios costs 9,161 ×
$0.00069064 = **$6.33**, and the free Instagram page route is dead (six mechanisms eliminated, 0
of 80). Not spent here — this round is investigate-only under a $0.20 cap.

### 7a. The nickname is the only signal that reaches the blind rows — and it is unvalidated there

The display name is a separate field from the bio, so it is the one candidate that can act where
the craft cut cannot see.

| platform | bio? | rows | has nick | nick fires | fire rate |
|---|---|---|---|---|---|
| instagram | **NO BIO** | 9,161 | 7,099 | 2,562 | **36.1%** |
| instagram | bio | 578 | 110 | 19 | 17.3% |
| tiktok | no bio | 197 | 7 | 2 | 28.6% |
| tiktok | bio | 3,961 | 2,787 | 322 | 11.6% |

**The coverage is there: 7,099 of the 9,161 blind Instagram rows — 77.5% — carry a display
name.** **⚠️ But its safety there is unmeasured, and the fire rate itself says so.** On the hand
labels this rule fired on 7.5% of creators and **0 of 109 editors**. Here it fires on **36.1% —
4.8x higher**. A rule validated at 0/109 on *TikTok bios* is being asked about *Instagram display
names*, and **0 of the 247 labels are Instagram rows**. That gap is evidence the populations
differ, not that the rule found more creators there. **It must not ship on Instagram on this
evidence** — firing it would remove 2,562 addressed rows on an extrapolation that has never been
tested. What would settle it: **hand-label ~120 addressed Instagram rows, $0.00**, since they
already carry a display name. That is the cheapest open question in the project.

## 8. What I got wrong, and what is absent

**One bug, caught by a control before it could produce a number.** The `"i am <Name>"` pattern
was written as a single lowercase alternation with no flag, so it could not match "I am
<Name>" — the capital `I` failed `i\s*am` — while the entire point of the pattern is that the
*name* is capitalised. A blanket `re.IGNORECASE` would have been the opposite error, firing on
"i am tired". The fix is a scoped `(?i:...)` on the prefix only. **A planted control caught this
before any rate was measured**, which is the only reason it is a footnote rather than a finding.

**Absent, and named as absent:** captions (0 of 1,350 rows, section 4); the email-local-part rule
in four directions (14 of 247 labelled rows carry an address — **untestable, not false**); and
any Instagram label whatsoever (0 of 247), which is what makes section 7a a warning rather than a
recommendation.

**What I did not do:** I did not build, ship or wire anything, and no threshold moved. Both new
rules exist only in `scratch/bl1571/name_signals.py` and are imported by nothing in production.
Cut A is **recommended, not applied** — that is your call, and section 6 is the condition I would
attach to it.

**Every load-bearing number was re-derived a second way**, by closed-form arithmetic rather than
the loop that produced it: cut A's creators removed (97.50 vs 97.50), editors lost (22.00 vs
22.02) and purity (96.60 vs 96.59) all agree.

### 8a. ⚠️ The full suite verdict was NOT obtained, and I am not rounding that up to green

Three attempts at the full 485-suite run were killed for low memory: the first at ~20 minutes,
the second at **136 of 485 suites**, the third at 13 of 246 chunks. **The cause is not the suite
and not this round** — your own work was running on the same machine throughout (a multi-GB
video render, ffmpeg, node, and two yt-dlp 1080p downloads), with free memory sitting near
**3.2 GB of 24 GB**. None of it was mine to kill, so I adapted the run and then reported what it
actually produced. A partial suite is not a suite run.

What I did obtain: a **targeted run of all 15 suites that reference any module this round's
manifest names — 13 green, 2 red** — plus the partial evidence from the killed run (136 of 485,
13 red). Every red was then settled with the decisive control, `run_all --head`, which runs a
clean `git archive HEAD` extract containing **none** of this round's files, since all of them are
untracked at run time:

| red | at clean HEAD | verdict |
|---|---|---|
| `tests/test_doc_citations.py` | FAILS | not caused by BL-1571 |
| `tests/test_brief_leakcheck.py` | FAILS | not caused by BL-1571 |
| `tests/test_bl1223_speech_reach.py` | FAILS | not caused by BL-1571 |
| `tests/test_bl1225_bed_covers_clip.py` | FAILS | not caused by BL-1571 |
| `memebot/…/test_content_crop.py` | **not present at all** | untracked, gitignored, dated six weeks before this round |

That last one is why it never appeared in BL-1569's baseline: `git archive HEAD` reports "NO
SUITES FOUND" for it, because it is somebody else's untracked file.

**So: no regression was found, and the full-suite gate was not obtained. Those are two different
statements and this round does not merge them.** The structural bound limits but does not replace
the run: this round changed no production code, and nothing outside `scratch/` imports `bl1571`
or `name_signals` — checked across `tests/`, `clippershq/` and `memebot/` — so there is no path
by which any red in the tree originates here.

**And one process note, because the guard earned its keep.** My first two attempts at slicing the
run into memory-bounded chunks were both unsound, and the chunk checker refused to run either.
The first produced the pattern `tests/test_b`, which — because the runner filters by *substring* —
selected all 205 `test_bl*` suites instead of its 8. The second reasoned about a prefix antichain,
which fixes nothing, because a substring can occur anywhere in a label: the pattern `m` matched
122 suites. The third stopped reasoning about the filter and asked it, accepting only chunks the
real filter confirmed. **A chunking that silently drops a suite is a false green, which is exactly
how a broken caption fitter shipped here for a dozen rounds behind "65/65 ALL GREEN".**
