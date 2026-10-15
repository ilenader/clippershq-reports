# BL-1646: 481 first-world EDITORS (US 201, Europe 243) for $15.86; country found for every editor; sports beats movies on first-world price

## Card

| | |
|---|---|
| **Honest line** | **481 new first-world editors** with emails (US 201, Europe 243, CA/AU/NZ 37), plus 163 in other countries and 7 with no known country, for **$15.86** of the $16.26 left. That is **$33 per 1,000 first-world editors** ($24 per 1,000 editors of any country). It is not under $15. |
| **Mix** | Movies & culture **275** first-world editors (57%), sports **177** (37%), football **29** (6%). Danilo asked for 70 / 30. Sports gave first-world editors at **$19–30 per 1,000**, movies and culture at **$36–125**. The culture edit tags ran out, so 70% movies would have cost more. |
| **Country** | **$0, from data we already had.** v2 hashtag pages and feed pages carry each account's `region` (US, GB, DE…). v1 pages carry only the **spoken language** of the captions ("eng-US" means English, not the United States), so v1 is never used as a country. With feed pictures, only 7 of 651 new editors have no region. |
| **The 703 already delivered** | Re-cut into copies: **499 first world** (US 234, Europe 233, CA/AU/NZ 32), 178 in other countries (Brazil 38), 26 unknown (23 of them are BL-1644 tennis, which never had a v2 page). The US share is **34.6%** of those with a known country. |
| **Files** (folder `operator\`) | `editors_movies_20261015_firstworld_w1..w4.xlsx`, `editors_sports_20261015_firstworld_w1..w2.xlsx`, `editors_football_20261015_firstworld_w1.xlsx`. Each has the sheets **Editors first world** (US first) and **Unknown country**, plus a separate `_other_countries` file. `_secondlook` files are **less sure** (see 5). The 703: `editors_{football,movies,tennis}_20261015_firstworld_recut.xlsx` and `*_EDITORS_*_with_country.xlsx`. Every row has `country_guess`, `us` and `country_basis`. |

## Your decisions

| | Question | My recommendation |
|---|---|---|
| A | A bigger budget (Danilo: "$50–100 but keep prices down")? | **Yes, but expect about $35 per 1,000 first-world editors, not $15.** $50 buys roughly **1,000–1,400 first-world editors** from new learned co-tags (sports first, then culture). It uses a lot of Claude eye time (~1M agent tokens per 100 editors on bare tags). Dusan's yes is needed. |
| B | Keep 70 / 30? | **Let the price decide the mix.** Sports (F1, NBA, NFL, UFC) gives 75–85% first-world editors; movies gives 55–75%. |
| C | Second-look files (`_secondlook`) | Send them, but after a quick look. My spot check found 3 of 4 are real editors; the others are lyric or mood pages. |

## 1. Asked

11:15 (P1): continue movies and football with the $16.26 left, in waves of 50 to new files, and add a `country_guess` + `us` column for every editor, including the 703 already delivered.
11:28 (P0, Danilo): ~70% movies & culture (films, series, actors, singers, rappers, celebrities, history) and ~30% other (football, NBA, UFC, F1, cars). First-world countries only, US first, then Europe; unknown country goes on its own sheet. New files `editors_<niche>_<date>_firstworld.xlsx`, and the 703 re-cut. Stop at $16.26 and report what more money would buy.

## 2. Country ($0)

`scratch/bl1646/country46.py` scans every stored page payload (`raw_store`, 4 GB gz, 6 processes, ~10 min) into a per-account cache (`bl1646_work/country_cache`, also per-tag region counts). `country_guess` = the most common `author.region` / item `region` on that account's stored v2 + feed videos. `us` = yes / no / unknown. `country_basis` says "region on n of m videos", or "no region stored; spoken language English" (hint only).

First world = US, CA, GB, IE, AU, NZ, DE, FR, NL, BE, AT, CH, SE, NO, DK, FI, IT, ES, PT (the order's list).

## 3. Sources and tags

- **Movies/series edit tags**: `bl1645_work/movies_c09..c15`, the rest of BL-1645's list.
- **Culture + sports edit tags (new)**: 3,436 unused "…edit" tags from the edit app's own accounts (n ≥ 2, junk/anime cut) were sorted by 4 Sonnet agents into culture 912 (movie/actor 741, singer 94, celebrity 62, history 15), sports 341 (NBA/NFL 160, UFC/boxing 93, F1/cars 88), football 107 and other 2,075. These became chunks `culture_c01..c07`, `sports_s01..s03` and `football_f01`.
- **Learned co-tags (new)**: the tags that ≥ 2 of today's confirmed editors use in their own captions, generic words removed. These became `culture_l01` (actors, singers, shows) and `sports_s04` (F1 drivers and teams, NBA players, NFL teams). They have huge volume (about 3,000 new accounts each) but only ~4% editors.

## 4. Results per chunk

Editors = first-look EDITOR verdicts. An account found by two chunks is delivered once, so delivered counts are slightly lower. Unsure = sent to the second look. $ = walk + feed calls (vendor-priced $0.0006/call).

| run | source | new accounts | editors | unsure | first-world editors | US | $ | $ / 1,000 first-world |
|---|---|---|---|---|---|---|---|---|
| movies_c09 | movies/series edit tags | 122 | 10 | 7 | 5 | 0 | 0.62 | 125 |
| movies_c10 | movies/series edit tags | 127 | 22 | 3 | 14 | 6 | 0.63 | 45 |
| movies_c11 | movies/series edit tags | 217 | 17 | 16 | 11 | 3 | 0.71 | 65 |
| movies_c12 | movies/series edit tags | 538 | 12 | 3 | 7 | 5 | 0.86 | 123 |
| movies_c13 | movies/series edit tags | 86 | 11 | 3 | 7 | 1 | 0.58 | 83 |
| movies_c14 | movies/series edit tags | 107 | 7 | 4 | 6 | 4 | 0.59 | 98 |
| movies_c15 | movies/series edit tags | 97 | 14 | 2 | 9 | 5 | 0.61 | 68 |
| culture_c01 | culture edit tags (actors, singers, history) | 149 | 36 | 5 | 18 | 7 | 0.64 | 36 |
| culture_c02 | culture edit tags | 135 | 28 | 13 | 17 | 7 | 0.65 | 39 |
| culture_c03 | culture edit tags | 114 | 19 | 18 | 12 | 4 | 0.64 | 53 |
| culture_c04 | culture edit tags | 159 | 24 | 16 | 19 | 10 | 0.68 | 36 |
| culture_c05 | culture edit tags | 140 | 20 | 8 | 18 | 8 | 0.66 | 37 |
| culture_c06 | culture edit tags | 118 | 12 | 8 | 9 | 2 | 0.65 | 72 |
| culture_c07 | culture edit tags | 20 | 4 | 1 | 4 | 2 | 0.07 | 16 |
| culture_l01 | learned culture co-tags | 3176 | 97 | 151 | 72 | 25 | 2.67 | 37 |
| sports_s01 | sports edit tags (NBA, UFC, F1) | 147 | 46 | 7 | 39 | 18 | 0.75 | 19 |
| sports_s02 | sports edit tags | 127 | 29 | 6 | 24 | 13 | 0.72 | 30 |
| sports_s03 | sports edit tags | 52 | 6 | 2 | 5 | 3 | 0.21 | 42 |
| sports_s04 | learned sports co-tags (F1, NBA, NFL) | 2648 | 113 | 94 | 87 | 40 | 2.38 | 27 |
| football_f01 | football edit tags (the last ones) | 99 | 36 | 4 | 27 | 6 | 0.53 | 20 |

## 5. Second look at "unsure" ($0)

Pages the first look could not decide (369 in all) got a closer look from Sonnet on the single full picture (`scratch/bl1646/unsure46.py` + `unsure46.js`). This found **94 more editors**: movies 66 (50 first world), sports 25 (8 went into sports w2, 17 into `_secondlook`), football 3 (into football w1). In my own spot check of 4 recovered pages, **3 were real** (a model edit page, a film-clip page, a history storytelling page) and 1 was a lyrics/mood page. That is why they sit in their own `_secondlook` files, labelled "less sure".

## 6. What was learned

- **First-world share depends on the subject.** Sports pages (F1, NBA, NFL, UFC) are 75–85% first world and ~40% US. Movies/culture are 55–75%, with Brazil the largest "other" country.
- **One junk tag can eat a chunk.** `#howtoedit` gave 441 of movies_c12's 494 emails and 0 editors (lifestyle/tutorial creators). Added to LESSONS (#4) and COUNCIL; 7 more generic/cartoon tags were removed from the unwalked chunks.
- **Learned bare co-tags give volume, not purity:** ~3,000 new accounts per $1.20 walk but ~4% editors. Feeds capped at 500 left 1,900 pages with fewer than 4 covers, so about 1,944 + 1,470 extra feed calls (~$2.05) were bought. **`raw_pages sheets` skips existing sheets**, so after re-rendering pictures the old sheets must be moved away first (done; the old ones are in `bl1646_work/old_*_sheets`).
- 4 walk lanes run ~3× faster than 2; 5xx retries are not billed.

## 7. Money

**$15.861 of $16.26** (vendor request counter: 260,636 at 11:18 → 15.861 / 0.0006 = 26,435 requests). The per-run walk + feed figures add up to $13.81, plus $1.17 and $0.88 of extra feeds = $15.86. The 4 Sonnet tag sorts, all eyes and the second looks used Claude tokens only (~25M agent tokens, most of them on the two learned co-tag chunks). No email was sent.

## 8. Code

`scratch/bl1646/`: chain46 (walk + background processing, a $ limit from the vendor counter, a STOP file), process46, finish46, done46.sh, country46, firstworld46, unsure46.py/.js, eyes46.js (rubric widened to singers, rappers, celebrities, history, cars/F1), cost46, stats46, table46. No change to `clippershq/`.

- 17:55 FINDER BL-1646 first-world editors: 481 first world (US 201) + 163 other for $15.86; 703 re-cut (499 FW); country $0 from v2 region (DONE)
