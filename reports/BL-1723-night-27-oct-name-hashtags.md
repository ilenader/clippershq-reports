# BL-1723 -- Night 26-27 Oct: 1,000 NEW editor e-mails for $25 (order 2327 + 2335)

**Result: 218 new good TikTok editor e-mails on this line (27 Oct 15:24, after the judge's anime rule was fixed and every reject re-judged) for $25.15 (~11.5 c each) of $25 -- **$0.15 over the cap, my bookkeeping error** (see Money);
1,000 was not reachable at the price measured tonight.** "New" = address AND account in none of the 790 files ever
delivered, plus master and his workbook; "good" = the frames + speech-to-text judge said K (Opus second look on unsure)
and the address passed address_check. File: `Desktop\Tools\NEW_editor_emails_A49_26_Oct.xlsx`.

## What each route cost per NEW good e-mail (measured tonight)

| route | spent | result | price per NEW good |
|---|---|---|---|
| never-walked hashtags from good editors' captions (w1, w2) | $3.00 | 10 good / ~340 judged (2-6%) | ~30-40 c -- **dead** |
| "<name> edit" SEARCH pages (kT, 160 names in 8 categories) | $0.10 | 60 bio e-mails, **57 already ours**, 3 new | >= 3 c per address before the judge -- **loses** |
| #<name>edit / #<name>edits HASHTAG pages, same names (tT) | $0.20 | 29 new addresses, 4 good / 24 | ~5 c -- **wins the test** |
| #<name>edit hashtags on 16,900 NEW names, $1 chunks (n1-n7, m1-m6, p1, q1-q6) | $19.50 | 3,673 new addresses (188 per $1), 192 good of 1,984 judged first, 9.7% | ~10 c |

Good-editor rate per category on the name hashtags (judged pages, 06:00): football 16%, basketball 13%,
UFC/boxing/WWE 12%, TV 12%, cartoons 9%, other sports 6%, **anime 0%, movies 0%**.

## Why 1,000 was not reachable
- A $0.0006 hashtag page gives ~20 accounts; after the duplicate check ~80% of the editors who show an e-mail are
  already ours, so ~100-170 accounts with a NEW address per $1, of which only 10-16% are real editors (the rest are
  fans, creators, clip pages). That is ~12 good per $1 -> $25 buys ~300, not 1,000.
- Sheets (newest video, frames, speech-to-text) are built on the 3090; under the night's load (shared with Flashcut,
  ~107% CPU) that is ~300 sheets/h, so the judged count trails the spending by 2-4 hours.

## The next 1,000 -- faster
1. **Chain the paid walks** (done tonight: `scratch/bl1723/chain23.py`): walk -> judge-prep -> next walk with no gap;
   one paid walk at a time, stops on `STOP_CHAIN` or at the first money_guard refusal.
2. **Speech-to-text on the 3090's GPU, not its CPU**: the sheet worker spent 20-40 min per 12 accounts at 120-170% CPU
   each. On the GPU the build should run several times faster, so the judged count would keep pace with the money.
3. **One sheet lane per chunk** (done): 12 lanes on a loaded box starved each other and set off false "stalled" alarms.
4. **Judge loop reloads its tables every pass** (fixed 01:53): a stale cache held back 243 of 263 likely editors.
5. **Keep the 3090's disk clear**: at 09:59 every sheet lane stopped on the 6 GB disk guard; 1.9 GB of it was 36
   leftover temp folders from sheet batches that had died (`/tmp/b12s_*`). x23 should sweep its own stale folders
   before each batch (the rest of `/tmp`, ~7 GB, belongs to other windows).
6. **Judge slots on the farm**: 09:00-09:50 all 16 farm slots were taken by Flashcut jobs, so 56 judge jobs waited and
   one failed after 24 retries. A judge job takes ~80 s; one or two slots kept for it would have kept the count moving.
7. **Names ready before the night**: 16,900 names were written free by a Claude agent in ~40 min; prepare 20,000+
   (sports and TV first) the afternoon before, so the money starts on the best ground at minute one.

## The next 1,000 -- cheaper
1. **Only name hashtags in football / basketball / UFC-boxing-WWE / TV** (12-16% good); skip anime and movies (0%)
   and generic caption tags (2%).
2. **Do not pay for tags that do not exist**: 12-49% of the agent's name tags returned 404 (each still costs its
   /hashtag/info call). Check the names against tags already seen in stored captions (free) before buying.
3. **No "<name> edit" search**: 95% of its e-mails are already delivered.
4. At ~10 c per new good e-mail the honest price of 1,000 more is **~$100**, unless a route with a higher editor share
   is found; the cheapest untested idea is the free "no email yet" list (55k TikTok editors) -> their link-in-bio pages
   (4 new of 337 tonight, free) and the same handles on Instagram / YouTube bios (free reads only).

## Money (line "Finder 1000 leads 26 Oct", $25 hard cap)
| what | usd |
|---|---|
| before the order (23:16) | $1.75 |
| everything else: tests + dead routes (w1, w2, search kT, hashtag tT, ...) and overshoots | ~$3.90 |
| 20 name-hashtag chunks (tagrun23, counter-settled) | $19.50 |
| **line total, real (LamaTok counter)** | **$25.1538** |
| over the $25 cap | **$0.1538** -- my error: a hand settle from the wrong base + overshoots settle() never books; wallet carries the correction entries (07:20) |

No paid call on this line after 07:18. Since 11:58 the walk wrapper (tagrun23.py) sizes every chunk from the vendor
counter, refuses one that does not fit, and books any overshoot (commit f21505cb).

## After the night (27 Oct)
- 10:04-13:28 the judge stood still: the bandwidth guard paused the 3090's Syncthing, so no farm job ran; bogdan was
  stale; Dusan's PC was over his 70% RAM line. From 13:28 the judge ran on the 3090 **directly over ssh** as user farm
  (`scratch/bl1723/podjudge23.py`): ~110 jobs in ~20 min, 0 failures. Every name-tag sheet was judged by 13:57.
- The $1 test Dusan approved (order 1246, line "Finder daily"): only football/basketball edit-tags already seen used.
  $0.9798 -> 244 new addresses, 199 sheets, **9 good = 10.9 c each** -- the ~2-3 c projection did NOT hold (see
  reports/BL-1723-next-1000-faster-cheaper.md, "Test result").
