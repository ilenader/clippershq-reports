# BL-1613 — Forecast: TikTok editor emails for football, tennis and movies

Read-only. **$0 spent.** The only network call was the free LamaTok balance read. All figures are counts.

## ANSWER CARD

1. **Free now ($0):** 239 new editor emails are already in the edit app's bios: **football 94, tennis 82, movies 63**. 154 of them posted in the last 7 days. None are in master_leads.csv or your workbook (checked by address and by account).
2. **Nearly free:** about **170 more** for about **$7 and 1 hour**. The app has found 11,448 accounts it never opened; fetching their bios would add these (an upper estimate).
3. **Paid, per 1,000 new clean emails** (phrase search "&lt;name&gt; edit"): **football ≈ $81 / 53 h, tennis ≈ $59 / 23 h, movies ≈ $147 / 99 h**. The cheapest paid route ignores niche: pro-tool hashtags (#aftereffects and similar) at ≈ $7.43 / 7.4 h, but nobody has proven there are enough fresh tags left.
4. **Reachable:**
   - **24 h:** ≈ 900 emails (239 free + 170 bios + 180 tennis + ≈ 350 football) for ≈ $47.
   - **7 days:** ≈ 1,500 emails, until all three name packs run dry, for ≈ $115.
   - **With today's app caps ($5 a day):** ≈ 800 in 7 days for ≈ $35.
5. **Recommended order:** the free 239, then the bios, then tennis (cheapest, runs dry at ≈ 180), then football (≈ 580), then movies last (≈ 340, most expensive).
6. **Decide or fix first:**
   - This PC is **paused for the move**, so every run is refused. Finish the move, or press Resume.
   - Nothing yet copies edit-app bio emails into master or your workbook. Say yes if you want that built.
   - Approve the movie pack below.
   - Raise the edit app's $5/day cap if you want the 7-day number.
   - Do **not** use the craft cut on these accounts.

## 1. Free emails already in the edit app (edits.db, 43,920 accounts)

Emails are read with the repo's own extractor (`bio_parser.extract_emails`). **New** means the address is not in master_leads.csv (16,293 addresses) or either copy of clipper_emails_ALL.xlsx (4,246 addresses), **and** the account is not there either (61,797 + 26,763 TikTok accounts). Club and brand accounts are excluded.

Movies = the app's superhero + marvel accounts. The app has no movie niche; other movie pages are marked out of scope.

| | Football | Tennis | Movies |
|---|---:|---:|---:|
| Accounts in the app | 11,100 | 5,691 | 13,608 |
| Bio contains an email | 229 | 137 | 331 |
| … of those, new to master + workbook | 121 | 107 | 108 |
| … and inside your 5 niches (the scope rule) | **94** | **82** | **63** |
| … posted in the last 7 days | **62** | **52** | **40** |
| You said **YES** (your own swipe) | 0 | 0 | 0 |
| You said **NO** | 0 | 0 | 0 |
| Auto-YES (the app's "proven" rule) | 38 | 24 | 18 |
| Never swiped | 56 | 58 | 45 |
| Out of scope (excluded above) | 27 | 25 | 45 |

- **Your swipes:** across the whole database you have answered 2 accounts NO and approved 8 videos. All 3,539 YES accounts were approved automatically by the "proven" rule, not by you.
- **Across all niches:** 485 new addresses.

## 2. The paid way

**How it was measured.** The edit app's own counters (edits.db `terms` and `runs`: 38,898 calls, $23.34) give how many new accounts each kind of search word brought. BL-1599 gives cost per account by niche: football $1.06, tennis $1.76, marvel $1.03 per 1,000; 0.69 h per 1,000 at 8 lanes. **New in this round:** the email rate per account the app has opened, which BL-1599 never measured:

| | Football | Tennis | Movies |
|---|---:|---:|---:|
| New in-scope email per opened account | 1.31% [1.1–1.6] | 2.96% [2.4–3.7] | 0.70% [0.5–0.9] |
| **$ / hours per 1,000 new clean emails** | **≈ $81 / 53 h** | **≈ $59 / 23 h** | **≈ $147 / 99 h** |
| Search words not yet used | 746 | 337 | 926 |
| Accounts left before the words run dry (est.) | ≈ 44,000 | ≈ 6,200 | ≈ 49,000 |
| **Emails left before dry** | **≈ 580** | **≈ 180** | **≈ 340** |
| Cost / time to run dry (8 lanes) | ≈ $47 / 31 h | ≈ $11 / 4 h | ≈ $50 / 34 h |
| Bio fetch for never-opened accounts | 3,921 calls, $2.35, ≤ 51 | 2,922 calls, $1.75, ≤ 87 | 4,605 calls, $2.76, ≤ 32 |
| Old hashtag walks (BL-1563/64), per 1,000 craft KEEP | $71–227 (only 4–11 KEEP) | never walked | $17–64 |

- **Best sources.** Phrase search "&lt;name&gt; edit" is the main source. Mined terms come next: 1.24× more accounts per $ (BL-1601). Pro-tool tags are best per email ($4.01 / 4.1 h per 1,000 KEEP over 13 tags, $7.43 / 7.4 h over the whole walk), but they don't target a niche, and the four big tags are already spent (BL-1584).
- **Tennis is nearly dry.** All 43 of its "&lt;name&gt; edit" words are retired, and its bigger pack yields only 24 new accounts per word.
- **"Clean" here** means new, in scope, and not a club or brand account. The craft cut is not applied (see section 3).
- **Uncertainty:** the 24 h and 7-day totals are estimates. Account supply per unused word is taken from words already used (bigger-pack names are less famous). Each email rate carries the interval shown.

### Proposed MOVIES pack (60 names, for your approval; nothing changed)

- **Already searched by the app (34):** Spider-Man, Iron Man, Captain America, Thor, Hulk, Black Widow, Avengers, Thanos, Loki, Deadpool, Wolverine, Doctor Strange, Black Panther, Guardians of the Galaxy, Venom, Batman, Joker, Superman, Wonder Woman, The Flash, Aquaman, Harley Quinn, Robert Downey Jr, Chris Hemsworth, Chris Evans, Tom Holland, Ryan Reynolds, Hugh Jackman, Margot Robbie, Scarlett Johansson, Zendaya, Christian Bale, Heath Ledger, Henry Cavill.
- **New (26):** Star Wars, Darth Vader, Harry Potter, Lord of the Rings, John Wick, Fast and Furious, Transformers, Jurassic Park, Mission Impossible, James Bond, Pirates of the Caribbean, Top Gun, Interstellar, Oppenheimer, Dune, Avatar, Godzilla, The Matrix, Brad Pitt, Leonardo DiCaprio, Tom Cruise, Keanu Reeves, Timothée Chalamet, Cillian Murphy, Johnny Depp, Dwayne Johnson.
- **Note:** the app's scope rule marks non-superhero movie pages as *other movies/shows* (out of scope). The 26 new names need a MOVIES niche in scope, or their accounts will be filtered out.

## 3. Editors, not creators

- **The craft cut today** (BL-1585): about **21% of editors lost** [14.5–29.7], measured on 109 labels; about **8% creators leak through** on TikTok [3.2–18.8], from 4 of 50 of your grades. Both were measured on hashtag-walk rows.
- **On the edit app's accounts, the craft cut does much worse.** Test set: 187 proven edit pages that have an email (active, with 2+ viral posts found by "&lt;name&gt; edit").

| Filter | Keeps | Of the 187 proven edit pages |
|---|---:|---|
| Craft cut (bio rule) | 53 | **28% [22–35]** — it throws away 72% of them |
| Name or bio rule | 68 | 36% [30–44] |
| **Edit app caption signal** (half of captions are edits) | 144 | **77% [71–83]** |

- **Why:** faceless edit pages rarely describe themselves as editors in their bio, so a bio rule cannot see them. Their captions show it. For edit-app emails, the caption signal is the better filter.
- **Your swipes cannot measure creator leakage yet.** There are only 2 NO swipes. About 100 graded accounts would measure it.

## 4. Can it run today?

- **LamaTok key: works.** The free balance read returned **$211.41**. The key has still not been rotated; the new key is for the new PC.
- **Tests:** **ALL GREEN**, 22 of 22 suites, 1,119 checks, run sandboxed through run_all. This covers the TikTok funnel (test_funnel 815 checks, wiring, resilience, editor filter, email harvester, cursor stride, dedup, craft cut, caps, zero-cap guards, preflight) and the edit app's search, engine and parked runs.
- **Blockers:**
  1. **This PC is paused for the move** (Prepare to move, 16:16). It is still the main PC, but the edit app refuses every run until you press **Resume runs on this PC** or finish the move.
  2. **No path** copies edit-app bio emails into master or your workbook.
  3. **Edit app caps:** $3 per run, $5 per day, $60 per month.
  4. **The hashtag email walker** is still scratch code (BL-1586); its direct command books $0 to the ledger.
  5. **Movies** sit outside the app's scope.

## Files

`scratch/bl1613/`: free_emails.py, paid_niche.py, terms_yield.py, bio_gaps.py, forecast.py (+ the JSON outputs), movie_pack_proposal.txt, tests.log. All are read-only; edits.db was opened with `mode=ro`.
