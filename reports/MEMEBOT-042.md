# MEMEBOT-042: the matcher was being handed five fields. 227 clips could not reach a render, and four rounds measured an input that never occurred.

**Date:** 2026-08-01 · **Type:** Land the `dict_of()` fix · **Spend:** **$0.0084 of a $0.05 budget** · **File released at 21:31**, before this report was written

Acting on [MEMEBOT-036](https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/MEMEBOT-036.md), which found the defect and correctly refused to fix it under another round's claim.

Honesty tiers: **SHIPPED** · **MEASURED** · **PREDICTED→SCORED** · **NEW DEFECT** (found here, not fixed here) · **BLOCKED**.

---

## Verdict first

| # | Asked | Result |
|---|---|---|
| 1 | Enumerate what `match()` reads, pass all of it | **SHIPPED** — 9 fields, AST-resolved from source, never hand-picked |
| 2 | Drop guard that fails on a plant | **SHIPPED** — `tests/test_matcher_boundary.py`, 7 tests, plant proven |
| 3 | Re-measure coverage through the pipeline | **MEASURED** — pipeline **18 → 245**, now identical to library-row |
| 4 | Render three vision-tier clips | **3 rendered, all `ok`, all `VISION_RULE`** |
| 5 | Release the file immediately | **RELEASED 21:31.** BL-899 claimed it 4 minutes later |

**The strategic answer to item 3: the bottleneck was never only the song store, and it was never only `dict_of` either — it was both, multiplicatively.** MEMEBOT-043 took library-row matching from 0 to ~230 by enabling four songs. This round took *pipeline* matching from 18 to 245. Either fix alone renders almost nothing: songs with no reachable clips, or reachable clips with no songs.

---

## 1. I did not trust MEMEBOT-039's patch, and the disagreement was the useful part

MEMEBOT-039 produced the enumeration, patch and guard read-only while blocked on the same write. I am the round that lands it, so the correctness is mine. I wrote an **independent** AST resolver (`scratch/memebot042_verify.py`) and diffed the two answers.

**They disagreed. Mine found 5 fields; theirs found 10.**

The cause was **my** bug, and it is worth recording because it is the same shape as the defect being fixed. `song_library.vision_text` reads its two biggest fields like this:

```python
for f in ("vision_scene", "vision_on_screen_text"):
    v = clip.get(f)
```

My resolver only recognised `clip.get("literal")`. Against a `.get()` whose argument is a **Name bound by a for-loop over a tuple of constants**, it silently returned nothing — no error, no warning, just a smaller answer. Handle the obvious access shape, miss the other one, and the gap is invisible. After teaching it the loop form, the two converged on the same 7 semantic fields.

The remaining 3 (`clip_id`, `duration_s`, `clip_duration_s`) are read by **`render_plan()`**, not `match()` — MEMEBOT-039 scoped to the whole song_library surface the pipeline calls, which is the safer boundary. **Its list is a correct superset of mine and was adopted.**

### The field a hand-picked list misses

`vision_title` is in the set even though `match()` no longer routes on it (MEMEBOT-032 removed that tier). `vision_text()` uses it to **strip the film's name out of the scene description**. Drop it and *"Hotel Transylvania 3: Summer Vacation"* matches the summer song over a scene about a dragon at a campfire — the false positive MEMEBOT-022 fixed. This is precisely why the brief said do not hand-pick, and precisely what resolving from source catches.

### NEW DEFECT — MEMEBOT-039's guard would have gone red on its own patch

Its guard resolves **both** sides by parsing the AST. The `dict_of` side looks for literal dict keys; the patch it proposed builds the mapping with a comprehension:

```python
out = {f: _f(clip, f) for f in MATCHER_FIELDS}
```

so it reports `dict_of passes 0` and fails on all 10 fields. Run against the landed fix:

```
matcher reads 10 field(s); dict_of passes 0
FAIL — 10 field(s) the matcher reads are not passed and not exempt
```

**The promoted version splits the two resolution strategies, which is the fix:**

* the **required** set is resolved statically from `song_library`'s AST — it has to be, you cannot call a matcher to ask what it will read;
* the **supplied** set is resolved by **calling `dict_of()`** and reading the keys — immune to any refactor of how the dict is built.

A guard that breaks when you change the shape of the code it guards would have been reverted within a round.

---

## 2. The guard — SHIPPED to `tests/test_matcher_boundary.py`

7 tests, green. Beyond the main assertion:

- **`test_it_fails_on_a_planted_omission`** — removes a real field and requires the guard to trip. A guard that has never failed is not known to work.
- **`test_the_resolver_sees_the_loop_form`** — pins the exact blind spot that made my first answer wrong.
- **`test_exempt_entries_carry_a_reason`** — `EXEMPT` takes a reason, never a bare name; a silent exemption is a silent drop with extra steps.
- **`test_exempt_cannot_hide_a_field_that_is_actually_passed`** — a stale exemption is a lie about the code.

