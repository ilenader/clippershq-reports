# MEMEBOT-021: Bed level and treatment are one decision. Also, the duck depth I reported last round does not survive real dialogue.

**Date:** 2026-08-01 · **Type:** Implementation + measurement · **Spend:** $0.00 · **No paid call, memebot/ only, the 61 local clips**

Honesty tiers: **VERIFIED** (measured here), **CORRECTION** (a previous round's number that does not survive real material), **GAP**.

---

## Verdict first

Bed level and treatment now come from one place — BL-848's four-way audio class — and `mode: auto` routes on that class instead of source loudness, so the duck path can actually fire. The dialogue bed moved from **-20..-14 dB to -8..-5 dB** relative to the voice, which is what makes the new track audible at all.

Three things matter more than the wiring, and two of them correct my own previous round:

1. **MEMEBOT-009's -8.50 dB duck depth is an artifact of injected speech.** That bench mixed TTS into real clips at +6 dB over their own bed. On clips carrying their **own** dialogue, the same shipped setting delivers **-1.12 dB**, and the best setting tested reaches only **-2.64 dB**.
2. **There is a physical ceiling and it is low.** Across 12 real dialogue-over-music clips the median gap between speech and the music between words is **+2.9 dB** (range -1.4 to +8.9). One clip is *negative* — the music between words is louder than the words. A sidechain keyed off unseparated audio cannot duck harder than that gap allows.
3. **The bed LEVEL does nearly all the work; the duck is a ~2 dB refinement on top.** Moving the track from -14 to -6 dB changes the speech-to-bed ratio by 8 dB. Ducking at that level adds 2.2 dB.

And the finding that reframes the corpus: **the 61 local clips are 80.3% music-only and contain zero dialogue-only clips**, against BL-853's library figures of 51.9% / 43% / 7.6%. This corpus is not the library.

---

## What shipped

| file | what |
|---|---|
| `memebot/scraper/duck.py` | class → treatment routing, class → bed plan, `relative_basis()`, clip_speech vocabulary accepted |
| `memebot/scraper/edit.py` | `mode: auto` routes on class; bed volume routes on class; `--audio-class`, `--speech-dbfs`; unknown treatment now LOUD |
| `memebot/scraper/config.yaml` | `treatment: auto`, `volume_mode: auto`, dialogue offsets -8..-5, `auto_threshold_db` marked dead |
| `memebot/scraper/tests/test_duck.py` | 43 tests (up from 29) |

**72 tests pass** in `memebot/scraper/tests/`.

```
python scraper/edit.py --template white_frame --captions caps.txt \
    --audio-class dialogue-over-music --speech-dbfs -12.8
```

---

## Part 1 — The class, measured on all 61 clips

**VERIFIED.** `clip_speech.decode_pcm` + `analyse` over every local clip, **25.5 s total, 0.42 s per clip = 0.116 CPU-hours per 1,000** — about a quarter of BL-846's declared 0.44.

| class | n | this corpus | BL-853 library |
|---|---|---|---|
| music-only | 49 | **80.3%** | 51.9% |
| dialogue-over-music | 12 | **19.7%** | 43.0% |
| dialogue-only | **0** | **0.0%** | 7.6% |
| silent | 0 | 0.0% | — |

**GAP, and it bounds everything below.** There is no dialogue-only clip here and nothing near one: the closest sits at **-22.9 dBFS** between words, 22 dB the wrong side of the -45 dBFS line that defines the class. Every dialogue measurement in this report is therefore from dialogue-**over**-music only.

---

## Part 2 — What bed level makes the duck audible

**VERIFIED.** 3 real dialogue-over-music clips, speech windows taken from **the labeller's own Silero VAD spans** — no synthetic speech anywhere. SBR is the speech-to-bed ratio during speech: how far the dialogue stands above the new track.

| bed vs source | bed-leg depth | **MIX duck depth** | pumping | **SBR unducked** | **SBR ducked** |
|---|---|---|---|---|---|
| -18 dB | -1.14 dB | **-0.02 dB** | 0.05 | +16.8 dB | +19.0 dB |
| **-14 (old range)** | -1.19 | **-0.04** | 0.10 | +12.8 | +15.0 |
| -10 | -1.14 | -0.09 | 0.19 | +8.8 | +11.0 |
| **-6 (new range)** | -1.15 | **-0.25** | 0.67 | **+4.8** | **+7.0** |
| -3 | -1.20 | -0.39 | 0.83 | +1.8 | +4.0 |
| 0 | -1.19 | -0.58 | 1.33 | **-1.2** | +1.0 |

At the old range the track sat 14-20 dB under the clip: SBR +12.8 to +16.8 dB means it was background texture, and ducking it moved the mix by **0.04 dB**. At 0 dB the track is *louder* than the dialogue and ducking only just claws it back to +1.0.

**-8..-5 dB is the band where the track is unmistakably present and the dialogue keeps a 6-8 dB margin over it once ducked.** That is what shipped.

**The audibility criterion is a judgement, not a measurement**: ~1 dB is the textbook just-detectable broadband level change, ~3 dB clearly audible. I cannot listen. The three renders are the deliverable that tests it.

---

## Part 3 — CORRECTION: the duck depth I reported last round

MEMEBOT-009 reported **-8.50 dB** duck depth. That bench took real clips and mixed Windows SAPI speech into them at **+6 dB over each clip's own bed** — a large, clean key excursion. Real dialogue does not look like that.

**VERIFIED**, 4 real dialogue-over-music clips, the labeller's VAD spans, bed at -6 dB:

| threshold reference | offset | duck depth | headroom | pumping |
|---|---|---|---|---|
| clip mean | +3 dB | -0.57 dB | -0.56 dB | 0.87 dB |
| **clip mean** | **0 (shipped)** | **-1.12** | **-1.57** | **1.66** |
| clip mean | -3 | -1.75 | -3.18 | 2.51 |
| clip mean | -6 | -2.23 | -5.41 | 3.06 |
| clip mean | -12 | -2.64 | -10.62 | 3.70 |
| between-words bed | 0 | -1.82 | -3.21 | 2.58 |
| between-words bed | -6 | -2.51 | -8.00 | 3.54 |

**Why it caps out.** `sidechaincompress` only reduces gain above the threshold, so the differential can never exceed the key's own speech-vs-bed excursion times (1 − 1/ratio). Measured across the 12 real dialogue clips, that excursion has a **median of +2.9 dB** and a range of **-1.4 to +8.9 dB**. The music between words is nearly as loud as the words. **-2.5 dB is close to the physical ceiling on this material**, and no parameter choice moves it.

Keying the threshold off `clip_speech`'s between-words `bed_dbfs` instead of the clip mean was tested and is **equivalent at matched headroom** (bed+0 gives -1.82/-3.21 against mean-3's -1.75/-3.18). It needs an extra input for no gain, so **the shipped rule stays the clip mean at offset 0** — which is also the knee of the curve.

