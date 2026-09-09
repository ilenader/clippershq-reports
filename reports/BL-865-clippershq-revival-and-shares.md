# BL-865 — the shares are working, and the missing money is a return leg that was never built

**2026-09-09. Shipped on `checkpoint/BL-865`. Requires a Railway REDEPLOY, and one environment
variable the owner must set himself or PART 4 does nothing.**

---

## THE HEADLINE: THE OWNER'S IMPRESSION ABOUT SHARES IS MISTAKEN, AND HERE ARE THE FIGURES

The brief allowed for this outcome explicitly and it is the outcome. BL-820's Instagram share fix
deployed at `b9a288cc`, **2026-08-23 21:23:36 UTC**. Measured in production today, either side of
that instant:

| Platform | Snapshots BEFORE | with shares > 0 | Snapshots AFTER | with shares > 0 | labelled `sharesSource` |
|---|---|---|---|---|---|
| Instagram | 142,534 | **3** (0.002%) | 85,591 | **46,270** (54.1%) | 54,348 |
| TikTok | 62,975 | 32,873 | 5,761 | 1,739 | 5,761 (100%) |
| YouTube | 61,401 | 0 | 222 | 0 | 0, correctly |

Before the fix, three Instagram snapshots in 142,534 carried a share count, and BL-820 already
established that those three are the owner's own manual overrides. After it, **46,270 do**. That is
not a fix that failed to land. That is a measure that went from nothing to a majority.

**AND THEY MOVE.** The brief asked specifically whether shares rise as views rise, because a frozen
number can look measured. Across the last seven days, restricted to Instagram clips with at least two
labelled snapshots:

- 2,145 clips qualified, **1,544 gained views**
- **790 of those (51.2%) gained shares in the same window**
- 567 (36.7%) held a positive share count that did not happen to change, which is what a reel that
  nobody re-shared this week looks like
- 187 (12.1%) sat at zero throughout

So 1,357 of 1,544 carry a real measured number and half of them moved. The remaining twelve percent
is an ordinary long tail, not a broken pipe.

**YOUTUBE IS RECORDED ABSENT, NOT AS A FABRICATED ZERO, AND THAT WAS CHECKED RATHER THAN ASSUMED.**
`ClipStat.shares` is `Int NOT NULL DEFAULT 0`, so the column itself cannot hold "absent" and the 0 is
unavoidable. The absence is carried by `sharesSource`, and on all 222 post-deploy YouTube snapshots
it is NULL. The write side is correct. YouTube's Data API `statistics` resource publishes viewCount,
likeCount, favoriteCount and commentCount and nothing else, so no fetch could ever supply one.

**THE 36.5% OF POST-DEPLOY INSTAGRAM ROWS WITH NO LABEL ARE NOT A FOURTH LOSS POINT.** 31,243 rows
carry `sharesSource = NULL`. That looked like a leak and it is not one. `classifyV2Media`
(`hikerapi.ts:583`) sets the label only when `reshare_count` is actually present and
`share_count_disabled` is not true, so an unlabelled row is Instagram not returning the field, which
is exactly the ABSENT the brief demands. The split confirms it is a property of the response rather
than a code path: of 5,264 Instagram clips with post-deploy snapshots, 2,041 are always labelled,
2,153 never are, and 1,070 are mixed. A pure code fault could not produce the mixed group. And the
labelled proportion is climbing on its own, 42.1% on the deploy day to 75.0% on 7 September.

**I FOUND NO FOURTH LOSS POINT IN THE WRITE CHAIN.** `apify.ts:1627` and `tracking.ts:1789-1837`
both carry `shares` and `sharesSource` through. The one real gap was on the READ side, and it is
fixed below.

---

## WHAT WAS ACTUALLY WRONG ABOUT SHARES, AND IT IS SMALL

`api/client/campaigns/[id]/route.ts` summed shares raw. BL-820 fixed the campaign LIST
(`api/client/campaigns/route.ts:90`) and missed the campaign DETAIL beside it, so a client opening one
campaign met a bare number where the list carried a qualified one. **20 CLIENT accounts exist, so
this is a live screen, not a theoretical one.**

