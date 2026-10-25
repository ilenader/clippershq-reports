# BL-1721 -- the app's silent-zero sites: 15 fixed, 52 baselined with a reason

Order: 2 APP 2026-10-25_2014 (from 3 FIXER): `tests/test_silent_zero_shape.py` fails on new silent-zero sites in
`edits_*` and `tools/edits*.py`. Fix each one or add a BASELINE line with a measured reason. $0.

## What the scan found
81 new `file:func` sites over the frozen baseline. 67 are app code (`clippershq/edits_*`, `tools/edits*.py`,
`tools/clippershq_open.py`), owned by 2 APP. 14 are `tools/office/*` (remote_fixer 6, check_state 4, stop_guard 3,
job_hop 1, launcher 1); those are 3 FIXER's files and are handed back, untouched.

## Fixed (15): a failure there now raises or is logged, not read as "nothing there"
Money:
- `tools/edits.py:campaign_spent`: an unreadable spend.json returned $0.00 booked, so the session cap had the full
  amount left. Now: missing = $0; unreadable = RuntimeError.
- `edits_db.settings` (config.json + edits_overrides.json): a torn or locked file fell back to the inline caps
  (cap_run $3, cap_day $5), even when he had set lower ones. Now: missing = defaults; unreadable = RuntimeError.

Read, then written back (the `load_spend` shape, where `{}` gets saved over the real file):
- `edits_db.set_override`: a torn overrides file + one Settings click would have saved over every other setting.
- `edits_share._read_json`: friends list, link tokens and the friends' day cap ($) are all read and written back
  through it.
- `edits_jobs.read`, `edits_transfer.read_state`, `edits_ai_learn.load_policy` (the learner's history and its
  "never again" list), `tools/edits_package._package_state` (now prints instead).

Gates:
- `edits_app.run_busy`: a run.lock that exists but cannot be read now counts as BUSY. Before, it counted as "no run",
  so a second paid run could start.
- `tools/edits_package._imports_of`: an unparseable module returned no imports, so the portable package could ship
  with modules missing. `make_data_me` shipped the default settings instead of his when his overrides file was
  unreadable. Both now raise. `import_graph()` still walks all 167 repo modules.
- `edits_gdrive.connect_start`: a broken `google_client.json` silently fell back to rclone's shared client, which is
  being retired. Now it raises (a missing file still means the shared client).
- `edits_decide_queue.drain_spool`: a failed spool rewrite is now written to server_errors.log.
- `edits_claude_lane.read_answers` / `lane_score`: only a MISSING file may mean "no answers" / "n=0 checks".

## Baselined (52), grouped in the test file with a reason on each line
(a) 13 `json.loads` of a database column the app's own `json.dumps` wrote. Measured on the live edits.db
(read-only), 0 unparseable values in 724,909 `videos.hashtags`, 47,802 `accounts.signals` and 49 `runs.detail` rows.
(b) 3 model-output / eval-file parses (None becomes `{"err": "unparsed"}`).
(c) 7 that fail to the refusing side (no key, not verified, not connected, no match, download rejected).
(d) 4 reachability probes. (e) 14 caches and displays. (f) 11 best-effort side work.

## Checks
- All 15 changed functions read this PC's live files with no error: settings (42 keys), ts_status, ts_day_cap,
  run_busy False, load_policy, transfer read_state.
- Suites: 50 of the 51 that import a changed module pass (run one by one with py -3.11). `test_silent_zero_shape`:
  18 of 19 pass. The one red is exactly the 14 `tools/office` sites; no baseline line is stale.
- Live: `restart_app` ~20:36, server pid 2092 -> 32180 in 12 s. 8793 + 8794 up. home / settings / jobs / runs /
  transfer / people / history all answer 200. No new line in server_errors.log.

## Left over
- `tools/office/*`: 14 sites for 3 FIXER (BL-1718 judged them; `pending_orders` should log).
- Also fixed while reading (outside the detector): `drain_spool` skipped a torn spool LINE, which is a click that
  was not saved, with no log line. It now writes "spool-torn" to server_errors.log.
