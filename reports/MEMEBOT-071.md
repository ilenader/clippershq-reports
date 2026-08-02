# MEMEBOT-071: two croppers were eating the source's caption, and `pad` was silently re-centring the frame

**Date:** 2026-08-02 · **Type:** Fix + measure + decide · **Spend:** **$0.00** of a $0.10 budget (no paid calls; ffmpeg and local library reads only) · `memebot/scraper/edit.py` + tests, `scratch/bl940_batch.py`

---

## SUMMARY

- **Shipped:** the parent's `[:90]` slice is gone; the zoom no longer crops; the content crop no longer trims the sides; `pad` can no longer silently re-centre the frame. memebot `b7eca8b`, parent `de2970c`.
- **The one number:** **30 renders, 90 frames, 0 misplaced, every source caption complete at both edges** — "Bro thought it was funny... until it wasn't" where it previously read "ought it was funny... until it wasn'".
- **Off-brief:** the brief named *one* crop; there were **two**, plus a third defect underneath — `pad` re-centres an overflowing input instead of refusing, which hit **4 of 30 renders (13%) including the shipped 864 geometry**. Dead canvas is **61.0%**, not ~45%.
- **Got wrong:** my first misplacement detector counted caption glyph rows as video and reported 20 of 30 broken; the real figure was 4. I also let two background sweeps be killed with their results held in memory.
- **Still broken:** dead canvas is still **53%** at best and the lever is vertical, not `scale_width` — `memebot/scraper/templates.yaml`, my claim, not shipped. The caption *text* decision needs a watermark-vs-hook filter that does not exist.
- **Suite:** 182 green in `memebot/scraper/tests`. Spend $0.00.

---

## 1. The parent slice (item 1) — removed

`scratch/bl940_batch.py:227` was:

```python
caption = (str(clip.get("caption") or "clip")[:90]) or "clip"
```

It is gone. The full caption now reaches `edit.py`, which owns the trim because it owns the typesetting — it has the font, the box and the sentence rule; the caller has none of them.

This mattered more than "redundant". MEMEBOT-064a's `caption_hook()` repairs a severed tail *when it can tell the text was severed*. A character slice destroys exactly that evidence: after `[:90]`, `"...in his hotel room per"` carries no signal distinguishing `per` from a real word. The downstream fix was working with damaged input for as long as this line stood.

---

## 2. The source's caption was being cut by TWO croppers (item 2)

The brief says "fix the crop". There were two, on the same axis, and neither was the one the earlier round named.

### 2a. The zoom was a crop

```python
if zoom > 1.0:
    prefix.append(f"crop=iw/{zoom}:ih/{zoom}")     # centred crop
```

`zoom: {min: 1.05, max: 1.20}` removes `(1 - 1/zoom)/2` at **every** edge:

| zoom | keeps | lost per side (1080px source) |
|---|---|---|
| 1.05 | 95.2% | 26 px |
| 1.10 | 90.9% | 49 px |
| 1.15 | 87.0% | 70 px |
| 1.20 | 83.3% | **90 px** |

90px is the "t" of "this" and the "m" of "messed".

**The zoom is now a scale.** It is carried to the scale step (`tx_zoom`) and enlarges the target box instead of cropping the source. This is free on `white_frame`: the video scales to 864 on a 1080 canvas, so 108px of margin sits unused on each side and the 1.20 ceiling asks for 1037 — still inside the canvas.

Per-render geometric variation survives: **10 distinct picture widths across 10 renders** at `scale_width: 864` (929, 934, 938, 942, 976, 979, 993, 996, 1010, 1023). The zoom still fingerprints; it just stopped paying for it with the product.

### 2b. The content crop trimmed the sides

This is the one that was still cutting text after 2a was fixed. `detect_content_crop` on clipcapture.tv's clip returned:

```
crop=988:1374:46:242        # 1080-wide source → 46 px off EACH side
```

and the frame read `"ought it was funny... until it wasn'"`.

**Why cropdetect gets this wrong:** a meme page's caption bar runs the full width of its frame, and the bar's outermost pixels *are* the dark bar. cropdetect reads them as letterbox and takes the first and last characters with them. The bar looks like padding and is actually the headline.

**The crop is now pinned to the full source width.** No benefit is lost, because the win this filter was built for is entirely vertical — its own docstring measures it as *"1080x1920 carrying 1080x820 of picture"*, full width, bars top and bottom. All ten sources now return `x=0, w=source_width`.

The cost is a genuinely pillarboxed source, whose side bars now survive into the pad. Rare on 9:16 reposts, cosmetic, and the right way to be wrong: keeping a black bar is recoverable, cutting the hook off a caption is not.

### 2c. Two tests had to move axis, and that is the finding

