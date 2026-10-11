# BL-1621: briefing for the strategist — the business, the machines, the rules, the money, and what is broken right now

Read-only. $0, no vendor call, no config change, no commit in the project repo. `config.json` was read only through `tools/config_peek.py`. Counts only. Measured 2026-10-11, 10:40–11:35. `<repo>` = the project folder on his OneDrive Desktop; `%LA%` = `%LOCALAPPDATA%`. **UNSURE** marks anything not measured.

## Answer card

| | |
|---|---|
| **What this is** | A lead factory plus a video-harvest app, run by the owner (voice, not technical) through Claude Code rounds named BL-NNNN. The code repo is private and **835 commits ahead** of its GitHub copy, unpushed on purpose. Reports go to the public reports repo. |
| **BROKEN NOW #1** | **This morning's 07:00 daily run failed, and the main "ClippersHQ" shortcut is dead.** At 10-10 18:22, BL-1620's test suite ran `tools/edits_me_first_start.py --help` from a temp copy. That tool ignores `--help`, so it reinstalled the daily task's `.bat`, the Start Menu and Desktop shortcuts, and `MAIN_PC.json`, all pointing at the temp folder, which is now gone. The task still shows "result 0" because the `.bat` swallows the exit code. The fix is small (repoint 1 `.bat` and 2 shortcuts, and make that tool honour `--help`), but it touches his live setup, so it needs its own round. |
| **BROKEN NOW #2** | **The $100 lifetime cap is used up:** $116.32 booked. Every old finder (TikTok clippers, Spotify, Twitch, meme pages, email finder) now resolves to $0 and refuses. The edit app and the editor-email walker have their own caps and still run. |
| **Power loss** | It was **last night, not today**, and there were **two**: about 14:58 and about 22:30–22:50 on 10-10. The last boot was 10-10 22:50. The app server, Tailscale and Google Drive all came back within 2 minutes. A BL-1619 paid walk started at 22:26 died with the power. |
| **BL-1619 is LIVE in another session** | Its report says "finished", but a phase-2 walk started after the report. Today at 11:26–11:31 a session wrote `scratch/bl1619/` (integrity, ledger replay) and booked $0.03 "crash gap". I did not touch it. Its code is **uncommitted**. |
| **Not published** | BL-1610, 1612, 1613, 1619, 1620 (and 1584) exist only on this PC. **BL-1618 has no report anywhere.** You cannot read those by raw link. |
| **Money** | $51.04 spent in the last 30 days, of which $24.87 is the edit app. LamaTok balance was about **$204** (10-10 evening). **The LamaTok key is still not rotated** (partly printed in BL-1598). |

## 1. The business

