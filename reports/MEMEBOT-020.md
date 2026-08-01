# MEMEBOT-020 — The duck depth is **3.57 dB mean, 2.57 dB median**, and **7 of 11 clips are under the 4 dB audibility bar**. Tuning cannot fix it: the dip is **bounded by the source's own speech-to-bed contrast (r = 0.920)**, and no setting in a 23-point sweep beat it.

**Date:** 2026-08-01 · **Type:** Measurement · **Spend:** **$0.00** (61 already-downloaded clips, no paid calls)
**Wrote:** `scratch/mb020_*.py`, `scratch/mb020/` only. **`memebot/` was not modified** — MEMEBOT-021 holds `duck.py` and its brief overlaps this one, so every tuning result below is *reported* for it to adopt, not written.

---

## The answer, first

| | measured |
|---|---:|
| gain reduction **while someone is talking** | **5.77 dB** mean |
| gain reduction **while nobody is** (the permanent cost) | **2.19 dB** mean |
| **the dip a listener actually hears** | **3.57 dB** mean · **2.57 dB** median · **−0.28 dB** worst |
| clips under the brief's ~4 dB bar | **7 of 11** |
| clips under 2 dB | **5 of 11** |
| clips where the duck runs **backwards** | **1 of 11** |

**It lands between MEMEBOT-006's two poles and reaches neither.** It is not the −0.4 dB
no-op MEMEBOT-006 predicted for the ffmpeg defaults, and it is not the −8.5 dB duck.py's
own table advertises. On the shipped default the treatment is **marginal on the median
clip and inaudible on the majority.**

### Why duck.py's table says −8.50 and this says 3.57

Both are right; they measure different things. duck.py reports *gain reduction during
speech* (−8.50) and *permanent headroom* (−4.60) as two separate columns and **never
subtracts them**. The music underneath the dialogue holds the compressor open when nobody
is talking, so a permanent floor is already applied — and a listener hears only the
**difference**. duck.py's own numbers imply a dip of `8.50 − 4.60 = 3.90 dB`, within
0.4 dB of what I measure independently. **The number was sitting in the table for two
rounds as a subtraction nobody performed.**

---

## Method — and why the obvious measurement returns nothing

The production graph mixes the ducked bed **with** the source. Measuring that tells you
nothing about ducking: the source dominates the sum, so the mix gets *louder* exactly
where the bed dips. MEMEBOT-018 measured that gap at 0.3 dB and correctly called it
inconclusive.

So this taps the bed leg. It takes `duck.build_audio_graph`'s real DUCK graph and replaces
**only** the final `amix` with a passthrough of `[a1d]`, leaving the bed chain, the key
chain and the `sidechaincompress` string byte-identical to production. Two renders per
setting — compressor on, compressor removed — driven from identical inputs, so they are
sample-aligned and

```
GR(t) = unducked_dB(t) − ducked_dB(t)
```

is the compressor's gain reduction directly, frame by frame at 10 ms. Every number here is
read off that curve.

**Two controls, because a measurement rig that flatters itself is worse than none:**

| control | expected | measured |
|---|---|---|
| `ratio = 1.0` (compression bypassed) → GR must vanish | 0.00 | **0.00 / 0.00 / 0.00** |
| GR must not depend on the bed's **volume** (the key is the source) | 0 | **0.01 dB** across a 34.9 dB bed-gain change |

The bypass control is the one that matters: if it were not 0.00, the tap would be
measuring something other than the compressor and every figure in this report would be
noise.

---

## 1. The test source — silencedetect picked the wrong clip

`silencedetect` over all 61 downloads: **only 4 of 61 (6.6%) have any gap ≥ 0.3 s below
−35 dB.** That reproduces MEMEBOT-006's 95.5%-no-gaps almost exactly (93.4% here).

But its top pick was wrong. `DaFNBnoo8Hr.mp4` has the most gaps (7, 30.7% quiet) and the
**VAD classifies it music-only** — those are musical rests, not speech pauses. Ducking
against it would have measured a drum machine.

So the windows come from the **silero VAD in `clip_speech.py`** — the same one BL-848
used, run locally and free:

| class | n | share | treatment |
|---|---:|---:|---|
| music-only | 49 | **80.3%** | mute-and-replace |
| dialogue-over-music | 12 | **19.7%** | duck-under |
| dialogue-only | **0** | **0.0%** | — |

**This corpus is not the one the brief describes.** BL-848's ~43% / ~9% does not hold on
these 61 downloads: dialogue-over-music is **19.7%**, and there is **no dialogue-only clip
at all**. That last point is load-bearing for item 5 — every duckable clip here has music
under the speech, which is precisely the condition that holds the sidechain open.

Primary source **`DYctewoBTxB.mp4`** — 18.6 s, speech_frac 0.217, speech −11.0 dB over a
−18.5 dB bed, VAD spans `11.00–13.92` and `17.18–18.28`, giving 11 uninterrupted seconds
of non-speech before a single clean onset.

---

## 2 + 3. The depth, and the ceiling that no setting clears

Per clip, at the shipped default (offset 0 dB, ratio 20, attack 20 ms, release 400 ms):

| clip | contrast | GR speech | GR quiet | **DIP** |
|---|---:|---:|---:|---:|
| DUAaRozCWYc | 11.6 | 10.32 | 0.59 | **9.73** |
| DYctewoBTxB | 7.5 | 9.37 | 1.76 | **7.62** |
| Da3KdBYksJA | 9.7 | 5.15 | 0.08 | **5.07** |
| DbY81MbOIAT | 6.8 | 5.04 | 0.42 | **4.61** |
| DINgqplRV3c | 3.7 | 5.89 | 3.05 | **2.84** |
| DXd8PrcDuHl | 5.2 | 4.45 | 1.87 | **2.57** |
| Da0UT_fvF0D | 4.4 | 4.84 | 2.87 | **1.97** |
| DJZAh-NRC_E | 3.4 | 4.79 | 2.87 | **1.92** |
| DQozMHQCevx | 2.9 | 5.05 | 3.21 | **1.84** |
| DXdczT4gFMI | 1.7 | 5.10 | 3.69 | **1.41** |
| DQZSDZWiYSQ | **−0.5** | 3.43 | 3.71 | **−0.28** |

`contrast` is the VAD's own `speech_dbfs − bed_dbfs` — a property of the **source**, not of
any setting. Read the last two columns together.

**23 settings swept.** DIP = GR_speech − GR_quiet, mean over 3 clips:

| setting | GR speech | GR quiet | **DIP** | worst |
|---|---:|---:|---:|---:|
| offset +6 dB | 1.64 | 0.03 | 1.61 | 0.54 |
| offset +3 dB | 3.61 | 0.63 | 2.99 | 1.29 |
| **offset 0 dB — shipped** | 6.22 | 2.17 | **4.05** | 1.97 |
| offset −3 dB | 9.07 | 4.62 | 4.45 | 2.12 |
| offset −6 dB | 11.92 | 7.40 | 4.52 | 2.12 |
| ratio 2 | 3.28 | 1.11 | 2.16 | 1.04 |
| ratio 10 | 5.89 | 1.99 | 3.90 | 1.87 |
| **attack 5 ms** | 7.74 | 3.23 | **4.52** | **2.10** |
| attack 100 ms | 3.94 | 0.93 | 3.01 | 1.27 |
| release 100 ms | 3.56 | 0.73 | 2.83 | 1.02 |
| release 800 ms | 7.79 | 3.57 | 4.23 | 1.69 |
| **ffmpeg defaults untuned** | 3.21 | 1.11 | **2.10** | 0.85 |

**Nothing reaches 4 dB worst-case.** Driving the threshold down to −6 dB buys 0.47 dB of
extra dip and costs **5.2 dB more permanent headroom**. Driving it *up*, which I expected to
help by keeping the bed out of the key, collapses the duck entirely (+6 dB → dip 1.61;
+12 dB → 0.10). **My hypothesis going in was wrong and the sweep says so.**

### Why — the ceiling is arithmetic, not a tuning failure

At ratio 20 `sidechaincompress` is close to a limiter: whenever the key is over the
threshold the output sits near the threshold, so `GR(t) ≈ key(t) − threshold`, and in the
dip **the threshold cancels**:

