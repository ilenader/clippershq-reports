# 2026-09-22-c — Neymar v01 is delivered; identity was never actually running until this round, and finding that is what the round cost

**Round metadata:** delivered `2026-09-22_neymar_v01.mp4` (30.50 s, 914 frames,
1080x1920, libx264 master), all five gates passing with their controls firing.
Four bugs fixed on the way, one of which had silently disabled the identity
rule in every re-planned edit. NOT in this edit: the transitions, the beat-drop
matte and the ambient glow — none is wired into the builder, so all three were
left out rather than rushed.

## The video

    C:\Users\<PROFILE>\Desktop\flashcut-renders\2026-09-22_neymar_v01.mp4
    (repo copy: output/neymar_v01.mp4)

## The paragraph

The edit is delivered and every requirement you set is met and measured:
identity picks Neymar or nothing is drawn (**every one of the 21 placed
segments carries a confirmed face, 0.36–0.78 similarity**, and the three that
do not — the 2013 archive and your two hand-cut treble shots — carry **no
ink**), white ink over the contact shadow with no colour logic anywhere, all
three looks placed (**converge, box, skeleton**), the motion gate on at
**1.5 hw/s**, density **15% of runtime** inside your 9–19% band, degenerate
geometry refused, and the card schedule, the five flashes and the grade
byte-for-byte as style 1 has them — the delivered picture-band luma is
**36.9 mean** against the Ronaldo baseline's **37.1**, so it is the same look,
not a darker one. The script is the approved option (a): **CIRCUS · ALL TRICKS
· SHOW PONY · NO SUBSTANCE · CLOWN · ACTOR · FAKER · FRAIL · HYPED · SOFT ·
BRAND · DIVA · NEYMAR**, every accusation attested before Berlin 2015, and
`check_scripts` passes clean with its control firing. The identity threshold is
**0.30 with a 0.05 subject-area floor**, which on the 93 hand-labelled shots is
**72 right, 0 wrong, 0 drawn on nobody** — four shots better than 0.40 and, with
the floor, the scoreboard case is gone (the no-floor control brings it back).
The thing worth your attention is what the round actually uncovered:
**`plan_verify.py` never passed `--athlete` to the solver**, so every edit it
re-planned was tracked by the OLD subject score with identity switched off
entirely — the first Neymar solve came back `face_samples: 0, identity: None`
on all 21 segments. It rendered, it looked plausible, and it would have shipped
with ink chosen the way the 23-wrong-in-93 score chooses. With identity
actually on, **14 clips were refused** and the plan is a different plan.

## 1. The card list, all 13

Approved option (a): the turn is Berlin 2015, so every accusation has to
predate it.

| # | tier | card | the accusation, and when it was made |
|---|---|---|---|
| 1 | slow | **CIRCUS** | Santos 2011–13, the showboating charge |
| 2 | slow | **ALL TRICKS** | "all tricks, no end product" — the standing pre-move criticism |
| 3 | slow | **SHOW PONY** | the English phrase for him before the 2013 move |
| 4 | slow | **NO SUBSTANCE** | style over substance, the same charge in three words |
| 5 | fast | **CLOWN** | Santos era, the rainbow flicks and the reaction to them |
| 6 | fast | **ACTOR** | the diving charge, from the Brasileirão onward |
| 7 | fast | **FAKER** | the same charge, one word |
| 8 | fast | **FRAIL** | "too frail for European football" — the 2010–13 transfer doubt |
| 9 | fast | **HYPED** | overhyped by the Brazilian media before he had played in Europe |
| 10 | fast | **SOFT** | "he will be kicked out of La Liga" — the 2013 arrival |
| 11 | fast | **BRAND** | a marketing product before a footballer — the sponsorship charge |
| 12 | fast | **DIVA** | the haircuts, the entourage, the celebrity — Santos era |
| 13 | name | **NEYMAR** | |

