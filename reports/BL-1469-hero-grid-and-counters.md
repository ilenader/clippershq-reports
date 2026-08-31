# BL-1469 — the hero grid is built and measured; its headline is RETRACTED as noise

> **IS THE FUNNEL SAFE TO RUN? — NO.**
>
> Not for TikTok edits judging. The judge chain answers and the spend caps hold, but what the
> model actually *receives* on roughly four TikTok pages in five is a **155x275 crop**, and this
> round measured that resolution and could not establish whether text is readable at it. The
> hero-grid strip this round built is **NOT wired in**, and wiring it the obvious way would
> destroy 84.8% of its area silently. Nothing here should be run to produce leads until the
> encoder question below is closed.
>
> What *is* safe: no vendor money was spent, no store was written, nothing was deleted.

---

## 1. WHAT THIS ROUND WAS ASKED TO DO

**Round:** BL-1469 · run 2026-08-30/31 · published 2026-08-31.

In plain words, the brief asked for four things:

1. **Build a "hero grid".** Today the funnel shows the judge a sheet of equal-sized video
   frames. The operator's observation is that on-screen text — the thing that tells an edit page
   from a meme page — becomes unreadable as more frames are packed in, while the motion and
   colour-grading cues get *better*. His fix: make the first frame, the one with the text, much
   **larger** than the rest, so text and motion are both served by one picture.
2. **Prove it running**, not just prove it exists.
3. **Build a live watch view** in the dashboard so he can see a run progress page by page.
4. **Do a 20-page run** through the result.

The round was also gated: it was not to start until a separate round (BL-1468) confirmed the
judge was safe to measure against. That gate was checked and it opened — a real grid already on
disk was put through the live judge and came back with a real verdict and a real reason in
14.8 s, which is a positive control rather than an absence of errors.

**Of those four asks, one and a half were delivered.** The strip and the geometry were built and
measured. The counters the live view needs were made persistable. The panel, the wiring, the
watch and the 20-page run were **not done** — see section 4.

---

## 2. WHAT ACTUALLY SHIPPED

Each item below names the file and how it was proved. A grep, a docstring, or a passing test is
not proof here.

### 2.1 `hero_geometry()` and `build_hero_strip()` — `clippershq/video_strip.py`

Computes and builds a sheet with one large frame beside N small ones.

**How proved: BUILT, THEN RE-MEASURED OFF DISK.** Three sheets were built and their delivered
pixel sizes read back out of the written JPEG files, then compared against what the function had
predicted before building:

```
  hero+3   predicted 585x760, hero tile 416x740   delivered 585x760, hero tile 416x740   MATCH
  hero+5   predicted 530x760, hero tile 416x740   delivered 530x760, hero tile 416x740   MATCH
  hero+8   predicted 498x760, hero tile 416x740   delivered 498x760, hero tile 416x740   MATCH
```

Predicted equals delivered on all three, and the long edge is exactly 760 on all three. The
property that makes it a *hero* — the large frame stays 416x740 no matter how many small frames
are added — holds at every count tested.

### 2.2 The frame extractor was made runnable — `clippershq/video_strip.py`

The module could not be imported and run on its own: four names it used were never brought into
scope, one field was read under the wrong name, and one call site unpacked a return value that
is a tuple as though it were not.

**How proved: BY RUNNING IT.** It now extracts frames end to end from real downloaded videos —
every measurement in section 3 is its output. Before the fix it raised on import.

A docstring in the same file claimed a behaviour the code does not have. That claim was
corrected rather than left standing.

### 2.3 Ten fields declared in the run-status record — `clippershq/run_status.py`

Five progress counters (`discovered`, `captured`, `judged`, `paid`, `delivered`) and five
live-page fields (`page_now`, `image_now`, `verdict_now`, `confidence_now`, `reason_now`).

**How proved: BY WRITING AND READING THE STATUS FILE BACK.** Values are set through the normal
update path, the file is re-read from disk, and the values are there. Proved the same way: an
*undeclared* key is still silently dropped. The whitelist that makes this necessary was
deliberately left in place — loosening it would make the next counter someone adds look like it
works when it does not.

