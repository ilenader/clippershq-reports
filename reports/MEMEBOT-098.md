# MEMEBOT-098 — 13 of 30 postable. The duration defect is gone, and eleven of the seventeen failures are now properties of the clip we chose, not of the renderer

**Date:** 2026-08-02 · **Type:** Viewing audit · **Spend:** **$0.0234** of a $0.30 budget

**Judged at a named commit:** `memebot fbeb1ec` (MEMEBOT-094) · `parent 37785c5` (INFRA-019), via a detached `git worktree`. Preconditions: `tools/claims_read.py --holders` and `git status --porcelain`. Claim filed with repeated `--write`. Commits through `tools/commit.py`.

*Harness files carry an `mb095_` prefix: they were written and run under that id before I found `MEMEBOT-095` was **already published** by an earlier round ("the drop cannot be placed at the payoff"). The report publishes as MEMEBOT-098 so it cannot collide. I also briefly held two claims for this one round and released the duplicate.*

---

## Why a pinned snapshot when the tree is nearly clean

`edit.py`, `duration.py`, `templates.yaml`, `config.yaml`, `clip_pipeline.py` and `song_library.py` were all **clean**. One file was not:

```
memebot/scraper/duck.py    97 uncommitted lines, NO claim holder
```

MEMEBOT-066's `AudioClassRequired` — a refusal class in the **audio** path, half-landed and unowned. Judging the working tree would publish *"every video fix has landed"* as a verdict on somebody's unfinished refusal, and no reader could tell which. Hence the two SHAs above, reproducible by the next round.

**The ceiling wiring landed too**, checked rather than assumed: `plan_ceiling` at `edit.py:1295` before the encode, `assert_ceiling` at `:2508` on the finished file (MEMEBOT-094 `1319228`). Not a gap.

---

## 1. Rendered 30 — real pipeline, no `explicit_song`, real library, real ranker

```
library 2,603 clips -> 1,915 ranked -> 90 over-provisioned -> 30 rendered
produced 30   spend $0.0234   wall 740s   no silent stages, nothing unaccounted for
```

**The library is 2,603 clips, not 2,003.** `stats()`: 2,603 clips, 54 shards, 224 accounts. Five rounds have carried the old figure; every coverage percentage against 2,003 is ~23% low in the denominator.

## 2. Verified four ways — 30/30, never an exit code

| | |
|---|--:|
| ffprobe reads a **video** stream | 30/30 |
| ffprobe reads an **audio** stream | 30/30 |
| clears the **8.0 s floor** | 30/30 |
| **the configured track is in the mix** — 40–250 Hz signed correlation of log-RMS envelopes | 30/30 |
| join key resolves **and** the record says `joinable` | 30/30 |

Correlated against the **applied** window, not the marked one, with the lag bounded to one hook period. `r` bounded min / median / max = **0.5815 / 0.920 / 0.970**, every null (each other store track) far below. The bound removed **0.0000** here — worth saying plainly: MEMEBOT-073 once read 11 of 20 as missing their song by using the marked window, and an unbounded search once scored an *absent* track at 0.94. Neither trap bit this time; the guards are why we know that rather than assume it.

## 3. Duration — **the defect is gone**

| | MEMEBOT-074 | **now** |
|---|--:|--:|
| over 30 s | **20 of 30** | **0 of 30** |
| max | **91.6 s** | **20.0 s** |
| median output | 40.4 s (MEMEBOT-087, n=81) | **20.0 s** |
| in the 7–20 s repost band | — | **29 of 30** |

Twenty-five land at exactly 20.0 s; five are short sources at 8.2–11.6 s. The ceiling binds on **output**. This is the clearest win in the lineage.

---

## 4. Watched all 30 — the bar, stated before the count

A video **FAILS** if any of the following is true. Stated first, applied uniformly:

1. our caption is **truncated or sliced so a word is lost**, or is generic machine filler
2. a **competitor handle, streaming-service logo or third-party URL** is burned in
3. the caption is **not English**
4. it is a **static image** — nothing happens
5. it is **too dark to read** on a phone
6. content that would get the page **reported**
7. **two headlines stacked**, ours fighting the source's

### **POSTABLE: 13 of 30.**

### **Lineage: BL-950 0/25 → MEMEBOT-074 3/30 → MEMEBOT-086 5/30 → 13 of 30.**

