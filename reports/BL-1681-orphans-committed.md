# BL-1681: 11 reports were public but never in the repo, and 2 passing test files were never committed; all 13 committed now ($0)

3 FIXER, 20 Oct 07:30. This is real work taken while idle (lessons 62/65). It started as a read-only sort of the working tree: 3,088 entries
(48 modified, 58 deleted, 2,982 untracked; 2,947 of the untracked are under scratch/).

| # | Item | Result |
|---|---|---|
| 1 | **Public, not in the repo** | 9 untracked reports were already published, byte-for-byte (CRLF ignored): BL-1468, 1469 (hero grid), 1473, 1477, 1562, 1585, 1586, 1597, 1621. 2 more, BL-1479 and BL-1508, were modified after their commit and the **public copy is the modified one**. All 11 committed exactly as published. |
| 2 | **Orphan tests** | `tests/test_bl1221_supply.py` (modified 31 Aug, 6 tests) and `tests/test_bl1469_search_paging.py` (untracked, 15 tests) both **pass** on today's code (`.venv`, each file alone). Committed so they are no longer only on this PC. |
| 3 | **Left alone, on purpose** | Live stores that change every run (clip_seen.json, *_seen.json, email_harvest_tags.json, suppress_mx.json, dashboard/*.json, provenance files); 58 deleted `outputs_bl11xx_*` files (old operator outputs, removed on disk: whoever removed them decides); 2,947 scratch/ entries; `ground_truth/*` marks, `review_marks.jsonl`, `a_emails.pkl` (his data / private, not mine to commit); `CLAUDE.md`, `.claude/skills/`, `.office/` (setup, untracked by choice); `reports/BL-1371.md` (one of the 113 never published, waits for Dusan with the rest). |
| 4 | **Check** | `tools/report_drift.py` before and after: these 11 were "same" (already public); nothing is published or changed in public by this round. |
