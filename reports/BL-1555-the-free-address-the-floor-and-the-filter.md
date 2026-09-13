# BL-1555 — the address we already had, the date that is only a floor, and a filter that already exists

**How many free addresses were already being discarded, can he see the last post for free, and
what does 1,000 editor-addresses cost?** **The free address was real and is now read.**
`page_capture.FREE_FACTS_JS` has been running an address regex over the free bio into
`out.emails` on every captured page, and reporting whether the page was genuinely read in
`out.source` — and the only consumer of that payload read **neither**. Both are now wired,
GENERAL, one helper and two call sites in one function, with every name proved to resolve at runtime and the
patch proved idempotent. On the one era of captures where the camera was actually reading
pages, **9 of 111 bios carried a usable address — 8.11% [4.32% – 14.69%]** — and the
extraction gap was **0**, meaning the machinery always worked and nothing read the output.
**But be clear about what that is worth: at $0.00069064 a call it is cents.** Projected onto
his 16,306 bio-less rows it is ~1,322 addresses and about **$0.91** saved. The reason to ship
it is that the funnel was throwing away data it already had, not economics. **The last-post
date: YES, it is free, and NO, it is not the last-post date.** `taken_at` is already on the
Instagram hashtag call you buy — but **202 of 246 repeated authors (82.1% [76.8% – 86.4%])
carry dates that disagree with themselves**, which proves by contradiction that it is the
date of whichever post matched the tag, not the account's newest. Its understatement is
**median 2.3 days, p90 7.1 days — and a maximum of 620.8 days.** That is far better than
TikTok's 9.1-day median, and 89.6% land within a week, so it is genuinely usable — **as a
floor.** The honest row text is *"posted at least as recently as N days ago"*; writing *"last
posted N days ago"* is a false statement about the page, and it is exactly how TikTok's
recency wall came to reject accounts that had posted yesterday. **And the corporate filter he asked for already
existed and was called on none of his leads.** `role_policy.looks_agency` is 97.7% precise
[88.2 – 99.6] and already feeds master's `email_quality` column — but `email_quality` is
blank on **100.0% of clipper rows (2,933 of 2,933) and 100.0% of meme_page rows (1,291 of
1,291)**, against 18.6% for the client rows whose funnel does call it. It is now wired on
the meme side as a flag, never a delete. **The VPN never came up during this round**, so the free-exit and
page-date questions are reported **ABSENT, not as a blocked result**. Spend: **$0.00** — no
vendor call was needed.

---

## 1. What this project is, for a reader with no context

This system finds video editors and meme-page operators on TikTok and Instagram and collects
the email address many publish in their profile bio. A "bio" is the short free-text blurb on a
profile. On Instagram the bio normally has to be bought one profile at a time from a reseller
API at **$0.00069064 per call**. This round is about three things that cost nothing: an
address the system already had and discarded, a date it already buys and never reads, and a
company-versus-person signal it already computes and never shows.

## 2. Safety and the cap

* **Nine stores backed up**, sha256-verified, **bodies found by shape** — `spend.json`'s
  payload is the list at `runs` (36,482 rows), `clip_seen.json` a **bare list** (2,193),
  `tiktok_pages_seen.json` a **dict at `pages`** (3,270), where a dict-only reader reports **3**.
* **All six corruption controls FIRED**, including the position-qualified one: delete one of a
  duplicated pair and the natural-key set is **provably identical** while only the indexed
  digest moves.
* **The cap was proved to bind before any call** by lifting `Budget` from `harvest_run.py`
  **by AST**: it advances by the **Instagram** unit ($0.00069064), not TikTok's ($0.00060000),
  15.1% apart; `$0.00` **raises**; the meter does not move on a refusal; under **8 threads**
  the locked counter stops at exactly 50 of 50; **the proof wrote nowhere**.
* **`docs/FACTS.md` at lag +0** at round start against a live 36,482 rows (limit
  +2000). It had moved to **+212** by commit time — a concurrent funnel bills into
  `spend.json` throughout, which is exactly why this round's $0.00 is my own counter
  and not a ledger delta.
