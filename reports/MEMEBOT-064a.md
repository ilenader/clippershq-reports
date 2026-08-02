# MEMEBOT-064a: a caption ends where a sentence ends, not where the characters run out

**Date:** 2026-08-02 · **Type:** Diagnose + fix · **Spend:** **$0.00** (no paid calls) · `memebot/scraper/edit.py` + its tests are the only files changed

*Published as MEMEBOT-064a: my round id is MEMEBOT-064 and I hold the claim, but `reports/MEMEBOT-064.md` was already taken on origin by the duration-floor round before this was ready. MEMEBOT-066 and MEMEBOT-067 are free on origin but claimed by live rounds, so taking either would collide later. Suffixing is the rule after MEMEBOT-057 overwrote a live report.*

---

## SUMMARY

- **Shipped:** sentence-aware caption trimming in `memebot/scraper/edit.py` — `caption_hook()`, `strip_leading_punctuation()`, a boundary-preferring `_ellipsize_to_box()`, and a `MAX_CAPTION_LEN` gate that trims instead of rejecting. 14 new tests.
- **The one number:** **10 real renders, 30 frames, 0 mid-word cuts, 0 stray leading punctuation** — read off the frames, against 25/25 broken in BL-950.
- **Off-brief:** the stray colon is **not** a cut "Title:" prefix as the brief supposed — it is what `strip_emoji()` *exposes*. And the caller's `[:90]` slice, not the fitter, is the cut.
- **Got wrong:** my first verifier passed `"…the young c"` as clean; a token lookup cannot detect a severed short word. Replaced with prefix alignment.
- **Still broken:** the caption *text* is the wrong text (item 3) and we cover a better hook with a worse one (item 4). Neither is fixed here — both are proposals. `scratch/bl940_batch.py:227` (parent repo) still hard-slices.
- **Suite:** 176 tests green in `memebot/scraper/tests`. Spend $0.00.

---

## 1. The defect is not where the brief expected, and not where I expected

The brief says: *"It is NOT a wrap failure — it wraps to three lines and stops with no sentence-aware trim."* That is exactly right about the symptom and points at the wrong module.

`compute_caption_layout()` and `_ellipsize_to_box()` were **never invoked** on these captions. Reading the shipped frame for v01:

> The Macarena is a Spanish dance song by the duo Los del Río, released in the 1990s. It bec

That is **90 characters**, and 90 characters *fits* the three-line box at 56pt. The fitter had nothing to do. It never ellipsized because it never needed to.

The cut happens one repo up, before `edit.py` is ever called:

```python
# scratch/bl940_batch.py:227
caption = (str(clip.get("caption") or "clip")[:90]) or "clip"
```

A hard character slice. `[:90]` of the library caption reproduces every example in the brief exactly:

| clip | `[:90]` ends | brief reported |
|---|---|---|
| v01 | `…released in the 1990s. It bec` | `…released in the 1990s. It bec` |
| v02 | `…referred to the San` | `…accidentally referred to the San` |
| v12 | `…in his hotel room per` | `…in his hotel room per` |

**And the reason the caller slices is this module's own gate.** `edit.py` `main()` rejected any `--override-text` over `MAX_CAPTION_LEN = 120` with `return 2`. A programmatic caller cannot let a render fail, so it pre-slices to get under the limit — and a character slice cuts mid-word. The guard designed to keep captions readable is what made them unreadable.

That is the finding: **a validation that refuses instead of repairing pushes the repair to a caller that cannot do it.** The caller has no font, no box, and no sentence rule.

### The stray colon — the brief's hypothesis is wrong

The brief reads v24 (`": The Three Stooges (2012)…"`) as *"an artefact of cutting a `Title:` prefix"*. It is not. `[:90]` cuts the **end**, never the front. The real source, from the library rows:

```
'🎥🎬: The Legend of Hei II (2025)\n\nTwo years after…'
```

`strip_emoji()` removes `🎥🎬` and leaves `": The Legend of Hei II (2025)"`. The colon was always there — it belonged to an emoji that no longer exists. Nothing was cutting a `Title:` prefix; the emoji strip **exposed** punctuation that had been legitimate. This matters for the fix order: the punctuation strip has to run **after** `strip_emoji`, not before.

---

## 2. What shipped

All in `memebot/scraper/edit.py`, committed as `b5ce4f1` and pushed to the memebot remote.

**`caption_hook(text, max_chars=180)`** — the function that makes a mid-word cut impossible.

- If the text contains a sentence terminator, keep **whole sentences** up to the budget and **discard any unterminated tail**. That tail is either a severed word (`It bec`) or a sentence there is no room for. Dropping it is what repairs a caller's slice.
- If there is **no terminator anywhere** — list captions like `Minions 2015 Animation Comedy Adventure`, and also every hard slice — the final token is untrusted and dropped, with an ellipsis. Nothing in `per` says whether it is a word or the front of `perfecting`; rather than guess, we decline. That costs a genuine list caption its last word. Given 25 of 25 shipped severed, the trade is the right way round, and it is stated in the code rather than left to be discovered.
- A **shorter true fragment beats a longer cut one**, as the brief asks: when only the first sentence fits, only the first sentence ships.

