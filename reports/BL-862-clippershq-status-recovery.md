# BL-862 — recovering the rounds that finished while the machine was off

**AUDIT ONLY. No code, data, schema or config changed. Nothing merged, nothing deployed.** Worktree `C:/w862`,
branch `checkpoint/BL-862`, from `main` at `3b3c48cc`. Database read 2026-09-09 08:48 UTC, `now()` cast `::text`.

**Collision with BL-861, which is live now:** it holds `C:/w862`'s neighbour `C:/w861` on branch
`checkpoint/BL-861` at the same base commit and it touches payouts. This round writes no file it could conflict
on, works only in `C:/w862`, and its only shared resource is the database, read serially, one query at a time,
never more than one connection, read only. No payout row was written or locked.

**The good news first: nothing was lost. Every round you dispatched produced a report, and all four are safe.**

---

## PART 1 — every report published since 7 September

| published (::text, UTC) | file | which round it really is |
| --- | --- | --- |
| 2026-09-09 00:07:52 | `reports/BL-859-clippershq-pwa-active-use.md` | **BL-859**, the PWA active use rule |
| 2026-09-08 23:51:59 | `reports/BL-1533.md` | **BL-860**, health and launch readiness |
| 2026-09-08 23:13:25 | `reports/BL-1532.md` | **BL-858**, the merge of the streak remedy |
| 2026-09-08 22:49:19 | `reports/BL-1531.md` | **BL-857**, the outage streak remedy |
| 2026-09-08 22:18:48 | `reports/BL-856-clippershq-scaling-sweep.md` | **BL-856**, the scaling sweep |
| 2026-09-08 21:27:14 | `reports/BL-855-clippershq-slowness-diagnosis.md` | **BL-855**, why the site was slow |
| 2026-09-07 20:38:13 | `reports/BL-1530.md` | **BL-853**, the botted payout reject button |
| 2026-09-07 18:58:21 | `reports/BL-854-clippershq-pwa-and-report-entry.md` | **BL-854**, the install bonus review |

**No dispatched round is missing a report.** Nothing was lost to the shutdown.

**One report exists for a round not in your list: BL-855**, published 21:27 on 8 September, the slowness
diagnosis. It is the round that identified the outage as infrastructure rather than a bad merge.

**One thing you may expect and will not find:** there is no separate merge report for BL-859. Its merge is
recorded in the commit on `main` instead. Nothing is missing; it is only filed differently.

---

## PART 2 — what each round did, in plain language

**BL-855, why the site was slow.** Asked to find out why pages were slow and figures wrong. It found the
database had been refusing every connection for more than 27 hours, so this was infrastructure and not a bad
merge, and it cleared four merges you suspected. It changed no code. It left you the conclusion that the
database itself, not the platform, was down.

**BL-856, the scaling sweep.** Asked what will bring the site down as you grow. **Money first: your vendor bill
is about $147 a month today and scales straight with clips, roughly $1,470 a month at ten times the clippers,
and no server upgrade touches it.** It found the admin analytics page burns about 43 seconds of database time
on every single visit, one query reads the entire snapshot table with no limit, and **a live data leak: the
client name and the AI knowledge field reach every clipper on the main campaign list**, which breaks a standing
rule. It also found the tracking cron saturates at roughly 73 new clips a day sustained, fixable with one
environment variable and no redeploy. It changed no code and applied no index. It left you a ranked, costed
plan.

**BL-857 and BL-858, the outage streak remedy.** Asked to protect clippers who could not post during the
outage. It measured the outage from the cron heartbeat at **24 hours 11 minutes, from 19:37 on 7 September**,
and corrected you on the start time. It protected **10 clippers holding 63 streak days**, changed eleven lines
in one file, and merged to `main` at `cc3abf60`. **It is deployed and it worked: six of the seven I checked
today hold and have grown their streaks.** It also found seven other things the outage broke, including a
2 percent bonus seven clippers lost.

**BL-859, the PWA active use rule.** Asked to make the 2 percent app bonus depend on opening the app rather
than merely installing it. **The headline is that the rule was already live, at two days, and nobody had
written it down.** It widened the window to seven days, excluded the outage so nobody is punished for our
downtime, and **fixed a real money defect: the old rule recomputed already earned clips downward, which broke
the promise that earnings never decrease.** That is gone. It merged to `main` at `3b3c48cc`. It left you a
piece of SQL to run if you want to restore the people the old rule stripped, printed rather than executed.

**BL-860, health and launch readiness.** Asked for a real health check, the cron ceiling and a launch verdict.
**Money and urgency first: a real clipper has been waiting 96 days for $52.40 and no automated watcher on this
platform can see them, and six of your twelve in flight payouts are overdue today.** It confirmed the health
endpoint returns ok without touching the database, so it stayed green for the whole outage. It corrected two of
its own alarming first readings: the tracking backlog is 1,316 and not 6,783, and **no clip that can still earn
is going unpolled.** It found only three scheduled jobs have ever run in the platform's history, that about
thirty five endpoints show zeros instead of errors so the site looked healthy while it was down, and that the
storage gauge has been pinned at 100 percent for some time. It changed no code. It gave a straight launch
verdict, in PART 5 below.

---

## PART 3 — what is on main, and what is not

| round | state |
| --- | --- |
| BL-855 | **unmerged on origin** |
| BL-856 | **unmerged on origin** |
| BL-857 | **merged** into `main` at `cc3abf60` |
| BL-859 | **merged** into `main` at `3b3c48cc` |
| BL-860 | **unmerged on origin** |

**The three unmerged branches, and merging them changes nothing about how the site behaves:**