**THE NUMBER DOES NOT MOVE AND THAT IS THE POINT.** A row that fails `isMeasuredShare` has
`shares === 0` by construction, so it contributed nothing to the old sum either. Measured today,
GainzAlgo reports **117 shares across 764 approved clips, of which 97 were actually read**. 117 was
never wrong. It was never qualified. The fix adds the sentence "from 97 of 764 clips" underneath it,
in the exact wording and shape the list page has used since BL-820, so the two screens now agree.

Three further read-side omissions were found and **deliberately NOT changed**, because changing them
is not this round's job:

- `api/admin/fraud-review/route.ts:186` feeds `shares` into the shadow-ban heuristic without the
  label. Changing a detector's input changes who gets flagged for fraud. REPORTED, not touched.
- `api/admin/users/[id]/clips/route.ts:51` omits the label on an admin profile row.
- `analytics-summary.ts:311` still sums raw shares into `totalShares`, but **nothing renders it**:
  BL-820 removed Shares as a selectable metric from `/admin/analytics` (page.tsx:116). It is latent,
  not live, so the owner's impression was not formed there.

---

## PART 2 — THE CLIPPER WHO SEES $0.00

No clipper matches "earned $1.27". The one whose figures match the shape is **`cmq2is2j` (handle
redacted)**, and his position is exact:

| | |
|---|---|
| Clips, not deleted | 27 |
| Marked unavailable | **24** |
| Earnings across every clip | **$1.38** |
| Counted (approved, not unavailable) | **$0.00** |
| Held on unavailable clips | **$1.38** |
| Payout requests, ever | 0 |

All $1.38 of his money sits on flagged clips, which is why COUNTED reads $0.00. It is on exactly TWO
of the 24: `cmq4m52g` at $0.59 and `cmq3i4dz` at $0.79. The other 22 earned nothing and would show
$0.00 whatever their flag said.

**HIS VIDEOS ARE NOT BACK. I probed all 24 live and every one returned 404.** So the honest answer to
"is he owed anything unreachable" is **no**. Nothing is lost, nothing is stuck behind a bug, and the
$1.38 is sitting on his rows where the platform can see it. It is simply not payable while the videos
are gone, and it returns to his counted total automatically the moment either of those two is
readable again, with no action by anybody.

His clips, marked times against DB `now() = 2026-09-09 12:14:40.988807+00`, casts to `::text`:

| Marked (UTC) | Clips | Earnings | Campaign |
|---|---|---|---|
| `2026-07-18 19:09:41.778551` | 1 | $0.00 | GainzAlgo (REPOST) |
| `2026-07-18 19:09:57.398719` | **11** | $1.38 | GainzAlgo (REPOST) |
| `2026-07-18 19:10:11.545056` | 2 | $0.00 | GainzAlgo (REPOST) |
| `2026-07-23 06:00:19` to `06:03:27` | 10 | $0.00 | WinGram |

**Eleven of his clips carry the identical timestamp to the microsecond.** That is one statement, not
eleven verdicts.

### The sentence for the owner to send him

> Your clips are still earning what they earned. The $1.38 is recorded against your account and it
> has not been taken away. It is not being counted at the moment because the videos behind those
> clips cannot be opened from our side, and we only count a clip while we can still read it. I
> checked all 24 of them today and they are still unreadable. If any of them comes back, that clip
> starts counting again on its own and the money is there waiting. Nothing is lost.

---

## PART 3 — THE ONE-TIME REVIVAL SWEEP

### Population and cost, reported BEFORE anything was spent

**1,482 clips.** Reconciled exactly: 1,484 rows carry `videoUnavailable = true`, of which 2 are
`isDeleted` and correctly excluded, 0 are non-Instagram and 0 lack an account. All 1,482 are
Instagram, so the LamaTok rate never applies and YouTube is free.

At BL-838's measured HikerAPI rate of **$0.00069214**: 1,482 × $0.00069214 = **$1.026**. Under the
$10 ceiling, so the sweep proceeded.

