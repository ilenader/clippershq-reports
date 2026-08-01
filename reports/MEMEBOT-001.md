# MEMEBOT-001 — It is **two pipelines, not one**, and the audio answer is the good news: arbitrary audio + a start offset **already works** — in `scraper/edit.py`, which is the half that does not render captions.

**Date:** 2026-08-01 · **Type:** Audit, READ-ONLY · **Spend:** $0.00 · **Paid calls:** 0
Nothing in `./memebot` was modified. Output confined to `scratch/`.

---

## 2. The pipeline — there are two, and they do not meet

`memebot` is not one program. It is two, with separate launchers, separate configs, separate
outputs, and **no code path between them**.

### Pipeline A — `meme/` · the caption renderer · `MAKE_VIDEOS.bat`

```
links.txt (IG reel URLs)                       jobs.txt ("file.mp4 | caption")
        |                                              |
   download.py  --HikerAPI /v2/media/info/by/url-->    |
        |  picks video_versions[max width], fetches CDN (no auth)
        v                                              v
   meme/downloads/<shortcode>.mp4  <---------- source_dir, the ONLY way video enters
        |
   ocr.py      tesseract -> find the existing caption band
   band.py     locate/measure the band geometry
   text.py     lay out the new caption
   reword.py   optional LLM reword
   transforms.py  roll a random fingerprint (zoom/rotate/eq/hue/noise/speed/pitch)
   render.py   ffmpeg: overlay PNG -> rotate -> crop -> scale -> eq/hue/unsharp/noise
        v
   meme/out/<shortcode>_v01.mp4
```

### Pipeline B — `scraper/` · the bulk scraper+editor · `run.bat`

```
scraper/run.py -> scrape.py (profile lists) -> scraper/clips/tiktok/<account>/*.mp4
                                                        |
                                              edit.py  ffmpeg transforms
                                                       + AMBIENT AUDIO BED  <-- item 4 lives here
```

**They share only the fonts directory.** Pipeline A never reads `scraper/clips/`; pipeline B
never renders a caption. `MAKE_VIDEOS.bat` says so in its own header: *"The separate run.bat
launches the scraper — leave that one alone."*

---

## 4. Audio — the most important answer

**Short version: the capability you need exists and is already tested. It is in the wrong half,
and it picks its file at random.**

### `scraper/edit.py` — has real external-audio mixing

From the live ffmpeg construction (`edit.py:1020-1063`):

```python
cmd += ["-stream_loop", "-1"]                      # short audio loops to cover the clip
if amb_start_offset > 0.0:
    cmd += ["-ss", f"{amb_start_offset:.3f}"]      # <-- START OFFSET, input-side seek
cmd += ["-i", str(amb_file_path)]                  # <-- ARBITRARY EXTERNAL AUDIO FILE
...
fc = ("[0:a]{main_chain},aresample=44100[a0];"
      "[1:a]volume={amb_volume_db}dB,aresample=44100{fade_chain}[a1];"
      "[a0][a1]amix=inputs=2:duration=first:dropout_transition=0[a_out]")
cmd += ["-filter_complex", fc, "-map", "0:v", "-map", "[a_out]", ..., "-shortest"]
```

Everything the integration needs is present:

| requirement | status |
|---|---|
| accept an **arbitrary audio file** | **YES** — any path, probed with ffprobe |
| **start offset** | **YES** — `-ss` before `-i`, input-side seek |
| **end offset** | **implicit only** — `amix duration=first` + `-shortest` trim to the video |
| audio shorter than the clip | handled — `-stream_loop -1` |
| source clip has **no** audio track | handled — `source_has_audio()` → single-input `[1:a]…[a_out]` |
| volume, fade in/out | present, config-driven, with a relative-to-source loudness mode |
| picking a **specific** file | **NO — `pick_ambient_file(folder, rng)` chooses at RANDOM** |

There is even a `_find_loudest_window_start()` that scans a long track in windows via `astats`
and seeks into its loudest section — which is a crude version of the hook-selection this repo
has been building, already written.

