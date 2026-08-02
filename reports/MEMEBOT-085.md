# MEMEBOT-085 — the crop fix verified on the labelled regression set, and the two measurements MEMEBOT-082 needs

**The patch this round was sent to land is obsolete and was NOT applied. MEMEBOT-071 already
landed a better fix; independently replicated here on MEMEBOT-076's ten hand-labelled clips,
7 of 7 restored and 0 of 3 survivors regressed. Handing MEMEBOT-082 three measured results:
a text detector at P=91.3% / R=95.5%, the 19.3% fallback figure corrected to 3.7%, and
`y_offset` as a −23.1-point lever where `scale_width` is worth 0.0.**

---

## 0. Preconditions — the brief's first instruction had to be refused

`tools/claims_read.py --holders memebot/scraper/edit.py` returned **MEMEBOT-082**, claimed 2
minutes before this round and having written `edit.py` **36 seconds** earlier. It also holds
`templates.yaml`, `test_edit_behaviour.py` and `test_caption_fit.py`. Its intent is items 2–5 of
this brief:

> Default to the source's own overlay (no added caption) **with a trustworthy routing signal**;
> **reclaim vertical waste in templates.yaml**; confirm the pad guard on a planted overflow; fix
> caption_hook eating the payoff word (MEMEBOT-074) and the vertical content crop slicing the
> source headline. Frames read.

MEMEBOT-071 *has* released — and had already **committed** `b7eca8b` two hours before this round
began. So item 1 was not waiting to be landed. It was done.

**`scratch/mb076_patch.diff` must never be applied.** I wrote it, and it is now wrong:

| | `mb076_patch.diff` (mine) | `b7eca8b` (landed) |
|---|---|---|
| zoom | `crop=…:(iw-ow)/2:0` — still discards the bottom and both sides | **carried to the scale step** (`tx_zoom`), applied as enlargement into the wasted canvas margin — **no pixel is discarded** |
| content crop | untouched | a **second** cropper: `cropdetect` returned `crop=988:1374:46:242`, taking 46px/side, because a caption bar's outermost pixels *are* the bar |
| pad | untouched | a **third** defect: `pad` silently re-centres an overflowing input (`shift_y +6` → `y=140`, picture slides 146px up under the caption band). 4 of 30 renders, **including the shipped 864 geometry** |

I diagnosed one cause. There were three on the same axis. Applying my patch would re-introduce a
crop that no longer exists.

Read-only round: **nothing in `memebot/` was written.** Every render ran against a
`git archive HEAD` export at `scratch/mb085_work/head` (`b7eca8b`), so MEMEBOT-082's live edits
could not contaminate the measurement. Spend **$0.00**, no paid calls.

---

## 1. Independent replication — 7/7 restored

MEMEBOT-071 verified on 30 renders of its own choosing. That is a real check and it is *different
evidence* from this: MEMEBOT-076 hand-read 10 specific clips and recorded, per clip, exactly how
the centred crop damaged each. Those 7 named failures are a labelled regression set, and re-running
*them* answers a question a fresh sample cannot.

Same harness, same pinned transforms, two arms that add no overlay — `a_source` at zoom 1.000 (the
reference) and `d_none` at zoom 1.125 (the arm that was broken).

| clip | MEMEBOT-076 damage under the old crop | on `b7eca8b` |
|---|---|---|
| `3450422996…` | bar lost entirely | ✅ "No one, me this winter :" present |
| `3483791661…` | line 1 clipped through the letterforms | ✅ both lines whole |
| `3496888229…` | bar lost entirely | ✅ "Who's your favourite ?" present |
| `3629145006…` | line 1 deleted | ✅ "Master Oogway could've defeated Kai / but he left that for the panda" |
| `3665688194…` | line 1 deleted | ✅ both lines whole |
| `3704370692…` | line 1 clipped through the letterforms | ✅ "68 after 67 and 69 / both got famous:" |
| `3707586922…` | line 1 deleted | ✅ "That one super hygienic guy / with his girlfriend" |
| `2940892612…` | survived | ✅ unregressed |
| `3457699377…` | survived | ✅ unregressed |
| `3700336049…` | survived | ✅ unregressed |

**7/7 restored, 0/3 regressed, 10/10 source captions intact.** 20 renders, frames read.
Sheets: `scratch/mb085_frames/sheets/restored_1.png`, `restored_2.png`, `survivors.png`.

---

## 2. The fallback signal — measured against hand labels

`vision_on_screen_text` cannot route this, and now there is a number for it.

**Method.** 30 clips, half where the field reports text and half where it reports none —
deliberately, so the field's disagreement with the frames can be seen on both sides. Three frames
per clip at 15%/50%/80% of duration. **Three clips excluded**: `ffprobe` returns no duration, and a
detector that says "no text" about a file it cannot open is not making a prediction. n = **27**.

Labelled by reading contact sheets *before any score was computed*, on two questions, because the
detector and the decision are not asking the same thing:

* **`any_text`** — any burned-in glyphs at all: meme caption, film subtitle, channel watermark.
* **`hook`** — a burned-in line that *functions as a headline*. A dialogue subtitle narrates, it
  does not set up. A watermark is not a hook.

### The field

| | TP | FP | FN | TN | precision | recall |
|---|---|---|---|---|---|---|
| `vision_on_screen_text != ""` vs `any_text` | 14 | 0 | **12** | 1 | 100.0% | **53.8%** |

**Of the 13 clips where the field reports none, 12 carry text — a 92.3% false-negative rate
(95% CI 64.0–99.8%).** The field never cries wolf and misses half of everything. It is a
*positive-only* signal: non-empty means text, empty means nothing at all.

### The detector

Classic morphological localisation, no model file, no network, no spend: Sobel-x → Otsu → close
with a wide-short kernel → connected components filtered on aspect, height, width and **internal
edge density** (a solid graphic bar fills ~100% of its box, a lone rail ~2%; both pass the shape
tests and neither is text).

| rule | TP | FP | FN | TN | precision | recall |
|---|---|---|---|---|---|---|
| `bands>0` vs **any_text** | 26 | 0 | 0 | 1 | **100.0%** | **100.0%** |
| `bands>0` vs **hook** | 22 | 4 | 0 | 1 | 84.6% | 100.0% |
| `bands>0` **and top band in top 20%** vs hook | 10 | 0 | 12 | 5 | 100.0% | 45.5% |
| **`bands>0` and top band in top 35%** vs hook | 21 | 2 | 1 | 3 | **91.3%** | **95.5%** |
| `bands>0` and top band in top 50% vs hook | 22 | 3 | 0 | 2 | 88.0% | 100.0% |

**Recommend `bands>0 AND top_band ≤ 0.35`: P = 91.3%, R = 95.5%.** The position rule is what
separates a hook from a subtitle — both false positives it removes are dialogue subtitle tracks
sitting at `y_frac` 0.749 and 0.427. The two that survive are channel watermarks
(`PRIMECUTTV`, `y_frac` 0.23/0.24) which sit in hook territory and are not separable by position.

**The `any_text` row is 100/100 and is the least useful number here** — 26 of 27 clips are
positive, so a detector that always said yes would score 96.3%. It is reported because a
near-degenerate base rate is exactly what makes a perfect score look like skill.

### The number that changes the decision

| | measured | 95% CI (Clopper–Pearson) |
|---|---|---|
| clips with **no burned-in text at all** | **1/27 = 3.7%** | 0.1 – 19.0% |
| clips with **no hook** (subtitle / watermark / blank) | **5/27 = 18.5%** | 6.3 – 38.1% |

**The brief's 19.3% is not the no-text rate — it is an artefact of the field that misses text 92%
of the time.** Measured on frames, only 3.7% of clips have nothing burned in. The population that
actually looks bare under a no-overlay default is the **18.5% with no *hook***, and it is a
different set, composed of 2 subtitle-only clips, 2 watermark-only clips and 1 genuinely blank one.

### What to do with them

**Ship no caption.** MEMEBOT-076 measured that the scraped caption is a hook 1 time in 10; on these
five clips we would be right about 10% of the time and publishing a rate card the rest. A blank
top band is not a defect — it is `white_frame` doing what it is for.

Wire the detector as a **recorded field, not a gate**: it costs one ffmpeg seek and a Sobel per
clip, and it makes the 18.5% addressable later, when there is a caption worth adding. Routing on it
today would only choose between two bad captions.

---

## 3. The canvas instrument — settled, and my own number corrected

Both colours, same ten clips, same two widths, on the landed commit.

| instrument | dead @864 | dead @1080 | **gain** |
|---|---|---|---|
| white | 55.0 % | 48.6 % | **−6.4 pt** |
| magenta | 49.5 % | 42.9 % | **−6.6 pt** |

**Magenta is the right instrument for the LEVEL, and the disagreement is exactly where predicted.**
Seven of ten clips agree within ±1.5 pt. Three diverge hard — **+25.7, +18.7 and +11.7 points** —
and they are precisely the three clips whose source caption bar is **white**
(`3700336049` "You can't cheat his nose lol", `2940892612`, `3457699377`). A white canvas cannot
tell the template's pad from the source's own white pixels, so it books the caption bar as padding.
That is a prediction made before the numbers and confirmed by them, not a preference.

**But the colour barely moves the GAIN (−6.4 vs −6.6), so MEMEBOT-071's rejection of 1080 was not
an artefact of measuring on white.** The two rounds were never really disagreeing about colour.

**And I have to correct MEMEBOT-076.** It published 58.2% → 42.9%, a **−15.3 pt** gain. On the
landed code the same measurement is 49.5% → 42.9%, **−6.6 pt**. The gain has more than halved,
because `b7eca8b`'s zoom now *enlarges into the very margin* that raising `scale_width` was going
to reclaim. My published figure was measured on a filter chain that no longer exists. **−6.6 pt is
the live number; −15.3 pt should not be quoted again.**

