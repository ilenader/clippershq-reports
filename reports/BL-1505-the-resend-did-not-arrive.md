# BL-1505 — the resend did not arrive, and the picture chooser was wrong across 708 pages

> **Reading this cold?** This project runs an automated funnel that finds social-media pages
> worth contacting. A vision model — the "judge" — is shown a picture of a page and decides
> whether the operator would want it. It learns from **worked examples**: real pages he picked
> himself. This round was asked to ingest a resent list of meme pages and build material from
> them.
>
> Creator handles are redacted throughout. No sample image is published — see §4. No port
> numbers appear.

---

## ⚠️ THE RESENT MEME LIST IS NOT ON THIS MACHINE. I searched four ways and the search proves itself: the ten handles the brief quotes as examples **are** findable, so a zero from it is a measurement. **Nothing that looks like a resent list exists** — in the tree, the paste cache, the transcripts, or anything written today.

## SO THE MEME SIDE IS STILL 46 ACCOUNTS, NOT ~108, and **35 of those 46 have material** — unchanged from yesterday, because there was nothing new to ingest.

## ⚠️ BUT THE PICTURE CHOOSER WAS WRONG, AND FAR MORE WIDELY THAN THE BRIEF SAYS. `_grid_index` keeps the **newest** file per page. Measured over every PNG under `output/` — 20,350 files, 11,159 pages — **3,031 pages (27.2%) have more than one picture**, and the rule now returns a different one for **708 of them (6.34%)**. It was not three pages.

## AND THE FIX IS THE RULE, NOT THE THREE ENTRIES. Three of his 10-scored pages resolved to **45 KB, 116 KB and 26 KB** crops while full sheets of the same pages sat on disk at **478 KB, 522 KB and 300 KB**. All three now resolve to the full sheet — and so does every other page with the same shape, including 18 low-scored pages a sibling round found were each showing **a different round's photograph**.

## ⚠️ AND I FOUND FOUR MORE FAILURES OF MY OWN, FROM AN EARLIER ROUND. My BL-1496 threshold change (13→10 posts) left four assertions red in a suite I had mis-attributed as pre-existing. All four repaired.

**Money: $0.0036 of a $2.00 cap, 10 billed calls** counted by this round's own counter.

---

# 1. ROUND ID, DATE, AND WHAT I WAS ASKED TO DO

**BL-1505**, 2026-09-05. Ingest the resent meme list, fetch fresh material, build and disqualify
sheets, and fix the displaced-grid defect. **Produce material, not verdicts** — nothing was
wired into the judge.

**Before filing.** The reports clone was checked to exist *first*, because a claim filed while
it is missing records `reports_checked=false` and this repo has silently overwritten four
published reports under exactly that condition. **BL-1504 was already claimed by another
session**, so this is BL-1505. The listening-port table (never a command-line grep, never
`dashboard/.running.json`, which has claimed a dead pid since 30 August) showed one Python
listener — his sheet server. Nothing was killed. Free disk re-read throughout: never below
367 GB against a 5 GB floor.

**Concurrency, recorded.** `clippershq/meme_finder.py` had two other claimants. I asked, and a
peer released `_grid_index` explicitly; another asked me for two different functions in the same
file and I released those. Every edit re-read the file at the moment of editing, because two
rounds moved ~200 lines in it today.

---

# 2. THE TABLE

| # | The thing | Before | After | Proof |
|---|---|---|---|---|
| 1 | The resent list | expected ~108 | **not on this machine** | 4 searches, needles as control |
| 1 | Meme accounts with material | 35 of 46 | **35 of 46** | nothing new to ingest |
| 4 | Pages with >1 picture on disk | unknown | **3,031 of 11,159 (27.2%)** | IHDR read, no decode |
| 4 | Pages the chooser now resolves differently | — | **708 (6.34%)** | old rule vs new, same data |
| 4 | His 10-scored pages on a thin crop | **3** | **0** | 45→478, 116→522, 26→300 KB |
| 4 | Fix category | — | **GENERAL** | the rule changed, not 3 entries |
| — | Tests left red by my own BL-1496 | **4** | **0** | repaired, boundaries both sides |
| — | Anything wired into the judge | — | **nothing** | material only |

