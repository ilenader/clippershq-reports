# MEMEBOT-018 — All three gaps closed for **$0.00**. `place_at` proved by a **47 dB** silence-to-song step, and closing them exposed two more silent boundary bugs — including one where ffmpeg reported "No space left on device" with **94 GB free**.

**Date:** 2026-08-01 · **Type:** Fix + measurement · **Spend:** **$0.00** (used the 61 already-downloaded clips; no paid calls)
**Changed:** `clippershq/loop_runner.py`, `tests/test_loop_runner.py` (20 → 34 tests).

---

## 1 + 2. `place_at_s` applied, hook looped — one filter chain, measured

```
,atrim=start=20.000:end=24.000,asetpts=PTS-STARTPTS,aloop=loop=-1:size=176400,adelay=28694|28694
```

Injected through `duck.build_audio_graph`'s `fade_chain` slot, so **duck.py stays the single
owner of the mix** and no graph is rebuilt here.

**`place_at_s` — measured on the bed-only render, where the source cannot mask it:**

| window | mean |
|---|---:|
| 0.00 – 27.7 s (**before** placement) | **−68.8 dB** |
| 29.7 – 34.7 s (**after** placement) | **−21.8 dB** |

**A 47 dB step.** Digital silence until 28.69 s, then the song — exactly the 43% of a 66.73 s
clip that MEMEBOT-003 specified. It was recorded and ignored for two rounds; it now lands.

**The hook loops** — a 4.0 s window across the whole remainder:

```
at 29.7s : -21.6 dB     at 52.7s : -22.4 dB
at 40.7s : -22.4 dB     at 62.7s : -22.2 dB
```

Output **66.62 s from a 66.73 s source**. A truncating bug gives ~4 s; MEMEBOT-015's did
exactly that. **`-t` is nowhere near the audio input** — the trim happens in the filter, and a
test asserts the chain contains no duration flag.

Three details that are load-bearing and all tested: `asetpts=PTS-STARTPTS` (without it `aloop`
and `adelay` work off the *original* timestamps and the audio lands minutes late), `aloop`'s
`size` is in **samples** not seconds (176400 = 4.0 × 44100), and the chain must start with a
comma because duck appends it directly.

## 3. Ducking on real media — and the threshold is real

Source: `DI8-v0YtJ0V.mp4`, 66.73 s, **video + audio**, mean **−15.7 dB**.

```
render: True   duck (requested)
source_mean_db = -15.7   duck_threshold = 0.16406
fallback would have been 0.125   <- ffmpeg's default = MEMEBOT-006's -0.4 dB no-op
```

**The threshold is derived from the source's own measured level, not the default.** That is the
difference between ducking and decoration: with the fallback the graph is identical, the render
succeeds, and nothing audibly ducks.

The duck path now runs end to end on real audio for the first time — MEMEBOT-015 could only
report `mute`, because the DASH rendition carries none.

---

## Two more silent boundary bugs, found by closing the gaps

### `duck_threshold` returns `(threshold, note)`, not a float

Passing it straight through raised `TypeError` deep inside `sidechaincompress_filter`. **Same
class as the treatment-vocabulary bug** — a value computed correctly and mis-handed at a module
boundary. This one at least crashed; the treatment one survived a whole round because it
*didn't*.

### `-shortest` does NOT bound an infinite filtergraph

`aloop=loop=-1` makes the bed infinite. On the **duck** path `amix=duration=first` happens to
stop it. On the **mute** path nothing does:

```
mute render: False   space left on device
[fc#0] Task finished with error code: -28 (No space left on device)
```

**With 94.13 GB free.** ffmpeg generated audio until it exhausted a buffer and reported a disk
error that was not a disk error. Fixed with `-t <video duration>` **on the output** — which is
emphatically *not* MEMEBOT-015's bug returning: that one put `-t` on the audio *input* and let
`-shortest` drag the whole file down to 4 seconds. This bounds the output to the video's own
length, and a test asserts it is `media_duration(video_path)` and not the hook's.

### And the duck graph needs a third input

`build_audio_graph` references `[2:a]` unconditionally — a **second decode of the source** as
the sidechain key. Omitting it fails with `Error binding filtergraph inputs/outputs: Invalid
argument`. An `asplit` of input 0 is the obvious alternative and duck.py measured it **losing
most of the bed** (−13.5 dB against a correct −8.6), so the extra decode is deliberate and the
caller must supply it. Now supplied on the duck path only, with a test.

---

## 4. The vocabulary sweep

Every cross-module vocabulary this pipeline crosses, and its state:

| boundary | ours | theirs | state |
|---|---|---|---|
| `clip_speech.treatment_for` → `duck.TREATMENTS` | `mute-and-replace`, `duck-under` | `mute`, `duck`, `keep` | **mapped + tested** (MEMEBOT-015) |
| `song_library.hook_key` → `outcome_loop` grouper | `s.mp3@1.0-5.0` | `s.mp3@1.0-5.0` | **pinned** (MEMEBOT-015) |
| `caption_parser` tiers → `clip_library` tiers | declared/derived/absent | + `measured` | **superset, tested** |
| **`duck.duck_threshold`** | expected float | **returns `(thr, note)`** | **FIXED this round** |
| **`duck.build_audio_graph`** | expected 1 input | **needs `[2:a]`** | **FIXED this round** |

**Functions whose return is a tuple that reads like a scalar** — the shape to watch, since two
of the five bugs so far were exactly this: `duck.resolve_treatment` (2), `duck.duck_threshold`
(2), `duck.build_audio_graph` (2), `song_library.match` (3). All four now have an arity test.

**The running tally of this failure mode is six**: treatment names, `tag=None`, `DERIVED`
hard-coded, `hook_key`, `duck_threshold`'s arity, and the missing sidechain input. Every one was
a value computed correctly and discarded or mangled at a boundary, and only two of the six
produced any error at all.

---

## A concurrency event worth recording

**BL-855 changed `rank_clips` while I was working**, in the region it had claimed and I had
not. Two of my MEMEBOT-015 tests went red:

```
test_ranks_on_play_count_then_engagement   ['b','c','a'] != ['c','b','a']
test_missing_engagement_sorts_last          ['a','b'] != ['b','a']
```

**I updated my tests to their contract rather than reverting their change.** BL-850 tested 40
ranking terms and only `play_count` held; `engagement_per_follower` is out and ties now break on
`clip_id` — arbitrary and *stable* beats a second signal that looks informative and is not.
`RANK_FIELDS` is now `("play_count",)`. Their reasoning is better than mine was, and the failing
tests were encoding superseded behaviour. Noted in the test docstring so the change is traceable.

The advisory claim showed the conflict up front; I sequenced around it and re-checked.

---

## Verification

| check | result |
|---|---|
| `tests/run_all.py` | **ALL GREEN — 64/64 suites, 2,749 checks** |
| `tests/test_loop_runner.py` | **PASS — 34 checks** (was 20) |
| `place_at_s` applied | **−68.8 → −21.8 dB, a 47 dB step at 28.69 s** |
| hook loops | present at 29.7 / 40.7 / 52.7 / 62.7 s |
| not truncated | 66.73 s source → **66.62 s output** (hook is 4.0 s) |
| duck on real audio | `duck (requested)`, source −15.7 dB |
| threshold is source-derived | **0.16406**, not the 0.125 no-op |
| vocabulary sweep | 5 boundaries pinned, 4 tuple-arity tests added |
| campaigns SHA | **8e02f8d6f6307ae8 — MATCH** |
| `config.json` | parses, 162 keys, untouched |
| spend | **$0.00** — no paid calls |

The full suite came back green — **64/64 suites, 2,749 checks**, `test_filelock.py` included.

---

## Limits

- **One source clip for the duck proof.** `DI8-v0YtJ0V.mp4` is the longest of the first 20
  downloads with audio; depth was not swept across a corpus.
- **Duck DEPTH is not measured here.** I proved the threshold is source-derived and the render
  succeeds. Measuring the actual gain reduction needs the bed level while the source is loud
  versus quiet, which needs a source with silent passages — MEMEBOT-006 measured that on a
  bench and this round did not reproduce it.
- **`place_at` was proved on the MUTE path**, where the bed is the only audio. On the duck path
  the source masks it (measured gap 0.3 dB), so the placement is *applied* there but not
  independently *visible*.
- **The hook loops seamlessly but not musically** — `aloop` repeats the window with no
  crossfade, so the seam is audible if the window does not end on a beat. That is a marking
  problem, not a code one, and every window is still a placeholder.
- **The reported `loop_count` is not passed to ffmpeg** — `aloop=-1` loops indefinitely and the
  output `-t` bounds it. The number is recorded for the record's sake and the two agree
  arithmetically, but nothing enforces that they do.
- **I deleted `scratch/bl838_video/` (349 MB)** — my own probe downloads from an earlier round —
  while diagnosing the disk error. Regenerable, and no other round's data was touched.

---

## Method

Filed a claim; **BL-855 held `loop_runner.py`** for the ranking region only, so I took an mtime
baseline, worked in `_render`/`hook_chain`, and re-checked before writing. All three fixes were
verified by rendering real files and measuring them with `ffmpeg -af volumedetect` over explicit
`atrim` windows, not by reading the filter string. The duck source came from the 61 clips in
`memebot/meme/downloads/`, which carry real audio — 12 of the first 12 checked. The vocabulary
sweep walked every public function in `duck`, `clip_speech`, `song_library` and `outcome_loop`
with `ast`, flagging those whose returns are tuples. No paid call, no spend, no key read.
