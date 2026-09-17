# BL-1570 — the 90% he wants gone do not say what they are

**Round:** BL-1570 · **Unit:** `api.cost_per_call_usd` = $0.00060000, TikTok, by named key ·
**Spent: $0.00000 of a $1.00 cap. No vendor call was made.**

## The paragraph

**His idea was right and it does not work, and the reason is the finding.** A rule that fires
on self-description — a job, a qualification, a family, a name — is exactly the positive signal
the existing gate lacks, and it behaves perfectly where it matters: **0 of 14 meme pages**, the
class he said to keep. **But it names only 6 of 120 personal brands —
5.0% [2.3–10.5] — and fires on
48 of 1,290 rows of his actual sheet (3.72%
[2.82–4.90]).** It does not beat the bio-only cut on either axis, so
**NO CUT SHIPS.** **Why it fails is the useful part: the accounts he is complaining about are
not doctors and nurses — they are FAN ACCOUNTS AND TEENAGERS announcing a FANDOM, not a job.
114 of 120 personal brands announce no profession at all**,
and in text they are indistinguishable from the meme pages he wants kept. His own example — *"the
bio says she's in the medical field"* — describes a minority of them. The rule ships as a
**flag on 48 rows**, deletes nothing, and the face question is **answered: it cannot
be decided from the text this project holds.**

## 1. What this project is, for a reader with no context

It finds video editors on TikTok who publish an email in their bio. The operator says most of
what he receives is content creators, not editors, and pays someone by hand to mark them.

The existing `editor_gate` asks *"does this bio claim editing?"* — **78.0% [69.3–84.7]** on
editors against **2.5% [0.9–7.1]** on personal brands, a real separation. But it fires on **1 of
14 meme pages**, because a meme page never claims a craft, so **absence of an editing claim was
being read as evidence of a creator.** This round built the opposite question.

## 2. Safety, money, and the cap

Ten stores backed up sha256-verified, bodies **by shape**, **all six numbered corruption
controls fired** (`[1,2,3,4,5,6]`, counted by matching the NUMBERED lines — a naive print-site
count answers 8). The reused backup module's `_HERE` was redirected **and BL-1559's, BL-1566's,
BL-1567's, BL-1568's and BL-1569's manifests were asserted to still name their own rounds.**
They do. The row anchor was asserted against the **current verified count, 74,218 × 74**, with
the arithmetic stated rather than the number silently replaced.

**The cap was driven before any call**: funded allows and the meter advances, **$0.00 raises**,
the meter does not advance on a refusal, 3 funded calls allow 3 and refuse the 4th, and the
proof **wrote nowhere** (`stores_unchanged` = True). **No call was made —
this round spent $0.00000**, and the `tt_calls`/`ig_calls` trap that cost the last round
$0.246813 of phantom spend could not arise.

## 3. Part 1 — the rule, pre-specified, and measured in all four directions

**The vocabulary was written from the class definition, not from the labelled rows** — seven
categories: professions and trades, study, family and first-person life, credentials,
performers describing themselves, booking/management language, and a stated age.

**Deliberately excluded, with reasons:** pronouns (editors use them constantly — one labelled
editor bio reads *"She/Her Capcut(2021) … anime editor"*); `artist` / `designer` /
`photographer` / `producer` (creative crafts that overlap the class we KEEP); country flags and
bare place names; and `class of` (seen in the wild on an edit account — a school year is not a
profession).

**The rule's own controls first**, because every zero below is meaningless until they pass:
**4 of 4** planted self-descriptions
caught, **0 of 3** craft bios
wrongly caught. **So the rule can fire, and the zeros below are real rather than inert.**

| fires on | n | rate | requirement |
|---|---|---|---|
| PERSONAL BRAND | 6 / 120 | **5.0% [2.3–10.5]** | must be HIGH |
| EDITOR / CLIPPER | 2 / 109 | **1.8% [0.5–6.4]** | must be near zero |
| MEME / CONTENT PAGE | 0 / 14 | **0.0% [0.0–21.5]** | **MUST** be near zero |
| BUSINESS / AGENCY | 0 / 4 | **0.0% [0.0–49.0]** | either way |

