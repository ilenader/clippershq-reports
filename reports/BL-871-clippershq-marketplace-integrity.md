# BL-871 — one hole is real and fixed, one is unfixable by hashing and needs no hashing, one is trivially detectable

**TEARDOWN FIRST: NOTHING IS UNREMOVABLE. NO SQL IS OWED.** 6 ledgered rows,
`VERIFIED: 0 of 6 recorded rows remain`. A direct catalogue sweep confirms zero
`bl871sbx-` rows survive in `users`, `campaigns` or `marketplace_poster_listings`,
and zero `MARKETPLACE_LISTING_SLOTS_CLAMPED` audit rows remain.

**2026-09-09. One bounded fix, two specs. Requires a Railway REDEPLOY.**

---

## THE THREE ANSWERS IN ONE PARAGRAPH

**Overselling: the owner's premise is wrong in his favour, and a narrower hole is
real and now fixed.** A listing cannot be created offering more than the campaign
allows. But the check runs once and never again, so lowering a campaign cap under
a live listing left the listing offering the old number. Nobody's work is
stranded; the campaign's own limit is breached instead. **Theft: the platform can
see nothing at all, and no hash will ever change that.** But the theft and the
"poster who never posts" are THE SAME EVENT, and that event is trivially visible
at zero cost. **Detection at scale: fingerprinting is not worth building, and the
report recommends against it.**

---

## PART 1 — CAN A LISTING PROMISE MORE THAN THE CAMPAIGN ALLOWS

### Where capacity is checked, with file:line