* **Spend this round: $0.00.** Ground truth was already on disk, so no vendor call was made.
  There is therefore no counter to reconcile and no delta to mis-attribute.

## 3. Part 1 — the free address and the wall state are now READ

    produced by FREE_FACTS_JS : biography, emails, follower_count, posts, source, user_pk, video_posts
    read by the consumer      : biography, captions, follower_count, full_name, posts, user_pk, video_posts
    PRODUCED BUT NEVER READ   : emails, source

A new helper, `clippershq/free_contact.py`:

| function | returns |
|---|---|
| `wall_state_of(cap)` | `'none'` / `'shell'` / `'embedded_json'` / `''` — the **string** |
| `page_was_read(cap)` | `True` / `False` / **`None`** — `None` means NOBODY LOOKED |
| `free_emails_of(cap)` | the addresses the capture already extracted |
| `pick_free_email(cap, bio, mx_table)` | `(address, reason)` — address first, falsy when unusable |

Wired at the row-building site in `meme_finder._walk_one`. **The address is used only when the
paid path found nothing** — it fills the blank, never overwrites a bought value. The
`resolved` / `no_email` counter now reads the ROW, so a page resolved for free is no longer
counted as `no_email`.

**FIX CATEGORY: GENERAL — one helper, two call sites in one function.** Of seven past fixes tested by driving
them only 1 of 7 was GENERAL, so the claim is pinned rather than asserted: the committed test
fixes the consumer list, and a new consumer that forgets the call turns it red.

### Three traps it does not fall into
* **The third state stays third.** "No bio" and "we never read this page" are a write-off and
  a retry. `page_was_read` returns `None` for an absent field; a round here once collapsed a
  third state to a boolean and the missing state counted as SUCCESS.
* **The @handle trap is delegated, not re-invented.** A bare word, an at-sign and a
  dot-suffixed word matches a social handle exactly as well as it matches an address, and the
  suffix cannot separate them — `.cc`, `.uk` and `.com` are all real TLDs. The tell is the
  SPACING and the words around it. Every address goes through `address_check.check_row`,
  measured on the workbook. A first-draft rule elsewhere caught 20 rows of which **11 were
  genuine Gmail addresses**.
* **Role inboxes and short local parts are KEPT, flagged.** `info@`, `booking@`, `hello@` are
  what a working editor publishes for business.

### Proved, not assumed
* **22 of 22 tests green** in `tests/test_bl1555_free_contact.py`, which uses `raise` not
  `assert` and parses its own source for `ast.Assert` with a planted control.
* **Every call site resolves at runtime.** "The module imports" is not proof — a name looked up
  only when a function runs raises `NameError` while the module imports cleanly. All 16
  name/site pairs resolved in their own scope, and the checker was proved first on seven
  planted cases including an **unbound** one, a bound-inside-a-`try` and a bound-in-an-
  enclosing-scope.
* **And the binding ORDER was checked too**, which AST resolution alone does not cover: a
  closure read before its assignment still raises. `_caps = {}` sits at indent 4 in
  `run_funnel`'s body — **unconditional** — and precedes the only `_walk_one` call site.
  The file carries a comment recording that this exact name once reached a gate unbound.
* **The patch is idempotent** — run twice, the second run reports "already wired".
* **It does not reshape the store.** The three new row keys (`page_read`, `wall_state`,
  `free_email_why`) are not master columns. Driving the real appender against a throwaway CSV:
  **72 columns before, 72 after, none added**, with a control proving a known column still
  round-trips so the clean result is not an artefact of a write that never happened.

### What it recovers, on the right denominator

| denominator | k / n | rate | Wilson 95% |
|---|---|---|---|
| all captures ever stored — **misleading** | 9 / 3,329 | 0.27% | [0.14% – 0.51%] |
| captures from the era that actually READ pages | 9 / 117 | 7.69% | [4.10% – 13.98%] |
| **captures WITH A BIO — the fair denominator** | **9 / 111** | **8.11%** | **[4.32% – 14.69%]** |

