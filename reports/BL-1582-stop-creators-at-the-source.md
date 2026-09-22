# BL-1582 — The creators come from the title-only hashtags: 3.4% KEEP against 28.8% for tags that carry the word "edit"; the spend screen now prices delivered addresses

**Round:** BL-1582 · **Read-only analysis + one screen line.** · **Spent: $0.00** — `spend.json`
sha256 `4edc0802cd…` / 16,043,805 bytes at start and at close, byte-identical; no vendor call, no
walk. · Paths redacted: `<PROFILE>` is the user folder. · No campaign config or tag list was
changed; both review pages and manifests he is grading are untouched; hashtags are named, accounts
never are.

## The paragraph

**The hashtags feeding us creators are the ones that name a film or a series without the word
"edit".** Over every TikTok row whose hashtag can be recovered by value (55,461 of 56,680 rows,
97.8%; 3,845 addressed rows), tags carrying editing vocabulary in the name yield **28.8% [27.0–30.6]
KEEP** under the craft cut (667 of 2,319 addressed), title-only tags yield **3.4% [2.6–4.5]** (48 of
1,398) and fan/fyp/meme tags **2.3% [0.8–6.7]** (3 of 128) — an 8.5× gap, re-derived on the bare
suffix rule (ends in "edit"/"edits": 28.7% vs 3.9%). Almost all of the title-only supply sits on the
**PANICBABY** list: 176 such tags, 1,374 addressed rows, 46 KEEP, an estimated **$156 per 1,000
KEEP** against **$14 per 1,000** for the same campaign's "edit" tags. **How much dropping them
saves:** the whole title-only class holds 48 of 718 KEEP rows (6.7%) — over his 5% line, so it
cannot be dropped wholesale; but the **13 title-only tags with ≥20 addressed rows and zero KEEP**
(eternalsunshine, midnightsun, wutheringheights, lalaland, tellmelies, itendswithus, moulinrouge,
conversationswithfriends, casablanca, maxtonhall, dearjohn, outlander, thegreatgatsby) hold 326
addressed rows and **0 KEEP**: dropping them costs no editor by the yardstick and saves an estimated
$1.70 of every walk that revisits them. On the last real walks themselves (91 tags, all "edit"
tags, $5.38, 325 min, 183 KEEP), skipping the worst half by KEEP rate loses **8 of 183 KEEP
(4.4%, under the line)** and moves the price from **$29.39 → $22.47 per 1,000 KEEP and 29.6 → 23.1
hours** — but that ranking is confounded: KEEP rate in the big walk fell from 22.5% in the first
quarter of the walk order to 10.4% in the last, and 64% of the tags the cutoff drops were walked
in the second half, so a "bad tag" there is partly a late tag. **Candidates worth a capped test:**
19 unwalked tags, all "one character/franchise + edit" or a tool word (velocityedit,
aftereffectsedit, capcutedit, alightmotionedit, thanosedit, banedit, arcaneedit …; the best 12
walked tags are 12 of 12 of that shape) — ~$1.96 and ~2 hours at the depth wall, judged by KEEP
rate at n ≥ 20 against the 28.8% baseline, then by his grades. **The spend screen** now carries
one more line under the TikTok estimate: `Per 1,000 DELIVERED (after the craft cut): ~$29.82 and
~30.2 h -- from 3 counted run(s) (2026-09-16): 185 delivered of 1,052 addressed; the run estimate
above prices calls, not addresses` — counted at runtime from master and the ledger, and
**"unknown"** when nothing can be counted (driven both ways, vendor mocked, sockets refused; a $0
cap still refuses). Every ranking above leans on the craft cut, whose 14.8% [10.1–21.3] editor loss
is measured on 247 model-labelled rows, not his grades.

## 1. What this project is, for a reader with no context

ClippersHQ walks TikTok hashtags, collects the accounts that post under them, and delivers the
ones with an address and editing vocabulary in the bio to one operator, who wants "no content
creators and no businesses at all, while keeping the fast pace for 1,000 emails" — under the
standing rule that a real editor is never wrongly cut. BL-1581 found that 4 of 5 addressed rows
are thrown away by the craft cut after being paid for. This round asks which hashtags produce the
rows that are thrown away.

## 2. Part 1 — yield per hashtag: the fields, the denominators, the table

**The tag is recovered by value.** `master.source_hashtag` carries `tt:hashtag:<tag>` on the
campaign-funnel rows (53,920) and a bare `<tag>` on the walker rows (BL-1563/64/66, where
`source_tag` carries the same tag) and on ANIME15K's rows; a bare value counts as a tag only if it
is on a campaign tag list, in the TagLedger (`email_harvest_tags.json`, 669 tags with a walk
record) or in the `tt:hashtag:` set. Everything else is provenance, not a tag, and is **not
guessed**: `tt:search:<term>` (593 rows, a search route), `his_graded` (258), `tiktok_pages` (239),
`twitch_finder` (124) — **1,219 rows, 2.2%, unrecoverable**. `found_via` is blank on all 56,680
TikTok rows, `post_hashtags` on 55,228 — checked before either was trusted.

