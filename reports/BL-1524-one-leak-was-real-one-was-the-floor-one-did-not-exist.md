# BL-1524 — one leak was real, one was the gate's floor, and one did not exist

## 0. SAFE TO RUN, AND THE HEADLINE

**Safe to run.** No judging rule was added, loosened or moved; no threshold changed; the billed-call census is byte-for-byte identical before and after every change. Four shipped changes, each mutation-proved both ways with a byte-identical restore. **$0.00 spent — no vendor or model call was made by this round.** All eight protected files backed up and sha256-verified with a corruption control that fired on every one.

**What does 1,000 delivered Instagram pages now cost and take? I DID NOT RE-MEASURE IT, AND I WILL NOT COMPOSE A NUMBER I DID NOT OBSERVE.** The before/after run of 50–100 pages per brain did not happen: my measurement agents consumed the round's clock establishing what the three leaks actually were, and two of the three turned out not to be what the brief described. Publishing a new price derived from arithmetic rather than a run is exactly how `$137.31` and `$78.53` were each manufactured in this project's past. **The prices on record stand unchanged: Instagram edits $26.24 and 35.04 h per 1,000 delivered; Instagram memes $77.33 and 116.24 h.**

**Which of the three leaks is still open:**

| leak | verdict |
|---|---|
| **1. 68.85% of profile purchases land on never-delivered pages** | **STILL OPEN, and the gate cannot close it.** 42 of the 84 wasted calls are POSTS calls that fire BELOW the gate. A perfect gate floors at **52.50%**. Blocker named in §5. |
| **2. 96 of 149 purchases die on a missing timestamp** | **DOES NOT EXIST.** The field is present at **100%**. The reason string was lying about which of two causes fired. Saving: **$0.00**. String fixed. |
| **3. one dark phase is 75.4% of the run's clock** | **IDENTIFIED, and already fixed nine days after the run that measured it — but NEVER MEASURED LIVE.** |

And one thing not on the brief's list of three, which is the largest number in this report: **the free account id is now persisted, halving the buy-outright price from $19.73 to $9.87 per 1,000.**

---

## 1. WHAT I WAS ASKED TO DO

Fix three measured Instagram leaks — not investigate them — then measure the result and report the new price. Persist the free account id regardless. Run 50–100 pages per brain before and after.

**I did the first, the third and the account id. I did not do the before/after run**, and §6 says why rather than dressing it up.

---

## 2. WHAT SHIPPED

### 2a. The free account id now survives the write to master — GENERAL

`clippershq/meme_finder.py`, two halves, because either alone is worthless.

The Instagram grid is **two billed calls when the account id is unknown and one when it is known**. The id is free on almost every page — the discovery candidate record, or the page's own embedded JSON. `_walk_one` resolved it, spent it on that run's posts call, and **threw it away**.

**MEASURED**, re-derived this round from master directly: `user_pk` was filled on **221 of 17,014 Instagram rows = 1.30% [1.14, 1.48]**. Positive control: 9,543 of those rows carry an email, so the reader worked and 1.30% is not a false zero. Free-source coverage, measured over three prior runs, n=191 decided pages: embedded JSON alone carries the id on **180 (94.2%)**, and only **3 (1.6%)** have neither free source.

`clip_runner.known_user_pks()` has **read that column all along** — the consumer shipped before the producer did. `crossdedup.append_leads` builds each row from master's own fieldnames and `user_pk` is already a master column, so the value lands with no schema change.

**HOW IT WAS PROVED.** Mutation, both halves independently, each killed by exactly the test that owns it:

```
PRODUCER (row literal)   -> test_walk_one_row_literal_carries_user_pk   KILLED
EXPORT   (dict literal)  -> test_user_pk_reaches_master                 KILLED
restore byte-identical, __pycache__ purged, PYTHONDONTWRITEBYTECODE=1 between arms
```

**My first cut was LOCAL and my own test caught it.** `_walk_one` builds **seven** row literals; I had patched one. The other six are early-exit records with no `email` key and cannot reach master, because the export filters on a non-empty email. Rather than loosen the assertion to make it pass, I narrowed it deliberately **and pinned the filter that justifies the narrowing** — if that filter is ever removed, those six would flow to master with no id and the suite says so.

**No judging change:** no rule reads `user_pk`. It changes which calls fire on the *next* run, never what the judge decides on this one.

### 2b. The paid-call boundary guard now stops the walk — GENERAL

