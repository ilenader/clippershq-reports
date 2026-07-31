# BL-695 — the authoritative stuck-money list, recomputed after the clamp fix

## THE CURRENT GENUINELY STUCK TOTAL IS $387.81 ACROSS 23 CLIPPERS, not the $544.77 across 41 that BL-693 published before the fix deployed. Two things moved it. The clamp fix released $20.59 across five clippers, taking the figure from $408.40 to $387.81 and dropping three clippers off the list entirely. And the $544.77 itself was measured with a formula that ignores how the gate actually works, so it overstated the problem: it compared two global totals and never accounted for the fact that a clipper may submit one payout request per campaign. Under the mechanics the code really applies, the pre-fix figure was $408.40, not $544.77. **One of the released clippers has already requested his money: a $22.70 payout went in at 2026-07-31 08:42:34.014 and is REQUESTED right now. If the owner pays that person from the old list, he pays twice, today.**

**2026-07-31 · AUDIT ONLY. READ ONLY on code, data and money. No payout was created, modified, approved or cancelled. No balance was written. `GLOBAL_PAYOUT_CLAMP_ENABLED` was not flipped. Nothing was paid.**
**Base** origin/main `46115e32` (`post-merge-BL-693`) · **Branch** `checkpoint/BL-695` · **Worktree** `C:/b695` (short path, node_modules never junctioned) · **DB `now()` at final measurement: 2026-07-31 10:02:12.550646+00.** Every timestamp below is `::text` against that clock.

**Redaction.** The reports repo is PUBLIC. Every clipper appears as BL-661's own `substr(md5(userId),1,6)` short id plus an 8-character user-id prefix, so the owner can map both privately in his admin. No handle, email or wallet address appears anywhere, not even partially.

---

## PART 0 — the headline, and why the number moved

| measure | figure |
| --- | --- |
| **Genuinely stuck TODAY** | **$387.81 across 23 clippers** |
| Genuinely stuck immediately before the fix, same formula | $408.40 across 26 clippers |
| Released by the clamp fix | **$20.59 across 5 clippers** |
| BL-693's published figure | $544.77 across 41 clippers |

**Two separate reasons the number differs from $544.77, and they must not be blurred together.**

**1. The fix released $20.59.** That part is real, and it exactly matches BL-692's own measurement of five movers when the same mechanics are applied.

**2. The remaining $136.37 of the difference is measurement, not money.** BL-661's formula, which BL-693 reused, is `stuck = (displayed earned − paid − locked) − (live earned − paid − locked)`. Both sides are **global totals**. It never looks at campaigns. But the gate is applied **per campaign**, and a clipper may submit **one request per campaign**, so a clipper with money on three campaigns can reach it in three requests. BL-661's formula treats all of that as unreachable. Measured with the mechanics the code actually applies, the pre-fix figure was **$408.40**, not $544.77.

**And BL-661's formula cannot be used at all any more.** Post-fix the clamp's earnings base is lifetime, exactly the base the displayed balance uses, so `displayed − globalAvailable` is now **structurally zero for every clipper**. Re-running that formula today would report $0.00 stuck, which is plainly false. **The figure that is true is the one below: $387.81, caused by the per-campaign rule at `payouts/route.ts:424`, which still excludes retired clips and which the fix deliberately did not touch.**

---

## PART 1 — the authoritative list, three buckets, every dollar in exactly one

Each clipper's displayed balance is partitioned as follows, using the merged code's real mechanics: `globalAvailable` from lifetime earnings (`payouts/route.ts:567`, no `videoUnavailable` filter), per-campaign `available` still excluding retired clips (`:424`), `effectiveCap = min(available, globalAvailable)` per request, and the **$10 minimum applied per request** (`:268`).

| bucket | meaning | amount | clippers |
| --- | --- | --- | --- |
| **1. Reachable today** | can be requested right now, one or more campaigns each at $10 or more | **$1,342.00** | 24 |
| **2. Blocked only by the $10 per-campaign minimum** | released and payable, but no single campaign reaches $10. Ordinary product behaviour, NOT the bug | **$328.81** | 99 |
| **3. GENUINELY STUCK on retired clips** | the per-campaign gate excludes it and no code change has released it | **$387.81** | 23 |
| **total displayed** | | **$2,058.62** | 128 |

**$1,342.00 + $328.81 + $387.81 = $2,058.62 exactly.** Nothing is double-counted and nothing is missing. A clipper can appear in more than one bucket for *different dollars*, which is unavoidable and is why the partition is done on dollars rather than on people.

### The five the clamp fix released, and where they landed

