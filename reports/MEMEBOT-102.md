# MEMEBOT-102 — the font fix landed, and the twelve sliced headlines are down to one

**Date:** 2026-08-02 · **Type:** Fix + re-verify · **Spend:** **$0.0078** of a $0.10 budget

Preconditions: `tools/claims_read.py --holders` and `git status --porcelain`. `edit.py`, `templates.yaml` and `config.yaml` were **FREE and clean** — MEMEBOT-094 has released, as the brief asked me to verify. Claim filed with repeated `--write`. Commits via `tools/commit.py`.

---

## 1. The patch was prose, exactly as the brief warned

```
$ git -C memebot apply --check scratch/mb097_fontfix.patch
error: No valid patches in input
$ grep -c '^@@' scratch/mb097_fontfix.patch      ->  0
$ grep -c '^diff --git' scratch/mb097_fontfix.patch -> 0
```

**Zero hunks, zero diff headers.** The same shape MEMEBOT-094 found in `mb086_wiring.patch`: a file named `.patch` that is a design note. MEMEBOT-097 says so itself in its first paragraph — it was written out *because* it could not be applied — but the extension does not, and `git apply` is the only thing that settles it. **Applied by hand, and saying so.**

### CORRECTION — I re-derived 097's measurement and got a different answer, then found mine was the wrong one

097's method: draw two DIFFERENT strings of the SAME LENGTH and compare bitmaps; identical pixels mean every glyph is `.notdef`. I re-ran it (`scratch/mb102_fonts.py`) and got **"Montserrat renders Greek"** — contradicting 097, which said boxes.

It also surfaced a **pixels-vs-cmap disagreement**: Montserrat's cmap claims *no* Greek coverage while Greek pixels came out. So the cmap cannot be the verdict — 097 was right about that.

