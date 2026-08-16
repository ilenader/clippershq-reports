# BL-812 — the payout confirm control shows what the clipper RECEIVES, and everything left is merged

**2026-08-16 · DB `now()` = `2026-08-16 15:30:37.702142+00` (first read) to `2026-08-16 16:12:00.30571+00` (last) · BUILD AND MERGE.**
Base `origin/main` @ `c94dc229` (BL-809 and BL-811 both merged). Branch `checkpoint/BL-812` @ `df187099`. **Merged to main and verified pushed: `origin/main == local == b91364cf`.** Tags `pre-BL-812` (`c94dc229`), `post-BL-812` (`df187099`) and `pre-BL-812-merge` on origin. Isolated worktree `C:/w812`, a short path, `node_modules` never junctioned, **removed at the end**. Every database read through `scripts/run-select.js`, every timestamp cast `::text` against DB `now()`. Handles are redacted and no wallet address is printed.

**A REDEPLOY ON RAILWAY IS REQUIRED BEFORE ANY OF THIS IS LIVE.**

> **The owner walked his own payout flow and found it. Step 2 read `You receive $27.70` on Standard and `You receive $26.48` on Express, and the swipe control underneath read `Swipe or hold to request $30.44`. That is the GROSS, and it did not move when he switched option. A clipper swiped expecting $30.44 and received $26.48.**
>
> **Only the labelling was wrong. Every figure was arithmetically correct.**
>
> **And it was not the only place. `PAYOUT_PAID` told 106 clippers `Your payout of $X has been sent` using the gross, while the email sitting beside it already said the cash. Across the 93 PAID rows those notifications claimed $10,396.98 was sent against $8,642.01 that actually was.**

---

## PART 0 — THE THREE NUMBERS ON ONE SCREEN, RECONCILED BEFORE ANYTHING CHANGED

### Each figure, its formula, and the line that produces it

| what the owner saw | what it is | produced by |
|---|---|---|
| **$30.44** on the swipe control | the **GROSS**: what the clipper typed, and what leaves their balance | `amountNum = parseFloat(form.amount)`, `PayoutRequestFlow.tsx:226`; passed to the control at `:759` as `amountLabel={formatCurrency(amountNum)}` |
| **$27.70** on the Standard card | the **CASH** after the 9% platform fee | `platformFee = round2(amountNum * pf / 100)` `:228`, `standardNet = round2(amountNum - platformFee)` `:230` |
| **$26.48** on the Express card | the **CASH** after 9% **plus** a further 4% express premium | `expressFee = round2(amountNum * 4 / 100)` `:229`, `expressNet = round2(amountNum - platformFee - expressFee)` `:231` |

The rate that drives `pf` comes from `gamification.ts:617`, `user.referredById ? DEFAULT_REFERRED_FEE : config.platformFee`, which is `4 : 9`. The server charges through `calculatePayoutBreakdown` (`payout-calc.ts:61-83`) called at `payouts/route.ts:419`, with its own rate decided identically at `payouts/route.ts:403`.

### The arithmetic is CORRECT. Only the labelling is wrong.

That distinction decides the fix, so it is proven rather than asserted. `scripts/bl812-amounts.ts` puts the owner's exact case through **the same helper the POST route calls**, and compares the flow's on-screen preview against what the server would actually charge. **12 assertions, 0 failures, exit 0.**

```
gross the clipper typed                 $30.44
platform fee, 9% of gross              -$2.74
STANDARD cash                           $27.70
express premium, 4% of gross           -$1.22
EXPRESS cash                            $26.48

PASS  the $27.70 on the Standard card is gross minus the 9% fee      $30.44 - $2.74 = $27.70
PASS  the $26.48 on the Express card is gross minus 9% then a further 4%
PASS  the express premium is 4% ON TOP of the 9%   platform $2.74 both ways, express adds $1.22
PASS  the flow's PREVIEW equals what the server would CHARGE, standard   $27.70 vs $27.70
PASS  the flow's PREVIEW equals what the server would CHARGE, express    $26.48 vs $26.48
PASS  so every figure is ARITHMETICALLY CORRECT and only the LABELLING is wrong
      the control shows $30.44 while express pays $26.48, a $3.96 gap
```

**Nothing is miscalculated.** Had a figure been genuinely wrong the fix would have been in the arithmetic; it is in the words, so the fix is in the words. This is BL-744's rule stated as a defect: **a figure must never sit beside a label that did not produce it.** The gross sat under two cards that both said `You receive`.

### The reduced 4% referred rate, and how it was handled

**It changes the cash and never the gross, which is exactly why the control had to show cash.** On the same $30.44:

| | platform fee | STANDARD cash | EXPRESS cash |
|---|---|---|---|
| not referred | 9%, $2.74 | **$27.70** | **$26.48** |
| **referred** | **4%, $1.22** | **$29.22** | **$28.00** |

**The express premium stays 4% for a referred clipper too**, asserted. So two clippers requesting the identical $30.44 receive $26.48 and $28.00, and no reader can derive either from the gross. This is not academic: **178 of 1,430 users carry a `referredById`, and 23 of the 162 fee-bearing payout rows were charged 4%.**