**`strip_leading_punctuation()`** — removes `: ; , . ! ? – — • ·` and friends from the front, after the emoji strip. Quotes and brackets are deliberately **not** stripped: `"POV: …"` and `(2025)` open a caption legitimately, and a test locks that in.

**`_ellipsize_to_box()`** now prefers a sentence boundary inside what fits, and drops the ellipsis when it lands on one — a complete sentence abbreviates nothing. Guarded at 40% of the fitting text so a stray `Wow.` cannot throw away three good lines. This is the backstop for text that overruns the *box* rather than the character budget.

**`main()` trims instead of rejecting.** Over `MAX_CAPTION_LEN`, the caption is passed through `caption_hook` and a warning is printed. A caller can now hand over the whole caption, which removes the incentive that produced `[:90]`.

Left alone deliberately: `run.py`'s 120-char limit on **interactively typed** captions. A human typing their own hook sees the message immediately and can shorten it; there is no silent slice there.

---

## 3. Verification — frames, because that is what caught it

The brief is emphatic, and correct: *"This bug survived a dozen rounds of green suites and was caught by a human sampling frames."* So the suite is not the evidence here.

`scratch/mb064_render.py` renders real clips from local media (no paid retrieval), extracts three frames each, crops the caption band, and stacks them. **It passes the full library caption, not a slice** — proving the new trim path end to end.

**10 renders, 30 frames.** Read directly:

| | caption as rendered | ends on |
|---|---|---|
| m01 | The Macarena is a Spanish dance song by the duo Los del Río, released in the 1990s. | sentence |
| m02 | In an Australian news segment covering the NFL… | word + ellipsis |
| m03 | I Love You Phillip Morris (2009) is one of Jim Carrey's most underrated and underappreciated films of all time. | sentence |
| m04 | Title: Two and a Half Men Created by: Chuck Lorre, Lee Aronsohn Genre: Comedy, Sitcom Runtime… | word + ellipsis |
| m05 | The Legend of Hei II (2025) Two years after the events of the first film… | word + ellipsis, **no leading colon** |
| m06 | Dragon Lord (1982) Dragon is the mischievous son of a wealthy aristocrat in old China. | sentence, **no leading colon** |
| m07 | Minions 2015 · Animation · Comedy · Adventure Context That one chaotic Minion moment that perfectly matches… | word + ellipsis |
| m09 | Wrath of the Titans (2012) is a fantasy action film and the sequel to Clash of the Titans (2010). | sentence |
| m10 | Dove Cameron and Booboo Stewart hilariously trolled their own Descendants movie by poking fun at some of its most… | word + ellipsis |
| m11 | Movie: Final Destination (2000) You can cheat death… but you can't escape it. | sentence |

**Zero mid-word cuts. Zero leading punctuation.** v01 went from `…the 1990s. It bec` to `…released in the 1990s.` and v05/v06 lost the colon.

