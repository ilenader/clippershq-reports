# BL-905 — live sweep before launch. AUDIT ONLY.

**Verdict: nothing is broken, and nothing can happen.** The marketplace is safe, guarded and
correct, and completely empty. No campaign is opted into it, so the launch it waits for cannot
produce a single action by anybody.

**Changed nothing.** No code, schema, data, config or flag. Read-only SQL plus GETs against a
local production build on the live database. Peak use was ONE pooled connection
(`connection_limit=1`, pgbouncer 6543); the server ran under four minutes, stopped by its
port-derived PID. No Apify actor, no vendor call, no .tsx changed.

## PART 1 — the owner's question, answered by request

**Can an ordinary clipper see the Marketplace test campaign? NO.**

Proven as a real signed-in CLIPPER, `isTestUser` read from his row and never minted (BL-904's
mistake was minting the very flag the filter reads):

| request | ordinary clipper | owner |
| --- | --- | --- |
| `/api/marketplace-v2/campaigns` | 200, **0 campaigns** | 200, 1 — the test campaign |
| `/api/marketplace-v2/poster/campaigns` | 200, **0 campaigns** | 200, 1 — the test campaign |
| `/api/marketplace-v2/catalogue` | 200, 0 clips | 200, 0 clips |
| `/api/campaigns` | 200, 3, **test campaign absent** | 200, 6, test campaign present |
| `/api/marketplace-v2/catalogue/<test id>` direct | **404** | 404 |

**He sees it because he is the owner, by design.** `filterTestCampaigns` returns `{}` for
`role === "OWNER"` (`test-campaigns.ts:38`); BL-892 built it that way and BL-904 applied it to the
marketplace. The direct route by id is refused too, per BL-888. Nothing needs fixing: the filter
is applied at all 13 clipper-facing campaign sites.

## PART 2 — the first five minutes

An arriving clipper reaches `/market` (200, title "The marketplace — Clippers HQ"), is told to
pick a side (`needsToChoose: true`), picks one, and then the **maker** sees "No campaigns are
open to the marketplace yet." and the **poster** sees "No clips to post yet. Check back soon. New
clips show up here as soon as the owner approves them."

Both empty states are real, accurate copy, so he is not facing a blank screen. But **whichever
side he picks there is nothing to do**, and the poster copy misleads: it promises clips once the
owner approves them, when no maker can create one either.

## PART 3 — guards

`npm run build` clean, exit 0, 0 TypeScript errors, all 18 prebuild steps pass. Schema-drift
verified 101 tables / 1,225 columns / 142 uniqueness constraints, no drift. `check:budget-lock`
B8 re-confirms **on live main** that BL-901's row lock is taken before the committed spend is
read (offsets 4510 then 4694); B9 confirms the floored maker leg is still the summand.
`lint:hooks`: **0 errors, 11 warnings against a cap of 11** — correct, zero headroom.

## PART 4 — first-day risks, ranked

1. **Nobody tells the owner a maker submitted.** `createV2Clip`
   (`marketplace-v2-catalogue.ts:216`) writes a `PENDING` row and returns. No email, no Discord,
   no notification. *First symptom:* a maker submits and hears nothing. *Would anyone notice?*
   Only the maker, by waiting. *Where he looks:* nowhere — he must decide to go look. It matters
   more than on v1 because **his approval gates the entire poster side**: no approved clip means
   an empty catalogue and idle posters. The v1 queue shows the pattern — 40 pending, 35 older
   than a day, oldest 3 days 8 hours.
2. **The hooks gate has no headroom.** 11 warnings against a cap of 11. The next hook warning
   anybody adds fails `prebuild`, which fails the Railway deploy. *First symptom:* a routine
   deploy fails on a warning, during a launch.
3. **Alerts cannot report a dead database.** The watchdog decides and delivers through
   `db.notification` rows, so if Postgres is what is down, nothing fires. Pre-existing, but the
   failure a launch is least able to absorb.
4. **`setPosterState` has no test-campaign check** (`marketplace-v2-poster.ts:611`: the lookup is
   `{ id, status: "APPROVED" }` only). Every other poster path filters. It writes a state row
   only — no money, no visibility — so it is cosmetic, and the single gap in the whole sweep.

**The one alert worth setting up:** a v2 clip sitting `PENDING` beyond a few hours. It is the only
queue whose latency stalls both sides at once, and nothing watches it (the watchdog mentions the
v2 marketplace zero times).

## PART 5 — verdict

**Today's blocker, and it is the only one:** no real campaign is opted into the marketplace.
`ANGIE BROWN THE REAL ME` ($3,000, ACTIVE, created 2026-09-18) is `campaignType NORMAL`. The only
row satisfying the marketplace filters is still the owner's test campaign, correctly hidden from
everyone else. **Not a defect any round can fix: it is the owner opting a campaign in.** BL-904
named it; it is unchanged. **Later, not today:** the notification gap (it costs nothing until
somebody submits), the hooks headroom, `setPosterState`.

**Nothing is wrong with the money.** 10,202 live clips, 0 invariant violations, 0 negatives. 21
budgeted campaigns, 0 over budget, closest $300 under. Tracking is live: last tick 19:01 UTC, 79
clips in the last hour, 862 in 24h.

**A figure I reported earlier this round was wrong.** I said 4,968 overdue tracking jobs sat on
approved, live, earning clips. Measured properly it is **zero**: the whole overdue backlog sits
on PAST or PAUSED campaigns (4,974 on PAST). It costs nobody money and needs no action.

**Correcting the record, as instructed:** the account holding $248.60 of earnings and $991.11 of
payouts is the owner's own clipper account, **not** flagged `isTestUser` and not a test account.
The brief that first called it one was wrong; BL-904 corrected it and this round confirms it.

**Not built, and still not built:** the owner's dashboard and the unseen-clip badge.
**Every proof of this marketplace is a sandbox proof.** Production census: **0** v2 clips, **0**
posts, **0** side requests, **0** strikes, ever; two people have chosen a side. Not one line of
the maker-to-poster path has run against a real campaign with real money. Everything any round
has demonstrated, mine included, was demonstrated against fixtures.

**Could not be measured:** whether `NEXT_PUBLIC_MARKETPLACE_V2_ENABLED` is true in Railway. No
round can read or set it. I proved the behaviour with the flag forced on locally; if it is off in
production, every finding above is simply deferred until he turns it on.
