# MEMEBOT-014 — `should_bias` is wired. The biased window lands at **exactly 2.00×**, the sequence is byte-identical across fresh loads, and on today's data the rule correctly fires **never**.

**Date:** 2026-08-01 · **Type:** Implementation · **Spend:** $0.00 · **Paid calls:** 0
**Changed:** `clippershq/song_library.py`, `tests/test_song_library.py` (+10 tests).
`outcome_loop.py` untouched — it owns the statistics and this round does not re-implement them.

---

## The mechanism: bias by dividing effective uses

The hard constraint was item 4 — the bias must not break determinism. Rotation was
`min(key=(hook.uses, song.uses, song_id, hook_id))`, a total stable order.

**A proven window's uses are divided by its weight.** It reads as less-used than it is, so
least-used-first reaches it sooner:

```python
w = float((bias.get(hook_key(s, h)) or {}).get("weight") or 1.0)
w = max(1.0, w)                    # bias only ever HELPS; never demote here
out.append((int(h.get("uses") or 0) / w, int(s.get("uses") or 0), song_id, hook_id, s, h))
```

Three properties fall out of that one line, and none of them is a check bolted on afterwards:

- **Determinism is untouched.** The key is still a plain total order over
  `(float, int, str, str)`, computed from the same state. No randomness anywhere.
- **The 2× cap is STRUCTURAL, not a limit test.** At weight `w` the window settles where
  `uses/w` equalises against `uses/1` — i.e. at exactly `w×` its peers. `w=2.0` **is** the
  ceiling; the share cannot run away even if the weight were mis-set.
- **It can never be exclusive.** Every pick raises the window's own `uses` and hands the next
  turn back.

That last point carries the comment the brief asked for, in `_candidates`:

> *A WINDOW THAT STOPS BEING SAMPLED CAN NEVER BE SHOWN TO HAVE DEGRADED. That is the whole
> reason for the cap: an exclusive winner freezes the evidence at the moment it won, and a
> window whose audience moved on would keep winning on stale data forever.*

---

## The proofs

### 1. Below the bars — rotation is byte-identical

```
n per window: 8 (bar is 25)
bias_map     : {} — nothing earned
shares       : unbiased {'h1': 20, 'h2': 20, 'h3': 20}
             : with map  {'h1': 20, 'h2': 20, 'h3': 20}
IDENTICAL    : True
```

Even with a window showing **100× the views of its peers**, at n=8 the map is empty and
rotation does not move. A test also pins that an empty map is identical to no map at all.

### 2. Above both bars — 2.00×, never exclusive

```
EARNED scratch/song01.mp3@20.0-25.0
   n=30 weight=2.0
   earned: n=30, 95% CI [49493.5, 49506.5] excludes zero. (bias weight 2.0, never exclusive)

shares over 60 picks: {'h1': 30, 'h2': 15, 'h3': 15}
winner h1 = 30 ; others = [15, 15] ; ratio 2.00x (cap 2.0)
NEVER EXCLUSIVE — every window still sampled: True
```

Exactly 2.00×, and the two unbiased windows keep half the rotation between them.

A further test pushes the weight to **50×** — an absurd mis-set value — and every window is
*still* sampled, because the structural cap does not depend on the number being sane.

### 3. A significantly worse window is refused

```
window 0 median is 100x LOWER than its peers, n=30 (enough data)
in bias_map? False
should_bias -> False : significantly WORSE than the rest — do not bias toward it
shares with that map: {'h1': 12, 'h2': 24, 'h3': 24}  (still rotating)
```

**The loser is not demoted — it keeps 12 of 60 picks (20%).** The other two windows earned
bias on their own evidence, which is why they sit at 24. A test also pins that a sub-1.0
weight is clamped to 1.0: **this mechanism can only ever promote.** Demoting a window would
starve the evidence needed to ever change the verdict.

### 4. Determinism with bias on

```
A: 123112311231123112311231
B: 123112311231123112311231
IDENTICAL: True
uses after 24: [12, 6, 6]
```

Two fresh loads, identical sequence. The `1231` period is the 2:1:1 ratio made visible.

### 5. The biased pick explains itself

```
song_id       sng_0001
hook_id       h1
biased        True
bias_weight   2.0
bias_n        30
bias_reason   earned: n=30, 95% CI [49493.5, 49506.5] excludes zero. (bias weight 2.0, never exclusive)

unbiased plan: biased=False weight=1.0 reason=''
```

Four fields ride on **every** plan, biased or not. The docstring says why:

> *Without them a favoured window is indistinguishable from a bug: you would see the same hook
> keep winning and have no way to tell an earned preference from a broken tie-break.*

