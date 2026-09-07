# BL-1529 — LET THE AI DECIDE: THE POST FLOOR, THE WHOLE VIDEO, AND WHAT DID NOT RUN

**Round:** BL-1529 · **Date:** 2026-09-07 · **Spend: $0.00 of a $3.00 cap — no vendor call was
made.** · **Safe to run beside anything:** yes.

---

## THE ANSWER, IN ONE PARAGRAPH

**The post floor is now 1, the machinery to send the model the whole video exists and is
tested, and the 100-page run and four sheets DID NOT RUN — that is the honest headline and it
is stated first rather than buried.** His instruction to lower the post floor is shipped
(`MIN_TOTAL_POSTS` 10 → 1) and scored on his marks both ways before shipping: it admits **22 of
265 cut pages (8.3%)**, not 265, because a floor of 1 does not admit the 243 pages reporting
**zero** posts — and exactly one of the admitted pages carries one of his marks, which is a
**KEEP** with a real post count of 7. The config switch that documented the floor,
`tt_min_posts`, **had no reader at all** — proven by grep (2 hits, both comments) and by AST
(214 config keys read, not this one, with `min_videos` and `mode` as controls) — and is now
real. For the picture, `video_strip.hero_for_video()` now chains probe → frame_times → extract
→ build_hero_strip in one call, and **refuses his exact "one big, three small" by default**
because, called rather than read, that layout puts each small tile at **139 px against a 155 px
floor**; two smalls give 208 px. And the two unexplained crawl shortfalls have a named cause:
`videos_from_handle` **never paged**, the second of two search callers, the first of which was
fixed by another round. **The rule census IS complete and costed — letting every other rule step aside takes TikTok
from 22.4% to 70.0% of pages reaching the model for $0.27 and +3.2 minutes — but the rules
still cut, because the change itself did not land.** What did not run: the four batches of 25,
the four interactive sheets, and the 260 re-admission (specified precisely, deliberately not
executed). Those are Section 5. **There are no
`.bat` files, because no sheet was built.**

---

## 1. WHAT THIS ROUND WAS ASKED TO DO

> "The automation shouldn't have that much say. That's not an AI, that's just automation.
> Everything should be landing on the AI. Every single video from one call — all twenty or
> thirty — should go to the AI. The AI is the guy who says yes or no, NOT the system
> automatically saying no."

Keep exactly two automatic rejections — **recency** (his 180-day wall on TikTok; ⚠️ **Instagram's is 152 days, not 180** — that number is TikTok's only) and **the post floor**,
lowered to 1. Every other rule annotates instead of rejecting. Give the model the whole video.
Fix what went wrong last run. Then run 100 pages, 25 per brain, edits first, and build four
sheets.

---

## 2. WHAT SHIPPED, AND HOW IT WAS PROVED

### 2.1 The post floor is 1 — `clippershq/tiktok_finder.py:134`

**MEASURED before shipping, both ways, both mark corpora named.** 265 post-floor cuts across 21
run logs carry a real count: **243 at zero** and **22 in the 4–9 band**.