**THE HONEST COST IS HIGHER THAN THAT AND I AM CORRECTING MY OWN FIGURE.** `fetchHikerInstagramByUrl`
issues ONE request for a live clip and **TWO** for a gone one, because a 404 from `by/code` falls
through to `by/url` (`hikerapi.ts:264`). Almost every clip here is gone, so the true worst case is
1,482 × 2 × $0.00069214 = **$2.05**. Still well under the ceiling, and stated so the ceiling is
measured against the real number rather than a flattering one.

### THE MONEY WAS NEVER REMOVED, AND THAT CHANGES WHAT THE SWEEP IS

**Only 6 clips in the entire population ever had earnings zeroed.** 603 clips still carry the full
**$3,966.69**, held across **45 clippers** (worst case $1,462.20, average $88.15). The money is
sitting in the rows. What the flag does is remove those rows from every query that filters
`videoUnavailable: false`, which is what turns EARNED $1.38 into COUNTED $0.00.

So reviving a clip is a **VISIBILITY** change, not a new credit. The earnings were recorded at
accrual and were already charged against campaign budgets then.

### RETROACTIVE OR FORWARD ONLY: retroactive, and the choice is not really the owner's

**Retroactive, because forward-only is not implementable without inventing something.** The product's
revival path (`tracking.ts:1753`) clears the flag and then recomputes earnings from CURRENT stats
through `writeClipEarnings`. Current stats already include every view accumulated while the clip was
flagged. There is no stored "views at the moment of flagging" to compute a forward-only figure from,
so forward-only would mean inventing a new baseline column and a new rule.

It is also the SAFE choice rather than the generous one, on three grounds: it is what the owner's own
Force Now button already does today, so this ships no new policy; the money was never deducted, so
nothing is being handed back; and **every campaign stays inside budget if every held penny returns**,
which was checked campaign by campaign before any write.

### What the sweep does, and why it cannot do damage

It **writes nothing itself**. It calls `runSingleClipCheck`, the exact function
`admin/clips/[id]/force-now/route.ts:205` calls, so the flag is cleared only at `tracking.ts:1753`
when a real fetch returns `views > 0`, and earnings recompute through the normal chokepoint with
BL-627, BL-538 and the budget hard lock all in the path.

**A CLIP STILL GONE IS NOT TOUCHED, BY CONSTRUCTION.** Detect and revive are separate runs: detect
probes and writes nothing, revive is handed an explicit id list that already answered ALIVE. There is
no code path that discovers and acts in the same pass, and no code path that writes a gone verdict at
all, so none can be widened. Independently, the marking branch at `tracking.ts:3327` is guarded by
`if (clipData && !clipData.videoUnavailable)`, so a re-check of an already-flagged clip cannot re-mark
it, cannot reset `videoUnavailableSince` and cannot restamp `savedEarnings`.

### THE RESULT: 34 of 1,482, and NOT ONE VERDICT RESTS ON A FAILED READ

**1,482 probed, 34 ALIVE (2.29%), 1,448 still gone.** The still-gone breakdown is the line that
matters most: `{"http_404": 1448}`. **Every single one was a clean 404.** There was not one timeout,
not one 429, not one 5xx and not one network error in 1,482 calls, so there is no clip anywhere in
this population whose gone verdict rests on a fetcher failing to reach it.

### THE FINDING THAT INVERTS THE INTUITION: THE CAREFUL PATH IS THE WRONG ONE

Splitting the population by what actually marked each clip:

| Marked by | Population | Money held | Alive again | Rate |
|---|---|---|---|---|
| **`retire-dead-clips` daily 06:00 cron** (audited: 3 consecutive live-probed 404s) | 761 | $466.37 | **33** | **4.34%** |
| **One bulk event, 2026-07-18 19:09:41 to 19:10:11** | 708 | **$3,482.17** | **1** | **0.14%** |
| other | 13 | $18.15 | 0 | 0% |

**The audited path is 31 times more likely to have been wrong than the bulk event**, and that is the
opposite of what I expected to find. It makes sense once stated: `retire-dead-clips` retires a clip
after three definitive 404s, which is exactly the signature of a temporarily private, blocked or
rate-limited account as well as a deleted one, and those come back. The bulk event caught videos that
were genuinely deleted.

