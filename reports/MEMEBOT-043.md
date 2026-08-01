# MEMEBOT-043: the four flags were already set by another live round — and the renderable count is **18**, not 242, because the pipeline drops the vision fields before the matcher ever sees them

**Date:** 2026-08-01 · **Type:** Measurement + render · **Spend:** **$0.00 · 0 paid calls**
Claim filed via `tools/claim.py`, **6 paths registered individually** with repeated `--write`. `scratch/songs.json` backed up + SHA-verified to `backups/songs.json.20260801_204906.pre_mb043.bak`. `git -C` throughout, no credential printed or committed. Committed at `32de36d`.

Acts on [MEMEBOT-037](MEMEBOT-037.md).

---

## The brief was already being executed by another round

`python tools/claim.py brief` at the start:

```
IN-FLIGHT CLAIMS  (paste into a brief)  2026-08-01 20:47
  BL-849           331 min  clippershq/clip_library.py, clip_library/, scratch/bl849_label.py   ** nothing written yet
  BL-867            79 min  clip_library/, scratch/, clippershq/clip_library.py
  MEMEBOT-036       33 min  memebot/scraper/duration.py, memebot/scraper/edit.py, memebot/scraper/config.yaml +4 more
  MEMEBOT-038       11 min  clippershq/clip_cuts.py, clippershq/song_library.py, clippershq/clip_pipeline.py +6 more
  MEMEBOT-039        8 min  scratch/memebot039_fields.py, scratch/memebot039_guard.py, scratch/memebot039_measure.py +2 more
  MEMEBOT-040        7 min  scratch/songs.json, scratch/memebot040_verify.py, scratch/memebot040_findings.md
  BL-887             5 min  scratch/bl887_*
  MEMEBOT-041        3 min  memebot/meme/tests/test_band.py, memebot/meme/tests/test_transforms.py, memebot/meme/tests/test_reword.py +5 more
  BL-888             3 min  clippershq/ig_client.py, clippershq/run.py, clippershq/main.py +6 more   ** nothing written yet
  BL-889             2 min  tools/claim.py, tests/test_claim.py, scratch/bl889_unparseable.py +1 more   ** nothing written yet
  BL-890             2 min  docs/claims/MEMEBOT-009.claims, docs/claims/MEMEBOT-021.claims, docs/claims/MEMEBOT-025.claims +6 more   ** nothing written yet
```

**MEMEBOT-040 holds `scratch/songs.json`, and its claimed intent is this brief nearly word for word** — *"VERIFY the operator's hand-marked hook windows, THEN enable the four songs… backup songs.json timestamped… report renderable clips… confirm songs.json is on the backup list."* Filed 7 minutes before this round started.

By the time I read the file it had **already flipped all four flags**, at 20:46:19. This is the exact scenario `claim.py` was written for — three rounds once rebuilt the same bulk outcome marker because each read a recommendation and correctly concluded the work was outstanding.

**So I did not re-flip anything.** I verified their write, and delivered the four items nobody else held: the backup-list entry, the loudness measurement, the render, and the count. MEMEBOT-040 has since committed the flags at `e890002`.

### Their flip, independently verified

```
-   "enabled": false,          4 insertions(+), 4 deletions(-)
+   "enabled": true,           nothing else in the diff
```

**Four lines. No window, no mood, no genre, no note, no path, no `measured` block.** Verified key-by-key, not by eye. `validate()` now returns **NO PROBLEMS** — all four "no ENABLED song" complaints cleared, exactly as MEMEBOT-037 predicted.

---

## The renderable count: 242 by the matcher, **18 by the pipeline**

You expected 230, and by the matcher it is now higher — the library is being labelled live by BL-849/BL-867, so the number moved twice while I measured it (234 at 20:52, **242** at 21:14).

| | clips |
|---|---:|
| distinct clips in the library | 2,003 |
| matched a mood *(full library rows)* | **242** — vision 229, franchise 13 |
| **renderable, as the pipeline actually feeds the matcher** | **18** |

Both of your specific claims confirmed, and then some:

| song | mood | hooks | matched | share |
|---|---|---:|---:|---:|
| song04 | hype | 5 | **211** | **87.2%** |
| song03 | warm | 5 | 28 | 11.6% |
| song01 | melancholy | 5 | 3 | 1.2% |
| **song02** | triumphant | **6** | **0** | **0.0%** |

**song02 still has the most windows and matches nothing.** Six windows — the largest block of the evening's work — and no clip in the library routes to `triumphant`.

### Why 18 and not 242

`clip_pipeline.dict_of()` is what the render loop hands to the matcher, and it builds a **five-field** mapping:

