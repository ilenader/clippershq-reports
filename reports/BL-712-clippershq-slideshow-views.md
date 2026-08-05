# BL-712 — Are photo slideshow and carousel clips getting their views counted? (READ ONLY)

Date 2026-08-05. Base origin/main `8b5aaf57`. Branch `checkpoint/BL-712`. Isolated worktree `C:/b712`.
READ ONLY: no code, config, data or money change; NO Apify actor run; the 11 BL-678 guards untouched.
DB now() at first query `2026-08-05 10:02:57.579208+00`. Clipper handles redacted (user hashes only).

## PROBES DISCLOSED (21 vendor requests, cap ~20, one over and stated)

An initial run made **0** vendor calls (tsx did not load `.env.local`, both providers bailed on a missing key).
The keyed runs made: **HikerAPI 10 calls** (prepaid `/v2/media/info/by/code`; 8×200, 2×404) and **LamaTok 11
requests** of which **4 were billed 200s** (`/v1/media/by/id`); the 7 others were 6 timeouts plus 1 HTTP 500
on `/v1/media/by/url`, which this file's own comment states are not billed. Plus **3 free redirect resolutions**
to tiktok.com (not a vendor). All per-post calls, never profile scans, so ONE CALL PER PROFILE is not engaged.
Every response was id-matched, never row-matched (BL-550 trap).

## PART 1 — MEASURED FROM THE DATABASE

**How slideshows and carousels were identified, and with what confidence.**
• TikTok, HIGH confidence, canonical form: `www.tiktok.com/<user>/photo/<id>` → **5 clips, ALL isDeleted=true,
  all REJECTED, all earnings $0, lastCheckedAt NULL, one submit-time ClipStat each.** Zero live ones.
• TikTok short links, **the gap**: 862 live clips are `vm.` / `vt.tiktok.com`, whose media type is invisible in
  the URL. 8 of them are APPROVED with **zero ClipStat rows ever**; all 3 sampled resolved to `/photo/` URLs, so
  these are slideshows the URL could not reveal. Confidence that these 8 are slideshows: HIGH for the 3 probed,
  MEDIUM for the other 5 (same campaign, same cohort, identical symptom).
• Instagram, LOW to MEDIUM confidence: the only DB-visible proxy is `/p/` (69 clips, 64 live). `/p/` is shared by
  single image, single video and carousel, and nothing in the schema stores a media type. `?img_index=` is 100%
  specific but appears on only 1 live clip. Live probing is the only way to be sure; 3 were probed and all 3 were
  carousels. BL-610 characterised 3 of 63 `/p/` as carousels, so the carousel share of `/p/` is small.
• 4,884 clips total; 2,094 IG reel, 1,396 YouTube, 1,291 TikTok canonical, 862 TikTok short link, 69 IG `/p/`.

**View-update behaviour, 7-day window, APPROVED + tracking active + videoUnavailable=false:**

| shape | age band | n | polled 7d | views GREW | frozen | earnings |
| --- | --- | --- | --- | --- | --- | --- |
| IG `/p/` | <14d | 5 | 0 | **0** | 0 | $0.00 |
| IG `/p/` | 14 to 45d | 11 | 7 | **0** | 11 | $1.69 |
| IG `/p/` | >45d | 32 | 3 | 0 | 32 | $91.66 |
| IG reel (CONTROL) | <14d | 357 | 357 | **128** | 1 | $1,177.14 |
| IG reel (CONTROL) | 14 to 45d | 409 | 367 | **249** | 160 | $542.35 |
| IG reel (CONTROL) | >45d | 250 | 24 | 9 | 241 | $741.84 |
| TikTok (CONTROL) | <14d | 141 | 133 | **47** | 2 | $714.63 |
| TikTok (CONTROL) | 14 to 45d | 409 | 245 | **154** | 255 | $1,684.16 |

Old clips freezing is NORMAL (reels >45d: 241 of 250 frozen). The decisive number is the **zero-ClipStat** rate:
IG `/p/` **5 of 53** (9.4%), TikTok **9 of 1,017** (0.9%), IG reel **4 of 1,695** (0.24%), YouTube **0 of 1,117**.

**The frozen cohort is one campaign.** 13 APPROVED clips (5 IG `/p/` + 8 TikTok short link), created 2026-07-29 to
07-31, across 3 clippers, ALL in campaign `cms4nt3d50keg0pn2637e2daz` ("SomeSome", ACTIVE, CPM $2, minViews 1,000).
Every one: `cadenceReason=INFRA_DEFER`, `checkIntervalMin=360`, being polled (lastCheckedAt today,
e.g. `2026-08-05 10:02:58.169`), **0 ClipStat rows ever written**, earnings $0.00. The same campaign's 4 reel and
YouTube clips DO have stats (up to 453 views) — a perfect within-campaign control.

