# BL-1500 — he sent 176, not ~200, and 151 of them now have reference material

> **Reading this cold?** This project runs an automated funnel that finds social-media pages
> worth contacting. A vision model — the "judge" — is shown a picture of a page and decides
> whether the operator would want it. To judge well it needs **worked examples**: real pages he
> picked himself. There are four judges — Instagram and TikTok, each in "memes" and "edits" mode.
> Until today all four were shown **the same eight TikTok pictures**.
>
> Creator handles are redacted throughout. Paths are relative to the repository. No port numbers
> appear. **No sample image is published** — see §4 for why.

---

## HE IS RIGHT THAT THERE WERE NO EXAMPLES, AND HE IS RIGHT ABOUT THE CAUSE. All four brains were shown the same eight TikTok pictures. **Five of those eight are 75.7–91.9% bare canvas and two repeat a cover inside themselves.** Three of the four pictures teaching "he wants this" are unfit.

## ⚠️ BUT HE DID NOT SEND ~200. HE SENT **176**, AND THE MEME HALF IS **46**, NOT ~105. Edit: 66 TikTok + 64 Instagram. Meme: **31 TikTok + 15 Instagram**, sent three weeks earlier in two different formats. Short by **24** against his own belief and by ~59 against what this round was told to expect.

## AND NOW **151 OF THE 176 HAVE REAL REFERENCE MATERIAL** — fetched fresh today, 851 videos, 1,702 frames, **0 decode failures, 0 leftover files, 0 repeated covers**. Per brain: TikTok/edits **57 of 66**, Instagram/edits **59 of 64**, TikTok/memes **23 of 31**, Instagram/memes **12 of 15**.

## ⚠️ THE REJECT SIDE IS NOT MISSING THE WAY EVERYONE THOUGHT. It is short on **brain assignment**, not on pictures: **416 of 428** reject-side pages already have a grid on disk, median 724 KB, already paid for. What is missing is any record of which brain they belong to — **mode is recorded on 0 of his mark rows.**

**Money: $0.166542 of a $2.00 cap**, 187 billed calls counted by this round's own counters.

---

# 1. ROUND ID, DATE, AND WHAT I WAS ASKED TO DO

**BL-1500**, 2026-09-05. Ingest his two supplied lists, fetch 5–10 non-pinned videos per account
**fresh** (everything retained is expired), build a reject side from his low scores, disqualify
unfit pictures, and save the exact bytes a judge would receive. **Produce material, not verdicts** —
nothing was wired into the judge.

**Before touching anything.** The listening-port table (never a command-line grep, and never
`dashboard/.running.json`, which has claimed a dead server since 30 August) showed **one** Python
listener — his sheet server. No dashboard. Re-checked before every write. Nothing was killed.
Backups of config, the ledger, the lead store and all five seen stores: **9 of 9 verified by
sha256 against the source**, with a control proving a corrupted copy is detected. Free disk
re-read before every account: never below 368 GB against a 5 GB floor.

⚠️ **My claim was first filed while `../clippershq-reports` was missing**, so it recorded
`reports_checked=false` — the report namespace went unverified. I re-filed once a peer restored
the clone, and re-checked that BL-1500 is free on origin/main immediately before pushing.

---

# 2. THE TABLE

| # | The thing | Before | After | Proof |
|---|---|---|---|---|
| 1 | His supplied lists, parsed | never fully | **176** across 4 sets | two independent derivations |
| 1 | Duplicates | "at least two" | **0** in all four | traced the belief to reel *posts* |
| 1 | Cross-list collisions | unknown | **0** | no labelling conflict to resolve |
| 2 | Accounts with fresh material | **0** | **156** | 851 videos, 1,702 frames |
| 2 | Decode failures | expected ~11.5% | **0 of 851** | probe proved in both directions |
| 2 | Videos left on disk | — | **0** | verified by *listing*, not `*.mp4` |
| 4 | Current exemplars unfit | unknown | **5 of 8** | 17 planted controls, 17 fired |
| 4 | New sheets repeating a cover | — | **0 of 156** | cell-level hashing |
| 5 | Delivered exemplar size | **215×460** | **320×568** | the shipped encoder |
| — | Anything wired into the judge | — | **nothing** | this round produces material only |

---

# 3. WHAT WAS MEASURED