```
DIP = GR(speech) − GR(quiet) ≈ key(speech) − key(quiet)
```

The dip is therefore bounded by the source's own speech-to-bed contrast, and no threshold,
ratio, attack or release can exceed it. Tested on all 11 clips:

```
correlation dip vs contrast     r = 0.920
fit                             dip = 0.77 × contrast − 0.36
clips whose dip exceeds their
  own contrast by > 0.5 dB      0 of 11        <- the ceiling holds
```

`DQZSDZWiYSQ` is the proof by contradiction: its speech sits **0.5 dB below** its own bed,
so the compressor ducks *harder in the gaps than under the voice* and the dip is
**−0.28 dB — the treatment runs backwards.** No parameter can fix a clip whose dialogue is
quieter than its music.

### The one free thing that does help

The key is the **full-band** source, so the music under the dialogue is in the key too,
eating the contrast. Band-limiting the key to the speech band lifts it — but only once the
threshold is re-referenced to the filtered key's own level (my first attempt left the
threshold on the full-band mean, the key fell below it, and the duck got *worse* by
0.86 dB; that measured the level change, not the idea). Done properly, n = 8:

| sidechain key | dip mean | dip worst | permanent cost |
|---|---:|---:|---:|
| full band — shipped | 4.52 | 1.74 | 1.71 |
| **highpass 300 + lowpass 3400** | **5.17** | **2.38** | **1.25** |
| highpass 200 only | 5.03 | 2.28 | 1.37 |
| highpass 150 + lowpass 4000 | 5.02 | 2.30 | 1.40 |

**+0.65 dB mean, +0.64 dB worst-case, and the permanent cost drops too** — one filter, no
measurable CPU. **Recommended to MEMEBOT-021, which owns `duck.py`:** keep offset 0 and
ratio 20, move `attack_ms` 20 → 5, and band-limit the key. Combined that is roughly
2.4 dB worst-case against 1.74 today. **It is an improvement and it is still under the
audibility bar** — this is a source-material problem, and the only constructions that break
the ceiling are source separation (MEMEBOT-006: 16.7 CPU-hours/1,000 clips) or not ducking
clips whose contrast is too low to carry it.

---

## 4. Attack and release, against real speech

| clip | onset | rise | attack | release |
|---|---:|---:|---:|---:|
| DYctewoBTxB | 11.00 | 9.85 | **100 ms** | 0 ms |
| DYctewoBTxB | 17.18 | 9.68 | **140 ms** | 150 ms |
| Da0UT_fvF0D | 5.69 | 5.47 | **130 ms** | 0 ms |
| Da0UT_fvF0D | 12.44 | 8.33 | **100 ms** | 190 ms |
| DXd8PrcDuHl | 0.57 | 7.52 | **500 ms** | 0 ms |
| DXd8PrcDuHl | 10.46 | 7.84 | **480 ms** | 370 ms |
| DXd8PrcDuHl | 7.36 | 4.03 | **240 ms** | 80 ms |

**Configured attack is 20 ms. Measured onset-to-full-duck is 100–500 ms.** The VAD pads
spans by 100 ms, so subtract that and the honest range is **0–400 ms** — but that is still
5–20× the configured value, because `detection=rms` has to accumulate energy and real
speech ramps in rather than switching on. **The consequence the brief predicted is real:
the first syllable plays before the bed has finished moving.** `attack_ms = 5` shortens it
and is free (dip 4.05 → 4.52 mean).

**Release is not the problem.** Measured 0–570 ms against a configured 400 ms, and four of
seven offsets read 0 ms — the speech had already tapered before the VAD span ended, so the
bed was back up before the gap began. Nothing is left suppressed through the gaps.
`release_ms = 400` is well chosen and I would not touch it.

---

## 5. The headroom cost — **REFUTED in magnitude, confirmed in kind**

MEMEBOT-006 predicted a permanent ~5 dB loss. duck.py's table says −4.60 mean / −9.80 worst.

**Measured on real media, n = 11: 2.19 dB mean, 2.87 dB median, 3.85 dB worst, 0.08 dB best.**

