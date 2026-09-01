# BL-1481 — thirty things were tested against the belief that they work; twenty-five do not

## HOW MANY THINGS THIS PROJECT BELIEVES ARE WORKING THAT ARE NOT: **25 of 30 tested.**

That number is derived from the table in §2, not asserted. Denominator: 30 specific mechanisms
this project believes are working, each tested by running it. Five behave as believed. Twenty-five
do not.

## IS THE FUNNEL SAFE TO RUN? **NO.**

Four of the twenty-five cost money or corrupt decisions the moment a run starts:

1. **A zero lifetime spend cap still means NO CEILING.** `spend_cap_usd: 0` returns
   `run_budget_usd: None`. Believed fixed three times.
2. **A live language gate fails open silently.** One broken import and every foreign-language page
   passes, with no log and no counter.
3. **The field a live gate reads as "the sampled mean views" is one video's view count**, on
   100.0% of 55,766 populated rows.
4. **Three runs on 30–31 August wrote `"complete": true` with `videos: 0`** while all 15 vendor
   calls were refused and billed.

---

# 1. ROUND ID, DATE, AND WHAT I WAS ASKED TO DO

**BL-1481 · 2026-09-01 · read-only · no production file written.**

I was asked to assume nothing works until I had seen it run: audit the test suite itself by
mutation, verify every fix believed shipped with a runtime spy, hunt code that reports success
without doing anything, find the code shapes that generate wrong numbers, and check the
documentation against the code. Five sub-agents ran the five parts; I re-derived the headline of
each myself.

⚠️ **The repository moved under this round.** HEAD went `88429d8` → `da30cef` → `c69fdd7` →
`5a2f11f` while the work ran — four commits from three other rounds. **Every line number below is
recorded against the sha it was read at (`88429d8` unless stated).** A prior round here published
stale line numbers from a file that moved mid-audit; this is the guard against repeating it.

**Environment at filing:** 9 peer sessions live, plus this one. ⚠️ **A session-NAME collision is
live** — two distinct sessions share one name, so any message addressed by name rather than by
pipe address is ambiguous.

---

# 2. THE TABLE — EVERY THING BELIEVED TO WORK, AND WHETHER IT DOES

Each row was tested by RUNNING it. No row rests on a grep, a docstring, or a passing test.

