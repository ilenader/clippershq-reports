# MEMEBOT-022 — the genre tier is gone, and a title is no longer a description

*2026-08-01. Mood map and matcher only. No paid calls. `clip_library/` read-only — BL-849,
BL-851, BL-854, BL-863 and BL-864 were all writing it while this ran.*

Both fixes MEMEBOT-019 specified are in. The fight song drops from 164 matches to **87**, and
the share of its matches where *nobody knows what the clip shows* drops from **52% to 15%**.
The title false positive is gone, and hunting it turned up two more of the same bug.

---

## 1. THE GENRE TIER IS DELETED

`genre_mood_map` is now `{}`. It routed four genre keys — action, superhero, war and
hand-to-hand combat — to the fight song and supplied 75 of its matches — every one of them from a film-recommendation caption.
A genre says the **film** is an action film. It says nothing about whether **this clip** is a
fight or two people talking in a car. Same lesson as `content_genre` being 70.8% from two
accounts (BL-847): a broad label is not evidence about a specific clip.

Measured on today's snapshot, old map vs new:

| | song 4 | tiers | matches with **no vision label at all** | song 1 | song 3 | total |
|---|---|---|---|---|---|---|
| **before** | 164 | genre 75, vision 65, franchise 16, title 8 | **86 = 52%** | 2 | 3 | 169 |
| **after** | **87** | vision 62, franchise 16, title 9 | **13 = 15%** | 2 | 2 | 91 |

MEMEBOT-019 reported 156 and predicted ~81 after the deletion. Today's before-figure is 164
and the after is 87 because the library moved underneath both measurements — BL-849/BL-854
labelled seven more clips between the two rounds. The prediction was right; the denominator
shifted.

The `_readme` in `scratch/songs.json` records what putting a line back would buy and cost, so
the trade is visible to whoever considers it.

## 2. A TITLE IS AN IDENTIFIER, NOT A DESCRIPTION

`vision_title` used to be concatenated into the text the subject rules read. That is why
**"Hotel Transylvania 3: Summer Vacation"** routed to the summer song: the words *summer* and
*vacation* were in the film's NAME. The scene is a dragon at a campfire talking about a
marshmallow.

Chasing it found two more of exactly the same shape:

| Title | Routed to | What the clip actually is |
|---|---|---|
| Hotel Transylvania 3: **Summer Vacation** | song 3 | a dragon at a campfire |
| **Kung Fu** Panda (×2) | song 4 | a children's cartoon; a panda surprised that birds fly |
| Interstellar | song 4 | **legitimately Interstellar** |

So: the subject rules now read **only what the clip shows** — `vision_scene`, every
`vision_beats[].what`, and on-screen text. The title is excluded, and it is also **stripped
out of the scene text** where the description repeats it, which 68 clips do. Only the whole
title string is stripped, never its individual words — a film called "War" must not delete the
word from every clip that legitimately uses it, and there is a test for that.

Interstellar was the one honest title match, and titles are **franchise facts**, so they now
route through the franchise tier instead of being thrown away. That was worth doing on its own
terms: `vision_title` is better filled than the curated column — 290 clips carry a title,
only 131 of those have `franchise` set.

### The audit found a third title problem, this one mine

Routing on `vision_title` immediately produced a bad match of its own: `vision_title: "300"`
on a clip that is an **IMAX-vs-normal-theatre comparison** which merely uses 300 as sample
footage. A title the vision model *recognised in the frame* is weaker evidence than a curated
franchise column — it says a film appears, not that the clip is about it.

So title routing got its own tier, **`TITLE_MOOD`**, at `confidence: medium` with
`needs_review: true`, sitting below `FRANCHISE_MOOD`. It keeps the 9 matches it earns and
declares that they need an eye. The curated column keeps `high` / unflagged.

## 3. ONE MORE TIGHTENING THE AUDIT FORCED

