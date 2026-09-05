# BL-1502 — Two of the three levers were already pulled, and one was two models fused

**2026-09-05.** Vendor spend **$0.00** by the run's own counter, against a **$2.00** cap.
No page was walked, no model was called, no socket was opened.

---

## THE ANSWER, FIRST

**This round did not reduce his cost or his clock, and I am not going to imply otherwise.**

It was sent to pull three levers. Measuring them first — which the brief demanded — showed
that **two had already been pulled by earlier rounds, and the third was two different models
fused into one description.** What I shipped instead is the *ruler*: five price constants that
were mis-billing Instagram by 13.1%, one of which would have inflated TikTok by 15.1% if
"fixed" the obvious way.

So the honest before/after per brain is: **unchanged.** The numbers below are the baseline,
and the gap is stated exactly rather than approximated toward.

| brain | $ / 1,000 delivered | h / 1,000 | vs $2.00 | vs 2 h |
|---|---|---|---|---|
| TikTok memes | $19.52 | 8.21 | **9.8x over** | **4.1x over** |
| Instagram edits | $131.21 | 175.22 | **65.6x over** | **87.6x over** |
| Instagram memes | $176.76 | 265.69 | **88.4x over** | **132.8x over** |
| TikTok edits | 0 delivered | — | **undefined, not free** | — |

⚠️ Those rest on **one to six runs per brain** with the seconds as a **pooled ratio, not a
median**. They are the baseline to beat, not precision.

---

## 1. WHAT I WAS ASKED TO DO

Get the cost and the clock down: time-box or remove a slow judge model; move a pre-judge
profile purchase; shift the discovery mix; and make the five stage counters measurable first.
**Gate: do not start until three prior rounds have committed and published, verified by
driving the shipped code and parsing the committed blob — not by reading their reports.**

---

## 2. WHAT SHIPPED

| # | change | fix category |
|---|---|---|
| 1 | Four Instagram price constants re-priced to the true rate | **GENERAL** — each imports one canonical constant instead of a seventh literal |
| 2 | `email_finder` split into **two** constants, one per vendor | **GENERAL** — the one-constant-two-vendors shape is gone |
| 3 | The billing summary now prints **each leg's own price** | LOCAL |
| 4 | The gate itself: six rounds verified by driving | — |

**Nothing else was changed.** No judging rule was added or loosened. No file held by another
round was touched.

---

## 3. WHAT WAS MEASURED

### 3a. THE GATE — and I nearly published a false failure on a correct fix

Parsing the **committed blob** (not the working tree — three rounds were writing): the
booking chokepoint exists, all three former sites route through it, and the wrapper passes no
argument the inner function lacks. **That is the mismatch a grep and a signature check both
miss**, and it is clean.

Then I drove it, and my first probe said **FAIL: a failed send still books.** It was my probe
that was wrong. Reading the predicate showed the design **deliberately errs toward billing**,
because the ledger feeds the caps — **a ledger that reads LOW authorises MORE spend than the
budget allows.** Only failures that provably never generated return False.

Re-driven across the whole matrix the predicate actually distinguishes:

| failure class | booked | expected | |
|---|---|---|---|
| SUCCESS (control) | 1 | 1 | PASS |
| HTTP 402 / 401 / 400 — refused before generating | 0 | 0 | PASS |
| HTTP 500 — may have generated | 1 | 1 | PASS |
| connection refused — never left the machine | 0 | 0 | PASS |
| read timeout — sent, no reply | 1 | 1 | PASS |
| torn JSON — bytes were received | 1 | 1 | PASS |
| bare exception — unclassifiable, errs to billing | 1 | 1 | PASS |

**9 of 9.** The fix is better reasoned than the brief describes it.

**AND IT RECLASSIFIES EIGHT PHANTOM LEDGER ROWS FROM AN EARLIER ROUND OF MINE.** They were
written by probes that sealed the socket with a *custom* exception, which the predicate cannot
classify, so it books — correctly. A probe sealing with a socket-level error books **nothing**.
Those rows are not evidence of the old bug; they are the new code behaving as designed.

### 3b. THE CLOCK — the brief fused two different models   [MEASURED, second denominator]

| model | reject authority | calls | median call | usable inside the 45 s timeout |
|---|---|---|---|---|
| the paid model, tried first | **90** | 325 | 5.90 s | **91.4%** [87.8, 94.0] |
| the second scored model | **90** | 428 | **20.59 s** | **88.1%** [84.7, 90.8] |
| a free-chain model | **none** | 641 | **98.71 s** | **17.3%** [14.6, 20.4] |

**The "16.4% usable, 68.8 s median answered" model is the third one — which holds NO reject
authority and is never asked**, because the free-try limit slices it off the chain.
Independently recomputed as **17.3% on 641 calls** against the code's 16.4% on 390.

