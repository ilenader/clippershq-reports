# BL-1487 — The four dangerous defects, driven rather than read

## IS THE SYSTEM PRODUCTION-READY? **NO — BUT IT IS CLOSER, AND THE REMAINING GAP IS NAMED.**

Three of the four defects I was asked to fix are fixed, and each is proved by driving the real
code path with a positive control beside it. The fourth was handed to another live round by
agreement and is not mine to claim. The test runner no longer counts a skipped test as a
check, and no longer scores a suite green while 25 of its test methods never bind.

It is **not** production-ready, for three reasons stated plainly:

1. **The tree has 16 red suites at HEAD, not the 12 the brief expected.** I fixed three. The
   remaining 13 are named below with owners; four belong to a round editing that file *now*.
2. **Three of the five stage counters are still measured by nothing.** They are declared, they
   are honest about being unmeasured, and the screen says "not yet" instead of showing a zero
   — but "the run is 40% through judging" remains unanswerable.
3. **Five rounds were writing this repository while I worked**, and one rewrote a file I hold
   four separate times. Only the things I drove myself are load-bearing here.

---

## 1. ROUND ID, DATE, AND WHAT I WAS ASKED TO DO

**BL-1487**, 2026-09-02. Asked to fix four defects described as dangerous today, make the test
suite honest, make the operator UI production-ready, and correct misleading documentation.

**THE ROUND NUMBER COLLIDED WHILE I WAS READING.** I opened on BL-1486 as the next free id and
verified it free in all three namespaces; by the time I finished reading the registry another
session had taken it. I moved to BL-1487. Rounds live at the moment I filed:

| round | filed | holds | overlap with me |
|---|---|---|---|
| BL-1377 | **243 h stale** | its own report | none |
| BL-1484 | 16:56 | `tiktok_finder.py`, `control.py`, `config.json` | **direct** |
| BL-1485 | 16:58 | read-only | none |
| BL-1486 | 17:00 | `meme_finder.py`, `tools/exemplar_review.py` | none |
| BL-1488 | 17:06 | read-mostly, `tools/health_check.py` | none |

**THE HANDOVER, AGREED WITH THE OPERATOR BEFORE I EDITED ANYTHING.** BL-1484's filed intent
names two of my four items almost word for word — "stop `complete: true` with zero videos and
refused vendor calls" and "render the EFFECTIVE value at control.py:420". I left **both** to
BL-1484 and wrote neither `control.py` nor `config.json` at all. I took the two defects inside
`tiktok_finder.py` that its intent does **not** name. The handover is recorded in the claim
record, and I messaged BL-1484 to say exactly what I had touched.

**LIVE-PROCESS CHECK, BY THE LISTENING-PORT TABLE, NEVER A COMMAND-LINE GREP.** At round start
ports 8000-9100 carried one listener (Docker) and there were **zero python processes**. No
dashboard, no sheet servers, no funnel. I re-checked before every write under the dashboard
directory. By mid-round fourteen python processes and a new listener had appeared from other
rounds; I killed none of them.

**BACKUPS: 8 of 8, sha256-VERIFIED AGAINST SOURCE**, not assumed — config, ledger, master
leads, and all five seen stores.

---

## 2. WHAT ACTUALLY SHIPPED

| # | change | where | fix category |
|---|---|---|---|
| 1 | `lifetime_cap_declared()` — one chokepoint; a declared `0` and an absent key stop being the same answer | `spend_ledger.py` | **GENERAL** — safer default + single chokepoint |
| 2 | six truthiness sites routed through it | `finder_common.py`, `spend_ledger.py`, `clip_pipeline.py`, `main.py` x2 | **GENERAL** |
| 3 | `over_budget()` lifted out of a closure so it can be driven | `main.py` | **GENERAL** — testability |
| 4 | language gate RAISES, counted, loud; `language_unjudged` as a fourth state | `tiktok_finder.py` | **GENERAL** — boundary assertion |
| 5 | `avg_views_ok(..., n_posts=)` now **required** | `filters_free.py`, `main.py` | **GENERAL** — required argument |
| 6 | runner prints skips separately and stops counting them as checks | `tests/run_all.py` | **GENERAL** |
| 7 | a test method that never binds FAILS its suite loudly | `tests/run_all.py` | **GENERAL** — structural, every suite forever |
| 8 | `update()` warns and counts a dropped key | `run_status.py` | **GENERAL** |
| 9 | `set_stage_counts()` refuses an unknown stage name | `run_status.py` | **GENERAL** — required argument |
| 10 | effective per-campaign value on the settings screen | dashboard server + app script + stylesheet | LOCAL to that panel |
| 11 | hidden-tab guard, the pattern the board script had and the app script never did | dashboard app script | LOCAL |
| 12 | the sheets launcher reads both exit codes | `SHEETS.bat` | LOCAL |
| 13 | `test_bl1443_lifetime_cap.py` made able to test the thing it exists to test | `tests/` | **GENERAL** |

