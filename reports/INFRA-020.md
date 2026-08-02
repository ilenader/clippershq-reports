# INFRA-020 — the three "standing reds" were already green, and the suite went **154/154, 5,100 checks** ten minutes later. What was actually broken is that **both staleness checks in the guard file had been retired by their own success**, and the second list never had one at all.

**Date:** 2026-08-02 · **Type:** test infrastructure · **Spend:** **$0.00**, no paid call
**Wrote:** `tests/test_guard_resolution.py`, `tests/test_render_argv.py` (commits `6cb7010`,
`77abed2`), and `scratch/infra020_*`. **Read but never wrote:** `clippershq/song_library.py`,
`clippershq/clip_pipeline.py`, `scratch/songs.json`, `tests/run_all.py`.

---

## The premise, re-measured on arrival

`docs/CORRECTIONS.md` and BL-974 both say to re-verify "still broken" before acting on it, so
the three named suites were run first, before anything was touched:

| suite | brief says | measured on arrival |
|---|---|---|
| `tests/test_guard_resolution.py` | stale baseline listing 6 guards | **green, 8/8** — `BASELINE = {}` already |
| `tests/test_render_argv.py` | red on an uncommitted `--force-caption` | **green, 8/8** — the flag is at memebot HEAD, entry is correct |
| `tests/test_song_library_meme_rule.py` | red on in-flight `song_library.py` | **green, 0 failures** |

**All three were already green, and INFRA-018 had already done items 1 and 5** — it pruned
`BASELINE` to `{}` and recorded the AST-vs-text finding, including the ~1,350-line example,
in the comment block directly above it.

That is the whole brief, minus what INFRA-018's own success quietly broke.

---

## 1. Both staleness checks had been retired by reaching their goal

`scratch/infra020_probe.py`, run before any edit.

### The baseline check computes the right answer over nothing

```
BASELINE entries                : 0
text guards found in the tree   : 0
stale, as shipped               : []
stale, with one planted entry   : 1   <- the expression works
VERDICT: CORRECT BUT UNREACHABLE
```

`stale = [k for k in BASELINE if k not in found]` over an empty dict is `[]` on every run,
forever. So is `test_every_baseline_entry_says_what_is_wrong_with_it`, which loops the same
empty dict. **Emptying the baseline — the correct outcome — is what switched its guard off.**

This is `docs/TESTING.md` RULE 1 exactly: a fixture that cannot produce the failing case makes
a test that cannot fail. And it is that rule inside the one file that already knew it — this
is the module that wrote `test_the_detector_fails_on_a_planted_text_guard` for its *other*
mechanism, on the stated grounds that **"a guard that has never failed is not known to work."**
The same standard was never applied to its own bookkeeping.

### `EXEMPT` never had a staleness check, and its only entry was dead

`EXEMPT` short-circuits `scan()` and skips the whole function, so it grants the same licence
by the same mechanism. `BASELINE` has had a staleness check since INFRA-017; `EXEMPT` has had
none. Planting a dead entry:

```
tests that caught the dead exemption : 0
VERDICT: NOTHING CATCHES IT
```

And the single real entry —
`("tests/test_guard_resolution.py", "test_the_detector_fails_on_a_planted_text_guard")`,
reasoned as *"the planted counter-example this file's self-test requires"* — **was not holding
anything back.** That function calls `ast.parse`, so `_parses()` skips it before `EXEMPT` is
ever consulted. Measured directly:

```
whole tree with EXEMPT emptied : 0 text-resolved guard(s)
```

It had been redundant for its entire life. That is not harmless: an exemption is a standing
licence to text-resolve one named function, and it reads to the next person as evidence that
somebody weighed it.

### What shipped

Both computations are now pure functions — `stale_baseline_keys()` and `dead_exemptions()` —
so the enforcing tests can call them with the real (empty) lists while **mechanism tests
exercise them against synthetic input on every run**. An empty record and a broken checker no
longer look the same from outside.

`dead_exemptions` catches both ways of being dead: **GONE** (names a function that no longer
exists) and **REDUNDANT** (exists, but would not be flagged even without the exemption). The
redundant case is the one that bit here. The dead entry was removed; `EXEMPT` is now empty and
its emptiness is enforced rather than assumed.

`test_every_exemption_carries_a_reason` was also raised to `BASELINE`'s bar (>20 characters) —
the two lists grant the same licence and were holding their entries to different standards.

### Mutation-proven, 4/4

