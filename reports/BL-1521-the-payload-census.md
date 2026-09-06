# BL-1521 — The payload census: what one paid call actually gives us

**Round:** BL-1521 · **Filed:** 2026-09-06 · **Cap:** $0.75 · **Spent: $0.0406** ·
**READ-ONLY — no production file was written, nothing shipped, no threshold moved**

---

## 1. Safe to run, and the headline answer

**Safe to run.** This round wrote no production file, added no rule, moved no threshold and
changed no verdict. Every defect below is named with `file:line` and left in place.

**He asked: "With one call, what does the API return? I'm pretty sure we're getting more, but
we're not even using it." The answer is yes, and the size of it is this:**

**Of 6,962 item-level fields the vendors return across 15 endpoints, 6,703 are read by no
production code, and 1,678 of those both VARY and are unread** — a field that never varies
cannot decide anything, so that 1,678 is the honest haystack, not the 6,703.

**On TikTok, exactly ONE field is genuinely paid-only: `createTime`, the account's age.**
Everything else the paid profile call buys — bio, verified, private, display name and all seven
stat counters — already arrives free in the author block of the hashtag call we have already
made. Paid bio versus free bio: **35 of 35 byte-identical.**

**On Instagram the bio is free too**, though not from the paid payload: a plain
`GET instagram.com/<handle>/` with a non-Chrome user-agent returned **200 on 65 of 65, none
walled**, and its `<meta name="description">` carries followers, following, posts, full name and
the biography. **What is genuinely left, paid-only, is four things: the exact follower count,
`category`, `external_url`, and the contact email** — and the email is the one that cannot be
dropped: 33 of 64 accounts had one, the free bio had one on 34 of 64, **but the overlap is only
11, so 22 accounts have a paid email that appears nowhere in their bio.**

**And the reason the Instagram free path can't already do this is one defect:**
`clippershq/ig_discovery.py:276-283` reads `biography`, `follower_count`, `following_count`,
`media_count` and `external_url` out of an object **that has 28 keys and none of those five**.
Driven over 781 stored media: bio `""` on **781/781**, followers `None` on **781/781**. The free
path structurally cannot see them, so every one of those facts forces the paid call.

---

## 2. What I was asked to do

Produce the complete field list for every endpoint both platforms call, with fill rate, whether
each field varies, whether any production code reads it, and what a rule could decide from it;
answer what is left that only the paid profile call provides; find the field killing 64% of
Instagram profile purchases; count the causes of pages that never get a picture; do the same
census for TikTok including why one brain delivers nothing; and rank everything we pay for that
we already have, by dollars and hours saved per 1,000 delivered.

---

## 3. What shipped

**Nothing.** By instruction. Four defects are named below and left in place.

---

## 4. What was measured

### 4a. The full sheet

**MEASURED.** 15 endpoints, both platforms. Four had no sample on disk and were probed fresh.

| | count |
|---|---:|
| item-level field paths | **6,962** |
| …that VARY | 2,705 |
| …unread by production code | 6,703 |
| **…varying AND unread** | **1,678** |
| …varying, ≥80% fill, and unread | **913** |

AST census over 164 files, 0 unparsed, 2,910 distinct keys found read, 6 positive controls fire,
negative control 0. ⚠️ **The honest limit: 1,738 accesses are dynamic and cannot be resolved
statically**, so "unread" means "no static reader found", not "provably never read".

**Fields a rule could use tomorrow, all free, all unread:** `original_lang_for_translations` (IG,
70–83% fill — the post's language); the `clips_metadata.original_sound_info.*` block (67–75% —
original versus licensed audio, title, explicit flag); `like_and_view_counts_disabled` (100% —
explains a zero engagement reading); and on TikTok `music.is_original_sound`,
`music.has_human_voice`, `music.user_count`, and
`video.cla_info.original_language_info.is_burnin_caption` — **burned-in captions, free and
unread, which is the signal the OCR gate currently pays to derive.**

### 4b. What only the paid profile call still gives us

