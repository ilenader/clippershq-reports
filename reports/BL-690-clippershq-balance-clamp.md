# BL-690 — the balance clamp asymmetry: what is actually owed, and the correct fix

## TWO CLIPPERS ARE OWED $38.26, NOT THREE OWED $52.86. BL-688 was right about the mechanism and wrong about one of the three people: C-3's $14.65 is not owed to him at all, because he has been paid $1,894.14 against $1,848.32 of lifetime earnings and is the single most overpaid clipper on the platform at $45.82. The clamp blocking him is the clamp doing exactly the job BL-627 requires of it. The other two are genuinely owed, and their money is the good case: it sits on ACTIVE campaigns where their clips are still live and still counted in the budget, so paying them releases money the campaign already reserves and creates no new spend at all. That is the opposite of BL-657's answer for the $390.60.

**2026-07-30 · AUDIT ONLY. READ ONLY on code, data and money. No payout was created, modified, approved or cancelled. No balance was touched. The env kill switch was NOT flipped. Nothing was fixed.**
**Base** origin/main `765bb0e4` (`post-merge-BL-687`) · **Branch** `checkpoint/BL-690` · **Worktree** `C:/b690` (short path, node_modules never junctioned) · **DB `now()` at final query: 2026-07-30 19:26:27.663773+00**

**Redaction.** The reports repo is PUBLIC. Clippers appear as **C-1**, **C-2**, **C-3** with an 8-character id prefix and, where they also appear in BL-661, that report's `substr(md5(userId),1,6)` short id so the owner can reconcile the two tables privately. No handle, email or wallet address appears anywhere, not even partially.

---

## PART 0 — the asymmetry, in plain English

Think of a clipper's balance as a simple subtraction the platform does every time he asks to withdraw:

> **what he has earned, minus what he has already been paid**

The bug is that the platform changed its mind about the first number and not the second.

Follow C-1, with his real figures:

1. He posted clips and earned money on them. Over his lifetime, **$41.28**.
2. In June he withdrew **$25.54** of it. That payment was correct and he received it.
3. On **2026-07-18 19:10:11**, an automated cleanup checked his videos and found **21 of them had been deleted from Instagram**. It stamped them "video unavailable". Those 21 clips carried exactly the **$25.54** he had already been paid for.
4. Since then he has kept clipping on a different campaign and earned a further **$15.74**, on 8 clips that are all still live and playing right now.

Now the subtraction. When he asks to withdraw:

* The "what he has earned" side **stops counting deleted videos**. So it sees only the **$15.74** still live.
* The "what he has been paid" side **counts everything he was ever paid**. So it still sees the full **$25.54**.

**$15.74 minus $25.54 is negative, so the platform floors it at $0.00 and tells him he has nothing.**

The money he was paid for the deleted clips is subtracted twice over, in effect: once when he received it, and again when the earnings that justified it were removed from his total. He is charged for a payment whose matching earnings the platform has quietly stopped counting, and the $15.74 of brand-new work on a completely different campaign gets swallowed paying off a debt that was already settled.

**Both of the platform's own rules look at this and disagree.** The per-campaign rule, applied to the campaign where his live work is, says **$15.74 is available**. The global clamp says **$0.00**. He is shown one number and enforced against the other, and told neither.

---

## PART 1 — the exact population

### The three from BL-688, re-examined

