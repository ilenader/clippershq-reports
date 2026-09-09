# BL-863 — show the cash, not the gross, and stop the seventh round happening

**2026-09-09 · DB `now()` = `2026-09-09 10:15:05.965718+00` (first read) to `2026-09-09 11:03:50.932412+00` (last) · BUILD, PROVE, RENDER AND MERGE.**
Base `origin/main` @ `a527de2d`. Branch `checkpoint/BL-863` @ `bffd5316`. **Merged and verified pushed: `origin/main == local == 13151279`.** Tags `pre-BL-863`, `post-BL-863`, `pre-BL-863-merge`, `post-BL-863-merge`, all on origin. Isolated worktree `C:/w863`, a short path, `node_modules` never junctioned, **removed at the end and verified gone by listing the path**. Every read through `scripts/run-select.js`, every timestamp cast `::text` against DB `now()`. Handles redacted, **no wallet address read or printed**.

**A REDEPLOY ON RAILWAY IS REQUIRED BEFORE ANY OF THIS IS LIVE.**

**Collision.** `main` moved under this round: **BL-864 merged at `2991bc87` while this was in flight**, touching twelve files, two of which this round also touches (`BACKLOG.md` and `admin/payouts/page.tsx`). Both conflicts were import lists and both were resolved as **UNIONS**, keeping BL-864's `isSentToAdmin`, its two new icons and its `ScrollTable` import alongside this round's `resolvePayoutCash`. `ownerPriceCash` was dropped from that file because this round replaced its only caller there; it is still exported and still used by the price route. The merged tree was then **rebuilt from scratch**, because a moved base means the branch's green build is no longer the merge's build. `checkpoint/BL-723` confirmed **NOT an ancestor of main**.

---

## THE ANSWER, BEFORE THE WORKING

> **THE OWNER'S OWN EXAMPLE IS WRONG BY 36 CENTS, AND THAT IS THIS ROUND IN ONE FACT.** He wrote that a $100 express request sends "about $87.36". **IT SENDS $87.00.** The express premium is charged on the **GROSS**, not on the post-fee amount: 4 percent of $100 is $4.00, not 4 percent of $91.00 which would be $3.64. Verified against every real express row on the platform, each one reproducing exactly as a percent of gross. **If the person who owns the platform cannot derive the figure from memory, no clipper can**, and that is the argument for showing it rather than a quibble about it.
>
> **THE DISCORD MESSAGE CARRIED ONE FIGURE AND IT WAS THE GROSS.** It is the only message that reaches the person holding the wallet, and the cash appeared nowhere in it.
>
> **THE CENSUS FOUND 150 SURFACES, NOT 35.** BL-813 tabulated 35 and reported "9 fixed"; its own table marks **13** rows FIXED, so that headline never reconciled and this report says so rather than repeating it. Of the 150, **8 live surfaces** showed a gross where the cash was meant, and **3 more in the dead rollback branch drop the trainer cut entirely**.
>
> **THE PATTERN IS THE FINDING, AND THE CAUSE IS AN IMPORT.** `calculatePayoutBreakdown` was always the arithmetic, but it takes five loose arguments, so **fourteen independent derivations** each decided for themselves which gross to pass and how to treat a trainer cut. On one priced row they returned **four different answers: $39.15, $34.80, $45.50 and $78.30.** The reason the trainer rule alone existed in three copies is that `mintableTrainerCutAmount` is pure but **lived in a module that imports `db`**, so no client component could reach it.
>
> **NOTHING ABOUT THE MONEY MOVED, AND IT IS MEASURED RATHER THAN ASSERTED.** 19 parity checks, 0 failed, across all 227 payout rows, against every pre-change derivation reimplemented verbatim.
>
> **THE PARITY SUITE CAUGHT TWO THINGS NO REVIEW DID**, and one of them was my own first version of the authority inventing a $0.90 deduction that was never charged.
>
> **BL-860 IS RECOVERED IN FULL.** Its launch verdict: the marketplace is **no to a general launch, yes to a one-slot watched pilot**; the trainer is **yes, with exactly one trainer**, after two ten-minute fixes.

---

## PART 0 — THE RECOUNT, BEFORE ANYTHING WAS CHANGED

### The raw counts, `grep -c` and `wc -l`, never piped through `head`

Run independently by me and by a census agent. Where we differed, both numbers are shown and reconciled rather than averaged.

| command | mine | census agent |
|---|---|---|
| `grep -rn "calculatePayoutBreakdown" src/ \| wc -l` | **52** | **51** |
| `grep -rn "finalAmount" src/ \| wc -l` | **240** | 240 |
| `grep -rn "actualPaidAmount" src/ \| wc -l` | **261** | 261 |
| `grep -rnE "payoutLiability\|clipperLiability\|campaignBudgetLiability" src/ \| wc -l` | **105** | 105 |
| `grep -rn "formatCurrency" src/ \| wc -l` | **491** | 491 |
| `grep -rln "payout-calc" src/ \| wc -l` | **13 files** | 13 |
| `grep -rn "calculatePayoutBreakdown(" src/ \| grep -v payout-calc.ts \| wc -l` | — | **15 real invocations** |

**The one-line discrepancy is reconciled and it is mine.** My count of 52 was taken after I had already added the authority to `payout-calc.ts`, which adds one referencing line; the agent's 51 is the untouched figure at `origin/main` `a527de2d`. **51 is the correct pre-change number.** Stated rather than quietly harmonised, because a count that cannot be reproduced is not evidence.

**`src/components/payouts/PayoutRequestFlow.tsx` was NOT among the 13 files importing `payout-calc`.** The first screen a clipper ever sees a money figure on was the one surface that re-implemented the formula.

### The census: 150 surfaces

Full table in the working notes; the load-bearing rows are here. **G** = requested gross, **C** = cash after all four deductions, **P** = an owner-stamped gross, **B** = a balance figure.