### `meme/render.py` — has none of it, deliberately

`grep -c ambient` → **`render.py` 0, `transforms.py` 0**. Its audio handling is:

```python
cmd += ["-c:a", "aac", "-b:a", "128k"]     # re-encode the SOURCE audio
if tx.get("af"): cmd += ["-af", tx["af"]]  # pitch / tempo / EQ / volume on that same audio
```

and in `edit.py`'s non-ambient branch, `-c:a copy` when no filter is rolled.

**This is a decision, not an omission.** `meme/config.yaml:47`:

> `# NOTE: no ambient_bed here -- memes keep their own audio.`

### What would need to change

Three things, all small, none structural:

1. **Move or import the ambient block into `meme/render.py`.** ~40 lines of `filter_complex`
   assembly that already exist and are exercised by `scraper/tests/`.
2. **Replace `pick_ambient_file(folder, rng)` with a caller-supplied path.** One parameter.
   The random pick is the only thing standing between this and a chosen sound.
3. **Add an explicit end offset.** Today the audio is trimmed by the video's length. A job
   saying "use 12.4 s → 27.9 s of this track" needs either `-t` on the second input or
   `atrim=start=…:end=…` in the chain. `-ss` already handles the start.

**Nothing about the mixer needs rethinking.** It already survives short audio, missing source
audio, loudness matching and fades.

---

## 1. What is actually there — 3.6 GB, of which **source is 0.01%**

| | size | version-control? |
|---|---:|---|
| `scraper/clips/tiktok/` — 11 scraped account folders | **3.4 GB** | **never** |
| `scraper/clips/diag/` | 68 MB | never |
| `meme/out/` — 52 rendered videos | 89 MB | never |
| `meme/downloads/` | 64 MB | never |
| `meme/review/`, `meme/data/` | 4.8 MB | `data/` yes (emoji + wordlist) |
| `scraper/fonts/` | 1.4 MB | one .ttf, already whitelisted |
| **Python source — 19 files** | **~9,900 lines** | **yes** |
| docs / `.bat` / findings `.txt` | ~150 KB | yes |

**Its own `.gitignore` is already correct** — it excludes `clips/`, `meme/downloads/`,
`meme/out/`, `*.log`, `.venv/`, `meme/jobs.txt`, `meme/links.txt` and the ambient sounds folder
while whitelisting `Montserrat-Bold.ttf` and `.gitkeep`. Its own git has **992 loose objects,
0 bytes packed**.

**So the 3.5 GB is not in its history and never was.** Ignoring `memebot/` from the parent repo
was still the right call — the risk was `wip_commit.py` sweeping the working tree, not the
child repo's index.

The largest source files: `meme/cli.py` 1,733 · `meme/ocr.py` 1,691 · `scraper/edit.py` 1,464 ·
`meme/band.py` 923 · `meme/render.py` 794 · `scraper/scrape.py` 586 · `scraper/run.py` 506.

---

## 3. How it is invoked — and the exact input contract

**`meme/cli.py`** — argparse, the real entry point behind `MAKE_VIDEOS.bat`:

```
--auto              render everything already in source_dir
--jobs [PATH]       the job list
--links [PATH]      URLs to download first (default meme/links.txt)
--variants N        N fingerprinted outputs per input
--captions / --reword / --preview / --read / --dry-run / --force-rerender
--config PATH       default meme/config.yaml
```

**The job contract is one line of text** (`meme/jobs.py`):

```
filename.mp4 | caption text to burn
```

