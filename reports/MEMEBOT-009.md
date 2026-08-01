# MEMEBOT-009: Ducking wired, tuned, and two bugs that an audio-only bench cannot see

**Date:** 2026-08-01 · **Type:** Implementation + measurement · **Spend:** $0.00 · **No paid call, nothing installed, memebot/ only**

Honesty tiers: **VERIFIED** (measured on this machine), **CORRECTION** (a MEMEBOT-006 number that does not survive real material), **GAP**.

---

## Verdict first

Ducking is wired into `memebot/scraper/edit.py` behind a per-run treatment switch, defaulting to **mute** as instructed. It is tuned, and the tuning is not MEMEBOT-006's.

Three things matter more than the wiring:

1. **MEMEBOT-006's recommended `threshold=0.03` costs -13.75 dB of permanent bed level on real clips, not the ~5 dB it predicted** — and it buys *less* duck depth than the setting shipped here. The threshold cannot be a constant. It is now placed relative to each clip's own measured level.
2. **The obvious filtergraph silently loses most of the bed.** `asplit` feeding both the mix and the sidechain measured -13.5 dB where -8.6 dB is correct. It only misbehaves once a video stream shares the graph, so an audio-only bench — which is what MEMEBOT-006 ran, and what I ran first — reports it as fine.
3. **The ffmpeg defaults are not the -0.4 dB no-op MEMEBOT-006 reported.** On real clip audio they duck by -3.9 dB. The no-op was an artifact of its quiet synthetic bed.

And one that reframes when to use this at all:

> **Ducking a bed that already sits under the source is close to pointless.** At memebot's shipped bed level the end-to-end effect measured **-0.40 dB**. With the bed *above* the source it measured **-1.29 dB** in the mix. The bed itself ducks by -3.7 to -8.5 dB; the mix does not, because the source is still in it.

Recorded in `duck.py`, in the config, and in the CLI help, exactly as instructed:

> **Ducking does not remove the original song.** Pointed at a copyright or detection problem it fails silently. Only `mute` removes it.

---

## What shipped

| file | what |
|---|---|
| `memebot/scraper/duck.py` | **new.** Treatment resolution, clip-relative threshold, the filter graph. Pure functions. |
| `memebot/scraper/tests/test_duck.py` | **new.** 29 tests. |
| `memebot/scraper/edit.py` | treatment resolved before the render, graph delegated to `duck.py`, third input for the sidechain key, `--treatment` flag, one guard bug fixed. |
| `memebot/scraper/config.yaml` | `ambient_bed.treatment` + `ambient_bed.duck` block. |

**43 tests pass** in `memebot/scraper/tests/` (29 new, 14 pre-existing). **565 pass** in `memebot/meme/tests/`, unchanged.

The switch, per job:

```
python scraper/edit.py --template white_frame --captions caps.txt --treatment duck
```

`mute` (default) · `duck` · `keep` · `default` (take `ambient_bed.treatment` from config). `keep` is the pre-MEMEBOT-009 plain mix, kept so the default change is reversible.

A source with no audio stream is forced to `mute` whatever was asked for, with the reason logged — that is the normal case for retrieved clips, since the DASH video rendition carries no audio.

---

## Part 1 — The two bugs

Both need a **video stream in the filtergraph** to appear. Both measured correct when the same graph was rendered audio-only. This is the part of the round I would most want a future agent to read.

### 1. `asplit` into a sidechain loses most of the bed

The obvious construction: split the source, send one branch to the mix and the other to `sidechaincompress` as the key. Source at -15.2 dBFS, bed at -10.1 dBFS, so a correct mix is about -8.9 dB. **VERIFIED**, three runs each:

| graph | mix level |
|---|---|
| no sidechain at all, plain `amix` | **-8.6 dB** — correct |
| `asplit` → sidechain → `amix` | **-13.5 dB** — bed mostly gone |
| **second decode** → sidechain → `amix` | **-8.6 dB** — correct |

`amix`'s direct branch races ahead of the branch that has to travel through `sidechaincompress`, and `amix` drops what has not arrived. The fix is to give the sidechain its own decode of the source — one extra audio input, measured at **1% of render cost**.

The same evasion chain is applied to the key as to the mix leg, because that chain carries the `atempo` matching the video's speed transform. A key at a different tempo drifts further out of sync the longer the clip runs.

### 2. `amix` renormalises when a branch starves

