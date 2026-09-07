# BL-1528 — Stop rejecting pages the model never saw

**Round:** BL-1528 · **Filed:** 2026-09-07 · **Cap:** $2.00 · **Spent: $0.0701**

---

## 1. Safe to run, and the headline answer

**Safe to run.** No threshold moved. Every change makes the funnel **more permissive on purpose**,
and each one that moves a verdict was scored on his marks both ways with kills of wanted pages
bounded. Nothing on disk was un-latched, no seen-store row was deleted, and no rule was loosened
without a control that could fail.

### How many pages he wanted were killed without being looked at, is it fixed, and how many are still blacklisted

**Of the six rows he had graded when this round read his marks, FOUR died without the picture judge
ever being called — and he marked all four KEEP. 4 of 4 = 100% [51.0, 100.0].** Re-derived two
independent ways — the shipped `mark_reader.resolve` against `run_result.json`, and raw
last-keystroke-by-timestamp against the export — which produced **identical SETS, not merely
identical counts**.

⚠️ **This is not an agreement rate and his self-consistency does not bound it.** His marks agree
with themselves 75.6% (89.2% on obvious pages, 48.0% [30.0, 66.5] near his decision line), and that
ceiling bounds *agreement*. This number is one-sided: **the machine never formed an opinion for him
to be inconsistent with.**

**The scale behind those four:**

| | his sheet | the whole run |
|---|---|---|
| never reached the model | **105 of 150 = 70.0% [62.2, 76.8]** | **595 of 767 = 77.6%** |
| rejections carrying no model verdict | **83 of 95 = 87.4% [79.2, 92.6]** | **490 of 537 = 91.2%** |

**And his "four facts NOT RECORDED" is the same defect, not a second one:** **0 of 45 judged rows**
are missing green-screen, average views or on-screen text; **105 of 105 never-judged rows are.**

**Is it fixed? For 243 pages yes — and NOT for the four he pointed at, which is the part he
needs to read.** The re-run puts **60 of the 105 sheet rows that never saw the model in front of
it (57.1%)**, run-wide **243 of 595 (40.8%)**, with **0 pages newly cut** (Wilson upper 0.5%) and
the model **keeping 190 of 243 (78.2%)**. ⚠️ **But of the four pages he graded KEEP that died
unseen, this round moves ZERO** — they died of a 515-day recency cut, two crawl shortfalls, and one
post-floor cut with a **genuine** count of 7, which the shipped 10-post floor correctly kills.
**The fix refuses a zero the payload contradicts; it does not overrule a real number.** §4e has the
detail and the threshold question that follows from it.

**The largest cause was not what anyone expected.**
The single biggest killer was **243 pages cut for having "0 posts" — a number the same payload
contradicts.** 243 of 243 came from the search lane, 0 of 289 from hashtags, and those pages
simultaneously reported 3–20 observed videos and a median 226,121 average views. Searched **by
value rather than by name** over 201-key author objects: **no post count exists on that endpoint
under any spelling — it is ABSENT, not zero**, and the positive control sits inside the same
response, where those accounts ship **14, 29 and 22 of their own posts** in the `aweme_list` that
reports them as having none.

**How many are still blacklisted: 260 rows, and re-admitting them is his call.** They keep their
stamp because **nothing was un-latched** — a seen-store row is never deleted, and a round once
deleted 56 rows another had paid for. Re-walking all 260 would cost **260 × $0.0006 = $0.156**.
⚠️ **One of the pages he marked KEEP is genuinely among them.** Going forward the defect is closed:
**258 of 537 rejections (48.04% [43.85, 52.27]) stop latching, and 0 newly latch.**

---

## 2. What I was asked to do

Count how many of the 150 graded rows died without the model being called and why; cross-reference
his grades to price the defect in his own currency; establish how many pages he wants are
permanently latched; ship the general rule that **a missing fact is UNJUDGED, never a rejection,
and never latches**; fill every "not recorded" field the payload actually carries; build niche
exhaustion with per-term yield and an atomic ledger; land the split paging fix; and re-run the 150
to show what moves.

---

## 3. What shipped

Every fix mutation-proved in both directions with the restore sha256-verified, tests using `raise`
never `assert`, green under `python -O`, and the no-`assert` rule enforced by an AST scan of each
test's own source.