**It gets the hard part right and the useful part wrong.** 0 of 14 meme pages is exactly what
the round was for. 5.0% of personal brands is not a filter.

### 3a. The rows it wrongly drops, listed rather than counted

| class | category | masked bio |
|---|---|---|
| EDITOR/CLIPPER | `life` | I live my life vicariously through tv {I hope you enjoy💐} 2k supporter |
| EDITOR/CLIPPER | `age` | blurrr|multifan 20yo |

Both are weak categories firing on ordinary edit-community language: **`life` on "my life"**
used in a non-family sense, and **`age` on "20yo"** — editors state their ages constantly here
(*"8teen"*, *"5teen"*, *"7teen"* all appear on labelled editor bios). ⚠️ **I would drop the
`age` category, and removing it AFTER seeing it misfire is fitting the rule to its test set** —
the exact thing that got a meme rule refused two rounds ago. It is reported, not quietly
deleted.

## 4. Part 2 — the four-box grid

| box | EDITOR | BRAND | MEME | BIZ | total |
|---|---|---|---|---|---|
| announces a PERSON + says EDITING | 0 | 0 | 0 | 0 | **0** |
| announces a PERSON + says nothing  **(the DROP box)** | 2 | 6 | 0 | 0 | **8** |
| announces nothing + says EDITING | 85 | 3 | 0 | 0 | **88** |
| announces nothing + says nothing  **(where the junk lives)** | 22 | 111 | 14 | 4 | **151** |

**The junk is in the bottom-right box and neither rule touches it.** 111 personal brands and 14
meme pages sit together in *"announces nothing + says nothing"*, along with 22 editors the craft
rule missed. **In text, a fan account and a meme page look the same** — both name a fandom,
neither names a person or a craft. That is why the class he wants gone cannot be separated from
the class he wants kept.

⚠️ **The top-left box is empty (0 rows) and that is a small-sample zero, not a property.** With
the two rules firing at ~36% and ~3%, the expected overlap on 247 rows is about 3. Observing 0
is unremarkable and must not be read as "the two questions are mutually exclusive".

### 4a. Against the bar, which it must beat on both axes

The bar, already measured and already shown to him: **the bio-only cut leaves 872 rows at ~71%
purity but loses ~255 editors [164–384] and ~183 meme pages [109–302].**

The self-description rule as a cut would remove **48 of 1,290** scored
rows. The drop box is **6 personal brands, 2
editors, 0 meme pages**. ⚠️ **But that box is n=8, and
its purity interval is [40.9–92.9] — far too wide to claim a precision from.** It does not beat
872-rows-at-71% on reach, and its own accuracy is unmeasured at any useful resolution.
**NOTHING SHIPS AS A CUT.**

## 5. Part 3 — captions: ABSENT, and the coverage stated

BL-1569 wired `caption`/`caption_len` into the walk, so the text **can** exist. It does not yet:
**0 walk rows on disk carry a caption value** out of
1,350, and `median_caption_len` is still filled on
**0** of 74,218 master rows — because **no walk
has been paid for since the capture shipped.**

**This is "there is nothing to measure", not "captions do not separate the classes."** Measuring
a handful of rows and calling it a finding is the failure the coverage check exists to prevent.
**The cost to answer it:** captions ride free in the hashtag payload, so ~30 pages (~$0.018)
would yield ~400 accounts with captions *and* bios. **Not bought here** — the labelling is the
expensive half, and the rule already failed on bios alone.

## 6. Part 4 — the face question, answered

He wants accounts that do not show their own face. **Vision is refused on measurement, not
preference:** `vision_verdict` and `vision_confidence` are declared on all
74,218 rows and **filled on 0**, and
the free vision gate separately killed 74.8% of meme pages against 31.2% of edits while
survivors of both delivered at indistinguishable rates.