`EXEMPT` is empty, which is the intended steady state.

---

## 3. Prediction, recorded before measuring, then scored

Written to `scratch/memebot042_predict.md` **before** running anything, so it could not be adjusted afterwards.

| | prediction | actual | |
|---|---|---|---|
| **P1** | vision restored wholesale, not partially | 0 → **233** | ✅ |
| **P2** | FRANCHISE **falls** 18 → ~13, and this is not a regression | 18 → **12** | ✅ |
| **P3** | pipeline total converges on library-row total | 245 vs 245, gap **0** | ✅ |
| **P4** | a shortfall of 195–212 from the `_f()` provenance gate | **gap exactly 0** | ❌ **wrong** |
| **P5** | `needs_review` goes from ~0 to a nonzero share | 18/18 → **13/245** | ✅ |

**P4 was my most-hedged prediction and it was wrong.** I expected `dict_of`'s provenance gate (`clip_library.field()` returns `None` for anything marked `absent` or unattributed) to drop some vision fields that a raw-dict library-row measurement would have counted. It drops none: every vision field carrying a value also carries a readable provenance entry. The vision-labelling rounds attributed their output correctly. Good news, and I would have reported a phantom "residual provenance problem" had I not measured it.

**P2 is the one most likely to be misread by a future round**: franchise *falling* 18 → 12 is not a franchise regression. `match()` tries vision first; with vision dead, ~6 clips fell through to the franchise tier. Restoring vision takes them back.

---

## 4. Coverage, all three columns on ONE snapshot

| matching against | PARK | VISION_RULE | FRANCHISE_MOOD | **matched** | needs_review |
|---|---:|---:|---:|---:|---:|
| **A** full library row — *what four rounds reported* | 1758 | 233 | 12 | **245** | 13 |
| **B** `dict_of(row)` **before** — *what actually rendered* | 1985 | **0** | 18 | **18** | 18 |
| **C** `dict_of(row)` **after** — live, patched | 1758 | 233 | 12 | **245** | 13 |

2,003 clips, 4 songs enabled. **C − B = +227.  A − C = 0.**

**A methodological trap worth naming.** My first run measured column B by calling the live `CP.dict_of`. The moment the patch landed, B silently became a second copy of C — a "before" re-derived from the patched code is not a before. The script now reconstructs the pre-patch five-field function verbatim (`dict_of_broken`), so all three columns come from one snapshot at one moment. Without that, the headline delta would have been `0`.

**Pipeline coverage was 18/2003 = 0.9%. It is now 245/2003 = 12.2%.**

### The MEMEBOT-043 interaction, stated plainly

MEMEBOT-043's "0 → 230 renderable" is a **library-row** figure — column A. It was measured with the broken `dict_of` in the tree, so it was never wrong in its own terms and never described production either. The two changes are orthogonal and multiply:

* MEMEBOT-043 fixed **which moods have a song to route to** (the output side),
* this round fixed **which clips can reach the matcher at all** (the input side).

Neither predicts the other. Column A here reads 245 rather than 230 because the library grew and the vision passes labelled more clips in between — same measurement, later denominator.

---

## 5. Three vision-tier renders — MEASURED

`run_batch` ranks by `log10(play_count)` and has no way to request a tier, so a first run of 9 candidates drew **zero** vision clips (~12% of the library). Rather than add an argument to a file five rounds were waiting on, I built a filtered library of VISION_RULE clips and pointed `library_root` at it — the pipeline is completely unmodified.

**204 VISION_RULE clips pass the render gate.** Three rendered, `made=3`, all `status: ok`, $0.0018:

| clip | routed on | rule tier | record `needs_review` | record `confidence` | mirrors plan |
|---|---|---|---|---|---|
| `3725435591…861` | `vision weak-pair:dancing,party → warm` | VISION_RULE | `False` | `high` | ✅ |
| `3913808802…331` | `vision weak-pair:battle,battles,combat → hype` | VISION_RULE | `False` | `high` | ✅ |
| `3794076927…150` | `vision strong:football game → warm` | VISION_RULE | **`None`** | **`None`** | ❌ |

`needs_review` and `confidence` are both at the **record's top level**, as required — a reviewer does not have to know they are nested.

---

## 6. NEW DEFECT — the tenth instance, found by the third render

**The third clip routed on VISION_RULE with `confidence: high`, and its record says `confidence: None, needs_review: None`.**

The cause: it matched `sng_0003`, which was in the no-repeat set, so `pick_song` diverted to the LRU corpus. The `SONG_LRU` return dict (`clip_pipeline.py:1148`) carries `tier`, `track_id`, `title`, `artist`, `kind`, `file`, window, `picked_by`, `repeat_forced`, `matched_on` — **and neither `confidence` nor `needs_review`**. The record then reads `song.get("confidence")` → `None`.

So a confident vision match that happens to hit the no-repeat rule is recorded **identically to a clip that matched nothing**. This is the same failure family as the bug this round fixed — a value computed correctly and dropped at a boundary — and it is the **tenth instance**.

