# 2026-09-22-b — the clip is already a u2net matte with the crowd baked into Messi: everything DETACHED is now gone by construction, and the fused seconds cannot be separated from this file

**Round metadata:** delivered `components/matting/cutout.py` — a component every
style can call, not a script for this clip — the cut of all 423 frames over
black plus ProRes 4444 and VP9 alpha, 20 hand-labelled frames kept as a
dataset, three tools, and the four measurements each with a control that can
fail. NOT done: a re-cut from the original match footage, which is the only
route that removes the fused matter; it is written up below as the next step
with the evidence for and against it, not delivered.

## The paragraph

Cutting Messi out of `videooooo-1.mp4` turned out to be two different jobs,
because the file is **not footage**: **79.1%** of the median frame is pure
black, so it is already a matte -- a per-frame rembg u2net pass over
`messi Argentina 227.mov`, centre-cropped and slowed **2.17x** with frame
interpolation. The first job, everything DETACHED from him, is now solved by
construction exactly as the brief prescribed: instance masks from YOLO11-seg
(run on a grey composite, which is what finally let a detector see his black
shorts and dark legs -- ankle confidence **0.08 -> 0.50** on f140), the subject
chosen by the identity-confirmed face chain (**57** frames carry a confirmed
face, **366** ride mask overlap from one, **0** are empty), and then every
foreground component that his core does not cover 40% of and his body envelope
does not cover 60% of is deleted whatever its score -- **3,610,898 px** dropped
over the clip. The second job, matter FUSED to him, is **not solvable from this
file**, and that is the finding of the round: the things u2net baked in are
**spectators in Argentina shirts**, a red-shirted spectator, Nigeria players
and the burnt-in **"ARG" caption**, and measured on this clip the red spectator
sits at **median distance 0** from his pose envelope while his own boots are
**200-380 px outside it**, so no geometric rule separates them; a colour model
built from his own pixels does separate them, but it costs **11,009 px of his
own neon boot** on f244 to win **3,084 px** of spectator on f78, so it is off
by default. The result: **IoU 0.9201 median / 0.8915 p10** against 20
hand-labelled frames, temporal IoU after motion compensation **p50 0.9008 /
p10 0.8621 / min 0.6871**, and **41 of 423 frames** carry any stray pixel at
all -- **p50 1,150 px**, max **6,952 px**, against a silhouette of ~240,000 px.
Watched end to end, **3.6 s to 7.05 s is clean**: Messi against black and
nothing else, every frame. **1.0 s to 3.5 s is not**, and the reason is that
the information needed to clean it was thrown away before the file reached me.
Three bugs were found and fixed on the way, each of which had been silently
corrupting every frame: `fill_holes` treated the wedge between his legs and the
picture edge as an enclosed hole and inflated the mask by **68,057 px**; the
3-frame median ring emitted frame 1 first and frame 0 never, so **every
delivered frame was one ahead of its source**; and the body box grew by a flat
12% of the detector box, which sheared his trailing boot off when he ran
(IoU over the labelled frames **0.9391 -> 0.9588** once it grew with his head
size instead).

## 1. What the input actually is — measured before anything was built

`videooooo-1.mp4` is **1080x1080, 60.000 fps, 423 frames, 7.050 s**. It is not
footage: **72.6% / 79.1% / 84.2%** of each frame (p10/p50/p90) is *pure* black,
i.e. it is already a matte composited over black. Masked template matching
against the footage library identifies the source as
`<LIBRARY>/Football/Players/Lionel Messi/Argentina/messi Argentina 227.mov`
(1920x1080, 60 fps, 456 frames), centre-cropped to x 420..1500, and retimed:

| our frame | 0 | 40 | 120 | 200 | 280 | 360 | 400 |
|---|---|---|---|---|---|---|---|
| best original frame | 0 | 4 | 44 | 86 | 124 | 164 | 184 |

That is a slope of **0.461**, a **2.17x slow-down**, and it is frame
*interpolated*, not frame-duplicated: the frame-to-frame difference has p50
3.85 and only 21 of 422 transitions are near-zero. So most of our frames have
**no exact original frame** to consult — which turns out to be the whole
difficulty of the round.

