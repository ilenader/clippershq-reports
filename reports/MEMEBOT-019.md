# MEMEBOT-019 — the mood map, and what the library actually contains

*2026-08-01. Song library and mood map only. No paid calls. `clip_library/` read-only — BL-849,
BL-851 and BL-854 were all appending to it while this ran.*

Four songs are in `memebot/scratch/`. This round read the library first, built the map against
what is really in there, and reports the coverage honestly. The short version: **song 4 works,
song 3 half-works, song 1 is rare, and song 2 has nothing to play over.** The library is mostly
comedy, and no song targets comedy.

---

## 1. WHAT IS ACTUALLY IN THE LIBRARY

Snapshot: **2,003 unique clips** from 2,580 raw rows across 52 files, deduped by `clip_id`
keeping the richest row (BL-710 — a thin duplicate loses permalink and caption).

| Signal | Fill | Comment |
|---|---|---|
| `vision_scene` / `vision_beats` | **20.6%** (412) | BL-849/BL-854 are filling this **right now** — it went 302 → 412 during this round |
| caption | 98.7% | but **42.6% are film-recommendation templates** (IMDb / cast / where to watch / a bracketed release year) |
| `franchise` | 34.9% | |
| `content_genre` | 17.7% | BL-847: 70.8% of it from two accounts |
| `valence_text` | 98.1% | and useless here — see below |

**What the clips are ABOUT**, one primary topic each, vision first then caption then genre:

| Topic | Clips | % |
|---|---|---|
| unclassified (no vision label, no usable caption yet) | 482 | 24.1% |
| **comedy / sitcom** | **400** | **20.0%** |
| action / fight | 241 | 12.0% |
| anime / comic power-scaling | 195 | 9.7% |
| romance / relationships | 158 | 7.9% |
| crime / thriller | 136 | 6.8% |
| titled clip, not described yet | 84 | 4.2% |
| meme / relatable | 84 | 4.2% |
| football & sport | 52 | 2.6% |
| party / summer | 47 | 2.3% |
| kids & animation / animals / horror / music | 98 | 4.9% |
| grief & loss, conspiracy & politics, wrestling | 25 | 1.2% |
| **women winning** | **1** | **0.0%** |

### A correction to my own first pass

The first distribution I measured said **football was 22.7% of the library**. It was an
artefact of matching without word boundaries: `mma` hit 306 clips inside "e**mma** Stone",
"co**mma**" and "dile**mma**"; `nfl` hit inside "i**nfl**uential"; `nba` inside "fa**nba**se";
`war` inside "warm", "toward" and "award". The real figure is **2.6%**. Every phrase in the
shipped map is now anchored automatically, and that anchoring is a tested property, not a
convention.

---

## 2. THE MAP

`scratch/songs.json` now carries a `vision_rules[]` block that runs **before** franchise,
genre and valence. Rules are **plain phrases, never regexes** — the operator edits this file
by hand, and `song_library` compiles each phrase with word boundaries itself.

Each rule is narrow on purpose. Not "sad" — *a relationship ending*.

| Song | Mood | Routes on | Guarded against |
|---|---|---|---|
| **1** breakup | `melancholy` | "broke up", "getting a divorce", "cheated on him/her", "ex-girlfriend" — **and** a relationship word must be present | grief (a dead dog is sad, not a breakup); real-estate and obituary stories that mention an ex-wife |
| **2** empowerment | `triumphant` | "independent woman", "she's a boss", "trust no man", "female CEO" — **and** a female subject must be present | royalty: bare "queen" matched Queen Elizabeth conspiracy clips and *King of Queens* |
| **3** summer / football | `warm` | World Cup, Messi, Ronaldo, FIFA, Champions League, "soccer match" | "quidditch world cup"; "Palm Beach" in an obituary; "#friendshipgoals" |
| **4** fight | `hype` | "fight scene", "car chase", "john wick", "interstellar", plus franchise routes (Troy, Gladiator, Dark Knight, Mad Max…) | "fighting cancer", "battling depression", "food fight" |

Three design decisions worth stating outright:

**STRONG once, or WEAK twice.** A single weak word never fires. "A Roman army is destroyed"
(a history podcast) was a fight scene until this rule existed.

**`valence_mood_map` stays EMPTY, deliberately.** Valence is the best-filled signal in the
library at 98.1% and it cannot do this job: `negative` cannot tell a breakup from a funeral,
and that is precisely the distinction song 1 needs. Ninety-eight percent coverage of the wrong
question is worth nothing.

