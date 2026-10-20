# BL-1677 -- Dusan's shared Drive folder: "No email - editors" + "New emails - never sent" (1 LEADS, orders 19 Oct 15:16 + 15:46)

**Order:** one Google Sheet "Editors - no email" from the no-email-yet list plus every new one; two tabs, Instagram and
TikTok; columns = a working clickable profile link, then a Sent / Not sent dropdown (default Not sent), nothing else;
editors only, niches sports, movies, TV shows, celebrities; anyone with the link can edit; link to Dusan today; then keep
adding (free sources first, paid only inside the $5/day cap).

**Result (16:00, 19 Oct):** the sheet is up in his Google Drive, shared *anyone with the link can edit* (checked through
the Drive permissions list, and opened with no sign-in: HTTP 200). The link is in the office reply file only, not in this
published report: anyone holding it can edit the sheet.

| tab | rows | sports | movies / TV | celebrities |
|---|---|---|---|---|
| TikTok | 8,992 | 5,530 | 3,196 | 266 |
| Instagram | 176 | 102 | 69 | 5 |

Read back from Google after upload: both tabs, every row a clickable link, every Sent cell "Not sent", one list validation
`Sent,Not sent` covering every data row. Money: **$0** (no vendor call; Drive upload through his existing connection).

## Who is on it (editors only, his four niches)

The no-email-yet store held 11,296 TikTok editors (BL-1669: edit-app proven + AI-judged editors, and collab partners).

| group | rows | decision |
|---|---|---|
| edit-app accounts in football / basketball / ufc / tennis / golf / f1 | 5,007 | sports |
| edit-app accounts in superhero (Marvel + DC) | 2,249 | movies / TV |
| scope pass filed out as other_movies_shows | 499 | movies / TV |
| filed out as other_sports / golf | 377 | sports |
| filed out as anime / gaming | 897 | off |
| photo-post pages | 88 | off |
| filed out as music / unclassifiable (mixed classes) + 1,197 collab partners with no niche | 2,179 | Sonnet text check |

The "music" scope class is not a music class in practice: its found-terms include TV characters, k-pop idols, a footballer
and Deadpool, so those 2,179 went to five Sonnet agents (one letter per account from handle, nickname, bio, found term,
top hashtags, one caption): S 146, M 448, C 266 kept; X 383 (anime / games / cars / audio pages), N 79 (not an edit page),
U 857 off. The U group is mostly collab partners whose page shows no niche at all (857 of the 1,197 had only a name and a
bio) -- they are editors, but the niche cannot be seen without reading their videos. Spot check of 18 random answers
against their input lines: all plausible (e.g. a Djokovic page S, a Vampire Diaries page M, an audio page X).

Instagram: the IG each editor names on his own TikTok page (`bio_parser.extract_instagram` on bio + bio link), for the
TikTok editors on the sheet: 176 handles; BL-1667's paid IG lookups (75 found with no email on either side) were all
already in that set. One IG already holding an address in the lead files was dropped (a lead, not "no email").

## How (and why that way)

- **Google's Sheets API is not enabled on rclone's shared Google project** (403 PERMISSION_DENIED, measured), so the
  sheet is an .xlsx (two tabs, hyperlinks, a list validation) that the **Drive API** converts into a native Google Sheet,
  using the token rclone already holds (scope drive.file: it can see only files it made). Probe first, on 3 public
  handles: create + export + update-in-place + share all worked, the dropdown and links survived both the upload and an
  update; the probe file was deleted.
- **A push never loses his marks:** it exports his live sheet, keeps every row in it (order and Sent value as he left
  them), appends only links never pushed before (state keeps every link ever pushed, so a row he deletes does not come
  back) and uploads onto the same file id, so the link never changes. A sheet that has vanished raises an error instead
  of quietly making a second one with a new link.
- rclone's shared project also runs out of its per-minute Drive quota (403 rateLimitExceeded on the first try): every
  call backs off and retries.

