# MEMEBOT-046: the bed now refuses instead of shipping silence — and item 3 was already fixed, so the "7.96 dB mis-levelled" claim I put in MEMEBOT-043 is wrong

**Date:** 2026-08-01 · **Type:** Fix + refutation · **Spend:** **$0.00 · 0 paid calls**
Claim filed via `tools/claim.py`, **6 paths registered individually** with repeated `--write`. `config.yaml`, `edit.py`, `song_loudness.py` backed up + SHA-verified to `backups/*.20260801_212809.pre_mb046.bak`. `git -C` throughout, no credential printed or committed. Committed at `ec6d482`. **Both files released** — see the end.

Acts on [MEMEBOT-045](MEMEBOT-045.md). **Corrects [MEMEBOT-043](MEMEBOT-043.md), which is my own report.**

`clippershq/clip_pipeline.py` and `tests/test_matcher_boundary.py` were **not touched**, as instructed.

---

## Item 3 first, because it is a refutation

You asked me to wire the stored per-window loudness because *"edit.py computes its bed level from the whole file"* and every hook render is *"mis-levelled by 7.96 dB, in the OPPOSITE DIRECTION."*

**That is not true, and the error originates in my own MEMEBOT-043.** edit.py has measured the bed over the window since MEMEBOT-023/030. `_bed_window_filter()` builds an `atrim` naming the exact slice and `_probe_source_loudness()` measures through it.

Measured on song04's h1 window — the same window MEMEBOT-043 rendered — in the unit edit.py actually uses:

```
  song04 whole file      : -10.30 dBFS
  song04 h1 WINDOW       : -14.80 dBFS        (13.769-29.369 s)
  difference             :  -4.50 dB

  gain to reach the target edit.py used (-18.4 dBFS):
    from whole-file basis :  -8.10 dB
    from WINDOW basis     :  -3.60 dB   <- and -3.6 dB is EXACTLY what it applied
```

The applied gain matches the window basis to the decimal. **The bed level is already window-derived; there was nothing to fix.**

### Where my error came from, precisely

MEMEBOT-043 said edit.py *"computes its own bed level and never reads `scratch/song_loudness.json`"*. The second half is true and the first half is empty — it computes the level **from its own window probe**, which is the correct reference. I let "does not read our cache" imply "uses the whole file", and the 9.47 dB / 7.96 dB figures — which are real, and are the spread between `gain_db_whole_file` in `songs.json` and my per-window measurements — got attached to a consumer that never reads `gain_db_whole_file` at all. **Nothing in the render path has ever used that field.**

### Why I did not wire the cache anyway

The two systems measure **different quantities for different purposes**:

| | `clippershq/song_loudness.py` | `edit.py` |
|---|---|---|
| unit | **LUFS-I** (`loudnorm`) | **mean dBFS** (`volumedetect`) |
| target | −14 LUFS, a platform normalisation | a level under the voice / a solo target in dBFS |

Substituting one for the other is precisely the units bug this file's own comments were written about — *"THE UNITS BUG, IN ONE PLACE SO IT CANNOT BE FIXED IN ONLY ONE OF THREE"*, measured at 15.6 dB on a real render. Wiring the stored LUFS gain into a dBFS level would have reintroduced it wearing the costume of a fix. **The remaining benefit is one redundant ffmpeg probe per render, not correctness.**

**What I did instead:** locked the behaviour so it cannot silently regress. `BedLevelIsMeasuredOverTheWindow` asserts the window reaches the measurement with its marked edges unrounded, and that a missing window yields no filter rather than an invented one.

---

## Item 2: the bed now refuses

Three defects, and the third makes the first two inert without it.

### 1. The repo root was never a search candidate

`ROOT` is `memebot/scraper`, so `ROOT.parent` is `memebot/`. A path written from the **repo** root — `memebot/scratch/song04.mp3`, which is exactly how `clippershq` stores song paths — resolved to `memebot/memebot/scratch/...` and missed.

`REPO_ROOT = ROOT.parent.parent` is now the first relative candidate in both `resolve_asset()` (the font path) and the new `_bed_search_paths()` (the bed path). **One list now does both the lookup and the diagnostic**, because a "searched:" list that differs from the search that failed is worse than none.

### 2. A named bed that is missing now raises

`ambient_bed.file` is a caller's *decision* — an integration that already chose the music. The old path printed one lower-case line among fifteen filter lines, returned the no-bed filters, and let the render succeed:

```
  ⚠  ambient_bed.file='memebot/scratch/song04.mp3' not found — skipping ambient
  RESULT edit: rendered=1 skipped=0 errors=0 status=ok          <- exit 0
```

Now it raises `AmbientBedMissing` and prints a banner naming every path searched. **The random-folder path is untouched**: an empty folder or an unreadable sample is a taste failure, not a decision, and still degrades quietly. There is a test for that distinction.

### 3. `edit.py` returned 0 even when everything failed

```python
print(f"RESULT edit: ... status={status}")
return 0                      # unconditional
```

`status` could read **`failed`**, every video could have errored, and the process still exited **0**. `clip_pipeline.render_one()` judges exactly one thing — `res["returncode"] == 0` — so every one of those was recorded as a successful render.

Without this, the refusal in (2) is inert: the per-video handler catches it into `counters["E"]` and the process exits 0 anyway. **The refusal and the exit code are one fix, not two.** Now `return 1 if errors else 0`.

