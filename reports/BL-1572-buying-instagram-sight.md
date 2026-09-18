# BL-1572 — Instagram can now be seen, and what it shows is a 22x gap

**Round:** BL-1572 · **Unit:** `ig_api.cost_per_call_usd` = $0.00069064, Instagram/HikerAPI, by
named key · **Spent: $7.050744 of a $9.00 cap.** · No row deleted anywhere.

## The paragraph

**The buy cost $7.050744 and it should have cost $6.305543 — $0.745201 of that is my own
error, and section 8 is about it.** For that money Instagram went from **5.9% judgeable to
94.17% [93.68–94.62]**: 9,074 accounts fetched, **94.70% [94.22–95.14] returned a bio**, 4.68%
were genuinely empty and 0.62% could not be reached. Then the craft cut was applied to both
platforms, **flagged and never deleted**, and it says something nobody has seen before: **TikTok
keeps 18.51% [17.33–19.75] of the rows it can judge, Instagram keeps 0.82% [0.65–1.02]** — a
factor of **22.6**, with intervals nowhere near touching. In raw counts Instagram keeps **75 of
9,739 addressed rows** against TikTok's 733 of 4,158. **I cannot tell you yet whether Instagram
genuinely holds almost no editors or whether the rule simply does not transfer**, because the
cut's 97.5%/22.0% come from 247 labels of which **0 are Instagram**, and master records no
harvest route for these rows. **That is exactly what the review page is for.** It is on your
Desktop as **`clipper_review_100.html`** — double-click it; 50 TikTok and 50 Instagram accounts
that all *survived* the cut, two buttons, arrow keys, ~10 minutes. **Your 50 Instagram grades are
the first evidence either way, and until they exist I would not run this cut on Instagram.**

## 1. What this project is, for a reader with no context

The project finds video editors on TikTok and Instagram who publish a contact address, so they
can be offered clipping work. A hashtag walk collects accounts, the ones carrying an address
become leads, and a workbook of ~3,000 of them is the deliverable. The recurring problem is
precision: most rows that carry an address are not editors. BL-1571 measured a cut that fixes
that — keep only accounts whose bio says they edit — but could not apply it, because **68.1% of
addressed rows had no bio to judge**, almost all of them Instagram. This round buys that sight.

## 2. The price, verified before a cent was spent

