# BL-1537 — what the 180-day recency wall is throwing away

**Measured 2026-09-09 against production, from `checkpoint/session-2026-07-23-full-day` at
`30702a9f`. READ-ONLY on the funnel: nothing was re-judged, no verdict moved, no page latched.**
Spend cap $0.25. **Actual spend $0.0078**, counted by this run's own wrapper counter.

---

## THE HEADLINE

**The five pages BL-1536's recency wall cut are now in front of him, with a picture for three
of them and a stated reason for the other two.** All five were cut by `stale` — the 180-day
wall — **before the model was ever called**, which is why none of them had a picture: the wall
fires in triage, upstream of the picture-judge block. The pictures were built now, the same
way the delivered pages got theirs: from each account's own videos through the same
`contact_sheet_for`.

**The sheet is at `output\bl1537_sheet\` — double-click `OPEN_BL1537_SHEET.bat`.** It asks
KEEP or DROP on each of the five, and it says out loud what his own answers mean: keep two or
more and the wall is throwing away pages he wants.

**This round does not answer his question — he does.** It only makes the five visible.

---

## WHAT WAS MEASURED, WITH DENOMINATORS

**Denominator: 5 — every page BL-1536 rejected.** Not a sample; the whole rejected set from a
55-page walk.

| | |
|---|---|
| pages BL-1536 walked | 55 |
| **rejected** | **5** |
| rejected by `stale` (the 180-day wall) | **5 of 5 — 100%** |
| rejected by any other rule | **0 of 5** |
| pictures built now | **3 of 5** |
| could not be built | **2 of 5** |
| billed vendor requests | **13 = $0.0078** |

**How far past the wall each one was, in days:** 244, 393, 455, 617, 634.
**Median 455 — two and a half times the wall.** The nearest miss is **64 days over**; the
furthest is **454 days over**. Not one of the five is a borderline case.

**That matters for the question he is asking.** If the wall were the wrong length, the pages
it cuts would cluster just past it. These do not — the closest is 64 days beyond a 180-day
line. On this evidence, moving the wall to 250 days would recover **1 of 5**; moving it to
400 days would recover **2 of 5**. Whether either is worth it is what his KEEP/DROP answers
decide, and **five pages is a small denominator for that decision** — it can show him the
shape, not settle it.

**The two that could not be photographed** returned an empty own-video list — an HTTP 200
carrying no items, not a vendor refusal and not an error. For accounts last active 393 and
617 days ago that is a plausible state, but **this round did not establish why**, and the
sheet says "no picture could be built" rather than guessing. Nothing else is shown in their
place.

**The handles were recovered, not re-fetched.** BL-1536 deliberately logs a sha prefix and
never the handle. Re-hashing the 55 keys in that run's scratch seen store matched **5 of 5**
shas exactly — a verifiable join, no guessing, and the handles never entered a transcript.

---

## READ-ONLY, AND THE PROOF OF IT

`judge_page` was **never called**. No verdict was written, no seen store was touched, nothing
can latch. The only vendor call made was `videos_from_handle` — the same call the delivered
pages made — and its sole purpose was to fetch cover images so a picture could be drawn.

**The cap binds.** `reserve()`'s real source was lifted by AST and driven: a funded $0.25 cap
**allows** and the meter advances (416 requests); the ceiling **raises**; **$0.00 raises**;
and **the meter does not advance on either refusal**. `spend.json` was **byte-identical
across the whole proof**. Spend was counted by this run's own wrapper counter — `api_client.py`
contains no ledger writer at all.

**The `.bat` was tested by launching it the way a double-click launches it**, not by an HTTP
check: `Start-Process` from its own directory, then the listening-port table confirmed a
**python process listening**. The page it served is the page in the screenshots.

**Round trip proved:** clicked KEEP on card #2 → `answers.jsonl` on disk carried the answer
with `mode`/`platform`/`lane` and the question id stamped at write time → reloaded → the
header read *"answered 1 of 5 · keep 1"* and the control came back selected. **Every test
answer was then deleted, and the deletion verified after the automated tab was closed** — a
probe row once landed in his ground truth. Console: **clean, zero messages.**

**The sheet he opens is empty.** `answers.jsonl` does not exist; the first answer in it will
be his.

---

## WHAT YOU GOT WRONG

**1. The sheet appeared to write answers nobody gave — and I got the cause wrong twice before
isolating it.** Across two builds, answers were persisted with no human having touched the
page: first two KEEPs and two clears at load time, later six writes across all five rows
spread over 31 seconds. **The cause was my own browser automation interacting with the page**,
established by the only control that settles it: delete the file, **close the automation-
attached tab**, wait 90 seconds — **nothing is written**. It is not a defect in the sheet and
it will not happen when he opens it, because there is no automation attached to his browser.

**My two wrong diagnoses along the way, both acted on before being tested:**

- **"It is browser autofill."** No evidence beyond the timing; refuted by a clean reload.
- **"It is my bare-letter K/D shortcuts."** The pattern fitted — a DROP on one card and a
  KEEP on another, a second apart — so I removed the shortcut block. **The writes continued
  with zero keydown listeners on the page**, which killed that theory outright.

**What I kept anyway, and why.** Every write path now requires **`ev.isTrusted`** and the
controls carry `autocomplete="off"`. Neither was the cure, but both are correct hardening for
a page that persists to his ground truth, and neither costs anything. **The K/D shortcuts stay
removed on THIS five-card sheet** — at n=5 clicking is no slower and it is one less surface —
but the justification I removed them for was wrong, and **BL-1536's fifty-card sheet should
keep its shortcuts**, where fast keyboard grading genuinely earns its place.

**2. I twice concluded the guard was blocking legitimate clicks. It was not — I kept
missing.** The first click targeted the radio by reference, and that radio is a `1px`,
`opacity:0` input; the second landed on the "why" field because the page scrolled between my
screenshot and my click. I had started reasoning about relaxing the guard before checking
whether the control was being hit at all. A real coordinate click persists correctly.

**3. The deeper mistake behind all three.** Each time I inferred a mechanism from a pattern
that fitted, and changed code on it, before running the control that would have distinguished
it. The control that finally worked — close the tab and see if writes stop — was available
from the first minute and cost 90 seconds.

---

## WHERE THE `.bat` IS

```
output\bl1537_sheet\OPEN_BL1537_SHEET.bat
```

Double-click it. It picks a free port itself and opens the browser — there is no port to
remember. Five cards, KEEP or DROP on each, answers saved to disk on every click and fsynced
before the page confirms them.

---

*Round BL-1537. Claim filed in `.claims/BL-1537.json` and ended on completion. Backups in
`backups_bl1537_20260909/`, sha256-verified, both corruption controls fired.*
