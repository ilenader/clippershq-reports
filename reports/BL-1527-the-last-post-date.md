# BL-1527 — THE LAST-POST DATE, THE PAGE-SIZE CEILING, AND WHAT WE BUY AND NEVER READ

**Round:** BL-1527 · **Date:** 2026-09-07 · **Spend: $0.0598 of a $1.50 cap (4.0%)**
**Production files changed: none.** Read-only: probes, measures, names defects with `file:line`
and leaves them.
**Safe to run beside anything:** yes.

---

## THE ANSWER, IN ONE PARAGRAPH

**Can we get the last-post date? Yes on Instagram, mostly no on TikTok — and that split is the
whole dispute.** He said *"I can tell with assurance that it gives us the date of the latest
post… I go to that date and it's correct."* He is right, and so is the report, because they are
about different routes. On the **Instagram hashtag route the surfaced date is the account's
newest post with a median error of 0.0 days and 97.3% [95.9, 98.2] within a week** — checking it
looks correct essentially every time, because it *is* correct. On the **TikTok hashtag route the
median error is 12.4 days, p90 157.8 days and the worst case 1,895 days**, and only 6.6% [4.2,
10.2] are provably the newest. **No last-post field is hiding under a name nobody searched** —
post dates resolve to exactly four names, and the paid TikTok profile carries none of them (46
leaf keys, 2 timestamps, neither within a day of truth on 3 of 3 accounts driven live).
**Can we get more than 30 per call? No, anywhere.** TikTok refuses 40/50/100 with an HTTP 400 on
hashtags and an HTTP **422 that names the limit** (`"Input should be less than or equal to 30"`,
`ctx {le: 30}`) on search; Instagram's v2 hashtag endpoints have **no size parameter at all**
while `config.ig_page_size: 50` is wired through four files and never granted; and the one
documented no-maximum lever, `amount` on the v1 route, returns **30 items at `amount=200`**.
**Paging, however, works and is not the same question** — one Instagram tag walked 35 pages for
793 distinct authors with zero byte-identical pages. **What are we buying and not reading?** The
strongest candidate in the brief collapses on inspection, but a new one is real:
`image_versions2.additional_candidates.first_frame`, present on 532/549 IG media at 640×1136 —
4.1× the judge's pixel floor — **a different image from the cover on 532 of 532**, with zero
readers. And `is_top`, the **pinned** flag, is on 1,033/1,033 TikTok `aweme_list` items and read
by nothing, while pinned posts carry **543.6×** the views of unpinned and sit a median 141 days
behind the account's newest.

---

## 1. WHAT THIS ROUND WAS ASKED TO DO

Three questions, driven live rather than read:

1. **Does a post date exist, and is it the account's newest?** The operator disputes a published
   finding and **he has observed the thing work**. A report is not evidence against an
   observation — it is a competing measurement, and this round settles which is right.
2. **Can one call return more than 30?**
3. **Can one call carry more information — what do we already buy and never read?**

Plus one reserved agent: *what is in these payloads that would let us decide without a model?*

---

## 2. WHAT SHIPPED

**Nothing, by design.** No production file was modified, no threshold moved, no verdict changed.
Defects are named with `file:line` in §4 and left.

---

## 3. Q1 — DOES A POST DATE EXIST? YES, AND THERE IS NO HIDDEN FIELD

**MEASURED.** Post dates resolve to exactly **four** field names across every payload on disk:
`taken_at` (3,599 occurrences), `create_time` (1,226), `createTime` (315), `taken_at_ts` (189).

**The paid TikTok profile carries none of them.** `/v1/user/by/username` driven live on 3
accounts whose true newest post was established independently: **46 leaf keys** (a prior record
said 56 — **named as a discrepancy, not reconciled**) and exactly **two** timestamps,
`createTime` (account creation) and `nickNameModifyTime` (a name change). **Neither was within a
day of the true newest post on 3 of 3.** The hunt was **by value shape, not by name** — every
integer or numeric string at any depth inside the unix-timestamp window.

### 3.1 Why an earlier value-search returned "NOT ESTABLISHED" — and it was the classifier

