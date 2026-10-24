# BL-1700: the three free tests from the cost audit (Dusan's yes, 24 Oct 16:34) -- $0, reads on the 3090

Background: BL-1697 found one real editor costs ~42 LamaTok requests on the main method (27.6 hashtag pages + 14.8
picture-check feeds), $25 per 1,000. These tests ask which of those requests can become free. **No LamaTok call was made**;
the 3090 read TikTok's own public web pages (its IP, plain HTTP): 6 probe accounts x 3 reads, then 100 + 200 reads.
Labels = 4,378 pages checked on 23 Oct (runs k3-k5, q1-q3), 367 of them real editors. Tool: `scratch/bl1700/lab1700.py`.

## Test 1 -- can the picture check be free? YES for the covers
The profile **embed** page (`tiktok.com/embed/@handle`) on the 3090 returns the account's latest ~12 videos with covers, free.
(The profile page itself carries no videos; the unsigned post-list API returns empty.)

| sample (23 Oct pages) | fetched | videos in the paid feed | videos in the free embed | same video ids | >= 9 (or all) the same |
|---|---|---|---|---|---|
| real editors | 50/50 | 11.2 | 12.3 | 9.9 | 43 |
| rejected pages | 48/50 | 11.5 | 12.6 | 9.4 | 36 |

The gap is time: the paid feeds were bought on 23 Oct, the embed shows today's newest posts. Same videos -> same covers ->
the same picture for the eyes. **Open:** the embed shows no photo-post marker (0 of 98 accounts), so the "photos > 30% out"
part of the filter needs another free signal (or the page is judged on videos only) -- not solved yet.
Free reads have a limit: the 22 Oct profile re-read got 403 after 14,548 reads, so a big run must be spread over time/IPs.

## Test 2 -- can we tell rich tags before paying? NO
A co-tag's co-use count (how many real editors used it -- known before the walk) does not forecast real editors per call:

| co-use count | tags | hashtag calls | new-email pages checked | real | real per 100 calls | real share of checked |
|---|---|---|---|---|---|---|
| 1 | 333 | 1,304 | 651 | 68 | 5.21 | 10.4% |
| 3-4 | 1,024 | 3,965 | 2,368 | 172 | 4.34 | 7.3% |

And yield falls round by round as the co-tag pool is used: real per 100 hashtag calls k3-k5 ~4.1, q1 4.0, q2 3.6, q3 2.5,
q4 2.1. Hashtag pages stay ~25-28 calls per real editor whatever we pick.

## Test 3 -- can we skip private following lists for free? YES, exactly
The profile page's `followingVisibility` (free) against the paid outcome of the same following-list call:

| followingVisibility | list was public (paid call returned users) | list was private (paid call 403) |
|---|---|---|
| 1 | 99 | 0 |
| 2 | 0 | 99 |
| (profile read failed) | 1 | 1 |

198 of 198 correct. 48% of the 22-23 Oct following calls (1,186 of 2,453) went to private lists; all avoidable.

## What it does to the price (same filter, from the 22-23 Oct actuals)
| route | requests per real editor today | with tests 1 + 3 | $ per 1,000 real |
|---|---|---|---|
| following lists of real editors (f3: 1,500 seeds -> 96 real) | 29.4 | 8.4 (805 public lists, covers free) | **$5.0** |
| following lists (f4: 953 seeds -> 44 real) | 38.0 | 10.5 (462 public lists) | $6.3 |
| co-tag hashtag walks (k3-q4) | 42.4 | 27.6 (covers free) | $16.6 |

**$5 per 1,000 is reached on the following-list route** -- but that route is small: ~5 real editors per 100 seeds, one page
of following per seed, and ~2,600 proven editors were already used as seeds. The ~530 real editors found since f4 would
give ~26 more. To reach 1,000 it needs more per seed (page 2+ of each public following list -- not measured) or the
co-tag walks at ~$17 per 1,000.

## Next (each step on Dusan's yes; $ only where marked)
1. ($0) Build the free picture path on the 3090: embed covers -> the same sheets -> the same eyes; solve the photo-share
   signal; re-check 100 known pages end to end (same verdicts as the paid pictures?).
2. ($0.30 cap, needs yes) Following lists, page 2-3, for ~150 PUBLIC seeds (free check first) + free covers: real editors
   per call. If it holds near $5-6 per 1,000, this is the route; seeds are the limit.
3. ($1 cap, needs yes) One co-tag chunk with free covers to confirm ~$17 per 1,000 for the bulk.
