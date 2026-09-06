# BL-847 — the marketplace, hardened where nobody had looked

**Nothing could not be removed.** 154 sandbox rows plus 38 audit rows and 5 video hashes the product
wrote in response, all deleted by primary key, 0 remaining, every closing count and both real
fingerprints identical to the opening snapshot. There is no leftover with an id and no SQL for the owner
to run.

Measured 2026-09-06, 20:50:17 to 21:20 UTC, against production. Worktree `C:/w847`, branch
`checkpoint/BL-847`, from `main` at `da3eb5fb`.

**Collision with BL-846 avoided by construction, and checked rather than assumed.** No BL-846 worktree
existed, no claim file, no live session, no listening server, and `main` had not moved past this
session's own BL-845 merge. This round used its own worktree, its own sandbox round (`bl847`, its own
prefix, ledger, directory and confirmation variable), its own port, and touched no COMPLETED or PAST
campaign except two it created and deleted itself.

---

## 1. Instagram: eleven loss points, not one

Marketplace posting to Instagram was refused **one hundred percent of the time, in every environment**,
and Instagram carries most of this owner's volume. BL-845 named two causes and was right as far as it
went. Here is the whole path.

| # | file:line | Condition | Fired? |
|---|---|---|---|
| 1 | `apify.ts:800` | `if (APIFY_HARD_OFF) return null` — IG tier 1 | always |
| 2 | `apidojo.ts:552` | `apifyCredential()` is null → tier 2 returns null | always |
| 3 | `apify.ts:217` | `legacyActorsCanResolve()` refuses `/reel/`, `/reels/` — tier 3 skipped with no call | ~96% of IG |
| 4 | `apify.ts:254` | `APIFY_HARD_OFF` in the `/p/` fallback | the other 4% |
| 5 | `post/route.ts` | `fetchClipStats(url, { skipHikerOverlay: true })` removes the only IG provider that answers | always |
| 6 | `post/route.ts` | `stats == null` → 400, `PROVIDER_NULL` | **the refusal** |
| 7 | `hikerapi.ts:1028` | `createdAt: null` is hardcoded on the overlay | **the trap** |
| 8 | `marketplace-timers.ts` | the no-strike branch never ended its iteration | see §4 |
| 9 | `marketplace-timers.ts` | BL-845's own "NO STRIKE" log line was dead code | see §4 |
| 10 | `post/route.ts` | `verifyFailedAt` was written and never cleared | fixed |
| 11 | `youtube.ts:84` | `YOUTUBE_API_KEY` unset → YouTube dead too | config, not code |

**Loss point 7 is the one that matters most, because it defeats the obvious fix.** Deleting
`skipHikerOverlay: true` does **not** work: the overlay hardcodes `createdAt: null`, with its own comment
saying the real value lives on `rawBody`, so the null falls straight into the "no timestamp" branch and
refuses every Instagram post again, at a different line number, **while measuring clean in code review**.
BL-673, BL-682, BL-746 and BL-820 were each this same trap, and **two of the four were nearly
mis-diagnosed by a probe reading the wrong field**.

**The fix reads what the clipper submit path already reads, the way it reads it:**
`fetchHikerInstagramByUrl`, unwrap `media_or_ad ?? media ?? data` (BL-682's order, established by
measurement), then `evaluateInstagramFreshness`, which is already exported and already carries the
clock-skew tolerance. No new vendor integration and no second call.

**IT FAILS OPEN, AND THAT IS A POLICY CHANGE THE OWNER SHOULD SEE.** Only a provider-**confirmed**
too-old post is refused. An unconfigured key, a throw, an unreadable body or a missing `taken_at` all
accept. That is the contract `clipper-submit-core.ts:581-596` already states in full for the ordinary
clipper path, on the measured grounds (BL-664: a 0.77% human overturn rate) that a wrongly refused person
is worse than a late clip accepted. **What still protects the campaign is unchanged:** the clip lands
PENDING and the OWNER must approve it before a cent accrues.

**Proven end to end, not at the piece that changed:**

```
THE INSTAGRAM POST IS ACCEPTED, which it never was on main ....... http 201
a real Clip row exists for the Instagram post .................... status=PENDING, owner=poster
tracking was started for it, so it can actually earn ............. tracking jobs=1
the submission is POSTED and the platform is recorded once ....... ["INSTAGRAM"]
and the verification-failure mark is cleared by a successful post . verifyFailedAt=null
```

