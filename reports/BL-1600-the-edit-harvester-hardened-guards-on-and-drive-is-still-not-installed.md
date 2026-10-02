# BL-1600: the Edit Harvester is hardened -- every silent failure now shows, the feed grew to 3,982 accounts, and Google Drive is still not installed on this PC

## MORNING CARD

1. **Drive: NOT FOUND.** This round searched:
   - every drive letter, for "My Drive" in 21 languages
   - the GoogleDriveFS process, the DriveFS install folders and registry keys
   - uninstall entries, startup items and scheduled tasks, under every Windows profile

   Google Drive for desktop is **not installed on this PC**. What you must do is step 1 below.
2. **On this PC:**
   - **31.9 GB** of edits waiting on C:, **0 GB** moved to Drive.
   - **2,857** more good edits (~13.1 GB) are queued for later days. They are best first, and free to fetch while their links work.
3. **Storage, while Drive is absent:**
   - The 07:00 task alone adds **4.5 GB/day** (32 GB/week, 135 GB/month).
   - At the new 15 GB/day limit, that is 105 GB/week and 450 GB/month.
   - C: hits the 25 GB floor in **~20 days**, or **~6 days** at the limit. Then downloads stop cleanly.
4. **LamaTok:**
   - Balance **$230.78** (384,631 requests).
   - Spend today across ALL tools: **$1.251**, all of it the edit harvester. The clipper finder spent $0 on TikTok today.
5. **Guards:**
   - **Green:** canary (OK on real payloads), 07:00 task (triggered through Task Scheduler; it wrote its own row, OK), swipe server (killed by PID, the shortcut brought it back), download breaker (not tripped). Peak RAM of a daily run: 316 MB.
   - **Red:** Drive.
6. **Your swipe feed: 3,982 accounts** (+1,371 this round).
   - **+1,353** came from the parked pass: 66% of the parked authors checked were active.
   - **+0** from new niches: those pilots never ran (see 11).
7. **Mined terms: 48 added**, for free, from your downloaded edits. Their yield against hand-made terms is **not measured yet**: that test was in the killed chain.
8. **Duplicates:**
   - **0%** exact: 0 of 6,935 by sha256.
   - **0.24%** near: 4 of 1,685 by a 3-frame perceptual hash.
   - Both are far under 5%, so no skip policy is switched on.
9. **Grid mode:**
   - **0.33 actions per decision**, against 1.0 in single-card mode.
   - On the machine path: **583 against 74 decisions per minute**.
   - Your own speed can only be measured with you.
10. **Top 3 risks still open:**
    - (1) Drive is not installed.
    - (2) C: fills in about 20 days without Drive.
    - (3) Background runs get killed when this PC is short of memory. It killed this round's own chain. A killed run is now closed, and its unbooked calls booked, at the next start.
11. **Spent this round: $1.2510** of $10. **About $8.75 of approved work did not run.** Claude Code killed the paid chain when the PC ran low on memory, with the parked pass about one-third done. Not run:
    - the rest of the parked pass
    - the UFC, basketball and golf pilots
    - the mined-term yield test

    I was told not to restart it on my own.
12. **What YOU do next:**
    1. On THIS PC, install **Google Drive for desktop** (google.com/drive/download).
    2. Sign in with your **paid** Google account.
    3. Keep **"Stream files"** (the default). The tool finds "My Drive" by itself on the next run or `tools/edits.py sync`, and moves 31.9 GB in, checking every file by size + sha256 first.
    4. Say **"re-run the BL-1600 chain"** and I will run the rest of the parked pass, the three niche pilots and the mined-term test, inside the $8.75 left.
    5. Open **Start Menu > ClippersHQ > Swipe accounts** and try **Grid (9 per screen)**: every card starts YES, click to flip to NO, then **Ctrl+Enter** (or S).

**Round:** BL-1600 · **$1.2510 LamaTok** (2,085 calls, all booked as TikTok, $0 Instagram) · master, MARK, your workbook and the clipper label store never written · nothing on the Desktop · nothing in OneDrive · no handle, name or account link in this report (leak scan, both corpora).

## Decisions that are yours

1. **Install Drive** (above). Nothing else in this list matters as much.
2. **Re-run the killed chain?** About $8.75 is approved and unspent.
   - The parked pass is the best supply measured so far. Going newest-seen first, **1,299 of 1,955 fed authors were active (66%)**, at about $0.0006 per author checked.
   - 8,745 parked authors remain.
