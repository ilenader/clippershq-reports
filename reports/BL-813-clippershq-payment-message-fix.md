# BL-813 — every place that told a clipper the wrong payment amount, fixed in words only

**2026-08-16 · DB `now()` = `2026-08-16 17:30:06.236252+00` (first read) to `2026-08-16 17:50:58.870962+00` (last) · BUILD AND MERGE.**
Base `origin/main` @ `b91364cf`. Branch `checkpoint/BL-813` @ `d9b78e6e`. **Merged to main and verified pushed: `origin/main == local == 89fda8a3`.** Tags `pre-BL-813` (`b91364cf`), `post-BL-813` (`d9b78e6e`) and `pre-BL-813-merge` on origin. Isolated worktree `C:/w813`, a short path, `node_modules` never junctioned, **removed at the end**. Every database read through `scripts/run-select.js`, every timestamp cast `::text` against DB `now()`. Handles redacted to an 8 character id prefix; no wallet address printed.

**A REDEPLOY ON RAILWAY IS REQUIRED BEFORE ANY OF THIS IS LIVE.**

> **THE MONEY WAS ALWAYS CORRECT. Only the words were wrong.** No arithmetic, fee, balance or payout amount changed, proven to the cent on real standard, express and referred rows and across 380,000 exhaustive combinations.
>
> **35 surfaces were tabulated before anything was touched. 9 needed fixing. 26 were already correct.**
>
> **Three of the nine could not have been found by searching for the phrase.** The clipper's own earnings page shows the GROSS under the word `Paid out`, in three places. The growth engine calls approved earnings a payment in six lead-ins. And an email announced a verification call had been *scheduled* when its only caller is the request path.

---

## PART 0 — THE COUNTED TABLE, PRODUCED BEFORE ANYTHING CHANGED

Every count below comes from `scripts/bl813-sweep.sh`, using `grep -c` or `| wc -l`, and **never piped through `head`**. That discipline is not decoration: a truncated count once reported 5 hits here where the real number was 112, and BL-734 found seven copies of a scattered value after three earlier rounds had counted four and five.

| what | count |
|---|---|
| `.amount` read sites in `src/` | 235 |
| `finalAmount` | 97 |
| `actualPaidAmount` | 99 |
| `feeAmount` | 24 |
| `expressFeeAmount` | 23 |
| `payoutLiability` | 23 |
| `clipperLiability` | 49 |
| `calculatePayoutBreakdown` | 26 |
| `createNotification` call sites | 78 |
| email template functions | 24 |
| email templates that render money | 6 |
| **`payout of $X` raw hits** | **7** |
| of those, live clipper-facing copy | **3** |
| of those, **false positives** | **4** |
| `payout request of`, the correct form already present | 1 |

### The four false positives, named rather than counted as defects

| file:line | why it is not a defect |
|---|---|
| `review/route.ts:433` | a BL-812 code comment quoting the old bug |
| `notifications.ts:822` | a comment quoting copy that was deliberately removed |
| `balance.ts:231` | `for (const payout of input.payouts)`, a loop variable |
| `payout-reminders.ts:290` | `for (const payout of candidates)`, a loop variable |

### Every place a payout amount is stated, and which figure it uses

**Clipper-facing**

| # | surface | file:line | figure | verdict |
|---|---|---|---|---|
| 1 | `PAYOUT_PAID` notification | `review/route.ts:487` | cash and gross, both labelled | correct (BL-812) |
| 2 | `PAYOUT_APPROVED` notification | `review/route.ts:471` | cash and gross, both labelled | correct (BL-812) |
| **3** | **`PAYOUT_REJECTED` notification** | **`review/route.ts:480`** | **GROSS, `payout of`** | **FIXED** |
| 4 | `PAYOUT_ADJUSTED` notification | `notifications.ts:849` | **no amount at all** | correct by construction |
| **5** | **verification call requested, in-app** | **`calls/route.ts:306`** | **GROSS, `payout of`** | **FIXED** |
| 6 | call confirmed, in-app | `calls/book/route.ts:158` | no amount | correct |
| 7 | call cancelled, in-app | `calls/[id]/route.ts:56` | no amount | correct |
| **8** | **`sendPayoutApproved` email** | **`email.ts:600-610`** | **cash, bare and unexplained** | **FIXED** |
| 9 | `sendPayoutRejected` email | `email.ts:617` | gross, `payout request of` | correct, and the model for the fix |
| 10 | `sendPayoutAdjusted` email | `email.ts:632-670` | **no amount at all** | correct by construction |
| **11** | **`sendCallScheduled` email** | **`email.ts:677`** | **GROSS, `payout of`, and a false verb** | **FIXED** |
| 12 | `sendPayoutReminder` email | `email.ts:862` | gross balance, `unpaid` | correct |
| 13 | `sendClipApproved` email | `email.ts:558` | clip earnings, not a payout | correct |
| **14** | **payout card headline** | **`PayoutsRedesign.tsx:155`** | **NO LABEL AT ALL** | **FIXED** |
| **15** | **payout card fee line** | **`PayoutsRedesign.tsx:158`** | **polarity lost to screen readers** | **FIXED** |
| 16 | balance card, `in queue` | `PayoutsRedesign.tsx:240` | gross locked | correct, it is a queue position |
| **17** | **history table col 1** | **`payouts/page.tsx:608`** | **duplicate header** | **FIXED (rollback path)** |
| 18 | history table `Requested` | `payouts/page.tsx:610` | gross | correct |
| 19 | history table `Fees` | `payouts/page.tsx:611` | itemised | correct |
| 20 | history table col 5 `You receive` | `payouts/page.tsx:612` | cash | correct, and now the only such header |
| 21 | request flow, every step | `PayoutRequestFlow.tsx` | gross and cash, separated | correct (BL-812) |
| **22** | **`Paid out` tile, earnings page** | **`earnings/page.tsx:266`** | **GROSS** | **FIXED** |
| **23** | **`Paid out` tile** | **`EarningsSummary.tsx:23`** | **GROSS** | **FIXED** |
| **24** | **`Paid out` tile** | **`EarningsPremium.tsx:276`** | **GROSS** | **FIXED** |
| **25** | **growth in-app, `got paid over`** | **`growth/in-app.ts` ×3** | **gross approved EARNINGS** | **FIXED** |
| **26** | **growth email, `got paid over`** | **`growth-email/templates.ts` ×3** | **gross approved EARNINGS** | **FIXED** |
| 27 | growth nudge, distance to minimum | `growth/in-app.ts:386` | gross balance distance | correct |

