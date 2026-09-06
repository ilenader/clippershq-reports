# BL-1514 — The camera can take a proxy. The free ones forge certificates, and the wall was never a counter.

**Round:** BL-1514 · **Date:** 2026-09-06 · **Spend: $0.00** — no vendor call by me or by any of
the four sub-agents. Production page loads spent: **20 of ~1,036 (1.9%)**, and the production IP
was left **clean** (verified 3/3 twelve-tile grids at the end).

---

## Can Instagram go faster, how much faster, and what does it cost?

**Mechanically, yes — and that half is now finished and shipped.** The camera's browser always
could take a proxy; nobody had ever passed one. It is wired now, at the only browser launch in
the project, and rotation turns out to be nearly free: **0.051 s to change the outbound IP
against a 2.4 s page load**, with no relaunch. **But the cheap version he proposed is dead.** Of
a 3,938-entry public proxy list, **114 were usable — 2.89%** — and of those that carried TLS to
Instagram, **91 of 91 presented forged certificates for the site**, minted the day before. **And
the number the whole plan rests on was never measured:** "1,036 page loads per IP" reproduces as
a count, but **"per IP" was never observed** — no experiment before this round ever varied the
IP. When we did, **7 of 18 IPs were refused on load #1 with zero budget consumed** while the
direct IP returned clean grids in the same minutes. **Entry is gated by IP reputation, not by a
counter**, which is a different mechanism with a different fix, and it is not the one "just
click the VPN" addresses. On cost, paid residential proxies **never** beat simply buying the
grid ($42–$335 per 1,000 against **$19.73**, and cost does not fall as you add IPs). On clock
they win, but only past a **step at 14 IPs** — and this machine runs out of RAM at about **12
browsers**. So: faster is possible, it costs more than buying the answer, and the first purchase
is hardware, not IPs.

---

## 1. Round ID, date, and what it was asked to do

BL-1514, 2026-09-06. Investigate the per-IP wall on the free Instagram camera, then fix it. Five
parts: prove the camera can take a proxy at all; measure free proxies honestly; ship an
automatic, general rotation; measure the already-proven free mirror; and re-derive the floor.

Four sub-agents ran in parallel. **The claim registry used was `.claims/`** — `docs/claims/` is
an archive and was verified to hold **0** files, so it could not have answered a question about
the present either way. Before editing the shared launch file I asked two peer sessions on the
pipe rather than inferring ownership; one replied that it holds an unrelated round in a
different repository, and the file was unclaimed. **The claim was ended when the round
finished.**

---

## 2. What actually shipped

**`clippershq/proxy_pool.py`** (new) and **one hunk in `clippershq/page_capture.py`**.

**It is general, and that is a structural fact rather than a promise.** An AST census of all
**274 production Python files** found **exactly one `.launch()`** — `page_capture.py:920` — and
`open_browser()` is the only way to obtain a browser (2 callers, both the Instagram funnel). A
proxy applied there **cannot be bypassed**, because there is no other path. That matters here:
of seven past fixes tested by driving them, only 1 of 7 was general, and 3 of the 6 local ones
were still failing.

**Three states, kept apart, because conflating two of them is the dangerous part:**

| state | behaviour |
|---|---|
| **no pool configured** | `acquire()` returns `None`; **no `proxy` kwarg is constructed**; byte-for-byte the launch that has always shipped |
| pool configured, an IP free | that IP is used |
| **pool configured, all burnt** | **raises `PoolExhausted`** |

**An exhausted pool must never fall back to the direct IP.** That would spend the one address
the funnel depends on and would look exactly like success. The exception is deliberately not
caught at the launch site, and the test suite drives both branches through the real
`open_browser` with a fake browser injected — so "no proxy kwarg when unconfigured" is
*observed*, not argued.

**The pool refuses to pretend to know things.** The per-IP budget defaults to **`None` = NOT
MEASURED**, not to 1,036, because that figure's "per IP" was never observed (§3.5). A missing
success rate is `None`, never `0.0` — "never tried" and "tried and failed every time" are
opposite facts. An unreadable state file **raises** rather than reading as empty, because
reading it as empty would clear every cooldown and immediately reuse burnt IPs. And endpoints
are treated as credentials: `stats()`, `__repr__` and every message emit a **hash**, never a
host — the exhausted-pool exception is asserted not to leak the endpoint.

