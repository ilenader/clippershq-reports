# BL-1506 — The crop was already fixed. The guard that stops it returning was not.

**2026-09-05.** Vendor spend **$0.00** against a $1.50 cap. No socket opened, no ledger row
written, no page walked.

---

## WHICH OUTCOME HAPPENED: I ASKED, I WAS GRANTED THE FILES, AND I SHIPPED

The operator's instruction was to ask on the pipe for two held files, record the handover, and
**fall back to verify-and-publish-unfixed if nobody answered.** Nobody had to.

**Both holders answered and both granted the files**, and both are recorded here:

- **BL-1503** — *"YES to both files… my work in them is committed and I have no pending edits."*
- **BL-1505** — *"take both files. `tile_b64` in free_judge.py is not mine at all, and in
  meme_finder.py my edit is confined to `_grid_index`."*

I did not infer who held what. A claim file addresses **files, not sessions**, and inferring a
round's session from content has been wrong three times in two days here — so I asked, and a
third session routed the request.

**And then the handover turned out to matter less than the correction that came with it.**

---

## THE HEADLINE: MY OWN PREMISE WAS WRONG, AND I MEASURED IT WRONG FIRST

I was told: *a composed sheet falls to `cols=3` and is cropped, so **84.8% of every built sheet
is thrown away** before the model sees it, and the hero frame is intact in 0 of 2,302 sheets.*

**Three of the supporting facts are true. The conclusion does not follow.**

True, verified against the **committed blob**: `tile_b64` still computes `tw = w // cols`; the
selector still reads `_cols = min(_tiles, 3) if _single else 3` with `_single = 1 <= _tiles <= 2`,
so a composed sheet does fall to 3; and there is **no boundary assertion anywhere**.

**But `_cols` is then not used.** At `free_judge.py:1036`:

```
enc = tile_b64 if single_video else grid_b64
```

and at `:1113`:

```
b = enc(grid_path, cols=page_cols) if single_video else enc(grid_path)
```

A composed sheet has `single_video = False`, so `enc` **is `grid_b64` — the whole image** — and
`page_cols` is dead in that branch. `_cols = 3` is computed and harmlessly discarded.

**DRIVEN AT THE REQUEST-BUILDER, decoding the bytes actually placed in the body:**

| case | page arrives | share of source area |
|---|---|---|
| **composed sheet** (`single_video=False`) | **760×760 — the whole image** | 66.2% |
| genuine one cover (`single_video=True`, cols=3) | 311×552 | 19.7% — **a correct crop** |
| genuine one cover (`single_video=True`, cols=1) | 760×760 | 66.2% |

**The whole sheet already reaches the model on the composed path.** A peer measured the same
thing over **3,292 Instagram capture records**: whole sheet **3,177 (96.5%)**, crop path
**115 (3.5%)** — and those 3.5% are pages that genuinely are one or two covers, where cropping
is the truthful behaviour.

**And the TikTok half was already fixed** by an earlier round, where the crop was real and
severe: 155×275 on 98.2% of 1,026 sheets, now 356×760.

### I measured it wrong before I measured it right

**My first instrument called `tile_b64(path)` directly and found a crop — of course it did,
that is what the function does.** The question was never what `tile_b64` does; it was whether
the pipeline calls it. Testing a helper's return value instead of the request body is the exact
failure this project keeps paying for, and I committed it before catching it.

**A second instrument of mine also failed its own control.** My negative control — "a different
sheet must not encode to the same bytes" — reported **2 of 12 matches**. The cause was my
sample, not the encoder: it contained byte-identical duplicate files, so I had compared a file
with its own copy. After deduplicating by content it still matched **1 of 12**, because the
corpus contains re-encodings of the same picture. **Both of those zeros were discarded rather
than published.**

**A peer that had endorsed my conclusion withdrew that endorsement**, and named its own bad
instrument: `grep -c "tiles=" meme_finder.py → 0` cannot see `_g.get("tiles")`, which is how the
tile count is actually read. A literal-substring grep is not a search for whether a value is
used.

---

