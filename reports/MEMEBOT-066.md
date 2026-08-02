# MEMEBOT-066 — the class was not missing; the guess behind it was

**Brief:** find why `audio_class` is None at render time, make a missing class refuse rather
than guess, and prove 10 rendered videos carry the configured track.

**Result:** `audio_class` is **not** None at render time any more, and BL-950's diagnosis no
longer reproduces. What is still live is the second half of the brief — a missing class was
guessed as `keep`, and that guess is now a refusal. 10 of 10 freshly rendered videos carry
their configured track, measured against a null of every other track in the store.

---

## 1. Where the class actually died, and why it is no longer dying there

BL-950 reported `audio_class: None` on 14 of 14 and concluded the value was being dropped
between the record and the renderer. I could not reproduce that, so I measured every link.

| Link | Measured | Verdict |
|---|---|---|
| Raw library shards carry the field | 2,190 of 6,503 lines have the key; 2,094 populated | present |
| `read_all` last-wins view | **1,852 of 2,003 clips (92.5%)** carry a class | present |
| `clip_pipeline._f(clip, "audio_class")` | returns it on all 1,852 | reads fine |
| `audio_treatment(clip)` | `"stored class (measured)"` | routes |
| `render_one` argv | `--audio-class` present on 10 of 10 | wired |
| `edit.py` → `duck.resolve_treatment` | `routed on class …` in the edit log | acts |

**The class died at the WRITE, not the read.** MEMEBOT-035 found it: `make_speech_fn`
computed all four values and returned only `speech_frac`, so `audio_class` read 0% populated
for four rounds while everyone assumed the labelling pass had not been run. It had been run.

**BL-950 audited a batch that predates the fix landing.** The ledger dates it exactly:

```
19:56 UTC 2026-08-01   audio_class=None   "class UNKNOWN -- defaulting to keep"    <- BL-950's batch
22:15 UTC 2026-08-01   audio_class set    "stored class (measured)"                <- and every batch since
08:43 UTC 2026-08-02   audio_class set    "stored class (measured)"
```

Of 95 ledger rows recording `None`, **93 name a clip whose library row carries the class
today**. Those rows are a photograph of the old bug, not evidence of a current one. This is
worth stating plainly because acting on the brief's stated cause would have meant "fixing" a
read path that already works.

Two things I did find, both real and both smaller than reported:

- **89 clips lose a populated class to a rev collision** — two writers holding the same
  snapshot, `read_all` breaking ties last-in-file-order. `append_many`'s merge-under-lock
  (BL-919) fixed the mechanism; these 89 are residue from before it, recoverable by
  re-reading the shard rather than the view. 4.4% of the library, not 100%.
- **151 clips (7.5%) genuinely have no class.** These are the ones the rest of this report
  is about.

## 2. The guess is gone

With no class, `duck.resolve_treatment` returned `FALLBACK_TREATMENT` (`keep`) plus a loud
warning. Every other branch of that function is a decision — an operator typed a word, a
config named one, the labeller measured a class. This one was a guess, and it lost both ways:

- guess `keep` on **music-only** — the majority class at ~51.9% (BL-853) / 80.3% (MEMEBOT-020)
  — and the original copyrighted song survives under the new one;
- guess `keep` on a **DASH rendition**, which carries no audio stream at all, and there is
  nothing to keep, so the file is silent.

Both produce a healthy-looking mp4 at returncode 0. The warning had been in place for three
rounds and did not prevent BL-950, and the reason is structural rather than careless:
`clip_pipeline.render_one` judges `returncode == 0` and nothing else, so stderr could say
anything at all.

So the fallback is now `duck.AudioClassRequired`, modelled on the `AmbientBedMissing` refusal
already in `edit.py`. Measured end-to-end on a real render:

```
WITHOUT --audio-class    returncode=1    output file: NOT created
   RESULT edit: rendered=0 skipped=0 errors=1 status=failed
WITH    --audio-class    returncode=0    output file: created
   RESULT edit: rendered=1 skipped=0 errors=0 status=ok
```

The refusal fires **only where the treatment would have been guessed**. `--treatment`, a
fixed word in config, and a measured class all still win outright, and
`ambient_bed.require_audio_class: false` restores the old behaviour deliberately for anyone
who wants it. It also fires *before* the no-source-audio branch can quietly rewrite the guess
into a mute — that branch is what made the DASH case look survivable.

## 3. Ten videos, and how "the song is present" was decided

BL-950's `|r| <= 0.06` finding was not reproducible: the report records the number and not
the method. So the method is written down in `scratch/mb066_corr.py` and validated before use.

- **Feature:** log-RMS envelope, 40 ms window / 20 ms hop, z-scored. A bed is mixed under the
  source, resampled, re-encoded to AAC and attenuated; sample-aligned waveform correlation
  survives none of that, the loudness contour survives all of it.
- **Band: 40–250 Hz.** A music bed puts its bass and kick there and dialogue puts almost
  nothing (`duck.py` band-limits its own key to 300–3400 Hz for the complementary reason).
  This mattered: broadband, one dialogue clip scored 0.26 against its configured track and
  0.28 against a competitor — undecidable. Band-limited, the same file scored **0.36 against
  ≤0.10 for all four competitors**. A measurement change, not a threshold change.
- **Lag search:** the track is tiled across the video and the best lag over a full window
  length is taken, because `aloop` phase is not knowable from the record.
