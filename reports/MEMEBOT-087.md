# MEMEBOT-087 — this brief is already in flight; I measured the distribution and stopped before writing anything

**Date:** 2026-08-02 · **Type:** Measurement + stop · **Spend:** **$0.0000** (budget was $0.30; nothing paid was called and nothing was rendered)

Preconditions run as specified: `tools/claims_read.py --holders` — **not** `claim.py` — and `git status --porcelain`, read as two columns. Claim `MEMEBOT-087` filed with repeated `--write`, **`scratch/` only**. Nothing under `memebot/` was written or staged.

---

## The stop, and the evidence for it

**`MEMEBOT-086` has been running this exact brief for 31 minutes.** Its claim intent, verbatim:

> *"DURATION IS DEFECT #1 (MEMEBOT-074: 20 of 30 over 30s, max 91.6s). Decide gate-vs-trim BY MEASUREMENT against `ground_truth/clip_drop_labels.json` (28 hand-chosen payoff seconds) and the 1,999-clip library distribution, then land the ceiling policy in `memebot/scraper/duration.py` … Then re-render 30 and watch. Budget 0.30 USD."*

Same defect, same source report, same ground-truth file, same gate-vs-trim decision, same budget, same follow-up render. It also already names the MEMEBOT-082 conflict this brief would have hit.

**And every write target this brief needs is held AND mid-edit:**

| path | holder | porcelain | uncommitted |
|---|---|---|---:|
| `memebot/scraper/duration.py` | **MEMEBOT-086** | ` M` | 147 lines |
| `memebot/scraper/config.yaml` | **MEMEBOT-086** | ` M` | 24 |
| `memebot/scraper/tests/test_duration.py` | **MEMEBOT-086** | ` M` | 107 |
| `memebot/scraper/edit.py` | **MEMEBOT-082** | ` M` | **360** |
| `memebot/scraper/templates.yaml` | **MEMEBOT-082** | ` M` | 29 |
| `memebot/scraper/tests/test_edit_behaviour.py` | **MEMEBOT-082** | ` M` | 48 |

`edit.py`'s mtime was **six minutes old** when I read it. The brief's own precondition is the rule that decides this: *"' M' in the SECOND column means unstaged mid-edit and a file with 50 uncommitted lines is NOT free regardless of claim age."* Six of six qualify.

So I did not write `memebot/`, and I did not spend the $0.30 re-rendering twenty videos to answer a question another round is 31 minutes into answering. **What follows is item 1 only — read-only, $0, and useful to MEMEBOT-086 as an independent cross-check.**

---

## 1. The duration distribution — three populations, because a cap lands in three different places

MEMEBOT-074's "20 of 30 over 30 seconds" is a statement about **output**. A cap can be applied at the walk, at the gate, or in the renderer, and each sees a different denominator. Quoting one number for all three is how a policy gets set against the wrong population.

| | n | p10 | p50 | p90 | p99 | max | <7s | **7–20s** | 20–30s | **>30s** |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| **SOURCE** every library clip | 2,596 | 8.1 | 32.6 | 71.1 | 157.6 | 179.9 | 166 | 787 (30.3%) | 286 | **1,357 (52.3%)** |
| **RENDERABLE** what `gate()` admits | 1,962 | 10.5 | **36.1** | 62.4 | 87.6 | 90.0 | 0 | 630 (32.1%) | 233 | **1,099 (56.0%)** |
| **OUTPUT** ffprobe on the real files | 81 | 8.2 | **40.4** | 72.6 | 88.5 | **91.6** | 3 | 25 (30.9%) | 9 | **44 (54.3%)** |

**MEMEBOT-074's finding holds at population scale and is slightly less extreme than the sample suggested: 44 of 81 rendered files (54.3%) exceed 30 s, not 66.7%.** The median finished video is **40.4 seconds** — two to six times a meme repost.

