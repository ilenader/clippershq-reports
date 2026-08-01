# MEMEBOT-012 — the hook-marking page

*2026-08-01. Builds only `hookmark/` and `scratch/`. No `clippershq/` or `memebot/` edits, no paid calls.*

MEMEBOT-007 closed on the honest caveat: *"the window is my judgement from an RMS map, not
yours — if 120-162s isn't the hook you'd pick, the pipeline will place the wrong one just as
precisely."* That is the gap. Marking a hook by hand was already the design and it is
measured-correct; what was slow about it was that "by hand" meant reading an RMS map in a
text dump and typing two numbers into JSON.

`python hookmark/server.py` now opens a local page that draws the song, takes a dragged
window, plays it, plays it again against a real clip's length, and writes it to the song
library. It decides nothing.

![The hook marker: waveform and RMS contour with a dragged window, the dashed suggestion
marker, and the clip-length rehearsal showing the hook entering at 17.20 s and repeating
4×](memebot012_proof.png)

---

## What it does

| | |
|---|---|
| **Load a song** | from the library, or add any audio file the server can see on disk |
| **See it** | peak waveform + RMS energy contour in dBFS, one shared time axis, one ruler |
| **Mark it** | drag on the waveform, drag an edge to adjust, or type the two numbers |
| **Hear it** | play the window, loop it, with a playhead running over both plots |
| **Hear it in context** | place it in a real clip length and repeat it exactly as the renderer would |
| **Save it** | to `songs[].hooks[]`, many per song, with a label |

Measured on the one real song in the tree, `memebot/scratch/song01.mp3` (162.54 s, 44.1 kHz
mp3): 3,000-bucket peak envelope, **3,251-point RMS contour** at a 0.05 s hop spanning
**-90.0 to -6.3 dBFS**, both drawn from the decoded PCM rather than from anything inferred.

## The suggestion is a marker. It is never a default.

`_find_loudest_window_start` is ported into `hookmark/suggest.py` verbatim from
`memebot/scraper/edit.py`, units fix and all, so the marker on screen is that function's real
answer and not an approximation of it. Everything after that is deliberate friction:

* it is drawn as a **dashed** band with the label `SUGGESTION (a guess) — press Use to adopt`;
* the word **"guess"** is in the prose, not only in the colour;
* it **never** pre-fills the selection — the proof asserts the start/end fields are *empty*
  after a song loads;
* it takes **two** presses to reach the library (Use, then Save);
* when it cannot produce an answer it stands behind, **no marker is drawn at all** — a marker
  at 0.0 would be a claim.

The reasons are on the page itself, not just in the code: BL-690 measured automatic drop
detection at **100% fabrication** on real audio — a timestamp on all 36 clips including all
19 with nothing there, its most confident outputs the wrong ones. BL-795 closed automatic
mood at 40% reproducibility. `edit.py`'s own docstring says *"THIS IS A SUGGESTION, NOT A
HOOK FINDER."*

**One corroboration worth recording.** The port independently returns **120.00 s** for
`song01.mp3` — the exact start of the 120–162 s window MEMEBOT-007 read off its RMS map by
hand. Two different methods, same section. That is evidence the port is faithful and that
MEMEBOT-007 read its map correctly. It is *not* evidence the section is the hook, which is
the whole reason the marker stays a marker.

## The playback check that matters

A hook that sounds right in isolation can land wrong in a 40-second video. **Hear it against
a real clip length** mirrors `clippershq/song_library.py`: `place_at()` puts the window at 43%
of the clip, `loop_count()` repeats it to the end, and a timeline strip shows the entry point
and every repeat. Clip lengths in the picker are **real** `duration_s` values out of
`clip_library/*.jsonl` — 589 of them, median 29.9 s — because a rehearsal against a round
number is a rehearsal against a clip that does not exist.

For a 7.50 s window in a 40 s clip the page states: enters at **17.20 s**, repeats **4×**,
**7.20 s** cut off the last repeat. Verified against `song_library.render_plan()` on the saved
library: same numbers.

Silence stands in for the clip's own audio. That is stated on the page — this checks
placement and repetition, not the mix.

## Writing to the library, in a tree with nine other rounds in it

`scratch/songs.json` by default, `--library` to point elsewhere. Writes go through
`clippershq.song_library.save()` when that module imports (an identical atomic
tmp+fsync+replace fallback when it does not, since it was itself under construction).

Every write is a read-modify-write against the file on disk with a **`rev` guard** — a sha1 of
the library as the page loaded it. If it changed in between, the save is **refused** with a
message telling you to reload. Never a silent overwrite. Saved hooks carry
`marked_by: "hand"`, `marked_with: "hookmark"` and a timestamp, so a later reader can tell a
marked window from a typed one.

