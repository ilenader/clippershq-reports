# MEMEBOT-003 — The song library, the matching rule, and why it must gate on `valence` and not on `genre`

**Date:** 2026-08-01 · **Type:** Spec · **Spend:** $0 · **READ-ONLY** — nothing implemented
**Sample:** `scratch/memebot003_song_library.json` — 5 imaginary songs, 5 **real** clips
Claimed as MEMEBOT-003. Measured against the live library (**629 clips**, 2026-08-01).

---

## The measurement that should drive the design

Before proposing a rule, here is what the clip record can actually offer today:

| signal | fill | provenance |
|---|---|---|
| `caption` | 100% | declared |
| `play_count` | 100% | declared |
| `media_duration_s` | 99.0% | declared |
| **`valence_text`** | **99.0%** | derived |
| **`layout`** | **67.4%** | **measured** |
| `franchise` | 45.2% | **derived — 0 declared** |
| `content_genre` | 28.3% | derived 176 / **declared 2** |
| `content_medium` | **0%** | — |
| `subtitle_text` | **0%** | — |
| `title` / `genre_declared` | **0.3%** (2 clips) | declared |

**Coverage of the obvious matching key:**

| | clips | share |
|---|---|---|
| genre AND franchise | 167 | 26.6% |
| genre only | 11 | 1.7% |
| franchise only | 117 | 18.6% |
| **NEITHER** | **334** | **53.1%** |

Two things follow, and they are the spec's two load-bearing decisions.

---

## 3. The matching rule — and the provenance answer

### Requiring `declared` would give you a two-clip library

The brief asks whether song matching should require declared provenance. **It must not.**
Measured: `content_genre` is declared on **2 of 629 clips (0.3%)** and `franchise` on **zero**.
A declared-only matcher is a zero-error subset in exactly the sense that an empty set has no
errors. The declared panel is thin because it only started being stored in BL-843 and no walk
has run since — it will grow, but it cannot be the gate today.

**Accept `derived`, and carry the tier on every output.** Every match record stores
`confidence` (`declared` / `derived` / `fallback`) and `needs_review`. That way a bad batch is
*attributable* — you can ask "were the misses all `fallback`?" — instead of being a vague sense
that the music is off. This is the same discipline `field()` enforces in the library: the value
travels with its attribution.

### The rule: four tiers, first hit wins

```
TIER 1  FRANCHISE_MOOD   franchise in franchise_mood_map        -> that mood     (18.6-26.6%)
TIER 2  GENRE_MOOD       any content_genre in genre_mood_map    -> that mood     (+1.7%)
TIER 3  VALENCE_MOOD     valence_text -> mood                   (99% coverage)
TIER 4  FALLBACK         the house set                          (always answers)
```

Tiers 1 and 2 are the *specific* ones and they cover about a quarter of the library. **Tier 3
is the one that actually carries the system**, because `valence_text` is present on 99% of
clips while genre is present on 28%. That inversion is the main finding here: the signals that
feel like the right key are the sparse ones.

`franchise` is placed **above** `genre` deliberately — "Young Sheldon" tells you more about the
right music than "comedy" does, and it is the better-filled of the two (45.2% vs 28.3%).

### What NOT to gate on

- **`content_medium`** — 0% filled. It is wired but no walk has populated it.
- **`subtitle_text`** — 0% filled, same reason. When it lands it is *spoken dialogue*, which is
  a good tone signal, but it is not available today.
- **`is_templated`** — 1.9%, and BL-692 **refuted** templating as a quality signal anyway
  (engagement is *worse* on templated pages, 1.0% vs 2.7%, p=0.021).
- **The Gemini scene description**, when it lands. BL-835 measured it declining correctly 9/9 on
  an unanswerable control, which is genuinely good — but it costs $2.47–$9.21 per 1,000 and
  the mood mapping it would feed is already covered by valence at $0. Add it as a **Tier 0**
  override later if measurement justifies it; do not make the first version depend on it.

---

## 2. Why hand-marked hooks are correct — put this in the code, not just the spec

**Automatic drop detection was measured at 100% fabrication (BL-690).** It returned a timestamp
on all 36 clips *including all 19 that had nothing there*, and — the part that kills the whole
approach — **its most confident outputs were the wrong ones**. Confidence did not separate right
from wrong, so no threshold rescues it. Requiring timbre agreement removed every fabrication but
cut correct hits from 4-of-8 to 2-of-8, with 11 of 17 tracks returning nothing at all.