**THE BULK EVENT IS A FINDING IN ITS OWN RIGHT AND IT IS UNEXPLAINED.** 708 clips across **94
accounts and 70 different clippers**, every account APPROVED so it is not a ban cascade, flagged in
**three database writes inside thirty seconds** at identical microsecond timestamps. That is three
statements, not 708 verdicts. It carries **87.8% of all the held money**. And `audit_logs` for that
entire two-and-a-half-hour window contains exactly one row, an unrelated
`ACCOUNT_VERIFY_ATTEMPT`. **The largest money-affecting event in this population has no audit trail at
all.** It appears to have been substantially correct, which is luck rather than design.

### WHAT THE REHEARSAL CAUGHT, AND IT WOULD HAVE BEEN A SILENT FAILURE

The sandbox rehearsal is the reason this round shipped a fix rather than a no-op. Built five clips 30
days old, called the real `runSingleClipCheck(id, "force-now")` on four of them, and got:

```
  a: old-clip-fallback-skipped  earnings 12.34 -> 12.34   flag true -> true
  b: old-clip-fallback-skipped  earnings 0 -> 0           flag true -> true
  RESULT: 13 passed, 4 failed.
```

**Nothing fetched. Nothing revived. Zero provider calls.** `processTrackingJob` gates the individual
fetch on clip age at `tracking.ts:1358`, and `runSingleClipCheck` passes `prefetchedStats = null`, so
**any clip older than 48 hours returns `old-clip-fallback-skipped` without fetching.**

**THAT MEANS THE OWNER'S OWN FORCE NOW BUTTON HAS BEEN A NO-OP ON EVERY CLIP OLDER THAN TWO DAYS.**
Every one of the 1,482 is far older than that. The owner has had no working manual way to bring any
of them back, and the sweep would have reported "0 revived" and looked like proof that nothing was
recoverable.

### THE ONE MONEY-FILE CHANGE, AND THE JUSTIFICATION

`tracking.ts` is a money file and the brief requires it byte-identical unless a fix genuinely needs
it. This one genuinely needed it. **The full diff is 29 lines, of which 28 are comment and ONE is
logic:**

```diff
-      if (clipAgeHours >= FALLBACK_AGE_LIMIT_H) {
+      if (clipAgeHours >= FALLBACK_AGE_LIMIT_H && source !== "manual" && source !== "force-now") {
```

Loudly, then: **the gate is a CRON cost guard and it was never meant to reach a deliberate check.**
Its own comment says so, describing a saving of "15-35% of cron Apify calls" and a clip that "can
wait one more cron tick (5-10 min) for the next batch attempt". For a flagged clip there is no next
tick, because the cron's due-jobs filter excludes `videoUnavailable: true` (`tracking.ts:3719`), so it
waits for something that structurally never comes. **The exemption is the codebase's own idiom, not a
new invention:** `tracking.ts:1926` already reads `source !== "manual" && source !== "force-now"` to
exempt exactly these two sources from an old-clip gate. **Cron behaviour is byte-identical** —
`source === "cron"` still takes the branch and the saving is untouched — and a deliberate check stays
bounded by the Apify cap and the individual-fallback cap immediately below it, both of which fired
during the real run and behaved correctly.

Re-run against the fix: **17 passed, 0 failed.** Clip A revived and its earnings recomputed $12.34 to
$18.23; clip B, the six-row zeroed shape, came back from $0.00 to $1.19 with `savedEarnings` cleared;
the clip pointing at a genuinely gone URL came out **byte-identical including its gone timestamp**;
the clip that was never named came out byte-identical; and all four money invariants held.

### THE REAL RUN

Two passes, because the first hit the individual-fallback cap at 25 and **correctly deferred the rest
untouched** rather than pushing through it. The snapshot and the exact rollback were printed before
either pass wrote anything: **34 `UPDATE clips SET ...` statements, valid before the first write**,
and saved to `C:/bl865-sweep/rollback.sql`.

**34 revived, 0 failed, 0 still flagged.** Flagged population 1,484 to 1,450.

