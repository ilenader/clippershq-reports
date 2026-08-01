# MEMEBOT-030 — `--audio-class` reaches the renderer. Without it a music-only clip **kept its original song**; with it, it mutes. The argv guard catches a planted drop three ways. And the solo track was **4.3 to 12.3 LU quieter than the audio it replaced**.

**Date:** 2026-08-01 · **Type:** Fix + measurement · **Spend:** **$0.00** of $0.05 (61 local clips, no paid calls)
**Changed:** `clippershq/clip_pipeline.py`, `memebot/scraper/edit.py`, `memebot/scraper/config.yaml`, `memebot/scraper/tests/test_duck.py`; **new** `tests/test_render_argv.py`.
**Backed up:** `config.json`, `spend.json` — timestamped, `scratch/mb030_backup/`.

---

## The claim, and the two rounds it collided with

The brief asked me to verify BL-855 had released `clip_pipeline.py`. **It has not** — it is
still in flight at 163 minutes and still claims that file. `memebot/scraper/edit.py` was
claimed by **MEMEBOT-027** two minutes before I filed.

I proceeded on both, under the protocol BL-855's own claim uses: they declared they touch
**only the `rank_score`/`rank_clips` scoring region**; I touched only `render_one()`'s argv
and its call site — disjoint functions — under a per-file hash guard, re-checked
immediately before writing (`c8782d23b05f957f`, unmoved for 75 minutes). `edit.py` had not
moved from `84f3b84db32db434` in the 9 minutes between my baseline and my edit, and
MEMEBOT-027 has since released. **Neither file was overwritten and nothing was lost.**

The `--write` paths registered individually, verified by hand as asked:

```
will_write is a list with 5 entries:
  1. 'clippershq/clip_pipeline.py'     4. 'memebot/scraper/config.yaml'
  2. 'tests/test_render_argv.py'       5. 'scratch/mb030_*'
  3. 'memebot/scraper/edit.py'
entries containing a comma: NONE
```

and the conflict check fired on **both** contended paths — which a comma-joined string
would have missed entirely. (BL-870 has since fixed `split_paths` so old broken claims are
matched too.)

---

## 1. The class reaches the renderer

```
A. WITHOUT a class  -- what every render did for three rounds
   argv: ... --override-text MEMEBOT-030 --force-rerender
   --audio-class present: False
   audio_treat  keep (no class available, conservative default)
   ambient_bed  song01.mp3 @ -9.3dB [relative (clip mean -18.7dB -6.5dB -> bed at -25.2dBFS)]
   WARNING RAISED: yes

B. WITH the class
   argv: ... --force-rerender --audio-class music-only
   --audio-class present: True
   audio_treat  mute (routed on class music-only)
   ambient_bed  song01.mp3 @ -3.3dB [solo (class music-only, target -19.2dBFS)]
   warning raised: no
```

**The clip is music-only. Without the class it kept its original audio; with the class it
mutes** — the only free way to actually remove the original song. Not a cosmetic
difference: the majority class is music-only (BL-853 ~51.9%, MEMEBOT-020 80.3% locally) and
every one of them was keeping its source track.

Note the bed line too. Without a class the level was computed in **relative** mode against
the clip mean — an offset under a voice that was being deleted. With the class it takes the
**solo** path, because `bed_plan()` decides level and treatment together.

**An unroutable class is withheld, not passed** — `argparse` would exit 2 and lose the
render entirely — but it prints why, because silently dropping it is the bug being fixed.
Verified: render still returns 0.

`speech_dbfs` is wired the same way and is **always None today** — nothing persists it on a
clip record, so dialogue clips fall back to the clip mean, which `duck.relative_basis`
warns under-places on a quiet-gapped clip. Wired now so whichever round starts storing it
needs no change here. Stated because it is a real remaining gap, not a finished item.

## 2. The argv guard, and it can fail

`tests/test_render_argv.py`. Not "does `--audio-class` appear" — that guards one field and
misses the eighth. The rule is structural:

> if clip_pipeline **computes** a value and edit.py **accepts** it, it must be **wired** —
> or listed in `NOT_WIRED` with a reason.

It parses edit.py's argparse **with `ast`** (a usage string is documentation and can lie),
diffs it against a registry, and requires every option to be one or the other. A new CLI
option on edit.py fails the suite until somebody decides about it. The decision may
legitimately be "not wired"; what it may not be is silence. Twelve options are currently
listed not-wired, each with a reason, and `--treatment` is the interesting one:

> DELIBERATE. The class is passed instead, so edit.py ROUTES rather than being told. A fixed
> word here would outrank the class and nothing would ever route — which is exactly what
> `ambient_bed.treatment: auto` exists to avoid.

**Three planted-drop tests prove the guard has teeth**, because a guard that cannot fail is
worse than none — it reads as coverage:

| planted defect | caught |
|---|---|
| `cmd += ["--audio-class", cls]` deleted from `render_one` | **yes** |
| `render_one` keeps the parameter but the **call site stops passing it** | **yes** |
| a **new option** appears in edit.py's parser | **yes** |

The second is the exact shape of the original bug: the function can support the argument
perfectly and the caller can still fail to supply it.

The guard also pins `RENDER_AUDIO_CLASSES` against edit.py's own `choices=[...]`, so the
list cannot drift into passing a value argparse rejects.

---

## 3 + 4. What level should a track that IS the soundtrack sit at?

Nobody had measured it. The anchor is not abstract: on a music-only clip the new track
**replaces** the source's own audio, so the question is whether the video is about as loud
as it was. Measured in dBFS (comparable with previous rounds) and **LUFS-I**, which is what
platforms normalise to and the closer of the two to what an ear does.

Source: `DUAaRozCWYc.mp4`, its own audio **−18.7 dBFS / −15.8 LUFS-I / −0.7 dBTP**.

| target dBFS | out LUFS-I | vs the source it replaced | true peak |
|---:|---:|---:|---:|
| −30.0 | −28.2 | −12.4 LU | −14.3 dBTP |
| −26.0 | −24.2 | −8.4 LU | −10.2 dBTP |
| −22.0 | −20.2 | −4.4 LU | −6.2 dBTP |
| **−18.0** | **−16.2** | **−0.4 LU** | **−2.2 dBTP** ← parity |
| −16.0 | −14.2 | +1.6 LU | **−0.2 dBTP** ← at the ceiling |
| −14.0 | −12.5 | +3.3 LU | **+1.8 dBTP** ← over full scale |

```
SHIPPED solo gain -14 dB (raw) -> -28.1 LUFS  (-12.3 LU vs source)
SHIPPED solo gain  -6 dB (raw) -> -20.1 LUFS   (-4.3 LU vs source)
```

**The shipped range delivered a soundtrack 4.3 to 12.3 LU quieter than the audio it
replaced, with 8 LU of spread from the random roll alone** — and it moved with whatever bed
file happened to be picked, because it was a gain, not a target.

**Recommendation, now shipped: `solo_volume_db_min/max = −20 / −18`, as TARGETS.** That
lands within ~2.5 LU of parity at every roll with at least 2.2 dB of true-peak headroom.

**The obvious answer is wrong and worth stating.** Platforms normalise to about −14 LUFS,
so −14 looks like the target — and it is **not reachable with this bed**: −16 dBFS already
true-peaks at −0.2 dBTP and −14 goes over full scale. **The peaks run out before the
loudness does**, so parity with the source is the honest ceiling, not the platform norm.

### The units bug lived in THREE places, not one

MEMEBOT-023 fixed the relative branch. There were two more solo branches — one reached by
class, one by a source having no audio stream, which is the path **every retrieved DASH
clip takes**. Fixing one would have left the others, so the logic is now a single helper,
`_bed_gain_for_target()`, used by all three, and a test asserts exactly four occurrences
(one definition, three call sites) so re-inlining any of them fails the suite.

Item 4's window probe moved into that helper too, so all three paths get it: `song01.mp3`
is **−12.6 dBFS overall and −15.9 dBFS over the ten seconds actually used**.

### A design error I made and caught by measuring

My first version applied the **−18 dBFS true-peak ceiling to the dialogue path as well**,
which silently clamped MEMEBOT-021's measured −8..−5 range:

```
bed at -16.6dBFS; bed target -16.6 dBFS is above the -18.0 dBFS true-peak ceiling, clamped
```

That ceiling was measured for a **solo** bed, where the bed *is* the output and nothing
bounds its peaks. On the **keep** path the bed is amix'd with the source and the sum goes
through MEMEBOT-023's limiter, so peaks are bounded downstream. The ceiling is now a
per-caller argument — **−18 for solo, −10 for keep** — with the reason in the docstring.
I would not have seen it without reading the render log.

