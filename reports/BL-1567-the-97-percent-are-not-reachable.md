# BL-1567 — the other 97% are not reachable, and 3.4% is what the platform publishes

**Round:** BL-1567 · **Unit:** `api.cost_per_call_usd` = $0.00060000, TikTok, by named key
(never `ig_api`'s $0.00069064) · **Spent: $0.00000 of a $0.50 cap**

## The paragraph

**3.4% is the real ceiling, and there is no cheaper way round it.** Four routes to the other
97% were measured against the one that works today — **$2.48 per 1,000 net-new at p≤30** — and
**every one loses.** The @mention chase needs **24.19%** of
resolved pointers to pay for itself and the best yield this project has ever measured is
**6.47%**, so it is **3.7x short before
a single call is bought** — refused on arithmetic, $0.00 spent. The link chase on TikTok
reaches **1.272%** of bios. The extractor is not missing a class of
format: hand-adjudicated, the absolute best case is **27 addresses out of
47,023**, or **0.057%**. And his geography hunch is
**refuted in the direction he proposed** — the apparent 8.8x language effect was **my own
classifier reading the answer**, and it collapsed when repaired. **The whole round cost
$0.00: every figure here is arithmetic on bios this project had already bought.**

⚠️ **The one thing that is NOT refuted is the thing nobody has tried.** 13,007 addresses have
been collected and **not one has ever been contacted.** Every rate in this report is a proxy
for a value nobody has measured.

## 1. What this project is, for a reader with no context

It finds video editors on TikTok who put an email address in their bio. A paid vendor API
returns hashtag pages; each page carries up to 30 posts and the author's bio rides along
**free**. A dedup guard refuses accounts and addresses already held. One call = one page =
$0.00060000.

The operator's question this round: *30 pages returns ~500 videos and ~208 people never seen
before, and only 5 publish an address. When I scroll I see more than that — are we failing to
read some bios?* **The bio is free and all 208 are read. The ceiling is publication, not
access** — and this round set out to find out whether the other 97% are reachable at all.

## 2. Safety, money, and the cap

Ten stores backed up sha256-verified, bodies found **by shape**, and **all six numbered
corruption controls fired** — counted by matching the NUMBERED lines, because `controls()` also
prints a warning and a summary and a naive print-site count answers 8.

**The cap was driven before the first call** (`Budget` lifted from `harvest_run.py` by AST):
funded allows and the meter advances, **$0.00 raises**, the meter does not advance on a
refusal, 3 funded calls allow 3 and refuse the 4th, and **the proof wrote nowhere**
(`stores_unchanged` = True). **In the end no call was made at all: this
round spent $0.00000, so the cap was never the thing that stopped it.**

### 2a. The suites, quoted per name — including 29 reds I did not chase to their origin

`tests/run_all.py` took ~48 minutes and landed: **453 PASS, 29 FAIL, 10,345 checks**, plus
**18 suites that did not run at all** — and the runner is explicit that *"a skip is NOT a pass
and is NOT counted in the 10,345 checks above."*

⚠️ **29 REDS IS NOT ONE PRE-EXISTING RED, AND I AM NOT GOING TO PRETEND I PROVED THEY ARE ALL
INNOCENT.** What I did establish:

* **Zero of the 29 failing suites reference any symbol this round added or changed** —
  `vendor_anomalies`, `_emit_vendor_anomalies`, `unclassified_rule`, `effective_run_cap`,
  `JUDGE_RULES_NEEDING_PROFILE`. Checked by reading all 29 files.
* **Four were opened and traced to unrelated causes**: `test_atomic_io` names
  `clippershq/proxy_pool.py:290` (a file this round never touched); `test_bl1359_ig_cost_fixes`
  wants `stats["judge_batches_pages"]`; `test_bl1516_paid_call_ordering` reports
  *"0 UNEXPECTED"* reds and fails on a census mismatch (10 expected-red tests are now green);
  `test_bl1529_post_floor` fails because 4 of its tests are **defined after the `__main__`
  guard and never bind**.
* **The runner itself says the tree was moving**: *"16 round(s) in flight at 22:45 — a suite
  count is a moment, not a property."*

**What I did NOT do is run the suite at the commit before mine and diff the failure sets.** That
is the only thing that would settle it, and without it "pre-existing" is an inference, not a
measurement. **It is stated here as an inference.**

What *is* measured is the targeted set covering every file this round changed, each by name:

| suite | verdict |
|---|---|
| `test_bl1487_zero_cap` | **OK** |
| `test_bl1443_lifetime_cap` | **OK** (10 tests) |
| `test_cap_reserve` | **OK** |
| `test_bio_parser_backtrack` | **OK** |
| `test_bl1541_email_harvester` | **OK** |
| `test_bl1567_zero_cap_and_dead_counters` | **OK** (14 tests, and **OK under `-O`** too) |

All five changed modules import cleanly.

**And a skip is not a pass.** 18 suites did not run; they are excluded from the 10,345 checks
by the runner's own rule and are excluded from any claim here.

**`spend.json` was snapshotted around the suites: 38,639 rows / $72.882000 before, and
38,639 rows / $72.882000 after — a delta of +0 rows and $0.000000.** The suite that once booked
+212 rows nobody spent stays fixed.

⚠️ **One honest correction about my own backup.** I added `master_leads.csv` as an
"eleventh artefact this round modifies", on the principle that a store you are about to write
is the one you cannot afford to leave out. **It was already in the nine.** The extra copy
verified clean and changed nothing; reported rather than presented as a catch.

## 3. Part 1 — is the extractor missing addresses? No, and the control says so

**THE INSTRUMENT WAS VALIDATED BEFORE IT WAS BELIEVED.** Run the shipped
`bio_parser.extract_emails` over the 3,063 TikTok rows that already carry a stored
address: it re-finds **2,968 of 3,063 (96.90%)**.

Of the **95** it missed, **93 of the 95 inspected are not in the bio
text at all** — they were found via a biolink or another funnel and stored on the row. So the
extractor's true miss rate on bios that actually contain an address is **2 in
95**, and a raw "3.16% miss" would have been a false alarm.

**There is then a 100% zero, and it is a real one.** Across all **47,023** address-free
TikTok bios, the extractor finds an address on **0**. A
100% zero is an instrument failure until a control says otherwise — here the control above is
that proof: the same extractor finds 96.90% of stored
addresses, so the zero means the pipeline applies it **consistently**, not that it is broken.

### 3a. What the filters removed, and which rule did it

183 address-free bios contained something the regexes matched and
the filters then removed. `valid_email()` has nine independent rejection rules; attributing the
drop to the rule that actually fired is the whole question, because **eight of the nine cannot
drop a genuine address** (punctuation-only local parts, `www.` prefixes, known bouncing typos)
and **one can**:

| rule that fired | addresses |
|---|---|
| KNOWN FREE-MAIL TYPO (would bounce) | 2 |
| TLD NOT IN _GOOD_TLDS ALLOWLIST ⚠️ | 160 |
| domain label count/empty label | 1 |
| local has .. | 1 |
| local has scraped leading/trailing punctuation | 10 |
| local is punctuation only | 11 |

**So the question reduces to the TLD allowlist**, and a TLD is decidable without looking at
anybody's address: it either is or is not delegated in the IANA root.
**182 addresses across 148 distinct TLDs**, and
the split is not close:

* **174 are at TLDs that do not exist** — `.aep` (an After
  Effects *project file*), `.editz`, `.vfx`, `.logoless`, `.audios`, `.gif`. These are
  filenames and jargon glued onto a word. **The allowlist is doing exactly its job.**
* **8 are at delegated gTLDs** — `.digital`, `.management`,
  `.films`, `.network`, `.team`. These could be real.

⚠️ **AND MY OWN ADJUDICATION LIST WAS WRONG IN THE OTHER DIRECTION.** It called
`.la`, `.mp`, `.va` and `.tt` junk; all four are delegated ccTLDs. That is
**8 more addresses** that my
instrument, not the data, classified as dead. Counted here rather than left implied — though
`.tt` and `.mp` in an editor's bio are far more likely to be "tiktok" and "mp4" than Trinidad
and the Northern Marianas.

A separate shape: **11 bios name a mail provider
after a real `@` and produce nothing**, all of them the same form — a provider with **no TLD**
(`<local>@gmail`), which is mechanically repairable and which a human reading the bio would
absolutely count.

**THE TOTAL, AT ITS MOST GENEROUS: 27 addresses out of 47,023 address-free bios
— 0.057%.** Against the 3,063 TikTok addresses already
stored, recovering every single one would be **+0.9%**. It is
worth the ten-minute change; **it is not a route to the 97%, and it is not why he sees more by
eye.**

## 4. Part 2 — the @mention chase, priced and refused on arithmetic

**The prerequisite was measured on bios already bought, before anything was built.**

| | count | share of address-free bios |
|---|---|---|
| carries an `@` pointer at all | 8,125 | 17.28% |
| points at a **different** account | 7,518 | 15.99% |
| …an Instagram cue or URL | 1,476 | |
| …a bare `@handle` (TikTok-shaped) | 7,117 | |
| cued as the person's **own** account | 2,132 | |
| cued as a **credit/collab/repost** | 950 | |
| no cue either way | 5,043 | |

**The mechanism is real and cheap to state.** One pointer resolves through
`api_client.user_by_username()` → `GET /v1/user/by/username`, which is **one billed call** at
$0.00060000. Nothing about that is in doubt. The only question is whether the yield can pay:

| assumed yield | $ per 1,000 net-new | basis |
|---|---|---|
| 6.470% | $9.27 | master in-bio rate, ALL tiktok bios (the STORE -- generous, the store is enriched) |
| 3.274% | $18.33 | a fresh walk at p<=30 (BL-1566, the honest comparator) |
| 0.795% | $75.47 | BL-1564's 17-tag walk |

**And the decisive form of the sum does not depend on how many pointers exist.** Cost per
1,000 = ($ per call × 1000) ÷ yield, so the break-even yield can be solved directly:

* to match **$2.48** per 1,000 (p≤30) the chase needs **24.19%** of resolved pointers to pay;
* to match **$3.92** (full depth), **15.31%**;
* the same sum on Instagram ($0.00069064) needs **27.85%**.

**The best yield this project has ever measured is 6.47%**,
and that one is the *store*, which is enriched. **REFUSED ON ARITHMETIC — 3.7x
short before a single call, and no probe can rescue it**: a probe can only measure the yield,
and a yield at the top of everything ever observed still loses. Chasing the
7,518 pointers already in stock would cost
**$4.51**. $0.00 was spent.

⚠️ **This is a different question from the cross-platform join, which is separately refuted**
(0 of 55,628 and 0 of 17,045, four positive controls passing). That joined two stores; this
follows a pointer. The refusal here is on price, not on mechanism.

## 5. Part 3 — the link chase on TikTok, and a prior that does not hold here

The earlier numbers were **Instagram**. On **TikTok**, over 50,086 bios:

| | count | rate | Instagram prior |
|---|---|---|---|
| carries a link in the bio **text** | 677 | 1.352% [1.254–1.457] | 7.19% |
| link **and no email** — the actual prize | 637 | 1.272% [1.177–1.374] | 1.05% [0.66–1.68] |

**The prize replicates: ~1%, overlapping the Instagram prior.** The brief's condition is met,
so **the link chase is closed.**

⚠️ **But one prior is CORRECTED, and the next round must not re-open the chase on it.** The
claim "0 of 116 were link-aggregators" **does not hold on TikTok**:
**96 of 677 linked rows
(14.18% [11.75–17.01])
are aggregators** — `linktr.ee` on 76 rows, `linktree` on 33, `guns.lol` on 22, `carrd.co` on
19. The old zero was **n=116 on a different platform**. It does not change the verdict —
1.272% of bios is the ceiling on the whole chase however good the
pages are — but "aggregators do not exist here" is now false and should not be quoted again.

**And the two things called "a link" are not the same thing.** This is the bio **text**, which
is free. TikTok's dedicated `bioLink` **field** is paid-only and was separately measured at 1
address in 60. That is a different question at a different price and was not re-measured.

## 6. Part 4 — his geography hunch, refuted in the direction he proposed

**THE FIRST ANSWER WAS WRONG AND MY OWN POSITIVE CONTROL CAUGHT IT.** The first pass reported
Latin/other-language bios carrying an address **34.95%** of the time against English **3.98%** —
8.8x, and *opposite* to his hunch. The control printed the tokens driving each bucket, and the
top token for "other-latin" was **`com`** — Portuguese for "with", **and the tail of every
`.com` address**. *The classifier was calling a bio non-English because it contained an email.*
It was reading the outcome it was supposed to predict.

Repaired — strip addresses and URLs before tokenising, and drop every token that collides with
email vocabulary — the control now reads cleanly (English: *for, my, and, to, the*;
other-Latin: *la, que, en, mi, el, es, para*) and **the finding collapses**:

| bucket | n | address in bio | rate |
|---|---|---|---|
| `latin/english` | 25,118 | 1,625 | 6.469% [6.172–6.780] |
| `latin/other-latin` | 1,388 | 115 | 8.285% [6.948–9.853] |
| `latin/too-short` | 8,295 | 411 | 4.955% [4.508–5.443] |
| `latin/undetermined` | 11,035 | 753 | 6.824% [6.368–7.309] |
| `neutral` | 1,582 | 0 | 0.000% [0.000–0.242] |
| `non-latin` | 2,612 | 8 | 0.306% [0.155–0.603] |

* **English 6.469% [6.172–6.780] against
  other-Latin 8.285% [6.948–9.853]** — a
  difference of **1.82 points**, not 31, and if
  anything **non-English publishes slightly MORE**. **His hunch is refuted in the direction he
  proposed.**
* **Non-Latin script replicates the known prior exactly**: 0.306%
  [0.155–0.603] against a published 0.4% [0.3–0.7]. **That is a
  positive control on this entire pipeline**, arrived at independently.

⚠️ **THE WITHIN-TAG TEST IS REPORTED AS ABSENT, NOT AS A RESULT.** Language could still be a
proxy for *which tags were walked* — BL-1566 proved tag selection is the dominant lever on this
surface. Holding the tag fixed, only **1 tag** of
1,042 carries ≥20 rows in both arms. One cluster is not a contrast: the
bootstrap degenerates to a single point and **the question cannot be answered from this store.**
It is not answered here.

⚠️ **AND THE STORE IS NOT A FRESH WALK.** Every rate in this section is master's, and master is
exactly what a walk's dedup guard exists to EXCLUDE — its pooled rate runs ~6% against 3.4%
fresh. The **contrast** is what is claimed, never the level.

## 7. Part 5 — the four fixes, and 56 addresses finally delivered

**`effective_run_cap()` ALREADY EXISTED AND WAS ALREADY CORRECT.** The brief said not to write
a seventh implementation of the zero-cap rule, and the right move turned out to be smaller than
that: `finder_common.effective_run_cap` already resolves by **presence**, already returns 0.0
for a declared zero, and already folds in the lifetime ceiling via
`spend_ledger.lifetime_cap_declared`. **The three sites simply never called it** — they
hand-rolled `float(config.get(k, 5.0) or 0)`, whose result then met `if max_run_usd and …` in
the finder, where **0.0 means *no cap*.** The operator most likely to type 0 is the one who
means *spend nothing*. Now wired to the existing resolver, with `meme_finder.py:5794`'s
refuse-at-zero idiom copied rather than reinvented.

⚠️ **AND THE TWO HALVES STILL DISAGREE ABOUT WHAT ZERO MEANS — reported, not fixed.**
`effective_run_cap`'s docstring says "0.0 means *no budget* and every caller already reads it
that way". The finders read 0.0 as **unlimited** (`email_finder.py:643`,
`twitch_finder.py:1501` and `:1552`, `spotify_finder.py:1041` and `:1110`). Closing the
operator-facing path does not reconcile that, and flipping the finders' convention would
reverse a default other callers depend on. **It needs its own round.** The family is also
larger than six: `caption_finder.py:1102` and `:1325` carry the same `or 0` shape.

