# BL-824 — Money already paid is final

**Ships:** a code fix that writes nothing. Balances are derived on every read, so the repair releases the money with no database surgery. **Requires a Railway REDEPLOY.**

## The rule, and where it is enforced

> Money already PAID OUT is final and can never be clawed back by a later video deletion. If a clip is found deleted BEFORE payment its earnings may be removed. If the clipper was ALREADY PAID for that work it stays theirs and must NOT offset anything they earn afterwards.

Encoded once, in `src/lib/balance.ts`, as a property of how paid money is **subtracted**:

    effectivePaid(campaign) = min(paidGross(campaign), payableEarnings(campaign))

A payment can only ever consume the earnings of the campaign it was made against. Nothing is refunded, nothing is written, `available` is still floored at zero, and the clipper is still **shown** the full gross as paid out. Only what the balance subtracts changes.

**Why there and not at a call site.** The defect surfaced twice by two different derivations. BL-716: a pool trim rewrote one clipper's recorded earnings on a campaign down to $1,833.67 after he had been correctly paid $1,894.14, and the $60.47 was charged against his live money elsewhere; that round wrote *"a payment, once made, is a floor"* and never encoded it. BL-823: seven clippers, by a completely different route, clips rejected weeks after payment. A patch at either site would have left the other wrong.

**That place catches every path because there are three, and all three now call it.** `computeBalance` (every displayed balance), the withdrawal gate's global clamp in `payouts/route.ts`, and `campaigns/[id]/min-payout-impact` — the owner's blast-radius preview. **The brief named two. The guard found the third.** That is the argument for the guard, in one sentence.

Two admin surfaces deliberately do **not** get the rule: `admin/payouts/unpaid` and `admin/payouts/user/[id]` answer a lifetime **accounting** question on a different base, they agree with each other, and `src/lib/liability.ts` documents the two bases as first-class. The stale BL-187 comment claiming equality with `computeBalance.available` was corrected in place; no behaviour there changed.

## The two disagreeing clamp bases (BL-822), fixed — and a deliberate departure

The gate's global earnings aggregate moved from the LIFETIME base to the PAYABLE base, so the gate and the screen now compute from one base and one paid rule. BL-823 recommended the opposite — adopt the lifetime base on both sides. **That would have been wrong:** it would have released the worked clipper's $8.60 of unpaid retired earnings, breaking the other half of the owner's rule and undoing BL-818. The lifetime base was a blunt proxy for half the rule that broke the other half; the rule is now explicit, so the proxy is gone.

## What it actually releases — measured, not assumed

Production, 2026-08-24 14:45:54 UTC. Handles redacted; no wallet address appears anywhere in this report.

| clipper | ever earned | payable | paid gross | screen before | screen after | withdrawable before | withdrawable after | cash after (9%) |
|---|---|---|---|---|---|---|---|---|
| B (BL-716) | 2,293.78 | 2,293.78 | 2,293.78 | 0.00 | **60.47** | 0.00 | 60.47 | 55.03 |
| **A** | 100.87 | 92.27 | 41.59 | 50.68 | **92.27** | 59.28 | 92.27 | 83.97 |
| C | 233.95 | 214.77 | 158.87 | 23.10 | **42.28** | 42.28 | 42.28 | 38.47 |
| D | 103.34 | 37.15 | 59.98 | 0.00 | **15.97** | 15.97 | 15.97 | 14.53 |
| E | 23.56 | 12.99 | 10.31 | 2.68 | **5.54** | 5.54 | 5.54 | 5.04 |
| F | 994.82 | 993.88 | 993.36 | 0.52 | **1.46** | 1.46 | 1.46 | 1.33 |
| G | 56.77 | 48.33 | 56.69 | 0.00 | **0.88** | 0.08 | 0.88 | 0.80 |
| H | 17.05 | 17.05 | 11.23 | 5.82 | **5.84** | 5.82 | 5.84 | 5.31 |

**The brief's $121.28 to 7 reconciles, to $1.45.** BL-823 counted the seven whose **withdrawable** money moves, dropping clipper C because the per-campaign floor the gate applies means his withdrawable figure does not change (42.28 before, 42.28 after) even though his screen rises by $19.18. On that same basis today: **7 clippers, $122.73 gross, $111.69 cash** — $1.45 above BL-823's $121.28 gross / $110.37 cash, one day of ordinary accrual apart. Same rule, same seven, same arithmetic. **The code was not tuned to hit a number**; the difference is stated rather than smoothed.

On the wider basis the table above uses, **$141.91 gross of displayed balance moves across 8 clippers**, of which **$94.28 gross ($85.80 cash at 9%) is genuinely new withdrawable money to 4 of them**. The other $47.63 was **already withdrawable through the gate** and merely hidden from the screen — that is BL-822's defect closing, not new money.