Of thirteen, **nine are general** by the brief's own test — a required argument, a safer
default or a boundary assertion, not a docstring or a note. Four are local, and I say so.

---

## 3. WHAT WAS MEASURED

### 3a. The zero lifetime cap — DRIVEN, not read

I found the defect live at **six** sites, one more than the brief listed:

| site | expression | a cap of literal `0` gave |
|---|---|---|
| `finder_common.py:262` | `if not lifetime_cap:` | no ceiling |
| `spend_ledger.py:390` | `if not cap: return False` | uncapped |
| `spend_ledger.py:418` | `if lifetime_cap and spend_path:` | room dropped |
| `clip_pipeline.py:3941` | `if lifetime_cap and spend_path:` | room dropped |
| `main.py:5115` / `:5259` | `or None`, then `if spend_cap` | dropped from `min()` |
| **`main.py:2410`** | `if not _b: return False` | **the live mid-run governor switched OFF** |

The sixth was in no brief and is the worst: a resolved budget of `0.0` disabled the governor
entirely — precisely when the operator had asked for a hard stop.

**WHY IT CAME BACK THREE TIMES.** Every previous fix was local. BL-1454 converted the *per-run*
half of `effective_run_cap` to presence, wrote a long comment saying "a zero is an answer, not
a silence", and then tested the *lifetime* half with `if not lifetime_cap:` **eight lines lower
in the same function**. The fix and the bug shipped in one stanza. That is why this is one
resolver with callers and a test, not a seventh repair.

Driven with a positive control on every case: **13 of 13 pass, every control fired.**

### 3b. The language gate — loud, counted, and a fourth state

An AST census found the `except: return True` shape at **5 sites** repo-wide; two sat inside a
live gate predicate. Any failure inside the lazily-imported meme module admitted **every** page
with no log and no counter.

It now raises a dedicated exception, increments a counter, prints on the 1st, 2nd, 3rd and
every 100th occurrence, and the call site records `language_unjudged` on the verdict.

**IT IS NOT A REJECTION EITHER.** A dependency failure is not evidence about a page. The page
keeps its other verdicts and is not cut on language. Nothing latches: after 12 consecutive
failures a working gate works again on the next call, and a test asserts exactly that — because
a spy that raises instead of returning has latched a gate off in this project before.

### 3c. The views statistic — and I am CORRECTING the headline figure

The field is written by four sites carrying three statistics: mean, mean, median, and **one
video's view count** (where the single-video column is tried *first* in an `or`). A **passing
test pins the last one**. The export renames the column "MEAN".

**THE BRIEF SAYS 100.0% ON 55,766 OF 55,766 ROWS. THAT READING IS NOT INDEPENDENT EVIDENCE.**
It compares the single-video column against the mean column — and a backfill in the writer
**copied one column into the other**. The identity is the backfill's own signature.

Re-derived a second way, on the field's own `n`:

| quantity | value | denominator |
|---|---|---|
| master rows | 72,954 | — |
| rows carrying the field | 55,766 | **76.44%** of 72,954 |
| of those, **n = 1** | **53,825** | **96.52%** of 55,766 |
| n median / mean / max | 1 / 1.052 / 14 | — |

So: **96.52%, not 100%**, and the honest denominator is the 55,766 rows that carry the field —
itself only 76.44% of master. Quote 96.52%.

**THE FIX MOVES NO VERDICT, DELIBERATELY.** The gate now *requires* `n_posts`, so a caller that
does not know its own n fails loudly at the call. The pass/fail arithmetic is byte-identical: a
210-cell grid test asserts the new function agrees with the pre-BL-1487 decision on every
combination of value, floor, policy and n. Only the reason string gained the statistic's name.

