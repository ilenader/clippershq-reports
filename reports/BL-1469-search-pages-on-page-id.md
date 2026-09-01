# BL-1469 — `/v2/search` paginates. It always did. We were sending the wrong parameter.

# IS THE FUNNEL SAFE TO RUN? **YES.**

Nothing in this round changed what the funnel spends per call, what it rejects, or what it
delivers. The one behavioural change — TikTok keyword search now fetches every page instead of
only the first — **is written but NOT committed**, because the file it lives in is claimed by
another round. The funnel on disk today behaves exactly as it did before this round started.

Two standing cautions, neither introduced here and both explained in §6:

* **The lifetime spend cap cannot see LamaTok money spent through the client directly.** It is
  computed from a ledger that the LamaTok client never writes to. The cap still works for
  everything that goes through a funnel run; it is blind to probe scripts.
* This round's own vendor spend, **$0.0480**, is real and does not appear in that ledger.

---

## 1. ROUND ID, DATE, AND THE TASK

**BL-1469 — measured 2026-08-31, published 2026-09-01.**

The vendor (LamaTok) confirmed that their TikTok keyword-search endpoint `/v2/search` supports
pagination: you take a value called `next_page_id` out of each response and send it back as
`page_id` to get the next page. They also said the parameter we were actually using, `offset`, is
deprecated and *"on its own cannot page."* I was asked to find out what the funnel sends today,
measure whether `page_id` really pages and how deep, re-check whether asking for 30 results per
call beats 20, check whether search results carry the free profile bio, and cost it all out per
1,000 delivered pages — with a $0.50 vendor cap and a hard ceiling of 100 sampled pages.

**Why it matters:** the funnel's best-performing supply surface (Instagram reels) cannot paginate
at all and is therefore capped forever. Search is the second-best surface. If search pages, the
better half of the supply stops being a dead end.

---

## 2. WHAT ACTUALLY SHIPPED

⚠️ **NOTHING IS COMMITTED TO THE FUNNEL YET.** All code below is written, tested and verified
against the live vendor, but two files are **held pending a handover** (see §4). What IS committed
is this round's evidence and report.

| change | file:line | what it does |
|---|---|---|
| `SEARCH_MAX_COUNT = 30` | `api_client.py:56` | the documented maximum; the clamp was `min(50, ...)`, **above** what the vendor documents |
| `search()` gains `page_id` | `api_client.py:375` | sends the cursor, and **drops `offset` when paging** — the vendor documents `offset` as naming a *different* search, so sending both sends two questions |
| `_next_page_id()` | `tiktok_finder.py` (new) | finds the cursor anywhere in the response, because the vendor publishes **no response schema at all** — every documented 200 is an empty object |
| `videos_from_search()` walks to exhaustion | `tiktok_finder.py:393` | three stop conditions: empty page, repeated page, no cursor |
| cost model corrected | `tiktok_finder.py:1599` | `search_videos_per_call` 20 → 27 (n=19); new `search_authors_per_keyword` = 134 (n=3) |
| the stale comment replaced | `tiktok_finder.py:2037` | it said *"ONE CALL AND NO MORE… this loop deliberately has no cursor"* |

### HOW IT WAS PROVED — a live run against the real vendor, with a control

Not a grep, not a docstring, not a passing test. **The shipped function was called against the
live vendor and the billed requests were counted**, with a positive control that constrains the
walk to one page so the two arms must differ:

```
CONTROL  max_pages=1     ->  1 billed request,  30 videos,  30 distinct authors
FULL     to exhaustion   ->  6 billed requests, 132 videos, 125 distinct authors
found_via tagged on every video across all six pages: True
```

**If the counter were measuring nothing, both arms would report the same number.** They do not.

A second live check compared my own call counter against the client's internal HTTP counter, which
counts retries:

```
keyword "baller quotes"   my count 6   client http_requests 6   unexpected statuses 0
```

