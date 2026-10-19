# BL-1676: the office launcher counts a window started by MILOJE's resume bat; lookalike bat paths no longer match ($0)

3 FIXER order `2026-10-19_0553_COUNT-MILOJE-RESUME-BAT` (P2, ALFRED auto-builder; source: 3 FIXER's COUNCIL post 05:44).
After an account switch or a terminal restart, ALFRED reopens Finder windows through
`MILOJE\state\resume\finder\START_<n>_<ROLE>.bat`. The launcher counted a window only by the full path of
`tools\office\START_<n>_<ROLE>.bat`, so this 3 FIXER window (cmd 15992) was invisible: `launcher_status` said 3_FIXER = [],
STOP 3_FIXER would find nothing, and START 3_FIXER would open a second window. Money: **$0**. Code only; nothing restarted.

## Card

| # | Item | Result |
|---|---|---|
| 1 | **Fix** | `tools/office/launcher.py`: `windows()` also matches `MILOJE_RESUME` = `<Desktop>\MILOJE\state\resume\finder` (taken from the repo's parent folder, the same way MILOJE's finder_sleep finds the repo), with the same bat names and the same `cmd /c|/k "<full path>"` rule. STOP, RESTART, START (already-running check) and ALREADY all go through `windows()`, so all of them now see the window. |
| 2 | **Tightened** | `_runs_bat` used `startswith`, so `...\START_3_FIXER.bat.txt` (or `START_3_FIXER.bat2...`) counted as the bat. Now the path must end there: end of line, a quote or a space. |
| 3 | **Tests** | `tests/test_office_tools.py` **34/34 OK** (1 new): the resume bat counts for its role (quoted and unquoted); the same name in another folder, `START_3_FIXER.bat.txt`, the passing `cmd /c start "" <bat>` and a `.bat2` lookalike do not; STOP 3_FIXER kills only the resume-bat window; ALREADY sees it. |
| 4 | **Before / after** | Before (`launcher_status.json` 05:55:59, launcher 52320 started 05:45 with the old code): 3_FIXER = []. New code (`python tools/office/launcher.py STATUS`, one print, writes nothing) at 05:54:38: **3_FIXER = [15992]**, 1_LEADS [52028], 2_APP [42344]. The running launcher keeps the old code until its next start (not restarted, per the order); the status file then shows 3_FIXER True. |

## Files
`tools/office/launcher.py`, `tests/test_office_tools.py`.
