# BL-1629: keep the friend's app reachable, always

$0. No paid call. Counts only. Measured 2026-10-12, 15:30–17:10. BL-1628, the editor round in the other window, was not touched.

## Card

| | |
|---|---|
| **14:53 cause confirmed** | **Yes: my BL-1627 restart at 14:53:58** (server down until 14:54:07). His last click was at 14:53:37. His old page stopped on its first failed check, and the "(still no connection at 14:53)" line is his "Check again" pressed inside that 9 s gap. His previous server had run without a break since 10-10 22:52 (its process start time), so on 10-12 that restart was the only time the server was down while he was working. He came back at 15:56 and has since made 507 clicks, **all saved, 0 failed**. |
| **Other outages found** (last 7 days) | 2 power cuts on 10-10 (14:58 → about 15:06, and 22:25 → about 22:52) and 2 Windows restarts on 10-05 (17:34–17:38), plus my 2nd BL-1627 restart (14:56:53–14:57:01, while he was already stopped). **None of these** fell inside his review sessions. 17 pauses of 1–4 min inside his 10-12 session have **no logged cause**: the old server recorded nothing, and they are not server restarts. **UNSURE:** BL-1627's 17-second save failures fit them. Tailscale-side drops: **UNSURE** (its service logs need admin). Tailscale did not auto-update this week. |
| **Auto-update of old pages** | **Built and proved.** Every ping carries the app's build id. A page that sees a new build reloads itself at a safe moment, with clicks and BACK kept. In the throwaway-world test the friend's page reloaded by itself after an app file changed. **One last refresh is needed:** the page he has open now predates this, so it can't update itself. After that refresh, never again. |
| **Watchdog + start at boot proven** | **Watchdog: live and proven.** In the throwaway world: killed → back in **13.0 s**, the friend's page needed no click, and the clicks made while the server was down saved afterwards. Hung → back in **16.1 s**. **Live:** killed at 16:58:27, **back in 18.2 s** locally and **18.3 s through the real Tailscale address**, logged as "Server stopped (restarted by the watchdog)". **Start at system start:** built, but Windows needs admin to create it. It is one script you run once (below), and Tailscale "unattended" mode is already on, so the link works before anyone logs in. |
| **Settings changed** | **Tailscale:** unattended mode **off → on**. Service already Automatic with restart-on-failure (unchanged). Serve config survived the 10-10 power cuts; the admin script proves a service restart too. **Sleep/hibernate on AC:** already never (unchanged). **Windows Update:** active hours 08:00–01:00 → **07:00–01:00 (18 h, the maximum)** plus "no automatic restart while you're logged in", via the admin script. **App server:** Above Normal priority. Clicks refuse cleanly under 5 GB free disk. **Home:** "Friend connection". |
| **What you must do** | **1.** Run the admin script once (one "Yes" in the Windows prompt): `powershell -ExecutionPolicy Bypass -File "%USERPROFILE%\OneDrive\Desktop\clipper finder\tools\edits_admin_setup.ps1"` (or type `! powershell -ExecutionPolicy Bypass -File tools\edits_admin_setup.ps1` here). **2.** BIOS: "Restore after AC Power Loss" = Power On (steps below). **3.** The 2-minute reboot test (below). **4.** The friend presses F5 once, the last time. |

## Your steps

### 1. The admin script (once, about 1 minute)
`tools\edits_admin_setup.ps1` asks Windows for administrator rights itself, then:
- installs **ClippersHQ-AppWatchdog-Boot**, which starts the app at system start whether anyone is logged in or not. No password is stored;
- sets Windows Update active hours to 07:00–01:00 and turns on "no automatic restart while a user is logged on";
- restarts the Tailscale service and checks that the friend's link (Serve 443 → 8794) is still there.

It prints before and after, and writes `%LOCALAPPDATA%\ClippersHQ\edits\logs\admin_setup.log`. **The friend's link drops for a few seconds while Tailscale restarts**, so run it when he isn't reviewing.

