# BL-1588: "faceless" cannot be read from a bio, "for hire" barely appears in one, and nothing tested removes creators without costing editors

**Round:** BL-1588 · **read-only, $0.00, no vendor call** · every store byte-identical at close (35 files:
master, `spend.json`, config, the tag ledger, the workbook hashed as bytes and never parsed, every
`ground_truth/` file) · no suite run · paths redacted · accounts never named, no bio quoted, no handle.
Rules, rubric and decision thresholds were committed **before** any bio was drawn (`3de664ef`); the blind
labels were committed **before** they were joined to anything (`7e8b6e1a`).

**Whose judgement.** Every rate carries one tag, never pooled:
- **[HIS]** his 100 grades (99 join master: 82 EDITOR with a bio, 17 NOT). Survivors only.
- **[247]** the 247 masked labels written by an earlier model (TikTok; the only sample containing cut rows;
  its E class is "EDITOR/CLIPPER").
- **[FACE]** this round's blind face label, written by me from masked text (a model's judgement, one rater).
- **[CUT]** the craft cut's own opinion (`editor_gate.bio_rule`, or master's stored `craft_cut`).

## The paragraph

**Can we tell a faceless channel from text? No, not in the sense he means.** In a fresh random draw of
200 master TikTok bios, the text says the owner is on camera for **5/200 = 2.5% [1.1–5.7] [FACE]**, and
**91/200 = 45.5% [38.7–52.4]** cannot be told at all. The 52.0% that reads "does not show a face" is
**63.5% [53.9–72.1] the craft cut restated**: the account posts edits, and the craft cut already keeps
those. The part that is new information (fan pages, clips, memes, "not impersonating") is 11.0% [7.4–16.1].
Those words mark the pages he **rejects** about as readily as the editors he keeps. Face is also not
what separates his rejects. By a blind reading, **3 of his 17 rejects** are on camera (two musicians, one
athlete), and **0 of his 82 editors** are. The pre-specified face rule fires on **0 of 17 and 0 of 82**.
The face-on commentary channel, the clearest case on record, reads **cannot tell**, and no rule fires on it.
**Only a picture could answer "faceless"** (the avatar or the first frames). That is an image call per
account; it is named here and was not made.

**Can we tell who is available for hire? Available, partly. For hire, almost not at all.** Contact and
promotion wording is common and works as a **rank**:
- "dm for" is on 21 of his 82 editors and 0 of his 17 rejects [HIS].
- The mined contact vocabulary fires on 34 of 35 editors where it fires, **97.1% [85.5–99.5] [HIS]**,
  against a base rate of 82.8%.

But the vocabulary of **labour** barely exists in a bio. In 967 KEEP bios, "hire" appears in **1**,
"freelance" in **3**, and "rates", "slots", "clients" and "fiverr" in **0**. The mined work words ("paid",
"open", "commissions") fire on 2 of his rejects, and **both are edit accounts that are not for hire**. The
text cannot tell someone selling editing from someone selling reach.

**Would either one remove creators without costing editors? No.**
- **Availability as a cut:** every availability signal costs **18–42% of his editors**.
- **The face rule:** removes nothing.
- **The self-description rule:** the only rule under his 5% line on both label sets. It costs 1/82 =
  1.2% [0.2–6.6] [HIS] and removes 2 of 17 rejects. It was refuted before, and its interval crosses the
  line, so it is at most a HOLD.
- **The best HOLD measured:** `name_rule` OR the pre-specified faceless rule. It recovers **11 of 23**
  lost editors, against 7 for `name_rule` alone, taking loss from **14.7% to 11.0% [6.4–18.3] [247]**, and
  it parks 9 non-editors instead of 6. But 3 of the faceless rule's 5 rescues rest on "clips", and it is
  still above 5%.

**Nothing ships.** The one change that would make both halves of his goal measurable is a grading button
(§6). It is recommended, not shipped.

## 1. What this is, for a reader with no context

ClippersHQ finds video editors on TikTok and Instagram and delivers their addresses to one operator. His
goal, unchanged since the start: **faceless editor channels available for hire; no creators, no
businesses.** BL-1586 found that neither "faceless" nor "for hire" is recorded anywhere. No label, grade or
rate measures them, so every rate in the project optimises a proxy. This round asks whether the text
already owned (bio plus display name, 75,540 master rows, 65,972 orphan bios) can carry either one. It spends
nothing and ships no cut. The standing rules: never wrongly cut a real editor; unknown is a hold.

