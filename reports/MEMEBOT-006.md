# MEMEBOT-006: Strip the music, keep the dialogue — don't. Duck it with ffmpeg, which is already installed and 39× cheaper.

**Date:** 2026-08-01 · **Type:** Deep research, read-only · **Spend:** $0.00 · **Nothing installed, no code changed, no paid call made**

Honesty tiers used throughout: **VERIFIED** (measured on this machine, or quoted from a primary source), **UNVERIFIED LEAD**, **REFUTED**, **GAP**.

---

## Verdict first

**Do not separate. Duck.** Three independent measurements point the same way:

1. **Separation costs 16.7 CPU-hours per 1,000 clips** — the same number that already killed the per-frame OCR line at 16 CPU-h/1,000.
2. **The ffmpeg path costs 0.43 CPU-hours per 1,000** and is already installed. **39× cheaper.**
3. **The only fast separator is refused by `pipguard`** — it wants to downgrade numpy 2.3.2 → 1.26.4.

And a fourth, from the clips themselves: **21 of 22 real clips have zero silent gaps.** This is music-bed material, not dialogue material. The premise of the round — that there is dialogue underneath worth rescuing — is weaker on this corpus than it looks.

**One thing must be said plainly before anything else, because it decides whether any of Part 2 applies:**

> **Ducking does not remove the original song. It only makes it quieter under speech.**

If the goal is to lay a new track *underneath* and keep the clip listenable, ducking is the right tool and this report recommends it. If the goal is to get a copyrighted or algorithm-flagged song *out of the file*, ducking does nothing at all — the song is still there, still audible, still fingerprintable. That job needs separation (expensive) or muting (free). Those are different problems and the rest of this report keeps them apart.

---

## Part 1 — Source separation

### The reframing that matters

Demucs, Spleeter, MDX-Net and Open-Unmix are trained on MUSDB18 to split a **song** into vocals/drums/bass/other. Their "vocals" stem means **sung** vocals. Spoken dialogue over a song is a different distribution from what any of them were fitted to. The tool family that treats music **as noise** is speech enhancement — a different family, evaluated below.

### Install hazard — `pipguard` dry-run verdicts, run locally, nothing installed

| package | verdict |
|---|---|
| `demucs` | **CLEAN** |
| `openunmix` | **CLEAN** |
| `onnxruntime` | **CLEAN** |
| `audio-separator` | **CLEAN** |
| `torchaudio` | **CLEAN** |
| `spleeter` | **FAILS — cannot even resolve** |
| `deepfilternet` | **REFUSED** |

**VERIFIED.** `spleeter` tries to build numpy from source and dies (`NameError: name 'CCompiler' is not defined`, `error: metadata-generation-failed ╰─> numpy`). It pins an ancient numpy and cannot coexist with this repo's numpy 2.x floor. `deepfilternet` is refused outright, verbatim:

```
package  import as  installed  pip would use  verdict
numpy    numpy      2.3.2      1.26.4         DOWNGRADE
REFUSED. Nothing was installed; your environment is untouched.
```

Same hazard class that BL-681/BL-682 already hit. The guard worked; nothing was installed.

### Demucs — the only clean, capable option, and it is too slow

**VERIFIED, licence:** MIT — *"Demucs is released under the MIT license as found in the LICENSE file."* Commercially unencumbered.

**VERIFIED, declared speed (primary docs):** *"With Demucs, processing time should be roughly equal to 1.5 times the duration of the track."*

The arithmetic against this repo's own corpus (p50 clip = **46.0 s**, measured over 767 library rows):

```
46 s x 1.5 = 69 CPU-seconds per clip
       x 1,000 clips = 69,000 CPU-seconds = 19.2 CPU-hours
```

At the mean clip length (43.6 s) it is **16.7 CPU-hours per 1,000**. Either way it lands on the line that killed per-frame OCR. Memory is ~7 GB at default arguments against 15.9 GB total — one job at a time, no parallelism worth having.

