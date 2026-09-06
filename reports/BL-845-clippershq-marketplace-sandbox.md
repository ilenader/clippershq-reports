# BL-845 — the whole marketplace, exercised in the sandbox

**Nothing could not be removed.** Every row this round created is gone, proven by primary key and by
identical closing counts. There is no leftover with an id and no SQL for the owner to run to clean
anything up. The only thing left in the database on purpose is the unique index that should always have
been there.

Measured 2026-09-06, 18:48:48 to 19:45 UTC, against production. Worktree `C:/w845`, branch
`checkpoint/BL-845`, merged to `main`.

---

## 1. The two defects the round was called to fix

### The index that was declared and never created

`prisma/schema.prisma:2850` declares `@@unique([submissionId, platform])` on `MarketplaceClipPost`, and
the comment above it states the index was "applied out-of-band by the owner". **It never was.** Three
indexes existed on that table and not one of them was unique across those two columns.

Applied:

```sql
CREATE UNIQUE INDEX CONCURRENTLY IF NOT EXISTS "marketplace_clip_posts_submissionId_platform_key"
  ON public.marketplace_clip_posts ("submissionId", "platform");
```

It went in as its own single `--inline` statement. `scripts/run-schema-sql.js:203` sends the whole file
as one simple query, and Postgres wraps a multi-statement simple query in an implicit transaction block,
where `CREATE INDEX CONCURRENTLY` fails with SQLSTATE 25001. BL-696 recorded the same constraint in its
own header; two independent sources agree, so it is settled rather than inferred.

**Verified in the catalogue, not in the schema file:**

```
marketplace_clip_posts_submissionId_platform_key | UNIQUE btree ("submissionId", platform)
indisunique = true   indisvalid = true   indisready = true   indislive = true
```

**And verified by reproducing the race.** Two concurrent `/post` calls, same submission, same platform,
two different urls — the exact shape BL-842 watched succeed twice and produce two earning clips:

```
response 1: http 400 in 832 ms
response 2: http 201 in 1200 ms
EXACTLY ONE MarketplaceClipPost exists ......... rows=1, was 2 before the index
EXACTLY ONE earning Clip exists ................ clips=1
postedPlatforms holds the platform ONCE ........ ["TIKTOK"]
```

**Rollback needs the owner.** `run-schema-sql.js` refuses `DROP INDEX` outside a one-entry allowlist,
and that allowlist was **deliberately not widened**. In the Supabase SQL editor:

```sql
DROP INDEX CONCURRENTLY IF EXISTS "marketplace_clip_posts_submissionId_platform_key";
```

### A poster punished because our fetch failed

Two nullable columns, added additively through `run-schema-sql.js` and never `prisma migrate`:

```sql
ALTER TABLE public.marketplace_submissions ADD COLUMN IF NOT EXISTS "verifyFailedAt" TIMESTAMP(3);
ALTER TABLE public.marketplace_submissions ADD COLUMN IF NOT EXISTS "verifyFailedReason" TEXT;
```

Both confirmed present with `is_nullable = YES`.

**How the code tells "did not post" from "could not confirm."** `checkFreshness` in `/post` now returns
an optional `ourFailure` tag, and six branches carry one:

| branch | tag |
|---|---|
| provider returned null stats | `PROVIDER_NULL` |
| Instagram returned no `createdAt` | `PROVIDER_NO_TIMESTAMP` |
| Instagram provider threw | `PROVIDER_THREW` |
| YouTube returned no details | `PROVIDER_UNCONFIGURED` |
| YouTube returned no `publishedAt` | `PROVIDER_NO_TIMESTAMP` |
| YouTube provider threw | `PROVIDER_THREW` |

The "posted more than 30 minutes ago" branches **deliberately carry no tag**, because that is the
poster's own doing and it must still cost them. When a tagged failure fires, the submission is stamped
with the instant and the reason. The sweep reads it and reuses the existing active-ban arm: status still
flips to `POST_EXPIRED` so the creator is still told, but no strike is written and the `continue` lands
before `postersTouched.add`, so the poster cannot reach the ban count either.

