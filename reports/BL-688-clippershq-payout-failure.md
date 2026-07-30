# BL-688 — a clipper cannot withdraw: "Something went wrong, please try again"

## THIS IS NOT AN OUTAGE AND IT IS NOT EVERYONE. Payouts are being created successfully right now: the most recent one was created today at 2026-07-30 15:21:53.814, and July is the platform's busiest month at 46 payouts by 30 clippers. It is a CLASS OF THREE clippers holding $52.86 they genuinely earned and genuinely cannot reach, and the reporting clipper is one of them. The cause is exact and it is two defects stacked: a legitimate refusal is being thrown with a message the error handler does not recognise, so a 400 "your balance is $0.00" becomes a 500 "Something went wrong. Please try again."; and underneath it, the balance really is computed as $0.00 because he is charged for a payout he was correctly paid while the earnings that funded it have been removed from his balance.

**2026-07-30 · AUDIT ONLY. READ ONLY on code, data and money. No payout was created, modified, approved or cancelled. No balance was touched. Nothing was fixed.**
**Base** origin/main `765bb0e4` (`post-merge-BL-687`) · **Branch** `checkpoint/BL-688` · **Worktree** `C:/b688` (short path, node_modules never junctioned) · **DB `now()` at final query: 2026-07-30 17:34:15.547509+00**

**Redaction.** The reports repo is PUBLIC. The reporting clipper is **C-1**; the owner can map that privately to the user id prefix `cmpl310f`. The other affected clippers are **C-2** (`cmpfozzs`) and **C-3** (`cmqez5c2`). No handle, email or wallet address appears anywhere below, not even partially.

---

## PART 0 — C-1 specifically

| | |
| --- | --- |
| role | CLIPPER, `isTestUser = false`, an ordinary clipper |
| clips (not deleted) | **37**: 30 APPROVED, 0 PENDING, 7 REJECTED |
| lifetime earnings across all clips | **$41.23** |
| **earnings the withdrawal gate can see** (APPROVED, not videoUnavailable) | **$15.69** |
| **earnings stranded on videoUnavailable APPROVED clips** | **$25.54** across 21 clips |
| payout history | **exactly one row**: $25.54 gross, $23.24 net, **PAID** |
| that payout created | 2026-06-08 18:32:55.063 |
| that payout paid | 2026-06-24 16:09:02.602 |
| that payout's campaign | `cmoaa70j…` (somesome, the PAST campaign) |
| where his $15.69 lives now | a **DIFFERENT** campaign, `cmqcnzpzk…`, 8 live approved clips |
| wallet stored on his user record | **none exists, and none is expected**: there is no wallet column on `users`. The wallet is supplied in the request body on every payout |
| wallet on his one payout row | plaintext present AND encrypted present (he is in the 92 of 144 rows carrying both) |

**What the gate computes for him, from the live database, matching the code's arithmetic exactly:**

| term | value |
| --- | --- |
| global eligible earned (APPROVED, not videoUnavailable, all campaigns) | **$15.69** |
| global money out (PAID, plus VOIDED with a `paidAt`) | **$25.54** |
| global locked (REQUESTED / UNDER_REVIEW / APPROVED) | **$0.00** |
| **globalAvailable** = max(15.69 − 25.54 − 0, 0) | **$0.00** |
| **available** on campaign `cmqcnzpzk…` = 15.69 − 0 − 0 | **$15.69** |
| **effectiveCap** = min(available, globalAvailable) | **$0.00** |

### Should he be able to withdraw right now, and how much?

**By the platform's own per-campaign rule, yes: $15.69.** He has 8 live, approved, still-playing clips on a campaign he has never withdrawn a cent from.

**By the global clamp, no: $0.00**, because the clamp subtracts the $25.54 he was already correctly paid from a pool that no longer contains the earnings that funded it.

**Both figures are the platform's own. It is showing him one and enforcing the other, and telling him neither.**

---

## PART 1 — the trace, and the failing line

Every guard in `src/app/api/payouts/route.ts` POST, in order, against C-1's exact state. He passes all of them until the last one.