`ex-girlfriend` / `ex-boyfriend` moved from **strong** to **weak** on song 1. A Modern Family
clip was routed to the breakup song because a tutor mentions "phil's ex-girlfriend" in passing
while insulting someone's intelligence. An ex being *mentioned* is not a relationship *ending
on screen*; as a weak phrase it now needs a second signal. Song 1 goes 3 → 2, and the one it
lost was the false positive.

## 4. SONG 2 — LEFT ALONE, AS INSTRUCTED

Still zero. Nothing was loosened to manufacture a match. The library contains one clip in the
"women winning" topic out of 2,003. The song is ready before the supply is, and that is a
sourcing problem, not a matcher problem.

## 5. THE TWO REVERSALS ARE KEPT, WITH THEIR REASONING

Both are still in `song_library.py` with the comments intact and are covered by tests:

* **`pick(store, None)` returns nothing.** `_candidates` used to skip the mood filter on a
  falsy mood, so a clip that matched nothing became a candidate for every enabled song.
* **`pick()` no longer falls back to any song when no track carries the mood.** MEMEBOT-008's
  reasoning — *"a library with no 'eerie' track must still produce a video"* — was sound for a
  broad library. With four narrow songs it puts a breakup ballad over a football clip.

The code says so at both sites, and the `pick()` parking test records
that it asserts the opposite of what it asserted this morning, and why.

---

## 6. RE-MEASURED

**91 clips routed (4.54%), 1,912 parked (95.46%)** of a 2,003-clip snapshot.

| Song | Mood | Matches | needs_review | Tiers |
|---|---|---|---|---|
| **4** fight | hype | **87** (4.34%) | 9 | vision 62, franchise 16, **title 9** |
| **1** breakup | melancholy | 2 (0.10%) | 0 | vision 2 |
| **3** summer | warm | 2 (0.10%) | 0 | vision 2 |
| **2** empowerment | triumphant | **0** | — | — |

**Projection.** 419 clips carry a vision label (20.9% of the library). The vision rules reach
66 of them = **15.8%**, which projects to **~316 clips of 2,003** once labelling finishes —
down from MEMEBOT-019's ~369, because that figure was inflated by the title matches this round
removed. Fewer clips, and the ones that remain are the ones with evidence.

## 7. THE HAND AUDIT

Every match for songs 1 and 3 (all four of them), plus 10 of song 4's 87 sampled evenly across
the ordered match list. Verdicts typed by reading each clip's description; recorded against
`clip_id` in `scratch/memebot022_audit.py` so the same claim can be re-checked, and the script
reports loudly if an audited clip stops matching.

**Song 4 — 10 audited: 4 RIGHT, 5 WEAK, 1 WRONG**

| | Clip | Verdict |
|---|---|---|
| ✅ | Doctor Strange fighting with magic and the cape — "the most spectacular fight in MCU history" | RIGHT |
| ✅ | Shaolin-Soccer-style football with fight choreography: kicks, saves | RIGHT — *also a football clip; first-rule-wins gave it to song 4* |
| ✅ | Iron Man suit sequence turning chaotic | RIGHT |
| ✅ | The Man in the Iron Mask: guards, swords, a fight | RIGHT |
| ⚠️ | Sandman powers explainer contrasting comics with the films | WEAK — impressive, but a power-scaling breakdown |
| ⚠️ | Lego Batman action used as a "me and bro" meme backdrop | WEAK — action on screen, but the clip is a joke |
| ⚠️ | The Dark Knight *(franchise column)* — Joker and Batman **arguing** | WEAK — dialogue, not a fight |
| ⚠️ | Gladiator *(franchise column)* — **no vision label at all** | WEAK — content unknown |
| ⚠️ | Avengers: Endgame *(franchise column)* — no vision label | WEAK — content unknown |
| ❌ | `vision_title: 300` — an IMAX-vs-theatre comparison | WRONG — the reason TITLE_MOOD is flagged |