**Denominators.** 3,845 addressed TikTok rows with a recovered tag (of 4,158): KEEP 718, CUT 3,110,
HOLD 17. 1,094 distinct tags have rows; **only 37 have ≥ 20 addressed rows**, the minimum for a
per-tag verdict (Wilson half-width ≈ 20 points at n = 20; below that a rate is noise). Pages/$ are
known for the 669 TagLedger tags (1,042 addressed rows); **minutes only for the 90 tags of the two
walks with a log** (1,004 addressed rows) — from `attempts.jsonl` epoch stamps, never from the
ledger's booking times. Cost = pages × 1.0104 calls/page (ledger calls 8,963 / walk-log pages 8,871)
× `api.cost_per_call_usd` = 0.0006, read by named key.

| tag | rows | addressed | KEEP | CUT | KEEP % [Wilson] | pages | $ | $/KEEP | min/KEEP | his E/N |
|---|---|---|---|---|---|---|---|---|---|---|
| squidgameedit | 64 | 64 | 17 | 47 | 26.6 [17.3–38.5] | 169 | 0.102 | 0.006 | 0.37 | 1/0 |
| ironmanedit | 102 | 56 | 14 | 42 | 25.0 [15.5–37.7] | 170 | 0.103 | 0.007 | 0.44 | 1/0 |
| venomedit | 28 | 28 | 7 | 21 | 25.0 [12.7–43.4] | 168 | 0.102 | 0.015 | 0.90 | 2/0 |
| captainamericaedit | 20 | 20 | 5 | 15 | 25.0 [11.2–46.9] | 171 | 0.104 | 0.021 | 1.24 | 0/0 |
| ichigoedit | 22 | 22 | 5 | 17 | 22.7 [10.1–43.4] | 169 | 0.102 | 0.021 | 1.24 | 0/0 |
| narutoedit | 136 | 42 | 9 | 32 | 21.4 [11.7–35.9] | 171 | 0.104 | 0.011 | 0.69 | 0/0 |
| cobrakaiedit | 28 | 28 | 6 | 22 | 21.4 [10.2–39.5] | 169 | 0.102 | 0.017 | 1.06 | 0/0 |
| stephcurryedit | 30 | 30 | 6 | 23 | 20.0 [9.5–37.3] | 170 | 0.103 | 0.017 | 1.11 | 1/0 |
| lebronedit | 56 | 56 | 9 | 45 | 16.1 [8.7–27.8] | 170 | 0.103 | 0.011 | 0.65 | 1/0 |
| deadpooledit | 68 | 68 | 10 | 56 | 14.7 [8.2–25.0] | 169 | 0.102 | 0.010 | 0.61 | 1/0 |
| haalandedit | 36 | 36 | 1 | 35 | 2.8 [0.5–14.2] | 170 | 0.103 | 0.103 | 6.27 | 0/0 |
| eternalsunshine | 112 | 38 | 0 | 38 | 0.0 [0.0–9.2] | — | — | — | — | 0/0 |
| midnightsun | 121 | 35 | 0 | 35 | 0.0 [0.0–9.9] | — | — | — | — | 0/0 |
| casablanca | 162 | 22 | 0 | 22 | 0.0 [0.0–14.9] | — | — | — | — | 0/0 |
| (10 more title-only tags at 0 KEEP of 20–28) | | | | | | | | | | |

Full table: `scratch/bl1582/tag_yield.csv` (1,680 tags, tags only). **His grades per tag**: 48
of his 50 TikTok grades join to a tag, spread over 43 tags — 0, 1 or 2 per tag; shown, never ranked
on. The three-hundred-line answer to "which tag" is a five-line answer to "which *kind* of tag":

