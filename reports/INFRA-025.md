# INFRA-025 — closing the silent-zero class

**The shape.** A failure yields an empty or zero value **indistinguishable from a true,
benign answer**. It is the most expensive recurring defect in this project, it was still
producing new instances today, and every previous instance was found by a different round,
one at a time, after the fact — because each one looked like a clean pass.

This round swept both repositories for it by AST, ranked every hit by what it would wave
through, fixed the top ten, proved each fix **both ways**, and planted a permanent guard so
the eleventh goes red on arrival.

---

## SUMMARY

```
SHIPPED     15 silent-zero sites fixed across 10 modules; an AST sweep tool, a permanent
            shape guard (15 tests) and 33 both-ways proofs; the rule in PRECONDITIONS.md
ONE NUMBER  3,386 hits ranked -> 210 DOLLARS / 420 CORRECTNESS / 2,756 noise
OFF-BRIEF   #1 by consequence (clip_pipeline._ledger_total) is BL-1013's LIVE claim -- not
            touched; ranked and cited to them instead
GOT WRONG   over-tightened reconcile() to raise on an ABSENT ledger; turned
            test_killed_runs.py red; narrowed to FileNotFoundError and it went green
STILL BROKEN clip_pipeline._ledger_total (BL-1013), edit.py::_floor_trim_budget
            (INFRA-023), iter_records' torn-line skip (held file),
            tests/bl932_probe_67vrvaav.py unparseable (untracked, not mine)
SUITE+SPEND 170/171 suites green; the one red is the bl932 probe above. $0.00 -- no paid
            calls, spend.json and config.json never written
```

---

## 1. The sweep: AST, never text

`tools/silent_zero_sweep.py`, five detectors, both repos (`memebot/` is nested and was
walked as part of the tree).

**Resolved by AST on principle.** INFRA-018's rule: a text sweep for text-matching guards
once matched its own subject matter and returned 201 hits of its own data.

| detector | the question it asks | hits |
|---|---|---|
| A | an `except` resolving into a permissive default | 455 |
| B | a subprocess read with no return-code check | 15 |
| C | a file read whose failure path is empty / 0 / None | 63 |
| D | a `.get()` on a missing key feeding a decision | 2,749 |
| E | error path and success path returning the same constant | 104 |
| | **total** | **3,386** |

### Ranked by consequence — from AST location, not from finding text

| tier | rule | count |
|---|---|---|
| **DOLLARS** | the site is on the money path | **210** |
| **CORRECTNESS** | it gates a publish, a commit, or "is this file free" | **420** |
| noise | everything else, plus `tests/` and `scratch/` | 2,756 |

**A survey is not a guard.** 3,386 is a hypothesis generator; a 3,386-entry baseline is
unreadable and churns on every diff. The *enforced* rule is separately derived — see §4.

---

## 2. The top ten, by what each would wave through

**#1 was already owned, and was not touched.** `clip_pipeline._ledger_total` /
`resolve_budget` — the unreadable ledger that made the lifetime cap fail open 50× — is
**BL-1013's live claim** (started 23:17, holding `clip_pipeline.py`,
`test_vision_failure_reason.py`, `test_cap_fails_closed.py`).
`memebot/scraper/edit.py::_floor_trim_budget` is **INFRA-023's**. Both named, neither
written.

### DOLLARS