**TikTok — ONE field.** `createTime`. MEASURED on a fresh pull: bio key present **90/90 = 100%**,
non-empty **77/90 = 85.6% [76.8, 91.4]**; paid vs free bio **35/35 byte-identical** (28/28 when
restricted to non-empty). ⚠️ **Seven of those 35 are `empty_str` vs `empty_str` — real agreement
that a truthiness test would score as a miss.** Everything else the paid TikTok profile adds is
a settings flag nothing reads, or is empty on every sample.

**Instagram — four things.** Of the 265 keys the paid profile returns, **241 are paid-only, and
roughly 155 of those are constant or empty across all 65 accounts.**

| paid-only field | free availability | verdict |
|---|---|---|
| exact follower count | free page rounds to "159K" — exact match **0/64** | genuinely paid |
| `category` / `category_id` | value in free body **5/27** | genuinely paid — and `category_id` is **100% filled with an 18-value taxonomy and never read** |
| **`public_email`** | paid 33/64; free bio 34/64; **overlap only 11** | **cannot be dropped — 22 accounts have a paid email absent from the bio** |
| `external_url` / `bio_links` | 72.3% paid; **0/18** in free body | genuinely paid |

⚠️ The Instagram profile call returns **zero medias** — the envelope is exactly `{user, status}`
on **65 of 65**. Confirmed, not assumed.

⚠️ **AND A BRIEFED FACT IS REFUTED.** "The Instagram verified flag is free on 150 of 150 and
NEVER MAPPED" is **wrong**: it *is* mapped at `ig_discovery.py:280`, filled **781/781**, and read
at `filters_free.py:136`, `filters_free.py:217` and `free_judge.py:976`.

⚠️ **A second inherited claim corrected:** TikTok's `/v2/search` author object has 201 keys and
**no `signature` at all** — `search_user_desc` is the handle on 42/42, not the bio. So the free
bio exists on the hashtag lane and **not** on the search lane.

### 4c. The field killing 64% of Instagram profile purchases — the framing is wrong

**The field is `taken_at`** (`meme_finder.py:3562-3585`), and the rule that needs it is the
`STALE_MONTHS` recency cut at **`meme_finder.py:2598`**.

⚠️ **BUT THE REASON STRING IS A MISLABEL, AND `taken_at` IS NOT WHAT KILLS THESE PAGES.**
`meme_finder.py:2852` branches on `unjudged`, and line **2847** (`if shortfall: unjudged = True`)
sets that True for **any crawl shortfall**, which the `undated` flag never touches.

MEASURED on `output/rejections/meme_pages.jsonl`, **n = 4,215** rows, all past the purchase:

| | n / 583 | Wilson |
|---|---:|---|
| carry the reason string | 583 | — |
| **entered via `shortfall`, not `undated`** | **583** | **100% [99.3, 100.0]** |
| entered via `undated` | **0** | [0.0, 0.7] |
| actually carry a `last_post_days` (a date existed) | 321 | 55.1% [51.0, 59.1] |
| have a non-empty `fired` — refuting the branch's own comment at `:2853` | 480 | 82.3% [79.0, 85.2] |
| had the date-based `stale` rule FIRE on a page the sentence calls dateless | 75 | 12.9% [10.4, 15.8] |

Driven, with a positive control: a genuinely dateless plant prints the string with
`undated=True`; **two plants whose every post carries a real `taken_at` print the same string.**

**Is it recoverable free? The timestamp yes, the 64% no.** `ig_embed.py:136` yields
`last_post_ts`; driven live at $0.00 it recovered a date on **11 of 14** sampled handles =
**78.6% [52.4, 92.4]** — but it flips **0 of 583**, because none of them was unjudged by the
date. **DERIVED cost of the mislabel: those 583 rows are UNJUDGED and get re-walked at ~3 billed
IG calls each = $1.21 per re-walk cycle. Fixing the timestamp recovers $0.00 of it.** The money
is in the shortfall class.

### 4d. The pages that never get a picture

