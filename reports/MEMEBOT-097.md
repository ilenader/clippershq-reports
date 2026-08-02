# MEMEBOT-097 — Cyrillic already worked, Inter fixes three more free, and five need a decision

**Brief:** fix non-Latin captions or gate them with a named reason; re-verify the twelve
sliced headlines at current HEAD; verify the caption classifier on 10 forced captions;
confirm `test_render_argv` green; verify the pad guard both directions; read frames.

**Scope was cut at the gate, and the reason is on the record.**
`memebot/scraper/edit.py` was claimed by **MEMEBOT-094 roughly 40 seconds before I reached
for it**. I did not take it. Item 1's fix ships as a measured, ready-to-apply patch
(`scratch/mb097_fontfix.patch`) instead of a contended edit.

**Item 2 was not done.** Not blocked — not reached. Said plainly rather than estimated.

**$0.00 spent. No paid calls, no renders purchased.**

---

## Preconditions, and what they caught

```
git -C memebot status --porcelain
     M scraper/edit.py          M scraper/duck.py          M scraper/tests/test_duck.py
tools/claims_read.py --holders
    memebot/scraper/edit.py            -> MEMEBOT-094  (claimed 19:19:20, ~40s before me)
    memebot/scraper/duck.py            -> FREE   ... but ' M'
    memebot/scraper/tests/test_duck.py -> FREE   ... but ' M'
```

**Two separate hazards, and they are not the same hazard.**

1. **`edit.py` is under a live claim.** MEMEBOT-094 took it seconds ahead of me. Contending
   would have been the cross-round collision this repo keeps paying for.
2. **`duck.py` and `test_duck.py` are ` M` with NO live claim** — orphaned uncommitted
   work. Reading it: MEMEBOT-066's `AudioClassRequired`, which replaces a `keep` guess with
   an exception when a bed is laid and nothing declared what to do with the source audio.
   **198/198 memebot tests pass against it**, so it is coherent, finished, and uncommitted.

