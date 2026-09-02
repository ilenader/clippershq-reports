# BL-1486 — the pack he could not see, and a refusal that could not refuse

> **Reading this cold?** This project runs an automated funnel that finds social-media pages
> worth contacting. Part of it is a vision model — a "judge" — that looks at a screenshot of a
> page and decides whether the operator would want it. The judge is shown **worked examples**:
> eight real pages the operator graded himself, four he loved and four he hated. That set of
> eight is called the **exemplar pack**. There are four judges — Instagram and TikTok, each in
> "memes" and "edits" mode — and each is supposed to have its own pack.
>
> Handles of real creators are redacted throughout as `[IG-1]`, `[TT-1]` and so on. Paths are
> written relative to the repository, or with `%USERPROFILE%`.

---

## 1. Round ID, date, and what it was asked to do

**BL-1486, 2026-09-02.** Run alone. Cap $0.50.

The operator's own words:

> "I will approve it. You just need to make a prompt that actually OPENS it, because right now
> I don't think it's open, and obviously I cannot approve something that I don't see."

He is right, and the gap is embarrassingly simple. Since BL-1471 the code has carried an empty
tuple, `APPROVED_IG_EXEMPLARS = ()`, whose only job is to wait for him to say yes. The proposal
that would fill it existed as **a JSON file of file paths**. A JSON file is not an approval
surface. He was being asked to approve pictures he had never been shown.

So this round had two jobs: **build the thing he actually opens**, and **make sure the thing he
is approving is worth approving**.

**Vendor spend this round: $0.00.** No model was called. Every picture, mark and grid was
already on disk, and every instrument was run offline with the network poisoned before import.
The round's own call counter is zero; the shared ledger is not cited, because it carries a round
id on zero rows and has been observed to move during rounds that made no calls.

---

## 2. What actually shipped

### 2.1 A page he opens by double-clicking

```
output\bl1486_pack_review\OPEN_THE_PACK_REVIEW.bat
```

Two columns of real pictures: the eight pages teaching the Instagram judges today, beside eight
Instagram pages he graded himself. Under each picture: what he scored it, when, which sheet it
came from, and one plain sentence saying why it is there. Per picture, **APPROVE**, **REJECT**,
and a free-text box. Decisions are appended to `approvals.jsonl`, **fsynced on every click**, and
the receipt reports the line count the server **reads back from the file** — never a number it
counted in memory.

He gets the `.bat`, never an address. The port is not stable, a grading session was lost to a
bookmarked one, and one port on this machine is a zombie serving a folder that no longer exists.

### 2.2 The pictures are shown AS THE MODEL RECEIVES THEM

This is the part that changes what he is actually approving. The encoder crops and caps before
the model ever sees a picture, and — measured, not assumed — **the exemplars and the page under
judgement are encoded at different caps**:

| | call site in `_messages()` | cap |
|---|---|---|
| **each exemplar** | `enc(path, 460)` | **460 px** |
| **the page being judged** | `enc(grid_path)` — no second argument | **760 px** (the default) |

A 1.65× linear, 2.73× areal asymmetry between the worked examples and the thing being compared
against them. The page defaults to the as-model render, with the on-disk original one click away.

### 2.3 A refusal that can actually refuse

`clippershq/meme_finder.py`, and this is the defect I did not expect to find. The guard standing
in front of the approved pack was:

```python
approved = {str(h).lower() for h, _s, _w in APPROVED_IG_EXEMPLARS}
source = tuple(e for e in APPROVED_IG_EXEMPLARS if str(e[0]).lower() in approved)
```

It **builds its allow-list out of the very list it then filters**. Every entry is in `approved`
by construction. It is an identity function wearing a guard's comment — and the comment directly
above it read `⚠️ REFUSE ANY ENTRY NOT ON THE APPROVED LIST`. Reading the code top to bottom does
not catch that. Running it does.

Replaced with a refusal that works, and works **generally**:

- each pack **declares its platform in data** (`EXEMPLAR_PACK_PLATFORM`), not in a comment;
- each resolved grid must not be **observed**, from its own path, to belong to another platform.

**A tag is a claim; a path is an observation, and the loader now checks both** — because the
failure being fixed is precisely a list that *claimed* to be the Instagram pack while every file
on it sat under a TikTok capture directory. `None` (a path that says nothing either way) is
explicitly **not** a refusal: missing evidence is not evidence of a mismatch.