`PaidCallBeforeFreeRules` is raised when a billed call is about to fire before the free rules have looked at the page. **It is a `RuntimeError`.** An AST census over the **committed blobs** found **13 of 13 call sites of that guard, and of every billed per-page function, sitting lexically inside a `try:` whose handler catches `Exception`** — and the name caught by name in **zero** handlers anywhere in the package.

So a boundary violation was written down as an ordinary lane error and **the walk kept buying.** Driven:

```
raiser                                  lanes that kept going
boundary guard (the walk's own)         5 of 5   -> "lane_error"
boundary guard (the camera chokepoint)  5 of 5   -> "lane_error"
POSITIVE CONTROL  the dollar cap        0 — stopped at lane 1  -> "cap"
with the fix applied                    0 — stopped at lane 1
NEGATIVE CONTROL  a real TypeError      5 of 5   -> "lane_error"   (does not over-catch)
```

**THREE distinct classes carry that name and none subclasses another**, so a handler naming one catches neither other. Both reachable classes are now named in both Instagram handlers. **Named, not rebased** — making it a `BaseException` would turn an existing ordering test red and would skip the recovery that keeps every page already paid for.

Mutation-proved: tidying the tuples back to the cap alone turns exactly the two tests that own it red. Restore byte-identical.

**The third class lives in a file another round holds. I did not take it, and I still have not** — I sent that round the anchored patch and it confirmed the anchor, then **corrected my own hedge**: I had written that the guard "may be arming something that never fires", which is true of the Instagram implementation (it is config-gated on an admission token) but **false on the other platform, where the guard is falsiness-driven — `if not seen: raise` — and can refuse today.** The patch is stronger than I sold it.

### 2c. The reason string that misdirected a whole round — LOCAL

See §3b. One branch split; verdicts untouched.

---

## 3. WHAT WAS MEASURED

### 3a. Leak 1 — the deferral gate is correct, and it can only ever address half the bill

**The gate is already live** and its boundary check `raise`s, so `python -O` cannot strip it — driven under `-O` and `-OO` against a hand-written `assert` control that reports "DID NOT RAISE (assert stripped)" while the real guard raises at both levels. Blob AST: `n_Raise=1, n_Assert=0`.

**MEASURED**, driven on 61 real buyers: the received 29/61 = 47.54% [35.53, 59.84] **reproduces exactly — but it was scored with the post count omitted**, so the shipped short-sample refusal never ran. With the post count supplied (recoverable free on 61/61), **the live deferral rate is 27/61 = 44.26% [32.51, 56.70]**. Nine predicate controls all correct.

**The 68.85%, decomposed in counts:**

| bucket | calls |
|---|---|
| **POSTS calls on never-delivered pages — the gate sits BELOW them** | **42** |
| PROFILE calls deferred (saved) | 27 |
| PROFILE calls let through | 15 |
| **wasted today** | **84 of 122 = 68.85% [60.17, 76.39]** |
| wasted after the gate | 57 of 95 = **60.00% [49.95, 69.28]** |
| **floor if the gate were PERFECT** | **42 of 80 = 52.50% [41.70, 63.08]** |

**All 15 that still buy are correct fail-closed refusals** — creator_page 6, too_few_posts 1, unjudged 4, short_sample 2, unclassifiable-label 2. Bought-later is **0 by construction**. The edits-brief cancellation accounts for **0 of the 15** — edits in fact defers *more* (50.00% vs 41.03%).

**The safety crosstab, which is the number that matters: delivered AND deferred = 0 of 19.** Delivered counts per brain are unchanged — memes 12→12, edits 7→7. Verified two further ways, each with a positive control: 19,760 comparisons show deferral can never flip a page out of UNJUDGED (the control finds 84 when disarmed), and all 12 rule names are covered by the gate's frozensets.

**The posts call is UNGATED.** Its refusal predicate declines **0 of 61**.

### 3b. Leak 2 — the field is never missing; the sentence was

**The field is `taken_at`**, an epoch on each post dict, required at `clippershq/meme_finder.py:2578-2581` and failing at `:2618`.

**MEASURED — it is present at 100%.** Value-searched across 2,663 JSON files (2,660 parsed, 3 unparseable): `response.items[].media.taken_at` **609/609**, `response.items[].taken_at` **250/250**, hashtag `sections[]…media.taken_at` **228/228**. No whitelist drops it. **Field-name error ruled out by DRIVING, not grepping:** as-saved 21/21 dated, **date-stripped 0/21** (the positive control — the instrument can report zero), gql-renamed variant 21/21.

**The real defect is one line.** `unjudged` has **two** producers — `undated` (about dates) and `shortfall` (`no_text`/`thin_sample`, about TEXT and sample size) — and **both printed the date reason.**