| # | believed to work | does it? | proved by |
|---|---|---|---|
| 1 | Zero-cap guard (fixed 3×) | **NO** | `resolve_budget({spend_cap_usd:0})` → `run_budget_usd: None`; `5.0` → `5.0` (control fired) |
| 2 | Key-name mismatch fixed (3×) | **NO** | `his_rules_say(shipped dict)` → `PASS`; `{views:1,video_count:1}` → `BAD` (control) |
| 3 | Encoder crop fixed | **NO** | 311px 1-tile sheet: unset → **103×183**; `tiles=1` → **311×552** |
| 4 | Dead judge primary removed | **YES** | absent from chain, `MAY_REJECT`, `askable_models()`; preflight WARNs on a bare declaration |
| 5 | Test marker gone from renderer | **NO** | 3 copies present in the working tree today |
| 6 | Nested-payload reader adopted | **NO** | `envelope.read()` correct on 8 shapes; **0 production callers** |
| 7 | Adult-content safety flag | **NO** | all three keywords together → `False`; keyword list has **0 production readers** |
| 8 | Preflight returns SKIPPED not OK | **YES** | returns `SKIPPED`, counted separately; production caller now exists |
| 9 | "Armed" asserts reachability | **YES** | unset → WARN; `[]` → FAIL "not one of them answered" |
| 10 | Free-side `source` field honest | **YES** | all 3 states fire under a real DOM; 310 of 360 false records all pre-date the fix |
| 11 | Envelope surfaces vendor errors | **NO** | 2-of-20 + "No more videos" → `state=ok, is_failure=False` |
| 12 | `complete` means complete | **NO** | 3 runs `complete=true, videos=0`, 15 calls billed and refused; **`complete` has 0 readers** |
| 13 | Run markers reflect liveness | **NO** | **60 say running, 59 processes dead**; one shows **$4.6272 over 19.1 h** |
| 14 | The GC frees disk | **NO** | quarantine = **20,169 files / 19.91 GB inside the repo, same volume**. A rename |
| 15 | Silent handlers are bounded | **NO** | 409 of 1,249 strict; 945 of 1,249 loose — **the gap is open, see §5** |
| 16 | Language gate cuts foreign pages | **NO** | cuts normally; **returns True with one import broken**, no log, no counter |
| 17 | Every test file is collected | **YES** | 427 on disk under live `tests/`, **427 collected, difference 0** |
| 18 | Every defined test runs | **NO** | **25 methods** defined after an exiting `__main__` guard; suites print OK |
| 19 | A passing test guards its subject | **NO** | **3 of 13 mutations SURVIVED** deletion of the behaviour |
| 20 | Reported check counts are checks | **NO** | the runner counts a **skipped** test as a check; no skip count printed |
| 21 | Suite is "94 of 425, 3 failures" | **NO** | **427 suites, 16 failures**; 12 red at HEAD itself |
| 22 | Rate figures carry a median and an n | **NO** | 6 single-quotient generators live; 2 correctly cleared |
| 23 | `avg_views_sampled` is a mean | **NO** | **== one video's count on 55,766 of 55,766 = 100.0%** |
| 24 | Gates read the right statistic | **NO** | two live cuts read a MEAN with the median one line away |
| 25 | The drift guard catches drift | **NO** | fires at 25%; live drift **15.78% / 19.36%**; returns 0 problems |
| 26 | Docs describe the architecture | **NO** | four-brain split: **0 hits in docs**; one doctrine doc asserts the opposite |
| 27 | NO-SEND is enforced | **NO** | **no code anywhere**; 5 docs instruct sending, 3 committed **82m53s** before the rule |
| 28 | The Instagram price in docs is current | **NO** | **three different values**, and the correcting doc is now wrong the other way |
| 29 | Supersession travels | **NO** | `superseded_by` filled on **5 of 1,042**, and has **no reader** |
| 30 | The report corpus is one application | **NO** | **276 of 1,042** belong to another app; **131 ticket numbers collide** |

**5 YES · 25 NO.**

---

# 3. WHAT WAS MEASURED

Every rate carries its denominator. Deterministic measurements are marked as such — a Wilson
interval on a deterministic pixel or file count is meaningless and none is invented.

| figure | value | denominator | status |
|---|---|---|---|
| Test files on disk under live `tests/` | 427 | os.walk, whole repo | MEASURED |
| Test files the runner collects | 427 | runner's own discovery | MEASURED |
| **Files wired to nothing** | **0** | 427 − 427 | **REFUTES the belief of 34** |
| Test files in deliberately skipped trees | 407 | os.walk | MEASURED |
| Test methods never bound (after `__main__`) | 25 | 6 classes in 3 files | MEASURED |
| Source-text tests | 493 = **6.2%** | **7,923** tests in 427 files | MEASURED |
| Files containing ≥1 source-text test | 169 | of 427 | MEASURED |
| **Mutations that SURVIVED** | **3 of 13** | 13 attempted, 1 unmeasurable | MEASURED |
| Suite result | 411 pass / **16 fail** | 427 suites, 9,885 checks | MEASURED |
| Failures red at HEAD itself | 12 of 16 | clean archive extract | MEASURED |
| `avg_views_sampled` == one video's count | **55,766 of 55,766 = 100.0%** | rows with BOTH fields populated, of 72,954 | MEASURED, re-derived |
| Rows whose "sample" is 1 video | 53,825 = **96.5%** | 55,771 non-empty | MEASURED, re-derived |
| Run markers saying `running` | 60 | 206 markers | MEASURED |
| …whose process is dead | **59 of 60** | 1 alive = control | MEASURED |
| Spend on one latched marker | **$4.6272 over 19.1 h** | one marker | MEASURED |
| GC quarantine | **20,169 files / 19.91 GB** | inside repo root, same volume | MEASURED |
| Net disk freed by the GC | **0 bytes** | a move is a rename | DERIVED |
| Silent handlers, STRICT predicate | 409 = 32.7% | **1,249** handlers in 120 reachable modules | MEASURED |
| Silent handlers, LOOSE predicate | 945 = 75.7% | same 1,249 | MEASURED |
| Live drift vs the 25% guard | total **15.78%**, IG **19.36%** | ledger vs docs | MEASURED |
| Instagram price, live | **$0.00069064** | `config.json` | MEASURED |
| Manifest rows | **1,042** (not 1,032) | manifest | MEASURED |
| …belonging to another application | **276** | of 1,042 = 26.5% | MEASURED |
| …colliding ticket numbers | 131 | across the two apps | MEASURED |
| `superseded_by` filled | 5 of 1,042 = **0.48%** | manifest | MEASURED |

