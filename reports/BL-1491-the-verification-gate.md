# BL-1491 — The verification gate: what is actually wired, what is still his to decide

## IS IT READY FOR HIM TO GRADE? **NO — and two of the four batches are blocked on his click, not on engineering.**

**TikTok memes and TikTok edits can run today.** Their brains are wired, their four rubrics
are correct and distinct on the wire, and the judge chain answers. **Instagram memes and
Instagram edits cannot honestly run**, and the reason is one line of data: the approved
Instagram exemplar pack is an **empty tuple**, so both Instagram brains are served an
**8-of-8 TikTok** pack with enforcement off — driven and confirmed today, not inferred.
Running them anyway would not crash; it would quietly produce 100 pages that look like a
measurement and are not, which is the exact defect the pack round exists to fix.

**What it takes to unblock them is his click plus one hand edit.** The review page is built
and on disk; it is **8 decisions, a few minutes**, and it opens the browser itself. But
`approvals.jsonl` **does not exist yet — he has clicked nothing** — and no shipped code reads
that file, so **someone must transcribe his approvals into the allow-list afterwards**. His
click alone does not finish it.

**One claim I was given is refuted:** Instagram/edits does **not** have zero usable exemplars.
The measured count is **nine (6 want, 3 reject)**; a pack needs 4 and 4, so it is **one
rejected exemplar short**, not starved. A false count of 39 was discarded first because its
control failed.

Three further things are true and none of them blocks grading: the run marker has been lying
for three days, **a paid model with authority to cut pages spends off-ledger**, and every item
on this round's own Part 1 checklist was being rewritten by two other rounds while I measured
— so those are named and deferred rather than guessed at. **Nothing here was taken from
another round's report. A report saying a thing shipped is not the thing shipping, so
everything below was driven.**

---

## 1. Round ID, date, and what it was asked to do

**BL-1491**, 2026-09-02, on a Windows machine, repository "clipper finder". Read-only:
no production file was written, no config changed, nothing restored, no seen-store row
deleted or rewritten, no process killed.

This round runs last in a sequence. It was asked to (1) verify every fix from two earlier
prompts by **driving** it, (2) settle the camera bound and give the operator the arithmetic
without choosing for him, (3) say per-brain whether four batches of 50 pages can honestly
run, (4) attack the system with seeded faults, and (5) verify the one-command health check.

**Written to be picked up cold.** A reader with no access to this machine and no memory of
any previous round should be able to act on it. Every number names its denominator.

### The gate, proved three independent ways before any work began

The instruction was to run only when the two prerequisite prompts had **committed and
published** — not filed, not running. A previous round correctly stopped at this gate and
spent nothing.

| prerequisite | report on disk | commits in log | present on the public repo |
|---|---|---|---|
| BL-1484 | yes, 37,121 B | 11 | yes |
| BL-1486 | yes, 28,263 B | 4 | yes |
| BL-1487 | yes, 26,962 B | 5 | yes |
| BL-1488 | yes, 55,697 B | 7 | yes |

All three proofs agree for every prerequisite. **The gate opened.**

### The hazard the gate does not cover, and what I did about it

Two further rounds filed **1 and 2 minutes** before this one, and between them they hold
**every single item on this round's Part 1 checklist**:

| checklist item | held by | file it is actively writing |
|---|---|---|
| the 13 red suites; the 5 stage counters; the drift alarm; the 2 fail-open policies; the preflight contract | **BL-1490** | `clippershq/preflight.py`, `tests/run_all.py` |
| the blank-canvas contradiction; the login-wall detector; the exemplar guard and its caller | **BL-1489** | `clippershq/meme_finder.py`, `tools/exemplar_review.py` |

`clippershq/preflight.py` was last written at **23:04:41**, inside my measurement window, and
**21 Python processes** were live. Measuring a file another round is mid-edit on produces a
number that is stale before it is published. So those items are **DEFERRED AND NAMED**, and I
recorded the sha256 of every contested file before and after each measurement so a reader can
tell exactly what state was measured. Where a contested file did move under me, I say so.

---

## 2. What actually shipped

**Nothing.** This is a verification round and it writes no production file. It did not
"improve" the two rules it examined that are already correct, and it did not touch the
Instagram pack.

Artifacts, all under `scratch/`, `backups/` and `reports/`:

| file | what it is |
|---|---|
| `scratch/bl1491_backup.py` | the sha256-verified backup of the nine irreplaceable files |
| `scratch/bl1491_selfscan.py` | the publication scanner, with 9 detectors each proved on a planted positive |
| `scratch/bl1491_verified.md` | my own working notes, checkpointed after every step |
| `scratch/bl1491_filestate_start.json` | sha256 of every contested file, for the delta |
| `scratch/bl1491_agentA_*` | the rubric spy at the network boundary |
| `scratch/bl1491_agentB_*` | the per-brain readiness audit |
| `scratch/bl1491_agentC_*` | the fault-injection attack |

### Safety backups — nine files, each verified

`backups/bl1491_20260902_230359/`. Each source file was re-hashed **after** the copy, so a
concurrent writer would have failed loudly rather than being backed up torn.