**Why declaring was the whole job:** the update path keeps only keys **already present** in the
record, so a counter that is set but not declared cannot move. Two of the five did not exist
under the names the brief used at all — there is no "paid" counter anywhere (the only paid
quantity is a dollar figure, not a page count), and "delivered" is really the pass counter under
a different name.

`None` means NOT MEASURED YET; `0` means MEASURED ZERO. Those two must stay distinguishable,
because a panel showing a stale zero looks identical to a dead run.

---

## 3. WHAT WAS MEASURED

Sample size is 8 videos for everything model-related. That is small, and it is stated on every
line rather than hidden in a footnote.

### 3.1 Geometry — MEASURED (arithmetic plus built files, no model involved)

The judge's encoder caps the **long edge** of any sheet at 760 pixels, so the layout question is
which element gets to own that long edge.

| layout | large frame delivered | small frame delivered | basis |
|---|---|---|---|
| hero **above** 3 smalls | 321x570 | 107x190 | DERIVED (same formula, for comparison) |
| hero **beside** 3 smalls | 428x760 | 142x253 | DERIVED |
| hero beside any N smalls | **416x740** | shrinks with N | MEASURED (built and read back, 3 counts) |
| uniform 3x2 sheet (today) | 214x380 per tile | — | MEASURED (built and read back) |

The mechanism is the cap itself, and it is arithmetic rather than preference:

```
  hero+3    built  585x760  -> encoder scale x1.000 -> text frame reaches model at 416 px
  uniform6  built 1120x1312 -> encoder scale x0.579 -> text frame reaches model at 208 px
```

The hero sheet is built **at** the cap, so nothing is thrown away. The uniform sheet is built
above it and loses 42% of every tile on the way in. **MEASURED.**

Independently reproduced by a peer round on a different machine.

### 3.2 What production actually delivers — MEASURED, and it is not what I first reported

The encoder is chosen by a single line: single-video calls take a **cropping** encoder,
everything else takes the scaling one. The cropping encoder **crops to the top-left cell first**,
then caps, and never upscales.

Measured across **1,060 real contact sheets** already on disk, all built at 465x992:

| tile count requested | what the model receives | basis |
|---|---|---|
| 1 | 427x760 (at the cap) | MEASURED, n=1,060 |
| 2 | 232x412 | MEASURED, n=1,060 |
| 3, 6, 9, or unspecified | **155x275** | MEASURED, n=1,060 |

**Denominator for how often that matters:** of **901 recorded rows**, 640 requested 9 tiles —
**71.0%**, Wilson 95% **[68.0, 73.9]** — and 100 requested 6 — **11.1%**, Wilson 95%
**[9.2, 13.3]**. So **82.1%** of rows reach the model at 155x275. The row census is a peer
round's; I re-derived the pixel sizes myself.

**Positive control for those small numbers:** a synthetic 2000x2400 sheet encodes to 633x760
through both encoders, so the cap demonstrably fires and 155x275 is a **crop**, not a broken
measuring instrument.

### 3.3 Cost of naive wiring — MEASURED (arithmetic on built files)

A hero sheet is not a contact sheet, so the cropping encoder slices straight through it:

```
  hero+3 sheet built 585x760
    scaling encoder                  -> 585x760   the whole sheet
    cropping encoder, tiles unset    -> 195x346   A SLIVER CUT THROUGH THE 416 px TEXT FRAME
    cropping encoder, tiles=4        -> 195x346   same
    cropping encoder, tiles=1        -> 585x760   whole, correct
```

```
  whole   585x760  = 444,600 px of area
  sliver  195x346  =  67,470 px of area
  area retained 15.2%   ->   AREA LOST 84.8%
```

**MEASURED.** Wired the obvious way, the hero grid would be reduced to a sixth of its area, and
the only symptom would be text accuracy *worse* than the baseline, with nothing in the record
explaining why.