| class (by the tag's own name) | tags | addressed | KEEP | KEEP % [Wilson] |
|---|---|---|---|---|
| edit-vocabulary in the tag (edit/edits/amv/aftereffects/capcut/vfx/…) | 565 | 2,319 | 667 | **28.8% [27.0–30.6]** |
| title / name only | 187 | 1,398 | 48 | **3.4% [2.6–4.5]** |
| fan / fyp / meme vocabulary | 24 | 128 | 3 | 2.3% [0.8–6.7] |

Second derivation, suffix only: ends in `edit`/`edits` 657/2,288 = 28.7% [26.9–30.6]; does not
61/1,557 = 3.9% [3.1–5.0].

## 3. Part 2 — the counterfactual

**Universe A = the last real walks** (BL-1563 + BL-1564: 91 tags with a walk log, 1,004 addressed,
183 KEEP, 8,871 pages, $5.38, 325 min; baseline **$29.39 per 1,000 KEEP, 29.6 h per 1,000 KEEP**),
ranked by KEEP rate, worst first (tags under n = 20 are ranked too and marked — a small tag is still
a tag that was paid for):

| drop bottom | tags dropped | KEEP lost | KEEP kept | lost % | $ saved | min saved | $/1k KEEP | h/1k KEEP | flag |
|---|---|---|---|---|---|---|---|---|---|
| 0% | 0 | 0 | 183 | 0.0% | 0.00 | 0 | 29.39 | 29.6 | — |
| 10% | 9 | 0 | 183 | 0.0% | 0.13 | 7 | 28.68 | 29.0 | under 5% |
| 25% | 23 | 0 | 183 | 0.0% | 0.29 | 16 | 27.82 | 28.2 | under 5% |
| 50% | 46 | 8 | 175 | 4.4% | 1.45 | 82 | 22.47 | 23.1 | under 5% |

The largest cutoff under his line is the 50% one (46 of 91 tags, 40 of them with zero KEEP rows;
the next tag crosses 5%). It saves the most hours per 1,000 — **but suspect the instrument**: in the
75-tag walk, KEEP rate by walk-order quartile is **22.5% → 19.7% → 18.3% → 10.4%** [6.2–17.0], and
64% of the tags the 50% cutoff drops were walked in the second half; a tag walked last, against a
pool already deduped by everything before it, looks bad for that reason. The 17-tag walk shows no
such slope (12–25%, wide). So the within-walk ranking is half tag quality and half walk order, and
the honest saving from *tag choice* on those walks is smaller than the table says.

**The bigger lever is outside those walks.** The walks were all "edit" tags already; the title-only
supply lives on the campaign lists, where per-tag pages are not recorded, so its cost is estimated
at the measured 8.7 calls per addressed row (BL-1581 §4):

| campaign | class | tags | addressed | KEEP | KEEP % [Wilson] | est $ | est $/1k KEEP |
|---|---|---|---|---|---|---|---|
| PANICBABY | title-only | 176 | 1,374 | 46 | 3.3 [2.5–4.4] | 7.17 | **155.92** |
| PANICBABY | edit-vocab | 456 | 1,225 | 446 | 36.4 [33.8–39.1] | 6.39 | **14.34** |
| PANICBABY | fan/fyp/meme | 24 | 128 | 3 | 2.3 [0.8–6.7] | 0.67 | 222.72 |
| ZHUS | edit-vocab | 44 | 287 | 79 | 27.5 [22.7–33.0] | 1.50 | 18.96 |
| ZHUS | title-only | 5 | 18 | 2 | 11.1 [3.1–32.8] | 0.09 | 46.98 |
| DAYLIGHT | edit-vocab | 10 | 75 | 11 | 14.7 [8.4–24.4] | 0.39 | 35.59 |
| ANIME15K | edit-vocab | 3 | 51 | 16 | 31.4 [20.3–45.0] | 0.27 | 16.64 |

What can be dropped without losing an editor by the yardstick: the **13 title-only tags with ≥ 20
addressed rows and zero KEEP** (326 addressed rows, est. $1.70, upper Wilson bound 9–16% each).
What cannot: the whole title-only class — 48 KEEP of 718 = **6.7%, over the 5% line** — so the
recommendation is the 13, plus "edit"-suffix variants of the titles that are kept (bare
`bridgerton` has 535 rows and reads title-only; `bridgertonedit` runs 6 KEEP of 11).

## 4. Part 3 — unwalked tags likely to do better

What the best 12 walked tags share: 12 of 12 end in "edit"; every one names ONE character,
franchise or athlete + "edit"; none is a bare title, none a tool word. Nineteen candidates, none
walked by the harvester (`scratch/bl1582/campaigns_and_candidates.out` has each one's reason):
**velocityedit, aftereffectsedit, capcutedit, alightmotionedit** (tool vocabulary — editors
self-tag their technique; all on ZHUS's list, never walked; `capcutedit` is also the creators'
tool, so it is a judgement of the class), **thanosedit, banedit, thepunisheredit, bladeedit**
(character + edit siblings of tonystarkedit/jokeredit, ZHUS list, unwalked), **arcaneedit,
oshinokoedit, dexteredit, acrossthespiderverseedit, outerbanksedit, thevampirediariesedit,
thesummeriturnedprettyedit, bridgertonedit, attackontitanedit, bleachedit** (walked small at 5–7
KEEP of 6–12 — deepen them), **onepieceedit** (130 funnel-era rows, 3 addressed; a v2 walk would
price it). A capped test: 19 × ~170 pages × 1.0104 × $0.0006 = **$1.96**, ~118 min at 27.3
pages/min — cap $2.50 / 2.5 h; judged per tag by KEEP of addressed (verdict at n ≥ 20) and pooled
against 28.8%, then by his grades on a three-button page drawn from the new rows. **Not walked
this round.**

## 5. Part 4 — the spend screen

**Fix category: LOCAL, 3 sites in one module** — `main.delivered_projection(master_path, spend_file,
walk_log_root)` (pure over the two files: a window is a `run_id` in both master and the ledger;
dollars from the ledger; delivered = addressed rows with `craft_cut == KEEP`; hours only from a
walker's own `attempts.jsonl`, never the ledger's booking `ts`; any read error → `runs == 0`),
`main.delivered_line(proj)` (counted, or "unknown"), and one `delivered_proj=` parameter on
`preflight_check` that adds one line when TikTok is on, computed in `_execute_run` at runtime.
Driven as BL-1581 did (vendor mocked with planted numbers, every socket refused — control fired):

```
Case A, today's config, TikTok-only, target 1,000 -> ok=True
   | Estimated cost  : ~$1.04   (estimate — actual may vary with lead density; hard-capped below)
   | Per 1,000 DELIVERED (after the craft cut): ~$29.82 and ~30.2 h  -- from 3 counted run(s) (2026-09-16): 185 delivered of 1,052 addressed; the run estimate above prices calls, not addresses
Case B, spend_cap_usd = 0, master absent from the box -> ok=False, BLOCKED
   | Per 1,000 DELIVERED (after the craft cut): unknown (no counted runs yet -- the rate appears after the first run whose rows and ledger entries can be joined)
   abort: Your spend cap is set to $0.00, which refuses all spend, but this run would cost about $1.04.
VERDICT: A REAL ZHUS TIKTOK-ONLY RUN REACHES BEFORE YOU SPEND, AND A DECLARED $0 CAP REFUSES
```

The $29.82 / 30.2 h equal BL-1581 §4's hand-derived figures (a second derivation of the same
counts). Suites covering the change, through the runner with the stores snapshotted:
`ALL GREEN -- 6/6 suites passed, 910 checks` (`test_bl1582_…` 5, `test_bl1581_…` 7, `test_bl1580_…`
18, `test_funnel` 815, `test_resilience` 51, `test_estimate` 14); snapshot diff 0 of 1,274 moved.

## 6. What did not move

No campaign config or tag list; no walk; no store outside the temp boxes. Commits: `6b93bd99`
(`main.py`, under `--foreign BL-1577`, the CLOSED round that still lists it), `af4c393a` (the new
suite), then the report/scratch and the manifest.

## 7. What I got wrong

1. **The first tag-recovery rule threw away 1,060 rows that were tags** — bare values such as
   `aotedit` written without the `tt:hashtag:` prefix. Checking the bare values against the
   campaign lists, the TagLedger and the prefixed set (by value) recovered them; the
   "unrecoverable" share fell from 4.0% to 2.2%. A prefix is a claim about the writer, not the tag.
2. **Wilson lower bounds printed as −0.0** on zero-KEEP tags before clamping.
3. **A candidate on the first list had already been walked** (kobebryantedit is in the TagLedger);
   the filter against the ledger removed it — 19 candidates, not 20.
4. **The counterfactual's headline saving is inflated by walk order** and I only saw it because
   the brief said to look: 64% of the dropped tags are second-half tags of the big walk. The
   number stands in the table with that caveat beside it; it is not the recommendation.
5. **No `python -c` wrote a file this round, and no heredoc** — the six-round streak ends here;
   the file tool wrote every script and every edit.
6. **The leak scan flagged one token in this report** (D2, a 12-character handle-shaped word seen
   in one prior report). It is a hashtag, adjudicated by value, not by eye: it appears 105 times as
   `tt:hashtag:<it>` in master (78 rows, 6 addressed). Hashtags are publishable; the detector
   cannot tell a tag from a handle by shape, and the frequency rule (BL-1571) is what let a
   one-report tag through — recorded here so the next round does not re-litigate it.

## 8. Assertions at close

```
master_leads.csv 74,218 x 76, header == FULL_COLUMNS · workbook Emails 3,028 rows, MARK non-empty 0
spend.json 4edc0802cd... / 16,043,805 bytes == start · label store 100 rows, sha == start
both review pages + manifests byte-identical (51e89edc / fa026ea3 / 4f4abcbb / 8dd8dc29) · vault verify: VAULT VERIFIED (both roots)
store snapshot around the suites: 0 of 1,274 files moved · no walk, no vendor call, no config change
```
