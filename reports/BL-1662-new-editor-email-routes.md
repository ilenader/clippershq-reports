# BL-1662 -- new ways to get REAL editor emails: 7 routes tested, ranked

Order: office 1_LEADS 2026-10-17_1013 "Main goal is more emails of real" (ALFRED for Dusan, HELM chat 10:12): more emails
of real video EDITORS (football + every sport, movies, TV, history, plain editors), new ways, ranked by usable emails,
inside Dusan's budget. Money: no new $ figure, so the cap = the $3.34 left of Dusan's 16 Oct $30 (stop at $3.20).
**Spent: ~$0.37** (LamaTok 177 requests = $0.106 by the counter, 147,355 -> 147,178; TikHub ~260 calls at $0.001 = ~$0.26).
Counts only -- no handle, name or email here.

## How each route was judged
Every route's accounts WITH a new email went through the usual pipeline (raw_pages filter -> feeds -> covers ->
pictures -> 8-page sheets) and were **eye-checked by hand** (E = faceless edit page of real people / live-action
characters / history / cars). "$ per 1,000 editors" = the route's spend (walk + feeds) / editors found x 1,000.

## Results (small tests, 27-45 pages checked each)
| # | route | test spend | accounts with a new email | eye-checked | editors (E) | $ per 1,000 editors |
|---|---|---|---|---|---|---|
| 0 | **Hashtag walk on small edit tags** (existing, BL-1649/1656) | - | - | 1,000s | 28-50% of email pages | **~$33-43 first world (sports / clippers); movies/TV ~$72** |
| 1 | Sounds that confirmed editors used (TikHub music video list, 13 sounds) | $0.069 | 32 | 28 | 2 (7%) | ~$35, but n = 2 |
| 2 | Sounds from music search "football/movie/nba edit audio" (9 sounds) | $0.052 | 33 | 27 | 1 (+1 game, +1 art) | ~$52 |
| 3 | TikTok "similar accounts" of 30 confirmed editors (TikHub) | $0.076 | 33 | 27 | ~1 (+1 unsure) | ~$76 |
| 4 | Account search "football / movie / nba / ufc / history edits" + 1 profile call each | $0.098 | 1 of 93 profiled | - | <= 1 | ~$100 |
| 5 | Accounts that 20 movie editors FOLLOW (LamaTok following list) | ~$0.05 | 52 | 45 | **0** | none |
| 6 | Video / general search ("messi edit") | 5 calls | - | - | - | impossible: results carry **no bio** |
| 7 | Same handle on Instagram | not re-run | - | - | - | dead: tested Jul 2026, 1-6% email hit |

## What we learned
- **Only the hashtag walk concentrates editors.** On small edit hashtags 28-50% of the email pages are editors; every
  new route sits at 0-7%. Editors follow big creators (not other editors); TikTok's "similar accounts" are matched by
  audience, not by page type; popular sounds belong to everyone.
- **Editors rarely put an email in their bio**: 1 of 93 accounts named "...edits" had one. So a route is only cheap
  when the bio comes FREE with the list (hashtag pages, sound lists, following and similar lists do; search does not).
- The "editor-only sounds" ranking was noise: 3-of-3 samples. Rank a signal on a count with a minimum sample.
- Sound lists DO carry bios and are email-dense (6 of 11 on one page) -- the route would only work with sounds used
  almost only by editors, and we found no way to pick those reliably.

## Ranking (best first, usable editor emails per $)
1. **Hashtag walk on small edit tags** (sports/football + clippers ~$33-43 per 1,000 first world; movies/TV ~$72). Still the best.
2. Free bio-link pass on editors we already hold (BL-1657): $0, ~20 candidate emails/hour, small pool.
3. Editor sounds (#1/#2 above): ~$35-52 per 1,000 on 1-2 editors -- not proven better, 5x more eye-check work.
4. Similar accounts, account search, following lists, video search, Instagram: dead.

## Not done
No new lead file (the tests found ~4 editors, not worth a file). The rest of Dusan's $30 (~$2.97) is untouched.
Tools (scratch/bl1662/): follow62.py, similar62.py, tikhub62.py (sound walk), soundids62.py (fast music-id lookup),
usersearch62.py, sound62.py. Runs: raw_emails f62_movies_t1, s62_mix_t1, snd62_t1, snd62_t2.
