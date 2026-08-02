# MEMEBOT-077 — 40-clip audit, the ceiling arithmetic, and a free signal we are throwing away

**Scope:** read-only. No matcher, no map, no `songs.json` touched. Everything below is a
measurement or a proposal.

**Filed as MEMEBOT-077, not 072.** Another round was already working under MEMEBOT-072 and has
published `reports/MEMEBOT-072.md` to origin. My `claim.py start MEMEBOT-072` at 13:42
silently overwrote their claim record — it did not warn. I did **not** overwrite their report:
the write refused because I had not read the file, I stopped and checked, and re-filed here.
Details in §7.

**Headline:** of the 14.3% of clips that get a song, **56% get a right one** — so **8.0%** of
the library ends up with a song a human would have chosen. 96% of *all* clips is not reachable
by buying songs at any sane number. The best lever measured here is neither a song nor a rule:
it is a metadata column we already have and never read.

---

## 1. The 40-clip audit

**Sampling, stated because it is not random.** Only 286 clips match anything and only 10 come
from the FRANCHISE tier. A proportional sample of 40 would hold ~1 franchise clip and could not
test the standing claim at all. So I took **all 10 franchise clips and 30 of the 276 vision
clips** by fixed stride. Franchise is over-represented 7×; per-tier rates are the readable
numbers and the pooled figure is re-weighted before it is quoted.

I read `vision_scene`, `vision_beats`, `vision_on_screen_text` and the caption for each clip and
asked: would this song, over this clip, read as *chosen* or as *accidental*? RIGHT = a viewer
would think it was deliberate. WEAK = defensible, not what a human picks. WRONG = actively
fights the clip. Consistency rule: **no action in the clip + an aggressive combat track =
WRONG; action present but tone off = WEAK.** Single judge, so the RIGHT/WEAK boundary is softer
than the WEAK/WRONG one — the WRONG calls are the load-bearing ones.

| tier | n | RIGHT | WEAK | WRONG |
|---|---|---|---|---|
| FRANCHISE | 10 | 4 (40.0%) | 4 (40.0%) | 2 (20.0%) |
| VISION | 30 | 17 (56.7%) | 7 (23.3%) | 6 (20.0%) |
| **population-weighted** | 286 | **56.1%** (160 clips) | 23.9% (68) | **20.0%** (57) |

**The prior claim is REFUTED at n=40.** "Every RIGHT came from the VISION tier, while FRANCHISE
routed clips nobody had looked at" is not what larger n shows: franchise produced **4 RIGHT out
of 10**, including the Dark Knight truck-flip chase and the Mad Max war-boy V8 ritual. Vision
does lead on RIGHT-rate (56.7% vs 40.0%), but the **WRONG-rates are identical at 20%**.
Franchise is weaker, not broken, and its weakness is specific: it routes on the *film*, so a
Gladiator monologue and a Gladiator battle receive the same combat track.

**The eight WRONG calls, and what they share.** Every one is a clip with *no action in it* that
matched on vocabulary describing the **setting**:

- *Tropic Thunder* — lost soldiers bickering in a river. Matched `gun,soldier,soldiers`.
- *Catch-22* — a satirical business argument. Matched `gun,soldier,soldiers`.
- *The Greatest Beer Run Ever* — an interrogation. Matched `combat,soldier,soldiers`.
- *The Simpsons* — Bart begs out of military school. Matched `strong:explosion`. No explosion.
- *Super Mario Bros.* — Bowser Jr. and a caged Lumalee delivering a dark joke. Matched
  `strong:explosion`. No explosion.
- *Avengers: Endgame* — Tony carrying his daughter by the cabin, a quiet meme.
- *Avengers: Endgame* — "you've lost everything, but God says try one more time", a faith edit
  whose own declared track is *Like a Prayer (Choir Version)*.
- **The cleanest failure in the set:** a yacht party cutting to a storm, matched
  `celebrating,dancing → warm`. The burned-in text reads *"2022: ChatGPT does your homework.
  2026: AI now does the job you studied for."* It is a doom meme about layoffs. The rule read
  the surface and inverted the meaning.

A war satire and a war film share a vocabulary. The rules cannot tell them apart because they
match nouns, and nouns name the setting.

### Three separators I tested and could not confirm

Reported because the negative results change the recommendation:

| candidate | result |
|---|---|
| `audio_class` (stored, 92.5% filled, **not read**) | music-only 10R/5W vs dialogue-over-music 8R/3W — **does not separate** |
| which sub-field the matched term came from | scene-confirmed 57.9% RIGHT vs not-in-scene 50.0% (n=30) — **does not separate** |
| duration | WEAK median 59.9s vs RIGHT 40.8s vs WRONG 26.4s — suggestive (the WEAKs are long video essays), too small to act on |

I expected `audio_class` to separate talk from action and it does not. That matters: the
failure is **semantic, not lexical**, so it will not yield to a cheap gate.

## 2. The ceiling arithmetic

