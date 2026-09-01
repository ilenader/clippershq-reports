# BL-1483 — the parts nobody opened: a live cut that calls itself a dry run, 939 pages latched on nothing, and a debt register whose alarm has been ringing unheard

## IS THE FUNNEL SAFE TO RUN? **NO — ONE CAMPAIGN-LEVEL REFUSAL IS BEING IGNORED TODAY.**

`cut_garbage_dry_run` is `false` at the top level of the configuration and `true` in four
campaigns. The top level wins. Both ZHUS and DAYLIGHT already carry
`cut_garbage_dryrun_seen: true` in `state.json`, which is the gate that forces a first run to be
a rehearsal — so that gate is **already unlocked**. The next ZHUS or DAYLIGHT run performs a
**live cut of up to 40% of the sheet** while the campaign's own configuration says
`dry_run: true` and the Control Panel (`clippershq/control.py:420`) prints `Garbage-cut : False`,
because it renders the *campaign* value rather than the effective one.

Nothing was changed. This round wrote no production file. The fix is one line of configuration
and it is his call, not mine.

---

## 1. ROUND ID, DATE, AND WHAT I WAS ASKED TO DO

**BL-1483**, 2026-09-01. Read-only. The brief: *find what nobody has ever looked at.* Six
territories, one sub-agent each, one ranked list of holes ordered by cost, every zero carrying a
positive control, and no production write of any kind — five other rounds were in flight and one
was mid-rewrite of three of the files this audit reads most.

Vendor spend this round: **$0.0147** against a $0.25 cap. Five of the six territories spent
**$0.00** — nearly everything came off data already on disk.

---

## 2. WHAT ACTUALLY SHIPPED

Nothing. No file under `clippershq/`, `dashboard/`, `tests/` or `config.json` was modified.
`meme_pages_seen.json`, `tiktok_pages_seen.json` and `master_leads.csv` all carry their
pre-audit mtimes. Every artefact is under `scratch/bl1483_*`, plus this report.

Defects are named with `file:line` and **left in place**, as the brief required.

---

## 3. WHAT WAS MEASURED

### 3.0 The round's own premise, re-derived — and both of its numbers were wrong

The brief said 107 report ids exist only locally and 727 only in the public repo. Measured by id:

| | ids | files |
|---|---:|---:|
| local `reports/` | 329 | 331 |
| public repo | 879 | 1031 |
| in both | 223 | |
| **local-only** | **106** | (brief said 107) |
| **public-only** | **656** | (brief said 727) |

**The two archives overlap on 22.6% of their union.** The public clone was fetched the same day
and contains the most recently published round, so "local-only" is not clone staleness. A
content probe settles it: a known-published report matched **6 of 6** distinctive lines in the
public corpus (control passes), and **12 of 12** randomly sampled local-only reports matched
**0 of 6**.

**106 report ids — 2.1 MB, 104 of them inside the newest 200 ids, carrying 5,208 `%`/`n=`/CI
tokens — exist only on this machine.**

This is not a footnote; it is the mechanism. Territory 2 found six thresholds documented **0
local / 1 public**, and Territory 1 measured that searching only the local archive would wrongly
call **10** modules unmentioned, and only the public archive **12**. A round that searches one
archive searches half the history, and that is how findings get re-discovered.

Two adjacent measurements from the same instrument family:

- **21 of 180 settled round ids (11.7%) in BL-1300..1483 produced no report anywhere.** Eight
  left working artefacts on disk — the work ran and the finding was never written: BL-1353,
  BL-1356, BL-1361, BL-1364, BL-1367, BL-1373, BL-1421, BL-1438.
- **A claim has been open 214.8 hours over a round that produced nothing.** Its `will_write`
  declared exactly one file; that file exists neither locally nor publicly. Its intent was a
  sweep of *every* funnel for six recurring error shapes. `tools/claim.py:27-29` deliberately
  never expires claims, which is defensible — the gap is that **nothing checks whether a round's
  declared `will_write` ever appeared.**

### 3.1 TERRITORY 1 — the code nobody has read

**204 modules** (clippershq 160, dashboard 5, tools 39); the application is **165**.

**The prescribed control passed while the graph was still broken.** The brief told the agent to
prove its import graph by checking that the two live finders and the judge came back reachable.
They did — under a graph that was nonetheless wrong. What it missed was
`dashboard/server.py:5575`, which does `for _mod in (...): __import__(_mod)` with a **Name**
argument rather than a literal, orphaning three live route modules plus `clippershq/paste_driver.py`
behind them: **77 KB of shipping dashboard**. Two further sites of the same shape sit at
`control.py:3898` and `control.py:4645`.

**A control that only checks the modules you already suspect proves nothing about the ones you
don't.** That is the most transferable result of this round.

- **Dead application modules: 13–18 of 165.** Thirteen undisputed; five move depending on how
  false-alive revivals are treated. All five were read by hand and all five are false-alive — a
  function name in another module's `__all__`, a dict key of the same spelling, and a process
  *identification* allowlist used for stopping a server rather than launching one.
- **Only 2 of 165 modules (1.2%) appear in neither archive** — and both are live and imported.
- **47 of 165 (28.5%) never appear on a report line containing a number; 63 (38.2%) appear on at
  most one.** Stated limit: the test is same-line proximity and cannot tell whether the number
  is *about* the module, so it **over-credits** — every **NO** is reliable, every count is an
  upper bound.
- `page_rules.py` and `song_loudness.py` have **zero references of any kind**. `page_rules.py`
  was written **2026-08-31, the day before this audit, and was never wired**.
- **The repo already audits itself, and nothing acted.** `judge_batches.py:14` says three named
  modules "are all correct, all measured, and all have zero production callers";
  `tools/status_board.py:317` says a fourth has "ZERO importers"; `review_sheet.py:1381` says a
  fifth "has no caller".

### 3.2 The debt register — and its alarm has been ringing unheard

This is my own thread, and it is the mechanism behind 3.1.

The repo has a **formal marker convention**, `NO-CALLER-PENDING:`, carried by **14 modules in
`clippershq/`** and three in `tools/`. It is load-bearing, not decoration:

- `tools/no_caller_sweep.py:484` states it plainly — a marked module "**is filtered out one line
  above and can never be reported**".
- `tests/test_bl1389_no_caller.py:51` pins the count with `assertLessEqual(len(pending), 17)`.

So the mechanism is a ratchet: a module with no caller gets a marker, the sweep stops reporting
it, and the test only goes red if the debt **grows**. Standing still is green forever.

**Measured: the marker set is byte-identical at the pin commit and at HEAD.** The pin was set
**2026-08-24**; the same 14 modules carry the same markers today. Not one wired, not one
removed, in eight days — **307,578 bytes across 14 modules**, most with test files and no caller.

**And the guard is not green. It is red, and it has been red unheard.** Run directly, the suite
takes **257.8 seconds** and reports **4 failures of 11 tests**:

1. `test_main_exits_zero_on_the_real_tree` — the sweep returns **1**: *"something is untriaged
   right now."*
2. `test_no_untriaged_orphan` — **7 modules have no caller and no marker at all.** Derived
   independently by marker absence, and the set matches the assertion exactly:
   **`dm_send_list`, `ig_embed`, `mark_reader`, `mark_sent`, `page_rules`, `suggest_harvest`,
   `video_strip`.** Two of those seven are items 67 and 71 of the ranked list below — the
   `suggested` walker, and the module written the day before this audit.
3. `test_tests_are_not_counted_as_callers` — **`score_sheet` now reports `importers: ['sheets']`
   while still carrying `NO-CALLER-PENDING`.** This is exactly the stale-marker case
   `no_caller_sweep.py:484` documents as its own blind spot: a dead-module detector has no
   question for a module that came alive, so it exits 0 the whole time.
4. `test_the_check_fires_on_an_untriaged_tree` — the fixture asserting `score_sheet` appears as
   an orphan now fails for the same reason.

**Two instruments disagree about `score_sheet` and I am not resolving it here.** The sweep counts
`sheets` as an importer; Territory 1 read that call site and judged it a process
*identification* allowlist used for **stopping** a server rather than launching one — i.e.
false-alive. Both readings are in this report; the module is item 64 either way, because on
Territory 1's reading it is still the only sheet builder handling UNJUDGED with nothing calling
it.

**And the guard crashes under this project's own normal operating conditions.** `edges_of`
(`tools/no_caller_sweep.py:263`) wraps its file read in a `try` that catches **`SyntaxError`
only**. It parses `scratch/`. With six to nine concurrent sessions writing and cleaning
`scratch/`, a peer deleting a file mid-walk raises an unguarded `FileNotFoundError` and takes
the whole sweep down — **which is what happened to me while running it**, on a path under
another live round's sandbox. Parsing `scratch/` and quarantined third-party code is also why
the guard takes four minutes.

The 257.8 seconds, the four failures, the seven untriaged modules and the crash are **MEASURED**.
That *a guard slow enough to skip is a guard that gets skipped* is **SUSPECTED** — but the four
standing failures are evidence for it.

### 3.3 TERRITORY 2 — every threshold, and where it came from

**50 named Tier-A constants** plus 12 config overrides across 204 files — **the brief's "25" is
half the real surface**. It cannot be reached without dropping the entire `paid_grid` bars/drawn
stage, the `free_judge` pre-gate, and every TikTok constant.

| claim | measured | verdict |
|---|---|---|
| 23 of 25 fitted pre-split, never re-examined | **48 of 50** | directionally right, denominator wrong |
| only 2 of 25 consult mode | **exactly 2** | **CONFIRMED** |

`tiktok_triage.py` contains **zero occurrences of the word `mode`**.

**The actively misleading threshold, both halves proven: `free_judge.REJECT_AT = 80`
(`clippershq/free_judge.py:390`).**

- **It decides no cut.** The only cut is `free_judge.py:1533`, `c >= _bar`, where `_bar` comes
  from `MAY_REJECT` and both live bars are **90**. `reject_at` does not appear in
  `should_reject`'s body at all.
- **It is printed to the operator**, rendered into the banner he reads at
  `meme_finder.py:5609-5611`.
- **It sets the preflight floor** — `preflight.py:148-150` fails a run when any bar falls below
  it. That is its only remaining job.

**The strongest missing-measurement flag: `MIN_AVG_VIEWS = 1000` carries five lines of
justification ending "He named 1,000; this is 1,000" — and `config.json` ships
`min_avg_views = 500`.** The Instagram view floor runs at **half the number its own
justification describes**, `meme_finder.py:5322` prints 500 to the operator, and **no document
in 1,378 across both archives supports 500**.

About **30 further thresholds return zero documents for their own name** across both archives.

### 3.4 TERRITORY 3 — what the vendors return that nobody reads

**26,063 (family, key-path) pairs across 42 payload families**, 0 parse errors, **$0.00 spent**.

**6,212 pairs (23.8%) are read by `clippershq/`; 19,851 (76.2%) are not, and 11,343 of the
unread sit at 100% non-empty fill.** By leaf name, **269 of 2,986 (9.0%)** are read. The join is
on leaf name and therefore **over-credits reads** — three collisions were verified by hand — so
23.8% is an upper bound and 76.2% a lower bound.

**The grep trap, measured: 106 leaf names appear as bare string literals in `clippershq/` and
are never subscripted or `.get()`'d.** A grep would call all 106 alive. The AST reader passed
17 of 17 positive controls and missed its negative control.

The highest-value unread fields, all on calls already being paid for:

| field | fill (denominator) | why it matters |
|---|---|---|
| a 100-float visual embedding on IG media | 41.9–91.7% on user endpoints | the project computes its own with a local model pass; this arrives free |
| TikTok `video.meta` — loudness, peak, quality score, watch-time distribution | **74/75 = 98.7%** | vendor-measured loudness, free, parsed by nothing, while the loudness module documents three consecutive rounds of defects |
| `like_and_view_counts_disabled` | 100% of 299 media; true on 70 (23.4%) | **on 67 of those 70, the field the code DOES read is the constant 3** — reading it is a correctness fix, not a feature |
| a 105-frame scrubber storyboard | **100% of 62** | a free frame strip, while `clip_cuts.py` derives one with ffmpeg scene detection |
| `ig_play_count` | 100% of 371 | differs from the read `play_count` on **30 of 371 (8.1%)**, by up to 493× — nobody has decided which is intended |