The fix inherits this for free, because the new figures are derived from the existing `standardNet` and `expressNet`, which already use the per-user rate. The render proof includes a referred case at 4% at all five widths.

---

## PART 1 — THE FIX

### What shipped, quoted exactly

The confirm control now reads, with Express selected on a $30.44 request:

```
You receive                                              $26.48
$30.44 comes off your balance

[ →   Swipe to confirm   » ]
```

and with Standard selected the first figure reads **$27.70**. It changes the instant the radio does.

Quoted verbatim: **`You receive`**, **`comes off your balance`**, **`Swipe to confirm`**, and the handle's accessible name **`Swipe to confirm, or press Enter`**.

**`You receive` is reused verbatim from the speed cards' own `netLabel`.** That is the point rather than a convenience: the same words now always carry the same number, so the eye moving from the card to the control sees no new figure appear.

### Why the money is above the track and not in it, measured

The obvious fix is `Swipe or hold to receive $26.48`. **It does not fit, and the figure would be the first thing cut off.** Measured in a real Chromium, inside the REAL `<Modal>`:

| viewport | track | label box | text needs | clipped? |
|---|---|---|---|---|
| **320** | 238px | **102px** | 220px | **yes** |
| 360 | 278px | 142px | 220px | yes |
| **375** | 293px | **157px** | 220px | **yes** |
| **414** | 332px | **196px** | 220px | **yes** |
| 1280 | 462px | 220px | 220px | no |

**So the shipped string has been clipped on every phone since BL-465, and nobody noticed because the truncated part was the money.** A short instruction is the only thing that fits: `Swipe to confirm` measures 116px and lands in the 116px box exactly once `px-14` becomes `pl-14 pr-4` (the left 56px clears the 48px handle by 4px and cannot shrink; the right 56px cleared nothing).

**An honest correction to my own work.** My first harness wrapped the flow in its own padding and reported a 278px track at 320px. The accessibility lead challenged it, and was right: that is 40px of harness chrome. The real chain is `modal.tsx:55` overlay `p-4`, `modal.tsx:91` panel `w-full max-w-lg p-6`, `PayoutRequestFlow.tsx:388` `-m-6` cancelling that padding, then the step content re-adding `px-6`, giving a 240px content column. The harness was rebuilt to mount inside the real `<Modal>` and re-measured; the table above is the corrected one, and it matches the lead's independent derivation to the pixel.

### The gross is kept, clearly labelled as the deduction, and here is why

The brief warns against adding numbers until the screen is cluttered, and step 2's header already says `Withdrawing $30.44 from <campaign>`. **It stays anyway**, for a reason that only shows up on a phone: the panel is `max-h-[85vh] overflow-y-auto` and step 2 carries two large speed cards, so **at 320px that header has scrolled out of view by the time the control is on screen**. A figure you have to scroll back for is not reviewable at the one irreversible point in the flow. In the summary block the deduction also stops being a stray fourth number and becomes the second half of one statement: what you get, and what it costs you.

### The diff, code only

```diff
- const [speed, setSpeed] = useState<Speed>("STANDARD");
+ const [speedChoice, setSpeedChoice] = useState<Speed>("STANDARD");
+ const speed: Speed = expressLockedBySolana ? "STANDARD" : speedChoice;
+ const netForSpeed = speed === "EXPRESS" ? expressNet : standardNet;

- <fieldset className="space-y-3">
+ <fieldset
+   className="space-y-3"
+   aria-describedby={expressLockedBySolana ? `${errId}-express-lock` : undefined}
+ >

- onSelect={() => { if (expressLockedBySolana) return; setSpeed("EXPRESS"); }}
+ onSelect={() => { if (expressLockedBySolana) return; setSpeedChoice("EXPRESS"); }}
- onSelect={() => setSpeed("STANDARD")}
+ onSelect={() => setSpeedChoice("STANDARD")}

  <SwipeToConfirm
    handleRef={swipeHandleRef}
-   amountLabel={formatCurrency(amountNum)}
+   receiveLabel={formatCurrency(netForSpeed)}
+   deductLabel={formatCurrency(amountNum)}

- function SwipeToConfirm({ handleRef, amountLabel, busy, errored, onConfirm }: {
-   amountLabel: string;
+ function SwipeToConfirm({ handleRef, receiveLabel, deductLabel, busy, errored, onConfirm }: {
+   receiveLabel: string;
+   deductLabel: string;

+ const summaryId = useId();

- const labelOpacity = Math.max(0, 1 - (fillPct / 100) * 1.8);
- const labelText = busy ? "Requesting your payout" : done ? "Confirmed"
-                 : `Swipe or hold to request ${amountLabel}`;
+ const labelLeftPct = maxTravel > 0 ? (56 / (maxTravel + HANDLE)) * 100 : 100;
+ const labelOpacity = Math.max(0, 1 - fillPct / (labelLeftPct * 0.9));
+ const labelText = busy ? "Requesting" : done ? "Confirmed" : "Swipe to confirm";

+ <div id={summaryId} className="mb-2 space-y-0.5">
+   <div className="flex items-center justify-between gap-3">
+     <span className="text-sm font-semibold text-[var(--text-primary)]">You receive</span>
+     <span className="text-lg font-bold tabular-nums text-accent">{receiveLabel}</span>
+   </div>
+   <p className="text-xs text-[var(--text-muted)]">
+     <span className="tabular-nums">{deductLabel}</span> comes off your balance
+   </p>
+ </div>

-   className="... rounded-full border border-accent/30 bg-[var(--bg-input)]"
+   className="... rounded-full border border-accent/70 bg-[var(--bg-input)]"

-   className="... justify-center gap-1.5 px-14 text-sm font-bold text-white ..."
+   className="... justify-center gap-1.5 pl-14 pr-4 text-sm font-bold text-white ..."

- aria-label={`Swipe or hold to request ${amountLabel}, or press Enter to confirm`}
+ aria-label={busy || done ? labelText : "Swipe to confirm, or press Enter"}
+ aria-describedby={busy || done ? undefined : summaryId}

  // SpeedCard: the lock reason leaves the <label> it was being folded into
- <label className="relative block cursor-pointer">
+ <div className="relative">
+ <label className="relative block cursor-pointer">
-   aria-describedby={locked && lockedId ? lockedId : undefined}
-   </label>  (reason was inside)
+   </label>
+   {locked && lockedReason && (<p id={lockedId}>…</p>)}
+ </div>
```