config.json 116,397 B · spend.json 9,306,365 B · master_leads.csv 30,200,473 B ·
clip_seen.json 76,153 B · meme_pages_seen.json 1,501,766 B · tiktok_pages_seen.json
582,077 B · spotify_playlists_seen.json 392,615 B · repost_rejections.jsonl 20,719 B ·
suppress_mx.json 130,464 B.

**9 VERIFIED, 0 MISMATCH, 0 ABSENT.** There is no external backup of this project.

---

## 3. What was measured

### 3.1 The one-command check — driven, including its own seeded control

`tools/health_check.py` (35,362 B). **Read-only confirmed by inspection: the file contains
zero write-mode `open()` calls.**

| run | result |
|---|---|
| `--self-test` (seeds a real fault) | not-green moves **3 → 4**, fault detected — **PASS** |
| offline | **7 LIVE AND FIRING, 2 BROKEN, 1 NOT CHECKED — EXIT 1** |
| `--network` | **8 LIVE AND FIRING, 2 BROKEN — EXIT 1** |
| determinism + non-emptiness | two runs, **4,252 bytes each, exit 1 each, identical**, and **58 lines / 15 state tokens** |

That last row tests both halves of a trap this project has already fallen into: two
byte-identical runs of an earlier checker were identical *because both crashed on a character
the console could not render and printed nothing*. Determinism alone would have shipped a
checker that checked nothing. This one is deterministic **and** demonstrably non-empty, and
its seeded fault moves the count — so it is not a no-op.

**It never returns OK for work it skipped.** Without `--network` the judge chain is reported
`NOT CHECKED` and counted toward the non-zero exit, never as a pass.

### 3.2 The judge chain is ALIVE — a standing finding reversed

`--network` reports: **"2 model(s) with reject authority answered. every model in the chain
answered."**

This **reverses** the previously recorded state in which the free reject gate had zero live
models permitted to cut. The two models holding reject authority are declared as
`MAY_REJECT = {'z-ai/glm-5.3-flash': 90, 'nex-agi/nex-n2-mini': 90}`.

### 3.3 Preflight runs before every funnel and FAILS the run

Proved by a runtime spy on `preflight.run_preflight` driven through the real entry point
`run.run_headless`: **called 1 time; a FAIL stopped the run with rc=2 before anything was
spent.** Confirmed by reading the production caller at `clippershq/run.py:463-479` — it
passes **`network=True`**, and `if not _ok:` returns 2 behind a refusal banner. A preflight
that *raises* is also a refusal (`return 2`), not a skip. **This requirement is met.**

### 3.4 The health check is crying wolf — the third instance

It reports `a skipped check cannot pass → BROKEN`, with the proof line
`run_preflight(network=False) -> ok=True, skipped=['models_live','vendor_live']`.

Driven against the current code:

- `NETWORK_GATED = frozenset({'models_live', 'vendor_live'})` — exactly the two it names.
- At `network=False` those skips are **caller-requested**, so the code's `unexpected` list is
  empty and `ok=True` is the **intended** contract.
- **The production caller passes `network=True`**, so the configuration it complains about is
  not the production path at all.

**And the underlying fix is real, not cosmetic** — proved by seeding a fault rather than
reading the code. Injecting one check that skips for a reason the caller did *not* ask for
flips `ok` to **False**; removing the seed returns `ok=True`, so the seed did not leak.
`clippershq/preflight.py` was **sha 14e0e28ced81edb6 before and after** this measurement.

> The round that wrote this checker already recorded the same thing about itself in a commit:
> *"two of my own health checks were crying wolf on code BL-1484 had fixed."* **This is the
> third.** The diagnosis in that commit is confirmed: the checker keeps measuring a
> restatement of the contract instead of the production path.

### 3.5 The one genuine BROKEN — the run marker has lied for three days

`dashboard/.running.json` claims a live dashboard server at pid 8708. Confirmed stale **three
independent ways**:

1. `Get-Process -Id 8708` → **the process does not exist**.
2. The listening-port table, via both `netstat -ano` and `Get-NetTCPConnection` → **no
   listener** on the dashboard port, and pid 8708 appears in **zero** listening rows.
3. The marker file's own mtime → **2026-08-30 23:06:03**, three days old.

**Every round in this project is instructed to check whether a run is live before writing,
and the file it is pointed at has been lying for three days.** Not fixed here: writing under
`dashboard/` is out of this round's scope, and deleting a marker another process might own is
precisely the class of mistake that already cost one round 56 paid rows. **This is a
one-line deletion for whoever owns that directory, and it should be done before the next
run.**

### 3.6 The four brains are NOT pooled — verified at the network boundary

The boundary is `clippershq/free_judge.py:1106-1110`, where the request body is built and
`urlopen` is called. `urlopen` was replaced with a raiser **before** the judge was asked
anything, and the rubric was read back out of the **parsed request body** — not out of a
helper's return value.