Detector controls passed first: the shipped `META_JS`/`SETTLED_EXPR` driven under a real browser
on 5 planted DOMs plus 2 negative controls, all correct.

**MEASURED, corpus A — 11 capture manifests, n = 3,277 labelled records. No picture: 584 = 17.8%
[16.5, 19.2]** — **not the briefed 40.1%.**

| cause | n / 584 | Wilson |
|---|---:|---|
| **private** (permanent) | 386 | 66.1% [62.2, 69.8] |
| **unknown** (its own category) | 145 | 24.8% [21.5, 28.5] |
| **login wall** (retryable, unjudged) | 53 | 9.1% [7.0, 11.7] |
| not found | 0 | control passed — a real zero |
| **age gate** | **NOT MEASURABLE** | the flag is ABSENT on 3,242 of 3,359 records |

⚠️ **Two other corpora disagree and both are named rather than averaged:** corpus B (n=1,624)
gives 17.2% [15.4, 19.1]; corpus C, an export of 14,417 rows, says "no cover image captured" on
**59.5%** — but **12,793 of those rows have no camera record at all**, so it is a different
measurement.

⚠️ **DEFECT — the wall count is inflated 6x by a labelling bug.** `page_capture.py:619-638` gates
only the `unknown` branch on `_no_grid`; private, not-found and **login_wall** are not.
**MEASURED: 257 of 310 login_wall-labelled records HAVE tiles > 0.** The comment at
`page_capture.py:704-705` — "`no_grid_reason` is only set when `tiles == 0`" — is false. **The
briefed "310 walled" is really 53.**

⚠️ **The age gate is a fifth state with a name and no handler.** No module outside
`page_capture.py` reads `age_gate`; it is absent from the suppression tuple (`:729`) and from
`_paid_grid_needed`'s refusal list (`:862-864`), **so an age-gated page is still photographed and
still bought.**

**Clock. MEASURED:** no-picture pages median **15.67 s**, total **9,131 s**. **DERIVED: 0.77 h per
1,000 walked**, and at the export's delivery rate (530 of 14,417 = 3.68% [3.38, 4.00]) that is
**~20.9 h per 1,000 delivered.**

**And the payload-built sheet — DRIVEN, not read.** `clippershq/payload_sheet.py` is **NOT
committed** (`git ls-files` empty, `git log --all` empty), has **zero importers and zero tests** —
but it **RUNS**: driven offline with an injected opener at **0 billed calls** it produced
`tiles=6`, 1720×2024 on disk, `trimmed=false`, and through the shipped `free_judge.grid_b64` it
delivers **645×760 with ~215×380 tiles — 1.63× the browser's tile area.** It is the only way to
look at the 386 private and 53 walled pages, and it is wired to nothing.

### 4e. TikTok

**MEASURED, live** (24 billed calls, cross-checked against the vendor's own balance counter:
427353 → 427339 = 14 over probe 1, exactly its 19 calls minus 5 refusals).

| endpoint | videos/call | **distinct authors/call** | bio present |
|---|---|---|---|
| `/v1/hashtag/medias` @30 | 29–30 | **24, 25, 27** | **27/29 = 93.1% [78.0, 98.1]** |
| `/v2/search` @30 | 28–30 | **24–29** | **absent on 88/88** |
| `/v1/user/by/username` | 0 | 1 | — |
| `/v1/hashtag/info` | 0 | 0 | pure tax: one billed call to turn a word into an id |

**Page-size ceiling is 30 on both, and it is enforced differently.** `/v1/hashtag/medias`:
40/50/100 → HTTP 400, refused and **not billed**; `amount=100`/`max_amount=100` → **200 OK with
29 items, silently ignored.** `/v2/search`: 40/50 → HTTP 422 naming the limit. Paired 20→30 gave
**+51.3% items and +57.6% distinct authors for the same billed call** — already banked in
`tiktok_finder.py:589` and `:453`.