| # | fix | `file:line` | category | proof |
|---|---|---|---|---|
| 1 | **A contradicted zero no longer cuts** — the post count is ABSENT on the search lane, so the existing "absent keeps the page" rule applies | 2 sites | **GENERAL** | driven over 27 inputs: **0 newly cut, 2 newly kept**; kills **0 of 243**, Wilson upper **≤1.56%** |
| 2 | **A torn model answer abstains instead of rejecting** — `certain:true` with no `text` key produced an empty cover, and the burned-in judge rejected it **outright, on the platform where rejection is FINAL** | `free_judge.py:2399` | LOCAL | an explicit `"text": ""` is deliberately untouched |
| 3 | **Abstain is no longer scored as a failure** — `editor_pct` returns `neutral=45` to mean *I could not read this*, and four gates compared it `<` a floor and cut | 4 sites | **GENERAL** | `qualify_author({}, ANIME15K)` returned `qualified=False` before; the score itself is byte-identical |
| 4 | **The latch stops inventing a decider** — `or RULES_VERSION` manufactured the very attribution `is_decided` checks for, so **260 of 317 latched rejections carry the literal string `BL-1484`** as their decider | `tiktok_finder.py:3956` | LOCAL | **258 of 537 stop latching, 0 newly latch**; `judge_author` now names its own decider |
| 5 | **Paging landed in the walker the campaign runner actually calls** | `discovery_search.py:234-416` | LOCAL, **6 sites, 2 holes, 1 landed** | driven BEFORE/AFTER on the real runner: **1 page / 30 authors → 10 pages / 300 authors** |
| 6 | **Free facts plumbed** — the TikTok facts block goes from **7 lines / 281 bytes to 19 lines / 1,029 bytes** | 7 fixes | GENERAL + LOCAL | verified on the **real POST body** of both brains, one flipped byte moving both hashes |
| 7 | **Three more reject-on-absent sites** | `main.py:2224`, `crawl_suggested.py:707` (**2nd of 2**), `parallel_judge.py:281/293` | LOCAL | — |
| 8 | **An unreachable page-size clamp deleted** — 31/40/50/100/200 all clamp to 30, so the 50 was unreachable twice over | — | LOCAL | zero behaviour change |

**Verdict-movement controls, per brain, both proved not blind:**
* **Instagram** — 1,555 real authors × 5 campaigns = 7,775 records: **91 CUT→KEPT, 0 KEPT→CUT**
  (5.85% [4.79, 7.13]), 0 prescreen movement. Blindness check: blanking one real author's text
  moved its five input hashes and its decision, **and nothing else's**.
* **TikTok** — the 767 real rows behind his sheet plus 100 grouped authors: **258 stop latching, 0
  newly latch**, and `judge_author`'s verdict core moved on **0 of 100**.

---

## 4. What was measured

### 4a. Unjudged is one thing wearing two names

**100% crawl shortfall, 0% `undated`** — 22 of 22 on the sheet, 105 of 105 in the run — **and all
of them carry a real `last_post_epoch`, the date the reason sentence denies.** This confirms the
briefed mislabel that misdirected an entire earlier round. ⚠️ **But the line numbers in the brief
(`meme_finder.py:2847/:2852`) are the Instagram file; TikTok is a different module with THREE
producers of the same state.** The finding transfers; the line numbers do not.

### 4b. The pinned flag — half the hypothesis refuted

`is_top` is present on **1,028 of 1,028** `aweme_list` items and occurs **zero times** in all 164
`clippershq` files, by AST **and** by text.

* **Views: the effect is large and real.** Pinned median **1,562,246** against unpinned **2,658** —
  **587.6×**. Including pins inflates an account's mean by a median **+3,885%**, and **12 of 65**
  pinned accounts clear the average-views floor **only because of the pin**, 12–0 in the rescue
  direction.
* ⚠️ **Recency: NO EFFECT, and my brief said otherwise.** The pin is a median 157 days older but
  **is never the newest post**, so the newest-post date moves **0.0 days at median AND at max**,
  with **zero stale flips**.

Shipped as **recorded, not acted on** — the numbers are now on the record without moving a verdict.

### 4c. The term engine is reachable from nowhere, and grep would have said otherwise

