# INFRA-032 — clip_seen.json needed a **merge as well as a lock**, and a lock alone measured **worse than no lock at all**: 36 of 39 ids lost against 30. **551 library clips are already missing from the cache.**

**Date:** 2026-08-03 · **Type:** concurrency fix · **Spend:** **$0.00**, no paid call
**Wrote:** `clippershq/clip_runner.py`, `tests/test_clip_seen_lock.py` (`5161c9a`),
`scratch/infra032_*`. **Read but never wrote:** `repost_finder.py`, `caption_finder.py`,
`song_library.py`, `main.py`, `decision_log.py`, `tools/claim.py`.

---

## Taking INFRA-030's finding, and then finding where it stops

INFRA-030's result is used exactly as proven and not re-derived: **the write was already
atomic and records vanished anyway.** `os.replace` makes one write indivisible; it cannot
make a *pair* of them ordered.

But copying its fix across would have shipped something that still lost every walk, and that
is the whole of this round.

### The window here is an entire walk, not microseconds

```
clip_runner.run_clip_finder
    :608   seen = load_seen(seen_path)      <- read, at the START
    :700   seen.add(cid)                    <- mutated, for minutes or hours
    :775   save_seen(seen_path, seen)       <- written, at the END
```

`runs.json` held its stale snapshot for the microseconds between a read and a replace. This
holds one for as long as a walk takes.

### And `save_seen` had no merge at all

| | merges? | locked? | what was needed |
|---|---|---|---|
| `runs.json` (INFRA-030) | **yes** — drop my run_id, insert mine, keep the rest | no | the lock was the whole fix |
| `clip_seen.json` | **no** — it dumped the caller's set over the file | no | lock **and** merge |

Serialising writes that do not merge just makes the loss orderly. **Measured, 13 concurrent
processes, 39 ids in flight:**

| variant | ids surviving | lost |
|---|---:|---:|
| old — no lock, no merge | 9 of 39 | **30** |
| **lock only — INFRA-030's fix copied across** | **3 of 39** | **36** |
| lock + re-read inside it + union | **39 of 39** | **0** |

**The plausible fix is worse than the bug.** Serialising makes the last stale writer win
*deterministically*, where unlocked interleaving at least occasionally let a later read pick
up an earlier write. A round that copied the lock across, ran a lock-shaped test, and saw it
go green would have shipped a regression and recorded it as a fix.

### Union is the correct merge, and why that is written down

The seen-set is **monotonic**: an id is added when a clip is processed and never removed —
verified, there is no `discard`, `remove`, `clear` or prune of it anywhere. That is asserted
in the test as a **property of the tree**, not of the function, so if a future round teaches
the walk to forget an id the assertion fails *before* union silently resurrects it.

---

## The proof, with two controls that must keep failing

`tests/test_clip_seen_lock.py`, 9 tests. Both controls keep a verbatim copy of code that must
stay broken:

```
[CONTROL] the old code loses a whole walk                          -> lost {a1,a2,a3}
[CONTROL] a lock ALONE still loses a whole walk                    -> lost {a1,a2,a3}
          lock + re-read + union loses nothing                     -> lost nothing
```

And the deterministic version, with no timing at all — two walks, each reading at its start,
A writing then B writing:

```
old        LOST 3   ['a1','a2','a3']
lock_only  LOST 3   ['a1','a2','a3']
fixed      LOST 0
```

**Item 3's warning was taken literally.** INFRA-030's first "fixed" scenario passed against
the broken version because `write()` re-read on every call, so no stale snapshot ever existed.
Here the harness was run against the *old* code first and required to lose ids before it was
trusted to prove anything — and then against the lock-only variant, which is the specific way
this could have been got wrong.

---

## The damage already done: **551 clips**

A lost seen-id leaves no trace — the file simply does not contain it, and nothing logs what a
walk added. So it cannot be counted after the fact. It can be **bounded**, because the cache
and the library have a hard relationship:

> `clip_seen` is a **superset** of the library by construction. The cache records every clip
> **walked**; the library only those **kept**. `clip_runner`'s own docstring: *"the seen-cache
> also covers clips that were walked and REJECTED, which the index by definition cannot."*

So `seen < library` is impossible unless entries were lost. On disk right now:

```
clip_seen.json entries : 2,178
clip library clips     : 2,728
library clips NOT in the seen-cache : 551
```

**551 clips were walked, kept, and then forgotten by the cache.** Each is a page the walk will
re-open and re-pay for. Worst affected: `loste1980` 118, `movies.avengers` 69, then a long
tail of ~10 each.

At $0.0006/call and 1–2 calls per re-walk that is **$0.33–$0.66** — and the dollars are not
the cost that matters:

> A walk halts on a dollar **cap**. Every re-opened page consumes cap that a never-walked page
> would have used. **BL-979 measured exactly that failure from a different cause**: the cap
> was spent re-opening catalogues already in the library, 67 paid-for pages were never reached
> at all, and it cost 658 clips — a third of the library at the time.

**This is a bound on what is still missing today, not on what was ever lost.** A re-walk
re-adds the id, so the damage self-heals at the price of the re-walk; entries lost and later
re-walked are invisible to this count.

---

## Re-audit by traced path, not by mention

INFRA-030's AST scan reported 5 unlocked and **3 were false positives**, because it asked
whether a *module* mentions a lock when the property is whether a *file's* read-modify-write
is serialised. Each row below is traced by hand through the actual read → modify → write.