**Automatic audio genre closed at 40% reproducibility (BL-795)** — the *same clip* returning
different answers on repeated calls. A tag that changes when you ask twice cannot key a
rotation experiment, because you can never tell whether the output changed or the label did.

Hand tags are not a pragmatic compromise pending a better model. **They are the only method
measured to work.** The spec's instruction to a future maintainer: an automatic hook detector
may be *added* alongside, writing to a separate `hooks_auto` list that never feeds a render
until it has been measured against the hand-marked windows on the same tracks. It may not
replace `hooks`.

---

## 1. The song record

```json
{
  "song_id": "sng_0002",
  "path": "memebot/scraper/sounds/library/last_lap.mp3",
  "title": "Last Lap", "artist": "KRVN",
  "mood": "hype",            // YOUR vocabulary, hand-set
  "genre": "phonk",          // YOUR vocabulary, hand-set
  "duration_s": 141.0,
  "hooks": [
    {"hook_id": "h1", "start_s": 44.0, "end_s": 52.0, "note": "beat switch", "uses": 0},
    {"hook_id": "h2", "start_s": 96.0, "end_s": 100.0, "note": "cowbell run", "uses": 0},
    {"hook_id": "h3", "start_s": 12.0, "end_s": 16.0, "note": "cold open",   "uses": 0}
  ],
  "uses": 0,
  "enabled": true
}
```

Notes on three fields that are not obvious:

- **`uses` lives on the hook AND on the song.** Rotation needs both: you want hook variety
  within a song *and* song variety across the batch, and one counter cannot express both.
- **`enabled`** so a song can be retired without deleting it and orphaning the render records
  that reference it.
- **`note`** is for you, not the machine. When a window under-performs you need to know which
  moment it was without re-listening.

Two vocabularies (`mood_vocabulary`, `genre_vocabulary`) sit at the top of the file and are
**closed sets**. A typo'd mood should fail loudly at load, not silently create a bucket of one.

---

## 4. Rotation and attribution

### Rotation: least-used-first, deterministic — not random

Random selection does not spread evenly; it clumps. Over 40 renders across 10 hook windows,
random assignment routinely leaves some windows at zero and others at five, and you cannot
tell an under-performing window from an under-*sampled* one.

```
candidates = hooks of all enabled songs whose mood matches the tier's mood
pick       = min(candidates, key=(hook.uses, song.uses, song_id, hook_id))
then       = hook.uses += 1 ; song.uses += 1   (persisted immediately)
```

Least-used-first with a **deterministic tie-break** gives every combination comparable exposure
and makes a batch reproducible — the same library state and the same clip list produce the same
assignment, which is what lets you re-run a comparison.

### Attribution: the columns must be written by the renderer

MEMEBOT-001 found that memebot has **no database, manifest, or processing log**, that idempotence
is filesystem-based, and that the transform fingerprints are *printed to the console and
discarded*. So today the answer to "which song was on that video" is unrecoverable.

**This is the `message_variant` lesson exactly** — on the email side the columns existed and
nothing wrote them, so a year of sends produced no learning. One row per rendered variant,
written at render time:

```
rendered_at, run_id, clip_id, source_stem, variant, out_path,
song_id, hook_id, audio_ss_s, audio_to_s, place_at_s, loop_count,
rule_tier, matched_on, confidence, needs_review
```

`clip_id` is the join back to the library; `source_stem` is memebot's own `{stem}_v{NN}`
convention, which is the only trace Pipeline A currently keeps. Both are recorded because they
are the two halves of a link that is otherwise broken — and Pipeline B outputs have **no**
upstream link at all today.

---

## 5. The fallback — a house set, and it is the PRIMARY path

**Recommendation: a house set. Never skip the clip.**

53.1% of the library has neither genre nor franchise. A skip rule discards the majority of your
inventory to avoid a wrong song, which is the wrong trade when the cost of a mediocre pairing is
one under-performing video and the cost of skipping is no video at all.

The fallback is not a dumping ground:

1. **Try valence first** (Tier 3) — 99% coverage, so the true no-signal population is ~1%, not
   53%. The clip with *no* genre, *no* franchise and *no* valence is the rare case.
2. **The house set is a curated, mood-neutral subset** you mark yourself — songs that work
   under anything.
3. Every fallback render carries `confidence: "fallback"`, so you can measure the house set
   against the matched tiers. If fallback performs *as well*, that is a real and useful finding
   about how much the matching is worth.

