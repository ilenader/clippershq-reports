# BL-1673: review app console leak -- every child of the review server now starts with CREATE_NO_WINDOW; trap test 81 ffmpeg/ffprobe console hosts, 0 left alive ($0)

2 APP order `2026-10-18_1801_CONSOLE-LEAK-SWIPE` (P1, ALFRED for Dusan). ALFRED's 17:55 trap found 14 empty console
windows in 4 minutes whose parent was ffmpeg.exe / ffprobe.exe on `review/tennis/*.mp4` and whose grandparent was
`pythonw.exe edits_swipe_server.py --port 8793`. Money: **$0**.

## Card

| # | Item | Result |
|---|---|---|
| 1 | **Cause** | The review server runs under pythonw.exe (no console). A console program it starts with no creationflags (ffmpeg, ffprobe from edits_ai_review, clip_media, clip_cuts, clip_motion, clip_pipeline, add_song ...) gets a NEW console of its own, and on this PC those windows stayed behind empty. |
| 2 | **Fix** | `clippershq/no_console.py` (new): `install()` wraps `subprocess.Popen.__init__` once; a call that sets no creationflags gets `CREATE_NO_WINDOW` (0x08000000); a caller's own flags (keyword or the 14th positional) are kept exactly. Off Windows it does nothing. |
| 3 | **Wired** | `clippershq/edits_swipe_server.py` lines 49-50: `import no_console` + `no_console.install()` -- the first local import, before any module that runs ffmpeg. 8794 (share listener) is the same process, so it is covered too. |
| 4 | **Other app processes** | Already clean: run_detached jobs and the watchdog pass CREATE_NO_WINDOW on every call; the server was the only gap. |
| 5 | **Live** | The server running now (8793 + 8794, started 18:08:39) loaded the fixed file (saved 18:02:31). |
| 6 | **Tests** | `tests/test_no_console.py` 5/5 OK: default added; own flags kept (keyword + positional); install twice wraps once; a real pythonw parent's child has no console window (GetConsoleWindow = 0); the server installs it before every other local import (AST). The "control" real child was removed: without the fix it opens a real window that can stay behind. |
| 7 | **Pass test** | `MILOJE/tools/console_trap.py 180` (18:34:38-18:37:40) while `scratch/bl1673/harness.py fix 50` ran the server's own ffmpeg/ffprobe code (edits_ai_review.free_signals) on 50 review tennis clips from a pythonw parent (50/50 ok, 156 s): **81 console hosts with ffmpeg/ffprobe ancestry, all hidden conhost.exe, 0 still alive at 18:38:36**. `console_orphans.py`: 787 orphans (18:27) -> 789 (18:38) on the whole PC while ~470 hosts were made by all teams -- none of the survivors are ours. |

## Notes
- CREATE_NO_WINDOW still gives each console child a hidden conhost.exe; it closes with the child. The leak is a host that
  outlives its program, so the pass test is "alive afterwards", not "zero hosts".
- A first trap run (18:28:45-18:31:45) started 80 s late under load and missed the harness (18:27:25-18:28:28); it is not
  counted. Its 0 ffmpeg lines only cover the live server.
- The 787 existing orphan windows were not touched (not ours to close; `console_orphans.py --close` needs Dusan's yes).

## Files
`clippershq/no_console.py`, `clippershq/edits_swipe_server.py` (lines 49-50), `tests/test_no_console.py`, `scratch/bl1673/harness.py`.