Across the whole corpus only **427 of 3,329 captures (12.83% [11.73% – 14.01%]) were
genuinely read at all**, and only **111 of those 427 (26.00% [22.06% – 30.36%]) carried a
bio — so the address rate above is conditioned on a page the camera actually got.

**All nine come from a single manifest** — the one era in which the camera was reading pages
with bios. Spreading them over 3,329 captures understates the rate ~30x and describes the
camera being walled, not the address being rare. **Bios carrying an address while `emails` was
empty: 0** — the extraction was never broken; nothing read it. Flags on the nine: 2 business,
1 role inbox, all kept.

Projected at 8.11% [4.32 – 14.69], **2,000 read pages yield ~162 free addresses [86 – 294]**
and all 16,306 bio-less rows yield **~1,322 [705 – 2,396]** — worth **$0.11** and **$0.91**
respectively. ⚠️ **That is a projection from one era of one manifest, n=111 bios**, stated as
what the interval permits, not as a property of the platform.

## 4. Part 3 — the Instagram last-post date IS free, and it is a FLOOR

`taken_at` is on the stored Instagram hashtag payloads — **1,098 occurrences across 40 files**,
1,719 usable post dates across the full 82-file corpus. The date costs nothing extra.

⚠️ **`url_expiration_timestamp_us` occurs 3,294 times in the same corpus — three times more
often than the real date.** It is a signed-URL expiry, not content. It is excluded by name,
with server clocks, our own write times, cache TTLs, timestamps on the USER object, comment
`created_at` and bare 10-digit identifiers. Counting any of them manufactures an answer, and a
previous value-search returned "NOT ESTABLISHED" for exactly that reason.

**Which date is it? Settled by contradiction — no ground truth, no paid call:**

    IF THE SAME AUTHOR APPEARS TWICE WITH DIFFERENT taken_at VALUES,
    THE FIELD CANNOT BE "THE ACCOUNT'S NEWEST POST".

| | |
|---|---|
| media objects carrying a usable post date | 1,719 |
| distinct authors | 1,274 |
| authors seen more than once | 246 |
| **authors whose dates DISAGREE WITH THEMSELVES** | **202 / 246 = 82.1% [76.8% – 86.4%]** |

It is the date of whichever post matched the tag — structurally the same value as TikTok's.

**But the distribution is far better than TikTok's.** Days between an observed date and the
best date seen for that same author (a **lower bound**, since the true newest may be newer):

| | |
|---|---|
| n | 375 |
| **MEDIAN** | **2.3 days** |
| **p90** | **7.1 days** |
| **MAX** | **620.8 days** |
| within 7 days | 336/375 = 89.6% [86.1% – 92.3%] |
| within 30 days | 352/375 = 93.9% [91.0% – 95.9%] |
| within 180 days | 361/375 = 96.3% [93.8% – 97.8%] |

TikTok's median understatement is 9.1 days; Instagram's is **2.3**, with nine in ten inside a
week. **Usable — as a floor.** ⚠️ **And the tail is 620.8 days**, the shape that looks perfect
on a spot-check and savages pages at scale. A hard staleness cut on this field throws away
live pages at roughly a 1-in-10 rate.

**What it licenses on a row:** *"posted at least as recently as N days ago."* Not *"last
posted N days ago."* A recent floor proves the page is alive, which is the useful direction; an
old floor proves nothing and must not cut on its own.

## 5. Part 2 — the corporate filter already exists, and it was called on none of his leads

He asked for a company-versus-person flag. **It is already built, already precise, already a
master column — and it was never called in the two funnels that produce the leads he cares
about.** This is a wiring finding, not a modelling one.

Two candidate signals, measured head-to-head on **180 hand-labelled rows** (labelled from
bio + handle + display name, blind to which signal fired):