---

# 3. WHAT WAS MEASURED

## 3.1 ⚠️ THE RESEND DID NOT ARRIVE

The brief says he was asked to resend the meme pages as one plain labelled list, that "this is
that resend", and to expect ~63 Instagram + ~45 TikTok. **It is not here.**

**The search is self-controlling.** Last round I nearly published a false absence because I
searched by *shape* — files ≥55% handle-shaped tokens — and his lists turned out to be a URL
list and a prose markdown table, which fail that test by construction. So this time I searched
by **identity**: the ten handles the brief itself quotes as examples. If the search works, they
appear; if they appear and nothing else does, the absence is real.

| where | result |
|---|---|
| whole tree, by the ten named handles | found in **old graded-page files** (9 of 10, dated 28–31 Aug) and in the brief itself (10 of 10) |
| `~/.claude/paste-cache`, all **10** pastes dated today | **0 of 10 carry them** — every one is a round brief |
| session transcripts since 04 Sep | **one** hit: this session, i.e. the brief text |
| every file written today with ≥20 handle-shaped lines | **7 files**, all outputs of my own last round and a peer's |

The needles are findable, so the instrument works, and it still returns nothing resembling a
resent list. **Nothing was ingested, because there was nothing to ingest.**

⚠️ **What that means for the numbers:** the meme side remains the **46** accounts from the
earlier sets (31 TikTok + 15 Instagram, sent 8 and 13 August as share-URLs and a prose table),
of which **35 have qualified material** — 23 TikTok and 12 Instagram. It is not 108, and no
figure in this report assumes it is.

## 3.2 THE ELEVEN ACCOUNTS WITH NO MATERIAL — retried, and now they have a definite answer

Yesterday these were UNKNOWN. A retry today is cheap and turns most of them into a real state:

```
TikTok    6 accounts   still 0 items of their own from the search route, on both days
Instagram 2 accounts   NOT FOUND / PRIVATE  <- a private page is PERMANENT, not a retry candidate
Instagram 1 account    9 posts, ALL PHOTOS  <- there is no video to fetch
```

**So of the 11, only the 6 TikTok remain genuinely unknown**, and their consistency across two
days makes "unreachable through this route" the better description than "try again". The
per-account TikTok route is a search with the handle as the keyword — a **partial substitute for
a user-posts endpoint by design**. A page it cannot reach is UNKNOWN, never a reject.

## 3.3 ⚠️ THE PICTURE CHOOSER — the defect is 708 pages, not three

`_grid_index` maps each page to one picture on disk. It kept the **newest** file. Measured by
reading the PNG header only — 24 bytes, no decode — over every PNG under `output/`:

```
   PNGs indexed            20,350
   distinct pages          11,159
   pages with >1 picture    3,031   (27.2%)      worst case 156 copies of one page
   pages the OLD rule and a richness rule disagree on   102 by dimensions
   pages whose chosen file MOVED under the new rule    708   (6.34%)
```

A sibling round independently found the same shape from the other direction: of 18 low-scored
pages it checked, **18 of 18** were being handed **a different round's photograph** — so an
exemplar would have shown the model a page he never graded, wearing his grade.

**THE HARD PART, AND I GOT IT WRONG FIRST.** BL-1419 deliberately changed this rule *from*
"largest file wins" *to* "newest wins", for a good reason: a bigger PNG is usually a picture with
**more in it**, i.e. the account at its busiest, so size-preferring reached back through history
and served a photograph of a different page-in-time. Any fix that prefers size reintroduces
exactly that.

So I ranked by **pixel area** instead — layout, not content — reasoning that a full sheet is
465×992 and a crop is 155×275. **That fixed 102 pages and none of the three the brief names**,
because every copy of those three is **the same 465×992**: the thin capture is not a smaller
picture, it is *the same canvas mostly unpainted*. At equal dimensions the only available signal
of how much was drawn is the compressed size.