- **Statistic: max *signed* Pearson.** The first version maximised `|r|` and scored one video
  "present" on r = −0.45. Anti-correlation is not weak evidence of presence.
- **Null:** every other track in the store, on the identical code path. A bare r of 0.3
  proves nothing on its own; two arbitrary pieces of music share broad structure.
- **Bar:** r ≥ 0.25 **and** margin over the best competitor ≥ 0.10.

Validated on four controls before being pointed at any render — **4/4 correct**: the track
alone (0.96), the track 12 dB under pink noise (0.83), the wrong track (rejected, and the
null correctly identified the right one at 0.9997), and a file with no audio stream.

### The result

| clip | class | r | best other | margin | verdict |
|---|---|---|---|---|---|
| 3923023365239161294 | dialogue-over-music | +0.957 | +0.229 | +0.728 | present |
| 3898520032929759070 | music-only | +0.987 | +0.206 | +0.781 | present |
| 3676715116732298613 | dialogue-over-music | +0.681 | +0.167 | +0.514 | present |
| 3875222167844207093 | dialogue-over-music | +0.690 | +0.349 | +0.341 | present |
| 3915146003363721805 | dialogue-over-music | +0.365 | +0.100 | +0.265 | present |
| 3817080192548982238 | dialogue-over-music | +0.474 | +0.241 | +0.233 | present |
| 3711445528099092854 | music-only | +0.977 | +0.278 | +0.699 | present |
| 3921750279025853869 | dialogue-over-music | +0.682 | +0.445 | +0.237 | present |
| 3716465589432016475 | dialogue-over-music | +0.425 | +0.244 | +0.181 | present |
| 3940318810397427210 | music-only | +0.951 | +0.338 | +0.613 | present |

**10 of 10.** Every one clears BL-950's own `|r| <= 0.06` unrelated bar by at least 6×, and
every one beats its nearest competing track by ≥ 0.18.

A second, independent check ran alongside: each clip was rendered **twice**, once with the bed
and once with it disabled. On the music-only clips the no-bed twin has **no audio stream at
all** — the DASH source carries none — so 100% of the rendered audio is the bed, which is as
direct as attribution gets. On the dialogue clips the twin is audible and the bed adds 2.5 dB.

**Honest limit of the paired control:** `edit.py` builds its RNG as `random.Random()` with
fresh entropy per call and exposes no seed, so the twin is *not* the same timeline as the
main render. It is therefore a valid per-clip null (this clip's audio against this track) but
**not** a subtractable baseline, and I have not treated it as one. The attribution above rests
on the band-limited correlation and its null, not on the twin.

## 4. What is not fixed, and why

**`build_render_config` disables the bed when no song file resolves, and a DASH source then
renders silent at returncode 0.** This is the *other* half of BL-950 — the 12 files with no
audio stream, whose ledger rows read `song: "."`. It is a genuine silent-success path and it
is still open.

Measured today it is **unreachable in practice**: 0 of 400 clips fail to resolve a bed file
(91.5% land on `lru_corpus`, 8.5% on `matched`). It is a latent branch, not a live leak.

I did not fix it because `clippershq/clip_pipeline.py` is claimed by **BL-958** (active) and
**BL-899**. `memebot/scraper/edit.py` is claimed by **MEMEBOT-064** (active). I was read-only
on both; the refusal went into `memebot/scraper/duck.py`, which was free and is where the
guess actually resolved, and needed no change to either held file. The suggested patch for
whoever holds `clip_pipeline.py` next: `build_render_config` should refuse rather than
disable when `song["tier"]` is not `none` but the file does not resolve — a named track that
cannot be found is the same class of failure `AmbientBedMissing` already refuses one layer down.

## 5. Guards

`tests/test_audio_class_reaches_render.py` (11 checks). `tests/test_render_argv.py` already
pinned the argv and was green throughout BL-950 — it was also irrelevant, because the value
being written was `None`. An argv guard on a structurally-always-None value passes forever.
These cover the **read path** and the **fill rate** instead:

- the class survives the read, flat and provenance-wrapped;
- an absent class is reported absent, never invented (tri-state);
- `clip_speech` and `duck`'s treatment tables still agree, class by class;
- **`audio_class` is populated on > 50% of live library rows** — the guard that was missing
  when it read 0% for four rounds. Floor set far below the measured 92.5% deliberately: this
  catches the 0% regression, it is not a quality bar.

Both regressions were planted to confirm the suite catches them:

| planted bug | failures |
|---|---|
| class never persists (`audio_treatment` → None) | **6** |
| missing class guesses `keep` (pre-MEMEBOT-066) | **2** |
| restored | **0** |

`memebot/scraper/tests/test_duck.py` gained the refusal contract and lost two assertions that
encoded the old fallback — the previous text of `test_no_class_at_all_is_conservative` is
exactly the behaviour BL-950 measured as 0/25. `None` also moved out of
`test_routing_only_ever_picks_a_shipped_treatment`'s loop and is asserted separately; keeping
it in would have meant relaxing that assertion to "shipped treatment OR raises", which is how
a guard gets weakened by a test that was only ever about something else.

**Suites: parent 126/126, 4,492 checks. memebot/scraper 178/178.** Both green.

## 6. Cost

$0.00. No paid calls — every render reused clips already staged on disk by earlier rounds, so
only the free half of `run_batch` (stage → song → config → render) was exercised.
