# BL-1609: Advisor tour of the app, rules, numbers, money, gaps and reports

Read-only. $0, zero vendor calls, nothing changed. The database was opened read-only (`mode=ro`), and `config.json` was read only through `tools/config_peek.py`. Counts only. Measured 2026-10-06, about 23:00.

This covers everything not already in BL-1599, 1600, 1601 and 1608. "The owner" is the person whose tool this is; "you" is the advisor.

## CARD

1. **Key: NOT ROTATED.** The LamaTok key that BL-1598 partly printed is still the live key, and the "me" package for the owner's other PC holds that same key (sha256 compare).
2. **Nothing has reached Drive under the go-live rules.**
   - 2,011 videos wait in local review (10.05 GB of the 20 GB cap).
   - The owner has decided **1** video (NO). The friend has decided 0.
   - **772 of the waiting videos are 8 to 14 days old**, so they expire within a week unless someone reviews them.
3. **Drive free space for the new account is unmeasured.** G: now reports exactly C:'s size (930.51 GiB). So the Drive guard is reading the local disk, not the Drive quota (section 5, gap 2).
4. **Money:** $21.48 spent this month against the $60 cap, all of it since 10-02.
   - If the 07:00 daily spends its $3 ceiling every day, the cap stops it from **Oct 20** (Oct 20-31).
   - At the dailies' recent pace ($1.16 a day), the cap does not stop it in October.
