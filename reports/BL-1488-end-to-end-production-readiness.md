# BL-1488 — end to end, with spies: what is live, what it costs, and the one thing that blocks it

## IS IT PRODUCTION READY? **NO.**

**1,000 good (delivered) pages** costs **$1.01 and 1.79 h** on the Spotify route (the only route that
meets both targets), **$2.68 and 0.96 h median / 2.47 h tail** on tiktok/memes, **$1.59 and 0.52 h
median / 2.92 h tail** on tiktok/edits, and **$36.08 and 220.49 h** on instagram/memes. **1,000 emails**
costs **$1.83 and 3.09 h** on Spotify, **$20.40** on TikTok new supply (**$5.24** if you first resolve
the 2,272 addressable handles already in the TikTok store — a one-off worth ~260 addresses), and
**$82.31 judge-excluded / $113.59 judge-corrected** on the Instagram page funnel. **The single
remaining blocker is that the funnel cannot distinguish a judged page from an unjudged one, and it
caches the confusion.** Of eleven deliberately seeded faults, **one stops the run and five are
silent-and-cached** — a vendor 200 carrying an error, a salvaged torn answer, a judge timeout, a
private page and a wall all write `passed: true` into the seen store, which `is_decided()` then skips
forever. Underneath that, the camera reaches **1.82%** of fresh pages (223 of 12,237) and got a grid on
**60.09%** of those (134 of 223), **8,580 of 14,108** delivered rows say no cover was captured, only
**16 of 8,590** were ever recovered (0.19%), and **nothing in shipped code enforces "no page delivered
without an image the model saw"** — a runtime spy put a pictureless row into the delivered .csv and
.xlsx with no exception. Fix the five silent-and-cached faults first; every other number here improves
once a wrong answer stops being permanent. **And one thing must be fixed before even that, because it
was observed happening during this round:** two concurrent rounds interleaved a read-modify-write on the
Instagram seen store and **49 already-walked, already-judged, already-paid pages were written at 17:45
and gone by 18:24**, the key set back to byte-identical with round start. The in-process race test is
green; the cross-process case loses data. While that holds, no seen-store guarantee means anything.

---

## 1. ROUND ID, DATE, AND THE ASK

**BL-1488**, 2026-09-02, 17:04–18:20 CEDT. The ask: verify every change five rounds claim, by **driving
it** rather than reading its report; build one scoreboard per brain; answer the email question; hunt the
code that will produce the next bad number; attack the system deliberately; and ship one read-only
health check that fails loudly.

### ⚠️ THE TREE WAS MOVING. THIS IS THE FIRST FINDING.

Five rounds were in flight when I filed, **four of them within nine minutes**:

| round | filed | holds |
|---|---|---|
| BL-1377 | 2026-08-23 | `reports/BL-1377.md` — **stale 244 h, nothing ever written under it** |
| BL-1484 | 16:56 | `tiktok_finder.py`, `control.py`, `config.json` |
| BL-1485 | 16:58 | read-only — **published 17:29, the only one that landed** |
| BL-1486 | 17:00 | `meme_finder.py`, `tools/exemplar_review.py` |
| BL-1487 | 17:05 | `tiktok_finder.py`, `finder_common.py`, `spend_ledger.py`, `main.py`, `clip_pipeline.py`, `dashboard/*`, `tests/run_all.py`, `docs/*.md` |
| **BL-1488** | 17:07 | this round — **no path conflict with any of them** |

I hashed all 683 code files at round start. **Sixteen moved under me**, several repeatedly:
`tiktok_finder.py` **seven times**, `meme_finder.py` five, plus `control.py`, `main.py`,
`free_judge.py`, `edits_rubric.py`, `finder_common.py`, `spend_ledger.py`, `clip_pipeline.py`,
`filters_free.py`, `config.json` and four test files. Every figure below is anchored to a named sha256
and was re-derived at publication. **`run_mode.py` never moved once.**

Consequence for Part 2: **I did not run the four brains live.** Running a funnel against a spine two
rounds were rewriting is exactly the wrong-clock this project has already published twice. The
scoreboard is built from retained run records instead, and every cell that could not be defended reads
NOT MEASURED with its reason.

**At 17:34:41 `edits_rubric.py` was on disk in a state that raises `NameError` at `:195`** for modes
`both` and `emails`. Two minutes later the name was defined. A run started in that window would have
taken a `NameError` out of the brief picker. That is an in-flight write, not a shipped defect — recorded
because it is what "do not measure a moving tree" means in practice.

---

## 2. WHAT SHIPPED, AND HOW EACH WAS PROVED

Only one thing shipped, because the round is a verification round and every other file was held.

**`tools/health_check.py`** — one read-only command answering "is everything wired and safe to run?".
Ten checks, **each proved by a runtime spy, none by reading source text**. It prints in plain words and
**exits non-zero when anything is not `LIVE AND FIRING`**. Current state: **6 live, 4 broken, exit 1.**

It is built against the three ways a checker has already failed here:

1. **A check that did not run returned the same token as a check that passed** — that hid a dead judge
   for five days. Here `NOT CHECKED` is **not** in the green set and turns the exit non-zero.
2. **A structural guard passed the whole time the block was dead.** So no check reads the AST for a
   caller; each drives the real function and asserts its spy fired.
3. **Two byte-identical runs of an earlier checker were identical because both crashed on an
   unrenderable character and printed nothing.** Stdout is forced to UTF-8 with `backslashreplace`,
   every line is byte-counted, and the process refuses to exit 0 having produced no output or run no
   checks.

**Its own positive control** (`--self-test`) seeds a real fault through the real runner and **fails if
the not-green count does not rise**: measured **5 → 6, PASSED**. `tests/test_bl1488_health_check.py`,
**11 tests, green**, includes an AST assertion that the module opens nothing for writing, and a test
that `_emit` survives a `UnicodeEncodeError` without raising.

**The preflight requirement was already met, and I proved it rather than assuming it.** Patching
`preflight.run_preflight` to return a FAIL and driving the real `run.run_headless` (with the status
writer and run-id setter stubbed, so nothing was written) gave **rc=2, spy fired once, nothing spent**.
The dashboard spawns `clippershq/run.py`, so that path is covered too. **Wiring the preflight is
therefore NOT outstanding.** What *is* outstanding is that it still passes on skipped work — see §3.

