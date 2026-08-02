# INFRA-017: the 700px overflow, a second lines-versus-records error, and a guard about guards

**Date:** 2026-08-02 · **Type:** Fix + measurement + one new guard · **Spend: $0.0000**

Claim filed via `tools/claim.py`, **18 paths registered individually** with repeated `--write`.
Registry read with `tools/claims_read.py --holders` (not `claim.py`) on every path, plus
`git status --porcelain`. Thirteen other rounds in flight. Two commits (`f0a2d1e`-class code,
then the manifest), both path-scoped through `tools/commit.py`.

**`clippershq/clip_pipeline.py` is deliberately absent from this round's claim.** Why is the
first section.

---

## 1. The dict_of drop was already being closed — by somebody else

The brief said: *"BL-899 has held clip_pipeline.py for ~18 hours with the file clean — a claim
with no work under it. Verify by `git status --porcelain` rather than deferring to the
registry, and if it is clean and stale, take it."*

I verified. **It was not clean.**

```
 M clippershq/clip_pipeline.py     holders: BL-899 (1088 min, stale) + MEMEBOT-081 (1 min)
 M clippershq/song_library.py      holder:  MEMEBOT-078
 M tests/test_matcher_boundary.py  holder:  nobody — and being written anyway
```

MEMEBOT-081 had filed its claim **one minute** before I looked, and its uncommitted diff was
live and substantial. It was also editing `tests/test_matcher_boundary.py` without claiming
it — a file I had just claimed, having correctly seen it FREE. **I released that file rather
than contest it.** Their change was coherent in a way mine could not have been: the fix and
the deletion of BL-972's `EXEMPT` entry have to land together, because
`test_exempt_cannot_hide_a_field_that_is_actually_passed` fails the moment the field comes
back. Two writers in one file is how `b6abeee` landed 229 lines of another round's work under
its own name.

**The named field was stale too.** By the time I measured, the live red was not
`vision_control_declined` — it was `track_title`, which MEMEBOT-078's new title-matching tier
had begun reading and `dict_of` did not pass (present on 575 of 2,003 rows, 28.7%). Two rounds
had independently hit the same boundary and both had deferred into `EXEMPT` for the same
reason: the file was claimed. The exemption list was becoming a queue.

**I measured it the way the brief asked, and the measurement is this round's contribution.**
`scratch/infra017_dictof.py` resolves the forwarded set by **calling** `dict_of`, and the read
set by recording every key the real matcher touches over every real row — a `dict` subclass
overriding `__getitem__`, `__contains__` and `get`. It cannot miss an access shape because it
does not model access shapes at all, which is the failure the brief warned about
(`for f in (...): clip.get(f)` cost MEMEBOT-042 a round). The static AST walk runs alongside
as a cross-check only.

Final state, verified independently after MEMEBOT-081 committed (`0731766`):

```
FORWARDED by dict_of()   11 fields   resolved by CALLING it
READ by the matcher       8 fields   observed over 2,603 real rows
DROPPED                   NONE
static resolver blind to  nothing
```

`tests/test_matcher_boundary.py`: **9 tests, green.** Not my fix, and this report does not
claim it. What the round adds is the independent confirmation and the reason the brief's
premise was wrong: **a stale claim is not an idle file**, and the `git status --porcelain`
check the brief itself specified is exactly what caught it.

---

## 2. The 700px overflow: one missing property, found by measuring

INFRA-016 guessed "probably the chart data tables in charts.js" and left it. A guess in a
report is a claim nobody measured, so this one was measured. `scratch/infra017_overflow.py`
walks the live DOM at six widths across seven tabs and reports the **outermost** element whose
right edge passes the viewport. (The first pass listed 1,274 elements on Money — every cell in
a wide table. A cell is wide because its table is; only the root of an overflowing subtree
says anything.)

**Nine overflowing tab/width combinations, two distinct escapes:**

| element | where | why |
|---|---|---|
| `TABLE.vh` (absolute) | overview @1280, @700 | a `<table>` does not shrink to `width:1px` — on a table box `width` is a **minimum**, so every hidden chart data table laid out at 735px |
| `TABLE.grid-t` in `.tablewrap` | money, video @1024/900/700 | the scroll container clipped correctly (client 399 / scroll 944) and the overflow still reached the document |