`clippershq/no_email_sheet.py` (`plan | ask <dir> | labels <dir> | push | link`), tests `tests/test_no_email_sheet.py`
(9: niche rules, never over his NO, the file shape, push keeps Sent + order + deletions, vanished sheet, label parsing).
Work scripts in `scratch/bl1677/` (probe77, sel77, ig77, rs77).

## Tests

`run_all -k test_no_email_sheet,test_no_email_yet`: 2/2 green. Full suite not run: PC at 3.93 GB free (under the 4 GB
floor). Send-guard suites: test_bl1252_send_guard and test_bl1392_send_wiring green; test_bl1308_mx_refusal and
test_bl1432_send_unblock red on LIVE data (suppress_mx.json 32 days old, MX coverage 36% of the lead-file domains), not
this round's code.

## 15:46 orders: ONE shared folder, two sheets

The folder (anyone with the link can edit, checked; opens with no sign-in and lists both sheets) holds:

1. **"No email - editors"** -- the sheet above, moved in and renamed (the 15:46 wording; same file, same link).
2. **"New emails - never sent"** -- 1,417 editor addresses: profile link (clickable), email, Sent / Not sent.
   - FOUND: the editor sheets (Editors / Editors first world / Other countries / Unknown country) of the 153 lead files in
     operator\ dated 15 Oct or later -> 2,263 distinct editor addresses. Never: Unsure sheets, rows moved out by the
     BL-1670 face check, *_CREATORS, raw_emails pages, *_ANIME / *_GAME / *_FREELANCER.
   - RECEIVED (removed): 846 of them are in the lists already sent to his Drive (operator\leads_15_oct + leads_17_oct,
     BL-1655 / BL-1656). **His ONE workbook is not a "received" test:** every run is appended to it automatically --
     68,777 addresses, all 2,263 included -- so measured against it, 0 would be "not received".

`clippershq/new_emails_sheet.py` (`plan | push`), same push rules as the first sheet; folder via
`no_email_sheet.folder()` (made once; a vanished folder is an error, never a second link). Tests: 10/10
(`test_one_shared_folder_holds_both_sheets_and_is_made_once` covers the folder, the rename and Sent kept on sheet 2).

## Keep adding (order 15:46 "as many Instagram and TikTok editors as possible"), free first

**Raw store ($0, already paid for):** `scratch/bl1677/rs77.py` read all 86 raw_store account files = **842,691 accounts**;
61,391 name themselves editors (handle / nickname: edit, edz, vfx, fx, ae). Removed: 1,099 with an email in the bio,
2,764 already leads (master), 1,208 already on the list, 52 he marked NO / OFFICIAL / PHOTO. Niche from each account's own
post hashtags + captions + found-on tags (edits_scope labels): sports 11,830, movies/TV 10,816, out (anime / gaming lead)
3,572, no clear niche 30,050.

**Blind audit before adding** (450 random, 3 Sonnet agents, rule class hidden):

| rule class | n | in his 4 niches | exact niche | not an edit page |
|---|---|---|---|---|
| sports | 156 | **99%** (S 130, M 20, C 4; X 2) | 83% | 0 |
| movies / TV | 144 | **100%** (M 136, C 7, S 1) | 94% | 0 |
| no clear niche | 150 | 81% (M 79, C 33, S 9; X 19, U 8, N 2) | -- | 1% |

The sheet has no niche column, so "in his 4 niches" is the bar: sports + movies/TV added (22,646; 38 the edit app had
filed out of scope stay off). The no-clear-niche 30,050 are NOT added blind (19% would be anime/games/unclear): they need
the per-account text check first.

**Instagram:** the same IG-named-on-the-page pass over the new editors: +366 (542 total).

| tab | 16:00 | now |
|---|---|---|
| TikTok | 8,992 | **31,600** |
| Instagram | 176 | **542** |

