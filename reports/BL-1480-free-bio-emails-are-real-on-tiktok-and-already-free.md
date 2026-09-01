# BL-1480 — the free bio emails are real, already yours on TikTok, and worth $0.00 on Instagram

> ## IS THE FUNNEL SAFE TO RUN? **YES — nothing was changed.**
> This round measured and shipped no behaviour change. The free-side reader's self-report was
> **confirmed fixed** before any result was trusted. **No vendor call was made: $0.00 of a $0.75
> cap.**
>
> ## AND THE DIRECT ANSWER TO YOUR QUESTION
> **Is it real?** Yes — on TikTok the bio really does carry the address, and the test is not close:
> **96.88%** on 2,756 rows, and where the free read returns anything it is byte-identical to the
> paid address **2,670 times out of 2,670**.
> **Is it worth it? / How much does it save?** **On TikTok you already have it — it is harvested
> today, free, and there is nothing to switch on.** **On Instagram it saves $0.00**, because the
> one paid call that would be removed is the same call that returns the contact button, and the
> bio rides along inside it at no extra charge. **The "50% of paid emails, free" headline does not
> survive: the honest Instagram figure is 30.11%, and it buys nothing.**

---

## 1. Round ID, date, and what it was asked to do

**BL-1480 — 2026-09-01.**

The round was asked to test a specific claim honestly: that the page capture **already extracts
bio email addresses for free**, at **50.0% [29.0, 71.0]** of what the paid call finds, returning
**the same address** — and that **no contact path consumes them**, making it the largest saving
available with no vendor needed.

The instruction was blunt and correct: *"Test it out — if it's actually really beneficial to us,
that he doesn't lie to us, that it's actually true."* Every number behind the claim had already
been retracted or contradicted once, so nothing was to be inherited — all of it re-derived from
raw data. Budget **$0.75**.

**Result: the mechanism is real, the headline number is wrong, and the saving is zero.**

---

## 2. What actually shipped

**No production code was changed.** This was a measurement round, and the measurement said not to
wire anything (§4). What shipped is the verification, the report, and the correction of several
published figures.

| # | Finding | Where | How it was proved |
|---|---|---|---|
| 1 | The free reader's self-report is genuinely fixed | `page_capture.py:279, 285, 309` | Read the logic: the field is set **last, from what was actually extracted**, with three distinct states |
| 2 | Every "empty" record on disk **predates** that fix | — | Dated the files against the fix commit: fix at **08-30 23:37**, all empty records from **08-27/08-28** |
| 3 | The free reader is **not** walled any more | post-fix capture file | **48 of 50** post-fix records carry a real free biography; 3 carry a free address |
| 4 | The address really is in the bio, on TikTok | lead store, n=2,756 | Ran the reader's **exact regex** against the stored bio and compared to the paid address as a hash |
| 5 | One Instagram call returns bio **and** contact field | `config ig_api.field_map` | The map lists `biography` and `email → public_email` in the same response shape |
| 6 | TikTok already ships the additive free-address merge | `tiktok_finder.py:2851` | Read the assignment: paid wins, free fills only an empty |
| 7 | Instagram has **no path** from the free addresses to a lead row | `meme_finder.py:4849` copies free facts but not `emails` | Call-graph trace; the two names never co-occur in the package |

---

## 3. What was measured

Every figure is marked **MEASURED** or **DERIVED**, with a **named denominator** and a **Wilson
95% interval**.

### 3.1 First: is the free reader's self-report trustworthy?

This had to be settled before any free-side result could mean anything. The field that reports
whether the free read worked was once initialised to `"embedded_json"` **as the default value of
its own object literal**, so it reported that the function had been entered, not what it found.

**MEASURED — the fix is real and general.** The field is now assigned **last**, from what was
actually extracted, and distinguishes three states: no script blob at all, a blob with no profile
data (this is the login wall), and a genuine extraction.

**MEASURED — but the data on disk is still the old, untrustworthy kind.** Across **491 free-facts
records** found by walking every JSON file under the output and scratch trees:

| `source` says | records | of which carry no data at all |
|---|---:|---:|
| `embedded_json` | 486 | **436** |
| `shell` / `none` (the new states) | **0** | — |

**Zero records use either new state.** Dating the files against the fix commit settles why: the
fix landed **08-30 23:37**, and every file containing an empty record was written **08-27 or
08-28**. The single post-fix capture file contains **50 records with 0 empties**.

> **So the fix works and the archive is stale.** Any free-side measurement drawn from the older
> records would have been unfalsifiable — which is exactly the trap the round was warned about.
> **A caveat I will not hide: I never observed the new `shell` state on a real walled page**, so
> the fix's behaviour *on a wall* is **NOT MEASURED** — only its behaviour on pages that worked.

### 3.2 Is everything still login-walled? No.

A previous round called the whole question unverifiable because 310 records carried free facts and
the same 310 were walled. **MEASURED: that is no longer true.** In the post-fix capture, **48 of
50 records carry a real free biography** and 3 carry a free address. The free read is working.

### 3.3 The spine — does the free reader return the paid address, character for character?

**The strongest part of the round, and it uses a denominator in the thousands rather than the
handful behind the original [29.0, 71.0] interval.**

The lead store records, for every row, both the address and the **bio text**. So the reader's
**exact regex** can be run against the **exact bio** and the result compared to the address we
already hold. Addresses were hashed the moment they were read; **no address appears anywhere in
this report or in any file this round produced.**

**TIKTOK** — denominator: **2,756** rows holding both a paid address and a bio.

| measure | result | Wilson 95% |
|---|---|---|
| **Coverage** — free read returns an address at all | **2,670 / 2,756 = 96.88%** | [96.16, 97.47] |
| **Exact match** — byte-identical to the paid address | **2,670 / 2,670 = 100.00%** | [99.86, 100.00] |
| **End-to-end** — what a free-only path recovers | **96.88%** | [96.16, 97.47] |
| **Net-new** — addresses the paid column lacks | **0** | — |
| **False positives** — address invented where none exists | **53 / 47,054 = 0.11%** | [0.09, 0.15] |

**INSTAGRAM** — denominator: **93** rows holding both a paid address and a bio.

| measure | result | Wilson 95% |
|---|---|---|
| **Coverage** | **29 / 93 = 31.18%** | [22.67, 41.19] |
| **Exact match** | **28 / 29 = 96.55%** | [82.82, 99.39] |
| **End-to-end** | **28 / 93 = 30.11%** | **[21.73, 40.07]** |
| **Net-new** | **1** row | — |
| **False positives** | **2 / 227 = 0.88%** | [0.24, 3.16] |

> **THE ORIGINAL HEADLINE DOES NOT SURVIVE.** It claimed **50.0% [29.0, 71.0]**. The measured
> Instagram figure is **30.11% [21.73, 40.07]** — near the bottom of that old interval, and the
> new interval **excludes 50%** entirely. The old point estimate was wrong; only its very wide
> error bar contained the truth.
>
> **The false-positive rate is the good news and it was previously unmeasured.** The reader is
> **not** inventing addresses: **0.11%** on 47,054 TikTok rows and **0.88%** on 227 Instagram rows.
> That is the failure mode that would have been worst, and it is essentially absent — the reader
> derives addresses from bio text only, so it has nothing to hallucinate from.

**⚠️ THE LIMIT OF THIS MEASUREMENT, STATED PLAINLY.** It proves the address is **in the bio**. It
does **not** prove the bio was obtainable **free**, because the stored bio may itself have come
from a paid response. **I tried to close that loop and could not: 0 of the 50 post-fix free
captures correspond to any row in the lead store.** So these figures are an **upper bound
conditional on already having the bio** — and §3.4 is what actually decides the money.

### 3.4 Where the addresses really come from

**MEASURED**, denominator = rows carrying an address with a recorded source:

| source | count | share |
|---|---:|---:|
| resolved via the music-catalogue route | 7,425 | 57.5% |
| *(blank)* | 2,891 | 22.4% |
| Instagram **contact button** | 517 | 4.0% |
| Instagram **bio text** | 463 | 3.6% |
| TikTok **bio text** | 112 | 0.9% |

**DERIVED**, denominator = the 980 Instagram addresses with a known source: **52.8% [49.6, 55.9]
come from the contact button** and **47.2% [44.1, 50.4] from bio text**.

**⚠️ AND A LABEL THAT IS EASY TO MISREAD.** `meme_finder.py:3043` assigns the label by checking
whether the **paid** address happens to appear in the bio. So a row marked "bio text" **was still
bought** — the label records where the address *could* have come from, not where it *did*. Nobody
should read those 463 rows as addresses already obtained for free.

---

## 4. What was refused, and why — and the price

**NOTHING WAS WIRED. THE HONEST SAVING IS ZERO, AND THAT IS THE ANSWER, NOT A SHORTFALL.**

**Instagram: $0.00 saved. Calls removed per 1,000 delivered pages: 0.**
One profile call's field map returns **`biography` and `email → public_email` in the same
response**. The bio is therefore **already free inside the call you are already paying for**. A
separately-obtained free bio can only save money if that call disappears entirely — and it cannot,
because it is the only source of the contact button, which supplies **52.8%** of Instagram
addresses. Dropping it would forfeit more than half of them to recover at most **30.11%** of the
rest. **DERIVED:** at the true unit price the call is **$0.69 per 1,000 pages**; that is the price
of the *call*, not of the funnel, and it must not be quoted as either a saving or a total.

**TikTok: nothing to save, because it is already free and already harvested.**
The bio arrives as part of the **discovery response** — `signature` → `author_bio`
(`tiktok_finder.py:249`) → the stored bio (`:2478`) — on a call that fires anyway, and the
address is extracted from it and labelled at `:3013`. **The free bio is not an unclaimed saving on
TikTok; it is the mechanism already in use.**

**⚠️ CORRECTION, MADE AFTER FIRST PUBLICATION AND BEFORE ANYONE ACTED ON IT.** I first wrote that
the free-bio path is "wired on both platforms" and that wiring it would merely duplicate something
that already works. **That is wrong for Instagram, and a traced call-graph proved it.**

**TikTok already ships exactly the additive merge this round was asked to consider**
(`tiktok_finder.py:2851`): the paid address wins, and the free bio address fills in **only when
the paid one is empty**, labelled as having come from the free bio. Its own comment states the
reason plainly — without it, *"a page with a perfectly good address in its free bio would be
delivered as having none — turning a saving into a supply loss."*

**Instagram has no such path at all.** The free addresses are captured, carried into the funnel,
and read twice — but the function that copies free facts forward (`meme_finder.py:4849`) takes the
biography, the captions, the handle, the display name and the post counts, **and never the
`emails` array**. A search for those two names co-occurring anywhere in the package returns
**nothing**. The lead row's address is set only from the **paid** response
(`meme_finder.py:7172-7177` via `:3003-3062`).

**This does not change the price — it changes what the opportunity is.** The saving is still
**$0.00**, because the paid call fires regardless for the contact button. But the honest
description is not "a redundant duplicate"; it is **a possible supply gain on pages where the paid
call returns no address at all** — and **I have not measured that**, because my net-new figure was
computed on rows that already carry an address, which is the wrong denominator for this question.
**That measurement is now the top recommendation in §7, and it is free to run.**

**Also not done, and named rather than skipped:**
- **A fresh paced walk to close the free-vs-paid loop — NOT RUN.** It is the right next experiment
  (§7) but it is a clock cost, and the pricing answer above does not depend on it.
- **The `shell` state on a real wall — NOT MEASURED** (§3.1).
- **Nothing was changed in the deduplication rules.** Its refusals are deliberate: shared inboxes
  are real, and a false merge deletes a person silently.

---

## 5. What I got wrong

**The most useful section, and every item was caught by a control rather than by luck.**