**Money.** Slideshow and carousel clips carry **$0.00**, accruing or frozen. All 64 live IG `/p/` clips together
hold $95.21 (overwhelmingly ordinary single-video `/p/` posts, not carousels); the 862 TikTok short links hold
$3,152.92 (overwhelmingly ordinary videos); platform-wide approved earnings are $11,161.91. The three TikTok
slideshows probed return play counts of **151, 0 and 1** — all below the campaign's 1,000-view minimum, so even
if counted correctly today they would still earn **$0.00**. This is a real defect with, at this moment, no money on it.

## PART 2 — THE SILENT FAILURE MODES, CHECKED SPECIFICALLY

• **Writing NULL every tick:** YES, 13 clips. Worse than "views never grow" — because no baseline stat was ever
  written (BL-605 correctly skips the first snapshot on a null resolve), these clips have **no ClipStat row at
  all**, so their view count is not frozen at a stale value, it does not exist.
• **QUARANTINED by BL-610:** the 3 IG `/p/` probed returned `verdict=quarantine`, `useResult=false`,
  `reason="carousel uncountable (carousel_image_only, views=null) — quarantine, skip Apify"`. Quarantine is
  **not permanent state** — nothing is persisted, and the clip is re-probed every tick. It is permanently
  unresolvable in practice, and each retry bills one prepaid HikerAPI 200 (~20 calls/day for the 5 clips).
• **consecutiveGone strikes:** NO. All 13 have `consecutiveGone=0`. Verified in code and live: a slideshow's
  `by/url` returns HTTP 500 `AppException` (`lamatok.ts:260-265` requires 404 AND `MediaNotFound` for "gone")
  and a quarantined carousel is deliberately NOT added to `igGoneUrls` (`apify.ts:1618-1627`). BL-604's rule
  still holds with Apify dead: `gone-counter.ts` never increments on a transient 5xx. `retire-dead-clips.ts:74`
  still restricts candidates to `clipUrl contains "instagram"` and still demands a fresh HTTP 404 at `:111`.
• **Wrongly stamped videoUnavailable:** **NO — and this was checked, not assumed.** 11 IG `/p/` clips carry the
  flag; 5 are APPROVED holding $1.86. The two carrying real money were probed live and BOTH returned HikerAPI
  **404 MediaNotFound** — genuinely deleted, correctly stamped. No live post is wrongly frozen, so no clipper's
  withdrawal is wrongly blocked and no balance is wrongly hidden. Note for the record: 9 of the 11 share
  identical microsecond `videoUnavailableSince` values (`2026-07-18 19:09:41.778551` / `19:10:11.545056`),
  the signature of a bulk backfill rather than per-clip tracking; the 2 spot-checked were correct.

## PART 3 — LIVE PROBES THROUGH THE PRODUCTION PATH

**Instagram, `fetchHikerInstagramByUrl` then `tryHikerForInstagram` (the real overlay), 3 posts, ids matched:**

| shortcode | endpoint | HTTP | classification | children | video children | views | production verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DbdUxIVjY00 | HikerAPI `/v2/media/info/by/code` | 200 | carousel_image_only | 4 | 0 | null | quarantine |
| Dbcv1swDdOP | HikerAPI `/v2/media/info/by/code` | 200 | carousel_image_only | 4 | 0 | null | quarantine |
| DbX7cerjU1E | HikerAPI `/v2/media/info/by/code` | 200 | carousel_image_only | 4 | 0 | null | quarantine |

Exact id match proven on DbX7cerjU1E: `media_or_ad.code === "DbX7cerjU1E"`, `pk=3951888639873339000`,
`media_type=8`, 4 children, 0 video children, `play_count=null`, `view_count=null`. Storage agrees: no stat.

**TikTok, `fetchLamatokTiktokByUrl` (the real production reader), 3 posts, ids matched:**

| clip | short link resolves to | production `by/url` | `by/id` (shadow path) |
| --- | --- | --- | --- |
| cms9j26h… | `/@…/photo/7668823960754113799` | timeout ×2 → verdict transient, views null | **200, imagePost=true, playCount 151** |
| cms8y6ev… | `/@…/photo/7668673801437170977` | timeout ×2 → verdict transient, views null | **200, imagePost=true, playCount 0** |
| cms5y1dm… | `/@…/photo/7667894322632592672` | timeout ×2 → verdict transient, views null | **200, imagePost=true, playCount 1** |

Control on the canonical form: `by/url` on `…/photo/7667894322632592672` returned **HTTP 500
`{"detail":"Response error","exc_type":"AppException"}`**, verdict "carousel" — BL-604's finding, unchanged.
Every `by/id` response carried the exact id requested. Storage has no stat for any of the three.

**Is the count retrievable TODAY?** TikTok: **YES**, via LamaTok `by/id`, on all 3. Instagram: **NO** for
image-only carousels — the media object exposes no play or view field anywhere, on any endpoint tried.
**The production path uses `by/url`, never `by/id`** (`lamatok.ts:205`); `by/id` exists ONLY as
`shadowProbeSlideshowById`, which logs and returns void (`lamatok.ts:111-137`), and it is only fired when
`urlClass === "photo"` (`lamatok.ts:198`) — which a short link never is. That single detail decides the question.

