# BL-1710 -- 3 FIXER's status said "Working" for hours: the relay never forgot hand-answered orders

25 Oct 02:22, ALFRED (auditor): 3 FIXER's status was 116 min old and still said Working, and its 23:28 seed-plan
order was BLOCKED on files that exist only on HQ. Done by 1 LEADS at HQ, $0.

## What was wrong
- The HQ relay (`tools/office/remote_fixer.py`) stamps NOW_PLAIN line 1 "Waiting" only when it is tracking no
  forwarded order. Its state still held **18 orders from 22-23 Oct** (RAM floor, supervisor corrections, the move
  to the 3090, ...). Those were forwarded while 3 FIXER's bogdan window was paused (LESSON 89), then answered **by
  hand at HQ** and moved to `read\`. No window reply ever came, so the relay kept them forever.
- Result: after the 23:28 order was forwarded, line 1 said "Working (23:28)" and could never change back.
  The window on the 3090 was alive and idle the whole time (heartbeat ~30 s old at 02:44).
- The 23:28 order's numbers already existed: 1 LEADS ran both counts at HQ at 01:08 (BL-1709, order 0046),
  so 3 FIXER's BLOCKED line was out of date.

## What changed
- `one_pass`: a forwarded entry with no window reply whose order file is gone from the folder is forgotten. The
  blocked-export branch already did exactly this. Two new tests in `tests/test_remote_fixer.py` (29 OK); the
  hand-answered test fails on the old code.
- Relay restarted by its own PID: 26112 -> 18344 (detached job `fixer_relay_0245`, outside the Windows job, host
  vast3090 from the user environment). Its first pass dropped the 18 entries and stamped "Waiting (02:46) ... the
  3090 ALIVE".
- 3 FIXER's reply to 23:28 now has line 1 = DONE with the HQ numbers. The original 3090 text is kept below it.

## Numbers (from BL-1709, unchanged)
- Follow-list seeds left: **229**, mostly private; also 2,023 public lists read only on page 1.
- Free covers vs paid labels: **92.9%** match (92 of 99 pages).
- Both are at the top of `reports/BL-1708-cheap-seed-source-plan.md`.

## Note
Advisory claim overlap with BL-1707 (3 FIXER, `tools/office/`). The change is 3 lines in `one_pass`; if a
BL-1707 patch touches the same lines, git apply at HQ will say so.