Fitting the six measured per-song gains (meme +129, wholesome +40, grief +35, pressure +29,
money +29, horror +18) gives `gain(rank) = 106.6 × rank^-0.955` — a Zipf curve, the right
family for subject matter in a repost library.

| songs | clips covered | coverage | the next song unlocks |
|---|---|---|---|
| 10 | 566 | 28.5% | 16.6 clips |
| 20 | 676 | 34.0% | 7.1 |
| 50 | 804 | 40.5% | 2.7 |
| 100 | 898 | 45.2% | 1.3 |
| 200 | 992 | 50.0% | 0.7 |
| 1,000 | 1,220 | 61.4% | 0.1 |

**96% of all clips needs ~72,800 songs** on the fitted curve. Even the deliberately optimistic
bound — assume the tail never thins and every further song is as good as the *sixth* (18 clips)
— needs **~85 songs**. The honest range is 85 to ~73,000 and both ends say the same thing.

*Caveat, plainly: six points extrapolated four orders of magnitude. The exact figure is not the
deliverable; the shape is. The curve falls below one clip per song around the 145th song, and no
catalogue reaches 96% after that.*

**So 96% of all clips is not a sane target.** The sane goal is the operator's second
formulation — **96% of the clips we do match are right** — which is a precision problem on 286
clips, not a catalogue problem. Today that number is **56.1%**.

Note also: of four songs bought, **song02 (triumphant) matches zero clips** and song01 matches
three. The catalogue is not the binding constraint; the routing is.

## 3. Signals bought and unused

| signal | fill | read by `match()`? |
|---|---|---|
| `vision_scene`, `vision_beats` | 99.1% | yes |
| `vision_on_screen_text` | 80.7% | yes |
| `vision_title` | 69.8% | yes (franchise tier only) |
| `valence_text` | 98.1% | yes — **but the map is empty** |
| `content_genre` | 17.7% | yes — **but the map is empty** |
| `franchise` | 34.9% | yes |
| **`caption`** | **99.9%** | **no** |
| **`audio_class`** | **92.5%** | **no** |
| **`media_duration_s`** | **98.8%** | **no** |
| **`like_count`** | **89.8%** | **no** |
| **`speech_frac`** | **67.8%** | **no** |
| **`track_title`** | **28.7%** | **no** |

Two tiers are **wired but inert**: `genre_mood_map` and `valence_mood_map` are both `{}`, so the
genre and valence tiers can never fire. `valence_text` is filled on 98.1% of clips and routes
nothing. Fill them or delete the tiers — a tier that cannot fire is a comment that costs a lookup.

Nothing here proposes listening to the source audio. Audio mood classification (40%
reproducibility), automatic drop detection (100% fabrication) and source separation (39×) stay
closed and are not reproposed.

## 4. The operator's "similar song" idea — viable, and better than the premise

**The premise does not hold; what replaces it is more useful.** The expectation was that declared
tracks would be trending rap. The measured top of the distribution is **production-library music
with openly descriptive names**: *milk and cookies* (19), *hallucinations.* (16), *whisper walk*
(15), *forest knight* (14), *don't leave me.* (14), *it snows silently* (13), *hidden sorrow*
(11), *piano craft* (10), *jolly morning* (8).

That is *better* than a rap title, because **the name states the mood the poster chose after
watching the footage** — free, on 28.7% of clips (575), of which **475 are currently parked**.

### The cross-check, which is the most alarming number in this report

Of the 100 clips we already match that *also* declare a track, 46 have a name unambiguous enough
to read (the other 54 I left UNKNOWN rather than guess):

> **AGREE 7 (15.2%) — DISAGREE 39 (84.8%). Every single disagreement is us assigning `hype`.**

Posters who chose *hidden sorrow*, *don't leave me.*, *it snows silently*, *piano craft* and
*milk and cookies* over their own footage got an aggressive combat track from us.

**What this is and is not.** The poster's choice is not ground truth — we are making a different
video, and a sad piano bed over a sword fight is one editorial choice while a hype track is
another. This is a **disagreement measure, not an error measure**. What it proves is narrower
and still damning: our matcher assigns `hype` to **87% of everything it matches**, so it cannot
express the choice the source creators actually make. At 87%, one mood is not a choice, it is a
default — and it corroborates the 20% WRONG rate from an independent direction.

### The payoff

**21 hand-read titles route 152 currently-parked clips to songs we already own** — song01 +90,
song03 +39, song02 +18 (its first clips ever), song04 +5. No purchase, no paid call, no audio
touched.

| judgements | parked clips un-parked | per judgement |
|---|---|---|
| 10 | 108 (5.4% of the library) | 10.8 |
| 20 | 174 (8.7%) | 8.7 |
| 50 | 248 (12.4%) | 5.0 |
| 120 | 327 (16.3%) | 2.7 |

The whole 475 is reachable at ~269 judgements, though the tail needs moods we may not own.

## 5. Multi-song variants — **zero clips qualify today**

