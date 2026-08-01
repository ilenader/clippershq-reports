# MEMEBOT-035 — `speech_dbfs` persists, and it was never alone. **Three of four measurements were being discarded**, `audio_class` among them — which is why it has read 0% populated since MEMEBOT-015. The bed moves **6.9 dB** on a real dialogue clip.

**Date:** 2026-08-01 · **Type:** Fix + measurement · **Spend:** **$0.00** (61 local clips, injected fetcher, no network)
**Changed:** `clippershq/clip_speech.py`, `clippershq/clip_runner.py`, `clippershq/clip_library.py`, `tests/test_clip_speech.py`.
**`clippershq/clip_pipeline.py`: NOT TOUCHED** — MEMEBOT-030's wiring was already right.

---

## The brief was right and the problem was three times bigger

`clip_speech.analyse()` returns **four** values from one VAD pass. `make_speech_fn` returned
the float and nothing else, and `on_measure` was wired in `control.py` to an in-memory dict
that lives for one run and never reaches a clip record. So:

| value | what it decides | state before |
|---|---|---|
| `speech_frac` | the format label | stored |
| **`audio_class`** | the audio **treatment** and the bed **plan** | **computed, discarded, undeclared** |
| **`speech_dbfs`** | the level a dialogue bed sits under | **computed, discarded, undeclared** |
| **`bed_dbfs`** | separates dialogue-over-music from dialogue-only | **computed, discarded, undeclared** |

**Two failures were hiding each other.** Each was undeclared in `CLIP_FIELDS` *and* never
written, and nobody goes looking for a missing declaration on a key that is never on disk.
BL-847 caught the declared-half of this trap for `speech_frac`; this is the other half.

**`audio_class` has read 0% populated since MEMEBOT-015 and that was taken as evidence the
speech pass had not run.** It ran. `clip_pipeline.audio_treatment()`'s `"stored class
(measured)"` branch has never once fired — every clip fell through to the free declared
signal, which only `licensed_music` answers.

Storing all three is one payload down one code path, so the brief's `speech_dbfs` arrives
with the other two rather than instead of them.

## 1. The fix keeps the float contract

`speech_fn(media) -> float|None` is what `clip_runner` injects and expects. Changing that
return type is exactly the boundary change that caused this family of bugs, so it is
untouched. The function now additionally carries `speech_fn.detail(clip_id) -> dict|None`,
reading a record it already built:

```python
detail = getattr(speech_fn, "detail", None)      # attribute, not a second injection
if callable(detail):
    rec = detail(clip_id) or {}
    audio_class, speech_dbfs, bed_dbfs = (
        rec.get("audio_class"), rec.get("speech_dbfs"), rec.get("bed_dbfs"))
```

Read defensively so a `speech_fn` that predates it — every existing test's stub — still
works and simply yields nothing extra. **Nothing is re-measured and no call is made**: the
analysis already happened, and the values were being thrown away one function call from
where they were wanted.

One thing fixed along the way: the four *no-measurement* paths (no audio URL, fetch failed,
undecodable, `licensed_music`) previously reported only to `on_measure`, so they left no
durable trace at all. They now go through the same `_record()` fan-out, because **"never
measured" and "measured as absent" are different facts and a fill rate has to tell them
apart.**

## 2. Declared, with a tier

```
speech_frac   declared=True  field()=0.295                  tier=measured
audio_class   declared=True  field()='dialogue-over-music'  tier=measured
speech_dbfs   declared=True  field()=-13.5                  tier=measured
bed_dbfs      declared=True  field()=-17.2                  tier=measured
```

All four **MEASURED** — a detector was run over the media itself. None is declared by the
platform, none is derived from another field. The trap, demonstrated on a record that
really carries the value:

```
rec['bed_dbfs']          = -17.2   <- on the record
field(rec,'bed_dbfs')    = -17.2   <- readable because it is DECLARED
field(rec,'not_a_field') = None    <- undeclared: None regardless
```

### Fill rate, 61 real clips, the real VAD

`make_speech_fn` takes an injected `http_get`, so a fetcher reading the already-downloaded
clips off disk exercises the **real** pass — real silero VAD, real `analyse()`, real record
path — at zero spend and with no network.

| field | fill | before |
|---|---:|---|
| `speech_frac` | 61/61 **100.0%** | stored |
| `audio_class` | 61/61 **100.0%** | **0.0%** |
| `bed_dbfs` | 61/61 **100.0%** | **0.0%** |
| `speech_dbfs` | 35/61 **57.4%** | **0.0%** |

**`speech_dbfs` is 57.4% and that is the correct number, not a gap.** It is None where the
VAD found no speech at all, which is most music-only clips. On the clips that *use* it:

```
dialogue classes : 12/12 = 100.0%
music-only       : 23/49 =  46.9%   (None where nobody speaks)
```

And the label that read 0% for twenty rounds, finally readable:

```
music-only            49  (80.3%)
dialogue-over-music   12  (19.7%)
speech_dbfs range: -27.3 to -9.9 dBFS (median -13.5)
```

## 3. It reaches the renderer

MEMEBOT-030's argv guard is **satisfied unchanged** — `speech_dbfs` was already in its
`WIRED` registry, and `clip_pipeline.py` needed **zero edits**. The value went from "always
None" to real purely by being stored and declared. That is what a correctly-wired boundary
looks like when the thing behind it finally exists.

## 4. The difference it makes: **6.9 dB**

