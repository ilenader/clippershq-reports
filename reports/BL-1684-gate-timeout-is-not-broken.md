# BL-1684: Send gate -- a picture-check timeout is no longer cached as "broken" ($0)

Found in BL-1678. The Send gate's picture pass (`clippershq/edits_send_gates.py`) answered **broken** when ffprobe
or the ffmpeg decode ran out of time on a busy PC. `send_gates` cached that answer per file size forever. Two good
videos stayed "broken" from a busy 14 Oct night (one with 11 of 94 frames read), and every later Send skipped them.
This is the same trap as LESSON 20/22 (a timeout is not a verdict).

## Change
- `TIMEOUT = "timeout"`: `_duration` returns it on `subprocess.TimeoutExpired`, and `picture()` returns problem
  `timeout` when ffprobe or the decode times out. Other failures (no duration, ffmpeg error, too few frames) are still
  `broken`.
- `_row()` never trusts a cached `timeout` row: the next check looks again and the real answer replaces it.
- `check()` gates a timeout for this send only (why = `timeout`). The video stays in the library, unsent, and is tried
  next time.
- The send worker starts as a fresh process for each Send, so no server restart is needed.

## Tests
- New `tests/test_bl1684_gate_timeout.py` 5/5: ffprobe timeout -> timeout; ffmpeg timeout -> timeout; a real non-video
  -> still broken; a cached timeout is re-checked and replaced by ok; check() gates a timeout, then passes on the next
  look. On the old code 4 of 5 fail.
- Existing tests on the send path all OK: test_bl1631_library_send, test_bl1636_send_gates (6), test_bl1639_film_is_superhero,
  test_edits_send_fixed_folder; test_atomic_io OK.
- **Not run:** the full suite (~22 min). The PC had 2.6 GB free, under Dusan's 4 GB floor (LESSON 58). It is owed to
  3 FIXER on the farm.

## Not changed
- Old rows already cached as `broken` stay as they are (2 known stale ones; BL-1678 already re-added those 3 videos to
  the everything folder). Clearing cached rows is a delete, so it waits for a decision.
- A 240 s video that decodes cleanly but yields < 80 % of the expected frames is still `broken` (the frame-count rule).
  It needs its own look.

$0.
