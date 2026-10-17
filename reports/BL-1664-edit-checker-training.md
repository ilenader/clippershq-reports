# BL-1664: edit-checker training -- 3 blind rounds over 202 hard clips stay at ~70 %; 99.5 % is not reachable. The checker now answers EDIT / NOT only when sure (sealed 50: 29 of 30 sure answers right) and says NOT SURE for the rest ($0)

2 APP order `2026-10-17_1334_EDIT-CHECKER-TRAINING-TAKE-200-TENNIS-CL` (ALFRED for Dusan, 13:34): 200 tennis clips in
4 batches of 50, the script judges each batch blind, Claude Code checks the same clips, every miss explained and the
script improved; then whole rounds again as if it never saw them; repeat until 99.5 %; the real score is 50 brand-new
clips; every past mistake kept and rerun after every fix. Money: **$0** (local CLIP model, Claude Code sub-agents).

## Card

| # | Item | Result |
|---|---|---|
| 1 | **Data** | No never-seen tennis clips were on disk (all 108 tennis downloads already labelled) and downloads are OFF by Dusan's rule. So the 838 clips the Claude lane already judged were split once, by whole account: **4 batches 50 / 50 / 52 / 50** (the tennis-folder clips + the hardest fan-edit clips; ~50 % of them the lane was NOT sure of), a **sealed 50** (never opened, never used to choose anything) and a base of 586. |
| 2 | **New numbers** | `clippershq/edit_checker_look.py`: a free local CLIP model looks at the 30 frames of each clip's saved sheet (no video decode, nothing downloaded). Whole accounts held out: free numbers alone **75.7 %**, free + look **85.3 %**. |
| 3 | **Round 1** (each batch judged by a model that never trained on it, taught before the next batch) | b1 41/50, b2 38/50, b3 28/52, b4 37/50 = **145 of 202 (71.8 %)** |
| 4 | **Round 2** (leave-batch-out, "as if it never saw them") | 40 / 38 / 26 / 37 = **141 of 202 (69.8 %)** |
| 5 | **Round 3** (with fix 3, scene coherence) | 41 / 38 / 28 / 35 = **142 of 202 (70.3 %)** -> two rounds in a row gained < 1 point = the planned stop line (b). |
| 6 | **Fixes tried** (chosen only on held-out accounts of base + judged batches; the sealed 50 never used) | scene-variety numbers, compressed look (PCA 32), structure weighted up, stacking, trees / SVM / blends, look x scene interactions, scene coherence. **None beat noise**: what helped the hard clips cost the easy ones by the same amount. Kept: logistic regression, C 0.01, free + look numbers. |
| 7 | **Why it misses** (Opus eye on the misses, WHY only, never a relabel) | Batch 3 (worst): 8 of 19 false EDITs are ONE TV-drama / sitcom scene re-posted with subtitles -- 30 frames over 60 s land on a new camera angle each time, so it reads as many shots. Missed edits: lyric edits from animated films, a tennis clip with colour flashes, fan montages. Batch 4: Turkish / Portuguese drama re-cuts with captions that nobody is sure of. |
| 8 | **The label is the ceiling** | A blind Opus third look at ALL 115 clips the lane was not sure of (sealed never opened): sure on 32 (10 differ -> 10 corrections, new rows), **unsure on 83**. Of the 202 hard clips only 125 have a label anybody is sure of. 99.5 % against a label that is a coin flip cannot be measured. |
| 9 | **Mistake book** | 199 rows: every miss of every batch and round, rerun in every dev measurement after every fix. No fix moved more than 4 of the first 9 back to right without breaking others. |
| 10 | **Sure answers** (whole accounts held out, sealed excluded, 705 clips with a sure label) | band p <= 0.10 / >= 0.90 answers **54 %, right 97.9 %**; 0.05 / 0.95 answers 37 %, right 98.5 %. On the 202 hard clips: 26 % answered, 90.6 % right (EDIT answers 26 / 27). |
| 11 | **Sealed 50** (scored ONCE, 21:47, by a model that never saw them) | **43 of 50 right (86 %)**; sure answers **29 of 30 right (96.7 %)** on 60 % of the clips; 20 NOT SURE. Provisional: the sealed clips are older, easier clips (1 of 50 lane-not-sure vs ~50 % in the batches). |
| 12 | **In the tool** | `edit_checker.answer()` -> **EDIT / NOT / NOT SURE** + a reason; the round's `predictions.csv` gets an `answer` column; NOT SURE goes to Claude Code, never to Dusan. Model **v5** (838 clips, look numbers). 13 checks green (`tests/test_edit_checker.py`) + guard suite green. |

## Honest limits
- **99.5 % is NOT reached** and is not in sight with free numbers: three rounds sit at 70-72 % on the hard clips and
  more in-domain clips did not help (round 2 lost 2 points). Even its sure answers are ~98 %, not 99.5 %.
- The **real score** (50 brand-new clips) still needs new downloads. Downloads stay OFF until Dusan says so; 1,183
  tennis videos wait in the queue. The sealed 50 is a provisional stand-in.
- The rounds re-used labelled clips, so round 2 / 3 "as if it never saw them" means: the judging model was refit
  without that batch (no ids, names, hashes or saved answers looked up). Only the sealed 50 is truly unseen.

## What Dusan gets from it
The checker can already take the clear cases off Claude Code's desk: about half of all clips get a sure answer that is
~98 % right; every EDIT still goes through Claude Code before anything reaches Dusan (LESSONS 31). To get the real
score: **Dusan says "download 50 tennis"** -> `edit_checker.py round N` on them -> Claude Code checks -> compare.

## Files
`clippershq/edit_checker.py` (look numbers, `answer()`, NOT SURE band, `look` command), `clippershq/edit_checker_look.py`
(new), `tests/test_edit_checker.py` (+5 checks), `scratch/bl1664/` (rounds.py split / batch / dev / book / unsure /
adopt / sealed, bands.py, probe.py, PROGRESS.md log). Data in `<edits home>\edit_checker\` (bl1664\scores.jsonl,
book.jsonl, eye3.jsonl, corrections.jsonl; labels.jsonl +10 rows, models v4 / v5). No handle, caption or path printed.
