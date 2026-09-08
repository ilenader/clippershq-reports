# BL-855 — why the site is slow and showing wrong numbers

**AUDIT ONLY. Nothing was changed. No fix was performed. Branch `checkpoint/BL-855` at `cbad2858`.**

---

## The one line

**Your database has been refusing every connection for over 27 hours, so this is infrastructure and not a
merge: nothing recent touched the connection layer, and the four merges you suspected most were live and
healthy for hours before it broke.**

---

## PART 4 first, because it answered the question and stopped the round early

I checked infrastructure before code, as the brief says to.

| check | result |
| --- | --- |
| `run-select.js` through the pooler | **FAILS.** `ECHECKOUTTIMEOUT ... after 15000ms in Session mode`, then `authentication did not complete within 15000ms` |
| A probe past the pooler on `DIRECT_URL` | **FAILS.** `EAUTHQUERY: authentication query failed: connection to database not available` |
| TCP to the pooler, port 6543 | **OPEN, 124 ms** |
| TCP to the direct port 5432 | **OPEN, 32 ms** |
| The project's own REST endpoint | **HTTP 401 in 312 ms**, the correct answer to a bogus key, so the project is UP |
| Connections held from this machine | **0 established.** Only `TIME_WAIT` from my own probes |
| Stray dev server on ports 3000 to 3899 | **none listening** |
| Leftover worktrees from concurrent rounds | **none.** `C:/w853` and `C:/w854` are gone |

**Seven attempts across two endpoints over the whole round, every one refused, the last at 2026-09-08 19:26
UTC.** The last time this database was confirmed healthy is **`2026-09-07 16:15:04.411905+00`**. That is a
**sustained outage of more than 27 hours**, not a momentary spike.

**Read the combination carefully, because it is specific.** The network is fine, the pooler answers in 124 ms,
and the project answers in 312 ms. What fails is the pooler reaching the database behind it, and the error says
so in as many words: **"connection to database not available"**.

**This is precisely the symptom you described.** A database that cannot be reached makes every page slow,
because each one waits out its timeouts, and makes figures wrong, because a page renders from whichever reads
happened to succeed and shows stale or missing numbers for the rest. **Slow and wrong together is the signature
of this fault, not of a bad calculation.**

**And 27 hours changes the diagnosis.** A saturated pool clears itself within minutes as backends time out.
Something that has not answered in over a day is not a spike: it points at the project being **paused,
suspended, or over a hard quota**, with the API gateway left running in front of it. That is the first thing to
look at.

## What I could NOT measure, stated rather than invented

**PART 2 and PART 3 are not measurable while this is happening, and I did not fake them.** Load times, request
counts and query counts taken now would measure the outage rather than any regression, and comparing displayed
figures against the database requires reading the database, which no client can currently do. Numbers produced
in this state would have sent you after the wrong thing.

**What I did instead was clear the specific code paths you named, by reading their diffs.**

## PART 1 — the dating, and it exonerates four of your six suspects

| merge | deployed (UTC) | live while the database was proven healthy? |
| --- | --- | --- |
| BL-847 `eb825971` | 2026-09-06 21:26:22 | **yes, excluded** |
| BL-849 `f1833ffe` | 2026-09-07 09:11:17 | **yes, excluded** |
| BL-850 `f6a418ad` | 2026-09-07 11:38:04 | **yes, excluded** |
| BL-851 `2c108cd3` | 2026-09-07 13:07:59 | **yes, excluded** |
| BL-852 `ee15936d` | 2026-09-07 16:25:45 | after the last healthy reading |
| BL-854 `d276c746`, `84e08ac7` | 2026-09-07 16:32:41, 16:47:23 | after |
| BL-853 `b2475636` | 2026-09-07 18:37:36 | after |

**BL-849, BL-850, BL-847 and BL-851 are excluded by measurement rather than by argument.** All four were
deployed and several hundred queries ran successfully against the live database while they were, right up to
16:15:04 UTC. **BL-849 is the one that touched a money file, and it is cleared.**

**The timing does not point at any single one of the remaining three, and I will not pretend it does.** It only
narrows the window to after 16:15 UTC. What decides it is the next section.

**Three corrections to the brief, each measured:**

1. **`BL-1528` does not exist in this repository.** `grep -c` over every ref returns **0**. The bonus
   corrections round is **BL-851** at `2c108cd3`.