---

## 6. The length math

Library median clip is **40.7s**; 22% are under 15s. A hand-marked hook is typically 4–8s. So the
common case is a short hook against a long clip, and the hook must land **where you want it**,
not merely at t=0.

Three numbers are passed, and they are separate on purpose:

| field | meaning |
|---|---|
| `audio_ss_s` | the hook's **start in the song** — memebot's input-side `-ss` |
| `audio_to_s` | the hook's **end in the song** |
| `place_at_s` | where in the **finished video** the hook's first beat lands |

`audio_ss/-to` are copied verbatim from the marked window. `place_at_s` is computed:

```
hook_len = audio_to_s - audio_ss_s
if clip_len < 2 * hook_len:      place_at_s = 0.0        # no room to place it later
else:                            place_at_s = clamp(0.43 * clip_len, 0, clip_len - hook_len)
```

43% rather than 50%: on a caption-bar clip the payoff sits just past the middle, and the beat
should arrive *slightly before* it, not on top of it. It is a starting value to tune, and the
render record stores `place_at_s` so it can be tuned against outcomes.

**Looping is memebot's job, but the count is ours to state.** Pipeline B's mixer already
supports `-ss`, looping short tracks, `-shortest` and fades (`edit.py:1020-1063`) — so nothing
new is needed technically. `loop_count = ceil((clip_len - place_at_s) / hook_len)` is passed so
the caller and the renderer agree on what should happen, rather than the renderer deciding
alone and the record not knowing.

### The integration gap this spec runs into

Pipeline A's job format is `filename.mp4 | caption text` — **two fields**. It cannot express an
audio path or offsets. MEMEBOT-001 called this out as the one blocker, and it still is: the
mixer lives in Pipeline B, the caption renderer lives in Pipeline A, and there is *no code path
between them*.

This spec deliberately does not choose the plumbing — that is MEMEBOT-004's territory (an
end-to-end orchestration spec is in flight as I write this). What it does assert is the
**contract**: whatever carries the job must carry `path`, `audio_ss_s`, `audio_to_s`,
`place_at_s`, `loop_count`, plus `song_id`/`hook_id` for the record. A pipe-delimited format
will not stretch to that; a JSON job line will.

---

## The sample

`scratch/memebot003_song_library.json` — 5 imaginary songs with **10 hook windows** between
them, and **5 real clips** from the library with their values verbatim, one per case:

| case | clip | signals | tier | song / hook |
|---|---|---|---|---|
| declared-rich | `39151460…` 57.1s | genre `[sitcom, comedy]`, franchise *Two and a Half Men* | GENRE_MOOD | Rubber Duck Riot / h2 |
| genre only | `39260657…` 59.8s | genre `[drama, action]` | GENRE_MOOD | Last Lap / h1 |
| franchise only | `38999232…` 52.6s | franchise *Young Sheldon* | FRANCHISE_MOOD | Rubber Duck Riot / h1 |
| short (<15s) | `34301763…` **7.2s** | nothing at all | FALLBACK | Last Lap / h2, `place_at_s = 0.0` |
| bare | `39035331…` 42.6s | valence `positive` only | VALENCE_MOOD | Coliseum / h1 |

Validated: every `audio_ss_s`/`audio_to_s` matches its marked window, every `hook_len_s` matches
the window length, and no placement overruns its clip.

## Honest limits

- **The mood maps are not specified, because they are yours.** `franchise_mood_map` and
  `genre_mood_map` are empty scaffolding in this spec. Nobody but you can say whether *Young
  Sheldon* is `goofy` or `warm`, and a guess here would become a default nobody revisits.
- **43% and the tier order are proposals, not measurements.** There is no outcome data yet —
  that is what the attribution record exists to produce. Expect to move them.
- **Fill rates will shift.** BL-843 wired `subtitle_text`, `content_medium` and ~30 declared
  caption fields into storage, but **no walk has run since**, so they read 0% today. The next
  walk changes the inputs to this rule, and `content_genre`'s declared share should rise from
  its current 2 clips.
- **`layout` (67.4%, measured) is unused by this spec** and is the best-attributed signal in the
  library. Caption-bar vs full-bleed plausibly wants different music. I did not build it into
  the rule because there is no evidence for the mapping — but it is the first thing I would test.
- **No same-batch A/B is specified.** Rotation gives comparable exposure, which is a
  precondition for learning, not a substitute for a designed comparison.
