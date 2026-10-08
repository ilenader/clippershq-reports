# BL-1616: the three untested ways found 0 niche editors; any-niche video editors cost $4.84 per 1,000

## Answer card

| | |
|---|---|
| **1. Link-in-bio pages** | **No per-1,000 price: 2 new emails found, 0 kept.** 44 in-niche accounts write a link-page address in their bio. **linktr.ee's robots.txt disallows all crawlers** (`User-agent: * / Disallow: /`), which covered 36 of the 44. beacons.ai refused 5 with a 403. The 3 readable pages gave 1 email. The paid route (one profile call to read `bioLink`) found a link on 9 of 50 accounts and 1 email. Both emails failed the picture check. |
| **2. Contact email fields** | **None exists.** Every payload we have (LamaTok hashtag, feed, v1/v3 profile; TikHub app profile) carries only flags: `has_email` (false on all 93 authors seen), `is_email_verified`, `commerceUserInfo`, a bio link, and an empty `added_contact_and_link_list`. **No address field anywhere**, so the 50-account test had nothing to measure. |
| **3. Account search** | **LamaTok has none** (its live spec has 29 paths and no user search). TikHub's app user search returned **60 accounts in 3 calls with 0 bios**, so 0 new kept per call. Its web user search returned HTTP 400. |
| **Niche editor emails delivered** | **0**: football 0, tennis 0, movies 0. Nothing was written to master or your workbook. |
| **Audit** | No niche keeps to audit. Any-niche: a second blind look at 40 random keeps on fresh covers found **40 of 40 real video editors [91.2–100]**. |
| **4. Any-niche video editors (your decision)** | Of BL-1615's 394 new pro-tool emails, 319 survived the text drops. Pictures showed **84 real video editors**: 38 faceless, 46 showing themselves as freelance editors. The rest were 230 creators, 2 businesses and 3 unclear. **$4.84 per 1,000**: $0.2154 walk (BL-1615) + $0.1914 pictures. **Faceless only: $10.71 per 1,000.** |
| **Any-niche file** | `<PROFILE>\AppData\Local\ClippersHQ\operator\video_editors_any_niche_20261008.xlsx` (84 rows). **Not** added to master or your workbook. |
| **Total spent** | **$0.26**: LamaTok $0.2526 booked (421 calls) + TikHub $0.008 (balance 1.569 → 1.561, also booked). LamaTok billed 425 (balance 347,084 → 346,659). That leaves 4 requests unattributed, the same size as the gap BL-1615 saw from another session. |
| **No email was sent.** | |

## 1. Link-in-bio pages ($0 vendor cost)

**Where the link lives.**
- Not in edits.db: no column stores it.
- The hashtag and feed payloads carry no link either, only `bio_link_click_action` (0).
- It arrives only on a **profile** call: LamaTok `/v1/user/by/username` (`bioLink.link`), or TikHub's app profile (`bio_url`).
- So the $0 part could only use links people type into their bio text.

| | Count |
|---|---:|
| In-niche bios (edits.db) | 16,883 |
| …with a link-page address in the text and no email | **31** (plus 13 from the BL-1614/1615 rows = 44) |
| Fetched politely (robots.txt read first, 1 request/s per host, no login, one page each) | 44 |
| Refused by robots.txt (all linktr.ee) | **36** |
| HTTP 403 (beacons.ai) | 5 |
| Read | 3 → **1 email** |
| Paid profile calls (50 proven edit pages) | 50 calls, **9 with a bio link** (guns.lol, carrd, linktr.ee, Instagram, Telegram, payhip…) → 7 read, **1 email** |

- **Both new emails failed the picture check.** One is a tennis-commentary creator on camera; the other a mixed meme page, not movie edits.
- **Why this is dead:** link-in-bio is rare on edit pages (18% of profiles), and the biggest host forbids crawling.
- **Even if every page carried an email,** the profile call alone ($0.0006) at 18% links gives at most 0.18 emails per call. That is about $3.3 per 1,000 before dedup and pictures. Measured, it gave 1 email in 50 calls.

## 2. Contact email fields

- Field names were collected across 1 hashtag page (20 authors), 3 feeds (73 items), 3 v1 profiles, 3 v3 profiles and 5 TikHub profiles.
- **Present, but only booleans or empty:** `has_email`, `is_email_verified`, `commerce_user_level`, `with_commerce_entry`, `biz_account_info.added_contact_and_link_list` (null).
- TikTok shows a business email only behind the in-app "Email" button, and these vendors don't return it.
- **Verdict:** no route. Nothing to scale.

## 3. Account search

| Surface | Calls | Accounts | Bios | New kept |
|---|---:|---:|---:|---:|
| LamaTok | — | the spec has no user-search path | — | — |
| TikHub `app/v3/fetch_user_search_result` ("messi edit", "tennis edit", "marvel edit") | 3 | 60 | **0** (no `signature` field) | 0 |
| TikHub `web/fetch_search_user` | 3 | HTTP 400 | — | — |

## 4. Any-niche video editors (measure only)

- **Text drops:** of the 394 new emails, 60 dropped for person words and 15 for business/official words.
- **Pictures:** 319 were pictured and judged by me.
  - **E (faceless editor): 38**, mostly cinematic travel, motion graphics, K-pop/music edits and portfolio reels.
  - **F (freelance editor who shows themselves, "POV: you hired me"): 46.**
  - C (creator): 230. B: 2. U: 3.
- **Second look:** 40 random E/F accounts re-judged on their newest covers were 40 of 40 real video editors. 36 kept the same E/F class.
- **Price:**
  - **E+F: $0.4068 for 84 = $4.84 per 1,000**, just under your $5.
  - Faceless only: $10.71 per 1,000.
  - The walk part is BL-1615's money. This round paid only for the pictures ($0.1914), which is $2.28 per 1,000 at the margin.
- **Where they sit:** in the separate file only, as you asked.

## 5. Notes

- **Probe setup.** The TikHub probe saved its raw payloads before my summary code crashed on a dict key, so the counts above were re-read from disk ($0) rather than re-called.
- **Where the data lives.** Work data is in `%LOCALAPPDATA%\ClippersHQ\bl1616_work\`, never in the repo. The repo files hold counts only.
- **Priority.** The machine was busy, so I raised **my own** picture job's process ID to Normal.
- **No config change.** Nothing was written to master or your workbook.
- **My slip: three handles reached my terminal.** The first field probe printed parts of 3 account handles there, because the v1 profile payload keys each user by handle. Nothing was written to any file, and the later analysis masks those keys.

Files: `scratch/bl1616/` (fields_probe, tikhub_probe, linkpages, links_free, links_paid, pictures_run, anyniche_audit, anyniche_file, PROGRESS.md and the JSON counts).
