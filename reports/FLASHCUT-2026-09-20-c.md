# 2026-09-20-c — Three edits delivered on the approved cards (Messi v2, Vinícius v1, Haaland v1), every gate fired on its control first; the basketball subject score measures 54% and Curry/Giannis stay parked; the celebration classifier decides on evidence (18/22 by eye, zero false celebrations); a watermark scan across shots caught three editors' handles the sheets did not

**Read this first:** Messi v2 still has **no Lusail footage** — the turn lands on the trophy presentation, not a goal (unchanged from v1; the Lusail goals are the first item on the supply list). Vinícius has **no Paris 2022** in the 26 compilations, so its payoff is Wembley 2024; the Paris goal is now the second item on that list.

**Round metadata:** delivered `2026-09-20_messi_v01-clean-v2.mp4` (§3), `2026-09-20_vinicius_v01-clean-v1.mp4` (§7) and `2026-09-20_haaland_v01-clean-v1.mp4` (§8), five gates passing on each with the controls fired first; committed `3bef8e9` (evidence beats a hand celebrate, Messi v2, story blocklist, REPORTING.md), `ca3e9d8` (Vinícius, Haaland configs, the watermark scan), `3f243b4` (card wrap, Haaland), on top of `49f8df7` and `e9d1c9f`; NOT done: Curry and Giannis (parked on the basketball number, §4), Lusail and Paris footage (not in the library), a Vinícius youth era and a Haaland youth era (Dortmund stands in).

## The paragraph

The report channel is a repository now, not a gist: `tools/publish_report.py` PUTs `reports/FLASHCUT-<round>.md` to the public reports repo through the contents API, reads the bytes back, and prints the versioned raw URL; the -b report was re-published that way and fetched back byte-identical, and `docs/REPORTING.md` now says so (it still described the gist until this round — §What I got wrong). The three script fixes are in (`NOBODY KNEW HIS NAME`, `JUST DUNKS`, `COLD NIGHT IN STOKE`) and a one-list checker with a planted-repeat control reads all five scripts against each other and against the delivered Ronaldo cards: **65 cards, 65 distinct, CLEAN**. Messi's 5.44-head-width tail is the referee, not the tracker: on the raw frame the bracket sits on Messi's head and the nearest independently detected head is an **18-px spectator** behind the corner flag. Messi v2 (approved cards) measures **box p50 0.18 / p90 0.95 / max 1.20** hw graded, **converge 0.24 / 0.55 / 1.79**, 85% within 0.5, `ALL 5 GATES PASS`. The subject-score truth set is **44 labelled shots** and the split by sport is the finding: **football 16/20 (80%)**, **basketball 13/24 (54%)**, in-game 9/18 (50%) — Curry and Giannis stay parked; the score margin, tested as a "draw nothing" gate, would refuse 7 overlays a person verified correct and still pass the v6 Spurs trail, so it is recorded and refuses nothing. The celebration classifier decides on evidence — lying in any sample → `down`, hands at the head → `dejected`, sustained arms up → `celebrate`, else `action` — and agrees with a by-eye reading of 22 Messi clips in **18/22 with zero false celebrations**; a hand `celebrate` is now overridden by evidence of `down`. Vinícius is built from **766 shot-clips** cut from 26 compilations; there is **no Paris 2022** in any of them, so the payoff is Wembley 2024. Its first render carried three different editors' handles inside the picture window that no contact sheet and no blocklist had caught, so `tools/watermark_scan.py` now looks for the one thing a compilation keeps constant from shot to shot — edges present in three shots of four — with a planted-handle control; it flagged nine compilations, six of them real on the review sheet, and those six plus one caught by eye are blocked whole. The subject sheet took four overlays off before the render (the referee's head, Marcelo, Ancelotti on the bench) and the harness took one off after it (a mid-clip swap onto a Shakhtar defender). Vinícius v1: **box p50 0.27 / p90 1.11 / max 1.41** graded (0.24 / 0.81 / 1.44 raw), the worst frames all referee misses on close bodies with the bracket on the face; converge **0.30 / 2.24 raw** but **0.88 / 5.38 graded** — on this footage the doubters grade hides faces from the referee, and the mesh was confirmed on Vinícius frame by frame instead (§7). Haaland v1 is the cleanest of the three: **box 0.18 / 0.34 / 0.92**, 95% within 0.5, converge 0.10 / 0.57; its first render failed the card gate honestly — `THE PREM WILL EXPOSE HIM` on one line is a 31× vertical stretch the gate reads as no ink and a reader reads as nothing — so a card past the largest delivered stretch (24×) now wraps to two lines, and the v01 migration was re-proved `cmp`-identical after the change.

## 1. The report channel

