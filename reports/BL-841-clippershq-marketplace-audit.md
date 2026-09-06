# BL-841: the marketplace, established from the code rather than from the description

**2026-09-06 · DB `now()` = `2026-09-06 10:35:17.436204+00` (first read) to `2026-09-06 10:40:50` (last) · AUDIT ONLY.**
Base `origin/main` @ `7075e6a3`. Branch `checkpoint/BL-841`. Isolated worktree `C:/w841`, a short path, `node_modules` never junctioned, **removed at the end**. **NOTHING WAS CHANGED**: no code, no config, no schema, no data. Nothing created, nothing deleted. Every request a read. Every database read through `scripts/run-select.js`, every timestamp cast `::text` against DB `now()`. Handles redacted; no wallet address read or printed. Five subagents ran in parallel on the money path, the listing and slot logic, the posting verification, the three role views and the prior reports; **their findings are reconciled here, not averaged, and three of them are corrected.**

> ## THE HEADLINE
> **THE MARKETPLACE IS DORMANT AND HAS NEVER CARRIED A SINGLE TRANSACTION.** 0 submissions, 0 posts, 0 creator earnings, 0 platform earnings, 0 marketplace clips, **$0.00 ever moved**. One listing exists, created 2026-07-11 by a **test user**, still `PENDING_APPROVAL` 57 days later, and **zero listings have ever been ACTIVE**. One poster is approved and he is the same test user.
> **SO BL-842 IS THE FIRST REAL TEST, AND THE RISK IS THE OPPOSITE OF WHAT IT WOULD BE ON A LIVE SYSTEM.** Nothing can be corrupted because nothing is there. Everything below is latent.

> **FOUR OF THE OWNER'S PREMISES ARE WRONG, AND EACH ONE MATTERS.**
> **1. The 10 percent is NOT on top of what the owner already takes. It REPLACES it.** `isCpmSplit = !isMarketplaceClip && …` at `tracking.ts:2047` and `review/route.ts:520`, so **no `AgencyEarning` row is ever written for a marketplace clip**. What IS on top is the ordinary 9 percent payout fee, which both parties still pay on withdrawal.
> **2. A SLOT IS NOT A PLATFORM.** It is one platform-post of a **DAILY** quota that resets at midnight UTC. `dailySlotCount Int @default(5)` at `schema.prisma:2634`; the day boundary at `submissions/route.ts:429-430`.
> **3. There is no prior marketplace round to reuse.** 33 BL rounds and roughly 50 F-prefixed rounds built it across 158 commits, and **not one of them has a report**: the reports repo begins at BL-538 and the marketplace's last commit was BL-500 on 2026-07-15.
> **4. BL-840's sandbox tooling does not exist for this project.** `BL-840.md` in the reports repo belongs to a **different project** that shares the BL numbering. There is no BL-840 commit on `main`, no sandbox script, no BACKLOG entry. **PART 7 specifies building the harness, not reusing one.**

---

## PART 1: WHAT EXISTS TODAY

### The surface, enumerated

**14 Prisma models** (`prisma/schema.prisma`): `MarketplacePosterApplication` `:1813`, `MarketplacePosterListing` `:2628`, `MarketplaceListingAccount` `:2716`, `MarketplaceListingFavorite` `:2751`, `MarketplaceSubmission` `:2765`, `MarketplaceClipPost` `:2828`, `MarketplaceRating` `:2848`, `MarketplaceMessage` `:2879`, `MarketplaceChatThread` `:2908`, `MarketplaceChatMessage` `:2924`, `MarketplaceStrike` `:2940`, `MarketplaceVideoHash` `:3012`, `MarketplaceCreatorEarning` `:3036`, `MarketplacePlatformEarning` `:3061`.

**31 API routes** under `src/app/api/marketplace/**` plus 3 admin and 4 cron. **14 pages**, **29 components**, **12 lib files**.

| area | state | evidence |
|---|---|---|
| poster application and owner approval | **COMPLETE** | gate at `listings/route.ts:99`, DB-read not token, fail-closed; OWNER-only CAS flip at `admin/listings/[id]/approve/route.ts:79-88` |
| listing create, edit, pause, pin, delete | **COMPLETE** | PATCH hard-rejects 8 privileged fields at `listings/[id]/route.ts:689-692` |
| slot capacity and the claim race | **COMPLETE** | `SELECT … FOR UPDATE` + Serializable, `submissions/route.ts:559-683` |
| submission state machine | **COMPLETE**, one unguarded write | 6 statuses, every transition CAS-guarded except `marketplace-cascades.ts:262` |
| the 60/30/10 arithmetic | **COMPLETE** | `earnings-calc.ts:629-691`, platform as residual |
| post declaration and per-platform fan-out | **COMPLETE** | `submissions/[id]/post/route.ts`, atomic per URL |
| **proof the posted video is the submitted video** | **DOES NOT EXIST** | `MarketplaceVideoHash` is SHA-256 of the **Drive URL**, `video-hash.ts:12-23`, never read by `/post` |
| **proof the posting account belongs to the poster, at post time** | **DOES NOT EXIST** | the word `username` appears 0 times in the 990-line post route |
| strikes, bans, disputes, decay | **COMPLETE in code**, partly unreachable | see PART 4 |
| chat | **COMPLETE** | scoped three ways, 404 not 403 to a non-participant |
| email and broadcast | **COMPLETE** | 12 senders, no figure in any body; external legs hard off |
| budget and per-creator caps | **COMPLETE** | Y1/Y2 hard-lock `clip-earnings-writer.ts:490-598` (BL-299; BL-627 corrects BL-542 and BL-617, which called them absent) |
| `allowContentReuse` per campaign | **PARTIAL** | owner-set **by SQL only**, no admin UI, `schema.prisma:186` |
| `payoutReductionRatio` on marketplace | **PARTIAL** | extended by F-MARKETPLACE-CAP, but the adjust route still filters `isMarketplaceClip: false` |

### The live population, measured

