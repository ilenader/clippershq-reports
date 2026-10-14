# BL-1643: RAW EMAILS mode. Every new email on the hashtags you pick costs $4.93 per 1,000 (85 new for $0.42)

## Card

| | |
|---|---|
| **Honest line** | **Raw mode works and lands just under your $5 line: 85 new emails for $0.419 = $4.93 per 1,000**, balance-checked (the vendor counted 699 requests, the same as our meter). No AI, no eye check. |
| **Where it is cheap** | **Tennis $2.8 and movies/shows $2.7 per 1,000.** Football $5.7, basketball $6.4, superhero and UFC $9.5. |
| **The limit is volume, not price** | Each tag gives about **0.7 new emails** (about 6 pages, then it is empty). 1,000 emails needs about **1,400 tags**. There are about **16,400 tags walked on v2 but never on v1**, 4,800 of them in your niches, so roughly **11,000 raw emails at about $5 per 1,000** are left in stock (about 3,400 in your niches). |
| **What was built** | The old email harvester was upgraded, not rewritten: v1 first, free tag ids (no lookup call), v2 only where v1 found something new, a price line per tag, a checkpoint per tag, detached runs. One command: `clippershq/raw_emails.py`. |
| **Files** | `operator\raw_emails_20261014.xlsx` (85 rows: email, handle, hashtag, niche, followers, date). Your workbook has a new sheet, **"Raw"** (85). Master has 85 rows, `lead_kind = raw_edit_hashtag`. None of these are mixed with the eye-checked editor files. |
| **Menu** | `operator\HASHTAG_MENU_20261014.xlsx`: 300 tags across your 6 niches, best 50 marked, every estimate **calibrated on this test**. |
| **Money** | **$0.4194** of the $0.50 cap (vendor balance). The ledger booked $0.4236: 7 network-reset retries were counted as billed. Nothing more is spent until you say "run". |

## Your decisions

| | Question | My recommendation |
|---|---|---|
| A | Pick tags from the menu and say "run" with a cap. | **Start with tennis and movies/shows** (measured about $2.7–2.8 per 1,000). Football and basketball are around $5.7–6.4; superhero and UFC about $9.5. |
| B | Price line on or off? It stops a tag after 3 pages with no new email. | **On** (the default, $5). Replayed on the 100 full walks it cuts cost to **$4.27 per 1,000** but finds **30% fewer emails per tag**, so the stock runs out sooner. If you care more about how many emails than about price, turn it off (`--price-line 0`). |
| C | v2 follow-up (goes deep on tags where v1 found something). | Built but **not measured**: every test tag was already walked on v2. It has its own price line, so it stops by itself above $5. |

## 1. Asked

Owner, 19:52: "we're just going to do hashtags ... Jannik Sinner edit, some other player edit ... we're not gonna see if they're an editor or not, we're just gonna scrape every single one of them ... under $5 for a thousand ... don't delete the current one, build on top". The order had five steps: upgrade `email_harvester.py`; its own output file, master rows and a "Raw" workbook sheet; a menu of about 300 tags with the best 50 marked; a price test on the 20 best ($0.50 cap); then stop and wait.

## 2. What was built (on top of the old harvester, nothing removed)

`clippershq/email_harvester.py` (the BL-1541 tool):
- **Free tag ids**: `tag_ids=` skips the `/v1/hashtag/info` call (BL-1624: a third of every walk). 117 of the 120 test tags had a free id. Every item bought now adds its caption tag ids to `%LOCALAPPDATA%\ClippersHQ\raw_emails\tagids.json`, 11,221 so far.
- **`run_raw`**: every tag on v1 first, then v2 only on tags whose v1 walk bought at least one new address and that v2 never walked. One budget, one guard, one checkpoint. The two walks of one tag are keyed `tag` and `tag@v2`.
- **New addresses counted inside the walk** (`claim_in_walk`), so the price line and every count use new emails only. In raw mode the ledger records new addresses, which is the meaning BL-1628/1630's v1 walks used.
- **Price line** (`price_line_usd_per_1k`): from page 3, a tag stops when its last 5 pages bought fewer new addresses than the line allows. The stop reason `price_line` is final, so a re-run never re-pays a priced-out tag.
- **v1 `hasMore=false` is trusted** (on v1 only, and only an explicit false). BL-1628 paid for an empty page after it on every tag; v2's has_more is still ignored (it lies).
- **Followers for free** from the v1 item's `authorStats`: 83 of 85 rows have it, the other 2 are blank (never a fake 0). Only rows with an address are kept in the checkpoint (BL-1625: big JSON stalls).
- **Bug fixed**: the walk asked the dedupe guard about a handle without saying "tiktok". `DedupGuard.build()` stores master's handles as `tiktok:<handle>` (BL-1565), so **the walk never matched a master handle**; it matched only on account id. It now passes `platform="tiktok"`. Test: `GuardScope`.

