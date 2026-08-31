# BL-1471 — the Instagram judge is taught with TikTok pages, and correcting that changes nothing measurable

> ## IS THE FUNNEL SAFE TO RUN? **NOT CERTIFIED — but this round found no new blocker.**
> The defect this round was sent to fix is **real and confirmed**: the Instagram brains learn what
> a 10-of-10 Instagram page looks like from **8 TikTok pages out of 8**. It is also, on 50 held-out
> pages and 100 live calls, **not costing any measurable accuracy** — both packs score identically.
> The judge itself answered **100 of 100 calls with 0 unjudged**. Whether the funnel as a whole is
> safe is a separate round's verdict and **it has not reported yet**; nothing here overrides that.

---

## 1. Round ID, date, and what it was asked to do

**BL-1471 — 2026-08-31.**

The round was asked to fix one specific defect: the picture-judge "exemplar pack" — the worked
examples shown to the model so it knows what a good page looks like — contains **eight TikTok pages
and zero Instagram pages**, yet it is what teaches both Instagram brains. The instruction was to
map every supplier properly (a previous round had published a false absence here), build
platform-correct and mode-correct packs from the operator's **own graded pages**, keep the packs
honest and de-identified, **then measure whether any of it actually helps**, and finally report what
the examples look like by the time the model receives them. Budget **$0.50**, most of which needed
no vendor call because the pages were already on disk.

**Spent: 100 vendor calls, 18.6% of the cap.** The defect is confirmed. The fix is built. **The
measurement says the fix buys nothing**, and that is the honest headline.

---

## 2. What actually shipped

Every claim below was proved by a **runtime spy that counted real calls and decoded the actual
bytes placed in the request**, or by an **AST parse** — not by a grep, not by a docstring, not by a
passing test.

| # | Item | Where | How it was proved |
|---|---|---|---|
| 1 | Exemplar suppliers mapped for all four brains | `tiktok_finder.py:371`, `meme_finder.py:4369` | AST parse for the keyword argument at every call site, then both packs resolved live |
| 2 | The pack really does reach the model | `free_judge.should_reject` | Spy captured the payload: **9 images with the pack, 1 with an empty pack** — negative control fired |
| 3 | Proposed Instagram pack, 4 wanted + 4 rejected | built from his marks | Every score re-derived a **second way** from raw mark files without the shipped reader: **8 agree, 0 disagree** |
| 4 | Approval gate in front of the pack | `meme_finder.py` | 6 tests including a **mutation control** that fails if the new argument is ignored |
| 5 | Paired measurement, 100 live calls | — | 0 unjudged, 0 overlap between test set and either pack |

**Exactly two exemplar suppliers exist in the whole package**, and **neither takes a mode**. So
**four brains share two packs**: one for TikTok (both its modes) and one for Instagram (both its
modes). The Instagram one resolves 8 of 8 to TikTok output directories. **The TikTok pack is
correct — 8 of 8 genuinely TikTok — and was not touched.**

---

## 3. What was measured

Every rate carries a **Wilson 95% interval** and a **named denominator**. Figures are marked
**MEASURED** or **DERIVED**.

### 3.1 The headline: correcting the pack changes nothing measurable

**Paired design** — the same page, the same brief, the same model, **only the pack changing**.
Denominator: **50 held-out pages** (25 he scored 9–10, 25 he scored 1–2), **100 calls**, **0
unjudged**, **0 overlap** between the test set and either pack.

| Arm | Kills of his 9–10s | Wilson 95% | Catches of his 1–2s | Wilson 95% | Accuracy |
|---|---|---|---|---|---|
| **OLD** (8/8 TikTok, shipped) | **0/25 = 0.0%** | [0.0, 13.3] | 11/25 = 44.0% | [26.7, 62.9] | **36/50 = 72.0%** [58.3, 82.5] |
| **NEW** (8 Instagram, proposed) | **0/25 = 0.0%** | [0.0, 13.3] | 11/25 = 44.0% | [26.7, 62.9] | **36/50 = 72.0%** [58.3, 82.5] |

**McNemar on the paired disagreements: χ² = 0.250 on 4 discordant pairs — NOT SIGNIFICANT** at
p=0.05. **MEASURED.** Four pages did flip verdict, **two in each direction, every one a page he
scored 1** — a real change in individual decisions with a net effect of zero.