| table | rows | oldest `::text` | newest `::text` |
|---|---|---|---|
| `marketplace_poster_applications` | **1** (APPROVED) | `2026-05-05 19:55:36.199` | same |
| `marketplace_poster_listings` | **1** (PENDING_APPROVAL, **0 ACTIVE**) | `2026-07-11 15:59:24.403` | same |
| `marketplace_listing_accounts` | **3** | `2026-07-11 15:59:24.456` | same |
| **`marketplace_submissions`** | **0** | null | null |
| **`marketplace_clip_posts`** | **0** | null | null |
| **`marketplace_creator_earnings`** | **0** | null | null |
| **`marketplace_platform_earnings`** | **0** | null | null |
| `marketplace_video_hashes` | **0** | null | null |
| `marketplace_ratings` | **0** | null | null |
| `marketplace_chat_threads` / `_messages` | **0** / **0** | null | null |
| `marketplace_strikes` | **31** | `2026-07-07 17:18:17.235` | `2026-09-05 12:15:42.699` |
| `clips WHERE isMarketplaceClip = true` | **0** | null | null |

**The 31 strikes are not marketplace strikes.** All 31 carry `reason = EXCESSIVE_REJECTIONS`, written by `excessive-rejections.ts:158` from ordinary clip rejections. **Zero `MISSED_POST_DEADLINE`, zero `DISPUTED`, zero `RESOLVED`, zero `OWNER_ISSUED`.** The only marketplace table with rows is being filled by a feature that is not the marketplace.

**Poster population:** `posterStatus` is `APPROVED` on exactly **1** of 1,633 live users, and that user is `isTestUser = true`. **1,632 are `NONE`. Zero `PENDING`, zero `REJECTED`.**

**Visibility.** `isMarketplaceVisibleForUser` (`marketplace-flag.ts:33-40`) shows the marketplace only when `NEXT_PUBLIC_MARKETPLACE_ENABLED === "true"`, or to `role === "OWNER"`, or to a test user. The variable is **commented out** in the local `.env.local` and absent from `.env` and `.env.example`. That is why the owner's dashboard has carried a Marketplace item for months: he is `OWNER` and sees the preview.

> **LIVE OR DORMANT: DORMANT, and it always has been.** Independently measured the same way by BL-542, BL-617, BL-642, BL-714, BL-718, BL-730, BL-758, BL-834 and R-5 across two months. **No report has ever recorded it as live.**

---

## PART 2: THE MONEY

### Where the split lives

| | `file:line` |
|---|---|
| the three constants, ONE declaration each | `earnings-calc.ts:584` `= 0.6`, `:585` `= 0.3`, `:586` `= 0.1` |
| the only arithmetic | `calculateMarketplaceEarnings`, `earnings-calc.ts:629-691` |
| the two writers | `tracking.ts:2099` and `clips/[id]/review/route.ts:526` |
| the rows written | `tracking.ts:2780`, `:2803`; `review/route.ts:777`, `:801`, `:824`, `:839` |
| display-only re-derivation, never persisted | `marketplace-payout-shape.ts:79-127` |

No duplicated literal anywhere; every other site imports the constants.

### What it is applied to, and what shape it is stored in

**Applied to the GROSS clip revenue, before any fee**, after the per-clip cap: `earnings-calc.ts:651-663`.

```
gross        = (views / 1000) * cpm,  capped at maxPayoutPerClip
creatorBase  = round2(gross * 0.6)
posterBase   = round2(gross * 0.3)
platformBase = max(0, round2(round2(gross) - creatorBase - posterBase))
```

**IT IS NOT THE BL-835 SHAPE.** `payout_requests` carries `trainerCutPercent`, `trainerCutAmount`, `trainerRelationshipId` and `trainerEligibleGross` and **no marketplace column at all**, confirmed against the live table. The marketplace split is applied UPSTREAM, at earnings time, into three separate stores:

| party | share | stored in |
|---|---|---|
| clipper (creator) | 60% | `MarketplaceCreatorEarning.amount` (`schema.prisma:3041`) |
| poster | 30% | **`Clip.earnings`** (`schema.prisma:949`), written only through `writeClipEarnings` |
| owner (platform) | 10% | `MarketplacePlatformEarning.amount` (`schema.prisma:3065`) |

**So on a marketplace clip `Clip.earnings` holds the POSTER'S figure, not the clipper's and not the gross.** That single fact is the source of several defects below, and it is why BL-829 had to special-case "the marketplace-swap trap" so a creator's own earnings page did not read the poster's number.

**The trainer cut and the marketplace cut are opposite designs and both are defensible.** BL-835 chose a stamped payout-row deduction because *"a percentage applied to EARNINGS necessarily includes every dollar the clipper has already withdrawn and spent"*. The marketplace does not have that problem: it splits at the moment the money is created, before anyone can have been paid, so there is nothing already withdrawn to re-rate. **The stamped shape was the right answer to a different question.**

### The $100 example, worked, gross and cash

Gross $100.00, no bonuses, no cap, budget headroom ample, both parties standard (unreferred, no trainer, no express):

| | gross | fee | **cash** |
|---|---|---|---|
| clipper (creator) | $60.00 | 9% = $5.40 | **$54.60** |
| poster | $30.00 | 9% = $2.70 | **$27.30** |
| owner: platform row | $10.00 | none | **$10.00** |
| owner: the two payout fees | | | **$8.10** |
| **owner total** | | | **$18.10** |

**$54.60 + $27.30 + $18.10 = $100.00 exactly. Nothing created, nothing lost.** The platform leg is a residual rather than an independent multiplication (F-SEC-2A-FIX, `earnings-calc.ts:657-663`), which is what makes the three legs sum to `round2(gross)` at every price including sub-cent boundaries.

Both parties referred instead: fees become 4 percent, referrers receive 5 percent of net, and the owner nets **$9.28**. Still exactly $100.00.

> **BUT THE PARTS ONLY SUM TO THE WHOLE WHEN NEITHER PARTY HAS A BONUS.** `earnings-calc.ts:667-668` computes a level plus streak plus PWA bonus for **each** party against **their own** profile and adds it **on top** of their share. The platform gets none. At a 10 percent creator bonus and a 5 percent poster bonus the same $100 clip disburses **$107.50**, the campaign budget pays $107.50, and the owner's slice is 9.3 percent of what actually left rather than 10. **A marketplace clip is the only clip on the platform that carries TWO bonus stacks.** That is by design on the standard path, where one clip carries one; nobody appears to have written down that the marketplace doubles it.

### The stacking order, for a clipper who is referred AND trained AND posting through the marketplace

On withdrawal, `src/app/api/payouts/route.ts` and `payout-calc.ts`:

1. `feePercent = referredById ? 4 : 9` (`payouts/route.ts:452`), base = the payout GROSS (`payout-calc.ts:88`).
2. Express 4 percent (`payout-calc.ts:96-102`), base = **the same gross**, computed independently.
3. Trainer 10 percent (`trainer-cut.ts`), base = eligible slice less a prorated fee and a prorated notional 5 percent referral; express deliberately excluded (`TRAINER_BASE_INCLUDES_EXPRESS = false`).
4. `finalAmount = amount − feeAmount − expressFeeAmount − trainerCutAmount` (`payout-calc.ts:130`).
5. At PAID, the referrer's 5 percent is computed on `finalAmount + trainerCutAmount` (`payouts/[id]/review/route.ts:834-840`), which is BL-835 holding the referrer harmless from the trainer.

**No deduction is applied twice to the same dollar.** Two facts are worth the owner's attention:

• **The platform fee and the express premium share a base.** A referred express clipper loses 4 + 4 = 8 points of gross before the trainer's base is even computed. Deliberate, but it means "4 percent" appears twice on one payout meaning two different things.
• **BL-835 holds the referrer harmless from the trainer cut but NOT from the express fee.** `effectivePaid` still has express subtracted, so a clipper buying express silently shrinks their inviter's 5 percent. Same shape as the defect BL-835 fixed, one term away.

> **AND THE MARKETPLACE FINDING INSIDE THE TRAINER PATH: a marketplace CREATOR is never charged a trainer cut on their 60 percent.** The eligibility query is `db.clip.findMany({ where: { userId, campaignId, … } })` reading `clip.earnings` (`payouts/route.ts:496-506`), and on a marketplace clip `clip.userId` is the **poster**. For a creator-only withdrawal the clip set is empty, `totalApprovedGross = 0`, and `computeTrainerCut` returns zero. **A poster IS charged, on their 30 percent.** No comment anywhere addresses this, so it reads as an oversight rather than a decision. A mixed clipper is worse: `eligibleFraction` is computed over a denominator that excludes their creator dollars, so one withdrawal can be over-attributed to the trainer. The lifetime cap bounds it in aggregate, so it cannot overcharge across the relationship, only within a single withdrawal.

---

## PART 3: SLOTS AND THE RACE

### A slot is not a platform, and the correction costs the owner half his capacity

| the owner said | the code does | `file:line` |
|---|---|---|
| a slot is a platform | a slot is **one platform-post of a daily quota** | `schema.prisma:2634` |
| capacity is per listing | capacity is **per listing per UTC day**, reset at midnight | `submissions/route.ts:429-430` |
| platforms are the capacity | `platforms String[]` is a **validation set**, and `MarketplaceListingAccount` is capped at one account per platform by `@@unique([listingId, platform])` | `schema.prisma:2646`, `:2739` |

The arithmetic, `submissions/route.ts:442-455`, with the authoritative copy inside the lock at `:574-580`:

```
usedToday      = sum over today's PENDING|APPROVED|POSTED submissions of platforms.length (min 1)
requestedSlots = platforms.length (min 1)
refuse 409 when usedToday + requestedSlots > listing.dailySlotCount
```

**The owner's own example, worked.** A listing covering TikTok and Instagram; one clipper sends two clips.

| | |
|---|---|
| posted videos | **4** · one `Clip` and one `MarketplaceClipPost` per (submission, platform), `post/route.ts:705-742` |
| **slots consumed** | **4, not 2** |
| fits the default listing? | **No.** `dailySlotCount` defaults to 5, so one clipper eats 4 of 5 and the second clipper sending one dual-platform clip is refused that day |

**His "four posted videos" is right and his "two slots" is not.** There is also a ceiling he did not mention: `dailySlotCount` cannot exceed `campaign.maxClipsPerUserPerDay` (`listings/route.ts:329-336`), overridable only by the owner with `forceCap: true`.

A naming collision worth knowing: `api/marketplace/call-slots/route.ts` is 15-minute interview booking times for the poster application. It has nothing to do with capacity.

### The last-slot race: CLOSED, and better protected than several money paths

`submissions/route.ts:547-683` takes a row lock **and** Serializable:

```sql
SELECT id FROM marketplace_poster_listings WHERE id = ${listingId} FOR UPDATE
```
then recounts inside the transaction and throws `SLOT_EXCEEDED` → 409.

**Two simultaneous last-slot claims CANNOT oversell.** The second blocks on the lock, re-reads the committed count and is refused. The in-code comment at `:550-557` correctly explains why Serializable alone was insufficient: both transactions read the same snapshot and the write is an INSERT, not a conflicting UPDATE, so SSI does not detect it. This is the `FOR UPDATE` plus Serializable pattern, used at only 6 sites repo-wide, and it is **stronger** than the payout path's Serializable-plus-partial-unique-index (`uq_payout_open_per_user_campaign`, BL-696).

**The comment above the pre-flight check is stale and should be deleted, not believed.** `:424-428` still says *"Race condition between read and create is still acceptable for v1… A later hardening pass can wrap this in a serializable transaction if needed."* The hardening shipped; the comment did not.

### The double-post race: OPEN, and this is the worst defect in the round

`schema.prisma:2843` declares `@@unique([submissionId, platform])`, and the comment above it at `:2838-2842` asserts *"The matching DB index is applied out-of-band by the owner (CREATE UNIQUE INDEX CONCURRENTLY IF NOT EXISTS "marketplace_clip_posts_submissionId_platform_key")"*.

**IT WAS NEVER APPLIED. Measured against `pg_indexes` this round:**

```
marketplace_clip_posts_clipId_key          UNIQUE (clipId)
marketplace_clip_posts_pkey                UNIQUE (id)
marketplace_clip_posts_submissionId_idx    (submissionId)          <- NOT unique
```

A count of unique indexes covering both `submissionId` and `platform`: **0**. Prisma does not enforce `@@unique` at runtime; it only types `where` clauses. **So the constraint enforces nothing, and the `P2002` handler at `post/route.ts:771` is unreachable code.** What remains is an in-transaction `findFirst` at `:696-705`, inside a transaction that takes **no `isolationLevel`** (`post/route.ts:560`), so it runs at Read Committed.

**The exact interleaving:** poster opens two tabs and posts two different TikTok URLs for the same platform on one APPROVED submission. TX A's `findFirst` sees nothing. TX B's `findFirst` sees nothing either, because A's insert is uncommitted and invisible at Read Committed. Both commit. **Two tracked, earning `Clip` rows for one slot**, `totalPosted` incremented twice, both accruing CPM against the campaign budget.

The fix is one `CREATE UNIQUE INDEX CONCURRENTLY`. **It was not run.**