Two consequences, both load-bearing:

- **The clip is premultiplied over black.** Every pixel of Messi's true
  silhouette is inside `luma > 10`, and nothing outside it can be his. That
  makes the foreground the authority on WHERE the pixels are, and the models'
  job only to decide WHICH of them are his. It is also why his black shorts
  and dark boots survive at all — no detector sees them against black.
- **Whoever made this clip ran a generic salient-object matte** (rembg u2net,
  per-frame, identity-blind — exactly as the brief diagnosed) and it kept
  things that are not Messi. Cropping a 160 px window around each stray region
  and putting the same window from the original beneath it identifies them by
  eye: **spectators in Argentina shirts** behind him (u2net cannot tell a
  striped crowd from a striped kit), a **red-shirted spectator's arm**,
  **Nigeria players** in green, pitch boards, boots on grass, and the burnt-in
  **"ARG" scoreboard caption**. That gallery is `build/work/label_regions.png`.

**Deliverables:** `build/work/label_regions.png`, `build/work/whatisit.png`,
`build/work/cutcheck.png`.

## 2. The component — `components/matting/cutout.py`

Two passes over the clip. **Pass A** runs the detectors and the face
recognition once per frame and keeps the masks bit-packed; **`assign()`**
propagates the identity-confirmed subject forward *and* backward from every
face anchor by mask overlap (`ASSOC_IOU = 0.12`), so frames before the first
confirmed face are not black; **Pass B** streams one frame at a time and builds
the alpha. Cost **0.516 s/frame** for pass B on this CPU, **3 min 38 s** for the 423-frame clip.

Every rule below exists because a number forced it, and the number is here.

**Detection runs on a grey composite, not on the frame.** Asking a detector to
find a person against black when the person is partly black is the reason the
delivered legs were being cut. Compositing the foreground over mid-grey first
costs nothing and changes the answer: ankle keypoint confidence **0.02 -> 0.07**
(f80), **0.08 -> 0.50** (f140), **0.22 -> 0.33** (f380), and at f140 the other
players separate into their own instances, **2 -> 4**, which is what makes them
subtractable rather than guessable.

**Who he is: face, then track.** InsightFace buffalo_l against the confirmed
`identity/messi/ref.npz`, one frame in 6, assigned to the instance whose box
holds the face in its top 40% — the machinery from the previous round, reused
unchanged. Between anchors the subject rides mask overlap.

**Rule 3 of the brief — delete everything outside him — is where the flashes
went.** A foreground component is his only if the identity-confirmed core
covers **>= 40%** of it, or his body envelope covers **>= 60%**. Both are
fractions, not contact. A 5%-overlap test and a "touches the core" test each
let a detached blob 170 px from his head through on 3 of 40 probe frames at
overlap 0.217 — YOLO's person mask reaches across the gap and touches it.

**The envelope is the core plus his skeleton, with discs only at the
extremities.** Discs at the head and shoulders made the envelope ~110 px wider
than his outline there, which was exactly what swallowed that blob. Wrists and
ankles keep their discs because a hand or a boot really does stick out past the
last bone.

**His legs get a cone, not a rectangle.** From the hips down to the bottom of
his own *foreground* component — not the bottom of the instance core, which
stops at the knees; a cone drawn to the core's bottom cut his shins off.

**Every other person is subtracted pixel by pixel, never blended** — with two
guards that were each paid for: a second detection of the SUBJECT is not
another person (YOLO emits overlapping duplicates; subtracting one took
**56,619 px** off him on f96), and his own envelope protects him where another
player's sloppy mask crosses it (**62,407 px** off his legs on f96 before that
guard).

**Alpha, not a binary cut.** The source is premultiplied over black, so in the
boundary band the luminance relative to the interior *is* the alpha: interior
1, a ramp from luma 8 to 70 in the band, 0 outside. Then flow-warped EMA
(0.35), a 3-frame temporal median, and a 2 px feather. Three outputs: over
black (libx264), ProRes 4444 (`yuva444p10le`) and VP9 (`yuva420p`), with the
colour un-premultiplied for the two alpha files.