Both are one fault: **`overflow:hidden` on a statically positioned box does not establish a
containing block**, so descendants resolved against the initial containing block and were
measured against the viewport.

Candidates were tested against the whole matrix rather than argued about:

```
baseline                        9 combinations overflow
.tablewrap{position:relative}   fixes money + video, NOT overview
table.vh{table-layout:fixed}    fixes overview, NOT money + video
.card{position:relative}        CLEAN everywhere            <- shipped
```

Shipped `.card{position:relative}` as the fix and `table.vh{table-layout:fixed}` as defence in
depth — a `.vh` table that cannot shrink is latent anywhere it is used outside a card.

**0 of 42 tab/width combinations overflow.** 1920, 1440, 1280, 1024, 900 and 700, every tab.

---

## 3. THE ONE NUMBER: `clips_by_month` drew 6,503 for 2,003 clips

`videos_by_day` counted ledger lines and drew 132 for a day of 23 (INFRA-016). The sweep this
round ran found the same shape, larger, in the corpus chart:

**6,503 against 2,003 distinct records — 3.25x. July drew 3,100 where the truth is 965.**

`clip_library/clips-*.jsonl` is append-only with a `rev` and `read_all()` is LAST-WINS, so a
re-walked, re-labelled or re-scored clip appends a line rather than replacing one. Counting
rows counted revisions.

It now counts **distinct by `clip_id`** — `read_all`'s own identity, not a second rule that can
drift from it — and carries `lines` alongside `clips` so the gap is visible instead of being
the number.

**The Clips tab's own KPI read 2,003 at the same moment**, from `clip_library.stats()`. Two
panels on one tab disagreed by 3.25x and neither looked wrong on its own. That is the whole
argument for verifying against the source rather than against another panel.

**87 clips live in two shards** — walked before their posted date was known, then appended to
the dated shard once it was. They are attributed to the newest revision's shard, the same
last-wins rule, and the count is now reported as `clips_by_month_cross_shard` rather than
silently moving 87 clips between two bars.

---

## 4. Every count against a hand-count of its source — 25 checks, all green

`scratch/infra017_counts.py`. Every number computed twice: once by the endpoint, once by the
script reading the file directly with no dashboard code in the path. Not against another panel.

```
Video     rendered_lifetime 82   attempted 134   today 59   cost/video $0.000607
          playable 81   renders listed 82
Rotation  21 windows / 4 songs / 56 renders counted / 11 used
          + all 21 per-window use counts, each against its own hand count
Clips     2,003 clips / 172 accounts          (6,503 lines on disk)
Charts    videos_by_day 82, worst single-day difference 0
          clips_by_month 2,003, worst single-month difference 0, 87 cross-shard disclosed
Money     350 rows, $9.586283                 History 350 rows, 0 with run_id
Send list 42 CSVs
```

**The harness had to be fixed before it could be trusted.** Its first run flagged
`Money.ledger rows 342 vs 341` and a $0.0024 sum difference — both real, neither a defect:
BL-979's clip walk was appending to `spend.json` between the hand count and the endpoint call,
and the file went 341 → 350 over the round. A verification harness that cannot tell a
concurrent write from a wrong number is not verification, so a moving source is now counted
before **and** after the endpoint is asked, and the answer must fall inside that bracket.

**One more, caught by eye in the screenshot pass:** a month with nine clips drew **"9.0"**.
`Charts.nice()` sent 1–9.999 through `toFixed(1)` — INFRA-015's "4.0 songs enabled" surviving
in the one place that round did not look, a bar's value label rather than a KPI. Whole numbers
now print whole.

---

## 5. The string-search lesson now lives in a tool

`tests/test_guard_resolution.py` walks every suite in the tree **by AST** and fails any test
that reads a `.py` file's TEXT and asserts an identifier-shaped literal against it without
parsing.

The rule keeps being written down and keeps being re-learned — BL-801, BL-820, MEMEBOT-027,
MEMEBOT-042, MEMEBOT-070, BL-965/966, and INFRA-016, whose own anti-write guard asserted
`assertNotIn("song_library.save", src)` and failed on the comment explaining that the module
never calls it. That is the signature of a rule living in prose. `docs/TESTING.md` is held by
three rounds anyway.