`test_content_crop.py`'s fixture varies **width only** (540 → 684px after 110s). With the horizontal axis pinned, a 90s probe and a full probe now return the same width — correctly and identically — so the fixture could no longer detect the bound MEMEBOT-050 exists to guard.

The guarantee is still real; it just lives on the vertical axis now. The fixture grows on **both** axes and the assertions read height. A third test was added asserting the horizontal pinning holds *across* a framing change, at every probe bound.

---

## 3. `pad` silently re-centres an overflowing input — the biggest find

Testing item 3 surfaced a defect that was **already shipping**.

`pad` places the video at `y = vid_y + tx_shift_y`. When that plus the video height exceeds the canvas, **ffmpeg does not refuse — it centres the input instead.**

MEASURED, 720x1280 source at `scale_width: 1080`:

| `position_shift_y` | expected top | actual top |
|---|---|---|
| −6 | 274 | 274 ✓ |
| 0 | 280 | 280 ✓ |
| **+6** | **286** | **140** ✗ |

The picture slides **146 px up**, into the caption band. The caption's black text then renders on the video's black background and is invisible. That is the frame I nearly shipped as evidence.

**It is not caused by `scale_width`.** At 864 a 9:16 source is *width*-bound and comes out 1536 tall, 104px short of `avail_h`, so a +8 shift had room. At 1080 the same source is *height*-bound and fills `avail_h` exactly, so every positive shift overflows. Raising `scale_width` only exposes it.

**Incidence: 4 of 30 renders (13%), and 2 of those were `v864cap` — the shipped geometry.** It fires whenever a clip is height-bound *and* the roll gives a positive `shift_y`.

`avail_h` now reserves the downward shift. All six shift × width combinations land exactly where `pad` says.

---

## 4. `scale_width` 864 → 1080 (item 3): measured, and I recommend **against** it

| | dead canvas | mean picture | distinct widths / 10 |
|---|---|---|---|
| MEMEBOT-064a baseline (zoom crops, 864) | 61.0% | 880 × — | — |
| **v864cap** (zoom scales, 864) | **59.6%** | 972 × 1092 | **10** |
| **v1080cap** (zoom scales, 1080) | **53.0%** | 1046 × 1177 | **4** |
| v1080nocap (1080, no caption) | 53.6% | 1050 × 1176 | 3 |

**What it buys:** 6.6 points of dead canvas.

**What it costs, all measured:**
1. **Most of the zoom's per-render variation.** `zoom_w` clamps to the canvas, so 6 of 10 renders collapse to exactly 1080 — 10 distinct widths become 4. The config's own comment says the ranges were "widened for 2025 TikTok detection floor (~70% similarity)", so this is spending the anti-detection budget to buy white space.
2. **The template does not hold unchanged.** `caption.x: 108` is documented as "matches video's left edge ((1080-864)/2)" and `max_width: 864` as "= video width". Both track the video; at full bleed they must become a deliberate gutter (I used 40 / 1000) or the caption sits inset under a full-width video.
3. **It makes the `pad` bug the common case** rather than an occasional one — now fixed, but it would have gone out first.

**Recommendation: keep 864.** 53% dead canvas is still bad, so 1080 does not solve the problem it was proposed for — and **the waste is vertical, not horizontal**. With the video top pinned at `y_offset: 280` and a mean picture height of 1177, roughly 460px of white sits below the picture and 280px above it: ~39% of the canvas, against ~3% left/right at 1080. The lever is vertical placement (centre the picture in the space below the caption, or shrink `y_offset` when the caption is short), not `scale_width`. Not shipped — it changes the composition of every video and belongs in a round that can measure the result.

---

## 5. The caption text (item 4): use the source's own overlay

### A note on the three options

"Use the source's own overlay" and "add nothing at all" are **the same render** — caption disabled — and differ only in whether the clip was *selected* for having its own hook. So the three strategies are two render sets, and I rendered both (20 caption-on across two geometries, 10 caption-off) and judged all three from those frames. I am flagging this rather than reporting a third set of identical pixels as independent evidence.

### What the frames show

8 of 10 clips carry their own burned-in caption. Now that both croppers are fixed, all 8 render complete. Every one is a better hook than ours:

| | ours (first sentence of the caption) | the source's own, in the same frame |
|---|---|---|
| c01 | The Macarena is a Spanish dance song by the duo Los del Río, released in the 1990s. | **This is how the world got the Macarena move** |
| c02 | In an Australian news segment covering the NFL… | **This anchor knew immediately she messed up** |
| c03 | I Love You Phillip Morris (2009) is one of Jim Carrey's most underrated and underappreciated films of all time. | **A criminally underrated and overlooked gem from Jim Carrey** |
| c04 | Title: Two and a Half Men Created by: Chuck Lorre, Lee Aronsohn Genre: Comedy, Sitcom Runtime… | **Bro thought it was funny... until it wasn't** |
| c06 | Dragon Lord (1982) Dragon is the mischievous son of a wealthy aristocrat in old China. | **Jackie Chan ended up becoming the victim of the very fight he thought he could win.** |
| c09 | Wrath of the Titans (2012) is a fantasy action film and the sequel to Clash of the Titans (2010). | **The fact that this is what an underperforming movie looked like in 2012.** |