And the verdict itself, branch by branch, with **no vendor call**: a post one minute old is `fresh`, one
twelve hours old is `too_old` and is refused, and a body with no `taken_at` is `unknown` and accepts.

**Instagram stays dead until Railway is redeployed.** YouTube needs `YOUTUBE_API_KEY` set, which is the
owner's to do.

---

## 2. The quota was charged on the wrong day

`dailySlotCount` is described everywhere as a daily cap on **posts**, and the listing card counts down
"slots used today". Capacity was charged only at submission time, against the UTC day the **submission**
was created (`submissions/route.ts:435`). A submission can be posted up to **48 hours** later: 24h TTL to
approval, then 24h to the post.

**The worked example, at the default of 5, targeting the 10th:**

| UTC | who | action | charged to | posts landing on the 10th |
|---|---|---|---|---|
| 8th 23:50 | creator | submits 5 | **the 8th** | — |
| 9th 23:45 | poster | approves; deadline 23:45 on the 10th | nothing | — |
| 9th 00:05 | creator | submits 5 | **the 9th** | — |
| 9th 00:06 | poster | approves; deadline 00:06 on the 10th | nothing | — |
| 10th 00:04 | poster | posts cohort B | — | **+5** |
| 10th 12:00 | creator | submits 5, posts them | **the 10th** | **+5** |
| 10th 23:40 | poster | posts cohort A, five minutes inside the deadline | — | **+5** |
| | | | | **15 posts against a cap of 5** |

Every gate returns 200. Nothing is bypassed: the rule is obeyed three times against three different days.
The ceiling is exactly **3x**, because a 48 hour window touches exactly three calendar days. **Two of the
three cohorts need no collusion at all** — a merely slow poster produces 2x by accident. It takes two
accounts, because a poster cannot submit to their own listing.

**The fix is a settle gate, not a move.** Charging everything at post time would make the name true and
destroy the one thing the submit gate is good at: telling a creator there is no room **before** they cut
the video. Shortening the deadline to the end of the creation day hands a submission made at 23:50 a ten
minute window and then **strikes the poster** for missing it, which punishes the wrong person for a rule
they did not break. So the reservation stays exactly as it shipped, all six "used today" displays are
untouched, and a second independent count of **real posts that landed today** sits immediately before the
fan-out loop. A poster who posts promptly never meets it. It counts through the submission relation, so
**no schema change and nothing to backfill**.

Proven by building the drift with aged rows: the third post today refused, and real posts landing today
equal the cap of 2 rather than 3.

### The timezone question, settled

It is **genuine UTC midnight** — `new Date()` then `setUTCHours(0,0,0,0)` is an absolute instant zeroed in
UTC, regardless of the container's `TZ`. There are **six** copies of those lines and they agree.

`MarketplacePosterListing.timezone` is a **dead column**: written by the edit modal and the owner
override, read only for a display label, and present in **none** of the six boundary sites. Zero of one
live listings has it set.

| poster | reset lands at, local |
|---|---|
| Belgrade (UTC+2) | 02:00 — defensible, the middle of the night |
| Los Angeles (UTC−7) | **17:00** — a defect |

An LA poster's single local day contains **two** resets, so they receive 2N slots from the boundary alone
before any of the 48h drift. It is consistent with `maxClipsPerUserPerDay`, so the platform has one
definition of "day" for quotas — but `gamification.ts:115` already ships a DST-aware, user-local
`dayBoundsForTz`, and `User.timezone` is populated by the navbar, so **streaks already use the person's
day while every quota uses UTC**. Moving the quota to listing-local time is a product decision, and the
helper it needs exists and is already tested. **Recorded, not changed.**

---

## 3. The strike trap: six entrances, now none

BL-845 stopped a poster being struck when our **provider** failed. It did not stop the wider case.

A submission is APPROVED with a 24 hour deadline. Then the campaign is **paused**, **archived**,
**completed**, **destroyed**, or **exhausts its budget** underneath the poster; or the destination account
is **revoked**, **rejected** or **user-deleted**. `/post` refuses every attempt from that moment. The
deadline elapses. `marketplace-timers.ts` selects on "deadline passed and nothing posted" with **no
campaign filter and no account filter anywhere** and writes `MISSED_POST_DEADLINE`. Three inside thirty
days bans them for 72 hours and flips **every ACTIVE listing they own** to BANNED.

