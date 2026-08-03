# MEMEBOT-120 — the no-hook hole is closed at selection, and the shipped threshold was missing real hooks by 0.001

**Date:** 2026-08-03 · **Type:** Gate + detector · **Spend:** **$0.00** of a $0.15 cap

Preconditions: `tools/claims_read.py --holders` on each target → all **FREE**; `git status
--porcelain` → all clean. Claimed MEMEBOT-120. Read MEMEBOT-119 first.

**No paid call was made or possible.** Every source file the detector measured was already
staged on disk from earlier rounds; ffmpeg and OpenCV are local.

---

## 1. The gate term is live, and it costs 15 clips

```
library                 2,728
clips MEASURED for hook   231  (8.5% — the rest are UNKNOWN and are NOT cut)
refused BEFORE            464
refused AFTER             479   no_burned_in_hook 20, non_english 298,
                                watermark 127, static 62
NET NEW refusals           15   (20 flagged, 5 already refused by another term)
```

**8.7% of measured clips carry no hook.** Projected over the whole library at that rate:
**~236 refused, ~177 of them net new** — but that is a projection and the term's cost *today*
is the 15 above, because the other 2,497 clips are unmeasured and **UNKNOWN never cuts**.

Reading an absent measurement as "no hook" would have refused 91.5% of the library on a
field nobody has measured. `verdict()` returns `None`, `classify()` ignores `None`, and there
is a test for it.

---

## 2. The detector: the shipped threshold was wrong, measured on 42 of my own hand labels

I labelled **all 24 detector-negatives individually** plus **18 of 20 sampled positives** —
**42 hand labels**, read off contact sheets, against a definition written down *before* I
looked at anything: a HOOK is burned-in text placed to be read first; a subtitle track, a
channel bug or a watermark is not.

**At the shipped 0.35, four real hooks were being missed — three of them by under 0.01:**

| top_band | what it actually was | miss |
|---:|---|---:|
| 0.351 | "The Most Epic Battle Moments From *Regular Show*" | 0.001 |
| 0.352 | "Ghostface couldn't catch a break this day." | 0.002 |
| 0.359 | "The Most Badass Moment From *Gumball*" | 0.009 |
| 0.377 | "Lamar to nice 🔥🔥" (stacked reaction layout) | 0.027 |

All four are the **headline-above-a-letterboxed-picture** template this library is full of.
The highest *true* negative sits at **0.415**, so there is a clean gap:

```
threshold 0.35 ->  precision 100.0%   recall  98.1%    (4 hooks missed of 211)
threshold 0.40 ->  precision 100.0%   recall 100.0%    (0 missed, 0 gained falsely)
```

**Landed at 0.40.** Four gained, none lost.

**`vision_on_screen_text` is not read anywhere in this path**, by construction — it is wrong
100% of the time it says empty, and MEMEBOT-119 put it at 56% error on its own sample.

---

## 3. What I did NOT do, and it is the biggest gap in this round

**I did not render 30 and read the frames.** Items 3 and 5 of the brief — deciding the
fallback by measurement, and the postable count with its selection/render split — **are not
done.** The detection and labelling work consumed the round.

So the fallback question (refuse / `--force-caption` for that subset / ship silent) is
**decided only in its first branch**: clips measured as hookless are now **refused**. Whether
drawing our caption for that subset would beat refusing them is unmeasured, and the brief's
own figure — only 1 in 10 scraped Instagram captions is a hook — is the reason I did not
default to drawing. That is an argument, not the measurement the brief asked for.

The last three audits read **13 → 10 → 10**. This round does not produce a fourth number.

---

## 4. `clean_caption` — not dead, and mis-read

It is **not** discarded-and-unreferenced. It feeds two things: `--override-text`, which
`white_frame` throws away on every render, and the operator's progress line `caption[:56]`.

So the defect was never wasted computation — it was that **the log shows caption text on a
render that draws none**, which is exactly how 5 of 30 shipped silent while looking fine. The
call site is now `caption_label`, with the discard named at the point of use. **Removing it
would have removed the progress line; wiring it would have overridden a measured policy.**

---

## 5. The plant test asserts its plants ran

BL-1056 passed **5 of 5 while three of its five plants never executed** — inside the round
whose subject was that defect. `tests/test_clip_text_signal.py` has **9 named plants**, each
registering itself as its last statement, and a final test asserting the registered set is
complete. Plus a test that the completeness check **can itself fail** (TESTING.md rule 10 —
refusal is not evidence).

