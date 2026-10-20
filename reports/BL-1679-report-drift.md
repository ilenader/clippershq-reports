# BL-1679: 3 published reports were out of date and 113 were never published; `tools/report_drift.py` now finds both ($0)

3 FIXER, 19-20 Oct, from the supervisor's 20:01 and 05:14 orders ("pick real work"). No money, nothing deployed.

## Card

| # | Item | Result |
|---|---|---|
| 1 | **Stale in public** | 3 reports were edited after publishing and the public copy never changed: **BL-1659** (repo edit 21:00, published 20:57), **BL-1219** (the test_verify_claims row it later retracted), **BL-1223** (its own "CORRECTED after publication" block, local only). All 3 republished with `publish_report.py --update`; the public GET is now identical. |
| 2 | **Never published** | **113** local reports have no public copy: BL-1228, BL-1247, BL-1345 to BL-1467 (17-31 Aug), BL-1513-agentF, BL-1584-professional-tool-vocabulary. The public repo has no add and no delete for them. |
| 3 | **Secret scan (dry run, nothing pushed)** | 107 pass. **6 fail** and stay local: BL-1392, BL-1399, BL-1469 (email addresses), BL-1408, BL-1464, BL-1466_disk_survey (credential-shaped literal). |
| 4 | **Waits for Dusan** | Publishing the 107 is public and cannot be taken back, so it waits for his yes. Then one command: `office/3_FIXER/scratch/publish_107.sh` (each one still goes through publish_report.py's own scan + public check). |
| 5 | **PRIORITY item 4 was wrong** | Its "unpublished BL-1610/1612/1613/1619/1620" are all published. BL-1628 is published as `BL-1628.md` (same text, other name). |
| 6 | **Tool** | `tools/report_drift.py`: every local `BL-*.md` is **same**, **stale** (same name, other text -> `--update`) or **missing**. Matches by **content**, not name, and ignores CRLF. Reads only: it never pulls, pushes or writes. Exit 0 = clean, 1 = work to do, 2 = no folder. Live run: same 413, stale 0, missing 113. |
| 7 | **Tests** | `tests/test_report_drift.py` 5/5 OK: same/stale/missing; CRLF is not drift; a report published under another name counts; "missing" names the round's other public files; non-BL files ignored + exit codes. |

## Rule
A report you edit after publishing is still wrong in public. Run `python tools/publish_report.py <report> --update`, then
`python tools/report_drift.py` (pull the clone first) to see that nothing is stale.