`amix`'s default `normalize=1` divides by the number of inputs it currently considers *active*. **VERIFIED:** the identical graph produced **-22.0 dB audio-only and -17.1 dB with the video mapped** — a 5 dB swing with no filter change, purely from scheduling. `normalize=0` removes the activity tracking and the level becomes reproducible.

Consequence, stated because it is a real difference: **duck's output sits ~6 dB above keep's**, which still halves both legs. Here the bed's configured volume is what you actually get and the source passes at unity, as it does on the no-bed path.

### 3. One I introduced, and fixed

Stashing a non-transform key in `_LAST_ROLLED_VALUES` defeated `_print_rolled_values`'s `if not v` guard and every render died on `KeyError: 'zoom'`. The guard now tests for an actual rolled value rather than dict emptiness. Pre-existing fragility, tripped by my change, fixed rather than worked around.

---

## Part 2 — Tuning. The threshold cannot be a constant.

### Method

MEMEBOT-006's duck depths came from a 440 Hz sine at -27.1 dBFS. Real clips in `memebot/meme/downloads/` measure **-11.4 to -35.2 dBFS**, most of them 12-16 dB hotter. So the bench here is real on both sides:

- **key** = a real clip's audio (continuous broadband music) + **real offline TTS speech** (Windows SAPI, free, no network) placed over one known window. Knowing exactly when speech is present is what makes depth measurable; only the *placement* is scripted.
- **main** = a *different* real clip's audio, as the new track.
- **gain reduction** = ducked minus undecked, per window. Immune to the song's own level drifting between windows, which a ducked-only comparison is not.
- **duck depth** = GR(speech) − GR(quiet). **headroom** = GR(quiet), the price paid always.

### The number that decides it — 12 real clips

**VERIFIED.** Threshold offsets are relative to each clip's own measured `mean_volume`; `attack=20, release=400, detection=rms` throughout.

| setting | depth mean | depth worst | **headroom mean** | headroom worst |
|---|---|---|---|---|
| **MEMEBOT-006 `threshold=0.03`, ratio 8** | -8.40 dB | -4.35 | **-13.75 dB** | -20.05 |
| relative +3 dB, ratio 20 | -7.61 | -3.95 | **-2.65** | -7.30 |
| **relative 0 dB, ratio 20 — shipped default** | **-8.50** | **-4.80** | **-4.60** | **-9.80** |
| relative -3 dB, ratio 20 | -8.93 | -4.90 | -7.02 | -12.55 |
| relative -6 dB, ratio 20 | -9.06 | -4.80 | -9.74 | -15.40 |

The shipped default buys **slightly more depth than MEMEBOT-006's fixed threshold for a third of the permanent cost.** Below 0 dB the trade turns bad fast: -3 dB buys 0.44 dB of extra depth for 2.4 dB more permanent loss.

A single-clip bench liked -3 dB. The 12-clip spread is what set the default — one clip cannot show whether a default travels. A separate travel test confirms the mechanism: fixed threshold gives headroom mean **-13.99 dB (spread 14.45)**, the relative rule **-7.33 dB (spread 7.25)** — half the cost and half the variance, for more depth.

### Pumping, measured rather than judged by ear

MEMEBOT-006 listed pumping as failure mode 4 and judged it by ear on a sine — which has no beat to pump against. Here: 50 ms RMS frames, gain reduction series, standard deviation taken **only where nobody is speaking**, so all movement is the compressor riding the music itself.

| setting | depth | headroom | **pump std** | p5-p95 spread |
|---|---|---|---|---|
| ffmpeg defaults | -3.90 | -2.10 | 1.76 dB | 5.43 |
| **MEMEBOT-006 recommended** | -9.25 | -13.25 | **4.58 dB** | **14.85** |
| relative +3, ratio 20 | -5.30 | -1.00 | 1.43 | 4.32 |
| **relative 0, ratio 20 (shipped)** | -6.80 | -2.20 | **2.31** | 7.16 |
| relative -3, ratio 20 | -8.10 | -3.80 | 3.25 | 10.01 |

**CORRECTION.** On real percussive material MEMEBOT-006's recommended setting has the **worst pumping of everything tested** — the bed's level wanders across a 14.85 dB span with nobody speaking. Its "audible at -15 dB, not at -10" was measured on material that could not exhibit the failure.

### Attack, release, detection

**VERIFIED**, and here MEMEBOT-006's choices hold up:

- `detection=rms` beats `peak` at **every** attack/release tested, by 1.0-1.7 dB of depth for the same headroom.
- `attack=20 ms` is the knee — 50 ms loses 1.1 dB of depth, 100 ms loses 2.3 dB. 5 ms gains 0.9 dB but at more headroom and more pumping.
- `release=400 ms` beats 250 ms by 1.5 dB. 800 ms buys 0.1 dB more depth for 1.4 dB more permanent loss.

### Sensitivity to how loud the dialogue is

Depth is a property of how far speech lifts the key above the bed. At the shipped setting: **-3.45 / -6.85 / -9.00 dB** for speech at **+0 / +6 / +12 dB** over the clip's own bed. Quiet dialogue under loud music ducks weakly, and no parameter choice fixes that.

---

## Part 3 — The headroom cost, and that it is free to recover

Instruction 3 said to accept a permanent ~5 dB loss and document it. **The shipped setting costs -4.60 dB mean across 12 clips (worst -9.80).** That is the ~5 dB, and it is the honest price of keying off unseparated audio: the original music holds the sidechain open when nobody is speaking.

**But it costs nothing to claw back. VERIFIED:**

| makeup | = dB | duck depth | headroom |
|---|---|---|---|
| 1.000 | +0 | -8.10 dB | -3.80 dB |
| 1.412 | +3 | -8.05 | -0.85 |
| 2.000 | +6 | -8.00 | +2.10 |
| 2.818 | +9 | -8.00 | +5.10 |

**CORRECTION.** MEMEBOT-006 called the loss "recoverable with `makeup`, at the cost of the ducking being less obviously motivated." **Depth is unchanged within 0.1 dB across a 9 dB range of makeup.** `makeup` lifts the ducked and unducked passages equally. The only thing it costs is that the bed's loud state is louder.

Default is **`makeup: 1.0` (none)** anyway — the operator set the bed level deliberately via `relative_offset_db`, and silently adding gain on top would undo that choice. The knob is in the config with the measurement beside it.

---

## Part 4 — Real renders, in each mode

Real source through the shipped `edit.py`: a real clip with **real TTS speech at two known windows**, so depth has something to be measured over. A stock clip has no ground-truth speech mask — MEMEBOT-006 found 21 of 22 are continuous music bed — so this is the only way the end-to-end number exists at all.

The "new track" is a different real clip's audio, because `scraper/sounds/ambient/` ships only a README. Real broadband music; not a licensed track; nothing published.

All four configurations render, pass `edit.py`'s own ffprobe health check, and produce 13.87 s output. **VERIFIED:**

| render | mean | peak | correlation vs source |
|---|---|---|---|
| **mute** | -10.1 dB | 0.0 dB | **-0.0051** |
| **duck** | -11.2 dB | -0.0 dB | +0.6183 |
| **keep** | -14.6 dB | -0.5 dB | +0.4744 |
| duck, threshold clamped (control) | -10.0 dB | -0.0 dB | +0.4577 |

**Mute genuinely removes the source** — correlation -0.005 against the source audio, i.e. none of it survived. That is the one treatment that actually gets the original song out of the file.

The **control** is the same render with the threshold clamped to 0 dBFS so the compressor never engages. Only the ducking differs between it and the live render.