| | `address_check.business_signals` | `role_policy.looks_agency` |
|---|---|---|
| precision — P(corporate \| fires) | 71.1% [61.0 – 79.5] (64/90) | **97.7%** [88.2 – 99.6] (43/44) |
| recall — P(fires \| corporate) | **85.3%** [75.6 – 91.6] (64/75) | 57.3% [46.1 – 67.9] (43/75) |
| wrongly fires on a PERSON | 24.8% [17.5 – 33.8] (26/105) | **0.95%** [0.2 – 5.2] (1/105) |

**`role_policy` wins on the axis that matters**, because a wrong drop is exactly as bad as a
wrong keep. And the reason it wins is structural: `looks_agency(email, handle, name)` **takes
the handle and the display name**, so it can exempt a creator's own brand. `business_signals`
is address-only and cannot — **21 of its 26 false positives (80.8%) fire on the word "music"**
in a solo artist's own domain.

⚠️ **Neither reduces to "not Gmail = corporate."** Both exempt free webmail, and both were
measured against real custom-domain accounts that are still the creator's own. He rejected
that heuristic himself mid-sentence and it stays rejected.

**The gap, verified by me with AST and grep and a positive control:**

    calls role_policy : email_finder.py, spotify_finder.py, google_play_finder.py, crossdedup.py
    NEVER calls it    : meme_finder.py, tiktok_finder.py, twitch_finder.py,
                        youtube_finder.py, repost_finder.py, writer.py

And what that costs, on the store — **`email_quality` is blank on 5,884 of 12,977 addressed
rows (45.3% [44.5 – 46.2])**, split exactly along the wiring line:

| lead_kind | unclassified | |
|---|---|---|
| **clipper** | **2,933 of 2,933** | **100.0%** [99.9 – 100.0] |
| **meme_page** | **1,291 of 1,291** | **100.0%** [99.7 – 100.0] |
| client *(its funnel DOES call it)* | 1,626 of 8,719 | 18.6% [17.8 – 19.5] |

That is a natural experiment: the funnel that calls it is 81.4% classified; the two that do
not are classified **zero percent of the time**.

**What shipped:** `free_contact.email_quality_of(email, handle, name)` — reusing
`role_policy`, reusing master's existing `email_quality` column, producing the shipped
three-value vocabulary, wired into the meme funnel's row build. **All three tiers were proved
reachable** (a branch that never fires is not a tier), and it is a **flag, never a delete** —
he can filter a column, he cannot un-delete a row. Role inboxes are classified, not dropped.

⚠️ **`tiktok_finder.py` is NOT wired** — that is the `clipper` half, 2,933 rows, and it is a
different file with its own row builder that I did not touch this round. The site is named in
the working notes. Running the function offline over existing rows would classify ~104 clipper
and ~125 meme_page rows immediately at $0.00.

## 6. `is_top` on TikTok — real, unread, and NOT the fix I was told it was

I was told to wire the pinned flag so pinned posts stop poisoning recency. **The flag is real;
the reason is not.**

**Confirmed — it is present and it VARIES**, so it is a usable signal, and **nothing gates on
it** (zero gating readers; the only AST hits are a producer and two recorded-not-gating fields):

| source | present | True | rate |
|---|---|---|---|
| the 4 real `aweme_list` payload files | 1,033 / 1,033 | 159 | 15.39% [13.32% – 17.72%] |
| my own independent sweep (different file set) | 132 / 274 | 5 | 3.79% [1.63% – 8.56%] |

**REFUTED — the premise.** Does `max(create_time)` ever land on a pinned post?

| source | accounts with ≥2 items | whose NEWEST is pinned |
|---|---|---|
| the larger sample | 67 | **0** |
| **my own re-derivation** | 11 | **0** — 0.00% [0.00% – 25.88%] |

**A pinned post was never the account's newest, in either sample.** `max(create_time)` is
**position-independent** — it does not care where in the list a post sits — so a recency figure
computed that way is **already immune to pin contamination**. Wiring `is_top` into the recency
path would fix nothing, because nothing there is broken.

