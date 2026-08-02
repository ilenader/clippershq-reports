# INFRA-016: the dashboard runs, shows and plays the video pipeline — and still cannot advance rotation

**Date:** 2026-08-02 · **Type:** Feature + one measured correction · **Spend: $0.0000**

Claim filed via `tools/claim.py`, **15 paths registered individually** with repeated `--write`.
Registry read with `tools/claims_read.py --holders` (not `claim.py`) on every path, plus
`git status --porcelain`: `dashboard/` FREE, `tests/test_dashboard.py` FREE,
`memebot/runs.jsonl` FREE. Twelve other rounds in flight; no path conflicts. Nothing in
`clippershq/` or `memebot/` was written — BL-899 holds `clip_pipeline.py` and this round only
**reads** it. Two commits (`a2b41f1` code, `3b88ec7` manifest), both path-scoped.

---

## The one number

**The chart called "videos rendered per day" drew 132 for a day on which 23 videos were made.**

It counted ledger LINES. `memebot/runs.jsonl` is append-only: one video writes a `pending`
line and then an `ok` line, outcome lines share the file by design, and a re-render bumps
`rev` rather than replacing anything. Measured on the live file
(`scratch/infra016_verify.py`):

| | |
|---|---|
| raw lines | 211 |
| render lines (outcome lines skipped) | 163 |
| **DISTINCT records** | **80** |
| finished (`status: ok`) | 31 |
| 2026-08-01: lines → finished videos | **132 → 23** |

A 5.7x overstatement, on the only chart the video half of this system has, in the one place
an operator would look to ask "is it working". It now resolves through
`clip_pipeline.read_records()` — the renderer's own last-wins resolver, keyed on the output
path exactly as `outcome_loop.record_id_for()` is. Reusing it rather than re-deriving the rule
is the point: MEMEBOT-015 already paid for what happens when one ledger has two readers with
two rules.

---

## 1. The video funnel is startable from the page

`clip_render` was reachable from `run.py` (BL-958) and from `control.py`'s menu key `[v]`, and
from nowhere on the dashboard. The cause was one line: `ALL_FUNNELS` was a **hand-kept copy**
of run.py's table, and run.py grew a tenth entry without it. A hardcoded copy of someone
else's list is a bug with a delay on it.

It is now read from `run.py` itself. The literal survives only as an import-failure fallback,
and the suite asserts the two agree — a funnel added tomorrow appears on the page without an
edit.

The existing test asserted `len(funnels) == 9`, which is the same defect in miniature: a count
pinned to a number cannot tell "a funnel went missing" from "a funnel was added", and it
duly reported the new funnel as the error. It now asserts against `run.FUNNELS`.

**A `--target` does not mean the same thing on every funnel.** Nine count leads; this one
counts **videos**, and each video is one billed re-fetch. `/api/now` returns `funnel_units`,
and the form rewrites its own label and cost note on change, so it never tells the operator
they are buying leads when they are buying videos.

### Proven, from the page, for $0.0000

`scratch/infra016_runproof.py` drives the real form with Playwright — select `clip_render`,
target 1, cap, click Start run. Captured off the wire and off disk:

```
argv          -m clippershq.run --funnel clip_render --cap 0.001 --target 1
status file   completed, 10.5s, spend_usd 0.0, spend_scope campaign:memebot
ledger delta  $0.000000
console       0 errors        external requests   0
```

**Why the cap is $0.001 and why that is not a cheat.** This round's preconditions say no paid
calls, and a render costs one billed re-fetch. `run_batch` judges its cap on the **worst case
for the next candidate** — `max_pages * cost` = 2 × $0.0006 = $0.0012 — and stops **before the
first request**. So the run starts, is attributed, writes its status file and exits cleanly
having spent nothing: every link this round added is exercised, and it stops exactly at the
one that costs money. The render path itself is not in question — 81 finished videos are on
the ledger, made by other rounds through the same code.

The first draft typed $0.0001 and the browser silently refused to submit: the cap field
carries `min="0.001"`. The page's own constraint is real, and the harness now respects it.

---

## 2. The video state

`/api/videos` keeps its disk walk and gains a `ledger` block. **Two populations, both named,
neither standing in for the other.** The walk finds 55 video files lying around — it sees
renders from scratch drivers and files moved in, misses anything outside its two roots, and
carries no song, no window and no money. The ledger knows what this system *made*.

```
renderable right now   286      14.3% of the corpus
rendered today          58      2026-08-02
rendered lifetime       81      of 133 attempted
cost per video      $0.0006     RENDER LEG ONLY
playable now            80      1 no longer on disk
video files on disk     55      a different count, and it says so
```
*Snapshot 15:11. These move while you read them — MEMEBOT-071/073 render into this ledger
continuously, and finished renders went 31 → 81 over this round.*

The cost basis names what is **not** in the figure. BL-877 established that every clip cost
quoted in this repo has been vision-only at least once; a per-video number that does not say
"the walk and the labelling are upstream" will be read as the cost of a video.