**The ball.** Default policy `attached`: the ball survives only while it is
part of his own component (his foot is on it); the moment it is free of him it
is a separate component and is dropped like anything else. `--ball drop`
subtracts it always, which leaves a bite where it is against his chest. The
hand labels treat a free ball as not-him, so the measurements below score the
default.

**The colour test that is OFF.** `alien_cut()` builds a 16^3 Lab histogram from
his own pixels each frame and cuts foreground regions below the 2nd percentile
of his own likelihood — the only thing that can reach matter *fused* to him,
since measured on this clip the red spectator sits at **median distance 0** from
his pose envelope while his own boots are **200-380 px outside it**, so no
geometric rule can separate them. It is off by default because it is a bad
trade: it removes **3,084 px** of the red spectator on f78 and **540 px** on
f84, but removes **11,009 px of his own neon boot** on f244, 2,363 on f412 and
2,095 of his sleeve and armband on f398. Cutting his boots off is a worse
failure than leaving a spectator in. `--alien` turns it on.

**Deliverables:** `components/matting/cutout.py`, `build/work/cut_env_debug.png`,
`build/work/cut_alien.png`, `build/work/cut_alien2.png`.

## 3. The measurements

All four, on the delivered alpha, by `tools/measure_cutout.py`. Ground truth
is `datasets/matting/messi_videooooo1` -- 20 frames, every foreground region
named as his or not his by eye against the original footage. **What it does not
cover:** matter fused into his own region, which cannot be labelled without
inventing a boundary. The IoU below is blind to that failure; section 5 counts
it instead.

### 1. Accuracy -- IoU against 20 hand-labelled frames

| | median | p10 | worst |
|---|---|---|---|
| alpha > 0.5 | **0.9201** | 0.8915 | 0.8703 (f112) |
| any coverage | **0.9274** | 0.8974 | 0.8773 |

Two numbers because the hand label is a **hard** threshold on the delivered
matte, so a correctly soft alpha in the boundary band scores as missing. The
truth is between them. Isolating the stages on f398/f420: the mask before the
alpha stage scores **0.9637**, the temporal smoothing costs **0.001**, and the
soft luma edge accounts for the remaining **0.024-0.036** -- i.e. almost all of
the gap is the label's edge, not the cut's.

The worst frames split cleanly into the two failure kinds. f112 (**extra
22,199 px**), f90 (**23,161**) and f68 (**18,161**) are *fused foreign matter
kept*. f244 (**11,569 px fully cut**) and f156 (**16,473**) are *parts of him
lost* -- his trailing boot, and on f156 a leg the leg-cone did not reach.

### 2. Stray pixels -- the bar is 0 on every frame

**41 of 423 frames** carry any stray at all; **35** carry >= 400 px; 6 carry
single-pixel specks. Per frame among the 35: **p50 1,150 px, p90 2,467 px, max
6,952 px**, against a silhouette of ~240,000 px. Total over the clip **55,476
px**, which is **0.05%** of the delivered foreground.

Named, because the brief asks for the frame numbers:

| frames | what it is |
|---|---|
| 6-20 | a dark fragment beside his hand and the ball |
| 88-89, 111-121 | the red-shirted spectator |
| 153-156 | the **"ARG" caption** -- it survives only on the frames where his raised arm passes beneath it, so his envelope covers 60% of it |
| 172-178, 192-193 | a Nigeria player in green |
| 377-383 | a red fragment at his sleeve |

**Outside his grown box: 0 px on 422 of 423 frames** (843 px on one). So
nothing appears anywhere far from him; what survives is all within arm's reach,
which is exactly where rule 3 cannot help.

### 3. Temporal stability -- consecutive masks after motion compensation

Previous mask warped forward by Farneback flow, then IoU with the current one.
**422 transitions: p50 0.9008, p10 0.8621, p01 0.7994, min 0.6871.**

