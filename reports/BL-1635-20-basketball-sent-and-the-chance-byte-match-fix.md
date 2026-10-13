# BL-1635: 20 basketball edits sent to Drive, all 20 clean; the byte check no longer fails a file on a chance match

$0 vendor spend. 2 APP order `2026-10-13_2235_SEND-20-basketball`, 2026-10-13 22:35–23:25.

## Card

| # | Item | Result |
|---|---|---|
| 1 | **Send** | `tools\edits.py send --niche basketball --count 20` (best first) = send 3. **16 of 20** went up; **4 were held back** by the send's own check. Every pick was a library file on F:, none sent before (basketball: 62 approved, 0 sent). |
| 2 | **Why 4 were held back** | Each failed the byte search on **one** 4-letter word: `lavc` (2 files), `lavf`, `aigc`. All 4 matches sit **inside the compressed picture/sound data (mdat)**, in mixed case (`lUUU`, `UlUl`, `UlUU`), with 0–2 printable bytes around them. No software writes those. They were **chance**: a 4-letter word, any case, turns up about once per 27 MB of compressed data, so ~1 file in 5 failed for nothing. The real tags in the sources (`Lavf60…`, x264 settings, `vid:`, `aigc`) were all stripped. |
| 3 | **Fix** | `clippershq/edits_clean.py` `string_hits`: a forbidden word of **5 letters or fewer inside mdat** counts only when it sits in **text** (8+ printable bytes next to it), as every real one does (`Lavc60.31.102`, `vid:<id>`, `aigc_info`, x264's settings). **Unchanged:** any word outside mdat, every longer word (`tiktok`, `bytedance`, `capcut`...), and the video's own secrets (handle, id, name) count on every occurrence, anywhere. SEI, AAC filler, ffprobe and exiftool checks are untouched. |
| 4 | **Test + guard** | `tests/test_bl1635_chance_hits.py`, 6 tests: mixed-case short words in mdat binary are not hits; the same words in text are; anything outside mdat is; long words and secrets hit anywhere; **guard:** 500 chance matches planted in 8 MB of random mdat give ≤ 3 hits (the old rule: all 500); the thresholds cannot be loosened (`SHORT_WORD ≤ 5`, `TEXT_RUN ≥ 8`). `tests/test_bl1631_library_send.py`: 14 green. |
| 5 | **The 4, re-sent** | `scratch/bl_send20/top_up.py 3`: the 4 held-back files re-cleaned, verified with the fixed check, uploaded into **the same folder**, Drive size + sha256 checked, marked sent. The folder was renamed `(16)` → `(20)`; the folder ID (= the link) is **unchanged**. Send 3 is now `done`, 20 sent, 0 failed. |
| 6 | **Independent check, all 20** | `scratch/bl1631/verify_live_send.py 3`: all 20 downloaded back **from Drive** and re-checked: ffprobe + exiftool no tags beyond the mp4 basics, **0 SEI**, no handle / id / name / `tiktok` / Lavf / Lavc string, first and last second decode (plays), decoded frames + sound **bit-identical** to the library file, sha256 = what the send recorded. **20 of 20 pass.** |
| 7 | **The link** | Opened with no cookies and no Google login: HTTP 200, no sign-in redirect, names the folder, lists **20 of 20** files. |

## What a chance match looks like

| file | word | where | casing | printable bytes next to it |
|---|---|---|---|---|
| 2 | lavc | mdat | lUUU | 3 |
| 8 | lavf | mdat | UlUl | 0 |
| 12 | aigc | mdat | UlUU | 0 |
| 16 | lavc | mdat | lUUU | 0 |

(`scratch/bl_send20/probe_hits.py` -- offsets, box, casing and counts only, never a value.)

How rare is a false hold-back now: a chance match that also has 8+ random printable bytes next to it is about 1 in 1,000 chance matches, so about 1 file in 5,000. Such a file is held back, never sent -- the safe side.

## Not done / for later

- A send does not back-fill: if a file is held back, the folder has fewer than asked. With the fix this should almost never happen; when it does, the send says `sent N of M`.
- The app's live server needed no restart: a send runs in its own new process (`edits.py send-run`), which loads the fixed code.