| measured on | duck depth | headroom |
|---|---|---|
| **the bed leg**, exact render filter args, video in graph | **-3.71 dB** | -3.22 dB |
| **the final mix**, bed above source (bed -10.1, source -15.2) | **-1.29 dB** | -0.93 dB |
| **the final mix**, bed below source (memebot's shipped level) | **-0.40 dB** | -0.52 dB |

**This is the finding to carry forward.** The bed ducks by several dB. The *mix* barely moves, because the source is still in it and dominates the sum. Ducking only earns its place when the new track is at or above the clip's level — which is not what `relative_offset_db: -20..-14` configures today.

**Peak levels reach -0.0 dBFS with a loud bed.** With `normalize=0` the source and bed sum without attenuation. Check peaks before raising the bed; this round did not add a limiter, because one would change the measured depth.

### CPU per clip

**VERIFIED.** Measured at 46.0 s — the library's p50 — rather than extrapolated from an 11 s corpus. Best of 5, video stream-copied so this is the audio path only, directly comparable to MEMEBOT-006.

| treatment | audio-only | RTF | **CPU-h / 1,000** | MEMEBOT-006 predicted |
|---|---|---|---|---|
| mute | 1.054 s | 0.0229 | **0.293** | 0.40 |
| **duck** | 1.129 s | 0.0245 | **0.314** | 0.43 |
| keep | 1.119 s | 0.0243 | 0.311 | — |
| *the same render with libx264* | 4.40 s | 0.0956 | **1.22** | not measured |

Cheaper than predicted, and the extra decode for the sidechain key costs **1%**. The number that matters for memebot: **the video re-encode is ~4× the entire audio path**, so the treatment choice is not the cost driver. Ducking is free at this scale. Dollar cost $0.00 — local CPU, no API.

---

## Part 5 — Not built, per instruction 5

Mid/side centre extraction and band-passing the sidechain key to the voice band were both refuted in MEMEBOT-006 (-0.4 dB median removed; -3.8 dB vs -6.5 dB). **Neither was attempted.** Nothing here revisits them.

---

## Two interactions worth knowing (pre-existing, not changed)

1. **`ambient_bed.mode: auto` makes ducking unreachable.** `auto` lays a bed only when the source is *quieter* than `auto_threshold_db` (-32 dB). Real clips run -11 to -20 dB. A clip quiet enough to pass that gate has nothing worth ducking against. **Ducking needs `mode: always`.**
2. **`transform.enabled: false` also disables the ambient bed.** `ambient_bed` lives inside the `transform` block and `build_transform_filters` returns before reaching it. The config comment says "disable all transforms below"; it disables the bed too. This cost me a render pass that produced three byte-identical files with no bed at all.

Neither is fixed here — both are outside this round's scope and in a file another round was editing an hour ago.

---

## Concurrency

`MEMEBOT-011` held `scraper/edit.py` and `scraper/config.yaml` when this round opened; the claim tool flagged it. I benched first and touched neither file until that claim had cleared, then re-read the mix site before editing it. No collision.

---

## Honest limits

- **I cannot listen.** Every "confirmed" in this report is a measurement. The renders in each mode exist and are attached for someone with ears; I did not verify them by playback and do not claim to.
- **The speech is Windows SAPI TTS**, not a person on a real clip. Real dialogue has different dynamics; the placement being scripted is what makes depth measurable at all, and it is the same trade MEMEBOT-006 made with its sine.
- **The bench uses one song as the ducked track throughout.** Depth is a property of the *key*, which was varied across 12 real clips, so this is defensible — but it is one track.
- **Bed-leg depth is 2-3× what reaches the mix.** Both are reported above; quoting only the bed-leg number would overstate what a listener gets.
- **No VAD.** Routing between mute and duck is still a config decision. `speech_frac` is unwired (BL-846); BL-848 was wiring it during this round.
- **`verify_claims.py` cannot verify this round.** `.gitignore:137` ignores `memebot/` entirely — `git ls-files memebot` returns 0 files, so every claim reads "not committed at HEAD" and always will. Verified locally by the 43 tests instead. **Every MEMEBOT-NNN round has this hole**; it is a gap in the guarantee, not in this round. `docs/claims/MEMEBOT-009.claims` is filed and says so at the top.
- **The clipping question is open.** Peaks hit -0.0 dBFS with a loud bed and no limiter was added.

---

## Say it plainly

Ducking works, costs nothing, and is wired. What the round actually bought is smaller than it sounds: on this corpus the default is **mute**, mute is cheaper and cleaner, and ducking changes the audible mix by about a decibel unless the new track is loud enough to be in the source's way. The tuning matters — untuned or tuned to MEMEBOT-006's constant, you pay 13 dB of permanent bed level for less depth than the shipped setting gives. And the two filtergraph bugs would have shipped silently: both render successfully, both sound plausible, and both are invisible without a video stream in the graph.

<!-- CLAIMS
file:   memebot/scraper/duck.py
file:   memebot/scraper/tests/test_duck.py
func:   memebot/scraper/duck.py::resolve_treatment
func:   memebot/scraper/duck.py::duck_threshold
func:   memebot/scraper/duck.py::duck_config
func:   memebot/scraper/duck.py::sidechaincompress_filter
func:   memebot/scraper/duck.py::build_audio_graph
const:  memebot/scraper/duck.py::DUCK_DEFAULTS
const:  memebot/scraper/duck.py::TREATMENTS
const:  memebot/scraper/duck.py::DEFAULT_TREATMENT
file:   memebot/scraper/edit.py
file:   memebot/scraper/config.yaml
-->