**The dead counters now have a reader, on live paths.** `unexpected_status_count` had **2
stores and 0 loads** in both clients; `unbilled_requests` and `throttled_requests` the same in
`ig_client`; `unexpected_statuses` had **0 loads anywhere in the tree**. Their own comment says
why they exist: a vendor changing its refusal code "would look exactly like Instagram running
out of posts — **silently, and at full price**". Added `vendor_anomalies()` to both clients and
wired it into **four** production paths — the three finder funnels and the hashtag walk, where
it is stamped onto the per-tag summary the checkpoint already persists. On the walk that is the
worst place for silence: an unexpected status returns `None`, the page loop sees no items, and
`classify_stop` calls the tag **`drained`** — the normal, unalarming end of every tag.

**`JUDGE_RULES_NEEDING_PROFILE` is wired, not deleted.** It had 1 store and 0 loads while its
comment claimed it made an unknown rule "fail CLOSED" — a property that really comes from the
allowlist tested one line above. It is now consulted to separate *a rule we classified as
needing the billed payload* from *a rule nobody has classified at all*, which is the case the
comment was written about. **No keep/reject decision changes**; a negative control in the suite
proves the gate did not open.

**And the 56 addresses BL-1566 bought are delivered.** BL-1566 refused to write them because
its own claim did not declare `master_leads.csv` or the workbook — right, and the cost was a
round's delay. This round declared both up front:

| | |
|---|---|
| rows parsed | 56 |
| appended to `master_leads.csv` | 56 (74,162 → 74,218) |
| appended to the workbook | 46 (Emails 2,982 → 3,028) |

The workbook was found **by searching**, never by a hard-coded path. The guard loaded
148,284 accounts and 13,882 addresses and **its polarity was proved in both directions** before
a single row was written; **zero C0 control bytes were asserted BEFORE the write, not after**.
The 10 rows that went to master but not the workbook were
already held there — the same master/workbook divergence BL-1564 measured at 94%.

⚠️ **The `Instagram` column already existed and was not invented.** The workbook also carries
`Bio source`, `Staleness` and `Email quality` **three times each** in its header row. That is
pre-existing, it was not introduced here, and it means a positional writer could silently fill
the wrong one.

## 8. What I got wrong, and what is absent

**I shipped a circular classifier and reported its output as a finding.** The 34.95%-vs-3.98%
language split was my stop-word list counting `com` — from `.com` — as evidence of Portuguese.
It was caught only because the positive control printed the tokens driving each bucket. **A
classifier that can see the outcome is not a classifier**, and I would have published an 8.8x
effect that does not exist.

**My first wiring test counted the wrong symbol and failed on correct code.** It demanded three
calls to `vendor_anomalies()` in `control.py`, where the three finders correctly reach it
through one shared helper. Counting the leaf call measured the architecture, not the wiring.
Both links of the chain are checked now.

