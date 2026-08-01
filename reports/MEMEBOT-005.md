# MEMEBOT-005: All six fixed, each proven on a real render

**Date:** 2026-08-01 · **Class:** Fix + proof · **Spend:** $0.00, no paid calls. **`clippershq` untouched** — only `memebot/scraper/edit.py` and `memebot/scraper/config.yaml` changed, both backed up first (`*.20260801_142313.memebot005.bak`).
**Claim:** `MEMEBOT-005` filed at start, ended at close.

Every defect below was measured on real renders by MEMEBOT-002, and every fix is proven the same way.

---

## 1. `-pix_fmt yuv420p`, and CRF pinned

There was no `-pix_fmt` anywhere in `edit.py`, so x264 kept the filter chain's 4:4:4 and emitted **High 4:4:4 Predictive** — rejected or silently re-encoded by every major platform, and not hardware-decodable on most phones. Added to **both** command branches (ambient and plain).

**Proof — same clip, before and after:**

| | pix_fmt | profile | size / bitrate |
|---|---|---|---|
| before | `yuv444p` | High 4:4:4 Predictive | 39.8 MB · 29 Mbps |
| **after** | **`yuv420p`** | **High** | 10.7 MB · 7.2 Mbps |

1080×1920 and `aac` at ~128 kb/s are unchanged.

**CRF pinned at 20** (`crf_min: 20`, `crf_max: 20`). It was rolling 18–23, so the same source came out at unpredictable size and quality — MEMEBOT-002 saw 18, 19, 20, 21 and 23 across a handful of renders. 20 is near-transparent at this resolution and leaves headroom for the platform's own re-encode in a way 23 does not. Preset and keyint still vary, so per-variant encoder fingerprints still differ. Live render log now reads `enc(fast/crf20)` every time.

One honest note: the surviving bitrate is still high (7–19 Mbps) because `frame_noise` grain is expensive to encode. That is the grain setting's cost, not a defect, and it is now a decision you can see rather than a dice roll.

## 2. Zoom clamped against the pad — root cause found

The failure was **arithmetic, not luck**. `crop=iw/zoom:ih/zoom` truncates to integers, which nudges the aspect ratio; `scale=W:-1` then sets the width and lets the height land where it may. On a **full-bleed** template (`gainzalgo`, `scale_width` 1080 == canvas width) that height comes out **1922** for most zoom values, and `pad=1080:1920` refuses anything larger than the canvas:

```
zoom 1.05 -> 1080x1920 pass      zoom 1.08  -> 1080x1922 FAIL
zoom 1.15 -> 1080x1920 pass      zoom 1.10  -> 1080x1922 FAIL
zoom 1.20 -> 1080x1920 pass      zoom 1.13  -> 1080x1922 FAIL
                                 zoom 1.164 -> 1080x1922 FAIL
                                 zoom 1.19  -> 1080x1922 FAIL
```

`white_frame` (864 wide) never overflowed, which is why the bug looked random rather than structural.

**Fix:** scale into the *box* instead of setting width alone —
`scale={w}:{canvas_h - y_offset}:force_original_aspect_ratio=decrease`, then an even-dimension trunc. It only ever shrinks, so compositions that already fitted are unchanged.

**Proof: 20 consecutive renders (10 runs × 2 clips) — `rendered=20 errors=0`.** Before the fix the same session logged 6 failures against 6 successes.

## 3. The destination is never deleted before a successful render

`apply_template` unlinked `dst` *before* rendering. The render already wrote to `tmp` and only `os.replace`d after both the ffmpeg return code and an ffprobe health check passed — so the deletion bought nothing and cost the previous good file on every failure. MEMEBOT-002 lost an output exactly that way. The pre-emptive unlink is gone.

**Proof:** I corrupted a source clip (4,096 garbage bytes) so its render had to fail, with a good output already on disk:

```
before  size=5,743,121  mtime=14:46:06  sha256=ED18D6C94092EC11F58F…
render  RESULT edit: rendered=1 skipped=0 errors=1 status=partial
        log: smoke01 edit:fail [mov,mp4…] moov atom not found
after   size=5,743,121  mtime=14:46:06  sha256=ED18D6C94092EC11F58F…
        PREVIOUS OUTPUT SURVIVED UNCHANGED: True     stray .tmp.mp4: 0
```

## 4. `_find_loudest_window_start()` units — and demoted to a fallback