### Filling, adding slots, and returning a slot

**When a listing fills, nothing happens.** No auto-close, no auto-pause, no status write. `dailySlotCount` appears in 0 lines of `src/lib/`. A full listing stays fully visible in browse (`browse/route.ts:196-197` has no capacity predicate) showing `slotsLeft = 0`. The only automatic listing pause is budget-driven.

**Adding slots reopens capacity instantly and retroactively for the same UTC day**, because the gate re-reads `txListing.dailySlotCount` live inside the lock. Raising 5 to 8 with 5 used lets 3 more through immediately, with no cool-off and no re-approval. On a `PAUSED` listing the edit is accepted but does not unpause; only a budget top-up can auto-resume, and only when `pauseSource = BUDGET_EXHAUSTED`.

**A slot is never "returned", because there is no counter to return it to.** Capacity is a derived aggregate recomputed from scratch on every read, over `status IN (PENDING, APPROVED, POSTED)`. The instant a row leaves that set its slots are back. **Racy? No. Returned twice? Impossible.** Every status flip is CAS-guarded, so the flip itself is once-only.

**One genuine leak of intent:** capacity is keyed on `createdAt`, not on state. A submission created at 23:59 UTC that is still PENDING rolls off the counter at 00:00 while remaining live for another 23h59m. **A listing sized for 5 can carry 10 simultaneously in-flight PENDING submissions across a midnight boundary.** Nothing treats that as an error.

---

## PART 4: THE POSTER'S OBLIGATION AND THE PENALTY

### What is verified, and what is not

The poster pastes up to 3 URLs (`post/route.ts:200-311`). They are sanitised, length-capped, https-only, host-matched to platform, TikTok slideshows blocked, checked against the platforms committed at submission time, and deduped on `normalizedUrl`. **Then the URL is fetched exactly once, and the only thing that fetch is used for is the AGE of the post** against `MAX_CLIP_AGE_MS` = 30 minutes (`clip-config.ts:13`), at `post/route.ts:60-132`, called at `:503`.

**Nothing in the response is compared to the submitted video.** View counts, author, caption and thumbnail are all discarded.

**Two verifications the owner may believe exist and which do not:**

• **The video is never matched.** `MarketplaceVideoHash` is SHA-256 of the canonicalised **Google Drive URL** of the submitted file (`video-hash.ts:12-23`, labelled "LITE version", perceptual hashing deferred). It is written at submission and incremented on rejection, and **never read by `/post`**. Its only consequence is a UI badge. A poster can post an entirely different video and nothing notices.
• **Account ownership is never re-proven at post time.** The clip is stamped with the listing's `ClipAccount`, and `resolveListingAccount` checks only that the join row is ACTIVE and the account APPROVED. **The word `username` appears zero times in the 990-line post route.** A poster can paste any in-window URL, including someone else's, and it is accepted. The only backstop is human: the clip lands PENDING and the owner must approve it.

### CAN A POSTER BE PENALISED BECAUSE OUR FETCH FAILED? YES, AND THERE IS NO GUARD

**Six branches treat a fetch failure as a refusal**, `post/route.ts`: `:77-84` (Instagram or TikTok null), `:97-99` (Instagram null `createdAt`), `:104` (Instagram throw), `:114-116`, `:117-119`, `:126-129` (all three YouTube branches, including a missing `YOUTUBE_API_KEY`). **TikTok is the only platform with a lenient fall-through**, at `:100` and `:106`, and it is lenient by accident of two comments rather than by policy.

Upstream, `fetchClipStats` collapses "gone", "carousel quarantine", "persisted gone", "provider 5xx" and "we skipped the call to save money" all into `{stats: null}` (`apify.ts:2422`, `:2431`, `:2450`, `:2474`, `:2489`). `checkFreshness` reads only `stats == null` and never inspects the provider or the verdict. **This is precisely the conflation BL-720 narrowed the gone-verdict to prevent, reintroduced at the marketplace post gate.**

The path, end to end:

1. The poster posts the clip for real at T+0.
2. They call `/post` at T+2 min. The provider is down, rate-limited, timing out, or 404s a live-but-private post.
3. **400. Nothing is recorded.** No attempt log, no counter, no audit row. The system now has no evidence this poster ever tried.
4. They retry. **The 30-minute freshness window closes.** From that moment the same URL is refused **permanently** by a different branch (`:89-95`), even after the provider fully recovers. The only escape is deleting the real post and re-posting it.
5. At T+24h the sweep selects on `postDeadline < now AND postedAt IS NULL` and writes `reason: "MISSED_POST_DEADLINE"` (`marketplace-timers.ts:206-219`).
6. The third such strike in 30 days triggers a **72-hour marketplace ban and flips every ACTIVE listing the poster owns to `BANNED`** (`:386`, `:416-431`).

**There is no provider-health check, no circuit breaker, no deadline extension, and no record of a refused attempt anywhere in the 771 lines of `marketplace-timers.ts` or the 567 of `expire-deadlines`.** The strike predicate is purely "deadline passed and nothing posted". **The system cannot distinguish "did not post" from "posted, tried to declare it, and we refused them."**

**One fabricated zero on this path, named:** `post/route.ts:723-731` writes `views: 0, likes: 0, comments: 0, shares: 0` unconditionally at clip creation. It is a seed row for a clip seconds old rather than a measurement over an unknown, but it is a real `0` in `clip_stats` indistinguishable from a measured one, and the `shares: 0` bypasses BL-820's `sharesSource` "unmeasured" convention entirely. **Everywhere else the never-zero contract holds**: no provider failure path writes a 0 view count.

### The penalty, who decides, and reversibility

**Automatic. The owner does not confirm and is not even notified**; only the struck poster is. Thresholds live in the `strike_config` singleton, and the live row is **version 0, untouched since 2026-05-20 14:57:39.107**, so the running values are the schema defaults: `permanentStrikeThreshold` **3**, `missedDeadlineBanHours` **72**, `rejectionThresholdCount` 10, `rejectionWindowDays` 5, `rejectionBanHours` 48.

**No money is lost by a missed deadline**, because no clip was ever created, so there is nothing to claw back. **No rating hit**: a `POST_EXPIRED` submission can never be rated (`rate/route.ts:121-124`).