A text-level sweep over all 14 BL-950 clips that still carry a library caption, in both modes (full caption, and the caller's `[:90]`), is **28/28 clean**.

One render failed: **m08**, `returncode=1`, xHE-AAC — `Error submitting packet to decoder: Not yet implemented in FFmpeg`. That is the known ~35.5% undecodable-source problem, unrelated to captions, and the harness rendered an 11th clip to reach ten.

### What I got wrong

My first verifier looked up the final token anywhere in the source and passed if any occurrence ended cleanly. It reported `"…of the first film, the young c"` as **clean** — a lone `c` matches inside other words. Replaced with **prefix alignment**: every step only cuts from the end, so the output must be a prefix of its input, and the character immediately after must not be a letter. That is exact, and it is the check the shipped tests use.

My first `_SENTENCE_END_RE` also stopped between the `.` and the `"` of `…us home."`, silently eating the closing quote. Caught by my own test, fixed by absorbing trailing closers into the match.

---

## 4. Item 3 — where the caption comes from, and what it should be

**Provenance:** `clip_library.build_record()` stores `put("caption", caption, DECLARED)` — `DECLARED` meaning *taken verbatim from the platform*. It is the **reposting account's own Instagram caption**, scraped from the GQL response and never touched again.

That text was never a hook. It is what a meme page types into the IG caption box, and it reliably contains, in this order: a plot synopsis or fun-fact blurb, credits, runtime, a follow-CTA, a copyright disclaimer, and a hashtag wall. Measured previously at a **median 922 characters** over 1,058 captions. `caption_headline()` already strips the hashtag block; what remains is still reference prose.

The brief's v16 — *"@Moviezar posts the best movie memes on instagram daily Spidey Sense, also known as Spider-Sense, is a special ability.."* — is the account **bio** run into a definition. My m07 shows the same shape from the other end:

> Minions 2015 · Animation · Comedy · Adventure … **Follow @zusx.editz for more meme reels like this!** … Copyright Disclaimer … #minions #despicableme #memes

**So the honest summary of item 3 is: the caption field is doing its job — it is a faithful copy of someone else's feed text. It is simply not a hook, and no amount of trimming will make it one.** MEMEBOT-064a makes the wrong text *well-formed*; it does not make it *right*.

**Proposal, in preference order:**

1. **Preserve the source's hook (see item 4) and add nothing.** Cheapest, and on this evidence the best.
2. **Write a hook from what we already know about the clip.** The library holds `vision_on_screen_text`, `vision_scene`, `franchise` and the engagement panel. A hook template built from those is $0 and grounded in the clip, not the reposter's SEO.
3. **Generate a hook.** Only worth it if 1 and 2 fail; it costs money per clip and needs its own quality gate.

What should **not** happen is shipping the reposter's caption as a headline. It is the wrong register, it names the wrong account, and on 100% of the frames I read it says less than the picture does.

---

## 5. Item 4 — the source already has a better hook, and we clip it

This is the larger finding and the frames make it plain.

Of the 10 renders, **7 sources carry their own burned-in caption**. Reading them against ours:

**m02** — ours: *"In an Australian news segment covering the NFL…"*. Theirs, in the same frame: **"this anchor knew immediately she messed up"**. Theirs is the hook. Ours is a wire-service lede.

**m03** — ours: *"…is one of Jim Carrey's most underrated and underappreciated films of all time."* Theirs: **"overlooked gem from Jim Carrey"**. Same claim, a third of the words.

And we are **damaging** theirs. In m02 the source's caption is cut at both edges by the render:

> `…the most unforgettable bloopers` / `his anchor knew immediately she` / `essed up`

`this` → `his`, `messed` → `essed`. The scale-and-pad step fits the source's *picture* to 864px without regard for text that runs to the source's full width, so the source's caption loses characters off both sides. At least **3 of the 7** are visibly clipped this way (m01, m02, m09 — `underperforming` → `derperforming`).

So the current composition manages to do three unhelpful things at once: it **covers** a good hook with a worse one, **truncates** the good one horizontally, and stacks them with no separation so they read as one garbled block.

**Recommendation: for a clip that already carries a burned-in caption, add no caption of our own.** Render the source's frame intact — that is one fewer thing to get wrong, it is free, and the meme page already did the work of writing a hook that performed. Detecting the burned-in caption is not speculative: `vision_on_screen_text` is already a library field, and the repost-finder's **layout caption-bar CV** already locates caption bars and was measured as beating OCR text-density for exactly this.

Two things must be fixed regardless of whether a caption is added:

- **The horizontal clip of the source's own text.** This is a defect on its own — it damages the source frame even when we add nothing.
- **The dead canvas.** In m03's full frame the picture occupies roughly the top half and the bottom ~45% is empty white. BL-950 flagged black pixels; on `white_frame` it is white space, and it is just as unpostable.

Neither is in scope here and neither is in a file I hold.

---

## 6. What is still broken, and whose file

| What | Where | Held by |
|---|---|---|
| `caption = str(...)[:90]` hard slice | `scratch/bl940_batch.py:227` (**parent repo**) | unheld — now harmless, since `edit.py` repairs it, but it should be deleted |
| Caption text is the reposter's feed prose, not a hook | `clippershq/clip_library.py` field + whatever chooses it | proposal only, item 3 |
| Source's burned-in caption clipped horizontally | `memebot/scraper/edit.py` scale/pad | **I hold this file** — out of scope for this round, not attempted |
| ~45% dead canvas below the picture | `memebot/scraper/templates.yaml` composition | open question flagged in the template's own comments |
| m08 undecodable audio (xHE-AAC) | source media | pre-existing, ~35.5% of clips |

**Not touched by me:** `edit.py` also carries **uncommitted work from another round** (the MEMEBOT-064 duration-floor budget and an ambient-bed message). I staged only my four caption hunks by filtering the diff, and left theirs in the working tree untouched. `MEMEBOT-066` and `MEMEBOT-067` both declared `edit.py` read-only because of my claim, and wrote `duck.py` / `run_record.py` / `test_duck.py` instead — the coordination held.

---

## Files

- `memebot/scraper/edit.py` — `caption_hook`, `strip_leading_punctuation`, `_ellipsize_to_box`, `main` (commit `b5ce4f1`, pushed)
- `memebot/scraper/tests/test_caption_fit.py` — `TestCaptionHookNeverCutsMidWord`, 14 tests
- `scratch/mb064_render.py` — render + frame-extraction harness
- `scratch/mb064_source_hook.py` — source-caption band extractor (item 4)
- `scratch/mb064_frames/` — 30 frames, `SHEET_bands.png`, `SHEET_source_hooks.png`
- `scratch/mb064_render.json`, `scratch/mb064_captions.json`