**Hardware, VERIFIED:** AMD Ryzen 5 5500 (Zen 3), 6 physical / 12 logical cores, 15.9 GB RAM, **AVX2 but no AVX-512**. This matters more than it looks: on this class of chip fp16/bf16 runs ~350× slower than fp32 (0.7 vs 278.7 GFLOP/s), so the usual "just run it in half precision" speed-up is unavailable. Demucs on this box gets fp32 or nothing.

**GAP:** Demucs was not run. It is `pipguard`-clean and could be installed, but the brief forbade installing and the cost arithmetic made it moot. The 1.5× figure is the authors' own and is **declared, not measured here.**

### Quality on degraded social clips — the evidence is against it

**VERIFIED (ISMIR 2022, Jeon & Lee, musdb-L/XL):** on loudness-normalised and limited material, *"performance of the state-of-the-art algorithms significantly deteriorated."* Social clips are exactly that — normalised, limited, re-encoded, often several generations deep.

**GAP:** the exact dB drops. The paper's PDF could not be parsed here (`pdftoppm` is not installed and WebFetch returns raw binary for the arXiv/ISMIR PDFs), so only the abstract-level claim is quoted. The direction is solid; the magnitude is unquantified.

**VERIFIED, artefact vocabulary (MSG paper):** separators *"add extraneous noise and remove harmonics"*; *"waveform-based models tend to add high-frequency noise, while spectrogram models tend to lose transients and high-frequency content."* Both failure modes are audible on speech — the first as hiss around consonants, the second as dulled plosives.

### DeepFilterNet — the fast one, and it is blocked

**VERIFIED:** RTF **0.04** single-threaded on a notebook Core-i5 (DFN2 paper) — about **25× realtime on one core**, versus Demucs' 1.5× *slower* than realtime. Roughly a 37× difference. Licence is dual **MIT / Apache-2.0**, commercially clean.

It is refused by `pipguard` (above), so it is not available on this machine today.

**UNVERIFIED LEAD:** DeepFilterNet also ships as a Rust binary and as ONNX, and **`onnxruntime` is `pipguard`-clean**. An ONNX route may sidestep the Python package and its numpy pin entirely. Not tested; nothing was installed.

**GAP, and it is the important one:** DeepFilterNet is trained on the DNS Challenge — fan noise, babble, street noise. Whether it removes **music** (a structured, harmonic, foreground signal) rather than treating it as part of the speech scene is **not established**. Do not assume the RTF number transfers to this problem until someone measures it on music.

---

## Part 2 — Ducking. Measured locally, on real clips.

**VERIFIED:** ffmpeg 8.0 is already on this machine with `sidechaincompress` (AA→A), `sidechaingate`, `acompressor`, `loudnorm` and `silencedetect`. Zero install, zero `pipguard` exposure, zero new dependency.

### Parameters (primary source: `ffmpeg-filters.html`)

| param | range | default |
|---|---|---|
| `threshold` | 0.00097563–1 | **0.125** |
| `ratio` | 1–20 | **2** |
| `attack` (ms) | 0.01–2000 | 20 |
| `release` (ms) | 0.01–9000 | 250 |
| `makeup` | 1–64 | 1 |
| `knee` | 1–8 | 2.82843 |
| `detection` | peak/rms | rms |
| `level_sc` | 0.015625–64 | 1 |

### The defaults are a no-op — measure before trusting them

Duck depth measured on a 6 s synthetic case with dialogue present only over t = 2–4 s:

| chain | duck depth |
|---|---|
| **ffmpeg defaults** (thr 0.125, ratio 2) | **−0.4 dB — no ducking at all** |
| thr 0.05, ratio 4, attack 20, release 300 | −5.2 dB |
| **thr 0.03, ratio 8, attack 20, release 400** | **−10.1 dB — recommended** |
| thr 0.02, ratio 20, attack 5, release 250 | −15.0 dB (pumping becomes audible) |

**VERIFIED.** Anyone who wires `sidechaincompress` and trusts the defaults ships a filter that does nothing. The control held: the music measured −27.1 dB in all three windows before ducking, so the dip is caused by the sidechain and nothing else.

