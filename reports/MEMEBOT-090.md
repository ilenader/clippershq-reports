# MEMEBOT-090 — The input-population sweep, and a population hole inside the previous fix

**Round:** MEMEBOT-090 · **Date:** 2026-08-02 · **Spend:** **$0.00**, no paid calls
**Claim:** `MEMEBOT-090`, six repeated `--write` flags. `claims_read.py --holders` per target;
`git status --porcelain` read by column — `clip_pipeline.py` and `song_library.py` are both
`' M'` unstaged mid-edit and were **not touched**.
**Commits:** `83c8b7e` (sweep + closure), `8375777` (the instrument's own tests).

Acts on [MEMEBOT-080](https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/MEMEBOT-080.md).

---

## The instrument failed its own acceptance test twice

This is the part worth reading, because a sweep that cannot find the bug it was built for is
not evidence about anything else it reports.

**Failure 1 — intra-procedural provenance.** The first version resolved argument provenance
inside a single function. The motivating case spans three frames:

```python
def _committed_manifests():                       # tests/test_claims_manifest.py:165
    out = _still.run_checked(("git", …, "ls-tree", …, "HEAD", "--", "docs/claims"))
def test_every_committed_manifest_still_verifies(self):
    manifests = self._committed_manifests()
    for rel in manifests:  vc.parse_manifest(…)   # the guard, three frames away
```

Fixed with a **fixed point over functions that return a population**.

**Failure 2 — I reintroduced MEMEBOT-080's error #1 one level up.** That fixed point keyed
producer functions by **bare name**. `_run` is defined in six modules, so one module's
`clip_library.read_all` lineage propagated onto `publish_report.exists_on_remote` and
`clip_cuts.find_cuts` — neither of which touches the library. Now resolved **qualified** by
`(file, name)` with an import graph.

**And the taxonomy was incomplete**, which is why the case stayed invisible even after the
fixed point landed: neither `git ls-tree` nor the `run_checked` runner was in the producer
list. Both were caught by *reading the output*, not by an assertion — which is exactly the gap
`tests/test_input_population.py` now closes.

### One more correction: tiering was on the wrong axis

The first cut tiered on the **consumer** — "is the caller in `tools/`?" as a proxy for "is
this a real population?" That put this sweep's own reason for existing in the noise tier,
because the manifest guard lives in `tests/`. **A test enforcing rules against the real
repository is a guard on a real population.** Tiering now keys on the **producer**:
real-world (git / filesystem / library) versus hand-written literal.

---

## THE SWEEP

Excluded sets, measured at run time: **3,455 untracked files**, 13 unstaged, 14 uncommitted,
249 untracked/uncommitted `.py`, **4 untracked `.claims`**.

**13 guards fed from a narrowing population** — 8 TIER 1 (real-world), 5 TIER 2 (registry).

| # | Guard @ site | Producer | Cannot see | In set | Verdict |
|---|---|---|---|---:|---|
| 1 | `parse_manifest` / `verify` @ `test_claims_manifest.py` ×5 | `_committed_manifests() → git ls-tree HEAD` | UNTRACKED | 3,455 | **By design, COVERED** by the filesystem sweep |
| 2 | `check` @ `commit_guard.py:295` | `committed_paths → git diff --cached` | UNCOMMITTED | 14 | **FALSE POSITIVE** — the guard's domain *is* the staged set |
| 3 | `parse_manifest` @ `test_manifest_prose_refused.py:106` | `_on_disk() → os.listdir` | SUBDIRECTORIES | 0 | **REAL, OPEN — closed this round** |
| 4 | `scan_source` @ `paid_write_guard.py` | `os.walk` | pruned dirs | 0 | **FALSE POSITIVE** — prunes only `__pycache__`, `.git`, `.venv`, `node_modules` |
| 5 | `scan` @ `test_secret_scanner.py` ×5 | `REGISTRY ALL_PROFILES` | profiles not listed | — | Registry shape; low radius, adding a profile is deliberate |

Two of the four TIER-1 shapes are false positives **with reasons stated**. A narrowing
producer is only a hole when the guard's *domain* is wider than the producer's output — for
`commit_guard` the domain is exactly what the commit will contain, so `git diff --cached` is
not a narrowing bug but the definition of the population.

---

## THE FINDING: a population hole inside MEMEBOT-075's fix

`_on_disk()` was the fix for the original hole — discover manifests from the **filesystem**
instead of the git index, which closed the untracked case. It did so with a **flat
`os.listdir`**, so a manifest at `docs/claims/<subdir>/X.claims` was invisible. *A population
hole inside the fix for a population hole, one directory level down.*

### Proven by planting, in the real population, both directions

Two plants of the **same** prose manifest — the control matters as much as the finding,
because without it a green nested result could mean "closed" or "the harness is broken":

| | Before (`os.listdir`) | After (`os.walk`) |
|---|---|---|
| flat `docs/claims/ZZZ.claims` (control) | exit 1 — **FIRED** | exit 1 — **FIRED** |
| nested `docs/claims/zzz_sub/ZZZ.claims` | exit 0 — **SILENT** | exit 1 — **FIRED** |
| after cleanup | green | green |

`_tracked()` moved to the same key space in the same change — it returned basenames, which was
fine while the directory was flat and silently wrong the moment `_on_disk()` began returning
`sub/X.claims`: two sets keyed differently compare as *"everything is untracked"*.

**The excluded set measures 0** — `docs/claims` is flat today. That makes this **latent, not
active**, and it is reported that way. It was still worth one line: the alternative way to
find it is a round.

### Pinned by the fix, not the bug

`test_discovery_reaches_any_depth` asserts discovery **reaches** a subdirectory. Asserting the
old failure would go green the moment anyone reverted, because a reverted fix reproduces the
old failure exactly. **Rehearsed: with `_on_disk` reverted to `os.listdir`, the new test
fails.**

---

## CARRIED FORWARD, NOT RE-DERIVED

- **The call-graph sweep stands at 0 unreached of 188** (126 called, 54 runner-invoked, 8
  duck-typed), *with its limitation attached*: it cannot see this class, and it marks
  `parse_manifest` CALLED.
- **`vision_control_declined` is HALF consumed.** `song_library.vision_suspect()` reads it;
  `clip_pipeline.dict_of()` drops it; the flag is `None` through the pipeline. A green
  boundary test is not the field being consumed. **Still not fixed here** — both files are
  `' M'` unstaged mid-edit, which is not free regardless of claim age.

## VERIFICATION

| Check | Result |
|---|---|
| `tests/test_manifest_prose_refused.py` | **8/8**; new pin goes RED on a revert to `os.listdir` |
| `tests/test_input_population.py` | **9/9** |
| Plant, before → after | SILENT → **FIRED**; green after cleanup |
| Sweep acceptance (finds its own case) | **PASS** — 6 rows |
| Stray `ZZZ-*` files / probe dirs after all rehearsals | **0 / 0** |
| `config.json` | unmodified, parses, **5 campaigns** |
| Full suite | **146 pass, 3 red — none mine** |

### The three reds, attributed

| Suite | Owner | Evidence |
|---|---|---|
| `test_dashboard.py` | **INFRA-018** (holds the file) | `test_an_absent_marker_is_unknown_never_failed` — an absent/idle marker reads as `failed`, hiding real runs. Nothing to do with this round. |
| `test_guard_resolution.py` | *transient* | **passes on re-run** |
| `test_suites_parse.py` | *transient* | **passes on re-run** |

My five committed files are `scratch/mb090_*` (3), `tests/test_input_population.py` and
`tests/test_manifest_prose_refused.py` — zero overlap with any of the three. With nine rounds
writing concurrently a suite result is a moment, not a property; two reds that pass on re-run
are a scheduling artefact and are named rather than hidden.

## STILL OPEN — and whose

- **`dict_of()` drops `vision_control_declined`** — one line at `clip_pipeline.py`. That file
  is unstaged mid-edit; not mine to touch.
- **`MEMEBOT-066` / `-077` / `-078` / `-088`** — untracked, claims failing, **correctly
  waiting** (BL-874). Reported by the suite without failing it.
- **My claim did not name `tests/test_manifest_prose_refused.py`**, which I edited. It was
  unheld so nothing was trampled, and `commit.py` flagged it on the record — but the claim
  should have listed it.