**Unit tests exist but are explicitly NOT offered as proof of wiring:** 15 new tests and 480 across
every module that imports either changed file (1 pre-existing failure, unrelated — a test file that
imports a sibling module only resolvable when run from inside its own directory).

---

## 3. WHAT WAS MEASURED

Every rate below carries its denominator and a Wilson 95% interval. **MEASURED** = observed this
round. **DERIVED** = computed from measured numbers.

### 3a. What the funnel sends today

**Every TikTok keyword-search call this funnel has ever made returned page 1.** `MEASURED` by
reading the shipped code: the client sent `{keyword, count, offset}` and no cursor; the one caller
passes no offset (defaulting to 0) and a second hardcodes 0. The discovery loop's own comment said
it had *"deliberately no cursor."*

The vendor's live specification (fetched unauthenticated, **$0.00**) states:

> `offset` — *"Superseded by page_id. On its own it cannot page: results past the first page belong
> to a search this parameter does not name."*

**The earlier round that tested `offset` measured it correctly** — 20 items at offset 0, zero
beyond, no error — **and drew the wrong conclusion from a correct measurement.** The endpoint
paginated the whole time, on a parameter nobody sent.

### 3b. Does `page_id` page?

Three keywords walked to exhaustion at 20 results per call. **Validated on the number of records
returned, never on the HTTP status** — a sibling endpoint has previously returned HTTP 200, charged,
with an empty body and no error to catch.

| keyword | billed pages | distinct videos | distinct authors | why it stopped | |
|---|---:|---:|---:|---|---|
| motivation quotes | 10 | 156 | 136 | repeat detected | `MEASURED` |
| relatable memes | 8 | 131 | 103 | no cursor returned | `MEASURED` |
| movie edits | 8 | 122 | 104 | no cursor returned | `MEASURED` |

Net-new authors per page do not decay: the first keyword ran 17, 18, 16, 12, 13, 17, 13, 13, 17
across its nine productive pages. `MEASURED`

**Per-page latency, n = 33 billed pages** `MEASURED` — median **2.94 s**, p90 **3.67 s**, max
**4.29 s**, min **1.51 s**. Median and tail reported separately because the mean hides the tail.

### 3c. Are the extra pages actually new accounts?

Two denominators, both named, because pooling them is how this project once published a supply
problem as a dedup problem.

* **"seen store"** = the file the TikTok funnel checks to avoid re-offering a page. **2,459 handles.**
* **"master"** = the full lead table ever written. **72,935 handles.**

| | count | rate | Wilson 95% | |
|---|---:|---:|---|---|
| net-new vs **seen store** | 216 of 265 | **81.5%** | **[76.4, 85.7]** | `MEASURED` |
| net-new vs **master** | 241 of 265 | **90.9%** | **[86.9, 93.8]** | `MEASURED` |

**And the result that decides whether paging is worth buying** — net-new against the seen store, by
page depth, two keywords: `MEASURED`

| page | keyword A | keyword B |
|---:|---|---|
| 1 | 17 of 24 | 23 of 29 |
| 2 | 17 of 28 | 22 of 24 |
| 3 | 12 of 28 | 24 of 29 |
| 4 | 19 of 29 | **29 of 29** |
| 5 | 19 of 27 | **29 of 30** |
| 6 | 7 of 7 | 8 of 8 |

**Pages 2 and beyond are MORE net-new than page 1, not less** — because page 1 is exactly the part
this funnel has already harvested on every previous run.

### 3d. Does asking for 30 per call beat 20?

Same keyword, same single billed request, 20 versus 30: `MEASURED`

| keyword | records 20 → 30 | distinct authors 20 → 30 |
|---|---|---|
| sad quotes | 20 → 30 | 20 → 27 |
| football quotes | 20 → 30 | 10 → 14 |
| car edits | 20 → 28 | 19 → 27 |
| velocityedit | 18 → 27 | 16 → 25 |
| **pooled** | **78 → 115 = +47.4%** | **65 → 93 = +43.1%** |