**The model that DOES hold reject authority answers inside the timeout 88.1% of the time.**

**And the "30.85% of the judging stage" is a page-total artefact.** The page-level file
reproduces it exactly — 9 pages, median 116.33 s — but **every one of those rows records two
calls**: it is a page total spanning a failed first attempt plus throttle wait, not a model's
latency. Per call, that model medians **20.59 s**. **Same model, two denominators, 5.6x apart.**

**What a 45-second time-box would cost: ZERO CUTS.** 25 of 428 verdicts lost (6.2%), and **0
of them are cuts** — all 94 of its real cuts land under 45 s. On the 200-page run it changed
**zero verdicts**: its 7 REJECTs came in at confidence 0, 0, 72, 72, 75, 78, 80 — **every one
below its own bar of 90.**

**Controls fired:** the shipped predicate replayed over 200 rows reproduces the recorded drops
**200/200**, including all 108 real drops; a synthetic REJECT@95 cuts and REJECT@89 does not;
and 94 real cuts exist in the call file, so the harness can demonstrably produce a kill.

**The verdict-change scoring is INCONCLUSIVE and I will not pretend otherwise.** On the 97
handles both cutters answered (he wants 29, rejects 68): **2 of 29 wanted pages killed = 6.9%,
Wilson [1.9%, 22.0%]**, identical for both models; constant-answer baseline on that scope
**70.1%**. **All 7 cuts unique to the second model are pages he does NOT want**, so removing it
rescues nothing and costs 7 correct catches. Clearing a 5% upper bound needs **0 kills on 73**,
or 2 on **142**. At n=29 the bound is 22% — that cannot support a ship-or-cut decision.

⚠️ **A number was retracted mid-measurement.** An unfiltered mark corpus classified the judge's
own output as marks and scored the model **against its own verdicts**. That figure is withdrawn;
the table above excludes it.

**The time-box is free and worth doing — but the file is held by another live round, so it is
handed over rather than taken.**

### 3c. THE MONEY — the purchase was already moved   [MEASURED]

Both briefed line numbers had **moved** (the purchase and the picture judge). The execution
order today: free rules judge -> **free rejection returns** -> free bio email -> profile gate
-> **paid profile** -> picture judge.

The purchase still precedes the picture judge, **but it is already gated behind three measured
conditions** and the code says so: *"only for a page ALREADY APPROVED, only when want_emails
is on, and only when the FREE bio did not already yield the address."*

| era | rows | reached the gate | bought |
|---|---|---|---|
| before that gate | 3,412 | 1,771 = **51.91%** | **100.00%** of gate-reachers |
| after | 4,113 | 520 = **12.64%** | **4.62%** of gate-reachers |

**The saving applies to 11.18%–47.27% of pages, not 100%. The "1,185 verdicts" headline
over-states the affected population by roughly 1.1x–4.6x.**

**AND THE WASTE IS ZERO.** Across 14 run files / 2,447 rows: **1,258 pages bought a profile,
and 1,258 of them ended as targets. Zero bought profiles were later rejected.**
⚠️ **The discriminating-field control fired**: that field is **1,263 True / 1,184 False**
overall, and **all 1,184 False rows are among the NOT-bought** — cut before the purchase. The
zero is earned, not assumed. **There is no "stop paying before you decide" saving left here.**

**Route (a) is nonetheless proven available**, if it is ever moved again: **all four prompt
fields are free on 108/108 recorded authors**, and a free-sourced prompt is **byte-identical to
the paid one on 97/108** (+0.48% bytes). The 11 differences are one line every time —
`followers` — on exactly the 11 authors whose count is **0**, because the paid path uses
`or`-truthiness and **silently drops a real zero**. Route (a) is a strict superset and fixes
that bug. ⚠️ **The brief is wrong on two of the four fields**: display name is already free
(lost 0/108) and post count is lost 1/108; only `verified` and `followers` are genuinely lost.

### 3d. THE PRICE CONSTANTS — searching one layer out found 7, not 5

| file | verdict | action |
|---|---|---|
| four Instagram files | wrong, live | **re-priced** |
| the email finder | **BOTH vendors from ONE constant** | **split in two** |
| two more | vendor **not settled** by any call site | **left, and named** |

**The email finder is the one that mattered.** It billed both legs from a single constant, so
raising that value would have fixed Instagram **and inflated TikTok by 15.1% in the same
edit** — indistinguishable from a correct fix if you only checked the Instagram number.

**PROOF, 10 of 10, with TikTok as the control:** the four re-priced constants read the true
Instagram rate; the split file reads the true rate on one leg and **the unchanged TikTok rate**
on the other; driven at 1,000 calls each, the legs bill **$0.6906 vs $0.6000 — they differ**;
and TikTok's own constant is **untouched**.

