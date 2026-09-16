# BL-880 — marketplace v2, round four: teaching the tracking tick to pay 45 percent

> **NOTHING IS UNREMOVABLE AND NO SQL IS OWED. FIRST LINE, AS THE ROUND REQUIRES.**
> 263 ledgered rows, **`VERIFIED: 0 of 263 recorded rows remain`**, 0 failed, 0 cascaded. A direct
> catalogue sweep afterwards returns **zero** `bl880sbx-` rows in `users`, `campaigns`, `clips` or
> `clip_accounts`, **zero** rows in all five v2 tables, **zero** clips carrying `marketplaceV2PostId`
> and **zero tracking jobs of any kind behind a v2 clip**. Campaigns are back to **34**, all **34**
> NORMAL, with the fingerprint `e9defb11fcf63f2a100fbb1a63ed98de` identical to the opening snapshot.

**2026-09-16. Shipped on `checkpoint/BL-880`, merged to `main`. Requires a Railway REDEPLOY**, and
BL-877's, BL-878's and BL-879's are all still owed. Base `origin/main` @ `7b66447`. Isolated worktree
`C:\w\b880`, a short path, `node_modules` never junctioned, **removed at the end and verified by
listing the path**. DB `now()` **17:35** (opening snapshot) to **17:42:21.693221+00** (closing
sweep), every timestamp cast `::text`.

---

## THE HEADLINE

> **1. `tracking.ts` CHANGED FOR THE THIRD TIME, AND THE SHAPE OF THE CHANGE IS THE FIRST THING TO
> SAY: 212 INSERTIONS AND EXACTLY ONE DELETION.** That one deletion is
> `const totalForThisClip = newEarnings + newOwnerAmt;`, replaced by the same line with the two v2
> legs added to the projection. **Everything else in the diff is pure insertion.** The full diff is
> printed below and every hunk is justified. The other six protected money files plus
> `campaign-era.ts` are byte-identical by blob OID on both refs.
>
> **2. THE FREEZE WAS WATCHED HAPPENING, NOT ARGUED.** The round named it as the subtlety that
> matters most, so it was demonstrated: the editor-leg update was deliberately withheld for one tick
> and **the poster climbed to $54.00 while the editor stayed frozen at $13.50**. Nothing in the
> platform would have noticed, because the invariant middleware watches `Clip.earnings` alone. The
> update was restored and both came back in step at **$54.00**.
>
> **3. THE LEGS GROW IN LOCKSTEP AND SUM EXACTLY, MEASURED ACROSS FIVE TICKS.** 2,000v $0.90/$0.90,
> 6,000v $2.70/$2.70, 10,000v $4.50/$4.50, 18,000v $8.10/$8.10, 30,000v $13.50/$13.50, with the three
> legs summing to the recomputed gross **exactly at every tick**.
>
> **4. ADDS SURVIVED, AND BREAKING IT WAS THE EASY MISTAKE.** The v2 fork closes ABOVE the untouched
> `if (isCpmSplit)` agency block, so a v2 clip still writes and still grows its `AgencyEarning` row.
> A fix that routed v2 around that branch to control the split would have turned ADDS into REPLACES
> **with no error anywhere**.
>
> **5. A SECOND WRITE SITE WAS FOUND AND CLOSED.** The approve path has the same
> `if (isMarketplaceClip) ... else ...` shape and its else branch writes the FULL clipper rate. That
> is BL-824's own lesson about a patch at one site leaving the other wrong.

**PROOFS: 26 of 26 sandbox checks passed, 0 failed**, after a first run that failed 2. Both failures
are real, both are reported in full below, and one of them was a defect in the proof rather than in
the product.

---

## PART 0 — THE MODEL SPLIT, AND WHAT WAS CHECKED AGAINST SOURCE

| tier | what ran there | subagents |
|---|---|---|
| **cheapest (Haiku)** | nothing. **This round used no retrieval subagent at all** | **0** |
| **strongest (Opus), NOT SPLIT** | every line of the read-only map, every character of the `tracking.ts` change, the review-route change, the recompute path, the branch placement, every interaction analysis, the proof scripts and this report | **0 subagents between it and the source** |

**THE ROUND WARNED THAT TWO PRIOR ROUNDS RECORDED SUBAGENTS MISCHARACTERISING A DESIGN, AND SAID TO
CHECK EVERY CLAIM AGAINST THE FILE.** The strongest answer to that warning was to use none: the only
file that decides who gets paid is `tracking.ts`, and nothing between it and the model would have
made the change safer. Every figure in this report was read out of the file or measured against the
live database.

**BL-879's finding was confirmed independently rather than inherited**, and the confirmation is
below.

---

## PART 0b — THE TICK'S MONEY PATH, MAPPED READ-ONLY BEFORE ONE CHARACTER CHANGED

Every line reference is to `src/lib/tracking.ts` **as it stood at `pre-BL-880`**.

| step | `file:line` | what happens |
|---|---|---|
| the money variables are declared | `:2112-2115` | `newEarnings`, `newOwnerAmt`, `newCreatorAmt`, `newPlatformAmt`, all zero |
| the economic snapshot is resolved | `:2121` | `resolveClipEconomicFields(clip, clip.campaign)`, snapshot-first with a live fallback |
| **`isCpmSplit` is computed** | **`:2122-2124`** | `!isMarketplaceClip && econ.pricingModel === "CPM_SPLIT" && campaign.ownerCpm` |
| the CPM pair is resolved | `:2129-2137` | override, then frozen, then per-platform, then legacy |
| **the v1 marketplace fork** | `:2140-2196` | `calculateMarketplaceEarnings` sets the 60/30/10 legs and `newEarnings = mktBreakdown.poster.total` |
| **the ordinary fork** | `:2197-2221` | `recalculateClipEarningsBreakdown` sets `newEarnings = breakdown.clipperEarnings`, the FULL clipper rate |
| the owner's ordinary cut | `:2250-2256` | `calculateOwnerEarningsGuaranteed` or `calculateOwnerEarnings`, from the full gross |
| the payout reduction cap | `:2275-2300` | a MULTIPLIER, immutable once set, applied to every figure |
| the guarantee and proportional cuts | `:2330-2410` | scale the clipper side, bonus shrinking first |
| **the retry snapshot** | `:2424-2431` | so a Serializable retry starts from the same inputs and cannot double-cap |
| **the Serializable transaction opens** | `:2436` | `db.$transaction(..., { isolationLevel: "Serializable" })` |
| the committed-spend read | `:2541-2559` | clips, agency, and both v1 marketplace legs, inside the transaction |
| **the v1 per-tick truncation** | `:2498-2536` | ratio-caps the poster, creator and platform legs **together** |
| **the ordinary per-tick truncation** | `:2576-2698` | the guarantee cap, the no-remaining hold, the ratio cap and BL-718's paid floor |
| the owner lock | `:2703-2740` | re-derives the owner amount from the FINAL clipper amount |
| **the v1 write** | `:2833-2947` | the poster floor, then `writeClipEarnings`, then both v1 leg writers |
| **the ordinary write** | `:2949-2995` | `writeClipEarnings` with the full amount, then **`agencyEarning.upsert` gated on `isCpmSplit`** |
| the transaction closes | `:2998` | |

