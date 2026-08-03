# MEMEBOT-118 — three of the four named caption defects were never caption defects

**Write-blocked on `memebot/scraper/edit.py` and did everything else.** MEMEBOT-117 claimed
it at 11:40:28 for the **pillarbox** class, two minutes before this round started. I did not
add a second claimant. Every finding below is read-only: sources re-rendered at HEAD, frames
read by eye. **No fix landed.** memebot suites **253/253 green**.

---

## The method, and why it matters here

MEMEBOT-108 rendered a **pinned worktree** at `memebot fbeb1ec` (MEMEBOT-094) — not the
then-current tree. Its 30 source mp4s survive in `scratch/mb108_work`, so every case here was
re-rendered at **current HEAD from the same source file** and both frames were read.

**No glyph detector was trusted.** The brief lists four that were wrong in this exact area
(20-of-30 against a real 4; 7 flagged with 4 false; `"the young c"` passing a mid-word check;
a non-white bbox counting glyphs as picture). Frames were read directly.

---

## 1. The four named cases at HEAD

| # | clip | MEMEBOT-108 said | verdict at HEAD |
|---|---|---|---|
| 6 | `3920114711639315624…` | caption truncated with an ellipsis | **never our defect** |
| 28 | `3950695051654151195…` | caption LEFT-sliced, loses the H | **reproduces, 4 of 8 (50%)** |
| 1 | `3899882050747343299…` | no caption of ours drawn | **source has no text** — not a drawing failure |
| 7 | `3926681198499934620…` | no caption of ours drawn | **correct behaviour** — source text present and intact |

### #6 — the ellipsis was already in the source

The decisive frame is the **source mp4 before any of our processing**. It already reads:

> *Bro really blamed a raccoon for breaking…*