1. **My first record-matcher counted 1,298 records and reported an 88.8% self-report failure rate.**
   It required only the field name `source` plus *any* profile-ish key — so it swept in rows where
   `source` means a **file path**, a **surface name**, or a probe label. **Those are not free-facts
   records and their "disagreement" was my matcher, not the reader.** Retightened to the exact key
   set the JavaScript emits, and the count fell to 491. **The retracted number would have been a
   dramatic and completely false headline.**
2. **My first spine design failed outright, and the assertion is the only reason it produced
   nothing instead of something wrong.** I guessed the join column from five plausible names; all
   five missed, because the column is named for one platform but used for both. The script asserted
   *"no paid addresses parsed — instrument failure, not a finding"* and stopped. **Had I written
   `if not paid: return 0` instead of an assertion, this report would have carried a clean,
   confident zero.**
3. **I published "the free TikTok bio field is NOT read anywhere" and it was false.** My search
   output was truncated at ten lines and never reached the file that reads it — the field **is**
   read, at `tiktok_finder.py:249`. **A truncated search is not a search**, and this inverted the
   entire TikTok conclusion: from "an unclaimed free saving" to "already wired and already
   harvested."
4. **I inherited a claim from my own brief without checking it.** The brief states the configured
   unit price is `$0.000600` and that every Instagram figure is therefore 15.1% low. **The
   Instagram-specific config key already holds the correct `$0.00069064`** — the `$0.0006` belongs
   to a *different vendor's* key, where it is right. The stale price survives in the documentation,
   not the configuration.
5. **I published that the free-bio path was "already wired on both platforms", and it is not.**
   I reached that from two source-label assignments and stopped there. A traced call graph showed
   the Instagram funnel copies free facts forward **without the addresses**, so no free address has
   ever reached an Instagram lead row. **My conclusion on price survives unchanged, but my
   description of what is on the table was wrong** — it is a potential supply gain, not a redundant
   duplicate. Corrected above before anyone acted on it.
6. **The brief said "two doc files"; I found more.** One reference-page line is definitively stale
   for Instagram, and two further pages quote the figure generically in a way that reads as stale.

---

## 6. Money and safety

**Spend: $0.00 — zero vendor calls, by this round's own counter.** Nothing here required a
purchase: the addresses, bios and captures were already on disk. **0.0% of the $0.75 cap.** The
shared ledger is deliberately not used to attribute spend — it has moved while a round made no
calls at all, so a delta cannot attribute anything. **And it did exactly that during this round:
the shared ledger rose by $0.000445 while this round made no call whatsoever.** That is a
concurrent round billing into the same file, and it is the clearest possible demonstration of why
the ledger cannot attribute spend. **This round: 0 calls, $0.00.**

**Integrity, re-verified at publication rather than only at check time:**

| file | result |
|---|---|
| Configuration file | **byte-identical** |
| Campaigns fingerprint | **`8e02f8d6f6307ae8` — unchanged** |
| All four seen stores | **byte-identical** |
| Lead store | **byte-identical** |

**Backups were taken before anything ran, and each copy was verified by re-hashing it** — 7 of 7
matched. This matters more than usual: **the scheduled backup to external storage returns an error
and has not run**, so nothing overwritten here would be recoverable. Nothing was overwritten.

**Processes: nothing was killed.** All four of the operator's servers held the same process IDs
throughout. The watcher that would restart on a source write **is not running** — its state file is
absent — and in any case no file under the application package was written.

**Files another round is actively rewriting were read, not written**, and their versions were
pinned by hash so the line numbers in this report describe a known state.

**Address handling: no address was printed, logged, or written to any file.** Every address was
reduced to a hash on read; only counts and hash comparisons left the measurement scripts. **No
partial address appears either** — truncating to the first two characters is not a redaction, since
for some addresses that *is* the entire local part.