| # | guard | file:line | C-1 |
| --- | --- | --- | --- |
| 1 | CLIPPER role required | `:248` | PASSES |
| 2 | rate limit, 3 per hour | `:256` | passes on a first attempt; a clipper retrying **more than 3 times an hour hits this too**, adding a second confusing message |
| 3 | amount valid and > 0 | `:265` | PASSES |
| 4 | **minimum $10** | `:268` | PASSES if he requests his displayed $15.69 |
| 5 | maximum $100,000 | `:271` | PASSES |
| 6 | wallet address present | `:274` | PASSES |
| 7 | wallet length ≤ 200 | `:277` | PASSES |
| 8 | chain-aware address format | `:281` | PASSES |
| 9 | asset / chain length | `:285`, `:288` | PASSES |
| 10 | Discord username present and ≤ 100 | `:291`, `:294` | PASSES |
| 11 | campaign selected | `:302` | PASSES |
| 12 | **payout speed must be STANDARD or EXPRESS** | `:318` | PASSES. The speed choice he described is validated cleanly and is **not** the cause |
| 13 | payout method rule (asset/chain vs net) | `:353` | PASSES |
| 14 | canonical address re-check | `:363` | PASSES |
| 15 | duplicate in-flight payout | `:383-394` | PASSES, he has none |
| 16 | **the balance gate** | **`:510`** | **FAILS: $15.69 requested > $0.00 effective cap** |
| 17 | **which branch of the refusal** | **`:513-514`** | **the GLOBAL branch, because `globalAvailable ($0.00) < available ($15.69)`** |

### The failing line, and why it renders as a crash

**`src/app/api/payouts/route.ts:514`** throws:

```ts
throw new Error(`Amount exceeds your total available balance (${formatCurrency(effectiveCap)} available across your account)`);
```

**`src/app/api/payouts/route.ts:616`** is the handler meant to catch it:

```ts
if (err.message?.includes("Amount exceeds available balance")) {
  return NextResponse.json({ error: err.message }, { status: 400 });
}
```

**The strings do not match.** The thrown message says `Amount exceeds your total available balance`. The matcher looks for the literal substring `Amount exceeds available balance`, which requires `exceeds` to be followed immediately by ` available balance`. Here `exceeds` is followed by ` your total available balance`. **No match.**

The sibling throw at **`:516`** (`Amount exceeds available balance for this campaign`) **does** contain the substring and is caught correctly, which is why this bug is invisible for the ordinary case and only appears for clippers whose global balance is the binding constraint.

So execution falls past `:606` (DUPLICATE_PAYOUT), `:613` (P2002), `:616` (balance), `:619` (serialization) to the final catch-all:

**`src/app/api/payouts/route.ts:623`**
```ts
console.error("Payout creation failed:", err);
return NextResponse.json({ error: "Something went wrong. Please try again." }, { status: 500 });
```

### Refusal displayed badly, or an actual crash? A REFUSAL, displayed badly.

**This is not an exception, not a failed write, and not a null dereference.** It is a deliberate `throw` used as control flow inside the transaction, exactly like the sibling at `:516`, which the catch chain fails to recognise and therefore reports as a server error. Nothing crashed; the database write simply never happened because the gate correctly declined it.

That distinction matters for the fix: **the 500 is a message-routing bug, and it is trivially fixable. Whether the refusal itself is correct is a separate and much harder money question, addressed in PART 5.**

**The retry advice is actively harmful here.** The condition is permanent. "Please try again" invites a clipper to retry until guard 2 (`:256`, 3 per hour) also trips, at which point he receives a rate-limit message on top of a false server error, having done nothing wrong.

---

## PART 2 — how many others

Simulated across the whole population with the code's exact semantics: eligible clips are `isDeleted=false AND status='APPROVED' AND videoUnavailable=false`; money out is `PAID` or `VOIDED with paidAt`; liability is `actualPaidAmount ?? amount`; both sides rounded to cents before comparison, as `Math.round(x*100)/100` does; and the $10 minimum applied, because below it the clipper gets a clean 400 instead.

### The failing class: THREE clippers, $52.86

| clipper | campaign available (what the per-campaign rule says he can take) | global available (what he actually gets) | effect |
| --- | --- | --- | --- |
| **C-2** (`cmpfozzs`) | **$22.52** | $0.00 | every request ≥ $10 → generic 500 |
| **C-1** (`cmpl310f`, the reporter) | **$15.69** | $0.00 | every request ≥ $10 → generic 500 |
| **C-3** (`cmqez5c2`) | **$14.65** | $0.00 | every request ≥ $10 → generic 500 |
| | **$52.86 total** | | |

**All three are totally blocked**, not partially: their global available is $0.00, so no amount at or above the $10 minimum can ever succeed, and every attempt produces "Something went wrong. Please try again."

### The other candidate causes, measured, and none of them produces this message