| | **C-1** `cmpl310f` (the reporter) | **C-2** `cmpfozzs` | **C-3** `cmqez5c2` |
| --- | --- | --- | --- |
| BL-661 short id | `91a758` | `540fef` | not in that population |
| lifetime earned, including retired clips | **$41.28** | **$65.39** | **$1,848.32** |
| lifetime paid | $25.54 | $37.28 | **$1,894.14** |
| **earned minus paid** | **+$15.74 owed** | **+$28.11 owed** | **−$45.82 OVERPAID** |
| earnings on retired clips | $25.54 across 21 clips | $32.13 across 57 clips | **none, zero retired clips** |
| when retired (`::text`) | 2026-07-18 19:10:11.545056 | 2026-07-18 19:09:41.778551 to 19:10:11.545056 | not applicable |
| campaign holding the live money | **Panic Baby, ACTIVE**, 8 live clips, $15.74, never paid from | **bees.n.honey, ACTIVE**, 52 live clips, $33.26, $10.74 paid | Panic Baby, ACTIVE, $14.65 |
| campaign holding the payout that triggers the clamp | somesome, **PAST** | GainzAlgo REPOST, **PAST** | STRAENGE, **PAST** |
| per-campaign rule says | **$15.74** | **$22.52** | $14.65 |
| global clamp says | $0.00 | $0.00 | $0.00 |
| can he withdraw anything at all today | **no** | **no** | no |
| **genuinely owed?** | **YES** | **YES** | **NO** |

### The correction, stated plainly

**C-3 is not a victim of the asymmetry. He has no retired clips whatsoever.** His global available is $0.00 for the ordinary reason that he was paid $45.82 more than he has ever earned, on STRAENGE, where he earned $1,833.67 and was paid $1,894.14. He is the largest of BL-627's five over-held clippers, a group that today totals **$127.94** across five people (down from BL-627's $142.59, still shrinking, still unrecoverable by design).

**BL-688 grouped him with the other two and reported $52.86 owed. That was wrong, and this round corrects it. The correct figure is $38.26**, being C-1's $15.74 plus C-2's $22.52, both measured as what the per-campaign rule already says they may take.

### Overlap with BL-661's $390.60: partial, and the double-pay risk is real

Reproducing BL-661's exact `stuck` formula live today gives **26 clippers** (up from 24 on 2026-07-24).

| clipper | in BL-661's population today? | BL-661 `stuck` today | BL-690 amount owed |
| --- | --- | --- | --- |
| **C-1** | **YES**, as `91a758`, a new entrant since 2026-07-24 | $15.74 | $15.74 |
| **C-2** | **YES**, as `540fef`, was $20.27 in BL-661, now $28.11 | $28.11 | $22.52 |
| **C-3** | **NO** | not applicable | $0.00 |

**So the two genuinely owed clippers are a SUBSET of BL-661's population, not a disjoint group.** Their money is already inside the $390.60-and-growing figure the owner has been shown once.

**The owner could pay the same dollar twice, and here is exactly how.** BL-661 defines `stuck` as what the earnings page shows minus what the gate offers. A rule change that raises what the gate offers **shrinks the BL-661 figure by exactly the same amount**. If the owner pays BL-661's table as it is computed today AND ships the clamp fix, C-1 and C-2 receive their money once through each route. **The mitigation is simple and must not be skipped: recompute BL-661's table AFTER any clamp change, or subtract the delta from it before paying.**

---

## PART 2 — which side is right, and does paying create new spend?

### Was the earlier payment correct at the time? Yes, verified.

C-1's $25.54 was created 2026-06-08 18:32:55.063 and paid 2026-06-24 16:09:02.602. His clips were live and earning throughout. They were not retired until **2026-07-18 19:10:11.545056**, twenty-four days after the money left. **Nothing about that payment was wrong then and nothing about it is wrong now.** The same holds for C-2's three payments (2026-06-17, 2026-07-01, 2026-07-12), all predating the same 2026-07-18 sweep.

### Did they genuinely earn the additional money? Yes.

C-1's $15.74 sits on **8 clips on Panic Baby that are APPROVED, not deleted, and playing right now**. C-2's $22.52 sits on **52 live clips on bees.n.honey**. This is not retired money and not disputed money. It is ordinary current earnings on live work, and neither clipper has withdrawn a cent from the campaign holding it (C-1 has taken $0.00 from Panic Baby; C-2 has taken $10.74 of his $33.26 on bees.n.honey).

### Does paying release reserved money or create new spend? **It RELEASES reserved money. This is the clean case.**

This is where BL-690 differs sharply from BL-657, and the difference is decisive.