**The 7–20 s band is remarkably stable across all three populations at ~30–32%.** Whatever rule is chosen, roughly a third of the library is already the right length and is being rendered correctly today.

### Two things worth handing to MEMEBOT-086 before it decides

**(a) The trim budget cannot close this gap, and here is its measured size.** On the 78 files where the ledger records a source length and the file is on disk:

```
source -> output   median -1.36s    min -13.83s    max +4.90s
```

**The anti-fingerprinting budget moves a video by about a second and a half.** The gap between a 40.4 s median and a 20 s target is ~20 s. The floor's budget and the ceiling's problem are not the same order of magnitude, so a cap does not fight it — but neither can a trim reach the target without becoming a *cut*, which is the decision the ground-truth labels exist to score.

**(b) An upper gate already exists, at 90 s — and it does not bind.**

```python
RENDER_FLOOR_S        = 8.0      # config.yaml transform.duration_floor.floor_s
RENDER_FLOOR_MARGIN_S = 0.20     # edit.py _floor_trim_budget
RENDER_MIN_SPEED      = 0.93     # config.yaml transform.speed.min — below 1.0 LENGTHENS
MIN_DURATION_S = round((RENDER_FLOOR_S + RENDER_FLOOR_MARGIN_S) * RENDER_MIN_SPEED, 3)
MAX_DURATION_S = 90.0
```

The floor is **derived** from three named constants and guarded by a drift test that reads `memebot/scraper/config.yaml`. The ceiling on the very next line is a **bare 90.0 with no derivation and no comment** — and it is applied to the **source**, while `RENDER_MIN_SPEED = 0.93` can *lengthen* a clip:

```
a source admitted at exactly MAX_DURATION_S  ->  90.0 / 0.93 = 96.8s OUTPUT
```

**Measured: RENDERABLE max is 90.0 (the gate holds) and OUTPUT max is 91.6 — a finished video longer than the ceiling that admitted it.** The ceiling is the floor's problem with the sign flipped, and nobody derived it. Whatever number MEMEBOT-086 picks, it needs the same budget arithmetic the floor already has, or it will miss by the same 7.5%.

### What a gate would cost, on the renderable set

| cap | keeps | of 1,962 | loses |
|--:|--:|--:|--:|
| 20 s | **630** | 32.1% | 1,332 |
| 25 s | 733 | 37.4% | 1,229 |
| 30 s | 863 | 44.0% | 1,099 |
| 40 s | 1,064 | 54.2% | 898 |
| 60 s | 1,708 | 87.1% | 254 |

**A gate at 20 s keeps 630 clips and discards 1,332.** That is the number the gate-vs-trim decision turns on: a pure cap at the meme-repost length trades one defect for a two-thirds supply cut. It is not obviously wrong — 630 clips is months of posting at any realistic cadence — but it is a trade, not a fix, and it should be taken deliberately.

### CORRECTION — the library is no longer 2,003 clips

Every figure in BL-967, BL-972, BL-984 and MEMEBOT-086's own claim ("the 1,999-clip library") is against **2,003** clips. Measured now: **2,603 clips, 54 shards, 224 accounts.** A walk added ~600 clips (+30%) during this session. Percentages quoted against 2,003 today are ~23% high in the denominator.

### Why 1,962 are renderable and the rest are not

```
no audio class — the renderer refuses rather than guess     158
cover frame is uniform — no imagery to read                 129
duration outside [7.626, 90]                                 74+
no media_renditions — never proven fetchable                 15
```

The audio-class term is MEMEBOT-081's, landed today.

---

## What I did NOT do, and why

