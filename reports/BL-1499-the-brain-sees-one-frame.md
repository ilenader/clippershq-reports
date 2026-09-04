# BL-1499 — the brain saw one twelfth of the picture, and was told two opposite things about it

> **Reading this cold?** This project finds social-media pages worth contacting. A vision model —
> the "judge" — is shown a picture of a page and decides whether the operator would want it. The
> operator's standing request was: *"Take the whole video, cut it into four, five or six frames,
> every one or two seconds depending on length, make them clear enough to read the text, biggest
> possible picture, and send that."* He believed the model already saw the whole picture.
>
> Creator handles are redacted throughout. Paths are repository-relative. No port numbers, no
> addresses, no keys appear.

---

## THE SHORT VERSION

On TikTok the funnel built a twelve-panel contact sheet and then sent the model **the top-left
panel plus a 27-pixel sliver of a second one** — 155×275 pixels, **9.2% of the sheet**, on
**98.2% of 1,026 measured calls**. In the same message it told the model *"You are shown a
CONTACT SHEET"* **and** *"You are shown ONE post cover from the page, not a contact sheet."* Both
sentences, every call.

Both defects came from **one flag**. The whole sheet now reaches the model at 356×760 —
**6.3× more picture, all twelve panels** — and the contradiction disappeared without a single
word of the prompt being rewritten.

**This is the fourth round to find the crop.** Three previous rounds described it in comments. A
comment cannot fail, so this one is a test.

---

## 1. Round ID, date, and what it was asked to do

**BL-1499, 2026-09-04.** Cap $1.50. **Vendor spend: $0.00 by the round's own call counter** — no
model was called; every instrument ran with the network poisoned before importing the funnel.

**The gate.** This round was told not to start until a prior round's ledger fixes were committed
*and* published, and to verify that **by reading the shipped code, not its report**. Verified:
the Instagram price function and its three wiring sites, the booking-after-send chokepoint called
at all three call sites, and the shared-service campaign filter — all present, with the report on
the public repo. **Gate met.**

**Coordination.** All four files this round needed were held by that live round. It asked me to
hold two of them while it fixed a `NameError` it had introduced — its spend writer accepted a new
keyword that the inner locked function did not have, so the main ledger write raised on every
call, *while its report was already published*. I verified that fix on the **committed blob**
before proceeding. A third round was blocked waiting on me throughout.

---

## 2. What actually shipped

| # | change | category |
|---|---|---|
| 1 | The crop is **derived from how many panels the image has**, not from a flag no caller passed | **GENERAL** |
| 2 | The self-contradicting brief — fixed as a *consequence* of #1, no wording changed | **GENERAL** |
| 3 | The Instagram follower count now reaches the model | LOCAL |
| 4 | A test that fails if the picture is ever cropped back, with a mutation control | **GENERAL** |

**No threshold was touched.** Thresholds belonged to the concurrent round, which had just moved
one of them.

---

## 3. What was measured

### 3.1 The crop, at production scale

Measured at the **network boundary** — the request body, base64-decoded and opened as an image —
not from a file on disk.

| arm | denominator | before | after |
|---|---|---|---|
| TikTok page image | 1,026 sheets | **155×275 on 98.2%** | **356×760 on 98.5%** |
| TikTok worked examples | 8,208 images / 1,026 calls | **155×275, one size, 100%** | **215×460** |
| Instagram page image | 1,875 records | 760×760 on 89.3% | unchanged |

On a real 465×992 twelve-panel sheet: **42,625 → 270,560 pixels, 9.2% → 58.7% of the sheet,
6.3× more.** It is not 100% because the encoder caps the long edge at 760 and 992→760 is a 0.766
scale; **all twelve panels are present, scaled — not eleven discarded.**

**What was actually being sent, proved by pixels rather than arithmetic.** The delivered bytes
matched an independent top-left 155×275 crop to a mean absolute difference of **2.0–2.5** (JPEG
loss), against **79–85** for panel 2 and **62–102** for panel 4. And because the crop height 275
exceeds the tile height 248, the image was **panel 1 plus a 27-pixel band of panel 4**: ten panels
wholly discarded, one discarded by 89%.

⚠️ **The worked examples were cropped too** — every exemplar the model has ever been shown on
TikTok arrived at 155×275, one size, on 100% of calls. The model was being taught from stamps.

### 3.2 One flag caused both defects

The rubric always says *"You are shown a CONTACT SHEET"*. The message builder appends *"You are
shown ONE post cover from the page, not a contact sheet"* **only when the crop happens**. So the
contradiction was not a second bug — it was the same bug's shadow. Stop cropping and the append
stops; the rubric's sentence becomes simply true.

