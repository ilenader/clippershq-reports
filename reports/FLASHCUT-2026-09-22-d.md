# 2026-09-22-d — the other three edits were identity-confirmed all along; the 1.41 head box was the referee, not the fit; and two overlays were being drawn into thin air

**Round metadata:** delivered `2026-09-22_neymar_v02-era-converge.mp4` — converge
on the treble celebration, the accusation section period-correct, six gates
passing. Proved Messi v4 / Vinícius v3 / Haaland v3 were solved WITH identity
and need no re-render. Added the sixth gate, the solver's refusal, the render
lock, the footage-era constraint, young faces in two reference sets. Three new
defects found and fixed on the way, one of which had been drawing nothing at
all.

## The video

    C:\Users\<PROFILE>\Desktop\flashcut-renders\2026-09-22_neymar_v02-era-converge.mp4
    (repo copy: output/neymar_v02.mp4)

## The paragraph

Everything you asked for is done and measured. **The other three edits had
identity on**: their delivered solve files — preserved and hashed before
anything touched them — carry `face_samples > 0` on every tracked segment, 11 /
4 / 9 identity refusals, and every inked segment identity-confirmed; re-solving
them under the current 0.30 + floor rule reproduces that and recovers one more
segment each for Vinícius and Haaland. **No re-render is needed.** The solver
now **refuses to run without `--athlete`**, and the sixth gate reads the solves
the render was built from and fails if any inked segment has no face sample
behind it — with a control that strips the samples and confirms it fires. **The
head box was the referee**: against 12 hand-marked heads the drawn box is
**p50 0.968**, not 1.41 — the independent detector finds the FACE and the
bracket bounds the HEAD, and on the closing close-ups, where his hair has
volume, the drawn box is if anything **too small at 0.77**. **The motion gate
no longer bans the payoff**: after the drop, narrative position replaces
motion, and converge now sits on the **treble celebration at 20.37 s**, not a
tunnel — density **19%**, inside your band. **The footage-era rule is in the
planner**, derived rather than hand-set (the `era` rank of each club folder
against the club the drop happens in), and the audit says Messi and Haaland
were already clean, Vinícius has a single-club library, and Neymar had **9 of
11** accusation segments on post-turn footage — now **0**. The render takes a
**PID lock** that names the holder and never kills it. And the f840 "vanishing
ink" was not a contrast failure at all: it was **27 pixels** of a bracket drawn
almost entirely outside the crop window, which exposed two worse things — the
overlay gate was assigning looks to segments where the subject's head is off
the window on **100% of frames**, so segment 8 of the v01 edit was written into
the index as an overlay and **drew nothing on all 23 frames**; and the contrast
tool was judging frames where no ink exists at all, which is how 15 frames of
the Haaland edit read as "ink vanished 100%" when the real signal was **1 luma
of encoder noise** between a master and a twin built days apart. Both are
fixed. Across all five edits the worst-case ink-or-shadow contrast is now
**40 – 130 luma with zero vanishing frames**.

## 1. The other three edits: identity was on

Two independent pieces of evidence.

**What actually shipped.** The solve files those renders were built from were
copied and hashed before anything in this round ran
(`build/work/delivered_solves/`, sha256 `8a6df831f67b74d3` Messi,
`dbcfe3b38d2bcc7c` Vinícius, `cceca98a46496eb3` Haaland,
`9a7cfa2de2e0488b` Neymar):

| edit | tracked segments | `face_samples == 0` | identity refusals | inked segments with no face behind them |
|---|---|---|---|---|
| Messi v4 | 10 | **0** | 11 | **none** |
| Vinícius v3 | 16 | **0** | 4 | **none** |
| Haaland v3 | 14 | **0** | 9 | **none** |

Per inked segment, the confirmed similarity: Messi seg5 0.57 / seg7 0.53 /
seg11 0.44; Vinícius seg4 0.70 / seg8 0.73 / seg9 0.67 / seg11 0.51 / seg15
0.62 / seg22 0.55; Haaland seg7 0.51 / seg8 0.61 / seg10 0.55 / seg14 0.54 /
seg19 0.61. Every one of them had a face.

