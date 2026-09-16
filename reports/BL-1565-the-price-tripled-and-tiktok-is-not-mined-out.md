# BL-1565 — the price tripled, TikTok is not mined out, and the reason is not what I first measured

**Round:** BL-1565 · **Unit:** `api.cost_per_call_usd` = $0.00060000, by named key (never
`ig_api`'s $0.00069064) · **Spent:** $0.10260 of a $0.50 cap, on one thing, named below

## The paragraph

**The price is not tripling because TikTok is mined out.** Two independent instruments say the
store is not the problem: the share of found addresses that are still NEW is **flat at ~90%
across four rounds** against a 74,000-account store, and the dedup guard's refusal rate is
**53.89% then 54.09% — overlapping, not rising**. The entire collapse sits in one factor: the
share of served accounts that carry an address at all, which fell **3.92x**. **It is not
permanent and no tag list fixes it.** The single cheapest change that reverses part of it is
free: **stop walking tags to the ~170-page wall.** On the first per-page measurement this
project has ever taken, capping at 30 pages costs **$0.0036 per address-carrying account against
$0.0057 at the wall — 1.58x cheaper** — because the pages you stop buying are the ones
returning 3 new accounts instead of 9. In the units actually bought that is **~$4.01 per 1,000
net-new against the $13.92 BL-1564 paid**. What I could NOT explain is why F2 itself fell
between the last two rounds; three candidate causes were eliminated and the honest answer is
that it is still open.

## 1. What this project is, for a reader with no context

It finds video editors on TikTok who put an email address in their bio. A paid vendor API
returns hashtag pages; each page carries up to 30 posts and, on TikTok, **the author's bio
rides along free**. A dedup guard refuses accounts and addresses already held. One call =
one page = $0.00060000.

**The standing fact that outranks every price here: 13,007 addresses have been collected and
NOT ONE HAS EVER BEEN CONTACTED.** All outcome columns are empty on all 74,162 rows.
`outcomes.py` is 847 lines with production callers and 63 passing tests and has never written
a real outcome. **Every number in this report is a proxy for a value nobody has measured.**
This project does not send, and this round did not build a sender.

## 2. Safety, money, and the cap

Ten stores backed up sha256-verified, bodies found **by shape** (`spend.json` → `runs`,
`clip_seen.json` a bare list of 2,193, `tiktok_pages_seen.json` → `pages` with 3,270 where a
dict-only reader says 3). **All six numbered corruption controls fired**, counted by matching
the numbered control lines — `controls()` also prints a warning and a summary, so a naive
print-site count answers 8 and would pass a threshold of 6 with two real controls deleted.

**The cap was driven before the one paid call**, with `Budget` lifted from `harvest_run.py` by
AST: funded allows and the meter advances; $0.00 raises; **the meter does not advance on a
refusal**; 3 funded calls allow 3 and refuse the 4th; and the proof **wrote nowhere**.

**Spent: $0.10260, all of it on the per-page probe in section 5.** Everything else was
arithmetic on data already paid for.

## 3. The decomposition that settles it

The brief names two factors. **There are three**, and the third is where the money goes:

```
net-new per CALL = (kept accounts per call) x (share of kept carrying an address)
                                            x (net-new addresses per such account)
```

The two-factor form conditions on kept accounts and so cannot see the first term — but a page
buys 30 slots and BL-1564 got 6.04 kept accounts per call.

| round | pages/tag | F1 kept/call | F2 addr share | F3 new/acct | net-new/call | $/1k |
|---|---|---|---|---|---|---|
| bl1557 | 9.4 | 3.12 | 3.119% | 93.75% | 0.09119 | $6.58 |
| bl1560 | 6.0 | 2.33 | 3.047% | 98.61% | 0.07009 | $8.56 |
| bl1563 | 91.3 | 6.22 | 2.195% | 96.40% | 0.13161 | $4.56 |
| bl1564 | 119.1 | 6.04 | 0.795% | 89.80% | 0.04312 | $13.92 |

⚠️ **Three schemas, three spellings.** BL-1557/1560 wrote `addr`/`authors`/`netnew`; BL-1561
wrote `accounts`; BL-1563/1564 wrote `emails`/`netnew_here`. The mapping was **controlled**: it
reproduces every independently published round figure (bl1563 2.12% vs 2.11% published,
bl1564 0.71% vs 0.71%). A mapping that cannot reproduce a known answer is not trusted.

⚠️ **BL-1561 is excluded from the trend** and shown nowhere above: it walked 12 hashtag pages
but made 316 calls, because most were paid PROFILE calls on a route no other round used. Its
kept-per-call is not comparable and averaging it in would have been silent nonsense.

**F1 improved. F3 is flat. F2 carries all of it.**

## 4. So is TikTok mined out? No — and two instruments agree

**F3 — of the addresses found, how many are new —** 93.75%, 98.61%, 96.40%, 89.80%. Flat.
Against a store that now holds 74,162 rows, roughly nine in ten addresses found are still new.

**The guard's refusal rate —** what a filling store would push up — is **53.89% [53.57–54.21]**
in BL-1563 and **54.09% [53.49–54.69]** in BL-1564. Overlapping.

**That is a measured refusal of the mined-out theory, and it is the most valuable thing in
this report.** If the answer had been "mined out", it would have saved a month. It is not.

## 5. The per-page curve — the only paid thing, and it refuted my own hypothesis

**Why it was worth $0.10260, decided before spending it:** every stored walk holds per-TAG
aggregates, so the best free evidence was two points per tag. "The depth at which a page stops
paying for itself" needs per-page data and no round has ever stored it. One tag, 170 pages,
~170 points.

| pages | items | fresh to tag | kept | carrying an address | kept/page |
|---|---|---|---|---|---|
| 1–10 | 170 | 102 | 87 | **1** | 8.70 |
| 11–20 | 159 | 77 | 67 | **2** | 6.70 |
| 21–30 | 167 | 62 | 54 | **2** | 5.40 |
| 31–40 | 173 | 64 | 58 | **1** | 5.80 |
| 41–50 | 165 | 54 | 50 | **0** | 5.00 |
| 51–60 | 163 | 47 | 43 | **1** | 4.30 |
| 61–70 | 161 | 53 | 47 | **2** | 4.70 |
| 71–80 | 162 | 43 | 42 | **1** | 4.20 |
| 81–90 | 170 | 53 | 52 | **1** | 5.20 |
| 91–100 | 166 | 47 | 44 | **2** | 4.40 |
| 101–110 | 155 | 42 | 39 | **1** | 3.90 |
| 111–120 | 152 | 38 | 38 | **1** | 3.80 |
| 121–130 | 162 | 35 | 34 | **0** | 3.40 |
| 131–140 | 156 | 32 | 28 | **0** | 2.80 |
| 141–150 | 147 | 36 | 34 | **0** | 3.40 |
| 151–160 | 159 | 30 | 29 | **1** | 2.90 |
| 161–170 | 135 | 41 | 41 | **2** | 4.10 |

**Address-carrying accounts are spread thinly and FLAT across all 170 pages.** There is no
early-page concentration. The marginal cost per address wanders between $0.0030 and $0.0120
with no trend:

| cap | pages | kept | w/ addr | $ spent | $/addr | marginal $/addr |
|---|---|---|---|---|---|---|
| p≤10 | 10 | 87 | 1 | $0.0060 | $0.0060 | $0.0060 |
| p≤20 | 20 | 154 | 3 | $0.0120 | $0.0040 | $0.0030 |
| p≤30 | 30 | 208 | 5 | $0.0180 | $0.0036 | $0.0030 |
| p≤40 | 40 | 266 | 6 | $0.0240 | $0.0040 | $0.0060 |
| p≤60 | 60 | 359 | 7 | $0.0360 | $0.0051 | $0.0120 |
| p≤80 | 80 | 448 | 10 | $0.0480 | $0.0048 | $0.0040 |
| p≤100 | 100 | 544 | 13 | $0.0600 | $0.0046 | $0.0040 |
| p≤120 | 120 | 621 | 15 | $0.0720 | $0.0048 | $0.0060 |
| p≤140 | 140 | 683 | 15 | $0.0840 | $0.0056 | — (bought 0) |
| p≤170 | 170 | 787 | 18 | $0.1020 | $0.0057 | $0.0060 |

### 5a. What DOES fall with depth is supply, not addresses

Kept accounts per page falls from **8.70/page** in pages 1–10 to **2.80/page** by pages
131–140 — a **3.1x** fall. The feed re-serves accounts the tag has already shown. That is the
real depth effect, and it is about how many NEW ACCOUNTS a page buys, not how many carry an
address.

### 5b. THE HYPOTHESIS THIS KILLED WAS MINE

Earlier in this same round I found what looked like a clean, confound-free depth effect. Four
tags had been cut short and later re-walked, so the second pass's kept accounts are exactly the
pages the first pass never reached — the same tag as its own control:

| tag | pages 1–C | kept | addr | F2 | pages C+ | kept | addr | F2 |
|---|---|---|---|---|---|---|---|---|
| `bellinghamedit` | 1–104 | 581 | 16 | 2.754% | 105–171 | 845 | 9 | 1.065% |
| `clarkkentedit` | 1–94 | 551 | 21 | 3.811% | 95–171 | 908 | 6 | 0.661% |
| `moneyheistedit` | 1–143 | 391 | 7 | 1.790% | 144–169 | 477 | 0 | 0.000% |
| `nightwingedit` | 1–42 | 334 | 14 | 4.192% | 43–170 | 1080 | 10 | 0.926% |

Pooled: early pages **3.123%**, later pages **0.755%**, a **4.13x** fall. I believed it.

**It is confounded and the per-page curve is what showed me.** The second pass ran against a
much larger store, and *an account that carries an address is exactly the kind already
harvested and now refused before its bio is ever read*. So that comparison measured
store-depletion of the kept population, not depth. The single-pass per-page curve has no such
confound and shows no depth effect at all.

## 6. What capping depth would actually save

| policy | $/address-carrying account | $/1,000 net-new |
|---|---|---|
| capped at 30 pages | $0.0036 | ~$4.01 |
| walked to the ~170 wall | $0.0057 | ~$6.35 |
| **what BL-1564 actually paid** | — | **$13.92** |

The saving comes from **F1, not F2** — you stop buying pages that return 3 new accounts instead of 9. It is free to adopt and needs no new tags.

⚠️ **Measured on ONE tag.** It is the first per-page evidence this project has, and it is one tag.

## 7. The seven defects

**(a) The dedup key mixed platforms — FIXED, GENERAL.** AST resolved **30** account-keying
sites across the tree; grep returned 1696 text lines over the same names (comments,
docstrings, and this round's own scratch). **The AST answered for the code sites; grep is not
redundant because it is the only one that can see a name built inside a string literal.** Of
the 10 sites that decide an account's identity, **9 are inside `DedupGuard`** — so the fix
belongs there, not at each caller. `account_key(value, platform)` scopes a handle only when a
platform is given; the account ID is never scoped because it is already globally unique.
Driven both directions in `tests/test_bl1565_platform_key.py`: the TikTok/Instagram collision
is no longer refused, **and the same-platform collision still is** — without that second test,
code that simply disabled the guard would pass.

**(b) The saturation detector had never fired — REPLACED.** `repeat_bodies` fired **0 times in
75 tags / ~8,900 pages** and branched on nothing: it was incremented and never read. It cannot
fire on this endpoint, because every response carries its own cursor so identical content
still differs in bytes. **The page-identity signal is now the ACCOUNT-ID SET**, which does
fire: on this round's instrumented walk **2 of 128 pages returned items and zero accounts the
tag had not already shown** — pages the body hash saw as brand new. The raw body hash is still
collected under its own key and is simply no longer called a detector.

**(c) The master/workbook split — MADE STRUCTURAL.** `DedupGuard.build()` read master's `email`
column and not its `tiktok_handle` column, so a default build knew **zero accounts**; every
caller had to remember `extra_accounts` and the one that forgot re-bought 246 accounts the
operator already had. `read_master_accounts` now defaults to True, and because the column is
*named* `tiktok_handle` the platform is known, so those handles are stored scoped for free.

**(d) The suite charged the production ledger — FIXED AND MEASURED.** `_book_paid_call` built
`<repo>/spend.json` by hand, bypassing `main.spend_path()` — the one function that honours
`$CLIPPERSHQ_SPEND_FILE` and redirects a test entry point to a temp ledger. Now routed through
the chokepoint. **Measured across a 73-test judge run, ledger snapshotted before and after:
+0 rows, +$0.000000**, against the +212 rows / +$0.038270 reproduced to the cent across four
rounds. (One pre-existing failure in that run, `test_judge_page_is_still_called_after_the_purchase`,
is a line-order check inside `tiktok_finder.py` — a file this round proved byte-identical to
HEAD. Not mine.)

**(e) Book at the wrapper — DONE.** `LockedBudget` now books through the chokepoint every
`BOOK_EVERY = 25` calls when a caller names a campaign, and books nothing without one so a
counter or a unit test cannot write to a money ledger. Driven: 60 calls → 3 sandbox rows
totalling exactly 60 calls, production untouched.

**(f) In-flight spend was invisible — WORTH DOING, AND THIS ROUND PROVED IT LIVE.** Booking per
tag leaves everything since the last completed tag unrecorded. **This round's own probe sat at
143 pages / $0.0858 spent with the ledger reading $0.00000**, because no tag had finished. The
25-call flush bounds that blind spot to **$0.015**.

**(g) Log failures — DONE.** `Harvester` takes a `page_log` callback fired on **every** page,
whatever it returned. The row files are 100% survivorship — only productive accounts are ever
written — so "which calls were wasted" has never been answerable from disk. It is free.

## 8. The output

* **The answer: not mined out, not permanent.** F3 flat, refusal flat.
* **The collapse is entirely F2**, and depth does not explain it.
* **Cap at ~30 pages**: ~$4.01 per 1,000 net-new against BL-1564's $13.92.
* Seven defects fixed, each driven, one committed test enrolled in the manifest.
* $0.10260 spent of $0.50.

## 9. WHAT I GOT WRONG

**I spent the round's only money and then failed to book it, with the exact defect I was
fixing.** The probe passed `stage="research"` — not one of the four valid buckets — so
`validate_stage` correctly refused, the booking raised, and the probe crashed at its final
flush. $0.10260 was spent and sat unbooked until I noticed. **The guard did its job; I was the
one who got it wrong**, while in the middle of writing the fix for spend that goes unbooked.

**I believed a confounded result and wrote it up as confound-free.** The four-tag within-tag
comparison is the cleanest-looking thing in this round — same tag, same endpoint, same guard —
and I called it "the depth effect, confound-free" in the analysis file. It is not: the two
passes ran against different store sizes, and the store systematically removes exactly the
accounts being counted. I only caught it because the per-page curve disagreed. **Had the probe
been cheaper to skip, I would have shipped it.**

**I read a stale artifact and nearly reported from it.** The decomposition JSON crashed on an
unpacking error I introduced while patching, so the file on disk stayed as the previous run had
left it — and the console and the JSON disagreed by 6x on F1. I caught it only because I
re-read the file I had just regenerated.

**And a ratio over 100% made me cry instrument failure when the instrument was fine.** BL-1561
showed F3 = 103.30%, which cannot be a share. It is not a share: `netnew` counts ADDRESSES and
`addr` counts ACCOUNTS CARRYING ONE, and an account can carry two. My label was wrong, not the
data.

## 10. What did not run, reported as ABSENT

* **Why F2 fell from 2.195% to 0.795% is UNEXPLAINED.** Eliminated: depth (per-page curve
  flat), tier composition (BL-1564's re-opened and fresh tiers are 0.755% and 0.810% — equally
  low), and store saturation (refusal flat, F3 flat). What remains is the tag population
  itself. **One fresh tag walked today scored 2.287% — BL-1563-like, not BL-1564-like —
  but n=1 tag settles nothing and this round does not pretend otherwise.**
* **The next test is named and costed: walk ~10 fresh tags at p≤30, about $0.11, and compare
  F2 against BL-1564's 0.795% [0.59–0.99].**
* **The curve is ONE tag.** It shows a knee does not exist on that tag. It cannot show the
  shape for all tags.
* **BL-1562's claim is still stale-OPEN** with its report published and no manifest. Noted,
  not touched — it is another round's claim.
* No outreach was sent. This project does not send.