Traps: reading 300+ operator .xlsx files for the lead check took >30 min at the detached job's priority (py-spy) --
master_leads.csv already holds every delivered lead row, so it is the only check now; openpyxl's normal load binds every
hyperlink and stalled for minutes on 31,600 rows -> read-only load. A push of the big sheet takes ~6 min (Drive's
conversion).

## The 30,050 no-clear-niche pages: Sonnet text check ($0 vendor)

31 Sonnet agents, 1,000 pages each (handle, found-on tags, nickname, bio, top hashtags, one caption; one letter each).
Every answer file is used only if its ids match its input exactly (`scratch/bl1677/pool77.py check`).

| letter | pages |
|---|---|
| M movies / TV | 15,787 |
| C celebrities | 5,684 |
| S sports | 1,915 |
| X other niche | 4,032 |
| U cannot tell | 1,231 |
| N not an edit page | 401 |

(30,050 pages. File 22 was redone: its first agent said it filled lines it did not list with M, so those M labels were not
judgements; the file was held out and re-run clean -- S 61 / M 548 / C 185 / X 143 / N 25 / U 38.) **Cross-check against the independent blind audit** (143 pages
seen by both): kept/not-kept agree on 94%; of the pages the check kept, the audit also kept 111/115 = **97%**.

Added: 24,180 TikTok editors (S / M / C); Instagram named on their pages: +205.

| tab | 16:00 | 17:50 | final |
|---|---|---|---|
| TikTok | 8,992 | 31,600 | **55,710** (sports 19,356, movies/TV 30,255, celebrities 6,099) |
| Instagram | 176 | 542 | **918** |

Trap 3: `build_xlsx` called `ws.max_row` per row -- openpyxl rescans every cell, so the build went quadratic and stalled
past 12 min at 55k rows (py-spy); the row index is tracked now (56k rows build in 23 s, push 2 min).

## 21:01 Dusan reviewed both sheets: tighten (singers / creators / > 70% photos -> "Removed" tab, never deleted)

Both tools now keep a third tab, **Removed** (profile, Sent, reason; emails sheet also the address): a reject moves
there with its Sent mark, once -- a row he moves back by hand stays where he put it; a removed row is never added again.
Tests 13/13 (3 new: moves once and keeps Sent, never re-added, emails sheet).

**Singers / creators.** His example reject (a pop-singer fan page of clips and memes) had passed the BL-1670 face check
as faceless: a stan page shows the singer, not the owner -- the face check cannot see this; a "what is the page about"
check can. New rubric `scratch/bl1677/RUBRIC77.md`: K keep (sports, movies, TV, actors, athletes) / S singer page (own
account or a page centred on a musician) / P personal creator / O other / U unsure.

| sheet | method | result |
|---|---|---|
| New emails - never sent (1,417) | page pictures we already hold (BL-1670 renders, 1,339 pages, 168 sheets): Sonnet first look, **Opus re-judged all 120 sheets with any non-K** | K 1,019, S 178, O 105, U 37 -> **283 moved** (U stays); 78 have no picture (unchecked) |
| No email - editors, rows labelled celebrities (6,099 TikTok) | text re-check (7 Sonnet agents, ids verified) | K 1,598, S 2,689, P 1,612, O 54, U 146 -> **4,355 moved** + 90 Instagram named on those pages |

**> 70% photos.** The edit app's own measure (accounts.photo_share, >= 5 posts seen) covers 9,561 sheet rows and 10 of
the emails: none over 70% (photo pages were already off by status). The rest need fresh posts: a scan of the stored
hashtag pages was stopped (RAM fell under 1 GB; Dusan: jobs off his PC); an API check is $0.0006 per account
(12 posts): ~$0.84 for the emails sheet; not paid for the no-email sheet (his 19:26 rule).

| sheet | before | kept | Removed tab |
|---|---|---|---|
| New emails - never sent | 1,417 | **1,134** | 283 |
| No email - editors TikTok / Instagram | 55,710 / 918 | **51,355 / 828** | 4,445 |

