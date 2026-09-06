# BL-843 — the trainer cashout, and every trainer figure made true

Round of 2026-09-06. Branch `checkpoint/BL-843`, worktree `C:/w843`.

BL-835 built the trainer commission ledger; BL-840 proved its arithmetic exact and named the hole:
**nothing in the product ever set a commission to PAID or ever wrote `trainerPayoutRequestId`.** A trainer
could accrue forever and never be paid. The column, the FK, the relation `TrainerCashoutPayouts`, the
`PAID` status and three display surfaces were all already there, waiting for a write that did not exist.
Production holds **0 trainers, 0 pairings, 0 commissions and 0 payouts carrying a cut**, so nothing here
could move a real person's money. Read off the database, not hoped.

## PART 1 — `POST /api/payouts/trainer-request`

**IT CREATES AN ORDINARY `PayoutRequest` AND HANDS IT TO THE ORDINARY OWNER WORKFLOW**, at REQUESTED, so
it appears in the existing list with no new screen. Reused verbatim: `calculatePayoutBreakdown`, the same
function the clipper's withdrawal uses; `referredById ? 4 : 9`, character for character from
`payouts/route.ts:452`; `validateWalletForChain`, then `validatePayoutMethod` against the NET, then a
re-check against the CANONICAL chain, the ordering BL-556 fixed because `"ERC20"` skipped format
validation entirely; `encryptWalletFields` inside the transaction; `PayoutRefusal` (BL-689). Approval,
payment, the notification, the email and the audit row are the existing route, untouched.

**FIVE THINGS GENUINELY DIFFER.** (1) **The fee** — `payouts/referral-request` charges nothing:
`finalAmount: total, // commissions have no platform fee`. (2) **PENDING at request, PAID only when
paid** — the referral cashout stamps PAID at request time and its reversal cascade keys on
`sourcePayoutRequestId`, which matches nothing on a cashout, so a rejected referral cashout strands its
commissions stamped PAID forever against a payout never sent. (3) **One open cashout at a time, checked in
code**, because `uq_payout_open_per_user_campaign` is partial on `("userId","campaignId")` and Postgres
treats NULLs as distinct, so it constrains this not at all; the real guarantee is the PENDING flip inside
a Serializable transaction. (4) **The platform minimum, $10** — every existing minimum is per campaign and
`belowMinimumMessage` is wired to a campaign name that would not exist. (5) **No express.**

**THE TRAINER PAYS THE 9 PERCENT ON THEIR OWN WITHDRAWAL, GROSS AND CASH, ON A REAL ROW:** gross $100.10,
fee $9.01, cash $91.09, asserted as `$100.10 less $9.01 = $91.09` against the stamped row.

## PART 2 — one press, and a correction of the question

**STOPPING A SILENT TRAINER'S MONEY IS ALREADY ONE PRESS AND WAS BEFORE THIS ROUND.** BL-840 said it
needed two; that was wrong. DEMOTE stops it three ways over, none new: no further cut mints, because the
gate reads `isTrainer` off the live row at `payouts/[id]/review/route.ts:928`; a cut already taken from a
clipper on a payout in flight is REFUNDED to that clipper on the same gate; and the cashout route refuses
a non-trainer. Measured: `HTTP 200` with no typed phrase, then `HTTP 403` on the cashout, and a fresh $300
withdrawal after demotion **minted no commission at all**, so nothing was taken from the clipper to need
refunding and they kept their whole after-fee pay.

**WHAT IS LEFT IS ONE DIFFERENT DECISION, NOW UNMISSABLE.** Money already on the ledger is frozen and
nobody can reach it. The receipt reads *"ONE THING IS LEFT: $22.75 before fees, $20.70 after, is frozen"*
with the two ways out, and it appears again on `/admin/liability` as a row reading "No, settle this". The
old message opened "THIS IS NOT FINISHED" over the accrual, which was false, and was keyed on the PAIRING
count while claiming something about MONEY, so an open pairing with no commission printed that over $0.00.

## PART 3 — the four figures that were lying

- **The rate.** "You get 10 percent of what they take out." Ten percent of $1,000 is $100; the trainer
  gets $91. BL-835 corrected this on the clipper's side and it was never applied here, so two screens
  stated two rates about one sum. Now the clipper's own wording.
- **"Ready to take out" carried the GROSS** on a column whose name promises what arrives.
- **The three money columns did not tile.** "You earned" counts AVAILABLE + PENDING + PAID; the others
  counted one state each, so a cashout in flight left the row short by exactly the amount asked for with
  nothing naming the gap. Before this round no row could be PENDING, so they tiled by accident. A fourth
  column closes it, with a visible sentence saying the three add to the first.