---

## 3. WHAT WAS MEASURED

### 3.1 EVERY CLAIMED CHANGE, LIVE-VERIFIED, WITH ITS FIX CATEGORY

`GENERAL` = a required argument, a safer default, a boundary assertion. `LOCAL` = a docstring, a
comment, one call site. The category predicts which come back — and one here **already has**.

| # | change | status | fix category |
|---|---|---|---|
| 1 | Camera bound reworded, `capture_unreached` counter added | **LIVE** — but the bound is byte-identical and delivery is unchanged | **LOCAL** |
| 2 | No-grid page marked `unjudged`, `passed: None` | **SHIPPED-BUT-OFF** — lives inside `if capture_dir:`; when the camera is off the page is bought and delivered unmarked | **LOCAL** |
| 3 | `_CappedCameraClient` reserves before each billed camera call | **LIVE** | **GENERAL** |
| 4 | `bars_kill(run_mode, …)` restores the dropped argument | **LIVE** | **GENERAL** |
| 5 | TikTok latch → `is_decided` (verdict **and** judged_by) | **NOT DONE at round start → LIVE at exit** (landed mid-audit) | **GENERAL** |
| 6 | TikTok facts: real video count + display name | **NOT DONE at round start → LIVE at exit** | **GENERAL** (count) / **LOCAL** (name) |
| 7 | Garbage-cut screen prints the **effective** value | **LIVE** — `control.py:440-441` reads `eff.get(...)` | **GENERAL** |
| 8 | Zero per-run cap refuses | **LIVE** — presence test, not truthiness | **GENERAL** |
| 9 | Language gate `except: return True` | **NOT DONE — deliberate, and uninstrumented** | — |
| 10 | "mean views" statistic named, `n_posts` required | **LIVE**, but **the verdict deliberately did not move** | **GENERAL** (form only) |
| 11 | `complete: true` with `videos: 0` | **NOT DONE. No guard exists.** | — |
| 12 | Exemplar approval list + cross-platform refusal | **SHIPPED-BUT-OFF** — list is empty, so `enforce=False` on **32 of 32** shipping slots | **GENERAL** (inert) |
| 13 | Bogus **platform** refuses | **LIVE** for 12 of 12 bogus cells — **but `platform=None` still buys the bare rubric, and is the parameter default** | **GENERAL** (incomplete) |
| 14 | Bogus **mode** refuses | **NOT DONE end-to-end** — the refusal sits downstream of the coercion | **GENERAL** (wrong layer) |
| 15 | `both`/`emails` borrowed-brief announcement | **LIVE** — announced, **not fixed**; bytes unchanged | **LOCAL** |
| 16 | Dead judge model removed from the chain | **LIVE** — verified: the 404 model is gone, both reject-authority models answered | **GENERAL** |
| 17 | Runs spawned genuinely detached | **LIVE** — `_detach_kwargs()` used at both spawn sites, returns `creationflags=520` | **GENERAL** |

**The LOCAL-vs-GENERAL thesis, demonstrated on live code.** `free_judge.py:999` states outright:
*"`platform=None` still yields the bare RUBRIC, so every existing caller behaves exactly as before."*
The fix went to the **call sites**, not the function. And `free_judge.py:1276` records that this very
bug **already came back once** — wired at one round, found dropped again at a different layer the next.
A local fix to a permissive function is one refactor from being wrong again, and this one has the
receipts.

### 3.2 THE CAMERA — "reached" and "obtained" are different numbers

Source: one production log, sha `739ec90d…`; delivered sheets counted row-by-row.

| quantity | longhand | Wilson 95% |
|---|---|---|
| camera slice offered / fresh | **225 / 12,237 = 1.8387%** | [1.62, 2.09] |
| **CAMERA REACHED** / fresh | **223 / 12,237 = 1.8223%** | [1.60, 2.07] |
| **GRID OBTAINED** / reached | **134 / 223 = 60.0897%** | [53.54, 66.29] |
| **GRID OBTAINED** / fresh | **134 / 12,237 = 1.0950%** | [0.93, 1.30] |
| delivered rows saying no cover | **8,580 / 14,108 = 60.8166%** | [60.01, 61.62] |
| ever recovered | **16 / 8,590 = 0.1863%** | [0.11, 0.30] |

All four briefed figures **CONFIRMED exactly**, re-derived twice from the log bytes. The recovery zero
carries a **positive control that passed**: the same instrument aimed at a different reason string finds
**92 of 153 = 60.13%** recovered, so 0.19% is real and not a dead reader.

**The bound is `min(fresh, max(50, target × 15))` — a function of the target only. It does not scale
with supply.** At target 15 the camera can never photograph more than 225 pages however many are fresh.

**The no-cover string does not mean "never asked".** It means the grid path was falsy: never-asked
(≥98.16% on that run) **or** asked-and-suppressed (≤1.04%). It is **not written at all when the camera
is off** — so 60.82% is a floor, not the true share of pages no model saw. And a page with **zero
tiles** that still saved a file does *not* get the string: 32 of 119 records in one manifest have
`tiles == 0` with a path, so the model is shown an empty page and the row reads as judged.

**"NO PAGE MAY BE DELIVERED WITHOUT AN IMAGE THE MODEL SAW" is not enforced.** The sentence appears in
**8 files, all under `scratch/`**; zero hits in `clippershq/`, `tools/`, `tests/`, `dashboard/`. Runtime
spy: a row shaped exactly as a no-grid page produced landed in the delivered `.csv` and `.xlsx` with no
exception (control: an ordinary row emits `YES` through the same writer). The only thing withheld is the
WANT **badge** — confirmed 0 of 8,580 no-cover rows carry one.

**And the camera did not run at all on the last delivered run: 0 of 58 fresh pages.** Corroborated two
ways (no `capture_*` keys in the provenance file; no capture manifest with that date on disk).
**COULD NOT MEASURE** why — the config trail says it should have run.