## PART 4 — WHAT IS ACTUALLY BROKEN

**TikTok slideshows: the code asks the wrong way.** Not "the provider cannot" and not "we discard the answer".
Chain, with lines: `apify.ts:456` calls `fetchLamatokTiktokByUrl(videoUrl)` with the STORED short link →
`lamatok.ts:205` probes `by/url`, which 500s (canonical) or times out (short link) on a slideshow →
`lamatok.ts:260-265` yields "transient" for a short link (urlClass is "unknown", not "photo") →
`apify.ts:508` falls through to the Apify chain → `apify.ts:581` `throw new Error("apify hard off (BL-678)")` →
`tracking.ts:1442` sees `fetchThrew`, `tracking.ts:1481` classes it infra, `tracking.ts:1495-1515` writes
INFRA_DEFER and **no ClipStat**. The correct answer was one call away the whole time.

**A second, upstream defect that let this population exist.** `carousel-config.ts:36-38` matches only
`tiktok.com/<user>/photo/`, and no submit path resolves a short link before the check
(`clipper-submit-core.ts:286`). So the slideshow block that BL-604 relied on is bypassed by any `vm.`/`vt.` link,
which is how 8 live APPROVED TikTok slideshows exist while the flag is still ON.

**Instagram image-only carousels: the provider genuinely cannot.** `hikerapi.ts:537-553` returns
`views: null` when a carousel has zero video children, and the live response confirms there is no count to read.
`hikerapi.ts:835-839` then quarantines it. That is CORRECT behaviour under BL-543, not a bug: an image-only post
has no view metric. **Nothing is broken here and no fix should be manufactured.**

**Instagram mixed carousels: the code asks correctly and would count them.** `hikerapi.ts:809-833` serves a
mixed carousel with a summed count > 0 as a genuine hit. **0 mixed carousels exist in the live population**
(BL-610 measured the same), so this path is currently unexercised, not broken.

## PART 5 — VERDICT AND FIX SPEC

**ONE LINE PER PLATFORM. TikTok: NO, slideshow views are NOT being counted today, and the count IS retrievable
(8 live APPROVED clips affected). Instagram: carousels are not counted, but image-only carousels have no count
to fetch from any endpoint, so this is correct behaviour, not a defect.**

**Money affected: $0.00.** All 13 affected clips hold $0.00, accruing or frozen; the three measured slideshows
sit at 151, 0 and 1 views against a 1,000-view minimum, so correct counting would still pay $0.00 today. The
owner's instinct about the MECHANISM is right on TikTok and wrong on Instagram; the exposure is not yet money.

**FIX (TikTok only), in dependency order:**
1. `lamatok.ts` — resolve a `vm.`/`vt.` short link to its canonical URL before `classifyTiktokUrl`, so
   `urlClass` becomes "photo" and the existing `/photo/` handling applies (`lamatok.ts:191-205`). Vendor cost
   $0 (one free redirect follow, proven above on 3 of 3).
2. `lamatok.ts:205` — for `urlClass === "photo"`, call `by/id` (`lamatok.ts:118`) as the PRIMARY reader instead
   of `by/url`, promoting the shadow to a real return value. Cost: one billed LamaTok 200 per slideshow poll,
   replacing a call that returns nothing. **Blocked on a pricing decision, not on code:** BL-604 proved `by/id`
   is display-rounded (25,700 vs a true 25,835), so promoting it moves stored earnings ~0.3 to 0.9% under the
   true count. Do not flip this silently.
3. `carousel-config.ts:36` plus `clipper-submit-core.ts:286` — decide deliberately whether the short-link
   bypass is closed (block resolves-to-`/photo/`) or left open because step 2 makes slideshows trackable.
   Leaving both as they are is the one option that is definitely wrong.

**What must be proven before any of it ships:** `by/id` id-match on ≥100 slideshow ids with zero row mismatches;
the rounded-versus-exact delta measured either side of the 10k boundary (BL-544/600); and that a live slideshow
returning 500 or a timeout still never increments `consecutiveGone` and never stamps videoUnavailable.
**Rollback:** all three are single-file, behind existing flags; `git revert` the commit, or reset to `pre-BL-712`.
No schema change, no backfill, nothing to undo in the database.

## COULD NOT BE MEASURED

• Whether the other 5 zero-stat TikTok short links are slideshows (3 of 8 probed; the cap stopped further probes).
• Which of the remaining 61 live IG `/p/` clips are carousels — the schema stores no media type and only 1 clip
  carries `?img_index=`. A persisted media-type column would turn this whole audit into one SELECT.
• Whether the 9 bulk-stamped videoUnavailable `/p/` clips are all correct; 2 of 11 were probed and both were.
• No build was run and none is claimed: this round changed one markdown file and cannot affect tsc.