**Secret scan: this file was scanned by reading its bytes**, with **every detector proving itself
on a known positive first**, and the control-byte assertion running **before** publication.
**Result: 0 email addresses, 0 key-shaped literals, 0 wallet-shaped strings, 0 street-shaped
strings, 0 absolute paths containing a username, 0 C0 control bytes.** No creator handles appear
anywhere.

---

## 7. What to do next — ranked, with the arithmetic

**1. Do nothing about the Instagram free bio. It saves $0.00. (Recommended, and it is free to
follow.)**
The call you would remove is the call that fetches the contact button, which supplies **52.8%** of
your Instagram addresses. The bio already arrives inside that same paid response. There is no
version of this that saves money without losing more than half your Instagram addresses.

**2. Know that TikTok already works this way, and stop treating it as an opportunity.**
On TikTok the bio comes free with discovery and the address is extracted from it — **96.88%
coverage, and byte-identical to the paid address 2,670 times out of 2,670**. This is the best
number in the report and it describes something you already own.

**3. Measure the one thing that could still be worth something — and it is free.**
Instagram lead rows that go out **with no address at all**: how many of them have a free bio
address sitting unused? My net-new figure (1 row) was computed on rows that **already** had an
address, which cannot answer this. TikTok already fills that gap and says in its own code comment
that not doing so turns a saving into a **supply loss**. If the count is material, the fix is a
single assignment in a function that already holds both values; if it is near zero, close the item
for good. **Either way it costs no money and settles a question that has been reopened three
times.**

**4. If you want the free-vs-paid loop closed, it costs clock and no money.**
Everything above proves the address is *in* the bio. It does not prove the bio can be obtained
**free** for the pages you care about, because no page with a free capture also appears in your
lead store. **A paced walk over a few dozen pages where you already hold the address** would close
that loop end to end. It needs no vendor call. It is the only measurement that could change the
Instagram answer, and I would expect it to confirm it rather than overturn it.

**5. Fix one stale line of documentation.**
A reference page still prices the Instagram vendor at the old figure, which is **15.1% low**. The
configuration is already correct, so this is a documentation error, not a billing one — but it is
the number a reader would quote.

**6. Treat the "bio text" source label with care in any future analysis.**
It marks addresses that were **bought** and happened to also appear in the bio. Read as "already
free", it would overstate the free yield by roughly 460 rows.

---

## 8. Paths to open

Written with `%USERPROFILE%`, which **File Explorer expands when pasted into its address bar** —
this keeps a username out of a public document while staying directly pasteable.

| What | Path |
|---|---|
| This round's full working report | `%USERPROFILE%\OneDrive\Desktop\clipper finder\reports\BL-1480.md` |
| The self-report census (§3.1) | `%USERPROFILE%\OneDrive\Desktop\clipper finder\scratch\bl1480_census.py` |
| The spine measurement (§3.3) | `%USERPROFILE%\OneDrive\Desktop\clipper finder\scratch\bl1480_spine.py` |
| Its results — counts only, no addresses | `%USERPROFILE%\OneDrive\Desktop\clipper finder\scratch\bl1480_spine.json` |
| The free-side reader under test | `%USERPROFILE%\OneDrive\Desktop\clipper finder\clippershq\page_capture.py` |
| Where TikTok reads the bio (line 249) | `%USERPROFILE%\OneDrive\Desktop\clipper finder\clippershq\tiktok_finder.py` |
| Where the Instagram source label is set (line 3043) | `%USERPROFILE%\OneDrive\Desktop\clipper finder\clippershq\meme_finder.py` |
| The free bio→email extractor | `%USERPROFILE%\OneDrive\Desktop\clipper finder\clippershq\bio_parser.py` |

**No port numbers are given deliberately** — they are not stable between runs, and a grading
session was once lost to a bookmarked one. Start the sheet server from its own launcher and use
the port it prints at the time.

---

*Round BL-1480 closed 2026-09-01. Claim tested, mechanism confirmed real, headline figure
corrected from 50.0% to 30.11% on Instagram, saving measured at $0.00, nothing wired. Zero vendor
calls against a $0.75 cap.*