**Cut, with the reason:** ROLLING (2018 Russia, three years after the turn),
TIKTOK (the app did not exist in 2015), INJURED (a PSG-era charge, 2017+),
ALONE ("left alone at PSG", 2017+), PARTY (the Paris lifestyle charge, 2017+),
WASTED ("wasted his career" — only sayable after the PSG years).

Lengths hold: slow tier 6–12 characters (max 15), fast tier one word of 4–6
letters (max 7). `check_scripts.py` is **CLEAN** — no repeat within the script,
across the other five, or against the delivered Ronaldo edit — with its control
(a planted repeat and a planted fast-tier phrase) firing first.

**Deliverables:** `configs/scripts.json`, `configs/neymar.json`.

## 2. Identity: 0.30 plus the size floor, and the bug underneath it

**The sweep, rerun with the floor** (`tools/identity_eval.py --floor-sweep`,
93 hand-labelled shots):

```
  thresh | score: right wrong | identity: right wrong refused drew-on-nobody
   0.30  |  70  23            |  72   0   21    0
   0.35  |  70  23            |  70   0   23    0
   0.40  |  70  23            |  68   0   25    0

  FLOOR SWEEP at 0.30   (0.000 = the control)
   0.000 | right 72  wrong 0  refused 20  drew-on-nobody 1  <- vi_winners
   0.030 | right 72  wrong 0  refused 20  drew-on-nobody 1  <- vi_winners
   0.050 | right 72  wrong 0  refused 21  drew-on-nobody 0
   0.080 | right 72  wrong 0  refused 21  drew-on-nobody 0
   0.100 | right 71  wrong 0  refused 22  drew-on-nobody 0
```

**0.30 + 0.05** it is. The floor is on the matched chain's box area as a
fraction of the frame, and `vi_winners` — the WINNERS board, where a photograph
of Vinícius 4% of the frame wide matched at 0.42 and the ink went on a
scoreboard — is what it removes. The band 0.05–0.08 is flat; 0.10 costs a
correct shot, so 0.05 is the smallest floor that does the job. The control is
the no-floor row: it brings the scoreboard case straight back, so the floor is
demonstrably the thing doing the work.

**The bug.** `tools/plan_verify.py` calls `solve_cache.py` for every round of
its plan → stage → solve → refuse loop, and it was calling it **without
`--athlete`**. `--athlete` is what loads `identity/<athlete>/ref.npz`; without
it `shot_track` is handed `ref=None` and skips the face model entirely. The
first Neymar solve is the evidence: `face_samples: 0` and `identity: None` on
all 21 segments, and "identity refusals: 0" — a number that meant nothing
because identity had not been consulted. The previous three edits were solved
by calling `solve_cache` directly with `--athlete`, which is why their reports
show identity working; anything that went through `plan_verify` did not.

Fixed, and the cache is now keyed to the identity RULE as well
(`_id-neymar@0.30-a0.050`), so a track solved at the old threshold can never be
served for a run at the new one.

**Identity on the delivered plan**, per segment:

| segments | identity | ink |
|---|---|---|
| 0, 3–12, 14, 15, 18–22 (18 segments) | confirmed, **0.36 – 0.78** | 5 of them carry a look |
| 13 (archive, Brazil 88, the 2013 boy) | no match — the reference set is adult Neymar | none |
| 16, 17 (your hand-cut treble shots) | no match | none |

**14 clips were refused** by the presence rule once identity was real, across
four rounds: PSG 110 / 197 / 134, Brazil 77 / 74 / 90 / 58 / 69, Barcelona 74 /
88 / 75 / 82 / 83 / 58. The plan converged clean on the next round.

**Deliverables:** `components/identity/identity.py`, `shot_track.py`,
`tools/identity_eval.py`, `tools/plan_verify.py`, `tools/solve_cache.py`,
`build/work/refused_neymar.json`, `build/work/solves_neymar.json`.

## 3. The overlay: density, looks, and the numbers

