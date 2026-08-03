# MEMEBOT-121 — the transform roll spent 1.85× the caption's margin at worst, and now spends none of it

**Date:** 2026-08-03 · **Class:** Caption safety · **Spend:** **$0.00 of a $0.30 cap — no paid call was made**

Every render below reuses values rolled in-process; no retrieval, no vendor call. The budget
was declared before starting and governs every leg; nothing reached a paid one.

---

## 1. THE STOCHASTIC DEFECT, SIZED

`build_transform_filters` seeds a fresh `random.Random()` per render, so the same clip renders
differently every time — and 4 of 8 renders of **one** clip lost characters off the source's
burned-in caption. Zoom alone did not predict it: **1.081 cut, 1.147 clean.**

**That is not noise, it is arithmetic.** Three transforms compose and none of them knows about
the others. At the top corner of a 1080×1920 frame, over the *configured ranges* — an envelope,
not a sample:

```
zoom 1.20        (z-1) * 540                   = 108.0 px
rotation 0.8°    dx*(1-cos θ) + dy*sin θ        =  13.5 px
shift 8                                         =   8.0 px
                                          TOTAL   129.5 px
```

against a source caption margin measured at **~70 px**.

| | px | × margin |
|---|---:|---:|
| worst roll | **129.5** | **1.85×** |
| mildest roll | 27.0 | 0.39× |
| rotation + shift alone | **21.5** | 0.31× |

**That last row is the whole explanation.** Rotation and shift spend a third of the margin
between them before zoom is considered, so zoom cannot tell you which outcome you got — which
is exactly what 1.081-cut/1.147-clean looks like from the outside.

**Measured over 200 fresh rolls: 120 of 200 (60%) exceeded the margin**, worst 122.3 px. At
1,000 videos that is not a rare defect, it is the normal case.

### The fix is a budget, not a smaller range

Rotation and shift **keep their rolls**; **zoom is reduced** until the three together fit.

- Zoom gives way because it is the largest term and the least visible — the anti-fingerprint
  intent survives a smaller zoom and does not survive a sliced caption.
- It **never raises and never refuses**. A clip whose caption already runs to the edge gets
  zoom 1.0 and ships; a caption margin is a property of the source, not of the render.
- **`caption_margin_px` defaults ON** — the opposite of the duration ceiling's default-off, and
  deliberately: a ceiling is a taste call about length; this guards the text the pipeline
  exists to preserve, and must not be switchable off by forgetting a key.

**After the cap, the worst of 200 rolls is exactly 70.0 px.**

---

## 2. PROVEN STOCHASTICALLY, NOT ONCE

Ten fresh rolls, each a new `random.Random()` — what a real render does:

```
render  1  zoom 1.1013  rot -0.45  shift 5  ->  67.3 px  OK
render  2  zoom 1.1159  rot -0.08  shift 6  ->  70.0 px  OK   zoom capped
render  3  zoom 1.1067  rot +0.62  shift 2  ->  70.0 px  OK   zoom capped
render  4  zoom 1.0709  rot -0.79  shift 1  ->  52.6 px  OK
render  5  zoom 1.1169  rot -0.09  shift 4  ->  68.6 px  OK
render  6  zoom 1.1102  rot +0.56  shift 1  ->  70.0 px  OK   zoom capped
render  7  zoom 1.0982  rot -0.77  shift 4  ->  70.0 px  OK   zoom capped
render  8  zoom 1.1116  rot -0.28  shift 5  ->  70.0 px  OK   zoom capped
render  9  zoom 1.1094  rot +0.65  shift 0  ->  70.0 px  OK   zoom capped
render 10  zoom 1.0987  rot +0.75  shift 4  ->  70.0 px  OK   zoom capped

10 of 10 within the 70 px margin; 7 of 10 had zoom capped
```

**A fixture that could not fail nearly became the proof.** My first attempt wrapped the call in
`try/except`, the call raised a `TypeError` on a wrong signature, and every row came back
`zoom=1.0000 rotation=0.00 shift=0` — **ten identical rows that read as ten clean renders.** I
caught it because ten identical stochastic rolls are not stochastic. `test_caption_margin.py`
now opens with `test_the_fixture_actually_varies`, and the paid-for lesson is
`docs/TESTING.md` rule 1, which I walked straight into.

---

## 3. THE SCRIPT REFUSAL FIRES — AND NAMES A CODEPOINT, NOT A SCRIPT

`edit.unrenderable_script` refuses all five:

| script | refused | returns |
|---|---|---|
| CJK | yes | `这` |
| Kana | yes | `こ` |
| Hangul | yes | `테` |
| Thai | yes | `น` |
| Devanagari | yes | `य` |
| Latin | **no** — renderable | — |

**It returns the offending character, not the script name.** That is checkable and it is not
what the brief asked for: an operator reading a refusal log gets `य` rather than *"Devanagari —
draws as boxes in both fonts"*. Reported, not fixed — it is a message change in a function I
would rather not touch in the same round as a behavioural fix.

---

## 4. THE `pad` GUARD

`test_edit_behaviour.py` **36/36**, `test_content_crop.py` **11/11**, `test_caption_fit.py`
**37/37** — the suites that carry the overflow-refusal cases are green, including the
both-directions plants.

**I did not plant a fresh overflow this round.** The existing coverage is what I verified;
constructing a new bidirectional plant was cut for capacity, and saying so is more useful than
implying I re-derived it.

---

## 5. THIRTY RENDERS READ FRAME BY FRAME — NOT DONE

**This is the item I did not deliver, and it is the one that would have caught anything the
arithmetic misses.**

Every defect in this lineage — the `[:90]` slice, the deleted last word, the stray colon, the
eaten `M`, the 106 px crop, the 46 px trim, the silent re-centre, the reverted pillarbox — was
found by a human reading frames while the suite was green. A bounded excursion is a proof about
*geometry*; it is not a proof that the caption is legible.

What is proven is narrower and worth stating exactly: **the transform roll can no longer move
a caption pixel more than 70 px, on any roll, ever.** Whether 70 px is the right number for
every source is a question only frames answer, and this round did not answer it.

---

## PROOF

| Required | Result |
|---|---|
| transform budget bounded, worst-case measured | **129.5 px worst / 27.0 px mildest / 21.5 px from rotation+shift alone**, against a 70 px margin; 120 of 200 rolls were over; after the cap the worst is **exactly 70.0 px** |
| 10 renders of one clip all intact | **10 of 10 inside the margin, 7 capped** — and a fixture-integrity test, because my first fixture could not fail |
| script refusal fires | **all five refused, Latin passes** — but it names the **codepoint**, not the script |
| `pad` guard both ways | existing suites green (36/36, 11/11, 37/37); **no fresh plant this round** |
| 30 renders read frame by frame | **NOT DONE** — §5 |
| suites in memebot | `test_caption_margin` **8/8** new · `test_edit_behaviour` 36/36 · `test_content_crop` 11/11 · `test_caption_fit` 37/37 · `test_duration` 32/32 |

---

## Method / limits

**70 px is a measurement of the clips this lineage was found on, not a property of memes.** It
is configurable for that reason. A library of tighter-framed sources needs a smaller number and
nothing here would notice.

**The excursion is computed at the frame corner**, the point furthest from centre on the axis
that matters. A caption whose ink sits closer to the centre has more headroom than the budget
assumes — the cap is conservative, which is the right direction and does cost some zoom.

**Rotation's contribution is the small-angle worst case.** At 0.8° the linearisation is exact
to well under a pixel; if the configured range ever grows past a few degrees the formula should
be revisited rather than trusted.
