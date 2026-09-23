# BL-1586: the full sweep. The loop that carries his judgement back has worked once and its pages are now deleted, 39% of all money went to a funnel that yielded 29 keepers, and "never contacted" was never measured

**Round:** BL-1586 · **read-only, $0.00, no vendor call** · eight territory agents in parallel, every
load-bearing claim re-derived by the orchestrator (the M-files) · store files byte-identical start to
close (see §Assertions) · paths redacted (`<Desktop>` is the OneDrive Desktop) · accounts never named ·
this file replaces the interim published at the halfway mark (same path; no second report file).

**Whose judgement.** Every rate carries one of three tags, never pooled:
- **[HIS]** his 100 grades, which are craft-cut survivors only;
- **[247]** masked labels written by an earlier agent;
- **[CUT]** the craft cut's own opinion.

## The paragraph

**What in this system is not doing what it appears to do:**

1. **The only thing that tells anyone whether the output is good is his grading. It has returned once:**
   5 review pages (423 cards) asked, 1 page (100 cards) answered, with a reason on 0 of them. The four
   pages still waiting on him, and the manifests needed to score them, are **gone from the Desktop**;
   only the one page that was already graded had been vaulted.
2. **Every stage that decides what he sees is round-numbered scratch code.** The craft cut, the dedup
   wiring, the delivery and the sheet are re-copied each round with no test, and nothing has written
   his actual workbook since 2026-09-21.
3. **The standing fact "not one address ever contacted" was never measured.** The repo's own
   `docs/NO_SEND.md:13` says he runs a separate tool that sends leads daily. Master holds no
   outcome only because nothing ever fed that tool's log back.

**The single hole that costs him most is the broken grading loop.** It is the only route to the
~616 [420–883] editors [247] the cut hides on TikTok, and to any Instagram loss number at all, and
it now has no pages to grade.

**What he should do next, in order, all at $0:**
1. Answer one question: has his sending tool mailed addresses from these sheets, and can it export
   who replied? If yes, `outcomes.mark_sent_from_csv` already exists to take it, and every proxy in
   this project can be checked against real replies for the first time.
2. Grade one freshly generated page, which must be vaulted, page **and** manifest, the moment it is
   written.
3. Plug in the backup drive. The scheduled off-machine backup has failed every night.

## 1. Territory 1: computed, declared or documented, and never read

Every deadness verdict is an **upper bound**: leaf-name matching cannot see a runtime-assembled name.
Two false-deads from exactly that were caught this round and are logged under Dead ends. Planted
controls (`bl1586_planted_unread` columns, config keys and attributes) fired in every census, and
known-live names (`email`, `spend_cap_usd`) read as live.

**(b) Dead and DANGEROUS: it reads like a live safety check.**

| finding | where | AST / grep | what it costs |
|---|---|---|---|
| `money_off_the_books()` has **0 callers**. It was written by BL-1451 to surface "the two counters nobody read" (`write_failures`, `unmetered_calls`) [T1a_01] | `spend_ledger.py:1121` | grep over all tracked code: the definition only (other hits are copies in `scratch/`); AST agrees. Orchestrator re-grep confirms | the silent off-the-books failure BL-1451 thought it had closed is still silent |
| `spend_ledger.CAP_ANOMALIES` counts malformed or negative caps, with **0 production readers** [T5_07] | `spend_ledger.py` | AST + grep | a config typo yields an uncapped lifetime run with no visible signal; $0 today (current caps are sane) |
| `DedupGuard` ("no duplicate ever reaches the operator") has **0 production callers** [T1b_04, T2_03] | `dedup_guard.py:103` | AST + grep agree | **orchestrator correction:** it DID run on his last walk, because `scratch/bl1584/walk.py:113,144,195` wired it. See M01 |
| the client-half modules (`client_intake`, `client_delivery`, `editor_assignment`, `editor_brief`) have validators run only by `tests/` [T1b_03] | four modules | AST BFS + grep + `tools/no_caller_sweep.py:379` | none while the client half is idle (T4: silent 24–54+ days) |

