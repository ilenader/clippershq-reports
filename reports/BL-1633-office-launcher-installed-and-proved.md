# BL-1633: the office launcher is installed, fixed and proved on his PC

$0 vendor spend. No paid call. Measured 2026-10-12, 20:40–20:55. 3 FIXER order `2026-10-12_1820_INSTALL-office-launcher`.

## Card

| | |
|---|---|
| **Launcher** | **Running** (hidden, one copy). It refreshes `launcher_status.json` about every **22 s**. It sees all 3 windows: 1_LEADS, 2_APP and 3_FIXER are **up**. |
| **Round trip** | `STATUS` dropped into `_control\launch_inbox\`. The answer appeared in `launch_done\` in **4.1 s, 4.4 s and 4.6 s** (3 tries). Before the fix it took 9.3 s. **No START, STOP or RESTART was sent.** |
| **Starts at logon** | Startup folder: `ClippersHQ Office launcher.lnk` → `tools\office\launcher_start.bat` (minimised). Running it while a launcher is up starts a second copy, which **exits by itself**. Proved twice: still one launcher, same PID. |
| **Start Menu** | New folder **ClippersHQ Office** (next to **ClippersHQ**). It holds **START 1 LEADS**, **START 2 APP** and **START 3 FIXER**. Nothing was put on the Desktop. |
| **Tests** | `tests/test_office_tools.py`: **14 of 14 green** in 12 s. They use fake homes and a fake process list only. Nothing is started or killed. |
| **check_state.py** | Live run: **0.96 s**. On a fake home it prints every section and **writes nothing**. |
| **Not touched** | The other project's `CLIPPERS HQ OFFICE.bat` (Desktop) and `Clippers HQ office.bat` (Startup). |

## What was wrong in launcher.py, and the fix

1. **A window was found by the bat's NAME anywhere in a cmd.exe command line.** So these counted as a window: another project's `START_3_FIXER.bat`; the short-lived `cmd /c start "" <bat>` the launcher itself runs, which made START report "started" too early; and a `cmd /c type <bat>`. A STOP would have killed them too.
   **Fix:** a window is now a cmd.exe that **runs** this folder's bat by its **full path** (`cmd /c|/k "<full path>"`). That covers a double-click (`/c ""path" "`), a `start` (`/K "path"`, which is what his PC shows) and a Start Menu shortcut.
2. **One launcher at a time used a pid file, checked with `tasklist`.** A reused PID that belongs to any python process (a paid run, say) would have stopped the launcher from ever starting.
   **Fix:** an exclusive lock on `_control\launcher.lock`, held while the process lives. The OS frees it when the process dies, so a stale lock cannot happen.
3. **`launcher.py STATUS` from a terminal overwrote `launcher_status.json`.** It put in its own short-lived PID as `launcher_pid`.
   **Fix:** STATUS writes nothing. The file belongs to the running loop, and `launcher_pid` is read from `launcher.pid`.
4. **One bad pass ended the loop for good.** An OSError on the inbox, for example, killed it, and nothing restarted it until the next logon.
   **Fix:** each pass is wrapped and logged. A file younger than 1 s is skipped while it may still be half-written. A Notepad BOM is read. Folders are ignored.
5. **The poll was every 5 s,** so the round trip took 9.3 s against a 10 s target. **Fix:** every 2 s, so it now takes about 4.5 s. The status file still refreshes every ~20 s.

**Kept as it was, and checked:** STOP ends the window's cmd.exe and its **cmd / claude / node / conhost** descendants, **by PID**, children first. The walk **stops at anything else**, so python, pythonw, ffmpeg and bash survive, and so does everything below them (pinned by a test). `taskkill /PID <n> /F` only. Never `/IM`, never by name. The `cmd /c start "" <bat>` call works with the space in the repo path: the path is quoted by `subprocess`, and the earlier START 2_APP and START 1_LEADS succeeded with it.

## Live proof (his PC)

- The old launcher (PID from `launcher.pid`) was stopped **by that PID** and restarted on the fixed code via `launcher_start.bat`. Its venv redirector exited with it. Nothing else was stopped.
- `python tools\office\launcher.py STATUS` → `{"windows": {"1_LEADS": true, "2_APP": true, "3_FIXER": true}, ...}`. The 3_FIXER PID is this window's own cmd.exe.
- Status file times, sampled every 12 s: `20:48:29 20:48:29 20:48:51 20:48:51`.

## Open, for the prompter

- A Start Menu or Desktop START shortcut opens a **second** window if that role is already running, because the bats have no guard. The launcher's `START <role>` does refuse ("already running"), so use the launcher when unsure.
- No office window was started, stopped or restarted in this round. Only the launcher itself was restarted. The first real START or RESTART stays with the prompter, as ordered.