One dialogue-over-music clip, rendered twice through `render_one()`, with the offset pinned
at −6.0 dB so the runs differ **only** in the basis:

```
FALLBACK  --speech-dbfs in argv: False
  song01.mp3 @ -8.4dB [relative (clip mean (no speech level given; on a quiet-gapped clip
  this under-places the track) -17.9dB -6.0dB -> bed at -23.9dBFS)]

MEASURED  --speech-dbfs in argv: True
  song01.mp3 @ -1.5dB [relative (speech level -11.0dB -6.0dB -> bed at -17.0dBFS)]
```

| run | basis | bed target | gain |
|---|---|---:|---:|
| fallback | clip mean −17.9 dB | −23.9 dBFS | −8.4 dB |
| measured | **speech level −11.0 dB** | **−17.0 dBFS** | −1.5 dB |

**+6.9 dB.** Not under a decibel — the clip mean sits 6.9 dB below the voice because the
clip's own silences drag it down, and the bed inherits that error one-for-one. That is
`duck.relative_basis`'s documented warning, now measured on a real render instead of
predicted: MEMEBOT-021 chose −8..−5 dB under the *voice*, and the fallback was delivering
roughly −15 dB under it.

Worth stating plainly: this is one clip. The size of the error is the gap between a clip's
mean and its speech level, which varies with how much silence it carries. A wall-to-wall
dialogue clip would show almost none.

## 5. `dialogue-only` is still unmeasured

**The corpus has no dialogue-only clip** — 0 of 61 here, and this round's pass confirms it
again with `audio_class` finally readable. Its routing, its bed plan and its `speech_dbfs`
handling are all exercised by tests and by constructed sources only. **Every render of that
class in this project, including MEMEBOT-030's third video, is constructed**, and no claim
about how it behaves on real material has been earned.

---

## Verification

| check | result |
|---|---|
| `tests/test_clip_speech.py` | **55/55 OK** (6 new) |
| `tests/test_clip_library.py` | **41/41 OK** |
| `tests/test_render_argv.py` | **7/7 OK** — guard satisfied, unchanged |
| `tests/run_all.py` | **88 of 89 suites green**; the 1 red is another round's stale manifest — see below |
| all four declared + readable + `measured` | proved on a built record |
| fill rate | `audio_class` 0 → **100%**, `bed_dbfs` 0 → **100%**, `speech_dbfs` 0 → **100% of dialogue clips** |
| bed level, fallback vs measured | **+6.9 dB** |
| `clip_pipeline.py` | **not modified** |
| **campaigns SHA** | **`8e02f8d6f6307ae8` — MATCH** |
| `config.json` | parses, 162 keys |
| spend | **$0.00**, no network |

### The one red suite is not this round's

`tests/test_claims_manifest.py` fails on:

```
docs/claims/MEMEBOT-022.claims claims that no longer hold:
  const clippershq/song_library.py::TIER_TITLE: no assignment to TIER_TITLE at HEAD
```

**MEMEBOT-032 deleted that constant** — `song_library.py:91` says so in as many words —
and did not update MEMEBOT-022's finished-work manifest, which still asserts it exists.
I touched none of those files. It is a real failure and somebody should fix it; it is
not mine to fix, and I am reporting the batch number rather than excluding it.

## Concurrency

Claim filed with **repeated `--write` flags**, verified by hand: 5 entries, no commas in
any. The advisory fired on both contended paths.

- **BL-849** holds `clip_library.py` (243 min, the vision labelling pass). I added field
  declarations and three `put()` lines under a hash guard, re-checked immediately before
  writing (`0c139e69b35405bf`, unmoved). Not overwritten.
- **BL-855** holds `clip_pipeline.py` (188 min). **I did not touch it** — the prediction in
  my claim held, so the contended file stayed untouched entirely.
- `clip_speech.py` and `clip_runner.py` were free.

One false alarm worth recording: the editor warned `clip_speech.py` had been "modified on
disk since you last read it". It had not been touched by anyone else — the warning was
stale context from an earlier session's read. **Verified with a hash against my own
baseline and a `git diff` showing only my change before continuing**, which is the check
that distinguishes a real concurrent writer from a stale one.

## Limits

- **Fill rate is measured on the 61 local downloads, not the library.** Existing clip
  records were written before this change and still carry none of the three. **Nothing here
  backfills them** — a migration would have to re-run the VAD over stored media, and
  `clip_library/` has live writers (BL-849/BL-872) so this was not the round to attempt it.
- **The 6.9 dB is one clip.** The error equals a clip's mean-to-speech gap and varies with
  its silence.
- **`speech_dbfs` on music-only clips is 46.9% and meaningless where present** — it is the
  level of whatever brief VAD span fired below the speech threshold, not a voice.
- **`_detail` grows for the life of the pass.** One dict entry per clip; at library scale
  (thousands) that is small but unbounded, and it is not evicted.
- **The class distribution is this corpus's, not the library's**: 80.3% music-only here
  against BL-853's ~51.9% library-wide.
- **`dialogue-only` remains unmeasured on real material.** See item 5.

## Method

Claimed with one `--write` per path and verified the stored list. Both contended files were
hash-baselined and re-checked before writing; one needed no edit at all. The fill rate and
the class distribution come from running the real `make_speech_fn` with a fetcher that
reads local files, so the pass is genuine and the spend is zero. The bed difference was
measured by rendering the same clip twice through `render_one()` with the offset pinned, so
the only variable is the basis. No paid call, no key read, no network.