**Owner-facing**

| # | surface | file:line | figure | verdict |
|---|---|---|---|---|
| 28 | review row headline `Send $X` | `admin/payouts/page.tsx:1281` | cash, labelled | correct (BL-812) |
| 29 | review row sub-line | `admin/payouts/page.tsx:1311` | gross and fees, itemised | correct (BL-812) |
| 30 | column header `Net to send` | `admin/payouts/page.tsx:1238` | cash | correct (BL-812) |
| **31** | **tile `Total Paid`** | **`admin/payouts/page.tsx:832`** | **GROSS** | **FIXED** |
| 32 | tile `Net After Fee` | `admin/payouts/page.tsx:841` | cash | correct (BL-133) |
| 33 | liability dashboard, every figure | `LiabilityView.tsx` | gross AND cash, both stated | correct (BL-810) |
| 34 | payout reminder ladder | `payout-reminders.ts` | **no amount at all** | correct by construction |
| 35 | 1099 tax report | `tax-1099.ts:82-86` | cash, documented | correct |

**Also checked and found to carry no payout figure:** the admin export, the campaign budget cap alert, the Discord path (0 money renders), and push notifications (no `web-push` dependency and no service worker).

---

## PART 1 — THE FIX, EVERY SENTENCE QUOTED

### The three the phrase sweep could not have found

These carry no `payout of` phrase and are not emails. The accessibility review surfaced them; each was then verified independently against the source before being touched.

#### 1. `Paid out` on the clipper's earnings page is the GROSS

`computeBalance.paidOut` (`balance.ts:192-194`) sums `clipperLiability`, and `clipperLiability` (`:126-132`) is `actualPaidAmount ?? amount` — **it never reads `finalAmount`**. So the figure is the gross that came off the balance, and it renders to clippers under the word **`Paid out`** in **three** places.

**A clipper who requested $30.44 and received $26.48 read `PAID OUT $30.44`.** Platform wide: **$10,396.98 displayed against $8,642.01 actually received.**

`balance.ts` is one of the six money files and was **not touched**. The figure stands exactly as it was; only the label is made true.

> **before:** `Paid Out` · `Paid out` · `Paid out`
> **after:** `Paid out, before fees` in all three

The root cause deserves naming: `clipperLiability` (gross) and `campaignBudgetLiability` / `payoutLiability` (net) are near-synonyms differing by **one line**, and the names give no warning. Any surface that picked the wrong one is silently gross.

#### 2. The growth engine called approved earnings a payment

`weeklyClipperPayoutsUsd` is documented at its own declaration (`growth/in-app.ts:126-128`) as `Clip.earnings APPROVED + MarketplaceCreatorEarning` — **gross earnings, before any fee, before any payout exists**. Six lead-ins presented it as money paid, against seven that already said earned.

> **before:** `Clippers here got paid over $8,300` · `Across the platform, clippers got paid over $8,300`
> **after:** `Clippers here earned over $8,300` · `Across the platform, clippers earned over $8,300`

Six sites, three in `growth/in-app.ts` and three in `growth-email/templates.ts`. All thirteen lead-ins now say earned. Counted after: `got paid over` **0**, `earned over` **8 and 7**.

#### 3. `sendCallScheduled` announced an event that had not happened

Its only call site is `api/calls/route.ts:316`, the **request** path. The subject said scheduled, the body said scheduled, and the next line asked the clipper to pick a time.

> **before:** subject `Verification call scheduled`, body `A verification call has been scheduled for your payout of $30.44.`
> **after:** subject `Verification call needed`, body `A verification call is needed before we can send your payout request of $30.44.`

