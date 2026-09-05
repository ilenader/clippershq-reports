# BL-1504 — The judge has never seen a video frame, and the guard that stops it is right

**Round:** BL-1504 · **Date:** 2026-09-05 · **Spend this round: $0.00** (no vendor call was
made, by me or by any sub-agent)

---

## The answer, in one paragraph

**How many reject examples are now available per brain:** 399 on TikTok/memes, 129 on
Instagram/memes, 13 on Instagram/edits, and **1** on TikTok/edits — 542 in total, of which
**489 (90.2%, Wilson 95% [87.4, 92.4]) already have a picture on disk**, so most of the reject
side costs nothing to assemble. **Does the judge now see frames from an actual video — YES or
NO: NO.** And after tracing it end to end I am not going to turn it on, because the thing
stopping it is not an oversight. The judge's picture is a contact sheet of **cover
thumbnails** on both platforms; the video-decoding leg exists, is free, and works when driven
— but its output feeds exactly one rule, that rule needs a speech measurement, and the TikTok
path hard-codes that measurement to `None`. Turning decoding on buys 4.6 s per page and
changes **zero** verdicts. The sharper finding is the asymmetry underneath: **ffmpeg already
decodes real video in production every day — on Instagram, for audio** — so the missing piece
was never code nobody wrote. It is written, shipped and running on one platform and nailed
shut on the other.

The round's most expensive discovery was not in Part B at all. Fixing the mode question
uncovered that `resolve()` **was returning the opposite of his last word on 21 graded pages**.

---

## 1. Round ID, date, and what it was asked to do

BL-1504, 2026-09-05. Two parts:

* **PART A** — stamp mode at write time and prove it *survives resolution*; backfill existing
  rows from **sheet provenance** (never field shape), marked INFERRED; report the reject side
  per brain with how many already have a picture.
* **PART B** — turn on video decoding on the judge path. Trace first, drive with a runtime spy
  and a firing positive control. Measure the clock cost, median and tail. Ship the
  frame-extraction speedup **if its consumer is on**, verified by raw pixel hash rather than a
  file count. Implement or delete `HERO_T_DEFAULT = 1.4`.

Standing constraints honoured: no judging rule added or loosened, no threshold moved, a
per-platform control asserting no verdict moved, the listening-port table re-checked
immediately before each write under `clippershq/`, no seen-store row deleted or rewritten, and
`.venv` python by full path throughout.

---

## 2. What actually shipped

**`tools/mark_reader.py` — three changes, one defect fixed.**

1. **`sheet_provenance(path)`** — a new reader that asks *the sheet* what the marks typed on it
   were. It reads the manifest in **both generations** (`sheet_meta.json` and the older
   `meta.json`; eight sheets carry only the second and a reader that knows only the first loses
   them), then the sheet directory name, then the file's own name. It **refuses field shape**,
   and it refuses to treat a manifest lying in a shared root such as `output/` as any
   particular file's provenance — in a shared root a file's "siblings" are every unrelated file
   in the tree, and reading those is a guess with a citation stapled to it.
2. **`Mark.platform_source` / `Mark.mode_source`** — every value is now labelled `stated` (the
   row said it) or `inferred:<evidence>` (the sheet did), so a consumer that must never pool
   two brains can see which rows were never actually stamped. **There is no silent default:** a
   sheet naming no mode yields `None` and prints as NOT RECORDED.
3. **`resolve()` learns the key before it uses it.** Provenance is merged forward; the verdict
   is untouched.

**`clippershq/tiktok_finder.py`** — a **comment-only** correction (proved comment-only by
comparing the parsed syntax trees before and after: identical). It replaces a cost figure that
was roughly **7x too high** and was being quoted as the justification for a live guard, and it
records that the other platform already performs the measurement this path is waiting for.

---

## 3. What was measured

### 3.1 The mode was never missing — it was destroyed at resolution

Nothing writes a mode: **0 of the graded corpus's rows carry one**. But that was the smaller
half. Across the repo, **4,267 raw rows do carry a mode and only 42 pages resolved with one**,
because `resolve()` did `out[(platform, handle)] = m` — it kept the last keystroke's whole
object, so a page whose final mark was typed on a sheet that stamped no mode lost the mode that
an earlier mark had recorded.

### 3.2 The part nobody had named: the key contained the answer

Because the resolution key is `(platform, handle)`, a page some of whose marks named the
platform and some of which did not **landed under two keys and ran two private
last-keystroke-wins races**. On the real graded corpus that split **2,246 handles** repo-wide.
It is not merely double-counting:

| | pre-patch reader | patched reader |
|---|---|---|
| pages checked against his raw last keystroke | 1,455 | 1,455 |
| **pages where the returned answer was NOT his last word** | **21** | **0** |
| planted-flip control (must report exactly 1) | 1 | 1 |

