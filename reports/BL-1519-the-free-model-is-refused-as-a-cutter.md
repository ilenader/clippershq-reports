# BL-1519 — the free model is refused as a cutter, and the measurement already existed

## 0. SAFE TO RUN, AND THE HEADLINE ANSWER

**Safe to run.** Nothing about the judge's behaviour changed. This round shipped **one test file and one claims manifest** — no production code, no store, no config. $0.00 spent, no vendor or model call made. All eight protected files backed up and sha256-verified with a corruption control that fired on every one.

**Is the judge now free? No — and it should not be.** The brief asked me to score `minimax/minimax-m3:free` on ~60 of his wanted pages and grant it cutting authority if it cleared the bar. **That run already exists, at exactly n=60, and it refuses the model.** I re-derived it from the raw per-page rows rather than from any report: at the threshold where minimax cuts usefully it **kills 3 of his 60 wanted pages including one he scored 10**, and at the only threshold where it kills none it **rejects nothing at all**. The brief's "0 of 38" is a smaller, luckier sample of the same model.

**What did that cost in accuracy? Nothing — because the free model was never going to be the cutter.** But there is a real prize next door that nobody costed: minimax as a **free first pass** with the paid model kept as the sole cutter saves **39.0% of all paid judge calls with 0 of 60 wanted pages killed**, at a measured cost of one lost correct rejection in 86. That is $0.0890 → $0.0543 per 1,000. **I did not ship it**, for a reason given in section 5, and the reason is itself a defect I proved by driving.

**Is the Instagram wall still worth buying a solution for? Unanswered by me, and I will not guess.** I asked the round that is removing the browser from that path whether its work drives end to end today. It said **no, not yet** — so the browser is still on the critical path and the question stays open. My own wall measurements did not happen: all six of my sub-agents were killed by a platform session limit before any of them reported.

---

## 1. WHAT I WAS ASKED TO DO

Ship a free judge model; attack the Instagram wall from an untried angle; confirm a cap fix; persist a free account id; and hunt for anything else being paid for that is free.

**What I actually delivered is narrower than that, and section 6 says why.** Six sub-agents — the minimax scoring run, a live enumeration of every free image-capable model, the cap confirmation, the wall/header work, a payload-overlap census and the reserved free-hunt — all terminated on a platform rate limit (HTTP 429, "session limit") within minutes of launch. None reported. I finished the round single-handed and scoped it to what I could measure myself and prove.

---

## 2. WHAT SHIPPED

**One artefact, and it is a protection rather than a proof.**

`tests/test_bl1519_quartering_guard.py` — 9 tests for `clippershq/free_judge.py:1151 _assert_not_quartered` and its exception `SilentlyQuartered` (`free_judge.py:507`), enrolled in `docs/claims/BL-1519.claims`.

**Why this and not something bigger:** that guard was shipped one round earlier to stop a silently-cropped contact sheet reaching the judge, and **mutation-proved 5/5 by its own author with an ad-hoc driver that was never committed.** A later audit found it had **zero test references repo-wide** and that deleting it **survived three suites — including the one named after the very defect it prevents.** A proof is an event; a protection must be an artefact.

**How it was proved — mutation, both ways:**

```
ARM 1  guard intact    Ran 9 tests   rc=0   GREEN
ARM 2  raise deleted   Ran 9 tests   rc=1   RED
         FAIL: test_raises_on_an_exact_half
         FAIL: test_raises_on_an_exact_quarter
         FAIL: test_raises_on_an_exact_third
         FAIL: test_survives_dash_O
VERDICT: KILLED
```