BL-657 asked whether paying the $390.60 of **retired** earnings creates new spend, and answered that it does: the instant a clip flips `videoUnavailable`, its earnings leave `getCampaignBudgetStatus.spent` and the campaign's pool room re-opens, so paying retired earnings spends against room the budget has already released.

**None of that applies here.** The $38.26 owed to C-1 and C-2 is on clips that are **live, approved and not retired**, so their earnings are **still counted in their campaigns' spend right now**. The budget has never released this room and still holds it against exactly these clips.

| campaign | status | whose money | still counted in `spent`? | paying it |
| --- | --- | --- | --- | --- |
| Panic Baby | **ACTIVE** | C-1's $15.74 on 8 live clips | **YES** | releases reserved money |
| bees.n.honey | **ACTIVE** | C-2's $22.52 on 52 live clips | **YES** | releases reserved money |

**Stated as plainly as BL-657 stated its answer: paying the $38.26 releases money that is already reserved. It creates no new spend, it re-opens no pool room, it cannot double-spend against any campaign, and it does not depend on those campaigns staying frozen, which matters because both of them are ACTIVE.** Payouts are not a term in `getCampaignBudgetStatus.spent` in any case, so no recorded spend moves and no L1 lock can trip.

---

## PART 3 — the options, priced with the full blast radius

### The measurement that decides this

I simulated every candidate rule against **the entire clipper population**, not just these three, comparing what each clipper can withdraw today against what they could withdraw after the change. The proposed rule replaces the clamp's earnings base with **lifetime earnings including retired clips**, which is the same base BL-627 uses to test for overpayment:

`globalAvailable = max(lifetimeEarnedInclRetired − moneyOut − locked, 0)`

**The complete platform-wide effect is five clippers and $40.69. Nobody else on the platform moves by a cent.**

| clipper | max withdrawable today | after | delta |
| --- | --- | --- | --- |
| **C-2** `cmpfozzs` | $0.00 | $22.52 | **+$22.52** |
| **C-1** `cmpl310f` | $0.00 | $15.74 | **+$15.74** |
| `cmp75zkf` (BL-661 `70aa2a`) | $2.68 | $4.09 | +$1.41 |
| `cmosmyqk` (BL-661 `bc64d4`) | $0.52 | $1.46 | +$0.94 |
| `cmp71p89` (BL-661 `9d81d0`) | $0.00 | $0.08 | +$0.08 |
| | | | **+$40.69 total** |

**C-3 does not appear, and that is the single most important line in this report.** His new global would be `max(1848.32 − 1894.14 − 0, 0) = $0.00`, unchanged. **BL-627's proof that an overpaid clipper cannot withdraw further survives the change exactly**, because the new base is the very quantity BL-627 measures overpayment against.

Note also what the change does **not** do: it does not release retired earnings. The per-campaign rule at `payouts/route.ts:411` still excludes `videoUnavailable`, so on a campaign whose clips are all retired the per-campaign available stays $0.00 and `effectiveCap = min(available, globalAvailable)` still yields $0.00. **A clipper can only ever reach live earnings on a live campaign.** That is why the blast radius is $40.69 and not $390.60, and why the three small clippers gain only $1.41, $0.94 and $0.08 rather than their full BL-661 stuck amounts of $10.57, $0.94 and $0.08.

### The four options

**(a) Exclude already-paid amounts on retired clips from the clamp, by attribution.**
* **Cost: $40.69**, same five clippers.
* **Mechanism problem:** it needs to know how much of each past payout was for now-retired clips. `payout_requests.clipIdsSnapshot` exists but covers only **101 of 144 rows, and 61 of 68 PAID rows**. Seven PAID payouts carry no snapshot and cannot be attributed at all. C-1's and C-2's four PAID rows all do have snapshots, so it would work for them, but the rule would behave differently for clippers depending on when their payout was created.
* **Could it pay twice?** Yes, against BL-661, unless that table is recomputed.
* **Verdict: correct in spirit, fragile in mechanism.**