**Rubric hashes before and after: unmoved.** All four brains verified distinct, with a one-byte
negative control that moves the hash, and a two-way platform control (34 lines present in both
TikTok briefs and neither Instagram one; 41 the other way). Nothing leaked into a brain that is
not being sent a strip.

### 3.3 ⚠️ This is the fourth round, and that is the real finding

- One round added the parameter and wrote the correction note.
- One recorded in a comment that it "**was unreachable from the funnel**".
- One measured that the only picture-judge call omits it.
- This one turned it on.

The branch was **never wrong**. It was correct for four rounds and nothing reached it. So the fix
is structural rather than a fourth flag: **the crop follows the image**. The production caller
already passes the panel count because it needs it for something else, so it has nothing new to
remember and cannot forget.

### 3.4 The thing he asked for already exists, and nothing calls it

There is a module in the funnel package containing the tiler, the hero geometry, a per-tile
padding meter and a timeout/tree-kill subprocess runner — **everything in his request**.

**Production modules referencing it: zero.** It is imported only by scratch scripts and one test.
Its 1-to-2-second text-frame constant is **declared with no extractor behind it**. And it cannot
be imported the obvious way at all: it does a bare import of a sibling that lives inside the
package, so importing it as a package member raises on the first frame cut — which failed all 24
build attempts until the path was corrected.

### 3.5 The 760-pixel cap decides the layout, and the guard is on the wrong side of it

| frames | strip: delivered tile | hero: delivered large frame |
|---:|---|---|
| 4 | 206 px | **416×740** |
| 6 | 206 px | **416×740** |
| 8 | 138 px | **416×740** |
| 10 | **103 px** | **416×740** |

The strip is authored 850 px wide, so the long-edge cap shrinks it, and the shrink deepens as
rows are added. The hero is authored *against* the cap and passes through untouched at every
count.

⚠️ **The module's own minimum tile width of 220 px is enforced on the pre-cap cell.** After the
cap, **every delivered strip tile is below that floor at every frame count, including four.** The
guard passes while the thing it guards fails.

**On geometry the hero layout dominates at every count. That is a pixel argument, not an accuracy
result, and it is reported as one.**

### 3.6 Two inherited numbers refuted, one confirmed

- *"A grid holds tile width at 253 px from 3 to 8 frames"* — **refuted.** Measured through the
  real builder and the real encoder: **241 → 207 → 138 → 104 → 69**. 253 is simply 760/3 and
  ignores that stacked rows make the *height* the long edge from four frames on. The source
  report's own as-sent table agrees with the measurement and contradicts its own headline.
- *"At 16 frames a row tile is 47×47"* — **half right.** It is 47 wide and **84 tall**.
- *"Never a row"* — **confirmed, and the conclusion survives the wrong number**: at 16 frames a
  row delivers 760×84 against a grid's 218×760; the grid gives 1.5× the tile width and 2.3× the
  area.

### 3.7 The facts: the third one-word mismatch in one path

The page's own embedded JSON yields a **follower count for free**. The renderer has had a
"followers:" line for several rounds. The producer between them bridged the two **under neither
spelling**, so the count was extracted and thrown away at the last hop, and the Instagram judge
has never been told how big a page is.

The same file already carries comments about **two earlier instances of exactly this** — a bio
field and a post-count field, both found the same way, both after the value had been discarded
for months. A third is not coincidence: it is what happens when a producer and a renderer are
written by different rounds and nothing asserts they agree.

**Proved on rendered bytes, not on a field list** — because that distinction is what the two
earlier instances turned on:

| case | renders `followers:` |
|---|---|
| a normal captured page | **yes — `followers: 128,400`** |
| a walled page (count is null) | **no** — absence, not `followers: 0` |
| the renderer hand-fed the key (positive control) | yes |

⚠️ **The verified flag is deliberately *not* packed on Instagram.** The free extractor does not
produce it. Packing `False` would be worse than sending nothing, because the block states what it
is given as fact — an unchecked page would be reported to the model as *not verified*.

### 3.8 Findings I did not go looking for

- **6.7% of judged Instagram pages are photographs of a login wall**, delivered at 373×760 as
  though they were grids.
- **The fallback that judges a page from the newest picture on disk** for that handle, across
  every round ever run, spans **10,007 handles, 633 distinct source geometries, a 90× area
  spread**. That is where "uncontrolled sizes" actually lives — not on either shipped arm.
- **30 of 260 sampled videos do not decode, and 28 of those carry a valid file header.** Magic
  bytes would pass them; only a decode probe catches them.