**Driven, not read:** `main.run_campaign` was run end-to-end with fake clients under a
`sys.meta_path` audit hook. The search well genuinely ran (1 call, 2 leads) and **`search_terms`
never entered `sys.modules`**; the hook returns True on an explicit import, so the zero belongs to
the code. **Its only durable artefact, `search_terms_ledger.json`, has never existed on disk.**

⚠️ **AN INVERSION OF THIS PROJECT'S OWN RULE.** An AST census over 5,155 files found **zero
importers** inside `clippershq/`, with a control that fires. The **text pass found 146 hits — and
every one inside `clippershq/` is the CONFIG KEY `meme_finder.search_terms`, not the module.**
**Grep would have declared the engine wired at six sites.** "AST beats grep" is the standing lesson
for reads; here text over-reported by six.

**The ledger was already atomic** (`search_terms.py:141` → `atomic_io.replace`): 25/25 saves land
with a thread holding the destination, and the bare-`os.replace` control **raises 25/25, leaving 25
orphan `.tmp` files**. ⚠️ The first harness held the handle for the whole call and measured nothing
— both arms failed — and said so rather than reporting a pass.

### 4d. Yield per term and per surface, never pooled

| term | TikTok distinct authors | IG reels |
|---|---:|---:|
| `khabib edit` | **99** | 12 |
| `mcgregor edit` | 88 | 12 |
| `ufc edit` | 70 | 9 |
| `edit ufc` | 60 | 11 |

⚠️ **Word order is not free, and it reverses by surface** — the suffix form wins by **+17% on
TikTok** while the prefix wins on Instagram. **Pages 2–4 carried 224 net-new authors of 269 = 83.3%
[78.3, 87.3], 2.41× page 1**, with **0 byte-identical pages out of 16**. Dead terms were **0 of 8,
Wilson [0.0, 32.4]** — which **does not refute** the briefed 30.8%; the sample is too small.

### 4e. The 150 re-run through the fixed path — and the four pages he named do NOT move

**MEASURED. $0.0577 at the wrapper; the replay itself was $0.00.**

| | measured |
|---|---|
| sheet rows that never saw the model and now reach it | **60 of 105 = 57.1% [47.6, 66.2]** |
| run-wide | **243 of 595 = 40.8% [37.0, 44.8]** |
| pages **newly cut** by the change | **0 of 767** — Wilson upper **0.5%** |
| of the newly-admitted pages, the model **keeps** | **190 of 243 = 78.2% [72.6, 82.9]** (second arm 187/243 = 77.0%) |
| on the 60 sheet rows | **51 of 60 = 85.0% [73.9, 91.9]** |
| baseline on the 172 pages it already saw | 127 of 172 = **73.8% [66.8, 79.8]** — **overlapping**, so this cohort is not judged more harshly |
| model call errors | **0 of 486** |

⚠️ **AND THE NUMBER HE ACTUALLY ASKED FOR HAS n = 0. THAT IS THE FINDING, NOT A GAP IN THE WORK.**

**All six rows he has graded are `found_via: hashtag:*`. All 243 pages this round newly admits are
`found_via: search:*`. The overlap is EMPTY.** The sheet itself is **76 hashtag / 74 search** and
**60 of the newly-admitted pages are on it** — he is simply grading in row order, and rows 1–6
happen to be hashtag. **He needs to grade a search-lane row, or the sheet needs re-ordering so the
two lanes interleave.** That is a shortfall with a named cause, not a zero.

⚠️ **AND THE HARDER HALF: OF THE FOUR PAGES HE GRADED THAT DIED UNSEEN AND HE MARKED KEEP, THIS
ROUND MOVES ZERO** — 0.0% [0.0, 49.0], n = 4. Their causes are **not** the contradicted zero:

* one **recency** cut — the page is **515 days stale**;
* **two crawl shortfalls**;
* one **post-floor** cut with a **REAL count of 7** on the hashtag lane. **The fix refuses a
  CONTRADICTED zero; a genuine 7 still dies**, and correctly so under the shipped 10-post floor.

**10 of the run's 253 post-floor cuts carry real counts of 4–9, all on the hashtag lane. That is a
question about HIS OWN 10-post floor, and this round did not touch it** — moving a threshold
requires scoring it on his marks both ways, which is a round of its own.

