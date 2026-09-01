# BL-1478 — the funnel discovers and does not judge, and the camera is never asked

## IS THE FUNNEL NOW JUDGING END TO END? **NO — BUT THE CAUSE IS NOW KNOWN AND NAMED.**

**The judge is not broken.** Driven live this round on real pages: **200 of 200** pages that had a
picture reached the model and came back with a parsed verdict. **Zero torn answers, zero errors.**

**The camera is not broken either.** The most recent capture run is **50 of 50 grids, zero login
walls, all free, HTTP 200 on all 50, median 2.16 s per page.**

**The camera is simply never asked.** On the only complete production log, the funnel photographed
**225 of 12,237 fresh pages — 1.84% [1.62, 2.09]** — and then walked, rule-judged and **delivered
the other 12,012 with no picture at all.** A page with no picture cannot reach the model judge;
it can and does reach the rules engine. So those pages are not unjudged — **they are judged by the
half of the system that has no picture, with nothing able to overrule it.**

Three independent faults produced "discovered 15,323, judged zero". **One is fixed here, one is a
config change held by another round, and one was somebody running the funnel from a test harness.**

---

## 1. ROUND ID, DATE, AND THE ASK

**BL-1478**, worked 2026-09-01. The instruction: the last full run discovered 15,323 pages and
judged none of them; 65.9% of 14,108 delivered rows carry no verdict; clipper acquisition is down
99.2% month on month. Find out why, with a runtime spy and a stage count rather than a grep — then
fix the latch that makes rejections permanent, verify each of the four judging "brains" gets its
own brief, make a reject say what it saw, and prove the thing runs end to end on 50–100 pages per
brain.

---

## 2. WHAT SHIPPED, AND HOW EACH WAS PROVED

Proof means a **runtime spy** — drive the real shipped function, count actual calls — or a live
run. A passing test is not proof on its own.

| # | change | file:line | how it was proved |
|---|---|---|---|
| 1 | **The skip latch.** Skip now requires a positive, attributable decision instead of the absence of a marker | `meme_finder.py` — `PageSeen.handles` + new `PageSeen.is_decided` | Drove the real function over the live 6,044-page store: **re-admits exactly 1,351**, leaves 2,647 attributable rejections skipped. **5 of 5 mutations caught** |
| 2 | **A reject now says what it saw.** `model_why` reaches the record *and* the visible reason | `meme_finder.py` — new module-level `model_said()` | Live run: **108 of 108 rejections carry the model's own sentence**; before this commit it was 0 of 5,827 |
| 3 | **An unrecognised platform refuses** instead of silently serving the bare brief | `free_judge.py` — `rubric_for` | `rubric_for("instgram")` now raises; `None`/`""` still return the bare rubric. Safe to raise, **checked by AST**: the production call site sits inside two enclosing `try` blocks and a model failure there is KEEP |
| 4 | **The post count renders.** It survived the whitelist and then printed nothing | `free_judge.py` — `facts_block` | Micro-control: `{"handle","posts":360}` rendered no line, now renders one; with `video_posts` present the original wording is unchanged |
| 5 | **The camera bound states its consequence** and records `capture_unreached` | `meme_finder.py` — the capture slice | The replaced sentence was the bug's own justification and was false (section 5) |

**Tests:** one new suite of 12, plus one existing suite corrected deliberately. All pass.

---

## 3. WHAT WAS MEASURED

**MEASURED** = observed this round. **DERIVED** = computed from those observations. Every rate
names its denominator and carries a Wilson 95% interval.

### 3.1 The six stages — three separate runs, never cross-multiplied

⚠️ These are six different numbers and this project has conflated them repeatedly.

**Run A — the "judged zero" walk.** Denominator = 5,029 distinct pages in its own checkpoint.

| stage | count | of | status |
|---|---:|---|---|
| walked (entered the buy loop) | 5,029 | — | MEASURED |
| had a picture at all | 723 = **14.38% [13.43, 15.37]** | 5,029 | MEASURED |
| entered the judge | 711 | 723 | MEASURED |
| **judged (a verdict came back)** | **0 = 0.00% [0.00, 0.54]** | 711 | MEASURED |
| paid | 0 | 723 | MEASURED |
| delivered | +4,371 rows, **−1** net YES | 14,108 | MEASURED |