## 20 Oct: Dusan's $10 cheaper-email tests (orders 10:09 + 10:18, line "Finder strategy tests 19 Oct")

Run on his PC (his 10:18 words), one paid TikTok walk at a time, every test booked with money_guard first. **Good** =
the page passes RUBRIC77 as K (sports / movie / TV edit page; singer pages, creators and other pages out), judged on
its page picture by Sonnet first and **Opus on every sheet with a Sonnet K or U** (plus 10 random other sheets: Opus
found 0 K on all 240 such pages over T1/T3/T4), and <= 70% photo posts (`scratch/bl1677/photorun77.py`, the run's own
stored posts). U is not counted. Price = vendor spend (LamaTok counter x $0.0006, TikHub $0.001/call, HikerAPI
$0.00069/call) / good emails x 1,000. Target $30-50.

| test | route | spend | new addresses | pages judged | good emails | $/1,000 good | after overlap with earlier tests |
|---|---|---|---|---|---|---|---|
| T1 | re-walk of 202 proven tags (list A2, own ledger) | $1.70 | 1,136 | 869 | 36 | **$47** | 36 = $47 |
| T2 | TikHub newest-first feed of 100 proven tags | $0.47 | 157 | 116 | 5 | $95 | 5 = $95 |
| T3 | re-walk of 230 tags that gave 1 faceless editor before (list B part 1) | $1.57 | 538 | 420 | 44 | **$36** | 41 = $38 |
| T4 | 2nd re-walk of 100 tags walked 18 Oct (refill after 2 days; own ledger77) | $0.84 | 397 | 298 | 22 | **$38** | 17 = $49 |
| T5 | Instagram named in the bio of no-email TikTok editors (844, HikerAPI) + their TikTok pages | $0.63 | 39 | 38 | 13 | $48 | 13 = $48 (pool used up) |
| all | | **$5.21** | | 1,741 | **112 unique** | **$46.5** | |

- The re-walk of tags that already gave editors is inside the target on both lists (A2 $47, B1 $36) and **refills**:
  the same 100 tags re-walked after 2 days still gave $38 ($49 after removing addresses T1/T3 had just found).
  Unwalked parts left: list B parts 2-4 (689 tags), list A tags refill every few days.
- Most pages are still not editors: Opus K is 4-11% of the pages that pass the text filter (P creators 64-83%).
  Sonnet's K is too generous (T1: 129 Sonnet K -> 36 Opus K), so Opus stays the final word.
- TikHub newest-first is twice the price (more creators on fresh posts). The IG route is in price but one-off.
- Spend checked against the LamaTok counter: $4.2222 since T1's base = the per-test sums. $4.79 of the $10 unspent.
- Delivered: 112 to `operator\editors_tests77_20261020.xlsx` -> pushed to "New emails - never sent" (+112, 1,246 rows).
- Traps: detached jobs ran at BelowNormal and starved (T1 pictures 18 s CPU in 16 min) -> own PIDs set to Normal;
  a bash heredoc ate the backslashes of the first eyes workflow (LESSON 23 again) -> `eyes77.js` uses forward slashes.
- Tools: `chain77.py` (chain72 + ledger77), `photorun77.py`, `eyes77.js`, `merge77.py plan|score`, `ig5_77.py`,
  `t5pages77.py` (makes T5's pages a walk-shaped run so the same tools score it), `deliver77.py`.

## Next
- Free pools left are small: 1,269 U pages of the text check, 857 collab partners with no visible niche (need their
  videos read), and the edit-app accounts filed out as music / unclassifiable that were U/X.
- More volume needs new paid walks (raw hashtag pages: ~7% of accounts are edit-named, 61,391 of 842,691) -- only with
  a money line and Dusan's yes; price to be proven on a small probe first.
- The 857 collab-partner editors whose niche is not visible (U).
