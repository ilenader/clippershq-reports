# BL-1520 — Instagram edits is not the worst brain. The denominator was.

**Round:** BL-1520 · **Date:** 2026-09-06 · **Spend: $0.00** — no vendor or billed call, by me
or by any sub-agent. Cap was $2.50 and nothing was spent against it.

**SAFE TO RUN: yes, and nothing was changed.** This round wrote **no production file**. Five
other rounds were live and held every file this work touches, so everything below is
measurement plus a specification. No judging rule was added or loosened, no threshold moved,
and no verdict can move because no judging code was edited.

---

## The headline answer

**Instagram edits should NOT be the priority, because it is not the worst brain — and the
figure that said it was is arithmetic, not economics.** The published **$131.21 per 1,000
delivered** divided vendor dollars by a run-record field called `leads`, and `leads` is not
delivered: it is **delivered AND carries an email AND is new to master** — three conditions.
On the single run every published Instagram-edits figure rests on, the checkpoint holds **20
passes and 4 leads**, so the price was divided by 4. Corrected, with the numerators untouched:
**Instagram edits is $26.24 and 35.04 hours per 1,000 delivered; Instagram MEMES is $77.33 and
116.24 hours** — memes is worse by **2.9x on money and 3.3x on clock**. Two further things fall
out of the same correction: **TikTok memes already meets the 2-hour clock target** at 1.97 h,
the only target this project has ever hit, hidden until now; and **TikTok edits has never
delivered a single page**, so calling it "the cheapest brain" was reading a zero denominator.
**Yes, the two Instagram brains genuinely run differently** — the edits brief cancels the memes
brief's central reject rule, so the free gate keeps **2.2x more pages and gets no better
pages**. But the single thing still making Instagram expensive is not the judge: **96 of 149
profile purchases die on a missing timestamp in our own payload**, and **one dark batch phase
is 75.4% of the entire clock**.

---

## 1. What this round was asked to do

Do for Instagram edits what an earlier round did for TikTok edits: test his hashtag-and-search
claim non-circularly; wire hashtag-led discovery for edits; find out why the edits brain buys a
paid profile nearly three times as often as memes; move the paid calls behind free decisions;
check whether his config actually selects edits mode; and re-measure cost and clock before and
after.

**This round did not complete all of it, and the incomplete parts are named in §5 rather than
reported as zeros.** Six sub-agents were launched; all six died on an account rate limit before
producing anything. Three were relaunched after the limit reset and completed. **The three that
were not relaunched — his-claim-tested-three-ways, hashtag wiring with the surface table, and
the nine dead free rules — were NOT measured.** No figure for them appears below.

---

## 2. What shipped

**Nothing was written to production, deliberately.** At the moment this round filed, five other
rounds were live and between them held every file the work needed: one held `meme_finder.py`,
`page_capture.py` and `ig_client.py`; another held `free_judge.py` and `tiktok_finder.py`. A
claim addresses files, not sessions, so rather than infer ownership I asked on the session pipe
and registered only `scratch/`, `output/`, `tests/`, `reports/` and `backups/` paths under this
round's id. Every recommendation below is therefore a **specification with its call site named**,
not an edit.

**Safety instruments that were built and driven, and which are the round's committed artefacts:**

* **The cap was verified to bind before any paid work was authorised**, by driving the funnel's own `reserve()` rather than reading it. A zero cap **refuses by raising** (`_CapReached`), the meter **does not advance on a refusal** (0 after refusal), a non-zero cap allows the first call (positive control — without it the refusal proves nothing), and it refuses again exactly at the ceiling. The shipped source was asserted to still contain the three statements the check assumes, and the raise was confirmed to sit **before** the increment by byte offset, so a future reordering fails this check loudly instead of silently.
* **The backup finds the body BY SHAPE and verifies by ROW KEY SET.** Both controls fire: a one-byte corruption at identical file size is detected, and **a top-level list is read as a body with its real length** — the exact case that once read a 2,193-row store as 0. All eight protected files copied and sha256-verified; at publication **0 of 8 changed** and every seen-store key set was identical. **The backup path is built from a single round constant**, because two rounds once wrote their backups under a third round's id.

