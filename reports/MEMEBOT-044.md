# MEMEBOT-044 — the batch ran end to end, and every finished video is silent

Budget $0.20; **spent $0.0102**. `config.json` and `spend.json` backed up before any paid call.
No credential printed or logged.

**The headline is not the one I expected.** The pipeline works: 12 videos rendered from the
live API, playable, correctly framed, floor held on all 12, 34 run records written with every
required field. And **all 12 have no audio stream at all.** Not the wrong music — no audio
track. That is why ten rounds of audio findings have only ever been computed: there was never
anything to listen to.

---

## `claim.py brief` at round start — and why item 1 is not done

```
BL-849       338 min  clip_library/ …                              ** nothing written yet
BL-867        86 min  clip_library/, scratch/, clip_library.py
MEMEBOT-038   17 min  clip_cuts.py, song_library.py, CLIP_PIPELINE.PY +6
MEMEBOT-039   15 min  scratch/memebot039_*
BL-887        12 min  scratch/bl887_*
MEMEBOT-041   10 min  memebot/meme/tests/*
BL-888         9 min  ig_client.py, RUN.PY, MAIN.PY +6
BL-889         9 min  tools/claim.py, tests/test_claim.py …
BL-890         8 min  docs/claims/*.claims +6                      ** nothing written yet
MEMEBOT-042    6 min  CLIP_PIPELINE.PY, tests/test_matcher_boundary.py +3
MEMEBOT-043    5 min  BACKUP_THESE_6_FILES.md …
BL-891         3 min  CONTROL.PY, RUN.PY, tests/test_headless.py +4
```

**Every file item 1 needs was held for the entire round:**

| Needed for | File | Held by |
|---|---|---|
| the orchestrator | `clippershq/clip_pipeline.py` | MEMEBOT-038, MEMEBOT-042 |
| menu entry | `clippershq/control.py` | BL-891 |
| menu entry | `clippershq/main.py` | BL-888 |
| headless command | `clippershq/run.py` | BL-888, BL-891 |

I waited **20 minutes in two blocks**; at the end MEMEBOT-038 was 38 min old and MEMEBOT-042
27 min, both with work under them. **So the menu entry and headless command are NOT done.**
Editing a file another round is mid-way through is the one thing the claim system exists to
prevent, and BL-891 in particular is working on `test_headless.py` — the exact surface.

**What I did instead needed no write to any held file: I called `run_batch()` from a scratch
harness.** That is the part that actually proves something. My claim covers `scratch/mb044_*`
only and registered **zero conflicts**.

---

## 1. WIRING IT UP FOUND THE FIRST DEFECT

`run_batch()` with its default arguments **cannot run**:

```
TypeError: 'NoneType' object is not callable
  clip_media.retrieve -> env = fetch_clips_page(uid, token)
```

`fetch_clips_page` and `http_get` default to `None`, and `clip_media.retrieve` calls them
unconditionally. **Every existing caller is a test injecting fakes.** The production adapters
exist — `ig_client.IgClient.make_clip_fetch_page()`, and a plain CDN GET — and nothing had
ever assembled them. That is precisely what "no entry point" costs: not a missing menu line, a
never-exercised path.

**`dry_run` does not gate retrieval**, only the render. A dry run still pages the API and still
spends, so there is no free rehearsal of this path. The dollar cap is therefore enforced
*before* entry, not trusted afterwards.

---

## 2. THE BATCH

| | |
|---|---|
| Videos rendered `ok` | **12** |
| Attempted | 17 (5 `failed:render`, retried to the next candidate) |
| Wall clock | **583.5 s** for the batch of 10 (~58 s/video) |
| Cost, pipeline's own count | **$0.0102** (17 calls @ $0.0006) |
| Cost per finished video | **$0.00085** |
| Budget | $0.20 — used **5%** |

### What broke

- **`render FAILED rc=0`.** One render reported failure with **returncode 0** —
  `ambient_bed (skipped: <repo path> not found)`. A failure and a success exit code at the
  same time; the pipeline correctly treated it as a failure and moved to the next candidate,
  but anything trusting the exit code would have shipped it.
