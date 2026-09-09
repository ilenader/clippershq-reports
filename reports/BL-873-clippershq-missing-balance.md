# BL-873 — his $58 is real, it is still his, and it stopped being withdrawable at 06:00 this morning

**2026-09-09. AUDIT ONLY. Nothing was changed, nobody was paid, no balance or status was touched.
One markdown file. No build was run and none is claimed, because a markdown diff cannot change
TypeScript.**

---

## THE ONE LINE

**Nothing was taken from him. At 06:00 UTC today the dead-clip cron marked 46 of his Instagram clips
unreachable in three minutes, moving $256.35 out of the pool his balance is computed from, which
dropped his withdrawable figure to $0.00 and made the $58.30 he had correctly not yet been paid
temporarily unreachable.**

---

## PART 0 — THE CONNECTION CAP

**One.** Every query in this round was run by me, serially, one shell at a time, through
`run-select.js`, which opens a single short-lived connection and closes it. **The one subagent used
was explicitly forbidden from running any database query or any script that opens a connection**, and
was given report reading only. Seventeen queries were run in total, never concurrently. Nothing
heavy: no `VACUUM`, no `EXPLAIN ANALYZE`, no `pg_stat_statements` read.

---

## PART 1 — HIS BALANCE, RECONSTRUCTED

Clipper `nziz...` (redacted), id `cmrkvjpk4...`, CLIPPER, ACTIVE, joined `2026-07-14 16:37:24.387`,
not referred, not a test user. All figures against DB `now()` between
`2026-09-09 17:59:10.157380+00` and `2026-09-09 18:02:38.110215+00`.

### His position today

| | Gross | Cash |
|---|---|---|
| Earned across all 112 clips (109 approved) | **$395.13** | |
| Counted, meaning approved and still reachable | **$132.47** | |
| Held on 53 clips marked unavailable | **$262.66** | |
| Paid to him, two payouts, both PAID | **$336.83** | **$293.04** |
| **Earned but never paid** | **$58.30** | about $50.72 after the 9 percent fee |
| **Available to withdraw right now** | **$0.00** | **$0.00** |

**$395.13 minus $336.83 is $58.30. That is his number, to the cent, and he is right that he has not
been paid it.**

### Why his screen says zero, and it is not a bug

Every clip he has is on one Instagram account, still APPROVED, on one campaign. Using BL-824's rule
exactly as `balance.ts` applies it:

```
effectivePaid = min(paidGross, payableEarnings) = min(336.83, 132.47) = 132.47
available     = max(0, payable - effectivePaid) = max(0, 132.47 - 132.47) = 0.00
```

**The floor is working.** He has been paid $336.83 against a payable pool that is now only $132.47.
Without BL-824's `min`, the arithmetic would read minus $204.36 and the platform would try to claw
back money he has already been given. **Paid is final, so it clamps at zero instead.** He is not in
debt and nothing will be taken back.

### Exactly when it changed, and by how much

| When, `::text` | Event | Clips | Moved out of payable | Available after |
|---|---|---|---|---|
| before `2026-09-03` | steady state | | | **$58.30** |
| `2026-09-03 06:00:43.890` | dead-clip cron | 1 | $0.00 | $58.30 |
| `2026-09-05 06:00:55.909` to `06:01:04.627` | dead-clip cron | 6 | **$6.31** | **$51.99** |
| **`2026-09-09 06:00:09.505` to `06:03:06.416`** | **dead-clip cron** | **46** | **$256.35** | **$0.00** |

**Three minutes this morning took him from $51.99 to $0.00.** If he looked at his screen yesterday
and again today, that is exactly what he saw, and he is not imagining it.

### His earnings, recomputed independently

BL-823 found a clipper's hand count right and the platform wrong by $41.59, so this was not taken on
trust. Recomputed from each clip's own views and its own stamped `cpmAtSubmissionDecimal`, not from
any stored total:

| | Value |
|---|---|
| Approved clips | 109 |
| Total views | 1,871,876 |
| **Recomputed base from views times own stamped CPM** | **$374.38** |
| Stored `baseEarnings` | $374.31 |
| Stored `bonusAmount` | $20.82 |
| Stored total | $395.13 |

