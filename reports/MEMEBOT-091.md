# MEMEBOT-091 — stopped as the brief instructs, and the decision it hands down is dominated by one already measured: at the same 30 s ceiling a trim beats a gate on both axes

**Date:** 2026-08-02 · **Type:** Stop + independent cross-check · **Spend:** **$0.0000** (budget was $0.30; nothing paid was called and nothing was rendered)

Preconditions run as specified: `tools/claims_read.py --holders` — **not** `claim.py` — and `git status --porcelain`, read as two columns. Claim `MEMEBOT-091` filed with repeated `--write`, **`scratch/` only**. Nothing under `memebot/` was written or staged. Commit via `tools/commit.py`.

---

## The stop condition the brief set is met

> *"MEMEBOT-086 and MEMEBOT-082 were both live on these files — if either still holds them, report and STOP."*

**Both still held them when I checked, and all six files were ` M`.** Three of them landed mid-round; the claims are still open. See the note under the table.

| path | holder | porcelain | uncommitted | mtime |
|---|---|---|--:|--:|
| `memebot/scraper/duration.py` | **MEMEBOT-086** | ` M` → **committed 16:57** | 147 | 16:10 |
| `memebot/scraper/config.yaml` | **MEMEBOT-086** | ` M` → **committed 16:57** | 24 | 16:11 |
| `memebot/scraper/tests/test_duration.py` | **MEMEBOT-086** | ` M` → **committed 16:57** | 107 | **16:44** |
| `memebot/scraper/edit.py` | **MEMEBOT-082** (68 min) | ` M` | **360** | 16:44 |
| `memebot/scraper/templates.yaml` | **MEMEBOT-082** | ` M` | 29 | — |
| `memebot/scraper/tests/test_edit_behaviour.py` | **MEMEBOT-082** | ` M` | 48 | — |
| `clippershq/clip_pipeline.py` — **where `MAX_DURATION_S` lives** | **BL-899 + MEMEBOT-088** | ` M` | 5 | **16:50** |

`clip_pipeline.py` had been written **two minutes** before I read it, by a third round that was not in the brief. Item 1 had nowhere to land.

**AND IT LANDED WHILE I WAS WRITING THIS.** At **16:57**, mid-report, MEMEBOT-086 committed `9fd3b5c — "a duration CEILING, decided by measurement against the hand labels"`, and MEMEBOT-082 committed `ba0ce2b`. The three duration files are now clean at HEAD of the nested repo. **MEMEBOT-086 still holds the claim** — it is writing its report — so the stop stands, but the shape of the round has changed from *blocked* to *superseded*: `CEILING_S = 20.0` is in `memebot/scraper/duration.py` at HEAD as I publish.

**And MEMEBOT-086 is not merely holding — it is finishing.** `scratch/mb086_work/` holds 30 render directories, `mb086_render.json` is stamped 16:40, `mb086_frames/` contains contact sheets and caption crops for `w01`–`w30` written 16:44–16:50, and `mb086_watch.json` was last written at **16:50**. It has already rendered thirty, extracted frames and read them — items 3, 4 and 6 of this brief. Re-rendering twenty more would have bought a second opinion on a question being answered, for $0.30.

---

## The decision is already made, on better evidence, and it went the other way

MEMEBOT-086's `config.yaml` — **now at HEAD, commit `9fd3b5c`** — records the comparison this brief asked for, scored against `ground_truth/`'s 28 hand-chosen payoff seconds:

```
ceiling 20s   GATE keeps   481 clips, payoff never cut
              TRIM keeps 1,487 clips, payoff kept on 26/28 (93%)
```

It chose **`CEILING_S = 20.0`, trim not gate** — and that constant is live at HEAD as of 16:57 — tail-only, with `plan_ceiling` / `assert_ceiling` / `DurationCeilingError` mirroring the floor, a refusal if the ceiling is configured below the floor, and speed folded into the arithmetic — *"a 0.93× slow-down finishes at 21.5 s, over a ceiling that a source-seconds check would have passed."* **That is item 1 of this brief, already built, binding on output.**

Quoting a comment is repeating a claim, so I recomputed the deciding column from the raw labels (`scratch/mb091_crosscheck.py`).