⚠️ **BUT IT DOES NOT COMPOSE WITH PAGING, AND I CHECKED RATHER THAN ASSUMED.** The same keyword
walked to exhaustion at both settings: `MEASURED`

```
count=20   10 billed pages   156 videos   136 authors
count=30    7 billed pages   155 videos   137 authors
```

**The result set is fixed at roughly 155 videos per keyword. Asking for 30 reaches the same pool in
7 calls instead of 10.** The gain is **30% fewer calls for the same supply**, not 47% more supply.
Multiplying the two measurements together would have overstated a keyword's yield by about half.

### 3e. Do search results carry the free profile bio? No.

| | count | rate | Wilson 95% | |
|---|---:|---:|---|---|
| search results carrying a bio field | **0 of 845** | **0.0%** | **[0.00, 0.45]** | `MEASURED` |

**A zero is uninterpretable without proof the detector can fire**, so two controls ran, and the same
code did the counting:

| control | result | |
|---|---|---|
| the hashtag endpoint, bio field present | **28 of 28 = 100.0% [87.9, 100.0]** | `MEASURED` |
| the hashtag endpoint, bio non-empty | **24 of 28 = 85.7% [68.5, 94.3]** | `MEASURED` |
| a synthetic record with a planted bio | detector read it back correctly | `MEASURED` |

**So the search zero is real**, and it has a cost consequence: a search-sourced account arrives with
no bio, while a hashtag-sourced one arrives with a bio about 86% of the time. Search accounts
therefore need a paid profile fetch to reach what hashtag accounts hand over free.

### 3f. Cost per 1,000 delivered — discovery only

⚠️ **THIS IS DISCOVERY COST ONLY.** It excludes the profile fetch and the judging model, which are
where the money actually is. It must never be quoted as the cost of a lead.

⚠️ **The 77.8% approval rate below is from a DIFFERENT population** — it is the operator's historical
approval on search-sourced pages, not measured this round. The populations do not match, so both
raw figures are given and the multiplication is marked `DERIVED`.

```
Vendor price per request: $0.000600            MEASURED (vendor quota receipt, prior round)

BEFORE  authors per billed call = 116 / 7 = 16.57          MEASURED (7 first pages)
AFTER   authors per billed call = 402 / 19 = 21.16         MEASURED (19 pages, 3 keywords)

BEFORE  16.57 x 0.815 net-new x 0.778 approval = 10.509 delivered/call     DERIVED
        1000 / 10.509 = 95.2 calls x $0.000600 = $0.0571 per 1,000         DERIVED
AFTER   21.16 x 0.815 net-new x 0.778 approval = 13.417 delivered/call     DERIVED
        1000 / 13.417 = 74.5 calls x $0.000600 = $0.0447 per 1,000         DERIVED

CHANGE  $0.0571 -> $0.0447  =  21.7% cheaper per 1,000 delivered           DERIVED
```

### 3g. The number that actually matters is supply, not price

Discovery already cost about four cents per thousand. **What changed is the ceiling.**

```
configured search terms: 13   (6 meme + 7 editing)                    MEASURED (from config)

BEFORE  13 x  16.57 =   215 authors  <- and that was the LIFETIME CEILING   DERIVED
AFTER   13 x 134.00 = 1,742 authors                                          DERIVED
        of which net-new = 1,742 x 0.815 = 1,420                             DERIVED
        cost of one full sweep = 13 x 6.3 calls x $0.000600 = $0.0494        DERIVED

for comparison, the surface this is meant to relieve:
   Instagram reels -- 476 handles from 9 phrases across its WHOLE LIFETIME, cannot paginate
   search after paging -- 1,742 authors per sweep, repeatable
```

**Search stops being a dead end for about five cents a sweep.**

---

## 4. WHAT WAS REFUSED OR NOT DONE