**THEREFORE THERE IS NOTHING TO SCORE ON HIS MARKS.** The brief asked me to score a moved
verdict with Wilson bounds against a constant-answer baseline. **No verdict moved, so that
scoring would be theatre, and quoting it would manufacture a result.** Requiring `n >= 2`
*would* move it and would cut 96.52% of master; that is a judging-rule change, his to approve,
and I did not take it.

### 3d. `complete: true` with zero videos — NOT MINE

Held by BL-1484, which named it in its own filed intent. Not duplicated. **Unverified by me**;
this report is not evidence about it either way.

### 3e. The test suite

- **A skipped test was counted as a pass. CONFIRMED.** The runner scraped `Ran N tests`, and
  unittest includes skips in that number. Skips are now subtracted and printed on their own
  line, pass or fail.
- **25 test methods never bind. CONFIRMED, and it is ONE shape in THREE files** — definitions
  after a module-level main guard, which `unittest.main()`'s `sys.exit()` never reaches. The
  arithmetic closes exactly: 35+27+39 = 101 defined, 28+24+24 = 76 ran, **101 − 76 = 25**. All
  three printed OK. The runner now fails such a suite and names every lost method. The other
  three shapes I tested for — duplicate method names, `test_*` on a non-TestCase, orphan
  top-level `test_*` — came back **0, 0, 0**.
- **"34 test files wired to nothing" is REFUTED**: 427 on disk, 427 collected, difference 0.
- **The real state is 427 suites with 16 failures, not 12.**

### 3f. The frame-extractor red — REFUTED

The brief calls it known and orphaned. It is **already fixed**: the extractor calls a retrying
atomic remove, committed by BL-1477, and its covering suite is green. A repo-wide AST sweep for
an unguarded delete inside a loop returns exactly one hit, and that one passes
`ignore_errors=True`. **Zero unguarded.**

### 3g. The UI, in a real browser

Chrome, every page opened and looked at. **A syntax check passes on all four shipped scripts**
— the apostrophe SyntaxError the brief describes is historical, not current.

- **All 12 pages paint. None sits at "loading".**
- **Console: zero real messages across the whole walk.** That zero is worth something only
  because I planted an error first and confirmed the reader saw it. A clean console from an
  unproven detector is not evidence.
- **The hidden-tab guard, driven with a fetch spy:** visible poll **18** fetches (control
  fires), hidden poll **0**, hidden *first* load **18** — it does not swallow the initial call,
  which is the bug the board script's own comment records — and returning to the tab re-fetches
  (**18**).
- **`None` vs `0` is ALREADY distinguished in three layers** (file, server, page). A measured
  zero prints `0`; an unmeasured one prints "not yet". That part of the brief is **refuted**.

### 3h. The effective value, proved by a spy

The overlay constant and its single consumer function are BL-1484's work, and that constant's
comment says outright that a renderer which reimplements the list will drift from it. So the
dashboard **calls** it. The settings screen now shows, per campaign, the value that will
actually be used and where it came from.

The spy copies the config, edits the **copy**, points a second server at it via the env var the
path resolver exists for, and reads the answer back over HTTP:

| campaign | before | after top-level switch set true |
|---|---|---|
| campaign 1 | *not set anywhere* (code default) | **true** — top-level overrides |
| campaign 2 | false (this campaign) | **true** — top-level overrides |
| campaign 3 | false (this campaign) | **true** — top-level overrides |
| campaign 4 | false (this campaign) | **true** — top-level overrides |
| campaign 5 | false (this campaign) | **true** — top-level overrides |

**5 of 5 moved.** One switch makes the garbage-cut live on every campaign at once, including
four that explicitly say `false`. The real config was byte-identical afterwards.

On the live config the screen now flags **exactly one** genuine disagreement: the garbage-cut
enable shows blank while four campaigns hold `false` and the fifth has no value in any file.

### 3i. What the live view costs

Timed both arms, interleaved, median and tail separately:

| arm | n | median | p90 | p99 |
|---|---|---|---|---|
| live view OFF | 900 | 0.121 ms | 0.183 ms | 0.282 ms |
| live view ON | 900 | 2.990 ms | 3.634 ms | 4.682 ms |

**One status write costs 2.869 ms (median).** Against a funnel tick of ~1000 ms that is
**0.287%** — comparable to the 0.7% a previous build measured.

