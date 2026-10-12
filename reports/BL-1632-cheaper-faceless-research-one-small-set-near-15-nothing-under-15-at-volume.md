# BL-1632: a cheaper route to faceless TikTok editors? One small set of tags measures about $15–17 per 1,000; nothing gets under $15 at volume

## Card

| | |
|---|---|
| **Honest line** | **Nothing untested gets under $15 per 1,000 at volume.** One small set measures **$15.1–16.6 per 1,000** on v1. About 25 editors are left in it, for about $0.50. Everything else untested is about $20 (TikHub, about 65 editors) or $29–60+. |
| **The new fact** | **The best free predictor of a good tag is how many confirmed faceless editors use it in their own captions** (leave-one-out, so an editor never counts for the tag it was found on). v2: 0.55 → 2.7 → 8.1 → 14.8 faceless per 100 pages for 0 / 1 / 2–4 / 5+ editors. v1: 1.6 → 2.7 → 2.3 → 4.9. Add "also used by 20+ of the edit app's accounts" and v1 measures **4.0–4.5 per 100 pages = $15–17 per 1,000**. |
| **Why it can't scale** | Only **109 clean tags** in that group are still unwalked on v1, so about 25 editors. The loop does not feed itself: each new editor adds about 0.7 such tags, and each tag gives about 0.24 editors. |
| **Second idea** | **TikHub's tag feed is a third slice of each tag, sorted newest-first:** median post age 14 days, against about 100 on v1 and about 580 on v2. Recent posts bring editors at the same rate as old ones. On the same 222 tags (walked ones included) it is estimated at **about $20 per 1,000, about 65 editors**, if it overlaps little with v1. That overlap is the one unmeasured number. |
| **Money** | **$0.** No vendor call, not even a balance read. |
| **Recommend** | **Test A** ($0.50 cap): v1 on the 109 tags, kill at $30. **Test B** ($0.25 cap): TikHub tag feed on 40 of the 222 tags, 20 of them already walked on v1 so the overlap is measured directly. Total $0.75. |

## Your decisions

| | Question | My recommendation |
|---|---|---|
| A | Test A: about 25 editors at a measured $15–17 per 1,000 (95% range about $11–24), $0.50. | **Yes, if 25 editors are worth $0.50.** This is the only idea that measures at your line. Expect the high end: these are the tags nobody picked before. |
| B | Test B: $0.25 tells whether TikHub's newest-first slice adds about 65 more editors at about $20 per 1,000. | Only if you would accept about $20–25 per 1,000 for volume. It is above $15. |
| C | Everything else (bare fandom tags, sounds, video search, similar accounts, re-walks, other vendors). | **No.** Each is $29 or more (table below). |

## 1. Asked

$0, research only: every untested way to faceless TikTok editors with an email under $15 per 1,000, from data on disk and the saved vendor specs; each idea with its $0 evidence, expected $ per 1,000 eye-checked faceless and cost of a test; rank them; at most 2 tests, at most $2.

## 2. The ranked table

$ per 1,000 eye-checked faceless editors. "Measured" = from eye-checked yields already on disk; "estimated" = built from measured parts.