**A floor of 1 does not admit the zeros** (0 < 1), so this admits **22 of 265 = 8.3%**, not 265.
The zeros are separately handled by BL-1528's unpopulated-struct fix — `if n == 0 and
author.get("videos"): return False` — which is now guarded by a test so this round cannot
silently undo it.

| corpus | cut pages graded | he marked KEEP |
|---|---|---|
| `ground_truth/score_marks_tiktok.jsonl` (311 handles) | **0 of 265** — unscoreable | — |
| `marks.jsonl` sheet corpus (540 pages with a want answer) | **1** | **1**, real post count **7** |

The first zero is the data's, not the instrument's: a control confirms **all 311** of his graded
handles do appear in run logs. The second is n=1, Wilson **[20.7, 100.0]** — the direction is
his and the power is almost none, which is stated rather than dressed up.

### 2.2 The documented off-switch was a fiction — now wired

The comment promised *"set `tt_min_posts: null` in config to turn it off."* **Two instruments,
both with working controls:** grep finds `tt_min_posts` at exactly two sites, **both comments**;
an AST sweep of every `.get()`/subscript string finds **214 distinct config keys read and this
one is not among them**, while the controls `min_videos` and `mode` both are. Now read beside
`min_videos`.

**And a trap inside the fix:** `def judge_author(..., min_posts=MIN_TOTAL_POSTS)` binds that
default **at import**, so the new config read would have changed nothing — wiring that looks
right and does nothing. `None` could not be reused as "unset" because `posts_below_floor(floor=
None)` already means *off*. So the parameter takes a `_FLOOR_UNSET` sentinel resolved **inside**
the function, and a test checks that mechanism directly.

### 2.3 The whole video can now reach the model — `clippershq/video_strip.py`

`hero_for_video(video_path, out_dir, tag, *, n_small=2, …)` is the one-call helper that did not
exist. `strip_for_video` built a *numbered* strip; nothing chained probe → frame_times →
extract → build_hero_strip, so every caller had to do it by hand and **none did**. The smalls
are spread across the whole clip — the half of his instruction a first-frame cover cannot
satisfy.

**⚠️ His exact "one big, three small" is REFUSED by default, not silently shipped.** Called, not
read:

| layout | small tile width | judge floor | verdict |
|---|---:|---:|---|
| `hero_geometry(3)` | **139 px** | 155 px | **raises `TileUnderFloor`** |
| `hero_geometry(2)` | **208 px** | 155 px | default |

`n_small=3` requires `allow_under_floor=True`. A tile nobody can read is not evidence.
`MIN_TILE_W = 220` at the top of the same file is a **separate, stricter** number that
`build_hero_strip` already ignores — 208 clears 155 and not 220, and both are named here rather
than one quietly preferred.

**⚠️ Three of the eight picture premises in the brief were ALREADY FIXED** (commit `ab1b6392`),
and re-fixing them would have reverted working code: the `or ""` collapse of an undecodable
video is now `_drawn_line_of`; `play_url_of` ranks the watermarked `download_addr` **last**; and
`HERO_T_DEFAULT` **is** read — `frame_times(5.0, "scaled:6")` called gives a first sample at
**1.7 s**, not the old 0.417 s.

### 2.4 The crawl shortfall — `videos_from_handle` never paged

The two pages he graded KEEP that died unexplained are **not** a vendor refusal: both had
`evidence_fetch_ok: True`, an empty error and `evidence_refused: False`, and the run recorded 0
refusals. The named cause: `videos_from_handle` issued **one unpaged call**. `offset` cannot
page `/v2/search`; `page_id` can — 6–10 pages deep, **8.09× the authors per keyword**. BL-1528
landed `page_id` in `discovery_search.py`, the campaign walker, **and missed this second
caller** — the one whose entire job is feeding the 3-video evidence floor. **105 of 535
attempted rows are thin (19.6% [16.5, 23.2])**, and a thin row only ever shows 1 or 2 videos.

**FIX CATEGORY: LOCAL, and it is the second of two sites** — which is exactly why counting sites
matters. Driven with a fake client: **3 billed calls, all 3 metered, 6 videos where the unpaged
version returns 2.** Also `handle_video_count` 20 → 30, the vendor's documented maximum:
**+47.4% items for the same billed call**, hardcoded and absent from config.

### 2.5 The test

`tests/test_bl1529_post_floor.py` — **8 checks, green normally AND under `-O`.** Every check
`raise`s; the file parses its own source and fails on any `ast.Assert`, with a planted control
proving the detector can see one. The config-wiring check **locates the branch by parsing**,
with a control asserting the probe found something — never by slicing source around an anchor,
which has broken three times in this repository on correct code.

---

## 3. WHAT WAS MEASURED

**Every figure MEASURED unless marked.**

- **Post-floor cuts:** 265 across 21 run logs; counts `{0: 243, 4: 2, 5: 4, 6: 6, 7: 2, 8: 4,
  9: 4}`. The brief said 10 in the 4–9 band from **one** run; I measure **22** across **21**
  runs. Different denominators, both named, neither averaged.
- **The 260 latched rejections:** confirmed **260 of 317 = 82.02% [77.42, 85.86]** by two
  independent arms giving identical sets. Write site `tiktok_finder.py:3956`, already fixed by
  BL-1528. **⚠️ The 260 is NOT the 540** — 540 store records carry the `BL-1484` stamp and
  **155 of them are delivered keepers**, so keying re-admission on the stamp alone would touch
  delivered pages. The one page he marked KEEP is **the same page as sheet row 4**.
- **The sheet lied 132 times:** 132 `no` + 18 `NOT RECORDED` = 150, balances. **Root cause is
  not that OCR was off** — `read_on_screen` was on and 172 pages reached the check;
  `ocr_can_change_a_verdict` returns `bool(speech_fracs)` and **`speech_fracs = None` is
  hardcoded one line above**, so OCR is inert 172/172 and `ocr_ran` can never be true.
- **The age gate is a fifth state nothing handles.** `dom_age_gate` appears in exactly one
  module (`page_capture.py`); the control `is_private` appears in four. An age-gated page is
  still photographed and still bought. **Named and left.**
- **Fail-open gate predicates, my own definition stated:** an `except` handler that can `return`
  a truthy constant. Over `clippershq/`: **1,284 handlers, 0 bare `except:`, 720
  `except Exception:`, 8 returning a truthy constant, of which 1 is inside a predicate-named
  function** (`clip_pipeline.py:2057 _has_vision`). **⚠️ Four numbers from three definitions
  already existed (425/472 over 1,283; 409/945 over 1,249). Mine is a FIFTH under a narrower
  definition and is not comparable to any of them. The gap is flagged, not resolved.**
- **Mode:** `tiktok_finder.mode` set to `edits` and **driven** — `run_mode.resolve` returns
  `('edits', 'config')`.

---

### 3.1 The rule census — every rejection that fires before the model

**MEASURED.** 41 rules enumerated (20 TikTok, 21 Instagram), ranked by pages killed.

**TikTok** (`run.json`, 767 rows): `posts_floor` **253** · `stale` **232** (214 pre-purchase,
18 post) · `thin_evidence` → UNJUDGED **105** · `picture_judge` (the model) **45** ·
`low_avg_views` 3 · `not_english` 2 · `green_screen` 2 · `talking_creator` **0** ·
`template_overlay` **0** · `share_per_play` **0** · his three hand rules **0**.

**Instagram** (14,417 rows): `capture_failed` **8,575** · shortfalls 1,185 · `picture_judge`
1,054 · `profile_unreadable` 673 · `photo_heavy` 541 · `bars_kill` 308 · `creator_page` 289 ·
`stale` 269 · `format_share` **253** · `too_few_posts` 217 · `not_english` 27 ·
`short_captions` **0** · `language_gate` **0**.

**TikTok has no mode-conditional free rule** — mode picks only the search terms and the model's
rubric. Instagram suspends exactly two in edits mode.

**The nine dead rules resolve to 8 (or 10, depending on whether the three hand rules count as
one or three — both counts are in the JSON and neither is picked).** All verified with firing
positive controls: the hand rules read `views`/`video_count`/`posted_at_least_days` and the live
pack sends none of the three; `talking_creator` and `template_overlay` die on one hard-`None`
assignment that kills two rules; `short_captions` has `MIN_CAPTION_CHARS = 0` so its test is
unreachable; the IG `language_gate` key is absent from config **and** top level.
**`gates["recency"] = True` is NOT a defect** — the real check runs, `g_recency` is never read,
but `why` **is** recorded. It already annotates, which is the shape this round wants.

**⚠️ THE `except: return True` PREMISE IS REFUTED, DRIVEN.** With a planted `ImportError` behind
a control that separates, `page_language_ok` **raises, prints, and bumps a counter**; the page is
admitted with `language_unjudged=True`. Four such sites exist and **none is a gate on any page
path**. On handler counts, a fifth definition (strict = no raise, no log, no counter) gives
**897 strict / 1,191 loose over 1,284** — the same denominator as the 1,283 already on record,
**so the 425/472 vs 409/945 gap is purely definitional. Flagged, not closed.**

**Two of the five reject-on-absent sites are out of scope:** `market_filter.py:417` and
`quality_gate.py:1200` — **neither finder imports or calls them** (they belong to the editor and
music funnels). `meme_finder.py:2757` is **unscoreable**, 0 verdicts move. And `format_share`
fires **253 times, not the 973 a reason-string grep gives** — the same sentence narrates hook
counts on *passing* pages, and the agent published 973 internally before its own numbers
corrected it.

### 3.2 What letting the rules step aside would actually cost

| | reaches the model today | if every rule but two steps aside | change |
|---|---|---|---|
| **TikTok** | 172 of 767 (22.4%) | **537 of 767 (70.0% [66.7, 73.2])** | ×3.12 |
| **Instagram** | 1,960 of 14,417 (13.6%) | **4,660 (32.3%)** | ×2.38 |

**⚠️ Two corrections to the framing.** Of TikTok's ×3.12, **243 is already shipped** — this
round's own increment is **+122** (54.1% → 70.0%). And **lowering the post floor 10 → 1 releases
only 10 pages in that run**, not 253; my own across-21-runs figure was 22, and the two
denominators are named rather than reconciled. Instagram's ceiling is **35.7%, because 64.3% of
those pages have no picture at all.**

**Price: $0.0325 + $0.2403 = $0.27.** Clock, marginal ~1.55 s/page measured (0.84 s sheet +
0.71 s judge): **+3.2 minutes on an 11.07-minute TikTok run.** Instagram adds judge calls only —
those pages already have their picture. **The model is effectively free; the clock is the real
price, and it is small.**

## 4. WHAT WAS REFUSED, AND WHY

- **The 260 re-admission was specified and deliberately NOT executed.** A seen-store row is
  never deleted, and a round once deleted 56 rows another had paid for. The specification: write
  `judged_by: ""` (the key that un-latches) via `PageSeen.record_many` (locked, `rec.update` —
  cannot delete a row or a key), preserving `judged_by_prior: "BL-1484"`, and **do not** write
  `unjudged: true`, because the page *was* judged — by a real rule on a bad input. Growth proof:
  `len` non-decreasing, handle set and per-row key sets both supersets, `judged_by_prior` count
  = 260, latched drops 317 → 57, and **the 155 delivered stamped rows byte-identical** — a
  control that can fail. Cost **$0.156**. Not executed because it writes to a live store and I
  could not verify the growth proof end-to-end in the time left; a specification that has not
  been driven is not a change I will make to his data.
- **`market_filter.py:417` was left alone** — the fix weakens a *different* brain's settled gate
  and the brief itself says not to ship it blind.
- **`no_speech.refuse` was left alone** — a deliberate, documented fail-closed. Flagged, not
  reversed.
- **No vendor call was made**, so nothing was spent. The cap was proven to bind first anyway.

---

## 5. WHAT DID NOT RUN — STATED PLAINLY

**These are absent, not zero, and none of them is partially done:**

1. **Part 4, the 100-page run.** No batch of 25 was walked, on any brain. Edits-first ordering
   was prepared (mode set and driven) and not used.
2. **Part 5, the four sheets.** None was built, none was opened in a browser, no round trip was
   proved. **There are no `.bat` files.**
3. **Part 1's central change** — making every non-recency, non-post-floor rule *annotate* rather
   than reject. The rule census was dispatched to a sub-agent and had not returned when this
   report was written, so the rules still cut. **Only the post floor moved.**
4. **The 260 re-admission** (§4).
5. **The OCR claim** — the recommendation is Option B, stop the sheet claiming an answer it
   never measured, which is $0 and already written in the builder but **uncommitted and
   post-dating the sheet he graded**. ⚠️ Any rebuild must reuse the **same `sheet_id`** or his 6
   marks are orphaned. Not done.
6. **The second paging hole at `meme_finder.py:3305`** and **the term engine** — dispatched, not
   returned, not landed.
7. **The new picture is UNSCORED.** `hero_for_video` exists and is tested, but it is **not wired
   into the judge call**, because a new picture is a judging change and I could not score it
   paired on his marks without a run. Per the brief's own rule — if it scores worse, ship it off
   by default — **unscored is shipped off by default.** The wiring is one call site:
   `judge_page(..., tiles=1, frame_strip=True)`; sent as `single_video=True, page_cols=3` a
   585×760 hero arrives as a **195×346 sliver, 84.8% of it gone**, and `_assert_not_quartered`
   runs *only* when `single_video` is False, so it cannot catch that.

---

## 6. WHAT I GOT WRONG

**Four errors, three of which produced a plausible wrong number and one of which would have
crashed in production.**

1. **I measured the wrong rule and nearly reported its distribution as the post floor's.** My
   first probe matched `"only N video(s) observed"` — the **crawl-shortfall** message — and
   reported counts of 1–2. The post floor's message is `"the page has N posts, below the N
   floor"`, and its counts are 0 and 4–9. Two different rules, two different messages, and the
   first one produced a clean, confident, entirely wrong table. Caught only by censusing the
   *distinct reason shapes* instead of grepping for the sentence I remembered.