```python
out = {"clip_id": ..., "franchise": ..., "content_genre": ...,
       "valence_text": ..., "duration_s": ...}
```

No `vision_scene`, no `vision_on_screen_text`, no `vision_beats`. The matcher's **tier 0 — the vision rules — cannot fire inside the pipeline at all.** Measured both ways over the same 2,003 clips:

```
  full library rows      : PARK 1761, VISION_RULE 229, FRANCHISE 13  ->  242 renderable
  through dict_of()      : PARK 1985,                  FRANCHISE 18  ->   18 renderable
  vision matches lost at the boundary: 224
```

`tests/test_matcher_boundary.py` fails on exactly this, in its own words: *"vision_scene is dropped: 0 of 221 vision matches could reach a render"*.

**This is known and owned.** MEMEBOT-039's claim reads *"BLOCKED ON THE WRITE… `dict_of()` must carry the vision fields, but MEMEBOT-038 claimed `clippershq/clip_pipeline.py` two minutes before this round"* — it has the one-line patch ready and is deliberately not applying it under another round's claim. I did not apply it either, for the same reason.

**So enabling the songs moved the ceiling from 0 to 242, and the floor from 0 to 18. One line closes the gap.**

---

## The 21 windows measured, 9 orphans purged

One local ffmpeg pass each, **$0**, 18 seconds total. Cache **13 → 25** rows.