Evaluating each rule *alone* against every clip (the shipped matcher is first-hit-wins and
structurally cannot report a second match):

> **0 of 2,003 clips match more than one rule.**

Not a bug. `requires_any` — the guard forcing the rule's subject to actually be present — blocks
**450 of 812** cross-rule evaluations, and "no phrase at all" accounts for 360 more. The four
rules target genuinely disjoint subjects. Only **16 clips** are one weak phrase short of a second
match, and I relaxed nothing to manufacture one.

**Variants are a catalogue-growth feature, not a rules feature.** Two things should be specified
now, before either is built:

**a. The record needs a `variant_group`, and this is the load-bearing part.**
`song_library.bias_map` keys outcomes on `"%s@%s-%s" % (song, start_sec, end_sec)` — **there is
no clip dimension**. Render one clip with two songs today and the outcomes land in two unrelated
global buckets, so the comparison is confounded by clip quality: the strongest clip's song wins
regardless of the song. A paired test needs the loop to difference *within* a clip. Minimum
additions to the render record:

```
variant_group   the clip+batch identity shared by every variant   <- the paired key
variant_index   1..n within the group
variant_of      clip_id, explicit rather than parsed from a path
edit_signature  zoom / trim window / template actually applied    <- proves not-a-duplicate
rule_tier + matched_on   PER VARIANT, since each song has its own evidence
```

**b. A naming hazard.** `edit.py --variants` and the `_v01` suffix **already mean
randomisation-variant** — the same song rendered twice with different jitter. A song-variant is a
different axis. Reusing the word will silently merge two populations in the ledger; pick a
distinct term before either is built.

## 6. Recommended order, with measured gain

1. **Hand-map declared track titles → mood.** +152 clips (+7.6 pts) for **21 judgements**, using
   songs already owned. Best gain-per-unit-of-work measured anywhere in this round, and it needs
   no purchase. Extends to +475 clips at ~269 judgements.
2. **Fill or delete `genre_mood_map` / `valence_mood_map`.** `valence_text` is 98.1% filled and
   routes nothing. Cheap either way; today it is dead weight.
3. **Buy the meme song (+129), then wholesome (+40).** The ranked list is sound. After the sixth,
   songs are worth under a point each — stop there and revisit.
4. **Rule precision work.** Worth ~6 pts of coverage, and it is the *only* route to the
   56.1% → 96% precision goal, which is the target that is actually achievable. Start with the
   setting-vs-action confusion: `soldier`/`gun`/`war` matching satire and dialogue, and
   `strong:explosion` firing on clips with no explosion. No cheap gate I tested separates these —
   it will take rule surgery.
5. **Multi-song variants.** Not reachable today. Specify `variant_group` now; build when the
   catalogue supports it.

**Off-brief, one line each:** `song02` has matched zero clips since purchase. And
`strong:explosion` fired on three clips in a 30-clip sample with no explosion anywhere in the
scene — that single phrase looks like the highest-yield rule fix available.

## 7. The claim collision, recorded

`tools/claim.py start MEMEBOT-072` at 13:42 reported *"claimed … no path conflicts"* and did not
warn that MEMEBOT-072 already had a live claim from another round — it **silently overwrote the
claim record**, so that round's intent is gone from `.claims/` and I cannot restore its text.
Their work is intact: `scratch/mb072_unattended.py` (13:06), `scratch/mb072_rotation.py` (13:19),
`scratch/MEMEBOT-072.md` (13:52), `scratch/mb072_work/`, and `reports/MEMEBOT-072.md` already on
origin.

The report itself was saved by an unrelated safety property: **Write refuses a file that has not
been read**, so my overwrite of their report failed, I checked instead of retrying, and re-filed
here. That is luck, not a guard. `claim.py start` should refuse an id that already holds a live
claim unless `--force` is passed, exactly as `publish_report.py` now refuses an existing report
path — the same lesson MEMEBOT-057 paid for. `tools/claim.py` is not mine and is currently
modified in the working tree by another round, so I have not touched it.

## 8. Suite state

**132 of 135 suites green; 3 red, none of them mine.** This round changed no shipping file —
its only write outside `scratch/` is a new, untracked `docs/claims/MEMEBOT-077.claims`.

| red suite | attribution |
|---|---|
| `test_claims_manifest.py` | **Verified not mine by removal:** the same test fails identically with my claims file moved aside. |
| `test_no_unchecked_stdout.py` | Fails on a PENDING deferral entry in `clippershq/clip_pipeline.py` — held by BL-899/BL-958, never touched here. |
| `test_dashboard.py` | Dashboard code, untouched by this round. |

The five suites covering what this round actually reads are green: `test_song_library`,
`test_song_library_cache`, `test_song_library_meme_rule`, `test_pipeline_join`,
`test_clip_pipeline_gate`.

13 rounds were in flight during the run, several holding the files above — a suite count is a
moment, not a property.

**Spend: $0.00.** No paid calls.