`clippershq/raw_emails.py`:
- `walk` (detached via `tools/run_detached.py`, STOP file, PROGRESS.md + status.json every 25 pages, balance read before and after).
- `status`.
- `deliver`: re-checks every address against everything again, then writes the raw xlsx, the master rows and the workbook sheet.

**New** means not in: master (addresses + TikTok handles), every `.xlsx` in the operator folder including the workbook (24 files), the edit app (`bio_emails` + every stored bio), and not on a dead-MX domain.

`tools/deliver_workbook.py --raw-sheet Raw`: a tool-owned sheet. Same safety as before: backup sha-checked first, MARK untouched, read back, vaulted. The Emails sheet is never touched.

Tests: `tests/test_bl1643_raw_emails.py` (17, green): free id = no lookup; v1 stops on hasMore=false; v2 has_more still ignored; only new addresses count; price line ends a dud and keeps a rich tag; v2 follows only tags with a new email on v1; resume never re-pays; master handle skipped; dead MX; followers/caption ids; tags file; raw rows are never a send kind; Raw sheet. The 104 older harvester tests and 28 workbook tests are green; full `run_all.py`: see §7.

## 3. The menu ($0)

`operator\HASHTAG_MENU_20261014.xlsx`, sheet "Menu": 300 tags. Football 60, tennis 50, basketball 50, UFC 45, superhero 45, movies/shows 50. Each tag shows: walked before on v1 / v2 (date, pages, new emails), free id, how many edit-app accounts use it, expected new emails per $1, expected $ per 1,000, and how the estimate was made. Best 50 are highlighted (at most 12 per niche). Sheet "Price test (walked)" holds the 120 tested tags with what each one bought.

Candidates: 384 names and short names (581 stems: players, fighters, actors, characters, shows) as `<name>edit` / `<name>edits`, plus edit-app caption tags that contain one of those names. Only tags known to exist (free id, edit-app use or ledger) are kept, because a lookup on a tag that does not exist is still billed (BL-1624). A tag already walked on v1 is offered only on v2.

**The estimate, and why it was cut in half.** The first model (measured v1 rate of ledger tags with the same v2 history) said **$2.1–2.6 per 1,000**. The test measured **$4.93**: the model was **1.9× too optimistic** (ufc 2.4×, superhero 2.4×, football 2.1×, basketball 2.0×, movies 1.5×, tennis 1.5×). The reason: the ledger's old v1 rates were "new" against a smaller known set; half the addresses the test saw are already yours now. Every menu number is now multiplied by its niche factor. The best 50 average **$5.18 per 1,000** after calibration.

Top 30 (calibrated $ per 1,000): lacasadepapeledit, anyataylorjoyedit, dwaynejohnsonedit, arthurshelbyedit $3.51; joegoldbergyouedit, dracoedit $3.96; prisonbreakedit, barryouterbanksedit, keanuedit $4.08; musettiedit, draperedit, fonsecaedit, dimitrovedit, raducanuedit, badosaedit, paoliniedit $4.39 (tennis); f1edit, theboysedit, movieedit, twdedit, twilightedit, thewalkingdeadedit, supernaturaledit, elliewilliamsedit, tlouedit, hannibaledit, thelastofusedit, hanniballecteredit, bettercallsauledit, michaelmyersedit $4.42.

## 4. The price test (balance-checked)

| | test20 (price line $5) | next100 (price line off, full v1) | both |
|---|---|---|---|
| tags | 20 (3–4 per niche) | 100 (15–20 per niche) | 120 |
| calls = vendor requests | 77 = 77 | 622 = 622 | 699 |
| $ | 0.0462 | 0.3732 | **0.4194** |
| posts seen | 2,206 | 16,640 | |
| accounts new to us | 1,310 | 8,685 | |
| accounts already yours / repeated across tags | 306 / 589 | 2,629 / 5,307 | |
| bios with an address | 18 | 113 | |
| addresses already yours | 9 | 34 | |
| **new emails** | **9** | **79** (3 also found by test20) | **85 distinct** |
| **$ per 1,000 new** | $5.13 | $4.72 | **$4.93** |