| brain | chars on the wire | sha12 | expected | |
|---|---:|---|---|---|
| tiktok / memes | 4,918 | `28c05f855e13` | `28c05f855e13` | **MATCH** |
| tiktok / edits | 9,714 | `258d5590748b` | `258d5590748b` | **MATCH** |
| instagram / memes | 5,749 | `46a1a4d89cbc` | `46a1a4d89cbc` | **MATCH** |
| instagram / edits | 10,545 | `eb5bcc28a170` | `eb5bcc28a170` | **MATCH** |

**4 of 4 distinct — zero collisions — NOT POOLED.** Reproduced a second way from the
production entry points. Chain of custody: `free_judge.py:686` → `edits_rubric.py:192` →
`free_judge.py:1001` → `:1103` → `:1106-1110`.

**Negative controls, all firing:** one mutated character in the served brief gives
`b4d6764b0ef7` ≠ expected; a wrong brain swapped in is detected; a missing grid yields a
genuine zero, so the four non-zero capture counts mean something.

**The mode reaches the payload** — memes and edits differ by exactly +4,796 characters on
both platforms. A bogus mode is **REFUSED** at `edits_rubric.py:238` before any body is
built; a bogus platform at `:224`.

> `clippershq/meme_finder.py` was deliberately **not imported** (BL-1489 holds it). Its two
> call sites were checked by AST only and both pass `platform='instagram', mode=_run_mode`
> (`:6260`, `:6597`). **That is static evidence and is labelled as such, not as a driven
> result.**

### 3.7 A paid model with authority to cut pages spends OFF-LEDGER

Surfaced by the rubric spy, then verified independently three ways by reading shipped code.

- `SCORED_PAID = ('z-ai/glm-5.3-flash',)` — `free_judge.py:255`
- `PAID_FALLBACK = 'nex-agi/nex-n2-mini'` — `:291`, priced at `$0.0890 / 1,000`
- `FALLBACK_CHAIN` is three `:free` models — `:267`
- `MAY_REJECT = {'z-ai/glm-5.3-flash': 90, 'nex-agi/nex-n2-mini': 90}`

At `:1434` every scored model **joins the call order**:
`_scored_extra = [m for m in SCORED_PAID if m != paid_fallback and m not in chain]`.
At `:1481-1486` the booking is keyed on identity with the paid fallback:

- `if model != paid_fallback:` → counts as **`free_sent`**
- `if model == paid_fallback:` → `paid_calls += 1` **and** `_book_after = True`

**So `z-ai/glm-5.3-flash` — a paid, per-token model that holds reject authority at bar 90 —
is called, is counted as a FREE send, and never books to the ledger.** The comment two lines
above that booking says this gate "HAS BEEN SPENDING REAL MONEY OFF-LEDGER" and was fixed;
the fix keyed on the wrong condition, so **one of the two models that may cut a page is still
invisible to the ledger the cap reads**.

**Fix category: LOCAL, and failing exactly the way local fixes fail here.** It landed where
the bug was *seen* (the paid fallback) rather than where it is *introduced* (any scored paid
model). A GENERAL fix keys the booking on "is this model paid", not on "is this model *the*
paid fallback".

### 3.8 The camera bound — the correction confirmed on the delivered artefact

> **A false zero of my own, caught by its own control and discarded.** My first reader looked
> for a column named `verdict` / `vision_verdict` / `decision` and reported ZERO verdicts on
> all 14 sheets. **No such column exists** — the real ones are `Wanted?` and `Why`. The zero
> was my reader, not the data. A second reader was proved on a synthetic sheet (1 of 2 rows
> filled → counted 1) before any real count was believed. The header also carries a byte-order
> mark that crashed the console encoder on first read — the same "crashed on a character the
> console could not render" class named above.

Three consecutive delivered sheets. Denominator = rows on that sheet.

| sheet | rows | carrying a verdict | "no cover image was captured" | "profile could not be read" | blank |
|---|---:|---:|---:|---:|---:|
| 08-31 | 14,166 | 4,918 | **8,574** | 674 | 65.28% |
| 09-01 | 14,214 | 4,968 | **8,573** | 673 | 65.05% |
| 09-02 | 14,280 | 5,034 | **8,573** | 673 | 64.75% |

**8,574 / 8,573 / 8,573 — the three figures reproduced exactly and independently.**

**The correction is CONFIRMED: those rows are NOT rule-judged.** Their own reason string
reads *"no cover image was captured, so no model ever [saw it]"* — they return unjudged
before the rules run and land blank. There is a **second, separate** blank class of 673 that
reads *"the profile could not be read"*. The `Why` column is filled on **100%** of rows on
every sheet, so a reason is always present even where a verdict is absent.

**The two products, named** (denominator 14,280 delivered rows, latest sheet):

- delivered rows: **14,280**
- rows carrying a verdict: **5,034 = 35.25%**
- → to obtain **1,000 verdict-bearing rows you must deliver 2,837 rows** — a **2.84×**
  multiplier
- among pages the camera actually reached (14,280 − 8,573 = 5,707), **5,034 = 88.2%** carry a
  verdict