**(c) Dead and VALUABLE: wiring it would help.**

| finding | where | why it would help |
|---|---|---|
| `page_rules` encodes his own quoted rule (*"at least 50-60% of the videos have to be the kind we're looking for… last post two years ago, that's dead"*) and has **0 production callers** [T2_02] | `clippershq/page_rules.py` | the share-of-videos half of his rule runs nowhere; the recency half has a substitute (`tiktok_triage`) |
| `email_harvester` computes `editor_gate_hits` / `editor_class_counts` per tag and never prints or reads them back [T1a_04] | `email_harvester.py:871-890` | the per-tag editor yield, his priority number, is computed free and thrown away |
| four master columns are computed, varying, and read by nothing [T1a_03]: `editor_signals` (55,798 rows), `theme_match` (55,808), `dominant_lang` (12,763), `spotify_followers` (12,763) | writer build sites | `spotify_followers`' own comment documents a measured 52× loyalty spread that was never wired |
| `triage.py`, the judge's token-cost guard, has no caller and no test, by its own docstring [T1b_06] | `clippershq/triage.py`, `judge_batches.py:14` | judge spend is small today (FREE_JUDGE $3.75 lifetime, §3), so this is low value now |
| Instagram's "paid" stage counter `ig_client.profile_calls` has **0 readers**, and `run.py::STAGE_KEYS` has no Instagram entry [T1a_02] | `ig_client.py`, `run.py` | Instagram's per-profile cost stays uncomputable |

**(a) Dead and harmless: leave it.**
- 15 fully dead modules, mostly manual CLI tools that already say they are orphaned [T1b_01].
- 68 test-only modules [T1b_01].
- Two config keys that are decoys of live knobs under other names (`meme_page_cap_per_tag`,
  `meme_max_profiles_per_run`, already in `KNOWN_UNUSED`); config has **no new drift** [T1a_05].
- `ig_client.clips_fallbacks` is logged but never summarised [T1a_06].
- `main.py`'s stranded niche/quality/vision stack [T2_01].
- The 25 zero-filled master columns BL-1585 already listed, including all nine outcome columns.

## 2. Territory 2: every gate on his path

**His actual path, traced [T2_04, M01]:**
1. `scratch/bl158x/walk.py` wires the guard and walks tags through `email_harvester`, which classifies
   `editor_class` and removes nothing.
2. The rows land in a scratch JSONL.
3. `scratch/.../deliver.py` stamps `craft_cut` / `review_hold` and appends through
   `crossdedup.append_leads`, which re-stamps `editor_class` and writes master.
4. `scratch/.../sheet.py` writes a one-off Desktop `.xlsx`.

No production launcher reaches `email_harvester` (T1b's AST reachability from every launcher, plus
grep; `harvest_run.py` is the paste-box, not the hashtag walk).

| gate | on his path? | removes | measured by | owner / test |
|---|---|---|---|---|
| the tag list | yes (scratch walker) | tags chosen per round | [CUT] only | none |
| `DedupGuard` | **yes, only because a scratch walker wires it** | already-owned accounts and addresses | the walker's polarity control | tested module; wiring untested |
| `editor_gate.classify` | stamps at all 3 chokepoints, removes nothing [T2_00] | nothing | [247] 94.67% recall (gate) | tested |
| craft cut (`bio_rule`) | **scratch only** | 78% of TikTok and 93% of Instagram addressed rows | [247] editor loss 23/109 = 21.1% [14.5–29.7]; [HIS] false pass 8.0% TikTok / 26.0% Instagram | no test in `tests/` |
| `review_hold` | scratch only | nothing (parks) | none | none |
| `looks_agency` | **no** (3 modules, all send-side) | nothing | [HIS] fires on 0/17 rejects | tested module |
| creator gate `garbage_cut_reason` | **no** (only `main.py:3484`) | nothing | untestable offline | tested module |
| `page_rules` | **no** (0 callers) | nothing | none | own test only |
| `exporters.check_operator_columns` | scratch sheet scripts only [T1b_05] | nothing (contract check) | none | tests |

