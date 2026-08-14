# BL-807 — the full health check after the quiet days: the money is correct, and the redeploy already happened

> **NO MONEY HAS APPEARED FROM NOWHERE. $0.00, zero clippers.** Every one of the 4,745 approved live clips was recomputed from its own views and its own frozen stamped CPM. **Not one clip and not one clipper holds a cent more than that arithmetic supports.** The platform is under credited by **$1,883.92**, not over credited, and 99.95 percent of that sits on campaigns that hit their budget cap and stopped.

**2026-08-14 · DB `now()` = `2026-08-14 20:01:44.169683+00` (first read) to `2026-08-14 20:11:36.160907+00` (last) · AUDIT ONLY. READ ONLY.**
Nothing was changed. No code, data, schema or config. Nobody was paid. No payout created, altered, approved or voided. No balance touched, nothing restamped, nothing retired, nothing deployed. `agency-monitor --fix` never run. No Apify actor and no paid probe: **spend for this round is $0.00.** Base `origin/main` @ `3a1b6a34`, isolated worktree `C:/w807` at a short path, `node_modules` never junctioned, **removed at the end**. Every database read through `scripts/run-select.js`. Every timestamp cast `::text` against DB `now()`, and naive UTC columns compared only against `now() AT TIME ZONE 'UTC'`.

Clippers are identified by **`id8`** (first 8 characters of the user id) and **`md6`** (`substr(md5(userId),1,6)`), the two forms every earlier round used, so the owner can map them privately in admin. **No handle appears anywhere. No wallet address was selected, printed or partially printed.**

**On "two quiet days".** The last commit on main, `3a1b6a34`, was authored **`2026-08-13 18:43:45 UTC`**, which is **25.3 hours** before this audit, not two days. The platform, however, has not been quiet at all: 531 clips submitted, 334 clip decisions, 6 payments and 3 clipper problem reports since BL-758. What has been quiet is the shipping, not the product.

**Money files byte identical by blob OID across the whole chain** (`d004b396` → `15fc29b1` → `3a1b6a34`), verified by `git rev-parse <ref>:<path>` and never by comparing a working tree hash: `clip-earnings-writer.ts` `ac5be7de`, `earnings-calc.ts` `797e2098`, `balance.ts` `e887f80a`, `tracking.ts` `83ce4bab`, `clip-earnings-invariant-middleware.ts` `61cef393`, `money-decimal.ts` `ef5cdae7`, `campaign-era.ts` `106e16ad`. **All seven unchanged.**

---

## PART 1 — THE MONEY

### 1.1 The recompute BL-758 declined to run, run in full

BL-758 refused this and gave sound reasons: earnings are not a pure function of current views, because they pass through `payoutReductionRatio`, `maxPayoutPerClipAtApproval`, `minViewsAtApproval`, per tick pool cap trimming, and BL-718's `capButNeverBelowStored` floor. Those confounders are real. They are also **measurable**, and this round measured them rather than citing them.

The ceiling was rebuilt per clip in the order `earnings-calc.ts:135-186` applies it: the minimum views gate, then views divided by 1000 times the clip's own `cpmAtSubmissionDecimal`, then the per clip cap on **base before bonus**, then `payoutReductionRatio` as a multiplier (`earnings-calc.ts:556-576`, a no op when the ratio is null, negative or at least 1). Earnings ratchet and never decrease, so **peak views is the honest basis**; latest views is reported alongside it.

| | latest views basis | **peak views basis** |
|---|---|---|
| stored `baseEarnings` | $12,010.79 | $12,010.79 |
| recomputed ceiling | $13,683.19 | **$13,894.71** |
| **signed difference (stored minus recomputed)** | −$1,672.40 | **−$1,883.92** |
| **clips ABOVE the ceiling** | **1** (+$1.44) | **0** |
| clips below the ceiling | 681 | 786 |
| clips matching within $0.01 | 4,063 | 3,959 |

**Zero clips and zero clippers are above the ceiling on the peak basis.** The single latest basis outlier, clip `cms2iisc` held by `cmryam5j` / `5e1e62`, has peak 79,577 views against latest 69,458; its stored $36.17 sits between the latest figure $34.73 and the peak figure $39.79. That is the ratchet doing exactly what it is built to do, and against peak the clip is **$3.62 under credited**.

Classification of everything above any ceiling, with no residue: views fell since the last write, **1 clip, $1.44**, fully explained. Carries a `payoutReductionRatio`, **0 clips**. Sits on a budget exhausted campaign where `capButNeverBelowStored` refused to subtract, **0 clips**. No `clip_stats` row or a null stamp, **11 clips, all holding exactly $0.00**, which cannot create money. **Genuinely unexplained: 0 clips, $0.00.**

**Independently cross checked.** I ran a separate coarser recompute of my own before the subagent reported, with a different rounding treatment and a different `payoutReductionRatio` guard. It returned the same decisive result: **0 clips above the peak ceiling**, under credit in the same $1.88k band. Two independent computations, one conclusion.

**The other half, stated rather than folded away.** The $1,883.92 under credit is real. 745 clips carrying **$1,859.45** sit on PAST campaigns that hit their budget cap (`lastBudgetPauseAt` set), 37 clips carrying $21.53 on paused budget capped campaigns, and 4 clips carrying $0.96 on one active campaign. **99.95 percent is documented pool cap trimming on campaigns that stopped.** The alternative explanation, that the peak arrived after the last earnings write, was tested and **rejected: 0 of 786 clips**. It cannot be decomposed further from stored state, because there is no per tick pool cap audit trail, and I will not claim a precision that does not exist. The direction is under payment. It is not money creation.

### 1.2 Nobody's paid plus claimable exceeds what they earned — BL-627, re-verified not inherited

Measured over **259 users** holding any approved earnings or any payout row, using `isPayoutMoneyOut` (`balance.ts:117-124`: PAID always, VOIDED only when `paidAt` is not null) and `clipperLiability` (`balance.ts:126-132`: `actualPaidAmount ?? amount`, gross, never `finalAmount`).

| id8 | md6 | lifetime earned | paid | excess | available |
|---|---|---|---|---|---|
| `cmofpudr` | `2abe41` | $1,570.58 | $1,607.33 | **$36.75** | **$0.00** |
| `cmoaejuc` | `f95b37` | $38.80 | $61.89 | **$23.09** | **$0.00** |
| `cmq0qn2l` | `fa0da6` | $0.00 | $14.46 | **$14.46** | **$0.00** |
| `cmoal818` | `7ef3f3` | $4.94 | $12.76 | **$7.82** | **$0.00** |

**4 clippers, $82.12, every one clamped to exactly $0.00 available. Clippers who could withdraw more than they earned: 0 of 259. BL-627's property holds.** Identical to BL-758 to the cent, same four ids: the population has not grown in four days.