A check nobody has seen fail is the thing this round is about, so:

| mutation | expected | result |
|---|---|---|
| `stale_baseline_keys` stubbed to return `[]` | baseline mechanism test red | **RED** |
| `dead_exemptions` stubbed to return `[]` | exemption mechanism test red | **RED** |
| plant a **GONE** exemption in the real list | `test_no_stale_exemption` red | **RED** |
| plant a **REDUNDANT** exemption in the real list | `test_no_stale_exemption` red | **RED** |

`tests/test_guard_resolution.py`: **8 → 11 tests, green.**

### And the prose that described a protection the code no longer has

The comment block above `BASELINE` says `test_the_baseline_has_not_gone_stale` *"went red the
moment the sixth conversion landed"* — true, and a reader stopping there takes it for live
protection. It cannot fire again. The paragraph now says so and points at the mechanism test
that does the work while the dict is empty (`77abed2`). **A comment describing a protection
the code no longer has is a stale baseline entry in prose.**

---

## 2. `test_render_argv` — green for the right reason, with one false sentence

`--force-caption` is in `NOT_WIRED` with a considered reason: `white_frame` ships
`caption.enabled: false` because the source clip's own burned-in text is the better hook, the
pipeline renders that measured-better variant, and forcing a second caption is a per-render
human judgement rather than a value the pipeline computes. There is also already a staleness
guard — `test_no_not_wired_entry_names_an_option_edit_py_no_longer_accepts` — and it passes.

But the entry's own note still read *"the flag is MEMEBOT-082's and is uncommitted at the time
of writing — 3 occurrences in the worktree copy of `memebot/scraper/edit.py`, 0 at HEAD."*

```
occurrences at memebot HEAD : 4        landed in: ba0ce2b
occurrences in the worktree : 4
```

The decision is unchanged and correct; only the claim about the tree was out of date. Updated
to record the history and retire the caveat. **It is the same defect the registry's own
staleness test exists to catch, one field over** — the test checks whether the *flag* still
exists, and nothing checks whether the *reason* is still true.

---

## 3. `test_song_library_meme_rule` — verified by measurement, not by "it passes"

| check | result |
|---|---|
| `_pending_vision_rules` present | **1 rule**, keys include `_activate`, `_activation_steps`, `_activation_impact`, `_status` |
| the matcher still never reads it | **true** — the rule is not in `vision_rules` |
| `_activate` packet complete | 13 keys: `song_id`, `path`, `mood`, `hooks`, `targets`, `enabled`, … |
| numbered activation steps | **4**, current |
| per-clip zero-regression assertion | **passes** |

The assertion reads `clip_library.read_all(LIB_ROOT)` **live**, not a frozen snapshot, so it
re-measures on every run. It now runs against **2,661 clips — the brief said 2,603, and the
library has grown by 58 since that number was written.** The assertion still holds on all of
them: no clip that has a mood today loses one on activation, and the only clips permitted to
change are those named in `_activation_impact`.

---

## 4. Two full-suite runs — and I polluted my own first attempt, twice

Both taken back to back with my own two files committed and untouched throughout, each
recording the commit and the live-claim count it started at:

| | run 1 | run 2 |
|---|---|---|
| started | 19:38:05 | 19:48:35 |
| `HEAD` at start | `77abed2` | **`0dd9bb2`** |
| rounds in flight | 11 → 7 | 7 → 5 |
| suites | 154 | 154 |
| result | **4 red** (628.7s) | **ALL GREEN — 154/154, 5,100 checks** (527.5s) |

Run 1's four:

```
tests/test_claims_manifest.py
tests/test_manifest_prose_refused.py
tests/test_market_filter.py
tests/test_verify_claims.py
```

**None of them are mine, and all four were green ten minutes later** with nothing done to
them by me — three are claims-tooling suites that go green together, which is the signature of
one round landing its half of a change between the two runs. **The two runs are not even at
the same commit**: another round committed `0dd9bb2` in the gap, which is the point made
concretely rather than argued.

**Run 2 is the state the next session should start from: 154/154, 5,100 checks, 5 rounds in
flight at 19:57.**

### The finding that matters more than the counts

The brief calls these reds "standing across multiple rounds, each attributed and left". The
measurement says something different and more useful: **the red set is not stable between
runs, because the tree is not stable between runs.**

