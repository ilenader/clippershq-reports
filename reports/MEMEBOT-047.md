# MEMEBOT-047 — the audio is back: 0/12 → 12/12 clips retrieved with sound

Budget $0.15. `config.json` and `spend.json` backed up before any paid call. No credential
printed or logged.

**The fix landed and is proven on live media.** Every clip retrieved this round carries an AAC
audio stream; before this round every one was video-only. What is *not* proven end-to-end is
the finished render, and the reason is worth as much as the fix — see §4.

---

## `claim.py brief` at round start

```
BL-849       391 min  clip_library.py, clip_library/, scratch/bl849_label.py
MEMEBOT-039   68 min  scratch/memebot039_*
BL-895        29 min  clip_library/, scratch/
BL-896        24 min  clip_vision.py, clip_library.py, scratch/bl896_tokens.py +4
MEMEBOT-046   19 min  memebot/scraper/EDIT.PY, config.yaml, song_loudness.py +3
BL-898        16 min  dashboard/server.py, test_dashboard.py, clip_cuts.py +6
BL-897        16 min  clip_library/, tools/claim.py, tests/test_claim.py +3
BL-899        12 min  clippershq/CLIP_PIPELINE.PY, test_clip_pipeline_gate.py +2
BL-900        11 min  spend_ledger.py, repost_finder.py, run_status.py +6
MEMEBOT-046H   7 min  scratch/mb046h_*
BL-901         4 min  test_quality_score.py, verify_claims.py, test_claims_manifest.py +1
BL-902         1 min  spend.json, scratch/bl902_*                    ** nothing written yet
```

**The block is the inverse of what was assumed.** The instruction anticipated
`clip_pipeline.py` blocking item 1. It does not — item 1 lives in `clip_media.py`, which was
**free**. What `clip_pipeline.py` (BL-899) blocks is **items 3, 4 and 5**, all of which are
`run_batch` internals.

| Item | Lives in | Status |
|---|---|---|
| 1 — fetch + mux the audio | `clippershq/clip_media.py` | **FREE → DONE** |
| 2 — silent output must fail | `memebot/scraper/duration.py` | **FREE → DONE** |
| 3 — `run_batch` defaults | `clippershq/clip_pipeline.py` | **BLOCKED** (BL-899) |
| 4 — `dry_run` gates retrieval | `clippershq/clip_pipeline.py` | **BLOCKED** (BL-899) |
| 5 — trust output not exit code | `clippershq/clip_pipeline.py` | **BLOCKED** (BL-899) |
| 6 — re-render 12 | called, not written | **DONE, with a caveat** |

One advisory accepted: BL-895 claims `scratch/` broadly; my files are `scratch/mb047_*`.

---

## 1. THE FIX — `retrieve()` now returns video WITH its sound

`clip_media.retrieve()` took `kind=VIDEO` and **defaulted to it**. `parse_renditions` correctly
built *both* lists; `retrieve` picked one rendition, of `kind`, and the audio representation
was parsed and discarded on every clip.

**The default moved rather than a new function being added, deliberately.**
`clip_pipeline.retrieve_video()` is the only production caller and it was held by BL-899 all
round. A new `retrieve_av()` would be dead code nobody calls. Changing what `retrieve()`
returns fixes the existing call site **without editing a file another round is mid-way
through** — and "video means video with its sound" is the honest default anyway.
`with_audio=False` restores the old behaviour explicitly.

| | |
|---|---|
| Extra API spend | **none** — the audio rendition is a second CDN GET on a manifest already fetched. Unbilled, one paid call per clip, exactly as before. |
| Mux | `ffmpeg -c copy`, no re-encode — the two tracks come from one manifest and are already aligned |
| Failure modes | reported in `res["audio"]`, never silent: `no audio rendition in manifest`, `audio download failed`, `ffmpeg not available`, `mux failed` |

`tests/test_clip_media_audio.py` — **6/6 green**, offline, real ffmpeg mux of real synthesised
media: default retrieve produces an audio stream, both renditions are fetched,
`with_audio=False` restores the old behaviour *and spends no fetch on audio*, a manifest with
no audio says so rather than going quiet, a dead audio URL degrades without losing the video,
and `kind=AUDIO` does not try to mux onto itself.

