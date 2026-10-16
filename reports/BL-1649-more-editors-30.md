# BL-1649: 869 more first-world EDITORS (US 337, Europe 479) for $25.40 of the $30 cap; real-name tags only; $4.60 left unspent on purpose

## Card

| | |
|---|---|
| **Honest line** | **869 new first-world editors** with emails (US 337, Europe 479, CA/AU/NZ 53), plus 386 in other countries and 3 with no known country, for **$25.40 of the $30.00 hard cap** (Dusan 20:38). That is **$29 per 1,000 first-world editors**, or $35 counting only the first look. It is not under $15. **140 of the 869 come from the less-sure second look.** |
| **Per niche (first world)** | Football **380** (soccer and NFL), movies & culture **300**, sports (NBA, F1, UFC, cars) **189**. By money spent: football $28, sports $34, movies $45 per 1,000 first-world editors (first look only). |
| **Source** | The hashtags that the 1,300+ confirmed editors of BL-1645/1646 use in their own captions ("learned co-tags"), never walked before. **Generic words in that list are poison:** the first sports chunk was 66% #techtok / #chicago / #gymtok / #school…, and the first football chunk was 60% #losangeles / #morocco / #netherlands… Sonnet then kept only **named subjects** (players, teams, drivers, car brands, actors, singers, shows): 1,542 of 2,978 tags. Editor rate went from 2.6% to 6–10%. |
| **Stopped early** | The last two lists (BL-1645's movies edit tags c16/c17) gave 3 and 6 first-world editors for $0.61 and $0.83 (**$139–204 per 1,000**). They are drifting into anime and game pages. **$4.60 is left unspent** rather than paying 6× the price ("keep prices down"). |
| **Files** (folder `operator\`) | `editors_sports_20261015_firstworld_b1..b3.xlsx`, `editors_football_20261015_firstworld_b1..b5.xlsx`, `editors_movies_20261015_firstworld_b1..b4.xlsx`. Each has the sheets **Editors first world** (US first) and **Unknown country**, plus a separate `_other_countries` file. The second look is in `editors_{movies,sports,football}_20261016_firstworld_secondlook.xlsx` (less sure; check before sending). Every row has `country_guess`, `us`, `country_basis`. The "20261015" in the names is the round's start date. |

## Your decisions

| | Question | My recommendation |
|---|---|---|
| A | More money? | The learned co-tag pool is **used up** for sports and football, and movies is fading. The next source would be a new co-tag pass over today's ~1,250 new editors (free to build), at roughly the same $30–45 per 1,000 first-world. **$15 per 1,000 is not reachable** with hashtag walks plus eye checks; the eye check itself is the volume limit. |
| B | Mix | Danilo asked for 70% movies. Movies co-tags give the most creators per editor; football and sports are cheaper. This round followed the order's "cheapest first". |
| C | Second-look files | Send after a quick look (about 3 in 4 are real editors; the misses are lyric, mood and fan pages). |

## 1. Asked

Order 2026-10-15 21:29 (ALFRED for Dusan, 20:38: "get more leads you can do 30 dollars more dont spend a cent over that"): get more editor leads, a $30.00 hard cap, cheapest source first (sports learned tags), stop at $30.00. Reply with the number of new leads, total spent and where the leads are.

## 2. Money

Base: LamaTok request counter **234,164 at 21:29**; end **191,834** → 42,330 requests × $0.0006 = **$25.398**. Chain guard (`scratch/bl1649/chain49.py`): before each walk it reserves the walk cap ($1.20) plus feed calls ($1.30), plus the feeds of the processing still running, against a $29.80 limit, reading the vendor counter (never spend.json). The counter also counts other windows' calls, so the figure is an upper bound on this round.

## 3. Results per chunk

Editors = first-look EDITOR verdicts; unsure = sent to the second look. $ = walk + feed calls.

| run | source | new accounts | editors | unsure | first-world editors | US | $ | $ / 1,000 first-world |
|---|---|---|---|---|---|---|---|---|
| b49_sports_n01 | unfiltered learned co-tags | 3225 | 80 | 210 | 56 | 27 | 2.50 | 45 |
| b49_football_n01 | unfiltered learned co-tags | 2468 | 141 | 58 | 99 | 34 | 2.31 | 23 |
| b49_movies_k01 | named subjects only | 2698 | 84 | 137 | 67 | 25 | 2.46 | 37 |
| b49_sports_k01 | named subjects only | 1770 | 95 | 61 | 74 | 41 | 1.96 | 26 |
| b49_football_k01 | named subjects only | 1930 | 125 | 46 | 87 | 21 | 2.05 | 24 |
| b49_movies_k02 | named subjects only | 2262 | 92 | 117 | 71 | 28 | 2.21 | 31 |
| b49_sports_k02 | named subjects only | 667 | 36 | 32 | 27 | 14 | 0.78 | 29 |
| b49_football_k02 | named subjects only | 1523 | 146 | 49 | 76 | 20 | 1.88 | 25 |
| b49_movies_k03 | named subjects only | 2230 | 44 | 92 | 32 | 19 | 2.23 | 70 |
| b49_football_k03 | named subjects only | 1691 | 113 | 40 | 75 | 27 | 1.94 | 26 |
| b49_movies_k04 | named subjects only | 2033 | 83 | 63 | 60 | 31 | 2.12 | 35 |
| b49_football_k04 | named subjects only | 1231 | 55 | 21 | 32 | 12 | 1.49 | 47 |
| b49_medit_c16 | movies edit tags (BL-1645 list) | 116 | 8 | 9 | 3 | 1 | 0.61 | 204 |
| b49_medit_c17 | movies edit tags (BL-1645 list) | 339 | 9 | 8 | 6 | 3 | 0.83 | 139 |

The football co-tags carry many South American and Turkish club tags: football_k02 was 10% editors but only 52% first world (Argentina 17, Brazil 11).

## 4. Second look ($0)

935 unsure pages got one closer Sonnet look on the single full picture (`scratch/bl1646/unsure46.*`): **197 editors** (movies 91, sports 50, football 56), **140 first world**. These are delivered apart and labelled less sure.

## 5. What was learned

- **A learned co-tag list must be cut to named subjects before walking.** Generic words that editors also use (cities, countries, tech, gym, school, music genres) flood the walk with creators. Sonnet classification of the tag text ($0) fixed it: editors 2.6% → 6–10% of pages.
- **The eye check is the cost centre, not the vendor.** About 1.2M agent tokens per 80 sheets; this round used ~45M agent tokens for ~1,250 editors.
- Chains per niche share one pictures folder, so two processings must never run in the same niche folder at once (picture numbers continue the folder). The chain waits for its own processing; a new chain starts on a different niche.
- `finish46.py` now accepts wave names like `b1` (it only knew `w1`).

## 6. Code

`scratch/bl1649/`: tags49 (learned co-tags per niche), chain49 (walk + processing with a vendor-counter money guard and its own stop file), done49.sh (merge workflow outputs → deliver into a wave → first-world file), pertag49 (emails per tag, lesson 7), stats49, table49. `scratch/bl1646/finish46.py`: wave names `[a-z]?N`. No change to `clippershq/`.

- 05:20 FINDER BL-1649 more editors $30 cap: 869 first world (US 337) + 386 other for $25.40; $4.60 unspent on purpose (DONE)
