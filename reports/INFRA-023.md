# INFRA-023: the modules were already committed; the exposure was a font on one machine

**Date:** 2026-08-03 · **Type:** Infrastructure / release hygiene · **Spend: $0.00, no paid calls**

Claim filed via `tools/claim.py`, paths registered individually with repeated `--write`.
Registry read with `tools/claims_read.py --holders` and `git status --porcelain` before every
step. `tools/commit.py` throughout on the parent — **seven commits across two repositories**
(five parent, two in `memebot/`, which is a separate git repo with its own remote), each by
explicit path.

---

## 0. The brief's premise had moved, and the right response was to check rather than act

The brief sends this round to commit three untracked modules with `Claim-Override`. They were
already tracked:

| module | committed by | when |
|---|---|---|
| `clippershq/client_delivery.py` | **BL-1006**, its own author | 23:09:32 |
| `clippershq/client_intake.py` | **BL-1006**, its own author | 23:09:32 |
| `clippershq/audit_labels.py` | **BL-1011**, its own author | 23:10:26 |

Both rounds closed their own files roughly eight minutes after the reds were reported.
Committing them under my name would have put their work in the permanent record under the
wrong author for no benefit — the exact harm `commit.py`'s override warning cites. So this
round **verified** instead: all three import cleanly, and both previously-red suites
(`test_clip_pipeline.py`, `test_no_unchecked_stdout.py`) are green in the worktree.

What was left over was the part nobody had closed, and it was worse than the part that had.

## 1. The font: decided by the licence, because the file is not what it is called

The brief offers a choice — commit the font if licensing allows, or make its absence loud.
**The licence made the choice.** Read from the font's own name table rather than from what
Inter is generally known to be:

```
scraper/fonts/Inter-Bold.ttf   family   Arial
                               version  Version 7.05
                               vendor   The Monotype Corporation
                               licence  "Microsoft supplied font"
                               960,832 bytes
```

It is **Arial Bold**, installed under Inter's name by `ensure_font_available`'s auto-copy,
which copied the first system bold font to whatever path was asked for. A Microsoft-supplied
face cannot be redistributed, so committing it was never on the table — and the fix that
"exists on one machine" was resting on a file whose identity nobody had checked.

**What the absence costs, measured.** `font_for_caption` falls back to Montserrat when the
alt face is not beside it, calling that "a caption in the wrong face". That is only the
smaller failure if the wrong face can draw the letters:

| face | Latin | Cyrillic | Greek | Hebrew | Arabic |
|---|---|---|---|---|---|
| Montserrat-Bold (shipped, OFL) | yes | yes | **boxes 11 of 11** | **boxes** | **boxes** |
| the installed "Inter" (= Arial) | yes | yes | yes | yes | yes |

Nothing raises. FreeType substitutes `.notdef`, ffmpeg exits 0, the row is written, the cost
is paid, and the video ships with boxes where the caption was.

### Three changes, and the failure is loud now

* **`face_cannot_draw(font_path, text)`** — asks the font on disk, by pixels, cached,
  PIL-optional, returning `""` whenever it cannot answer so it never becomes a new way for a
  render to fail.
* **`_caption_survives_filter`** gives the last word to the face actually selected, not to a
  hardcoded range table. A caption it cannot draw is dropped **by codepoint** and the clip
  keeps its own burned-in frame — which MEMEBOT-076 measured as the better hook on 9 of 10
  clips anyway. The failure mode replaced was not "no caption", it was "a caption of boxes".
* **`ensure_font_available` will not install one font under another font's name.** Copying
  under the *same* name is untouched and still the common case.

```
  i  Caption dropped: Montserrat-Bold.ttf cannot draw U+05E9 ('ש') and would print a
     .notdef box. Keeping the source's own frame.
```

MEMEBOT-102's 13 tests still pass. 8 new tests in `test_font_presence.py`, including the
clone simulated directly — Montserrat alone in a temp dir with no alt face beside it.

**PIXELS, NOT THE CMAP.** My first instrument read the cmap and reported Montserrat as
*having* Greek. MEMEBOT-102 had already established that a font's cmap and its glyphs can
disagree, and the pixel method says Montserrat boxes **all eleven** Greek sample characters.
The decision rests on pixels; the cmap harness is kept only for the licence read.

## 2. The staged manifest

`docs/claims/MEMEBOT-094.claims` had been `A ` — staged, never committed — since 19:54. The
index here is global, so any round running a bare `git commit` sweeps up whatever is staged;
while I was writing that commit the index also grew **7 of BL-1002's files**, the same hazard
arriving again. MEMEBOT-094 has released, its report is published, and the manifest verifies
**9/9 at HEAD** (checked, not assumed). Committed by explicit path, attributed to its author,
`Claim-Override` recorded.

## 3. The guard was not looking at the product

The brief's hypothesis was that the 480-minute in-flight exemption let the three modules
through. It did not. **They were never in scope:**

