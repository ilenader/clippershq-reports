# BL-1511 — What fails without saying so

**Eleven of the fifteen faults this round seeded or hunted fail without saying so. Four of those are worse than silence: they return a confident, plausible, wrong answer, and a careful operator lands in them *because* they checked.**

Read-only round. No production file, store, config, doc, exemplar pack or test fixture was written. Zero vendor calls; **$0.00 spent** against a $0.25 cap. Five sub-agents, each required to prove a positive control before reporting any zero.

Every `file:line` below is pinned by **sha256**, not mtime — one file on this tree changed mtime tonight with byte-identical content, so mtime answers "was this written", not "did it change".

---

## 0. The answer, and the fourth bucket

The brief asked for three classes: LOUD, SILENT, SILENT-AND-CACHED. A fourth arrived independently **three times** tonight, from three instruments with no contact between them, and it is the one that matters most:

**CONFIDENTLY WRONG** — the system answers, the answer is well-formed and plausible, and it is garbage. It is worse than silence because silence leaves the operator still looking, while a confident answer ends the search. And its victims are selected for diligence: you only reach it by running the check.

Three arrivals:

- A round checked the published claims archive for a round id, got "free", and collided with a live round that had filed in the live registry.
- A seven-file `ImportError` fallback reports a missing package that is not the one missing.
- A garbage-collection tool's own console says "moved (NOT deleted)" honestly, while the dashboard tells the operator it deletes.

A fifth class deserves its own name too: **LOUD-AND-UNREAD**. The free judge's `_STATE` counters for errors, torn JSON and abstentions all increment correctly. The only reader is `free_judge.stats()`, which has **zero callers anywhere in the repo**. A perfect instrument wired to nothing lands exactly where silence lands.

---

## 1. The seeded faults

| # | Fault | Where it is absorbed | Verdict |
|---|---|---|---|
| 1 | HTTP 200 + vendor error + items together | `envelope.py:373-376` (error computed `:350`, never checked when items present); consumed `tiktok_finder.py:208-233` | **SILENT AND CACHED** |
| 2 | Vendor error, item list absent vs genuinely empty | `envelope.py:349-366` | SILENT |
| 3 | `[items, cursor]` two-element payload | `envelope.py:340-343` | SILENT (worse than the brief) |
| 4 | Torn JSON / timeout / blank at token cap | `free_judge.py:1296-1362` | LOUD-AND-UNREAD |
| 5 | Private page / login wall | `page_capture.py:125-188`, `428-442` | LOUD internally, never leaves the file |
| 6 | **Age gate** | `page_capture.py:494-500` | **SILENT AND CACHED** |
| 7 | Run killed mid-batch | `run_status.py:83-128` | FIXED |
| 8 | Console cannot render a character | `control.py` `_emit`; `run.py:873` | SILENT AND CACHED (mitigated during this round, see §4) |
| 9 | Budget set to zero | `tiktok_finder.py:3634`, `meme_finder.py:5899`, `finder_common.py:221` | FIXED — verified by executing the real reserve path |
| 10 | Test entry point launches the funnel | `meme_finder.py:5109` `_drain()` | **SILENT on Instagram, fixed on TikTok** |
| 11 | Config key missing / campaign override | `main.py:5110-5230` | not a live fault |
| 12 | Two writers, one seen store | `filelock.py` `_try_acquire()` | FIXED |
| 13 | Disk fills mid-run | `run_resume.py:266`; no disk check in `meme_finder.py`, `tiktok_finder.py`, `run.py` | **SILENT on four funnels** |
| 14 | Unbound name swallowed by `except Exception` | `paste_batch.py:1079` | SILENT, sticky for the process |
| 15 | Claim archive queried as if it were the live registry | archive vs live claims directory | **CONFIDENTLY WRONG** |

**Fault 1 is the compounding one and it is proven, not argued.** A three-item truncated payload was fed to the real `judge_author()` and returned a confident `NOT_TARGET`, indistinguishable from a genuine observation, which `PageSeen.is_decided()` then latches permanently. It caches whenever truncation lands at or above `MIN_VIDEOS_FLOOR = 3`. The funnel then skips the very evidence that would correct it.

**Fault 6 is the fifth state nothing handles.** All four age-gate phrasings fall through to `no_grid_reason="unknown"`, the shot is **not** suppressed, and the interstitial is photographed and handed to the judge as an ordinary grid.

**Fault 10 is the highest-value unfixed item.** `run_provenance()` has exactly one caller in the tree, in `tiktok_finder.py`. `meme_finder` stamps none, and `_drain()` swallows per-page exceptions into a dict field the run watcher never reads. So on Instagram, *"judged 0 legitimately"* and *"judged 0 because everything errored"* are indistinguishable — the exact failure the brief describes, fixed on one platform and live on the other, on the platform with the highest cost per delivered page.