The brief named three classes to exclude, and a sub-agent found **two more** that a pure
value-shape sweep miscounts:

| class | why it is not a post date | scale |
|---|---|---|
| `extra.now` | the vendor's server clock — ~today by construction | — |
| `fetched_at` | our own write time — ~today by construction | — |
| signed-URL `expire` | when the **link** dies, not when the post was made | — |
| **10-digit identifiers** | `user.pk`, `user.pk_id`, `user.id`, `strong_id__`, `caption.user_id` — **IDs that fall inside the unix window** | **~1,900 hits** |
| **dates of a different object** | `clips_metadata.original_sound_info.time_created` (2,308), `music.create_time` (998), `added_sound_music_info.create_time` (998), `author.unique_id_modify_time` (1,033), `user.latest_reel_media` (417) | **~5,754 hits** |

A sweep that counts those reports a haystack of candidates and concludes nothing. **The absence
of a hidden last-post field is now a real absence, not an instrument artefact.**

---

## 4. Q2 — IS IT THE NEWEST? THE ANSWER SPLITS BY ROUTE

### 4.1 The error distribution — median AND tail, separately

Error = (account's true newest post) − (the date the route surfaced), in days. Positive means
the surfaced date is **stale**. Every figure is a **LOWER BOUND**: the reference is the newest
post provable from the data, so the true error can only be larger.

**Pooled, all routes, n = 3,365 observations / 559 authors (MEASURED, on-disk):**

| median | p75 | p90 | p95 | p99 | **max** |
|---|---|---|---|---|---|
| **1.9 d** | 7.9 d | **78.6 d** | 205.8 d | 731.9 d | **2,137.1 d** |

within 7 d **73.0% [71.5, 74.5]** · within 30 d **85.0% [83.7, 86.2]** · within 180 d **94.3%
[93.5, 95.1]** · **over 180 d 5.7% [4.9, 6.5]** · over 365 d 3.4% [2.8, 4.0]

**And the split that resolves the dispute (MEASURED):**

| route | n | median | p90 | max | within 7 days |
|---|---:|---:|---:|---:|---|
| **Instagram hashtag** | 782 obs / 347 authors | **0.0 d** | **4.0 d** | — | **97.3% [95.9, 98.2]** |
| **TikTok hashtag `itemList`** | 272 obs / 14 authors | **12.4 d** | **157.8 d** | **1,895 d** | only 6.6% [4.2, 10.2] are provably newest |
| TikTok `aweme_list` | 1,025 obs / 105 authors | 9.9 d | 224.6 d | 1,619.7 d | — |

**A methodological control that had to be added, and that changes the numbers:** an old page
correctly reported the newest post *at its fetch time*. Without clamping the reference to each
file's fetch epoch, the mere passage of time scores as route error. Fetch epochs were recovered
per file (payload clock on 14 files, signed-URL `expire` on 7, mtime on 340). Sensitivity on
payload-clock files only: median 10.3 d, p90 205.5 d, over-180 d 11.7% [10.1, 13.5].

### 4.2 My live measurement disagrees with the on-disk one. Both are named.

I drove this independently: one live TikTok hashtag page on 2026-09-07, 24 accounts, truth =
`max(create_time)` over each account's **own** posts via `search(username)` — a *different*
endpoint from the hashtag route, so the comparison is not circular.

| instrument | n | median | p90 | max | within 7 d |
|---|---:|---:|---:|---:|---|
| **live, mine** | 24 | **1.23 d** | 13.74 d | 67.62 d | 70.8% [50.8, 85.1] |
| **on-disk, sub-agent** | 272 | **12.4 d** | 157.8 d | 1,895 d | — |

**They disagree by an order of magnitude on the tail and I did not reconcile them.** Mine is
fresh but small (n=24, one page, one day) and its truth source is capped at 30 of an account's
own posts; the sub-agent's is far better powered and spans many pages and dates. **Neither is
averaged.** The honest reading: the on-disk figure is the better-powered estimate of the tail,
and my live figure shows the *median* really is small on a fresh page — which is exactly the
condition under which he checks it.

**And my own live figures had to be stratified**, because a low own-post count forces the error
to zero by construction — if `search(username)` returns only the same post the hashtag route
showed, the error *cannot* be anything else:

| stratum | n | median | max | within 7 d |
|---|---:|---:|---:|---|
| own ≤ 3 (weak evidence) | 5 | 0.00 d | 3.93 d | 100.0% [56.6, 100.0] |
| **own ≥ 10 (strong evidence)** | 14 | 1.64 d | 67.62 d | **57.1% [32.6, 78.6]** |

The zeros cluster in the weak stratum exactly as predicted. **57.1%, not 70.8%, is the honest
within-a-week figure from my live pass.**

### 4.3 The 50% disagreement figure was NOT reproduced — and its source file cannot carry it

The published *"19 of 38 repeated authors = 50.0%"* could not be re-derived: the named source
file has author identities replaced by redaction placeholders, so all 239 items collapse to
**one** distinct author. The 186-distinct-author figure cannot come from that file, and the
unsanitised source is not on disk. Two independent instruments, **both named**: within a single
page, **267 of 277 repeated-author cases disagree = 96.4% [93.5, 98.0]**; pooled across files,
**399 of 560 = 71.2% [67.4, 74.8]**. **Direction confirmed, magnitude higher than 50%.**

**Descending time order: 0 of 75 Instagram hashtag pages and 0 of 5 TikTok hashtag pages.**

### 4.4 Why the feed does this, reproduced

The feed ranks on performance, not recency. On the TikTok hashtag route, posts **>180 days old
carry median 3,000,000 views against 523,200 for posts <30 days — 5.5×** (a prior reading said
6.9×; both named). On `aweme_list` the gap is **20.4×**. **Instagram shows no such gap (0.31×)**
— consistent with its near-zero date error.

### 4.5 THE PINNED FLAG — present, 100% filled, and read by nothing

**`is_top` is on 1,033 of 1,033 TikTok `aweme_list` items (100.0% [99.6, 100.0])** and 65/65
`search_item_list` items, with **159 carrying `is_top = 1`**. `is_pinned` appears on 12
Instagram items. It is **genuinely absent** on the TikTok hashtag `itemList` route (0/313, [0.0,
1.2]) and Instagram hashtag (0/2,006, [0.0, 0.2]) — the same sweep reports both, so those zeros
are the payload's, not the instrument's.

**It has zero readers in `clippershq/`.** Meanwhile `clippershq/clip_walk.py:38-41` and
`harvest_accounts.py:38-40` both state that pinned posts break reverse-chronological order
outright and route around it via `sort_by_views` — **while nothing reads the flag that
identifies one.**

**Measured cost of not reading it:** pinned median **1,562,246** views vs unpinned **2,874** =
**543.6×**; pinned items sit a median **141 days** behind the account's newest (p90 732 d)
against 6.1 d for unpinned.

---

## 5. CAN ONE CALL RETURN MORE THAN 30? NO — DRIVEN ON BOTH PLATFORMS

**All MEASURED live this round. Validated on LIST LENGTH, never on status.**

| endpoint | asked | result |
|---|---|---|
| `/v1/hashtag/medias` (TikTok) | 30 | 30 items |
| | 40 / 50 / 100 | **HTTP 400 BadRequest**, 0 items |
| `/v2/search` (TikTok) | 30 | 30 items |
| | 40 / 50 / 100 | **HTTP 422 naming the limit**: `"Input should be less than or equal to 30"`, `ctx {le: 30}` |
| `/v2/hashtag/medias/{clips,top,recent}` (Instagram) | `count` = none / 50 / 100 | **identical** — the parameter is accepted and ignored |
| `/v1/hashtag/medias/clips` (Instagram) | `amount` = none / 50 / 100 / **200** | **30 items every time**, HTTP 200 |

**⚠️ The saved vendor spec is STALE AT THE SAME VERSION NUMBER — exactly the hazard the brief
predicted.** All four LamaTok dumps on disk (v1.3.3, 23 paths) document `/v2/search` `count` as
**min 1, max 50, default 20**, and document **no `page_id` at all** even though `page_id` is
measured working. **The live 422 says the real maximum is 30.** The version did not move. I could
**not** re-read the live spec — all four documented suffixes returned HTTPError — so "the spec has
not grown" is **UNREACHED, not verified**; but the *ceiling* is now settled by driving it.

### 5.1 The four denominators, counted separately (they are not the same number)

Live, one Instagram call per endpoint:

| endpoint | sections | top-level slots | carousel children | slots incl. children | distinct `media.pk` | **distinct AUTHORS** |
|---|---:|---:|---:|---:|---:|---:|
| `/clips` | 10 | 30 | 0 | 30 | 30 | **29** |
| `/top` | 9 | 33 | 27 | 60 | 56 | **27** |
| `/recent` | 9 | 27 | 24 | 51 | 51 | **23** |

**`/clips` yields the most distinct authors, which is the only denominator that matters for
supply.** On-disk corpus (74 payloads): sections 642 · slots 1,932 · incl. children 1,961 ·
distinct pk 1,931 · **distinct authors 1,877**; max slots per page **33**, modal 30.

**Three containers, and the brief undercounts the risk.** On `/top` the split is `medias[]` 24 +
`fill_items[]` 4 + `one_by_two_item.clips.items[]` 5 = 33 — so **9 of 33 (27.3%) sit outside
`medias[]`, not 4 (12.1%)**. **The shipped extractor reads all three** (`ig_discovery.py:219,223`;
`repost_finder.py:280-285`; `envelope.py:133`): executed, it returns **33** against a
`medias`-only control's **24**, and the 9-sections-as-9-medias trap is guarded at
`envelope.py:126-133`. **No live defect here.**

**A stability control before crediting any difference:** `/top` called three times with identical
parameters returned **56/56 identical media pks** all three times. So the surface is stable
within a burst, and the 21→27→27 author spread across my `count` sweep is **not** attributable to
`count`.

### 5.2 Paging is a different question, and it works

- **Instagram hashtag paging genuinely pages:** one tag walked **35 pages for 793 distinct
  authors, 0 byte-identical pages, minimum 15 net-new authors per page** — counted by **author
  ID, never by a count**, because a bogus cursor once returned more "new" accounts than the real
  one by changing the cache key.
- **`more_available` is `True` on all 68 pages examined, including a 3-slot one.** It never says
  stop. Any walker trusting it walks forever.
- `/v2/search/accounts` — the vendor's own summary says *"The current route doesn't support
  paging."*

### 5.3 Two paging defects, named and left

- **`clippershq/discovery_search.py:263` never pages.** AST: **0** `page_id` identifiers; grep:
  **0** lines including string literals; control on `ig_discovery.py` returns True, so the
  instrument fires. **It is a split fix:** `page_id` landed in `api_client.py:383,414` and in
  `tiktok_finder.videos_from_search:598` — **but not in the walker `main.py:3874` actually
  calls.** There are two search walkers and the campaign runner uses the unpaged one, which then
  declares the well exhausted on its own offset-stall guard at `:325`.
- **`clippershq/main.py:3875` clamps `count=min(50, …)`** against a ceiling the vendor enforces
  with a 422, saved only by `api_client.py:411` re-clamping to 30. **But `page_count` has no
  config wiring at all**, so the real flow is 30 → 30 → 30 and **neither clamp has ever fired.**
  Removing the re-clamp changes nothing today; it would matter the moment `page_count` became
  settable.
- **`clippershq/envelope.py:364-365`** — a list-absent `{"status":"ok","status_code":0,"message":
  "No more videos"}` returns state `single` and **1 item**. **Fail-open.**
- **`clippershq/envelope.py:339-342`** — an `[items, cursor]` payload returns **0** items and
  `EMPTY`. No longer "counted as 2", but now **fail-closed**, which writes off a live endpoint.

---

## 6. WHAT ARE WE BUYING AND NOT READING?

**Five of the thirteen briefed candidates are already read in production** —
`like_and_view_counts_disabled` (`ig_discovery.py:441`, `clip_runner.py:566`), `ig_play_count`
(`ig_discovery.py:76`, `paid_grid.py:218`), `media_repost_count` (`ig_discovery.py:430`),
`fill_items` (`envelope.py:111,133`), and `music.is_original_sound`, whose only production
mention (`discovery_search.py:159`) writes it off as measured-useless.

### 6.1 The brief's strongest candidate collapses — three ways

`video.cla_info.original_language_info.is_burnin_caption` was offered as *"free, and the signal
the OCR gate currently pays to derive."* All three parts fail:

1. **The OCR gate costs $0.00 in vendor money already** — `clip_ocr.gate_text_for` OCRs an mp4
   already on disk.
2. **Its one caller (`harvest_run.py:212`) is Instagram-only, and `cla_info` does not exist on
   Instagram.**
3. **It derives watermark / at-mention identity, not speech subtitles** — the ground-truth file files
   "dialogue subtitles" under neither.

And structurally: **`is_burnin_caption` is 0/74 [0.0, 4.9] on `/v1/hashtag/medias`** — the lane
that is 98.7% of his graded corpus — and where the schema does exist it is silent on **604/978
(61.8% [58.7, 64.8])**, because `original_language_info` only appears when `no_caption_reason ==
0`. Effect on his verdicts is **NOT VERIFIED**: his 311 graded handles and the 100 `cla_info`
handles overlap **0 of 100**.

### 6.2 The new #1, which was not in the brief

**`image_versions2.additional_candidates.first_frame`** — present on **532/549 IG media [94.6,
98.0]**, **640×1136 on 90.8%** (4.1× the judge's 155 px floor), and **a different image from the
cover on 532 of 532 = 100.0% [99.3, 100.0]** (control: `candidates[0]` against itself is
identical 532/532). **Zero readers** across 164 production and 105 secondary files. The judge
currently sees only the cover, which is a *chosen title card*; this is frame 0, free, inside a
response already bought.

**#2 `videoSuggestWordsList`** — TikTok's own search phrasing with stable `word_id`s, **13/74
[10.6, 27.8]**, unread, and the only unread candidate on the shipped lane.
**#3 `location`** — `name/address/city/lat/lng` on **87/87** dicts present (87/549 fill), and
`market_filter.infer_country_from_profile(location=…)` **already exists**, fed only by a Spotify
city. A consumer with no supply.

**Closed:** TikTok's sprite sheet is `video.big_thumbs`. It exists and is fetchable (`img_urls`
79/79) but tiles are **27×48**, with **0/79 reaching 155 px** — worse than Instagram's already-
rejected 100×176, and absent from the shipped lane. **`top_likers`** is the absent-vs-empty trap:
key present 100%, non-empty **95/642 = 14.8% [12.3, 17.7]**, always length 1.

**⚠️ THE HONEST BOTTOM LINE: zero of the thirteen has a measured effect on an operator verdict.
Every recommendation above is a SUPPLY claim, not an accuracy claim** — and when TikTok facts
were last actually forwarded and measured, not one field earned its tokens and the bio was
slightly worse.

---

## 7. THE RESERVED QUESTION — DECIDING WITHOUT A MODEL

**The blocking finding first: for his 311 graded TikTok pages, the number of stored raw vendor
payloads on disk is ZERO.** Ten payload stores were walked; labelled-handle coverage was 1, 7, 3,
8, 0… The only artefact covering 311/311 is a **derived** funnel row of 40 keys, 9 of them with
no non-null variance. **So the 1,678 varying-and-unread vendor fields cannot be scored against
his grading at all from disk.**

What the 40 derived fields do give (WANT = score ≥ 6; n=311, 101 want; planted control AUC
1.0000 p=0.0005; noise control AUC 0.4293–0.5441, p ≥ 0.16):

- **Recency** (`last_post_epoch`, free, 311/311): **AUC 0.6124, permutation p = 0.0014**, and
  **0.617 pooled within `found_via`**, so it survives channel stratification. Median days since
  last post: **145.9 for his 1s and 2s against 27.4 for his 8–10s.** ⚠️ But it is **all bottom,
  no top** — the most-recent decile sits at base rate (0.323 vs 0.325, lift 0.99×) and the whole
  signal is the stalest quartile at 14.1% [8.1, 23.5]. As a cut it loses **11 of 101 wanted for
  25% of traffic**, which is worse than the free gate already shipping.
- **A follower CEILING** — the inverse of the long-refused *floor* — on the **free link-preview
  count** (`tiktok_finder.py:1715`, $0.00, n=178): **AUC 0.6091, p = 0.030**, within-channel
  0.6031. Top quintile (≥50,500) want rate **0.132 [0.058, 0.273]** against a 0.247 base. At
  100,000 it removes 12.9% of traffic and kills 1 of 44 wanted — **kill-rate CI [0.4%, 11.8%], so
  "1 of 44" is not safe.** `follower_max` already exists (`quality_gate.py:2183`), set to
  10,000,000 in all four campaigns, firing on 1 of 178.
- Two free fields together: low-followers/recent **43.2% [29.7, 57.8]** against high-followers/
  recent **17.8% [9.3, 31.3]**.

**Refuted with numbers:** handle-string lexicon (best term AUC 0.5198 — *under* the noise
control), `avg_views` (0.4483, p = 0.50), evidence count (p = 0.89), hearts (p = 0.95),
following (p = 0.67), mean share (p = 0.45).

**⚠️ Two hazards stated rather than buried:** all 311 come from **one capture batch**, so they
cannot be stratified; and **the contact sheet displayed `last_post_days` to him**, so readback
cannot be ruled out on the recency finding — he may partly be grading the number the finding is
derived from. A second corpus (n=57) fails to replicate recency (p = 0.53), though it is
range-restricted with 57/57 already WANT.

**A note that connects §4 to this:** the recency signal is computed on `last_post_epoch` — the
very field this round shows is stale by a median 12.4 days on the TikTok hashtag route. The
signal's gap (145.9 d vs 27.4 d) is an order of magnitude larger than that error, so it plausibly
survives; **but nobody has measured it on a corrected date, and I have not either.**

---

## 8. WHAT I GOT WRONG

**Six failures — five instruments, four of which produced a ZERO, and one redaction that damaged
the file it was protecting. Every zero was caught only by refusing to believe it without a
control.**

1. **The universal zero that cost $0.0144.** My first date probe looked for items under
   `("itemList", "aweme_list", "medias", "items", "data")`. `/v2/search` returns them under
   **`search_item_list`** — and **`aweme_list` exists and is empty**, so a key-presence check
   finds it and reports zero. All 24 accounts came back `own=0`, which reads exactly like "the
   vendor has no data for these accounts". **Production was never affected:**
   `discovery_search.py:28-31` already leads its candidate list with `search_item_list` and skips
   empty lists by design, with a comment naming this exact trap. The rewrite imports production's
   own parser rather than writing a third one.
2. **I measured my own clamp and called it the vendor.** `api_client.search()` does
   `count = max(1, min(SEARCH_MAX_COUNT, int(count)))` **before sending** (`api_client.py:411`),
   so asking it for 40 or 50 asks the vendor for 30 and returns a tidy 30 that looks exactly like
   a silent vendor clamp. I recorded "silently clamped" — it was my own code. Re-driven through
   `_get`, the vendor's real answer is a 422 that names the limit.
3. **I fed a `Response` object to a JSON counter.** `ig_client.raw_get` returns the response
   object, not parsed JSON, so my Instagram `amount` probe scored a live 30-item payload as 0 and
   I nearly reported "the v1 route returns nothing."
4. **Then I counted the wrong containers on it.** After parsing, the v1 route turned out to
   return a **bare list**, not the v2 `sections`/`medias`/`fill_items` shape my counter
   understood — a second zero on the same probe, same root cause: counting a container I had not
   confirmed.
5. **My own spend log overcounted by 19%.** `prove_cap()` exercises the refusal contract with
   throwaway meters, and every synthetic reservation wrote to the **same** JSONL as the real
   calls — 18 phantom rows in 114. A naive `sum(usd)` reported 4.7% of cap where the truth is
   4.0%. A counter that counts the wrong thing and is believed because it is precise is the exact
   shape this project keeps paying for, and I built one.

6. **My redaction corrupted the file it was redacting.** A sub-agent's raw JSON carried 57
   handles and 11 email addresses. I redacted by regex **over the serialised JSON text**, and the
   address pattern consumed part of an escape sequence — leaving a dangling backslash that made
   the file invalid JSON. Redacting a JSON document by regex over its own text can eat half an
   escape; the safe form walks the parsed object and replaces whole values, because `json.dump`
   then re-escapes correctly. My second attempt at that then hit **lone surrogates** in the bio
   strings (`ensure_ascii=False` cannot encode them) and truncated the file mid-write. Since the
   file was a raw intermediate whose findings already live in the agent's actual deliverable, and
   it carried real addresses, **I deleted it rather than keep patching a PII-bearing artefact.**
   It had never been committed, so nothing published was affected. Final state verified by a
   full-commit-set scan: **95 files, 0 carrying a handle or address**, detectors proved on
   planted controls first.

**And one reading error:** the vendor's `requests` field **counts down** — it is remaining quota,
not cumulative usage — so my first before/after comparison read a correct −26 as a disagreement
between instruments.

---

## 9. MONEY AND SAFETY

**From the run's own counter at the wrapper, booked explicitly**, because
`clippershq/api_client.py` **contains no ledger writer at all** (verified by grep: zero hits for
`record_spend`/`spend_ledger`/`_book_paid`/`ledger`), so every LamaTok call ever made is invisible
to `spend.json`.

| | calls | rate | cost |
|---|---:|---|---:|
| TikTok (LamaTok) | 72 | $0.000600 | $0.043200 |
| Instagram (HikerAPI) | 24 | $0.00069064 | $0.016575 |
| **TOTAL** | **96** | | **$0.059775 of $1.50 (4.0%)** |

**⚠️ TWO INSTRUMENTS ON THE SPEND, AND THEY DISAGREE. Both are named; neither is averaged.** My
wrapper counter says 72 TikTok calls. The vendor's own receipt (`/sys/balance`) fell from 425,914
to 425,780 = **134 consumed**, a gap of **62**. I tested the leading candidate and **ruled it
out**: three consecutive balance readings returned an identical figure, so `/sys/balance` is
genuinely free and its docstring is right. **The cause of the remaining gap is NOT ESTABLISHED** —
retries inside the client on the 400/422 probes, or another process on the same key, are both
plausible and I did not distinguish them. **Even on the pessimistic reading the round spent
$0.0804, or 5.4% of cap.** The wrapper counter is the only *attributable* instrument; a shared
vendor key means the vendor's own counter cannot attribute a single round, which is the same
lesson as "never use a ledger delta", one level up.

**The cap was proven to bind before the first call**: a $0.00 cap **raised** and **the meter did
not advance**; a funded cap **allowed** and metered (the positive control, without which a
refusal proves nothing); a two-call ceiling bound at exactly two and stayed bound.

**Backups:** 7 files (config, ledger, all five seen stores), every one sha256 MATCH, path built
from one round constant, corruption control fired. Bodies found **by shape** — `spend.json` is a
list at `runs` (30,081 rows), `clip_seen.json` a bare list (2,193).
**And the deletion control planted the shape a key-set check is blind to:** `spend.json` holds
30,081 rows under only **23,911 distinct natural keys**, so deleting one of a duplicated pair
leaves the key set **identical** (23,911 → 23,911) — invisible — while the index-qualified row
hash caught it.

**Redaction, verified by reading the bytes back:** the profile payload is keyed **by handle**, so
every leaf path embedded a real creator handle; all six were redacted as **whole values, never
truncated**, and the file re-read to confirm zero residuals. A raw payload dump was deleted
outright. **A scan of the whole commit set — not just the report — found a sub-agent's raw JSON
carrying 57 handles and 11 email addresses**; it is redacted before commit. Every detector was
proved on a planted control first.

No process was killed. No production file was modified.

---

## 10. WHAT HE SHOULD DO NEXT — RANKED

**1. Trust the Instagram date. Do not trust the TikTok hashtag date as a *newest-post* date.**
IG hashtag: median error 0.0 d, 97.3% within a week. TikTok hashtag: median 12.4 d, p90 157.8 d.
**But the shipped treatment is still correct**, because the funnel uses a **180-day** wall and
94.3% of all errors are inside 180 days — the date is fit for the purpose it is actually used
for, and unfit for the purpose its name suggests. **MEASURED.**

**2. Read `is_top`. It is free, 100% filled on two TikTok lanes, and nothing reads it.** Pinned
posts carry **543.6×** the views and sit a median **141 days** behind the account's newest — so an
unread pin flag corrupts both the recency signal and any view-based ranking. Two production files
already work around pinned posts without ever identifying one. **MEASURED.**

**3. Stop asking for a page size larger than 30 — it has never once been granted.**
`config.ig_page_size: 50` is wired through four files and silently ignored; TikTok refuses with
400/422. **Delete the parameter or document it as inert**, and put the effort into **paging**,
which genuinely works (35 pages, 793 distinct authors). **MEASURED.**

**4. Fix the split paging fix.** `page_id` landed in the client and in one walker but **not in
the walker the campaign runner calls** (`discovery_search.py:263`, called from `main.py:3874`).
That walker returns page 1 forever and then declares the well exhausted. **MEASURED.**

**5. Try `first_frame` on the Instagram judge.** 532/549 present, 640×1136, **a different image
from the cover on 532 of 532**, zero readers, already inside a response being bought. It is the
only unread field in this round with both real fill and real pixel size. **Supply claim, effect
NOT VERIFIED.**

**6. Spend $0.19 to make the reserved question answerable.** One raw re-pull of his 311 graded
handles' own videos (~311 LamaTok calls), **stored raw**, would let every one of the 1,678
varying-and-unread fields be screened against his actual grading — which today is impossible
because zero raw payloads for those pages exist on disk.

**7. Do not act on the recency or follower-ceiling signals yet.** Both are real (p = 0.0014 and
p = 0.030) and both fail their own cost test: recency as a cut loses 11 of 101 wanted for 25% of
traffic, and the ceiling's kill-rate CI reaches 11.8%. The sheet also **showed him** the recency
number, so readback is not excluded.

---

## 11. WHERE THE FILES ARE

All committed under `BL-1527` in `%USERPROFILE%\…\clipper finder\scratch\`:

| Path | Contents |
|---|---|
| `bl1527_probe.py` | The meter, the cap contract, the value-shape timestamp walker |
| `bl1527_drive_dates2.py` | Live Q2 via production's parser · `bl1527_dates2_checkpoint.json` |
| `bl1527_error_distribution.txt` | The stratified live error distribution |
| `bl1527_drive_routes.py` | Profile leaf dump, live-spec attempt, TikTok ceiling |
| `bl1527_drive_ig.py` · `bl1527_ig_rotation.py` | IG four-denominator counts; the stability control |
| `bl1527_ig_v1_amount2.py` | The `amount` ceiling, counted on a bare list |
| `bl1527_reconcile.py` · `bl1527_isbalancefree.py` | Counter vs vendor receipt; the free-call test |
| `bl1527_a1_fields.json` | Field census, ranked |
| `bl1527_a2_paging.json` | Paging defects, five denominators, spec inventory |
| `bl1527_a3_dates.json` | The on-disk error distribution and the pin-flag census |
| `bl1527_a4_reserved.json` | The model-free screen |
| `bl1527_safety.py` | Backups, corruption + duplicate-key deletion controls |

Reproducing the headline costs about **$0.02**:

```
PYTHONIOENCODING=utf-8 python scratch/bl1527_drive_dates2.py     # the dispute, live
PYTHONIOENCODING=utf-8 python scratch/bl1527_ig_v1_amount2.py    # the 30 ceiling
PYTHONIOENCODING=utf-8 python scratch/bl1527_reconcile.py        # counter vs vendor
```

`PYTHONIOENCODING=utf-8` is required — the default console encoding here is `cp1252` and any
script emitting a warning glyph dies on it.
