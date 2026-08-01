# MEMEBOT-023 — Two treatments ship, duck is off behind a flag with its own measurement in the comment. Item 3's answer is **no: the bed-gain fix did not hold** — the bed landed **20.8 dB under the voice where the config asked for 5.2**. Fixed, and the residual is now **0.10 dB**.

**Date:** 2026-08-01 · **Type:** Ship + fix · **Spend:** **$0.00** (61 local clips, no paid calls)
**Changed:** `memebot/scraper/duck.py`, `edit.py`, `config.yaml`, `tests/test_duck.py`.
Verified released before starting: **MEMEBOT-021** (duck.py) and **MEMEBOT-016** (edit.py, config.yaml).

---

## 1. Two treatments, and duck behind a flag

| | routes to | why |
|---|---|---|
| `music-only` | **mute** | no dialogue to rescue; the only free way to remove the original song |
| `silent` | **mute** | |
| `dialogue-over-music` | **keep** | muting destroys the dialogue |
| `dialogue-only` | **keep** | |
| unknown word / unknown class / no class | **keep** | was `duck`; a fallback must land on a treatment that ships |

```python
SHIPPED_TREATMENTS = (TREATMENT_MUTE, TREATMENT_KEEP)
DUCK_ENABLED_DEFAULT = False
```

`TREATMENTS` still lists all three and `build_audio_graph` still renders duck correctly —
the path is **disabled, not rotted**, and a test proves it still builds. Asking for it by
name gets a refusal that carries the number:

```
duck requested but it is OFF by default and this run did not turn it on -- using keep
instead. MEMEBOT-020 swept 23 settings over 11 real dialogue clips and none reached the
~4 dB audibility bar: the dip is bounded by the clip's own speech-to-bed contrast
(r=0.920, 0 of 11 clips beat their own contrast) and one clip ducked BACKWARDS. Set
ambient_bed.duck.enabled: true if you want it anyway.
```

The alias is gated too — `clip_speech` says `duck-under`, and that must not slip past.
A test asserts the refusal is **not** phrased as an unknown word: *an unrecognised word is
a bug, a refused one is a decision*, and the two must stay distinguishable.

The full 23-row sweep, the r=0.920 ceiling, the backwards clip and the arithmetic reason
(`DIP = GR(speech) − GR(quiet) ≈ key(speech) − key(quiet)`, threshold cancels) are now in
the `duck.py` docstring and in `config.yaml` beside `enabled: false`. A test pins four
tokens of it, so the verdict cannot outlive its evidence.

## 2. Both free improvements taken

**`attack_ms` 20 → 5.** Dip 4.05 → 4.52 mean. Release left at 400 — measured 0–570 ms with
four of seven offsets at 0 ms; it was never the problem.

**`key_band = highpass=f=300,lowpass=f=3400`**, on the key leg and nowhere else. A test
asserts the band appears **exactly once**, on `[sc]`, and never on `[a0]` or `[a1]` — it
shapes what the compressor listens to, never what anyone hears.

The trap MEMEBOT-020 measured is wired shut. Band-limiting while computing the threshold
from the full-band mean makes the duck **0.86 dB worse**, so `key_band_filter()` exists and
`edit.py` probes through it:

```python
duck_thr, duck_thr_note = duck.duck_threshold(
    _probe_source_loudness(src, af=duck.key_band_filter(duck_cfg)), ...)
```

`_probe_source_loudness` gained an `af` argument and its cache key became
`(path, mtime, af)` — without that the windowed probe would be served from the unwindowed
entry. Both are pinned by tests, including one that reads `edit.py`'s source and fails if
the `duck_threshold` call stops referencing `key_band_filter`.

---

## 3. The bed-gain fix did NOT hold — and this is the real finding

MEMEBOT-021 moved the dialogue offset from `-20..-14` to `-8..-5`. **It fixed the
reference and not the units.** `basis + offset` is where the track should *sit*; `volume=`
takes a *gain*. Handing one to the other under-places the track by the bed file's own
level. Measured on a real render through the shipped CLI:

```
voice          -11.0 dBFS      offset rolled  -5.2 dB
INTENDED       bed at -16.2 dBFS,  5.2 dB under the voice
DELIVERED      bed at -31.8 dBFS, 20.8 dB under the voice
ERROR          15.6 dB
```

15.6 dB is the difference between a track that is present and one that is texture. It is
why `-8..-5` read as "unmistakably present" on a bench and did not arrive that way.

**Fixed in two steps, each measured:**