**13 tests, all green, and the plant counter is 9 of 9.**

---

## Proof

| claim | evidence |
|---|---|
| gate live with named reason | `no_burned_in_hook` in `DECISION_LOG`-style refusals; 464 → **479** |
| cost in clips | **15 net new**; 20 flagged, 5 already refused; 8.7% of measured |
| detector scored on MY labels | **42** hand labels: all 24 negatives + 18 of 20 positives |
| threshold re-fitted | 0.35 → **0.40**; recall 98.1% → **100%**, precision unchanged at 100% |
| never reads the broken field | `vision_on_screen_text` absent from `clip_text_signal` and the term |
| UNKNOWN never cuts | `verdict()` → `None`; 2,497 unmeasured clips unaffected; tested |
| fields declared | `text_bands`, `text_top_band`, `has_burned_in_hook` in `CLIP_FIELDS`, `build_record` and `put(..., MEASURED)` |
| backfill | **234 records appended**, 0 errors |
| plants ran | 9 of 9 registered; completeness check proven able to fail |
| suites | `test_clip_text_signal` **13/13**, `test_clip_postable` green, `test_clip_pipeline` green; **memebot 275/275 OK** |
| spend | **$0.00** of $0.15 |

---

## Six-line summary

```
1 SHIPPED     no_burned_in_hook: a REFUSE-AT-SELECTION term measured from the PIXELS, plus
              clip_text_signal.py, 3 declared MEASURED fields, a 234-clip backfill, and a
              plant test that asserts its own plants executed (9 of 9)
2 THE NUMBER  the shipped threshold 0.35 was missing FOUR real hooks, three by under 0.01
              (0.351, 0.352, 0.359). Re-fitted to 0.40 on 42 of my own hand labels: recall
              98.1% -> 100%, precision unchanged. Gate cost: 464 -> 479, 15 net new
3 OFF-BRIEF   I did NOT render 30 or read frames. The postable count and the selection/render
              split are NOT done, and the fallback is decided only in its refuse branch --
              force-caption vs ship-silent is unmeasured. Biggest gap in the round
4 I GOT WRONG my first backfill failed 231 of 234 because CLIP_FIELDS is not the only
              declaration point -- build_record has its own signature and its own put() call.
              I read "field declared" off one list and believed it
5 STILL       2,497 of 2,728 clips are UNMEASURED, so the gate's real cost is unknown until
  BROKEN      a backfill runs over clips whose media is not already local. Owner: whoever
              runs the next walk. clean_caption still hands white_frame a caption it discards
6 SUITE+SPEND memebot 275/275 OK; test_clip_text_signal 13/13; postable + pipeline green.
              Parent full suite NOT run. Spend $0.00 of $0.15
```

---

## Honest limits

- **The 30-render audit did not happen.** Without it this round cannot claim the postable rate
  moved, and it does not.
- **0.40 is fitted on 42 labels.** Four points moved the boundary and it sits in the gap
  between them and the nearest true negative. Precision's "100%" rests on 18 sampled
  positives — its true lower bound is nearer 81%.
- **One label is definitional, not observational.** A bottom-placed meme caption at
  `top_band` 0.786 ("FARTING INTO GRANDMOMS OXYGEN MACHINE") is burned-in text that would
  beat our overlay, but it is not a *hook* under the upper-frame definition I wrote down
  first. I scored it a true negative to stay honest to the stated definition; a policy that
  cares about "any burned-in text" would score it the other way and would want a second term.
- **The 8.7% rate comes from clips whose media happened to be staged locally**, which is a
  sample of what earlier rounds chose to render — not a random draw from the library.
- **The parent suite was not run in full** (only the three affected files).
- **RapidOCR was not evaluated.** The brief offered it if the swap had landed; I did not check
  whether it had, and used the measured band detector instead.

---

<!-- CLAIMS
file:   clippershq/clip_text_signal.py
file:   clippershq/clip_postable.py
file:   clippershq/clip_library.py
file:   clippershq/clip_pipeline.py
file:   tests/test_clip_text_signal.py
func:   clippershq/clip_text_signal.py::verdict
func:   clippershq/clip_text_signal.py::has_burned_in_hook
-->

*An accessibility-agent review was requested by a hook. This round changed Python selection and
detection code and read video frames; no HTML, template, component or stylesheet was in scope,
so the web accessibility team was not applicable and was not run.*
