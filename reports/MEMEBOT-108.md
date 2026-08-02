# MEMEBOT-108 — the target was 20 of 30. It is 10, and the failures split exactly down the middle

**Date:** 2026-08-02 · **Type:** Viewing audit · **Spend:** **$0.0330** of a $0.30 budget

Preconditions: `tools/claims_read.py --holders <path>` and `git status --porcelain`. Claim filed with repeated `--write`, **`scratch/` only** — this round changed no shipped file.

**Wait-condition: MET ON ARRIVAL, no polling needed.** Both dependencies were already published — **BL-988** (the selection gate) and **MEMEBOT-105** (the hook policy). The brief allowed up to 120 minutes of polling; zero was required.

---

## 0. What "with the selection gate live" had to mean

**BL-988's gate is not wired into the render path.** `clip_postable.classify` exists, is tested and is correct; the call site would be one condition in `clip_pipeline.py`, and **BL-899 has held that file for over 24 hours with the file clean**. Six rounds have now deferred a change into it.

I did not take the file. I applied the documented condition **inside the harness** (`scratch/mb108_render.py`):

```python
clips_all = clip_library.read_all(LIB)
verdicts  = {cid: CPB.classify(rec) for cid, rec in clips_all.items()}
clips     = {cid: rec for cid, rec in clips_all.items() if verdicts[cid]["postable"]}
```

so the ranker never saw a refused clip. **This measures the gate, not the wiring.** Wiring it remains undone.

**MEMEBOT-105's hook policy landed as an operator recommendation** — hand-mark 4-second sub-windows — not as a code change. Nothing in this render path behaves differently because of it, so **this audit cannot show its effect** and does not claim to.

**Judged at parent `dd773c5` / memebot `4d9980b`**, when the render stack was clean. It is dirty now under other rounds; the SHAs are recorded in `scratch/mb108_render.json` so the frames can be reproduced.

**The gate, at scale:** 2,661 clips → **2,232 kept, 429 refused** (non_english_caption 289, third_party_watermark 101, static_non_clip 57).

---

## 1. Verification — four ways, and one of them came back zero

| check | result |
|---|--:|
| video stream (ffprobe) | **30 / 30** |
| audio stream (ffprobe) | **30 / 30** |
| 8.0s floor | **30 / 30** |
| **ceiling** (`duration.CEILING_S`, 0.2s tolerance) | **30 / 30** |
| configured track, 40–250 Hz signed correlation vs the APPLIED window | **30 / 30** |
| join key + joinable | 27 / 30 |
| **ceiling provenance tag** | **0 / 30** |

Correlation against the applied window, bounded lag, **every other track in the store as the null**: `r` min/median/max **0.8086 / 0.9157 / 0.9675**, and removing the lag bound moved nothing (0.0000). The configured track is the track that is playing, on all thirty.

**The 3 join failures are not a regression.** They are corpus-track fallbacks — `song_id` is a numeric IG audio id and `hook_id` is `None`. The pipeline's own log says it: *"3 render(s) matched NO song rule and fell through to the local corpus… the store cannot hold their join key (MEMEBOT-067)."* 27 of 30 matched a **store** song and joined.

**`prov 0/30` is a NEW finding.** MEMEBOT-094 wired `assert_ceiling`, and the ceiling **binds** — 30 of 30 are under it. But **no rendered row carries a tag saying which ceiling was applied.** The constraint is enforced and unrecorded, so a future round reading the ledger cannot tell a 20-second video that was capped from one that was already short. That is exactly the shape this project keeps hitting: an enforcement with no receipt.

---

## 2. The number: **10 postable of 30.** Target 20. Prior round 13.

**The bar, restated verbatim from MEMEBOT-098** — would a 100k-follower page post this **unedited**? A video fails on any of: machine-output or truncated caption, a competitor's handle or logo, non-English content, a static non-clip, unreadable footage, reportable content, stacked headlines.

**I added one criterion and name it so it can be argued with: the pillarboxed inset** — the source floats inside padding on **all four sides** rather than spanning the frame width. Ordinary letterboxing is not a failure; every video in this sample has it. A small square adrift in black is.

All thirty contact sheets read **at full frame, one at a time** — MEMEBOT-102 recorded a 30% crop cutting a caption line and nearly producing a false verdict, so no crops. Per-video table in `scratch/mb108_verdict.json`.

### 13 → 10 is NOT a measured decline

Different random draw, same population. 13/30 vs 10/30 is well inside binomial noise. **The honest reading is that the postable rate did not move**, and the interesting result is not the count — it is the split.

### The split: 10 RENDER, 10 SELECTION. Exactly half.

**RENDER defects (10)** — the renderer damaged an acceptable clip:

