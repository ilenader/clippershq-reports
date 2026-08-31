# BL-1470 — the gate was shut, so nothing ran; and the judge sees a 155×275 crop

> ## IS THE FUNNEL SAFE TO RUN? **NO.**
> Two of six preconditions fail. The Instagram exemplar pack teaches the Instagram judge using
> **8 TikTok pages out of 8**, and the frame strip **never reaches the model** because no caller
> turns it on. The judge chain itself is alive. **No page was walked, no sheet was built, and
> $0.000691 of a $3.00 cap was spent.**

---

## 1. Round ID, date, and what it was asked to do

**BL-1470 — 2026-08-31.**

The round was asked to run **four batches of fifty pages** — TikTok memes, TikTok edits,
Instagram memes, Instagram edits, four separate "brains" that are never pooled — and to hand back
four sheets that can be **graded by eye, showing accepts AND rejects**, so a human can see what
the automated judge saw without opening every video. Budget **$3.00 total across all four**.

The brief opened with a blocking precondition: **do not start until two other concurrent rounds
have both declared the funnel safe**, and verify six specific things with a runtime spy and a call
count *before the first page*, because "if the judge chain is dead or the strip is unwired, this
run measures nothing and spends real money doing it." **If any check fails: stop and report, do
not spend.**

Two checks failed. Neither gating round declared safe. **So this is a verification report, not a
batch report.** No sheets exist to grade.

---

## 2. What actually shipped

**No production code was changed this round, by design** — the brief said *"do not add or loosen a
rule this round; this is a measurement run."* What shipped is the verification itself, plus the
report you are reading. Every check below was proved by a **runtime spy that counted actual calls
or read the actual bytes placed in the request payload** — not by a grep, not by a docstring, not
by a passing test.

| # | Check | Verdict | How it was proved |
|---|---|---|---|
| a | The picture judge is actually called | **PASS** | Replaced the model-call function at runtime and counted entries: 1 via the TikTok funnel's judge entry point, 1 via the free-judge reject path. Control fired. |
| b | The frame strip reaches the model | **FAIL** | See below. |
| c | The right brief reaches each of the 4 brains | **PASS** | Hashed the rubric **off the bytes actually placed in the payload**, not re-derived from source. All four match. |
| d | Exemplars are the right platform's | **FAIL** | See below. |
| e | A model answers | **PASS** | 4 of 5 chain models answered a live probe. |
| f | The rejection reason survives to the record | **PASS** | Scripted a model answer at runtime and read back what landed in the record. |

### (b) FAIL — the strip is unwired because *nothing turns it on*

`clippershq/tiktok_finder.py:2648` is the **only** production call to the picture judge, and it
**omits the `frame_strip` argument**. So it defaults to false, and `judge_page`
(`clippershq/tiktok_finder.py:3653-3657`) takes its other branch — which crops the sheet to a
single cover. The string `frame_strip=True` appears **exactly once in the entire package**, inside
the branch at `:3656` that no caller reaches.

**The guard itself is correct.** The failure is that it is **never exercised**.

### (d) FAIL — the Instagram exemplar pack is 8/8 TikTok pages

`meme_finder._exemplar_pack()`, fed to the reject gate at `clippershq/meme_finder.py:6326`,
returns eight example sheets whose file paths **all** sit under TikTok output directories.
**Zero Instagram.** It is teaching the model what a 10/10 *Instagram* page looks like using
*TikTok* pages, so two of the four requested batches would have been contaminated at the source.
The TikTok pack is correct (8 of 8 genuinely TikTok).

### (c) PASS — with a negative control

The four brains' rubric hashes were read back from the payload bytes and all four matched their
expected values, **all four differ from each other** (positive control — otherwise the check would
be blind), and a deliberately bogus platform name produced a **fifth, different** hash rather than
silently falling through to a real brain's rubric (negative control).

### (f) PASS — and this is the one that matters for the actual request

The ask was to grade **rejects**. That requires the model's own stated reason to survive into the
record. It does: a separate field carries the model's sentence alongside the machine-generated
reason string. Verified at runtime with three controls that all fired — a reject from a model
without cut authority is **kept** and says so; an approval does not drop; and **malformed JSON
from the model is recorded as UNJUDGED, never as a rejection.**

---

## 3. What was measured

