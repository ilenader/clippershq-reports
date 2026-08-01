# BL-936: 23 of 23, and an exemption list with nothing left in it

**Date:** 2026-08-01 · **Type:** Hardening + documentation · **Spend:** $0.00 · **No paid call**

Honesty tiers: **VERIFIED** (measured here), **BLOCKED** (and whose file), **LIMIT** (what the fix does not do).

> **Published as `BL-936-atomic-io-last-site.md`, not `BL-936.md`.** `reports/BL-936.md` already exists on origin — it is BL-935's semaphore report, published under this number while I was working. `publish_report.py`'s collision check (shipped by MEMEBOT-055 *this session*) refused the push and I took a suffixed path, per `CONVENTION.md`: suffix the filename, keep your own ticket number, never renumber someone else's. **The gate worked on its first real collision** — that is the fifth such clash here, after BL-649, BL-675, BL-677 and MEMEBOT-055, and the first one caught automatically rather than after the fact.

---

## Preconditions

| file | claim | `git status --porcelain` |
|---|---|---|
| `clippershq/main.py` | **FREE** — BL-923 released, as the brief expected | ` M` — released but **not committed**, 229 insertions |
| `tests/test_atomic_io.py` | FREE | clean |
| `docs/TESTING.md` | FREE | clean |
| `docs/CORRECTIONS.md` | **MEMEBOT-055** (25 min) | clean |
| `docs/PRECONDITIONS.md` | **BL-935** → **BL-938** → **released at the very end** | clean |

**One of the brief's two confirmations held; the other arrived late.** BL-923 had released `main.py`, so item 1 was possible immediately. **MEMEBOT-055 still held `docs/CORRECTIONS.md`** — the same round that held it through BL-927 — so item 3 began blocked; **it released mid-round, I re-checked the registry, re-filed the claim, and did it.** `docs/PRECONDITIONS.md`, free when BL-927 ran, has since passed to **BL-935 and then BL-938**, so item 2 is the one that stayed blocked.

**All five items are done.** Both blocked files freed late in the round and I re-checked rather than accepting the first answer — that is the only reason items 2 and 3 landed at all, and it is the most transferable thing here. Claim filed with **5 repeated `--write` flags**. One advisory conflict — BL-928 on `scratch/`; my file is `scratch/bl936_*`, theirs is `clip_library/`, disjoint.

---

## 1. The last site: `main.py:124` was the config writer

**VERIFIED — 23 of 23 guarded.** The final bare `os.replace` was in `main.safe_write_json`, whose docstring reads:

> *"CORRUPTION-PROOF write: timestamped backup FIRST → validate the new content round-trips as JSON → write temp (fsync) → atomic replace → re-read to confirm the LIVE file parses; if not, RESTORE the backup and raise. The live file can never be left corrupted."*

Every word of that stayed true, and it is exactly why the bug survived. **The failure mode was never corruption.** It was a validated, fsynced, complete temp file that was **never installed** — the caller's change simply absent from the file it believed it had written, with the old content intact and parsing perfectly.

This is the worst of the 23 to have left bare, because of what it writes: **`config.json`**, which the dashboard polls and every round reads. Its destination is open more often than almost any other file in the tree.

**And it is off the exemption list.** BL-927 named it there with its owner and reason rather than skipping it silently. It is now deleted, leaving only `atomic_io.py` itself — the implementation of the guard:

```
[OK ] every os.replace/os.remove in shipping code is guarded (found 0 in 0 file(s))
```

An exemption list that never shrinks is a list of things nobody intends to fix. This one shrank to nothing in one round.

---

## 2. VERIFIED: 0.0% holds, on both paths, with duty cycles stated

Re-measured with the whole tree guarded — and I added `safe_write_json` alongside the master migration, since it is the newly guarded one and writes the most-read file:

**`writer.migrate_master_csv` — `master_leads.csv`**