### A latent state bug found while reading, and fixed

`speed` was React state that persisted across step changes. So a clipper could pick EXPRESS, go back, lower the amount until Solana's threshold locked express, and return to step 2 where **three things disagreed at once**: the Express card rendered unselected (its `selected` prop already ANDs in `!expressLockedBySolana`) so **neither radio was checked**, the net displayed was the wrong one, and `confirmRequest` still posted `EXPRESS` to a server that correctly refuses it with a 400.

Deriving `speed` fixes all three read sites in one place. **The choice is kept rather than reset**, because BL-556 explicitly refuses silent reselection: a reset would destroy the clipper's express choice permanently, so raising the amount again would silently leave them on Standard.

---

## PART 2 — EVERY SCREEN AND MESSAGE IN THE PAYOUT JOURNEY

Twenty three surfaces walked. Each is marked with which figure it shows.

| # | surface | file:line | shows | verdict |
|---|---|---|---|---|
| 1 | step 1 amount input, `Amount to withdraw` | `PayoutRequestFlow.tsx:503` | GROSS | correct, it is what leaves the balance |
| 2 | step 1 Max chip accessible name | `:551` | GROSS available | correct |
| 3 | step 1 minimum hint | `:538-541` | GROSS threshold | correct, the gate compares gross |
| 4 | step 1 Solana hint, `sends $27.70 after fees` | `:653` | CASH | correct |
| 5 | step 2 header, `Withdrawing $30.44 from` | `:691` | GROSS | correct |
| 6 | step 2 Express card, `You receive` | `:722-723` | CASH | correct |
| 7 | step 2 Standard card, `You receive` | `:737-738` | CASH | correct |
| 8 | step 2 express lock, `Express would send` | `:716` | CASH | correct |
| **9** | **step 2 SWIPE CONTROL** | **`:759`, `:1103`, `:1126`** | **GROSS** | **THE BUG. FIXED** |
| 10 | step 3 success receipt | `:812-817` | both, itemised | correct |
| 11 | history table, header `Amount` over a NET cell | `payouts/page.tsx:602` | CASH, vague label | **relabelled `You get`** |
| 12 | legacy modal speed cards, bare accent figures | `payouts/page.tsx:993`, `:1015` | CASH, **no label at all** | **labelled `You receive`** |
| 13 | legacy modal breakdown | `:1040-1055` | both, itemised | correct |
| **14** | **`PAYOUT_APPROVED` notification** | **`review/route.ts:431`** | **GROSS** | **WRONG. FIXED** |
| **15** | **`PAYOUT_PAID` notification** | **`review/route.ts:447`** | **GROSS** | **WRONG, the worst one. FIXED** |
| 16 | `PAYOUT_REJECTED` notification | `review/route.ts:439` | GROSS | correct, nothing was sent |
| 17 | `sendPayoutApproved` email | `email.ts:600-610` | CASH | correct, and it **disagreed with 15** |
| 18 | `sendPayoutRejected` email | `email.ts:612` | GROSS | correct, `payout request of` |
| 19 | `sendPayoutReminder` email, `You have $X unpaid` | `email.ts:859` | GROSS balance | correct |
| **20** | **owner review row headline** | **`admin/payouts/page.tsx:1281`** | **CASH, NO LABEL** | **BL-763's trap. FIXED** |
| 21 | owner unpaid tiles, `Net After Fee` | `admin/payouts/page.tsx:790`, `:841`, `:882` | CASH | correct, BL-133 did this |
| 22 | owner void confirm phrase | `admin/payouts/page.tsx:415` | GROSS, demands exactly what it shows | correct, BL-735 verified |
| 23 | referral cashout | `referral-request/route.ts:165` | **no fee at all**, gross equals cash | no trap possible |

### The second bug, which is larger than the reported one and lands after the money moves

