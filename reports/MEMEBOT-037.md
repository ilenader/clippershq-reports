# MEMEBOT-037: all 21 hook windows are there, all real, all valid — and now committed. Renderable is still **0**, because the four songs are still `enabled: false`

**Date:** 2026-08-01 · **Type:** Read-only verification (+ one commit of the operator's own work) · **Spend:** **$0.00 · 0 paid calls**
No window was changed. `scratch/songs.json` was committed exactly as marked, staged by explicit path, diff scanned for credentials first. Committed at `57be1e4`.

Verifies the hook-marking session against [BL-879](BL-879.md).

**In-flight claims at the start of this round** (`python tools/claim.py brief`):

```
IN-FLIGHT CLAIMS  (paste into a brief)  2026-08-01 20:35
  BL-849           320 min  clippershq/clip_library.py, clip_library/, scratch/bl849_label.py   ** nothing written yet
  BL-867            67 min  clip_library/, scratch/, clippershq/clip_library.py
  MEMEBOT-036       21 min  memebot/scraper/duration.py, memebot/scraper/edit.py, memebot/scraper/config.yaml +4 more
  (** = the claim is older than any work under it. Ask the owner; nothing expires automatically.)
```

`scratch/songs.json` is held by nobody. BL-867 holds `scratch/` broadly; this round wrote only `songs.json` and only by committing what was already on disk.

---

## 1. Every song, every window

**Nothing was lost. 21 windows, exactly the expected 5 / 6 / 5 / 5.** Every one is hand-marked (`marked_by: hand`, `marked_with: hookmark`), timestamped between **20:07:44 and 20:32:35**.

### SONG 1 — `song01.mp3` · mood **melancholy** · genre *(empty)* · **enabled: false** · 162.54 s
*Sad, breakup. Not sad in general — the subject is a relationship ending.*

| hook | start | end | duration | note |
|---|---:|---:|---:|---|
| h4 | 13.572 | 28.392 | 14.820 | small beat drop kinda slow still |
| h1 | 0.427 | 18.701 | 18.274 | slow build works on anything |
| h2 | 49.264 | 65.401 | 16.137 | kinda good beat drop |
| h3 | 30.456 | 44.883 | 14.427 | a bit beat drop |
| h5 | 116.695 | 143.625 | 26.930 | the best beat drop |

### SONG 2 — `song02.mp3` · mood **triumphant** · genre *(empty)* · **enabled: false** · 94.29 s
*Female rap, empowerment anthem. NOT romance, NOT sad.*

| hook | start | end | duration | note |
|---|---:|---:|---:|---|
| h2 | 0.360 | 9.981 | 9.621 | a bit beat drop |
| h1 | 9.857 | 19.466 | 9.609 | just singing no beat drop |
| h3 | 19.404 | 28.641 | 9.237 | no beat drop but this is the main part of the song refrain |
| h4 | 37.556 | 47.363 | 9.807 | a bit of a bit drop at the start just a litl bass |
| h5 | 47.115 | 65.341 | 18.226 | just Rapping bars hard |
| h6 | 65.527 | 84.001 | 18.474 | this is acculy the main part of the song the refrain this is it |

### SONG 3 — `song03.mp3` · mood **warm** · genre *(empty)* · **enabled: false** · 195.19 s
*Summer, good vibes, going out, football. NOT old money.*

| hook | start | end | duration | note |
|---|---:|---:|---:|---|
| h1 | 7.828 | 22.714 | 14.886 | this is just a warm up just music a bit going lounder and lounder like a pregame |
| h2 | 43.118 | 58.389 | 15.271 | one of the beat drops nice and cool |
| h3 | 60.186 | 78.152 | 17.966 | at first is just the beat and then the singer starts singing |
| h4 | 79.998 | 103.817 | 23.819 | a bit of singing but a chill part with a drop down in the middle |
| h5 | 140.263 | 159.640 | 19.377 | again the good beat drop |

### SONG 4 — `song04.mp3` · mood **hype** · genre *(empty)* · **enabled: false** · 121.06 s
*Fast, aggressive, fighting. The drop must land where the action starts.*

| hook | start | end | duration | note |
|---|---:|---:|---:|---|
| h1 | 13.769 | 29.369 | 15.600 | this one is just the warm up start of the song started singing no beat drop only when he started singing a litl some some |
| h2 | 29.130 | 53.405 | 24.275 | this is the beat drop at the begining and after its good |
| h3 | 46.640 | 67.015 | 20.375 | this is a like a line when he says puta pata body its like a good beat drop around 4th to 5th sec |
| h4 | 66.696 | 83.490 | 16.794 | second sec is the beat drop him singing for the rest of the clip |
| h5 | 99.567 | 117.236 | 17.669 | this is the good part and down drop and ending so use it wisly |

`artist` is empty on all four and `genre` is empty on all four — unchanged, and neither is read by `match()` or `pick()`.

---

## 2. Placeholders: all gone. Songs: all still disabled.

| BL-879 found | now |
|---|---|
| 8 windows, every one `"PLACEHOLDER - mark by ear"` | **0 placeholders.** 21 real windows, all `marked_by: hand` |
| all four songs `enabled: false` | **all four songs still `enabled: false`** |

**The window half of BL-879's finding is fixed. The flag half is not.** The `_readme` in the file still instructs "mark the windows, then flip the flag — one word each"; the marking is done and the flag has not been flipped.

That readme is now **stale in three places** — it still says "Every start_s/end_s below is a PLACEHOLDER" and "ALL FOUR SONGS ARE enabled:false ON PURPOSE". The first sentence is no longer true. I did not edit it: you said do not change any window, and rewriting the file's own instructions during a verification round is not verification.

---

## 3. Window validation — 21 of 21 pass

Checked against the real audio, not the declared numbers:

| check | result |
|---|---|
| audio file exists | **4 / 4** |
| declared `duration_s` vs `ffprobe` | **exact match on all four** (162.54 / 94.29 / 195.19 / 121.06) |
| `start_s < end_s` | **21 / 21** |
| window inside the track | **21 / 21** — the latest end is 159.640 s in a 195.19 s track |
| suspiciously short (< 3 s) | **none** — shortest is 9.237 s |
| suspiciously long (> 30 s) | **none** — longest is 26.930 s |

Durations run **9.237 s – 26.930 s**, median ≈ 16.8 s. Song 2's are the tightest (9.2–18.5 s), which matches it being the shortest track.

**Windows overlap, and that is not an error.** Song 1's h1 (0.427–18.701) and h4 (13.572–28.392) share five seconds; song 4's h2/h3/h4 form a near-continuous chain. `hooks[]` is a list of alternative windows for rotation, not a partition of the track, so overlap is legitimate. Flagging it only so nobody later reads it as corruption.

---

## 4. `song_library.validate()` — 4 problems, all the same problem

```
vision_rules[0]: mood 'melancholy'  has no ENABLED song — clips matching this rule park
vision_rules[1]: mood 'triumphant'  has no ENABLED song — clips matching this rule park
vision_rules[2]: mood 'warm'        has no ENABLED song — clips matching this rule park
vision_rules[3]: mood 'hype'        has no ENABLED song — clips matching this rule park
```

**Not one complaint about a window.** Every problem is the `enabled: false` flag. Structurally the marking session is clean.

---

## 5. Renderable clips: **0** — and **230** the moment the flags flip

Measured over the live library through `read_snapshot`, de-duplicated last-wins by `(clip_id, rev)`:

| | clips |
|---|---:|
| distinct clips in the library | **2,003** |
| matched a mood | **230** — vision rule 217, franchise 13 |
| parked (no rule matched, no house set) | 1,773 |
| **RENDERABLE NOW** | **0** |
| renderable if the four songs were `enabled: true` | **230** |

`_candidates()` skips any song with `enabled: false`, so `pick()` returns `(None, None)` for all 230 matched clips and every one of them parks.

**230, not BL-879's projected 210.** The projection was made against a smaller labelled set; the library and its vision labels have grown since.

By mood, and this is worth seeing:

| mood | song | matched clips |
|---|---|---:|
| hype | song04 | **203** |
| warm | song03 | 24 |
| melancholy | song01 | 3 |
| triumphant | **song02** | **0** |

**Song 2 has the most windows (6) and matches nothing.** Its six windows are the largest single block of the evening's work and no clip in the library routes to `triumphant`. Separately, `song02.measured.can_sit_under_dialogue` is **false** (LRA 3.0 LU — a wall of sound), so even a future match would be filtered out on any dialogue clip.

---

## 6. The file is safe — it was not, forty minutes ago

| question | answer |
|---|---|
| gitignored? | **No.** Tracked since `19a1971` |
| committed? | **It is now** — `57be1e4`. Before this round it was **modified and uncommitted**: 178 added lines, 88 removed, living only in the working tree |
| in the backup list? | **No.** `BACKUP_THESE_6_FILES.md` has 8 entries and `scratch/songs.json` is not one of them |

**The exposure was real and it was open for the whole session.** The windows had existed on one disk, in one uncommitted file, since 20:07. The commit closes it.

Diff scanned before staging — **0** config string leaves, **0** credential-named fields, **0** email addresses, **0** opaque literals ≥32 chars. The diff is 21 hook objects in and 8 placeholder objects out; `enabled`, `path`, and the song-level `measured` blocks are untouched, which I verified key-by-key rather than by eye.

**Still not in the backup list.** BL-888 added `clip_library/` and `memebot/runs.jsonl` as entries 7 and 8 on the reasoning that they are what the video half cannot be rebuilt without. `scratch/songs.json` is now in git, so it is not in the same class — but git is on the same disk, and the file is the only record of half an hour of listening. I did not edit `BACKUP_THESE_6_FILES.md`; this round was read-only apart from the commit you authorised.

---

## Off-brief: the 21 windows have no loudness measurement

The 8 placeholders that were replaced each carried a per-hook `measured` block — `integrated_lufs`, `gain_db`, `resulting_lufs`, `window_is_placeholder`. **None of the 21 new windows has one**, and the loudness cache confirms it:

```
scratch/song_loudness.json — 13 entries
the 21 marked windows: 0 cached, 21 NOT measured
```

The 13 cached rows are keyed to the **old** placeholder spans and are now orphans.

**This is not a loss and it is not urgent.** `song_loudness.measurement_for()` keys its cache on `path@start-end` precisely because "the same file gives different loudness over different spans (song01: −9.5 LUFS whole, −17.2 LUFS over its first 20 s)", and it measures on demand. The first render of each window pays one local ffmpeg pass — **$0, no API**.

It matters for one reason: MEMEBOT-025 established that a gain computed on the whole file and applied to a window is the wrong-reference bug, 8.3 LU apart in the case it measured. **The whole-file `gain_db_whole_file` in each song's `measured` block is the wrong number for every one of these 21 windows** and must not be used as a shortcut for them. Nothing currently reads it that way — I grepped, and no code reads a per-hook `measured` block at all — but the number is sitting right there in the file next to windows it does not describe.

---

## Honest limits

- **I did not listen to a single window.** Everything above is arithmetic, file checks and `ffprobe`. Whether h5 really is "the best beat drop" is not something this round can verify, and no automated check ever will — that is why the marking was done by ear.
- **The mood→song assignments are unverified.** `song01 = melancholy`, `song02 = triumphant`, `song03 = warm`, `song04 = hype` are taken from the file as written. The file's own `_readme` warns that the song01..song04 → SONG 1..4 mapping is an assumption from filename order, and only song02 has an ID3 tag at all ("Untitled Project"). If that mapping is wrong, all four moods are on the wrong tracks and every number in §5 is attached to the wrong song.
- **230 is a match count, not a render count.** It says `pick()` would return a song and a hook. It does not account for the dialogue-class filter, which would remove `song02` candidates on dialogue clips — currently moot, since song02 matches nothing.
- **The library moved while I measured it.** BL-849 and BL-867 both hold `clip_library/`. Every read went through `read_snapshot` so the numerator and denominator agree with each other, but 2,003 is a figure from 20:4x and will not be the figure tomorrow.
- **`validate()` was run on the store as loaded**, not on a store with the flags flipped. The 230 figure comes from a deep copy with `enabled: true`, in memory only — `scratch/songs.json` on disk still has all four `false`, exactly as you left it.

---

https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/MEMEBOT-037.md