**Density: 5 of 21 segments, 4.6 s = 15% of runtime**, inside the 9–19% band
you asked for and under the 19% cap this edit is held to. The cap is now a
config knob (`density_max`) rather than a constant, so style 01's own 23%
stays the default and this edit's 19% is written down where the look lives.

**All three looks placed:** converge (seg 5), box (segs 7, 8, 18), skeleton
(seg 11). Converge needed a new pass to get there and the honest account is
this: converge was **legal on four segments but only one of them also passed
the motion gate**, and the local "don't repeat the previous look" rule had
already given that segment skeleton. The gate now runs a coverage pass — a
required look is placed on the segment where it is legal and whose current look
is still covered elsewhere — and if there is no such segment it prints **NOT
PLACED** rather than shipping quietly. Here there was exactly one home, seg 5,
and converge took it. It is a tunnel shot rather than a celebration, which is
not where the style would rather have converge; the celebrations (segs 20–22)
all measure 0.1–1.0 hw/s and fail the motion gate.

**Bracket → head distance, in head widths** (measured against the overlay-free
twin, `tools/measure_overlay.py`):

| | p10 | p25 | p50 | p75 | p90 | p95 | max |
|---|---|---|---|---|---|---|---|
| **pre-grade** | 0.040 | 0.066 | **0.103** | 0.261 | 0.604 | 0.672 | 0.740 |
| **post-grade** | 0.051 | 0.071 | **0.109** | 0.168 | 0.262 | 0.345 | 0.43 |

**Bracket / head size ratio** (want ~1.0):

| | p10 | p50 | p90 |
|---|---|---|---|
| **pre-grade** | 1.114 | **1.256** | 1.898 |
| **post-grade** | 1.295 | **1.406** | 1.556 |

**Converge centre → head:** pre-grade p50 **0.160**, p90 0.741, max 1.784,
**80% within 0.5 hw**; post-grade p50 **0.290**, p90 4.071, **60% within
0.5 hw**. The post-grade tail is the referee's limit, not the ink's — the grade
crushes the picture and the independent head detector loses faces in it, the
same effect recorded last round. The pre-grade numbers are the ones that
describe where the ink actually is.

**Ink contrast** (`tools/ink_contrast.py`, control fires: bare white on a white
shirt vanishes 100%, with the shadow 0%): across 26 frames with ink, the
ink-or-shadow per-frame p10 is **p50 144, p10 114, worst 9.0**. One frame of 26
— **f840, 28.00 s, seg 18** — has the ink under 40 luma even with its shadow:
white ink on the bright lime Barcelona away kit after the grade. One frame, and
it is named rather than averaged away.

**Deliverables:** `components/overlay/overlay_gate.py`,
`build/work/neymar_overlay_graded.json`, `build/work/neymar_overlay_raw.json`,
`build/work/neymar_ink.json`.

## 4. The five gates

```
POSITIVE CONTROLS
  control freeze : moving clip OK, six held frames FAIL -> fires
  control flash  : +32 measured +31 (OK), +60 measured +59 (FAIL) -> fires
  control cards  : phantom 14th card -> fires
  self-test OK

DELIVERY GATES  output/neymar_v01.mp4
  1 frames   OK
  2 freeze   OK  (on the grain-free render)
  3 cards    OK  13 scheduled, 13 rendered, 13 runs in the file
  4 flash    OK   13.87s:+32  14.37s:+32  15.80s:+31  16.77s:+32  21.33s:+30
  5 overlay  OK   bracket->head p50 0.11  worst 0.43 head widths (gate: p50 <= 0.5)

ALL 5 GATES PASS
```

The five flashes land on their scheduled frames at +30 to +32 luma against the
configured +32. The 13 cards are all present and all read structurally by the
card gate, not just counted from the schedule.

## 5. The five worst frames

`build/work/neymar_worst/worst_f0417.png`, `worst_f0423.png`, `worst_f0855.png`,
`worst_f0858.png`, `worst_f0867.png` (and the sheet
`build/work/neymar_worst_sheet.png`). Each panel shows the located bracket in
magenta and an independently detected head in cyan.