`PAYOUT_PAID` said **`Your payout of $30.44 has been sent`**, interpolating `existing.amount`. The email sent in the same block already used `payoutLiability` and said **$26.48**. So the platform told the same clipper two different figures for one event, and the wrong one was the one that arrived in the app.

**Measured across the 93 PAID rows:**

| | |
|---|---|
| what the notifications claimed was sent | **$10,396.98** |
| what was actually sent | **$8,642.01** |
| **overstatement** | **$1,754.97** |
| worst single message | **$461.62** (a $725.62 request the owner adjusted down to $264.00) |
| `PAYOUT_PAID` notifications ever sent | **106** |
| `PAYOUT_APPROVED` notifications ever sent | 312 |

**Both now state the sent figure through `payoutLiability`, the same expression the email uses, so the two can never disagree again.** The new copy:

> **PAID:** `Your payout has been sent. You receive $26.48, from your $30.44 request. Please allow a few business days for it to arrive.`
> **APPROVED:** `Your $30.44 payout is approved and being processed. You receive $26.48 after fees.`

**One exception, guarded rather than glossed.** The auto-adjust path at `review/route.ts:242` rewrites `amount` and deliberately leaves `finalAmount` behind ("finalAmount/actualPaidAmount stay where they were"), so on that path alone the stored net belongs to the pre-shrink gross and would overstate again. There the cash is re-derived from the adjusted gross through `calculatePayoutBreakdown`, the same helper that produced the row. **That branch has never fired in production** (0 `PAYOUT_AUTO_ADJUSTED_FOR_STALE_REDUCTION` audit rows), so it is a guard, not a repair, and the ordinary path stays byte-identical to the email.

### The owner side, per BL-763

BL-763 caught the owner about to send $71.98 and $10.15 when $65.50 and $8.83 were owed. The review row was still the shape that invites it: a **bare, unlabelled** bold number, with `$20.67 req -$1.86 -$0.83 exp` underneath.

**Before:** `smokyy Zhus Meme (0.20 CPM) $17.98 EXPRESS +4% OVERDUE 7D $20.67 req -$1.86 -$0.83 exp`
**After:** `smokyy Zhus Meme (0.20 CPM) SEND $17.98 EXPRESS +4% OVERDUE 7D $20.67 requested -$1.86 fee -$0.83 express`

The column header moved from `Amount` to **`Net to send`**, the cell gained the word **`Send`**, and `req` / `exp` are spelled out. No per-cell `sr-only` sentence was added: the information is column-invariant, so it belongs in the header once rather than repeated across ten columns on every row.

---

## PART 3 — THE MONEY DID NOT MOVE

**`payout-calc.ts` is not in the diff.** Nor is any of the six money files. The change touches display strings, one derived variable and two notification sentences.

**Proven on real data.** All eight live open payout rows were re-derived through `calculatePayoutBreakdown` and compared against what is stored:

```
cmsv1ifo  EXPRESS   gross   $60.27  stored cash   $52.44  re-derived   $52.44  IDENTICAL
cmq084lz  STANDARD  gross   $57.58  stored cash   $52.40  re-derived   $52.40  IDENTICAL
cmsnvqqn  STANDARD  gross   $46.51  stored cash   $42.32  re-derived   $42.32  IDENTICAL
cmst92ua  STANDARD  gross   $24.56  stored cash   $22.35  re-derived   $22.35  IDENTICAL
cmsul7p1  STANDARD  gross   $21.00  stored cash   $19.11  re-derived   $19.11  IDENTICAL
cmsl8dbu  EXPRESS   gross   $20.67  stored cash   $17.98  re-derived   $17.98  IDENTICAL
cmsuku4g  STANDARD  gross   $20.29  stored cash   $18.46  re-derived   $18.46  IDENTICAL
cmsq04pf  EXPRESS   gross   $10.00  stored cash    $8.70  re-derived    $8.70  IDENTICAL
```

**And exhaustively**, across every amount from $10.00 to $2,000.00 at both fee rates, 380,000 checks: express is always 4% on top and never instead, the base fee never changes between speeds, express cash never exceeds standard cash, and cash never exceeds gross. **0 violations.**

Live totals, before the round and after it, identical:

| | before | after |
|---|---|---|
| payout rows | 172 | **172** |
| Σ gross `amount` | $15,714.34 | **$15,714.34** |
| Σ express premium | $180.56 | **$180.56** |
| payouts touched in the round window | | **0** |
| earnings invariant violations | 0 | **0** |
| approved live clips | 4,913 | 4,913 |

**BL-696's no-double-pay survives:** this round adds no payout creation path, does not touch the Serializable transaction, the ten-second dedupe or the `uq_payout_open_per_user_campaign` partial unique index. **BL-627's no-overpayment survives:** no term in `earned − paid − locked` was touched, and `balance.ts` is byte-identical.

---

## PART 4 — RENDERED AND MEASURED

BL-793's method: real Chromium, the CSS viewport set through `browser.newContext({ viewport })`, `next dev --webpack`, and `window.innerWidth` read back and asserted every time. Run **on the merged main tree**, not only on the branch. **150 assertions, 0 failures, exit 0.**

Three cases at five widths, each with Standard and then Express selected: the owner's **$30.44 at 9%**, the real live **$60.27 express row**, and a **referred clipper at 4%**.