The other **5 tests stayed GREEN under the same mutation** — they are negative controls (a plain 1200→760 downscale, an equal-width encode, a ratio just outside the 2% tolerance at 1200/2.1 = 571, an unreadable input, and the exception's own existence). **That is what proves the suite is not simply a guard that raises unconditionally**, which is the failure mode of a test written to pass.

Restore verified byte-identical: sha256 `c8d16199edffd437` before and after, `git diff --numstat` empty. `__pycache__` purged and `PYTHONDONTWRITEBYTECODE=1` set between arms, because a same-byte-length edit once reused a stale `.pyc` and reported a false SURVIVED.

`test_survives_dash_O` drives the guard in a **subprocess under `python -O`**, because `-O` strips an `assert` and would disarm a guard silently. This guard uses `raise`; the test pins that it still fires.

**Fix category: LOCAL.** It protects one guard in one file. Searching one layer up: the general form — *every guard in this repo that was mutation-proved but never given a committed test* — is not addressed here and remains open.

**Suite state, stated honestly rather than claimed green.** The new suite is 9 of 9 green and mutation-proved. The claims manifest verifies 3 of 3 at HEAD, and **`tests/test_claims_manifest.py` — the one suite this round's manifest could have turned red — was run to completion and PASSED (exit 0).** The full run of **451 suites** was started and had **not finished** when this was published — at 52 suites in, one unrelated failure had appeared (`tests/test_atomic_io.py`). **I did not take "pre-existing" on trust:** both of this round's commits are pure ADDITIONS (`git show --name-status` reports `A` for both paths and no modification to any existing file), so breaking a pre-existing suite is structurally impossible for this change. That is a proof, not an assumption — but **the full suite result is NOT VERIFIED here**, and a green suite would only be evidence if I could say how many it was meant to run.

**Observed in passing, and recorded because it makes the guard non-theoretical:** while driving an unrelated probe, `SilentlyQuartered` **fired on a real contact sheet from the mark set** — a 1,720 px source encoded at 431 px, exactly one quarter, with `single_video=False`. Whether that is a true positive on a real defect or a false positive on a legitimately wide sheet, **I did not establish, and I am not claiming either.**

---

## 3. WHAT WAS MEASURED

### 3a. The pool, and its constant-answer baselines

**MEASURED.** 146 of his graded Instagram pages that have a grid, paired — the identical page set on both model arms, verified `|overlap| = 146`.

```
wanted (he scored >=6)      60
lows   (he scored <=5)      86
eights-to-tens (>=8)        40
CONSTANT-ANSWER BASELINES ON THIS POOL:  accept-everything 41.1%   reject-everything 58.9%
```

The baseline differs by pool — it is 58.1, 66.1, 56.4 or 59.1 elsewhere in this project. **58.9% is the reject-everything figure for THIS 146-page Instagram-with-grid pool** and no other.

**Ceiling, and it binds everything below:** his marks agree with themselves 75.6% overall, 89.2% on obvious pages and **48.0% [30.0, 66.5] near his decision line** — an interval spanning 50%. Nothing scored against his marks can exceed that. **The 95% bar belongs on kills of wanted pages, not on agreement.**

### 3b. minimax is refused at every threshold — RE-DERIVED from raw rows

**MEASURED**, re-derived by me from the raw per-page score rows, not from any report or comment.

```
minimax/minimax-m3:free   (FREE)
   T   rejects  catches/86   KILLS of 60 wanted   kill% [Wilson 95%]   of his 8-10s
  80        64          52                   12    20.0% [11.8, 31.8]             7
  85        53          45                    8    13.3% [ 6.9, 24.2]             7
  90        40          37                    3     5.0% [ 1.7, 13.7]             3
  95        12          10                    2     3.3% [ 0.9, 11.4]             2
  97         2           1                    1     1.7% [ 0.3,  8.9]             1
  98         0           0                    0     0.0% [ 0.0,  6.0]             0

nex-agi/nex-n2-mini       (PAID, the incumbent cutter, $0.0890 per 1,000)
  80        47          45                    2     3.3% [ 0.9, 11.4]             2
  85        44          43                    1     1.7% [ 0.3,  8.9]             1
  90        36          36                    0     0.0% [ 0.0,  6.0]             0
```

**The refusal is structural, not marginal. At every threshold where minimax cuts anything, it kills pages he wants. At 98, the only threshold where it kills none, it rejects nothing at all** — a cutter that cuts nothing is not a cutter.

**And its confidence carries no information where it matters.** At confidence **exactly 97** it killed one page he scored **10** and one page he scored **1**. Verified at row level from the raw data (handles withheld). More confident, more wrong.

**Head to head at T=90 on the identical paired set:** minimax rejects 40 and kills 3; nex-n2-mini rejects 36, catches 36 of the lows, and kills **0 of 60 [0.0, 6.0]**. The paid model catches essentially the same lows while killing none. **minimax is strictly worse on the axis that matters.**

**The brief's figure and mine are both real and they are not the same measurement.** The brief cites "0 of 38 wanted killed". My pool is 60 wanted from a paired 146. I name both rather than average them; on the larger pool the answer is 3, not 0.

**Failure modes, counted rather than dropped** — a torn or blank answer is UNJUDGED, never a rejection:

```
minimax      torn 1/146 = 0.7% [0.1, 3.8]   errored 13   total unjudged 14/146 = 9.6%
nex-n2-mini  torn 9/146 = 6.2% [3.3, 11.3]  errored  0   total unjudged  9/146 = 6.2%
```

minimax's failures are **errors, not tears** — the opposite profile to the incumbent's.

### 3c. The prize nobody costed: a free FIRST PASS

**MEASURED**, on the same paired 146, scored both ways as a judging change must be.

The rule tested: *minimax answers first; if it says WANT the page is kept and no paid call is made; anything else escalates to the paid model, which alone may cut.* This preserves the property that makes the chain safe — **a model with no score against his marks may ANSWER but may never CUT.**

```
                        paid calls   correct rejections   KILLS of 60 wanted
BASELINE (shipped)        146/146                   36                    0
FREE FIRST PASS            89/146                   35                    0
```

- **39.0% of paid judge calls eliminated.**
- **Kills of wanted pages: 0 of 60 — UNCHANGED.**
- **Safety cost, stated as a loss:** exactly **1** correct rejection discarded — 1 of 86 lows now reaching him, **1.2% [0.2, 6.3]**. Zero wanted pages were wrongly rescued, so the trade is one extra low delivered, not one fewer good page.
- **Money — and there are two defensible rates, so both are given rather than one chosen:**

```
                                   baseline    first pass    saving per 1,000
shipped constant  $0.0890/1,000     $0.0890       $0.0543            $0.0347
peer-MEASURED     $0.1054/1,000     $0.1054       $0.0643            $0.0411
```

`PAID_FALLBACK_USD_PER_1000 = 0.0890` at `free_judge.py:299` is the shipped constant and the file calls it "measured, not the sticker". **A concurrent round metered it today at $0.1054 from observed usage — 18.4% higher.** I have NOT verified that figure myself; it is marked NOT VERIFIED and named beside mine rather than averaged. If it is right, the shipped constant understates the baseline this change improves on, which makes the saving **larger**, not smaller.

**DERIVED, not measured:** the 39.0% assumes the live mix of pages resembles this 146-page graded pool. It will not exactly.

**And a caution against overselling this, from the same peer's round:** on TikTok the judge is roughly **a tenth of the bill** — about $0.13 per 1,000 delivered edit pages against $1.19 per 1,000 total, where discovery and `videos_from_handle` dominate at 22.5% and 75.7%. **Making the judge cheaper is an Instagram win, not a TikTok one.** On Instagram it sits beside the $19.73 → $9.88 grid halving, which is two orders of magnitude larger.

### 3d. The cap binds — DRIVEN, all three properties separately

**MEASURED**, by driving `clippershq/harvest_run.py:95 Budget.reserve`:

```
a zero cap REFUSES                                         PASS
the refusal is a RAISED EXCEPTION (BudgetExceeded)         PASS   — not a returned value
the METER DID NOT ADVANCE on the refusal                   PASS   — spent 0.0->0.0, calls 0->0
NEGATIVE CONTROL: a funded cap ALLOWS                      PASS   — proves the refusal is not vacuous
the meter DID advance when allowed                         PASS
BOUNDARY: the 3rd call over a 2-call cap is refused        PASS   — meter still reads exactly the cap
the refusal survives `python -O`                           PASS   — it is a raise, not an assert
```

The raise sits **before** `self.spent += want`, which is why the meter cannot advance on a refusal.

**One documented consequence worth stating, because it is easy to misread as a hole:** with `unit = 0.0` — a genuinely free model — a `$0.00` cap **allows** the call, because `0 + 0 > 0` is false. That is correct: a free call costs nothing. **But it means a cap cannot be used to stop a free model from running.** Rate, not budget, is the only lever on a free lane.

---

## 4. WHAT WAS REFUSED, AND WHY

**Cutting authority for `minimax/minimax-m3:free` — REFUSED, on the numbers in 3b.** This is the round's primary deliverable and it is a refusal. It matches the decision already recorded in the code, reached independently from the raw rows.

**Shipping the free first pass — REFUSED THIS ROUND, and the reason is a defect.** See section 5. In short: the chain cannot currently escalate, so wiring a free model first would not produce the arm I measured — it would produce the catastrophic one.

**Part 4, persisting the free account id — DROPPED, because another round holds it.** Persisting the `user_id` already present free on the discovery record makes an Instagram grid one billed call instead of two, halving the buy-outright price from **$19.73 to $9.88 per 1,000** with no purchase and no new capability. That work is **in flight in a file another round holds**, and its owner told me explicitly not to redo it. A third round independently re-derived the arithmetic forward (2 × $0.00069064 × 14,300 loads = $19.75 against the $19.73 on record), so **the halving is arithmetic, not an estimate.** I will confirm it by driving their committed code, not by reimplementing it.

**Buying any proxy — REFUSED.** I have no authority to purchase anything and did not. Pricing was assigned to an agent that died before reporting.

---

## 5. THE DEFECT I PROVED AND DID NOT FIX

**`clippershq/free_judge.py:1899-1910`. The code contradicts its own message.**

When a model that is not in `MAY_REJECT` returns REJECT, the code writes a reason saying the page *"is KEPT and escalated"* — and then, on the next line, `return False, detail`, which **leaves the loop.** Nothing is escalated. The later models, including the paid cutter that alone may cut, are never asked.

**Driven, not read.** I patched the ask function with a spy that raises a **`BaseException` subclass** — so the chain's `except Exception` fallbacks could not swallow it and silently retry — and it never fired:

```
is the free model scored?  False        (not in MAY_REJECT, so it may not cut)
PAID_FALLBACK              nex-agi/nex-n2-mini
RETURNED WITHOUT ESCALATING
  reason: "... said REJECT at 95, but it has never been scored against his marks,
           so the page is KEPT and escalated"
  models asked in order: ['minimax/minimax-m3:free']
=> the paid model was NOT asked.
```

**Why it matters more than it looks.** Today the chain asks the paid model **first**, so this branch is reached only after the paid model has already failed — the practical exposure is small. **But it is exactly the wall between the measured prize and the catastrophe.** Wire a free model first without fixing this, and a free REJECT terminates the chain and returns KEEP: the judge becomes free, fast, and **stops rejecting anything**, which photographs as success on every metric that counts cost rather than delivered pages.

**Why I did not fix it.** The fix is a control-flow change inside a loop dense with load-bearing history, in a live judge, and it needs a full paired re-validation on his marks in both directions. I lost all six sub-agents to a platform rate limit and did not have the capacity left to validate it to the standard this change requires. **A control-flow edit to a judge that I cannot fully validate is precisely the class of change that looks like success and is not.** It is named here with `file:line` and left in place.

---

## 6. WHAT I GOT WRONG

**I lost the entire measurement programme and did not see it coming.** I launched six sub-agents in two batches. All six died on a platform session rate limit within minutes, none reported, and the round's whole empirical plan — the live minimax run, the free-model enumeration, the header-set door, the proxy pricing, the free-hunt — went with them. **I should have run the single decisive measurement myself first, before fanning out.** As it happened the decisive answer was already on disk, but I found that by luck, chasing a line a dying agent left behind.

**I very nearly trusted a partial artefact.** Two dying agents emitted single tantalising lines — one flagging that a code comment contradicted the brief, one saying "confirmed a real fail-open." Those are exactly the fragments a round publishes and retracts within the hour. **I re-derived the first from raw per-page rows myself and it held; I discarded the second entirely** and this report makes no fail-open claim, because I never verified one.

**My first backup instrument understated a store by 36x.** It reported `spend.json` at **781 rows**. The true count is **28,805**. My row-key function built a set from a truncated natural key, and a ledger whose rows share few distinct id/url/handle values collapsed almost entirely. A deletion that preserved the distinct key set would have been invisible. Fixed to an index-qualified hash of the whole row, and the true count is now reported beside the key-set size so a collapsing key function cannot silently understate a population again.

**I used the wrong check on the reports clone.** I tested `[ -d ../clippershq-reports/.git ]`. A peer warned that the same clone had been **broken until 16:00 today with `.git/objects` deleted** while HEAD, config, refs and packed-refs all remained — so the directory looks healthy and `[ -d .git ]` returns true in both states. Re-verified properly with `git rev-parse --is-inside-work-tree` and `count-objects -v` (5,825 packed objects). Healthy — but my original check could not have told me otherwise.

**My first probe of the chain was wrong twice** — wrong function signature, then wrong return type — and each failure printed an empty "models asked" list. **An empty list from a broken probe looks identical to an empty list from a chain that does not escalate.** Only the third attempt, once the free model actually appeared in the asked list, produced evidence. The two earlier "zeros" were instrument failures and are discarded.

**And my own console mangled its own output.** Several transcripts in this round render an em-dash as a replacement character, because the console is not UTF-8. Cosmetic here — but it is the same defect class that makes a peer's `claim.py list` crash partway through the third record, so that peer saw only two of four in-flight claims.

---

## 7. MONEY AND SAFETY, FROM THE RUN'S OWN COUNTER

**Spend: $0.00.** No vendor call, no model call, no network request was made by this round. Not measured by a ledger delta — a ledger delta cannot attribute a round here, because the shared ledger gained **1,131 rows from concurrent peers** while I worked, one client books nothing at all, and another autoflushes under a generic label (that once produced a 61% under-count). **$0.00 is the count of calls I made, which is zero.**

The cap was proven to bind **before** any spending agent was launched (3d), and no spending agent survived to use it.

**Backups: all 8 protected files, sha256-verified, each with a corruption control that fired.** Path built from a single round constant, never a prefix in a separate join argument.

```
config.json                     41 rows    sha OK  keyset OK  corruption detected
spend.json                  28,805 rows    sha OK  keyset OK  corruption detected
master_leads.csv             (not JSON)    sha OK  keyset OK  corruption detected
clip_seen.json               2,193 rows    sha OK  keyset OK  corruption detected
meme_pages_seen.json         6,196 rows    sha OK  keyset OK  corruption detected
tiktok_pages_seen.json       2,518 rows    sha OK  keyset OK  corruption detected
spotify_playlists_seen.json  1,923 rows    sha OK  keyset OK  corruption detected
suppress_mx.json             4,146 rows    sha OK  keyset OK  corruption detected
```

Bodies found **by shape** — the largest dict-or-list value — never by a guessed key name, because a dict-only helper once read a 2,193-row store as 0 and a 26,947-row ledger as 8, both being lists.

**No store, config or production file was written.** The only production file touched was `free_judge.py`, temporarily, during the mutation proof, restored byte-identical and verified twice.

**Concurrency.** Five other rounds were live. Two files I needed were held by other rounds; **I asked on the pipe rather than inferring, and recorded both answers.** One granted `free_judge.py` on loan. One retained three files and answered the question that mattered more than the files. The dashboard port was verified unbound from the listening-port table — never a command-line grep, never the stale marker file — immediately before every write under `clippershq/`.

---

## 8. WHAT HE SHOULD DO NEXT, RANKED BY DOLLARS AND HOURS SAVED PER 1,000

1. **Persist the free account id — $9.85 per 1,000 saved.** Halves the Instagram buy-outright price from $19.73 to $9.88. Already in flight under another round; needs confirming by driving, not rebuilding. **By far the largest number on this page.**
2. **Fix the escalation defect, then ship the free first pass — $0.0347 per 1,000 saved at the shipped rate, $0.0411 at the peer-measured one.** In that order, never the reverse. The fix is `free_judge.py:1899-1910`; the prize is 39.0% of paid judge calls at 0 additional kills. Requires a paired re-score on his marks in both directions before it ships. **Note this is an Instagram win: on TikTok the judge is about a tenth of the bill.**
   **And re-meter the constant while you are there** — `PAID_FALLBACK_USD_PER_1000 = 0.0890` at `free_judge.py:299` may be 18.4% low against a peer's $0.1054. A price constant that drifts makes every saving computed from it wrong in the same direction.
3. **Leave the cutter paid.** The free model is refused at every threshold. Re-testing it is not free of cost — it costs the pages it kills.
4. **Answer the wall question before pricing any proxy.** The round removing the browser from that path says it does not work end to end yet. Until that lands or fails, proxy pricing is a solution looking for a problem — and the economics already refuse residential at $42–$335 per 1,000 against $19.73 for simply buying the grid, or $9.88 once item 1 lands.
5. **Give every mutation-proved guard a committed test.** This round did one. The general form is unaddressed and is how a guard silently stops existing.

**Paths** (no absolute paths, no ports): the test is `tests/test_bl1519_quartering_guard.py`, the manifest `docs/claims/BL-1519.claims`, the evidence under `scratch/bl1519_*`, and the verified backups under `backups/bl1519_safety/`.