1. ⚠️ **THE CODE WAS NOT COMMITTED, AND THAT IS DELIBERATE.** The commit guard correctly refused:
   one of the two files is claimed by another round, filed **32 hours** earlier and silent for
   **31 hours 39 minutes** of that. That round has **committed nothing to this file** — the three
   most recent commits touching it belong to two other rounds — and its work sits in four untracked
   files that a normal diff cannot see, proving it did real, paid work **elsewhere**. A peer session
   independently corroborated the staleness **and explicitly declined to authorise the release**,
   correctly: *"the file is that round's or the operator's to release, not mine."* **Corroboration
   is not permission.** `--no-verify` was never used.
2. **A partial commit was refused too.** The client change alone is backwards-compatible, but its
   test exercises the caller, so committing half would land a red test. Nothing is lost by waiting;
   every measurement is already on disk.
3. **The ledger under-count was not investigated.** A peer proposed that the shared spend ledger may
   be losing writes under concurrency. My own apparent discrepancy turned out to have a simpler
   cause (§5) and is **no evidence either way**. The discriminator is cheap — append a known number
   of marked rows from two processes at once and count survivors — and **I did not run it**: this is
   a pagination round, not a ledger audit.
4. **415 candidate sites for a code smell were found and NOT triaged.** Counting them was free;
   fixing them is someone else's round.
5. **The obvious fix for the spend-visibility gap was refused on measurement.** Making the LamaTok
   client book its own spend the way the Instagram client does **would double-count**, because the
   funnel already writes spend deltas against a high-water mark. That is a defect two earlier rounds
   already fixed once.
6. **NOT MEASURED:** whether the hashtag endpoint has the same untapped pagination. Its config note
   already says the cursor "is not sent" and page-2 density is unmeasured. Still unmeasured.
7. **NOT MEASURED:** whether a deeper page cap finds more. Settled from data already bought instead —
   at 30 per call, four keywords used 7, 6, 6 and 6 pages against a cap of 10, so the cap never
   binds. **I nearly spent ten calls re-buying an answer three files already held.**

---

## 5. WHAT I GOT WRONG

**Ten corrections. Every one was in an interpretive sentence; not one measured number changed.**

1. ⚠️ **My own error handling turned a programming error into "no videos found."** The first version
   of the paged walk caught a type error from a mis-shaped client and returned an empty list with a
   message — a broken signature wearing a dead endpoint's clothes, which is the exact failure this
   round exists to correct. It now re-raises.
2. ⚠️ **I published "100% net-new against master" computed against an EMPTY denominator.** My reader
   looked for a column named `handle`; the column has a different name. It matched nothing, returned
   an empty set, and produced a confident, specific, wrong number **with no error raised.** The
   loader now refuses to return an empty master rather than report a rate against nothing.
3. **My first probe saved counts and not identifiers**, so the net-new question could not be answered
   offline and a re-run had to be bought.
4. **A test fixture I wrote reused one payload across three pages**, so the repeat-detector correctly
   stopped the walk and the test failed. **The fixture was wrong and the shipped code was right.**
5. ⚠️ **I reported a spend discrepancy that did not exist.** I wrote that my counter said 74 calls
   while the ledger moved 60 rows, and blamed concurrent writers. **Both halves were wrong.** A
   ledger row is not a call, and **not one of my calls is in that ledger at all** — it is written by
   the funnel, not by the client, and my probes called the client directly. The "60 rows" was a
   snapshot of an unrelated process.
6. ⚠️ **I metered the wrong counter, four lines from the right one.** The client documents an
   internal counter as *"ACTUAL HTTP requests made (incl. retries) — the true billed count. Callers
   meter THIS, not one-per-logical-call."* **I counted logical calls — precisely what that comment
   says not to do — while quoting a cost to four decimal places.** Spot-checked afterwards on a
   fresh walk: the two counters agreed, 6 and 6, with zero unexpected statuses.
