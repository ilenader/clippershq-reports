# INFRA-013 — Reading the dashboard as the operator, not the author

**Date:** 2026-08-01 · **Type:** Read-only review · **Spend:** **$0.00**
Claimed as INFRA-013 · no file changed outside `scratch/infra013_*` · nothing saved, nothing started

I walked the server already running on `127.0.0.1:8787` — the operator's own, up since 16:16,
pointed at the live config — rather than a clean one, because a clean one would not have had
four half-dead runs in it. I clicked tabs and read. I never pressed **Save** and never pressed
**Start**. The ledger moved underneath me while I read (lifetime `$4.7650` → `$4.78`, 162 → 163
entries) because other rounds were spending; that is the page working, not a fault.

The short version: **five of the six tabs are honest and two of them are genuinely good. The
one you would actually open every day is the one that is currently wrong.**

---

## Now

![Now tab](https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/infra013/now.png)

*The question:* is anything running, and is it going well? I would ask this every time I opened
the page. It is the right panel to lead with.

*What it told me:* two runs, both costing nothing, one of them running for 58 minutes without
finding anything. Every part of that is misleading.

**There are not two runs — there is one funnel appearing twice.** `repost_finder` comes from
the marker file; `repost` comes from `run_status`, the per-run source INFRA-002 added. The
frontend concatenates the two in `runningOf()` without reconciling them, so one funnel with a
marker *and* a headless run status is two cards. The operator has no way to know that.

**`$0.000 spend` is fabricated.** `/api/now` returns `"spend": null` for `repost_finder` —
correctly, because the marker carries no spend field. The page renders it as `$0.000`, because
`money(null)` computes `Number(null)`, which is `0`, which is finite, which formats as
`"$0.000"`. Meanwhile the ledger's most recent entry is `repost_finder … $0.015` and that
campaign has spent `$0.297` lifetime. So the single number on the page that says what a live
run is costing you is a zero the backend never sent.

This one stings because the file argues against it three functions earlier. `progressOf()`
carries the comment *"A null target must yield no bar, never a fabricated percentage,"* and it
honours that. `money()` was written to protect the sign of a correction and was never asked what
it should do with an absent value. The discipline is in the codebase; it just did not reach this
call.

**`0 leads` is not leads.** `statsOf()` falls back through `['leads','pages','appended_incrementally']`
and labels whatever it finds "leads". For a repost run the marker carries `pages`, so pages are
being shown under the word leads. One page is not one lead.

**A dead run is shown as running.** The headless entry `repost-20260801-152147-15296` reports
`status: running`, `elapsed 0.2s`, from a run stamped 15:21 — three hours before I looked. I
checked pid 15296 with the same `OpenProcess`/`GetExitCodeProcess` call the dashboard itself
uses: **the process is gone.** Marker-sourced funnels get that liveness check on every read;
`runningOf()` filters the headless list on the status *string* and checks nothing. The fix from
INFRA-011 covers one of the two sources, and the source it misses is the newer one.

**And the honest part is thrown away.** For each of the four stale funnels the API attaches:

> `marker says running but pid 36740 has exited — a killed run cannot update its own marker.
> Treat as ended, not failed.`

The renderer reads `pick(f, ['summary','last'], 'idle')`. Neither key exists. All four collapse
to the word **"idle"**, behind a disclosure reading *"4 idle funnels"*. Four runs were killed
mid-flight and the page says the same thing it would say if they had never been started. There
is even a function that would have rendered it properly — `idleLine()`, which checks `status`
and `ts` — and it is **never called**; the weaker version was inlined one screen above it.

## Start

![Start tab](https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/infra013/start.png)

A funnel picker, a target, a spend cap, and a **Start** button that ships disabled. It does not
pretend: the note says it would show an estimate and confirm before spending. But it is the one
tab that offers an action and cannot perform it, and it does not say why — a disabled button
with no reason reads as broken rather than deliberate. Either say "not wired yet" on the face or
drop the tab until it does something.

## History

![History tab](https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/infra013/history.png)