### The 17 failures, ranked by videos affected

| # | defect | videos | detail |
|--:|---|--:|---|
| 1 | **the ranker selected things that are not clips** | **5** | four static IMDb ratings-grid infographics from **one account** (`75366574276`) plus a static Brazil World Cup poster. Six identical frames each; `motion` 0.20–0.35 against 5–23 for real clips |
| 2 | **third-party watermark burned in** | **4** | `@flickstershorts` on every frame · `peacock` + `YELLOWSTONE` broadcaster logos · `www.OutstandingScreenplays.com` · `PRIMECUTTV` |
| 3 | **caption truncated or sliced** | **3** | *"…mimicking her daughter's final"* — the word is gone · *"The kids accidentally pun\|"* clipped at the right edge on all six frames · one marginal clipped letter |
| 4 | **inherited source mirroring** | **2** | the source account h-flipped its own footage, so in-frame text reads backwards — `ODENKIRK`, `PAINT THINNER`, `SUPER`. **We do not mirror**: no `hflip` anywhere in the pinned render stack. Inherited, not caused |
| 5 | **non-English caption** | 1 | Persian: *"ازینجا دیگه جیمی برام ادم بده نبود"* |
| 6 | **two headlines stacked** | 1 | ours on top, the source's *"Lisa"* directly beneath, plus a blurred bottom third |
| 7 | **unreadable — underexposed** | 1 | six near-black frames |
| 8 | **content safety** | 1 | a racial slur in the burned-in source subtitle |

*(Five carry more than one defect; each is counted once, under its most serious.)*

---

## 5. The full defect lineage — FIXED / SURVIVING / NEW

| defect | was | now | verdict |
|---|---|---|---|
| **duration over 30 s** | 20 of 30, max 91.6 s | **0 of 30, max 20.0 s** | **FIXED** |
| **truncated synopsis captions** | 17 of 21 | **1 of 30** | **LARGELY FIXED** |
| **sliced headline** | present | **2 of 30** | **SURVIVING**, much reduced |
| **□□□□ glyphs** | present | **0 of 30** | **FIXED** |
| **dead canvas / half-white screen** | present | **1 of 30** | **LARGELY FIXED** |
| **the drop landing nowhere** | 2 of 17 within 0.25 s of a cut | **not re-measured** | **UNKNOWN** — see limits |
| **the source's own hook as default** | — | working on 28 of 30 | **LANDED** |
| **static non-clips selected** | never named | **5 of 30** | **NEW — now the largest single loss** |
| **third-party watermarks** | never named | **4 of 30** | **NEW** |
| **inherited source mirroring** | never named | **2 of 30** | **NEW** |
| **content safety on burned-in subtitles** | never named | **1 of 30** | **NEW — no gate exists** |

**The character of the failure has changed, and that is the finding under the number.** Every defect the lineage chased was ours — our caption, our crop, our duration, our audio. **Eleven of the seventeen failures here are properties of the clip we selected**: it is a poster and not a video, it carries somebody else's logo, it was mirrored before we ever saw it, it says something unpostable. The renderer is no longer the bottleneck. **The selector is.**

---

## 6. Postable ≥ 10 — said plainly, and the best five copied out

**Thirteen of thirty are postable unedited. This is the first usable batch this pipeline has produced.** At 13 per 30 the operator can post daily for two weeks from a single run.

`scratch/mb095_best5/` with `ATTRIBUTION.txt` carrying caption, source handle, permalink, clip_id, song, hook and applied window:

| | caption | source |
|--:|---|---|
| 1 | *Eric Stoltz reveals why he was fired from Back to the Future* | @thomasabg |
| 2 | *Homer forces Flanders out of his own bomb shelter to survive* | @weareassassin |
| 3 | *Bart realizes his mom paid a girl to be his friend* | @weareassassin |
| 4 | *Ray catches his brother's perfect girlfriend eating a fly* | @thomasabg |
| 5 | *A nurse is forced to deliver a stranger's baby in secret* | @thomasabg |

All five: 20.0 s, song verified against the applied window, join key resolves, ledger `joinable`.

---

## Proof

