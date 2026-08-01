# MEMEBOT-040 — 21 of 21 windows verified, then enabled. Not one window touched.

**Date:** 2026-08-01 · **Type:** Verify-then-enable · **Spend:** **$0.0000 · 0 paid calls**
Backup `backups/songs_20260801_204117.json` taken before anything was read twice · claim filed
with three repeated `--write` flags, each verified individually

**The verification passed on every count, so the songs are enabled. `validate()` is clean and
234 of 2,003 clips are renderable — +24 on BL-879's projection of 210.**

---

## `python tools/claim.py brief`, as run at the start

```
IN-FLIGHT CLAIMS  (paste into a brief)  2026-08-01 20:40
  BL-849           324 min  clippershq/clip_library.py, clip_library/, scratch/bl849_label.py   ** nothing written yet
  BL-867            72 min  clip_library/, scratch/, clippershq/clip_library.py
  MEMEBOT-036       26 min  memebot/scraper/duration.py, memebot/scraper/edit.py, memebot/scraper/config.yaml +4 more
  MEMEBOT-038        4 min  clippershq/clip_cuts.py, clippershq/song_library.py, clippershq/clip_pipeline.py +6 more
  MEMEBOT-039        1 min  scratch/memebot039_fields.py, scratch/memebot039_guard.py, scratch/memebot039_measure.py +2 more
  (** = the claim is older than any work under it. Ask the owner; nothing expires automatically.)
```

**MEMEBOT-038 was the one to check.** It holds `song_library.py` and `clip_pipeline.py` and its
intent says it renders six videos through this matcher — enabling songs changes what `pick()`
can return, so I checked before flipping anything. **Its pid 16640 is dead**: the claim is
stale and no live render was disturbed. BL-867 holds `scratch/` broadly; my files are uniquely
prefixed.

## The full window table

| song | file | dur | mood | genre | enabled (before) | windows |
|---|---|---:|---|---|---|---:|
| 1 | `memebot/scratch/song01.mp3` | 162.54 s | melancholy | *(empty)* | false | **5** |
| 2 | `memebot/scratch/song02.mp3` | 94.29 s | triumphant | *(empty)* | false | **6** |
| 3 | `memebot/scratch/song03.mp3` | 195.19 s | warm | *(empty)* | false | **5** |
| 4 | `memebot/scratch/song04.mp3` | 121.06 s | hype | *(empty)* | false | **5** |

Every window verbatim — `note` is the operator's own text, quoted exactly:

| song | # | start | end | duration | note |
|---|---|---:|---:|---:|---|
| 1 | 1 | 13.572 | 28.392 | 14.820 | "small beat drop kinda slow still" |
| 1 | 2 | 0.427 | 18.701 | 18.274 | "slow build works on anything" |
| 1 | 3 | 49.264 | 65.401 | 16.137 | |
| 1 | 4 | 30.456 | 44.883 | 14.427 | |
| 1 | 5 | 116.695 | 143.625 | 26.930 | |
| 2 | 1 | 0.360 | 9.981 | 9.621 | "a bit beat drop" |
| 2 | 2 | 9.857 | 19.466 | 9.609 | " just singing no beat drop " |
| 2 | 3 | 19.404 | 28.641 | 9.237 | |
| 2 | 4 | 37.556 | 47.363 | 9.807 | |
| 2 | 5 | 47.115 | 65.341 | 18.226 | |
| 2 | 6 | 65.527 | 84.001 | 18.474 | |
| 3 | 1 | 7.828 | 22.714 | 14.886 | "this is just a warm up just music a bit going lounder and lounder like a pregame" |
| 3 | 2 | 43.118 | 58.389 | 15.271 | "one of the beat drops nice and cool" |
| 3 | 3 | 60.186 | 78.152 | 17.966 | |
| 3 | 4 | 79.998 | 103.817 | 23.819 | |
| 3 | 5 | 140.263 | 159.640 | 19.377 | |
| 4 | 1 | 13.769 | 29.369 | 15.600 | "this one is just the warm up start of the song started singing no beat drop only when he started singing a litl some some" |
| 4 | 2 | 29.130 | 53.405 | 24.275 | "this is the beat drop at the begining and after its good" |
| 4 | 3 | 46.640 | 67.015 | 20.375 | |
| 4 | 4 | 66.696 | 83.490 | 16.794 | |
| 4 | 5 | 99.567 | 117.236 | 17.669 | |

Every one also carries `hook_id`, `uses: 0`, `marked_by: "hand"`, `marked_with: "hookmark"` and
a `marked_at` between **20:07:44 and 20:29:xx today** — the half hour, timestamped.

## Reconciliation against 21

| song | marked | expected | |
|---|---:|---:|---|
| 1 | 5 | 5 | OK |
| 2 | 6 | 6 | OK |
| 3 | 5 | 5 | OK |
| 4 | 5 | 5 | OK |
| **total** | **21** | **21** | **COMPLETE** |

Not just the total — the *shape* matches, including the 6 on song 2, whose `_note` says it "has
two or three separate drops and needs multiple hook windows". BL-888's 11-of-11 an hour ago was
a correct reading of a file still being edited.

## Is every window real?

**Yes, on every check asked for.** All 21 numeric; `start_s < end_s` throughout; none negative;
every `end_s` inside its track's ffprobe-measured duration (the deepest is song 3 window 5 at
159.640 s against 195.19 s); all four audio files present on disk.

### Two false alarms my own first pass raised, corrected rather than acted on