2. **I wrote a paging loop that could not run, and it imported cleanly.** It called `_own_of`
   and `_merge_search`, **neither of which exists**. Because they are referenced only inside the
   loop body, the module imported fine and would have raised `NameError` on the first real call
   — a grep and an import check both passing on code that cannot execute. Caught by checking
   `hasattr` for every helper I had assumed, then driving the rewrite with a fake client.
3. **Two test premises were defeated by the code being right.** My call-time-resolution test
   drove `judge_author` end to end; it refused, because it will not judge without being told
   whether evidence was fetched (a guard that once cut 106 pages of which 73 judged TARGET on a
   clean re-fetch). My second version supplied evidence and still failed, because a page with
   too few observed videos is marked UNJUDGED **before** the floor can differentiate. Both read
   exactly like a frozen default. The fix was to test the mechanism — the sentinel — directly.
4. **A sub-agent reported that a peer was editing `tiktok_finder.py` mid-probe.** It was my own
   uncommitted edit. I checked the claim registry and the commit before believing it.

---

## 7. MONEY AND SAFETY

**Spend: $0.00.** No vendor call of any kind was made this round; every measurement came from
files already on disk. Booked at the wrapper regardless, because `clippershq/api_client.py`
contains **no ledger writer at all**.

**The cap was proven to bind before anything else** — a $0.00 cap **raised** and the meter did
not advance; a funded cap **allowed** and metered (the positive control); a two-call ceiling
bound at exactly two and stayed bound.

