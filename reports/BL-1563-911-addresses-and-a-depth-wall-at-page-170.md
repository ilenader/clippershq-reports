# BL-1563 — 911 net-new addresses, a depth wall at page 170, and the editor rate this round could not measure

**Round:** BL-1563 · **Endpoint:** LamaTok v2 hashtag · **Unit:** `api.cost_per_call_usd`
= $0.00060000, read by named key (never `ig_api`'s $0.00069064)

## The one-line answer

The round was killed mid-walk, resumed from its checkpoint without re-paying for a single
completed tag, and delivered **911 net-new TikTok addresses for $4.15320** — 89 short of
1,000. **The cap did not bind.** $0.85 of the $5.00 was still unspent when the vendor stopped
serving: the last tag sat blocked on the wire for ~50 minutes after a steady 28 pages/min all
day. What stopped this round was throughput, not money.

The address rate came in at **2.12% of kept accounts** [1.74–2.50] against the
**3.08%** the round was planned at — a 1.46x miss that compounds: the next 1,000 costs
**$7.13**, not the $4.56 the round average implies.

All 911 addresses are **in `master_leads.csv`**, which went 73,166 → 74,074 rows
(+908 accounts), introducing **zero** duplicate handles.

## Where the round actually was when it restarted

| | |
|---|---|
| Claim `.claims/BL-1563.json` | OPEN, mine |
| Commits for the round | **none** — nothing had been committed |
| Report on the reports remote | **none**; publishing was current through BL-1562 |
| Reports clone on disk | **absent again** (third disappearance) — re-cloned |
| Checkpoint | 72 tags, 879 net-new, authoritative |
| `master_leads.csv` | **73,166 rows, untouched** — no write had happened |
| Ledger | **zero BL-1563 rows — $3.94560 was off the books** |

The stores were compared against the round-start backups by **shape-aware** row count — a
dict-only reader calls `tiktok_pages_seen.json` 3 rows when its body is a 3,270-entry dict
under `pages`. All ten matched, with one expected exception: `email_harvest_tags.json` had
grown by exactly **+72 tags**, matching the 72 in the checkpoint. Nothing was half-written.

### The money was metered but unbooked

The walker meters at the wrapper (`LockedBudget`) and writes **nothing** to the ledger —
the same omission that left BL-1557's $0.26866 off the books. The pre-crash spend was
reconstructed from the two session counters (83 + 6,493 calls), booked as one row, and
verified by re-reading `spend.json`. Then the walker was **patched to book per tag**, and
that fix immediately proved itself: the run was interrupted twice more and **the money
survived both times**.

## The three checks, before resuming

**The guard.** `DedupGuard.build()` reads addresses from master but **not accounts** — driven
directly, a default build returns **0 accounts** and 12,886 addresses. Built as the walker
builds it: **73,148 accounts, 12,886 addresses**. Polarity control passed on known values:
`claim_address(held)` → `'already in master or an earlier round'`, `claim_address(fresh)` →
`None`. Refuse is a **string**; fine is `None`. `if guard.claim_address(e)` keeps only
duplicates.

**The row file.** 908 lines, **908 distinct account ids**, 911 distinct addresses — a
lines-minus-ids gap of **0**. The 106-lines-for-71-ids pathology did not recur.

**The prerequisites, re-derived rather than read.** v2 supply against the plain endpoint on
the 72 comparable tags: **7.12x pooled** (704.4 vs 98.9 accounts per tag), median 6.83x —
the claim's ~7.5x holds. All 406 planned tags were in the round-start ledger and **zero**
carried a v2 record. The bio field is `signature`: driving `account_row` with `biography`
instead returns `bio_state='unknown'`, `has_email=False`.

But the 7.12x is **not evenly spread**. 49 tags grew (9.9x, 884 net-new); **23 tags shrank on
v2 and produced 2 net-new between them.** A third of the supply was worth less on the
richer endpoint.

## Yield per tag, and where each one stopped

Tags walked: **75**. Dead (zero net-new): **25** (33.33%).

| tag | pages | kept | NET-NEW | how it stopped |
|---|---|---|---|---|
| `deadpooledit` | 169 | 1521 | **68** | DEPTH WALL at page 169 -- NOT drained |
| `squidgameedit` | 169 | 1467 | **64** | DEPTH WALL at page 169 -- NOT drained |
| `lebronedit` | 170 | 1421 | **56** | DEPTH WALL at page 170 -- NOT drained |
| `ironmanedit` | 170 | 1107 | **54** | DEPTH WALL at page 170 -- NOT drained |
| `charlesleclercedit` | 171 | 1122 | **47** | DEPTH WALL at page 171 -- NOT drained |
| `narutoedit` | 171 | 1303 | **41** | DEPTH WALL at page 171 -- NOT drained |
| `haalandedit` | 170 | 1065 | **36** | DEPTH WALL at page 170 -- NOT drained |
| `tonystarkedit` | 171 | 1320 | **31** | DEPTH WALL at page 171 -- NOT drained |
| `stephcurryedit` | 170 | 1240 | **30** | DEPTH WALL at page 170 -- NOT drained |
| `cobrakaiedit` | 169 | 814 | **28** | DEPTH WALL at page 169 -- NOT drained |

Four different endings, never collapsed into one:

| ending | tags | meaning |
|---|---|---|
| drained (empty list below the wall) | 40 | genuinely exhausted |
| **depth wall (page ≥165)** | **33** | **not drained — the feed stops serving** |
| dry-page saturation | 1 | the 3-dry-pages rule |
| cut by the cap, recorded done | 1 | see below |

### The depth wall is the structural finding

**33 tags stopped between page 168 and 171 and not one went beyond.** They carry most of
the round's kept accounts and **822 of its 911 net-new addresses**. Their supply is *not*
exhausted — the endpoint simply stops serving past ~page 170 (~2,000–2,800 items). Anything
deeper in those tags is unreachable on this endpoint at any price. The round's premise was
"walked but not drained"; the correct statement is that v2 reaches ~7x deeper than the plain
endpoint **and then hits its own ceiling**.

The body-hash saturation instrument **never fired once** — 0 repeat bodies in 75 tags. It
is carrying no weight and has never been shown to work on this endpoint.

### A cap-truncated tag is recorded as done

`nightwingedit` was cut at page 42 by a $0.05 smoke-test cap after yielding 14 net-new — one
of the best rates in the round. `tags_done` does not distinguish "walked out" from "cut
off", so every later resume skipped it. **A truncated tag is silently retired.**


**The dead tags — accounts bought for zero addresses:**

| tag | pages | kept | how it stopped |
|---|---|---|---|
| `giyuedit` | 170 | 1093 | DEPTH WALL at page 170 -- NOT drained |
| `warrioredit` | 33 | 198 | drained: feed returned an empty list at page 33 |
| `riceedit` | 13 | 98 | drained: feed returned an empty list at page 13 |
| `whisedit` | 16 | 97 | drained: feed returned an empty list at page 16 |
| `martinezedit` | 21 | 83 | drained: feed returned an empty list at page 21 |
| `bulledit` | 8 | 51 | drained: feed returned an empty list at page 8 |
| `kroosedit` | 7 | 49 | drained: feed returned an empty list at page 7 |
| `mainooedit` | 7 | 44 | drained: feed returned an empty list at page 7 |
| `gothamcityedit` | 10 | 40 | drained: feed returned an empty list at page 10 |
| `runningmanedit` | 21 | 40 | dry-page saturation at page 20 |
| `starshipedit` | 4 | 33 | drained: feed returned an empty list at page 4 |
| `ultravioletedit` | 5 | 30 | drained: feed returned an empty list at page 5 |

## The six duplicate counts, separately

| # | count | n |
|---|---|---|
| 1 | account sightings **refused** by the guard, before the bio was read | **50318** |
| 2 | accounts **kept** (passed the guard) | 43048 |
| 3 | kept accounts carrying ≥1 address | 945 |
| 4 | kept accounts whose addresses were **all already held** | 37 |
| 5 | within-run duplicate **row lines** | **0** |
| 6 | **net-new addresses shipped** | **911** |

Denominator: **93366 account sightings** through the chokepoint, refusal rate **53.89%**.
The guard refused more than half of everything it saw.

**Count 1 is conflated and this round cannot split it.** `skipped_accounts` merges three
different refusals — a re-sighting later in the same tag, an account kept under an earlier
tag, and an account already in master. `DedupGuard.counts` keeps them apart, but it lives in
the process and every one of this round's processes was killed. *Next round: dump
`guard.report()` after every tag. It is free.*

## The cost table

| | |
|---|---|
| unit (`api.cost_per_call_usd`, by named key) | $0.00060000 |
| calls | **6922** |
| spend | **$4.15320** of a $5.00 cap |
| booked to `spend.json` | 6922 calls |
| ledger rows `run_id=bl1563` | 6922 calls / $4.15320 |
| **three-way control** | **counter == checkpoint == ledger** |
| accounts kept | 43048 |
| **kept accounts per call** | **6.22** |
| addresses on kept accounts | 945 |
| net-new addresses | **911** |
| $ per 1,000 accounts kept | $0.0965 |
| **$ per 1,000 net-new addresses** | **$4.56** |

**And the money nobody can count.** Every interruption left one tag in flight whose calls
were paid for and never recorded — the checkpoint and the ledger are both written *after* a
tag completes, so a tag that never completes is invisible to both. With 4 interrupted
processes and a 200-page ceiling, that is **$0 – $0.4800 unrecoverable**, giving a worst-case
true spend of **$4.63320**. The $5.00 cap is not breached under any accounting. The bound is
reported and deliberately **not booked**: an estimate must not sit in the money ledger beside
counted calls.

Gross address rate **2.20%**; net-new **2.12%**. Cluster-bootstrapped over tags —
the honest interval, because accounts arrive in tags and a pooled Wilson is 1.1–1.7x too
narrow on clustered data — the net-new rate is **2.11% [1.74–2.50]**.

**The round was planned against 3.08%. It came in at 2.11%.** That is the single number
that moves every projection.

## The decay, and what the next 1,000 costs

| quarter of the walk | tags | kept | net-new | kept/call | $/1k net-new |
|---|---|---|---|---|---|
| Q1 | 18 | 8575 | 173 | 6.11 | $4.87 |
| Q2 | 18 | 14206 | 404 | 6.59 | $3.20 |
| Q3 | 18 | 9821 | 176 | 6.47 | $5.18 |
| Q4 | 18 | 8224 | 126 | 5.49 | $7.13 |

| projection basis | calls | cost |
|---|---|---|
| round average (0.13161 net-new/call) | 7598 | $4.56 |
| **last quarter (0.08416/call)** | **11883** | **$7.13** |

The average **understates the next 1,000 by 1.56x**. And the last quarter is *itself* an
overestimate of what remains: every address collected this round enlarged the store the
guard dedups against, and the supply was walked best-first off a recorded-yield table — the
next 1,000 comes off tags that table ranked lower. **6.22 kept accounts per call is the dedup
guard working, and it will keep falling.**

## The editor rate — what this round cannot say

**75 of 908, 8.26% [6.64–10.23], on `name_rule` alone.**

This is **not** the largest sample anyone has had on the editor question, and it must not be
used to reconcile the four disagreeing priors (6.59, 13.33, 22.54, 29.37%). It is **half a
gate run on a population selected by the other half**:

* **The bio is gone, so this is a floor.** The walker persisted `bio_len` and not the bio, so
  `bio_rule` cannot run on a single one of these 908 accounts and `gate()` collapses to
  `name_rule`. Every editor who says so in the bio but not the handle is counted as a
  non-editor. **The bio ships free in the hashtag payload and was thrown away.**
* **The frame selects for the surviving half, pushing the other way.** All 75 tags end in
  `edit` and `name_rule` fires on `edit` in a *handle*.

The two biases oppose each other and neither is measured, so the sign of the net error is
unknown — but the result lands *below* all four priors, so the missing bio dominates. That
is a fact about the instrument, not about the editor rate. **The four priors remain
unreconciled.** The walker has since been patched to persist the bio.

## What I got wrong in this round

* **I ran two walkers against one checkpoint and one budget for ~50 minutes.** The cause was
  a false liveness test: `kill -0 <pid>` in Git Bash cannot see a native Windows PID and
  reported EXITED for a process that was running, so I relaunched a "dead" walker that was
  mid-tag. Both spent against the same $5.00 cap and raced on `walk_state.json`. The
  checkpoint's `sessions` list was clobbered last-writer-wins; `calls_booked` and the ledger
  survived only because both are monotonic and written per tag. Fixed with an `O_EXCL`
  single-instance lock that refuses to start and names the right liveness test.
* **I diagnosed three "silent kills" that were not kills.** Two of the three processes were
  alive the whole time.
* The in-flight tag of each interrupted walker was re-walked, so the round paid twice for
  at most ~170 calls (~$0.10) per interruption. That is the only re-payment; no completed
  tag was ever re-walked.

## What to fix before the next walk

1. **Dump `guard.report()` per tag** — splits duplicate count 1 into its three real parts, free.
2. **Keep the bio** (done) — it is the difference between measuring the editor rate and not.
3. **Mark cap-truncated tags as resumable**, or `nightwingedit` stays retired at page 42.
4. **Book at the wrapper, not in the caller** — this walker had to be patched to book at all,
   and it is the third round to find the same hole.
5. **Stop trusting the body-hash saturation detector** until it fires once.

## Appendix — every tag, in walk order

| # | tag | pages | supply | kept | addr | NET-NEW | how it stopped |
|---|---|---|---|---|---|---|---|
| 1 | `troymovieedit` | 4 | 8 | 8 | 0 | **0** | drained: feed returned an empty list at page 4 |
| 2 | `frenkiedejongedit` | 34 | 176 | 173 | 1 | **1** | drained: feed returned an empty list at page 34 |
| 3 | `nightwingedit` | 42 | 400 | 334 | 14 | **14** | CUT BY THE CAP at page 42 -- NOT drained, and recorded done |
| 4 | `stephcurryedit` | 170 | 1266 | 1240 | 31 | **30** | DEPTH WALL at page 170 -- NOT drained |
| 5 | `cobrakaiedit` | 169 | 921 | 814 | 35 | **28** | DEPTH WALL at page 169 -- NOT drained |
| 6 | `kobebryantedit` | 122 | 917 | 826 | 9 | **9** | drained: feed returned an empty list at page 122 |
| 7 | `mainooedit` | 7 | 45 | 44 | 0 | **0** | drained: feed returned an empty list at page 7 |
| 8 | `ichigoedit` | 169 | 1353 | 1081 | 23 | **22** | DEPTH WALL at page 169 -- NOT drained |
| 9 | `ultravioletedit` | 5 | 32 | 30 | 0 | **0** | drained: feed returned an empty list at page 5 |
| 10 | `tonystarkedit` | 171 | 1470 | 1320 | 36 | **31** | DEPTH WALL at page 171 -- NOT drained |
| 11 | `viniciusedit` | 58 | 453 | 447 | 3 | **3** | drained: feed returned an empty list at page 58 |
| 12 | `saltmovieedit` | 2 | 9 | 9 | 1 | **1** | drained: feed returned an empty list at page 2 |
| 13 | `shazamedit` | 126 | 702 | 651 | 12 | **11** | drained: feed returned an empty list at page 126 |
| 14 | `heatmovieedit` | 4 | 23 | 21 | 0 | **0** | drained: feed returned an empty list at page 4 |
| 15 | `michaelcorleoneedit` | 111 | 518 | 483 | 9 | **9** | drained: feed returned an empty list at page 111 |
| 16 | `truedetectiveedit` | 170 | 1025 | 906 | 13 | **13** | DEPTH WALL at page 170 -- NOT drained |
| 17 | `westbrookedit` | 20 | 174 | 155 | 1 | **1** | drained: feed returned an empty list at page 20 |
| 18 | `starshipedit` | 4 | 33 | 33 | 0 | **0** | drained: feed returned an empty list at page 4 |
| 19 | `muzanedit` | 171 | 1192 | 1018 | 12 | **12** | DEPTH WALL at page 171 -- NOT drained |
| 20 | `deadpooledit` | 169 | 1843 | 1521 | 69 | **68** | DEPTH WALL at page 169 -- NOT drained |
| 21 | `venomedit` | 168 | 1479 | 1208 | 30 | **28** | DEPTH WALL at page 168 -- NOT drained |
| 22 | `narutoedit` | 171 | 1602 | 1303 | 43 | **41** | DEPTH WALL at page 171 -- NOT drained |
| 23 | `powerchainsawedit` | 2 | 4 | 3 | 0 | **0** | drained: feed returned an empty list at page 2 |
| 24 | `warrioredit` | 33 | 230 | 198 | 0 | **0** | drained: feed returned an empty list at page 33 |
| 25 | `ironmanedit` | 170 | 1776 | 1107 | 58 | **54** | DEPTH WALL at page 170 -- NOT drained |
| 26 | `arsenaledit` | 169 | 608 | 577 | 10 | **10** | DEPTH WALL at page 169 -- NOT drained |
| 27 | `haalandedit` | 170 | 1109 | 1065 | 37 | **36** | DEPTH WALL at page 170 -- NOT drained |
| 28 | `donovanmitchelledit` | 12 | 104 | 83 | 2 | **2** | drained: feed returned an empty list at page 12 |
| 29 | `luffyedit` | 169 | 1296 | 1013 | 18 | **18** | DEPTH WALL at page 169 -- NOT drained |
| 30 | `squidgameedit` | 169 | 1782 | 1467 | 67 | **64** | DEPTH WALL at page 169 -- NOT drained |
| 31 | `saulgoodmanedit` | 171 | 1234 | 1039 | 21 | **20** | DEPTH WALL at page 171 -- NOT drained |
| 32 | `jokeredit` | 169 | 1289 | 1006 | 21 | **20** | DEPTH WALL at page 169 -- NOT drained |
| 33 | `sukunaedit` | 169 | 1593 | 1151 | 26 | **25** | DEPTH WALL at page 169 -- NOT drained |
| 34 | `bulledit` | 8 | 52 | 51 | 0 | **0** | drained: feed returned an empty list at page 8 |
| 35 | `ghostintheshelledit` | 41 | 417 | 385 | 6 | **6** | drained: feed returned an empty list at page 41 |
| 36 | `mavericksedit` | 2 | 13 | 11 | 0 | **0** | drained: feed returned an empty list at page 2 |
| 37 | `gothamcityedit` | 10 | 49 | 40 | 0 | **0** | drained: feed returned an empty list at page 10 |
| 38 | `runningmanedit` | 21 | 40 | 40 | 0 | **0** | dry-page saturation at page 20 |
| 39 | `shangchiedit` | 171 | 1413 | 1162 | 24 | **24** | DEPTH WALL at page 171 -- NOT drained |
| 40 | `jetliedit` | 5 | 30 | 27 | 0 | **0** | drained: feed returned an empty list at page 5 |
| 41 | `lebronedit` | 170 | 1661 | 1421 | 57 | **56** | DEPTH WALL at page 170 -- NOT drained |
| 42 | `banebatmanedit` | 2 | 2 | 2 | 0 | **0** | drained: feed returned an empty list at page 2 |
| 43 | `redsparrowedit` | 4 | 20 | 18 | 0 | **0** | drained: feed returned an empty list at page 4 |
| 44 | `deadpoolwolverineedit` | 21 | 181 | 157 | 4 | **4** | drained: feed returned an empty list at page 21 |
| 45 | `kevindurantedit` | 85 | 744 | 546 | 6 | **6** | drained: feed returned an empty list at page 85 |
| 46 | `captainamericaedit` | 171 | 1485 | 909 | 21 | **20** | DEPTH WALL at page 171 -- NOT drained |
| 47 | `erwinedit` | 142 | 883 | 812 | 5 | **5** | drained: feed returned an empty list at page 142 |
| 48 | `inumakiedit` | 170 | 1734 | 1462 | 18 | **18** | DEPTH WALL at page 170 -- NOT drained |
| 49 | `nightcrawleredit` | 171 | 1505 | 1166 | 16 | **17** | DEPTH WALL at page 171 -- NOT drained |
| 50 | `tombraideredit` | 169 | 951 | 797 | 17 | **16** | DEPTH WALL at page 169 -- NOT drained |
| 51 | `enterthedragonedit` | 2 | 8 | 6 | 0 | **0** | drained: feed returned an empty list at page 2 |
| 52 | `inosukeedit` | 170 | 1509 | 1152 | 10 | **10** | DEPTH WALL at page 170 -- NOT drained |
| 53 | `scholesedit` | 2 | 7 | 7 | 0 | **0** | drained: feed returned an empty list at page 2 |
| 54 | `whisedit` | 16 | 106 | 97 | 0 | **0** | drained: feed returned an empty list at page 16 |
| 55 | `magnetoedit` | 171 | 1323 | 979 | 16 | **15** | DEPTH WALL at page 171 -- NOT drained |
| 56 | `manutdedit` | 75 | 380 | 366 | 1 | **1** | drained: feed returned an empty list at page 75 |
| 57 | `rockyedit` | 171 | 1123 | 979 | 13 | **13** | DEPTH WALL at page 171 -- NOT drained |
| 58 | `zenitsuedit` | 169 | 1495 | 950 | 16 | **16** | DEPTH WALL at page 169 -- NOT drained |
| 59 | `darkmanedit` | 2 | 8 | 7 | 0 | **0** | drained: feed returned an empty list at page 2 |
| 60 | `giyuedit` | 170 | 1327 | 1093 | 0 | **0** | DEPTH WALL at page 170 -- NOT drained |
| 61 | `jasonbourneedit` | 7 | 38 | 30 | 1 | **1** | drained: feed returned an empty list at page 7 |
| 62 | `martinezedit` | 21 | 88 | 83 | 0 | **0** | drained: feed returned an empty list at page 21 |
| 63 | `kroosedit` | 7 | 50 | 49 | 0 | **0** | drained: feed returned an empty list at page 7 |
| 64 | `paulgeorgeedit` | 33 | 267 | 173 | 6 | **6** | drained: feed returned an empty list at page 33 |
| 65 | `riceedit` | 13 | 114 | 98 | 0 | **0** | drained: feed returned an empty list at page 13 |
| 66 | `matrixreloadededit` | 2 | 3 | 2 | 0 | **0** | drained: feed returned an empty list at page 2 |
| 67 | `charlesleclercedit` | 171 | 1172 | 1122 | 47 | **47** | DEPTH WALL at page 171 -- NOT drained |
| 68 | `frankyedit` | 61 | 430 | 352 | 3 | **3** | drained: feed returned an empty list at page 61 |
| 69 | `totalrecalledit` | 2 | 10 | 9 | 0 | **0** | drained: feed returned an empty list at page 2 |
| 70 | `batmanbeyondedit` | 64 | 606 | 490 | 6 | **6** | drained: feed returned an empty list at page 64 |
| 71 | `barcelonaedit` | 171 | 859 | 780 | 9 | **9** | DEPTH WALL at page 171 -- NOT drained |
| 72 | `tanjiroedit` | 171 | 1328 | 662 | 9 | **9** | DEPTH WALL at page 171 -- NOT drained |
| 73 | `lewishamiltonedit` | 168 | 1021 | 987 | 21 | **21** | DEPTH WALL at page 168 -- NOT drained |
| 74 | `saitamaedit` | 169 | 1298 | 1208 | 11 | **11** | DEPTH WALL at page 169 -- NOT drained |
| 75 | `collateraledit` | 6 | 38 | 27 | 0 | **0** | drained: feed returned an empty list at page 6 |

---
*911 net-new addresses across 908 distinct accounts are in
`scratch/bl1563/walk_rows.jsonl` and have been appended to `master_leads.csv`
(73,166 → 74,074 rows, zero duplicate handles introduced).*