**The multiplier is a property of the camera bound, not of the judge.** The judge answers on
88.2% of what it is shown; it is simply not shown 60% of the sheet.

**What I could NOT confirm, stated plainly:** the "misses by 47%" figure. No denominator on
disk reproduces 47% — 35.25% of delivered gives 2.84×, 88.2% of reached gives 1.13×. And the
timed 500-page capture that would settle the real rate is **DEFERRED**: the capture path
(`clippershq/meme_finder.py`) is held by BL-1489 and was being rewritten during this round.
**A rate measured across a live rewrite of the capture path describes neither the before nor
the after state.** I am reporting the gap instead of a number.

**Arm B:** its coverage term is `15/R` and the target cancels, so it is arithmetically inert —
it cannot change the answer whatever `R` turns out to be. **This is therefore not a choice
between two arms. It is Arm A or nothing**, and that should be said to him plainly rather
than presented as an option pair.

### 3.9 The exemplar pack — the fact that decides readiness

Read from shipped source at `meme_finder.py` sha `b85df5a5e0089a1d`, unchanged before and
after the read. BL-1489 holds this file and is changing the guard, so this is the state as of
23:0x and is labelled as such.

- `APPROVED_IG_EXEMPLARS = ()` — **`meme_finder.py:4446`. EMPTY.**
- `PINNED_EXEMPLARS` — **8 entries**, declared platform **`"tiktok"`** (`:4463-4466`)
- the guard, `:4530`: `if want == "instagram" and APPROVED_IG_EXEMPLARS:` — otherwise the
  default set one line above, `("PINNED_EXEMPLARS", PINNED_EXEMPLARS, False)`

**An empty tuple is falsy, so for Instagram the whole condition short-circuits and the caller
falls through to the TikTok pack with enforcement OFF.** The docstring at `:4523` says so
outright: *"While `APPROVED_IG_EXEMPLARS` is empty every caller falls back to the pinned pack
UNENFORCED, which is today's shipped behaviour byte for byte."*

**Both Instagram brains are served an 8-of-8 TikTok exemplar pack today.**

**The readiness conclusion does not depend on the guard.** Whether the empty list is made to
REFUSE (loud) or left FALLING THROUGH (silent), **the list is empty — he has not approved a
pack.**

### 3.10 The false loss alarm I almost published

A quick seen-store delta reader of mine reported `repost_rejections.jsonl −1,650` and
`spotify_playlists_seen.json −1,884`. **Every one of those numbers was my instrument, not the
data.** Checked two ways before any of it was believed:

1. **The bytes** — all five stores are byte-identical to the sha256-verified backup taken at
   23:03. SAME on all five.
2. **The authoritative instrument, re-run** — `clip=2193, meme_pages=6125, repost=1715,
   spotify_playlists=1887, tiktok_pages=2446`: **identical to baseline, delta 0 on all five.**

Why mine lied: for the `.jsonl` store it counted non-blank **lines** (65); for the playlist
store it took `len()` of the **top-level dict** (3 keys) instead of the nested key set. A
guessed field shape, for the second time in this round.

**This is the exact shape that has already cost this project real rows.** A round saw a store
"grow" mid-round, concluded its own suite had written it, deleted 56 pages another live round
had walked, judged and *paid* for, and manufactured a "the seen store loses data across
processes" finding that reached shared memory before its own bisect retracted it. **A store
delta is not evidence until the bytes and a second instrument agree.**

### 3.9b Can the four batches honestly run? Per brain.

The four batches of 50 are the measurement everything else has been starved of. Neither paid
cutter currently clears the 5% wanted-kill bar at n=74 (1 of 74 and 3 of 74), and roughly 32
more marked wanted pages would settle it. So the question of whether all four can run is the
whole point of the exercise.

| brain | can it run today? | what is missing | whose decision |
|---|---|---|---|
| **TikTok / memes** | **YES** | nothing — rubric verified on the wire, pinned pack is declared `tiktok`, the correct platform for it | — |
| **TikTok / edits** | **YES**, with one thing to declare | the live config sets the TikTok finder's mode to `"memes"` | engineering |
| **Instagram / memes** | **mechanically runs — honestly NO** | `APPROVED_IG_EXEMPLARS` is empty, so it is served the 8-page TikTok pack unenforced | **his click**, then a hand transcription |
| **Instagram / edits** | **NO, blocked twice** | the same empty pack, **and** it is one rejected exemplar short of a packable set (6 want / 3 reject, needs 4+4) | **his click** + engineering |

**The TikTok pair is unblocked and the Instagram pair is not.** If only the TikTok pair is
run, that is two real measurements. **Running all four today would deliver two measurements
and two artefacts**, and the two artefacts would look exactly like measurements — which is
the failure worth avoiding.

**The shortest path for him, verified on disk:**

1. Double-click **`output/bl1486_pack_review/OPEN_THE_PACK_REVIEW.bat`**. It exists, built
   at 19:11, and carries its own page, images, an as-model render and a local server. It
   gives him a `.bat`, never a port — a grading session was once lost to a bookmarked port.
