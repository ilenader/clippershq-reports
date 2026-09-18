# BL-904 — Launch clearance

**Round:** BL-904 · **Date:** 2026-09-18 · **Merge commit:** `8f6f0433`
**Tags:** `pre-merge-BL-904`, `post-BL-904`

**NOTHING WAS DELETED, AND NOTHING COULD BE.** The five `bl###` test fixtures and their four clips are
**unremovable**: `reviewer_audit_log` is append-only (BL-87 trigger) and holds **9** rows pointing at
`bl833-watch-only` and **11** pointing at the four fixture clips, all `ON DELETE SET NULL`, so removing
any of them requires an UPDATE of an immutable table. Both attempts rolled back whole and the database is
byte-for-byte as it was. They are invisible to every clipper regardless.

**ONE LINE VERDICT:** The code is ready and the gate is proven both ways, but **the marketplace is empty
for an ordinary clipper**, because no real campaign is opted into it; setting the Railway flag today would
open a working marketplace with nothing in it.

---

## Model split

Opus did all of it. The enumeration, every classification, the deletion file, the filter fix, the walk,
the renders and this report, with **no subagent between it and the source**, because the round's intended
output was a delete against a live database with 1,766 users.

---

## The two things he must decide

### 1. No real campaign is in the marketplace

| measure | value |
| --- | --- |
| campaigns an ordinary clipper sees with the flag on | **0** |
| campaigns with `campaignType` of `BOTH` or `MARKETPLACE_ONLY` | **1**, and it is the test one |
| every real campaign's type | `NORMAL` |
| real campaigns that are ACTIVE and not archived | **1**: *Zhus Edit (0.50 CPM)*, $2,000 budget, 862 approved clips |
| also live but PAUSED | *SomeSome App*, $2,214 budget, 769 approved clips |

To open one, for whichever campaign he chooses:

```sql
UPDATE campaigns SET "campaignType" = 'BOTH' WHERE id = 'cmsisj3d800f10po8jvz526hf'; -- Zhus Edit
```

**What that costs him, measured by BL-902 rather than estimated:** the platform's 10 percent **ADDS** to
his ordinary cut, and the ordinary cut is `views/1000 × ownerCpm`. On *Zhus Edit* that means the campaign
spends **$163.94 per $100 of gross** and he nets **$82.04**. Same budget, fewer views. That is the trade
and it is his.

### 2. The three flagged accounts, and whether they keep the flag

`isTestUser` does **not** gate money. It gates two things: it grants early sight of the marketplace, and
it grants sight of **test campaigns**. Once the flag is on, the first stops mattering and only the second
does.

| account | flagged | last sign-in | what the flag does for him now |
| --- | --- | --- | --- |
| `ankara06885` (the OWNER) | yes | **today 11:58** | nothing extra; OWNER already sees test campaigns |
| `testclipper_26758` | yes | **today 09:38** | lets him keep walking the clipper side of the test campaign |
| `1jackclipstest` | yes | **today 09:06** | same |

**Recommendation: leave all three flagged.** The only consequence is that they can still see his test
campaign, which is precisely what he uses them for. Clearing the flag would take that away and buy
nothing, because no ordinary clipper can see a test campaign any more regardless of who is flagged.

**A test campaign still cannot pay out** either way: BL-884's typed `CAMPAIGN_IS_TEST` refusal sits at the
payment site, and BL-904 adds a refusal at the posting route so nobody reaches that wall by surprise.

---

## PART 0 — Everything enumerated, then classified

All four marketplace v2 tables hold **zero** rows. Every previous round cleaned up after itself.

### The eight flagged accounts

| id | name | created (`::text`) | money | classification |
| --- | --- | --- | --- | --- |
| `cmn4m6lh60000q8w7a62mjrey` | ankara06885 (OWNER) | 2026-03-24 12:52:07 | none | **IN USE. Signed in today.** |
| `cmoobbldj00000po3cdg29a6r` | testclipper_26758 | 2026-05-02 12:23:11 | none, 6 clips, 4 accounts | **IN USE. Signed in today.** |
| `cmobu3f02000a0pojvlorsdzr` | 1jackclipstest | 2026-04-23 18:47:42 | none | **IN USE. Signed in today.** |
| `bl815-fixture-clipper` | BL-815 TEST FIXTURE | 2026-08-20 17:59:43 | none | SAFE, but **unremovable** |
| `bl821-fixture-clipper` | BL-821 TEST FIXTURE | 2026-08-23 21:48:28 | none | SAFE, but **unremovable** |
| `bl825-stranger-clipper` | BL-825 TEST FIXTURE (stranger) | 2026-08-24 17:09:38 | none | SAFE, but **unremovable** |
| `bl825-invitee-clipper` | BL-825 TEST FIXTURE (invitee) | 2026-08-24 17:09:38 | none | SAFE, but **unremovable** |
| `bl833-watch-only` | BL-833 TEST FIXTURE (watch only) | 2026-09-01 18:02:10 | none | SAFE, but **unremovable** |