**THE EIGHT LIVE SURFACES THAT WERE WRONG**

| # | file:line | what the person saw | figure | why wrong |
|---|---|---|---|---|
| 1 | `payouts/page.tsx:1264` | `Hey, I'm {name}. I'm requesting a payout for {campaign} of {formatCurrency(dmStep.amount)}.` | **G** | the Discord message; `dmStep.amount` is `parseFloat(form.amount)`, the raw typed gross |
| 2 | `payouts/page.tsx:1273` | the same string rendered in the panel | **G** | same string |
| 3 | `payouts/page.tsx:1288` | the same string copied to the clipboard | **G** | same string |
| 4 | `admin/payouts/page.tsx:2421` | input labelled **`Actual paid amount ($)`** | **P** | the words say cash, the field takes a gross. This is the origin of the whole `actualPaidAmount` confusion |
| 5 | `admin/payouts/page.tsx:2531` | `Approve Full ($X)` / `Apply Adjustment ($X)` | **P/G** | the commit button named a gross with no cash beside it |
| 6 | `admin/payouts/page.tsx:757` | toast `payout APPROVED at $X` | **P** | "APPROVED at $11.00" reads as the payment; the clipper receives $10.01 |
| 7 | `admin/users/[id]/page.tsx:636` | tile **`Paid Out`** | **B, gross** | the identical clipper-side tile was relabelled `Paid out, before fees` by BL-813; this one was missed |
| 8 | `admin/calls/page.tsx:336` | a bare `· $X` with **no label at all** | **C or G** | an unlabelled coalesce that silently falls back to the gross on the ten legacy rows with a null `finalAmount` |

**THE THREE IN THE DEAD ROLLBACK BRANCH** — `payouts/page.tsx:1122`, `:1147`, `:1185`. All three compute a net that **omits the trainer cut entirely**, under the words `You receive` and `You'll receive`. `useNewPayouts` is hardcoded `true` at `:442`, so none of them renders today. **A flip back would have over-promised every trained clipper by exactly their trainer's share** — a trap that only springs on the day you are already rolling something back.

**SURFACES THAT SHOW THE GROSS CORRECTLY AND DELIBERATELY**, counted as correct and left alone: `comes off your balance` (`PayoutRequestFlow.tsx:881`), `Withdrawing {amount} from {campaign}` (`:788`), the `Requested` row label (`:934`), `You asked for` (`PayoutsRedesign.tsx:258`), `held by a closed request` (`:501`), `Paid out, before fees` (`earnings/page.tsx:326`, `EarningsPremium.tsx:392`), `Total Paid (gross)` with `Off balances, not cash sent` (`admin/payouts/page.tsx:1420`), `Amount to pay, before fees` (`:2633`), `They asked for` (`:2574`, `:2626`), and `your payout request of $X` in the rejection email and the call notification.

### The surfaces that did their own fee arithmetic — the key finding

| file:line | expression | consequence |
|---|---|---|
| `PayoutRequestFlow.tsx:250` | `platformFee = round2(amountNum * pf / 100)` | **the LIVE request screen.** Every net on it is built from four lines, never from the helper |
| `:251` | `expressFee = round2(amountNum * EXPRESS_FEE_PERCENT_DISPLAY / 100)` | ditto |
| `:295` | `standardNet = round2(amountNum - platformFee - trainerCutStandard)` | ditto |
| `:296` | `expressNet = round2(amountNum - platformFee - expressFee - trainerCutExpress)` | ditto |
| `:87` | `const EXPRESS_FEE_PERCENT_DISPLAY = 4;` | a hand copy whose own comment calls it a **"DISPLAY MIRROR of the server constant"** |
| `payouts/page.tsx:1088-1091`, `:1158-1166`, `:160` | four more hand computations and a **third** independent copy of the `4` | dead branch, drops the trainer cut |
| `admin/payouts/page.tsx:99-101` and `:132` | the trainer-cut **scaling**, hand-written **twice**, once with `Math.min(1, …)` and once without | the same rule, two clamps |
| `admin/export/route.ts:209` | `Math.round(totalClipperEarnings * 0.09 * 100) / 100` | hardcodes **9 percent** into a spreadsheet column; wrong for every referred clipper |
| `trainer-copy.ts:103-107` | `"Take a $100 withdrawal. $9 comes off for fees." / "You receive $81.90."` | four hand-computed literals on a **consent screen** |

---

## PART 1 — ONE AUTHORITY, AND WHY THERE HAD NEVER BEEN ONE

### The diagnosis

`calculatePayoutBreakdown` (`payout-calc.ts:86-143`) was always the arithmetic. It is **not** an authority, because it takes five loose arguments and leaves three decisions to every caller: which gross to pass, whether this row is express, and how to treat a trainer cut on a row the owner priced down. Those decisions were made independently at **fourteen** sites.

**Measured disagreement.** One row: `amount 100.00`, `feePercent 9`, `expressFeePercent 4`, `trainerCutAmount 8.70`, priced by the owner to `actualPaidAmount 50.00`.

```
adminSendFigure       scaled cut 4.35    50 − 4.50 − 2.00 − 4.35   = 39.15
priceCashFor          scaled cut 4.35    same                      = 39.15
review sentAmount     scaled cut 4.35    same                      = 39.15
price route cashAfter scaled cut 4.35    same                      = 39.15
clipper payout CARD   cut UNSCALED 8.70  50 − 4.50 − 2.00 − 8.70   = 34.80
clipper payout TABLE  cut UNSCALED 8.70  same                      = 34.80
liability rowCash     express DEAD, trainer ABSENT   50 − 4.50     = 45.50
liability openPayouts stale pre-price net                          = 78.30
```