**Run B — the only complete production log.** Denominator = 12,237 fresh pages.

| stage | count | of | status |
|---|---:|---|---|
| discovered | 14,033 | — | MEASURED |
| fresh | 12,237 | 14,033 | MEASURED |
| **camera reached** | **225 = 1.84% [1.62, 2.09]** | 12,237 | MEASURED |
| captured | 223 | 225 | MEASURED |
| got a grid | 134 = **60.09% [53.54, 66.29]** | 223 | MEASURED |
| judged | 225 verdicts in 223 s | 225 | MEASURED |
| paid / delivered | — | — | **NOT MEASURED** (log truncated mid-walk) |

### 3.2 The delivered sheet — reproduced independently, with an exact-sum control

Denominator = 14,108 rows on one delivered sheet.

```
489 YES + 10,528 infrastructure + 3,091 rule + 0 unclassified = 14,108 = row count   EXACT
```

| finding | value | status |
|---|---|---|
| infrastructure decides | 77.30% [76.59, 78.00] of 13,619 non-YES | **CONFIRMED** |
| rules decide | 22.70% [22.00, 23.41] | **CONFIRMED** |
| "no cover image was captured" | **8,580 = 60.82% [60.01, 61.62]** of 14,108 | **CONFIRMED to the unit** |
| rows with no verdict | 9,291 = 65.86% [65.07, 66.63] | **CONFIRMED** |
| ever recovered on a later sheet | **16 of 8,590 = 0.19% [0.11, 0.30]** | MEASURED — control: the flag does flip for exactly those 16 |
| printed in that state on five consecutive sheets | 4,425 pages | MEASURED |

⚠️ **"3.6× every shipped rule combined" is REFUTED as stated.** Against the same rule bucket the
ratio is **2.78×**. It reaches 3.66× only by excluding 746 hook-count rows, 439 of which sit on
*wanted* pages — a defensible exclusion that was never declared. Report **2.78×**, or state the
exclusion.

### 3.3 Grid coverage — the structural version of the same fact

Denominator = 6,044 pages in the live Instagram seen-store; index = 10,904 grids on disk.

| | | |
|---|---:|---|
| pages **with** a grid | 2,905 = 48.1% | MEASURED |
| pages **without** a grid — can never reach the model judge | **3,139 = 51.9%** | MEASURED |

Controls: a key the index holds resolves; an impossible handle returns nothing.

### 3.4 The latch

Denominator = 6,044 pages, by driving the real `handles()`.

| | before | after |
|---|---:|---:|
| skipped | 5,788 | 4,437 |
| re-walkable | **256** | **1,607** |
| rejections carrying **no** verdict and **no** decider | 1,351 | re-admitted |
| rejections that are attributable | 2,647 | still skipped, correctly |

TikTok, measured read-only: **939 of 2,446** rejections, and **all 939 are unattributable** — that
store carries no verdict or decider field at all.

### 3.5 The four brains — rubric bytes hashed at the network boundary

| platform | mode | rubric sha256 (first 12) | bytes | distinct? |
|---|---|---|---:|---|
| tiktok | memes | `28c05f855e13` | 4,918 | yes |
| tiktok | edits | `258d5590748b` | 9,714 | yes |
| instagram | memes | `46a1a4d89cbc` | 5,749 | yes |
| instagram | edits | `eb5bcc28a170` | 10,545 | yes |
| **NEG** bogus platform | memes | `f81c4b39bd4f` | 2,126 | **5th, distinct** |
| **NEG** tiktok | bogus mode | `28c05f855e13` | 4,918 | **⚠️ = tiktok/memes exactly** |

**The recorded claim that the brains share a rubric is REFUTED at HEAD** — all four are
byte-distinct. Two negative-control findings survive:

1. **A bogus platform silently served the bare rubric** — a genuinely different prompt, 2,126
   bytes, measured at 74.0% against the platform-aware 86.0%. **Fixed this round: it now refuses.**
