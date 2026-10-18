# BL-1670 -- overnight 17->18 Oct: strict faceless check on the old lists done; the paid run never started (no wallet line); free routes closed

Order: office 1_LEADS 2026-10-17_2241 (ALFRED for Dusan, HELM 22:41): leads by 09:00, test cheaper routes (movies ->
TV -> sports), Claude screenshot check keeps ONLY faceless editors (99 % right, zero creators), the same check on the
existing lists, up to $30 hard cap. Dusan's own words (HELM 17 Oct 22:39:48): "if you don't get cheap enough, then just
spend $30 anyway". **Spent: $0.** Counts only -- no handle, name or email here.

## Result in one line
Old lists cleaned (1,355 accounts moved out); no new paid leads, because money_guard refused all night: wallet.json
never got a budget line for this run (only MILOJE/ALFRED writes budgets; asked 00:24, again in the reply 02:55 / 03:58).

## 1. Faceless check on the existing lists (point 4) -- done 00:30 ($0)
- 3,680 pages the eyes had called EDITOR, each re-rendered from its own run's store (avatar, bio, up to 12 covers),
  8 per sheet, judged by Opus with scratch/bl1670/RUBRIC.md (F faceless editor / C own face / B business / X other / U unsure).
- Kept 2,295 faceless (62 %). Moved out: 326 own face, 709 unsure, 286 not faceless editors (anime/game/other), 64 businesses
  = 1,355 accounts, 2,627 rows in 129 lead files -> a "Moved out (face check)" sheet in the same file with the reason;
  backups first (operator\backups\bl1670\). Commit b12a04b9.
- NOT touched: his workbook clipper_emails_ALL.xlsx (add-only); 1,353 of its rows are these accounts -- needs his word.

## 2. Paid run (points 1-3, 5) -- staged, never started
- Measured run length: one chunk = 10-27 min walk + 15-35 min eyes; BL-1663's 4 chunks took 1 h 50 -> start by ~06:45 for 09:00.
- Staged: `bash scratch/bl1670/paid70.sh 4` = money_guard books $4 on "Finder overnight 18 Oct" (refuses with no line)
  -> LamaTok counter base -> detached `bl1670_chain` (chain70.py: one paid walk at a time, limit = the booked amount):
  movies 40/40/39 named movie/TV tags (cap $0.60 each), sports 39 ($0.50), 6 fresh current titles ($0.20).
- New eye step (eyes70.js, built by mk_eyes70.py): Haiku -> Sonnet re-check -> **Opus strict faceless look on every sheet
  still holding an E**; an E stays only when Opus says F (C -> C, B -> B, else U). Mock test: 1F kept, 1C removed.
- Wallet note: money_guard shows $29.47 left on the old "Finder leads" line, but only $0.53 of its spend was booked
  there; the LamaTok counter says $29.36 of that $30 is spent. That line must not be read as money.

## 3. Cheaper routes tested tonight ($0)
| route | result |
|---|---|
| Collab partners of proven editors (BL-1669 free read, 9,905 accounts, 07:33) | 8,492 read, 492 with an email, **368 new**, 56 of them look like edit pages; 1,197 no-email edit pages -> "no email yet" list (11,296) |
| Face check of those 368 without a vendor | **closed**: headless profile page = slider CAPTCHA (also with the read stopped), /embed/@ = "overload-protect". Not worked around. Covers via the paid vendor ~ $0.0006 a call once a budget exists. |
| ALFRED LAB idea: "edited by @" in Video Downloader's .info.json | **0** -- it keeps only 8 .info.json; its logs are YouTube sports clips |
| New movie / TV titles of October 2026 | 15 of 21 current big titles were already in walked or staged lists; 6 fresh (staged, $0.20) |
| Username tools / Osintgram / free lookups | already 0 in BL-1667 |

## What we learned
- A budget the owner gave in chat is not money until the wallet holds it; nothing reads money_requests.md, and a
  BLOCKED reply only reaches ALFRED once the order moves to read\. Ask on line 1 of the reply AND move the order.
- TikTok profile pages always show a slider CAPTCHA to headless Chrome from this PC; the SSR user JSON (bio, links)
  still reads fine. Covers for a face check need the vendor (or the eyes pipeline's CDN covers from a paid walk).
- The big new titles are already mined: the fresh-title pool is ~6 tags, not a lever.

## Files
- scratch/bl1670/{partners70.py, shots70.py, chain70.py, process70.py, eyes70.js, mk_eyes70.py, done70.sh, paid70.sh}
- work data: %LOCALAPPDATA%\ClippersHQ\bl1670_work\ (partner_cands.json, c70_*.tsv, verdicts70.json)