**Two faults could not be measured** and are declared, not asserted: cloud-sync free-space swings during a real multi-hour run, and a full end-to-end run launched from a test entry point. Both were traced statically instead.

---

## 2. The shapes

Denominator: **205 `.py` files** across the two production trees. AST, not text. A positive control planted and caught for every sweep.

| Shape | Raw hits | Confirmed live |
|---|---|---|
| Three-state collapsed to boolean | 11 | **0** |
| Check returns OK when it skips | 46 scanned | **0** |
| `except:` → permissive in a gate | **419 strict / 968 loose** on 1,471 | **0** |
| Lock returns True when both imports fail | — | 0 — raises a timeout instead |
| One field carrying several statistics | — | 0 — now requires its denominator |
| `complete: true` with `videos: 0` | — | 0 — gated on "bought nothing" |
| Funnel latched at running | 79 of 225 records | 0 mis-surfaced |
| **GC moves bytes sideways** | — | **1 — LIVE** |

**419 raw became 0 confirmed on triage.** The single most on-point hit — the live language gate the brief names as its worked example — is a **false positive**: it raises through a called helper, which no lexical AST detector can see through. These sweeps measure a *lexical shape*, not a live defect. Anyone publishing the raw number is publishing the shape.

**The one live shape:** the scratch garbage collector moves quarantined directories to a sibling directory **on the same volume, inside the same cloud-synced tree**. `shutil.move` there is a rename: zero bytes freed, nothing leaves the sync scope, against the tool's own stated purpose. It has **no purge path at all**, unlike its sibling tool. The tool is honest on screen; the dashboard describes it to the operator as deleting.

---

## 3. The tests

| | |
|---|---|
| Test files | **444** |
| Test methods resolved to real `TestCase` classes | **8,256** |
| Module-level `test_*` functions in script-style files | 280 across 10 files — **all wired** |
| Never-run (defined after a `__main__` guard) | **0** |
| Never-bound (shadowed, or outside a collected class) | **0** |
| Mutations | **8 guards, 8 KILLED, 0 SURVIVED** |

**The skip-count claim is false for the current code.** A synthetic two-pass/two-skip suite was put through the real runner end to end: skips are excluded from the check count and printed separately.

**A direct-base check first flagged 99 live suites as uncollected.** All 99 were false — they inherit through local harness chains. A denominator that fails its own control produces a confident large number about a scope it never covered.

**⚠️ The grep-word defect reproduces, and is proven by mutation.** Two suites do a whole-file substring search for the word `continue`. Deleting the real `continue` at `meme_finder.py:6186` left one of them **SURVIVED**, printing *"Ran 9 tests ... OK"* — because four lines above, the target's own explaining comment reads *"report, count, continue."* and the assertion matched the prose. Restored and sha256-verified. **A test that survives its own subject's deletion is not a test.**

**The red set, derived independently rather than inherited.** Full run, 444 of 444, 2,512.6 s, six other rounds live: **19 red + 2 timeouts**. Every one re-run individually on a clean restored tree:

- **14 genuinely red** in isolation.
- **5 not reproducible alone** — false reds from concurrency.
- **2 timeouts**, declared as timeouts rather than failures, and not independently re-verified.

**One of the five false reds was contaminated by this round's own mutation testing** — the audit's instrument corrupting the audit's evidence, caught only by re-running on a restored tree. Neither 19 nor 14 is "the" red count: 19 is what a full run shows under load, 14 is what survives isolation, and the gap is a direct measurement of the hazard.

One mutation caveat kept rather than smoothed: one lock guard's proof is **timing-flaky** — it passed once through startup luck with the mutation live, and failed only on an isolated re-run. Its sibling lock suites force the race deterministically and are the model fix.

---

## 4. The clone rehearsal — the brief is stale here

**The fresh clone commits.** Cloned to a temp directory, hooks installed, no virtualenv, no config, no ledger present. A trivial commit **succeeded**. The facts guard printed *"28 of 35 fact(s) agree — 7 COULD NOT BE CHECKED AT ALL"*, labelling each `UNCHECKED` and "normal in a fresh clone."

That is the **opposite** of the defect this round hunts: a check that says *"could not look"* instead of returning OK. It was fixed two days before this round began.

A different fresh-clone failure does exist: the commit-message ownership guard refuses a staged file whose name matches a round pattern when no live claim exists — reproduced both ways.

**The encoding fault was live at the start of this round and was mitigated during it.** A stream-level hardening landed mid-round, verified by hash. It edits no literal and no emit site, so the census population is unchanged. Its author's stated limit is kept here: it makes the crash **message survive**; it does not make the literals portable, and an escaped character is degraded output, not correct output. The residual gap is that only three modules import the console module at module level, so anything emitting before that import is still bare.

