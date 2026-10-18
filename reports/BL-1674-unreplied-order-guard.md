# BL-1674: unreplied-order guard -- wait_orders.py wakes a window when an order sits in read/ without its reply ($0)

3 FIXER order `2026-10-18_2200_SUPERVISOR-CORRECTION` (P1, ALFRED for Dusan). The 22:00 audit found the 20:37
RESUME-NOTE order in `3_FIXER\read\` with no `replies\2026-10-18_2037_RESUME-NOTE.md`; 1 LEADS made the same miss the
same night (LESSON 55). Money: **$0**.

## Card

| # | Item | Result |
|---|---|---|
| 1 | **Owed reply** | Written: `3_FIXER\replies\2026-10-18_2037_RESUME-NOTE.md` (line 1 DONE + the 4 resume lines). Cause: after the account switch the 20:37 order was moved to read/ on the belief that the 19:58 reply (same text, other name) covered it. |
| 2 | **Guard** | `tools/office/wait_orders.py`: each poll first lists orders (`orders.is_order`) in `<ROLE>\read\` changed in the last 24 h that have no `<ROLE>\replies\<same name>`; if any, it prints `NO REPLY: ...` and exits 0, so the idle window wakes and writes the reply. `--ignore` does not hide it. Older files (> 24 h) are not owed -- 9 old NOTE files from 14-16 Oct (info only) would otherwise wake 2 APP / 3 FIXER forever. |
| 3 | **Test** | `tests/test_office_tools.py` 29/29 OK (new: a filed order with no reply exits 0 with `NO REPLY:` and its name; a 3-day-old one is not named; once the reply exists, exit 3). |
| 4 | **Live** | `wait_orders.py <role> --max 1` on the real office for 1_LEADS, 2_APP, 3_FIXER: all exit 3 (no false wake). |

## Files
`tools/office/wait_orders.py`, `tests/test_office_tools.py`.