- **5 of 17 attempts failed** and were retried. Degrade-and-record worked exactly as the
  docstring promises — no attempt was lost, all 5 have records.

---

## 3. WHAT THE VERIFICATION ACTUALLY FOUND

### The 8-second floor — HOLDS, 12/12

Every video this round clears it. (The verifier also reads 9 historical renders from earlier
rounds; **4 of those are under 8s** — they predate the floor being wired, which is itself the
evidence the floor was needed.)

### The hook — NEVER PLACED, on any of the 12

Not "landed at frame one". **No song matched at all.** Every record reads `song: "."`,
`song_id: ""`, `hook_id: None`, window `0.0-20.0` or `0.0-0.0` — defaults, not a marked hook.

Measured against the live store: of 2,003 library clips, **1,761 PARK (87.9%)**, 229 match
`VISION_RULE`, 13 `FRANCHISE_MOOD`. `run_batch` ranks candidates by `play_count` and **does
not prefer clips that can be scored a song**, so all 10 draws were parked clips. `pick()`
then correctly returns nothing — *"a wrong song is worse than no video"* — and **the render
proceeds anyway, with no music.**

So the hook-placement question this round was meant to settle is still unsettled, for a reason
worth more than the answer: **the production path renders videos that have no song, silently,
and calls them `ok`.**

On the two historical records that do carry a `song_id` + `hook_id`, the stored window matches
**0 of 2** marked windows — consistent with MEMEBOT-036's finding, and not something I could
re-test live because nothing matched.

### The treatment — never determined

`audio_class` is `None` on **34 of 34** records; `treatment` is `keep-original` on all 34.
The recorded reason is honest: *"class UNKNOWN — defaulting to keep: muting a dialogue clip is
unrecoverable."* Music-only clips therefore never mute, because no clip was ever classified.

**And the cause is the headline below**: you cannot classify audio that is not there.

---

## 4. THE HEADLINE — EVERY FINISHED VIDEO IS SILENT

```
$ ffprobe -show_entries stream=index,codec_type,codec_name <output>
index=0
codec_name=h264
codec_type=video
```

One stream. No audio. **All 12 of 12**, confirmed on the files directly, not inferred from the
records.

**The staged source has no audio either** — so this is not the render dropping it.

### Root cause

`clip_media.retrieve()` takes `kind=VIDEO` and **defaults to it**. The DASH manifest parser
builds *both* lists —

```python
"video": [strip(r) for r in reps if r["kind"] == VIDEO],
"audio": [strip(r) for r in reps if r["kind"] == AUDIO],
```

— and `retrieve` picks **one** rendition, of kind `VIDEO`. `clip_pipeline.retrieve_video()`
calls it without `kind`. **The audio representation is parsed and discarded on every clip.**

This is the whole chain in one line: no audio fetched → no audio in the staged source → no
audio in the output → `audio_class` unknowable → treatment defaults to `keep` → and the
"keep-original" it keeps is silence.

It also explains the shape of the last ten rounds. Ducking, bed levels, pumping, hook
attacks — all correct work, all measured against `song_library` and synthetic media, none of
it ever reaching a rendered file, because the rendered file has no audio track to reach.

**I did not fix it.** `clip_media.py` and `clip_pipeline.py` are outside this round's claim and
the latter was held throughout. It is a one-argument change with a real retrieval cost (a
second rendition per clip) and belongs to a round that holds those files.

---

## 5. WHAT THE 12 VIDEOS LOOK LIKE

For the operator to check against while watching. All h264, all `1080` wide, all silent.