*My first fixture was wrong and all 6 failed at `ok=False`* — I used `{"items": [...]}` where
the wire shape nests the media under the gql clips-connection edges (`…edges[].node.media`), and
`play_count` is required or `clip_walk._is_media` does not recognise the dict at all. Both
traps were already documented in the module's own self-test.

---

## 2. A SILENT RENDER NOW FAILS LOUDLY

`duration.assert_has_audio()` + `SilentRenderError`, beside `assert_floor` — the module that
already exists to measure properties of the **finished artefact**.

```
probe_audio_streams(path) -> 0 = silent | -1 = unprobeable | n = streams
```

**`-1` rather than `0` on a probe failure, deliberately.** "I could not look" and "I looked and
found nothing" are different, and collapsing them is exactly what let the credential scanner
print PASS after reading zero files (BL-874).

`memebot/scraper/tests/test_duration.py` — **19/19 green**, including the test that explains
why this had to be a *new* check rather than a tightened old one:

> *the silent file passes every older check* — a silent 9-second file clears
> `assert_floor` and `is_healthy_video`, and only `assert_has_audio` catches it.

Same family as MEMEBOT-010's 5.0s truncation and the zero-file scanner. The pattern each time:
**the check that existed answered a narrower question than the one that mattered, and its
silence read as health.**

---

## 3. THE PROOF ON LIVE MEDIA — 12/12

Clips retrieved this round, straight off the live API:

```
staged sources WITH audio : 12 / 12      (MEMEBOT-044: 0 / 12)
```

Every one `aac`, across `av1`, `vp9` and `h264` video. Measured source levels run
**−8.2 to −18.1 dBFS** — real, varied, present.

| clip | src codec | dur | src mean dBFS | out mean dBFS | out dur | audio | floor |
|---|---|---:|---:|---:|---:|---|---|
| 3450422996491878949 | aac | 21.55 | −16.6 | **−16.7** | 21.5 | PRESENT | HOLDS |
| 3483791661230862319 | aac | 15.00 | −17.1 | **−17.1** | 14.97 | PRESENT | HOLDS |
| 3496888229134169456 | aac | 19.41 | −14.7 | **−14.8** | 19.4 | PRESENT | HOLDS |
| 3616453840670917323 | aac | 7.01 | −9.8 | **−10.2** | **8.0** | PRESENT | HOLDS |
| 3623069011230752018 | aac | 6.15 | −11.5 | **−11.9** | **8.0** | PRESENT | HOLDS |
| 3629145006751110009 | aac | 12.49 | −8.2 | **−8.8** | 12.4 | PRESENT | HOLDS |
| 3665688194863942347 | aac | 10.77 | −16.5 | **−16.6** | 10.77 | PRESENT | HOLDS |
| 3448924568930352855 | aac | 5.40 | −18.1 | — | — | rejected (<5.95s) | — |
| 3526816883515201077 | aac | 5.13 | −18.0 | — | — | rejected (<5.95s) | — |
| 3490822008194341979 | aac | 8.03 | — | — | — | **re-encode failed** | — |
| 3586077779226464604 | aac | 8.03 | — | — | — | **re-encode failed** | — |
| 3652694609280160087 | aac | 6.39 | — | — | — | **re-encode failed** | — |

**7 of 7 rendered clips carry audio and hold the 8-second floor.** Two rejects are the floor
working as specified (both under 5.95s). Levels survive the transform within 0.6 dB, and the
two short clips were lifted 7.01s → 8.0s and 6.15s → 8.0s **with their audio intact**.

### The 3 failures are a real limitation, and they are not the mux

The mux succeeded on all 12 — the streams are there. The **re-encode** fails on three:

```
[dec:aac] env_facs_q 252 is invalid
[dec:aac] Error submitting packet to decoder: Not yet implemented in FFmpeg, patches welcome
```

Those clips carry an AAC profile **ffmpeg 8.0 cannot decode** (the "not yet implemented"
message points at xHE-AAC / USAC). `-c copy` remuxes it fine; anything that has to *decode*
the audio — a speed change, a fade, a duck — will fail on roughly **1 in 4 clips**. That is a
new, measurable constraint on the whole audio pipeline and it was invisible while every render
was silent.

---

## 4. THE END-TO-END RENDER DID NOT COMPLETE — and the reason is another correct fix

`run_batch` retrieved all 12 clips successfully and then **every render failed**:

```
render FAILED rc=1: ambient_bed.file='C:\...\clipper finder' was requested and does not exist
```

Not caused by this round. The chain:

1. no song matches the clip (87.9% of the library parks) → `song` resolves to `"."`
2. `clip_pipeline` sets `ambient_bed.file` from that → it becomes **the repo root**
3. MEMEBOT-046's `edit.py` now **REFUSES** rather than rendering, and its own comment says
   why: *"This used to print a warning… a healthy video, exit code 0, and no music in it."*

**MEMEBOT-046 is right.** It converted a silent success into a loud failure — the same
correction this round made twice — and in doing so exposed a pre-existing `clip_pipeline` bug
that had been hidden behind a warning. `ambient_bed.enabled` is already `false` in the live
config, so the path is reached regardless of the toggle.

`clip_pipeline.py` (BL-899) and `edit.py` (MEMEBOT-046) are both held, so the renders in §3
are driven directly through the same ffmpeg transform the 8-second floor uses, on the same
staged sources. That measures the audio honestly; it does **not** exercise captions,
templates, the hook window, or treatment routing.

**Hook window and treatment remain unverified**, for the same reason as MEMEBOT-044: no song
matched any of the 12, so there was no hook to place and no class to route.

---

## 5. ITEMS 3, 4, 5 — BLOCKED, NOT FORCED

All three are `run_batch` internals in `clip_pipeline.py`, held by BL-899 for the whole round.
Confirmed again at the end. Each is small and the diagnosis from MEMEBOT-044 stands:

- **`run_batch` defaults** — `fetch_clips_page`/`http_get` default to `None` and
  `clip_media.retrieve` calls them unconditionally, so the production path raises `TypeError`
  before spending. Every existing caller is a test injecting fakes. *(My harness assembles
  `ig_client.IgClient(...).make_clip_fetch_page()` and a CDN GET — that wiring is the fix,
  and it belongs in `run_batch`'s defaults.)*
- **`dry_run`** gates only the render, so a dry run still pages the API and still pays.
- **Exit code** — a render reported FAILED with `rc=0` in MEMEBOT-044; this round it reported
  `rc=1` correctly, so the defect is intermittent rather than constant.

## 7 — noted, not chased

The ledger stamps **local** time while render IDs are **UTC**; a naive window comparison reads
two hours out and shows zero entries. Residual remains ~8 of 17 calls unaccounted. Not
investigated: `spend_ledger.py` is held by BL-900.

---

## PROOF

| Required | Result |
|---|---|
| ffprobe shows an audio stream on real output | **12/12 staged sources**, 7/7 rendered — was 0/12 |
| A silent render fails loudly | `SilentRenderError`; 19/19 duration tests, incl. silent-passes-every-older-check |
| `run_batch` callable with production defaults | **BLOCKED** — clip_pipeline.py held by BL-899 |
| `dry_run` costing $0.00 | **BLOCKED** — same file |
| 12 clips re-rendered with audio levels | **12 retrieved with audio**, 7 rendered + levels; 2 correctly rejected, 3 undecodable AAC |
| Suites | **99 of 100 green.** The red is `test_clip_pipeline.py` — **not this round**: with my `clip_media.py` change stashed to HEAD the same 2 failures persist. Both are matcher/tier assertions (`'lru_corpus' != 'matched'`), which is BL-899's live edit to that file. |
| Campaigns byte-identical | `8e02f8d6f6307ae8` — **MATCH** |
| config.json | parses, 161 keys, 5 campaigns |
| Budget | $0.15 allowed; **ledger delta $0.0000**, pipeline count ~$0.007 |

---

### Method / limits

- `clip_media.py` and `duration.py` were written; **no held file was edited**. `run_batch` was
  called, not modified.
- The end-to-end render is **not** proven. §3's renders use the floor transform directly, so
  captions, templates, hook placement and treatment routing are untouched by this evidence.
- The undecodable-AAC finding is from 3 clips of 12. The proportion is indicative, not
  measured at scale, and I did not identify the exact profile — only that ffmpeg 8.0 reports
  it unimplemented.
- Audio levels are `volumedetect` mean/peak on the file, not loudness-normalised LUFS.
- The `ambient_bed` diagnosis is read from `edit.py` and the failure text; I did not
  instrument `clip_pipeline` to confirm which line composes the path.
