# INFRA-001 — You were right: only the menu blocked it, and **headless already shipped while this brief was being written**. The real ceiling is not the API limits — it is 0.5 GB of free RAM against 173 MB of master per process. Railway: **no**.

**Date:** 2026-08-01 · **Type:** Research, READ-ONLY · **Spend:** $0.00 · **Paid calls:** 0
Primary sources verified for MusicBrainz and Railway. Findings saved incrementally to
`scratch/infra001/`.

**Honesty tiers used throughout: VERIFIED** (I read the code or the vendor's own doc) ·
**MEASURED** (I ran it on this box) · **DERIVED** (arithmetic on verified inputs) ·
**GAP** (not established).

---

## Before anything else: two of the three parts are already done

| this brief | status |
|---|---|
| Part 1 §2 (spec headless) + §3 (contention) | **INFRA-002 — in flight RIGHT NOW**, 4.6 min old when I checked. `clippershq/run.py` is already **committed**. |
| Part 2 §6–8 (dashboard) | **INFRA-003 — already PUBLISHED**, six panels, a working mockup, 11–14 h estimate |
| Part 3 §9–12 (Railway) | **genuinely undone** |

`clippershq/run.py`'s own docstring names the round that measured what §3 asks me to measure:

> *"INFRA-002 measured spend.json, the caches and run.log under two concurrent processes."*

My claim was filed 2 minutes before INFRA-002's. **The claim file surfaced the overlap; it did
not prevent it**, because neither of us was writing the same *file* — INFRA-002 writes
`run.py`, I write nothing. Path-level conflict detection cannot see two rounds researching the
same question. That is a real limit of the mechanism, worth knowing.

So below: Part 1 is **what I verified independently** (it agrees), Part 2 defers to INFRA-003
with two additions, and Part 3 is the work.

---

## PART 1 — parallel runs

### 1. What actually blocks it — **only the menu. VERIFIED.**

Your belief is correct, and the code makes it unusually clean:

```python
_find_twitch (config, config_path, confirm_fn=None, run_fn=None, categories=None)
_find_spotify(config, config_path, confirm_fn=None, run_fn=None, seeds=None)
_find_app_devs(config, config_path, confirm_fn=None, run_fn=None, terms=None)
_find_youtube(config, config_path, confirm_fn=None)
_find_crawl  (config, config_path)                      <-- NO confirm_fn
```

Four of five already take an injection point, with the pattern
`interactive = confirm_fn is None` and
`_confirm = confirm_fn or (lambda: _ask_yes_no("Proceed?", …))`. **Each funnel body contains
exactly ONE interactive call** — the Proceed gate. Nothing else asks.

`_find_crawl` is the only one without the parameter. That is the entire gap.

### 2. Headless — **already built, so the spec is moot**

`clippershq/run.py` ships today:

```
python -m clippershq.run --funnel spotify --target 700 --cap 0.50
python -m clippershq.run --list | --status
```

Its safety model is the part worth repeating: **`--funnel` without `--cap` refuses to start** —
not a default, an exit — because "a default cap is a number nobody chose". `--cap 0` is legal
only with `--free-only`. The six `_ask_*` helpers are replaced with functions returning the
*current* value (what pressing Enter does), and **any ask with no current value raises**, so a
headless run cannot silently guess.

**Time to build: zero. It exists.** The remaining work is `_find_crawl`'s missing parameter.

### 3. Where they genuinely contend — **VERIFIED per file, evidence below**

| file | mechanism | verdict |
|---|---|---|
| `master_leads.csv` | `filelock` + read **inside** the lock + temp→fsync→`os.replace` | **SAFE** |
| `spend.json` | `main.py:311` `with filelock.file_lock(path)` wrapping load→add→write | **SAFE** |
| `resolve_cache` | `resolve_cache.py:135` lock + **merge** + `os.replace` | **SAFE — merges, never clobbers** |
| `caption_seen` | `caption_finder.py:314` lock + `os.replace` | **SAFE** |
| **`clip_seen.json`** | `clip_runner.py:163` `os.replace`, **no lock** | **UNSAFE — last writer wins** |
| `run.log` | `_SafeRotatingFileHandler` | **DEGRADES, not fatal** |

**On spend.json specifically, since you asked whether the 25-call flush is safe:** yes, and the
reason is that the meter does not write the file. `IncrementalMeter.flush()` calls
`record_aux_spend`, which takes the lock and **re-reads inside it**, so two flushing processes
each add their own dollars. The docstring states the intent outright: *"Reading INSIDE the lock
makes the in-memory copy fresh, so two concurrent runs each add their own dollars instead of the
second clobbering the first (lost-update)."* The flush interval is irrelevant to correctness —
it only changes how much metering a crash loses.

**`clip_seen.json` is the one real hole**, and it is benign by design: its own docstring says
*"losing the cache costs re-processing, not correctness."* Two clip runs would each drop the
other's entries and re-walk some clips — money, not corruption. Worth a lock; not a blocker.

**`run.log`**: `_SafeRotatingFileHandler`'s docstring names the exact scenario —
*"the sync client (or a second running process) can hold run.log open, so os.rename() during
rollover raises PermissionError"* — and swallows it, letting the file grow past `maxBytes`.
Known, mitigated, cosmetic.

### 4. API limits — **the MusicBrainz problem is worse than you thought**

**VERIFIED against musicbrainz.org's own rate-limiting doc:** *"allow through (on average)
**1 request per second**"* **per IP address**, declining the rest with **HTTP 503**. (Per
user-agent 50/s, global 300/s — neither binds here.)

