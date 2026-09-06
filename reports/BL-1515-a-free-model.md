# BL-1515 — A free model that is good enough, proved on his own grades

**Round:** BL-1515 · **Date:** 2026-09-06 · **Spend:** $0.041 (model census) + $0.008 (paired
scoring) = **$0.049 of a $1.50 cap**, counted by each run's own counter at the wrapper. The
360-page local evaluation and the 200-call free-model run cost **$0.00**.

---

## Is there a free model good enough, what does it cost, and what does it cost in accuracy

**Yes. `minimax/minimax-m3:free` costs $0.00 per 1,000 pages against the shipped judge's
$0.1054, and on his own grades it is not worse — it is slightly better.** Paired on the same 80
pages, same brief, same pictures, only the model changing: it answered **58 of 80** against the
paid model's 49, failed to parse on **27.5%** against **38.75%**, ran at a **3.13 s** median
against 3.78 s, and killed **0 of 38** of his wanted pages against the paid model's 0 of 35.
**The accuracy cost is not measurable at this sample size; the price cost is 100%.** Two things
stop this being a one-line change, and both are measured below: the chain converts an unscored
model's REJECT into a KEEP, so promoting it without cutting authority would make the judge free
*and stop it rejecting anything*; and above roughly half a call per second the free lane refuses
**59.5%** of requests outright. **The free model is real. The free lane is rate-bounded, and the
authority question needs 60 wanted pages, not 38.**

---

## 1. Every image-capable model, verified by a live call

A catalogue listing is not evidence — one model was named in the shipped chain, looked valid,
and returned 404 on 198 of 198 calls while being absent from the catalogue entirely. So every
candidate here was called with the **production payload**: `_messages(sheet, tt_exemplar_pack(),
platform="tiktok")` — 8 exemplars plus a real 465×992 sheet, 9 images, 244,337 bytes.

**The catalogue: 431 models, 262 declare image input, and exactly 11 of those are priced 0/0.**

| model | price | verdict | n | median | ≤45 s | blank/torn |
|---|---|---|---:|---:|---:|---:|
| **minimax/minimax-m3:free** | **$0.00 measured** | **ALIVE** | 9 | **2.56 s** | 9/9 | 0/9 |
| dots-studio/dots-3-note-preview:free | $0.00 | ALIVE | 9 | 21.98 s | 8/9 | 1/9 |
| nex-agi/nex-n2-mini | $0.0001054/call | ALIVE | 3 | 4.55 s | 3/3 | 0/3 |
| z-ai/glm-5.3-flash | $0.000208–0.000354 | ALIVE | 3 | 20.05 s | 3/3 | 0/3 |
| nvidia/nemotron…:free | $0.00 | **OVER CLOCK** | 3 | **371.76 s** | **0/3** | 2/3 |
| google/gemma-4-26b, gemma-4-31b:free | $0.00 | **429 — LIVE, refusing** | 3 ea | — | 0/3 | — |
| stealth/ox-alpha | — | **404** | 1 | — | 0/1 | — |

**The dead stealth model's 404 body disclosed its own successor, verbatim:** *"This model was
ZAI's GLM-5.3 Flash."* The repo had already guessed that; this is the first time the disclosure
itself was read.

### Two price corrections, from measured `usage.cost` rather than catalogue text

- ⚠️ **`PAID_FALLBACK_USD_PER_1000 = 0.0890` is 18.4% low.** The shipped judge measures
  **$0.1054 per 1,000 pages**. Every cost figure in this project that used the constant is low
  by that margin.
- ⚠️ **`google/lyria-3-clip-preview` billed $0.04 on ONE call while the catalogue lists prompt 0
  and completion 0.** The module's own warning — *"`pricing.prompt == 0` IS NOT A TEST FOR
  FREE"* — is now a measurement rather than a caution. That single call was 97% of the census
  spend and **40,000× his price bar**.

### His six-zero bar is unreachable by any priced model

He asked for about **$0.000001 per call**. The cheapest vision model in the catalogue prices
prompt tokens at $2.5e-8; at ~2,500 prompt tokens that is **$0.0000628 before a single
completion token — 62× his bar**, and 105× measured. **Only a $0.00 model can meet six zeros.**