7. ⚠️ **I published a false label twice, and the rule it broke was one I had written and committed
   hours earlier.** I reported that a function name *"appears only in comments"* in a file where it
   appears **zero times**. The cause was not a misreading — it was a hardcoded fallback string in my
   own diagnostic, `calls or "NONE (comment mentions only)"`. **The instrument measured an empty
   list; the string asserted an explanation the instrument never tested.** My own committed rule:
   *"Report what the instrument saw and let the comparison be mechanical. The moment you write down
   what it means, you have added something that can be wrong."*
8. ⚠️ **The auditor I then wrote to catch that class returned a clean zero, and the zero was
   worthless.** Run against two known defects, it caught someone else's and **missed my own**, for
   two reasons: it examined only top-level strings, and it treated `x or "CLAIM"` as *guarded*. **It
   is the opposite of a guard — the claim fires exactly when there is no evidence.** Fixed; the
   control now catches 2 of 2.
9. **My corrected rule was then unusable as specified.** A peer showed it would flag a great deal of
   correct code. Measured: **11,023 sites flagged by my rule, 415 by the refined one — 96.2% were
   false positives.** The discriminator is theirs and it is one word: **the defect is not the
   fallback, it is the parenthetical.** A short token renders emptiness faithfully; a clause with an
   explanation in it is a claim.
10. ⚠️ **A warning about my own memory index sat in my context from the first turn of the session and
    I never acted on it.** Another session fixed it. The same warning appeared in that session's
    context and was ignored there too — **two independent sessions, same warning, same file, same
    outcome.**

### THE PATTERN, WHICH IS WORTH MORE THAN THE ROUND

Four safeguard mechanisms failed in this round: an explanatory comment at the point of use, a
hardcoded label, a control that could not fail, and an automated start-of-session warning. **All
four share one property: none of them can fire.**

> **A safeguard that informs is not a safeguard. Only one that intercepts is.** Comments,
> docstrings, labels, decorative controls and start-of-session warnings all *inform*. Assertions,
> hooks and computed verdicts *intercept*. **Every failure in this round was informed against in
> advance, in writing, and happened anyway.**

The three things that actually worked were an assertion that halted a write, a control run against a
known defect, and a second reader.

---

## 6. MONEY AND SAFETY

### Vendor spend — from the run's own call counter, never a ledger delta

```
billed requests made by this round: 80        (counted in one place, in-process)
price per request:                  $0.000600
TOTAL:                              $0.0480
cap for this round:                 $0.50      -> 9.6% of it used
page ceiling:                       100        -> 80 used
```

⚠️ **The shared ledger cannot confirm this and must not be used to.** It carries a round identifier
on zero rows, several sessions write to it concurrently, and **none of this round's 80 requests
appear in it at all** — it is written by funnel runs, not by the client, and these were probes.

⚠️ **SAFETY FINDING, NOT INTRODUCED HERE, SURFACED FOR A DECISION.** The lifetime spend cap is
computed from that ledger. The Instagram client books its own spend; **the LamaTok client does not**
— and the function name does not appear anywhere in its source, so a reader gets no hint. Counted:
**78 scratch scripts construct that client; 47 of them book nothing.** **Direction certain,
magnitude unmeasured** — I have not summed the unbooked spend and will not estimate it.

### Seen stores — RE-VERIFIED AT PUBLICATION, not only at check time

Checked again immediately before writing this file:

| file | delta since this round's baseline | |
|---|---:|---|
| **TikTok seen store** (the one this round would write) | **0 bytes — UNCHANGED** | last modified **2 days before this round began** |
| TikTok clip seen store | 0 bytes — UNCHANGED | |
| Spotify seen store | 0 bytes — UNCHANGED | |
| `config.json` | 0 bytes — UNCHANGED | |
| Instagram meme seen store | **+16,843 bytes — CHANGED** | modified **after** this round ended; another session |
| master lead table | **+517 bytes — CHANGED** | modified by another session |
| shared spend ledger | +497,027 bytes — CHANGED | several sessions billing |

**This round wrote to none of them.** The two that moved were changed by other sessions, and the
timestamps place both outside this round's activity. **Reported as changed rather than as "delta 0,"
because the check-time answer was 0 and would have been stale by publication.**