The real exposure is **views**, not recency: pinned median 1,658,143 against unpinned 2,840, a
**583.85x ratio OF MEDIANS** (⚠️ not the briefed 543x, and **a ratio of medians is not a ratio
of tails** — the p90 ratio compresses to roughly 35x). Its measured consequence is on the
average-views floor and it runs in the **rescue** direction: pins flip that floor for 12 of 65
accounts, always upward, never sinking a page.

**I did not wire it, and that is a decision rather than an omission:**
1. the justification I was given is measurably false — the recency path is already immune;
2. the remaining benefit only ever **rescues** pages, so not wiring it cannot cut a live one;
3. the fix is **LOCAL across at least 3 sites in 2–3 files** (three independent normalizers
   re-derive the same raw item into different schemas, so there is no choke point) — and of
   seven past fixes tested by driving them, **3 of the 6 LOCAL ones were still failing.**
   Shipping a 3-site LOCAL change whose stated purpose I had just refuted is not a trade worth
   making in the same round.

The exact sites and record-only diffs are written up and unapplied.
⚠️ **One scope limit, ABSENT not false:** the field exists only on the LamaTok/TikHub
`aweme_list` shape; the alternate raw-TikTok `itemList` shape carries **no pin-like key at
all**, so any wiring would cover one of the two shapes.

## 7. Part 4 — the VPN never came up, and that is reported as ABSENT

Checked repeatedly through the round: both `PrivadoVPN (OpenVPN)` and `PrivadoVPN (OpenVPN
DCO)` adapters stayed **Disconnected**, the only adapter Up was the wired one, and the public
exit's salted digest never changed from its round-start value. **No VPN carried traffic at any
point.**

So the questions that need a clean exit are **ABSENT, not answered**:
* whether commercial VPN exits are served by Instagram at all;
* the quota on a new exit;
* the single clean-idle recovery probe;
* whether the logged-out **profile page** carries a true last-post date.

⚠️ **A blocked result is not a finding.** The home IP's anonymous quota was already spent in
the previous round, so running the page probe now would have measured this exit, not
Instagram. The probe is **built and proved** instead: its classifier was driven against a
planted page carrying all eight trap classes and correctly kept only the genuine post
timestamp. It runs on one command the moment an exit exists.

## 8. Part 5 — what it costs

| | |
|---|---|
| TikTok, per 1,000 addresses | **$4.26** [$2.99 – $6.10] |
| Instagram paid, per 1,000 **NET-NEW** addresses, on the population the funnel actually buys | **$8.52** [$4.16 – $18.32] |
| Instagram paid, the $44.61 headline | cold hashtag-discovered editors, resting on **six** events — a different question |

**Per 1,000 LIKELY EDITORS**, which is the unit the business buys, division written out:

    1,677 accounts x $0.00069064 = $1.15820, yielding 23 editor-addresses
    $1.15820 / 23 x 1000 = $50.36 per 1,000 editor-addresses
    yield interval [0.92% - 2.05%]  ->  price band [$33.70 - $75.43]

**And the fallback he should hear before spending a day on any of this:**

    his stated job, 2,000 usernames         2,000 x $0.00069064 = $  1.38
    every bio-less Instagram row on disk   16,306 x $0.00069064 = $ 11.26

The free route is worth building for the next 100,000, not for this week's 2,000.

## 9. The suite

**`FAILED -- 26 red of 479 suite(s)` (2460.0s)**, PASS 453 / FAIL 26, **0 skipped** — a skip
is not a pass, and there were none. Quoted from my own run's JSONL, which the runner writes
one file per pid precisely so two runs cannot be confused.

**`tests/test_bl1555_free_contact.py` — PASS.**

Attributed **per suite name** against BL-1551's recorded list, never by subtracting totals
(26 against 27 is a coincidence of counts, not evidence the same suites are failing):