**Our limiter is process-local.** `musicbrainz.py:194` holds `state = {"next_at": …}` in a
closure guarded by `threading.Lock()`, with `MIN_INTERVAL = 1.1`. That is correct across
threads and **invisible across processes**. Two Spotify runs in two terminals = **~1.8 req/s
from one IP** → 503s, and the retry logic then absorbs them as latency.

**So the answer to "would two funnels throttle each other" splits by vendor:**

| vendor | shared limiter? | two funnels interfere? |
|---|---|---|
| **MusicBrainz** | process-local, **1/s per IP** | **YES — do not run two Spotify funnels at once** |
| HikerAPI | `polite_delay_ms: 50`, per-process | **GAP** — no published RPS found; config has no rate key |
| LamaTok | `polite_delay_ms: 150`, per-process | **GAP** — same |
| TikHub | `tikhub_api: {}` — **no timeout, no delay, no retries configured** | **GAP**, and the empty config is itself worth noting |

**GAP, stated plainly:** I did not verify HikerAPI/LamaTok/TikHub published limits against
their docs. Their per-process politeness delays double when you double the processes, exactly
as MusicBrainz does. **The safe reading is that any two funnels sharing a vendor halve that
vendor's politeness margin**, and only MusicBrainz is confirmed to have a hard ceiling.

Your 1.02× figure for concurrency 6 vs 3 on Spotify follows directly: when a global 1/s
limiter is the bottleneck, in-process concurrency buys nothing. **That logic applies across
processes too, which is why two Spotify runs is the one combination to avoid.**

### 5. How many can run at once — **MEASURED, and RAM is the binding constraint**

| | brief assumed | **measured now** |
|---|---|---|
| free RAM | 2.6 GB | **0.5 GB** |
| cores | 12 | 12 ✓ |
| disk free | 95 GB | 97 GB ✓ |

**`master_leads.csv` costs 173 MB of Python heap per process** — 58,470 rows, 7.1× the 24.5 MB
file (tracemalloc, measured). Add interpreter and working set and a funnel is **~250–300 MB**.

Currently running Python: 3 processes, **29 MB total** — so the 0.5 GB shortfall is other
software, not this project.

**DERIVED verdict:**

| concurrent funnels | RAM needed | fits 0.5 GB free? | fits if you close other apps? |
|---|---:|---|---|
| 1 | ~300 MB | no (marginal) | yes |
| **2** | **~600 MB** | **no — swaps** | **yes, comfortably** |
| 3 | ~900 MB | no | yes |
| 4+ | ~1.2 GB+ | no | tight |

**Answer: 2–3, and only after freeing RAM.** CPU is not the limit (12 cores, and these funnels
are I/O-bound on API latency). Disk is not the limit. **The limit is that 0.5 GB of free RAM
does not fit one funnel, let alone three.** Close the browser first — that is a bigger lever
than any code change here.

**And regardless of RAM: never two Spotify runs** (§4).

---

## PART 2 — the dashboard: see INFRA-003

**INFRA-003 already specifies this** — six panels, one visible at a time, reading the same state
files the menus read, **11–14 hours, zero funnel changes**, with a working static mockup at
`scratch/infra003_mockup.html` and an accessibility section. I am not going to re-spec it.

**Two things I verified that reinforce it:**