---

## 3. What was measured

Every figure is marked **MEASURED** (observed here), **DERIVED** (computed from measured
inputs) or **NOT VERIFIED**. Rates carry Wilson 95% intervals and a named denominator.

### 3.1 The denominator, which is the round's headline — MEASURED

The published brain prices divided ledger dollars by a run record's `leads` field and called it
"delivered". The funnel's own code defines `leads` as **delivered ∧ carries an email ∧ new to
master**, and defines *delivered* separately as the PASS counter. On the one Instagram-edits run
all published figures rest on: **20 passes, 4 leads.**

| brain | delivered (passes) | $ / 1,000 delivered | hours / 1,000 | vs targets ($2 / 2 h) | published figure overstated by |
|---|---:|---:|---:|---|---:|
| instagram / edits | **20** | **$26.24** | **35.04** | 13.1x / 17.5x | **5.00x** |
| instagram / memes | **16** | **$77.33** | **116.24** | 38.7x / 58.1x | 2.29x |
| tiktok / memes | **25** | **$4.68** | **1.97** | 2.3x / **1.0x — MET** | 4.17x |
| tiktok / edits | **0** | undefined | undefined | — | — |

**The substitution is named in the project's own shipped source**, in a comment that says the
target counts delivered pages rather than addresses and that the email-bearing count is "a far
smaller number". **It was fixed in the targeting and never in the accounting.**

Consequences, stated plainly: **Instagram edits is not the worst brain — memes is.** Five
published reports point future work at the wrong one. **TikTok memes already meets the clock
target.** And **"TikTok edits is the cheapest brain" is a zero-denominator reading** — it has
never delivered a page, so it has no price.

### 3.2 Where the remaining 13.1x and 17.5x actually go — MEASURED unless marked

* **Clock: one dark batch phase is 75.4% of the run.** Inter-event gaps are median 0.002 s; a single gap is **1,901.9 s**. Without it the run is **8.63 h per 1,000 delivered — 4.3x the target** rather than 17.5x. This is structural, not an incident: **25 of 60 runs on record have a single gap ≥50% of their span.**
* **Camera: 230 of 574 walked pages — 40.1% [36.1, 44.1] — got no picture at all**, so no model ever saw them. They bought nothing; the cost is clock. **DERIVED: 10.85 h per 1,000.**
* **Money: 96 of 149 profile purchases — 64.4% [56.5, 71.7] — die on a missing timestamp field**, and the funnel's own reason string calls it *"a hole in OUR payload, not a property of the page."* **MEASURED floor: $4.04 and 3.07 h per 1,000 delivered.** A floor, not a total, because **481 of 704 billed calls cannot be attributed to a stage** — the ledger carries no run or stage id.

⚠️ **The baseline is 9 days stale on exactly these mechanisms.** The Instagram funnel has taken
seven commits since that run, two of them directly on the picture chooser and the profile
deferral. These figures describe the run that was measured, not necessarily the code today.

### 3.3 Why edits buys three times as often — the three candidates, separated by driving them

**It reproduces, and was re-derived a second way.** Corpus: three live metered Instagram runs on
disk (memes ×2, edits ×1).

| | free vision gate kills | buys a profile |
|---|---|---|
| memes | **116/155 = 74.8% [67.5, 81.0]** | 25.2% [19.0, 32.5] |
| edits | **10/32 = 31.2% [18.0, 48.6]** | **68.8% [51.4, 82.0]** |

Disjoint. A second derivation from per-page checkpoint events agrees **to the unit**. The
received 73.6% back-solves to 117/159 — **a 1.2-point denominator choice, not a disagreement.**