| | bed vs voice | error |
|---|---:|---:|
| before this round | 20.8 dB under | **15.6 dB** |
| after the units fix (`target − bed_db`) | 8.8 dB under | **3.0 dB** |
| after probing the bed's **window** | **7.3 dB under** (asked 7.2) | **0.10 dB** |

The 3.0 dB residual was not noise — `song01.mp3` is **−12.6 dBFS overall and −15.5 dBFS
over the 18 s window from 20.0 s that the render actually used**. Probing the file instead
of the window *was* the residual, exactly. The clamp moved from the gain to the level for
the same reason: `min(-10.0)` on a gain silently vetoed most targets once the units were
right.

**One instance remains and I did not change it.** Solo mode (music-only, ~52–80% of the
corpus) applies `solo_volume_db_min/max` as a raw gain with the same latent bug: the
music-only deliverable's soundtrack lands at **−26.9 dBFS**. MEMEBOT-011 chose that range
empirically against real deliverables, and I have no measurement of what level is right for
a track that *is* the soundtrack — so changing it would be swapping their evidence for my
guess. **Reported, not touched.**

---

## 4 + 5. The headroom figure, and the lesson

**Corrected in both files: 2.19 dB mean, 2.87 median, 3.85 worst, 0.08 best** — not ~5.
Real, permanent, caused by the predicted mechanism, under half the predicted size. The
`makeup` comments in `duck.py` and `config.yaml` carried absolutes from the injected-TTS
bench that read about 2× too deep; they now say so, and note that the *relative* finding
(makeup buys headroom back at zero depth cost) survives — so +3 dB now covers the whole
real loss rather than most of it.

The lesson is recorded in the docstring under its own heading:

> `relative 0 dB, ratio 20   duck depth -8.50   permanent headroom -4.60`
>
> Both numbers were CORRECT. Both were measured properly. The conclusion drawn from them —
> "ducking delivers 8.5 dB" — was wrong, because the music under the dialogue holds the
> compressor open even when nobody is speaking, so the −4.60 is already applied and a
> listener hears only the DIFFERENCE: 3.90 dB. That subtraction sat undone in this file for
> two rounds.
>
> **TWO CORRECT NUMBERS IN ONE TABLE CAN STILL PRODUCE A WRONG CONCLUSION. If a table has a
> "cost" column, subtract it before quoting the benefit.**

---

## 6. The renders

`scratch/mb023/renders/`, produced by the **shipped `edit.py` CLI** — no imported
internals, no hand-built filtergraph, just `--audio-class` and the config as it ships.

```
--- dialogue-over-music (DYctewoBTxB.mp4) ---
  song01.mp3 @ -2.7dB [relative (speech level -11.0dB -7.2dB -> bed at -18.2dBFS)]
  audio_treat  keep (routed on class dialogue-over-music)
  keep_dialogue-over-music.mp4   mean -15.6 dBFS   PEAK -0.7 dBFS

--- music-only (DUAaRozCWYc.mp4) ---
  song01.mp3 @ -11.4dB [solo (class music-only)]
  audio_treat  mute (routed on class music-only)
  mute_music-only.mp4            mean -28.1 dBFS   PEAK -11.7 dBFS
```

Over the speech window 11.3–13.7 s: **keep −12.7 dBFS** (the source, still there, at
−13.3, plus the track) against **mute −20.6 dBFS** (the track alone — the dialogue is
gone). That 7.9 dB is the binary choice, made audible.

---

## Two things shipping `keep` exposed

### It carried a 5 dB swing that depended on ffmpeg's scheduling

`keep` was a reversibility escape hatch and used `amix` with the default `normalize=1`,
which divides by the number of inputs it currently considers **active** and re-normalises
when one appears to starve — the duck branch measured **the same graph at −22.0 dB
audio-only and −17.1 dB with the video mapped**. That is not a level anyone chose, and it
was quietly halving both legs underneath `bed_plan()`'s choice. Now `normalize=0`, matching
the duck path.

### Which made it clip, so it needed a limiter

These sources are mastered to the ceiling — the deliverable clip **peaks at −0.0 dBFS
before anything is added to it**. With `normalize=0` and no limiter:

```
keep no limiter    mean -15.00 dBFS   peak   0.00 dBFS     <- clipping
keep with limiter  mean -15.20 dBFS   peak  -1.00 dBFS
```

`alimiter=limit=0.891:attack=5:release=50:level=disabled`. **Measured: mean moves 0.20 dB,
peak moves 1.00 dB** — peaks only, mix level preserved, which is the claim the comment
makes and a check I ran rather than asserted. `level=disabled` is load-bearing: alimiter's
default normalises the output *up* to the limit, which would undo `bed_plan()`'s level
choice exactly the way `normalize=1` did.

