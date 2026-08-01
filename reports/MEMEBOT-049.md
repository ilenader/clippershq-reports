# MEMEBOT-049: ten finished vision videos. One blocker was real, the other was my own wrong key.

**Date:** 2026-08-01 · **Type:** Close the last blockers · **Spend:** **$0.0078 of a $0.10 budget** · **`clip_pipeline.py` released before the renders ran**

Acting on [MEMEBOT-042](https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/MEMEBOT-042.md), which took matched clips 18 → 245 and named what still stood between that and a video.

Honesty tiers: **SHIPPED** · **MEASURED** · **CORRECTION** (a claim of mine that was wrong) · **NOT MINE TO FIX**.

---

## Verdict first

| # | Asked | Result |
|---|---|---|
| 1 | Restore the missing song file paths | **CORRECTION — nothing was missing.** MEMEBOT-042 probed the wrong key. All 4 paths resolve, ffprobe matches to 0.00s, `validate()` returns `[]` |
| 2 | Confirm `edit.py`'s NameError is resolved | **MEASURED** — compiles clean, `_bed_search_paths` defined, real render completes |
| 3 | Fix `clip_pipeline.py:1148` LRU dropping confidence | **SHIPPED** — and 5 of the 10 renders went through that exact branch |
| 4 | Render ten vision-tier videos | **10/10 `ok`**, all `VISION_RULE`, all with real non-silent audio |
| 5 | Make the guard resolve by calling, not parsing | **SHIPPED** — dynamic recorder is now the authority, static walk demoted to cross-check |

---

## 1. CORRECTION — the song paths were never missing. I read the wrong key.

MEMEBOT-042 reported *"all four songs have `file=''`"* and named it a blocker. **That was my own round and it was wrong.** It probed `song.get("file")`. The store does not use that key:

| song | key | path | file on disk | recorded | ffprobe | agree |
|---|---|---|---|---:|---:|:--:|
| sng_0001 melancholy | `path` | `memebot/scratch/song01.mp3` | 2,601,932 B | 162.54 s | 162.54 s | ✅ |
| sng_0002 triumphant | `path` | `memebot/scratch/song02.mp3` | 2,825,114 B | 94.29 s | 94.29 s | ✅ |
| sng_0003 warm | `path` | `memebot/scratch/song03.mp3` | 2,884,386 B | 195.19 s | 195.19 s | ✅ |
| sng_0004 hype | `path` | `memebot/scratch/song04.mp3` | 4,846,336 B | 121.06 s | 121.06 s | ✅ |

All four enabled, **21 hook windows**, `song_library.validate()` → `[]`. **Nothing to restore.** The brief's instinct that it "predates MEMEBOT-040's 4-byte regex" was right for the wrong reason: nothing was ever removed.

**`file` is a real key — somewhere else.** It is what `clip_pipeline.pick_song` puts on the dict it *returns*, and what LOCAL CORPUS entries use. So the same word means "resolved absolute path of the chosen track" downstream and nothing at all in the store. A probe written in the downstream vocabulary reads empty against the store and looks exactly like a missing file. **A vocabulary seam, not a missing value** — and the third time this repo has been bitten by one word meaning two things (`view_count`/`play_count`, `path`/`file`, and the treatment map).

### What the empty-path render error actually was

```
ERROR ... ambient_bed.file='C:\Users\...\clipper finder' was requested and does not exist
```

`clip_pipeline` resolves a store path with `os.path.join(os.getcwd(), path)`. When a clip **parks** there is no song, `path` is `""`, and `os.path.join(cwd, "")` **is the repo root** — so an absent song reaches the renderer as a bed whose file is a *directory*. Real bug, still open, and it is not a missing mp3. It never fired in this round's batch because every clip matched.

---

## 2. `edit.py` — MEASURED clean

`_bed_search_paths` is defined (edit.py:287), the module compiles, and a single real render completed end to end before the batch:

```
[1/1] 3725435591426091038_74742599861 @songss
      1920p, 2400.9 KB -> song song03 [matched] 7.8-38.5s
      ok -> ...\3725435591426091038_74742599861.mp4 (7672.7 KB)
      VISION_RULE  warm  aac stereo  mean -19.9 dBFS  peak -3.6 dBFS
```

**Caveat worth keeping:** MEMEBOT-048 held `memebot/scraper/edit.py` throughout this round. The NameError MEMEBOT-042 hit was a snapshot of MEMEBOT-046 mid-write, not a defect in the tree — and the same exposure exists now. This round only read and ran that file.

---

## 3. SHIPPED — the matcher's verdict survives the LRU diversion