2. **⚠️ A bogus mode silently becomes the memes rubric**, because the mode resolver falls back to
   the default. `both` and `emails` are *valid* modes that also return the memes rubric — **four
   run modes, two briefs.** NOT FIXED (the resolver is outside this round's claim); named here.

### 3.6 What the judge is told, and what it receives

**The seven-key whitelist** (`free_judge.facts_block`): `posts`, `video_posts`, `captions`,
`handle`, `full_name`, `biography`, `found_via`. Of the 8 keys the TikTok side packs, **4 are
dropped silently** and `posts` was **dropped a second time** by requiring `video_posts` as well —
so the TikTok brains received **at most two lines: handle and biography.** The second drop is
fixed here; the first half is in a file another round holds.

**The TikTok facts, driven against a real captured payload with a control:**

| | sent | true | |
|---|---:|---:|---|
| video count | **5** | **360** | MEASURED |
| across 18 real captured authors | median understatement **168×** (min 6×, max 895×) | | MEASURED |
| display name non-empty | **0 of 18** | 18 of 18 have one | MEASURED |

⚠️ **One correction to the recorded claim:** it is *not* "None from both then falls back". The
second term returns a **real but wrong number** — our own crawl count, capped at 20. A search
finds both key names present and populated; only executing the chain shows the account-level
number is nowhere in it.

**Input resolution is uncontrolled** — measured by decoding the base64 actually in the payload,
n=600 sampled grids:

| path | median | distinct sizes | spread | tail |
|---|---|---:|---|---|
| contact sheet | 465×760 | 73 | 6.0× | 67 sizes seen ≤3 times |
| single cover | 311×552 | 15 | **22.9×** | floor **103×183**, ceiling 760×760 |

The reject bars were fitted across that mixture with **no size recorded on any verdict**. Not
fixed — any floor changes the bytes of every prompt and invalidates the existing safety numbers.

### 3.7 The Instagram exemplar pack — CONFIRMED 8 of 8 TikTok

All 8 exemplars live under a `*_tiktok*` capture directory; **8 of 8 handles appear in the TikTok
mark file and 0 of 8 in any Instagram mark file.** All carry 8 distinct hashes, so the "same cover
pasted twice" claim stays refuted.

**A correct pack is available and was NOT shipped.** From his in-sheet Instagram marks: 142 pages,
of which **33 score ≥9 with a grid on disk and 56 score ≤2** — comfortably a 4+4 pack. It is
written as a **proposal** only, because the shipped design is an approval gate: the funnel may
propose, never promote. Promoting a pack he has not approved would defeat the mechanism.

### 3.8 The end-to-end run — 50 per brain

Denominator = pages that had a grid on disk, 50 per brain.

| brain | captured | entered judge | **judged** | rejected | kept | torn | errors |
|---|---:|---:|---:|---:|---:|---:|---:|
| instagram / memes | 50 | 50 | **50** | 19 | 31 | 0 | 0 |
| instagram / edits | 50 | 50 | **50** | 28 | 22 | 0 | 0 |
| tiktok / memes | 50 | 50 | **50** | 26 | 24 | 0 | 0 |
| tiktok / edits | 50 | 50 | **50** | 35 | 15 | 0 | 0 |
| **total** | **200** | **200** | **200 = 100%** | 108 | 92 | **0** | **0** |

**Every page that had a picture was judged. None was lost, none came back torn, none errored.**

The four brains also *behave* differently, not merely receive different bytes — the reject rate
runs 19 / 28 / 26 / 35 out of 50. That is the rubric reaching the model and changing the answer.

**108 of 108 rejections carry the model's own sentence.** Before this round's commit that number
was 0 of 5,827.

Clock per page: **median 9.13 s, p90 28.07 s, max 152.54 s** — median and tail separately, because
a mean over one 152-second page would misdescribe every other page in the set.

Models that answered: `nex-agi/nex-n2-mini` 191, `z-ai/glm-5.3-flash` 9.

⚠️ **This measures the stages the judge owns.** `paid` and `delivered` are **NOT MEASURED HERE** —
this driver buys no profiles.

**Sanity watch, live, armed on every page:** a page delivered with no image · a rejection with no
reason · a rejection with no model sentence · a judged page with zero model calls. **ALARMS: 0.**

Its positive control was run first, before any live page: with the model stubbed, a confident
REJECT produces `drop=True` with a reason and a sentence, a WANT produces `drop=False`, and a torn
answer produces `drop=False` — **a torn answer is never a rejection**, which is the property that
matters most and the one this project has broken before.

---

## 4. WHAT WAS REFUSED OR NOT DONE

- **The TikTok half of the latch.** Identical defect, 939 pages, all unattributable. The file is
  held by another live round and dirty in the working tree. **Handover requested and recorded; the
  patch was handed over rather than applied.** A round published stale line numbers this week by
  measuring a file that moved under it.
- **The TikTok facts fix.** Same file, same reason. Patch handed over in full.
- **`capture_headroom = 0`**, the one-line operational fix that moves the camera from 1.84% to
  100% of fresh pages at zero vendor cost. `config.json` is held by another round. **And it should
  not ship alone:** an uncapped camera with the other two faults unaddressed delivers zero with
  5,000 photographs instead of 50.
- **The 0x08 wall-detection arm.** Four literal backspace bytes where JavaScript word boundaries
  were meant, so arm 2 of 4 can never match — **confirmed at byte level, with a control proving
  the regex is live and merely unmatchable.** ⚠️ But the brief calls it "the structural one" and
  that is **wrong**: the broken arm is *phrasal*; the structural arm (a password field) is arm 3
  and works. Wall detection fires on 696 of 3,292 records via the other three arms, and no page is
  provably lost to arm 2. Fixing it also moves pages from a free screenshot into a **paid** grid.
  **Left deliberately, named precisely.**
- **The input-resolution floor.** Not a one-liner; it needs its own A/B.
- **A judging rule.** None added, loosened or tightened. Not this round's to touch.

---

## 5. WHAT I GOT WRONG

**1. My test fixtures collided with real data and dumped 1.2 MB of it.** I used the handles
`a`/`b`/`c`. **`a` is a real handle in his store**, so the guard failed *and* `assertNotIn` printed
the entire 6,044-page container into the log. Fixtures are now unmistakable and the guard asserts
on a computed set, never on membership.

**2. My own new test asserted the wrong thing.** I claimed `"tiktokk "` must be refused. It must
not — the platform match is a *prefix* match on purpose so `tiktok_edits` keeps working. **I
corrected my test, not the code.**

**3. I broke a passing test and had to decide who was right.** My platform refusal broke a suite
that passed `"something-else"` as a stand-in platform while testing a property about the *mode*
argument. The platform was incidental, so I removed the sentinel and pinned the new refusal with
three tests of its own — a deliberate update, not a green-washing.

**4. A sub-agent's spy latched the gate off and produced four false zeros.** Its stub *raised*
instead of returning; `should_reject` counts that as a model failure and the gate disables itself
after 12 consecutive ones, so it measured 12 payloads out of 600 and reported "nothing measured"
four times. Caught by its own positive control, fixed, re-run at 600/600.

**5. Two headline facts in the brief did not survive checking**, and I would rather say so than
inherit them: the "3.6×" is **2.78×** as stated, and the camera's "900-second timeout read as a
login wall" is **refuted** — the navigation timeout is 45 s, the only 900 in the file is a 900
*millisecond* scroll settle, and a navigation failure is recorded as an error that **skips the
classifier entirely**, so it can never become a login wall.

**6. The "discovered 15,323 → judged 0" arithmetic conflates two runs.** The provenance file is
overwritten by every run and **four meme runs overlapped that night**. The checkpoints prove the
5,029-page walk made **≥711** judge calls, not 0. The conclusion survives — that walk still judged
nothing — but the attribution does not, and the "byte-identical delivered file" fact is now
**stale**: that file was rewritten later the same night.

**7. And the fault nobody had named: the run everyone reasoned about was a test-harness run.** All
711 picture-bearing pages died on an exception whose name appears **nowhere in the codebase**, and
the log for exactly those two runs records the ledger redirecting itself because *"entry point is
under tests/"*. That explains `passed 0` and `master_appended 0`. It does **not** explain the
no-cover pages, because the camera is free and needs no vendor. **Three independent faults, not
one.**

---

## 6. MONEY AND SAFETY

**Vendor spend: 216 model calls = $0.0192, against a cap of $1.00**, by **this round's own call counter** —
the shared ledger carries a round id on zero rows and moved during a round that made no calls, so
a delta cannot attribute anything. **No funnel was run**; the only calls were the judge stage
driven directly.

**Seen store — RE-VERIFIED AT PUBLICATION, not only at check time.** Against the pre-round backup:
**6,044 → 6,058**, of which **0 removed by me** and **+14 added by funnels running concurrently**.
This round changed the *read* rule, not the store: no page record was rewritten, which is why the
removal count is zero and the re-admission of 1,351 pages takes effect without touching a byte of
his data. **No fixture handle reached the live store** — asserted on a computed set, not by
membership, because the first version of that guard dumped 1.2 MB of live records into a log.

**Campaigns SHA — re-verified at publication:** `8e02f8d6f6307ae8` / `7a029ee5447cddd8`, 5
campaigns, **UNCHANGED**.

**Backups, taken before any change and verified by hash, not assumed:** config, spend,
master_leads and all five seen stores — **8 of 8 verified** by comparing the copy's sha256 against
the source.

**What was killed: nothing.** No Python process was signalled. All four local servers held
**identical process ids** from the first check of the round to publication, checked with the
listening-port table and a process query, never a command-line text match — a process filter once
matched its own command line and reported two live where there were none.

**Disk: NOT MEASURED.** This round deleted nothing and wrote no bulk data.

**Test writes:** every write in the new suite goes to a temp directory. The suite asserts on every
run that no fixture handle reached the live store — a previous round poisoned it with 138 fixture
pages.

---

## 7. WHAT TO DO NEXT, RANKED

**1. Decide the camera bound deliberately, because it decides what "delivered" means.** Today it
photographs `max(50, target × 15)` pages while the walk consumes every fresh page, so at target 15
that is 225 photographs against 12,237 walked — and the remaining 12,012 are delivered with no
picture and no model verdict. Either set `capture_headroom` to 0 (free, but hours of browser time
for 12,000 pages) or lower the target so the walk and the camera agree. **The run now prints this
consequence out loud.**

**2. Check what is launching the funnel.** The run behind "judged zero" was driven from a `tests/`
entry point with vendor calls stubbed to raise; the ledger said so in the log and nobody read it.
A run that cannot buy anything will deliver nothing however well the judge works.

**3. Take the two handed-over patches** into the file that holds them: the TikTok latch (939 pages,
all unattributable) and the TikTok facts (a 360-video page arriving as 5, and a display name that
is structurally always empty).

**4. Approve or reject the proposed Instagram exemplar pack.** The Instagram brains are currently
taught with 8 TikTok pages out of 8. A correct 4+4 pack exists from his own marks and is waiting
on the approval gate. This is not an accuracy claim — a prior round measured the change as not
detectable at n=50 — it is a correctness one.

**5. Decide what a bogus *mode* should do.** A typo in a mode string silently becomes the memes
brief, and two *valid* modes do the same: four run modes, two briefs.

---

## 8. PATHS

Paths use `%USERPROFILE%`, which File Explorer expands. **No port numbers** — start the dashboard
from its launcher, because the port is not stable between runs.

| what | path |
|---|---|
| the funnel, the latch, the camera bound | `%USERPROFILE%\OneDrive\Desktop\clipper finder\clippershq\meme_finder.py` |
| the judge, the rubrics, the facts block | `%USERPROFILE%\OneDrive\Desktop\clipper finder\clippershq\free_judge.py` |
| the camera | `%USERPROFILE%\OneDrive\Desktop\clipper finder\clippershq\page_capture.py` |
| this round's tests | `%USERPROFILE%\OneDrive\Desktop\clipper finder\tests\test_bl1478_latch_and_reason.py` |
| the proposed Instagram pack, awaiting approval | `%USERPROFILE%\OneDrive\Desktop\clipper finder\scratch\bl1478_ig_pack_proposal.json` |
| the stage-count driver and its raw rows | `%USERPROFILE%\OneDrive\Desktop\clipper finder\scratch\bl1478_stagecount.py` |
| his grading sheets — the honest denominator | `%USERPROFILE%\OneDrive\Desktop\clipper finder\output\` — the folders whose sheet mark file he filled in |
| dashboard launcher (use this, not a saved address) | `%USERPROFILE%\OneDrive\Desktop\clipper finder\tools\dashboard_launcher.py` |

---

*No creator handles, addresses, credentials or lead-store rows appear in this document. Model
identifiers are vendor product names, not personal data.*
