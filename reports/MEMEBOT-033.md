# MEMEBOT-033: Blocked again, on a file that turned out to be genuinely busy — and a bug of my own found on the way

**Date:** 2026-08-01 · **Type:** Blocked round + verification + one fix · **Spend:** $0.00 mine · **No paid call**

Honesty tiers: **VERIFIED** (run here), **BLOCKED** (and why), **CORRECTION** (mine).

---

## Verdict first

**`clippershq/clip_pipeline.py` is still held by BL-855 — 194 minutes — so items 1, 2 and 4 are NOT done.** The brief said: confirm all three holders released, and if any still holds it, report and stop. BL-855 has not released. MEMEBOT-030 has; MEMEBOT-032 has not, but it holds `song_library.py`, not this file.

**CORRECTION, and it matters more than the block.** My first read of BL-855 said its artifacts had not moved in three hours and the claim looked abandoned. **That was wrong.** I had looked at `scratch/bl855_backups/` — a directory whose mtime does not change when its siblings do — and at two clippershq files. BL-855's declared namespace is `scratch/bl855_*`, and `scratch/bl855_suite2.out` was written **two minutes** before I checked. **BL-855 is actively running a test suite right now.** The stop was right, for a better reason than the one I first gave.

The tool I built this round is what caught me. That is the most useful thing in it.

---

## What shipped

### 1. A real bug in `edit.py`, and it is mine

**`edit.py --help` has been crashing since MEMEBOT-021.** Found while verifying MEMEBOT-030's work, not while looking for it:

```
TypeError: must be real number, not dict
```

argparse formats every help string through `help % params`. The `--audio-class` help text **I wrote in MEMEBOT-021** contains a literal `63.3% false-negative`; `% f` parses as a format spec and the whole help renderer dies.

**It also broke every argparse usage error.** A mistyped flag printed a traceback instead of usage — the two moments a person most needs the CLI to work were the two it could not. Renders were unaffected, which is exactly why it survived twelve rounds: argparse only formats help when a human asks for it or gets something wrong, and nothing in the suite ever did either.

Fixed (`%%`), commented at the site, and closed by `memebot/scraper/tests/test_cli_help.py` — 4 tests: help renders, a bad flag prints usage not a traceback, `--audio-class` is actually offered, and an AST sweep that fails on **any** future literal `%` in an `add_argument(help=...)`.

### 2. `claim.py brief` — the smallest thing that tells a brief-writer what a round already knows

The gap the brief names: claim.py answers *"is this taken?"* for a **round**, at the moment it starts. It cannot answer it for the person **writing** the brief an hour earlier — and that is where the cost lands. Four consecutive rounds were briefed to fix this one file; each was correctly reasoned, each correctly blocked, the tool worked perfectly every time, and the queue still formed.

```
$ python tools/claim.py brief
IN-FLIGHT CLAIMS  (paste into a brief)  2026-08-01 19:25
  BL-849           249 min  clippershq/clip_library.py, clip_library/, scratch/bl849_label.py   ** nothing written yet
  BL-855           194 min  clippershq/clip_pipeline.py, clippershq/loop_runner.py, +2 more
  BL-875            40 min  tests/test_dashboard.py, tests/test_filelock.py, +2 more   ** nothing written yet
  MEMEBOT-033        5 min  tools/claim.py, tests/test_claim.py, memebot/scraper/edit.py +2 more
  (** = the claim is older than any work under it. Ask the owner; nothing expires automatically.)
```

**It carries a staleness clock, and getting that right is the whole design.** A first version dated each claim by the newest write across *all* its declared paths — and it showed BL-855 as active, because **MEMEBOT-030** had written `clip_pipeline.py` an hour earlier. A shared file cannot date a round. `own_paths()` prefers the round's own namespace (`scratch/bl855_*`, the convention every round here follows) and falls back to everything only when there is none, saying which basis it used.

It **reports** staleness and never enforces it. A long round is not an abandoned one, and only a human should decide which a given claim is — so the flag says *"ask the owner"*, and nothing expires automatically. That is claim.py's existing design constraint and this does not weaken it.

### 3. MEMEBOT-030's wiring — VERIFIED, not assumed

MEMEBOT-031 confirmed the files existed and explicitly did not check they worked. Two gaps file-existence cannot close, both now closed (`scratch/mb033_verify.py`, 28 checks, all green):

