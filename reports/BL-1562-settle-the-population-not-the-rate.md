# BL-1562 — settle the population, not the rate

> ⚠️ **INTERIM, published at the halfway mark on purpose.** Territory 1 is settled and
> re-derived; two sub-agents are still running and the free-window probe needs the rest of the
> night's silence. Anything not yet measured is marked ABSENT rather than guessed. This file
> will be updated in place at the same URL.

**An Instagram editor's email address costs about $4.83 per thousand today, and about $2.31 per
thousand when the free bio route is serving — roughly three times cheaper than the figure I
published four hours ago, because that figure divided by the wrong denominator.** The four
disagreeing editor rates were never an unstable gate. Today's gate over BL-1548's *identical*
corpus returns **30.62% [28.81–32.50]** against the **29.37% [27.57–31.23]** it published —
overlapping, and identical to two decimal places on one of its four runs. **The gate is stable.
The populations differ, and they differ on an axis nobody had named: two thirds of this
project's address inventory is the BUYER funnel, not the labour funnel.** Of 13,172 rows
carrying an address, **8,719 (66.19% [65.38–67.00]) are `lead_kind = client`** — people you
would *sell* clipping to. Only 2,933 are `clipper`. **So "the editor rate" was being measured
over a population that is mostly not editors, and the answer changes by 3.3x once the
population is named.**

**And the standing fact, re-confirmed at a larger n than last time: 13,172 addresses collected,
not one ever contacted.** All seven outcome columns are non-blank on **0 of 73,166 rows**, with
a positive control firing at 73,166/73,166 so the zero is a real absence and not a broken
reader. Every price in this report is a proxy for a value nobody has measured.

---

## 1. What this project is, for a reader with no context

ClippersHQ walks TikTok and Instagram hashtags like `#creededit`, reads the bios of the accounts
that appear, and keeps the email addresses so a human can offer them paid clipping work. It buys
data from **HikerAPI** for Instagram (`ig_api.cost_per_call_usd` = **$0.00069064**/call) and
**LamaTok** for TikTok (`api.cost_per_call_usd` = $0.00060000). Those are 15.1% apart and reading
the wrong one once let a $3.00 cap spend $3.45.

A gate called `editor_gate` decides whether a bio belongs to a likely video editor. **Four
measurements of that rate disagreed 4x and nobody had reconciled them** — which matters because
at $2.32 per 1,000 addresses it is the difference between $8 and $36 per 1,000 editors.

## 2. Safety and money

| | |
|---|---|
| nine stores backed up | sha256-verified, bodies found **by shape** |
| corruption controls | **all six fire**, counted **in the source** (the docstring says five) |
| `clip_seen.json` | **bare list**, 2,193 · `tiktok_pages_seen.json` dict at `pages`, **3,270** |
| `master_leads.csv` | **73,166 rows × 72 columns** at start |

**MONEY SPENT SO FAR: $0.00.** Every number in this interim came off disk. No network request of
any kind has been made — the free-window probe needs an untouched exit and three sub-agents were
instructed not to touch `instagram.com`.

## 3. Territory 1 — the editor rate, settled

### The gate is stable, so the gate is not the problem

Only one of the four corpora can be re-scored at all (see §4), and today's gate reproduces what
it published:

| corpus | platform | published then | **today's gate, masked** |
|---|---|---|---|
| `bl1541_run` | TikTok | 49.51% [40.05–59.01] | **49.51% [40.05–59.01]** |
| `bl1542_run` | TikTok | 35.51% [32.94–38.17] | **37.31% [34.70–39.98]** |
| `bl1544_run` | TikTok | 20.12% [17.57–22.93] | **20.70% [18.12–23.53]** |
| `bl1545_run` | Instagram | 15.00% [10.02–21.84] | **16.43% [11.20–23.45]** |
| **pooled** | | **29.37% [27.57–31.23]** | **30.62% [28.81–32.50]** |

Overlapping throughout. **The gate did not move underneath the measurements.**

⚠️ **A method difference nobody had named, measured rather than assumed.** BL-1548 scored a
**masked** bio (`bl1548_apply.py:90`); every walk scored a **raw** one, address still in it — and
an address whose local part is something like `editshop` contains the word "edit". On the
re-scoreable corpus the gap
is at most **+1.09 points** and the intervals overlap, so it is **not** the explanation. It was a
live candidate until it was measured. The mask itself is verified before anything is scored, on
four planted shapes — plain, `(at)`/`(dot)` obfuscated, space-padded, and an editor-ish local part
— plus bare provider names, because a naive `@[\w.]+` regex once matched the trailing
`@gmail.com` **of the address it was predicting** and manufactured a fake 99.8% recall.

### What the four numbers actually were

Two effects are visible inside one corpus:

- **PLATFORM.** Instagram **16.43%** against TikTok **20.70%–49.51%**.
- **DEPTH.** Inside TikTok the rate decays across successive runs: **49.51% → 37.31% → 20.70%**.

**BL-1548's headline 29.37% is a pooled figure over a corpus that is 2,247 of 2,387 TikTok
(94%), dominated by its two shallowest TikTok runs.** It was never an Instagram number and was
never comparable to the three Instagram walks it was being contrasted with.

### ⚠️ And then the reserved agent showed my own answer was still wrong

I first reported **Instagram 14.76% [11.35–18.98]**. That is a weighted average across three
funnels that have nothing to do with each other:

| `lead_kind` within my own Instagram population | today's gate, masked |
|---|---|
| **`clipper`** — the labour funnel, video editors | **49/102 = 48.04% [38.59–57.63]** |
| `meme_page` — a different funnel entirely | 4/359 = 1.11% [0.43–2.83] |
| `client` — the buyer funnel | 0/9 |

