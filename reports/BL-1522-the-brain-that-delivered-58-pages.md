# BL-1522 — TikTok edits delivered 58 pages at $1.64 per 1,000. The zero was an accounting error, twice.

**Round:** BL-1522 · **Date:** 2026-09-06 · **Spend: $0.00** — no vendor, billed or model call,
by me or by any of the five sub-agents. The cap was $2.00 and nothing was drawn against it.

**SAFE TO RUN: yes.** One production file changed, one hunk, verdict-neutral. The per-platform
judging fingerprint is byte-identical before and after (`a4d740102da431a6`), and its one-byte
flip control still fires, so that "unchanged" means something. No judging rule was added or
loosened and no threshold was moved.

---

## The headline answer

**TikTok edits never delivered zero. It delivered 58 pages across its four production runs, for
$0.095090 in 119.4 seconds — $1.64 per 1,000 delivered and 0.57 hours per 1,000, which meets
BOTH targets ($2.00 and 2 hours) and makes it the cheapest and fastest brain in the project.**
The zero was produced by two independent accounting errors, either sufficient alone. **First,
the TikTok run record has no mode field at all**, so the brain label was a hand-typed literal
guessed from the run id — and an id with no mode became the *default*, which is memes. **Two of
the three runs filed under `tiktok/memes` are EDITS runs by their own stamp, and 42 of the 58
edits deliveries were booked to memes** — so "the only target this project ever met" was met
substantially by the brain the same table declared dead. **Second, `delivered` for TikTok was
parsed out of a stop STRING that only exists when a run reaches its target**; a run that misses
target prints no such line and scores 0 by construction, which is exactly the state of the two
runs that were sampled. The pass counter was on disk the whole time, in 18 findings files, and
**nothing in the accounting chain reads them.** Is it fixed? The accounting error is now named
with its cause; the brain itself was never broken. **What is genuinely broken is that it has not
run since 29 August** — `config.json` has `tiktok_finder.mode = "memes"` — and that **his seven
configured edit search terms have never been searched**, because the edits branch passes the
wrong list.

---

## 1. What this round was asked to do

Find out why the TikTok edits brain has delivered zero pages, fix it, and prove it delivers.
Trace one page through and find the exact line where they die; measure the no-picture rate;
check the brief and the reject reasons; evaluate a free deterministic filter; count how many
edit pages are permanently latched; and re-run to prove delivery.

Five sub-agents ran in parallel and all five completed. **The premise turned out to be false,
so the round became a measurement of why it looked true.**

---

## 2. What shipped

**One hunk in `clippershq/tiktok_finder.py`, at the picture-judge recording site, plus
`tests/test_bl1522_model_why.py`.**

**The defect.** The free judge has captured the model's own sentence in a `model_why` field
since an earlier round, and the Instagram funnel reads it. **The TikTok funnel never did —
`model_why` appeared ZERO times in the file.** Measured consequence: **0 of 29 TikTok
confident-reject rows carry the model's own words**, every one carrying a funnel template
instead. **Positive controls fire on the other platform: 10/10 on instagram/edits, 350/700 on
instagram/memes, and 2,884 non-empty model sentences across 37 files.** So the question this
round was asked — *read what the model actually said about the pages it killed* — was
unanswerable on this platform.

**How it was proved.** Three controls, all green before the write: the verdict string is
**byte-identical** before and after; there is **exactly one** site in the file that records the
judge's output, which is what makes the fix **GENERAL** rather than local (no caller can
bypass it); and `model_why` went from **0 occurrences to 4**.

**The test is the artefact, not the proof event.** 8 tests, all 8 executed, passing **both
normally and under `python -O`** — the guards use `raise`, never `assert`, because `-O` strips
an assert and would disarm the check silently. One test is a **mutation control** that removes
the field from a copy and confirms the main assertion would have caught it.

**What was deliberately NOT shipped, in the same hunk.** The verdict string hard-codes the
MEME question — *"said this is not a repost page"* — and that text is emitted **on an EDITS
run**. It is wrong. It is also parsed by callers and tests, so changing it is a different kind
of change; it is reported here and pinned by a test so a later round changes it deliberately
rather than by accident.

---

## 3. What was measured

Every figure is **MEASURED**, **DERIVED** or **NOT VERIFIED**, with its denominator.

### 3.1 The delivery figures — MEASURED, re-derived three ways

