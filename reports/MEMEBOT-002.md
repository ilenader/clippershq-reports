# MEMEBOT-002: The ambient mixer works. Four other things do not.

**Date:** 2026-08-01 · **Class:** Smoke test · **Spend:** $0.00, no paid calls. Read-only on `clippershq`. `memebot/scraper/config.yaml` was modified and **restored from backup** at the end; `clips/tiktok/smoketest/` remains as the proof artifact and can be deleted.
**Claim:** `MEMEBOT-002` filed at start, ended at close.

---

## The headline

**A finished video with a song mixed onto it exists**, at
`memebot/scraper/clips/tiktok/smoketest/final/gainzalgo/smoke01.mp4` (8.4 MB, 10.07 s).
`_mix_ambient_bed()` ran on real audio for the first time and did its job.

**But your song was never there.** `scraper/sounds/ambient/` contained only `.gitkeep` and `README.md` when I started. I searched every audio extension under `memebot/`, every audio file modified anywhere in the project in the last 24 hours, and the Desktop root: nothing. Two `.mp3`/`.m4a` files that existed under `clips/tiktok/*/_raw/` when I first looked had vanished by the time I tried to copy one, minutes later.

So I built test tracks by extracting real audio from a real clip in `meme/downloads/` — 3 s, 19.9 s and 179 s versions. Everything below is measured on real audio. **The one thing I could not do is item 3's comparison against where you would say the hook is, because that needs your track.**

---

## 1. Does it produce a video with the song on it? Yes — and the proof is the silent clip

The cleanest evidence is the source clip I stripped of audio. Source `smoke02_silent.mp4` has **one stream, video only**. After the ambient render the output carries an AAC stream at **mean −56.6 dB, max −40.6 dB**. Audio exists where there was none, so every decibel of it is the ambient bed.

Run log for that render:

```
ambient_bed  test_long.mp3 @ -41.3dB [relative (src -22.0dB -19.3dB)],
             start=112.4s [loudest] (always)
```

## 2. Every capability, one at a time

| capability | result |
|---|---|
| arbitrary file | **works** — picked up both staged tracks |
| start offset (`-ss` before `-i`) | **works** — `start=112.4s` on the long track |
| looping when track < clip | **works** — a **3.0 s** track under a **10.07 s** clip produced **10.06 s** of audio (`-stream_loop -1` looped it ~3.4×) |
| silent source clip | **works** — ambient becomes the only audio (the `else` branch, `[1:a]…[a_out]`) |
| volume | **works** — `-45.8 dB` and `-41.3 dB` applied |
| fades | wired; **not independently verified** — my clips were long enough to keep fades on, but I did not isolate the fade envelope |
| loudness-relative mode | **works mechanically**, and see the defect below |

**Defect in relative mode on a silent source.** For `smoke02_silent` the log reports `src -22.0dB` — but that clip has no audio stream, so there is no source level to be relative to. `_probe_source_loudness()` returned a number anyway, and the bed landed at **mean −56.6 dB, which is inaudible in any practical mix**. Relative mode should fall back to absolute when the source has no audio track.

## 3. `_find_loudest_window_start()` — it is not doing what its name says

On the 179 s track it returned **112.297 s** (62.7% in); the pipeline then seeked to `112.4s`. Reproducible across runs.

**But the window is wrong by a factor of ~43.** The function passes `window_sec` straight into `astats=reset=N`, and **`reset` counts frames, not seconds**:

```
1024 samples @ 44100 Hz = 0.0232 s per frame
reset=20  ->  20 x 0.0232 = 0.464 s     (what it actually scans)
a true 20-second window needs reset = 861
```

Measured directly: with `reset=20` the emitted timestamps step **0.0240 s** apart across 7,466 windows. So `_find_loudest_window_start(window_sec=20)` returns **the start of the loudest half-second**, not of the loudest 20-second section. Setting `reset=862` changes the answer to **103.46 s** — a different part of the track entirely.

There is a second, subtler issue: `ametadata=print` emits **per frame** regardless of `reset`, so `max()` picks a frame *inside* the loudest window rather than the window's start.

**What that means for hook selection:** as written, this finds a transient — a snare, a bass hit, a shout. That is not a hook. It is close enough to be tempting and wrong in a way that will not be obvious in output. **My recommendation is to always pass an explicit offset** and keep this only as a fallback, and if you keep it, fix `reset` to `round(window_sec * sample_rate / 1024)` and take the window start rather than the peak frame.

I cannot tell you how far it lands from *your* hook, because your song is not on disk.

## 4. The two gaps — confirmed, with the exact changes

**Gap 1 — random selection.** Confirmed empirically: `pick_ambient_file(folder, rng)` with seeds 1–5 returned `test_long, test_long, test_long, test_long, test_short`. There is no parameter to request a file.
*Change:* add an optional first-class argument —
`def pick_ambient_file(folder, rng, explicit=None)` returning `Path(explicit)` when given, after an existence check; and thread a `--ambient-file` / `ambient_bed.file` config key through `edit.py`'s transform builder to it. Four lines, no behaviour change when unset.