| site | returned | what it waved through |
|---|---|---|
| `main.load_spend` | `{}` | **Strictly worse than a misread.** `_record_spend_locked` calls this, mutates the result and **writes it back** — one torn read replaces the lifetime ledger with a single run's cost. Separately, the pre-flight cap (`:681`) and the IG profile cap (`:4887`) read `total_spent_usd` off it, so both fail open. |
| `run._spend_now` | `0.0` | The third instance of the `_ledger_total` shape. A status file reports `$0.0000 spent` for a run that spent real money — in a function whose own docstring argues that a confidently-wrong money number is worse than an absent one. |
| `run._leads_now` | `0` | One half of a **subtraction**. A zero on the "before" side makes the delta the negative of the starting total: a run that found leads reports destroying them. |
| `spend_ledger.reconcile` | `{}` | `total $0.00, 0% estimated, 0 runs` — the most reassuring output the function can produce, printed for a ledger it never read. |
| `spend_ledger.read_marker` | `{}` | `completed()` → `False`: a **finished run reported as killed**. Exactly the BL-822 conflation that cost a $0.0060 double-count. |
| `IncrementalMeter.flush` | `False` | The same `False` for "nothing pending", "not due yet" and **"the write failed"**. Dollars going unmetered looked identical to an idle meter. |
| `dashboard._read_ledger` | `{}` | An unreadable ledger rendered as a healthy, empty one (`available: true`, 0 videos). **And the caller was already correct** — `_ledger_state` has the right `unavailable:` handler, and it could never fire because the callee swallowed the exception one frame below it. |
| `dashboard.config_version` | `''` | A cache key that is *stable* when the file is unknown ⇒ "config unchanged" forever ⇒ stale values served, by a function whose docstring says it should stop and show the operator what moved. |

### CORRECTNESS

| site | returned | what it waved through |
|---|---|---|
| `claim.dirty_declared` | `[]` | `[]` here is a **clean bill of health** — `end` uses it to decide nothing is uncommitted. A claim file caught mid-write (fourteen rounds in flight) read as "declared no paths", for exactly the round most likely to have uncommitted work. |
| `commit_guard.check` | `[]` | A torn claim made every staged path "outside your own claim" — a refusal blaming the author for files they *did* claim. **The dangerous part was the fix:** raising out of `check` landed in `main`'s crash handler, which deliberately returns 0, so a torn registry would have **waved a commit through while printing the word CRASHED**. Routed to the existing fail-closed `RuntimeError` clause instead. |
| `repo_paths.git_common_dir` | `None` | "not a repository", "git is not installed" and "git failed" all collapsed into one `None`, which callers read as the first ⇒ a CWD-relative `.claims` no other round reads. A **silent registry split**, in the module whose entire job is preventing that. |
| `decision_log.write` | `[]` | Read-empty then write-back **is a delete, not a read failure**: an unreadable `runs.json` was rewritten from `[]`, erasing every run in it. The outer handler then reported success, because the write itself worked perfectly. |
| `main.setup_logging` | `{}` | Value-based **secret redaction** silently degraded to pattern-only. The first anyone would know is a key sitting in `logs/run.log`. |
| `main.save_config` | `{}` | Cosmetic (relative vs absolute paths) but silent: every path in a shared config rewritten with no explanation. |
| `claim.start` | `{}` | Message only — the refusal never depended on the read. But `started ?, 0 path(s)` reads like a stub claim worth stealing, when what it actually means is that the round is **writing its file right now**. |

---

## 3. The rule, and the two ways it is easy to get wrong

> **An unknown must RAISE. It must never resolve to a permissive number.**

`clippershq/stillness.py` already owned this doctrine for *programs* — `run_checked()`
refuses to hand back stdout unless the process exited 0. **`UnreadableInput` extends it to
*files*** and subclasses `ToolFailed`, so the handlers that already say "I could not look"
keep working unchanged. In `tools/`, the fixes raise `RuntimeError`: the tree's established
blindness signal, which `commit_guard` already treats as a refusal rather than as a crash.

**The distinction the whole class turns on is the WIDTH of the handler:**

```python
except FileNotFoundError:              return {}    # LEGAL — absent really IS zero
except (OSError, ValueError) as exc:   raise UnreadableInput(...)   # the defect, fixed
```

**Mistake 1 — over-tightening.** Making `reconcile` raise on `FileNotFoundError` turned
`tests/test_killed_runs.py` red: an absent ledger genuinely *does* reconcile to an empty
report. Narrowing is the fix; narrowing too far breaks real callers.