**CONSTANT-ANSWER BASELINE, WITH ITS SCOPE NAMED:** this test set is **balanced 25/25 by
construction**, so its constant answer is **25/50 = 50.0% [36.6, 63.4]** on *these 50 pages*.
Three other baselines exist in this project (61.5% on 1,791 pages; 82.0% on 9,182; 83.3% on a full
sweep) and **none of them is quoted beside the figure above** — they describe different
populations, and pairing one with a figure from another manufactures a win.

**HIS OWN CEILING: his marks are 75.8% self-consistent [68.4, 82.0].** Nothing scored against them
can exceed that, so **72.0% is already at the ceiling** and there is very little headroom for any
pack to win.

> **⚠️ THE 95% SAFETY BAR IS NOT DEMONSTRATED, IN EITHER ARM.** Keeping 25 of 25 wanted pages is
> 100% — but the interval is **[86.7, 100.0]**, and the **lower** bound is 86.7. **At n=25 that bar
> cannot be certified either way**, and this round does not claim it. Certifying it needs a larger
> held-out set, not a better pack.

**Honest prior:** swapping all eight exemplars was already measured as **not significant across
four rounds (McNemar 0.00)**, while merely *paraphrasing the rubric* killed 2 of 34 wanted pages —
the wording carries the result, not the pictures. This round was the first **Instagram-for-Instagram**
swap, which is why it was worth running. **It did not change that conclusion.**

### 3.2 What his marks can and cannot build

Denominator: **683 raw marks → 537 distinct pages** after last-keystroke-wins. **89 pages were
re-marked; the most re-marks on a single page was 9.** **MEASURED.**

The mode is **never written into a mark** — the normaliser returns nothing on all 683 rows,
**verified** — so memes-vs-edits survives only in directory names.

| Brain | Marked pages | Scored 9–10 | Scored 1–2 | Balanced 4+4 pack? |
|---|---:|---:|---:|---|
| instagram/memes | 220 | 40 | 113 | **YES — built** |
| instagram/edits | 21 | **2** | 11 | **NO — only 2 wanted exist** |
| tiktok/memes | 264 | 55 | 78 | yes (not needed; its pack is already correct) |
| tiktok/edits | 30 | 20 | **0** | **NO — zero rejected examples exist** |

**Two of the four brains cannot have a balanced pack built from his marks at all.** That is stated
rather than padded out with substitutes.

### 3.3 What the examples look like by the time the model sees them

Measured by **decoding the base64 actually placed in the request**, never by reading the file on
disk. **The encoder gives exemplars a smaller size limit than the page they are teaching about.**

| Path | Exemplars arrive at | Page arrives at |
|---|---|---|
| Instagram (whole-sheet mode, ~83% of pages) | **215×460** | 356×760 |
| TikTok (its judge always uses single-cover mode) | **155×275 — cropped to ONE cell** | varies |

**DERIVED: an Instagram exemplar reaches the model at 60.5% of the page's long edge.** On TikTok
the exemplars are cropped to a single cover **in both the 9-tile and 1-tile cases**. The proposed
Instagram grids are tall (up to 1720×3031) and arrive scaled to **×0.152–×0.260** of their original
width. Controls fired: an empty pack yields exactly 1 image, adding one synthetic exemplar yields 2.

**The encoder was NOT changed** — another round owns it and it is a spend decision.

### 3.4 Keeping the pack honest

- **Leak check FIRED**: 27 handles across **9 of 15** briefs, against a corpus of **7,305 marked
  handles**. Against that live check, **my 8 proposed exemplars leak 0** — and they *are* in the
  mark corpus, so the check **could** have fired on them. **An earned zero, not a dead check.**
- **One candidate the operator scored 10 was disqualified for being 91% blank canvas.** This is a
  *candidate*, and is **not** evidence for the refuted claim below.
- Repeat-detector and blank-detector each proved on a synthetic positive before any zero was
  trusted.

---

## 4. What was refused or not done