### The live payout card, which was the worst clipper surface

`PayoutsRedesign.tsx` rendered a **bare bold figure with no label at all**, and `shown` is a three-way coalesce whose meaning changes with which branch fires:

```
actualPaidAmount   the owner adjusted the payment down: this is the cash sent
finalAmount        the net after fees: sent, or promised, or never sent
amount             the GROSS, on 10 legacy rows where finalAmount is null
```

**Measured: 10 rows carry a null `finalAmount`, and all 10 are VOIDED.** So the label had to be derived from **the field first and the status second**. A status-only label would have printed `You received` over a gross on exactly those rows, which is the defect this round exists to remove.

| condition | label |
|---|---|
| `actualPaidAmount != null` | `You received` |
| `finalAmount != null`, status PAID | `You received` |
| `finalAmount != null`, status APPROVED | `You will receive` |
| `finalAmount != null`, REQUESTED or UNDER_REVIEW | `You receive if approved` |
| `finalAmount != null`, REJECTED or VOIDED | `Would have received` |
| otherwise | `Requested` |

REQUESTED and UNDER_REVIEW are split off APPROVED deliberately: an approved payout is the owner's own commitment so a promise is safe, while one still under review can be rejected and a promise would not be.

### The adjusted rows, which carried the biggest gaps and showed nothing

`showBreakdown` excludes `actualPaidAmount != null`, so on a payout the owner reduced, the clipper saw a bare number and no explanation. **Those are precisely the rows with the largest real gaps: one clipper requested $757.20 and was sent $264.00; another requested $169.98 and was sent $25.00.**

The suppression itself is **correct and was not touched**: `finalAmount` is stale on those rows (it is the net of the *original* gross), so rendering `Requested $757.20, less fees $30.29, you receive $726.91` beside a headline of $264.00 would contradict itself.

> **after, on adjusted rows only:** `From your $757.20 request`

**This re-opens no privacy decision.** BL-812 already sends that clipper `You receive $264.00, from your $757.20 request` in the `PAYOUT_PAID` message for the same event, and both values are already in that clipper's own `/api/payouts/mine` payload with one of them already on the card. `F-CLIPPER-LEAK-FIX` stripped the pair from the **`PAYOUT_ADJUSTED` notification**, which has poster and "both" recipients — a different surface with different readers — and that notification is **untouched**. The wording is BL-812's own so the two surfaces cannot drift apart.

### The fee line had lost its polarity to screen readers

`-{formatCurrency(totalFees)}` put U+002D directly against a dollar sign, and `·` (U+00B7) was the only separator between three money facts. NVDA and VoiceOver are **silent on both at default punctuation**, so `-$3.96` announced as "3 dollars 96" — indistinguishable from a credit — and the three facts ran together as one clause.

> **before:** `Requested $46.51 · fees -$4.19 · you get $42.32`
> **after:** `Requested $46.51, less fees $4.19, you receive $42.32`

Polarity now lives in the word `less`. `you get` also became `you receive`, the phrase the other eleven payout surfaces already use.

### The rejection notification and the call notification

> **before:** `Your payout of $30.44 was rejected: <reason>`
> **after:** `Your payout request of $30.44 was rejected: <reason>`

> **before:** `A verification call has been requested for your payout of $30.44. Please select a time slot on your Payouts page.`
> **after:** `A verification call has been requested for your payout request of $30.44. Please select a time slot on your Payouts page.`

Both figures are the gross and both are **correct** — nothing was sent in either case. Only `payout of` read as a payment. `payout request of` already existed once in the codebase, in the rejection email, so the fix reuses words rather than inventing them.

### The payout-sent email now explains the difference

It showed `Your payout has been sent.` and then a single large figure. The figure was right; nothing explained why it differed from what the clipper requested.

> **after**, on a real express row:
> ```
> Your payout has been sent.
> You received
> $52.44
>
> Payout request                $60.27
> Less platform fee (9%)        −$5.42
> Less express premium (4%)     −$2.41
> You received                  $52.44
> ```

**The three fee shapes are all represented honestly and none changed.** The platform percentage is **interpolated from the row**, never written as a literal: it is 9 but **4 for a referred clipper**, and hardcoding "9%" would have been wrong for every referred clipper on the platform. The express row renders **only when a premium was actually charged**, so a standard payout does not show a `−$0.00` line.

**And it renders only when the stored parts reconcile to the cash within a cent.** On an owner-adjusted row, and on the auto-adjust path where the route rewrites `amount` and deliberately leaves `finalAmount` behind, they do not. Four lines that visibly fail to subtract are worse than three honest ones, so those rows fall back to the plain body plus one sentence:

> `This was adjusted before sending. Message us on Discord if it looks wrong.`

Proven by dumping the shipped templates: the reconciling row renders `Payout request`, `Less platform fee (9%)`, `Less express premium (4%)` and `You received`; the adjusted row renders **none of them** and carries the sentence instead.

### Full diff