### Pumping, as instruction 5 requires

At the shipped setting, **pumping std is 1.66 dB against a duck depth of 1.12 dB.** The bed wobbles *more* from the music than it dips for speech. That ratio holds everywhere tested — pumping runs about 1.4× the depth at every offset — so there is no setting on this material that ducks cleanly. MEMEBOT-006 judged pumping by ear on a 440 Hz sine, which has no beat to pump against; MEMEBOT-009 measured 2.31 dB on injected speech. On real dialogue it is worse relative to what it buys.

---

## Part 4 — Routing, and the boundary MEMEBOT-015 found

**`mode: auto` used to gate on source loudness** — a bed only when the source measured quieter than -32 dB. 60 of the 61 local clips sit above that line, and a clip quiet enough to pass it has nothing worth ducking against. The duck path could not fire in the configuration that ships.

Source loudness also answers the wrong question — "is there anything here", not "is anyone talking" — and BL-742 measured that exact substitution at a **63.3% false-negative rate**. So `auto` now routes on the class. All four classes want a track (two take one *instead of* their audio, two *under* it), so auto always lays one and the class picks treatment and level. `never` is still how you say no.

**The boundary.** `clip_speech.treatment_for()` answers `"mute-and-replace"` / `"duck-under"`; `duck.py` speaks `"mute"` / `"duck"`. The words never matched, and `resolve_treatment` took an unknown word, fell back to its **default**, and returned a reason nobody raised on — so the render succeeded and **the treatment silently became mute on every clip**. All 3 clips of MEMEBOT-015's first live run reported exactly that.

Closed from this side, in three parts:
- the aliases are accepted, so the vocabulary matches;
- an unrecognised word now prints to stderr and is logged, rather than being absorbed;
- the fallback is **duck**, not the default. Ducking a music clip wastes CPU; muting a dialogue clip destroys the dialogue. Only one of those is recoverable.

A test asserts `duck.py` and `clip_speech.treatment_for()` agree class for class, so they cannot drift apart again silently.

---

## Part 5 — Three renders, one per class

**THIS IS THE DELIVERABLE.** Every number above was produced by an agent that cannot listen.

| class | source | treatment | bed level | output |
|---|---|---|---|---|
| **music-only** | `DVJ6-J0kmVy` (real) | **mute** | solo, -12.8 dB gain | -28.8 dBFS, peak -14.9 |
| **dialogue-over-music** | `DXd8PrcDuHl` (real) | **duck** | -6.6 dB under the **voice** (-12.8 dBFS) | -17.3 dBFS, peak -1.3 |
| **dialogue-only** | **constructed** | **duck** | -5.1 dB under the voice (-25.0 dBFS) | -31.5 dBFS, peak -9.8 |

Each render reports its own routing, e.g.:

```
ambient_bed  song.mp3 @ -19.4dB [relative (speech level -12.8dB -6.6dB)] (auto: class dialogue-over-music -> add)
audio_treat  duck (routed on class dialogue-over-music), threshold 0.15849 @ +0.0 dB vs source
```