**The shipped rule:** among copies **within 30 days of the newest**, prefer the largest pixel
area, then the most bytes; **outside that window, newer always wins**. The window is the guard
against BL-1419's defect — the richer files here are **4.8, 4.8 and 6.0 days** older than the
crops that displaced them, and across all 102 dimension-disagreements the displacing file was
newer by a **median of 1.6 days, p90 3.9, max 11.0**. Thirty days is comfortably above every
observed displacement and far short of "history".

**Six controls, all passing:**

```
a thin crop 2 days newer LOSES to a full sheet                        PASS
a lone file is returned unchanged (inert where nothing to choose)     PASS
a LARGER sheet 400 days old cannot beat a fresh one  (BL-1419)        PASS
inside the window the richer sheet wins                               PASS
inside the window, MORE BYTES at equal pixels wins   (the fix)        PASS
OUTSIDE the window, a far bigger old file still LOSES (BL-1419)       PASS
```

**Result on his three pages:**

| was | is |
|---|---|
| a 45 KB crop | the **478 KB** full sheet |
| a 116 KB crop | the **522 KB** full sheet |
| a 26 KB crop | the **300 KB** full sheet |

**FIX CATEGORY: GENERAL.** The rule changed, not three entries. Re-pointing three files would
have been LOCAL and would have recurred on the next capture — and of seven past fixes tested by
driving them here, only 1 of 7 was general and 3 of the 6 local ones were still failing.

⚠️ **The remaining weakness, named rather than hidden:** bytes are a *proxy* for drawn content
and are foolable by padding appended after the image data. No real PNG in this tree does that,
but a measure of actual content — tile count, or blank fraction against the builder's canvas
`RGB(24,24,27)` — would be strictly better and is what a round with an image-decode budget
should use.

## 3.4 ⚠️ VERDICTS DO MOVE, AND THAT IS THE POINT

The index feeds the exemplar pack, so this changes what the brains are shown — deliberately, for
**3 of the 8** pinned exemplars.

**My first control could not have seen it.** It hashed `os.path.basename`, and the thin capture
and the full sheet **share a filename**; only the directory differs. It printed a reassuring
unchanged hash whichever picture was chosen — a control blind to the thing it was watching for,
which is worse than no control. Rebuilt to hash the **path and the file size**:

```
   pinned pack signature   BEFORE ca1cfda2452a   AFTER 2832bb5c2f9f   MOVED
   pinned exemplars whose FILE changed: 3 of 8
```

**No judging rule was added or loosened**, and no rubric was touched.

## 3.5 ⚠️ FOUR TESTS LEFT RED BY MY OWN EARLIER ROUND

`tests/test_meme_finder.py` carried **four** assertions about `MIN_TOTAL_POSTS`, which my BL-1496
round lowered from 13 to 10 on his instruction. I fixed the pin in one suite at the time and
missed these — because this suite had been red for an *unrelated* reason since before that
round, so I filed it under "pre-existing" and stopped looking. **A suite that is already red
hides the next failure**, and that is how four of them survived a bisect.

| assertion | what it said | repaired to |
|---|---|---|
| the floor pin | `MIN_TOTAL_POSTS == 13` | 10, with the justification rewritten — 13 was *fitted* to his examples, 10 he **dictated** |
| twelve posts | "twelve posts is rejected" | twelve is now **KEPT** and nine is still cut — **both sides of the new boundary** |
| the undercount fixture | expected prose about 10 posts | 8 posts, asserts the veto |
| every-rule-fires | expected `too_few_posts` | 8 posts |

⚠️ **And a trap inside the repair that only driving it revealed:** shortening a post list also
shortens its **date span**, and a span of ≤7 days with a recent newest post trips the
`just_started` rescue, which sets `tiny = False`. So a fixture that "should" trip the posts floor
silently stops tripping it for a reason unrelated to the floor. The posts are now spaced three
days apart to keep the span wide.

**Result: 5 failures → 1.** The one remaining is a `SeenSet` merge test that is genuinely
unrelated and **not mine** — I have left it red rather than sweep it into this round, because I
have not diagnosed it and a repair I cannot justify is worse than a red I can name.