Ours is a synopsis; theirs is a hook. On c03 they say the same thing and theirs does it in half the words — ours is redundant *and* longer.

### This is structural, not anecdotal

Across all 2,000 library captions, after `caption_headline` + `caption_hook`:

- median drawn length **128 characters**
- **21.1%** come out hook-shaped (≤60 chars)
- **54.0%** come out as prose (≥120 chars)
- 13.7% open with a handle, credit or promo line in the first 120 characters; 6.5% contain a copyright/fair-use disclaimer

The brief's example is real and appears **7 times verbatim**: `"@Moviezar posts the best movie memes on instagram daily 🎞️ Minions (2015) is an animated film that explores the origins of…"` — the account's promo line welded to an encyclopedia entry.

**No trimming fixes this.** The field is doing its job: `clip_library` stores `caption` at tier `DECLARED`, a faithful copy of the reposter's Instagram caption. It was never written to be a hook.

### The decision

**Use the source's own overlay. Add our caption only when the source has none.**

The signal already exists: `vision_on_screen_text` is populated on **1,617 of 2,003 clips (80.7%)**, and the samples are the right shape — `"Bro waited 9 months for this / Wait for it.."`, `"The She-Hulk we got / The She Hulk we wanted"`.

**I have not flipped the default, and that is deliberate.** Two things must exist first, and neither does:

1. **A watermark-vs-hook filter.** The same field also returns `"FANDANGO\nMOVIECLIPS"` and `"cinema club"`. Promoting a watermark as the hook is a worse failure than the current one, because it looks intentional.
2. **A fallback for the 19.3%** with no detected on-screen text. Those would ship bare.

The render path already supports it (`caption.enabled: false`) and I proved it renders correctly — v1080nocap, 10 of 10, frames read. What is missing is the *selection* rule, and shipping a default flip without it would trade a caption that is dull for one that is absent or wrong.

---

## 6. What I got wrong

**The misplacement detector.** My first pass flagged "first row >50% non-white" as the video top. With the caption on, dense black glyph rows exceed 50%, so it found the caption and reported **20 of 30 renders misplaced**. The real figure was **4**, found by taking the longest *contiguous* run instead. I nearly reported a 67% failure rate for a 13% one. The caption-off variant was the tell: it showed 1 of 10 where caption-on showed 9 of 10, and identical geometry cannot have different placement rates.

**Two background sweeps were killed with their results in memory.** The harness only wrote its JSON at the end, so finished ffmpeg work was discarded twice. It now writes after every render, and the resume reads that file. Cost: about 25 minutes of re-rendering.

---

## 7. Still broken, and whose file

| What | Where | Status |
|---|---|---|
| ~53% dead canvas; the lever is vertical placement, not `scale_width` | `memebot/scraper/templates.yaml` (`y_offset`, vertical centring) | **My claim.** Measured, not shipped — changes every video's composition |
| Caption text is the reposter's feed prose | selection rule over `vision_on_screen_text` | Decided (§5), blocked on a watermark filter + a 19.3% fallback |
| `scale_width: 1080` collapses zoom variation 10 → 4 | `memebot/scraper/edit.py` | Inherent to full-bleed; the reason to keep 864 |
| c08 undecodable audio (xHE-AAC) | source media | Pre-existing, ~35.5% of clips, fails identically in all three variants |

**Not touched:** `memebot/scraper/edit.py` also carries **uncommitted work from another round** (a duration-floor budget and an ambient-bed message), and `duck.py` / `test_duck.py` belong to MEMEBOT-066. I staged only my five hunks by filtering the diff and left the rest in the working tree.

`tools/commit.py` refused a bare `git commit` with 11 rounds in flight — correctly: it commits the shared index, not what you staged. Committed via the pathspec form.

---

## Files

- `memebot/scraper/edit.py` — zoom-as-scale, `tx_zoom`, full-width content crop, `avail_h` shift reservation (`b7eca8b`, pushed)
- `memebot/scraper/tests/` — `test_edit_behaviour.py` (+3), `test_caption_fit.py` (+2), `test_content_crop.py` (axis move +1)
- `scratch/bl940_batch.py` — the `[:90]` slice removed (`de2970c`)
- `scratch/mb071_render.py` / `mb071_analyse.py` / `mb071_measure.py` — three-variant harness, pixel geometry, baseline
- `scratch/mb071_frames/` — 90 frames, `SHEET_v864cap_top.png`, `SHEET_v1080cap_top.png`, `SHEET_v1080nocap_top.png`