```diff
  // PayoutsRedesign.tsx — the live payout card
+ const amountLabel =
+   payout.actualPaidAmount != null
+     ? "You received"
+     : payout.finalAmount != null
+       ? (payout.status === "PAID" ? "You received"
+         : payout.status === "APPROVED" ? "You will receive"
+           : payout.status === "REJECTED" || payout.status === "VOIDED" ? "Would have received"
+             : "You receive if approved")
+       : "Requested";
+ const showAdjustedNote = payout.actualPaidAmount != null && payout.amount != null;

+ <p className="text-[11px] font-semibold uppercase tracking-wider text-[var(--text-muted)]">{amountLabel}</p>
  <p className="text-xl font-bold tabular-nums text-[var(--text-primary)]">{formatCurrency(shown)}</p>
+ {showAdjustedNote && (
+   <p className="mt-1 text-xs tabular-nums text-[var(--text-muted)]">
+     From your {formatCurrency(payout.amount)} request
+   </p>
+ )}
- Requested {…} · fees <span>-{formatCurrency(totalFees)}</span> · you get <span>{…}</span>
+ Requested {…}, less fees <span>{formatCurrency(totalFees)}</span>, you receive <span>{…}</span>

  // the three Paid out tiles
- Paid Out / Paid out / Paid out
+ Paid out, before fees   (×3)

  // review/route.ts
- `Your payout of ${formattedAmount} was rejected…`
+ `Your payout request of ${formattedAmount} was rejected…`
- await sendPayoutApproved(payoutUser.email, payoutLiability(existing as any));
+ await sendPayoutApproved(payoutUser.email, payoutLiability(existing as any), {
+   requested: Number(existing.amount ?? 0),
+   feePercent: …, feeAmount: …, expressFeePercent: …, expressFeeAmount: …,
+ });

  // calls/route.ts
- `…for your payout of ${formattedAmount}. Please select a time slot…`
+ `…for your payout request of ${formattedAmount}. Please select a time slot…`

  // email.ts
- subject: "Verification call scheduled"     +  subject: "Verification call needed"
- "has been scheduled for your payout of"    +  "is needed before we can send your payout request of"
+ sendPayoutApproved gains an optional breakdown, rendered only when it reconciles

  // growth/in-app.ts and growth-email/templates.ts
- "Clippers here got paid over"              +  "Clippers here earned over"
- "Across the platform, clippers got paid over"  +  "…clippers earned over"

  // admin/payouts/page.tsx
- { label: "Total Paid", …, sub: null }
+ { label: "Total Paid (gross)", …, sub: "Off balances, not cash sent" }

  // payouts/page.tsx  (rollback-only branch)
- <TableHead scope="col">You get</TableHead>
+ <TableHead scope="col">Payout amount</TableHead>

  // notifications/page.tsx
- line-clamp-3 on the notification body
+ (removed; see the accessibility section)
```

**18 files, +705 / −19**, of which five are proof scripts.

---

## PART 2 — THE 106 MESSAGES ALREADY SENT

**They were NOT edited, and will not be.** Rewriting what somebody was already told is worse than the original error. They are reported instead.

| | |
|---|---|
| `PAYOUT_PAID` messages ever sent | **106** |
| distinct payouts behind them | 106, **0 notified twice** |
| **what the messages claimed was sent** | **$11,548.97** |
| **what was actually sent** | **$9,700.82** |
| **overstatement** | **$1,848.15** |
| messages that overstated | **105 of 106** |
| messages that were exactly right | **1** |
| **clippers affected** | **55** |
| worst single message | **$461.62** |
| oldest / newest | `2026-04-01 12:05:05.876` / `2026-08-15 21:10:27.318` |

**Reconciled against BL-812's figures, which look different and are also correct.** BL-812 measured the **93 PAID rows** ($10,396.98 against $8,642.01). This measures the **106 messages**, which are 92 rows still PAID plus **14 that were later VOIDED**. Different populations, both true. One further observation: **one PAID row (`cmokeyth`, $61.89 gross, $56.32 cash) never received a notification at all** — a legacy row with a null `paidAt`.

**The single exactly-right message is the exception that proves the model:** it is a **referral cashout**, the one payout type that takes **no fee at all** (`referral-request/route.ts:165`), so gross equalled cash. Every message with a fee behind it was wrong.

### Per clipper, redacted to a mappable short id

`id8` is the first 8 characters of the user id and `md6` is `substr(md5(userId),1,6)`, the two forms every earlier round used, so the owner can map them privately in admin.

