# BL-1561 — the free bio route, and the thing that actually sets the price

**When the free route serves, an Instagram address costs about $1.11 per 1,000. When it is
shut, it costs between $2.32 and $9.86 per 1,000 — and which of those two you pay is decided
by WHICH TAG YOU WALK, not by the free route.** This walk ran with the free route **completely
dead — 0 of 304 accounts served a page** — and still delivered **94 net-new addresses for
$0.21824, which is $2.32 per 1,000**, because it walked the highest-recorded-yield tag first.
BL-1560's drained half paid **$9.86** for the same conditions on mediocre tags. **So the free
route is worth about 2x, and tag choice is worth about 4x, and the free route is the one you
cannot control.** I could not summon it once all evening: four measurements now give
**12.6 h of silence → 45 successes, 2.82 h → 784, 1.00 h → 0, 1.11 h → 0.** That is
non-monotonic in silence, which kills "wait a long time and collect a burst" as a scheduling
rule. **So do not schedule around the free route. Walk the top of the yield table, price it at
$2.32 per 1,000, and treat any free window you happen to catch as a 2x discount rather than a
plan.**

**And the honest counter changes one number you were given.** `bio_free` counted *taking* the
free branch, not succeeding on it. Re-derived from an arithmetic identity that never touches
it, BL-1560's free half was **898 of 1,786 accounts**, not 780 — and session 1 alone was
**784 of 797 = 98.4% [97.2–99.0]**. The figure was real and slightly understated. There was
never a counter artefact to explain the contradiction away.

---

## 1. What this project is, for a reader with no context

ClippersHQ finds video editors and meme-page operators on TikTok and Instagram and collects the
email addresses in their bios, so a human can offer them paid clipping work. It buys data from
**HikerAPI** for Instagram (`ig_api.cost_per_call_usd` = **$0.00069064** per call) and
**LamaTok** for TikTok (`api.cost_per_call_usd` = $0.00060000). Those are 15.1% apart and
reading the wrong one once let a $3.00 cap spend $3.45, so every figure here is the Instagram
one, read by named key.

An Instagram bio can be read two ways: **free**, by fetching the public profile page, or
**paid**, by buying the profile from the vendor. The free route works until it doesn't, and two
prior rounds disagreed about it by 17x. **That disagreement is what this round was asked to
settle, because it is the difference between a dollar and ten dollars per thousand addresses.**

## 2. Safety, money, and the cap

| | |
|---|---|
| nine stores backed up | sha256-verified, bodies found **by shape** |
| corruption controls | **all six fire**, and the count is taken **from the source** |
| `spend.json` | list at `runs`, 38,180 rows at start |
| `clip_seen.json` | **bare list**, 2,193 |
| `tiktok_pages_seen.json` | dict at `pages`, **3,270** (a dict-only reader reports 3) |
| `master_leads.csv` | 73,072 rows × 72 columns at start |

The backup wrapper counts the control print-sites in the module source rather than trusting its
docstring, which says "THE FIVE CORRUPTION CONTROLS" and has six.

**Money, by leg, all booked:**

| leg | calls | spend |
|---|---|---|
| free-route probes (2×2, origin ×2, detector demo) | 4 | $0.00276 |
| the paid walk | 316 | $0.21824 |
| deliverability re-fetch | 91 | $0.06285 |
| **round total** | **411** | **$0.28385** of a $1.00 maximum |

**And 210 requests cost nothing at all**, because the free route is free by definition — that
is what made a four-experiment investigation affordable.

Each booking went through `record_aux_spend` with `ig_cost_per_call` passed **by name** (its
`cost_per_call` argument defaults to LamaTok's rate, which is how 6,642 rows were once booked
13.1% cheap), and each was verified to move the ledger by exactly one row of exactly the
expected amount.

### The leak scan fired, and here is why this was published anyway

