# MEMEBOT-089 — 21 of 21 verified four ways, 0 of 21 postable, and the caption is now the blocker

**Date:** 2026-08-02 · **Class:** Viewing audit · **Spend:** **$0.0084** of a **$0.30** budget · 21 renders, 26 minutes of rendering

Preconditions read before any write: `tools/claims_read.py --holders` per target **and**
`git status --porcelain` with the second column read as *unstaged mid-edit*. Claimed as
`MEMEBOT-089`, eleven repeated `--write` flags, no path conflicts. This round wrote nothing
outside `scratch/` and its own claim.

---

## 0. THE PRECONDITION DECIDED THE METHOD

Every module that makes a video was **unstaged mid-edit** when this round started:

| file | holder | state |
|---|---|---|
| `memebot/scraper/edit.py` | MEMEBOT-082 | ` M`, **+360 lines**, mtime 16:44 |
| `memebot/scraper/templates.yaml` | MEMEBOT-082 | ` M` |
| `memebot/scraper/config.yaml`, `duration.py` | MEMEBOT-086 | ` M` |
| `clippershq/clip_pipeline.py` | MEMEBOT-088 | ` M`, mtime **16:50** |
| `clippershq/song_library.py`, `scratch/songs.json` | MEMEBOT-088 | ` M`, songs.json **1,719 lines changed** |

Rendering that tree would have judged three rounds' half-finished code and published the
verdict as an assessment of what landed. So this renders a **pinned HEAD snapshot** — a
detached `git worktree` of memebot at `b7eca8b` (MEMEBOT-071's crop fix, the one the brief
names) plus HEAD copies of the parent modules and HEAD's song store. That is what a fresh
clone gets, and the next round can reproduce it from the same commit.

**One trap this created, caught before any money was spent.** The pinned `clip_pipeline`
computes `_REPO_ROOT` from its own location, so `ledger_song_path()` would have spelled every
song `../../memebot/scratch/song01.mp3` and **every join key would have missed**. The driver
overrides `_REPO_ROOT` and then *asserts the spelling against the store before rendering*.

---

## 1–2. TWENTY-ONE RENDERS, VERIFIED FOUR WAYS

**21 attempted, 21 finished, 0 failed.**

| check | result |
|---|---|
| file exists, ffprobe reads video **and** audio | **21 / 21** |
| clears edit.py's 8.0s floor | **21 / 21** |
| carries the **configured** track (40–250 Hz signed correlation, every other store track as the null) | **21 / 21** |
| join key resolves **and** the record says `joinable` | **21 / 21** |

```
r bounded  min / median / max : 0.3914 / 0.8677 / 0.9957
margin over the best null     : min 0.19   (bars: r >= 0.25, margin >= 0.10)
```

Correlated against the **applied** window, not the marked hook — MEMEBOT-073 read 11 of 20 as
missing their song by using the hook, and the failures were all long clips, which reads
exactly like a real defect.

**The lag bound removed nothing, and I am reporting that rather than claiming a catch.** The
search was bounded to one hook period, since the bed is `aloop`ed and every alignment that
can physically occur is inside one. Measured against an unbounded search: **max difference
+0.0000 across all 21**. The bound is a guarantee that this batch did not need — it did not
rescue a single row, and saying it caught something would be false.

---

## 3. WHAT THEY ACTUALLY LOOK LIKE

**All 21 were watched** — a six-frame contact sheet each, read one at a time, plus a
source-versus-output comparison for the defect below.

| defect, hand-read | count |
|---|---:|
| **caption is a truncated synopsis, cut mid-sentence with an ellipsis** | **17 / 21** |
| source's own headline sliced by our transform | **12 / 21** |
| dead canvas ≥ 30% of the frame | 11 / 21 |
| over 30 seconds | 15 / 21 |
| competitor watermark on screen throughout | 7 / 21 |
| non-English caption or burned-in subtitles | 5 / 21 |
| caption renders as empty boxes | 1 / 21 |
| a still image with a soundtrack, not a clip | 1 / 21 |
| **in the 7–15s repost band** | **2 / 21** |

Durations **8.5 / 54.9 / 86.8s** (min/median/max). Blank canvas median **34.7%**, max 52.1%.

### The caption is the new headline defect, and it is not a truncation bug

MEMEBOT-074 fixed mid-word cuts and the deleted trailing word. What ships now is worse in a
way neither of those measured: **the caption is the source's description field** — title,
year, genre list, plot synopsis — hard-cut with an ellipsis.

```
"Gladiator (2000) - Russell Crowe reveals the last-minute script changes Movie Genre:
 Historical Drama, Action, Epic…"

"The Simpsons (1989) - Ned Flanders' Suppressed Rage Therapy TV Series Genre: Animated
 Sitcom, Satire, Comedy…"

"I'm sorry for the Batman…"          <- five words, then it stops
```

The one video with a real hook shows the shape exactly: *"She followed her dreams — and bent
the rules doing it." Bend It Like Beckham (2002) Story: Jess, a young…* — a usable first
line, then metadata, then an ellipsis. **The hook is in there and the pipeline buries it.**

### The sliced headline is OURS, and here is the proof

I did not want to attribute this from the output alone, so I pulled the **staged source** for
one of the twelve and compared the same frame:

```
SOURCE : "Police officer demands the suspect / show his hands immediately"
         intact, with generous black space above it
OUTPUT : the same two lines with the TOP ROW OF GLYPHS CLIPPED,
         and our caption panel butted directly against them
```