**16 tests, all 16 executed and passing.**

---

## 3. What was measured

### 3.1 The camera always could take a proxy; nobody ever passed one

`proxy` appears **0 times** in `page_capture.py` — confirmed by three independent instruments
(line grep, occurrence count, AST identifier census). **The positive control fired**: `headless`
is non-zero on all three.

⚠️ **A unit correction worth generalising.** The published "`headless` appears twice" and my
"3" are the same file: **`grep -c` counts LINES, not occurrences**, and one line carries the
word twice. The same trap produced a 9-vs-10 disagreement with a peer session about `proxy` in
the same hour. **If a word count is used as evidence anywhere, it must say which unit it is in.**

Playwright 1.62.0 is what the camera drives, and signature introspection on the installed
version shows `launch`, `new_context` **and** `launch_persistent_context` all accept `proxy`.
The capability was always there. Repo-wide there was **zero** proxy plumbing: 0 of 173 config
keys and 0 environment variables.

**Free and load-bearing:** the camera persists **no cookie jar** — `storage_state`,
`user_data_dir`, `launch_persistent_context` and `add_cookies` are all **0** (control:
`new_context` = 1). Every launch is a fresh, empty profile.

### 3.2 The outbound IP really changes — proven, not assumed

A configuration that is accepted and silently ignored looks identical to one that works, so
this was proved three ways. The **shipped launch line, verbatim**, lands on the same response
fingerprint as plain `urllib` — control fired. Through proxies, **7 of 7** reads returned
exactly the address an *independent* probe had predicted for that endpoint; an ignored config
would have returned the direct fingerprint and never did. All were **on a different /8** from
direct, and **none shared a /24**. (Addresses are reported as shapes only — one of them is his
home IP.)

### 3.3 Rotation is nearly free, and needs no relaunch

Chromium was launched with **no proxy at all**, and then `new_context(proxy=…)` changed the IP
**3/3**. Mechanism cost, network removed, **n = 12 per arm**:

| | median | p90 | max |
|---|---:|---:|---:|
| per-context rotation | **0.051 s** | 0.053 s | 0.085 s |
| full relaunch | 0.168 s | 0.180 s | 0.247 s |

A relaunch is 3.3x dearer and **both are noise beside a ~2.4 s page load**. Re-derived with the
network in the loop: 2.07 s vs 2.61 s, same sign. **So rotation frequency is a free variable —
there is no reason to batch pages onto one IP**, which is what makes a per-page rotation policy
affordable.

### 3.4 ⚠️ The deciding test: what was established, and what was not

| arm | result |
|---|---|
| **direct** (production IP, n=3) | **3/3 clean 12-tile grids** — the production IP is clean today |
| **proxy** (n=20 loads, 18 distinct IPs, 12 distinct /8s) | **2 clean grids**, 7 hard login walls, 3 zero-tile, **8 discarded** |

The 8 discards are the honest part: they produced **no Instagram verdict at all** (transport
failure, control did not fire). Counting them as walls would have inflated the wall rate from
**58.3% to 75%**.

**Established:**

1. **The camera works end to end through a proxy** — two proxy IPs each returned a full 12-tile
   grid from the shipped capture path.
2. **The cooldown cannot be cookie- or profile-borne.** There is no jar, so the historical wall
   survived hundreds of fresh-profile launches. One of the three candidate carriers is
   eliminated outright.
3. **The IP alone flips the verdict** — same browser, same empty profile, same handle, same
   minutes.
4. **The wall is NOT solely a page-load counter.** Seven proxy IPs were walled on **load #1 with
   zero budget consumed**.

**NOT established, and not inferred:** whether a fresh IP **resets** the ~1,036-load budget.
Answering it requires burning ~1,036 loads on one IP and then rotating. The only IP available to
burn is production — forbidden while three other rounds depend on the camera — and free proxies
cannot carry it (12.7 s median per page and ~19% blocked on arrival leave no clean runway).
**That question still decides the economics, and it is open.**

