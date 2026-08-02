# MEMEBOT-080 — Both dependencies resolved, and the sweep that would not have found its own bug

**Round:** MEMEBOT-080 · **Date:** 2026-08-02 · **Spend:** **$0.00**, no paid calls
**Claim:** `MEMEBOT-080`, seven repeated `--write` flags, *"7 path(s) registered individually"*.
`claims_read.py --holders` run per target; `git status --porcelain` checked.
**Commits:** `3bfc580` (TESTING.md 14–15), `861b9a7` (reachability + sweep).

Acts on [MEMEBOT-075](https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/MEMEBOT-075.md).

---

## 1. MEMEBOT-066 — NOT landed. It stays untracked, and that is correct.

Re-verified rather than inherited (BL-974's rule). Still **2/8**. The interesting part is
*why*, and it is not what "not landed" usually means — **the work is written**:

| Symbol | On disk | At `memebot` HEAD |
|---|---|---|
| `AudioClassRequired` | ✅ `duck.py:459` | ❌ |
| `require_audio_class` | ✅ `duck.py:496` | ❌ |
| `REQUIRE_AUDIO_CLASS_DEFAULT` | ✅ `duck.py:493` | ❌ |

All six failing paths **exist on disk**; three are parent-repo files that are untracked, three
are nested-repo symbols that are uncommitted. `memebot/` is dirty across four files
(`duck.py`, `edit.py`, `tests/test_duck.py`, `runs.jsonl`), so that repo is mid-flight for
somebody.

**I did not commit it.** `duck.py` is unclaimed, so I *could* have — and that is exactly the
trade this repo has repeatedly declined. Committing another round's authored nested-repo
source, while that repo is dirty across files I have not read, under my name, to make a
manifest enrollable, is the same move BL-972 refused two rounds ago for the same reason.
MEMEBOT-066 is **not a live round**, so nobody can confirm the work is finished.

**What closes it** (for whoever owns it): `git -C memebot commit -- scraper/duck.py
scraper/tests/test_duck.py`, then commit `tests/test_audio_class_reaches_render.py`,
`scratch/mb066_corr.py`, `scratch/mb066_render.py` in the parent, then enrol the manifest.

---

## 2. test_matcher_boundary.py — GREEN, resolved by BL-972. The field is *half* consumed.

**9/9 pass.** BL-972 has it, along with `song_library.py`, and resolved it — but not by wiring,
and the brief's reading needs one correction:

> `song_library.vision_suspect()` **does** read `vision_control_declined`.
> `clip_pipeline.dict_of()` still **does not** pass it.

So through the pipeline path the flag is `None` on every clip. BL-972 recorded this as an
`EXEMPT` entry with the reason, the blast radius, and the one-line patch — not as a silent
pass. Their note is worth quoting because it is the right shape:

> *"WHY NOT JUST FIX dict_of: `clippershq/clip_pipeline.py` is held by BL-899 and has been for
> ~17 hours. Editing another round's file to make my own suite green is the trade this repo
> has repeatedly decided against."*

**BL-899 is now 1,085 minutes old, its own files untouched for 1,082** — `claim.py brief`
flags it `** POSSIBLY STALE`. It also says, in the same breath, *"nothing expires
automatically. Ask the owner."* So I attribute rather than take it. The patch is one line:
add `"vision_control_declined"` to `MATCHER_FIELDS` at `clip_pipeline.py:1467`.

**Measured blast radius while it waits:** 3 clips of 2,003 carry `declined == False`, and
`vision_suspect(absent)` returns `None`, which never forces `needs_review`. A missing field
cannot flip a clip to suspect — only fail to flag one. It degrades safely.

---

## 3. The refusal path is genuinely reachable — proved by planting

`scratch/mb080_plant.py` plants an **untracked, never-staged** prose manifest, runs the real
suite, and asserts red; removes it and asserts green.

```
STEP 1  baseline, no plant          suite exit 0  GREEN
STEP 2  plant (tracked by git? False)
        suite exit 1  RED (correct)
        names the offending file? True
        names the offending line?  line 1: unknown claim kind 'claim'
STEP 3  plant removed               suite exit 0  GREEN (restored)
VERDICT: REACHABLE
```

Both directions, because a guard that is always red is as useless as one that is always green.

### And a new permanent test that pins the FIX, not the bug

The existing assertions prove `parse_manifest` *refuses* prose. It refused prose for the
entire time three broken manifests sat undetected — what was broken was **discovery**. So
`DiscoveryIsTheFilesystem` asserts that `_on_disk()` sees a file the index cannot. Rehearsed:
**with discovery reverted to `git ls-files`, the new test fails.** A refactor back to the index
would leave every other assertion passing and silently restore the hole.

---

## 4. The three-state distinction — recorded as `docs/TESTING.md` rule 14

| State | Meaning | Verdict |
|---|---|---|
| untracked + **unparseable** | invisible; fails the moment anything looks | **DEFECT** |
| untracked + **claims fail** | waiting for its code (BL-874) | **CORRECT** |
| untracked + **claims hold** | never enrolled | **READY**, report don't fail |

The middle row is the one that matters: a sweep reporting "untracked" as one fault pressures
the author to `git add` a manifest whose claims fail, turning the suite permanently red — and
destroying the discipline BL-874 exists to create. Three manifests are in that state right now
(`MEMEBOT-066`, `-077`, `-078`) and the suite reports them without failing.

---

## 5. THE UNREACHABLE-GUARD SWEEP — and why its clean result proves less than it looks

`scratch/mb080_unreachable.py`, AST-resolved, import-scoped, across `tools/` and `tests/`:

| Status | Count |
|---|---:|
| **CALLED** (import-scoped caller found) | **126** |
| **EXEMPT** — unittest-runner invoked | **54** |
| **DUCK-TYPED** — injected test doubles | **8** |
| **NO CALLER** | **0** |
| *total guard-shaped functions* | **188** |

### The finding that matters: this sweep would not have found `parse_manifest`

It has **48 in-repo references / 19 call sites**. By call-graph reachability it is one of the
best-covered functions in the repo, and the sweep marks it `CALLED`. It was still unreachable
for the files that mattered. **"A check that never runs" is two different faults:**

- **A — no caller.** The call graph has a hole. This sweep finds these. **0 found.**
- **B — no caller on the failing input.** The call graph is perfect and the *population* is
  wrong. **No caller-counting tool can see this**, including this one.

MEMEBOT-075's bug was type B. Reporting "0 unreached" as coverage of the fifteen-instance
pattern would be the guard-cited-as-coverage error one level up, so the number ships with its
limitation attached. This is now `docs/TESTING.md` rule 15.

### Three measurement traps, each of which gave a confident wrong answer first

1. **Bare-name matching → "0 unreached", for the wrong reason.** 71 of 188 guard names are
   defined more than once (`check` ×15, `boom` ×18). Every reference to any `check` counted as
   a caller for all fifteen. Fixed by scoping callers through the **import graph**.
2. **Inert decorators.** Counting `@staticmethod`/`@property` as "registered by a decorator"
   laundered dead helpers into EXEMPT. Only a decorator that *registers* is a caller.
3. **Duck-typed injection → 8 false positives.** `_Boom.user_videos`, `FakeResp.json`,
   `_FakeTorch.no_grad` and five others have no importer *by construction* — production calls
   them on an injected object (`user_videos` 3 sites in `clippershq/`, `sync` 9, `json` 9).
   An import-scoped count calls them dead; they run on every test.

Every exemption is printed with its count so a reader can disagree with it. An exemption
nobody can see is how a sweep launders its own false negatives.

---

## VERIFICATION

| Check | Result |
|---|---|
| `tests/test_manifest_prose_refused.py` | **7/7**; new test goes RED on a reverted discovery |
| Planted prose manifest | **refused**, named by file and line; cleaned up |
| `test_matcher_boundary.py` | **9/9 green** |
| Unreachable-guard sweep | 188 examined, **0 unreached** |
| `config.json` | unmodified, parses, **5 campaigns** |
| Stray `ZZZ-*` manifests after all rehearsals | **0** |
| Full suite | **137 pass, 5 red — none mine** |

### The five reds, attributed

| Suite | Owner | Evidence |
|---|---|---|
| `memebot/…/test_caption_fit.py` | **MEMEBOT-082** | `memebot/scraper/edit.py` + `templates.yaml` dirty, mid-edit |
| `memebot/…/test_edit_behaviour.py` | **MEMEBOT-082** | same |
| `tests/test_render_argv.py` | **MEMEBOT-082** | *"edit.py accepts `--force-caption` and clip_pipeline neither passes it nor records why not"* — that flag is on disk **3×** and **absent at `memebot` HEAD** |
| `tests/test_matcher_boundary.py` | *transient* | **passes on re-run**; flipped mid-suite while BL-972 wrote `song_library.py` |
| `tests/test_suites_parse.py` | *transient* | **passes on re-run**, same cause |

MEMEBOT-080 committed **no** `memebot/` file — verified against its own commits. The two
transients are worth naming rather than hiding: with 6–8 rounds writing concurrently, a suite
result is a moment, not a property, and a red that passes on re-run is a scheduling artefact
rather than a defect.

## STILL OPEN — and whose

- **`MEMEBOT-066.claims`** — untracked and *correct* per BL-874. Its work is written but
  uncommitted in `memebot/`. **Its owning round's to land**, not mine to commit.
- **`dict_of()` drops `vision_control_declined`** — one line, `clip_pipeline.py:1467`. Held by
  **BL-899**, 1,085 min, possibly stale. Nothing expires automatically; ask the owner.
- **`MEMEBOT-077` / `-078`** — untracked, claims failing, correctly waiting.
