# MEMEBOT-032 — the tier decisions, applied

*2026-08-01. `song_library.py` and the mood map only. No paid calls. `clip_library/` read-only —
BL-849 and BL-872 are labelling it live and it grew under the measurements again.*

## THE HEADLINE, BECAUSE IT SHOULD DECIDE THE NEXT ROUND

**With perfect rules the four songs reach 19.5% of labelled clips. The rules deliver 13.2%.
Every remaining rule fix put together is worth at most 6.3 points — about 126 clips.**

**80.5% of the labelled library belongs to topics no song targets**: memes 18.1%, comedy
15.3%, romance 10.8%, anime 9.9%, crime 5.2%. One comedy bed is worth more than every rule
improvement still available.

MEMEBOT-028 measured that headroom at 6.2 points on 1,011 labelled clips. It is 6.3 points on
1,451. The number did not move when the sample grew by half, which is about as much
corroboration as a projection of this kind can get. **Nobody should spend another round on
rules.** That is not a criticism of the rules — it is what a precise matcher pointed at an
under-covered library looks like.

---

## 1. THE THREE TIER DECISIONS

| tier | before | after |
|---|---|---|
| **VISION_RULE** | high, no review | **unchanged** — every RIGHT match came from it |
| **FRANCHISE_MOOD** | high, **no review** | high, **`needs_review: true`** |
| **TITLE_MOOD** | medium, review | **deleted** |

**Franchise is flagged, not downgraded.** Its confidence stays `high` deliberately: the tier
is not *wrong* about the film, and on a clip with no other signal it is the only thing there
is. What it cannot support is the "no review" half. Of its 15 matches MEMEBOT-028 audited,
**twelve routed clips carrying no vision label at all** — nobody can say what they show. Of
the three that could be checked, one was right (the Joker flipping a semi-truck) and two were
a Gladiator **monologue** and a Batman/Joker **argument**. Which is what these pages post: the
famous lines, not the famous fights. "High, no review" meant that monologue rendered under a
fight song with nobody seeing it. All 15 are now flagged.

**TITLE_MOOD is deleted.** 1 RIGHT in 13, 5 outright WRONG, and 9 of the 13 the same film —
mostly one re-uploaded Joker edit. It was added in MEMEBOT-022 to rescue a single honest match
(Interstellar) which the full audit then graded WEAK anyway, because that clip is two people
*walking through a landscape*. Same judgement the genre tier got in MEMEBOT-019, on the same
grounds: a label that identifies a **film** is not evidence about a **clip**. The deletion is
recorded in the code where the constant used to be, so the next round to consider re-adding it
argues with the measurement rather than the idea.

### Re-scored on the same 44 hand verdicts

Not a fresh sample — MEMEBOT-028's recorded verdicts, re-run against the changed matcher, so
the effect is the same clips read the same way:

| tier | audited | RIGHT | WEAK | WRONG | BLIND | RIGHT of checkable |
|---|---|---|---|---|---|---|
| VISION_RULE | 16 | 9 | 5 | 1 | 1 | **60%** (9/15) |
| FRANCHISE_MOOD | 15 | 1 | 2 | 0 | 12 | 33% (1/3) — now all flagged |
| ~~TITLE_MOOD~~ | — | — | — | — | — | gone |

**5 WRONG and 7 WEAK matches stopped rendering. The cost was 1 RIGHT.**

---

## 2. `outcome_contradicts_any` — A GUARD, NOT A LEXICON

The Enchanted clip routed to the breakup song on "getting a divorce" while the same
description says *"without realizing it, she **saved their marriage**"*. The relationship did
not end, so the match is **false** — not merely badly-toned. That is a narrower and better
aimed question than tone, and it gets its own guard.

There are now three guards and they are deliberately not the same guard:

| guard | question | effect |
|---|---|---|
| `excludes_any` | wrong **context** — "real estate", "obituary" | blocks |
| `outcome_contradicts_any` | wrong **outcome** — the thing the song is about did not happen | **blocks** |
| `tone_conflict_any` | wrong **feeling** — the subject is right and the clip is a joke | **demotes only** |

Outcome blocks and tone only flags because they answer different questions. "She saved their
marriage" means the match is false. "This is a comedy" means the match is true but the pairing
may land badly — and at 21% recall the tone signal is far too insensitive to hold a veto: it
would throw away four right answers for every one it saved.

**What it catches, measured across the whole library:**

    clips blocked by outcome_contradicts_any: 1
      3937161994631327045_13264963167 — the Enchanted case

**One clip. Zero collateral.** The guard is aimed, not broad — it removes the known-wrong case
and touches nothing else in 2,003 clips. The other known-wrong case, Futurama's Bender, is
**still matched and still unflagged**: nothing in its description says it is funny. It is funny
because it is Futurama, which is a fact about the franchise, and the genre tier was deleted on
measurement. MEMEBOT-028 said that case was not catchable this way and it is not; reporting it
as solved would be the lie.

## 3. THE DEMOTE-ONLY TONE FLAG NOW ACTUALLY DEMOTES

