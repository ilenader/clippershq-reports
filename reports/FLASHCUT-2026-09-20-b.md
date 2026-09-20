# 2026-09-20-b — The subject score was choosing bodies by size; measured against hand labels it goes 60% → 70%, and its ceiling is identity, not weights. Messi v1 is rendered, five gates pass, and its converge mesh sits at 0.24 head widths on the sky celebration.

**Read this first:** Messi v1 has **no Lusail footage** — the World Cup is in the library only as the trophy presentation, so the turn that the whole edit builds to (NO WORLD CUP → the goals) has no goal on screen; it lands on the trophy in the bisht and nothing else. The Lusail goals are the first item on the supply list (§7). Judge the mechanics on this version, not the payoff.

**Round metadata:** delivered `2026-09-20_messi_v01-clean-v1.mp4` (five gates pass; card words are the de-duplicated Messi script below, pending your approval — one config edit and a 4-minute re-render to change); committed `8b2d4d7` (subject truth) and this round's builder/gate/story work; de-duplicated scripts for all five athletes in §1; Haaland kept on option (a), §2; Vinícius rewritten with the abuse off, §3; one-game basketball carve done, §5; NOT done: the other four edits (waiting on scripts), Vinícius/Haaland carving (running in the other session, not in this report), Lusail goal footage (not in the library).

## The paragraph

Thirty shots were hand-labelled from contact sheets for which body is the subject (`docs/subject_truth_2026-09-20.json`); the SPEC.md weights choose right in **18/30 (60%)**, and area 0.4 / centrality 0.6 / motion 0.5 / persistence² from zero choose **21/30 (70%)**, fixing v01 seg 4, seg 3 and two Curry shots and breaking none of the football ones — but on the four in-game basketball labels the new weights go 2/4 → 1/4, and every remaining miss is the same shape: subject and picked body both present ~100% of the frames, the other bigger or nearer centre (Poole's back over Curry's face). No weighting of size, centre, motion and persistence separates those; identity does, and the score has none — so every overlay shot in a delivered edit is confirmed on a contact sheet by a person before rendering, which is what caught the v6 seg 16 trail on a Spurs player and the Messi trophy handover locking onto the Emir. The one-game carve says basketball is **in**: Curry Games 10 cuts into 95 shots, median **6.7 s**, 49 in the 3–8 s band; Games 1 was a 283-cut mixtape and is the exception, not the rule. Messi v1 is built from one config through the one builder: the bench opener (hands over his face, 5.9 s, nothing drawn), the 2018 Nigeria runs, the 2006 boy as the archive, the Qatar trophy in the bisht on the drop, the sky celebration as the long shot with the mesh, Copa 2021 fingers to the sky, and the trophy again to close. Measured on the delivered pixels: box **p50 0.18 / p90 0.95 / max 1.20** hw graded (0.17 / 0.92 raw), converge centre **p50 0.24 / p90 0.55 / max 1.79**, 85% within 0.5, endpoints on independent keypoints 72% per frame; `ALL 5 GATES PASS`. Two gates fired first and were right to be examined: the freeze gate reads stillness under grain as a freeze (fixed by reading the grain-free render), and the flash gate measured across a cut (fixed by taking the brighter neighbourhood as baseline; the +32 flash reads +26..+33 now on both edits). What the Messi footage cannot do: pay off PENALTY MISSER (no penalty in the folder) or show Lusail's goals (the World Cup is in the library only as the presentation) — those are on the list to supply.

## 1. The five card scripts, de-duplicated

