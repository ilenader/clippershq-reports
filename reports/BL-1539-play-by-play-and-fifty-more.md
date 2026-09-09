# BL-1539 — fifty more, narrated, and the operator graded them live at 54 of 54

**TikTok edits only. Measured 2026-09-09 against production, from
`checkpoint/session-2026-07-23-full-day` at `9ead24e3`.**
Spend cap $2.00. **Actual spend $0.1146** across all runs, counted by each run's own wrapper
counter — `api_client.py` contains no ledger writer at all.

---

## THE PARAGRAPH AT THE TOP

**50 pages are in front of him and 7 were rejected to get there** — 57 walked in total. It
cost **$0.0972** and took **21.7 minutes**. The sheet is at `output\bl1539_sheet\` —
double-click **`OPEN_BL1539_SHEET.bat`**; it picks its own port. **And he graded it while
this round was still running: 54 of the 57 cards, and the funnel and he agreed on every
single one — he kept 49 of 49 delivered pages and dropped 5 of 5 rejections.** The previous
round's five rejections were all *wrong*, cut by a date that was not the page's date; this
round bought the account's true newest-post date for **15 pages the tag-date floor would
have cut, and 10 of those 15 were saved**. Not one account repeats: **57 rows, 57 distinct
account ids, zero overlap with the seen store's delivered pages and zero overlap with the
previous run.**

---

## 1. THE THREE FIXES FROM PART 1

### 1.1 The paid-call guard now DERIVES its list instead of carrying one

`test_bl1516_paid_call_ordering` enforced "every free question before you buy anything"
against a **hand-maintained tuple of function names**. A hand-maintained allow-list cannot
notice a call nobody added to it — and the previous round added a real purchase
(`newest_post_epoch`) that this file could not see, *and said so in its own report*, and the
gap survived anyway.

**The general fix: derive the set from the module's own structure.** A billed function here
has one signature, in both modules — it meters through `on_call(...)` **and** calls a method
on `client`. Forgetting to declare it would mean not making the call.

```python
def derive_billed_names(module_path):
    """-> {name} for every top-level function that meters a call and hits the vendor."""
```

**FIX CATEGORY: GENERAL.** One function, both platforms, and it found things immediately:

| Module | Found |
|---|---|
| `tiktok_finder` | 6 billed functions; **1 undeclared** — `newest_post_epoch` |
| `meme_finder` | **8 undeclared purchases**: `accounts_from_search_reels`, `captions_for`, `media_likers`, `profile_facts`, `search_accounts`, `suggested_profiles`, `user_followers`, `user_following` |

**Nine purchases this guard had never heard of.** One of them, `suggested_profiles`, is
called *inside the Instagram worker* — declaring it subjected it to the boundary test, which
it **passed**. The other seven are declared and counted; their ordering is the Instagram
side's decision and it now has the list to make it from. No Instagram behaviour was changed.

**The ordering decision, made explicitly.** `newest_post_epoch` is declared as a purchase and
is exempt from the *ordering* rule, with the reason written into the spec where a reader will
find it:

> The boundary exists to stop the funnel buying **evidence** for a page the free rules would
> reject. This call is not evidence: it is the **input to** the free rule that is about to
> reject, it is made **only** when that rule would otherwise cut, and its only possible
> effect is to **spare** the page. It cannot waste money on a doomed page, because the page
> is doomed at the moment it fires and this call is what un-dooms it.

A committed test fails if that exemption set grows, empties, or gains a name with no
justification — so the next person to exempt a call has to say why in the same commit.

### 1.2 The full suite, re-run, verdict line quoted

```
FAILED -- 27 red of 469 suite(s)   (2389.5s)
```

**Attribution is per-suite-name against the previous full run — the two totals are never
subtracted.** Result: **zero suites red now that were not red before**, and
`test_bl1326_recency_wired.py` — repaired last round and only ever verified on its own — is
now **confirmed green in a full run**. `test_bl1516_paid_call_ordering` remains red on a
pre-existing assertion about `videos_from_handle` ordering that this round did not touch; its
three new tests pass.

### 1.3 Both prior fixes driven on the real path

| | Driven result |
|---|---|
| True date consulted **only** when the floor would cut | floor passes a 3-day page → **0 calls**; floor says 634d → **1 call**, truth 5.0d → **page saved** |
| A dead call | `epoch=None`, `RuntimeError: vendor down` → **UNJUDGED, never a rejection** |
| Crop gone at `cols == 1` | 465×992 → **356×760, scale 0.766/0.766 — whole image** |
| **The control** (`cols=3`, which *should* crop) | 155×275, scale **0.333/0.277 — CROPPED** |

Every helper `hasattr`-checked before being driven: a module can import cleanly and still be
unrunnable.

---

## 2. THE STOP, PROVED BEFORE SPENDING

Asked for 3. Got exactly 3.

```
DONE: walked 3, delivered 3, rejected 0, unjudged 0, 2 billed = $0.0012, 1.5 min
```

---

## 3. THE PLAY-BY-PLAY LOG

One line per event, plain English, **fsynced before the next event starts**. A real page:

```
[12] @<handle> -- never seen before (checked by id against the seen store and this run)
     free facts: 3 video(s) from this tag, best 694,800 views, 412 post(s) on the account
     the tag video is 31 days old -- that is a FLOOR, not the page's date (it can only be
     older than the truth). Against the 180-day wall this passes
     fetched the account's own videos: 12 (1 call, $0.000600)
     picture: built [934, 1993], delivered [356, 760] -- whole image
     the model said GOOD at 85 confidence: 80s movie montage edit, found footage,
     stylised text inside frame; classic wanted edit page
     VERDICT DELIVERED
     running total: walked 12, delivered 11, rejected 1, unjudged 0, spent $0.0090