| branch | SHA | what merging it would do |
| --- | --- | --- |
| `checkpoint/BL-855` | `cbad2858` | adds two read only diagnostic scripts. No product code |
| `checkpoint/BL-856` | `5da07214` | adds one file of watch queries. No product code |
| `checkpoint/BL-860` | `fece1fe0` | adds the health and launch report as a file. No product code |

**Railway redeploy: the one after the streak remedy DID happen, and it is proven.** Six of the seven clippers
BL-857 protected hold and have grown their streaks today, which only occurs if that code is live.

**What is not proven is whether the deploy also carries BL-859**, which merged at 00:07 this morning, after
that. Nothing readable from here settles it. **One redeploy now is harmless and removes the doubt.** Until it
is certain, the seven who lost the app bonus could be stripped again by the old two day rule.

---

## PART 4 — the decisions waiting on you, with today's figures

**1. The 96 day payout. THIS IS THE URGENT ONE.** Still open today at **96.3 days**, still with no deadline
stamped, still invisible to every reminder and every counter. Five more sit overdue in REQUESTED and one in
APPROVED, so **six of twelve in flight payouts are overdue right now.** Options: pay it, or reject it.
**If you do nothing, nothing on this platform will ever raise it and the person keeps waiting.**

**2. The seven who lost the app bonus. This has largely resolved itself.** Today **all seven hold the bonus
again.** Two reopened the app; the other five sit 2.70 to 3.54 days idle, inside the new seven day window.
Platform wide, only **one** clipper is now in the stripped state the restore SQL was written for, against nine
when BL-859 measured. The money was always small, about **$1.56** as a scale marker across everything those
seven have ever earned. Options: run BL-859's restore SQL for the remaining one, or leave it, since they regain
it the moment they open the app. **If you do nothing, one clipper stays 2 percent short until they next open
the app.** The real risk here is not the SQL, it is the redeploy in PART 3.

**3. The bonus dilution question, still undecided.** A $100 marketplace clip could disburse $127 in the worst
case. **Cost so far today: $0.00**, because marketplace submissions, clip posts and both earnings tables all
read **zero** right now. Analysis says you realise below 10 percent in 99.312 percent of cases, median 8.99
percent, and the reachable worst case is $122.50 rather than $127. Options: cap it, accept it, or write down
that you accept it. **If you do nothing, the first real marketplace clip settles it by default.** It is still
free to decide.

**4. Archived campaign pending clips. There are none.** Measured today: **zero** pending clips sit on an
archived campaign. The only pending clips are 92 on active campaigns and 2 on paused ones. **Nothing to
decide.**

**5. Turn on failure notification for the cron ping you already have.** Not really a decision, but it is on
you rather than on code. Two minutes, in an account you already own, no deploy. **It would have cut the 24 hour
blind outage to about twenty minutes.** If you do nothing, the next total outage is again invisible until a
clipper complains.

**6. Enable two scheduled jobs that have never run.** One environment variable. If you do nothing, 787 dead
tracking jobs keep inflating the queue and notifications grow without limit.

**7. The clipper whose streak did not survive.** One of the seven I checked reads a streak of **0** with a last
active date of 7 September. I cannot tell from a read only query whether they were evaluated before the
redeploy or whether the remedy simply does not reach them. **Worth one look.**

---

## PART 5 — the launch answer

**BL-860 completed and it gave a verdict.**

**Marketplace: no to a general launch. Yes to a one slot watched pilot.** Measured again today, everything
still reads zero: no submissions, no posts, no creator earnings, no platform earnings, one listing. The first
real user is the first real test. Before a pilot: redeploy, and keep it to one poster you can telephone, one
listing, one slot, one creator, and a campaign capped at $20 or less per clip so any arithmetic error is
bounded. Do not press Adjust on a marketplace payout and do not use fix budget during the pilot. One caution
worth repeating: the source claims every marketplace earnings write goes through a single door and **that claim
is false**, only about two of fourteen sites are routed through it.

**Trainer: yes, with exactly one trainer, after two fixes that take ten minutes.** Measured today: **zero
trainers, zero pairings, zero commissions.** The money path is complete and correct end to end and nothing
touches clip earnings. What is missing is arrival: a promoted trainer is told nothing, and the trainer page has
no link anywhere in the app, so you are currently the only way anyone finds their own balance.

---

## PART 6 — what to do next, worst first

| # | do this | type |
| --- | --- | --- |
| 1 | Open the 96 day payout and either pay or reject it | **decision** |
| 2 | Turn on failure notification for the existing cron ping | **decision**, two minutes |
| 3 | Redeploy Railway once, to be certain BL-859 is live | **redeploy** |
| 4 | Close the client name and AI knowledge leak on the campaign list | **new round** |
| 5 | Decide the bonus dilution question in writing before any marketplace pilot | **decision** |
| 6 | Enable the two scheduled jobs that have never run | **decision**, one env var |
| 7 | Add the real health check and point a monitor at it | **new round**, then four clicks |
| 8 | Fix the analytics page query and the unlimited snapshot fetch | **new round** |
| 9 | Add a trainer link and a promote notification, then start one trainer | **new round** |
| 10 | Merge BL-855, BL-856 and BL-860 for the record, or leave them | **merge**, optional, no behaviour change |

---

## Honesty notes

**Could not be established:** whether the current Railway build carries BL-859. The streak evidence proves a
redeploy after BL-857 and no further. **Not re-derived:** every finding above is quoted from its own round's
report; nothing was re-measured except the figures explicitly marked as today's. **Measured today:** the PWA
flag state of the seven, the platform wide restorable count, the pending clips by campaign status, the in
flight payout ages, the marketplace and trainer counts, and the streaks of seven protected clippers.

No handle, wallet address or key appears above. Short ids only where a person had to be identified.