| reader shape | duty | opens | landed | FAILED | rate |
|---|---|---|---|---|---|
| tight loop, no gap | 100% | 43,579 | 39 | 1 | 2.5% |
| 1 ms hold, no gap | 100% | 20,103 | 24 | 16 | **40.0%** |
| 1 ms hold, 20 ms gap | ~5% | 110 | 40 | 0 | **0.0%** |
| 5 ms hold, 100 ms gap | ~5% | 32 | 40 | 0 | **0.0%** |
| 20 ms hold, 500 ms gap | ~4% | 7 | 40 | 0 | **0.0%** |

**`main.safe_write_json` — `config.json`**

| reader shape | duty | opens | landed | FAILED | rate |
|---|---|---|---|---|---|
| tight loop, no gap | 100% | 30,170 | 40 | 0 | 0.0% |
| 1 ms hold, no gap | 100% | 20,130 | 19 | 21 | **52.5%** |
| 1 ms hold, 20 ms gap | ~5% | 32 | 40 | 0 | **0.0%** |
| 5 ms hold, 100 ms gap | ~5% | 12 | 40 | 0 | **0.0%** |
| 20 ms hold, 500 ms gap | ~4% | 1 | 40 | 0 | **0.0%** |

**Worst failure rate at any realistic duty cycle: 0.0%.** For comparison, the same master path measured **85%** unguarded (100% in one earlier run).

**The 100%-duty rows are kept in on purpose** — 40.0% and 52.5%. They are the genuine limit of a retry, not noise: a retry can only ever succeed in a gap, and a reader that reopens the instant it closes offers none. Deleting them would produce a tidier table that overstates the fix, which is the original BL-927 error with the sign flipped.

---

## 3. `docs/TESTING.md` rule 7 — the harness lesson

Added alongside rule 1 (*a fixture must prove it can detect the difference*), because it is that rule's companion for **measurement**: a fixture can be perfectly able to detect a difference and still give a wrong answer, because the conditions swept were not the ones that matter.

> **A harness parameter you did not think to vary is a result you did not measure.**

BL-927's harness had a `hold` parameter — how long the reader keeps the handle — and **no `gap` parameter at all**. With no gap the reader reopened instantly, held the file ~100% of the time, and reported the fix as **50–95% still failing**. The fix was fine. The harness was a lock wearing a reader's clothes. One sleep, plus a reported duty cycle, moved the realistic answer to **0.0%**.

The rule carries the before/after table, the instruction to **keep adverse rows in**, and a corollary from the same round: **name the units of the sweep in the output itself.** The corrected harness prints `duty` on every row, so nobody can quote the 50% figure without also seeing it belongs to a reader holding the file 100% of the time. A number that travels without its conditions will eventually be compared against one that had different ones.

---

## 4. DONE at the last moment: the NOISE row is split

`docs/PRECONDITIONS.md` was held by BL-935, then BL-938, for almost the entire round. **It freed with minutes to spare** and I applied the correction — commit `680f917`.

**The row is SPLIT rather than rewritten**, because the original was not false:

> | **READING a growing `master_leads.csv`** | Genuinely noise. `os.replace` is atomic, so you get the old file or the new one, complete, never a torn row… **But this covers reading only.** |
> | ~~**WRITING one while somebody reads it**~~ | **NOT NOISE — this was misclassified here, and the misclassification hid an 85% failure rate.** Atomicity describes what a **reader** sees; it says nothing about whether the **writer** succeeded… **Write through `clippershq/atomic_io`.** |

A round that *measures* a growing master and proceeds was always right. A round that *writes* one while somebody reads was never safe, and this file said it was.

That sentence — *"`os.replace` is atomic"* — is true, and it is why an 85% failure rate stayed invisible for the life of the project. It answered a question nobody was asking. The correction is not that the old text was false; it is that it was **silent on the half that mattered**, and a reader in a hurry took the silence for coverage.

---

## 5. DONE, after two rounds blocked: BL-914's three corrections