**§8 — what exists today is more than the brief assumed.** `clippershq/run_status.py` was
purpose-built for this. Its docstring says so:

> *"This is the LIVE view: what is running right now, how far in, how much spent. **A dashboard
> polls this**; nothing polls a completion marker."*

with a declared shape — `run_id, funnel, status, started, updated, elapsed_s, pid, target,
cap_usd, progress, leads, spend_usd, note` — atomic-replaced on every update so it is safe to
read mid-run, and **one file per run so two funnels never contend**. `list_runs()` reads the
directory; there is no registry to lock.

Available with **no new instrumentation**: live runs + progress (`run_status.list_runs()`),
**128 historical runs** with per-run campaign/calls/dollars (`spend.json:runs[]`), lifetime
totals split by vendor (`total_spent_usd`, `ig_spent_usd`, `tiktok_spent_usd`,
`tikhub_spent_usd`, `link_spent_usd`), the output spreadsheets (`output/`), and detail
(`logs/run.log`). **Everything panel 1–5 needs already exists.**

**On Flask vs FastAPI:** for a localhost page polling JSON files, the honest answer is that the
framework does not matter — neither is doing anything the other cannot. Pick Flask for fewer
moving parts (no ASGI server, no async), unless you want the free OpenAPI page, in which case
FastAPI. **This is not a decision worth research time.**

---

## PART 3 — Railway

### 9. Would it run there? **Technically yes, but not the way you use it.**

**VERIFIED from Railway's own docs**, Hobby plan:

| | |
|---|---|
| price | **$5/month, including $5 of usage** |
| RAM / vCPU per service | 48 GB / 48 vCPU (not a constraint) |
| ephemeral disk | 100 GB — **lost on every deploy** |
| **volume storage** | **5 GB**, **one volume per service**, 10 volumes per project |
| egress | **$0.05/GB** |
| usage rates | **$10/GB RAM/month**, **$20/vCPU/month** |
| replicas + volumes | **"Replicas cannot be used with volumes"** |

**The three hard parts, against those numbers:**

1. **`master_leads.csv` at 24 MB, mutated constantly.** Fits a 5 GB volume 200× over. **Not a
   problem** — but it must be *on the volume*, not the ephemeral filesystem, or every deploy
   wipes it. And "one volume per service" plus "no replicas with volumes" means **one writer
   service, ever**. The parallel-run goal from Part 1 becomes harder there, not easier.
2. **memebot's ffmpeg encoding.** 48 vCPU available; CPU is fine. **The 3.6 GB tree does not
   fit a 5 GB volume alongside anything else**, and 3.4 GB of it is the TikTok corpus that
   should never be uploaded anyway. Source-only is ~10 MB and fits trivially.
3. **Clip retrieval downloading MP4s.** This is where it bites: **egress is billed at
   $0.05/GB**, and BL-787 measured 8.5 MB per clip at best quality. Ingress is normally free,
   but every clip you *serve back* to yourself costs.

**GAP: whether Hobby services sleep.** Railway's free-trial page documents the trial reverting
to a $1/month Free plan but does not state sleep behaviour for Hobby, and I did not find an
authoritative statement. Do not assume always-on.

### 10. Cost at your usage, and the CSV→DB question

**DERIVED from the verified rates.** Funnels are bursty, not 24/7:

| scenario | RAM×time | monthly resource cost |
|---|---|---|
| 1 service, 512 MB, 2 h/day | 0.5 GB × 60 h | **~$0.41** |
| + dashboard always-on, 256 MB | 0.25 GB × 730 h | **~$2.50** |
| + 1 vCPU during those 60 h | | **~$1.64** |
| **total resources** | | **~$4.55** |
| **plus** egress, 500 clips × 8.5 MB = 4.25 GB | | **+$0.21** |

**≈ $5–6/month, i.e. inside or barely over the $5 credit.** Cost is **not** the reason to say no.

**The CSV→database question — MEASURED:**

```
write sites : 51 occurrences across 8 modules
              (all funnels route through append_found_to_master / crossdedup.append_leads)
read sites  : 250 occurrences across 27 modules
```

**The writes are already funnelled — 8 modules, one choke point.** The reads are not: **250
references across 27 modules**, and they are scattered exactly as you suspected — every
exporter, every audit, every scratch script opens the CSV directly with `csv.DictReader`.

**So a DB migration is not "rewrite `append_found_to_master`". It is 250 call sites**, or a
compatibility shim that presents a `DictReader`-shaped iterator over SQL — which is the only
sane path, and which buys you nothing on a 24 MB file that already loads in 173 MB.