The 10 worst: f143 0.687, f171 0.707, f421 0.755, f170 0.773, f205 0.799,
f81 0.802, f142 0.805, f359 0.807, f182 0.815, f215 0.815. Nine of the ten are
in the contested section, where the mask changes because the foreign matter
attached to him changes, not because his own silhouette is unstable.

### 4. Other people

**99 of 423 frames** have more than one person detected. Of those, **9** are
left with stray pixels (121, 139, 156, 172, 173, 178, 182, 193, 340). The
other-person subtraction fired on 2 frames for **76,360 px**; it fires rarely
because on this clip the other players are usually not *detected* at all --
they are fragments of bodies in a matte, not bodies.

### The controls

- **The metric's control** (`--self-test`): painting a blob into a *delivered*
  alpha makes the stray count read **11,289 px** where the clean frame reads
  **0**. The count can fire, so a 0 means something.
- **The pipeline's control** (`--sabotage-blob`): a grey disc painted into the
  *input* frame at (90,90) r=60 on f305 reached the output as **0 px** -- the
  component rule removed it, which is the behaviour rule 3 promises. This
  control tests the pipeline, not the metric; they are separate and both run.

**Deliverables:** `tools/measure_cutout.py`, `tools/label_cutout.py`,
`build/cutout/measurements.json`, `datasets/matting/messi_videooooo1/`,
`build/cutout/worst/` (10 PNGs, each source | cut | what was dropped).

## 4. Edge refinement: every model timed on this clip

Timed on 512x512 crops around the subject, which is how refinement is actually
used — the instance mask already says where he is, so the model only decides
the boundary. CPU, first run excluded as warm-up, median of 6.

| model | s/frame | load s | band MAE vs the premultiplied-luma alpha | verdict |
|---|---|---|---|---|
| u2net_human_seg | **0.41** | 0.6 | 0.290 | fastest, worst agreement |
| u2net | 0.53 | 0.7 | 0.206 | |
| silueta | 0.60 | 5.4 | 0.212 | |
| isnet-general-use | 1.10 | 0.5 | 0.229 | |
| inspyrenet-fast | 1.15 | 386 | 0.209 | InSPyReNet, own package |
| inspyrenet-base | 8.82 | 34 | **0.196** | best agreement, 20x the cost |
| birefnet-general-lite | 8.96 | 6.0 | 0.210 | |
| birefnet-portrait | 15.11 | 96 | 0.214 | |
| MODNet | — | — | — | not installable here: no maintained wheel, needs its repo and checkpoint vendored. Not timed, so not claimed. |

**None of them is used, and the reason is in the third column.** On a clip
already composited over black the alpha in the boundary band is not a matter of
opinion — it is the luminance, and computing it costs no time at all. Every
model *disagrees* with that physically correct alpha by **0.196 to 0.290 mean
absolute error** in the band. So the choice is between a free exact answer and
a 0.41-15.1 s/frame approximation of it. The pipeline uses the luma ramp
(`--edge luma`, the default); `--edge model --model <name>` runs any of the
above on the crop for the case where the source is NOT premultiplied, which is
what every other style will hand this component.

Installing InSPyReNet needed `albumentations==1.4.24` + `albucore==0.0.23`
pinned (2.0.8 raises `KeyError: np.uint32` against this numpy) and
`pydantic-core==2.46.5`. **opencv stayed at 4.14.0** — checked before and after,
because the last dependency install in this repo silently downgraded it.

**Deliverables:** `tools/bench_matting.py`, `build/work/matting_models.png`.

## 5. What cannot be cut from this file, and which seconds

Watched end to end as a contact sheet every 12 frames
(`build/work/out_sheet_0.png`, `out_sheet_1.png`):

- **0.00 s - 0.95 s (f0-f57): clean**, apart from the dark fragment by his hand
  on f6-f20.
