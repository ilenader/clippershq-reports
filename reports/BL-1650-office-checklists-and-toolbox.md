# BL-1650: every Clipper Finder window has a START CHECKLIST + TOOLBOX; only a dated file is an order now

ALFRED for Dusan, order `2026-10-16_0222_SAME-FOR-1-LEADS-2-APP-AND-3-FIXER-START` (3 FIXER): START CHECKLIST + TOOLBOX.md
for 1_LEADS, 2_APP and 3_FIXER, plus each window's 3 best tools posted to COUNCIL. Copied from the ClippersHQ team's
3_REVIEWER pattern. Money: $0.

## Card

| # | Item | Result |
|---|---|---|
| 1 | **The trap found first** | `tools/office/wait_orders.py` treated EVERY `*.md` in a role folder as a new order, except RESUME.md and NOW_PLAIN.md. Dropping START-CHECKLIST.md / TOOLBOX.md into the folders would have woken all three windows on a fake order (the same bug COUNCIL reported from Flashcut on 15 Oct). `check_state.py` would have counted them as unread too |
| 2 | **Fix** | New `tools/office/orders.py` with `is_order()`: an order is ONLY `YYYY-MM-DD_HHMM_<TOPIC>.md` (office README's own naming; all 40 past orders in the three `read\` folders match). `wait_orders.py` and `check_state.py` both use it. Any other `.md` (not a known reference file) is named ONCE on a `note:` line, so a misnamed order is still seen, and does not wake the window |
| 3 | **Tests** | `tests/test_office_tools.py`: 21 OK (was 18). New: reference files alone never wake a window; a misnamed .md is noted once and does not wake it; `is_order` names; check_state still reads "unread 1" with START-CHECKLIST/TOOLBOX/HANDOFF present. **Base control:** the same tests against the old `wait_orders.py` + `check_state.py` -> 3 FAIL |
| 4 | **Live check** | On the real office: 2_APP and 3_FIXER (standing orders ignored) -> exit 3 with the new files present; 1_LEADS shows only its real order; `check_state.py` unread counts unchanged |
| 5 | **Checklists + toolboxes** | `office\<ROLE>\START-CHECKLIST.md` + `TOOLBOX.md` for 1_LEADS, 2_APP, 3_FIXER: orient (list the folder directly, LESSONS + COUNCIL), the money gate (only Dusan's quoted words with a $ figure; 1 LEADS only; $10 default cap; $15 per 1,000 target), round machinery, the role's own rules, close-out (proof, PROGRESS line, read\). Every command checked against the real tool's usage |
| 6 | **Office README** | Step 1 now says: tick START-CHECKLIST, commands in TOOLBOX; only a dated file is an order |
| 7 | **COUNCIL** | 3 lines at 02:45, best 3 tools per window: 3 FIXER (wait_orders + is_order, check_state, AI monitor), 2 APP (claude-lane, app_watch, restart_app job), 1 LEADS (raw_emails walk, run_detached, raw_pages pictures) |

## docs/FACTS.md re-stamped (not my spend)
The pre-commit facts_guard refused this commit: lifetime TikTok drifted +$19.58 past the $7.40 limit. That is
BL-1649's live $30 editors run (1 LEADS, in flight), not this round ($0). Re-stamped from one live read with
`scratch/bl1634/restamp_facts.py --round BL-1650` (47,428 rows, 2026-10-16 02:31; TikTok $132.65, total $205.92) rather
than bypassing the hook. BL-1649 will re-stamp again at its close.

## Also found (reported, not fixed: 2 APP's file)
`clippershq/edits_claude_lane.py` `lane_score()` keeps one result per VIDEO, last one wins. 3 FIXER's wrong-NO
finding (m10085) was later re-decided YES on the same video (m10152), so `claude-lane status` shows 25/25 while the
per-decision count is 25 of 26. Told 2 APP via the 01:25 reply; COUNCIL + office LESSONS line 12.

- 02:50 FINDER BL-1650 office START-CHECKLIST + TOOLBOX x3, only dated files are orders (21 tests, base control 3 red), COUNCIL best-3 x3 (DONE)
