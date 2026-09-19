# BL-910 — the first day, read rather than reasoned about

**Audit only. Nothing changed.** No code, schema, data, config or flag. **Cap: one pooled
connection at a time** (`connection_limit=1`, pgbouncer), about twenty short read-only queries.
**Two subagents (Sonnet) read reports and source and opened zero database connections**; I ran
every query and judged every finding. Subagent claims are marked READ; every number below I ran.

**One correction to the brief up front:** the campaign budget is **$2,700, not $3,000**. He cut it
by $300 at 19:58:27 on the 18th (`CAMPAIGN_BUDGET_CHANGED`, `oldBudget 3000, newBudget 2700`).
Nothing spent it. He also narrowed the platform from "TikTok, Instagram" to **Instagram** at the
same minute.

## 1. The funnel, measured

Clock at the last query: **2026-09-19 08:18:02 UTC**, **13 hours 10 minutes** after it opened.

| step | people |
| --- | --- |
| emailed in the launch broadcast (19:08 to 19:11) | **1,551** |
| arrived at the marketplace | **19** |
| chose a side | **15** (8 poster, 7 maker) |
| arrived and chose nothing | **4** |
| submitted a clip | **3** |
| posted a clip | **0** |

Fifteen clips from three makers. Seven approved, eight pending, **zero rejected, zero posted**.
People are still arriving: the most recent side choice was 08:12:33 and the most recent arrival
08:12:52, minutes before the last query.

**Why the four did nothing, from what they hit.** One (`67fb39`) opened the campaigns list then the
catalogue at 19:43 and left; **the catalogue was empty then and stayed empty until 07:05 the next
morning**. That one is answered: nothing worth doing. The other three loaded the landing page once
and left, no refusal, no second request. **The data cannot say whether they were confused or
uninterested and I will not invent which.**

**The same explains the eight posters.** First poster chose at 23:35; first approval 07:02 this
morning. Everyone who looked before then saw an empty catalogue. Within forty minutes of the first
approvals three posters opened a clip detail (07:42 to 08:12). **The catalogue has been worth
looking at for seventy minutes**, too short to call anything.

## 2. Every refusal, and the honest reading of it

**The recorder is genuinely writing, which had to be checked because an empty table and a broken
writer look identical.** 198 arrivals from 40 people across 11 surfaces, the most recent **2 minutes
16 seconds** before I looked. 52 refusals from 6 people across 7 surfaces.

**No real user hit a single refusal in the entire live window.** That is the finding, and it took
work to establish, because the refusal table at first glance says otherwise.

| refusal | people | when | what it actually is |
| --- | --- | --- | --- |
| `mkt2.choose-role` 404 "Not found" | 2 | 20:50 on the 18th | **BL-907's own audit**, not users |
| `mkt2.decision` 400 "A reason is required." | 1 | 21:23:14 | **my own BL-908 proof** |
| `mkt2.decision` 400 "The reason must be 1000 characters or fewer." | 1 | 21:23:14 | **my own BL-908 proof** |
| `mkt2.submit` 403 "You are set up to post clips..." | 1 | 17th, pre-launch | a rule BL-903 has since deleted |
| `mkt2.post` 400 "Pick the account you posted from." | 1 | 13:47 on the 18th, pre-launch | a prior round's sandbox |
| `mkt2.post` 409 "You have already submitted this exact post." | 1 | 13:48, pre-launch | same sandbox |
| 39 x 401 "Unauthorized" | 0 (no user id) | 17th and 18th | signed-out containment probes |

**How I know the 404s are not real people.** The two rows are 30ms apart, twice, 25 seconds apart:
a script, not two humans. Five seconds earlier an OWNER session hit two owner-only surfaces.
BL-907's report says its proof ran "side by side with a real clipper carrying **392 clips**" (READ);
one account has **exactly 392**, the other 203, which BL-905 measured as the owner's own clipper
account, BL-907's subject. **Verified by clip count, not inference.**

**Two of those rows are mine**, disclosed: my BL-908 proof left one approval and one rejection in
his audit log at 21:23:15 against sandbox clips since deleted.

**And the small-numbers rule applies anyway.** BL-870 set the floor at five people: "That is too few
to read a pattern into." Nothing here reaches two real people. No trend, and I am not inventing one.

## 3. The queue, and the person still waiting

**Eight pending, three real makers, oldest waiting 11.7 hours.** One of the eight is the Drive
folder BL-908 found. Seven are proper file links. **If resubmitted today, exactly one would be
refused: the folder.** It cannot be reviewed at all, so it needs a rejection rather than a look.

**He worked the queue this morning and stopped mid-way.** Seven approvals between 07:02:14 and
07:05:16, taken **newest first** — BL-908's default, used the morning it shipped. Worth naming:
**the folder clip is oldest, so newest-first put it last.** Under the old order he would have seen
it first.

**Did the notification fire? Yes, and it worked.** Three distinct alerts, nine bell rows (three
owner accounts):