**`fallback_moods` stays EMPTY.** With no house set, a clip that matches nothing **parks**.

**Tone conflict is flagged, not hidden.** Futurama's Bender breaking up with his fiancée is
genuinely a relationship ending *and* a joke. The match still happens, but the evidence string
carries `+TONE_CONFLICT:comedy` and `needs_review` goes true. Right subject, wrong feeling is
the same failure as the dead dog, one level up.

---

## 3. COVERAGE — WHAT EACH SONG ACTUALLY REACHES

Measured by running `clippershq.song_library.match()` against the real library, not by a
second copy of the rules.

| Song | Mood | Clips | % of library | By tier |
|---|---|---|---|---|
| **4** fight | hype | **156** | **7.8%** | genre 75, vision 65, franchise 16 |
| **1** breakup | melancholy | **3** | 0.1% | vision 3 |
| **3** summer | warm | **3** | 0.1% | vision 3 |
| **2** empowerment | triumphant | **0** | 0.0% | — |
| | | **162** | **8.1%** | |
| **PARKED** | | **1,841** | **91.9%** | |

**The honest forecast.** Today's 8.1% is mostly a measure of how far vision labelling has got.
On the 412 clips that *are* labelled, the vision rules reach **18.4%**. If the rest of the
library looks like that sample, the four songs land at roughly **18%, about 369 clips**, once
BL-849/BL-853/BL-854 finish — and song 4 is 17.0 of those 18.4 points.

**Precision, hand-audited.** I read every song 1/2/3 match individually:

- **Song 3 — 7 of 9 right.** Genuinely football: the Messi shirt clip, Foden in a Champions
  League warm-up, China vs Japan, the 2026 World Cup draw, a World Cup finals retrospective.
  Two wrong: *Hotel Transylvania 3: **Summer Vacation*** matched on its own title, and a
  designated-driver party clip is "going out" but thin.
- **Song 1 — 3 of 5 right.** Right: a That '70s Show breakup scene, Bender's breakup
  (flagged tone-conflict), *Enchanted*'s "are you getting a divorce, is it forever". Wrong: a
  Modern Family clip where an ex-girlfriend is mentioned in passing, and a rom-com plot
  synopsis. Both wrong ones came through captions.
- **Song 2 — 0 of 2 right.** Elizabeth Taylor founding an AIDS foundation is a woman doing
  something admirable but it is not "go get that money"; the Workaholics clip has a character
  *mocked* for saying "I'm an independent woman". After tightening, both are gone and the
  count is zero.

The caption fixes cut the routed total from 203 to 162. That is the right direction: those 41
were mostly film synopses describing a *movie's* plot, not this clip.

**Song 4's quality mix is worth your eye.** 75 of its 156 come from the **genre** tier, which
only knows the *film* is an action film — it says nothing about what this clip shows. Those
carry `confidence: low` and `needs_review: true`. The 65 vision hits and 16 franchise hits are
the trustworthy ones. If you want song 4 to only fire on real evidence, delete the four entries
in `genre_mood_map` and it drops to 81 clips of much higher quality.

---

## 4. THE PARKED BUCKET — your shopping list

Nothing is discarded. Every unmatched clip keeps its topic and a reason, and every topic says
what kind of song would take it.

| Parked topic | Clips | % | What it is waiting for |
|---|---|---|---|
| unclassified | 480 | 24.0% | nothing yet — no vision label. Not a gap, just unlabelled |
| **comedy / sitcom** | **384** | **19.2%** | **a goofy / playful bed. THE BIGGEST GAP BY FAR** |
| anime / comic power | 178 | 8.9% | epic heroic build; song 4 may take some once vision lands |
| romance / relationships | 151 | 7.5% | a warm romance bed — happy couples are not the breakup song |
| action / fight | 135 | 6.7% | song 4 already targets these; parked on thin evidence only |
| crime / thriller | 123 | 6.1% | a tense bed |
| meme / relatable | 75 | 3.7% | goofy or deadpan — probably the same bed as comedy |
| party / summer, football | 85 | 4.2% | song 3 targets these; waiting on vision |
| horror | 23 | 1.1% | an eerie bed |
| animals / kids | 48 | 2.4% | warm, cute, playful |
| music performance | 21 | 1.0% | **no bed at all** — these clips already have their own music |