The source is clean; the output is cut. **The crop still eats into the source's own text
after MEMEBOT-071's 106px fix**, and our caption panel now collides with what survives.

---

## 4. THE VERDICT: **0 of 21**

**Not one of these would go out on a 100k repost page as rendered.** The last audit judged
3 of 30, and all three were static graphics from one account.

Two are close and worth naming, because they say what "close" costs:

- **`3750637685862205222` (Bend It Like Beckham, 37.3s)** — full-bleed, headline intact, no
  watermark, English, song verified. **One caption edit away.** Its first line is a real
  hook; everything after it is machine spill.
- **`3916628187392010037` (14.7s)** — the right length, a genuine narrative beat, a complete
  caption. Blocked by a **competitor's logo on screen throughout** and Portuguese.

### Ranked by how many videos each problem blocks

| # | problem | videos | whose file |
|---|---|---:|---|
| 1 | caption is scraped metadata, ellipsis-truncated | **17** | the caption builder — `clip_pipeline` caption field / the walk that stores the description |
| 2 | source's own headline sliced by the crop | **12** | `memebot/scraper/edit.py` (held, MEMEBOT-082) |
| 3 | duration 2–6× the repost norm | **15** | `clip_pipeline` — no upper trim; `MAX_DURATION_S` is 90 |
| 4 | dead canvas ≥30% (square source on a 9:16 canvas) | **11** | `templates.yaml` / the fitter (held, MEMEBOT-082) |
| 5 | competitor watermark left on screen | **7** | nothing addresses this today |
| 6 | non-English content selected at all | **5** | the gate — no language term |
| 7 | non-Latin caption renders as boxes | **1** | the font in `templates.yaml` |
| 8 | a still image selected as a "clip" | **1** | the gate — no motion term |

---

## 5. AGAINST MEMEBOT-074'S LIST, DIRECTLY

| MEMEBOT-074 | then | now | verdict |
|---|---|---|---|
| song present | 27/30 | **21/21** | **FIXED** |
| mid-word caption cuts | 0/30 | **0/21** | **stays fixed** |
| last caption word deleted | 5/30 | **0/21** | **fixed** — replaced by a metadata dump, which is worse |
| caption's last line sliced by the video | 3/30 | **0/21** | **fixed** |
| source headline top-sliced | ≥6/30 (20%) | **12/21 (57%)** | **SURVIVES**, and proven ours by source-vs-output |
| dead canvas (median 39.2%) | 12/30 ≥45% | median **34.7%**, 11/21 ≥30% | **SURVIVES**, slightly better |
| duration over 30s | 20/30 (67%) | **15/21 (71%)** | **SURVIVES** |
| non-Latin captions as boxes | 2/30 | **1/21** | **SURVIVES** |
| **postable** | **3/30** | **0/21** | **worse** |

---

## 6. THE INSTRUMENTS, VALIDATED AGAINST THE EYE

The brief named three detectors that have been wrong here. Mine were checked against the
hand labels before any count was used, and **one of the three failed**:

| instrument | vs 21 hand labels | used? |
|---|---|---|
| `blank ≥ 0.30` as dead canvas | **TP 11, FP 0, FN 0, TN 10** | yes — every count above |
| `picture` row fraction | **WRONG** — reports 0.82 on a frame that is half black letterbox, because a black row is neither near-white nor uniform | **no count uses it** |
| `motion < 1.0` as a still detector | 1 of 1, no false positives | yes, for the single still |

The `picture` failure is the same family as the three the brief listed: **a two-class
"blank or picture" split has nowhere to put a black bar**, exactly as it has nowhere to put a
caption glyph. Three classes were not enough either; four would be needed. It was caught by
reading a frame that the number disagreed with.

---

## PROOF

| Required | Result |
|---|---|
| 20 renders through the real pipeline | **21** (one smoke render kept), no `explicit_song`, real library, real ranker, **pinned to HEAD** |
| verified four ways | **21/21** on all four; applied window; lag bounded to one hook period |
| every one watched | 21 contact sheets read, plus a source-vs-output comparison |
| a postable count with failures ranked | **0 of 21**; eight problems ranked by videos blocked |
| compared against MEMEBOT-074 | 4 fixed, 4 survive, postable 3/30 → **0/21** |
| suites | **ALL GREEN — 149/149, 5,036 checks** (400s, 4 rounds in flight) |
| spend | **$0.0084** of $0.30 |

---

## Method / limits

**This judges HEAD, not the working tree.** Three rounds have ~1,500 uncommitted lines in the
render stack right now; some of what I list may already be fixed in their buffers. What I can
say is what a clone gets today.

**The postable bar is mine and it is a judgement, not a measurement.** I applied: would a
page with 100k followers put this out unedited? Caption that reads as machine output, a
competitor's logo, a foreign language, or half a white screen all fail it. Someone applying a
looser bar would get 1 or 2, not 10.

**I verified the sliced headline on ONE video, not twelve.** The source-vs-output comparison
is decisive for `3944866942203277339`; the other eleven are labelled from the output alone
and share the visual signature. If the cause differs for any of them, that count is soft.

**Duration is the cheapest fix and nobody owns it.** 15 of 21 run 2–6× the repost norm
because nothing trims the top end — `MAX_DURATION_S` is 90 and `fit_window` stretches the
audio to whatever the clip is. A hard output cap would move more videos toward postable than
any other single change on this list.