**The owner's case at 320px, read out of the DOM:**

```
STANDARD control text : "You receive $27.70 $30.44 comes off your balance Swipe to confirm"
EXPRESS  control text : "You receive $26.48 $30.44 comes off your balance Swipe to confirm"
track label           : "Swipe to confirm"   box 116px for 116px, track 238px
handle name           : "Swipe to confirm, or press Enter"
handle description    : "You receive $27.70 $30.44 comes off your balance"
```

**Before, for comparison, measured the same way:**

```
swipe visible : "Swipe or hold to request $30.44"
swipe aria    : "Swipe or hold to request $30.44, or press Enter to confirm"
CHANGED when switching to Express? false
```

Asserted at every width, for every case:

| assertion | result |
|---|---|
| the STANDARD control shows the received figure | pass ×15 |
| the EXPRESS control shows the received figure | pass ×15 |
| **the control CHANGED when the option changed** | **pass ×15** |
| the gross is labelled as what comes off the balance | pass ×15 |
| the handle's description carries the same received figure, no dangling idref | pass ×15 |
| the accessible name contains the visible label (2.5.3) | pass ×15 |
| no money figure leaked into the accessible name | pass ×15 |
| the track label is not clipped | pass ×15 |
| exactly one speed radio is checked | pass ×15 |
| no sideways page scroll | pass ×15 |

**One honest note on the harness.** A fresh browser context per width made `next dev` recompile on every navigation and the run timed out part way through, which is the same load behaviour BL-809 recorded. It was restructured to one context per case with the viewport resized, and the committed script is the one that produced the 150/0 result, in its own follow-up commit, because a proof script that does not match its own output is not a proof.

### The `/campaigns/[id]` report control, and why this round did NOT fix it

**Stated plainly, as the brief allows.** This round did no sidebar work at all: its files are `PayoutRequestFlow.tsx`, the two payouts pages and the payout review route. The condition attached to the instruction ("while you are in the sidebar work") never arose.

More importantly, **it is a product decision the owner reserved and has not yet made.** BL-809's accessibility lead recommended keeping a fixed launcher on that one route; the owner's standing instruction was to remove every floating entry so nothing hovers over the page. Those conflict, and BL-809 put the question to him rather than picking. Nothing has changed that.

The cause, confirmed: `app-layout.tsx:1078` suppresses the entire mobile top bar on `/^\/campaigns\/[^/]+/`, and that bar carries the hamburger, so the drawer opens there by left-edge swipe only.

**Three candidate fixes, so the decision is one word rather than another round:**

1. **Bring back a fixed launcher on that route only.** Two lines. Directly contradicts the instruction that produced BL-809.
2. **Narrow the suppression so the bar renders with only the menu button.** One regex, no floating control, satisfies both instructions. But it puts a bar back on a drill-in surface where stripping all chrome was a deliberate BEHAVIOR B decision, and it needs its own render proof at five widths.
3. **Leave it.** The drawer still opens by the ordinary phone swipe gesture, and its rows are still in the tab order.

**Say which and it is a small round.** It was not taken unilaterally because every option overrides an instruction the owner gave deliberately.

---

## PART 5 — WHAT WAS MERGED

**A clean `tsc` baseline was recorded on the untouched worktree BEFORE any edit**, after `npm ci` exit 0 and `npx prisma generate` exit 0: **`tsc --noEmit` exit 0, `grep -c "error TS"` = 0.** So no error later needed attributing, and none appeared.

### On main now

| branch | SHA | merge commit | what it is |
|---|---|---|---|
| `checkpoint/BL-810` | `b415680e` | **`c3e2ed01`** | the owner liability dashboard |
| `checkpoint/BL-812` | `df187099` | **`a0e460e7`** | this round |
| (follow-up) | | **`b91364cf`** | the render harness as actually run, and the BACKLOG union resolver |

**`origin/main == local == b91364cf`**, verified by `git ls-remote`, which is the authority.

### BL-810, re-confirmed before merging and again after

It was genuinely unmerged: **not an ancestor of main, 12 files, +2,075 lines.** Re-checked on the branch and then proven on the merged tree by direct request:

```
OWNER     h1="Liability"  tables=1  money-strings=5  nav-link=true   GET /api/admin/liability -> 200
ADMIN     h1="404"        tables=0  money-strings=0  nav-link=false  GET /api/admin/liability -> 403
REVIEWER  h1="404"        tables=0  money-strings=0  nav-link=false  GET /api/admin/liability -> 403
CLIPPER   h1="404"        tables=0  money-strings=0  nav-link=false  GET /api/admin/liability -> 403
```

By grep on the merged tree: **0 write verbs** in its four files, **GET is the only exported HTTP verb**, `requireOwner` on the route, `notFound()` for any role but OWNER on the page, the nav entry appears **once in the whole sidebar and only inside `ownerNav`**, and **0 reads** of `agencyEarning`, `ownerCpm`, `agencyFee`, `clientName` or `aiKnowledge`. BL-531 holds.

### Conflicts, resolved as unions and counted

