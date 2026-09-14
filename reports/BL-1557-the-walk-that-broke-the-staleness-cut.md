# BL-1557 — a real Instagram walk: 30 net-new addresses at $7.57 per 1,000, and the staleness cut is wrong 93% of the time

**30 net-new Instagram addresses, from 5 hashtags, for $0.26866 of a $0.75 cap — the walk
itself cost $7.57 per 1,000 net-new [$5.37–$10.74] and the whole round $8.96 per 1,000,
against a $44.61 [$20.72–$97.05] bar. The free bio FIRED on a
live page: 285 of 584 bios (48.8%) came free, and 29 of 30 addresses are MX-deliverable
(96.7% [83.3–99.4]) with all 30 taken verbatim from the account's own bio. About 4 of the 30
are likely editors (13.3% [5.3–29.7]) — an interval that permits anything from 5% to 30%, so
treat it as "consistent with the expected 16.4%", not as a measurement. The addresses are in
the `Emails` sheet of `clipper_emails_ALL.xlsx` on the Desktop, which grew 2,042 → 2,072 rows,
and in `master_leads.csv`, which grew 72,971 → 73,001 rows with its 72 columns unchanged.
⚠️ AND THE HEADLINE FINDING IS A WARNING, NOT A WIN: the 17-month staleness cut shipped last
round flagged HALF this walk, and when I bought the accounts' real post dates, 14 of those 15
flags were WRONG — 93.3% [70.2–98.8] false cuts, including an account that posted THE SAME DAY
being flagged as 761 days dead. Nothing was deleted; the cut is flag-only in this run. It must
not be turned on for this surface.**

---

## 1. What this project is, for a reader with no context

ClippersHQ finds video editors and meme-page operators on TikTok and Instagram and collects the
email addresses they publish in their own profile bios, so its operator can contact them about
paid clipping work. It buys data from two vendors: **HikerAPI** for Instagram
(`ig_api.cost_per_call_usd` = **$0.00069064** per call) and **LamaTok** for TikTok
(`api.cost_per_call_usd` = $0.000600). Those two numbers are 15.1% apart and reading the wrong
one once let a $3.00 cap spend $3.45, so every figure here is the Instagram one, read by named
key.

This round was asked to stop measuring and actually run: walk real Instagram hashtags, try the
free bio route first and fall back to paid, and report what it cost, what it found, and whether
the free route fired.

## 2. Safety, and the cap that had to bind first

Nine stores were backed up and sha256-verified before anything ran, with their bodies found by
**shape** rather than by a top-level key count — `spend.json` is a dict whose payload is at
`runs`, `clip_seen.json` is a bare list of 2,193, and `tiktok_pages_seen.json` is a dict at
`pages` holding **3,270** where a dict-only reader reports **3**. All six corruption controls
fired, including the position-qualified one: deleting one of a duplicated pair leaves the
natural-key **set** provably identical, and the digest still catches it.

The cap was proved to bind **before the first paid call**, by lifting `Budget` out of
`harvest_run.py` **by AST** and exec'ing the shipped class rather than a copy:

| check | result |
|---|---|
| unit used | `ig_api.cost_per_call_usd` = $0.00069064, by named key |
| `harvest_run`'s own default unit | `harvest_accounts.USD_PER_CALL` = $0.00069064 — **is** the IG unit, not TikTok's |
| funded budget | allows, meter advances by exactly one unit |
| $0.00 budget | **raises**, and the meter does **not** advance on the refusal |
| cap with room for 2 | refuses the 3rd |
| 8 threads against one cap | 199 calls granted of 200 allowed — **within cap** |
| did the proof write anything? | **no** — repo snapshotted before and after, 0 files added, 0 changed |

⚠️ **`Budget.reserve` is a check-then-increment with no lock.** It held here, but it is a real
race and this is measured, not assumed. It is not load-bearing for this run because **the walk
uses one lane** — Instagram's wall is per-IP and more lanes make it worse.

