# MEMEBOT-036 — an 8-second floor: the rule, the renders, and the check that makes it a floor

New operator requirement: **no finished video may be under 8 seconds.** A hard floor.

`memebot/` only. No paid calls. Every duration below comes from ffmpeg producing a playable
file and ffprobe reading it back.

**`claim.py brief` at round start** — 3 rounds in flight, none touching `memebot/`:
`BL-849` (298 min, `clip_library/`, flagged ** nothing written yet), `BL-867` (46 min,
`clip_library/`, `scratch/`), `BL-888` (12 min, `dashboard/`, flagged ** nothing written yet).
One advisory on filing: BL-867 claims `scratch/` broadly; my files are `scratch/mb036_*`,
distinct names, no real overlap. Proceeded.

---

## 1. THE PROBLEM, MEASURED FIRST

**9.3% of the library is under 8 seconds.** Not 2%, not 20% — it shapes the render path.

Measured on **`media_duration_s`** (98.8% coverage), not `duration_s` (69.3%):

| Below the floor | clips | % of library |
|---|---:|---:|
| 7–8s | 56 | 2.8% |
| 6–7s | 56 | 2.8% |
| 5–6s | 63 | 3.1% |
| 4–5s | 7 | 0.3% |
| 3–4s | 2 | 0.1% |
| **total under 8.0s** | **184 / 1,978** | **9.3%** |

p1 = 5.0s, p5 = 6.3s, p10 = 8.2s, median 32.8s, min 3.13s.

### The two duration columns disagree, and it matters

`duration_s` and `media_duration_s` differ by >0.5s on **13.5%** of clips, and **classify 9
clips differently against the floor** — one stores `duration_s=9.80` where the retrieval
payload says `media_duration_s=5.04`. A rule tuned on `duration_s` waves those 9 straight
through. Filtering must use `media_duration_s`; the renderer probes the real file anyway.

---

## 2. THE RULE

| Source duration | Technique | What happens |
|---|---|---|
| **≥ 8.00s** | pass | nothing |
| **7.00 – 8.00s** | **fade** | +1.0s black (0.5s each end) |
| **5.95 – 7.00s** | **slow + fade** | 0.85–1.0× plus the same 1.0s black |
| **< 5.95s** | **reject** | skipped, never stretched |

**Fade before slowing — which inverts the operator's stated order, on measurable grounds.**
Fading costs nothing: it adds real time and alters not one frame. Slowing alters every frame.
Where fade alone clears the floor (src ≥ 7.0s — 56 of the 184) there is no reason to touch
the pixels. Slowing is applied only where fade cannot get there alone.

### What slowing actually costs

- **Pitch: nothing.** The chain uses ffmpeg **`atempo`**, a time-domain stretch that
  *preserves pitch*. The operator's pitch concern applies to `asetrate`, which is not used
  for speed. (`edit.py` uses `asetrate` only for the deliberate pitch-shift transform, and
  composes an inverse `atempo` to hold duration — the two are independent.)
- **Judder: real, and the binding constraint.** Measured on the actual renders:
  **16.0% duplicated frames at 0.8688×**, **14.6% at 0.8987×**. Source is 30fps, so at 0.85×
  roughly 1 frame in 7 is a duplicate — at the edge of visible on panning shots, invisible on
  static ones. Below ~0.80× the cadence becomes a visible stutter. **0.85× is the floor.**
- **Audio artefact:** `atempo` below ~0.8× smears transients. 0.85× stays inside the clean
  single-stage range.

### Why 5.95s is the reject line

It is not chosen, it falls out: `(8.0 − 1.0 fade) × 0.85 = 5.95`. Below that, reaching 8s
needs a slower stretch or more than a second of black, and both look wrong.

**The operator independently said "above six seconds you can slow it down."** 5.95 and his 6.0
are the same boundary, reached from opposite ends.

**No looping.** Explicitly forbidden, and there is no code path that can do it — `plan()` has
no loop branch, and a test asserts no plan ever mentions one. It also never freezes a frame,
for the same reason. (The *audio* hook still loops to fill; that is separate and intended.)

---

## 3. REAL RENDERS — 4/4 CLEAR THE FLOOR

Playable files, in `scratch/mb036/`. All four decode end-to-end with video **and** audio.

| Case | Source | Technique | Planned | **Actual** | Drift | Judder |
|---|---:|---|---:|---:|---:|---:|
| A | 7.127s | fade | 8.127s | **8.133s** | +0.006s | — |
| B | 6.082s | slow 0.8688× + fade | 8.001s | **8.000s** | −0.001s | 16.0% |
| C | 6.291s | slow 0.8987× + fade | 8.000s | **8.000s** | −0.000s | 14.6% |
| D | 7.567s | fade | 8.567s | **8.600s** | +0.033s | — |

All h264 720×1280, aac audio, `ffmpeg -f null -` decode exit 0.

### Three things that had to be got right, each found by a render failing

**1. The fade must PAD, not dim.** `fade=t=in` over existing content adds **no time** — it
darkens the first half second and the file is exactly as short as it was. The operator asked
for black that "buys ~1s", which is `tpad`: real black frames, with a fade across the join.
Getting this wrong produces a technique that measurably does nothing.

**2. `apad` hangs ffmpeg.** Bare `apad`, and `apad=whole_dur=N`, both hang indefinitely here
— **even with `-t` set**. Bisected filter by filter: `tpad` alone fine, `tpad`+`adelay` fine,
`+apad` times out at 60s every time. Not used. The tail silence comes free: the audio stream
simply ends before the video, which is what a black tail means.