### 3.3 THE TWO TIKTOK PATCHES, AND A NEW LIVE DEFECT

**The latch.** `939 of 2,446` rejections — **CONFIRMED exactly, first try**, and I reproduced it
independently: `passed` is True on 1,383, False on **939**, None on 124. Of the 939, **919 carry no
reason key at all**; `verdict` and `judged_by` are present on **0 of 2,446**. The 20 that *do* carry a
reason are all from 2026-08-28 onward — the reason-persistence fix **is** firing (20 of 20 since), and
the 919 are pre-fix residue the latch made permanent.

**The facts chain.** Median understatement **168.0× across 18 authors — CONFIRMED exactly** (min 6.0×,
p75 326.0×, p90 875.0×, max 895.0×; ≥100× on 12 of 18; correctly stated on **0 of 18**). Display name
non-empty on **0 of 18 — CONFIRMED**, with a positive control that passed three ways. A runtime spy on
the prompt assembler shows what the judge actually received: a 58-video page announced as **"1 posts
read"**, with no display-name line. After the fix, on the same 18 authors: **1.0× median, 18 of 18
display names**.

> **⚠️ THE LATCH BECAME A RATCHET, AND THIS IS MY OWN FINDING — VERIFIED AT RUNTIME.**
> `is_decided` requires **both** `verdict` and `judged_by`. `judged_by` is written from `r["rule"]`
> (`tiktok_finder.py:3116`) — and **`judge_author` never sets `rule`**. AST-confirmed: it builds 26 keys
> including `verdict`, and no `rule`. Driven live, with its own control:
>
> | record | `is_decided` |
> |---|---|
> | model rejection (`verdict` set, `judged_by: ""`) | **False** ← re-walked and **re-bought** every run |
> | rule rejection (`judged_by: "green_screen"`) | True (control fired) |
> | kept page | True (control fired) |
>
> **Cost: 939 × $0.0006 = $0.5634 per run, recurring, because model rejections never settle.**
> Instagram does **not** have this: `meme_finder` writes `judged_by` at **five** sites, every one
> anchored to `RULES_VERSION`, so it is always non-empty — I verified 49 pages written today are
> `is_decided` True on **49 of 49**. Both twins carry a **byte-identical** `is_decided` contract
> (`meme_finder.py:264`, `tiktok_finder.py:1755`); only one feeds it. **`tiktok_finder.py` has no
> `RULES_VERSION` at all** (0 occurrences), so the fix needs one defined, not just a fallback.

### 3.4 THE FOUR DANGEROUS DEFECTS

| defect | verdict | guard | failure mode |
|---|---|---|---|
| zero cap = unlimited | **REFUTED** at the reserve path — every zero spelling yields 0.0 | **NOT PROVEN** — a truthiness mutant survives on the Instagram arm | — |
| free judge outside the cap | **CONFIRMED** — 16,133 ledger rows, **$1.4358**, never calls `reserve()` | none | SILENT |
| language gate `except: return True` | **CONFIRMED** — fails **OPEN**, keeps every page | **PROVEN** | SILENT, uninstrumented |
| "mean views" is one video | **CONFIRMED — 55,766 of 55,766 = 100.00%** | **PROVEN** | SILENT; verdict deliberately unmoved |
| `complete: true`, `videos: 0` | **CONFIRMED — 3 of 16** | **NONE — nothing to mutate** | **SILENT-AND-CACHED** |

**Polarity matters and it inverts the conclusion:** the language gate's `return True` means the page is
**KEPT**. A broken import does not reject everything; it silently switches the gate off.

**The billing detail on defect 4 is worse than briefed.** Three runs wrote `complete: true` with zero
videos and 15 refused calls. **Two were billed $0.009 each ($0.018 total); the third recorded
`billed_calls: 15` and `$0.009` that never reached the ledger at all** — an opposite defect in the same
three files. And it compounds: the repo's own measured constants select their corpus by globbing "the
complete run exports", which now returns 16 files, 15 flagged complete, three of them all-zero.

**COULD NOT MEASURE:** the stronger 96.52% reading of the mean-views defect. `views_used_count` **is not
a column in the export** — 0 of 55,766 rows carry it. The key was asserted before the number was
trusted, and the key was not there.

### 3.5 EXEMPLARS, MODES, BRIEFS AND SHEETS

**The Instagram exemplar pack is 8 of 8 TikTok images — CONFIRMED**, in **both** Instagram brains, by
three independent signatures: file path, membership in his own **TikTok** mark corpora (15 of 16 named
there, 0 of 16 in either Instagram corpus), and `tiktok.com` URLs in the source row records. **Zero
Instagram exemplars reach any of the four payloads.**

**Pixels were useless, and that is the finding.** All 16 images are 465×992, a bare 3×4 grid of covers
on black with **no UI chrome, no handle, no view count, no watermark**. A TikTok cover and a Reels cover
are both 9:16. Anyone proposing to audit packs by looking at them will get nothing. **16 distinct
sha256, 0 byte-duplicates** — the older "pasted twice" claim stays refuted. One *page* appears in both
packs under two different captures.

**The approval gate is inert.** `APPROVED_IG_EXEMPLARS = ()` is empty, and `enforce` is only true when
the list is non-empty — so the cross-platform refusal governs **0 of 32** shipping slots. No approvals
file exists.

**A guard that cannot fail.** Mutation testing killed 4 of 5 mutants. The survivor is
`declared != want` (`meme_finder.py:4533`): `enforce` is only true when `want == "instagram"` **and**
the source is the approved list, whose platform tag is `"instagram"` **by construction**. It is an
identity comparison wearing a guard's comment — **the same shape that round shipped to remove,
reintroduced one line lower.** The path check is carrying the guard alone.

**Bogus mode is still served the memes brief, end to end.** `run_mode.resolve()` coerces an unknown
mode to `memes` **upstream** of the new refusal, so the refusal is unreachable from the run path:

```
--mode=meme      -> resolve()=memes  how='default (he asked for memes-only for now)'  -> MEMES brief
--mode=edit      -> resolve()=memes  how='default …'                                  -> MEMES brief
--mode=bogus_zzz -> resolve()=memes  how='default …'                                  -> MEMES brief
--mode=edits     -> resolve()=edits  how='--mode on the command line'                 -> EDITS brief
```