**And the display lied until I fixed that too:** the summary printed one price for both legs,
so after the split the arithmetic was right and the **label** showed Instagram at TikTok's
price. That is how the original error survived.

### 3e. THE COUNTERS AND THE CAP — both already correct   [DRIVEN]

All five stage counters are present on a **fresh** record, all five **moved** (7/5/3/2/1), an
undeclared key was **dropped with a loud warning** so the whitelist still binds, and `None`
(never measured) stays distinguishable from `0` (measured zero) on disk.

**The cap binds: 6 of 6, every control firing.** A declared zero refuses; absent is not
confused with zero; a zero budget stops before the first page. Live room was
**$100.00 − $61.472656 = $38.527344**, so this prompt's **$2.00** was the binding number.

---

## 4. WHAT WAS REFUSED OR NOT DONE

- **The time-box was not applied** — its file is held by a live round. Measurement handed over.
- **The profile purchase was not moved** — measured and **deferred with the arithmetic**, which
  the brief explicitly permits, because the waste it would recover is **zero**.
- **PART 3, the source mix, was NOT ATTEMPTED.** This is the real gap in this round. I spent it
  establishing that Parts 1 and 2 rested on wrong premises, and I would rather say that than
  ship a mix switch on top of unverified arithmetic.
- **Two price constants were left alone** because no call site settles their vendor. Changing
  them on a filename would be the exact error this round exists to avoid.
- **The source stamp and the rule reason were not done.**

---

## 5. WHAT I GOT WRONG

1. **I nearly published "the booking fix is broken" on a correct fix**, because I raised a bare
   exception the design deliberately bills for. My instrument was wrong where the code was
   right. Caught by reading the predicate instead of trusting the probe.
2. **My backup helper made the exact mistake the brief warned about.** It hard-coded body key
   names, so a **1,900-row** store reported **3 rows** and a **2,193-row** list reported
   `None`. Fixed structurally — the body is now found by shape, not by a longer list of names.
3. **My own syntax check printed PASS without running**, in an earlier round of mine, and the
   same shell-pipeline shape nearly recurred here. Exit codes are read explicitly now.

---

## 6. MONEY AND SAFETY

- **Vendor calls: 0. Spend $0.00**, by the run's own counter — never a ledger delta, which
  cannot attribute anything (no run id on any row, and one model books nothing).
- **Backups 8/8 sha256-verified, with a control proving a single flipped byte is detected.**
- **Seen stores: row KEY SETS recorded** — 2193 / 6125 / 2446 / **1900** / 1715. No row read,
  written or deleted.
- **No process killed.** His sheet server untouched. The dashboard port was re-checked
  immediately before every write under the application directory.
- ⚠️ **`dashboard/.running.json` claims a live dashboard on a pid that does not exist**, and has
  since 30 August. It was not used for any decision here.
- **No key, address or handle printed, logged or committed.**

---

## 7. WHAT HE SHOULD DO NEXT

1. **Take the free time-box.** It costs **zero cuts** on 428 recorded calls. The file's holder
   has the measurement.
2. **Do not spend a round moving the profile purchase.** The waste is **0 of 1,258**. Route (a)
   is proven available if that ever changes.
3. **The source mix is the untouched lever**, and on the published arithmetic it is worth
   **3.6x** on pages-walked-per-approved-page. It needs its own round and a switch.
4. **Settle the two unresolved price constants** by finding their callers.
5. **Accept that the targets are not close.** The best brain is 9.8x over on money and 4.1x
   over on the clock, and nothing measured this round changes that.

---

## 8. PATHS

```
scratch/bl1502_gate.py              parse the committed blob; wrapper/inner mismatch
scratch/bl1502_drive_gate.py        drive the booking fix and the counters
scratch/bl1502_billing_matrix.py    9 failure classes, 9 of 9
scratch/bl1502_cap_binds.py         the cap, 6 of 6, controls firing
scratch/bl1502_backup.py            8/8 verified, with a corruption control
scratch/bl1502_fix_prices.py        the four Instagram re-prices
scratch/bl1502_price_proof.py       10 of 10, TikTok as the control
scratch/bl1502_profile_waste.py     0 of 1,258, with the discriminating-field control
clippershq/email_finder.py          two constants, one per vendor
```

---

## 9. THE SINGLE LARGEST REMAINING GAP

**The clock on Instagram.** Instagram memes is **265.69 hours per 1,000 delivered** against a
**2-hour** target — **132.8x over** — and nothing in this round, or in the two levers it was
sent to pull, touches it. The mix shift is worth 3.6x on pages walked; even taken in full it
was costed at **8.6 hours per 1,000**, still **4.3x over**. **No measured lever currently
closes the Instagram clock, and pretending otherwise would be the confident wrong number this
project has been hurt by more than by missing ones.**
