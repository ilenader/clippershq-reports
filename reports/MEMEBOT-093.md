# MEMEBOT-093: `strong:explosion` is 55.9% RIGHT, not 38.2% — the hype rule's problem is COMEDY, not setting

**Date:** 2026-08-02 · **Type:** Precision audit + one code fix + operator proposals · **Spend:** **$0.00 · 0 paid calls**
Claim filed with **repeated `--write` flags** (11 paths). `claims_read.py --holders` and `git status --porcelain` run on every target: `song_library.py` and `songs.json` both **FREE and clean**. **`scratch/songs.json` is untouched** — every rule change is a proposal in `scratch/mb093_songs_proposed.json`. `config.json` unmodified (`sha256 5fb1a8a2…`, 161 keys, 5 campaigns unchanged).

**The brief's central premise does not reproduce, and the real defect is a different one.**

---

## 1. `strong:explosion`: the premise, measured

MEMEBOT-088 reported *"34 fires, 38.2% scene-confirmed"* and diagnosed a setting-versus-action confusion — *"a poster OF an explosion"* matches. Re-measured on 2,661 clips through `dict_of`:

| | |
|---|---|
| firings | **34** — matches MEMEBOT-088 exactly |
| the word is in the **description** (`vision_scene` or a beat) | **33 of 34 — 97.1%** |
| the word is in **burned-in text only** | **1 of 34** |

**I could not reproduce 38.2%, and MEMEBOT-088's report does not define "scene-confirmed".** I tried three candidate definitions — phrase-in-description (33), an action verb in the scene (1), "explosion" as the subject of a verb (1). None yields 13. The number is not wrong so much as **unmethodded**, and it is doing load-bearing work in a shopping list, so it needed settling on evidence rather than on whose substring rule wins.

### So I hand-audited all 34

Read each clip's `vision_scene` + beats. **RIGHT** = an action clip a hype track fits. **WEAK** = defensible but the register is off. **WRONG** = not an action clip at all.

```
RIGHT  19  (55.9%)
WEAK    7  (20.6%)
WRONG   8  (23.5%)
```

**55.9% RIGHT is exactly the matcher's own 56.1% baseline (MEMEBOT-077).** `strong:explosion` is not the loosest phrase in the hype rule; it is a perfectly average one.

### And the cause is not setting-versus-action

Grouping every non-RIGHT verdict by what actually went wrong:

| cause | n |
|---|---|
| **COMEDY register** — Simpsons, Regular Show, Anchorman 2, Jackie Chan slapstick, Down Periscope | **9** |
| reaction / commentary video — a streamer reacting, a ranking overlay | 3 |
| horror / tragedy register — Final Destination, Deepwater Horizon | 2 |
| dialogue, no action | 1 |
| **"a poster OF an explosion"** | **0** |

The scene text says *"explosion"* and there really is one. **The clip is a comedy.** That is consistent with BL-894's standing finding that the system cannot see comedy — and it means dropping the phrase, as MEMEBOT-088 proposed, would cost **19 right matches to remove 8 wrong ones**.

---

## 2. Every `strong:` phrase, not just one

38.2% was found by checking one phrase. All 32 that fire, across all four rules:

```
phrase                 mood        fires  scene ost-only   confirm%
explosion              hype           34     33        1     97.1%
action sequence        hype           10     10        0    100.0%
martial arts           hype            9      8        1     88.9%
fight scene            hype            9      9        0    100.0%
fight sequence         hype            7      7        0    100.0%
shootout               hype            6      6        0    100.0%
fifa                   warm            5      5        0    100.0%
football game          warm            4      4        0    100.0%
interstellar           hype            2      1        1     50.0%
epic battle            hype            1      0        1      0.0%
showdown               hype            1      0        1      0.0%
... 21 more, all 100%
ALL STRONG PHRASES                   114    109        5     95.6%
```

**No phrase is under 50% on any sample worth acting on.** The two 0% rows fire **once each**; proposing a drop on n=1 would be the "DAYLIGHT 78:1 was an artifact" mistake. The only structural signal is the last column: **5 firings out of 114 come from burned-in text alone**, and that is a fixable class rather than a judgement call.

### The five, read individually

| phrase | what matched | verdict |
|---|---|---|
| `explosion` | `"no. 5 great-explosion murder god dynamight"` — a hero's **name** in a ranking overlay, over a reaction video | **WRONG** |
| `interstellar` | film names in a Nolan **meme collage** | **WRONG** |
| `epic battle` | `"the most epic battle moments from Regular Show"` — a **title card** over comical cartoon fights | **WRONG** |
| `martial arts` | a Kill Bill meme caption — but the description independently says *"fight scene"* | right anyway |
| `showdown` | `"a desperate showdown as a machine gun meets a knife"` — a caption that genuinely describes the action | **RIGHT** |

---

## 3. The fix: a STRONG phrase must be in the DESCRIPTION

`vision_text()` concatenates three fields and the matcher searched the join. Two of them describe the clip; `vision_on_screen_text` is characters burned into the frame — a meme caption, a title card, a ranking list. It describes the clip only by accident, and when a `strong` phrase lands inside a **proper noun** there it is not a claim about the clip at all.

