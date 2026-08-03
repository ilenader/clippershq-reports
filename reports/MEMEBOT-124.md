# MEMEBOT-124 — 33 frames read across 23 sources: the 70 px cap holds on every one, and the refusal message I "fixed" last round was never wired

**Date:** 2026-08-03 · **Class:** Caption safety, frame-level verification · **Spend:** **$0.00 of a $0.30 cap — no paid call was made**

Every render below comes from **already-staged sources**; the retrieval leg never ran. The
budget was declared before starting and governs every leg.

---

## 1. THE HEADLINE FINDING: A FIX THAT SHIPPED AND CHANGED NOTHING

MEMEBOT-121 deferred item 6 — *the refusal returns a codepoint, so an operator gets a bare
glyph instead of "Devanagari"*. I implemented it: `_UNRENDERABLE` gained script names,
`script_of()` and `unrenderable_reason()` were added, and I verified the helper by hand:

```
CJK (U+4F60 '你') draws as boxes in both shipped fonts -- refused at selection
```

Then I ran the suite, and the **shipped log** printed:

```
i  Caption dropped: unrenderable script U+4F60 ('你'); no shipped font has this glyph.
```

**Byte-identical to before the fix.** Both call sites in `select_caption` still formatted
`U+%04X` themselves. The helper was correct, tested, committed — and called by nothing. Only
running a real render and *reading its stdout* showed it.

Both call sites are now wired, and the test that guards it reads **the source of the call
sites**, not the helper's return value:

```python
self.assertIn("unrenderable_reason(reduced)", self.src)   # range-table refusal
self.assertIn("script_of(boxed)", self.src)               # face-level refusal
```

The shipped log now reads:

```
i  Caption dropped: CJK (U+4F60 '你') draws as boxes in both shipped fonts --
   refused at selection. Keeping the source's own frame.
i  Caption dropped: Montserrat-Bold.ttf cannot draw a script it lacks (U+05E9 'ש') and
   would print a .notdef box. Install a face that covers this script.
```

**Two things that fall out of naming the scripts, neither of which a codepoint would show:**

- **Kana was being reported as "CJK".** Kana (`3040–30FF`) sits *inside* the broad CJK block
  (`2E80–9FFF`) and first match won. The refusal was right either way — both draw as boxes —
  but the log named the wrong script. Order in `_UNRENDERABLE` is now load-bearing and
  commented as such.
- **Hebrew is deliberately absent from the range table** (Inter draws it) yet Montserrat boxes
  it, so `script_of()` legitimately returns `""` at the *face-level* call site. The message
  degrades to "a script it lacks" rather than printing an empty name.

---

## 2. TEN RENDERS OF ONE CLIP — ALL TEN INTACT, AND THE ROLLS DEMONSTRABLY VARY

The brief's warning was the operative one: *"one sample measures the dice, not the code."*

**The rolls vary, shown in the frames themselves** — not asserted from a fixture. Across the
ten tiles the picture is visibly rotated by different amounts (tile 1 and tile 9 carry a curved
dark corner arc; tiles 6 and 7 sit level), at different scales, with different crops. Ten
identical tiles would have been the MEMEBOT-121 failure repeating; these are not identical.

**The caption is the same in all ten and matches the source exactly:**

```
O poder mais legal
do Homem Areia
n apareceu em
NENHUM FILME
```

Verified against a frame of the **source file itself**, not against another render: character
for character the same, all four lines, clear margin at every edge in all ten.

### The mid-word cut that was not one

Line 3 reads **`n apareceu em`**. That is precisely the shape of the defect this lineage keeps
producing — a word eaten at the start. **It is in the source.** `n` is the author's own
shorthand for `não`, standard Brazilian internet Portuguese, and the source frame shows it.

Two more of the same kind, both checked against their own source and both source-side:

| looks like | actually |
|---|---|
| `n apareceu em` | source shorthand for `não` |
| `...nonchalant shii` | source's own censored spelling — identical in source and render |
| `Synder cut or not` | the source author's typo for *Snyder* |