**The decisive evidence that the five fixtures are not people:** every one has `discordId IS NULL`.
Discord OAuth is the only way to sign in, so none has ever signed in or can. Their names say TEST FIXTURE
in capitals. "do not review" is an instruction to a human reviewer not to approve the fixture clips; it is
not a deletion warning.

### The brief's own figures pointed at the wrong account

The brief said the owner's test accounts hold *"$248.60 of clip earnings and 13 payouts totalling
$991.11."* Checking rather than trusting:

**That is `dusan_ristic_` (`cmn4nlfgc0003q8w7h4a3vynu`), and `isTestUser` is FALSE.** It is the admin's
real account: 203 clips, 13 payouts totalling exactly $991.11, and **$260.30** of clip earnings today, not
$248.60, because the tracking cron has kept ticking since that figure was taken. It was never at risk
from anything keyed on the test flag, and it was not touched.

### The two test campaigns

| id | name | state | contents | classification |
| --- | --- | --- | --- | --- |
| `cmu5yeax20000h4w7yv5n387y` | Marketplace test campaign | ACTIVE, `BOTH`, $500 | 0 clips, $0 | **IN USE.** His walking campaign. |
| `cmomvxcu000000ppbu6762nxx` | "Test " | PAUSED, **archived**, $300 | 0 clips, $0, 2 members | **LEFT.** Both members are his own accounts; archived so invisible. |

### The four fixture clips

All four are `isDeleted = true`, `status PENDING`, `earnings 0`, on two **real** campaigns (*Zhus Edit*,
*Zhus Meme*). Because they are deleted, pending and worth nothing, **no aggregate on this platform counts
them**, so they change no campaign's spend.

### Left alone and named

- `bl825-selfclip` — a fixture clip attached to a **real** user, `jdb001` (a REVIEWER who signed in
  today). Already `isDeleted`, so already invisible. Left because it sits on a real person's record and
  removing it buys nothing visible.

---

## PART 1 — What a real clipper would actually see

### The leak, measured rather than read

`/api/marketplace-v2/campaigns` filtered on archived, status and campaign type, and **not on
`isTestCampaign`**. It deliberately *sent* `isTestCampaign` so the screen could show a warning.

BL-892's reasoning was right for its moment: one test campaign went into production so the owner could
walk the whole loop, and the screen warned that withdrawal would be refused. **It stops being right the
moment everybody can see it.** A warning is not a substitute for not showing somebody a campaign that
cannot pay them.

**Measured:** that route returned exactly **one** campaign platform-wide and it was
*Marketplace test campaign*.

### The fix, at the filter

`filterTestCampaigns(role, isTestUser)` already decides exactly this question for the first marketplace:
OWNER and test users see test campaigns, nobody else does. **Reused, not re-invented**, so there is one
definition of the rule and the owner keeps his access. Applied at:

| surface | file |
| --- | --- |
| the campaigns list | `api/marketplace-v2/campaigns/route.ts` |
| the clip catalogue | `marketplace-v2-poster.ts` → `listCatalogueForPoster` |
| the poster's campaign cards | `marketplace-v2-poster.ts` → `listCampaignsForPoster` |
| the clip detail | `marketplace-v2-poster.ts` → `getCatalogueClipForPoster` |
| **the posting route itself** | `createV2Post`, a **refusal**, not a hide |

The last one matters: BL-888 measured **nine of eleven** v2 routes ungated while all six pages were
gated. A hidden tile whose route still answers is that defect wearing a different hat, so somebody
holding the clip id from a link or an open tab is refused rather than allowed to earn and be stopped at
withdrawal.

### The `includeTestCampaigns` divergence, settled

BL-882 recorded it and three rounds mirrored it: the clipper-facing display **excludes** test campaigns
while the withdrawal gate **includes** them, so the two could disagree about a balance.

**It cannot bite, and this is the measurement rather than an opinion.** Across *both* test campaigns:

| | |
| --- | --- |
| clips | **0** |
| earnings | **$0.00** |
| payouts | **0** |
| maker legs | **0** |

A divergence can only disagree about money that exists, and there is none. With BL-904's posting refusal,
no ordinary person can put money there either. It is left as it is, deliberately, because changing a
withdrawal predicate hours before launch to fix a disagreement that has nothing to disagree about would
be the riskier act.

---

## PART 2 — The deletion that the database refused