1. **THE CODE CHANGE IS COMMITTED — but only after a claim conflict I had to resolve carefully,
   and a peer caught something I had missed.** The file it touches sat inside a **second live
   claim** belonging to a round that had been **untouched for 32.9 hours**. When this round was
   filed the project's tool *granted* a takeover because the file was clean — but **a takeover
   does not narrow the older claim**, so the pre-commit guard correctly refused a commit spanning
   two rounds. **The guard was right and was not bypassed.** I committed the evidence separately
   and asked a live peer before touching anything.

   **The peer's warning changed what I checked.** That stale claim declared **two** files, not
   one, and the second had **136 uncommitted insertions**, including a **+106-line hunk inside the
   TikTok exemplar-pack function** — which looks exactly like this round's work. **It is not
   mine.** The added lines carry **six markers from a different round and none from this one**, and
   their content is vendor pagination work matching that round's declared intent, while my own
   change carries this round's markers. **I verified that before deciding, rather than asserting my
   own innocence.** Only then did I release the abandoned claim — **a decision, recorded with its
   full rationale** — having confirmed that **both files remain protected by live claims
   afterwards**, and I did not revert, restore, or touch the other round's file.

2. **NOTHING WAS PROMOTED INTO THE SHIPPED PACK.** The funnel may propose and may never promote —
   the model's confidence has never predicted his approval. The new approval list ships **empty**,
   so today every caller gets **byte-identical** output to before and **no verdict moves**.
3. **Mode-specific packs for two brains — NOT BUILT**, because his marks cannot support them (§3.2).
4. **A mode-aware TikTok pack — NOT ATTEMPTED.** It would require a file inside another live round's
   claim.
5. **Emails burned into exemplar frames — NOT MEASURED.** The OCR library imports but its engine
   binary is absent, so no text was read. The email pattern itself is proven (it fires on 2 of 47
   real non-empty biographies) — **but a proven pattern with nothing to read is not a measurement**,
   and installing an OCR engine was out of proportion to the round.
6. **"Prints its own handle" — NOT MEASURED for this cell.** A prior round recorded that flag for 64
   Instagram *edit* pages (4 flagged); those are not the pages proposed here.
7. **The full test suite — DELIBERATELY NOT RUN.** Another round has it running, and one test
   asserts on a shared name prefix, so a concurrent run would collide. My own 6 tests pass.

---

## 5. What I got wrong

**The most useful section, and every item here was caught by a control rather than by luck.**

1. **My mark reader returned zero scores and a zero/zero want-split, and I nearly reported it.**
   The control I had written — "if either side is 0 the reader is broken" — fired immediately. The
   cause was mine, not the data's: **the score field is a floating-point number and I tested it for
   integers**, so all 421 scored rows were silently rejected; the want field has a different name
   than I assumed; and the platform field is **empty on 101 marks**, needing a fallback to the
   source directory. Fixed, and the corpus then read 492 of 537 scored.
2. **I reported "0 leaked" from a check that had not looked.** I walked the leak tool's JSON for
   key names I guessed, found none, and printed a self-contradictory line claiming the tool "fired
   (0 leaked)" — while the tool had plainly printed 16 leaked handles to the screen. **A zero and a
   confirmation of the zero, both produced by my own parser guessing.** Redone against the real
   structure: 27 handles across 9 of 15 briefs.
3. **I searched for biographies in files that have no biography field** and got 0 of 28 and 0 of 21.
   Those records carry abbreviated keys and **no bio at all**. Discarded, and a real corpus found.
4. **I claimed all sampled sheets were 465×992.** True of the *current* pack's sheets; the proposed
   Instagram grids are **1720×1784 and larger**, which is exactly why they scale down so much harder
   (§3.3). The generalisation was too broad.
5. **My first commit attempt failed on a filename I invented** (a scanner named for the wrong round)
   which aborted the whole staging operation — and then I initially misread the resulting refusal as
   a mixed index, when the real cause was the stale claim (§4.1).
6. **A background job I started scanned the entire repository and had to be abandoned**; the same
   answer came from a scoped search in seconds. Later, the mark reader's default walks the whole
   tree and timed out at 300 s for the same reason.

7. **I reported a test suite as passing after running one of its three files.** A peer named a
   red suite; I ran the file whose name I recognised, saw "12 tests OK", and told them it passed
   cleanly. There are **three** files sharing that prefix and **the one I did not run is the one
   that fails**. This project already records the lesson that a shared prefix is not a suite; I
   repeated it anyway. **Two red suites come from a single stale artefact**, and the peer's count
   was right where mine was wrong.

**Not an error, but worth recording:** a peer's report reached me addressed to a different round.
I redirected it rather than letting a real defect evaporate, and the peer confirmed the file it
named is now in **nobody's** claim.