**Verdict: the CSV is not the problem, and moving to a database to enable hosting would be the
tail wagging the dog.**

### 11. Local vs hosted, on the axis that matters

**"Running while my PC is off" is the only axis where hosted wins**, and it is worth being
precise about what it would cost:

| | local | Railway |
|---|---|---|
| runs while PC off | **no** | yes |
| parallel funnels | 2–3 (RAM) | **1 writer** (one volume, no replicas) |
| master safety | filelock + atomic, proven | same code, one writer only |
| memebot 3.6 GB | already there | does not fit a 5 GB volume |
| clip MP4s | free, local disk | $0.05/GB egress |
| cost | £0 | ~$5–6/month |
| failure mode | you see it | you find out later |

**The middle path you suggested is the right one, and it is better than both:**

**Keep everything local; run the funnels on a Windows Scheduled Task.** `clippershq/run.py`
already makes this a one-liner —
`python -m clippershq.run --funnel spotify --target 700 --cap 0.50` — with a mandatory cap as
the safety model. A scheduled task at 3 a.m. runs while you sleep, on the machine that already
holds the data, with no egress, no volume limit, and no migration.

**It does not run while the PC is *off*.** It runs while you are not *using* it, which is the
actual need behind the question. If the PC must be off, the answer is not Railway — it is a
machine that stays on.

**Hosting only the dashboard** is worse than it sounds: the dashboard's entire value is reading
`spend.json`, `run_status/` and `output/` — all local. Hosting it means syncing those files out,
which is more moving parts than the dashboard itself.

### 12. Recommendation

**Do not use Railway. Run headless funnels on a Windows Scheduled Task, and keep the dashboard
local.**

- `clippershq/run.py` already exists, with the cap gate as its safety model
- no migration, no egress, no 5 GB ceiling, no second copy of a 24 MB file that mutates
- the 250 read sites never have to move
- ~$5–6/month saved, and more importantly no split-brain between two copies of master

**Trigger to revisit — any ONE of these:**

1. **You need runs while the machine is genuinely off** (travel, or the PC becomes someone
   else's). Scheduled tasks cannot help; a small always-on box or a VPS can.
2. **Master exceeds ~500 MB** (currently 24 MB, ~20× headroom). At that size the 173 MB/process
   load becomes 3.5 GB and both local parallelism *and* a 5 GB volume fail together — that is
   the moment the DB question becomes real, independent of hosting.
3. **A second person needs to run funnels.** One volume and one writer stops being a limitation
   and starts being a requirement, and shared state has to leave this laptop.

---

## Limits

- **HikerAPI, LamaTok and TikHub rate limits are a GAP.** I verified MusicBrainz against its own
  doc and read our configured politeness delays; I did not find or check the three vendors'
  published limits. §4's per-vendor table says so.
- **Railway's Hobby sleep behaviour is a GAP** — not stated in the pages I read.
- **The $5–6/month figure is DERIVED**, not observed. It assumes 2 h/day of funnel time and a
  256 MB always-on dashboard; a different duty cycle moves it linearly.
- **The 173 MB/process figure is one measurement** of a full `list(DictReader(...))`. A funnel
  that streams rather than materialises would use less; none of them currently do.
- **I did not test two funnels running concurrently.** INFRA-002 is doing exactly that, live.
  My §3 verdicts are read from the locking code, not from an observed race.
- **§5's concurrency table is arithmetic on one measured process size**, not a load test.
- **Part 2 defers to INFRA-003**, which I read but did not re-verify.

---

## Method

Filed a claim, then read the funnel entry signatures, `filelock`, `crossdedup.append_leads`,
`main.record_aux_spend`, `spend_ledger.IncrementalMeter`, `resolve_cache.save`, both
`save_seen` implementations, `_SafeRotatingFileHandler` and `musicbrainz.make_country_fn`
directly — every §3 verdict cites the file and line that justifies it. Machine figures from
`Win32_OperatingSystem`/`Win32_LogicalDisk`; the 173 MB figure from `tracemalloc` around a full
master load. MusicBrainz and Railway figures fetched from the vendors' own documentation and
quoted. Read/write site counts by `grep -rn` over `clippershq/` and `tools/`, excluding tests.
Findings written incrementally to `scratch/infra001/part1_findings.md`. No code was modified, no
API call was made, nothing was spent.
