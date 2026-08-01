# INFRA-006 — The marker leak was real but my diagnosis of it was wrong. Fixed at the actual cause, and the settings list cut from 44 to 23 with one line each

**Date:** 2026-08-01 · **Type:** Fix + curation · **Spend:** **$0.00** — no paid call
Claimed as INFRA-006 · guarded scope · timestamped backups · `git -C` only
Suite **63/63, 2,703 checks** · campaigns SHA `8e02f8d6f6307ae8` · config 162 keys

---

## 1. The marker side effect — corrected, then fixed

**INFRA-004 said "importing `control` writes a RUNNING marker as a side effect." I wrote that,
and it is wrong.** It was inferred from the marker's pid matching the suite's, never tested.
Measured here by importing each module in a fresh process and diffing marker mtimes:

| action | markers written |
|---|---|
| `import control` | **NONE** |
| `import spotify_finder` | NONE |
| `import twitch_finder` | NONE |
| `import youtube_finder` | NONE |
| `import server` (the dashboard) | NONE |

**The real cause:** `tests/test_funnel_wiring.py` calls the *real*
`control._find_spotify / _find_twitch / _find_youtube` with `confirm_fn=lambda: True`. Those
functions write their RUNNING marker **at run start, which is correct** — but the suite runs
with `cwd=ROOT`, so `marker_path()` resolved to the **shared production `scratch/`**. A green
test run therefore left three funnels looking live, carrying the suite's own pid, and
`/api/now` reported them as in flight.

**The timing was never the bug. The path was.** So the fix is not to move marker creation —
it is already in the right place — but to make its root redirectable:

```python
def marker_path(round_id, root=None):
    if root is None:
        root = os.environ.get("CLIPPERSHQ_STATUS_DIR") or "scratch"
```

and one line in `tests/run_all.py` pointing every child at its sandbox.

**This is the third file in exactly this class**, and `run_all.py` already carries the scars of
the other two in its comments: the money ledger (155 phantom rows, ~$1.69 never actually spent,
because a test resolved `./spend.json` to the real one) and `run.log` (truncated real forensic
history twice). Same shape, same one-line fix, third time.

### Proven

```
PRODUCTION MARKERS BEFORE THE SUITE      ... 3 with recent timestamps
running tests/run_all.py ...             ALL GREEN -- 63/63 suites, 2703 checks (138s)
PRODUCTION MARKERS AFTER
  spotify_finder   unchanged
  twitch_finder    unchanged
  youtube_finder   unchanged
  markers written by the suite: 0
```

> An earlier attempt at this proof reported markers still moving. That run was **confounded**:
> nine other rounds were in flight and a marker was written at 15:45:40 by a pid that was not
> mine. The isolated child test (env set, markers land in the sandbox, production untouched)
> is what actually establishes the mechanism, and the clean full-suite run above confirms it.

## 2. Settings: 44 → 23 curated, 43 advanced

Each curated knob shows its **live value** and **one line** on what moving it does.

| setting | value | consequence |
|---|---|---|
| `spotify_finder.run_target` | 700 | How many Spotify artists to deliver before stopping. **⚠** |
| `twitch_finder.run_target` | 500 | How many Twitch streamers to deliver. |
| `youtube_finder.run_target` | 50 | How many YouTube channels to deliver. |
| `repost_finder.run_target` | 50 | How many confirmed repost pages to deliver. |
| `repost_finder.pages_per_tag` | 2 | Pages per tag. Each is one paid call and ~30 clips. |
| `twitch_finder.min_viewers` | 20 | Drop streamers below this many live viewers. |
| `twitch_finder.max_viewers` | 1000 | Drop above this; past ~1k they already have clippers. |
| `spotify_finder.min_listeners` | 50,000 | Drop artists below this many monthly listeners. |
| `spotify_finder.max_listeners` | 3,100,000 | Drop artists above this — too big to hire cold. |
| `youtube_finder.min_subscribers` | 50,000 | Drop channels below this. |
| `youtube_finder.max_subscribers` | 5,000,000 | Drop channels above this. |
| `clip_max_pages_per_account` | 1 | Pages per account. 1 page = 12 clips = the cap. **⚠** |
| `clip_round_robin` | true | One clip per account per pass. **⚠** |
| `clip_view_floor` | 20,000 | Skip clips below this. Sits at p25; excludes no page. |
| `*_max_run_usd` ×5 | 2.0–5.0 | Hard dollar ceiling per run, on real billed requests. |
| `ig_crawl_enabled` | false | Turn the IG suggested-crawl funnel on or off. |
| `ig_recover_enabled` | true | Recover emails from already-paid profiles first. |
| `ig_follower_scrape_enabled` | true | Scrape follower counts. |
| `cut_garbage_enabled` | true | Apply the garbage cut before export. |

**The three dangerous ones carry a second line, each citing a measurement:**

- **`spotify_finder.run_target`** — above ~777 the run exhausts its seeds and forces
  expansion, at a **measured 17-point handle-rate penalty**. Raise the seed list, not this.