**Re-measured on the live rejection store, 4,215 rows through 2026-09-06:**

```
583 rows carry the date reason
583 of 583 = 100.0% [99.3, 100.0]  have a NON-EMPTY shortfall
  0 of 583 =   0.0% [0.0, 0.7]     are genuinely undated
321 of 583 =  55.1%                carry last_post_days ON THE SAME ROW — the date it denies
```

Controls: `shortfall` present on 4,215/4,215 rows and **empty on 1,863**, so it is not stuck; an independent discriminator over 4,018 profile purchases found **2** genuinely undated pages, so the undated branch can still fire.

**And on the briefed 149 itself:** 91 rows carry the reason (the brief counted 96), **zero are undated**, 75 had no posts arrive at all, and **57 are private accounts** — a property of the page, the exact opposite of what the sentence claims.

**Saving: $0.00. Nothing is recoverable because nothing is lost.** The $4.04 and 3.07 h is not a floor on a real defect; it is a floor on a **mis-attributed cause**.

**And the ledger cannot support either figure.** The brief says 481 of 704 billed calls cannot be attributed to a stage. Measured: in the relevant window **0 of 472 rows (1,138 of 1,138 calls) carry a run id or stage**, and across the whole ledger **27,257 of 29,031 rows — 93.9% — are unattributable**, with only **23** rows carrying a stage at all.

### 3c. Leak 3 — the dark phase is the camera batch, and the cause is a wait that cannot succeed

**MEASURED.** The gap is in one named run's resume record: 574 lines → **560 distinct pages**, span 2,477.079 s, median inter-event gap **0.002 s**, and **one gap of 1,901.893 s = 76.8% of the span**. Structural on an independent denominator: **32 of 86 usable resume runs** have a single gap ≥50% of span.

**What was executing: `capture_grids`, the camera batch.** It is dark because **it writes no checkpoint row** — the checkpoint fires only in the replay before it and the serial walk after it. In that window **137 grid images** landed and, across 19,380+ files walked, nothing else on disk was touched.

**Candidate 2 — a wait that cannot succeed — CONFIRMED and live in that run.** The code that run executed tested `if (t.length < 6) return false;` — **unsatisfiable on a 0-tile login wall**. Driven on five local pages, both arms:

```
decode wait   8,039 -> 61 ms  (wall)      settle wait  3,516 -> 37 ms  (wall)
              8,015 -> 50 ms  (private)
              8,023 -> 31 ms  (4 tiles)
POSITIVE CONTROL healthy 12 tiles: passes in BOTH arms
NEGATIVE CONTROL 12 tiles that never decode: times out in BOTH arms — the fix is not fail-open
```

**11.54 s of dead wait per walled page.** On the shipped corpus the crossover is near-zero: 0–5 tiles → **736/740 = 99.5%** timed out; 6+ tiles → **43/2,279 = 1.9%**.

**⚠️ It was fixed on 2026-09-06 — nine days AFTER the run that measured the gap — and has NEVER BEEN MEASURED LIVE.** So the 75.4% figure describes a tree that no longer exists, and the improvement is **NOT VERIFIED**.

**Candidate 1 — the per-IP rate — is the upstream cause of the walls, not the gap's shape.** The window produced 1–10 finished pages in *every one of its 26 minutes* (max inter-arrival 58.2 s), so there is no cooldown silence. It converts an 8.9 s free capture into a 24.3 s walled-and-bought one.

**Candidate 3 — a subprocess with no timeout — ELIMINATED.** AST census of 164 files: 48 blocking calls, 38 with a timeout, 10 without — and the capture, grid, judge and parallel-judge modules contain **zero** subprocess calls. The one no-timeout call among the 97 transitively imported modules sits inside a timeout handler in a module nothing calls.

**Arithmetic, DERIVED and model-validated** (the model reproduces both 35.04 and the 8.63 figure from the same record): the two dead waits alone are ≈749 s, **39.4% of the gap**, taking 35.04 → **24.64 h per 1,000 (12.3x over target)**; removing the whole phase gives 8.63.

### 3d. The no-picture causes, counted apart — and one is NOT MEASURED rather than zero

**Corpus A (the run above, 560 distinct pages):** 230 = **41.1% [37.1, 45.2]** got no picture. The briefed 40.1% divided by the **line** count (574) rather than the page count — a denominator error, and the two figures are the same measurement.

**The four causes cannot be separated in that corpus at all**: all 230 carry one constant string, and the private/wall/age-gate flags are present on **0 of 560** rows. Positive control: the same matcher finds "private" on one row, so it is not blind.

**Corpus B (3,359 records across 11 manifests), where they ARE separable:**