### Privacy, tested rather than asserted

The provider documents a per-request routing flag: `"deny"` = *"use only providers which do not
collect user data"*. **The negative control passed**, which is what makes a successful route
evidence: two other free models returned `404 "No endpoints found matching your data policy
(Free model training)"`. Under the same flag, **minimax-m3:free, dots-3-note-preview:free and
nex-n2-mini all routed and answered** — they are not in the training class.

⚠️ **Human review: NOT FOUND.** No reachable published text from the router or either provider
states whether human reviewers see submissions. **That is an absence of a statement, not a
guarantee**, and the earlier refusal of a free tier that *did* disclose human review with no
opt-out stands untouched.

---

## 2. Scored paired on his own grades

**The test set is 457 of his graded pages** (160 he scored 8–10, 207 he scored 1–3), grid on
disk, **pages he supplied excluded** — they are positive by construction, and on an all-positive
pool "says yes more" and "is right more" are the same thing. They belong in the prompt as
worked examples, which is where they are.

**The constant-answer baseline is not one number**, so each is quoted with its scope:

| scope | n | always-REJECT |
|---|---:|---:|
| all scored pages | 457 | 65.0% |
| the decidable 8–10 vs 1–3 pool | 367 | **56.4%** |
| TikTok only | 220 | 54.5% |
| Instagram only | 237 | 74.7% |

The 56.4% reproduces one of the four figures on record, which identifies the pool it came from.

### The paired result — same 80 pages, same brief, same pictures

| | `minimax:free` | `nex-n2-mini` (paid) |
|---|---:|---:|
| answered | **58 / 80** | 49 / 80 |
| blank or torn | **27.5%** | 38.75% |
| latency median | **3.13 s** | 3.78 s |
| latency p90 | **5.19 s** | 14.28 s |
| answered within 45 s | 100% | 100% |
| **kills of his wanted pages** | **0 of 38** | 0 of 35 |
| kill rate, Wilson 95% upper | **≤ 9.2%** | ≤ 9.9% |
| catches of his 1–3s | 9 / 20 (45.0%) | 7 / 14 (50.0%) |
| **price per 1,000** | **$0.00** | **$0.1054** |

**Blank and torn are counted as a failure mode with a denominator, never as a missing
datapoint** — and on that axis the free model is the better one.

⚠️ **Nothing here can exceed his own consistency.** He agrees with himself 75.6% overall and
**48.0% [30.0, 66.5] near his decision line** — an interval spanning 50%. So the 95% bar is
placed on kills of wanted pages, which is the number that costs him something real, and not on
accuracy.

---

## 3. ⚠️ The free lane is rate-bounded, and that is the finding that decides deployment

Running the same free model at roughly twice the rate changed it completely:

| | ~0.5 calls/s (n=80) | ~1 call/s (n=200) |
|---|---:|---:|
| answered | **72.5%** | **14.0%** |
| HTTP refusal (rate limit) | **0%** | **59.5%** |
| torn / blank response | 27.5% | 26.5% |
| latency when it answered | 3.13 s | 3.04 s |
| latency when it failed | — | **0.45 s** |

**Two separate failure modes, and only one is throttling.** The HTTP refusal is purely
rate-driven — 0% at the slower rate, 59.5% at the faster. The torn-response rate is
**rate-independent at ~27%**, so it is a property of the model, not of the lane. And failing
**8× faster than answering** (0.45 s against 3.04 s) is the signature of a refusal, not a
timeout.

**What that means in production:** the free model is usable at a bounded rate, and its
abstentions cost nothing — an abstention keeps the page, exactly as a torn answer does. It is
not a drop-in replacement for a paid lane running at 235 calls/min.

---

## 4. The local option, and why I refuse it

`clippershq/siglip_probe.py` looked like the answer: on disk, no network, $0.00, already
imported by `judge_batches.py` which `meme_finder.py:6560` imports, and reporting **held-out AUC
0.9695** on his own marks. **I scored it on 360 pages it has never seen — every page it was
fitted or tested on excluded — and it does not survive.**