---

## 6. Money and safety

**Spend: 100 vendor calls by this round's own counter.** The shared ledger moved **$0.093183**
across the same window — **18.6% of the $0.50 cap** — but **that delta is not this round's spend**:
the ledger carries a round identifier on **zero** rows and concurrent rounds bill into the same
file. The call count is the honest figure; the dollar figure is an upper bound that includes
whatever peers spent alongside.

**Integrity at publication — re-verified at publication, not only at check time:**

| File | Result |
|---|---|
| Configuration file | **byte-identical** |
| Campaigns fingerprint | **`8e02f8d6f6307ae8` — unchanged** |
| TikTok pages seen · playlists seen · clip seen | **byte-identical** |
| **Master leads file** | **CHANGED (grew)** |
| **Meme pages seen** | **CHANGED (grew)** |

> **Both changed files were IDENTICAL mid-round and had changed by publication — and it was not
> this round.** Proved rather than asserted: **importing the modules changes neither**, and **a
> judge call changes neither**, tested directly. Both **grew**, which is what a peer discovering
> pages looks like. **Not restored** — another round's legitimate writes are not mine to revert.
> This is exactly why the delta is re-checked at publication: mid-round it read clean.

**Processes: nothing was killed.** All four of his servers held **identical process IDs before and
after** the only file write. The watcher that supposedly restarts on any such write **is not running
at all** — its state file is absent — which I verified myself rather than accepting on a peer's
word.

**Disk: 378.38 GiB free at the start, 362.77 GiB at publication.** Re-read before the write phase.

**Secret scan: this file was scanned by reading its bytes**, with **every detector proving itself on
a known positive first**, and the control-byte assertion running **before** publication rather than
after. **Result: 0 email addresses, 0 key-shaped literals, 0 wallet-shaped strings, 0
street-address-shaped strings, 0 absolute paths containing a username, 0 C0 control bytes.** **No
creator handles appear anywhere in this document** — this round worked directly with his graded
pages, and every page is referred to by score and class only. The saved example images are named by
class and score, never by page name, and live outside version control. Nothing was bypassed.

---

## 7. What to do next — ranked, with the arithmetic

**1. Decide whether you want the Instagram pack corrected at all. (Your call, and it is genuinely
close.)**
The defect is real: your Instagram judge learns from 8 TikTok pages. But on 50 held-out pages the
corrected pack scored **exactly the same — 36/50 both ways** — and the four pages that moved
cancelled out. Your marks are only 75.8% self-consistent, and both packs already score 72.0%, so
**there is roughly three points of headroom in total and no evidence the pack captures any of it**.
Correcting it is *right*; expecting it to buy accuracy is not supported.

**2. If you do want it, approve or reject the eight proposed pages — it takes minutes.**
They are saved as pictures named only by class and score. Four are pages you scored 9, four you
scored 1–2, all drawn from your own marks, none used in any scoring set. **Nothing changes until you
say yes**: the approval list ships empty and the code refuses any page not on it.

**3. Look at what the model actually receives, because you never have.**
Your examples reach the model at **215×460** while the page it is judging arrives at **356×760** —
the examples are **smaller than the thing they are teaching about**. On TikTok they are **cropped to
a single cover**. Both sets of images are saved for you. **This is a bigger lever than which pages
are in the pack, and nobody has measured it.**

**4. Fix the operator-facing help text that contradicts the code.**
One settings description still tells you the TikTok judge never receives worked examples. That was
true, was fixed some rounds ago, and **the description was never updated** — so the interface
asserts the opposite of the wiring. It is in no round's claim and will keep rotting.

**5. If you want the 95% safety bar certified, the lever is sample size — and you are closer than
anyone thought. (ADDED AFTER PUBLICATION.)**

Two rounds have now independently failed to find headroom in the model layer: this one found the
pack makes no difference, and a concurrent round found that agreement *between* models (85.8%) is
indistinguishable from one model agreeing with *itself* (84.4%). Both bottom out in the same
place — **the sample is too small to answer the question**, not the model or the examples.

But "there aren't enough marks" turns out to be **too pessimistic**, and I checked rather than
repeating it. Counting your marks after last-keystroke-wins: **127 pages scored 9–10 and 175
scored 8–10 exist.** At **zero kills**, the Wilson lower bound on safety by sample size is:

| Scored 9–10 available | Lower bound at 0 kills | Certifies ≥95%? |
|---|---|---|
| instagram/edits — 2 | [34.2, 100] | no |
| tiktok/edits — 20 | [83.9, 100] | no |
| **this round's test set — 25** | [86.7, 100] | no |
| instagram/memes — 40 | [91.2, 100] | no |
| **tiktok/memes — 62** | **[94.2, 100]** | **just short** |
| all four pooled — 127 | [97.1, 100] | yes |

**So no single brain can certify the bar on its own today — but TikTok/memes is roughly eight
graded pages short of it.** That is the cheapest outcome available anywhere in this report: **you
already own the pages, they are on disk, and grading about eight more of them converts an
uncertifiable gate into a certified one for that brain.** Instagram/memes needs about thirty more.

**One caveat I will not paper over:** the pooled row certifies *the gate in aggregate*, not any
brain you would actually run — and this project's standing rule is that the four brains are never
pooled. Pooling marks to state a safety floor is a different act from pooling brains to judge, but
it is still a weaker claim than a per-brain certificate, and should be labelled as such wherever
it is quoted.

> **⚠️ AND A LARGER WARNING, ADDED AFTER PUBLICATION, BECAUSE A CONCURRENT ROUND NEARLY SHIPPED
> THE OPPOSITE CONCLUSION.** It is tempting to enlarge the sample by sweeping every mark-like file
> in the project rather than only your grading sheets. **That count is not your judgement, and
> building it destroys your judgement.** Measured with the shipped reader:
>
> - Sweeping the tree yields **18,203 pages and 1,968 "wanted"** — against **469 pages and 187
>   wanted** in your actual grading sheets.
> - **The single biggest contributor of "wanted" pages is a backup copy of a *seen store*** — 336
>   pages from one file. A seen store records what the funnel *encountered*, not what you want.
>   The rest of the top sources are run extracts, generated datasets, and a backup of a
>   review-marks file this project already documents as circular.
> - **Worse: the resolver is last-write-wins across whatever it is given. All 469 of your graded
>   pages end up resolved from some other file, and on 58 of them the want/not-want answer
>   REVERSES** — your sheet says you did not want the page; the pooled corpus says you did.
>
> **So a bigger corpus assembled that way is the funnel counting its own memory, and it overwrites
> you.** Every figure in the table above is built from your grading sheets only, deliberately. Any
> future "we have thousands of marks" claim should be asked which files it swept.

---

## 8. Paths to open

Written with `%USERPROFILE%`, which **File Explorer expands when pasted into its address bar** —
this keeps a username out of a public document while staying directly pasteable.

| What | Path |
|---|---|
| The 8 proposed pictures, full size | `%USERPROFILE%\OneDrive\Desktop\clipper finder\output\bl1471_proposed_pack` |
| The same 8 **as the model would receive them** | `%USERPROFILE%\OneDrive\Desktop\clipper finder\output\bl1471_proposed_as_sent` |
| The **current** pack as the model receives it | `%USERPROFILE%\OneDrive\Desktop\clipper finder\output\bl1471_exemplars_as_sent` |
| This round's full working report | `%USERPROFILE%\OneDrive\Desktop\clipper finder\reports\BL-1471.md` |
| The paired measurement and its raw rows | `%USERPROFILE%\OneDrive\Desktop\clipper finder\scratch\bl1471_paired.py` |
| The proposal and its disqualifiers | `%USERPROFILE%\OneDrive\Desktop\clipper finder\scratch\bl1471_propose.py` |
| What the exemplars arrive as | `%USERPROFILE%\OneDrive\Desktop\clipper finder\scratch\bl1471_arrives.py` |
| The Instagram exemplar supplier | `%USERPROFILE%\OneDrive\Desktop\clipper finder\clippershq\meme_finder.py` |
| The TikTok exemplar supplier | `%USERPROFILE%\OneDrive\Desktop\clipper finder\clippershq\tiktok_finder.py` |

**No port numbers are given deliberately** — they are not stable between runs, and a grading session
was once lost to a bookmarked one. Start the sheet server from its own launcher and use the port it
prints at the time.

---

*Round BL-1471 closed 2026-08-31. Defect confirmed, fix built and tested, measured effect zero.
100 vendor calls, 18.6% of a $0.50 cap. No verdict moved and no rule was added or loosened.*