**$374.31 plus $20.82 is $395.13 exactly, and my independent recomputation of the base lands within
$0.07 across 109 clips, which is rounding.** Unlike BL-823's case, **the platform's arithmetic is
correct and his hand count and the platform agree.**

### The verdict, stated plainly

**The money did not vanish, and it did not merely never exist either. Both of the easy answers are
wrong.**

He is reading two correct figures that measure different things, exactly as BL-818 describes, **but
the reason the gap opened is a real event with a timestamp**, not a display quirk he had simply never
noticed. **$58.30 is recorded against his account, it is unpaid, and it is his.** It is not
withdrawable today because the clips it sits on stopped being reachable this morning.

**It returns on its own if those clips come back.** BL-865 built the liveness recheck for exactly
this and measured the dead-clip cron's false-positive rate at **4.34 percent**, so on those numbers
about two of his 46 would be expected back.

---

## PART 2 — RULING EACH RECENT CHANGE IN OR OUT, BY EVIDENCE

| Shipped change | Touched him? | Evidence |
|---|---|---|
| **BL-866 clip devaluation** | **NO** | `devaluedAt` null on all 112 clips; `cpmOverriddenAt` null; `payoutReductionRatio` null. **Platform-wide, ZERO clips have ever been devalued.** |
| **BL-861 Close with no payment** | **NO** | `settledUnpaidAt` null on both his payouts. **Platform-wide, ZERO payouts have ever been closed unpaid.** |
| **BL-864 Set amount** | **NO** | `actualPaidAmount` null on both his payouts. It HAS been used 11 times platform-wide, but not on him. |
| **BL-865 liveness sweep** | **NO** | It revived 34 clips today; none of his. His clips were flagged at 06:00 and the sweep's population was taken at 11:57, so they were eligible and did not come back. |
| **BL-871 listing clamp** | **NO** | Marketplace only. He has no marketplace clips; the marketplace has never had a live clip. |
| **The dead-clip cron** | **YES, and it is the whole answer** | 46 clips at `2026-09-09 06:00:09.505` to `06:03:06.416`, $256.35 |

**Three of the five are ruled out platform-wide, not merely for him**, which is the strongest form
the answer can take: no clip on this platform has ever been devalued, and no payout has ever been
closed unpaid.

### Held money versus lost money, since they look identical to a clipper

BL-864 established that closing a payout HOLDS the full requested gross so it leaves Available to
withdraw without being paid. **That is not what happened here** and the distinction matters: his
money is not held against a closed claim, it is **excluded from the payable pool because the clips
behind it are unreachable**. The practical difference is direction of travel. **Held money is gone
unless the owner reopens it. His money returns automatically if the videos do.**

### Was the marking itself correct?

By the platform's own rule, yes, and comfortably. `retire-dead-clips` requires three consecutive
live-probed 404s. His flagged clips carry `consecutiveGone` of **14 to 31**, with `firstGoneAt`
between `2026-08-31 08:01:02.280` and `2026-09-05 22:20:58.463`. **They have been returning 404 for
four to nine days and were probed dead between fourteen and thirty-one times.** This is not a blip.

**One caveat I cannot settle from the data, and it is the one that would change the answer.** All 46
are on a single Instagram account which is still marked APPROVED here, and they went dark in a tight
cluster. BL-720's rule is that a clip may only be marked gone when NO HUMAN can see it, and a private
or restricted account returns 404 for every post while every follower can still see them. **Whether
that account is private, restricted or genuinely emptied cannot be determined from this database**,
and this round did not probe the provider because the brief says pay nobody. **If the account is
merely private, these 46 clips are wrongly retired and the money should come back.** That is worth
one look by eye at the account.

### One thing that leaves no trace