| id8 | md6 | msgs | told | actually sent | gap |
|---|---|---|---|---|---|
| `cmpl1dds` | `a0f203` | 1 | $725.62 | $264.00 | **$461.62** |
| `cmqez5c2` | `dfb43b` | 1 | $1,894.14 | $1,647.90 | $246.24 |
| `cmp0zwli` | `9cbad3` | 3 | $233.14 | $38.39 | $194.75 |
| `cmp7153e` | `3a8763` | 2 | $1,441.54 | $1,252.27 | $189.27 |
| `cmpy4psy` | `ceb76d` | 1 | $169.98 | $25.00 | $144.98 |
| `cmosmyqk` | `bc64d4` | 1 | $993.36 | $903.96 | $89.40 |
| `cmn4nlfg` | `a92aea` | 9 | $910.11 | $828.20 | $81.91 |
| `cmofpudr` | `2abe41` | 3 | $1,607.33 | $1,543.04 | $64.29 |
| `cmpzxsgn` | `d0bf8a` | 1 | $74.80 | $20.00 | $54.80 |
| `cmrl046b` | `299618` | 3 | $411.67 | $372.62 | $39.05 |
| `cmnd5tai` | `471193` | 7 | $511.00 | $475.51 | $35.49 |
| `cmryxhyv` | `1e0ce1` | 2 | $246.96 | $224.73 | $22.23 |
| `cmp7ic4p` | `aaebb6` | 2 | $37.01 | $17.00 | $20.01 |
| `cmoafodb` | `8638e0` | 2 | $350.00 | $334.05 | $15.95 |
| `cmrng806` | `a0f7fd` | 7 | $123.49 | $107.85 | $15.64 |
| `cmq7qh6p` | `f191a2` | 2 | $112.00 | $101.22 | $10.78 |
| `cmosj3qk` | `99635c` | 3 | $114.16 | $103.38 | $10.78 |
| `cmpk11wz` | `e13a90` | 1 | $78.87 | $68.62 | $10.25 |
| *37 more clippers* | | | | | **$120.36 combined** |

**The five largest gaps are not fee gaps.** `$461.62`, `$194.75`, `$144.98`, `$89.40` and `$54.80` are payouts the owner deliberately **adjusted down** before sending, where the message still stated the full request. Those are the ones most likely to be queried, and they are also the rows the payout card now explains with `From your $X request`.

### Has anyone queried it?

**No, in every surface the platform stores.** `problem_reports` holds 7 rows, of which exactly one mentions money, and it is about **speed, not amount**: *"I request to pay out yesterday but still it's not paid me"*. Chat messages matching payout plus a complaint word: **0 of 109**.

**An honest limit:** the chat was removed by BL-804, and anything said on Discord is outside this database. So the accurate claim is that **no query has been recorded anywhere the platform keeps a record**, not that nobody ever mentioned it.

### Wording the owner can send, if anyone asks

> You were paid the right amount. The message you got named the amount you asked to withdraw, not the amount that reached your wallet after the payout fee, and that wording was our mistake. Nothing was deducted twice and nothing is missing. Your payout page now shows both figures side by side, so you can always see what you asked for and what arrived. If the two still do not look right to you, send me the date and I will pull the record up.

For one of the five adjusted cases, add:

> On this one I also paid less than the full request, and the message should have said so. Your payout page now shows the request beside the amount sent.

---

## PART 3 — THE OWNER SIDE, WHERE A WRONG NUMBER COSTS REAL MONEY

BL-763 caught the owner about to send $71.98 and $10.15 when $65.50 and $8.83 were owed, and BL-760 caught $5.44. Every owner-facing amount was re-checked at the moment he pays.

| surface | figure | verdict |
|---|---|---|
| review row headline | cash, labelled `Send $17.98` | correct, BL-812 |
| review row sub-line | `$20.67 requested −$1.86 fee −$0.83 express` | correct, BL-812 |
| column header | `Net to send` | correct, BL-812 |
| **`Total Paid` tile** | **GROSS** | **FIXED** |
| `Net After Fee` tile and column | cash, `~X% blended` | correct, BL-133 |
| `Total Available` tile | gross owed, with a cash twin beside it | correct |
| **liability dashboard** | **every figure states gross AND cash** | correct, BL-810 |
| payout reminder ladder | no amount at all | correct by construction |
| 1099 tax report | cash, `actualPaidAmount ?? finalAmount ?? amount` | correct, documented |
| admin export | campaign spend, no payout figure | correct |

**The one fix.** `Total Paid` is sourced from `clipperLiability` (`unpaid/route.ts:131`), so it is the **gross that came off clipper balances, not the cash sent**. On the page where the owner decides what to pay, an unqualified `Total Paid` is the same ambiguity that twice nearly caused an overpayment.

> **before:** `Total Paid`
> **after:** `Total Paid (gross)`, with the sub-caption `Off balances, not cash sent`

**The qualifier is in the LABEL, not in `sub`.** The tile renders three sibling paragraphs with no programmatic association — label, value, then sub — so a `sub` arrives **after** the number it is meant to disambiguate, and two of the five tiles omit `sub` entirely, so a reader cannot rely on one existing.

---

## PART 4 — THE MONEY DID NOT MOVE

`scripts/bl813-amounts.ts` re-derives every row through `calculatePayoutBreakdown`, the same helper the POST route calls, and compares against what is **stored**. **5 assertions, 0 failures, exit 0.**

