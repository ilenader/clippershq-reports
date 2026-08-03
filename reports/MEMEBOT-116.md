# MEMEBOT-116 — the fixed-5s drop target, landed. And the third half nobody had named.

MEMEBOT-105 measured the single biggest quality lever in the render path and deliberately
did not land it. BL-1021 then corrected the operator-facing claim: re-marking hooks alone
buys 2 → 8 of 28, because **both** changes are needed. This round lands the code half.

It also reports, from 15 rendered videos, that there is a **third** change neither round
named, and without it the other two cannot show up on screen at all.

---

## SUMMARY

```
SHIPPED     PLACE_AT_TARGET_S = 5.0 in song_library.py, fraction RETAINED as the fallback;
            13-check test; 19 stale 43% assertions updated; hookmark mirror; 15 renders
ONE NUMBER  2.00s median |err| and 16/28 within 2s, against 3.47s and 8/28 for the fraction
OFF-BRIEF   place_at_s is PLANNED AND NOT APPLIED on 15 of 15 renders -- clip_pipeline.
            hook_chain, the function that would apply it, has ZERO CALLERS
GOT WRONG   my first watch verdict scored 5 rows "placement APPLIED" that had plan=0.00 --
            a tautology. Reclassified; the honest count is 0 of 6 applied
STILL BROKEN the renderer cannot consume a placement (nobody's claim); hooks still 9.24s+
            so only 4 of 21 can place (the operator's half); 8 of 28 labels unreachable
SUITE+SPEND parent 183/187 (4 reds ALL GREEN STANDALONE, 13 rounds in flight);
            memebot 250/250 OK. $0.0126 of a $0.12 cap, 15 renders
```

---

## 1. The constant, landed and scored

`clippershq/song_library.py`:

```python
PLACE_AT_TARGET_S = 5.0     # the target
PLACE_AT_FRACTION = 0.43    # RETAINED — the fallback where a fixed offset cannot fit
```

`place_at_detail` now runs a **two-rung ladder**, and records which rung answered in a new
`target_rule` field so a render record read months later says *why* the drop is where it is:

| condition | result |
|---|---|
| `clip_len < 2 × hook_len` | `0.0` — the refusal, **untouched** |
| `5.0 ≤ clip_len − hook_len` | `5.0` — the fixed target |
| otherwise | `0.43 × clip_len` — the fraction |

**The fallback is not decoration.** Clamping to `latest` instead would pin the drop to the
last legal instant on every short clip — a worse rule than the proportional one being
replaced. On the 8.0s floor with a 4s hook, `latest` is 4.0s and the fixed offset genuinely
cannot fit; that clip gets 3.44s.

### BEFORE and AFTER, through the shipped function

28 hand labels (`ground_truth/clip_drop_labels.json`, one labeller, one pass, **1s
resolution** — nothing here supports a claim finer than ±1s), on a 20s tail-trimmed clip.