**The dead-clip cron writes no audit row.** The largest money-visible event in this clipper's history,
46 clips and $256.35 leaving his available balance in three minutes, produced **nothing** in
`audit_logs`. His entire audit trail is 111 `APPROVED_CLIP`, 3 `REJECTED_CLIP`, and Discord and email
noise. The only record that it happened is `videoUnavailableSince` on the clips themselves.

---

## PART 3 — EVERYONE ELSE IN THE SAME POSITION

Measured, not extrapolated, because BL-822's 24 clippers and $274.12 became 5 and $27.00 when
BL-823 measured it properly.

**48 positions across 37 clippers hold earned, unpaid money that is currently unreachable, totalling
$523.71 gross.** The ten largest:

| Clipper | Earned | Payable now | Held on unavailable | Paid gross | **Unreachable** |
|---|---|---|---|---|---|
| `vdeb...` | $147.61 | $0.00 | $147.61 | $0.00 | **$147.61** |
| `isai...` | $60.06 | $0.00 | $60.06 | $0.00 | **$60.06** |
| **`nziz...`** | **$395.30** | **$132.64** | **$262.66** | **$336.83** | **$58.47** |
| `slay...` | $34.52 | $0.28 | $34.24 | $0.00 | $34.24 |
| `mcye...` | $34.23 | $0.00 | $34.23 | $0.00 | $34.23 |
| `dext...` | $2,383.77 | $2,359.29 | $24.48 | $491.54 | $24.48 |
| `sade...` | $19.07 | $0.00 | $19.07 | $0.00 | $19.07 |
| `sarm...` | $18.52 | $0.00 | $18.52 | $0.00 | $18.52 |
| `alon...` | $119.30 | $100.81 | $18.49 | $98.23 | $18.49 |
| `amol...` | $38.24 | $27.34 | $10.90 | $0.00 | $10.90 |

**Our clipper is third, at $58.47.** That figure drifted up from $58.30 during the twenty minutes of
this investigation because his still-live clips kept earning, which is itself evidence the engine is
working normally on the clips it can still see.

**The two above him are worse in kind.** `vdeb...` and `isai...` have **never been paid anything at
all** and have **100 percent** of their earnings sitting on unreachable clips. They cannot be reading
a confusing gap, because for them there is no counted figure at all: their screen says $0.00 and
their earned figure says $147.61 and $60.06. **If anyone writes in next, it will be one of those
two.**

### The standing checks, run regardless

| Check | Result |
|---|---|
| Earnings invariant, `earnings = base + bonus` | **0 violations** |
| Any clip with negative earnings | **0** |
| Any clipper whose recorded earnings sit below money already paid, unprotected | **0.** 30 positions across 27 clippers have paid gross above current payable, totalling $4,707.00, and **every one is correctly clamped by BL-824's floor rather than clawed back** |
| Payouts closed unpaid | **0**, the feature has never been used |
| Clips devalued | **0**, the feature has never been used |
| Payouts with a set price | 11, none belonging to this clipper |
| PAID payouts with no `paidAt` | 26, legacy rows, no money effect, noted not chased |

---

## PART 4 — THE TRACKING QUERY, RUN FOR THE OWNER

He raised `CLIPS_PER_TICK` after BL-872. Here is what it did.

| Measure | BL-872, about an hour ago | Now | Change |
|---|---|---|---|
| **Starved on an active cadence** | **512** | **512** | **none** |
| Active jobs | 8,427 | 8,441 | +14 |
| All overdue 24h+ | 4,035 | 4,036 | +1 |
| Clips per tick | 51 | **46.2** | slightly down |
| Snapshots per day | 6,527 | about **6,000** | slightly down |

Measured over the last six full hours: ticks are firing **6 per hour**, exactly on schedule, and
snapshots per hour ran 150, 217, 411, 196, 174, 305 and 313, averaging **46.2 clips per tick**.

### The per-tick cap was NOT the binding constraint, and here is what is

**Throughput did not rise. It fell slightly.** So the cron was never being held back by how many
clips it was allowed to collect.

