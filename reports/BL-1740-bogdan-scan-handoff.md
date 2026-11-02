# BL-1740 -- view scout loosened, and the one command for Bogdan's PC

Loosening rule (number picked by 3 FIXER): a video passes the view scout when views >= 10,000 AND likes >= 1 per 10 views (before: 20,000 views floor; the old 2x-normal rule still applies unchanged). Constant `LIKE_PASS_MIN_VIEWS` in `clippershq/edits_signals.py`. Undo: set it to 20000 or revert the patch.

Needs Bogdan's PC (ALFRED runs; I cannot reach it). Exact command from the repo folder, free calls only, capped, headless, no send:

    python clippershq/run.py --funnel tiktok_editors --target 300 --cap 0 --free-only

Check first with `python clippershq/run.py --list` and `--status`. If `tiktok_editors` is not the edit-finder funnel, replace only the name after `--funnel`; the other flags stay. Count line to post by 23:00 (late now): the number of rows added to the run's output file.
Judging of the results stays on the 3090; copy the output file into /srv/finder_gate/ for it.