`astats=reset=N` counts **audio frames**, not seconds. At 1024 samples/frame the old `reset=window_sec` asked for 20 frames = **0.46 s**, about 43× short, so the function returned the loudest half-second — a snare or a shout, not a section. It also returned the peak *frame* rather than the window start, because `ametadata=print` emits every frame regardless of `reset`.

Both fixed: seconds are converted using the file's real sample rate, and per-frame readings are bucketed by window so the returned value is the window **start**.

**Proof** on a 179.1 s / 48 kHz track:

| window_sec | reset (frames) | actual window | returned start |
|---|---|---|---|
| 20 | 938 | 20.01 s | **100.00 s** |
| 10 | 469 | 10.01 s | 30.00 s |
| 5 | 234 | 4.99 s | 110.00 s |

Before the fix, `window_sec=20` returned 112.30 s — a transient inside a different section. The live pipeline now logs `start=99.5s [loudest]` (100.0 s window start, minus the ±2 s per-variant jitter).

**And it is now explicitly a suggestion.** The docstring says so, and explicit offsets take precedence over it in the config path below. Loudness is not structure; hand-marked windows are the design.

## 5. Both integration gaps closed

**Explicit file.** `pick_ambient_file(folder, rng, explicit=None)` — accepts an absolute path, a repo-root-relative path, or a bare filename in the folder, driven by `ambient_bed.file`. A named file that does not exist returns `None` and **skips ambient loudly rather than falling back to a random track**, so a typo cannot silently ship the wrong sound.

```
explicit=bed_long.mp3        -> bed_long.mp3
explicit=does_not_exist.mp3  -> None (fails loudly)
same name across 5 seeds     -> {'bed_short.mp3'} (deterministic)
random path still works      -> bed_long.mp3
```

**Explicit end offset.** `ambient_bed.start_sec` / `end_sec` add an input-side `-t (end-start)` immediately after the existing `-ss`, so the bed is cut to the requested length instead of being trimmed implicitly by video length.

**Proof** with `file: bed_long.mp3, start_sec: 12.4, end_sec: 17.4` (a 5.0 s window) on a **silent** source, so every decibel is the bed. Per-second mean volume of the output:

```
t=0-1 -55.4   t=1-2 -55.0   t=2-3 -59.7   t=3-4 -62.4   t=4-5 -64.4
t=5-6 -90.3   t=6-7 (silent)  t=7-8 (silent)  t=8-9 (silent) …
```

Audio for exactly 5 seconds, then nothing. The render log reads `bed_long.mp3 @ -44.7dB … start=12.4s [explicit-window]`.

## 6. The two smaller ones

**Font path.** Added `resolve_asset()`, which tries the CWD, then repo-root-relative, then scraper-relative. Used by `ensure_font_available`, the `apply_template` pre-check, and the `drawtext` filter itself, so the resolved path is what ffmpeg receives. Running `python edit.py …` **from inside `scraper/`** now renders: `rendered=2 skipped=0 errors=0`. Previously it reported the shipped font as missing and told you to download a file already on disk.

**Empty clips tree.** `0 videos to process` now says where it looked and why:

```
0 videos to process
   looked in: …\emptyclips
   platform dirs present: tiktok — but no <platform>/<handle>/*.mp4 inside them.
   run the scraper first, or drop a clip in by hand to test.
```

---

## State on exit

`config.yaml` restored to its shipped defaults — **`ambient_bed.enabled: false`**, no `file`/`start_sec`/`end_sec` keys — with only the CRF pin kept, since that is one of the fixes. Test tracks deleted; `sounds/ambient/` holds `.gitkeep` and `README.md` again. `edit.py` and `config.yaml` both parse. `clips/tiktok/smoketest/` is left in place as the working artifact and is safe to delete.

To use the ambient bed: set `enabled: true`, drop a track in `scraper/sounds/ambient/`, and optionally set `file` / `start_sec` / `end_sec` to name the exact sound and window.

## Limits

The 20-render proof used one template (`gainzalgo`, full-bleed) and two clips; `white_frame` was never failing and was not re-tested at length. The pad fix is proven for the full-bleed case that was breaking — a template whose `y_offset` plus scaled height still exceeds the canvas would now be shrunk to fit rather than failing, which is a behaviour change I judged correct but did not exercise. Fades remain unverified. CRF 20 is my judgement call, not a measured optimum. Audio was confirmed present, at the right level, and cut at the right time by measurement; I did not watch the video for lip-sync beyond confirming stream durations match (11.97 s video / 11.97 s audio).