Every RIGHT came from the **vision** tier. Four of the five WEAKs and the single WRONG came
from **franchise or title** — the tiers that identify a film rather than describe a clip. That
is the same pattern that condemned the genre tier, one step milder, and it is now visible in
the tier breakdown of every plan instead of hidden in a total.

**Song 3 — 2 audited, 2 RIGHT.** China vs Japan soccer match; a party clip where the
designated driver is too into it to leave ("going out" is in the brief).

**Song 1 — 2 audited, 0 RIGHT, 2 WEAK.** Futurama's Bender breaking up with his fiancée is a
relationship ending played for laughs. *Enchanted*'s couple confirm they are separating
"forever", but the arc of the scene is a marriage saved. Both are subject-correct and
tone-wrong. Song 1 needs sad clips, and the library's romance content is mostly comedy.

**Song 2 — 0 of 0.**

## 8. VERIFICATION

| check | result |
|---|---|
| `tests/run_all.py` | **ALL GREEN — 81/81 suites, 3,552 checks** (482.6s) |
| `tests/test_song_library.py` | ALL PASS — 66 checks, 7 new for this round |
| campaigns SHA (`sha256[:16]`) | **8e02f8d6f6307ae8 — MATCH** (config.json untouched) |
| `config.json` parses | OK — 162 top-level keys |
| `crossdedup` / `google_play_finder` import | OK |
| `scratch/songs.json` | parses; validates clean apart from the expected disabled-song warnings |
| `docs/claims/MEMEBOT-022.claims` | 9/10 at HEAD |
| `docs/claims/MEMEBOT-019.claims` | **17/17 at HEAD** |

Two notes on that table, because a clean number that hid something would be worse than no
number:

**The first suite run was red and the second was green.** Run one: 66 suites, 2 red —
`test_filelock` and `test_claims_manifest`. `test_filelock` passes in isolation and is
contention-flaky in a tree with nine rounds writing files. `test_claims_manifest` was failing
on the MEMEBOT-009 and MEMEBOT-021 manifests, which BL-865 was mid-fix on at that moment
(`.gitignore` carve-out so memebot code can verify at HEAD). Neither suite imports
`song_library`. Run two, after BL-865 landed: 81 suites, all green. The suite count rose from
66 to 81 between runs because other rounds were adding tests while this one measured.

**The claims manifest is 9/10, not 10/10.** `scratch/memebot022_audit.py` was written after
BL-865's commit sweep passed through, so it is the one path not yet at HEAD. Everything else
this round claims verifies. Committing is not this round's call.

## What this does not do

* **It does not fix song 1's tone problem.** Both its matches are subject-right and
  tone-wrong. The `tone_conflict_any` list exists and did not fire on either, because neither
  description contains a comedy word — the *franchise* is a comedy, the sentence is not. A
  real fix needs the clip's genre, and genre is exactly the signal this round deleted for
  being untrustworthy. Left as a known gap rather than papered over.
* **It does not resolve the song-3/song-4 overlap.** A football clip with fight choreography legitimately
  fits both; first-rule-wins gave it to song 4 because that rule is listed first. No priority
  scheme was invented for a single observed case.
* **Franchise matches on unlabelled clips stay high-confidence.** Two of the ten audited had
  no vision label at all. The franchise column is curated and being right about the film is
  what that tier claims, so this is arguably correct — but it means "high confidence" there
  means confidence in the *film*, not the clip. Worth knowing before trusting the flag.
* **The library moved during the round.** 2,003 clips, 419 labelled at the time of measuring;
  BL-851 is appending and BL-849/BL-854 are labelling. Re-run
  `scratch/memebot022_audit.py` to reproduce against whatever it holds then.

## Files

    clippershq/song_library.py     title excluded from subject text + stripped from scene;
                                   TITLE_MOOD tier; both pick() reversals kept
    scratch/songs.json             genre_mood_map emptied; ex-girlfriend demoted to weak
    tests/test_song_library.py     66 checks
    scratch/memebot022_audit.py    the re-measure and the recorded hand audit
    docs/claims/MEMEBOT-022.claims