**Candidate 1 — the exemplar pack: REFUTED.** At the network boundary both brains receive
**byte-identical packs**: 9 of 9 image blocks share hashes, 8 of 8 exemplar files share sha256.
**A constant cannot explain a difference.**

**Candidate 2 — the wall shrinking edits' grid supply: REFUTED as the explanation, CONFIRMED as
a real supply problem.** Grid yield is memes 94.9% [90.6, 97.3] against edits 56.7% [46.4, 66.4]
— disjoint and real. **But restricted to complete 12-tile sheets only, the two brains still
split 76.4% [68.3, 82.9] against 32.1% [17.9, 50.7]** — still disjoint, with no tile dependence
inside either brain. Thin grids are a genuine cost, not the cause of the gap.

**Candidate 3 — the edits addendum: the only thing the system varies.** Of **21 content blocks
in the real POST body, exactly 2 differ, and both are text**: the brief grows **5,749 → 12,373
bytes (+115%)**, and a 385-byte header tells the model **not to trust the scores** on the four
reject examples. The exact-concatenation claim is **confirmed byte-for-byte** across all four
briefs, with a negative control that fails as it should. The mechanism is named in the project's
own rule table: **the memes brief's central reject rule — no burned-in text means REJECT — is
explicitly cancelled for edits**, full-frame is reversed, and the replacement criterion ("the
treated look") **is a judgement, not a test**.

**`bars_kill` ruled out with two positive controls, not by assumption.** It fired **0 times in
both brains**. Control one: a 7/7 truth table proving the rule *can* fire and is off in edits by
construction. Control two: **real production runs on disk that did record it** (42 and 123
rejections), proving the reader finds the key when a run wrote one. In all three corpus runs the
measurement is **absent**, meaning the rule **abstained rather than declined**. **All 126 free
kills were the model's own verdict.**

**Cost lever or accuracy defect? A COST LEVER.** Survivors of both gates deliver at
indistinguishable rates — memes 30.8% [18.6, 46.4], edits 31.8% [16.4, 52.7]. **The edits gate
keeps 2.2x more pages and gets no better pages.** The brief moves mass into UNCERTAIN (53.1%
against 21.9%), not into KEEP. Tightening edits to the memes rate would avoid roughly 28 paid
calls per 32 judged pages. **It is not recommended**, because the criterion that would be
restored **has never been scored against his marks**.

⚠️ **A confound that could not be removed, stated rather than buried.** The two brains walked
**disjoint channels** in this corpus — memes entirely one surface, edits entirely two others,
**zero page overlap**. Brief and population are therefore perfectly confounded. The boundary
diff proves the brief is the only thing **the system** changes; **it cannot prove the brief
changed the model's mind.** Settling that needs roughly 120 model calls, which this round's cap
forbade.

### 3.4 Corrections to figures this round was handed

* **"Five of eight exemplars are 75.7–91.9% bare canvas" → it is TWO of eight.** Measured **per tile** against the builder's own canvas constant, taken from the source rather than assumed. Two reject-side sheets are **92.0%** (11 of 12 tiles empty) and **76.1%** (9 of 12); the other six are 2.7–10.6%. The claimed *range* matches; the *count* does not. **A rival claim of "worst 16%, none above 70%" is also refuted.** And the reason both readings were wrong is instructive: **a detector counting "blank" as below grey 16 reads those two sheets at 0.5% and 5.5% and reads a FULL sheet at 60.4% — exactly backwards** — because the canvas is painted lighter than its threshold.
* **"Two exemplars repeat a cover inside themselves" → REFUTED**, 0 of 8, with a planted-duplicate control that does detect one.
* **"392 private and 310 walled captures" → not present in this corpus.** The private and login-wall flags are false on **all 237 captured rows**, and all 10 zero-tile rows carry cause "unknown". Private, login-wall and unknown are reported apart, never pooled.
* **`reject_at = 80` is NOT "never read in the body".** It is read, at the judge's GOOD-versus-MAYBE boundary — the line that decides whether a keep is escalated. It **is** dead as a *cut* threshold: the per-model bar of 90 is the only path to a rejection, and the source says so, recording that at 80 one model killed 2 of his 60 wanted pages. **Removing it as "dead" would silently change escalation.**
* **"95.2% of purchases against pages with an address"** is a **TikTok** figure, mis-attributed to Instagram. Instagram measures **96.72% [91.87, 98.72]**.
* **"62.3% did not need it" and "79 calls instead of 122, 35.2% fewer" do not hold for the shipped gate.** The live deferral defers **29 of 61 = 47.54% [35.53, 59.84]**, giving **122 → 93 calls, 23.77% fewer**. The nine-page gap is 5 pages rejected on a rule that genuinely needs the profile and 4 left UNJUDGED — **both refused correctly, fail-closed.**
* **A "96.4% verified free" figure is a hardcoded note string in a prior round's script, not a computed value.** Measured independently on 150 distinct accounts: **150/150 = 100% [97.5, 100]**.

### 3.5 Does his config actually select edits mode? — MEASURED, driven

**No, and the mechanism is more specific than "it resolves to memes".**

His config sets the mode **per funnel** — one key under the Instagram funnel and one under the
TikTok funnel, both currently reading `memes`. **The funnel passes the TOP-LEVEL key**, which is
**absent**, so the resolver falls through to its hard-coded default.

Driven, on copies of his real config:

| | resolves to |
|---|---|
| his config as it stands | **memes** — "default", not "config" |
| per-funnel key set to `edits` | **memes** — the key is never read |
| top-level key set to `edits` | edits — "config" |

**The per-funnel mode keys he set are dead.** It is invisible today only because both happen to
say `memes`, which is also the default. **The moment he sets the Instagram funnel's mode to
`edits`, the run will still walk memes, and will report its mode as "default" rather than saying
an argument was dropped.**

**The working non-interactive routes are the command-line `--mode=edits` and the environment
variable** — both verified. **Correction to my own first probe:** I initially passed `--edits`
and read the resulting "memes" as a broken argv path. That was my instrument, not a defect — the
contract is `--mode=VALUE`. **Control:** an unrecognised mode **raises** rather than coercing to
memes, so the resolver is not silently swallowing typos.

### 3.6 The paid calls — MEASURED

**The reorder this round was asked to recommend is already shipped.** The Instagram profile
purchase already sits below the picture judge behind a deferral gate, with a boundary check that
**raises** (so `python -O` cannot strip it). ⚠️ **The round that shipped it says in its own
report that it did not** — "patch not delivered in time; the Instagram funnel untouched" —
**which is stale and contradicts that report's own headline.** Anyone planning from it will plan
work that is already done.

**Reproduced exactly:** 68.85% [60.17, 76.39] of 122 per-page purchases land on pages never
delivered (memes 69.23%, edits 68.18%). The flattering 59.6% variant reproduces at 59.57% of 141
— and the extra endpoint landed on a delivered page **19 of 19 times, by construction**, because
it only fires after a page has passed. **51.03% [47.96, 54.09] of 1,019 Instagram addresses come
from the paid contact button**, so that call **cannot be dropped — only deferred.**

**The free-field table**, n=61 buyers, compared by hash after first censusing the sentinel
vocabulary, with positive and negative comparator controls:

| field | free | note |
|---|---|---|
| account id | **61/61** | already free on the discovery record |
| private flag | **61/61** | |
| display name | **56/56** | byte-identical where present |
| bio | **49/49** | byte-identical where present |
| follower count | 91.8% | every disagreement a live counter moving; worst gap 0.068% |
| **verified flag** | **150/150 = 100% [97.5, 100]** on an independent 150-account corpus | **free in the payload and NEVER MAPPED** |
| category, media count | **0/61** and 0/150 | genuinely paid-only |

**A shipped comment claiming none of four fields is free is still live and still wrong** — two
are free, one is free but unpacked, one is paid-only. **The packing gap is one line**: the
normaliser maps six keys and drops the verified flag, which is present on 100% of raw accounts
and reaches **zero** judges.

**Recommendation, with the delivered-count hazard checked per brain** (19 delivered: memes 12,
edits 7). That hazard is real and has bitten: a rule moved earlier on an "invariant by
construction" argument took one brain's delivery **from 18 pages to zero**, because the author
object is rebound to the paid videos and the same rule read a different count either side of the
purchase.

| lever | delivered at risk (memes / edits) | $ per 1,000 delivered |
|---|---|---:|
| deferral gate — **already shipped** | 0 / 0, driven | $1.05 |
| **persist the account id** | **0 / 0, structural** | **$9.86** |
| pack the verified flag | 2/12 / 0/7 | $0.00 — saves no calls |
| move a creator rule above the posts buy | 2/12 [4.7, 44.8] / 0/7 | ≤$0.36 — **refuse** |

**Do the second one.** The account id is free on every discovery record and is **already wired
within a run**. The gap is **cross-run**: master's id column is filled on **221 of 17,014
Instagram rows = 1.30% [1.14, 1.48]**, so the next run starts blind. Writing it at the export
site **halves the buy-outright price from $19.73 to $9.87** with no purchase. **No rule reads
that column, so the rebind hazard cannot arise.**

**Refuse the fourth.** The rule it would move fires on the verified flag, and its follower
exemption is free on only 56 of 61 — **five buyers have no free follower count.** "Mostly
recoverable" is exactly the argument that took the other brain to zero delivered.

---

## 4. What was refused, and why

* **Writing any production file.** Five rounds were live and held all of them. I asked on the pipe and registered only my own paths.
* **Tightening the edits gate**, despite it being a measured cost lever. The criterion it would restore has never been scored on his marks, and this round may not move a threshold without scoring it both ways.
* **Arming a creator rule above the posts purchase** — five buyers have no free follower count, and the near-identical argument previously zeroed a brain's delivery.
* **Claiming the edits brief changed the model's mind.** The boundary diff proves the brief is the only thing the system varies; the two brains walked disjoint populations, so the confound is unremovable at this n. Settling it needs ~120 model calls the cap forbade.
* **Spending anything.** The cap was verified to bind, then nothing was spent.

---

## 5. What I got wrong — and what this round did not do

**This is the most useful section, and this time it includes a scope failure.**

* **Three of the seven briefed parts were not measured at all.** Six sub-agents died on an account rate limit; three were relaunched and completed. **His claim tested three ways, the hashtag wiring with a re-derived surface table, and the nine dead free rules were NOT done.** No figures for them appear anywhere above. **In particular the brief asked for search terms with their yields, which it correctly called among the most useful output — this round has none, because that measurement never ran.** That is an absence, not a zero.
* **My own first probe of the mode resolver was wrong.** I passed `--edits`, got "memes", and briefly read it as a broken argv path. The contract is `--mode=VALUE`. Caught by reading the resolver's own contract before publishing.
* **A sub-agent scored a field "56/56 byte-identical" by comparing `True` to `True`**, and another field "100% free" by treating an `<absent>` sentinel as a value. Both discarded before publication, after censusing the sentinel vocabulary first.
* **A sub-agent's leak scanner was wrong twice** — first with an **empty needle set**, giving a vacuously clean pass, then with substring matching that produced 82 false positives on ordinary English words. The final check is exact-token membership minus the source vocabulary: **0 findings across 27 files**, with a planted address, a key-shaped token and a **real** handle all caught.
* **Two false zeros were found and discarded rather than reported**: a sweep that read the wrong two field names (0 of 51,429 rows), and a corrected sweep that appeared to show one brief killing 85.2% on one surface and **0.0% of 2,892 pages** on another — an artefact, because the journal writes that key **only on a rejection**, so it has no keep-side denominator at all.
* **A "96 offered → 4 appended" reading was nearly published as "96 delivered."** It would have manufactured a price. The offer unions an all-time checkpoint, so that number measures checkpoint size.
* **A repo-wide search timed out** against ~135 unrelated sibling folders and had to be re-scoped — after a known-present control string was confirmed to fire, so the narrowed search was not trusted blind.

---

## 6. Money and safety

**$0.00 spent**, from the run's own counter at the wrapper — not from a ledger delta, which
could not attribute anything here in any case: the shared ledger gained rows from peer rounds
throughout, one client books nothing at all, and the Instagram client autoflushes on a timer
under a generic label that once mis-attributed 61% of a round's own spend.

**The cap was proved to bind before any paid work was authorised** — see §2. Nothing was spent
against it.

**Data.** All eight protected files backed up and sha256-verified before any work, with both
controls firing. At publication: **0 of 8 changed, and every seen-store row key set identical.**
No seen-store row was deleted or rewritten.

**Concurrency.** Five other rounds were live. This round wrote no production file; the other
modified paths in the tree are theirs. One of them is mid-edit on the Instagram funnel — **+72
lines, confined to the seen-store class**, far from the judge and purchase code measured here,
which is why these measurements are unaffected. **That round has committed nothing**, and the
data-built contact sheet it is building **does not exist in the committed blob or the working
copy**, so the clock baseline is **not** stale from that cause — checked by parsing the blob,
not by reading its report.

**No verdict can move**: no judging code was edited.

---

## 7. What he should do next — ranked by dollars and hours saved per 1,000 delivered

1. **Fix the denominator and re-aim at Instagram MEMES.** Costs nothing, changes everything: memes is worse than edits by 2.9x on money and 3.3x on clock, and five reports currently point the other way. **$0 and 0 h directly — but it redirects every future round.**
2. **Close the missing-timestamp hole that kills 64.4% of profile purchases.** **$4.04 and 3.07 h per 1,000** — a measured floor, because most billed calls cannot be attributed to a stage. Re-verify against the two recent commits first.
3. **Persist the account id across runs.** **$9.86 per 1,000**, halving the buy-outright price, with **zero delivered pages at risk in either brain** and no rule reading the column.
4. **Stop capturing pages the camera cannot photograph** — 40.1% of walked pages yield no picture. **$0 vendor, ~10.85 h per 1,000 (DERIVED).**
5. **Investigate the dark batch phase.** One gap is 75.4% of a run's clock, and 25 of 60 runs share the shape. Removing it alone takes Instagram edits from 17.5x to **4.3x** the clock target.
6. **Fix the mode key so the funnel reads the per-funnel value he actually sets** — otherwise the first time he asks for edits, he will silently get memes.
7. **Pack the verified flag** — free on 100% of accounts, reaches zero judges today. Saves no calls; it is an accuracy input, not a cost lever.
8. **Do NOT tighten the edits gate yet, and do NOT arm the creator rule above the posts buy.** Both are measured; both are refused above with the reason.

---

## 8. Paths to open

Relative to the project root (`%USERPROFILE%\...\clipper finder`):

* `scratch\bl1520_cap_binds.py` — the cap driven, with its four conditions and the control
* `scratch\bl1520_backup.py` — shape-based body finder, both controls, one round constant
* `scratch\bl1520_mode_resolves.py` — the mode resolver driven against his real config
* `scratch\bl1520_agentA_whybuys.md` — the three candidates separated, with the boundary diff
* `scratch\bl1520_agentC_paid.md` — the free-field table and the per-brain hazard check
* `scratch\bl1520_agentF_finding.md` — the denominator, and the corrected brain table

https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/BL-1520-instagram-edits-is-not-the-worst-brain.md