5. **The 90-day item rule** (the owner's open decision) would save about 65% of per-account discovery money and lose about half the eligible new accounts (section 4).

## 1. The app

**Address:** one bilingual (Serbian and English) app at `http://127.0.0.1:8793/`, with hash routes.
- Server: `edits_swipe_server.py` + `edits_app.py`. It was started 2026-10-06 22:01 and listens on 8793 (local) and 8794 (the friend listener, which needs a token cookie).
- The share tunnel is OFF. Quick-tunnel addresses change on every start.

| Screen | Route | What it does |
|---|---|---|
| Home | `/#/home` | Shows what is waiting (videos, accounts), the API balance, free space where YES goes and on this PC, the last run, and red warnings (setup unfinished, wrong Drive account, downloads off). |
| Approve videos | `/#/approve-videos` (also `/approve`) | One review video at a time. YES places it in Drive `Approved\...`; NO deletes it (purged at next start); BACK undoes within the session; A/D keys sit behind a checkbox. **The only screen a friend can reach.** |
| Approve accounts | `/#/approve-accounts` | Eligible NEW accounts (in scope, posted within 7 days). YES = collect its fresh videos; NO = blocklisted forever. Auto-approved accounts are marked, and a NO overrides them. |
| Niches | `/#/niches` | Turns the five niches on or off, edits their hashtags and terms, and adds a niche (a niche the owner adds counts its own hashtags). |
| Accounts | `/#/accounts` | Searches stored accounts. Pasting TikTok links adds accounts to a niche. |
| Run | `/#/run` | Starts a paid run (find new accounts / get fresh videos), with an estimate bound by the run, day and month caps. Shows live progress and has Stop. One run at a time. |
| History | `/#/history` | Past decisions and videos, filterable, with CSV export. |
| Settings | `/#/settings` | API key (set or test, never shown), where YES goes (Drive or a folder, plus a test write), daily run on/off and time, caps and rules, the review-downloads switch, and My package > Rebuild. |
| People | `/#/people` | Friends' names and share links (create, revoke) and sharing start/stop. |
| Welcome | `/#/setup` | First-run wizard: key, name, destination. "Later" skips it for one browser session. **Still unfinished on this PC** (`setup_done` = False). |

**Legacy pages still served:**
- `/classic`: the old TikTok-embed video swipe. It shows videos up to 33 days old, and the app does not use it.
- `/classic-approve`: the old approve page.

**Scheduled tasks (4).** Windows task history is switched off, so each "last 3" comes from the task's own log.

| Task | Time | What it does | Last 3 results |
|---|---|---|---|
| ClippersHQ-EditsDaily | 07:00 | `tools\edits.py daily`: auto-approves proven accounts, harvests approved accounts' fresh videos into local review, snowballs, then a $0.50 discovery top-up. Budget = the $3 run cap. | **10-06** OK (cap reached), 1,036 calls, $0.6216. 56 videos went to review; 707 were skipped because the review folder was full. Alert: "download limit lowered". **10-05** OK (cap reached), 4,990 calls, $2.9940. **10-04** OK (cap reached), 824 calls, $0.4944. All exit 0. |
| ClippersHQ-Backup | 20:00 | Backs up to `D:\ClippersHQ_vault\backups`, including a consistent `edits.db` snapshot. Keeps the newest 30. | 10-04, 10-05, 10-06: PASS. 10-06: 207.1 MB, restore check 223 of 223 identical. |
| ClippersHQ-BackupPrune | 04:30 | Prunes old backups. | 10-04, 10-05, 10-06: NOTHING TO DO, exit 0. |
| ClippersHQ-OutputsGC | 04:45 | **Dry run** of the `outputs/` cleanup. | 10-04, 10-05, 10-06: "would quarantine 25 files, 469.30 KB", exit 0. Never applied. |

## 2. Every rule (setting = current value)

Values come from code defaults, overridden by `config.json`'s `edits` block, overridden by the owner's `edits_overrides.json`.
- `config.json`'s block sets the three caps, the balance lines, `max_gb_per_day`, `max_post_age_days_download` and `staging_floor_gb`.
- The owner's override file sets only `destination`, `drive_account` and `owner_name`.

| Rule | Setting = value | Notes |
|---|---|---|
| Niches | `allowed_niches` = football, basketball, ufc, tennis, superhero | "marvel" is an alias of superhero. |
| Scope | positive evidence (`edits_scope.video_verdict`) | No evidence = out; any gaming word = out. An account goes out only when its posts' out-evidence is at least 2x its in-scope evidence (`OUT_MARGIN`). |
| Out-of-scope handling | status `OUT_OF_SCOPE` | Never NO, never blocklisted. Logged in `scope_log`; undo with `edits.py scope restore <class>`. Drive files were moved to `_out_of_scope/<class>/`, and nothing is deleted until the owner says "DELETE OUT OF SCOPE". |
| Rule mode | `rule_mode` = fresh14 | the go-live rules |
| Account flagging | `flag_min_views` = 100,000 | A hashtag item of any age with this many views flags its author. Unflagged authors are never stored or paid for. |
| Account recency | `eligible_days` = 7 | Needs 1 post in 7 days. An INACTIVE account is not paid for again until an item shows a post inside 7 days. |
| Video age | `video_max_age_days` = 14 | |
| Video views floor | `video_min_views` = 20,000 | |
| Viral threshold | `viral_multiple` = 3.0, `normal_mature_days` = 3, `normal_min_posts` = 4, `viral_unknown_normal` = skip | Views must be at least max(20,000, 3 x normal). Normal = the median of the account's other posts that are at least 3 days old. |
| Review folder | `review_cap_gb` = 20, `review_floor_gb` = 25 | The cap is in decimal GB. C: must keep 25 GB free. After 14 days a video becomes REVIEW_EXPIRED. Every review status is sticky: a video is never downloaded twice. |
| Drive target | `destination` = drive, `drive_account` = SET (a hash) | With any other Google account signed in, nothing is written and YES waits. |
| Drive guards | WARN < 30 GB, STOP < 15 GB, `max_gb_per_day` = 15 | The constants live in `edits_storage`. The day limit is lowered to (free - 15) / 14 when needed, and becomes 25 GB/day once the total reads at least 1,800 GB (2 TB plan). **All of these assume G:'s size = the quota (gap 2).** |
| Daily caps | `cap_run_usd` = 3, `cap_day_usd` = 5, `cap_month_usd` = 60 | The month counts `edits.db` runs since the 1st. Also `daily_topup_usd` = 0.50, `balance_warn_usd` = 5, `balance_stop_usd` = 1. |
| Daily run | `daily_on` = True, `daily_time` = 07:00 | |
| Download pause | `review_downloads` = ON, `downloads_enabled` = OFF | Two switches. In fresh14, `review_downloads` decides whether qualifying videos download into the **local** review folder. `downloads_enabled` (BL-1604's standing pause) now governs only the legacy direct-to-Drive path, sync and index writing. Net: videos reach local review, and nothing reaches Drive without a human YES. |
| Auto-approve | `edits_auto` (no setting; always on) | NEW + active (last post within 7 days, 4+ posts in 30 days) + 2+ good edits in 30 days = YES with source `auto_proven`. Runs after every paid run and before the daily harvest. A human NO overrides it. |
| Friend links | 1 active friend link, 0 revoked | Plus the owner's own row. Sharing is off now, so the friend link reaches nothing until `share start`. |
| Other | `lanes` 4, `dl_workers` 4, `download_breaker` 10, `park_sample` 0.10, `unit_usd` 0.0006, `max_post_age_days_download` 30, `staging_floor_gb` 25, `setup_done` False | |

## 3. The numbers now

**Accounts (42,376)** by status and the niche they are stored under:

| Status | Total | superhero | football | tennis | basketball | golf | ufc | marvel |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| PARKED | 14,677 | 4,438 | 4,033 | 2,557 | 2,057 | 0 | 1,592 | 0 |
| OUT_OF_SCOPE | 9,947 | 1,735 | 1,036 | 1,188 | 211 | 4,153 | 94 | 1,530 |
| INACTIVE | 6,432 | 2,180 | 2,023 | 515 | 939 | 0 | 775 | 0 |
| NEW | 6,420 | 2,237 | 2,353 | 317 | 722 | 0 | 791 | 0 |
| YES | 3,452 | 1,163 | 1,343 | 124 | 329 | 0 | 493 | 0 |
| OFFICIAL | 829 | 125 | 134 | 276 | 58 | 162 | 74 | 0 |
| PHOTO | 517 | 140 | 161 | 60 | 51 | 43 | 46 | 16 |
| CANDIDATE | 64 | 29 | 4 | 7 | 16 | 0 | 8 | 0 |
| UNREACHABLE | 36 | 13 | 13 | 4 | 0 | 0 | 6 | 0 |
| NO | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 1 |

- **Accounts waiting** on Home and Approve accounts: 5,436 (NEW, in scope, posted within 7 days).
- **All 3,452 YES accounts are `auto_proven`.**
- **Out of scope by class:** golf 3,826, anime 1,682, music 1,600, other movies/shows 1,228, unclassifiable 775, gaming 502, other sports 334.

**Videos:**
- **Waiting in review: 2,011**, 10.05 GB.
  - By niche: football 1,538, superhero 227 + marvel 61, basketball 113, ufc 55, tennis 14, golf 3.
  - By age: up to 3 days 333, 4-7 days 900, **8-14 days 772**, over 14 days 6 (these expire at the next start).
- **Approved through review (YES): 0. Rejected: 1.**
- **Taken out of review by rules:** 2,798 dropped by the viral rule (BL-1606), 1,960 scope-out, 100 expired.
- **Before go-live (legacy, straight to Drive, no human YES):** 14,661 videos, 68.8 GB. They are in the **old** account's Drive.

**YES rates:**

| | Owner | Friends |
|---|---|---|
| Videos (Approve videos) | 0 YES of 1 decision (0%) | 0 decisions |
| Video swipe votes (BL-1603) | 0 | 0 |
| Accounts | 0 YES of 2 swipes (both NO) | cannot reach the screen |
| Accounts, automatic | 3,452 YES live (4,936 auto decisions; 1,483 withdrawn by scope) | n/a |

**Disk and storage:**
- **Review folder:** 10.05 GB of its 20 GB cap (50%).
- **C: free:** 57.8 GB (floor 25).
- **Drive:** G: reads 54.9 GB free of 999.1 GB. That is the local disk, not the quota (gap 2), so **the real Drive free space is unknown.**
- **edits.db:** 557.7 MB + 160.7 MB WAL. `edits_archive.db`: 65.4 MB.

## 4. Money

**Spend per day, last 7 days.** The ledger (`spend.json`) covers every funnel; `edits.db` covers the edit harvester only, and it is what the month cap reads.

| Day | Ledger, all funnels | Edits only | Mostly |
|---|---:|---:|---|
| 09-30 | $0.00 | $0.00 | none |
| 10-01 | $0.00 | $0.00 | none |
| 10-02 | $3.98 | $2.99 | BL-1599 $2.99, Spotify $0.98 |
| 10-03 | $4.80 | $4.53 | BL-1601 $2.79, BL-1600 $1.23, daily $0.52 |
| 10-04 | $4.89 | $4.89 | BL-1601 $4.40, daily $0.49 |
| 10-05 | $7.64 | $7.64 | daily $2.99, BL-1605 $2.99, BL-1601 $1.56 |
| 10-06 | $1.43 | $1.43 | app run (BL-1606) $0.81, daily $0.62 |
| **7 days** | **$22.74** ($3.25/day) | **$21.48** ($3.07/day) | |

The edit harvester's first paid run was 10-02, so its all-time total is the month-to-date total: $21.48.

**$ per 1,000 videos:**
- **Go-live rules** (runs 25-27, $4.42):
  - $0.64 per 1,000 downloaded into review (6,870);
  - **$2.20 per 1,000 still waiting** after the viral and scope rules removed files (2,011).
  - Per run: $0.80 (run 25); $11.10 (run 26, the folder was full); $0.26 (run 27, before its cleanup).
  - **Per video that reached Drive: undefined (0 so far).**
- **Before go-live** (legacy, $17.05 for 14,661 straight into Drive): about $1.16 per 1,000.

**When the monthly cap stops the daily.** $38.52 is left for Oct 7-31, and the month resets Nov 1.

| Pace | When the cap binds |
|---|---|
| Daily at its $3 ceiling | Oct 7-18 spend $36.00. Oct 19 gets $2.52. **Oct 20-31: no daily (12 days).** |
| The 7-day pace including manual paid runs ($3.07/day) | about Oct 19 |
| The last 4 dailies' average ($1.16/day: $0.52, $0.49, $2.99, $0.62) | $29 by Oct 31, so **it does not bind in October** |

Any run started from the Run screen draws on the same $38.52. The 10-06 daily stopped at $0.62 because the review folder was full. The folder is now at 50%, so tomorrow's daily has room to spend more.

**The "90-day hashtag items" rule.** The rule: an item must be 90 days old or less to flag its author.
- **Method:** BL-1605's method, re-run on today's database.
- **Sample:** 2,616 accounts flagged under the go-live rules over 2 days, each with a known item date.
- **Statuses are as of now.** Since BL-1605, 42% of the old-item accounts went out of scope, so its "71% inactive" now reads 41%.

| Item age | Accounts | Eligible (NEW/YES) | Inactive | Out of scope | Feed $ | 14-day 20k+ videos | In review now |
|---|---:|---:|---:|---:|---:|---:|---:|
| 7 days or less | 151 | 44 | 0% | 101 | $0.10 | 792 | 52 |
| 8-30 days | 321 | 85 | 7% | 198 | $0.20 | 763 | 33 |
| 31-90 days | 423 | 112 | 14% | 230 | $0.26 | 470 | 20 |
| **over 90 days** | **1,721** | **253** | **41%** | **720** | **$1.04** | **732** | **46** |

**What the rule would change:**
- **It saves** $1.04 of $1.59 in per-account calls (65%), about **$0.52 a day** at this pace, or about **$15 a month**. The term walk (paid per page) is not saved.
- **It loses** 253 of 494 eligible new accounts (51%), about **125 a day / ~3,800 a month** if the next 30 days look like these 2.
- **It also loses** 11 of 33 auto-YES accounts, 27% of the 14-day 20k+ videos, and 30% of these accounts' review videos.

## 5. The gaps, ranked by how much they could hurt

1. **The LamaTok key is NOT ROTATED, and it now travels.**
   - BL-1598 printed 25 of its characters into a transcript. The live key (from `config.json`; the app's own secrets file does not exist on this PC) has the same sha256 as the BL-1598 backup.
   - **The "me" package holds the same key** at `D:\ClippersHQ_portable\me\data\secrets`, and the package is meant to go onto a USB stick. The balance at stake is about $213.
   - **To fix:** rotate it at the vendor; set the new key in Settings (the secrets file takes priority for the app); update `config.json` (the other funnels read it); rebuild the package.
2. **Drive's free space for the new account is unmeasured.**
   - G: total = C: total = 930.51 GiB, to the hundredth, and the two disks' used space differs by 2.7 GiB. For the old account, G:'s size was exactly the 200 GiB quota (BL-1602's measurement), and `edits_storage` still assumes that.
   - So WARN/STOP/pacing currently watch the local disk, and the 2 TB switch can never fire.
   - If the new account's quota is smaller than its usage plus the YES videos, `place()` will still write. What Google Drive for desktop then does with a file it cannot upload has not been tested.
   - **To fix:** read the quota once on drive.google.com; make `edits_drive` report UNKNOWN when G:'s total equals the local disk's.
3. **Paid videos are expiring unreviewed.**
   - $4.42 under the go-live rules, 2,011 waiting, 1 human decision ever. 772 expire within 7 days, and REVIEW_EXPIRED is sticky (never fetched again).
   - The daily keeps refilling at up to $3/day.
   - There is no rule to pause paid runs while the queue is full of unseen videos.
4. **No human has ever checked auto-approve.**
   - 3,452 YES accounts, all automatic, against 2 human account decisions (both NO). The daily's harvest money goes to these.
   - `learn()` reads only human swipes, so nothing is learning.
5. **The month cap (section 4)** binds about Oct 19-20 if the daily runs at its ceiling. 12 days with no daily.
6. **The old Drive account holds 14,661 videos (68.8 GB).**
   - Their stored paths point there. The new account sees none of them unless the owner shares or moves the folder.
   - The old account's unexplained drain of 3-5 GB an hour outside My Drive (BL-1603/1604) was never found.
7. **The share link is dead until sharing is started.** The tunnel is off, and the address changes on every start; the friend has made 0 decisions.
8. **A frozen detached run can block the daily** (BL-1602). Detached runs run at below-normal priority and starve at 100% CPU. A frozen run holds the run lock, and the 07:00 daily is then refused.
9. **Small scope leaks into review:**
   - 3 videos whose own niche is golf (from a football YES account);
   - 18 videos from accounts that are now OUT_OF_SCOPE.
10. **Setup is unfinished on this PC** (`setup_done` = False). Home warns about it until it is done.
11. **Untested or flaky (BL-1606):**
    - the pasted-link resolver was tested only against a fake;
    - one share-access test failed once and passed on rerun, cause unknown;
    - `/classic` still shows videos up to 33 days old.
12. **`edits.db` is 557.7 MB + 160.7 MB WAL.** BL-1603 said to prune again at 605 MB (`edits.py archive`). SQLite crawls when the owner's Chrome takes the memory (BL-1601).
13. **The "me" package is a snapshot.** It must be rebuilt (Settings > My package) right before the move, or the other PC starts from tonight's state.
14. **Repository hygiene:**
    - the branch `checkpoint/session-2026-07-23-full-day` is 806 commits ahead of its remote and is not pushed (the code is vaulted on D:);
    - BL-1608's local commit contains part of the new account's email address;
    - the working tree has 58 deleted, 45 modified and about 2,900 untracked paths, so a careless `git add -A` would sweep them in;
    - 12 old claims are still listed as in flight (BL-1377, BL-1553-1559, BL-1562, BL-1597 and others).
15. **Housekeeping:** OutputsGC only ever dry-runs (25 files, 469 KB), and Windows task history is off.

## 6. The reports (BL-1599 to now)

- https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/BL-1599-the-edit-harvester-2611-edit-pages-in-the-swipe-feed-for-3-dollars.md
- https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/BL-1600-the-edit-harvester-hardened-guards-on-and-drive-is-still-not-installed.md
- https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/BL-1601-drive-found-38-gb-moved-feed-doubled-mined-terms-beat-hand-made.md
- https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/BL-1602-auto-approved-4572-proven-accounts-and-drive-is-guarded.md
- https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/BL-1603-video-swipe-and-a-friend-link-tunnel-proven-2tb-switch-waiting.md
- https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/BL-1604-downloads-paused-scope-set-to-five-niches-out-of-scope-moved-not-deleted.md
- https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/BL-1605-go-live-3747-videos-wait-for-you-nothing-reaches-drive-unapproved.md
- https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/BL-1606-the-app-bilingual-portable-minecraft-closed.md
- https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/BL-1608-drive-pinned-to-new-account-me-package-everything.md
- https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/BL-1609-advisor-tour-the-app-the-rules-the-numbers-the-gaps.md (this report)

BL-1607 has no report of its own; BL-1608 finishes it.

## What I got wrong

1. **My first tally put the system's own review verdicts in the "friend" column:** 4,858 rows of viral drop, scope-out and expiry. Those rows have no reviewer entry. Caught before writing; the table above counts them as system.
2. **My first claim was refused** because its scratch folder did not exist yet. Re-run with `--allow-new-dir`.

## How this was measured

- **Scripts:** `scratch/bl1609/`, all read-only:
  - `numbers.py`: settings, accounts, videos, decisions, disk, runs;
  - `runs_detail.py`: per-run counts and reviewer roles;
  - `item_age.py`: the 90-day rule;
  - `ledger7.py`: 7-day money;
  - `home_counts.py`: Home and the queue's ages;
  - `drive_space.py`: G: vs C:;
  - `key_rotated.py`: three sha256 values compared in memory; it prints only ROTATED / NOT ROTATED and SAME / DIFFERENT.
- **Task results** come from `edits\logs\daily.log`, `scratch\backup_logs`, `logs\backup_prune.log` and `logs\outputs_gc.log`.
- **Nothing written** to master, MARK, the workbook, `config.json`, `edits.db`, overrides or `dashboard/`.