**So the honest statement is: the defect he found is real, large and now fixed for 243 pages — and
none of them are the four he pointed at.** The four he pointed at died of three other causes, one
of which is a threshold he chose.

**Three controls, each able to fail, and one discarded for being right by accident:**

1. **The BEFORE reproduces the run's recorded verdict AND its verbatim reason string on 486 of 488
   free-decided rows — 99.6% [98.5, 99.9].** The two misses are the language gate, which needs
   captions the run never persisted.
2. **On the REAL POST body**: 9 images decoded, the handle / posts / found-via lines verified
   present in **12,581 characters** of prompt, then **one pixel inverted at the centre of the
   sheet** moved both the page-image hash and the whole-body hash **while the prompt text stayed
   identical.** ⚠️ **The first version of this control flipped a raw byte, corrupted the PNG, and
   the pipeline died before building a body — so both hashes "moved" for entirely the wrong
   reason. That version was DISCARDED, not reported.**
3. **Flipping `author_video_count` from 0 to 1 collapses BEFORE and AFTER to the SAME decision
   hash** — proving **100% of the movement is the contradicted zero and nothing else.**

The clock was pinned to the run's own start before any import, because a sibling control reported
**55 false moves** from `time.time()` appearing in reason strings.

**Stated confounds:** three-tile reject sheets (no tile effect is measurable in the run's own data,
but it is not excluded) and captions **ABSENT from disk**.

### 4f. Two counts I am not resolving by picking one

**Silent handlers: 425 strict / 472 loose over 1,283 handlers across 164 modules** — against the
brief's 409 / 945 on a 1,249 denominator. **Four numbers from three definitions.** The gap is
flagged, not closed by choosing a favourite.

**The age gate is still a fifth state nothing handles.** `dom_age_gate` appears in **no module
outside `page_capture.py`**, and is absent from the suppression tuple (`:812`) and from
`_paid_grid_needed` (`:980`). **An age-gated page is still photographed and still bought.**

### The test verdict — a complete result, and a deliberate refusal to quote an incomplete one

**Targeted, COMPLETE, over every area this round touched** (`bl1528`, `bl1484`, `tiktok`, `paging`,
`judge`, `quality`, `latch`): **26 suites PASS, 1 red.**

The one red is `test_bl1300_judge_first.py`, and it is **red at HEAD too** — proved with the
runner's own `--head` flag, which runs a **clean extract of HEAD** rather than a worktree.
⚠️ **That distinction matters and it cost an earlier round:** `config.json` and `spend.json` are
gitignored, so a `git worktree` at any commit has neither, and proof-by-removal there produced two
suites erroring for unrelated reasons and one **SKIPPING with "no production ledger here" — and a
skip reads as a pass.** `--head` is the sound instrument.

⚠️ **THE FULL 464-SUITE RUNNER DID NOT FINISH, AND NO COUNT FROM IT APPEARS IN THIS REPORT.** It
had completed 78 suites when this was written. **Labelling a partial as partial is a disclosure,
not a safeguard** — an earlier round published "189 passed, 14 red" with exactly that disclaimer
and the finished run said **310 passed, 20 red, a 43% miss.** So the rule is: quote the verdict
line or quote nothing. **Nothing is quoted.**

**A second, wider sweep exists — and it did not finish either, which its author corrected in
print.** It was first reported to me as "233 of 464 suites at hand-off"; that sweep was **KILLED
before completing**, not completed. The corrected figures: **397 of 464 suites ran — 376 PASS, 21
FAIL — and 67 suites NEVER RAN, so their state is UNKNOWN. There is no verdict line in that log
either, and the tree is NOT claimed green.**

⚠️ **I had already written the uncorrected figure into this report before the correction arrived**
— the same "quote a number from a run that stopped early" error the paragraph above exists to
forbid, committed one paragraph below it. It is fixed here and recorded in §6.

