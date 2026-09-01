# BL-1468 — the judge was dead for five days, and a WARN is not a gate

## IS THE FUNNEL SAFE TO RUN?

**YES for Instagram in `memes` mode — which is what the config is set to.** The model that held the
authority to throw pages away had been returning HTTP 404 since 26 August. It is out, its
replacement was scored on the operator's own marks *before* being given that authority, the
preflight now FAILS a run instead of printing a warning, and the file lock no longer returns a
`True` it does not hold. Eight deliberate sabotages of those fixes were all caught by the tests.

**QUALIFIED YES for TikTok in `memes` mode.** Nothing dead or lying remains in its path and the
same gate protects it — but the accuracy evidence behind it is **4 graded pages**, and TikTok
builds a *different* judge payload from Instagram. Run it; do not quote a kill rate for it.

**NO for `edits` mode on either platform.** It spends real money to fetch supply that is wrong on
arrival. Details in section 4.

---

## 1. ROUND ID, DATE, AND THE ASK

**BL-1468**, worked 2026-08-31 into 2026-09-01. A follow-on fix, **BL-1477**, is included because it
came out of the same work.

The instruction was: nothing runs until the judge is proven alive. The free vision-judge chain was
running on a model, `stealth/ox-alpha`, that had 404'd since 26 August while still holding *reject
authority* — the right to discard a candidate page. I was asked to (1) find and live-verify every
usable replacement and score it on the operator's marks before giving any of them that authority,
(2) fix the three checks that failed to catch a five-day outage, (3) work through a list of
suspected-dead code with a runtime spy and a call count for each, (4) report a dead Twitch branch
without acting on it and sweep Instagram and TikTok for the same shape, and (5) say plainly, at the
end, whether the funnel is safe to run. I was also asked to tell the operator the truth about his
95% accuracy target.

---

## 2. WHAT SHIPPED, AND HOW EACH WAS PROVED

Proof here means a **runtime spy** — monkeypatch the callee, drive the real shipped function, count
the calls — or a live network call. A passing test is not listed as proof on its own; three of my
own tests passed against deliberately broken code before I rewrote them (section 5).

| # | change | file:line | how it was proved |
|---|---|---|---|
| 1 | `stealth/ox-alpha` removed from `MAY_REJECT` and `FALLBACK_CHAIN` | `clippershq/free_judge.py:239-242`, `:268-270` | **Live calls: 198 of 198 returned HTTP 404.** Its own response body states the Stealth programme ended |
| 2 | `z-ai/glm-5.3-flash` given authority at bar 90, in a new `SCORED_PAID` tuple | `clippershq/free_judge.py:240`, `:255` | **1,341 live scored calls** (section 3). Kept OUT of `FALLBACK_CHAIN` because that tuple's contract is that every id is free and this one bills |
| 3 | Chain reordered so the slowest link is last | `clippershq/free_judge.py:268-270` | **390 live calls** measured against the shipped 45 s timeout (section 3) |
| 4 | `askable_models()` — one definition of "what can be asked" | `clippershq/free_judge.py:298` | Replaced **four** hand-kept copies that had silently disagreed (section 5) |
| 5 | `model_why` hoisted out of the reject branch | `clippershq/free_judge.py:1442-1444` | **Runtime**: stub the ask call to return a WANT, drive real `should_reject`, assert the model's sentence survives on a verdict that never reaches the reject branch |
| 6 | New `SKIPPED` preflight status | `clippershq/preflight.py:277` | Runtime: the model-liveness check with the network off returns `SKIPPED` and the text `NOT CHECKED`, where it previously returned the same `OK` token a real pass returns |
| 7 | `check_gate_armed` reads live reachability, not `len()` of a dict | `clippershq/preflight.py:114`, map at `:83` | Runtime: with the map empty it will not return `OK`; with an empty name list it returns `FAIL`; only a live answer yields `OK` |
| 8 | Preflight given a production caller that **refuses** | `clippershq/run.py:429-445` | **Runtime**: force the preflight to return failure, call the real headless entry point, assert return code **2** and that the funnel never starts |
| 9 | File lock raises instead of returning a lock it does not hold | `clippershq/filelock.py:107` | **Runtime spy, 4 threads counting simultaneous holders.** Positive control: real lock max holders = **1**. With both primitives stubbed out it refuses |
| 10 | Unguarded delete replaced with the retrying wrapper (BL-1477) | `clippershq/video_strip.py:197` | **Runtime spy on the wrapper**, driving the real frame-extract function against a directory holding a stale frame and a cover: **1 call, on the stale frame, cover untouched, control fired** |
| 11 | 8 synthetic handles removed from the Instagram seen-store | `meme_pages_seen.json` | Set-diffed against a pre-round backup: **−8, +0**, each removal named |

