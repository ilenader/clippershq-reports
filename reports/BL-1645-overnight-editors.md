# BL-1645: overnight EDITORS run: 674 confirmed editors with emails (football 431, movies 241, tennis 2) for $13.74; tennis is walked out

## Card

| | |
|---|---|
| **Honest line** | **674 Claude-confirmed EDITORS** with new emails: **football 431 / 1,000, movies 241 / 1,000, tennis 2 / 500.** About **$20 per 1,000 editors**, $13.74 of the $30 cap. The targets were not reached; the limit was time and how many editor pages exist, not money. |
| **Search vs hashtag** | **Search finds editors but cannot sell them.** No search source carries a bio: LamaTok `/v2/search`, TikHub app/web video search and user search all have 0 bios. The authors of "<name> edit" searches are 55% editors by their bio, but **7 of the 8 addresses among 90 of them are already yours**. Every bio costs a paid profile call. **Hashtag pages win**: bios are free and the accounts are fresh. |
| **Best source** | **Movies/series edit-community tags** (the "...edit" tags the edit app's own accounts use): **28–50% of their new emails are editors**, about $19–38 per 1,000 editors. Football's edit tags: 29% once the junk was removed. |
| **Cheapest emails** | **Bare tags that confirmed editors use** (#ballondor, #portugal, #championsleague, #lamineyamal…): 6,448 new emails for $2.50, but only **4–11% editors**. Bare movie tags (#spiderman, #marvel): 4%. Cheap per editor ($12–25 per 1,000), but they cost a lot of judging. |
| **Text filter** | `clippershq/raw_filter.py` ($0, before any picture): on 1,185 eye-labelled accounts it drops **36.8% of creators and 0 of 267 editors**. Live tonight it dropped **1,662 of 9,436 accounts**, and an eye check of 40 random dropped ones found **0 clear editors** (1 borderline lyric page). |
| **Tennis** | **Walked out.** BL-1644 took nearly every tennis tag; the 14 left gave 17 new emails and 2 editors. With BL-1644's 29, tennis has 31 confirmed editors in all. 500 is not reachable from TikTok hashtags. |
| **Files** | `operator\football_EDITORS_20261015.xlsx` (431), `movies_EDITORS_20261015.xlsx` (241), `tennis_EDITORS_20261015.xlsx` (2), Claude-confirmed only. Next to them, the raw files `<niche>_raw_emails_20261015.xlsx` hold every new email with its verdict, plus `_CREATORS` / `_ANIME` / `_GAME` / `_FREELANCER` files. Page pictures are in `operator\<niche>_pages_20261015\`. Master: every row is `lead_kind raw_edit_hashtag` with its verdict. |

## Your decisions

| | Question | My recommendation |
|---|---|---|
| A | More movies editors? | **Yes, cheapest per eye-check**: about 20 more movies edit-tag chunks are ready (`bl1645_work\movies_c09..c28.tsv`), at about 25–30 editors per chunk for about $0.60. |
| B | More football editors? | The football edit tags are used up. Next would be bare player/club tags (cheap emails, about 5–10% editors), or growing more learned tags from tonight's 431 editors. |
| C | "Football" includes some **American football / college** editor pages (#browns, #olemiss, #alabama came in through the learned tags). | Say if you want those moved to their own file; tonight they count as football editors (edits of athletes). |

## 1. Asked

Owner 23:32: "editors is the word of the day". Faceless pages posting edits of famous people, not creators, not businesses. Tennis 500, football 1,000, movies 1,000 (real movies and series, not anime or cartoons). Text filter first, then pictures and eyes. Research search vs hashtag. Squeeze everything; learn while running. Cap $30. Deliver in waves; reply at 09:00.

## 2. Research (step 1, $0.071)

`scratch/bl1645/research45.py` and `research45b.py`. Queries "sinner edit", "mbappe edit", "homelander edit"; 3 pages per source:

| source | authors per call | with a bio | notes |
|---|---|---|---|
| LamaTok `/v2/search` | 24–30 | **0** | the only search endpoint in the live spec (1.4.5); 250 of 251 found videos have "edit" in the caption |
| TikHub app `fetch_video_search_result` | 20 | **0** | |
| TikHub web `fetch_search_video` / `fetch_search_user` | 0 | – | empty without a cookie |
| TikHub `fetch_hashtag_search_result` | 19–20 tags | – | mostly generic tags; 0–2 with "edit" |
| profiles of 90 LamaTok-search authors ($0.054) | – | 84 | **55% have edit words in bio/name**; 8 have an address, **7 already yours** |

Hashtag pages (v1 + v2) carry the bio for free, so they stayed the backbone.

## 3. The pipeline (per chunk of about 150 tags)

1. **Walk** `raw_emails.py walk` (v1 to its end, then v2 on tags where v1 bought a new address, $10/1k line on v2 only, raw store).
2. **Text filter** `raw_pages.py filter` ($0).
3. **Feed**: one paid call ($0.0006) per kept account with fewer than 6 posts, so every picture shows about 12 covers (BL-1644 pictures had 1.4). 4 parallel lanes after 04:55 (serial took about 2 h for 2,562).
4. **Pictures + sheets** (8 per sheet).
5. **Eyes**: Haiku judges every sheet; Sonnet re-checks every sheet with an EDITOR or UNSURE. Codes: E editor / C creator / B business / A anime-cartoon / G game / R freelancer / U unsure. Sheets s0001 / s0026 / s0068 (BL-1644) and football_c01 s0001, football_c03 (all), tennis_n1 (all) were checked by me.
6. **Deliver** `raw_emails.py deliver --verdicts --editors-file`, in waves.

The free OpenCV judge (Video Downloader's `page_judge.py`) was tested again on full 12-cover pictures. Its CREATOR calls hid 3 of 61 football editors (5%) and 3 of 29 movies editors (10%), so it was **not used to skip pages**.

## 4. Results per chunk

| run | tags | new emails | text-dropped | EDITOR | CREATOR | UNSURE | other | $ | $ / 1,000 editors |
|---|---|---|---|---|---|---|---|---|---|
| tennis_n1 | tennis tags left | 17 | 6 | **2** | 14 | 1 | 0 | 0.07 | 32.4 |
| football_c01 | football edit tags (2 junk tags = 78%) | 562 | 76 | **40** | 441 | 38 | 43 | 1.08 | 27.0 |
| football_c02 | football edit tags | 209 | 24 | **61** | 101 | 9 | 38 | 0.82 | 13.4 |
| football_c03 | football edit tags | 24 | 0 | **15** | 6 | 2 | 1 | 0.14 | 9.4 |
| football_x01 | learned bare football tags | 3535 | 702 | **257** | 2950 | 119 | 209 | 3.14 | 12.2 |
| football_x02 | learned bare football tags | 2862 | 546 | **94** | 2439 | 125 | 204 | 2.35 | 25.0 |
| movies_c01 | movies/series edit tags | 88 | 6 | **25** | 31 | 4 | 28 | 0.62 | 24.9 |
| movies_c02 | movies/series edit tags | 97 | 11 | **17** | 49 | 16 | 15 | 0.64 | 37.9 |
| movies_c03 | movies/series edit tags | 80 | 6 | **29** | 15 | 15 | 21 | 0.62 | 21.4 |
| movies_x01 | learned bare movie tags | 1346 | 214 | **56** | 1088 | 149 | 53 | 0.90 | 16.1 |
| movies_c04 | movies/series edit tags | 62 | 4 | **31** | 15 | 3 | 13 | 0.58 | 18.9 |
| movies_c05 | movies/series edit tags | 108 | 9 | **31** | 40 | 2 | 35 | 0.63 | 20.3 |
| movies_c06 | movies/series edit tags | 68 | 10 | **19** | 35 | 9 | 5 | 0.60 | 31.8 |
| movies_c07 | movies/series edit tags | 304 | 43 | **28** | 222 | 15 | 39 | 0.84 | 30.0 |
| movies_c08 | movies/series edit tags | 74 | 5 | **19** | 29 | 6 | 20 | 0.61 | 32.3 |

Judged EDITORs (football 467, movies 255, tennis 2) are more than the delivered ones: an account found by two chunks is delivered once; the second delivery drops it as already yours. **Delivered: football 431, movies 241, tennis 2 = 674.**

## 5. What was learned during the night

- **Junk tags dominate emails**: "specialedition" (contains "edit") gave 332 emails and 1 editor; "microwaveedit" 106 and 0. Together they were 78% of football chunk 1. Removed from every later list (edition, microwave, video, text, phonk, tuff, game…).
- **Clean edit tags ≈ 30% editors**; football chunk 3: 15 of 24.
- **Learned tags** (tags that ≥ 2 confirmed editors use in their own captions): bare player/club tags. Huge volume (3,559 and 2,889 new emails for $1.50 and $1.00) but 9% and 4% editors after the text filter; bare movie tags 4%.
- **HEIC covers**: the app dialect lists `.heic` first, which no image library here opens; the `.jpeg` twin is now preferred, and a HEIF file on disk is re-downloaded.
- **Best tags by confirmed editors**: #ballondor 32 of 137, #portugal 28 of 267, #oliviarodrigo 22 of 484, #browns 16 of 98, #basketball 12 of 126, #olemiss 10 of 291, #alabama 9 of 282, #cinema 8 of 220, #gabrieljesus 7 of 20, #championsleague 6 of 32, #bijanrobinson 6 of 16, #newyork 6 of 566, #cover 6 of 413, #disneyplus 6 of 249, #taylorswift 6 of 271.

## 6. Money

**$13.74 of the $30 cap** booked (`raw_emails` campaign since 23:40), research included ($0.071: LamaTok 99 + TikHub $0.012). Walks plus feeds: football $7.53, movies $6.04, tennis $0.06. That is **$20.4 per 1,000 delivered editors**: football $17.5, movies $25.1. Each walk read the vendor balance before and after; where nothing else ran at the same time the billed requests matched the meter. Feed calls ran next to walks, so those balance deltas overlap, and the ledger books every call. Agent tokens for the eyes: about 15M, most of them on the learned bare tags (5,069 football + 1,132 movies accounts at 4–11% editors).

## 7. Code

- `clippershq/raw_filter.py` (new): the text filter. `scratch/bl1645/textfilter45.py` scores it.
- `clippershq/raw_pages.py`: `filter`, `feeds` (parallel lanes), filter-aware `new_rows`, `defer:` marks (a held-back sample is never a verdict), run date marker, HEIF re-download, more verdict codes (B/A/G/R).
- `clippershq/raw_emails.py`: `.jpeg` cover preference, run date marker, `deliver --date --editors-file`, own files for anime / game / freelancer.
- `scratch/bl1645/`: research45(b), tags45, chain45, process45, eyes45.js (workflow), finish45, dropcheck45, ana45.

- 09:00 FINDER BL-1645 OVERNIGHT editors: 674 confirmed editors (football 431, movies 241, tennis 2) for $13.74; search has no bios, hashtag wins; text filter 0/267 editors lost (DONE)