| short id | id prefix | lifetime | paid | displayed | could get before | can get now | released | largest single request | bucket |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `91a758` | `cmpl310f` | 42.22 | 25.54 | 16.68 | 0.00 | 16.68 | **+16.68** | **$16.04** | **(a) can request today** |
| `70aa2a` | `cmp75zkf` | 23.56 | 10.31 | 13.25 | 2.68 | 5.54 | +2.86 | $4.09 | (b) below the $10 minimum |
| `bc64d4` | `cmosmyqk` | 994.82 | 993.36 | 1.46 | 0.52 | 1.46 | +0.94 | $1.46 | (b) below the $10 minimum |
| `9d81d0` | `cmp71p89` | 56.77 | 56.69 | 0.08 | 0.00 | 0.08 | +0.08 | $0.88 | (b) below the $10 minimum |
| `540fef` | `cmpfozzs` | 65.60 | 37.28 | 5.62 | 0.00 | 0.03 | +0.03 | $0.03 | **already withdrawn, see below** |
| | | | | | | | **+$20.59** | | |

**BL-693's two at $22.70 and $16.04 are confirmed, with one important update.** `91a758` still has **$16.04** available as a single request, exactly as reported. `540fef`'s **$22.70 is no longer waiting: he requested it at 2026-07-31 08:42:34.014** and it is sitting as `REQUESTED`, $22.70 gross, $20.66 net, STANDARD speed. His displayed balance has correspondingly fallen from $28.32 to $5.62 with $22.70 now locked in flight. **The fix worked and the clipper it unblocked has already acted on it.**

**BL-693's three at $4.09, $1.46 and $0.08 are confirmed exactly**, as the largest single request each can make: `70aa2a` $4.09, `bc64d4` $1.46, `9d81d0` $0.08. **Bucket (b) for these three totals $5.63.** This is the ordinary $10 threshold, not the asymmetry bug, and it must not be paid as though it were stuck money.

### Bucket 3, the genuinely stuck list, $387.81 across 23

Sorted by amount. `stuck` is the portion of the displayed balance the per-campaign gate cannot release. Every row has real retired clips; no row is here for any other reason.