| | |
|---|---|
| **ClippersHQ** | The owner sells short-form clipping (cutting creators' long content into shorts) and runs edit pages. This repo **only produces leads and harvests videos. It never sends anything:** he has a separate tool that emails leads daily and closes clients (`docs/NO_SEND.md`, a standing rule since BL-1446). |
| **Clippers / editors** | People who cut and edit short videos: faceless "edit pages" (football, movies, anime…), fan-editors and clip channels. They are the **supply side**, people to hire or recruit. The biggest lead list (about 55.8k "clipper" rows) is them. |
| **Clients** | Creators with money who would pay for clipping: Spotify artists (the only live client funnel), Twitch streamers, YouTubers and app developers (all dormant). |
| **Lead lists, what each is for** | **Clipper / editor emails** (`operator\clipper_emails_ALL.xlsx`, about 4.4k distinct addresses): recruit editors. **Niche editor emails** (football/tennis/movies, 216 rows): editors for his five niches. **Spotify clients** (`operator\spotify_clients_*.xlsx`, about 14.5k rows): sell clipping. **Meme pages** (1.9k): pages to buy or partner with (UNSURE of the exact use). All feed his separate sending tool. |
| **Edit harvester / "the app"** | Finds TikTok edit accounts in 5 niches (football, basketball, UFC, tennis, superhero), downloads their **viral** recent edits (≤14 days, views ≥ max(20k, 3× the account's normal)) into a local review folder. He or a friend presses YES/NO; only a YES moves a video to Google Drive. **UNSURE:** what the approved videos are used for after Drive (presumably reposting on his pages). |
| **The friend** | A reviewer on another machine who reaches the app through Tailscale (tailnet only, never public). Since BL-1620 a "final" friend can approve videos and accounts, start or stop their own runs (capped at $5/day for all friends together) and read history. On 10-10 the friend judged 401 videos (155 YES). |
| **Danilo** | Runs **his own copy of the Spotify client-lead system** on his own machine with his own keys, set up by his own Claude Code from `%LA%\ClippersHQ\operator\handoff\SETUP_GUIDE_FOR_DANILO.md` (BL-1596). He has the guide, a config template with placeholder keys, and a skip list of **5,135** Spotify artist IDs so his runs do not duplicate ours. Open since BL-1596: the skip list covers only 5,135 of about 14,048 Spotify rows. The owner must choose: send the partial list, split seeds between the two machines, or share a hashed handle list. **UNSURE** whether Danilo's copy is current (it could not be compared from here). |

## 2. Machines

| Fact | Value | Source |
|---|---|---|
| This PC | The owner's desktop, Windows 11 Pro. Hostname withheld. | `hostname` |
| MAIN PC? | **Yes.** `G:\My Drive\ClippersHQ Edits\MAIN_PC.json` names this PC (hashed machine id matches). It was rewritten 10-10 18:22 by the same accidental `first_start` run (same PC, so harmless). | Machine agent, re-hashed |
| Other PC / transfer | **No transfer.** BL-1618 cancelled the move, and this PC stays main. A complete transfer package sits on Drive (`ClippersHQ Transfer\`, 5,153 files, 19.9 GB, verified 10-08). It was never installed on another PC. | Drive listing; BL-1612/1618 |
| Google Drive | Installed, signed in, **G:**, running (started 2 min after boot). G: reports C:'s size (930.5 GB), so **the real Drive quota is unknown**. | `Win32_LogicalDisk`; BL-1609 gap 2 |
| Disks free / total | **C:** 327.7 / 930.5 GB · **D:** 212.1 / 894.2 · **F:** 3,010 / 3,726 · **G:** reads 311.3 / 930.5 (not the quota) | `Win32_LogicalDisk`, 11:33 |
| RAM | 23.9 GB, about 6.4 GB free | `Win32_OperatingSystem` |
| Last boot | 2026-10-10 22:50 | same |
| Vault roots (every operator file is copied to both and sha-checked) | `%LA%\ClippersHQ\vault_bl1574` and `D:\ClippersHQ_vault` (3.4 GB) | `clippershq/operator_home.py` |
| Backups | Nightly tgz to `D:\ClippersHQ_vault\backups` (newest 10-10 20:39). The code also has a git bundle in both vault roots (BL-1576). | scheduled task; memory |
| His files ("operator home") | `%LA%\ClippersHQ\operator`. **Never his Desktop** (he deleted Desktop files; BL-1587). | `operator_home.py` |
| Edit app data | `%LA%\ClippersHQ\edits\` (`edits.db` about 600 MB, review folder, logs, `bin\*.bat`) | BL-1609 |
| D: folders | `ClippersHQ` 26 GB (friend picks and more), `ClippersHQ_vault` 3.4 GB, `ClippersHQ_portable` (old package; agents are blocked from deleting it, so he must) | `du` |

## 3. Repo map

| Folder | What lives there |
|---|---|
| `clippershq/` | **All code (231 modules).** One package; the funnels are below. |
| `tools/` | 72 entry points (below) |
| `tests/` | 538 suites. **Run them only with `tests/run_all.py`** (one process per suite; `unittest discover` lies). The full run takes 20–45 minutes; the last result was 37 red of 563. |
| `reports/` | Local copies of every report (`BL-NNNN-<slug>.md`) |
| `scratch/blNNNN/` | Each round's scripts plus `PROGRESS.md` (11.7 GB in total, mostly old) |
| `docs/` | About 70 docs. Some are stale: `STATE.md` (07-22), `HANDOVER.md` (08-03, still tells you to fill a send file, which contradicts NO_SEND). |
| `dashboard/` | The old lead-finder dashboard on port 8787. **Not running now.** UNSURE whether it is still wanted. |
| `video download/` | **His own downloader** (yt-dlp + ffmpeg). The app calls it for every video. Never modify it. |
| `memebot/`, `hookmark/`, `clip_library/` | Older side projects. `memebot/` is its own git repo. |
| Root | `master_leads.csv` (77,533 rows, the de-duplicated master of every lead), `spend.json` (the shared money ledger), `config.json` (keys, so read it only via `config_peek`), `START.bat` (the old lead-finder menu), hundreds of `*.bak` backups |

**Key module per funnel:**

| Funnel | Module |
|---|---|
| TikTok clipper finder | `tiktok_finder.py` (older campaign path: `main.py`) |
| Editor / email walks | `email_harvester.py`, `harvest_run.py`, `edits_vendor.py` |
| Spotify clients | `spotify_finder.py`, `playlist_harvest.py`, `listenbrainz.py` |
| Twitch / YouTube / Google Play | `twitch_finder.py` / `youtube_finder.py` / `google_play_finder.py` |
| Meme pages | `meme_finder.py` |
| Repost accounts | `repost_finder.py` |
| Edit harvester + app | `edits_engine.py`, `edits_app.py` (+ `.html/.js/.css`), `edits_swipe_server.py`, `edits_scope.py`, `edits_viral.py`, `edits_review.py`, `edits_drive.py`, `edits_share.py` (friend roles), `edits_db.py` |
| Ledger and caps | `spend_ledger.py`, `finder_common.effective_run_cap` |
| Dedupe into master | `crossdedup.append_leads` |

**Entry points you will see in briefs:**

| Tool | Does |
|---|---|
| `tools/edits.py` | The edit harvester CLI: `daily`, `waiting`, `scope restore`, … |
| `tools/edits_app_run.py` | A run started from the app |
| `tools/run_detached.py` | Long jobs as one-off scheduled tasks |
| `tools/claim.py` | Live claims |
| `tools/commit.py` | Pathspec commits |
| `tools/publish_report.py` | The only way to publish |
| `tools/config_peek.py` | Masked config reads |
| `tools/verify_claims.py` | Checks shipped-claim manifests |
| `tools/backup.py`, `backup_prune.py`, `outputs_gc.py`, `scratch_gc.py` | Housekeeping |
| `tools/edits_package.py`, `edits_transfer*`, `edits_me_first_start.py` | Portable copy and moving PCs |
| `tools/review_loop.py` | Grading pages |
| `tools/clippershq_open.py` | Opens the app |

**Start Menu > ClippersHQ** (targets read 11:00):

| Shortcut | Opens | State |
|---|---|---|
| **ClippersHQ** (also on the Desktop) | The app | **BROKEN:** points at a deleted temp folder |
| Approve videos / Approve accounts / Swipe accounts | App pages via `edits\bin\*.bat` | OK |
| Find new accounts / Get today's edits | Paid app runs via `.bat` | OK |
| Share video swipe / Stop sharing | The old quick-tunnel share | OK (superseded by Tailscale) |
| Open edits folder | Explorer | OK |
| Grade cards | `operator\review_CURRENT.html` | OK |
| Lead workbook | `operator\clipper_emails_ALL.xlsx` | OK |
| ClippersHQ Leads | Explorer on `operator\` | OK |
| Spotify clients | The newest `spotify_clients_*.xlsx` | OK |
| ClippersHQ Friend picks | `D:\ClippersHQ\friend_picks` | OK |

The app itself is at `http://127.0.0.1:8793/` (bilingual Serbian/English). Screens: Home, Approve videos, Approve accounts, Niches, Accounts, Run, History, Settings, People.

## 4. How rounds work

| Piece | How |
|---|---|
| **BL ids** | Sequential (latest BL-1620; this is BL-1621). Check that an id is free locally and on the reports remote before writing. The reports repo **also receives BL-9xx reports from a second project on this PC** (a separate "ClippersHQ" repo, e.g. a marketplace engine). Ignore those ids. |
| **Live claims** | `python tools/claim.py start BL-N --intent … --write <paths>` at the start, `end BL-N` at the end. This writes `.claims/BL-N.json`. **Advisory only**, meant to answer "who is touching what right now". The registry is dirty: 13 stale entries show as "in flight", and 2 files are malformed. |
| **Shipped claims** | `docs/claims/BL-N.claims` lists every identifier the report says shipped. `tools/verify_claims.py` proves each one is committed at HEAD, and a test re-checks every manifest forever. Commit the manifest only **after** the code it cites. |
| **PROGRESS.md** | `scratch/blNNNN/PROGRESS.md`, a step table updated after every step, so a crash or a new session can resume. Paid runs also checkpoint per page or tag. |
| **Work data** | Handles, bios and addresses go to `%LA%\ClippersHQ\blNNNN_work\`, **never the repo**. Repo files hold counts only. |
| **Commits** | `tools/commit.py BL-N -- <paths>` (pathspec only; the git index is shared by every concurrent round). Never `add -A`, `reset --hard`, `clean`, `checkout --` or `stash -u`. |
| **Suite** | `PYTHONUTF8=1 .venv\Scripts\python.exe tests/run_all.py`. Quote only its final verdict line. Check whether a red is yours with `-k <suite>` or `--head` (each `--head` leaves about 1.3 GB in %TEMP%). |
| **`publish_report.py`** | `python tools/publish_report.py reports/BL-N-<slug>.md`. It runs the secret scan (`--profile public`: config strings, credential shapes, emails, and a join against real leads), reads the scan's exit code from the process (never through a pipe), refuses to overwrite an existing report unless given `--update`, regenerates `MANIFEST.tsv`, pushes from the fixed clone `%LA%\ClippersHQ\clippershq-reports`, then fetches the raw URL anonymously to prove it is public. |
| **Eight-section standard** | A card first, then **his steps / decisions**, then 1 Asked · 2 Shipped and proved · 3 Measured · 4 What I got wrong · 5 Money and stores · 6 Leak scan · 7 Next · 8 Paths. After publishing, a 6-line summary block (shipped / the number / outside the brief / wrong / still broken + whose / suite + spend). |
| **Leak scan** | Run in addition to the secret scan. Every file the round wrote is checked against **two corpora**: the **edit corpus** (`edits.db` handles and nicknames) and the **lead corpus** (`master_leads.csv` handles, display names and Instagram handles). Hits are matched against the public term vocabulary and adjudicated **by value without printing it**. Recent rounds use `scratch/bl1604/leak_adjudicate.py <files>`. |
| **`run_detached.py`** | `start --name X -- <cmd>` runs a long or paid job as a one-off Windows scheduled task (pythonw, no window), so it survives the Claude Code session, which **reaps background shells on low memory** (BL-1600 lost about $8.75 of approved work that way). Jobs and logs go to `%LA%\ClippersHQ\jobs`. Use `status` / `tail` to read them. Jobs run at below-normal priority and starve when the CPU is busy. |

## 5. Rules

**There is no CLAUDE.md in the repo.** The rules live in the owner's global `~/.claude/CLAUDE.md`, the repo docs, and **728 memory files** (only about 344 of them fit in the always-loaded index).

**Global CLAUDE.md:**
- Never kill a process by image name; kill only PIDs you started.
- Browser automation gets its own throwaway profile, never his real Chrome profile.
- When attaching to a browser you did not start, close the page, never the browser.

**Hooks:**

| Hook | Fires on | Blocks | Born from |
|---|---|---|---|
| `chrome-guard.py` (user level) | Every Bash/PowerShell call, and any script it runs | Killing chrome by name in any shell form | 2026-09-15: two `taskkill /IM chrome.exe` closed his whole browser; four more on 08-29 |
| `flashcut-root-guard.py` (user level) | SessionStart and every Edit/Write | Nothing here: it wraps a guard from **another project** whose file is absent on this PC, so it lets everything through | — |
| `clippershq/pipguard.py --hook` (repo) | Bash only (**not PowerShell**) | pip installs that downgrade numpy, torch, etc. | BL-681/682 numpy 2.0 near-misses (segfault at import) |
| accessibility-agents plugin | Prompts and UI-file edits | UI edits until the accessibility-lead agent has reviewed | Third-party plugin; recent UI rounds ran its reviews |
| Git hooks in `tools/githooks/` (only if `core.hooksPath` is set) | commit / push | Real addresses in staged files, a manifest before its code, paths claimed by another round | BL-1235 committed 3,972 addresses |
| **Stop hook** | — | **None exists.** The "stop hook" of BL-1598 is an app setting (Spotify stop-after-N), default off. | — |

**Standing rules, each with the incident that created it:**

| Rule | Incident |
|---|---|
| Kill only your own PIDs | 09-15: his whole browser killed twice |
| Never write to his Desktop; his files go to the operator home | BL-1587: 16 rounds wrote there; he deleted 4 ungraded pages |
| Read config only via `config_peek` | BL-1598 printed part of the LamaTok key; **the key is still not rotated** |
| This project never sends or asks him for pitches | BL-1446: rounds kept asking |
| Nothing downloads to Drive without a human YES; the review folder comes first | BL-1604/1605: 14,661 videos went straight to Drive without review |
| Scope = 5 niches **with positive evidence**; out of scope = `OUT_OF_SCOPE`, never NO or delete | BL-1606: Minecraft leaked in (1,827 of 3,746 review videos had no evidence) |
| Long or paid runs go through `run_detached` | BL-1600: a background chain was reaped by the host, losing about $8.75 of approved work |
| Liveness by `Get-Process -Id`, never `kill -0` | BL-1563: two walkers ran on one checkpoint; BL-1572: 1,079 duplicate paid calls ($0.75) |
| Pathspec commits only; never reset, clean or stash | 07-31: a failed `cd` plus `reset --hard` wiped 7 modules of uncommitted work |
| Commit every round before the session ends | BL-797's work was lost uncommitted; **BL-1619 is uncommitted right now** |
| Never read an exit code through a pipe | BL-901 pushed while its secret scan had FAILED (the third time) |
| Leak-scan everything written; no handles, emails, keys or username paths | BL-1235 committed 3,972 real addresses |
| Write files with the editor, not heredocs; never type `scratch\bl####` in a shell | `\b` becomes a backspace and corrupts paths (BL-1465; again in BL-1573 and BL-1602) |
| Tests must never touch production state | Happened 3 times before (phantom ledger rows, a test cap saved to the live config), and **a fourth time on 10-10** (BROKEN NOW #1) |
| Attribute spend from your own run counter or the vendor balance, never a `spend.json` before/after delta | The ledger is shared; BL-855 over-reported 2× |
| Don't spend the resource you are measuring | BL-1558: probes drained the quota under test |
| A sub-agent's number is a claim; re-derive it | BL-1559: 2 of 5 agents' headline numbers were wrong |
| A fix must be wired to a real call site and proven live | BL-1565: 0 of 36 construction sites used a shipped fix ("tenth instance") |
| Don't run the full suite while other rounds run it | Concurrent runs flip live-state tests; 5 rounds took 76 min for 14 min of work |
| His latest word wins; never ask him to do steps an agent can do; never make the reports repo history public-cleaned without his say | Several reversed briefs; BL-1590 |

## 6. Funnels

Row counts come from `master_leads.csv` (77,533 rows); prices come from the cited reports.

| Funnel → produces | Status | Last run | Delivered (total) | $ per 1,000 | Still enabled? |
|---|---|---|---|---|---|
| **Edit harvester / app** → viral edit videos + edit accounts | **ALIVE but BROKEN today** (the daily task points at a deleted folder) | 10-10 17:37 (run 38) | 24,202 videos downloaded all-time (14,661 of them pre-review, on the old Drive account); 3,604 YES accounts (almost all auto-approved, never human-checked); 163 videos YES'd by him or the friend through review | $0.51 per 1k good edits; $1.15 per 1k accounts (BL-1599); about $0.80 per 1k review videos (BL-1605) | Yes (`daily_on`, 07:00). Caps $3/run, $5/day, $60/month |
| **Niche editor emails** (football, tennis, big films and series) → editor emails | **ALIVE, nearly exhausted.** BL-1619 is still being closed out | 10-11 11:30 (crash-gap reconcile) | 216 editor rows (BL-1614/15/16/17/19) | $16 (BL-1614), $121 (BL-1617), **$19.9 (BL-1619)**; the next 1,000 would cost $30–65, and **700 is not reachable** inside his rules | Per-run CLI `--cap` (BL-1619: $15) |
| Any-niche editor / address walks → editor emails | Dormant | 09-23 | About 2,377 rows | About $15.9 per 1k delivered (BL-1583) | CLI cap |
| **TikTok clipper finder** → clipper leads | **Blocked** (lifetime cap) | 09-07 | 55,829 clipper rows; about 4.4k distinct emails in the workbook | $12.63 per 1k emails; $7.60 per 1k he wants (FACTS) | Config yes, effective $0 |
| **Spotify artists** → client leads | **Blocked** (lifetime cap); was the cheapest funnel | 10-03 | About 14,540 client rows (+1,000 emails in BL-1598) | **$1.20–1.25 per 1k emails** | Effective $0 |
| Meme pages → meme-page leads | Blocked | 09-06 | 1,909 | $6.7–7.6 per 1k wanted; $20.5 per 1k with an address | Effective $0 |
| Twitch / YouTube / Google Play → client leads | Dead | Jul–Aug | 269 / 49 / 27 | Not meaningfully priced | Effective $0 / cap 5 / no cap key |
| Repost accounts → client leads | Dead | 08-06 | 36 in master (445 in its export) | $1.90 per 1k addressed | Cap 2 |
| Clip pipeline / caption finder → rendered clips | Dead | 08-31 / 07-27 | About 210 rendered | About $0.002 per video | Caps 2 |
| Instagram crawl / follower scrape | Off | — | — | — | `false` |

## 7. Money

**Vendors.** Spend comes from `spend.json` rows, not its headers, because the headers still carry a ±$1.88 misbooking (BL-1573). The ledger is shared by every session.

| Vendor | For | Balance now | Last 30 days | All-time |
|---|---|---|---|---|
| **LamaTok** (TikTok API) | Edit app, editor walks, TikTok finders | **About $204** (340,445 requests at $0.0006; free balance read 10-10 evening, BL-1619) | $40.72 | $49.53 |
| **HikerAPI** (Instagram API) | Spotify contact lookups, Instagram bios | UNSURE (no recent local reading) | $9.46 | $55.24 |
| **OpenRouter** (vision judge) | Picture judging, clip labels | UNSURE (last read $4.81 in August) | $0.82 | $10.83 |
| **TikHub** | Deep checks, bio links | About $1.56 (BL-1616) | $0.01 | $0.71 |
| Free: YouTube Data API, Twitch Helix, MusicBrainz/ListenBrainz, Spotify pages | — | n/a | $0 | $0 |
| **Total** | | | **$51.04** | **$116.32** |

The 30 days by work: edit app $24.87 · September editor research $10.11 · Instagram research $8.21 · niche editor emails $5.75 · Spotify $1.25 · vision $0.82.

**Caps** (values via `config_peek`):

| Cap | Value | Binds? |
|---|---|---|
| `spend_cap_usd` (lifetime, all old finders) | 100 | **Yes, binding now** ($116.32 spent → every old finder gets $0). Proven by `test_bl1443_lifetime_cap.py`. |
| `ig_budget_usd` (lifetime, Instagram profiling) | 20 | Already exceeded; untested |
| `tiktok_max_run_usd` / `meme_finder_max_run_usd` | 0.5 / 0.5 | Tested (bl1443, bl1260) |
| `spotify_` / `twitch_` / `email_finder_max_run_usd` | 5 each | Tested (bl1601, bl1602, bl1567) |
| youtube 5, repost 2, caption 2, clip 2, `tikhub_max_usd_per_run` 1 | — | Partly tested; repost and tikhub have no test |
| **Edit app:** `cap_run_usd` / `cap_day_usd` / `cap_month_usd` | **3 / 5 / 60** | **Proven live** (runs ended "OK (cap reached)" at $2.99). October so far: $24.85 of $60. |
| Edit app balance guards | warn $5 / stop $1 | Tested (bl1600) |
| **Friends' runs** | **$5/day, all friends together** (default; the key is absent from the friend file) | Tested on a $0.01 run only |
| Editor walker `--cap` | Per run | Tested; never reached live |

**Trap:** a cap of 0 in some finders means "unlimited". They are safe only because `control.py` refuses first.

## 8. Automation

| Thing | Runs | Last result | Back after the power loss? |
|---|---|---|---|
| **ClippersHQ-EditsDaily** (07:00) | `edits\bin\edits_daily_task.bat` → `tools/edits.py daily`: auto-approve, harvest, snowball, $0.50 top-up | **10-11: FAILED** ("can't open file", exit 2) while the task shows 0x0. Earlier: 10-09 exit 3, 10-08 and 10-10 with no exit line (UNSURE why). | The task exists, but its target is broken |
| ClippersHQ-Backup (20:00) | Backup to `D:\ClippersHQ_vault\backups` | 10-10 OK | Yes |
| ClippersHQ-BackupPrune (04:30) | Prunes old backups | 10-11 OK | Yes |
| ClippersHQ-OutputsGC (04:45) | **Dry run only**; never applied | 10-11 OK | Yes |
| ClippersHQ-Job-bl1619-p2movies | A leftover one-off job (fires in 2036) | Its run died in the power loss | n/a |
| **App server** (ports 8793 app, 8794 friend listener) | HKCU Run → `tools/clippershq_open.py --no-window` at logon | Running since 22:52 | **Yes** |
| **Tailscale serve** (friend link, tailnet only) | tailscaled service (Automatic) | Up; serves 443 → 8794 | **Yes** |
| Google Drive for desktop | HKCU Run | Running | **Yes** |
| Old dashboard (8787) | Manual (`START_DASHBOARD.bat`) | **Not running** | n/a (not auto-start) |
| Old quick-tunnel share | Manual shortcut | Superseded by Tailscale | — |

## 9. Open state

**Live claims:**
- **BL-1619** is the only real one. Its claim is open and another session is closing it out today. Its code (the `user_by_handle` fix in `edits_vendor.py`, the bio-email hook in `tools/edits.py`, the new `edits_bioemails.py` and 2 tests) is **uncommitted**, and the live daily imports that untracked module.
- 13 stale claims (BL-1377, 1553–1562, 1597) still list as "in flight", and 2 claim files (BL-1583, BL-1612) are malformed.

**Decisions waiting for the owner:**

| # | Decision | Source |
|---|---|---|
| 1 | **Rotate the LamaTok key** (about $204 balance exposed; the same key is in the package) | BL-1609, BL-1612 |
| 2 | **The $100 lifetime cap:** raise or reset it, or leave the old finders off (Spotify at $1.25/1k is behind it) | this briefing |
| 3 | **Editor emails:** 700 is not reachable in the 3 niches. Widen (any-niche pro-tool editors at $4.84/1k, 40/40 real; or anime / K-drama / TV), walk 140 more series tags at about $31/1k, or stop | BL-1616, 1617, 1619 |
| 4 | **Danilo's skip list:** partial list, split seeds, or hashed handles | BL-1596 |
| 5 | **90-day item rule:** saves about 65% of account-discovery money and loses about half the new accounts | BL-1609 |
| 6 | **Auto-approved accounts:** 3,539 auto YES that he has never seen | BL-1609, daily log |
| 7 | Measure the real Drive quota; what to do with the old Drive account's 14,661 pre-review videos | BL-1609, 1611 |
| 8 | Delete `D:\ClippersHQ_portable` himself (agents are blocked) | BL-1618 |
| 9 | Tailscale: send the friend a proper invite and revoke the reusable link | BL-1618 |
| 10 | Commit BL-1619 (left uncommitted because he had not asked) | BL-1619 |

**Top 10 open items:**

| # | Item | Evidence |
|---|---|---|
| 1 | Repair the daily `.bat`, the 2 shortcuts, and `edits_me_first_start.py --help`; then make `test_tools_tracked` never run a tool that acts | `daily.log`; `.bat` and shortcut targets; `tests/test_tools_tracked.py:466` |
| 2 | Finish and commit BL-1619 (in progress elsewhere) | `git status`; `.claims/BL-1619.json` |
| 3 | Rotate the key | BL-1609 §5.1 |
| 4 | Lifetime-cap decision | `spend.json` $116.32 vs 100 |
| 5 | Drive guard reads C:'s size, so the quota is unknown and the 2 TB switch can never fire | BL-1609 §5.2 |
| 6 | Review backlog: about 3,800 videos waiting, 681 expired; nothing pauses paid runs while the queue is full | `edits.db`; BL-1609 §5.3 |
| 7 | The `edits.db` archive never runs (about 600 MB, over its 500 MB trigger; it refuses on "another run holds the lock") | `daily.log` 10-08/09 |
| 8 | 7 suite reds new since 09-21 with no recorded cause (bl1307, bl1413, bl1432, bl1443, bl1461, no_unchecked_stdout, scratch_gc) | `scratch/bl1620/logs/reds.txt` |
| 9 | Publish the 6 unpublished reports; BL-1618 needs a report | reports clone vs `reports/` |
| 10 | Claims registry cleanup; the leftover bl1619 scheduled task | `.claims/` |

**Suite:** BL-1620's run was **37 red of 563**:
- 25 were already red on 09-21.
- 1 environment, 1 data.
- 3 come from the edit app's download pause (bl1599, bl1604, bl1602).
- 7 are new with no recorded cause.

**Known bugs:**
- The daily-task breakage above.
- The scheduled task reports 0 even when the run fails.
- `claims_read.py` calls a malformed claim "being written right now".
- Detached jobs starve at below-normal priority.
- The 10-10 daily log has no RESULT line while the DB says OK (UNSURE).

**Never tested end to end:**
- Installing on another PC, or the Drive transfer (simulated on this PC only).
- Drive full or quota behaviour.
- A friend's final YES/NO on real videos (a final NO deletes the file; synthetic tests only).
- The friend $5/day cap under real spend.
- Auto-start and Tailscale serve across a deliberate reboot (last night's power loss is the first real evidence: **they came back**).
- BL-1619's bio-email hook in a real daily.
- The pasted-link resolver against the live vendor.
- Auto-approve accuracy.
- The 90-day rule (forecast only).

## 10. How to prompt me

| | |
|---|---|
| **Helped** | One goal with a number (BL-1619: "700 editors"). A **hard $ cap** plus a **stop rule** ("drop any source over $30 per 1,000 kept"): BL-1619 stopped itself at $1.39 of $15. "Free first, paid last." "Counts only." An explicit list of what must NOT be written (master, MARK, workbook). Naming the output file and its folder. "Read-only, $0" for audits. Asking for an answer card first. |
| **Hurt** | **A second task sent into a session mid-run:** BL-1620 was pasted into BL-1619's session at 15:01, BL-1619 stalled with nothing delivered, and its paid tail then died in the power loss. **Eight-phase rounds:** BL-1596 ran out of time before Phase 7. **Build + live test + review + caps in one round:** BL-1620's own suite run broke the daily task, and nobody saw it because the round was already wide. **Facts in the brief stated as given:** 114 of 468 reports correct something the brief asserted (stale counts, "run alone" while others were live). **Restating rules in new words each time:** the same rule written two ways reads as two rules. |
| **Rules I break most** | 1. Shell shortcuts: heredocs and `python -c` writes, typed `\b` paths (BL-1596, 1602, 1573). It happens because they are faster, and the editor rule is easy to forget mid-task. 2. **Printing identifiers in tool output while probing** (BL-1619 printed 2 handles; BL-1598 printed part of the key). It happens when debugging a vendor shape. 3. **Leaving work uncommitted or claims open** (BL-1619 now; BL-1596's stale `started_epoch`), because the round ends on the report, not the commit. 4. **Running narrower tests than the change touches** (BL-1596 left `test_config_contract` red). 5. Restarting after a false "killed" notice, which caused duplicate spend (BL-1572). |
| **Right scope for one round** | **One deliverable, one money cap, at most 3 phases, about 4–6 hours.** Keep paid runs separate from code changes, and audits separate from builds. A UI change should include its own a11y review and nothing else. If a fix touches his live setup (tasks, shortcuts, Drive), make that the whole round. |
| **When to start a fresh session** | For **every new BL round**. After a power loss or crash (re-read PROGRESS.md). When the context has been compacted once (specs get lost). **Never** send a new round into a session that has a paid run going; let the paid run go detached and close the session. |
| **Write prompts like this** | Goal + number · cap + stop rule · what must not be touched · where the output goes · "report: card, then the eight sections" · "UNSURE if not measured". Point at earlier reports by BL id; I read them. Skip restating the standing rules: they are in memory and docs, and a restatement that differs creates a conflict. |

## 11. Questions for the strategist and the owner

1. **What happens to an approved video after Drive** (repost on his pages, sell to clients, give to editors)? It decides what "good" means for the harvester.
2. **The $100 lifetime cap is spent.** Raise it, reset it, or keep the old finders off? Spotify clients at $1.25 per 1,000 are behind it.
3. **Editor emails:** is 700 still the goal? If yes, which widening: any-niche pro-tool editors ($4.84/1k), anime / K-drama / TV, or over $30/1k?
4. **Next round = repair the daily task, the shortcuts and the test that broke them?** I recommend it first: one small round, no spend.
5. **When will the key be rotated?** I can prepare everything except the vendor-side click.
6. **Danilo:** which skip-list option, and is Danilo's copy of the code current?
7. **Auto-approved accounts** (about 3,500, never seen by a human): keep auto-approve on, sample-audit it, or switch it off?
8. **The 90-day item rule:** yes or no?
9. **Reports:** should every round's report be published even when the session moves on (6 are not)? Do you need a report for BL-1618?
10. **One session per round from now on?** And should a paid run always be detached, with the session closed, before a new task is sent?

## Round notes (eight-section essentials)

- **Asked:** a full briefing for a new strategist; read-only, $0.
- **Shipped:** this report only. **Nothing was changed** on the machine or in the repo, beyond writing this report file into `reports/`. No claim file was started, because the brief said read-only. The id was checked free locally, in `.claims/` and on the remote.
- **Measured by:** me plus four read-only helper agents (machines, money, open state, rules). I re-derived the load-bearing facts myself: the broken `.bat` and its log line, the tool that ignores `--help`, the marker time 18:22:47, the cap values, the $116.32 / $51.04 ledger sums, disks, RAM, boot time, BL-1619's activity today, and the unpublished-report list.
- **What I got wrong:** an early working note said the code repo was 1,690 commits unpushed. That was against `main`; against its own upstream branch it is **835**.
- **Money and stores:** $0. No vendor call. `edits.db` and `master_leads.csv` were opened read-only (the leak scan only).
- **Leak scan:** the secret scan runs inside `publish_report.py`; the two-corpus scan was run on this file before publishing (result in the commit message).
- **Next:** see §11, question 4.
- **Paths:** `reports/BL-1621-briefing-for-the-strategist.md`; evidence paths are cited inline.
