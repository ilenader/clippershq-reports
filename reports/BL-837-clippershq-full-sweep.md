# BL-837 — I walked the whole platform, and here is what was broken

Round of 2026-09-04. Branch `checkpoint/BL-837`, merged to `main`. **Requires a Railway REDEPLOY.**
Handles are redacted. Every timestamp is the database's own `now()`, cast to text.

## 1. Your audit trail was being destroyed, quietly

`audit_logs.userId` said "set it to null when a user is deleted" in the schema and said **CASCADE** in
the live database. Deleting a user therefore **erased their history** instead of keeping it.

I proved it before touching anything: three audit rows for a throwaway account, account hard-deleted,
`0 of 3 survived`. After the fix, on the same test: `3 of 3 survived`, all three orphaned rather than
erased, and the table back to its exact prior count both times.

**Nothing real was lost.** The 15 audit rows pointing at users who no longer exist all pointed at test
fixtures from last round. Your 39 soft-deleted users kept every row, because a soft delete never fired
the rule. A drift checker now compares all 137 declared rules against the live database: `NO DRIFT`.

One table was deliberately left alone. `reviewer_audit_log` refuses updates AND deletes by design, so
a delete is simply blocked and the 3,482-row reviewer trail is protected. That is already correct.

## 2. Your pending clips: the filter was lying to you

The Status chip filtered **the thirty rows already on your screen**, not the database. 57 pending clips
existed. 10 were in the newest 30. The deepest one sat at position 7,318, which is **244 presses of
"Load more"**. That is why the dashboard said clips were waiting and the queue looked nearly empty.

The chip now narrows the database, and Pending carries Flagged with it, because a flagged clip is still
waiting for your decision. Proven by 31 direct requests, 0 failures: the totals match the database
exactly, every reachable pending clip is on page one, and paging returns each row exactly once.

A reviewer still cannot use this to reach decided clips. I attacked my own change and it held.

## 3. Three screens told you "nothing here" when they meant "it broke"

Your clip queue, a clipper's own list, and Agency Earnings all answered a database failure with an
empty success. An empty queue and a broken queue looked **identical**.

All three now say so plainly. I proved it against a database that was **actually down**, by running a
second copy of the site pointed at a dead port: 7 checks, 0 failures, and your live database was never
touched by that test.

## 4. What looking at the screen caught that no test did

The new error message sat directly above a button reading "Loading more clips". Worse, that was a
**retry loop I had just introduced**: the page kept asking a failing database for more. The whole block
is now hidden while the error stands. 45 checks across five screen sizes in the broken state, 12 more
in the working state, 0 failures, no sideways scrolling anywhere.

## 5. Numbers that were wrong

- **Agency Earnings was capped at 500 rows** and understated by **$884.51**, 8.8 percent. Now uncapped.
- **The payouts "Send" figure showed the gross amount on 11 adjusted rows**: $995.34 shown where
  $937.79 was correct. It now re-derives through the same code that builds the real payout.
- Two "Total Paid" labels now say "Total Paid (gross)", because fees still come off that number.
- The sidebar's pending badge was counting 5 deleted test rows.

## 6. Found, and deliberately NOT fixed, each for a reason

- **A fourth place derives what a clipper can withdraw and skips your paid-is-final rule.** $3,416.06
  across 23 clippers, on 1 open payout row. It is a money path. It deserves its own round, not a sweep.
- **2 pending clips sit on archived campaigns and cannot be reached at any page.** The queue hides
  archived campaigns; the dashboard counts them. Which one is right is **your call**, not mine.
- An ADMIN sees only the newest 500 clips with no way to load more.
- Command Center's six money tiles show 0 when they fail, and cache that 0 for five minutes.
- "Paid to clippers" is actually approved earnings, and "Your profit" is gross revenue.
- A clipper's own clip list is built in a way that hands him every future column automatically. Today
  that is harmless. Narrowing it can silently blank a field his page already shows, so it waits.

## 7. Your money did not move

Across the **whole** population, before and after: earnings invariant **0 violations**; **0** clippers
holding two open payouts on one campaign; the 18 historical over-payable holders unchanged and not
grown; every payout count and total identical; **no clip's status changed**. The six money files plus
tracking, era, payout-calc, apify and the reassignment route and dialog are **byte-identical** by blob
id on both branches. The paid-is-final guard passes 14 of 14. Campaign creation is still owner-only,
the capability gate still refuses, and the partner scope still narrows: 18 requests, 0 failures.

Earnings rose $61.70 with the approved count unchanged and **0 clips reviewed**, because the tracker
took new snapshots on 187 already-approved clips. Four new clips arrived and one clipper signed up.
That is your platform working, not this round.

## 8. What I could not do, stated plainly

- **Your database connection pool was already failing before I started**: three errors against your own
  live session at 17:12 to 17:13 UTC. Two more appeared at 18:00:50 and 18:06:32. The first is before
  my server existed at 18:02:33; the second is inside my window, so **I cannot rule out that I
  contributed to it**. Every test request was sequential and both servers were stopped immediately.
- The **ADMIN branch** of the campaign-creation gate could not be tested live, because **zero accounts
  hold ADMIN**. It is covered by the rule's shape, not by a request.
- Four checks in the old reassignment harness fail on text that later rounds rewrote on purpose. They
  fail **identically on main**, so they are the test ageing, not a break.
- The reversal SQL for the constraint is printed at the top of the migration file and is **lossy in one
  direction**: restoring the old NOT NULL needs a value for any row orphaned since, and there is no way
  to know which user it named.

## 9. To undo it

`git revert -m 1 <merge>` or `git reset --hard pre-BL-837`. The constraint change is separate from the
code, and reverting the code alone leaves it in place doing no harm.