The file is `scripts/migrations/BL-904-remove-test-fixtures.sql`, written by explicit id with no pattern,
no wildcard, no LIKE and no date range anywhere in it.

**Every cascade was traced against `information_schema`, not against the schema file**, because BL-837
found `audit_logs` was CASCADE in the live database while the schema declared SetNull. It is genuinely
`SET NULL` now, so history survives its actor.

What would have followed the five users: 4 clips, 4 clip_accounts, 4 user_lifecycle rows. Zero clip_stats,
zero tracking_jobs, zero campaign_accounts, zero notifications, **zero payout_requests**, zero
agency_earnings, zero audit rows as actor.

**Then the database refused, twice:**

```
Mutation failed: reviewer_audit_log is append-only (BL-87 immutability trigger).
UPDATE and DELETE are blocked at the DB layer.
```

Measured **after** the first refusal rather than guessed: `reviewer_audit_log` holds **9** rows pointing
at `bl833-watch-only` via `reviewerUserId` and **11** pointing at the four fixture clips via `clipId`,
both `ON DELETE SET NULL`, so removing any of them requires updating an immutable table. Deleting the
users is blocked too, because their clips cascade from them and the clips are what the audit rows point
at.

**This is correct rather than unfortunate.** Those fixtures existed to be *reviewed*, so they have review
history, and the platform guarantees review history is immutable. Removing them would mean disabling an
immutability trigger on an audit table on a live platform hours before fifty people arrive, to tidy rows
nobody can see.

### Nothing moved

| measure | before | after |
| --- | --- | --- |
| users | 1,772 | **1,772** |
| clips | 10,285 | **10,285** |
| clip_accounts | 1,527 | **1,527** |
| payout_requests | 250 | **250** |
| real-clip fingerprint | `a33fee4dc3a81fe8e31c3c2c1b05c140` | **identical** |
| payout fingerprint | `dd731273bed48fe90074846d0f5ef8d8` | **identical** |

Both transactions rolled back whole. Nothing was half applied. The file is kept as the record with every
DELETE commented out.

---

## PART 3 — The gate, both ways

### With the flag off

| check | result |
| --- | --- |
| 24 requests, 6 routes × 4 personas (ordinary clipper, REVIEWER, non-owner ADMIN, signed out) | **all refused** |
| every refusal 404 and never 403 | yes (a signed-out visitor is allowed 401, having no session to test the flag against) |
| any refusal that was a rate limit | **0 of 24** — each persona had its own account |
| served page titles naming the feature | **none** |

### With the flag on

Proven on a **second server with the real environment variable set**, not simulated.

| check | result |
| --- | --- |
| an ordinary clipper reaches the marketplace | **200** (the same account was 404 with the flag absent) |
| test campaigns visible to him | **0 of 0** |
| the owner's test campaign id anywhere in the catalogue or card bodies | **absent** |
| its clip detail route asked directly | **404** |
| he can read the side chooser | **200** |
| **he can choose a side** | **stored side written and read back** |

**My first simulation was wrong and the check caught it.** Minting `isTestUser: true` does reach the
feature, but `filterTestCampaigns` reads that same flag, so the check was looking at a *test user* and
correctly reported the test campaign visible. A title check also failed on "Clippers HQ" because it
searched for "clip", which is the brand.

### The renders — BL-903's skip, overruled

**30 of 30 clean**, using BL-793's method: `innerWidth` and **the URL** read back from the page, every
state asserted **in words** from the rendered text, and the **pan** measured as
`scrollWidth − innerWidth`.

| | 320 | 375 | 414 | 1280 | 1440 |
| --- | --- | --- | --- | --- | --- |
| `/market` | 0px | 0px | 0px | 0px | 0px |
| `/market/campaigns` | 0px | 0px | 0px | 0px | 0px |
| `/market/catalogue` | 0px | 0px | 0px | 0px | 0px |
| `/market/editor` | 0px | 0px | 0px | 0px | 0px |
| `/market/editor/earnings` | 0px | 0px | 0px | 0px | 0px |
| `/market/poster` | 0px | 0px | 0px | 0px | 0px |

Titles read *"The marketplace — Clippers HQ"* and *"Clips you can post — Clippers HQ"*. **No v2 anywhere.**
Screenshots at `C:/bl904-sandbox/renders`. The `__Secure-` cookie needed `secure: true`, which the first
run lacked; 127.0.0.1 is a secure context so the app saw exactly the cookie it would in production.

---

## PART 4 — The money

| invariant | result |
| --- | --- |
| BL-627 no overpayment, both v2 aggregates counted | **20 budgeted campaigns, 0 over** |
| BL-696 no double pay, four tables | 0, 0, 0, 0 |
| the earnings invariant | **10,202 live clips, 0 violations, 0 negatives** |
| BL-824 paid is final, both earners separately | 0 negative maker legs |
| both reconciliation forms | 0 and 0 |
| the two uniques BL-902 and BL-903 added | verified present in `pg_indexes` |
| owner's test campaign | present, ACTIVE, untouched |