---

## 5. Three renders, one per class

`scratch/mb030/renders/`, produced through the shipped `edit.py` with `--audio-class`.

| class | treatment | source LUFS-I | output LUFS-I | delta | true peak |
|---|---|---:|---:|---:|---:|
| music-only | **mute** | −15.8 | −18.1 | **−2.3 LU** | −3.5 dBTP |
| dialogue-over-music | **keep** | −14.0 | −12.4 | **+1.6 LU** | −0.7 dBTP |
| dialogue-only *(constructed)* | **keep** | −11.3 | −13.8 | **−2.5 LU** | −0.6 dBTP |

All three within ±2.5 LU of the source they replaced or kept, all peaks under full scale.

**The dialogue-only source is CONSTRUCTED and labelled as such everywhere** — the corpus
has none (MEMEBOT-020 measured 0 of 61). It is a real clip's video with its own speech
windows kept and digital silence between them, so the "bed between words" is genuinely
absent.

One number needs explaining rather than reporting flat: the constructed clip's source reads
**−11.3 LUFS-I** despite a −20.4 dBFS mean, because LUFS gating discards the silence and
measures only the speech. The output's −13.8 is the mix of that speech with a continuous
bed across the whole timeline. The −2.5 LU is a gating artefact of a constructed source,
not a level error.

---

## Verification

| check | result |
|---|---|
| `memebot/scraper/tests` | **92/92 OK** |
| `tests/run_all.py` | **84 of 86 suites** green in batch; the 2 red (`test_dashboard`, `test_song_library`) **PASS standalone** |
| `tests/test_render_argv.py` (new) | **7/7**, including 3 planted-drop tests |
| `--audio-class` in the argv | proved on a live render, both ways |
| unroutable class | withheld, loud, render still returns 0 |
| all three level paths share one helper | asserted (4 occurrences) |
| bed probed over its window | asserted functionally, not by grep |
| true-peak ceiling clamps and says so | asserted |
| **campaigns SHA** | **`8e02f8d6f6307ae8` — MATCH** |
| `config.json` | parses, 162 keys |
| backups | `config.json` + `spend.json`, timestamped |
| spend | **$0.00** of $0.05 |

`test_dashboard.py` and `test_song_library.py` are owned by INFRA-012 and MEMEBOT-029, both
live and both writing those files while the batch ran. Same class as the known
`test_filelock.py` flake. **I am reporting the batch number as the headline rather than the
standalone one**, because a green run I had to explain away is not a green run.

---

## Limits

- **One bed file and one source per class.** The solo sweep is `song01.mp3` over one
  music-only clip. The −18 dBFS ceiling is a true-peak result **for this bed**: a more
  compressed track has a smaller crest factor and could exceed 0 dBTP at the same target.
  A bed-aware ceiling would need the bed's own true peak, which is not measured here.
- **`speech_dbfs` is wired but always None.** Nothing persists it, so dialogue clips still
  place the track against the clip mean.
- **`dialogue-only` was tested on a constructed source.** Its routing and level are real;
  its material is not.
- **The argv guard reads source text, not behaviour.** It proves the flag is assembled and
  passed; the live render above is what proves it arrives.
- **`clip_pipeline.audio_treatment()` still returns `"duck-under"` on an unknown class**,
  which is stale since MEMEBOT-023 disabled duck. It is harmless — duck.py's gate converts
  it to `keep` loudly — and it is in BL-855's file, so I left it. Worth a line in whichever
  round next holds that file.
- **BL-855 is still live in `clip_pipeline.py`.** My edit is disjoint and hash-guarded, but
  it is not a merge — if they land a change to the same region, one of us loses.
- **No listening test.** Every number here is a measurement. The three renders exist so the
  operator can settle the parts a meter cannot.

---

## Method

Claimed with one `--write` per path and verified the stored list by hand; backed up
`config.json` and `spend.json` before touching anything. Both contended files were
hash-baselined and re-checked immediately before writing. The wiring change is three lines
in `render_one` plus one at the call site; everything else is the guard, the helper the
three level paths now share, and the measurement that set the solo target. Levels were read
with `volumedetect` and with `loudnorm`'s analysis pass, the second because dBFS mean is
not what an ear or a platform uses. No paid call, no key read, no spend.