### 3.4 Text legibility by layout — MEASURED, n=8, EVERY CELL ASKED TWICE, result RETRACTED

The answer key is the **same single frame at 1280 px** that the hero shows, read by the same
model. Every arm is then asked to read that same frame's text out of the composed sheet. Both
runs of every cell are recorded, and a cell scores only if **both** runs came back perfect.

| arm | perfect on BOTH runs | Wilson 95% | disagreed with itself | blank answer |
|---|---|---|---|---|
| hero + 3 smalls | 7 of 8 = 87.5% | [52.9, 97.8] | 1 of 8 | 0 of 8 |
| hero + 5 smalls | 6 of 8 = 75.0% | [40.9, 92.9] | 0 of 8 | 0 of 8 |
| hero + 8 smalls | 6 of 8 = 75.0% | [40.9, 92.9] | 1 of 8 | 1 of 8 |
| uniform 6-tile (today) | 5 of 8 = 62.5% | [30.6, 86.3] | 2 of 8 | 1 of 8 |

**The ceiling over all of it: the answer key agreed with itself on only 6 of 8.** No arm can be
read as better than the instrument that produced it.

**HIS 98% TARGET IS NOT REACHED.** Best arm 87.5%, lower bound 52.9%, n=8.

**And this headline is RETRACTED — see section 5.4.** The intervals overlap almost entirely, and
a control run placed the same nominal size 25 points away from itself, a swing larger than the
whole hero-versus-uniform gap.

Blank answers behaved as the brief predicted: the model stops answering before the pixels run
out — 0 of 8 blank at the two lowest densities, 1 of 8 at the two highest.

### 3.5 Legibility at production's real size — MEASURED, n=8, and it separates NOTHING

The same hero frame at three delivered sizes, asked twice each against the same 1280 px key, so
that size is isolated from layout:

| delivered size | perfect on BOTH runs | Wilson 95% | disagreed with itself | blank |
|---|---|---|---|---|
| 585x760 (hero sheet size) | 5 of 8 = 62.5% | [30.6, 86.3] | 2 of 8 | 2 of 8 |
| 427x760 (single-tile path) | 4 of 8 = 50.0% | [21.5, 78.5] | 3 of 8 | 1 of 8 |
| **155x275 (production today)** | **3 of 8 = 37.5%** | **[13.7, 69.4]** | 3 of 8 | 0 of 8 |

The direction is monotone in pixel count. **Nothing separates.** The correct label for 155x275
is **UNMEASURED — not PASSED, and not FAILED either.** The interval contains both "fine" and
"bad".

### 3.6 Frame extractor speed — MEASURED, n=5 videos, with a raw-pixel check

```
  arm         seconds   frames   pixels identical to a per-frame reference
  shipped        0.68        6   6 of 6 frames are the SAME PICTURE
  naive loop     1.58        6   6 of 6
  -> shipped is 2.33x the speed of the naive loop
```

The pixel comparison is the part a frame *count* cannot do — an earlier candidate passed on
count while returning different pictures.

**A finding that argues for the hero design:** the shipped arm returned only 4 distinct pictures
out of 6, and the per-frame reference shows the same non-distinctness, so it is a property of
the **content**, not of the extractor. Across the 5 sampled videos the distinct-frame counts
were **5, 1, 4, 6, 1 out of 6** — two of five videos are essentially a single still for their
whole duration. Where a video is static, small motion tiles carry nothing, and the pixels belong
on the text.

### 3.7 Costs — NOT MEASURED this round, deliberately

No per-page or per-lead cost figure is produced here, because this round made **zero vendor
calls**. A cost from another run must not be multiplied by a rate from this one, so no such
figure appears rather than an estimated one.

---

## 4. WHAT WAS REFUSED OR NOT DONE, AND WHY

A measured refusal is a valid result. These are the four, with their reasons.

- **The dashboard live-watch panel — NOT BUILT.** Its stated precondition (persistable counters)
  is now met. The panel itself is a change to a 248 KB front-end file that must be syntax-checked
  and exercised in a real browser, and it was left unstarted rather than half-built.
  **Consequence worth knowing: no dashboard file was written, so the operator's running dashboard
  was never restarted by this round.**