Rule applied: an accusation stays with the player it was said about loudest; the Ronaldo v01 cards count as taken (FINISHED, CAN'T DRIBBLE, OVERRATED, PENALTY MERCHANT, ONLY TAP-INS, FLAT-TRACK, TOO SLOW, PAST IT, SELFISH, NO LEFT FOOT, DONE, TOO OLD). Every card below appears in exactly one script. Two tiers: 4 at 5.97 / 7.87 / 9.80 / 11.70 (0.33 s each), 9 at 13.57 … 17.30 (0.17 s each), the 13th is the name, ending on the frame the hole starts.

**MESSI** — turn: the World Cup in the bisht (as rendered)
```
slow:     PESSI · NO WORLD CUP · CHOKER · DOESN'T SING
pile-on:  MADE BY XAVI · GHOST · PENALTY MISSER · RETIRED 2016 · STOKE · FRAUD · ZERO COPAS · PSG PASSENGER
name:     MESSI
```
Changes: SYSTEM PLAYER → MADE BY XAVI (the form it took for him); FINISHED → PSG PASSENGER (FINISHED was Ronaldo's; the PSG years were the loudest "finished" said about Messi and the card is specific to them). CHOKER stays with Messi — three lost finals 2014–16 is where that word was used, Giannis gets his own. PENALTY MISSER has no penalty footage to destroy it in the library (see §7); keep it only if you can supply the Copa 2021 shoot-out.

**VINÍCIUS** — turn: Paris, 28 May 2022, 59'
```
slow:     CONE · CAN'T FINISH · DIVER · CRYBABY
pile-on:  DANCER · SHOWBOAT · €45M FLOP · NO END PRODUCT · ALL PACE NO BRAIN · PROVOCATEUR · CRY TO THE REF · SECOND PLACE
name:     VINÍCIUS
```
Changes: BALLON D'OR? NO → SECOND PLACE. The abuse is off entirely, per your call. The drop is built on the Paris goal.

**HAALAND** — option (a): the accusation is volume and the league; the turn is the 36 and the treble as a body of work
```
slow:     ROBOT · FARMERS' LEAGUE · PENALTY BOX ONLY · THE PREM WILL EXPOSE HIM
pile-on:  BUNDESLIGA BULLY · ONE SEASON WONDER · NEEDS DE BRUYNE · NO FIRST TOUCH · NEVER PASSES · 20 GOALS MAX · PEP'S PUPPET · STATS PADDER
name:     HAALAND
```
Changes: MISSING IN MADRID and NO BIG GAMES are gone (Istanbul cannot destroy them); CAN'T DRIBBLE → NO FIRST TOUCH (CAN'T DRIBBLE was Ronaldo's); CAN'T PASS → NEVER PASSES; SYSTEM STRIKER → PEP'S PUPPET; OVERHYPED dropped. Every card left is destroyed by a goal count on screen — the drop is a run of goals and the trophies, not one moment. Why (a) and not Jokić: the Haaland footage IS volume footage (68 City compilations, 173 minutes of goals) and matches the accusation; Jokić's folder is 22 game files not yet carved. If you want the single-moment shape for all five, swap to Jokić and I carve.

**CURRY** — turn: Boston, 16 June 2022
```
slow:     TOO SMALL · GLASS ANKLES · WON'T LAST · NO DEFENSE
pile-on:  SYSTEM PLAYER · CAN'T CREATE · NEVER FINALS MVP · BLEW A 3-1 LEAD · LEBRON'S SHADOW · LUCKY SHOTS · KD CARRIED HIM · NOT TOP 10
name:     CURRY
```
Changes: SYSTEM PLAYER stays with Curry (the Warriors-system debate is the loudest use); WASHED → KD CARRIED HIM (specific to 2017–18; WON'T LAST already covers the draft-era doubt).

**GIANNIS** — turn: Game 6, 20 July 2021, 50 points, 17/19
```
slow:     CAN'T SHOOT · NO JUMPER · ALL ATHLETE · SKINNY KID
pile-on:  WALL HIM OFF · FREE THROWS · SECOND ROUND · NOT A CLOSER · NO FOURTH QUARTER · TWO MVPS NO RING · BUCKS BUST · LEAVE MILWAUKEE
name:     GIANNIS
```
Changes: CHOKER → SECOND ROUND (the 2020 exit); GOES MISSING → NO FOURTH QUARTER; OVERRATED → TWO MVPS NO RING (the specific 2020 line); + LEAVE MILWAUKEE.

Cross-check: 65 cards, 65 distinct strings, none shared with Ronaldo v01.

## 2. Haaland

Kept, on option (a) — see the script above and its rationale. The accusations now name volume, the league and the supply line; the footage in the library is 173 minutes of goal compilations, which is the only thing that destroys "20 GOALS MAX" and "FARMERS' LEAGUE": the number on screen. The drop is a run of goals into the treble, no single moment. If that shape is wrong for the set, Jokić is the swap and his folder (22 game files, 107 min) needs the carve first.

## 3. Vinícius

Abuse off entirely, per your decision. "BALLON D'OR? NO" → "SECOND PLACE". Paris 59' is the drop. Footage is 97 Real Madrid compilations (117 min) that need carving; the peer session is carving them now and the numbers are not in this report.

## 4. The subject score, measured

**Ground truth:** 34 shots collected (`tools/subject_truth.py collect`), each tracked once with every candidate chain boxed and numbered at three moments (`build/work/truth_sheets/`), labelled by me from the sheets into `docs/subject_truth_2026-09-20.json`. 30 labelled; 4 unlabelled and why: v01 seg 9 (the subject striking the ball is motion-blurred and not a candidate), v01 seg 16 (wide shot, the subject never a candidate over 20% presence), curry_game01 (Curry not in the shot), curry_game04 (cannot identify #30 at that size — I do not label what I cannot see). Sources: 17 v01 segments, 6 Curry mixtape shots, 5 Messi clips, 6 in-game shots carved from Curry Games 10.

**Accuracy, same 30 shots:**

| weights | right | wrong (truth → picked, presence, area) |
|---|---|---|
| SPEC.md: area 1.0, centrality 0.6, motion 1.1, persistence linear from 0.3 | **18/30 = 60%** | v01_seg03 1→2 (100%/.20 vs 100%/.19), v01_seg04 3→2 (92%/.17 vs 46%/.25), curry_mix00 1→2, curry_mix03 6→4 (100%/.09 vs 100%/.28), curry_mix04 1→6 (100%/.28 vs 56%/.25), curry_mix05 1→2 (100%/.18 vs 78%/.34), messi00 1→9, messi01 4→5, messi02 1→2, messi04 11→4, curry_game00 3→2, curry_game02 3→20 (57%/.03 vs 8%/.07) |
| measured: area 0.4, centrality 0.6, motion 0.5, persistence² from 0 | **21/30 = 70%** | curry_mix00, curry_mix03, messi00, messi01, messi02, messi04, curry_game00 3→8, curry_game02 3→1, curry_game05 6→2 (92%/.08 vs 97%/.06) |

**Flips:** fixed v01_seg04 (the required one), v01_seg03, curry_mix04, curry_mix05; broke curry_game05 (a 5% persistence edge beat a 33% area edge). On the 26 football + mixtape shots the same weights are reached by 25 of 432 grid combinations (not fragile); on the full 30 exactly one combination reaches 23/30 and it is not taken. Persistence beats area once a track is long enough: shown by seg 4 (92%/.17 over 46%/.25), curry_mix04 and curry_mix05, all fixed by squaring persistence and halving the area exponent.

**The ceiling:** the nine still wrong are all "both present the whole shot, the other is bigger or more central". No exponent on these four features changes which of two 100%-present bodies is chosen except by size or centre, and the subject is neither. That is identity. The consequence for delivery is a process, not a number: every segment that carries an overlay is confirmed on a sheet before the render (§6 did it for 12 segments and moved one).

**In-game basketball:** 2/4 old, 1/4 new — too few to conclude, and the shape of the misses is the identity case again. Basketball edits get the same sheet check.

**Deliverables:** `tools/subject_truth.py`, `tools/shot_track.py` (`features()` / `choose()` / `DEFAULT_WEIGHTS`, `SPEC_WEIGHTS` kept), `docs/subject_truth_2026-09-20.json`, `build/work/truth_cache.json`, `build/work/truth_sheets/*.png`.

## 5. The one-game carve

`tools/carve.py` (PySceneDetect, the same detector the references were measured with), seven long basketball files:

| file | length | shots | p10 / p50 / p90 s | < 1 s | ≥ 0.7 s | 3–8 s (minutes) | > 8 s |
|---|---|---|---|---|---|---|---|
| Curry Games 1 (the earlier probe) | 110 s | 283 | 0.22 / **0.27** / 0.58 | 265 | 18 | 2 | 0 |
| Curry Games 2 | 155 s | 17 | 4.0 / 9.9 / 12.6 | 0 | 17 | 5 (0.5) | 10 |
| Curry Games 16 | 186 s | 4 | 16.8 / 36 / 85 | 0 | 4 | 0 | 4 |
| Curry Games 40 | 222 s | 81 | 0.70 / 2.34 / 4.80 | 12 | 73 | 20 (1.5) | 2 |
| **Curry Games 10** | 782 s | **95** | 3.1 / **6.7** / 14.2 | 2 | **94** | **49 (4.5)** | 38 |
| Giannis Games 12 | 186 s | 50 | 1.3 / 2.8 / 6.9 | 3 | 50 | 19 (1.5) | 4 |
| Giannis Games 3 | 703 s | 40 | 0.5 / 10.9 / 41 | 7 | 33 | 5 (0.4) | 22 |
| Jokić Games 4 | 212 s | 30 | 1.6 / 7.7 / 12.7 | 0 | 30 | 10 (0.9) | 13 |

Verdict: the "Games" files are games, not mixtapes; Games 1 was the outlier. Curry Games 10 alone yields 49 pieces in the 3–8 s band and 94 that hold a 0.7 s overlay. Basketball is in, with the §4 caveat on the subject score in clustered play.

**Deliverables:** `tools/carve.py`, `build/work/carve_bb.json`.

## 6. Messi v1

**Story:** `configs/story_messi.json` — hand labels read off five contact sheets of the Argentina folder (96 clips ≥ 2.5 s; the folder is 2018 Russia and 2024 Copa heavy). The story layer now takes a file per athlete (`tools/story.py:load`), with per-slot club rules (the proof draws from Argentina, not a Barça goal) and hand in-points for long clips. `tools/screen_pool.py --story`, `tools/plan_v01.py --story`.

**Plan:** the planner's rule labels ("arms up = celebrate") put two disappointments into the proof — #236 (hand on head after the 2018 exit) and #186 (the 2024 final *injury*, taken three times as the long shot). Both hand-corrected; the drop was then cut by hand:

| seg | time | shot | style |
|---|---|---|---|
| 0 | 0.00–5.90 | #202: hands over his face on the bench, one held shot | none |
| 3, 4 | 6.30–9.80 | 2024 corner; with the referee | box |
| 5, 6 | 10.13–13.57 | 2018 Nigeria: with the ball; the dribble | converge; trail |
| 7–12 | 13.74–17.20 | the Nigeria goal run, the Bayern dribble | converge (8), vector (11), none on the sub-0.4 s cuts |
| 13 | 19.40–20.30 | the 2006 boy vs Mexico (archive) | box |
| 14 | 20.30–22.13 | Qatar: the trophy in the bisht (#191 at 22 s) | none — see below |
| 15–17 | 22.13–27.34 | #229 arms to the sky, one 5.2 s shot | converge, converge, box |
| 18 | 27.34–29.07 | #198 Copa 2021, fingers to the sky | converge |
| 19–22 | 29.07–30.30 | the lift, a hug, Rojo, Messi with the trophy | none |

**Subject verification before rendering (`build/work/messi_subj_*.png`):** 12 tracked segments ≥ 0.7 s, 11 on Messi; seg 14 locked onto the Emir (bigger, central — the §4 ceiling exactly), so it carries no overlay. A first render put a box on the opener; the five worst frames were all that shot — a 139 px bracket (the size ceiling) on a 600 px covered face, scored against a 110 px proxy from a box the frame truncates — wrong as a choice as much as a measurement, and the format's opener is one slow shot with nothing on it. Removed.

**Measured on the delivered pixels** (differencing against the overlay-free twin, independent pose pass, `tools/measure_overlay.py`):

| | graded (delivered) | raw look (same frames, grade off) |
|---|---|---|
| bracket→head p10 / p25 / p50 / p75 / p90 / p95 / max | 0.04 / 0.08 / **0.18** / 0.52 / **0.95** / 1.03 / **1.20** | 0.03 / 0.09 / **0.17** / 0.46 / **0.92** / 1.01 / 5.44 |
| within 0.5 / 1.0 / 1.5 hw | 72% / 92% / 100% (65 frames) | 76% / — / — (71 frames) |
| bracket / head size p10 / p50 / p90 | 0.76 / 0.87 / 1.17 | 0.77 / 0.85 / 1.18 |
| converge centre→head p50 / p90 / max | **0.24 / 0.55 / 1.79**, 85% within 0.5 (73 frames) | 0.21 / 0.91 / 2.06, 75% |
| converge endpoints on an independent keypoint (≤ 0.5 hw), per frame | p50 **72%**, p10 38%, min 18% | p50 62%, p10 39%, min 26% |
| endpoint → nearest keypoint, hw | 0.33 | 0.41 |

Per shot, graded, p50 / p90 / max: seg 3 box 0.36/0.73/1.20 · seg 4 box 0.90/1.09/1.18 (the referee shot: the model's head sits on the ref's shoulder) · seg 5 converge 0.40/0.57/0.75 · seg 6 trail 0.23/0.54/0.57 · seg 8 converge 0.44/0.55/0.55 · seg 11 vector 0.15/0.41/0.51 · seg 13 box 0.08/0.17/0.17 · **seg 15–16 converge 0.14/0.23/0.29** · seg 17 box 0.06/0.18/0.23 · seg 18 converge 0.24/1.01/1.79 (the crowd behind him; 87% ink on person). Ink on the subject's person box: 87–100% on every converge/box shot, 91% trail (the trail extends behind him by design).

The raw max 5.44 is one frame of seg 3 (the corner, small figure, referee found a different head); graded max is 1.20.

**Gates (`tools/delivery_gates.py --config configs/messi.json --clean … --raw … --index …`):**
```
DELIVERY GATES  <PROFILE>/Desktop/flashcut-renders/2026-09-20_messi_v01-clean-v1.mp4
  1 frames   OK
  2 freeze   OK  (on the grain-free render)
  3 cards    OK  13 scheduled, 13 rendered, 13 runs in the file
  4 flash    OK   13.93s:+26  14.27s:+33  15.93s:+28  16.60s:+28  21.43s:+30
  5 overlay  OK   p50 0.17  worst 1.79 head widths (gate: p50 <= 0.5)

ALL 5 GATES PASS (report-only tools are not counted; see docstring)
```

**Two gates fired on the first pass, and both were the gate:**
- freeze: `FROZEN: 1 run(s) at 2.33s 6 frames (0.20s) mean luma 15.6` — inside the bench shot. My MAD series there never drops below 0.354 against the gate's 0.35; a duplicated frame reads ~0.05. Grain re-applied every frame makes a true freeze read ~0.3, which is also what a man holding still reads, so on the graded file the two cannot be told apart. The grain-free `--raw-look` render of the same edit reads `OK (no picture run over 4 frames)`. The gate now reads the raw render when `--raw` is given.
- flash: `15.93s:+41` against a band ending at +41.0. The flash sits on a cut; the baseline (frame+3) was the darker next shot, so a +32 flash measured +41.3. The baseline is now the brighter of the two neighbourhoods (3 frames before, +3..+5 after, black ignored). Both edits: Messi +26..+33, doubters v6 +24..+29.

**Worst 5 frames:** `build/work/messi_worst/worst_f0195.png` (seg 3, 1.20 hw), `worst_f0267.png`, `_f0270.png`, `_f0273.png`, `_f0276.png` (seg 4, 1.03–1.18 hw: the referee shot — bracket on Messi, the model's head on the ref's shoulder).

**What the footage cannot pay off:** PENALTY MISSER (no penalty in the Argentina folder); Lusail's goals (the World Cup exists only as the 2-minute presentation — the bisht and the lift are in; the goals are not). Copa 2021 is two 720p clips.

**Deliverables:** `configs/messi.json`, `configs/story_messi.json`, `build/work/plan_messi_staged.json`, `build/work/solves_messi.json`, `build/work/messi_measure.json`, `build/work/messi_raw_measure.json`, `build/work/messi_subj_a.png`, `messi_subj_b.png`, `build/work/messi_worst/`, `output/messi_v01.mp4`, `build/work/messi_v01_twin.mp4`, `build/work/messi_v01_raw.mp4`, `build/work/messi_v01_raw_twin.mp4`.

## 7. Youth / turn footage to supply, one line each

- **Messi:** in the library (2006 vs Mexico #130/#141/#152; young `messi 10` back #154). To supply instead: **Lusail 2022, the two goals + the celebration, 3 clips, 5–8 s, 1080p**; **Copa 2021 final, the shoot-out or the whistle, 1–2 clips, 5–8 s, 1080p**.
- **Vinícius:** Flamengo 2017–18, red-and-black hoops, a dribble or a goal, 5–10 s, ≥ 720p, no watermark.
- **Haaland:** Bryne or Molde 2016–18, the teenager, a goal or a run, 5–10 s, ≥ 720p.
- **Curry:** Davidson 2008, the NCAA run, 5–10 s, ≥ 480p is fine — the archive slot suits grain.
- **Giannis:** Filathlitikos 2012–13 or the Greece youth games, 5–10 s, ≥ 480p, grain welcome.

## Deliverables

- `<PROFILE>/Desktop/flashcut-renders/2026-09-20_messi_v01-clean-v1.mp4` — 14.3 MB, 914 frames (30.47 s), 1080×1920, aac
- `<PROFILE>/Desktop/flashcut-renders/2026-09-20_messi_v01-clean-v1_index.json`
- `configs/messi.json`, `configs/story_messi.json`, `configs/doubters_v01.json`
- `tools/subject_truth.py`, `tools/carve.py`, `tools/build_edit.py`, `tools/delivery_gates.py` (`--config`, `--raw`, the flash baseline), `tools/shot_track.py`, `tools/story.py`, `tools/screen_pool.py`, `tools/plan_v01.py`
- `docs/subject_truth_2026-09-20.json`, `docs/FORMAT.md` §4
- `build/work/truth_sheets/`, `build/work/messi_subj_*.png`, `build/work/messi_worst/`, `build/work/carve_bb.json`, `build/work/messi_measure.json`, `build/work/messi_raw_measure.json`

## Assertions at close

- Messi v1: 915 frames pushed, 914 in the file (audio-limited, as every delivery); `ALL 5 GATES PASS` as quoted; cards 13/13/13.
- Doubters v6: unchanged file; re-run of the corrected flash gate: `13.93s:+28 14.27s:+31 15.93s:+24 16.60s:+29 21.43s:+28`, OK.
- Migration test (last round): `configs/doubters_v01.json` through `build_edit.py` is `cmp`-identical to the delivered v6.
- `tests/test_overlay_transform.py`: 34 passed, 0 failed, after the subject-score refactor.
- Cache schema v6 (measured weights); every solve in `build/work/solves_messi.json` labelled `space=canonical`, `tbase=source`.

## What I got wrong

- **v6 seg 16's trail is on a Spurs player.** The wide United–Spurs shot: Ronaldo (red, celebrating) never became a candidate chain over 20% presence; the score picked chain 4, a Tottenham player at 73%, the gate passed it, and I drew the trail on him and shipped it. Found only by labelling the shot by hand. The delivered v6 has it. The sheet check before rendering exists because of this.
- **The first Messi render had a bracket on the opener** — the size-ceiling bracket on a face that fills the frame. Wrong as a choice; the format says nothing is drawn on the opening shot. Caught by the worst-frame dump.
- **The planner's "arms up = celebrate" rule put the 2024 final injury and the 2018 exit into the proof**, three cuts of the injury as the long shot. A rule label is not a story label; the drop is hand-cut now and the story file carries the corrections.
- **The flash gate measured across a cut** and would have failed a correct flash by 0.3 luma; last round it passed v6 by luck of which shot was next.
- **The freeze gate cannot tell a still man from a held frame on a grained picture**; it fired on a bench shot. Last round it passed v6 for the same reason it failed here — the threshold sits where grain puts a real freeze.
- **The first cut-detector inside `shot_track` chained a montage across its cuts and called it 93%** (last round's report said the fix was measured; the measurement was on the version before the tracker reset, and the reset needed an ID offset too). Corrected before commit; recorded here because the intermediate number was printed.
- **The Curry probe last round said "12 of 12 shots pass the gate, Curry boxed in 10"** on a mixtape; the game carve shows the mixtape was the wrong file to draw conclusions from.

## Unsure

- Whether the measured weights generalise beyond 30 shots; in-game basketball is 4 labels.
- Whether `#191`'s 2-minute presentation is the Lusail broadcast or a re-edit; it is used only for three short pieces.
- The raw-look referee scores the converge slightly worse than the graded one (p90 0.91 vs 0.55) on the same drawn pixels — the brighter picture yields more detected people and keypoints in the crowd, which the nearest-keypoint metric counts against the mesh. Both numbers are reported; neither is tuned.
- The other session's Vinícius/Haaland carve numbers were not available at close and are not in this report.

## Addendum — the Vinícius and Haaland carve (from the second session, `tools/carve.py`, same detector as §5)

Per athlete, every file over 60 s in the folder, pooled:

| athlete | files | minutes | shots | p10 / p50 / p90 / max s | < 1 s | ≥ 0.7 s | 3–8 s (minutes) | > 8 s | files with median < 1 s (mixtapes) |
|---|---|---|---|---|---|---|---|---|---|
| Vinícius (Real Madrid, 26 files > 60 s) | 26 | 84 | 3795 | 0.23 / **0.42** / 2.88 / 63.7 | 2264 | 1710 | **277 (19.6)** | 37 | 14 of 26 |
| Haaland (City + Dortmund, 35 files > 60 s) | 35 | 137 | 4639 | 0.23 / **0.53** / 3.80 / 119.6 | 2570 | 2206 | **606 (44.1)** | 110 | 18 of 35 |

Shot-length histogram, pooled per athlete (count of shots):

| bin s | Vinícius | Haaland |
|---|---|---|
| 0–0.5 | 1969 | 2282 |
| 0.5–1 | 295 | 288 |
| 1–2 | 735 | 876 |
| 2–3 | 482 | 477 |
| 3–5 | 215 | 453 |
| 5–8 | 60 | 153 |
| 8–15 | 16 | 62 |
| 15–30 | 15 | 25 |
| 30+ | 8 | 23 |

**Vinícius**, per file (length s, shots, median s, 3–8 s pieces): #130 204/220/0.27/16; #132 497/219/1.96/26; #133 85/68/1.04/4; #134 61/29/0.65/10; #135 287/333/0.27/8; #137 87/18/3.05/6; #138 235/100/1.70/19; #139 801/452/0.81/66; #140 277/325/0.25/13; #143 97/131/0.33/4; #144 61/56/0.42/2; #145 62/38/1.99/1; #146 195/121/0.90/7; #148 62/92/0.30/0; #149 192/195/0.30/7; #150 94/7/15.97/2; #156 94/6/16.51/1; #159 97/14/4.66/8; #174 68/36/1.83/7; #175 233/105/2.43/32; #177 154/182/0.27/1; #184 393/626/0.25/11; #185 192/172/0.33/5; #187 183/128/0.64/6; #188 219/112/1.57/14; #205 95/10/2.18/1

**Haaland**, per file (length s, shots, median s, 3–8 s pieces): #100 181/122/1.20/9; #101 180/175/0.27/16; #103 141/167/0.27/17; #104 162/154/0.27/17; #107 257/109/2.00/22; #108 60/103/0.33/4; #109 121/210/0.27/7; #117 135/8/11.64/2; #118 699/53/7.28/18; #119 483/17/32.24/2; #60 62/31/2.20/0; #63 264/160/1.88/4; #76 282/187/0.33/42; #77 257/112/1.83/9; #80 332/71/3.60/29; #81 209/125/1.40/7; #83 123/127/0.28/10; #84 260/147/1.63/4; #85 280/191/1.85/6; #87 330/313/0.33/32; #88 318/127/2.23/38; #89 65/39/0.40/7; #90 235/81/2.83/22; #91 121/37/2.77/14; #93 98/59/1.27/11; #95 248/226/0.33/19; #96 88/342/0.25/0; #97 62/63/0.30/7; #99 211/137/0.40/22; #27 258/126/0.43/37; #28 243/156/0.28/26; #29 234/152/0.28/25; #31 240/249/0.27/23; #32 188/120/0.43/17; #52 793/143/5.12/81

Verdict: both folders are mixtape-heavy by file count — **14 of 26** Vinícius files and **18 of 35** Haaland files have a median shot under 1 s, and 0–0.5 s is the largest bin for both — but the 3–8 s band still pools to **277 pieces / 19.6 min** for Vinícius and **606 pieces / 44.1 min** for Haaland, against the ~15 min of 3–8 s clips per 30 s edit that `docs/FORMAT.md` §4 gives as the v01 sourcing ratio. Both clear it on count. The richest single files: Haaland #52 (Dortmund, 793 s, 81 pieces, median 5.1 s), #76 (42), #88 (38), #27 (37); Vinícius #139 (801 s, 66 pieces), #175 (32), #132 (26). What this does NOT say: whether the player is in the shot, whether a 3–8 s piece in a mixtape is footage or a graphic, or whether it is 1080p — that is the screening and labelling pass (`tools/screen_pool.py`, the contact sheets), not the carve. Wall time: 26 Vinícius files in 24 min, 35 Haaland files in 26 min, CPU only, alongside the Messi renders.

**Deliverables:** `build/work/carve_vini.json`, `build/work/carve_haaland.json` (every shot with its source time, per file, plus the per-file summary).
