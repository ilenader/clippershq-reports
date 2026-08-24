# BL-823 — the clipper's hand count was right, and applying the owner's rule owes 7 people $121.28

**2026-08-24 · DB `now()` = `2026-08-24 14:05:44.976167+00` (first read) to `14:12:31.756459+00` (last) · AUDIT ONLY. READ ONLY.**
No code, data, schema, config or money changed. Nobody paid, nothing restored, no status touched, no balance moved, no payout created, altered, approved or cancelled. **`agency-monitor --fix` was never run** and no repair SQL was executed. Every database access through `scripts/run-select.js`, which refuses a write keyword before it connects. Every timestamp cast `::text` against DB `now()`. Base `origin/main` @ `4ea1c139`, isolated worktree `C:/w823`, a short path, `node_modules` never junctioned, removed at the end. **No Apify actor and no paid probe: spend for this round is $0.00.**

Clippers appear as an 8 character id prefix plus `substr(md5(userId),1,6)`, the two forms every prior round used, so the owner can map them privately in admin. No handle and no wallet address appears anywhere.

> **HIS HAND COUNT IS THE MOST ACCURATE NUMBER ANYBODY HAS PRODUCED. He said about $92. Recomputed from his 262 approved clips, their views and each clip's own stamped CPM, his live payable earnings are $92.27 and every cent of it is unpaid.** The platform shows him $50.67 because it is deducting $41.59 he was paid in June and August for work on two finished campaigns.
>
> **Under the owner's rule he is owed $41.59 gross, $37.85 cash, taking him to $92.27 gross and $83.97 cash.**
>
> **Across the platform the rule owes 7 clippers $121.28 gross and $110.37 cash.** The largest is **$60.47** to `cmqez5c2`, which is BL-716's clipper, reproduced to the cent by a completely different derivation, and BL-760's *"pay $55.03, not $60.47"* is reproduced to the cent as well.
>
> **A CORRECTION TO MY OWN BL-822. Its "24 clippers, $274.12" is WRONG and overstated by $247.12.** The true figure is **5 clippers and $27.00**, and PART 3 shows exactly which line of arithmetic BL-822 omitted. Its per-clipper $8.60 for this clipper was right; only the platform total was not.

---

## PART 1 — SETTLING CLIPPER A, TO THE CENT

**Clipper A** = `cmpl310f` / `91a758`. Not referred, so the standard **9%** payout fee applies and not BL-812's reduced 4%; `feePercent = 9` is stored on both his payout rows.

### Computed from first principles, clip by clip

Nothing below is read from a stored total. `calculateClipperEarnings` (`earnings-calc.ts:112-212`) applied by hand in SQL, on **peak** views because earnings ratchet and never decrease:

```
peak_views < minViewsAtApproval                                    ->  0
base  = min(peak_views / 1000 x own stamped CPM, maxPayoutPerClipAtApproval)   cap on BASE only
bonus = base x own bonusPercent / 100
earned = round2(base) + round2(bonus)
```

Every one of his clips, grouped, at `db_now = 2026-08-24 14:05:44.976167+00`:

| campaign | status | video | why | clips | peak views | stored now | **entitlement from views and own CPM** | difference |
|---|---|---|---|---|---|---|---|---|
| **SomeSome App** ACTIVE | APPROVED | live | | **234** | 196,119 | **$92.26** | **$92.26** | **$0.00** |
| SomeSome App | APPROVED | retired | | 21 | 19,622 | $8.60 | $8.60 | **$0.00** |
| SomeSome App | PENDING | live | | 18 | 14,003 | $0.00 | *would be $5.68* | |
| SomeSome App | REJECTED | live | | 29 | 31,388 | $0.00 | *would be $12.70* | |
| SomeSome App | REJECTED | retired | | 8 | 6,749 | $0.00 | *would be $2.14* | |
| SomeSome App | REJECTED | retired | **video not found** | 9 | 6,136 | $0.00 | *would be $1.99* | |
| **somesome** PAST | **REJECTED** | retired | **video not found** | **15** | 41,698 | **$0.00** | **$28.57** | **$28.57 ERASED** |
| somesome | REJECTED | retired | | 4 | 3,487 | $0.00 | $1.87 | $1.87 ERASED |
| somesome | APPROVED | retired | | 7 | 3,363 | $0.00 | $0.00 | |
| **Panic Baby** PAST | **REJECTED** | retired | **video not found** | **8** | 33,660 | **$0.00** | **$16.39** | **$16.39 ERASED** |
| bees.n.honey PAST | REJECTED | retired | video not found | 1 | 1,456 | $0.00 | $0.73 | $0.73 ERASED |