**It is the wall clock.** The tracking loop has a budget of `TRACKING_LOOP_BUDGET_MS = 210_000`, that
is 210 seconds, inside a 300 second route limit. **210 seconds divided by 46.2 clips is 4.5 seconds
per clip**, which is what one Instagram fetch costs. **The tick is not stopping because it ran out of
allowance; it is stopping because it ran out of time.**

Demand is not the constraint either: **4,165 jobs were due at the moment of measurement** against
about 46 served per tick, so there is plenty of work waiting.

**The three things that could actually move it**, none of which is the per-tick cap: run the cron
more often than every 10 minutes, cut the per-clip provider latency, or cut demand by pushing settled
clips to longer intervals as BL-872 recommended. **The first is a schedule change and the cheapest to
try.**

*He should put `CLIPS_PER_TICK` back where it was, or leave it, but either way it is not doing
anything.*

---

## PART 5 — WHAT TO SEND HIM

### The message

> Nothing has been taken from you and nothing has been lost. Here is exactly what happened.
>
> You have earned $395.13 with us. We have paid you $336.83 of that, across two payouts on 4 and 5
> September. So $58.30 of what you earned has not been paid yet, and you are right about that number.
>
> Early this morning our system checked your clips and could not open 46 of them on Instagram. When
> we cannot open a clip we stop counting it, because we cannot see whether it is still getting views.
> That is why your withdrawable balance dropped to zero: the money is still recorded against your
> account, but it is sitting on clips we cannot currently read.
>
> This is not a penalty and it is nothing you did wrong. If those clips become readable again, they
> start counting again on their own and the money comes back with them. We check for that
> automatically.
>
> One thing that would help me: could you open a few of those clips on your own phone and tell me
> whether you can see them? If you can see them and we cannot, that points at a setting on the
> account rather than the clips being gone, and that is something we can fix.

### Is he owed money he cannot reach?

**Yes: $58.30 gross, about $50.72 after the 9 percent fee.** It is recorded, it is unpaid, and today
he cannot withdraw it.

**Whether he SHOULD be able to reach it depends on the one thing I could not measure**, which is
whether that Instagram account is private or genuinely gone. **If those 46 clips are visible to
humans, the retirement is wrong under BL-720's rule and the money should be released.**

### The fix, spec'd and deliberately not performed

BL-716 and BL-718 both established that a money repair deserves its own round with snapshots and a
printed rollback, so nothing here was touched.

**What that round would do:** probe the account and a sample of the 46 clips through
`fetchHikerInstagramByUrl`, costing 47 calls at BL-838's measured $0.00069214, so **about three
cents**. If the account resolves and the media does not, that is BL-720's private-account case and
the clips should be un-retired. If the account itself is gone, the retirement stands and the answer
to him is that the money cannot be released.

**It should sweep all 37 clippers and $523.71, not just this one**, because the same question applies
to every one of them and the two clippers above him on the list are worse off. **The repair is
clearing `videoUnavailable` on clips that are provably reachable, which BL-865 already built and
proved, so it is a re-run rather than new code.**

---

## WHAT COULD NOT BE MEASURED

• **Whether the Instagram account behind the 46 clips is private, restricted or emptied.** That needs
  a provider probe and the brief says pay nobody. It is the one fact that decides whether his $58.30
  should be released or is correctly unreachable.
• **The exact per-clip provider latency.** The 4.5 seconds in PART 4 is derived from 210 seconds
  divided by 46.2 clips, not timed directly.
• **What his screen literally rendered on any past day.** Balances are derived on every read and
  never stored, so the timeline above is reconstructed from clip and payout state, not replayed.

---

## THE MODEL SPLIT

**Opus did every database query and every money judgement**: all seventeen queries, the independent
recomputation from stamped CPMs, the `effectivePaid` arithmetic, the population sweep, the reading of
the gone-counters, and the conclusion that the per-tick cap was never the constraint.

**Sonnet did one job**: reading seven prior reports and returning the columns and formulas to query
against. **It was forbidden from opening a database connection**, which is what made PART 0's cap of
one possible.

**Nothing money-touching was split.** A subagent reporting "$58.30 is unreachable" would be a claim
about whether a real person is owed money, which is not mechanical work.