| short id | id prefix | displayed | gate can release | **stuck** | retired clips | campaigns and status | retired between (`::text`) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `3159ac` | `cmps3tgl` | 147.61 | 0.00 | **147.61** | 16 | somesome [PAST] | 2026-07-18 19:09:57.398719 |
| `20d221` | `cmponzpo` | 78.07 | 18.01 | **60.06** | 13 | somesome [PAST] | 2026-07-18 19:09:57.398719 |
| `71108c` | `cmpbazci` | 34.52 | 0.28 | **34.24** | 4 | somesome [PAST] | 2026-07-18 19:10:11.545056 to 2026-07-23 06:00:30.867 |
| `5185f3` | `cmpe951o` | 34.23 | 0.00 | **34.23** | 2 | somesome [PAST] | 2026-07-18 19:10:11.545056 |
| `57560a` | `cmr1rz2j` | 19.09 | 0.00 | **19.09** | 32 | GainzAlgo REPOST [PAST], WinGram [ACTIVE] | 2026-07-18 19:10:11.545056 |
| `c865a9` | `cmpfp1mw` | 18.52 | 0.00 | **18.52** | 22 | somesome [PAST] | 2026-07-18 19:10:11.545056 |
| `3a8763` | `cmp7153e` | 15.45 | 0.00 | **15.45** | 48 | somesome [PAST] | 2026-07-18 19:09:57.398719 to 19:10:11.545056 |
| `64d4a4` | `cmqgqnw4` | 59.75 | 47.77 | **11.98** | 11 | Panic Baby [ACTIVE] | 2026-07-18 19:09:57.398719 to 2026-07-25 06:01:44.456 |
| `70aa2a` | `cmp75zkf` | 13.25 | 5.54 | **7.71** | 32 | GainzAlgo REPOST [PAST], somesome [PAST], WinGram [ACTIVE] | 2026-07-18 19:09:57.398719 to 2026-07-30 06:01:19.473 |
| `540fef` | `cmpfozzs` | 5.62 | 0.03 | **5.59** | 57 | bees.n.honey [ACTIVE], GainzAlgo REPOST [PAST], STRAENGE [PAST] | 2026-07-18 19:09:57.398719 to 19:10:11.545056 |
| `aaebb6` | `cmp7ic4p` | 4.92 | 0.00 | **4.92** | 10 | somesome [PAST] | 2026-07-18 19:10:11.545056 to 2026-07-20 06:00:36.924 |
| `b1865e` | `cmp5a6k0` | 19.66 | 15.90 | **3.76** | 10 | Panic Baby [ACTIVE], somesome [PAST] | 2026-07-18 19:09:57.398719 to 19:10:11.545056 |
| `99635c` | `cmosj3qk` | 3.31 | 0.00 | **3.31** | 12 | Panic Baby [ACTIVE] | 2026-07-18 19:10:11.545056 to 2026-07-31 06:00:23.497 |
| `1e7d9e` | `cmpfn1e5` | 4.00 | 0.88 | **3.12** | 7 | somesome [PAST] | 2026-07-18 19:09:57.398719 to 19:10:11.545056 |
| `f1abe3` | `cmp5j44i` | 2.99 | 0.00 | **2.99** | 1 | somesome [PAST] | 2026-07-18 19:10:11.545056 |
| `5306a1` | `cmoibh57` | 2.82 | 0.00 | **2.82** | 1 | somesome [PAST] | 2026-07-18 19:10:11.545056 |
| `ae9c46` | `cmp48eh8` | 2.76 | 0.00 | **2.76** | 5 | somesome [PAST] | 2026-07-18 19:10:11.545056 |
| `3e9c22` | `cmpb8lbj` | 2.42 | 0.00 | **2.42** | 3 | somesome [PAST] | 2026-07-18 19:10:11.545056 |
| `2b623c` | `cmoagj49` | 6.35 | 4.23 | **2.12** | 4 | bees.n.honey [ACTIVE], somesome [PAST], WinGram [ACTIVE] | 2026-05-15 11:41:14.341199 to 2026-07-18 19:10:11.545056 |
| `ed443f` | `cmpqxvna` | 15.89 | 14.38 | **1.51** | 1 | somesome [PAST] | 2026-07-18 19:10:11.545056 |
| `20bd85` | `cmq2is2j` | 1.38 | 0.00 | **1.38** | 21 | GainzAlgo REPOST [PAST], WinGram [ACTIVE] | 2026-07-18 19:09:57.398719 to 2026-07-23 06:03:27.322 |
| `a92aea` | `cmn4nlfg` | 155.23 | 153.97 | **1.26** | 3 | BAD BITCH ANTHEM [ACTIVE], Panic Baby [ACTIVE] | 2026-07-29 06:00:30.75 to 2026-07-30 06:00:55.212 |
| `df8f32` | `cmogxget` | 0.96 | 0.00 | **0.96** | 9 | somesome [PAST] | 2026-05-15 11:41:14.063779 to 2026-07-18 19:10:11.545056 |
| | | | | **$387.81** | | | |

**The over-held clippers are NOT on this list and are owed nothing.** Six clippers have been paid, or have in flight, more than they have ever earned: $36.75, $29.30, $23.09, $14.46, $7.82 and one at $0.87 whose in-flight request slightly exceeds his earnings, **$111.42 in total**. Every one computes to **globalAvailable $0.00 and gate capacity $0.00** on the merged tree. **BL-627's no-overpayment property is intact and was re-verified this round, not assumed.**

---

## PART 2 — what happens if the owner pays from BL-661's published table today

Walking the 21 rows of BL-661's published table that could be reconstructed from the report (the remaining three published rows are each under $0.50 and immaterial), against today's state:

| short id | BL-661 published | still stuck today | in flight now | **would be OVER-PAID by** |
| --- | --- | --- | --- | --- |
| `540fef` | 20.27 | 5.59 | **$22.70 REQUESTED** | **$14.68** |
| `70aa2a` | 10.57 | 7.71 | 0.00 | **$2.86** |
| `bc64d4` | 0.94 | 0.00 | 0.00 | **$0.94** |
| all other 18 rows | unchanged | unchanged | 0.00 | $0.00 |

# TOTAL DOUBLE PAYMENT IF THE OLD TABLE IS USED VERBATIM: $18.48

**And $22.70 of that risk is already crystallising.** `540fef` requested $22.70 this morning. If that request is approved and paid, and he is also paid his published $20.27, he receives **$42.97** against a true entitlement of **$28.32** ($5.62 displayed plus the $22.70 in flight). **The old table must not be paid from.**

Eighteen of the twenty-one rows are unchanged, so the old table is not worthless; it is wrong in exactly three places, and one of those three is live right now.

---

## PART 3 — is it still growing?

Newly retired approved earnings since the 2026-07-18 bulk event, by day:

| date | clips | clippers | earnings retired |
| --- | --- | --- | --- |
| 2026-07-19 | 6 | 1 | $18.15 |
| 2026-07-20 | 1 | 1 | $1.24 |
| 2026-07-21 | 1 | 1 | $0.00 |
| 2026-07-22 | 4 | 2 | $1.48 |
| 2026-07-23 | 9 | 2 | $1.72 |
| 2026-07-24 | 1 | 1 | $1.12 |
| 2026-07-25 | 7 | 1 | $11.37 |
| 2026-07-27 | 2 | 2 | $0.89 |
| 2026-07-28 | 2 | 1 | $0.00 |
| 2026-07-29 | 5 | 3 | $0.00 |
| 2026-07-30 | 9 | 4 | $3.73 |
| 2026-07-31 | 6 | 1 | $5.60 |
| **13 days** | **53** | | **$45.30, about $3.48 a day** |

**That is higher than BL-657's $1.15 a day**, roughly three times, and BL-657's expectation that the rate would decelerate has not held over these thirteen days.

**Honest limits on projecting it.** $3.48 a day is the rate at which earnings become retired. It is an **upper bound** on how fast bucket 3 grows, not the growth itself: retired earnings only become stuck if the clipper has not already been paid for them and cannot reach them through another campaign. **UNMEASURED:** I have one snapshot of bucket 3 under this formula, so I cannot state its own growth rate; a second measurement in a week would give it.

| horizon | upper bound added | bucket 3 upper bound |
| --- | --- | --- |
| 1 month | ~$104 | ~$492 |
| 3 months | ~$313 | ~$701 |

**The real risk remains the step, not the drip.** A single event created $3,507.71 of retired earnings across 539 clips on 2026-07-18 and is the origin of nearly this entire list. Another mass takedown would add hundreds in a day and dwarf a year of the cron.

---

## PART 4 — what paying bucket 3 would actually cost, per campaign

Retired earnings belonging to the 23 stuck clippers, by campaign:

| campaign | status | budget | affected clippers | retired clips | retired earnings | paying it |
| --- | --- | --- | --- | --- | --- | --- |
| somesome | **PAST** (frozen) | 9,750 | 17 | 155 | $1,668.35 | **new spend on the books, harmless in practice** |
| GainzAlgo REPOST | **PAST** (frozen) | 2,000 | 4 | 108 | $71.70 | new spend, harmless in practice |
| STRAENGE | **PAST** (frozen) | 3,000 | 1 | 10 | $4.15 | new spend, harmless in practice |
| Panic Baby | **ACTIVE** | 3,000 | 4 | 26 | $23.38 | **new spend, and the freed room is genuinely claimable** |
| WinGram | **ACTIVE** | 5,000 | 4 | 22 | $19.07 | **new spend, freed room claimable** |
| BAD BITCH ANTHEM | **ACTIVE** | 1,112 | 1 | 1 | $0.30 | new spend, freed room claimable |
| bees.n.honey | **ACTIVE** | 3,000 | 2 | 2 | $0.00 | no money involved |

**Determined per campaign, not assumed from either prior round, and the answer is BL-657's, not BL-690's.** BL-657 proved from the enforcement code that the instant a clip flips `videoUnavailable` its earnings leave `getCampaignBudgetStatus.spent` and the pool room re-opens. **Everything remaining in bucket 3 is by definition retired-clip money**, so paying it is **new spend on the books on every campaign**.

**BL-690's opposite finding has not been contradicted; it has been resolved.** BL-690 found two clippers whose money sat on **live** clips still counted in spend, so paying them released reserved funds. **That is exactly the money the clamp fix has now released**, which is why it has left bucket 3 and sits in buckets 1 and 2. The two answers were about different dollars, and only BL-657's applies to what is left.

**The material change since BL-657 is that not every campaign is frozen any more.** BL-657 could say every campaign holding this money was paused or finished, so the freed room was claimable by nobody. Today **$42.75 of it sits on three ACTIVE campaigns** where new clips can and do fill the re-opened room. That portion is a genuine potential double-spend, not a theoretical one. The frozen campaigns still hold the overwhelming majority.

---

## PART 5 — the safe payment procedure

If the owner decides to pay bucket 3, this order makes double payment impossible. **No payment was made by this round.**