**On his live campaign the recompute agrees with the record exactly: $92.26 against $92.26, a difference of $0.00 on 234 clips, and not one clip holds more than its own views and rate support.** By the last read at `14:12:09.161323+00` ordinary accrual had moved it to **$92.27** on 262 approved clips; the figures below use that clock and the drift is named rather than smoothed.

### His position, gross and cash

| | gross | cash |
|---|---|---|
| lifetime approved earnings, including retired | **$100.87** | |
| **payable approved earnings, all on the ACTIVE campaign** | **$92.27** | |
| excluded because the video is gone, and never paid for | $8.60 | |
| **paid to date** | **$41.59** | **$37.21** |
| locked in a pending request | $0.00 | $0.00 |
| **what the page displays as available** | **$50.67** | $46.11 |
| what the payout gate would allow today | **$59.27** | $53.94 |
| **what the owner's rule says he is owed** | **$92.27** | **$83.97** |

The two payouts, field by field, showing the cash:

| payout | campaign | gross | fee 9% | express 4% | **cash** | paid at (`::text`) |
|---|---|---|---|---|---|---|
| `cmq5jtla` | somesome | $25.54 | $2.30 | none | **$23.24** | `2026-06-24 16:09:02.602` |
| `cms8shrg` | Panic Baby | $16.05 | $1.44 | **$0.64** | **$13.97** | `2026-08-01 12:01:18.695` |
| | **total** | **$41.59** | | | **$37.21** | |

### Why his hand count reached about $92, and whose figure is closer

**He added up his SomeSome App clips. That total is $92.27. He is right, and the platform's $50.67 is the number that needs explaining.**

He did not include deleted-video earnings, he did not confuse gross with cash, and he did not make an arithmetic error. **He counted the campaign he is currently working on, found $92, and the platform showed him $50.67 because it silently subtracted $41.59 of payments made for work on two OTHER campaigns that are finished.**

The $8.60 clamp difference BL-822 found is real but is not the explanation either: it is a separate defect worth $8.60 and it is entirely inside the $41.59 (PART 4).

**And the $41.59 was paid for work that has since been erased from his record.** Both campaigns now read $0.00:

| campaign | paid | when paid | what happened to the clips | when | days after payment |
|---|---|---|---|---|---|
| somesome | $25.54 gross | `2026-06-24 16:09:02.602` | retired, then 15 **REJECTED, "Video not found"** | `2026-08-19 15:07:38.928` | **56** |
| Panic Baby | $16.05 gross | `2026-08-01 12:01:18.695` | retired, then 8 **REJECTED, "Video not found"** | `2026-08-19 15:07:47.111` | **18** |

**Those 23 clips recompute to $46.83 from their own views and stamped CPMs, and he was paid $41.59 against them.** The payments were fully covered by the work at the time. A bulk sweep on `2026-08-19` between `14:55:00.052` and `15:07:47.111` rejected them with the reason **"Video not found"**, which is a statement about the video and not about the work.

> **ONE LINE: under the owner's rule he should be able to withdraw $92.27 gross today, which is $83.97 in cash, and the $41.59 he was paid in June and August must stop being deducted from it.**

---

## PART 2 — APPLYING THE OWNER'S RULE ACROSS THE PLATFORM

**The rule, stated as arithmetic.** A payment can only ever consume the earnings of the campaign it was made against. It may never consume a different campaign's money:

```
paid_effective(campaign) = min(paid_gross(campaign), payable_earnings(campaign))
available_under_rule     = max( SIGMA payable - SIGMA paid_effective - SIGMA locked , 0 )
```

Today the platform uses `SIGMA paid_gross` with no per-campaign bound, which is `balance.ts:200` reading a single account-wide `paidOut` from `balance.ts:192-195`. That is BL-140's design and it is exactly what lets an erased campaign's payment reach a live campaign's balance.

### Every campaign whose payment its own earnings no longer cover

**20 clippers, 22 (clipper, campaign) pairs, $3,369.90 of payments now sitting beyond what their own campaign records.** The full list, redacted, ordered by size, all timestamps `::text`:

| id8 | md6 | campaign | payable now | paid gross | paid cash | marked unavailable | days paid to marking | rejected "not found" | days paid to rejection | **charged elsewhere** |
|---|---|---|---|---|---|---|---|---|---|---|
| `cmofpudr` | `2abe41` | somesome PAST | $108.38 | $1,607.33 | $1,543.04 | `2026-07-18 19:10:11.545056` | | 0 | | **$1,498.95** |
| `cmp7153e` | `3a8763` | somesome PAST | $0.00 | $1,313.86 | $1,349.66 | `2026-07-18 19:10:11.545056` | | 0 | | **$1,313.86** |
| `cmpl1dds` | `a0f203` | somesome PAST | $0.00 | $264.00 | $660.31 | `2026-07-18 19:10:11.545056` | **26** | 0 | | **$264.00** |
| `cmqez5c2` | `dfb43b` | STRAENGE PAST | $1,833.67 | $1,894.14 | $1,647.90 | none | | 0 | | **$60.47** |
| `cmr1rz2j` | `57560a` | GainzAlgo PAST | $0.00 | $31.75 | $28.45 | `2026-07-18 19:10:11.545056` | **9** | 0 | | **$31.75** |
| `cmpfozzs` | `540fef` | GainzAlgo PAST | $0.00 | $26.54 | $23.52 | `2026-07-18 19:10:11.545056` | **15** | 0 | | **$26.54** |
| **`cmpl310f`** | **`91a758`** | **somesome PAST** | **$0.00** | **$25.54** | **$23.24** | `2026-07-18 19:10:11.545056` | **24** | **15** | **56** | **$25.54** |
| `cmoaejuc` | `f95b37` | somesome PAST | $38.80 | $61.89 | $56.32 | none | | 0 | | **$23.09** |
| `cmrng806` | `a0f7fd` | Panic Baby PAST | $57.65 | $76.83 | $66.85 | `2026-08-13 06:02:13.687` | **5** | 0 | | **$19.18** |
| `cmp7ic4p` | `aaebb6` | somesome PAST | $0.00 | $17.00 | $33.67 | `2026-07-20 06:00:36.924` | | 0 | | **$17.00** |
| **`cmpl310f`** | **`91a758`** | **Panic Baby PAST** | **$0.00** | **$16.05** | **$13.97** | `2026-08-03 06:01:09.486` | **2** | **8** | **18** | **$16.05** |
| `cmq0qn2l` | `fa0da6` | GainzAlgo PAST | $0.00 | $14.46 | $13.16 | `2026-07-18 19:09:41.778551` | | 0 | | **$14.46** |
| `cmoal818` | `7ef3f3` | somesome PAST | $0.00 | $12.76 | $11.61 | `2026-07-18 19:10:11.545056` | | 0 | | **$12.76** |
| `cmpfozzs` | `540fef` | bees.n.honey PAST | $21.18 | $33.44 | $30.00 | `2026-08-10 06:01:03.657` | **7** | 0 | | **$12.26** |
| `cmr1bsip` | `17c12d` | bees.n.honey PAST | $0.00 | $10.17 | $8.84 | `2026-08-05 06:00:33.003` | **2** | 0 | | **$10.17** |
| `cmp71p89` | `9d81d0` | somesome PAST | $25.55 | $34.79 | $31.66 | `2026-07-24 06:00:02.88` | | 0 | | **$9.24** |
| `cmqv7svp` | `4e6238` | bees.n.honey PAST | $99.01 | $104.62 | $94.80 | `2026-08-13 06:04:05.677` | **10** | 0 | | **$5.61** |
| `cmosj3qk` | `99635c` | Panic Baby PAST | $109.97 | $114.16 | $103.38 | `2026-07-31 06:00:23.497` | **-3** | 0 | | **$4.19** |
| `cmp75zkf` | `70aa2a` | GainzAlgo PAST | $7.45 | $10.31 | $9.38 | `2026-07-18 19:10:11.545056` | | 0 | | **$2.86** |
| `cmpmuwfh` | `a38822` | somesome PAST | $19.65 | $20.61 | $18.76 | `2026-08-18 06:03:38.12` | **60** | 0 | | **$0.96** |
| `cmosmyqk` | `bc64d4` | somesome PAST | $992.42 | $993.36 | $903.96 | `2026-07-18 19:10:11.545056` | | 0 | | **$0.94** |
| `cmqmnvgs` | `f9cf0b` | WinGram PAUSED | $11.21 | $11.23 | $9.77 | `2026-07-23 06:00:59.294` | **6** | 0 | | **$0.02** |
| | | | | | | | | | **TOTAL** | **$3,369.90** |