**No double count, and nobody loses.** Measured across every clipper on the platform: `gate_total_gain` $94.28, **`gate_total_closed` $0.00**. The $148.28 the owner warned about (the rule plus the clamp counted separately) did not occur, because the two changes overlap almost entirely.

**Named for your attention.** The largest release, $60.47, is BL-716's clipper. After it his recorded earnings sit $60.47 **below** what he has been paid. Two others land $0.80 and $0.02 below. In every case the gate validated the payout against his available balance at request time, so the shortfall is a later **reduction of the record**, not an over-payment. But you should know that once the rule is on, a record sitting below money paid is arithmetically possible.

## Both halves of the rule, each with a real example

**Paid before deletion — kept.** Clipper A was paid $25.54 and $16.05 on two campaigns whose recorded earnings are now $0.00 (7 clips retired with earnings zeroed, 21 rejected; 8 rejected on the second). Under the fix that $41.59 stops offsetting, and his live campaign's $92.27 is his.

**Unpaid on a deleted clip — still excluded.** The same clipper has $8.60 on 21 retired clips of that live campaign, **never paid**. It stays out. His screen reads Counted $92.27 of $100.87 earned. Had BL-823's recommendation been followed he would have been handed that $8.60.

## Proven on his real screen

Rendered as the **real clipper** (minted session for his own id, dev bypass off — a synthetic user has neither retired earnings nor finalised paid money, so photographing one would prove nothing) at 320 / 375 / 414 / 1280 / 1440. **20 shots, 20 at the asked width**, `window.innerWidth` printed beside every one.

- `/api/earnings` as him: `available 92.27`, `paidOut 41.59`, `paidNoLongerOffsetting 41.59`, `removedFromBalance 8.60`.
- Earnings tiles: `COUNTED $92.27 of $100.87 earned · APPROVED $92.27 · PAID OUT, BEFORE FEES $41.59 — of which $41.59 is from finished campaigns and does not reduce this balance`.
- Payouts page: **AVAILABLE TO WITHDRAW $92.27**, and the campaign row *"$92.27 available. This clears its $15.00 minimum, so you can request a payout on it."* He saw $50.68 before.
- **No payout was requested.** The brief forbids creating one, so the gate is proven by the guard and by code, not by a POST.

## The on-screen promise, checked and fixed

The a11y review (run before any UI was written) found the existing sentence *"Money you were already paid stays yours"* true but incomplete — it does not say the money will not be taken out of later earnings, which is the whole point. Both copies now read: **"Money you were already paid stays yours, and it is never taken out of what you earn later."** Hero note and the per-row spoken sentence changed together so they cannot drift.

It also found that the fix makes the tiles contradict the hero for exactly the clippers it helps: counted minus paid out no longer reaches the balance. Hence the new server-derived sub-line under the paid tile. It is $0.00 for everyone the rule does not touch, so their page is unchanged. Reported and not fixed (out of scope): `EarningsPremium.tsx:69` mixes a period-scoped figure with an all-time one, so two different "not counted" numbers can appear on one screen.

## The guard, demonstrated failing

`scripts/bl824-paid-is-final.ts` — 14 checks, no DB, no network. Structure (the rule is one exported function; both balance derivations call it; the gate shares the payable base; every file summing `clipperLiability` is classified; every global-availability derivation applies the rule), behaviour (the real BL-823 shape through the real function), and the other half (unpaid retired stays out, BL-696 no-double-pay, BL-627 no-overpayment and the zero floor, 16 shapes asserting the rule can only ever reduce what offsets, unattributed payouts offset in full).

**Reverted both derivations to their pre-BL-824 behaviour: 9 passed, 5 FAILED**, with `B1` reading `available=50.68, expected 92.27` — the exact figure the clipper sees today. Restored; both files verified byte-identical by sha256; 14/14 green again.

## Safety

- **Money files by blob OID against the branch point:** `clip-earnings-writer.ts` `ac5be7deb061`, `earnings-calc.ts` `797e20985ad5`, `tracking.ts` `359bcbbe22fe`, `clip-earnings-invariant-middleware.ts` `61cef3939536`, `money-decimal.ts` `ef5cdae757b9`, `campaign-era.ts` `106e16ad7512` — all **IDENTICAL**. `balance.ts` **CHANGED** `e887f80acfc7 → 81a683c1a6ed`, and it had to: it is the one place both derivations share, which is the entire point of the round. The diff is two new exported pure functions and one line inside `computeBalance` swapping the raw paid sum for the bounded one. `writeClipEarnings` untouched; no write path touched.
- **Nothing written.** Invariant breaches **0**. 190 payout rows, newest payout write `2026-08-24 05:08:22.794`, hours before the first request this round made. No clip earnings or status changed, no payout created, modified, approved or cancelled, no schema change, no `prisma migrate`, no Apify actor, BL-678's 11 guards untouched.
- `npm run build` **exit 0**, `tsc --noEmit` 0 errors, hooks gate **0 errors / 11 warnings**.
- BACKLOG 163 → 164.