**This is the same defect `vision_text` already fixes one field over.** MEMEBOT-019 removed `vision_title` from the match text for exactly this reason (*"Kung Fu Panda"* → the fight song). The burned-in-text half was never done.

```python
strong_text = description_text(clip)     # vision_scene + beats[].what, title stripped
...
m = rx["strong"].search(strong_text)
```

**Strong only, deliberately.** `weak` still reads the full blob — a weak term needs a second weak term to fire, so a caption is trusted to *corroborate*, never to decide. **Every guard** (`excludes_any`, `requires_any`, `outcome_contradicts_any`, `tone_conflict_any`) still reads the full blob: a guard that reads less than the matcher is a block that silently stops firing, which would have been a worse bug than the one being fixed.

### Per-clip effect — and it is smaller than I predicted

A set difference cannot see a MOVE (MEMEBOT-088 found two clips that changed tier with the song unchanged), so every clip is keyed by `clip_id` and compared field by field against **HEAD's** `song_library.py`, loaded from `git show` into its own module:

```
               before      after
  matched         460        459
  parked         2201       2202

  LOST    (had a song, now parks) : 1
  CHANGED (different song)        : 0
  MOVED   (same song, new tier)   : 0
  GAINED  (parked, now matched)   : 0
```

**The one clip lost is the Nolan meme collage — a WRONG match.** Zero right matches lost.

**I predicted three wrong removed and one right lost. Both halves were wrong.** The My Hero Academia and Regular Show clips still match hype through another phrase in their descriptions, and No Country for Old Men — which I expected to lose — was never at risk. So the honest result is: **the burned-in path was carrying almost no unique signal and exactly one unique wrong answer.** A smaller win than advertised, measured rather than assumed.

`tests/test_song_library_hype_precision.py`, 8 checks, including `test_a_planted_reversion_is_caught` — it restores the old behaviour and asserts the suite would have gone red, because a test that only asserts today's behaviour passes just as happily after a revert.

---

## 4. Twenty TRACK_TITLE matches, read for irony

| | |
|---|---|
| RIGHT | 4 (20%) |
| WEAK | 7 (35%) |
| **WRONG** | **9 (45%)** |

**Stated limit before the number is used: these are the first 20 in library order, not a random sample,** and they are heavy on Young Sheldon / Futurama / Simpsons and one repeated ratings graphic. This is **not** a tier-wide precision estimate and it does **not** refute MEMEBOT-088's 68.8% — it is a flag that a random re-audit is worth doing.

**The brief's example is live today.** `"Milk and Cookies"` → `warm`, on a clip whose scene reads *"a pastor questions Todd Flanders in church about his beliefs **after his mother's death**"*. A wholesome song over a child's grief — the exact counter-textual shape, currently shipping.

Two other patterns: `"In Another Lifetime"` → `melancholy` over a Homer **kidnapping comedy** and a Bender vending-machine gag; and `"Me and the Devil (slowed)"` → `hype` on four clips that are **static IMDb ratings graphics** for the series *FROM* — no depicted action at all.

### The two mechanical findings, measured tier-wide

Judgement-free, so they generalise where the 20 do not:

```
TRACK_TITLE matches                                  160
  no scene text AT ALL -- routed on the title alone   35   (21.9%)
  scene is a static ratings/info graphic               4    (2.5%)
  union: a song chosen with no depiction to check     39   (24.4%)
```

**Roughly a quarter of the title tier picks a song with nothing to check it against.** Irony cannot be detected even in principle on those 35 clips — there is no scene to contradict the title.

---

## 5. The vocabulary slots

| mood | in `mood_vocabulary` | `validate()` with a song added |
|---|---|---|
| `goofy` (meme) | yes | clean except *"no hand-marked hooks"* |
| `tender` (wholesome) | yes | same |
| `sombre` (grief) | yes | same |
| `lavish` (money) | yes | same |

Live store `validate()`: **CLEAN**. The meme rule's zero-regression assertion still holds — `tests/test_song_library_meme_rule.py` passes on the current library, including `test_valence_map_stays_empty` and `test_vocabulary_has_a_token_for_every_proposed_song`.

**A correction to "one-move".** Every slot is prepared, but activation is **two moves, not one**: adding the song leaves `validate()` reporting *"no hand-marked hooks — it can never be picked"*. That is the guard working exactly as intended (BL-690 measured automatic drop detection at 100% fabrication, so windows must be marked by ear), but it means a purchase is not live until somebody marks hooks in `hookmark/`. Worth knowing before the money is spent.

---

## 6. The ceiling, re-derived

The last ranking (meme +129 > wholesome +40 > grief +35) predates the track-title tier, which moved 155 clips out of park — a delta measured against a library that no longer exists. Recomputed today:

```
clips            2,661
matched            459   (17.2%)
parked           2,202   (82.8%)

by tier                     by mood (which song a matched clip gets)
  VISION_RULE        286      hype         274   (59.7% of matched)
  TRACK_TITLE_MOOD   160      warm          94   (20.5%)
  FRANCHISE_MOOD      13      melancholy    78   (17.0%)
                              triumphant    13   (2.8%)
```

