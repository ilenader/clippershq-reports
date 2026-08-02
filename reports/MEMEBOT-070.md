# MEMEBOT-070 — The rule cache keyed on content, the vocabulary widened, and the meme song made a one-move purchase

**Round:** MEMEBOT-070 · **Date:** 2026-08-02 · **Spend:** **$0.00**, no paid calls
**Claim:** `MEMEBOT-070`, seven repeated `--write` flags, *"7 path(s) registered individually"*.
`claims_read.py --holders` run per target (all FREE); `git status --porcelain` checked —
`MEMEBOT-067` had work **staged** (`A ` in column 1), so this round staged only its own paths
and never `git add -A`.

Acts on [MEMEBOT-068](https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/MEMEBOT-068.md).

---

## 1. The cache is keyed on content, and the old key really did corrupt matches

`_rule_regexes` cached on `(id(rule), idx)`. `id()` is unique only among **live** objects:
CPython hands a garbage-collected object's address straight to the next allocation, so any
caller that builds a trial rule, measures it, and drops it eventually gets a **new** rule
sitting where a **dead** rule was cached — and matches it with the dead rule's regexes.

It now keys on the six phrase lists and nothing else. `mood` is deliberately excluded: it
decides where a match is *routed*, never whether one happens, so two rules with identical
phrases can and should share one compiled entry.

**This was not a theoretical hazard.** Monkeypatching the old key back and running the
build/measure/drop loop:

| Key | Iterations matching the WRONG phrase |
|---|---|
| `(id(rule), idx)` | **60 of 400** — first contamination at iteration 81 |
| content | **0 of 400** |

The `idx` argument is gone from the signature, not just from the key, so it cannot drift back
in. `_RULE_CACHE` remains a dict, so the existing harnesses that call `.clear()` still work —
the clear is now unnecessary rather than load-bearing.

### The invariant is permanent now

MEMEBOT-068 found this because a **behavioural invariant** broke, not by reading code: under
first-hit-wins an appended rule can only see what earlier rules rejected, so its marginal gain
must *shrink*. `B_eerie_horror`'s gain grew 19 → 47 while `C_tense_crime` collapsed to 0.

`tests/test_song_library_cache.py` pins three separate things, and they are not redundant:

- `test_collision_under_address_reuse` — drives the id-reuse mechanism directly.
- `test_marginal_gain_never_grows_as_rules_are_appended` — the invariant that actually caught it.
- `test_totals_can_agree_while_attribution_is_wrong` — pins *why* both are needed: MEMEBOT-068's
  corrupted and clean runs both totalled **566**. A test asserting the total would have passed
  on the bug.

---

## 2. I was wrong about "0 regressions", and the stricter test found one

MEMEBOT-068 reported *"0 clips lost the song they have today"*. That check compared **sets of
clip ids** that had a mood before and after. A clip moving from `hype` to `goofy` is in **both
sets**, so a membership check structurally cannot see it. It reported 0 because it was asking
the wrong question, not because the answer was 0.

Re-measured **per clip**, comparing the mood itself, activation moves exactly one:

> `3949927977003962019_46975058585` — an **Avengers: Endgame** scene captioned
> *"when you finally decide to leave the game... but your squad needs you."*
> Today: `franchise: Avengers: Endgame (2019) → hype`. On activation: `vision strong: "when you" → goofy`.

That trade is arguably **correct** — TIER 0 outranks the franchise tier precisely so what a
clip *shows* beats what the poster typed, and this clip is a meme. It is now recorded in the
rule's `_activation_impact` and pinned by name in the test, so a **second** one turns the suite
red instead of passing unnoticed.

---

## 3. The meme rule is prepared — and deliberately NOT in `vision_rules`

The brief asked for it shipped disabled. The obvious placement is `vision_rules`, inert because
`goofy` has no enabled song. **I built that, tested it, and rejected it on a measurement.**

`_vision_match` is **TIER 0**. It runs *above* the franchise tier. So a rule that "does nothing"
still **intercepts**. All four songs are enabled, so that Endgame clip renders *today* — and
with the meme rule merely present it matches `goofy`, `pick("goofy")` returns `(None, None)`,
and `render_plan` **parks it**. A renderable clip lost, bought for nothing, purely because a
rule was sitting there.

So it ships in **`_pending_vision_rules`**, a key the matcher never reads:

| | In `vision_rules` (inert) | In `_pending_vision_rules` |
|---|---|---|
| Regressions today | **1 renderable clip parks** | **0, structurally** |
| `validate()` | 1 warning to learn to ignore | **clean** |
| Live contract | `vision_rules` 4 → 5, existing test needs weakening | **unchanged** |

Activation is still one move, and the operator invents nothing: `_activate` carries the exact
song entry to paste, and `_activation_steps` carries the order — *rule LAST, song enabled, and
step 3 without step 4 parks every clip it matches.*

