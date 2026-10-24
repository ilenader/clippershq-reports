# BL-1696 -- the three "maybe bugs" from the 3090 suite sort

Order: ALFRED 0801 (take the 3 group-(c) items from 3 FIXER's sort of `full_run4.txt`: 7707 passed / 780 failed / 63 errors).
Checked at HQ first: 2 of the 3 were red here too (they are not 3090-only); the third passes alone at HQ and only fails in a whole-suite run.

| item | at HQ | cause | fix |
|---|---|---|---|
| `test_silent_zero_shape` GUARDED boundaries | red, 2 sites | `main._cap_backups` caught `Exception` around a `scandir` and returned 0 (same value as "nothing to prune"); `main.delivered_projection` did `except (ValueError, AttributeError): pass` per attempts.jsonl line (bad lines dropped without a word) | `_cap_backups`: `FileNotFoundError` -> 0, anything else logs a WARNING and returns 0 (the write is still never broken). `delivered_projection`: bad lines are counted and logged with the file and first error. |
| `test_zero_collection` | red | `tests/test_bl1528_paging_and_ledger.py` is script-style (10 module-level tests, no TestCase): `python -m unittest` collected 0 | `load_tests` hook (BL-1282 shape). Its `check()` records instead of raising, so each test is wrapped to raise when it added to FAILURES -- otherwise a red check would collect as a pass. unittest now runs 31 checks. |
| `test_run_status` | green alone | `clippershq/run_status.py` and `tools/run_status.py` share the module name; in a whole-suite pytest run whichever was imported first owned `run_status` -> "no attribute ROOT" | the test loads `tools/run_status.py` by path under its own name. |

Suites after the fix (HQ, run_all): test_zero_collection, test_run_status, test_bl1528_paging_and_ledger, test_bl1460_backup_cap, test_bl1582_tag_yield_and_spend_screen PASS.
`test_silent_zero_shape`: the GUARDED-boundary test now passes; the suite stays red on its RATCHET test -- 98 new silent-zero sites
outside the guarded files since the 2026-08-15 baseline (top: edits_app 6, edits_remove 5, tools/edits_package 5, tools/office/remote_fixer 5,
edits_swipe_server 4, edits_transfer 4, raw_emails 4, raw_pages 4, tools/office/check_state 4). Each needs its own judgement (fix, narrow,
or a baseline line with a measured reason) and most belong to the edits app (2 APP). Not done here.
Money: $0.