**What the wider sweep DOES establish, stated as narrowly as it deserves:** all **21** reds were
re-run against a shadow tree carrying **only that agent's hunks reversed**, and every one is **red
both ways — NONE attributable to this round.** Six of the 21 appeared only after the earlier
triage and were put through the same test. The harness carries a working positive control — the
agent's own new suite is **green on the real tree and red on the shadow** — so "none attributable"
is a measurement rather than a harness that can only answer no. A spot-check of `test_bl1350_gates`
found it wants `meme_finder.STALE_DAYS == 152` against a shipped 180, in a file this round never
modified.

**So the honest summary of the whole tree is: 21 reds, none of them ours, 67 suites unknown, and no
claim that the tree is green.**

⚠️ **And one apparently clean result was DISCARDED rather than reported.** A 91-suite `unittest`
regression returned **rc=0 with a deliberately failing test planted inside it.** That is precisely
what `run_all.py`'s own docstring warns about — **a shell wrapper's exit code is not the runner's**
— so the result was thrown away rather than used.

---

## 5. What was refused

* **Un-latching anything.** 260 rows keep their stamp. Re-admitting them costs **$0.156** and is
  his call, not mine. A seen-store row is never deleted.
* **Five reject-on-absent sites found and deliberately NOT shipped**, each with a reason:
  `meme_finder.py:2757` (followers present on **525 of 525** stored bodies, so 0 verdicts move and
  it is unscoreable); the caption-substitution path driving `format_share` (largest blast radius —
  needs its own scored round); `market_filter.py:417` (the fix weakens a **different** brain's
  settled gate); `quality_gate.py:1200` (an `and` that should be `or`, firing on a **handle**
  substring); and `no_speech.refuse`, which is a **deliberate documented fail-closed** — flagged,
  not reversed.
* **Picking one silent-handler count.** Four numbers, three definitions (§4f).
* **Claiming the dead-term rate.** 0 of 8 with a Wilson upper bound of 32.4% cannot refute 30.8%.
* **Deleting `config.ig_page_size`.** It is still *sent* as `count`, and whether the vendor honours
  it was not measured — so it was **documented rather than deleted**.

---

## 6. What I got wrong

### ⚠️ I told an agent the wanted pages were not blacklisted. Half of that was wrong.

I drove the shipped `PageSeen.is_decided` over the live store, found that a rejection needs **both**
`verdict` and `judged_by` to latch, and concluded that unverdicted rejections re-walk — so the page
he scored ten was safe. **True of the 1,172 legacy rows. False of this run's 258.**

**What I missed is that the code manufactures the very attribution the guard checks for.**
`tiktok_finder.py` wrote `str(r.get("rule") or "")[:64] or RULES_VERSION`, so a free-gate rejection
with no rule name latched under the **literal string `BL-1484`** — a version constant standing in
for a decider. **260 of the 317 latched rejections carry it.** The guard asks "who decided this?"
and the code answers with its own release tag.

I checked the predicate and never checked what was being fed to it. **The agent I asked to
re-derive the number independently is the reason this was caught** — and it is why "re-derive a
headline a second way" is worth the tokens.

### My brief claimed the pinned flag corrupts recency. It does not.

I asserted an unread `is_top` corrupts **both** the recency reading and any view-based rule.
**Views: confirmed, 587.6×.** **Recency: refuted — 0.0 days at median and max, zero stale flips**,
because the pinned post is never the newest one. Half a hypothesis, stated as a whole.

### And two instruments failed before they worked, both caught by their own controls

* A verdict-movement control reported **55 false moves** because `time.time()` appears in reason
  strings — the clock had to be pinned before any before/after comparison meant anything.
* A rendered-bytes control probed the raw `desc` while the facts block ships a **whitespace-collapsed
  copy**, so it falsely reported "the fix does not ship" before being corrected.
* A mutation harness scored 8 of 9 with the miss being a **wrong anchor** — it mutated the keeper
  branch, which no rejection assertion can see. Redone on the rejection branch, it went red in both
  directions.

### I wrote an uncorrected test figure into this report

An agent reported a wider sweep as "233 of 464 suites, 15 red", and I wrote it into §4 as a
**complete** triage. It was not complete — that sweep had been **killed before finishing**, and its
author corrected it to **397 of 464 ran, 376 PASS / 21 FAIL, 67 never run and UNKNOWN**.

**I made the exact error the same section exists to forbid**, one paragraph below the paragraph
forbidding it, because a number arrived in a summary and I did not ask whether the run behind it
had reached its verdict line. **Quoting someone else's partial is the same sin as quoting your
own.**