**$33.30 is counting again for 6 clippers, and only $0.21 of it is new.** That single pair of numbers
is the whole thesis: 99.4% of the money that came back was already recorded on the rows and merely
hidden by the flag. The rest is the ordinary recompute from views the clips accumulated meanwhile.

## PART 4 — THE RECURRING LIVENESS CHECK

### The hole it fills

`tracking.ts:3719` filters the cron's due-jobs on `clip.videoUnavailable: false`. **A flagged clip is
excluded from every future tick, so the revival path at `tracking.ts:1753` is structurally
unreachable for exactly the clips that need it.** 1,365 tracking jobs are still active on flagged
clips and none of them will ever be polled. Today the only way back is the owner pressing Force Now
by hand.

`src/lib/clip-liveness-recheck.ts` is the return leg, wired at
`/api/cron/clip-liveness-recheck` and registered in the scheduler at **daily 07:00 UTC**, an hour
after retire-dead-clips so the two never hit the provider in the same minute.

### It fails open, and that is checkable rather than argued

**The module contains no write of `videoUnavailable: true`.** Not behind a flag, not in a catch, not
anywhere. One grep settles it. The probe is read-only and separate from the revival: only a clip that
already answered ALIVE is handed to `runSingleClipCheck`. A provider outage, a rate limit, a timeout
or a bad deploy therefore produces exactly zero writes.

**I GOT THE REASON FOR THAT SPLIT WRONG FIRST AND THE CORRECTION IS WORTH STATING.** I wrote that
driving `runSingleClipCheck` over the whole population would strike every gone clip on the auto-ladder
and bell the owner about it, since 1,457 of 1,482 sit below the 3-failure threshold. **The code says
otherwise.** A gone Instagram clip classifies as `infra`, and the INFRA_DEFER branch at
`tracking.ts:1507` explicitly does not increment the counter; the 385 REJECTED ones are not
ladder-eligible and return earlier at `tracking.ts:1529`. Neither group strikes and neither bells. The
real reasons the split is right are that a gone clip still gets its tracking job rewritten every day
to no purpose, that the no-strike behaviour depends on `INFRA_FAILURE_CLASSIFICATION_ENABLED` whose
production value I cannot read, and that a grep beats an argument.

### The consecutive-failure stop

**A 404 is an ANSWER, not a failure**, and it resets the run. A failure is a 429, a 402, a 5xx, a
network error or a missing key. After **10 consecutive failures** the run halts, reports the last HTTP
status and how far it got, and marks nothing. The clips it never reached are simply due next cycle.

### Cadence and cost, against both ceilings

Every clip is rechecked every five days. The population splits into five deterministic buckets by an
FNV-1a hash of the clip id and one bucket runs each day, so there is **no new column, no migration and
no state** — the bucket is a pure function of the id and the date.

- ~297 clips a day, at two requests each for a gone clip: **$0.41 a day, $12.51 a month**
- against the existing Instagram spend of about **$139 a month**, that is **about 9%**
- **against BL-856's 4,320-snapshot-a-day ceiling it is free.** `processTrackingJob` writes a
  `ClipStat` row only on a successful fetch, so a gone clip produces no row. Only an actual revival
  writes one, and a revival is a clip rejoining the normal cron where its snapshots were always
  budgeted for.

### IT DEPENDS ON THE `tracking.ts` FIX, AND WOULD HAVE BEEN A SILENT NO-OP WITHOUT IT

Worth stating plainly because it is the kind of thing that ships green and does nothing: the recheck
revives through `runSingleClipCheck`, which is exactly the call the 48-hour gate was swallowing. Every
clip this job will ever look at is older than 48 hours by definition. Without the one-line change in
PART 3 this cron would have run every day, spent the money, logged "0 revived" for ever, and looked
like proof that nothing was recoverable.

### The owner is told, because money starts moving

A new notification type `CLIP_REVIVED`, registered at all four sites a type must appear
(`notifications.ts`, `notif-href.ts` → `/clips`, `notification-toast.tsx` as emerald CheckCircle2,
and left at the default `info` severity because it is good news). `Notification.type` is a free-form
String column so **no migration is needed**.