**"No run carries a run_id yet."** This is correct, and I verified it independently rather than
taking the panel's word: **163 ledger entries, and not one has a `run_id` field at all** — not
empty, absent. That is exactly consistent with BL-862 finding `--run-id` discarded on all five
headless funnels. The panel is not broken and is not lying, and the *"Why so few?"* note
("History is honest going forward and empty looking back") is the right sentence.

But an empty table is still an empty table, and it will stay empty until BL-862's fix lands and
runs accumulate. Right now this is a tab that costs a click and returns one sentence. That
sentence belongs on **Now** as a caveat under lifetime spend; the tab can come back when it has
rows.

## Spend — **both requirements confirmed**

![Spend tab](https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/infra013/spend.png)

**Metered vs estimated: yes, on the face, unmissable** — `$4.7650 lifetime`, `$4.5736 metered`,
`$0.1914 estimated`, with *"Estimated spend is shown separately so it is never quoted as
measured."*

**Corrections negative: yes, verified in the rendered DOM** —

```
CORRECTION_bl842_double_count_242_calls_reversed   −242   −$0.1452   [correction]
```

Negative calls, negative dollars, a proper minus sign, a `correction` tag, and a
visually-hidden *"minus $0.1452"* so a screen reader does not read it as positive. A second row,
`CORRECTION_killed4_was_not_killed_double_count`, is classified by label at `$0.00`. The ledger
total is `corrections_total: -0.1452`. Nothing clamps at zero.

![Spend, entries open](https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/infra013/spend_open.png)

Two things are computed and then discarded, though:

- **The percentage.** The API returns `estimated_pct: 4.004`. The page shows three dollar
  figures and no ratio. Your **4.55%** was right when it was measured — the estimated dollars
  are frozen at `$0.1914` while lifetime keeps growing, so the same reconstruction is 4.55% at a
  `$4.21` lifetime and **4.00%** at today's `$4.78`. It will keep drifting down without ever
  getting more measured. The page should say the ratio, because the ratio is the thing that
  decays.
- **The corrections total.** Also computed, also never rendered. The one correction is a single
  row among 163, behind a collapsed disclosure. The ledger overstated by up to 100% once; the
  evidence that it was caught should not require scrolling 163 rows to find.

## Files — the best panel here

![Files tab](https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/infra013/files.png)

One file at the top, and the reason it is the only one:

> **Send from this one.** It contains every other send file — using a second one mails the same
> people twice.

That is the actual question (*what do I send?*), answered with the actual trap named. The other
40 sit behind a disclosure and each carries its own one-line reason not to use it — *"Predates
the current suppression rules — do not send from it"*, *"Handles to DM, not emails to send. A
different channel."* This is what every other panel should read like.

![Files, other files open](https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/infra013/files_open.png)

One stale string: **"Videos — Nothing yet, memebot is not wired."** There are **55 rendered video
files on disk** — 52 in `memebot/meme/out` (26 clips × `_v01`/`_v02`, rendered 29 July) and 3 in
the scraper's `final/` directories. Hardcoded, and now false.

## Settings

![Settings tab](https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/infra013/settings.png)

23 knobs, each with a consequence line, and the dangerous ones carrying a second **Careful** line
that quotes the measurement — *"Above ~777 the run exhausts its seeds and forces expansion, which
cost a MEASURED 17-point drop in handle rate"*, *"At the old default of 10 one page took 120 of a
200-clip target and 95.5% of the library came from two accounts"* — plus the MusicBrainz
single-run warning pinned at the top. The other 43 are behind **Advanced** rather than deleted.
This is the best-argued panel on the page and I would not change its content.

Two notes. The labels are raw config keys — `spotify_finder.run_target`, `clip_max_pages_per_account`
— on a page whose entire thesis is plain language; the *description* is in English and the
*name* is not. And nothing here says which of these values the last run actually used, so 23
numbers sit at the same weight whether they are load-bearing today or vestigial.

---

## What is missing — I measured all four, and the page shows none of them