```python
GUARDED = ("tools",)        # before
GUARDED = ("tools", "clippershq")   # after
```

That is the worse failure of the two and the more instructive one. A too-generous exemption
at least prints what it excused; a directory that was never enumerated produces silence, and
silence is indistinguishable from a pass — the same shape as BL-908's crashing git and
BL-999's swallowed exception.

Three new tests: an untracked shipping module is **in scope at all** (asserted through
`_untracked()`, so adding the directory without the scan reaching it still fails); a
**released** round's untracked module is an orphan **immediately**, no grace period
(`claim.py end` deletes the claim file, so released and never-claimed look identical — and
should); and a round still mid-write is **reported, not failed**, which is BL-929's lesson
and must survive the widening.

**Proven on plants — 4/4:** unclaimed RED, released RED, fresh claim GREEN, stale claim RED
with the round named. The plants go in throwaway repos, never the live tree: this file's own
history is BL-938, where a plant in the real `tools/` raced every round writing a tool and
made the suite flip between exit 0 and exit 1 on identical input. Ten rounds are in flight
and BL-1016 has an untracked `clippershq/clip_motion.py` on disk right now — the widened
guard reports it as in-flight, which is exactly right.

## 4. The clean extract: 5 of 5 green, and two of the reds were mine

`git status` compares the worktree to HEAD, so it reports what is *different*. A file that is
untracked **and ignored** is neither — it is invisible. Both repositories were extracted with
`git archive HEAD` (parent, and `memebot/`, which the parent ignores, so a parent-only
extract yields a tree with no renderer at all).

```
  repo     suite                                result
  parent   tests/test_tools_tracked.py          PASS
  parent   tests/test_no_unchecked_stdout.py    PASS
  parent   tests/test_clip_pipeline.py          PASS
  memebot  scraper/tests/test_font_scripts.py   PASS
  memebot  scraper/tests/test_font_presence.py  PASS
  5 of 5 suites green in the extract.     (Inter-Bold.ttf: ABSENT, as in every clone)
```

Getting there required fixing two tests that asserted **this machine** rather than HEAD:

* `test_font_scripts.py` asserted Greek/Hebrew/Arabic are drawn in the Inter face. The
  routing is now asserted only where that face exists; the refusal that replaces it in a
  clone is asserted unconditionally in `test_font_presence.py`, which is green in the
  extract. Neither case goes unchecked and every skip prints its reason.
* `test_a_pending_site_is_still_claimed` read an empty `.claims/` — which is **gitignored** —
  as "every deferral has been released", so it failed in every clone, permanently, for a
  reason with nothing to do with deferrals. **An absent registry is not a released claim.**

## 5. Stale claims — named, not taken

| round | age | state of its declared paths |
|---|---|---|
| **MEMEBOT-039** | **1,641 min (27.4 h)** | 4 untracked `scratch/` harnesses. Its own note says "BLOCKED ON THE WRITE" on a conflict that resolved long ago. |
| **BL-899** | **1,585 min (26.4 h)** | `clippershq/clip_pipeline.py` **CLEAN and tracked — a claim with no work under it**, holding the most contended file in the repo. Plus `tests/test_clip_pipeline_gate.py` untracked for 26 hours. |

`clip_pipeline.py` is contended (BL-899, and MEMEBOT-110 earlier), so it is named here rather
than taken.

**Measured, not proposed blind — what widening the guard further would catch today:**