---

## 5. The encoding class — the question was badly posed

Four instruments counted "unprintable emit sites" and produced 6, 13, 29, 158 and 358. **None was wrong.** The count is a property of the **launch context**, not of the source:

| launch context | sites that raise |
|---|---|
| forced UTF-8 (the test runner does this) | **0** |
| redirected / piped — the dashboard path | 6 – 29, by rule |
| interactive console | 153 – 358, by rule |

**Nothing in the codebase pins the launch context.** The test runner exports UTF-8 for every suite child; the money path is spawned with no encoding flag and no environment. **Tests protected, money path bare** — the suite structurally cannot see this class.

Two corrections that cost three rounds an hour between them, kept in print:

- **A codec name is family-level and diagnoses nothing.** The same codec name is emitted by four different codepages. The **module path in the traceback** is the diagnostic that works.
- **The two codepages are not nested.** One character is fatal in one and safe in the other, and vice versa. Reporting either column alone misses sites in the other direction.

**And the class that actually kills the error reporter is invisible to all four censuses.** The site that destroys a run's cause carries a **pure-ASCII literal** and raises on the *interpolated exception message*. Every census counted literals; none counted what is interpolated into them. Sized independently: **33 of 323 raise sites** are fatal on the console path, led by the ledger and the clip pipeline — **the money path**. An exception raised in the ledger kills the thing trying to report it.

---

## 6. Ranked by what it costs him

1. **The Instagram provenance gap.** "Judged nothing" and "everything errored" are indistinguishable on the platform that costs the most per delivered page. Fixed on the other platform; the fix is twenty lines away.
2. **The truncated-envelope cache.** A partial vendor page becomes a permanent, confident rejection of an account that was never really seen.
3. **The interpolated-exception class on the money path.** A ledger exception destroys the message naming it, and the persisted failure cause becomes an encoding error.
4. **The age gate.** A fifth state nothing handles, photographed and judged as an ordinary page.
5. **The grep-word tests.** Two guards a comment can satisfy — one proven to survive deletion of its subject.
6. **Disk-full silence on four funnels.** The resume ledger goes quietly incomplete.
7. **The claim archive queried as a live registry.** Two rounds on one id; caught only because three rounds happened to be comparing notes.
8. **The GC that frees nothing** while the dashboard reports deletion.
9. **The unbound name** returning a plausible empty map, sticky for the process.
10. **The seven-copy import fallback** naming the wrong missing package.

---

## 7. What I got wrong

Five instrument failures of my own, all caught — four by a positive control or a peer, one by me:

1. **A truncated grep produced a false zero.** I searched for the environment flags that pin the launch context, got nothing, and was one message from publishing "nothing pins it". A positive control on a file I knew contained the string caught it: the test runner sets both, and my pipe had cut the list before reaching that directory.
2. **I propagated an unchecked inference as though I had verified it** — that a codec name identified a specific codepage — and used it to tell a peer their predicate was right "on the correct grounds rather than by luck".
3. **I treated the two codepages as nested** when neither contains the other.
4. **I misread a line number by one and reported it as file drift**, from counting a window instead of printing line numbers. The file had not moved; same hash.
5. **I proposed pinning citations by mtime.** A peer produced a file whose mtime moved with identical content. It is sha, or sha and mtime, never mtime alone.

Every one is the round's own subject: **an instrument answering confidently about a scope it never covered.**

---

## 8. The brief itself

Several of the brief's own figures did not reproduce, from more than one instrument independently:

- Its emit-site figure is not reproducible under any tested definition, and the underlying claim is **not well-posed** — it depends on the launch codepage, which is not a property of the source.
- Its silent-handler pair has **no stated rule and no reproducible denominator**; three instruments produced three different answers.
- Its worked example of a live permissive gate is a **repaired guard**.
- Its skip-count claim, its never-bind claim and its mutation-survival claim **do not reproduce** on the current tree.
- Its list of offending characters names one that is **safe** in the codepage it is cited for.

Stated as a finding, not a grievance: **a commissioning document carrying numbers with no predicate beside them is the same defect class it commissions an audit of.** The fix is the one this report recommends everywhere else — state the rule beside the number, and the denominator beside the count.

**Recommendations, all specified and none shipped:** a note in the claims archive naming it as an archive; the launch context pinned where funnels are spawned; a provenance stamp on the second funnel; the interpolated-exception class addressed on the money path; a purge path for the collector, or a truthful description of it in the dashboard.

---

*Read-only. Nothing shipped. $0.00 spent. Every zero in this report has a passing positive control, and every zero whose control failed was discarded rather than published.*