| | published (its own held-out 100) | **measured, 360 unseen pages** |
|---|---|---|
| AUC | 0.9695 | **0.7420** |
| kills at its own recommended threshold 0.11 | 0 of 9 | **82 of 149 (55.0%)** |
| Wilson 95% upper on those kills | 29.9% | **62.8%** |

At **every** threshold from 0.02 to 0.50 it kills between 74 and 98 of his 149 wanted pages.
**The module's own docstring predicted this** — *"THE THRESHOLD IS NOT PORTABLE ACROSS
CAPTURES"* — because it was fitted on 934×934 square grids and this corpus is mixed geometry.
But the AUC is rank-based and scale-free, so a fall from 0.9695 to 0.7420 is a **generalisation
gap, not a threshold artefact**. Its published number is true of one capture geometry and does
not transfer to the corpus that actually exists.

**And the lead three rounds have been carrying is gone.** "He already owns a 2–4B VLM in GGUF,
already downloaded" — a full drive walk found **zero `.gguf` files anywhere**; the model cache
shrank from 34.70 GiB to 4.5 GB, almost certainly in the disk-reclaim rounds. What remains is
three *contrastive encoders* and three *text-only* Ollama models (proven structurally: no
projector layer in any manifest). **Generative vision models on disk: 0.** CUDA is impossible
here, confirmed four ways.

---

## 5. What shipped, and what did not

### Shipped — the cap hole, closed at the chokepoint · **GENERAL**

⚠️ **The judge consulted no cap on any path.** By AST over the whole module,
`effective_run_cap`, `max_run_usd`, `finder_common`, `reserve` and `cap` appear **nowhere** in
`free_judge.py`. Driven end to end: `effective_run_cap` returned **$0.00** for the run and the
judge then made **501 bookings, 0 refusals, $0.133589 written.**

The fix filters the ask order **before the loop**, not by raising inside it — because the loop
treats an exception as "that model is dead" and **moves to the next model**, so a ceiling
enforced by raising would have been answered by spending on the model after it.

Driven both directions: at a $0.0001 budget it refuses the expensive model and keeps the
cheaper one **and every free link**; at $10 it keeps all five. With a **$0.00** budget the chain
degrades to free-only, the free model says REJECT at 95, and **the page is KEPT** — an exhausted
budget cannot produce a rejection.

⚠️ **My first version of this fix shipped fail-open and I caught it before committing.**
`resolve_run_budget` returns a **dict of numbers**, not a budget object, so `.can_afford(...)`
raised `AttributeError` — which my own `except: ok = True` swallowed into "never bound on a
broken check". It reported *"kept 5, refused 0"* while binding nothing. **A fail-open that looks
like a pass, inside the fix for a fail-open.** The swallowing `except` is now gone.

### Shipped — the truncation that silently dropped a cutter · **GENERAL**

The free-first branch truncated the **whole** non-paid list to `FREE_TRIES`, so a model that
*may cut* could be dropped by a ceiling whose only purpose is limiting how long one page waits.
Driven: with `PAID_FIRST=False` it dropped `z-ai/glm-5.3-flash`, a cutting model, and
`test_bl1468::test_every_model_that_may_reject_is_actually_asked` went red — the guard working.
It now mirrors the branch above: **scored links survive whatever `FREE_TRIES` says; only
unscored ones are bounded.**

### NOT shipped — the free model is not yet allowed to cut, and here is why

⚠️ **The obvious change is a trap.** `should_reject`'s loop **stops at the first parseable
verdict**, and an unscored model's REJECT is **converted to a KEEP** (`free_judge.py:1776`).
Putting a free unscored model first would make the judge free **and silently stop it rejecting
anything** — the ~30.5% of Instagram pages the free judge rejects today would become keeps, and
every one would flow on to the paid profile call.

So the free model needs **scored cutting authority** in `MAY_REJECT`, which today holds exactly
`z-ai/glm-5.3-flash @ 90` and `nex-agi/nex-n2-mini @ 90`. The incumbent earned its place with
**0 of 60** wanted pages killed. **minimax has 0 of 38.** That is the same answer, on a smaller
sample, and the honest position is that it is not yet the same evidence. **The remaining work is
one free run over ~60 wanted pages at a bounded rate** — no new capability, no spend.

