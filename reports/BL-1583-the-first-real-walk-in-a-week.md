# BL-1583 — $1.65 bought 514 addresses and 104 clean ones: tool-word hashtags run at 32.6% KEEP, "title + edit" at 6.8%, and 1,000 clean emails now cost $15.89 instead of $29.82

**Round:** BL-1583 · **Spent: $1.652400** of a $3.00 hard cap (55.1%), all TikTok, `ig_usd`
$0.000000 on every booked row — Instagram buying stays paused pending his 50 Instagram grades. ·
Paths redacted: `<PROFILE>` is the user folder, `<Desktop>` the OneDrive Desktop. · Hashtags are
named; accounts never are. · The two review pages and their manifests are byte-identical to their
start hashes; the workbook and the MARK column were not touched.

## The paragraph

**The walk cost $1.6524 and produced 514 new addressed TikTok rows, 104 of which survive the craft
cut** — and it did it at **$15.89 and 16.3 hours per 1,000 delivered addresses against the $29.82
and 30.2 hours BL-1581 measured**, 1.88× cheaper and 1.85× faster. **Under the rule written and
committed before the first paid call the result is INCONCLUSIVE**: pooled KEEP on the new rows is
**20.2% [17.0–23.9]**, which straddles the 15–20% band, and at that rate no amount of extra volume
clears it — the lower bound would need 182,428 rows and the upper bound never falls below 15%. The
set has to change, and the per-tag table says exactly how: the three groups the plan named before
the walk came apart cleanly. **Tool-word tags — aftereffectsedit, velocityedit, alightmotionedit,
capcutedit — run at 32.6% [25.1–41.0]**, above BL-1582's 28.8% baseline, with `aftereffectsedit`
alone at **68.6% [52.0–81.4]** on 35 addressed rows, the best tag this project has measured.
**Character/franchise tags run at 18.3% [14.4–23.0]**. And **"<title>edit" variants run at 6.8%
[2.9–14.9]** — barely above the 3.4% title-only floor, so **bolting "edit" onto a title tag does
not turn it into an editor tag**; that half of the experiment is refuted, cheaply. The 13 dead
title-only tags are disabled, not deleted, in the one campaign that owned all of them (PANICBABY),
recorded with their counts and provenance so undoing it is one step; the whole-document config diff
is exactly two keys and all five campaigns are intact. The new rows went into master through the
locked `crossdedup.append_leads` path after a sha-verified backup (74,218 → 74,732 rows, still 76
columns), 71 of them carrying `review_hold: custom-domain`. His 104 clean rows are on the Desktop
as a sheet, and an 86-card three-button page over **this walk's rows only** — 60 survivors / 6 held
/ 20 cut, stratum hidden, zero overlap with anything he has already graded — is waiting. Nothing
was ingested this round: neither page's results file exists yet. Every KEEP number here is the
craft cut's opinion, and the craft cut fails 14.8% [10.1–21.3] of labelled TikTok editors — **his
grades on that new page are the real test.**

## 1. What this project is, for a reader with no context

ClippersHQ walks TikTok hashtags, keeps the accounts whose bio shows they edit video for other
people, and delivers their addresses to one operator who wants "no creators, no businesses, fast
pace for 1,000 emails" — under the standing rule that a real editor is never wrongly cut. BL-1582
measured that hashtags carrying editing vocabulary in the tag itself yield 28.8% [27.0–30.6] under
that cut while title-only tags yield 3.4%, and proposed dropping the dead ones and testing fresh
"edit" tags. This round did both, for $1.65.

## 2. Part 0 — his grades

**Neither results file exists.** The two open pages download as `review_20260921_152635_results.csv`
(87 cards) and `review_20260921_202836_results.csv` (50 Instagram cards); neither is in `output/`,
on either Desktop, in Downloads, Documents or `Random/`. The only results file on disk is the
BL-1572 one already ingested on 2026-09-21. Nothing was ingested, the label store is unchanged at
100 rows, and the Instagram decision rule (≥22 EDITOR → burning, 0 → thin, 1–21 → inconclusive)
still has nothing to decide on. This did not block the walk.

## 3. Part 1 — the 13 dead tags, disabled reversibly