## 3.6 ⚠️ THE GUARD ON THE OLD RULE — RE-PINNED, RENAMED, AND PROVED IN BOTH DIRECTIONS

`tests/test_bl1419_defects_and_bands.py` pins `_grid_index`'s behaviour, and my change turned it
red. **I did not run it** (§5.6). A peer round found it.

⚠️ **And the obvious repair would have destroyed the record.** The class was named
`TheGridIndexPicksTheNewest`; swapping the expected path and moving on would have erased *why*
newest-wins existed. So it is **renamed** the richest-recent-sheet name, the invariant
is restated in the file in three parts, and the real-collision test now asserts the **shipped**
rule rather than a paraphrase of it.

**Four new guards, deliberately synthetic.** ⚠️ **The real tree cannot exercise the recency
window**: the largest displacement anywhere in it is **11.0 days against a 30-day window**, so a
guard reading only real files can never tell this window from **no window at all**. It would pass
for years and stop meaning anything the first time a corpus went stale.

```
test_a_thin_crop_does_not_displace_a_full_sheet_from_the_same_week
test_an_ancient_busy_snapshot_still_LOSES            <- BL-1419's decision, guarded
test_the_window_is_a_real_boundary_and_not_decoration   <- wins 2d inside, loses 2d outside
test_a_page_with_one_picture_is_untouched
```

**Proved by mutation in both directions**, because a guard that passes proves nothing until it
can fail:

| mutation | result |
|---|---|
| revert the rule to **newest-wins** | **3 guards fire** |
| remove the **window** (largest-wins across all history = BL-1419's defect) | **2 guards fire**, including the ancient-snapshot one |
| restored | **25 of 25 green** (was 21 tests) |

**Suites re-run after the repair:** `grid` 2/2, `bl1419` 1/1, `camera` 1/1, `sheet` 7 of 8. The
one red there, `test_bl1444_board_and_sheets`, is **pre-existing** — proved by reverting my
change and re-running, where it still fails.

---

# 4. WHAT WAS REFUSED OR NOT DONE

- **Nothing was ingested**, because the list is not here. I did not substitute a different file
  that merely contains meme handles — the brief warns against exactly that, and it would be
  indistinguishable from his list to anyone reading later.
- **Nothing was wired into the judge.** No pack constant, no `EXEMPLAR_PACK_PLATFORM` row, no
  rubric, nothing written to `approvals.jsonl` — which is superseded and which the funnel no
  longer reads at all.
- **No sample image is published.** The handle detector reads a 7px watermark in a control but
  **misses a real alpha-blended `@handle`** legible to the eye at 6×, and a JPEG's compressed
  bytes can trip a handle pattern by chance. I cannot prove a sheet clean, so none is published;
  they are on disk for him.
- **The unrelated `SeenSet` failure was left red** (§3.5).
- **No seen-store row was written, rewritten or deleted.**

---

# 5. WHAT I GOT WRONG

1. **⚠️ MY FIX DID NOT FIX THE THING IT WAS FOR, AND I ONLY FOUND OUT BY MEASURING.** I reasoned
   that pixel area separates a full sheet from a crop while file bytes are content-dependent —
   correct in general, and **wrong for these three pages**, where every copy is the same 465×992
   and the crop is the same canvas unpainted. I had already written and driven the rule, and it
   passed five controls, before I checked whether it moved the pages the brief actually named.
   **Controls that pass prove the rule you wrote, not the rule you needed.**
2. **⚠️ MY "NO VERDICT MOVED" CONTROL WAS BLIND BY CONSTRUCTION.** It hashed the picture's
   *basename*, and the two candidates share a filename — so it reported "unchanged" whichever
   was chosen. A control that cannot see the change it guards is worse than none, because its
   green is persuasive.
3. **I wrote a control that encoded my own wrong premise.** It asserted "file bytes never win",
   which I believed until the measurement above. I rewrote it to test the real requirement — an
   *old* file must not win for being bigger — rather than deleting it to make the suite green.
4. **My backup helper hard-coded each store's body key**, which is a lookup table pretending to
   be a measurement. Rewritten to find the body **by shape** — and my first shape rule was also
   wrong, requiring most values to be dicts, which refused a store that maps id → float. The
   working discriminator is **size**: a wrapper has three keys, a body has thousands.
5. **I mis-attributed a red suite as pre-existing and stopped looking**, which hid four failures
   of my own for a full round (§3.5).
6. **⚠️ I PUBLISHED THIS REPORT WITH THE GUARD ON THE RULE I REPLACED LEFT RED, AND I DID NOT
   RUN IT.** A regex `-k` matched no suites, so I fell back to three separate runs — `pack`,
   `meme_finder`, `exemplar` — and **silently dropped `bl1419` and `grid` from that list**. The
   suite that pins `_grid_index`'s behaviour is the one suite that had to be run, and it was the
   one I lost. A peer round found it and told me. **A fallback that quietly narrows what it
   checks is worse than the failure it was working around**, because the narrower run still
   prints a green summary. Corrected in §3.6 below.

---

# 6. MONEY AND SAFETY

**$0.0036 of a $2.00 cap. 10 billed calls** — 6 TikTok, 4 Instagram — counted by this round's own
counter, never a ledger delta.

⚠️ **The TikTok calls were booked EXPLICITLY, because that client books nothing on its own** —
no autoflush, no flush method. Without an explicit booking at the end its calls are invisible to
the ledger entirely. The Instagram client is the opposite problem: it **autoflushes on a timer
under a generic label**, which put **$0.101526 of a previous round's spend into an unattributed
bucket — 23 rows, a 61% under-count by campaign**. Both are attribution defects in opposite
directions and both are worth fixing at the client.

**Backups: 11 of 11 verified**, each by sha256 against the source, with three controls: a
corrupted copy must be detected, the shape finder must **refuse** a document it cannot read, and
it must still find a real body (so the refusal control cannot pass vacuously).

**Seen stores at publication, ROW KEY SETS found BY SHAPE:** TikTok **2,446** · meme **6,125** ·
clip **2,193** (a top-level LIST) · repost **1,715** (top level IS the rows, values are scalars) ·
Spotify **1,902**. **All five unchanged.** The method used for each is printed, not assumed.

**Ports:** re-checked immediately before every write under `clippershq/`. His sheet server was up
throughout and untouched. No `taskkill` was issued.

---

# 7. WHAT HE SHOULD DO NEXT — RANKED

1. **⚠️ THE MEME LIST STILL HAS NOT ARRIVED.** Three rounds have now looked for it. What exists
   is 46 accounts from August. If he wants ~108, the list needs to be sent somewhere it lands as
   a file — pasting it into a message works, since that is how the 130 edit handles survived.
2. **The picture chooser is fixed for 708 pages** and three of his 10-scored exemplars now show
   the full sheet. Worth a look at whether those three exemplars now read as he expects.
3. **Two of his meme accounts are private and one posts only photos** — those three are
   permanent states, not retry candidates. Six TikTok accounts are unreachable through the
   search route on two consecutive days.
4. **Both vendor clients mis-attribute spend**, in opposite directions (§6). Neither loses money;
   both lose the ability to say which round spent it.
5. **A richness measure that counts drawn content** — tiles, or blank fraction against the
   canvas — would replace the byte proxy in the grid chooser and cannot be fooled by padding.

---

# 8. FULL PATHS

Relative to the repository root.

**Changed:** `clippershq/meme_finder.py` — `GRID_RECENCY_WINDOW_S`, `_png_area`, `_pick_grid`,
and the body of `_grid_index` · `tests/test_meme_finder.py` — four fixtures repaired.

**Instruments, all re-runnable:** `scratch/bl1505_backup.py` (shape-based, three controls) ·
`bl1505_measure_grids.py` (the 20,350-file census) · `bl1505_drive_grid.py` (six controls plus
the before/after) · `bl1505_fix_tests.py` · `bl1505_stage2_build.py` / `_stage2_ig.py` (the
retry) · `bl1505_leakscan.py`.

**Read but never modified:** all five seen stores · `config.json` · his three supplied sources.

**Backups:** `backups/bl1505_<timestamp>/`.

https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/BL-1505-the-resend-did-not-arrive.md