- The brief's three: `guard_resolution`, `render_argv`, `song_library_meme_rule`.
- My first (discarded) run's three: `config_contract`, `guard_resolution`, `message_template`.
- Clean run 1's four: `claims_manifest`, `manifest_prose_refused`, `market_filter`,
  `verify_claims`.
- Clean run 2's: **none**.

**Four different answers in one evening, and the only overlap across the first three sets is
`guard_resolution`, which I caused myself.** Every one of those suites was green when run
standalone, minutes apart.

`tests/run_all.py` already documents exactly this at line 189 (BL-892 → BL-901 → BL-903 →
BL-906): *"With a dozen rounds writing concurrently the thing being measured changes faster
than the measurement takes to run."* BL-903 sampled the tree for 60 minutes and never saw two
consecutive identical hashes.

**And I caused it twice myself.** My first run started 19:31:10 and I committed edits to
`tests/test_guard_resolution.py` at 19:36:02 while it was executing — the giveaway is that the
run recorded *11 checks* for a file that had 8 tests when the run started. An earlier
background run did the same. Both were discarded and the pair below was taken with my own
files committed and untouched throughout.

So BL-871's point stands — standing red trains people to ignore red — but the mechanism here
is not "nobody fixed them". It is that **a red taken on a moving tree is not evidence a suite
is broken**, and the honest unit is a suite run standalone, or a full run whose start and end
commit are the same. The runs below record `HEAD` and the live-claim count at start for
exactly that reason.

---

## 5. INFRA-018's finding, recorded beside the guards

Already there, and left as INFRA-018 wrote it (lines 105–117) — the measurement, the split,
and the example:

```
AST forms  10/10 correct
text forms  3/10 correct
```

The seven the text forms got wrong split **both ways**: they PASSED a governor that was defined
and never called (a write-only cap — the exact defect `tests/test_caps.py` exists to prevent)
and a counter that survived only in a comment; and they FAILED a reformat, a variable rename,
and a docstring that correctly documented a removal.

One of them could only ever pass by slicing the documentation out of the file first —
`src.split('"""', 2)[-1].split("# NOTE")[0]` — which also left **~1,350 of
`repost_finder.py`'s lines unsearched**, so a real resurrection of the knob went undetected.

**That single expression is the whole class argument.** It punishes a correct comment and
misses the bug, in the same line, for the same reason: it is reading characters where it means
to ask a question about code. A parser cannot make that trade because it never sees the comment
in the first place.

---

## Verification

| check | result |
|---|---|
| three named reds, on arrival | **all green standalone** — 8/8, 8/8, 0 failures |
| baseline staleness check | **correct but unreachable**, measured before any edit |
| `EXEMPT` staleness check | **did not exist**; its one entry was **REDUNDANT** |
| tree scans to zero text guards with `EXEMPT` emptied | **0** |
| new checks mutation-proven | **4 of 4 go red** |
| `test_guard_resolution.py` | **8 → 11 tests, green** |
| `test_render_argv.py` | 8/8 green, note corrected |
| meme-rule packet | intact; zero-regression holds on **2,661** clips (was 2,603) |
| `config.json` | parses, 161 keys, `spend_cap_usd` 50.0 |
| campaigns | **5, unchanged** — ZHUS 216, PANICBABY 1811, STRAENGE 113, DAYLIGHT 95, ANIME15K 5 |
| full suite, run 1 | 4 of 154 red, 628.7s, `HEAD=77abed2` |
| full suite, run 2 | **ALL GREEN — 154/154, 5,100 checks**, 527.5s, `HEAD=0dd9bb2` |
| paid calls | **none** |

## Limits

- **A suite count is still a moment.** Both runs below were taken with my files committed and
  untouched, but a dozen other rounds were writing throughout, and the live-claim count is
  printed with each. Neither number is a property of the tree.
- **The reds I did not own are not diagnosed here.** I established they are green standalone
  and that the set moves between runs; I did not chase whose in-flight edit caused which. They
  are named in the runs below with their owners where a claim exists.
- **`dead_exemptions`' REDUNDANT arm depends on `scan()` being right.** If `scan()` ever
  under-reports, a genuinely load-bearing exemption would be called redundant and deleted, and
  the next text guard in that function would go unnoticed. The mechanism test pins the three
  cases apart, but it cannot pin `scan()` itself — `test_the_detector_fails_on_a_planted_text_guard`
  is what does that, and it remains the only thing that does.
- **I did not touch the six untracked test files** in `tests/` (other rounds' in-flight work).
  They scan clean for text-resolved guards, which is the only question this round asks of them.