**Median and tail, where the distinction is the finding:** the `judge_prepass_per_min` generator
emits one quotient with no median and no n; the value on disk is **41.17** and prior observed
values span **10.48 to 126.09**. A single figure from that spread is not a rate — that is the
defect, and it is why no median is available to quote.

**NOT MEASURED, and named rather than filled in:** whether the earlier 999/783 silent-handler
predicate reproduces at this sha (the script is unavailable); whether the three zero-video runs
incremented the ledger or only a call counter; run-to-run spread of the per-minute generator (one
value on disk); how many of the other 491 source-text tests survive a dead-branch mutation
(n=2 tested, both survived — **not extrapolated**).

---

# 4. WHAT WAS REFUSED OR NOT DONE

- **No production file was written**, and none of the 25 defects was fixed. They are named with
  `file:line` and left, as instructed.
- **The silent-handler gap was NOT resolved by picking a number.** 409 (strict) and 945 (loose) on
  the same 1,249 denominator bracket the prior 431 and the earlier 999/783 differently. Different
  predicates, denominators and shas. **409 neither refutes 999/783 nor supersedes 431**, and the
  round says so rather than crowning a winner.
- **Two agent results were discarded because their controls failed**, not reported with a caveat.
  See §5.
- **No vendor call was made.** The $0.25 allowance was untouched; no model was called, paid or
  free.
- **Nothing was killed.** Four expected listeners were confirmed present via the listening-port
  table — never a command-line process grep, which has previously matched the checking process
  itself.

---

# 5. WHAT I GOT WRONG

**My own instrument failed first, and it failed in the exact way this round exists to find.**

**1. I read a key that does not exist and reported it as a value.** Re-deriving the zero-cap
finding, I read `lifetime_room` from the returned dict. The real key is `lifetime_room_usd`. The
function returned `None` for **every** input — including `5.0` and `100.0`, my own positive
controls. Had I not noticed the controls were flat, I would have published "the zero-cap guard is
fine." The corrected run shows `0 → None` and `5.0 → 5.0`. **A true value about the wrong thing.**

**2. My arithmetic and the documentation's disagree, and the documentation is the loose one.** The
stale Instagram price is `$0.0006` and the live one `$0.00069064`.

    ratio true/stale                    = 1.1510667
    increase needed on a stale figure   = 15.107%
    stale figure as a shortfall vs true = 13.124% BELOW true

A doc states *"every Instagram figure on record is 15.1% LOW."* **15.107% is the increase needed;
the shortfall is 13.1%.** Same gap, two quantities, and the larger one is named as the error size.
My own script printed 13.1% while the sub-agent reported 15.1% — both true, describing different
things. This is the interpretive-clause failure this project keeps repeating, inside a correction.

