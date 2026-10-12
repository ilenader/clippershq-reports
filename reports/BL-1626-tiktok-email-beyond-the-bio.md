# BL-1626: the email beyond the bio: about $236 per 1,000 faceless, so I stopped at Step 0 ($0)

## Card

| | |
|---|---|
| **1. Faceless delivered** | **0** (bio path 0 / linked path 0). Your rule fired at Step 0: the linked path is estimated over $40 per 1,000. |
| **2. Spent** | **$0.** No vendor call: no LamaTok, no OpenRouter, no HikerAPI, no balance read. |
| **3. $ per 1,000 each path** | **Linked path, estimated: about $236 per 1,000 faceless** (optimistic $22, pessimistic $1,136). That counts only its extra steps; the hashtag pages are already paid by the bio path. If it paid its own pages: about $1,100. **Bio path, measured in BL-1625: $91.** |
| **4. Where linked emails would come from** | A hashtag item carries an **Instagram id on about 2.7%** of authors and a **YouTube channel on about 3.1%**. Twitter: 0. No bio link: that field is only on the profile endpoint, a separate paid call. `has_email` is always false, even on accounts that show an email in the bio. |
| **5. The deciding fact** | **Faceless editors almost never point elsewhere.** Of 99 eye-checked faceless bios, **4% mention Instagram, 0% YouTube, 0% a link page.** The other classes: non-editors 16%, freelancers 32%. A link marks a creator or freelancer, not a faceless edit page. |
| **6. Files** | `scratch/bl1626/` (fields0.py, links0.py, estimate0.py, estimate0.json). No lead file: nothing delivered. |

## Your decision

| | Question | My recommendation |
|---|---|---|
| A | The estimate has one weak input: how often faceless editors set the Instagram / YouTube **field** (not mentioned in their bio). It was never saved for them. | **A $0.12 probe settles it.** Re-buy the feeds of BL-1625's 95 delivered faceless editors and about 100 eye-checked non-editors (1 request each), and read their `ins_id` / `youtube_channel_id`. If faceless editors fill it at 10% or more, the linked path could reach the optimistic case (about $22 incremental). Below about 5%, close this idea for good. |
| B | Step 2's bio-only run with new fandom pools (K-drama, C-drama, Bollywood, Thai, J-pop) was not started, because your rule said stop. | Only if you accept about $60–100 per 1,000 (BL-1625's live sources after K-pop names ran dry). Say "run the bio path" and I'll do it with the $0.10 trials, the game filter and the plays pre-check. |

## 1. Asked

Find TikTok faceless editors whose email is **not** in the bio: Instagram, YouTube, bio links. $9 cap.
- **Step 0 (free):** which author fields are present, how often each class links out, and an estimate. **Stop and report if the estimate is over $40 per 1,000.**
- Then a $1.50 test, then a run to the cap.

## 2. Measured (free)

**0.1: what a TikTok author block carries.**
- BL-1625's `items.jsonl` kept only play count + date per item, not the author block.
- So I read every raw payload kept on disk instead: 1,706 files, 970 accounts.

| Field | Accounts with the key | Filled | Filled % |
|---|---:|---:|---:|
| `ins_id` (Instagram) | 264 | 7 | 2.7% |
| `youtube_channel_id` | 162 | 5 | 3.1% |
| `twitter_id` / `twitter_name` | 162 | 0 | 0% |
| `has_email` | 99 | 0 (false even on 3 accounts with an email in the bio) | 0% |
| `bio_link_click_action` | 98 | 0 | 0% |
| `bio_url` / `bioLink` | 18 / 1 | 18 / 1 | profile payloads only |

- **On hashtag-page items alone:** `ins_id` 3 of 39, YouTube 2 of 39. The fields are there, but the sample is small.
- `bio_url` never appears on hashtag or feed items, so a bio link needs an extra profile call per account.

**0.2: link mentions per eye-checked class** (BL-1622/1623/1625 verdicts, bio text):

| Class | n | Instagram | YouTube | Link page | Any |
|---|---:|---:|---:|---:|---:|
| **Faceless** | 99 | **4.0%** | **0%** | **0%** | **4.0%** |
| Not | 114 | 13.2% | 2.6% | 0.9% | 15.8% |
| Freelancer | 84 | 21.4% | 9.5% | 2.4% | 32.1% |
| Anime | 11 | 18.2% | 0% | 0% | 18.2% |
| Game | 12 | 8.3% | 0% | 0% | 8.3% |

- **Caveat 1:** every one of these accounts was found because its bio held an email.
- **Caveat 2:** this is the bio text, not the structured field (decision A measures the field).

**0.3: the estimate** (`estimate0.py`, per 1,000 new authors):

| | Central | Optimistic | Pessimistic |
|---|---:|---:|---:|
| Linked, no bio email | 56.5 | 84.7 | 39.5 |
| …of them faceless | 0.97 | 4.36 | 0.34 |
| …with an email found (YouTube description / IG bio) | 0.10 | 1.31 | 0.02 |
| Extra spend (1-cover pre-check, feed, judge, IG lookup) | $0.023 | $0.029 | $0.019 |
| **$ per 1,000 faceless (extra steps only)** | **$236** | **$22** | **$1,136** |
| $ per 1,000 if the path paid its own pages | $1,114 | $87 | $6,149 |

**How the central case is built:**
- P(faceless | link) = 4.0% × 7.5% ÷ 17.6% = **1.7%**: links are four times rarer on faceless editors than on email-bearing accounts in general.
- Email found on 10% of linked faceless: BL-1623 saw an email in 15% of YouTube edit-channel descriptions and estimated 5–10% for IG bios.
- **For comparison, the bio path gives 1.19 faceless per 1,000 new authors.**
- **The optimistic case** triples P(faceless | link), assumes 30% of emails are found, and adds 50% to the link rate. Even then it only beats $40 when the pages are free.

## 3. What I got wrong / limits

- The structured-field rates come from 264 / 162 author blocks spread across old probes, not from this round's editor pools.
- The faceless link rate comes from bios, not fields.
- **Both could be wrong by a factor of 2–3.** That is exactly why decision A is $0.12, not $1.50.
- The 1-cover pre-check (a) was never built or tested. No paid step ran, so a)–c) of Step 1 are untested.

## 4. Money and stores

**$0. No vendor call, no master / workbook / config write.** The only reads were bl1622/1623/1625 work files and raw payloads already on disk. Claimed and released as BL-1626.

## 5. Leak scan

Two-corpus scan (`scratch/bl1604/leak_adjudicate.py`, all committed files + this report): 23 hits, all explained by the public vocabulary; **0 unexplained, 0 leaks**. Secret scan: run at publish.

## 6. Paths

`scratch/bl1626/` (common.py, fields0.py, links0.py, estimate0.py, estimate0.json)