**BL-845's shield did not save them**, because it reads `verifyFailedAt` and that is stamped further down
the file, past both gates. **The poster was struck for failing to do the one thing the server would not
let them do.**

Both gates now record the refusal as ours before returning, and both messages end with "You will not get
a strike for this one."

**The budget entrance is the sharpest, and it needs nobody to press anything.** `pauseSource: "AUTO"` has
fired **eleven times** in production. The same tracking cron that pauses the campaign strikes the poster a
day later.

Proven: a campaign moved to COMPLETED under a live deadline leaves the poster unstruck and stamps
`campaign:COMPLETED`, while a poster who simply did not post is **still** struck. Exactly one strike.

**Also recorded:** nothing cascades on a campaign **status** transition at all. `cascadeCampaignArchive`
exists, is imported into `campaigns/[id]/route.ts`, and its own contract says to wire it to PAST and
COMPLETED transitions — and no status transition calls it. So the listing stays ACTIVE, browse never
filters campaign state, and a creator can still submit to a dead campaign. The rule lives only in a
component, which means it is not a rule.

---

## 4. A bug inside BL-845's own fix, which I shipped

The no-strike flip was entered on `activeBan || couldNotConfirm`. The `continue` that ends the iteration
sat inside a branch testing `activeBan` **alone**. So for the exact case BL-845 was written for — a poster
whose verification **we** failed, who is not banned — execution fell straight through and:

- added them to `postersTouched`, so the ban check saw them, **directly contradicting BL-845's own comment**
- wrote an audit row saying `MARKETPLACE_STRIKE_ISSUED` for a strike that was never created
- notified them **"A strike has been issued"**
- emailed them the missed-deadline mail with a strike count

No `MarketplaceStrike` row was ever written, so the ban **count** stayed honest and **BL-845's test passed
for a true reason while the person was told something false**. That is the same class as the ban email
saying 48 hours: the record and the message disagreed with the act.

The condition is `activeBan || couldNotConfirm` now, the audit action branches
(`MARKETPLACE_STRIKE_SKIPPED_VERIFY_FAILED`), and the poster is told plainly: **"Post window closed, and
no strike was given. We could not check your post in time, so this one is closed and NOTHING was counted
against you."**

Proven by reading the rows back: exactly one "a strike has been issued" message for the one real strike,
and exactly one `MARKETPLACE_STRIKE_ISSUED` audit row.

---

## 5. Five more defects, from going where nobody had been

**A REVIEWER COULD APPROVE THE MARKETPLACE CLIP THAT PAYS THEM 60 PERCENT.** The self-review block
compares `clip.userId`, and on a marketplace clip that column holds the **poster**. The creator is
`marketplaceSubmission.creatorId` and nothing compared it to anybody — not in the mutation, not in the
read filter that builds the reviewer's queue. The poster leg was safe only by the accident of which id
landed in which column. Closed on the server and in the queue. Proven: 403, and absent from the payload.

**A MARKETPLACE CLIP COULD BE REASSIGNED TO ANOTHER CAMPAIGN.** The move overwrites
`cpmAtSubmissionDecimal`, which is the rate the **creator** agreed to at post time, so their 60 percent is
computed from a number they never saw; the notification goes to `clip.userId`, the **poster**, so the
person whose rate changed is never told; the sentence the poster does receive quotes the **gross** cpm,
overstating his own 30 percent by more than three times; and the listing's `campaignId` is untouched, so
the clip is billed against two listing budgets that know nothing about each other. Now blocked with
`CLIP_IS_MARKETPLACE`, matching `override/route.ts:157` and `campaign-freeze-undo.ts:310`, which already
refused marketplace clips. An ordinary clip is still moveable, proven.

**APPROVING A MARKETPLACE CLIP AGAINST A NEARLY EXHAUSTED BUDGET THREW INSTEAD OF WRITING.**
`review/route.ts` scaled the poster's 30 percent down but passed the **unscaled** `base` and `bonusAmount`
to `writeClipEarnings`; `assertInvariant` throws above a cent of drift, so the whole approval transaction
failed. The non-marketplace path has rescaled its components since F-AUDIT-CLEANUP-T5. The bonus is now
scaled by the same ratio and **the base is the residual**, so base plus bonus equals the scaled earnings
by construction rather than by two roundings agreeing.