The mechanism is confirmed — the loss is real, it is permanent, and it is caused by exactly
what was predicted, the original music holding the sidechain open with nobody speaking
(every duckable clip in this corpus is dialogue-**over-music**; there are no dialogue-only
clips to contrast against). **But it is under half the predicted size.** The likely reason
for the gap: MEMEBOT-009 measured with offline-TTS speech *pasted over* the clips, so its
key carried source **plus** added speech and sat hotter than any real clip's does.

**Is it worth accepting? Yes, and it is close to free.** 2.19 dB is a small price, and
duck.py already measured that `makeup = 1.412` (+3 dB) recovers the loss at **zero cost in
depth** (depth held at −8.05 against −8.10 while headroom moved −0.85 from −3.80). The
permanent cost is the one part of this treatment that is genuinely solved. **It is not what
makes the duck inaudible** — the dip being 2.57 dB median is, and that is the ceiling above.

---

## 6. The renders — one source, both treatments

`scratch/mb020/renders/`, all from `DYctewoBTxB.mp4` (18.6 s, h264 + aac, ~1.05 MB each).
Graphs come from `duck.build_audio_graph` **unmodified** — no tap, no substitution.

| file | treatment | bed gain | what it is for |
|---|---|---:|---|
| **`A_mute.mp4`** | mute-and-replace | −15.3 dB | the source audio is gone; the bed is the whole soundtrack |
| **`B_duck.mp4`** | duck-under | −15.3 dB | **same bed level as A**, so the only difference is the treatment |
| `C_duck_production_bed.mp4` | duck-under | −34.9 dB | what `edit.py`'s shipped relative rule actually computes |
| `D_duck_loud_bed.mp4` | duck-under | −8.3 dB | the bed 3 dB under the source — the duck is unmistakable here |

**A vs B is the comparison.** Play them back to back: same picture, same bed, same level —
in A the dialogue is gone and the music runs flat; in B the dialogue is present and the
music steps down 7.62 dB under it at 11.0 s and again at 17.18 s. `DYctewoBTxB` is the
**best** clip in the corpus (dip 7.62 dB against a 2.57 dB median), chosen deliberately so
the effect is audible at all — on the median clip it would not be.

**D is there because B and C are the same file to your ear.** Which brings up the thing I
did not go looking for:

### The bed is 29.6 dB under the source, so the depth barely matters

`edit.py`'s relative rule is `clamp(src_mean_db + offset, −50, −15)` and it is applied as a
**gain on the bed file**, not as a target level — the bed's own level never enters. For this
clip: source −17.9 dBFS, offset −17 → gain −34.9 dB on a bed measuring −12.6 dBFS →
**the bed lands at −47.5 dBFS, 29.6 dB below the source.**

```
mix over the non-speech window
  C_duck_production_bed  (bed -47.5 dBFS)   -18.82 dB
  B_duck                 (bed -27.9 dBFS)   -18.54 dB
  difference                                  0.28 dB
```

**A 19.6 dB change in bed level moves the output by 0.28 dB.** At the shipped level the
ducking is inaudible not because the depth is small but because there is almost nothing
there to duck. Fixing the depth without fixing this changes nothing a listener can hear.

**MEMEBOT-021 found this independently while I was measuring** — its `BED_PLAN_BY_CLASS`
now sets `dialogue-over-music` to `offset_db: (−8.0, −5.0)`, up from (−20, −14), landing
within a few dB of `D_duck_loud_bed`. Two rounds converging on the same number from
different directions is the strongest evidence in this report. **I have not touched it.**

---

## Concurrency — `duck.py` changed twice underneath me

It went **302 → 468 lines across three SHAs** during this round (`22b8685e` → `45a77ffd`),
because MEMEBOT-021 claimed it 2 minutes before I filed and is actively editing it.

I did not pin a frozen copy, because that would have measured a snapshot instead of what
ships. Instead I re-ran everything and checked whether the surface my numbers depend on had
moved. It had not:

```
DUCK_DEFAULTS      offset 0, ratio 20, attack 20, release 400, makeup 1, fallback .125
duck_threshold(-17.9, 0)                                              0.12735
sidechaincompress=threshold=0.127350:ratio=20:attack=20:release=400:makeup=1:detection=rms
DUCK graph string sha256[:16]                                9dc2929af08f3246
```