## 3. Part 1 — the free bio fired, and one published finding is wrong

**It fired.** On 8 live pages through Chromium: 7 read, 1 walled, and **7 of 7 free bios
value-matched the stored paid bio**. This exit's anonymous quota — which BL-1554 measured as
spent, recovering 0 of 50 over 72.6 minutes — **had recovered**.

Then a head-to-head on the same 12 handles, interleaved in the same minutes, because two rounds
disagreed and both could have been right:

| route | bio returned | value-matched | median | p90 |
|---|---|---|---|---|
| **A — plain HTTP under `PROFILE_UA`** (not a browser UA) | 10/12 | 6/10 | **0.67 s** | 0.92 s |
| **B — real Chromium** | 10/12 | 6/10 | 1.87 s | 1.98 s |

They agree **handle for handle**: the same 10 succeed, the same 2 return `unknown`, the same 6
match. Plain HTTP is **2.8x faster**.

⚠️ **THIS REFUTES BL-1554's "IT IS THE CLIENT, NOT THE IP — URLLIB CAN NEVER WORK."** That
round tested urllib bare, urllib with a perfect Chrome UA, full Chrome header order with
`Sec-Fetch-*`, and HTTP/2 — **every Python arm sent a browser user-agent**, and `ig_bio`'s own
docstring says in capitals never to send a desktop-Chrome one, because desktop Chrome gets a
~623 KB shell with nothing in it. BL-1554 measured *"a Python client pretending to be Chrome is
refused"*, and generalised it to *"Python is refused"*. The TLS-fingerprint explanation was
never needed. A Python HTTP client under an honest user-agent works exactly as well as Chromium.

*(The 4 of 10 that did not value-match are identical across both routes, which is what rules
them out as route failures: they are bios that changed since the stored copy was bought.)*

### Where the free route died, measured

The walk's own timeline is sharp. Every address found up to **6.1 minutes** in came from the
free route; **every one after came from a paid call**:

```
 0.0–6.1 min   free_http  ██████████████████   19 addresses
 6.6–24.2 min  paid       ███████████          11 addresses
```

Across the walk: **285 of 584 bios free (48.80% [44.77–52.85])**, 265 paid (45.38%), 34 with no
bio from any route (5.82% — `unknown`, never `empty`). Counting the probes, roughly **300–320
profile fetches from this exit** preceded the wall, which sits below but in the same region as
BL-1554's ~445-render figure.

**The Chromium fallback rescued 0 of the accounts the free route lost** — and that zero has a
positive control: capture files exist on disk, so the browser genuinely ran. It was walled too,
which matches BL-1554's finding that the quota is keyed to the IP and survives a fresh context,
a fresh cookie jar, a fresh process and a different engine.

## 4. Part 2 — the walk

**Tags were chosen so they provably exist.** 35 of 35 "fresh" tags a previous round picked
returned server errors because the names do not exist — they look fresh in the ledger precisely
because nobody could ever walk them. The ledger keys on tag **and** endpoint, and it holds **489
tags walked on the plain endpoint against only 83 on `@v2`**. A tag with a plain entry is
therefore *proven to exist* and *fresh for v2*, which is where the volume is. 406 such tags
exist; the film-bucket ones were ranked by prior yield.

Film bucket only: **9.22% [7.79–10.88] on Instagram against sport 3.37% and anime 1.26%**.
Real-fighter tags were **not opened** — three independent TikTok measurements put them at 1.21%
[0.68–2.15], non-overlapping with film.

### Yield per tag, and where each stopped

| tag | pages | distinct authors | new accounts | with an address | **NET-NEW** | stopped because |
|---|---|---|---|---|---|---|
| `#cobrakaiedit` | 12 | 197 | 79 | 13 | **11** | pages exhausted |
| `#magnetoedit` | 12 | 342 | 139 | 6 | **6** | pages exhausted |
| `#saulgoodmanedit` | 12 | 235 | 138 | 6 | **6** | pages exhausted |
| `#warrioredit` | 10 | 223 | 202 | 3 | **3** | no `next_page_id` |
| `#wolverineedit` | 1 | 29 | 26 | 4 | **4** | target reached |

