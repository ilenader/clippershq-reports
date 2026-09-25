# BL-933 — object-level authorisation, production errors, the down-signal, and the reminder flood

**Shipped 2026-09-25.** Branch `checkpoint/BL-933` (0d17b7f0), merged to main as 73d7e31d.
Rollback: `git reset --hard pre-merge-BL-933` (no schema, no SQL to undo).

**Model split.** Opus judged every finding, wrote every fix and this report. A cheaper subagent read-mapped the route tree (READ); every request result below was measured live (VERIFIED). At most one database connection was held at a time; subagents opened none. No vendor call, no Apify actor.

## The ranked list: found, fixed, left

| # | Item | State |
|---|---|---|
| 1 | `/api/health` returned ok without touching the database (BL-855, never fixed) | **FIXED** |
| 2 | No alert path independent of the database and email (BL-872) | **BUILT** |
| 3 | Payout reminders re-fired every 6h per payout forever | **FIXED (daily digest)** |
| 4 | `TRACKING_RECALC_FAIL`: deadlock on the tracking recompute, 8 people/14 days | **NAMED, LEFT (money path)** |
| 5 | Object-level authorisation across 25 id-routes | **TESTED, 0 leaks** |

## PART 1: object-level authorisation, by request
Enumerated (grep -c): 111 dynamic id-path routes, 34 reading an id from the query, 28 from the body. Two sandbox clippers, A and B, were created, each owning a clip, an account, a payout, a v1 submission and listing, a v2 maker clip, a v2 post and a side request. Signed in as A, against a **local** production build, 25 routes that address one of B's objects were requested: read, update, delete and action.

**Result: 0 private-data leaks. 0 cases of A's own data returned for B's id. B's objects were all intact after every mutate attempt. No response was a 429.** 13 routes refused with 404, 6 with 403.

Three routes returned 200:
* two GETs (a marketplace listing detail page and a marketplace catalogue clip page) are **public browse surfaces by design** — a listing is an advert and a catalogue clip is what a poster posts. Their bodies were checked field by field: every CPM, `ownerCpm`, `clientName`, `aiKnowledge` and `agencyFee` is stripped for a non-owner viewer. This is the marketplace working, not a leak.
* one POST (favouriting a listing) is a normal action on a public listing.

The remaining id-routes are role-gated staff tooling (already covered by BL-875's role tests) or campaign-scoped, and were read-mapped into four safe patterns (ownership-scoped query, role gate, hybrid owner-or-role check, self-scoped record).

**No guard was added.** There is no hole to keep from regressing, and a generic "reads an object by id without a caller scope" guard would flag the many legitimate public-browse and staff routes, trading a real signal for a noisy one. This is stated so a later round does not read the absence as an oversight.

## PART 2: what is failing in production that nobody reads
Ranked by distinct people over 14 days, from the platform's own `audit_logs` and `activity_events`:
* **`TRACKING_RECALC_FAIL` — 8 people, 10 times.** A `prisma.clip.update()` in the tracking recompute fails with `P2034` (a write conflict / deadlock) after 6 retries and gives up. The person sees stale views/earnings on that clip until the next tick recomputes it. It is on the **money recompute path**, so it is named and left, not fixed here; it needs a design decision on serialization or retry.
* Everything else was an ordinary user refusal (a duplicate post 409, a side-locked submit 403, a role-choice 404) or an unauthenticated 401. None is a bug.

**Sentry could not be read here:** the DSN is a write-only ingest key, not a read key, and the dashboard needs its own login. The owner reads recurring errors at sentry.io for this project.

## PART 3: can the platform tell anyone it is down
* **The health check now tells the truth.** `/api/health` was returning `{ ok: true }` without ever touching the database, which is the exact shape BL-855 measured hiding a 24h11m outage. It now runs `SELECT 1` with a 2-second cap, returns 200 `{ ok: true }` when the database answers and **503 `{ ok: false }` when it does not**, leaking nothing (no error text, no stack, no schema). Proven both ways: 200 against the live database, and 503 against a build pointed at an unreachable database, with zero forbidden tokens in the body.
* **An alert path that does not depend on the database or on email.** `src/lib/independent-alert.ts` posts one Discord message through the bot the platform already has, reaching Discord directly so it works when the database and the mail provider are the things that failed. Guards against becoming a second flood: a kill switch (`INDEPENDENT_ALERTS_ENABLED=false`), a 30-minute cooldown per alert kind held in memory, and a no-op when no bot token is configured. **Trigger:** the health check's database read fails. **Rate:** at most one message per 30 minutes per container. Proven with a stubbed sender (send once, cooldown blocks the next, fires again after 30 min, kill switch silences it, no token sends nothing).
* **HikerAPI balance:** not read this round, because a stray vendor call spends real money (BL-929 spent 483 by accident) and HikerAPI's balance is finite. BL-930 read the balance from the vendor dashboard. Whether a free balance endpoint exists must be verified before wiring a low-balance warning onto this path; it is not guessed here.
* **The owner's one external step:** point a free uptime monitor (for example UptimeRobot's free tier) at `https://clipershq.com/api/health` and have it alert when the response status is not 200. Nothing inside a system can report that system being down; this is the outside observer.

## PART 4: the reminder flood
Measured before: about 30 overdue-reminder notifications a day (5 payouts past their deadline, each re-firing every 6 hours, fanned out to 3 owners). The catch-up had measured 189 of 210 owner alerts in 37 hours as these repeats, burying every real alert.

**Changed:** the first OVERDUE notice for a payout still fires once, when it crosses its deadline. The six-hourly repeats are gone; in their place a **single daily digest** per owner lists every overdue payout, its amount and how late it is, once per UTC day. Expected after: about 3 notifications a day (one digest to each of 3 owners), no matter how many payouts are overdue.

What a payout is, when it is due and who can pay it are unchanged; only how often the owner is told changed. The `PAYOUT_REMINDERS_ENABLED` kill switch still works. Proven with mocks, so no real owner notification was written: the first-overdue still fires, a repeat no longer does, the pre-overdue ladder is untouched, the digest lists count/amount/lateness, it writes no payout row, and a second run the same day sends nothing.

## PART 5: safety
* **Money untouched:** the 6 money files are byte-identical by blob OID; the reminder change reads `amount` for display only and writes nothing to a payout.
* **Invariants:** 11 of 11 across the full population after teardown, including both reconciliation forms (0 rows each), no campaign over budget, and ANGIE BROWN at a $2,700 budget.
* **No `.tsx` changed,** so no render pass was run.
* **Sandbox:** 21 prefixed rows, all ledgered, torn down; a sweep of 343 id columns found 0 remaining. No real row was touched. The snapshot's small deltas (+1 user, +6 notifications, +$0.01 in clip earnings) are real production activity during the run, none of it from this round; `sbx_rows` was 0 at open and close.
* **Build:** tsc clean, `BUILD_EXIT=0` on every build; the merge tree equals the branch tree; pushes to the branch and main were verified; tags `pre-BL-933`, `post-BL-933`, `pre-merge-BL-933`, `post-merge-BL-933`; BACKLOG 239 to 240; `checkpoint/BL-723` not merged; the worktree was removed and confirmed gone.

**Left for later:** the `TRACKING_RECALC_FAIL` deadlock (money path, needs a serialization or retry decision); a verified free HikerAPI balance read, to wire a low-balance warning onto the new alert path.

**Object-level access: 25 id-taking routes were request-tested as clipper A against clipper B, and 0 leaked.**
