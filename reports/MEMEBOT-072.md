# MEMEBOT-072 — 21 of 21 hand-marked windows are reachable, and the unattended run joins on every record

**Date:** 2026-08-02 · **Class:** Fix + land + prove unattended · **Spend:** **$0.0024** on the records of a **$0.10** budget; `spend.json` delta **$0.0000**

Preconditions read before any write: `tools/claims_read.py --holders` per target **and**
`git status --porcelain` with the columns read separately. Claimed as `MEMEBOT-072`, nine
repeated `--write` flags, one advisory conflict accepted and recorded below. Ledger backed
up (`scratch/mb072_runs.pre.bak`, 202 lines) before the run.

**The one number: 4 → 21.** Every window the operator marked by ear is now reachable. The
unattended run at `n=4` produced four finished videos on **four windows that had never been
played**, and **every record joins**.

---

## 0. THE CONFLICT, AND WHAT ACTUALLY HAPPENED

`clippershq/clip_pipeline.py` was held by **BL-899** (stale, 914 min) and **BL-958** (active,
293 uncommitted insertions). The brief ordered the patch landed, so I did not edit the file
in place — I staged **only my own hunks** with `git apply --cached` against a HEAD-relative
patch, leaving BL-958's uncommitted work in the worktree and out of my commit.

**BL-958 committed while I was applying.** That is exactly the race the technique exists for,
and it came out clean: `git show HEAD:clippershq/clip_pipeline.py | grep -c` for my
identifiers returns **0** across both of their commits, and my staged diff contains all of
mine. Two rounds landed in one file within a minute of each other and neither lost a line.

---

## 1. ROTATION — the counter is DERIVED, not stored

`pick()` orders least-used-first on `hook["uses"]`. `pick_song` passes `count=False`, which
is correct — the store is the operator's file. **Nothing else ever incremented those
counters either.** All 21 hooks sat at `0`, `pick()` returned `h1` for a mood every single
time, and **17 of the 21 windows marked by ear could never be selected.**

### The obvious fix is the one BL-888 already caught

`count=True` + `save()` moves the counter at PLAN time. The dashboard polls `render_plan()`
every 5 seconds — ~1,440 phantom uses a day against clips nobody rendered. Any fix of that
shape has to be defended by every future caller remembering not to plan speculatively, and
**a preview, a dry run and a dashboard read all look exactly like a render to a planner.**

**So the counter is not stored at all. It is counted from the ledger** — which records
exactly one thing: renders that really happened.

| property | how it is achieved |
|---|---|
| a dashboard poll cannot advance rotation | it writes no ledger record. **By construction**, not by discipline — there is no flag to get wrong |
| `scratch/songs.json` is never written at run time | half an hour of hand-marking cannot be corrupted by a render |
| the count survives a crash mid-render | it was never held in memory to lose |
| a `dry_run` plans without advancing anything | free, no special case |

It counts **distinct records, not lines** (`record_id_for()` keys on the output path; one
render writes both a `pending` and an `ok` line, and MEMEBOT-060 already found 48 lines
standing for 22 records), and **only `status: ok`** — a window that was never played has not
been sampled.

### Measured

```
store keys (hand-marked windows) : 21
reachable WITHOUT the fix        : 4     0.427-18.701  7.828-22.714  9.857-19.466  13.769-29.369
reachable WITH the fix           : 21
still unreachable                : 0
200 plans moved the counter      : False        <- BL-888's property, held
```

---

## 2. THE PATCH LANDED, AND THE RANKER NOW REACHES SERVABLE CLIPS

Both hunks of `scratch/mb067_clip_pipeline.patch` are at HEAD.

**Hunk B — `servable_by()` + a stable re-order in `rank_candidates`.** 1,508 of 1,751 gated
clips park and the first the matcher can serve sat at **rank 55**, while `run_batch` cuts to
`n × 3`. Measured on the real library at the `n` actually used:

```
library 2003 clips -> top 12 candidates: 12 SERVABLE   (5.36s to rank)
  the same top 12 WITHOUT the fix:        0 servable
```

The re-order is **stable and drops nothing** — parked clips sit behind the servable ones
rather than being cut, and a library with no servable clip renders exactly as before.

**A defect my own patch had, found by the test written for it.** `song_library.load()`
returns a *fresh empty store* for a missing file rather than raising — deliberately, so a
first run needs no setup. `servable_by` swallowed that: with an unreadable store every clip
parks, the predicate reports **nothing** servable, and the re-order puts the parked clips
back in front **while looking like it had decided something**. It now returns `None` (no
predicate, order untouched) when the store holds no songs. That is precisely the failure the
function's own docstring warned about, written by the person warning about it.

---

## 3. THE NO-REPEAT FALL-THROUGH — conditional, not disabled

It discarded **60 of 60** real store matches for a corpus track, and **0 of 17** corpus
tracks are in the store, so every diversion produced a record that joins nothing.

The fall-through now requires a corpus track that **could** join. When none can, the match is
kept and `repeat_forced` records it. **It is not disabled**: a corpus whose track is in the
store is still a legitimate alternative and the rule still takes it — asserted by its own
test, because "fixed" and "switched off" look identical from the outside.

And with rotation seeded, **a repeated song is no longer a repeated window**. All four
renders below logged `song_repeat_forced` — the old code would have sent all four to the
corpus; instead each was kept and each got a window nothing had played.

---