Recommended chain for speech-over-music — **attack 20 ms** catches the start of a word without clipping its transient; **release 400 ms** rides through the gaps between words instead of pumping on every syllable:

```bash
ffmpeg -i newsong.wav -i clip.mp4 -filter_complex \
  "[1:a]aformat=channel_layouts=stereo[key];\
   [0:a][key]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=400[duck];\
   [duck][1:a]amix=inputs=2:normalize=0[out]" \
  -map "[out]" -c:a aac out.m4a
```

### Item 6 — does it need a separate speech track? No. It works keyed off the original, at a price.

Main track = the new song; sidechain key = varies. Depth = how much the new song dips while dialogue is present.

| sidechain key | song level when quiet | when dialogue | duck depth |
|---|---|---|---|
| isolated dialogue (**needs separation**) | −27.1 dB | −37.4 | **−10.1 dB** |
| **raw clip mix (NO separation)** | **−32.1 dB** | −38.8 | **−6.5 dB** |
| raw mix, voice-band 300–3400 Hz | −31.4 dB | −35.4 | −3.8 dB |

**VERIFIED, and this is the finding that decides the round.** Keying off the unseparated mix **works** — you keep 64% of the duck depth for **zero** separation cost. The real price is the first column, not the third: the new song sits **5 dB quieter all the time**, because the original music holds the sidechain open even when nobody is speaking. You trade permanent headroom for 39× the CPU. That is a good trade, and it can be clawed back with `makeup`.

**REFUTED — my own hypothesis.** Band-passing the key to the voice band to bias it toward speech makes it **worse** (−3.8 dB), not better. Music occupies 300–3400 Hz too. The idea is intuitive and wrong.

### Item 7's other half — the free separator that isn't

Dialogue in film and TV is mixed dead centre; music is spread wide. So mid/side maths should isolate the centre for free — no model, no install, real time. Measured across **60 real clips** in `memebot/meme/downloads/`:

- median S−M = **−9.9 dB**; 22/61 wide, 24 some width, **15/61 mono or near-mono** (6 are digital-silence mono, where the trick is arithmetically impossible)
- and the number that kills it: **discarding the sides removes a median of −0.4 dB of total energy**, worst case −2.4 dB

**REFUTED.** Bass, drums and lead vocal all sit centre and survive intact. Mid/side is free, instant, and removes essentially nothing. It is not a music remover on this material.

### Item 8 — the simplest case, and it reframes the problem

`silencedetect` (−35 dB, 0.3 s) over 22 real clips: **21/22 (95.5%) have zero silent gaps.** Every clip carries a continuous wall-to-wall audio bed.

**UNVERIFIED LEAD, stated as a proxy and not more.** This cannot separate "music only" from "dialogue on top of music" — both look continuous, because the music fills the pauses. What it *does* establish is that **no clip is dialogue-with-quiet-pauses**, so muting always removes something continuous, and the routing decision genuinely needs a real VAD rather than a silence heuristic.

What the library already knows (**VERIFIED**, 767 clips, measured here):

| field | value |
|---|---|
| `audio_type` = `licensed_music` | **334 (43.5%)** |
| `audio_type` = `original_sounds` | 426 (55.5%) |
| `track_title` declared | 328 (43%) |
| **`speech_frac`** | **None on all 767 — UNWIRED (BL-846)** |
| duration | p50 **46.0 s**, mean 43.6 s, p90 65.1 s |

So the routing signal half-exists. `audio_type` is free and populated, but it says what the audio **is licensed as**, not whether anyone is **talking**. The speech gate does not exist. BL-846 costed the missing VAD pass at ~1.6 s/clip — **0.44 CPU-hours per 1,000**, the same order as the entire ffmpeg path, and therefore affordable.

---

## Part 3 — Cost per 1,000 clips, and the recommendation