| clip (trunc) | dur | resolution | kbps | caption chars | floor |
|---|---:|---|---:|---:|---|
| 2940892612405750801 | 13.23 | 1080 | 2,857 | 39 | HOLDS |
| 3457699377771013847 | 11.57 | 1080 | 6,774 | 85 | HOLDS |
| 3618524478543487669 | 8.10 | 1080 | 3,767 | 120 | HOLDS |
| 3700336049278341456 | 16.10 | 1080 | 2,533 | 115 | HOLDS |
| 3716465589432016475 | 58.57 | 1080 | 3,495 | 120 | HOLDS |
| 3720886649015663691 | 11.17 | 1080 | 3,546 | 119 | HOLDS |
| 3721233920508309740 | 16.77 | 1080 | 1,443 | 120 | HOLDS |
| 3725435591426091038 | 27.50 | 1080 | 1,653 | 117 | HOLDS |
| 3837759588729845635 | 16.10 | 1080 | 1,900 | 118 | HOLDS |
| 3898520032929759070 | 58.93 | 1080 | 4,028 | 113 | HOLDS |
| 3923023365239161294 | 79.63 | 1080 | 3,311 | 119 | HOLDS |
| 3928326874557705008 | 25.40 | 1080 | 2,800 | 120 | HOLDS |

**Audio level: not measurable — there is no audio stream.**

Two things to note while watching: durations run to **79.6 s**, far past a reel's useful
length and with no upper bound anywhere in the pipeline; and captions cluster at **120
characters**, which is the truncation limit — 8 of 12 sit exactly on it, so they are being cut.

---

## 6. RUN RECORDS — 34/34 COMPLETE

Every attempt has a record, including the 5 failures and 17 reconcilable `pending` lines.
**All 34 carry every required field**: `clip_id`, `permalink`, `song`, hook window
(`start_sec`/`end_sec`), `treatment`, `output`, `cost_usd`. `outcome_loop` has what it needs
— what it does not yet have is a record where the song is anything but empty.

---

## 7. A METERING DISCREPANCY

| | calls | $ |
|---|---:|---:|
| `run_batch`'s own summary, both runs | **17** | **$0.0102** |
| Written to `spend.json` in that window | **9** | **$0.0054** |
| **Unaccounted** | **8** | **$0.0048** |

Roughly **47% of the round's API calls did not reach the shared ledger.** Stated as a measured
discrepancy rather than a diagnosed mechanism — I did not trace which leg is unmetered, and
`clip_pipeline.py` was held so I could not instrument it.

*I nearly reported this as a total leak.* The ledger stamps local time and the render IDs are
UTC; my first window comparison was two hours out and showed **zero** entries. The finding
survived the correction, smaller.

---

## 8. THE FILE — NEVER TAKEN, SO NOTHING TO RELEASE

Item 6 asked me to release `clip_pipeline.py` immediately afterwards. **I never claimed it.**
My claim was `scratch/mb044_*` only; the four files item 1 needs were held by other rounds the
whole time and I wrote none of them. The queue point is not held by me and was not extended by
this round. My own claim is released.

---

## PROOF

| Required | Result |
|---|---|
| Both entry points live | **NOT DONE** — all four files held for the round; waited 20 min, reported not forced |
| 10 videos with cost and time | **12 rendered ok**, 583.5 s, **$0.0102** (cap $0.20) |
| Hook lands where marked | **Could not be tested** — no song matched on any clip; 87.9% of the library parks |
| Treatment matches class | **Not exercised** — `audio_class` None on 34/34, because there is no audio |
| Floor holds on real output | **12/12 HOLD** |
| Run records written | **34/34 complete**, all required fields |
| Suites | **ALL GREEN — 96/96 suites, 4,009 checks** (443 s) |
| Campaigns byte-identical | `8e02f8d6f6307ae8` — **MATCH** |
| config.json | parses, 162 keys, 5 campaigns |

---

### Method / limits

- Library figures read through `read_snapshot` (BL-849/BL-867 are appending).
- The verifier reads 21 rendered files, 12 from this round and 9 historical; every per-round
  number above is filtered to this round's render IDs.
- `run_batch` was **called, not modified**. No held file was written.
- The silent-audio finding is confirmed on the output files *and* the staged sources, and
  traced to `kind=VIDEO` in `clip_media.retrieve` by reading the code — I did not fix it or
  re-run with `kind=AUDIO` to prove the fix works.
- Caption fit is reported as character count against the truncation limit, not as a rendered
  overflow measurement; I did not inspect frames.