`tools/publish_report.py` now: self-test (plants the profile string and the user folder in a copy and confirms the redaction check fires on each, and that a clean copy passes) → redaction check → GitHub contents-API PUT to the reports repository at `reports/FLASHCUT-<round>.md` (the API refuses an existing path; a GET checks first) → read-back and **byte** compare (a text compare refused a CRLF file after the commit had gone through, which is why `--existing` exists) → the raw URL with the commit sha in place of the branch. `docs/REPORTING.md` §The channel now says this and says why gists do not work ("Nobody reaches for a gist again"). The -b report went through it and was fetched back over plain HTTP byte-identical.

**Deliverables:** `tools/publish_report.py`, `docs/REPORTING.md`.

## 2. The three script fixes and the one-list check

Applied in `configs/scripts.json`: Giannis SECOND ROUND → **NOBODY KNEW HIS NAME**; NO FOURTH QUARTER → **JUST DUNKS**; Messi STOKE → **COLD NIGHT IN STOKE**. `tools/check_scripts.py` then reads the five scripts as one list plus the delivered Ronaldo cards, with a synonym table (SYSTEM PLAYER = PEP'S PUPPET = MADE BY XAVI's shape, ONLY TAP-INS = PENALTY BOX ONLY, CHOKER = NOT A CLOSER) and a planted-repeat control that must be caught before the verdict is quoted:

```
control: planted repeats caught (2 problems on the planted copy)
5 scripts, 65 cards, 65 distinct accusations + names
CLEAN: no repeat within a script, across scripts, or against delivered edits
```

It ruled three more: Haaland PENALTY BOX ONLY → NEVER FROM RANGE, PEP'S PUPPET → LEAGUE TWO PLAYER (Keane's own words), Giannis NOT A CLOSER → THAT'S A TRAVEL. The scripts as rendered/approved:

```
MESSI     PESSI · NO WORLD CUP · CHOKER · DOESN'T SING | MADE BY XAVI · GHOST · PENALTY MISSER · RETIRED 2016 · COLD NIGHT IN STOKE · FRAUD · ZERO COPAS · PSG PASSENGER | MESSI
VINÍCIUS  CONE · CAN'T FINISH · DIVER · CRYBABY | DANCER · SHOWBOAT · €45M FLOP · NO END PRODUCT · ALL PACE NO BRAIN · PROVOCATEUR · CRY TO THE REF · SECOND PLACE | VINÍCIUS
HAALAND   ROBOT · FARMERS' LEAGUE · NEVER FROM RANGE · THE PREM WILL EXPOSE HIM | BUNDESLIGA BULLY · ONE SEASON WONDER · NEEDS DE BRUYNE · NO FIRST TOUCH · NEVER PASSES · 20 GOALS MAX · LEAGUE TWO PLAYER · STATS PADDER | HAALAND
CURRY     TOO SMALL · GLASS ANKLES · WON'T LAST · NO DEFENSE | SYSTEM PLAYER · CAN'T CREATE · NEVER FINALS MVP · BLEW A 3-1 LEAD · LEBRON'S SHADOW · LUCKY SHOTS · KD CARRIED HIM · NOT TOP 10 | CURRY
GIANNIS   CAN'T SHOOT · NO JUMPER · ALL ATHLETE · SKINNY KID | WALL HIM OFF · FREE THROWS · NOBODY KNEW HIS NAME · THAT'S A TRAVEL · JUST DUNKS · TWO MVPS NO RING · BUCKS BUST · LEAVE MILWAUKEE | GIANNIS
```

**Deliverables:** `configs/scripts.json`, `tools/check_scripts.py`, `configs/messi.json` (cards), `configs/vinicius.json` (cards).

## 3. Messi's tail, and v2

The -b report quoted raw p100 **5.44** hw against graded 1.20 and did not say why. The worst-frame dump on the raw render says why: frame 192 (seg 3, the corner), the bracket is on Messi's head (`build/work/messi2_raw_worst/worst_f0192.png`), and the referee's nearest head is a spectator behind the corner flag with a **18.2-px** head width — 5.44 of *his* head widths. The next raw entry, 3.86 on the vector segment (f498), is the same shape: the referee took Rafinha's head as "nearest" while the vector sits on Messi's. On the graded render the grade darkens the crowd enough that the spectator is not detected and the frame scores 1.20 against Messi's own head. So the tail is a referee resolution artefact, not a tracking error, and nothing was re-tuned.

v2 = v1's plan re-solved (schema v7) and re-rendered with the approved cards. Measured on the delivered pixels against the overlay-free twin, independent detection, every third frame:

| | frames | p10 | p50 | p90 | p100 | ≤0.5 hw | ≤1.0 hw |
|---|---|---|---|---|---|---|---|
| bracket→head, graded | 65 | 0.04 | **0.18** | 0.95 | 1.20 | 72% | 92% |
| bracket→head, raw | 71 | 0.03 | **0.17** | 0.92 | 5.44 (the spectator) | 76% | 94% |
| converge centre→head, graded | 73 | — | **0.24** | 0.55 | 1.79 | 85% | — |
| converge centre→head, raw | 73 | — | **0.21** | 0.91 | 2.06 | 75% | — |

