# INFRA-002 — Headless mode for every funnel. Two ran concurrently for 47 seconds; the shared state held; and the first real headless run found a funnel-breaking bug the suite could not see

**Date:** 2026-08-01 · **Type:** Feature + live proof · **Spend:** **$0.0384** of a $0.05 budget
Claimed as INFRA-002 · guarded scope · timestamped backups · `git -C` only
Suite **58/58, 2,475 checks** (+19) · campaigns SHA `8e02f8d6f6307ae8` · config 162 keys

---

## 1. The entry point

```
python -m clippershq.run --funnel spotify --target 700 --cap 0.50
python -m clippershq.run --list
python -m clippershq.run --status
```

Nine funnels: `spotify twitch youtube google_play ig_crawl tiktok repost email_finder clip_walk`.

**The menus are untouched.** `run.py` calls the SAME `control._find_*` functions the menu calls,
with the same config, so there is no second implementation of any funnel to drift out of step.
What it replaces is only the *asking*: control's six `_ask_*` helpers are swapped for
Enter-equivalents that return the current config value — so a headless run takes exactly the
path an operator pressing Enter would take.

**A question the config cannot answer RAISES** rather than defaulting. Guessing is how a
headless run silently does the wrong thing for a week. `_ask_menu` always raises: a menu choice
is never inferable.

## 2. The cost gate

`--cap` is **mandatory and has no default**. A default cap is a number nobody chose, and the
failure mode of "I forgot the cap" must be a run that does not happen.

```
$ python -m clippershq.run --funnel spotify --target 10
  REFUSED: --cap is required. … headless has no human, so --cap IS that gate.   exit=2
$ … --cap -1     REFUSED: --cap must be >= 0.                                    exit=2
$ … --cap 0      REFUSED: --cap 0 means 'spend nothing' … pass --free-only too.  exit=2
$ … --cap 0 --free-only   REFUSED: --free-only is not true of 'spotify'.         exit=2
```

The cap is pushed into the funnel's own `max_run_usd` knob, which is enforced against **real
billed requests**. It works: the first clip-walk run stopped itself at `$0.0204` against a
`$0.02` cap.

## 3. Shared-state safety — measured under two real processes, file by file

Not threads. Two OS processes, so the kernel lock is actually exercised.

| file | mechanism | test | verdict |
|---|---|---|---|
| `master_leads.csv` | `filelock` + atomic replace | 2×, live | **SAFE** — 58,472 rows, every row exactly 71 wide, no ragged rows |
| `spend.json` (`record_aux_spend`) | `filelock` read-add-write | 2 × 60 writes | **SAFE** — 120/120 rows, total exact |
| `spend.json` (`IncrementalMeter`, flush 25) | same lock per flush | 2 × 130 billed calls | **SAFE** — 260/260 calls, total exact |
| `resolve_cache` / seen-caches | locked read-modify-write | 2 × 40 keys | **SAFE** — 80/80 keys |
| `run.log` | append-only, **unlocked** | 2 × 400 lines | **SAFE below ~4 KB lines** — see below |

**The answer to the question that gated this round: `IncrementalMeter` is safe under two
writers.** Each flush goes through `record_aux_spend`, which takes the same cross-process lock
for its whole read-add-write. 260 of 260 billed calls landed and the total was exact.

**`run.log` is the one with a caveat, and I got it wrong first.** My initial check reported
"560 torn lines" — that was **my own bad length assertion** (I compared against 194 chars for a
200-char record), not tearing. Re-measured properly at four widths:

| line width | lines landed | malformed | verdict |
|---|---|---|---|
| 120 B | 800/800 | 0 | SAFE |
| 200 B | 800/800 | 0 | SAFE |
| 4 KB | 800/800 | 0 | SAFE |
| **9 KB** | **753/800** | 0 | **LOSES LINES** |