```
cmq084lz  standard 9%                  gross    $57.58  stored cash    $52.40  re-derived    $52.40  IDENTICAL
cmsnvqqn  standard 9%                  gross    $46.51  stored cash    $42.32  re-derived    $42.32  IDENTICAL
cmst92ua  standard 9%                  gross    $24.56  stored cash    $22.35  re-derived    $22.35  IDENTICAL
cmsul7p1  standard 9%                  gross    $21.00  stored cash    $19.11  re-derived    $19.11  IDENTICAL
cmsuku4g  standard 9%                  gross    $20.29  stored cash    $18.46  re-derived    $18.46  IDENTICAL
cmsv1ifo  express 9% + 4%              gross    $60.27  stored cash    $52.44  re-derived    $52.44  IDENTICAL
cmsl8dbu  express 9% + 4%              gross    $20.67  stored cash    $17.98  re-derived    $17.98  IDENTICAL
cmsq04pf  express 9% + 4%              gross    $10.00  stored cash     $8.70  re-derived     $8.70  IDENTICAL
cmpird39  referred 4%, owner-adjusted  gross   $757.20  stored cash   $726.91  re-derived   $726.91  IDENTICAL
cmq7rzof  referred 4%, owner-adjusted  gross    $74.80  stored cash    $71.81  re-derived    $71.81  IDENTICAL
```

**The three fee shapes, on one gross so they can be compared:**

```
standard, not referred   $30.44 − $2.74 = $27.70
standard, referred       $30.44 − $1.22 = $29.22
express,  not referred   $30.44 − $2.74 − $1.22 = $26.48
express,  referred       $30.44 − $1.22 − $1.22 = $28.00
```

The reduced referred rate lowers the platform fee and **never** the express premium; express is **4% ON TOP**, so the platform fee is identical between speeds. Asserted, then re-asserted exhaustively: **every amount from $10.00 to $2,000.00 at both platform rates, 380,000 combinations, 0 violations** — express always on top, cash never exceeding gross, never negative, and the parts always summing back to the gross.

**Live totals, before the round and after it:**

| | before | after |
|---|---|---|
| payout rows | 173 | **173** |
| Σ gross `amount` | $15,745.49 | **$15,745.49** |
| Σ express premium | $180.56 | **$180.56** |
| cash paid on PAID rows | $8,642.01 | **$8,642.01** |
| `PAYOUT_PAID` notifications | 106 | **106, none edited** |
| earnings invariant violations | 0 | **0** |

**BL-627's no-overpayment property, re-verified live:** 4 clippers hold $82.12 above their earnings, **0 with a negative available balance** — every one clamps at zero, exactly as BL-810 and BL-812 measured. **BL-696's no-double-pay property, re-verified live:** **0** duplicate open payouts per (clipper, campaign). Neither property has any term this round could touch.

**One payout row moved during the round and it was not mine.** `cmsw1rit`, a real clipper (`cmst3xpf`) requesting $31.15 at `2026-08-16 16:56:36.866`, with `createdAt == updatedAt`, so it was created and never modified. This round made no payout request of any kind.

---

## PART 5 — RENDERED AND MEASURED

BL-793's method: real Chromium, the CSS viewport set through `browser.newContext({ viewport })`, `next dev --webpack`, and `window.innerWidth` read back and asserted every time. **70 assertions, 0 failures, exit 0.**

### The clipper's payout screen, before and after, read out of the DOM

**Before:**
```
Paid    $42.32   Requested $46.51 · fees -$4.19 · you get $42.32
Paid    $52.44   Requested $60.27 · fees -$7.83 · you get $52.44
Approved $71.81  Requested $74.80 · fees -$2.99 · you get $71.81
Paid    $264.00                                      (nothing at all)
Rejected $27.70                                      (nothing at all)
Voided  $71.98                                       (nothing at all)
```

**After:**
```
Paid     YOU RECEIVED         $42.32   Requested $46.51, less fees $4.19, you receive $42.32
Paid     YOU RECEIVED         $52.44   Requested $60.27, less fees $7.83, you receive $52.44
Approved YOU WILL RECEIVE     $71.81   Requested $74.80, less fees $2.99, you receive $71.81
Paid     YOU RECEIVED        $264.00   From your $757.20 request
Rejected WOULD HAVE RECEIVED  $27.70
Voided   REQUESTED            $71.98
```

Note the last row: its `finalAmount` is null so the figure is the **gross**, and the field-derived label correctly reads `Requested` rather than a false `Would have received`. That is the case a status-only label would have got wrong.

| assertion, at every width | 320 | 375 | 414 | 1280 | 1440 |
|---|---|---|---|---|---|
| CSS viewport really is the asked width | yes | yes | yes | yes | yes |
| no sideways page scroll | yes | yes | yes | yes | yes |
| **every money headline has a label before it** | yes | yes | yes | yes | yes |
| each of the six figures reads its expected label | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 |
| the adjusted row states `From your $757.20 request` | yes | yes | yes | yes | yes |
| the fee line carries polarity in the word `less` | yes | yes | yes | yes | yes |
| the outlier `you get` is gone | yes | yes | yes | yes | yes |

**It reads well at 320px**, which was the specific risk: the labels are `text-[11px]` uppercase on their own line above the figure, so a longer sentence cannot push a number above its own label, and no card wraps badly.

### The emails were rendered too