### 3.5 Two published figures that do not survive contact

**"1,036 loads per IP."** The 1,036 is real. **"Per IP" was never observed** — no experiment in
any prior round varied the IP; every figure came from one IP and one browser. **The denominator
was never measured**, so every plan built on "budget per IP" inherits an assumption nothing
tested. Independently, the free-proxy arm found the budget is **not a constant either**: three
IPs were cut off at **20, 96 and 114** loads while **twelve passed 600+ untouched and two beat
1,036 outright (1,300 and 1,086)**. A prior round had already measured **80 loads at a faster
pace** — a 13x range. It is **rate-dependent and reputation-dependent**, not a fixed allowance.

**"At least 8.26 hours dark."** A lower bound from a **single** episode in which recovery was
never observed. Recovery has plainly happened since — clean captures today. It remains the only
number available, so every floor below is **optimistic by however much the truth exceeds it**.

### 3.6 Free proxies, measured

| stage | HTTP family | SOCKS5 |
|---|---|---|
| listed | 3,467 | 471 |
| connected | 453 — **13.07%** [11.98, 14.23] | 183 — **38.85%** [34.56, 43.33] |
| HTTPS-capable | 76 — 2.19% [1.76, 2.74] | — |
| **served Instagram** | **44 — 1.27%** [0.95, 1.70] | **70 — 14.86%** [11.93, 18.36] |

**Combined: 3,938 listed → 114 usable = 2.89% [2.42, 3.47].**

**The collapse is at TLS, not at connect** — 377 of the 453 that spoke plain HTTP could not
carry HTTPS, and Instagram is HTTPS-only. **SOCKS5 is 3x better and the project cannot currently
use it**: the SOCKS library is not installed, so it was measured by hand-rolling the handshake
on a raw socket rather than installing into a virtualenv two live rounds share. **One install is
worth 70 usable proxies against 44.**

**Clock cost — do not quote a single ratio.** Direct **1.55 s** median / 2.79 s p90 (n=12);
proxy first load **3.50 s** / 7.87 s (n=44); proxy **sustained 2.35 s median / 5.10 s p90 /
8.87 s p99 / 53.05 s max** (n=11,359). Median cost **2.25x**, tail **2.82x** — about **1.5
proxies in parallel to match one clean IP**. The same proxies are **19.9x** slower against a
lightweight reference site and 2.25x against Instagram: **the ratio measures the target, not the
proxy.** Absolute seconds are the honest figure.

**Half-life.** Measured window **75 minutes**. Single-probe survival looked like a cliff and
then *flattened*, which no decay curve does — so three probes each at t+75 split the pool into
near-thirds: **33.6% dead, 32.9% flaky, 33.6% reliable**, 66.5% answered at least once.
Extrapolated half-lives: **47.6 min** on "reliable", **127.2 min** on "answers at least once".
**A pool sized off the single-probe number is sized wrong in both directions.**

### 3.7 ⚠️ The privacy finding, stated plainly

A free proxy is operated by a stranger who sees every request that passes through it. That is
the generic warning. **What was actually measured is worse.**

Of 190 free proxies that tunnelled to Instagram, **120 presented a certificate chain that failed
verification — 63.16% [56.10, 69.69]**. The certificates they presented for the site were
retrieved and compared by fingerprint against the genuine one: **91 of 91 forged, 0 genuine
[95.95, 100.00]**, across **67 distinct certificates**, with validity windows beginning **the
day before they were tested**. Corroborated from the other side: 26 of 43 TLS failures worked
the instant verification was disabled.

**These are not slow or unreliable proxies. They are actively intercepting the session.** A box
that re-signs TLS reads every URL, header, cookie and byte in plaintext. HTTPS protects you from
the network, not from the proxy — **the proxy is the endpoint**. A further **314 proxies
demanded credentials and were refused untested**: a candidate that needs a secret in order to be
evaluated cannot be evaluated.

**What this round sent through a stranger's box: zero credentials, zero API keys, zero lead
data, zero email addresses, zero creator handles.** All Instagram requests used eight public
institutional accounts, each verified to occur **0 times** in the lead store. **The rule this
implies, if free proxies are ever wired in: they may carry the free camera and nothing else.**

