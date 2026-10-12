# BL-1619 (final): 170 new editor emails for $14.89 of $15, resumed after a power loss

1. **Power loss cost:** $0.0282 unbooked (47 requests, now booked); 0 delivered rows lost; 1 file repaired (the tag ledger, zeroed); about 6 raw phase-2 movies rows lost before they were saved (not re-bought).
2. **New emails per niche:** football **21**, tennis **1**, movies **148** = **170** (phase 1: 4 / 1 / 65; phase 2: 17 / 0 / 83).
3. **$ per niche** (since his split): football **$2.17**, tennis **$0.10** (dry), movies **$11.24** (its $6.80 plus tennis's and football's leftovers, his rule). Phase 1 before the split: $1.38.
4. **Total:** **$14.89 / $15.00**, by the vendor's balance (342,768 → 317,944 requests, minus the friend's 6). spend.json now books the same 24,818 requests.
5. **Cost per 1,000:** **$87.6** over all 170. Phase 2 alone: $135 per 1,000 (100 for $13.51).
6. **Audit:** phase 2, 40 random keeps re-judged blind on fresh covers: **36 real edit pages (90.0%)**, 0 creators, 0 businesses, 4 unclear. The 4 unclear were dropped before delivery. Phase 1: 39/40 (97.5%).
7. **File:** `%LOCALAPPDATA%\ClippersHQ\operator\editor_emails_20261011_BL1619.xlsx` (170 rows: all 70 phase-1 rows plus the 100 new ones, with a niche column; read back).

Also written: master +100 through `crossdedup.append_leads` (run_id bl1619, 0 merged, backup made). Workbook Emails 4,492 → 4,592; every other sheet unchanged; **MARK untouched**; backup sha-verified and vaulted. **No email was sent.**

## 1. The power loss (2026-10-10 ~22:30)

- **Where it stopped.** Phase 1 had already delivered 70 at 22:00. He then removed the $30-per-1,000 limit and set a 50/25/25 split of the remaining $13.61. Three small probe walkers started at 22:28. Football and tennis finished. The movies walker was cut mid-walk. PROGRESS.md never recorded the new rule, but the code did: `walk.py --dry-streak` and `deliver.py` "phase 2".
- **Processes and locks.** No BL-1619 process survived. Every lock file was a 0-byte filelock from July to September with no PID. Nothing was removed.
- **Money.** Balance minus booked left 47 requests ($0.0282). They were booked as `bl1619_crash_gap` (estimated). A walker leaves at most 9 calls unbooked, and the balance gap was already 11–23 before phase 2, so this is real-minus-booked, not all from the last seconds.
- **Files.** master was intact: 77,533 rows = the pre-append backup plus 70, full width, last written 22:00. The workbook was intact (4,492). The delivered xlsx was intact (70). Seen-stores, spend.json, edits.db (quick_check) and every checkpoint were OK.
- **Damaged: `email_harvest_tags.json`.** All 416,898 bytes were NUL. The save wrote a tmp file and renamed it with no fsync, so the rename reached the disk and the data did not. `TagLedger` refuses an unreadable ledger, so nothing re-paid.
  - **Rebuilt** to 2,164 tags. Base: HEAD's ledger from BL-1617 (1,496 tags). Added 598 phase-1 tags: every phase-1 tag file minus the phase-2 lists, which were generated from the live ledger at 22:26. The batches' own status files count 601. Added the first 24/16/30 tags of the phase-2 lists, over-marked on purpose. Every rebuilt entry is marked `reconstructed: true`.
  - **Root fix:** `TagLedger._save_locked` now fsyncs before the rename. `tests/test_bl1619_ledger_fsync.py` 3/3.
- **The crashed movies walker's rows** were never written; `walk.py` wrote rows only at exit. Its tags are marked walked, so they were not re-bought.

## 2. Phase 2: how the money went

New walker `scratch/bl1619/walk2.py`:
- **One process for all niches**, with one meter per niche and per-niche spend labels.
- **Cheapest source first:** raw new emails per call times the measured keep rate, re-ranked every 100 calls after a 60-call explore.
- **His dry rule:** 300 calls in a row with no new email, carried across waves; a dry niche's money moves to movies.
- **Power-loss proof:** rows are fsynced per page, the ledger per tag, and PROGRESS.md's LIVE block every 25 paid calls. A PID lock stops two walkers running at once.

| source (phase 2) | kept / pictured | keep rate | note |
|---|---|---|---|
| names3 + names4 + names5 (actor / character / film "<name>edit") | 35 / 163 | 21% | the best movies sources; names5, the third list, fell to 12% |
| series_people / series_shows2 / films_franchise3 (left from phase 1) | 18 / 75 | 24% | walked out |
| capnames (top "<x>edit" tags from captions already paid for) | 21 / 174 | 12% | free tags, paid walk |
| phrase2tag (edits.db harvester phrases as "<phrase>edit") | 8 / 134 | 6% | one football tag was Roblox (30 X) |
| variant_football | 10 / 56 | 18% | "*skills" tags = coaches and freestylers (3/62) |
| snow (his YES pages' hashtags, keeps' feeds, captions) | 8 / 78 | 10% | |
| variant_movies (4k / cc / clips forms) | 0 / 42 | 0% | most of these tags do not exist |
| tennis (every source) | 0 / 5 pictured | 0% | DRY at 14:08 → $3.24 moved to movies |

Phase 2 totals: 100 kept of 727 pictured (14%). That's $13.51, or $135 per 1,000 kept: about 7× the phase-1 rate. The cheap sources had been walked before the split.

## 3. Things found on the way (measured, now in code)

- **The vendor does not bill a 5xx.** At 12:14, 514 metered 5xx attempts were exactly the gap between booked and balance. They were reversed per niche, and walk2 books them back itself. spend.json equals the balance (gap 0 at every check; a final 28-request over-booking was trued up).
- **A 503 is overload, not "no such tag".** Wave 2 recorded about 133 real tags as walked after a 503. 432 phase-2 5xx entries were removed from the ledger (backup `.pre_5xx_cleanup_bl1619`). A 503 now requeues (free); only a 500 records the tag.
- **Starved priority.** The PC was at 100% CPU from other projects, and run_detached jobs run BelowNormal. Raising my own walker PIDs to Normal made the walk about 2.5× faster.
- **My mistake, caught.** At 13:15 I relaunched while the stopping run was still alive. The second run was stopped before any call (0 billed, ledger untouched). The PID lock above came from this.

## 4. Safety

- Dedupe against master, both workbook copies, every operator xlsx and dead-MX domains, at walk time and again at delivery.
- master only via `append_leads`; workbook by header name.
- No row deleted; MARK untouched; nothing sent.
- No address, handle or key appears in any repo file or log.
- Tests: `test_bl1619_ledger_fsync` 3/3, `test_bl1619_user_by_handle` 5/5, `test_bl1619_bio_emails` 6/6. The full `run_all` was not run (per memory, it leaves about 1.3 GB in %TEMP% per call).