**No new code path.** The FORM is a conjunction — a caption **and** a reaction — which `strong`
cannot express, so it uses semantics the engine already had: caption markers in `requires_any`
(a hard gate) and reaction markers in `weak` (needs **two distinct**). `song_library.py` gained
no new field and no new branch in `_vision_match`.

**Activation unparks 130 clips, not 129.** MEMEBOT-068 measured 129; the library has grown by
one matching clip since. The corpus is live and appending.

`hooks` ships **empty** on the stub. Filling it with placeholder windows is what the store's own
readme forbids in capitals — BL-690 measured automatic drop detection at **100% fabrication**,
and guessing them by hand is the same mistake wearing a different hat.

---

## 4. The vocabulary now has a token per proposed song

`mood_vocabulary`: 7 tokens → **10**. Added `tender`, `sombre`, `lavish`; `goofy`, `eerie` and
`tense` were already free. Each carries a note in `_mood_vocabulary_notes` saying *why it cannot
reuse an existing token*, because that is the part that bites:

> `sombre` cannot be `melancholy`. **`melancholy` IS song 1, the breakup ballad.** A grief rule
> routed there hands every dead-dog clip the breakup song — *silently*, because `pick()`
> succeeds.

A song purchase is now a one-file edit rather than two coupled ones. `test_new_tokens_are_not_
already_taken_by_a_song` asserts none of the six collides with an existing song's mood.

---

## 5. The valence map is untouched

`valence_mood_map == {}` and `fallback_moods == []`, pinned by test. MEMEBOT-068 measured every
version and all three fail: `negative → melancholy` routes **326** clips to the breakup ballad;
`negative → sombre` adds **298** clips the rules had already *rejected*, **19%** carrying an
explicit comedy marker; the full map gives `triumphant` **zero** while dumping **850** clips
(42% of the corpus) on the fight song off a `neutral` label.

## 6. The two non-purchases are recorded in the store

`_non_purchases` in `songs.json`, so the next round costing the park does not re-propose them:

- **superhero_comic** — 163 parked, only **18 action-bearing**. Song 4 already took the fights;
  what parks is fandom *talk* (unboxings, fan art, casting discourse). An "epic superhero" song
  would buy 18 clips.
- **music_performance** — 113 clips that **already contain music**.

---

## VERIFICATION

| Check | Result |
|---|---|
| `tests/test_song_library_cache.py` | **9/9 pass**; goes RED on the old key (60/400 wrong) |
| `tests/test_song_library_meme_rule.py` | **20/20 pass** |
| Per-clip zero-regression, real 2,003-row corpus | 0 lost a song; 1 known trade |
| `validate(scratch/songs.json)` | **`[]` — clean** |
| `vision_rules` / `songs` | **4 / 4 — unchanged** |
| `config.json` | unmodified, parses, **5 campaigns** intact |
| Store edit | **idempotent** — re-running changes nothing |
| Full suite | **130 of 131 green** (1,095.9s) |

### The one red suite is not this round's

`tests/test_claims_manifest.py` fails on one check,
`test_no_manifest_claims_it_cannot_verify_while_it_verifies`, and it names exactly one file:

```
these manifests say they cannot be verified, and then verify cleanly:
  docs/claims/MEMEBOT-067.claims
```

That manifest is **MEMEBOT-067's**, committed by them at `ddb4a90` *("enrol the claims
manifest, now that its code is at HEAD")*. Its header says the fix "is not claimable here"
because it lives in the nested `memebot/` repo — and now that the manifest verifies cleanly,
the caveat reads as stale and the check calls it. Nothing in it relates to this round: the
only mentions of `song_library.py` anywhere in that suite are `TIER_TITLE`/`TIERS`
supersession fixtures, which are untouched here and all passed. **Their file, their call.**

## FILES

| Path | What |
|---|---|
| `clippershq/song_library.py` | `_rule_key` + content-keyed `_rule_regexes`; `idx` removed |
| `scratch/songs.json` | +3 mood tokens, `_pending_vision_rules`, `_non_purchases` |
| `tests/test_song_library_cache.py` | the collision, the invariant, the totals trap |
| `tests/test_song_library_meme_rule.py` | pending-ness, the form, zero-regression |
| `scratch/mb070_store_edit.py` | the idempotent store edit |
| `docs/claims/MEMEBOT-070.claims` | claims manifest |

## STILL OPEN

- The meme rule's precision is still a **14-clip spot-check** (13/14), not a hand-labelled
  measurement. Sample ~20 before buying the song.
- No song bought, added or enabled. Songs 2–6 on the ranked list still need their files.
- `clippershq/clip_pipeline.py` is held by **BL-899** and untouched.
- `MEMEBOT-067`'s staged work was left staged and uncommitted — not this round's to land.
