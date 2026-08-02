# MEMEBOT-092 — The claim namespace and the report namespace are now both checked at pick time

**Round:** MEMEBOT-092 · **Date:** 2026-08-02 · **Spend:** **$0.00**, no paid calls
**Claim:** `MEMEBOT-092`, repeated `--write` flags; amended once with `--force-reason` on the
record. `claims_read.py --holders` per target; `git status --porcelain` read by column —
`clippershq/clip_pipeline.py` is `' M'` unstaged mid-edit and untouched.
**Commit:** `b6a62fa`.

Acts on [BL-983B](https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/BL-983B.md).

---

## The gap was live while I was picking this round's id

Not a reconstruction. Choosing an id for the round that fixes this:

```
MEMEBOT-091   claim registry: FREE      origin/main: reports/MEMEBOT-091.md EXISTS
MEMEBOT-092   claim registry: FREE      origin/main: free
```

Picking "the next free id" by the registry alone would have collided immediately. `start()`
refuses a duplicate by testing `.claims/<id>.json` — but `end()` **deletes that file**, so the
moment a round finishes, its id reads as free while its report is published and permanently
cited under that name.

Four reports were lost this way. MEMEBOT-057's publish-side check has since saved five — but
it fires at **publish** time, hours after the id was picked, when the work is written and the
cheapest way out is a suffix. **`046H`, `064a`, `983B`, `BL-936-atomic-io` are all scars of
this one gap.**

---

## What shipped

`check_id_free()` consults `origin/main` at claim time and refuses a taken id, naming **which
check fired** — the live-claim check and the published-report check have different fixes, and
"REFUSED" alone leaves the reader to guess.

**Both layouts are checked.** MEMEBOT-053 moved publishing into `reports/`; everything older
is still live history at the repository **root**. Checking one layout would leave the *older*
half of the namespace unchecked — the half most likely to hold a forgotten id.

**The refusal suggests the next free id**, computed across both namespaces. A refusal that
costs minutes gets worked around; one that costs seconds gets obeyed:

```
REFUSED by the PUBLISHED-REPORT check: round id MEMEBOT-091 already has a PUBLISHED
REPORT at reports/MEMEBOT-091.md on origin/main.
    Pick a free id — next free in BOTH namespaces: MEMEBOT-092, or pass --force with
    --force-reason if you are deliberately revising THAT round.
```

**`--force` now requires a reason**, enforced in `start()` rather than only in the CLI so no
caller escapes the audit trail, and recorded in the claim as `forced` / `force_reason`. This
round's own amendment used it, and the reason is in the registry.

### The design decision that determines whether any of this works

`publish_report.py` takes `--clone` as **required with no default** — there is no ambient path
to the reports repo. A check that silently did nothing when it could not find one would be
reached on every claim and never see a single collision: **the exact input-population fault
MEMEBOT-090 swept for, shipped fresh.**

So an unresolvable clone is **never** reported as free. Resolution is
`--reports-clone` → `$CLIPPERSHQ_REPORTS_CLONE` → sibling checkout; if none resolves, the
claim records `reports_checked: false` and the CLI prints an unmissable banner:

```
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
PUBLISHED-REPORT CHECK DID NOT RUN — this id was NOT checked against
origin/main. …  Recorded in the claim as reports_checked=false.
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
```

`false` in the record means *not consulted*, not *consulted and free* — a later reader can
tell those apart. And a git **failure** is a third thing again: it **raises**, per BL-950's
rule that *"git could not tell me"* and *"it is not there"* are the same empty string and must
never be the same answer.

---

## The tests — four cases, plus the hazard that comes first

All in a throwaway repo with a real `origin/main`; no network.

| Case | Result | Firing check asserted |
|---|---|---|
| Live duplicate | refused | `DuplicateClaim` |
| **Published but released** | refused, leaves no file | `PublishedIdTaken` |
| Genuinely free id | accepted, records `reports_checked: true` | — |
| `--force` **with** reason | accepted, reason recorded | — |
| `--force` **without** reason | refused | `ValueError` |
| git failure | refused | `PublishedIdTaken` |
| absent clone | **UNCHECKED**, not free | — |
| `next_free_id` with no remote | suggests **nothing** | — |

Every refusal asserts the **exception type**. Asserting only "it refused" would pass if the
wrong check fired.

