# BL-1636: wrong niche in the basketball send -- found why, 4 real ones added, and every send now looks at each video first

2 APP order `2026-10-13_2340_P0-wrong-niche-in-send` (P0, cap $0.50). 2026-10-13 23:40 – 2026-10-14 01:15.
Money: **$0.0048 of $0.50** (231 model calls: 169 library pass, 60 calibration, 2 probes) (OpenRouter, the vision model; booked to spend.json campaign `send_gates`).

## Card

| # | Item | Result |
|---|---|---|
| 1 | **Added** | **4** eye-checked basketball edits (contact sheets, 4 frames each: basketball, not black, not a repeat) into the **same folder, same link** (files 021–024). Clean + metadata verify + Drive size/hash check: 4/4. Only 3 were asked for, but there were **4** wrong files: **011 is UFC**, not only 001/002/014. He had already deleted 001, 002, 014; once he deletes 011 the folder is exactly 20 basketball. |
| 2 | **Root cause** | A library video's niche was **never read from the video**. `videos.niche` = the **account's** niche, and the account's niche = **the hashtag that found it** ("kobe edit", "shai gilgeous alexander edit"). An account found on a basketball tag that also posts football / UFC edits files every one of them as basketball. A YES on the review page says "good edit", not "this niche". All 4 wrong files came this way (3 from one "kobe edit" account, 1 UFC from an "sga edit" account); 2 via the BL-1631 Drive import, 2 via review YES -- not a migration bug. |
| 3 | **"Same clip twice"** (001/002) | Not one video posted twice: **two different football edits by the same account that open with the same match moment** (same broadcast, ~0.5 s apart, a different crop), then go on to different players. Measured: 0 % of their frames match even at loose settings. |
| 4 | **"All black"** (014) | The library file is **not black**: it decodes start to end, 1.0 s of black in 52.8 s (a fade), normal H.264. What he saw was most likely Drive's player before Drive finished processing the file. It was football anyway. |
| 5 | **The fix: 3 gates in the send** | `clippershq/edits_send_gates.py`, wired into `edits_send.run`. Candidates are taken **in his order** (best first) and only videos that pass all three go into a send. A gated video gets a `send_items` row (`gated`, why); a send that cannot fill its count ends `partial`, never with a wrong video. |
| 5a | NICHE | 4 frames (15/40/65/88 %) in a 2x2 sheet → `qwen/qwen3.7-flash` (BL-1630's judge model): "which subject is this?" **Only YES is sent.** NO → the library row is relabelled to the niche the video shows (or `out_of_scope:<subject>`), its file moved to that folder on F:, logged in `scope_log`. UNSURE / error → skipped, untouched. Answers cached per file (paid once). **Calibrated on 30 eye-checked basketball-library files: 30/30 agree** (all 6 wrong ones caught: 3 football, 1 UFC, 1 film, 1 Spider-Man), $0.0006. |
| 5b | DUPLICATE | One decode of the whole video at 2 frames/s, a 256-bit picture hash per frame. A **repost** = half or more of the shorter video's frames match a video already sent (any send) or already in this send. Measured on 62 basketball files: unrelated pairs share **≤ 4 %**; a re-encoded, shrunk, brightened copy shares **100 %**. Limit, said plainly: two *different* edits of the same moment (like 001/002) are not reposts and are not caught here; the niche gate stopped those two. |
| 5c | BLACK / BROKEN | Same decode: can't decode / no duration / far fewer frames than the length → broken; ≥ 90 % of frames black → black; ≥ 90 % of steps unchanged → frozen. Never sent. |
| 6 | **Tests + guard** | `tests/test_bl1636_send_gates.py` (6): black / frozen / broken / ok clips; a re-encode is a repost, different footage is not; the model's echo format parses; a full send through the **real** gates with a fake model: UNSURE skipped, other-niche skipped **and** relabelled (row + file + log), repost skipped and never shown to the model, black never sent, cached answers reused, no real ledger write; **guard (AST):** `run` calls the gate before it cleans anything, and `GATE` / `ASK` ship as `None`. BL-1631 send tests get a pass-through gate (their clips are all one test pattern). `run_all -k test_bl16*`: **59/59 green, 621 checks.** |
| 7 | **Library pass** | **Stopped part-way (not by me):** Claude Code stopped the background pass when the PC ran critically low on memory, at **175 of 817** files (the internet was also very slow: ~20 s per model call). Done: **basketball 62/62**, **football 117/558**. UFC, tennis, superhero and the rest of football are **not checked yet**, and the pass was not restarted (rule: a pass stopped for memory restarts only when asked). The relabels for everything checked **were applied** (`scratch/bl_send20/relabel_checked.py`, cached answers, no new calls). A send checks every candidate itself anyway, so nothing unchecked can be sent. |

## Library pass: every local file, all 5 niches (counts only)

| niche | checked | right niche | wrong niche → relabelled | black / frozen | broken (no decode) | reposts |
|---|---|---|---|---|---|---|
| basketball | **62 / 62** | 56 | **6**: football 3, UFC 1, superhero 1, film (out of scope) 1 | 0 | 0 | 0 |
| football | 117 / 558 | 107 | **2**: gaming 1, music (both out of scope) | 0 | 9 | not measured |
| ufc | 0 / 45 | – | – | – | – | – |
| tennis | 0 / 7 | – | – | – | – | – |
| superhero | 0 / 145 | – | – | – | – | – |

- **Basketball's 42 "ready" before this round:** 2 fail the niche gate (the film and the Spider-Man edit); 0 black/broken; 0 reposts. The 4 wrong **sent** ones (001, 002, 011, 014) are now football / UFC in the library, still marked sent, so they are never sent again under any niche. Basketball now: 56 files, 20 sent, **36 ready**.
- Football's 9 "broken": no decode in the pass (ffmpeg failed or timed out while the PC was out of memory). They are not relabelled; a send skips them until they decode. Re-check when the PC is quiet.
- Repost counts inside the library are computed at the end of the pass, which did not run; inside a send the duplicate gate is live.
- Money: 231 model calls, **$0.0048** in total (ledger: 3 rows of 50 + reconcile rows for the 81 calls the stopped pass and the calibration had not booked: +91 then -10 calls), ~$0.00002 per video. The full library would be ~$0.02.

## Changed
- `clippershq/edits_send_gates.py` (new), `clippershq/edits_send.py` (gates in `run`), `tests/test_bl1636_send_gates.py` (new), `tests/test_bl1631_library_send.py` (pass-through gate).
- `scratch/bl_send20/add_more.py` (step 1), `scratch/bl_send20/gate_library.py` (the library pass), result `scratch/bl_send20/gate_library_result.json`.
- Commits: e5f3cf87 (code) + this report.

## For the owner
- Delete **basketball_…_011.mp4** (UFC) in the Drive folder → 20 real basketball.
- Nothing else; the next Send checks every video by itself (~$0.00002 per video, a few seconds each).
- Option, not done: allow at most N videos per account in one send (would also spread out same-moment edits like 001/002).