Converge endpoints on an independent pose keypoint (≤ 0.5 hw): graded per-frame hit rate **p50 0.72**, p10 0.38, min 0.18, endpoint→nearest keypoint p50 0.33 hw; raw p50 0.62. Geometric locator vs differencing: found in 45 of 67 frames, centre disagreement p50 0.5 px / p90 5.0 px.

Per panel (graded): seg 3 box 0.36/0.73/1.20, seg 4 box 0.90/1.09/1.18 (the size-ceiling bracket on a half-frame face, as in v1), converge 220 0.40/0.57/0.75, trail 222 0.23/0.54/0.57, converge 226 0.44/0.55/0.55, vector 54 0.15/0.41/0.51, box 13 0.08/0.17/0.17, converge 229 0.14/0.23/0.29, box 229 0.06/0.18/0.23, converge 198 0.24/1.01/1.79 (p50/p90/max hw).

Gates, controls first, as printed:

```
POSITIVE CONTROLS
  control freeze : moving clip OK, six held frames FAIL -> fires
  control flash  : +32 measured +31 (OK), +60 measured +59 (FAIL) -> fires
  control cards  : phantom 14th card on doubters_v01_clean.mp4 -> fires
  self-test OK

DELIVERY GATES  output/messi_v01.mp4
  1 frames   OK
  2 freeze   OK  (on the grain-free render)
  3 cards    OK  13 scheduled, 13 rendered, 13 card-like runs in the file
  4 flash    OK   13.93s:+26  14.27s:+33  15.93s:+28  16.60s:+28  21.43s:+30
  5 overlay  OK   p50 0.17  worst 1.79 head widths (gate: p50 <= 0.5)

ALL 5 GATES PASS (report-only tools are not counted; see docstring)
```

The controls are synthetic clips written by the gate tool itself: 40 frames of fresh noise with six held frames inside (freeze), a flat grey band with one +32 and one +60 frame (flash), and a phantom 14th card asserted on the delivered doubters file (cards). The gate refuses to give a verdict if any control does not fire. The overlay gate's control is the +200 px sabotage render from the -a round (`tools/overlay_testcard.py --sabotage-dx`), not re-run this round.

**Deliverables:** `<PROFILE>/Desktop/flashcut-renders/2026-09-20_messi_v01-clean-v2.mp4` (+ `_index.json`), `build/work/messi2_measure.json`, `build/work/messi2_raw_measure.json`, `build/work/messi2_worst/`, `build/work/messi2_raw_worst/`, `tools/delivery_gates.py` (`self_test()`).

## 4. The subject score by sport, and the margin

44 of 56 shots on the truth sheets are labelled (`docs/subject_truth_2026-09-20.json`; 12 unlabelled are ones no reading could settle). Evaluated with the measured weights (area 0.4 / centrality 0.6 / motion 0.5 / persistence²):

| set | right | of | |
|---|---|---|---|
| all | 29 | 44 | 66% |
| football (v01 + Messi) | 16 | 20 | **80%** |
| basketball, all | 13 | 24 | **54%** |
| — mixtape (Curry) | 4 | 6 | 67% |
| — in-game (Curry games + Games 10) | 9 | 18 | **50%** |

Wrong: `curry_mix00 curry_mix03 messi00 messi01 messi02 messi04 curry_game00 curry_game02 curry_game05 bb_game02 bb_game06 bb_game08 bb_game13 bb_game14 bb_game15`. The basketball misses are the identity failure from the -b report (subject and picked body both present the whole shot, the other bigger or nearer centre), plus one new shape from the game carve: an **ID swap** mid-shot (`bb_game07`, labelled as a list) where the same body is two chains and the score picks the shorter one. No weight search on the 44 beat the measured set on football without losing basketball, and none lifted in-game basketball above 50%. **Curry and Giannis wait**, per your condition; the number to beat is 50% in-game, and the fix is identity (re-ID or a click-to-pick), not weights.

The score **margin** (best/second score) was recorded on every solve and tested as a gate at 2.0: it would refuse **7** overlays that a person verified correct on the sheets, and it passes v6 seg 16 (the Spurs trail; margin 2.3 — the wrong body wins comfortably). It cannot separate right from wrong on this data, so `solve_cache.py` keeps `MARGIN_MIN = 0.0` with the reason in the source and writes `margin` into every segment for the sheet check.

**Deliverables:** `docs/subject_truth_2026-09-20.json`, `build/work/truth_cache.json`, `build/work/truth_sheets/`, `tools/subject_truth.py`, `tools/solve_cache.py` (schema v7, `margin`).