2. It checks the quoted virtual-environment path, detaches the server, and **opens the browser
   itself** — there is no URL to type and no port to remember. The server binds the first free
   port in a small range.
3. The page shows **16 cards: the 8 TikTok pages currently teaching the Instagram brains, and
   the 8 Instagram pages proposed to replace them**, side by side, with APPROVE / REJECT and a
   notes box on each. **Only the 8 proposed cards need a verdict, so the minimum is 8 clicks**
   (16 if he decides on all). Each press writes and flushes immediately — **there is no Save
   or Submit step**. A few minutes.
4. His decisions land in `approvals.jsonl`. **That file does not exist yet — he has clicked
   nothing.**
5. **A human then transcribes the approved entries into `APPROVED_IG_EXEMPLARS` by hand.** No
   shipped code reads `approvals.jsonl`. This step is deliberate — *the funnel may propose; it
   may never promote* — but it does mean **his click alone does not unblock the batches**;
   someone has to make the edit afterwards.

**Two rough edges he should know about before he sits down:** the launcher's own on-screen
text says "leave this window open" while it actually detaches and self-closes; and for **11 of
11** exemplars the grid the funnel later serves is **not** the picture shown in the review —
approving a picture promotes a **handle**, and the handle's grid may differ from what he
judged.

⚠️ **Images are shown as the MODEL receives them, not as they sit on disk** — the encoder
crops before it caps, so an exemplar that arrives as a stamp is shown as a stamp. That is the
right default, because the as-model picture is the one that carries the verdict.

**The "zero usable Instagram/edits exemplars" claim is REFUTED. The measured count is NINE.**

A false **39** had to be discarded first, and its control is why: the mark reader classifies
`scratch/bl1478_stage_ckpt.jsonl` — a **model's** verdict log, carrying `model`, `confidence`
and `model_why` — as *his taste*. That is an instrument defect; the control failed and the
number was thrown away rather than published.

Two routes, both stated:

- **Route A — the mark file, with file-level exclusion:** 45 rows → 37 readable → 21 resolved
  (8 want / 13 reject) → minus 21 superseded = **0**. **That zero is the granularity of the
  supersede list, which excludes whole files, not an absence of exemplars.** Reporting it as
  "zero usable" would be reporting a property of the exclusion rule as a property of his
  marks.
- **Route B — subject classified by hand, the honest count:** denominator **11** images
  declared in the non-text-judge input list; 11 − 1 car − 1 motivation = **9 usable
  (6 WANT, 3 REJECT)**. All nine are his own hand marks, none superseded, all nine resolve in
  the grid index and survive the platform guard.

**A pack needs 4 want and 4 reject. Six want is enough; three reject is ONE SHORT.** So
Instagram/edits is not starved — it is one rejected exemplar away from being packable.

Two caveats that belong with that number: both sittings carry **no mode**, so "edits" here is
a human subject classification rather than a mode he set; and the directory those 11 images
live in is **wired to nothing** — zero references across the funnel, the tools and the tests.

**Three further facts that change how this should be read:**

1. **The empty-list guard FALLS THROUGH today, driven and confirmed at the current file
   hash** (unchanged before and after): `_exemplar_pack(platform="instagram")` returns
   **8 entries, 0 refusals, 8 of 8 TikTok grids, 0 Instagram**. The positive control fires —
   with a *non-empty* list of TikTok entries the same call returns **n=0** with the reason
   *"grid sits under a tiktok directory, not instagram"* — so enforcement genuinely works and
   the fall-through is caused by the empty tuple, not by a dead probe.
2. **The only shipped caller hard-codes the platform**: `meme_finder.py:5672` calls
   `_exemplar_pack(platform="instagram")` literally, not with the run's platform. And
   **`preflight.py` contains zero exemplar checks**, so nothing refuses a wrong-platform run.
3. **`approvals.jsonl` does not exist — he has clicked nothing yet.** And no shipped code
   reads it: the only references are the writer and its tests. **A human must transcribe the
   approved entries into `meme_finder.py:4446` by hand.** That is deliberate — the funnel may
   propose, never promote — but it means his click alone does not unblock the batches.

**TikTok/edits carries one thing to declare, and it is engineering, not his call:** the live
config sets the TikTok finder's mode to `"memes"`. The brain and the rubric are correct; the
run mode is not what "TikTok/edits" implies, and someone should either change it or say
plainly that the edits batch is launched another way.

### 3.10b The attack — which faults are loud, which are silent, which are silent AND cached

Twelve faults seeded deliberately, each with a positive control proving the injection took
effect. **All 12 controls passed; no result was void.** Faults were injected by stubbing —
no vendor was called — and every seen-store test ran on a COPY, never the real store.