The owner gets **ONE summary per run** with the count and the money, never one bell per clip, because
a burst of hundreds is how a real signal gets muted. The clipper gets one per clip, because the total
he has been watching read $0.00 is his own.

---

## PART 5 — THE PROOF

**The sandbox, BL-842's tooling, `SANDBOX_ROUND=bl865`.** Three fixtures were built and destroyed:
one render fixture (31 rows), one pre-fix rehearsal (32 rows) and one post-fix rehearsal (34 rows,
including 2 the product itself created and the sweep adopted). Every id was ledgered at creation and
**only ledgered ids were deleted**: 31 of 31, 32 of 32 and 34 of 34, each reported `0 already gone, 0
FAILED` and `VERIFIED: 0 of N recorded rows remain`.

`verify-gone.ts`: **50 checks, 50 passed, 0 failed.** The real payout fingerprint
(`c8a12e5d321a319fc337dbdc27af42a2`) and the real user fingerprint
(`b03e13c0c386b05e6958e5d107dd7c35`) are byte-identical before and after. The counts that did move are
attributed to the live platform rather than waved at: during the round window one real clipper
submitted one clip and the cron wrote 77 view snapshots. Zero real signups, zero payouts created,
zero audit rows.

**The money invariants, across the FULL population, not just the touched rows.** 9,802 clips and 120
PAID payouts fingerprinted either side of the revive:

| Invariant | Result |
|---|---|
| BL-538 never decrease | **PASS** — 0 clips lost money (7 gained, 34 un-flagged) |
| BL-824 paid is final | **PASS** — 0 PAID payouts changed, 0 vanished |
| BL-696 no double pay | **PASS** — 0 new PAID payouts appeared |
| BL-627 no overpayment | **PASS** — 0 campaigns over budget |
| `earnings == base + bonus` | **PASS** — 0 clips break it, and 0 did before |

The baseline was taken FIRST and was already clean, so nothing here is attributed to the sweep that
was not caused by it.

**The render pass, BL-793's method: 65 assertions, 0 failures, 10 shots.** Both share-coverage states
at 320, 375, 414, 1280 and 1440, against a PRODUCTION BUILD with `DEV_AUTH_BYPASS=false` and a real
minted Auth.js cookie. `window.innerWidth` was read back and matched at every width, horizontal
overflow was 0 at every width, and the splash lifted on every shot. The partial-coverage campaign read
"163" with the note "from 3 of 8 clips" tied by `aria-describedby`; the fully-measured campaign read
"94" with **no note and no `aria-describedby`**, which is the assertion that stops the note being
decoration.

The render fixture could not use `isTestCampaign` (the route 404s test campaigns for every non-owner,
so it would have photographed a 404), and rendering as an OWNER was rejected because owner rows are
enumerated for email fan-out with no `isTestUser` filter. It used an **archived, paused, member-less**
campaign instead, invisible because `api/campaigns/route.ts:110` applies `isArchived = false` to every
live list for every role.

**The accessibility review ran and it changed the code.** One MUST FIX: the coverage note was three
sibling paragraphs away from the number with nothing tying them, so a reader navigating by paragraph
would meet "from 3 of 8 clips" orphaned. Fixed with `aria-describedby`, no visual change. Contrast
passed at a measured 18.4:1, CSS-off resilience passed, reading order and landmarks unaffected. One
pre-existing house-rule breach was reported and NOT fixed here: all eight metric icons lack
`aria-hidden`, which predates this round and applies across the whole grid.

**Builds, from a log, with the exit code echoed rather than inferred.** Build #1 `BUILD1_EXIT=0`,
0 TS errors. All four prebuild gates ran and passed: prisma-bypass 0 violations, removed-fields OK,
event-wiring 0 problems, and the BL-348 hooks gate **0 errors, 10 warnings against a limit of 11**,
every warning in a file this round did not touch. eslint is genuinely present (three binaries in
`node_modules/.bin`), so the gate is not a silent no-op. Build #2, taken AFTER the `tracking.ts`
change: **`BUILD2_EXIT=0`, 0 TS errors, hooks gate 0 errors / 10 warnings.** The baseline before any
edit was also clean (`TSC_BASELINE_EXIT=0`, 0 errors), so no error here is attributed to the wrong
cause.