- **The consent panel was $5.00 wrong for every referred clipper**, in the sentence they tick a box
  against: they pay 4 percent, so 100 − 4 − 9.10 = **$86.90**, not $81.90. `CONSENT_COPY.cost` is now
  `costFor(wasInvited)`; `/api/trainer/me` answers `wasInvited` as a **boolean**, never an inviter's id.

**THE OWNER'S HUB.** "Not cashed out yet" summed AVAILABLE + PENDING, so money already cashed out read as
money the trainer still had to act on. Split into "Theirs to cash out" and "On a cashout, waiting for
you", both "before fees". The refund cards gained the line they lacked: "These two are exact. No fee comes
off them." Every other figure there is gross, so a reader who had learnt that rule would have sent a
clipper less than they are owed.

**NOTHING CAN BE STALE.** The cashout figures are derived on every read by the SAME helper the route
charges with, on the same rows. Nothing is cached or stored, so there is no copy to go stale. A failed
read returns `null`, never `0`.

## PART 4 — the owner's overview, on the existing surface

`/admin/liability` gains a **Trainer commission** section: owed, requested and paid, each gross AND cash,
plus a per-trainer table with a "Still a trainer" column. A separate bucket for a structural reason: the
cut is a stamped deduction on a payout row and `Clip.earnings` is never touched by any trainer path.
**Before this round it was in none of the page's totals, which was the defect** — null-campaign payouts
are skipped by the two `campaignId` filters in `liability.ts`, so a cashout was invisible and the page
understated what the owner owed. The three states are disjoint because a row holds one status. PENDING and
PAID cash comes off the payout's **stamped `finalAmount`**, summed once per payout; only AVAILABLE is
projected, because no row exists yet. The projection names what it omits: `cashFor` does not pass the
trainer argument, so a clipper WITH a trainer has projected cash overstated by up to ten percent, not
guessed because the cut depends on which clips fall inside a window. It errs toward setting aside too
much, and the page says so.

## PART 6 — the sandbox: 61 checks, 61 passed, 0 failed

Production build on port 3843, `DEV_AUTH_BYPASS=false`, real minted `__Secure-authjs.session-token`
cookies, and **every account minted by this round including the owner** — BL-842 found and this round
confirmed that `findFirst({role:"OWNER", isTestUser:true})` resolves to the REAL owner, so a fifth lock,
`sandboxOnly()`, refuses to mint a session for any id without the `bl843sbx-` prefix.

**THE FULL LOOP.** c1 withdraws $1,000: fee $90.00, cut $91.00, cash $819.00. c2 withdraws $100: cut
$9.10. The trainer accrues $100.10 across two trainees, all AVAILABLE, cashes out at $100.10 → $9.01 →
$91.09 with the commissions PENDING and linked, then PAID only on payment. **Every cent conserves three
ways:** clipper leg `$900.90 + $99.00 + $100.10 = $1100.00`; trainer leg `$91.09 + $9.01 = $100.10`;
nothing from nowhere `$900.90 + $91.09 + $108.01 = $1100.00`.

**SEVEN FAILURE CASES.** Under the minimum, refused with the shortfall named ("you need $5.45 more").
Asking for more than accrued is **impossible by construction**: `amount: 999999` in the body was ignored
and the gross was the ledger's own $22.75. Asking twice: 409 `TRAINER_CASHOUT_ALREADY_OPEN`. A bad-faith
revoke landing on an open cashout: 409 `TRAINER_CASHOUT_OPEN`, pairing `ACTIVE to ACTIVE`, 0 refund rows.
Turning a cashout down returns the money to AVAILABLE with the link cleared and they can ask again.
Good-terms wind-down refunds nobody and stamps `ENDED_OWNER_WINDDOWN`. Bad-faith revoke refunds 2 of 2,
one refund row per commission.

**THE BOUNDARY, GREPPED OVER THE REAL BYTES.** A stranger's id, username and clip id all absent from the
trainer's payload; a clip posted before the join absent; **0 of 25 forbidden field names present**; a
clipper refused the cashout 403; a non-trainer refused the dashboard 403. BL-627, BL-696 and BL-824 hold:
0 invariant violations, 0 rows claimable after payment, `$1650.00 recorded against $1650.00 written`.