⚠️ **`aweme_type` and `duration` confirmed unused** by AST over 4,861 files with positive controls
(sibling keys of the same dict literal are found read at 4 and 5 sites). **Correction to the
brief:** `aweme_type` is 100% filled on `/v2/search` but **absent on 59/59 of
`/v1/hashtag/medias`** — and the hashtag feed is where every TikTok page on disk came from.
**DEFECT `tiktok_finder.py:374`: the two lanes write different UNITS into the same `duration`
key** — hashtag returns seconds (5–43), search returns milliseconds (21931–329967). A rule tuned
on one lane would be off by 1000× on the other. It has never bitten because nothing reads it.

⚠️ **THE "TIKTOK EDITS HAS DELIVERED ZERO PAGES" PREMISE IS FALSE.** `output/bl1427_edits_tiktok`
holds **28 delivered pages, 31 marks, and he wanted 30 of 31 = 96.8% [83.8, 99.4]** — the highest
of the four brains. Its price is **$0.00162 per delivered page** over 4 runs and 157 billed
calls. **A table reading zero had the wrong denominator, not an empty one.** What it has never
done is deliver a *lead*: 4 addresses once, 0 since. Five causes, with `file:line`:

1. **The mode is never selected** — `config.json` sets `mode: memes`, `run_mode.py:60` defaults
   to memes; all four edits runs happened in one 32-hour window nine days ago.
2. **The hashtag lane is structurally empty** — `tiktok_finder.py:3660`, `editing_hashtags = []`,
   `tags_walked = 0` on 4/4 runs.
3. **His seven configured edit terms are read and discarded** — `:3641` assigns them, `:3661`
   passes the *meme* list instead, and `run_mode.py:137` **prints a note that is false**: "no
   configured TikTok search term is an edit term". `velocityedit`, `fanedit`, `amvedit`,
   `cinematicedit`, `fan edit` **have never been searched.**
4. **Supply exhausts in three runs** — `handle_searched` 34 → 22 → 16 → 3 against a page-1-only
   walk.
5. **The email gate** — 58 `is_target` → 4 emails = 6.9% [2.7, 16.4]; on runs 2–4, **0 of 31
   [0.0, 11.0]**. And because edits mode is 100% search lane, **the free bio is absent on 100% of
   its authors**, so the route that cancels the paid profile call can never fire there.

⚠️ **And 31 photographed pages were never put in front of him** — three sheet directories hold 38
PNGs and a `run.json` with **no `index.html` and no `marks.jsonl`. Exactly one TikTok edits sheet
has ever been built.**

**Two paging defects, named and left:** `discovery_search.py:263` never pages (zero `page_id`
literals in the file; BL-1469 fixed only `tiktok_finder.py:640`), so that walker returns page 1
forever; and `main.py:3875` clamps `count=min(50, …)` against a ceiling the vendor enforces with
a 422, saved only because `api_client.py:411` re-clamps to 30.

### 4f. The account id — my own two-instrument check

**MEASURED.** `master_leads.csv`, 17,014 Instagram rows: `user_pk` carries a pk-shaped value on
**221 = 1.30%** — confirming the briefed figure exactly. But a second column, `secuid`, carries
one on **772 = 4.54%**, the two are **completely disjoint** (0 rows have both), and both are
dominated by 11-digit values. Union: **993 = 5.84%.**

⚠️ **NOT VERIFIED, and I am not going to label it.** `secuid` is fed from TikTok's `secUid`
(`crawl_suggested.py:806`) and read at 18 sites as a dedup key. Whether those 772 values *are*
Instagram account ids is **unestablished**: I joined 62 of 67 handles whose pk I know
independently from saved payloads, and **not one of those rows carried a pk-shaped `secuid`** —
the two populations do not overlap. The join's positive control passed (62 handles matched), so
the inconclusive result is real and not a broken reader.

⚠️ **And the Instagram seen store carries an id on 0 of 6,196 records.** The persistence added
yesterday protects the value going forward; **it has nothing to protect yet.**

### 4g. What we pay for that we already have — the reserved question