The generality test is *does it make the next occurrence impossible, or only remove this one?*
Only 1 of 7 past fixes in this project was general when tested, and 3 of the 6 local ones are
failing today. A declared tag the loader enforces makes the next wrong-platform pack impossible.
A comment does not.

### 2.4 And the argument is now actually passed

`meme_finder.py:5581` called `_exemplar_pack()` — **with no platform argument** — and handed the
result straight to `judge_many(..., platform="instagram")` and `should_reject(...)`. So the
loader honoured `platform=` perfectly while its only caller withheld it. **Fixing the loader
alone would have been a correct fix on a branch nothing takes**, which is the newest failure
class in this project. That line now passes `platform="instagram"`.

### 2.5 Nothing was promoted

`APPROVED_IG_EXEMPLARS` **is still empty.** While it is empty every brain receives today's pack
unchanged — asserted by the pre-existing `test_empty_approval_changes_nothing`, which compares
the platform call against the bare one. **This round moves no verdict.** The funnel may propose;
it may never promote.

---

## 3. What was measured

### 3.1 Every supplier for all four brains, by runtime interception

Not by grep, and not by docstring — a module's docstring in this repo once claimed a caller it
never had. The instrument called the real `_messages()` with call-site-faithful arguments and
dumped every byte placed in the payload.

| brain | exemplars in payload | where all 8 live | as encoded | facts | rubric sha12 |
|---|---|---|---|---|---|
| instagram / memes | **8 of 8** | **TikTok capture dirs** | 215×460 | yes | `46a1a4d89cbc` |
| instagram / edits | **8 of 8** (identical bytes) | **TikTok capture dirs** | 215×460 | yes | `eb5bcc28a170` |
| tiktok / memes | **8 of 8** | TikTok sheet dirs | 155×275 | yes | `28c05f855e13` |
| tiktok / edits | **8 of 8** | TikTok sheet dirs | 155×275 | yes | `258d5590748b` |

Counted two independent ways — image parts in the payload, and `"EXAMPLE - he scored this…"`
label parts — which agree on every row. **All four expected rubric hashes MATCH.**

**Eleven positive controls, eleven fired**, including the one that matters most: planting a
two-entry approved list made `_exemplar_pack` return a different two-file pack, proving
`platform=` was a **starved branch, not a dead argument**. No zero in this section is unproven.

### 3.2 The Instagram pack really is 8 TikTok pages out of 8

Re-resolved file by file this round, not quoted from a report. Both Instagram judges are taught
what a good **Instagram** page looks like using **TikTok** pages.

### 3.3 His marks: the claimed counts verify, and then the denominator moves

The inherited figure — *142 Instagram pages, 33 scoring ≥9 with a grid, 56 scoring ≤2* —
**verifies exactly, all three, derived twice by independent code paths.**

And it is still the wrong denominator. Two of his sheet files **write no `platform` field at
all**, so 101 pages key as `(None, handle)` and vanish from the 142. Both directories carry a
note in his own prose saying they are Instagram and their marks are still used as ground truth.

> **The honest in-sheet Instagram count is 243, not 142.** The 142 is correct for the rule that
> produced it and incomplete as a description of his grading.

And the 101 are not just any pages: **99 of them ARE the held-out set of 99** on which the
shipped Instagram judge's central safety claim ("0 of 34 wanted pages killed") was measured. The
previous round excluded the judge's own test set **by accident, through a missing field**, rather
than by rule.

### 3.4 Both existing proposals are unshippable, for two different reasons

**`scratch\bl1478_ig_pack_proposal.json` — the selection is alphabetical.** All 8 scores are
correct against his marks. But:

```
IG score>=9 pool, first 4 alphabetically  ==  the proposal's "wanted", sorted      MATCH
IG score<=2 pool, first 4 alphabetically  ==  the proposal's "not_wanted", sorted  MATCH
```

The pool was **sorted by handle and truncated**, not ranked by score. Its labels advertise
9, 9, 10, 10 — that is simply what alphabetical order happened to hand it. Ranked by score it
would have begun with an entirely different four. This is the standing failure in this project:
**rank by the key you were given.** Two of its eight are also in a test set.