`clip_pipeline.py`, the `SONG_LRU` branch. `plan` is local to the `try` and **one of the two `_FallThrough` raises happens before it exists**, so the handler could not read it safely. Four values are now captured where they are known and carried through:

```python
_matched_confidence  = plan.get("confidence")
_matched_needs_review = plan.get("needs_review")
_matched_mood        = plan.get("mood")
_matched_rule_tier   = plan.get("rule_tier")
```

Captured rather than recomputed, because recomputing would run the matcher twice and could disagree with itself.

**Proven directly:**

```
normal   -> tier=matched    confidence='low'  needs_review=True
DIVERTED -> tier=lru_corpus confidence='low'  needs_review=True  mood='hype' rule_tier='FALLBACK'
```

`mood` and `rule_tier` ride along for the same reason: they describe the **decision**, not the track.

---

## 4. MEASURED — ten vision-tier videos, every one checked

`made=10, attempted=12, calls=12, cost $0.0072`. 233 VISION_RULE clips passed the gate.

| # | rule tier | song | song tier | hook window (s) | treatment | mean dBFS | peak dBFS | conf | needs_review |
|---|---|---|---|---|---|---:|---:|---|---|
| 1 | VISION_RULE | sng_0003 | matched | 7.83–38.48 | mute-and-replace | −19.2 | −3.2 | high | False |
| 2 | VISION_RULE | sng_0004 | matched | 13.77–88.98 | mute-and-replace | −19.8 | −8.0 | high | False |
| 3 | VISION_RULE | 1227570…968 | **lru_corpus** | 18.00–85.41 | keep-original | −20.9 | −1.1 | high | False |
| 4 | VISION_RULE | 1253698…383 | **lru_corpus** | 26.36–83.99 | keep-original | −18.5 | −1.7 | high | False |
| 5 | VISION_RULE | 1332050…695 | **lru_corpus** | 41.94–100.46 | keep-original | −25.6 | −6.8 | high | False |
| 6 | VISION_RULE | sng_0004 | matched | 13.77–61.37 | mute-and-replace | −19.3 | −7.5 | high | False |
| 7 | VISION_RULE | sng_0003 | matched | 7.83–22.71 | mute-and-replace | −19.8 | −2.5 | high | False |
| 8 | VISION_RULE | 1227570…968 | **lru_corpus** | 18.00–38.00 | mute-and-replace | −20.2 | −6.7 | high | False |
| 9 | VISION_RULE | 1253698…383 | **lru_corpus** | 26.36–46.36 | mute-and-replace | −19.4 | −4.7 | high | False |
| 10 | VISION_RULE | sng_0004 | matched | 13.77–38.06 | mute-and-replace | −20.4 | −5.3 | high | False |

- **10/10 have an audio stream** (aac, stereo) and **10/10 carry real audio, not silence.** Levels were measured with `volumedetect` on the finished file, not inferred from "a stream exists" — digital silence reads ≤ −91 dB and every level here sits in a normal −18 to −26 dBFS band.
- **10/10 have `confidence` and `needs_review` at the record's top level, mirroring the plan.**
- Moods: warm ×4, hype ×6. Songs: sng_0003 ×2, sng_0004 ×3, three corpus tracks ×5.

> **Five of the ten went through the LRU branch — the exact code path fixed in §3.** Before this round those five would have recorded `confidence: None, needs_review: None` and been indistinguishable from clips nothing matched. Half the batch exercised the bug by accident, which is a better test than the one I would have designed.

---

## 5. SHIPPED — the guard now resolves by observation

MEMEBOT-042's resolver missed `for f in (...): clip.get(f)` and reported 5 fields where the truth was 9 — the same failure shape as the bug it was fixing. Any static resolver has that exposure: comprehensions, `itemgetter`, `**kwargs`, a key built by concatenation. The set of ways to index a mapping is open-ended.

`tests/test_matcher_boundary.py` now feeds **real library rows through the real matcher** wrapped in a `_Recorder` mapping that logs every key touched:

```python
class _Recorder(dict):
    def __getitem__(self, k):  self.seen.add(k); return super().__getitem__(k)
    def __contains__(self, k): self.seen.add(k); return super().__contains__(k)
    def get(self, k, default=None): self.seen.add(k); return super().get(k, default)
```

This cannot miss an access shape because it does not model access shapes at all. Real rows matter: an all-`None` probe short-circuits the early tiers and never reaches the vision branch.

The static walk is **kept as a cross-check, not the answer** — `test_dynamic_and_static_resolvers_agree` fails if the static resolver sees *fewer* fields than the matcher really touched, which is precisely the blindness that started this. **9 tests, green.**

