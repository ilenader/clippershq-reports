# MEMEBOT-095 — the drop cannot be placed at the payoff, and the reason is not the rule

**NOTHING SHIPPED. Item 2 triggered.** No placement rule clears the bar, and the reason
sits underneath the rule rather than in it: **on 24 of 28 hand-labelled clips the payoff is
in a place the placer is structurally forbidden to aim at.** A better rule cannot reach a
target the clamp excludes.

This is the **fourth** automatic drop-placement idea to fail on measurement, after audio
drop detection (100% fabrication), audio mood (40% reproducibility), and BL-963's signal
comparison (12–12 tie).

---

## 1. The finding the brief did not anticipate: there is almost no room to place

Two mechanics, shipped by two rounds that did not meet:

* **`song_library.place_at_detail` refuses outright** when `clip_len < 2 × hook_len` —
  *"no room to place it later; starting at 0 is the only honest answer"*. It is the first
  branch, not a preference. Otherwise the choice is clamped to `[0, clip_len − hook_len]`.
* **MEMEBOT-086's ceiling trims every clip to ≤ 20.0 s.**

Those two together mean placement is possible **only for hooks under 10.0 s**. Measured
against the live song store:

| | measured |
|---|---|
| hand-marked hooks | **21** |
| shortest / longest | 9.24 s / 26.93 s |
| hooks that can EVER place under a 20 s ceiling | **4 of 21 (19%)** — all from `song02` |
| (clip, hook) pairs with any freedom | **50 of 588 (8.5%)** |
| labelled clips where at least one hook can place | **14 of 28 (50%)** |
| **labelled clips where the LABEL is reachable** | **4 of 28 (14%)** |

Even using the **shortest hook in the store** — the most permissive case that exists — a
20 s clip gives a window of `20 − 9.24 = 10.76 s`. Every label later than that is
unreachable by construction.

```
clip                             window  label   reachable?
3900528591427547715_39246491      10.76      7   YES
3952620206207417320_38422583      10.76      5   YES
3794076927062279403_78094105      10.76      5   YES
3712056345639094481_33304581      10.66      4   YES
3711445528099092854_74742599      10.76     17   no — label past the clamp
3951346812883339612_80072930      10.76     20   no — label past the clamp
3872160633634838837_74742599      10.76     30   no — label past the clamp
… 14 more                             —      —   no — clip < 2× hook, refused outright
```

### The two features are pulling against each other

MEMEBOT-086 chose **trim over gate** precisely to *keep the payoff*, and measured 26/28
(93%) retention. That worked. But `place_at`'s clamp then makes **86% of those retained
payoffs unreachable by the drop**. The payoff is in the video and the drop cannot go there.

**Neither round is wrong on its own terms.** The ceiling protects the picture; the clamp
protects the hook from running off the end. Nobody measured them together, and the brief's
premise — *"the head window now contains the payoff by construction, so the target exists"*
— is true about the **picture** and false about the **placer**.

---

## 2. The rule, scored anyway

The briefed rule, expressed through the shipped clamp: prefer a scene cut within
`snap_tolerance`, else the nearest beat, else `0.43 × length`.

| population | tol | hit rate | baseline | **lift** |
|---|---|---|---|---|
| placeable (n=14) | ±1 s | 7.1% | 6.0% | **1.19×** |
| placeable (n=14) | ±2 s | 7.1% | 11.9% | **0.60×** |
| label reachable (n=4) | ±1 s | 25.0% | 19.1% | **1.31×** |
| label reachable (n=4) | ±2 s | 25.0% | 36.4% | **0.69×** |

**Nothing clears ~1.5×.** Three of the four figures are at or below chance, and the best is
1.31× on **n = 4**, which is not a result.

### Two scoring choices that change the answer, both stated

**The baseline is a SINGLE PICK, not any-of-n.** BL-963 asked *"does any of this signal's
n events fall within tol"* — for 11 cuts on a 20 s clip that is already ~52%. A placer does
not get n guesses; it picks one time, so its baseline is one uniform draw from the window
it may pick in. Using BL-963's baseline here would have set the bar far too high and scored
a working placer as worthless.

**The closed form was wrong and the empirical check caught it.** `2·tol / window` assumes
the target is inside the window. On this population **10 of 14 labels are outside it**,
where a uniform draw can never hit and the true probability is 0, not 18.9%. The closed
form reported ±1 s lift as **0.38×** where the empirical says **1.19×** — an artefact in the
*pessimistic* direction, but an artefact. Both are in the JSON; the empirical is the one to
read. This is why the Monte Carlo was run alongside a formula that looked obviously correct.

---

## 3. Item 3 is moot, and that is the point

No renders were produced, no flag was wired, no frames were hand-judged — because item 2
fired first. Rendering 15 clips to inspect a placer that scores below chance would produce
15 videos and no evidence.

**It could not have shipped anyway.** `memebot/scraper/edit.py` is `' M'` and owned by
MEMEBOT-094 (landing the ceiling and the orphaned `_floor_trim_budget`), and
`clippershq/song_library.py` — where `place_at` lives — is held by MEMEBOT-093. Both were
checked before any code was written; nothing was written into either.

---

## 4. Mechanics, respected and corrected

