# MEMEBOT-082: ship the source's own hook, centre the picture, and stop eating the payoff word

**Date:** 2026-08-02 · **Type:** Fix + measure + decide · **Spend:** **$0.00** of a $0.10 budget (no paid calls) · `memebot/scraper/edit.py`, `templates.yaml` + tests

---

## SUMMARY

- **Shipped:** `white_frame` defaults to **no added caption**; a classifier drops the reposter's advertising when one *is* requested; `vertical_align: center` reclaims the vertical waste; the pad guard now covers both shift directions; `caption_hook` stopped deleting the last word; the content crop stopped decapitating the source's headline. memebot `ba0ce2b`, parent `a00eea6`.
- **The one number:** **20 renders, 0 containing a `drawtext`** — the source's own hook is what ships, and "POV: the friend who is supposed to be driving us home" now renders whole with nothing competing above it.
- **Off-brief:** the brief's fallback design cannot be built as specified — `vision_on_screen_text` being empty is **not** evidence of no on-screen text (MEMEBOT-076), so nothing may route on it. Two of the brief's premises came from my own MEMEBOT-071 and were wrong.
- **Got wrong:** MEMEBOT-071's "dead canvas 61.0%" was measured on a white canvas and counted the **source's** own white bars as template waste. True template pad was **29.2%**. My MEMEBOT-064 caption rule was also destroying every short hook, and my own test helper had a latent bug that hid it.
- **Still broken:** duration — 20 of 30 renders run over 30s, up to 91.6s (MEMEBOT-074), `memebot/scraper/edit.py`, not this round. Non-Latin captions render as `□□□□`.
- **Suite:** 195 green. Spend $0.00.

---

## 0. Two of this brief's premises were mine, and both were wrong

The brief says *"dead space is 61.0% not the ~45% previously believed"* and *"raising scale_width buys 6.6 points"*. Both numbers are MEMEBOT-071's — mine — and both are contaminated.

**MEMEBOT-076 caught the instrument error:** several source clips carry **their own white caption bar**, which on a white canvas is indistinguishable from the template's pad. My measurement counted flat-white and flat-black pixels as "dead canvas", so it summed the template's padding *and* the source's own letterbox *and* the source's own caption bar into one number and attributed all of it to the template.

Re-measured on a **magenta** canvas — a colour no source contains, so every magenta pixel is padding this template added and nothing else:

| | template pad | picture band |
|---|---|---|
| before (top-anchored, caption on) | **29.2%** | top 278, h 1549 |
| after (centred, caption off) | **22.6%** | top 144, h 1633 |

So the template was padding 29.2% of the canvas, not 61%. The remainder of what looked dead belongs to the source, and the content crop is what addresses that — a different mechanism with a different fix.

I have not re-litigated `scale_width`: the brief rules it out explicitly and the waste is vertical, which is where I fixed it. But the 6.6-point figure it cites should be treated as unreliable for the same reason, and MEMEBOT-076 measured 15.3 points with the better instrument.

---

## 1. The source's own overlay is now the default (item 1)

`white_frame` ships `caption.enabled: false`.

**Verified on 20 renders, frames read: zero contain a `drawtext` filter.** Read off those frames, the source's own captions now stand alone and whole:

> "POV: the friend who is supposed to be driving us home"
> "Jackie Chan ended up becoming the victim of the very fight he thought he could win."
> "I was just trying to record my gf during her track meet 😂😂"
> "Me watching her profile every day, but I can't text her:"
> "No one, me this winter :"

The first of those is the line that opened this whole thread of work — the one whose own caption was better than ours while ours sat truncated above it. It now ships alone.

### The watermark-versus-hook filter

`classify_caption()` sorts caption text into **ad / reference / watermark / hook**, and only `hook` is drawn. Measured over all 2,000 library captions, after the same headline+emoji reduction the renderer applies:

| verdict | count | share |
|---|---|---|
| hook | 1,046 | 52.3% |
| **ad** | 650 | **32.5%** |
| **reference** | 202 | **10.1%** |
| **watermark** | 96 | **4.8%** |
| empty | 6 | 0.3% |