Real log lines are far under 4 KB, so this is safe in practice. The failure mode above ~8 KB
(Python's buffer) is **lost lines, not torn ones** — which is worse to diagnose, because the
file still parses cleanly. Do not log a multi-kilobyte payload dump from two concurrent runs.

## 4. The status file

One file per run under `scratch/runs/<run_id>.json`, rewritten atomically on every update
(temp → fsync → `os.replace`), so a reader never sees a half file. **One file per run, not one
shared file** — a shared registry would reproduce in miniature the exact contention headless
mode exists to remove.

```json
{"run_id","funnel","status","started","updated","elapsed_s","pid",
 "target","cap_usd","progress","leads","spend_usd","spend_scope","note"}
```

`status` ∈ running / completed / failed / halted_cap. `progress` is `None` rather than a
fabricated fraction — several funnels cannot know their denominator until late, and a
dashboard should divide `leads` by `target`, both of which are real counts.

Proven live: while both funnels were mid-run, a **third** process read both status files and
printed them. That is the dashboard contract working.

## 5. Two funnels at once — the proof

`repost` and `clip_walk`, tiny caps, launched together:

| | status | leads | elapsed | spend (ledger truth) |
|---|---|---|---|---|
| `infra002b-clipwalk` | completed | 0 new | 48 s | **$0.0132** |
| `infra002b-repost` | completed | **2** | 212 s | **$0.0048** |

**47 seconds of genuine overlap.** Afterwards:

- **master**: 58,472 rows, **every row exactly 71 fields**, no ragged rows, repost's 2 rows present.
- **ledger**: 132 rows, `total_spent_usd` **matches the sum of rows exactly**, 0 malformed rows.
- **no lost writes** anywhere.

### Two bugs the live run found, both fixed

**(a) `NameError: name '_w' is not defined` — repost died on entry. This was mine, shipped in
BL-843.** I added `_w.set_run_id(...)` to `run_from_config`, but `import writer as _w` is bound
inside a *different* function (L805). **The suite never caught it because every test injects
`run_fn` and never reaches that line** — the funnel was broken in production and green in CI.
Fixed with a local import. This is the strongest argument in this report for headless mode
existing at all: the first time a funnel was run end-to-end by a machine, it fell over.

**(b) My status file said `completed` for a run that failed.** `_find_repost` catches its own
exception, logs it, and returns normally — so the wrapper saw a clean return and wrote
`completed, 0 leads`. A status file that is confidently wrong is worse than one that is absent.
Fixed by attaching an ERROR-level log handler for the duration of the run: **a funnel that
logged an error did not complete, whatever it returned.**

**(c) A third defect, in my own status file: the spend figure was the GLOBAL ledger delta**, so
under concurrency each run was credited with the other's spend — both files read `$0.0132` for
what was really a `$0.0132 + $0.0048` pair. Now scoped by campaign and start time:

```
infra002b-repost   written (global delta): $0.0180      <- wrong
                   per-campaign (fixed)  : $0.0048      <- correct
```

**Known limit:** two runs of the *same* funnel concurrently share a campaign and would still
split wrongly. The ledger has no `run_id` column, so this cannot be fixed in the status layer.
`spend_scope` on the file records which reading you are looking at.

## 6. The honest ceiling

Measured per-process resident memory:

| process | RSS |
|---|---|
| light funnel (clip_walk, spotify, twitch — no OCR/vision) | **69 MB** |
| heavy funnel (repost / ig_crawl, with easyocr + SigLIP loaded) | **484 MB** |

Free RAM measured **1.56 GB while the pair was running** and 3.46 GB idle — the box has 15.9 GB
total but very little of it free, which is the real constraint. **RAM, not cores, is the bound:**

- ~**3 heavy funnels** at 1.5 GB free; ~7 at 3.4 GB.
- Light funnels are nearly free at 69 MB — a dozen would fit.
- 12 logical cores are not the limit at these counts, but the heavy funnels are CPU-bound
  internally (BL-839 measured OCR at **4.03 s/frame**), so two OCR-heavy funnels will contend
  on cores well before they contend on memory.

**The more important ceiling is not this box.** Spotify's `concurrency: 6` buys only **1.02×
over 3** because MusicBrainz enforces a **global 1 req/sec** limit — a shared external limiter,
not CPU. The consequence for headless mode is the part worth stating plainly: **two concurrent
Spotify runs share that same one-request-per-second budget.** They do not double throughput;
they halve each other. Funnels that contend on an external limiter should be run in sequence.
Funnels on different providers (Spotify/MusicBrainz vs IG/HikerAPI) genuinely parallelise.

---

## Verification

| check | result |
|---|---|
| headless refuses without a cap | **exit 2**, four refusal modes |
| cap enforced live | clip_walk halted itself at $0.0204 vs a $0.02 cap |
| two funnels concurrently | **47 s overlap**, both completed |
| master after | 58,472 rows, all 71 wide, 0 ragged |
| ledger after | 132 rows, total == sum of rows, 0 malformed |
| spend attributed per run | $0.0132 / $0.0048, correct after the fix |
| status file readable mid-run from a third process | yes |
| suite | **58/58, 2,475 checks** |
| campaigns SHA | `8e02f8d6f6307ae8` **MATCH** · config 162 keys |
| spend | **$0.0384** of $0.05 |

## Honest limits

- **`run_id` is still blank on every master row.** The column is in `FULL_COLUMNS` (72) but
  **master's header is 71 and lacks it** — `master_header_status` reads `drift`. So BL-841/843's
  attribution work still does not land in production until master is migrated
  (`--rewrite-master`). I did not run that here: it rewrites a 24 MB file and other agents are
  active. The 2 new rows stayed correctly at 71 fields because `_stamp_run_id` refuses to widen
  a short row — that BL-843 decision is what kept this from corrupting anything.
- **The proof pair was `repost` + `clip_walk`, not `spotify` + `ig_crawl`** as the brief
  imagined. Those two are the cheapest and fastest that between them write master, the clip
  library and the ledger. The concurrency mechanism is funnel-agnostic, but I have not run
  *your* pair.
- **Only `clip_walk` and `repost` have been exercised headlessly.** The other seven are wired
  through the same dispatch and covered by the prompt-suppression tests, but a funnel whose
  config is missing an answer will raise `HeadlessAskError` on first headless use. Expect to
  find one or two of those.
- **`--target` does not reach every funnel.** `email_finder` and `clip_walk` take it as a
  function argument; the rest take it through a config block. Two funnels
  (`ig_crawl`, `tiktok`) have no `confirm_fn` parameter at all, so their internal prompts are
  handled only by the `_ask_*` suppression — untested live.
- **The 484 MB heavy-funnel figure is one measurement of one import set**, taken with the model
  weights already cached. A cold first load will be larger and slower.
- **No dashboard exists.** The status shape is designed for one; nothing reads it yet except
  `--status`.