- **`clip_max_pages_per_account`** — at the old default of 10, one page took 120 of a 200-clip
  target and **95.5% of the library came from two accounts**.
- **`clip_round_robin`** — off, the walk drains accounts in master order and reaches **17 of 41
  pages instead of all 41**.

**And one warning that belongs to no single knob:** two concurrent Spotify runs breach
MusicBrainz's 1 req/sec per-IP limit, because **the limiter is process-local** — two processes
do not share it. Run Spotify one at a time.

The remaining **43** stay reachable under `_advanced` rather than being deleted.

### A collision caught before shipping

`run_target` exists in **four** funnel blocks. Keying the response by the bare name collapsed
all four into one entry showing repost's value — and silently discarded Spotify's danger note,
which is the single most important line on the page. Settings are now addressed by a qualified
id (`spotify_finder.run_target`), which is the only representation that can hold four different
run targets.

### The frontend contract is preserved

INFRA-003 fixed this endpoint as a flat `{name: {value, consequence}}` mapping and a frontend is
being written against it. Curation needs tiers, so the tier lists ride **alongside** the flat
mapping under `_curated`, `_advanced`, `_warnings`. A config key never starts with an
underscore, so they cannot collide with a real setting, and a frontend that ignores them keeps
working unchanged.

## 3. Liveness — untouched

`status` still passes through verbatim; `stale` is still a separate derived boolean; nothing is
added to the on-disk marker format. Tests still assert it. As instructed, not changed.

## 4. run.log: a `run_id` prefix is enough. Per-run files are not worth it.

Measured across **180,586 lines** in 4 log files:

| | |
|---|---|
| p50 line | **104 chars** |
| p99 | 1,313 chars |
| **longest line in the entire history** | **1,599 chars** |
| lines over 4,096 chars | **0 (0.000%)** |
| lines over 8,192 chars | **0** |
| **lines carrying any run identifier** | **0 (0.00%)** |

INFRA-002 measured unlocked append as safe to ~4 KB lines and lossy only at ~9 KB. **The real
log never gets within 2.5× of the safe limit**, so the corruption risk is theoretical here —
the interleaving is by line, and every line stays intact.

**The actual defect is attribution, not corruption: 0% of lines can be traced to a run.** Two
concurrent funnels produce one file nobody can demultiplex. A `run_id` prefix fixes that
completely, costs ~31 chars (≈30% of the median line, taking 0.65 MB to ~0.85 MB), and keeps
the single-file tooling — rotation, and a dashboard that reads one log — working as-is.

Per-run files would also fix attribution and would additionally remove the >8 KB risk, but that
risk is not reachable at these line lengths, and they would multiply file count and break every
consumer that expects one log.

**One caveat worth naming:** `log.exception` writes a traceback as one record spanning several
physical lines, and under two writers another process's line can land in the middle of it. A
per-line `run_id` prefix fixes that too, because each physical line then carries its own id —
which per-run files also solve, but at higher cost.

**Recommendation: add a `run_id` prefix to the log formatter. Not implemented here** — this
round was scoped to the marker fix and the settings, and the formatter touches every funnel's
output.

---

## Verification

| check | result |
|---|---|
| does any import write a marker | **no** — measured across 5 modules |
| suite leaves production markers | **0 written**, 63/63 green |
| curated settings | **23**, each with a live value and one line |
| dangerous knobs flagged | 3, each citing a measurement |
| concurrent-Spotify warning | present |
| advanced disclosure | **43** knobs retained |
| bare-key collisions | **0** (qualified ids) |
| flat contract preserved | yes — meta under `_`-prefixed keys |
| liveness check | unchanged, still tested |
| PUT into a funnel block | writes `twitch_finder.min_viewers`, restored after |
| suite | **63/63, 2,703 checks** |
| campaigns SHA | `8e02f8d6f6307ae8` **MATCH** · config 162 keys |

## Honest limits

- **The consequence lines are mine, not measured copy.** The three danger notes cite real
  measurements; the other twenty are my one-line readings of what each knob does. Worth a pass
  from you — you know which of these you actually turn.
- **`google_play` and `ig_crawl` have no `run_target` or `max_run_usd` in config**, so their
  caps are code defaults. They appear in the curated list only where a key exists; the dashboard
  shows `is_set: false` so an unset knob does not read as "off".
- **The settings shape changed additively.** I preserved the flat contract deliberately, but the
  frontend round should know `_curated` / `_advanced` / `_warnings` now exist, and that curated
  ids are qualified (`spotify_finder.run_target`, not `run_target`).
- **The marker fix depends on the env var reaching the child.** Suites launched outside
  `run_all.py` — a bare `python tests/test_funnel_wiring.py` — still write to production
  `scratch/` unless `CLIPPERSHQ_STATUS_DIR` is set. I did not add it to the test file itself,
  because the sandbox belongs to the runner.
- **run.log was assessed, not changed.**
- **My first proof run was confounded by nine concurrent rounds** and appeared to fail. Both the
  isolated test and the clean full-suite run are what the claim rests on.