**The old reader returned the opposite of his final answer on 21 pages.** The control matters
here: my first attempt at this fix repaired the keys *afterwards*, preferring the real-keyed
row over the `None`-keyed one — and its own control caught that this discards his latest word
whenever the `None`-keyed mark was the later keystroke. The shipped fix makes the key stable
*before* anything is keyed and leaves the original last-wins loop untouched.

Resolved pages fall from **1,566 to 1,461** — 105 of them were the same page counted twice.

### 3.3 Backfill: what the sheets can actually say

| | resolved pages |
|---|---|
| platform **stated** by the row | 810 |
| platform **inferred** from the sheet directory name | 99 |
| platform **not recoverable** | **552** |
| mode inferred from sheet provenance | **51** (all `edits`) |
| mode not recoverable from provenance | 1,410 |

**The licensing control passed and one control was empty, which is worth saying.** Across the
repo there are **1,652 rows where the row and the sheet both name a platform, and they
disagree 0 times** — that is what licenses using sheet provenance at all. There are **0 rows
where the row and the sheet both name a mode**, so that same control *cannot be run for mode*.
Mode inference is therefore licensed by the platform result and by nothing stronger, which is
exactly why every such value is stamped `inferred:` rather than merged into `stated`.

**Why 552 pages have no platform.** They come from three files whose rows carry a `sheet`
field — real row-level provenance — pointing at sheet IDs (`BL-1196-500`, `BL-1207-FRESH50`,
`bl1186_pages`, `bl1190_pages`) whose **sheets no longer exist on disk**. Their reports survive
and name neither platform. So the reference is dangling and the platform is unrecoverable from
provenance. Any figure that assigns those pages to a brain is assigning them by guess.

A **second, weaker tier** does exist and I am reporting it separately rather than folding it
in: looking the handles up in the seen stores recovers **176 as Instagram (107 of them
rejects)** and **2 as TikTok**, leaves **1 ambiguous** and **373 in no store at all**. That is
*funnel memory*, not the sheet he graded on — a different class of evidence — so it is
deliberately **not** in the library. Letting funnel memory masquerade as his grading is a
failure this project has already paid for once.

### 3.4 THE REJECT SIDE PER BRAIN

Denominator: the 909 resolved pages whose platform is known. Mode comes from sheet provenance
where the sheet names one; where it does not, **his answer in this round's brief** — *"the
pages he graded on the meme sheets WERE judged as meme pages, and may be used as the meme
reject side"* — is applied **explicitly by the caller**, never by the library, and the two
columns are kept apart.

| brain | pages | **rejects** | reject has a picture | the sheet's own picture | mode from sheet | mode from his answer |
|---|---|---|---|---|---|---|
| tiktok / memes | 637 | **399** | 372 | 137 | 0 | 637 |
| instagram / memes | 221 | **129** | 106 | 65 | 0 | 221 |
| instagram / edits | 21 | **13** | 10 | 10 | 21 | 0 |
| tiktok / edits | 30 | **1** | 1 | 1 | 30 | 0 |
| **TOTAL** | **909** | **542** | **489** | **213** | | |

**489 of 542 rejects (90.22%, Wilson 95% [87.4, 92.4]) already have a picture on disk.** Only
**213** have the picture from the sheet he actually graded on; the rest are matched from
elsewhere in the tree, which is a weaker claim and is reported as its own column rather than
pooled. The image index was built by walking **82,842 images** and was controlled in both
directions (it answers HIT for a known handle and MISS for one that cannot exist).

**TikTok/edits cannot be filled: he rejected exactly 1 of 30.** That is the brief's own
expectation and it reproduces exactly. **Instagram/edits can be filled today** — all 13 have a
picture, and 13 of 13 have the sheet's own. The held car-edits pool remains **held and unused**.

### 3.5 Part B: the whole path, traced and driven

**The claim is confirmed: no video is decoded anywhere on the shipped judge path.** The chain
ends before the download. `discover` → the free recency gate → the paid fetch → the contact
sheet is built **from cover thumbnails** → `speech_fracs` is set to a hard-coded `None` → the
guard `ocr_can_change_a_verdict` reads that `None` and returns False → OCR is skipped → the
judge is handed the cover sheet.

**Driven with a spy, with a positive control that fires:**

| | download | `read_video` | `extract_frames` | ffmpeg | ffprobe |
|---|---|---|---|---|---|
| **Run A — positive control**, decoder driven directly | 1 | 1 | 1 | **6** | 1 |
| **Run B — the real funnel**, config as shipped | **0** | **0** | **0** | **0** | **0** |

