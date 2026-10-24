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

## Part 2 (09:00): the ratchet sites in 1 LEADS' own lead files (98 -> 88 new sites)
Three of these were real data-loss paths, not style:
- `raw_emails.save_tag_ids`, `cmd_walk` (tags.json), `cmd_deliver` (the day's `.rows.json`): a torn JSON file was read as empty and then WRITTEN OVER -- the tag-id store, the run's tag list, or the day's earlier delivered rows would be lost. `cmd_deliver`'s `delivered.json` read torn as "nothing delivered yet" -> re-delivery. Now only `FileNotFoundError` means empty; a torn file raises.
- `raw_pages.page_index`: a torn `pages.json` restarted the numbering -> new pages re-used old numbers and overwrote their pictures. Same fix.
- `no_email_sheet.Api.alive`: ANY Drive error (expired token, rate limit) read as "file gone" -> callers (no_email_sheet, new_emails_sheet, sheet89) created a NEW sheet/folder and repointed the state. Now only a 404 is "gone"; anything else raises.
Loud, not narrowed: `raw_emails.dead_domains` (absent -> empty, torn raises), `raw_pages._get` (error types counted, shown in `cmd_covers` as `download_errors`), `raw_pages.render_page` (unreadable avatar/cover prints a line), `raw_pages.cmd_verdicts` (absent judge.json -> no second opinion; torn raises), `no_email_sheet.call` (an HTML error body keeps a reason).
Live files checked before narrowing: suppress_mx.json (145 dead domains) and both tag-id stores (309,134 / 819,883 ids) parse.
Suites: test_bl1643_raw_emails, test_bl1644_raw_pages, test_bl1645_text_filter, test_no_email_sheet, test_no_email_yet PASS. test_silent_zero_shape: 88 new ratchet sites left, none in 1 LEADS' files (edits app 2 APP, tools/office 3 FIXER).
Claims: BL-1677 (old, mine; its only dirty path was this round's no_email_sheet edit) released with --force; BL-1696 widened to these three files.

## Part 3 (08:16): finder-side ratchet sites (88 -> 81) + one test that never ran
- `edit_checker._tags` (measured 0 unparsable of 724,909 edits.db rows -- now says so if one appears), `edit_checker.sheet_numbers` (unreadable sheet prints a line), `free_judge._run_budget` (keeps the exception text in `_STATE["budget_unresolved_why"]`, not only a count), `meme_finder._png_area` (vanished file -> 0; other OSError printed), `mark_reader.load_records` (format tag carries the parse error), `review_loop.cmd_generate` / `cmd_ingest` (unreadable mark lines counted and printed -- they could redraw or re-append a card).
- `tests/test_bl1529_post_floor.py`: the `__main__` guard sat ABOVE `class HeroSheet`, so run as a script its 4 tests were never defined; moved to the end (8 -> 12 checks).
- 114 suites that import these modules: 16 red, 15 of them red on the 3090 before this round (full_run4, base 525625d1); the 16th was bl1529 above.
- Left: 81 ratchet sites, all in the edits app (2 APP), tools/office (3 FIXER) and tools/clippershq_open.py (app launcher).
- `requirements.txt`: `scikit-learn==1.9.0` pinned. edit_checker's learner (BL-1664) imports it, but it lived only in the system Python, so `test_edit_checker` was 6 errors in the .venv here and on the 3090. Installed into .venv through `clippershq/pipguard.py` (clean resolution; numpy 2.3.2 / scipy 1.17.1 unchanged). test_edit_checker 13/13, test_env_audit / test_bl1606_package / test_remote_fixer PASS.

## Part 5 (08:25): three finder tests that went stale against their own rules (red at HQ too)
- `tests/test_meme_finder.py` SeenSet: expected an unsigned `passed: False` page in the skip set; since BL-1478 only a SIGNED rejection (verdict + judged_by) is decided. Now checks all three were written (`include_unjudged=True`) and the skip set is a + c. 82/82.
- `tests/test_bl1528_absent_never_rejects.py`: (1) `author_video_count=4` stopped tripping the posts floor when BL-1529 set it to 1 (and a zero contradicted by the payload's own videos is not a zero), so the floor is passed explicitly (`min_posts=10`) -- the check pins that a rejection NAMES its rule; (2) `low_avg_views` was expected to reject, but BL-1534 (Dusan's instruction) made it a fact for the model -- now a check that low views does NOT reject. 21/21.
- `tests/test_funnel.py`: REVIEW_COLUMNS missed `phone` (added by BL-1666, 1 LEADS, 17 Oct). ALL PASS.
- `tests/test_bl1407_free_first.py`: the 'no image is not a rejection' window ran from the no-grid branch to the profile call, ~400 lines on, and took in the language gate's real REJECT; it now ends at the branch's own `return res`. 16/16.
- `tests/test_bl1400_ordering_and_third_state.py`: same stale fixture as SeenSet -- the "real rejection" is now written SIGNED (verdict + judged_by), as every real one is. 9/9.
- `tests/test_bl1443_bars_replay_mode.py`: a TIME BOMB. The "fresh" fixtures were dated 2026-08-30 and aged past BARS_MEMO_DAYS (30) on 29 Sep, so memes mode "stopped" skipping a barred page with nothing wrong in the code. Fresh = one day ago, computed. 6/6.
- `tests/test_bl1350_gates.py` (7 reds -> 51/51), each a pin of a rule Dusan later changed, each change documented in the code: IG recency is 180 days (BL-1496, his value, same as TikTok at his ask -- was "5 months = 152" and "must differ from TikTok"); the boundary test now sits either side of the shipped cut; share-per-play is a NOTE since BL-1534 (low ratio -> JUDGE + note; undated -> UNJUDGED still carrying the note); the `min_share_per_play=-1.0` count is 2 -- both in the same pre-purchase gate (triage + true-date re-triage); the seen-set fixture is a signed rejection (BL-1478).
- FLAG, not changed: config.json `meme_finder.stale_days` is still 152 while the code says his value is 180 (BL-1496). `run_funnel` (meme_finder.py:5964) takes `stale_days` from config when present, so the Instagram meme finder runs on the old 152 unless a campaign overrides it. `test_config_carries_it` still pins 152. Live config, owner's call -- not touched.