Two merges, **one conflicted file each, `BACKLOG.md` only**. `globals.css` and `sidebar.tsx` auto-merged cleanly even though BL-809 had edited the same sidebar file. Resolved by `scripts/bl812-union.py`, which keeps **both** sides of every hunk and then refuses to write if a marker survives or a section count drops:

```
conflict hunks resolved as unions : 1
conflict markers before / after   : 3 / 0
## BL- sections before / after    : 156 / 156
```

Counted with `grep -c`, **never piped to `head`**: **154 sections on main before, 156 after.** `BL-809` ×1, `BL-810` ×1, `BL-811` ×1, `BL-812` ×1, **0 conflict markers**.

### BL-723, and the 103 branches that did NOT get merged

**`checkpoint/BL-723` was excluded by instruction and is confirmed not an ancestor of main.**

"Everything left" needed a number, so here it is. **105 checkpoint branches were unmerged at the start of this round.** Classified by whether they carry anything other than markdown:

| | count |
|---|---|
| **documentation only** (an audit report and nothing else) | **93** |
| carry non-markdown files | 12 |
| of those: merged this round | 2 (BL-810, BL-812) |
| of those: excluded by instruction | 1 (BL-723) |
| **of those: left unmerged** | **9** |

**The 93 doc-only branches were not merged deliberately.** Their reports already live in `ilenader/clippershq-reports`; merging them would add roughly a hundred stale audit markdown files to the application repository and change no behaviour. That is not what "everything left" can sensibly mean.

**The 9 code-carrying branches, named so the owner can decide rather than wonder:**

| branch | date | what it is |
|---|---|---|
| `BL-351` | 2026-07-11 | redesigned clip card polish |
| `BL-493` | 2026-07-14 | owner growth transparency and preview centre |
| `BL-524` | 2026-07-16 | growth dashboard wording |
| `BL-681` | 2026-07-29 | REQUIRED_SOUND readiness audit |
| `BL-704` | 2026-07-31 | round report plus scripts |
| `BL-745` | 2026-08-09 | Instagram submit-time views |
| `BL-749` | 2026-08-09 | zero-stat population |
| `BL-785` | 2026-08-12 | three-line owner-submit fix |
| `BL-802` | 2026-08-13 | partner reviewer scoping SQL |

**None was merged.** Each was left unmerged by its own round for its own reason, several are five weeks stale against a main that has moved a long way, and merging nine of them blind inside a payout-labelling round is exactly the change CLAUDE.md tells an agent to stop and explain rather than perform. **Name any of them and it is a merge round with its own build and its own proof.**

---

## PART 6 — THE AVG CPM MOVE, ANSWERED WITH ARITHMETIC

BL-809 reported the tile moving from **$0.05 to $0.46** and flagged it for investigation. **It is a CORRECTION, not a defect, and the ninefold factor is exactly reproducible.**

### The denominator has ALWAYS been every campaign

When nothing is selected the page sends **no** `displayedCampaignIds` (`analytics/page.tsx:302-307` sets it only inside `if (selectedCampaigns.length > 0)`), and the route then defaults it at **`src/app/api/admin/analytics/summary/route.ts:134-136`** to *every campaign id present in the clip dataset*, which is fetched with `includeArchived=true`. So past campaigns' views were in the denominator all along. **Each campaign's views are counted once. There is no double count.**

### The arithmetic, from live data

Denominator, approved live clips excluding `videoUnavailable`, latest stats views:

| scope | views |
|---|---|
| **all campaigns** | **36,588,240** |
| non-archived (the 14 now selectable) | 36,265,145 |
| the old selector scope (5 ACTIVE or PAUSED) | **3,910,665** |
| PAST, non-archived | 32,354,480 |
| archived only | 323,095 |

Numerator, clip side filtered plus agency side unfiltered, the `/api/campaigns/spend` shape BL-642 documented:

| scope | spend |
|---|---|
| all campaigns | $17,159.56 |
| **non-archived (14)** | **$16,742.99** |
| **the old selector scope (5)** | **$1,901.38** |
| archived only | $416.57 |

```
OLD tile   $1,901.38 / 36,588,240 x 1000 = $0.0520
NEW tile  $16,742.99 / 36,588,240 x 1000 = $0.4576

the jump   36,588,240 / 3,910,665 = 9.36x
```

**The ninefold move is precisely the ratio of the denominator's scope to the old numerator's scope.** BL-809's figures ($1,893.90 and $16,735.51) reproduce with the same $7.48 of accrual on both sides, which is itself a consistency check.

### What the owner was previously being shown

**$0.05 per 1,000 approved views**, on a tile captioned "lifetime spend per 1,000 approved views". The truth is about **46 cents**. He was under-reading his own cost of acquisition by roughly an order of magnitude, because the tile was dividing all-campaign views into five-campaign spend.

### The residual, named with file:line, specified and NOT changed

The numerator is `displayedCampaigns` (`analytics/page.tsx:465-467`), built from `allCampaigns`, which **excludes archived campaigns**. The denominator includes them. So **323,095 views and $416.57 of spend sit on opposite sides of the fraction**, and the tile now **understates by 2.4%**.

Two candidate fixes give **different answers**, which is why this is specified rather than done:

```
narrow the denominator to the same 14   $16,742.99 / 36,265,145 x 1000 = $0.4616
widen the numerator to all 34           $17,159.56 / 36,588,240 x 1000 = $0.4690
```

BL-809 already put the archived-campaign question to the owner, noting that folding archived campaigns into the selector also moves the "Active campaigns" tile from 3 to 16 unless that tile is fixed in the same round. **Only he can say which figure he means**, and this round's own safety rule forbids moving a calculated number. Say the word and it is one line.

---

## PART 7 — THE EVIDENCE

| claim | evidence |
|---|---|
| **the control shows what they receive, and it changes** | 320px, owner's case: `"You receive $27.70 … Swipe to confirm"` becomes `"You receive $26.48 …"` on Express. `CHANGED` asserted at **15 of 15** width-and-case combinations |
| the gross is still shown, unmistakably labelled | `$30.44 comes off your balance`, asserted present at every width |
| every other payout surface is labelled correctly | 23 surfaces walked in PART 2; 5 fixed, 18 already correct or correct by construction |
| **the received amount is unchanged to the cent** | 8 live open rows re-derive IDENTICAL; 380,000 exhaustive checks, 0 violations; `payout-calc.ts` not in the diff |
| **no double pay, no overpayment** | BL-696's index, transaction and dedupe untouched; BL-627's subtraction untouched; `balance.ts` byte-identical |
| the Avg CPM question answered | `36,588,240 / 3,910,665 = 9.36`, a correction; residual 2.4% named at `summary/route.ts:134-136` and `analytics/page.tsx:465-467` |
| **both branches merged** | BL-810 `b415680e` via `c3e2ed01`, BL-812 `df187099` via `a0e460e7`; `origin/main == b91364cf` by `ls-remote`; BL-723 confirmed not an ancestor |
| renders at all five widths, both options | **150 assertions, 0 failures**, on the merged main tree |
| BL-810 is owner only on the merged tree | OWNER 200 with the table; ADMIN, REVIEWER and CLIPPER each get the 404 view, 0 tables, 0 money strings, no nav link, and **403** from the route |
| **no clip's earnings or status changed** | 4,913 approved clips before and after; this round issued no clip write of any kind |
| **no payout created, modified, approved or cancelled** | 172 rows, Σ gross $15,714.34, Σ express $180.56, all identical; **0 payouts with `updatedAt` in the round window** |
| **the earnings invariant** | **0 violations**, before and after |
| the 6 money files plus `tracking.ts` and `campaign-era.ts` | **byte-identical by blob OID** on `c94dc229` and on merged `HEAD`: `ac5be7de`, `797e2098`, `e887f80a`, `83ce4bab`, `61cef393`, `ef5cdae7`, `106e16ad`, and `payout-calc.ts` `029834b4` |
| BL-678 guards | **18 `APIFY_HARD_OFF` references intact**, no Apify actor run |
| schema | **no change, no `prisma migrate`**; `prisma generate` only |

> **A REDEPLOY ON RAILWAY IS REQUIRED BEFORE ANY OF THIS IS LIVE.** Main carries the fix and the liability dashboard; production does not.

---

## THE ACCESSIBILITY REVIEW, AND WHERE IT CORRECTED ME

Reviewed by the accessibility lead with specialists **before any code was written**. It returned **8 blocking items and all 8 are implemented.**

**It caught a real error in my own measurements, and I want that on the record.** I reported a 278px track at 320px; it derived 238px independently and said my figures were shifted one device class. I checked rather than argued, found my harness was wrapping the flow in its own padding instead of the real `<Modal>`, rebuilt it, and re-measured: **238px track, 102px label box, matching its derivation to the pixel.** Had I shipped on my own number I would have chosen a string that still truncated at 320.

1. **Zero radios checked in the locked state (4.1.2).** The shadowed `speedChoice` plus a derived `speed`, so all three read sites are fixed at once.
2. **The accessible name must track the phase strings (2.5.3).** The name was static while the visible label became `Requesting` and then `Confirmed`, and `Confirmed` is not transient.
3. **Money out of the truncating span (1.4.10).** `pl-14 pr-4`, and the truncating span carries the instruction only.
4. **Money in `aria-describedby`, not in the name (2.5.3, 1.3.1).** A name identifies, a description elaborates, so 2.5.3 cannot silently break when the money copy changes later. The summary is **not** `aria-hidden`: hiding it would fail 1.3.1 for browse-mode and braille users.
5. **`lockedReason` leaves the `<label>` (4.1.2).** A label's accessible name is its entire text content, so a thirty word refusal was being folded into the radio's name and then repeated. Flagged by BL-811's review and fixed now rather than carried again.
6. **That `aria-describedby` moves to the `<fieldset>` (1.3.1).** Once the derived `speed` checks Standard, roving tabindex takes the locked Express option out of the tab order entirely, so a description on that input is unreachable by Tab.
7. **The track border was invisible (1.4.11).** `border-accent/30` composited to **1.55:1**, on the one control where travel distance *is* the interaction. Now `/70`, **3.18:1** inside and 3.30:1 outside.
8. **The label washed out mid-swipe (1.4.3).** The fixed `1.8` multiplier left opacity at 0.58 when the fill reached the text at 320px, compositing white on accent at **1.81:1**. Keyed to `maxTravel + HANDLE` instead, so it is correct at every width, using the ResizeObserver that already exists and needing **no new state and no new effect**.