All rates carry a **Wilson 95% interval** and a **named denominator**. Every figure is marked
**MEASURED** (observed directly) or **DERIVED** (computed from other figures).

### 3.1 What resolution the judge actually receives — the round's largest finding

The image encoder has two modes. The shipped call uses the one that **crops to the top-left cell
first, then caps the long edge at 760 pixels, and never scales anything up.**

Denominator: **901 recorded page-judging rows** carrying a tile count, across 116 result files.

| Tiles on the sheet | Rows | Share (MEASURED) | Wilson 95% | What reaches the model |
|---|---:|---:|---|---|
| 1 | 142 | 15.8% | [13.5, 18.3] | 427×760 — at the cap |
| 2 | 8 | 0.9% | — | 232×412 |
| 3 | 11 | 1.2% | — | **155×275** |
| 6 | 100 | 11.1% | — | **155×275** |
| 9 | 640 | 71.0% | [68.0, 73.9] | **155×275** |
| **3 or more (combined)** | **751** | **83.4%** | **[80.8, 85.6]** | **155×275** |

**MEASURED:** every sampled sheet on disk is 465×992 pixels (14 of 14 sampled, all above the 760
cap). **MEASURED:** encoding one of those sheets the way production does returns **155×275**
whenever the sheet holds 3 or more covers.

**So roughly four judged pages in five arrive at the model as a 155×275 image** — against the
427×760 the same cap would permit from the same file. **DERIVED:** that is 3.5× smaller on each
edge.

**Positive control:** a synthetic 2000×2400 image encodes down to 760 on the long edge, so the cap
demonstrably fires and these small numbers are genuine crops, not a broken measuring tool.

### 3.2 The same encoder destroys a "hero" sheet layout

A hero layout (one large frame beside small ones) is built at 585×760 — *at* the cap, unlike a
465×992 contact sheet. The crop divides by column count regardless:

| Encoder / argument | Hero sheet 585×760 | Production sheet 465×992 |
|---|---|---|
| Whole-sheet mode | 585×760 (whole) | 356×760 |
| Cropping mode, tile count unset / 3 / 4 / 9 | **195×346** | **155×275** |
| Cropping mode, tile count = 1 | 585×760 (whole) | 427×760 |

**MEASURED**, reproduced independently on two machines. **DERIVED:** wired the obvious way, a hero
sheet arrives at **0.152× its own area — an 84.8% loss** — sliced straight through the large frame
it exists to deliver. The symptom would be accuracy *worse* than baseline **with nothing in the
record explaining why**.

**This function has now failed this exact way twice.** Its own documentation records a previous
instance: a 311-pixel single-tile sheet was divided by three into a **103-pixel sliver** while the
report said "one thumbnail." The fix then was the same as the fix now — *pass the tile count* —
and the function grew a **warning in its documentation rather than a safer default**, so the trap
survived and caught the next design.

### 3.3 The exemplar packs, opened rather than counted

Denominator: **8 exemplar images** in the Instagram pack.

| Claim under test | Result | Wilson 95% |
|---|---|---|
| Pack is TikTok pages | **8/8 = 100% CONFIRMED** (MEASURED) | [67.6, 100.0] |
| "Five were 77-92% empty canvas" | **REFUTED** — worst is 16%; **0/8** exceed 70% (MEASURED) | [0.0, 32.4] |
| "One is the same cover pasted twice" | **REFUTED** — 8 distinct file digests, 0 duplicates (MEASURED) | — |

**Positive control:** a synthetic all-white image measures 100% blank, so the blankness detector is
not blind. **A claim can be right about which platform and wrong about everything else it
asserts**; the true part does not carry the false parts.

### 3.4 The model chain

**MEASURED**, live, one small image each: **4 of 5 responded** — 80.0% [37.6, 96.4].

The one dead model is the chain's nominal primary, retired by its vendor and returning HTTP 404.
**The consequence is specific and expensive:** cut authority is granted to exactly two models, and
that dead one is one of them. **So exactly one live model may reject a page, and it is the paid
one.** The free chain currently contributes **no rejections at all** — every cut is billed.

A concurrent round independently reports the paid model taking **591 of 591 rejections across four
runs**, with the dead model taking zero, which agrees.

### 3.5 Legibility — NOT MEASURED BY THIS ROUND, AND RETRACTED BY ITS AUTHOR