**3. A sub-agent's first mutation result was an artefact of its own tool.** Its `ast.unparse`
mutation returned FAILED — apparently a real test. Its identity control (parse and unparse with
**no mutation**) showed the suite goes red on a pure reformat, because it greps for a quoted
string and unparse normalises quotes. **Both results were dropped and redone byte-preserving.**
Reported here because a discarded result that would have been a false positive is worth more than
a clean-looking table.

**4. A sub-agent's first inventory pass reported "83 tests never called" for one file** — it had
read only the `__main__` guard body and not the helper that guard calls. **The auditing instrument
committed the error it was auditing.** Discarded and redone.

**5. A minor discrepancy I resolved rather than averaged.** My skipped-tree count was 407; the
sub-agent's was 406 plus 1 file outside any `tests/` directory. Same 407 files, a boundary
difference on one. Stated rather than smoothed.

**6. The publication scanner failed its own control, during publication of this report.** The
first version was typed through a shell heredoc, and the shell ate a backslash out of the
username-path pattern. The detector then could not match a username path at all — and **it failed
its positive control and aborted the publish**, which is the only reason it was caught. Had the
controls been decorative, this file would have shipped with a redaction detector that could not
detect anything, reporting a clean zero. Rewritten to a file, building every backslash from
`chr(92)`; all six detectors then fired. **The defect this report documents fired inside the
instrument verifying this report, at the last possible step.**

**7. Three of the brief's own premises did not survive testing** — and saying so is part of the
job: "34 test files wired to nothing" is **refuted** (427 collected of 427 on disk); "94 of 425
with three failures" is **refuted** (427 suites, 16 failures, none of the three named causes among
them); and the manifest denominator is **1,042, not 1,032**.

---

# 6. MONEY AND SAFETY

**Vendor spend: $0.00, from the run's own counter.** No vendor call of any kind was issued by this
round or by any of its five sub-agents. This is not a ledger delta — the shared ledger carries a
round id on zero rows and has been observed moving during a round that made no calls.

**Seen stores, re-read at publication time, not only at check time:**

| store | pages at publication | attributable to this round |
|---|---|---|
| meme pages | 6,058 | **0** |
| tiktok pages | 2,446 | **0** |
| clip seen | 2,193 | **0** |
| spotify playlists | 3 | **0** |

⚠️ **Stated as attribution, not as state.** The meme store grew from 6,044 to 6,058 during this
round — by a peer, not by me. The provable claim is *zero attributable to this round*: it issued
no vendor call, ran no funnel, and wrote only its own report and its own scratch files.

**Disk: 385.46 GB free at start, 385.26 GB at publication.** Re-read before every write phase.
A sub-agent created a 333 MB sandbox and a 1,149 MB clean-commit extract for mutation testing and
**deleted both on completion, verified after.**

**Processes: none killed.** The four expected listeners were confirmed present at publication via
the listening-port table.

**Campaigns fingerprint: UNCHANGED**, reproduced rather than quoted —
`8e02f8d6f6307ae8` (default separators) and `7a029ee5447cddd8` (compact). Both are the same object
under two encodings; a bare hash without its encoding is not a fingerprint.

⚠️ **An orphan hazard the registry cannot see.** Two production files carry uncommitted work that
**no in-flight claim declares**: **+45/−9 over 2 hunks** in one vendor client and **+136/−17 over
3 hunks** in one funnel — 181 added lines. A broad commit sweeps them in; a checkout destroys
them. Three dashboard state files are in the same condition.

**Public-repo scan — every detector proven on a positive control before its zero was believed:**

| detector | control | fired? | findings |
|---|---|---|---|
| email address | synthetic address | YES | **0** |
| API key / bearer | synthetic key | YES | **0** |
| username in an absolute path | synthetic path | YES | **0** |
| port number | synthetic port | YES | **0** |
| creator handle | synthetic handle | YES | **0** |
| C0 control bytes (excl. tab/LF/CR) | synthetic NUL + backspace | YES | **0** |

