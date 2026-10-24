# BL-1704: 2 APP on the 3090 -- app steps on the relay allowlist, and the round trip proven (24 Oct 18:37)

3 FIXER's order 1813 (BL-1702 made the relay role a setting and added `STEP: <name> <args>`): put the app's restart
job on the STEP list, start the relay as role 2_APP, prove the round trip with `STEP: ping`. $0.

1. **`tools/app_step.py`** (new, stdlib only, counts and codes only):
   - `status`: local page 8793 (build), friend listener 8794 (401 without a token = up), heartbeat pid + age; rc 1 if a port is down.
   - `restart`: the SAME POST the Tools screen sends (`/api/app/jobs {"job":"restart_app"}` on 127.0.0.1) -- the app
     starts a fresh server and the old one ends by its own PID. Never a kill. Waits up to 120 s for a new heartbeat pid.
   Proven live 18:34: **restart done in 9 s, server pid changed, 8793 + 8794 up** (no review decision in the hour before).
2. **Allowlist entry** in `tools/office/remote_fixer.py`: `"app": tools/app_step.py, args ^(status|restart)$, free,
   300 s`. New test: `app status|restart` run; `app`, `app stop`, `app restart;x`, `app kill` refused and run nothing.
   test_remote_fixer 20/20.
3. **Remote brief** `tools/office/REMOTE_2_APP_ROLE.md` (without it the window would read 3 FIXER's): the app's data,
   library, Drive and Tailscale stay on Dusan's PC; the window gets code only; a server change is live after its commit
   AND `STEP: app restart`.
4. **Round trip:** relay (role 2_APP, host vast3090) pid 5988 started 18:36, exported HEAD 4004c243 (982 files, 93
   redacted), forwarded the ping order 18:36; window started once by hand (`farm-claude-window-1024183648`; the relay
   only restarts a window that has a heartbeat); answered 18:37 "DONE -- 2 APP on the 3090 answers"; HQ ran
   `STEP: ping` -> "pong role=2_APP host=vast3090 base=4004c243" and `STEP: app status` -> "8793 UP, 8794 UP".

## Then stopped, and why the 2 APP conductor stays on the PC for now
Relay 5988 stopped by its PID (command line checked first); STOP file written in the 3090 team folder. Two 2 APP
windows on one order folder would both act on every order. Almost every 2 APP order needs Dusan's PC itself: edits.db,
the approved library on F:, Drive sends, Tailscale serve, the watchdog task. From the 3090 today only code fixes +
`app status|restart` work. Switch when wanted: delete the STOP file in
`D:/neuraltrack/alfred_remote_vast/teams/finder_2_app`, then
`CLIPPERSHQ_REMOTE_ROLE=2_APP CLIPPERSHQ_REMOTE_HOST=vast3090 python tools/office/remote_fixer.py relay`.
Before that is worth it: counts-only data steps (library status, share tailscale status, downloads status, claude-lane
status) -- each one more allowlist line pointing at `tools/edits.py`-backed commands.
