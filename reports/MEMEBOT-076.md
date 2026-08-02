# MEMEBOT-076 — the caption text is the reposter's business, and the crop deletes the joke

**112 renders across six arms, every one read as frames. The recommendation is (a): keep the
source's own burned-in caption and add no overlay. The blocker to (a) was never the caption
layer — it was a centred zoom crop that was destroying the very text (a) preserves, on 7 of 10
clips. That is fixed and measured, 7/7 restored.**

---

## 0. Preconditions — this brief was already in flight

`tools/claims_read.py --holders memebot/scraper/edit.py` returned **MEMEBOT-071**, not FREE.
Its intent line was this brief almost word for word:

> Remove parent [:90] slice; fix source-caption horizontal clip; measure scale_width 864->1080;
> decide caption strategy by reading frames. Budget $0.10, no paid calls.

It was 58 minutes in, and `memebot/scraper/edit.py` had been written **1.7 minutes** before this
round started (+180/−10 uncommitted, a new `_floor_trim_budget()` not at HEAD). By the end of
this round it had also taken `tests/test_caption_fit.py` and `tests/test_content_crop.py`.

Claims are advisory, so this was put to the operator, who chose the read-only path. **Nothing
inside `memebot/` was written by this round.** Every render ran against a
`git archive HEAD` export at `scratch/mb076_head/`, so a working tree moving under the
experiment could not contaminate it. `MEMEBOT-073`, `074` and `075` were all claimed within five
minutes of this round starting; this is `076` and its prefix is `mb076_`.

Spend **$0.00** — no paid calls. All 112 renders are local ffmpeg.

---

## 1. The strategy experiment

Ten clips × five arms, plus three follow-up arms the main run could not answer.

| arm | what goes on screen | overlay | zoom |
|---|---|---|---|
| **a_source** | nothing — the source's own burned-in caption | no | 1.000 |
| **b_sentence** | first sentence of the scraped caption | yes | 1.125 |
| **c_vision** | first clause of `vision_scene` | yes | 1.125 |
| **d_none** | nothing | no | 1.125 |
| **e_hook** | `caption_hook(caption, 180)` — MEMEBOT-064a | yes | 1.125 |
| *ftop* | nothing, top-anchored crop (the fix) | no | 1.125 |

**The only variable is the caption text.** `edit.py:1044` rolls zoom, brightness, saturation,
gamma, rotation, shift and eleven more from an unseeded `random.Random()`, which is right for a
repost bot and fatal for an A/B — two arms would differ in fifteen ways and no frame could be
attributed. Every transform is pinned to a scalar, which `config.yaml` explicitly permits.

Arm (a) is the one deliberate exception at zoom=1.000, because "preserve the source's caption"
cannot mean "add no overlay and centre-crop 5.6% off every edge anyway". That makes **(a) vs (d)
a clean single-variable pair of its own** — both add no overlay, and they differ only in the
crop.

### What the ten scraped captions actually say

This is the finding. The mechanics are fixed; the text is somebody's marketing.

| # | clip | what (b)/(e) put on screen | class |
|---|---|---|---|
| 1 | `2940892612…` @moviezar | "Wait for it 😭 - (Credit: @kayshhabarrett)" | credit line |
| 2 | `3450422996…` @cawncept | "Story promotion 49₹ ✅ Maintain a healthy lifestyle ⬇️ 1. Eat a balanced diet…" | **price list** |
| 3 | `3457699377…` @moviezar | "Can someone explain to me why she ran off the track?" | **genuine hook** |
| 4 | `3483791661…` @self_respect_club | "#spiderman #trendingreels #viral #single #reels" | hashtags only |
| 5 | `3496888229…` @cawncept | "DM for paid promo starting at just 49₹ ✅ The art of decision making 👇…" | **advert** |
| 6 | `3629145006…` @cawncept | "Story promotion at just 49₹ 📈 He could've ended it all…" | **advert** |
| 7 | `3665688194…` @memes_literallyme | "Real #literallyme #memes #me #real #relatable #ryangosling…" | one word + tags |
| 8 | `3700336049…` @moviezar | "@Moviezar posts the best movie memes on instagram daily 🎞️ Kraven the Hunter (December 2024) is a gritty and somber superhero origin story…" | **bio + Wikipedia** |
| 9 | `3704370692…` @solidshampooz | "Justice for 68 #batman #batmanmemes #legobatman…" | 3 words + tags |
| 10 | `3707586922…` @cawncept | "🎬 Fact: The movie Deep Water (2022), starring Ben Affleck and Ana de Armas, was originally shot in 2019…" | unrelated trivia |