⚠️ **This section was drafted from checkpoints and then REWRITTEN.** The reserved agent's
final report arrived after I had written the round up, and it materially changes the section:
what the checkpoints called "the sharpest thing" is now a priced item, and the largest finding in
it — that yesterday's deferral has never executed — was not in the checkpoints at all.
**Publishing the partial would have understated it.**

**$0.00 spent** — no network probe. From the funnel's own journal (89 run files, 51,429 rows,
87 run ids) and the shipped code **driven**, not re-implemented.

**The Instagram page-walk baseline, which did not previously exist.** 2,029 page-walks carry
stage times; 354 delivered.

| stage | times run | calls / 1,000 delivered | clock h / 1,000 delivered |
|---|---:|---:|---:|
| profile | 2,029 | 5,732 | 3.19 |
| posts | 1,763 | 4,980 | 3.62 |
| speech | 1,848 | 0 (free) | 3.26 |
| **page total** | 2,029 | — | **14.62** |

**DERIVED: $7.40 per 1,000 delivered from profile + posts alone**, at HikerAPI's
$0.00069064 — not LamaTok's rate, which is the error this project has made at seven sites.

**THE LARGEST CLOCK ITEM: speech runs ABOVE nine rules that never read it.** `attach_speech`
fires at `meme_finder.py:7728`, `judge_page` at `:7857`. Speech writes one field, `speech_frac`,
read at `:2489-2490` **and nowhere else.** Over 1,848 pages costing 4,159 s:

| | n | share | clock |
|---|---:|---:|---:|
| delivered — speech mattered | 354 | 19.2% | 783 s |
| **rejected by ≥1 rule that does NOT read speech** | **1,367** | **74.0%** | **2,698 s = 64.9% of all speech clock** |
| rejected by `dialogue` alone | 61 | 3.3% | 567 s |
| unjudged | 66 | 3.6% | 112 s |

**DERIVED: 2.12 hours per 1,000 delivered** spent downloading video, running ffmpeg and detecting
voice for pages the verdict had already gone against. **$0 of vendor money — the saving is pure
clock.** Instagram only; `tiktok_finder` never calls `attach_speech`. **Named cost of moving it:**
rejected rows would show `dialogue_state = "unmeasured"` on the sheet (`review_sheet.py:290`).

⚠️ **AND THE DEFERRAL SHIPPED YESTERDAY HAS NEVER RUN.** Driving the shipped
`profile_deferrable` over the 2,029 pages that provably bought a profile: **DEFER on 828 = 40.8%,
worth $1.62 and 1.31 h per 1,000 delivered.** It was committed at **13:30:53**; the newest journal
begins **12:32:05**. Its measured reach is real and its production effect to date is **zero** —
which is the same shape as a helper shipped with no call site, one layer up.

The largest residual refusal is the `unjudged` arm — **610 of 2,029 = 30.1%** — and
`meme_finder.py:2843` says an unjudged page "comes back on the next run". Measured: **404
consecutive profile purchases across 136 handles where the earlier walk ended unjudged.** That is
the re-buy the mislabel in §4c feeds.

⚠️ **`free_facts["emails"]` is extracted free at capture and has NO READER.**
`page_capture.py:338` pulls emails from the bio with no billed call; the packer `_free_facts_for`
(`meme_finder.py:5350`) lifts seven other keys and **drops that one** — while `resolve_contact`
(`meme_finder.py:3057`) is documented as "ONE BILLED REQUEST (the profile)" for the same thing.
**Fill is 7.7%** on the 117 records where the free read returned content, so this is small — and
the denominator is stated because only **427 of 3,329** capture records carry a `free_facts` dict
at all.

**MEASURED REFUSALS — do not spend a round on these:**

* **Repeat paid walks are 11.0%, not 68.3%.** The raw journal shows 31,107 of 45,542 handle/run
  pairs repeating, but that is not spend; restricted to rows with post-derived measurements, three
  independent markers agree at **11.0% / 9.7% / 10.5%**. **Lifetime value $0.30–0.60.**