**A contradiction between two subagents, resolved rather than averaged.** One measured 4 clippers and $82.12; another measured 7 and $143.41. Both are right about different quantities, and I verified the reconciliation directly. **Globally** 4 clippers are over by $82.12. **Per campaign** 7 clippers are over by $143.41, the extra three being covered by earnings on another campaign: `cmqez5c2` $60.47 on STRAENGE, `cmp71p89` $0.80 on somesome, `cmqmnvgs` $0.02 on WinGram. $82.12 plus $61.29 equals $143.41 exactly. The per campaign figure is the one that matters for `cmqez5c2`, and it is PART 6 item 7.

### 1.3 No campaign exceeds its budget — BL-627's property, which BL-718 nearly broke

**0 of 19 comparable campaigns exceed budget on realized live spend.** Fifteen further campaigns carry a null budget and cannot be compared at all; every one is a zero clip, zero money test artefact.

| campaign | status | budget | clipper live | owner live | total | **remaining** |
|---|---|---|---|---|---|---|
| **STRAENGE** | PAST | $3,000.00 | $1,997.56 | $998.48 | $2,996.04 | **$3.96** |
| Panic Baby | PAST | $3,000.00 | $1,969.39 | $983.56 | $2,952.95 | $47.05 |
| bees.n.honey | PAST | $3,000.00 | $1,565.59 | $1,283.35 | $2,848.94 | $151.06 |
| every other campaign | | | | | | comfortable |

**STRAENGE has $3.96 of headroom**, $1.90 on the stricter unfiltered owner reading. It is the tightest position on the platform and it is PAST, so nothing new should land on it.

**Panic Baby is no longer at its cap.** BL-758 recorded it at exactly $3,000.00 of $3,000 with $0.00 remaining. It now reads $2,952.95 with **$47.05 remaining**, and the reason is measurable rather than mysterious: 70 of its clips have been retired since, holding $59.91, so the money was reclassified, not un spent. Its lifetime clipper earnings including retired clips are still $2,029.30.

Under the loosest possible reading, lifetime earnings including retired videos plus the unfiltered agency sum, three campaigns edge negative: Panic Baby by $42.64, bees.n.honey by $13.14, STRAENGE by $2.25. **I am not calling that a breach.** It counts money on videos that no longer exist plus agency rows whose clips are no longer live, which is precisely the direction BL-642 established errs safe by inflating `spent` so a campaign auto pauses early.

**The 34th campaign**, new since BL-758 saw 33, is **SomeSome App**: ACTIVE, budget $2,214.00, created `2026-08-12 13:38:10.125`, 13 clips of which 2 approved live, `guaranteeOwnerSplit` with a locked share of 0.33333333. **It carries $0.00 of clipper earnings and $0.00 of owner earnings.** No money rests on it. Its budget was reduced $2,500 to $2,214 by the owner on `2026-08-12 14:28:31.407`, logged as `CAMPAIGN_BUDGET_CHANGED`.

**The L1 budget hard lock is firing in production, and this is the best money evidence in the round.** `audit_logs` holds **13 `BUDGET_HARDLOCK_THROW` rows** across 9 clips, **8 of them carrying `throwReason: "already-over-budget"`**, the most recent `2026-08-12 16:34:21.320` on Panic Baby. Each row records a write the L1 chokepoint in `writeClipEarnings` **rejected**: deltas of $0.50, $0.51 and $0.55 that were never applied. The three target clips still carry **$0.78, $0.00 and $0.00** today, confirming the rejections held.

**A subagent read those rows as $0.25 of spend landing on a campaign already at its cap, and flagged it as the one movement with no sanctioned cause. That reading is wrong and I checked it rather than passing it on.** A `BUDGET_HARDLOCK_THROW` is the defence working, not a payment. The `spent` figure inside the row is the L1's own reading, which per `balance.ts:354-355` uses the **unfiltered** owner aggregate, so BL-642's phantom agency rows on retired and flagged clips move it without a cent reaching anyone. The $0.25 drift between the 08-09 and 08-12 rows is that documented behaviour, and it errs safe by auto pausing early. **No clipper was overpaid and no write succeeded.**

### 1.4 The earnings invariant

| population | rows | violations | total signed drift | max single drift |
|---|---|---|---|---|
| APPROVED, not deleted | **4,745** | **0** | −$0.0100 | $0.0100 |
| every clip | **5,851** | **0** | −$0.0100 | $0.0100 |

**Zero violations.** The whole platform wide drift is one cent, on a single clip sitting exactly at the tolerance boundary rather than over it. BL-758 measured 0 across 4,308 clips; the population has grown by a third and the invariant still reads zero.

### 1.5 Every clip earns off its own frozen stamp

**Clipper side: proven, without exception.** Of 4,745 approved live clips, **0 have a null `cpmAtSubmissionDecimal` and 0 have a non positive one**, and **0 carry a `cpmOverriddenAt`**. There is no clip on the platform earning off a live campaign rate.

**Owner side: still not stamped, and this is unchanged rather than new.** **2,973 of 4,745 clips (62.7 percent)** have a null or zero `ownerCpmAtSubmissionDecimal`, so they resolve the owner rate live on every tick. BL-758 measured 2,972 of 4,308. Of those unstamped clips, 1,164 nonetheless hold **$3,677.00** of `agency_earnings` that has no stamp to check against. Tested against the live `campaigns.ownerCpm`, 391 match, 508 are below, and **265 are $101.74 above**. That $101.74 is **not evidence of fabrication** and I will not present it as such, because the live owner rate may have moved since; it is **unverifiable by construction**, and that is the honest verdict. **No clipper is affected by any of it.**

**The stamp versus locked share test (BL-539, BL-563, BL-570) is contained and has not grown.** Comparing `ownerCpmAtSubmissionDecimal / cpmAtSubmissionDecimal` against `s/(1−s)` at BL-563's 0.01 tolerance, across 12 `guaranteeOwnerSplit` campaigns holding both stamps:

| campaign | clips with both stamps | **ambiguous** | clipper earnings on ambiguous rows |
|---|---|---|---|
| **somesome** | 182 | **179** | **$2,298.55** |
| every other campaign (11) | 1,586 | **0** | $0.00 |

**179 clips on somesome and nowhere else, identical to BL-758 to the cent.** The three newest split campaigns, Zhus Meme, Zhus Edit and SomeSome App, carry 700 clips between them and reconcile perfectly, so **the defect is not reproducing on new work.** This remains BL-570's $933.94 do not touch, and no platform wide owner re-derive was run.

### 1.6 The four platform totals