**If you buy one more song, buy a comedy bed.** Comedy plus meme is 459 parked clips, 22.9% of
the library — nearly three times what all four current songs reach today. A crime/tense bed is
second at 123, and a warm romance bed third at 151.

Why nothing matched, by count: 864 had no vision label and a caption that matched nothing; 584
had no vision label and a film-recommendation caption; 371 were vision-labelled but simply not
about any of the four subjects; 22 had no usable text at all.

---

## 5. TWO FORCED-MATCH BUGS, BOTH CLOSED

Rule 5 said never force a match. Wiring the map exposed two places where the library did
exactly that:

1. **`pick(store, None)` handed back an arbitrary song.** `_candidates` skipped the mood
   filter when the mood was falsy, so a clip that matched *nothing* — mood `None` — became a
   candidate for **every enabled song**. This was invisible while `fallback_moods` was always
   configured, because `match()` could not return `None` before this round. It can now.
2. **`pick()` fell back to any song when no track carried the requested mood.** That was a
   deliberate MEMEBOT-008 decision — *"a library with no 'eerie' track must still produce a
   video"* — and this round **reverses it** on the brief's explicit instruction. With four
   songs on four narrow subjects the fallback did not deliver a different mood; it delivered a
   breakup ballad over a football clip. The test that asserted the old behaviour now asserts
   the new one and says why.

`render_plan()` also now returns `parked: True` with a `park_reason` instead of a bare error,
so a parked clip is a countable state rather than a failure.

**53 checks in `tests/test_song_library.py` pass**, including the word-boundary regressions
("warm"/"toward"/"award"/"eMMA"), the dead-dog rule, the tone-conflict flag, and the
regex-in-a-phrase-list validator. `tests/test_clip_pipeline.py` (82 tests) still passes.

---

## 6. THE SONG RECORDS

All four are filled in with mood, the file, the measured duration, and a `targets` line in your
words. **All four are `enabled: false`.**

That is deliberate and it is the one thing to undo. Every hook window in the file is a
PLACEHOLDER — they were not chosen by listening. A song that is enabled with a placeholder
window will be picked and rendered against a window nobody chose, which is the same class of
error as a wrong song. Mark the windows with `python hookmark/server.py`, then flip the flag —
one word each.

Song 4's record states it has **two or three drops and needs multiple hook windows**, and
carries three placeholder slots so they exist; delete the third if there are only two.

**One assumption you should check.** `song01..song04` are mapped to SONG 1..SONG 4 by filename
order. The files carry no useful titles — only `song02` has a tag at all, reading "Untitled
Project" — so there is no evidence in the audio confirming the order. I measured each track's
energy structure hoping to corroborate it and it does not: a crude loud-section count puts 5
sections in song03 and 0 in song04, which tells you the counter is not a drop detector rather
than anything about the songs (the BL-690 lesson, again). If the order is wrong, swap the four
`path` values and nothing else changes.

## What this does not do

* **No hook windows were marked.** Correct per the brief and per MEMEBOT-008.
* **The caption tier is measured but NOT wired.** Captions are 98.7% filled against vision's
  20.6%, so it is tempting; the brief's chain is vision → franchise → genre → valence and I
  kept to it. Adding it strong-phrases-only would take routing from 162 to 203 clips, and the
  hand audit says most of that gain is film synopses. The measurement is in the report script
  under section 2a if you want it later.
* **The rules are keyword rules.** They read a description; they do not understand it. Every
  non-vision match carries `needs_review: true` for that reason.
* **The library moved while I measured.** BL-851 is growing it and BL-849/BL-854 are labelling
  it; vision fill went 15.1% → 20.6% during this round. Every number here is one snapshot,
  stated as such, and re-running `scratch/memebot019_distribution.py` reproduces it against
  whatever the library holds then.
* **Nothing is committed.** `docs/claims/MEMEBOT-019.claims` verifies once it is;
  `verify_claims.py` checks `git show HEAD:` and will report 0/17 until then.

## Files

    clippershq/song_library.py         VISION_RULE + PARK tiers, phrase compiler, two bug fixes
    scratch/songs.json                 4 songs, 4 vision rules, franchise + genre maps
    tests/test_song_library.py         53 checks
    scratch/memebot019_distribution.py the measurement, re-runnable
    scratch/memebot019_distribution.json
    docs/claims/MEMEBOT-019.claims