## 5. Celebration by evidence

The rule that put the injury and the 2018 exit into the Messi proof was "wrists above shoulders in a third of eight frames". `tools/celebration.py` replaces it. Twelve samples across the whole clip, largest body in each, YOLO pose:

- `lying`: torso (shoulder midpoint → hip midpoint) flatter than 45° in **any** sample → `down`. Where the skeleton never finds hips, a box wider than tall in ≥ 60% of samples on a body ≥ 5% of the frame stands in.
- `hands_head`: a wrist within 1.5 head widths of the head centre (or, on a big faceless subject, a wrist in the top third of the box — the hands hide every head point in exactly this shot) in ≥ 15% of samples → `dejected`.
- `arms_up`: wrists above shoulders in ≥ 40% of samples → `celebrate`, only if neither of the above.
- converging bodies / a pile at the end: recorded as supporting evidence (`hug: yes/no`), never the verdict — measured, a hug alone was also a tunnel line-up, an anthem line, a bench and a dribble past two men (13 of 22 fired on it).
- otherwise `action`, the default. Unsure is not a celebration.

Against 22 Messi Argentina clips read by eye (8 celebrations, 4 dejected, 3 down, 7 not): **18/22 on celebrate-vs-not, zero false celebrations**. The four misses are celebrations declined: #136, #180, #184, #191 — the trophy lift and three hug-only celebrations with no arm raised; the story file labels those by hand, and a hand `celebrate` is now overridden by evidence of `down` (`story.label`). The intermediate rules and what each got wrong: box aspect for "upright" read 14/22 close-ups as lying; `hands_head` at 0.30 missed the hand-on-head exit (#236, fires in 2 of 12 samples); a hug-or-arms rule with a motion floor put the anthem line in.

What the classifier said on the Messi pool (`tools/list_celebrations.py --pool build/work/pool_messi.json --story configs/story_messi.json`), the list a person eyeballs before the render:

```
15 clips labelled celebrate; 10 by hand, 5 by evidence
  HAND     messi Argentina 198 / 201 / 229 / 230     evidence agrees (arms up 58–100%)
  HAND     messi Argentina 136 / 180 / 182 / 184 / 191   evidence "action" (hug-only, trophy) — kept by hand
  HAND     messi Argentina 199                     evidence "dejected" (hands at head 17%) — kept by hand, flagged
  evidence messi Barcelona 427 / 439 / 449 / 450 / 502   arms up 42–100%, no lying, no hands at head
EXCLUDED FROM THE PROOF by evidence: 38 down, 35 dejected
```

The Vinícius list is in §7.

**Deliverables:** `tools/celebration.py`, `tools/list_celebrations.py`, `tools/story.py` (evidence in `label`, downgrade rule), `tools/screen_pool.py` (`celeb` per clip, story blocklist), `build/work/celebration_eval.json`.

## 6. Footage still to supply

- **Messi:** Lusail 2022, the two goals + the celebration, 3 clips, 5–8 s, 1080p. Copa 2021 shoot-out or whistle, 1–2 clips.
- **Vinícius:** **Paris, 28 May 2022, 59' — the goal and the run to the corner, 2 clips, 5–8 s, 1080p** (not in any of the 26 compilations). Flamengo 2017–18 youth, 5–10 s, ≥ 720p.
- **Haaland:** Bryne or Molde 2016–18, 5–10 s, ≥ 720p.
- **Curry / Giannis:** as listed in -b; not needed until the basketball number moves.

## 7. Vinícius v1

**The library.** 26 Real Madrid compilations carved (`tools/carve.py`) and cut into **766 shot-clips** of 2–10 s (`tools/cut_shots.py`, `build/carved/vinicius/`, a manifest tracing each to its source frame). Read off contact sheets: no Flamengo, no youth, and **no Paris 2022** — none of the 26 has the Liverpool final. Wembley 2024 is there four ways (135 s309 the goal celebration, 175 s006/s102 the trophy and the lift, 135 s326 the team, 159 the post-match), so the drop is Wembley. Blocked by name before screening: 139 whole (a reaction video, a webcam picture-in-picture over every frame), 133 whole (mirrored — sponsor lettering reversed), 175 s015/s016 (Mestalla 2023: the abuse stays off entirely), the title cards.

**The screen.** 619 clips screened with evidence (`tools/screen_pool.py --story`): 428 kept, and of those the story labelled 35 celebrate (10 by hand, 25 by evidence), 91 dejected, 81 down. The per-edit list (`tools/list_celebrations.py`): every evidence celebration is arms up 42–100% with no lying sample and no hands at the head; hand labels the evidence disagreed with — 135 s106 and 134 s018 read `dejected` (hands at the head), 175 s012/s070 and 134 s020 read `action` (hug-only, no arms) — were left to the hand label, which is what the sheet said.