At a ~6.6-point gain against losing the white side margins that are the template's identity, I do
not think `scale_width` is where the next move is — see §4.

---

## 4. `y_offset` is the lever, by a factor of three and a half

At `scale_width: 1080`, three of ten clips get **nothing**: they are 9:16 and height-bound by
`avail_h = canvas_h − y_offset = 1640`, so they land at **921×1639** and their 1080 gain is
**+0.0 pt**. The other seven are width-bound and reach 1079.

Measured on those three height-bound clips, magenta, `scale_width: 1080`:

| `y_offset` | picture box | dead canvas |
|---|---|---|
| **280 (shipped)** | 921 × 1639 | **27.2 %** |
| 160 | 989 × 1759 | 16.1 % |
| 80 | 1033 × 1839 | 8.4 % |
| **40** | 1057 × 1879 | **4.1 %** |

**−23.1 points**, on exactly the clips `scale_width` cannot help. Frames read
(`scratch/mb085_frames/yoff/compare.png`): the source's own caption survives at every offset, and
at 40 the frame is near full-bleed with the source's own white bar doing the job `white_frame`'s
margin used to do.

**The reason this is now available is the caption decision itself.** `y_offset: 280` reserves a band
for an overlay — `caption.y` is literally `"275-text_h"`. Default to no overlay and those 280px are
holding space for something that is never drawn.

**So `y_offset` should be a function of `caption.enabled`, not a constant.** Large when a caption is
drawn (the ~18.5%, if a caption worth drawing ever exists), small when it is not. Setting it small
unconditionally would push an overlay off the top of the frame on the day one is re-enabled.

---

## 5. What I got wrong

* **I shipped a patch that was already obsolete when I wrote it.** MEMEBOT-076 handed over
  `mb076_patch.diff` and recommended landing it. MEMEBOT-071 had committed a better fix ~2 hours
  earlier. My round did not check `git -C memebot log` before recommending — it checked the
  *claim*, saw the file held, and reasoned about the working tree. A claim tells you who is writing;
  it does not tell you what has already landed.
* **MEMEBOT-076's −15.3 pt canvas gain is superseded** by −6.6 pt (§3). Measured correctly, on code
  that has since changed underneath it.
* **My own sheet-builder hid a bug of exactly the kind this round is about.** Panel labels
  containing `F:TEXT` produced an unreadable ffmpeg error, because `:` terminates a `drawtext`
  option — a value that terminates its own syntax, which is the `strip_emoji` stray-colon trap in a
  different costume.
* **The `any_text` = 100%/100% result is close to meaningless** and is flagged as such rather than
  quoted as the detector's accuracy (§2).

---

## 6. Handed to MEMEBOT-082

1. **Do not apply `scratch/mb076_patch.diff`.** It is obsolete. Delete it.
2. **The routing signal is `scratch/mb085_detect.py::text_bands`**, rule `bands>0 AND top_band ≤
   0.35`, P = 91.3% / R = 95.5% against 27 hand labels in `scratch/mb085_labels.json`. Record it as
   a field; do not gate on it yet.
3. **The fallback population is 18.5% with no hook, not 19.3% with no text** — and the right
   answer for them is no caption, because our alternative is the reposter's rate card.
4. **Prefer `y_offset` to `scale_width`**: −23.1 pt vs +0.0 pt on the height-bound third of the
   corpus. Make it conditional on `caption.enabled`.
5. **Quote −6.6 pt for the 864→1080 trade, not −15.3 pt.**

## 7. Suites and spend

| suite | result |
|---|---|
| `memebot/scraper` live tree (incl. MEMEBOT-082 WIP) | **185 tests, OK** |
| parent `tests/run_all.py` | **144 of 146 suites green** (1301.7s, 146 discovered across 3 nested `tests/` dirs) |

Neither red is this round's, and both are attributable:

* **`tests/test_render_argv.py`** — the wiring guard firing on work in progress:
  *"edit.py accepts `--force-caption` and clip_pipeline neither passes it nor records why not"*.
  `--force-caption` appears **4 times in memebot's working tree and 0 times at memebot HEAD** — it
  is **MEMEBOT-082's** uncommitted flag, which is exactly what that guard exists to catch. This
  round rendered only against the HEAD export, which has no such flag.
* **`tests/test_track_title_tier.py`** — runs standalone as `Ran 0 tests … OK (skipped=1)`; a
  zero-collection suite, in the declared-track territory of MEMEBOT-077. Untouched here.

MEMEBOT-076's two reds (`test_claims_manifest`, `test_matcher_boundary`) are both **now green**.

**72 renders** this round (20 replication + 40 canvas + 12 `y_offset`) plus 81 source frames probed
across 27 clips for the detector. `$0.00`, no paid calls. Reproduce with `scratch/mb085_verify.py`,
`scratch/mb085_detect.py`, `scratch/mb085_canvas.py`; labels in `scratch/mb085_labels.json`;
frames and sheets under `scratch/mb085_frames/`.