**The meme page truncated its own caption.** Our renderer drew nothing at all — captions have
been OFF by default since MEMEBOT-082 (the source's own burned-in text is the hook), and the
clip's `edit-*.log` carries no drawtext line.

So the answer to "find THIS cause, do not assume it is one of the three known lineages" is
that **there is no cause in our code**. It is not the caller's `[:90]` slice, not
`caption_hook` eating a terminator-less last word, not a stray colon from `strip_emoji`. The
truncation is upstream of us and it is the product we chose to preserve.

MEMEBOT-108 was reading a finished frame and attributing burned-in text to the renderer. That
attribution is the defect worth recording — at the moment the default flipped to
"ship the source's own hook", every burned-in flaw became ours by appearance and none of them
by cause.

### #28 — real, ours, and stochastic

The source reads **"Hostage takers demand a getaway car or they will execute everyone"** —
complete, H present. Our render loses characters.

**`build_transform_filters` does `rng = random.Random()` — fresh entropy per render.** So a
single re-render proves nothing; it is one sample of a random process. My first re-render came
back clean and would have supported "already fixed". Eight renders of the same clip at HEAD:

| run | zoom | rotation | result |
|---|---|---|---|
| 01 | 1.0811 | +0.418 | **cut** — `getaᴡ` (right) |
| 02 | 1.1368 | +0.167 | clean |
| 03 | 1.0618 | +0.275 | clean |
| 04 | 1.1481 | +0.320 | **cut** — H (left) |
| 05 | 1.1467 | +0.570 | clean |
| 06 | 1.1978 | −0.059 | **cut** — `ᴜstage … getᴀ` / `everyonᴇ` (BOTH ends) |
| 07 | 1.1206 | −0.485 | clean |
| 08 | 1.0881 | +0.260 | **cut** — H (left) |

**4 of 8 = 50%.**

**Zoom alone does not predict it** — 1.0811 was cut and 1.1467 was clean. The transform block
rolls **zoom 1.05–1.20, rotation ±0.8°, and position shift ±8px** independently, and the
source's own caption sits only ~70px from the frame edge. The combined geometry consumes that
margin. This is the anti-duplicate fingerprint transform eating the hook — the same trade
MEMEBOT-071 identified when it converted zoom from a crop to a scale for exactly this reason,
and MEMEBOT-064a read off a frame as *"his anchor knew immediately she / essed up"*. **That
fix was already in MEMEBOT-108's pinned commit.** The remaining margin loss comes from the
other two terms, which were never part of that fix.

**Whose class is this?** The slicing mechanism is horizontal geometry, which is
MEMEBOT-115's and now MEMEBOT-117's territory, not a caption path. I am naming it rather than
patching it.

---

## 2. The no-caption split — 0 of 2 are drawing failures

The brief asked to separate "source has no burned-in text" (not a bug) from "drawing failed"
(a bug). Both named cases read cleanly:

- **#7 — source text present and intact.** The HEAD frame carries the source's own hook,
  *"One of the Most Cinematic Standoffs Ever Put on Television."*, complete and legible.
  Drawing nothing is **correct**. What MEMEBOT-108 actually saw — "a thin letterboxed strip
  under ~45% dead black" — is real, and it is the **pillarbox class**, not a caption class.
- **#1 — no text anywhere.** No source caption, no overlay, no hook at all. Its stored caption
  is a 1,160-character catalogue blob (`Main Cast:` / `IMDb:` / `Streaming on:`) correctly
  rejected as unusable. **Nothing failed to draw; there was nothing worth drawing.**

| | n |
|---|---|
| source has no burned-in text (product gap, not a bug) | **1** |
| source has text, overlay correctly absent | **1** |
| **drawing failed (the actual bug)** | **0** |

#1 is a genuine product gap — a video shipping with no hook — but it belongs to selection
(refuse clips whose source carries no hook and whose caption is a catalogue blob), not to the
renderer.

---

## 3. Non-Latin refusal is firing

`edit.unrenderable_script` returns the offending character for every script the brief names
and `''` for Latin:

| CJK | Kana | Hangul | Thai | Devanagari | Latin |
|---|---|---|---|---|---|
| `这` | `こ` | `이` | `น` | `य` | *(passes)* |

Wired into selection at `clippershq/clip_pipeline.py:379-381`, which appends
`"caption script unrenderable: <script name>"` as a refusal reason — **refused by name**, as
the brief requires. Both shipped fonts (`Inter-Bold.ttf`, `Montserrat-Bold.ttf`) are present.
No boxed frame appeared in any frame I read.

---

## What I did NOT do

- **Item 6 — 20 renders with per-class counts before and after — was not done.** I spent the
  render budget establishing that #28 is stochastic (8 renders of one clip), which changed
  the question: a before/after count over 20 clips at n=1 each would have measured the dice,
  not the code. A correct version needs repeated renders per clip and is a larger job than
  this round had left.
- **No fix landed.** `edit.py` is MEMEBOT-117's. The surviving defect is horizontal geometry,
  which is that round's own class — it should take it with this measurement in hand.

## A mistake I made

Running `edit.py` against MEMEBOT-108's per-clip configs **overwrote four of that round's
finished renders**: `output_dir` in those configs is an absolute path back into
`scratch/mb108_work`. I noticed after the fourth. Scope: 4 of 30 outputs, in an **untracked**
scratch directory, nothing committed; MEMEBOT-108's actual published evidence — the 90 contact
sheets in `scratch/mb108_sheets/` — is untouched, and I had already captured the pre-overwrite
frames for exactly those four clips. Every later render redirects `output_dir` into a private
work dir first (`scratch/mb118_cause.py`).

---

## SUMMARY

```
MEMEBOT-118 — three of the four named caption defects were never caption defects.
#6  "caption truncated with an ellipsis" is in the SOURCE mp4 before we touch it. Captions are
    OFF by default; the renderer drew nothing. Not one of the three known lineages -- no cause
    in our code at all.
#28 IS ours and REPRODUCES: 4 of 8 renders at HEAD lose characters, one losing BOTH ends. The
    transform block rolls fresh entropy per render (zoom 1.05-1.20, rotation +/-0.8, shift
    +/-8px) and eats the source caption's ~70px margin. Zoom alone does NOT predict it.
NO-CAPTION SPLIT: 0 of 2 are drawing failures -- 1 source has no text at all (a selection gap),
    1 has its hook present and intact (correct behaviour; its real defect is the pillarbox).
NON-LATIN: refusal fires, names the script, wired at clip_pipeline.py:379-381. No tofu shipped.
NOT DONE: the 20-render before/after count, and no fix -- edit.py is MEMEBOT-117's. Suites 253/253.
```