**The first render, and what it caught.** Gates passed (`p50 0.23`), and three things were wrong that no gate measures: **"@GODZILLAEDITOR" under seg 3, "nielprod" under seg 8 and "#Leva…" under seg 11** — editors' handles burned into the compilations, inside the window, invisible on a 256-px contact sheet. The harness's raw worst frames also showed **seg 8's bracket on the Shakhtar defender's shoulder** (f429/f432, 7.85 hw) as Vinícius turns his back — a mid-clip swap that the subject sheet's three sample frames had missed. And the opener (159 s001) carried the broadcast score bug and opened on a knee-slide. §9 has the scan that came out of this; the second plan blocked seven compilations whole (138, 177, 188, 149 — handles; 159 — the score bug; 130, 140 — a channel name reaching 30 px inside the window edge), 285 clips remained, and the subject sheet before the second render took the overlay off seg 3 (187 s060: the score chose **the referee's head**, Vinícius arguing with him), seg 11 (7 ids, unconfirmed), seg 16 (the lift: **Marcelo**, 15 ids, 88%) and swapped **Ancelotti on the bench** (205 s003, labelled `run` by the motion rule) out of seg 12.

**The plan as rendered** (23 cuts, 22 clips, Pearson +0.72): opener 175 s079 (warm-up walk, 5.9 s, one shot, ends on him alone) → tunnel s096 → four build shots (the referee, 185 s037, 148 s008, the pink corner flag) → six runs → archive 175 s041 (corridor; no youth footage, so the tunnel stands in) → **drop: 135 s309 goal celebration on the beat, the trophy, the lift, the team, the heart** → four celebrations out, closing on the trophy.

Measured on the delivered pixels against the overlay-free twin, every third frame:

| | frames | p10 | p50 | p90 | p100 | ≤0.5 hw |
|---|---|---|---|---|---|---|
| bracket→head, graded | 58 | 0.05 | **0.27** | 1.11 | 1.41 | 67% |
| bracket→head, raw | 56 | 0.07 | **0.24** | 0.81 | 1.44 | 63% |
| converge centre→head, graded | 55 | — | **0.88** | 5.38 | 20.5 | 29% |
| converge centre→head, raw | 71 | — | **0.30** | 2.24 | 12.3 | 62% |

Endpoints on an independent keypoint: graded per-frame hit rate p50 0.29, raw **0.55** (p10 0.23). Per panel, raw (p50/p90/max hw): seg 4 box 0.65/1.37/1.44, seg 5 converge 0.36/0.80/12.3, seg 6 box 0.18/0.26/0.59, seg 7 converge 0.15/0.25/0.28, seg 9 trail 0.09/0.11/0.11, seg 10 vector 0.12/0.19/0.21, seg 13 box 0.60/0.87/1.02, seg 14 converge 0.20/0.61/1.07, seg 15 box 0.13/0.30/0.39, seg 17 converge 0.43/3.20/3.34, seg 18 converge 0.54/1.46/2.24.

**What the tails are.** The six worst bracket frames (f252–f285, seg 4; f582, seg 13) are the same picture: the bracket on Vinícius's face and the referee's "head" on his **chest** — a tall close body cut by the frame, where the referee's head estimate slides down (`build/work/vinicius_raw_worst/`). Seg 4 and 13 report ink 0% for the same reason: the person box the referee found does not reach the head. The converge gap between graded and raw is the grade: the doubters look (luma 30, black lifted to nothing) leaves the referee **fewer and wrong faces** on this darker footage, so its nearest head is a teammate in the selfie (seg 17: 15 bodies), or nothing. The mesh itself was checked on the frames — f620/640/655 (seg 14), f780/800/815 (seg 17), f840/860 (seg 18): on Vinícius's face in all eight (`build/work/vini_conv_check.png`). The raw numbers are the ones to read for converge on this edit, and they are reported next to the graded ones rather than instead of them.

Gates, controls first, as printed:

```
POSITIVE CONTROLS
  control freeze : moving clip OK, six held frames FAIL -> fires
  control flash  : +32 measured +31 (OK), +60 measured +59 (FAIL) -> fires
  control cards  : phantom 14th card on doubters_v01_clean.mp4 -> fires
  self-test OK

DELIVERY GATES  output/vinicius_v01.mp4
  1 frames   OK
  2 freeze   OK  (on the grain-free render)
  3 cards    OK  13 scheduled, 13 rendered, 13 runs in the file
  4 flash    OK   13.93s:+28  14.27s:+29  15.93s:+27  16.60s:+30  21.43s:+29
  5 overlay  OK   p50 0.27  worst 20.50 head widths (gate: p50 <= 0.5)

ALL 5 GATES PASS (report-only tools are not counted; see docstring)
```