**Reversal is partial.** A dispute (`strikes/[id]/dispute/route.ts`) opens a ticket and flips the strike to `DISPUTED`; the owner resolves `UPHELD | REMOVED | REDUCED`. `REMOVED` sets `status: RESOLVED, bannedUntil: null` and the ban lifts on the next read. **But `User.clipperMarketplaceBannedUntil` is written by `expire-deadlines/route.ts:387` and cleared by NOTHING.** The dispute resolver does not touch it and the manual unban route clears only the other scalar. Since `isUserMarketplaceBanned` merges all three sources by MAX, **a ban from that scalar has no reversal path in the product at all**, only waiting it out or direct SQL. Unreachable today, and one boolean away from reachable.

### The cron reconciliation, which neither subagent could make alone

`cron_runs` has **four kinds, ever**: `tracking` (14,931 runs), `lifecycle` (5,065), `watchdog` (2,531), `tracking-timeout` (5, legacy). **Nothing else has EVER fired.**

`expire-deadlines`, `decay-strikes` and `counter-recompute` are all registered in `CRON_JOBS` (`railway-cron-scheduler.ts:72`, `:81`, `:84`) **and each writes a `cronRun.create` heartbeat on completion**. Zero rows of any of those kinds exist. `isJobEnabled` returns false for everything when `RAILWAY_NATIVE_CRON` names it not (`railway-cron-scheduler.ts:102-108`), and the observed set says the allowlist contains only tracking, lifecycle and watchdog.

| path | live today? | consequence |
|---|---|---|
| `processMarketplaceTimers` | **YES** | called from `tracking.ts:4295`, inside a cron that ran 6 minutes before this read. **The poster-strike path IS reachable.** |
| `expire-deadlines` | **NEVER RUN** | the competing `APPROVED → EXPIRED` flip cannot fire, and the disabled creator-strike path is doubly unreachable |
| `decay-strikes` | **NEVER RUN** | **strikes never decay.** The 1-per-day decay after a 30-day quiet period has never executed |
| `counter-recompute` | **NEVER RUN** | listing counters are never reconciled |
| `expire-submissions` | **NOT EVEN REGISTERED** | absent from `CRON_JOBS`; its work is duplicated inside `expire-deadlines`, which also never runs |

**This resolves a nondeterminism one subagent reported as live.** Two crons do disagree about whether an overdue APPROVED submission becomes `EXPIRED` or `POST_EXPIRED`, and a partially posted submission would be labelled by whichever ticked first. **Today only one of them can run**, so the outcome is deterministic by accident, and it will stop being deterministic the moment the allowlist is widened.

> **CROSS-ROUND CORRECTION I OWE, since it is my own:** yesterday's BL-838 attributed roughly 4.2 HikerAPI calls an hour to the `retire-dead-clips` cron. **`retire-dead-clips` is registered at `railway-cron-scheduler.ts:92` and has never fired either.** That line of BL-838's reconciliation is wrong; the residual it was covering belongs to the thumbnail path alone. The round's conclusion is unaffected, its arithmetic is not.

---

## PART 5: WHO SEES WHAT

### The owner's 10 percent: never sent, and derivable anyway

**The field-level protection is genuinely well built, across five independent mechanisms.** `MARKETPLACE_PLATFORM_SHARE` appears in exactly four places, none on a non-owner path. `computePayoutShape` (`marketplace-payout-shape.ts:70-104`) returns only the viewer's own share-applied rate; the type has no gross and no platform figure. `computeAdminPayoutShape` is the only producer of `platform_cut` and both call sites are ternary-gated on `viewerRole === "admin"`. Two independent `sanitizeCampaign` twins strip seven CPM fields for every non-admin, `browse/route.ts:440-448` rebuilds `campaign` as four harmless keys, and `stripSubmissionCpm` removes the frozen CPM on all five non-owner submission responses. BL-531's four forbidden names return **three hits across the entire marketplace, all of them comments.**

**And the marketing copy defeats all of it.** Five surfaces print the percentages in plain English:

| surface | `file:line` |
|---|---|
| "You earn **60%** of what the views make." | `MpExplainer.tsx:104-105` |
| "You earn **30%**." | `MpExplainer.tsx:110` |
| "Posters earn **30%** of campaign revenue… Clippers earn **60%**." | `apply-client.tsx:298-299` |
| "…earn **30%** of campaign revenue. Clippers earn **60%**." | `incoming-client.tsx:396` |
| "earning **60%** per landed clip… (earn **30%**…)" | `marketplace-client.tsx:469` |

Beside them, `MpPayoutChip.tsx:76-82` renders the viewer's own share as dollars per 1k views. A clipper reading "$3.00 / 1k" and "you earn 60%" computes gross = $5.00 and the missing tenth = $0.50 per 1k. `apply-client.tsx:298-299` is worse: it names **both** halves in one sentence, so 100 − 60 − 30 = 10 needs no dollar figure at all. The chip's own header comment at `MpPayoutChip.tsx:15` claims *"Never shows 60% / 30% percent labels on non-admin cards"* · true of the chip, false of every page it sits on.

> **VERDICT ON THE OWNER'S REQUIREMENT: the 10 percent is (a) never sent as a field and (c) effectively rendered, recoverable by one division and one subtraction from strings the product prints to both non-owner parties.** This is a sharper version of the residual leak F-MARKETPLACE-EARNINGS-CARD already documented and accepted in 2026-05-21, which assumed the deriver had to be a clipper enrolled in the campaign reading a gross CPM elsewhere. **They do not. One screen is enough.**

**A third route, and it is the one I did not expect.** `listing/[id]/page.tsx:246-262` and `listings/[id]/route.ts:388-400` build `budgetWarning = { budgetUsedPercent, isApproaching, isCritical, remainingUsd }` **with no `viewerRole` gate at all**, send it to every viewer on every listing-detail load, and render it ungated at `listing-detail-client.tsx:243` and `TrustBadges.tsx:102-120` ("Budget approaching limit (87%, $412.50 left)"). And `spent` in `getCampaignBudgetStatus` (`balance.ts:487-497`) **includes the platform earnings aggregate and the ghost fee**, so it is the full gross spend. **A campaign's budget and remaining spend are owner economics, they are disclosed to clippers and posters, and this is the only place on the platform where that happens** (`budgetUsedPercent` and `remainingUsd` appear nowhere outside the marketplace).

### Cross-party visibility

**A clipper sees about a poster:** username, avatar, join date, the two marketplace rating aggregates, `posterStatus`, the listed social account, and listing counters. **No email, no Discord id, no wallet, no payout method, no earnings.** Email is selected in 8 places and every one is consumed server-side to address a transactional email, never returned.