```

**It does not slow the run, and that is measured, not asserted: 473 lines, 3.24 s of a
21.7-minute run — 0.2%.**

---

## 4. THE RUN

`mode: edits`, resolved and driven (`run_mode.resolve('edits') -> ('edits','config')`).
Hashtags only. Entry point asserted **not** under `tests/`; client asserted a live
`LamaTokClient`.

| | |
|---|---|
| pages walked | **57** |
| **delivered** (the `passing` counter, **never `leads`**) | **50** |
| rejected | **7** |
| unjudged | 0 |
| delivery rate | **87.7% [76.8, 93.9]**, denominator 57 |

**`#ufcedit` was not opened.** It is drained — 138 accounts, saturated at page 7, 55 used
last run — and his rule is *use it once, never again*. **`#movieedit` alone supplied all 57**
and did not saturate; six further tags (`animeedit`, `footballedit`, `caredit`, `gymedit`,
`nbaedit`, `f1edit`) remain unopened.

### No duplicates, checked by account id

| Check | Result |
|---|---|
| within this run | **57 rows, 57 distinct ids — none** |
| against pages already **delivered** to him | **NONE** |
| against the previous run's 55 rows | **NONE** |

Eight rows *do* exist in the seen store — all `is_decided=False` (four explicitly UNJUDGED,
four rejections carrying no attributable decider, which re-walk by design). **Not one page he
has already been given is repeated.**

### The seven rejections, and every one carries a picture or says why not

| row | cut by | on what |
|---|---|---|
| 2 | recency | newest post **478 days** old |
| 8 | **the model** | *"Film student posting her own creations and personal footage, not found edits."* |
| 27 | recency | **1114 days** |
| 29 | recency | **353 days** |
| 38 | recency | **1180 days** |
| 40 | **the model** | *"Movie edit shape, but Spanish burned-in text on every cover — non-English."* |
| 53 | recency | **274 days** |

**Pictures were built for 6 of 7 rejects** — a recency cut fires before any picture exists, so
they were built afterwards from the same covers. The seventh says on its card *"this account
no longer appears on #movieedit page 0, so its covers could not be re-fetched"*. **Nothing
else is ever shown in its place.**

### Did the recency fix land?

**The count did not fall — 5 recency rejections last run, 5 this run. What changed is that
they are now right.** Last round's five had true dates of 1.3, 24.5, 12.0, 127.4 and 67.7
days: **all five were inside the wall and all five were wrong.** This round's five have true
dates of **274, 353, 478, 1114 and 1180 days** — every one verified against the account's own
posts *before* the cut was made.