**And `how` lies about provenance.** A one-character typo reports that the mode came from a *default*,
never saying a command-line argument was dropped — defeating the exact purpose the field was added for.
The refusal belongs in `resolve()`. **GENERAL, wrong layer.**

**Four run modes receive two briefs per platform. CONFIRMED, and the collision is exact:**
`memes`, `both` and `emails` hash **byte-identically** on both platforms; only `edits` differs. `both` —
the mode whose whole purpose is to search edit terms *and* meme terms — is judged on the brief that
demands text burned onto the video, which an anime or football edit does not have by construction. It is
now **announced**, not fixed.

**A hole I found myself:** a bogus platform correctly raises, but **`platform=''` and `platform=None`
return the bare 2,126-byte rubric** against 5,749 (Instagram) or 4,918 (TikTok) — no platform addendum
at all — and `None` is the **default value** of `_messages`, `classify` and `should_reject`. Whitespace
refuses; empty does not. This repo's own comment prices that substitution at **74.0% → 86.0% accuracy**.

**The sheets.** Four built, all four verified row by row: **167 of 167** rows carry an image reference,
the file **exists and is non-empty on disk**, its sha256 matches the provenance record, and the source
artifact claims that picture for that row. **167 distinct sha256, 0 duplicates, 0 orphans.** So "rows
may reference images that do not exist" is **REFUTED** for this set. But **"both sides" is REFUTED at
the sheet level** — 3 of 4 are single-sided by construction; only one carries delivered, rejected and
unjudged together. And **"every row from its own run" holds for 36 of 167**; for the other **131 of 167**
the "run" is a **prior grading sheet** — a copy of a copy. **0 of 4 have been graded.**

### 3.6 THE SCOREBOARD — FOUR BRAINS, NEVER POOLED

The four brains are the partition `rubric_for(platform, mode)` actually makes: **instagram/memes,
instagram/edits, tiktok/memes, tiktok/edits**. `both` and `emails` are supply choices with no brief of
their own. Runs were classified by their **own supply lists**, not by filename; five mixed-supply TikTok
runs were **excluded rather than folded into memes**.

⚠️ **Every `spend_usd` on disk EXCLUDES THE JUDGE.** `run.py` filters the ledger on an exact campaign
string; the judge books under a campaign absent from that table. Lifetime judge spend is **$1.4373 over
16,149 rows = 2.35%** of the ledger; on the worst-affected brain it is **7.9%** of true cost. Windows
below were re-summed by campaign to recover it, and the method reproduces two independent recorded
figures exactly.

| | tiktok/memes | tiktok/edits | instagram/memes | instagram/edits |
|---|---|---|---|---|
| pages walked / delivered | 2249/534 = **4.212** (median 3.959, tail 12.13) | 260/58 = **4.483** (median 4.402, tail 28.0) | 7717/50 = **154.34** (median 9.99) | **NOT MEASURED** — no findings export |
| calls / paid page | 2202/538 = **4.093** | 157/58 = **2.707** | **NOT MEASURED** — no "profiles bought" counter | **NOT MEASURED** |
| paid / delivered | 538/534 = **1.007** | 58/58 = **1.000** | **NOT MEASURED** | **NOT MEASURED** |
| calls / delivered | 2202/534 = **4.124** | 157/58 = **2.707** | 3008/50 = **60.16** | 704/16 = **44.00** |
| **$ / 1,000 delivered** | **$2.68** | **$1.59** | **$36.08** (vendor only) | **$32.80** |
| **$ / 1,000 approved** | **$0.89** (same pages) | **NOT MEASURED** — only edits marks are superseded | **$6.92** (same pages, derived) | **NOT MEASURED** — marks file is **byte-empty** |
| s / delivered, median | **3.5 s** | **1.9 s** | **424.0 s** | **157.7 s** |
| s / delivered, tail | **8.9 s** | **10.5 s** | **793.8 s** | 157.7 s (n=1) |
| **hours / 1,000** | median **0.96**, tail **2.47** | median **0.52**, tail **2.92** | **220.49** | **43.80** |
| approval (n, Wilson, baseline) | n=265: **44.5% [38.7, 50.5]**; baseline **ALWAYS REJECT 55.5% — the constant beats it** | **EXCLUDED** (superseded) | n=121: **56.2% [47.3, 64.7]**; baseline **ALWAYS WANT 56.2% — tie** | **EXCLUDED** |
| email / DM-only / neither | **9.4% / 1.9% / 88.8%** (n=534) | **6.9% / 22.4% / 70.7%** (n=58) | email **19.5%** (n=123); rest **NOT MEASURED** | email **25.0%** (n=16); rest **NOT MEASURED** |

**Against the targets — the exact gaps, not approximated toward them:**

| brain | vs $2.00 | vs 2 h |
|---|---|---|
| tiktok/memes | **MISSES by $0.68** (1.3×) | median passes by 1.04 h; **tail MISSES by 0.47 h** |
| tiktok/edits | **MEETS**, $0.41 under | median passes by 1.48 h; **tail MISSES by 0.92 h** |
| instagram/memes | **MISSES by $34.08** (18.0×) | **MISSES by 218.49 h** (110.2×) |
| instagram/edits | **MISSES by $30.80** (16.4×) | **MISSES by 41.80 h** (21.9×) |

**Only tiktok/edits meets the dollar target, and no brain meets the clock at its tail.**

**The accuracy ceiling, carried with every figure.** His marks are **77.2% self-consistent [69.8,
83.2]** and he reproduces his own 1–10 score only **18.5%** of the time, so everything is scored
**want/not-want at a declared cut: score ≥ 6**. Corpus: **15 mark files inside delivered sheet
directories only, 683 raw rows → 537 distinct pages** — which I reproduced independently to the row. The
reversed-subject set is **excluded: 76 rows / 51 pages** (car, gym, motivation). That exclusion matters
enormously — scored against the old marks the same run reads "34.5% of wanted pages killed"; excluding
them it killed **0 of 16**.

**The 95% bar on kills of wanted pages — both cutters still fail, and his new marks do not help:**