## WHAT I SHIPPED: THE GENERAL GUARD, NOT THE ARGUMENT

The crop is not live today — **but nothing stops it returning.** That is what shipped.

**FIX CATEGORY: GENERAL.** A boundary assertion on the **encoded bytes**, at the point they are
placed in the request:

> When no crop was requested, if the encoded width is a whole-number fraction of the source
> width, raise — the sheet was silently quartered.

**Why an assertion and not a comment:** this defect has been found **four times**, and three of
those rounds wrote it in a comment. `tile_b64`'s own docstring already tells callers to pass
`tiles=`, and no caller in the meme path ever did. **A comment cannot fail; an assertion can.**
Passing the right argument at one call site is LOCAL and gets forgotten — of seven past fixes
tested by driving them here, **only one was general and three of the six local ones were still
failing.**

### The naive form is wrong, and the measurement shows why

"the decoded width is a whole-number fraction of the source" fires on the **legitimate**
one-cover crop exactly as loudly as on the bug — a 934 px sheet cropped to 311 gives
**934/311 = 3.003 either way**:

| case | ratio | naive rule |
|---|---|---|
| composed 934 → 760 | 1.229 | passes |
| **one-cover 934 → 311 (correct)** | **3.003** | **would FIRE — wrong** |
| **quartered composed 934 → 311 (bug)** | **3.003** | should fire |

**So the discriminator cannot be the ratio. It is whether a crop was requested.** The guard is
conditioned on `single_video`: when the caller asked for one cover a fraction is correct; when
it did not, a fraction is a defect. A change that stopped `tiles=1` cropping would be a
regression, and an earlier round guards that with its own negative control — which still passes.

### Mutation-proved, 5 of 5

| case | fired | expected | |
|---|---|---|---|
| today's composed path | no | no | PASS — the funnel does not go down |
| today's legitimate one-cover crop | no | no | PASS — no regression |
| **PLANTED: a composed sheet quartered to 1/3 width** | **yes** | yes | **PASS** |
| **MUTATION: assertion disabled, same input** | **no** | no | **PASS — it is load-bearing** |
| RESTORED: same input again | yes | yes | PASS |

The planted case reports: *"the page was encoded at 311 px from a 934 px source — exactly 1/3
of it — while single_video was False, so NO crop was requested. 33.3% of the sheet would have
reached the model."*

**A green that cannot fail is worthless**, so the fourth row is the one that matters: with the
guard removed the same input goes silent.

---

## THE EXEMPLAR PATH, MEASURED SEPARATELY — and the quoted figure is wrong

The exemplars encode at **460**, the page at **760**. Measured at the boundary on both shapes:

| sheet shape | on disk | exemplar arrives | page arrives |
|---|---|---|---|
| square | 934×934 | **460×460** | **760×760** |
| tall | 465×992 | **215×460** | **356×760** |

⚠️ **The widely-quoted "215×460 while the page arrives at 760×760" mixes a TALL exemplar with a
SQUARE page.** Compared like with like, the exemplar is **61% of the page's linear scale and
37% of its area — consistently, on both shapes.** That is a real asymmetry and a smaller one
than stated. **A carefully chosen pack still arrives at roughly a third of the page's area**,
which is worth fixing, but it is not the eight-stamps picture the figure implies.

**NOT CHANGED THIS ROUND.** Changing the exemplar encode size alters what every brain is shown
and belongs with the pack work, which is another round's.

---

## THE TWO-BRAIN STRUCTURE — INDEPENDENTLY CONFIRMED, AND IT ALREADY HOLDS

The operator asked me to verify this even though I was not touching those files, because it
decides whether the merge is a file re-organisation or a change to what is sent. **It is a
re-organisation.**

**All four briefs are exact concatenations — built == live, byte-for-byte, 4 of 4:**

```
RUBRIC (the meme body)        2,126 B
  + TIKTOK_ADDENDUM           2,792 B   -> tiktok/memes     4,918 B
  + INSTAGRAM_ADDENDUM        3,623 B   -> instagram/memes  5,749 B
  + EDITS_ADDENDUM            6,628 B   -> the two edits briefs
```