- **Wiring the hero strip into the judge — REFUSED.** Wiring changes *what the judge sees*, which
  changes verdicts. Doing that on the strength of n=8 — and, as it turned out, on an n=8 whose
  effect does not survive its own noise — is exactly the move that has cost this project rounds
  before. It needs the hero arm scored against the operator's own marked pages on both sides of
  the change first.
- **The sanity watch and the 20-page run — NOT DONE.** Both depend on the two items above.
- **The encoder's default was not changed.** The cropping default is the trap that would have
  broken this design, and it has now caught two designs the same way — a prior round lost a
  311 px sheet to a 103 px sliver while its report described it as "one thumbnail". That file was
  **held by another round**, so this was passed to its owner as a finding rather than edited
  across a claim boundary.

---

## 5. WHAT I GOT WRONG

The most useful section in the file. Everything here is a retraction or a correction of something
this round asserted.

### 5.1 A first run scored FLAWLESS on every arm, and it was a bug

The judge helper returns a **plain string**, not the structured response object I assumed. My
attempt to read a field off it raised. Because both the answer key **and** every arm then held
the identical error text, the character-error-rate scored them as **0.0 — a perfect match on
every arm**. A fake perfect score is exactly the shape this project keeps producing. The tell was
not that the score looked too good; it was that the key was an error string. **Every result from
that run was discarded and the whole measurement re-run.**

### 5.2 My headline comparison described a code path production does not take — RETRACTED

I reported "416 px versus 208 px" as the hero grid's advantage. A peer round challenged it; they
were right, and I verified it myself. My harness explicitly called the **scaling** encoder, while
the shipped TikTok call takes the **cropping** one. So 416 versus 208 is a fair A/B between two
sheet designs at one encoder, **but neither number is what production delivers.** Production is
worse than the number I had used as the baseline: **155x275 on 82.1% of rows.**

The corrected comparison, against what production actually delivers today:

| | delivered to the model | versus production |
|---|---|---|
| production sheet, 9 tiles | 155x275 | — |
| hero+3 wired single-tile | 585x760 | **3.77x the width, 10.43x the area** |

### 5.3 I quoted a WIDTH ratio and called it the loss — corrected

I wrote that naive wiring destroys the hero "to a third of itself". 0.333 is the **width** ratio.
The area ratio is 0.152, so the real loss is **84.8%**. I undersold my own case by a factor of
two.

### 5.4 The central claim of this round does not survive its own noise — RETRACTED

In section 3.4 the composed hero sheet at 585x760 scored **87.5%**. In section 3.5 a bare frame
at the **same** 585x760 scored **62.5%**. Two runs, a nominally similar thing, and a **25-point
swing — larger than the entire hero-versus-uniform gap I had reported as the headline.**

So: **the hero grid's legibility advantage is suggestive, not established.** The *geometry*
findings stand — they are arithmetic, reproduced independently on a second machine, with no model
in the loop. The *readability* claim does not. It needs a much larger n before anyone wires
anything on it.

### 5.5 I then overstated the retraction in the other direction — corrected

Reporting section 3.5, I told the operator that text at 155x275 is "not obviously unreadable" and
called that "the honest answer to the question". **It is not an answer; it is the absence of
one.** 37.5% [13.7, 69.4] is an interval containing both "fine" and "bad". Retracting the hero
headline does not issue a clean bill of health to the resolution production ships today — that
would be the same overreach with the sign flipped. The label is **UNMEASURED**.

### 5.6 Two smaller corrections accepted from peer rounds

- I described a model-ordering line as unconditional. It applies **only when the caller took the
  default chain**; an explicitly supplied chain is honoured deliberately.
- A claim from another round that a particular model is "dead" is now **"flaky, not dead"** — it
  answered in 2.33 s on a live re-probe.

### 5.7 An instrument that lies about a store's own history