| added to GUARDED | orphans | in-flight | verdict |
|---|---|---|---|
| `tests` | **2** — `tests/test_clip_pipeline_gate.py` (BL-899, 1,585 min) and `tests/bl932_probe_67vrvaav.py` (**no claim at all** — see §6: it turned out to be a test's own litter, now fixed at cause) | 5 | **right, but not by me tonight** |
| `scratch` | **4,486** | 32 | wrong — `scratch/` is a junk drawer by design |
| `docs` | 0 | 4 | harmless, catches nothing today |

`tests` is the correct next step and I did not take it. Adding it turns the suite **red for
all ten live rounds** until BL-899's 26-hour orphan is resolved — and I cannot resolve it
without taking the file the brief told me to name rather than take. Forcing another round's
hand by reddening everybody's suite is the harm this round exists to reduce.

## 6. The full suite's two reds were one 17-byte file, left by a test

The 174-suite run came back **172 green, 2 red** — `test_suites_parse.py` and
`test_claims_manifest.py`. Attributed individually, they are **one cause**, and it is the
same subject as the rest of this round:

`test_suites_parse.py::test_it_detects_a_planted_unparseable_file` `mkstemp`'d its plant into
the **real `tests/` directory** and relied on a `finally` to remove it.

* A run that dies between the mkstemp and the unlink leaves the plant behind. One was on
  disk: **`tests/bl932_probe_67vrvaav.py`, 17 bytes reading `"""unterminated`**, written at
  23:54 while eight suites ran concurrently. Untracked, unclaimed, unparseable — and it made
  `test_every_test_module_parses` red for **every** round in the tree.
* Concurrent runs failed each other: the final assertion said no `bl932_probe_` file remains
  anywhere under `tests/`, so a second run's live plant broke the first run's cleanup check.

**This is BL-938 arriving a second time.** That round found the identical pattern in
`test_tools_tracked.py` and recorded why it matters — *a guard that is itself intermittently
red is worse than no guard, because intermittent red trains people to ignore red.* The fix is
the same: `_unparseable` already took a base, so it now accepts an absolute path and the
plant goes in a `mkdtemp`. The assertion is not weakened; the same function still detects.

Verified: both suites green, and **two concurrent runs of `test_suites_parse` both exit 0** —
the case that was failing.

**The leftover was not deleted.** A byte-identical copy sits in this session's scratchpad
under `quarantine/` before it was removed from `tests/`. It is 17 bytes of a deliberate
fixture with no owner, but an untracked file is unrecoverable once gone, and that is this
round's entire subject.

This also retires the "stray probe, not mine to delete" item from §5 — it had an owner after
all: the test that planted it.

---

## Honest limits

* **My own harness was wrong three times, and every error read as a real finding.**
  (1) `git archive` + `tar` yields plain files, not a repository; three suites shell out to
  git, got exit 128, and `run_checked` correctly raised — I nearly filed them as clone
  defects. The extract is `git init`-ed now, because a clone *is* a repo. (2) `%TEMP%` here
  is the 8.3 short form; `os.path.abspath` leaves a short name short while `Path.resolve`
  expands it, so `clip_pipeline` and `run_record` derived one ledger file as two different
  strings and I had it written up as a clone defect until the same suite passed by hand in
  the same directory. (3) The harness built an env with `PYTHONUTF8=1` and never passed it to
  `subprocess.run` — a variable sitting there looking like configuration while every suite
  ran under the system codepage, which `docs/TESTING.md` names as a source of false reds.
* **The cmap instrument was the weaker one** and I used it first, after MEMEBOT-102 had
  already documented why. Corrected to pixels; the wrong measurement is left in the harness
  docstring rather than deleted.
* **The font is not committed and Greek/Hebrew/Arabic captions are still not drawn in a
  clone.** They are now *refused by name* instead of printed as boxes. That is a smaller
  failure, not no failure. Installing real Inter (OFL, redistributable) and adding a
  `.gitignore` exception is the actual fix and it is one file — the README says so.
* **`git push` on the parent pushed 8 commits, not 5.** The branch is shared; the other 3
  were already-committed work from other rounds sitting unpushed. Named because "I pushed"
  should not read as "I authored".

## Still broken, and whose file

* **Montserrat-Bold.ttf ships under SIL OFL 1.1 and the repo has no licence file.** OFL
  clause 2 requires the licence and copyright notice to accompany redistribution. The remedy
  is one file, `scraper/fonts/OFL.txt`, from the canonical Montserrat repo. I did not
  hand-type a licence — a mistyped licence is worse than a missing one. **memebot's, and
  the operator's call.**
* **BL-899, 26.4 h**, holding a clean `clippershq/clip_pipeline.py` and a 26-hour untracked
  `tests/test_clip_pipeline_gate.py`.
* **MEMEBOT-039, 27.4 h**, 4 untracked scratch harnesses, blocked on a conflict long resolved.
* ~~`tests/bl932_probe_67vrvaav.py`, a stray probe with no owner~~ — **closed in §6.** It had
  an owner: the test that planted it into the live `tests/` directory. Fixed at cause.

## Suite and spend

`PYTHONUTF8=1 python tests/run_all.py` on the parent, discovery rule: every `test_*.py` under
`tests/` and any nested `<pkg>/tests/` (MEMEBOT-026), which includes both memebot suites.

**Run 1 — 172 of 174 green.** Both reds were the one 17-byte leftover in §6, fixed at cause.

**Run 2 — 173 of 175 green (485s, 4 rounds in flight).** The two reds moved to
`tests/test_claim.py` and `tests/test_doc_citations.py`, and neither is mine: **both are held
by INFRA-024**, and `test_claim.py` was `M ` — staged, mid-edit — while the run was in
progress. Re-run after the edit settled, **both pass**, along with every suite this round
touched:

```
  tests/test_claim.py            PASS      tests/test_suites_parse.py        PASS
  tests/test_doc_citations.py    PASS      tests/test_claims_manifest.py     PASS
  tests/test_tools_tracked.py    PASS      tests/test_no_unchecked_stdout.py PASS
```

A suite count in this tree is a moment, not a property — the runner prints that itself. The
durable number is the one from the clean extract: **5 of 5**, which is what a clone gets.

**Spend $0.00 — no paid call was made.** Campaigns unchanged; `config.json` untouched.
`memebot/runs.jsonl` was `M ` under a live render throughout and was never committed.