- 20:52:18, "2 clips are now waiting"
- 21:42:36, "3 clips are now waiting"
- **06:25:00 today, "15 clips are now waiting" — and he approved seven at 07:02.**

**The very first submission at 20:37 got no notification at all**, because BL-906's code had not
reached production yet; the first alert is fifteen minutes later.

**The 15-minute batching worked and its cost is visible too.** Twelve submissions between 21:42 and
21:47 produced **one** message, which said "3 clips are now waiting" when fourteen existed by the
end of the burst, because it is sent at the start.

**All nine bell rows are unread.** On Resend, `digitalzentro` is the only address that receives; the
other two owner addresses 403 every time (READ). **So two thirds of the email delivery is silent,
and the channel that always works is the one he does not read.**

## 4. The money: none has moved, and everything is intact

**No v2 clip has earned anything.** Zero maker-earning rows, zero platform-earning rows, zero posts.
That is correct rather than broken: nothing is approved into a post yet, and BL-901 measured that a
post moves **$0.00 at post time** anyway because earnings accrue from views (READ).

Across the **full population**: **10,202 live clips, 0 invariant violations, 0 negatives, 0
double-paid rows on either v2 leg. 21 budgeted campaigns, 0 over budget**, tightest headroom
$300.00. Below paid floor: **26, exactly BL-908's figure**, so it has not moved. **Both
reconciliation forms return 0 rows**, and every row is explained by there being none: with no v2
earning rows, nothing can be out of balance.

**ANGIE BROWN THE REAL ME:** ACTIVE, MARKETPLACE_ONLY, Instagram, budget **$2,700**, $0 spent,
clipper CPM 0.20, minimum 500 views.

## 5. What the first day says that no sandbox could

**Every thumbnail has failed. Fifteen of fifteen, from the first clip at 20:37:39 to the newest at
06:25:02 today.** Zero previews exist. Two verbatim reasons: "Your browser could not read the video
from Drive, so we could not make a preview." (14) and "We could not read a file id from that
link..." (the folder). **The code predicted it** in its own header: "IT WILL OFTEN FAIL, AND THAT IS
EXPECTED RATHER THAN A BUG." Production says it does not fail often, it **fails always**. A poster
sees seven approved clips as seven identical placeholders and must open each Drive link to choose.

**Nobody changed their mind about a side.** Zero side requests, zero strikes, zero bans. The switch
mechanism two rounds built has not been touched by anybody.

**Four people chose the maker side and submitted nothing**, and eight chose poster and posted
nothing. One maker sent thirteen of the fifteen clips, eleven of them in five minutes.

**Nothing blocked a poster structurally.** All eight posters hold approved **Instagram** accounts,
24 between them, and the campaign is Instagram, so the platform matches. Gate zero is not in play
either: no maker also holds the poster side.

**Three things every round assumed and none can yet be measured**, stated rather than guessed:
whether a maker reads a rejection and resubmits (**zero real rejections have ever been issued**);
whether a poster returns from Drive on the same device (**zero posts**); and whether the **30 minute
posting window** is long enough now BL-907 removed the last exemption (**zero posts, so it has never
been exercised by a real person**). That window is the largest untested assumption on the platform.

## 6. What to fix, worst first

**People are stuck right now:**

1. **Eight clips pending, three makers waiting, oldest 11.7 hours.** He is working it and stopped
   part way. **Owner action, not code.**
2. **The folder clip has waited 11.7 hours for an outcome that cannot exist.** It can never be
   opened, so it needs the "Cannot open it" rejection BL-908 shipped. **Owner action**, two presses,
   and newest-first ordering has put it at the bottom of his list.
3. **No preview on any clip, ever.** 15 of 15. It does not block posting but it makes choosing what
   to post cost a Drive round trip each time, on the exact screen posters are on right now.
   **Code**, and it needs a different approach than browser canvas capture, which has now been
   measured at a 100 percent failure rate.

**Should merely be better:**

4. The burst notification undercounts, saying "3 waiting" when fourteen arrived in that window.
   **Code**, small.
5. Two of three owner email addresses receive nothing. **Owner action in Resend**, verify a domain.
6. Nine unread bell rows. The one channel that always works is the one he does not use. **Not a
   defect**, but it means email is doing the real work, and email is two-thirds broken.
7. 1,551 people were emailed and 19 arrived. **That is the funnel's real shape** and no round has
   ever looked at it before. Not a defect, and far too early to call it one.

**The single most valuable thing today: clear the remaining eight, and reject the folder one first.**
Three real people have been waiting up to 11.7 hours, his approval is the only thing that fills the
catalogue, and one of those eight can never be approved no matter how long it sits there.

**And the honest headline is that almost nothing is wrong.** No real person hit a single refusal in
thirteen hours of live use. The money is untouched and every invariant is clean. The notification
fired at 06:25 and he reviewed at 07:02, which is the feature working on its first real day. The
catalogue has only been non-empty for seventy minutes, so **zero posts is not yet evidence of
anything**, and the correct thing to do about it today is wait and look again, not build.