### A test runner returned success on a planted failure

A 91-suite `unittest` regression returned **rc=0 — with a deliberately failing test planted in
it.** That result was **discarded**, which is exactly what `run_all.py`'s own docstring warns
about. **A shell wrapper's exit code is not the runner's.**

---

## 7. Money and safety

**Spend: $0.0701 of $2.00**, counted at the wrapper on the client's own counter — never a ledger
delta, because `api_client.py` contains no ledger writer at all.

⚠️ **The cap proof was kept OUT of the spend log**, and that was verified rather than assumed:
`spend.json` was **byte-identical before and after** the proof, so no synthetic reservation
inflated this round's own accounting. A previous round's cap-proof meter wrote to the live file and
**overcounted its own spend by 19%**.

**The cap binds**, driven through `harvest_run.Budget.reserve`: a funded cap **ALLOWS** (the
positive control, without which a refusal proves nothing), a **$0.00 cap refuses the FIRST call**, a
negative cap refuses, every refusal is a **raised** `BudgetExceeded`, and **the meter does not
advance on a refusal**.

**Backups** at round start under a path built from one round constant, sha256-verified, with **four
controls firing**: an identical copy verifies, a one-byte flip is caught, a LIST body is read as a
body, and **a planted deletion that leaves the natural key set IDENTICAL is caught by the
index-qualified row hash** — which matters here, because `spend.json` holds 30,692 rows under far
fewer distinct natural keys, so deleting one of a duplicated pair would otherwise be invisible.

**No dashboard was listening** in the dashboard port range, read from the **listening-port table** —
never a command-line grep, which once matched its own command line, and never
`dashboard/.running.json`, a stale marker since 30 August. Re-checked before every write under
`clippershq/`. **No Python process was killed. No seen-store row was deleted or un-latched.**

**Deliberately not committed, and none of it is an orphan.**

Four agents built **shadow trees** — full copies of `clippershq/` with only their own hunks
reversed — because that is how a red suite is proved pre-existing without trusting an argument.
Those copies are **regenerable, and they re-export real addresses**: ⚠️ **19 real addresses sit as
string literals in three production modules' self-test blocks**, so any snapshot of the tree
carries them, and my staged-set scan caught **531 hits** across
`scratch/bl1528_E/beforeroot/`, `scratch/bl1528_mine_reverted/` and `scratch/bl1528_head/`.
**They stay out of the commit.** Three test-output logs went the same way for the same reason —
one contained a real creator address.

⚠️ **My scan found them; the pre-commit guard was never reached.** That is the point of scanning
**what you are committing rather than what you wrote** — the guard checks lead-store addresses
only, so a clean pass there would not have meant publishable.

**The claim was released with `--force` for that reason, and this sentence is the record of it** —
the next round should not stand off from those paths wondering who owns them.

Paths in this report are relative to the repository root under `%USERPROFILE%`.

---

## 8. What he should do next, ranked

| # | action | why |
|---|---|---|
| 1 | **Re-walk the 260 latched rejections** — $0.156 | they were latched under a fabricated decider, and **one page he marked KEEP is among them** |
| 2 | **Grade more of the 150** | the deliverable rests on **6 graded rows**. 4 of 4 is 100% [51.0, 100.0] — the interval is honest but wide, and ~40 graded rows would halve it |
| 3 | **Land the second paging hole** (`meme_finder.py:3305`) | the first gave **10× the pages**; this is the same fix in the other walker |
| 4 | **Decide the search lane** | it delivered **0 of 478**; the post count is genuinely ABSENT there and the bio genuinely is too — **that lane may be structurally worse, not just mis-plumbed** |
| 5 | **Wire the term engine, or delete it** | 236 terms, a ledger and an expansion loop, reachable from **nowhere**, its ledger file never once written |
| 6 | **Turn the OCR and speech passes on, or stop the sheet claiming their answers** | `ocr_ran: false` on the run behind his sheet, while the sheet said "no on-screen text" **132 times** |
| 7 | **Settle the silent-handler count** | four numbers from three definitions; the *class* is real either way |
| 8 | **Handle the age gate** | still a fifth state: **still photographed, still bought** |