**Four different answers for one row.** And two shipped comments disagreed **in writing** about which was right: `payouts/page.tsx:704-707` says the cut is "**NOT** rescaled to the owner's smaller gross"; `admin/payouts/page.tsx:93-94` says "the only honest scaling is the same ratio the payment itself was reduced by". Both deliberate, both load-bearing, and they cannot both be true about the same row.

### THE ROOT CAUSE IS ONE IMPORT

`mintableTrainerCutAmount` is a pure function that reads no database. It lived in `src/lib/trainer-relationship.ts`, which does `import { db } from "@/lib/db"` at the top. **That single import made it unreachable from any client component**, and the consequence was three implementations of one rule:

* the two **server** routes called it and scaled the cut correctly;
* the **owner's** client screens hand-inlined `cut × (gross/amount)` twice, with different clamps;
* the **clipper's** two client screens could not reach it at all and did not scale it, **printing a figure that is never paid to anybody**.

**The rule was never in dispute. Only its reachability was.**

### Where the authority now lives, and why there

**`src/lib/payout-calc.ts`.** It imports **nothing at all**, so it is safe in a client bundle and in an API route alike. That is not incidental: BL-859 lost a build to a rule module that reached a client bundle and dragged `node:module` in with it, and the first screen a clipper sees a money figure on is a client component. **An authority a client component cannot import is not an authority.**

```ts
export function resolvePayoutCash(row: PayoutCashRow): PayoutCash
export function projectPayoutCash(input: { amount, feePercent, isExpress, ... }): PayoutBreakdown
export function mintableTrainerCutAmount(row): number   // moved here
```

`trainer-relationship.ts` re-exports `mintableTrainerCutAmount`, so **no existing call site breaks**. `resolvePayoutCash` calls it rather than repeating its ratio, which makes the trainer rule provable instead of a comment. **It is the arbiter because it is the function that MINTS the trainer's actual commission row** — so the scaled figure is the money that really moves, and the unscaled displays were printing a number no person ever receives.

### The rules the authority encodes, and the measurement behind each

| rule | why, measured |
|---|---|
| **the stored `finalAmount` wins on an unpriced row** | **7 rows** from the April 2026 reset era carry a `finalAmount` their own sibling columns no longer reproduce: a $10.00 request with `feeAmount` $0.90 (nine percent) beside `finalAmount` $9.60 (a four percent deduction). Re-deriving would move a figure on a real row |
| **a row with no stored cash keeps showing the GROSS** | **10 rows** have no `finalAmount` at all, every one VOIDED, every one with a NULL `feeAmount` because they predate fee stamping. **My first version re-derived them and turned $10.00 into $9.10**, inventing a deduction never charged, under a label that reads "Requested". `cashKnown: false` now says so |
| **re-derive only when the owner has priced the row** | neither the adjust route nor the price route recomputes the fee columns, so on those rows the cash exists in no stored column |
| **the trainer cut scales with the price, via one function** | `mintableTrainerCutAmount`, the one that mints the commission |
| **the fee percent defaults to 9, never 0** | see the latent overpay below |
| **a closed request sends nothing** | BL-861's settle keeps the row in an open status, so it still carries an ordinary `finalAmount`; `settledUnpaid: true` returns `cash: 0`. Measured: 0 closed rows exist, so nothing on screen moves |

### A LATENT OVERPAY, REMOVED ON THE WAY

`adminSendFigure` read **`feePercent ?? 0`** while every other surface reads `?? 9`. On a row with a null fee percent the owner's Send column would have charged **nothing** and shown a figure **$9 per $100 too high, in the overpay direction, on the one screen where the money actually leaves.**

**Measured: 0 of 227 rows carry a null `feePercent`, so it has never fired.** A loaded gun rather than a wound, and it is now unloaded because the authority owns the default.

### Every surface now reads it, and the ones that cannot

| surface | how |
|---|---|
| the owner's Send column, `adminSendFigure` | `resolvePayoutCash(payout).cash` |
| the owner's price dialog, `priceCashFor` | `resolvePayoutCash({ ...payout, actualPaidAmount: gross }).cash` |
| the clipper's payout card | `resolvePayoutCash(payout)` |
| the PAID notification and email, `sentAmount` | `resolvePayoutCash(cashRow).cash` |
| the request screen's two nets | `projectPayoutCash(...)` |
| the dead rollback branch's three nets | `projectPayoutCash(...)`, so a rollback cannot over-promise |
| the Discord message | `resolvePayoutCash(row)` on the server's own response |
| the calls list's bare figure | `resolvePayoutCash(call.payout)` |

**THE ONE SURFACE THAT CANNOT FULLY REACH IT, NAMED.** `review/route.ts`'s **auto-adjust branch** knows something the row does not: the recomputed `amount` is in memory and not yet written, and the stored `finalAmount` belongs to the gross it replaced. It is handed the row with `amount` overridden and the stale `finalAmount` cleared, which forces the identical re-derivation the old code did. **That branch has never fired in production (0 `PAYOUT_AUTO_ADJUSTED_FOR_STALE_REDUCTION` rows), so it is preserved by construction rather than by measurement, and this report says so rather than implying it was tested.**

**REPORTED, NOT FIXED, because each is a calculation and not a display:** `admin/export/route.ts:209` hardcodes 9 percent into a spreadsheet column (wrong for every referred clipper); `trainer-copy.ts:103-107` hand-writes a worked example on a consent screen, where changing copy requires bumping `CONSENT_TERMS_VERSION`; and `EXPRESS_FEE_PERCENT_DISPLAY` remains a third hand copy of the server's `4`, because moving it means changing what the server charges reads from. **The brief said stop rather than widen, and these are where it stops.**

---

## PART 2 — THE DISCORD MESSAGE

### Before, verbatim

`src/app/(app)/payouts/page.tsx:1264`:

```
Hey, I'm ${dmStep.name}. I'm requesting a payout for ${dmStep.campaignName} of ${formatCurrency(dmStep.amount)}.${dmStep.discord ? ` (my Discord: ${dmStep.discord})` : ""}
```

Rendered on a $100.00 request:

```
Hey, I'm Sam. I'm requesting a payout for Zhus Edit of $100.00. (my Discord: sam)
```

`dmStep.amount` came from **two** producers and both were the raw typed gross: `PayoutRequestFlow.tsx:437` (`parseFloat(form.amount)`) and `payouts/page.tsx:374`. The server's `finalAmount` was already on `r.payout` and was never used. **The owner reads this in Discord and sends money. On standard the clipper receives $91.00; on express, $87.00.**

### After, verbatim, as rendered

```
Payout request from Sam.
Campaign: Zhus Edit.
My Discord: sam.

Comes off my balance: $100.00.
Platform fee (9%): less $9.00.
Express premium (4%) for fast pay: less $4.00.

Please send me: $87.00.
```

On a standard request the express line is **absent entirely** rather than printed as a zero, and the last line reads `Please send me: $91.00.` A trainer line, `Trainer share (10%): less $8.70.`, appears only when a cut is stamped.

### Every decision in it, and why

* **Built from the SERVER'S OWN ROW.** `resolvePayoutCash(dmStep.row)`. **Both** `setDmStep` producers were widened to carry `r.payout`; widening one would have left the other still sending the gross.
* **Multi-line, one fact per line.** No money line exceeds 42 characters, so a label and its figure can never separate on a 320px wrap. Every line is a complete sentence with a **leading** label and a terminal period, so if Discord collapses the newlines no figure is left beside a label that did not produce it. Every line starts with a letter, so Discord's markdown parser cannot reinterpret the block.
* **THE EXPRESS PREMIUM IS ON ITS OWN LINE WHEN IT APPLIES, with what it bought.** "for fast pay" is there so a clipper who chose express sees what that choice cost them.
* **Percentages are interpolated from the row, never literals.** The platform fee is 9, or **4 for a referred clipper**; BL-813 established that hardcoding "9%" is wrong for every referred clipper on the platform.
* **"You receive" is deliberately absent.** In a first-person message the clipper writes to the **owner**, so "you receive" would name the wrong person. The platform's own "You receive" vocabulary stays on the platform's own screens.
* **It reconciles or it simplifies.** If the parts do not subtract to the cash within a cent, the itemised block is dropped for `Payout request: $X / I receive after fees: $Y`. BL-813's rule: four lines that visibly fail to subtract are worse than two honest ones.
* **ONE ARRAY IS THE SOURCE OF BOTH THE SCREEN AND THE CLIPBOARD.** `messageLines[]` is rendered one paragraph per entry and `join("\n")`ed for the copy, so what is read and what is pasted cannot drift, and a screen-reader user gets per-line boundaries to re-read a single figure.

### The panel around it

* The block is a **`<figure>` with a `<figcaption>` reading "The message you will send"**, so it is announced as the message rather than as more instructions. A read-only `<textarea>` was rejected because it announces "edit" and invites the belief the amount can be changed there.
* **The copy button's label never changes.** It stays `Copy message`. Flipping it to "Copied!" is unreliable on iOS VoiceOver and TalkBack, it breaks the numbered instruction below that names the button by its label, and it makes the accessible name a moving target for voice control.
* **Both sonner toasts are gone.** Sonner's region is a direct child of `<body>`, so it goes silent the moment this modal gains `aria-modal`, with no build error to warn anybody. Success is a `role="status"` line mounted **empty** inside the panel; failure is a `role="alert"` **keyed on a counter**, because `role="alert"` announces on insertion and a second identical failure would otherwise be silent.
* **Two emoji removed**, the last pair on any payout surface: the modal title `Almost done — DM me to get paid 💸` is now `Almost done. DM me to get paid`, and the button `I've sent the DM ✅` is now `I've sent the DM`. CLAUDE.md forbids emoji in UI outright.

---

## PART 3 — EVERY OTHER CHANGED SENTENCE, BEFORE AND AFTER

| file | before | after |
|---|---|---|
| `payouts/page.tsx:1268` | `Your payout request is in! To get paid, send this message to @dusan_ristic_ on Discord:` | `Your payout request is in. To get paid, send this message to @dusan_ristic_ on Discord. It says what comes off your balance and what you will actually be sent.` |
| `payouts/page.tsx:1308` | `I'll do it later — my payout still stands` | `I'll do it later. My payout still stands` |
| `admin/payouts/page.tsx:2421` | label `Actual paid amount ($)` | label **`Amount to pay, before fees ($)`** — the exact phrase BL-861 already ships on the newer control 200 lines away |
| `admin/payouts/page.tsx:2531` | `Approve Full ($1,000.00)` | **`Approve full: they receive $910.00`** |
| `admin/payouts/page.tsx:2531` | `Apply Adjustment ($11.00)` | **`Cut earnings: they receive $10.01`** |
| `admin/payouts/page.tsx:757` | `Adjusted 40 clips; payout APPROVED at $11.00.` | **`Adjusted 40 clips. Approved at $11.00 before fees; they receive $10.01.`** |
| `admin/users/[id]/page.tsx:636` | tile `Paid Out` | **`Paid out, before fees`** — the same words BL-813 gave the three clipper-side tiles |
| `admin/calls/page.tsx:336` | `· $52.44` (no label) | **`· sends $52.44`**, or **`· requested $71.98`** on a row that never had a cash figure |

**Every gross that remains on screen is labelled as a gross**, and the vocabulary is reused rather than reinvented: `comes off your balance`, `before fees`, `They asked for`, `Requested`, `Paid out, before fees`, `Total Paid (gross)`. **Polarity lives in the word `less`**, never a hyphen-minus, because NVDA and VoiceOver announce `-$3.96` as "3 dollars 96", which is indistinguishable from a credit.