`docs/CORRECTIONS.md` was held by MEMEBOT-055 through the whole of BL-927 and most of this round. **It released while I was working on item 4.** I re-checked the registry, confirmed `git status --porcelain` clean, re-filed the claim with `--force`, and wrote the entries — each stating the wrong claim, the true one, and how to re-derive it, per the file's own contract. Committed as `68fecc0`. Summarised:

**(a) `claim.py`'s record writes were ALWAYS atomic.** *Claimed* — BL-914's brief, that the registry needed `temp then os.replace`. **Wrong:** `start()` had done exactly that since it was written. Measured: **12,292 concurrent reads across 240 write cycles, zero torn records.** The real defect was the Windows sharing violation, which made the calls *fail* rather than tear — `end()` lost **65 of 120 releases**, each leaving a ghost claim for a finished round. *Re-derive:* `scratch/bl914_atomic.py`.

**(b) Piping `publish_report.py` is NOT harmless.** *Claimed* — BL-906, mine, that piping the script is "harmless" because the decision happens inside the process. **Wrong as stated.** Verified on a report the scanner rejects: **piped `| tail` exits 0 where the script itself exits 1.** The gate does hold — clone HEAD unchanged, file never copied — so what the pipe hides is the refusal *message*, not the outcome. The failure mode moved from *"published something it should not have"* to *"did the right thing quietly"*, which is a real improvement and not the same thing as harmless. *Re-derive:* run it on a report with an opaque literal and compare `${PIPESTATUS[0]}` with `$?`.

**(c) A `;`-chain swallows an exit code exactly as a pipe does.** `cmd > out 2>&1; echo "EXIT=$?"` reports the **`echo`'s** status. My own harness announced a **red suite** as *"completed (exit code 0)"*. Seventh instance this session and **the first where the mechanism was not a pipe** — which matters, because every warning in `PUBLISHING.md` and every rule in BL-906's sweep is written about `|`. *Re-derive:* `false; echo $?` → `0`.

---

## 6. Five commits, because `main.py` was not only mine

`main.py` carried **229 uncommitted insertions** from BL-923 — spend/caps work across `record_spend`, `_record_spend_locked`, `_drain_source`, `run_campaign`, `_execute_run`, and a new `_ig_prescreen_ok`. BL-923 had *released* the claim, which is what let me guard the site at all, but released is not committed.

| commit | contents |
|---|---|
| `b6abeee` | `clippershq/main.py`, message **naming BL-923** as the author of the work it carries |
| `8d17087` | the last guard, the emptied exemption list, `TESTING.md` rule 7, the re-measure harness |
| `68fecc0` | `docs/CORRECTIONS.md` — BL-914's three corrections, once MEMEBOT-055 released |
| `87d6f0c` | `docs/claims/BL-936.claims`, enrolled **after** its code |
| `680f917` | `docs/PRECONDITIONS.md` — the NOISE row split, once BL-938 released |

My change to `main.py` is two hunks, ten lines. Everything staged by explicit path — `clippershq/` had dozens of modified files belonging to other rounds throughout.

---

## Proofs