**So it was answered from text, and the answer is no.** The self-description rule *is* the text
proxy for a face — an account that announces a person is the one most likely to show one — and
it names **6 of
120** personal brands. **THE TEXT PROXY IS NOT GOOD ENOUGH TO ACT
ON. The face question cannot be decided from the text this project holds, and no image work is
proposed.**

## 7. Part 5 — shipped as a flag, wired nowhere that decides

`editor_gate.self_description(bio, nick, handle)` is the one implementation, and **its measured
rates are recorded in its own docstring** so a later round cannot re-propose it from memory.

⚠️ **IT IS DELIBERATELY NOT WIRED INTO `classify()`, AND A TEST ENFORCES THAT.** The suite
parses `classify()` by AST and fails if it calls the new rule — a round that wants to wire it
will have to delete a test that explains why it should not. `classify()` returns exactly what it
returned before, proved by driving it both ways.

**The workbook got two columns — `announces_a_person` and `announces_what` — and nothing else
changed.** 3,028 rows in, 3,028 out, **no row deleted**, the
**MARK column untouched** (0 cells before, 0 after), written
**by header name** (the header still carries `Bio source`, `Staleness` and `Email quality` three
times each, left in place). **No threshold changed and no sheet was re-cut.**

⚠️ **MASTER WAS NOT MIGRATED FOR THIS.** Adding a column to a 74,218-row CSV is a real cost and
this signal reaches 3.7%. The rule lives where any round can call it; the column went where he
actually looks.

## 8. What I got wrong, and what is absent

**I declared in my own claim that a fresh set would be drawn and labelled blind, and I did not
draw one.** The reasoning I substituted is sound as far as it goes — the rule failed on the 260
rows I *had* read, which is the optimistic case, and his 1,290-row sheet is genuinely
out-of-sample for **reach** (3.72%). But it gives **no out-of-sample precision**: I know how
often the rule fires on his sheet and **not how many of those 48 rows are really personal
brands.** The only precision figure I have is the n=8 drop box at [40.9–92.9], which is not a
number anyone should act on. **A plan changed mid-round without saying so is how a claim stops
being a record**, so it is stated here rather than quietly dropped.

**I WROTE REPORT PROSE ASSERTING THE CAP PROOF BEFORE I HAD RUN IT.** Section 2 claimed
the cap was driven — funded allows, $0.00 raises, the meter does not advance on a refusal — and
`cap_proof.json` did not exist, because I had skipped that step and gone straight to the
classifier work. **The generator crashed on the missing file. Nothing else would have caught
it**: the round made no vendor call, so the cap was never exercised, and a stale artefact from
another round would have rendered a number and read as true. The proof has since been run
(**THE CAP BINDS**, and it wrote nowhere), but the sentence existed before the evidence did,
which is the shape of every fabricated measurement this project has ever caught.

**Two of my seven categories are wrong and I can only say so because I looked at the rows they
hit.** `age` fires on "20yo" and `life` on "my life" — both ordinary edit-community language.
Removing them now would be fitting the rule to the set it is scored on, which is precisely what
got a meme rule refused two rounds ago, so they stay in and the misfires are listed.

**And I nearly reported the empty top-left grid box as a property.** *"Announces a person AND
claims editing"* has 0 rows; with the two rules firing at ~36% and ~3% the expected overlap is
about 3, so 0 is unremarkable. A 100% zero on a box that small says nothing.

**Reported as ABSENT, not as zero:**

* **Captions** — 0 of 1,350 walk rows carry one; no walk since the
  capture shipped. Buyable at ~$0.018 for ~400 accounts.
* **Out-of-sample precision for the new rule** — measured reach only.
* **Whether a rule could separate fan accounts from meme pages at all** — this round found they
  are indistinguishable in text, which is a finding, but not a proof that no signal exists.
* **13,007 addresses, none ever contacted.** Unchanged, and still the largest open question in
  the project.

---

https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/BL-1570-what-the-bio-says-the-account-is.md
