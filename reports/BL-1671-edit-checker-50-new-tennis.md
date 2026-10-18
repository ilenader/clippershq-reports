# BL-1671: edit checker on brand-new tennis clips -- 46 % then 55 % (NOT SURE counted wrong); the Claude teacher itself is only ~85 % consistent, so 99.5 % needs Dusan as the judge ($0)

2 APP orders `2026-10-18_1035` (Dusan: don't accept 70 %, download 50 more tennis, new rounds) and `2026-10-18_1039`
(change: keep the current checker; in parallel find a better tool or improve it until 99.5 % on never-seen videos;
honest held-out test, no peeking, no dropping hard cases; free first; one-line score after each round). Money: **$0**
(free downloads with his downloader; AI reviewer day cap set to $0 during the run, restored to $1 after).

## Card

| # | Item | Result |
|---|---|---|
| 1 | **Never-seen clips** | 125 new tennis-tag videos downloaded free (his downloader, from the 1,183 queued; 3 failed, ~24 out of scope stay queued). Each round's clips were judged by the newest model BEFORE any label existed; the answers were frozen (sha256 in the log). |
| 2 | **Round 1** (65 clips, model v5) | **30 of 65 right = 46 %** (NOT SURE = wrong; a clip the two blind Claude eyes split on = wrong). Always answering EDIT / NOT would give 66 %. |
| 3 | **Improve** | Taught round 1's 57 clips where both eyes agree -> model v7 (895 clips, 84.4 % with whole accounts held out). |
| 4 | **Round 2** (60 clips, model v7) | **33 of 60 right = 55 %** (same strict rule). Always answering EDIT / NOT: 70 %. |
| 5 | **Free tool tried: audio** | Local AudioSet model (AST) on 670 clips' sound (music vs dialogue): accounts held out 85.2 % -> 85.2 % (key classes), 83.6 % (all 527); hard clips +4 of 172 = noise. **Not adopted.** |
| 6 | **The teacher** | Two blind Claude eyes (Sonnet, Opus) on the same new clips agree **88 %** (round 1) and **83 %** (round 2, with a written borderline rule). With **4x bigger pictures** (12 frames of 360 px): **87 %**. The same model on small vs big pictures of the same clip: 83-90 %. All four eyes agree on only **73 %** of round 2's clips. |
| 7 | **Why they split** | Round 1: definition (subtitled TV-drama reposts, memes of clips, creator vlogs, lightly stylised highlights). Round 2: what the frames show (one scene or several? a montage at the end? plain gameplay or graded?) -- even "sure" eyes split. |

## What it means
- The checker is graded against Claude's eye, and Claude's eye is only ~85 % consistent on these clips. So **99.5 % cannot
  be measured, let alone reached**, with Claude as the teacher -- no tool fixes that; a better judge does.
- The only judge that can make the truth consistent is **Dusan** (or the friend): his call on the ~15 of every 60 clips
  where the eyes split, plus 4 yes/no rules for the borderline kinds (subtitled TV-scene repost / broadcast highlight with
  one effect / meme of clips under text / a creator's own fast-cut vlog: EDIT or NOT?).
- The strict score also punishes NOT SURE: the checker says NOT SURE on ~40 % of new clips. Forced to answer, it is
  66-70 % right. Under Dusan's rule (NOT SURE = wrong) it should always answer; NOT SURE stays useful only as a "send to
  Claude Code" flag in the app.

## Files
`scratch/bl1671/`: new_round.py (blind round on clips downloaded for this order), score_eyes.py (HEADLINE = right / all
clips, NOT SURE and eye-split = wrong), teach.py (agreed labels only), audio_tags.py + audio_dev.py (AST test), hires.py
(12-frame big pictures), TASK_rule.md (the default borderline rule), PROGRESS.md (log). Data: `<edits home>\edit_checker\`
rounds\002, rounds\003 (predictions, eyes, eyes_hires), audio\audio.npz, labels.jsonl +107 rows, models v6 = v7.
No handle, caption or path printed.