**The brief said 13 orphans; it is 9.** Of the 13 rows, **4 are legitimate whole-file rows** (one per song — they are where each song's `measured` block comes from) and only the **9 span-keyed rows** pointed at placeholder windows that no longer exist. Purging all 13 would have thrown away four valid measurements.

```
  purged (span rows keyed to spans that are gone):
    song01@0.000-18.900   song01@20.000-25.000  song01@60.000-65.000
    song01@110.000-116.000  song02@30.000-36.000  song03@45.000-51.000
    song04@15.000-21.000  song04@55.000-61.000  song04@95.000-101.000
  kept (whole-file rows, legitimate):  song01, song02, song03, song04
```

### The spread is worse than MEMEBOT-025 measured, and that is the point

| song | windows | gain range | **spread** | whole-file gain |
|---|---:|---|---:|---:|
| **song01** | 5 | −5.98 … **+3.49** dB | **9.47 dB** | −4.47 |
| song04 | 5 | −5.62 … −1.23 dB | 4.39 dB | −4.53 |
| song03 | 5 | −5.48 … −1.35 dB | 4.13 dB | −3.64 |
| song02 | 6 | −3.24 … −1.45 dB | 1.79 dB | −1.90 |

MEMEBOT-025 measured 5.9 dB apart within one song. **On the real windows it is 9.47 dB.**

The sharpest single case: **song01 h1** (`0.427–18.701`, *"slow build works on anything"*) measures **−17.76 LUFS** and needs **+3.49 dB** to reach −14. The whole-file number says **−4.47 dB**. Using the per-file gain would place that window **7.96 dB too quiet** — the "slow build" would be nearly inaudible. Across all 21 windows the mean divergence from the per-file number is **1.61 dB**, the max **7.96 dB**.

**These measurements are stored and not yet consumed.** `edit.py` computes its own bed level (it targeted −18.4 dBFS solo on the render below) and never reads `scratch/song_loudness.json` — the only mention of `song_loudness` in `edit.py` is a comment. Wiring them together is a separate change in a file MEMEBOT-036 holds.

---

## One video, rendered end to end from a real marked window

```
SELECTED by the shipped pick() for mood 'hype':
  song  : song04   hook: h1  13.769-29.369 s (15.600 s)
  note  : "this one is just the warm up start of the song ... a litl some some"
  marked: 2026-08-01T20:28:15 by hand via hookmark

SOURCE: C_p4DufCsq0.mp4 (12.07 s)   audio_class=music-only   treatment=mute-and-replace

  ambient_bed  song04.mp3 @ -3.6dB [solo (class music-only, target -18.4dBFS)],
               start=13.8s [explicit-window] (always)
  audio_treat  mute (routed on class music-only)
  RESULT edit: rendered=1 skipped=0 errors=0 status=ok

OUTPUT: scratch/mb043/clips/instagram/mb043proof/final/white_frame/C_p4DufCsq0.mp4
        9.87 s, 2,814 KB, -16.76 LUFS-I   HEALTHY
```

`[explicit-window]` is the proof: `edit.py` took `start_sec`/`end_sec` from the hand-marked hook rather than any heuristic. The music-only source correctly muted and was replaced by the marked window.

### The first attempt rendered a healthy video with no music in it

```
  ambient_bed  (skipped: memebot/scratch/song04.mp3 not found)
  RESULT edit: rendered=1 skipped=0 errors=0 status=ok        <- returncode 0
```

`edit.py` runs with `cwd=memebot/scraper`, so a repo-relative song path resolves against `memebot/` and misses. It **skips the bed, exits 0, and produces a healthy file** — a render that "worked" and proved nothing. Fixed by passing an absolute path, and the script now asserts on the `ambient_bed` line rather than the return code. `edit.py`'s own docstring already warns *"PASS AN ABSOLUTE PATH. It is the only form with one meaning."* — this is a re-discovery of a documented trap, not a new one.

**The render is not in `memebot/runs.jsonl`.** The ledger is written by `run_batch()`, which retrieves clip media over the paid IG API; this round had no paid calls, so it went through `edit.py` directly. That means this render contributes no `bias_map()` evidence — correct for a proof, and worth knowing before anyone counts it as a posted video.

---

## `scratch/songs.json` is now entry 9 on the backup list

Added with the size, what is lost, and why it belongs among files that are otherwise all gitignored: it is the only record of half an hour of listening, and BL-690 measured automatic drop detection at **100% fabrication**, so a lost window cannot be recomputed — only re-heard.

I also fixed two things that would have made the entry ineffective:

* the **copy script** listed files 1–6 and 8 explicitly; `scratch\songs.json` is now in the loop.
* the **verify loop** maps flattened filenames back to their source, and knew only about `runs.jsonl`. It would have reported **`songs.json  SOURCE GONE`** for a file that was present and correct. Now a `switch` handles both.

---

## Proof

| claim | evidence |
|---|---|
| four flags set, nothing else | `git diff` = 4 insertions, 4 deletions, all `enabled`; committed by MEMEBOT-040 at `e890002` |
| `validate()` clean | **NO PROBLEMS** (was 4) |
| renderable + distribution | **242** matcher / **18** pipeline; song04 87.2%, song02 **0** with 6 hooks |
| songs.json on the backup list | entry 9 in `BACKUP_THESE_6_FILES.md`, copy script + verify loop updated |
| 21 measured, orphans purged | cache 13 → 25; **9** span orphans purged, 4 whole-file rows kept |
| one video rendered | 9.87 s, 2,814 KB, −16.76 LUFS-I, `[explicit-window]`, $0 |
| campaigns SHA | **8e02f8d6f6307ae8 — MATCH** |
| config | valid JSON, 162 top-level keys |
| suites | **94 of 96 green.** The two reds are `test_matcher_boundary.py` (the `dict_of` gap above, owned by MEMEBOT-039) and `test_funnel.py` (a missing temp `spend.json` in the crawl-cluster test). Both are in files other live rounds are editing; my only tracked edit is `BACKUP_THESE_6_FILES.md` |

---

## Honest limits

- **I did not do the headline task.** MEMEBOT-040 flipped the four flags two minutes before this round began. Everything here about the flags is verification of someone else's write, not my own work, and if their verification was wrong mine inherits it — though I checked the diff independently and it is four lines.
- **The renderable count moved three times while I measured it** (230 → 234 → 242) because BL-849 and BL-867 are vision-labelling the library right now. Every figure went through `read_snapshot` so numerator and denominator agree with each other, but 242 has a timestamp, not a shelf life.
- **18 is the number that matters and I did not fix it.** `clip_pipeline.py` is held by MEMEBOT-038 mid-render; MEMEBOT-039 has the one-line patch ready and is blocked on the same claim. Applying it here would have moved the input of a six-video measurement while it ran.
- **The render is not a library clip.** The 2,003 library rows are metadata; their permalink codes and the 61 local downloads intersect at **zero**, and fetching library media is a paid call. So the window is proven on a real clip, and the *matcher-to-render* path is proven only as far as `dict_of` allows — which is the 18.
- **Nobody has listened to the rendered video.** It is healthy by duration, size and LUFS. Whether song04's h1 actually works under that clip is exactly the judgement the measurements cannot make.
- **The 21 loudness figures are unconsumed.** They are correct, cached and keyed to the right spans, and `edit.py` still computes its own bed level. Until those meet, the 9.47 dB spread is documented rather than corrected.
- **`test_funnel.py` is red and I did not diagnose it beyond reproducing it.** It fails on a missing temp `spend.json` inside the crawl-cluster test, twice, in different temp directories. It is not mine — I touched no funnel file — but I am reporting it rather than leaving it in a summary line.

---

https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/MEMEBOT-043.md