### 3.8 The free TikTok mirror: worth $0.60, and rotation will not multiply it

The bucket was **derived** rather than guessed, by solving two runs that walled from a rested
start: **burst 15.4, refill 0.360 req/s → 1,298 requests/hour/IP**, confirming the published
~1,190 within 10%, and not contradicted by five clean runs totalling 732 requests.

**Against our own ground truth** (84 handles, rebuilt independently from the paid payloads;
a prior round's 70 reproduce 70/70 byte-identically): **bio exact 56/68 = 82.4% [71.6, 89.6]**,
**followers within 15% = 80/80 = 100% [95.4, 100]**, reachable 80/84 = 95.2%.

**The 17.6% gap is churn, not error** — and this is the part worth keeping. The paid answer is
**52 days old**; zero of the 12 disagreements are blanks and seven are *longer* than the paid
string; the mirror against its own answer 7 days earlier is 94.1%, a weekly churn of 5.9%
[2.3, 14.2] which predicts **63.7% [32.1, 84.1]** agreement after 52 days. We measured 82.4% —
**at the good end of what pure churn predicts, leaving no residual to blame on the mirror.**

**Rotation will not multiply it, and the published mechanism is wrong.** It is not an honest
429 token bucket: the responses carry a bot-management challenge, it is **zone-wide**, and it is
**not keyed on user agent** — a browser UA and a command-line UA are throttled alike. **The
request fingerprint binds before the IP does**, so more IPs do not buy more throughput. The
economics refuse it independently: the call it would replace costs **$0.0006** and a page is
~98 KiB, putting break-even proxy bandwidth at **$6.24/GB** — roughly six times the cheapest
residential price.

**What it is worth:** it replaces **one stage** — the profile fetch — which is **23.5% of all
billed calls, $0.60 per 1,000 delivered pages** of a $2.57 total. It cannot replace discovery,
video search, or the contact sheet: **bio only, never a grid**. It carries **zero outbound
links**, so the bio-link field is lost — the sole source for **3 of 122 addresses (2.5%)**,
keeping **96.7% [91.8, 98.7]**. At its own pace that is **47 minutes per 1,000, serial and
unparallelisable**. **Ship it as a $0.00 availability fallback behind the vendor, never as a
replacement, and price it at zero savings** so nobody quotes a per-1,000 figure it cannot
deliver.

### 3.9 The new floor, against his target

Inputs re-verified from disk where possible. **One did not reproduce: median loads per delivered
page is 13.2 today, not 14.3** (the p90 of 48.0 and max of 62.3 did not move — **the tail is the
sturdier number**). The vendor price and the two-call grid were verified in code, and **$19.73
per 1,000 re-derives** ($19.75 forward). The prior 124–216 h band **reproduces**.

**⚠️ EVERY CELL BELOW IS OPTIMISTIC.** The cooldown is a *lower* bound, and the model assumes
the budget is purely per-IP with N IPs perfectly independent — the very assumption §3.4 shows
was never tested.

| loads/delivered | N=1 | N=10 | N=25 | N=50 | **N at which no IP ever walls** | **N for a 10-minute sprint** |
|---|---:|---:|---:|---:|---:|---:|
| 13.2 (median today) | 108 h | 9.2 h | **0.36 h** | 0.18 h | **13** | **55** |
| **48.0 (p90 tail)** | 413 h | 36.3 h | 9.6 h | **0.66 h** | **47** | **197** |

The published **43.8 hours per 1,000 is refuted** — it sits 2.8x below the physical floor and
came from a run with 50 captures and 2 delivered, before the wall existed. **It is still live
and unmarked on disk in two published reports**, named in §7.

### 3.10 Three costed options

| option | $ per 1,000 delivered | hours per 1,000 | reliability | risk |
|---|---|---|---|---|
| **(a) free proxies** | $0.00 | ~2.25x slower per page, and **only 2.89% of a list is usable** | **~19% blocked on arrival; 33.6% dead within 75 min** | **63% intercept TLS with forged certificates** — camera-only, never lead data |
| **(b) paid residential** | **$42–$335** median · $141–$1,125 at the tail | 0.70 h at N≥14 · **9.01 h at N=13** | works against Instagram; pass rate never measured here | **never beats (c) on cost, at any N** |
| **(b′) paid datacentre** | $21.98 one-off · $0.27 amortised | same | ⚠️ **unmeasured, probably near zero** — Instagram refuses datacentre networks | a ~$22 experiment, and the highest-information purchase available |
| **(c) buy the grid** | **$19.73** · **$9.88 if the id is persisted** | unmeasured; bounded ~0.9–1.1 h | vendor already keyed and paid | ~10x the current per-run budget |

**Two break-evens, two different answers.** On **cost**, residential proxies **never** win —
they bill bytes, so adding IPs buys clock and never cost; it would need $0.47/GB and the market
floor is $1.00/GB. On **clock**, proxies win at **N = 14** — and it is a **step, not a curve**:
N=13 is 9.01 h and N=14 is 0.70 h, a **12.9x cliff for one additional IP**, because 14 is the
first N at which no IP ever walls.

**And one constraint nobody had priced: N IPs is not N browsers.** The camera launches one
browser per lane. This machine has 12 CPUs and 23.9 GiB of RAM with 4.2 GiB free, which tops out
near **12 concurrent browsers — below the cliff of 14, and 5x below the 55 a ten-minute sprint
needs. Proxies are necessary and not sufficient; the second purchase is hardware.**

**A cheaper lever than any of this:** the grid is **two** billed calls but only **one** when the
account id is already known. **Persisting that id halves the buy-outright price to $9.88 per
1,000** — a code change with no purchase, and it makes option (c) harder to beat.

---

## 4. What was refused, and why

* **Burning the production IP to answer the budget-reset question.** It would take the camera dark for 8+ hours for three other live rounds. 20 loads were spent (1.9%) and the IP was left clean.
* **Wiring free proxies into anything.** 2.89% usable, and 63% of those forge certificates.
* **Installing a SOCKS library into a shared virtualenv** mid-round with two other sessions live. Measured by hand instead, and the install is recommended rather than performed.
* **Inferring that rotation resets the budget.** The mechanics are green; this specific question is open and is labelled open.
* **Changing the free mirror's status to "replacement".** It is an availability fallback worth $0.60 per 1,000, and pricing it higher would be a number it cannot deliver.
* **Editing the shared launch file without asking.** Two peers were asked on the pipe first.

---

## 5. What I got wrong, and what the brief got wrong

**Mine:**

* **My first verdict control could not fail, and it caught itself.** It flipped a byte next to the word "rubric" — which landed in a *comment*, so the fingerprint did not move and the instrument correctly refused to certify anything. The fix derives the flip target from the rubric's **own output text**, so the byte provably reaches the model. Only then did it fire.
* **I told a peer the launch file was "clean in the working tree" in the present tense** when the check had a timestamp on it; I patched the file before their reply arrived and they reasonably read my own edit as a second session doing my round's work.
* **I discarded the detail of my own regression run** by piping it through `tail`, and had to re-run 198 tests to find out which four failed.
* **I did not take "pre-existing" on trust.** Four failures in the orphan sweep looked like mine — I had just added a module whose only importer is a function-level import. I removed my module entirely and re-ran: the same four failures. They are pre-existing, in committed files I never touched.

**The brief's, and the project's:**

* **"1,036 loads per IP"** — the count reproduces; **"per IP" was never observed**, and the free-proxy arm shows it is not even a constant (20 to 1,300 across IPs).
* **"At least 8.26 hours dark"** — one episode, recovery never observed, and recovery has since plainly occurred.
* **"1,464 burst / 115.5 sustained"** — burst reproduces; the sustained figure measures **86.4/h**.
* **"Median 14.3 loads per delivered page"** → **13.2** today. The p90 did not move.
* **"page_capture contains 'proxy' zero times, control 'headless' twice"** — both true, but "twice" is a **line** count and the occurrence count is 3.
* **The free mirror's mechanism** — described as an honest 429 token bucket; it is bot-management challenge, zone-wide, and fingerprint-bound before the IP. Also "368 at 0.33 req/s" was 0.280, "120 clean" contains one wall, and "dies at request 33" is 33 *successes*.
* **"$19.73 per 1,000"** — reproduces exactly, and is **halvable to $9.88** without spending anything.

**Two zeros discarded because their controls failed** — recorded because the discards are the interesting part. A raw-HTTP re-derivation of the wall verdict was thrown away: the *known-clean* direct request returned a 620 KB page with no grid, indistinguishable from 17 proxy responses, so **any HTTP-only wall probe reads "walled" on a clean IP**. The cause was found: **the header set alone decides whether Instagram serves a shell** — using the project's own headers, the same request returns a full page. A sub-agent also caught its own artefact persisting 84 handles and 13 addresses, deleted it, and re-verified 0 leaks across 14 files.

---

## 6. Money and safety

**$0.00.** No vendor or billed call by me or any sub-agent; the round's own counter at the
wrapper is the source, not a ledger delta — `spend.json` moved during the round because other
rounds are live, and the API client books nothing, so a ledger delta could not attribute
anything here anyway.

**No verdict moved, and the control can fail.** The per-platform judging surface fingerprints
identically before and after (`a4d740102da431a6`; Instagram `09370ced…`, TikTok `fcbb03c0…`),
while a **one-byte flip** in the rubric's own output text moves it — so the "unchanged" verdict
is worth something. No judging rule was added or loosened and no threshold was moved.

**Tests.** 16 new, all 16 executed and passing. The capture-related suite runs **198 tests with
4 pre-existing failures**, proved pre-existing by removing this round's module and observing the
identical four.

**Data.** Seen stores backed up and sha-verified with a corruption control before any work, body
found **by shape** — the top-level-list store read correctly at 2,193 rows, which is the exact
case a previous helper read as 0. No seen-store row was deleted or rewritten. No address, key,
proxy endpoint, host, port, IP or creator handle appears in this report or any committed
artefact.

**Concurrency.** Three other rounds were live throughout. This round wrote only its own files;
the other dirty paths in the tree are theirs.

---

## 7. What to do next — ranked

1. **Answer the one open question before spending anything: does a fresh IP reset the budget?** It decides whether options (a) and (b) exist at all. It needs one IP burnt deliberately at a quiet hour — not the production IP, and not during another round.
2. **Persist the account id and halve the grid price to $9.88 per 1,000.** A code change, no purchase, and it makes the buy-outright option harder for any proxy plan to beat.
3. **Buy one month of datacentre proxies (~$22) as an experiment, not a solution.** Reliability against Instagram is unmeasured and probably near zero — which is exactly why it is the highest-information $22 available.
4. **Price the hardware before the IPs.** The cliff is at 14 concurrent lanes and this machine tops out near 12. Proxies alone cannot reach the target.
5. **Install the SOCKS library.** It is 70 usable proxies against 44 from the same list, for one command.
6. **Mark the refuted 43.8 hours per 1,000 where it still lives** — `reports/BL-1508-the-cost-baseline.md:134` and `reports/BL-1488-end-to-end-production-readiness.md:302`. It sits 2.8x below the physical floor and is unmarked in both.
7. **Ship the free mirror as an availability fallback behind the vendor**, priced at zero savings.

---

## 8. Paths to open

* `clippershq/proxy_pool.py` — the pool, its three states, and the loud refusal
* `clippershq/page_capture.py` — the one hunk, at the only browser launch in the project
* `tests/test_bl1514_proxy_pool.py` — 16 tests, including both launch branches driven through a fake browser
* `scratch/bl1514_verdict_control.py` — the per-platform fingerprint and its one-byte-flip proof
* `scratch/bl1514_agentA_mechanics.md` — the proxy proof, rotation cost, and the deciding test
* `scratch/bl1514_agentB_freeproxies.md` — the free-proxy census and the certificate evidence
* `scratch/bl1514_agentC_urlebird.md` — the derived bucket, the ground-truth comparison, and the churn analysis
* `scratch/bl1514_agentD_arithmetic.md` — the floor as a function of N, and both break-evens

https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/BL-1514-the-wall-is-reputation-not-a-counter.md