Saturation was decided **by body hash, never by `has_more`** — a surface once reported
`has_more: true` on 7 of 7 pages while pages 3 and 4 came back byte-identical to page 2. No tag
saturated by repeat here; four ran out of pages and one hit the target. **0 pages came back
HTTP 200 with an empty list**, which is the other trap (five of six parameter variants once
returned 200, charged and empty).

### Four denominators, counted separately

```
sections .................... 452
top-level slots ............ 1355
slots incl. carousel ....... 1355
DISTINCT account ids ....... 1026   <- the only one that means "accounts"
```

329 slots (24.3%) were the same account appearing again. Reading sections as medias, or slots as
accounts, would overstate the surface by 2.3x and 1.3x respectively.

### Dedup

**440 of 1,026 accounts (42.88% [39.89–45.93]) were skipped as already held — BEFORE their bio
was fetched**, which on Instagram is the entire saving. The guard loaded **72,956 accounts and
12,691 addresses**; a build that loads zero is silently vacuous and would have made every
account look new, so a zero count is a hard stop.

⚠️ **`DedupGuard.build()` reads ADDRESSES from master but not ACCOUNTS** — accounts come only
from `prior_rows`/`extra_accounts`, so master's handles were passed in explicitly. A default
build knows zero accounts.

⚠️ **Polarity was proved before walking**, on a value known to be held: `claim_address` returns
a **reason string to refuse** and `None` when fine. A round that wrote `if guard.claim_address(e)`
kept only duplicates. The control asserted a held address is refused *and* a fresh one allowed.

**Proof of zero duplicates:** 30 addresses shipped, 30 distinct; 30 accounts shipped, 30
distinct. Deduplicated on both keys, after normalising case, trailing dots, zero-width and
fullwidth look-alikes.

## 5. Part 3 — did the shipped filters fire?

**Which funnel:** this walk drives `quality_gate.qualify_author` — **the editor funnel** — so
the 17-month cut *could* fire. `meme_finder.py` and `tiktok_finder.py` never import
`quality_gate`; they cut at 180 days on an account-level date instead.

### The corporate flag — fired, and behaved

`role_policy` classified the 30 addresses as **28 personal, 1 role, 1 agency**. Both non-personal
addresses were **flagged and kept**, never dropped. One carried
`domain_reads_as_creator_or_business:studios`.

### The staleness cut — fired, and was wrong 93% of the time

The cut flagged **15 of 30 = 50.00% [33.15–66.85]** as stale. BL-1556 measured it removing **2
of 1,274 authors (0.16%)** on the stored corpus with a false-cut rate of **0 of 691 [0.00–0.55]**.
Those two numbers cannot both describe the same rule, so I bought the answer: for all 30
accounts I fetched the account's **own** newest post and compared it to the hashtag-matched date
the rule had judged.

| | result |
|---|---|
| **FALSE CUTS** | **14 of 15 = 93.3% [70.2–98.8]** |
| missed, on the FRESH arm (control) | **0 of 15** |
| matched date understates recency by | **median 489 d, p90 971 d, max 1,180 d** |

A sample of what the rule called "stale", against what the account had actually done:

| matched clip | account's real newest post | verdict |
|---|---|---|
| 761 days | **0 days — posted today** | FALSE CUT |
| 784 days | 1 day | FALSE CUT |
| 1,159 days | 2 days | FALSE CUT |
| 525 days | 3 days | FALSE CUT |
| 1,020 days | 48 days | FALSE CUT |
| 598 days | 586 days | correct |