## 3.1 THE TWO LISTS — 176, and the meme half is a third of what was expected

| list | platform | raw | after strip | distinct | duplicates |
|---|---|---:|---:|---:|---:|
| MEME | TikTok | 31 | 31 | **31** | 0 |
| MEME | Instagram | 15 | 15 | **15** | 0 |
| EDIT | TikTok | 66 | 66 | **66** | 0 |
| EDIT | Instagram | 64 | 64 | **64** | 0 |
| | | | | **176** | **0** |

**Provenance, primary sources — not the derived copies:**
* **EDIT 66 + 64** — `scratch/bl1436_handles.py`, from his paste of **2026-08-30**. Stored as
  triple-quoted **strings**; an AST walk for list literals returns 0, which has misled a round
  before.
* **MEME TikTok 31** — `scratch/bl1189_urls.txt`, his mobile share URLs
  (`tiktok.com/@<handle>?_r=1&_t=…`), **2026-08-08**. His surviving raw paste matches the saved
  file byte-for-byte, 31 vs 31, zero drift.
* **MEME Instagram 15** — a **16-row markdown table inside `scratch/bl1240_reference_study.md`**,
  **2026-08-13**. ⚠️ The 16th row is a **reel shortcode, not a handle**, so it is 15 accounts and
  one post; it was never folded into the count.

⚠️ **So the meme list was sent three weeks before the edit list, in two different formats,
neither of them a list file.** That is why it reads as missing: a search for a dense handle list
cannot find a prose table, and every line of the TikTok set carries a query string.

**I nearly published that it did not exist at all.** §5.1.

**Duplicates: ZERO** in all four lists — and zero in his raw paste. The belief that "at least two
are repeated" traces to **five repeated reel shortcodes** in a paste that was never sent or
saved. Those are **posts, not accounts**. **Cross-list collisions: ZERO**, so there is no
labelling conflict to put to him.

**Name flags for his confirmation only, not reclassified** — he is the authority on his own
taste and a name is not evidence: two meme-list handles carry `fx` and `aep`. A third apparent
hit is a substring artefact inside "acc" and I would not put it to him. The brief expected four;
the likelier referent is a different fact — **four of his Instagram meme bios literally read
"Reel creator"**.

**The `edits` matcher, proved on the exact handle that once fired on all 567 files in a
directory:** 17 of 17 controls pass. `edits`→match, `my_edits`→no, `myedits`→no, `edits.co`→no,
`@edits`→match, `1edits`→no, and the handle followed immediately by an at-sign (the local part of
an address) →**no**. The rule is that neither neighbour is in `[A-Za-z0-9._]`, with `@` allowed on
the **left** only — otherwise every URL paste goes invisible, and an address would read as a
handle.

**Zero leading-dot handles across all 176** — checked, not assumed, with `os.walk` throughout.

> ### ⚠️ THE FIRST THING TO TELL HIM
> **He believes he sent ~200. What is on disk is 176, and only 46 of those are meme pages.** The
> edit sets are complete and exactly as he sent them. If he wants 50–100 meme pages per brain,
> that is a genuine resend — ideally as one plain labelled list, since the two meme sets arrived
> as share-URLs and a prose table and have been hard to find ever since.

## 3.2 THE FETCH — fresh, because everything retained is dead

Instagram material on disk is **expired, not absent**: every retained URL returns
`URL signature expired`. I confirmed the contrast directly — on one of his accounts, **9 of 9
FRESH urls returned HTTP 200 with real mp4 headers**, against 39 of 39 expired on disk. So
nothing here reads disk for media.

```
                accounts  videos  decode   frames  deleted  LEFTOVER  pinned    pinned
                          fetched failures  cut     videos   FILES     excluded  UNKNOWN
   TikTok          97      438      0        876     438       0          0        0
   Instagram       79      413      0        826     413       0         65        0
   TOTAL          176      851      0      1,702     851       0         65        0
```

**Decode failures: 0 of 851 (0.00%).** The brief expected ~11.5% (30 of 260, 28 of them
header-valid). **This zero is trustworthy because the probe is proved in both directions** — a
generated file must decode `True` and a valid-header-over-rubbish file must decode `False`, and
both controls fire on every run. The likeliest reason for the difference is that this round takes
the clean `play_addr` render rather than whatever the earlier sample used.