---

## The join key, and the failure it prevents

`hook_key(song, hook)` → `"scratch/song01.mp3@20.0-25.0"`, which **must** match
`outcome_loop`'s hook grouper exactly. A test pins the literal string.

If those two drift, the evidence for a window attaches to nothing, `bias_map` returns `{}`
forever, and **the rule silently never fires with no error anywhere**. That is the most likely
way this breaks in six months, so it is a test rather than a comment.

`bias_map()` imports `outcome_loop` lazily and returns `{}` if it is unavailable — the song
library keeps working standalone, and there is no import cycle.

---

## The honest floor — where you will read it

**25 outcomes per window clears only a LARGE effect (Cohen's d = 0.8).** That is in
`outcome_loop.MIN_N_PER_ARM` with the derivation, and it is referenced from `pick()`'s
docstring:

> *at the honest floor this rule correctly never fires until dozens of videos are posted, and
> that is the intended behaviour rather than a failure.*

| effect | per arm | two-arm question | four-arm (hook windows) |
|---|---:|---:|---:|
| large (d=0.8) | 25 | **50 posts** | **100 posts** |
| medium (d=0.5) | 64 | 128 posts | 256 posts |
| small (d=0.3) | 178 | 356 posts | — not worth powering |

**On today's data — zero posted videos — `bias_map()` returns `{}` and rotation is exactly what
MEMEBOT-008 shipped.** Nothing about this round changes behaviour until real outcomes exist.

---

## Verification

| check | result |
|---|---|
| `tests/run_all.py` | **61 of 62 suites green** — see below |
| `tests/test_song_library.py` | **PASS — 69 checks** (was 55; +10 tests) |
| below the bars | shares **identical** to unbiased |
| above the bars | **exactly 2.00×**, all windows sampled |
| absurd 50× weight | still samples every window |
| sub-1.0 weight | clamped to 1.0 — never a demotion |
| worse window | refused, keeps 20% of rotation |
| determinism | **identical sequence**, two fresh loads |
| plan self-reports | `biased`/`bias_weight`/`bias_n`/`bias_reason` on every plan |
| `hook_key` ↔ outcome grouper | pinned to the literal string |
| campaigns SHA | **8e02f8d6f6307ae8 — MATCH** |
| `config.json` | parses, 162 keys, untouched |
| `outcome_loop.py` | **not modified** |

### The one red suite is not mine

`test_filelock.py` failed in the batch run and **passes standalone**:

```
$ python tests/test_filelock.py
Ran 4 tests in 34.073s
OK                                  exit=0
```

`clippershq/filelock.py` and `tests/test_filelock.py` are both **unmodified** — `git status`
shows nothing for either. It is a CROSS-PROCESS lock-contention test, and it ran while **10
other rounds were writing to this repo**, competing for the same locks; it took 14.8 s in the
batch against 34 s alone. That is the test doing its job under real concurrency, not a
regression from this round — but it is a real failure in that run and I am not going to call
the suite green.

---

## Limits

- **All bias evidence in the proofs is synthetic.** The n=30 windows are generated, not posted.
  Nothing here demonstrates the rule on real outcomes, because there are none.
- **The 2× ratio was measured over 60 picks in steady state from zero uses.** A store with
  lopsided existing counters converges to 2× rather than starting there.
- **`bias_map` recomputes from the whole outcome history on every call.** Fine at hundreds of
  records; it is an O(windows²) pooled-rest comparison and would want caching in the thousands.
- **The 2× weight itself is a judgement, not a measurement.** It is the value MEMEBOT-013
  proposed and this round wired; nothing has tested whether 1.5× or 3× would learn faster.
- **`bias` must be passed by the caller.** `pick()` and `render_plan()` default to `bias=None`,
  so a caller that forgets it silently gets plain rotation. That is the safe default, but it is
  a default — no renderer currently passes one.
- **Nothing calls `bias_map()` in production yet.** The wiring is inside the song library; the
  renderer that would supply `runs.jsonl` is MEMEBOT-007's path.

---

## Method

Filed a claim (10 rounds in flight, no path conflicts). Read MEMEBOT-013 for the agreed rule,
then wired it without touching `outcome_loop` — `should_bias` remains the single owner of both
bars, so there is no second copy of the statistics to drift. The proof builds synthetic
`runs.jsonl` files at n=8 (below the bar), n=30 with a real winner, and n=30 with a real loser,
runs each through the shipping `bias_map` → `pick` path, and measures the resulting shares over
60 picks. Determinism was checked by running 24 picks against two independently constructed
stores. No API call, no spend.