**Re-solved now**, at 0.30 with the 0.05 subject-area floor: Messi unchanged
(10 tracked, 11 refused), Vinícius 16 → **17** tracked and 4 → 3 refused,
Haaland 14 → **15** tracked and 9 → 8 refused. Still `face_samples == 0` on
nothing, still no inked segment blind. The lower threshold recovers a segment
each in two edits; it does not change who was chosen anywhere ink was drawn.

**So: no re-render.** What went wrong was confined to `plan_verify`, and those
three were solved by calling `solve_cache` directly with `--athlete`.

**Deliverables:** `build/work/delivered_solves/`, `build/work/resolve_*.json`,
`build/work/identity_audit.json`.

## 2. Making it impossible

**The solver refuses.** `--athlete` was optional and defaulted to `None`;
`solve_cache.py` now exits with an explanation unless it is given one, and the
only way past is an explicit `--no-identity`, which prints
`!! solving with the OLD SUBJECT SCORE. Do not render this.` Same shape as the
coordinate-space boundary: the unsafe path has to be spelled out.

**The sixth gate.** `delivery_gates.py --solves` reads the solves the render
was built from and fails if any segment in the config's `track_plan` has no
face samples or no confirmed identity:

```
  control identity: face samples stripped -> 7 of 7 inked segments read blind -> fires
  ...
  6 identity OK   7 inked segments, every one identity-confirmed (0.51-0.87); 18 segments carry face samples
```

The control deep-copies the solves, strips `face_samples` and `identity` from
the inked segments, and asserts the gate would fail on that. If it does not
fire, no verdict is given at all.

**The cache knows the rule.** The solve cache key now carries the threshold,
the size floor AND the size of the reference set
(`_id-neymar@0.30-a0.050-r36`), so neither a threshold change nor adding young
faces can be served a stale answer. It could before.

## 3. The head box: it is the referee

Twelve heads hand-marked on the delivered edit off a 25 px grid
(`datasets/heads/neymar_marks.json`, sheets in `build/work/hm_zoom/`), marked
as *the smallest box containing the head including hair, excluding the neck* —
which is what the bracket is drawn around. No detector anywhere in the chain.

| | drawn / hand-marked head |
|---|---|
| p10 | 0.771 |
| **p50** | **0.968** |
| p90 | 1.282 |
| min / max | 0.766 / 1.405 |

Centre distance from my marks: **p50 0.248 head widths**, p90 0.435, max 0.515.

**So the 1.34–1.41 is the referee.** `measure_overlay` scores the bracket
against a head found by an independent detector, and that detector finds the
**face**: on f885 it reports a head 239.8 px wide where my mark is 455 px,
because his hair is not in its answer. Against the face, a box drawn around the
head is 1.4×. Against the head, it is 0.97×.

**What the marks DO show is a spread, and that is the fit's fault.** Sorted by
shot: the short-hair profile f430 is **1.40**, the front-on PSG shots 1.12–1.28,
and the six closing close-ups where his hair has volume are **0.77–0.90** —
the box is too big on a tight skull and too small on a big head of hair.
`headsize.py` fits from ear / eye / nose-ear spans, none of which see hair. The
fit is right on average and wrong per shot by the hair, which the 28 hand-marked
heads it was fitted on evidently did not span. **From now on both numbers get
reported**: against the referee and against hand marks, and they are different
questions.

**Deliverables:** `tools/head_marks.py`, `datasets/heads/neymar_marks.json`,
`datasets/heads/neymar_marks_scored.json`, `build/work/hm_zoom/`.

## 4. The motion gate, the payoff, and two overlays drawn into thin air

**The payoff rule.** A segment is now eligible if it passes the motion gate
**or** it sits after the drop (`slot_kind` in `drop`, `out`). The gate is
unchanged before the drop, where it is doing the right job. And the density cap
— which sorts by motion and throws the slowest away first — now sorts payoff
segments **last**, because on the first run it undid the payoff rule one line
after it fired: the treble celebration is the slowest thing in the edit, so it
was the first overlay the cap discarded.

