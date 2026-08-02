# MEMEBOT-107 — The known-state checkpoint

**Round:** MEMEBOT-107 · **Date:** 2026-08-02 · **Spend:** **$0.00**, no paid calls
Read-only on every production module; the only source file written is one flaky test of my
own. Nothing sent; `master_leads.csv` not touched by this round.
**Commit:** `f3863b2`.

**This is the document the next session opens with.**

---

## The wait-condition was satisfied on the first poll

`MEMEBOT-099 — rescue the duck.py orphan; refusal proven from a clean extract` landed on
origin at **22:18**, after the brief. No waiting. Its work is visible at memebot HEAD:
`b28f521 MEMEBOT-066: refuse to guess the audio class instead of silently keeping the source
audio`.

**Bonus, verified:** the `BL921_WORKING_TREE_ONLY_MARKER` that MEMEBOT-092 found committed
into `memebot/scraper/edit.py:2980` is **gone from memebot HEAD**. That one is closed.

---

## 1. TWO PARENT SUITE RUNS — and the tree moved under both

| | Run 1 | Run 2 |
|---|---|---|
| Suites discovered | 159 | **162** |
| Passed | **157** | **160** |
| Red | 2 | 2 |
| Wall clock | 712 s | 944 s |
| Rounds in flight, **start** | **3** | **11** |
| Rounds in flight, **end** | 7 | **13** |

**Neither count is the "quiet tree" number the brief hoped for, and that is the finding.**
The tree went from 3 rounds to 13 in ninety minutes, and gained 3 suite files mid-checkpoint.
A suite count here is a moment, not a property — the runner says so itself, and two runs an
hour apart agree only on that.

### The four reds, each attributed

| Suite | Run | Owner | What |
|---|---|---|---|
| `test_claim_id_namespaces.py` | 1 | **MINE** | flaky assertion I shipped in MEMEBOT-092 — **fixed**, see below |
| `test_dashboard_video.py` | 1 | transient | passes on re-run |
| `test_clip_pipeline.py` | 2 | **BL-1006** | `clippershq/client_delivery.py` (untracked, 22:50) writes to the ledger and is not on the sanctioned-modules list |
| `test_no_unchecked_stdout.py` | 2 | **BL-1011** | `clippershq/audit_labels.py:71` (untracked) reads a subprocess `stdout` with no return-code check |

Both run-2 reds are **live rounds' uncommitted files tripping guards that work**. That is the
guards doing their job, not a broken tree — but a fresh clone would not see either file, so
**a clone is greener than this working tree.**

### The one that was mine

Run 1 went red on `test_claim_id_namespaces.py` and passed on re-run. My MEMEBOT-092
`tearDown` asserted the **whole** `.claims` listing was unchanged, so any other round starting
or ending a claim during the run failed it. With ten concurrent rounds that is a coin flip,
and a flaky red is worse than no check: it trains the reader to re-run until green. Now scoped
to the ids the test itself creates — still catches the failure it was written for, verified by
planting `BL-900.json` in the live registry and watching it go red.

---

## 2. MEMEBOT — live tree vs a clean extract of HEAD

memebot HEAD `4d9980b`.

| | Suites | Tests | Failed |
|---|---:|---:|---|
| **Live tree** | 22 | **870** | **none** |
| **`git archive HEAD`**, nested layout | 22 | 870 | **1 — `scraper/tests/test_font_scripts.py`** |