**This is the documented failure case, reproduced live and quantified.** `quality_gate.py`
carries a hard rule written after exactly this: *"an old edit still ranking in the feed makes an
ACTIVELY-POSTING editor look 400 days dead (real case: an account posted 1 day ago but was
flagged 390d, 9/15 leads hit bogus penalties)."* The `/v2/hashtag/medias/clips` surface returns
**top-ranked** clips, so its dates say how good a clip was, not when the account last posted.

**Why BL-1556's 0.16% was not wrong, and still misled.** It measured a different surface, where
the matched date understates recency by a median of 2.3 days. Here the median understatement is
**489 days — 213x larger**. The rule is safe on the surface it was measured against and unsafe
on this one, and nothing in the config distinguishes them.

**Nothing was deleted.** The cut is flag-only in this harness; all 30 addresses shipped, with
the verdict recorded next to each. **Recommendation: set `hashtag_stale_max_months = 0` (its
documented disable) until the cut can read an account-level date** — `deep_latest_ts`, which it
already prefers when present. On this surface it would reject half of every walk and be wrong
about 93% of those rejections.

## 6. Part 4 — the numbers, every division written out

```
unit (ig_api.cost_per_call_usd) .... $0.00069064
calls billed ....................... 329  = 47 hashtag pages + 282 profile calls
walk spend  = 329 x $0.00069064 .... $0.22722
+ deliverability re-fetch (30) ..... $0.02072
+ the false-cut test (30) .......... $0.02072
ROUND TOTAL ........................ $0.26866  of a $0.75 cap  (35.8% used)
```

| | |
|---|---|
| accounts touched (distinct) | 1,026 |
| skipped as already held | 440 (42.88% [39.89–45.93]) |
| distinct new accounts | 584 |
| bios FREE | **285 (48.80% [44.77–52.85])** |
| bios PAID | 265 (45.38% [41.38–49.43]) |
| no bio from any route | 34 (5.82%) — `unknown`, not `empty` |
| accounts carrying an address | 32 (5.48% [3.91–7.63]) |
| **$ per 1,000 accounts touched** | $0.22722 / 1,026 × 1000 = **$0.22** |
| **$ per 1,000 NET-NEW addresses — the WALK** | $0.22722 / 30 × 1000 = **$7.57** |
| …as an interval | **$5.37 – $10.74** |
| **$ per 1,000 NET-NEW — the WHOLE ROUND** | $0.26866 / 30 × 1000 = **$8.96** |

⚠️ **Which spend the headline divides matters, so both are given.** $7.57 is the walk alone —
what a repeat of this walk would cost. $8.96 divides the round's *entire* spend, including the
$0.04144 I spent on two diagnostics that found nothing a production run would need (re-buying
30 bios to fix my own empty-bio bug, and buying 30 real post dates to test the staleness cut).
**$8.96 is the honest number for "what did this round cost per address"; $7.57 is the honest
number for "what does this walk cost".** Neither is quotable as the other.
| wall clock | 1,457.6 s (24.3 min) |
| seconds per account | **median 1.12 s, p90 3.71 s** |

⚠️ **The addresses split three ways, or the price is understated.** 32 raw addresses: **0**
already held for the same handle, **2** held under a different handle (duplicates, worth $0),
**30 NET-NEW**. Reporting the 32 would have understated the price by 6.7%.

**Against the bar:** $44.61 per 1,000 cold [$20.72–$97.05] is the population a fresh walk
resembles. This walk came in at **$7.57 [$5.37–$10.74]** — intervals that do not overlap. The
reason is not a better funnel: **the free bio carried the first half of the walk**. Had the
quota been spent from the start, all 584 bios would have been bought and the price would have
been roughly `(47 + 584) × $0.00069064 / 30 × 1000` = **$14.53 per 1,000** — still under the
bar, because 42.9% of accounts were skipped before their bio was ever fetched.

⚠️ **17 of 282 profile calls (6.03% [3.80–9.44]) were CHARGED AND EMPTY** — billed, and returned
no biography.

### Deliverability