Result: **converge on seg 14, the Berlin treble celebration at 20.37–22.03 s**,
at 0.3 hw/s, placed on narrative position. Density **5.7 s = 19% of runtime**,
7 of 21 segments, at the cap you set and not over it.

**The thing this uncovered.** Chasing the f840 "vanishing ink" led to a
silent failure: `overlay.render` returns without drawing when the head box is
outside the crop window — correct behaviour, you cannot draw on a man who is
not in the picture — but nothing counted it, and the index still recorded the
segment as carrying an overlay. Measured on the v01 edit:

| segment | frames | head on-window | ink actually drawn |
|---|---|---|---|
| seg 7 | 10 | 100% | 10 |
| **seg 8** | **23** | **0%** | **0** |
| seg 18 | 35 | 57% | 25 |

Segment 8 is the fastest shot in that edit (5.3 head widths/s) and the framing
solve — low-passed and velocity-capped by design — simply could not keep the
window on him. It was assigned `box`, written into the index, counted by gate 6
as an inked identity-confirmed segment, and **drew nothing on all 23 frames**.
The overlay gate now measures on-window fraction per segment and will not place
a look below **60%**; three segments of the new plan are refused on it.

## 5. The footage era

Derived, not hand-set. Each story file already ranks its club folders
(`era`), and `slot_clubs["drop"]` names the club the turn happens in — so the
accusation-era clubs are those ranked at or before the turn, and anything after
it, or missing from the ranking entirely, is out. `tools/story.py` fills the
`open` / `build` / `late` slots with that unless the story pins them itself.

**The audit, all five:**

| edit | accusation segments | from post-turn footage |
|---|---|---|
| Ronaldo v01 | — | the era rank was hand-set per slot; Sporting CP / Man United ARE the young era and are where its archive draws |
| Messi v4 | 11 | **0** — already clean |
| Vinícius v3 | n/a | single-club library, no era ranking derivable |
| Haaland v3 | 13 | **0** — already clean (Dortmund and City both predate the treble) |
| Neymar v01 | 11 | **9** — PSG ×4, Al Hilal ×4, and one more |
| **Neymar v02** | **11** | **0** |

The new Neymar accusation section is Barcelona and Brazil only. The drop keeps
one PSG shot, which the rule allows: the payoff is allowed to be later, that
being the point of it.

## 6. Young faces

`identity.py young` builds a candidate sheet from the clips the STORY calls
young or archive — the same list already read off contact sheets — and offers
them without a threshold, because these faces are *expected* not to match; that
is why they are needed. `add-young` merges the chosen ones and keeps the old.

| athlete | offered | added | note |
|---|---|---|---|
| **Neymar** | 15 from 4 archive clips | **12** (24 → 36) | 3 rejected: they are **Fred**, not Neymar |
| **Haaland** | 24 Dortmund faces | **5** (24 → 29) | the low-scoring profiles; his archive already matched at p50 0.72 |
| Messi | 21 | **0** | the sheet is mostly opponents in old Argentina matches; the one clear Messi already scores 0.59. There is no younger Messi era filed in the library |
| Vinícius | — | — | no earlier era filed separately |

**It did not rescue the archive shot.** Neymar seg 13 (the 2013 Brazil archive)
still refuses: best similarity **0.25** against the enlarged set, under the 0.30
threshold. I did not lower the threshold to force it — that would undo a
measured choice for one segment. The archive is exempt, so it plays; it carries
no ink.

## 7. The render lock and the contrast re-check

**The lock.** `tools/render_lock.py`; `build_edit.py` takes it on `--out`.
A second render on the same path refuses and names the pid and its age. A lock
whose pid is no longer a live python process is reported as stale and taken
over. It **never kills the holder** — that is the repo's SAFETY rule, and "my
lock file is old" is not evidence the other process is dead. Both directions
are tested: a live holder refuses, a dead one is taken over, the file is
removed on exit.