* **Free photo-mix versus paid `photo_heavy`: n = 13, agreement 69.2%** — too small to conclude.
* **The ledger cannot answer this question at all.** `spend.json`'s `runs` is 29,023 rows of
  `{ts, campaign, calls, tiktok_usd, ig_usd, dollars}` — no endpoint, no argument.
* **Neither Instagram client has any response cache.** Every run starts cold, so no stored payload
  exists for a later run to re-read. "Re-use what we bought" has nowhere to read from today.

⚠️ **DEFECT FOUND ON THE WAY, NAMED AND LEFT — 102 rows never reached the lead store.**
`exports_meme_pages/_provenance.json` records `master_offered 102, master_appended 0,
master_merged 0` with a `PermissionError: [WinError 5]` on `master_leads.csv.tmp`.
`_append_to_master` (`meme_finder.py:8595-8657`) wraps the write in `except Exception`, returns
the failure as a counter and **does not retry**. On disk now: `master_leads.csv` 30,201,662 B at
23:49 versus `master_leads.csv.tmp` **30,201,847 B at 00:14** — **the newer content is stranded
in the temp file.** The export directory still holds those rows, so nothing is lost yet.

### 4h. An amendment received after its own agent had reported

⚠️ **`aweme_type` lines up exactly backwards from where this project has been looking for
it.** §4e records it absent on 59/59 hashtag items and 100% present on 88/88 search items. The
amendment supplies what makes that matter: TikTok edits mode walks `tags_walked = 0` on 4 of 4
runs, so **it is 100% search lane.** The field is therefore **free on 100% of edits-mode
discovery** and **structurally unavailable on the meme hashtag lane** that supplies every meme
page on disk. A prior round recorded that this "has never been measured and a no-network round
cannot close it"; a network round could, and this is the answer.

**The photo rate itself already exists and is not mine:** **70 of 1,099 = 6.37% [5.07, 7.97]**,
with `aweme_type == 150` coinciding with a photo payload on **978/978**, measured by an earlier
round — carried forward with that round's own caveat that it is a convenience sample clustered
by author. **§5 previously refused to price this as unmeasured; the refusal was right about my
sample and wrong about the repository.**