All 13 sat on **PANICBABY's `default_hashtags`**, once each — the survey checked every campaign
list and every top-level list first. They moved into `PANICBABY._default_hashtags_disabled_<round>`,
following the convention config.json already carries (`_meme_hashtags_dropped_bl1404`), each entry
holding its campaign, its list, its master counts and the reason. Config was read as raw JSON (never
through `load_config`, which rewrites path values), asserted to round-trip byte-identically before
any edit, and written under `filelock` with tmp + fsync + rename, after two sha-verified backups.

| | |
|---|---|
| PANICBABY `default_hashtags` | 1,811 → 1,798 tags |
| new key | `_default_hashtags_disabled_<round>`, 13 entries |
| whole-document diff | exactly `.campaigns.PANICBABY.default_hashtags` and `.campaigns.PANICBABY._default_hashtags_disabled_<round>` |
| campaigns | ANIME15K, DAYLIGHT, PANICBABY, STRAENGE, ZHUS — all intact |

The 13, with the master counts that condemned them (≥20 addressed rows, **0** KEEP): eternalsunshine
38, midnightsun 35, wutheringheights 28, lalaland 26, tellmelies 25, itendswithus 24, moulinrouge 24,
conversationswithfriends 23, casablanca 22, maxtonhall 21, dearjohn 20, outlander 20, thegreatgatsby 20.

## 4. Part 2 — the walk: money, discipline, and what was pre-registered

**Written and committed before the first paid call** (commit `264b4edd`): the decision rule, the tag
plan and the cap proof. The rule: pooled KEEP of the new addressed rows against the 28.8%
[27.0–30.6] baseline — lower Wilson bound above 20% adopt, upper below 15% reject, between
inconclusive; per-tag verdicts only at n ≥ 20; walk order randomised with seed 1583 because BL-1582
measured KEEP falling 22.5% → 10.4% across walk-order quartiles.

**The set:** BL-1582's 19 candidates plus 10 `<title>edit` variants of PANICBABY's most-addressed
title-only tags that are not among the 13, minus one duplicate = **28 tags**, none of them in the
TagLedger (checked by value, not memory). **Estimate printed before the first call:** 28 tags ×
≤ 120 pages × 1.0104 calls/page + 28 resolves ≤ 3,423 calls × $0.00060000 (`api.cost_per_call_usd`,
by named key) = **≤ $2.0538**, 68% of the cap.

**The cap, driven, with `cap_proof.json` on disk before any prose about it:** a funded $0.05 cap
grants 10 reserves and the meter advances to $0.006000; a **$0.00 cap REFUSES and the meter does not
move** (`calls 0→0, spent $0.000000`); a cap with exactly 3 calls of room grants 3 and **refuses the
4th, with the meter stopped at 3 × unit**. All four cases PASS.

**The screen he sees before spending**, quoted from the real entry point driven with the vendor
mocked and every socket refused:

```
   | Estimated cost  : ~$1.04   (estimate — actual may vary with lead density; hard-capped below)
   | Per 1,000 DELIVERED (after the craft cut): ~$29.82 and ~30.2 h  -- from 3 counted run(s) (2026-09-16): 185 delivered of 1,052 addressed; the run estimate above prices calls, not addresses
   | Spend cap       : $100.00  ($17.39 left after this run)
```

**The money, counted two ways and agreeing:** the ledger holds 28 rows for `run_id` bl1583 —
**2,754 calls, $1.652400, all `tiktok_usd`, `ig_usd` $0.000000**; pages 2,726 + 28 hashtag-id
resolves = **2,754 calls × $0.00060000 = $1.652400**. `spend.json`'s totals moved by exactly
$1.652400 and by nothing else.