| | today | BL-758 (2026-08-10) | change |
|---|---|---|---|
| **TOTAL EARNED** (approved live, the global clamp's base) | **$12,551.91** | $12,154.11 | **+$397.80** |
| of which sits on videos now unavailable | $3,629.74 across 707 clips | $3,605.15 | +$24.59 |
| payable subset (`videoUnavailable = false`) | $8,922.17 | not stated | |
| **TOTAL PAID** (money that has actually left) | **$9,305.03 across 91 PAID rows** | $8,881.01 / 85 | **+$424.02, +6 rows** |
| in flight, requested and awaiting the owner | **$248.40 across 7 rows** | $580.81 / 9 | **−$332.41** |
| still owed on the books (per clipper, clamped at zero) | **$3,329.00** | $3,355.22 | −$26.22 |
| **TOTAL WITHDRAWABLE today, unaided** | **$2,206.13** | $1,944.39 | **+$261.71** |
| **VISIBLE BUT UNWITHDRAWABLE** | **$874.56** | $830.02 | **+$44.54** |
| of which earnings on videos that no longer exist | $404.21 | $403.61 | +$0.60 |
| of which below the campaign minimum | $470.35 | $426.41 | +$43.94 |

**The identity closes with no residual:** `248.40 + 2,206.13 + 874.56 = 3,329.09`, and `404.21 + 470.35 = 874.56`. The $0.09 against the clamped owed figure is per clipper rounding, disclosed rather than hidden. Independently, global available measured directly as the sum of `max(earned − paid − locked, 0)` is **$3,080.69**, and `3,329.00 − 248.40 = 3,080.60`, agreeing to nine cents.

**A second contradiction, resolved by measurement.** One subagent stated that every campaign's `minPayoutAmountDecimal` is NULL and therefore every minimum is the $10 default. **That is wrong.** Three campaigns carry a non default minimum: **Zhus Edit $20.00, Zhus Meme $20.00, and SomeSome App $15.00**, the last being new since BL-758, which recorded only the two Zhus raises. I recomputed the whole reachable figure myself with the correct floors and with a flat $10 floor: a flat $10 would **overstate reachable by $71.37 across 5 clippers**. Because that subagent reported $2,206.10, the real floor figure and not the $2,277.50 flat figure, **its arithmetic was correct and only its prose was wrong.** My independent recompute returns $2,206.13. The figure stands; the sentence did not.

### 1.7 The answer to the owner's question

**No money has been created from nothing. $0.00. No clipper is named because there is none to name.** Every standing property re-verified on live data rather than inherited: no overpayment holds, no campaign over budget holds, the invariant reads zero violations across 5,851 clips, and every clip earns off its own frozen clipper stamp.

---

## PART 2 — WHAT MOVED, AND WHETHER IT SHOULD HAVE

| measure | BL-758 (08-10) | BL-801/805/806 (08-13) | **today** | cause |
|---|---|---|---|---|
| clips, all | — | 5,681 | **5,851** | 531 submitted since BL-758. Ordinary. |
| approved live clips | 4,308 | 4,538 | **4,745** | 428 of the 531 new clips approved, plus 9 older pending clips decided. Ordinary. |
| approved live earnings | $12,154.11 | — | **$12,551.91** | +$397.80 against **$431.64** of growth that view accrual alone justifies on the 1,290 clips touched. **Under what views support.** |
| payout rows | 165 | 167 → 168 | **169** | four new requests, each accounted for below. |
| PAID rows / value | 85 / $8,881.01 | — | **91 / $9,305.03** | 6 payments, all by an OWNER account. |
| campaigns | 33 | — | **34** | SomeSome App, created 08-12, $0.00 on it. |
| users | — | 1,400 | **1,415** | ordinary signups, 6 to 13 per day. |
| retired approved clips | 666 | — | **707** | retire-dead-clips at 06:00 UTC daily, roughly 7 per day, unchanged rate. |
| conversations / messages / people | — | 55 / 109 / 51 | **55 / 109 / 51** | **frozen.** See below. |
| problem reports | — | 1 | **4** | the new button is being used. See below. |
| referral commissions | — | 6 / $109.57 | **7 / $111.53** | one new row, arithmetic verified below. |
| held above earnings | $82.12 / 4 clippers | — | **$82.12 / 4 clippers** | unchanged, same four ids. |
| FLAGGED clips | 3 carrying $113.50 | 6 (BL-801) | **6 carrying $113.50** | 3 zero earning clips flagged between BL-758 and BL-801. **The money is identical.** |
| earnings invariant violations | 0 | 0 | **0** | unchanged. |

**Nothing moved without an obvious cause.** Every line above is attributable, and two lines are worth naming for what they prove rather than what they changed.

**The chat is frozen at exactly the right instant.** Conversations, messages and participants are unchanged from BL-805's 55 / 109 / 51, and the newest message in the entire system is still `2026-08-13 15:06:04.572` — the clipper who opened a chat at 15:05. **Not one message has been written since.** That is precisely what a successful redeploy removing the chat looks like from the data side, and it independently corroborates PART 3.

**The report button replaced it and is working.** `problem_reports` went 1 to 4. The three new rows are real CLIPPERs on 2026-08-14 at 11:49:38.449, 12:13:13.928 and 15:07:38.004, submitted at **viewport widths of 360 to 363 pixels in installed app mode**. That is direct production evidence that the report entry is reachable on a phone, which is the exact failure BL-803 found in the old chat launcher and BL-804 fixed. **A correction to BL-806:** it described the single existing row as "a real user's report". That row (`2026-08-13 17:39:07.061`, a 7 character body) belongs to `cmnd5tai`, an **OWNER** account. It was the owner testing his own button, not a user report.

### Did any clip's earnings rise faster than its views justify

**No.** Across the 1,290 approved live clips whose `updatedAt` moved since BL-758, the maximum growth justified by view accrual at each clip's own stamped CPM is **$431.64**, against actual platform earnings growth of **$397.80** which also includes 428 brand new clips. The recompute in PART 1.1 is the stronger form of the same answer: **0 clips of 4,745 sit above their own peak views ceiling.**

### Did any earnings figure move DOWN

**No, on every measure.** Approved live clips whose `earnings` is below their own `savedEarnings`: **0**. Approved live clips with `earnings = 0` but a positive `baseEarnings`: **0**. REJECTED clips carrying stale base and bonus against zero earnings: **0** — BL-617 recorded 9 such clips holding $42.15 of cosmetic residue, and **that has since cleared entirely.** The never decrease guard and BL-718's `capButNeverBelowStored` are both holding.

### Every payout created, approved or paid in the window, with its actor

**Six payments, totalling exactly $424.02, every one actioned by an OWNER account (`cmn4m6lh`).**

| row8 | clipper8 | gross | paid at (::text) |
|---|---|---|---|
| `cmsgdfcv` | `cmpp3jgm` | $12.14 | 2026-08-11 14:35:01.010 |
| `cmsjtbee` | `cmryxhyv` | $227.62 | 2026-08-11 18:46:28.546 |
| `cmsjterz` | `cmryxhyv` | $19.34 | 2026-08-11 18:46:30.325 |
| `cmsj32eq` | `cmryam5j` | $102.88 | 2026-08-13 20:21:36.158 |
| `cmsm2ae0` | `cmrl046b` | $21.25 | 2026-08-13 20:34:37.016 |
| `cmsg7dgp` | `cmpoj6uo` | $40.79 | 2026-08-13 21:17:33.740 |

Four new payout requests were created since BL-758, all by the clippers themselves: `cmsnvqqn` $46.51 (08-10), `cmsq04pf` $10.00 (08-12), `cmsri38a` $10.54 (08-13) and `cmst92ua` $24.56 (**2026-08-14 17:58:03.747, roughly two hours before this audit**).

**Every sensitive action in the last two days was performed by an OWNER account. No reviewer, no admin and no unknown actor touched anything.** From `audit_logs`: 287 clip approvals (286 by `cmnd5tai`, 1 by `cmn7d5hr`), 47 rejections (`cmnd5tai`), 3 payout approvals and 3 payments (`cmn4m6lh`), 2 clip campaign reassignments (`cmnd5tai`). The 7 `SERVER_ERROR` rows are the owner's own session and were already disclosed by BL-800 and BL-801 as the render pass side effect; the last is `2026-08-13 19:35:07.171` and none is new.

### The 5 percent referral earning, after BL-799 issued 1,039 codes

**It is behaving correctly and has not double credited anyone.**

**No double credit, and it is structurally impossible rather than merely absent.** Grouping by `sourcePayoutRequestId` returns **0 groups with more than one row**: 7 commissions against 7 distinct source payouts. Grouping by referrer, referred user and source returns **0 duplicates**. Two rows do share a referrer and referred user (`cmoboo97` to `cmofpudr`) but sit on **different source payouts**, which is legitimate. **Decisively, `pg_indexes` confirms a UNIQUE index `referral_commissions_sourcePayoutRequestId_key` on `sourcePayoutRequestId`**, so a second commission against the same payout would fail at the database, and the create path catches the resulting P2002 for idempotent re-PAID. This is the same class of guarantee BL-696 found on `uq_payout_open_per_user_campaign`: a database constraint, not an application check.

**Arithmetic, checked row by row against the implemented basis.** The code at `src/app/api/payouts/[id]/review/route.ts:616-620` uses `effectivePaid = actualPaidAmount ?? finalAmount ?? amount`, that is the **net after fee**, falling back through the coalesce chain. **All 7 rows agree with that basis to within $0.01**, including the oldest row `cmpjx7hy`, which uses its `actualPaidAmount` of $629.52 because that field is first in the chain. All seven carry `rateBps = 500`. The one new row since BL-801, `cmss0rk3` created `2026-08-13 21:17:34.209`, is **$1.96 on a $39.16 net — exact**, minted 0.43 seconds after the payment of `cmsg7dgp`, which is the correct trigger. **Zero arithmetic defects.**

**The reverse test, which matters as much as the double credit test: nobody is missing a credit.** Two PAID payouts belong to users who currently hold a `referredById`, and **both have a commission row**. Zero missing.

**One policy question, disclosed rather than called a bug.** Measured against the **gross** rather than the net, 6 of the 7 rows are short by a combined **$3.32**. That is not a broken calculation, it is a definition: is the referrer's 5 percent owed on what the clipper requested or on what the clipper actually received after the platform fee? The code has consistently chosen net since 2026-05-29. **Only the owner can say whether that is the intended deal.**

**Coverage.** 1,363 of 1,415 users hold a referral code and **all 1,363 are distinct — zero collisions.** 174 users carry a `referredById`. 20 live non deleted CLIPPERs lack a code, up from BL-801's 8.

**Every one of the 20 signed up on or after `2026-08-12 17:55:55`, so BL-799's backfill missed nobody.** All 174 users who carry a `referredById` have a referrer holding a code, so no referral chain is broken.

**A subagent concluded from this that new signups are never minted a code and nothing back fills them, calling it a live gap. I read the code rather than inferring, and that is not what happens.** `ensureReferralCode` (`src/lib/referrals.ts:16`) is called from exactly two places, `/api/referrals` and the reviewer grant route, and **never at signup**. Codes are minted **lazily**, the first time a clipper opens their own referrals page. The 20 are simply clippers who have not opened that page yet, and each will get a code the moment they do. The daily pattern fits exactly: signups on 08-10 and 08-11 show 100 percent coverage because the backfill caught them, while 08-13 and 08-14 show 3 of 13 and 2 of 10, the minority being those who visited the page. **It self heals, no referral is lost, and it needs no second backfill.**

**Fee consistency, re-measured and identical to BL-758 in both directions.** 8 PAID rows at `feePercent = 4` totalling $2,826.64 gross belong to 6 users with no `referredById` today, implying the same **$141.33** owner side shortfall, and **0 rows across all 169** exist where a referred user was charged 9 percent. Neither number has moved. No clipper was ever overcharged; the shortfall costs only the owner and remains historical.

---

## PART 3 — IS THE LIVE SITE RUNNING THE MERGED CODE

> **YES. The owner did redeploy. Live is serving `3a1b6a34`, and no further redeploy is needed.**

Proven from the live site itself, unauthenticated, never by inference from the repository, and confirmed twice by two independent passes.

**The dating argument.** Main's tip `3a1b6a34` was committed **`2026-08-13 18:43:45 UTC`**. Every one of the 16 JavaScript chunks and both CSS bundles served by clipershq.com carries `last-modified: Thu, 13 Aug 2026 18:56:16–18:56:17 GMT` — **12 minutes 32 seconds after that commit.** Decisively, **the exact CSS chunk BL-803 measured on 2026-08-12 now returns 404**: the previous build has been replaced, not merely supplemented. Nothing has been pushed since `3a1b6a34`, so the running build can only be that commit.

**The content argument.** Every discriminating string was first verified absent at `d004b396` and present at `3a1b6a34` using `grep -c`, never piped through `head`, then searched inside bundles downloaded from clipershq.com. Occurrence counts, not line counts:

| string | in the live bundle |
|---|---|
| `Use this to tell the team about anything that looks broken or wrong` (BL-806's only change) | **1** |
| `This form goes one way` | **1** |
| `Close report a problem` | **1** |
| `Chat Archive` (BL-804's sidebar entry) | **1** |
| `Send us a message and the team will get back to you here` (**chat copy, deleted**) | **0** |
| `ChatWidget` / `needsHumanSupport` / `/api/chat/` | **0 / 0 / 0** |

**The negative test is load bearing rather than vacuous:** `ReportProblemWidget` sits in the same app shell chunk `ChatWidget` used to occupy, both imported by `app-layout.tsx`. The new copy is present in exactly the chunk the old copy has vanished from.

### Each change, checked individually

| change | verdict | evidence |
|---|---|---|
| the chat is gone with no reachable route | **LIVE** | all 8 `/api/chat/**` probes return **404 with a body byte identical (40,799 bytes) to the nonexistent route control**, while sibling gated routes return 401 or 405. Independently, zero chat strings survive in the bundle, and the database shows **zero chat messages since `2026-08-13 15:06:04.572`**. |
| the one sentence explanation | **LIVE** | 1 occurrence in the live chunk, 0 occurrences at `d004b396`. |
| the owner only chat archive | **LIVE (existence); owner only NOT proven** | `/admin/chat-archive` returns **200** against a **404** control at `/admin/definitely-not-a-page-bl807`; the sidebar string is in the live chunk. The 200 is the pre hydration splash shell containing **no archive data at all**. The guard itself needs a signed in session to test and **I did not sign in to production**, so I am not claiming it. |
| the report entry visible at 320 pixels | **LIVE, and now confirmed by real production use** | The launcher markup in the live bundle carries no display gate: `hidden md:inline-flex` occurs **0** times anywhere, and the live stylesheet contains the `bottom-[calc(env(safe-area-inset-bottom,0px)+104px)]` rule **unconditionally, inside no media query**, so it applies at 320px. A fetch cannot prove nothing overlaps it in a real viewport. **The database settles what the fetch cannot: three real clippers filed reports through it today at 360 to 363 pixels.** |
| the partner reviewer surfaces | **LIVE for BL-788 and BL-799; not applicable for BL-802** | BL-799's nav strings are in the live chunk (`Review queue` 1, `My proposals` 1, `REFERRAL_MANAGE` 3). BL-788's routes answer as existing and gated (`/api/clips/abc/review` 405, `/api/admin/users/abc/reviewer-config` 401) against a 404 control. **BL-802 was data only** — a single database column — so it cannot appear in any bundle and no outside fetch can confirm or deny it. |

**What outside evidence still cannot give** is the commit hash Railway believes it is serving, only the build time and its contents. If the owner wants the hash itself: **Railway, service `web`, Deployments, the active deployment's commit hash.** It should read `3a1b6a34` with a build starting around 18:44 to 18:56 UTC on 2026-08-13. **The "requires a Railway REDEPLOY" warnings on the `15fc29b1` and `3a1b6a34` commit messages are now stale.**

---

## PART 4 — THE TRACKING AND EARNING MACHINERY

### The crons are alive

| cron | last fire (::text) | age | fires / 24h | BL-617 reference | verdict |
|---|---|---|---|---|---|
| **tracking** | `2026-08-14 20:01:16.629` | 3 min | **144** | 143 | HEALTHY |
| **lifecycle** | `2026-08-14 20:00:18.100` | 4 min | **96** | 97 | HEALTHY |
| **watchdog** | `2026-08-14 20:00:18.344` | 4 min | **48** | 49 | HEALTHY |
| **retire-dead-clips** | `2026-08-14 06:00:38.892` (by effect) | 14 h | 1 daily | BL-593's 06:00 UTC | HEALTHY |

**No gap over 90 minutes for any heartbeat cron in 72 hours.** All three fired within four minutes of this audit, and I confirmed these figures independently before the subagent reported them.

**An honest limit, stated rather than glossed.** `cron_runs` has **no success or error column**, so what is measurable is the last **fire**, not the last **success**. Every claim above is backed by side effect: clip_stats rows were written in all 25 hourly buckets of the last 24 hours (most recent `2026-08-14 20:01:15.772`), and the exact hour ticks number **24 in 24 hours, a complete set with no missed hour**. `cron_locks` is **empty**, so nothing is stuck.

**retire-dead-clips writes no heartbeat row at all.** By side effect it is running exactly on schedule: **every single retirement in the last 26 days falls inside 06:00:0x to 06:04 UTC**, most recently `2026-08-14 06:00:38.892`. Two days (08-04, 08-07) show zero retirements, and I cannot distinguish "ran and found nothing" from "did not run" without a heartbeat row. Adding one is what would close that gap; nothing else would.

### First stats, per platform

| platform | clips with a stat (7d) | **median delay** | within 60s |
|---|---|---|---|
| Instagram | 794 | **0.0 s** | 68% |
| TikTok | 59 | **0.0 s** | 86% |
| YouTube | **0** | not computable | |

**Has Instagram regressed? No, not now — but it did, for 18 days, and the fix landed five days ago.** The 7 day aggregate hides a sharp break that the daily series exposes:

| period | IG median first stat | within 60s |
|---|---|---|
| through 2026-07-21 | **0.0 s** | ~100% |
| **2026-07-22 → 2026-08-09 ~15:00 UTC** | **2,825 to 4,853 s** | **0 on every single day** |
| 2026-08-10 → 2026-08-14 | **0.0 s** | ~100% every day |

The recovery is precise to the hour: clips created in hour `2026-08-09 14:00` still had a median of 4,062 seconds; clips created in hour `15:00` had **0.0 seconds**, and it has held at zero every hour since. **869 Instagram clips were created inside that window** and got a first stat 45 to 80 minutes late. TikTok was never affected. **This matches BL-782's 0 second median today**, and the entire p90 tail in the 7 day table is the residue of 08-07 to 08-09 ageing out. YouTube cannot be measured because **zero YouTube clips have been created in 7 days** — an absence of traffic, not a failure.

Clips created in the last 7 days with no stat at all: **12**, none under 24 hours old. Eleven are REJECTED Instagram clips where tracking legitimately stops. One is a genuine small anomaly, a TikTok PENDING clip (`cmsoyebz`) carrying **$0.00** which has an active job but has never produced a stat in 3 days.

### View decreases

| | today | BL-753 | change |
|---|---|---|---|
| decrease **events** | **1,340** | 1,245 | +95 |
| distinct clips involved | **704** | 650 | +54 |
| clips currently below their own peak | **241** | | |

Movement is modest and consistent with continued organic recounting. **BL-753's decision to reject a guard against decreases still looks right.**

**Implausible movement, separated out and quantified: 108 events across 80 clips**, of which 51 are drops to exactly zero. Money sits on only three of them, all Instagram, all held by `cmr0gixm`, carrying **$543.91**. Their signature is provider corruption rather than organic decay: clip `cms7ogj2` ($300.00) oscillates between roughly 730,000 views and a near constant **1,213** across consecutive four hourly checks, against a smoothly rising 700k series. **No money is currently mis stated** — all three sit at their peak, so stored earnings rest on the correct high value. Had a recompute landed while the reading was 1,213, that $300 clip would have been written down to roughly $0.50. **It has stopped: zero implausible events on every day from 2026-08-09 through 2026-08-14, six consecutive clean days**, the same date as the Instagram first stat recovery.

### Fabricated zeros

**None. Zero in the last 7 days.** Of 374 `clip_stats` rows written with `views = 0`, **0 had a positive prior stat** — that is the fabricated zero signature and it does not appear. 357 were a clip's genuine first stat and 17 followed another zero. The last fabricated zero event of any kind was **`2026-07-31`**: fourteen consecutive clean days. **BL-748 and BL-785 are both holding.**

The 13 legacy clips whose latest stored view count is 0 after a positive peak match BL-758 **field for field with zero drift**: 13 clips, all YouTube, all APPROVED, 5 clippers, **$0.00** of earnings, biggest ever peak 2 views.

### A finding I raised and then overturned, reported because the process matters

A subagent surfaced what looked like the round's most serious problem: **2,151 approved live clips carrying $6,445.48 have active tracking jobs 1 to 24 days overdue**, averaging 15.2 days since their last actual check, while daily clip coverage halved from ~1,438 to ~674. I verified all of it independently and it is arithmetically true.

**It is not a defect. It is the system working exactly as designed, and I checked the source rather than reasoning about it.** Every one of the five campaigns holding that $6,445.48 is **PAST and carries a `lastBudgetPauseAt`**: STRAENGE $1,997.56, somesome $1,967.14, bees.n.honey $1,534.26, Panic Baby $735.09, GainzAlgo REPOST $211.43. `campaignStatusBlocks` at **`tracking.ts:1939-1944`** blocks the earnings write for `status === "PAST"`, and the cadence logic at **`tracking.ts:293`** deliberately widens those clips to a 4320 minute interval, with a comment saying why: *"clips on AUTO paused campaigns can't accrue earnings (campaignStatusBlocks freezes the writer), so polling them every 48h was pure observability."*

**Overdue jobs on campaigns that can still earn: 0, carrying $0.00.** The coverage halving is explained better by bees.n.honey going PAST on 08-06 and Panic Baby on 08-07 than by the Instagram fix, and it matches the 08-07 and 08-08 coverage drop precisely. **No money is stale. Nothing needs building.**

---

## PART 5 — THE PARTNER REVIEWER ARRANGEMENT

**The scope the owner set is intact and behaving correctly.** Every field on the partner (`cmp9d0xu`) matches BL-802's snapshot: role REVIEWER, `reviewerMode` **TRIAL**, `reviewerScopeInvitedOnly` **true**, `canActAsClipper` false, capabilities empty, `reviewerCanSeeDecided` true, campaign scope still the single archived campaign, `referralCode` still **`VSHJYM4H`**, status ACTIVE. **No value has changed.**

**His queue behaves correctly, measured rather than asserted.** Reproducing in SQL the exact where clause `/api/clips` builds for him (`route.ts:83-88, 278-282, 307-313, 324-326, 360-391` plus `src/lib/reviewer-scope.ts`): the archived inclusive read returns **1,047 without the invitee scope and 0 with it**, reproducing BL-802's figure exactly. The default read returns 0 either way. **It fails closed** — `isClipperInReviewerInviteeScope` returns false for a clipper with a null `referredById`, and the filter is a `where` narrowing rather than a throw, so he gets **an empty list at HTTP 200, never an error**.

**He still reaches every clipper page.** Proven structurally today at the chokepoint, `src/lib/clipper-access.ts:54-57`, which BL-799 widened to `if (role === "CLIPPER" || role === "REVIEWER") return true`, so `canActAsClipper = false` is irrelevant for him. Verified gate by gate on `/api/clips/mine`, `/api/accounts/mine`, `/api/payouts/mine`, `/api/earnings`, `/api/referrals`, `/api/gamification` and the clip submission POST. **Two honest caveats.** `/api/campaigns` returns **an empty list at 200** rather than a populated one, because a REVIEWER needs the `CAMPAIGN_VIEW` capability and his array is empty — capability driven, not caused by the scope flag. And he can read the leaderboard but does not appear on it, which is deliberate and documented at `clipper-access.ts:47-51`. **BL-801's and BL-802's request based 200s are carried forward and explicitly not re-proven**, since this round made no authenticated request.

**His decisions remain recommendations, not final.** `src/app/api/clips/[id]/review/route.ts:233-302` branches TRIAL into a transaction creating a `proposedClipDecision` with `status: "PENDING"` and returns *"Queued for owner ratification (TRIAL mode). Clip status unchanged."* **No clip mutation on that path.** Measured: 10 proposals exist, **6 are his**, of which **1 is still PENDING**, 4 declined and 1 applied. His `reviewer_audit_log` shows 6 `PROPOSE_APPROVE` and **zero `APPROVE_CLIP` and zero `REJECT_CLIP` — he has never changed a clip status.**

**Has anyone joined through his link? No. Zero.** 0 users carry his id as `referredById`, 0 rows exist in `referral_clicks` for `VSHJYM4H`, and 0 referral commissions. His code is still on his row and still unique across all 1,415 users. **His queue will stay empty until the first clipper joins through that link**, which is the trade off the owner accepted.

**Recommendations awaiting the owner: exactly 1**, his, from `2026-07-27 21:25:45.522`. It targets clip `cms3i5tp`, **which is already APPROVED**, so ratifying it is moot and a reviewer re-decide would 400.

**The three LIVE reviewers the owner deliberately left alone are unchanged.**

| id8 | mode | invitedOnly | invitees | `updatedAt` (::text) |
|---|---|---|---|---|
| `cmoagb7e` | LIVE | false | 27 | 2026-08-14 09:42:30.167 (moved) |
| `cmovb0q6` | LIVE | false | 5 | 2026-08-03 13:01:44.615 (identical) |
| `cmpod0dh` | LIVE | false | 1 | 2026-08-02 08:52:24.264 (identical) |

Role, mode, invitedOnly and invitee count are **unchanged on all three**. The one moved stamp is **positively explained rather than left ambiguous**: `cmoagb7e`'s `lastPWAOpenAt` is `2026-08-14 09:42:29.662`, **half a second before** the new `updatedAt`. It is the PWA open write. His last `REVIEWER_CONFIG_UPDATED` is still 2026-07-14, `sessionVersion` still 16, capabilities unchanged. **No config change happened.**

**The position, restated so it is not forgotten: 27 reviewer rows, 1 scoped (the partner and only the partner), 26 unscoped.** Of the 27, **4 are real humans** and 23 are development seeds. **A correction to BL-802**, which recorded "13 live rows": that number is not reproducible under any definition tested — `isDeleted = false` gives 14, real cuid ids give 4, `reviewerMode = LIVE` gives 9, and 13 is exactly the count of **soft deleted seed rows**, which suggests an inverted filter. **The reproducible answer is 4 real reviewers.** Separately, BL-802's claim that the partner's `updatedAt` did not move when his flag was written is **not supported**: it now reads `2026-08-13 18:57:12.645`. No field value changed, only the stamp.

---

## PART 6 — WHAT IS WAITING ON THE OWNER

Every figure below was re-measured today, not carried from the report that first found it.

**1. The 70.8 day payout. `cmpq15k2` / `7b86e2`, $57.58 gross, $52.40 net, on bees.n.honey, UNDER_REVIEW since `2026-06-05 01:06:42.901`.** He has earned $59.11 and been paid **$0.00 in his lifetime**. It was 66.5 days at BL-758 and is now **70.8**. This is the oldest unresolved money item on the platform. **Do: pay it or reject it with a reason, today.**

**2. The 15:05 clipper. `cms4qr2d` / `d3a84c`, waiting 1.2 days.** His conversation still holds exactly **1 message**, written `2026-08-13 15:06:04.572`, and **nobody has replied**. His is the last message anyone ever sent through the chat, and the chat is now gone in production, so **no reply can ever reach him there**. He also has 1 clip pending since this morning. **Do: answer him on Discord today.**

**3. The 18 never answered people, of whom 7 asked for a person. Unchanged: 19 conversations, 17 distinct people, all CLIPPERs.** The 7 who escalated, by the structural `needsHumanSupport` flag rather than by text matching, and their current wait: `cmoaejuc` 112.9 days, `cmofpudr` 110.1, `cmpcip3n` 85.6, `cmpbl72e` 83.8, `cmpiiy8o` 79.3, `cmoyq9m9` 76.5, `cmp0zwli` 33.9. The longest wait of all is `cmn4nlfg` at **136.2 days** (not escalated). **Do: contact the 7 escalated first, off platform; the history is readable at `/admin/chat-archive`, which is live.**

**4. Three unread problem reports, all filed today, all from real clippers.** `2026-08-14 11:49:38.449`, `12:13:13.928` and `15:07:38.004`. **None has been read and none resolved.** All three are about **clip review latency** rather than a bug: one disputes a rejection reason, two ask why submissions are not being approved. Two of the three have since had their clips approved. A fourth row from `2026-08-13 17:39:07.061` is the owner's own test. **Do: read all four, answer the three clippers; the fix is faster review, not code.**

**5. Five PENDING clips older than 7 days**, out of 31 pending across 19 clippers. Oldest `2026-06-27 16:07:07.146` = **48.2 days**; then 45.6, 42.0, 31.2 and 9.1 days. The other 26 arrived in the last three days. **Do: clear the 5 stale ones — they are what the three new problem reports are about.**

**6. Six FLAGGED clips holding $113.50, frozen 37 to 77 days.** `cmpqrt6u` **$56.20** (77.2 days), `cmpu64wk` **$45.90** (75.0), `cmoso5zv` **$11.40** (74.4), all on bees.n.honey which is PAST; three more carry $0.00. **Do: approve or reject all six; nothing about them changes on its own.**

**7. The $60.47 case, unchanged to the cent since BL-716 and still the only clipper harmed by a proven code defect.** `cmqez5c2` / `dfb43b`: STRAENGE earned **$1,833.67** against **$1,894.14** paid, so his recorded earnings sit **$60.47 below money already sent**. Panic Baby earned **$460.11**, paid $0.00. Globally he has earned $2,293.78 and been paid $1,894.14, so **the gate offers him $399.64 while he should receive $460.11.** BL-758's four step procedure still applies and its order must not be varied: ask him to raise the request first for whatever the gate offers **at that moment**, pay $399.64 plus $60.47 against that single row, mark it PAID through the normal review path so `paidAt` is stamped, then strike the entry in `docs/OWED-MANUAL-PAYMENTS.md`. **Do not pay the $60.47 separately** — it would be invisible to every balance calculation and he could claim it again. He is one of 7 clippers overpaid per campaign, $143.41 total; the others need no action.

**8. Twenty seven clippers hold $2,206.13 they can withdraw right now and have not.** Up from BL-758's $1,137.43 across 8. The largest, with today's figures: `cmr0gixm` **$545.37** on Panic Baby (unchanged, and still the largest untouched position on the platform), `cmqez5c2` $399.64 on Panic Baby (see item 7), `cmrujf29` **$289.59** on Zhus Meme (was $105.05), `cmpqrt6u` $210.80 on bees.n.honey, `cmovgvov` $91.32, `cmq7qh6p` $73.23 on WinGram, `cmsiyg70` $59.66 on Zhus Edit, `cmqs7gjq` $51.91, `cmpq1awm` $51.60, `cmpq0od6` $51.37. **Do: message them. It costs nothing and it is the cheapest item on this list.**

**9. Six fresh REQUESTED payouts, $190.82 gross**, aged 0.1 to 5.7 days. **Do: clear them before one becomes the next 70 day row.**

**10. $874.56 that nobody can reach, across 133 clippers, and it has risen at every measurement.** $404.21 is earnings on videos that no longer exist, which under the owner's stated policy is not genuinely owed. **$470.35 is below the campaign minimum and every cent of it is genuinely owed**, spread across 142 (clipper, campaign) pairs and 115 clippers, of which **$311.48 (66 percent) is frozen forever** on PAST or archived campaigns where those clippers can never earn their way over the floor. The trend has never once gone down: 111 pairs / $324.33 (BL-728), 115 / $332.00 (BL-731), 118 / $338.20 (BL-734), 139 / $426.41 (BL-758), **142 / $471.11 today**. **Do: set a policy — a sweep payout, a lower floor on dead campaigns, or an explicit written forfeiture — because it grows every week.**

---

## PART 7 — THE VERDICT

> **The platform is sound and the money is correct: no money has been created from nothing, every standing property re-verified holds, the crons are alive, and the redeploy the owner was unsure about already happened.**

Nothing genuinely wrong was found in the money. What follows is ranked by what actually deserves the owner's attention, and **three of the five are people waiting rather than code**.

| # | what is wrong | severity | what it would take |
|---|---|---|---|
| 1 | **A real clipper has been waiting 70.8 days** on a $57.58 payout and has never been paid a dollar. Not a test user. | worst thing on the platform | one click |
| 2 | **`cmqez5c2` is still $60.47 short**, unchanged since BL-716, and it now sits under a $460.11 balance. The only clipper harmed by a proven defect. | real money, one person | BL-758's four step procedure, in order |
| 3 | **$470.35 owed below the campaign minimum, $311.48 of it frozen forever**, growing at every measurement. | real money, 115 people | an owner policy decision, then its own round |
| 4 | **Three unread problem reports and 18 unanswered people**, 7 of whom asked for a human, the oldest waiting 136 days. | reputational | messages, off platform |
| 5 | **`retire-dead-clips` writes no heartbeat row**, so a missed run is indistinguishable from a run that found nothing. | small, observability only | one `cron_runs` insert in that cron |

**What I checked and found genuinely fine, said plainly rather than dressed into findings.** The recompute from first principles: clean, zero clips over. No overpayment: holds, zero of 259. No campaign over budget: holds. The invariant: zero violations across 5,851 clips. Own stamp earning: zero unstamped clipper rates. The referral 5 percent after 1,039 codes: no double credit, and a UNIQUE database index makes one impossible. Crons: all four alive. Fabricated zeros: none in 14 days. Instagram first stats: recovered and holding at a 0 second median. The partner's scope: working exactly as built. The three LIVE reviewers: untouched. The money files: byte identical.

**The single most reassuring thing found this round, which no brief asked for.** The L1 budget hard lock is not a theory verified by reading code, it is **firing in production and logging every rejection**: 13 `BUDGET_HARDLOCK_THROW` rows, 8 of them refusing a write to a campaign already at its cap, the most recent on 2026-08-12, with the target clips demonstrably unchanged afterwards. The defence BL-627 reasoned about from the source is observable in the audit log doing its job.

**Two prior rounds correctly recommended against building things, and this is a third.** The largest apparent finding of this round, $6,445.48 of earnings on clips with badly overdue tracking jobs, is the tracking cron **correctly declining to spend money polling clips that cannot earn another cent**, on five campaigns that are all PAST with a budget pause. Overdue jobs on campaigns that can still earn: **zero**. The 20 clippers without a referral code, which looked like a growing gap, is **lazy minting that self heals on first visit to the referrals page**. Neither needs anything built. **The one thing I would build is the smallest item on the list: a heartbeat row for `retire-dead-clips`.**

---

## WHAT COULD NOT BE MEASURED, AND WHY

Stated plainly, because a gap presented as a result is worse than a gap.

**Whether `/admin/chat-archive` is genuinely owner only.** Its 200 is the pre hydration splash shell and contains no archive data. Testing the guard needs a signed in session against production, which is impersonation of a live account and outside a read only audit. **Not done, nothing claimed.**

**The exact commit hash Railway believes it is serving.** Outside evidence gives the build time and the build contents, both of which point unambiguously at `3a1b6a34`. The hash itself is a dashboard reading: Railway, service `web`, Deployments.

**Whether the report entry is unobstructed at 320 pixels in a real viewport.** The markup and the compiled CSS prove there is no width gate. Whether something overlaps it needs an authenticated browser at that width. **Three clippers filed reports at 360 to 363 pixels today, which is production evidence at close to that width but not at 320 itself.**

**Whether `retire-dead-clips` ran on 2026-08-04 and 2026-08-07.** Both days show zero retirements, and with no heartbeat row a run that found nothing is indistinguishable from a run that did not happen.

**The $101.74 of owner side agency earnings sitting above a live rate recompute** on 265 unstamped clips. The live `ownerCpm` may have moved since those rows were written, so it is **unverifiable by construction** and I will not call it either way. No clipper is affected.

**Per tick attribution of the $1,883.92 under credit.** There is no pool cap audit trail, so it can be attributed to budget exhausted campaigns (99.95 percent) but not decomposed tick by tick.

**Whether any hand payment has been made outside the platform.** By definition it leaves no trace, which is BL-696's standing gap. No evidence of one was found, and no evidence is not the same as none happened.

---

## VERIFICATION AND SAFETY

READ ONLY throughout, including all seven subagents, none of which held a write tool on the database. **No code, data, schema, config or money change. Nobody paid. No payout created, altered, approved, cancelled or paid. No balance touched, nothing restamped, nothing retired, nothing deployed.** `agency-monitor --fix` never run. No platform wide owner re-derive. No Apify actor, no paid probe, **$0.00 spend**. No authenticated request was made against production and no account was signed into. Every database read through `scripts/run-select.js`, which refuses every write keyword. Every timestamp cast `::text` against DB `now()`. Counting done with `grep -c` and **never piped through `head`**. No heredocs were used; SQL was passed directly or written with the file tool. **No build was run and none is claimed:** this round changed no TypeScript, so tsc and `npm run build` would prove nothing about it.

**Six subagent contradictions were found and resolved rather than averaged or dropped.**

**One.** `minPayoutAmountDecimal` was reported NULL on every campaign; **three campaigns carry a non default minimum** (Zhus Edit $20, Zhus Meme $20, SomeSome App $15). I recomputed reachable both ways, proving a flat $10 floor would overstate it by $71.37 across 5 clippers, and that the reported arithmetic had in fact used the correct floors. **The figure stood; the sentence did not.**

**Two.** Overpaid clippers were reported as both 4 / $82.12 and 7 / $143.41. **Both are correct**, for global and per campaign respectively, and $82.12 plus $61.29 equals $143.41 exactly.

**Three.** Withdrawable was reported as both $2,206.13 and $2,266.57. The difference is **exactly $60.47**, `cmqez5c2`'s global clamp, and the clamped figure is the one the gate will honour.

**Four.** $6,445.48 was raised as stale tracking money needing action; **it is frozen by campaign status, not by stale tracking**, and the source at `tracking.ts:1939-1944` and `:293` says so explicitly. Overdue jobs on campaigns that can still earn: zero.

**Five, and the most consequential.** Panic Baby's `spent` reading of **$3,000.25** was raised as $0.25 landing on a campaign already at its cap, the one movement with no sanctioned cause. **It is the opposite.** Those rows are `BUDGET_HARDLOCK_THROW` events in which the L1 chokepoint **rejected** the write, and the three target clips still carry $0.78, $0.00 and $0.00. The `spent` drift is BL-642's unfiltered agency aggregate. **Had this gone into the report unchecked it would have told the owner money leaked onto a capped campaign, which is false.**

**Six.** The 20 clippers without a referral code were called a live gap where nothing back fills them; **`src/lib/referrals.ts:16` mints lazily on first visit to the referrals page**, so it self heals.

Two further figures diverged on definition rather than fact and I used the stricter form in both cases: approved clips read 4,745 filtering `isDeleted = false` against 4,753 unfiltered, and the below minimum population read $470.35 on the gate's own arithmetic against a $523.77 reconstruction whose definition did not reproduce.

**Three corrections to earlier reports, made because they would otherwise be carried forward.** BL-806 described the single `problem_reports` row as a real user's report; it belongs to an **OWNER** account. BL-802 recorded "13 live reviewer rows"; that number is not reproducible and the answer is **4 real humans**. BL-802 stated the partner's `updatedAt` did not move when his flag was written; **it now reads `2026-08-13 18:57:12.645`**, though no field value changed.

Handles redacted throughout, no wallet address selected or printed, no report body quoted. **The worktree `C:/w807` was removed.**

**Nothing was changed. 5,851 clips, 169 payout rows, 34 campaigns, 1,415 users and $12,551.91 of recorded earnings are exactly as they were found.**