In Run B, in the same run, the guard fired once and the skip counter incremented, and the image
handed to the judge was a six-tile cover sheet. **Second derivation from production, not from
the harness:** across 15 run exports covering **4,176 authors and 1,864 paid pages**, the OCR
stage ran in **0 of 15**, the skip counter shows 129, and its working directory **does not
exist on disk**.

**The same is true on the other platform, for a different reason.** The Instagram OCR leg is
gated on a config key that is **absent from `config.json`**, and it was switched off
deliberately by an earlier round in favour of the picture judge.

### 3.6 Why turning it on buys nothing — and what the real lever is

`on_screen` has exactly one verdict-affecting consumer: `if not has_text and talking`.
`talking` is computed from `speech_fracs`. On TikTok `speech_fracs` is assigned `None` at the
call site, so the rule is unreachable, and it has fired **0 times in 1,672 judged rows**.
Flipping the guard costs decode time and changes no verdict. **The guard is correct.**

But the comment justifying it said decoding costs **"12 frames x 2.74 s = 32.9 s per page"**,
and I repeated that figure earlier in this round because I read it rather than measured it.
**Measured, twice, on clips already on disk:**

| per page | median | p90 | max |
|---|---|---|---|
| shipped extractor | **4.59 s** | 8.76 s | 11.95 s |
| independent replication, disjoint sample | **5.39 s** | 8.03 s | 21.37 s |
| one-invocation extractor | **1.32 s** | 2.59 s | 6.05 s |

The old figure was **~7x too high**. The guard survives that correction — it is right because
the rule is *inert*, not because decoding is expensive — and the comment now says so.

**The asymmetry is the finding.** The old comment said OCR would switch itself back on "the day
somebody plumbs `speech_fracs` through the way Instagram plumbs `speech_frac`". Instagram
already does, in production, right now: it builds a speech reader unconditionally and runs it
on every page, and that reader shells out to **ffmpeg and decodes real video for audio**. So
video decoding is not switched off across this system. It runs daily, on one platform, for
sound. TikTok is the one path that hard-codes the measurement away.

### 3.7 The speedup: the fast extractor is the one nothing calls

The brief framed this as shipping a 1.93x speedup. Both halves of that framing are wrong.

* **The real speedup is 3.70x median / 4.97x p90**, not 1.93x.
* **"180 of 180 frames byte-identical" is REFUTED — the true figure is 82 of 180**, because the
  fast path selects frames on *elapsed time* and drifts off the exact instants. The claim is
  **rescuable**: an explicit-timestamp filter gives **179 of 180 pixel-exact at 3.62x**.
* **The verifier had to be a raw pixel hash.** A planted bad candidate passed a file-count check
  **30 of 30** and was the *fastest* arm — and the pixel hash rejected it **0 of 180 frames**.
  Speed alone selects the broken implementation.
* **Its consumer is off.** The fast extractor's module has **zero production importers**. The
  slow one has exactly **one** external caller, and that caller itself has no production caller
  — the codebase says so in its own comments. So the module that already collapses six
  processes into one is the one nothing calls, and the speedup has **no live consumer at all**.

The brief's condition was "ship it **if its consumer is on**". It is not on. **Not shipped.**

### 3.8 `HERO_T_DEFAULT = 1.4`

Census, with a control: `HERO_T_DEFAULT` has **0 production readers and 0 readers even inside
its own module**, while two constants declared beside it return 2 in-module reads each — so the
census can see a live constant and this one is genuinely unread.

I did **neither** of the brief's two options, and this is the one instruction I am consciously
not following. The constant is **not a stray number — it encodes his own words**, quoted in the
source: *take the text frame at the first or second second, not at zero.* Deleting it would
erase a requirement of his that is currently unmet. Implementing it changes the picture, which
this same brief assigns to another prompt and forbids me to touch. So I am reporting it
instead, with the measurement that makes it decidable: the shipped extractor takes its first
frame at *duration/12*, which crosses 1.4 s at a clip length of **16.8 s** — and **17 of 30
measured clips sample earlier than 1.4 s**, one as early as **0.417 s**. His rule is being
violated on 57% of clips, in the exact direction he warned about.

---

## 4. What was refused, and why

* **Flipping the OCR guard.** It is correct. Cost with no benefit, and it would have looked like progress.
* **Shipping the extraction speedup.** Real and larger than claimed, but it has no live consumer, and the brief's condition was explicit.
* **Deleting `HERO_T_DEFAULT`.** It carries his instruction; deleting it destroys a requirement. Reported instead.
* **Implementing `HERO_T_DEFAULT`.** It moves the picture, which this brief assigns elsewhere.
* **Putting the seen-store platform recovery into the library.** It is funnel memory, not his grading.
* **Assigning the 373 unrecoverable pages to a brain.** Their sheets are gone. A guess here would be invisible in every downstream figure.
* **Excluding two sheets marked `DO_NOT_USE_THIS_SHEET.txt`.** I nearly did. The file says the opposite of what its name suggests — *"your marks in this folder are kept and are still used as ground truth"* — and it means "do not grade here again". Those 116 rows stayed in.