**One row deserves naming:** `cmosj3qk` shows **-3 days**, meaning that campaign's last retirement PRECEDED his payment. That is the one case in the table where the deletion was already known when the money went out, so the owner's rule does not obviously apply to it; it is left in the table and excluded from the settlement below by the arithmetic rather than by hand, because he has no balance the offset can reach.

### What the rule actually returns

**A shortfall only becomes a real deduction if the clipper has other earnings for it to be taken from.** Most of the 20 do not: they are already floored at $0.00 and returning the offset changes nothing they can spend today, though it would matter the moment they earn again.

**Applying the rule: 7 clippers, $121.28 gross, $110.37 cash.** (The eighth candidate, `cmrng806`, drops out once the per-campaign floor the gate applies is included, see PART 4.)

| id8 | md6 | withdrawable today | **owed under the rule** | withdrawable after | **owed cash** |
|---|---|---|---|---|---|
| `cmqez5c2` | `dfb43b` | $0.00 | **$60.47** | $60.47 | **$55.03** |
| **`cmpl310f`** | **`91a758`** | **$50.67** | **$41.59** | **$92.27** | **$37.85** |
| `cmpfozzs` | `540fef` | $0.00 | **$15.97** | $15.97 | **$14.53** |
| `cmp75zkf` | `70aa2a` | $4.13 | **$1.41** | $5.54 | **$1.28** |
| `cmosmyqk` | `bc64d4` | $0.52 | **$0.94** | $1.46 | **$0.86** |
| `cmp71p89` | `9d81d0` | $0.00 | **$0.88** | $0.88 | **$0.80** |
| `cmqmnvgs` | `f9cf0b` | $5.82 | **$0.02** | $5.84 | **$0.02** |
| | | | **$121.28** | | **$110.37** |

**`cmqez5c2`'s $60.47 is a cross-check worth stating.** BL-716 audited that clipper by hand, reconstructed a $2,000 pool clipper by clipper, and concluded he was owed **$60.47**. BL-760 then said **"pay $55.03, not $60.47"** because the gross carries the 9% fee. **This round reaches $60.47 gross and $55.03 cash from a completely different derivation, a per-campaign paid-effective cap applied platform-wide, with no knowledge of that pool.** Two independent methods, three weeks apart, identical to the cent.

### The exclusions that are CORRECT and must stay

Kept strictly separate, because the owner's rule removes only the offset and never the exclusion:

| | pairs | clippers | retired clips | money |
|---|---|---|---|---|
| **retired on a campaign the clipper was NEVER paid on** | **70** | **57** | **302** | **$387.77** |
| retired on a campaign the clipper WAS paid on | 32 | 27 | 489 | $3,250.79 |

**The $387.77 stays excluded and nobody is owed it.** Those are unpaid earnings on deleted videos, which is precisely the case the owner's rule says may be removed. Clipper A's own **$8.60** is in that bucket and stays out of his balance under the rule.

---

## PART 3 — THE CLAMP DEFECT, AND A CORRECTION TO BL-822

### BL-822's $274.12 was overstated. The true figure is $27.00.

**I wrote BL-822 and its platform total is wrong, so the correction goes here rather than in a footnote.**

BL-822 compared the two **global** clamp bases and stopped there:

```
gate global   = max(SIGMA lifetime - paid - locked, 0)      payouts/route.ts:666-668, no videoUnavailable filter
screen global = max(SIGMA payable  - paid - locked, 0)      earnings/route.ts:209, payableClips
gap           = gate global - screen global                <-- what BL-822 measured
```

**It omitted the line immediately below.** `payouts/route.ts:689` is `effectiveCap = Math.min(available, globalAvailable)`, and `available` is the **per-campaign** figure computed on the **payable** base at `payouts/route.ts:362` and `:524`. So a looser global base cannot release a cent unless the clipper still has per-campaign payable headroom to release it into.

Measured both ways, at `db_now = 2026-08-24 14:08:56.498458+00`:

| | clippers | total |
|---|---|---|
| BL-822's global-only comparison, re-run today | **34** | **$2,392.53** |
| **the same comparison with the per-campaign floor the gate actually applies** | **5** | **$27.00** |

**BL-822 reported 24 and $274.12; today the same flawed query returns 34 and a much larger number, which is itself evidence the metric was unstable.** The correct figure is **5 clippers and $27.00 gross, $24.57 cash**:

| id8 | md6 | screen offers | gate would allow | **short by gross** | short by cash |
|---|---|---|---|---|---|
| `cmpfozzs` | `540fef` | $0.00 | $15.97 | **$15.97** | $14.53 |
| **`cmpl310f`** | **`91a758`** | **$50.67** | **$59.27** | **$8.60** | **$7.83** |
| `cmp75zkf` | `70aa2a` | $4.13 | $5.54 | **$1.41** | $1.28 |
| `cmosmyqk` | `bc64d4` | $0.52 | $1.46 | **$0.94** | $0.86 |
| `cmp71p89` | `9d81d0` | $0.00 | $0.08 | **$0.08** | $0.07 |
| | | | | **$27.00** | **$24.57** |

**BL-822's per-clipper $8.60 for Clipper A was correct**, and remains correct; only its platform aggregate was wrong. The error direction was to overstate, which is the safer direction for a report and the wrong direction for a payment, and it is corrected here before anybody acts on it.

### Which base is correct

| | file:line | base |
|---|---|---|
| the gate's global clamp | **`payouts/route.ts:666-668`** | `status: "APPROVED"`, **deliberately NO `videoUnavailable` filter** |
| the display's global balance | **`earnings/route.ts:209-210`** | `payableClips`, filtered `!videoUnavailable`, into `computeBalance` at `balance.ts:200` |

**The GATE's lifetime base is correct, and its own comment says why**, at `payouts/route.ts:670-673`: *"a creator's 60% share was earned when the clip was live, and retiring the clip later must not retroactively un-earn money already paid against it."* **That is the owner's rule, already written into the code, on one side only.**

**The display is the side that drifted.** `payouts/route.ts:655-662` still asserts that the displayed balance uses the lifetime base. That was true when BL-692 wrote it and **BL-698 made it false**, and it has misled every reader since, including BL-765, which recorded the asymmetry and routed around it rather than closing it.

> **These 5 clippers can already withdraw more than their screen offers, and the only thing stopping them is the browser.** `payouts/page.tsx:289` returns *"Amount exceeds available balance"* and `PayoutRequestFlow.tsx:331` returns *"That is more than your $X available"*, both comparing against the display figure. The server would accept the larger amount and never gets asked. **This is a straight defect, not a policy question.**

---

## PART 4 — THE OVERLAP, AND ONE COMBINED LIST

**They overlap almost entirely, and the direction matters: the clamp defect is fully SUBSUMED by the owner's rule.** Every dollar the clamp fix would release is also released by paid-is-final, so applying both returns exactly what applying the rule alone returns.

Computed four ways per clipper, each summing `min(per-campaign available, global base)` across their campaigns so no per-campaign floor is ignored:

| id8 | md6 | today | from paid-is-final | from the clamp defect | **combined, no double count** | overlap removed | after both |
|---|---|---|---|---|---|---|---|
| `cmqez5c2` | `dfb43b` | $0.00 | $60.47 | $0.00 | **$60.47** | $0.00 | $60.47 |
| **`cmpl310f`** | **`91a758`** | **$50.67** | **$41.59** | **$8.60** | **$41.59** | **$8.60** | **$92.27** |
| `cmpfozzs` | `540fef` | $0.00 | $15.97 | $15.97 | **$15.97** | $15.97 | $15.97 |
| `cmp75zkf` | `70aa2a` | $4.13 | $1.41 | $1.41 | **$1.41** | $1.41 | $5.54 |
| `cmosmyqk` | `bc64d4` | $0.52 | $0.94 | $0.94 | **$0.94** | $0.94 | $1.46 |
| `cmp71p89` | `9d81d0` | $0.00 | $0.88 | $0.08 | **$0.88** | $0.08 | $0.88 |
| `cmqmnvgs` | `f9cf0b` | $5.82 | $0.02 | $0.00 | **$0.02** | $0.00 | $5.84 |
| **7 clippers** | | | **$121.28** | **$27.00** | **$121.28** | **$27.00** | |

**The totals reconcile exactly.** The overlap column sums to **$27.00**, which is PART 3's total to the cent, and `121.28 + 27.00 − 27.00 = 121.28`. **Adding the two causes naively would have claimed $148.28 and overpaid by $27.00.**

> **THE PLATFORM TOTAL: $121.28 gross, $110.37 cash, to 7 clippers.**

**`cmrng806` is the row that proves the method.** He appears in PART 2 with a $19.18 shortfall on Panic Baby, and he is absent from this list, because his per-campaign payable headroom is already fully released and a looser global base gives him nothing. Counting him would have been a $19.18 error.

---

## PART 5 — WHAT MUST NOT BREAK

### Could returning this let anyone withdraw more than they genuinely earned? No.

**Not measured against the record, which is the thing that was erased, but against what each clipper's own clips, views and stamped rates actually generated:**