**NAME THE DENOMINATOR:** the 1000 ms tick is an **assumption**, not something I measured. The
defensible number is the absolute 2.869 ms. The percentage against my own synthetic workload
(+2370%) is meaningless and I am not quoting it as a result.

My first version cost **6.001 ms** because the counter setter rewrote the file a second time
every tick. Removing that halved it.

---

## 4. WHAT WAS REFUSED OR NOT DONE

- **`complete: true` with zero videos**, and the control-panel effective value — left to
  BL-1484 by agreement. Not duplicated, not verified by me.
- **The config file — NOT TOUCHED.** It is held, and on the one figure in question it is
  **correct**. The facts document was the wrong one.
- **The meme finder — NOT TOUCHED.** Held by BL-1486.
- **Requiring `n >= 2` on the views gate** — would cut 96.52% of master. His call.
- **Making a malformed cap or an unreadable ledger fail CLOSED** — I tried both and **backed
  out of both** (see section 5). Recommended, not taken.
- **The drift threshold left at 25.0.** Lowering it would redden the tree on the very commit
  that arms the guard, bundling two decisions.
- **No screenshot is published.** They are clean to the eye, but a JPEG's compressed bytes trip
  a regex by chance, so I cannot *prove* an image clean the way I can prove text clean. They
  are on his machine under the scratch directory.
- **No `/T` added to the launcher's `taskkill`.** The brief is right: the "spawned DETACHED"
  reason was false, the detach helper says so itself, and what protects live runs is the
  missing `/T`. It is still missing, deliberately.
- **No launcher deleted.** 43 exist for three real doors; three look redundant and are
  load-bearing — one pinned by 3 tests, two pointing at directories the sheet tool cannot
  discover. Proposal only.

---

## 5. WHAT I GOT WRONG

**Five things — three caught by my own instruments, two by other people's tests.**

1. **I reversed a settled decision I was not asked to touch — twice.** I made an unreadable
   ledger fail closed, and a malformed cap refuse. Both are *defensible* policies and both were
   **already decided deliberately, with tests on them**. Both went red immediately. I restored
   both directions and kept only the part that was actually missing: the silence. This is the
   failure mode where a "fix" becomes the next round's defect, and I walked into it twice.

2. **My own fix returned a negative budget.** With a declared cap of `0` against a $10 ledger,
   `cap − spent` was **−10.0** and `min()` propagated it as the run budget. Caught by the
   driver on its first run, not by reading. Clamped.

3. **My loud warning crashed the run.** The warning line used a warning glyph and an em-dash
   and raised `UnicodeEncodeError` on a cp1252 console. A warning that kills the run is
   strictly worse than the silence it replaced, and it would have fired only in production and
   only when something was already broken. Both loud lines are now ASCII.

4. **My mutation harness reported a false SURVIVED.** Mutating `+= 1` to `+= 0` is the *same
   byte length*, so with an unchanged mtime-second CPython reused a stale bytecode cache and
   the mutation never ran. The harness now purges the cache and disables bytecode writing.
   Suspect your own instrument.

5. **My config spy read the wrong file and nearly published a false negative.** I typed an env
   var name that does not exist. The server read the *real* config, nothing moved, and the spy
   was about to report "the screen does not follow the config". A wrong key name returns a
   plausible answer for every input, controls included. It now imports the constant instead of
   typing it.

**And one thing I nearly got wrong in the UI:** my first effective-value pass produced **22
warnings of which one was real**, because it treated block-scoped settings as
campaign-overridable. Twenty-two loud rows bury the one that matters — the same
loud-and-unread failure this project has already measured. It now warns on 1.

**One equivalent mutant, reported rather than hidden.** In the governor, the `<= 0` branch is
unreachable-by-effect: with a budget of 0 the final comparison already returns True. The
load-bearing line is the `is None` test. I annotated the branch as intent-stating and pointed
the mutation at the line that carries the behaviour.

---

## 6. MONEY AND SAFETY

- **Vendor calls made by this round: ZERO**, by the run's own counter. Nothing here constructs
  a vendor client — the cap driver, the gate spy, the config spy and the live-view timer are
  all offline. Prompt cap was $1.00.
- **The shared ledger is not used as evidence.** It has a round id on zero rows and has moved
  during a round that made no calls.
