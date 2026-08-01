# MEMEBOT-053: there was no collision — my seven reports were simply in the wrong directory

**Date:** 2026-08-01 · **Class:** Repair + verification · **Spend:** **$0.00**, no paid calls.
**Claim:** `MEMEBOT-053`, four repeated `--write` flags, *"4 path(s) registered individually"*.
Two advisories, both proceeded on: BL-895 claims `scratch/` broadly (my paths are `scratch/mb053_*`), and **MEMEBOT-051 intends to write `memebot/meme/tests/test_band.py`** — I only perform git *index* operations on that file, which do not alter bytes, and I verified the result by blob afterwards.
**`claims_read.py` (run first):** 13 live claims — BL-849 (429 min), MEMEBOT-039, BL-895, BL-899, BL-900, MEMEBOT-049, MEMEBOT-051, MEMEBOT-052, MEMEBOT-050, BL-913, BL-917, BL-918, BL-914. **MEMEBOT-046 has released.**

---

## 1. The collision did not happen. Something quieter did.

The brief assumed two rounds overwrote each other at `MEMEBOT-046.md`. **They did not.** The two documents were written to two different paths and have different blob SHAs:

```
MEMEBOT-046.md           blob 385abade…   <- mine (repo ROOT)
reports/MEMEBOT-046.md   blob 3d448032…   <- the bed-level round
```

(Short-form blob ids: the secret scanner correctly refuses a 40-character hex string in a
public report, and it is right to — a full SHA is indistinguishable from a token by shape.)

**The real defect is that mine was at the root at all.** The README is explicit — *"reports live at `reports/<TICKET>.md`"* — and origin carries **468 reports under `reports/`** against 15 stray entries at the root. Checking all seven reports I have published this session:

| report | at root | in `reports/` | in `MANIFEST.tsv` |
|---|---|---|---|
| INFRA-007, MEMEBOT-016, -026, -029, -034, -041 | yes | **no** | **no** |
| MEMEBOT-046 | yes | *taken by another round* | **no** |

**Seven reports, none indexed.** `MANIFEST.tsv` has 270 rows and lists none of them. They were published and citable by raw URL, but invisible to anything that reads the manifest or walks `reports/` — which is what "published" means in this repository. A report nobody can find is the same failure as a report that was overwritten; it just leaves no evidence.

### What I did

`CONVENTION.md` already prescribes the answer and I followed it rather than inventing one:

> **The established fix is to suffix the filename, not to renumber someone else's ticket.**

The bed-level round claimed `MEMEBOT-046` first (21:27), so the number is theirs. My harness report is now **`reports/MEMEBOT-046H.md`**, and the other six moved to their canonical `reports/` paths. All seven went through `tools/publish_report.py`, which ran the secret scanner on each.

**Verified on `origin/main` by blob, not by push output** — the repo has silently lost a report three times, so a successful push proves nothing:

```
reports/INFRA-007.md      YES  14411      reports/MEMEBOT-034.md    YES   7903
reports/MEMEBOT-016.md    YES  12499      reports/MEMEBOT-041.md    YES   9756
reports/MEMEBOT-026.md    YES   8411      reports/MEMEBOT-046H.md   YES   9876
reports/MEMEBOT-029.md    YES  10866
7 of 7 verified byte-identical on origin/main

reports/MEMEBOT-046.md  10951 bytes
first line: # MEMEBOT-046: the bed now refuses instead of shipping silence …
-> PRESERVED
```

**Both documents survive at distinct IDs.** The root copies are left in place so every raw URL already handed out keeps working; they are now duplicates of the canonical copies and are the owner's to delete.

**The secret scanner blocked four of the seven on first attempt** — every hit a false positive: long test-function names, `force_original_aspect_ratio=decrease`, and a clip id in a path, all ≥32 characters and therefore "opaque literals". I reworded them rather than bypassing the scanner; it guards a public repo and a false positive is a cheap price. One of my own replacement strings was itself 34 characters and had to be shortened again.

## 2. The test files are safe — and MEMEBOT-029 is reproducible after all