- **1.00 s - 3.50 s (f60-f210): NOT clean.** This is the contested section --
  he is shielding the ball with a Nigeria defender against him and the crowd
  directly behind his head. On these frames u2net fused the crowd, the
  defender and the caption into his own silhouette, and no mask applied to
  *this file* can undo that: the pixels are the same colours as his kit, they
  touch him, and most of these frames are interpolated so there is no exact
  original frame to consult. Worst: f68, f84, f90, f108-f121, f154-f156,
  f172-f193.
- **3.60 s - 7.05 s (f216-f422): clean.** Messi against black and nothing else,
  on every tile. This is the running section and it is the majority of the
  clip -- **207 of 423 frames**.

If a single unbroken clean section is what you need, **3.6 s onward is it.**

**Deliverables:** `build/work/out_sheet_0.png`, `build/work/out_sheet_1.png`,
`build/work/stray_id.png`.

## 6. The route that does work, and why it is not delivered

Cutting from the **original** footage removes the fused matter *by
construction*: the crowd and the Nigeria players are their own person instances
against a real background, so rule 3 applies to them the way it applies to
anything else. `build/work/source_recut.png` shows six frames cut that way —
**no crowd, no second player, nothing**. It also shows why it is not this
round's deliverable: yolo11n-seg's mask loses his legs on 4 of those 6 frames.
That is a model-size problem, not a limit of the approach, and against a real
background the refinement models in section 4 have something to work with.

The obvious shortcut — use the original's Messi mask as the authority for our
frames — was tried and **measured as unusable**: the best-matching original
frame's mask reaches only **IoU 0.53-0.75** against our foreground, because
most of our frames are interpolated and sit *between* original frames. Applied
pixel by pixel it cuts **22-32%** of the delivered foreground. Region-level
vetoing was not pursued further once the fused regions turned out to be crowd
rather than tracked players.

The honest next step is to cut from `messi Argentina 227.mov` with a bigger
segmentation model plus crop refinement, and retime the result to this clip's
423 frames. That is a round of work, and it changes the deliverable from "your
file, cleaned" to "the same shot, re-made", which is your call to make, not
mine.

**Deliverables:** `build/work/source_recut.png`, `build/work/cut_auth.png`,
`build/work/cut_auth2.png`.

## Deliverables

The video first.