**The hazard first.** A previous test wrote three real claim files into the live registry
because it set `claim.CLAIM_DIR` and assumed that redirected the writes. It does not —
`claims_dir()` resolves through `repo_paths` against the git common dir, so inside a
repository the module constant is ignored and `$CLIPPERSHQ_CLAIMS_DIR` is the only lever.
So `setUp` **asserts the redirect took before writing anything**, and `tearDown` asserts the
live registry is unchanged. Verified: 12 files before, 12 after.

---

## THE SUFFIX SWEEP — all 45 indexed

Every suffixed report on `origin/main`, checked against `MANIFEST.tsv`:

| | |
|---|---:|
| Distinct report names on origin | 578 |
| …resolving to `reports/` | 564 |
| …existing **only** at the legacy root | 4 |
| MANIFEST.tsv ids | 564 |
| **Suffixed (collision scars)** | **45** |
| **Suffixed missing from the index** | **0** |

Counted by name, so a report present in *both* layouts (a migration leftover) is counted once
and attributed to `reports/`.

`BL-983B`, `MEMEBOT-046H`, `MEMEBOT-064a`, `BL-936-atomic-io-last-site`, `R-1`…`R-6` and the
`BL-676`–`BL-711` legacy block are **all indexed**.

### Off-brief: one *plain* report is unindexed, and the cause is the same fault class

**`BL-864.md`** is on origin with no `MANIFEST.tsv` row, while `BL-863`, `BL-865` and `BL-866`
all have one. Root cause: `gen_manifest.py` enumerates with a flat
`os.listdir(reports_dir)` — it can never *add* a root-level legacy file, so no amount of
regeneration will pick it up. That is an input-population hole in the generator, the same
shape as everything else this line of work keeps finding. **Not fixed here** — changing how
560 reports get indexed is not a side-quest, and the manifest lives in the reports repo.

---

## VERIFICATION

| Check | Result |
|---|---|
| `tests/test_claim_id_namespaces.py` | **9/9** |
| `test_claim.py` / `test_claim_collision.py` / `test_claim_location.py` | **all pass** |
| CLI: published id / no-reason force / absent clone | refused / refused / banner + recorded |
| Live claim registry after all tests | **untouched**, no `ZZTEST` leak |
| `config.json` | unmodified, parses, **5 campaigns** |
| Full suite | **152 pass, 1 red — not mine, and it found real damage** |

### The one red: a test marker is now committed in `memebot`

`test_verify_claims.py::test_it_reads_HEAD_and_not_the_working_tree` proves the checker reads
HEAD by appending a marker function to `memebot/scraper/edit.py`, asserting it does **not**
verify, then restoring the bytes. Under concurrency that is a race against anyone committing
in `memebot/`, and it lost:

```
git -C memebot log -S BL921_WORKING_TREE_ONLY_MARKER -- scraper/edit.py
  1319228  MEMEBOT-094: the duration ceiling is wired into the shipped path …
```

- **memebot HEAD** now contains `def BL921_WORKING_TREE_ONLY_MARKER():` at `edit.py:2980`.
- The working tree has it **twice** (2980 committed, 2984 from a later run whose restore raced).
- So the test now finds the marker *at HEAD*, its assertion correctly fails, and it will keep
  failing until the marker is removed from the nested repo.

`memebot/scraper/edit.py` is held by **MEMEBOT-094**, live, in a separate git repo — not mine
to revert. My commit `b6a62fa` touched neither `verify_claims.py` nor the test, and both are
clean in the working tree. The suite passed this test in my previous round's run.

**The design fault is the test's, not MEMEBOT-094's:** it perturbs a live 118 KB source file
that another round owns. Its own comment shows the hazard was already known — the fix went to
restoring *bytes* rather than to not touching a shared file at all. A scratch copy, or a
throwaway nested repo like the one this round's tests build, has no race to lose.

## STILL OPEN — and whose

- **`BL-864.md` unindexed**, and `gen_manifest.py`'s flat `os.listdir` is why. Reports-repo
  tooling; not this round's to re-plumb.
- **`reports_checked: false` is possible** whenever no clone resolves. That is the honest
  floor of this design, not a bug — but it means the check's coverage depends on the
  environment, and the claim records which way it went every time.
- **`BL921_WORKING_TREE_ONLY_MARKER` is committed in `memebot` HEAD** (`edit.py:2980`, via
  `1319228`) and appears twice in the working tree. `memebot/scraper/edit.py` is held by
  **MEMEBOT-094**. Removing it needs a commit in the nested repo — `git -C memebot`, never a
  parent-repo edit.
- **`clippershq/clip_pipeline.py`** remains `' M'` unstaged mid-edit; `vision_control_declined`
  is still dropped by `dict_of()`. Untouched, as declared.