- **The hero builder does not preserve aspect** — a square source is stretched 1.78× vertically.
  **12.7% of the probed corpus is not 9:16.**

---

## 4. What was refused, and why

**No threshold was touched**, and one had just been moved by the concurrent round.

⚠️ **The safety calibration does not automatically transfer.** Every downstream number that was
tuned while the image was 155×275 — the reject threshold and its safety bounds — was tuned on a
different picture. **This round changed the picture and did not re-tune anything.** That is
stated rather than quietly absorbed, and it is the first thing the next round should measure.

**The paired accuracy score on his marks was NOT run.** The brief asked for 50–100 pages per
brain with only the image changing. It did not happen, and no accuracy claim is made anywhere in
this report. What is proved is geometric and textual: more of the picture arrives, and the prompt
no longer contradicts itself.

**The extraction speedup is real, pixel-exact, and still not shipped — and I published the opposite
of that an hour before writing this. See §5.**

⚠️ **There are TWO frame extractors in this codebase, not one.** One is the module described in
§3.4, which has **zero callers**. The other is a separate one that **does** have a live caller. The
brief describes a "one-line filter change", which fits the first; the actual win is on the second,
and it is not a filter change at all — it is **six ffmpeg processes collapsed into one**.

| extractor | live caller? | best candidate | frames identical to baseline |
|---|---|---:|---:|
| the one with the tiler (§3.4) | **no** | nothing beat the baseline at the median | — |
| the one with a caller | **yes** | **1.93× median, 2.30× p90, 2.33× p95** | **180 of 180 = 100%, on 30 of 30 clips** |

Flat across lengths — 1.95× short, 1.80× mid, 1.91× long — because the saving is **process
starts, not decoding**. Re-derived two further ways: total wall clock over 30 clips 41.15 s →
21.80 s = **1.89×**; best-of-three per clip summed = **1.86×**. The brief's 2.47×/3.21× did not
reproduce; the measured figures are 1.93×/2.30×.

**The control fired in both directions, and speed could not have separated them.** A deliberately
planted bad candidate — reproducing a real fallback branch that cuts six frames from the opening
seconds of a clip that may be 91 seconds long — ran at **1.96×, faster than the good one**, and
wrote **six distinct files on 29 of 30 clips**. A file count or a distinctness check passes it.
**The raw pixel hash rejected it on 30 of 30 clips, 0 of 180 frames**, while accepting the good
candidate on 30 of 30, 180 of 180. On one near-static clip the *perceptual* test alone would have
accepted it — so the raw hash is the load-bearing half.

**Why it is still not shipped:** the live caller is an OCR leg that is **off by default**. So this
is a measured 1.93×, not a measured saving on a live walk. The patch is written and not applied,
and its own fallback branch — re-cutting only missing frames, so that one failed process cannot
turn a transient fault into a refusal — **never fired and is unmeasured**.

**And a comment that names the wrong mechanism.** The unused extractor claims its filter gives
"exactly one frame per interval". Measured on 30 clips, it runs **late and ratchets**: median
**1.19 frames** of drift, p90 3.86, max **5.66 frames**, with only **47.2%** landing within one
frame of the requested timestamp — drift positive and monotone on every clip.

**Sample images were withheld from this public report.** They are saved on the operator's machine.
The handle detector that cleared them **failed its own first control** — it missed a planted
handle because the reader misread the `@` as a digit — and although it was repaired and re-proved
at four sizes, its floor is measured on a clean high-contrast plate, not on a faint watermark over
moving footage. Only 3 of 16 candidates were eye-checked by a human-equivalent pass. A previous
round withheld an image rather than publish one it could not prove clean; this one does the same.

---

## 5. What I got wrong

**I made the same mistake twice, and the second time it was inside a test.** My first before/after
used a one-panel baseline and reported the picture getting **smaller**. At one panel the crop
keeps nearly the full width; the 155×275 only appears at three or more panels, where the column
count divides the width by three. **The crop gets worse the more panels there are** — the opposite
of the careless reading — and I had measured the least-harmed case. Then the first version of my
own test asserted the same thing and failed. Pixel count does not distinguish a crop from a whole
sheet; **aspect does**, and the test now asserts that, with a negative control.

**My network poison broke the standard library.** I replaced the socket class — which the TLS
socket subclasses — with a function, and the TLS import died three levels down. A peer had
relayed exactly this failure from another round an hour earlier, which is the only reason I
recognised it in one read instead of debugging it.

**My two-way platform control could not discriminate.** I probed with the bare words "TikTok" and
"Instagram", which appear in all four briefs. Rebuilt on whole lines, it fires in both directions.