1. **"21 windows have an empty name."** My check read `name`. Hookmark writes **`note`**, and
   every window has the operator's words in it. Checking a field the tool does not write is my
   error, not his.
2. **"the file contains PLACEHOLDER."** Literally true, and misleading. It appears only in
   `_readme` and in each song's `_note` — prose from when the file was seeded, saying *"windows
   below are PLACEHOLDERS ... enabled:false until they are marked by ear."* **No window object
   contains it.** Those sentences are now **stale** and contradict the data beneath them. A
   file-wide token scan cannot tell a stale instruction from a live placeholder value, so the
   check now runs over the window objects only.

*Left alone, as instructed:* the five stale `_note`/`_readme` sentences still describe a
pre-marking state that no longer exists. That is a documentation defect, not a data one, and
correcting prose was not this round's job.

## `song_library.validate()`

**Before:** four warnings, every one of the form
`vision_rules[N]: mood 'X' has no ENABLED song — clips matching this rule park`.

That is not a defect in the marking — it is `validate()` reporting the disabled state. I
confirmed that by simulating the enable **in memory, writing nothing**:

```
BEFORE (as on disk):  4 warnings, all "has no ENABLED song"
AFTER  (simulated)  :  CLEAN — no warnings
```

The warnings *were* the thing enabling fixes. **After the write, `validate()` is clean.**

## The enable

Every gate passed, so the flags were flipped — **surgically**. A regex on `"enabled": false`,
not a `json.dump` round-trip, which would have reformatted the entire document. Half an hour of
hand-marked windows is not something to hand to a pretty-printer.

```
occurrences of enabled:false : 4
bytes 24282 -> 24278   delta 4 (one character per flag)
sha256[:16] 5837ed1eaea570eb -> 37bd2582d71f7c4a
windows touched: 0
```

Asserted **before** the write: no song field other than `enabled` changed; `hooks` identical
per song; nothing outside `songs` changed; byte delta exactly one per flag.

## What became renderable

| | |
|---|---|
| clips in library | 2,003 |
| **renderable now** | **234 (11.68%)** |
| BL-879 projected | 210 |
| **delta** | **+24** |

By mood: **hype 206 · warm 25 · melancholy 3 · triumphant 0.**

**Song 2 is enabled, correctly marked with six windows, and matches nothing** — consistent with
what MEMEBOT-019 already found. Three of the four songs are carrying the whole library, and
hype alone is 88% of it.

## Commit and the backup list

Committed by explicit path. **Credential scan on the diff: 8 changed lines, all four flag
flips, 0 matches** against Google/Gemini `AIza`, OpenAI `sk-`, generic key/secret/token,
bearer, long hex and long base64 patterns.

**The exposure item 7 names was already closed, and not by me.** `git diff` on `songs.json` was
**empty** when I started: **MEMEBOT-037 (`57be1e4`) had already committed the 21 windows**, and
`git branch -r --contains` confirms that commit is on **`origin/main`** — so the ear-work is on
other hardware, not one disk. The working tree differed from HEAD only by CRLF line endings
(24,282 vs 23,545 bytes = 737 newlines), and I did not manufacture a line-ending commit.

**On the backup list: `songs.json` is deliberately not one of the eight, and the document says
why.** `BACKUP_THESE_6_FILES.md` (which now lists eight; the filename is a historical address)
addresses it explicitly in its excluded section:

> **`scratch/songs.json`** — the song store, and genuinely irreplaceable (the hook windows are
> marked by ear and cannot be recomputed). It is **tracked in git**, so a push protects it.
> That is the only reason it is not on the list above; if it is ever gitignored it belongs
> there immediately.

The list's own criterion is "irreplaceable **and not in git**". `songs.json` is tracked, not
ignored, and pushed. So this is a considered exclusion with a stated trigger, not an omission —
and I have left the document alone.

---

## Verification

| check | result |
|---|---|
| brief run and reported | yes, 5 claims in flight |
| backup taken before touching | `backups/songs_20260801_204117.json`, byte-identical |
| full window table | 21 rows, verbatim, above |
| count reconciled | **21/21**, per song 5/6/5/5 — exact |
| placeholder text in any window | **none** (only in stale `_readme`/`_note` prose) |
| start < end, inside track, files present | **all 21 pass** |
| `validate()` after enabling | **CLEAN** |
| enable applied | yes — 4 bytes, **0 windows touched** |
| renderable clips | **234** of 2,003 (+24 vs projection) |
| committed by explicit path | `e890002`, credential scan 0 matches |

## Honest limits

- **I did not verify the windows are musically *right*.** I verified they are present, real,
  ordered, inside their tracks and hand-marked. Whether window 3 of song 1 is actually the
  beat drop is an ear judgement and only the operator can make it.
- **Two of my own checks were wrong before they were right** — the `name`/`note` field and the
  file-wide placeholder scan. Both would have blocked a correct enable had I acted on the first
  reading, which is the argument for verifying the verifier.
- **`genre` is empty on all four songs.** Not in the checklist and not touched, but
  `genre_mood_map` is empty too, so nothing routes by genre today.
- **234 is measured against a library that four rounds are appending to.** It was read from one
  frozen copy, so the ratio is internally consistent, but it will drift.
- **`triumphant` has an enabled song and zero clips.** Enabling did not fix song 2's reach, and
  nothing in this round tried to.
- **MEMEBOT-038's claim is stale, not released.** Its pid is dead but the claim file remains; I
  proceeded on the liveness check rather than asking, and its owner may still return to it.