## 2. Part 1: can "faceless" be read from text at all?

**The draw.** The sample has two parts:
- **200 fresh rows**, drawn at random (seed 15880) from the 52,010 master TikTok rows that have a bio.
  This is 90.2% of TikTok rows; the 5,682 with no bio are "cannot tell" by definition. The draw excludes the
  247-set draws and his 100, and the craft cut is not consulted.
- **His 99 joinable rows**, with verdict and platform withheld.

All 299 rows were shuffled together. **Mask first:** four planted address shapes (plain, `(at)/(dot)`,
`[at]/[dot]`, `word at word dot`), all synthetic, were all removed. A clean-prose control survived
unmangled, and a planted own-handle was removed. On the real draw, **0 of 299** masked rows still carried an
address or their own handle.

**The rubric, committed before the draw** (`scratch/bl1588/rules.py`). The three labels:
- **F:** the text says or clearly implies the owner appears on camera.
- **N:** the text says or implies the content is not the owner.
- **U:** everything else, as a real bucket. A job title alone ("editor"), an age or a pronoun is U.

Every N also notes whether its only cue is a craft word.

| fresh draw, n=200 [FACE] | rows | rate |
|---|---:|---|
| **shows own face (F)** | 5 | **2.5% [1.1–5.7]** |
| does not (N) | 104 | 52.0% [45.1–58.8] |
|  of which the only cue is a craft word | 82 | 41.0% [34.4–47.9] |
|  of which a non-craft cue (fan page, clips, memes, not impersonating, anime/game content) | 22 | 11.0% [7.4–16.1] |
| **cannot tell (U)** | 91 | **45.5% [38.7–52.4]** |

**Decision rule D1, fixed in advance:** readable only if U < 50% and F ≥ 20 and N ≥ 20. **Result: NOT
READABLE.** U is 45.5%, but F holds 5 rows, which is too few to measure anything against. Over all master
TikTok rows, counting the bio-less ones: F about 2.3%, N about 46.9%, U about 50.8%.

**"Faceless" by text is mostly the craft cut restated** [CUT]:
- The craft rule already fires on **66/104 = 63.5% [53.9–72.1]** of N rows.
- Its precision for N is 66/73 = 90.4% [81.5–95.3].
- It misses 19 craft-cued N rows, measured rather than guessed:
  - **5 of the 19** carry the cue only in the display name, which `bio_rule` never reads (`name_rule` fires
    on them).
  - The rest carry "multi" (4), "am" (3) and "ae" next to punctuation (2), which the rule does not read in
    that form.

**The tokens driving each bucket** (all 299 rows; only tokens present in ≥ 100 master bios, so no identifier
can print):
- **F (n=8):** "me", "my", "i", "a". Personal pronouns, and nothing about a camera.
- **N (n=178):** "after", "effects", "ae", "multi", "capcut", "vsp" and tool-version years. The craft rule's
  own vocabulary.
- **U (n=113):** "discord", "music", "business", "editor", "video".
- **Address-shaped tokens among the drivers:** none. The `com`-as-Portuguese trap was checked and is not here.

Masked bio length (median / p90) is F 70/74, N 49/91 and U 34/70 characters. U bios are shorter, but not
empty.

**The pre-specified rules against the blind label:**

| rule | fresh: fires on F / N / U | his rows: fires on F / N / U | verdict |
|---|---|---|---|
| `R_FACE` (camera words) | 0/5 · 1/104 · 1/91 | 0/3 · 0/74 · 0/22 | **catches no face-on row**; fires on a planted "daily vlogs and grwm" (control), so the zero is **real, not blind** |
| `R_FACELESS` (non-craft "not me" words) | 0/5 · 3/104 · 0/91 | 0/3 · 11/74 · 0/22 | precise where it fires (3/3, 11/11), recall of N **2.9% [1.0–8.1]** fresh |
| `self_description` (existing) | 0/5 · 1/104 · 6/91 | 1/3 · 1/74 · 1/22 | fires on personal U rows, not on face |

**Against what he said** [FACE × HIS]:

| his verdict | n | F | N | U |
|---|---:|---|---|---|
| EDITOR | 82 | **0 = 0.0% [0.0–4.5]** | 68 = 82.9% [73.4–89.5] | 14 = 17.1% [10.5–26.6] |
| NOT | 17 | **3 = 17.6% [6.2–41.0]** | 6 = 35.3% [17.3–58.7] | 8 = 47.1% [26.2–69.0] |

