# MEMEBOT-075 — The manifest faults swept, and "untracked" turns out to be three states

**Round:** MEMEBOT-075 · **Date:** 2026-08-02 · **Spend:** **$0.00**, no paid calls
**Claim:** `MEMEBOT-075`, eighteen repeated `--write` flags, *"18 path(s) registered individually"*.
`claims_read.py --holders` run per target; `git status --porcelain` checked.
**Commits:** `69b1b33` (code), `33af537` (docs/TESTING.md), `16de306` (enrolments).

Acts on [MEMEBOT-070](https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/MEMEBOT-070.md).

---

## The brief's item 1 was already done, and the red was a different one

BL-965 fixed the MEMEBOT-067 failure in `7ec702d` and added **four** stale-header recurrence
tests. They hold `tests/test_claims_manifest.py`, so I did not touch it; my sweep test lives
in a file I own.

The suite was still red — on **`docs/claims/MEMEBOT-065.claims`**. Three functions
(`crashed`, `check`, `live_claim`) stopped verifying at `scratch/mb065_clone.py` because
**MEMEBOT-069** (`cdc4ec4`) promoted the clone rehearsal into `tests/test_clone_rehearsal.py`
so `run_all.py` would actually execute it. **Re-pointed, not deleted** — deleting the claims
would have turned the suite green by *removing* enforcement, when the functions still exist
and still matter. All nine claims verify now.

> **The general shape:** moving a claimed symbol breaks a claim in **another round's**
> manifest, and it surfaces under *that* round's name. That is why two rounds in a row
> reported this red as "not mine". Before promoting a file out of `scratch/`, grep
> `docs/claims` for its path.

---

## MEMEBOT-067's header was still false — and the suite structurally cannot see that

The brief's premise checked out. I measured it directly:

| Claim | Result |
|---|---|
| `file memebot/scraper/run_record.py` | **OK** — tracked at HEAD of `memebot/` |
| `func …::annotate_joinable` | **OK** — `def` at :77 |
| `func …::record` | **OK** — `def` at :116 |

So the header sentence *"a memebot path can never verify no matter how thoroughly it is
committed"* is **wrong**, and `verify_claims` resolves against the owning repo
(`_nested_repo_for`). The header did not merely age badly: it **withheld the round's headline
deliverable from enforcement** on the strength of a limitation that no longer existed. Header
corrected; the two functions are now claimed. Enforcement went **up**.

**Why no test caught it, which is the part worth keeping.** BL-965's `denial_is_out_of_scope()`
correctly stopped flagging this header, because the denial named a path the manifest did not
claim — an explanation of an absence, not a stale caveat. That exemption is right. But it
means a header can be **factually false and still pass**, as long as it is false about
something unclaimed. The check compares a caveat against the **claim list**; nothing compares
it against the **world**. That gap is a human read, and this was one.

---

## The silent absence: nothing reads an untracked manifest

`parse_manifest` already refuses prose loudly — it raises `ManifestError` naming the line.
**`tools/verify_claims.py` needed no change.** The failure was never that the parser was
quiet. It was that **nothing called it**:

- `test_every_committed_manifest_still_verifies` iterates `git ls-files -- docs/claims`.
  An untracked file is not in that list.
- `verify_claims.py --enrolling` runs from the pre-commit hook against **staged** paths. A
  manifest never `git add`ed is never staged.

So a manifest written, left untracked and forgotten is checked by **nothing**. It does not
fail — it is **absent**, and absence looks exactly like "this round had no claims to make".

`tests/test_manifest_prose_refused.py` therefore walks the **filesystem**, not the index.
Proved it can fire: planting a two-line prose manifest turns both sweep assertions red, naming
the file and the offending line.

---

## "Untracked" is three states and only one is a defect

This is the finding I did not expect, and it changed the sweep:

| State | Meaning | Verdict |
|---|---|---|
| untracked + **unparseable** | invisible; would fail the moment anything looked | **DEFECT** |
| untracked + claims fail | waiting for its code — **BL-874** | **CORRECT** |
| untracked + claims hold | never enrolled | **READY**, report don't fail |

A sweep that called all three a fault would push rounds to enrol early — exactly what the
guard exists to refuse. So the test asserts **one** thing (every `.claims` file parses) and
*reports* the other two without failing.

---

## THE SWEEP — all 41 manifests

**Zero faults.** Every fault found is fixed or correctly classified:

| Round | Fault found | Resolution |
|---|---|---|
| **MEMEBOT-065** | BROKEN_CLAIM ×3 (tracked ⇒ enforced ⇒ red) | re-pointed to `tests/test_clone_rehearsal.py`; 9/9 verify |
| **MEMEBOT-067** | header factually false | corrected; +3 claims, all verify |
| **MEMEBOT-068** | **PROSE** — 0 kind-prefixed lines | converted; code committed; **15/15 verify**, enrolled |
| **MEMEBOT-066** | invalid `class:` kind disabled all 8 claims | fixed to `func:`; **left untracked** — 6/8 still fail, BL-874 |
| **MEMEBOT-033** | none; well-formed, never enrolled | **8/8 verify**, enrolled |
| **MEMEBOT-077** | untracked, code not landed | correctly waiting (another round's, untouched) |

### I got the stale-header count wrong first

My first sweep reported **six** stale headers — MEMEBOT-009, 021, 025, 027, 033, 067. **All
six were false positives.** I had scanned the whole file for denial phrases and skipped the
two exemptions the suite applies: the *correction marker* (a correction **quotes** the thing
it retracts, so flagging it punishes the fix) and *out-of-scope*. Header-only, with both
exemptions mirrored, the true count is **zero**. A sweep that disagrees with the check it is
auditing is measuring itself, so the corrected sweep now prints the exempt cases explicitly as
"would be a false alarm".

---

## THE MEME RULE'S ACTIVATION PACKET — complete

All four keys present; store validates **clean**; `vision_rules` 4, `songs` 4; vocabulary at
10 tokens. Impact: **unparks 130**, loses-a-song **0**, one known trade.

**The operator's exact steps:**

1. Drop the mp3 at `memebot/scratch/song05_meme.mp3` and measure `duration_s` with `ffprobe`.
2. Mark the hook windows **by ear**: `python hookmark/server.py`. Never guess them — BL-690
   measured automatic drop detection at **100% fabrication**.
3. Move the rule block from `_pending_vision_rules` into `vision_rules`, **LAST**.
4. Paste `_activate` into `songs` and set its `enabled` to `true`.

> **Order matters: step 3 without step 4 parks every clip the rule matches.**

---

## STILL RED — and it is BL-965's file, by my hand

`tests/test_claims_manifest.py::test_the_exemption_is_reached_by_the_live_manifest_it_was_written_for`.

BL-965 wrote it so the exemption "cannot quietly stop matching what it exists for", using the
**live MEMEBOT-067 manifest** as its fixture. By correcting that header I removed the
out-of-scope denial — so the exemption no longer fires there, and the tripwire has nothing
live to catch.

**I did not revert, and I did not edit their file.** Reverting would restore a false statement
and un-enforce two working functions, to keep a fixture alive; and inventing a denial purely
to satisfy the test would be writing a false caveat on purpose. Either is worse than the red.

The honest reading is that **the exemption was written for a condition that has since been
fixed**: there is now no live manifest with an out-of-scope denial, because nested-repo paths
verify. The synthetic fixture directly above it
(`test_the_real_memebot_067_shape_is_exempt`) still covers the logic.

**For BL-965 — one line:** make that test `skipTest` loudly when no live manifest exercises
the exemption, the way it already does when the file is absent. The shape is worth keeping for
the next nested-repo absence; pinning it to a specific round's manifest is what broke.

---

---

## I SHIPPED THE EXACT FAULT I WAS WRITING ABOUT

`tests/test_no_unchecked_stdout.py` went red on **my own new test**, line 73:

```python
r = subprocess.run(("git", "ls-files", "--", "docs/claims"), capture_output=True, text=True)
return {... for p in (r.stdout or "").splitlines() ...}      # no return-code check
```

If `git ls-files` fails for any reason its stdout is **empty**, so the tracked set comes back
empty, **every manifest reads as untracked**, and the state report cheerfully calls the whole
directory unenrolled. *A crashed program's empty output reads as "nothing found"* —
`docs/TESTING.md` **rule 5**, shipped by the round writing about rule 5's cousin. It now raises
with git's exit code and stderr rather than returning a confident empty set. Fixed in `4e697a8`.

Worth stating plainly: I did not catch this by reading my own code. An existing guard did.

## VERIFICATION

| Check | Result |
|---|---|
| `tests/test_manifest_prose_refused.py` | **6/6 pass**; goes red on planted prose |
| Manifest sweep, 41 files | **0 faults** |
| `MEMEBOT-065` / `-067` / `-068` / `-033` | 9/9, 9/9, 15/15, 8/8 verify |
| Store `validate()` | **clean**; `vision_rules` 4, `songs` 4 |
| `config.json` | unmodified, parses, **5 campaigns** |
| `scratch/songs.json` | untouched this round |
| `tests/test_no_unchecked_stdout.py` | **green** after `4e697a8` |
| Full suite | **135 of 138** green; see below |

### The three reds, and whose they are

| Suite | Owner | State |
|---|---|---|
| `test_no_unchecked_stdout.py` | **mine** | **FIXED** in `4e697a8` |
| `test_claims_manifest.py` | **BL-965's file, my hand** | the retired live fixture — see above |
| `test_matcher_boundary.py` | a concurrent round | `dict_of()` drops `vision_control_declined`, a field just added to `song_library.py` in an unstaged edit. My round touched none of `song_library.py`, `clip_pipeline.py` or `songs.json` — verified against my four commits. |

## STILL OPEN

- `MEMEBOT-066.claims` — `class:` fixed on disk but **uncommitted and untracked**, because
  6/8 of its claims fail until its `duck.py` work lands. Its owning round's to enrol.
- `MEMEBOT-077.claims` — another live round's, correctly waiting.
- `BL-901-selftest.claims` — a deliberate NOT-READY fixture; not a fault.