| id8 | md6 | recorded now | **true entitlement from views and own CPM** | paid gross | would be returned | total received | **headroom** | verdict |
|---|---|---|---|---|---|---|---|---|
| `cmqez5c2` | `dfb43b` | $2,293.78 | **$2,964.15** | $2,293.78 | $60.47 | $2,354.25 | **$609.90** | **WITHIN** |
| **`cmpl310f`** | **`91a758`** | $100.87 | **$170.94** | $41.59 | $41.59 | $83.18 | **$87.76** | **WITHIN** |
| `cmpfozzs` | `540fef` | $103.34 | **$105.12** | $59.98 | $15.97 | $75.95 | **$29.17** | **WITHIN** |
| `cmp75zkf` | `70aa2a` | $23.56 | **$26.49** | $10.31 | $1.41 | $11.72 | **$14.77** | **WITHIN** |
| `cmosmyqk` | `bc64d4` | $994.82 | **$1,139.34** | $993.36 | $0.94 | $994.30 | **$145.04** | **WITHIN** |
| `cmp71p89` | `9d81d0` | $56.77 | **$162.59** | $56.69 | $0.88 | $57.57 | **$105.02** | **WITHIN** |
| `cmqmnvgs` | `f9cf0b` | $17.05 | **$30.42** | $11.23 | $0.02 | $11.25 | **$19.17** | **WITHIN** |

**Not one of the seven would receive more than their own work supports, and the smallest headroom is $14.77.** BL-627's no-overpayment property survives.

**The assumption inside that, named rather than buried:** the entitlement column counts every clip including those later rejected. That is the right basis **because the rejections in question are "Video not found"**, a statement about the video and not about the work, and because those clips were APPROVED and earning at the moment the payment was made. **If any of these clips had been rejected for quality, the payment would have been wrong when it was made, and the owner's rule explicitly does not cover that case.** I checked Clipper A's: all 23 carry "Video not found". I did not read all 489 rejection reasons across the wider population, and that is named as a limit.

### Could anyone be paid twice? No, and it is structural.

BL-696 proved `available = max(earned − paidOut − locked, 0)` and that the already-paid amount **stays subtracted forever**. Every repair shape in PART 6 works by raising the **earned** side, never by reducing `paidOut`, so:

* the $41.59 Clipper A already received **remains subtracted from every future read**, and raising his floor by $41.59 gives him the new money once and never the old money again;
* the database-level partial unique index `uq_payout_open_per_user_campaign` is untouched, so at most one open payout per clipper per campaign still holds;
* nothing in either spec creates a payout row, and `grep -c "payoutRequest.create" src/app/api/admin/` still returns **0**, so there is still no admin creation path to abuse.

### Does anyone's record sit BELOW money already paid? Yes. 4 clippers, $82.12.

This is BL-716's defect, still live, and it is exactly what the owner's rule exists to prevent:

| id8 | md6 | recorded lifetime | paid gross | **recorded below paid by** | available | in the seven? |
|---|---|---|---|---|---|---|
| `cmofpudr` | `2abe41` | $1,570.58 | $1,607.33 | **$36.75** | $0.00 | **no** |
| `cmoaejuc` | `f95b37` | $38.80 | $61.89 | **$23.09** | $0.00 | **no** |
| `cmq0qn2l` | `fa0da6` | $0.00 | $14.46 | **$14.46** | $0.00 | **no** |
| `cmoal818` | `7ef3f3` | $4.94 | $12.76 | **$7.82** | $0.00 | **no** |
| **4 clippers** | | | | **$82.12** | | |

**This reproduces BL-758's figure to the cent, fourteen days later**, and BL-627 measured the same population at 5 clippers and $142.59 in July, so it is shrinking rather than growing.

**None of the four is in the seven, and that is the correct outcome rather than an oversight.** All four sit at $0.00 available and stay there: the owner's rule stops an old payment consuming NEW earnings, and these four have no new earnings for it to consume. **The rule does not create money and it does not claw any back from them.** The moment any of them earns again, the rule protects them automatically.

---

## PART 6 — THE VERDICT AND THE TWO SPECS

> **ONE LINE: $121.28 gross and $110.37 cash is owed to 7 clippers, of which $41.59 gross and $37.85 cash is owed to the clipper who wrote in, taking him to the $92 he counted by hand.**

### SPEC A — the CODE fix. NOT PERFORMED.

**A1. Paid work must never offset future earnings.** The offset happens because `computeBalance` subtracts one account-wide `paidOut` with no per-campaign bound.