All three changed emails were dumped as HTML **from the shipped template functions** through the shipped `wrap()`, so the markup measured is the markup that ships rather than a retyped copy, and rendered at all five widths. **`email-payout-sent`, `email-payout-sent-adjusted` and `email-call-needed` each fit with no sideways scroll at 320, 375, 414, 1280 and 1440.**

The breakdown markup follows the email specialist's constraints: a `role="presentation"` table rather than a `<dl>` (Outlook's Word engine flattens a `<dl>` into indented paragraphs with no term or definition semantics), no `<th>`, `<thead>`, `scope` or `<caption>` (Gmail strips `role="presentation"` and would expose a headerless data table), widths as HTML attributes with `align` alongside `text-align`, the font stack repeated on every text element, and **the dark-mode class on the `<p>` and never the `<td>`**, because `body .content-cell p` is specificity (0,1,2) and repaints the paragraph directly, so an inherited colour would lose. `.footnote` was deliberately **not** used on any breakdown row: it measures **4.33:1** in dark mode, under the 4.5:1 floor.

**No width had to be skipped and no screen is claimed that was not seen.**

---

## PART 6 — MERGED AND PUSHED

**A clean `tsc` baseline was recorded on the untouched worktree BEFORE any edit**, after `npm ci` exit 0 and `npx prisma generate` exit 0: **`tsc --noEmit` exit 0, 0 errors.** One error appeared later and was **attributable to the uncommitted render harness, not to the fix**; it was fixed and `tsc` returned to 0.

| | |
|---|---|
| branch | `checkpoint/BL-813` @ **`d9b78e6e`** |
| merge commit | **`89fda8a3`** |
| **`origin/main`** | **`89fda8a3`**, verified by `git ls-remote` |
| conflicts | **none**; main had not advanced |
| BACKLOG sections | **156 before, 157 after**, `BL-813` ×1, counted with `grep -c` and never piped to `head` |
| **`checkpoint/BL-723`** | **confirmed NOT an ancestor of main** |

> **A REDEPLOY ON RAILWAY IS REQUIRED.** Main carries all of this; production does not.

---

## PART 7 — THE EVIDENCE

| claim | evidence |
|---|---|
| every place counted before anything changed | `scripts/bl813-sweep.sh`, 35 surfaces tabulated, 7 raw phrase hits split into 3 live and 4 named false positives |
| every clipper-facing figure now shows what they received | 6 of 6 labels correct at all five widths, **0 money headlines without a label** |
| the gross is kept and clearly labelled | `From your $757.20 request` on adjusted rows, `Paid out, before fees` on the three tiles, `Requested` on the legacy-null rows |
| the three fee rates are honest and unchanged | 9% and referred 4% interpolated from the row, express 4% on top, all asserted over 380,000 combinations |
| **the received amount is identical to the cent** | 10 real rows across standard, express and referred re-derive **IDENTICAL** |
| no-double-pay and no-overpayment survive | 0 duplicate open payouts; 4 over-held clippers all clamped, 0 negative |
| the earnings invariant | **0 violations**, before and after |
| the 106 historical messages | **unedited**; 106 before, 106 after |
| owner side states gross or cash | `Total Paid (gross)`, `Off balances, not cash sent`; every other owner figure already correct |
| rendered at five widths | **70 assertions, 0 failures**, screens and all three emails |
| no clip's earnings or status changed | this round issued no clip write of any kind |
| no payout created, modified, approved or cancelled | 173 rows, Σ gross and Σ express identical; the one row touched was a real clipper's own request |
| the 6 money files plus `tracking.ts` and `campaign-era.ts` | **byte-identical by blob OID** on `b91364cf` and on merged `HEAD`: `ac5be7de`, `797e2098`, `e887f80a`, `83ce4bab`, `61cef393`, `ef5cdae7`, `106e16ad`, plus `payout-calc.ts` `029834b4` |
| BL-678 guards | **18 `APIFY_HARD_OFF` references intact**, no Apify actor run |
| schema | **no change, no `prisma migrate`**; `prisma generate` only |

---

## THE ACCESSIBILITY REVIEW, AND WHAT IT CAUGHT THAT I HAD NOT

Reviewed before any code was written, with two specialists. It returned **NO-GO as planned on three of my six items** and **10 blocking items, all 10 implemented**. Three of its findings were categories my sweep could not have reached, and each was verified independently before being acted on.

1. **The headline label must be derived from the FIELD, not the status.** `?? amount` still fires on legacy rows; I measured 10, all VOIDED.
2. **REQUESTED and UNDER_REVIEW split off APPROVED.** A promise is safe on the owner's own commitment and not on something that can still be rejected.
3. **Label above the figure, in DOM order**, so a 320px wrap can never put the number above its own label.
4. **The fee line's polarity** moved into the word `less`; the hyphen-minus and the middle dot were both silent to screen readers.
5. **The fee percentages must be interpolated**, never literals, or the email is wrong for every referred clipper.
6. **The breakdown must be gated on reconciliation**, because adjusted and auto-adjusted rows do not subtract.
7. **The adjusted sentence re-opens nothing**, evidenced by BL-812 already sending both figures for the same event.
8. **Do not make two column headers identical**, even in dead code: they hold the same figure in one of six data cases.
9. **`sendCallScheduled` states an event that has not happened** — subject and verb both corrected.
10. **`line-clamp` clips by LINE COUNT, not characters**, so at 320px or 200% zoom a rejection reason silently fell off the end while the full string stayed in the DOM for screen reader users only. Removed on `/notifications`, which has the room; the navbar dropdown and the toast keep theirs deliberately, because they are previews with that page behind them.