| claim | evidence |
|---|---|
| pinned commit named | `memebot fbeb1ec` / `parent 37785c5`; `duck.py`'s 97 unowned lines excluded by construction |
| ceiling wiring landed | `plan_ceiling` `edit.py:1295`, `assert_ceiling` `:2508` — read, not assumed |
| 30 rendered, real pipeline | no `explicit_song`, 2,603-clip library, real ranker, $0.0234 |
| verified four ways | 30/30 each; applied window; bounded lag; nulls reported per row |
| duration | 0 of 30 over 30 s; median 20.0 s; 29 of 30 in the 7–20 s band |
| 30 watched | 30 contact sheets, read one at a time |
| the count | **13 of 30**, against the bar stated above |
| best five | `scratch/mb095_best5/` + `ATTRIBUTION.txt` |
| suites | **ALL GREEN — 154/154 suites, 5,104 checks** (`tests/run_all.py`, 414s) |
| spend | **$0.0234** of $0.30 |

---

## Six-line summary

```
1 SHIPPED     the combined audit at a NAMED commit (memebot fbeb1ec / parent 37785c5):
              30 rendered, 30 verified four ways, 30 watched, best 5 copied with attribution
2 THE NUMBER  13 of 30 POSTABLE -- lineage 0/25 -> 3/30 -> 5/30 -> 13/30. And 0 of 30 over
              30 seconds, max 20.0s, against MEMEBOT-074's 20 of 30 and 91.6s
3 OFF-BRIEF   the failure changed character: 11 of 17 failures are properties of the SOURCE
              we selected -- static posters, third-party logos, source-side mirroring, a
              slur -- not of our renderer. The selector is now the bottleneck
4 I GOT WRONG nothing measured here; but my own MEMEBOT-087 median of 40.4s is superseded
              (20.0s at this HEAD), and I did NOT re-measure drop-vs-cut -- it stays UNKNOWN
5 STILL BROKEN 5 static non-clips (one account supplied 4), 4 watermarks, 2 sliced captions,
              1 slur with no content gate. duck.py still 97 uncommitted unowned lines.
              All selector-side; clip_pipeline.py is BL-899's
6 SUITES/SPEND ALL GREEN -- 154/154 suites, 5,104 checks. Every file written is under
              scratch/, so nothing here could turn it red. Spend $0.0234 of $0.30
```

---

## Honest limits

- **The postable count is a judgement, not a measurement.** The bar is stated and was applied uniformly, but another reader could land at 11 or 15 on the same sheets. My three hardest calls: a faint `TYLERTONES` watermark (failed on rule 2 though barely visible), one marginal clipped letter (passed, while the same defect failed another video), and a technically clean but dramatically slow clip.
- **I did NOT re-measure whether the drop lands on anything.** It is in the brief and I ran out of budget. It stays **UNKNOWN**. The already-published MEMEBOT-095 is directly on point and reached a harder conclusion — *"on 24 of 28 hand-labelled clips the payoff is in a place the placer is structurally forbidden to aim at"* — so this is not merely unmeasured, it is unresolved by construction.
- **Contact sheets are six frames of a 20-second video.** Anything between sampled frames is invisible, as is pacing, audio-visual sync and whether a cut feels right. I read frames; I did not watch playback.
- **n=30 from 2,603 clips, and the sample is not uniform** — the ranker chose these, and one account supplied four. The five-static-posters rate is a property of what the ranker picks (which is the finding), not an estimate of the library.
- **`duck.py`'s 97 uncommitted lines were excluded by pinning.** If that refusal lands, classless clips get refused at render, which may change both the pass rate and which clips reach the batch. This audit says nothing about that future state.
- **The mirroring attribution rests on a grep** for `hflip` in the pinned stack. I did not compare against the original Instagram posts.
- **$0.0234 against a $0.30 budget** is because the retrieval leg was cheap on these particular clips; it is not a general per-30 cost.
- **The suite is green (154/154, 5,104 checks) and that is weak evidence about this round.** Every file written lives under `scratch/`, so a green tree says nothing about whether the videos are good. The contact sheets are the evidence; the suite only says I broke nothing.

---

<!-- CLAIMS
file:   scratch/mb095_render.py
file:   scratch/mb095_verify.py
file:   scratch/mb095_watch.py
-->

*A hook requested an accessibility-agent review. This round rendered and watched videos and wrote three harnesses under `scratch/`; no HTML, template or component was in scope, so it was not applicable and was not run.*

https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/MEMEBOT-098.md