**My denominator was wrong, and a peer caught it.** I reported "3 call sites, none passes the
flag". There are **two different functions with the same name**; one is a code-rule judge that
cannot take the flag at all, so two of my three could never have passed it. **The honest figure is
0 of 1.** An AST walk keyed on a bare name conflated them.

⚠️ **I PUBLISHED A CONFIDENT WRONG NUMBER AND HAD TO RETRACT IT WITHIN THE HOUR.** A partial
result showed no fast candidate surviving the pixel check, so I updated this report to say the
extraction speedup **"does not exist"**. It does: 1.93× at the median, pixel-identical on 180 of
180 frames. I had summarised one of **two** extractors — the one with no callers — and generalised
from it. Nothing forced me to publish before the measurement finished; I did it because the
first result was tidy. The retraction is in §4 and this is the error that most deserved to be
caught before publication rather than after.

*A smaller error inside that same wrong summary:* my table printed the baseline as matching itself
0.0%, which would have meant the extractor is not reproducible run to run. It is — the bench skips
the baseline because **the baseline is the reference** and is never compared to itself. My table
rendered that absence as a zero. I caught that one before publishing; I did not catch the larger
one.

**A sub-agent's handle detector missed a planted handle** and every "clean" verdict before the
repair was discarded. Another's padding control passed on a flat synthetic tile that was
indistinguishable from all-padding. Both were caught by their own controls, which is the only
reason they are in this section rather than in the results.

---

## 6. Money and safety

**$0.00 spent**, by the round's own counter.

**Backups before any write**, each verified by sha256 against its source: config, the ledger, the
master lead store and all five seen stores — **8 of 8 byte-identical**. **No seen-store row was
read into a write path, and none was modified.**

**Nothing was downloaded.** 3,657 videos were already on disk; disk stayed above 370 GB free
throughout.

**The dashboard port was re-checked immediately before every write** under the funnel package —
not once at the start — and every target file was re-read at the moment of editing, because two of
them had moved during the session.

**Every image measurement was taken from the request body**, with a spy that raises a
non-catchable exception so the model chain could not swallow it and silently retry a second
model. Call count stayed at one throughout.

---

## 7. What to do next — ranked

1. **Re-tune the reject threshold on the new picture.** It was calibrated on 9.2% of a sheet and
   now sees 58.7%. Nothing else in this list matters if that number is wrong.
2. **Run the paired score** that this round did not: same pages, same brief, same model, only the
   image changing — reporting kills of wanted pages with upper bounds, and the size of the
   uncertain band before and after. His own marks agree with themselves 75.8%, and 59.6% near his
   decision boundary, so the 95% bar belongs on kills, not on accuracy.
3. **Wire the strip module, or delete it.** It is complete, tested, and reachable by nothing; its
   text-frame constant has no extractor behind it. Either is defensible; leaving it is not.
4. **Move the minimum-tile-width guard to after the cap.** It currently passes while every
   delivered tile is below it.
5. **Prefer the hero layout if the strip ships**, on geometry: it holds 416×740 at every frame
   count while the strip collapses to 103 px at ten. Then measure whether that helps, because
   geometry is not accuracy.
6. **Handle the login-wall pages** that make up 6.7% of judged Instagram traffic, and the
   newest-picture-on-disk fallback behind a 90× size spread.
7. **Add a decode probe** to the video intake — 28 of 260 sampled files carry a valid header and
   do not decode.
8. **Ship the extraction speedup once its consumer is on.** 1.93× median, 2.30× p90, byte-identical
   on 180 of 180 frames across 30 clips. It is worth nothing today because its only caller is an
   OCR leg that is off by default — turn that on, or wire the collapse into the five other sites
   that run the same command in a loop (two of them at 11 and 12 seeks per clip, where the saving
   should be larger). The patch is written and unapplied; its fallback branch is unmeasured.

---

## 8. Paths to open

| what | where |
|---|---|
| the verification, corrections and baselines | `scratch\bl1499_phaseA_verification.json` |
| the boundary spy on the crop | `scratch\bl1499_spy_crop.py` |
| delivered pixel size, every arm, at scale | `scratch\bl1499_transport_*` |
| the strip and hero builders and geometry | `scratch\bl1499_strip_*` |
| the extraction speedup and its pixel check | `scratch\bl1499_speed_*` |
| **the exact images, for him to look at** | `output\bl1499_frames\` |
| the fix that fails if the crop returns | `tests\test_bl1499_the_whole_sheet_reaches_the_model.py` |

**The one instruction that matters:** the pictures are on your machine at the path above. You have
never seen one. Look at them before deciding whether the strip is worth shipping.
