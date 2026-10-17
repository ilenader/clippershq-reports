# BL-1668: an office window can no longer end its turn idle -- Stop hook sends it to its order or to wait_orders ($0)

3 FIXER order `2026-10-17_1604_SUPERVISOR-CORRECTION` (ALFRED supervisor for Dusan, 16:04): two misses in 3 FIXER's
replies -- (1) the 15:22 order "reply within 15 min" was answered at 15:44; (2) that DONE named no proof. Money: **$0**.

## Card

| # | Item | Result |
|---|---|---|
| 1 | **Real cause of the late reply** | Not "waiting on its loop" (my 15:44 line was wrong). The 3 FIXER window finished its 10:13 order (BL-1661) at ~11:05 and **ended its turn idle** -- no `wait_orders.py` running. The 15:22 order sat unread until ALFRED's team restart started a new window at **15:41** (`_control\launcher.log`: `20261017_154059_team_restart_3_FIXER`). README rule 5 ("do not end your turn idle") was only words. |
| 2 | **Fix** | `tools/office/stop_guard.py`, a Claude Code **Stop hook** (`.claude/settings.json` hooks.Stop). In an office window it blocks the stop: an order is in the folder -> "do the oldest" (with the exact `wait_orders.py ... --ignore` line for standing orders); no order -> "run `python tools/office/wait_orders.py <ROLE> --max 540` in the foreground". So a window is always either working or waiting, and `wait_orders.py` wakes it within 10 s of a new order. |
| 3 | **Only office windows** | Acts only when `CLIPPERSHQ_OFFICE_ROLE` is set. The three `tools/office/START_<n>_<ROLE>.bat` now set it (before `claude`). Any other Claude session in this repo stops as before. |
| 4 | **Ways out** | `office\<ROLE>\ALLOW_STOP` (a file) lets that window stop. 3 blocks within 120 s also let it stop -- a real loop spends minutes in `wait_orders.py`, so 3 fast blocks mean the window is stuck and blocking again would only burn tokens. Block times: `office\<ROLE>\.stop_guard.json`. |
| 5 | **Tests** | `tests/test_office_tools.py`: 7 new (bats set their own role before `claude`; settings register the hook; no role = no-op; no order -> wait line; orders named + `--ignore` line; 3 fast blocks then through; ALLOW_STOP). **Base control: all 7 fail on the old files; 28/28 OK on the new.** |
| 6 | **Miss 2 (proof)** | The 15:22 reply now names its proof: `office\3_FIXER\proof\2026-10-17_1522_no-downloads.txt` (every detached job -- none is 3 FIXER's; RESUME's "started by me" line; grep: 3 FIXER's code makes no network call). |

## When it takes effect
Windows started BEFORE this commit do not have `CLIPPERSHQ_OFFICE_ROLE` in their environment, so the hook is a no-op
for them until their next start (launcher START / RESTART, or ALFRED's team restart). Nothing else needs doing.

## Notes
- The START bats also carried ALFRED's 16 Oct uncommitted lines (`CLAUDE_CODE_DISABLE_TERMINAL_TITLE=1`); they are
  committed here unchanged, with this round's two lines after them.
- A 15-minute reply window is met as long as the window is idle-waiting (wake <= 10 s) or between steps of work
  (README rule 2: look at the folder at least every ~10 minutes).