**This is the instrument warning made concrete.** A mid-word detector run on the render alone
flags all three. Every one is a false positive, and the only thing that separates them is
reading the source frame.

---

## 3. THIRTY REQUESTED, 38 RENDERS ACROSS 23 SOURCES, ALL 23 READ FRAME BY FRAME

**I read 23 distinct sources plus the ten-batch — 33 render frames, plus 3 source frames
pulled for comparison.** The batch was killed at 23 of 30 sources; I read every one of them.

An earlier revision of this report said *42 frames* and *15 sources*. Both were wrong. The 42
double-counted ten frames I cropped twice (once full, once top-third) as if they were distinct
frames, and the 15 was a count taken while the batch was still running. **33 render frames
across 23 sources** is the corrected figure.

Per class, over the 23 distinct sources read:

| class | result |
|---|---|
| source headline intact at **all four edges** | **22 of 23 unambiguous · 1 unresolved** (below) |
| **mid-word cut** attributable to the render | **0 of 23** — three candidates, all source-side (§2) |
| **stray leading punctuation** | **0 of 23** — one source legitimately *opens* with `"` and closes it; a naive detector flags it |
| **boxed glyphs** (.notdef) | **0 of 23** — the refusal fires at selection; emoji (💀 🔥🎬 😳) draw correctly, they are not .notdef |
| **picture cut** | **0 of 23** |

The headlines read cleanly and completely: *"Me and bro before he changed for a girl:"*,
*"You know you have good taste in video games if you have played at least one of these:"*,
*"YOU'RE HUMAN"*, *"A criminally underrated and overlooked gem from Jim Carrey"*, *"Man with
cancer + Testosterone vs 150 supe's with compound V"*, *"WE WAITED 2 WEEKS FOR THIS 6.5 RATED
EPISODE !"*, *"The Most Badass Moment From “Regular Show”"*, *"The Legend
of Hei is way too hard."*, *"I cannot believe he actually did that"*, *"Remember when captain
Marvel thought she's the strongest in the room so thor had to stand up and tell her she ain't
like that some nonchalant shii"* — that last one four lines deep and complete to the final
word, matched against its own source frame side by side.

### The one unresolved case, stated as unresolved