| stage | edits (4 production runs) |
|---|---:|
| discovered videos | 274 |
| discovered **authors** | 260 |
| walked | 80 |
| captured | 58 |
| **entered the judge** | **2** |
| judged | 2 |
| paid | 58 |
| **delivered (pass counter)** | **58** |
| with an address | **4** |

**$1.64 per 1,000 delivered · 0.57 hours per 1,000** — from that corpus's own dollars and
seconds ($0.095090, 119.4 s). **Both targets met.** Re-derived from each run's own `billed_usd`:
**$1.62 against $1.64, 1.2% apart.** Delivery re-derived a second way from `is_target is True`
in the exported rows — a different structure — **agrees exactly on 18 of 18 runs**. A third,
independent check: sheet PNGs on disk equal keep-sheets plus reject-sheets **exactly, per run**
(27+4=31, 15+6=21, 14+0=14, 2+1=3).

**A wider census I ran myself**, including two benchmark runs outside production: **7 runs with
`run_mode.mode == "edits"`, 123 passing, 129 sheets built, 9 with an address, 4 appended to
master.** Both denominators are defensible; **58 is the production figure and 123 includes
benchmark runs**, and mixing them is how this went wrong in the first place.

**Quality, independently: on the one graded edits sheet he wanted 30 of 31 pages — 96.8%
[83.8, 99.4], the highest of the four brains.**

### 3.2 Why it read as zero — MEASURED, two independent causes

1. **The run record has no mode field.** All five TikTok records carry 24 keys and none is a
   mode. So the brain label in the pricing script is a **hand-typed string in a tuple**, guessed
   from the run id — and an id with no mode fell to the default, memes. **17 of the 25 pages
   credited to `tiktok/memes` came from runs that are stamped `edits` in their own exports.**
   ⚠️ Stated carefully, because the two claims are not the same: what is **measured** is that
   those deliveries were **booked to memes while their own run stamp says edits**. Since the run
   record carries no mode field, the label is **unattributable rather than provably wrong**, and
   a per-brain table built on it cannot be trusted in either direction.
2. **`delivered` was parsed from a success-only stop string** that interpolates the *target*.
   `passing` overshoots it (27 passes against a target of 15), and a run that never reaches
   target prints no line at all and scores **0 by construction**. Both sampled runs are in that
   state; they delivered **14 and 2**.

**The pass counter existed on disk the whole time** — 18 findings files, key `passing`.
**Nothing in the accounting chain reads them.**

### 3.3 The one live supply defect — MEASURED by runtime spy, found independently twice

`clippershq/tiktok_finder.py:3662` passes **the meme/quote list** where his edit list belongs:

```
searches, _search_src = _rm.edit_searches_for(blk.get("searches") or [], _mode)
```

His `editing_searches` is read at `:3642` and used **only on the `both` branch** at `:3669`. Two
agents reached this line independently, one by spy and one by source. **Driven, with his real
config:**

| call | terms returned | source |
|---|---:|---|
| shipped: `edit_searches_for(blk["searches"])` | **3** | the hard-coded fallback, which self-describes as *"NEW, NEVER RUN, NO MEASURED YIELD"* |
| fixed: `edit_searches_for(blk["editing_searches"])` | **2** | *"configured `searches`: 2 edit term(s)"* |

**overlap between the two results: 1 term.**

**⚠️ AND THIS IS WHY IT WAS NOT SHIPPED.** His `editing_searches` holds **7 terms**, but the
helper filters them for edit shape and only **2** survive — so the obvious fix returns **fewer**
terms than the fallback it replaces (2 against 3). **Passing his list is correct and would
reduce supply**, and the right change is probably the union, which alters what gets walked and
must be measured before it ships. A shipped comment in the same file saying both edit lists are
empty is **stale**: `editing_hashtags` is empty (0), `editing_searches` is not (7).

`tags_walked` is **0 on 4 of 4** runs — the edits hashtag lane is structurally empty because
`editing_hashtags` is `[]`.

### 3.4 The picture, and a defect nobody had found — MEASURED

**No judgeable picture: 1,404 of 2,709 walked pages = 51.8% [49.9, 53.7]** — *higher* than the
other platform's 40.1%, for a completely different reason.

| cause | k | % of 2,709 |
|---|---:|---:|
| **cut by a free rule before the camera ran** | 1,145 | 42.3% [40.4, 44.1] |
| courtesy reject sheet only, never judged | 148 | 5.5% |
| reached the camera, no cover source | 111 | 4.1% |