**1 of 10 is a hook. 9 of 10 are the reposter's own business.** Row 8 is the brief's example,
reproduced exactly. Two accounts (`@cawncept`, `@moviezar`) account for six rows, and both prefix
every caption with a rate card or a bio — this is not noise, it is what a repost page's caption
field is *for*.

### And the source's own text is better in 9 of 10

| # | source's burned-in caption |
|---|---|
| 1 | "Bro waited 9 months for this 💀" |
| 2 | "No one, me this winter :" |
| 3 | "I was just trying to record my gf during her track meet 😂😂" |
| 4 | "Me watching her profile every day, but I can't text her:" |
| 5 | "Who's your favourite ?" |
| 6 | "Master Oogway could've defeated Kai / but he left that for the panda" |
| 7 | "\"Boys don't have feelings, they never talk about anything\" / Me and bro talking about family, crush and old memories at midnight" |
| 8 | "You can't cheat his nose lol" |
| 9 | "68 after 67 and 69 both got famous:" |
| 10 | "That one super hygienic guy with his girlfriend" |

Every one is a setup written by someone whose job is writing setups. On clip 3 — the only clip
whose scraped caption is a real hook — the two are equally good and the overlay is redundant.

### The verdict, arm by arm

* **(a) source preserved — WINS.** Nine of ten clips already carry a better hook than anything we
  can add, burned into the frame, in the source's own type. Adding an overlay above it produces
  two competing headlines; on clip 1 the overlay renders "Wait for it…" directly above the
  source's own "Wait for it .." — the same words, twice, in two fonts.
* **(d) no caption — second, and nearly the same thing.** Identical to (a) except for the crop.
  It is the honest fallback where a clip genuinely has no burned-in text.
* **(c) vision clause — third. Harmless, useless.** "A man in a suit walks past a woman in a fur
  coat." describes what the viewer can already see, in machine register. It never embarrasses the
  account, and it never earns a stop. It also truncates: "A group of people in…", "A funeral
  scene where a man is dramatically interacting with a…".
* **(b) first sentence — fails.** Publishes the rate card. Also cuts badly on its own terms:
  clip 1 renders "Wait for it 😭 - (Credit" — an unclosed parenthesis, because a naive
  clause-boundary rule stops at the colon in "(Credit:".
* **(e) caption_hook — fails identically, and that is the point of item 2.**

---

## 2. `caption_hook()` evaluated, not assumed

MEMEBOT-064a shipped it as a proposal. Measured as arm (e):

**Typographically it is flawless.** Across all 30 overlay renders:

| check | result |
|---|---|
| mid-word cuts (prefix alignment, not token lookup) | **0 / 30** |
| leading punctuation after `strip_emoji` | **0 / 30** |
| output not a prefix of its input | **0 / 30** |
| caption ending on a lone letter | **0 / 30** |
| `"🎥🎬: The Legend of Hei II (2025)"` | → `"The Legend of Hei II (2025)"` ✓ |
| `"4.4M views and counting. It was wild."` | → unchanged, the `M` survives ✓ |

**Semantically it changes nothing.** It is a typesetter, and the defect is editorial. On 3 of 10
clips its output is **byte-identical to the dumb first-sentence rule**, including the brief's
`@Moviezar` bio at 177 characters. Where it differs it is usually *worse for this purpose*,
because keeping whole sentences within a 180-char budget means it publishes **more** of the ad:

| clip | (b) first sentence | (e) caption_hook |
|---|---|---|
| 2 | 56 chars | **169 chars** — the entire six-point listicle |
| 5 | 97 chars | **171 chars** |
| 6 | 55 chars | **149 chars** |

**Keep `caption_hook`.** It is correct, it is the reason there are no mid-word cuts left, and any
strategy that ever puts scraped text on screen needs it. It is simply not a fix for *this* defect
and must not be mistaken for one.

---

## 3. The crop — root cause, and the fix, measured

`edit.py:1068` at HEAD:

```python
if zoom > 1.0:
    prefix.append(f"crop=iw/{zoom}:ih/{zoom}")
```

`crop=w:h` with **no `x`/`y` is centred** — ffmpeg defaults `x=(iw-ow)/2, y=(ih-oh)/2`. Over the
shipped range `zoom: {min: 1.05, max: 1.20}` that removes **2.4%–8.3% off every edge**. At the
pinned midpoint 1.125 on a 1080×1920 source: **60px left, 60px right, 106px top, 106px bottom.**

**The brief describes the horizontal case; the dominant failure is vertical.** A meme's caption
band sits at the very top of the frame, and 106px eats most or all of it. Read from frames,
10 clips, arm (a) zoom=1.000 vs arm (d) zoom=1.125, no overlay in either:

| outcome | n | example |
|---|---|---|
| **first line deleted entirely** | 4 | "Master Oogway could've defeated Kai / but he left that for the panda" → "but he left that for the panda" |
| **line clipped through the letterforms** | 2 | "Me watching her profile every day," rendered with its ascenders sliced |
| **whole caption bar gone** | 1 | "Who's your favourite ?" absent |
| survived intact | 3 | "You can't cheat his nose lol" |

**7 of 10 damaged.** Clip 6 is the clearest harm: the crop deletes the *setup* and keeps the
*punchline*, which is not a degraded joke, it is an incoherent one.

### The fix

```python
prefix.append(f"crop=iw/{zoom}:ih/{zoom}:(iw-ow)/2:0")
```

Anchor `y=0`. The vertical cut moves entirely to the bottom, where meme sources carry padding,
watermarks or nothing. **It removes exactly as much area as before, so the transform's
fingerprint value is unchanged** — only where the loss lands. The horizontal cut is deliberately
left centred: it is the smaller of the two (60px vs 106px) and burned-in captions are
horizontally centred with margin far more often than vertically.

**Measured, not proposed: 10 clips re-rendered top-anchored, frames read. 7 of 7 damaged clips
restored, 0 of 3 survivors regressed. 10/10 now carry their source caption intact.**

Full diff: `scratch/mb076_patch.diff`. It applies to `memebot/scraper/edit.py` and is **handed to
MEMEBOT-071**, which holds that file — this round did not land it.

---

## 4. The dead canvas, measured before and after

Measured on a **magenta canvas** (`0xFF00FF`), not white. Measuring "how white is the frame" is
unsound on this corpus: several sources carry their *own* white caption bar, which is
indistinguishable from the template pad and gets silently counted as dead. Non-magenta is
picture, exactly.

| `video.scale_width` | mean picture box | mean dead canvas | picture area |
|---|---|---|---|
| **864 (shipped)** | 864 × 1002 | **58.2 %** | 41.8 % |
| **1080** | 1032 × 1169 | **42.9 %** | 57.1 % |

Raising it buys **15.3 points of dead canvas back, and +36.6% relative picture area**. Per-clip
the gain runs −8.6 to −21.4 points.

**Two things the key alone does not tell you.**

1. **It does not bind on tall sources.** Three of ten clips are 9:16 and are capped by
   `avail_h = canvas_h − y_offset = 1640`, not by width. They go 863 → **921** px, not 1080, and
   keep their white side margins. The remaining constraint on those is `y_offset: 280`.