| hook | rule | median \|err\| | within 2s | within 3s | mean signed |
|---:|---|---:|---:|---:|---:|
| 4.0s | `0.43 × len` | 3.47s | 8/28 | 12/28 | −3.37s |
| 4.0s | **fixed 5.0s** | **2.00s** | **16/28** | **17/28** | −5.19s |
| 9.24s *(today's shortest real hook)* | `0.43 × len` | 5.70s | 4/28 | 7/28 | −5.77s |
| 9.24s | **fixed 5.0s** | 6.00s | 6/28 | 9/28 | −7.54s |
| any | start-at-0 *(what ships when the refusal fires)* | 7.00s | 2/28 | 5/28 | −10.04s |

**Stated against my own interest: at today's hook lengths the median gets slightly WORSE**
(5.70 → 6.00) while the hit rate improves (4 → 6 within 2s). 14 of 28 clips are shorter than
twice a 9.24s hook and refuse to zero, so the target is never consulted on half the set. The
2.00s / 16-of-28 result **requires the operator's half**. The two changes are multiplicative,
not additive — exactly as MEMEBOT-105 said.

*(The scorer validates itself against `place_at_detail` on 28 clips × 5 hook lengths before
reporting anything; a scorer that has drifted from the code it claims to measure is why.)*

---

## 2. The ceiling, stated honestly

At `CEILING_S = 20.0`, no placement rule can reach a label past `clip_len − hook_len`.

| hook | last legal start | reachable by ANY rule | past the 20s ceiling | past the last legal start |
|---:|---:|---:|---:|---:|
| 3.0s | 17.0s | **20/28 (71%)** | 2 | 6 |
| 4.0s | 16.0s | 17/28 (61%) | 2 | 9 |
| 5.0s | 15.0s | 14/28 (50%) | 2 | 12 |

**The brief's figure is confirmed exactly**: 71% reachable at best, **2 of 28** with the
payoff past 20s outright (at 30s and 25s), and **6 more** past the last legal hook start.
**No hook length and no detector reaches those eight.** Any future claim above 20/28 within
2s is arithmetically impossible without raising the ceiling.

---

## 3. It does not fight the other constraints

| constraint | interaction |
|---|---|
| **8.0s floor** | the only place the fallback fires: 8.0s clip + 4s hook ⇒ `latest` 4.0s, fixed 5.0s cannot fit ⇒ 3.44s |
| **tail trim (−1.36s median)** | trims before placement sees the clip; a fixed target does not scale, so a trim can only reduce room *after* the drop, never move the target |
| **`CEILING_S = 20.0`** | 5.0s is far inside it; the ceiling binds `latest`, not `target` |
| **`clip_len < 2 × hook_len` refusal** | **untouched, and still wins.** At 15.0s/9.24s there is 5.76s of room so 5.0s would "fit" — the refusal fires anyway. Pinned by a test. |

**Placeability today: 4 of 21 hooks.** A hook can place only if `2 × hook_len ≤ 20.0`, i.e.
`hook_len ≤ 10.0s`. The shortest real hook is **9.24s**, and only song02's four hooks (9.24,
9.61, 9.62, 9.81s) qualify. Every hook on songs 01, 03 and 04 is 14.4–26.9s and can never
place at any clip length the renderer produces.

---

## 4. Fifteen renders, and the finding that outranks the constant

15 videos rendered through a **pinned memebot HEAD snapshot** (`7a7cadc`; MEMEBOT-115 is live
on `edit.py`) with the patched placement. $0.0126 of a $0.12 cap, 1016.7s wall.

**`place_at_s` is computed, recorded, and never applied.** All 15 records carry:

> `plan_unapplied: "edit.py has no placement or loop input: place_at_s, loop_count were PLANNED and NOT applied"`

And `clip_pipeline.hook_chain` — the function written to apply it via `adelay`, whose own
docstring says it *"makes the recorded `place_at_s` real rather than a number the record
carries and nothing honours"* — **has zero callers**.

### Measured, not just read off the source

Envelope cross-correlation of each render against the song, cut from the **APPLIED** window
(`song_detail.window_start_s`), never the marked one — `fit_window` widens, and correlating
against the marked window once read 11 of 20 videos as missing their song when the truth was
20 of 20.

| outcome | n | meaning |
|---|---:|---|
| planned 5.0s, measured lag **0.00s** | **6** | the hook starts at frame one — **not applied** |
| planned 5.0s, correlation < 0.40 floor | 4 | **UNRELIABLE** — not evidence either way |
| no placement planned (2× refusal) | 5 | frame-one *is* the plan; nothing to judge |
| **placement applied** | **0** | — |

**Correction I had to make to my own harness:** the first pass labelled 5 rows "placement
APPLIED" — every one of them a row where the plan was `0.00` and the lag was `0.00`. That is
a tautology, and it is exactly the false-positive shape this repo has been bitten by before.
Reclassified with an explicit correlation floor; the honest count is **0 of 6**.

### Hand-judged at the planned 5.0s mark