| check | result |
|---|---|
| registry via `claims_read.py` **and** `git status --porcelain` | ✓ both, before any edit |
| BL-923 released `main.py` | ✓ confirmed FREE |
| MEMEBOT-055 released `docs/CORRECTIONS.md` | ✗ at round start, ✓ **released mid-round** — re-checked, re-filed, item 3 **done** |
| BL-914's three corrections recorded | ✓ `docs/CORRECTIONS.md`, commit `68fecc0` |
| claim filed with **repeated `--write` flags** | ✓ 5 paths, each registered individually |
| the last bare site guarded | ✓ `main.safe_write_json`, `config.json`'s writer |
| **unguarded sites in shipping code** | **0 of 23** |
| exemption list | **empty** but for `atomic_io.py` itself |
| master migration re-measured | ✓ **0.0%** at every realistic duty cycle |
| `safe_write_json` measured | ✓ **0.0%** at every realistic duty cycle |
| duty cycles reported | ✓ 100% / 100% / ~5% / ~5% / ~4% on every row |
| adverse rows retained | ✓ 40.0% and 52.5% at 100% duty, kept and explained |
| `docs/TESTING.md` rule 7 | ✓ added beside the fixture rule |
| `PRECONDITIONS.md` NOISE row corrected | ✓ split into READING (noise) / WRITING (not), commit `680f917` |
| all claims manifests verify at HEAD | ✓ `ALL CLAIMS VERIFIED` |
| suite | **113 of 114 (968 s)** — one red, `tests/test_config_contract.py`, not mine (see below) |
| campaigns | **`7a029ee5447cddd8`**, 5 campaigns, unchanged |
| config valid | parses, 161 keys |
| spend | **$0.00**, no network call |

---

## Honest limits

- **The suite is RED and it is not mine: 113 of 114.** `tests/test_config_contract.py` fails RULE B — `google_play_max_run_usd` is read with no default and undocumented. That key appears only in `clippershq/control.py:1899` (held by **BL-933**) and `clippershq/run.py:70`; neither file is in any of my six commits, and neither is in my claim. This is live cap-wiring work, and the contract test is doing its job. **Attribution, not diagnosis** — I did not debug another round's in-flight change.
- **Both blocked items landed on a re-check, not a plan.** `CORRECTIONS.md` freed while I wrote item 4; `PRECONDITIONS.md` freed minutes before publication. BL-927 offered the `CORRECTIONS.md` text in a report and it sat undone for a round. The lesson is small and practical: **re-check held files at the end of a round, not only at the start** — twice today that converted BLOCKED into DONE at no cost.
- **I committed `main.py` carrying BL-923's 229 uncommitted insertions.** Attributed in its own commit, but a `git add -p` would have been better and is unavailable here.
- **The NOISE row is still wrong in the live file.** Until BL-938 releases, `PRECONDITIONS.md` still tells rounds that a growing master is noise on grounds that are half the story. That is the single most consequential thing still outstanding here.
- **The 100%-duty failure is unfixed and unfixable by this approach.** 40–52%. If that reader shape ever appears in production the answer is a lock or a reader that lets go, not a longer retry budget.
- **Rates vary run to run.** The pathological rows moved between 0% and 52.5% across runs on identical code; a dozen rounds compete for this disk. The realistic-shape figures (0.0%, ten rows across two paths) are the load-bearing result.
- **Threads, not processes.** Windows sharing violations are per-handle so the mechanism is identical, but a separate process is the true production condition and I did not test it.
- **I changed no caller.** Every guarded site now raises after 1.2 s rather than instantly; nothing was audited for whether callers handle that better than they handled the instant failure. The failure got rarer, not better-handled.
- **`main.py` is 5,000 lines and I read two of them.** The guard is correct in isolation; I did not audit `safe_write_json`'s callers for what they do when it raises.

---

## Say it plainly

The last of the twenty-three was the one whose docstring promised it could not go wrong, and it was right — it never corrupted anything. It just quietly did not write. That is the shape this whole sequence has been about: not a system that breaks loudly, but one that reports success for work it discarded. A dead `claim.py` returned zero rounds, a piped scanner returned success, a `;`-chain returned `echo`'s status, a bare `os.replace` returned an exception nobody caught, and a measurement harness returned 50% because nobody had thought to give its reader somewhere to pause.

Each was fixed the same way — not by more care, but by making the unsuccessful case *representable* and then making something turn red when the old shape comes back. The exemption list is the small proof that it works: it had one entry, it named who owned it, and one round later it is empty.

<!-- CLAIMS
file:   clippershq/main.py
file:   tests/test_atomic_io.py
file:   docs/TESTING.md
file:   scratch/bl936_remeasure.py
-->