2. **The template's identity does not survive on the other seven.** At 1080 the white side
   margins vanish and `white_frame` becomes full-bleed — visually a different template, and one
   that already exists (`gainzalgo` is `scale_width: 1080`). The result is a template that looks
   like two different templates depending on source aspect. `templates.yaml` already calls this
   "a template redesign and a taste call, so it is left to you", and this round leaves it there —
   now with the number attached.

---

## 5. What I got wrong, and what the brief has slightly wrong

* **My first bounding-box measurement was the instrument reading itself.** I measured "dead
  canvas" as the non-white bbox and reported (c) at 51.9% dead vs (d) at 62.7% — as if the vision
  caption had *added picture*. It had not: the caption text is non-white, so it extended the
  bounding box. Redone on magenta with the caption layer off.
* **I eyeballed a size difference that was not there.** Arm (a)'s picture looked narrower than
  (d)'s in the 5-up. Measured, the widths are 863 vs 856 px — the zoom does not shrink the output
  at all, it *magnifies the source* so the same 864px window shows a narrower slice. My (a)-vs-(d)
  width table is the wrong instrument for the crop and is reported only to retire it.
* **My sample was 10/10 with burned-in text, not the 7/3 mix I designed.** The 9–25s duration
  window removed every without-text candidate and a fallback branch silently refilled from the
  with-text pool — a bias in favour of my own recommendation. Fixed by rendering the missing cell
  (4 clips, 3 arms).
* **A pin that matched nothing looked exactly like a pin that worked.** The first full run lost
  20 of 50 renders because I pinned invented key names (`input_seek_sec`) behind `if key in tx`.
  The rolled trim stayed live, four clips fell under the 8.0s duration floor, and `edit.py`
  refused them with `rc=1` and an **empty stderr**. The pin loop now raises on an unknown key.
* **The brief's "~45% is padding" is low.** Measured on delivered frames it is **58.2%**.
* **`vision_on_screen_text` is not trustworthy as a "has burned-in text" flag.** All four clips
  selected *because that field was empty* turned out to carry full burned-in tweet cards —
  "@Moviezar / The first time Spider-Man used his 'Spidey sense':", a two-bar PopBuzz card, and
  so on. The field is under-filled. Any rule that routes on `on_screen_text == ""` will
  mis-route; the library's 73% with-text figure is a floor, not an estimate.

---

## 6. Recommendation

1. **Ship (a): no overlay. Preserve the source's own caption.** It wins on 9 of 10 clips and it
   is free.
2. **Land the top-anchored crop first.** (a) is worthless without it — the shipped crop was
   deleting the text (a) exists to preserve on 7 of 10 clips.
3. **Fallback where a clip genuinely has no burned-in text: (d), no caption.** Not (b), and not
   (e). Publishing the rate card is worse than publishing nothing. Use (c) only if a caption is
   considered mandatory — it is inert rather than harmful. **Do not gate this on
   `vision_on_screen_text`;** it is under-filled (§5).
4. **Keep `caption_hook()`.** It is correct and it is why there are no mid-word cuts left. It is
   not a fix for this defect.
5. **`scale_width` 864 → 1080 is a real 15.3-point win** and remains the operator's taste call,
   with `y_offset: 280` as the next binding constraint on tall sources.

---

## 7. Suites and reproduction

| suite | result |
|---|---|
| `memebot/scraper` live tree (incl. MEMEBOT-071's WIP) | **182 tests, OK** |
| patched snapshot `scratch/mb076_head/scraper` | 171/172 — the one failure is `test_resolve_asset_also_tries_the_repo_root`, which **fails identically on a pristine unpatched export** (`REPO_ROOT = ROOT.parent.parent` cannot see `memebot/scraper/config.yaml` from a relocated tree). Not caused by the patch; proven against a clean second export. |
| parent `tests/run_all.py` | see summary block |

Reproduce: `scratch/mb076_strategies.py` (selection + the five strategies),
`scratch/mb076_render.py` (pinned-transform harness), `scratch/mb076_sheets.py` (contact sheets),
`scratch/mb076_canvas.py` (magenta canvas measurement). Frames and sheets in
`scratch/mb076_frames/`. 112 renders, `$0.00`.
