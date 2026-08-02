# MEMEBOT-104: the comedy-register fix applied — and one marker carries its entire cost

**Date:** 2026-08-02 · **Type:** Apply + audit + re-derive · **Spend: $0.0000**

Claim filed via `tools/claim.py`, **18 paths registered individually** with repeated `--write`.
Registry read with `tools/claims_read.py --holders` and `git status --porcelain` on every
target: all clean, all free. `clippershq/song_library.py` was in the first filing and was
**dropped** when BL-999 claimed it mid-round — the change here is data-only, in
`scratch/songs.json`, so nothing was contested.

`scratch/songs.json` is the operator's file. MEMEBOT-093 proposed and did not apply; this
round applied **exactly proposal 2, unmodified**, with this brief as the consent, and recorded
that fact inside the rule itself.

---

## 1. Applied, and accounted per clip

Ten `excludes_any` markers added to the hype rule. Measured **before** applying, then verified
**after** against the file on disk — same numbers both times:

```
clips                     2,661
matched BEFORE              474  (17.8%)
matched AFTER               448  (16.8%)

KEPT   same mood          2,634
MOVED  different mood         1   <- a set difference is BLIND to this one
PARKED matched -> nothing    26   <- visible loss, the only acceptable kind
GAINED nothing -> matched     0
                        -------
                          2,661   (the four buckets sum to the library)
```

The MOVE is why this is per clip and not a set difference: `3947016901880248224` went
**hype → melancholy** via the track-title tier. A before/after set of "clips matching hype"
contains that clip in exactly one side and looks identical to a clip that simply parked. It
silently changed song.

Per mood: hype **289 → 262**, melancholy 77 → 78, warm and triumphant unchanged.

## 2. THE ONE NUMBER: one marker of ten carries 100% of the cost

All 27 displaced clips hand-audited, definition stated before the result (`RIGHT to displace`
= the register really is reaction / commentary / gameplay / comedy; `WRONG` = straight action
losing a correct song).

**17 RIGHT (63.0%) · 10 WRONG (37.0%)** — and every one of the ten was fired by a single
marker:

| marker | fires | RIGHT | WRONG | precision |
|---|---|---|---|---|
| `reacting to` | 24 | 14 | 10 | **58.3%** |
| `streamer` | 6 | 6 | 0 | 100% |
| `text overlays discussing` | 2 | 2 | 0 | 100% |
| `selfie-style` | 1 | 1 | 0 | 100% |

The other six markers never fired at all.

The cause is structural, not a bad word choice: `excludes_any` reads the **full text blob**
— scene + beats + burned-in text — deliberately, because a guard reading less than the matcher
is how a block silently stops firing. `reacting to` names a FORM, but it also appears in a
*beat* of a straight action montage ("a man is shown reacting to..."), so Doctor Strange
fighting, the O.K. Corral shootout and a Kung Fu Panda combat scene all lost their song.

**PROPOSED, NOT APPLIED** — narrowing `reacting to` was not what was consented to:

* restrict that one marker to `description_text` (scene + beats[].what) — or
* replace it with the narrower forms that carry the register: `reacting to a video`,
  `reacting to a montage`, `split screen`, `gaming chair`.

Either keeps 14 of the 17 right displacements and returns 10 clips to hype. The other nine
markers are sound as proposed.

## 3. Where the displaced clips go if the meme song is bought

The pending `goofy` rule takes **4 of the 27** displaced clips — not 9. It takes 4 of the 17
correctly displaced and **0 of the 10 wrongly displaced**, which is a small point in its
favour: it does not paper over the mistake.

The purchase case does not rest on the displaced clips anyway — see §5.

## 4. Every `strong:` phrase, audited by MEMEBOT-093's method

30 distinct phrases fire; 104 strong-tier matches across 2,661 clips. One clip is credited to
exactly one phrase, so the rates partition rather than overlap. Sample capped at 12, reported
with its denominator.

| phrase | fires | audited | RIGHT | WEAK | WRONG | rate |
|---|---|---|---|---|---|---|
| `fight sequence` | 7 | 7 | 7 | 0 | 0 | **100%** |
| `shootout` | 5 | 5 | 5 | 0 | 0 | **100%** |
| `fight scene` | 10 | 10 | 7 | 2 | 1 | 70.0% |
| `explosion` | 29 | 12 | 6 | 3 | 3 | 50.0% |
| `action sequence` | 8 | 8 | 4 | 3 | 1 | 50.0% |
| `martial arts` | 8 | 8 | 3 | 4 | 1 | **37.5%** |
| `fifa` | 5 | 5 | 0 | 0 | 5 | **0.0%** |
| `football game` | 4 | 4 | 0 | 0 | 4 | **0.0%** |

22 further phrases fire once or twice each and are reported **UNAUDITED** — not 0%.

`explosion` at 50.0% on this 12-clip sample is consistent with MEMEBOT-093's 55.9% on 34, and
this sample is *post*-register-fix: the exclusion already removed five of its worst firings,
so the phrase that remains is the harder half.

**PROPOSED DROPS (never silently applied):**

* **`fifa` — 0 of 5.** Every firing is a **static results graphic**: "a graphic displaying the
  FIFA World Cup, organized by year", tables of semi-finalists 1998–2022. The `warm` song is
  summer, going out, football *as content*. A results table is not that.
* **`football game` — 0 of 4.** A streamer reacting; commentary about Chip and Joanna Gaines;
  a news anchor's blooper; a character tutoring students. None is football.