**AND IT IS GONE.** 90 deleted, 4 cascaded, **0 of 94 recorded rows remain.** `real_payout_fp`
`346bb94e…` and `real_user_fp` `b9da9c47…` byte-identical before and after; trainer tables back to 0;
`audit_logs` back to 27091 exactly; `referral_commissions` still 7; invariant 0 both sides; 0 Supabase
pool errors. Three counts moved by exactly +1 — clips, clip_stats, tracking_jobs — and that is **a real
clipper submitting a real clip at 13:58:45 mid-window**, not mine, named rather than smoothed.

## PART 7 — render: 20 shots, 220 assertions, 220 passed, 0 failed

320, 375, 414, 1280 and 1440 with `window.innerWidth` printed beside every shot: **0 at the wrong width,
0 with horizontal overflow.** The cashout disclosure was **pressed open** on every shot, because a closed
disclosure proves nothing about the form inside it; the SEND button was never pressed, because pressing it
moves money. Four surfaces: the trainer's cashout, `/admin/liability`, `/admin/trainers`, and the
clipper's own page, where exactly one worked example renders and no inviter id appears anywhere.

## Defects found that the brief did not name

- **A cashout minted a fresh referral commission to the recipient's inviter**, compounding commission on
  commission. Guarded on `campaignId == null`. **Measured: 31 null-campaign payouts exist, 0 ever PAID, so
  it never fired — 0 rows, $0.00.**
- **A pre-existing DEAD BRANCH, found by running the route rather than reading it, REPORTED not changed.**
  In `payouts/[id]/review/route.ts` the chain begins `if (action === "APPROVED")` and its second arm is
  `else if (action === "REJECTED")`, so the arm far below reading `else if (action === "REJECTED" || action
  === "VOIDED")` **cannot run for a rejection** and fires only for VOIDED. That makes the
  F-REFERRAL-COMMISSION void cascade dead code for every rejected payout, and it is on `main` today.
  Measured: 56 REJECTED payouts, 0 referral commissions on a REJECTED or VOIDED source, so nothing lost
  yet. **My own return-to-AVAILABLE was first written into that same arm and the sandbox failed three
  checks over it**, which is the entire reason the loop is run against real rows; it now lives in its own
  reachable `if`. Reordering another feature's branches was left as your decision.
- **`trainer-window.ts` carried my own BL-840 miss**: `pairingCoversDay` gated a display question on the
  CHARGING status, a second copy of a bug BL-840 fixed in one file.
- **`SOLANA_MIN_NET_USD` and the chain wire values are imported, not re-typed.** `payout-methods.ts`
  forbids re-declaring 12 and warns that storing the label `"ERC-20"` silently disables address
  validation. The radio group sends `CHAIN_ERC20` and displays "ERC-20".

## Accessibility

The first pass, before any UI existed, killed the modal: the shared `Modal`'s scroll lock is a no-op
because this app scrolls on `<main>`, its scrim carries no `data-no-swipe` inside an 80-percent swipe zone,
and a `title` renders its close button OUTSIDE the focus trap. The second pass, on the written code,
returned **13 blocking items and every one is implemented.** Worth naming: a successful send unmounted the
button holding focus and dropped it to `<body>`, so the receipt paragraph catches it and announces both
figures; the error announced twice in two wordings, and an identical second failure would have announced
**nothing at all**; "Less the 9 percent fee" beside a bare amount reads just as easily as the NET;
`aria-describedby` sat on a disabled radio focus can never reach; **two unrelated fees were both called
"fees" four inches apart** on the screen of the person being paid, undoing the rate correction directly
above; and six `--text-muted` uses rendered fine print at full white, that token being `#ffffff`.

## Safety and honesty

**No schema change at all.** `trainerPayoutRequestId String?` and the relation were already on `main` at
`prisma/schema.prisma:1604`, and the column is confirmed present and nullable in the live database.
Nothing to run in the SQL editor. No `prisma migrate`, no index, no Apify actor, the 11 BL-678 guards
untouched. The 6 money files plus `campaign-era.ts`, `payout-calc.ts` and `apify.ts` byte-identical by
blob OID on both refs. `npm run build` exit 0 pre-commit, hooks gate 0 errors and 10 warnings against a
ceiling of 11, `tsc` exit 0 with 0 errors, eslint v9.39.4 confirmed present so the gate is a real check.

**Two mistakes of mine, recorded so they are not repeated.** A kill line written as `taskkill //IM
node.exe` with a window-title filter matched nothing and killed nothing, which was luck: had the filter
worked it would have taken out every node process on this machine including a peer session's server. It is
now by PID from the port. And I edited a running `.sh` driver, which bash re-reads incrementally, so the
run died at a bogus syntax error minutes in, after its build had already succeeded. The phases are now run
directly.

**Requires a Railway REDEPLOY.**