- **No judging rule added or loosened.** The one gate I touched keeps a byte-identical decision
  under a 210-cell equivalence test.
- **Campaigns SHA, re-verified at publication, BOTH forms:** default separators
  `8e02f8d6f6307ae8` **MATCH**, compact `7a029ee5447cddd8` **MATCH**.
- **Seen-store delta at publication** (not at check time), against this round's own verified
  backup: clip **+0**, tiktok pages **+0**, repost **+0**, spotify playlists **+0 entries**,
  meme pages **+67 entries**. **This round wrote no seen store.** The +67 is another round's
  live Instagram walk; a peer round disclosed in-session that it had deleted 56 keys from that
  file at 18:24 and then put them back.
- **No key, address or handle printed, logged or committed.** Every measurement over the master
  lead store returns counts only.
- **Every teardown named a pid I captured myself and whose parentage I verified.** The port
  table showed the listener was one pid while my own process handle was another — the
  two-process shape the brief warns about — so I confirmed the parent before killing.

---

## 7. WHAT HE SHOULD DO NEXT

1. **Decide the two fail-open spend policies.** An unreadable ledger and a malformed cap both
   mean "the lifetime ceiling is not being applied". Both now say so out loud and are counted;
   neither refuses. I think both should refuse. Your call, not a refactor's.
2. **Decide whether the views gate should require n >= 2.** Today 96.52% of rows carrying that
   field are one video. Requiring a real mean cuts almost all of them.
3. **Ask BL-1484 and BL-1486 for their reds.** Four of the 16 are seen-set failures in a file
   being edited right now.
4. **The facts guard is now armed in the pre-commit hook** and drift is currently **+16.17%**
   and **+19.76%** on the two lifetime totals — both invisible under a 25% band. Consider 10.0,
   as a separate decision from arming it.
5. **Three of the five stage counters remain unmeasured.** Wiring them is one call inside each
   funnel, and those files are held.

---

## 8. PATHS

Repo-relative. Use the `.bat`, never a port — the port is not stable.

```
clippershq/spend_ledger.py     lifetime_cap_declared, CAP_ANOMALIES, would_exceed
clippershq/finder_common.py    effective_run_cap
clippershq/clip_pipeline.py    resolve_budget
clippershq/main.py             over_budget, the per-run cap call site, the views-gate caller
clippershq/tiktok_finder.py    the language-gate exception, its counter, language_unjudged
clippershq/filters_free.py     avg_views_ok(..., n_posts=) -- REQUIRED
clippershq/run_status.py       update() warns on a dropped key; set_stage_counts
clippershq/run.py              the five counters on the heartbeat
tests/run_all.py               skip counting; the never-binds check
tests/test_bl1487_zero_cap.py
tests/test_bl1487_language_gate_loud.py
tests/test_bl1487_views_statistic.py
tests/test_bl1443_lifetime_cap.py   made able to test what it exists to test
dashboard/server.py            the effective-value block on the settings endpoint
dashboard/static/app.js        hidden-tab guard; the EFFECTIVE column
SHEETS.bat                     both exit codes now read
```

Reproduce the measurements:

```
python scratch/bl1487_1a_drive.py         the zero cap, driven, 13/13
python scratch/bl1487_mutate.py           8 mutations, 8 caught
python scratch/bl1487_spy_run.py          change the config, watch the screen change
python scratch/bl1487_liveview_cost.py    both arms, median and tail
python scratch/bl1487_publish_check.py    campaigns SHA + seen-store delta
python tests/run_all.py -k bl1487
```

---

## 9. THE 16 REDS AT HEAD, EACH WITH AN OWNER

Three fixed by me. Thirteen named.