| cutter | kills | rate | Wilson 95% | upper vs 5% |
|---|---|---|---|---|
| model A @90 | **1 of 74** | 1.4% | **[0.2, 7.3]** | 7.3% > 5% → **FAILS** |
| model B @90 | **3 of 74** | 4.1% | **[1.4, 11.3]** | 11.3% > 5% → **FAILS** |

**His new marks narrow it by zero pages** — everything added since is either Instagram or in the
excluded superseded set. **What n would clear it:** with 1 kill observed, **n = 110** (+36 wanted
pages); with 0 kills, n = 73; with 2, n = 142; with 3, n = 173.

⚠️ **Baseline scope, because quoting one beside an accuracy from another manufactures a win.** The best
constant answer **flips by scope**: ALWAYS WANT wins at 73.0% on one TikTok sheet and at 83.7% on one
Instagram sheet; ALWAYS REJECT wins at 65.4%, 72.0% and 78.0% on three others. **The 74.0% baseline this
project has quoted is ALWAYS-WANT on one specific 100-page TikTok sheet and nothing else.**

### 3.7 THE EMAIL ANSWER

| route | $ / 1,000 delivered pages | **$ / 1,000 ADDRESSES** | gap | vs Spotify |
|---|---|---|---|---|
| **Spotify → handle** | **$1.0120** | **$1.8331** | **1.81×** | 1.0× |
| **TikTok new supply** | $2.3367 | **$20.4000** | **8.73×** | **11.1× dearer** |
| **Instagram meme pages** | $2.6047 judge-excl. / $3.5945 corrected | **$82.3089 / $113.59** | **31.60×** | **44.9× / 62.0× dearer** |

Worked longhand for TikTok: `$2.346000 / 1004 delivered = $0.00233665/page`; `1004/115 = 8.7304
pages per address`; `$2.346000 / 115 = $0.02040000/address`; `× 1000 = $20.40`. Positive control:
`$2.346000 / 3910 calls = $0.00060000` — exactly the configured unit price.

**A saving on pages is not a saving on emails.** Spotify's rows arrive **55.2%** pre-addressed;
Instagram's arrive **2.64%** (160 of 6,058, **CAPTURED** denominator — the briefed 2.61% [2.23, 3.04] is
confirmed on the identical n). That single ratio is the whole story.

**The two TikTok routes, priced side by side.** The 2,446 handles are confirmed; **2,272 are addressable**
(no address yet). Route B: `2,272 × $0.0006 = $1.3632` buying `2,272 × 0.114542 = 260.24` addresses =
**$5.2383 per 1,000** [$4.42–$6.23 across the yield CI], against Route A at **$20.40** — **3.89× cheaper.
But it does not scale**: it is a one-off worth ~260 addresses. To 1,000 TikTok addresses: Route B first
($1.3632 → 260) then Route A for 740 more ($15.0960) = **$16.4592**, a **19.32%** saving on pure Route A.

The briefed re-find figures reproduce **exactly**, from raw records against a pre-run master snapshot:
known handle carries an address **8/10 = 80.0% [49.02, 94.33]**, new handle **4/90 = 4.44% [1.74,
10.88]**, address-level re-find **8/12 = 66.67% [39.06, 86.19]**; control 10+90=100 and 8+4=12.
⚠️ But "known" there means *already in master* (n=10), a different population from the 2,446 in the seen
store — of which only 402 are master rows. **The 80% cannot be lifted onto the 2,446.**

**Free bio vs paid call.** On Instagram one billed response returns the bio **and** the contact field
together off the same object; the free feed carries them on **0 of 680** payloads. So the call cannot be
dropped — and the true figure is **stronger** than briefed: **96.56%** (981 of 1,016) of Instagram's
own-funnel addresses come from that one paid response, not 52.8%. (52.8% is the contact-button share
*inside* the paid call, not a free/paid split.) On TikTok the bio genuinely arrives free at discovery
and the additive merge ships — **but it has never paid off on a shipped run: 2 of 115 addresses free**,
because every retained run predates the reader fix. **CONFIRMED in code, COULD NOT MEASURE in production.**

**The deliverable count, not the row count.** Using the shipped validators plus fresh MX:

```
rows 12,985 -> unique 12,698 -> structurally valid 12,572 -> non-role 11,263 -> live-MX 11,194
DELIVERABLE = 11,194 / 12,985 = 86.21% [85.60, 86.79]
OVERSTATEMENT if you quote rows = 1,791 addresses = 13.79%
```

Instagram overstates by **15.99%**, TikTok by **3.76%**. The mangled class is real: **`.con` × 10** (a
`.com` typo) plus vocabulary-word TLDs that are bio-text spill. **The primary send file is already
clean — 8,699 of 8,699 survive every stage** — but the Instagram meme send file **does not drop role
inboxes**: 161 of 966 rows (16.67%) are shared `info@`/`contact@`-class addresses, so its true
person-reachable count is **805, not 966**.

**The MX gate's flag is load-bearing — proven by execution, production untouched.** The bare refresh
command defaults to a send file two days stale; run against a copy it probed 2,252 domains in 18.9 s,
exited 0, printed "wrote" — and changed **ADDED 0 / REMOVED 0 / CHANGED 0**. The `--from-master` form
probed 4,154, **ADDED 2, CHANGED 3, and found two more certain-bounce domains** — two live sends that
would have bounced. Three of four send files still refuse at 99.75–99.91% coverage against a 100.0%
requirement. **The refusal message already names the right flag; the tool's own header lists the no-op
form first.**

### 3.8 THE BAD-NUMBER GENERATORS — HUNTED BY SHAPE