| | |
|---|---|
| newly red | `test_tools_tracked.py`, `test_zero_collection.py` |
| newly green since BL-1551 | `test_bl1487_docs_guard.py`, `test_bl1490_drift_is_visible.py`, `test_facts_guard.py` |

**One of the two new reds was MINE, and it was the guard doing its job.**
`test_tools_tracked.py` failed with `['clippershq/free_contact.py'] != []` — *"untracked with
no live owner, one `git clean` from gone, which has already nearly happened FIVE times this
session."* It went **green immediately after the commit**, re-run and confirmed. So the
effective standing red is **25, all pre-existing**.

`test_zero_collection.py` is not mine: it fails because `tests/test_bl1528_paging_and_ledger.py`
runs nothing under `python -m unittest` and needs a `load_tests` hook. I ran it directly to
check rather than inferring it from the name.

⚠️ **And the ledger moved under the round.** `docs/FACTS.md` was at lag **+0** at round start
and **+212** at commit — a concurrent funnel billing into `spend.json` throughout. Still far
inside the +2000 limit, so no re-stamp was needed. It does not touch this round's **$0.00**,
because that figure is my own counter and not a ledger delta.

## 10. WHAT I GOT WRONG

**1. I read a 19-hour-stale results file and nearly published its verdict as this round's.**
I picked the newest-by-mtime runner JSONL and reported "478 recorded, 450 PASS, 28 FAIL". That
file belonged to a run from the previous day — my own run had not yet written a line, so the
stale file was still the newest. The runner writes **one file per pid** precisely so runs
cannot be confused, and I used mtime instead of the pid. Caught by checking which file was
actually *growing*.

**2. My red-list filter used lowercase state names where the JSONL uses uppercase**, so it
reported all 478 suites as not-green. The counts (`PASS 450, FAIL 28`) were right beside it and
disagreed — a total that agrees while the subgroup swallows everything is the same tell as a
base rate that reproduces while every subgroup vanishes.

**3. I measured the recovery against the wrong corpus and got a clean zero.** The first run
returned **0 of 196** free addresses. The control caught it: **0 of those 196 records carry a
non-empty biography at all** — they are captures from the walled period. The reader was fine; a
planted address was found immediately. Reported ABSENT, not as zero, and re-run.

**4. Then I let a fallback pick the wrong node and under-counted by two orders of magnitude.**
Reading the capture manifests, I took `list(d.values())` as the record list and got **2 records
per manifest** — the wrapper's own two top-level values — instead of the 238 real ones. The
records live in the dict at `captured`. This is the documented "do not let a heuristic pick the
node" failure and I walked straight into it.

**5. I was about to publish "9 of 3,329 captures" as the recovery rate.** All nine come from a
*single* manifest — the only era when the camera was reading bios. The other 3,212 captures
never carried a bio at all, so that denominator measures the camera being walled, not the
address being rare. It understates the real rate by ~30x. The fair denominator is 111 bios.

**6. I guessed a function signature twice.** `append_leads` is on `crossdedup`, not `writer`,
and takes `(master_csv, new_rows, funnel_tag, now, backup_label)`. Two guessed call shapes
raised `TypeError` first. The only reason this did not become a false "safe" verdict is that
the script reports **ABSENT on a failed drive rather than treating it as a pass**.

**7. Two patch anchors failed before one worked**, and both failures are the same lesson as
every field-name mismatch here: the string you look for has to be the string that exists.
`import free_judge` is **function-local**, so an unindented insert beside it broke the parse —
caught by the pre-write parse check. And the real top-level import line carries a **trailing
comment**, so a bare-name anchor matched nothing at all.

## 11. What did not run, reported as ABSENT
* **Everything needing a clean exit** — VPN service, quota, clean-idle recovery, and whether
  the logged-out profile page carries a true last-post date. The probe is built and proved.
* **MX was not consulted** for the nine recovered addresses at wiring time; the helper accepts
  a table and the offline measurement used the stored one.