*A note on build honesty: the background runner reported build #1 as "failed with exit code 1". It did
not fail. The script's last command was `grep -c "error TS"`, which exits 1 when it finds zero
matches. The real exit code was captured before it, which is exactly why it is captured rather than
inferred.*

**Byte-identity by blob OID on BOTH refs.** Six of the seven are IDENTICAL:
`clip-earnings-writer.ts` `ac5be7deb061`, `earnings-calc.ts` `797e20985ad5`, `balance.ts`
`81a683c1a6ed`, `clip-earnings-invariant-middleware.ts` `61cef3939536`, `money-decimal.ts`
`ef5cdae757b9`, `campaign-era.ts` `106e16ad7512`. **`tracking.ts` CHANGED, deliberately, and the full
diff is printed above**: one line of logic, `9563a4fc9994` to `89292141`.

**Provider discipline.** No Apify actor ran; the 11 BL-678 `APIFY_HARD_OFF` guards are intact and the
rehearsal log shows the product itself refusing one (`[SKIP-APIFY] reason=gone-404`). No schema
change, no `prisma migrate`, no index. No Supabase pool errors. `checkpoint/BL-723` confirmed NOT an
ancestor of main. No collision: the shared tree held 0 modified tracked files and only this worktree
existed.

**Every probe and its cost, disclosed.** 20 + 20 newest/oldest marks, 64 random-and-named-clipper
calls, 1,482 detect calls, 10 rehearsal calls across two runs, plus the revive's own fetches:
**about 1,600 HikerAPI requests, roughly $1.10.** One call per clip, no actor, nothing batched.

*One disclosure about my own tooling: after I parameterised the first probe's ordering, its console
line still printed "newest marks first" while it was querying oldest-first. The dates in its output
prove the ordering actually changed; only the label was wrong. No conclusion in this report rests on
that run.*

---

## WHAT THE OWNER MUST DO

1. **Redeploy on Railway.** Nothing here is live until then, including the Force Now fix.
2. **Add `clip-liveness-recheck` to `RAILWAY_NATIVE_CRON`**, or confirm it already contains `*`. The
   scheduler only fires jobs named in that allowlist (`railway-cron-scheduler.ts:111`). **I could not
   read its production value from here, so this is unverified and PART 4 does nothing until it is
   done.** This is the one step where an unread environment variable decides whether the round works.
3. **Send the sentence in PART 2** to the clipper. His $1.38 is safe and not payable yet.
4. **Decide what to do about `retire-dead-clips`.** It is retiring roughly 30 to 70 clips a day at a
   measured 4.34% false-positive rate. The liveness check now returns those clips, but it returns them
   after up to five days rather than preventing the retirement. Raising its threshold from 3 to 4 or 5
   consecutive gone verdicts would cut the inflow at source, and it is a one-number change I have
   deliberately NOT made because it is a policy decision about his money, not a defect.

## HOW THE WORK WAS SPLIT ACROSS MODELS

The brief's new rule, applied and stated.

**Opus (this session) did everything that decides money or data**, and none of it was delegated:
deciding what the sweep writes and how, reading `tracking.ts`'s marking, revival and ladder branches,
the retroactive-versus-forward-only judgement, the cost arithmetic, the cron design in PART 4 (which
CLAUDE.md pins to Opus regardless), the SQL that measures the money, and this report.

**Sonnet did one job**: the mandatory accessibility review of the one changed user-facing surface. It
returned one MUST FIX (the coverage note was not programmatically tied to the number it qualifies) and
that fix is in. Contrast, CSS-off resilience and reading order it passed cleanly, with the measured
ratio quoted.

**Nothing money-touching was split, and that is deliberate.** The obvious candidates for a cheap tier
were the probe runs and the row counting. They were not delegated, because a subagent reporting "24 of
24 came back 404" is a claim about whether a clipper is owed money, and the round already contains one
case of my own first explanation being wrong (the auto-ladder burst, above). Measurement that decides
money is not mechanical work.