**3. Container duration ≠ video-stream duration — and it put a render UNDER the floor.**
Source `DUGOWzskh75`: container **7.127s**, video stream **6.967s**. `tpad` works on the video
stream, so +1.0s gave **7.967s** where the plan predicted 8.127s — **0.03s short, from a plan
that looked right.** So the output length is not predicted, it is **forced**: pad generously
past the target, then cut with `-t` at exactly the planned duration.

---

## 4. THE AUDIO STILL LANDS — with one real problem found

### The hook placement trap

`place_at()` and `loop_count()` both take `clip_len_s`. If the renderer passes the **source**
length after stretching, the hook lands wrong:

| Length passed | place_at | as % of final |
|---|---:|---:|
| source (6.08s) — **wrong** | 2.614s | **32.7%** |
| final (8.00s) — **right** | 3.440s | **43.0%** |

The drop arrives **0.83s early**. Audio still covers the video (loop count over-covers, so
nothing goes silent) — which is exactly why this would not have been noticed.

### The fade DOES cut the hook — every time, not occasionally

`place_at` clamps to **0.0** whenever the clip is shorter than twice the hook. Measured
against the live song store: **all 15 hand-marked hooks run 6.0s–26.9s**, every one longer
than half of an 8-second video.

**So on every floor-lifted clip, `place_at` is 0.0 and the hook starts on frame one** — and a
0.5s audio fade-in would land squarely on the hook's **attack**, the drop, the single moment
the operator marked the window for.

**Fixed by decoupling the fades:** the video ramps from black, the audio starts at full level
(`AUDIO_FADE_IN_S = 0.0`). Black video under full-level music is a normal, deliberate opening
— a beat landing on the cut to picture. The **tail** keeps its audio fade, since the hook is
almost always mid-phrase at the end and a ramp is kinder than a cliff.

---

## 5. THE CHECK — what makes it a floor rather than a preference

`duration.assert_floor()` re-probes the **finished file** and fails loudly. Wired into
`edit.py` immediately after `is_healthy_video()` and **before `os.replace`**, so a short
render never becomes the output file.

**That placement is the MEMEBOT-010 gap exactly.** Demonstrated on a synthetic 5.0s file that
is genuinely healthy — 720×1280, aac audio, 2.7 MB:

```
duration              : 5.000s
is_healthy_video says : True     <- the file is FINE; it is the wrong LENGTH
FLOOR FIRES           : finished at 5.000s, under the 8.0s floor. Not shipping a short video.
```

A first attempt used a 5s file with no audio; `is_healthy_video` rejected it for an unrelated
reason, which would have proved nothing. The fixture above is the honest one.

It also catches the rest of the MEMEBOT-010 shape: `expected_s` fails a render that **clears
the floor but misses its plan** — 5.0s would clear a 5s floor while being 56.8s short.

Config: `edit.transform.duration_floor` (`enabled: true`, `floor_s: 8.0`), and **the code
defaults to enabled** — an opt-in floor is not a floor. Verified against the live config.

`memebot/scraper/tests/test_duration.py` — **15 tests, green.** The rule swept at 10ms
resolution across 0–20s: zero plans fail to reach the floor, zero speeds below the judder
limit, zero mentions of looping.

---

## 6. WHAT THE FLOOR COSTS

Against `media_duration_s`, n = 1,978:

| | clips | of the 184 |
|---|---:|---:|
| **Unusable with no stretching at all** | **184** | 100% |
| Rescued by fade alone (≥7.0s) | 56 | 30% |
| Rescued by slow+fade down to 0.85× (≥5.95s) | **114** | **62%** |
| **Rejected — below 5.95s** | **70** | **38%** |

**The floor costs 70 clips — 3.5% of the library.** They are not deleted; `plan()` returns
`reject` and the caller skips them.

Reference points if the operator ever wants to trade quality for volume: 0.80× would rescue
82 of 184 on slowing alone (vs 62 at 0.85×), at visible stutter. Not recommended, measured.

---

## PROOF

| Required | Result |
|---|---|
| Sub-8s distribution measured | **184/1,978 = 9.3%**, bucketed; two columns disagree on 9 |
| Rule recommended with quality costs | fade → slow+fade → reject; pitch **nil**, judder **14.6–16.0%** measured |
| Real render per technique, playable | **4/4 clear the floor**, decode exit 0, video+audio |
| Hard check fails on a synthetic 5s output | **fires** — while `is_healthy_video` says True |
| memebot suites | test_duration **15/15**, test_edit, test_duck, test_scrape, test_caption_fit — **all PASS** |
| clippershq suite | **ALL GREEN — 93/93 suites, 3,883 checks** (351 s) |
| Campaigns byte-identical | `8e02f8d6f6307ae8` — **MATCH** |
| config.json / config.yaml | both parse; floor reads `enabled=True, floor_s=8.0` |

---

### Method / limits

- Library figures read through `read_snapshot` — BL-849 and BL-867 are appending to
  `clip_library/`, and a numerator and denominator from two versions of the store is the bug
  that module exists to prevent.
- Judder is measured as **duplicated-frame percentage**, which is the mechanical cause. It is
  not a perceptual study; "invisible on static shots, edge-of-visible on pans" is my
  judgement from the cadence, not a viewer test.
- The four renders are real library clips but a small sample. The rule is swept exhaustively
  in tests; the *renders* prove the filter chain, not the aesthetics.
- `plan()` is pure arithmetic and knows nothing about content. A 6s clip whose last second is
  a hard cut will still be slowed; nothing here inspects the footage.
- The audio findings are computed against `song_library.place_at`/`loop_count` and the live
  store. I did **not** re-render a full pipeline video with music — `clip_pipeline.py` remains
  unreachable from any entry point (BL-859), so there is no end-to-end path to exercise.
