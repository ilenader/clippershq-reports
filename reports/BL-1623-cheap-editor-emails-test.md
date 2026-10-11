# BL-1623: cheap editor emails test: YouTube gives faceless edit pages for about $0.16 per 1,000; edit-community tags give freelancers, not faceless pages

## Card

| | |
|---|---|
| **1. Delivered (every row checked by eye)** | **Faceless 84** (YouTube 80, TikTok 4) → master + workbook + faceless file. **Freelancers 76** (TikTok 72, YouTube 4) → their own file only. |
| **2. Each source's $ per 1,000, eye-checked** | **YouTube** (free API quota, AI judge only): **$0.16 per 1,000 faceless**. **TikTok freelance tags:** **$5.70 per 1,000 freelancers**. **TikTok tool tags** (aftereffects, capcut, velocity…): **$10.8 per 1,000 freelancers**, but **$121 per 1,000 faceless**. **Edit sounds:** 0 emails for $0.055 (dead). **Instagram:** estimate about $20–50 per 1,000 faceless (not run). |
| **3. Judge on the new topics (BL-1622's 90 eye-checked rows)** | Before: keeps real **68.9%**, with 0% of the non-editors caught. After (v5, the version used): keeps real **80.3%**; it catches half the non-editors and keeps 92% of the real editors. Strict mode (both models must agree): **90.6%** real, but it keeps only 77% of editors. |
| **4. Page size and depth** | **Page size:** asking for 50 items returns about 19. The endpoint caps a page at about 20, so there is no gain. **Depth:** these tags end by page 4. New emails per page: 1.65 → 1.06 → 0.38 → 0.33. **Kill rule:** stopping after 1 empty page costs 52 calls for 48 emails; after 2 empty pages, 65 calls for 54. |
| **5. 1,000 emails from the winners only** | **Faceless via YouTube:** about **$0.16** of AI judging. The limit is the free YouTube quota: about **5 days** on one key, or about 1 day with 5 keys. About 1 hour of run time, plus my eye check. **Freelancers via TikTok:** about **$6–11** and 2–3 hours of runs, *if* new community tags exist. This round walked all 151 it had. |
| **6. Files** | `<PROFILE>\AppData\Local\ClippersHQ\operator\editor_emails_20261011_faceless.xlsx` (84) · `<PROFILE>\AppData\Local\ClippersHQ\operator\editor_emails_20261011_freelancers.xlsx` (76) |

**Spent: $0.80 of $2.00** (LamaTok $0.64 + OpenRouter $0.16), measured by both vendors' balances. **No email was sent.**

## Your decisions

| | Question | My recommendation |
|---|---|---|
| A | YouTube faceless pages cost about $0 in vendor money; the free quota (10,000 units a day per key) is the only limit. | Run it **every day** on the free quota (about 190 faceless a day per key). Add more Google Cloud keys if you want 1,000 sooner. |
| B | 76 freelance video editors sit in their own file. | Your call: add them to master and the workbook, or keep them apart. |
| C | Instagram is estimated at $20–50 per 1,000 faceless. | Skip it. Or approve a $0.30 test to replace the estimate with a measurement. |

## 1. Asked

Find sources under $10 per 1,000 (target $5), priced on **eye-checked** rows, with a $2 cap, reusing BL-1622's pipeline:

0. Retrain the judge for new topics.
1. Edit-community tags, sorted into faceless vs freelancer.
2. Page size.
3. Page depth.
4. The kill rule.
5. Edit sounds.
6. YouTube.
7. An Instagram estimate.

Every delivered row is checked by eye. A source is stopped once it measures over $10 per 1,000 after $0.30.

## 2. Shipped and proved

| Piece | Proof |
|---|---|
| `scratch/bl1623/judge5.py`: three classes (FACELESS / FREELANCER / NOT), plus NOT rules for what fooled BL-1622 (music and lyrics pages, gaming, manga, concert photos, highlight pages with meme captions, compilations, non-English text) | `tests/test_bl1623_judge3.py` 7/7; scored in `calib5_score.json` |
| `run.py`: BL-1622's stream, judge and gates, unchanged, pointed at this round's folders and judge | 4 paid runs; the funnels are in `status_*.json` |
| BL-1622 `stream.py --dry-pages` (the kill rule as a setting; default 2, unchanged) | The depth test ran with it at 0 |
| `yt.py`: YouTube Data API → address in the channel description → gates (180 days, channel average views ≥ 2,000) → same judge on the 6 newest thumbnails | 152 AI keeps → 84 checked by eye |
| `sounds.py`: editors' sounds → search by sound title | Measured dead (below) |
| `deliver5.py`: two files; only faceless rows go to master and the workbook | 84 + 76 rows read back; workbook 4,654 → 4,738, MARK untouched, vaulted |

## 3. Measured

**Step 0, judge, on BL-1622's 90 eye-checked rows (62 real, 28 not):**

| Judge | Real editors kept | Non-editors dropped | Keeps that are real |
|---|---:|---:|---:|
| v4 (BL-1622) | 100% | 0% | 68.9% |
| **v5: qwen first, then Haiku (used)** | **91.9%** | **50.0%** | **80.3%** |
| v5, both must agree | 77.4% | 82.1% | 90.6% |
| v5, Haiku alone | 85.5% | 67.9% | 85.5% |

- On the 659 older verdicts, v5 scores 87.4% / 97.4%.
- I used the qwen-then-Haiku setup because every delivered row is eye-checked anyway, and it keeps the most real editors per dollar.
- Cost of this step: $0.101 (the cap was $0.20).

**Eye checks, by source:**

| Source | AI keeps | Faceless | Freelancer | Not |
|---|---:|---:|---:|---:|
| YouTube "<name> edit" Shorts (40 searches) | 152 | **80** | 4 | 68: meme- and stat-caption football Shorts, celebrity fan pages, ranking lists |
| TikTok tool tags (95 tags) | 72 | 4 | **45** | 23: lifestyle creators, music producers, non-English text, game art |
| TikTok freelance tags (28 tags) | 30 | 0 | **27** | 3 |

**Funnels:**

| | Pages / searches | New emails | Passed the gates | AI keeps |
|---|---:|---:|---:|---:|
| TikTok tool tags | 47 + 225 pages | 54 + 307 | 30 + 268 | 14 + 58 |
| TikTok freelance tags | 91 pages | 127 | 69 | 30 |
| YouTube | 40 searches, 1,243 channels | 186 | 173 | 152 |
| Sounds | 40 feeds, 50 searches, 1,049 authors | **0** | — | — |

**Steps 2–4: page size, depth and kill rule:**

| | |
|---|---|
| Docs (`/openapi.json`, free) | `/v2/hashtag/medias` count: default 20, maximum 50 |
| Test (2 calls, both billed 1 request) | count=50 → **19 items**. BL-1622's count=30 pages averaged about 15 authors. **No gain.** |
| Depth, 20 tags × up to 10 pages, no kill rule | Pages per tag: 1 → 4 tags, 2 → 8, 3 → 5, 4 → 3, none deeper (`has_more` false) |
| New emails per page | p1 1.65 · p2 1.06 · p3 0.38 · p4 0.33 |
| Kill after 1 empty page vs 2 | 52 calls / 48 emails vs 65 calls / 54 emails. The 6 extra emails cost about $1.30 per 1,000 raw: still cheap, so **2 stays** |

**Edit sounds:**
- LamaTok has **no "videos by sound" endpoint** (its spec: 29 paths), so I searched each sound's title instead.
- Search results carry **no bio** (probe: 0 of 29). Every author would need a feed call just to read the bio.
- Stopped at $0.055, as dead.

**Instagram (estimate):**
- HikerAPI's hashtag and list routes carry 0 bios (BL-1553: 0 of 738 slots), and there is no bulk user route.
- That leaves 1 paid call per bio, at about $0.00078 (BL-1572: 9,074 bios for $7.05).
- At a 5–10% email rate: about **$8–16 per 1,000 raw emails, about $20–50 per 1,000 faceless.**

**Speed:** TikTok runs made 16–146 paid calls a minute. LamaTok answered "throttled (427)" on bursts of lookups; those are unbilled and were retried.

## 4. What I got wrong

- **I lost YouTube set 2** (50 more searches).
  - Its judge step crashed on a spend.json lock timeout before saving anything; spend.json is 19 MB and other writers held its lock for more than 120 seconds.
  - Today's free quota is nearly used, so I didn't re-run it. The lost judging cost $0.0037, which is booked.
  - Fixed: a booking failure no longer kills the work, and the candidates and answers are saved as they arrive.
- **The first depth launch had 0 tags** (my shell split failed). It exited at $0, after building the known cache.
- **The freelancer file has a judgment edge.** Tutorial and template creators count as freelancers, and editors with non-English on-screen text are excluded, following the brief's language rule.

## 5. Money and stores

| | Start | End | Spent |
|---|---|---|---|
| LamaTok (free balance read) | 316,367 requests | 315,298 | **1,069 requests = $0.6414** |
| OpenRouter (free credits read) | usage 16.6754 | 16.8310 | **$0.1556** |
| **Round total** | | | **$0.797 of $2.00** |

- **By source:**
  - Judge calibration $0.101
  - Tool tags $0.485
  - Freelance tags $0.154
  - Sounds $0.055
  - YouTube $0.013
  - Page-size test $0.001
- **Ledger:** spend.json campaign bl1623 matches the balances after 2 reconcile rows:
  - −24 LamaTok calls: throttled answers the meter counted but the vendor did not bill.
  - +$0.0037 OpenRouter: the crashed YouTube judge step.
  - No other campaign spent LamaTok in the window.
- **Stores written:**
  - master +84 (run_id bl1623, backup made)
  - Workbook: Emails 4,654 → 4,738, vaulted
  - The 2 operator files
  - Tag ledger
  - `bl1623_work\memory.jsonl`, seeded with BL-1622's paid-for accounts so nothing is paid for twice
- **YouTube quota used: about 9,300 of the 10,000 daily units.** Any other YouTube use on this key today has little room left.

## 6. Leak scan

| Scan | Result |
|---|---|
| Secret scan (publish_report) | PASS (run at publish) |
| Two-corpus scan (`scratch/bl1604/leak_adjudicate.py`, edit and lead corpora, every committed file) | 153 hits. 137 are explained by the public vocabulary. The other 16 were adjudicated by value, without printing them: public show, film, driver and anime names and editing-app words in the lists and prompts I wrote, plus ordinary English words. **0 leaks.** This report has 1 hit, an editing-app word in the source table. |

## 7. Next

1. **A daily YouTube faceless job**, on the free quota with saved checkpoints, plus my eye check. About 190 faceless a day per key.
2. If you want freelancers: generate new community and freelance tags; the 151 used here are walked. Expect about $6–11 per 1,000.
3. Don't spend on edit sounds or Instagram unless you want the $0.30 Instagram test.

## 8. Paths

- Code and counts: `scratch/bl1623/`
  - judge5.py · run.py · calib5.py · gen_community.py · yt.py · sounds.py · deliver5.py · PROGRESS.md
  - calib5_score.json · page_size.json · depth_kill.json · per_source.json · yt_result*.json · sounds_collect.json · search_bio_probe.json · status_*.json
- Test: `tests/test_bl1623_judge3.py`
- Work data: `%LOCALAPPDATA%\ClippersHQ\bl1623_work\` (keeps, eye verdicts, strips, YouTube rows)
- Files: `<PROFILE>\AppData\Local\ClippersHQ\operator\editor_emails_20261011_faceless.xlsx` · `…_freelancers.xlsx`
