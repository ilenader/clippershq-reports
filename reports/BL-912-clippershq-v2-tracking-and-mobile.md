# BL-912 — v2 clips were never polled a second time

**You were right, and it was one word.** Every one of your six live marketplace posts had a
tracking job that existed, was **due**, and was **switched off**. `lastCheckedAt` was NULL on all
six: not one had ever been polled after the check at submission. Each carried exactly one ClipStat,
written in the same millisecond as the post, reading 0 views, while the posts were live on
Instagram for up to 4.4 hours.

**Merged to main** (`1502b143`). **Model split:** I wrote every line of the tracking fix and ran
every database query myself; subagents (Sonnet) read reports and source and **opened no database
connections**. Cap: one pooled connection at a time. **Vendor calls: none beyond what the platform
was already doing** — see below.

## ITEM ONE — the tracking fix

### What was measured, before anything was explained

| post | live for | ClipStat rows | views | job | due | last polled |
| --- | --- | --- | --- | --- | --- | --- |
| six of six | 2.85 to 4.40 h | **1** each | 0 | exists | **yes** | **never** |

### The cause, and the others ruled out

`createV2Post` wrote `isActive: false`, behind a comment citing BL-879's reason: the tick of the day
would have paid a v2 poster the full clipper rate. **BL-880 fixed that tick and said so in the tick
itself** — "this is the line that makes activating them safe" — then wired activation to the
**approval** event and never came back to the creation path. `marketplace-v2-poster.ts` even carried
the sentence "ROUND FOUR MUST TEACH THE TICK ABOUT V2 AND THEN ACTIVATE THESE JOBS", unread for four
rounds while it stayed half done.

Ruled out by evidence rather than by preference: the job **is** created; the cron is healthy and
busy (4,416 Instagram clips handled minutes before I looked); the campaign is not excluded; nothing
swallowed an error, because `consecutiveFailures` is 0 on all six — the tick had never seen them.

**The deciding comparison, on fourteen days of your real data: 39 ordinary PENDING clips carry
ACTIVE jobs, and 0 of those 39 have any earnings.** v1 tracks from submission and pays only on
approval. v2 alone was waiting for an approval v1 never required.

### Why switching it on is safe

The tick **collects** pending clips deliberately — its own filter says "PENDING stays included so
owner-review stats stay current" — and **pays** only approved ones (`tracking.ts:2042`). So a
pending clip gathers view history and earns nothing, which is exactly what those 39 v1 clips do.

### Proved on real money, with no extra vendor spend

Rather than force a manual check I activated the six by id and let **your own ten-minute tick** reach
them. It did, at 13:00:44, returning real views: **1,399 / 388 / 153 / 421 / 118 / 315**.

**Nothing was lost while they were dark.** Confirmed rather than assumed: the first poll after 4.5
unpolled hours returned the **cumulative** total, not a delta.

On cost: `estimatedCostUsd` records **0.0000** for every provider in production, so I could not
price a single call and will not invent a figure. HikerAPI runs under a daily cap defaulting to $10.

### The split on real views, and an honest surprise

Only one of the six clears the campaign's **500-view minimum**. On it: gross **$0.2798**, maker
**$0.1300**, poster **$0.1300**, platform **$0.0200**, summing to $0.2800.

**That reads 46.43 / 46.43 / 7.14, not 45/45/10.** Nothing is lost or invented: the platform leg is
the residual, so the three always sum to the gross. At a gross of 28 cents, one cent of rounding is
3.6 percent. Every prior proof used synthetic view counts large enough to hide this. Worth knowing
before you read your first real numbers.

### Your earnings are still zero, and this is the second half of your question

**All six clips are PENDING in the ordinary clips queue**, sitting among 39 unrelated v1 clips with
nothing marking them as marketplace posts. **The money needs you to approve them there**, and
nothing on the marketplace screens tells you so. The owner's `AgencyEarning` row cannot exist until
then, which is correct rather than missing.

### So it cannot go silent again