**(b) Pay the two as a one-off and change no rule.**
* **Cost: $38.26.** No code, no deploy, no blast radius, reversible in the sense that nothing else changes.
* **What goes wrong:** it fixes nothing. The next clipper who is paid and then has those clips retired lands in the same hole, sees a balance he cannot touch, and gets "Something went wrong. Please try again." BL-688 showed that message is itself a separate defect.
* **Could it pay twice?** Yes, against BL-661, since C-1 and C-2 are in that population; subtract first.

**(c) Make the global clamp defer to the per-campaign rule generally, or switch it off.**
* **Cost: unbounded and wrong.** Measured: this would let **C-3 withdraw $14.65 on Panic Baby while $45.82 overpaid**, and would similarly release the other four over-held clippers up to their per-campaign figures. **It destroys BL-627's no-overpayment property, which is the one thing the brief says must survive.**
* **Verdict: reject.**

**(d) RECOMMENDED. Change the clamp's earnings base to lifetime earnings including retired clips.**
* **Cost: $40.69**, five clippers, measured platform-wide above.
* **Why it is better than (a):** it needs **no clip attribution and no `clipIdsSnapshot`**, so it behaves identically for every clipper regardless of payout vintage, and the seven snapshot-less PAID rows stop mattering.
* **Why it is better than (c):** it preserves the overpayment block exactly, proven by C-3 staying at $0.00.
* **What could go wrong:** it makes the clamp's base slightly more generous than the per-campaign base, so the two rules no longer use identical inputs. In practice `effectiveCap = min(available, globalAvailable)` means the stricter per-campaign rule still binds, which is what keeps the blast radius at $40.69.
* **Could it pay twice?** **Only against BL-661, and only if that table is paid without being recomputed.** Within the payout system itself, no: `moneyOut` and `locked` are still subtracted in full, so no dollar can be withdrawn twice.

---

## PART 4 — does this population grow?

**Slowly, and far more slowly than BL-661's phantom, because it requires a coincidence.**

Newly retired approved earnings since the 2026-07-18 bulk event, by day:

| date | clips retired | earnings |
| --- | --- | --- |
| **2026-07-18** | **539** | **$3,507.71** (the bulk event) |
| 2026-07-19 | 6 | $18.15 |
| 2026-07-20 | 1 | $1.24 |
| 2026-07-22 | 4 | $1.48 |
| 2026-07-23 | 9 | $1.72 |
| 2026-07-24 | 1 | $1.12 |
| 2026-07-25 | 7 | $11.37 |
| 2026-07-27 | 2 | $0.89 |
| 2026-07-30 | 9 | $3.73 |
| **12 days since** | **39** | **$39.70, about $3.31 a day** |

That $3.31 a day is what feeds **BL-661's** phantom. **This population grows only at the intersection of three conditions:** a clipper was already PAID for clips that later retire, AND the payment exceeds his remaining live earnings, AND he still has live earnings on another campaign. That intersection is why today's affected set is **five clippers and $40.69** while BL-661's is 26 clippers and roughly $400.

**Projection, stated with its uncertainty.** At the current drip the set should grow by a few dollars and perhaps one clipper a month, so a month from now is on the order of **$45 to $60 across five to seven clippers**. **UNMEASURED:** I have no time series of the blocked set itself, only today's snapshot, so this is an extrapolation from one point and should be treated as such.

**The real risk is not the drip, it is the step.** The 2026-07-18 event alone created at least two of today's five in a single evening. **Another mass retirement of a campaign's Instagram clips would convert a batch of correctly-paid clippers into blocked ones overnight**, and each of them would meet the same false "Something went wrong. Please try again." BL-688 documented. That, not the $3.31 a day, is the argument for fixing the rule rather than paying a one-off.

---

## PART 5 — the verdict

### ONE LINE

**Two clippers are genuinely owed $38.26 they cannot reach, not three owed $52.86: C-3's $14.65 is correctly blocked because he is $45.82 overpaid, and the money the other two are owed sits on ACTIVE campaigns that still reserve it, so paying it releases reserved funds rather than creating new spend.**

### Recommendation: option (d), plus the BL-688 message fix, plus a recompute of BL-661 before anyone is paid