**And the fix's real yield is the pages it saved: the true date was bought for 15 pages the
tag-date floor would have cut, and 10 of those 15 walked on.** Under the old code all 15
would have been rejected.

---

## 5. HE GRADED IT LIVE, AND AGREED ON EVERYTHING

He opened the sheet while this round was still running and graded **54 of the 57 cards**.

| Denominator | Result |
|---|---|
| pages the funnel **delivered** (49 graded) | **he KEPT 49 = 100.0% [92.7, 100.0]** |
| pages the funnel **rejected** (5 graded) | **he DROPPED 5 = 100.0% [56.6, 100.0]** |
| **overall agreement** (54 graded) | **54 of 54 = 100.0% [93.4, 100.0]** |
| disagreements | **none** |

**Read the intervals, not just the point estimates.** 5 rejections cannot support a tight
bound — the lower edge is 56.6%, so "the funnel rejects correctly" is *supported* here, not
*established*. The keep rate is one-sided and is not capped by his 75.6% self-consistency;
the agreement figure is, and at n=54 it sits at the ceiling.

Three cards were left ungraded (1 delivered, 2 rejected). **His marks were not touched** —
see §7.4.

---

## 6. THE NUMBERS, EVERY DIVISION WRITTEN OUT

| Measure | This run | Previous run | Change |
|---|---|---|---|
| pages walked | 57 | 55 | — |
| delivered | 50 | 50 | — |
| rejected | **7** | 5 | +2 |
| delivery rate | 87.7% [76.8, 93.9] | 90.9% [80.4, 96.1] | overlapping intervals |
| billed requests | 162 | 141 | +21 |
| spend | **$0.0972** | $0.0846 | +$0.0126 |
| pages walked per delivered | 57 ÷ 50 = **1.14** | 1.10 | — |
| paid calls per delivered | 162 ÷ 50 = **3.24** | 2.82 | +0.42 |
| **$ per 1,000 delivered** | 0.0972 ÷ 50 × 1000 = **$1.94** | $1.69 | +$0.25 |
| seconds per page — **median** | **19.1** | 53.7 | **2.8× faster** |
| seconds per page — **p90** | **41.5** | 168.5 | **4.1× faster** |
| seconds per page — max | 116.0 | 279.9 | — |
| **wall clock for 50 delivered** | **21.7 min** | 66.0 min | **3.0× faster** |

**The clock moved, and by a lot.** 22 hours per 1,000 delivered became **7.2 hours per
1,000** (21.7 min ÷ 50 × 1000 ÷ 60). That is still above the 2-hour target and the gap should
not be buried: the remaining time is the per-page cover fetches and the model call, not the
logging.

**The money target is still met**, at $1.94 against $1.69 — the extra 42 calls per 100
delivered are the true-date checks and the per-page own-video fetch. **Never composed from a
carry rate; measured per 1,000 delivered directly.**

**MAYBE rate: 20 of 52 = 38.5% [26.5, 52.0]** — against 22.0% last run. Higher, and the cause
is in §7.1: the pictures this run were built from fewer covers on average than last run's, so
the model had less to go on. **GOOD 30, MAYBE 20, BAD 2.**

**Pictures: 0 of 56 cropped.** Every one delivered whole, verified by aspect ratio.

---

## 7. WHAT YOU GOT WRONG

**1. I starved the model of facts and it hedged on everything.** My first 50-page run passed
`{"handle", "notes"}` as the facts pack where production builds eleven fields. The model
returned **MAYBE on 50 of 50 pages** — 100%, against 22% the previous run. It was not being
cautious; it had nothing to reason from. Wiring the full pack (bio, followers, posts,
captions, `found_via`) restored discrimination immediately: GOOD 5 / MAYBE 7 in the first
twelve pages, with confidences of 88, 85 and 80. **I re-ran the whole thing.**