| what you asked for | measured now | on the page? |
|---|---|---|
| clip library size | **2,003 clips**, 172 accounts, 52 shards | **no** |
| its concentration | **top-2 = 10.3%** (`loste1980` 6.1%, `movies.avengers` 4.2%) | **no** |
| finished videos | **3** in the current pipeline's `final/`; 52 older meme renders | shows *"Nothing yet"* |
| clips parked for want of a song | **1,891 of 2,003 (94.4%)** match no mood; 112 match one | **no** |
| last run cost | **not answerable** — see below | **no** |

Two of these deserve more than a row.

**"Last run cost" cannot be answered at all.** Not "is missing from the page" — cannot be
computed. No ledger entry carries a `run_id`, so there is no boundary between one run and the
next. The nearest honest answers are *the most recent entry* (`$0.0048`, BL864_VISION) and
*today's total* (`$0.6018` across 51 entries). This is the same root cause as the empty History
tab, and it is worth seeing that your two questions — "what did the last run cost" and "why is
History empty" — are one question with one fix.

**The parked-clips number is the one I would put on the wall.** By the current matching rule
**94.4% of the library cannot be used** — 1,891 clips resolve to no mood, against 112 that match
one of the 4 songs (hype 102, warm 8, melancholy 2). Separately, only **732 of 2,003 (36.5%)**
carry vision labels at all, and labelling is running right now. So the number will move, but the
shape is clear: the library is not the bottleneck, the song store is.

**One figure I cannot reconcile, and am flagging rather than asserting.** I measure top-2
concentration at **10.3%**; BL-851 recorded **1.8%** at the same library size of 2,003. Same
corpus size, very different number. The likely explanation is that 1.8% described one walk's
contribution rather than the standing library, but I did not verify that and I am not going to
claim a regression I have not proven. Worth ten minutes from whoever owns the walk.

---

## The verdict

**No — I would not learn from this page whether the system is healthy, and on the Now tab I
would learn something false.**

Everything about the day's actual work is invisible: 2,003 clips, 94.4% of them unusable, 3
finished videos, 51 ledger entries today. What *is* visible is two cards for one funnel, a dead
run described as running, four killed runs flattened to the word "idle", and `$0.000` where the
backend said "unknown".

**The smallest change:** make **Now** stop fabricating, then let it carry the standing numbers.
Concretely, and it is about ten lines —

1. `money()` returns `null` for `null`/`undefined` instead of `$0.000`, so an absent value shows
   as `unknown` (the pattern this project already uses for `views_unknown`).
2. Run the existing `_pid_alive` check across the headless list too, not just markers.
3. Call `idleLine()` — it exists — and add `note` to its `pick` list, so a killed run says it was
   killed.

Do those and the panel becomes trustworthy. Then a single strip across the top of **Now** —
*library 2,003 · 94% unmatched · 3 videos · $0.60 today* — makes it answer "what do I do next",
because every one of those numbers is already computed by code in this repo. I have deliberately
not implemented any of it.

## Honest limits

- **I did not press Save or Start.** The concurrency check, diff preview and run launcher are
  therefore unexercised here; this is a reading, not a test of INFRA-012.
- **The library was being written while I measured it.** BL-849/851/863/864 are appending; the
  2,003 and the 10.3% are a snapshot, taken through the library's own reader.
- **The parked-clip figure depends on a rule that is being changed right now.** MEMEBOT-022 is
  editing the mood map and the title matcher this hour, so 94.4% is today's rule, not a constant.
  I read `match()` as returning a *mood*, and counted clips with no mood as parked.
- **"Finished videos" is my definition, not the system's.** Nothing declares a video finished; I
  counted files in `final/` and `out/` directories.
- **One tab I judged on content, not use:** Start ships disabled, so I could only read it.
- **Accessibility, unasked but worth recording,** since I was reading the markup anyway: this is
  better than most. Correct `tablist`/`tab`/`tabpanel` roles with roving `tabindex`, a
  visually-hidden `<h2>` per panel, both live regions placed *outside* every panel (a live region
  inside a `hidden` tabpanel never fires), `aria-hidden` on the progress bar so NVDA does not beep
  on every poll, a `<noscript>` fallback that reveals all panels, and the negative amount given a
  visually-hidden *"minus $0.1452"*. The gap is not markup, it is content: "idle" repeated four
  times conveys nothing to anyone, sighted or not.