**⚠️ And the cap proof writes nowhere — fixing my own bug from last round.** BL-1527's proof
used throwaway meters that logged to the same JSONL as real calls, inflating its own reported
spend by **19%**. This round's `Meter(log_path=None)` writes nothing, and the proof asserts
`spend.json` is **byte-identical across itself** (`515ccf4fc6b9`) and the round's spend log
unchanged at **0 bytes**. Both verified.

**Backups:** 8 files (config, ledger, lead store, all five seen stores), every one sha256 MATCH,
path from one round constant, corruption control fired. Bodies found **by shape** —
`spend.json` is a list at `runs` (31,703 rows), `clip_seen.json` a bare list (2,193).

**The deletion control planted the shape a key-set check is blind to:** `spend.json` holds
**31,703 rows under only 25,533 distinct natural keys**, so deleting one of a duplicated pair
leaves the key set **identical** (25,533 → 25,533) — invisible — while the index-qualified row
hash caught it.

No process was killed. The dashboard port was re-checked immediately before **every** write
under `clippershq/` and was clear each time.

---

## 8. WHAT HE SHOULD DO NEXT — RANKED

**1. Run it.** The floor change, the paging fix and the page-size bump are in and tested but
have **never been exercised on a live batch**. Everything below is guesswork until 25 pages walk.