**47.7% of the caption field is not a hook.** `ad` catches rate cards, DM-for-promo, follow-me lines, bios and credit/copyright boilerplate — MEMEBOT-076 found two accounts supplying six of ten rows that prefix *every* caption with a rate card or bio. `reference` catches the catalogue prose that dominated the earlier frames (`"Title: Two and a Half Men Created by: Chuck Lorre... Genre: Comedy, Sitcom Runtime..."`). `watermark` catches the bare brand mark.

It is **always on**, not a library function waiting for a caller: it runs inside `build_filter_chain` on the text that would actually be drawn, and a rejected caption produces **no `drawtext` at all** rather than an empty one. On this round's 20 clips, had captions been forced on, it would have blocked 8 of 20.

### The fallback, and why the brief's version cannot be built

The brief asks for *"a FALLBACK for the 19.3% of clips with no on-screen text at all"*, routed on `vision_on_screen_text`. **That routing is unsafe and I did not build it.** MEMEBOT-076 measured the reason: all four clips it selected *because* that field was empty turned out to carry full burned-in tweet cards. The field's fill rate is a **floor, not an estimate** — emptiness means "not detected", never "not present". Routing on `== ""` would strip the overlay decision from exactly the clips whose text the detector missed.

What ships instead is an explicit, loud fallback:

- `--force-caption` draws a caption on a captions-off template, and the classifier still guards it.
- Passing `--override-text` to a captions-off template now **prints why it is not being drawn** and how to opt in. That mattered: `clip_pipeline.render_one` passes `--override-text` on *every* render, so left silent it would have become a no-op that looks like a working feature — the exact shape this repo keeps rediscovering.

Automatic per-clip routing stays blocked on a **presence** signal that can be trusted, and that signal has to come from the pixels, not from the library field.

---

## 2. The vertical waste, reclaimed (item 2)

`y_offset: 280` reserved a caption band and anchored the picture beneath it. With the caption gone that band is 280px of nothing, and because the picture is anchored rather than centred, every pixel it does not use collects into a single slab of white at the bottom.

`vertical_align: center` gives the picture the whole canvas and splits the remainder. **Template pad 29.2% → 22.6%** (magenta, 8 renders each). The picture band grows from 1549 to 1633 rows and moves from top=278 to top=144.

`scale_width` is untouched at 864, as the brief directs. `vertical_align` defaults to `"top"`, so every other template is unaffected — and a test pins that.

---

## 3. The pad guard still fires, and it had a hole (item 3)

**Planted overflow, guard bypassed:**

```
shift=+0 -> top= 280 (pad asked for 280) placed
shift=+6 -> top= 140 (pad asked for 286) RE-CENTRED
```

**With the reserve in place:**

```
shift=+6 -> top= 286 (pad asked for 286) placed
```

The guard fires exactly as MEMEBOT-071 left it.

**But centring opened a second direction.** Reserving `max(0, shift)` is right for a top-anchored picture — only a downward shift can overflow, since an upward one has all 280px of `y_offset` to move into. Centred, `y = (canvas_h - ih)/2`, and a **negative** shift drives `y` below zero. That one does not re-centre; `pad` clamps it to 0 and crops the top instead — a quieter failure than the one this guard exists for. The reserve is now `abs(shift)` when centring, which makes `(canvas_h - ih)/2 >= |shift|` and holds both bounds.

**20 of 20 placements correct** across both alignments × both scale widths × five shifts.

**Anything else that can silently re-centre?** I checked the rest of the chain. `scale` with `force_original_aspect_ratio=decrease` only ever shrinks and cannot displace. `rotate` is called with `ow=iw:oh=ih`, so it preserves the frame and fills with the canvas colour. `pad` is the only filter in this chain that is handed a position it can decline, and it is the only one that declines silently.

---

## 4. Two live defects fixed on the way, both traceable to me

### `caption_hook` was deleting the payoff word

MEMEBOT-074 found it in a 30-render audit; I wrote it in MEMEBOT-064.

```
"Wait for it"                -> "Wait for…"
"lil bro pulled an ELITE"    -> "lil bro pulled an…"
"Hype is real"               -> "Hype is…"
```

