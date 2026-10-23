# BL-1691 -- 3 FIXER relay host is a setting (bogdan or the 3090)

Order: `3_FIXER/2026-10-23_1923_3-FIXER-RELAY-HOST-SETTING-FOR-THE-3090.md` (ALFRED for Dusan, P0 19:07 "move
everything to the 3090"). $0. Nothing started or stopped: no relay, no window. ALFRED does the switch.

## What changed
- `tools/office/remote_fixer.py`: `CLIPPERSHQ_REMOTE_HOST` picks the farm PC, default `bogdan`.
  `HOSTS = {bogdan: D:/neuraltrack/alfred_remote_bogdan, vast3090: D:/neuraltrack/alfred_remote_vast}` (the same
  offices as neuraltrack `tools/farm/window.py` OFFICES). `TEAM` = `<office>/teams/finder_3_fixer` unless
  `CLIPPERSHQ_REMOTE_TEAM` is set (unchanged). `start_window` passes `--to <HOST>`. An unknown host stops at import.
- The texts that said "on bogdan" now say where it runs ("bogdan" / "the 3090"): new_order_file `by=`, the COUNCIL
  line, the RESUME line, NOW line 1 (working + waiting), the export-scan BLOCKED line, the HQ BLOCKED rewrite.
- `tools/office/REMOTE_3_FIXER_ROLE.md`: one line -- the window may run on bogdan's PC or on the 3090 (ALFRED's rented
  Linux box, user farm, python3 + git), same rules: code-only, no data, no keys.

Default behaviour is unchanged: with no setting, TEAM, `--to bogdan` and every text are byte-identical to before
(the old COUNCIL-text test still passes untouched).

## Proof
- `tests/test_remote_fixer.py` 12/12 OK (3 new: default = bogdan team + `--to bogdan`; `CLIPPERSHQ_REMOTE_HOST=vast3090`
  = vast team folder + `--to vast3090` + "on the 3090"; unknown host refused).
- Base control: the 3 new tests run against the HEAD file fail (2 FAIL, 1 ERROR) -- the vast test fails on TEAM.
- `tests/test_office_tools.py` 35/35 OK.

## For ALFRED (the switch)
1. `D:/neuraltrack/alfred_remote_vast/teams/finder_3_fixer` does not exist yet (19:40: only alfredo_screen_vast).
   The relay restarts only a window that has ENDED (heartbeat 'stopped' or silent); with no heartbeat it never starts
   one (pinned by test_no_heartbeat_yet_is_never_a_second_start). So the FIRST start is ALFRED's:
   `window.py start finder_3_fixer --to vast3090 --role tools/office/REMOTE_3_FIXER_ROLE.md`.
2. Set `CLIPPERSHQ_REMOTE_HOST=vast3090` in the relay's environment, run `remote_fixer.py export` once (fills
   work/repo there), then start the relay (`pythonw tools/office/remote_fixer.py relay`). launcher_start.bat no
   longer starts the relay (BL-1690); if it should come back at logon, that line needs the setting too.
3. 3 FIXER's HQ window must stop running wait_orders when the relay is on (the relay owns the orders).
The bogdan team folder keeps its STOP file and its 18 stale inbox copies; a vast3090 relay does not read them.