* **`martial arts` — 3 of 8.** Four WEAK are comedy-franchise (Kung Fu Panda, Shaolin Soccer)
  and one WRONG is a "them trolling their own movie" meme. Weaker than a drop: this is the
  register problem again, in the `warm`/`hype` boundary, and the register markers do not reach
  it because those clips carry no format words.

Dropping `fifa` and `football game` costs 9 matches and removes 9 wrong ones — the only
zero-downside change on this table. It is a proposal.

## 5. The shopping list, re-derived at 2,661 with both changes live

Every prior ranking predates the library growing 2,003 → 2,661, the track-title tier shipping,
and this round's register fix.

```
clips        2,661
matched        448   (16.8%)
PARKED       2,213   (83.2%)

hype           262   9.8%    song04
warm            95   3.6%    song03
melancholy      78   2.9%    song01
triumphant      13   0.5%    song02

by tier: VISION_RULE 275 · TRACK_TITLE_MOOD 160 · FRANCHISE_MOOD 13
```

`TRACK_TITLE_MOOD` is now **36% of all matches** — the newest tier is already the second
largest, which no earlier ranking could have shown.

**The next purchase, measured.** Only one pending rule exists as executable code:

| | |
|---|---|
| `goofy` (the meme/reaction song) matches | **128** clips |
| ...parked today → **net unlock** | **119** |
| ...already matched elsewhere (re-assignment, not unlock) | 9 |
| library matched after | 448 → **567** (16.8% → **21.3%**) |

The 9 re-assignments come from triumphant (5), warm (2), melancholy (1), hype (1) — worth
naming, because counting them as unlocks is how a +129 becomes an argument for a song that
adds less.

**UNQUANTIFIABLE:** `eerie`, `tense`, `tender`, `sombre`, `lavish` are in the mood vocabulary
with **no executable rule anywhere** — not in `vision_rules`, not in `_pending_vision_rules`.
Earlier rankings quoted payoffs for some of these. Those figures are not reproducible and are
not repeated here. A rule that does not exist as code has no number.

## 6. The method rule, recorded where it binds

`docs/TESTING.md` **rule 19: a load-bearing number without a stated method is unmethodded, not
wrong.** Unmethodded is worse: a wrong number that states its method gets corrected; one with
no method gets repeated into the next ranking and the next purchase.

MEMEBOT-088's "38.2% scene-confirmed" is the case. No definition of *scene-confirmed* yields
13 of 34, and the report gave none. Re-audited with a method it came out at 55.9% — the
matcher's own baseline. The number had not merely missed by 17 points; it had **reversed the
finding**, naming an average performer as the worst one, and a round was spent acting on it.

The rule requires five things beside any deciding number: population, definition, denominator,
sample rule, and **configuration**. The last one earned its place this round: the same pending
rule measured **115** and **119** unlocks within an hour, with nothing about the rule changed
— the first run put it in a store containing only itself, the second appended it to the live
`vision_rules` last, as its own activation steps specify. Both are correct answers to
different questions and neither is interpretable alone. **119 is the number for the purchase
case**, because that is the configuration the rule would actually be activated in.

`tests/test_comedy_register.py` (9 tests) enforces what prose cannot: that the markers are
present, that the rationale names what was applied and what it cost, that the audit covered
every displaced clip, that one marker still carries the whole cost, and that an unaudited
phrase reports `null` rather than `0.0` — because a 0% reads as *measured and terrible*.

---

## Honest limits

* **The exclusion was applied exactly as proposed, cost and all.** 10 clips lose a correct
  song today. The narrowing that would return them is proposed, not applied, because it is
  not what the brief consented to.
* **`explosion` was sampled at 12 of 29**, per the stated sample rule. The other 17 are listed
  in `scratch/mb104_phrase_audit.json` and unread.
* **22 phrases are unaudited.** They fire once or twice each — 26 matches in total — and are
  reported as unaudited rather than scored.
* **The library moves while it is measured.** Other rounds walk it continuously; every figure
  here is from a single pass at 2,661 clips and is stamped as such.
* **`clippershq/song_library.py` was not touched** — BL-999 holds it and this change needed no
  code.

## Still broken, and whose file

* **`reacting to` at 58.3%** — `scratch/songs.json`, the operator's; the narrowing is proposed
  above with its measurement.
* **`fifa` and `football game` at 0%** — same file, same status: proposed, not applied.
* **Five moods with no rule** — `eerie`, `tense`, `tender`, `sombre`, `lavish`. Nothing to
  quantify until somebody writes a rule.
* **`MIN_DURATION_S` 5.0 vs `edit.py`'s 8.0 floor** — `memebot/scraper/`, MEMEBOT-071/072's.

## Suite and spend

`PYTHONUTF8=1 python tests/run_all.py`, discovery rule: **every `test_*.py` under `tests/` and
under any nested `<pkg>/tests/` directory** (MEMEBOT-026 — a suite count without its discovery
rule is not a count).

**Directly affected and green: 33 tests** — `tests/test_comedy_register.py` (9, new),
`tests/test_song_library.py`, `tests/test_track_title_tier.py` and
`tests/test_matcher_boundary.py`, run together against the applied store.

A full `run_all.py` was launched after the change and had not returned when this report was
published: the box is carrying nine other rounds and 32 concurrent Python processes. The
number is not quoted rather than guessed — which is this round's own rule 19 applied to
itself. The result is in the summary block that accompanies this report.

Campaigns unchanged; `config.json` untouched (0-byte diff).

**Spend this round: $0.0000.** No paid call was made — every measurement reads the local
library and the local store.