| frame | t | look | bracket → head | size | what it is |
|---|---|---|---|---|---|
| f867 | 28.9 s | box | **0.43 hw** | 1.64 | seg 18, Bayern semi; the bracket is high and wide on a head half-hidden behind a Bayern shirt |
| f417 | 13.9 s | box | 0.19 hw | 1.11 | seg 7, PSG, clean |
| f423 | 14.1 s | box | 0.16 hw | 1.42 | seg 7, clean |
| f855 | 28.5 s | box | 0.14 hw | 1.48 | seg 18, clean |
| f858 | 28.6 s | box | 0.08 hw | 1.38 | seg 18, clean |

All five are on Neymar's head; the worst is 0.43 head widths, inside the 0.5
gate. The size ratio 1.1–1.6 is the same band the delivered Messi (1.24) and
Vinícius (1.41) edits measured.

## 6. What is NOT in this edit

The transitions, the beat-drop matte move and the ambient glow are **not in
it**. None of the three is wired into `build_doubters`: the five measured
transitions exist as numpy functions in `components/transitions/transitions.py`
but nothing calls them from the builder, and the matte move and the glow are
prototypes on single clips (`components/transitions/drop_matte.py`,
`components/grade/ambient.py`) that have never run inside an edit. Each is real
work, not a switch, and you said you wanted the video more than you wanted
them.

## 7. How long the next edit takes

Measured on this one. For an athlete who already has a carved pool, a story
file with hand labels, a confirmed reference face set and a checked script —
which Messi, Vinícius and Haaland all do:

| step | cold | warm cache |
|---|---|---|
| plan → stage → solve → refuse, to convergence | ~6 min (4 rounds, identity on) | ~1 min |
| overlay gate | 20 s | 20 s |
| render: master + clean twin + raw + raw-clean | **402 s** (181 + 176 + 25 + 20) | same |
| five delivery gates (controls included) | ~4 min | ~4 min |
| measure_overlay ×2, ink_contrast | ~6 min | ~6 min |
| **total** | **~25 min** | **~18 min** |

The renders are the floor and they are CPU-bound on libx264 at 1080x1920; the
AMF proxy path would cut the two grade-carrying passes roughly in half at a
quality cost that is not worth it for a master.

What is NOT in that 25 minutes, and is the real cost for a NEW athlete: carving
the long compilations into shot clips, screening them into a pool, reading the
contact sheets to hand-label the story slots, and building and **confirming**
the reference face set. That is hours, and the face sheet needs your eyes on it
before anything downstream can be trusted.

## Deliverables

| path | what |
|---|---|
| `<PROFILE>\Desktop\flashcut-renders\2026-09-22_neymar_v01.mp4` | **the video** |
| `output/neymar_v01.mp4` | the repo copy |
| `output/neymar_v01_index.json` | which look was drawn when |
| `configs/neymar.json` | the frozen parameter set: cards, flashes, grade, `track_plan`, `density_max`, the gate's decisions |
| `configs/scripts.json` | the approved script and why each cut card was cut |
| `configs/story_neymar.json` | the story, with the two swapped hand cuts and why |
| `build/work/plan_neymar_staged.json`, `solves_neymar.json` | the plan and the identity-aware solves |
| `build/work/refused_neymar.json` | the 14 clips identity refused |
| `build/work/neymar_planverify.log` | the per-clip presence table, every round |
| `build/work/neymar_worst/worst_f*.png`, `neymar_worst_sheet.png` | the five worst frames |
| `build/work/neymar_overlay_graded.json`, `neymar_overlay_raw.json` | the distributions in section 3 |
| `build/work/neymar_ink.json` | the ink-contrast measurement |
| `build/work/neymar_clean.mp4`, `neymar_raw.mp4`, `neymar_raw_clean.mp4` | the measurement twins |
| `build/work/neymar_strip.png` | the delivered arc, 13 samples |

