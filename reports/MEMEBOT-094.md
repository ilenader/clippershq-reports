# MEMEBOT-094 — the ceiling is live: source median 56.3s → 20.00s on every render, through shipped code

**Date:** 2026-08-02 · **Class:** Wiring + orphan rescue + ledger provenance · **Spend:** **$0.0072** of a **$0.15** budget (12 retrieval calls; `spend.json` moved $0.0000 — no `spend_path` was passed)

Preconditions read per target with `tools/claims_read.py --holders` **and**
`git status --porcelain`, second column read as *unstaged mid-edit*. Claimed as
`MEMEBOT-094`, fourteen repeated `--write` flags.

---

## 0. TWO CORRECTIONS TO THE BRIEF, BOTH CHECKABLE

**`scratch/mb086_wiring.patch` is not a patch.** It has **0** unified-diff hunks and no
`diff --git` line; `git apply --check` answers *"No valid patches in input"*. It is a prose
handoff with fenced blocks, and it is a good one — but "land the patch, verify `git apply
--check` first" cannot be done as written. The three blocks were applied by hand.

**Its anchor did not exist at HEAD.** The note places the ceiling *"immediately after the
`_floor_trim_budget` call at edit.py:1271"*. That function had **never been committed**:
zero occurrences at HEAD, and `git log -S _floor_trim_budget` finds it in **no commit**,
although MEMEBOT-064 published it as the fix that took render success from 59.5% to 78.1%.
It had been orphaned in the worktree for about six hours.

This is `docs/ORPHAN_RULE.md`'s case exactly: HEAD was self-consistent without it, so nothing
looked broken, while every measurement quoting 78.1% described code no clone could run. It is
now committed as **MEMEBOT-064** (`1ee7dc7`, `Claim-Override: MEMEBOT-064`) — attributed to
the round that wrote it, not to the one that found it.

---

## 1. THE CEILING, WIRED

Three blocks into `memebot/scraper/edit.py`:

- **`build_transform_filters` plans it AFTER `_floor_trim_budget`.** That call rewrites
  `trim_end` and `speed`, and the ceiling arithmetic is in **output** seconds — it must see
  the values the render will actually use. A test asserts the order.
- **The finished-file check calls `assert_ceiling` beside `assert_floor`**, and **refuses**
  rather than warns. The plan never fails a render because it is optional; a finished file
  *over* the ceiling means the trim did not take effect, and shipping it puts the 55-second
  videos straight back with nothing else measuring length.
- **`_duration_ceiling_s` defaults OFF** — the opposite of the floor, deliberately. The floor
  is the operator's hard minimum and must not be switchable off by forgetting a flag; the
  ceiling is a taste call about length and must not arrive with an upgrade.

`duration.py` had `plan_ceiling`, `assert_ceiling` and `CEILING_S` with **32 green tests and
no caller**. That is what let 30 videos ship at a median 55 s while `CEILING_S = 20.0` sat in
the tree, and it is why the new suite tests the **wiring**, not the arithmetic.

---

## 2. 20 OVER 30 — and not on the payoff labels

| ceiling | payoffs kept | clips kept |
|---|---:|---:|
| 20 s | 26 / 28 | 1,487 |
| 30 s | 28 / 28 | 1,962 |

**28 labels cannot separate those, and the real number is smaller than 28.** Only **11 of the
28 clips are longer than 20 s**, so only 11 can be decided by any ceiling in that range at
all — the other 17 are shorter than the shorter ceiling. The whole 20-vs-30 difference is
**2 clips out of 11 decidable ones**, and MEMEBOT-091 already said the separation was
"defensible but not robust enough for confidence-interval support".

**So the decision rests on the norm instead, and says so.** Both viewing audits measured the
repost band at 7–15 s (MEMEBOT-074, MEMEBOT-089); 30 s is twice its top, and a 30 s ceiling
would leave every long clip at ~30 s — changing almost nothing a viewer notices. The payoff
distribution places the two lost labels in the extreme tail: median 7.0 s, p90 **exactly**
20.0 s, max **exactly** 30.0 s. At 20 s we lose the top decile of payoff positions and we
know precisely which two clips they are.

`_duration_ceiling_s` **derives** its default from `duration.CEILING_S` rather than restating
20.0, and the drift test **reads** `config.yaml` and `duration.py` and fails if they part —
neither number is written in the test. The reasoning above is in the test file, because a
constant without its reason gets tidied.

---

## 3. EVERY LEDGER ROW SAYS WHERE IT CAME FROM

MEMEBOT-086's 30 verification renders never reached `memebot/runs.jsonl`, and the reason it
could report that cleanly is that **there was no way to tell them apart if they had**. A
shared append-only ledger with no provenance column gives a test batch two options and both
are wrong: write it and poison the outcome evidence, or withhold it and lose the record that
the renders happened.

`run_record.record()` now stamps `source` on every row — `production` (default), `test`,
`backfill` — with `CLIPPERSHQ_RUN_SOURCE` to tag a whole driver without editing the pipeline
it is verifying. **Nothing is ever deleted**: a test render really happened and the row is a
fact; what the tag buys is that rotation, `bias_map` and the 25-outcomes-per-arm bar can
*exclude* it instead of a future round discovering a quarter of its evidence was a smoke test
with no way to prove which quarter.

Two choices worth naming: the default is `production`, **not** the safer-looking `test` — an
unlabelled row is a real render by a caller that has not been taught the argument, and calling
it a test would drop real outcomes out of the loop, which is this defect inverted. And an
unrecognised tag is **kept, not corrected**: a tag nobody recognises is still more information
than none.

---

## 4. THE CEILING BINDS THROUGH SHIPPED CODE

`clip_pipeline.run_batch` → `edit.py` → `config.yaml`. **No driver arithmetic** — MEMEBOT-086's
30 renders applied the same maths one stage earlier in their own harness, which proves the
arithmetic and not the wiring.

```
ceiling 20.0s, floor 8.0s
source   min/median/max : 29.5 / 56.3 / 86.5
finished min/median/max : 20.00 / 20.00 / 20.00
```

| check | result |
|---|---|
| inside the 8–20 s band | **11 / 11** |
| join key resolves and record `joinable` | **11 / 11** |
| record tagged `source=test` | **11 / 11** |
| configured track present (40–250 Hz, applied window, bounded lag, every other track as the null) | **10 / 11** |

The eleventh is `r = 0.283, margin = 0.096` against a 0.10 margin bar — a **near-miss on the
null margin, not an absent track**. Reported rather than rounded up.

---

## 5. THE SECOND LABELLER PASS, AND HOW FAR IT GOT

**4 of 4 exact agreement, to the second.** Zero deltas, on clips the first labeller rated
`high`, `high`, `high`, `med`.

**The blinding broke, and it broke on the clips that matter.** To find which labels could
decide a 20-vs-30 ceiling I printed the 11 clips longer than 20 s *with* their `drop_s`. Right
question, and it destroyed the blinding on exactly those 11 — a second pass over them now
would be a memory test, not a second opinion. So the blind pass covers clips at or under 20 s,
whose labels I had not seen.

That means: **the labels are reliable where it was possible to check (4/4 exact), and the
ceiling-critical 11 remain single-labeller.** The brief asked me to say so if agreement was
poor; it is not poor, but it is not measured where the ceiling evidence lives, and n = 4 is a
small number to carry.

---

## PROOF

| Required | Result |
|---|---|
| the patch landed | applied by hand — it is not a machine patch (0 hunks); its anchor `_floor_trim_budget` was **never committed** and is now, as MEMEBOT-064 |
| ceiling binding through shipped code | **source median 56.3 s → 20.00 s, 11/11 in the 8–20 s band**, no driver |
| test renders tagged | **11/11 `source=test`**; `production_rows()` excludes them; nothing deleted |
| 20 vs 30 decided and derived | **20**, from `duration.CEILING_S`, drift test reads `config.yaml` + `duration.py`; reasoning recorded in the test |
| inter-rater figure | **4/4 exact** on the blind set; the 11 ceiling-critical clips could not be blinded and stay single-labeller |
| suites | **153 of 154 green, 5,100 checks**; the one red was **mine and is fixed** — see below. memebot: `test_duration` 32/32, `test_duration_ceiling_wiring` 11/11, `test_run_record_batch` 10/10, `test_edit_behaviour` 36/36 |
| campaigns | `8e02f8d6f6307ae8` **and** `7a029ee5447cddd8` — both **MATCH** |
| config.json | parses, **161 keys, 5 campaigns** |
| spend | **$0.0072** of $0.15 |

---

## What I got wrong

**I committed a test's scratch state into the shipped renderer.**
`tests/test_verify_claims.py` appends `def BL921_WORKING_TREE_ONLY_MARKER(): pass` to the
**real** `memebot/scraper/edit.py`, asserts a working-tree-only symbol does not verify, and
restores the file in a `finally`. My `git -C memebot commit -- scraper/edit.py` landed inside
that window — **twice**, because the suite ran twice — so the marker went into HEAD. The test
then failed *for the right reason*: the symbol really was at HEAD. Removed, committed, pushed;
`test_verify_claims` is 6/6 green and `edit.py` parses.

The test is careful — it restores **bytes**, not an equivalent string, with a comment
explaining why. It still cannot defend itself: **a test that mutates a real shipped file is
undefendable against a concurrent commit**, and this repo runs seven rounds at once. The fix
belongs in the test (copy the file, or plant into a temp clone), not in the discipline of
whoever commits next.

---

## Method / limits

**`spend.json` did not move.** The renders cost 12 retrieval calls at $0.0006 = **$0.0072** on
the records; no `spend_path` was passed, so the ledger figure is $0.0000 and the record figure
is the real one.

**The ceiling was proven on clips that exceed it.** The driver asserts at least one candidate
is longer than the ceiling before spending anything — otherwise the run cannot prove the
ceiling binds, only that nothing tripped it. Every one of the 11 finished at exactly 20.00 s,
which is the trim landing on the target rather than a coincidence.

**Nothing here judges whether the videos are now postable.** MEMEBOT-089 found 0 of 21, with
duration ranked third of eight blockers behind the caption and the sliced headline. This
closes the third. The caption builder and the crop are still open and belong to other rounds.