**And only the page's own platform block is already sent. Zero leaks:**

| brief | own platform lines present | other-platform lines leaked |
|---|---|---|
| tiktok/memes | 35/35 | **0** |
| tiktok/edits | 35/35 | **0** |
| instagram/memes | 41/41 | **0** |
| instagram/edits | 41/41 | **0** |

⚠️ **THE CONTROL HAD TO BE BUILT ON WHOLE LINES, AND I PROVED THE WORD-LEVEL ONE CANNOT FIRE.**
The bare word "TikTok" appears in **all four** briefs, and so does "Instagram" — so a two-way
control on those words is blind by construction. Measured and reported rather than assumed.

---

## WHAT WAS REFUSED OR NOT DONE

- **Parts D and D2 — collapsing the brains and wiring his examples — are BL-1503's round**, word
  for word. It has committed and published them. **I did not take them.**
- **The `_cols`/`_single` selector was NOT changed.** It computes a value nothing reads on the
  composed path; changing it would be motion, not a fix, and it risks the genuine one-cover case.
- **The exemplar encode size was not changed** — it belongs with the pack work.
- **The aspect stretch and the tile-width guard were not touched**: `video_strip.py` is held by
  another live round whose intent covers them.
- **No judging rule was added or loosened. No threshold was re-tuned.** The reject bar is
  pooled across at least four geometries and tuning it honestly needs instrumentation this
  round does not own.

---

## WHAT I GOT WRONG

1. **I tested `tile_b64` directly instead of the pipeline**, and would have published an 84.8%
   loss that does not occur on that path.
2. **My negative control failed twice** — first on duplicate files, then on re-encodings of the
   same picture. Both zeros discarded.
3. **I nearly acted on a peer's endorsement** of my own conclusion. It withdrew it, having
   checked the line neither of us had read. Agreement between two people who read the same
   three facts is not a third fact.

---

## MONEY AND SAFETY

- **Vendor calls 0, spend $0.00**, by the run's own counter — never a ledger delta, which
  cannot attribute anything here.
- **Backups 8/8 sha256-verified, with a control proving a single flipped byte is detected.**
- **Seen stores: row KEY SETS recorded by finding the body by SHAPE, not by name** —
  2193 / 6125 / 2446 / **1902** / 1715. A name-based helper reported one of these as 3 rows in
  an earlier round; that is why the body is now found structurally.
- **No process killed.** Dashboard port re-checked immediately before every write under the
  application directory. `dashboard/.running.json` was **not consulted** — it has claimed a dead
  pid since 30 August.
- **No key, address or handle printed, logged or committed. No sample image published** — the
  handle detector has a known false negative on alpha-blended watermarks, so it cannot prove a
  sheet clean.

---

## WHAT HE SHOULD DO NEXT

1. **Nothing about the crop.** It is not live on the composed path and the guard now stops it
   returning.
2. **The exemplar size is the real remaining asymmetry** — worked examples arrive at 37% of the
   page's area. Worth a round, with the pack work.
3. **The `_cols` computation is dead code on the composed path.** Harmless today, and a trap for
   the next reader who assumes a computed value is used.

---

## PATHS

```
clippershq/free_judge.py            SilentlyQuartered + _assert_not_quartered + the call
scratch/bl1506_gate.py              parse the committed blob
scratch/bl1506_boundary.py          the four briefs, whole-line leak control
scratch/bl1506_realpath.py          drive _messages; what actually ships
scratch/bl1506_assert_proof.py      5 of 5 including the mutation
scratch/bl1506_sizes2.py            sizes with a deduplicated control
scratch/bl1506_backup.py            8/8 verified, corruption control
```

---

## THE HONEST SUMMARY

I was sent to fix a crop that was already fixed, and found that out by driving the code instead
of trusting three true facts that pointed the wrong way. What shipped is smaller than what was
asked for and, I think, worth more: **the crop cannot come back silently now, and the assertion
that stops it has been proved to fail when it should.**
