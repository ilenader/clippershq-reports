# BL-1692 -- pytest no longer dies at collection on script-style tests

Problem: 9 test files end with a module-level `raise SystemExit(...)`. Under pytest that runs at import and aborts the whole session (INTERNALERROR, 0 tests run).
Fix: each now ends with `if __name__ == "__main__": raise SystemExit(...)`. Running them as scripts (`python tests/test_x.py`) behaves exactly as before.
Files: test_bl1525_stop_buying_the_tiktok_profile, test_bugfix_cap_and_402, test_enrich_concurrent, test_estimate, test_ig_cap_flag, test_market_filter, test_post_count, test_quality_score, test_video_format.
Proof: test_post_count.py as a script = 10 passed, exit 0; all 9 files parse; full pytest on the 3090 gets past collection (before: 137 errors + INTERNALERROR).
Not covered: tests needing openpyxl/tenacity (missing on the 3090) or live data cannot run there.