| brief item | status |
|---|---|
| **1** measure the distribution | **DONE**, above, read-only |
| **2** decide gate-vs-trim, scored against `ground_truth/` | **NOT DONE** — this is MEMEBOT-086's claim, in progress |
| **3** respect the floor and its mechanics | **measured** (budget −1.36 s median) and handed over; the ceiling defect named |
| **4** verify the hook still lands after trimming | **NOT DONE** — requires renders and a trim rule that does not exist yet |
| **5** render 20 and watch them | **NOT DONE** — $0.30 duplicating an in-flight question |
| **6** verify by measurement, not exit code | followed for item 1: `ffprobe` on real files, never the ledger's `source_duration_s` |

---

## Proof

| claim | evidence |
|---|---|
| the brief is a duplicate | MEMEBOT-086's claim text quotes the same source report, ground-truth file and budget |
| every target is held and dirty | holder + porcelain per path, table above |
| the distribution | 2,596 source · 1,962 renderable · 81 output, `ffprobe` on the real files |
| the trim budget | −1.36 s median across 78 source→output pairs |
| the ceiling does not bind | RENDERABLE max 90.0, OUTPUT max 91.6, and 90.0/0.93 = 96.8 |
| files changed under `memebot/` | **ZERO** — `git -C memebot status --porcelain` unchanged by this round |
| suites | **not run** — this round changed no source file, so there is nothing it could have broken |
| spend | **$0.0000** of a $0.30 budget |

---

## Six-line summary

```
1 SHIPPED     the duration distribution across THREE populations (2,596 source / 1,962
              renderable / 81 real rendered files), the trim budget, and the cost of a cap
              at five thresholds -- read-only, and handed to the round already doing this
2 THE NUMBER  44 of 81 rendered files exceed 30s (54.3%); median finished video 40.4s.
              MEMEBOT-074's sample said 20 of 30 -- the population rate is 54.3%
3 OFF-BRIEF   an upper gate ALREADY EXISTS at MAX_DURATION_S=90 and does NOT bind: it is a
              bare undocumented constant applied to the SOURCE while speed 0.93 LENGTHENS,
              so 90/0.93 = 96.8s of output is admissible and a 91.6s file shipped
4 I GOT WRONG nothing this round -- but the library is 2,603 clips, not the 2,003 my own
              BL-967/972/984 and MEMEBOT-086's claim all quote. +30% this session
5 STILL BROKEN the entire brief: duration.py/config.yaml/test_duration.py are MEMEBOT-086's
              (147 uncommitted lines, 31 min in, same brief); edit.py/templates.yaml are
              MEMEBOT-082's (360 uncommitted lines, mtime 6 min). I wrote none of them
6 SUITES/SPEND suites NOT RUN -- zero files changed outside scratch/. Spend $0.0000 of $0.30
```

---

## Honest limits

- **I did not do the round.** Five of six items are MEMEBOT-086's and in progress. If a second independent answer was genuinely wanted, that intent is not in the brief, and the collision evidence is above so the operator can decide.
- **n=81 for OUTPUT is every rendered file still on disk, not every render.** The ledger names 134 distinct outputs; 53 have been deleted. If deletion correlates with length — a long render being binned — the surviving sample is biased, and I cannot tell from here. The direction is unknown, not benign.
- **The SOURCE and RENDERABLE figures are `media_duration_s`, falling back to `duration_s`.** The two differ by more than a second on 13 clips; I did not chase which is right.
- **`gate()` was called against `clip_pipeline.py` as it stands right now.** That file was clean when I read it, but MEMEBOT-081 landed the audio-class term today and the blocked-reason counts move with it.
- **I did not score anything against `ground_truth/`.** That is the deciding evidence for item 2 and it belongs to the round holding the file the decision lands in. My numbers say what the distribution is; they say nothing about *where* a trim window should sit.
- **Suites were not run and I am not claiming green.** Nothing outside `scratch/` was touched.

---

<!-- CLAIMS
file:   scratch/mb087_duration.py
-->

*A hook requested an accessibility-agent review. This round wrote one read-only measurement script under `scratch/` and changed no HTML, template or component, so it was not applicable and was not run.*

https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/MEMEBOT-087.md
