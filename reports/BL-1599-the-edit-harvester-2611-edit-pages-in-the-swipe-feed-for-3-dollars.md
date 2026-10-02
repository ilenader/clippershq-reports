# BL-1599: the Edit Harvester is built -- 2,611 active edit pages are in your swipe feed and 5,842 good edits are downloaded, for $2.99

## MORNING CARD

1. **Accounts in your swipe feed now: 2,611** (target 2,000). Football 1,200, Marvel 1,057, Tennis 354. 2,578 of them show 4+ thumbnails.
2. **Good edits downloaded: 5,842 (26.94 GB). Google Drive is NOT OK:** Google Drive for desktop is not installed on this PC (no G:, no DriveFS). Every edit waits in `%LOCALAPPDATA%\ClippersHQ\edits\staging\ClippersHQ Edits\<Niche>\<date>\`. The moment Drive appears, the next run (or `tools/edits.py sync`) moves them in, each verified by size + sha256 first.
3. **Money:**
   - **Spent today: $2.9934 of the $5.00 cap.**
   - **$1.15 per 1,000 accounts** found for the feed.
   - **$0.51 per 1,000 good edits.**
4. **Time:** **0.69 hours per 1,000 accounts** (107.6 min of runs in total).
5. **Best per dollar:**
   - **Niche:** Marvel ($1.03 per 1,000 accounts), then Football ($1.06), then Tennis ($1.76).
   - **Term type:** **phrase search "<name> edit"**, at **$1.08 per 1,000**. The name hashtag feed costs $2.37 and suggested-accounts snowball $4.70.
6. **Rejected automatically today:**
   - inactive **1,101**
   - official **347**
   - photo **93**
   - blocklist **0** (no NO yet)
   - not yet judged: **10,757 parked** (only an old post seen) and **8 unreachable**
7. **Start Menu > ClippersHQ > Swipe accounts: WORKS.** The server is running and the page was driven for real (keys, undo, touch, server-down). Arrows/A/D to decide, Down to skip, Z to undo.
8. **Next build:** 300+ more names per niche, plus a parked pass. Phrase terms run dry after about 7 pages, and Tennis is already spent. The 10,757 parked authors are active 36.9% of the time, which works out to about $1.63 per 1,000 accounts.

**Round:** BL-1599 · **$2.9934 LamaTok** (4,989 calls, all booked as TikTok; $0.00 Instagram) · master, MARK, your workbook and the clipper label store never written · nothing on the Desktop · nothing in OneDrive · no handle, name or account link anywhere in this report (leak scan 0 hits, both corpora).

## Decisions that are yours

1. **Install Google Drive for desktop and sign in.** I cannot do this: it needs your account, and you gave me none. After that nothing else is needed; the tool finds `My Drive` by itself.
2. **The 07:00 task is installed** (ClippersHQ-EditsDaily, first run tomorrow).
   - It harvests your YES accounts, snowballs new YES accounts, and spends a **$0.50** discovery top-up.
   - It is capped at $3 per run, $5 per day and $60 per month.
   - Until you swipe YES on something, it only does the top-up.
   - Change the caps with an `"edits"` block in config.json (keys in the code). Nothing was written to config.json tonight.
3. **Feed the parked pool?** 10,757 authors were seen only through an old post. 36.9% [34.1–39.7] of a 1,158-account sample were active, so about 3,970 more accounts would cost about $6.45. Tonight's runs did not spend it.
4. **Downloads from INACTIVE accounts:** 175 of the 5,842 edits came from accounts that post too slowly to reach your feed. That is your rule ("every good edit found"). Say if you would rather skip them.
5. **Snowball is the weakest source today.** 258 of 300 suggested accounts were already known, and most of the new ones were inactive. It stays on for your YES accounts, as you asked, and gets re-measured once seeds are real YES swipes.

## 1. What it was asked to do

Build the Edit Harvester inside Clipper Finder.
- **Discovery:** find TikTok edit pages by niche (football, marvel, tennis first; then UFC, basketball, golf) and keep only ACTIVE ones (last post ≤ 7 d and ≥ 4 posts in 30 d).
- **Free filters, before any per-account call:** reject photo pages and official accounts for free, and check NO forever before any paid call.
- **Good edits:** download every GOOD EDIT (≥ 20k views and ≥ 2× the account's normal views, judged at ≥ 3 days, watched for 30 days) into Google Drive.
- **Swipe feed:** a one-card swipe page that writes every decision to one database.
- **Creator signals:** order the feed now; once you have swiped 200, learn creator rules (switched on only at ≥ 90% of NO caught and ≤ 5% of YES lost, held out).
- **Harvest:** keep harvesting YES accounts daily.
- **Limits:** $5.00 hard cap, no handle outside your private files.

## 2. What shipped, and how each was proved

Each module had its test file written first and seen failing on import. Nine suites, all green: signals 24 · db 14 · terms 7 · drive 12 · engine 19 · swipe 10 · learn 5 · backup 3 · cli 4 checks.

| Shipped | Proof |
|---|---|
| `edits_db` (SQLite, WAL): accounts, videos, decisions, terms, runs, blocklist, rules, snowball | **Two writers cannot double-write.** 8 concurrent POSTs on one card give exactly 1 decision and 7 × HTTP 409. **NO blocks** by secUid, uid and handle (a rename stays blocked). Undo restores and lifts the block. Paths in OneDrive or on the Desktop are refused. |
| `edits_signals`: parsing, active rule, good edit, photo, official, creator signals | Leave-one-out median, a 4-post minimum baseline, PENDING / EXPIRED / PHOTO states. Pinned posts and photos never set the normal. A missing view count is PENDING, never zero. |
| `edits_vendor`: the one door to LamaTok | Meters `client.http_requests`, so every billed attempt counts, retries included. The **hard cap holds under 8 lanes** because each call reserves its worst case before sending. Books `tt_calls` every 25 calls. **20 × 5xx in 10 min stops the run** (test: storm stops in under 30 requests, retires no term). |
| `edits_engine`: discover / snowball / harvest / refresh | Scripted fake-vendor tests: books reconcile, NO never re-bought, official/photo/old-post authors filtered free, resume never re-buys a page, term retired on yield, YES-only harvest, a PENDING post downloaded when it matures, silent accounts paused. |
| `edits_drive`: staging, `.part` writes, Drive | Each download is checked for an `ftyp` box. The staging copy is deleted only after the Drive copy re-hashes equal. Drive absent means the file stays and the run says so. Startup clears `*.part`. |
| `edits_swipe_server` + `edits_swipe.html` (127.0.0.1:8793) | Driven in Playwright's own Chromium (temp profile) on synthetic data: keys write to the DB; undo; held key = 1 decision; no decision while a dialog is open; touch tap reaches a tile; 390 px has no horizontal scroll; a dead server turns red and the page goes inert. Accessibility: reviewed **before** writing; the post-build review found 0 critical, 2 serious, 8 moderate, 10 minor, and all 20 were fixed. |
| `edits_learn` (Part F) | < 200 swipes learns nothing. A separating signal switches on (Wilson + denominators stored). A noisy one does not. A rule losing > 5% of YES switches OFF. |
| `tools/backup.py` | `edits.db` is snapshotted through sqlite's backup API. **Real restore:** 14,950 / 14,950 accounts, 101,766 videos, integrity `ok`. |
| `tools/edits.py`, `tools/edits_shortcuts.ps1` | Four Start Menu shortcuts plus the 07:00 task. The cap guards are tested: the smallest limit binds; a spent allowance means **NOT RUN, recorded**; a held lock means **REFUSED, recorded**. |
| Repo guard suites + full suite | `run_all.py -k` test_atomic_io, test_config_contract, test_tools_tracked, test_operator_home, test_guard_resolution, test_backup: **6/6 green, 88 checks**. The FULL suite was **stopped by Claude Code at 288 suites because the machine ran critically low on memory** (3.7 of 23.9 GB free); I did not restart it. Of those 288: 266 green, 22 red. **None of the 22 is a BL-1599 suite**, 20 never mention a file this round changed, and the 2 that match by text do so coincidentally (`_edits_mode`, `acog.hitbox.backup`). The 6 I re-ran in a clean extract of the PRE-ROUND commit 74148c72 fail there too. The suite run moved no store: master, config, all five seen stores and config.backups were byte-identical; the 59 ledger rows added during it are all SPOTIFY_FINDER (BL-1598's live run). |
| Part H | Every swipe is mirrored to `edits\swipe_labels.jsonl`, each line tagged `[SWIPE]` and regenerated from the DB (an undo removes its line). No clipper file is touched. **Overlap with master at close: 232 of 2,611 feed accounts (8.9%)** are already in master (75,522 TikTok handles there), and 1,220 of all 14,950 accounts seen. Mid-round the share was 68 of 1,189 (5.7%). |

## 3. What was measured

**Pilot, then two cheap experiments, then the plan changed.** All costs below include the feed calls of the accounts each source found.

| Source (this round) | Calls | $ | Accounts → feed | $ / 1,000 accounts | Good edits downloaded | $ / 1,000 edits |
|---|---|---|---|---|---|---|
| phrase "<name> edit" | 4,352 | 2.6112 | 2,423 | **1.08** | 5,454 | **0.48** |
| phrase "<name> 4k edit" | 288 | 0.1728 | 98 | 1.76 | 177 | 0.98 |
| phrase "<team> edit" | 114 | 0.0684 | 38 | 1.80 | 85 | 0.80 |
| hashtag "#<name>edit" | 182 | 0.1092 | 46 | 2.37 | 102 | 1.07 |
| suggested (snowball, 10 seeds) | 47 | 0.0282 | 6 | 4.70 | 24 | 1.17 |

**Why phrase search wins:** search surfaces RECENT posts, while the hashtag feed ranks old hits. 79% of the pilot's hashtag authors were parked as not recently seen.

**Parking is measured, not assumed.** A hash sample of parked authors was fed anyway:

| Group | Active | 95% interval | Sample |
|---|---|---|---|
| Parked sample | **36.9%** | 34.1–39.7 | n = 1,158 |
| Fresh authors | **84.7%** | 83.3–86.0 | n = 2,643 |

| Niche | $ | Accounts → feed | $ / 1,000 accounts | Edits downloaded | $ / 1,000 edits |
|---|---|---|---|---|---|
| Marvel | 1.0842 | 1,057 | 1.03 | 2,505 | 0.43 |
| Football | 1.2768 | 1,200 | 1.06 | 2,685 | 0.48 |
| Tennis | 0.6228 | 354 | 1.76 | 652 | 0.96 |

- **Tennis** ran dry: every tennis phrase term was exhausted at $0.63 of its $1.00, with more officials (players and tournaments) and more inactive accounts.
- **Funnel, all runs:**
  - 14,950 accounts new to the DB
  - 2,611 into the feed
  - 1,101 inactive
  - 347 official
  - 93 photo
  - 10,757 parked
  - 33 still waiting for their feed call (cap reached)
- **Downloads:** 5,842 edits from 1,603 accounts (5,667 from feed accounts, 175 from inactive ones). 1 download failed. 0 from official or photo accounts (a test pins this). Codecs on the pilot: 83 h264, 3 HEVC; `play_addr_h264` is now preferred.

**The books, four ways:**
- **Runs metered:** 4,984 calls in the run rows, plus 5 probe calls (4,989).
- **Ledger:** 200 rows under BL-1599 with 4,989 calls, $2.993400 TikTok, $0.000000 Instagram.
- **Vendor balance:** debited **4,991** requests. That is **2 more** than I metered (+1 on the football run, +1 on the tennis run, 0.04%). I cannot attribute them. The free balance read was measured as debiting nothing. The concurrent BL-1598 run booked $0 TikTok.

## 4. What was refused and why

- **No paid vision call and no face model.** Part F.3 is optional. cv2 here has no face-embedding model, and `face_recurrence` records that Haar measures presence, not identity. Not attempted.
- **No auto-reject of any kind on creator signals.** Day one, they only order the feed and show as grey tags. `learn()` refuses below 200 swipes.
- **No write to config.json.** BL-1598 holds a live claim on it. The caps are read with inline defaults.
- **No vendor download endpoint.** It costs $0.0006 per video; `play_addr` is free and already unwatermarked.
- **The email walker's +30 cursor stride was not changed.** The vendor's own cursor is +20, so it likely skips about 10 items per page. That is reported here for the clipper funnel, not fixed in this round.

## 5. What I got wrong

1. **I printed about 40 staged file names to my terminal.** The names carry handles. It happened in a shell loop checking codecs. The output went nowhere else: not committed, not reported, not published. Since then, staging and Drive paths are only touched through scripts that print counts.
2. **Two heredocs, against your rule.** One patched a scratch probe script. The other was an empty no-op. Every later edit used the Edit tool or a script file.
3. **The first commit lacked the Co-Authored-By/Session lines.** Not amended; all later commits carry them.
4. **I hashed master mid-round, not at round start.** It is byte-identical from then to close (`227cf1f5…`). My code has no write path to it; `overlap` only reads it. The proof is by code reading, not by a start-of-round hash.
5. **Adjudicating the last leak-scan hits, I printed four values from the database to my terminal.** They were three ordinary words from my own code and an official club's name. Each equals some account's display name, and each was already a word in my own code or test fixture. None is a handle. Nothing left the terminal.
6. **The CLI's tests came after the CLI**, not before as for every other module.
7. **Bugs my tests or the pilot caught before they cost anything:**
   - A vendor error on a hashtag-id lookup used to retire the term forever.
   - 234 of 234 thumbnails failed because the covers are HEIC.
   - A live tag's `has_more=0` ended it after 2 pages.
   - `daily` shut its download pool between modes.
   - A second meter on one client was blind to 5xx.
   - "$ today" lagged a running run.
   - Two serious accessibility issues: touch taps were swallowed, and dialog links had low contrast.

## 6. Money, stores, disk

| | |
|---|---|
| LamaTok this round | **$2.993400** (4,989 calls × $0.0006): probe 5, discover 4,880, refresh 37, snowball 47 |
| `spend.json` since round start | +387 rows: **200 BL-1599 ($2.993400)** and 187 SPOTIFY_FINDER ($0.583605, BL-1598's concurrent run) |
| master_leads.csv | never written by this round; sha `227cf1f5…` unchanged from mid-round to close |
| MARK, his workbook, clipper label store, dashboard/ | never opened for write |
| His files | `%LOCALAPPDATA%\ClippersHQ\edits\` (edits.db, staging 26.94 GB, thumbs, logs, bin) -- outside OneDrive, not on the Desktop |
| Disk | C: 127 GB free after the downloads; downloads stop below 10 GB free |
| Backup | `edits.db` (+ `[SWIPE]` labels) is now in the nightly archive; restore proven on the real DB |

## 7. Ranked next steps

1. **You: install Google Drive for desktop.** It unblocks 26.94 GB going to Drive, verified file by file.
2. **Grow the phrase supply.** Add 300+ more names per niche (squads, academy players, more characters), and fill UFC, basketball and golf. Phrase terms retire after about 7 pages, and that is where the $1.08 per 1,000 comes from.
3. **Parked pass**, if you say yes: about $1.63 per 1,000 accounts against the 36.9% active rate.
4. **After 200 swipes:** `tools/edits.py learn`. It reports catch-NO and lose-YES with Wilson intervals, and switches a rule on only past your 90% / 5% bar.
5. **Fix the email walker's cursor stride** (+30 against the vendor's +20), in the clipper funnel's own round.

## 8. Paths

- Code: `clippershq/edits_{db,signals,terms,vendor,engine,drive,learn,swipe_server}.py`, `clippershq/edits_swipe.html`, `tools/edits.py`, `tools/edits_shortcuts.ps1`, `tools/backup.py` (extended)
- Tests: `tests/test_bl1599_edits_{signals,db,terms,drive,engine,swipe,learn,backup,cli}.py`
- Round files: `scratch/bl1599/` (probe, page proof, leak scan, numbers script)
- His private files: `%LOCALAPPDATA%\ClippersHQ\edits\`; Start Menu > ClippersHQ

## Appendix (inside the eight sections above: the Part A study)

### REUSE MAP

| Piece | Status | What |
|---|---|---|
| `api_client.LamaTokClient` | **reused as-is** | auth header, retries (tenacity), 429/427/5xx mapping, `http_requests` = the billed count. The new meter reads that counter; nothing in the client changed. |
| `tiktok_finder._envelope_items`, `_next_page_id` | **reused as-is** | the payload unwrapper (nested-payload bug solved once) and search paging by `next_page_id` (BL-1469). |
| `email_harvester` walker lessons (+ `scratch/bl1584/walk.py`) | **reused as rules, not imported** | validate a page on its LIST, never its status; saturate on net-new ids; resume from a saved cursor and never re-pay; the depth wall at ~165 pages; book as you go; O_EXCL PID lock with a real liveness test. The tag ledger itself is NOT reused: it records tags walked for ADDRESSES; this tool keeps its own `terms` table so an email walk never blocks an edit walk or the reverse. |
| `editor_gate` | **reused as-is** | `bio_rule`, `name_rule`, `self_description` feed the creator signals (grey tags; they order the feed, reject nothing). `looks_agency` is about e-mail addresses and does not apply. |
| `creator_signals.self_narration_share` | **reused as-is** | first-person caption share, one more creator signal. |
| `main.record_aux_spend` | **reused as-is** | every billed request booked as `tt_calls` (never `ig_calls`) under the run's campaign. |
| `atomic_io`, `safe_name`, `proc_detach` | **reused as-is** | Windows-safe rename/remove, file-name sanitiser, detached swipe server. |
| `operator_home` lesson | **reused as a rule** | nothing on the Desktop; his files under `%LOCALAPPDATA%\ClippersHQ\` (here `edits\`), outside OneDrive. |
| `tools/backup.py` | **extended** | `edits_entries()`: a consistent snapshot of `edits.db` through sqlite's online-backup API + the `[SWIPE]` label file; restore proven by a test that recovers a row still sitting in the WAL. |
| `review_loop` lessons | **reused as rules** | nothing lives only in browser storage (every click is a server write); one page, one server, one database; a vocabulary-stable verdict word per click. |
| `free_judge` / `edits_rubric` | **noted, not used** | a paid vision judge exists; this build needed none (no paid vision call). |
| `face_recurrence` / face check | **not built** | cv2 here has no face model (face_recurrence's own note: Haar is presence, not identity; YuNet not bundled). Part F.3 is optional and was not attempted. |
| **NEW** | `clippershq/edits_db.py`, `edits_signals.py`, `edits_terms.py`, `edits_vendor.py`, `edits_engine.py`, `edits_drive.py`, `edits_learn.py`, `edits_swipe_server.py` + `edits_swipe.html`, `tools/edits.py`, `tools/edits_shortcuts.ps1` | each with its own `tests/test_bl1599_edits_*.py`, written first. |

### LAMATOK, MEASURED (5 probe calls, $0.0030, each bracketed by the FREE `/sys/balance` read)

A "call" is one HTTP request; every attempt (retries included) is billed. The balance read debits nothing (two reads, same counter). Unit **$0.0006** (`api.cost_per_call_usd`).

| Endpoint | Debited | Measured |
|---|---|---|
| `/v2/hashtag/medias?id=&count=30&cursor=` | 1 | **20 items per page** (`count` ignored); the response's own `cursor` is **20** -- a fixed +30 stride (as `email_harvester` steps) would skip ~10 items a page; `has_more` is not evidence (a live name tag said 0 on page 2) |
| `/v1/hashtag/info?hashtag=` | 1 | the challenge id; cached in `terms.hashtag_id` (and read from `cache_hashtags.json`) so it is paid once per tag |
| `/v2/user/medias/by/secUid?count=50` | 1 | **30 posts** (50 is accepted, 30 returned); a daily poster's 30 posts span ~71 days; `has_more` + `max_cursor` page further |
| `/v1/user/suggested/by/secUid` | 1 | **30 accounts** with `followerCount`, `videoCount`, `verified`, `signature`, `secUid`; no `next_page_id` on the probe |
| `/v2/search?keyword=&count=30&page_id=` | 1 per page | not probed separately (documented by BL-1469); measured in this round's runs: ~6-7 pages per keyword |
| `/v1/media/video/download/by/id?watermark=false` | **1** | returns `download_url` + `headers` (incl. a Cookie), url valid ~48 h -- **NOT NEEDED**: the feed item's own `video.play_addr` downloads over plain HTTP for **$0**, unwatermarked (its path equals `download_no_watermark_addr`; `download_addr` is the watermarked file and is never used) |

Fields on every feed item (free): `author.{unique_id, sec_uid, uid, nickname, signature, follower_count, aweme_count, verification_type, custom_verify, enterprise_verify_reason}`, `statistics.play_count` (+ likes/comments/shares), `create_time` (epoch s), `video.duration` (**milliseconds**), `text_extra[].hashtag_name`, `is_top` (pinned), **photo marker: `aweme_type == 150` and `image_post_info`** (1 of 30 on the probe feed). Covers: `cover.url_list` leads with **two `.heic` urls Chrome cannot render** (234/234 pilot thumbnails failed) and carries a `.jpeg` third -- the tool takes the first browser-readable url. Downloads: 83 of 86 pilot files h264, 3 HEVC; `play_addr_h264` is preferred when present. The CDN url states no expiry, so a video is fetched in the same run as its feed call.

### WHAT I BORROWED FROM OUTSIDE (ideas only; no code copied)

| Source | License | Borrowed |
|---|---|---|
| Overseer outlier benchmark write-up (overseeros.com) | article | **leave the scored post out of its own baseline** -- implemented as a leave-one-out median |
| Vamos "outlier score" (median, no score under 10 posts) / Eden (median of last 30 posts of the same type) | articles | median over the account's own recent posts, same type only (videos; photo posts and pins excluded), and a minimum baseline (4 other matured posts) before any verdict |
| faceless.so outlier finder | article | a young post's multiple is a floor -> his rule's PENDING state (< 3 days) |
| yt-dlp TikTok extractor | Unlicense | format ranking: `play_addr` first, watermarked `download_addr` never |
| Prodigy / SpaceML Swipe-Labeler | proprietary / no license | one card at a time, arrow keys, undo, best-first ordering -- ideas only |
| YuBen (MIT) | MIT | likes-per-1,000-views as a bought-views check -- **noted, not built** |

### TERM PACKS (publishable: famous names + edit words; no account anywhere)

Phrase terms go to `/v2/search`; hashtag terms go to `/v1/hashtag/info` and then `/v2/hashtag/medias`. Order is phrase first (measured, section 3). Walked = the terms this round actually paid for.

| Niche | Terms | by kind | Walked | Retired |
|---|---|---|---|---|
| football | 293 | phrase:name edit 66, phrase:team edit 28, phrase:name 4k edit 30, name+edit 66, generic 10, team+edit 27, name+edits 66 | 52 | 51 |
| marvel | 240 | phrase:name edit 62, phrase:team edit 9, phrase:name 4k edit 30, name+edit 62, generic 8, team+edit 8, name+edits 61 | 49 | 48 |
| tennis | 181 | phrase:name edit 43, phrase:team edit 8, phrase:name 4k edit 30, name+edit 43, generic 8, team+edit 6, name+edits 43 | 81 | 81 |
| ufc | 162 | phrase:name edit 38, phrase:team edit 6, phrase:name 4k edit 30, name+edit 38, generic 9, team+edit 3, name+edits 38 | 0 | 0 |
| basketball | 175 | phrase:name edit 38, phrase:team edit 12, phrase:name 4k edit 30, name+edit 38, generic 8, team+edit 11, name+edits 38 | 0 | 0 |
| golf | 150 | phrase:name edit 30, phrase:team edit 8, phrase:name 4k edit 30, name+edit 30, generic 6, team+edit 6, name+edits 30, name+4k 10 | 0 | 0 |

**Football** -- phrase: messi edit, ronaldo edit, cr7 edit, neymar edit, mbappe edit, haaland edit, vinicius jr edit, lamine yamal edit, bellingham edit, salah edit, de bruyne edit, harry kane edit, modric edit, benzema edit, lewandowski edit, pedri edit, gavi edit, rashford edit, saka edit, foden edit, cole palmer edit, musiala edit, wirtz edit, kvaratskhelia edit, osimhen edit, griezmann edit, sergio ramos edit, ronaldinho edit, zidane edit, kaka edit, beckham edit, thierry henry edit, maldini edit, pirlo edit, iniesta edit, xavi edit, pique edit, puyol edit, courtois edit, van dijk edit, rodri edit, fede valverde edit, rodrygo edit, endrick edit, odegaard edit, son heung min edit, julian alvarez edit, lautaro martinez edit, di maria edit, dybala edit, garnacho edit, bruno fernandes edit, grealish edit, trent alexander arnold edit, kroos edit, kimmich edit, thomas muller edit, hakimi edit, dembele edit, raphinha edit, cancelo edit, rafael leao edit, sadio mane edit, luis suarez edit, buffon edit, ibrahimovic edit, real madrid edit, barcelona edit, barca edit, man utd edit, manchester united edit, man city edit, liverpool edit, arsenal edit, chelsea edit, tottenham edit, psg edit, bayern munich edit, juventus edit, ac milan edit, inter milan edit, dortmund edit, atletico madrid edit, napoli edit, argentina football edit, portugal football edit, brazil football edit, france football edit, england football edit, spain football edit, champions league edit, world cup edit, premier league edit, la liga edit, messi 4k edit, ronaldo 4k edit, cr7 4k edit, neymar 4k edit, mbappe 4k edit, haaland 4k edit, vinicius jr 4k edit, lamine yamal 4k edit, bellingham 4k edit, salah 4k edit, de bruyne 4k edit, harry kane 4k edit, modric 4k edit, benzema 4k edit, lewandowski 4k edit, pedri 4k edit, gavi 4k edit, rashford 4k edit, saka 4k edit, foden 4k edit, cole palmer 4k edit, musiala 4k edit, wirtz 4k edit, kvaratskhelia 4k edit, osimhen 4k edit, griezmann 4k edit, sergio ramos 4k edit, ronaldinho 4k edit, zidane 4k edit, kaka 4k edit.  
hashtag: #messiedit, #ronaldoedit, #cr7edit, #neymaredit, #mbappeedit, #haalandedit, #vinijredit, #yamaledit, #bellinghamedit, #salahedit, #debruyneedit, #kaneedit, #modricedit, #benzemaedit, #lewandowskiedit, #pedriedit, #gaviedit, #rashfordedit, #sakaedit, #fodenedit, #colepalmeredit, #musialaedit, #wirtzedit, #kvaratskheliaedit, #osimhenedit, #griezmannedit, #ramosedit, #ronaldinhoedit, #zidaneedit, #kakaedit, #beckhamedit, #henryedit, #maldiniedit, #pirloedit, #iniestaedit, #xaviedit, #piqueedit, #puyoledit, #courtoisedit, #vandijkedit, #rodriedit, #valverdeedit, #rodrygoedit, #endrickedit, #odegaardedit, #sonheungminedit, #julianalvarezedit, #lautaroedit, #dimariaedit, #dybalaedit, #garnachoedit, #brunofernandesedit, #grealishedit, #trentedit, #kroosedit, #kimmichedit, #mulleredit, #hakimiedit, #dembeleedit, #raphinhaedit, #canceloedit, #leaoedit, #maneedit, #suarezedit, #buffonedit, #ibrahimovicedit, #footballedit, #footballedits, #socceredit, #socceredits, #footedit, #football4k, #footballaftereffects, #footballcapcut, #ucledit, #footballvelocity, #realmadridedit, #barcelonaedit, #barcaedit, #manutdedit, #manchesterunitededit, #mancityedit, #liverpooledit, #arsenaledit, #chelseaedit, #tottenhamedit, #psgedit, #bayernedit, #juventusedit, #acmilanedit, #interedit, #dortmundedit, #atleticoedit, #napoliedit, #argentinaedit, #portugaledit, #braziledit, #franceedit, #englandedit, #spainedit, #worldcupedit, #premierleagueedit, #laligaedit, #messiedits, #ronaldoedits, #cr7edits, #neymaredits, #mbappeedits, #haalandedits, #vinijredits, #yamaledits, #bellinghamedits, #salahedits, #debruyneedits, #kaneedits, #modricedits, #benzemaedits, #lewandowskiedits, #pedriedits, #gaviedits, #rashfordedits, #sakaedits, #fodenedits, #colepalmeredits, #musialaedits, #wirtzedits, #kvaratskheliaedits, #osimhenedits, #griezmannedits, #ramosedits, #ronaldinhoedits, #zidaneedits, #kakaedits, #beckhamedits, #henryedits, #maldiniedits, #pirloedits, #iniestaedits, #xaviedits, #piqueedits, #puyoledits, #courtoisedits, #vandijkedits, #rodriedits, #valverdeedits, #rodrygoedits, #endrickedits, #odegaardedits, #sonheungminedits, #julianalvarezedits, #lautaroedits, #dimariaedits, #dybalaedits, #garnachoedits, #brunofernandesedits, #grealishedits, #trentedits, #kroosedits, #kimmichedits, #mulleredits, #hakimiedits, #dembeleedits, #raphinhaedits, #canceloedits, #leaoedits, #maneedits, #suarezedits, #buffonedits, #ibrahimovicedits.

**Marvel** -- phrase: spiderman edit, iron man edit, tony stark edit, captain america edit, thor edit, loki edit, hulk edit, deadpool edit, wolverine edit, venom edit, thanos edit, black widow edit, scarlet witch edit, wanda edit, doctor strange edit, black panther edit, peter parker edit, miles morales edit, gwen stacy edit, spider gwen edit, ant man edit, hawkeye edit, star lord edit, groot edit, rocket raccoon edit, gamora edit, captain marvel edit, moon knight edit, shang chi edit, winter soldier edit, bucky barnes edit, vision marvel edit, nick fury edit, magneto edit, professor x edit, x men edit, avengers edit, mcu edit, guardians of the galaxy edit, blade marvel edit, ghost rider edit, daredevil edit, punisher edit, kingpin edit, ultron edit, kang edit, yelena belova edit, thunderbolts edit, fantastic four edit, tom holland edit, robert downey jr edit, chris evans edit, chris hemsworth edit, tom hiddleston edit, elizabeth olsen edit, scarlett johansson edit, ryan reynolds edit, hugh jackman edit, andrew garfield edit, tobey maguire edit, zendaya edit, benedict cumberbatch edit, marvel edit, avengers endgame edit, infinity war edit, no way home edit, spider verse edit, deadpool and wolverine edit, loki series edit, wandavision edit, multiverse of madness edit, spiderman 4k edit, iron man 4k edit, tony stark 4k edit, captain america 4k edit, thor 4k edit, loki 4k edit, hulk 4k edit, deadpool 4k edit, wolverine 4k edit, venom 4k edit, thanos 4k edit, black widow 4k edit, scarlet witch 4k edit, wanda 4k edit, doctor strange 4k edit, black panther 4k edit, peter parker 4k edit, miles morales 4k edit, gwen stacy 4k edit, spider gwen 4k edit, ant man 4k edit, hawkeye 4k edit, star lord 4k edit, groot 4k edit, rocket raccoon 4k edit, gamora 4k edit, captain marvel 4k edit, moon knight 4k edit, shang chi 4k edit, winter soldier 4k edit.  
hashtag: #spidermanedit, #ironmanedit, #tonystarkedit, #captainamericaedit, #thoredit, #lokiedit, #hulkedit, #deadpooledit, #wolverineedit, #venomedit, #thanosedit, #blackwidowedit, #scarletwitchedit, #wandaedit, #doctorstrangeedit, #blackpantheredit, #peterparkeredit, #milesmoralesedit, #gwenstacyedit, #spidergwenedit, #antmanedit, #hawkeyeedit, #starlordedit, #grootedit, #rocketraccoonedit, #gamoraedit, #captainmarveledit, #moonknightedit, #shangchiedit, #wintersoldieredit, #buckybarnesedit, #visionedit, #nickfuryedit, #magnetoedit, #professorxedit, #xmenedit, #avengersedit, #mcuedit, #guardiansofthegalaxyedit, #bladeedit, #ghostrideredit, #daredeviledit, #punisheredit, #kingpinedit, #ultronedit, #kangedit, #yelenaedit, #thunderboltsedit, #fantasticfouredit, #tomhollandedit, #rdjedit, #chrisevansedit, #chrishemsworthedit, #tomhiddlestonedit, #elizabetholsenedit, #scarlettjohanssonedit, #ryanreynoldsedit, #hughjackmanedit, #andrewgarfieldedit, #tobeymaguireedit, #zendayaedit, #benedictcumberbatchedit, #marveledit, #marveledits, #mcuedits, #marvel4k, #marvelaftereffects, #superheroedit, #marvelvelocity, #comicedit, #avengersendgameedit, #infinitywaredit, #nowayhomeedit, #spiderverseedit, #deadpoolandwolverineedit, #lokiseriesedit, #wandavisionedit, #multiverseedit, #spidermanedits, #ironmanedits, #tonystarkedits, #captainamericaedits, #thoredits, #lokiedits, #hulkedits, #deadpooledits, #wolverineedits, #venomedits, #thanosedits, #blackwidowedits, #scarletwitchedits, #wandaedits, #doctorstrangeedits, #blackpantheredits, #peterparkeredits, #milesmoralesedits, #gwenstacyedits, #spidergwenedits, #antmanedits, #hawkeyeedits, #starlordedits, #grootedits, #rocketraccoonedits, #gamoraedits, #captainmarveledits, #moonknightedits, #shangchiedits, #wintersoldieredits, #buckybarnesedits, #visionedits, #nickfuryedits, #magnetoedits, #professorxedits, #xmenedits, #avengersedits, #guardiansofthegalaxyedits, #bladeedits, #ghostrideredits, #daredeviledits, #punisheredits, #kingpinedits, #ultronedits, #kangedits, #yelenaedits, #thunderboltsedits, #fantasticfouredits, #tomhollandedits, #rdjedits, #chrisevansedits, #chrishemsworthedits, #tomhiddlestonedits, #elizabetholsenedits, #scarlettjohanssonedits, #ryanreynoldsedits, #hughjackmanedits, #andrewgarfieldedits, #tobeymaguireedits, #zendayaedits, #benedictcumberbatchedits.

**Tennis** -- phrase: djokovic edit, nadal edit, federer edit, alcaraz edit, jannik sinner edit, medvedev edit, zverev edit, tsitsipas edit, holger rune edit, casper ruud edit, taylor fritz edit, tiafoe edit, ben shelton edit, kyrgios edit, andy murray edit, serena williams edit, venus williams edit, sabalenka edit, swiatek edit, coco gauff edit, rybakina edit, naomi osaka edit, raducanu edit, pegula edit, ons jabeur edit, badosa edit, dimitrov edit, berrettini edit, musetti edit, jack draper edit, de minaur edit, joao fonseca edit, mensik edit, monfils edit, wawrinka edit, dominic thiem edit, sharapova edit, mirra andreeva edit, paolini edit, zheng qinwen edit, emma navarro edit, madison keys edit, danielle collins edit, wimbledon edit, roland garros edit, us open tennis edit, australian open edit, atp edit, wta edit, laver cup edit, davis cup edit, djokovic 4k edit, nadal 4k edit, federer 4k edit, alcaraz 4k edit, jannik sinner 4k edit, medvedev 4k edit, zverev 4k edit, tsitsipas 4k edit, holger rune 4k edit, casper ruud 4k edit, taylor fritz 4k edit, tiafoe 4k edit, ben shelton 4k edit, kyrgios 4k edit, andy murray 4k edit, serena williams 4k edit, venus williams 4k edit, sabalenka 4k edit, swiatek 4k edit, coco gauff 4k edit, rybakina 4k edit, naomi osaka 4k edit, raducanu 4k edit, pegula 4k edit, ons jabeur 4k edit, badosa 4k edit, dimitrov 4k edit, berrettini 4k edit, musetti 4k edit, jack draper 4k edit.  
hashtag: #djokovicedit, #nadaledit, #federeredit, #alcarazedit, #sinneredit, #medvedevedit, #zverevedit, #tsitsipasedit, #runeedit, #ruudedit, #fritzedit, #tiafoeedit, #sheltonedit, #kyrgiosedit, #murrayedit, #serenaedit, #venusedit, #sabalenkaedit, #swiatekedit, #cocogauffedit, #rybakinaedit, #osakaedit, #raducanuedit, #pegulaedit, #jabeuredit, #badosaedit, #dimitrovedit, #berrettiniedit, #musettiedit, #draperedit, #demnauredit, #fonsecaedit, #mensikedit, #monfilsedit, #wawrinkaedit, #thiemedit, #sharapovaedit, #andreevaedit, #paoliniedit, #zhengedit, #navarroedit, #keysedit, #collinsedit, #tennisedit, #tennisedits, #tennis4k, #tennisaftereffects, #tennisvelocity, #atpedit, #wtaedit, #tenniscapcut, #wimbledonedit, #rolandgarrosedit, #usopenedit, #australianopenedit, #lavercupedit, #daviscupedit, #djokovicedits, #nadaledits, #federeredits, #alcarazedits, #sinneredits, #medvedevedits, #zverevedits, #tsitsipasedits, #runeedits, #ruudedits, #fritzedits, #tiafoeedits, #sheltonedits, #kyrgiosedits, #murrayedits, #serenaedits, #venusedits, #sabalenkaedits, #swiatekedits, #cocogauffedits, #rybakinaedits, #osakaedits, #raducanuedits, #pegulaedits, #jabeuredits, #badosaedits, #dimitrovedits, #berrettiniedits, #musettiedits, #draperedits, #demnauredits, #fonsecaedits, #mensikedits, #monfilsedits, #wawrinkaedits, #thiemedits, #sharapovaedits, #andreevaedits, #paoliniedits, #zhengedits, #navarroedits, #keysedits, #collinsedits.

**Ufc** -- phrase: conor mcgregor edit, khabib edit, jon jones edit, islam makhachev edit, alex pereira edit, adesanya edit, ilia topuria edit, sean omalley edit, sean strickland edit, dustin poirier edit, justin gaethje edit, charles oliveira edit, max holloway edit, volkanovski edit, tom aspinall edit, ngannou edit, khamzat chimaev edit, dricus du plessis edit, merab dvalishvili edit, pantoja edit, shavkat rakhmonov edit, belal muhammad edit, kamaru usman edit, georges st pierre edit, anderson silva edit, ronda rousey edit, amanda nunes edit, valentina shevchenko edit, zhang weili edit, nate diaz edit, nick diaz edit, tony ferguson edit, derrick lewis edit, paddy pimblett edit, bo nickal edit, kai kara france edit, arman tsarukyan edit, umar nurmagomedov edit, ufc edit, mma edit, ufc knockout edit, knockout edit, bjj edit, boxing edit, conor mcgregor 4k edit, khabib 4k edit, jon jones 4k edit, islam makhachev 4k edit, alex pereira 4k edit, adesanya 4k edit, ilia topuria 4k edit, sean omalley 4k edit, sean strickland 4k edit, dustin poirier 4k edit, justin gaethje 4k edit, charles oliveira 4k edit, max holloway 4k edit, volkanovski 4k edit, tom aspinall 4k edit, ngannou 4k edit, khamzat chimaev 4k edit, dricus du plessis 4k edit, merab dvalishvili 4k edit, pantoja 4k edit, shavkat rakhmonov 4k edit, belal muhammad 4k edit, kamaru usman 4k edit, georges st pierre 4k edit, anderson silva 4k edit, ronda rousey 4k edit, amanda nunes 4k edit, valentina shevchenko 4k edit, zhang weili 4k edit, nate diaz 4k edit.  
hashtag: #conormcgregoredit, #khabibedit, #jonjonesedit, #islammakhachevedit, #alexpereiraedit, #adesanyaedit, #topuriaedit, #omalleyedit, #stricklandedit, #dustinpoirieredit, #justingaethjeedit, #charlesoliveiraedit, #maxhollowayedit, #volkanovskiedit, #tomaspinalledit, #ngannouedit, #chimaevedit, #dricusduplessisedit, #merabdvalishviliedit, #pantojaedit, #shavkatedit, #belaledit, #usmanedit, #gspedit, #andersonsilvaedit, #rondarouseyedit, #amandanunesedit, #valentinaedit, #zhangweiliedit, #natediazedit, #nickdiazedit, #tonyfergusonedit, #derricklewisedit, #paddypimblettedit, #bonickaledit, #kaikarafranceedit, #armanedit, #umaredit, #ufcedit, #ufcedits, #mmaedit, #mmaedits, #boxingedit, #fightedit, #ufc4k, #ufcaftereffects, #knockoutedit, #ufcknockoutedit, #koedit, #bjjedit, #conormcgregoredits, #khabibedits, #jonjonesedits, #islammakhachevedits, #alexpereiraedits, #adesanyaedits, #topuriaedits, #omalleyedits, #stricklandedits, #dustinpoirieredits, #justingaethjeedits, #charlesoliveiraedits, #maxhollowayedits, #volkanovskiedits, #tomaspinalledits, #ngannouedits, #chimaevedits, #dricusduplessisedits, #merabdvalishviliedits, #pantojaedits, #shavkatedits, #belaledits, #usmanedits, #gspedits, #andersonsilvaedits, #rondarouseyedits, #amandanunesedits, #valentinaedits, #zhangweiliedits, #natediazedits, #nickdiazedits, #tonyfergusonedits, #derricklewisedits, #paddypimblettedits, #bonickaledits, #kaikarafranceedits, #armanedits, #umaredits.

**Basketball** -- phrase: lebron edit, steph curry edit, kobe edit, michael jordan edit, giannis edit, luka doncic edit, wembanyama edit, kevin durant edit, jokic edit, embiid edit, jayson tatum edit, anthony edwards edit, ja morant edit, kyrie irving edit, james harden edit, shai gilgeous alexander edit, devin booker edit, kawhi leonard edit, jimmy butler edit, damian lillard edit, westbrook edit, klay thompson edit, shaq edit, allen iverson edit, dwyane wade edit, vince carter edit, kd edit, bronny james edit, caitlin clark edit, zion williamson edit, lamelo ball edit, trae young edit, paolo banchero edit, jalen brunson edit, haliburton edit, cooper flagg edit, anthony davis edit, draymond green edit, nba edit, lakers edit, warriors edit, celtics edit, bulls edit, knicks edit, miami heat edit, mavericks edit, spurs nba edit, okc thunder edit, nba finals edit, march madness edit, lebron 4k edit, steph curry 4k edit, kobe 4k edit, michael jordan 4k edit, giannis 4k edit, luka doncic 4k edit, wembanyama 4k edit, kevin durant 4k edit, jokic 4k edit, embiid 4k edit, jayson tatum 4k edit, anthony edwards 4k edit, ja morant 4k edit, kyrie irving 4k edit, james harden 4k edit, shai gilgeous alexander 4k edit, devin booker 4k edit, kawhi leonard 4k edit, jimmy butler 4k edit, damian lillard 4k edit, westbrook 4k edit, klay thompson 4k edit, shaq 4k edit, allen iverson 4k edit, dwyane wade 4k edit, vince carter 4k edit, kd 4k edit, bronny james 4k edit, caitlin clark 4k edit, zion williamson 4k edit.  
hashtag: #lebronedit, #curryedit, #kobeedit, #jordanedit, #giannisedit, #lukaedit, #wembyedit, #durantedit, #jokicedit, #embiidedit, #tatumedit, #anthonyedwardsedit, #jaedit, #kyrieedit, #hardenedit, #shaiedit, #bookeredit, #kawhiedit, #butleredit, #lillardedit, #westbrookedit, #klayedit, #shaqedit, #iversonedit, #dwyanewadeedit, #vincecarteredit, #kdedit, #bronnyedit, #caitlinclarkedit, #zionedit, #lameloedit, #traeedit, #paoloedit, #brunsonedit, #haliburtonedit, #cooperflaggedit, #adavisedit, #draymondedit, #nbaedit, #nbaedits, #basketballedit, #basketballedits, #nba4k, #nbaaftereffects, #hoopsedit, #nbavelocity, #lakersedit, #warriorsedit, #celticsedit, #bullsedit, #knicksedit, #heatedit, #mavsedit, #spursedit, #thunderedit, #nbafinalsedit, #ncaaedit, #lebronedits, #curryedits, #kobeedits, #jordanedits, #giannisedits, #lukaedits, #wembyedits, #durantedits, #jokicedits, #embiidedits, #tatumedits, #anthonyedwardsedits, #jaedits, #kyrieedits, #hardenedits, #shaiedits, #bookeredits, #kawhiedits, #butleredits, #lillardedits, #westbrookedits, #klayedits, #shaqedits, #iversonedits, #dwyanewadeedits, #vincecarteredits, #kdedits, #bronnyedits, #caitlinclarkedits, #zionedits, #lameloedits, #traeedits, #paoloedits, #brunsonedits, #haliburtonedits, #cooperflaggedits, #adavisedits, #draymondedits.

**Golf** -- phrase: tiger woods edit, rory mcilroy edit, scottie scheffler edit, bryson dechambeau edit, jon rahm edit, brooks koepka edit, xander schauffele edit, viktor hovland edit, ludvig aberg edit, collin morikawa edit, jordan spieth edit, justin thomas edit, rickie fowler edit, phil mickelson edit, tommy fleetwood edit, shane lowry edit, hideki matsuyama edit, dustin johnson edit, cameron smith edit, tom kim edit, nelly korda edit, lydia ko edit, paige spiranac edit, grant horvat edit, good good golf edit, bubba watson edit, adam scott edit, patrick cantlay edit, wyndham clark edit, max homa edit, pga tour edit, the masters edit, ryder cup edit, liv golf edit, golf swing edit, golf edit, the open golf edit, us open golf edit, tiger woods 4k edit, rory mcilroy 4k edit, scottie scheffler 4k edit, bryson dechambeau 4k edit, jon rahm 4k edit, brooks koepka 4k edit, xander schauffele 4k edit, viktor hovland 4k edit, ludvig aberg 4k edit, collin morikawa 4k edit, jordan spieth 4k edit, justin thomas 4k edit, rickie fowler 4k edit, phil mickelson 4k edit, tommy fleetwood 4k edit, shane lowry 4k edit, hideki matsuyama 4k edit, dustin johnson 4k edit, cameron smith 4k edit, tom kim 4k edit, nelly korda 4k edit, lydia ko 4k edit, paige spiranac 4k edit, grant horvat 4k edit, good good golf 4k edit, bubba watson 4k edit, adam scott 4k edit, patrick cantlay 4k edit, wyndham clark 4k edit, max homa 4k edit.  
hashtag: #tigerwoodsedit, #rorymcilroyedit, #scottiescheffleredit, #brysondechambeauedit, #jonrahmedit, #brookskoepkaedit, #xanderschauffeleedit, #viktorhovlandedit, #ludvigabergedit, #collinmorikawaedit, #jordanspiethedit, #justinthomasedit, #rickiefowleredit, #philmickelsonedit, #tommyfleetwoodedit, #shaneslowryedit, #hidekimatsuyamaedit, #dustinjohnsonedit, #cameronsmithedit, #tomkimedit, #nellykordaedit, #lydiakoedit, #paigespiranacedit, #granthorvatedit, #goodgoodedit, #bubbawatsonedit, #adamscottedit, #patrickcantlayedit, #wyndhamclarkedit, #maxhomaedit, #golfedit, #golfedits, #golf4k, #golfaftereffects, #pgaedit, #golfswingedit, #pgatouredit, #themastersedit, #rydercupedit, #livgolfedit, #theopenedit, #usopengolfedit, #tigerwoodsedits, #rorymcilroyedits, #scottiescheffleredits, #brysondechambeauedits, #jonrahmedits, #brookskoepkaedits, #xanderschauffeleedits, #viktorhovlandedits, #ludvigabergedits, #collinmorikawaedits, #jordanspiethedits, #justinthomasedits, #rickiefowleredits, #philmickelsonedits, #tommyfleetwoodedits, #shaneslowryedits, #hidekimatsuyamaedits, #dustinjohnsonedits, #cameronsmithedits, #tomkimedits, #nellykordaedits, #lydiakoedits, #paigespiranacedits, #granthorvatedits, #goodgoodedits, #bubbawatsonedits, #adamscottedits, #patrickcantlayedits, #wyndhamclarkedits, #maxhomaedits, #tigerwoods4k, #rorymcilroy4k, #scottiescheffler4k, #brysondechambeau4k, #jonrahm4k, #brookskoepka4k, #xanderschauffele4k, #viktorhovland4k, #ludvigaberg4k, #collinmorikawa4k.