Wiring this turned up a live bug. `needs_review` was read straight off the tier table, so a
vision match carrying `+TONE_CONFLICT` in its evidence still came back **`needs_review: False`**.
The demote-only flag demoted nothing — it was printed in the reason and dropped on the floor.
A flag that does not reach the field a consumer filters on is decoration.

`match_detail()` now carries the per-match flags through, and `render_plan()` uses it.
`match()` keeps its three-tuple, so no existing caller changes.

    vision matches carrying +TONE_CONFLICT: 1
      3950314681070836281_2002894504  needs_review=True
      vision strong:left her for +TONE_CONFLICT:funny -> mood:melancholy

The tone vocabulary is MEMEBOT-028's channel A′ and nothing else — 21% recall, 0% false alarms
on the 30-clip hand-labelled sample. Two things are deliberately absent, and the store says so
at the field:

* **No laugh words.** "laughing" describes a *character*; it fired on the Joker laughing
  maniacally in the most serious scene in the sample. Dropping it took false alarms 14% → 0%.
* **No meme framing.** "pov:", "text overlay", "when you" score 58% recall but **57% false
  alarms** — they fired on two men squaring up in a desert, a wistful goodbye, and a distressed
  woman's monologue. A signal that fires on 57% of serious clips cannot demote anything.

## 4. WHERE THE MAP STANDS

2,003 clips, **1,451 now vision-labelled (72.5%)** — labelling moved a long way during this
round.

| song | mood | matches | needs_review | tiers |
|---|---|---|---|---|
| **4** fight | hype | 184 (9.19%) | 13 | vision 171, franchise 13 |
| **3** summer | warm | 23 (1.15%) | 0 | vision 23 |
| **1** breakup | melancholy | 3 (0.15%) | 1 | vision 3 |
| **2** empowerment | triumphant | **0** | — | — |
| | | **210 routed (10.5%)** | | **1,793 parked (89.5%)** |

Projection at today's rate: **~265 clips of 2,003** once labelling finishes.

## 5. VERIFICATION

| check | result |
|---|---|
| `tests/test_song_library.py` | ALL PASS — **137 checks**, 9 new/changed this round |
| `tests/test_clip_pipeline.py` | PASS (82 tests) — it consumes `render_plan` |
| `tests/run_all.py` | **ALL GREEN — 87/87 suites, 3,724 checks** (549s) |
| campaigns SHA (`sha256[:16]`) | **8e02f8d6f6307ae8 — MATCH** (config.json untouched) |
| `config.json` parses | OK — 162 top-level keys |
| `song_library` / `crossdedup` / `google_play_finder` / `clip_pipeline` import | OK |
| `scratch/songs.json` | validates clean apart from the expected disabled-song warnings |
| stale `TIER_TITLE` references | none outside the deletion note and the test that asserts it is gone |
| `docs/claims/MEMEBOT-032.claims` | 8/10 at HEAD — the two misses are `match_detail` and `memebot032_remeasure.py`, both new this round and therefore working-tree only. One commit closes them, which is not this round's call. |

## 6. PROCESS NOTES

**The claim registered all five paths individually** — verified by reading
`.claims/MEMEBOT-032.json` rather than trusting the console line, which is worth doing while
BL-870 is mid-fix on `claim.py`'s path handling. One advisory fired: BL-868 declares `docs/`
broadly and my only file there is a uniquely-named new manifest, so there is no real overlap.
Proceeded, as the advisory invites.

**MEMEBOT-027 had released both files** before this round started, and no in-flight claim held
either. One mid-round scare: an Edit reported `song_library.py` had changed on disk. It had —
MEMEBOT-027's dialogue-class work landing between reads — and the later mtime was my own edit.
Checked against the claim registry and the mtimes before continuing rather than assuming.

## What this does not do

* **It does not fix the Bender case**, and nothing here pretends otherwise. It needs the
  franchise's genre, which was deleted on measurement.
* **`outcome_contradicts_any` is written for song 1 only.** Songs 2–4 have no outcome that can
  contradict them in the same clean way — "a fight happened" has no negation a scene
  description reliably states. Adding empty lists to look symmetrical would be noise.
* **The outcome guard is 18 phrases against one measured case.** Seventeen of them have never
  fired. They are written the way the one that fired is written, but a phrase list with no
  positives is a hypothesis, not a result.
* **60% precision on the vision tier is unchanged** — this round removed bad matches from other
  tiers, it did not make the vision rules better. The 6.3-point ceiling is why that is the
  right place to stop.
* **The library moved throughout.** Vision labelling went 44.5% → 72.5% during the session and
  routed counts rose with it. Every figure is one snapshot;
  `scratch/memebot032_remeasure.py` reproduces them against whatever the library holds.

## Files

    clippershq/song_library.py        TITLE_MOOD deleted; FRANCHISE flagged;
                                      outcome_contradicts_any; match_detail()
    scratch/songs.json                the outcome guard + the A' tone vocabulary
    tests/test_song_library.py        137 checks
    scratch/memebot032_remeasure.py   the re-score and the ceiling
    docs/claims/MEMEBOT-032.claims
