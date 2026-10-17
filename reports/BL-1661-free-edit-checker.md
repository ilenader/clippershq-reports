# BL-1661: a free edit checker that learns -- built, round 1 done (62 % right on unseen tennis clips); its sure "NOT" is 97 % right, its "EDIT" needs Claude Code ($0)

3 FIXER order `2026-10-17_1013_BUILD-THE-EDIT-CHECKER-INTO-A-FREE` (ALFRED for Dusan, 10:13): a free script looks at
downloaded clips and says edit / not edit with a one-line reason; Claude Code checks the same clips; the script is taught
where it was wrong; repeat on new tennis downloads until it rarely misses; only real edits reach Dusan. Money: **$0**.

## Card

| # | Item | Result |
|---|---|---|
| 1 | **What it is** | `clippershq/edit_checker.py`: EDIT / NOT + a one-line reason per clip, from FREE numbers only -- the AI reviewer's own picture and sound numbers (cuts per second, still share, motion, beat, cuts on the beat, speech), new craft numbers read off the 30-frame sheet (different scenes, black-and-white, blur, vignette, on-screen text, sharpness), the hashtags and the account's earlier results (never the clip's own). No paid call, no model API. |
| 2 | **How it learns** | `round N` -> its verdicts + sheets for Claude Code; `compare N` -> every miss with the numbers that misled it; `learn N` -> the labels are taught (a correction is a new row) and a new model version is fitted; `deliver N` -> only clips Claude Code confirmed as edits. Score book per round. |
| 3 | **Teacher** | Claude Code's checks: 843 clips the Claude lane (Sonnet / Opus sub-agents) already judged EDIT or NOT, plus every round's labels. |
| 4 | **Round 1 (blind)** | 61 tennis-folder downloads, held out of training: **script right 38 of 61 (62 %)**: 12 called EDIT wrongly, 11 edits missed. The misses: subtitled TV dialogue scenes (cuts but no craft) called edits; "quiet" edits (few cuts, grade, lyric text) missed. |
| 5 | **Taught** | Round 1's 61 labels + the craft numbers from the sheets (the lesson from its misses). Now **model v3, 838 clips**. Whole accounts held out: **77 % right** overall (edit precision 69 %, recall 77 %). |
| 6 | **Where it is already useful** | Its SURE answers (accounts held out): p <= 0.10 = **19 % of clips, 96.8 % really NOT**; p <= 0.05 = 11 %, 100 %. Its EDIT calls are only ~80 % right, so an EDIT never goes to Dusan on the script's word: Claude Code checks every one. Each prediction carries a `sure` flag. |
| 7 | **Delivered to Dusan from round 1** | **0 new.** Claude Code confirmed 34 of the 61 as edits, but none is a tennis edit (BL-1659: the tennis tags bring TV / music / other edits) and all 34 already wait in the friend's review queue. |
| 8 | **Stopped** | The full measuring pass (one decode per clip) was stopped by Claude Code for low memory at 528 of 843 clips (PC ~4 GB free); it was not restarted. The rest used the saved sheets, no decode. |

## Honest limits
- Free numbers alone plateau at ~77-84 % against Claude Code's eye; "rarely misses" is NOT reached. What it cannot see:
  craft vs plain re-posts of TV scenes, and edits of out-of-scope subjects (anime, music) that look the same as in-scope ones.
- The daily loop needs new tennis downloads. Downloads are OFF by Dusan's rule (he runs them himself), so the
  checker waits for his next download; nothing downloads by itself.

## Daily round (3 FIXER, when new tennis downloads exist)
`Python311 clippershq/edit_checker.py round N` (sheets + verdicts; one decode per clip at below-normal priority) ->
one Sonnet sub-agent with the round's `CHECK_PROMPT.md` writes `labels.csv` -> 3 FIXER re-checks every disagreement by
eye -> `compare N` -> `learn N` -> `deliver N` (Claude-confirmed in-scope edits only).

## Tests
- `tests/test_edit_checker.py`, 8 tests, synthetic (temp edits home, fake picture numbers, synthetic sheets). They check:
  - a clip's own result never feeds its features, and stored numbers are used without a decode;
  - it learns edits vs talking heads, with a reason, and a black picture is never an edit;
  - sheet numbers: 30 different scenes vs one grey still; an unreadable sheet gives nothing;
  - the round, compare, learn (v2, the taught label wins) and deliver steps work, and a used clip is not picked again.
- **8/8 pass** (run with ResourceWarning as an error). Control: `clippershq/edit_checker.py` does not exist at HEAD,
  so every test fails on the old code.
- `tests/run_all.py` not run: new files only, no existing file changed.
