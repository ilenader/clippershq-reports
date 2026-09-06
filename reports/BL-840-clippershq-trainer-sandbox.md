# BL-840 — the trainer system, run for real, then removed without trace

**Nothing was left behind.** 140 rows created, 139 deleted and 1 taken by a cascade, 0 remaining
across 19 separate scans. No removal SQL is needed and none is owed.

Round of 2026-09-06. Merged to `main` at `febfc88`. **Requires a Railway REDEPLOY.** Handles redacted.

## Your own example, on a real payout row

BL-835 built this and said plainly its arithmetic was proven on the pure functions and **not** by
creating a real payout. Nobody had used it since: 0 trainers, 0 pairings, 0 commissions. This round
created the payouts. A **$1,000** withdrawal by a trained clipper with no referrer:

| | |
|---|---|
| platform takes 9% | **$90.00** |
| what remains | **$910.00** |
| trainer takes 10% of that | **$91.00** |
| **the clipper receives** | **$819.00** |
| trainer pays 9% on his own share | $8.19, leaving **$82.81** |

Every figure was worked out by hand from your rule **first**, then compared: a test whose expectation
comes from the code it tests only proves the code agrees with itself.

## All four combinations, and every cent accounted for, in 56 checks

| case | gross | fee | express | trainer cut | clipper cash |
|---|---|---|---|---|---|
| trainer, no referrer | $1,000.00 | $90.00 | none | **$91.00** | **$819.00** |
| trainer **and a referrer** | $200.00 | $8.00 | none | **$13.65** | **$178.35** |
| trainer **and express** | $100.00 | $9.00 | $4.00 | **$9.10** | **$77.90** |
| **no trainer** (the control) | $100.00 | $9.00 | none | none | **$91.00** |

Across all four: $1,400.00 gross became $1,166.25 clipper cash, $116.00 platform fee, $4.00 express
and $113.75 trainer accrual. **Cash plus cut plus fee plus express equals the gross exactly**, on
every row and in total. The platform never gained a cent from nowhere.

The referred clipper's trainer takes the same base as an unreferred one, so nobody is charged more for
how they arrived. **The referrer was held harmless at $9.60** rather than the $8.92 a naive
calculation would have paid him because his invitee chose a coach. And the control clipper's row
carries **nothing at all** in the four trainer columns, so it is indistinguishable from a row written
before the feature existed.

## What happens when things go wrong, in 37 checks

| case | what happened |
|---|---|
| clip **rejected** after earning and after payment | earnings zeroed, trainer's money **not** clawed back |
| clip **deleted** after earning | soft delete only. **It does not zero the earnings**, worth your knowing |
| clip deleted **after payment** | the paid row untouched, to the cent and the status |
| **good-terms exit** through the appeal | the 10% **continues** at exactly $4.10, on $45.00 eligible not $60.00 |
| **bad-faith revoke** | $13.65 wiped and refunded to the clipper. The preview wrote nothing |
| **good-terms wind-down** | the trainer **kept** $91.00, nothing refunded |
| **partial revoke** | one trainee ended, the other three untouched |
| **trainer goes silent** | no cut at all on the next withdrawal, clipper kept the whole $18.20 |

Two early failures were my test aiming at the wrong clipper, and the platform was right: a withdrawal
was refused because that clipper had been paid $60 and then had a $30 clip deleted, so his record sits
below his payments. That is your no-overpayment rule and your paid-is-final rule both working.

## Three things that were broken, now fixed

**1. Every clipper's browser was receiving your test campaigns.** `/api/campaigns/spend` had no test
filter of any kind, so the id and the total spend of every test campaign went to everyone signed in.
Nothing drew it, but it left the building. This is **not** a sandbox problem: it was already true, and
your own rules already said clippers cannot have that endpoint in full. Now a clipper sees **0 of 2**
test campaigns and you still see the one that has spend.

**2. A trainer's screen showed "0 clips" beside "$91 earned from them".** The dashboard used the rule
that decides what to *charge for* to decide what to *show*, so when a pairing ended the work vanished
while the money stayed. Only visible once a pairing ends, which is why nobody had seen it. Fixed
without touching the money.

**3. Taking trainer status back would not have cleared the new grant**, so giving it back later would
have silently restored a view you thought you had removed.

## The addition you asked for

A trainer can now be granted the **views, likes and comments** on each clip they already see. **Off by
default.** It shows three numbers and nothing else: no money, no campaign name, no rates, no clipper
id, proven by 16 forbidden field names being absent from the real response. A clip we have never
checked reads **"Not measured"**, never 0. Turning it on **tells every clipper it affects**, and their
own page now always lists what their trainer can see today. The accessibility review returned **nine
blocking items and every one was built**, including telling clippers who joined *before* the change,
and bumping the consent record so it cannot claim they agreed to a list they never saw.

## Two things you should know

**A silent trainer takes two presses, not one.** You said the 10% should stop "entirely including
accrued-but-unpaid". Taking trainer status back stops all future cuts immediately but does **not** wipe
what is already accrued ($14.11 in the test). Ending each pairing does that, and refunds it to the
clipper. Those two were separated deliberately when the system was built.

**A trainer still cannot be paid.** There is no cashout route anywhere in the product, so nothing can
turn an accrued commission into money. The accrual, the ledger and the refunds all work; the last step
does not exist. Building it is its own round, and the shape was already specified.

## Nothing real was touched

Every table only the sandbox could move is **exactly** what it was: 1,672 users, 34 campaigns, 220
payouts, 9 adjustments, 1,476 accounts, 7 referral commissions, 8 clip-limit overrides. The payout
fingerprint and the user fingerprint are **byte-identical** before and after, and the earnings
invariant was at **0 violations** throughout. What did move is named: **4 clips from 2 real clippers**
and **508 view snapshots from the tracking cron**. Zero signups, zero payouts. None of it mine.

## The sandbox is reusable, and cannot be aimed at real data by accident

It lives in `scripts/sandbox/` with a README. Four locks must all agree before one row is deleted,
there is no delete by pattern or name or date anywhere in it, and the ledger of what it created lives
**outside** the repository, so a fresh clone has nothing to act on. Replace two files to point it at
the marketplace.

**To undo this round:** `git revert -m 1 <merge>` or `git reset --hard pre-BL-840`. The one column
added is defaulted off; reverting the code alone leaves it read by nothing.