| | |
|---|---|
| MX resolves | **29/30 = 96.7% [83.3–99.4]** (1 dead domain) |
| taken verbatim from the account's own bio | **30/30 = 100.0% [88.6–100.0]** |
| `address_ok` (both judgements) | 29/30 = 96.7% |
| role inbox — flagged, kept | 1/30 |
| short local part — flagged, kept | 0/30 |
| structurally suspect (`@handle` trap) | **0 of 30** |

MX was refreshed against **this run's 8 domains**, not by a bare refresh — a bare refresh
re-probes domains already covered, so it reports success and changes nothing.

The `@handle` trap found nothing, and that absence is a result rather than a miss: the
de-obfuscator that rescues `name @ gmail.com` also fuses a lead-in word onto a handle, and 66 of
1,870 addresses were once removed for it. `.cc`, `.uk` and `.com` are all real TLDs, so suspects
are **listed** rather than counted — a first-draft rule once caught 20 rows of which 11 were
genuine Gmail addresses, caught only because someone listed them.

### The editor rate

**4 of 30 = 13.33% [5.31–29.68]** pass `editor_gate`. The expected figure for a fresh Instagram
walk is 16.4% [11.20–23.45], and TikTok's first harvest was 49.5%.

⚠️ **On 30 rows the interval is ±12 points and permits anything from 5% to 30%.** It is
consistent with the expectation and cannot distinguish it from half or double. The gate's own
honest accuracy is **precision 87.65% [78.74–93.15], recall 94.67% [87.07–97.91] on n=240** —
not 97.56%, which was one sample of 120 while a disjoint 120 scored 79.41%.

⚠️ **Not validated against `lead_kind` or `verdict`:** `writer.py:363-367` returns CLIPPER for
any `tt:`/`ig:` source regardless of the bio, and its own docstring says so. Two guesses agreeing
is not evidence.

## 7. Part 5 — the output

`master_leads.csv`: **72,971 → 73,001 rows, 72 columns unchanged.** The backup was verified by
sha256 **before** the write, against the digest recorded at round start.

The workbook was found by **searching** — a hard-coded path once reported "workbook not found",
which reads exactly like *deleted* and was nothing of the kind. Exactly one candidate was found;
more or fewer would have been refused rather than guessed. Rows counted **with a parser, never
by counting lines** (bios contain newlines; a line count once reported 346 and 3,755 where the
truth was 103 and 1,739):

| sheet | before | after |
|---|---|---|
| **Emails** | 2,042 | **2,072** (+30) |
| No email | 24,241 | 24,241 |
| Unjudged leads | 13,178 | 13,178 |

Read back from disk after writing and compared per sheet — a workbook once silently lost 66
addresses and nobody noticed for a round. Zero C0 control bytes were asserted **before** writing.
Three columns were **added** (bio source, staleness, email quality) so every new row is marked
with platform, tag, FREE or PAID, the staleness verdict, the corporate flag and the editor
verdict. Nothing was overwritten and nothing deleted. The spreadsheet is not committed.

### The suite

    FAILED -- 25 red of 480 suite(s)   (2684.3s)

**This round changed no production code**, and the red set is **identical** to BL-1556's
closing baseline — zero new, zero fixed, attributed per suite name rather than by subtracting
totals. The 25 are pre-existing.

## 8. WHAT I GOT WRONG

**1. I reported "0 of 30 passing deliverability" from a bug in my own harness.** I called
`check_row(addr, "")` with an empty bio, so every address was rejected for
`not_a_verbatim_substring_of_the_bio`. A **planted control — a bare `@gmail.com`, whose MX is
beyond doubt — came back `reject` too**, which is what exposed it. The tell was the shape of the
zero: every subgroup vanished while the denominator was right, which means the grouping key is
wrong, not the data. The real numbers are 96.7% MX-deliverable and 100% verbatim-sourced. **I
had to re-buy 30 bios ($0.02072) to fix a number I had already reported once.**