The overview tile labelled "videos rendered" was showing the **file** count. It now shows the
ledger's.

---

## 3. Playing them

`/api/renders` returns **paths, not counts** — a count cannot be watched. Each row carries the
song, the hand-marked window, the operator's own note on that window, the template, the match
reason and the cost.

`/api/video/{token}` streams one render. It is allowlisted **by the ledger**: the URL carries
a sha256 of the output path, never the path, so there is nothing to traverse — `..` cannot be
spelled. `/download/{name}`'s approach (allowlist by listing one flat directory) cannot work
here, because renders land in nested per-run work directories. Two further gates: the resolved
path must sit under the repo root, and it must carry a video extension, so a malformed or
hostile `output` field cannot turn this into `GET /any/file`. Range requests are honoured, so
the player seeks without downloading first.

A record whose file has moved still counts as a video that was made — the record is the truth,
not the file (MEMEBOT-004 failure mode 4) — and shows "file gone" with the reason rather than a
button that 404s.

**Proven:** the harness clicks the first Play control and reads back from the element itself —
`readyState 4, currentTime 2.84s, 1080×1920, paused false`. A screenshot of a `<video>` tag
proves markup; only `currentTime` proves playback.

---

## 4. Rotation — 21 windows, 11 used, 10 never played

The counter is **derived**. `/api/rotation` calls exactly one thing:
`clip_pipeline.hook_uses_from_ledger()`, which reads the ledger and returns a dict. It does not
load a store, does not call `pick()` or `render_plan()`, and there is no code path from any
endpoint here to a write.

That design is MEMEBOT-072's, not this round's, and it is the reason this feature is safe to
build at all. BL-888 found `render_plan()` defaulting to `count=True` while this page polled
every 5 seconds: ~1,440 phantom uses a day against clips nobody rendered, corrupting the
fairness the counter exists to provide. The fix was not to remember `count=False` at every call
site — a preview, a dry run and a dashboard read all look identical to a planner. It was to
stop storing the number.

Guarded three ways in `tests/test_dashboard_video.py`:

* `scratch/songs.json` is **byte-identical** after six full poll rounds across all eleven
  endpoints (thirty seconds of the real 5 s poll; BL-888's counter moved on the first one).
* `memebot/runs.jsonl` is byte-identical after the same.
* an **AST walk** over `dashboard/server.py` refuses any call to `save`, `pick`,
  `apply_ledger_uses`, or `render_plan` without `count=False`.

The AST walk replaced a string search, and the first draft is why: written as a grep it failed
on `server.py`'s own **prose** — the comment explaining that this module never calls
`song_library.save()` contains those words. A grep cannot tell a call from a sentence about a
call, and half the value of that file is the sentences.

### The bug the panel had, caught by writing it down

Written the obvious way, the panel showed `sng_0001 h1 — uses 0, last played
2026-08-01T16:06:19`. A window reported as never played, with the date it was played.

Two populations behind two numbers in one row. `hook_uses_from_ledger` counts `status == "ok"`
exactly; `_is_finished` also accepts a record with no status but a real output, which is how
every line predating the field looks and is the right test for "did this produce a video". The
count now uses the renderer's population, and the four records in the gap are **reported**
(`renders_not_counted: 4`) rather than dropped — they are real renders that rotation cannot
see, exactly as the renderer cannot see them.

### What the rotation now says out loud

`sng_0004` (hype) carries **45 of 56** counted renders; `sng_0002` (triumphant) has **never
been played at all** — six hand-marked windows, zero renders. That is not a code defect. It is
the supply problem MEMEBOT-019 measured (0 of 412 vision-labelled clips matched song02) now
visible on the page instead of buried in a scratch file, and what to do about it is a
song-purchase decision.

---

## 5. Everything that was already true, still true

Asserted, not assumed — `ThePageStillHasEveryPropertyItHad` plus the screenshot harness:

* **zero external requests** — 0 at 1920 and 1280, every tab, including while the player is
  streaming. `/api/video/...` is same-origin, which is precisely why the player streams from
  the server rather than linking a `file://` path.
* **zero console errors** — 0 at both widths.
* **`money(null)` renders "unknown"**, never `$0.000`.
* **panels render independently** — the two new endpoints are two more promises, not two more
  things to wait for.
* **the in-place poll preserves open panels and focus** — focus on a Play control survives 6.5 s,
  more than one poll cycle, measured.
* **no credential is reachable from any endpoint** — the import-time assertion is untouched, and
  the new endpoints read only the ledger and `songs.json`.
* **one panel visible at a time** — `panels_visible=1` on all seven tabs at both widths. That is
  the 12,232px stack expressed as a number rather than as an eyeball.

---

## 6. The screenshots, and the two defects they caught

Seven tabs × two widths in `scratch/infra016_shots/`, plus `video-playing-1920.png` and the
two run-form shots:

```
overview-1920.png  money-1920.png  run-1920.png  clips-1920.png
video-1920.png     history-1920.png  settings-1920.png       (+ the same seven at 1280)
video-playing-1920.png   run-form-clip_render-1920.png   run-started-1920.png
```

**At 1280 the rotation grid fitted three song blocks per row, each ~375px, against a
four-column table whose narrowest honest width is 424px — and `.card` sets `overflow:hidden`,
so the operator's own note on each window was cut off mid-word at the card edge.** Two changes:
each table went into a `.tablewrap` (so nothing can ever be lost, only scrolled), and the
grid's track minimum went 320 → 420px, giving four songs across at 1920 and two at 1280 with
no internal scrolling at either. Verified by measurement, not by eye: `tableW == wrapW` at both
widths, body never overflows horizontally.

That is the second layout defect in this file's history found only by looking at a picture.

## 7. Accessibility

Run **inline**. The project hook asks for the accessibility-lead subagent on any web change;
this round's brief says RUN ALONE, and the brief wins — so `scratch/infra016_a11y.py` runs the
checks the lead would have coordinated, against the **live page** rather than the source, since
a source scan cannot see a computed contrast or an accessible name. 18 checks, all passing.

**One real finding, fixed.** 24 Play controls produced **18 unique accessible names**: this
system renders the same account through the same window repeatedly, so account + song + window
is not an identity. Six controls announcing the same sentence is six controls a screen-reader
user cannot tell apart. The timestamp is now part of the name — 24 of 24 unique.

Also: the "file gone" reason moved out of a `title=` attribute (unreachable by keyboard,
unreliable on touch) into a visually-hidden span; every rotation bar is `aria-hidden` with the
count as text and **"never" as a word**, not a dim row; each per-song table carries a caption;
the `<video>` states that these renders carry no caption track and names the clip, song and
window as the text alternative available. New surfaces measured for contrast: 5.96–13.09:1.

---

## Honest limits

* **No video was rendered by this round**, by design — see §1. The wiring is proven end to
  end; the render leg was already proven by 81 videos on the ledger.
* **Port 8797, not 8787.** Another round's server already held the operator's port. Killing it
  to take the number was the worse trade; the page is identical either way.
* **A 700px viewport overflows horizontally, and it did before this round.** Measured per tab:
  Overview and Money overflow at 700 with no video panel on them at all. Every container this
  round added is verified inside the viewport at 700 (rightmost edge 671 of 700) and scrolls
  internally, so the residual is elsewhere — probably the chart data tables in `charts.js`.
  700px is below this page's stated target and `charts.js` is outside this claim.
* **The counts in this report moved while it was being written.** MEMEBOT-071/073 were
  rendering into `scratch/mb07*_work/` throughout: finished renders went 31 → 81 in the session.
  Every figure is stamped where it was taken. The `+1 render` the run-proof observed during its
  own window was **not** this run's — this run stopped on its cap and made zero — and the
  script now says so rather than reporting a global delta as its own.
* Two pre-existing oddities left alone as out of scope: the Run tab's funnel grid shows a
  duplicate `spotify` card (marker vocabulary `spotify_finder` vs headless `spotify`), and the
  Money tab is a 9,040px page because it lists every ledger row.

## Still broken, and whose file

* **`MIN_DURATION_S` 5.0 vs `edit.py`'s 8.0 floor** — MEMEBOT-071/072's, `memebot/scraper/`.
* **One song carries 80% of renders and one has never been played** — visible on this page now.
  The operator's decision, not a code fix.
* **`_reconcile` shows a duplicate card per funnel vocabulary** — `dashboard/server.py`, mine,
  not touched this round.

## Suite and spend

`PYTHONUTF8=1 python tests/run_all.py`, discovery rule: **every `test_*.py` under `tests/`
and under any nested `<pkg>/tests/` directory** (MEMEBOT-026 — a count without its discovery
rule is not a count). **138 suites discovered, 135 green, 3 red in 1,666 s**, with twelve
rounds in flight and four other invocations of the same runner competing for the box.

**None of the three is this round's**, and each was run individually to find out rather than
assumed from its name:

| red suite | what it actually asserts on | holder |
|---|---|---|
| `test_claims_manifest.py` | `docs/claims/MEMEBOT-067.claims` reaching a named exemption | MEMEBOT-075 |
| `test_no_unchecked_stdout.py` | `tests/test_manifest_prose_refused.py:73` reads a subprocess's stdout with no return-code check | MEMEBOT-075 |
| `test_matcher_boundary.py` | `clip_pipeline.dict_of()` drops `vision_control_declined`, the ninth value computed then discarded at that boundary | BL-899 |

This round's two commits touched `dashboard/`, `tests/test_dashboard*.py`,
`scratch/infra016_*` and `docs/claims/INFRA-016.claims` — no file any of those three
assertions reads. `tests/test_dashboard.py` (94) + `tests/test_dashboard_video.py` (43) =
**137 tests, green**. `config.json` is **byte-identical** (0-byte diff) and the campaigns
block is untouched.

**Spend this round: $0.0000.** No paid call was made.
