# BL-1634: housekeeping -- FACTS re-stamp, no double windows, 7 old reports published, claims registry clean, run_all --help

$0 vendor spend. No paid call. 3 FIXER order `2026-10-12_2120_HOUSEKEEPING`, 2026-10-12 21:20–21:55.

## Card

| # | Item | Result |
|---|---|---|
| 1 | **FACTS.md re-stamp** | Done **before** the guard refused anything. The drift was **$6.78, 91.6% of the $7.40 limit**; it is now **0.0%** on every column. Lifetime **$147.470596** from one live read (46,514 rows). The guard is OK, 35 facts checked. Commit `d0c34f23`. |
| 2 | **No second window** | Each START bat first asks `launcher.py ALREADY <role>`. If **another** window of that role is open, the bat says so and closes; its own window does not count. Live proof (copies of the bats that echo instead of starting claude): 1 LEADS and 2 APP were **refused**; 3 FIXER **would start**, because the only 3 FIXER window is this one. Commit `ea1eb265`. |
| 2b | **Launcher bug found on the way** | From a normal cmd console, PowerShell turned a curly quote in **any** process's command line into a plain `"`. That broke the JSON, so STATUS, STOP and ALREADY all crashed. Reproduced (chcp 852), fixed by reading as UTF-8, and re-proved from chcp 852 and 437. The launcher was restarted by its own PID on the fix; round trip **2.3 s**. |
| 3 | **Old reports** | **Published:** BL-1610, BL-1612, BL-1613, BL-1619 (both parts: 70 and 170 editors) and BL-1620. Every scan passed, and each URL returned **HTTP 200** with the same bytes. **BL-1618** had no report. It is now written from its commit, its claims manifest (verified at HEAD) and its scratch files only, and published. BL-1613's report was untracked and is now committed. |
| 4 | **Claims registry** | **14 claims released. 1 is live: this round.** 4 cleared normally (BL-1377, 1553, 1556, 1559). 8 were refused over leftover untracked scratch files (BL-1554, 1555, 1557, 1558, 1560, 1561, 1562, 1597) and released **deliberately with `--force`** (why below). 2 malformed files repaired (syntax only) and released: BL-1583 (a missing comma) and BL-1612 (unescaped `\w` in a path). 0 files fail to parse. |
| 5 | **run_all.py --help** | `-h` and `--help` print the usage and **run nothing** (exit 0, about 1 s). An unknown argument also runs nothing (exit 2), so a typo can no longer start the 21-minute suite. Commit `e8a05f14`. |

## Item 1: how

`scratch/bl1634/restamp_facts.py` is the `scratch/bl1600` script with one change: the note now names the round that stamped it (`--round`). The old script always wrote "BL-1600", so two notes were mislabelled:
- BL-1617's stamp (10-09) is now named BL-1617.
- BL-1625's duplicate stock note is removed. BL-1625's own correct note stays.

The table and the machine block both come from one read of the rows, never from the guard's printout. FACTS.md went in its own commit.

## Item 2: the guard

`launcher.py ALREADY <role>` exits **0** when a window of that role runs that is **not one of the caller's ancestors**. The START bat's own cmd.exe is a window of its role, and the python it calls sits below it through the venv redirector. It exits **1** when there is none and **2** on a bad role. On any error the bat goes on and starts the window (fail-open): a broken check must not stop the owner from working.

The bats call `%SystemRoot%\System32\timeout.exe`. Under a Git-bash PATH a bare `timeout` is the coreutils one, which rejects `/t`.

`tests/test_office_tools.py`: 17 tests green (3 new for ALREADY). The checks: its own window does not count, another window does, and every bat runs the guard with its own role before `claude`, with no control characters in the file.

## Item 4: why `--force` for 8, and what stays on disk

All 14 rounds are 3–7 weeks old. No process references any of them, none had scratch touched since 10-11, and every one except BL-1377 has a **published report** (BL-1377's last commit was 08-28). `claim.py end` refuses while a round's own paths hold uncommitted files. Here those are **leftover untracked scratch**: commit-message drafts, probe scripts, raw walk rows, and screenshots named after accounts.

These must not be committed:
- raw rows and account-named images do not belong in history;
- a commit-message draft is not work.

So the release was made deliberately and the files were **left exactly where they are**:

| round | untracked files left in its scratch folder |
|---|---:|
| BL-1554 | 10 |
| BL-1555 | 3 |
| BL-1557 | 38 |
| BL-1558 | 1 |
| BL-1560 | 2 |
| BL-1561 | 1 |
| BL-1562 | 39 |
| BL-1597 | 18 |
| BL-1583 | 1 |
| BL-1612 | 33 |

BL-1583 and BL-1612 also declared live shared files (`spend.json`, `config.json`, `clippershq/*`, `tests/*`). Every round touches those, so a normal `end` could never clear. Their torn originals are kept in `scratch/bl1634/*.json.torn`. The repair (`scratch/bl1634/repair_claim_json.py`) changed +1 and +2 characters and kept every key.

**Not touched:** BL-1563 to BL-1582, BL-1587 and BL-1596. They are already `"status": "CLOSED"`, which every reader skips (BL-1592).

## Tests

- `tests/test_office_tools.py` 17/17 green.
- `tests/test_run_all_help.py` 4/4 green.
- Through `run_all.py -k`: 6 suites, 5 green. 1 red, `test_zero_collection.py`, and it is **not this round's**: it flags `tests/test_bl1528_paging_and_ledger.py` (10 hidden tests). Neither file has changed since 09-07 / 08-15.

## Note

BL-1620's report names the friend link's tailnet host. That host was already public in BL-1629's report, and it is reachable only inside the tailnet. It was published as is, because the scanner decides and it passed.