**Colour carries none of it.** Verified against the current CSS: dark `--text-primary`, `--text-secondary` and `--text-muted` are **all literally `#ffffff`**, so a three-tier hierarchy renders as one tier in the theme every clipper uses. The new copy therefore uses `--text-danger` (`#f87171` dark, `#b91c1c` light, 6.65:1 and 6.47:1) for the one error line and never the hardcoded `red-400`, which measures **2.77:1 on the light card** and **1.44:1 against emerald-400**.

---

## PART 4 — NO MONEY CHANGED, PROVEN TO THE CENT

`scripts/bl863-cash-parity.ts` reimplements **every pre-change derivation verbatim from the old source** and asserts the new authority returns the same figure. The old expressions are deliberately **not** imported: importing them would test the new code against itself.

```
BL-863 CASH PARITY: 19 passed, 0 failed
```

### Every real row

```
PASS  the owner's Send figure is unchanged on every real row        227 rows, 0 differ
PASS  the notification and email figure is unchanged                227 rows, 0 differ
PASS  the clipper's payout card is unchanged                        227 rows, 0 differ
PASS  every unpriced row still shows its STORED finalAmount
PASS  the 7 April-era rows whose own columns disagree are NOT moved
PASS  rows that never had a cash figure keep showing the GROSS, and say so
```

### The four cases the brief names, on a $100 request

```
PASS  STANDARD, 9%                     sends $91.00
PASS  EXPRESS, 9%                      sends $87.00
PASS  STANDARD, REFERRED 4%            sends $96.00
PASS  EXPRESS, REFERRED 4%             sends $92.00
PASS  STANDARD, 9%, trainer 10%        sends $81.90
PASS  EXPRESS, 9%, trainer 10%         sends $77.90
```

**The trainer cases are synthetic and that is stated: 0 payout rows on the platform carry a trainer cut**, because 0 trainers have ever been promoted. The standard, express and referred cases are all present in real data.

### The owner's $87.36, checked against real rows

```
NOTE  he wrote 'about $87.36'. It sends $87.00. The express premium is charged
      on the GROSS: 4% of $100 is $4.00, not 4% of $91.00 which would be $3.64.
  real row cmqgd957: gross $21.26,  express stored $0.85,  4% of gross = $0.85   MATCHES
  real row cmqofrc2: gross $78.87,  express stored $3.15,  4% of gross = $3.15   MATCHES
  real row cmqqw1kv: gross $372.97, express stored $14.92, 4% of gross = $14.92  MATCHES
PASS  the express premium is charged on the GROSS on every real express row   (82 rows)
```

### The request screen's projection

```
PASS  the shared projection equals the old inline arithmetic across the grid
      108 combinations of amount, fee percent, speed and trainer cut, 0 differ on any
      case the old code answered sanely. 13 further cases differ ONLY because the old
      inline arithmetic returned a NEGATIVE net there and the shared helper clamps.
PASS  the ONE deliberate difference: an over-large trainer cut is clamped, never negative
      old inline math returned $-0.40; the helper clamps and returns $0.00.
```

**The clamp can only ever lower a trainer cut, never raise one.** It is classified separately rather than absorbed into the parity claim, so "identical" stays exact.

### The four invariants, whole population

```
PASS  BL-538 never-decrease / the earnings invariant holds        0 violations
PASS  BL-627 no-overpayment: no clip carries negative earnings    0
PASS  no payout row carries a non-positive amount                 0
PASS  BL-696 no-double-pay: no duplicate open (user, campaign)    0
NOTE  PAID rows: gross $13,187.54, cash $11,967.47. This round moved neither.
```

**BL-824's paid-is-final and BL-849's write side hold structurally**: this round writes no clip, no earning row and no payout column. `balance.ts` is byte-identical.

### What the parity suite caught that no review did

**It failed on its first run, and both failures were real.**

1. **10 rows moved.** `cmnaqfmk old=$10.00 new=$9.10`. All ten are VOIDED, created 27 March to 1 April 2026, and every one has a **NULL `feeAmount`** as well: they predate fee stamping, so no fee was ever computed for them and no cash figure has ever existed. My first version re-derived them, **inventing a 9 percent deduction that was never charged**, under a label BL-813 deliberately set to "Requested". The old `finalAmount ?? amount` fallback is preserved exactly and `cashKnown: false` now marks them.
2. **13 grid cases differed** — every one a case where the old inline arithmetic produced a **negative net**. That is a pre-existing bug the shared helper fixes, not a parity failure, and it is counted and asserted separately rather than quietly widening the claim.

---

## PART 5 — BL-860, RECOVERED

**Found at `origin/checkpoint/BL-860`, commit `fece1fe0afc23aa284b486537f4d038de0cefc9e`, path `reports/BL-860-clippershq-health-and-launch.md`, 646 lines, committed Tue 8 Sep 2026 23:51:34 +0200.** Searched by content, not by number. Its own window: *"Measured 2026-09-08, 21:04 to 21:50 UTC, against production."* Ten subagents on ten failure modes, **all ten forbidden the database in writing**, with every query run serially by the lead on **one connection**.

### The health endpoint

> `GET https://clipershq.com/api/health` → `{"ok":true,"ts":1788902945586}`, HTTP 200 in 0.289s. Twelve lines: `NextResponse.json({ ok: true, ts: Date.now() })`. **No database, no external call, no cache header.**
>
> **"During the outage this endpoint returned 200 the entire time."** Green for all **24 hours and 11 minutes**.