I did **not** rescue it. `edit.py` holds the other half of the same orphan (a
`_floor_trim_budget` follow-on to MEMEBOT-086's duration ceiling) and now sits under
MEMEBOT-094 — committing duck.py alone would split one round's work across two commits and
two owners, which is worse than leaving it whole for whoever takes it. **Recorded so it
does not degrade further:** an orphan of exactly this shape became a live HEAD break within
an hour earlier this session.

---

## 1. Non-Latin captions — measured, and the brief's premise is a third wrong

Two independent tests, run against both fonts in `memebot/scraper/fonts/`:

- **cmap coverage** (`fontTools`) — what the font *file claims* it can draw.
- **rendered pixels** — draw two **different strings of the same length** in one font. Real
  glyphs give different pixels; `.notdef` boxes give **identical** pixels, because every box
  is the same box. No threshold, no tuning.

| script | **Montserrat-Bold** (shipped default) | **Inter-Bold** (also already shipped) |
|---|---|---|
| Latin | renders | renders |
| **Cyrillic** | **renders** | renders |
| Greek | boxes | **renders** |
| Arabic | boxes | **renders** |
| Hebrew | boxes | **renders** |
| CJK · Kana · Hangul · Thai · Devanagari | boxes | boxes |

**The brief says "Cyrillic/Arabic/CJK render as □□□□". Cyrillic already renders in the
shipped default** — a third of the stated problem does not exist. Arabic and CJK do.

### The fix is two parts and only one needs a decision

- **Greek, Arabic, Hebrew: free.** `Inter-Bold.ttf` is *already in the repo* and already
  carries them. Selecting it when the caption contains those scripts costs nothing — no
  download, no size.
- **CJK, Kana, Hangul, Thai, Devanagari: absent from both shipped fonts.** No selection
  logic can fix that. A CJK face is several megabytes — a repository decision, not a
  rendering one. Until it is taken these must be **gated with a named reason**
  (`unrenderable_script:U+XXXX`), because a box caption is worse than no caption and a
  silent drop hides the cause.

`scratch/mb097_fontfix.patch` carries both parts, the range tables, the gate call site, and
the tests that should ship with it.

### The instrument trap I walked into

My first pixel test used **unequal-length** string pairs and reported Arabic and Hebrew as
*rendering* under Montserrat — contradicting the cmap. Unequal length changes the **box
count**, which changes the pixels even when every glyph is a box. Equal-length pairs removed
the artefact and the two methods then agreed on all ten scripts.

> That is MEMEBOT-089's instrument trap in a new costume: a detector that answers a slightly
> different question than the one asked, and answers it confidently. I had also written a
> first-pass "ink ratio + column variety" heuristic that called Latin-in-Montserrat *boxes*
> and CJK-in-Inter *renders* — both wrong. It was discarded, not tuned.

---

## 3. The caption classifier and `test_render_argv`

**`tests/test_render_argv` — 8 tests, OK.** It was red for MEMEBOT-089 because
`--force-caption` was uncommitted; the flag is at memebot HEAD `ba0ce2b` (4 references in
`edit.py`) and the suite is green.

**The 10 forced-caption renders were NOT run** — same reason as item 2, below.

---

## 4. The pad guard fires in both directions — verified

`test_centred_alignment_reserves_the_shift_in_BOTH_directions` sweeps `shift_y ∈
{-8, -1, 0, +1, +8}` and asserts **both** failure modes on the real filter chain:

```python
y = (canvas_h - avail_h) / 2.0 + shift
self.assertGreaterEqual(y, 0,            "shift %+d puts the picture above the frame")
self.assertLessEqual(y + avail_h, canvas_h, "shift %+d overflows: pad would re-centre")
```

Both directions are genuinely covered, and the asymmetry is documented where it matters: a
positive shift drives `y+ih` past the canvas and `pad` **re-centres** (MEMEBOT-071 measured
y jumping to 140 instead of 286); a negative shift drives `y` below zero and `pad` silently
**clamps and crops the top**. `max(0, shift)` catches only the first — centring needs `abs`.

Green, alongside the rest: **198/198 memebot tests** across 8 files.

---

## 2. The twelve sliced headlines — NOT DONE

The re-verification needs twelve source-vs-output comparisons rendered at current HEAD. I
did not run them.

**It was not blocked. I ran out of round before reaching it**, having spent the budget on
establishing the non-Latin answer properly — including discarding two bad detectors before
trusting the third. Reporting it as "still soft" would be accurate; reporting a count would
be inventing one.

What the next round needs: `scratch/mb089_verify.py` and `mb089_sheets/` are on disk and
carry MEMEBOT-089's method and its one verified case
(`3944866942203277339`). The crop fixes landed in `ba0ce2b`, so **the honest prior is that
the count has dropped and may be 0** — MEMEBOT-082 measured content-crop keeping 16px of
safety margin specifically to stop cutting into text. That prior is untested.

---

## What I got wrong

- **Two detectors before a correct one.** An ink/variety heuristic that misclassified both
  directions, then an equal-length bug that contradicted the cmap. Neither was tuned into
  agreement; both were discarded once the disagreement showed up. The cost was the budget
  that item 2 needed.
- I initially planned to rescue the orphaned memebot work, and reversed it once `edit.py`
  went under a live claim — splitting one round's change across two owners is worse than
  leaving it whole.

## What is still broken, and whose file

- **Item 2 unverified — the twelve remain soft.** Nobody's file; it is a measurement.
- **Item 3's 10 forced-caption renders unverified.** Same.
- **The font fix is written and unapplied** — `memebot/scraper/edit.py`, **MEMEBOT-094**.
- **CJK/Kana/Hangul/Thai/Devanagari have no renderable path at all.** Needs a font asset
  decision from the operator, not code.
- **`duck.py` + `test_duck.py` orphan** — MEMEBOT-066's `AudioClassRequired`, coherent and
  uncommitted. Whoever next holds `memebot/scraper/edit.py` should land all three together.

---

## Verification

```
python scratch/mb097_nonlatin.py                  # cmap + pixel coverage, both fonts
python tests/test_render_argv.py                  # 8 OK
cd memebot && python scraper/tests/test_edit_behaviour.py    # pad guard, both directions
cat scratch/mb097_fontfix.patch                   # the ready-to-apply fix
```
