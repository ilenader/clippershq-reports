# MEMEBOT-058: three hooks were inert, and the rule I was implementing broke on me mid-round

**Date:** 2026-08-01 · **Class:** Governance audit + fix · **Spend:** **$0.00**, no paid calls.
**Claim:** `MEMEBOT-058`, seven repeated `--write` flags, *"7 path(s) registered individually"*. `claims_read.py --holders` run per target; `git status --porcelain` checked. **READ-ONLY on production modules** — I wrote `tools/`, `tests/` and one new doc. BL-938 holds `docs/PRECONDITIONS.md` and BL-936/BL-939 hold `docs/TESTING.md` and `docs/CORRECTIONS.md`; I read all three and wrote none.

---

## The headline: the rule proved itself while I was implementing it

While I was building a check for *"commit per round, not per day"*, **BL-936's commit took my in-flight file.**

```
680f917  BL-936: split the NOISE row that hid an 85% failure rate
   docs/PRECONDITIONS.md      <- BL-938's file
   docs/claims/BL-936.claims  <- BL-936's own
   tools/claim.py             <- MEMEBOT-058's, mid-edit
```

Three rounds in one commit, titled for the work of one. I found it because `git add` staged nothing and I went looking for why — my edit was already in `HEAD`. No warning fired, because nothing checks.

`python tools/claim.py staged` now does, and would have named all three.

## 1 & 2. The sweep, ranked by what non-compliance has already cost

Thirteen rules read out of the nine documents by hand and tested against the code that would have to enforce them. **Ten were already enforced.** The gaps, by proven cost:

| # | rule | status before | cost already paid |
|---|---|---|---|
| **1** | the hooks only run if `core.hooksPath` is set | **nowhere** | 3 hooks silently inert in any fresh clone |
| **2** | commit per round, not per day | prose ×3 docs | MEMEBOT-034's and -041's measured states **unreproducible forever** |
| **3** | quote a fingerprint with its encoding | prose | a full round spent proving a mismatch that did not exist |
| 4 | claim before writing | enforced for `tools/` only | not yet costed |

**Two of my own probes were defective and I caught them by hand-checking** — the exact "guard that cannot fire" shape this project has now hit ten times. One searched for `"An absent gate"` (capital A) against lowercase source and reported an enforced rule as missing. The other matched `test_tools_tracked.py` and concluded "claim before writing" was enforced everywhere, when that test covers `tools/` alone. A sweep that grades itself needs its misses read, not its totals.

## 3. The three implemented

**1 — `core.hooksPath` is asserted.** `tools/githooks/` holds `pre-commit`, `pre-push` and `prepare-commit-msg`. They fire **only** because local git config points there. That setting is **not committed and absent from every fresh clone**; `guard_amend.py --install` sets it and nothing ever checked anyone had run it. Every control in those hooks — including BL-906's manifest-enrolment guard, built precisely because *"nothing ran verify_claims.py, because nothing had to"* — was one un-run installer away from silence.

It caught a live defect immediately. **`.git/hooks/pre-push` was a shadowed dead copy**: byte-identical, but `core.hooksPath` *replaces* `.git/hooks` rather than adding to it. The cause is that **two installers disagree about where hooks live** — `repo_guard.py --install-hooks` writes to `.git/hooks`, `guard_amend.py --install` sets `core.hooksPath`. Running repo_guard's installer today writes hooks git will never execute. I removed the dead copy (SHA-verified identical first, zero loss); the one-line fix in `repo_guard.py` belongs to whoever holds it.

**2 — `python tools/claim.py staged`** refuses when staged paths span more than one live round, naming each and its paths. It reuses `paths_overlap`, so a directory claim covers files beneath it — the commonest bundling case. Unclaimed paths are deliberately **not** an error; plenty of honest commits touch unclaimed files, and the signal is two *different* rounds.

**3 — the fingerprint rule is now a test.** `7a029ee5447cddd8` and `8e02f8d6f6307ae8` are **the same campaigns object** under compact versus default JSON separators. Both correct, as the brief says. The test pins both, and asserts the two encodings *disagree* — if they ever agree the test is worthless and says so.

`tests/test_governance_rules.py` — **16 tests, green** (`test_publish_report.py` 17, also green).

### The check cried wolf on its own author, and that mattered

Its first run flagged **my own commit**: BL-943 held a broad `scratch/` claim, so `scratch/mb058_sweep.py` looked co-owned. A guard that fires on the honest case is a guard people switch off — the same disease as the secret scanner's seven false-positive classes. Fixed by assigning each path to its **most specific** claimant: exact beats glob beats directory prefix. Three tests pin the refinement, including one asserting it does **not** defeat the check it protects — two genuinely different rounds are still flagged.

## Suite

**113 of 116 green.** None of the three reds is mine:

- `test_claims_manifest.py` — `docs/claims/MEMEBOT-028.claims` names `scratch/memebot028_audit.py`, which commit `30c8a83` *"Delete 10 scratch probes that cannot run"* removed. **A cleanup commit broke a committed claims manifest** — worth someone's attention, and an argument for the pre-commit hook that guards enrolment being active everywhere.
- `test_ranked_runner.py`, `test_render_argv.py` — pass in isolation, touch none of my files, red only in the loaded full run.

## 4. The inverse: refusals a round cannot look up

Eleven refusals the tools can emit, checked against every doc. **Three were undocumented:**

- `publish_report.py` — *destination must be a bare `*.md` filename* (mine, from MEMEBOT-055; I added the rule and not the explanation)
- `scan_report_for_secrets.py` — *a config secret-block value appears verbatim*
- `repo_guard.py` — *push refused: HEAD drastically behind upstream*

All three are now in `docs/ENFORCEMENT.md`, which is a two-way index: rules → enforcing code, and refusals → what they mean. The secret scanner's checks are written out in its own terms for the first time, after **seven** false-positive classes taught rounds to read it as noise.

## 5 & 6. Recorded

**Additive by default** is in `ENFORCEMENT.md` as an enforced rule with `gen_manifest.py`'s `--reclassify` opt-in beside it, and the cost: a first draft would have silently re-labelled **69 reports**. The general form — *a tool that rewrites an index must be additive unless told otherwise, and must report what it would change before changing it* — is stated there.

**The campaigns question is settled and recorded as settled.** Both hashes are correct; `config.json` is gitignored so neither is checkable from history; the encoding must be quoted with the value. That is now a test, not a memory.

---

## Limits

Ten rules came back enforced, but "enforced" means *a probe demonstrated a code path exists* — not that the code is correct. I verified the three I implemented end to end and hand-checked the rest; I did not write a failing case for each of the ten.

The nine documents contain far more than thirteen imperatives. I extracted the rules that name a *mechanical* precondition and ignored advice that needs judgement, which is a defensible line but a line I drew.

`claim.py staged` is advisory: it exits non-zero, and **nothing calls it yet**. Wiring it into `tools/githooks/pre-commit` is the obvious next step and that file is not in my claim — so the rule I just made enforceable is, today, still one step from enforced. Naming that rather than implying otherwise, because it is the same gap this report is about.

The `core.hooksPath` test asserts the setting on *this* machine. It cannot make a fresh clone safe; it can only fail loudly the first time the suite runs there, which is the most a test can do about a setting git refuses to version.
