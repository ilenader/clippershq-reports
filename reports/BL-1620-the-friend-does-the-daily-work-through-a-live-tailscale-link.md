# BL-1620: the friend does the daily work, through a live Tailscale link

## Answer card

| | |
|---|---|
| **Link** | `https://desktop-fksrs2r.taileb466d.ts.net/`. It goes through `tailscale serve --bg --https=443` to `127.0.0.1:8794`, the share listener. It is tailnet only and Funnel is off. The serve config lives in tailscaled's state, so it survives restarts. The Tailscale service is Automatic, and the app starts at logon (HKCU Run, BL-1618). |
| **His one click** | Serve and HTTPS were off for the tailnet. He enabled both at `login.tailscale.com/f/serve?node=…` during the round. MagicDNS was already on. |
| **Friend can** | Approve videos (YES/NO final, BACK, SKIP). Approve accounts (YES/NO/BACK/SKIP; his decisions are tagged `friend:<name>`). Run: estimate, start, and stop or pause only a run a friend started. History, read only. |
| **Friend cannot** (403 "not allowed for this link") | The LamaTok key, Remove videos, deleting data (niches, words, people), Make this PC main, every Tools job, spend limits, every other setting, Home, and the raw /video files. 27 routes are on `edits_share.OWNER_ONLY`. |
| **Friend spend cap** | **$5/day**, shared by all friends' runs together. It is stored in `share\tailscale_friends.json` (`day_cap_usd`) and edited only in HIS Settings > Money ("Friends' runs, per day"). A run that has not ended counts its whole budget. His per-run, per-day and per-month caps still apply on top. |
| **Real-Tailscale test** | **PASSED.** Details below. |
| **Suite** | 18 new checks in `tests/test_bl1620_friend_daily_work.py`. BL-1618, 1606 (both), 1603 share and 1611 live-run all pass. See §3 for the full run. |

## 1. How the real test worked

`scratch/bl1620/friend_ts_test.py https://desktop-fksrs2r.taileb466d.ts.net --spend`

- **Who the requests came from:** this PC's own Tailscale login, added by Serve. For the test only, that login was listed as the final friend `friendtest`, the same way the real friend is listed, then removed. So every request took the real path: tailnet, then Serve (which adds the login and strips forged ones), then the share listener, then the friend policy.
- **Before:** the page was refused (this PC's login is not a friend).
  - A forged `Tailscale-User-Login` header carrying the real friend's login was also refused, because Serve strips it.
  - A forged Funnel header was refused.
- **During:**
  - `me` = friend, final.
  - Daily-work reads: 8/8 answered.
  - Video and account decide routes were reachable (a bad id got 400 and nothing changed).
  - **Owner-only routes: 27/27 refused** with "not allowed for this link", and none leaked money or key words.
  - Starting a run above the per-run cap was refused, and nothing launched.
  - In the browser (Playwright's own temp profile): the menu showed exactly 4 screens, and the video buttons yes/no/back/skip were present and enabled.
  - **Account YES then BACK** worked, and the counter was restored.
  - **Run:** Check worked. Start launched a **$0.01** friend run, Stop answered ok, and the run ended `ok_cap` with `by_friend=friendtest`, **$0.0036 spent**.
  - History loaded.
  - Each owner screen opened by link (settings, home, people, tools, niches, accounts) landed on Approve videos, with "That screen is only for the owner" shown under the heading.
- **After:** the test login was removed and the page was refused again. The real friend is still listed as final.
- **Not pressed on his real videos:** YES/NO. A final NO deletes the file. Those buttons are covered on synthetic data by the BL-1618 and BL-1620 suites.

## 2. Changes

- `edits_share`: `WORK_GET`/`WORK_POST`, `OWNER_ONLY`, `allowed(..., final)`, `ts_day_cap`/`ts_set_day_cap`. The day cap survives friend add, remove and on/off.
- `edits_swipe_server`: the final flag goes into the policy, and `_by()` goes into the run calls. `/api/cards` carries `waiting`. A friend's account decision gets the tab `friend:<name>`.
- `edits_app`:
  - `friend_spent_today`/`friend_left`, and `run_estimate`/`run_start` take `by`. The binding `friend_cap` and the error `over_friend_cap` are new.
  - `run_stop`/`run_pause` refuse `owner_run` for a friend.
  - `run_state` returns `caps` and `can_control`, so a friend never needs to read Settings.
  - `last_run.by_friend` is new, and so is the settings key `cap_friend_day_usd` (kept in the friend file, not overrides).
- `tools/edits_app_run.py --by`: writes `by_friend` into the run's detail.
- `edits_app.js` and `edits_i18n.json` (sr+en):
  - Final friends see 4 nav items.
  - A refused screen shows a visible and spoken note.
  - The Run screen shows the friend limit hint (kept live) and hides Stop/Pause on the owner's run, with a note in their place.
  - Settings > Money has the new field.
  - An accessibility-lead review found 2 major issues (the phone menu focused a hidden link; focus was lost when Stop/Pause hid) and 5 minor ones. Six were fixed. The People wording was left as is, because it is about token-link friends, and those are still videos-only.
- `tests/test_bl1618_friend_tailscale.py`: the final-friend refusal check now skips the routes that BL-1620 deliberately opens.

## 3. Suite

See the commit message for the full `run_all` result. The reds were checked against this round's files: none of them imports edits_share, edits_app, edits_swipe_server, edits_i18n or edits_app_run.