Also adopted: `Requesting` rather than `Requesting your payout` (166.11px against a 166px budget, truncating by 0.11px on font-load timing); `tabular-nums` on the figures only, never the prose; `text-lg` on the received figure to mirror the success receipt; and the `pl-14 pr-4` form written as two utilities because `cn` here is plain clsx with no tailwind-merge.

**Two rulings I asked for and accepted against my own plan.** No live-region announcement when the speed changes: the radio's own accessible name already contains `You receive $26.48`, so `setLiveMsg` would double-speak within about two seconds, and `liveMsg` is never cleared so a Standard-Express-Standard toggle would set an identical string and announce nothing anyway. And the deduction line stays rather than being dropped for tidiness, for the scrolled-header reason in PART 1.

**Reported, NOT fixed, and the owner should see it.** `PayoutRequestFlow.tsx:1116` hardcodes `text-white` against a themed `--bg-input`, which is **1.10:1 in the light theme**. It is currently unreachable because `toggleTheme` is destructured at `navbar.tsx:54` and never rendered, but it is a live trap the moment anyone wires that toggle up.

---

## GATES, HONESTLY

* **Clean baseline on the untouched worktree, BEFORE any edit:** `npm ci` exit **0**, `npx prisma generate` exit **0** (run before `tsc`, because `npm ci` wipes the generated client), `npx tsc --noEmit` exit **0** with `grep -c "error TS"` = **0**.
* **`eslint` confirmed present**, `npx eslint --version` reports **v9.39.4**, so the hooks gate is a real check and not a silent no-op.
* After the change: `npx tsc --noEmit` exit **0**, 0 errors, unchanged from baseline.
* `npm run build` **twice**, both from a log with the exit code echoed by hand and **never piped through `tail`**: **`BUILD1_EXIT=0`** on the branch (compiled in 53s) and **`BUILD2_EXIT=0`** on the merged tree (compiled in 76s). Prebuild clean both times: `check:prisma-bypass` **0 violations**, `check:removed-fields` **OK across 728 files**, hooks gate **11 problems (0 errors, 11 warnings)** at the ceiling of 11 with **zero added** (the fix introduces no new hook: `useId` is not an effect and the derived `speed` needs no dependency array).
* Both `/admin/liability` and `/api/admin/liability` appear in the merged build's route table as dynamic.
* `scripts/bl812-amounts.ts` **12 passed, 0 failed, exit 0**. `scripts/bl812-render.ts` **150 passed, 0 failed, exit 0**.
* Counted with `grep -c`, **never piped through `head`**. **No heredocs**: every multi-line file was written with the file-write tool, including the two patch scripts and the union resolver.
* The render harness route is **NOT committed**; its full source is in this round's commit history note and reproduced by `scripts/bl812-render.ts`'s header. A route that renders a payout flow with mock money has no business shipping.

---

## WHAT COULD NOT BE MEASURED, AND WHY

* **Whether a real screen reader speaks the new control as intended.** The markup is measured, the accessible name and the resolved `aria-describedby` text are read back out of the DOM, and there is no dangling idref. NVDA, JAWS and VoiceOver were not run.
* **The auto-adjust notification branch was not exercised.** It has never fired in production (0 audit rows), so the guard added there is reasoned from the code path rather than observed.
* **The express-locked-by-Solana state was not driven end to end in a browser.** The derived `speed` is proven by the "exactly one radio checked" assertion at every width, but the specific sequence (pick Express, go back, lower the amount below the Solana threshold, return) was not walked, because it needs a Solana address in the form and the harness ships an ERC-20 one.
* **Nothing was verified against production.** Every role probe ran locally against the merged tree with the dev-auth bypass. The gates are the same code that runs in production, but no authenticated request was made against clipershq.com and none is claimed.

---

## VERIFICATION AND SAFETY

Display and labelling only. **Seven files changed** across the round: `PayoutRequestFlow.tsx`, `payouts/page.tsx`, `admin/payouts/page.tsx`, `api/payouts/[id]/review/route.ts`, `BACKLOG.md`, and two scripts.

**No clip's earnings or status changed. No payout was created, modified, approved, cancelled or paid. No balance was touched. No schema change and no `prisma migrate`; `prisma generate` only. No Apify actor ran and the 18 `APIFY_HARD_OFF` references are intact.** The earnings invariant reads **0 violations** before and after. The 6 money files plus `tracking.ts` and `campaign-era.ts` are **byte-identical by blob OID** on both refs, and `payout-calc.ts` is byte-identical too and absent from the diff.

Every figure in this report traces to the query or the script that produced it. Every timestamp is cast `::text` against DB `now()`. Handles are redacted and **no wallet address is printed**. **NO dashes as bullets.** The worktree `C:/w812` was removed.

**Rollback:** `git revert -m 1 a0e460e7` for this fix and `git revert -m 1 c3e2ed01` for the liability dashboard, or `git reset --hard pre-BL-812-merge`. **Nothing in the database needs undoing.**