**private 0 · wall 0 · age gate 0 · unknown 0**, each [0.0, 0.3]. **That vocabulary is
architecturally Instagram-only** — TikTok pastes CDN cover bytes onto a canvas with no browser,
so a wall can neither become nor be observed as a sheet. **Positive control: the same classifier
finds 386 private, 310 walled and 145 unknown on the other platform.** TikTok's real causes are
**thin evidence (1–2 videos where 3 are needed): 701 = 55.8% [53.1, 58.5]**, recency 256, no
cover 111, view floor 81, share-per-play 60, language 47. **The camera refused 0 of 1,305.**

**The picture judge has been called 53 times, ever, against 1,305 available pictures — 4.1%
[3.1, 5.3].**

**What the model actually receives: 356 × 760 pixels**, captured by intercepting the request
body and raising before the send. A previously reported 155×275 crop **does not reproduce on the
page — that fix is live.** ⚠️ **But it was fixed on the page and NOT on the worked examples:
driven, all eight exemplars arrive at 155 × 275 — one panel of twelve, cut mid-panel.** It is
not firing today only because the minimum tile count on a judged picture is 3, which is held by
an evidence floor in a different module — **not by anything in the encoder.**

**Encode sizes: exemplars 215×460, page 356×760. The page arrives at 2.74x the pixel area of
every reference it is taught from.**

**Which pack this brain gets, established by opening the images:** all 8 exemplars are the
**pinned MEME pack** — matched by luma signature against a 164-file library, **8 of 8
unambiguous** (best match 0.222–0.386 against a runner-up of 36.4–56.8; matcher control
separates self 0.0 from other 43.7). **The edits pack is byte-identical to the memes pack.**
Meanwhile **60 edit reference sheets sit on disk**, 45 of them full 9-of-9 cells — **75.0%
[62.8, 84.2]**, measured per cell against the builder's own canvas colour read from source. They
are held back because his edit pack is **4 wanted / 0 reject** and a completeness check refuses a
want-only pack. ⚠️ A grey-16 blankness detector catches **0.0%** of that canvas and reports dark
footage as blank instead — **backwards**.

### 3.5 The brief — and the premise reverses under pairing

TikTok memes → edits differs in **exactly 2 of 20 content blocks**, both text: the brief grows
**4,918 → 11,546 bytes (+134.8%)** and a worked-examples header grows 58 → 389 bytes. **All 8
exemplar images are byte-identical between the two modes.** The edits delta is **86 whole lines
and is the identical set on both platforms — symmetric difference 0.**

**The negative control was built on whole lines because the obvious one cannot fail:** the word
"TikTok" appears **2/2/2/2** across all four briefs. The real control is 36 TikTok-only, 43
Instagram-only and 86 edits-only lines — **six assertions, all green, all falsifiable.**

**⚠️ The "edits brief is too permissive" premise reverses when tested on the same pages.** On 50
identical pages judged under all four briefs: TikTok **26/50 → 35/50 kills**, Instagram **19/50
→ 28/50**, discordant pairs 11 against 2, **McNemar exact p = 0.0225 on both platforms. The
edits brief is 18 points STRICTER.** A model-mix control strengthens rather than weakens it.

**What the model said about the pages it killed:** **24 of 35 TikTok-edits kills — 68.6% [52.0,
81.4] — name the absence of the "treated look".** A second independent corpus gives **104/173 =
60.1% [52.7, 67.1]** with a **negative control of 0/33 [0.0, 10.4]** on the memes brief. Both are
floors, because one matcher control is recorded as failing.

**His definition is present: 21 of 21 clauses at the wire, 0 of 21 in the memes brief.** The
subject list reads as **examples** five separate ways. ⚠️ **But 15 of those 21 clauses were added
after the only paired measurement — today's brief has never been scored.**

### 3.6 The free deterministic filter — MEASURED, and refused