| # | file:line | shape | verdict |
|---|---|---|---|
| 1 | `meme_finder.py:6249` | rate = count / one wall-clock, no median, no n | **LIVE** — the known one |
| 2 | `meme_finder.py:6251` | same quotient, operator-facing | **LIVE** |
| 3 | `main.py:3460` | `qualified / (elapsed/60)` printed as leads/min | **LIVE** |
| 4 | `parallel_judge.py:432` | `3600 × judged / elapsed` | LIVE shape, **no production caller** |
| 5 | `dashboard/server.py:3031-3032` | scaled share over one elapsed, feeds an hours estimate | **LIVE** |
| 6 | `harvest_accounts.py:238,258-259` | a "saving" that is **the same expression** as the cost | **LIVE** |
| 7 | `clip_vision.py:373-378` | per-page price × a match rate from another population | LIVE shape, **no production caller** |
| 8 | `clip_walk.py:352` | dollars from an **assumed** keep rate | LIVE, self-labelled |
| 9 | `outcome_loop.py:694-697` | a hard-coded constant described as **"measured on this project's own funnel"** | **LIVE** |
| — | `main.py:1208`, `editor_brief.py:143`, `filters_free.py:229`, `caption_finder.py:1115`, `clip_pipeline.py:4816`, `dashboard/server.py:3804` | — | **CLEARED** — each has a median companion or re-measures its outcome denominator |

Generator #1 is reachable from the shipped Instagram funnel. Recovered from the round archive, **66
observations at identical lane settings**: **min 10.48, max 126.09** on real walks (**1078.39** including
cached 3-page batches — a **103× spread on one field**). A 14-page/80.1 s batch reads **10.48**; an
18-page/11.5 s batch reads **93.95** — **9× apart at effectively the same batch size**. The number is
dominated by lane fill and cache state, and nothing sits beside it to say so.

**The drift guard fires only at 25%, and it is green right now — I verified this myself:**
`facts_guard.check_all(FACTS)` returns **`[]`**. Live drift on the two biggest money facts is
**+15.97%** and **+19.46%**, both invisible by design. The guard first fires after another **$4.76** of
spend. Its band demonstrably works (positive control: fires at +30%, not at +24%, fires downward), and
it **has** fired historically at 27.1% and 25.3% — **the threshold is the entire failure.** It runs in
the suite against the live file, so this is not a check nobody runs; it is a check that runs, on the
right file, and reports OK. It is **not** in the pre-commit hook.

**The documentation defects, named with file:line, nothing edited (`docs/` is held):**

- **Five documents instruct him to send** — `OPERATING.md:78-79` ("Send from that file and no other"),
  `docs/SENDING.md:342`, `docs/SEND_DAY.md:1`, `docs/FIRST_DAY.md:32`, `docs/HANDOVER.md:198`.
  `OPERATING.md` carries the no-send banner at `:3` and breaks it 67 lines later.
- **"4–8% reply rate" — REFUTED on the count: 16 live sites in 7 files, not five.** 15 now disclaim it
  as an outside rule of thumb; **one does not** — `outcome_loop.py:694`, the constant they all resolve
  to. **True denominator: 0 of 72,954 leads.** All nine outcome columns are empty on every row; the
  recorder writes a file that does not exist.
- **The send file: 2,970 quoted, 8,699 live.** I re-derived 8,699 three ways. **11 doc sites quote
  2,970; zero quote 8,699.** Stale by 5,729 rows (2.93×), including the two an operator reads
  immediately before a first send.
- **The four brains appear in no operator-facing doc** — zero conceptual hits across 1,037 markdown
  files outside the round archive, while 72 archive files document them richly. **A publishing gap, not
  ignorance.** And `docs/STATE.md:16`, self-described as "complete honest state", asserts the opposite:
  *"Run modes: [1] TikTok-only, [2] IG-only, [3] Both/IG-emails, [4] Both/IG-cheap-handles"* — the exact
  term, exactly four, and **not one of them is memes, edits, both or emails**.
- **The stale Instagram price is in a doc, not the config.** Config is **correct at $0.00069064**;
  `docs/FACTS.md:112` and `:527` say $0.0006, and `docs/TRUE_NUMBERS.md:98` mis-reports the config
  itself. One genuine code mismatch: `clip_vision.py:355` prices an Instagram page at the other vendor's
  rate, 15.1% low.

### 3.9 THE ATTACK — 11 FAULTS SEEDED, EVERY VENDOR RESPONSE FAKED LOCALLY

**1 of 11 stops the run. 5 are silent-and-cached, and every one writes `passed: true`.**

| verdict | faults |
|---|---|
| **LOUD (stops the run)** | disk full on the seen store / state file — raises, run dies, **store byte-identical and still valid JSON** |
| **CORRECT (no fault to report)** | torn JSON before the confidence field → **MAYBE**; a wall on a thin page → **UNJUDGED, `passed: null`**; two writers racing one store → **145/145, no lost update**; a test entry point reaching the funnel → **0 trips across 408 imports and 18 executions** |
| **SILENT** | config missing a key (**9 of 10 pass the gate**); killed at page 8 (**no record exists at all — 8/8 units lost**); disk full on the progress hook (warning only, run reports success); campaign-vs-global override (prints the effective value, but terminal-only — a headless run sees nothing) |
| **SILENT AND CACHED** | vendor 200 with `error` **and** `items`; torn JSON **after** the confidence field (salvaged); model timeout; **private page**; wall when discovery was generous |

The five that compound, each violating a standing rule:

- **A 200 carrying an error is recorded as `{"ok": true, "error": ""}`** — an explicit claim the look
  succeeded — while the body said results were partial and stale. Nothing on disk says the vendor
  complained. *Torn/error/wall must be UNJUDGED, never a verdict.*
- **The torn-JSON salvage reconstructs an answer and cuts on it**, producing a rejection byte-identical
  to one made on a complete answer. It sets a `_salvaged` flag **with zero readers in the entire tree**.
- **The judge times out and the page ships as WANTED**, while the run-level error counter reads **0** —
  it counts a key that path never sets. *Violates "a model error is UNJUDGED, never a verdict."*
- **Private is not a fourth state.** The word appears **once** in the whole TikTok path, never reaches
  the row, the store or any rule. The private page is delivered as a normal WANT and cached.
- **A wall is invisible when discovery was generous** — the refusal is only consulted if the page is
  *also* thin, so a walled page is judged on our own crawl and cached.

**Every positive control fired**, and one **failed first and was fixed**: the race control's second
writer crashed rather than racing, so its "60 records lost" proved nothing; re-run properly it produced
a genuine 59-record loss. A control that fails for the wrong reason proves nothing.