A concurrent round measured whether text can be read back at these sizes. **Reported here only
with its own retraction attached, because it does not support a conclusion:**

| Delivered size | Perfect reads | Wilson 95% |
|---|---|---|
| 585×760 | 5/8 = 62.5% | [30.6, 86.3] |
| 427×760 | 4/8 = 50.0% | [21.5, 78.5] |
| **155×275 (production today)** | **3/8 = 37.5%** | **[13.7, 69.4]** |

Monotone in pixel count — and **nothing separates**; the intervals overlap almost entirely at
n=8, under an answer key that agreed with itself only **6 of 8 = 75.0% [40.9, 92.9]**.

**The decisive number is not in that table.** The same author scored a composed sheet at 585×760
at **87.5%**, and a bare frame at the **same 585×760** at **62.5%** — a **25-point swing between
two runs of a nominally similar thing, larger than the entire effect being claimed.** The author
withdrew the legibility claim as *suggestive, not established*.

> **The honest state: text at 155×275 is NOT obviously unreadable** (3 of 8 perfect, several
> near-perfect). **The size effect is real in direction and UNMEASURED in magnitude.** Note the
> mirror-image error too: 37.5% [13.7, 69.4] is an interval containing both "fine" and "bad", so
> the correct label is **UNMEASURED, not PASSED.**

**The geometry in 3.1 and 3.2 does not depend on any of this.** It is arithmetic plus a row
census, reproduced on two machines. **It states what the model RECEIVES. It does not state what
the model can READ, and this round has no standing to claim the latter.**

---

## 4. What was refused, and why

**THE FOUR BATCHES WERE NOT RUN. NO SHEETS EXIST. THIS IS THE CORRECT OUTCOME, NOT A SHORTFALL.**

1. **The blocking precondition was never satisfied.** Both gating rounds were asked and neither
   declared the funnel safe. One is **actively rewriting the judge module** and opened with
   "nothing runs until the judge is proven alive." The other **held all model-dependent
   measurement** pending the first. Running fifty pages per brain through a judge another round is
   rewriting mid-flight would measure a moving target and bill for it.
2. **Two of six checks failed on their own merits.** Two of the four requested batches are
   Instagram, and the Instagram exemplar pack is entirely TikTok pages — those two batches would
   have been contaminated before the first page loaded.
3. **No rule was added, loosened, or "fixed" to get past this.** The brief forbade it and the
   failures belong to their owners.

**Not done, and named rather than quietly skipped:**

- **Legibility at 155×275 — NOT MEASURED by this round.** The only data is another round's,
  retracted by its author (§3.5).
- **Instagram-specific exemplars — NOT BUILT.** Fixing that pack is the owning round's work.
- **The frame strip — NOT WIRED.** Deliberately. Wiring it changes what the judge sees and
  therefore changes verdicts; nobody currently has the sample size to score that either way.
- **The 8 removed rows in one lead-tracking store — NOT RESTORED** (§6). Another round's writes
  are not this round's to revert.

---

## 5. What I got wrong

**The most useful section in the file.** Every failure that has cost anything in this project was
silent and plausible; every loud one was free.

1. **I searched for a function that never existed and reported its absence as a finding.** My first
   exemplar check asked the judge module for a loader by three plausible names. None exist — the
   module has no loader at all; the *callers* supply the packs. It returned "no exemplars" on all
   four brains, which looks exactly like a real and alarming absence. **Discarded that zero and
   re-ran against the real suppliers.** A zero whose control failed is not a result.

2. **I nearly published the same mistake a second time, at the very end of the round.** Verifying
   the configuration fingerprint the brief supplies, I tried six plausible serializations, none
   matched, and I drafted a paragraph stating the digest **could not be reproduced** and that no
   tool computes one. **Both claims were false.** The correct serialization was simply not among
   my six, and this repository documents the answer explicitly: the supplied digest and a second
   documented digest are **the same object** under default versus compact JSON separators. It
   reproduces exactly. **An incomplete candidate set produces a zero indistinguishable from a real
   absence — the identical failure to item 1, caught only because I checked the repository's own
   documentation before publishing rather than after.**