---

## The class never reaches the renderer

`clippershq/clip_pipeline.py` computes the audio class at line ~1445, writes it into the
record at ~1497, and then calls `render_one()` — which builds its argv **without
`--audio-class` or `--treatment`**. So `edit.py` gets no class, and every clip rendered
through that pipeline lands on the no-class fallback. **MEMEBOT-021's class routing is
correct and unreachable from the pipeline that matters.**

The consequence is not neutral: the majority class is music-only and every one of those
should mute. Instead they keep their original song — the copyright-shaped failure the top
of `duck.py` warns about, arrived at by omission. **Seventh instance of the MEMEBOT-015
shape**: a value computed correctly upstream and dropped at a module boundary, with the
render succeeding either way.

`clip_pipeline.py` is **BL-855's**, so I did not touch it. What I could do from my side is
make it impossible to miss, and that is done — the no-class path is now a loud warning
naming the fix, plus a test that pins it as the live path rather than an edge case.

---

## Verification

| check | result |
|---|---|
| `memebot/scraper/tests` | **90/90 OK** (was 43 before this round) |
| `tests/run_all.py` | **ALL GREEN — 81/81 suites, 3,556 checks** |
| routing never picks duck, any class | asserted over all 4 classes + `None` + garbage |
| duck still builds when enabled | asserted |
| key_band on the key leg only | exactly once, on `[sc]`, absent from `[a0]`/`[a1]` |
| `edit.py` probes through `key_band_filter` | source-pinned |
| bed lands where the config asks | **0.10 dB error** (was 15.6) |
| keep peak with limiter | **−1.00 dBFS** (0.00 without) |
| limiter touches peaks only | mean 0.20 dB, peak 1.00 dB |
| both treatments render via the shipped CLI | rc=0, h264+aac |
| `config.yaml` parses, new keys read | `duck.enabled=False`, `attack_ms=5`, `key_band` set |
| `config.json` | parses, 162 keys, untouched |
| spend | **$0.00** |

---

## Concurrency

**BL-865 committed my mid-round state.** Its commit `dbbaae1` ("Commit the audio work:
ducking, run records, and the caption-fit tests") snapshotted `duck.py` and `config.yaml`
while I was still editing them — which is exactly the git-index operation its claim
declared, and it did not disturb my working tree. Worth recording anyway: **the commit
message describes finished work, and what was in the tree at that moment was half a round.**
The limiter, the units fix, the window probe and the new tests all landed after it and are
still uncommitted. Nothing was lost and the suite is green.

`scraper/templates.yaml` also shows modified — that is MEMEBOT-016/026's cropping work,
not mine, and I left it alone.

---

## Limits

- **One clip per treatment.** `DYctewoBTxB` (dialogue-over-music) and `DUAaRozCWYc`
  (music-only). The bed-placement error was measured on one song and one window; the
  arithmetic is general but the 0.10 dB residual is not a corpus figure.
- **The bed window probe needs `start_sec`.** With no explicit window it falls back to the
  whole file and the 3.0 dB class of error returns. The clippershq pipeline always sets it;
  a bare `edit.py` run using the loudest-window heuristic does not.
- **Solo mode still has the units bug** — reported above, deliberately not changed.
- **`dialogue-only` is routed but untested on real media** — the corpus has none
  (MEMEBOT-020 measured 0 of 61). Its routing is asserted in tests only.
- **The limiter was measured on one render.** 0.20 dB of mean movement on a source peaking
  at −0.0 dBFS; a quieter source would see it act less, a hotter one more.
- **I went one step past "verify" on item 3.** The brief asked me to confirm the bed level;
  I found a 15.6 dB error and fixed it, because `keep` is a treatment this round ships and
  a track 20.8 dB under the voice would have made the deliverable meaningless. The fix is
  in `edit.py`, which my claim covers.
- **No listening test.** Every number here is a level measurement.

---

## Method

Claimed after verifying MEMEBOT-021 and MEMEBOT-016 were out of flight. Routing, the gate
and the graph changes are in `duck.py`; the bed arithmetic is in `edit.py`; the flag and
every measurement that justifies it are in `config.yaml` beside the knob they explain. The
two renders come from the shipped CLI with `--audio-class`, and every claim about them was
checked by measuring the file — peaks included, because `normalize=0` was a change I made
and the clipping risk was mine to close. Tests that encoded the old contract were updated
to the new one with the reason in the docstring rather than deleted. No paid call, no key
read, no spend.