**`output\bl1471_proposed_pack\` — 3 of its 4 "wanted" are drawn from the held-out 99** the
shipped judge's safety numbers were measured on. An exemplar taken from the set you later score
on is a leak, not a lesson.

Neither proposal disagrees with his marks. They disagree about **selection**.

### 3.5 The four brains, honestly

Mode is **never written into a mark** — 0 of 469 resolved marks carry one, on a corpus where the
normaliser was already known to return `None` for all 9,728 rows. Mode survives only in directory
names, which is an assumption, not evidence.

| brain | marked | excluded | usable | ≥9 w/ grid | ≤2 w/ grid | 4+4 buildable? |
|---|---:|---:|---:|---:|---:|---|
| instagram / memes | 222 | 129 | **93** | 10 | 38 | **yes** |
| **instagram / edits** | 21 | 21 | **0** | 0 | 0 | **NO — EMPTY** |
| tiktok / memes | 196 | 4 | 192 | 36 | 74 | yes |
| **tiktok / edits** | 30 | 30 | **0** | 0 | 0 | **NO — EMPTY** |

**Instagram-edits is empty, not thin.** Every IG-edits mark he has ever made sits in the one
sitting the current brief was written to reverse — car, gym and motivation edits, which are now a
firm no. Agreement on that file is 63.3% across all pages versus 94.1% excluding the reversed
subjects: a 31-point swing. A pack built from those pages would teach the model a rule he has
since reversed. There is no second source: the other edits sheets on disk were **built and never
graded**.

> **What unblocks the two edits judges is his keystrokes, not code.** Seven built, ungraded
> sheets are sitting on disk right now.

### 3.6 The disqualifier detectors, and what they found

Four detectors, run through the repo's own OCR engine, each proved on a positive control.
Denominator for the pool figures: **48 candidate images** — the 10 scoring ≥9 and the 38 scoring
≤2, all with a grid on disk.

**Detector (a), a grid printing its own handle: 13 of 48 fired**, including 2 of my own first
eight, which were replaced. ⚠️ Its **measured sensitivity is 3/13 strict and 6/13 on the fragment
rule** against known positives — so a CLEAN here means **"not detected at roughly 46%"**, not
"absent". That caveat now travels *inside the data file*, computed from the run's own control
rows so it cannot drift from what was measured. The selection rule deliberately uses the more
sensitive fragment reading: on a disqualifier, the conservative direction is to exclude.

**Detector (b), a contact email in frame: 0 of 48 — and the specified control could not be
built.** The nine TikTok pages that publish an address do so in their **bio**, and a bio is not
in the picture. The zeros therefore rest only on a manufactured drawn-address control.
**Sensitivity to a real burned-in address is UNMEASURED.** That is the honest statement, and it
is the one place in this round where a zero is weaker than it looks.

**Detector (c), one cover repeated: 0 of 48 in the pool — and 2 of 8 in the pack shipping
today.** My own hypothesis about this detector was **refuted, and correctly**. I suspected it was
firing on blank tiles; it was not — blanks were already excluded, and the decisive negative is
that another image with the identical 2-lit/10-blank shape **does not fire**. What was wrong was
a *reporting field* counting blanks. Fixing it changed **no verdict**.

### 3.7 ⚠️ A fourth disqualifier class that nobody had — and a refuted refutation

Two findings here, and both matter more than the defect this round was sent to fix.

**A candidate he scored 10 out of 10 is an Instagram LOGIN WALL.** Not a page grid: the Instagram
wordmark, "Log into Instagram", a password field, "Log in with Facebook", "Create new account",
and the site footer. **Zero** of that account's content. I found it by opening the picture.

It passed **all three** detectors clean, on 347 characters of OCR. Shipping it would have taught
the judge that an Instagram login screen is a 10-out-of-10 meme page — strictly worse than the
cross-platform defect this round exists to close. This is a known hazard here (a capture run once
came back walled 20 of 20) and **nothing anywhere checked an exemplar for it.**

So a **fourth detector** was built and proved in both directions: **17 of 17 known walls fired,
0 of 9 genuine page grids fired.** Tile-poverty is recorded but deliberately kept *out* of the
firing rule — this wall yields six tiles, so a tile-count rule would have missed it and
false-positived on partial captures.

Then the whole stored Instagram corpus was walked. **16 of 374 grids are walled**, 358 are not,
and all 16 were opened and audited by hand: **zero false positives**, in four flavours — a full
login wall, "This profile is private / Log in to see", an age gate, and a logged-out profile
header sitting above a completely empty grid. Concentration is uneven: 15 of the 16 come from a
single sheet directory.

**The pack shipping today contains no walled capture — 0 of 8.** This is a proposal defect, not a
live one. What the live pack *does* have is 2 of 8 firing the repeat detector and 5 of 8 at
75–92% empty canvas.

⚠️ **The TikTok sheets were never walk-scanned for this class.** Only the eight in the TikTok
pack were checked, and they are clean. If TikTok captures can wall too, that denominator does not
exist yet.

**And the "empty canvas" refutation was itself wrong.** My brief instructed me that the claim
"five of the current pack are 77–92% empty canvas" is REFUTED, worst 16%, with an all-white
control proving the detector was not blind. The refutation reproduces exactly — and the detector
is blind anyway. It counts a pixel as blank when grey `< 16`, while the sheet builder paints its
canvas at grey ≈ 24.6. **A 100%-empty sheet scores 0.0.** The all-white control exercises the
near-*white* branch and cannot detect a fault in the near-*black* branch — a control that checks
what you suspect rather than the mechanism you depend on.

> **The original claim stands: 5 of the 8 current exemplars are 75–92% empty canvas, and one
> carries a single lit tile out of twelve.** The narrower claim "the same cover pasted twice" is
> false *across the eight files* (8 distinct hashes) and **true within individual grids** — 2 of
> the 8 fire the repeat detector. Two different claims were collapsed into one and refuted
> together.

This is visible to the naked eye the moment the page is opened, which is the whole argument for
building the page.

### 3.8 What survives, and the pack he is actually being shown

| side | candidates | (a) | (b) | (c) | (d) | **survive all four** | of those, well-read |
|---|---:|---:|---:|---:|---:|---:|---:|
| he scored ≥9 | 10 | 2 | 0 | 0 | **1** | **7** | 7 |
| he scored ≤2 | 38 | 11 | 0 | 0 | 0 | **27** | 23 |

**A clean 4 + 4 is buildable, and neither side is thin.** The four "wanted" are three pages he
scored 10 and one he scored 9 — there are only seven survivors at that level, so the fourth slot
honestly reaches down to a 9 rather than pretending to a fourth 10.

The selection rule is written down and **consumes the detector output** rather than a
hand-maintained list — because two entries of the first attempt were dropped for printing their
own handle, and had that list lived in the selector, a wider pool would have quietly re-admitted
them:

> score first · then the most recent mark (last keystroke wins is already how this project reads
> his marks) · then at most two per source sheet, so a pack is not one sitting's mood · then
> handle, purely for determinism.

Compare the proposal it replaces, which sorted by handle and truncated. And the driver
**refuses to assemble the page at all** if the wall detector has not run — proved by running it
before the detector existed and watching it refuse.

### 3.9 The leak check, with a control that fired

The shipped tool reports **203 mark sets, 7,355 handles, 15 briefs — and 9 of the 15 name at
least one page the judge is scored on**, worst 21 handles. So there is no zero to defend here;
the tool is reporting real leaks, and that is a standing finding for another round.

**Its control fires.** A handle drawn from the tool's own discovered corpus, planted into a brief
verified clean beforehand: **leaked=2, both fired**, and the scoring guard correctly voided the
result. A handle present in **0** mark sets, planted the same way: **silent**. Both directions
proved, which is what makes the numbers above mean anything.

Three inherited claims, checked rather than repeated:

- **`MARK_FIELDS` is genuinely too narrow — but the cost is 51 handles, not 1,544.** Measured by
  re-binding the tuple in memory over a pass that reproduces the shipped discovery exactly. The
  earlier figure of 92 is not reproducible because the corpus has grown since.
- **The real hole is the depth limit, not the field names.** Lifting only the directory-depth cap,
  with the shipped fields untouched, takes 203 sets → 739 and **7,355 handles → 8,722**. That is
  **1,367 handles the field names were never responsible for**, and 30 of the 51 that `score`
  appears to buy are reachable by depth alone.
- **The boundary rule in the tool is CORRECT** — neither neighbour may be `[A-Za-z0-9._]`, with
  `@` outside that set so a citation passes. 10 of 10 boundary cases pass. The bare word `edits`
  flags 378 files under a naive substring test and is correctly **never counted** by the tool,
  which discards it as too short. The pathology belongs to the naive test, not to this tool.

**De-identification of the shipped filenames: clean.** 65 files checked against a 108-handle
corpus — **0 handles in any filename**, 0 names off the scheme. Worth recording *how*: the
project's own boundary rule is the **wrong test for a filename**, because `_` and `.` are handle
characters and are exactly what filenames separate with, so it would have returned a false zero.
Filenames were tested by segmentation instead, and that substitution was itself proved on
controls that the prose rule reads as clean.

---

## 4. What was refused, and why — and the price

**Nothing was promoted.** `APPROVED_IG_EXEMPLARS` is committed empty. Only he may fill it.

**I refused to put either existing proposal on his approval screen.** Both are contaminated
(§3.4). Rendering a contaminated pack next to APPROVE buttons invites the exact mistake the
screen exists to prevent. They are rendered on disk and described here instead.

**I did not touch `clippershq/tiktok_finder.py`, `clippershq/control.py` or `config.json`** —
all three are claimed by another round in flight. The TikTok half needed no work anyway (§5).

**I did not run the full test suite.** A test in this repo asserts on a shared filename prefix
and cannot run concurrently, and there were several other rounds live. I ran the two relevant
files directly and report that, rather than claiming a green suite I did not observe.

**Price of the refusals:** the Instagram judges keep a wrong-platform pack until he clicks. That
is the correct price. A previous round measured swapping this pack at n=50 and found **both arms
36/50, kills of his 9-10s 0/25 in each, McNemar 0.250** — no measurable accuracy change at his
own ~77% self-consistency ceiling. This is a **correctness fix, and I claim no accuracy win.**

---

## 5. What I got wrong

**My brief's premises, three of them, and I checked rather than inherited.**

- *"All four rubrics are byte-distinct at head."* **False.** All four are distinct in full, but
  **share an identical first 2,144 characters** — the addendum is appended. Anything comparing
  leading bytes would report all four judges as running the same prompt.
- *"TikTok's exemplars may arrive empty."* **Stale.** A previous round wired them; TikTok now
  receives 8 of 8. A dead comment in the source still says otherwise.
- *"A switch is true at top level and four campaigns override it false."* **Does not apply
  here.** `picture_judge` appears in **0 of 5** campaigns, and so does the free-judge switch.
  Both judges are reached through singleton config blocks that ignore campaigns entirely, so the
  effective answer is *both judges on, memes mode, every run, regardless of campaign*.

**My own errors.**

- I hypothesised the repeat detector was firing on blank tiles. **Refuted** by a decisive negative
  control I did not think of. I was pattern-matching a familiar failure onto a working instrument.
- My first card builder read the provenance fields by the wrong names, so "When" rendered **empty
  on every card** — and a blank field reads as *"he never marked this"*, the opposite of the
  truth. Caught by looking at the output, not by the code.
- My first card builder also read the disqualifier file with a guessed schema, found nothing, and
  reported **no flags on any picture** — a silent zero, the exact failure class this round is
  about, produced by me while writing about it.
- The first shipped page hardcoded two column keys while the render manifest carried three. Every
  proposal row would have matched **neither** column. The markup is server-rendered, so the page
  would still have *looked* right.
- I put **two real creator handles in a code comment** in the shipped script, while writing a
  round about de-identification. Filenames were clean and the data files are legitimately allowed
  to carry handles — a comment is neither, and it is precisely what a de-identification pass aimed
  at filenames and data would step over. Found by an audit, not by me, and removed.
- I built the review page single-threaded. It served `urllib` perfectly and rendered **Chrome's
  own error page**, because the browser preconnects and asks for 32 images at once while the
  accept loop sits behind a socket nothing has sent a request on. **Testing this over HTTP instead
  of in a real browser would have reported it working** — which is exactly why the instruction was
  to open it in a browser.

**A measurement I inherited and could not fully repair:** independence is **UNPROVEN** for the two
sheet files supplying 52 of the final 93 pages. Their pipeline-verdict column is a constant, and a
constant cannot agree or disagree with anything. The detector's zero covers only the files it
could test — and it fires correctly on the two known non-independent controls, so it is not blind.

---

## 6. Money and safety

**Vendor spend: $0.00.** No model call, by the round's own counter. Every input was on disk.

**Backups taken before any write**, timestamped, each verified by comparing sha256 against its
source: `config.json` and all five seen stores, **6 of 6 verified byte-identical**. Worth
restating plainly: there is **no external backup** on this machine — the scheduled one fails and
that is a known, accepted choice — so nothing overwritten here would have been recoverable.

**Nothing was killed that this round did not start.** Process identity came from the
listening-port table, never a command-line match — a process filter here once matched *its own
command line* and reported two servers live where there were none. The one server this round
started was stopped by its own pid.

**The test approvals were deleted.** Two rows were written during the round trip; both are gone,
and `approvals.jsonl` does not exist as this is written. A probe row once landed in his ground
truth; it will not happen from here.

**⚠️ An unrelated live defect, found by tripping over it:** `tools/githooks/pre-commit` is
currently **refusing every commit in this working tree**, and the reason it prints is false. It
invokes bare `python` for the facts guard; bare `python` resolves to a system interpreter that
lacks a dependency, the guard dies on import, and the hook reports *"FACTS.md contradicts the
ledger"*. Under the project's own interpreter the same guard reports **OK, 35 facts checked**.
Nothing is wrong with the canonical file. The round that owns the hook has been told. **The fix
is to resolve the interpreter explicitly** — a bare `python` in a hook is the same class of bug
as an unquoted path.

---

## 7. What to do next — ranked, with the arithmetic

1. **Open the `.bat` and decide.** Sixteen pictures, two clicks each. This is the only step that
   unblocks anything, and it costs him about five minutes. Everything else here is already done.
2. **Add the wall detector to the capture path, not just to exemplar review.** **16 of 374**
   stored Instagram grids are login walls, private-profile screens or age gates — and the judge
   is currently paid to look at every one of them and form an opinion about a page it cannot see.
   The detector is written and proved 17/17 against 0/9. Cost: wiring. Saving: every judge call
   spent on a login screen, plus every verdict those calls produced.
3. **Walk-scan the TikTok grids for walls.** The class was measured on Instagram only; the eight
   TikTok exemplars are clean but that is a sample of eight, not a denominator.
4. **Grade one edits sheet.** Both edits judges have **zero** usable exemplars and seven ungraded
   sheets are on disk. No code can fix this; roughly 8–10 graded pages per brain would.
5. **Fix the blank-canvas detector's threshold**, and re-run every quality claim that used it. It
   currently scores a fully empty sheet as 0.0% empty, so any figure derived from it is suspect
   in one direction only.
6. **Lift the leak checker's directory-depth cap.** It costs **1,367 handles** — far more than the
   field-name defect everyone has been quoting, which costs 51. And **9 of 15 briefs currently
   name a page the judge is scored on**, so this is a live measurement-integrity problem, not a
   hygiene one.
7. **Re-derive the held-out set membership before the next measurement.** The judge's headline
   safety claim is measured on 99 pages that a missing field makes invisible to the mark reader.
   That is how 3 of 4 proposed exemplars came from the test set without anyone noticing.

---

## 8. Paths to open

| what | where |
|---|---|
| the page he opens | `output\bl1486_pack_review\OPEN_THE_PACK_REVIEW.bat` |
| his decisions land here | `output\bl1486_pack_review\approvals.jsonl` |
| the builder, with the mechanics documented | `tools\exemplar_review.py` |
| the loader and its refusal | `clippershq\meme_finder.py` — `_exemplar_pack`, `EXEMPLAR_PACK_PLATFORM`, `_platform_of_grid` |
| the empty gate only he may fill | `clippershq\meme_finder.py` — `APPROVED_IG_EXEMPLARS` |
| the refusal proved by mutation | `tests\test_bl1486_pack_refusal.py` |
| pictures as the model receives them | `output\bl1486_pack_review\asmodel\` + `manifest.json` |
| the verified 93-page pool | `scratch\bl1486_marks_pool.json` |
| the clean proposal and its stated rule | `scratch\bl1486_pack_proposal.json` |
| detector results, controls and sensitivity | `scratch\bl1486_dq_results.json` |
| the runtime supplier map | `scratch\bl1486_spy_payload.json` |

**The one instruction that matters:** open that `.bat`, look at the pictures, and press APPROVE
or REJECT under each one. Nothing enters the live pack until you do.