| # | site | file:line | change |
|---|---|---|---|
| A1a | the balance | **`balance.ts:192-195`** and **`:200`** | `paidOut` becomes `SIGMA min(paid(campaign), payable(campaign))`. `computeCampaignBalances` at `:206-252` already groups by campaign, so both bases exist in the same function. **This is a MONEY FILE and the change must carry its own proof.** |
| A1b | the gate | **`payouts/route.ts:679-689`** | the same cap on `globalPaid`, or the gate and the display disagree again in the other direction. |
| A1c | the durable form | new nullable `PayoutRequest.earnedAtPaymentSnapshot` | **BL-716 specified exactly this** and it is the better shape: stamp what the clipper had earned at the moment of payment, then floor the earned side at `max(lifetimeEarned, SIGMA earnedAtPayment)`. It survives a campaign being deleted, which the per-campaign cap does not. Additive and nullable, applied with `run-schema-sql.js`, **never `prisma migrate`**. |

**A2. The gate and the display must agree on one base.** PART 3. **Adopt the gate's lifetime base**, because `payouts/route.ts:670-673` already states the owner's rule in its own comment, and correct the stale comment at `:655-662` that BL-698 falsified. `payouts/page.tsx:289` and `PayoutRequestFlow.tsx:331` must read the same number or the client keeps refusing what the server would allow.

**What must be proven before either ships:** every clipper's available recomputed before and after, with the 7 rising by exactly the amounts in PART 4 and **every other clipper unchanged to the cent**; the 4 clippers in PART 5 still computing $0.00; no clipper's paid-plus-available exceeding their true entitlement from views and stamped CPMs; the earnings invariant at 0; and `uq_payout_open_per_user_campaign` still present in `pg_indexes`. **Rollback:** A1a and A1b are single-file and revert with the commit; A1c's column is additive and goes unread if the code is reverted.

### SPEC B — the DATA repair. NOT PERFORMED, and it may not be needed at all.

**The honest recommendation: ship A and no data repair is required.** Balances are **derived on every read** (`balance.ts:200`, and BL-696 says so explicitly: *"There is no snapshot to go stale"*). So the moment A deploys, all 7 balances rise on their own and **no row has to be written.** That is the safest possible repair, because it writes nothing.

**If the owner wants the money out before A can ship**, the manual route, with its risks named:

1. **Do NOT pay by hand.** BL-763 refused exactly this and its reason applies here: the money is still claimable in their balances, so a hand payment would sit beside a live claim and could be requested a second time. **BL-696's PART 5 is blunt that no admin path records a manual payment**, so nothing would stop the double request.
2. **The only safe manual shape is to let them request through the platform once A is live**, and pay against that row.
3. **If a row must be written anyway:** snapshot `SELECT id, earnings, "baseEarnings", "bonusAmount" FROM clips WHERE "userId" = ...` for all 7 first, print the exact rollback `UPDATE` beside it, write through `writeClipEarnings` and never a direct update (it is the L1 budget hard-lock and the invariant chokepoint), keep **BL-538's never-decrease guard ON**, and write **no payout row**.
4. **Double counting is avoided by construction** if and only if the amounts used are PART 4's combined column and not PART 2's and PART 3's added together, which would overpay by **$27.00**.

**What must be proven either way:** the 7 balances land on the PART 4 "after both" figures exactly; no eighth clipper moves; `paidOut` is unchanged for everybody, so BL-696's no-double-pay still holds; and the invariant is 0 before and after.

### The reply the owner can send this clipper

> Hey, thanks for adding it up and sending it over. **You are right, and your number is better than ours.**
>
> You have earned **$92.27** on SomeSome App. I checked all 262 of your approved clips against their own views and their own rate, and your total is correct.
>
> The reason the app showed you about $50 is our mistake, not yours. **We were subtracting $41.59 that we already paid you** back in June and on the 1st of August, for clips on two older campaigns. Those clips were later marked as "video not found" and removed from your record, but **you had already been paid for them, and that money is yours.** It should never have been taken back out of what you are earning now.
>
> **The rule from now on is simple: once we have paid you, that is final. A video disappearing later never touches money already in your wallet.**
>
> So **you are owed $41.59 more than the screen shows**, which is **$37.85** after the 9% fee. That takes you to **$92.27**, or about **$83.97** in cash.
>
> I am fixing the app so this stops happening to anyone. In the meantime tell me how you want the difference and I will sort it out.
>
> One small thing so the numbers make sense to you: where the page says **"paid out, before fees $41.59"**, what actually reached you was **$37.21**, after the 9% fee and a 4% express fee on the August one because you chose express.