Two deliberate cross-listing trust signals a clipper does get: `posterTrust.rejectionRate30d`, computed across **all** the poster's listings, and `posterActiveListings`, a count of their other live listings. Neither carries rates or income. Design, not defect.

**A poster sees about a clipper:** id, username, the two rating aggregates, the Drive URL, platforms, status, timestamps and a duplicate-submission collusion flag. On a posted clip they see `clip.earnings`, **which on a marketplace clip is their own 30 percent**, and the creator's `views` but **not** the creator's `amount`. Correct. Their query is hard-scoped to `where: { listing: { userId: me } }`, so they cannot see a clip the clipper made for anyone else.

**No leak of either party's total earnings, other campaigns, balance, payout history or contact details to the other.** Ratings and rating notes are visible both ways by stated policy. One inconsistency: `submissions/route.ts:890` returns the poster's internal `userId` to the clipper where `browse/route.ts:451` strips exactly that field.

**Chat is clean and private from the owner too.** Eligibility is a live join requiring an active submission, listing is `OR [userAId, userBId] = me`, detail returns 404 not 403 to a non-participant, and **no admin or owner chat viewer exists anywhere**. That last point cuts both ways: marketplace DMs are an unmonitored channel in which two parties could agree an off-platform rate, which is the exact behaviour F-HIDE-PLATFORM-FEE exists to discourage.

**Email and broadcast carry no figure at all.** All 12 senders interpolate only handles, a campaign name, a reason, a deadline and a strike count. The broadcast's external legs are hard off (`MARKETPLACE_BROADCAST_MODE = "in_app"`).

**The ban-check contract holds: 17 `isUserMarketplaceBanned` call sites, 27 `assertNotMarketplaceBannedStrict`, and zero bare `db.user.findUnique` access checks.**

### The owner's own view: yes, and wider than intended

The full breakdown renders per clip in the admin queue, `admin/clips/page.tsx:2225-2270`: **"Clipper share"** `:2228`, **"Poster share"** `:2239`, **"Owner share"** `:2261`, **"Total paid ="** `:2265`. It also renders per listing in `MpPayoutChip.tsx:141-190` when `viewerRole === "admin"`.