**THE SCREEN THAT TELLS THE OWNER WHAT HE OWES had no clip predicate at all.**
`admin/payouts/user/[id]/route.ts` summed `MarketplaceCreatorEarning` with none of `isDeleted: false`,
`status: "APPROVED"` or `videoUnavailable: false`, while its own comment claimed it matched
`computeBalance`. It would have shown a debt larger than the payout system would let that person withdraw.

**THE LISTING DETAIL PAGE SAID "0 OF 5 SLOTS USED TODAY" FOREVER.** Five other surfaces compute
`usedToday`; this one never did and its select had no such field, so the chip fell back to 0 and the
submit modal it feeds received `undefined`, which turns the cap display off entirely. The one screen a
creator reads before spending an hour cutting a clip showed a full day's capacity on a listing that might
have none left.

---

## 6. Six pieces of copy that were false

The class BL-845's 48-hour ban email belonged to: text the user acts on that does not match the code.

| The string | What the code does |
|---|---|
| "You have **24 hours** to post it" — sent to the **CREATOR**, with a "Post your clip" button | A creator gets 403 "Only the poster can mark this as posted." BL-304 fixed this exact claim in the UI and never touched the mail |
| "Post your videos NOW and submit each URL **within your 24h deadline**" | Each URL is **also** gated on the 30 minute freshness window, and **no poster-facing string anywhere named it**. Post the video, come back an hour later well inside "your 24h", refused; run out of runway and take a strike |
| "Strike n**/3**… triggers a **48-hour** ban" | Config says 3 and **72**. And the count omitted the `EXCESSIVE_REJECTIONS` exclusion the ban trigger has, so a poster with two rejection strikes and one missed deadline is emailed "Strike 3 of 3" and never banned. **All 31 live strike rows are `EXCESSIVE_REJECTIONS`** |
| 409 on create-listing always said "you already have a listing…" | The other cause says the account is used in **another** listing, possibly somebody else's. The server's own sentence was discarded |
| "try again **tomorrow**" | It resets at **midnight UTC**, which for an American poster is this afternoon |
| "9 AM – 6 PM CET" | The last bookable slot starts at **16:45** |
| "Cash out **anytime**" | There is a per-campaign minimum, defaulting to **$10** |

All fixed, with the two numbers now read from the live config so they cannot drift again.

---

## 7. Cycles, and the harnesses that lied

**Four cycles.**

| cycle | what it found |
|---|---|
| 1 | Instagram's eleven loss points, including the trap that defeats the obvious fix; the bug inside BL-845's own fix; the budget scale-down throw |
| 2 | the quota's 48 hour drift with the worked example; the strike trap's six entrances; the reviewer self-approval hole; the reassignment hole; the owner's-debt query |
| 3 | `Clip` has no `marketplaceSubmission` relation, so the self-review guard had to reach through `marketplaceOriginPost`; the notification column is `body`, not `message` |
| 4 | **two harnesses had become unfaithful**, below |

**BL-845's ban script could no longer reproduce its own defect.** It induced a provider failure with an
Instagram url, which worked **only** because Instagram was refused 100 percent of the time. The moment
that was fixed the post returned **201** and the test measured nothing. A harness that cannot reproduce
the condition it was written for is broken, not passing. It uses a YouTube url now, with
`YOUTUBE_API_KEY` unset, which is a genuine "we could not check" and costs no vendor call.

**BL-845's views script read five source files from `C:/w845/`** — its own worktree, long removed. Those
five checks failed on this round while the gates they test were untouched. It reads `process.cwd()` now.
Two further round-specific literals were parameterised: the render harness named BL-845's sandbox
directory outright, and the audit sweeper's window was a BL-845 variable with a BL-845 default.

---

## 8. The money, re-proven

**280 checks, 0 failures.** This round's own suite (23), and the **entire BL-845 suite re-run against
these changes**: quota 16, **money 39**, ban 12, views 40, plus **25 shots and 150 render assertions** at
320, 375, 414, 1280 and 1440 with `window.innerWidth` printed beside every one, **0 at the wrong width and
0 with horizontal overflow**.