## 4. THE UNATTENDED RUN — real library, real ranker, no explicit song

`n=4`, `library_root=./clip_library` (2,003 clips, nothing filtered), **no `explicit_song`**.

```
status   tier      song      hook  window            resolves  joinable
ok       matched   sng_0004  h2    29.13-53.405      True      True
ok       matched   sng_0003  h2    43.118-58.389     True      True
ok       matched   sng_0004  h3    46.64-67.015      True      True
ok       matched   sng_0004  h4    66.696-83.49      True      True

finished videos            : 4
DISTINCT WINDOWS USED      : 4   — every one of them new
every record joinable      : True    (8 of 8 lines, pending and ok alike)
every finished key resolves: True
rotation counters after    : 6 windows carry a real render (2 before)
```

**Rotation advanced on every render, inside one batch.** `pick_song` re-reads the ledger per
clip, so render 2 saw render 1's `ok` record: `h2 → h2 → h3 → h4`, never the same window
twice.

Verified off the artefacts, never off an exit code:

| | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| stream | 1080×1920 h264+aac | same | same | same |
| duration | 53.88s | 49.17s | 49.54s | 71.04s |
| mean level | −20.6 dB | −18.3 dB | −25.7 dB | −18.2 dB |
| peak | −0.9 dB | −2.7 dB | −8.8 dB | −0.9 dB — **not silence** |

Wall 633.6s for four. **$0.0024** on the records (4 retrieval calls at $0.0006); the ledger
did not move because no `spend_path` was passed.

---

## 5. THE CORRECTION, CARRIED SO IT STOPS PROPAGATING

> **`explicit_song=` is tier 1 of `pick_song` and returns BEFORE the song store is opened.
> Any proof that uses it proves nothing about the pipeline path.**

MEMEBOT-060 and MEMEBOT-062 both reported the join key proven using it. It proved the record
builder and the normaliser — genuinely useful, and genuinely not the thing in question. It
took **two rounds and three briefs** for that to be spotted, because a run that names its own
song looks exactly like a run that chose one. This round's proof uses no explicit song at
all, which is the only version of the test that can fail for the right reason.

---

## PROOF

| Required | Result |
|---|---|
| `count=False` fixed, rotation past 4 keys | **4 → 21 of 21**, 0 unreachable; counter derived from `status: ok` ledger records |
| persist on a real render only | **200 plans move nothing**; a dashboard poll writes no record, so it cannot count — by construction |
| the ranker patch landed | at HEAD; **12 of 12 servable** in the top `n×3`, **0 of 12** without it; 5.36s to rank 2,003 clips |
| corpus fallback fixed | conditional on the corpus being able to join, **not disabled** — both directions asserted |
| unattended at realistic n, every record joinable | **4/4 finished, 8/8 lines joinable, 4 new windows**, real library, no explicit song |
| the `explicit_song` correction carried | §5 |
| suites | **130 of 131 green, 4,615 checks** (1,020s, 10 rounds in flight). The one red, `test_claims_manifest.py`, **passes 30/30 standalone, twice** — it recorded 24 checks in the full run against 30 standalone, because it reads `git show HEAD:` and my own three commits landed inside that window. `test_hook_rotation.py` **17/17**, `test_pipeline_join.py` 16/16, `test_join_key.py` 11/11, `test_clip_pipeline*.py` all green |
| campaigns | `8e02f8d6f6307ae8` (sort_keys) **and** `7a029ee5447cddd8` (compact) — both **MATCH** |
| config.json | parses, **161 keys, 5 campaigns** |
| budget | $0.10 allowed; **$0.0024** on the records, ledger delta **$0.0000** |

---

## Method / limits

**Rotation is now derived from `status: ok`, so a FAILED render is not a use.** That is a
behaviour change and it is arguably more correct — a window nobody heard has not been
sampled — but it means a run of failures leaves rotation standing still rather than moving
on. Worth naming rather than discovering later.

**The counter is per (song_id, hook_id), so renaming a hook_id resets its rotation.** The
join key is `song@start-end` and does not care, so evidence is unaffected; only the ordering
restarts.

**Three of the four renders drew `sng_0004`.** Rotation fixed the WINDOW problem, not the
SONG one: `hype` still carries 87% of matches behind one usable track (MEMEBOT-064). More
`hype` songs remain the highest-value purchase, and that is the operator's call.

**`MIN_DURATION_S` is still 5.0 against edit.py's 8.0s floor** — MEMEBOT-064 reported it and
it is still open in `clip_pipeline.gate`. It did not bite this run because every candidate
was long, but it still pays to retrieve clips that cannot ship.

**BL-958 and BL-899 still hold `clip_pipeline.py`.** BL-958's work is committed; BL-899 has
been stale for 15 hours. I wrote the file against a live advisory claim and said so in my
own claim before starting.

**One suite was red and it is mine to explain, not to blame on the neighbours.**
`test_claims_manifest.py` verifies every manifest against `git show HEAD:`, and my three
commits landed inside the 1,020-second run — it saw a manifest whose code was one commit
away. It passes 30/30 standalone, twice. The honest statement is *"a self-inflicted
live-writer artefact"*, not *"a flake"*: running a full suite while committing is a thing
I did, and it is cheaper to name than to re-run.

**Not measured here:** whether the audio in those four files is the marked window. The
record says which window was configured and `volumedetect` says the audio is real;
cross-correlating the rendered audio against the track is MEMEBOT-066's claim.