| file | shared RMW? | serialised | merges | verdict |
|---|---|---|---|---|
| `clip_seen.json` | yes | **yes** | **yes** | **FIXED THIS ROUND** |
| `dashboard/static/runs.json` | yes | yes | yes | fixed by INFRA-030 |
| `spend.json` | yes | yes | yes | **locked** — via `main.py:530`, not `spend_ledger.py` |
| `.claims/<ROUND>.json` | **no** | — | — | **no shared RMW; a lock is not the right tool** |
| `config.json` | yes | yes (CAS) | no | **compare-and-swap** — refuses a stale write (INFRA-012) |
| `clip_library/*.jsonl` | yes | yes | yes | locked + merging — the pattern this round copied |
| `output/master_leads.csv` | yes | yes | yes | locked + merging |
| **`repost_seen.json`** | yes | **NO** | **NO** | **UNFIXED — same class, window is an entire run** |
| **caption-finder seen cache** | yes | **NO** | **NO** | **UNFIXED — same class, TWO call sites** |
| `scratch/songs.json` | yes | NO | NO | unfixed, lowest exposure (operator hand-edits it) |

The four-question form matters: *is there a shared RMW → is it serialised → does it merge →
how wide is the window*. Question 3 is the one INFRA-030 never had to ask, and it is the one
that separates copying a lock from reading the code. Question 4 is why `config.json`'s
compare-and-swap is a legitimate answer and a lock is not the only one — refusing a stale
write works when a human can retry, which a walk cannot.

**Two more files have the identical shape and are unfixed**, both with whole-run windows:
`repost_finder.save_seen()` (:457, called at :1793) and `caption_finder.save_seen()` (:312,
called at **two** sites, so a single run can also overwrite its own earlier save). Both are
dicts rather than sets, so the merge is a dict-update rather than a union; otherwise the fix
is the one just written. **Not taken here — this brief is `clip_seen.json`.**

---

## Verification

| check | result |
|---|---|
| 13 concurrent processes, old | 9 of 39 ids survived — the harness detects the bug |
| 13 concurrent processes, **lock only** | **3 of 39** — worse than no lock |
| 13 concurrent processes, fixed | **39 of 39, 0 lost** |
| deterministic, no timing | old lost 3, lock-only lost 3, fixed lost 0 |
| tests | **9 of 9**, two of them controls that must keep failing |
| monotonicity of the set | asserted against the source, not assumed |
| never-raise contract | planted lock failure → walk continues |
| lock path | `clip_seen.json.lock` yes, `.lock.lock` no (BL-817) |
| damage | **551 library clips missing from the cache**; $0.33–$0.66 to re-walk |
| re-audit | 10 files traced; **2 unfixed same-class**, 3 of INFRA-030's flags resolved as false |
| campaigns | **unchanged** — hashes `7a029ee5447cddd8` (compact) and `8e02f8d6f6307ae8` (default) both reproduce, confirming the brief's note that they are one object |
| config | parses, 161 keys, `spend_cap_usd` 50.0 |
| suite | **182 of 188 green** (1876s, 14 rounds in flight at 12:24) |
| the six red | **none are mine** — none mention `clip_runner` or `clip_seen`; see below |
| paid calls | **none** |

### The six reds, attributed

| suite | standalone | owner |
|---|---|---|
| `test_filelock` | **OK** | transient — and the one I checked first, since this round now uses `file_lock` |
| `test_two_leg_budget` | **OK** | transient |
| `test_commit_guard` | FAILS | `tools/commit_guard.py`, `tools/claim.py` — **BL-1036** |
| `test_silent_zero_fixes` | FAILS on `commit_guard_STILL_REFUSES_a_foreign_path` | same — **BL-1036** |
| `test_doc_citations` | FAILS | `docs/CORRECTIONS.md` — **BL-1036** |
| `test_tools_tracked` | FAILS on `tar -xf … exit status 1` | environment/tooling, unowned |

**Checked against my own change first, not last.** `test_filelock` is the suite this round
could most plausibly have broken — it is green standalone. And none of the six failures
mention `clip_runner` or `clip_seen` anywhere in their output (grepped, 0 hits each).

## Limits

- **551 is a floor on what is still missing, not a count of what was lost.** A re-walk re-adds
  the id, so anything lost and later re-walked is invisible here. The true historical loss is
  unmeasurable — the bug leaves no trace, which is why it survived two rounds.
- **The 13-process figures are one machine, one run each.** "3 of 39" is not a rate; it is a
  demonstration that the lock-only variant loses *by construction*, which the deterministic
  test confirms without any timing at all.
- **I did not fix `repost_seen.json` or the caption-finder cache**, though both are the same
  bug and the fix is now written twice. That is scope, not oversight: this brief named one
  file. Both are recorded above with line numbers and their differing merge (dict-update, not
  union).
- **`clip_seen.json` itself was not repaired.** The 551 missing ids are left to heal by
  re-walking. Back-filling them from the library would be a one-line union and is deliberately
  not done: the library is a *subset* of what should be in the cache, so writing it in would
  assert that every walked-and-rejected clip was also seen, which is false.
- **No walk was run.** The fix is proven on synthetic sets through the real `save_seen`, not
  by observing a live concurrent walk — that would cost paid calls, which this brief forbids.