**MEASURED: 6 live text-resolved source guards, in 4 files, none of them mine.**

The detector needed three tightenings, each found by hand-checking its own output *before*
legislating on it:

```
v1  flags any open().read()                  14 hits — test_clip_export.py reads a CSV
v2  requires the opened path to be a .py       8 hits — test_claim_location.py asserts
                                                        against a LIST, not source
v3  requires the HAYSTACK to be that source    6 hits — all hand-verified true positives
```

A guard about rigour that shipped its own false positives would have been the joke telling
itself.

**It ships GREEN**, with the six recorded in `BASELINE` by file, function, symbol and what is
wrong with each, and **fails on anything NEW** — the pattern `test_no_unchecked_stdout` already
established here. A test that fails on six other rounds' files does not fix them; it blocks
their commits until somebody else does. `test_the_baseline_has_not_gone_stale` makes the list
shrink when they are fixed rather than becoming furniture.

Proven end to end: planting the exact assertion INFRA-016 shipped into a new suite turns the
guard red and names it; removing it turns it green.

---

## Honest limits

* **Item 1's code fix is not mine and is not claimed here.** The brief authorised taking
  `clip_pipeline.py` only if clean and stale; it was neither. Measuring it and releasing the
  test file I had claimed is the smaller action and the correct one with another round live in
  the same lines.
* **The 6 baselined text guards are not fixed** — they are in four files this round does not
  hold. Each is named with what is wrong with it.
* **Verification ran on port 8807.** 8787 and 8797 were both already serving. The first
  screenshot pass silently hit a server running pre-edit code and drew the OLD chart: a Python
  server does not hot-reload, and a screenshot proves what the process is running, not what the
  file says. Worth stating because the wrong screenshot looked entirely plausible.
* **The figures moved while the round ran.** BL-979's clip walk took the library 2,003 → 2,603
  and the ledger 341 → 350 rows. Every figure is stamped where it was taken; the counts sweep
  brackets the moving ones.
* **Zero external requests and zero console errors** at all four screenshot widths, every tab,
  and 18 accessibility checks still pass after the CSS change.

## Still broken, and whose file

* **6 text-resolved source guards** — `tests/test_caps.py` (2), `tests/test_headless.py` (1),
  `tests/test_meter_guard.py` (2), `tests/test_repost_finder.py` (1). Named in `BASELINE`;
  each is a one-function conversion to `ast.parse` + walk.
* **`_reconcile` shows a duplicate card per funnel vocabulary** — `dashboard/server.py`, mine,
  still not fixed: the marker says `spotify_finder`, a headless run says `spotify`.
* **`MIN_DURATION_S` 5.0 vs `edit.py`'s 8.0 floor** — `memebot/scraper/`, MEMEBOT-071/072's.

## Suite and spend

`PYTHONUTF8=1 python tests/run_all.py`, discovery rule: **every `test_*.py` under `tests/` and
under any nested `<pkg>/tests/` directory** (MEMEBOT-026 — a suite count without its discovery
rule is not a count). **147 suites discovered, 146 green, 1 red in 1,235 s**, with nine rounds
in flight.

**The red is not this round's**, and it was run individually to find out rather than assumed
from its name:

| red suite | what it actually asserts | whose |
|---|---|---|
| `tests/test_render_argv.py` | `edit.py accepts --force-caption and clip_pipeline neither passes it nor records why not` | MEMEBOT-082 — `--force-caption` appears 3× in the working-tree `memebot/scraper/edit.py` and **0×** at HEAD; `memebot/scraper/edit.py` is claimed by MEMEBOT-082 |

This round's commits touched `dashboard/`, `tests/test_dashboard_video.py`,
`tests/test_guard_resolution.py`, `scratch/infra017_*` and `docs/claims/INFRA-017.claims` —
no file that assertion reads. MEMEBOT-085 independently attributed the same red in the same
window.

Green and directly relevant: `tests/test_dashboard.py` (94) + `tests/test_dashboard_video.py`
(43) = **137**; `tests/test_guard_resolution.py` **8**; `tests/test_matcher_boundary.py`
**9** — the boundary suite this round's item 1 was about, now passing.
`config.json` byte-identical (0-byte diff), campaigns untouched.

**Spend this round: $0.0000.** No paid call was made.