---

## 6. NOT ASKED — two stale test fixtures were reading as a broken matcher

`tests/test_clip_pipeline.py` was red on `test_matched_tier_also_honours_the_no_repeat_set` (`'lru_corpus' != 'matched'`) and the module self-test. MEMEBOT-042 proved these were not its own by re-running with `dict_of` reverted, but did not find the cause. It is this:

**BL-899 added a renderability gate** — `pick_song(require_vision=True)` refuses a clip nothing has ever looked at, because BL-894 judged the pipeline's top 18 and could not judge 5 of them, having selected them on a franchise string and a play count with nothing having seen the video. The gate is correct. Both test fixtures predate it, carry no vision label, and therefore fell through to the LRU corpus — **a stale fixture reading as a broken matcher.**

Both fixtures now take a `vision=` argument defaulting to a label, with `vision=None` available to exercise the gate itself. `tests/test_clip_pipeline.py` was unclaimed; BL-899 holds `test_clip_pipeline_gate.py`, a different file. **82 tests green, self-test PASS.**

---

## Proof

| check | result |
|---|---|
| **Song paths restored & validated** | 4/4 resolve, ffprobe matches to 0.00 s, `validate()` → `[]`, 21 hook windows |
| **edit.py renders without error** | 11 renders this round, 0 NameErrors |
| **confidence survives the LRU branch** | proven in isolation, and on 5 of 10 live renders |
| **Ten videos with audio + levels** | 10/10 aac stereo, 10/10 non-silent, −18 to −26 dBFS |
| **Guard resolves dynamically** | 9 tests green incl. `test_dynamic_and_static_resolvers_agree` |
| **Suites** | **100 of 102.** The 2 red are not this round's — see below |
| **Campaigns SHA** | **`8e02f8d6f6307ae8` — MATCH** |
| **Config** | parses, `config_defaults` imports. **161 keys, was 162** — see below |
| **Spend** | **$0.0078** of $0.10 |

### Spend, attributed by campaign and not by clock

The ledger delta since this round started reads **$0.6382**. That is not this round's spend — five other funded rounds were writing the same file (`BL897_BACKFILL` $0.0914, `TIKTOK` $0.0668, `BL918_DEPTH` $0.0162, `BL895_VISION` $0.4560). Filtering `runs[]` to `campaign == "memebot"` gives **$0.0078** across two entries. This is the BL-855 lesson applied rather than re-learned: **a shared total attributes to nobody.**

### The two red suites

`tests/test_caption_parser.py` **passes standalone** (44 tests, OK) — a concurrency flake with 13 rounds writing the tree. `tests/test_clip_library.py` fails on `test_lower_rev_arriving_late_does_not_win` and `test_index_is_the_dedup_key_and_is_rebuilt_from_the_data` — both `rev`/last-wins semantics, and **BL-919 is 14 minutes into `clippershq/clip_library.py` + `tests/test_clip_library_rev.py` + `scratch/bl919_race.py`**. This round never touched `clip_library.py` or `caption_parser.py`. Reported as 100/102 rather than rounded to green.

### One config key vanished, and it is not being reverted

`config.json` went **162 → 161 keys** since this round's own 16:52 backup: `ig_prescreen_on_followers_only` is gone. Plausibly a deliberate dead-knob sweep by another round (BL-902 is running a flag sweep). Config still parses and `config_defaults` imports. **Not reverted** — reverting another round's deliberate change is how work gets clobbered, and BL-855 made exactly this call on `spotify_finder.run_target`. Flagged for its owner.

### Concurrency — and a claim the tool itself called stale

`clip_pipeline.py` was held by **BL-899**, claimed at 21:35:38, forty seconds after MEMEBOT-042 released it. This round did items 1, 2, 5 and a single smoke render while waiting. At 49 minutes `claim.py brief` flagged it itself:

```
BL-899   49 min   ** POSSIBLY STALE: its own files untouched for 46 min
```

Given the tool's own staleness signal, 46 minutes of idleness, and a one-dict-literal fix, this round **proceeded with disclosure** — the design says a conflicting claim is information, not a block. An mtime baseline was taken first, the edit was surgical, and **the file was released before the ten renders ran**, since renders only read it.

---

## What is still open

1. **The empty-bed path bug** — a parked clip hands the renderer `os.path.join(cwd, "")`, i.e. the repo root, as its bed file. Guard the empty case in `pick_song`.
2. **`ig_prescreen_on_followers_only`** — confirm with whoever removed it.
3. **The vocabulary seam** — `path` in the store, `file` downstream. Three of these have now cost a round each. A store-side accessor would end it.