## 3. Territory 3: the clipper path priced, and where the money went

**The clipper path's entire cost is one stage: the hashtag page fetch** [T3_07]. Dedup, bio, address,
the editor gate and the craft cut are all free. T3 re-derived BL-1584's $7.43 and BL-1583's $15.89
per 1,000 KEEP exactly from raw `walk_state.json`.

**Where the lifetime $84.42 went** (spend.json: 39,107 rows; row sum == header total; orchestrator
re-derivation M03):

| campaign | dollars | share of dollars | share of rows | what it served |
|---|---:|---:|---:|---|
| MEME_FINDER | $22.08 | 26.2% | 6.4% | meme-page funnel |
| SPOTIFY_FINDER | $9.49 | 11.2% | 7.2% | client half (musicians) |
| TIKTOK_FINDER | $7.22 | 8.5% | 1.8% | meme-page funnel |
| FREE_JUDGE | $3.75 | **4.4%** | **76.5%** | meme-page funnel only; **0 call sites on the clipper path** [T3_02] |

- **The brief's "77.4% of the ledger is FREE_JUDGE" is a row share, not a dollar share** [T3_01, M03].
  FREE_JUDGE is the sixth-largest spender by dollars. Its biggest line, `glm-5.3-flash` $1.63, is
  priced from a figure the code calls "probably LOW" (`free_judge.py:314-320`) [T3_08]. Even doubled,
  it moves nothing that matters.
- **The meme-page funnel took $33.05, 39.1% of every dollar ever spent, for 29 KEEP rows.** That is
  about $1.14 per KEEP, against $0.0074 per KEEP on BL-1584's editor walk. It has been idle 17 days
  and is still enabled [T3_03]. FREE_JUDGE also spent $1.29 during 8 days after both its funnels went
  idle: calibration money, not production [T3_06].
- **Funnels nobody can judge.** 328 addressed rows from google_play, twitch, youtube and kick carry
  **no bio**, so the craft cut can never run. They sit as permanent HOLD, their funnels still enabled
  and 53+ days stale [T3_05]. Keeping them costs nothing while idle; running them buys rows no one
  can judge.

## 4. Territory 4: the client side, first audit in twenty rounds

- **The client label is real, unlike the clipper one** [T4_01, T4_05]: 15,173 rows stamped
  `lead_kind=client` explicitly by their own funnels; 8,719 addressed = 57.46% [56.68–58.25].
  `docs/FACTS.md` reproduces; the brief's "10,164" does not reproduce under any definition tried.
  The clipper catch-all everyone cites as `writer.py:363-367` is now at `writer.py:443-446`.
- **All five client funnels are wired and launchable, and all have been silent 24–54+ days.** The last
  client row is dated 2026-08-30 [T4_03].
- **Nothing judges client output.** No file in `ground_truth/` grades a client, meme-page or
  Spotify/Twitch/YouTube row. "Is this client worth pitching?" is **untestable**, not untested
  [T4_04, T4_05].
- **One live mislabel:** `meme_finder.py:8913` hardcodes `"lead_kind": "clipper"` on meme pages. It was
  diagnosed by BL-1445 and BL-1432 and never fixed; 8 rows since 08-31. `meme_send_list.is_meme_row`
  still routes them correctly, but every census by `lead_kind` is wrong [T4_02; orchestrator read the line].
- **Spotify:** $9.49 spent, 12 KEEP among 15,173 client rows, 0 KEEP among Spotify-sourced rows [T3_04].
  KEEP is the editor craft cut, which is the wrong question for a client. So this says the Spotify
  rows are not editors, which nobody expected them to be, and nothing about whether they are good
  clients.

## 5. Territory 5: the guards on money and safety