### The short reply for the other six

> Hey, quick one and it is good news. We found a mistake in how your balance was worked out.
>
> When a video disappears after we have already paid you for it, we were quietly taking that money back out of what you earn afterwards. **That is not right, and money we have already paid you is yours to keep.**
>
> Your balance is going up by **$X**, which is **$Y** after the payout fee. Nothing you did caused this and there is nothing you need to do. It will show on your earnings page once the fix is live.

Both state a fact and a correction, neither implies the clipper did anything wrong, and neither invites a request that would fail. BL-518 and BL-521.

---

## WHAT COULD NOT BE MEASURED

* **What each campaign's earnings were at the exact moment of payment.** Earnings are overwritten in place, the platform stores no earnings history, and `savedEarnings` is null or zero on the rows that matter. Every "what it was worth" figure here is a reconstruction from peak views and stamped CPMs, and it is a **lower bound**: it cannot be higher than the clipper's true entitlement, so it can only understate what is owed. **BL-716 asked for an earnings history row three weeks ago and its absence cost this round the same question again.**
* **Whether all 489 erased clips across the wider population were rejected for "video not found" rather than for quality.** Clipper A's 23 were checked individually. The rest were not, and the distinction decides whether the payment was correct when it was made. **The repair must not ship without that check on the 7.**
* **The `cmosj3qk` row with -3 days**, where the retirement preceded the payment. It falls out of the settlement by arithmetic rather than by judgement, and if the owner ever revisits it, it is the one row in PART 2 the rule may not cover.
* **Whether the 12 clippers in PART 2 who gain nothing today would gain later.** They would, automatically, the moment they earn again, but no figure can be put on it now.
* **No browser render was performed and no build was run.** This round changed one markdown file in the reports repository and cannot affect `tsc` or `next build`.

---

## ACCESSIBILITY

**No UI code was written or edited.** This is an audit and its only artefact is this document, so there is no component, markup or user-facing string to review. The unexplaining-display defect BL-822 named is unchanged and is not re-litigated here.

---

## VERIFICATION

Read only throughout: no code, data, schema, config or money changed, nobody paid, nothing restored, no status or balance touched, **`agency-monitor --fix` never run**, no repair SQL executed, and every read through `scripts/run-select.js`. Clipper A is settled from first principles clip by clip with the working shown, his live payable earnings recomputed from views and each clip's own stamped CPM at **$92.26 against $92.26 stored, a difference of $0.00 on 234 clips**, and every figure stated as **both gross and cash**: earned $100.87, paid $41.59 gross and $37.21 cash, displayed $50.67, gate-allowable $59.27, owed under the rule **$92.27 gross and $83.97 cash**. His hand count is explained precisely and **named as more accurate than the platform's figure**. The owner's rule is applied platform-wide, listing all 22 pairs across 20 clippers holding $3,369.90 of payments beyond their own campaign with every timestamp cast `::text` and the days between payment and marking stated, kept strictly separate from the **$387.77 across 57 clippers whose deleted clips were never paid for and whose exclusion is correct**. BL-822's "24 clippers, $274.12" is **corrected to 5 clippers and $27.00**, with the omitted line of arithmetic named at `payouts/route.ts:689` and both bases given at file:line, and the gate's lifetime base identified as correct on the strength of its own comment. One combined list of **7 clippers** removes an overlap that reconciles to **$27.00** exactly, giving a platform total of **$121.28 gross and $110.37 cash**, and the method is shown to work by the row it correctly excludes. BL-627's no-overpayment property is proven to survive against **true entitlement recomputed from views and stamped CPMs**, with the smallest headroom $14.77, and BL-696's no-double-pay is proven structurally because every repair shape raises the earned side and never reduces `paidOut`. The 4 clippers whose record sits below money already paid are named at **$82.12**, reproducing BL-758 to the cent, and **none of them is in the seven**. Two specs are given with file:line, proofs, rollback and an explicit warning that adding the two causes would overpay by $27.00, and **neither was performed**; the recommended repair writes nothing at all, because balances are derived on every read. Both replies are plain and non-accusatory. The earnings invariant is **0 violations**, payout rows **190** with the newest `updatedAt` at `2026-08-24 05:08:22.794`, nine hours before this round's first read. Handles redacted, no wallet address printed, spend **$0.00**, no Apify actor. The worktree at `C:/w823` is removed. **No dashes as bullets.**