**Nothing here was inherited.** The unit was re-read from `ig_api.cost_per_call_usd` **by named
key** — `api.cost_per_call_usd` is TikTok's $0.00060000 and would have priced the buy at
$5.4966. (TikTok's unit is 13.1% *below* Instagram's; Instagram's is 15.1% *above* TikTok's —
the same gap under two denominators, and this project's rule is to name which.)

The rows were re-counted three ways so a single wrong predicate could not pass: **9,739 addressed
Instagram rows = 578 with a bio + 9,161 without**, and the parts sum to the whole.

> **9,161 × $0.00069064 = $6.326953**, re-derived a second way in integer 1e-8 units.

**And the inherited figure was slightly wrong.** Of those 9,161, **87 carry no handle at all** —
there is nothing to fetch — so the real target was **9,074**. That correction came from running
the thing, not from reasoning about it.

## 3. The reader was proved before the money

One call, against an account whose bio was already on disk. The response tree was searched for
the **stored value**, and the field is whatever path holds it — **the field name is an output of
the probe, never an input.** This matters because TikTok's bio field is `signature`, not
`biography`, and a probe that searched for the name it expected once reported 0 of 25 where the
truth was 86.2% **and was believed**.

The field is **`user.biography`** (`biography_with_entities.raw_text` carries the identical
value). The stored bio scored **0.736 similarity** against the live one — **drift, not a reader
failure**: the account had edited its bio since harvest. And the ledger moved by exactly
**$0.000691**, the unit, on both `ig_spent_usd` and `total_spent_usd`.

## 4. The buy, with the three outcomes kept apart

**A failed fetch is UNKNOWN, never "no bio".** A private, deleted or not-found account, an
empty-but-served profile, and a torn response are three different things and only one is evidence
about the account. Validation is on **content, never status** — this vendor returns HTTP 200 with
the payload absent, and five of six parameter variants once returned HTTP 200, charged and empty.

| outcome | count | rate (denominator: 9,074 **distinct accounts**, not calls) |
|---|---|---|
| **bio** | 8,593 | **94.70% [94.22–95.14]** |
| empty_bio | 425 | 4.68% [4.27–5.14] |
| fetch_failed | 56 | 0.62% [0.48–0.80] |

The 200-row sample read 94.50% [90.42–96.90] and the full run landed at 94.70% — this time the
sample did *not* overstate (the previous buy-back's sample read 95.0% against a 93.8% outturn).

**The 56 failures were re-fetched one at a time, and all 56 failed again.** That is a zero with a
positive control: the same code path returned bios for 8,593 other accounts, so these are genuine
unknowns, not an artefact of the parallel fetch. Cost of that certainty: $0.038676.

**Where the bios landed:** all 8,593 went into `master_leads.csv`, into rows that had **no bio**
— the never-overwrite guard was armed and counted, and it skipped **0**, because eligibility
required an empty bio in the first place. **None were lost.** That is a change from the last
buy-back, where only 1,020 of 2,552 could be stored because the rows came from the workbook
rather than master. Master is **74,218 × 75** and Instagram bio coverage went **817 → 9,410**.

## 5. The cut, applied to both platforms — flagged, never deleted

`craft_cut` is a new column: **KEEP** (the bio says editing), **CUT** (a bio was read and it does
not), **HOLD** (there is no bio — the gate's UNKNOWN, which is *not* a rejection). **No row was
deleted**, and a "would remove" sheet lists exactly what the cut would take.

| platform | addressed | KEEP | CUT | HOLD | judgeable | **keep rate of what it judged** |
|---|---|---|---|---|---|---|
| **instagram** | 9,739 | **75** | 9,096 | 568 | **94.17% [93.68–94.62]** | **0.82% [0.65–1.02]** |
| **tiktok** | 4,158 | **733** | 3,228 | 197 | 95.26% [94.57–95.87] | **18.51% [17.33–19.75]** |
| google_play | 213 | 0 | 0 | 213 | 0.00% | — |
| twitch | 99 | 0 | 0 | 99 | 0.00% | — |

**Instagram is now as judgeable as TikTok — and keeps 22.6x less.** The intervals do not come
close to overlapping, so the gap is real and not sampling noise.

**⚠️ What I cannot tell you, and will not pretend to.** Two explanations fit equally well:
Instagram genuinely contains almost no editors, or **the rule does not transfer to Instagram**.
The cut's 97.5%/22.0% were measured on **247 hand labels drawn from master's TikTok bios
harvested from editor-targeted hashtags — 41.9% EDITOR, editor-enriched by construction. They
measure separation, not your lead mix, and 0 of them are Instagram rows.** I tried to settle it
from provenance and could not: master records no tag or source for these rows, and `lead_kind`
and `verdict` are unusable for this — `writer.py:363-367` returns CLIPPER for any `tt:`/`ig:`
source regardless of the bio, and says so in its own docstring.

**HOLD is load-bearing and stayed a hold.** 765 addressed rows across both platforms still have
no bio and were **not** cut. A naive "keep only bio hits" would have deleted them on no evidence;
before this buy that population was 9,685 rows — 68.1% of everything mailable.

### 5a. Your workbook

3,028 rows in, **3,028 out**, `MARK` untouched (0 non-empty before, 0 after), the existing
"Would remove (T2)" sheet left alone, and a new **"Would remove (craft cut)"** sheet with 2,257
rows.

| | KEEP | CUT | HOLD |
|---|---|---|---|
| **this round, bio-only cut** | **576** | 2,257 | 195 |
| BL-1571's prediction via `class_guess` | 680 | 2,156 | 192 |

The ~104 missing keeps are exactly the **handle-only** keeps: `class_guess` is the full gate
(bio OR handle) while this is the bio-only cut, and a handle-only keep is the weakest kind —
79.17% precision alone against the full gate's 87.65%.

**The join is reported because a silent failure looks like a result:** 2,833 of 3,028 rows
(93.56% [92.63–94.38]) found a bio. A first pass joined only 42.9% and would have reported "the
buy did not reach his sheet" when the truth was "the lookup did not reach the bios" — 1,532
handles live only in BL-1569's checkpoint, never storable in master because the workbook and
master are ~94% disjoint.

## 6. The review page

One self-contained dark HTML file on your Desktop, **`clipper_review_100.html`**. No server, no
build step, no external font, script or image — it opens offline, in a year, on a machine with no
network. **100 cards: 50 TikTok + 50 Instagram, drawn after the cut from what survives**, because
the question being graded is "did the filter let a creator through", not "what is in the raw
pile". Each card carries handle, display name, bio, followers, the email, the tag, and a
clickable profile link opening in a new tab. **Two buttons only** — EDITOR / NOT AN EDITOR — with
an optional "why" box on a NOT that never blocks a click. Arrow keys or 1/2, a progress counter,
`localStorage` autosave and a **Download results** CSV button. Every storage read and write is
wrapped in try/catch and the page works with storage unavailable, warning you to download instead.

**Both platforms' coverage is shown on the page itself**, so the Instagram picture is visible
while grading rather than discovered afterwards.

**⚠️ The Instagram half is 50 drawn from only 69 survivors that carry a handle — 72% of the
entire surviving pool**, not a small sample of a large one. That is a direct consequence of the
0.82% keep rate, and it is why those 50 grades are decisive rather than indicative.

## 7. Money, and the cap

| | |
|---|---|
| calls booked | 10,209 |
| ledger | **$7.050744** |
| calls × unit, re-derived | $7.050744 — agrees |
| legitimate calls | 9,074 distinct + 56 retries = **9,130** |
| **duplicate calls (my error)** | **1,079 = $0.745201** |
| what it should have cost | **$6.305543** |
| cap | $9.00, headroom $1.949256 |

**The cap was driven and the proof written to disk before any prose about it:** a funded cap
allows and the meter advances ($0 → $0.00069064); a **declared $0.00 cap refuses** on the per-run
half, the lifetime half, and when absent entirely; the meter **does not advance on a refusal**
(meaningful only because the same meter advanced when funded); and the proof **wrote nowhere** —
0 of 10 stores changed. This matters because `effective_run_cap` once read an explicit 0 as "not
set" and handed over every remaining dollar — $39.5329 on the live config.

Booking used `ig_calls` with `ig_cost_per_call`, and the ledger delta was asserted exact on every
pass. `record_aux_spend`'s `cost_per_call` **defaults to 0.0006 — TikTok's price** — which is how
three ledger sites once booked Instagram 13.1% cheap.

## 8. What I got wrong

**I spent $0.745201 of your money re-buying accounts I already had.**

The harness twice reported my background buy "killed for low memory". **The Python process had
not died — only the harness's handle on it had.** I believed the report and started a
replacement. Four of my own processes ended up fetching at once, each having read the checkpoint
**at startup**, each therefore believing the same rows were outstanding. They raced: **3,128
fetch records covering only 2,050 distinct accounts — 750 accounts bought twice or more, 1,079
duplicate calls.**

Three things worth separating, because conflating them would have made it worse:

- **The ledger was never wrong.** It booked 10,209 calls because 10,209 calls were genuinely made
  and charged. Had I seen the ledger running ahead of my own counter and "fixed the booking", I
  would have corrupted the one part that was honest. **The defect was concurrency, not
  accounting.**
- **A checkpoint makes a *restart* free. It does not make a second *concurrent* run free**,
  because the exclusion it provides is read once at startup and never re-checked. I had reasoned
  about the first property and assumed the second.
- **The fix is a PID lock, and I drove it** rather than shipping code that looks right: a second
  instance refuses by PID, and the refusal was demonstrated. A later "killed" notification then
  cost nothing, because the process was still alive and the lock held.

**A second, smaller error:** the vendor client logs the handle it failed on at INFO level, and my
200-row sample printed a real creator handle to the console before I noticed. Console output is
not committed, but the standing rule here is never to print, log or commit handles, and a log line
is exactly how one reaches somewhere it should not. Silenced before the full run.

**And a judgement call that went right, recorded because it could have gone wrong:** I
parallelised the fetch to 8 workers and `fetch_failed` jumped to 3.50% [1.71–7.05] against 0.50%
[0.09–2.78] serial. A spurious failure is permanent here — the checkpoint stops the row being
retried — so the round would have recorded "we do not know" for accounts that would have answered.
I dropped to 6 workers (failures fell to 0.60%) **and** added the serial retry pass. All 56
survivors of that pass failed again, so the final figure is honest either way.

**What is absent, and named as absent:** any Instagram hand label (0 of 247), which is the whole
reason section 5's gap cannot be attributed; and the harvest route for addressed rows, which
master does not record.

**The suite:** see the note below — the full run could not be completed on this machine, and that
is stated rather than rounded up.

https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/BL-1572-buying-instagram-sight.md