**Two traps caught.** `video.meta` and `music.extra` are JSON **strings**, so a tree walker sees
a single leaf — a second parse pass found 66 such paths in one family alone. And the field-name
check was actually run: `author.signature` really is 0 of 65 in that endpoint, proved by the same
reader finding two sibling fields at 65 of 65 in the same object.

**Negative finding worth recording:** the clips call does **not** make the profile call
redundant — 379 of 416 `user.*` paths, including the bio fields, exist only in the profile
payload.

### 3.5 TERRITORY 4 — the stages either side of the judge

**The latch moved mid-audit.** Commit `ab060d0` ("BL-1478: the skip latch buried 1,351 pages on
nothing") is HEAD. **The standing figure of 4,888 latched pages is 3,586 today.**

**Defect #1 — CONFIRMED, and its stated justification is REFUTED.** The target counts
`stats["passed"]` (`meme_finder.py:7310-7311`), the run prints "counted as DELIVERED" (`:5326`),
and then `:7529` discards every row without an address.

- Instagram, n=827 target-counted: **159 = 19.2% [16.7, 22.1]** carry an email; **668 = 80.8%
  refused.** TikTok: **1,226 of 1,383 = 88.6%.**
- The docstring at `:7518-7521` defends this by asserting those pages are already in master as
  handle-only rows. Joined against master: **only 279 of 668 = 41.8% [38.1, 45.5] are there.
  389 = 58.2% exist nowhere in master.** The control passes at 99.4% on the emailed arm.
- A runtime spy proves the defence is not even a constraint: `crossdedup.append_leads` **will
  append an emailless row**. The filter is `meme_finder`'s own choice.

**Defect #2 — CONFIRMED, partly fixed, and the surface has moved to TikTok.** The Instagram
recount shows the fix worked — 0 of 2,647 latched by an infrastructure decider. But
`tiktok_finder.py:1637-1638` **still runs the old expression**: **939 pages latched, 919 =
97.9% with no recorded reason at all.** `verdict` is absent on 2,446 of 2,446 TikTok records, so
porting `is_decided` unchanged readmits **all 939**, not a subset.

**Three stages can silently drop everything**, all measured with a fake client against passing
n=1 controls:

1. `search_accounts`, `suggested_profiles`, `user_following`, `user_followers` and
   `media_likers` all return **n=0 with an empty error string** on a billed HTTP-200 empty
   payload — a paid nothing reads as an unpopular query. **The file documents this exact hazard
   at `:3220-3231`; the fix was applied to the two functions that observed it and to none of the
   five that carry it.**
2. `crossdedup.py:457-458` — a headerless master returns `{appended: 0, merged: 0}`,
   byte-identical to a legitimate no-op.
3. `run_mode.py:202-203` and `:150-151` — `edits`/`emails` mode eliminates the whole hashtag and
   term supply. Deliberate and announced, but total and uncounted.

**The instrument built to answer exactly this question was never pointed at the funnel.**
`grep -n "decision_log" meme_finder.py tiktok_finder.py` returns **0 lines**. The module logs
57,170 drops across 25 runs — **all of them clip runs, zero page runs**.

**No expiry and no exit, proved four ways:** no `del`, `pop` or `clear` on any seen store;
`record` only ever `update`s, so a field can be overwritten but never removed; `first_seen` is
read by exactly two things and **nothing compares either to now**; and the stale re-judge pass
**cannot be re-run** — a follow-up sweep returned **21 files and not one `.py` producer**, so no
code that writes those markers exists on disk or in git history.

**One latch escapes by accident.** The language-gate writer at `meme_finder.py:6937` omits a
`verdict` key, and that omission is the only reason its records stay re-walkable. **Adding a
`verdict` there would permanently bury every non-English reject.**

### 3.6 TERRITORY 5 — configuration, resolved per campaign by a runtime spy

Resolution happens in `clippershq/main.py::_execute_run`. Precedence is **TOP > CAMPAIGN > CODE
DEFAULT** for a 64-name allowlist (`main.py:4865-4930`), and **CAMPAIGN > CODE DEFAULT** for
everything else. The spy drives the real function on his real config and lifts the merged dict
out of the live frame, aborting before any client is built. The positive control passes on every
family — the outcome moves when a known-live setting moves.

**Denominator: 648 real settings, 258 distinct names, resolved 258 × 5 = 1,290 times. 17 names
select nothing as configured. 17 keys absent from config are read with an OFF-shaped default.
251 `or <falsy>` sites.**

**The brief's "purest case" is REFUTED at the switch and CONFIRMED one key over.**
`cut_garbage_enabled` has exactly the described shape — but it sits *in* the allowlist, so his
top-level `true` wins on all five campaigns and **it is the four campaigns' `false` that select
nothing**. The described mechanism is real on the **non-allowlisted** twins:
`cut_garbage_threshold` (top `40` selects nothing anywhere; the campaign that omits it falls to
the code default **20**, so a score-30 lead is cut on four campaigns and kept on the fifth),
plus `ig_max_pages_per_tag`, `tt_min_deep_median_views` and `ig_min_deep_median_views`.

Also measured:

- **`deep_check_max_usd_per_10k` — top `30.0` beats four campaigns' `10.0`: three times the
  deep-check budget the campaigns declare.**
- **`tt_min_deep_median_views` has two readers returning two different effective values in the
  same run** — 0 at `main.py:2922` via an `or 0`, and 4000 from `quality_gate._median_floor`.
- **`language_gate` is absent from the configuration entirely**, so a gate whose own comment
  records 0 misses of 26 and 100% coverage — against the alternative's 5 of 26 and 78.8% — is
  never called.
- **`mode` is set to the value that already equals the code default**, leaving 7 real TikTok
  editing terms reachable only from a branch that is never selected.

**15 allowlist entries have no top-level key** (the entry is a no-op) and **10 config keys have
zero read sites anywhere** — dead knobs the operator can still edit from the Control Panel.

### 3.7 TERRITORY 6 — the reserved agent, which disagreed and was right

**A false pagination win was caught before anyone shipped it.** `meme_finder.py:3190` calls the
reels search with no cursor, while `ig_client.py:596` has accepted a page parameter all along
and every stored envelope carries a cursor and `has_more: True`. That reads as a one-line win on
his **best** surface. The control says otherwise:

```
no-cursor call, repeated 3x   -> net-new 0, 0, 0    (endpoint is deterministic)
+ the real cursor             -> net-new 6
+ an INVENTED cursor value    -> net-new 6
+ a parameter name I made up  -> net-new 9
```

**Any extra query parameter perturbs what the vendor serves.** A sibling round has just
established cursor-paging for the neighbouring endpoint and left "the hashtag path may have the
same shape" as an open item. Whoever copies it here will measure 60–90% "net-new", call it
pagination, and be reading cache-key noise.

**Why the mix is what it is — and it was never a decision.** Per-handle discovery costs 0.000
calls for seeds (they are a file) against roughly 0.09 for reels. But the **walk** costs **3.20
calls per handle regardless of source** (19,371 lifetime calls over 6,044 handles). So the
83%/3% split is **15,340 free enumerable seed handles meeting roughly 1,850 paid ones**. The
funnel fills its walk with whatever is free to *enumerate*, then pays full price to *walk* all
of it at 38.6% approval instead of 82.4%.

**Inverting it is a config edit.** `meme_finder.search_terms` holds **10** entries and
`hashtags` **11** — while the same file already holds **1,811 / 216 / 113 / 95** hashtags for
four other campaigns. **This project has authored 2,235 phrases for other campaigns and 21 for
this one.**

**The cheaper-unit hypothesis was refused by its own author.** 12,959 addressed master rows →
**12,673 distinct addresses, collapse 1.023**, median 1 row per address, p99 = 2, and only 6
addresses spanning more than one platform. Pages do not collapse into operators.

**And the number that reframes the round:** lifetime vendor spend across the whole project since
07-11 is **$61.04**. Master holds 72,953 rows; `date_sent` is non-empty on **0** and `status` on
**0**. The operator has graded **1,230 distinct pages on 8 active days**. A 2.56× improvement on
the mix converts about $61 of supply into about $61 of better supply, for a consumer with no
recorded consumption. **The missing unit is not a cheaper page.**

---

## 4. WHAT WAS REFUSED OR NOT DONE

- **No production file was touched** — not `clippershq/`, not `dashboard/`, not `config.json`,
  not the seen stores, not master. Five rounds were in flight and one held three of the files
  this audit reads most.
- **No defect was fixed.** The brief said to name them with `file:line` and leave them. The live
  `cut_garbage_dry_run` finding is a configuration change and is his to make.
- **No sender, pitch or outreach of any kind was proposed or built.** This project does not send.
- **The 8,580 / 60.8% "no cover image" figure is not carried forward.** It is not in the
  dashboard run log, not in the rejection store, and not derivable from master, which holds
  72,953 rows over 72,938 distinct handles — **repeat factor 1.00**. The 11 capture manifests
  show a 25.7% no-grid rate over 3,292 records, not 60.8%. Reported as unreproduced.
- **"69 handles cached as failed forever" is not carried forward** either — historical, and
  reproducible from neither live store. Today's equivalent is the 919 TikTok records.
- **Nothing from the measured-and-refused list was re-proposed.**

---

## 5. WHAT I GOT WRONG

**Both numbers in my own round premise were wrong before I checked them,** and I have published
the corrected pair rather than the briefed one: 106 and 656, not 107 and 727.

**My claim-registry reader returned `paths=0` for my own claim** — which I knew carried two
entries. The real key is `will_write`. That is exactly the field-name error this project already
has on record, reproduced live inside the round that was warning about it. The zero was
discarded, not published.

**I nearly published "49.6% of test files never run".** The runner's discovery is airtight — 427
discovered against 427 on disk, zero missed. Looking inside the skip set finds 420 more test
files, which reads as a catastrophe and is nothing: **403 are a vendored package's own legacy
suite, correctly quarantined 28.8 days ago, and 17 are scratch scaffolding — 13 of them
positive-control stubs written the same day by another live round.** Zero project tests are
excluded. I report it because the raw number is alarming, wrong, and reachable by anyone who
runs the obvious query.

**One of my own instruments failed its control, and I did not publish its number.** A narrowed
pass for present-tense "no caller" comments returned 67 lines across 31 files — but it **lost 2
of the 3 hand-verified sites** it was tuned against. A 2-in-3 miss rate on the control set makes
67 a floor with a known defect, not a count. The finding therefore rests on the
`NO-CALLER-PENDING` marker set, the git history, and the live test result — all three exact.

Sub-agents corrected themselves the same way, and it is worth recording: Territory 6's
first-pass timestamp reader missed a field name and would have reported 17 files as having no
timestamps; Territory 3's path index broke on handles containing dots; Territory 1's import
graph passed the prescribed control while still being wrong. **Three of six territories caught a
silent instrument failure in themselves.**

**Where I disagree with my own sub-agents:** Territories 1 and 2 report the archive split in
**files** (112 local-only / 824 public-only); I report it in **ids** (106 / 656). Both are
correct in their own unit — the public repo holds 1,042 files across 880 ids. The id is the
right unit for "how many rounds' findings are invisible", and I have used it throughout. The
corpus also moved under us mid-round, which is why these counts drift by one or two.

---

## 6. MONEY AND SAFETY

**Vendor spend this round: $0.0147** against a $0.25 cap — all of it Territory 6's pagination
control, the measurement that stopped a false scaling claim. Territories 1, 2, 3, 4 and 5 spent
**$0.00**.

Backups were unnecessary because nothing was written. `meme_pages_seen.json`,
`tiktok_pages_seen.json`, `master_leads.csv` and `config.json` all carry pre-audit mtimes. No
process was killed. No ledger row was written — one agent deliberately declined, having
established that each ledger write first copies a 9 MB file.

**The live safety item is at the top of this report.** Two further money items:

- **`deep_check_max_usd_per_10k` runs at 3× what four campaigns declare** — $30.00 effective
  against their $10.00.
- **`cut_garbage_threshold` differs between campaigns by an omission rather than a decision**:
  four cut at 40, one cuts at the code default of 20.

---

## 7. WHAT HE SHOULD DO NEXT

1. **Set `cut_garbage_dry_run: true` at the top level, or delete the top-level key.** Today the
   next ZHUS or DAYLIGHT run cuts live while its own config says it will not. One line.
2. **Port the latch fix to `tiktok_finder.py:1637-1638`** — but read the note first: `verdict`
   is absent on all 2,446 TikTok records, so the change readmits **all 939**, not a subset.
   That is probably what he wants; it should be a decision, not a surprise.
3. **Decide what `meme_finder.py:7529` should do with the 668 emailless Instagram pages.** 389
   of them exist nowhere in master, and the docstring defending the discard is measurably wrong.
4. **Read `like_and_view_counts_disabled`.** It is a correctness fix, not a feature: on 67 of 70
   affected media, the like count the code trusts is the constant 3.
5. **Add phrases.** The largest lever measured this round is that his best surface runs on 21
   phrases while the same config file already holds 2,235 for other campaigns.
6. **Either wire the 14 `NO-CALLER-PENDING` modules or delete them** — and change the pin from
   `assertLessEqual` to equality, so standing still stops being green. The suite is **already
   red**; it just takes four minutes to say so.
7. **Publish the 106 local-only reports**, or accept that half this project's measured history
   is invisible to anything reading the public repo.

**And one thing not to do:** do not copy cursor-paging to the reels search on the strength of a
net-new count. An invented parameter name produced *more* net-new than the real cursor.

---

## 8. PATHS

Everything this round produced, all read-only, all under `scratch/`:

```
scratch/bl1483_t1_report.md    module census, 204 rows, reachability under five policies
scratch/bl1483_t2_report.md    50 thresholds with provenance and archive re-examination
scratch/bl1483_t3_report.md    26,063 vendor key paths, fill rate, AST read column
scratch/bl1483_t4_report.md    stage-by-stage, seen-store writer inventory, runtime spies
scratch/bl1483_t5_report.md    258 settings resolved per campaign by a live-frame spy
scratch/bl1483_t6_report.md    the reserved agent's disagreement
scratch/bl1483_own_archive.md  the archive split, the missing reports, the stale claim
scratch/bl1483_self_documented.py  scratch/bl1483_selfdoc_tight.py
scratch/bl1483_skipped_tests.py    scratch/bl1483_reconcile_archive.py
scratch/bl1483_t{1..6}_*.json  the underlying data for every table above
```

The defects named in this report are still in the tree, unmodified, exactly as the brief
required.

---

## 9. THE RANKED LIST — every hole found, ordered by cost to him

**134 items: 112 MEASURED, 3 INFERRED, 15 SUSPECTED, and 4 that are measured on one axis and
inferred or suspected on another.** Counted mechanically off this table, not by hand — my own
hand-count said 131 and was wrong. Ordered by what being wrong costs, not by how interesting it
is.

### TIER 1 — costs money or pages TODAY (1–20)

| # | hole | file:line | grade |
|---:|---|---|---|
| 1 | `cut_garbage_dry_run` top `false` beats four campaigns' `true`; both dry-run gates already unlocked → the next run cuts up to 40% of the sheet live | `main.py:4865-4930`, `state.json` | **MEASURED** |
| 2 | The Control Panel prints the *campaign* dry-run value, not the effective one | `control.py:420` | **MEASURED** |
| 3 | TikTok latch never got the fix: 939 pages permanently skipped, 919 (97.9%) with no recorded reason | `tiktok_finder.py:1637-1638` | **MEASURED** |
| 4 | IG rule latch surviving the fix: 2,647 records, no expiry, no re-judge path | `meme_finder.py:7201` | **MEASURED** |
| 5 | 963 pages latched by round scripts that no longer exist in the tree | seen store, legacy records | **MEASURED** |
| 6 | The target counts pages master then refuses: 389 of 668 exist nowhere in master | `meme_finder.py:7529` | **MEASURED** |
| 7 | The docstring justifying that discard is measurably false — claims "already in master"; 58.2% are not | `meme_finder.py:7518-7521` | **MEASURED** |
| 8 | `deep_check_max_usd_per_10k` effective 30.0 against four campaigns' declared 10.0 — 3× budget | allowlist merge | **MEASURED** |
| 9 | 5 of 7 discovery producers return n=0 with an empty error on a **billed** HTTP-200 empty | `meme_finder.py:3220-3231` + 5 callers | **MEASURED** |
| 10 | That hazard is documented in the file; the fix reached the 2 observed functions, not the 5 that carry it | same | **MEASURED** |
| 11 | `min_avg_views` ships 500 against a `MIN_AVG_VIEWS = 1000` whose comment says "He named 1,000" | `config.json` vs `meme_finder.py:1204` | **MEASURED** |
| 12 | No document in 1,378 across both archives supports the shipped 500 | both archives | **MEASURED** |
| 13 | `tt_min_deep_median_views` — two readers, two effective values in the same run (0 vs 4000) | `main.py:2922` vs `quality_gate._median_floor` | **MEASURED** |
| 14 | …so the TikTok low-reach sink never fires on 4 of 5 campaigns | `main.py:2922` `or 0` | **MEASURED** |
| 15 | `cut_garbage_threshold` — top 40 selects nothing; the omitting campaign cuts at code default 20 | not in the allowlist | **MEASURED** |
| 16 | A headerless master returns `appended: 0` — byte-identical to a legitimate no-op | `crossdedup.py:457-458` | **MEASURED** |
| 17 | A failing atomic replace loses a whole batch and reports success | `crossdedup.py:516` | **MEASURED** |
| 18 | 32 of 144 offered TikTok rows (22.2% [16.2, 29.7]) refused at the master write | `crossdedup.py:419` | **MEASURED** |
| 19 | One live meme provenance: 97 rows offered, **0** appended | run provenance | **MEASURED** |
| 20 | `like_and_view_counts_disabled` unread: on 67 of 70 affected media the read `like_count` is the constant 3 | IG clips payload | **MEASURED** |

### TIER 2 — a live rule or gate is wrong, off, or unjustified (21–48)

| # | hole | file:line | grade |
|---:|---|---|---|
| 21 | `language_gate` absent from config → a gate measured at 0/26 misses and 100% coverage never runs | `meme_finder.py:6918` | **MEASURED** |
| 22 | `REJECT_AT = 80` decides no cut, is printed to the operator, and sets the preflight floor | `free_judge.py:390`, `meme_finder.py:5609-5611`, `preflight.py:148-150` | **MEASURED** |
| 23 | `KEEP_AT = 95` — same shape: measured, and its single reader writes a label that skips nothing | `meme_finder.py:4350`, `:6543` | **MEASURED** |
| 24 | `MAY_REJECT` bars of 90 applied identically in edits mode, fitted entirely on meme-question grading | `free_judge.py:239-241` | **MEASURED** |
| 25 | The file's own warning text says so, and the bars were not changed | `free_judge.py:962` | **MEASURED** |
| 26 | 48 of 50 thresholds fitted before the mode split and never re-fitted | 204-file AST sweep | **MEASURED** |
| 27 | Exactly 2 of 50 thresholds consult mode at all | `meme_finder.py:2708`, `:2098` | **MEASURED** |
| 28 | `tiktok_triage.py` contains **zero** occurrences of the word `mode` | `tiktok_triage.py` | **MEASURED** |
| 29 | `DEFAULT_MAX_DIALOGUE_SHARE = 0.10` — measured and REFUTED (0 of 623), still shipped | `meme_finder.py:1951` | **MEASURED** |
| 30 | `PAD_PAIR_NEED` + `bars_n>=4` is the only mode-re-examined rule, and 0 of his 7 graded edit pages have a bars reading | `paid_grid.py:297` | **MEASURED** |
| 31 | `DRAWN_NEED` / `DRAWN_UNIQ_MAX` — comments cite "67 pages he graded"; **no report in either archive contains either constant** | `paid_grid.py:351`, `:346` | **INFERRED** |
| 32 | `CREATOR_MIN_VIEW_FOLLOWER` / `CREATOR_EXEMPT_FOLLOWERS` — 58 justification lines, 0 archive hits, n=94 with no per-split n | `meme_finder.py:1805`, `:1932` | **INFERRED** |
| 33 | `MIN_AVG_VIEWS = 3000` (TikTok) — no denominator, no report, 6× the IG shipped value | `tiktok_finder.py:108` | **SUSPECTED** |
| 34 | `STALE_DAYS = 180` (TT) vs 152d (IG) — both pre-split; edit-page cadence never measured on either | `tiktok_triage.py:194`, `meme_finder.py:1354` | **MEASURED** |
| 35 | `MIN_SHARE_PER_PLAY` — config sets it null, i.e. OFF, while the constant is documented as live | `tiktok_triage.py:285` | **MEASURED** |
| 36 | `VIEW_GRACE_HOURS = 48` — zero comment, zero archive hits | `meme_finder.py:1208` | **SUSPECTED** |
| 37 | `NICHE_MIN_SHARE = 0.25` / `NICHE_MIN_HITS = 2` — no measurement found | `meme_finder.py:1122-3` | **SUSPECTED** |
| 38 | `DIALOGUE_MIN_CHARS = 90` — no measurement found | `meme_finder.py:980` | **SUSPECTED** |
| 39 | `NEWS_CAPTION_MIN_CHARS = 200` — no measurement found | `meme_finder.py:1024` | **SUSPECTED** |
| 40 | `FRAME_ONLY_MAX_CHARS = 69` — no measurement found | `meme_finder.py:535` | **SUSPECTED** |
| 41 | `MIN_VIDEO_SHARE = 0.7` — named in two reports, no number in either | `meme_finder.py:1424` | **SUSPECTED** |
| 42 | `NON_LATIN_FRAC = 0.15` — no measurement found | `meme_finder.py:740` | **SUSPECTED** |
| 43 | `PAGE_LANG_MIN_CALLED = 3` — no measurement found | `meme_finder.py:941` | **SUSPECTED** |
| 44 | `MIN_JUDGED_POSTS = 3` — no measurement found | `meme_finder.py:1727` | **SUSPECTED** |
| 45 | `DEFAULT_MAX_NEWS_SHARE = 0.6` — no measurement found | `meme_finder.py:1901` | **SUSPECTED** |
| 46 | `MIN_MEASURED_POSTS = 5` — no measurement found | `paid_grid.py:223` | **SUSPECTED** |
| 47 | `MIN_TILES = 3` — no measurement found | `judge_batches.py:78` | **SUSPECTED** |
| 48 | The whole `quality_gate` config surface (~120 keys) has no labelled provenance in 1,378 documents; a prior round found the same over 143 | `quality_gate.py` | **SUSPECTED** |

### TIER 3 — free money sitting in payloads already bought (49–63)

| # | hole | fill (denominator) | grade |
|---:|---|---|---|
| 49 | 100-float visual embedding unread; the project computes its own with a local model pass | 41.9–91.7% on IG user endpoints | **MEASURED** fill, **INFERRED** value |
| 50 | TikTok `video.meta` — vendor loudness, peak, quality score, watch-time distribution | **74/75 = 98.7%** | **MEASURED** |
| 51 | 105-frame scrubber storyboard unread while `clip_cuts.py` derives one with ffmpeg | **100% of 62** | **MEASURED** |
| 52 | `ig_play_count` differs from the read `play_count` on 30/371 (8.1%), by up to 493× | 100% of 371 | **MEASURED** |
| 53 | `basel_video_composition_model` — a literal cut list and text-overlay timeline | 5.1–6.9% | **MEASURED** fill, **SUSPECTED** value |
| 54 | `music.extra.beats` — beat grid and energy-trace URLs | 8/150 = 5.3% | **SUSPECTED** |
| 55 | `fifa_country_code` — a free country label | **100% of 65** | **MEASURED** |
| 56 | `top_likers[]` unread | 100% present, 47 distinct | **MEASURED** |
| 57 | `suggest_words` — discovery vocabulary, the thing captions cannot supply | 43.1% of 65 | **MEASURED** |
| 58 | TikTok `region`, `share_url`, `digg_count`, `share_count` all unread | 100% of 65 | **MEASURED** |
| 59 | `video.big_thumbs` unread | 9.2% | **MEASURED** |
| 60 | **19,851 of 26,063 key paths (76.2%) unread; 11,343 of them at 100% fill** | 42 payload families | **MEASURED** (lower bound) |
| 61 | By leaf name, only 269 of 2,986 (9.0%) are read | same | **MEASURED** (upper bound) |
| 62 | 106 leaf names appear as bare string literals and are never actually read — a grep would call all 106 alive | `clippershq/` AST | **MEASURED** |
| 63 | Embedded JSON strings hide 66 further paths in one family alone from any tree walker | TikTok + IG payloads | **MEASURED** |

### TIER 4 — correct code that is wired to nothing (64–90)

| # | hole | size / evidence | grade |
|---:|---|---|---|
| 64 | `score_sheet` — the only sheet builder that handles UNJUDGED, no production caller | 53,840 B | **MEASURED** |
| 65 | `parallel_judge` — the measured 2.95× parallel path, no production caller | 22,502 B, 9 tests | **MEASURED** |
| 66 | `song_loudness` — zero references of any kind, 7 quantified reports | 19,775 B | **MEASURED** |
| 67 | `suggest_harvest` — the `suggested` walker, and `suggested` is the only documented unjudged pool | 18,068 B | **MEASURED** |
| 68 | `track_id` — revived only by a dict key of the same spelling | 12,815 B, 6 tests | **MEASURED** |
| 69 | `triage` — revived only by function names in another module's `__all__` | 10,198 B, 11 tests | **MEASURED** |
| 70 | `mx_probe` — reachable only via other dead modules | 14,656 B | **MEASURED** |
| 71 | `page_rules` — **written 2026-08-31, zero references, never wired** | 8,181 B | **MEASURED** |
| 72 | `artist_genre_map` — marked pending, "last touched 2026-07-29 and never read" | 16,028 B | **MEASURED** |
| 73 | `artist_search` — marked pending | 26,736 B | **MEASURED** |
| 74 | `client_delivery` — marked pending, "UNRESOLVED whether the client line is real" | 10,620 B | **MEASURED** |
| 75 | `client_intake` — marked pending, same unresolved question | 10,888 B | **MEASURED** |
| 76 | `clip_cuts` — marked pending, 11 test files, no caller | 19,649 B | **MEASURED** |
| 77 | `editor_brief` — marked pending, 1,097 lines, finished at BL-1025 | 56,476 B | **MEASURED** |
| 78 | `frame_pipeline` — marked pending; sampler + phash dedup + per-frame OCR, unwired | 13,461 B | **MEASURED** |
| 79 | `hook_select` — marked pending | 9,918 B | **MEASURED** |
| 80 | `keyword_cooccurrence` — mines the master list's own confirmed editors for new keywords. No caller | 26,864 B | **MEASURED** |
| 81 | `tag_yield` — marked pending | 10,486 B | **MEASURED** |
| 82 | `two_tab_sheet` — the operator's KEPT/THROWN-AWAY sheet. Built, tested, never wired | 10,335 B | **MEASURED** |
| 83 | **The marker set is byte-identical at the pin commit (2026-08-24) and at HEAD** — 307,578 B frozen for eight days | git | **MEASURED** |
| 84 | The pin is `assertLessEqual(…, 17)`, so standing still is green forever | `tests/test_bl1389_no_caller.py:51` | **MEASURED** |
| 85 | A marked module "can never be reported" by the sweep that would otherwise find it | `tools/no_caller_sweep.py:484` | **MEASURED** |
| 86 | **The guard is RED — 4 failures of 11 tests — and the sweep exits 1: "something is untriaged right now"** | `tests/test_bl1389_no_caller.py` | **MEASURED** |
| 86b | **7 modules have no caller and no marker at all**: `dm_send_list`, `ig_embed`, `mark_reader`, `mark_sent`, `page_rules`, `suggest_harvest`, `video_strip` | derived by marker absence; matches the assertion exactly | **MEASURED** |
| 86c | **`score_sheet` reports `importers: ['sheets']` while still declaring `NO-CALLER-PENDING`** — the stale-marker blind spot the sweep documents against itself. Territory 1 reads that importer as false-alive; the two instruments disagree | `no_caller_sweep.py:484` | **MEASURED** (disagreement named) |
| 87 | `tools/facts_guard.py` — "SHOULD BE IN tools/githooks/pre-commit and is not" | marker | **MEASURED** |
| 88 | `tools/paid_write_guard.py` — "SHOULD BE ARMED", built to find branches that spend | marker | **MEASURED** |
| 89 | `tools/verdicts_merge.py` — its own docstring names it the helper every writer should use | marker | **MEASURED** |
| 90 | `rejection_store` — a writer with no reader: 65 rejections written, never once read | `rejection_store.py:222` | **MEASURED** |

### TIER 5 — instruments that cannot see what they are pointed at (91–110)

| # | hole | file:line | grade |
|---:|---|---|---|
| 91 | The decision log — built to answer "where did a dropped item go" — has **0 references** in either finder | `meme_finder.py`, `tiktok_finder.py` | **MEASURED** |
| 92 | …it logs 57,170 drops across 25 runs, all clip runs, zero page runs | decision log | **MEASURED** |
| 93 | The hashtag channel has no error counter, while search and reels both do | `meme_finder.py:5671-5673` | **MEASURED** |
| 94 | `record()` on the seen store has **zero production callers** | `meme_finder.py:277` | **MEASURED** |
| 95 | `readmitted()` is "reporting only" and has no callers | `meme_finder.py:267` | **MEASURED** |
| 96 | No expiry anywhere: no `del`, `pop` or `clear` on any seen store | four stores | **MEASURED** |
| 97 | `first_seen` / `walked` are read by two things, and **nothing compares either to now** | `exporters.py:387`, `:912` | **MEASURED** |
| 98 | The stale re-judge pass **cannot be re-run** — no `.py` producer for its markers exists on disk or in git history | 21-file follow-up sweep | **MEASURED** |
| 99 | 92 pages permanently skipped on a share the store's own schema note says must not be read | seen store | **MEASURED** |
| 100 | The language-gate latch escapes **by accident**; adding a `verdict` key buries every non-English reject | `meme_finder.py:6937` | **MEASURED** mechanism, **SUSPECTED** regression |
| 101 | 28,544 of 84,159 master identity keys (33.9%) are invisible to the funnel's skip set and fatal at the write | `crossdedup` | **MEASURED** |
| 102 | `meme_finder` has no master pre-skip at all | `meme_finder.py` | **MEASURED** |
| 103 | The dead-module count is instrument-dependent (13–18) and **no instrument is authoritative** | five policies | **MEASURED** |
| 104 | A dynamic-dispatch site orphaned 77 KB of live dashboard from the import graph | `dashboard/server.py:5575` | **MEASURED** |
| 105 | Two further dispatch sites of the same shape | `control.py:3898`, `:4645` | **MEASURED** |
| 106 | Extensionless git hooks are invisible to a `.bat`/`.sh` scan — 4 tools are live on every commit and read as dead | `tools/githooks` | **MEASURED** |
| 107 | Module stems that are ordinary English words contaminate every mention count | report search | **MEASURED** |
| 108 | 584 mark rows carry no timestamp in any field; the largest single file is 391 rows and untracked in git | `ground_truth/` | **MEASURED** |
| 109 | The no-caller sweep parses `scratch/` and quarantined third-party code; its guarding suite takes **257.8 s** | `tools/no_caller_sweep.py` | **MEASURED** runtime, **SUSPECTED** consequence |
| 109b | **The sweep crashes on a concurrent delete.** `edges_of` catches `SyntaxError` only, so a peer removing a `scratch/` file mid-walk raises an unguarded `FileNotFoundError` and kills the run — observed live during this audit | `tools/no_caller_sweep.py:263` | **MEASURED** |
| 110 | 403 quarantined third-party test files inflate any naive "tests never run" query to a false 49.6% | `quarantine/` | **MEASURED** |

### TIER 6 — configuration that selects nothing (111–124)

| # | hole | file:line | grade |
|---:|---|---|---|
| 111 | `cut_garbage_enabled` — four campaigns' explicit `false` selects nothing (the allowlist inverts it) | `main.py:4865` | **MEASURED** |
| 112 | `well_order_by_yield` — one campaign's explicit `false` selects nothing | allowlist | **MEASURED** |
| 113 | `mode` is set to the value that already equals the code default; deleting it changes nothing | both funnel blocks | **MEASURED** |
| 114 | 7 real TikTok editing terms are reachable only from a branch never selected | `tiktok_finder.editing_searches` | **MEASURED** |
| 115 | Two code comments still assert those keys are empty; they are not | `tiktok_finder.py:3090`, `page_mix.py:120` | **MEASURED** |
| 116 | 15 allowlist entries have no top-level key — the entry is a no-op | `main.py:4865` | **MEASURED** |
| 117 | 10 config keys have zero read sites anywhere, and remain editable from the Control Panel | `config.json` | **INFERRED** |
| 118 | `provenance_min` absent → the provenance gate is OFF | `repost_finder.py:1227` | **MEASURED** |
| 119 | `rejection_log_file` absent → no rejection log is written | `repost_finder.py:990` | **MEASURED** |
| 120 | `link_cost_per_call` / `gp_link_cost_per_call` absent → those calls are priced at **zero** | `control.py:1747`, `:1970` | **MEASURED** |
| 121 | `twitch_max_run_seconds` absent → no wall-clock ceiling | `control.py:2222` | **MEASURED** |
| 122 | `spotify_harvest_max_queries` is **0** in config → harvest queries off | `control.py:2593` | **MEASURED** |
| 123 | `spotify_released_within_days` is **0** in config → recency filter off | `control.py:2716` | **MEASURED** |
| 124 | 251 `or <falsy>` sites and 17 keys absent-and-read-as-off — the idiom is this project's most common hidden switch | `clippershq/`, `dashboard/` | **MEASURED** |

### TIER 7 — process and history (125–131)

| # | hole | evidence | grade |
|---:|---|---|---|
| 125 | **106 report ids exist only on this machine**, 104 of them in the newest 200, holding 5,208 measurement tokens | id diff + content probe, control passes | **MEASURED** |
| 126 | The two archives overlap on **22.6%** of their union | 329 vs 879 ids | **MEASURED** |
| 127 | Searching one archive would have wrongly called 10 (local) or 12 (public) modules unmentioned | T1 cross-check | **MEASURED** |
| 128 | Six thresholds are documented **0 local / 1 public** — invisible to a local-only search | T2 cross-check | **MEASURED** |
| 129 | **21 of 180 settled round ids (11.7%) produced no report anywhere**; 8 left working artefacts | BL-1300..1483 | **MEASURED** |
| 130 | A claim has been open 214.8 h over a round whose single declared output never appeared; nothing checks `will_write` | `.claims/`, `tools/claim.py:27-29` | **MEASURED** |
| 131 | A false pagination win is primed to be copied to the reels search — an **invented** parameter name produced more net-new than the real cursor | `meme_finder.py:3190`, `ig_client.py:596` | **MEASURED** |

**Counts, stated plainly as the brief asked: 134 items — 112 MEASURED, 3 INFERRED, 15
SUSPECTED, 4 mixed.** Every MEASURED item came from an instrument that passed a positive
control, or is reported with its control failure named. The three figures I could not reproduce
are in section 4 and are **not** in this list.