| case | fee | express | trainer base | trainer cut | **clipper cash** | referrer |
|---|---|---|---|---|---|---|
| plain | 9.00 | — | — | — | **91.00** | — |
| referred | 4.00 | — | — | — | **96.00** | 4.80 |
| trainer | 9.00 | — | 91.00 | 9.10 | **81.90** | — |
| express | 9.00 | 4.00 | — | — | **87.00** | — |
| all three | 4.00 | 4.00 | 91.00 | 9.10 | **82.90** | 4.60 |

`final + fee + express + trainerCut = 100.00` **exactly** in all five. The 60/30/10 residual sums exactly
at $100.00, $0.55 and $4.57. The referrer's 5 percent remains a separate row minted at PAID **on top of**
the gross, out of the platform's margin, so a plain referred payout still leaves the platform $0.80 down.

**THE 10 PERCENT STILL REPLACES THE OWNER'S NORMAL CUT RATHER THAN ADDING TO IT, and nothing in this
round changed that.** `isCpmSplit = !isMarketplaceClip && …`. All **nine** sites in `src/` that can create
an `AgencyEarning` row are closed to a marketplace clip by one of two mechanisms — `!isMarketplaceClip` in
the predicate, or `isMarketplaceClip: false` in the query — plus one route that refuses marketplace clips
outright. A tenth states the rule in a comment. Measured live: `agency_earnings` joined to marketplace
clips on `clipId` = **0 rows**.

**Every invariant survives, proven rather than asserted:** BL-824 paid-is-final and BL-827's below-paid
guard (payout fingerprint identical, 221 rows before and after), BL-627 no-overpayment and BL-538
never-decrease (earnings invariant 0 violations both sides), BL-696 no-double-pay (0 double-open payouts),
the `(submissionId, platform)` unique index created in BL-845 (still unique, still valid), and the rule
that a third party's cut is a stamped deduction on the payout row rather than a change to `Clip.earnings`
(all 39 money checks green, `Clip.earnings` untouched by the trainer path).

---

## 9. Nothing left behind

154 rows created, every id recorded in a ledger outside the repo at the moment of creation, deleted by
primary key and never by pattern, name or date: **150 deleted, 4 taken first by cascade, 0 of 154
remain.** Then, as BL-845 had to, everything the **product** wrote in response and whose ids the ledger
could never know: **38 audit rows and 5 `MarketplaceVideoHash` rows**, both swept in two passes — list,
print every id with the reason it is ours, write the ids to a file, then delete only what is in that file.

**50 verification checks, 0 failures.** Users 1675, campaigns 34, clip accounts 1480, memberships 782,
payout requests 221, adjustments 9, trainer relationships / commissions / refunds 0, referral commissions
7, notifications 14145, every marketplace table, `over_payable_holders` 17, and both real fingerprints
(`42ab3988…`, `79582590…`) **byte-identical**. Earnings invariant **0 violations** before and after.
**14 invisibility checks, 0 failures**, asking every campaign, spend, earnings, clips, leaderboard and
referral surface **as a real clipper with 840 approved clips**.

What moved is named: **2 clips and 401 view snapshots from 2 real clippers and the tracking cron, and 4
agency-earnings rows.** Nothing else.

**No vendor money was spent.** Every sandbox tracking job was deactivated and pushed a year out the moment
it existed, so there were **0 active tracking jobs on any sandbox campaign at any point a tick could have
seen one**. No Apify actor was run and the 11 BL-678 guards are untouched. `LAMATOK_KEY`, `HIKERAPI_KEY`,
`YOUTUBE_API_KEY` and `EMAIL_API_KEY` were all unset on the sandbox server, and every mail shows as
`[EMAIL PREVIEW]`.

---

## 10. Recorded and not fixed, with reasons

**The two that would cost real money:**

**The creator's 60 percent and the platform's 10 percent have no paid-is-final and no never-decrease
floor.** They bypass `writeClipEarnings` and the entire L1–L4 stack by design (`tracking.ts:2814`,
`:2828`), with only a NaN guard. If views fall under `minViews`, `calculateMarketplaceEarnings` returns
empty and **the row is overwritten to 0** — and a creator already paid for that 60 percent has the paid
money stranded. BL-824 and BL-827 bought that protection for `Clip.earnings`; it was never extended here.
**Not fixed because it is a change to a money file with real blast radius and it deserves its own round,
not a corner of this one.**