**Pinned posts were excluded, and the flag was present everywhere.** 65 pinned Instagram posts
skipped; **0 recorded as UNKNOWN on either platform**, i.e. the flag was readable on every video
examined. The brief warned it was verifiable on only 8 of 26 pages last time — on this corpus it
was verifiable on all of them, and that is worth knowing because pinned median views are
1,562,246 against unpinned 2,658.

**The no-watermark question, measured rather than assumed.** `download_addr` prints the handle on
every frame, which would burn the answer key into the exemplar. Every mirror is tried in order
and `play_addr` variants are preferred. The brief said the primary host 403s and the third works;
**on the account I probed all nine mirrors returned HTTP 200**, so the rule is not universal —
which is why the fetcher tries them in order and records which answered rather than hard-coding
an index.

**Zero orphans, verified by LISTING the directory** — not by searching for `*.mp4`, because a
hard kill leaves `.part`, `.tmp` or zero-byte stubs that a `*.mp4` search cannot see. Final
state: **1,552 files under the material tree, all PNG, no non-PNG of any extension anywhere.**

**Not reachable:** 20 accounts yielded no frames — 12 TikTok, 8 Instagram. On TikTok the
per-account route is `/v2/search` with the handle as the keyword, which is a **partial**
substitute for a user-posts endpoint by design (my probe returned 19 items of which only 4 were
the account's own). **A page it cannot reach is UNKNOWN, never a reject.** On Instagram, 3
handles would not resolve to a numeric id and the medias call was deliberately **not** sent — a
handle sent there is a billed HTTP 400, and 118 such calls once cost $0.0815 to be told the
argument was the wrong shape.

## 3.3 THE CURRENT EIGHT EXEMPLARS — five are unfit

Measured **per tile**, against the builder's **real** canvas colour `RGB(24, 24, 27)`, read off
`tiktok_finder.py` at source rather than assumed. **17 controls planted, 17 fired, none
discarded** — including one that proves the outer-bounding-box method blind: on a sheet with
interior gaps, per-tile reads **83.3%** and the outer box reads **0.0%**.

The old `grey < 16` rule reads **0.4%** where the truth is **91.9%** — structurally blind,
because the builder paints at grey 24.

| his score | old `grey<16` | **truth, per tile** | tiles ≥90% bare |
|---:|---:|---:|---|
| 10 | 5.4% | **87.8%** | 10 of 12 |
| 10 | 2.8% | **84.3%** | 10 of 12 |
| 10 | 12.3% | **83.9%** | 10 of 12 |
| 1 | 0.4% | **91.9%** | 11 of 12 |
| 1 | 5.5% | **75.7%** | 9 of 12 |
| 10 / 1 / 1 | — | 8.4% / 2.6% / 5.5% | 0 of 12 |

**Two of the eight repeat a cover inside themselves**, confirmed by **cell-level** sha256 and
verified visually. The previous "refutation" — *8 distinct file hashes* — hashed **whole files**
while the claim is about **cells within one file**, so it never addressed the claim at all.

**⚠️ AND THE CAUSE IS RECOVERABLE WITHOUT CHANGING THE PACK.** Three of the five (all scored 10)
resolve to thin 27–119 KB captures, while **full 12-tile sheets of the same handles sit on disk**
at 308–489 KB measuring **2.0%, 5.0% and 5.4% blank with 0 repeats**. `_grid_index` keeps the
**newest mtime**, so the thin capture displaced the good sheet. Re-pointing those three fixes 3 of
5 disqualifications and **both** repeats. The other two are bare in every copy on disk — those
pages genuinely captured 1 and 3 covers.

**Login walls 0 of 8, age gates 0 of 8, private 0 of 8** — and those zeros stand, because the
positive *and* negative controls fired for all three and OCR read 128–942 characters from the
content-rich sheets. ⚠️ **One age-gate false positive was caught and fixed**: the word
`birthday`, OCR'd out of the meme caption *"when you tired of birthday punches"*. Bare `birthday`
and `18+` were removed from the mark list and a negative control now guards it.

⚠️ **A known false negative, stated because a silent one is worse:** the handle detector reads a
7px watermark at real tile scale in a control, but **misses a real alpha-blended `@handle`
watermark** on one on-disk sheet that is legible to the eye at 6×. Alpha-blended text over moving
video is a different problem from small text. **"0 of 8 print their own handle" is therefore not
"no handle text anywhere."**

## 3.4 THE NEW MATERIAL — 151 of 156 sheets qualify

Same battery, same 17 controls re-run against the new sheets rather than taken on trust.

```
   sheets built            156
   with a repeated cover     0
   with an empty cell       24
   fewer than four cells      5
   ⇒ QUALIFIED             151
```

**Disqualification is on EMPTY CELLS, not on pixel blankness**, and that choice is the subject of
§5.2 — blankness on a composed sheet is dominated by letterbox, which is a property of my layout
rather than of his page.

## 3.5 ⚠️ COVERAGE PER BRAIN — the direct answer to his question

| brain | he supplied | material built | **QUALIFIED** | share |
|---|---:|---:|---:|---:|
| tiktok / edits | 66 | 60 | **57** | 86.4% |
| instagram / edits | 64 | 59 | **59** | 92.2% |
| tiktok / memes | 31 | 25 | **23** | 74.2% |
| instagram / memes | 15 | 12 | **12** | 80.0% |
| **TOTAL** | **176** | **156** | **151** | **85.8%** |

**Before today: TikTok edits had 0 reference pages and Instagram edits had 0.** The whole
276-page corpus on disk was graded on the memes brief, before an edits brief existed anywhere.

**What is still missing, per brain:** 9 TikTok edits, 5 Instagram edits, 8 TikTok memes, 3
Instagram memes — **25 accounts**, of which 20 could not be reached by the vendor at all and 5
yielded fewer than four usable frames. **None of the 25 is a rejection**; they are UNKNOWN.

## 3.6 THE REJECT SIDE — short on brain assignment, not on pictures

Every page he sent is a **want**, positive by construction. On an all-positive pool, "says yes
more" and "is right more" are indistinguishable, so a pack of accepts teaches half the question.

Sourced by **provenance** (which sheet wrote the file), not by field shape — a field-shape sweep
classifies 913 files / 171,867 rows as his-mark dialects and would have manufactured a corpus
**55× the real one**. Provenance gives **20 files → 3,116 rows → 1,523 resolved pages**, last
keystroke wins.

| brain | reject-side | at ≤2 | at ≤5 | **buildable today** |
|---|---:|---:|---:|---:|
| tiktok / memes | 442 | 252 | 303 | **235** (+98 where he pressed GOOD on a rejection) |
| instagram / memes | 240 | 98 | 113 | **110** (+34) |
| instagram / edits | 13 | 11 | 13 | **11** |
| **tiktok / edits** | **1** | **0** | **1** | **1** |

⚠️ **The premise that the reject side has almost nothing is wrong, and the reason matters.** The
review sheets bought pictures for the rows they asked him to judge, so **416 of 428 reject-side
pages at ≤5 already have a grid on disk**, median 724 KB. The earlier "only six have any URL" is
about **URLs**; a profile URL is the handle restated, and a **picture** is what the judge needs.

⚠️ **TikTok/edits cannot be filled from his keystrokes: he graded 30 pages there and rejected
exactly one.** The sheet was one-sided by construction. There is a pool of 11 TikTok-edits pages
he scored 6–9 that are **car edits**, a subject the edits brief has since reversed, and 8 of the
11 have a usable picture — that would take the brain from 1 to 9. **It is deliberately excluded**
from the table above and held separately, because it is a reject **by the brief**, not by his
keystroke, and building a pack from it would teach a rule as though he had chosen it.

⚠️ **AND THE REAL BLOCKER IS MODE.** Mode is recorded on **0 of his mark rows**, and no
`sheet_meta.json` carries one. "Edits" is claimed only by two directory names. **Everything else
is called memes only because the shipped config says memes on both funnels** — that is a
convention, not a measurement, and the reject-side meme numbers above rest on it. A peer round
reading the same data with a stricter rule got **0** for both meme brains. Both cannot be right,
and it is a question for him, not something either of us can measure.

**Reversed subjects excluded** with a handle-aware matcher: **naive substring 97 pages, correct
19 — 78 false positives.** 26 of 26 matcher controls pass (`car edits`→hit; `cartoon network`,
`gymnastics`, `oscar`, `carousel`, `car.toon`, `scarface`, `carnival`→no). Only 3 of the 19 are on
the reject side.

**21 mark files excluded**, including **2 that are not independent** — one reproduces the
machine's verdict on 97 of 100 rows and the other on 96 of 100, with **zero rows of text he
typed**.

## 3.7 WHAT A JUDGE ACTUALLY RECEIVES

Measured by calling the **shipped encoder**, never a re-implementation.

| | current eight | **new sheets** |
|---|---|---|
| delivered as an exemplar | **215×460** | **320×568** |
| delivered as a page | 356×760 | **760×760** |
| bytes as sent | 3.6–25.0 KB | 8.3–37.3 KB, median 17.4 |

The exemplar path calls `enc(path, 460)`, not the 760 default — which is why the current pack
arrives as a stamp. The new sheets are **2.9× the pixel area** of the current exemplars on the
same path.

---

# 4. WHAT WAS REFUSED OR NOT DONE

- **Nothing was wired into the judge.** No pack constant, no table row, no change to
  `_approvals_state`, nothing written to `approvals.jsonl`. A peer round holds that work, and a
  live hazard makes it worth stating: the `usable` branch of the pack loader does not pass its
  fallback flag, so anything flipping that gate true without populating the pack would run the
  funnel at **zero exemplars** — an arm measured at 53.0% against a 65.0% constant-answer
  baseline, with one log line as the only symptom.
- **⚠️ NO SAMPLE IMAGE IS PUBLISHED.** The handle detector has a **known false negative** on
  alpha-blended watermarks (§3.3), and a JPEG's compressed bytes can trip a handle pattern by
  chance. I cannot prove a given sheet is free of a burned-in handle, so none is published.
  **The sheets are on disk where he can open them**; only the public copy is withheld.
- **No reject-side pack was built**, only counted. Building one requires the mode question in
  §3.6 answered.
- **The 11-page reversed-subject pool was not used** to fill TikTok/edits.
- **No seen-store row was written, rewritten or deleted** — all five verified unchanged as row
  key sets at publication.
- **His sheet server was left running.** No `taskkill` was issued.

---

# 5. WHAT I GOT WRONG

1. **⚠️ I ALMOST PUBLISHED THAT HIS MEME LIST DOES NOT EXIST.** I searched for a file that was
   ≥55% handle-shaped tokens and under 60 KB; his meme sets are a **URL list** (every line
   carrying a query string) and a **prose markdown table**, and both fail that test by
   construction. I had already told a peer round "the meme list is not on disk" when it pushed
   back with the two paths. It was right and I withdrew. **A search that cannot find a prose
   table returns zero for "absent" and zero for "differently shaped", and I read the wrong one.**
   The corrected finding — 176, not ~200 — is far more useful to him than the false absence
   would have been.
2. **I measured my own ruler and called it his pages — twice.** My first sheet layout used square
   cells and reported a median tile "blankness" of **0.402**. I read that as empty pages and
   switched to 9:16 portrait cells; it got **worse (0.560)**. Only then did I measure his frames:
   aspect **min 0.562, median 1.000, max 2.376**, with 480×854, 480×360, 480×480 and 480×270 all
   common and **only 27.2% within 5% of 9:16**. His pages post mixed aspects, so **no cell shape
   avoids letterbox** and pixel blankness on a composed sheet is mostly my own padding. I went
   back to square (which matches the measured median) and moved the disqualifier to **empty
   cells**, which is a fact about the page rather than about my layout. Two guesses before one
   measurement.
3. **My first decode probe reported a false failure on its very first video.** It resolved
   `ffprobe or ffmpeg` and then passed `-f null -`, an **ffmpeg-only** output option; ffprobe
   exited non-zero on a perfectly good 2.6 MB mp4 and I read that as "does not decode". Had I
   trusted it, the headline decode-failure rate would have been fiction. Fixed, and the probe now
   refuses to report a rate unless a good file reads `True` **and** a header-over-rubbish file
   reads `False`.
4. **I filed my claim blind.** `../clippershq-reports` was missing, so `claim.py` recorded
   `reports_checked=false` and I did not notice the one-line warning. Re-filed once a peer
   restored the clone.
5. **My first client construction used a class name that does not exist** (`ApiClient` for
   `LamaTokClient`) — caught instantly, but it is the same shape as guessing a column name, which
   this project has lost a finding to.

---

# 6. MONEY AND SAFETY

**$0.166542 of a $2.00 cap. 187 billed calls**, counted by this round's own counters, never by a
ledger delta.

| | calls | booked |
|---|---:|---:|
| TikTok `/v2/search`, one per account | 98 | $0.058800 |
| Instagram resolve + medias | 89 | $0.107742 |

⚠️ **AND $0.101526 OF MY OWN SPEND LANDED UNDER `IG_AUX / unattributed`.** The Instagram client
autoflushes on a timer under a default label before a round can name itself, so **23 of my rows
are attributed to a generic bucket** and only 5 carry `BL1500`. My own counter and the vendor's
receipt agree exactly (10 = 7 + 3 on the trial run); the disagreement is purely one of
*attribution*. A round reading the ledger by campaign will under-count this one by 61%.

⚠️ **And the TikTok client books nothing at all** — it has no autoflush and no `flush_spend`, so
its 98 calls would have been invisible had I not booked them explicitly at the end. That is the
same shape as the leak this project has already measured at 38% of a round's true cost.

**Backups: 9 of 9 verified by sha256 against the source**, with a control proving a corrupted
copy is detected as a mismatch.

**Seen stores at publication, compared as ROW key sets** (not top-level keys — that mistake once
made a 2,446-row store read as 3): TikTok **2,446** · meme **6,125** · clip **2,193** · repost
**1,715** · Spotify **1,900**. **All five unchanged. No row written, rewritten or deleted.**

**Disk:** re-read before every account, never below **368 GB** against a 5 GB floor. **851 videos
downloaded and 851 deleted**, verified **after** by listing every directory: **0 non-PNG files
remain**, of any extension.

**The pre-commit guard was proved working before any refusal was trusted** — it exits 1 on a file
carrying a real lead-store address and 0 on a clean file. The planted test file was deleted
immediately and its absence verified.

---

# 7. WHAT HE SHOULD DO NEXT — RANKED

1. **Resend the meme pages if he wants more than 46.** He believes he sent ~200; 176 arrived and
   only 46 of those are meme pages. One plain labelled list per brain would end a search that has
   now cost three rounds.
2. **Answer the mode question** (§3.6). Nothing on disk says which brain a rejected page belongs
   to. Depending on the answer the meme reject side is either ~345 pictures already paid for, or
   zero. That single answer decides whether three of the four brains can have a reject side at
   all.
3. **Re-point three grid entries** (§3.3). `_grid_index` keeps the newest file, and a thin capture
   displaced the full sheet for three of his 10-scored pages. Fixing it repairs 3 of 5
   disqualifications and both repeated covers, without touching the pack.
4. **TikTok/edits needs rejects he has actually rejected.** He graded 30 pages there and rejected
   one. A short edits-mode sheet built from funnel-rejected TikTok edit pages would fix it —
   note the shipped config is `memes` on both funnels, so that sheet does not currently exist as
   something the pipeline emits.
5. **The 25 accounts with no material are UNKNOWN, not rejected** — 20 unreachable by the vendor,
   5 too thin. Worth a retry another day rather than a conclusion.

---

# 8. FULL PATHS

Relative to the repository root.

**Material (handles in directory names — local only):** `output/bl1500_material/` — 156 accounts,
1,702 frames.
**Sheets (de-identified, safe to share):** `output/bl1500_sheets/` — 156 sheets, named
`<list>_<platform>_<digest>.png`, no handle anywhere in the name.
**The map from sheet to handle, LOCAL ONLY:** `scratch/bl1500_sheet_index.json`.

**Instruments, all re-runnable:** `scratch/bl1500_probe_one.py` · `bl1500_probe_ig.py` ·
`bl1500_decode.py` · `bl1500_stage1_reach.py` · `bl1500_stage2_build.py` · `bl1500_stage2_ig.py` ·
`bl1500_sheets.py` · `bl1500_qualify.py` · `bl1500_backup.py` · and the three sub-agents' work
under `scratch/bl1500_agent{A,B,C}_*`.

**Read but never modified:** `scratch/bl1436_handles.py` · `scratch/bl1189_urls.txt` ·
`scratch/bl1240_reference_study.md` (his three supplied sources) · all five seen stores ·
`config.json`.

**Backups:** `backups/bl1500_<timestamp>/`.

https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/BL-1500-he-sent-176-not-200-and-now-151-have-material.md