**2. Then I shipped one-tile pictures and had to re-run again.** The second run built each
contact sheet from the *tag* videos, which return ~1 video per account: **51 of 54 sheets
were ONE tile**, against 28 of 55 at **twelve** tiles the previous run. The model was being
shown one cover and asked to judge a page. Adding the account's own-video fetch — the call
production already makes — brought 12-tile sheets back and dropped MAYBE from 58% to 38.5%.
**Two full re-runs, ~40 minutes, because I did not check what the picture actually contained
before judging on it.**

**3. The watcher cost 76,000 tokens and produced no findings.** I spawned a cheap-model
watcher as instructed, and it re-notified on every poll with "17 rows. Pipeline continues…"
instead of analysing anything. I stopped it and did the whole anomaly pass — six classes,
duplicate detection, timing percentiles — **in one command over one file**. That is exactly
the case the standing rule describes: *do not spawn a sub-agent for a task one command
answers*. I should have recognised the shape before spawning it, not after.

**4. I nearly deleted his live grading as "my test mark".** The instruction to delete my
probe row is a good one — a probe once landed in his ground truth. But when I went to clean
up, `marks.jsonl` held **53 marks he had made while I was working**. Had I run the deletion I
had planned, I would have destroyed real ground truth. **Nothing was deleted.** My own test
click appears never to have registered a row: the card was already marked KEEP, so setting the
same value fired no `change` event.

**5. The browser you picked could not reach the page.** The extension dropped mid-verification
and two Chromes were connected; you chose Browser 1, and it returned an error page for both
`127.0.0.1` and `localhost` while the server was demonstrably listening. Browser 2 — the one
already holding the sheet — worked. I switched and am saying so rather than quietly using a
different browser than the one you named.

---

## 8. SAFETY, AND WHAT I ROUTED WHERE

**Safety.** All 8 files backed up (config, spend, master, **all five** seen stores),
sha256-verified, path from one round constant. Bodies found **by shape**: `spend.json` is a
list at `runs`, `clip_seen.json` a bare list (2,193). **Both corruption controls fired**,
including the one that matters: deleting row #2279 — one of a duplicated pair — left the
natural-key set **identical** while the index-qualified fingerprint **changed**.

**The cap binds.** `reserve()`'s real source lifted by AST and driven: a funded $2.00 cap
**allows** and the meter advances (3,333 requests); the ceiling **raises**; **$0.00 raises**;
the meter **does not advance on either refusal**; and `spend.json` was **byte-identical across
the proof**.

**Ports.** The listening-port table was checked before every write under `clippershq/` and
before the live run. `dashboard/.running.json` still names a pid and a port and **still lies**;
it was not consulted. No Python process was killed. The `.bat` was tested by
`Start-Process` from its own directory — the way a double-click launches it, not via
`cmd /c start` — and a python listener was confirmed in the port table.

**Config was read by named key**, never printed whole.

### Routing

**One sub-agent was spawned and it was the wrong call — see §7.3.** Everything else was one
command each and stayed here: the guard derivation (one AST pass), the suite attribution (two
`grep`s and a `comm`), the duplicate proof (one pass over one JSONL), the MAYBE rate, the
timing percentiles, his grading score. The previous round delegated nothing and was right to;
this round delegated once and was wrong to. **Net: 76,000 tokens spent for no findings.**

---

## 9. WHAT THE NEXT ROUND SHOULD DO

1. **The clock.** 7.2 hours per 1,000 delivered against a 2-hour target. The remaining time is
   per-page cover fetches and the model call, not logging (0.2%).
2. **Open the next tag.** `#movieedit` did not saturate and six tags remain unopened.
3. **Fix the pre-existing `test_bl1516` ordering failure** — `videos_from_handle` is not
   dominated by the free-rules boundary, and that has been red for at least three rounds.
4. **Decide the Instagram orderings** for the eight purchases the derivation surfaced.
5. **Re-score the MAYBE wording paired**, now that the facts pack and the picture are both
   right — the 38.5% measured here is a fair baseline in a way the 100% and 58% were not.

---

*Round BL-1539. Claim filed in `.claims/BL-1539.json` and ended on completion. Backups in
`backups_bl1539_20260909/`, sha256-verified, both corruption controls fired.*