**I overwrote another round's committed artefact by reusing its code without redirecting every
path it writes.** BL-1566's backup module writes its manifest to *its own* `_HERE`, so
overriding `DEST` and `ROUND` sent the store copies to `backups_bl1567/` while the manifest
clobbered `scratch/bl1566/backup_manifest.json` — a file committed by the previous round, which
then read `round: bl1567` on disk. **Its own print line said "wrote scratch/bl1567/…" while
writing somewhere else**, so the output could not have caught it either; the claim manifest
did, by failing to verify. Restored from HEAD, redirected properly, and the re-run now asserts
BL-1566's manifest still says `bl1566` before it will pass. **Reusing a module means redirecting
every path it writes, not the one you happened to think of.**

⚠️ **And the re-run then refused, correctly**: the backup's row anchor expects master at 74,162
and found **74,218** — the 56 rows this round delivered. A guard that notices its own input
moved is doing its job, and the refusal is recorded rather than suppressed.

**I wrote a fresh declaration with no reader, in the round about declarations with no
readers.** My claim listed every path it would write under `paths_i_may_write` — a key of my
own invention. `tools/claim.py::rounds_owning` reads **`will_write`**, so `tools/commit.py`
reported six of my own files as "no live round declared" while the claim sat there naming all
six. It is the same shape as `unexpected_status_count` (2 stores, 0 loads) and
`JUDGE_RULES_NEEDING_PROFILE` (1 store, 0 loads) — and I committed it **while fixing those**.
A declaration with no reader is not a declaration. Fixed; the prose key is kept beside it.

**My TLD adjudication list was wrong in the direction that flatters the conclusion** — it
called four delegated ccTLDs junk. Small, but it is the error that makes a refutation look
cleaner than it is, and it is counted in section 3a rather than quietly fixed.

**Reported as ABSENT, not as zero:**

* **The within-tag language test cannot be answered from this store** — one tag of
  1,042 carries both arms at n≥20. Language versus tag selection is open.
* **The `bioLink` paid field was not re-measured**; the 1-in-60 figure stands on its own round.
* **No probe was bought for the @mention chase**, deliberately: the arithmetic refuses it at
  any yield ever observed, so a measurement could not change the decision.
* **Whether the operator is seeing addresses somewhere this round never looked** — video
  captions, pinned comments, or images — is untested. The bio is the only surface measured.
* **Whether the 29 failing suites were red before this round** — 0 of 29 reference anything
  this round changed and four trace to unrelated causes, but I did not run the suite at the
  previous commit and diff the sets, so it stays an inference.
* **13,007 addresses, none ever contacted.** Unchanged, and still the largest open question in
  the project.

---

https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/BL-1567-the-97-percent-are-not-reachable.md