**Mistake 2 — assuming raising is always right.** Three sites must continue (a cosmetic
default, a redaction seed, a config signature). The class is the ***silent*** zero, so those
now degrade **loudly**. That is encoded as a property of the code rather than an allowlist:
`_handler_is_loud` treats a handler as non-silent if it logs **or** if it binds the
exception and uses it — and every measured instance of the defect discards the exception
outright. `test_deleting_the_log_line_makes_the_loud_form_fire` holds that claim to its
word: delete the diagnostic and the same module becomes a violation.

**A sentinel only counts if it is distinguishable.** `dashboard._library_signature` returns
`None` on failure and a 3-tuple on success, and its caller reads that `None` as "could not
look". That is the rule being *followed*, and the detector was taught not to flag it —
a guard that tells people to make correct code worse gets switched off.

---

## 4. The permanent guard — `tests/test_silent_zero_shape.py`

**The enforced rule**, narrow enough to be a real invariant, applied only at boundaries that
spend, gate or free:

> A handler that catches something **wider** than "the thing genuinely is not there" and
> resolves to a permissive constant, in a `try` whose body reads a file or runs a program,
> is a violation.

Shaped by three constraints, each from a round that got the shape of a guard wrong:

1. **Mechanism tested separately from the record** (INFRA-020: a guard written to force a
   list empty *switches itself off when it succeeds*, and nothing says so). `scan_boundary`
   is a **pure function of its inputs** — the enforcing test calls it with the real
   `GUARDED` list and is allowed to come back empty; the mechanism tests call it with
   **plants that must produce a finding**. An empty record and a broken checker cannot look
   the same from outside.
2. **Every refusal paired with an acceptance.** Six legal forms are asserted *not* flagged:
   narrow `FileNotFoundError`, re-raising, loud degradation, a distinguishable `None`
   sentinel, a `try` that reads nothing. A refusal-only test stayed green through an entire
   outage in this repo because the guard crashed on the ALLOW path.
3. **The plant goes in a throwaway `tempfile.mkdtemp()`, never the real tree.** Fourteen
   rounds write this repo concurrently; a plant that races a live writer makes the guard
   flaky, and intermittent red trains people to ignore red. **Nothing under the repository
   is created, mutated or deleted by this test.**

Plus staleness: `GUARDED` must be non-empty, and every path in it must still exist.

**`tests/test_silent_zero_fixes.py` (33 tests)** proves each fix both ways, asserting the
exception type **and matching the guard's own words** — never a bare `assertRaises`, which
has fabricated proofs in this repo twice. Where "absent" is a true zero, that is asserted as
a third case.

---

## 5. Verification

* **Campaigns unchanged:** `7a029ee5447cddd8` (compact separators) and `8e02f8d6f6307ae8`
  (spaced) — the same object under different separators — both reproduced exactly.
  5 campaigns.
* **Config valid**, 161 keys, fingerprint `5fb1a8a2…` — matching what `FINAL_STATE.md`
  records. `test_config_contract.py` and `test_governance_rules.py` green.
* **`spend.json` and `config.json` untouched**, clean porcelain on both. **No paid calls.**
* Exactly the declared files were modified; every target was verified `FREE` via
  `tools/claims_read.py --holders` with clean porcelain before writing.

## 6. Not done, and whose it is

* `clip_pipeline._ledger_total` / `resolve_budget` — **BL-1013**, live and concurrent.
* `memebot/scraper/edit.py::_floor_trim_budget` — **INFRA-023**.
* `clip_pipeline.iter_records` silently skips a torn ledger line — held file, not written.
* `outcome_loop.load_runs` skips unparseable lines, which lowers the computed `rev`; at
  equal `rev` the near-empty row wins. Real, subtler, below the top ten.
* Three secondary dashboard endpoints (`/api/renders`, `/video/{token}`, the rotation panel)
  now return **500** rather than an empty list when the ledger is unreadable. Deliberate: a
  500 is unambiguous and "0 videos" is not. The main tile degrades gracefully with a reason.
* `tests/bl932_probe_67vrvaav.py` is unparseable and **untracked** — another round's probe
  artifact, not mine, and the sole cause of the one red suite.
* The 2,749 tier-D `.get()` hits are a survey, not a backlog. Most are formatters.