1. **Use the bucket 3 table in PART 1 of this report. Do NOT use BL-661's table, and do not use BL-693's $544.77 figure.** Both are superseded.
2. **Re-run the bucket 3 query immediately before paying** (the SQL is `docs/STUCK-MONEY-CURRENT.md`'s companion query below). Balances move every hour: this list changed measurably between 08:37 and 10:02 on the day it was written.
3. **For each person, immediately before paying, check they have no payout in flight.** `540fef` proves why: he had none when BL-692 measured and had $22.70 REQUESTED thirty-nine minutes later. Any clipper with a `REQUESTED`, `UNDER_REVIEW` or `APPROVED` row must be **skipped**, because that request will pay them through the normal route.
4. **Pay only the `stuck` column, never the `displayed` column.** The displayed figure includes money the gate can already release, and paying that is a double payment by definition.
5. **Skip the six over-held clippers entirely.** They are owed nothing and are correctly blocked.
6. **Record each manual payment somewhere the platform can see it.** A manual transfer that leaves no `payout_requests` row is invisible to every balance calculation, so the clipper's displayed balance will not fall and the same money can be paid again next month. **This is the largest ongoing risk in the whole procedure.**
7. **Afterwards, re-run the verification query below** and confirm nobody received both a manual payment and a released balance for the same earnings.

### The verification query

Run before and after any manual payment. Any clipper appearing in both result sets has been paid twice for the same dollars.

```sql
-- Anyone with money in flight through the normal route. Do NOT pay these people manually.
SELECT now()::text AS db_now,
       substr(md5("userId"),1,6) AS short_id,
       status,
       amount,
       "createdAt"::text AS requested_at
FROM payout_requests
WHERE status IN ('REQUESTED','UNDER_REVIEW','APPROVED')
ORDER BY "createdAt";
```

Cross-reference that short-id list against the bucket 3 table before paying anyone. Today it returns `540fef` at $22.70, who is on the bucket 3 list and **must be skipped**.

---

## PART 6 — the verdict

**The genuinely stuck total is $387.81 across 23 clippers, down from $408.40 across 26 immediately before the clamp fix, and not comparable to the $544.77 across 41 that BL-693 published, because that figure was produced by a formula that ignores the per-campaign structure the gate actually applies.**

**Paying BL-661's published table verbatim today would over-pay by $18.48 across three clippers, and $22.70 of that is already in flight as a live payout request made this morning.**

**Recommended next step: replace the published list with the bucket 3 table above, and decide the policy question separately from the arithmetic one.** Nothing here is urgent in the sense of getting worse quickly, at roughly $3.48 a day of newly retired earnings and an upper bound near $492 in a month, and the clamp fix has already resolved the part of this that was a genuine defect. What remains is a policy question BL-657 framed correctly and which has not changed: whether earnings on genuinely deleted videos should be paid at all. **If the owner decides to pay, the procedure in PART 5 makes it safe. If he decides not to, the honest step is to stop showing clippers a balance that includes money the platform will never release, which is a display change and not a payment.** The one thing that should not happen is paying from the old list.

### What could not be measured

Bucket 3's own growth rate is **UNKNOWN**: this is the first measurement under a formula that models the gate correctly, so there is no prior point to difference against, and PART 3's projection is an upper bound derived from the retirement rate rather than an observation. Whether any clipper has already been paid manually outside the payout system is **UNKNOWN and unknowable from the database**, because such a payment leaves no row; that is the risk step 6 above exists to close.

### A methodology note, disclosed rather than buried

Two earlier drafts of this measurement were wrong and were caught before publication. The first used Postgres `LEAST` against a possibly-NULL per-campaign value; `LEAST` ignores NULLs, so clippers with no reachable campaign appeared able to withdraw their full balance, inflating the released figure to $86.39. The second took the **maximum** single campaign rather than the **sum**, understating what a clipper can reach across several campaigns. The figures published here use the sum across campaigns with the $10 minimum applied per request, which is what `payouts/route.ts` actually enforces, and they reproduce BL-692's five movers and BL-693's pre-fix population exactly when the same model is applied to both.

---

## Safety

READ ONLY. One document. **No payout was created, modified, approved or cancelled. No balance was written. No env flag was flipped**, and `GLOBAL_PAYOUT_CLAMP_ENABLED` is neither recommended nor used as a rollback, per BL-690's finding that disabling it removes the overpayment block entirely. Every dollar of the $2,058.62 displayed across 128 clippers is classified into exactly one of three buckets and the three subtotals reconcile to the whole to the cent. The six over-held clippers are excluded from anything owed and **BL-627's no-overpayment property was re-verified on the merged tree, all six computing to $0.00**. Every figure comes from read-only `SELECT`s via the sanctioned `scripts/run-select.js`, with every timestamp cast to `::text` and anchored against DB `now()`. **No handle, email or wallet address appears anywhere.** Nothing a live round holds, including BL-694 and BL-696, was touched; this round worked in its own worktree at `C:/b695` on `checkpoint/BL-695`. A markdown-only diff cannot change tsc or the build, so **no build was run and none is claimed**. NO dashes used as bullets.