### WHAT A V2 CLIP DID BEFORE THIS ROUND, CONFIRMED INDEPENDENTLY

A v2 clip carries **`isMarketplaceClip = false`**, on purpose, because true would route it through
the first marketplace's 60/30/10 in four separate branches. So at `:2122` it satisfies
`!isMarketplaceClip`, at `:2140` it does **not** take the v1 fork, and at `:2197` it takes the
ordinary one, where `newEarnings = breakdown.clipperEarnings`.

> **THAT IS THE FULL CLIPPER RATE. A v2 clip reaching the tick would have been paid ONE HUNDRED
> PERCENT of a rate it is owed FORTY FIVE PERCENT of**, and `:2956` would have written it through
> `writeClipEarnings` with every existing test passing. BL-879 measured this and shipped every v2
> tracking job INACTIVE rather than let it happen. **Confirmed here from the file, not inherited.**

### IT RECOMPUTES FROM TOTAL VIEWS, AND THE WHOLE SHAPE OF THE FIX DEPENDS ON THAT

Every branch passes **`views: stats.views`**, the clip's TOTAL view count, into its calculator, and
**nothing anywhere in the file does `newEarnings +=`**. The proof asserts both. So each pass computes
what the clip is worth in total and overwrites, forever, rather than adding a delta once.

> **THEREFORE ALL THREE LEGS MUST BE REWRITTEN ON EVERY PASS FROM THE SAME GROSS.** If only
> `Clip.earnings` were taught the split and the other two were written once at post time, the
> editor's 45 percent would freeze at whatever the clip earned in its first hour while the poster's
> kept climbing. **That is exactly what PART 1 demonstrates happening.**

### EVERY OTHER CALLER THAT WRITES CLIP EARNINGS, ENUMERATED

`grep` for `writeClipEarnings(` across `src`, excluding the writer itself, returns **thirteen call
sites in ten files**:

| site | can a v2 clip reach it | what this round did |
|---|---|---|
| `tracking.ts` (the tick) | **yes, by design** | **FIXED. This round's subject** |
| `clips/[id]/review/route.ts:829` (v1 approve) | no, gated on `isMarketplaceClip` | untouched |
| **`clips/[id]/review/route.ts:958` (ordinary approve)** | **YES** | **FIXED. See PART 2** |
| `marketplace-v2-writer.ts:146` | yes | already correct, BL-877's |
| `owner-submit-core.ts:346` | no, a v2 clip is never created there | untouched |
| `cpm-restamp.ts:190` (BL-866's devaluation) | **yes, if an owner devalues the campaign** | **NOT fixed. Named for Round Five, see PART 4** |
| `gamification.ts:1169` | **yes, on a level or streak recompute** | **NOT fixed. Round Five** |
| `campaign-freeze-undo.ts:390` | yes, on an undo | **NOT fixed. Round Five** |
| `clips/[id]/override/route.ts:244` | yes, owner-run | **NOT fixed. Round Five** |
| `admin/fix-budget/route.ts:260,315` | yes, owner-run repair | **NOT fixed. Round Five** |
| `admin/fix-earnings/route.ts:183,407` | yes, owner-run repair | **NOT fixed. Round Five** |
| `admin/force-recalc-earnings/route.ts:310` | yes, owner-run repair | **NOT fixed. Round Five** |
| `admin/payouts/[id]/adjust/route.ts:485` | yes, owner-run | **NOT fixed. Round Five** |

**THIS IS STATED PLAINLY RATHER THAN GLOSSED.** Eight sites remain that would write a v2 clip the
full clipper rate **if an owner ran them**. None is reachable by a clipper, all are owner-initiated,
and none runs on a schedule. The tick and the approve path are the only two a v2 clip meets without
somebody deciding to press something, and both are fixed. **Round Five's first job is the other
eight**, and the right shape is one shared helper rather than eight copies of the split.

---

## PART 1 — THE RECOMPUTE

### The mechanism, and why an upsert rather than a delete and rewrite

The editor and platform legs are written through `writeMarketplaceV2Earnings`, which **upserts keyed
on `clipId`**. That was a choice against concurrency and it is justified rather than assumed:

* **`clipId` is UNIQUE on both tables**, with the indexes applied `CONCURRENTLY` and verified in
  `pg_indexes` by BL-877. So two ticks racing the same clip either serialise or conflict and retry
  under Serializable.
* **A delete-and-rewrite would leave a window with no row at all.** Any aggregate reading the table
  in that window, including the spend aggregate the budget lock depends on, would see the clip's
  editor and platform money as zero.
* **An upsert preserves `streakBonusPercentAtApproval`**, which a re-create would lose. That is the
  Persona-10 defect the first marketplace already had to fix, and its own comment at `:2903-2908`
  says so.
* **An incremental update was rejected outright** because the tick recomputes from total views. An
  increment would compound on every pass.

### The residual, on every recompute

The platform leg is the RESIDUAL of the other two on every pass, never an independent
multiplication, exactly as BL-877 built it. Proved across **4,520 generated view counts**, including
every integer to 4,000, eight primes times forty, and 200 sub-cent boundary values:

> **4,520 of 4,520 summed exactly. 0 wrong. Worst drift $0.0000.**

### The lockstep, across five ticks

One post on a campaign with room to grow, ticked five times with climbing views:

| views | poster | editor | platform | three legs | gross |
|---|---|---|---|---|---|
| 2,000 | $0.90 | $0.90 | $0.20 | **$2.00** | $2.00 |
| 6,000 | $2.70 | $2.70 | $0.60 | **$6.00** | $6.00 |
| 10,000 | $4.50 | $4.50 | $1.00 | **$10.00** | $10.00 |
| 18,000 | $8.10 | $8.10 | $1.80 | **$18.00** | $18.00 |
| 30,000 | $13.50 | $13.50 | $3.00 | **$30.00** | $30.00 |

### THE FREEZE, DEMONSTRATED AND THEN RESTORED

The round asked for the freeze to be watched rather than asserted, because a guard nobody has seen
fail proves nothing. So the editor-leg update was deliberately withheld for one tick, writing only
`Clip.earnings` through `writeClipEarnings`, which is exactly what a round that taught the split to
one leg would have produced:

> **The poster climbed to $54.00. The editor stayed frozen at $13.50.**
>
> **Nothing in the platform would have noticed.** `clip-earnings-invariant-middleware.ts` asserts
> `earnings == baseEarnings + bonusAmount` on `Clip` and has no opinion about a row in another table.
> The editor would have been short **$40.50 on one clip** with every test green.

The update was then restored through the real writer and both legs came back in step at **$54.00**.

---

## PART 2 — WHERE THE BRANCH GOES

### The identification

**A v2 clip is `(clip as any).marketplaceV2PostId` being set.** Never `isMarketplaceClip`, which must
stay FALSE. The proof asserts both halves in source: the v2 branch keys on `marketplaceV2PostId`
while `isCpmSplit` still keys on `!isMarketplaceClip`, unchanged.

### One fork, and the four places it had to be known

The round asked for one branch at one point. **The money decision IS one fork at one point**, at the
write site. But three other places had to learn the two new figures exist, and every one of them is a
place the FIRST marketplace already had to touch for exactly the same reason:

| what | why it could not be avoided | v1's equivalent |
|---|---|---|
| **the compute**, after the ordinary branch | the legs have to exist before anything can cap them | `:2174-2196` |
| **the reduction cap** | `payoutReductionRatio` is a multiplier and immutable; a poster reduced without his editor and platform legs reduced stops summing | `:2295-2300` |
| **the retry snapshot** | a Serializable retry starting from attempt 1's capped legs would cap them twice | `:2427-2428` |
| **the budget projection** | without the two legs in `totalForThisClip`, 55 cents in every dollar is invisible to the per-tick cap | `:2498` |
| **the write** | the one money fork | `:2924-2947` |

### The controls, measured

| clip | before BL-880 | after BL-880 |
|---|---|---|
| **a NORMAL clip**, 10,000 views, $1.00 CPM | $10.00, the full rate | **$10.00, identical to the cent** |
| **a V2 clip**, same views, same CPM | would have been $10.00 | **poster $4.50, editor $4.50, platform $1.00** |
| **a V1 MARKETPLACE clip** | 60/30/10 through its own writers | **untouched. No BL-880 line enters the `isMarketplaceClip` branch** |

### The second write site, and BL-824's lesson

`clips/[id]/review/route.ts` has the same `if (isMarketplaceClip) ... else ...` shape, and its else
branch at `:958` writes `finalClipperEarnings`, the **FULL** clipper rate. A v2 clip takes that
branch.

**A v2 clip now gets NO earnings write on approval at all**, rather than a second copy of the split:

* **Nothing is lost.** A v2 post is created with zero views and an inactive job, so its earnings are
  $0.00 at the moment of approval whatever that branch would have computed. The tick picks it up on
  its next pass.
* **A second copy of the split is the thing that drifts.** BL-539 measured what a second source of
  truth for a money rule costs at $933.94.
* **And skipping closes a sharper hazard.** If that branch wrote the full rate once, BL-538's
  never-decrease guard could then refuse the tick's correction downward, freezing the clip at the
  wrong figure permanently.

---

## PART 3 — THE ADDS DECISION SURVIVED

Mechanically, ADDS means the `AgencyEarning` row must still be written for a v2 clip on every tick,
because a v2 clip carries `isMarketplaceClip` FALSE and therefore satisfies `isCpmSplit`.

> **THE EASY MISTAKE WOULD HAVE BEEN TO ROUTE V2 CLIPS AROUND THE `isCpmSplit` BRANCH TO CONTROL THE
> SPLIT.** That would have stopped writing the agency row and turned ADDS into REPLACES silently,
> with no error anywhere and no test failing.

**The v2 fork therefore closes ABOVE the `if (isCpmSplit)` block**, which is byte-identical to
before, and both paths reach it. The proof asserts the ordering in source and the agency upsert's
presence.

**On a real campaign, not an illustrative figure.** `Zhus Edit (0.50 CPM)`, ACTIVE, CPM_SPLIT, owner
share **39.0021 percent**:

| | owner nets per $100 of v2 gross | campaign spends |
|---|---|---|
| REPLACES | $18.10 | $100.00 |
| **ADDS** | **$57.10** | **$139.00** |

**Identical to what BL-877 and BL-878 printed for the same campaign.** `MARKETPLACE_V2_PLATFORM_CUT_MODE`
reads `ADDS` and `v2AgencyEarningApplies()` returns true.

---

## PART 4 — EVERY INTERACTION, ONE BY ONE

### BL-627's three budget mechanisms, ACROSS TICKS

Fifty posters on one clip, one **$100** budget, five tick passes:

| | |
|---|---|
| money writes refused by the **L1 hard lock** | **200** |
| `getCampaignBudgetStatus().spent` | **$100.00** against a **$100.00** budget |
| poster legs / editor legs / platform legs | **$45.00 / $45.00 / $10.00**, summing **$100.00** |
| what `spent` would read without both v2 aggregates | **$45.00**, hiding **55.0 percent** |

* **Per-tick truncation inside the Serializable transaction:** intact, and the two v2 legs are now in
  its projection.
* **The L1 hard lock reading COMMITTED spend and throwing:** intact and firing, 200 times.
* **Per-campaign sequential tracking:** unchanged; nothing in this round touches the batching.

**WHAT HAPPENS TO THE OTHER TWO LEGS WHEN THE POSTER'S IS TRUNCATED:** they are scaled by **the same
factor**, and the platform leg is then taken as the **RESIDUAL of the scaled gross**, so the three
still sum exactly after a cap binds rather than by two roundings agreeing. The poster's own base and
bonus follow the total by the same residual technique BL-849 used for its floor, or the L1 invariant
would refuse the write and kill the whole tick's transaction.

### BL-538's never-decrease

`writeClipEarnings` treats the poster's leg exactly as it treats any clip's: its own header records
that decreases always pass, because a recompute can legitimately lower a figure when views fall and
BL-753 measured 1,245 legitimate decreases across 650 clips. **The editor and platform legs go
through `writeMarketplaceV2Earnings`, which carries BL-538's never-decrease guard on the editor leg
explicitly** (BL-877 built it there, with a `[MARKETPLACE-V2-NEVER-DECREASE] BLOCKED` log line and a
fail-safe that keeps the value the editor has already been shown).

### BL-824 paid-is-final, with TWO earners on one clip

**Each floor is respected independently and neither can be pushed below money already paid to that
person.** The poster's floor lives in `writeClipEarnings` and compares against `Clip.earnings`, which
holds his 45 percent and nothing else. The editor's floor lives in `writeMarketplaceV2Earnings` and
compares against his own row. They read different columns and cannot interfere.

Measured across the full population: **zero clips carry two agency rows, zero carry two v2 editor
rows**, and the 26 positions sitting below money already paid are pre-existing. **This round created
zero payout rows.**

### BL-866's devaluation, and this is the one that is NOT closed

A devaluation restamps the per-clip CPM pair rather than rewriting stored earnings, so **on a v2 clip
the restamped rate feeds all three legs at once on the next tick**, which is correct and needs no
work. The gap is different and it is named honestly: **`cpm-restamp.ts:190` itself calls
`writeClipEarnings` with a full-rate figure**, so an owner devaluing a campaign would write a v2
clip's poster leg at 100 percent once, before the next tick corrects it. Whether BL-538's guard then
blocks the correction downward **was not determined in this round** and is Round Five's first item.

### Retire and dead-clip paths

A v2 clip flagged `videoUnavailable` drops out of every earnings aggregate through the standing
`videoUnavailable: false` filter, which BL-877's aggregates carry. **BL-874's rule holds unchanged:
this round adds no path that records a failure as a fact about a video.** What happens to the two v2
rows when a clip is retired **was not exercised** and is stated as such.

### The two bonus stacks, measured

A $100 gross clip with a 10 percent editor bonus and a 5 percent poster bonus:

| leg | amount |
|---|---|
| editor | **$49.50** |
| poster | **$47.25** |
| platform | **$10.00** |
| **disbursed** | **$106.75** |

**The platform's $10.00 is 9.37 percent of what actually leaves**, matching BL-876's prediction to
the cent. **Bonuses recompute per tick alongside the base**, because the tick passes both parties
into `calculateMarketplaceV2Earnings` on every pass; nothing is frozen separately. **And with ADDS
on, the owner's ordinary cut is charged to the campaign on top of all of it.**

---

## PART 5 — ACTIVATION, DONE LAST

BL-879 shipped every v2 tracking job INACTIVE so nothing could be paid wrongly. Activation was done
only after everything above was proven.

**THE COUNT TO ACTIVATE IN PRODUCTION IS ZERO.** Measured at DB `now()` **17:42:21.693221+00**: there
are **0** clips carrying `marketplaceV2PostId` platform-wide and **0** tracking jobs of any kind
behind one. That is the expected figure and it independently confirms BL-879's own "266 of 266 rows
removed".

**So what ships is the mechanism, not a one-off UPDATE.** The approve path now flips an existing
inactive job on when the owner approves a v2 clip, which is the moment it should start earning and
not before.

**Reverse it in one statement:**

```sql
UPDATE tracking_jobs SET "isActive" = false
 WHERE "clipId" IN (SELECT id FROM clips WHERE "marketplaceV2PostId" IS NOT NULL);
```

---

## PART 6 — THE 30 MINUTE WINDOW

**THE COUNTDOWN WAS REMOVED, AND IT WAS REMOVED IN BL-879 RATHER THAN THIS ROUND.** A countdown that
lies is worse than none, and the one BL-876 designed would have lied in both directions.

**The window applies to v2, and that was a decision rather than an inheritance.** `MAX_CLIP_AGE_MS`
is enforced per path, and BL-879 moved `checkFreshness` verbatim into `src/lib/clip-freshness.ts` so
the v2 post path and the first marketplace share one implementation. Without it, v2 would have been
the one door in the product through which a week-old video could be submitted for full credit.

**It is compared against the post's timestamp ON THE PLATFORM, never against anything the poster does
on this site.** So:

> **A poster who downloads a large file and posts an hour later is NOT refused.** The hour in Drive
> costs him nothing. What is refused is a poster who posts and then waits more than thirty minutes to
> paste the link, and **that refusal is correct**: the rule exists so the views-at-approval baseline
> stays near zero, which is what stops somebody letting a video run for a week and then claiming
> every view.

What he sees, before he leaves, is the rule in words with `MAX_CLIP_AGE_LABEL` imported so the copy
cannot drift: *"Take as long as you like downloading and making your post. The clock does not start
until your video is LIVE."*

---

## PART 7 — THE PROOFS, AND THE TWO THAT FAILED FIRST

### The opening snapshot, taken before anything was created

```
campaigns 34, clips 10180, users 1749
v2: clips 0, posts 0, editor 0, platform 0
agency 4882, payouts 248
ACTIVE tracking jobs 8605, of which behind a v2 clip 0
campaign fingerprint e9defb11fcf63f2a100fbb1a63ed98de
```

### THE FIRST RUN FAILED TWO CHECKS AND BOTH ARE REPORTED

**FAILURE 1, and it was a defect in the PROOF's design rather than in the product.** The growth and
freeze proofs were run on the same $100 campaign as the fifty-poster budget test. The budget was
exhausted on the first tick, the L1 lock refused every write after it, and the watched post sat at
$0.90 forever. **The budget proof was working correctly and the growth proof was impossible in the
same campaign.** Fixed by giving the watched post a second v2 clip on a campaign with room, and the
lockstep table above is the result.

**FAILURE 2, and it was a defect in the PROOF's assertion string.** A source check looked for
`"// BL-880 — ONE BRANCH, ONE POINT, AND THE AGENCY ROW BELOW"` while the inserted comment carries a
box-drawing prefix. The assertion was corrected rather than deleted.

**Neither failure was in the product.** They are reported because a round that only prints its
passes is not reporting.

### 26 of 26 checks passed on the second run

Everything the round named: the tick recomputing from total views; the branch keyed on
`marketplaceV2PostId`; the agency block outside the fork; BL-879's zero leftover jobs; the residual
across 4,520 view counts; fifty posts; the editor growing in lockstep; the three legs summing at
every tick; **the freeze demonstrated and restored**; the L1 lock firing 200 times; spend at exactly
the cap; all three legs truncating in step; the ADDS flag and its real-campaign figures; the agency
upsert reachable; a normal clip unchanged; a v2 clip at 45 percent; the v1 path untouched; the two
bonus stacks at $106.75 and 9.37 percent; bonuses recomputing per tick.

### Every invariant, across the FULL population

| invariant | measured |
|---|---|
| **BL-538 and the earnings invariant** | **0 breaches** |
| **BL-696**, two open payouts on one campaign | **0** |
| **BL-696**, a clip with two agency rows | **0** |
| **BL-696**, a clip with two v2 editor rows | **0** |
| **BL-627 no overpayment**, counting both v2 aggregates | **0 campaigns over budget** |
| `isMarketplaceClip` true on a v2 clip | **0 of 51** |
| **BL-824 paid-is-final** | 26 positions, **pre-existing**; zero payout rows created |

### The teardown, exactly

```
263 rows recorded in C:/bl880-sandbox/ledger.jsonl
  all locks passed, nothing has been deleted yet
  marketplace_v2_posts       deleted  51
  marketplace_v2_clips       deleted   2
  clip_stats                 deleted   1
  tracking_jobs              deleted  51
  clips                      deleted  52
  clip_accounts              deleted  52
  campaigns                  deleted   2
  users                      deleted  52
  263 deleted, 0 already gone, 0 FAILED
  VERIFIED: 0 of 263 recorded rows remain.
```

Product-written rows were **adopted** rather than swept, by a script that adds a ledger line only
where it can prove the row belongs to this round from a column holding a sandbox id.

### Safety, itemised

* **No real user, clip, campaign or payout was touched.** Every row carried the `bl880sbx-` prefix
  and the `BL880-SANDBOX-DELETE-ME` marker, every person `isTestUser`, both campaigns
  `isTestCampaign`.
* **NO APIFY ACTOR RAN AND NO VENDOR LOOKUP WAS MADE.** Views were set directly on `ClipStat`, which
  is what the tick writes after its own fetch, so the money path was exercised and the metered path
  was not. The 11 BL-678 guards are untouched.
* **Six protected money files plus `campaign-era.ts` are BYTE-IDENTICAL by blob OID** on both refs:
  `clip-earnings-writer.ts ac5be7de`, `earnings-calc.ts 00410634`, `balance.ts 25a0b2f2`,
  `clip-earnings-invariant-middleware.ts 61cef393`, `money-decimal.ts ef5cdae7`,
  `campaign-era.ts 106e16ad`. **`tracking.ts` moved from `bf31646f` to `17e84eec`, deliberately, and
  the full diff is below.**
* **No Prisma in the browser bundle.** Nothing in this round touches a client component.
* **The branch did not drift.** `checkpoint/BL-880` throughout.
* **No handle printed that is not a sandbox handle, and no wallet address anywhere.**

### Build and gates, honestly

`eslint` is present in three forms, so the BL-348 gate did not silently no-op.

| run | result |
|---|---|
| `npx tsc --noEmit` | **exit 0**, three times across the round |
| `check:prisma-bypass` / `check:removed-fields` / `check:event-wiring` | **0 / OK / 0** |
| **`lint:hooks`** | **10 problems, 0 errors, 10 warnings** against a ceiling of 11 |
| **`npm run build`** | **`BUILD_EXIT=0`**, echoed by the build's own shell, never read off a pipe |

---

## THE FULL `tracking.ts` DIFF

**212 insertions, ONE deletion**, and the deletion is the `totalForThisClip` line being replaced by
the same line with the two v2 legs added. Every hunk is justified in its own comment in the code, and
the hunks are, in order: the two new money variables, the v2 compute fork, the reduction cap, the
retry snapshot and restore, the budget projection, the truncate-in-step block, the write fork, and
the nested clip select.

```diff
diff --git a/src/lib/tracking.ts b/src/lib/tracking.ts
index bf31646f..17e84eec 100644
--- a/src/lib/tracking.ts
+++ b/src/lib/tracking.ts
@@ -2113,6 +2113,13 @@ async function processTrackingJob(
       let newOwnerAmt = 0;
       let newCreatorAmt = 0;
       let newPlatformAmt = 0;
+      // BL-880 — MARKETPLACE V2. The editor's 45 percent and the platform's 10,
+      // alongside the poster's 45 which lives in `newEarnings` exactly as the
+      // first marketplace's poster 30 does. `v2Breakdown` is null on every
+      // non-v2 clip, which is every clip on the platform today.
+      let v2Breakdown: any = null;
+      let newV2EditorAmt = 0;
+      let newV2PlatformAmt = 0;
       // F-EARNINGS-LIVE-FIELD-SNAPSHOT — read pricingModel / minViews /
       // maxPayoutPerClip / ownerUserId from the clip's approval snapshot
       // first; fall back to live campaign when snapshot is null (PENDING/
@@ -2255,6 +2262,66 @@ async function processTrackingJob(
             ? calculateOwnerEarnings(stats.views, ownerCpmResolved, breakdown.baseEarnings, cCpm)
             : 0;
         }
+
+        // ═══ BL-880 — MARKETPLACE V2, THE 45/45/10 SPLIT ON EVERY TICK ═════
+        //
+        // PLACED HERE, AND THE POSITION IS THE WHOLE POINT. `newOwnerAmt` was
+        // computed immediately above from the clip's FULL clipper-side gross,
+        // and it is deliberately NOT touched. That is what keeps the owner's
+        // ADDS decision true: the platform's 10 percent is ADDITIONAL to his
+        // ordinary per-clip cut, so the `AgencyEarning` row below must still be
+        // written and must still grow. A fix that routed a v2 clip around the
+        // `isCpmSplit` branch to control the split would have stopped writing
+        // it and turned ADDS into REPLACES with no error anywhere.
+        //
+        // A V2 CLIP IS IDENTIFIED BY `marketplaceV2PostId`, NEVER BY
+        // `isMarketplaceClip`, WHICH MUST STAY FALSE. True would route it
+        // through the FIRST marketplace's 60/30/10 in four separate branches.
+        //
+        // WHAT THIS REPLACES. Before BL-880 a v2 clip fell into the ordinary
+        // else-branch above and `newEarnings` held `breakdown.clipperEarnings`,
+        // the FULL clipper rate. BL-879 measured that and shipped every v2
+        // tracking job INACTIVE rather than pay a poster 100 percent of a rate
+        // he is owed 45 percent of. This is the line that makes activating them
+        // safe.
+        //
+        // IT RECOMPUTES FROM TOTAL VIEWS, NOT FROM A DELTA, exactly like every
+        // other branch in this function, so all three legs are rewritten from
+        // one gross on every pass. That is what stops the editor's 45 percent
+        // freezing at its first hour's value while the poster's keeps climbing.
+        if ((clip as any).marketplaceV2PostId) {
+          const v2Editor = (clip as any).marketplaceV2Post?.v2Clip?.editor ?? null;
+          const { calculateMarketplaceV2Earnings } = await import("@/lib/marketplace-v2-earnings");
+          v2Breakdown = calculateMarketplaceV2Earnings({
+            views: stats.views,
+            campaignCpm: cCpm ?? resolved.clipperCpm,
+            campaignMinViews: econ.minViews,
+            campaignMaxPayoutPerClip: econ.maxPayoutPerClip,
+            editor: {
+              level: v2Editor?.level ?? 0,
+              streak: v2Editor?.currentStreak ?? 0,
+              isPWAUser: !!v2Editor?.isPWAUser,
+              isReferred: !!v2Editor?.referredById,
+              streakBonusPercentAtApproval:
+                ((clip as any).marketplaceV2EditorEarning?.streakBonusPercentAtApproval as number | null) ?? null,
+            },
+            poster: {
+              level: (clip as any).user?.level ?? 0,
+              streak: (clip as any).user?.currentStreak ?? 0,
+              isPWAUser: !!(clip as any).user?.isPWAUser,
+              isReferred: !!(clip as any).user?.referredById,
+              streakBonusPercentAtApproval: lockedStreakPct,
+            },
+          });
+          // `Clip.earnings` holds the POSTER'S 45 percent, which is the same
+          // contract the first marketplace uses for its poster's 30. Every
+          // floor, cap and never-decrease guard downstream compares against
+          // `clip.earnings`, so this value and that column must mean the same
+          // thing or none of them work.
+          newEarnings = v2Breakdown.poster.total;
+          newV2EditorAmt = v2Breakdown.editor.total;
+          newV2PlatformAmt = v2Breakdown.platform.amount;
+        }
       }
 
       // F-EARNINGS-CAP — apply payout reduction cap to ALL recomputed
@@ -2282,6 +2349,18 @@ async function processTrackingJob(
         newOwnerAmt   = applyPayoutReductionCap(newOwnerAmt,   reductionRatio) ?? 0;
         newCreatorAmt = applyPayoutReductionCap(newCreatorAmt, reductionRatio) ?? 0;
         newPlatformAmt= applyPayoutReductionCap(newPlatformAmt, reductionRatio) ?? 0;
+        // BL-880 — the v2 legs go through the same cap as every other figure.
+        // `payoutReductionRatio` is a MULTIPLIER and is IMMUTABLE once set, so
+        // a v2 clip whose poster has been reduced must have its editor and
+        // platform legs reduced by the same factor or the three stop summing.
+        newV2EditorAmt = applyPayoutReductionCap(newV2EditorAmt, reductionRatio) ?? 0;
+        newV2PlatformAmt = applyPayoutReductionCap(newV2PlatformAmt, reductionRatio) ?? 0;
+        if (v2Breakdown) {
+          v2Breakdown.poster.base        = applyPayoutReductionCap(v2Breakdown.poster.base,        reductionRatio) ?? 0;
+          v2Breakdown.poster.bonusAmount = applyPayoutReductionCap(v2Breakdown.poster.bonusAmount, reductionRatio) ?? 0;
+          v2Breakdown.editor.base        = applyPayoutReductionCap(v2Breakdown.editor.base,        reductionRatio) ?? 0;
+          v2Breakdown.editor.bonusAmount = applyPayoutReductionCap(v2Breakdown.editor.bonusAmount, reductionRatio) ?? 0;
+        }
         if (breakdown) {
           breakdown.baseEarnings = applyPayoutReductionCap(breakdown.baseEarnings, reductionRatio) ?? 0;
           breakdown.bonusAmount  = applyPayoutReductionCap(breakdown.bonusAmount,  reductionRatio) ?? 0;
@@ -2425,12 +2504,19 @@ async function processTrackingJob(
       const initialNewOwnerAmt = newOwnerAmt;
       const initialNewCreatorAmt = newCreatorAmt;
       const initialNewPlatformAmt = newPlatformAmt;
+      // BL-880 — snapshotted for the same reason as the four above. Without
+      // this a Serializable retry would start from attempt 1's already-capped
+      // v2 legs and cap them a second time.
+      const initialNewV2EditorAmt = newV2EditorAmt;
+      const initialNewV2PlatformAmt = newV2PlatformAmt;
 
       const runEarningsTx = async () => {
         newEarnings = initialNewEarnings;
         newOwnerAmt = initialNewOwnerAmt;
         newCreatorAmt = initialNewCreatorAmt;
         newPlatformAmt = initialNewPlatformAmt;
+        newV2EditorAmt = initialNewV2EditorAmt;
+        newV2PlatformAmt = initialNewV2PlatformAmt;
         autoPausedBudget = null;
         autoPausedSpent = null;
         await db.$transaction(async (tx: any) => {
@@ -2573,7 +2659,15 @@ async function processTrackingJob(
                 }
               }
             } else {
-              const totalForThisClip = newEarnings + newOwnerAmt;
+              // BL-880 — A V2 CLIP'S TOTAL IS NOT JUST THE POSTER PLUS THE
+              // OWNER. Without the two v2 legs in this projection, 55 cents in
+              // every v2 dollar is invisible to the per-tick cap and the
+              // campaign pauses late, which is the same 55 percent BL-877
+              // closed in the committed-spend aggregate and BL-879 measured.
+              const totalForThisClip = newEarnings + newOwnerAmt + newV2EditorAmt + newV2PlatformAmt;
+              // Remembered BEFORE any cap can move it, so the two v2 legs can
+              // be scaled by exactly the factor the poster's leg was scaled by.
+              const v2PosterBeforeCap = newEarnings;
               console.log(`[BUDGET-CHECK] Campaign: ${clip.campaignId} Budget: $${txCampaign.budget} Spent: $${spent.toFixed(2)} This clip: $${currentClipEarnings} Remaining: $${remaining.toFixed(2)} New: $${newEarnings}+$${newOwnerAmt}`);
 
               // BL-162 (2026-06-11) — guaranteed-owner-split per-clip cap.
@@ -2698,6 +2792,52 @@ async function processTrackingJob(
                 console.log(`[BUDGET-CHECK] Ratio-capped: clipper=$${newEarnings} owner=$${newOwnerAmt} remaining=$${remaining.toFixed(2)}`);
               }
 
+              // ═══ BL-880 — THE THREE LEGS TRUNCATE IN STEP OR NOT AT ALL ═══
+              //
+              // Every branch above may have moved `newEarnings`: the guarantee
+              // cap, the no-budget-remaining hold, the ratio cap and the
+              // BL-718 paid floor. Whatever it did, the editor and platform
+              // legs are scaled by the SAME factor here, and the platform leg
+              // is taken as the RESIDUAL of the scaled gross so the three still
+              // sum to it EXACTLY rather than by two roundings agreeing. That
+              // is the same construction BL-877 used to make the split sum in
+              // the first place.
+              //
+              // IF THIS DID NOT EXIST the poster's leg would be capped and the
+              // other two would sail past the cap untouched, which is 55 cents
+              // in every dollar escaping the budget.
+              if (v2Breakdown && v2PosterBeforeCap > 0 && newEarnings !== v2PosterBeforeCap) {
+                const v2Scale = newEarnings / v2PosterBeforeCap;
+                const grossBefore = Math.round(
+                  (v2PosterBeforeCap + newV2EditorAmt + newV2PlatformAmt) * 100,
+                ) / 100;
+                const grossAfter = Math.round(grossBefore * v2Scale * 100) / 100;
+                newV2EditorAmt = Math.round(newV2EditorAmt * v2Scale * 100) / 100;
+                newV2PlatformAmt = Math.max(
+                  0,
+                  Math.round((grossAfter - newEarnings - newV2EditorAmt) * 100) / 100,
+                );
+                // The poster's own base and bonus must follow the total or the
+                // L1 invariant (`earnings == base + bonus`) refuses the write
+                // and the whole tick's transaction dies. BASE IS THE RESIDUAL,
+                // same technique BL-849 used for its floor.
+                const unscaledV2 = Math.round(
+                  ((v2Breakdown.poster.base ?? 0) + (v2Breakdown.poster.bonusAmount ?? 0)) * 100,
+                ) / 100;
+                if (unscaledV2 > 0) {
+                  const heldBonus = Math.round((v2Breakdown.poster.bonusAmount ?? 0) * v2Scale * 100) / 100;
+                  v2Breakdown.poster.bonusAmount = heldBonus;
+                  v2Breakdown.poster.base = Math.round((newEarnings - heldBonus) * 100) / 100;
+                } else {
+                  v2Breakdown.poster.bonusAmount = 0;
+                  v2Breakdown.poster.base = newEarnings;
+                }
+                console.log(
+                  `[BL-880-V2-TRUNCATE] Clip ${clip.id} scale=${v2Scale.toFixed(4)} ` +
+                  `poster=$${newEarnings.toFixed(2)} editor=$${newV2EditorAmt.toFixed(2)} platform=$${newV2PlatformAmt.toFixed(2)}`,
+                );
+              }
+
               // BL-163 (2026-06-11) — OWNER-LOCK. After every clipper-side
               // manipulation (initial computation, PRR multiplier, F-PROP-
               // CUT scaling, per-clip cap), DERIVE owner = newEarnings ×
@@ -2953,6 +3093,55 @@ async function processTrackingJob(
             // skipped the write when totals matched but base/bonus had
             // drifted. The helper now writes unconditionally and the
             // invariant assertion catches any future drift.
+            // ═══ BL-880 — ONE BRANCH, ONE POINT, AND THE AGENCY ROW BELOW
+            //     IS DELIBERATELY OUTSIDE IT SO ADDS SURVIVES ════════════════
+            if (v2Breakdown) {
+              await writeClipEarnings(
+                tx,
+                clip.id,
+                {
+                  earnings: newEarnings,
+                  baseEarnings: v2Breakdown.poster.base,
+                  bonusPercent: v2Breakdown.poster.bonusPercent,
+                  bonusAmount: v2Breakdown.poster.bonusAmount,
+                },
+                { reason: "tracking-tick:marketplace-v2-poster" },
+              );
+              // THE OTHER TWO LEGS, UPDATED RATHER THAN CREATED ONCE, IN THIS
+              // SAME TRANSACTION. An upsert keyed on `clipId` is the right
+              // shape and not a delete-and-rewrite: `clipId` is UNIQUE on both
+              // tables with the index verified in `pg_indexes` by BL-877, so a
+              // concurrent tick on the same clip either waits or conflicts and
+              // retries under Serializable, where a delete-then-create would
+              // leave a window with no row at all. It also preserves
+              // `streakBonusPercentAtApproval`, which a re-create would lose,
+              // which is the Persona-10 defect the first marketplace already
+              // had to fix.
+              const { writeMarketplaceV2Earnings } = await import("@/lib/marketplace-v2-writer");
+              await writeMarketplaceV2Earnings(
+                tx,
+                {
+                  clipId: clip.id,
+                  v2ClipId: (clip as any).marketplaceV2Post?.v2ClipId ?? (clip as any).marketplaceV2Post?.v2Clip?.id ?? "",
+                  editorId: (clip as any).marketplaceV2Post?.v2Clip?.editorId ?? "",
+                  campaignId: clip.campaignId,
+                  views: stats.views,
+                  breakdown: {
+                    ...v2Breakdown,
+                    poster: {
+                      ...v2Breakdown.poster,
+                      total: newEarnings,
+                    },
+                    editor: {
+                      ...v2Breakdown.editor,
+                      total: newV2EditorAmt,
+                    },
+                    platform: { amount: newV2PlatformAmt },
+                  },
+                  reason: "tracking-tick:marketplace-v2",
+                },
+              );
+            } else {
             await writeClipEarnings(
               tx,
               clip.id,
@@ -2964,6 +3153,7 @@ async function processTrackingJob(
               },
               { reason: "tracking-tick:non-marketplace" },
             );
+            }
 
             // BL-541 — F-OVERRIDE-NO-AGENCY-EARN DELETED. This branch ran on
             // EVERY tick and removed the owner's row from every override clip,
@@ -3822,6 +4012,27 @@ export async function runDueTrackingJobs(options?: {
             // the 60/30/10 split without an extra round trip.
             isMarketplaceClip: true,
             marketplaceSubmissionId: true,
+            // BL-880 — MARKETPLACE V2. This is a NESTED select on the `clip`
+            // RELATION, not a top-level select on the dueJobs findMany, which
+            // is what F-AUTO-LADDER-DEPENDENCY forbids two comments above.
+            // Adding fields here is exactly what the marketplace fork already
+            // does on the four lines above.
+            marketplaceV2PostId: true,
+            marketplaceV2Post: {
+              select: {
+                id: true,
+                v2ClipId: true,
+                v2Clip: {
+                  select: {
+                    id: true,
+                    editorId: true,
+                    editor: { select: { level: true, currentStreak: true, referredById: true, isPWAUser: true } },
+                  },
+                },
+              },
+            },
+            marketplaceV2EditorEarning: { select: { amount: true, streakBonusPercentAtApproval: true } },
+            marketplaceV2PlatformEarning: { select: { amount: true } },
             marketplaceCreatorEarning: { select: { amount: true, savedAmount: true, streakBonusPercentAtApproval: true } },
             marketplacePlatformEarning: { select: { amount: true, savedAmount: true } },
             marketplaceOriginPost: {
```

---

## WHETHER A REAL POSTER COULD SAFELY USE THIS TODAY

> **THE MONEY PATH IS CORRECT AND PROVED. WHAT REMAINS IS A PRODUCT DECISION RATHER THAN A SAFETY
> ONE, AND THAT IS A CHANGE FROM BL-879, WHICH HAD TO SAY NO.**
>
> The tick now pays a v2 clip 45 percent, the editor's leg grows with it, the platform's is the
> residual, all three truncate together at the budget, and the owner's ordinary cut is still written
> on top under ADDS.
>
> **What still gates it:** both v2 pages are behind `isMarketplaceVisibleForUser`, so until
> `NEXT_PUBLIC_MARKETPLACE_ENABLED` flips, only the OWNER and test users can see the catalogue.
>
> **What the owner should weigh before flipping it**, stated plainly rather than buried: **eight
> owner-run earnings writers still have no v2 fork** and would write a v2 clip the full clipper rate
> if he ran one, the most likely being a campaign devaluation. None runs on a schedule and none is
> reachable by a clipper. **A cautious owner flips the flag after Round Five. A confident one flips it
> now and does not devalue a v2 campaign or run a repair route until Round Five ships.**

## WHAT ROUND FIVE MUST BUILD

1. **The other eight earnings writers**, as ONE shared helper rather than eight copies of the split:
   `cpm-restamp.ts`, `gamification.ts`, `campaign-freeze-undo.ts`, `clips/[id]/override`, and the
   four admin repair routes.
2. **The devaluation question this round could not close:** whether BL-538's never-decrease guard
   would block the tick's downward correction after a restamp writes a v2 clip at full rate once.
3. **The retire and flag paths for a v2 clip's two extra rows**, which were not exercised here.
4. **The editor's and the poster's payout surfaces**, since money now accrues to two people per clip
   and only one of them has a page that shows it.

---

## WHAT COULD NOT BE DETERMINED

* **Whether BL-538's guard blocks a post-devaluation correction on a v2 clip.** Named above.
* **What retiring or flagging a v2 clip does to its editor and platform rows.** Not exercised.
* **Whether the 26 positions below their paid floor is comparable to BL-849's 17.** Not re-measured
  with BL-849's exact query, for the fourth round running. This round created zero payout rows.
* **The tick's behaviour under genuine production concurrency on a v2 clip.** The Serializable shape
  and the L1 lock were exercised fifty posts wide across five passes, but not against a real
  concurrent cron tick, because nothing in production is reachable by the cron yet.

---

**PERFORM NO FIX ON ANYTHING ABOVE. The two defects this round found in its own proofs, it fixed and
re-ran. The eight sites it did not fix, it named.**