⚠️ **And a published per-brain price is flagged NOT VERIFIED rather than called wrong.** A
direct read of the four edits run files gives 157 billed calls / 58 `is_target` pages =
**2.71 calls/page, $1.62 per 1,000 delivered** — matching §4e. A published figure elsewhere says
1.77 calls/page and $1.19; those two are internally inconsistent with each other (1.77 calls at
$0.0006 is $1.06, not $1.19, while $1.19 ÷ 1.77 implies $0.000672 — close to the **Instagram**
rate, not LamaTok's). **I did not read that round's method or run set, so this is named as
unverified, not as an error.**

**Independently corroborated by a peer session, and reported as theirs, not mine:** a separate
round measured the same four runs at **58 delivered for $0.095090 in 119.4 s — $1.64 per 1,000
delivered and 0.57 h per 1,000** (my $1.62 by a different route), and found that **42 of those 58
were booked to `tiktok/memes`**, because the run record carries no mode field and the brain label
is a hand-typed literal. **If that holds, the only cost target this project has ever met was met
substantially by the brain a table declared dead.** Their measurement, cited with their caveats.

⚠️ **One correction to §4e cause 1, from the same peer, and it is good news.** The mode
resolution reads the **per-funnel** block, not a top-level key: `tiktok_finder.py:3634` builds
`blk` from `config["tiktok_finder"]`, and `resolve` returns `('edits', 'config')` when driven with
that block's `mode`. **So there is no resolution defect — `config.json` simply sets
`tiktok_finder.mode` to `"memes"`, which is a config value, not a bug, and setting it to `"edits"`
works today.** That makes item 7 below a one-line config change plus the search-term fix, not
repair work. ⚠️ **That peer had published the opposite and corrected it in print;** their
probe passed a top-level key and read the resulting default as proof the real key was dead. **It
is the same failure as my own guessed column names in §6: an instrument fed the wrong input
returns a clean, confident, wrong answer.**

### 4i. A fifth defect, found by the commit guard refusing me

⚠️ **Real addresses sit as string literals inside three production modules' self-test blocks.**
The pre-commit guard refused this round's commit because my agents' raw census re-exported
them — an AST census is *keyed by the string constant it found*, so every address hard-coded in
the source became a key in my artefact. **19 email-shaped literals across
`enrich_links.py:920-1026`, `writer.py:2552-2855` and `recover_ig_emails.py:505`**, of which
only 4 are role addresses (`info@`, `support@` and the like); the guard fingerprinted **38
occurrences as living in the gitignored lead stores.**

They are fixtures in `chk(...)`/`check(...)` self-tests — assertions like "this editor ships and
that one is excluded" written against real rows. **Those three files are already tracked, so this
is history, not something this round introduced**, and scrubbing it needs a rewrite rather than an
edit. **Named with `file:line` and left, per instruction.** ⚠️ **The guard did its job and my
own leak scan did not:** the scan covered the report and the manifest — what *I* wrote — and never
looked at what my agents wrote. Redacted copies are committed in their place, replacing the whole
value, because a truncation with an ellipsis still fingerprints the address.

---

## 5. What was refused

* **Any production change.** Read-only by instruction.
* **Calling `secuid` the account id.** The join was inconclusive; a label is not a measurement.
* **Pricing the TikTok photo-post rate from MY OWN sample**: its 88 items contain zero photo
  posts, so my sample says unmeasured, not zero. ⚠️ **The rate does exist elsewhere in the
  repository — 6.37% [5.07, 7.97] — and §4h carries it. I refused to price it and was right
  about my instrument and wrong about what was already known.**
* **Averaging the three no-picture corpora.** They measure different things; all three are named.

---

## 6. What I got wrong

* **My first join guessed column names that do not exist** (`handle`, `instagram_handle`,
  `username`) and matched **0 rows**. Its positive control caught it and refused to certify. The
  real columns are `tiktok_handle` and `instagram`. This is the same class as the probe that once
  reported 0 of 25 against a true 86.2%.
* **My first `secuid` reading was on its way to becoming a headline** — "4.5× more ids than
  anyone counted" — before I checked whether `secuid` is read at all. It is: 18 sites, as a
  TikTok dedup key. The finding survives only as an unexplained observation.
* **I inherited "40.1% get no picture" and "310 walled" from the brief and both are wrong** on
  the corpus I measured: 17.8% and 53. I would have repeated them had an agent not been told to
  count rather than inherit.
* **I wrote this report up from an agent's checkpoints and called §4g "partial" while the
  agent was still working.** Its finished result arrived minutes later and changed the
  section's headline: the deferral shipped yesterday **has never run**, which was not in the
  checkpoints at all, and the speech finding turned out to be the largest clock item in the
  round. **A partial result is not a small version of the finished one.**
* ⚠️ **My own leak scanner crashed on the ONE path where it found something.** Its clean
  runs printed fine; the moment a detector returned a hit it raised `UnicodeEncodeError` inside
  `print`, because the warning glyph attached to a HIT is not encodable in the console's cp1252
  — **so the scanner was reliable exactly while it had nothing to say.** That is the same
  defect I fixed in `clippershq/control.py` last round, reproduced by me in a fresh file the next
  day. The hit itself was a false positive (a 33-character filename matching the key-shape
  regex), which is the only reason the crash was not also a missed leak.
* ⚠️ **My leak scan passed and the commit guard then refused me** (§4i). The scan checked the
  report and the manifest and never touched the agents' raw JSON — it was scoped to what I
  wrote, not to what I was committing. **A clean scan of the wrong file set is a false
  absence**, and the only reason nothing escaped is that a guard I did not write was
  broader than the one I did.
* **I ran the previous round's five agents into a rate limit and lost them all.** This round used
  four, each instructed to checkpoint after every finding — and when the reserved agent did not
  finish, its numbers survived on disk. That instruction is the only reason §4g exists.

---

## 7. Money and safety

**Spend: $0.0406 of $0.75**, from each run's own counter at the wrapper, never a ledger delta:
39 LamaTok + 4 HikerAPI calls by the census agent ($0.02616), 24 billed LamaTok by the TikTok
agent ($0.0144), $0.00 by the capture agent (browser and free embed only).

⚠️ **$0.00276 of that HikerAPI spend never reached `spend.json`** — the client printed its own
warning — and **the 39 LamaTok calls are unrecorded because `api_client.py` contains no ledger
writer at all.** A ledger delta could not have seen this round's spend.

**The cap was proven to bind before the first call** by driving `harvest_run.Budget.reserve`, with
a positive control: a $1.00 cap ALLOWS (so the meter can say yes), an exhausted cap REFUSES, a
**$0.00 cap refuses the FIRST call**, a negative cap refuses, every refusal is a raised
`BudgetExceeded`, and **the meter does not advance on a refusal.**

**Backups** at round start, sha256-verified with a corruption control firing both ways, under a
path built from one round constant. **No seen-store row was removed or altered**, verified by row
key sets with the body found by shape — and note the shape matters: `spend.json`'s body is the
`runs` LIST (29,023 rows), and `clip_seen.json` is a bare list (2,193), both of which a
dict-only helper reads as near-zero.

Paths in this report are relative to the repository root under `%USERPROFILE%`.

---

## 8. What he should do next, ranked by what it costs him

Ranked by **dollars and hours per 1,000 delivered — not by how interesting it is.**

| # | change | worth per 1,000 delivered | basis |
|---|---|---|---|
| 1 | **Fix `ig_discovery.py:276-283`** — five fields read from an object that has none of them; bio `""` on **781/781** | **unlocks items 2 and 3**; this defect is what forces the IG paid profile call at all | MEASURED |
| 2 | **Move `attach_speech` below `judge_page`** — 74.0% of its clock runs on pages already rejected by rules that never read it | **2.12 h**, $0.00 | MEASURED, n=1,848 |
| 3 | **Let the shipped `profile_deferrable` actually run** — committed 13:30:53, newest journal 12:32:05 | **$1.62 and 1.31 h** | MEASURED, reach 828/2,029 = 40.8% |
| 4 | **Stop buying the TikTok profile** for anything but `createTime` | the whole TikTok profile line | 35/35 byte-identical bios |
| 5 | **Set `tiktok_finder.mode` to `edits` and give it its own search terms** (`:3661`) | unpriced, but **$1.62–$1.64 and 0.57 h** measured twice on its four runs — the only target ever met | MEASURED ×2 |
| 6 | **Fix the wall labelling at `page_capture.py:619-638`** — 257 of 310 "walled" pages have a picture | no dollars; **every wall statistic is inflated ∼6×** | MEASURED |
| 7 | **Fix the reason string at `meme_finder.py:2847-2860`** — 583/583 died of a crawl shortfall, not a missing date | $0.00 direct; it feeds the 404 re-buys in §4g and misdirects the next round, as it nearly did this one | MEASURED |
| 8 | **Retry the master append** (`meme_finder.py:8595-8657`) | 102 rows stranded in a `.tmp`, recoverable today | MEASURED |
| 9 | **Mine the 1,678 varying-and-unread fields** — burned-in captions, post language, original-vs-licensed audio | unpriced | MEASURED |
| 10 | **Wire or delete `payload_sheet.py`** — a 6-tile sheet for $0.00 at 1.63× the browser's tile area, committed to nothing | unpriced; the only way to see the 386 private pages | DRIVEN |

⚠️ **Deliberately NOT ranked, and both are mine.** The `secuid` observation (§4f) is
unverified, and the repeat-walk question was measured and **refused** — 11.0%, not the 68.3% the
raw journal suggests, worth **$0.30–0.60 for the project's whole lifetime.** The most interesting
thing I found this round is worth less than a single page walk.