**Hype share 59.7%**, confirming MEMEBOT-088's 59.3% held as the library grew from 2,003 to 2,661.

### The shopping list cannot be re-derived, and that is the finding

`_pending_vision_rules` contains **exactly one rule: `goofy`, worth +112 parked clips (4.2%)**. The wholesome / grief / pressure / money rules the brief asks me to re-rank **do not exist in the store**. The old ranking's +40 / +35 came from somewhere other than a runnable rule, so there is nothing to re-derive and I will not carry a number I cannot reproduce.

**The list, honestly stated:**

1. **`goofy` (meme) — +112 clips, measured by running the rule over the 2,202 parked clips.** The only purchase whose payoff is a measurement rather than an estimate.
2. `tender`, `sombre`, `lavish` — **slots prepared, rules not written.** Costing them requires writing the rule first; a fill rate is not a firing rate (BL-972).

`_non_purchases` already records the trap: the 163-clip superhero cluster is only 18 action-bearing clips; the rest is fandom *talk*.

---

## 7. Proposals to the operator — `songs.json` untouched

In `scratch/mb093_songs_proposed.json`:

1. **Do NOT drop `strong:explosion`.** 55.9% RIGHT, at the matcher's own baseline. Dropping it costs 19 right matches to remove 8 wrong.
2. **Format markers for the hype rule's `excludes_any`** (`"reacting to"`, `"selfie-style"`, `"displays a graphic"`, `"episode ratings"`, `"meme collage"`, …). **Measured and NOT yet recommended:** it stops 26 clips matching; of the 34 I audited it removes 5 WRONG/WEAK and costs 2 RIGHT. The other 19 are unaudited, so the trade is unknown. **Audit those 26 before applying** — I am not proposing a change whose net effect I have not measured.
3. **`TRACK_TITLE` with no scene text.** 35 clips. Preferred option: set `needs_review` rather than refuse, so **no clip loses a song** while the operator can see which songs were chosen with nothing to check.

---

## 8. What I got wrong

* **I predicted the burned-in fix would remove three wrong matches and cost one right one.** It removed one and cost none. I wrote the prediction down before measuring, which is the only reason the gap is visible.
* **My first framing accepted "38.2% scene-confirmed" as a fact to be fixed.** It is undefined in its source report and I could not reproduce it under three readings. The right response was to hand-audit, not to fix a number.

---

## 9. Suite

```
tests/run_all.py                            150 of 152 green    834.0s
tests/test_song_library_hype_precision.py   PASS   8 checks
```

**Neither red is this round's** — both pass standalone:

| suite | standalone | why |
|---|---|---|
| `tests/test_suites_parse.py` | `Ran 6 / OK` | it **walks `tests/`**, and other rounds are writing files there mid-walk — its own flake mode |
| `tests/test_wip_commit.py` | `Ran 5 / OK` | concurrency flake |

Directly re-run and green: `test_song_library` (ALL PASS), `test_song_library_meme_rule` (0 failures), `test_matcher_boundary` (9), `test_track_title_tier` (15), `test_join_key` (11).

---

## SUMMARY

- **Shipped:** `song_library.description_text()` — a `strong` phrase must appear in the clip's **description**, not in burned-in frame text — plus 8 pinning checks including a planted-reversion test. Four operator proposals in `scratch/mb093_songs_proposed.json`; **`songs.json` untouched**.
- **The one number: 55.9%.** `strong:explosion` hand-audited over all 34 firings is 19 RIGHT / 7 WEAK / 8 WRONG — **the matcher's own 56.1% baseline, not 38.2%**, and the cause of every miss is **comedy register (9)**, never "a poster of an explosion" (0).
- **Off-brief:** the shopping list **cannot** be re-derived — `_pending_vision_rules` holds exactly one rule (`goofy`, +112 measured); the wholesome/grief/money rules do not exist, so the old +40/+35 are unreproducible. And slot activation is **two moves, not one**: `validate()` still refuses a song with no hand-marked hooks.
- **Got wrong:** I predicted the fix would remove 3 wrong matches and cost 1 right one; it removed **1** and cost **0**. And I initially treated 38.2% as a fact to fix rather than a number to check — it is undefined in MEMEBOT-088 and reproduces under no reading I tried.
- **Still broken, and whose:** the hype rule cannot see comedy — proposal 2 needs its 26 affected clips audited before anyone applies it. **35 of 160 title-tier matches (21.9%) have no scene text at all**, so irony is undetectable there in principle. `"Milk and Cookies"` over a child's grief is shipping today. `clip_pipeline.py` is ` M` and held by INFRA-019 — imported read-only, never edited.
- **Suite / spend:** `run_all.py` **150 of 152 green** — neither red is mine, both pass standalone (`test_suites_parse` walks `tests/` while other rounds write into it). The five matcher suites re-run green, plus 8 new checks. **$0.00, zero paid calls.** `config.json` unmodified, 5 campaigns unchanged, `scratch/songs.json` byte-identical.
