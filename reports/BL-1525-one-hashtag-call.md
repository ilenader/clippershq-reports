# BL-1525 — One hashtag call: everything it returns, and what we still have to pay for

**Round:** BL-1525 · **Filed:** 2026-09-06 · **Cap:** $1.50 · **Spent: $0.1459**

---

## 1. Safe to run, and the headline answer

**Safe to run.** No judging rule was added or loosened and no threshold moved. Every change is
mutation-proved in both directions with the restore verified, every new test uses `raise` rather
than `assert` and is green under `python -O`, and delivered counts were measured on both TikTok
brains and did not move. Nine defects are named with `file:line`; the ones that would change what
the judge sees are **named and LEFT**, because no paired score exists to license them.

### What one hashtag call gives us, what we still pay for, and what 1,000 addresses cost

**One TikTok `/v1/hashtag/medias` call at page size 30 returns 29-30 videos, 24-27 DISTINCT
AUTHORS, and 317 fields per item — and the author block in it carries everything the paid profile
call exists to buy.** The bio (`author.signature`) is free on **88.7%** of items, the follower
count and video count on **100%**, `verified` and `privateAccount` on **100%**. Paid bio versus
free bio was 35 of 35 byte-identical in the previous round; this round measured the direct
consequence: **52 paid TikTok profile calls returned ZERO addresses [0.00, 6.88]**, and the
session's only address came from the free bio. **The TikTok profile purchase is now switched OFF**,
reversibly, and delivered did not move on either brain.

**What we still have to pay for is one field per platform, and they are not the same size.** On
TikTok it is **`bioLink`** — absent from 30 of 30 free author objects, worth a measured **1 address
in 60**. On Instagram it is **the contact email**, and that one is irreplaceable: the Instagram
hashtag payload carries **no biography, no follower count, no email and no post count at all** —
only `is_verified` — and **51.03% [47.96, 54.09] of 1,019 Instagram addresses came from the paid
contact button and appear nowhere in the bio.** ⚠️ **So "stop paying for what we already have" is a
TikTok instruction and an Instagram trap.** The Instagram profile call is deferred to survivors and
must never be removed.

⚠️ **AND THE DECIDING QUESTION IS ANSWERED NO.** The hashtag call carries a post date on
**239 of 239 items**, but it is the date of *the video that matched the tag* — **50.0% of authors
appearing twice carried different timestamps, the largest 449.8 days apart**, and **0 of 8 pages
were in time order**. **There is no pinned flag on this route at all.** The paid profile has no
last-post field either and LamaTok has no user-videos endpoint, so **a true last-post date is not
purchasable at any price.** The operator's condition — "the bio, and when the last non-pinned video
was posted" — is **half-satisfiable, and the shipped floor treatment is already the right one.**

**WHAT 1,000 EMAIL ADDRESSES COST, MEASURED.** On the cheapest route on record — TikTok hashtag to
the free bio — **$3.26 per 1,000 addresses** at the margin, after 50,041 pages have already been
banked, and **$0.47 per 1,000 on fresh supply**. Project lifetime all-in has been **$5.03 to $6.99
per 1,000** depending on which denominator you name. ⚠️ **And the denominator nobody had looked at:
of 10,164 ledger-era address rows, 8,719 are CLIENT addresses, 1,291 meme_page, and only 120 are
CLIPPER** — so every per-address price this project has ever quoted, mine included, is
overwhelmingly the price of a client address, not of the clippers the funnel exists to find.

---

## 2. What I was asked to do

Dump every field one hashtag call returns on each platform, hiding nothing, with values redacted
and paths published. Answer first whether that call carries the last non-pinned post date. Then
stop paying for what we already have — defer or remove the TikTok profile purchase, move TikTok
to hashtags, fix the broken Instagram free read, wire or delete the payload sheet, ship three
already-measured free fixes, and recover 102 stranded addresses. **Rank everything by ADDRESSES
PER DOLLAR, not pages per dollar** — the operator's goal is email addresses, and no report in this
project had ever ranked by it.

---

## 3. What shipped

All changes are mutation-proved both ways with the restore verified, and every new test is `raise`
rather than `assert` and green under `python -O`.