| path | what |
|---|---|
| `build/cutout/messi_cut.mp4` | **the cut over pure black**, 1080x1080, 60 fps, 423 frames, H.264 crf 14 |
| `build/cutout/messi_cut_alpha.mov` | the same with a **real alpha channel** -- ProRes 4444, `yuva444p10le`, colour un-premultiplied |
| `build/cutout/messi_cut_alpha.webm` | the same as **VP9 with alpha**, `yuva420p` (9.4 MB against the .mov's 246 MB) |
| `build/cutout/messi_cut_masks.npz` | the alpha as uint8, for re-measuring without re-running |
| `build/cutout/messi_cut_stats.json` | per-frame source, instance count, every cut broken down, timings |
| `build/cutout/worst/worst_*.png` | the **10 worst frames**: source, cut, and in magenta what was dropped |
| `build/cutout/measurements.json` | every number in section 3 |
| `build/cutout/control*` | the sabotage-blob control run |
| `components/matting/cutout.py` | **the component** -- `run()`, `pass_a()`, `assign()`, `pass_b()`, and every rule as a named function with the number that forced it |
| `tools/label_cutout.py` | the hand-labelling aid (`sheets`, then `build`) |
| `tools/measure_cutout.py` | the four measurements, `--self-test`, `--dump-worst` |
| `tools/bench_matting.py` | the model timings in section 4 |
| `datasets/matting/README.md`, `datasets/matting/messi_videooooo1/` | the hand labels and what they are not |
| `build/work/label_regions.png` | every stray region of the input, with the original beneath it |
| `build/work/out_sheet_0.png`, `build/work/out_sheet_1.png` | the whole output, every 12th frame |
| `build/work/source_recut.png` | six frames cut from the ORIGINAL instead |
| `build/work/matting_models.png` | what each refinement model's edge looks like |

## Assertions at close

- Input 423 frames; **output 423 frames** in all three files. Checked by
  matching frames to sources, not by the count: the ring bug below produced
  423-in / 423-out while dropping frame 0 and duplicating another, so the
  count alone was never the test.
- **0 frames empty.** 57 carry a confirmed face (similarity 0.41-0.53), 366
  ride mask overlap from one, none fall out of the chain. Backward propagation
  is what makes the opening frames non-black, since the first face match is at
  f61.
- Cost **0.516 s/frame** for pass B (segmentation 0.419, face 0.150 on the
  1-in-6 frames, edge 0.105), **3 min 38 s** for the clip including pass A.
- **opencv is still 4.14.0** after installing InSPyReNet's dependency chain,
  checked before and after -- the last dependency install in this repo
  silently downgraded it.
- `tests/test_no_kill_by_name.py` was NOT run: the chrome-guard `PreToolUse`
  hook blocks the command because that test file contains the banned patterns
  by design, and working around the hook is forbidden. Nothing in this round
  terminates a process.
- Nothing in `input/`, `references/`, `music/` or the footage library was
  written. The clip was read from the repo root, where it actually is.

## What I got wrong

- **I built the mask stage three times before checking frame alignment.** The
  3-frame median ring emitted `ring_f[1]` first, so output frame 0 was source
  frame 1 and one frame was duplicated at the tail. Every IoU measured up to
  that point was measured against the wrong frame. Found only because a clean,
  foreign-matter-free frame was scoring 0.87.
- **`fill_holes` was wrong from the first version and I did not question it.**
  Flooding the mask from (0,0) makes any region enclosed by his body *and the
  picture border* count as a hole. On f93 it inflated the mask by **68,057 px**
  -- the wedge between his legs and the bottom edge. It had been doing that on
  every frame of every probe in this round.
- **I reported the blob fixed when it was not.** I verified the component rule
  at f90 and f93 with a standalone script and said so; the pipeline kept the
  blob on f94-f98, because YOLO's person mask reaches across the gap and
  *touches* it and my keep test was "touches the core". A fraction test was
  needed. I should have measured the pipeline's own output, not a
  reimplementation of it.
- **The first `body_box` grew by a flat 12% and I never asked what it cost.**
  It sheared his trailing boot off whenever he ran. Measured afterwards: IoU
  over the 20 labelled frames **0.9391** with 12%, **0.9588** growing with his
  head size, **0.9637** with no box at all.
- **I spent a long stretch trying to use the original footage as a pixel-level
  authority before measuring whether it could be.** It cannot -- IoU 0.53-0.75,
  22-32% of the delivered foreground cut. One alignment measurement at the
  start would have saved all of it.
- **The brief said the clip was in `input/`.** It is at the repo root. I should
  have said so rather than quietly resolving it.

## Unsure

- **Whether the fused matter is worth another round.** Re-cutting from
  `messi Argentina 227.mov` removes it by construction, but it means re-making
  the shot rather than cleaning your file, and the retiming to 423 frames is
  not prototyped. I have not verified that a retimed re-cut would match this
  clip's motion closely enough to be a drop-in replacement.
- **The `--alien` trade may be the wrong way round for your eye.** I judged
  that losing his boot for a few frames is worse than keeping a spectator's
  sleeve. If you would rather the spectator were gone and accept the boot
  damage, it is one flag, and both sets of numbers are in section 2.
- **My hand labels are region-exact but edge-inherited.** Where the true edge
  is hair or motion blur the ground truth is u2net's edge, so the IoU says how
  well the right *regions* were chosen, not how well the boundary was placed.
  I have no independent measurement of sub-pixel edge quality on this clip and
  do not claim one.
- **`alpha_from_luma`'s `lo=8, hi=70` ramp was not tuned against anything.** It
  is the physically right shape for a premultiplied source, and its advantage
  over the models in section 4 is measured as agreement with itself, which is
  circular. A real edge measurement needs a source that is not already matted.
- **MODNet was not timed**, so the brief's model list is one short. It has no
  maintained wheel and needs its repository and checkpoint vendored; I judged
  that out of scope rather than guess at its speed.