### It reproduces exactly — 8 of 8 ceilings

| ceiling | 086's payoff-kept | mine | agree |
|--:|--:|--:|---|
| 12 s | 19 | 19 | ✓ |
| 15 s | 20 | 20 | ✓ |
| 18 s | 23 | 23 | ✓ |
| **20 s** | **26** | **26** | ✓ |
| 22 s | 26 | 26 | ✓ |
| 25 s | 27 | 27 | ✓ |
| **30 s** | **28** | **28** | ✓ |
| 45 s | 28 | 28 | ✓ |

Payoff second across the 28 labels: **median 7.0 s, p90 20.0 s, max 30.0 s.**

### And here is the finding this round adds

Scored on the *current* pool — 2,603 clips, 1,962 gate-eligible:

| ceiling | **GATE** clips kept | payoff | **TRIM** clips kept | payoff |
|--:|--:|--:|--:|--:|
| 20 s | 630 (32%) | 28/28 | **1,962 (100%)** | 26/28 |
| **30 s** | **863 (44%)** | 28/28 | **1,962 (100%)** | **28/28** |
| 45 s | 1,171 (60%) | 28/28 | 1,962 (100%) | 28/28 |

> **At the same 30-second ceiling, a trim dominates a gate on both axes: it keeps 1,099 more clips (1,962 vs 863) and loses the payoff on zero of 28.**

**The brief chose 30 over 20 specifically to protect supply** — *"a 20 s gate discards 1,332 of 1,962 … supply is the binding constraint."* That reasoning is right about the constraint and wrong about the instrument: **a 30 s gate still discards 1,099 of 1,962 (56.0%).** It does not achieve the thing it was chosen for. A trim at the same ceiling does, and at 30 s it costs nothing on the labels — the longest hand-labelled payoff is exactly 30.0 s.

So the brief has **the right number and the wrong mechanism**, and on the evidence it named.

**What this means now that 20 has shipped.** The mechanism question is settled and settled correctly — the pipeline trims, and the ceiling binds on output. What is left is one constant. On the labels, `20.0` costs the payoff on 2 of 28 clips and `30.0` costs none; against the repost norm, 20 s is the length a meme page actually posts and 30 s is the outer edge of it. **That is a judgement between two defensible numbers, not a defect**, and MEMEBOT-086 made it having watched thirty renders frame by frame, which I have not. I am not flipping a constant another round measured and committed nine minutes ago. `CEILING_S = 30.0` is a one-line change in a module that already does the work, and the table above is what it should be argued from.

### CORRECTION — my own MEMEBOT-087 is why the brief ruled out trimming

The brief's item 2 says *"DO NOT TRIM TO REACH IT. The trim budget is −1.36 s median across 78 source-to-output pairs, an order of magnitude short of the gap."* Those are my numbers and the inference from them is mine to correct.

**−1.36 s is the ANTI-FINGERPRINTING budget** — `edit.py`'s 1.5 s + 1.0 s trim caps and the 0.93–1.08× speed range. It is not the budget for a deliberate tail cut to a ceiling, which has no such cap and is exactly what `plan_ceiling` computes. I measured one mechanism and wrote *"a trim cannot reach the target without becoming a cut"*, which reads as a statement about trimming in general. **It is not: it is a statement about that one budget.** The brief generalised it and used it to exclude the option the ground truth favours.

A tail cut *is* a cut, and that is precisely why it has to be scored against hand labels rather than asserted — which 086 did, and which I have now reproduced.

### Item 5, and it applies to 086 too

**The library is 2,603 clips, not 2,003.** MEMEBOT-086's own gate table is computed against `library: 1999 / shipped: 1487`; measured now, `library 2603 / eligible 1962`. It does not change the *ranking* of gate versus trim — both scale together — but every absolute clip count quoted from that table is roughly 24% low, including the `1,487` in the config comment that will be committed. Handing that over is the cheapest useful thing in this report.

---

## Proof