| # | change | `file:line` | category | proof |
|---|---|---|---|---|
| 1 | **TikTok profile purchase switched OFF**, reversibly (`buy_profile`, read as `is True` so absent/null/`0`/`""` all mean don't spend) | `tiktok_finder.py:3927`, `:4255`, gate `:3431` | LOCAL (1 gate) | delivered 16→16 and 37→37; prompt sha256 identical over 18 real POST bodies with a control proved not blind, then moved by one flipped byte |
| 2 | **Eight `<topic>edit` hashtags supplied and walked**; his seven configured search terms passed through instead of discarded; the false note corrected | `tiktok_finder.py:3809`, `run_mode.py:105`, `:163` | GENERAL | live: 240 videos, 201 authors, free bio 183/201 = **91.04% [86.28, 94.26]**; `tags_walked` 0→8, `searches_walked` 3→7 |
| 3 | **Speech moved below the judge**, survivors re-judged, fails OPEN | `meme_finder.py:5622-5665`, `:7918-7961`, `:8106-8139` | GENERAL, **2 of 2 sites, count pinned by AST** | 47 checks; 18/18 mutation arms red |
| 4 | **The free `/embed/` owner block is read instead of discarded** | `ig_embed.py:150-268`, `:308`, `:316-318`; `payload_sheet.py:158-181` | GENERAL (extraction) + LOCAL (one key copy), **5 sites enumerated, 2 needed patching, 2 patched** | followers and posts **0/30 → 30/30**; **0 of 2,276 verdicts moved**, with a live control that injecting a follower count moves 2,276/2,276 |
| 5 | **Wall labelling fixed on all four branches** | `page_capture.py:619-676` | GENERAL, 4 of 4 | `login_wall` with tiles>0 = **257/310 = 82.9% [78.3, 86.7]**; `private` 0/386 and `unknown` 0/145 as the control |
| 6 | **The lost address recovered and the retry shipped at the shared layer** | `crossdedup.py:437-546`, `:576`; `atomic_io.py:75-135` (default unchanged) | GENERAL, **1 site covering all 8 funnels** | 72,962 → **72,963** rows, every prior row hashing identically **at its own index**; missing 1 → 0 |
| 7 | **Five sheet-rendering defects fixed** — the bare word "dialogue", the unenumerated fifth state, a truthiness test on a count, an untranslated machine key, and an unfloored negative count | `review_sheet.py:240-259`, `:308-373`, `:1497-1506`, `:1902-1910` | GENERAL | driven; the state he reads first can now see `not-reached` |
| 8 | **`profile_deferrable` given the protection it never had** (it was never broken — it had simply never run) | pinned by AST + positive control + dominance check | — | defers **29 of 61 = 47.54% [35.53, 59.84]** on this corpus |
| 9 | **A byte-window guard my own BL-1513 turned red, rewritten as a structural one** | `tests/test_bl1484_tiktok_latch_and_facts.py` | — | green as shipped, **RED when precedence is reversed**, green restored, production file sha256 unchanged |

**New tests, all enrolled:** `test_bl1525_stop_buying_the_tiktok_profile.py` (60 checks),
`test_bl1525_speech_wall_and_master.py` (47), `test_bl1525_free_owner_facts.py` (14),
`test_bl1525_payload_sheet_and_hero.py` (5).

---

## 4. What was measured

### 4a. PART 0 — does one hashtag call carry the last non-pinned post date? **NO.**

**This is the question the round turned on, and it was answered before anything else was done.**

**MEASURED, live, 12 billed LamaTok calls, 239 items over 8 `/v1/hashtag/medias` calls:**

| | n | Wilson 95% |
|---|---:|---|
| items carrying `$.itemList[*].createTime` | **239 / 239 = 100%** | [98.4, 100] |
| …on the single primary call | 30 / 30 | [88.6, 100] |
| absent / null / empty / zero | **0** | — |

**But it is the date of the video that matched the tag, not the author's newest post.** Of 186
distinct authors, **38 appeared more than once and 19 of those 38 (50.0% [34.8, 65.2]) carried
DIFFERENT timestamps** — largest disagreement **449.8 days**. **0 of 8 pages were in descending
time order**; one 30-item page spanned **1,894 days**. The feed ranks on performance: posts older
than 180 days carry median **3,000,000** views against **433,300** under 30 days (6.9×). **A
single appearance establishes only "this account posted at least this recently".**

⚠️ **AND IT IS NOT PURCHASABLE AT ANY PRICE.** The paid `/v1/user/by/username` call has **56 leaf
keys and no last-post field** — its `createTime` is *account creation*, and
`nickNameModifyTime` / `uniqueIdModifyTime` are name changes. LamaTok has no user-videos endpoint:
`api_client.py:439-447` **raises `UnsupportedEndpoint` rather than spending a call to be told
404**, recording that BL-1189 tested 23 paths and none returns a user's posts.

**Re-derived a second way, by me, offline at $0.00**, searching **by value shape rather than by
name** over every JSON on disk (6,036 files) for any post-shaped unix timestamp under *any* key:
**0 of 3 profile-only payloads carry one.** ⚠️ **n = 3, so this is CORROBORATION, NOT
CONFIRMATION**, and my script says so in its own verdict line — it originally printed "CONFIRMED"
and that was an overclaim on three files. ⚠️ **My first run of it returned NOT ESTABLISHED and
that was my classifier, not the data**: it counted `extra.now` (the vendor's server clock),
`fetched_at` (our own write time) and signed-URL `expire` fields as candidate post dates. A
timestamp meaning "now", "when we saved it" or "when this link dies" is not evidence of a
last-post date.

**Pinned posts: THE FLAG DOES NOT EXIST ON THIS ROUTE.** 0 pin-shaped keys among **241 distinct
leaf key names / 317 paths**, absent on **239 / 239** items [0.0, 1.6]. Positive control: the same
detector fires on a synthetic `is_top` and on the live `sticker*` keys, so the zero is the
payload's, not the instrument's. `isPinnedItem` / `is_top` / `isTop` / `pinned` also have **no
reader anywhere in `clippershq/`**. **Per the brief, this is reported as ABSENT per page and never
assumed False** — which matters, because pinned median views are 1,562,246 against unpinned 2,658.

**So the operator's condition — "if we can see the bio, and when the last non-pinned video was
posted" — is half-satisfiable.** The bio, yes. The date, no, and no amount of money fixes it. The
shipped treatment is already the correct one: `free_judge.py:1605-1621` documents the same finding
from BL-1371 (the surfaced post coincided with the account's newest on **2 of 18**, worst case 222
days) and treats it as a **floor** — "posted at least this recently" — which is exactly what the
evidence supports.

⚠️ **A FIFTH DEFECT, FOUND BY MY OWN LEAK SCAN AND NOT BY ANY AGENT — THE WALL DETECTOR HAS A
DEAD ARM.** `page_capture.py:182` builds a JavaScript regex inside a **non-raw Python string**, so
`\b` was interpreted by Python as a **BACKSPACE character (0x08)** instead of surviving as a regex
word boundary. What ships is `/<BS>log in<BS>/` and `/<BS>sign up<BS>/` — **patterns that can never
match anything.** MEASURED: 4 literal control bytes in the file, present identically at HEAD, so
this is long-standing and **not introduced by this round.**

It is one arm of four: the `log in to see|sign up to see|...` phrase test and the
password-field test still work, so the detector degrades rather than fails. **Named and LEFT** —
repairing it changes which pages are labelled walled, and this round is not licensed to move that
without a paired measurement. **This is the same `\b` corruption that has bitten this project
before in Windows paths**, and it was invisible to every reader because a backspace renders as
nothing.


### 4b. The full dump — one hashtag call, every field, values redacted

**Values are redacted; PATHS ARE THE DELIVERABLE and are published in full.** The exhaustive
per-path sheets are committed beside this report as evidence:
`scratch/bl1525_agentA_12_all_pages_field_table.json` (TikTok, 317 paths x 9 columns) and
`scratch/bl1525_agentB_*` (Instagram). The tables below are the parts that decide something.

**TIKTOK `/v1/hashtag/medias`, page size 30. MEASURED over 239 items across 8 calls.**
The item list is at **`$.itemList`** — TikTok's **web** shape, not the mobile `aweme_list`.
**317 distinct key paths, 241 distinct leaf key names.** Where they live:

| block | paths | what it is |
|---|---:|---|
| `video.*` | 96 | the media itself: bitrates, covers, subtitles, caption info |
| `music.*` | 25 | sound: title, author, original flag, human-voice flag, user count |
| `author.*` | 22 | **the account — see below** |
| `poi.*` | 19 | place-of-interest tagging |
| `anchors.*` | 18 | shopping / link anchors |
| `contents.*` | 15 | caption text and its entities |
| `textExtra.*` | 12 | hashtags and mentions inside the caption |
| `challenges.*` | 11 | the tags this video is in |
| `penaltyContext.*` | 11 | moderation state |
| `videoSuggestWordsList.*` | 9 | search terms TikTok associates with the video |
| `authorStats.*` / `authorStatsV2.*` | 8 + 8 | **follower, video, heart and digg counts** |
| `statsV2.*` / `stats.*` | 7 + 5 | per-video play, digg, comment, share |

**THE AUTHOR BLOCK — this is what makes the paid TikTok profile redundant.** Fill is over 239
items; "read" is by AST over `clippershq/`, with a control that a known-read key returns read and a
junk key does not:

| path | fill | varies | read by production? |
| `author.avatarLarger` | 100.0% | yes | **unread** |
| `author.avatarMedium` | 100.0% | yes | **unread** |
| `author.avatarThumb` | 100.0% | yes | **unread** |
| `author.commentSetting` | 0.0% | no | **unread** |
| `author.downloadSetting` | 5.9% | no | **unread** |
| `author.duetSetting` | 1.7% | yes | **unread** |
| `author.ftc` | 100.0% | no | **unread** |
| `author.id` | 100.0% | yes | read |
| `author.isADVirtual` | 100.0% | no | **unread** |
| `author.isEmbedBanned` | 100.0% | no | **unread** |
| `author.nickname` | 100.0% | yes | read |
| `author.openFavorite` | 100.0% | yes | **unread** |
| `author.privateAccount` | 100.0% | no | read |
| `author.relation` | 0.0% | no | **unread** |
| `author.secUid` | 100.0% | yes | read |
| `author.secret` | 100.0% | no | read |
| `author.shortDramaCreator` | 0.0% | no | **unread** |
| `author.signature` | 88.7% | yes | read |
| `author.stitchSetting` | 1.7% | yes | **unread** |
| `author.uniqueId` | 100.0% | yes | read |
| `author.verified` | 100.0% | yes | read |
| `authorStats.diggCount` | 100.0% | yes | read |
| `authorStats.followerCount` | 100.0% | yes | read |
| `authorStats.followingCount` | 97.9% | yes | read |
| `authorStats.friendCount` | 0.0% | no | **unread** |
| `authorStats.heart` | 100.0% | yes | **unread** |
| `authorStats.heartCount` | 100.0% | yes | read |
| `authorStats.videoCount` | 100.0% | yes | read |

⚠️ **Read the fill column against §4c: `signature` — the bio — arrives free on 88.7% of items,
`followerCount` and `videoCount` on 100%, `verified` on 100%, `privateAccount` on 100%.** Those
are the fields the paid profile call exists to buy.

⚠️ **TWO CAVEATS THAT THE COLUMN CANNOT CARRY, AND BOTH MATTER.** "Read" is matched on the LEAF
KEY NAME, so it is an **upper bound** — a name read anywhere in the repo counts here. And "unread"
means **no static reader was found, not that nothing reads it**: the same census recorded
**1,780 dynamic accesses in `clippershq/` that cannot be resolved statically** (2,294 on the
Instagram side, over 164 files with 0 parse failures).

⚠️ **AND I GOT THIS TABLE WRONG THE FIRST TIME.** My first pass read the AST verdict as a flag,
when it is four booleans, and so printed **UNREAD for all 39 author fields — including
`author.signature`, which production demonstrably reads.** I caught it only because that one row
contradicted code I knew. The table above is the corrected run, and it now carries the control that
would have caught it immediately.

**Fields that VARY, fill high, and have no static reader** — the honest haystack, since a constant
cannot decide anything: `music.is_original_sound`, `music.has_human_voice`, `music.user_count`,
`video.cla_info.original_language_info.is_burnin_caption` (**burned-in captions — free, and the
signal the OCR gate currently pays to derive**), `videoSuggestWordsList` (TikTok's own search terms
for the video), `CategoryType` and `diversificationId` (both 100% filled, both varying, both
undocumented — the nearest neighbours to the `aweme_type` photo flag that this route does not
carry).

**INSTAGRAM `/v2/hashtag/medias/top`. MEASURED, 18 billed calls.** **750 distinct key paths under
a single media, 154 direct children.** Of those 154: **93 fill at 100%, 95 are CONSTANT across
every item, and 25 never carry a real value at all.** Of 542 census leaf names, **63 have a static
reader and 479 do not.**

**Unread on the Instagram side, and worth a look:** `ig_play_count`, `media_repost_count`,
`top_likers`, `sprite_urls`, `first_frame`, `xray_visual_2025_100d_embed`, `location`, and
**`fill_items`** — that last one meaning **4 of the 33 medias in a response are invisible to any
statically-named extractor.**

### 4c. TikTok — the profile purchase is now OFF, and it cost nothing

**It was already DEFERRED.** BL-1516 had put the purchase below every free rule, the cover rules
and the picture judge (`tiktok_finder.py:3431`). What remained was to *stop* it, and that is now a
reversible config switch **defaulting OFF**: `config.json → tiktok_finder.buy_profile: false`, read
at `tiktok_finder.py:3927` as `is True` — so absent, null, `0` and `""` all mean **do not spend** —
passed at `:4255`, gated at `:3431`, with a `profiles_not_bought_by_switch` counter recording what
it saved.

**`createTime` reaches no rule at all.** `profile_of` (`:920`) has never extracted it; it is not a
key of the returned dict, so nothing downstream can read it. It is account age, not a last-post
date (§4a), and dropping the purchase costs no rule.

⚠️ **THE BRIEF IS WRONG BY ONE FIELD, AND IT IS THE REASON THIS IS A SWITCH AND NOT A DELETION.**
"Exactly one field is genuinely paid-only on TikTok" is not right — **`bioLink` is a second.**
Measured: **0 of 30 free author objects carry `bioLink` / `bio_link` / `bioUrl` / `link`** (Wilson
upper bound 11.35%), while `signature` — the bio — is non-empty on **29 of 30**. BL-1217 measured
the link's yield at **1 address in 60**. That is small, it is real, and it is named, which is
exactly why the purchase is switched off reversibly rather than deleted.

**THE DIRECT MEASUREMENT THAT SETTLES IT: 52 paid profile calls returned 0 addresses [0.00, 6.88].**
The session's only address came from the free bio.

**Delivered counts, both brains — the number that matters, not the call count.** Recorded once and
replayed twice, using the **pass counter** (not `leads`, which is delivered AND has an email AND is
new to master — three conditions, and reading it as "delivered" once overstated a brain's price by
5.00×):

| brain | delivered A → B | paid profiles | on ACCEPTED pages | on REJECTED pages |
|---|---|---|---|---|
| memes | 16 → **16** | 15 → 0 | 15 → 0 | **0 → 0** |
| edits | 37 → **37** | 37 → 0 | 37 → 0 | **0 → 0** |

Verdict fingerprints identical; replay misses 0. ⚠️ **The two arms mean different things and the
report says so:** arm A is the *ordering* proof — 0 purchases on rejected or unjudged pages, which
is BL-1516's guarantee holding. Arm B's zero is the operator's *decision* to stop buying, and it is
safe **only because delivered and the fingerprint did not move.** A change that simply stopped
buying would show the same zero on the first arm alone; that is the shape that once took a brain
from 18 delivered to 0.

**The judge prompt is byte-identical without the purchase.** sha256 over the **real POST body**
(`req.data` in `free_judge._ask`), 18 bodies: HEAD, working-tree default and working-tree
`buy_profile=False` **all hash to `5519b093587e1468…`**. ⚠️ **The control was proved not blind
first** — the handle *value* renders in 18 of 18 decoded bodies, so the hash sees the content that
matters — and then one flipped byte moved every hash to `9471115cdc6f26f0…` with exactly one
character differing per body. **A control that hashes a filename is blind by construction, and two
rounds did that independently.**

**TikTok now walks hashtags, and his edit terms are finally used.** `editing_hashtags` was `[]`;
it now carries eight `<topic>edit` tags — the shape he verified by hand — and **all eight resolved
and walked live: 240 videos, 201 distinct authors, free bio non-empty on 183 of 201 = 91.04%
[86.28, 94.26]**, corroborating the 93.1% from the earlier round. His seven configured
`editing_searches` were read at `:3775` and thrown away at `:3809`; they are now passed through a
new `configured_edits=` parameter on `run_mode.edit_searches_for:105`, and **the note at
`run_mode.py:163` that falsely claimed "no configured TikTok search term is an edit term" now
names both keys.** End-to-end at zero spend: EDITS `tags_walked` **0 → 8**, `searches_walked`
**3 (the hard-coded fallback that self-described as "NEVER RUN") → 7, his list verbatim.** MEMES
unchanged at 9 / 6.

**The `aweme_type` trade, stated plainly:** it is not merely lost on some items. The hashtag route
returns the TikTok **web** shape (`itemList` / `createTime`) and **the field is structurally absent
from it.** And it must not ship as a gate anyway — it kills **6 of 14 wanted pages = 42.86%
[21.38, 67.41]**, including two he scored 9, and **the direction is inverted**: photo posts are
*more* common on pages he wants.

**Protection:** `tests/test_bl1525_stop_buying_the_tiktok_profile.py` — **60 checks, `raise` not
`assert`, green under `python -O` and under `run_all.py`.** ⚠️ **It was scored "asserted NOTHING"
on its first run under the real runner**, which counts `[OK ]` lines, and that was fixed rather
than explained away. **5 of 5 mutations went red both ways with the restore verified by sha256**,
including one that re-swallows the boundary guard; guard non-swallowing is proved by AST — a named
handler before any bare `except Exception`.

⚠️ **AND A LESSON THAT INVERTS ONE OF THIS PROJECT'S OWN RULES.** "AST beats grep" is true for
reads, and **it under-counts writes hidden in strings**: `exemplar_sheet.py:267` buys a TikTok
profile **inside the `_SERVE` string literal**, where `ast.walk` sees 75 calls and none past line
131. **grep finds it instantly.** Code inside a string is invisible to the parser, so a purchase
census needs both instruments.

### 4d. Instagram — the paid profile is IRREPLACEABLE, and that is the round's central asymmetry

**MEASURED on a live `/v2/hashtag/medias/top` call (18 billed calls, $0.012432).** About the
author, the hashtag payload carries:

| field | present in the hashtag payload? |
|---|---|
| `is_verified` | **yes, 33/33** |
| `biography` | **ABSENT** |
| follower count | **ABSENT** — no `follower*` key exists, only viewer-relationship booleans |
| contact email | **ABSENT** |
| `media_count` | **ABSENT** |

**So the paid profile call is the SOLE source of the bio, the follower count, the post count and
the links** — above all of the contact email, which is the goal. Against the free routes on the
same accounts: biography **0/30 free vs 10/10 paid**, `external_url` 0/30 vs 5/10, email **0/30 vs
3/10**, `category` 0/30 vs 3/10. Corroborating the earlier round: **51.03% [47.96, 54.09] of 1,019
Instagram addresses came from the paid contact button and are provably absent from the bio.**

**THE INSTAGRAM PROFILE CALL IS DEFERRED TO SURVIVORS AND MUST NEVER BE REMOVED.** Removing it
costs roughly half the addresses on the platform. **Nothing in this round removed it**, and a test
arm fails if either module ever learns `skip_profile` / `enrich_profile` / `user_by_username` /
`profile_call`.

**What the free `/embed/` route DOES recover** (the fix in §6), on 30 frozen embed bodies:
followers **0/30 -> 30/30 [88.65, 100]**, post count **0/30 -> 30/30**, spread 28…131,849 across
30 distinct values. **It buys a size band, not a bio and not an address.**

⚠️ **"EXACT" WAS WITHDRAWN BEFORE IT COULD BE PUBLISHED.** The free follower count matches the
paid one on **1 of 10 accounts [1.79, 40.42]** — deltas +1, 0, -29, -8, -1, -1, -13, -6, -2, -8,
**median 0.238%, max 0.952%.** Unbucketed, but a **cached snapshot, not the live number.** Good
enough for a size band; wrong for anything exact.

**Structure — four denominators that are not the same number.** One `/top` call returned **9
sections, 33 top-level media slots, 0 carousel children**, and the medias arrive through **three
different containers**: `medias[]` 24, `fill_items[]` 4, `one_by_two_item.clips.items[]` 5. Those
33 slots deduplicate to **28 distinct `media.pk`** and **27 authors**. `/recent` is the case that
breaks a naive count: **8 sections, 24 top-level medias, 57 carousel children = 81 including
children, and zero video.** ⚠️ **A "biggest list" heuristic once read 9 SECTIONS as 9 MEDIAS
on this exact surface** — which is why the count is stated four ways rather than one.

**Signed-URL expiry: 474 of 475 URLs carry `oe` (99.79%)** — min 32.06 h, p05 32.92 h, **median
105.62 h**, p95 107.85 h, **max 108.00 h**. ⚠️ **The max agrees exactly with the earlier
round's 108 h; the median does not (105.6 against 34.8), nor does p05 (32.9 against 13.2). Both are
named rather than averaged.** They agree on what matters: **one to four and a half days, not "fetch
now or never"** — a run-time fetch is safe, a retained URL is not.

### 4e. The picture — KEEP the payload sheet, do NOT wire it

**Decision: keep, do not wire. $0.00 spent, entirely offline.**

**The paired score on his marks was not run, so a new picture may not go on the live judging
path.** That is the constraint, and it was not met. It was not deleted either, and that got
*stronger* during the round: another agent wired the `/embed/` owner block into
`payload_sheet.py:158-181` (followers and post count **30/30 free**), so deleting it now would
also delete a just-measured free-facts reader — **and it is `ig_embed`'s only production
importer.**

**What was removed is the limbo**, which was the actual instruction. `tests/test_bl1525_payload_sheet_and_hero.py`
— 5 tests, `raise` not `assert`, green under `python -O`, **discovered by `tests/run_all.py`**
(the real runner; `unittest discover` lies here). Mutation-proved on **both arms** with the
restores **verified by md5** and `__pycache__` busted between arms, leaving no residue in
`free_judge.py` or `frame_text.py`.

**THE 1.4-SECOND RULE: 1 of 2 page-judge text extractors honours it.**

| site | honours `HERO_T_DEFAULT = 1.4` |
|---|---|
| `frame_text.py:482` | **yes** |
| `video_strip.py:217` | **NO** — `dur/12` at `scaled:6` = **0.417 s on a 5 s clip** |

⚠️ **But the violation is in DEAD CODE** — `video_strip`'s only production importer takes *the
constant only* — so it is a trap for whoever wires the hero next, not a live defect. **The irony
is worth recording: `HERO_T_DEFAULT` is declared 159 lines BELOW `frame_times()` in that same
file and is never read by it.** Frame zero scores 79.2% text readability against 98.4% two
seconds in, which is why the rule exists.

⚠️ **The site count was wrong first, and LOCAL when it claimed to be GENERAL.** The initial
detector walked `ast.Call` arguments only and missed `video_strip.py:217`, where the frame list is
an `ast.Assign` (`argv = [...]`). **8 sites became 10** on the rerun, which carries positive
controls. This is the "count the sites" failure reproduced inside the instrument built to count
them.

**THE TILE COUNT, reproduced on decoded PIXELS rather than on a filename:** a 585×760 sheet
arrives as **195×346 — 84.8% of its area gone — cutting through the 416 px hero at x = 195.**
`tiles=1` returns the sheet whole. Now pinned by a mutation-proved test. **And `hero_geometry(n_small=3)`
— the operator's exact "one big, three small" ask — puts the smalls at 139 px, below the 155 px
floor**; consistent with their motion job, but it should be said out loud rather than discovered
later.

⚠️ **THE FREE SPRITE SHEET: CONFIRMED USELESS FOR TEXT, AND I RELAYED A WRONG FIGURE.**
`image_versions2.scrubber_spritesheet_info_candidates.default` is present on 33/33 Instagram media
— a 1500×518 sheet of up to 105 video frames, free, with **zero readers**. I passed it to the
picture agent as "~100×74 tiles". Measured properly at **n = 1179**: `thumbnail_width` is
**100 px on 1179 of 1179 = 100.0%**, a constant, and the modal tile is **100×176** — the 100×74 I
quoted is **5 of 1179 = 0.42%**, an outlier I relayed without its denominator. `grid_b64` **never
upscales**, so 100 px is what the model receives: **below the 155 px floor and 5.7% of the hero's
area.** Sending the sprite whole is worse, because 1500 px downscales to 760 and halves every
tile. **It is excellent free coverage for pacing and effects and it cannot carry text.** Prior art
`scratch/bl1443_sprite_census.json` already had it at 90.3% with zero readers; it still has zero.
**On TikTok: ABSENT, not zero — not measured.**

**THE WATERMARK: a measured zero WITH a positive control.** `play_url_of` ranks `download_addr`
— the render that **burns the handle onto every frame**, which would print the answer key into the
picture — **second, ahead of `playAddr`**. That is a latent hazard. On 80 stored video objects it
selected it **0 times (0/80, Wilson upper 4.6%)**, and `download_addr` was **present on 68 of those
80**, so the zero is the ranking's and not the sample's.

⚠️ **DEFECT NAMED AND LEFT — A REFUSAL LAUNDERED INTO A MEASUREMENT, ON THE PLATFORM WHERE A
REJECTION IS FINAL.** There is **no decode probe**. An undecodable file carrying a valid `ftyp`
header returns `frames_supplied = 0` with `reason = "no text detected on any frame"` — which is
false — and **`tiktok_finder.py:1477` collapses it via `or ""` into "we read it, and there was no
text"**, three lines beneath its own docstring promising it does not do that. **`meme_finder.py:4166`
and `parallel_judge.py:147` both get this right; only TikTok does not — and on TikTok a
picture-judge rejection is FINAL, so a wrong rejection there compounds forever.** It was not
fixed: it changes what the judge sees and no paired score exists to license it. Recall that 30 of
260 sampled videos do not decode and **28 of those 30 carry a valid header**, so a header check
cannot stand in for a decode probe.

### 4f. The three free fixes — all shipped, and the address count was wrong by 100x

**$0.00 spent. All GENERAL. Ports re-checked before each of 7 writes under `clippershq/`; nothing
listening; no process killed.**

**1 — Speech now runs BELOW the judge.** `speech_needed` at `meme_finder.py:5622-5665`, both
`attach_speech` call sites patched (`:7918-7961`, `:8106-8139`). **`attach_speech` has exactly 2
production sites — 0 in `tiktok_finder`, which never passes `speech_fracs` — and that count is
pinned by AST**, not asserted. A survivor is measured and then **re-judged** (`judge_page` is
pure), so the 61 pages only `dialogue` could reject **still reject.** ⚠️ **`speech_needed`
FAILS OPEN — deliberately the opposite of `profile_deferrable`** — because a wrong *measurement*
defer moves a verdict, while a wrong *purchase* defer only costs a call. **Named cost preserved:**
a fourth state `"not-reached"`, never `"unmeasured"`, rendering as *"not measured — already
rejected (Views too low), so we never listened."*

**2 — Why the profile deferral had never run: NOTHING WAS WRONG WITH IT.** Not unreachable, not
flag-gated — called at `meme_finder.py:7978`, reachable from both the serial (`:8577`) and pool
(`:8594`) lanes. **No meme run has happened since it was committed**: commit at 13:30:53, newest
funnel artefact 13.3 hours *earlier*, and that provenance carries no `profile_deferred*` key at
all. **What was missing was the protection — zero test references repo-wide**, the "a proof is an
event, a protection is an artefact" failure. Now pinned by AST with a positive control and a
dominance check. ⚠️ **Driven offline today it defers 29 of 61 = 47.54% [35.53, 59.84]; the
brief's 828 of 2,029 = 40.8% is the earlier round's corpus. Both named, neither averaged, and the
second is NOT VERIFIED here.**

**3 — The wall labelling, and it was never only a measurement bug.** `page_capture.py:619-676`,
**4 of 4 branches**. Reproduced independently over 3,359 records: `login_wall` records with
tiles > 0 are **257 of 310 = 82.9% [78.3, 86.7]** — **the real wall count is 53, not 310, a 5.85x
inflation of every wall statistic in this project.** Positive control: `private` 0/386 and
`unknown` 0/145 are correctly gated. `not_found` and `age_gate` are **ABSENT from this corpus, not
zero.**

⚠️ **AND IT COST MONEY, WHICH NOBODY HAD NOTICED.** `_paid_grid_needed` (`:898-901`) reads
that label **in both directions** and is called at `:809` **with no tiles precondition** — so
**257 pages that already had a grid were ordering a PAID grid they did not need**, which then
overwrote the tiles and the picture they already had.

⚠️ **4 — THE 102 STRANDED ADDRESSES WERE ONE ADDRESS. MY OWN FIGURE, WRONG BY TWO ORDERS OF
MAGNITUDE.** BL-1521 reported "102 rows stranded" from a counter reading `master_offered: 102`, and
this round's brief repeated it as "102 real addresses, which is his primary goal". Measured
properly: **102 offered = 101 distinct = 100 already present in master. Exactly ONE address was
lost.** Master was byte-identical to the failed run's own backup, and the temp file was master
**plus one row, with zero positional differences across all 72,962 rows.** **I read a counter named
`offered` and published it as a loss without ever diffing the two files.**

**It is recovered.** Installed under the file lock with the sha re-verified *under* the lock:
**72,962 -> 72,963 rows, every prior row hashing identically AT ITS OWN INDEX**, and
offered-addresses-missing **1 -> 0**. No address was printed anywhere.

**The retry ships at three layers, and the site count is the point:** an opt-in longer budget in
`atomic_io.py:75-135` (**default unchanged**), `crossdedup.install_pending_master` at `:437-546`
called at `:576` — **one site covering all 8 funnels, where a retry in `meme_finder` alone would
have been 1 of 8** — and both wrapper handlers. **Extra hazard found on the way:** four other
modules write the same `<master>.tmp` without this lock, so a 120-second staleness window and a
no-op short circuit were added.

**Protection:** `tests/test_bl1525_speech_wall_and_master.py` — **47 checks, green, and green under
`python -O`; every check is a `raise`, enforced by an AST scan of the test's own source.**
**Mutation harness: 18 of 18 arms RED, 0 survived, restore sha256-verified per arm.**

### 4g. The reserved question — the cheapest path from a hashtag to an ADDRESS

**$0.00 spent; the whole answer came off disk.**

**Within clipper supply, the TikTok hashtag route is the cheapest path on record and has no
competitor in this dataset: $0.00326 per address, MEASURED** — 5.7-9.1x cheaper than the Instagram
hashtag route measured **in the same window, by the same campaign, on the same days.** That window
contains only two campaigns in the entire ledger, so the attribution is not a guess: TikTok side
$0.0978 -> 30 addresses; Instagram side $1.0458 -> 56.

**You never pay for the address on that route: 2,641 of 2,757 = 95.79% [94.98, 96.48]** of
addresses stamped `tt:hashtag:*` are **verbatim substrings of the bio the free call already
returned.**

**Lifetime cost per address — three denominators, all named, none averaged:**

| | denominator | n | $/address |
|---|---|---:|---|
| **A — attributable** | distinct, ledger era | 9,881 | **$0.006459** |
| A as first published | rows, ledger era | 10,164 | $0.006279 — **WITHDRAWN** |
| **B — lifetime all-in** | distinct, all time | 12,682 | **$0.005032** |
| **C — usable** | ledger era, role addresses removed | 9,132 | **$0.006988** |

I re-derived B independently at **$0.005047**, agreeing to 0.3%. The two instruments disagreed by
19.6% until the denominators were named: **the window is deliberate — no ledger exists before
2026-07-11 in `spend.json` or in any of its 28 backups** — while the rows-versus-distinct
difference (283 duplicates, 2.86%) was **accidental, ran in the agent's own favour, and was
withdrawn.** **Both files are being appended by a live process, so neither figure should be quoted
past four significant figures.** C is new: **857 ledger-era addresses are role addresses**
(`info@`, `contact@`, `booking@`).

⚠️ **A HEADLINE WAS WITHDRAWN AS A CATEGORY ERROR, AND I HAD ALREADY REPEATED IT ONCE.** The
finding "Spotify is 2.7x cheaper per address than the best hashtag route" is **wrong and is
retracted.** `lead_kind` on address-bearing rows: **Spotify -> client 7,835/7,835 (100%); TikTok
hashtag -> clipper 2,757/2,757 (100%). Zero overlap.** Spotify produces artists to sell *to*;
hashtags produce the clippers. **Spotify cannot produce a clipper at any price**, so the two were
never on one ranking. They also sit at different points on the supply curve — Spotify's $0.001211
is a lifetime over a fresh corpus, the hashtag's $0.00326 is *marginal* after 50,041 pages were
banked. **At a virgin corpus the hashtag route is $0.000471, 2.6x cheaper than Spotify, and the
direction flips.**

⚠️ **THE DENOMINATOR NOBODY HAD LOOKED AT.** Of 10,164 ledger-era address rows, **8,719 are
client, 1,291 meme_page, and only 120 are clipper.** Every "cost per address" this project has ever
quoted — mine included — is **overwhelmingly the price of a CLIENT address**, not of the clippers
the funnel exists to find.

**The separation the brief asked for, and it is not followers.** Follower count predicts whether an
address **publishes** (0.84% -> 47.62%, n = 53,327) but runs *opposite* to what he wants: **his
6-10 scored pages carry an address 3.0% [1.03, 8.45] of the time; his 1-5 scored pages 84.6%
[57.8, 95.7]** — the pages he rejects are the ones that publish an address. **The separator is the
TAG.** Out-of-sample across 3 seeds: top-100 tags **12.9-13.5%** against bottom-100 **2.4-2.8%** —
a stable **2.4x lift** that **survives inside every follower band** (2.44% vs 0.27% under 1,000
followers), so it is **not a size proxy** and it never touches page size.

⚠️ **AND ITS LIMIT, STATED BY ITS OWN AUTHOR: 0 of his 311 scored handles came from a
`tt:hashtag` row.** The tag tiers are validated for **whether an address publishes** and are
**entirely unvalidated for his taste.**

---

## 5. What was refused

* **Wiring a new picture into the judging path.** `payload_sheet.py` is kept and deliberately not
  wired: **no paired score on his marks exists to license it**, and a new picture is a judging
  change. The limbo was removed with a test instead.
* **Fixing `tiktok_finder.py:1477`**, which turns an undecodable video into "we read it and there
  was no text". It changes what the judge sees, and **on TikTok a picture-judge rejection is
  FINAL.** Named and left.
* **Shipping `aweme_type` as a photo gate.** It kills **6 of 14 wanted pages = 42.86%
  [21.38, 67.41]**, including two he scored 9, **and the direction is inverted** — photo posts are
  more common on pages he wants. It is also structurally absent from the hashtag route.
* **Removing the Instagram profile call.** It is the sole source of the contact email; removing it
  costs roughly half the addresses on that platform.
* **Quoting a follower floor.** Measured and refused: followers predict whether an address
  *publishes*, not whether he wants the page — **his 6-10 scored pages carry an address 3.0%
  [1.03, 8.45] of the time against 84.6% [57.8, 95.7] for his 1-5 scored pages.**
* **A confident kill rate for TikTok edits.** He graded 30 pages there and rejected exactly one:
  **the negative class is n = 1**, so no such rate is available to anyone.
* **Averaging any two disagreeing instruments.** Four pairs are named separately instead: the
  deferral reach (47.54% here vs 40.8% on the earlier corpus), the URL expiry median (105.6 h vs
  34.8 h, though the max agrees exactly at 108), the cost per address (three denominators), and the
  sprite tile size.

---

## 6. What I got wrong

### ⚠️ My own BL-1521 headline was wrong, and this brief inherited it

**BL-1521 ranked `ig_discovery.py:276-283` FIRST**, calling it the defect that "forces the
Instagram paid profile call" and saying it "unlocks items 2 and 3". This round's brief repeated
that framing. **It is wrong.**

The line does read five fields from an object that has none of them. **But the fix is not "read
them from the right key", because there is no right key in that payload.** Three independent
instruments now agree:

1. **The live dump.** On `/v2/hashtag/medias/top`, `biography`, follower count, contact email and
   `media_count` are **ABSENT**; only `is_verified` is present (33/33).
2. **A value-search, not a name-search.** 737 distinct key names across the 30 largest hashtag
   payloads: **no key anywhere holds bio-shaped free text or a follower-shaped integer on any dict
   carrying a `username`** — not `user` (exactly 30 thin keys), not `caption.user` (present
   1,717/1,719, the same 30 keys), not `owner`, not the envelope.
3. ⚠️ **The repository already said so and I did not read it.** `clippershq/main.py:2171-2189` is
   an epitaph for a function deleted in BL-900: *"it gated on `followers_from_feed`, and the real
   IG hashtag payload carries no follower field at all — **0 of 143 authors across five saved
   payloads**."*

**I named a mechanism from the shape of the code and never asked whether the value existed in the
payload at all** — the same failure I had catalogued twice in other rounds' work in the very
report that got it wrong. The check that would have caught it costs one search and I did not run
it.

**What the free route actually is:** the `/embed/` `owner` block — a body `payload_sheet.py`
**already fetches** and `ig_embed.parse()` **was discarding**. Measured on 30 frozen embed bodies:
followers **0/30 → 30/30 [88.65, 100]**, post count **0/30 → 30/30**. **But biography is 0/30 free
against 10/10 paid, and contact email 0/30 against 3/10.** It buys a size band, not a bio and not
an address.

### The 102 stranded addresses were ONE address

BL-1521 reported "102 rows stranded" and this brief repeated it as "102 real addresses, which is
his primary goal". Measured: **102 offered = 101 distinct = 100 already in master. Exactly one
address was lost**, and it is now recovered. **I read a counter named `offered` and published it as
a loss without diffing the two files** — the same shape as reading a field name and never checking
whether the value exists.

### I mislabelled all 39 fields in my own author table

Building §4b I read the AST reader verdict as a flag when it is **four booleans**, and printed
**UNREAD for every author field — including `author.signature`, which production demonstrably
reads.** I caught it only because that single row contradicted code I already knew. The published
table is the corrected run and now carries the control that would have caught it in one line.

### I relayed a tile size without its denominator

I passed the free sprite sheet to the picture agent as "~100x74 tiles". It is **100x176 modal**;
the 100x74 I quoted is **5 of 1,179 = 0.42%**. The conclusion happened to survive — 100 px is below
the readable floor either way — but I handed on an outlier as if it were typical.

### I repeated a withdrawn headline to the operator before it was checked

I relayed "Spotify is 2.7x cheaper per address than the best hashtag route" as a finding. Asked
whether it was like-for-like, its author withdrew it as a **category error**: Spotify produces
client leads 7,835/7,835, hashtags produce clippers 2,757/2,757, **zero overlap.** I should have
asked before repeating it, not after.

### And two instruments of mine failed before they worked

My last-post value search first returned **NOT ESTABLISHED** because it counted the server clock,
our own `fetched_at`, and signed-URL expiries as candidate post dates. Then it printed
**CONFIRMED** on **n = 3**, which is an overclaim; the verdict line now scales with its own
denominator. Neither error changed the answer, and both were mine.

---

---

## 7. Money and safety

**Spend: $0.1459 of $1.50**, from each run's own counter at the wrapper, never a ledger delta.

**The cap was proven to bind before the first call** by driving `harvest_run.Budget.reserve`, with
a positive control so a refusal means something: a $1.00 cap **ALLOWS**, an exhausted cap refuses,
a **$0.00 cap refuses the FIRST call**, a negative cap refuses, every refusal is a raised
`BudgetExceeded` rather than a return value, and **the meter does not advance on a refusal.**
$1.50 stops at 2,171 calls.

**Backups** at round start under a path built from one round constant, sha256-verified, with
**four controls that fired**: an identical copy verifies, a one-byte flip is caught, and — the new
one this round required — **a planted deletion that leaves the natural key set IDENTICAL is
invisible to a key-set check and IS caught by an index-qualified row hash.** Without that last
control the row-hash check would have been decoration. 8 files: `config.json`, `spend.json`
(29,031 rows in the `runs` LIST — a dict-only helper reads it as near-zero), `master_leads.csv`,
and all five seen stores (2,193 / 6,196 / 2,518 / 1,925 / 4,146), **body found by shape.**

**No dashboard was listening** in the dashboard port range at round start, read from the **listening-port
table** — never a command-line grep, which once matched its own command line, and never
`dashboard/.running.json`, a stale marker since 30 August. Re-checked before every write under
`clippershq/`. **No Python process was killed.**

### The test verdict, with its denominator

**Targeted runs over every area this round touched — `bl1525`, `speech`, `wall`, `capture`,
`crossdedup`, `embed`, `profile`: 16 suites, ALL PASS, zero red.**

**The full runner is `tests/run_all.py`** (`unittest discover` under-reports here). It runs **458
suites** and was still running when this report was published: **189 suites had passed and 14 were
red.** ⚠️ **That is a PARTIAL run and it is named as one rather than quoted as a total.**

⚠️ **THIRTEEN OF THE FOURTEEN WERE ALREADY RED BEFORE THIS ROUND, AND EACH WAS PROVED BY REMOVAL
RATHER THAN ASSERTED** — run against a clean worktree detached at the pre-round commit, not argued
from a diff:

| suite | status | how it was established |
|---|---|---|
| `test_atomic_io` | pre-existing | fails at the pre-round commit; cause `proxy_pool.py:290`, an unguarded `os.replace` |
| `test_bl1300_judge_first` | pre-existing | fails at the pre-round commit (config-independent) |
| `test_bl1307_veto_refused` | pre-existing | **passes** at the pre-round commit; tripped by `scratch/bl1441_ast_sink_tests.json`, an **untracked file dated 30 August** |
| `test_bl1308_refuted_brief` | pre-existing | the same untracked file |
| `test_bl1327_lane_pool` | pre-existing | fails identically at the pre-round commit |
| `test_bl1350_gates` | pre-existing | asserts on `stale_days`, a config key **this round never touches** — proved by diff, because the clean-worktree method is UNSOUND here (see below) |
| `test_bl1352_evidence_before_floor` | pre-existing | fails at the pre-round commit, differing only in the line number it reports |
| `test_bl1359_ig_cost_fixes` | pre-existing | fails at the pre-round commit |
| `test_bl1389_no_caller` | pre-existing | fails at the pre-round commit |
| `test_bl1400_ordering_and_third_state` | pre-existing | fails at the pre-round commit |
| `test_bl1407_free_first` | pre-existing | fails at the pre-round commit |
| `test_bl1444_board_and_sheets` | pre-existing | fails at the pre-round commit |
| `test_bl1516_paid_call_ordering` | expected-by-design | **its own census says so** — 1 expected-by-design, 0 unexpected, 10 expected-red now green. Not independently re-proved by me. |
| **`test_bl1348_gates`** | ⚠️ **CAUSED BY THIS ROUND — and fixed** | see below |

⚠️ **THE CLEAN-WORKTREE METHOD HAS A HOLE AND I FOUND IT THE HARD WAY.** `config.json` is
**gitignored**, so a worktree checked out at any commit has none — and every suite that reads it
errors there for a reason that has nothing to do with the change under test. One suite appeared to
"fail at HEAD with 8 errors" purely because of that. **A proof by removal is only valid for a test
that does not read an untracked file**, and where it is not, a different argument is required —
which is why `test_bl1350_gates` above is settled by diff instead.

⚠️ **THE ONE THIS ROUND BROKE, AND WHY IT WAS WIDENED RATHER THAN RELAXED.**
`test_bl1348_gates` encodes a real invariant: **every walked tag must be declared either proven or
a bet**, because "an unlabelled bet gets quoted as a finding". This round supplied eight
`<topic>edit` tags and correctly declared them **bets** — they have been walked once and have no
result against his marks. The check then failed, not because a tag was undeclared but because it
compared **only the meme lane** against the declared set, and BL-1326 had split the walk into two
lanes. It now compares **the union of both lanes**, so an undeclared tag in *either* lane fails and
so does a declared tag nothing walks. **Restricting the right-hand side instead would have been the
loosening** — and would have let the edits lane grow unlabelled, which is the exact failure its
docstring names. **Mutation-proved in three directions**: red on an undeclared edit tag, red on a
declared tag nothing walks, red on an undeclared meme tag (the original teeth), green restored.

⚠️ **AND MY FIRST MUTATION HARNESS FOR IT REPORTED ALL FOUR ARMS GREEN**, because `setUp` re-reads
the config and discarded the block I had assigned. **A harness that cannot fail proves the
opposite of what it appears to prove**; patching the function the test actually calls fixed it.

Paths in this report are relative to the repository root under `%USERPROFILE%`.

---

## 8. What he should do next, ranked by ADDRESSES PER DOLLAR

**Ranked by addresses per dollar, not pages per dollar** — his goal, and the axis no report in this
project had used before.

| # | action | worth | basis |
|---|---|---|---|
| 1 | **Drop the INSTAGRAM half of hashtag discovery, not hashtags.** Measured in one window, same campaign, same days: the Instagram side cost **$1.0458 for 56 addresses** against TikTok's **$0.0978 for 30** — **5.7-9.1x more for the same product** | the largest single lever on record | MEASURED, in-window |
| 2 | **Keep the TikTok profile purchase OFF** (shipped this round) | **52 paid calls → 0 addresses [0.00, 6.88]**; costs only `bioLink`, worth 1 address in 60 | MEASURED |
| 3 | **Select tags by tier.** Top-100 tags carry an address **12.9-13.5%** of the time against **2.4-2.8%** for bottom-100 — a **2.4x lift** that survives inside every follower band, so it is not a size proxy | 2.4x on address yield, at zero cost — it is only term selection | MEASURED out-of-sample, 3 seeds ⚠️ **but 0 of his 311 scored handles came from a `tt:hashtag` row: validated for whether an address PUBLISHES, entirely unvalidated for his TASTE** |
| 4 | **Fix the paid-grid ordering exposed by the wall bug** (shipped): **257 pages that already had a picture were ordering a paid grid**, which then overwrote it | direct vendor spend on 257 pages, plus the picture they destroyed | MEASURED |
| 5 | **Let `profile_deferrable` actually run** — it has never executed, and this round gave it the test it lacked | defers **47.54% [35.53, 59.84]** of Instagram profile purchases **without losing an address**, because it defers rather than removes | MEASURED |
| 6 | **Run TikTok edits mode.** `tiktok_finder.mode` is `"memes"` — a config value, not a defect. Its tags and his search terms now work | its four historic runs are the only cost target this project has met | MEASURED |
| 7 | **Move speech below the judge** (shipped) | **2.12 h per 1,000 delivered**, $0.00 of vendor money | MEASURED |
| 8 | **Decide `tiktok_finder.py:1477`** — an undecodable video currently reads as "no text found" on the platform where a rejection is FINAL | no dollars; **wrong rejections that compound forever** | MEASURED, left unfixed |
| 9 | **Mine the free unread fields** — burned-in captions (which the OCR gate currently pays to derive), original-vs-licensed audio, `videoSuggestWordsList` | unpriced | MEASURED |

⚠️ **NOT RANKED, DELIBERATELY.** Wiring the payload sheet, and any use of the free 105-frame sprite
for text — the sprite's 100 px tiles are **below the 155 px readable floor and 5.7% of the hero's
area**, so it is free coverage for pacing and cannot carry text. Neither has a paired score, and
this project has twice shipped a picture change without one.