| suite | failure | owner |
|---|---|---|
| `test_bl1443_lifetime_cap.py` | env sandbox overrode its ledger — **it was testing nothing under the runner** | **FIXED (BL-1487)** |
| `test_vision_failure_reason.py:191` | malformed cap must degrade | **FIXED (BL-1487, my regression)** |
| (same suite) | unreadable ledger must fail OPEN | **FIXED (BL-1487, my regression)** |
| `test_bl1350_gates.py:331` | seen-set record merge | BL-1486 (editing that file now) |
| `test_meme_finder.py:344` | seen-set record merge | BL-1486 |
| `test_bl1397_channels_cap_and_sheet.py:182` | unjudged reason dropped | BL-1486 |
| `test_bl1400_ordering_and_third_state.py:124` | third-state value missing | BL-1486 |
| `test_bl1359_ig_cost_fixes.py:88` | judge-batch counter absent | BL-1486 |
| `test_bl1307_veto_refused.py` | judge pointed at a refuted brief | BL-1308 |
| `test_bl1308_refuted_brief.py:166` | offenders under the scratch directory | BL-1308 |
| `test_bl1389_no_caller.py` x4 | 39 untriaged orphan modules | BL-1432 |
| `test_bl1444_board_and_sheets.py:310` | an unexpected config key | BL-1452 |
| `test_doc_citations.py` x3 | doc citation drift | BL-1040 |
| `test_estimated_flag.py:123` | a 2026-08-30 ledger row not flagged estimated | BL-1441 |
| `test_send_list_rebuild.py:140` | a row-count mismatch of 6 | BL-1392 |
| `test_silent_zero_shape.py` x2 | mark-reader load path | BL-1389 |
| `test_exports.py` | **NOT REPRODUCIBLE** — green twice standalone and under the runner's env | tree state |

**The first is the finding worth keeping.** That suite was **green standalone and red under the
runner**, and under the runner it was **measuring nothing**: the runner sets a sandbox ledger
env var which the path resolver keeps outermost *on purpose* (a stray test config once put 155
phantom rows in the real ledger), so the suite's own ledger was silently ignored and every
lifetime-room assertion read an empty file. I proved it pre-existing by running **HEAD's own
code** under the same env: HEAD returns 5.0 where the suite asserts 0.0. A check that passes
for the wrong reason and a check that fails for the wrong reason are the same defect wearing
two faces.

---

## 10. THE DOCS

- **The four brains did not exist in the documentation at all** — 0 hits across 53 files,
  tested three ways. A new document now describes them: the selection site, what differs
  (brief text — **not** the exemplar pack, which is still one shared set, and that
  **contradicts the brief**), and what does not (no per-brain threshold; the reject threshold
  is one global).
- **The persona document asserted the opposite** — "one definition, applied identically to
  every platform", backed by a real controlled test. **The test is real and its scope was never
  stated:** it covers the free pre-spend text gate, not the vision judge, and it predates the
  edits rubric by 42 days. Scoped, not deleted; his measurement left intact and attributed.
- **The no-send rule is enforced by no code.** Two hits repo-wide, both false positives. The
  send guard is the *inverse* — it enforces send-*readiness*. **Six** documents still instruct
  sending, not five; three were committed **83 minutes before** the rule, and the primary
  operating document contradicts itself 67 lines apart **in the rule's own commit**. All six
  now carry the banner; the instructions are kept as the record of a decision and made
  conditional.
- **The facts document carried a stale Instagram price.** Corrected. **The config was right and
  was not touched** — the lower figure belongs to the other vendor's key, where it is correct.
- **The smallest anti-staleness mechanism, implemented:** a third check kind that resolves a
  dotted path in the live config and fails on a mismatch — about fifteen lines — **and armed in
  the pre-commit hook**, clearing a no-caller note the module had carried since 2026-08-24.
  Proved on a planted positive control and by mutation.

---

## 11. IS IT PRODUCTION-READY, AND WHAT REMAINS

**No.** What is now true: a declared zero cap refuses at six sites through one chokepoint; a
language gate that cannot run says so and admits nothing silently; a gate that reads a "mean"
is told how many posts it is over; the runner counts skips separately and fails a suite whose
tests never bind; every UI page opens clean in a real browser with a proven console detector;
and the settings screen shows what will actually happen per campaign, proved by a spy.

What remains, in the order it will cost him:

1. **13 red suites** with named owners, four in a file under active edit.
2. **Three of five stage counters unmeasured** — honest about it, but unanswered.
3. **Two fail-open spend policies** awaiting his decision.
4. **A drift guard armed at a threshold that hides the live drift** (+16.17% / +19.76% under a
   25% band).
5. **43 launchers for three doors**, three load-bearing despite looking redundant. Proposed,
   not touched.

And the structural point: **five rounds wrote this repository while I measured it.** One file I
hold moved under me four times; another grew by 84 lines. Everything in this report that I
drove myself is reproducible from the scripts in section 8. Anything I merely observed about
the tree as a whole was true at a moment, not as a property.