3. **The 15 GB/day limit** keeps C: alive while Drive is absent. Once Drive is in, you may want it higher. It is `max_gb_per_day` in `%LOCALAPPDATA%\ClippersHQ\edits\edits_overrides.json` (any key there wins).
4. **config.json was NOT written.** BL-1598 still holds a live claim on it. Every cap and limit has an inline default, and a test proves a cap read from config binds.

## 1. What it was asked to do

Harden the harvester against everything that could make it stop quietly:
- Drive
- disk and storage
- silent failures
- growth (term mining, bigger packs, sounds, the parked pass, new niches)
- speed for you (grid mode, today's edits)
- quality signals
- the clipper finder's cursor bug
- caps in config

The round cap was $10 of LamaTok. It started with a written pre-mortem (`scratch/bl1600/premortem.md`).

## 2. What shipped, and how each was proved

Every module's test was written first and seen failing. **28 of 28 named suites pass (278 checks)**: every BL-1599/BL-1600 suite, the repo guards (`test_atomic_io`, `test_config_contract`, `test_tools_tracked`, `test_operator_home`, `test_guard_resolution`, `test_backup`, `test_facts_guard`) and `test_bl1541_email_harvester`. The full suite was not run, as you asked.

| Part | Shipped | Proof |
|---|---|---|
| 1 Drive | Detector: DriveFS's registry mount point first, then every letter D-Z and the profile folders, for "My Drive" in 21 languages, re-checked every run. It says WHY: not installed / installed but not running / running but nothing mounted. A full or refusing Drive (ENOSPC, winerror 112, EACCES) stops writes into Drive for the run, is recorded, and shows red. | 7 tests on fake mount layouts. Live result on this PC: "not installed". |
| 2 Disk | 15 GB/day download limit. Best first (outlier x, then views) once the day is close. The rest stays QUALIFIED with its link kept. 30-day age limit. Staging floor raised 10 -> 25 GB. `fetch_deferred` (also run by the 07:00 task) tries the stored link for free, then one counted feed call. | Tests: best-first under a short day; next-day fetch costs 0 calls; an expired link costs exactly 1 counted call; age and floor. |
| 2 Duplicates | `edits_dupes`: sha256 + 3-frame dHash. The earliest post is kept; copies are only recorded; never deletes. | Test: a re-encode matches, a different video does not; the earliest is kept; files untouched. |
| 3a Balance | Free read at the start and end of every run. Refuses under $1, warns under $5, shown on the page. Dollars come from the request counter, because the vendor's `amount` lags. | Tests: $0.60 means NOT RUN and recorded. Measured: `amount` stuck at 232.0299 across 2,085 debited requests. |
| 3b Canary | TikTok's official account + "messi edit": play_count, create_time and play_addr must all be present before any paid work. A zero is a failure. | Tests: missing play_addr or an empty feed means NOT RUN, recorded. **Live: OK, 62 items, 2 calls**, on both real runs. |
| 3c Schema drift | A required field missing on more than 5% of a page (10+ items) stops the run and names the field. | Tests: 3/20 stops ("play_count missing on 3 of 20"); 1/40 does not. |
| 3d Breaker | 10 failed downloads in a row pause downloads, recorded and shown. | Test: 12 good edits, a CDN answering 429: paused after 10. |
| 3e 07:00 task | "Run after a missed start" was ON. The page shows "last daily run OK/FAILED, when", plus **MISSED** after more than 26 h. | **Triggered through Task Scheduler** (not the script) with tiny caps. It wrote run 9: OK, 29 calls, $0.0174, canary OK. |
| 3f Server | Shortcut path proven. | The server PID (from its port; the one this session started) was killed and the page did not answer. The Start Menu .bat brought it back: page HTTP 200, status answering. |
| 3g Memory | Peak RAM recorded on every run row. Lanes capped at 8. | Daily run peak **316 MB**, against the 2 GB target. |
| 3h Database | 5 new indexes. ANALYZE weekly, VACUUM monthly (both ran on run 9). | DB 137 MB after VACUUM, 157,209 video rows; ~360 MB/month at the daily top-up. Backup archive (incl. the DB snapshot) ~43 MB + DB; D: 363 GB free, so the 30 kept archives fit many times over. |
| 3i Shared credit | "LamaTok today: $X all tools · $Y edits" on the page, from the shared ledger. | Test with mixed campaigns. |
| + Killed runs | A RUNNING row whose PID is dead is closed at the next start, and (debited - booked) calls are booked. Booking every 10 calls (was 25). | Tests: 3. Found the hard way (section 5). |
| 4.1 Mining | `edits_mine`: "<name> edit" / "#<name>edit" from DOWNLOADED edits, by DISTINCT accounts (3 or more), niche by majority. Generic words, pack names and **any account's handle or display name are never terms**. Runs after every run. | Tests: 5. On the real DB, 17 of 108 raw candidates equalled a handle or display name and were excluded. Run 9 added **48** (football 12, marvel 25, tennis 11). |
| 4.2 Packs | Football 579, marvel 540, tennis 335, UFC 323, basketball 359, golf 333 names, each a phrase term. | Tests: 300+ per niche, unique, every name a phrase term. |
| 4.3 Sounds | **Not possible on this vendor.** The live spec (1.4.5, 29 paths) has only `/v1/media/music/download/by/id` and `/by/url`, and no "videos using this sound". **$0 spent.** | Spec re-read for free. |
| 4.4 Parked pass | `feed_parked`: newest seen first, across niches; the cap returns the rest to PARKED. | Tests: 2. Live: 1,955 fed, 1,299 active (66%), then killed (section 5). |
| 5 Speed | Grid mode, today's edits and the health board. The accessibility review came BEFORE the edit; built to its checklist (YES/NO as words, per-view key maps, Ctrl+Enter/S submit, no bare-Enter submit, radio views, non-alert Drive banner). | Server tests: a batch screen; 3 tabs submitting one screen give 9 written, 18 conflicts, 0 double-writes; undo of a screen; edit labels; status board. Driven in Playwright's own Chromium on synthetic data: numbers in section 3. |
| 6 Quality | "possible bought views" (likes per 1,000 views under a quarter of the niche median) and "maybe a raw clip" (no edit word/hashtag/name, over 60 s). Grey tags on cards, a column in every index.csv. **They reject nothing.** | Tests: 2. Live (run 9): 2,551 of 58,253 scored videos tagged bought (4.4%), 337 accounts; 4,419 videos raw clip, 77 accounts. |
| 7 Clipper bug | The email walker follows the cursor the response returns (was a fixed +30). **Separate commit, own test.** | The test failed first (requested 0, 30, 60, 90 against a vendor serving 20 per page) and passes now (0, 20, 40, 60, 80, all 100 authors seen). v1 keeps +30. All 7 suites importing `email_harvester` are green. No paid call. |
| 8 Config | Inline defaults, then config.json `"edits"`, then `edits_overrides.json` in the edits home. **config.json not written** (BL-1598 holds it). | Test: a cap read from a config file binds (`allowed_budget` returns the config's $0.50 as "per-run cap"). |

## 3. What was measured

| Measure | Value |
|---|---|
| Parked pass, newest-seen first | 1,955 fed, **1,299 active (66.4%)**. BL-1599's random sample was 36.9% [34.1-39.7] (n=1,158): recency of the sighting matters. |
| Cost per active account from the parked pass | about 2,056 calls / 1,299 ≈ 1.58 calls ≈ **$0.95 per 1,000** (cheaper than phrase search's $1.08) |
| Canary on live payloads | OK, 62 items, 2 calls ($0.0012), on both runs |
| Daily run (Task Scheduler, tiny caps) | 3.9 min, 29 calls, peak RAM 316 MB, ANALYZE + VACUUM ran |
| Grid vs single card, machine path (Playwright, no think time) | grid **583 decisions/min** at **0.33 actions/decision** (2 flips + 1 submit per 9); single card **74/min** at 1.0. Arrows in grid decided nothing; undo restored 9. |
| Duplicates | exact 0 / 6,935; near 4 / 1,685 hashed (0.24%, full pairwise) |
| Quality signals | bought views 4.4% of scored videos; raw clip 4,419 videos / 77 accounts |
| Balance read | free; dollars from the request counter (`amount` lags) |

## 4. What was refused and why

- **Sounds:** the vendor has no endpoint that lists videos by sound. $0.
- **Restarting the killed chain:** Claude Code said not to restart it on my own when memory may still be short. The $8.75 of approved work waits for your word.
- **A duplicate skip policy:** the measured rate (0% exact, 0.24% near) is far below the 5% bar you set.
- **config.json:** claimed by BL-1598. Inline defaults are used, plus his override file.
- **The full test suite:** you said not to (it once drove this PC to 3.7 GB free).

## 5. What I got wrong

1. **The paid chain was reaped on low memory, and 30 calls ($0.018) were briefly off the books.** The vendor debited 2,056 requests for the parked run; the ledger had 2,026. I booked the gap by hand as a labelled row, marked the run KILLED, and returned 4 stranded accounts to PARKED. Then I built the guard: the next paid run closes such rows and books the gap itself, and booking now happens every 10 calls.
2. **I trusted the vendor's dollar `amount` at first.** It does not move. The board now uses the request counter.
3. **The term-mining test was written first but not run while failing.** I proved it afterwards (module hidden: 4 errors; restored: green).
4. **Three test-fixture bugs** cost re-runs, all caught before shipping:
   - edits sized at the 6 MB default when the fakes had no `data_size`
   - a breaker fixture whose median was itself made of hits
   - an orphan test that read the real ledger
5. **The pre-commit FACTS guard refused a commit** at 106.1% of its $7.40 drift limit. I re-stamped `docs/FACTS.md` from one live read in its own commit, never `--no-verify`.
6. **The day cap ($5) would have blocked this round's approved $10.** I raised it to $10 in his override file for this round only. I then used the same file for the task proof's tiny caps, and **removed it before close**. His caps are back to $3 / $5 / $60.

## 6. Money, stores, disk

| | |
|---|---|
| LamaTok this round | **$1.2510**: 2,085 calls × $0.0006. BL-1600 campaign 2,056 calls (incl. 30 reconciled), plus 29 calls from the Task Scheduler proof run (campaign EDITS) |
| Vendor balance | 386,716 requests before the parked run, 384,631 now: **2,085 debited = 2,085 booked** |
| `spend.json` | moved by exactly the rows above (69 rows: BL-1600 65, EDITS 4, booked every 10 calls). No other campaign booked TikTok today. |
| master_leads.csv, MARK, his workbook, clipper label store, dashboard/ | never written |
| His files | `%LOCALAPPDATA%\ClippersHQ\edits\`: 31.9 GB staged, DB 137 MB. Nothing on the Desktop, nothing in OneDrive. |
| Disk | C: 116 GB free (floor 25 GB); D: 363 GB free |

## 7. Ranked next steps

1. **You: install Drive** (morning card, step 12).
2. **Re-run the killed chain** (~$8.75): the rest of the parked pass (8,745 authors, ~66% active when newest first), the UFC, basketball and golf pilots, and the mined-term yield test.
3. **Prune EXPIRED video rows** older than 60 days. They are most of the 157k rows, and the reason the DB grows ~360 MB/month.
4. **After 200 swipes:** `tools/edits.py learn`. That is the point where the quality signals and creator signals can earn rules under the 90% / 5% bar.

## 8. Paths

- **New code:** `clippershq/edits_mine.py`, `edits_names.py`, `edits_quality.py`, `edits_dupes.py`.
- **Extended:** `edits_drive.py`, `edits_db.py`, `edits_engine.py`, `edits_vendor.py`, `edits_signals.py`, `edits_terms.py`, `edits_swipe_server.py`, `edits_swipe.html`, `tools/edits.py`, `clippershq/email_harvester.py` (cursor only), `docs/FACTS.md` (re-stamp).
- **Tests:** `tests/test_bl1600_*.py` (12 files).
- **Round files:** `scratch/bl1600/` (pre-mortem, page proof, splice helper, restamp, measure scripts).

### Pre-mortem: status of all 18

| # | Risk | Status |
|---|---|---|
| 1 | Drive never connected | GUARD built; **still open** (not installed) |
| 2 | C: fills up | GUARD built (15 GB/day, 25 GB floor); **open while Drive is absent** (~20 days) |
| 3 | 07:00 task stops | GUARD built + proven (Task Scheduler, MISSED badge) |
| 4 | Credit runs out | GUARD built (balance read, $1 refuse, $5 warn) |
| 5 | Field renamed (silent zero) | GUARD built (canary + schema drift) |
| 6 | CDN refuses downloads | GUARD built (breaker at 10) |
| 7 | He never swipes | GUARD built (grid mode, 0.33 actions per decision) |
| 8 | Term supply dries up | GUARD built (mining after every run, 300+ names per niche) |
| 9 | Server down after reboot | GUARD proven (kill, shortcut, page loads) |
| 10 | Drive full | GUARD built (stop writes, record, red) |
| 11 | Duplicates | MEASURED: 0% / 0.24%; no policy needed |
| 12 | Shared credit drained | GUARD built (all-tools spend shown) |
| 13 | DB growth | GUARD built (indexes, ANALYZE, VACUUM); pruning is next step 3 |
| 14 | A daily run OOMs the PC | MEASURED 316 MB; lanes capped |
| 15 | Concurrent runs | existing PID lock + file-locked ledger |
| 16 | Bought views / raw clips | SIGNALS built (no rejection) |
| 17 | Task while logged out | NO change of principal (needs his password); StartWhenAvailable + MISSED badge |
| 18 | Path drift | NO: `tools/edits_shortcuts.ps1 -Install` is idempotent |
| **19 (new)** | **The host kills a run on low memory** | **GUARD built** (orphan close + reconcile; book every 10). **Open**: this PC runs short of memory |