**Proven in both directions, because either half alone proves nothing.** One poster, four submissions:
two never posted, one attempted inside the window and refused by our own provider, one more never
posted. Threshold 3, ban 72 hours, read live from `strike_config`.

```
sweep one   2 strikes, NOT 3           the failure we caused carries no strike
            not banned                 listing still ACTIVE
            POST_EXPIRED anyway        the creator is still told
sweep two   3 strikes, all genuine     banned until 2026-09-09T19:22:29Z
            listings BANNED            the next post refused 403
```

---

## 2. Seven more defects, found by running it

**1. The last-slot race answered the loser with a blank HTTP 500.** The data was always safe — the
`FOR UPDATE` lock only ever lets one submission through — but a Serializable 40001 (`P2034`) escaped the
catch, and `withDbRetry` does not treat a write conflict as retryable. Observed: statuses 201 and 500
with an empty body. Wrapped in `withSerializableRetry`, the retry re-enters the lock, re-counts, and
throws `SLOT_EXCEEDED`, which the existing catch already renders as a clean 409. Re-measured: **201 and
409, "This listing has reached its daily submission limit."** A conflict surviving three attempts now
gets a 503 saying the listing is busy, never a blank 500.

**2. A PENDING submission could be widened past the daily ceiling.** `PATCH` CAS'd on `status:
"PENDING"` and never re-derived capacity. On a listing with a ceiling of 2, `usedToday` went **2 then 3
on a plain HTTP 200**. The edit route now re-counts against the UTC day the submission was *created*
(the day it is charged to), refuses growth with the same 409 the create route uses, leaves narrowing and
swapping fully open, and **fails closed** on a database error. Re-measured: `PATCH` 409, `usedToday`
2 then 2, and a platform swap still 200.

**3. The same route did not dedupe platforms**, which the create route has done since F11.B. Now it
does: `["INSTAGRAM","INSTAGRAM"]` stores as one.

**4. Three blind status writes.** `marketplace-cascades.ts:262` and `clip-account-cascade.ts:170` wrote
`REJECTED` on ids alone, so a `/post` committing in the gap could have its `POSTED` row stamped
`REJECTED` while its clip kept earning. `marketplace-timers.ts:78` wrote `EXPIRED` with a bare
`update` — **and that is the one that actually runs**: `RAILWAY_NATIVE_CRON` is `lifecycle,watchdog`,
the marketplace cron routes are declared only in `vercel.json`, and `cron_runs` shows they have **never
written a heartbeat**. All three now CAS on the status they were read in. BL-300 fixed this shape in two
places and missed these.

**5. The `P2002` handler told the wrong story.** With the index live, a poster racing two *different*
urls for one platform was told "This clip URL has already been submitted to this campaign", which is
false and sends them hunting a duplicate that does not exist. Prisma's driver adapter left `meta.target`
**undefined** on the very race the branch exists for, so the code reads every place the cause might be
and, failing that, asks the database: the transaction rolled back, so a post row existing for that
(submission, platform) is the answer. Re-measured: **"This platform has already been posted for this
submission."**

**6. Every banned poster was emailed the wrong sentence.** `sendMarketplaceBanned` hardcoded "3 strikes"
and "48 hours"; `strike_config` says 3 and **72**, unchanged since 2026-05-20. The in-app notification
beside the call already interpolated the real values, and the strike notification carried the same false
"48h". Both now read the live config, at both call sites.

**7. Three places showed the marketplace 10% to a non-owner.**

| where | what leaked |
|---|---|
| `api/clips/route.ts` | `marketplacePlatformEarning` selected for anyone who could see money |
| `admin/clips/page.tsx` | "Owner share" **and** "Total paid", from which the cut falls out by subtraction |
| `marketplace/listing/[id]/page.tsx` | `listingBudgetWarning.earned` = poster 30 + creator 60 + platform 10, sent to every viewer |
| `api/admin/agency-earnings/route.ts` | gated on `EARNINGS_VIEW`, not OWNER |

The first three are now owner-gated server-side. On the fourth, the capability still opens the route and
still shows agency revenue; **only the marketplace figures are withheld**, and views and clip counts are
kept because they leak nothing.

**Live exposure measured before anything changed: 0 ADMIN accounts, 0 EARNINGS_VIEW holders, 0 rows in
`marketplace_platform_earnings`, 0 listings with a budget set. Nobody's screen changes today.**

---

## 3. The money, to the cent

Expected **by hand first**, from the shipped source, and written into the test as literals rather than
recomputed by the code under test. Five clippers, five campaigns, $100.00 gross each, requested,
approved and PAID as the owner so the commissions actually mint. **39 checks, 0 failures.**

| case | fee | express | trainer base | trainer cut | **clipper cash** | referrer | platform net |
|---|---|---|---|---|---|---|---|
| plain | 9.00 | — | — | — | **91.00** | — | +9.00 |
| referred | 4.00 | — | — | — | **96.00** | 4.80 | **−0.80** |
| trainer | 9.00 | — | 91.00 | 9.10 | **81.90** | — | +9.00 |
| express | 9.00 | 4.00 | — | — | **87.00** | — | +13.00 |
| all three | 4.00 | 4.00 | 91.00 | 9.10 | **82.90** | 4.60 | +3.40 |

**`final + fee + express + trainerCut = 100.00 EXACTLY` in all five.**

The trainer's base is **$91.00 whether or not the clipper is referred**, reached by two different routes
(100 − 9 − 0 unreferred, 100 − 4 − 5 referred), which is the property BL-835 designed for. Express is
excluded from that base by `trainer-cut.ts:139`. The referrer is **held harmless**: $4.80 and $4.60,
unchanged by the presence of a trainer cut.

**One thing does not sum, and it is stated rather than forced.** The referrer's 5% is not one of the
four parts of the payout row. It is a separate `ReferralCommission` minted at PAID and paid **on top of**
the gross, out of the platform's own margin. On a plain referred payout the platform collects $4.00 and
pays out $4.80 and is **$0.80 down**; add express and it collects $8.00, pays $4.60 and is $3.40 up.
That is arithmetic in the shipped code. It is reported, not changed.

**On the marketplace split itself**, `calculateMarketplaceEarnings` was checked against hand figures at
three grosses: $100.00 → 60.00 / 30.00 / 10.00; $0.55 → 0.33 / 0.17 / **0.05**; $4.57 → 2.74 / 1.37 /
**0.46**. The platform leg is a residual, so the three shares sum to the gross exactly at every rounding
boundary. **The 10% REPLACES the owner's CPM_SPLIT cut rather than adding to it** — `isCpmSplit` is
`!isMarketplaceClip && ...`, so no `AgencyEarning` row is written for a marketplace clip.

---

## 4. Slots, races and the daily quota

**16 checks, 0 failures.** Two slots, three clippers: the third refused 409. Rejecting a submission
returns its slot the same day. Two clippers on one free slot: exactly one wins, the loser gets the real
sentence, and the quota lands on its ceiling and not above it. One clipper firing two identical
submissions at once: one row, one 201, one 409. No clip broke the earnings invariant and no
`MarketplaceClipPost` exists without its clip.

**One defect is recorded and not fixed, because it is a design decision and not a bug.** A slot IS a
platform post, but capacity is charged at `submissions/route.ts:435` on the submission's `createdAt`.
`SUBMISSION_TTL_MS` and `POST_DEADLINE_MS` are both 24h, so a submission created late on day 1 can be
approved on day 2 and posted on day 3, while days 2 and 3 each grant a fresh `dailySlotCount`.
Reproduced: ageing one still-live submission back a day freed a slot it had not used, and a further
submission was accepted. **Real posts landing in one UTC day can reach three times `dailySlotCount`.**
Keying capacity on `MarketplaceClipPost.postedAt` would make the number mean what its name says. That is
the owner's call, not this round's.

---

## 5. Every role, every screen

**40 checks, 0 failures, by direct request** on the production build with real minted Auth.js sessions
and `DEV_AUTH_BYPASS=false`, because a bypass session carries an empty capability list and every
assertion would pass for the wrong reason.

Twelve forbidden field names are absent, **at any depth**, from every non-owner body across the listing
detail, submissions, browse and campaign-spend surfaces. `payoutAdmin` is present and **null** for a
non-owner, which is why the check asserts on VALUES and not on key names — asserting on the name raised
a false alarm on a null the first time it ran. The poster keeps their own listing's budget dollars,
deliberately, because it is their listing; the creator and the stranger get the warning with the
percentage and no dollars. Four owner-only routes answer 403 to all three roles and 200 to the owner,
each tested individually.

**25 shots, 150 render assertions, 0 failures** at 320, 375, 414, 1280 and 1440, `window.innerWidth`
printed beside every one, **0 at the wrong width and 0 with horizontal overflow**.

---

## 6. The accessibility review, and the one thing that needs a decision

It ran on every marketplace surface: 9 specialists, 65 files, **196 findings, 27 critical**. **Not one
was fixed in this round, deliberately.** The top five all land in `modal.tsx`, `globals.css` and
`app-layout.tsx`, which are app-wide files, and the reviewer's own conclusion is that they need their
own round with a full render pass:

- the shared Modal is not a dialog: no role, no `aria-modal`, no name, no focus trap, no Escape, across
  **11 marketplace dialogs at once**
- the marketplace focus ring measures **1.68:1** and is unlayered, so it silently beats every Tailwind
  `focus-visible:` utility written to fix it
- a one-second countdown ticks inside `role="alert"` on eight surfaces, so a banned user hears the
  banner re-read every second
- white on the accent fill is **3.40:1** on the primary CTA of every page
- `--bg-page` has 42 uses and **zero declarations app-wide**, so 18 marketplace panels paint transparent

Two items in lines this diff already touched were acted on: "Hard cap at write time" became "The cap is
checked when a clip is paid", and the budget chip now reads correctly without its numbers.

**One item is an owner decision and cannot be settled by a copy edit.** The 60/30 split is published in
`MpExplainer.tsx:104` and `:110`, four lines apart in one collapsed body rendered on every marketplace
tab, and again at `help/page.tsx:297` in a sentence that names the remainder outright. So `100 − 60 − 30`
is stated by implication on a page any clipper can load, and **no gate can close that identity**. The
gates in this round remove the DOLLAR TOTALS, which are somebody else's aggregate revenue and are not
derivable from anything a creator legitimately holds. The RATIO is the owner's own published policy.

---

## 7. Cycles

Seven, and each one found something.

| cycle | what it found |
|---|---|
| 1 | the index was missing; the strike path could not tell our failure from theirs; three visibility leaks |
| 2 | the race loser got a blank 500 (`P2034`); the PATCH bought capacity for free; the self-duplicate test had been passing without ever reaching the gate |
| 3 | the `P2002` message was false, and `meta.target` was undefined so the fix had to ask the database |
| 4 | the ban email and the strike notification both printed 48 hours over a 72 hour ban |
| 5 | the ban assertion read a user column and reported "not banned" while the next request in the same script was refused 403; it asks `isUserMarketplaceBanned` now |
| 6 | `payoutAdmin` raised a false leak on a null; the render harness timed out on three narrow widths while the pages were fully rendered |
| 7 | 66 audit rows and 13 video-hash rows the ledger could never have known about |

**Four tooling defects were fixed along the way**, and each had cost real time:
`resolveSandboxUser` took the FIRST ledger match for a label, so a re-run after a partial failure minted
a session for the abandoned user and every assertion failed for an invisible reason; `verify-gone.ts`
had BL-842's window start hardcoded, so it reported a real clipper's $128 payout from 13:04 as surviving
a round that began at 18:48; the render harness waited on one element's *visibility* rather than the
page's text; and `referral_commissions` was missing from the destroyer's allowlist, which would have
meant creating rows the destroyer refuses to touch.

**Recorded, not fixed, each for a stated reason:** the `createdAt`-keyed capacity above; the referrer's
5% exceeding the fee collected on an unadjusted referred payout; `totalApproved` and `totalPosted`
drifting by construction while `counter-recompute` would overwrite a correct lifetime figure with a
wrong instantaneous one; the trainer eligibility read being campaign-scoped and excluding
`MarketplaceCreatorEarning` while the withdrawal gate includes it; `assertTrainerCutSafe` returning HTTP
500 rather than a 4xx so a guard trip reads as a server fault; the poster keeping `remainingUsd` on
their own listing; and `audit_logs_userId_fkey` being ON DELETE CASCADE while the schema declares
SetNull.

**And one that is bigger than either defect this round was called to fix: Instagram marketplace posting
is dead on `main`.** `APIFY_HARD_OFF` is a compile-time const at `apify-hard-off.ts:62` with no env
lever, and `/post` passes `skipHikerOverlay: true`, so every Instagram URL is refused 100% of the time
in every environment. It needs its own round.

---

## 8. Nothing left behind

**195 rows created**, every id recorded in a ledger outside the repo at the moment of creation, deleted
by primary key and never by pattern, name or date: **191 deleted, 4 taken first by cascade, 0 of 195
remain.**

Then two things the ledger could not know about, because the **product** created them and their ids were
never recorded:

- **66 audit rows** written by the marketplace routes
- **13 `MarketplaceVideoHash` rows**, minted outside the submission's own transaction, on a table that
  held **zero** before this round

Both were swept in two passes: list, print every id with the reason it is ours, write the ids to a file,
then delete only what is in that file. **One of the 66 names the REAL OWNER** — `capture-server-error.ts`
attributes an error with no user context to him by convention, and its details carry this round's own
verbatim `TransactionWriteConflict` from the last-slot race. It is listed with that reason spelled out
rather than quietly swept.

**Closing counts, identical:** users 1675, campaigns 34, clip accounts 1480, campaign memberships 782,
payout requests 221, payout adjustments 9, trainer relationships / commissions / refunds 0, referral
commissions 7, notifications 14109, and **every marketplace table**. Real payout fingerprint
`42ab3988...` and real user fingerprint `79582590...` **byte-identical**. Earnings invariant **0
violations** before and after.

**14 invisibility checks, 0 failures**, asking every campaign, past-campaign, cross-campaign spend,
earnings, clips, leaderboard and referral surface **as a real clipper with 840 approved clips** — no
sandbox id, no prefix, no marker, no sandbox person in any answer.

**What moved is named:** 10 clips and 359 view snapshots from 5 real clippers and the tracking cron,
4 agency-earnings rows, and `over_payable_holders` 18 → 17, which is a derived metric of those same real
approvals. No sandbox row can appear in it, because none remains.

**No real vendor money could have been spent.** `tracking.ts` does not filter test campaigns and the
post route creates a job due immediately, so the one job the sandbox produced was deactivated and pushed
a year out the moment it existed: **0 active tracking jobs on any sandbox campaign at any point a tick
could have seen one.** No Apify actor was run and the 11 BL-678 guards are untouched.

**BL-842's disclosure recurred and is recorded rather than hidden.** A nested dotenv load inside a
dependency re-injects a variable deleted at module load, so the first script's sweep did attempt two
emails; Resend refused both with 403 because the addresses are `.invalid`. Every later script deletes
the key immediately before the call, and the logs then read `[EMAIL PREVIEW]`.

**A sandbox account held role OWNER for the length of the money run**, because the APPROVED and PAID
transitions are owner-only and no combination could be proven end to end without one. It carried the
marker, sat in the ledger, and is gone.

---

## 9. Build honesty

**Six production builds, every exit code echoed by hand and never piped through `tail`: 0, 0, 0, 0, 0, 0.**
Clean `tsc` baseline taken on the untouched worktree **before any edit**, exit 0 with
`grep -c "error TS"` = 0, and exit 0 with 0 errors again at the end. Hooks gate **0 errors and 10
warnings** against a ceiling of 11. `eslint` confirmed present, so the gate is a real check.
`check:prisma-bypass` 0 violations.

**The 6 money files plus `tracking.ts` and `campaign-era.ts` are byte-identical by blob OID on BOTH
refs** — against the branch base and against `origin/main` after the merge. BL-844 changed `tracking.ts`
on main; this round's diff does not touch it.

BACKLOG 177 → 178, counted with `grep -c` and never piped to `head`. The merge conflicted only in
`BACKLOG.md` and was resolved by keeping **both** entries in merge order; 0 conflict markers remain.
`checkpoint/BL-723` confirmed not an ancestor. Worktree `C:/w845` removed.

**Requires a Railway REDEPLOY.**