**f840 was not a contrast failure.** There is no bracket on that frame at all —
the head sits on the window edge and the ink is off-picture. The tool declared
"ink vanished 100%" from **27 pixels**, because its floor for judging a frame
was 20. Two fixes: the floor is now **200 px** (a bracket is a few thousand),
and frames outside an indexed overlay segment are **not judged at all** — which
is what was producing 15 "vanished" frames on the Haaland edit, where the real
signal was ~1 luma of encoder noise between a delivered master and a twin
rebuilt days later.

**Worst-case contrast, all five, on the delivered pixels** (ink-or-shadow
per-frame p10; the control fires on every run):

| edit | frames with ink | p50 | **worst** | frames where ink vanishes |
|---|---|---|---|---|
| Ronaldo v01 baseline | 16 | 150.5 | **105.0** | **0** |
| Messi v4 | 11 | 154.0 | **127.6** | **0** |
| Vinícius v3 | 18 | 142.0 | **130.0** | **0** |
| Haaland v3 | 6 | 107.1 | **40.0** | **0** |
| Neymar v02 | 11 | 116.0 | **110.0** | **0** |

Haaland's 40.0 is the real floor of the set — one frame of seg 19 — and it is
at the 40-luma line rather than under it.

## 8. The delivered edit

Cards unchanged from the approved list: **CIRCUS · ALL TRICKS · SHOW PONY · NO
SUBSTANCE · CLOWN · ACTOR · FAKER · FRAIL · HYPED · SOFT · BRAND · DIVA ·
NEYMAR**.

Inked segments, all identity-confirmed:

| seg | t | look | identity | face samples |
|---|---|---|---|---|
| 8 | 14.30 | box | 0.51 | 2 |
| **14** | **20.37** | **converge** | 0.66 | 4 |
| 15 | 22.03 | skeleton | 0.61 | 4 |
| 19 | 28.97 | box | 0.87 | 1 |
| 20 | 29.23 | box | 0.58 | 1 |
| 21 | 29.47 | box | 0.67 | 1 |
| 22 | 29.93 | box | 0.72 | 1 |

**Six gates:**

```
  1 frames   OK
  2 freeze   OK  (on the grain-free render)
  3 cards    OK  13 scheduled, 13 rendered, 13 runs in the file
  4 flash    OK   13.87s:+32  14.37s:+33  15.80s:+31  16.77s:+31  21.33s:+29
  5 overlay  OK   bracket->head p50 0.09  worst 0.73 head widths (gate: p50 <= 0.5)
  6 identity OK   7 inked segments, every one identity-confirmed (0.51-0.87)
  ALL 6 GATES PASS
```

**Bracket → head** (referee): pre-grade p50 0.103, post-grade **p50 0.091**,
93.8% within 0.5 hw. **Size ratio**: referee p50 **1.338**, hand-marked p50
**0.968**. **Converge centre → head** p50 0.211, 64.7% within 0.5 hw.

**Five worst frames:** `build/work/neymar_worst/worst_f0879.png`, `f0882`,
`f0885`, `f0894`, `f0897` — all `box`, all in the closing close-ups, the worst
0.73 head widths on f882 where the referee's head is 146 px against a drawn box
of 327.

## Deliverables