The C0 assertion runs **before the file is published**, and on any finding the local file is
deleted rather than left for the next command to publish — a post-write assertion is only a
safeguard if something reverts on failure.

---

# 7. WHAT HE SHOULD DO NEXT — RANKED

**1. Make the zero-cap guard general, not local.** `spend_cap_usd: 0` yields no ceiling. It has
been fixed three times at three call sites and the dangerous default survived each time. The
general form: a cap of `0` must mean *zero dollars*, and "no cap" must be a distinct value that
the budget resolver **refuses** when real money is in play. One boundary assertion in the resolver
replaces three call-site fixes.

**2. Rename `avg_views_sampled`, or make it a mean.** It is one video's view count on 100.0% of
55,766 rows; 96.5% of its "samples" are a single post. A live gate cuts leads on it while its
docstring says it gates on the sampled mean, and the export renames it to include the word MEAN.
Cheapest correct move: rename the field to what it is at all four writers, and let the gate fail
loudly on the old name rather than silently on the old meaning.

**3. Close the fail-open gates.** `except Exception: return True` inside a gate predicate converts
a dead dependency into a passed page. Two are live in the language gate; more are listed. The
general fix is a boundary rule — **a gate predicate may not have a bare fall-through return of
`True`** — enforceable as one AST test over the gate modules.

**4. Give `complete` and the run markers a reader, or delete them.** `complete: true` with zero
videos and 15 refused billed calls is written by code nothing reads. 60 markers say running and 59
of those processes are dead. Either something consumes these and acts, or they are removed so
nobody mistakes them for a signal.

**5. Pin the doc numbers to the code.** One new test file, ~70 lines, plus an invisible pin comment
beside each number in the docs; resolve each pin by AST without importing; assert **exact
equality, not a tolerance band**. The tolerance band is not a hypothetical — the existing drift
guard exits 0 printing *"ledger and prose agree"* while a doc is 16% wrong, which converts "nobody
checked" into "somebody checked and it was fine." This would have caught the three-way Instagram
price including the double-counting correction, the wrong spend cap, the master row counts and the
three conflicting spend totals. Three ~5-line complements in the same file catch the missing
architecture docs and the send instructions.

**6. Decide the silent-handler question with one predicate.** Three counts exist across four
rounds and none supersedes another because each used a different predicate and denominator. Fix
the predicate first, publish it, then the number means something.

---

# 8. FULL PATHS

`%USERPROFILE%` expands in File Explorer, so these paste without publishing a username. **No port
numbers appear in this file** — they are not stable across runs. Services are named by launcher.

| what | path |
|---|---|
| Project root | `%USERPROFILE%\OneDrive\Desktop\clipper finder` |
| This report | `...\reports\BL-1481-thirty-tested-twenty-five-do-not-work.md` |
| Budget resolver (zero-cap) | `...\clippershq\clip_pipeline.py` |
| Image encoder and prompt builder | `...\clippershq\free_judge.py` |
| TikTok funnel, language gate, complete flag | `...\clippershq\tiktok_finder.py` |
| Instagram funnel | `...\clippershq\meme_finder.py` |
| Vendor envelope reader | `...\clippershq\envelope.py` |
| Preflight checks | `...\clippershq\preflight.py` |
| Run markers | `...\clippershq\run_status.py` |
| The GC that moves instead of deleting | `...\tools\scratch_gc.py` |
| The 25% drift guard | `...\tools\facts_guard.py` |
| Test runner | `...\tests\run_all.py` |
| Docs audited | `...\docs\` |
| **Dashboard launcher** (start here; do not bookmark an address) | `...\dashboard\dashboard_launcher.py` |
| This round's evidence | `...\scratch\bl1481_*` |

---

*Five sub-agents ran the five parts. Every headline was re-derived a second way by the
orchestrator. The most useful section is §5.*