It destroyed **5 of the 5 short human-written captions** — the only ones worth burning in at all. The rule was written to defend against a caller that hard-sliced at 90 characters, where a trailing `"per"` might be the front of `"perfecting"`. Applied at *any* length it was pure damage: **Instagram captions do not end in a full stop**, so "no terminator" is the normal shape of a real hook, not evidence of damage.

The caller is gone (MEMEBOT-071 removed the `[:90]`) and `clip_pipeline.clean_caption` truncates only above its budget, at a word boundary, with its own `"..."`. So a caption arriving under budget is provably intact. The rule now applies **only over budget**, where a severed tail is still possible.

### The content crop was still decapitating the headline, vertically

MEMEBOT-071 pinned the horizontal axis. `cropdetect` thresholds on luma at `limit=24` and the anti-aliased top rows of a glyph fall below it, so the box lands a few pixels *inside* the letterforms — renders read `"rIFA WORLD CUr"` and `"Kip Wheeler"`.

Sized from data rather than guessed (`scratch/mb082_croptop.py` compares the detected top against the first row carrying real ink):

- **9 of 11** local sources cut into ink, by **1–9 px**
- `CROP_EDGE_SAFETY_PX = 16` clears the worst case with headroom
- after: **0 of 11**, and **0 of the 11** cropped sources among this round's 20

Cost: 16px of retained black per vertical edge, against a letterbox trim measuring 174–608px on the same clips — under 2% of the win.

---

## 5. What I got wrong

**The 61.0% dead-canvas figure** (§0). Measured on a white canvas, so the source's own white caption bar counted as template padding. The instrument was reading itself. Corrected to 29.2% on magenta.

**A latent bug in my own MEMEBOT-064a test helper.** `assert_clean` ended with:

```python
self.assertFalse(nxt.isalpha() or nxt in "'’", ...)
```

`nxt` is `""` when the output consumed the whole reference — nothing cut, the best possible outcome. But **`"" in "'’"` is `True` in Python**, so a perfect result was reported as a mid-word cut. It never fired while `caption_hook` was eating the final token, because `nxt` was never empty. Fixing the caption rule made the test fail, and the test was wrong, not the fix. This is the third detector fault in three rounds on this code path.

**Six tests asserted contracts I deliberately changed** and had to move rather than be deleted: three pinned the unconditional last-token drop, three pinned exact crop boxes without the margin.

---

## 6. Still broken, and whose file

| What | Where | Status |
|---|---|---|
| **Duration: 20 of 30 renders over 30s, up to 91.6s** — MEMEBOT-074 calls this defect #1 | `memebot/scraper/edit.py` transform trims | Not this round; unclaimed |
| Non-Latin captions render as `□□□□` (Montserrat-Bold has no Arabic glyphs) | `edit.strip_emoji` / font selection | 2/30 unshippable, unclaimed |
| Automatic per-clip caption routing | needs a pixel-level presence signal | Blocked — `vision_on_screen_text` emptiness is not evidence (MEMEBOT-076) |
| The drop lands nowhere (2/17 within 0.25s of a scene cut) | song/beat placement | MEMEBOT-074, unclaimed |

**Not touched:** `memebot/scraper/edit.py` carries uncommitted work from other rounds (a duration-floor budget, an ambient-bed message), and `duck.py` / `duration.py` / `config.yaml` belong to them. I staged 8 of 11 hunks by filtering the diff and left the rest.

---

## Files

- `memebot/scraper/edit.py` — `classify_caption`, `_caption_survives_filter`, `CROP_EDGE_SAFETY_PX`, `vertical_align`, both-direction shift reserve, narrowed `caption_hook`, `--force-caption` (`ba0ce2b`, pushed)
- `memebot/scraper/templates.yaml` — `caption.enabled: false`, `vertical_align: center`
- `memebot/scraper/tests/` — `test_caption_fit.py` (+10), `test_edit_behaviour.py` (+3)
- `scratch/mb082_render.py` / `mb082_measure.py` / `mb082_croptop.py` (`a00eea6`)
- `scratch/mb082_frames/SHEET_shipped_1.png`, `SHEET_shipped_2.png` — the 20 read frames