* **`place_at` already snaps to cuts.** `place_at_detail(clip_len, hook_len, cuts=...)`
  picks the nearest cut within `min(1.0 s, 12% of clip)` and records `snapped`,
  `snap_cut_s`, `snap_shift_s`, `snap_reason`. The briefed rule's cut half **already
  exists** — and is **unreached**: `render_plan(clip, store, *, count, bias, cuts=None)`
  takes the parameter, and **both** production callers (`clip_pipeline.py:439` and `:1336`)
  omit it, so `cuts` is `None` on every render and the fixed fraction is the only path ever
  taken. The beat fallback does not exist at all.
* **`fraction × clip_len` is clamped to `latest`**, so on any clip near the gate the "43%
  target" is not 43% of anything — it is the clamp.
* The 8.0 s floor, the 20 s ceiling and the −1.36 s median trim were taken as fixed and the
  window was computed **after** them, per item 4.
* Beat *timestamps* were used only as a fallback candidate and never as ground truth,
  per the settled finding.

---

## 5. Inter-rater agreement: NOT PRODUCED, and the reason disqualifies this round

`ground_truth/README.md` names the missing second labeller as *"the single biggest gap and
the cheapest to close"*. **This round could not close it.**

**The labels were read before any sheet was opened** — all 28 `drop_s` values were printed
while measuring placement freedom, which is upstream of everything else here. A "blind"
second pass by a rater who has seen the first rater's answers is contaminated toward
agreement, and an inflated agreement figure is worse than none: it would retire the loudest
caveat on the dataset while leaving the bias in place.

What was done instead is **adjudication** — the weaker question contamination cannot
flatter: *is the recorded second defensible from this image?*

| clip | record | conf | verdict | adjudicator's alternative |
|---|---|---|---|---|
| `3869108095872285783` | 2 s | low | DEFENSIBLE | 3 s |
| `3952620206207417320` | 5 s | high | DEFENSIBLE | 4 s |
| `3712056345639094481` | 4 s | high | DEFENSIBLE | — |
| `3711445528099092854` | 17 s | low | DEFENSIBLE | 18 s |

**4 of 4 defensible within ±1 s** — including all three that a wrong label would have
changed a conclusion on. A disagreement under a bias toward agreeing would have been strong
evidence; a concurrence is weak evidence and is reported as weak.

**The gap remains open and still costs $0**, for someone who has not read
`clip_drop_labels.json`. Every payoff-scored result in this project — BL-963's 1.52×,
MEMEBOT-086's 93% retention, and the numbers above — inherits an unbounded single-labeller
bias until then.

---

## 6. What would actually make this work

Not a better rule. The order is:

1. **Mark a short hook.** 4 of 21 hooks can place; all four are `song02`. A hand-marked
   hook of ≤ 6 s would give a 14 s window on a 20 s clip and make most labels reachable.
   That is a hookmark task, not a code task.
2. **Then re-measure.** With the window opened, the cut-snapping that `place_at_detail`
   already implements becomes testable against the labels for the first time.
3. **Only then consider a beat fallback**, and only if step 2 clears — the 14% of clips
   with no cut is the coverage argument for it, not a lift argument.

Shipping a placer before step 1 would be placing a drop inside a 10 s window on clips whose
payoff is at 17 s, which is what the current 43% fraction already does.

---

## 7. Proof

- `scratch/mb095_freedom.py` / `.json` — the joint constraint; 4/21 hooks, 8.5% of pairs,
  4/28 labels reachable.
- `scratch/mb095_score.py` / `.json` — the rule scored through the real
  `song_library.place_at_detail` clamp, single-pick baseline, closed form **and** 20,000-trial
  Monte Carlo.
- `scratch/mb095_relabel.py` / `.json` — 4 sheets adjudicated, with the contamination
  recorded in the artefact rather than only in prose.
- **Full suite: 152 suites, 1 red — `tests/test_filelock.py`, which PASSES on re-run.**
  It is a file-locking test and 11 rounds were in flight; lock contention is the flake it
  is built to detect. `clippershq/filelock.py` is unclaimed and clean. This round wrote
  three `scratch/` files and nothing else, and `run_all.py` excludes `scratch/` by design.
- **Spend: $0.00** against a $0.20 budget. No paid calls, no renders, no network.
- Nothing was written to `memebot/scraper/edit.py` (MEMEBOT-094, dirty) or
  `clippershq/song_library.py` (MEMEBOT-093).

---

## 8. Still open, and whose

1. **The ceiling and the clamp have never been measured together.** `duration_ceiling` is
   MEMEBOT-086's/094's; `place_at` is MEMEBOT-093's. Whichever moves next should read §1.
2. **No hook under 9.24 s exists.** A hookmark pass would unblock the whole idea; the
   hook-marking page (`hookmark/`) already exists.
3. **Inter-rater agreement is still unmeasured** — needs a rater who has not read the
   labels.
4. **`place_at`'s cut-snapping is shipped, tested, documented — and unreached.** Both
   production callers of `render_plan` omit `cuts`. `song_library.py` is MEMEBOT-093's.
   Note its own comment explains why there is deliberately no `clip.get("cuts_s")`
   fallback: no walk stores cuts and `dict_of` does not forward them, so the field and the
   passthrough must land together, in one round, with a test.
