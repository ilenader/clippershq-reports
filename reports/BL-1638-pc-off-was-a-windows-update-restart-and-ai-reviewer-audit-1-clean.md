# BL-1638: the 03:44 "PC off" was a Windows Update restart; blind audit #1 of the AI video reviewer is clean (240/240)

$0 vendor spend. No paid call. 3 FIXER orders `2026-10-14_0830_P0-why-the-PC-turned-off`,
`2026-10-14_1005_AUDIT-ai-reviewer` and the overnight standby `2026-10-14_0140_STANDBY-audit-ai-reviewer`.

## Card

| # | Item | Result |
|---|---|---|
| 1 | **Why the PC "turned off" 03:44-08:23** | **A Windows Update restart, not a power cut.** Windows restarted twice (03:44 and 03:49) for the October security update, was back by **03:49:34**, then sat at the sign-in screen until the owner signed in at **08:21:58**. Everything of ours starts only at sign-in, so `outages.log` booked the whole 4.6 h as `pc_off`. Our load played no part. |
| 2 | **Blind audit #1, AI reviewer v4 (BL-1637)** | AI right on **240 / 240** judged = **100.0 %, 95 % interval 98.5-100 %** (Clopper-Pearson). 0 undecided, 0 wrong. Strict reading (TV-series character edits are not "movies"): 238/240 = 99.2 % (97.0-99.9 %). |
| 3 | **wait_orders.py --ignore** | A window working on a standing order can wait for *new* orders without the standing order waking it at once. `--ignore NAME` can be repeated. Test added; office tests **18/18 OK**. |

## Item 1: evidence (System event log, read-only)

- 02:19 WindowsUpdateClient 43: install of the 2026-10 Security Update (KB5127648) started. The earlier pause on updates ran out on 10-01.
- **03:44:35 User32 1074**: `MoUsoCoreWorker.exe` started a restart on behalf of SYSTEM, reason "Operating System: Service pack".
- 03:44:53 Winlogon 7002: the user was logged off.
- 03:46:42 Kernel-Power 109: "Power Action Reboot".
- 03:47:03: boot.
- **03:49:11 User32 1074**: `TrustedInstaller.exe` started a 2nd restart, reason "Upgrade".
- 03:49:34: boot. This is still the current `LastBootUpTime`.
- 03:50:57 WU 19: KB5127648 and .NET KB5127694 installed.
- 04:02-05:10: Time-Service events show the PC was running.
- **08:21:58 Winlogon 7001**: the owner signed in. The watchdog started at 08:23:17 and the server was back at 08:23:51.
- **Not found** (all ruled out): Kernel-Power 41 and EventLog 6008 (both shutdowns were clean; Kernel-Boot 20 says the last shutdown succeeded), BugCheck 1001, minidumps, WHEA 17/18/19/47, thermal events and Resource-Exhaustion 2004. NTFS reported C, D and F as healthy.
- The PC never slept: sleep is set to Never on AC, and the wake history count is 0.
- Settings that made it possible: active hours are 08:00-01:00, so 03:44 was an allowed restart time. Auto sign-in is off (`AutoAdminLogon 0`).
- Side effect: the restart killed 2 APP's overnight BL-1637 run part-way through.

**Owner's steps** (in the order reply):
1. Turn on gpedit "No auto-restart with logged on users for scheduled automatic updates installations", or pause updates on nights with long runs.
2. Turn on Sign-in options > "Use my sign-in info to automatically finish setting up after an update".
3. Optional, for real power cuts: set BIOS "Restore on AC Power Loss" to Power On.

**Suggested to 2 APP** (its file; not touched): `edits_outages.py` could split `pc_off` into the restart itself and the wait for sign-in (boot to Winlogon 7001).

## Item 2: audit method

- 240 items: the AI said 152 YES and 88 NO, a random draw by 2 APP from 270 v4 auto-decisions.
- **Blind labelling.** Six independent sub-agents (sonnet, 40 items each) labelled every item against the owner's spec only, from 12-frame contact sheets (24-frame sheets when unsure). They opened only the sheet folders, and `ai_verdicts.csv` was opened only after all labels were in.
- **Agreement.** The labellers agreed with the AI on 238 items: the verdict, and the niche for every YES.
- **The 2 disagreements**, re-checked by me on both sheets. The AI was right on both:
  - a197 is a "quote + edit": a captioned press conference, then graded slow-mo cuts.
  - a159 is a heavy edit of TV-series characters, which is a spec question.
- **Spot-check.** I also looked at 8 risky agreements myself (stills-made edits, match clips with effects, lyric text over match clips, interview plus highlights, a TV-franchise edit). The AI was right on all 8.
- **Spec questions** passed to the owner through 2 APP:
  1. Do TV-series character edits count as "movies"?
  2. Do edits built from still photos count, when they have heavy motion effects (counted here as edits, not slideshows)?
  - Minor: 4 static screenshots or memes are labelled kind `broken` (the NO verdict is right).
- **Limit.** The labellers are Claude models, as the reviewer is, so the near-total agreement is strong but not fully independent. My own eyes covered 10 of the 240.
- Result file for 2 APP: `office\2_APP\2026-10-14_1015_AUDIT-RESULT.md`. Audit #2 is parked by 2 APP until OpenRouter is topped up.

## Commits

- `tools/office/wait_orders.py` and `tests/test_office_tools.py`: the `--ignore` option and its test.
- This report.