---

## 4. WHAT WAS REFUSED OR NOT DONE

- **No live four-brain run.** The spine was being rewritten by two rounds; `main.py` changed sha within
  ten minutes of my snapshot. A clock measured on that tree would be the exact wrong number this project
  has published twice. The scoreboard comes from retained records, and unmeasurable cells say so.
- **Nothing under `clippershq/`, `dashboard/`, `docs/`, `config.json` or any seen store was written.**
  All were held by live claims. Every defect in them is named with file:line and left, per the standing
  rule.
- **The preflight wiring was not changed** — driving it proved it is already wired and already fails the
  run (rc=2). The residual gap (it passes on skipped work) is in a held file.
- **The full suite is not claimed green.** It ran to completion — **434 suites, 2,313.9 s, 18 red** —
  but **while five rounds were writing**, and the runner's own footer says so. That is a reading, not a
  property of the repo. Families I drove directly: my own **11 green**; the language-gate family **43
  green**; the video-brain family **17 green**; the views-statistic family **6 green**.
- **Two of the 18 reds are stale guards asserting the opposite of a deliberate fix**, not regressions —
  see §5.
- **Nothing was promoted, approved, sent, or deleted.** No exemplar was promoted; no address was used.

---

## 5. WHAT I GOT WRONG

**My own health check shipped a false red, and I caught it before publication.** The zero-cap check
originally evaluated `int((cap or 999999) / price)` — **an expression I wrote myself** — and reported
BROKEN because that toy returned 1.4 billion. That is measuring my own paraphrase, not production. The
real `effective_run_cap` uses a **presence** test and returns 0.0 for every zero spelling. Corrected to
drive the real function.

**And my first correction was also wrong, caught by my own control being too weak.** `per_run_keys` is a
**list**; I passed a bare string, so it iterated the characters, matched nothing, and fell through to
the default — returning 5.0 for *every* input **including the control**. The control passed only because
it asked `> 0`. A control must **discriminate**: it now requires the declared $0.50 to come back as
exactly 0.5. This is the same trap the brief warns about — reading a key that does not exist and getting
the same answer for every input including the controls — and it caught me in my own instrument.

**I corrected a sub-agent's interpretation.** A red test was reported to me as *"`record_many` is
dropping a handle — a silent data-loss shape in a seen store."* Driven directly: **all three records
persist on disk.** The missing handle is a rejection with no verdict, correctly excluded from the
**skip set** by the new `is_decided` contract. It is not data loss; it is a **stale test pinning the
pre-fix contract**, the same shape as the lifetime-cap suite that is red because a round deliberately
inverted fail-open to fail-closed. The observation was right; the meaning attached to it was not.

**A sub-agent corrected itself, and the correction made its finding worse.** It first reported the drift
guard as having no caller; the completed sweep found the caller — the suite, pointed at the live file.
So the guard is not unrun. It runs, on the right file, and reports OK against a 15.97% drift.

### What I could not confirm

| claim | outcome |
|---|---|
| "$137.31 per 1,000 Instagram addresses" | **could not reproduce** — my same-pages figure is $82.31 / $113.59. A different run; **do not cross them.** |
| "a 360-video page arrives as 5" | **shape confirmed, exact figure not reproducible** — the nearest cases give **1** and **4**, never 5 |
| the 96.52% single-video reading | **could not measure** — `views_used_count` is not a column in the export, 0 of 55,766 rows |
| 74 wanted of 100 on the reference sheet | my independent read gives **73**. A one-page disagreement I am not resolving in the published figure's favour by default |
| why the camera was off on the last delivered run | **could not measure** — the config trail says it should have run |
| whether the pages-per-minute number has ever been read during a live run | **could not measure** |

---

## 6. MONEY AND SAFETY

**Spend, by this run's own counter: 12 calls — 10 judge probes at 8 tokens each, 2 vendor probes —
attributable cost $0.001381.** That is **0.07% of the $2.00 cap**. The shared ledger moved **$0.086803**
in the same window across four concurrent rounds, which is exactly why the round's own counter is the
authority and the ledger delta is not.

**Backups taken and each VERIFIED by sha256 against source**, read twice to catch a concurrent write:
`config.json`, `spend.json`, `master_leads.csv` and **all five seen stores** — 8 of 8 **VERIFIED**.

**Seen-store delta, computed as a SET at round start and again at publication** (never a membership
test, no key printed):

| store | start | publication | added | removed |
|---|---|---|---|---|
| meme pages | 6,058 | **6,107** | **+49** | 0 |
| tiktok pages | 2,446 | 2,446 | 0 | 0 |
| spotify playlists | 1,880 | 1,880 | 0 | 0 |
| repost | 1,715 | 1,715 | 0 | 0 |
| clip | 2,193 | 2,193 | 0 | 0 |

**+49 arrived mid-round from a concurrent Instagram funnel** — the brief warned to expect this and a
previous round saw +14. I verified they are **real, not fixture poisoning**: 0 bear a test stamp, all
walked today, 44 rejected / 5 kept, every one carrying `verdict` and `judged_by`. **`master_leads.csv`
is byte-identical to its backup.** Nothing this round wrote touched production.