**Gap 2 — no end offset.** Confirmed by reading the built command: trimming is implicit via `amix=duration=first` plus `-shortest`, so the bed always ends when the video does.
*Change:* the ambient input already accepts `-ss` before `-i`; add `-t <len>` immediately after it for input-side duration, **or** put `atrim=start=0:end=<len>,asetpts=N/SR/TB` at the head of the `[1:a]` chain. The `-t` form is simpler and composes with `-stream_loop -1` (loop, then cut). A "use 12.4 s → 27.9 s" job becomes `-ss 12.4 -t 15.5`.

## 5. The encoding chain — the audit's profile does not hold

| claimed | measured on output |
|---|---|
| `libx264` | ✅ h264 |
| `-crf 23` | ❌ **rolled randomly** — I saw crf 18, 19, 20, 21, 23 across runs |
| `-pix_fmt yuv420p` | ❌ **`yuv444p`, profile High 4:4:4 Predictive** |
| `aac -b:a 128k` | ✅ 127.8–128.2 kb/s |
| `+faststart` | ✅ `moov` at byte 36, before `mdat` |
| metadata stripped | ⚠️ partial — `encoder` blanked, but `handler_name`, `vendor_id`, `major_brand` remain (normal ffmpeg muxer output) |

**`yuv444p` is the serious one.** There is no `-pix_fmt` anywhere in `edit.py`'s command construction — neither the ambient branch nor the plain branch — so x264 keeps the filter chain's 4:4:4 output. **This is not caused by ambient**: a `--ambient never` control render produced `yuv444p` too. 4:4:4 High Predictive is rejected or silently re-encoded by most social platforms and will not hardware-decode on many phones. It also inflates the file — one 10.8 s output came out at **39.8 MB / 29 Mbps**.
*Change:* add `-pix_fmt yuv420p` to both branches, beside `-c:v libx264`.

## 6. Fragility the audit could not see

**A. The pipeline fails about half the time, and the failure destroys the previous good output.** Today's log: **6 `edit:fail` against 6 `edit ok`**. The error:

```
[Parsed_pad_8] Padded dimensions cannot be smaller than input dimensions.
[vf#0:0] Error reinitializing filters!  Task finished with error code: -22
```

The random `zoom` (1.05–1.2×) can scale the video past the 1080×1920 pad target, and the pad filter refuses. It is a dice roll per render, unrelated to ambient — one `--ambient never` render hit it too. Worse, the recovery path logs `edit:recover removing existing dst to re-render` **before** rendering, so a failed re-render leaves you with **no file at all** where a working one existed. I lost a good `smoke02_silent.mp4` output exactly this way.

**B. `edit.py` must be run from the memebot root, and says otherwise.** Running `python edit.py` from inside `scraper/` gives:

```
✕ Montserrat-Bold.ttf missing at scraper/fonts/Montserrat-Bold.ttf.
   Fetch with: git clone --depth 1 https://github.com/JulietaUla/Montserrat.git ...
```

**The font is present** (`scraper/fonts/Montserrat-Bold.ttf`, 454,864 b). The path is resolved against the CWD, so from `scraper/` it looks for `scraper/scraper/fonts/`. The error then tells you to download a file you already have. Correct invocation is `python scraper/edit.py …` from `memebot/`.

**C. Pipeline B's input directory is empty.** `clips/tiktok/` contained no clips at all; I had to stage them. `discover_videos()` expects `clips/<platform>/<handle>/*.mp4`. Anyone following the audit's "run pipeline B once" would get an empty batch and no error.

**D. No dependency manifest — confirmed, and it bites immediately.** No `requirements.txt`, `pyproject.toml` or lockfile anywhere. `edit.py` imported cleanly here only because this machine already has the packages. ffmpeg/ffprobe 8.0 are on PATH and every flag used worked.

## What I would fix, in order

1. **`-pix_fmt yuv420p`** — one flag, and without it the output is not postable.
2. **Clamp zoom against the pad target** — a 50% failure rate is the pipeline's dominant defect, and it currently eats good files.
3. **Do not delete the destination before a successful render** — write to temp, replace on success.
4. **Fix `reset=` units in `_find_loudest_window_start`**, or drop the function and always pass an explicit offset.
5. **Fall back to absolute volume when the source has no audio.**
6. Then the two integration gaps (explicit file, explicit end offset), which are the smallest changes here.

**Nothing was wired into clippershq.**

## Method and limits

Ran `edit.py --template gainzalgo --only smoketest` against two staged clips (one with audio, one stripped to video-only), with `--ambient always`, `--ambient never`, and repeated runs to characterise the intermittent failure. Test audio was extracted from `meme/downloads/Da0UT_fvF0D.mp4`; **it is not a song and has no hook**, so the loudest-window pick is reported as a measurement, not as a judgement of hook quality. Fades were not isolated. The `-c:a copy` path for a silent source without ambient was never observed cleanly — both attempts died on the pad bug first — so I make no claim about it. Config was restored to `enabled: false`; re-enable at `scraper/config.yaml:126`.