`memebot/` is gitignored in the parent, which is what made MEMEBOT-046H write *"every test file I have written across four rounds exists on one disk with no history"*. **That was wrong.** memebot has its **own repository and remote** (`github.com/ilenader/memebot`), and all ten files are already committed and pushed:

```
local HEAD 95a75c4 | ahead of origin/main by 0, behind by 0
meme/tests/test_band.py … test_transforms, test_download, test_jobs, test_text,
test_render, test_ocr, meme/text.py, scraper/tests/test_caption_fit.py,
scraper/tests/test_edit_behaviour.py
ALL WATCHED FILES ARE BYTE-IDENTICAL ON origin/main.
```

**A methodology gotcha worth keeping:** my first pass reported **8 of 10 as DIFFERS** while `git status` was clean and HEAD equalled `origin/main`. The cause was my own check — git stores blobs LF-normalised, the Windows working files hold CRLF, and I compared raw bytes. "Verify by blob" only means something against the same normalisation git applies.

### Which measured states can actually be re-run

| round | state | recoverable? |
|---|---|---|
| **MEMEBOT-029** | `d384516^` — jobs 13, download 13, text 7, transforms 20, band 45 | **YES** — and those counts match its report exactly |
| MEMEBOT-034 | after its additions, before -041's | **NO** |
| MEMEBOT-041 | band at 60 tests | **NO** |

Two rounds' work landed in one 18-file commit (*"Commit the day's memebot work"*), and MEMEBOT-041's band work landed together with -046H's in `80af888`. A bundled commit destroys the intermediate state a measurement was taken against. **Commit per round, not per day.**

So MEMEBOT-046H's blanket "unverifiable" was too pessimistic: **MEMEBOT-029's measurement can be re-run by anyone.** MEMEBOT-034's and MEMEBOT-041's cannot.

## 3, 4, 5. Recorded in `docs/CORRECTIONS.md`

Four new sections, where the next reader will meet them:

- **The stale-`.pyc` cause**, with the mechanism in one sentence, the measured 1-of-6 → 0-of-6 proof, the two-line fix, and the hypotheses ruled out with evidence. Framed as **the fourth instance** of a measurement tool corrupting its own measurement, with the common shape named: *the instrument shares mutable state with the subject.*
- **MEMEBOT-041's transforms tests were not ineffective** — the harness hid two kills; the module scores 50.0% and its remaining survivors are all equivalent-or-default.
- **`y1 <= y0` → `<` is a true equivalent mutant**, not a fixture miss, because the following `while y < y1` runs zero times. With the rule: check observability *before* writing a test to kill a survivor.
- **The reproducibility table above**, plus the CRLF-vs-LF blob gotcha and "commit per round, not per day".

## Suite

**103 of 104 green.** The red is `tests/test_clip_library.py` — `test_index_is_the_dedup_key_and_is_rebuilt` (`AssertionError: 2 != 3`) and a rev-ordering test, in a clippershq module held by the live library rounds. It does not import memebot. My tracked changes this round are `docs/CORRECTIONS.md` and three `scratch/mb053_*` scripts.

Every memebot suite passes, including the ones this session built: `test_band.py` 61 checks, `test_caption_fit.py` 15, `test_edit_behaviour.py` 30, `test_duck.py` 63, `test_edit_bed.py` 11.

---

## Limits

I did not re-run MEMEBOT-029's measurement, only proved its state retrievable and its test counts identical to what it reported. Re-running it is a ~35-minute pass and the brief asked for an honest status, not a re-measure.

The root copies of all seven reports remain on origin. Deleting them would break raw URLs already handed to the user, so I left them; until someone removes them, each report exists twice and the copies can drift. Only the `reports/` copy is indexed.

`MANIFEST.tsv` is not updated by `publish_report.py` and I did not edit it by hand — whatever regenerates it will need to run before these seven appear there. I verified only that they are now in the directory the manifest is built from.

The blob verification is a point-in-time check. Ten rounds are live, one of them (MEMEBOT-051) holding a file I committed, so `test_band.py` on memebot's remote may already have moved past what I verified.