### Disk, processes, campaigns

* **Disk: 388.4 GB free at round start, 359.6 GB free at publication.** Not consumed by this round —
  its total output is a report and eight small scripts.
* **Nothing was killed.** All four local servers were verified listening on their original process
  ids at round start and again at publication. No process was stopped, restarted, or signalled.
* **Campaigns configuration SHA: `7a029ee5447cddd8`.** ⚠️ This differs from the value recorded in an
  earlier round. `config.json` is **byte-identical** to this round's own baseline, so the change
  predates this round and was not made here. **Flagged, not explained.**

---

## 7. WHAT TO DO NEXT — RANKED

**1. Release the held file, or take the caller change as a written spec.** *(one decision, no cost)*
Everything else waits on this. The spec is: send `page_id` taken from `next_page_id`; drop `offset`
whenever paging; stop on an empty page, a repeated page, or a missing cursor; count **every** page
through the billing callback, not one per keyword.

**2. Ship the two changes and run one sweep.** *(about 5 cents)*
```
13 keywords x 6.3 calls x $0.000600 = $0.0494
expected: about 1,742 authors, of which about 1,420 net-new
against today's ceiling of about 215
```

**3. Put search-sourced pages in front of you before trusting the supply at 8x volume.** *(free)*
The 77.8% approval used in the cost arithmetic is **the judging model's opinion, not yours** — the
configuration file states plainly that zero search-sourced pages appear in the pages you have
graded. **This round multiplies supply from a surface you have never personally scored.** One
grading sheet carrying search-sourced rows settles it.

**4. Decide about the spend-visibility gap.** *(a scored round, not a one-liner)*
47 probe scripts can spend money the cap will never subtract. **Do not apply the obvious fix** —
making the client book its own spend would double-count against the funnel's existing high-water
mark. Both paths need scoring together.

**5. Check whether the hashtag surface has the same untapped pagination.** *(a few cents)*
It does not send a cursor either. If it pages like search does, it is the same finding again on a
larger surface.

**6. Budget for the bio gap.** *(arithmetic only)*
Search accounts arrive with no bio; hashtag accounts arrive with one about 86% of the time. Multiply
search supply by 8 and the share of accounts needing a paid profile fetch rises with it.

---

## 8. PATHS

Paste these into File Explorer; `%USERPROFILE%` expands automatically.

```
the project
   %USERPROFILE%\OneDrive\Desktop\clipper finder

this round's report and evidence
   %USERPROFILE%\OneDrive\Desktop\clipper finder\reports\BL-1469.md
   %USERPROFILE%\OneDrive\Desktop\clipper finder\scratch\   (files beginning bl1469_)

the two files holding the uncommitted change
   %USERPROFILE%\OneDrive\Desktop\clipper finder\clippershq\api_client.py
   %USERPROFILE%\OneDrive\Desktop\clipper finder\clippershq\tiktok_finder.py

the timestamped backup taken before any vendor call
   %USERPROFILE%\OneDrive\Desktop\clipper finder\scratch\   (folder beginning bl1469_backup_)
```

**To open the dashboard or a grading sheet, use the launcher — not a bookmarked address.** Port
numbers are not stable between runs and a grading session has already been lost to a stale bookmark.

```
   %USERPROFILE%\OneDrive\Desktop\clipper finder\dashboard\dashboard_launcher.py
```

---

### VERIFICATION OF THIS FILE

Every detector below was proven on a planted positive control **before** its zero was believed, and
the gate ran on the bytes **before** they were written to disk. On failure the file is removed
rather than published.

* **email detector** — fired on a planted positive control: **YES**
* **api key detector** — fired on a planted positive control: **YES**
* **wallet detector** — fired on a planted positive control: **YES**
* **windows user path detector** — fired on a planted positive control: **YES**
* **port number detector** — fired on a planted positive control: **YES**
* **control-byte detector** — fired on a planted NUL and backspace: **YES**