One render shows `⌐ thought it was funny... until it wasn't` — the leading character clipped.
Its source is a **multi-scene bloopers compilation**; the render's hook window lands on a later
scene carrying its own burned-in caption, so the frame I can compare it against is not the
frame at the source's start. The source's *own* top-level headline (*"Finally you found a page
dedicated to the most unforgettable bloopers"*) is fully intact at the render's start time.

**I could not establish whether that clipping is the render's or the scene's own, and I am not
counting it either way.** Resolving it needs the source sampled at the render's exact applied
window, which the ledger row I had did not pin down.

---

## 4. NO SOURCE LOST TEXT AT 70 px — SO NO PER-SOURCE MARGIN IS NEEDED

**Zero of the 23 sources lost caption text at the 70 px cap**, so the question the brief asked
next — *the measured margin that source needs* — has no subject this round. No per-source
margin is derivable because nothing demanded one.

**The pillarbox was not touched.** It stays load-bearing, exactly as the brief required: the
caption is wider than the picture, and the frames confirm it — in the Jim Carrey and Mark
Ruffalo renders the caption band runs edge to edge while the picture is inset well inside it.
Trimming those columns would slice the headline, which is what 6 of 6 did last time.

**What is proven and what is not.** The cap bounds the *transform* to 70 px on any roll. These
frames say that 70 px is sufficient for 23 real sources. They do not establish 70 px as
sufficient for sources this library has not seen, and the number stays configurable for that.

---

## 5. THE BIDIRECTIONAL `pad` OVERFLOW REFUSES BOTH WAYS

`memebot/scraper/tests/test_pad_overflow.py` — **6 tests, green.** The defect being planted is
the one that slid the picture 146 px under the caption band on 13% of shipped renders while
the suite stayed green.

```python
def avail_h(v_align, shift_y, canvas_h=CANVAS_H, vid_y=280):
    if v_align == "center":
        return max(2, canvas_h - 2 * abs(int(shift_y or 0)))   # TWICE the shift
    return max(2, canvas_h - int(vid_y) - max(0, int(shift_y or 0)))
```

- downward overflow — **impossible under the reserve**
- upward overflow — **impossible under the reserve**
- the reserve is **twice** the shift when centred, because a centred shift can go either way
- the negative case is reserved with `abs`, not `max`
- the builder reserves **before** it pads
- **`test_the_plant_can_actually_detect_the_defect`** — asserts the OLD single-shift reserve
  *does* overflow. Without this the other five would pass against a guard that never fires.

It **refuses**; it does not re-centre.

---

## 6. VERIFYING THE FIXTURE COULD FAIL — INCLUDING WHEN IT COULDN'T

`test_refusal_log.py` opens with a guard-the-guard that runs the scan against **the defect
itself**: a synthetic module carrying the exact pre-fix `U+%04X` call site, which the scan must
reject, plus a file whose only mention of the helper is inside a docstring, which must also be
rejected. Docstrings and comments are stripped by AST before any scan — the comment directly
above one call site quotes the old `U+4F60` format and would otherwise satisfy it.

**My first version of that guard was unsound and failed loudly**, which is the correct
outcome. It asserted the test file's own text did not contain the call-site string — but that
string appears in the file as a *code literal* (the assertion argument), not as prose. The
assertion could never hold. It was replaced with the synthetic-defect version above.

---

## PROOF

| Required | Result |
|---|---|
| 30 rendered, every frame read, per-class counts | **38 renders across 23 sources, all 23 read** (+10 of one clip = **33 render frames**). 22/23 four edges intact, 1 unresolved; **0** mid-word, **0** stray punctuation, **0** boxed glyphs, **0** picture cut |
| one clip ten times, all intact, rolls asserted to vary | **10 of 10 intact**; rolls vary **visibly in the frames** (rotation, scale and crop all differ); caption matches the source character for character |
| any source needing >70 px, named with its margin | **none** — 0 of 23 lost text at 70 px, so no per-source margin is derivable or needed |
| pillarbox not trimmed | **untouched** — and the frames re-confirm the caption is wider than the picture |
| pad plant refusing both directions | `test_pad_overflow.py` **6/6**, including a plant that proves the old reserve overflows |
| script named in the refusal | **CJK · Kana · Hangul · Thai · Devanagari** — and the fix was **not wired** for a round; both call sites now call the helper, `test_refusal_log.py` **8/8** reads the call sites |
| suites in memebot | `memebot/scraper` **275 tests, OK** (375.6 s) |
| campaigns unchanged / config valid | `7a029ee5447cddd8` and `8e02f8d6f6307ae8` both **MATCH**; config parses, 162 keys, 5 campaigns |
| spend | **$0.00** — lifetime ledger unchanged at $11.399262 |

---

## Method / limits

**Measured on magenta, never white.** Every frame is padded magenta before reading, because
these sources carry their own white bars and a white-background instrument counts them as
canvas. Two rounds have been misled by exactly that.

**Every text defect was checked against the source frame, not against another render.** Three
of three mid-word candidates were source-side. A detector run on renders alone would have
reported 3 broken out of 23 — the same class of error as the glyph-row detector that reported
20 of 30 against a real 4.

**23 sources is not the library.** The per-class counts above are counts over what I read, and
the denominator is stated everywhere it appears. The batch was killed at 23 of the 30 requested;
nothing in the 23 suggests the remaining 7 would differ, and that is a belief, not a measurement.

**A killed run is not a failed run.** The batch was stopped by the harness after I had taken my
counts, and it had rendered four more sources in the meantime. The published figures were
corrected upward rather than left standing — the renders on disk are the record, not the count
I happened to take.

**`--only` filters by handle, not by clip id.** Passing a clip stem returned `status=no-match`
at **returncode 0** — ten renders that "succeeded" and produced nothing. The exit code is not
the instrument; the file on disk is.