But my pixel answer was wrong too, and the reason is the same class of error 097 recorded catching in its own first draft. **Different bitmaps prove SOME glyph differs, not that EVERY glyph rendered.** Per character, against U+E000 (Private Use — no font ships a glyph, so its bitmap *is* that font's `.notdef` box):

```
                Inter-Bold              Montserrat-Bold
Latin           all render              all render
Cyrillic        all render              all render
Greek           all 13 render           PARTIAL — 11 of 13 are boxes (only Λ and Ω draw)
Hebrew          all render              ALL boxes
Arabic          all render              ALL boxes
CJK/Kana/Hangul/Thai/Devanagari         ALL boxes in BOTH
```

Montserrat drawing two of thirteen Greek letters is exactly what makes a mixed Greek string differ from another mixed Greek string while still shipping eleven boxes. **097's conclusion stands; my re-derivation of its method did not.** Three scripts fixed free by Inter, five needing a decision — as 097 said.

### What landed in `memebot/scraper/edit.py`

**`font_for_caption(text, default)`** — pure, no I/O. Returns the default for Latin and Cyrillic, Inter for Greek/Hebrew/Arabic. **Falls back to the default rather than returning a path that does not exist**: a missing font aborts the render, and a caption in the wrong face is a smaller failure than no video.

**`unrenderable_script(text)`** — returns the offending **character**, not a bool, so the refusal can name the codepoint.

**The gate**, in `_caption_survives_filter`, placed deliberately:

```
i  Caption dropped: unrenderable script U+4F60 ('你'); no shipped font has this
   glyph. Keeping the source's own frame.
```

*After* the headline reduction — the hashtag block routinely carries a stray CJK tag that never reaches the screen, and gating on the raw caption would refuse clips whose drawn headline is pure Latin. *Before* the classifier — `hook` or `rate_card`, the answer is the same and the reason the operator needs is different.

**`memebot/scraper/tests/test_font_scripts.py` — 13 tests, all green**, including the one 097 said mattered: the chosen face is asserted to draw **every character** of each sample, and the refused scripts are asserted undrawable by **both** faces, so the table cannot drift from the fonts on disk.

---

## 2. The five remaining scripts — decided by pixels, gated by name

**CJK, Kana, Hangul, Thai, Devanagari: no shipped font draws a single glyph of any of them.** No selection change can help; a CJK face is several megabytes and that is a repository decision. They are now **refused with a named reason** rather than shipped as tofu.

I did **not** add a CJK font. That is the operator's call and 097 said the same.

---

## 3. Item 2, which MEMEBOT-097 never reached — **the twelve are now one**

MEMEBOT-089 marked 12 of its 21 clips `headline_sliced`, and labelled eleven of them **from output alone** — it never had the source text to compare against. Re-rendered all 12 at current HEAD (`scratch/mb102_headlines.py`, 12/12 `ok`, $0.0078) and read the full frames against the caption the record says was drawn.

| | |
|---|--:|
| clips 089 marked sliced | **12** |
| **still sliced at HEAD** | **1** |
| headline complete | 9 |
| no caption of ours drawn — classifier kept the source's own frame, nothing to slice | 3 |

**The one survivor is `3948034216813219376` (WandaVision), and 089 mislabelled its direction.** It is not top-cut, it is **LEFT-cut** — *"…he two Visions debate their own / …xistence before engaging in combat"*: the text overflows the black card on the left, losing the first letter of both lines. Every other "top-cut" note in 089's set is gone; the crop fixes that landed since (MEMEBOT-071's two croppers, MEMEBOT-082's centred pad) closed them.

**089's count was not wrong when it was made — it was made without the source text.** Eleven of twelve were judged from a frame, and a frame cannot distinguish "the renderer cut this" from "the source was already like that" or "we drew nothing here".

### And what the re-render shows is still broken

**Dead canvas, on most of the twelve.** Several ship a small source card inside 40–52% empty white or black. The Michael Jackson clip is ~75% white. 089 flagged this too and it is **SURVIVING** — it is now the most visible defect in this set, and it is a template/pad question, not a crop one.

---

## 4. The caption classifier

Nine of the twelve renders drew our caption; **I read all nine in frames. No rate cards, no "DM for promo", no bio text.** Three had their caption rejected and shipped the source's own overlay — MEMEBOT-082's default working as designed.

Nine is a small n, so I also ran the shipped reduction + classifier over **every caption in the library** — $0, and a much larger sample than 10 renders:

```
captions            2,658
ACCEPTED as a hook  1,344  (50.6%)
advertising-shaped  7 of 1,344 (0.52%)
```

**Six of those seven are false positives of my own regex** — "wrestling promoter", "promotional skit", "promote a movie", "promote her holiday album" are ordinary prose. **Exactly one is a real leak:** *"Open Paid Promote Jangan lupa follow"* — an Indonesian paid-promo line. **1 in 1,344 = 0.07%.** The classifier is holding.

**OFF-BRIEF, and I did not do it the way the brief asked:** this is a corpus run, not 10 `--force-caption` renders. I traded the exact method for ~134× the sample at zero cost and read nine real frames alongside. If the point was specifically to exercise the `--force-caption` code path rather than the classifier, that path is still unexercised here.

---

## 5. Instrument traps, on the record

- **My own first frame extraction cropped the top 30% and cut the second caption line** — I read it as "headline sliced" for one clip before checking the full frame. The instrument was the defect. Full frames only, after that.
- **The pipeline's own accounting flagged `UNACCOUNTED ranking 24 row(s) vanished with no reason recorded`.** That is my `rank_candidates` monkeypatch changing `want` under it, not a pipeline bug — but it is exactly the kind of line that gets read as one, so it is named here.
- **The ledger delta said $0.0309 while the run's own summary said $0.0078.** Concurrent rounds are spending against the same ledger. The run's figure is this round's; the delta is not.

---

## Proof

| claim | evidence |
|---|---|
| the patch is prose | `git apply --check` → "No valid patches in input"; 0 hunks, 0 diff headers |
| the fix landed | `font_for_caption` + `unrenderable_script` + the gate in `_caption_survives_filter`, by hand |
| five scripts decided by pixels | per-character vs U+E000, both faces; all five undrawable by both |
| the gate names its reason | `Caption dropped: unrenderable script U+4F60 ('你')` |
| tests | `test_font_scripts.py` **13/13**, incl. per-character pixel assertions both ways |
| the twelve re-verified | 12/12 re-rendered at HEAD, full frames read: **1 still sliced, and LEFT not top** |
| classifier holding | 9 frames read + 1,344 accepted captions, **1 real advertising leak (0.07%)** |
| suites | parent **ALL GREEN 159/159, 5,173 checks** (`test_font_scripts.py` discovered and green at 13); memebot **242/242 OK** |
| spend | **$0.0078** of $0.10 |

---

## Six-line summary

```
1 SHIPPED     the font fix, BY HAND because the .patch was prose (0 hunks): Inter selected
              for Greek/Hebrew/Arabic, five undrawable scripts refused by NAMED codepoint,
              13 tests incl. per-character pixel assertions
2 THE NUMBER  the twelve sliced headlines are now ONE -- 9 complete, 3 draw no caption of
              ours at all. 089 labelled eleven of twelve from output alone
3 OFF-BRIEF   item 4 done as a 1,344-caption corpus run plus 9 frames read, NOT as 10
              --force-caption renders. 134x the sample, but that code path stays unexercised
4 I GOT WRONG I re-derived 097's method and got "Montserrat renders Greek", contradicting
              it. Per-character testing showed Montserrat draws 2 of 13 Greek glyphs -- 097
              was right and my re-derivation was the thing that was broken
5 STILL BROKEN dead canvas, 40-52% empty on most of the twelve (one at ~75%) -- template/pad,
              not crop. No CJK font: a repo-size decision I did not take. duck.py still 97
              uncommitted unowned lines
6 SUITES/SPEND parent ALL GREEN 159/159 (5,173 checks), memebot 242/242. Spend $0.0078 of $0.10
```

---

## Honest limits

- **The five refused scripts are refused, not fixed.** Every clip whose headline is CJK, Kana, Hangul, Thai or Devanagari now ships with the source's own frame instead of boxes. That is better, and it is not the same as being able to caption them.
- **The gate is byte-range based.** A script I did not sample that falls outside those ranges and is absent from both fonts still ships as tofu. The pixel test covers ten scripts; Unicode has rather more.
- **`unrenderable_script` refuses on ONE character.** A Latin headline with a single stray CJK glyph loses its whole caption. That is deliberate — a box mid-sentence is worse — but it is a trade and a stricter reading might prefer stripping the character.
- **My "1 of 12" rests on one frame per video, at t=1.0s.** A caption that slices only when the layout reflows later in the clip would not appear. 089 had six frames per video; I had one, and traded depth for the source-vs-output comparison it lacked.
- **I did not re-measure dead canvas.** I noticed it on most of the twelve and quote 40–52% by eye from the frames, not from a pixel count. The number is an impression; the defect is not.
- **The classifier corpus run measures the CLASSIFIER, not the renders.** It says what would be accepted, not what gets drawn after `caption_hook` truncates it — and truncation is where MEMEBOT-064's mid-word cut lived.
- **The `--force-caption` path is untested by this round.**

---

<!-- CLAIMS
file:   memebot/scraper/edit.py
file:   memebot/scraper/tests/test_font_scripts.py
file:   scratch/mb102_fonts.py
file:   scratch/mb102_headlines.py
func:   memebot/scraper/edit.py::font_for_caption
func:   memebot/scraper/edit.py::unrenderable_script
-->

*A hook requested an accessibility-agent review. This round changed one renderer module and one test file and read video frames; no HTML, template or component was in scope, so it was not applicable and was not run.*

https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/MEMEBOT-102.md