> ### ⚠️ AND THEN THOSE 49 PAGES WERE LOST — A LIVE READ-MODIFY-WRITE INTERLEAVE, OBSERVED
>
> I re-checked the delta **again after publishing**, which is the only reason this was caught.
> The Instagram seen store went **6,058 → 6,107 → 6,058**:
>
> | time | pages | key-set sha256 | note |
> |---|---|---|---|
> | round start | 6,058 | `222aed5a04bf117c` | my verified backup |
> | ~17:45 | **6,107** | `0abd7fad528b59f1` | +49 walked, judged, 44 rejected / 5 kept |
> | 18:24 | **6,058** | **`222aed5a04bf117c`** | **identical to round start — the 49 are gone** |
>
> The file was **rewritten** at 18:24 (fresh `updated` stamp of `2026-09-02T18:00:49`), and against my
> backup it shows **0 added, 0 removed, 0 records mutated in place**. A writer holding an in-memory copy
> that predated 17:45 wrote it back and **discarded 49 pages that had already been walked, judged and
> paid for.** They are not marked seen, so they will be re-discovered and re-bought.
>
> This is the classic two-interleaving-read-modify-writes shape, and the suite has a test named for it
> having happened before on a different store. My fault-injection territory tested exactly this and found
> **no lost update (145 of 145)** — but that test ran **two writers inside one process, both honouring the
> file lock**. What happened here is **two separate processes from two different rounds**, and the lock did
> not save it. **The in-process test is green and the cross-process case loses data**, which is precisely
> why a passing test is not evidence that the mechanism works.
>
> ⚠️ **This is the same failure class as the round's headline blocker, pointing the other way.** A
> silent-and-cached fault makes a wrong answer permanent; this makes a *right* answer disappear. Both
> come from the seen store being treated as a place you can read, hold, and write back later.
>
> **CHECK THE SEEN-STORE DELTA AT PUBLICATION, NOT ONLY AT CHECK TIME.** Had I checked once at 17:45 I
> would have published "+49 arrived, all real" and been wrong about the outcome. Had I checked only at
> 18:24 I would have published "+0, nothing moved" and never seen the 49 at all. **Both single readings
> are wrong; only the sequence is true.**

**Campaigns SHA re-verified at publication, both forms: `8e02f8d6f6307ae8` (default separators) and
`7a029ee5447cddd8` (compact) — both match.**

**A live safety defect found on the way in:** the run marker claims a live dashboard server at a named
process id, and **the listening-port table shows nothing there**; that process does not exist. The
standing rule "never save under the dashboard directory while a run is live" is being evaluated against
a file that lies — which blocks safe work and, once ignored, stops blocking unsafe work. The health
check now catches it, by the port table and never a command-line grep.

**One safety mechanism verified genuinely fixed:** the "spawned DETACHED" docstring used to be false —
what actually protected live runs was a missing `/T` on a taskkill. `_detach_kwargs()` is now used at
both spawn sites and returns real detach flags, so the comment and the code finally agree. The one
taskkill that *does* carry `/T` is the deliberate operator-initiated stop, which is correct.

---

## 7. WHAT TO DO NEXT, RANKED

0. **Stop the cross-process lost update on the seen stores.** Observed live this round: 49 walked,
   judged and paid-for Instagram pages were written at 17:45 and **gone by 18:24**, the key set back to
   byte-identical with round start. The in-process race test is green; the cross-process case is not.
   Until this is fixed, no other seen-store guarantee holds, and concurrent rounds silently destroy each
   other's paid work.
1. **Make a wrong answer stop being permanent.** The five silent-and-cached faults all write
   `passed: true` into the seen store, and `is_decided()` then skips those pages forever. Nothing else on
   this list matters as much, because this one makes every other error compound. Minimum: a vendor 200
   carrying an `error` must not record `ok: true`; a private page must get its own permanent fourth
   state; a wall must be consulted regardless of how generous discovery was.
2. **Fix the TikTok ratchet — one line, and Instagram already shows the shape.** Write `judged_by` from
   a rules-version constant rather than from a `rule` key the model path never sets. Costs **$0.5634 per
   run, recurring**, until it is done.
3. **Move the bogus-mode refusal into `resolve()`.** A `--mode=edit` typo is still served the memes
   brief end to end, and reports its provenance as "default". The refusal downstream is unreachable.
4. **Make `rubric_for` refuse `None` and `''`.** It is the parameter default on three functions, it
   silently buys a 2,126-byte brief instead of 5,749, and this exact bug has already come back once.
5. **Make the preflight fail on skipped work.** It returns ok with checks NOT CHECKED, so a caller
   gating on it exits 0 having never dialled the judge — the residue of the five-day dead judge.
6. **Grade the 16 delivered Instagram-edits pages.** Their marks file is byte-empty; both edits brains
   are unscoreable on accuracy today, and this is the cheapest item on the list.
7. **Get 36 more graded wanted pages** to bring the kill-rate bar from n=74 to **n=110**, the point at
   which the better cutter's Wilson upper bound finally clears 5%.
8. **Give generator #1 a median and an n**, or stop emitting it. A field with a 103× spread and no
   companion statistic will produce the next retracted headline.
9. **Lower the drift guard's band** below the live 15.97% / 19.46%, and add it to the pre-commit hook.
10. **Fix the four documentation defects** — the five send documents, the 16 reply-rate sites against a
    denominator of zero, the 11 sites quoting 2,970 rows against a live 8,699, and `docs/STATE.md:16`.
11. **Enforce "no page delivered without an image the model saw"**, or stop claiming it — it exists only
    in scratch files today.
12. **Replace `declared != want`** with a check that can fail, and give `both` its own brief.

---

## 8. PATHS

| what | where |
|---|---|
| this report | `reports/BL-1488-end-to-end-production-readiness.md` |
| the health check | `tools/health_check.py` — run it with `--network`; `--self-test` proves it can detect |
| its tests | `tests/test_bl1488_health_check.py` (11, green) |
| tree hashes at start / mid / publication | `scratch/bl1488_tree_at_start.json`, `_mid.json`, `_mid2.json` |
| seen-store baseline (computed sets) | `scratch/bl1487_seen_baseline.json` |
| verified backups + manifest | `backups_bl1487_<stamp>/_manifest.json` (8 of 8 VERIFIED) |
| camera instruments | `scratch/bl1488_camera_*` |
| four-defect instruments and mutants | `scratch/bl1488_defect_*` |
| TikTok latch/facts probes and mutation harness | `scratch/bl1488_tiktok_*` |
| exemplar/mode/sheet probes and mutants | `scratch/bl1488_pack_*` |
| bad-number AST census and drift | `scratch/bl1488_badnum_*` |
| the 11 attack probes | `scratch/bl1488_attack_*` |
| scoreboard and ledger windows | `scratch/bl1488_score_*` |
| email arithmetic and MX runs | `scratch/bl1488_email_*` |

Run the health check from the repo root with the project's own interpreter at
`.venv\Scripts\python.exe`. It writes nothing, dials nothing without `--network`, and its exit code is
the answer.