**Ship (d): change the global clamp's earnings base from live-only to lifetime-including-retired at `src/app/api/payouts/route.ts:487-505`.** One expression, in the block that already exists, on the route that already computes both figures.

**Why this and not simply paying them.** Paying $38.26 today settles two complaints and leaves the trap armed. Option (d) costs $2.43 more across the whole platform, needs no clip attribution, and is the only option measured to preserve BL-627's no-overpayment property. It is also the only one that stops the next mass retirement producing a fresh batch of blocked clippers.

**What must be proven before it ships:**
1. **No clipper's withdrawable balance goes DOWN.** The measured table above shows five clippers up and nobody down; re-run it immediately pre-deploy.
2. **C-3 and the other four over-held clippers stay at $0.00 global.** This is the BL-627 property and it is the gate on the whole change.
3. **The blast radius is still five clippers and about $40.69** at deploy time, not a larger number that has grown in the interim.
4. **No payout is created, altered or reopened** by the change; it touches a read-side comparison only.
5. **The earnings invariant stays at 0 violations** across the population.
6. **BL-661's table is recomputed after the change** and the $40.69 subtracted before any one-off settlement is paid, so no dollar goes out twice.

**Ship BL-688's one-line message fix at `payouts/route.ts:616` at the same time.** Even after (d), a clipper can still legitimately hit the global branch, and today that refusal renders as a false 500 telling him to keep retrying. The two changes belong in the same deploy.

### The rollback, and a warning about the switch BL-688 mentioned

**The existing env kill switch is `GLOBAL_PAYOUT_CLAMP_ENABLED` (`src/lib/payout-clamp-flag.ts:13`, default ON). Confirmed by grep, it controls THREE live call sites, not one:** the payout GET display (`payouts/route.ts:156`), **the payout creation gate** (`payouts/route.ts:486`), and the earnings page display (`earnings/route.ts:213`), plus an admin unpaid-notify path (`admin/payouts/unpaid/notify/route.ts:45`).

**It is NOT a safe rollback for this problem, and BL-688 should not have implied it was.** Setting it to `false` removes the global clamp entirely, which means `effectiveCap` falls back to the per-campaign figure alone. Measured consequence: **C-3 would immediately be able to withdraw $14.65 while $45.82 overpaid**, and the other four over-held clippers would be similarly released. **Turning the switch off to fix these two clippers would hand money to the people the switch exists to stop.**

**The correct rollback for (d) is `git revert` of the commit**, which restores today's behaviour exactly, including the block on all five over-held clippers. The env switch should be left ON.

### What could not be measured

Whether C-2 or the three smaller clippers have actually attempted a withdrawal is **UNKNOWN**: a refused request writes no row, and the only trace is a `console.error` in the Railway web-service log, which cannot be read from here. Only C-1 is confirmed to have tried, by his own complaint. The month-ahead projection in PART 4 rests on a single snapshot of the blocked set and should be treated as an extrapolation, not a measurement. Whether the two clippers *should* be paid is the owner's policy call; the data says they earned it, it is still reserved by an active campaign, and no dollar of it has been paid before.

---

## Safety

READ ONLY. One document. No code, data or money change; **no payout was created, modified, approved or cancelled, no balance was touched, and the `GLOBAL_PAYOUT_CLAMP_ENABLED` switch was not flipped.** Every figure comes from read-only `SELECT`s via the sanctioned `scripts/run-select.js`, with every timestamp cast to `::text` and anchored against DB `now()`. The recommendation preserves BL-627's no-overpayment property, proven by direct measurement rather than assertion, and the one path by which a dollar could be paid twice (BL-661's table) is named with its mitigation. The full platform-wide blast radius was measured across all clippers, not only the affected ones. **No handle, email or wallet address appears anywhere, not even partially.** Nothing a live round holds, including BL-689, was touched; this round worked in its own worktree at `C:/b690` on `checkpoint/BL-690`. A markdown-only diff cannot change tsc or the build, so **no build was run and none is claimed**. NO dashes used as bullets.