A peer round observed that when 8 records were removed from a seen-store, the store's own
"last updated" field **did not move**. A reader trusting that field would conclude nothing had
happened. That is worth knowing independently of this round.

---

## 6. MONEY AND SAFETY

### Vendor spend — from THIS RUN'S OWN CALL COUNTER

```
  vendor calls made by this round:   0
  vendor dollars spent:              $0.00
```

Every model call went through the free tier, and every video came from a content-delivery URL a
previous round had already paid for.

**The shared ledger is NOT the measure, and here is the proof.** Over this round's window the
shared ledger moved **+$0.031332**. That is other rounds billing into the same file. The ledger
delta read **$0.001314** when the internal version of this report was written and **$0.031332**
at publication — it kept moving while this round did nothing at all. A ledger delta cannot
attribute spend to a round; a run's own counter can, and it reads zero.

### Seen-store delta — RE-VERIFIED AT PUBLICATION

```
  store                     now    baseline   delta
  meme pages               5985        5993      -8
  tiktok pages             2446        2446      +0
  clip store               2193        2193      +0
  repost store             1715        1715      +0
```

**The meme store SHRANK by 8, and that was checked rather than assumed.** All 8 removed records
are rejections attributed to an old round, and **all 8 still have a checkpoint record**, so the
removal is recoverable rather than destructive. **This round made no seen-store write of any
kind**, and a peer round independently proved it was not theirs either. It appears to be a third
round un-burying pages that were rejected under a threshold set on a model that no longer runs.
Neither of us restored anything. **Attribution beyond that: NOT MEASURED.**

### Disk

```
  free at round start:     456 GB
  free at publication:     428 GB
  floor enforced:            3 GB   -- re-read before every download batch
  lowest observed:         never within 400 GB of the floor
```

Every downloaded video was deleted after framing, and each delete was **verified by re-checking
the path afterwards**, never assumed. The swing between the two readings is normal for this
machine (cloud-sync placeholders move it by tens of gigabytes on their own) and is not this
round's consumption.

### Processes — what was killed, and what was not

- **Killed: one.** A duplicate copy of my own frame-stripper, started twice by mistake, which was
  producing file-lock errors. Its command line was confirmed first, and it was then killed **by
  its own process id**. Nothing else.
- **Not killed: everything else.** No broad process sweep was run at any point. The operator's
  sheet servers and dashboard were untouched.
- **The dashboard was never restarted**, because no file under the dashboard directory was
  written.

### Campaign table

The campaign table was checked for drift by hashing its **source text** in the working copy and
in the last commit:

```
  campaign table text, working copy == last commit    UNCHANGED (12 entries)
```

**The SHA carried in the brief could not be reproduced by me, and is reported here as NOT
CONFIRMED** — I could not find the project's own method for computing it, and a hash produced by
a different method is not evidence of anything. What *is* established is the stronger practical
fact: the table's text has not changed, and no commit from this round touched that file.

### Content scan of this report

This file was scanned **by reading its own bytes**, not by listing what changed in the working
tree — an earlier self-scan once reported a directory clean without looking inside it, because a
directory appears in that listing as a single entry.

```
  email addresses                    0 (none)
  API-key-shaped strings             0 (none)
  wallet addresses                   0 (none)
  rows from the lead store           0 (none)
  creator handles                    0 (none)
  absolute paths containing a username   0 (none)
  C0 control bytes                   0 (none)
```

**The scanner was proved before its zeros were believed.** A zero from an instrument that cannot
detect the thing is not a measurement, so a real row out of the lead store was fed to the same
detectors first and they caught it (row, header and handle patterns all fired; nothing from that
row was printed anywhere). Only then was a zero on this report treated as meaningful.

**And the first version of that scanner was wrong.** It flagged **4 lead-store rows** in this
file that were nothing of the kind — a list of field names in backticks, a markdown table row,
and a list of frame counts. It was matching any prose containing commas. A scanner that cries
wolf on prose is a scanner someone eventually switches off, so it was tightened to require an
actual store-identifying token inside a comma-joined record, and then re-proved as above. The
counts in the table are from the tightened, proved version.