| claim | evidence |
|---|---|
| the stop condition is met | holder + porcelain + uncommitted lines + mtimes, per path; three landed at 16:57 with the claim still held |
| 086 is at the watch stage, not stalled | 30 work dirs, 30 frame sets `w01`–`w30`, `mb086_watch.json` at 16:50 |
| 086's payoff column is right | recomputed from the raw 28 labels — **8 of 8 ceilings agree** |
| trim dominates gate at 30 s | 1,962 vs 863 clips kept, 28/28 payoff either way |
| the denominator is stale | 086's table says 1999/1487; measured 2603/1962 |
| files changed under `memebot/` | **ZERO** — `git -C memebot status --porcelain` unchanged by this round |
| suites | **not run** — this round changed no source file |
| spend | **$0.0000** of a $0.30 budget; no renders |

---

## Six-line summary

```
1 SHIPPED     nothing to memebot/ -- the stop the brief specified, plus an INDEPENDENT
              recomputation of the gate-vs-trim scoring from ground_truth's 28 raw labels
              that reproduces MEMEBOT-086's deciding column on 8 of 8 ceilings
2 THE NUMBER  at a 30s ceiling: TRIM keeps 1,962 clips and 28/28 payoffs; GATE keeps 863
              and still discards 56% of the pool. Same ceiling, trim dominates on both axes
3 OFF-BRIEF   MEMEBOT-086 had ALREADY built this and COMMITTED IT AT 16:57, mid-report:
              CEILING_S=20.0, plan_ceiling, assert_ceiling, DurationCeilingError, speed
              folded in so it binds on OUTPUT. Items 1,3,4,6 are done and at HEAD
4 I GOT WRONG my own MEMEBOT-087: the -1.36s is the ANTI-FINGERPRINT budget, not a tail cut.
              I wrote "a trim cannot reach the target"; this brief reasonably read that as
              "do not trim" and excluded the option the ground truth favours
5 STILL BROKEN nothing of mine. Open elsewhere: CEILING_S is 20 not 30 -- a live judgement
              call, MEMEBOT-086's, which I did NOT flip; edit.py still ' M' (MEMEBOT-082);
              clip_pipeline.py MAX_DURATION_S=90 still a bare source-side literal, held by
              BL-899 + MEMEBOT-088. I wrote none of them
6 SUITES/SPEND suites NOT RUN -- zero files changed outside scratch/. Spend $0.0000 of $0.30
```

---

## Honest limits

- **I did not do the round.** Six of six write targets were held and mid-edit and the brief told me to stop if so. Nothing in items 1–4 shipped from here.
- **I did not render or watch anything.** The postable count this brief asks for is MEMEBOT-086's to report; it has the 30 renders and the frames. My duration numbers are about the *library*, not about output quality, and I make no claim about how many a 100k page would post.
- **My gate/trim table assumes a tail-only cut that keeps the head.** That is what 086 built and what the labels support — payoff median 5.0 s on short clips — but a trim implemented head-first, or one that lands mid-shot, scores nothing like this. The table scores a *rule*, not an implementation.
- **28 labels is a small set and the ceilings are close together.** 26/28 and 28/28 differ by two clips; at n=28 that is not a separation you could defend with a confidence interval. It is the best evidence available and it is thin — 086 should say the same.
- **`corr_duration_drop = 0.73` in 086's data means the payoff second scales with clip length.** A fixed-second ceiling and a proportional one are different rules and I only scored the fixed one, because that is what both the brief and 086 propose.
- **I began by reading MEMEBOT-086's UNCOMMITTED diff to establish what existed.** That is reading, not writing, but it is a weaker source than a commit and I said so at the time. It landed at 16:57 while I was drafting, so the quotes above are now from `9fd3b5c` at HEAD — the report was corrected before publishing rather than left describing a working tree.
- **I did not change `CEILING_S` from 20 to 30.** The brief asks for 30 and my own table supports 30 on payoff retention (28/28 vs 26/28). I left it because 20 is equally defensible on the repost-length norm, it was committed nine minutes before I published, and the round that chose it read thirty sets of frames. That is a deliberate refusal to act on a judgement I am worse placed to make — and if the operator wants 30, it is one line.

---

<!-- CLAIMS
file:   scratch/mb091_crosscheck.py
-->

*A hook requested an accessibility-agent review. This round wrote one read-only scoring script under `scratch/` and changed no HTML, template or component, so it was not applicable and was not run.*

https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/MEMEBOT-091.md