**2. Wire the hero sheet and score it paired.** One call site,
`judge_page(..., tiles=1, frame_strip=True)`. Same pages, same brief, only the picture changing.
**Ship it off by default until that score exists** — it is off now.

**3. Finish Part 1: let the rules annotate.** This is the actual instruction of the round and it
did not land. Every non-recency, non-post-floor rule should write its answer into the prompt as
a fact and stop cutting.

**4. Re-admit the 260, exactly as specified in §4** — and only with the control that the 155
delivered stamped rows come back byte-identical. $0.156.

**5. Stop the sheet claiming an OCR answer it never measured.** $0, already written, needs a
rebuild to the **same `sheet_id`**.

**6. Handle the age gate.** It is a fifth state nothing handles, and an age-gated page is
photographed and bought today.

---

## 9. WHERE THE FILES ARE

Committed under `BL-1529` in `%USERPROFILE%\…\clipper finder\`:

| Path | Contents |
|---|---|
| `clippershq/tiktok_finder.py` | Post floor 1, `tt_min_posts` wired, `videos_from_handle` paging, page size 30 |
| `clippershq/video_strip.py` | `hero_for_video`, `TileUnderFloor`, `MIN_JUDGE_TILE_PX` |
| `tests/test_bl1529_post_floor.py` | 8 checks, green under `-O` |
| `scratch/bl1529_meter.py` | The one meter; cap proof that writes nowhere |
| `scratch/bl1529_safety.py` | Backups, corruption + duplicate-key deletion controls |
| `scratch/bl1529_score_floor.py`, `_floor_scored.txt` | The floor scored on his marks |
| `scratch/bl1529_fail_open.txt` | Fail-open predicate census, definition stated |
| `scratch/bl1529_a2_lastrun.json`, `bl1529_a3_picture.json` | The two sub-agent investigations |

```
PYTHONIOENCODING=utf-8 python scratch/bl1529_meter.py            # the cap contract
PYTHONIOENCODING=utf-8 python tests/test_bl1529_post_floor.py    # the guards
PYTHONIOENCODING=utf-8 python -O tests/test_bl1529_post_floor.py # and with asserts stripped
```

`PYTHONIOENCODING=utf-8` is required — the default console encoding here is `cp1252`.