*(The brief's "229 tests" is the `scraper/` subset, now **242**; `meme/` adds 628.)*

### The extract failure is real, and it is an asset that never gets committed

```
.gitignore:7:  scraper/fonts/*.ttf     ->  scraper/fonts/Inter-Bold.ttf
```

`Montserrat-Bold.ttf` **is** tracked; `Inter-Bold.ttf` is **gitignored**, so it is in nobody's
checkout. MEMEBOT-102 landed the font selection that switches Greek, Hebrew and Arabic to
Inter — and in any clone that font is absent, so `test_greek_hebrew_arabic_switch_to_inter`
fails and the scripts it was added to handle cannot be drawn. **MEMEBOT-102's fix is not in a
clone.** Owner: whoever holds the font work; the fix is a one-line `.gitignore` negation plus
`git add -f`.

### And one failure that was MY harness, not a defect

My first extract put memebot's contents at the tree **root**, and
`scraper/tests/test_edit_bed.py` hardcodes `memebot/scraper/config.yaml` — a path that only
resolves when memebot is nested inside the parent. Re-run with the extract at
`<tmp>/memebot/`, it is **OK**. Reported as a harness artefact rather than a bug, because
that is what it is: memebot's tests assume the nested layout, so a *standalone* clone of
memebot is an untested configuration.

---

## 3. CLONE REHEARSAL — 9/9 in 25.5 s

All four properties present, and the attribution is the point:

- **Control:** hooks are **inert before the installer** — without this, "the hook refused"
  proves nothing.
- **Property 1:** the **legal commit is ACCEPTED** — without this, a hook that refuses
  *everything* passes the suite.
- **Property 2:** each refusal **names the check that made it** (docs/TESTING.md rule 10).
- **A crash is never counted as a refusal.**

The suite also carries its own can-fail tests (`TheRehearsalCanFail`), which pin that refusal
alone still looks like success — the finding, kept executable.

---

## 4. MANIFESTS AND TOOLS

| Check | Result |
|---|---|
| `.claims` manifests on disk | **69** |
| **Tracked (enforced)** | **66 — all verify clean, 0 failing** |
| Untracked | 3 — `MEMEBOT-066`, `-077`, `-078`, all **CORRECTLY WAITING** (BL-874) |
| Unparseable | **0** |
| `test_tools_tracked.py` | **11/11 OK** |
| `test_manifest_prose_refused.py` | **8/8 OK** |

The three untracked manifests are the *correct* state, not faults: their claims fail because
their code has not landed, and BL-874 says a manifest waits for the code.

---

## 5. THE STATE TABLE

### Unstaged (`' M'`) — 5 files, all ORPHAN (no live claim)

| File | Holder |
|---|---|
| `dashboard/static/runs.json` | ORPHAN |
| `scratch/bl864_run.json` | ORPHAN |
| `scratch/bl974_extract.json` | ORPHAN |
| `scratch/bl986_stamp.json` | ORPHAN |
| `scratch/mb075_sweep.json` | ORPHAN |

All five are generated data artefacts, not source. `clippershq/clip_pipeline.py`, which was
`' M'` for most of the day, is now **clean**.

### Staged — 1 file, orphaned in the index

`docs/claims/MEMEBOT-094.claims` has been staged-not-committed for hours. Anyone running a
bare `git commit` would sweep it in; `tools/commit.py` pathspec commits are why nobody has.

### Live claims — 13, with age

| Round | Age | Note |
|---|---:|---|
| **MEMEBOT-039** | **1,586 min** | ⚠ POSSIBLY STALE — files untouched 1,555 min |
| **BL-899** | **1,529 min** | ⚠ POSSIBLY STALE — files untouched 1,527 min; holds `clip_pipeline.py` |
| BL-1000 | 43 min | |
| BL-1001 | 43 min | |
| MEMEBOT-108 | 42 min | nothing written yet |
| MEMEBOT-107 | 32 min | this round |
| BL-1004 | 32 min | |
| BL-1002 | 31 min | |
| MEMEBOT-110 | 31 min | holds `clip_pipeline.py` jointly with BL-899 |
| BL-1003 | 23 min | |
| BL-1006 | 20 min | owns run-2 red #1 |
| BL-1011 | 18 min | owns run-2 red #2 |

**Two claims are >25 hours old and flagged stale.** Nothing expires automatically — `claim.py`
is explicit that staleness is a question for the owner, not a licence to take the file.
`clip_pipeline.py` is claimed by **both** BL-899 (stale) and MEMEBOT-110 (active).

---

## WHERE THE NEXT SESSION STARTS

- **Parent suite:** 160/162 with two reds owned by BL-1006 and BL-1011, both from untracked
  files. Re-run after those land.
- **memebot:** green in the live tree (870 tests); **one real extract failure** —
  `Inter-Bold.ttf` is gitignored and absent from every clone.
- **Hooks:** proven from a clean clone, refusals attributed.
- **Manifests:** the enforced set is 100% clean.
- **Two stale claims** to resolve with their owners before anyone edits `clip_pipeline.py`.

## VERIFICATION

| Check | Result |
|---|---|
| `config.json` | unmodified, parses, **5 campaigns** |
| `master_leads.csv` | **not touched by this round** (0 of my commits); its sha DID move mid-checkpoint — held by **BL-1000**, which is actively rebuilding the send list. The master is live and moving; that is state, not damage. |
| Emails sent | **0** |
| Files I wrote | `tests/test_claim_id_namespaces.py` (flaky fix) + `scratch/` + this report |