| # | Idea | $0 evidence | Expected $ / 1,000 | Editors it can give | Test cost |
|---|---|---|---:|---:|---:|
| 1 | **"-edit" tags used by ≥ 1 confirmed faceless editor AND by ≥ 20 edit-app accounts, unwalked on v1** | Measured on 612 v1 pages: 26 faceless, 53 candidates fed (4.0–4.5 per 100 pages). All 109 tags have a free tag id | **$15.1–16.6 measured** (95% about $11–24) | ~25 | **$0.50** |
| 2 | **TikHub tag feed (newest-first third slice) on the same group, 222 tags** | Probe: 26 distinct authors per $0.001 call, bio field on 30 of 30, median post age 14 days (v1 ~100, v2 ~580). v1 yield by post age is flat (≤ 14 d 10.6 vs > 365 d 9.7 per 10k items) | **~$20 estimated** (if little overlap with v1) | ~65 | **$0.25** |
| 3 | "-edit" tags used by ≥ 2 eye-confirmed editors only (no edit-app condition), v1 | Leave-one-out table above; 91 unwalked tags | ~$25 | ~13 (mostly the same tags as #1) | in #1 |
| 4 | Eye co-use 1 only, edit app < 5 | 8 faceless / 341 pages | $29 measured | ~57 | — |
| 5 | Edit-app co-use ≥ 20 only (the edit app's 25,512 accounts' 633,986 video hashtags as seeds) | 11 faceless / 536 pages; 476 unwalked tags | $32 measured | ~56 | — |
| 6 | Edit-app co-use 5–19 only | 12 faceless / 693 pages; 1,886 tags | $40 measured | ~186 | — |
| 7 | TikHub app video search "&lt;name&gt; edit" | Never called. The app post format carried a bio on 19 of 19 (BL-1628 probe). Edit-search pages show an email on 4.1% of bios, but BL-1625 found every such address already used | $30–60 estimated | unknown | $0.02 probe |
| 8 | Bare fandom tags editors use (a show, a group, a name without "edit"): 1,509 with ≥ 2 editors, never walked | Bare tags on v1 so far: 37 tags, 0.65 new emails per page, 3% precision, $54. Bare caption tags in BL-1628 ran $127–152 | $50–150 estimated | large | — |
| 9 | TikHub videos-by-sound (`fetch_music_video_list`) | Never called. BL-1623: 40 editors used 132 different non-original sounds (little sharing); LamaTok has no sound endpoint | ≥ $40 estimated | unknown | $0.05 probe |
| 10 | Re-walk proven tags on v1 later | v1: 15% of posts ≤ 7 days, 31% ≤ 30 days, so a re-walk after 30 days re-buys ~70% | ≥ $50 | — | — |
| 11 | TikHub similar accounts / following lists | User lists carry no bio (0 of 30, BL-1616); following lists hidden (4 of 4, BL-1614); LamaTok's "suggested" = the same 30 celebrities | ≥ $100 (a profile call per account) | — | — |
| 12 | Free pre-check (plays, post date) before the feed call | Skipping plays < 1,000: 8% of feeds saved, 3% of editors lost. Skipping > 180 days: 47% saved, 31% lost | < 2% saving | — | $0 |
| 13 | Another vendor (xpoz, EnsembleData, …) | BL-1628: best claim $0.03–0.04 per 1,000 authors with a bio, the same as v1's $0.029 | no gain | — | — |

**Why nothing reaches $15 at volume.** v1 costs $0.029 per 1,000 authors with a bio. With about $1.5 of feed + judge per 1,000 editors, $15 needs about 2.2 new faceless-with-email editors per 1,000 authors. The best measured group gives exactly that (4.5 per 100 pages ÷ 20.6 authors per page); the average v1 tag gives 0.9. Even the edit app's proven edit pages show an email on only 7.2% of bios, and most of those addresses are already his. A source of pure edit pages at v1's price would still sit around $15–20, which is BL-1624's floor.

## 3. Measured ($0, from disk)

**Post age per endpoint** (`age32.py`; age at the moment we bought the page):

| | v1 (BL-1628 / 1630) | v2 (BL-1628 / 1630) | TikHub tag feed (1 probe page) |
|---|---|---|---|
| Median post age | 107 / 101 days | 588 / 572 days | 14 days |
| ≤ 7 days | 15% | 3–5% | — |
| ≤ 30 days | 31% | 7–9% | — |
| v1 page 5 still had more | 77 / 92 tags of 376 / 474 | — | — |

**Recent posts are as good as old ones** (`recent32.py`, v1, first sighting of each author):

| Post age | BL-1628 faceless per 10k items | BL-1630 |
|---|---:|---:|
| ≤ 14 days | 10.6 | 5.5 |
| 15–60 days | 10.0 | 4.3 |
| 61–365 days | 10.8 | 5.2 |
| > 365 days | 9.7 | 2.4 |

**Co-use by confirmed faceless editors predicts a tag** (`coused32.py`): the caption tags of 305 eye-confirmed faceless editors (BL-1622/1625/1628/1630 feeds), leave-one-out, against every v1 and v2 tag walked in BL-1625/1628/1630. "-edit" / "-edits" tags only:

| Editors using the tag | v2 tags | v2 faceless / 100 pages | v1 tags | v1 faceless / 100 pages |
|---|---:|---:|---:|---:|
| 0 | 5,258 | 0.55 | 1,010 | 1.63 |
| 1 | 292 | 2.74 | 138 | 2.67 |
| 2–4 | 73 | 8.11 | 76 | 2.29 |
| 5+ | 20 | 14.81 | 27 | 4.89 |

The v2 numbers come from BL-1625, the first walk of those tags; v1 came later on tags partly mined. Most of the v2 stock is gone: 8 tags with ≥ 2 editors are left unwalked on v2.

**Both signals together** (`combo32.py`, v1, "-edit" tags):

| Eye editors | Edit-app accounts using it | v1 pages | Faceless | $ / 1,000 | Unwalked v1 tags |
|---|---|---:|---:|---:|---:|
| ≥ 2 | ≥ 20 | 334 | 15 | **15.1** | 52 |
| 1 | ≥ 20 | 278 | 11 | **16.6** | 79 |
| 1 | 0–4 | 341 | 8 | 29.3 | 429 |
| 0 | ≥ 20 | 536 | 11 | 31.9 | 476 |
| 0 | 5–19 | 693 | 12 | 39.5 | 1,886 |
| 0 | 0–4 | 4,337 | 68 | 49.0 | 16,193 |

- $ = pages × $0.0006 + the group's own fed candidates × $0.0008 (feed + judge). Lookups are $0: every tag in the top groups has a free id.
- **Cleaning the top two groups:** 25 of the 131 unwalked tags are the bare word "edit(s)", tool tags, aesthetic, anime or game tags, which earlier rounds measured as freelancers or NOTs. **109 are left.**
- **Shape:** "-edit" tags gave 2.0 per 100 pages and "-edits" tags 0.7 (708 pages). Tags of 10 characters or fewer: $31 per 1,000; 16 or more: $49. New lists should drop "-edits" variants.

**The edit app** (`editapp32.py`, edits.db opened read-only): 25,512 accounts with 633,986 stored videos and their hashtags. An email shows on **4.1% of accounts that have a bio** (954 of 23,332) and **7.2% of his YES pages**. BL-1624's 2.2% counted accounts with no bio stored. The new-email rate is still about 2%: BL-1625 found 0 of the 963 addresses new.

## 4. What I got wrong / limits

- **Small samples.** The $15–17 group rests on 26 faceless editors. Its 95% range is about $11–24, and the 109 tags left are the ones no earlier list picked, so the true price is more likely at the high end.
- **The TikHub overlap with v1 is not measured.** The probe tag was never walked on v1, so #2's $20 assumes little overlap. Test B measures it.
- **The sound route cannot be judged from disk.** BL-1623 kept only counts, not the 1,049 authors' ids, and feeds don't store sound ids.
- **The spec has no response examples.** Whether TikHub's video search and sound pages carry the bio is inferred from the app post format (bio on 19 of 19), not seen.
- **Caveat on the TikHub app hashtag list:** its probe page returned posts that mostly didn't carry the asked tag (2 of 19). Only the web tag feed (25 of 30 on the tag) is usable.

## 5. Money and stores

**$0.** No LamaTok, TikHub, OpenRouter or HikerAPI call, no balance read. Read only: the BL-1622/1623/1625/1628/1630 work folders, the tag ledger (`email_harvest_tags.json`), edits.db (`mode=ro`), the saved LamaTok and TikHub specs and the BL-1628 TikHub probe pages. Nothing written to master, his workbook, the ledger or config. Tag lists for the two tests are in `%LOCALAPPDATA%\ClippersHQ\bl1632_work\` (outside the repo).

## 6. Leak scan

The report names no account and no hashtag. Two-corpus scan and publish_report's secret scan: see the commit message.

## 7. Paths

- Code and counts: `scratch/bl1632/`
  - common32.py · age32.py · recent32.py · tags32.py · coused32.py · stock32.py · stock32b.py · editapp32.py · combo32.py · precheck32.py · slice32.py
  - age32.json · recent32.json · tags32.json · coused32.json · stock32.json · stock32b.json · editapp32.json · combo32.json · precheck32.json · slice32.json · PROGRESS.md
- Tag lists (outside the repo): `%LOCALAPPDATA%\ClippersHQ\bl1632_work\testA_v1_unwalked.tsv` (109) · `testB_tikhub_all.tsv` (222) · `stock32_tags.json`

<!-- CLAIMS
file:   reports/BL-1632-cheaper-faceless-research-one-small-set-near-15-nothing-under-15-at-volume.md
file:   scratch/bl1632/coused32.py
file:   scratch/bl1632/combo32.py
file:   scratch/bl1632/editapp32.py
file:   scratch/bl1632/age32.py
file:   scratch/bl1632/recent32.py
-->