- **A blind F reading never hit one of his editors.** It hit 3 of 17 rejects: 2 musicians and 1 creator
  (an athlete).
- **The 5 creators he rejected** read U four times and F once. `R_FACE` fires on 0 of 5 and
  self-description on 1 of 5.
- **The face-on commentary channel** (BL-1585's clearest case) reads **U**. Its text is a content type
  (film and TV breakdowns), a job title and a personal display name. None of the 8 signals tested fires on
  it: the three mined families, "dm for", `R_FACE`, `R_FACELESS`, self-description and `name_rule`.
  **BL-1585 called it face-on. Its text does not say so.** That disagreement is reported, not resolved.
- **A face rule does not catch it. Nothing in the text does.**

**What would answer "faceless":** a picture. That means the profile avatar or the first frames of recent
videos, judged per account. That is an image call per account, and it is **named and not made**. Its
price is not derived here. The other route is his own grades with a button that captures it (§6).

## 3. Part 2: the availability vocabulary, mined by frequency ratio

**This follows up BL-1584's mining, which was never followed up. Two changes:**
- **No labelled row contributes a count (D5).** His 100, all 260 of the 247-set draws and this round's 299
  are excluded, 559 handles in all.
- **The words the craft rule itself reads are stripped from every bio before counting.** The first run leaked
  (see §7). The final **circularity control: `bio_rule` fires on 0 of 967 stripped KEEP bios.**

Corpus: master rows with a bio, KEEP 967 against CUT 13,353, split by the stored `craft_cut` [CUT].

**Terms with ≥ 20 KEEP documents: 45, of which 33 have a KEEP/CUT ratio ≥ 3.** Each was classified by
roots registered before the run:

| family | mined terms (ratio ≥ 3, ≥ 20 KEEP docs) | examples of ratio |
|---|---|---|
| **WORK** (labour) | payhip, commissions, for paid, paid, open | commissions 11.3×, paid 8.5× |
| **PROMO** (reach) | for promos, promos, for promo, promo, ads | promo 8.2×, 17.4% of KEEP |
| **CONTACT** | dm for, discord, dm, email for, dm or, or email, mail | "dm for" 7.5×, 18.1% of KEEP vs 2.4% of CUT |

**How the mined terms line up:**
- **"dm for" reproduces BL-1584:** 18.1% vs 2.4% here, against 19.4% vs 2.4% there, with labelled rows now
  excluded.
- **The very top of the table is fragments, not discoveries.** "my s" (100% adjacent to a craft word:
  what stripping "scenepacks" leaves), the tool-version years 2020–2025 (92–100%), "video", "multi" and
  "anime" (91–94%) are flagged by a measured craft-adjacency test. That test was added after the run and
  is descriptive, not pre-registered.
- **The availability terms sit 30–62% adjacent.** They co-occur with the craft word inside the same offer
  ("paid edits"). That is part of why they separate KEEP from CUT.

**The labour vocabulary is below the support floor. It is present, but too rare to rank** (KEEP docs /
CUT docs): hire 1/3, freelance 3/5, portfolio 1/6, prices 1/1, rates 0/3, slots 0/0, clients 0/1,
fiverr 0/0, requests 6/14, commission 9/14, work 15/86. **Most editors he keeps do not describe themselves
as for hire in any countable way.** "Collab(s)", 16/191 and 7/128, leans toward CUT.

**What share of KEEP carries availability** [CUT], master as it stands:

| signal | TikTok KEEP (999) | Instagram KEEP (75) | his editors [HIS] (82) | his rejects [HIS] (17) |
|---|---|---|---|---|
| WORK | 10.5% [8.8–12.6] | 20.0% [12.5–30.4] | 15 = 18.3% | 2, **both "edits, not for hire"** |
| PROMO | 27.8% [25.1–30.7] | 14.7% [8.4–24.4] | 23 = 28.0% | 2 (not-for-hire 1, business 1) |
| CONTACT | 32.3% [29.5–35.3] | 28.0% [19.1–39.0] | 34 = 41.5% | 1 (not-for-hire) |
| "dm for" | 19.5% [17.2–22.1] | 21.3% [13.6–31.9] | 21 = 25.6% | **0** |

**Does it separate his 17 rejects from his 82 editors?** It separates them as a **rank**, not as a label.
Editors carry every family more often, but the words for selling labour and for selling reach are the
same words ("paid", "open", "dm for"). Both WORK hits among his rejects fall in the "edits, not for hire"
box.

## 4. Part 3: every candidate priced on both errors

The asymmetry this is priced against (BL-1585): TikTok leaks about 80 [32–188] creators into KEEP [HIS],
and hides about 616 [420–883] editors in CUT [247]. That is about 8 hidden editors per leaked creator.
Every candidate was tested as a rank and as a hold first, and as a cut only against his 5% line (D2).

| candidate | [HIS] fires NOT / EDITOR | as a RANK: precision where it fires (base 82.8%) | as a CUT on survivors: his editors lost | [247] as a HOLD: lost editors recovered / non-E parked → loss | [247] as a CUT on kept rows: total loss |
|---|---|---|---|---|---|
| **today** | — | — | — | 0 / 0 → **21.1% [14.5–29.7]** | 21.1% |
| **name_rule** (existing, free) | 1/17 · 28/82 | 28/29 = 96.6% [82.8–99.4] | 34.1% | **7/23 · 6 → 14.7% [9.2–22.5]** | 33.0% |
| "dm for" | 0/17 · 21/82 | **21/21 = 100% [84.5–100]** | 25.6% | 0/23 · 4 → 21.1% | 27.5% |
| CONTACT (mined) | 1/17 · 34/82 | **34/35 = 97.1% [85.5–99.5]** | 41.5% | 1/23 · 8 → 20.2% | 31.2% |
| PROMO (mined) | 2/17 · 23/82 | 23/25 = 92.0% [75.0–97.8] | 28.0% | 2/23 · 6 → 19.3% | 26.6% |
| WORK (mined) | 2/17 · 15/82 | 15/17 = 88.2% [65.7–96.7] | 18.3% | 2/23 · 2 → 19.3% | 24.8% |
| `R_FACE` | 0/17 · 0/82 | nothing to rank | 0.0% (removes nothing) | 0/23 · 7 → 21.1% | 21.1% |
| `R_FACELESS` | 3/17 · 8/82 | 8/11 = 72.7% (**below base**) | 9.8% [5.0–18.1] | **5/23** · 3 → 16.5% [10.7–24.6] | 27.5% |
| self-description | 2/17 · 1/82 | 1/3 | **1.2% [0.2–6.6]** | 2/23 · 6 → 19.3% | 21.1% (0 extra) |

**What the table says:**
1. **No cut is available.** Every availability signal as a cut loses 18–42% of his editors [HIS].
   **Self-description passes D2 by its letter:** 1/82 on his set, and 0 more on the 247. But its interval
   runs to 6.6%, it catches 2 of 17 rejects (one creator, one fan page), and it is on the refuted list
   (5.0% of creators, redundant). **Not recommended as a cut.** As a HOLD on KEEP rows it would
   park **12 TikTok and 6 Instagram** KEEP rows [CUT] for his eye.
2. **The ranks are real.** "dm for" (21/21), CONTACT (34/35) and `name_rule` (28/29) each lift precision
   well above his 82.8% base. That means: ship those rows first. It changes his order, not his inbox.
3. **The best HOLD measured is `name_rule` OR `R_FACELESS`** (D3: it must beat `name_rule` alone):

   | hold | recovers (of 23) | parks non-E (of 137) | editor loss [247] | master CUT rows parked |
   |---|---|---|---|---|
   | `name_rule` alone | 7 = 30.4% [15.6–50.9] | 6 = 4.4% [2.0–9.2] | **14.7% [9.2–22.5]** | TikTok 156, Instagram 26 |
   | `name_rule` OR `R_FACELESS` | 11 = 47.8% [29.2–67.0] | 9 = 6.6% [3.5–12.0] | **11.0% [6.4–18.3]** | TikTok 249, Instagram 133 |
   | `name_rule` OR WORK | 9 | 7 | 12.8% [7.8–20.4] | — |
   | `name_rule` OR "dm for" | 7 | 9 | 14.7% (adds nothing) | — |

   **It beats `name_rule` by four editors, at the price of three more parked non-editors.** In accounts, on
   the ~616 hidden TikTok editors, `name_rule` alone would move about 187 into a pile he can see, and the
   combined hold about 295. The intervals are as wide as the 23-row base implies.
   **Two cautions:**
   - **What the rescues rest on:** `R_FACELESS`'s 5 rescues rest on "clips" (3), "memes" (1) and
     "not impersonating" (1). The 247's E class is EDITOR/CLIPPER, and his page defines an editor as
     "someone who cuts clips for others", but whether a clips account cuts **for others** is not in the text.
   - **It fires on his rejects:** "memes" on 2 and "not impersonating" on 1 [HIS].

   **Still above his 5% line.** Recommended only as a HOLD, and only when he grades cut cards.
4. **Second derivations of the load-bearing figures:**
   - **`name_rule` hold:** from the stored `name_hit`/`bio_hit` keys instead of re-running the rules, lost
     24, recovered 6 and parked 6. Loss is 18/109 = 16.5% [10.7–24.6], against 14.7% re-run on masked text.
     The stored keys were computed on the raw bio and the re-run on the masked one, and at least one row's
     craft verdict differs between them.
   - **The 21.1% loss:** the stored-key form is 22.0% [15.3–30.7] (BL-1585).
   - **The orphan "dm for" reach:** 1,884 bios the cut discards, reproduced exactly (§5).

## 5. Part 4: the 65,972 orphan bios, which measure reach and never accuracy

These bios carry no label. The table says how many accounts a signal touches, not whether it is right
about them. The pass reproduces BL-1585: 77,302 keys and **65,972** with a present bio. 5 malformed lines and
1 re-shaped file were skipped and counted.

| signal | reaches | **of which the craft cut discards** |
|---|---|---:|
| `bio_rule` (the cut itself) | 20,629 = 31.3% [30.9–31.6] | — |
| `name_rule` | 8,743 = 13.3% [13.0–13.5] | **3,792** |
| CONTACT (mined) | 4,752 = 7.2% [7.0–7.4] | 2,770 |
| "dm for" | 3,414 = 5.2% [5.0–5.3] | 1,884 (= BL-1585) |
| PROMO (mined) | 2,804 = 4.3% [4.1–4.4] | 1,602 |
| `R_FACELESS` | 2,383 = 3.6% [3.5–3.8] | 1,675 |
| self-description | 1,770 = 2.7% [2.6–2.8] | 1,305 |
| WORK (mined) | 1,018 = 1.5% [1.5–1.6] | **545** |
| `R_FACE` | 835 = 1.3% [1.2–1.4] | 733 |

**The size of the prize before anyone grades anything:**
- **`name_rule` reaches 3,792** accounts the cut throws away.
- **The faceless words reach 1,675.** On the 247, the faceless words recover about 1 lost editor in 5, and
  they also fire on the fan and meme pages he rejects.
- **The labour words reach 545.**

The face words reach 733 accounts the cut already discards. The cut is already doing what a face rule would do,
on the few bios that say it.

## 6. Part 5: the grading button, proposed and not shipped

The live page (`tools/review_loop.py`, which BL-1587 is editing and this round did not touch) offers
**EDITOR / CREATOR / BUSINESS**. His 100 grades were collected on the older EDITOR / NOT page. Neither page can
record "edits, but not for hire", and neither captures a face. His 17 rejects, in the boxes BL-1585
published (reproduced id by id here: `scratch/bl1588/reject_boxes.py`), are 5 creators, 4 edit accounts not
for hire, 3 musicians, 3 fan/meme/news pages and 2 businesses.

**Recommended: four buttons (A).** One more than today, one key more:

| key | button | means | would have caught among his 17 |
|---|---|---|---|
| 1 | **EDITOR FOR HIRE** | edits for other people, or would | 0 (his 83 editors go here) |
| 2 | **EDITS, NOT FOR HIRE** | fan or hobby edit accounts, promo-slot sellers, edit communities | **4** (both TikTok, two Instagram) |
| 3 | **CREATOR** | posts themselves: on camera, personal, a performer or musician | **8** (5 creators + 3 musicians) |
| 4 | **PAGE / BUSINESS** | fan, meme and news pages, labels, companies | **5** (3 pages + 2 businesses) |

**Why four and not more:**
- **What A settles:** it makes "for hire" measurable in one click, and the 4 rows the current page forces
  into CREATOR get their own bucket.
- **Face gets no button.** In this round face separated 3 of 17 rejects and 0 editors, and CREATOR already
  holds face-on accounts. A separate face toggle doubles the clicks on every card to record something that
  moved 3 rows.

**Alternative (B): add a fifth, CAN'T TELL.** It gives his standing rule "unknown is a hold" a button, at
the cost of one more choice per card. His throughput is one page in five. So **A is recommended and B is
his call. Nothing was shipped.**

## 7. What I got wrong

1. **I tried to claim BL-1587 while another live round held it.** My directory listing at 18:04 did not show
   it; the claim tool refused. Nothing was written under that id, and this round is BL-1588.
2. **My personal-rule wrapper returned the truth value of a tuple.** `self_description` returns
   `(fired, categories)`, so `bool()` was always True. A negative probe ("anime edits | fan page" read as
   personal) caught it before the pre-registration commit.
3. **A false zero.** His file spells a reject `NOT_AN_EDITOR`. My first scoring run keyed on `NOT` and
   printed **n=0 rejects**. Caught from the output, fixed, and the script now asserts 83/17 before it scores.
4. **The first mining run leaked the craft rule into the corpus.** Stripping happened before punctuation was
   collapsed, so "ae/" and "scene-pack" became new craft matches in 6 of 967 KEEP bios. The circularity
   assertion stopped the run, and the final run strips again after the collapse and reads 0.
5. **I first tagged craft-adjacent terms "CIRCULAR" at a 50% cut, post hoc.** That would have mislabelled the
   availability terms, which co-occur with craft words inside real offers. The tag is now "FRAGMENT" at
   ≥ 90%, and described as not pre-registered.
6. **I ran one empty shell heredoc** (a no-op) against this round's no-heredoc rule. It wrote nothing.
7. **The mask has a known hole.** It removes addresses (0 of 299 left), the row's own handle and ASCII
   at-sign mentions. Other accounts' handles written bare ("IG: name") or in styled Unicode survive in the per-row
   reading file. That file was kept outside the repo and is not committed. The leak scan below covers
   everything that is.
8. **One rater, and the rater wrote the rules.** The rules were committed before the draw and the labels
   before unblinding, but no second rater measured agreement. Four consistency calls were made while
   labelling and are recorded in `face_labels.py`: a tool word or "edits" describing content is N; "editor"
   alone is U; an age or pronoun alone is U; a performing musician or live streamer is F. A different call on
   musicians moves 2 of the 3 F rejects.
9. **His denominators are 82 editors, not 83.** One graded row does not join master.
10. **My scoring script printed a guess as if it were a measurement.** The line about the 19 missed
    craft-cued rows named `vsp` as a word the rule cannot read. The rule does read it. That line is now
    measured (§2), and the report quotes the measurement.
11. **The leak scan flagged two ordinary words in my own prose.** Each matches some account's handle and
    appears in only 6 and 51 master bios, below the 100-bio vocabulary bar. Both were rephrased in the report
    and in `avail.py`. One of them stays in the already-committed pre-registration docstring, `rules.py`, and is
    disclosed here rather than edited after the fact. The other two hits in that file are shaped like
    at-sign handles, and both are mine: the planted `.invalid` control address, and the word "mentions"
    written with an at sign.

## 8. Assertions at close

```
store files (35: master, spend.json, config.json, email_harvest_tags.json, the workbook, bl1572 results,
             every ground_truth/ file incl. the label store and every mark file)
diff start -> end: 35 vs 35 files, 0 moved
MARK: never opened (the workbook was hashed as bytes, never parsed)
suites: none run. vendor calls: 0. network: GitHub reads + the publish push only
mask controls: 4/4 planted address shapes removed, clean prose intact, own handle removed; real draw: 0/299 address, 0/299 own handle
circularity control: bio_rule on stripped KEEP bios 0/967
verdict control: EDITOR 83 / NOT 17 read from his file before scoring
family controls: each mined family fires on its planted phrase and not on clean prose
files written: scratch/bl1588/* and this report; per-row reading files outside the repo, not committed
concurrent: BL-1587 is live and editing tools/review_loop.py + tests; this round did not touch either
```

**What would settle the open halves:**
- **Faceless:** his grades with a CREATOR button and a picture-based check. The image call is named, not made.
- **For hire:** the EDITS, NOT FOR HIRE button on one graded page.
- **Whether the `name_rule` + faceless HOLD is worth its 3 extra parked non-editors:** his grades on cut
  cards.

**Nothing in this report changes what he receives.**

https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/BL-1588-faceless-and-for-hire-measured.md