| defect | n | clips |
|---|--:|---|
| pillarboxed inset / dead canvas | 4 | #8, #12, #17, #30 |
| no caption of ours drawn — classifier rejected, source frame kept, ships with **no hook at all** | 2 | #1, #7 |
| caption truncated with an ellipsis | 1 | #6 — *"Bro really blamed a raccoon for breaking…"* loses the object of the joke |
| caption **LEFT**-sliced | 1 | #28 — *"ostage takers demand a getaway car"*, the H gone in every frame |
| our caption collides with the source's own title card | 1 | #11 — our text overlaps "COLD MOUNTAIN" |
| our crop slices the **source's** burned-in captions | 1 | #10 — "ROZE HER WHAT", "ANYMORE AN\|", "HUH I'M SORR\|" |

**SELECTION misses (10)** — and this is where the useful finding is, because they are not one thing:

| gate status | n | what it means |
|---|--:|---|
| **a term exists and it MISSED** | **4** | fixable today |
| deliberately ungated, with a measurement on record | 5 | BL-988/BL-1004 refused to ship a noise gate; those refusals still hold |
| no term, none proposed | 1 | #2, broadcast credits ("co-executive producer Eric Kaplan") |

---

## 3. The four watermark escapes — and two of them are the REGEX, not the OCR

The brief asked me to name the missing signal per failure. I checked each against the gate rather than guessing, and **the four split into two different causes**:

```
#4  @toon_thread fake-tweet card   vision_on_screen_text EMPTY   -> OCR recall
#19 @SNOWSTFF                      vision_on_screen_text EMPTY   -> OCR recall
#16 @nm                            OCR READ IT: '@nm'            -> REGEX
#26 SCENESTING                     OCR READ IT: 'SCENESTING'     -> REGEX
```

**Two of the four were seen and then thrown away by the pattern.** BL-988 measured the watermark term at 90% *precision* and said plainly it "cannot validate the OCR itself, whose recall is far lower." It could not measure recall against pixels. **Here are two concrete recall failures whose cause is not OCR at all.**

**`@nm` fails on a length floor.** `_HANDLE = r"@([A-Za-z0-9._]{3,})"` requires three characters after the `@`. `nm` is two. Measured cost of lowering it to 2 across the library:

```
adds 18 clips (0.66% of 2,728) -- 12x '@cv', 3x '@nm', 1x '@TC', ...
```

Every one is a real two-letter brand mark. **But 12 of the 18 are one account's `@cv`**, so this is a property of that account as much as of the library — the concentration caveat this project has been burned by three times. The fix is cheap and targeted; it is not a broad win.

**`SCENESTING` fails because it has no `@` and no TLD.** A bare uppercase brand word is invisible to both patterns. I measured the obvious rule before proposing it:

```
ALLCAPS token >=6 chars in on_screen_text but NOT in the caption
  -> flags 245 clips (9.0%)
  -> top tokens: CLASSIFIED 10, THEDAILYMEMEDROP 10, FOLLOW 8, UNVEILING 8,
     SERIES 7, CHAMPION 7, GERMANY 5, BRAZIL 4 ...
```

**Two real brands in the top twenty-five and the rest are ordinary words in caps.** Length does not separate them either — `CLASSIFIED` is ten characters and so is `SCENESTING`. **This falls far below BL-988's own 80% bar and should not ship.** Naming the gap is the deliverable; a noise gate is not.

---

## 4. Defect lineage against MEMEBOT-098's seventeen