| checked | result |
|---|---|
| `render_one()` puts `--audio-class` on a **real argv**, per class | ✓ all four classes |
| a bogus class is **not** passed (argparse would exit 2 and lose the render) and **is** reported | ✓ |
| no class supplied → flag absent, not an empty value | ✓ |
| `edit.py --help` exposes the flag and all four classes | ✓ *(after the fix above — this is how it was found)* |
| `duck.py` routes each class to the right treatment | ✓ mute / mute / keep / keep |
| the argv guard **fails on a planted drop** — argv line deleted | ✓ *"render_one() never puts --audio-class on the command line"* |
| the argv guard **also fails when only the CALL SITE stops passing it** | ✓ *"…so --audio-class never reaches edit.py however well render_one supports it"* |
| the three per-class renders exist, with right treatment and measured levels | ✓ −18.11 / −12.39 / −13.80 LUFS |
| only the dialogue-only source is marked `constructed` | ✓ honest — the corpus has none |

The second planted drop is the one worth noting: it is the **shape of the original three-round bug** — `render_one()` still supports the parameter, nobody passes it. The guard catches that too.

Note what a source-text guard cannot do: it proves the flag is *written*, not that it *arrives*. That is why part 2 above runs `edit.py` itself.

---

## What is NOT done, and whose file it is

| item | state | owner |
|---|---|---|
| 1. the two `"duck-under"` literals (`clip_pipeline.py:774, 790`) | **NOT DONE** | BL-855, 194 min, verified active |
| 2. delete `TREATMENT_TO_DUCK` (line 846) | **NOT DONE** | BL-855 |
| 4. release the file promptly | **N/A** — I never took it | — |

Both remaining fixes are trivial: two string literals and one dict deletion. MEMEBOT-027's invariant test still guards the dead map, and MEMEBOT-031's `expectedFailure` still marks the record defect, so neither can be forgotten — they are both visible in every suite run.

**I did not take clip_pipeline.py at any point**, so nothing here needed releasing. My own claim covered five paths and is cleared.

---

## Proofs

| check | result |
|---|---|
| claim registers each path individually | **hand-verified** against the stored JSON: 5 entries, all comma-free |
| campaigns byte-identical | **`8e02f8d6f6307ae8`** ✓ |
| config valid | parses, 162 keys |
| spend | **$0.00 mine.** `spend.json` moved **$0.0006** during the round (`ig_spent_usd` 3.9798 → 3.9804) — another live round's IG call. I made no network call of any kind. |
| backups | `scratch/mb033/config.json.bak`, `spend.json.bak` |
| credentials | none printed, logged or committed |

### Suites

`run_all.py` buffers and takes ~500-650 s; I waited rather than concluding it produced nothing, as instructed.

- A run completing mid-round, after the `edit.py` fix: **ALL GREEN — 87/87 suites, 3724 checks (497.8 s)**.
- A second run after **every** edit: **87 of 88 suites green (511.0 s)**. The one red is `tests/test_claims_manifest.py`, and it is **not mine**:

  ```
  docs/claims/MEMEBOT-022.claims: const clippershq/song_library.py::TIER_TITLE ... DEAD
  ```

  MEMEBOT-022's committed manifest claims a constant that **MEMEBOT-032 deleted** this afternoon (with an audit behind it: 1 right, 7 weak, 5 wrong out of 13 matches). The suite is doing exactly its job — catching a later round invalidating an earlier round's shipped claim — and the fix belongs to whoever owns that pair. `song_library.py` is held by MEMEBOT-032.
- `memebot/scraper/tests/`: **96 pass** (up from 92 — the four new `--help` tests).
- `tests/test_claim.py`: **57 checks, ALL PASS** (13 new).
- `scratch/mb033_verify.py`: **28 checks, all green.**

---

## Honest limits

- **The main items are undone.** This is the second consecutive round to report that, and the reason is the same file.
- **I got BL-855 wrong first** and would have reported an abandoned claim. Corrected above; the tool built here is what corrected me, which is the best argument for it I can offer.
- **`edit.py --help` was broken by me**, in MEMEBOT-021, and went unnoticed for twelve rounds because no test ran it. The AST sweep now catches the class, not just the instance.
- **The staleness flag is a heuristic.** It compares a claim's age against writes under its own namespace; a round that works entirely in files it shares with others will still read as quiet. It is a prompt to ask, never an authority.
- **I did not re-verify MEMEBOT-030's renders by ear** — I checked they exist, carry the right treatment for their class, and record measured levels. The dialogue-only source remains **constructed**, so that class's real behaviour is still unmeasured, as MEMEBOT-021 first said.

---

## Say it plainly

Four rounds have now been briefed to fix two string literals, and four have been blocked. Nothing is wrong with any of them and nothing is wrong with the tool — the queue forms upstream of both, when a brief is written against a tree that has since moved. `claim.py brief` is a two-minute paste that would have prevented all four, and it is the only part of this round that changes the odds next time. The rest is a bug I put in twelve rounds ago and finally tripped over.

<!-- CLAIMS
func:   tools/claim.py::brief_lines
func:   tools/claim.py::own_paths
func:   tools/claim.py::last_touch
file:   tools/claim.py
file:   tests/test_claim.py
-->
