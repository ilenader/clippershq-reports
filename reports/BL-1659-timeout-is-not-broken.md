# BL-1659: the AI reviewer rejected 9 good videos as "broken" because the PC was too busy to read them in 60 s; a timeout now leaves the video undecided and it is tried again later ($0)

Order `2_APP/2026-10-16_2125` (3 FIXER, standing check of AI decisions): 9 videos were auto-REJECTED as "broken" on
16 Oct. All 9 took 60.0-64.8 s, which is the probe timeout. Re-probed, all 9 read fine (8.9-271.6 s long). 2 of them are real
edits (3 FIXER's eye-check).

## Card

| # | Item | Result |
|---|---|---|
| 1 | **Cause** | `probe()` caught every error, the 60 s `ffprobe` timeout too, and returned "no duration". `analyze()` read "no duration" as `problem = "broken"`, and `route()` turns broken into a sure **NO**. With *AI decides* ON the NO was applied (video -> `_rejected`). A busy PC looked the same as a broken file. |
| 2 | **When** | All 9 between 20:12 and 20:35. 2 APP had just set the AI reviewer's day cap back from $0 to $1 (end of BL-1654), so the reviewer worked through the review backlog (96 videos, $0.034) while the PC was still loaded. Only these 9 were "broken". The other 87 were normal. |
| 3 | **Fix** (`clippershq/edits_ai_review.py`) | `_probe()` returns a 4th value, *timed out*. A probe timeout, or a decode that does not end (then our own ffmpeg child is killed by its handle), is `problem = "timeout"`. `route()` maps it to **HUMAN, why "timeout"**: no verdict, no model is asked. `todo()` tries `timeout` again after `RETRY_S` (1 h), like `model_missing` (`RETRY_WHY`). Only a file ffprobe really cannot read is still broken. `probe()` keeps its old 3-value answer for its callers. |
| 4 | **Tests** | `tests/test_bl1637_ai_review.py` +3: a fake probe that times out -> `timeout`, not broken, route HUMAN; a file that is not a video -> still broken -> NO; with *AI decides* ON a timeout moves nothing (all 5 stay in review, 0 model calls) and is back in `todo()` after `RETRY_S`. File 22/22 OK; the other AI-reviewer files (1639, 1641, 1642, 1647) 26/26 OK. |
| 5 | **Live** | The app was restarted through its own `restart_app` job (old server PID ended by the app itself; new server answers 8793 + 8794, friend link through Tailscale ON). |
| 6 | **The 2 real edits** | Re-decided **YES, superhero** as NEW decisions (`correct()`: BACK, wait for the undo, a new op id). Checked: both left `_rejected`, both are in the approved library with their file. |
| 7 | **The other 7** | BACK to review (checked: all 7 in REVIEW). Their AI row now says what the fixed code writes (HUMAN, `timeout`), so the AI reviewer looks at them again in an hour. 6 of them already had two Claude looks (Sonnet + Opus: unsure). The 7th goes through the Claude lane, with its pictures made on a Flashcut farm PC. The old 9 rows are kept in `scratch/bl1659/before.jsonl` (decision history stays in the app's review log). |

## Rule
A timeout is a fact about the PC, not about the file. Any check with a timeout must report "could not look" as its own
answer and retry it, never fold it into a verdict.