Six frames per clip spanning 4.0–6.5s. **HIT** = a hard cut or discrete impact whose onset
falls within ±0.5s of 5.0s. Frames are 0.5s apart, so an onset is localised to a 0.5s bucket
and nothing finer is claimed.

**4 HIT / 6 MISS** of the 10 clips where a 5.0s drop was planned:

- **HIT** — Ruffalo→Cheadle cut (4.5–5.0s); Harley→Joker cut (5.0–5.5s); close-up→group cut
  (4.5–5.0s); close-up→wide arms-out cut (4.5–5.0s)
- **MISS** — continuous scope pan; continuous talk-show shot; throw at ~5.5 with the cut at
  ~5.75 (late); and **three cuts at ~4.25s — 0.75s early**

Three of six misses clustering 0.75s early is interesting and is **not** a recommendation:
at n=10 with 0.5s frame spacing it is an observation. MEMEBOT-105 already showed 5.0 sits on
a plateau (4s→12, 5s→16, 6s→14, 7s→13 within 2s), so the defensible claim remains *"a fixed
target in the 4–7s band beats the fraction"*, not *"5.0 is optimal"*.

---

## 5. The operator's half — one paragraph

**Re-mark the hooks to ~4-second cores.** Every one of the 21 hand-marked hooks is currently
9.24–26.93s, and `place_at` refuses to place any hook longer than half the clip; since the
renderer never produces a clip longer than the 20s ceiling, that means a hook must be ≤10.0s
to place at all, and only song02's four qualify. **Re-marking to 4s cores takes
hooks-that-can-place from 4 of 21 to all 21**, and it is what turns the constant landed here
from a number in a ledger into 16-of-28 within 2s of the hand-labelled payoff — the fixed
target aims, but the re-marking is what creates something to aim. The spec already exists at
`scratch/mb105_remarking_brief.md`; the work is per-hook and needs an ear, not a detector.
**Both are still gated on a third change that is nobody's claim: `edit.py` cannot consume a
placement, so until `hook_chain` is wired, neither half moves a single frame on screen.**

---

## 6. Concurrency and honesty notes

- `clippershq/song_library.py` is claimed by **MEMEBOT-112**, which at 51 minutes had written
  nothing and whose work is in `_compile_terms` — a disjoint region. The file was clean. I
  took it with `Claim-Override` on the record and committed **immediately**;
  `scratch/mb116_apply_patch.py` re-applies the identical edit if a whole-file write lands
  over it. Committed alone, so no round's paths were bundled with another's.
- `memebot/scraper/edit.py` is **MEMEBOT-115's** — rendered *through* it from a pinned HEAD
  snapshot, never edited.
- **The 15 render rows landed in the live `memebot/runs.jsonl`** despite an override pointing
  elsewhere: the record path is resolved inside the renderer. They are real renders and
  belong on the ledger, but they were made with a placement constant that — as §4 shows —
  changed nothing on screen. They are identifiable by `mb116_work` in their `output` path.
- `ig_client` reported **21 billed requests never written to `spend.json`** (the BL-876 leak)
  at the end of the run. Not introduced here and not this round's to fix, but recorded.

---

## 7. Suites

**memebot** — `scraper/tests`, **250 of 250 OK**.

**parent** — `tests/run_all.py` at `HEAD` with **13 rounds in flight**: 183 of 187 green in
1583s. The four reds were `test_doc_citations`, `test_filelock`, `test_runner_contract` and
`test_silent_zero_shape`, and **all four pass standalone**, re-run minutes later against the
same tree. That is the documented pattern here — a full-suite red set on a busy tree is a
moment, not a property (BL-906 measured four different red sets in one evening, every suite
green standalone). Recording the count with its HEAD and its live-claim count rather than
calling any of it standing.

The suites this round actually touches were run standalone and are green:
`tests/test_song_library.py` ALL PASS, `tests/test_place_at_fixed_target.py` 13/13,
`memebot/scraper/tests/test_duration.py` 32/32.