**Tests:** one new suite of 15 tests, plus four existing suites corrected. All pass.

**Preflight, run live at publication:**

```
PREFLIGHT  9 check(s): 8 OK, 1 WARN, 0 FAIL, 0 NOT CHECKED
  models_live         OK    every model in the chain answered
  gate_armed          OK    armed and REACHABLE: 2 models answered and may reject
  thresholds          OK    both scored models at bar 90
  cap_price           OK    config and client agree on the per-call price
  capture_bounded     OK    same order as the walk, headroom 15x
  grid_dir            WARN  an existing manifest will be REWRITTEN WHOLE
  subprocess_timeouts OK    every subprocess call carries a timeout
  config_keys         OK    11 tag(s), supply configured
  vendor_live         OK    answered in 1.78s
```

**Does it gate every funnel?** The dashboard launches runs by spawning the run module as a
subprocess, and the command-line path enters the same function, so both hit the gate. One other
spawn — the harvest runner — is **not** gated and does not need to be: it never touches the model
chain. Stated so it is on the record rather than assumed.

---

## 3. WHAT WAS MEASURED

Every rate carries a Wilson 95% interval and names its denominator. **MEASURED** = observed this
round. **DERIVED** = computed from those observations.

### 3.1 The judge's kill rate on pages the operator WANTS

The number that matters: how often does the gate discard a page he marked as wanted? Denominator =
**76 wanted pages from this round's graded set that each model returned a verdict on.**

| model | wanted pages | killed | rate | keeps at least | |
|---|---|---|---|---|---|
| `z-ai/glm-5.3-flash` @ 90 | 76 | **1** | **1.3% [0.2, 7.1]** | **92.9%** | MEASURED |
| `nex-agi/nex-n2-mini` @ 90 | 76 | 3 | 3.9% [1.4, 11.0] | 89.0% | MEASURED |

glm was promoted on this: one third the kills of the incumbent on the same 76 pages.

### 3.2 The noise floor — a model asked the SAME page TWICE

Denominator = pages where that model was asked the identical question twice.

| model | repeated pages | agrees with itself | |
|---|---|---|---|
| `glm-5.3-flash` | 192 | **96.9% [93.4, 98.6]** | MEASURED |
| `nex-n2-mini` | 96 | 84.4% [75.8, 90.3] | MEASURED |
| `nemotron-3-nano` | 41 | **39.0% [25.7, 54.3]** | MEASURED |
| all pooled | 329 | 86.0% [81.9, 89.4] | MEASURED |

### 3.3 Parallel judging — measured against that floor, and the answer is DON'T

Denominator = pages both models in the pair answered.

| pair | pages | they agree | |
|---|---|---|---|
| `nex-n2-mini` vs `glm-5.3-flash` | 197 | **85.8% [80.2, 90.0]** | MEASURED |
| `nex-n2-mini` vs `nemotron` | 97 | 53.6% [43.7, 63.2] | MEASURED |
| `nemotron` vs `glm` | 107 | 44.9% [35.8, 54.3] | MEASURED |
| all three unanimous | 97 | 42.3% [32.9, 52.2] | MEASURED |

**Two different models agree with each other (85.8%) about as often as `nex-n2-mini` agrees with
itself (84.4%).** Their disagreement is explained by one model's own instability, so a second model
supplies no independent opinion — it costs double for what re-asking the first would give. DERIVED
conclusion: **do not parallel-judge.**

And on the 43 wanted pages all three models answered, no voting scheme separates:

| scheme | wanted | killed | |
|---|---|---|---|
| kill only if all authority agrees | 43 | 0 = 0.0% [0.0, 8.2] | MEASURED |
| kill if any one does (today's shape) | 43 | 1 = 2.3% [0.4, 12.1] | MEASURED |

### 3.4 LIVE IS NOT THE SAME AS USABLE

Denominator = **every call made to that model**, answered or not. "Usable" = a parsed verdict
returned inside the shipped 45-second timeout.

| model | calls | usable inside 45 s | median answered | median silent | slowest | |
|---|---|---|---|---|---|---|
| `nex-n2-mini` | 325 | **91.4% [87.8, 94.0]** | 5.5 s | 18.9 s | 24.9 s | MEASURED |
| `glm-5.3-flash` | 428 | **88.1% [84.7, 90.8]** | 19.7 s | 55.7 s | 399.8 s | MEASURED |
| `nemotron-3-nano` | 390 | **16.4% [13.1, 20.4]** | **68.8 s** | **300.6 s** | 756.9 s | MEASURED |

`nemotron` passes every liveness probe and its median *answered* call is **above the timeout**, so
most of its answers arrive after the caller has gone. It was sitting **second** in the chain,
costing roughly 45 wasted seconds on every page that fell past the first link. Moved last.

**It also answers about pages it never received.** On verdicts it did return, its stated reason was
that no page was provided:

| model | verdicts returned | said it had no page | |
|---|---|---|---|
| `nemotron-3-nano` | 161 | **15 = 9.3% [5.7, 14.8]** | MEASURED |
| `nex-n2-mini` | 297 | 0 = 0.0% [0.0, 1.3] | CONTROL |
| `glm-5.3-flash` | 402 | 0 = 0.0% [0.0, 0.9] | CONTROL |

The two zeros are the positive control that the detector is not simply over-firing on everything.

### 3.5 The 95% target

The operator asked for 95% agreement with his marks. **His own marks agree with themselves 75.8%
[68.4, 82.0]** (MEASURED in an earlier round, quoted here because it sets the ceiling). A model
cannot be 95% right about a target that is 76% stable, so that number is not available to anyone.

The 95% that *is* available is a floor on kills of wanted pages. Sample size needed for the Wilson
upper bound on the kill rate to reach 5% — DERIVED:

| kills observed | wanted pages needed |
|---|---|
| 0 | 73 |
| 1 (where we are) | 110 |
| 2 | 142 |
| 3 | 173 |

**At n=76 with zero kills the floor would already be 95.2%.** Part of the remaining distance is not
sample size at all — it is the one page the model killed.

### 3.6 How many marks actually exist

Denominator = the operator's **in-sheet** mark files only. These are the marks made inside a
delivered grading sheet, and they are population-matched by construction — nothing writes to them
but him.

| | | |
|---|---|---|
| sheets | 12 files, 683 rows, **537 pages** | MEASURED |
| marked wanted (want flag) | **241** | MEASURED |
| scored 9–10 (stricter criterion) | **127** | MEASURED |
| of the wanted, image already on disk | **237** | MEASURED, upper estimate — see below |
| the judge has actually been scored against | **78** | MEASURED |

⚠️ The want flag (241) and a score of 9-or-better (127) are **different criteria and must never be
averaged.** The 237 comes from matching mark handles against image filename stems, so it is an
**upper estimate** pending a proper resolver pass.

### 3.7 Mutation testing — the guards are not vacuous

Each fix was deliberately broken to check the tests scream. **First run caught 5 of 8. After
rewriting three vacuous assertions (section 5): 8 of 8**, with the unmutated tree passing and every
source file restored afterwards.

### 3.8 NOT MEASURED

- **Disk before/after.** This round did not delete or write bulk data; no disk measurement was taken.
- The unconditional production frequency of the vendor-error drop in section 4 — it needs a live
  paid walk, which was not run.
- Anything about TikTok accuracy beyond 4 graded pages.

---

## 4. WHAT WAS REFUSED, DEFERRED, OR DELIBERATELY NOT DONE

### 4.1 The dead-code list — findings, with the runtime evidence

| item | verdict | evidence |
|---|---|---|
| vendor-error envelope drop | **DEAD caller, LIVE drop** | Bytecode import sweep: exactly **one** importer, and it calls a different function. Driven over **195 captured vendor payloads**: state and reason discarded **194/194**. Stapling an error onto the 93 payloads that read OK: **93/93** still report success |
| four backspace bytes in an injected script | **branch DEAD** | 2 regexes × 5 real page texts = **10 trials, 0 matches**; with the escape corrected, **7**. Control: a string that really contains the byte matches **[True, True]** |
| a band label written 7 times | **DEAD** | **46,899 real records** across 48 checkpoints. Reads by production consumers: **0**. Controls on the same data: a known-read key **42,396** reads, a planted reader **14,132** |
| "a normaliser returns None 100% of the time" | **REFUTED** | Driven over **130,740 real records**: 99.937% None, but 44 and 39 real values. Not 100%, and not a code bug — the writers never stamp the field |
| a drift guard at 25% | **guard works, has NO caller** | The 25% is a growth limit against a stamped snapshot, applying to **5 of 35** facts. Spy: called **5×**. Control: halve a value → **1 problem** reported. Importers outside tests: **0** |
| a pages-per-minute metric | **correct but MISLABELLED** | Exact on **35 of 35** real runs. But it reads 1,662/min, 6,854/min, or **929,199/min** depending on how much work actually happened — a wall-clock page rate, not a judging rate |
| two profile fields read by the wrong name | **DEAD reads** | Driven on a real captured vendor payload: the source writes one key name and a video count of **360**; the funnel reads two different key names and gets nothing, so **the judge was told the page has 5 videos** and shown no display name. Control restores both |

**The backspace-bytes fix was refused on measured grounds.** Correcting it moves pages from
"screenshot the login wall for free" into "buy a billed grid", so it **increases** spend; and
emulating the whole expression on real page text showed the fix changes **nothing**, because two
other limbs already catch the case. Recommendation: leave it, or only behind a measured A/B.

**Two patches were written but NOT applied** — the files belong to other in-flight work. They are
handed over in full: the profile-field fix, and carrying the vendor error instead of dropping it.

### 4.2 Twitch — reported, not touched

Instructed to report and not act. Two dead paths were found; **nothing was fixed, deleted, or wired
up.** One config toggle selects a branch that raises an error on every free run (swallowed, and
surfaced to the operator as "couldn't update the running spend total"). Separately, the shipped
config and the example config select **opposite** discovery branches, so two features that shipped
into one of them — a call-count optimisation and a bio-based email source — cannot run on the
operator's own configuration.

### 4.3 The sweep of Instagram and TikTok for the same shape

**`edits` mode is the reason the answer above is NO for that mode:**

- **TikTok `edits` discards the seven edit search terms in the config.** Verified against the live
  config: the run walks **0 hashtags and 3 hard-coded terms** whose own source comment says
  *"NEVER RUN, NO MEASURED YIELD"*. Neither key is on the dashboard form, so it cannot be corrected
  from the page. An in-code comment claiming both keys are empty is now false.
- **Instagram `edits` pays to discover exactly what its own judge rejects.** The term list contains
  car-edit and motivation terms while the same run's rubric marks those subjects a REJECT
  *"however good the editing is"*. The equivalent term was removed from the TikTok list for this
  reason in an earlier round and not from Instagram.
- A fourth mode is legal via config but absent from the form, and does opposite wrong things per
  platform.
- A typo in one endpoint key silently downgrades to an endpoint measured at **0 of 37 passing**,
  with no warning, unlike its sibling which does warn.
- The dashboard's fallback funnel list holds 10 names against the real 13, missing the **main
  Instagram funnel**. A source comment claims a test asserts the two agree; **no such test exists.**

### 4.4 Not done, deliberately

- **The full 425-suite run did not complete.** Two attempts were killed. Every red was instead
  re-run individually on a settled tree (section 6).
- I did not widen a load-bearing guard responsible for two red suites; that belongs to its owner.
- I did not chase the one genuinely unexplained number in this round (section 5), because it cannot
  change any decision.

---

## 5. WHAT I GOT WRONG

The most useful section. Every failure below produced a **plausible** number.

**1. Three of my own tests were vacuous, and mutation testing caught them.** One asserted static set
membership rather than runtime behaviour; one compared string offsets in source and was satisfied by
a *different* occurrence of the same string; one grepped a file for three words that survived
replacing the refusal it guarded with an always-false branch. All three passed against deliberately
broken code. Rewritten to drive the real functions: **8 of 8**.

**2. I ran the full test suite while my own mutation harness was swapping source files underneath
it.** Thirteen suites went red. The tell was in the timings — my own suite reported **319.9 s
against a 21–32 s baseline.** Six of the nine retested came back green on a settled tree. The run
was discarded, not quoted.

**3. My first file-lock probe passed the wrong file and its control reported "max holders: 0"** —
impossible. Discarded and re-run correctly rather than written down.

**4. I claimed "you are 32 marks away from proving your bar."** Wrong: 78 was *this round's graded
scope*, not the mark corpus.

**5. Correcting that, I published "2,064 wanted pages already have images." Much worse.** I got it by
pooling every mark-shaped file in the project. Its top contributors were a **seen-store backup**
another round wrote that same evening, two **funnel run extracts**, and live scratch files from a
round still running. A seen store records what the funnel *encountered*. **I was counting the
funnel's memory of itself and calling it the operator's opinion.** Worse, the resolver is
last-write-wins, so pooling let machine records outrank his hand marks: **515 of 537** of his
in-sheet pages resolved from a different file, and some flipped from wanted to not-wanted.
**A peer round caught this; I verified it myself and retracted.**

**6. Correcting *that*, my in-sheet filter was still wrong.** A suffix test on the filename also
matched files whose names merely *end* with the sheet filename but are not sheets — 136 rows, 82
pages of contamination. Requiring the basename to *be* the sheet filename gives 12 files and
reproduces an independent count exactly. This is the same shape as a known bug in this codebase
where a prefix test stood in for an identity test.

**7. I reported a confounded experiment as a controlled one.** I said a reversal count moved from 80
to 14 "because of the join key" — having changed the file set *and* the key together. Controlled:

| | exact key | coarse key |
|---|---|---|
| correct 12-file set | **14** | **65** |
| my bad 15-file set | 26 | 77 |

My original 80 was the bottom-right cell: both errors at once.

**8. I measured one thing and published another — in the paragraph where I was cataloguing that very
error.** I measured that the pooled corpus grows (**+64 mark rows in 45 seconds**) and concluded the
reversal count "varies with the minute you sampled." **I never tested that.** Running the control:
two snapshots, **+57 rows arriving between them, every figure identical** (515/14 and 533/65). The
corpus drifts; *this statistic does not drift with it*. A peer ran the same control on their data and
withdrew the explanation before I did.

**So the reversal count is left labelled UNEXPLAINED.** The key's effect runs in *opposite*
directions on the two independent measurements, and no single confound produces both. A tidy story
was available and it was wrong. What survives every key and every snapshot, and is the only part
that carries a decision: **515 of 537** in-sheet pages resolve from a different file once the tree
is pooled, which disqualifies the pooled corpus as a safety denominator regardless.

**9. Three suites went red on my change and two were right to.** Two had each hand-rebuilt "what can
be asked" from parts, so adding a third source of askable models silently falsified **four** copies
at once — hence the single definition in section 2. The third asserted that confidence **88** must
cut; it only ever cut because the dead model's bar was 80, and every surviving model sits at 90.
**The gate was right and the literal was stale** — the same failure as the original 404, one level
up.

**The rule this round earns:** *a number that CONFIRMS the direction you are already arguing deserves
the control, not the number that contradicts it.* My 2,064 supported the conclusion I had just
reached, so I checked its arithmetic and never checked its provenance.

---

## 6. MONEY AND SAFETY

**Vendor spend: about $0.08, against a cap of $1.00**, from **this round's own call counter** — not a
ledger delta, because the shared ledger carries no round id and other rounds were spending
throughout.

| | calls | cost | |
|---|---|---|---|
| `nemotron-3-nano` (free) | 587 | $0.00 | MEASURED |
| `dots-3-note-preview` (free) | 1 | $0.00 | MEASURED |
| `glm-5.3-flash` (paid) | 428 | $0.0381 | MEASURED |
| `nex-n2-mini` (paid) | 325 | $0.0289 | MEASURED |
| liveness verification | ~30 | negligible | MEASURED |
| **total** | **~1,371** | **~$0.08** | DERIVED |

Booking was deliberately **disarmed** in the measurement harness so a scoring pass could not pollute
the operator's ledger, so these calls do not appear in it. **No funnel was run.**

**Seen store — RE-VERIFIED AT PUBLICATION, and the re-check changed the sentence.** When the edit was
made it read 5,993 → 5,985. **At publication it reads 6,044**: my 8 removals still absent, **+59
pages added by funnels running concurrently.** The check-time number was already stale. **The file is
deliberately NOT committed** — it was 3,305 pages ahead of the last commit before I touched it and is
being written to continuously; committing it would file live crawl state under this round.

**Campaigns SHA — re-verified at publication: UNCHANGED.** 5 campaigns, `8e02f8d6f6307ae8` and
`7a029ee5447cddd8` under the two serialisations.

**What was killed:** two of my *own* background test runs, stopped through the task manager. **No
Python process was killed.** All four of the operator's local servers held **identical process ids
from the first check of the round to publication** — verified with a socket listener query, never a
command-line text match, because a process filter once matched itself.

**A standing safety rule of this project is wrong, and it was verified at publication.** The rule
says writing under two source directories hard-kills the dashboard. The watcher **restarts** rather
than kills, its kill command omits the flag that would take child processes with it (so a running
funnel survives), **and no watcher process is running at all.** The live consequence: the dashboard
is serving the code it started with and has not picked up this round's fixes. Runs launched *from*
it are fresh subprocesses and do get them.

**Suite status — honest and incomplete.** Two full runs were killed; the second reached 257 of 425.
Every red was re-run individually on a settled tree:

| suite | state | attribution |
|---|---|---|
| the four I changed, plus the atomic-write guard | **PASS** | — |
| a lifetime-cap suite | **PASS** standalone | its in-suite failure was machine contention |
| two suites | RED | **one shared cause**: a census file that lists where a literal appears trips a guard looking for that literal. A false positive of a class the guard's own comment already records once |
| three suites | RED | a file being edited by another round; a triage registry; and a config switch the operator himself turned on in an earlier round |

**No remaining red is attributable to this round.** Checked, not assumed: none of them references any
module this round changed, and the config file was never touched.

---

## 7. WHAT TO DO NEXT, RANKED

**1. Point the judge at the 237 marked pages that already have pictures.** It needs no marking and no
purchases — the gap is that nobody has run the judge against what already exists: **78 of 237.** At
the kill rate already measured that puts the floor near **96.3%**, above the 95% target. This is the
cheapest item on the list by a wide margin.

**2. Fix the two profile field names.** The judge is currently told a TikTok page has **5** videos
when it has **360**, and is shown no display name. The patch is three lines and is written out in
full in this round's working notes. It is the **third** instance of the same one-word key mismatch in
that one file; the previous two fixes each landed one layer below the next occurrence.

**3. Leave `edits` mode off until the supply bug is fixed.** Today it discards the seven edit terms in
the config and walks three hard-coded ones with no measured yield, on zero hashtags.

**4. Restart the dashboard** when convenient, so it picks up this round's code. Nothing is unsafe
meanwhile; runs it launches already get the fixes.

**5. Do not build parallel judging.** Measured: a second model adds no independent opinion (3.3).

**6. Adopt one criterion for "wanted" and state it on every line.** A want flag (241 pages) and a
score of 9-or-better (127 pages) are different populations and were nearly averaged into one figure
during this round.

---

## 8. PATHS

Paths use `%USERPROFILE%`, which File Explorer expands. **No port numbers** — start the dashboard
from its launcher rather than a bookmarked address, because the port is not stable between runs.

| what | path |
|---|---|
| this round's full working report | `%USERPROFILE%\OneDrive\Desktop\clipper finder\reports\BL-1468.md` |
| the judge, the chain, and the bars | `%USERPROFILE%\OneDrive\Desktop\clipper finder\clippershq\free_judge.py` |
| the preflight that now refuses | `%USERPROFILE%\OneDrive\Desktop\clipper finder\clippershq\preflight.py` |
| the run entry point holding the gate | `%USERPROFILE%\OneDrive\Desktop\clipper finder\clippershq\run.py` |
| the new test suite | `%USERPROFILE%\OneDrive\Desktop\clipper finder\tests\test_bl1468_judge_alive.py` |
| his grading sheets, the honest denominator | `%USERPROFILE%\OneDrive\Desktop\clipper finder\output\` — the 12 folders whose sheet mark file he filled in |
| dashboard launcher (use this, not a saved address) | `%USERPROFILE%\OneDrive\Desktop\clipper finder\tools\dashboard_launcher.py` |
| run the preflight by hand | `%USERPROFILE%\OneDrive\Desktop\clipper finder\clippershq\preflight.py --network` |

---

*No creator handles, addresses, credentials, or lead-store rows appear in this document. Model
identifiers are vendor product names, not personal data.*
