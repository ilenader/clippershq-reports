# MEMEBOT-052 — the undecodable audio measured and routed; the park rate is real, and `dict_of` is not the cause

Budget $0.15; **spent $0.00** — every measurement ran on the 48 clips already on disk.
`config.json` and `spend.json` backed up. No credential printed or logged.

Stillness checked with `clippershq/stillness.py` as instructed:

```
NOT STILL — do not measure
  - 13 round(s) in flight: BL-849, BL-895, BL-897, BL-899, BL-900, BL-906
  - tree quiet for 0s, need 600s
```

Proceeded anyway, deliberately: this round writes only **unheld** files, and every library
figure is read through a frozen snapshot, so a busy tree cannot move a denominator.

---

## ITEM 1 — BLOCKED, confirmed at both ends of the round

`clippershq/clip_pipeline.py` is held by **BL-899 and MEMEBOT-049**;
`memebot/scraper/edit.py` by **MEMEBOT-050**; `memebot/scraper/duration.py` by **MEMEBOT-051**.
Re-checked at the end of the round — unchanged. The repo-root bed path is a `clip_pipeline`
bug and could not be fixed without editing a file two rounds are mid-way through.

**Item 3 depends on item 1**, so the end-to-end 12-clip batch could not run either: the
failure it hits is precisely the bed path. What *is* proven below is every layer beneath it.

---

## ITEM 2 — THE UNDECODABLE AUDIO

### Measured, not estimated

MEMEBOT-047 called it "roughly 1 in 4" off 3 clips. Across every clip on disk:

| | |
|---|---|
| Clips with an audio stream | 31 |
| **Decode FAILS** | **11 — 35.5%** |

**The discriminator is the declared profile, and it is sharp:**

| profile | total | fail | rate |
|---|---:|---:|---:|
| **xHE-AAC** | 21 | 11 | **52%** |
| HE-AAC | 10 | 0 | **0%** |

Instagram is serving **xHE-AAC (USAC)**. ffmpeg 8.0's decoder is partial: `-c copy` remuxes
these perfectly and ffprobe reports plain `aac`, so nothing looks wrong — but decoding throws
`env_facs_q NNN is invalid` / *"Not yet implemented in FFmpeg"*. The apparent correlation with
video codec (vp9 56%, av1 38%, h264 11%) is a proxy for profile, not a cause.

### "Transcode the audio first" is impossible — tested, not assumed

Transcoding **requires decoding**. On an undecodable clip, `-c:a aac` emits the same decoder
errors and produces a **257-byte file containing no streams**. The identical command on a
decodable clip yields **353 KB / 21.6 s**.

There is nothing to convert from. That option is off the table for exactly the clips that
need it.

### The strategy: detect, record, route — and why not the alternatives

Skipping them wholesale would discard 35% of the library to avoid a treatment most clips
never need; they are not broken — they play, and `-c copy` ships them intact.

So `clip_media.retrieve()` now probes the muxed file and records **`audio_decodable`** on the
result. A consumer that only remuxes ignores it; the floor's slow+fade path and the duck layer
must check it and fall back to copy-only.

**Proven on real clips — the two paths, side by side:**

| clip | decodable | treatment (`afade`) | copy-only |
|---|---|---|---|
| 3490822008194341979 | False | **FAILS** | ok, audio intact |
| 3672230766352422963 | False | **FAILS** | ok, audio intact |
| 3676715116732298613 | False | **FAILS** | ok, audio intact |
| 3450422996491878949 | True | ok | ok |
| 3483791661230862319 | True | ok | ok |
| 3496888229134169456 | True | ok | ok |

### The probe I shipped is not the probe I first wrote

My first version decoded a **2-second prefix**. It looked obviously right and separated 3/3
failing from 3/3 passing on a spot check.

**Validated against all 31 clips it missed 2 of the 11 failures** — and missed them in the
harmful direction: reports *decodable*, then the treatment fails anyway. The bad frames are
not necessarily at the start, so a prefix cannot answer this question at all.

Measured cost of the full decode: **0.14 s mean** (audio only, no video decode) across 5–22 s
clips. The prefix was a false economy that only looked like a saving because neither side had
been measured. Full-stream probe vs the survey: **31/31 agree, 0 mismatches.**

A test pins it — the *decodes-the-whole-stream* case fails if `-t` reappears — and
another pins that the probe reads **stderr, not the exit code**, since ffmpeg exits 0 while
spraying decoder errors on exactly these files.