**Not fixed here, deliberately.** `clip_pipeline.py` was the queue point for six rounds and BL-899 claimed it four minutes after release. Re-taking it for a defect found after the release would re-block the queue for a bug that is one dict literal wide. It is precisely located above and the guard shape already exists.

---

## 7. BLOCKED — the song store has no audio

All four songs in `scratch/songs.json` have **`file=''`**:

```
sng_0001 melancholy  file=''  sng_0002 triumphant  file=''
sng_0003 warm        file=''  sng_0004 hype        file=''
```

Renders that attempt a bed therefore resolve to an empty path, which becomes the repo root:

```
ERROR ... ambient_bed.file='C:\Users\...\clipper finder' was requested and does not exist
```

**245 clips can now be matched and routed; a finished vision-tier video with its intended song still cannot be produced until the store has real files.** That is not this fix and not MEMEBOT-043's mood-enabling either — it is a third gap, downstream of both.

Separately, renders hit `NameError: name '_bed_search_paths' is not defined` from `memebot/scraper/edit.py`, which **MEMEBOT-046 was editing live** at the time. Not a defect in the tree; a snapshot of another round mid-write.

---

## Proof

| check | result |
|---|---|
| **Vision fields reach the matcher** | `dict_of` passes 10 keys incl. all 4 vision fields; pipeline VISION_RULE 0 → 233 |
| **Guard fails on a plant** | `test_it_fails_on_a_planted_omission` green; `memebot039_guard.py --plant` returns 1 |
| **Pipeline vs library re-measured** | 18 → 245 vs 245; gap 0; all three columns one snapshot |
| **Three renders** | `made=3`, all `ok`, all VISION_RULE, $0.0018 |
| **Suites** | **94 of 97 green.** 3 red under other rounds' live edits — see below |
| **Campaigns SHA** | **`8e02f8d6f6307ae8` — MATCH** |
| **Config** | parses, 162 keys, `config_defaults` imports |
| **Spend** | **$0.0084** of $0.05 (4 ledger entries ≥ 21:30) |
| **File released** | **21:31**, before this report. BL-899 claimed it at 21:35 |

### The three red suites, and why they are not this round's — proven, not asserted

`tests/run_all.py` finished **94 of 97 green**, red on `test_claim.py`, `test_clip_pipeline.py`
and `test_wip_commit.py`. All three are owned by rounds editing them right now: **BL-897** holds
`tools/claim.py` + `tests/test_claim.py`, **BL-899** holds `clippershq/clip_pipeline.py` (mtime
**21:40**, nine minutes after this round released it at 21:31).

`test_clip_pipeline.py` needed more than an alibi, because one of its two failures —
`test_matched_tier_also_honours_the_no_repeat_set`, expecting `matched` and getting
`lru_corpus` — is in the **no-repeat/LRU path**, the same area as the defect found in §6, and
this round wrote render records. So it was checked properly rather than blamed away:

1. The test builds its own store and clip in a temp dir. **No shared state**, so the render
   records could not have polluted it.
2. `tests/test_clip_pipeline.py` ran **green at 21:28**, immediately after this round's edit
   and after MEMEBOT-038's `song_library.py` write at 21:12. The regression arrived after.
3. **Decisive:** the exact failing test was re-run with `dict_of` monkeypatched back to the
   pre-MEMEBOT-042 five-field version. **It still fails.**

```
WITH PRE-MEMEBOT-042 dict_of -> failures=1 errors=0
=> the failure is INDEPENDENT of MEMEBOT-042
```

This round's own suites are green: `tests/test_matcher_boundary.py` 7/7, and `dict_of` returns
all ten keys. Reported as 94/97 rather than "green", because a suite that is red for someone
else's reason is still red, and rounding it up is how a real break gets missed.

### Concurrency

The brief said `clip_pipeline.py` was free. It was — BL-882 released it — and **MEMEBOT-038 claimed it ~10 minutes later**, mid-render of six videos through this same pipeline. Changing the matcher's input underneath it would have moved the measurements it was producing. This round **waited 43 minutes** rather than pre-empt, and used the time for the verification, the prediction and the baseline measurement, all read-only. MEMEBOT-038 released at 21:25:27; the patch landed at 21:29 and the file was free again at 21:31.

Worth noting: **MEMEBOT-038 never wrote `clip_pipeline.py` at all** — its changes went to `song_library.py` and a new `clip_cuts.py`. The claim was precautionary. That is the system working as designed and also the cost of it: 43 minutes of queue for a file that was not modified.

---

## What to do next

1. **Fix the LRU branch** — `clip_pipeline.py:1148`, add `confidence` and `needs_review` to the `SONG_LRU` dict. Tenth instance; one dict literal.
2. **Put audio in the song store.** 245 matched clips have nowhere to route until then.
3. **Re-measure after both.** Pipeline coverage is now 12.2%; the ceiling is whatever the vision labelling reaches, and the labelling passes are still running.