**Byte-identical to the version I first measured.** MEMEBOT-021's additions are all in a new
routing layer *above* the compressor (`bed_plan`, `TREATMENT_BY_CLASS`, `normalise_treatment`),
so the numbers hold across all three SHAs. **The report pins the graph SHA rather than the
file SHA**, because the graph is what was measured and the file is still moving. The full
default and sweep tables were re-run end to end against the current file and reproduced
within 0.07 dB.

`clippershq/loop_runner.py` and `tests/test_loop_runner.py` — MEMEBOT-015/018's modules —
**no longer exist**; MEMEBOT-017 absorbed them into `clip_pipeline.py` as its claim said it
would. `hook_chain`, `media_duration` and the `aloop` construction survived the move intact.

---

## Verification

| check | result |
|---|---|
| bypass control (`ratio=1.0`) → GR must be 0 | **0.00 / 0.00 / 0.00** |
| bed-level independence over a 34.9 dB change | **0.01 dB** |
| ceiling: clips whose dip beats their contrast | **0 of 11** |
| dip vs contrast correlation | **r = 0.920**, n=11 |
| default + sweep re-run against current `duck.py` | reproduced within **0.07 dB** |
| DUCK graph string | **`9dc2929af08f3246`** — unchanged across 3 file SHAs |
| `tests/run_all.py` | **63/64 green**; `test_filelock.py` red in batch, **PASSES standalone (4 tests, OK)** |
| `memebot/` modified by me | **no** — `scratch/` only |
| `config.json` | parses, 162 keys, untouched |
| spend | **$0.00** — no paid calls |

`test_filelock.py` is the known concurrency-sensitive suite; with 11 rounds in flight it
lost its quiet window. It passes on its own, which is the documented behaviour, and I am
reporting the batch result rather than the standalone one as the headline.

---

## Limits

- **n = 11 clips, one corpus.** All from `memebot/meme/downloads/`, all
  dialogue-over-music. **Zero dialogue-only clips exist here**, so the class MEMEBOT-006
  expected to duck best is entirely unmeasured — a clip with speech over true silence
  should show a permanent cost near zero and a much larger dip, and I could not test that
  claim.
- **The dip is a level measurement, not a listening test.** 4 dB is the brief's bar and a
  reasonable one, but audibility depends on the bed's spectrum against the source's, and I
  have not listened to any of these files. The renders exist so you can.
- **`contrast` comes from the VAD's own `speech_dbfs`/`bed_dbfs`**, which are computed on
  the same span mask used for the windows. The correlation is therefore partly
  methodological — both sides share the mask. The 0-of-11 ceiling result does not depend on
  the correlation and is the stronger claim.
- **One bed file** (`song01.mp3`, −12.6 dBFS). Gain reduction is bed-independent and that
  is verified to 0.01 dB, so this does not affect the depth numbers — but it does affect
  every statement about audibility in the mix.
- **The band-limited key is measured, not shipped.** It changes `duck.py`, which
  MEMEBOT-021 holds. Numbers above, decision theirs.
- **Attack timings inherit the VAD's 100 ms span padding.** I subtract it in the text but
  the table reports raw onset-to-90%, so the true compressor-relative figures are ~100 ms
  lower than shown.
- **`makeup` was not swept.** duck.py's existing measurement (zero depth cost) was taken at
  face value rather than reproduced.

---

## Method

Filed a claim; MEMEBOT-021 held `duck.py` with an overlapping brief, so this round wrote
nothing outside `scratch/` and reports tuning rather than applying it. Sources are the 61
clips already in `memebot/meme/downloads/` — no paid call, no key read, no spend. Windows
come from `clip_speech.py`'s silero VAD run locally. Depth is measured by tapping
`duck.build_audio_graph`'s bed leg, rendering with and without the compressor, and
subtracting frame-wise envelopes at 10 ms; the rig is validated by a bypass control that
must read zero and does. Every table was re-run end to end against the current `duck.py`
after it changed mid-round, and the DUCK graph string is pinned by hash so a future reader
can tell whether these numbers still describe the shipping filter.
