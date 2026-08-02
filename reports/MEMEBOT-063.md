# MEMEBOT-063: the check is wired — and the hook beside it is broken at HEAD

> **Published as MEMEBOT-063.** The work was done under claim `MEMEBOT-059`, but
> `reports/MEMEBOT-059.md` was already taken by another round ("the loop is wired, the
> sheet is ready, and not one record joins the store"). **The collision check added in
> MEMEBOT-057 refused my publish** — the same mistake MEMEBOT-055 made by hand, caught by
> tooling this time instead of by reading a manifest row afterwards. Theirs is untouched.

**Date:** 2026-08-02 · **Class:** Enforcement wiring · **Spend:** **$0.00**, no paid calls.
**Claim:** `MEMEBOT-059`, eight repeated `--write` flags, *"8 path(s) registered individually"*. `claims_read.py --holders` per target, all FREE; `git status --porcelain` read with the index and worktree columns separated (`' M'` = unstaged, `'M '` = staged). One advisory: BL-946 holds `scratch/` broadly; my paths are `scratch/mb059_*`. **Noted and not touched:** `tools/publish_report.py` and `tools/verify_claims.py` are both `' M'` — unstaged work by BL-950 and BL-921.

---

## The finding that outranks the brief

**At HEAD, the pre-commit hook rejects every commit.**

It calls `python tools/verify_claims.py --enrolling`. `tools/verify_claims.py` **at HEAD has zero occurrences of `enrolling`** — the copy that supports the flag is BL-921's, still unstaged in the working tree. So in any fresh clone, the moment hooks are installed:

```
usage: verify_claims.py [-h] paths [paths ...]
verify_claims.py: error: the following arguments are required: paths
  pre-commit REFUSED: a manifest above would be enrolled into permanent enforcement...
```

An argparse usage error, reported as a manifest violation. It works on this machine only because an uncommitted file happens to be present. That is the *"promise committed before the thing it promises"* shape the hook's **own docstring** warns about, inverted — the caller shipped ahead of the flag it depends on.

I did not fix it: `verify_claims.py` belongs to a live round. It needs BL-921's commit, or the hook needs to tolerate a `verify_claims` without the flag.

**It also nearly fooled me.** My clean-clone harness printed **PROVEN** on its first run while the commit was being rejected by that usage error, not by my check. The harness now asserts *which* check refused and stubs the other out to isolate it. A guard that fires for the wrong reason is indistinguishable from one that works.

## 1. `claim.py staged` is wired

`tools/githooks/pre-commit` now calls it, with the status read off `$?` — never a pipeline, which is the hazard that ate an exit code three times in this repo. It fired on my own commit while I was making it:

```
no manifest would be newly enrolled by this commit.
staged paths belong to one round: MEMEBOT-059
```

## 2. One hook location; both installers agree

`repo_guard.py --install-hooks` wrote into `.git/hooks`; `guard_amend.py --install` sets `core.hooksPath=tools/githooks`. **`core.hooksPath` replaces `.git/hooks` outright**, so once anyone ran guard_amend, everything repo_guard installed was shadowed — and left a byte-identical copy that read as installed. `repo_guard` now writes the versioned hook, sets `core.hooksPath`, and warns about any shadowed leftover.

```
installed tools\githooks\pre-push
core.hooksPath -> tools/githooks (ok)
```

## 3. The stale attestation — already fixed by another round

Commit `2ece1c5 "Restore memebot028_audit.py: a published claims manifest attests to it"` restored the file that `30c8a83 "Delete 10 scratch probes that cannot run"` removed. Verified rather than assumed: the file is present at HEAD and `test_claims_manifest.py` is **24 tests green**. That is the honest resolution of the two — the manifest attested to it, so the file came back.

## 4. Proven from a clean clone, not from this tree

`scratch/mb059_clone.py` clones HEAD into a throwaway directory and measures three states. **State 1 is the load-bearing one** — without it, "the hook refused" proves nothing.

```
STATE 0  core.hooksPath : (unset)   all three hooks versioned, none in .git/hooks
STATE 1  planted cross-round commit BEFORE install   -> ACCEPTED  (hooks inert)
STATE 2  after repo_guard --install-hooks            -> REFUSED
STATE 2b verify_claims stubbed, so only `staged` can refuse:

           STAGED PATHS SPAN 2 LIVE ROUNDS -- commit them separately:
             ZZ-ONE   scratch/zz_one.py
             ZZ-TWO   scratch/zz_two.py
           pre-commit REFUSED: this commit mixes work from more than one live round.

STATE 3  pre-commit / pre-push / prepare-commit-msg  -> all reachable
```

## 5. The installation gap, recorded as a third failure mode

`docs/ENFORCEMENT.md` already named two: **documented but unenforced**, and **enforced but undocumented**. This is the third:

> **A rule can be written, implemented, unit-tested and committed, and still never run,
> because its INSTALLATION is uncommitted local state.**

**Neither existing sweep can find it.** A doc sweep asks *is this rule in code?* — yes. A tool sweep asks *does this code run when called?* — yes. Neither asks *is anything calling it on this machine?* The only detectors are a clean-clone rehearsal and an assertion that the setting exists.

And it generalises past hooks: anything **installed** rather than imported has this shape — `PATH` entries, scheduled tasks, editor plugins, shell aliases, environment variables. If the answer to *"how does this get turned on?"* is a command someone runs once, it is off everywhere that command was not run, and no test in the repository can tell.

## 6. Campaigns — both encodings, both unchanged

```
default separators : 8e02f8d6f6307ae8  MATCH
compact separators : 7a029ee5447cddd8  MATCH
config.json valid JSON
```

The brief is right and it is now mechanical: same object, two encodings. `tests/test_governance_rules.py` pins both, and asserts they *disagree* — if they ever agree the test is worthless and says so.

## Suite

**ALL GREEN — 120/120 suites, 4,395 checks.** First fully green full run of the session; the three reds MEMEBOT-058 left (`test_claims_manifest`, `test_ranked_runner`, `test_render_argv`) are all resolved — the first by the file restoration above, the other two having been load-flakes. `test_governance_rules.py` is 22 checks.

---

## Limits

**The pre-commit hook is broken at HEAD and I left it that way.** Fixing it means touching a live round's file. Anyone cloning today and installing hooks cannot commit until BL-921 lands — that is the single most actionable thing in this report and it is not mine to close.

`claim.py staged` is advisory in one direction that matters: it reads `.claims/`, so a round that never filed a claim is invisible to it. Two unclaimed rounds bundled in one commit pass silently. It enforces "declare your paths", not "commit per round" in the abstract.

The clean-clone rehearsal covers `pre-commit`. `pre-push` and `prepare-commit-msg` are proven **reachable**, not proven to fire — `pre-push` needs an upstream drastically behind, which the harness does not construct.

`core.hooksPath` remains uncommitted local state after all of this. Both installers now agree, the test fails loudly when it is unset, and the rehearsal shows what a fresh clone actually does — but git offers no way to version it, so the gap is *visible*, not closed.

**And one self-inflicted note:** the first upload of this report was mojibake and carried the wrong title, because I rewrote the file through a PowerShell string round-trip that mangled UTF-8. Corrected with `--update`. Editing a report through a shell re-encode is a good way to publish something you did not write.