**`counter-recompute` must not be enabled before it is fixed.** It defines truth as a current-status
snapshot against a lifetime write path, so the first Sunday tick would overwrite every poster's lifetime
record and a poster with a perfect 40-for-40 would render "Lifetime approved: 0". It is one config line
away. Separately `totalPosted` counts **platforms** while its siblings count **submissions**, so a
two-platform submission yields Submitted 1, Approved 1, **Posted 2** on the ordinary happy path — and
those numbers are shown to a **creator** deciding whether to work with that poster.

**The rest, each named with where it lives:** campaign DESTROY hard-deletes marketplace money rows with no
balance check and no notification, while payout rows survive with their `campaignId` nulled; clip
soft-delete leaves the 60 and 10 rows standing at full amount, the submission POSTED forever and the
creator untold; browse, submit and approve never check campaign state; three marketplace crons have never
run once, so strikes never decay and no `MarketplaceStrike` row is ever deleted anywhere; the trainer is
blind to a marketplace creator's 60 percent while a poster **is** charged on their 30, an asymmetry
nothing records a decision about; the trainer payout **preview** never reads `eligibleGrossCharged` and
can quote a figure ten times what the server charges, which can refuse a legitimate withdrawal client
side; a referrer who is also the poster double-dips; and the 60/30 split is published four lines apart in
`MpExplainer` and again in a help sentence naming the remainder, so `100 − 60 − 30` is stated by
implication and **no gate can close that identity**.

**Accessibility: 27 new criticals** on top of BL-845's 196 findings, of which six reach the whole app and
were deliberately left for a round that can render the whole app. The highest-value single fix is
`src/components/ui/button.tsx:50`, where `disabled={loading}` unmounts the control the user just pressed
and drops focus to `<body>` after every destructive action. Confined items worth taking next: Approve has
no confirmation while Reject does; the admin listings queue is the one marketplace surface with no error
state, so a 500 renders as "No listings"; the delete-confirm never names the listing it will delete; and
the poster application has no error output at all behind a natively disabled submit.

---

## 11. Build honesty

**One production build, exit code echoed by hand and never piped through `tail`: 0.** A clean `tsc`
baseline was taken **on the untouched worktree before any edit**: exit 0, `grep -c "error TS"` = 0. Six
further typechecks during the round, the last at exit 0 with 0 errors, and **one of them caught a real
error** (`marketplaceSubmission` is not a relation on `Clip`) which is recorded here rather than silently
retried. Hooks gate **0 errors, 10 warnings** against a ceiling of 11. `eslint v9.39.4` confirmed present,
so the gate is a real check.

**The 6 money files plus `tracking.ts` and `campaign-era.ts` are byte-identical by blob OID on both
refs.** No schema change, no migration, no index, no `prisma migrate`. BACKLOG 178 → 179, counted with
`grep -c` and never piped to `head`. `checkpoint/BL-723` confirmed not an ancestor. Worktree `C:/w847`
removed.

---

## 12. Is the marketplace safe to launch?

**Not yet, and the remaining blockers are short and specific.**

**What this round unblocked:** Instagram can be posted at all, which it could not; the quota means what
its name says; a poster can no longer be struck for a refusal that was ours, from any of the six
entrances; a reviewer cannot approve their own marketplace clip; a marketplace clip cannot be silently
re-rated by reassignment; and approving one against a nearly exhausted budget no longer throws.

**What must happen before real money flows:**

1. **Redeploy Railway.** Instagram posting stays dead until then.
2. **Set `YOUTUBE_API_KEY`**, or accept that YouTube posting is dead.
3. **Give the 60 and 10 legs a floor.** Until then a creator's paid 60 percent can be overwritten to zero
   by a view drop, and that is the one defect here that can strand money somebody already has.
4. **Do not enable `counter-recompute`.**
5. **Decide the trainer question**, which the code currently answers two different ways for the two
   parties without having been asked.

**What remains unproven, stated plainly.** Nothing in the marketplace has ever executed in production: 0
submissions, 0 posts, 0 creator or platform earning rows, 0 marketplace clips, $0.00 ever moved. Every
proof in this report is a sandbox proof against production **code**, not an observation of production
**behaviour**. The Instagram happy path was proven with a fail-open accept and a synthetic media object
rather than a genuinely fresh, live Instagram post inside a 30 minute window, because no such post could
be conjured on demand — so **the one thing still unproven is a real Instagram reel, freshly posted, being
read by HikerAPI and accepted on its real `taken_at`.** That needs one live post by one real poster after
the redeploy, and it is the single test I would run first.