**Eleven protected money files byte-identical by blob OID.** `marketplace-v2-poster.ts` changed, which is
the visibility gate. **Zero `.tsx` changed.** Build exit 0 on the branch and again on `main`; hooks gate
0 errors and 11 warnings, identical to baseline; every prebuild guard green including the drift check at
142 constraints.

---

## PART 5 — His launch card

### The steps, in order

1. **Decide whether to open a real campaign.** Without this the marketplace works and is **empty**. If
   yes, in the Supabase SQL editor:
   `UPDATE campaigns SET "campaignType" = 'BOTH' WHERE id = 'cmsisj3d800f10po8jvz526hf';`
   *You should see:* `UPDATE 1`. Zhus Edit now accepts both ordinary clips and marketplace posts.
2. **Deploy `main` at `8f6f0433`** if Railway has not already.
   *You should see:* the build go green.
3. **Open `clipershq.com/market` yourself.** *You should see:* the marketplace, no "v2" in the address
   bar, and your test campaign still listed because you are the owner.
4. **Set the flag.** Railway → your service → Variables → `NEXT_PUBLIC_MARKETPLACE_V2_ENABLED` = `true`
   → redeploy. **This is the one step no round can do for you**; the variable lives in Railway and nothing
   in this repository can reach it.
   *You should see:* an ordinary clipper's account now reaching `/market`, and **not** seeing your test
   campaign.

### What to send your clippers

> The marketplace is open. It is a place to team up: one person makes a clip, another person posts it,
> and you both get paid for the same video.
>
> If you **make** clips, send your best edit to a campaign. Every time somebody posts it, you earn
> **45 percent** of what that post makes. One clip can be posted by lots of people, and you earn from
> every one of them.
>
> If you **post**, browse the clips other people have made, pick one you like, post it to your own
> account and paste the link. You earn **45 percent** of what your own post makes. You can post the same
> clip from several of your own accounts and you earn on each.
>
> You choose which side you are on per campaign, so you can make on one campaign and post on another.
> You just cannot do both on the same campaign.
>
> Find it at **clipershq.com/market**.

### What to watch

**First hour**

| number | where | bad looks like |
| --- | --- | --- |
| clips submitted and approved | `/marketplace-v2/admin` (your review queue) | zero after an hour, meaning nobody found it or the arrival screen is broken |
| refusals | `/api/admin/marketplace-v2/funnel?days=1` | the same refusal reason repeating for many different people, which means a gate is wrong rather than one person being wrong |

**First day**

| number | where | bad looks like |
| --- | --- | --- |
| campaign spend against budget | your campaign page | spend climbing far faster than views justify |
| people who arrived versus people who chose a side | the funnel route above | many arrived, few chose, meaning the chooser is confusing or broken |

### How to close it again, in one action

Set `NEXT_PUBLIC_MARKETPLACE_V2_ENABLED` back to `false` (or remove it) in Railway and redeploy.

**What happens to money already earned: nothing.** Every leg already written stays written. Clips already
posted go on earning on the next tracking tick, because nothing in the money path asks whether the flag is
on. The flag controls **visibility and new actions only**. People simply stop being able to reach the
marketplace to make or post anything new, and anything they have already earned is still theirs and still
withdrawable.

---

## Still not built, and what remains unproven

**Not built** (named by four consecutive rounds, and neither blocks launch):

1. **The owner's dashboard.** Every control and nearly every figure exists and was mapped in BL-903; what
   is missing is the page, a per-person panel and the per-day series.
2. **The unseen-clip badge.** The mechanism to reuse and what marks a clip seen are both specified in
   BL-903's report.

**Unproven, and this is the honest part.** **No marketplace clip has ever existed in production.** All
four v2 tables hold zero rows. No maker has ever submitted, no poster has ever posted, no v2 money has
ever been written outside a sandbox, and every proof across twenty-eight rounds is a sandbox proof.

**What that does guarantee:** the arithmetic, the budget lock, the duplicate rule, the side rule, the
gates and the refusals have each been exercised against the real code and the real database, many of them
adversarially, and the invariants hold across the full population of 10,202 live clips.

**What it does not guarantee:** that fifty real people behave like a sandbox. The first real submission
and the first real post are the first of their kind, and the first hour is worth watching for that
reason rather than because anything specific is expected to fail.

---

## Rollback

`git revert 8f6f0433`. No row was deleted, no money figure changed, and the one migration file is a
deliberate no-op.