| Moment | What it compares | Where |
|---|---|---|
| Listing CREATE | `dailySlotCount` vs `campaign.maxClipsPerUserPerDay` | `listings/route.ts:334`, ceiling fetched `:315`, floored `:333` |
| Listing EDIT | the same | `listings/[id]/route.ts:518`, campaign preloaded `:78` |
| SUBMISSION | `listing.dailySlotCount` only | `submissions/route.ts:470`, twins at `:644` and `:805` |
| POST | `submission.listing.dailySlotCount` only | `post/route.ts:800` (BL-847's settle gate) |
| Campaign edit | **nothing** | `campaigns/[id]/route.ts:444-447` (owner, clamps to 20) and `:261` (admin, clamps to 10) |

**`grep -n "maxClipsPerUserPerDay"` returns ZERO hits in both `submissions/route.ts`
and `post/route.ts`, and `grep -n "marketplacePosterListing"` returns ZERO hits in
`campaigns/[id]/route.ts`.**

### So the owner's exact case CANNOT happen, and I am correcting his premise

A poster cannot create a listing offering ten when the campaign caps him at six.
`listings/route.ts:334` refuses it with `dailySlotCount must be between 1 and 6
(campaign cap)`. **That already worked before this round and the ten clippers he
worries about would never have been collected.**

### The real hole, which is narrower and different in kind

The check runs at creation and at a voluntary edit, and **never again**. A listing
created legitimately at ten against a cap of ten keeps offering ten after the
campaign is edited down to six.

**AND NOBODY'S WORK IS STRANDED, WHICH IS THE PART WORTH GETTING RIGHT.** Clips
seven through ten are not collected and then refused. They are submitted, posted
and paid, because every downstream gate reads the listing rather than the
campaign. What is silently breached is the CAMPAIGN's own per-user-per-day
intent. The marketplace post path never consults `maxClipsPerUserPerDay` at all:
the ordinary submit path enforces it at `clipper-submit-core.ts:384` as
`override ?? campaign.maxClipsPerUserPerDay ?? 3`, and the marketplace path has
no equivalent.

**Measured in production today.** One listing exists, offering 5 against a cap of
15, so nothing is oversold right now. Campaign caps range 3 to 20 with 18 of 34
campaigns at 3. Eight `clip_limit_overrides` rows exist, and **all eight RAISE a
poster's limit; not one lowers it**, so the second-order version of this hole
(an override below the campaign cap) has never been used in the dangerous
direction.

### The fix, and why it is at the moment of change rather than at submission

Prevention beats refusal, and the create-time check is already prevention. The
gap is only that the number can go stale, so the fix restores the same philosophy
at the moment the number changes: **when a campaign's cap is lowered, its
listings are lowered with it.**

Refusing the campaign edit while a listing exceeds the new cap was rejected: the
campaign is the authority and the listing is derived from it, so letting a
marketplace listing veto a campaign change is backwards. Refusing at submission
was rejected too: by then a clipper has already chosen the listing on the
strength of a number that was never true.

**Full diff.** One new file `src/lib/marketplace-listing-clamp.ts`, and one block
in `campaigns/[id]/route.ts` immediately after `db.campaign.update`:

```ts
const newCapRaw = (data as any)?.maxClipsPerUserPerDay;
const oldCap = (oldCampaign as any)?.maxClipsPerUserPerDay;
const newCap = typeof newCapRaw === "number" ? newCapRaw : parseInt(String(newCapRaw ?? ""), 10);
if (Number.isFinite(newCap) && (oldCap == null || newCap < Number(oldCap))) {
  const { clampListingsToCampaignCap } = await import("@/lib/marketplace-listing-clamp");
  const clamp = await clampListingsToCampaignCap(id, newCap, session?.user?.id ?? null);
  ...
}
```

The helper only ever LOWERS. It has no path that raises a number, it skips
`DELETED` and `REJECTED` listings, it writes one audit row per clamped listing so
the owner can see why a poster's capacity changed, and its entire body is inside
a try/catch that swallows and returns a count, so a clamp failure leaves the
listing exactly as it is today.

**Proof: 13 assertions, 0 failed.**

- a create asking for 11 against a cap of 10 is refused; 10 is allowed
- **without the clamp the listing still offers 10 against a cap of 6** (the hole, demonstrated)
- with the clamp it becomes 6
- a control listing already at 4 is **not touched**
- running the clamp twice changes nothing
- **a HIGHER cap never raises a listing** (10 to 6, then cap to 20, listing stays 6)
- an audit row records the clamp and its reason
- no clip, no earning, no payout, no agency row was created

### What happens when a campaign limit changes under a live listing

Before this round: nothing. The listing kept its old number for ever, and both
meters kept honouring it. After this round: the listings drop with the cap, one
audit row each, and the poster's next voluntary edit is validated against the new
number as it always was. **A cap moving UP leaves listings where they are**, which
is correct: a poster who chose five slots did not ask for twenty.

---

## PART 2 — THE THEFT CASE

### What the platform can see today: nothing. That is the finding.

A poster receives a clipper's video, posts it from his own account outside the
marketplace, and submits it as an ordinary clip.

`Clip` carries `marketplaceSubmissionId` and `isMarketplaceClip`
(`schema.prisma:1026-1027`), and both are written **only** by the marketplace post
path. The ordinary submit route `clips/route.ts` POST (`:1070-1398`) contains
**zero** marketplace references; every marketplace hit in that file is inside
`GET` and is for display. `clips/owner-submit/route.ts` has `grep -c` of **0**.

**So the stolen clip is created with `isMarketplaceClip = false`, no
`marketplaceSubmissionId`, and no link to anything. There is no column, no query
and no code path anywhere that would connect it to the submission it came from.**

This is not new. BL-841 said it in as many words: *"The video is never matched.
`MarketplaceVideoHash` is SHA-256 of the canonicalised Google Drive URL... and
never read by `/post`. Its only consequence is a UI badge. A poster can post an
entirely different video and nothing notices."*

### What BL-868's hash actually covers, and why it cannot help here

`computeVideoUrlHash` hashes `gdrive:<fileId>` for a Drive link, and
`hostname + pathname` for anything else. **It hashes the LINK to the file the
clipper sent. It has never touched a single byte of video, before or after
BL-868.**

**A FILE HASH CANNOT VERIFY A POSTED VIDEO, AND THE OWNER SHOULD NOT BE TOLD
OTHERWISE.** TikTok and Instagram transcode on upload: a different container, a
different bitrate ladder, a different resolution, re-encoded audio, and on TikTok
a burned-in watermark. **Not one byte survives.** A cryptographic hash is designed
so that a single flipped bit produces a completely unrelated digest, so a SHA-256
of the uploaded file and of the source file are not "close"; they are unrelated
numbers. This is not a tuning problem or a threshold to loosen. It is what a hash
IS.

### The four things that could actually work, priced

Costs use BL-838's measured rates: **HikerAPI $0.00069214 per request**,
**LamaTok $0.00060007 per request**, **YouTube free**. None of those vendors
returns video BYTES, so every content-matching option below is a self-hosted
compute cost plus bandwidth, not a per-call vendor price.

| Option | What it would take | Cost per clip | What it gets wrong | Worth it |
|---|---|---|---|---|
| **Perceptual video fingerprint** (pHash, TMK) | download the Drive source AND the posted video, decode both, sample frames, compute and compare fingerprints. Weeks of engineering plus a worker with ffmpeg. | roughly 20 to 80 MB of transfer and a few seconds of CPU per pair. Cents per clip on commodity hosting, but a new always-on service to run. | **Structurally high false positives in THIS business.** Every clipper clips the same podcast, the same stream, the same trailer. Two honest clippers cutting the same thirty seconds of the same source produce near-identical fingerprints. The detector cannot tell theft from the normal case. | **NO** |
| **Audio fingerprint** (Chromaprint) | same pipeline, audio only. Cheaper to compute. | a few MB and well under a second per pair. | **Worse.** Everyone uses the same trending sound on purpose, because the campaigns require it. Near total false positive rate on a music-driven platform. | **NO** |
| **Frame sampling with a cheap distance** | pull a handful of thumbnails, compare histograms or a small hash. | pennies, and the thumbnail is often already fetched. | Cheapest and least accurate. Same source-footage problem, with less signal to work with. | **NO** |
| **PROCESS: the poster must produce the live URL before the clipper is paid** | almost nothing. `/post` already records a `MarketplaceClipPost` with the live URL, and payment already flows from that. | **zero** | Nothing. It does not detect theft; it makes theft not pay. | **YES, and it is already how the system works** |

### The reframe that makes this tractable

**The theft case and PART 3's "poster who never posts" are the same event.** A
poster who steals a video simply never posts it through the marketplace. He
cannot: posting through `/post` is what creates the split that pays the clipper
30 percent, which is the thing he is avoiding.

So the question is not "can we prove he stole it", which needs content matching
and is not worth building. The question is **"is there a submission he accepted
and never posted"**, which is a single indexed database query over rows that
already exist, costs nothing, and is 100 percent accurate about the SIGNATURE
even though nothing can be accurate about the ACT.

**Detection of the act is impossible. Detection of the footprint is trivial.**

### And any detector must be evidence, never a verdict

BL-771 measured every computable signal on this platform against the human bar
and found the best one at **20.2 percent precision against a requirement above
99.2 percent**, concluding *"Every count-only signal is roughly two orders of
magnitude short"* and *"Nothing may auto-reject and no clipper may see machine
suspicion."* A fingerprint detector would sit in that same class. It would be a
queue for a human, and BL-771's own warning applies: *"a queue where four in five
entries are innocent will be ignored within a fortnight."*

---

## PART 3 — CHASING A POSTER WHO NEVER POSTS

### What exists today, with file:line

**Five real strike-creation sites** (`grep -c` = 5, a sixth match being generated
Prisma client code):

| # | Site | Reason | Live |
|---|---|---|---|
| 1 | `admin/users/[id]/marketplace-ban/route.ts:183` | `OWNER_ISSUED` | yes, manual |
| 2 | `excessive-rejections.ts:207` | `EXCESSIVE_REJECTIONS` | yes |
| 3 | `marketplace-timers.ts:252` | `MISSED_POST_DEADLINE` | **yes, the only automatic one** |
| 4 | `cron/marketplace/expire-deadlines/route.ts:390` | `MISSED_DEADLINE:<platform>` | **dead** |
| 5 | `cron/marketplace/expire-deadlines/route.ts:503` | `MISSED_DEADLINE:<platform>` | **dead** |

4 and 5 are gated off by `ISSUE_CREATOR_POST_DEADLINE_STRIKES = false` at
`expire-deadlines/route.ts:74`, checked at `:269`, deliberately, because strike
authority for a missed post deadline belongs solely to `marketplace-timers.ts`.

**The window is 24 hours**: `POST_DEADLINE_MS = 24 * 60 * 60 * 1000` at
`approve/route.ts:19`, stamped at approval at `:133`.

**The two excuses that stop a strike**: `activeBan`
(`marketplace-timers.ts:203-209`) and `couldNotConfirm = sub.verifyFailedAt != null`
(`:232`), both checked at `:234` and `:305`. When either holds, the submission
flips to `POST_EXPIRED` and **no strike row is written**, and the poster is told
*"We could not check your post in time, so this one is closed and NOTHING was
counted against you"* (`:336-342`).

**It runs inside the tracking cron**, not its own job: `tracking.ts:4428` calls
`processMarketplaceTimers`, reached from `cron/tracking/route.ts:315`. The
`tracking` job is `explicitOnly: true` in the scheduler (`railway-cron-scheduler.ts:63`).

### An attribution correction the brief asked for implicitly

The brief says BL-849 found a poster could be struck because our own fetch failed.
**It was BL-845** that found it and added `verifyFailedAt` and
`verifyFailedReason`. **BL-847** then found a bug inside BL-845's own fix, which
gated the no-strike flip on `activeBan` alone instead of `activeBan ||
couldNotConfirm`, so for the exact case BL-845 was written for the code fell
straight through. **BL-849** found the NEW entrance BL-847 had opened with its
settle gate. Three rounds, three different findings, and the record should say so.

### NOTHING CHASES. The owner is told nothing.

Every notification on the missed-deadline path targets the poster or the creator.
**No call anywhere in `marketplace-timers.ts` is parameterised with an owner id.**
The only owner-facing surface is a pull dashboard, `marketplace/admin/page.tsx`,
which shows a `strikes24h` count he has to go and look at.

BL-870's refusal recorder does not cover this either, and the reason is
structural: it wraps HTTP handlers, and a poster who never posts never makes a
request. **There is nothing to record because nothing happened.**

### The spec: a chaser that surfaces and never punishes

**What it is.** A read-only query, once a day, for submissions that are `APPROVED`
with `postedAt IS NULL` and `postDeadline` in the past, grouped by poster, shown
to the owner on the panel BL-870 already built at `/admin/problem-reports`.

**The window.** None to choose. The 24 hour deadline already exists and is already
stamped on the row. The chaser reports at deadline plus zero.

**What it costs: nothing.** Zero provider calls. One indexed query over
`marketplace_submissions`, which already has `@@index([postDeadline])` and
`@@index([listingId, status])`. At pilot scale it reads single-digit rows.

**How it avoids BL-849's trap.** It reads the SAME two excuses the strike path
reads, `verifyFailedAt` and the active-ban check, and shows an excused row
separately and labelled, rather than counting it against anybody. A row excused
because OUR fetch failed appears under "we could not check this one", not under
"this poster did not post".

**It never strikes and never bans.** It creates no `MarketplaceStrike` row, sends
the poster nothing, and changes no status. It is a list the owner reads. Given the
history here, seven claimed strike entrances across three rounds with one of them
opened by the round that was closing them, **a new automatic penalty is exactly
what should not be built.**

**Recommendation: build it, in a later round, as a query and a list.** It is
cheap, it is the actual answer to the theft question, and it carries no risk of
firing on the platform's own failure.

---

## PART 4 — WHAT WAS FIXED AND WHAT WAS SPEC'D

**FIXED: the overselling clamp.** One new helper and one block in the campaign
edit path, proven 13 of 13 in the sandbox with the hole demonstrated first.

**SPEC'D, NOT BUILT: the chaser.** It needs a new query, a new panel section and a
decision about how excused rows are presented. It is cheap and safe, but its
consequences are a screen rather than a guard, and it was not built in the same
round as a money-adjacent route edit.

**SPEC'D AND RECOMMENDED AGAINST: content fingerprinting.** Priced above. In a
business where every clipper clips the same source footage, the false positive
rate is not a tuning parameter, it is the shape of the problem.

### The proofs

**Sandbox**, BL-842's tooling, `SANDBOX_ROUND=bl871`, opening snapshot taken
before anything was created. `verify-gone.ts`: **50 checks, 50 passed, 0 failed.**
`agency_earnings` 4,676 to 4,676, `audit_logs` 27,838 to 27,838, `notifications`
14,635 to 14,635, **approved earnings $14,413.47 unchanged to the cent**,
**INVARIANT VIOLATIONS 0**, zero payouts created. The clips, tracking jobs and
snapshots that moved are three clips submitted by one real clipper during the
window, attributed by the tool itself.

**The four money invariants hold trivially and that is worth stating plainly.**
The only write this round makes is `dailySlotCount`, an integer on a listing. It
touches no earning, no payout and no clip. BL-824's paid-is-final, BL-627's
no-overpayment, BL-696's no-double-pay and BL-538's never-decrease are
arithmetically out of reach rather than merely respected.

**The 6 money files, `tracking.ts` and `campaign-era.ts` are byte-identical by
blob OID on both refs.** No schema change, no `prisma migrate`, no index, no
Apify actor, the 11 BL-678 guards intact, no Prisma in a browser bundle, no
Supabase pool errors. Clean tsc baseline of 0 errors taken before any edit;
eslint present with 3 binaries so the hooks gate is not a silent no-op.

**No accessibility review was needed and none is claimed.** This round changed one
library file and one API route. It touched no component, no page and no markup.

---

## PART 5 — THE VERDICT FOR TOMORROW'S PILOT

**Measured scale right now: one approved poster, one listing, zero submissions,
zero posts, zero marketplace clips, zero creator earnings.** The marketplace has
still never had a live clip.

| Hole | Matters at ONE poster | Matters at hundreds |
|---|---|---|
| Overselling | **No.** It needs the owner to lower a cap under a live listing. Fixed anyway, and the one live listing offers 5 against a cap of 15. | Yes, as campaigns are edited routinely |
| Theft | **It is a trust question, not a systems question.** One known poster, and every stolen clip is a submission he visibly never posted. | Yes, and it is the reason to build the chaser |
| Detection at scale | **No.** There is nothing to scale. | Yes, and the answer is still the chaser, not fingerprinting |

**The pilot should go ahead.** None of the three is a launch blocker at one
poster. The theft hole is real and permanent, and at this size it is answered by
the owner looking at one number.

### What to watch on day one

1. **Every submission that goes `APPROVED` and stays that way past 24 hours.** That
   single fact is the whole theft signal, and at one poster it is one query or one
   glance. Until the chaser exists, nothing will tell him.
2. **Whether the poster's posted URLs are the videos the clippers sent.** By eye,
   at this volume. It is the only content check that exists and the only one worth
   doing at ten clips.
3. **Any `MISSED_POST_DEADLINE` strike**, and specifically whether the submission
   carries `verifyFailedAt`. If it does, the platform failed, not the poster, and
   the strike path has fired wrongly three times across three rounds already.
4. **The listing's `dailySlotCount` against the campaign's cap**, if he edits the
   campaign. It should now follow the cap down on its own, and an audit row saying
   `MARKETPLACE_LISTING_SLOTS_CLAMPED` is how he confirms it did.

---

## THE MODEL SPLIT

**Opus** did the money and judgement work: reading the capacity chain and
establishing that nothing is stranded, deciding the fix belongs at the moment of
change rather than at submission or at refusal, writing the clamp and its proof,
the hash and re-encode reasoning, pricing the four detection options and
recommending against three of them, the reframe that theft and never-posting are
the same event, and this report.

**Sonnet** did two retrieval jobs: mapping capacity, strike and clip-linkage code
to file:line, and distilling nine prior reports. Its work produced the attribution
correction in PART 3, which I checked before using.

**Nothing money-touching was split**, and nothing money-touching was changed: the
only write this round makes is an integer on a listing row.
