# BL-1675: the office launcher leaves the Windows job it was started in -- it died silently 4x on 18-19 Oct ($0)

3 FIXER order `2026-10-19_0508_WATCHERS-LEAVE-AGENT-JOB` (P2, ALFRED auto-builder; source COUNCIL 19 Oct 05:00 and the
SENTINEL incidents 18 Oct 22:53 / 19 Oct 01:39). A program started from a Claude window's shell lives in that window's
Windows job and dies when the window is cleaned up. Money: **$0**. Code only; nothing restarted.

## Card

| # | Item | Result |
|---|---|---|
| 1 | **3 FIXER's 24/7 programs** | One: the office launcher `tools/office/launcher.py` (hidden pythonw, pid in `_control\launcher.pid`). The AI-decision monitor is not 24/7 (one foreground round per loop). The review app, its watchdog and the farm jobs belong to 2 APP. |
| 2 | **At risk?** | Yes. Live launcher pid 21684 (and its venv stub 40440): `crashproof.in_job` = **True**. `launcher.log` shows `launcher started` at 18 Oct 20:08, 20:48, 23:43 and 19 Oct 00:36 with no stop line between: four silent deaths, each one an account switch or terminal restart. |
| 3 | **Fix** | `tools/office/job_hop.py` (new, copied from MILOJE/tools/crashproof.py, not imported): `in_job`, `popen_free` (breakaway -> WMI `Win32_Process.Create` -> plain Popen) and `leave_job`. `launcher.loop()`: once it holds the lock, a launcher inside a job starts `launcher.py --hopped` outside it, closes the lock and exits. The `--hopped` copy waits up to 15 s for the lock and never hops again (a WMI copy does not inherit our environment, so an argument is the loop guard; `CLIPPERSHQ_JOB_HOP` still covers the plain-Popen fallback). A second launcher refused by the lock never hops. |
| 4 | **Tests** | `tests/test_office_tools.py` **33/33 OK** (4 new): a real child put into a job made by the test (no breakaway allowed, like an agent's job) hops out through WMI; the copy has `in_job` False and still has LOCALAPPDATA; the hop env var is consumed; `loop()` hops only once it holds the lock, then frees it and leaves no pid file; a refused copy or a `--hopped` copy never hops. |
| 5 | **Before / after** | Before: in_job True (pid 21684). After: **still True for the running copy**, because the order says not to restart anything. The fix takes effect the next time the launcher starts: a start from a Claude shell then leaves the job at once, and a start from the Startup folder at logon is in no job. The office windows the launcher starts (`cmd /c start`) inherit its job, so they leave it too. |

## Files
`tools/office/job_hop.py`, `tools/office/launcher.py`, `tests/test_office_tools.py`.