with three hard rules, each enforced with its own error message: **a bare filename, never a
path** (no `/`, `\`, or `..`); **URLs rejected outright** — *"URLs are not supported. This tool
renders local files"*; and the file must already sit in `source_dir`.

**This is the join point, and it is the narrowest part of the system.** The contract carries
exactly **two** fields — a filename and a caption string. There is nowhere to put a clip id, an
audio path, or an offset. Any integration either extends this parser or bypasses it.

`--links` is the other door: one URL per line, resolved by `download.py` through
**HikerAPI `/v2/media/info/by/url`** — the same vendor this repo already pays for.

---

## 5. What it already knows about a clip — almost nothing

**Consumed per job: `file` (str), `text` (str), `line_no` (int).** That is the entire external
metadata surface.

Everything else it derives itself, in-process, and discards:

- `download.py` receives the full HikerAPI media payload and keeps **the video URL and the
  shortcode**. Caption, play count, taken_at, owner — all present in that response, all dropped.
- `ocr.py` / `band.py` derive band geometry, existing caption text, emoji identity — held in
  memory for the render, never written.

**Overlap with the clip library's 61 exported columns: effectively zero today.** But
`download.py` is parsing the *same* HikerAPI response shape the library is built from, so the
fields are one assignment away rather than a new fetch.

---

## 6. The encoding chain

Both renderers converge on the same profile (`render.py:630-644`, `edit.py:1060-1074`):

```
-c:v libx264  -preset fast  -crf 23  -g 60  -pix_fmt yuv420p
-c:a aac  -b:a 128k
-movflags +faststart
-map_metadata -1  -fflags +bitexact  -flags:v +bitexact
-metadata encoder=  -metadata:s:v encoder=  -metadata:s:a encoder=
```

**Metadata stripping is thorough**: `-map_metadata -1` drops every container tag, `+bitexact`
suppresses the encoder version stamp libx264/ffmpeg would otherwise write, and the three
`encoder=` overrides blank the per-stream tags that survive that.

**Resolution is preserved, not normalised.** `render.py:583` splices
`scale=<even_down(w)>:<even_down(h)>:flags=lanczos` after the crop purely to undo zoom and force
even dimensions (`yuv420p` rejects odd ones). There is no 1080×1920 target.

**Against platform requirements:** H.264 High/yuv420p, AAC, MP4, faststart — all correct for
both Instagram and TikTok. **Bitrate is CRF-driven, not capped**, so a high-motion clip can
exceed IG's recommended ceiling and be re-encoded on upload. No explicit `-r` framerate
normalisation either — source fps passes through.

---

## 7. State — there is none, but the filename is a usable key

**No database. No manifest. No log of what was processed.** The only persistence is the output
filename:

```
meme/out/C5q7V4lCUEx_v01.mp4
         ^^^^^^^^^^^ the Instagram shortcode, from download.py
```

`_dst_for()` builds `{source_stem}_v{NN}.mp4`, and the run skips a job when that file exists —
so idempotence is filesystem-based.

**Can it tell you which clip produced which video? For pipeline A, yes** — the shortcode
survives into the filename, and the clip library stores `permalink`
(`instagram.com/reel/<code>/`), so the join is exact. **For pipeline B, no** — scraper outputs
are per-account folders with no link back to a library row.

**What is not recorded anywhere:** which transform values were rolled (they are printed to
console and lost), which caption was burned, which audio was mixed, when. A rendered file cannot
be traced to its inputs beyond the shortcode.

---

## 8. Fragility — cleaner than expected

| checked | result |
|---|---|
| absolute paths / other machines (`C:\`, `/home/`, `/Users/`) | **none** — `ROOT = Path(__file__).resolve().parent` throughout |
| secrets in source | **none** — HikerAPI token from `HIKERAPI_TOKEN` env var, with a `_redact()` on every error string |
| config keys read by nothing | **3 of 85** in `meme/config.yaml` (`angle_max`, `angle_min`, `prefer_quality`); **4 of 66** in `scraper/config.yaml` (`angle_max`, `angle_min`, `default_template`, `templates_path`) |
| computed-then-discarded | the HikerAPI payload (§5) and the rolled transform values (§7) |
| external binaries | **ffmpeg, ffprobe, tesseract** — all assumed on PATH, none version-pinned |
| fresh install | no `requirements.txt`, no `pyproject.toml`, no lockfile **anywhere** |

**The one live dead-knob:** `ambient_bed.enabled: false`, and
`scraper/sounds/ambient/` contains only `.gitkeep` and `README.md`. **The entire audio-mixing
subsystem — the thing this integration depends on — has never run on real audio.** It is
tested (`scraper/tests/`) but unexercised in production.

Missing dependency manifest is the real fresh-install risk: 19 modules importing `yaml`,
`requests`, `PIL`, `pytesseract` and more, with nothing declaring them.

---

## 9. The integration verdict — smallest change

The system already does 90% of what is needed. The gap is a **contract**, not a capability.

**Extend `meme/jobs.py` from two fields to five**, keeping the current line format as the
one-field default so nothing existing breaks:

```
file.mp4 | caption | audio=sounds/hook.mp3 | audio_start=12.4 | audio_end=27.9
```

Then, in order of size:

1. **`jobs.py`** — parse the extra `key=value` segments; keep the 2-field form valid. **~30 lines.**
2. **`render.py`** — import the ambient `filter_complex` block from `edit.py` rather than
   copying it, and take `audio_path` / `audio_start` / `audio_end` from the job instead of
   `pick_ambient_file(folder, rng)`. **~40 lines moved, one parameter changed.**
3. **End offset** — `-t` on the audio input, or `atrim`. **~5 lines.**
4. **A render record** — one JSONL line per output: `{output, source_clip_id, permalink,
   caption, audio_path, audio_start, audio_end, transform_values, rendered_at}`. This is the
   only genuinely new artefact, and it is what makes the loop auditable. **~20 lines.**

**~95 lines total, no new dependency, no architectural change.**

**The clip library already holds the other side of the join.** It stores `clip_pk`,
`account_user_id`, `permalink` and `media_renditions`, and MEMEBOT's `download.py` fetches from
the same HikerAPI endpoint — so "find clip → qualify → choose sound → make video" needs the
library to emit a job line, not a new fetch path.

**The sequencing risk worth naming:** the audio mixer has never processed a real file
(§8). Before wiring anything, drop one real track into `scraper/sounds/ambient/`, set
`enabled: true`, and run pipeline B once. If the mixer is broken, that is a much cheaper place
to find out.

---

## Limits

- **I read the source, not the runtime.** Neither pipeline was executed — no video was rendered
  and no ffmpeg command was run. The chains in §4 and §6 are read from the code that builds
  `cmd`, which is unambiguous, but ffmpeg's actual behaviour on a real clip is unverified here.
- **The dead-knob sweep is a substring match** over the two YAML files against all source; a key
  read via a computed name would read as dead. `angle_min`/`angle_max` appear in both configs
  and may be consumed by a rotation helper under another name.
- **`meme/ocr.py` (1,691 lines) and `meme/band.py` (923) were not read in depth** — they are the
  caption-detection half and do not touch audio, the job contract, or encoding.
- **Pipeline B's `run.py`/`scrape.py` were skimmed**, not traced. The scraper's own input
  contract (profile lists) is outside the integration surface.
- **The 3.4 GB TikTok corpus was not inventoried** beyond directory sizes and account count.
- **Instagram/TikTok "requirements" are the published container/codec guidance**, not a tested
  upload. I did not upload anything.

---

## Method

Filed an in-flight claim (`tools/claim.py`, no path conflicts with the two live rounds).
Measured sizes with `du`, counted source with `wc -l` over every non-test, non-`__pycache__`
`.py`. Traced both pipelines by reading `meme/cli.py`, `jobs.py`, `download.py`, `render.py`,
`transforms.py` and `scraper/edit.py`, `run.py` directly — the README was read but not relied
on, and §2's structure comes from the argparse table and the ffmpeg `cmd` builders. The audio
finding is read verbatim from `edit.py:1020-1063`. Fragility sweeps were regex over all source
for absolute paths and credential patterns, plus a YAML-key-vs-source membership test. `git -C`
used read-only against memebot's own history. **Nothing in `./memebot` was created, modified or
deleted.**