| cause | population | dollars | what the clipper actually sees |
| --- | --- | --- | --- |
| in-flight payout blocking a new one | **9 rows, 9 clippers** (6 REQUESTED, 3 UNDER_REVIEW dating to 2026-06-05, BL-680's stale three) | $435.44 | clean **409** with a plain explanation (`:607`) |
| below the $10 minimum | those with an eligible balance under $10 | small | clean **400**, "You need at least $10 to request a payout" (`:269`) |
| missing or malformed wallet | not possible to be stuck on | n/a | clean **400** (`:275`, `:283`). The wallet is supplied per request; there is no stored wallet to be missing |
| failed wallet decrypt | **impossible on this path** | n/a | encryption is write-only at create (`:564`); no decrypt occurs |
| entire balance on videoUnavailable clips | **29 clippers hold $3,547.41** on approved-but-unavailable clips | $3,547.41 | this is the BL-661 class. It causes a **clean** refusal on its own; it becomes THIS bug only when the clipper has also already been PAID for those clips |

### Stated plainly

**This is a class, not one clipper and not everyone.** Three clippers, $52.86, all with the identical signature: previously paid for clips that have since gone unavailable, while holding live earnings on a different campaign. The 29-clipper, $3,547.41 videoUnavailable population is the pool this class is drawn from, and more clippers will enter it as more paid-for clips are retired.

---

## PART 3 — when it started, and what did NOT cause it

### Payout creation is healthy

| month | payouts created | distinct clippers |
| --- | --- | --- |
| 2026-03 | 6 | 3 |
| 2026-04 | 32 | 10 |
| 2026-05 | 15 | 10 |
| 2026-06 | 45 | 39 |
| **2026-07** | **46** | **30** |

**The most recent successful payout creation was 2026-07-30 15:21:53.814**, roughly two hours before this audit. **The rate has not dropped; July is the busiest month on record.** There is no outage and no regression in payout creation.

### Recent deploys cleared, individually

* **BL-686 / BL-687, the Instagram freshness change.** Cleared decisively: BL-687's merge was pushed at approximately 15:09 today and the successful payout at **15:21:53.814** was created **after** it. The change touches `clipper-submit-core.ts` on the clip submit path and does not appear anywhere in the payout route.
* **BL-678, the Apify hard guard.** No Apify call exists on the payout path. Cleared.
* **BL-683, the stale-earnings cleanup.** **Confirmed it touched nothing that can feed a balance.** BL-683 wrote zeroes to 10 **REJECTED** clips, and the gate's clip query at **`route.ts:411`** filters `status: "APPROVED"`, so a REJECTED clip is categorically excluded from every balance term. C-1 has 7 REJECTED clips, all already at zero, and none of them can reach his balance under any code path. Cleared.
* **The earnings display work.** Display-only, and the gate reads the database, not a display. Cleared.

### The real onset, dated to the second

The trigger is not a deploy. It is the moment C-1's already-paid clips were retired:

**2026-07-18 19:10:11.545056** — all **21** of his clips carrying **$25.54** flipped to `videoUnavailable` in a single sweep, the same $25.54 he had been paid on 2026-06-24.

From that instant his global eligible earnings fell to $15.69 while his money-out stayed at $25.54, his `globalAvailable` became $0.00, and every payout attempt has failed with the generic error ever since. **He has been unable to withdraw for 12 days.**

---

## PART 4 — the message is a real and separate bug

The underlying condition is a legitimate refusal. Telling him "something went wrong, please try again" is therefore wrong twice: it is factually false, since nothing went wrong, and it invites a retry on a permanent condition, which costs him his rate limit and costs the owner a support conversation. A clipper who cannot reach money and is told to keep trying does not experience a bug; he experiences being stonewalled.

What each refusal should say, plainly and never accusingly:

| condition | what he should be told |
| --- | --- |
| **his case: global balance is the binding constraint** | "Your available balance is $0.00 right now. Earlier payouts have already covered the clips you were paid for, and some of those videos are no longer available, so they no longer count toward your balance. Your $15.69 on <campaign> is real and we can see it. Contact support and we will sort this out." **The number and the reason must both be shown, and it must not end at a dead end.** |
| per-campaign balance exceeded | "You can withdraw up to $X from this campaign right now." (already correct today at `:516`) |
| below the minimum | "You need at least $10 to request a payout. You have $X so far." (already correct at `:269`) |
| a payout already in flight | "You already have a payout being reviewed for this campaign. We will email you when it moves." (already correct at `:607`) |
| some videos are unavailable | "Some of your approved videos are no longer reachable at their links, so their earnings are on hold. This is not a penalty." |

Every one of these states a fact and a next step, and none of them implies the clipper did anything wrong.

---

## PART 5 — the verdict and the fix

### ONE LINE

**Yes, C-1 is owed $15.69 he genuinely earned and cannot reach, and he is not alone: three clippers are totally blocked from withdrawing $52.86 between them, each one shown a false "Something went wrong. Please try again." instead of the real reason, and C-1 has been stuck for 12 days.**

### Immediate unblock for C-1, C-2 and C-3 (owner action, not code)

The money is small and the harm is not. **Pay the three of them their per-campaign balances by the normal admin route**, $22.52, $15.69 and $14.65. This needs no deploy and no code change, and it settles today's complaint. **It does not fix anything, and the next clipper whose paid-for clips are retired will land in the same place**, so the systemic fix below still has to ship.

### Ranked systemic fix

**1. Fix the message routing. One line, ships today, zero money risk.**
**`src/app/api/payouts/route.ts:616`** — widen the matcher so it catches both throws, for example matching on `Amount exceeds` rather than the exact longer phrase, or better, throw a typed error from `:514` and `:516` and branch on the type rather than on prose. **Must be proven:** the global-clamp refusal returns **400** with its real message and figure; the per-campaign refusal is unchanged; DUPLICATE_PAYOUT, P2002 and P2034 still map to 409; a genuine exception still reaches the 500. **Rollback:** revert the one-line change; behaviour returns to today's, which is strictly no worse. **This does not give anyone their money, but it stops the platform lying to them, and it converts an invisible failure into one the owner can see in the logs.**

**2. Decide the money question, and this is the owner's call, not the code's.** The clamp at **`:487-505`** subtracts a payout the clipper legitimately received while `:411` and `:491` remove the earnings that funded it, so the clipper is charged twice for the same clips going unavailable. Three defensible answers, and they differ in who absorbs the loss:
* **Exclude already-settled payouts from the clamp**, so a PAID payout no longer suppresses unrelated new earnings. This is the smallest change that matches what clippers are shown, and it is what I would recommend, but it must be modelled against the whole population before it ships because it loosens a gate that exists to prevent over-payment.
* **Keep the paid clips in the eligible pool once they have been paid for**, so the numerator and denominator stay consistent. This changes what `videoUnavailable` means for settled work.
* **Leave the clamp as-is and treat these as support cases.** Honest, and viable at three clippers; it does not scale, because the 29-clipper, $3,547.41 videoUnavailable pool is where the next ones come from.
**Must be proven for any of them:** no clipper's balance goes DOWN; no payout is created, altered or reopened; the earnings invariant stays at 0 violations; and the change is modelled across all 224 clippers before deploy, not just the three. **Rollback:** `GLOBAL_PAYOUT_CLAMP_ENABLED=false` already exists as an env kill switch (`src/lib/payout-clamp-flag.ts:13`, default ON), so the clamp can be turned off instantly without a deploy if a change goes wrong.

**3. Surface this class to the owner before a clipper has to report it.** Three clippers were stuck for up to 12 days and the only signal was a `console.error` in the Railway log. A query on the same condition, run on a schedule, would have caught it on day one.

**4. Do not raise the rate limit.** Guard 2 at `:256` is doing its job; the retry advice is what should change, not the limit.

### What could not be measured

Whether C-1, C-2 or C-3 actually attempted a payout and how often is **UNKNOWN**: a refused request writes no row, and the only trace is the `Payout creation failed:` line at `:622` in the Railway web-service log, which cannot be read from here. The reporter's account is confirmed by his complaint; the other two are inferred from their identical state, and neither has necessarily tried yet.

---

## Safety

READ ONLY. One document. No code, data or money change; **no payout was created, modified, approved or cancelled, and no balance was touched.** Every figure comes from read-only `SELECT`s via the sanctioned `scripts/run-select.js`, with every timestamp cast to `::text` and anchored against DB `now()`. **No handle, email or wallet address appears anywhere, not even partially**; the three clippers are referred to as C-1, C-2 and C-3 with an 8-character id prefix the owner can map privately. Nothing a live round holds was touched; this round worked in its own worktree at `C:/b688` on `checkpoint/BL-688`. A markdown-only diff cannot change tsc or the build, so **no build was run and none is claimed**. NO dashes used as bullets.
