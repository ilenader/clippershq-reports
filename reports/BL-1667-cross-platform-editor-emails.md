# BL-1667 -- More emails for editors we already found: username tools, Osintgram, Instagram, collab partners

Orders: office 1_LEADS 2026-10-17_1449 (learning day, <= $10 per 1,000 real emails), 1450 + 1642 (Osintgram),
1456 + 1515 (Aliens Eye vs Sherlock vs Maigret, collabs), 1808 (more ways). **Spent: $0.19** (Osintgram $0.12 +
Instagram lookups $0.07, both HikerAPI, both booked in money_guard on "Finder leads": now $29.36 of $30.00).
Counts only -- no handle, name or email here.

## The test set
Proven editors = accounts with >= 1 video in the approved library (5,126). Random sample, seed 1667:
**A** = 40 WITH an email in the TikTok bio (the truth: does a tool re-find the right address?),
**B** = 60 with NO email (where a find would be new).

## Results
| route | cost | A: right / wrong | B: real new emails | verdict |
|---|---|---|---|---|
| Same handle on 6 sites (Linktree, Beacons, bio.link, YouTube, Behance, SoundCloud) | $0 | 4 right / 0 wrong | **0** | only re-finds the bio link |
| Aliens Eye (500 sites) | $0, ~2 h for 100 | 5 right (all Linktree) / 3 wrong | **0** (10 "hits" = 7 addresses: 4 are the site's own, 2 repeat across editors, 0 personal mail) | not adopted |
| Maigret (top 500 sites) | $0, ~2.2 h | 0 / 0 (15 hits were TikTok copy sites) | **0** | not adopted |
| Sherlock (400 sites) | $0, ~1.7 h for 40 | 2 right / 17 wrong | **0** (19 "new" came from a forum and a blog host's own pages) | not adopted, false matches |
| Osintgram 2.0 (HikerAPI, no login): accounts 5 proven editors FOLLOW | $0.12 (179 calls) | -- | 3 emails in 108 profiles, **0 editors** | not adopted |
| Osintgram: their FOLLOWERS | (in the $0.12) | -- | 0 in 50 (fans, 18 private) | dead |
| Instagram profile of proven editors who name their IG in the TikTok bio (105) | $0.07 (105 calls) | 10 of 20 found have an IG email | **3** new (of 78 found) + 2 extra addresses for A | **$14.50 per 1,000** -- best price, tiny pool |
| Collab partners: accounts proven editors @tag in captions, never read (9,905), free headless read | $0 | -- | 4 emails in 133 read, **3 new**, 1 of them an edit page; 22 of 133 look like edit pages | free top-up, ~14 new emails/hour, ~4 editors/hour |

## What this means
- **Username tools do not find editor emails.** Editors use a fresh handle per page; the same string elsewhere is
  another person or a site's own address. Every correct re-find was the Linktree the TikTok bio already links to,
  and the free bio-link read (BL-1665) does that already.
- **Graphs of an editor are not editors** -- on Instagram (following 7 of 108 edit-like) as on TikTok (BL-1662).
  Price floor of any graph scan = call price / email rate: $0.0007 / 2.8% = ~$25 per 1,000 before the editor cut.
- **Osintgram's useful parts already exist in Finder**: suggested accounts (crawl_suggested.py), contact-button
  email + phone (BL-1666), request cache (resolve_cache). Nothing to plug in.
- **Instagram of the proven editors** is the only route under $15 per 1,000, but only 105 of 5,126 proven editors
  name an IG, so it yields ~5 addresses. Store accounts that name an IG (~1,000, BL-1665) are not proven editors,
  so their price would be higher; not run.
- **Collab partners** read free at ~4.7 s each: ~2.3% new email, ~1 in 6 edit-like. 9,905 waiting = ~220 new emails,
  maybe ~75 editors (from 1 in 3 -- an eye check decides), at $0 -- a night job, not a price change. Not started:
  today is a learning day (no lead runs).

## Price per 1,000 real editor emails (today's measured routes)
| route | $ per 1,000 |
|---|---|
| best current walk list (BL-1663, all countries) | ~$14 |
| Instagram of proven editors | $14.50 (pool ~5) |
| collab partner read (free) | $0 (pool ~9,905 partners, few editors) |
| Osintgram following / followers | > $120 (0 editors) |
| Aliens Eye / Maigret / Sherlock / same-handle sites | no real email found |

The $10 per 1,000 target is not reached by any route tested. The cheapest real lever stays tag selection before
the walk (BL-1663/1665).

## Files
scratch/bl1667/: sample67.py, run67.py, conv67.py, xmatch67.py, collab67.py, osint67.py, ig67.py, partners67.py,
covers67.py. Tools installed only under %LOCALAPPDATA%\ClippersHQ\bl1667_work\{tools,venvs}, each in its own venv,
run from a helper folder, no logins. Per-account rows stay in bl1667_work.
