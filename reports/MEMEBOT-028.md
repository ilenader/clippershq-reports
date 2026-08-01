# MEMEBOT-028 — precision per tier, and whether tone is in the sentence

*2026-08-01. READ-ONLY on the matcher and on `clip_library/`; writes `scratch/memebot028_*`
only. No paid calls. BL-849, BL-863, BL-864 and BL-867 were all writing the library while this
ran — vision labelling crossed **50%** during the round.*

MEMEBOT-022 noticed a pattern in 14 clips. This measures it in 44 more, and the pattern holds
hard enough to change the tier order: **the vision tier is 60% right, franchise is 33% right on
the fifth of it anyone can check, and title is 8% right.**

---

## 1. PRECISION PER TIER

15 vision matches sampled evenly, plus **every** franchise match (15) and **every** title match
(13) — those tiers are small enough to read end to end. Verdicts typed by reading each clip's
description, recorded against `clip_id` in `scratch/memebot028_audit.py`.

A fourth verdict was needed: **BLIND** — the clip carries no vision label at all, so nobody can
say what it shows. Counting those as "not wrong" would have hidden the finding.

| tier | audited | RIGHT | WEAK | WRONG | BLIND | RIGHT of *checkable* |
|---|---|---|---|---|---|---|
| **VISION_RULE** | 16 | **9** | 5 | 1 | 1 | **60%** (9/15) |
| **FRANCHISE_MOOD** | 15 | 1 | 2 | 0 | **12** | **33%** (1/3) |
| **TITLE_MOOD** | 13 | 1 | 7 | **5** | 0 | **8%** (1/13) |

**The franchise tier's real problem is not that it is wrong — it is that it is unverifiable.**
Twelve of fifteen franchise matches route clips with no description at all. It is asserting
"this is a fight clip" about footage nobody has looked at, on the strength of the film's name.
Of the three that could be checked: one RIGHT (the Joker flipping a semi-truck, Batman on the
Batpod), two WEAK — Commodus interrogating Maximus is a *monologue*, and the Joker taunting
Batman is an *argument*. Which is what these pages actually post: the famous *lines*, not the
famous fights.

**The title tier is worse and its shape explains why.** Nine of its thirteen matches are the
same film — The Dark Knight — and most are the same superimposed-Joker edit re-uploaded by
different accounts. What the tier has actually learned is that meme pages love one movie.
The five WRONGs include Dark Knight footage under a "take showers and fill out job
applications" caption, a man *rapping* into a microphone with a Dragon Ball caption, and the
IMAX-vs-theatre comparison MEMEBOT-022 already caught.

### Proposed order and confidence

The current order is already right; the **confidence attached to it is not.**

| tier | now | proposed | why |
|---|---|---|---|
| VISION_RULE | high, no review | **keep: high, no review** | 60% right, one wrong in 16 |
| FRANCHISE_MOOD | **high, no review** | **high, but `needs_review: true`** | 80% of its matches are unverifiable; 1 of 3 checkable was right |
| TITLE_MOOD | medium, review | **remove the tier** | 8% right, 38% wrong, 69% one film |

Two recommendations, stated as recommendations because this round is read-only on the matcher:

**Demote FRANCHISE to needs-review.** Not to low confidence — the tier is not *wrong* about
the film, and on a clip with no other signal it is the only thing there is. But "high
confidence, no review" currently means a Gladiator monologue renders under a fight song
without anyone seeing it. Flagging costs nothing and is honest about what the tier knows.

**Delete TITLE_MOOD.** It was added in MEMEBOT-022 to recover the one honest title match
(Interstellar) after titles were pulled out of the subject rules. Audited in full it returns
1 RIGHT in 13, and even the Interstellar clip is two people *walking through a landscape* —
graded WEAK. It costs 13 matches of 143 and removes 5 outright wrong ones. The brief asked
whether the extra reach was worth its error rate: **it is not.**

That is the same judgement the genre tier got, on the same grounds, from the same kind of
measurement.

---

## 2. IS TONE READABLE FROM THE SCENE DESCRIPTION?

**Partly. One of the two known-wrong cases is catchable; the other is not.**

30 vision-labelled clips were read and labelled COMIC / SERIOUS / NEUTRAL **before** any
detector was written. Two candidate signals were then scored against those labels, and they
behave so differently that pooling them would have produced a meaningless number:

| channel | recall on COMIC | false alarms on SERIOUS |
|---|---|---|
| **A — the description says it is funny** ("humorous", "comedic", "parody"…) | 4/19 = **21%** | 1/7 = 14% |
| **A′ — same, minus the laugh words** | 4/19 = **21%** | **0/7 = 0%** |
| **B — meme framing** ("text overlay", "pov:", "when you", "meme") | 11/19 = 58% | 4/7 = **57%** |

**Channel B is not a tone signal.** Meme framing appears just as readily on serious clips: it
fired on two men squaring up in a desert ("text overlay"), on a wistful "pov: saying goodbye
to bro", on a motivational Superman quote ("when you"), and on a distressed woman's monologue
("on-screen text"). A signal that fires on 57% of serious clips cannot demote anything.

**Channel A′ is usable, and only as a demote-only flag.** It is precise and insensitive: zero
false alarms on this sample, but it catches only a fifth of comic clips. The one word worth
removing is `laughing` — it describes a *character*, not the clip, and it fired on the Joker
"laughing maniacally" in the most serious scene in the sample. That single edit took false
alarms from 14% to 0%.

### On the two clips that started this

| clip | channel A′ | "the relationship survived" check |
|---|---|---|
| **Enchanted** — separation in a scene whose arc is a marriage saved | **FIRES** — "leading to humorous and touching moments" | **FIRES** — "saved their marriage" |
| **Futurama** — Bender breaks up with his fiancée, played for laughs | silent | silent |