3. **I published a hazard as live when it is unreachable.** My spy reported that setting both
   relevant flags together "crops the strip away, 427×760 to 240×426." True of the encoder **called
   directly**, and **unreachable from the funnel**, because the caller guards it correctly.
   Testing a helper in isolation and reporting its behaviour as the system's is how a latent
   hazard gets published as a live one. **The real finding was the opposite shape: the guard is
   right, and never exercised.**

4. **I called a model dead on one empty response.** A prior round recorded one chain model as
   dead/empty. It answered in 2.33 seconds on a live re-probe. **It is intermittent, not dead** —
   "two of five are dead" should be read as **one dead, one flaky**. A single empty response is
   not a death certificate.

5. **I let two noisy numbers carry an inference, then wrote a conclusion on top of it.** I quoted a
   peer's 87.5%/62.5% and observed that 155 pixels sits below both points tested — arithmetically
   fine — and then closed my report to the operator with the line that at that size the sheets
   *"may not show you what you asked to see."* Those figures cannot survive their own run-to-run
   noise (§3.5). **That closing line went beyond the evidence and is withdrawn.**

6. **I had the seen-store timestamps backwards on first pass** and briefly reasoned from the wrong
   direction about which file was written when. Corrected by reading modification times directly
   rather than inferring them, and the conclusion changed (§6).

7. **A count I published is basis-dependent and I did not say so.** I earlier gave a playlist store
   as holding 1,878 entries; counting its top-level keys gives 3. Both describe the same unchanged
   file at different nesting levels. **Checksums are the reliable statement; my entry counts were
   not defined against a stated basis.**

**One thing that did NOT go wrong, because a peer warned in time:** the model-call function returns
a **plain string**, not a structured response object. A peer's first harness treated it as a
response object, crashed, and — because the error text then appeared identically in both the answer
key and every test arm — **scored every arm a flawless zero error rate.** A perfect result that was
a bug. My spy scripted it as a string throughout, so the check-(f) result stands.

---

## 6. Money and safety

**Spend: $0.000691 — 0.023% of the $3.00 cap.** **MEASURED by this round's own call counters**
(5 live calls: 4 free, 1 paid), *not* by a ledger delta. This is deliberate: the shared spend
ledger carries a round identifier on **zero** of its rows and concurrent rounds bill into the same
file, so a before/after difference measures other people's work as well as your own.

**Seen stores, re-verified at publication (not only at check time):**

| Store | At publication | Round-start checksum |
|---|---|---|
| TikTok pages seen | 2,446 entries | **identical** |
| Clip seen | 2,193 entries | **identical** |
| Playlists seen | unchanged | **identical** |
| Master leads file | — | **identical** |
| Configuration file | — | **identical** |
| **Meme pages seen** | **5,985** | **CHANGED — was 5,993** |

> **⚠️ One store shrank by 8 entries (8 removed, 0 added) mid-round — and it was not this round.**
> **Proved rather than asserted:** this round's backup is stamped 21:06:32 and the live file's
> modification time is **21:10:20**, i.e. it was rewritten *after* the snapshot; and the only two
> operations this round performed near that module leave the file's digest and size **unchanged**
> when run in isolation. A concurrent round independently confirms it made no such write either.
>
> **Two things deserve attention beyond the delta itself.** A seen store normally only grows. And
> **the removal did not update the file's own "last updated" field** — it reads the same value
> before and after — **so anything trusting that field would conclude nothing happened.** The 8
> removed rows still have checkpoint records elsewhere, so the change is recoverable.
> **Neither round restored it**: another round's legitimate writes are not ours to revert, and
> rolling one back to make our own delta read clean would be worse than reporting it.

**Configuration integrity: campaigns fingerprint `8e02f8d6f6307ae8` — UNCHANGED and reproduced**
(the same object also fingerprints as `7a029ee5447cddd8` under compact JSON separators; both are
documented and correct — **a bare hash is not a fingerprint, the encoding is half of it**).
Independently, the whole configuration file is **byte-identical** to its round-start checksum.

**Disk: 399.87 GiB free of 930.58 GiB at publication.** No abort threshold approached.

**Processes: nothing was killed.** No process was terminated, no server restarted, and nothing was
written into the dashboard or package directories while other work was live.