### 2. BIOS: power on after a power cut (MSI B450M-A PRO MAX, Click BIOS 5)
1. Restart the PC and keep pressing **Delete** until the MSI screen appears.
2. If it opens in **EZ Mode**, press **F7** for Advanced Mode.
3. Go to **Settings → Advanced → Power Management Setup**.
4. Set **Restore after AC Power Loss** to **[Power On]**. **[Last State]** also works if the PC is always left on.
5. If **ErP Ready** is there, leave it **[Disabled]**.
6. Press **F10**, then **Yes**, to save and restart.

### 3. The 2-minute reboot test (after steps 1 and 2)
1. Start → Power → **Restart**. **Do not log in.** Leave the PC at the sign-in screen.
2. On your phone (with Tailscale on), open `https://desktop-fksrs2r.taileb466d.ts.net/` about **2 minutes** after the sign-in screen appears. Your phone is not a friend login, so you get the short **"This link is not valid"** page. That page comes from the app, so it means the app is up. A browser error ("can't reach") means it isn't. Or ask the friend to open the link: he should see Approve videos.
3. Log in. Open the app → **Home → Friend connection**. There is a row **"PC was off or restarting"** with its start and end.
4. Optional: before logging in, the friend can press NO. A YES may say "YES is not possible right now" until you log in, because Google Drive starts at your login. About 30 s after you log in, the server moves into your session by itself (Home shows a row "Moved into the logged-on session").

## 1. Asked

Prove that 14:53 was the restart and list every other unreachable time with its cause. Old pages update themselves. No button needed after a lost link. A watchdog restarts the app within 30 s, and the app starts at system start without a login; prove it by killing the server. The PC never sleeps, no Update restarts while the app is in use, and Tailscale survives a restart (prove it); report each setting before and after; BIOS steps. Above Normal priority, clean refusal under 5 GB free, and the top 10 processes by RAM. Home shows "Friend connection" with every outage logged.

## 2. Shipped and proved

**Auto-update** (`edits_swipe_server.app_build`, `edits_app.js` `sawBuild`/`maybeReload`):
- `/api/r/ping` carries a 12-character build id taken from the size and modified time of the page files.
- The ping no longer waits behind the server's big lock. It used to, so a slow page read made the link check hang.
- A page reloads only at a safe moment: on a screen change, when the tab is hidden, or after 60 s with no key or pointer. Never while a click is being sent, and once per build at most, so a restart can't loop it.
- After reloading, it says "The app was updated." and puts focus on the heading.
- Clicks and BACK history live in localStorage, so a reload loses nothing.

**No button needed** (`halt`/`autoRetry`/`tick`):
- A lost link retries by itself every 3 s on every screen.
- The alert ("The PC is restarting or offline. Clicks on the Approve screens are kept; nothing on this screen can be saved until it reconnects.") is spoken once. Only a quiet "Last try: HH:MM:SS" line updates.
- One missed ping is ignored.
- Owner screens stay locked while offline, so nothing there can be written, and they unlock by themselves.
- The "Check again now" button stays as an optional control.
- The Approve screens never lock; their saving line says "The PC is restarting or offline. Your clicks are kept."

**The watchdog** (`tools/edits_watchdog.py`, task `ClippersHQ-AppWatchdog`):
- Every 5 s it checks the app and the friend's listener. After 2 misses in a row:
  - **Hung server:** it ends the one server process, identified by the pid in the server's own heartbeat and checked to be the app server.
  - **Dead server:** it starts a new one with no window, never idle-exiting.
- It respects the app's own Restart (a 25 s grace period).
- Every 5 min it checks Tailscale Serve and puts it back if it is missing.
- One watchdog per Windows session. The watchdog of your logged-in session takes over a before-login server that can't reach Google Drive.
- It runs at Normal priority. Task Scheduler's default is Below Normal, which starves under load.
- **Installed live** (your session): watchdog running, Normal priority.
- The boot version is `edits_watchdog_task.ps1 -Boot`, inside the admin script.