**MEMEBOT-008 held `clippershq/song_library.py` and `scratch/songs.json` for the whole of this
round.** Nothing here wrote either. The proof runs against its own
`scratch/memebot012_demo_library.json`; the live library was verified **read-only** — it loads
as 3 songs / 5 hooks / 0 validation problems and its hash is byte-identical afterwards.

## Proof

`python scratch/memebot012_prove.py` drives the page in a real browser. Nothing is mocked: it
adds the real mp3, samples the *drawn pixels* of both canvases, drags with real pointer
events, starts the Web Audio graph, rehearses against a 40 s clip, saves, and reads the
library back off disk.

**34/34 checks pass.** Highlights: the contour is real (`3251 points, -90.0..-6.3 dBFS`); the
drag lands where it was aimed (`121.50–129.00 s`); the playhead advances while playing; the
mp3 decodes to a 162.54 s buffer; the saved numbers are **verbatim** what was marked; and
`song_library.validate()` accepts the result with no problems.

### Two real bugs, both found only by running it

1. **The canvases grew without bound on any HiDPI display.** `fitCanvas` re-read the `height`
   attribute it had just written, so at `devicePixelRatio` 2 it read 200, wrote 400, read 400,
   wrote 800. The document reached **33,554,432 px** tall and every control fell out of the
   viewport. Invisible at 1×, which is exactly why it needed a browser at 2× to find.
2. **Playback stopped on its own first animation frame.** Audio is scheduled ~50 ms ahead, so
   the first frame's playhead is *before* the start — and the tick loop read "no playhead" as
   "finished". `playbackDone()` now asks the question it meant to ask. The same conflation
   would have killed every rehearsal during its silent lead-in.

Both are fixed and both are locked by a check.

## Accessibility

The project hook asks for an accessibility agent to review any UI. This round was told to run
alone, so the requirements were **measured** instead of delegated — and the measurements are
in the proof, section 11: every control has an accessible name, both plots carry `aria-label`s
that state the current window, status is a live region, worst-case text contrast is **5.2:1**
(WCAG AA is 4.5:1), and colour is never the only signal. The drag has a full keyboard
equivalent — focus the waveform, arrows move the window, Shift for 1 s, Alt stretches the end,
Space plays — verified by pressing the keys, not by asserting the handler exists. A human
review is still the stronger check and this does not replace one.

## Offline

Python standard library only, bound to `127.0.0.1`, system fonts, no CDN, no webfont, no
analytics. The server sends `Content-Security-Policy: default-src 'self'; connect-src 'self'`,
so a mistake in `app.js` could not call out even if one were written. Same rule as the
dashboard. `ffmpeg`/`ffprobe` must be on PATH — the renderer already requires them; without
them the page says so and shows nothing rather than guessing.

## What this does not do

* **"Hear it" is proved up to the speaker, not through it.** A headless browser has no audio
  device. What is verified is the decode, the scheduled source and the advancing playhead.
  The last few centimetres are yours.
* **The rehearsal plays silence where the clip's audio would be.** It checks placement and
  repetition. It is not a preview of the finished video.
* **`loudest_window_start` is a copy, not an import.** Importing `edit.py` drags in the whole
  render stack and this round could not edit that module. A future change there must be
  mirrored in `hookmark/suggest.py`; the docstring says so at the copy site.
* **The suggestion window is fixed at 20 s in the UI.** The API takes `window_s`; there is no
  control for it yet.
* **First open of a song costs ~9 s** (two ffmpeg passes over a 162 s track), cached by path
  and mtime afterwards. No progress bar, just a status line.
* **Nothing is committed.** `docs/claims/MEMEBOT-012.claims` is written and will verify once
  it is — `verify_claims.py` checks `git show HEAD:` and reports 0/19 until then. Committing
  is not this round's call in a tree holding nine other rounds' uncommitted work.
* **Claude-in-Chrome could not be used.** There is no Chrome process on this host, so the
  extension's browser cannot reach `127.0.0.1`. The proof drives the locally installed
  Playwright Chromium instead — a real browser, just not that one.

## Files

    hookmark/server.py            local server, library read/write, rev guard, clip lengths
    hookmark/suggest.py           waveform + RMS from PCM; the ported loudest-window suggestion
    hookmark/static/index.html    the page
    hookmark/static/app.js        canvases, drag, playback, rehearsal, save
    hookmark/static/app.css       system fonts, dark, AA contrast
    hookmark/README.md            why the suggestion is a marker, and what is measured vs guessed
    scratch/memebot012_prove.py   34 checks against the live page
    docs/claims/MEMEBOT-012.claims