- **Caps: three sites still read a declared 0 as "no cap"** [T5_01; orchestrator read each line in M03]:
  - `youtube_finder.py:1474-1479` filters `0` out of its cap list, so a declared `spend_cap_usd: 0`
    ("stop everything") falls back to the $5 default. `control.py:4257-4261` passes `None` for 0.
  - `repost_finder.py:1025-1026`: `if max_usd and …`, so 0 means unbounded, at a real $0.0006 per call.
  - `google_play_finder` has the same shape, dormant because its price is $0.
- **Booking still depends on the caller** [T5_02]:
  - `email_harvester`'s own documented CLI (`:996`) never passes `campaign=`, so running it as its
    docstring says books $0.
  - `caption_finder.py:1110-1134` books only after `run()` returns, with no `try/finally`.
- **The Instagram budget runs out $1.88 early.** BL-1573's misbooking is still in the headers:
  `ig_spent_usd` header $55.864276 vs row sum $53.983663; TikTok header $17.282224 vs rows $18.916024.
  `main.py:1253` gates Instagram on the header [T5_02, M03].
- **The suite sandbox holds** [T5_03]: statically structural, and one exactly named suite run moved 0
  of 1,266 store files.
- **The `sum(sessions)` false alarm** (`scratch/bl1584/walk.py:223`) repeats in every round's copied
  walker and is not in production code [T5_04].
- **Backups: the scheduled off-machine backup has failed every night.** Task `\ClippersHQ-Backup`, last
  result **2**, targets `E:\clippershq-backups`, and `E:` is not attached. T6 reads its log as 52 of 52
  nights failed since 2026-08-03 [T6_01; orchestrator confirmed the task state]. Copies of master:

  | copy | rows | as of |
  |---|---:|---|
  | live | 75,540 | now |
  | `.bak` / `backups_bl1584/` | 74,732 | 09-22 |
  | vault D: | 74,218 | 09-20 |
  | vault LOCAL | 65,132 | 08-29 |

  The 808 BL-1584 rows are in no copy of master, but can be rebuilt from
  `scratch/bl1584/walk_rows.jsonl`, which is correction to T5_05's "irreplaceable" (M03). Every copy
  except the stale D: vault is on C:, inside OneDrive.
- **Tag ledger:** its 51 uncommitted tags exist only in the working tree; both vaults are stale by the
  same margin. No code path reverts it automatically [T5_05].
- **The four review pages** gone from the Desktop were never vaulted [F00]. The reports clone had also
  been moved off the Desktop, the fourth time it has vanished from where a round left it.

## 6. Territory 6: what could be deleted, and what must not be

**Recommend only; this round deleted nothing.**
- **Disk has not regrown:** the repo is 29.17 GB, flat since BL-1574's reclaim, and `output/` shrank
  [T6_02].
- **Candidates:**
  - `quarantine/20260816_113854`, 826 MB, already approved for deletion in BL-1574: finish it with
    `outputs_gc.py --expire` [T6_04].
  - 1.81 GB of exact-duplicate files in `output/`, recoverable with `outputs_gc.py --apply` [T6_05].
  - The idle meme-page, Spotify and bio-less funnels: **disable, do not delete** (§3).
- **Tools that do less than their code can:** the scheduled `outputs_gc` never passes `--apply`, and
  `backup_prune` never passes `--config-backups` / `--backups-dir` (~1.5 GB unpruned). Both no-op if
  nobody is logged in at 04:30 [T6_03].
- **Deleted outside the sanctioned tools:** about 44 tracked `outputs_*` files were deleted from the
  working tree by something other than the GC tools [T6_08].
- **MUST NOT be deleted** [T6_06]:
  - master's **CUT rows**, the only route back to ~616 hidden editors;
  - the disabled tags (`_default_hashtags_disabled_*`), one edit from returning;
  - `scratch/bl1568` and `scratch/bl1569`, the [247] labels and the only labelled sample containing
    cut rows (protected today by file type, not by name: tighten that);
  - `ground_truth/`, the vaults, `spend.json` history and the tag ledger.

  No load-bearing file is currently eligible for automated deletion.