**The dialogue-only clip is CONSTRUCTED and labelled as such everywhere**, because the corpus has none. It is a real clip's video with speech-and-silence audio, and `clip_speech` was asked to confirm before it was used: `dialogue-only, speech_frac 0.444, bed -180.0 dBFS`.

The "new song" is a real music-only clip's audio (`DI8-v0YtJ0V`, 66.6 s). `scraper/sounds/ambient/` still ships only a README, so there is no real track to use. Nothing here is published.

### Two defects the renders caught, both fixed

1. **Music-only routed to the wrong config range.** The class said solo, my mapping turned that into `"absolute"`, which reads `volume_db_min/max` (-38..-28) rather than `solo_volume_db_min/max` (-14..-6). The first render came out **muted with a -44.2 dB track** — inaudible, the same shape as the -49 dB deliverable MEMEBOT-007 hit and MEMEBOT-011 fixed. Caught only because the render was measured.
2. **The relative offset was measured against a mean that silence drags down.** A dialogue-only clip measures -28.5 dBFS overall because most of it is silence between lines, so a -7 dB offset put the track at **-48.9 dBFS** — below the -45 dBFS line `clip_speech` uses to decide a bed is even *there*. The track was inaudible on the class that most needs to hear it, and nothing failed: the level was arithmetically correct against a reference that meant nothing. A relative offset means "this far under the **voice**", so `--speech-dbfs` now supplies the speech level and `relative_basis()` prefers it, saying so in the log when it has to fall back.

---

## Outstanding, with the number

**The solo level is a GAIN, not a target.** `solo_volume_db_min/max` (-14..-6) is applied to whatever track is supplied, so the output level depends entirely on the track's own loudness. With this track (mean ~-15 dBFS) the muted render landed at **-28.8 dBFS, 12 dB below the source clip it replaced**. For a clip whose entire soundtrack is now the track, that is quiet. The fix is to loudness-normalise the track once (`loudnorm`) rather than to widen the range, but that is a change to how tracks are prepared and it was not this round's scope. **Measured and left open.**

---

## Concurrency

`MEMEBOT-016` held `edit.py` and `config.yaml` throughout, having declared it touches only drawtext, video scale/pad and `frame_noise` — never the audio graph. I touched only the ambient decision layer and the `ambient_bed` block. Both sets of edits are present and intact. Note that `claim.py` reported **no conflict**, because MEMEBOT-016 passed its paths as one comma-joined string to a single `--write`; the detector compares whole strings. Worth knowing before trusting a clean claim report.

Two of my own background jobs also overlapped and one's cleanup deleted the other's render output mid-run. Re-run serially; the files in this report are from a single clean pass.

---

## Honest limits

- **I cannot listen.** Every conclusion here is a measurement. The three renders exist so someone with ears can check whether each treatment suits its class — that is the whole point of Part 5, and it is the one claim I cannot make myself.
- **No dialogue-only clip exists locally.** 0 of 61, nothing within 22 dB of the boundary. That render is constructed and says so; the class's real behaviour on real material is **unmeasured**.
- **Dialogue measurements come from 3-4 clips**, all dialogue-over-music, all from a 61-clip corpus that is 80% music-only and does not match the library's distribution.
- **The audibility thresholds (~1 dB detectable, ~3 dB clear) are textbook figures**, not something verified by ear here.
- **The duck is marginal on real material and I am not going to dress that up.** -1.12 dB of depth against 1.66 dB of music-driven wobble. It buys about 2.2 dB of speech-to-bed ratio, which is worth having, but the bed level change is what actually made the track audible.
- **`verify_claims.py` cannot verify this round.** `.gitignore:137` ignores `memebot/` entirely, so every claim reads "not committed at HEAD" and always will. Verified by the 72 tests instead. Same hole MEMEBOT-009 recorded.

---

## Say it plainly

The duck path can now fire, which it could not before, and the track is now audible, which it was not before. Both of those are real. But the honest headline is that ducking buys about two decibels on this material and the bed level buys eight, so the thing worth getting right was the level — and it was being decided in a different function from the treatment, by a rule that answered the wrong question. Two of the three numbers I shipped last round did not survive contact with real dialogue, and both were inflated by a bench that injected its own speech.

<!-- CLAIMS
file:   memebot/scraper/duck.py
file:   memebot/scraper/tests/test_duck.py
func:   memebot/scraper/duck.py::bed_plan
func:   memebot/scraper/duck.py::relative_basis
func:   memebot/scraper/duck.py::normalise_treatment
func:   memebot/scraper/duck.py::resolve_treatment
const:  memebot/scraper/duck.py::TREATMENT_BY_CLASS
const:  memebot/scraper/duck.py::TREATMENT_ALIASES
const:  memebot/scraper/duck.py::BED_PLAN_BY_CLASS
const:  memebot/scraper/duck.py::BED_OFFSET_DIALOGUE_DB
const:  memebot/scraper/duck.py::FALLBACK_TREATMENT
file:   memebot/scraper/edit.py
file:   memebot/scraper/config.yaml
-->