⚠️ **And a rename would break it silently.** A low-effort setting is gated on the old model's
*name* appearing in the string (`free_judge.py:1231`), so a promoted free model would inherit —
or lose — determinism by accident of spelling.

---

## 6. Corrections, and one instrument that lied to me

- **I reported a test as failing that passes.** `test_bl1418_gate_standdown_and_order.py` came
  back red once through the runner, then green standalone (14 tests) and green through the
  runner (14 checks). It is a ~350-second network-dependent suite and that red was a flake. I
  should have re-run before reporting it.
- **A sub-agent's "VIABLE" verdict on the local probe was wrong, and I only found that by
  measuring it myself.** Its verdict rested on the module's *published* AUC; mine is 360 fresh
  pages. Mine supersedes.
- **A sub-agent corrected itself before I published**: an AST census of 2,860 files was
  re-derived as **2,863** — the delta being exactly three test files a peer round added
  mid-session — one line number was off by one, and one claim it could not reproduce was
  withdrawn rather than restated. It also recorded that it had cited a delegated figure before
  confirming the delegation returned.
- **`clippershq/filelock.py` shadows the `filelock` package.** Putting `clippershq` first on
  `sys.path` made `huggingface_hub` fail and the encoder report a missing package **while its
  weights sat on disk**. The error named neither the real cause nor the real file.
- **`grep -c` counts lines, not occurrences.** A peer and I got 9 and 10 for the same file and
  the same word. If a count is evidence, its unit has to be stated.
- **One zero discarded.** A sub-agent's per-endpoint `data_policy.training` read `None` on all
  30 endpoints — because **the field does not exist on that response**. No control could produce
  a non-zero, so the reading measured the instrument. Discarded and replaced with the routing
  test that has a passing negative control.

---

## 7. What is still open

- **`reject_at` is a dead parameter on the `should_reject` path** — accepted at the signature,
  never read in the body; `classify` does read it. Cut decisions are byte-identical across
  `reject_at` 70/80/95/100. **90 cuts, 89 never does.** A future round tuning `reject_at` and
  believing it moved the spend gate would be wrong.
- **The interactive menu never preflights.** `control.py` has zero `run_preflight` call sites;
  `run.py:542` has the only production one. And `run_preflight(network=False)` returns
  **ok=True** with `gate_armed` at WARN — green while nothing has confirmed a cutter answers.
  For it to fail rather than warn, `check_gate_armed` must treat "nobody looked" as FAIL.
- **Two shipped test stubs are stale** (`test_bl1468` at :79 and :121):
  `lambda n=1, spend_path=None: True` predates `_book_paid_call` gaining `model=`, so they raise
  `TypeError`, which the chain converts into "a dead model" — **knocking both cutters out of the
  chain in those tests**. Fix before writing any re-pin, or the re-pin measures the wrong chain.
- **The rubber stamp to refuse**, recorded so nobody writes it: `asked[0] == FALLBACK_CHAIN[0]`
  is green on **both** forbidden variants, because it reads the same literal the code reads.

---

## 8. Test state and controls

`bl1418` **14 checks green**, `bl1468` **15 green**, `bl1414` **10 green** — the three suites
that pin the chain order, the judge's liveness, and the only-scored-models-may-cut invariant.

Every zero in this report carries a positive control on the same path, and the two that failed
their control were discarded and are named in §6. The scoring harness was proved before it
spent: its call ceiling fires at exactly the configured count, raising a `BaseException`
subclass so the chain's `except Exception:` cannot swallow it and retry on another model; its
wall-clock stop routes through the **same** exception so a killed run still writes its artefact;
and torn responses are counted as failures, never as keeps and never as rejections.

Backups sha256-verified with a corruption control that fires on one flipped bit. Seen stores
verified by **row key sets with the body found by shape** — `spend.json` is a list at `runs` and
`clip_seen.json` is a list at its root, the two a dict-only helper once read as 0 and 8.

---

*Every number here can be re-run from `scratch/bl1515_*`: the model census, the paired scoring
harness, the 360-page local evaluation, and the chain-hazard audit.*