**Where it escalated rather than decided.** On the adjusted-row sentence it flagged an accessibility-versus-privacy conflict and declined to reverse another round's intent. **The call was mine and I made it:** state the pair, because BL-812 already sends exactly those two figures to that clipper for that event, both are already in their own payload, and `F-CLIPPER-LEAK-FIX` governs the `PAYOUT_ADJUSTED` notification with its poster and "both" recipients, which is untouched.

**Reported, NOT fixed, each wanting its own round.** A currency figure as `<th scope="row">` prefixes every cell in the payout table row with a non-unique amount. `showBreakdown` suppressing the breakdown on adjusted rows wants a second, adjusted-row breakdown rather than silence. The verification-call notification uses `type: "PAYOUT_APPROVED"`, so a request for verification carries a success icon. `.footnote` measures 4.33:1 in dark-mode email. And `notifications.ts:833-838` still emits literal `/payouts` and `/earnings` in bodies, where the `/` is skipped at default screen-reader punctuation.

---

## GATES, HONESTLY

* **Clean baseline on the untouched worktree, BEFORE any edit:** `npm ci` exit **0**, `npx prisma generate` exit **0** (run before `tsc`, because `npm ci` wipes the generated client), `npx tsc --noEmit` exit **0**, `grep -c "error TS"` = **0**.
* **`eslint` confirmed present**, `npx eslint --version` reports **v9.39.4**, so the hooks gate is a real check and not a silent no-op.
* After the change: `npx tsc --noEmit` exit **0**, 0 errors.
* `npm run build` **twice**, both from a log with the exit code echoed by hand and **never piped through `tail`**: **`BUILD1_EXIT=0`** on the branch (compiled in 32.6s) and **`BUILD2_EXIT=0`** on the merged tree (33.8s). Prebuild clean both times: `check:prisma-bypass` **0 violations**, `check:removed-fields` **OK across 728 files**, hooks gate **11 problems (0 errors, 11 warnings)** at the ceiling of 11 with **zero added** — every change is a string, a ternary or a lookup, so no new hook and no new dependency array exists.
* `scripts/bl813-amounts.ts` **5 passed, 0 failed, exit 0**. `scripts/bl813-render.ts` **70 passed, 0 failed, exit 0**.
* Counted with `grep -c`, **never piped through `head`**. **No heredocs**: every multi-line file was written with the file-write tool.
* The render harness route is **NOT committed**; its full source is in the round's commit history and its purpose is documented in `scripts/bl813-render.ts`'s header.

---

## WHAT COULD NOT BE MEASURED, AND WHY

* **Whether any clipper queried the amount outside the platform.** The chat was removed by BL-804 and Discord is not in this database. What can be stated is that **no query is recorded in `problem_reports` or in the 109 archived chat messages**.
* **Whether a real mail client renders the breakdown as intended.** The HTML is the shipped markup, rendered and measured in Chromium at five widths, and it follows the Outlook and Gmail constraints the specialist set. Gmail, Outlook and Apple Mail were not opened.
* **Whether a real screen reader speaks the new labels as intended.** The DOM order, the label-before-value relationship and the absence of unlabelled figures are all measured. NVDA, JAWS and VoiceOver were not run.
* **The auto-adjust email branch was not exercised**, because it has never fired in production (0 `PAYOUT_AUTO_ADJUSTED_FOR_STALE_REDUCTION` audit rows). The reconciliation gate covers it by construction and is proven on the owner-adjusted shape, which is the same failure mode.
* **Nothing was verified against production.** Every render ran locally against the merged tree with the dev-auth bypass.

---

## VERIFICATION AND SAFETY

Wording and labelling only. **13 shipping files changed**, plus `BACKLOG.md` and five proof scripts.

**No arithmetic, fee, balance, payout amount or stored value changed. No clip's earnings or status changed. No payout was created, modified, approved, cancelled or paid. The 106 historical messages were not edited. No schema change and no `prisma migrate`; `prisma generate` only. No Apify actor ran and the 18 `APIFY_HARD_OFF` references are intact.** The earnings invariant reads **0 violations**. The 6 money files plus `tracking.ts` and `campaign-era.ts` are **byte-identical by blob OID on both refs**, and `payout-calc.ts` is byte-identical and absent from the diff.

Every figure traces to the query or the script that produced it. Every timestamp is cast `::text` against DB `now()`. Handles are redacted to an 8 character prefix and a stable `md5` short id; **no wallet address is printed**. **NO dashes as bullets.** The worktree `C:/w813` was removed.

**Rollback:** `git revert -m 1 89fda8a3`, or `git reset --hard pre-BL-813-merge`. **Nothing in the database needs undoing.**