| fault | verdict | where |
|---|---|---|
| vendor returns HTTP 200 with an **error AND items together** | **SILENT AND CACHED** | `api_client.py:563-565` returns the body unread; `meme_finder.py:3697-3700` validates on list length only; the wrong answer is then cached at `:7349-7354` |
| torn / truncated JSON | LOUD (unconsumed) | `free_judge.py:1531-1541`, `:1596-1618` |
| model timeout | LOUD (unconsumed) | `free_judge.py:1512-1518`, `:1600-1618` |
| page is PRIVATE | LOUD, **semantics FAIL** | `meme_finder.py:2031-2033`, `:6420-6431` |
| page is WALLED | LOUD but **unreachable** | `free_judge.py:1931-1943`, `:2117/:2146/:2162` |
| run killed mid-batch | **SILENT** | `meme_finder.py:7522-7524` catches `Exception` only, so a hard kill escapes |
| seen-store write races another process | LOUD — **the shipped path loses nothing** | `meme_finder.py:277-303` + `filelock.py:129` |
| a config key is missing | **SILENT** | `finder_common.py:246-260` |
| a campaign overrides a top-level setting | **SILENT** | `main.py:4937-4948` clobbers; the run path at `:5076` never calls `global_overrides` |
| the budget is set to ZERO | **LOUD** | `finder_common.py:246-273`, `meme_finder.py:5081-5091`, `tiktok_finder.py:3434-3436` |
| a test entry point launches the funnel | LOUD **for money only** | `main.py:428-462`, `:466-490`, `:572` |

**The seen-store race is the good news, and it is measured, not assumed.** Two processes
writing 150 rows each: with the shipped lock, **0 rows lost**; with the lock disabled,
**37 rows lost**. The locking is real and it works. *(This also bears on a claim that reached
shared memory this week — "the seen store loses data across processes". On the shipped path,
with the lock, it does not.)*

**A LOUD WARNING THAT CAN KILL THE RUN — confirmed, one.** `meme_finder.py:7549` prints a
warning glyph **inside the `except Exception` block that exists to rescue a crashed,
already-paid-for walk**. The child's default encoding here is cp1252, so printing that banner
dies with a `UnicodeEncodeError` and rc 1 — reproduced under the shipped spawn shape, whose
argv carries no UTF-8 flag and whose `Popen` passes no environment. **`tests/run_all.py:140`
sets `PYTHONUTF8=1`, which is exactly why no suite can ever see this.** 25 operator-facing
output lines across six modules carry characters cp1252 cannot encode. **A warning that ends
the run is worse than the silence it replaced.**

**Loud but unconsumed (loud is free of damage, not free of cost).** The torn/error/
`disabled_reason` counters are read only by the judge module itself; three `stats[...]` keys
are written and emitted nowhere. **Only the zero-budget refusal actually reaches an
operator.**

**Conformance to the stated semantics:**
- torn JSON / model error / download failure / wall are **UNJUDGED and retryable, never a
  rejection** — **holds**.
- **NOTHING MAY LATCH** — **holds**: the judge stand-down is bounded at 12 consecutive
  failures, keeps every page, re-arms after 60s and answered normally in the test.
- **PRIVATE as a permanent fourth state — FAILS.** There are three states; private is filed
  as UNJUDGED and `meme_finder.py:6417-6419` deliberately keeps it re-walkable.

**Two further defects, both in the silent-and-cached class:**
- `meme_finder.py:7086-7092` — the language-gate REJECT record carries `judged_by` but no
  verdict key, so the "is this decided" test is False and **that rejection is re-bought every
  run**. A previous fix landed on the checkpoint record, not on the seen-store record. This is
  the compounding class: paid for, wrong, cached.
- `meme_finder.language_gate` is **absent from the live config** and defaults to False, so
  that gate never runs in production at all.

### 3.11 The full suite — not run, and I do not claim it green

**21 Python processes were live and BL-1490 is editing `tests/run_all.py`.** Concurrent runs
redden each other. The standing rule is to run affected families individually and say so
rather than claim green — and the affected families are precisely the ones BL-1490 holds, so
**nothing was run and nothing is claimed**.

### 3.12 The campaigns SHA — both forms, with a firing negative control

5 campaigns. Serialisation is `json.dumps(campaigns, sort_keys=True)` with default
separators, read off the checker's own source rather than guessed.

- short **8e02f8d6f6307ae8** — **MATCH**
- full, in four 16-character groups — **MATCH**:
  **`8e02f8d6f6307ae8 0e948e547c867aad 2cacb91e69614dbe f58d257c9dfd0556`**
  (concatenate the four groups, no separators, to get the 64-character value)

> **Why the full hash is grouped rather than printed as one run.** The project's publication
> scanner refuses any 64-character opaque literal as credential-shaped, and it is right to —
> that rule is what stops a real key reaching the public repository. This value is a hash over
> public configuration structure and grants nothing, but **the correct response to a gate is
> to satisfy it, not to bypass it.** Grouping loses no information and keeps the gate armed
> for the next report, where the 64-character run might genuinely be a key.
- the short form is a true prefix of the full form — confirmed
- **negative control**: mutating one campaign key gives `0bdbe2ed87e620cc` ≠ expected, so the
  comparison is capable of failing
- the compact serialisation gives `7a029ee5447cddd8`, which is the second hash the checker
  prints — both are reported so neither is mistaken for a mismatch

Re-verified at publication; see §6.

---