**But the "Owner share" row is gated only on `isMkt`, not on `isOwner`.** Its CPM_SPLIT neighbour four lines above IS owner-gated (`:2222`, with a comment citing the CLAUDE.md rule that agency and owner data stay out of an ADMIN's reach). So **an ADMIN, and a REVIEWER holding `EARNINGS_VIEW`, would both see the platform cut in dollars** the moment a marketplace clip is approved. Live exposure today is zero: no marketplace clips exist and no account holds ADMIN.

**And the owner's own marketplace admin page does not render the breakdown it is sent.** `admin/listings/route.ts:165` computes `payoutAdmin` and ships it at `:175`; `marketplace-admin-client.tsx` never references it. Dead payload and an unnecessary widening.

---

## PART 6: EVERY HOLE, RANKED

**BROKEN** means it is wrong in shipped code. **UNBUILT** means it was never written. **UNTESTED** means it exists and has never executed.

| # | finding | class | `file:line` | what it would cost |
|---|---|---|---|---|
| 1 | **The `(submissionId, platform)` unique index was never created.** The schema comment asserts it was applied out of band. `pg_indexes` says no. `/post` runs at Read Committed with only an in-transaction `findFirst`. | **BROKEN** | `schema.prisma:2843`, `post/route.ts:560`, `:696-705` | **Two earning clips for one slot.** Duplicated CPM against the campaign budget for as long as it goes unnoticed. **Money created from nothing.** |
| 2 | **A poster can be struck and banned because our fetch failed.** Six branches, Instagram and YouTube fully exposed, including a missing `YOUTUBE_API_KEY`. No attempt is recorded and the 30-minute window then closes permanently. | **BROKEN** | `post/route.ts:77-129`, `:89-95`, `marketplace-timers.ts:128-219` | A 72-hour ban and every listing flipped to `BANNED`, for a real post, caused by our defect. |
| 3 | **Budget scale-down breaks the L1 invariant on approval.** `review/route.ts:643-645` floors the three legs but passes the unscaled `mktBreakdown.poster.base` to `writeClipEarnings` at `:744-747`; `assertInvariant` throws above $0.01 drift. The non-marketplace branch DOES rescale at `tracking.ts:2274-2280`. | **BROKEN** | `review/route.ts:643-647`, `:744-747`; `tracking.ts:2431-2437`, `:2751-2753` | **Approving a marketplace clip against a nearly-exhausted budget throws instead of writing.** The first real listing to near its budget hits this. |
| 4 | **Null dereference on the proportional-cut path.** `breakdown` stays null for a marketplace clip; `guaranteeScaleOn` excludes marketplace, so control reaches `:2295` which reads `breakdown.baseEarnings` unconditionally. | **BROKEN** | `tracking.ts:2034`, `:2258`, `:2295-2307` | Any marketplace clip in a budget-constrained campaign whose earnings rise throws a TypeError on the tick. |
| 5 | **`marketplace-cascades.ts:262` writes `REJECTED` with no status guard and no transaction**, on plain `db.`, after a JS filter. Every other status write in the marketplace is CAS-guarded. | **BROKEN** | `marketplace-cascades.ts:243-269` | Stamps `REJECTED` over a `POSTED` row with live earning clips if a `/post` commits in the window. The class of bug already fixed twice under BL-300 and BL-301. |
| 6 | **The 10 percent is derivable from one screen.** Field protection is excellent; the copy names both halves. | **BROKEN** (against the stated requirement) | `apply-client.tsx:298-299`, `MpExplainer.tsx:104,110`, `incoming-client.tsx:396`, `marketplace-client.tsx:469` | The behaviour F-HIDE-PLATFORM-FEE exists to prevent: off-platform renegotiation. |
| 7 | **Campaign budget and remaining USD sent and rendered to every viewer**, and `spent` is the full gross. | **BROKEN** | `listings/[id]/route.ts:388-400`, `listing/[id]/page.tsx:246-262`, `TrustBadges.tsx:102-120`, `balance.ts:487-497` | Owner economics disclosed to clippers and posters; a third route to the gross and therefore to the 10 percent. |
| 8 | **"Owner share" visible to ADMIN and to REVIEWER with `EARNINGS_VIEW`**, because the row is gated on `isMkt` and not on `isOwner` like its neighbour. | **BROKEN** | `admin/clips/page.tsx:2261-2264` vs `:2222` | The owner said not visible to anyone. Zero live exposure today. |
| 9 | **A marketplace creator is never charged a trainer cut on their 60 percent**, because eligibility reads `clip.userId`, which is the poster. A poster IS charged. A mixed clipper can be over-attributed within one withdrawal. | **BROKEN**, possibly unintended | `payouts/route.ts:496-506`, `trainer-cut.ts:328` | Trainers earn nothing on marketplace income. Whether that is right is the owner's call; nothing records a decision. |
| 10 | **`User.clipperMarketplaceBannedUntil` has no reversal path.** Written by one cron, cleared by nothing; the dispute resolver does not touch it. | **BROKEN** | `expire-deadlines/route.ts:387`, `marketplace-ban.ts:72-95` | A ban only SQL can lift. Unreachable while that cron never runs and its issuing flag is false. |
| 11 | **Bonuses are added on top of the split**, so the three parts exceed the gross and the platform's slice is under 10 percent of what actually leaves the budget. Two bonus stacks on one clip, unique to the marketplace. | **BROKEN** by omission | `earnings-calc.ts:667-668` | Budget drains faster than 60/30/10 predicts. Not a loss, but not what the owner described. |
| 12 | **`Math.floor` on all three legs at approval** leaves up to $0.03 of a capped clip allocated to nobody. Conservative, never an overpay. | **BROKEN**, minor | `review/route.ts:643-647` | A few cents per capped clip, budget-side. |
| 13 | **Independent rounding under `payoutReductionRatio`** re-rounds the three shares separately, so the exact-residual guarantee is lost by up to a cent. | **BROKEN**, minor | `tracking.ts:2207-2227` | Sub-cent drift per clip per tick. |
| 14 | **Freeze zeroes `baseAmount` and `bonusAmount`; restore puts back only `amount`.** Self-heals on the next tick. **No invariant middleware guards either marketplace table.** | **BROKEN**, transient | `tracking.ts:3243-3245`, `:1753-1756` | A creator row reading `amount = X, base = 0` between restore and the next tick. |
| 15 | **Listing hard-delete sets `videoUnavailable: true` via `updateMany` without stamping `savedEarnings`** or touching the creator and platform rows. | **BROKEN** | `admin/listings/[id]/override/route.ts:291` | The only marketplace `clip.update*` in the tree, and it writes none of the four invariant fields. |
| 16 | **Capacity keyed on `createdAt`, not state**, so 2× `dailySlotCount` can be in flight across midnight. | **BROKEN** by design gap | `submissions/route.ts:433-445` | A poster gets twice the review queue he sized for. |
| 17 | **Two crons disagree on the overdue-APPROVED exit** (`EXPIRED` vs `POST_EXPIRED`); a partially posted submission is labelled by whichever ticks first. | **BROKEN**, currently masked | `marketplace-timers.ts:190-201` vs `expire-deadlines/route.ts:314-322` | Deterministic only because one of the two has never run. |
| 18 | **The video is never matched and account ownership is never re-proven at post time.** | **UNBUILT** | `video-hash.ts:6-8`; `post/route.ts` (0 hits for `username`) | A poster can post a different video, or someone else's. Only owner approval stands in the way. |
| 19 | **No record that a poster attempted to declare and was refused.** No log, no counter, no audit row. | **UNBUILT** | `post/route.ts:64`, `:79`, `:86` are `console.log` only | The failure rate at the freshness gate is unmeasurable from the database, so item 2 cannot be detected after the fact. |
| 20 | **Three marketplace crons have never run**; `expire-submissions` is not even registered. | **UNTESTED** | `cron_runs`: 0 rows of every marketplace kind | Strikes never decay; counters never reconcile. |
| 21 | **The stale comment at `submissions/route.ts:424-428`** still says the slot race is unhardened. It was hardened. | **BROKEN** doc | `submissions/route.ts:424-428` | A future engineer "fixes" a race that is already closed, or trusts the comment and reopens it. |
| 22 | **`payoutAdmin` computed and shipped, never rendered.** | **UNBUILT** | `admin/listings/route.ts:165`, `:175` | Dead payload, unnecessary response widening. |
| 23 | **`allowContentReuse` is owner-set by SQL only.** | **UNBUILT** | `schema.prisma:186` | A policy switch with no way to reach it. |
| 24 | **Everything else in this report.** | **UNTESTED** | 0 submissions, 0 posts, 0 earnings | Every path above has executed zero times in production. |

**Money that could be created from nothing:** item 1 (duplicate earning clips) and item 11 (two bonus stacks). **Money that could be lost:** items 12 and 13, cents. **Double payment:** none found; the creator's 60 and the poster's 30 live in different tables joined to different user ids, the self-listing case is explicitly reasoned, and reject/undo deletes both rows atomically. **A share left unassigned:** item 12, up to $0.03 per capped clip.

**`writeClipEarnings` exclusivity holds.** A multiline grep for a `clip.update` whose `data` block contains any of the four invariant field names returns **0 matches** outside the two doc comments. Inside marketplace code specifically: **1** `clip.update*` and **0** invariant field names in it.

---

## PART 7: THE TEST PLAN FOR BL-842

> **THE SANDBOX TOOLING DOES NOT EXIST AND MUST BE BUILT.** There is no BL-840 commit on `main`, no script under `scripts/` matching `bl840`, `sandbox` or `seed`, and no BACKLOG entry. `BL-840.md` in the reports repo belongs to a different project sharing the numbering. **BL-842 must build the harness as its first act, and the safeguard is not optional given items 1 through 5 above.**

### The safeguard, specified

Before any write, the harness must assert **all** of the following and abort loudly on any failure, printing the offending row:

• every user it touches has `isTestUser = true`
• every campaign it touches has `isTestCampaign = true`
• the process is NOT pointed at a database whose `clips` count exceeds a stated ceiling without an explicit `--i-know` flag
• a pre-run census of all 14 marketplace tables is recorded with counts and `MAX` timestamps cast `::text`, and re-recorded at the end
• every row it creates carries an identifiable prefix (`bl842-`) so a sweep can find them
• teardown is by that prefix, is idempotent, and reports what it deleted against what it created

### What BL-842 must create

| | count | why |
|---|---|---|
| test posters | **3** | one approved, one pending, one approved-then-revoked, to exercise the cascade |
| test clippers | **4** | two ordinary, one referred, one referred AND trained, to exercise the stacking |
| listings | **3** | one single-platform, one dual-platform, one triple; `dailySlotCount` 1, 2 and 5 |
| campaigns | **2** | one with ample budget, one deliberately near exhaustion, both `isTestCampaign` |

### Every case that must be proven, with no judgement left

**Money**
1. A $100 gross marketplace clip produces creator 60.00, poster 30.00, platform 10.00, summing to exactly 100.00, and `Clip.earnings` holds **30.00**, not 100.00 and not 60.00.
2. The same at a sub-cent boundary (gross $0.55) proving the platform residual absorbs the drift and the three still sum to `round2(gross)`.
3. **With bonuses on both parties, record what actually leaves the budget** and state it beside 60/30/10. This is item 11 and it needs a number, not an argument.
4. A referred creator, a trained creator, and a referred-and-trained creator each withdraw; record fee, express, trainer cut and `finalAmount` for each, and **prove whether the trainer cut on the creator's 60 percent is zero** (item 9).
5. A poster withdraws and **is** charged a trainer cut on the 30 percent, confirming the asymmetry.
6. Self-listing (poster = clipper) produces the 90 percent combined hit with both rows written and findable.
7. Reject and undo an approved marketplace clip; prove both earning rows are deleted atomically and the budget is released.

**Slots and the race**
8. A dual-platform listing with `dailySlotCount = 2` accepts one dual-platform submission and **refuses the second with 409**, proving a slot is a platform-post and not a platform.
9. **Two concurrent last-slot claims**: fire both inside the same millisecond and prove exactly one wins with `SLOT_EXCEEDED` on the other.
10. **Two concurrent posts of DIFFERENT URLs for the same platform on one submission.** This is item 1. **Expect it to succeed twice and produce two earning clips.** Record it as the reproduction, then apply the index in a scratch database and prove the second is refused.
11. Cross the UTC midnight boundary with a PENDING submission and prove 2× `dailySlotCount` in flight (item 16).
12. Raise `dailySlotCount` on a full listing and prove capacity reopens retroactively the same day.
13. Reject a submission and prove the slot returns; reject it twice and prove nothing is returned twice.

**Posting and the penalty**
14. Post with the provider **stubbed to fail** on Instagram and on YouTube; prove the 400, prove nothing is recorded, then advance the clock past 30 minutes and prove the same URL is refused permanently.
15. Advance past the 24-hour deadline and prove `MISSED_POST_DEADLINE` is written **against a poster who really posted**. This is item 2 and it must be demonstrated, not argued.
16. Prove TikTok is lenient on the same failure, so the inconsistency is on the record.
17. Post a URL for a video the poster does not own and a video that is not the submitted one; prove both are accepted (item 18).
18. Issue three strikes, prove the 72-hour ban and that every ACTIVE listing flips to `BANNED`; dispute and `REMOVED`, prove the ban lifts; then prove `clipperMarketplaceBannedUntil`, if set, does not (item 10).

**Budget and the invariant**
19. Approve a marketplace clip against a **nearly exhausted** budget and prove item 3: the invariant throws rather than writing.
20. Let a marketplace clip's earnings rise in a budget-constrained campaign and prove item 4's TypeError on the tick.
21. Revoke a poster while a submission is mid-post and prove item 5 can stamp `REJECTED` over `POSTED`.

**Visibility**
22. Load the listing detail page as a clipper and as a poster and **capture the full JSON payload**. Prove `platform_cut` is absent, and prove `budgetWarning.remainingUsd` is present (item 7).
23. Screenshot `apply-client.tsx` and `MpExplainer` and record that 60 and 30 are printed, then compute the 10 from one screen (item 6).
24. Render `/admin/clips` as an ADMIN over a marketplace clip and prove "Owner share" is visible (item 8).
25. Prove a poster cannot see the creator's `amount`, and a clipper cannot see the poster's other listings' economics.

**Crons**
26. Invoke `processMarketplaceTimers` directly and prove the strike path fires. **Do not assume `expire-deadlines` runs**; prove from `cron_runs` that it still has not (item 20).

**Every one of these is a read or a write against test rows only. None requires touching a real user, a real campaign or a real payout.**

---

## SAFETY

| | |
|---|---|
| changes made | **none.** No code, config, schema or data. Nothing created, nothing deleted. The only file added is this report |
| requests | **every one a read.** No POST, no PATCH, no DELETE, no vendor call, no Apify actor |
| money | no clip, payout, earning or campaign created, modified or deleted; the 6 money files read and not edited |
| database | read-only through `scripts/run-select.js`, every timestamp cast `::text` against DB `now()` |
| the missing index | **identified, NOT created.** `CREATE UNIQUE INDEX` was not run |
| build | **not run.** A markdown-only diff cannot change `tsc`, and no build is claimed |
| concurrent rounds | a peer session holds a different repository entirely and was told so; nothing here touches anything it holds |
| worktree `C:/w841` | **removed** |
| counting | every count from a SQL `COUNT(*)` or `grep -c`, never piped through `head` |

**RECONCILED, NOT AVERAGED.** Three subagent findings are corrected here rather than repeated: the claim that two crons race for the overdue-submission flip (only one has ever run); the report digest's reading of BL-840 (a different project's round, which I confirmed against `git log` and `scripts/`); and the open question about whether `spent` is gross (it is, and it raises the budget leak's severity).

**WHAT COULD NOT BE DETERMINED**

* **The live value of `NEXT_PUBLIC_MARKETPLACE_ENABLED` on Railway.** It is commented out locally and absent from `.env` and `.env.example`. The zero-row production state and zero non-test poster applications are consistent with it being off, but the deployed environment was not read.
* **The live `RAILWAY_NATIVE_CRON` allowlist.** Inferred from `cron_runs`: only tracking, lifecycle and watchdog have ever fired, and six registered jobs never have. The variable itself was not read.
* **Whether all three `posterStatus` writers invoke `cascadePosterRevoke`.** The cascade is a caller obligation rather than an enforced invariant; the helper was traced, not each call site.
* **Whether the budget-scale invariant throw surfaces to an operator or is swallowed by the transaction retry loop.** The terminal error sink past `tracking.ts:2918` was not traced.
* **Whether the trainer's blindness to marketplace creator income is intended.** No comment anywhere addresses it.
* **The real-world failure rate at the `/post` freshness gate.** Nothing is persisted, so it is unmeasurable from the database, and with zero submissions it is currently zero by definition.

**PERFORM NO FIX. Nothing in this round was changed.**