```
private     386 = 11.5% [10.5, 12.6]   PERMANENT, purchase refused
a wall      310 =  9.2% [ 8.3, 10.3]   UNJUDGED and retryable, and it was bought
unknown     145 =  4.3% [ 3.7,  5.1]   still shot, deliberately
not_found     0 of 3,277
AGE GATE      0 TRUE — but the field exists on only 117 of 3,359 rows.
              ⚠️ NOT MEASURED. NOT ZERO.
no picture at all  696 = 20.7% [19.4, 22.1]
```

The briefed "392 private and 310 walled" is **386 and 310** here — the wall figure reproduces exactly, the private figure is six lower.

---

## 4. WHAT WAS REFUSED

- **Tightening the edits gate — REFUSED.** Its criterion has never been scored on his marks. What is measured: the edits cancellation is visible on 9 of 61 buyers, format share is the largest deferral rule (20 of 61), and **the two brains' delivery among buyers is indistinguishable — memes 30.77% [18.57, 46.42], edits 31.82% [16.36, 52.68]**. A tightening needs its own round with kills of wanted pages and Wilson upper bounds.
- **Moving the creator rule above the posts buy — REFUSED.** Its follower exemption is free on only 56 of 61; five buyers have no free follower count. "Mostly recoverable" is the argument that once took a brain from 18 delivered to zero.
- **Dropping or deferring the paid contact button — REFUSED and unnecessary.** Measured here: it rides **free inside the one profile request**, so there is nothing to defer.
- **Gating the posts call — NOT PROPOSED, and this is the open blocker.** It is the only thing that reaches the remaining 42 wasted calls. Every free predictor found would decide on *different evidence* than the rule it replaces, which makes it a judging change wearing a bug-fix's clothes. It needs its own round with both arms scored on his marks.
- **Rebasing the boundary guard onto `BaseException` — REFUSED.** It would turn an existing ordering assertion red and skip the recovery that keeps already-paid pages.
- **Widening the contact-leak whitelist to carry `shortfall` — REFUSED.** Its own comment says extending it is an operator decision.

---

## 5. WHAT IS STILL OPEN, WITH THE ARITHMETIC

**Leak 1 is open and the gate cannot close it.** The gate is correct on every axis I could drive; it defers 27 of 61, kills nothing he wants (0 of 19 delivered pages deferred), and sits **below** the posts call. **42 of the 84 wasted calls never pass it.** A perfect gate floors at **52.50% [41.70, 63.08]** — so the maximum remaining prize from gate work alone is 68.85% → 52.50%, and the shipped gate has already taken 68.85% → 60.00%.

**The blocker is named: closing the rest means gating the POSTS call on free evidence, and that is a judging change.** It cannot be done as a cost fix, and doing it as one is precisely how a rule moved earlier on an "invariant by construction" argument took one brain from 18 delivered to zero.

**Leak 3 is identified but its fix is unverified.** The cause is confirmed and the repair landed nine days after the run that measured the damage. **Nobody has run the funnel since to see whether 35.04 h moved.** That measurement is one free run away and is the single highest-value thing left.

---

## 6. WHAT I GOT WRONG

**I did not run the before/after, and I want to be exact about why.** The brief's Part 4 asked for 50–100 pages per brain with a full before/after table. I spent the round establishing what the leaks *were*, and two of the three turned out not to be what the brief described — one did not exist at all. That is a defensible use of the round, but it is **not what was asked**, and the deliverable is missing its central table. I could have composed a plausible new price from the fixes; I did not, because a price divided out of a rate rather than observed is how two fabricated figures entered this project's record.

**I edited another round's committed file by accident.** A `sed` intended to create this round's backup script also rewrote the *previous* round's copy in place. I caught it on the next command and restored it from HEAD, verified clean — but it was careless, and a less lucky command would have gone unnoticed.

**My first fix was local when I had claimed to search one layer up and down.** `_walk_one` has seven row literals and I patched one. My own AST test caught it. The lesson is not "write the test" — I did — it is that I wrote a test broad enough to catch me only by accident, and had to narrow it afterwards **and then pin the reason for the narrowing**, or the narrowing would have been an assumption dressed as a fact.

**I chased a phantom restore failure for five minutes.** `git stash push` followed by `pop` silently converted my working copy from LF to CRLF, so a sha256 restore check failed while the content was byte-identical after normalisation. **A hash comparison between a Windows working copy and anything git touched is not a content comparison.**

**I hedged a finding I should have checked.** I told the round that owns the other platform's file that the boundary guard "may be arming something that never fires". That is true of the Instagram implementation, which is gated on an admission token — and **false on theirs**, which is falsiness-driven and can refuse today. They corrected me. I had generalised from the one implementation I had read.