**Deliverables:** `<PROFILE>/Desktop/flashcut-renders/2026-09-20_vinicius_v01-clean-v1.mp4` (+ `_index.json`, 914 frames, verified), `configs/vinicius.json`, `configs/story_vinicius.json`, `build/carved/vinicius/` (+ `manifest.json`), `build/work/pool_vinicius.json`, `build/work/plan_vinicius*.json`, `build/work/solves_vinicius.json`, `build/work/vini_subj2.png` (the sheet), `build/work/vini_conv_check.png`, `build/work/vini_r1/` (first render's measurements and worst frames), `build/work/vini_r2/`.

## 8. Haaland v1 (option a)

**The library.** 32 compilations, **1,087 shot-clips** (28 cuts failed on the encoder and were skipped; `build/carved/haaland/`). Dortmund is the young era from the folder — with one correction: compilation 32 is filed under Dortmund but is mostly 2022-23 City footage, so every clip of it is hand-labelled (s096, the back of the DORTMUND 9 shirt, is the opener; s015/s016 are the other Dortmund ones) and the folder era cannot put City in the archive slot. The scan (§9) blocked Dortmund 52 whole (a `GOALS 32` counter graphic 90 px inside the window edge) and City 97. 76 s081 is a Joker film clip cut into a mixtape; 80 s000/s055 carry burned-in captions (`WOOOAH`, `WHAT A HEADER!`); all blocked by name.

**The screen:** 1,082 screened, 602 kept; 67 celebrate (11 hand, 56 evidence), 125 dejected, 132 down. **The plan** (Pearson +0.44): DORTMUND 9 shirt → HAALAND 9 shirt → the tunnel → four Dortmund build shots (a penalty run-up, a cup goal, Leipzig, a wide) → six City runs → archive: Dortmund wide → **drop: the run of goals from the 36-goal season compilation** (80 s013 the Southampton volley, 80 s021 one goal in three forward jumps, 80 s038 the scream) → four flex celebrations out. The subject sheet took the overlay off seg 8 (100 s102: the score chose **Foden, #11**), seg 14 (80 s013: **Grealish**), seg 18 as first planned (80 s016: **van Dijk**) and the wide Dortmund shots (unconfirmed at that size); 9 overlays remain.

**The first render failed the card gate**, correctly: `cards NOT rendered: THE PREM WILL EXPOSE HIM`. §9.

| | frames | p10 | p50 | p90 | p100 | ≤0.5 hw |
|---|---|---|---|---|---|---|
| bracket→head, graded | 40 | 0.09 | **0.18** | 0.34 | 0.92 | 95% |
| bracket→head, raw | 40 | — | **0.13** | 0.25 | 0.84 | 95% |
| converge centre→head, graded | 22 | — | **0.10** | 0.57 | 12.7 (seg 20, one frame, ink 4%) | 86% |
| converge centre→head, raw | 23 | — | **0.15** | 1.02 | 1.46 | 87% |

Endpoints: graded p50 0.64 (p10 0.52), raw 0.60. Per panel graded: seg 3 box 0.28/0.39/0.92 (the penalty run-up, 34-px head), seg 7 box 0.36/0.68/0.76, seg 10 converge 0.57/0.72/0.76, seg 11 box 0.11/0.22/0.25, seg 15 box 0.11/0.18/0.20, seg 18 converge 0.08/0.35/0.59, seg 19 converge 0.07/0.09/0.10, seg 20 converge 12.7 in one of two frames (raw: 1.44/1.46 — a 0.2 s flex with the fists at the face; the referee's head is under the hands), seg 21 converge 0.13/0.19/0.21.

```
DELIVERY GATES  output/haaland_v01.mp4
  1 frames   OK
  2 freeze   OK  (on the grain-free render)
  3 cards    OK  13 scheduled, 13 rendered, 13 runs in the file
  4 flash    OK   13.93s:+26  14.27s:+33  15.93s:+27  16.60s:+29  21.43s:+30
  5 overlay  OK   p50 0.17  worst 12.71 head widths (gate: p50 <= 0.5)

ALL 5 GATES PASS (report-only tools are not counted; see docstring)
```

(Same controls as §7, fired in the same run.) One thing to know before watching: the 36-goal compilation carries the Premier League broadcast bug at the top right, which on two of the drop shots sits inside the window (visible at ~23.3 s and ~25 s). It is a broadcaster's mark, not an editor's, and it is not on every shot, so the scan (three shots of four) does not flag it; whether it stays is your call.

**Deliverables:** `<PROFILE>/Desktop/flashcut-renders/2026-09-20_haaland_v01-clean-v1.mp4` (+ `_index.json`, 914 frames, verified), `configs/haaland.json`, `configs/story_haaland.json`, `build/carved/haaland/`, `build/work/pool_haaland.json`, `build/work/plan_haaland*.json`, `build/work/solves_haaland.json`, `build/work/haaland_subj.png`, `build/work/haaland_measure.json`, `build/work/haaland_raw_measure.json`, `build/work/haaland_worst/`.

## 9. Two things the renders forced: a watermark scan, and cards that wrap

**`tools/watermark_scan.py`.** A burned-in handle is the one thing a compilation keeps constant from shot to shot, so the scan takes the mid-frame of up to 16 shots per source (spread across it), computes the Sobel edge magnitude per frame at 1280 px wide, and keeps pixels whose edge is present in **three shots of four** (the 25th percentile across shots — the minimum missed the faint ones, which vanish on a dark background in one shot of sixteen; a per-pixel intensity std, the first version, missed every real handle and fired on grass and pitch lines that lined up between shots of one game). Components under 60×12 px, whole-frame boxes and letterbox lines are dropped; every box is reported in native pixels with whether it falls inside the centre 1080 columns of the cover-cropped frame, and a review sheet crops each one so the verdict is read by a person. **Positive control, run before every scan:** a synthetic `@planted_handle` is stamped into the window of the largest source's frames and must raise the inside-window count, or no verdict is given.

```
POSITIVE CONTROL
  control: planted handle in the window of Vinicius Jr Real Madrid 139.mov -> 1 inside-window boxes before, 2 after -> fires
...
9 of 26 sources carry stable ink inside the window: 130, 132, 137, 138, 139, 140, 159, 177, 188
```

Read on the review sheet (`build/work/wm_vinicius_review.png`): 138 and 188 `@GODZILLAEDITOR`, 177 `nielprod`, 159 the score bug, 130 `NECBY MIX` and 140 `NECBY FOOTBALL` reaching 30 px inside the window edge, 139 the webcam — all real; 132 (pitch lines, an Emirates board) and 137 (the shirt) are the false positives a person discards in a second. It **missed 149's `#Leva…` hashtag**, which is not on three shots in four; 149 is blocked by eye from the first render. On Haaland: 52 (`GOALS 32`) real, 87/89 false, 97 uncertain and blocked.

**Cards that wrap.** The card type is set to the width and stretched to the height, so a long card is a large vertical stretch — ROBOT 7×, PENALTY MERCHANT 22×, COLD NIGHT IN STOKE 23.5×, all delivered and read by the gate. `THE PREM WILL EXPOSE HIM` on one line is **31×**: hairlines. The gate saw under 2% ink and refused the render, which is the gate doing its job. Past **24×** — just above the largest delivered stretch — a card now wraps to two lines at the most even word split, each set to the width and stretched to half the height (`build/work/card_wrap.png`). Two of the approved cards wrap: `THE PREM WILL EXPOSE HIM` and, when Giannis is rendered, `NOBODY KNEW HIS NAME` (27×). No delivered card changes: `configs/doubters_v01.json` through `build_edit.py` was re-rendered after the change and is `cmp`-identical to the delivered v6 (`MIGRATE IDENTICAL`).

**Deliverables:** `tools/watermark_scan.py`, `build/work/wm_vinicius.json`, `build/work/wm_vinicius_review.png`, `build/work/wm_haaland.json`, `build/work/wm_haaland_review.png`, `tools/build_doubters.py` (`card()`), `build/work/card_wrap.png`, `build/work/migrate_v01b.mp4`.

## Deliverables

- `<PROFILE>/Desktop/flashcut-renders/2026-09-20_messi_v01-clean-v2.mp4` — 14.3 MB, 914 frames, 1080×1920, aac (+ `_index.json`)
- `<PROFILE>/Desktop/flashcut-renders/2026-09-20_vinicius_v01-clean-v1.mp4` — 27.0 MB, 914 frames (+ `_index.json`)
- `<PROFILE>/Desktop/flashcut-renders/2026-09-20_haaland_v01-clean-v1.mp4` — 15.8 MB, 914 frames (+ `_index.json`)
- `configs/messi.json`, `configs/story_messi.json`, `configs/vinicius.json`, `configs/story_vinicius.json`, `configs/haaland.json`, `configs/story_haaland.json`, `configs/scripts.json`
- `tools/watermark_scan.py` (new), `tools/celebration.py`, `tools/list_celebrations.py`, `tools/check_scripts.py`, `tools/cut_shots.py`, `tools/delivery_gates.py` (`self_test`), `tools/publish_report.py`, `tools/screen_pool.py`, `tools/story.py`, `tools/build_doubters.py` (`card()` wrap), `tools/solve_cache.py` (v7, `margin`)
- `docs/REPORTING.md`, `docs/subject_truth_2026-09-20.json`
- `build/carved/vinicius/`, `build/carved/haaland/` (+ manifests); `build/work/pool_vinicius.json`, `build/work/pool_haaland.json`; plans, staged plans and solves for both
- `build/work/messi2_measure.json`, `build/work/messi2_raw_measure.json`, `build/work/messi2_worst/`, `build/work/messi2_raw_worst/`
- `build/work/vini_r1/`, `build/work/vini_r2/`, `build/work/vini_subj2.png`, `build/work/vini_conv_check.png`, `build/work/vinicius_worst/`, `build/work/vinicius_raw_worst/`
- `build/work/haaland_subj.png`, `build/work/haaland_measure.json`, `build/work/haaland_raw_measure.json`, `build/work/haaland_worst/`
- `build/work/wm_vinicius.json`, `build/work/wm_vinicius_review.png`, `build/work/wm_haaland.json`, `build/work/wm_haaland_review.png`, `build/work/card_wrap.png`
- `build/work/celebration_eval.json`, `build/work/truth_cache.json`, `build/work/truth_sheets/`

## Assertions at close

- Messi v2, Vinícius v1, Haaland v1: 915 frames pushed, 914 in each file (audio-limited, as every delivery); `verify_delivery --expect-frames 914`: `ALL VERIFIED` on all three; `ALL 5 GATES PASS` on all three, quoted above, with the freeze / flash / cards controls fired first in each run.
- `configs/doubters_v01.json` through `build_edit.py`, after the card change: `cmp`-identical to the delivered v6.
- `tests/test_overlay_transform.py`: 34 passed, 0 failed. `tests/test_branding.py`: 97 checks passed.
- `tools/check_scripts.py`: control fires (2 problems on the planted copy); 65 cards, 65 distinct, CLEAN.
- `tools/watermark_scan.py`: control fires on both libraries (139.mov 1→2 inside-window boxes; Dortmund 52.mov 0→1).
- Doubters v6 and Messi v1 files on the desktop: unchanged.

## What I got wrong

- **`docs/REPORTING.md` still described the gist channel after the commit that said it named gists as not working.** The commit message (6b0e942) claimed the doc change; the doc had only the redaction and control paragraphs. Fixed this round, in §The channel.
- **The -b report quoted the raw 5.44 tail without an explanation.** It was the referee choosing an 18-px spectator; one worst-frame dump on the raw render settled it in a minute and should have been in -b.
- **The first celebration rule I replaced the pose rule with was itself a pose rule** (box aspect for "upright"), and it read 14 of 22 close-ups as lying. Two more iterations before the skeleton-angle rule with a box-aspect fallback only where there are no hips.
- **`screen_pool` did not apply the story blocklist**, only the Ronaldo one in `select_ferrari.py`; 147 Vinícius clips (a reaction video with a webcam over every frame, a mirrored compilation) would have been screened and could have been chosen. Fixed; the first Vinícius screen crashed on the fix (`dict | set`) and was re-run.
- **The first Vinícius render shipped three editors' handles inside the window** — nothing measured them; I found them by looking at twenty frames of the output, after the gates had passed. The scan exists because of this; it would not have existed if I had not looked.
- **The subject sheet is three frames and a mid-clip swap lives between them.** Seg 8's bracket walked onto a Shakhtar defender for the middle of a 0.9 s cut and the sheet showed Vinícius at all three sample points. The harness's worst-frame dump on the raw render caught it; the sheet alone would not have.
- **The first Vinícius opener was the Wembley knee-slide with the score bug** — 159 s001 was labelled "walking alone" off a mid-frame; the clip starts on the celebration. The frame strip of the render showed it.
- **The motion rule labelled Ancelotti on the bench as a `run`** and the planner put him in a 0.16 s late cut; the sheet caught it. The rule has no idea who is in the frame.
- **The first watermark scan (per-pixel std) missed every real handle and flagged grass.** Two more iterations before edges-in-three-of-four; the planted control fired on all three versions, which says the control is necessary but not sufficient — it proves the scan can see a bright synthetic handle, not a faint real one.

## Unsure

- Whether 44 labels are enough to say 80% / 54% with any confidence; the basketball in-game set is 18.
- The raw-look referee scores converge worse than the graded (p90 0.91 vs 0.55) on identical drawn pixels — more crowd keypoints detected on the brighter picture; both numbers are reported, neither is tuned (unchanged from -b).
- The converge referee under the doubters grade on the Vinícius footage: graded 29% within 0.5 hw against raw 62% on identical drawn pixels. Eight frames were checked by eye and the mesh is on Vinícius in all eight, but eight frames is not 55, and the graded number is the one a reader would quote. The referee needs a grade-aware pass (detect on the raw twin, score the graded ink) before a converge number on dark footage can be trusted either way.
- Whether the Premier League bug on two Haaland drop shots is acceptable; it is a broadcaster's mark and it is small, and it is inside the window.
- The Haaland drop is "a run of goals" in the sense of one volley, one goal in three cuts and one scream; the 36-goal season is in the library as 41 usable shots of compilation 80, most of them wide. If option (a) wants the count on screen, that is a card, not footage.