| path | RTF | **CPU-hours / 1,000 @ 46 s** | source |
|---|---|---|---|
| **mute original, lay new track** | 0.0312 (32× RT) | **0.40** | **measured, 60 real clips** |
| **duck new track under original** | 0.0337 (30× RT) | **0.43** | **measured, 60 real clips** |
| add a VAD routing gate | — | +0.44 | BL-846, declared |
| DeepFilterNet enhancement | 0.04 (25× RT) | ~0.5 | DFN2 paper — **BLOCKED by pipguard** |
| **Demucs htdemucs separation** | 1.5 (0.67× RT) | **16.7** | Demucs docs, declared |

Dollar cost of every viable path is **$0.00** — all of it is local CPU on hardware already owned, with no API in the loop. The 60-clip benchmark processed 12.3 minutes of real audio in 24.9 seconds of wall clock.

### Recommended path

**Duck the new track under the original clip audio, keyed off the original itself, using ffmpeg's `sidechaincompress` at `threshold=0.03:ratio=8:attack=20:release=400`. Do not separate anything.**

Then, when the VAD gate is wired, route on it:

- **no speech** → mute the original entirely and lay the new track on top (0.40 CPU-h/1,000, and the result is clean)
- **speech present** → duck as above (0.43 CPU-h/1,000, original stays audible underneath)

### Failure modes of the recommended path — stated up front

1. **It does not remove the original song.** If this is ever asked to solve a copyright or algorithmic-detection problem, it will fail completely and silently. Muting is the only free way to actually remove the song, and it takes the dialogue with it.
2. **A permanent 5 dB headroom loss** on the new track, because the original music holds the sidechain open during non-speech. Recoverable with `makeup`, at the cost of the ducking being less obviously motivated.
3. **The routing gate does not exist.** Until `speech_frac` is wired, there is no way to tell a music-bed clip from a dialogue clip, so every clip must take the conservative ducking path even when muting would be better and cleaner.
4. **Pumping on percussive material.** A 400 ms release riding a heavy beat can breathe audibly. The measured −15 dB setting is where this became obvious; −10 dB was not.
5. **Mono clips.** 15 of 61 are mono or near-mono. Ducking is unaffected — but it removes the last theoretical escape hatch, since no stereo trick can help there either.
6. **The benchmark is audio-only.** All timings stream-copy the video. Any path that re-encodes video will be dominated by that cost, not by the audio filter, and these numbers will not describe it.

### Say it plainly

Separation is not worth it on this material. Demucs is the only clean, capable option and it costs the exact CPU budget that already killed the OCR line, for a quality result the ISMIR evidence says degrades on precisely this kind of normalised, re-encoded, limited audio. The fast alternative is refused by the install guard. Meanwhile a tool already installed does the useful 80% for 1/39th of the cost.

**This is the fourth audio line closed on measurement here, and closing it is the correct outcome.**

---

## Honest limits

- **Demucs was never run.** Its cost is the authors' declared 1.5× realtime multiplied by this repo's measured clip length. It is `pipguard`-clean, so a real measurement is available to anyone willing to install it — the brief was read-only.
- **The duck-depth numbers come from synthetic audio**, deliberately: it is the only way to know exactly when dialogue is and is not present, which is what makes "duck depth" measurable at all. The *speed* numbers are from 60 real clips.
- **The synthetic "music" is a 440 Hz sine**, which is narrowband. Real broadband music would interact differently with the voice-band experiment — the REFUTED verdict on band-passing the key is directionally sound but the magnitude is proxy-derived.
- **`silencedetect` is not a speech detector** and is labelled a proxy everywhere it appears. It cannot distinguish music-only from dialogue-over-music, which is exactly why the VAD gate is still needed.
- **The 60-clip corpus in `memebot/meme/downloads/` may not represent the 767-clip library.** It is what exists locally; the durations run shorter (median ~11 s vs the library's 46 s), so the per-clip timings are extrapolated to 46 s rather than measured there.
- **The ISMIR degradation magnitude is a GAP**, not a soft claim — the PDF could not be parsed on this machine.
- **The DeepFilterNet ONNX route is untested.** It is the one lead worth chasing if the recommendation here is ever rejected.

---

https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/MEMEBOT-006.md