`aweme_type` (TikTok's own video-versus-photo flag) is filled on **1,093 of 1,094 = 99.91%
[99.48, 99.98]** — "100%" is one record short — and has **0 production reads, 0 writes and 0
byte-level occurrences**, with controls firing on four sibling fields in the same dict literal.

**It should not ship as a gate.** There is **no threshold at which it kills nothing he wants**:
"any photo post" kills **6 of 14 wanted pages = 42.86% [21.38, 67.41]**, including two he scored
9. Even the strictest rule the field can express still kills a page he scored 6. **The direction
is inverted** — photo posts are *more* common on pages he wants (0.1019 against 0.0509). Kill
precision never exceeds a coin flip.

**Two caveats that decide it:** the field is **absent where the funnel actually stands** —
present on 65/65 records from the search endpoint, **0 of 74** from the hashtag endpoint, and
83.9% of seen pages came via hashtag. And **`duration` is already corrupt**: one key is written
from two dialects with no conversion, so the store holds **44.11% seconds and 55.89%
milliseconds**.

**The letterbox signal does not transfer to edit pages.** His 9–10s against his 6–7s on edit
pages: mean pad 0.0269 against 0.0291, **p = 0.8877, AUC 0.5648**; rank correlation **−0.1381
(p = 0.4874)**. **Positive control — the same instrument on a meme batch gives rho +0.6927,
p = 0.0001** — so the absence is real, not a broken instrument. The **meme** finding does survive
its confound control (pooled AUC 0.7608 → batch-stratified 0.7473, against a refuted case that
fell 0.6245 → 0.5464). **Edits-versus-memes as classes cannot be computed at all: 0 capture
batches hold both labels.**

### 3.7 The latch question, and the seen store — MEASURED

**2,518 rows. `passed` is False on 965 (38.3%)**, and on TikTok a picture-judge rejection is
final, so those are latched. **536 rows are unjudged; only 94 (3.7%) carry a verdict at all and
only 205 (8.1%) carry any reason** — so the reject side is largely undiagnosable from the store.

**⚠️ No row carries a mode or brain field of any kind.** So "which brain rejected this page" is
**not recoverable**, and attributing a stored row to the edits brain is an inference, not a
record. Discovery in the store is **83.9% hashtag / 16.1% search / 0% seed**.

A contradiction I chased and resolved: the store's hashtag majority appears to contradict
`tags_walked: 0`. It does not — **the store holds no rows dated the day those runs finished, so
they never wrote to it.** The two records describe **disjoint populations**; both are true.

---

## 4. What was refused, and why

* **Shipping the search-term fix.** It is correct and it *reduces* terms from 3 to 2. Supply changes must be measured, and this round could not run the measurement.
* **Shipping an `aweme_type` gate.** It kills 42.86% of his wanted pages and the effect runs the wrong way.
* **Quoting a kill rate against his marks for this brain.** He graded 30 pages and rejected exactly **one** — the negative class is n = 1. No confident number is available to anyone, and producing one would be the round's own criticism made flesh.
* **Changing the verdict string** that hard-codes the meme question on an edits run. Callers and tests parse it; reported and pinned instead.
* **Applying a peer's verified one-line patch to a file I held.** Their evidence looked good and two sessions had checked it — but I had not driven it, and my own check then *disagreed* with their anchor (§5). I handed the file back rather than shipping it.
* **A live 50–100 page re-run.** Not performed. Three previous attempts at exactly this were killed by an execution ceiling, and the round's delivery question was already answered from seven existing runs.

---

## 5. What I got wrong — the most useful section

* **I published "TikTok edits has never delivered a page" yesterday. It is false.** My source was an agent that found **2 runs, both aborted after 27 and 22 seconds**. **Seven exist.** That is the same failure as the `leads` denominator I had just finished congratulating myself for catching: a number that reproduces for the wrong reason because the population was wrong. I had it in my own output within a day of naming it.
* **I published the mode resolution backwards.** I claimed the funnel reads a top-level key and that his per-funnel keys are dead. **The opposite is true** — the funnel sets its config block to the per-funnel dict first, so the per-funnel key is the one that works and the top-level one is never read. Driven: per-funnel `edits` → `('edits', 'config')`. **My previous recommendation would have broken a working path.** My probe passed the wrong input and I published the result.
* **I told a peer their patch anchor was verified, before reading my own command's output.** My check then disagreed with theirs — 0 anchor matches against their 1, and 3 call sites against their 2 — and I sent a correction a minute later saying so. **Both of my numbers were wrong, and the resolution is more useful than the mistake.** A third session settled it by parsing both the committed blob and my working copy: **my "3 call sites" was 2 calls plus the function's own `def`** — a bare name search counts the definition, which is a counter bug anyone would hit. And **the anchor block is present exactly once**; my exact multi-line string match returned 0 on **formatting, not absence**. I had privately guessed line-ending conversion as the cause and that was also wrong — neither copy contains a single CRLF. **The real cause was my own edit**, which added lines above the block and moved it by 18 lines. The lesson is narrow and worth stating: **an exact-string anchor handed between sessions editing the same file is fragile by construction** — locate the exception handler by parsing, not by matching text.
* **My first re-derivation of sheets on disk looked for an `img/` subfolder** and reported 0 images against 58 declared. The sheets are at the top level of each run directory. Corrected, they agree exactly.
* **I printed a directory listing of a sheet folder to my own terminal, and those filenames are creator handles.** Nothing was committed or published, and I stopped listing those directories afterwards.
* **Sub-agents discarded four false zeros before publication**, each caught by its own control: a row field read under the wrong name (0 pictures against 1,232 on disk); a loose regex scoring one "age gate" from the words *"over 18 observed"*; a checkpoint directory that holds 0 TikTok records taken as "TikTok records nothing"; and a repo-wide grep that timed out and was replaced rather than trusted.
* **Two figures in the brief did not reproduce as stated:** "57 accounts carrying reference frames" measures as **60 sheets, 45 full**; and the widely-quoted $2.46 was **never a zero denominator** — it was measured on a live run with 18 delivered. Two instruments were conflated.

---

## 6. Money and safety

**$0.00**, from the run's own counter at the wrapper — never a ledger delta, which could not
attribute anything here in any case: the TikTok client books nothing at all to the ledger, so
every call it has ever made was invisible to it.

**The cap was proved to bind before any paid work was authorised**, by driving the TikTok
funnel's own `reserve()`: a zero cap **refuses by raising**, the meter **does not advance on a
refusal**, a non-zero cap allows the first call (the positive control, without which a refusal
proves nothing), and it refuses again exactly at the ceiling. The shipped source was asserted to
still contain the three statements the check assumes, and the raise was confirmed to sit
**before** the increment by byte offset.

**Data.** All eight protected files backed up and sha256-verified with **three** controls firing:
a one-byte corruption at identical size is detected; a **top-level list is read as a body** (the
case that once read 2,193 rows as 0); and **a deletion that preserves the distinct key
vocabulary is detected** — the case that collapsed a 28,805-row ledger to 781 distinct keys and
would otherwise have been invisible. At publication: **0 of 8 changed, all row key sets
identical.** The backup path is built from a single round constant.

**No verdict moved.** Per-platform judging fingerprint `a4d740102da431a6`, identical before and
after, with a one-byte flip in the rubric's own output text still moving it.

**Tests.** 8 new, all 8 executed, green **normally and under `-O`**.

---

## 7. What he should do next — ranked

1. **Set the TikTok mode to `edits` and run it.** It is one config value. The brain meets both targets and has not run since 29 August. This is the whole ask, and it costs nothing.
2. **Make the accounting read the pass counter.** 18 findings files hold it and nothing reads them; the brain label is a hand-typed literal because the run record has no mode field. Add a mode field and the whole class of error disappears.
3. **Give his edit pack a reject side.** Four wanted and zero rejects is why a completeness check falls back to the meme pack, so **60 reference sheets he supplied reach no judge at all.** This is the largest unused asset in the project.
4. **Decide the search-term list deliberately.** His seven configured terms are ignored today; passing them yields 2 terms against the fallback's 3. The union is probably right — measure it.
5. **Fix the `duration` unit collision** — one key written from two dialects, 44% seconds and 56% milliseconds. A correctness defect, invisible only because nothing reads the field.
6. **Fix the exemplar crop.** The page was fixed and the worked examples were not; they arrive as one panel of twelve. Not firing today, held shut by an unrelated floor.
7. **Do not ship an `aweme_type` gate, and do not tighten the edits brief** on the "too permissive" figure — it reverses under pairing.

---

## 8. Paths to open

Relative to the project root (`%USERPROFILE%\...\clipper finder`):

* `clippershq\tiktok_finder.py` — the shipped hunk at the picture-judge recording site
* `tests\test_bl1522_model_why.py` — 8 tests, green under `-O`, with a mutation control
* `scratch\bl1522_cap_binds.py` — the cap driven, four conditions and a positive control
* `scratch\bl1522_backup.py` — three firing controls including duplicate-preserving deletion
* `scratch\bl1522_agentA_trace.md` — the nine denominators and the supply defect
* `scratch\bl1522_agentB_picture.md` — the no-picture census and the decoded pixels
* `scratch\bl1522_agentC_brief.md` — the brief at the wire and the paired reversal
* `scratch\bl1522_agentD_awemetype.md` — the filter scored on his marks, and the letterbox control
* `scratch\bl1522_agentE_finding.md` — the two accounting causes

https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/BL-1522-the-brain-that-delivered-58-pages.md