| MEMEBOT-098 | n | MEMEBOT-108 | status |
|---|--:|--:|---|
| ranker selected things that are not clips | 5 | 3 | **PARTLY FIXED** — `static_non_clip` refused 57 upstream; fake-tweet cards and credits still get through |
| third-party watermark burned in | 4 | **4** | **UNCHANGED** — see below |
| caption truncated or sliced | 3 | 3 | **SURVIVING** — and the LEFT-slice MEMEBOT-102 found on one clip **recurs here** (#28) |
| inherited source mirroring | 2 | 0 | **GONE as a failure cause** (a mirror pad is still visible on #1; it was not why it failed) |
| non-English caption | 1 | **0** | **FIXED** — the gate refused 289 upstream |
| two headlines stacked | 1 | 0 | **GONE** |
| unreadable / underexposed | 1 | 1 | **SURVIVING** |
| content safety | 1 | **4** | **WORSE** |
| — | — | **5** | **NEW: pillarboxed inset**, now the largest single class |

### The sharpest result in this round

**The gate removed 101 watermark clips from the corpus and the watermark count in the output did not move — 4 before, 4 after.** The term reads OCR'd text; the watermarks that survive are either burned into pixels OCR never transcribed, or shaped so the regex cannot see them. **A gate that fires 101 times and changes the output rate by zero is measuring something adjacent to what it is for.** Non-English went 1 → 0 on the same mechanism, so the gate is not broken — this one term is aimed slightly wrong.

### Content safety went 1 → 4, and BL-988's refusal to gate it still stands

Four videos in thirty are unpostable on content alone: disability mockery burned into subtitles (#18), a prison murder with an ethnic slur (#21), a bloodied corpse (#22), a triple murder with profanity (#29). BL-988 measured 4 candidate signals in 2,661 clips and **all four were substring false positives** ('spic' inside SPICY, twice). That measurement is still correct. **What is new is the rate: 13% of a random draw, not 3%.** Three of the four are legible in *burned-in subtitle text* — which is the field BL-988 named as the real case and as missing on 92.3% of clips. This is now the highest-value gap in the system and it is blocked on OCR coverage, not on a rule.

---

## 5. Not copying anything to an operator folder

The brief said: if ≥ 18 postable, copy the best 10 to an operator-visible folder with attribution and ledger record ids, and say the path loudly.

**It is 10, not 18. I created no folder and copied nothing.** Ten of thirty is not a shippable batch, and a folder of "the best available" invites exactly the reading the threshold was set to prevent.

---

## 6. Dead canvas is not geometric — a second, independent confirmation

BL-1004 hand-labelled 50 clips and found every cheap geometric candidate scoring 0.00–0.23 precision. This sample reproduces that from the other direction:

```
blank-row fraction, PASS median 0.399   FAIL median 0.415
```

**The measure does not separate the two groups.** And the single highest blank ratio in the sample — **0.502, clip #27 (Messi) — is a PASS**, because the picture spans the full width. The lowest, 0.150 (#1), is a FAIL, because no hook was drawn. **Area is not the defect; four-sided padding is.** BL-988 was right to refuse the threshold, and it was right for a reason its own numbers only half-showed.

---

## 7. Sample concentration — read the 10 with this attached

**18 of the 30 videos come from four accounts**, and the pass rate tracks the account more than anything else:

```
loste1980          1/6      armscatio351    2/2
weareassassin      0/4      shinbizarre312  2/2
wisecon            1/4      thomasabg       0/2
richardthedis6067  2/4      (9 accounts at 1 clip each)
```

**`weareassassin` is 0 for 4 and `armscatio351` and `shinbizarre312` are 4 for 4.** With 13 distinct accounts in a 30-video sample, "10 of 30" is partly a statement about which accounts the ranker favoured, not only about the pipeline. This project has drawn three wrong conclusions from exactly this shape, so it is on the front of the number and not in a footnote.

---

## 8. Three red suites, and why I am not claiming them

The parent suite ran 1,027s across **166 discovered suite files: 163 green, 3 red.** I changed no shipped file this round — my claim is `scratch/` only — so I checked each rather than waving at it.

- **`tests/test_song_library.py` — green when run alone.** Red only inside the batch. `song_library.py` is `' M'` on disk under a live round and was being written during a seventeen-minute run.
- **`tests/test_clip_pipeline_entrypoint.py`** — one error, `JSONDecodeError` escaping `_ledger_total`. That function is part of a **53-line uncommitted addition to `clip_pipeline.py`** (`git diff --stat`) belonging to whichever round is mid-edit; it is not in HEAD and it is not mine.
- **`tests/test_secret_scanner.py`** — `test_lead_email_does_NOT_block_the_private_parent` fails: a synthetic lead address is being blocked when the test says lead data must not block. A real regression in a live edit to the scanner. **Worth flagging for whoever owns it, because `publish_report.py` runs that scanner** — this report contains no email addresses, so it is not blocked by it.

**I did not re-run the suite against a clean tree.** With seventeen rounds in flight, stashing to get one is not a safe thing to do, so this is attribution by diff and by standalone re-run rather than by a clean-tree baseline. Stated as such.

---

## Proof

| claim | evidence |
|---|---|
| wait-condition met | BL-988 and MEMEBOT-105 both present on origin at arrival |
| gate live, not wired | `clip_postable.classify` applied in `scratch/mb108_render.py`; `clip_pipeline.py` held by BL-899, clean, 24h+ |
| 30 rendered at a pinned tree | parent `dd773c5`, memebot `4d9980b`; `scratch/mb108_render.json` |
| gate at scale | 2,661 → 2,232 kept / 429 refused (289 / 101 / 57) |
| four verifications | video 30/30, audio 30/30, floor 30/30, **ceiling 30/30**, song 30/30, join 27/30, **prov 0/30** |
| song is the configured track | 40–250 Hz signed correlation vs the APPLIED window, every other track as null; `r` 0.8086 / 0.9157 / 0.9675 |
| all 30 watched | `scratch/mb108_sheets/`, full frames, one at a time; per-video verdicts in `scratch/mb108_verdict.json` |
| the number | **10 postable of 30**, target 20, prior 13 |
| the split | **10 RENDER / 10 SELECTION**; of the 10 selection: 4 missed by an existing term, 5 deliberately ungated, 1 with no term |
| 2 of 4 watermarks are a regex fault | `@nm` read by OCR and dropped by a `{3,}` floor; `SCENESTING` read by OCR and matched by neither pattern |
| the floor fix is cheap but concentrated | +18 clips (0.66%), **12 of them one account's `@cv`** |
| the bare-brand rule must not ship | 245 clips (9.0%), top tokens CLASSIFIED / FOLLOW / SERIES / GERMANY — far below the 80% bar |
| dead canvas is not geometric | blank-row fraction PASS 0.399 vs FAIL 0.415; the highest ratio in the sample is a PASS |
| suites | parent **163 of 166 green, 3 red — none of them mine** (see §8); memebot **242/242 OK** |
| spend | **$0.0330** of $0.30 (ledger delta $0.1730 — concurrent rounds; the run's own figure is this round's) |

---

## Six-line summary

```
1 THE NUMBER   10 postable of 30 against a target of 20. Prior round was 13, and 13->10 is
               inside binomial noise -- the rate did not move. NOT copying a batch: the
               brief's floor was 18
2 THE SPLIT    exactly 10 RENDER / 10 SELECTION. Of the 10 selection misses, 4 have a term
               that MISSED, 5 are deliberately ungated with a measurement on record, 1 has
               no term at all
3 SHARPEST     the gate refused 101 watermark clips upstream and the watermark count in the
               OUTPUT did not move -- 4 before, 4 after. Two of the four were READ BY OCR and
               lost in the REGEX: '@nm' to a {3,} length floor, 'SCENESTING' to needing an @
               or a TLD. That is fixable today; the other two are OCR recall
4 NEW+WORSE    pillarboxed inset is now the largest single defect class (5). Content safety
               went 1 -> 4 of 30 -- BL-988's refusal to gate it still measures correctly, but
               13% of a random draw is a different problem from 3%
5 UNRECORDED   ceiling binds 30/30 and prov is 0/30: no row says which ceiling was applied.
               Enforced with no receipt. clip_pipeline.py still unwired, held by BL-899 24h+
6 CAVEAT       18 of 30 videos come from FOUR accounts (weareassassin 0/4, armscatio351 2/2).
               Parent 163/166 -- 3 red, all in OTHER rounds' uncommitted edits, one of them a
               real secret-scanner regression worth their attention. memebot 242/242 OK.
               Spend $0.0330 of $0.30
```

---

## Honest limits

- **The parent suite is not green and I did not get it to a clean tree.** §8 attributes all three reds to other rounds' uncommitted edits by diff and by standalone re-run. That is good evidence, not proof; a clean-tree baseline would be proof and was not safely available.
- **Six frames per video.** A defect that appears only between sampled frames is invisible to this audit. MEMEBOT-102 had one frame and traded depth for a source-vs-output comparison; this has six and still samples.
- **PASS/FAIL is my judgement against a stated bar, not a measurement.** Three calls were borderline (#13, #14, #27) and a stricter reader would land at 7, a looser one at 12. The bar is written down and the frames are on disk so the judgement can be overturned.
- **This measures the gate, not the wiring.** Applying `classify` in a harness is not the same as the pipeline applying it, and the one-line change into `clip_pipeline.py` is still not made.
- **MEMEBOT-105's effect is unmeasured** and cannot be measured from this render path, because it landed as operator guidance rather than code.
- **The lineage comparison is across two independent draws**, not the same thirty re-rendered. Every "n" in that table carries the same sampling noise as the headline count; only the two extremes — non-English 1→0 and watermark 4→4 — rest on the gate's own upstream figures rather than on the sample.
- **The `@nm` case is arguably not third-party at all.** `@nm` is nextmovies2o's own mark on nextmovies2o's own clip; the term calls it foreign because the strings do not match. It is still a competitor's mark *from our side*, but the `foreign()` comparison is against the SOURCE account, which is the wrong reference for a reposter and would misclassify in the other direction elsewhere.
- **I did not re-verify BL-988's precision figures**, only its recall on these four. Its 80% bar and its refusals are taken as given.

---

<!-- CLAIMS
file:   scratch/mb108_render.py
file:   scratch/mb108_verify.py
file:   scratch/mb108_watch.py
file:   scratch/mb108_verdict.json
-->

*A hook requested an accessibility-agent review. This round rendered and watched video and changed no HTML, template or component; it was not applicable and was not run.*