**And it corrected the obvious fix.** `railway.json` has **no `healthcheckPath`**, so Railway uses a default TCP check. If the owner points it at a path that touches the database, *"a Supabase blip during a deploy makes Railway refuse to promote a perfectly healthy container"*. So: two endpoints. `/api/health` stays twelve lines for Railway; a new **`/api/health/ready`** reaches the database for an external monitor, bounded with `SET LOCAL statement_timeout = 2000`, `Cache-Control: no-store`, at **1,440 calls a day and about 0.03 percent duty cycle on one connection slot**.

**The structural limit:** *"The watchdog runs **in the same process it watches**… It structurally CANNOT catch: a container crash-loop, an OOM, a failed deploy, database or pool exhaustion, an edge failure, DNS or TLS expiry. **That is every shape the 24-hour outage actually took.**"* No Discord webhook exists anywhere.

### The cron ceiling

It went past the framing to the capacity question and **corrected its own alarm twice**.

> **"The cron ceiling is NOT the emergency it looked like… The real backlog is 1,316, not 6,783, and zero eligible jobs are 30 days stale."**
>
> **"BL-856's figure of about 4,320 a day is arithmetically correct for the code default and is NOT a hard cap."** Every normal day measured exceeds it; **6 September reached 8,483**.
>
> The real fragility: **"Demand is 6,677 checks a day against a nominal ceiling of 4,320."** It keeps up only because a backlog makes all 144 ticks run a full batch instead of 24. **"If the backlog ever fully drains, the amplification stops and capacity halves."** At saturation the order is `checkIntervalMin ASC` with no aging term, so *"it would bite established clippers whose earnings freeze while new clippers work fine"* — and **"there is no overdue-job detector anywhere in the codebase."**

### THE LAUNCH VERDICT

**THE MARKETPLACE — "NO to a general launch. YES to a one-slot watched pilot."**

Measured at `2026-09-08 21:35:22`: submissions **0**, clip posts **0**, creator earnings **0**, platform earnings **0**, marketplace clips **0 ever**. *"Zero live marketplace clips have ever existed, and nothing has ever flowed."*

Of BL-849's five launch blockers: the **redeploy is OPEN and unverifiable from the repo**; the **bonus dilution question is OPEN, analysed exhaustively and never decided**; **`savedAmount` on rejection-after-payment is OPEN and now wider**; `counter-recompute` is *"satisfied by accident"* (never fired only because it is not in the allowlist, and *"a wildcard allowlist would enable it"*); `YOUTUBE_API_KEY` is OPEN.

And a false claim in shipped source: *"`marketplace-earnings-writer.ts` states that every site writing the marketplace earning columns goes through it and that a guard script fails the build otherwise. **The guard script does not exist anywhere in the repo, and only 2 of about 14 write sites are routed through the door.**"*

Pilot conditions, verbatim: *"one poster you can telephone, one listing, `dailySlotCount = 1`, one creator, a campaign with `maxPayoutPerClip` at $20 or less… Do not press Adjust on a marketplace payout and do not use fix-budget during the pilot; those are the two unfloored write sites. Do not destroy the pilot campaign, which erases both earning rows with no record."*

Bonus dilution, answered but not decided: across **11.5 million grid points the owner realises below 10 percent in 99.312 percent** of them, median **8.99 percent**; the reachable worst case is **$122.50 and 8.16 percent**; **real cost so far $0.00**.

**THE TRAINER — "YES, with exactly one trainer, after two ten-minute fixes."**

Measured: **0 trainers ever promoted, 0 pairings, 0 commissions, 0 payouts carrying a cut.**

> **"The money path is complete and correct end to end"** … `finalAmount = amount − feeAmount − expressFeeAmount − trainerCutAmount`, **"$9.10 on $100"** either way, and **"nothing touches `Clip.earnings`"**.
>
> **"What is missing is arrival, not money: A promoted trainer is told nothing.** No notification, no email in the promote branch… **`/trainer` has no link anywhere in the application.** Both the balance and the cashout button live behind it."

Closing: *"**This is not a false all-clear.** Both systems are at absolute zero, so the first real user is the first real test in each case, and both should be watched by hand."*

### Its other findings, briefly

**The finding of the round: "A real clipper has been in UNDER_REVIEW for 96 days, and every automated watcher is blind to them."** $57.58 gross, **$52.40 net**, created `2026-06-05 01:06:42`, with a **NULL `deadlineAt`** — which removes it from the reminder sweep, both overdue counters and every sort. **Six of the eleven in-flight payouts are already overdue.**

Ten crons registered, **three have ever fired**; `vercel.json` declares five and *"this app deploys on Railway, so all five are dead config"*. Vendor keys die invisibly: a dead `HIKERAPI_KEY` files a 401 as *"this post is not a reel"*, so **"Detection: never"**. The storage gauge is pinned at 100 percent because it has a hardcoded 500 MB denominator on a **718 MB** database. **`POST /api/upload` is open to every logged-in user** with no role check despite its own comment. **~35 endpoints return success-shaped empties on error** — *"The failure was reported by five endpoints and concealed by roughly thirty-five."* `decay-strikes` has never run, so no strike has ever faded. **19 tables have no retention of any kind.**