**Secret scan: this file was scanned by reading its bytes**, not by enumerating changed paths from
version control — a previous self-scan reported a directory clean *without looking inside it*,
because the directory listed as a single entry. **All six patterns caught a known positive control
first**, so the zeros are real rather than a broken regex. **Result: 0 email addresses, 0
key-shaped literals, 0 street-address-shaped strings, 0 wallet-shaped strings, 0 absolute paths
containing a username, and 0 C0 control bytes.** The control-byte assertion runs **before**
publication, not after. Nothing was bypassed.

---

## 7. What to do next — ranked, with the arithmetic

**1. Fix the Instagram exemplar pack before running any Instagram batch. (Blocking, cheap.)**
It is currently 8 TikTok pages out of 8. Two of the four batches you asked for are Instagram, so
**half the run is contaminated at the source until this changes.** This costs nothing but the work
of selecting real Instagram examples you consider 10/10.

**2. Make the cropping encoder safe by default rather than by documentation. (Blocking-ish, small.)**
It has now caused the same silent shrink **twice**, and the previous fix was a documentation
warning that did not prevent the second occurrence. Two available shapes: **require the tile count
when the cropping mode is on**, or **default the column count to 1 when the tile count is absent**.
Routed to the round that currently owns that file as a finding, deliberately with no preferred
shape.

**3. Decide the resolution question with a real measurement before wiring anything. (Do this
before spending the $3.00.)**
Today 83.4% of judged pages arrive at **155×275**. The same file could deliver **427×760** by
passing the tile count, and a hero layout could deliver **585×760** — **3.77× the width and 10.43×
the area** of what ships today. **But nobody has measured whether that buys accuracy**, and the one
attempt produced a 25-point swing between two runs of the same thing (§3.5). **Do not wire on the
current evidence.** The cheap decisive experiment is the existing one at a larger n, with the
answer key's own self-agreement reported alongside — it was only 6 of 8, which caps anything
measured against it.

**4. Then, and only then, run the four batches.**
The requirement you actually care about — **grading the rejects** — is already met: the model's own
sentence survives into the record, verified at runtime (§2f). Once items 1-3 land, the batches
become worth their money. At the observed cost profile, this round's verification consumed 0.023%
of the cap, so **the full $3.00 remains available.**

**5. Note that every rejection is currently billed.**
Cut authority sits with two models; one is retired and returns 404. So exactly one live model may
reject, and it is the paid one — **the free chain contributes no rejections at all.** That is a
standing cost you may not have priced.

---

## 8. Paths to open

Written with `%USERPROFILE%`, which **File Explorer expands automatically when pasted into its
address bar** — this keeps a username out of a public document while remaining directly pasteable.

| What | Path |
|---|---|
| This round's full working report | `%USERPROFILE%\OneDrive\Desktop\clipper finder\reports\BL-1470.md` |
| The runtime spy — checks (a)(b)(c)(d) | `%USERPROFILE%\OneDrive\Desktop\clipper finder\scratch\bl1470_spy.py` |
| The runtime spy — checks (e)(f) | `%USERPROFILE%\OneDrive\Desktop\clipper finder\scratch\bl1470_spy2.py` |
| The exemplar opener, and its results | `%USERPROFILE%\OneDrive\Desktop\clipper finder\scratch\bl1470_exemplars.py` |
| The encoder measurement (3.1, 3.2) | `%USERPROFILE%\OneDrive\Desktop\clipper finder\scratch\bl1470_whatreaches.py` |
| The publication byte-scanner used on this file | `%USERPROFILE%\OneDrive\Desktop\clipper finder\scratch\bl1470_pubscan.py` |
| The judge module (read-only this round) | `%USERPROFILE%\OneDrive\Desktop\clipper finder\clippershq\free_judge.py` |
| The only production judge call — line 2648 | `%USERPROFILE%\OneDrive\Desktop\clipper finder\clippershq\tiktok_finder.py` |
| The Instagram exemplar supplier — line 6326 | `%USERPROFILE%\OneDrive\Desktop\clipper finder\clippershq\meme_finder.py` |

**No port numbers are given deliberately** — they are not stable between runs, and a previous
grading session was lost to a bookmarked one. Start the sheet server from its own launcher and use
whatever port it prints at the time.

---

*Round BL-1470 closed 2026-08-31. Four batches requested, none run, gate shut on two failed
preconditions. $0.000691 spent of $3.00. No production code changed.*