**76.4% of my denominator was meme pages, and the gate was right to reject them — they are not
video editors.** The labour funnel's rate is **48.04%**, not 14.76%.

**$ PER 1,000 LIKELY EDITORS ON INSTAGRAM, CORRECTED:**

| regime | $/1k addresses | **$/1k editors** | interval |
|---|---|---|---|
| free bio route SERVING | $1.11 | **$2.31** | $1.93–$2.88 |
| free route DEAD, top-yield tag | $2.32 | **$4.83** | $4.03–$6.01 |
| free route DEAD, mediocre tags | $9.86 | **$20.52** | $17.11–$25.55 |

Against the $7.52 / $15.72 / $66.80 I published earlier today off the mixed denominator. **A 3.3x
correction, and it came from the agent told to disagree.**

⚠️ **A TENSION I AM NOT HIDING.** Master's **stored** clipper rows with a bio gate at
**48.04% [38.59–57.63]**; the three **fresh** walks' frozen booleans gate at
**26/192 = 13.54% [9.41–19.10]**. **Those do not overlap.** Stored rows are a *selected survivor
set* — they were kept; fresh walk rows are everything the hashtag surface returned. **The walk
number is what predicts a new walk; the stored number describes the inventory already held.**
Which one belongs in a price depends on whether you are valuing the next walk or the existing
asset, and this round does not settle that.

## 4. The operational finding that came out of an instrument failure

My first attempt to re-score the three Instagram walks joined their rows to `master_leads.csv` on
handle to recover the bios. It returned **2/30, 4/71 and 0/91**. A 100% zero is an instrument
failure until a control says otherwise, so I checked: **the joined rows carry a non-empty bio on
0 of 30, 0 of 71 and 0 of 91**, while the walks recorded `bio_len > 0` for every one.

**The Instagram walkers never persist the bio.** They read it, extract the address, gate on it and
drop it — deliberately, because a bio is personal data. The consequence nobody had noticed:

> **The three Instagram editor rates are frozen and can never be re-scored.** All that survives a
> walk is `editor_verdict`, a boolean from whatever the gate was on the day. If the gate changes
> tomorrow, no round can go back and check.

Those three are reported **ABSENT for re-scoring**, never as the artefact numbers my broken join
produced.

## 5. The inventory, re-derived independently

Every figure below was reproduced by me from `master_leads.csv` after a sub-agent claimed it — a
sub-agent's result is a claim until the numbers come out the same a second way.

| | |
|---|---|
| rows carrying an address | **13,172** |
| of which `lead_kind = client` (**buyer** funnel) | **8,719 = 66.19% [65.38–67.00]** |
| `clipper` (labour funnel) | 2,933 |
| `meme_page` | 1,291 |
| **sendable editors** (`clipper` AND verdict ∈ {EDITOR, LIKELY}) | **1,699** — TikTok 1,592 (93.7%), **Instagram 107 (6.3%)** |
| Instagram rows with an address | 9,739, of which **`clipper` = 132 (1.36%)** |
| distinct addresses | 12,886 |

**Five rounds of Instagram price engineering were spent on a route that supplies 6.3% of the
editors this project owns.**

⚠️ **One number I could not reproduce.** The reserved agent reported 2,004 role addresses
(15.6%); my own prefix list gives **1,743 of 12,886 = 13.53% [12.95–14.13]**. The lists differ
and neither is authoritative; the finding — *a `info@`/`contact@` inbox is not a person who edits
video* — survives either way, and the discrepancy is recorded rather than averaged away.

### The leak scan fired twice, and here is what each hit was

Built from **both** corpora — the lead store and this round's own files — with every detector
proved on a planted control first. It reported `{'ANY email address': 1, 'a real creator
handle': 1}`.

**Both were read by hand.** The email-shaped literal was **not a real address** — checked
directly against the lead store, which returned False — it was the mask verifier's own *planted
fixture*, an editor-ish local part invented to test that the mask hides the answer. **It has been
removed anyway and replaced with a description**, because publishing an email-shaped literal to a
public repo is avoidable even when it is synthetic. The handle hit is the ordinary English word
*evidence*, which is also somebody's handle in a corpus of 72,000 — the same false-positive class
that has fired in four rounds running.

⚠️ **Naming the token in this paragraph raises the count**; the published file scans at **3**,
all of them that one ordinary word, with **zero email-shaped literals** and **zero C0 control
bytes**, asserted before writing. The detector is deliberately **not** loosened here.

## 6. ABSENT so far

* **Territory 2** — whether charged-and-empty calls, dead tags or no-address profiles are
  predictable from free fields, and the dedup skip's trend. Two sub-agents running.
* **Territory 3** — the free window. Needs the night's silence; **zero Instagram requests have
  been made.**
* The reserved agent's TikTok price claim (**$2.254 per 1,000 addresses → $3.89 per 1,000
  editors**) is **not yet re-derived by me** and is therefore not in this report's headline.
* Whether the stored-vs-fresh 48.04%/13.54% tension resolves.

## 7. WHAT I GOT WRONG

**1. I published an Instagram editor rate over a denominator that was 76.4% the wrong funnel.**
14.76% should have been 48.04% for the labour funnel. The mistake was not arithmetic — it was
failing to ask what population I was averaging over, in a round whose entire subject is that
question.

**2. I tried to re-score three corpora whose evidence does not exist**, and got 0/91 before
checking whether the bios were there. The control caught it; the design should have.

**3. I had to be corrected by a sub-agent I told to disagree**, on the central number of the
round. That is the process working, and it is also me not seeing it first.

## 8. What did not run, reported as ABSENT

Listed in §6. Nothing in this interim is estimated, extrapolated, or carried over from another
round without its denominator.

---

https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/BL-1562-settle-the-population-not-the-rate.md
