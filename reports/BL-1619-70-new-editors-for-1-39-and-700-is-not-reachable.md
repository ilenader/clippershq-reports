# BL-1619: 70 new editor emails for $1.39 of $15; 700 is not reachable

## Answer card

| | |
|---|---|
| **Status** | **Finished, stopped early on his rule.** Every source is now either used up or above $30 per 1,000 kept. $13.61 of the cap is unspent. |
| **New emails delivered** | **70**: football **4**, tennis **1**, movies **65** (Marvel, DC, big films and big series) |
| **Free vs paid** | **26 free**: 18 bios the edit app had already paid for, plus old run files and link pages. **44 paid**: edit-hashtag walks. |
| **Spent** | **$1.39** by the vendor's free balance read: 342,768 → 340,445 = 2,323 requests. The ledger booked 2,306 calls ($1.384) to campaign bl1619. No other campaign spent in the window. |
| **$ per 1,000** | **$19.9** over everything delivered ($1.394 / 70). |
| **Audit** | 40 random keeps, newest covers, numbered rows only: **39 real edit pages (97.5%, 95% CI 87–100%)**. The 1 failure was a scene-compilation page; it was dropped before delivery. |
| **File** | `<PROFILE>\AppData\Local\ClippersHQ\operator\editor_emails_20261010_BL1619.xlsx` (70 rows, read back) |
| **Also written** | master +70 through `crossdedup.append_leads` (run_id bl1619). Workbook: Emails 4,422 → 4,492, every other sheet unchanged, **MARK untouched**, backup sha-verified and vaulted. **No email was sent.** |

## 1. Why it stopped the first time (15:04)

- The run started at 13:09.
- At 15:01 he sent the Tailscale friend-link task (BL-1620) to the same session, and the session switched to it.
- At that point: 61 kept, 61 waiting for a picture, nothing delivered, $0.875 booked.
- No process was left running. The claim stayed open.

## 2. What the continuation found

**A broken account lookup.** `/v1/user/by/username` now answers `{"users": {<handle>: …}, "stats": {<handle>: …}}`. `edits_vendor.user_by_handle` read that shape as "no user".
- So every old-file handle looked deleted.
- The app's **pasted accounts** (BL-1606 `resolve_handles`) were marked UNREACHABLE the same way.
- Fixed in `clippershq/edits_vendor.py`. `tests/test_bl1619_user_by_handle.py` 5/5.

**The 61 waiting accounts (old run files, handle only):**
- 26 are not found (deleted or renamed) and were dropped.
- 35 are live. All 35 were pictured; 1 is an edit page.
- New rule for old-file rows: the address must **still be in today's bio**, otherwise it is dropped (text may only drop). All 10 old-file keeps were re-checked: 9 still show it, 1 could not be matched and was dropped.

**Stored edit-app bios, re-pulled:** 0 new since this morning.

## 3. Paid sources, priced with their pictures ($ per 1,000 KEPT)

| Source | Calls | Kept | $/1k kept | Decision |
|---|---:|---:|---:|---|
| Series show tags (first list) | ~460 | 14 | ~$19 | done; all walked |
| Snowball, series tags | ~295 | 12 | ~$14 | done; mining finds no new series tags |
| Film franchises (Twilight, Harry Potter, horror, …) | ~380 | 8 | ~$27 overall, last stretch $37 | done; list walked |
| Series show tags (second list) | ~156 | 3 | ~$31 | **dropped** (over $30); 140 tags unwalked |
| Single film titles (third list) | 104 | 0 | — | **dropped** (1 raw new in 104 calls) |
| Films (first pass) | ~400 | 5 | ~$49 | dropped earlier |
| Characters/actors | 109 | 1 | ~$65 | dropped earlier |
| Snowball, film tags | ~90 | 2 | ~$53 | dropped; 4 tags left |

- **The cut, made honest.** The walker cuts a source by raw new emails per call. The franchise list was cut at 0.065 per call, against a 0.075 line set from an assumed 29% picture pass rate. Pictured, 57% of its raw emails passed, which is about $17 per 1,000 kept, so it was resumed with the line re-derived (0.045). Its last stretch then cost $37, and the list was used up.

## 4. What is realistic

- **Football and tennis have been gone since BL-1617:** every cheap source was walked, at $120–170 per 1,000. This round added 4 football and 1 tennis, all from data already paid for.
- **Big series and films were the one fresh pocket.** It gave about 45 paid keeps under $30 per 1,000 and is now walked.
- **Inside his rules, the next 1,000 costs $30–65 per 1,000 and would not reach 700.** What's left: the 140 unwalked second-list series tags at ~$31 (about 10 more), then characters ($65).
- **Cheap only outside the rules:**
  - Any-niche pro-tool video editors (BL-1616: $4.84 per 1,000, 40/40 real).
  - A wider niche: anime / K-drama / TV-show edit pages. These are the largest group of unknown tags among the keepers.

## 5. Notes

- **Slip:** while finding the lookup bug, a shape probe printed 2 handles into the tool output (dict keys). Not in any file or report.
- **Pre-existing reds:** `tests/test_bl1599_edits_engine.py` has 3 reds (expects DOWNLOADED, gets QUALIFIED: the BL-1604 download pause). Identical with the committed vendor file, so not this round's.
- **Where the data lives:** work data is in `%LOCALAPPDATA%\ClippersHQ\bl1619_work\`. The repo holds counts only.
- **Tag ledger:** every walked tag is recorded in `email_harvest_tags.json`, so none is paid twice.

Files: `scratch/bl1619/` (PROGRESS.md, combine.py with the stale-address and not-found drops, gen_series2.py, gen_films3.py, deliver.py with a free/paid column, the status and audit JSON).