- **Not a candidate:** the root `master_leads.csv.*.bak` pile (953 MB, 39 files) is already governed by
  a working, scheduled `backup_prune` [T6_07].

## 7. Territory 7: the reserved agent, told to disagree with the brief

1. **The grading loop's throughput is one page** [T7_01]. The pace is 16 rounds in 7 days, and 8 of the
   last 8 reports turn on his grades. MARK is filled on 0 of 3,028 workbook rows. Three decisions are
   now tied to files that no longer exist: the Instagram buying pause (its rule names the deleted
   50-card page), BL-1585's recommendation, and "dm for" ranking.
2. **"Never contacted" is a label, not a measurement** [T7_02]. BL-1559 said it could not prove it.
   10 of the 26 reports since state it as fact, and 0 carry the caveat. His sending tool
   (`NO_SEND.md:13`) may hold the reply data every rate here is a proxy for. **Every rate in this
   project, KEEP %, editor loss and $ per 1,000, is a proxy for "would this person do paid editing
   work for him", which nobody here has measured.**
3. **His EDITOR grade does not mean "for hire"** [T7_03]. Only 32 of the 82 accounts he graded EDITOR,
   39.0% [29.2–49.8] [HIS], show any for-hire wording in their bio (a deliberately broad pattern). "Faceless" and
   "available for paid work", the two words of his goal, are recorded nowhere. **This is not a cut**:
   cutting on it would drop 61% of his editors.

## 8. What I got wrong

1. **I stated "not one address ever contacted" as fact**, in BL-1585's report and in this round's own
   agent rules. `docs/NO_SEND.md:13` says the opposite is plausible. The reserved agent caught it;
   I should have, because the file is in this repo.
2. **I passed the brief's "FREE_JUDGE is 77.4% of the ledger, the biggest spender" to the agents
   unverified.** It is 76.5% of rows and 4.4% of dollars. The biggest spender is the meme-page funnel.
3. **In BL-1584 I generated a review page and a KEEP sheet on the Desktop and vaulted neither.** In
   BL-1585 I then made "grade the cards on your Desktop" the single recommendation. Both files are now
   gone, and the recommendation died with them.
4. **Two agent verdicts would have shipped as DANGEROUS without re-measurement.** "DedupGuard is
   inert" is false on his path (M01). "The weak normaliser lets duplicates through" found 0 on 15,583
   real addresses (M02). A third, "1,322 irreplaceable rows", was overstated (M03). The interim report
   also listed the idle client modules as DANGEROUS before T4 showed the client half has been idle
   for weeks. That is downgraded above.
5. **Two agents breached the no-identifier rule inside their own work.** T7 printed about a dozen short
   bio strings to its tool output, not to any file. T6 wrote handle-shaped filenames into a scratch
   JSON and redacted them before finishing. Both were disclosed by the agents; neither reached a
   finding file or this report (leak scan below).
6. **I published the interim with 4 of 8 territories, while two more had already returned.** It was
   honest about what it held, but it was staler than it needed to be.
7. **The round baseline is 35 store files, not the 44 the brief names.** The 9 missing ones were gone
   before the round began (F00), so "byte-identical at close" covers the 35 that exist.

## Dead ends, logged so nobody repeats them

- **Already fixed; the brief's examples are stale:** `unexpected_status_count` and
  `JUDGE_RULES_NEEDING_PROFILE` are wired now (BL-1567 / BL-1580) [T1a].
- **False-deads from dynamic access, not dead:** `total_likes`, `videos_sampled` and 7 `send_guard`
  counters are read through `row.get(col)` loops [T1a]. `teach_routes`, `paste_routes`,
  `dropmark_routes`, `meme_send_list` and `tiktok_send_list` are imported via
  `__import__(string)` at `dashboard/server.py:5662` and `control.py:4088` [T1b_02].