The scan is built from **both** corpora — the lead store (every address and handle it holds,
including this round's own 94) and this round's walk rows — and every detector is proved on a
planted control before it is trusted. It reported:

    HIT  {'a real creator handle': 2}      VERDICT: NOT publishable as-is

**Both hits were read by hand. Both are the ordinary English word *records***, which is also
somebody's handle in a corpus of 72,000. The file contains **no `@` sigil at all**, **zero
addresses from either corpus** (checked directly), and **zero C0 control bytes**, asserted
before writing rather than after.

This is the third round running to hit the same class of false positive — 8 of 8, then 6 of 6,
now 2 of 2. **The detector is deliberately NOT loosened here**, because a relaxed version would
never have been tested against a real leak in the same round that publishes through it. ⚠️ And
naming the token in this paragraph raises the count from 2 to **3 — every one of them the same
ordinary word**, counted on the exact file being published.

## 3. Part 1 — the honest counter, and the number it corrects

⚠️ **THE DEFECT, QUOTED.** `scratch/bl1557/bl1557_walk.py:259-262`:

    state, bio, _s = ig_bio.bio_for(h)
    src = "free_http"                     # <-- NAMED BEFORE THE OUTCOME IS KNOWN
    if state == "unknown":
        ... chromium ... then paid ...

`src` is only overwritten on a *successful* fallback, so an account whose free fetch walled,
whose Chromium fallback failed and whose paid call came back empty still increments
`bio_free`. **AST found the reachability (exactly one literal assignment to `src` in that
file); grep found the counter buckets 33 lines later.** Both were used and each answered a
different half.

⚠️ **AND A SECOND PROBLEM IN THE SAME PLACE.** `bio_for` returns **three** states — `present`,
`empty`, `unknown` — and the walker escalates to paid only on `unknown`. A profile page that
loaded and simply has no bio is `empty`: it needed no paid call and produced no bio. So "did
not need a paid call" is `present + empty`, which is a different question from "got a bio
free", and no artefact on disk can split BL-1560's figure into the two.

**THE REPLACEMENT** records every stage *after* it runs and reconciles its own identities —
`free_attempted = free_page_loaded + free_walled`, `free_page_loaded = free_bio_present +
free_page_no_bio`, `paid_attempted = paid_returned_bio + paid_charged_and_empty`. Fed a
deliberately broken counter it names both broken identities. `paid_attempted` is the **billed**
number, not `paid_returned_bio`, because the vendor charges on the attempt.

**RE-DERIVING BL-1560 WITHOUT THE BROKEN COUNTER.** Calls are billed for exactly two things,
hashtag pages and paid profiles, so `paid = calls − pages` and `never-needed-paid = accounts −
paid`. Nothing in that identity touches `bio_free`:

    hashtag pages, summed per tag                126
    calls billed (1,013 checkpointed + 1 orphaned) 1,014
    => PAID PROFILE CALLS                         888
    accounts kept                               1,786
    => NEVER NEEDED A PAID PROFILE                898

and as a cross-check the old counter's 974 minus its 77 charged-and-empty is **897**, agreeing
to within the single orphaned call. **The "780 free" was not an artefact — it was understated.**

| | accounts | never needed paid | |
|---|---|---|---|
| BL-1560 session 1 | 797 | **784** | **98.37% [97.20–99.05]** |
| BL-1560 session 2 | 989 | 115 | 11.63% [9.79–13.76] |

## 4. Part 2 — the reconciliation, and three candidates killed for $0.00

**(a) THE COUNTER — refuted above.** The contradiction is genuine.

**(c) THE HTML PAGE vs THE JSON ENDPOINT — refuted by reading the code, before spending
anything.** `ig_bio.fetch_profile` builds `https://www.instagram.com/<handle>/` with urllib
under `PROFILE_UA`; BL-1559's probe used httpx against the **identical** URL under the same
headers; both judge success with the same `has_content()`. **Neither ever called
`api/v1/users/web_profile_info`.** Separate budgets for the two surfaces may well exist, but
they cannot be what separates these two numbers.

**(d) CHROMIUM vs PLAIN HTTP — not involved.** BL-1560's entire walk recorded **one** Chromium
attempt across 1,786 accounts, and BL-1559's probe was plain HTTP. Both numbers are plain HTTP.

That left two differences, and both were tested as an interleaved 2×2 (A,B,C,D,A,B,C,D…) so a
bucket draining mid-run would hit every cell equally: **client** (urllib vs httpx) × **handle
history** (BL-1559's hammered slice vs a disjoint slice it never requested).

**It returned 0 of 80.** Every cell zero. The script had declared *before* the run that an
all-zero result measures the wall and not the factors, so it reported **AMBIGUOUS** rather than
a refutation.

⚠️ **AND RE-READING THE DESIGN AFTERWARDS EXPOSED A FLAW THE ZERO HID:** both "history" arms
drew from `master_leads.csv`, and **every Instagram handle in master has already been fetched
by this project** — that is how its stored bio got there. The contrast was "hammered" against
"hammered less", never "hammered" against "never requested". So a second test bought one
hashtag page and interleaved **master handles against handles seen for the first time**, 25
each. **0 of 50.** Re-run later on a cold exit after a full hour of silence: **0 of 50 again.**

**That last one is informative even though it is a zero: the wall blocks handles this project
has never requested, so it is not purely per-handle.**

### ⚠️ And I killed my own best hypothesis before spending a cent on it

I had written that BL-1560's 784 succeeded "one hour" after BL-1559's cliff "at a slow pace",
and built a rate-limit model on it. **Re-deriving the timeline from artefacts instead of from
my own narrative killed both halves.** Session 1 ran **14:51:45 → 15:08:24 — 797 accounts in
16.7 minutes, about 1.3 s per account** — the *same* pace at which BL-1559 walled at 45. And
the gap was **2.82 h**, not one hour. **Pacing cannot separate them.** The model was dead
before it cost anything, and the correction is recorded next to the original rather than
overwriting it.

### The four points, which are the finding

| round | untouched silence | successes | handles |
|---|---|---|---|
| BL-1559 | **12.61 h** | 45, then 27 straight shells | master |
| BL-1560 | 2.82 h | **784** | hashtag-fresh |
| BL-1561 | 1.00 h | **0** | both master AND hashtag-fresh |
| BL-1561 | 1.11 h | **0** | top-yield tag, fresh |

**NON-MONOTONIC IN SILENCE. The longest idle produced the second-worst result.** A per-IP token
bucket that refills with time cannot generate this sequence, and **"wait a long time and collect
a burst" is refuted as a scheduling rule.** What remains unidentified is what *does* govern it;
this round narrowed the field by three candidates and could not close it.

## 5. Part 3 — the walker, and a detector that refuses to run up a bill

The old walker took whatever tag order the candidate file listed and kept paying when the free
route dried up. In BL-1560 the free window landed on `#lebronedit` and `#motivationedit` **by
accident of ordering**. This one changes four things:

1. **Honest counting**, via the module above.
2. **Tags ordered by recorded yield** — 485 ranked tags, `#creededit` 16.2%, `#lakersedit`
   15.6%, `#michaeljordanedit` 12.8%. ⚠️ **Those are TikTok rates used as an ordering PRIOR and
   labelled as one**; `email_harvester.py` builds a `LamaTokClient` and says so.
3. **It halts when the free route drains** — a rolling window over the last N accounts against
   a floor.
4. **It reports the free share per tag**, so the ordering can be judged rather than assumed.

⚠️ **THE SIGNATURE SWEEP CAUGHT TWO OF MY OWN GUESSES BEFORE A SINGLE CALL.**
`free_contact.extract_emails_from` **does not exist** — the real extractor is
`bio_parser.extract_emails`. And `skip_account(account_id, handle="")` takes the **id first**;
I was passing the handle, which would have checked one key where the method deliberately checks
two. Five signatures have been guessed in five rounds; this time reading them cost a minute.

**THE DETECTOR, DEMONSTRATED LIVE ON A WALLED EXIT:**

    ---- #creededit  (TikTok prior 16.2%) ----
       tag done: 30 account(s), free-page 0/30, 0 addr, 0 NET-NEW  (free route drained)
    WALK OVER: FREE ROUTE DRAINED: 0% of the last 30 accounts served a page, below the 25% floor
       calls 2   spent $0.00138

It started on the **highest-prior tag**, fetched 30 accounts, and stopped for **$0.00138**.
Applied to BL-1560's second session — 874 paid profiles at an 88.4% paid share — the detector
would have bought about 30 instead of 874: **$0.02072 against $0.60362, a saving of $0.58290,
97% of that half.**

## 6. Part 4 — the walk, and the price in three parts

With the free window unavailable all evening and the operator wanting addresses, the walk was
run with the paid fallback **deliberately enabled** (it is off by default, and turning it on
also disables the drain halt — paying through a drained window is the thing the detector exists
to refuse, so it must be an explicit choice).

    calls                      316   (pages + paid profiles)
    spend    = 316 x $0.00069064                      = $0.21824
    NET-NEW addresses                                        94
    $ per 1,000 NET-NEW = $0.21824 / 94 x 1000        = $2.32

    row LINES 91 · distinct ACCOUNT IDS 91 · distinct ADDRESSES 94 · checkpoint netnew 94
    -> no duplicates (BL-1560's row file held 106 lines for 71 ids and was about to put 35
       duplicate rows into the lead store)

**The honest counter for this walk, reconciled:**

    accounts reaching the free route         304
      page LOADED                              0     0.0%     <- FULLY DRAINED
      WALLED (shell)                         304   100.0%
    PAID attempted (BILLED) / returned     304 / 294
    paid CHARGED AND EMPTY                    10             = 3.29% [1.80-5.93]
    RECONCILES: yes

The charged-and-empty rate is **3.29% [1.80–5.93]** against the 8.67% [6.99–10.70] prior —
lower, and the intervals do not overlap, so it is not a stable constant.

### THE THREE-PART PRICE

| regime | free share | $ per 1,000 net-new |
|---|---|---|
| free route SERVING (BL-1560 session 1) | 98.4% | **$1.11** |
| free route DEAD, top-yield tag (this walk) | **0.0%** | **$2.32** |
| free route DEAD, mediocre tags (BL-1560 session 2) | 11.6% | **$9.86** |

**Read that table twice.** Losing the free route entirely cost this walk about **2x**. Walking
the wrong tags cost BL-1560 about **4x** on top. **The controllable lever is the tag table, not
the free window.** At the round's *total* cost including every probe and the deliverability
pass, the 94 addresses came to **$3.02 per 1,000**.

## 7. Part 5 — the unit is editors, and this is where the cheap price gets worse

`editor_gate` fires on **6 of 91 = 6.59% [3.06–13.65]**.

    $ per 1,000 NET-NEW ADDRESSES = $0.21824 / 94 x 1000 = $2.32
    $ per 1,000 LIKELY EDITORS    = $0.21824 /  6 x 1000 = $36.37
      at the interval's edges     : $17.01 to $75.96

⚠️ **SAY WHAT THE INTERVAL PERMITS.** It permits anywhere from 3.1% to 13.7% of rows being
editors — between $17 and $76 per thousand. And **6.59% is well below BL-1560's 22.54%
[14.37–33.52]**, which is the uncomfortable half of this round's own headline: **the cheapest
addresses came from a film tag that is not editor-dense.** Cheap addresses and editor-dense
addresses are not the same objective, and the tag table ranks them by the first.

Three measurements of the editor rate now disagree — 13.33% [5.31–29.68], 29.37%
[27.57–31.23], 22.54% [14.37–33.52] and now 6.59% [3.06–13.65] — and **nobody has settled
them.** The gate is **not** validated here against `lead_kind` or `verdict`:
`writer.py:363-367` returns CLIPPER for any `tt:`/`ig:` source regardless of the bio and says
so in its own docstring.

**Deliverability**, checked with the bio present and both controls separating:

| | |
|---|---|
| MX resolves | **94/94 = 100.0% [96.1–100.0]** |
| sourcing — verbatim in the account's own bio | 94/94 = 100.0% |
| `address_ok`, both judgements | 92/94 = 97.9% [92.6–99.4] |
| role inbox (flagged, never dropped) | 4/94 = 4.3% |

## 8. The output

**94 net-new addresses written to `master_leads.csv`**, backup re-hashed *before* the write:

    rows 73,072 -> 73,166  (+94, expected +94)   OK
    cols 72 -> 72  UNCHANGED
    C0 control bytes in the new rows, checked BEFORE writing : 0
    workbook 'Emails' 2,143 -> 2,237 (+94); other sheets unchanged, read back from disk

### The suite, and what running it costs the ledger

    FAILED -- 25 red of 480 suite(s)   (2289.2s)

**25 red against BL-1560's 25, attributed PER SUITE NAME and never by subtracting totals: zero
newly red, zero newly green.** No production code under `clippershq/` was changed by this round.

⚠️ **AND THE SUITE CHARGED THE PRODUCTION LEDGER AGAIN, FOR THE THIRD ROUND, TO THE CENT:**

    rows   38,183 -> 38,395        (+212)
    total  67.186460 -> 67.224730  (+0.038270)
    vision 10.748717 -> 10.786987  (+0.038270)
    ig     46.932919 -> 46.932919  (+0.000000)   <- this round's money, untouched

**+212 rows and +$0.038270 of `free_judge_paid` spend that never happened** —
identical in row count and amount to BL-1559 and BL-1560, which makes three independent
reproductions of the same defect. `free_judge._book_paid_call` defaults to the production
ledger and the judge tests stub `_ask` but not the booking, so no network call is made and the
ledger is charged anyway. **None of it is Instagram spend**, so it does not touch the $0.28385.

## 9. WHAT I GOT WRONG

**1. I built a rate-limit model on a narrative instead of on artefacts.** "784 succeeded one
hour later at a slow pace" — the gap was 2.82 h and the pace was ~1.3 s/account, identical to
the probe that walled at 45. Caught by re-deriving the timeline from files. It cost nothing
only because I checked before spending.

**2. My own 2×2 could not test the thing it was built to test.** Both history arms came from
master, where every handle has already been fetched. The all-zero result hid the flaw; I found
it by re-reading the design after the fact, not from the data.

**3. I spent 130 free requests into an exit I had already walled**, across the 2×2 and the
first origin test — the confound this round exists to criticise. Only after that did I put the
silence gate in code. The gate then refused correctly, twice.

**4. ⚠️ I WROTE THE SAME DEFECT I WAS FIXING, IN THE SAME ROUND.** My per-tag display counter
`tg["free_bio"]` increments on `state == "present"`, which is true for a bio from **any** route
once the paid fallback is on. The progress line printed `free-page 0  free-bio 74` — a
statement that is impossible on its face, and that is how I caught it, mid-run. **Blast radius
is display and the per-tag checkpoint field only:** the authoritative module counter records
`free_bio_present` and `paid_returned_bio` separately and reconciles, and every headline number
here comes from it. But I named a counter for a route it does not measure while writing the
round about naming counters for routes they do not measure.

**5. I reported "780 free" last round from a counter I already knew was broken**, and did not
re-derive it until this round. The identity that corrects it is three lines of arithmetic and
was available the whole time.

## 10. What did not run, reported as ABSENT

* **What actually governs the free window.** Four points, non-monotonic in silence. Three
  candidates are dead; the mechanism is not identified. **This is still the most valuable open
  question in the project**, because it is worth 2x on every Instagram address.
* **Whether the wall is per-handle at all.** Both origin tests ran against a walled exit, so
  the hypothesis is untested rather than refuted. It needs a cold exit, and I could not get one.
* **Whether the TikTok yield ordering transfers to Instagram in general.** This walk is
  suggestive — the top-prior tag returned 94 addresses from 304 accounts — but it is **one tag**,
  and BL-1560 showed one TikTok class inverting completely on Instagram.
* **The editor-rate disagreement**, now four-way and untouched again.
* **The HTML page vs the JSON endpoint as separate budgets.** Refuted as the explanation for
  *these two numbers*; never tested as a fact in its own right.

---

https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/BL-1561-the-free-route-and-what-actually-sets-the-price.md