**Its three self-corrections, named:** the backlog (6,783 → **1,316** once the cron's real eligibility filters were applied); the "starved earning clips" (2,006 approved clips looked like silent money loss — *"I nearly published that they were"* — but every one is on a PAST/COMPLETED/DRAFT campaign or has a video gone, leaving **"genuinely eligible and starved: 0 jobs, 0 approved clips"**); and the planner-statistics hypothesis (`n_live_tup` near zero looked like a vacuum problem, but `pg_class.reltuples` is accurate — *"I checked because the finding was too good, and it did not survive"*).

**Its single most valuable pre-launch action, verbatim:** *"**Turn on failure notification for the cron ping that already exists.** It is one setting in an account he already owns, it costs nothing, it needs no deploy… **That one setting alone would have turned a 24 hour blind outage into about 20 minutes.**"* Total owner action across its whole 17-item plan: *"one setting, one env var, one decision on a payout, one decision on the bonus policy, and about four clicks."*

### Should the branch be merged?

**Yes, and it is safe.** Verified read-only against current main: `git diff --name-status origin/main...origin/checkpoint/BL-860` returns **exactly one line, `A reports/BL-860-clippershq-health-and-launch.md`**. No source, schema, config or money file. It cannot break a build or alter behaviour, and `reports/` on main already holds ~30 sibling files.

**This round did not merge it**, because merging another round's branch was not in this round's ship list and a shared repo is not the place for unrequested merges. **The recommendation is to merge it with a normal `git merge --no-ff checkpoint/BL-860` and pre- and post-merge tags.** Its content is summarised above either way, so nothing is lost if it stays unmerged.

---

## PART 6 — RENDERED, AND MERGED

### 25 shots, 205 assertions, 205 passed, 0 failed

BL-793's method unchanged: viewport set on the **context**, `window.innerWidth` read back and printed beside every shot, horizontal overflow measured on every shot, a **real minted Auth.js cookie** against a **production build** with `DEV_AUTH_BYPASS=false`, and the splash lifting asserted as the postcondition for "the screen is on screen".

```
payouts-page      320 375 414 1280 1440
request-amount    320 375 414 1280 1440
request-speed     320 375 414 1280 1440
request-success   320 375 414 1280 1440
discord-message   320 375 414 1280 1440

0 at the wrong width, 0 with horizontal overflow, splash lifted on all 25
```

**IT DRIVES THE REAL FLOW AND CREATES REAL PAYOUT ROWS.** The Discord message is built from the server's own response, so there is no way to photograph it honestly without submitting. Each width picks a campaign, types $100, chooses a speed and activates the real swipe control; the message photographed is the one a clipper would actually paste.

Assertions on the message, passing at every width:

```
the block is labelled as the message that will be sent
it names the gross as what comes off the balance     Comes off my balance: $100.00.
it names the platform fee with its own percent       Platform fee (9%): less $9.00.
IT NAMES WHAT THE OWNER SHOULD SEND                  Please send me: $91.00.
it does NOT name only the gross
no emoji appears anywhere in the modal
no dash is used as a bullet
the copy button keeps one stable label
```

And on the speed step: **`$91.00` standard, `$87.00` express, `$87.36` absent, `Adds a 4% premium ($4.00)`, `$100.00 comes off your balance`, `You receive`** — at all five widths.

### What the render cost me, reported rather than smoothed

**The run is split in two, and that is stated because it is a harness limitation I could not eliminate.** A single five-width run reliably completed the first three submits and then failed the fourth, while the same widths run standalone succeeded every time with `POST /api/payouts` returning **201**. So it is an ordering effect inside a long run, not anything about the wide layouts. Splitting it, each half against its own fresh fixture, produced **15 assertions × 3 widths (123, 0 failed)** and **10 × 2 widths (82, 0 failed)**.

Four other harness corrections, all mine and none a product defect: the step-1 control is labelled **"Request payout"**, not "Continue"; the campaign must be selected by **id**, because a label regex matched the wrong option at 1280; the swipe handle's accessible name is exactly **"Swipe to confirm, or press Enter"**, and a looser pattern matched the non-focusable track label so Enter went nowhere; and a five-second wait declared failure on a commit that took about six, then fired a second activation on a screen that had already moved on. **Each is recorded in the harness beside the line it fixed.**

**One thing I could not do:** the fixture campaigns had to be `isTestCampaign: false`, because `/api/earnings` filters test campaigns out of all five of its reads and a test campaign gives a clipper **$0.00**, so the request flow could never be driven against one. They are kept invisible a different way, **ARCHIVED and PAUSED**, so no real clipper can find or submit to them, and the marker is in the name. This is a departure from the sandbox README's "keep the campaign invisible" instruction and it is disclosed rather than buried.

### The sandbox

```
164 rows recorded in C:/bl863-sandbox/ledger.jsonl
  payout_requests 24   clips 57   clip_accounts 13   campaigns 57   users 13
164 deleted, 0 already gone, 0 FAILED
VERIFIED: 0 of 164 recorded rows remain.
```

**24 payout rows were written by the PRODUCT** through the real flow, so they carry Prisma cuids and were **adopted**, each recorded with the column that identifies its owner; the destroyer re-read every one and refused unless the database itself confirmed a sandbox id. `audit_logs_userId_fkey` verified `confdeltype = n` (SET NULL) **before any user was deleted**.

`verify-gone.ts`: **50 checks, 50 passed, 0 failed.** Every real fingerprint identical, and **nothing moved at all** — clips 9,789 → 9,789, `clip_stats` 358,484 → 358,484, approved earnings $14,132.82 → $14,132.82, with zero real clips, signups, payouts or audit rows in the window. A direct sweep confirms it: `LIKE 'bl863sbx-%'` returns **0 users, 0 payouts, 0 clips, 0 campaigns.**

### The merge

| | |
|---|---|
| clean `tsc` baseline on the **untouched** worktree, before any edit | `npm ci` **0**, `npx prisma generate` **0** (before tsc, because `npm ci` wipes the client), `npx tsc --noEmit` **0**, `grep -c "error TS"` **0** |
| branch | `checkpoint/BL-863` @ **`bffd5316`**, VERIFIED on origin by `safe-push` |
| **main moved under the round** | BL-864 merged at `2991bc87`, twelve files, **two overlapping** |
| conflicts | **2, both import lists, both resolved as UNIONS.** BL-864's `isSentToAdmin`, `Send`, `CheckCheck` and `ScrollTable` kept; this round's `resolvePayoutCash` added; `ownerPriceCash` and `calculatePayoutBreakdown` dropped from that file only after confirming their remaining occurrences are all comments |
| merge commit | **`13151279`**, `origin/main` verified by `safe-push` |
| **the merge was rebuilt, not assumed** | the base moved, so the branch's build is not the merge's build. On the merged tree: `prisma generate` **0**, `tsc --noEmit` **0** with **0** `error TS`, `npm run build` **exit 0**, and the parity suite re-run: **19 passed, 0 failed** |
| BACKLOG | **187 before, 189 after** (BL-864's entry plus this one), `## BL-863` ×1, `## BL-864` ×1, **0 conflict markers**, counted with `grep -c` and **never piped through `head`** |
| **`checkpoint/BL-723`** | **confirmed NOT an ancestor of main** |
| worktree `C:/w863` | **removed, verified gone by listing the path** |

---

## GATES, HONESTLY

* **eslint confirmed present**, `v9.39.4`, so the hooks gate is a real check and not a silent no-op.
* `npx tsc --noEmit` exit **0** with `grep -c "error TS"` = **0**, run fourteen times across the round, the first on the **untouched** worktree so no error could be misattributed.
* `npm run build` **three times**, each written to a log with the exit code **echoed by hand** and **never piped through `tail`**: `BUILD1_EXIT=0`, `BUILD2_EXIT=0`, and `MERGE_BUILD_EXIT=0` on the merged tree. Prebuild clean every time: `check:prisma-bypass` **0 violations**, `check:removed-fields` **OK**, `check:event-wiring` **0 problems**, hooks gate **10 problems (0 errors, 10 warnings)** — one **below** the ceiling, with **zero added**.
* **No heredocs.** One shell at a time. Counted with `grep -c` and explicit `count(*)`, never through `head`.
* **The 6 money files plus `tracking.ts` and `campaign-era.ts`, byte-identical BY BLOB OID on BOTH refs** (`origin/main` after the merge, and `pre-BL-863`):

```
ac5be7de  clip-earnings-writer.ts    797e2098  earnings-calc.ts
81a683c1  balance.ts                 9563a4fc  tracking.ts
61cef393  clip-earnings-invariant-middleware.ts
ef5cdae7  money-decimal.ts           106e16ad  campaign-era.ts
```

* **No schema change, no `prisma migrate`, no index, no Apify actor run.** The 11 BL-678 guards untouched. **0 Supabase pool errors**; the server was stopped by PID on its own port, never by image name, and stopped before teardown.

---

## WHAT I GOT WRONG, AND WHAT COULD NOT BE PROVEN

* **My first version of the authority moved ten real rows**, turning a $10.00 VOIDED request into $9.10 by inventing a deduction that was never charged. The parity suite caught it before it shipped. That is the whole reason the suite reimplements the old code instead of importing it.
* **My surface count of 52 was one too high**, because I took it after adding the authority. The pre-change figure is 51 and both are printed above.
* **Four harness bugs of my own** during the render, each documented at the line it broke: a wrong button label, a label regex that matched the wrong campaign, a locator that matched a non-focusable element, and a timeout shorter than the request it was waiting for.
* **The trainer cases are synthetic.** Zero payout rows on the platform carry a trainer cut, because zero trainers exist, so those two figures are proven by construction and not by production data.
* **The auto-adjust branch of `review/route.ts` is preserved by construction, not by measurement.** It has never fired (0 rows).
* **A real screen reader was not run.** DOM order, roles, accessible names, the live regions and the copy path are measured; NVDA, JAWS and VoiceOver were not.
* **Nothing was verified against production over HTTP.** Every request ran locally against the merged tree, pointed at the production database.
* **A one-cent preview divergence is reported, not fixed.** `PayoutRequestFlow.tsx:248` previews from a raw `parseFloat` while the server rounds the amount first, so typing `10.166` previews a cash figure one cent from what is paid. It is **pre-existing and unchanged by this round** — my change passes the identical value through — and fixing it means changing input handling rather than display.
* **BL-518 and BL-521 are not published.** Neither exists in the reports repo, whose `reports/` begins at BL-538. Their plain, non-accusatory rule is quoted here from later rounds that cite it and from `BACKLOG.md`, and that provenance is stated rather than implied.
* **THE SEVENTH ROUND IS ALREADY VISIBLE.** `referrals/page.tsx:486` and `ReferralsRedesign.tsx:375` render `r.totalEarnings * 0.05` — five percent of lifetime **GROSS** — while the commission is minted at five percent of **NET cash** (`review/route.ts:1009-1010`). Same defect class, live, ungated, and outside this round's files. `api/trainer/me/route.ts:315` hardcodes `9` where every sibling uses `referredById ? 4 : 9`, so a referred trainer sees a fee 2.25× too large.

---

## SAFETY

Worked in an isolated worktree at `C:/w863`, a short path, `node_modules` installed there and **never junctioned**, **removed at the end and verified gone by listing the path**. Every database read through `scripts/run-select.js`, which refuses every write keyword; every timestamp cast `::text` against DB `now()`. **No wallet address was read or printed**; the fixture used a synthetic address belonging to nobody. Handles redacted; no real clipper is named. **No fee, calculation, balance or payout amount changed** — proven identical to the cent on 227 real rows and on standard, express, referred and trainer cases. **No real payout was created, modified, approved, rejected, priced, closed or paid.** The 6 money files plus `tracking.ts` and `campaign-era.ts` byte-identical by blob OID on both refs. **No schema change, no `prisma migrate`, no Apify actor run**; the 11 BL-678 guards untouched. Zero Supabase pool errors. **164 sandbox rows created, 164 deleted, 0 remaining**, verified twice by two independent methods, with every real fingerprint identical. Conflicts resolved as unions and the merged tree rebuilt from scratch. No heredocs. One shell at a time. Counts with `grep -c`, never piped to `head`. **No dashes as bullets, and no emoji anywhere in the new copy** — two pre-existing emoji were removed from the modal this round rewrites.