The Enchanted miss is catchable **twice over**, and the second way is better than the first.
The scene text does not only carry tone — it carries the **outcome**: *"without realizing it,
she saved their marriage."* That is not a tone signal, it is a statement that the relationship
did not end, which is the actual reason the clip is wrong for a breakup song. A short
`outcome_contradicts_any` list ("saved their marriage", "they reconcile", "get back together",
"decide to stay together") is narrower, more precise, and more directly aimed than any tone
lexicon.

Bender is not catchable this way. Nothing in that description says it is funny; it is funny
because it is Futurama, and that is a fact about the *franchise* — the signal MEMEBOT-019
deleted on measurement, and this round did not reintroduce.

**So the honest answer:** tone is partially readable. A demote-only flag from channel A′ plus
an outcome-contradiction check would catch one of the two known-wrong cases with no measured
false alarms, and would flag roughly **48% of vision-labelled clips** for review if applied
across the board — which is the right order of magnitude, because that is roughly how much of
this library is comedy and memes. Neither should ever *cut* a clip: 21% recall means silence
is not evidence of seriousness.

---

## 3. COVERAGE — THE NEXT GAIN IS MORE SONGS, NOT BETTER RULES

Today, on a 2,003-clip snapshot with **1,011 clips (50.3%) now vision-labelled**:

**143 routed (7.1%), 1,860 parked (92.9%).** The vision rules reach 115 of the 1,011 labelled
clips = **11.4%**, which projects to **~228 clips of 2,003** when labelling completes.

That projection has moved twice, and both moves were down:

| round | labelled sample | projection |
|---|---|---|
| MEMEBOT-019 | 412 | ~369 |
| MEMEBOT-022 | 419 | ~316 |
| **MEMEBOT-028** | **1,011** | **~228** |

Each revision came from a bigger and more representative sample, and the earlier ones were
inflated — MEMEBOT-022's by title matches this round's audit graded WRONG, MEMEBOT-019's by
those plus the genre tier. The number to plan against is the current one, and it will keep
moving until labelling finishes.

**The question the brief asked — more songs or better rules — has an arithmetic answer.**
Topic mix of the 1,011 labelled clips:

| topic | share | is there a song for it? |
|---|---|---|
| meme / relatable | **19.1%** | no |
| comedy / sitcom | **15.5%** | no |
| unclassified | 11.8% | — |
| anime / comic power | **11.1%** | no |
| action / fight | 10.7% | **yes — song 4** |
| romance / relationships | **10.2%** | no (song 1 wants breakups only) |
| party / summer | 4.4% | **yes — song 3** |
| crime / thriller | **4.3%** | no |
| football & sport | 2.5% | **yes — song 3** |

**The four songs' ceiling, with perfect rules, is 17.6% of the labelled half.** The rules
currently deliver 11.4%. So *every possible improvement to the matcher is worth at most 6.2
percentage points* — about 125 clips library-wide. Meanwhile **82.4%** of the labelled library
belongs to topics no song targets, and the top two of those — memes at 19.1% and comedy at
15.5% — are one purchase away from being served by a single goofy bed.

**One comedy song is worth more than every rule fix available.** That is not a criticism of the
rules; it is what a precise matcher pointed at an under-covered library looks like.

## 4. NOTED, NOT FIXED

`docs/claims/MEMEBOT-022.claims` verifies 9/10 — `scratch/memebot022_audit.py` was written
after BL-865's commit sweep. One `git add` closes it. Left alone, as instructed.

## What this does not do

* **It changes nothing.** Read-only on the matcher by instruction. The two tier
  recommendations — flag FRANCHISE, delete TITLE_MOOD — are proposals with the measurement
  attached, not edits. MEMEBOT-027 *was* editing `song_library.py` and `songs.json`
  concurrently (dialogue-class routing around `pick()`, and hook records on the four songs).
  Verified before publishing that `match()`, `vision_text()`, `title_text()`, `_vision_match()`
  and every `vision_rules` entry are byte-identical to HEAD, so nothing in that work moves the
  numbers here — these measurements call `match()` and nothing else.
* **The samples are small where the population is small.** Franchise and title were audited in
  full (15 and 13), so those numbers are exact for today's matches, not estimates. The vision
  tier's 60% rests on 16 of 115 and carries the sampling error you would expect; it is
  consistent with MEMEBOT-022's independent 14-clip read, which is corroboration rather than
  proof.
* **One verdict is a judgement call.** The Kung Fu Panda clip matched on "kung fu" appearing
  inside the film's name *within the scene text* — the title strip only removes the exact
  `vision_title` string, and here the name arrived by another route. It also genuinely
  describes a battle, so it is graded WEAK rather than WRONG. A stricter reading would make
  the vision tier 9/16 rather than 9/15 checkable.
* **The tone labels are mine.** 30 clips, one reader, no second opinion. COMIC vs SERIOUS is a
  judgement, and a few of them (a wistful "saying goodbye to bro" meme; a baby Grinch) could
  reasonably go the other way. The channel-B result is robust to that — it fails on clips
  nobody would call funny — but the 21% recall figure would move a few points under a second
  reader.
* **The library moved during the round.** Vision labelling went from 44.5% to 50.3% while
  these measurements ran, and the routed count from 124 to 143. Every figure here is one
  snapshot; `scratch/memebot028_audit.py` and `scratch/memebot028_tone.py` reproduce them
  against whatever the library holds when re-run.

## Files

    scratch/memebot028_audit.py     44 hand verdicts, precision per tier, the title-route test
    scratch/memebot028_tone.py      30 hand tone labels, two channels scored separately
    scratch/memebot028_results.json the numbers above
    docs/claims/MEMEBOT-028.claims