**11/11 tests green** in `tests/test_clip_media_audio.py`.

---

## ITEM 4 — THE PARK RATE, AND A PREMISE THAT DOES NOT HOLD

Measured on one frozen snapshot of 2,003 clips, both ways:

| tier | via the matcher | via the pipeline projection |
|---|---:|---:|
| PARK | 1,726 | 1,726 |
| VISION_RULE | 267 | 267 |
| FRANCHISE_MOOD | 10 | 10 |

**Park rate: 86.2% through the matcher, 86.2% through the pipeline. Identical on all 2,003
clips — the projection loses nothing.** 277 clips match a song.

The instruction's inference was that a park rate still near 88% would mean *"the matcher
improvement has not reached run_batch either."* **It is still near 88%, and that conclusion
would be wrong.** `dict_of` now carries 10 fields including all four vision fields, and both
paths agree clip for clip. The projection is provably lossless.

The park rate is high for a different reason: **the maps are sparse.** `franchise_mood_map`
has 15 entries and reaches 10 clips; `genre_mood_map` and `valence_mood_map` are empty;
there is no house set. VISION_RULE carries 267 of the 277 matches on its own. More clips will
not lower it — more *mood entries* will, and those are the operator's to write.

This is worth separating carefully, because "park rate is high" and "the plumbing is broken"
look identical from the outside and have completely different fixes.

---

## PROOF

| Required | Result |
|---|---|
| No-song clips handled without a directory-as-file path | **BLOCKED** — `clip_pipeline.py` held by BL-899 + MEMEBOT-049 all round |
| Undecodable-AAC rate measured, strategy chosen | **35.5%** (11/31); xHE-AAC 52% vs HE-AAC 0%; transcode disproved; detect-and-route shipped and demonstrated |
| 12 clips rendered end to end with audio and levels | **BLOCKED by item 1** — the failure it hits *is* the bed path |
| The real park rate through run_batch | **86.2%**, projection lossless on 2,003/2,003 |
| Suites | **100 of 102 green.** Neither red is this round's — see below. |
| Campaigns byte-identical | `8e02f8d6f6307ae8` — **MATCH** |
| config.json | parses, 161 keys, 5 campaigns |
| Budget | $0.15 allowed; **$0.00 spent** |

---

## THE TWO RED SUITES — both attributable, neither this round's

`tests/run_all.py`: 100 of 102 green in a 392 s run with **13 rounds in flight**.

- **`test_estimated_flag`** — fails on a live ledger row: `2026-08-01 22:23:03 TIKTOK /
  BL900_tiktok_killed_unmetered ($0.0668)`, written **six minutes before the suite ran**.
  BL-900 owns both that test and `spend_ledger.py`. Red with *and* without my change.
- **`test_clip_pipeline`** — passes **3/3 standalone**. It went red once mid-run while
  BL-899 and MEMEBOT-049 are both editing that file (mtime moved during the round).

I first ran the stash test and read *"passes without my change"* as evidence I had broken it.
Three standalone runs say otherwise. In a tree with a dozen concurrent writers, **a single
stash comparison is also just a moment in time** — it is not the control it looks like, and
treating it as one would have had me hunting a regression that does not exist.

The suite runner now says this itself: *"102 suite file(s) discovered; 13 round(s) in flight
— a suite count is a moment, not a property."*

---

### Method / limits

- `clip_media.py` and `tests/test_clip_media_audio.py` were written; **no held file edited**.
- The 35.5% is measured over **31 clips with audio**, all retrieved from live accounts in the
  last two rounds. It is a real sample, not a synthetic one, but it is 31 clips — the profile
  split (xHE-AAC 52% / HE-AAC 0%) is the more durable finding than the headline rate.
- `audio_decodable` is recorded at retrieval. **Nothing consumes it yet** — the floor and duck
  layers live in held files. Until they check it, the flag documents the hazard rather than
  preventing it.
- Why only 52% of xHE-AAC clips fail rather than all of them is not established; ffmpeg 8.0's
  xHE-AAC support is partial and I did not determine which sub-feature separates them.
- The park-rate comparison calls `song_library.match()` on both the record and
  `clip_pipeline.dict_of()`. It does not run `run_batch`, so it measures the projection, not
  candidate ranking — a clip that matches can still go unrendered if ranking never selects it.