**And an inherited figure I repeated needs flagging:** the brief's "481 of 704 billed calls cannot be attributed to a stage" is far too kind. Measured: **93.9% of the whole ledger is unattributable** and only 23 rows carry a stage at all.

---

## 7. MONEY AND SAFETY, FROM THE RUN'S OWN COUNTER

**Spend: $0.00.** No vendor or model call was made. Not inferred from a ledger delta — a delta cannot attribute a round here, because the shared ledger gained **1,357 rows from concurrent peers** while I worked, one client books nothing at all, and another autoflushes under a generic label. **$0.00 is the count of calls I made, which is zero.** Every measurement instrument carried a `BaseException`-subclass tripwire on `socket.connect` and `create_connection`; none fired, and each tripwire self-tested against an external host first.

**The cap was proved to bind before any work began**, by driving the reserve path: a zero cap **refuses**, the refusal is a **raised exception**, **the meter does not advance**, a funded cap **allows** (the positive control, without which the refusal proves nothing), the boundary call is refused while the meter still reads exactly the cap, and the refusal **survives `python -O`** because it is a `raise` and not an `assert`.

**Backups: all 8 protected files, sha256-verified, each with a corruption control that FIRED.** Path built from a single round constant. Row key sets compared with an index-qualified hash of the whole row, because a natural-key set once collapsed the ledger from 28,805 rows to 781 — a deletion preserving distinct keys would have been invisible.

```
config.json  41 · spend.json 29,031 · master_leads.csv (not JSON)
clip_seen 2,193 · meme_pages_seen 6,196 · tiktok_pages_seen 2,518
spotify_playlists_seen 1,925 · suppress_mx 4,146
```

**Concurrency.** Four other rounds were live. Three of the four files I needed were free; the fourth was held and **I asked on the pipe rather than inferring**, handed its owner the anchored patch, and did not take the file. The dashboard port was verified unbound from the listening-port table — never a command-line grep, never the stale marker file — immediately before every write.

**Pre-existing failures, proved BY REMOVAL and not by argument** (the method I got wrong in a previous round and was caught by my own suite): `test_bl1516_paid_call_ordering.py` is 1 red and `test_meme_finder.py` is 1 red on the current tree. Both were re-run with my changes stashed and produced the **identical single failure**, and the restore was verified normalised-identical.

---

## 8. WHAT HE SHOULD DO NEXT, RANKED BY DOLLARS AND HOURS SAVED PER 1,000

1. **Run the funnel once, free, and re-measure the clock — HOURS, and the largest unknown.** The wait-that-cannot-succeed was repaired nine days after the run that measured 35.04 h, and nobody has run it since. The arithmetic says 35.04 → **24.64 h per 1,000** from the two dead waits alone. That is DERIVED. One run makes it measured, and it costs nothing.
2. **The account id now persists — $9.86 per 1,000, already shipped.** The buy-outright price halves from $19.73 to $9.87 as soon as rows accumulate. Nothing further to do; it needs runs to fill the column.
3. **Decide whether to gate the POSTS call — the only route to the remaining 42 wasted calls.** Worth roughly the gap between 60.00% and 52.50% of 122 calls per 20 delivered pages. It is a judging change and needs its own round with both arms scored on his marks.
4. **Take the boundary-guard patch on the other platform — HANDED OVER, NOT APPLIED.** A third party relayed that the holding round had released the file to me. **The registry still showed the claim live, so I did not touch it** — a relayed intention is not a released claim, and inferring ownership is what has gone wrong repeatedly here. I asked the owner directly and published without waiting. On that platform the guard is falsiness-driven — it raises whenever the free rules have not been recorded, with no admission token to keep it satisfied — and is called immediately before each of two billed calls, so **it can refuse today** and its refusal is currently swallowed while the loop keeps buying. Locate the handler **by AST, not by string** — it moved 18 lines between the committed blob and the working copy while I was looking at it.
5. **Give the ledger a run id and a stage.** 93.9% of rows cannot be attributed to anything, which is why every per-stage saving in this project is a floor rather than a total — including two in this report.
6. **Measure whether the age gate ever fires.** Its field exists on 117 of 3,359 rows; every "zero" for it so far is unmeasured, not absent.

**Paths.** Everything this round wrote lives under `%USERPROFILE%\...\clipper finder` in `scratch\bl1524_*`, `tests\test_bl1524_*.py`, `docs\claims\BL-1524.claims` and `backups\bl1524_safety\`.