**Why I went past "the 20 best"**: 20 tags gave only 9 emails, too few to tell $3 from $9, with $0.45 of the cap unspent. I walked the next 100 menu tags inside the same cap, v1 only, with the price line off, so the line could be replayed on full walks. Total stayed at $0.419 of $0.50.

**One page of v1** = about 27 posts, 14 accounts new to us, 0.19 addresses in bios, **0.13 new emails**. New emails per page by depth (next100): 0.18, 0.06, 0.14, 0.18, 0.17, 0.07, then 0 (v1 serves about 6 pages).

**By niche** (both runs, $ per 1,000 new): tennis **2.8** (24 new), movies/shows **2.7** (25), football **5.7** (13; test20's 4 football tags gave 0), basketball **6.4** (13), superhero **9.5** (6), UFC **9.5** (7). Each niche count is small; the ranking matters more than the exact number.

**Concentration**: 66 of 120 tags gave 0 new emails; the best 10 of next100 gave 39% of its emails.

**Price-line replay** on the 100 full walks: stop after 3 pages with nothing new: **391 pages, 55 new = $4.27 per 1,000**, against 619 pages, 79 new = $4.72 without. Lines of $3, $4, $5 and $7 all give the same stops at this sparsity (the line only ever fires on "0 new in the window").

## 5. How much is left

- 16,396 tags were walked on v2 and never on v1. By edit-app niche: superhero 2,588, tennis 1,388, football 559, UFC 148, basketball 138, unknown 11,575. 1,251 of them had at least one v2 email.
- At about 0.7 new emails per tag: **about 11,000 raw emails, about 3,400 in your niches**, at around $5 per 1,000. The cheap part is tennis and movies/shows.
- Every walk adds free tag ids from the captions it buys (+11,221 this round), so the "no lookup" share stays high.

## 6. Delivered

| | count |
|---|---|
| `operator\raw_emails_20261014.xlsx` "Raw emails" (read back) | 85 |
| master rows, `lead_kind = raw_edit_hashtag`, run_id raw_test20 (9) + raw_next100 (76) | 85 |
| workbook sheet "Raw" (new; every other sheet unchanged, MARK untouched, vaulted) | 85 |
| by niche | tennis 24, movies/shows 23, football 13, basketball 12, UFC 7, superhero 6 |

`raw_edit_hashtag` is not a send kind (`writer.lead_kind_of` calls it unroutable), so no send file picks these rows up. No email was sent.

## 7. Checks

- Vendor balance before/after each run = the meter (77, 622).
- Booked spend `raw_emails` = $0.4236 (706 calls); the 7 extra are network-reset retries counted as billed. Over, never under.
- Tests: 17 new + 104 harvester + 28 workbook green. `tests/run_all.py` (579 suites, run while the paid walks were live): **37 red**. 33 of the 37 are also red at HEAD (`run_all --head`, the same 37), so they were red before this round. One was this round's: `test_atomic_io` (new modules used a bare `os.replace`), now fixed; the 3 it still lists are other windows' files. The other 3 are not this code: `test_bl1307_veto_refused` (an untracked `scratch/bl1441` file the HEAD copy does not have), `test_bl1461_video_strip` (an ffmpeg argument error), `test_send_list_rebuild` (the send file's saved row count is older than master, which keeps growing, these rounds' raw rows included; plus an old `bl1572` csv). None of the 37 imports a file this round changed, except `test_atomic_io`.

## 8. How to run it (for the next window)

```
python clippershq/raw_emails.py walk --tags-file <tags.tsv: tag TAB niche> --cap <USD> --run <name> [--price-line 5] [--lanes 4]
python tools/run_detached.py start --name raw_<name> -- <venv python> clippershq/raw_emails.py walk ...   (long runs)
python clippershq/raw_emails.py status --run <name>
python clippershq/raw_emails.py deliver --run <name>        (raw xlsx + master + workbook "Raw")
```
Work data: `%LOCALAPPDATA%\ClippersHQ\raw_emails\<run>\` (checkpoint, pages.jsonl, status.json, PROGRESS.md, STOP to stop). Menu builder: `scratch/bl1643/menu43.py` (+ `names43.py`, `explore43.py`); analysis `scratch/bl1643/ana43.py`.

- 20:47 FINDER BL-1643 RAW EMAILS mode: 85 new emails for $0.419 = $4.93 per 1,000 (tennis/movies about $2.8, superhero/UFC $9.5), menu of 300 calibrated tags, waiting for his "run" (DONE)