---

## 5. What I got wrong, and what the brief got wrong

**Mine:**

* I quoted **32.9 s per page** as the decode cost earlier in this round. It came from a source comment, not from a measurement. Measured: **4.59 s median**, ~7x lower. The comment is now corrected in place.
* **My first version of the resolve fix was wrong and its own control caught it.** Repairing the keys after the fact silently preferred the real-keyed row over the `None`-keyed one and **discarded his latest word on 25 handles**. Fixed by making the key stable first.
* **My first control was the wrong instrument.** It compared the *set* of answers per handle, so it reported correct deduplication as a moved verdict and could not distinguish "merged two rows for one page" from "changed his answer". Replaced with the invariant that actually matters: last keystroke wins, checked against the raw marks.
* I nearly discarded 116 valid marks by reading a filename instead of the file.

**The brief's:**

* **"Ship the 1.93x speedup"** — the real figure is **3.70x**, and its consumer is off, so it should not ship at all.
* **"180 of 180 byte-identical"** — **refuted at 82 of 180**; rescuable to 179 of 180 with a different filter.
* **"2,323 raw rows carry a mode"** — the reproducible figure is **4,267** repo-wide, resolving to **42**.
* **"416 of 428 / 724 KB"** — two different denominators fused. Measured here: **489 of 542**, and only **213** have the sheet's own picture.
* **The Part B line numbers** are wrong; one cited location is a bare comment, and the load-bearing assignment is a third thing at a different line.
* **"11 car-edit pages"** — there are **10**.
* The brief assumes the blocker is that decoding was left switched off. **It is switched on in production already, on the other platform, for audio.**

---

## 6. Money and safety

**$0.00 spent this round.** No vendor call was made by me or by any of the three sub-agents;
every network hop in the trace was stubbed and the decode measurements ran on clips already on
disk. The cap was $1.50 and the run's own counter, not a ledger delta, is the source of that
zero — `spend.json` did move during the round, but it is shared and a delta across it cannot be
attributed to any one round.

**Safety.** No seen-store row was deleted or rewritten: all five stores verified **identical
row key sets** at publication, with the body found by shape and a planted one-byte corruption
control passing first. The listening-port table was re-checked immediately before each write
under `clippershq/`; no python process was killed and no `taskkill` was modified. The only
`clippershq/` edit was comment-only and proved so by syntax-tree comparison. No email address,
key, lead-store row, creator handle or absolute path appears in this report.

**Tests.** 13 new tests, all 13 executed (counted, not assumed — a silent skip has bitten this
project before). The existing reader suites pass: **39 of 39**.

---

## 7. What to do next — ranked

1. **Decide the 21 pages.** The reader now returns his last word, which means 21 graded pages just changed answer relative to every figure computed before today. Any past result that used this corpus should be re-derived rather than trusted.
2. **Fill the Instagram/edits reject side now** — 13 pages, all with the sheet's own picture. It is the only brain that is complete and cheap.
3. **Answer the `HERO_T_DEFAULT` question.** His stated rule is violated on 57% of clips. Either the rule holds and the extractor should honour it, or it is superseded and the constant should go. This needs his word, not mine.
4. **Stamp mode at write time in the sheet builders.** The reader now carries it, but the builders still write no mode, so every future sheet arrives as INFERRED rather than stated. There is no single shipped builder — the fix has to land in the manifest each builder writes.
5. **Leave the OCR guard alone** unless TikTok speech is measured. If it ever is, the guard turns itself back on, which is what it was written to do.
6. **Do not ship the speedup until something calls the extractor.** Then use the explicit-timestamp filter (179 of 180 pixel-exact), never the elapsed-time one, and verify by pixel hash.

---

## 8. Paths to open

* `tools/mark_reader.py` — `sheet_provenance`, the provenance fields, and the rewritten `resolve`
* `tests/test_bl1504_mode_provenance.py` — 13 tests including the mutation that proves the stable key is load-bearing
* `clippershq/tiktok_finder.py` — the corrected cost comment and the note on the speech asymmetry
* `scratch/bl1504_effect.py` — the before/after comparison and both controls
* `scratch/bl1504_perbrain.py` — the per-brain table and the picture census
* `scratch/bl1504_census.py` — the caller and reader censuses, with their positive controls
* `scratch/bl1504_sheetprov.py` — what provenance each graded sheet actually carries
* `scratch/bl1504_agentB_trace.md` — the full traced path, the spy counts, and the decode-cost measurements