**The outage record** (`clippershq/edits_outages.py`):
- The server writes a heartbeat every 5 s and a note saying why it ends. The watchdog writes a note before each repair.
- A starting server combines these with Windows' boot time and records **one row**: start, end, cause.
- The causes:

  | Cause | Shown as |
  |---|---|
  | restart | App restart |
  | pc_off | PC was off or restarting |
  | watchdog_hung | Server stopped answering (restarted by the watchdog) |
  | watchdog_died | Server stopped (restarted by the watchdog) |
  | handover | Moved into the logged-on session |
  | stopped | App closed |
  | link | The link dropped (friend's internet or Tailscale), reported by his page after it is back and never double-counted with a server outage |

- Every row also goes into `logs\outages.log`.
- **Home → Friend connection:** last seen (time and minutes ago), drops today, and a table of the newest 10 outages (start, end, length, cause).

**Resource guards:**
- The server sets itself to **Above Normal**.
- A click is refused with **507** and nothing recorded when the database disk has under **5 GB** free. The page keeps it and retries, and the saving line says "The PC's disk is almost full".
- The worker holds a YES copy while the destination disk is under 5 GB.

**Accessibility review first** (accessibility-lead, before any UI edit). All must-fix items are in:
- the "last try" line sits outside the alert;
- the alert is set only once;
- no reload while working, and none before the announcement; it is announced on the new page instead;
- the message is honest on the screens that lock;
- a change of failure cause (offline → disk) is announced;
- "Connected again." is said when nothing was waiting;
- the outages are a real table with row headers and scrolling on narrow screens.

**Proof on a throwaway world** (`scratch/bl1629/watchdog_proof.py`): a temp copy of the code; the friend's page in a throwaway Chromium profile **through Tailscale** (Serve port 8443, never 443); this PC's own login as the world's friend.

| Check | Result |
|---|---|
| Nothing running: the watchdog starts the server | 12.9 s |
| **Kill the server** | **back in 13.0 s**; the friend's page showed no banner, **no button pressed**, and the 4 clicks made while it was down saved 0.5 s after it came back |
| Owner screen, 40 s outage | showed "The PC is restarting or offline…" plus the "last try" line, and **cleared by itself 2.4 s** after the server came back |
| **Hang the server** (suspended) | the watchdog ended that one process: **back in 16.1 s** |
| An app file changed (a new build) | the friend's page **reloaded itself**; outbox kept (0 lost) |
| Database | **10 of 10 clicks carried out exactly**; outages logged: died, died, hung |

Caveat: my test clicks didn't count as "input", so the reload's 60-second-idle rule was met at once. The reload itself is proven; the wait-for-idle is not.

**LIVE** (his setup; every restart only after his last click was over 5 minutes old, checked with `scratch/bl1629/wait_idle.py`):

| Step | Result |
|---|---|
| Deploy | 16:57:30, the app's own Restart (his last click 16:51:05): back with the new code at **16:57:41** (11 s) |
| **Kill the live server** (`live_kill_test.py`) | 16:58:27: **back in 18.2 s locally and 18.3 s through the real Tailscale address** |
| The outage the new server recorded | 16:58:26 → 16:58:45, 19 s, cause **"Server stopped (restarted by the watchdog)"** |
| Watchdog log | "server not running → starting it", then "server back after 3.0 s" |
| Home → Friend connection | drops today 1, last seen 16:58:13 |
| Priority | the replacement server runs **Above Normal**; the watchdog runs at Normal |

**His real page:** it was open, and it reached the new server by itself at 16:58:13, after the 16:57 deploy restart, with no click. After the 16:58:27 kill it had not checked in again by 17:04. **UNSURE** whether he had closed it or Chrome had paused the hidden tab. The page that carries on without a click is proved in the throwaway world above.

**Suite:** 17 new checks in `tests/test_bl1629_reachable.py`. 29 related suites passed with `run_all -k`; the result is in the commit message.

## 3. Measured

**The settings, before → after:**

| Setting | Before | After |
|---|---|---|
| Sleep on AC / on battery | never / never | unchanged |
| Hibernate on AC / on battery | never / never | unchanged |
| Windows Update active hours | 08:00–01:00 (17 h) | **07:00–01:00 (18 h, max)**, admin script |
| No automatic restart while logged on | off | **on**, admin script |
| Tailscale service | Automatic, restarts itself on failure | unchanged |
| Tailscale unattended mode | **off** (the link only works while you're logged in) | **on** |
| Tailscale Serve | 443 → 127.0.0.1:8794, tailnet only | unchanged (the watchdog re-applies it if it's ever missing) |
| Tailscale auto-update | on (each update restarts its service briefly) | unchanged; such a drop is now logged |
| App server start | at your login only (Run key) | watchdog task in your session (live) **plus** at system start (admin script) |
| App server priority | Normal | **Above Normal** |
| Watchdog priority | (none) | Normal |

**Top 10 processes by RAM** (at 16:05, MB, all copies added up): chrome 5,678 · claude 4,782 · python 2,021 · svchost 1,507 · Spotify 1,103 · ffmpeg 1,100 · Discord 863 · MsMpEng 564 · msedgewebview2 529 · bash 484.
- RAM: 23.9 GB total, 4.1 GB free.
- Free disk:

  | Disk | Free |
  |---|---|
  | C: | 306.6 GB |
  | D: | 113.7 GB (down from 212.1 GB on 10-11; not this round) |
  | F: | 2,470 GB |

**The friend since 15:56**, on BL-1627's save path:
- 507 clicks, 507 done, 0 failed.
- From click to carried out: 1.25 s on average, at most 12.4 s.
- None of that is time he waits.

## 4. What I got wrong

- **I printed this PC's own Tailscale login into my tool output** while reading Tailscale's settings. It is in no file and no report.
- **I wrote two more pointless empty heredocs** (no-ops), against the editor rule; and one more later (counted below).
- **My first watchdog ran at Below Normal priority** (Task Scheduler's default). I caught it live and fixed it in both the code and the task.
- **One of my own test expectations was wrong** (outage order). The code was right.
- **"Above Normal" silently didn't apply the first time.** ctypes cut Windows' "current process" handle to 32 bits. The live check showed Normal; fixed (`set_priority`), a test now checks the real priority, and the live server runs Above Normal.
- **I wrote one more empty heredoc** while filling this report.

## 5. Money and stores

- **$0**, no vendor call.
- **His setup:**
  - Tailscale unattended mode turned on.
  - Task **ClippersHQ-AppWatchdog** added (his session).
  - The app server restarted once (16:57:30), and killed once for the proof, only after his last click was over 5 minutes old.
  - `edits.db` gained the `outages` table.
- **Untouched:** the live database apart from that, his files and other tasks.
- **Tests and proofs:** temp homes and throwaway worlds. Serve port 8443 was added and removed; 443 was never touched.

## 6. Leak scan

The secret scan runs inside `publish_report.py`. The two-corpus scan (`scratch/bl1604/leak_adjudicate.py`) on the round's new files: 0 unexplained.

## 7. Next

Your steps 1–3 above. After the reboot test, Home shows whether the before-login server could reach Google Drive. **UNSURE** until then: YES in the first minutes after a power cut, before you log in.

## 8. Paths

- **Code:**
  - `clippershq/edits_outages.py` (new), `edits_swipe_server.py`, `edits_decide_queue.py`, `edits_share.py`
  - `edits_app.js`, `edits_app.html`, `edits_app.css`, `edits_i18n.json`
- **Tools:** `tools/edits_watchdog.py`, `tools/edits_watchdog_task.ps1`, `tools/edits_admin_setup.ps1`
- **Tests:** `tests/test_bl1629_reachable.py`
- **Proof and evidence scripts:** `scratch/bl1629/` (`watchdog_proof.py`, `live_kill_test.py`, `outage_evidence.py`, `wait_idle.py`)
- **Logs:** `%LOCALAPPDATA%\ClippersHQ\edits\logs\watchdog.log`, `outages.log`, `server_errors.log`, `admin_setup.log`