`check:v2-tracking-active` now runs in prebuild and refuses a build that creates a v2 job inactive.
**Two of its own four checks could not fail until the demonstration caught them** — T3 tested the
whole review route for `isActive: true`, which appears five times there, so breaking the v2 one left
four and the check passed. All four are now demonstrated failing one at a time, each naming itself,
tree restored and hashed after each.

## ITEM TWO — the phone overlay is the install prompt

**Reproduced 6 of 6** at 375 wide with an iOS user agent and clean storage, and photographed. It is
the **"Install Clippers HQ / Add to your home screen"** sheet: `fixed inset-0 z-[100] flex
items-end`, a `bg-black/40 backdrop-blur-sm` scrim, over a card on `#141416`. On a dark theme that
is precisely "a black area covering the bottom of the screen, over everything".

**The prompt is not the bug and I did not disable it.** What is a bug is where it lands: `z-[100]`
is above the app's own dialog at `z-50`, so the two-second timer could drop it on a form you were
filling in. It is worse than visual — while a dialog is open its focus trap owns Tab, so the prompt
is keyboard unreachable, a mouse user is thrown back out on the next Tab, and Escape closes the
dialog underneath. **It now waits**, proved both ways: with no dialog it still appears, with one open
it stays away.

**The obvious one-line guard would have killed the feature silently.** I wrote
`querySelector('[aria-modal="true"]')` first. `ReportProblemWidget` is mounted for every signed-in
person and keeps that attribute permanently, hidden by `inert` — so it matches on every page, and
the prompt would never have appeared again with nothing failing anywhere. The review caught it
before it shipped.

**The brief's prime suspect is dead and should stop being inherited:** `--bg-page` has **zero** live
references in `src` today; the single match is inside a comment. Earlier rounds counted 33.

## ITEM THREE — the campaign filter

Server side, proved by request **8 of 8**: the scope goes into the `where`, every count is taken
over the same `where`, and paging with `skip` reaches the true total. An unknown id returns an empty
set rather than silently showing everything.

**Your test campaign was missing from your own picker**, because the list was a `groupBy` over
campaigns that *have* clips. It is a union now, so a campaign you have opened to the marketplace
appears before anyone has submitted to it.

## ITEM FOUR — the owner view was not a second defect

Verified: the overview and the poster's own dashboard read **byte-identical** expressions for views
(newest ClipStat, `checkedAt desc`, `take 1`) and the same `Clip.earnings` column. The zero was
real. No money is computed on the page.

**Found on the way, logged not fixed:** the *editor's* dashboard reads views from a snapshot column
rather than live ClipStat. Dormant today because both move together, but they can diverge.

**Thumbnails not rebuilt, as instructed.** BL-910 measured 15 of 15 failing; it is now **18 of 18**.
Next round's job.

## Proved

Build exit 0, 0 TypeScript errors, **20 of 20 guards**, hooks 0 errors and 10 warnings after
correcting the one warning this round introduced, so the cap keeps its single slot of headroom.
Invariants across the **full population**: 0 out of balance, 0 negative, 0 double-paid, **21
budgeted campaigns and 0 over budget**. Eleven money files byte-identical by blob OID. **Renders 5
of 5** at 320, 375, 414, 1280 and 1440 with the phone widths **scrolled**, URL and `innerWidth` read
back, pan measured at **0px everywhere**.

**The only real rows this round wrote: six `tracking_jobs.isActive` booleans, flipped by id**, by an
idempotent file kept at `scripts/migrations/BL-912-activate-v2-tracking-jobs.sql`. No money row, no
clip, no campaign, no user. **Zero sandbox rows were created at all** — the proofs ran against your
real posts and read-only queries.

## Are real v2 clips now tracking and earning?

**Tracking: yes, proved.** Six posts that had never been polled were polled at 13:00:44 and returned
2,794 real views between them, and they are scheduled again at 15:00 and 18:00.

**Earning: not yet, and that part is yours.** They are pending in your ordinary clips queue. Approve
them and the money starts; five of the six will still read zero until they pass 500 views.