2. **The newest merge is not BL-854.** It is **BL-853 at `b2475636`**, merged 2026-09-07 18:37:36 UTC, which
   landed after your brief was written.
3. **BL-850 did not hide 29 of 34 campaigns.** It fixed that; the hiding was pre-existing.

## The code side, cleared on the record

**No recent merge touched the connection layer.** The only two real `new PrismaClient` sites in `src/` are the
singletons at **`src/lib/db.ts:110`** and **`src/lib/db-cron.ts:85`**, and **both files last changed on
2026-06-04**, in BL-116, the round that right-sized the pool. `npm run check:prisma-bypass` reports **0
violations**, so nothing recent added an unmarked client. Ceilings are **`max: 48`** for web at
`src/lib/db.ts:107` and **`max: 10`** for cron at `src/lib/db-cron.ts:82`.

**BL-853 is cleared on both counts, and it was the best code-side candidate, being newest and touching a hot
read path.** Its change to `src/app/api/earnings/route.ts` adds **one field to an existing `select` and one
`.filter().length` over an array that was already fetched**. No new query, no N+1. Its migration
`scripts/migrations/BL-853-CLIP-REJECTION-CODE.sql` is one nullable column and one partial index on a 9,600 row
table.

**It is NOT a third instance of the client-side-filter defect**, which you asked me to look for. The new
`fakeViewClips` count filters a set fetched with `take: 5000` at **`src/app/api/earnings/route.ts:142`**, scoped
to one clipper whose largest peer holds 870 clips, so the cap is nowhere near reached, and it renders as a
sentence only when above zero, never as a number beside a filter.

**One thing I will not exempt because it is mine.** BL-852 added a `groupBy` to `/api/trainer/me`. It is one
query, guarded on `pairings.length > 0`, and **production holds zero pairings**, so it has never executed once.

## PART 5 — the verdict, and exactly what to do

**Verdict: the Postgres instance is not accepting connections and has not for over 27 hours. The pooler and the
project are healthy; the database behind them is not. No code change caused this and no revert will fix it.**

**A revert is the wrong answer and would cost you something for nothing.** Reverting BL-853 removes the bot
rejection action and the fake-views count; BL-854 removes the Help report entry and the marketplace pointer;
BL-852 takes the trainer code entry away again. **None of them can stop a database accepting connections**, and
you would still be down afterwards.

**What to do, in this order:**

1. **Open the Supabase dashboard for this project and look at the database's status first.** After 27 hours the
   likeliest answer is that it is **paused, suspended, or over a quota**, with a banner saying so. If there is a
   Resume or Restore button, that is the fix.
2. **If it is running, go to Reports then Database** and read the connection count against your ceiling. Pinned
   at the top means saturation, and **Settings, Database, Restart** clears every leaked backend at once.
3. **Then check Railway for how many instances are running.** This is the part most likely to be the underlying
   cause rather than the symptom. Web is configured for **48** connections per instance plus **10** for cron,
   which is **58 on one instance and 116 on two**. If Railway has scaled to more than one replica, or an old
   deployment is still running beside the new one, that alone explains this with no code being wrong.
4. **Check the billing or usage page for a hard limit reached**, since a project over quota presents exactly
   this way: gateway up, database unreachable.

**What must be proven once it is back:** run `node scripts/run-select.js "SELECT now()::text"` and confirm it
answers. **Only then** is PART 2 and PART 3 worth measuring, because until the database answers, every load time
and every figure on every page is a measurement of this outage.

**If it comes back and the numbers are still wrong, that is a second and separate round**, and it should start by
measuring the clips page against BL-816's recorded 51 requests and 4.0 seconds, and the cold launch against
BL-829's 11.6 seconds. I did not measure them here because doing so now would have produced a number I would
have had to retract.

---

## Honesty notes

**No build was run in this round and none is claimed.** No data, code or config was changed and nothing was
fixed. Two read-only probe scripts were committed on the branch, `scripts/bl855-pool.ts` and
`scripts/bl855-reach.mjs`; the second prints host names redacted and **neither ever prints a connection
string**. Every timestamp above is either the database's own `now()` cast to `::text` or a git committer date
converted to UTC. No handle is named and no wallet address was read. **No subagent was used, no sandbox was
built and the repository was not explored broadly**, as the budget required. The worktree `C:/w855` was removed
and verified gone.