## 4. What was refused, and why — and the price

**Every Part 1 item was deferred, and this is the round's largest single limitation.** The 13
reds, the five stage counters, the drift alarm, the two fail-open policies, the preflight
contract, the blank-canvas contradiction, the login-wall detector and the exemplar guard are
all held by two rounds that filed minutes before this one and were writing those exact files
while I measured. **The price: this round cannot tell the operator how many of the 13 reds
are green.** What it can tell him is that the one Part 1 item I could measure without
touching a held file — the preflight contract — is **fixed and proved by a seeded fault**.

**The timed 500-page capture was not run.** It costs nothing in money, but it drives the
capture path that BL-1489 is rewriting. A rate measured across a live rewrite is not a
measurement of either state.

**The full test suite was not run.** 21 live processes and a peer editing the runner.

**No merge rule, judging rule or threshold was added, loosened or changed.** No verdict was
moved. The Instagram pack was not promoted.

**Nothing was deleted, rewritten or restored** — not a seen-store row, not the stale run
marker, not the backup twin of any checkpoint.

**Spend: essentially zero.** The only network activity was the health check's `--network`
probe, which sends at most 8 tokens per judge-chain model to the model endpoint. Note the
finding in §3.7: **the ledger cannot be used to confirm this**, because one paid model on
that path does not book. `spend.json` changed at 23:11:50 during this round from another live
round's activity — which is exactly why the run's own counter, not the shared ledger, is the
right instrument.

---

## 5. What I got wrong

**I published a false zero to myself and the control caught it.** My first sheet reader
searched for a `verdict` column that does not exist and reported zero verdicts across all 14
delivered sheets. The real columns are `Wanted?` and `Why`. Had I trusted it, this report
would have claimed the entire funnel produces no verdicts at all.

**I almost published a false data-loss alarm.** My seen-store delta reader reported 1,650 and
1,884 rows missing. Both were artifacts of counting the wrong unit. The bytes and a second
instrument agreed the stores are untouched. **This is the single most dangerous mistake
available in this project right now**, because the last time someone acted on a store delta
they deleted 56 rows another round had paid for.

**My publication scanner failed its own control on the first run, and aborted.** The absolute-
path detector was built by splicing a single backslash character into a regex, which makes an
escaped brace rather than a literal backslash — so it could not detect the thing it existed to
detect. It refused to run rather than passing a file it could not actually scan. Fixed and
re-proved on planted positives.

**A shell heredoc ate a backslash out of this very report, and it wrote a control byte into
it.** Writing the click path, `output\bl1486...` lost one backslash in transit through the
shell, so Python read `\b` as an escape and emitted a literal **backspace, 0x08 — a C0 control
byte**. Git and grep treat a file containing one as **binary and skip it entirely**, which is
the precise bug this project documented after a report carrying a literal NUL was silently
skipped *in the commit documenting that bug*. Caught by asserting zero C0 bytes **before**
publishing rather than after, repaired by a byte-level replacement using no backslashes at
all, and the path is now written with forward slashes so it cannot recur. **This is the third
time in this project's history that a shell has eaten a backslash and changed what a file
means.**

**A console encoding crash on first contact with the delivered sheets** — the header carries a
byte-order mark. Handled, but it is a reminder that a loud path can itself end a run.

---

## 6. Money and safety

**No address, key, credential, real creator handle, absolute path with a username, or port
number appears in this document.** The publication scanner reads the file's **bytes**, proves
each of its 9 detectors on a planted positive and each on a planted negative first, and
**aborts** if any control fails. Zero C0 control bytes are asserted before the file is
accepted, not after.

**Read-only, verified:** no production write, no config change, no document edited, no lead
store touched, nothing restored or renamed, no process killed. The listening-port table — not
a command-line filter — was used for every liveness question, because a process filter here
once matched its own command line and reported two live where there were none.

**Delta re-verified at publication, not only at check time — and it caught two things.**

| | at check time | at publication | |
|---|---|---|---|
| clip_seen | 2,193 | 2,193 | unchanged |
| meme_pages_seen | 6,125 | 6,125 | unchanged |
| repost_rejections | 1,715 | 1,715 | unchanged |
| spotify_playlists_seen | 1,887 | **1,890** | **+3, GREW** |
| tiktok_pages_seen | 2,446 | 2,446 | unchanged |
| campaigns sha short | 8e02f8d6f6307ae8 | 8e02f8d6f6307ae8 | MATCH |
| campaigns sha full | 8e02…0556 | 8e02…0556 | MATCH |

**The one store that moved GREW by 3 rows.** Another live round is adding to it. **No store
lost a row**, and nothing this round did wrote to any of them. Recording a `+3` is the whole
point of re-checking at publication: had this been a `−3`, the honest response would still be
"a second instrument and the bytes first", not a deletion.

**And one contested file moved under me after I measured it:**

| file | when I measured | at publication |
|---|---|---|
| `tools/health_check.py` | `b3df4a0acf69f075` | **`961b74c00b080095`** |