The control-byte check runs **before** the file is written, against the exact bytes about to be
written, and the write is abandoned if it fails — a report once carried a literal NUL byte, and
both git and grep silently treated the file as binary and skipped it, in the very commit that
documented the bug. Paths in section 8 use forward slashes for a related reason: a Windows path
segment beginning with `b` becomes a backspace byte under string escaping, which makes a printed
path unopenable.

---

## 7. WHAT HE SHOULD DO NEXT — RANKED

**1. Close the encoder question. It is the only item that changes money today.**
82.1% of TikTok rows reach the judge at 155x275, and nobody knows whether text is readable at
that size — including me, at n=8. Every rejection those rows produce is a decision taken on a
picture we have not established the model can read. **The arithmetic:** measuring this properly
costs a few dozen free-tier calls and no vendor dollars; *not* measuring it puts every TikTok
verdict made since the cropping path shipped on an unverified footing. Run the same three-size
test at **n=60 or more** — that narrows a 37.5% point estimate from roughly ±28 points to
roughly ±12, which is enough to act on.

**2. Make the crop impossible to hit by accident.**
Either require the tile count whenever a single-video call is made, or default the sheet to one
column instead of three when the count is unspecified. Cropping is the surprising behaviour;
showing the whole image is not. **The arithmetic:** this trap has now silently destroyed **two**
designs — a 311 px sheet became a 103 px sliver in one round, and it would have taken 84.8% of
the hero sheet's area in this one. A warning in a docstring did not stop the second one; a rule
at the call site would have.

**3. Only then wire the hero strip — with the tile count set to 1.**
The strip is built, tested, and its geometry verified. It is one argument away from being correct
and one argument away from being destroyed. Do not wire it on the strength of the n=8 in
section 3.4, which this report retracts.

**4. Build the live watch panel.**
The counters are now persistable, which was the blocker. Two things found while surveying for it,
both of which save work: the TikTok export already carries the judged image path on every row,
while the meme export does **not** and needs a cross-reference by page name to recover it; and
the existing board front-end already contains a correct hidden-tab refresh pattern, with a
comment naming the exact bug where a board sat at "loading" forever in a background tab. Reuse it
rather than re-derive it.

**5. Leave the 8 un-buried meme pages alone until their owner explains them.**
They are recoverable, they have checkpoint records, and the round that removed them has not been
identified.

---

## 8. WHERE THE FILES ARE

Paste these into File Explorer. `%USERPROFILE%` expands on its own, so no username is written
here.

**No port number appears anywhere in this report.** Ports are not stable across runs, and a
grading session was lost to a bookmarked one. Start the dashboard from its own launcher and use
whatever address it prints at that moment.

```
  the project
    %USERPROFILE%/OneDrive/Desktop/clipper finder

  the two sample sheets -- he has never seen one of these
    %USERPROFILE%/OneDrive/Desktop/clipper finder/output/bl1469_samples
       HERO_GRID_hero_plus_3.jpg      585x760, text frame 416x740,    73 KB
       BASELINE_uniform_6.jpg        1120x1312, tile 360 wide,       241 KB

  the code that builds them
    %USERPROFILE%/OneDrive/Desktop/clipper finder/clippershq/video_strip.py

  the run-status fields behind the live view
    %USERPROFILE%/OneDrive/Desktop/clipper finder/clippershq/run_status.py

  the tests for both
    %USERPROFILE%/OneDrive/Desktop/clipper finder/tests/test_bl1469_hero_and_counters.py

  the raw measurement output, one JSON line per video
    %USERPROFILE%/OneDrive/Desktop/clipper finder/scratch
       bl1469_textacc.jsonl     the four-arm layout test   (section 3.4)
       bl1469_sizetest.jsonl    the three-size test        (section 3.5)
```

The sample images live under the output folder, which is excluded from version control, so they
exist on disk only and are not part of any commit.

---

*Every rate in this report carries its denominator and a Wilson 95% interval. Where something was
not measured, the cell says NOT MEASURED rather than being filled in.*