**What the kill cost, and what it exposed.** The host stopped the walker for low memory after 7
tags. The notice was checked, not believed: `Get-Process` said PID 38352 was dead (never `kill -0`,
which cannot see a native Windows PID), the checkpoint was intact and the lock had been left behind
on purpose. On resume, tag 8 completed and **`calls_booked` did not move** — `prior_calls` summed the
checkpoint's `sessions` list, which a kill leaves empty, so the booking delta went negative and
**$0.0726 of real spend went off the books**, the same shape as BL-1557 and BL-1563. The walker's own
tripwire (cumulative $ printed beside the booked count) showed it within one tag. The walk was
stopped, `prior_calls` changed to `max(sum(sessions), calls_booked)` — the ledger is authoritative
for what is already booked — the 121 missing calls were booked by a reconciliation whose number was
derived twice from disk (the session's own counter, and pages + 1 resolve) before it would write,
and only then did the walk resume. At the end the tripwire fired once more, and this time the
*counter* was the wrong side: `sum(sessions)` was missing the killed session's 620 calls, while the
ledger and the pages-plus-resolves derivation both said 2,754.

## 5. Part 3 — delivery

516 rows on disk → 514 built (2 dropped: the account was already in master, so **no existing bio
could be touched**; 0 dropped for held addresses). Judged exactly as master's rows are — no address
→ blank, address + no bio → HOLD (unknown is not a cut), `bio_rule` true → KEEP, else CUT — and
stamped with `review_hold` by BL-1579's rule. Appended through **`crossdedup.append_leads`
(crossdedup.py:548, `filelock` at :572)**, never the unlocked scratch append, after a sha-verified
backup into `backups_bl1583/`.

| | |
|---|---|
| master | 74,218 → **74,732** rows (+514), header still == `FULL_COLUMNS` (76) |
| craft cut on the new rows | KEEP **104**, CUT 410, HOLD 0 |
| `review_hold` | `custom-domain` on 71 rows (Instagram-only `fanpage-words` cannot fire on a TikTok walk) |
| `append_leads` | `{'appended': 514, 'merged': 0}` |
| sheet | 104 KEEP rows, newest first, clickable profile links — `<Desktop>/BL-1583_new_keeps.xlsx` |
| page | 86 cards over **this walk's rows only**: 60 survivor / 6 held / 20 cut, stratum hidden, overlap with graded or open pages **0** |

## 6. Part 4 — the numbers

Denominators: **514 addressed rows** delivered by this walk; 17,810 accounts seen; 542 addresses seen
by the walker, 518 net-new after dedup; 28 of 28 planned tags attempted; 2,726 pages in 101.7 minutes
of walk clock (26.8 pages/min) from the walkers' own epoch stamps, never the ledger's booking times.

| | this walk | BL-1581's counted runs |
|---|---|---|
| $ per 1,000 delivered (KEEP) | **$15.89** | $29.82 |
| hours per 1,000 delivered | **16.3 h** | 30.2 h |
| calls per addressed row | 5.4 | 8.7 |
| calls per delivered row | 26.5 | 49.7 |

**Pooled KEEP: 104 / 514 = 20.2% [17.0–23.9]** against the 28.8% [27.0–30.6] baseline →
**INCONCLUSIVE** under the pre-registered rule. The three groups the plan named beforehand:

| group | tags | addressed | KEEP | KEEP % [Wilson] |
|---|---|---|---|---|
| tool word in the tag | 4 | 129 | 42 | **32.6 [25.1–41.0]** |
| character / franchise + edit | 15 | 311 | 57 | 18.3 [14.4–23.0] |
| `<title>edit` variant of a title-only tag | 6 | 74 | 5 | **6.8 [2.9–14.9]** |

Per tag, verdicts only at n ≥ 20 addressed:

| tag | pages | accounts | addressed | KEEP | CUT | KEEP % [Wilson] | $ |
|---|---|---|---|---|---|---|---|
| aftereffectsedit | 120 | 770 | 35 | 24 | 11 | **68.6 [52.0–81.4]** | 0.0726 |
| dexteredit | 120 | 907 | 29 | 13 | 16 | 44.8 [28.4–62.5] | 0.0726 |
| velocityedit | 120 | 851 | 29 | 10 | 19 | 34.5 [19.9–52.7] | 0.0726 |
| oshinokoedit | 120 | 792 | 23 | 6 | 17 | 26.1 [12.5–46.5] | 0.0726 |
| outerbanksedit | 120 | 705 | 24 | 5 | 19 | 20.8 [9.2–40.5] | 0.0726 |
| thevampirediariesedit | 120 | 576 | 32 | 4 | 28 | 12.5 [5.0–28.1] | 0.0726 |
| insideoutedit | 120 | 821 | 26 | 3 | 23 | 11.5 [4.0–29.0] | 0.0726 |
| capcutedit | 120 | 1,048 | 57 | 5 | 52 | 8.8 [3.8–18.9] | 0.0726 |
| thesummeriturnedprettyedit | 120 | 604 | 52 | 3 | 49 | 5.8 [2.0–15.6] | 0.0726 |
| bridgertonedit | 120 | 676 | 37 | 2 | 35 | 5.4 [1.5–17.7] | 0.0726 |
| thelastofusedit | 120 | 835 | 25 | 1 | 24 | 4.0 [0.7–19.5] | 0.0726 |

(tags below n = 20 are listed without a verdict in `scratch/bl1583/walk_numbers.out`; the strongest
of them are bladeedit 9/19, alightmotionedit 3/8, thanosedit 4/11. Three tags produced no addressed
row at all; `maquiatiktokedit` does not resolve — 500 from the vendor, 1 call, $0.0006.)

**`capcutedit` is the finding inside the finding:** it drew the most accounts of any tag (1,048) and
the most addresses (57), and yields 8.8% [3.8–18.9] — the tool every creator uses is a creator tag,
exactly as the candidate list warned. `aftereffectsedit`, the tool only editors use, is the best tag
in the table. That is the shape worth extending: **not "edit", but the vocabulary of professional
tooling.**

**The spend screen now reads**, counted at runtime including this walk:
`~$24.81 and ~25.1 h -- from 4 counted run(s) (2026-09-16..2026-09-22): 289 delivered of 1,566
addressed`.

## 7. What I got wrong

1. **The resume booked nothing and put $0.0726 off the books.** `prior_calls` summed a `sessions`
   list that a kill leaves empty, so the delta against `calls_booked` went negative. Found by the
   walker's own tripwire within one tag, fixed at the source (`max(sum(sessions), calls_booked)`),
   and reconciled with a number derived twice before it would write. The defect is BL-1557's and
   BL-1563's, reappearing in the *resume* path that was built to prevent it.
2. **I named a scratch script `numbers.py`**, which shadows the stdlib module for anything run from
   that directory — openpyxl failed on import in the delivery script. This project has been bitten
   by exactly this before (`fastpath_numbers.py`). Renamed to `walk_numbers.py`.
3. **The first cap-proof verdict logic was wrong**, marking a correct budget FAIL: it expected the
   meter not to advance on a case where three of four reserves were legitimately granted. The
   checker was fixed, not the budget.
4. **The pre-registered rule cannot be settled by volume at the observed rate** — I wrote a band
   whose middle is where a mixed set of tags lands. The honest arithmetic is in §6 (182,428 rows for
   the lower bound, never for the upper); the fix is not more rows but a narrower set, which the
   subgroup table gives.
5. **Two monitors watched one walk** for a while, duplicating every progress line. Harmless, noisy,
   stopped.
6. **The leak scan flagged two tokens in this report, both adjudicated by value and both benign:**
   a hashtag that looks handle-shaped (105 rows in master carry it as `tt:hashtag:<it>`; hashtags are
   publishable, handles are not — the same false positive BL-1582 recorded), and the new config key,
   which is 33 characters and trips the "opaque literal" rule. The key is written here as
   `_default_hashtags_disabled_<round>`; in config.json it carries the round id.

## 8. Assertions at close

```
master_leads.csv 74,732 rows (74,218 + 514) x 76, header == FULL_COLUMNS
spend.json moved by EXACTLY $1.652400 (total and tiktok), bl1583 rows $1.652400, ig_usd $0.000000
calls: checkpoint 2,754 == ledger 2,754 == pages 2,726 + 28 resolves
label store unchanged (100 rows, sha == start) -- no results file existed to ingest
both review pages + both manifests byte-identical to their start hashes
config diff limited to the 13 disabled tags; 5 campaigns intact
workbook Emails 3,028 rows, MARK non-empty 0 -- untouched
vault verify: VAULT VERIFIED (both roots) · suites: ALL GREEN 4/4, 846 checks; 0 of 1,272 stores moved
```

## 9. Recommendation

Grade the 86-card page — it is the only thing that can say whether 20.2% KEEP means 20.2% editors.
Then extend the tag lists with **professional-tool vocabulary** (the shape `aftereffectsedit`
occupies), not with `<title>edit` variants, which this walk refuted at 6.8% [2.9–14.9]. Leave the 13
disabled tags disabled; they are one edit from coming back if he disagrees.