## Assertions at close

- **914 frames, 30.50 s, 1080x1920, libx264.** 914 is what every delivered
  edit in this style measures (30.488 × 30 = 914.64); the builder prints 915,
  which is its own count of frames written, not what the encoder lands.
- **13 cards scheduled, 13 rendered, 13 read structurally out of the file.**
- **5 flashes** at +30 to +32 luma on their scheduled frames.
- **Every placed segment carries a confirmed Neymar face** except the archive
  and your two hand cuts, and those three carry no ink.
- **0 degenerate refusals** on the delivered render (the earlier plan had 19
  frames refused; the identity-picked plan has none).
- **Grade unchanged from style 1**: picture-band luma mean 36.9 / p50 33.2
  against the Ronaldo baseline's 37.1 / 36.4.
- The chrome-guard hook blocks running `tests/test_no_kill_by_name.py` (that
  file contains the banned patterns by design) and I did not work around it.
  Nothing in this round terminates a process.
- Nothing was written to `input/`, `references/`, `music/` or the footage
  library.

## What I got wrong

- **I did not check that identity was actually running before rendering.** The
  first Neymar edit rendered, looked plausible, and had identity switched off
  for all 21 segments because `plan_verify` never passed `--athlete`. I read
  "identity refusals: 0" off the solves and reported it to myself as a good
  number; it was an empty one. The check that caught it — reading
  `face_samples` — takes ten seconds and should have been the first thing I
  did, not the fourth.
- **My first fix for the short opener made the edit worse.** The single-shot
  opener is merged AFTER selection, so its clip was chosen against a 1.93 s
  sub-cut and then asked for the whole 5.90 s; the render ran out of frames. I
  patched it by swapping in "the longest clip that fits", which put a close-up
  of **Verratti** in the opening shot of a Neymar edit. The right fix was to
  select against the real span with the same energy rule as every other slot,
  which is what it does now.
- **I started a second render job while the first was still running**, and the
  two overwrote each other's output files: the master came back with no moov
  atom and 0 frames while its log stopped mid-render. Entirely my process
  management.
- **A per-frame degenerate refusal was killing the whole render.** "Refused"
  has to mean nothing is drawn on that frame; it was raising through the build.
  Now it is caught, counted and reported.
- **`--expect-frames 915`** — I passed the builder's own claim instead of
  checking what the encoder writes, and gate 1 failed on my arithmetic, not on
  the file.
- **The cache key I added put a `/` in a filename** and crashed the solver on
  the first run.
- **I reported "identity refusals: 0" as a result in an earlier message of this
  round.** It was true only in the sense that nothing had been asked.

## Unsure

- **The accusation section's footage is PSG and Al Hilal era while every card
  predates 2015.** The cards are the accusations and they are period-correct;
  the footage under them is him playing, chosen by the story file's slot rules,
  which I did not change. If you want the adversity movement constrained to
  Santos/Barcelona/Brazil-before-2015 too, that is one line in
  `configs/story_neymar.json` and a re-plan — but it would shrink the pool a
  lot and I did not want to make that call for you.
- **Converge sits on a tunnel shot.** It is the only segment where converge was
  legal and the motion gate passed. The celebrations would be its natural home
  and they all measure under 1.5 hw/s. Lowering the motion gate for converge
  specifically would place it better and I have not measured what else that
  would let through.
- **One frame of ink vanishes** (f840, seg 18, white on the lime away kit after
  the grade). One of 26 frames with ink. I have not changed the shadow for it.
- **The 2013 archive gets no identity match**, so if you ever want ink on the
  archive shot the reference set would need young-Neymar faces in it. As it is,
  the archive is exempt and carries nothing, which is what the style intends.
- **I have not re-verified the three previously delivered edits** against the
  identity bug. They were solved by calling `solve_cache` directly with
  `--athlete`, which is the path that works, so I believe they are fine — but I
  did not re-run them to prove it, and "I believe" is not a measurement.