| path | what |
|---|---|
| `<PROFILE>\Desktop\flashcut-renders\2026-09-22_neymar_v02-era-converge.mp4` | **the video** |
| `output/neymar_v02.mp4`, `_index.json` | repo copy and the look index |
| `tools/render_lock.py` | one render at a time, per output path |
| `tools/head_marks.py` | drawn box vs hand marks, no detector |
| `datasets/heads/neymar_marks.json`, `_scored.json` | the 12 marks and their score |
| `tools/delivery_gates.py` | gate 6 and its control |
| `tools/solve_cache.py` | the refusal, the rule in the cache key |
| `tools/story.py` | the derived footage-era constraint |
| `components/overlay/overlay_gate.py` | payoff rule, on-window rule, cap ordering |
| `components/identity/identity.py` | `young` / `add-young`, threshold and floor |
| `tools/ink_contrast.py` | the 200 px floor and the index guard |
| `build/work/delivered_solves/` | the as-delivered solves, hashed |
| `build/work/resolve_{messi,vinicius,haaland}.json` | the re-solves |
| `build/work/identity_audit.json` | per-segment identity, all four edits |
| `build/work/{messi,vinicius,haaland,ronaldo}_clean_twin.mp4` | the graded twins the contrast check needed |
| `identity/{neymar,haaland}/young_candidates.png` | the young-face sheets, for your eyes |
| `build/work/neymar_v02_strip.png` | the delivered arc |

## Assertions at close

- 914 frames, 30.50 s, 1080x1920, libx264. Six gates pass, every control fires.
- Density **19%**, 7 of 21 segments, all three looks placed, converge on the
  celebration.
- Accusation section: **0 segments** from post-turn footage.
- Every inked segment identity-confirmed, 0.51–0.87, face samples 1–4.
- opencv still 4.14.0; nothing was installed this round.
- The chrome-guard hook still blocks `tests/test_no_kill_by_name.py` and I did
  not work around it. Nothing this round terminates a process — the render lock
  explicitly does not.

## What I got wrong

- **I claimed the f840 ink "vanished" and treated it as a contrast defect.** It
  was 27 pixels of a bracket that is almost entirely outside the picture on a
  frame that carries no visible overlay at all. I reported it from the tool's
  output without looking at the frame. Looking at the frame took one minute and
  changed the diagnosis completely.
- **The first fix I wrote for the payoff rule was cancelled by the next block
  of code.** The density cap sorts by motion, so the celebration — the slowest
  segment — was the first thing it threw away, and the rule I had just added
  did nothing. I only caught it because converge still was not in the output.
- **I built the overlay gate's look assignment without ever checking that the
  look could be drawn.** Segment 8 of the v01 edit was assigned, indexed,
  counted by a gate and rendered as nothing, for 23 frames. The index said
  there was an overlay; there was no overlay.
- **My first cache-key fix put a `/` in a filename** and crashed the solver
  on its first run of the round.
- **I wrote gate 6's control against `a.solves` inside a function that has no
  `a`**, and the patch half-applied — the tool briefly had a control for a gate
  that did not exist yet.
- **I re-checked contrast against twins rebuilt days after their masters**, got
  15 "vanished" frames on Haaland, and nearly reported a delivered edit as
  broken. The masters and the twins differ by about 1 luma of encoder noise
  everywhere; that is not something the tool should have been able to read as
  ink.

## Unsure

- **My head marks are good to about ±10% on width**, read off a 25 px grid on
  soft-edged hair, which is the same order as the spread I am reporting. The
  p50 of 0.968 is solid enough to answer "referee or fit"; the per-shot spread
  0.77–1.40 I would not quote to two decimals.
- **The hair problem is diagnosed but not fixed.** `headsize.py` fits from ear,
  eye and nose-ear spans, none of which can see hair volume, and I have not
  refitted it. Doing that properly means new hand marks across athletes with
  different hair, not a constant nudged on Neymar.
- **The on-window floor of 60% is a first choice, not a measured one.** I know
  0% is wrong and 100% would be too strict; I have not swept it.
- **Haaland's worst-case ink contrast is 40.0**, exactly on the line the tool
  calls vanishing. One frame. I have not looked at whether it reads badly to
  the eye.
- **Vinícius has no era ranking**, so the footage-era rule cannot apply to him
  at all. His library is one club and one period, so nothing is wrong today,
  but the rule will silently not protect that edit if the library grows.
- **I have not re-rendered the other three** under the 0.30 threshold. They were
  delivered at 0.40, identity-confirmed, and the re-solve says 0.30 would
  recover one segment each for Vinícius and Haaland. That is a change worth
  making next time they are rendered, not a reason to reissue them now.