- **The weak address normaliser:** 0 real duplicates missed (M02). 142 addresses appear on 2+ tokens,
  cause not measured.
- **The unbound-name / NameError sweep over 224 modules** found zero hits, with a control that
  fires [T1b_07].
- **Fine as they are:** the suite sandbox [T5_03]; disk regrowth, refuted [T6_02]; the `.bak` pile
  [T6_07]; config drift, none [T1a_05]; google_play's $0 is a real zero; send-list wiring was fixed at
  BL-1283; `editor_gate.classify` is wired at all 3 chokepoints [T2, T4].
- **Unmeasurable without an outside call or his input:**
  - whether he deleted the pages himself;
  - OneDrive's online recycle bin (a network call, named, not made);
  - whether his tool ever mailed these addresses;
  - time per graded card (all 100 grades carry one ingest timestamp).
- **Not traced this round (UNCHECKED, not cleared):** repost / youtube exception safety [T5]; `presort.verdict_of` [T2].

## Ranked by what it costs him

| # | hole | cost | what fixes it |
|---:|---|---|---|
| 1 | the grading loop has returned once, and its 4 pending pages + manifests are deleted, unvaulted [F00, T7_01] | **editors**: the only route to the ~616 [420–883] hidden TikTok editors [247] and to any Instagram loss number; Instagram buying paused indefinitely | a fresh page, vaulted with its manifest at generation; he grades it |
| 2 | the scheduled off-machine backup has failed every night; every other copy is on C: [T6_01, M03] | **the whole corpus**: 75,540 rows, $84.42 of purchases | attach the backup drive, or point the task at `D:` |
| 3 | "never contacted" unmeasured; his sender's replies never fed back [T7_02] | **hours**: 27 rounds tuning proxies for an outcome that may already be recorded on his side | one question to him; the intake exists (`outcomes.py:345`) |
| 4 | the meme-page funnel took 39.1% of all dollars for 29 KEEP, and is still enabled [T3_03] | **$33.05 so far**, about $1.14 per KEEP vs $0.0074 on the editor walk | disable it (do not delete) until something can judge its output |
| 5 | a declared $0 cap is ignored by the YouTube and repost funnels [T5_01] | **dollars, unbounded** on a run he believed stopped | route both through the resolver |
| 6 | Instagram gated on a header over-booked by $1.88 [T5_02] | **$1.88** of Instagram budget | re-derive headers from rows |
| 7 | his workbook not written since 09-21; 1,322 delivered rows only in one-off sheets, one now deleted [T2_04] | **hours** for him reconciling sheets; 808 KEEP-bearing rows not in front of him | one tracked delivery tool that writes his workbook |
| 8 | his path is scratch code, re-copied per round [M01] | **editors and dollars indirectly**: how craft_cut, looks_agency and the creator gate hid for weeks | promote walker, deliver and sheet to tracked, tested modules |
| 9 | `money_off_the_books` and `CAP_ANOMALIES` read by nothing; the booking gaps in `email_harvester` CLI and `caption_finder` [T1a_01, T5_07, T5_02] | **dollars, silent**; $0 measured today | wire one reader into the run summary |
| 10 | "editor" ≠ "for hire"; "faceless" recorded nowhere [T7_03] | **his outreach time** on the ~61% with no hire signal | a grading button that can say "edits, not for hire" |

## Assertions at close

```
store files (the 35 that exist at round start):  diff start -> end: 35 vs 35 files, 0 moved
wide snapshot (seen stores, config.backups, ground_truth, pages):  diff start -> end: 1266 vs 1266 files, 0 moved
suites: one, named exactly by T5, snapshot-wrapped: 0 of 1,266 moved; no full-suite run
vendor / network calls: 0 (the reports clone was re-cloned with gh; the publish is a push)
files written outside scratch/bl1586/: this report only (checked by mtime against the start snapshot)
```
