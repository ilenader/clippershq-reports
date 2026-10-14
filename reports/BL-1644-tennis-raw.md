# BL-1644: TENNIS raw run. 634 new tennis emails for $1.30 ($2.05 per 1,000), but only 29 are editors: tennis bios with an email are mostly creators

## Card

| | |
|---|---|
| **Honest line** | **634 new tennis emails for $1.298 = $2.05 per 1,000**, balance-checked. By eye on their page pictures: **29 EDITORS, 502 CREATORS, 100 UNSURE**. Raw mode is cheap; the people it finds on tennis tags are mostly creators. |
| **Where the editors are** | **Player-name tags** (sinneredit, alcarazedit, federeredit…): 135 emails, **23 editors (17%)**; surname tags alone 10 of 27. **Generic tennis tags** (tenniscore, tennistiktok, tennisedit…): **453 emails, 3 editors**. Those are tennis-fashion and lifestyle creators, coaches, players. **#tenniscore alone gave 400 of the 634 emails and 1 editor** (it is a fashion tag); #tennistiktok 47, 0 editors. Most editors per tag: naomiosakaedit 3 of 9, rublevedit 2/2, williamsedit 2/2, felixedit 2/2. |
| **Slices** | LamaTok v1 + v2 squeezed **every** tag: 590 new for $0.870 (**$1.47 per 1,000**); v2 went deep and bought 399 of them. TikHub's newest-first feed as a third slice: 44 new for $0.428 (**$9.7 per 1,000**), not cheap; it was stopped at its $0.60 test cap. |
| **Kept, all of it** | Every page bought (v1, v2, TikHub): raw JSON in `%LOCALAPPDATA%\ClippersHQ\raw_store\20261014\` (gzipped), plus every account's posts (cover, caption, hashtags, plays, date, music) and author block. Covers + avatars downloaded free from the CDN. |
| **Page pictures** | **631** in `operator\tennis_pages_20261014\<n>.jpg` (no handle in the file name) + `index_tennis.xlsx` / `index_tennis_tikhub.xlsx`. **Only 30 of 631 accounts have 4 or more covers**: a hashtag page carries only the account's posts on that tag (1.4 on average). No cover was bought. |
| **Free judge** | The Video Downloader's `page_judge.py` (free, local) ran on every picture. It agreed with the eyes on **10 of 21** pages with 4+ covers, and calls an empty picture "faceless = EDITOR", so **it cannot decide here**; it is kept as a second opinion only. The verdicts are Claude eyes (6 sub-agents + me, $0 vendor; my spot-checks of 3 sheets agreed). |
| **Files** | `operator\tennis_raw_emails_20261014.xlsx` (all 631 accounts, verdict + picture number), `..._EDITORS.xlsx` (29, + sheet "Unsure" 100), `..._CREATORS.xlsx` (502). Master has 631 rows, `lead_kind raw_edit_hashtag`, niche tennis, the verdict on every row. Workbook sheet "Raw" +631. |
| **Money** | **$1.298 of $5.00**: LamaTok 1,450 requests $0.870 (vendor counter = meter) + TikHub 428 calls $0.428 (balance). It stopped early because every tag was walked to its end. |

## Your decisions

| | Question | My recommendation |
|---|---|---|
| A | Keep only the 29 editors, or also the 502 creators? | Your rule: creator = reject. The 502 are in their own file in case another product wants them. |
| B | Want more tennis editors? | **Walk more player-name tags, not generic ones**: 17% editors vs under 1%. The top-100 ATP/WTA names, plus the player tags found in the captions we just bought (the free id store grew by 11,000+ tags), would be the next list. Expect about $1.5–3 per 1,000 emails and about 1 editor per 6 emails. |
| C | Real page pictures (12 covers)? | One paid call per account to its own video feed (about $0.0006 each, **about $0.38 for these 631**) would fill every picture. Not done: you said not to buy more. Only needed if the 100 UNSURE matter to you. |

## 1. Asked

1958 (P0): tennis only, today's ATP + WTA top 20 + the big names, as `<name>edit`, `<first>edit`, `<surname>edit`, `<name>edits`, `<name>tennisedit` (only tags that exist) + generic tennis edit tags. Squeeze each tag on v1 AND v2 to saturation, TikHub as a third slice if cheap, every new email, own file, master rows, cap $5.
2012 (P0 addendum): store everything bought; covers free for every new-email account (note when fewer than 4, buy none); one page picture per account; creator vs editor, the free local script first, else Claude eyes; three files.

## 2. Tags

`scratch/bl1644/tennis44.py`. Players: ATP top 20 of 5 Oct 2026 (Sinner, Zverev, Alcaraz, Shelton, Medvedev, Auger-Aliassime, Cobolli, Tiafoe, de Minaur, Fils, Djokovic, Fritz, Jódar, Vacherot, Menšík, Tien, Paul, Nakashima, Lehečka, Cerúndolo) + 10 editors' favourites. WTA top 9 of 12 Oct 2026 (Rybakina, Sabalenka, Andreeva, Pegula, Gauff, Svitolina, Muchová, Nosková, Świątek). Places 10–20 could not be confirmed from the web results, so the usual names around there were added. 14 legends. 23 generic tags. Plus edit-app tennis caption tags that carry a name.
328 candidate forms → 23 skipped (both endpoints already finished) → **196 walked**: 127 known to exist (73 with a free id) + 69 likely forms that cost one lookup each. **33 of those 69 do not exist** (billed lookups, $0.02).

## 3. The walk (LamaTok, balance-checked)

| | v1 | v2 (deep, richest v1 tags first) | total |
|---|---|---|---|
| tags | 196 | 195 | |
| pages | 778 | 436 | 1,214 (+ lookups) |
| new emails | 191 | 399 | **590** |
| billed requests | | | 1,450 = **$0.870** |

- v1 was walked to its end on every tag. v2 had a $10/1,000 line: stop after 5 pages with no new email, from page 3. 31 v2 tags stopped on it; one hit the page ceiling.
- **20:50 the vendor reset connections on 4 lanes** (`ConnectionResetError 10054`, 3 tries each, 28 of 33 tags gave up). Reset calls are **not billed** (96 metered, 67 billed). Restarted on 2 lanes: 0 resets in 1,380 requests. The failed tags were walked again (an error stop is never "finished").
- Each v1 page is about 800 KB; the line was slow (about 3 s per page).
- Fixed on the way: a looked-up tag id is now remembered for the v2 walk, and a tag v1 could not resolve gets no v2 walk. This run bought about 64 lookups twice ($0.04) before the fix.

## 4. TikHub (third slice)

`raw_emails.py tikhub`: `fetch_tag_post`, newest-first, 30 items, bios present. 129 tennis tags with a known id, richest first. Stop a tag after 2 pages with no new account or 3 calls with no new email. **428 calls = $0.428 (balance), 44 new emails = $9.7 per 1,000**; 3 of 43 accounts are editors. Not cheap; it was not extended.

## 5. Page pictures and the creator / editor split

- Covers: 1,441 + 86 downloads, 1,437 + 86 OK (links valid about 47 h). Byte-identical covers are shown once: the same video re-posted months apart was common.
- `page_judge.py` (Video Downloader, OpenCV faces): loaded from its project **read-only**, with its model folder in `%LOCALAPPDATA%\ClippersHQ\page_judge_models`, so nothing is written into their folder on the Desktop. Script: EDITOR 527, UNSURE 88, CREATOR 16; against the eyes 10 / 21 on 4+ cover pages. **Not usable on 1–2 covers.**
- Eyes: 80 sheets (8 pictures each) → `raw_emails\<run>\eyes\`. Rubric: E = edit / clip / fan page about famous people, owner never shown; C = the owner in their own videos (players, coaches, tennis-fashion, lifestyle, hosts); U = brand / shop / app / unclear. 74 sheets by 6 Sonnet sub-agents (the order allowed sub-agents), 6 by me. Sheets s0001, s0026 and s0068 re-checked by me: all agree.

| tag group | new emails | EDITOR | CREATOR | UNSURE |
|---|---|---|---|---|
| ATP names | 66 | 12 | 40 | 14 |
| WTA names | 60 | 6 | 43 | 11 |
| legends | 28 | 8 | 14 | 6 |
| generic tennis | 477 | 3 | 405 | 69 |
| **all** | **631 accounts** | **29** | **502** | **100** |

## 6. Delivered

| | count |
|---|---|
| `operator\tennis_raw_emails_20261014.xlsx` (verdict, picture number, why) | 631 accounts / 634 addresses |
| `..._EDITORS.xlsx` "Editors" / "Unsure" | 29 / 100 |
| `..._CREATORS.xlsx` | 502 |
| master rows (raw_tennis 588 + raw_tennis_tikhub 43), verdict set | 631 |
| workbook "Raw" sheet (MARK untouched, vaulted) | 85 → 716 |
| page pictures `operator\tennis_pages_20261014\` | 631 |

No email was sent. `raw_edit_hashtag` is not a send kind.

## 7. Code and tests

- `email_harvester.py`: `raw_sink` (every page payload, before parsing; a sink error never fails a walk), `price_line_endpoints` (v2-only line), v2 follow richest-first, lookup reuse, no v2 for a tag v1 could not resolve.
- `raw_emails.py`: `RawStore` (`--raw-store`), `tikhub`, `deliver --file-prefix --verdicts` (split files, verdict in master).
- `raw_pages.py` (new): `covers`, `pictures`, `judge`, `sheets`, `verdicts`.
- `tests/test_bl1644_raw_pages.py` (12): every page reaches the sink; a broken sink does not fail a walk; store keeps pages and posts and reloads; v1 to its end when the line is v2-only; v2 richest first; one lookup per tag, none of v2 for a ghost tag; the picture is profile-sized with the avatar top-left; stable numbering; the judge is loaded with OUR model folder; eyes decide, unanswered = UNSURE.
- `tests/run_all.py`: see the BL-1643 report §7 (one run for both rounds).

- 22:25 FINDER BL-1644 TENNIS raw: 634 new tennis emails for $1.30 ($2.05/1k); by eye 29 editors / 502 creators / 100 unsure; player tags 17% editors, generic tags under 1%; 631 page pictures (DONE)
