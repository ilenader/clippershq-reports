# BL-1703: 1 LEADS on the 3090 -- steps on the relay allowlist, and the round trip proven (24 Oct 18:26)

3 FIXER's BL-1702 made the relay role a setting (CLIPPERSHQ_REMOTE_ROLE) and added `STEP: <name> <args>` (named HQ
commands, regex-checked args, counts-only output, paid steps refused unless money_guard passes). This round:

1. **1 LEADS' steps on the allowlist** (`tools/office/remote_fixer.py`, all free): judge89 submit|collect|status,
   merge77 plan|score, pics3090 <run>, deliver89 editors_<name>.xlsx, sheet89 push (never share), new_emails_sheet push,
   lab1700 labels|probe|tests|forecast. The paid runners (tag3090, fol3090, feeds89, part3090) are deliberately NOT on it.
   Checked locally: ping and judge89 status run; `sheet89 share`, `judge89 rm`, a `..` path and `tag3090` are refused.
   test_remote_fixer 19/19.
2. **The remote brief** `tools/office/REMOTE_1_LEADS_ROLE.md` (without it the window would have read 3 FIXER's).
3. **Round trip:** relay (role 1_LEADS, host vast3090) started 18:15; order forwarded 18:16; the window had never run, so
   the relay would not start it (it only restarts a window with a heartbeat) -- started once by hand 18:25
   (`farm-claude-window-1024182543`); answered 18:26: "DONE -- 1 LEADS on the 3090 answers"; HQ ran
   `STEP: ping` -> "pong role=1_LEADS host=vast3090 base=ad93e6a8"; report line written.

## Then stopped, and why LEADS' conductor stays on the PC for now
Relay 24164 stopped by its PID 18:28 (shim 23932 had exited with it); the 3090 window got its STOP file. Two LEADS
windows on one order folder would both act on every order. A 3090-only LEADS today could not:
- start any paid search: the relay refuses every paid step (its `money_guard_ok` looks for tools/money_guard.py, which is
  in MILOJE/tools, and a bare `check` names no wallet line) -- and nobody at HQ would start one;
- read lead data for an answer: of today's 7 LEADS orders, 4 needed it directly (cost audit, ledger facts, free-test
  labels, the move's own numbers); the other 3 (code fixes, forwarding) would work from the 3090.
Switch when wanted (one command, then this PC window closes by its own PID):
`CLIPPERSHQ_REMOTE_ROLE=1_LEADS CLIPPERSHQ_REMOTE_HOST=vast3090 python tools/office/remote_fixer.py relay`
(and delete the STOP file in D:/neuraltrack/alfred_remote_vast/teams/finder_1_leads).
Before that is worth it: paid steps with a real per-step wallet check (line + amount), and counts-only data steps for
audits. Both are relay work (3 FIXER's tool).