---

## The two renders

**A — hand-marked window, absolute path:**

```
  ambient_bed  song04.mp3 @ -4.0dB [solo (class music-only, target -18.8dBFS)],
               start=13.8s [explicit-window] (always)
  returncode=0
  OUTPUT 10.22 s, 3,191 KB
  LEVEL  -19.20 dBFS mean / -16.91 LUFS-I     (source was -17.50 / -13.90)
  MUSIC PRESENT: True
```

`[explicit-window]` is the proof the marked edges drove it. The bed landed at −19.20 dBFS mean against a −18.8 dBFS target — 0.4 dB, which is measurement noise on a mean over a 10 s clip. Had the whole-file basis been used, the gain would have been −8.5 dB and the bed would have landed **≈4.5 dB too quiet**.

**B — deliberately missing bed, the exact repo-relative form that used to miss:**

```
  [banner rule]
    AMBIENT BED MISSING — REFUSING TO RENDER instagram/mb046b/C_p4DufCsq0
  [banner rule]
  ambient_bed.file='memebot/scratch/does_not_exist.mp3' was requested and does not
  exist. Refusing to render: a named track is a decision, and a silent video would
  look like a success. Searched: <5 paths> ...

  RESULT edit: rendered=0 skipped=0 errors=1 status=failed
  returncode=1        video produced: NONE
```

**Before this round that same config produced a healthy video, exit 0, and no music.**

---

## `memebot/` is not in git, at all

While checking my diff scope I found that **`.gitignore` line 137 ignores `memebot/` entirely** — `git ls-files memebot/` returns **zero** files. `edit.py`, `config.yaml`, `duck.py` and all six scraper test suites are untracked.

So **the fix in this report is not in the commit**, and cannot be: the commit carries only the scratch harness. The code change exists on one disk. `backups/` is ignored too (line 171), so the timestamped backup is on the same disk as the thing it protects.

`BACKUP_THESE_6_FILES.md` lists `memebot/runs.jsonl` as entry 8 — the render *ledger* — but not the render *code* that produces it. I did not change `.gitignore`: ignoring `memebot/` may be deliberate for `downloads/` and `clips/`, and that is a project-wide decision, not mine to take mid-round. **It is the largest exposure I found today and it needs an owner's call.**

---

## Proof

| claim | evidence |
|---|---|
| missing bed fails loudly | render B: banner, **returncode 1**, **no video**, `status=failed` |
| path resolves from the repo root | `_bed_search_paths()[0]` is `REPO_ROOT / path`; test asserts it |
| exit code no longer lies | `return 1 if errors else 0`; render B proves it end to end |
| per-window level | applied **−3.60 dB** = window basis exactly; whole-file would be −8.10 |
| item 3 refuted | measured, not argued — the two bases differ by 4.50 dB and edit.py used the window one |
| new guard | `memebot/scraper/tests/test_edit_bed.py` — **11 checks, green** |
| scraper suites | test_edit, test_edit_behaviour (30), test_duck, test_cli_help, test_caption_fit, test_duration — **all OK** |
| campaigns SHA | **8e02f8d6f6307ae8 — MATCH** |
| config | `config.json` valid; `config.yaml` valid YAML and **unmodified by me** |
| main suite | **96 of 98 green.** Reds are `test_clip_pipeline.py` and `test_claim.py`, in files held and being edited by **BL-899** and **BL-897**. My tracked diff is two scratch files |

---

## Honest limits

- **The headline of item 3 was my own error, and it was repeated back to me as a brief.** I wrote "computes its own bed level" in MEMEBOT-043 without checking what it computed it *from*. Anyone who acted on that sentence would have "fixed" a correct system and introduced a units bug doing it. The 9.47 dB spread is real; its consumer was not.
- **The window-level equivalence is shown on one window of one song.** −3.60 applied vs −3.60 predicted from the window basis is exact, and I did not repeat it across the other 20 windows.
- **Render A's 0.4 dB miss is unexplained.** −19.20 dBFS measured against a −18.8 dBFS target is within what a mean over 10 s of varying material will move, but I did not decompose it.
- **Nobody has listened to render A.** Music is present by the `ambient_bed` line and by a level that moved the right way; whether it *sounds* right is exactly the judgement these measurements cannot make.
- **`return 1 if errors else 0` changes edit.py's contract.** Six scraper suites and the main suite pass, and `clip_pipeline` already treats non-zero as failure — but any caller that was relying on "always 0" will now see failures it previously could not. That is the point, and it is still a behaviour change worth naming.
- **The refusal is scoped to a NAMED bed.** A run with `ambient_bed.enabled: true` and an empty folder still ships without music and exits 0. That is deliberate and tested, and it is also still a way to get a silent video — just not one where anybody named a track.
- **`clippershq/song_loudness.py` and `memebot/scraper/config.yaml` were claimed and never modified.** Item 3 needed no change in either, and I would rather report a claim I did not use than write something to justify it.

---

## Files released

`memebot/scraper/edit.py` · `memebot/scraper/config.yaml` · `clippershq/song_loudness.py` · `tests/test_song_loudness.py` · `memebot/scraper/tests/test_edit_bed.py` · `scratch/mb046_render.py`

The claim is ended; all six are free.

---

https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/MEMEBOT-046.md