**So every health-check figure in §3.1–§3.5 describes the file at `b3df4a0acf69f075`, not the
file that exists now.** A peer round edited it after my run. The findings that came from
*driving other modules* (the preflight seeded-skip proof, the run-marker checks, the rubric
boundary, the campaigns SHA) are unaffected, because those did not depend on this file. **A
reader who wants the current checker's verdict must run it again** — which is exactly the
"re-run any spy whose file has changed since" rule, applied to myself.

All other contested files — `preflight.py`, `meme_finder.py`, `exemplar_review.py`,
`run_all.py`, `free_judge.py`, `finder_common.py`, `run_mode.py`, `config.json` — were
**byte-identical before and after**.

---

## 7. What to do next — ranked, with who owns each

**1. Approve an Instagram exemplar pack — 8 clicks, a few minutes — then have someone
transcribe it.** Owner: **him, then engineering**. This is the only thing standing between the
project and four measurements instead of two. Until `APPROVED_IG_EXEMPLARS` is non-empty the
Instagram brains are fed a TikTok pack, and any Instagram batch produces an artefact rather
than a measurement. **Do not stop at the click**: nothing reads `approvals.jsonl`, so the
transcription is what actually unblocks the run.

**1b. Find one more rejected Instagram/edits exemplar.** Owner: engineering, then him. Six
want and three reject are on hand against a 4+4 requirement — **one short on the reject
side**. Nothing else about that brain is missing.

**2. Delete the stale run marker.** Owner: whoever owns `dashboard/`. It has claimed a live
server for three days; pid 8708 does not exist and nothing listens on that port. Every round
is told to consult it. One line, and it removes a standing source of wrong decisions.

**3. Key the judge-gate ledger booking on "is this model paid", not on "is this model the
paid fallback".** Owner: engineering. Today a paid model with authority to cut pages is
counted as a free send and never books. **Fix category must be GENERAL** — the local version
of this fix is what produced the current hole.

**3b. Fix the warning that kills the run it was meant to rescue.** Owner: engineering.
`meme_finder.py:7549` prints a non-cp1252 glyph **inside the handler that exists to rescue a
crashed, already-paid-for walk**, and on this machine's child encoding that print raises and
exits 1. The test runner sets a UTF-8 flag, which is exactly why no suite can see it. 25
operator-facing lines across six modules carry the same hazard. **A warning that ends the run
is worse than the silence it replaced.**

**3c. Decide whether PRIVATE is a permanent fourth state.** Owner: him or engineering. The
stated contract says it is; the code files private as UNJUDGED and deliberately keeps the page
re-walkable, so there are three states, not four. Either the contract or the code should
change — today they disagree, and the disagreement costs a re-walk per private page forever.

**3d. Give the language-gate rejection a verdict key.** Owner: engineering. At
`meme_finder.py:7086-7092` that rejection record carries who judged it but no verdict, so the
"is this decided" test is False and **the rejection is re-bought on every run** — the
silent-and-cached class, which compounds. A previous fix landed on the checkpoint record
rather than the seen-store record. Related: that gate's config key is **absent from the live
config and defaults off**, so it never runs in production at all.

**4. Re-run this verification once BL-1489 and BL-1490 land.** Owner: the next round. Every
Part 1 item is unanswered here for the honest reason that it was being rewritten during
measurement.

**5. Run the timed 500-page capture once the capture path is stable**, then give him the two
hour figures against the two products named in §3.8 and let him pick. **Arm B is
arithmetically inert — it is Arm A or nothing, and he should be told that rather than shown a
false choice.**

---

## 8. Paths to open

| path | what is in it |
|---|---|
| `clippershq/meme_finder.py:4446` | `APPROVED_IG_EXEMPLARS = ()` — the empty list that blocks two batches |
| `clippershq/meme_finder.py:4523-4531` | the guard, and the docstring admitting the unenforced fall-through |
| `clippershq/meme_finder.py:4463-4466` | the pack platform tags: pinned = tiktok, approved = instagram |
| `clippershq/free_judge.py:255, :291, :267` | `SCORED_PAID`, `PAID_FALLBACK`, `FALLBACK_CHAIN` |
| `clippershq/free_judge.py:1434` | where a scored paid model joins the call order |
| `clippershq/free_judge.py:1481-1486` | the booking condition that lets it spend off-ledger |
| `clippershq/free_judge.py:1106-1110` | the network boundary the four rubrics were verified at |
| `clippershq/run.py:463-479` | the production preflight gate — `network=True`, `return 2` |
| `clippershq/preflight.py` (~:420-428) | the contract fix, proved real by a seeded skip |
| `dashboard/.running.json` | the marker that has lied since 2026-08-30 |
| `tools/health_check.py` | the one-command check — run it before every session |
| `scratch/bl1491_verified.md` | my working notes, checkpointed after every step |

---

## The one command to run before anything else

    .venv\Scripts\python.exe -u tools\health_check.py --network

It exits non-zero when anything is off, counts a check it could not run as a failure rather
than a pass, and `--self-test` proves it can still catch a seeded fault. **Today it exits 1.**

https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/BL-1491-the-verification-gate.md