**2. I then produced a SECOND confident zero from the same class of error, and paid for it.**
The false-cut test asked for `taken_at`, got nothing on all 30 accounts, and printed
`unknown (no date returned -- ABSENT)` thirty times. The field on that endpoint is **`1ltaken_at`**
— a prefixed spelling — while the *hashtag* endpoint uses the plain name. Two endpoints from one
vendor, two spellings for one field. **That zero cost $0.02072 before I stopped to check it.**
What saved it was the standing rule: a 100% zero is an instrument failure until a control says
otherwise. Had I believed it, I would have published "the staleness cut could not be checked"
instead of the finding this round exists for.

**3. I nearly walked with a dedup guard that knew zero accounts.** `DedupGuard.build()` loads
addresses from `master_leads.csv` but **not accounts** — those come only from `prior_rows`. A
default build would have reported all 1,026 accounts as new, re-bought 440 bios, and shipped
duplicates. I caught it by reading `build()`'s body rather than trusting its name, and by
hard-stopping on a zero count.

**4. My bio-source counters count route ATTEMPTS, not successes.** `bio_free` reads 319 while
only 285 bios actually came free — the other 34 were free-route attempts that ended `unknown`.
The honest figure is derivable (584 − 265 paid − 0 Chromium − 34 none = 285) and that is what is
reported, but the counter as written would mislead anyone reading the raw checkpoint. A counter
named for a route should count what that route delivered.

**5. THE MONEY IS OFF THE BOOKS. This round's $0.26866 never reached `spend.json`.**
`IgClient(metered_by_caller=True)` is correct and was required — its autoflush was once
measured booking money **exactly 2x**. But turning autoflush off makes the *caller* responsible
for metering, and my harness never called `flush_spend`. Checked directly: **`ig_usd` booked in
the last 2.5 hours is $0.00000**, while my own counter says 389 Instagram calls and $0.26866.
The only recent ledger activity is a concurrent funnel's $0.03827 of vision spend.

So the vendor was paid and the ledger does not know. Lifetime totals and anything that reads
them for a cap are short by $0.26866. This is a known enough failure that `spend_ledger.py`
ships a function called **`money_off_the_books()`** to detect it.

**I have not booked it.** Hand-writing a row into a shared 15 MB ledger that a live funnel is
appending to is the shape that once deleted 56 rows another round had just written, and the
brief's own rule is to attribute by my counter rather than touch that file. The exact figure is
here, the backup is verified, and booking it is a decision for the operator — but **the gap is
real and it is mine**, not a quirk of the ledger.

**6. I described the free-route wall as "recovered" before I had watched it die.** The probe
said 7/8 and I wrote the economics around free bios. Six minutes into the walk it was gone. The
right statement at probe time was "it is open **now**, and the quota is ~445 renders", not "it
is open".

## 9. What did not run, reported as ABSENT

* **Whether the free route recovers, and how fast.** It died at ~6 minutes and every later
  fetch was paid. I did not wait it out; BL-1554 measured 0 of 50 over 72.6 minutes.
* **The false-cut rate on any surface but this one.** 15 stale accounts is a small arm, and the
  93.3% is [70.2–98.8]. It is measured on `/v2/hashtag/medias/clips` only. `top` and `recent`
  may behave completely differently, and that is exactly the untested variable that made
  BL-1556's 0.16% misleading.
* **Whether `#warrioredit`'s 202 new accounts from 3 addresses is a bad tag or a bad hour.**
  One tag, one walk.
* **`harvest_tag`, which `ig_bio.py`'s own usage line advertises, does not exist.** AST and grep
  agree — one occurrence, in the docstring. `from ig_bio import harvest_tag` is an `ImportError`
  waiting for whoever follows the documentation.
* **Any editor-rate conclusion.** 30 rows, ±12 points.

---

https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/BL-1557-the-walk-that-broke-the-staleness-cut.md
