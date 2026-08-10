# BL-763 — two payouts auto-voided six days ago, still unpaid

**2026-08-10 · DB `now()` = `2026-08-10 17:09:45.589620+00` · AUDIT ONLY, READ ONLY.**
No code, data, schema, config or money changed. No payout un-voided, approved, created, cancelled or
paid. No balance touched. No campaign un-archived. No Apify actor, no paid probe, spend $0.00. Base
`origin/main` @ `018c22ca`, isolated worktree `C:/m763`, removed at exit. Every timestamp cast `::text`
against DB `now()`. Handles redacted, no wallet address selected or printed.

**Clipper A** = `cmq7qh6p` · **Clipper B** = `cmrq9r65`. The owner can map these privately in admin.

---

## THE ANSWER, BEFORE THE WORKING

> **Pay $65.50 to Clipper A and $8.83 to Clipper B. Not $71.98 and $10.15.** Those are GROSS figures
> carrying the 9% fee, and Clipper B's also carries a 4% express fee that BL-732 did not name.
> **Sending the gross overpays by $7.80 across the two.**
>
> **But do NOT pay either of them by hand.** Unlike BL-760's case, this money IS still claimable in
> their balances, so a hand payment would sit alongside a live claim and could be requested a second
> time. They must request through the platform and be paid against that row.
>
> **Nothing is blocking them. They can both self-serve today.** The withdrawal gate contains no archive
> check and no campaign-status gate at all, `/api/earnings` does not hide archived campaigns, both are
> above the $10 minimum, and neither is clamped. **The only reason six days have passed is that nobody
> ever told them.** Zero payout notifications were sent to either clipper. That is the finding.
>
> **BL-733's fix holds.** Verified independently on current main: no executable path voids a payout on
> archive, no other status transition has the same shape, and both payout status paths write audit rows.

---

## PART 1 — WHAT EACH IS OWED TODAY, IN CASH

### The voided rows, field by field

| | **Clipper A** | **Clipper B** |
|---|---|---|
| Payout id | `cmsdtqi9` | `cms4pa6t` |
| Campaign | WinGram | WinGram |
| Requested | `2026-08-03 22:52:01.394` | `2026-07-28 13:37:26.029` |
| Voided | `2026-08-07 10:26:35.219` | `2026-08-07 10:26:35.219` |
| `rejectionReason` | "Campaign archived" | "Campaign archived" |
| **Gross `amount`** | **$71.98** | **$10.15** |
| Fee 9% (`feeAmount`) | $6.48 | $0.91 |
| **Express fee 4%** | **none** (STANDARD) | **$0.41** (EXPRESS) |
| **`finalAmount`, the CASH** | **$65.50** | **$8.83** |
| `paidAt` | **NULL** | **NULL** |
| Status now | VOIDED | VOIDED |

`71.98 − 6.48 = 65.50` and `10.15 − 0.91 − 0.41 = 8.83`, both exact.

**THE GROSS-VERSUS-CASH TRAP, WHICH BL-760 CAUGHT ABOUT TO BE MADE ON A DIFFERENT CLIPPER.** The admin
row showing "$65.50 available against a $71.98 request" is not a shortfall and not a defect. $71.98 is
what leaves the clipper's balance; $65.50 is what reaches his wallet. **The figure to send is the cash
figure.** Sending $71.98 and $10.15 would overpay by $6.48 and $1.32, **$7.80 in total**.

**Clipper B's express fee is new to this round.** BL-732 reported his row as "10.15 / 0.91 / 9 / 8.83"
and reconciled it correctly, but never said that $0.41 of the $1.32 gap is a 4% EXPRESS premium he
chose. It matters because it proves the two rows are not fee-symmetric, so no single percentage
applies to both. Clipper A is STANDARD at 9%; Clipper B is EXPRESS at 13% combined.

### Clipper A, independently computed

Earnings rebuilt from `clip_stats` views x each clip's own `cpmAtSubmissionDecimal`, applying
`calculateClipperEarnings` by hand (skip under 1,000 views; base = `min(views/1000 x stamp, 300)`;
bonus on the capped base; fee never subtracted at earnings time):

| campaign | status | clips | approved | genuinely earned | stored payable |
|---|---|---|---|---|---|
| STRAENGE | PAST | 26 | 25 | $115.33 | $94.53 |
| **WinGram** | **PAUSED + ARCHIVED** | **10** | **6** | **$74.53** | **$73.23** |
| Panic Baby | PAUSED | 12 | 12 | $47.58 | $46.51 |
| bees.n.honey | PAST | 9 | 7 | $20.73 | $20.72 |
| somesome | PAST | 2 | 1 | $7.89 | $3.73 |
| Zhus Meme | ACTIVE | 2 | 2 | $1.59 | $1.59 |
| SomeSome, Zhus Edit | | 3 | 2 | $0.00 | $0.00 |
| **TOTAL** | | **64** | **55** | **$267.65** | **$240.31** |

| | |
|---|---|
| Lifetime paid, by status | 2 PAID rows, **$112.00 gross** ($17.47 EXPRESS + $94.53 STANDARD) |
| Cash he has actually received | **$101.22** ($15.20 + $86.02) |
| **Current withdrawable, global** | **$128.31** (`$240.31 − $112.00`) |
| Withdrawable on WinGram specifically | **$73.23**, above the $10 minimum |
| Visible but unwithdrawable | **$0.00** |

The $27.34 gap between genuinely earned and stored is ordinary pool trimming and frozen-tick lag across
six campaigns, not a defect on this clipper. **The withdrawal gate uses stored, so $73.23 is the
number he can act on**, and the recomputation is here to prove the stored figure is not inflated.

### Clipper B, independently computed

| | |
|---|---|
| Campaigns | **WinGram only**, one clip |
| Views on that clip | 12,061 at a `1.0000` stamp |
| **Genuinely earned** | **$12.06** |
| Stored payable | **$12.02** |
| Lifetime paid | **$0.00. He has never been paid anything, ever.** |
| **Current withdrawable** | **$12.02**, above the $10 minimum |
| Visible but unwithdrawable | **$0.00** |

**Clipper B is the harder case of the two.** He has one clip, one campaign, has never received a cent,
requested his first payout on `2026-07-28`, waited ten days, and had it silently voided on a campaign
that is now archived and frozen. His entire relationship with the platform is $12.02 he has not been
paid and a request that vanished without a word.

---

## PART 2 — WHY NEITHER HAS SELF-SERVED IN SIX DAYS

**They CAN. Every blocker was tested and every one is clear. What failed is that nobody told them.**

| possible blocker | verdict | evidence |
|---|---|---|
| Does the withdrawal gate refuse an archived campaign? | **NO** | `grep isArchived src/app/api/payouts/route.ts` returns **zero matches**. The route has no `isArchived` check |
| Does it refuse on campaign status? | **NO** | `grep campaignStatusBlocks` in the payout route returns **zero matches**. There is no campaign-status gate in the withdrawal path at all |
| Does the balance endpoint hide the campaign? | **NO** | `/api/earnings` filters only `isTestCampaign: false` (`route.ts:64,83,100,117`). No `isArchived` filter anywhere, so WinGram still appears in `campaignBalances` |
| Below the per-campaign minimum? | **NO** | WinGram's `minPayoutAmountDecimal` is NULL, `resolveMinPayout` returns `PLATFORM_MIN_PAYOUT_USD = 10` (`payout-minimum-shared.ts:27`). A has $73.23, B has $12.02 |
| Is the global clamp blocking? | **NO** | A: $240.31 lifetime vs $112.00 consumed, $128.31 available. B: $12.02 vs $0.00, $12.02 available. Neither clamps to zero |
| Does a VOIDED row occupy the one-open-request slot? | **NO** | The slot check covers `REQUESTED / UNDER_REVIEW / APPROVED` only. VOIDED does not occupy it |
| **Were they told?** | **NO. THIS IS THE ANSWER** | see below |

### Nobody told them, and the code has no way to tell them

Every notification either clipper received since 2026-08-01, read from the table:

| clipper | most recent notifications |
|---|---|
| Clipper A | `CLIP_APPROVED` 08-09 12:26, `STREAK_WARNING` 08-07 16:15, `CLIP_REJECTED` 08-07 16:15, `CLIP_APPROVED` 08-07 **10:25:31**, `CLIP_APPROVED` 08-07 **10:25:17** |
| Clipper B | `growth_stalled_7d` "Checking in" 08-04 06:30 |

**Zero payout notifications to either clipper. Not one, ever.**

Look at Clipper A's timeline closely, because it is the whole story in three rows. He received
`CLIP_APPROVED` at `10:25:17` and `10:25:31`. The archive fired at `10:26:34.832`. His payout was voided
at `10:26:35.219`. **He was actively on the platform, receiving notifications, in the ninety seconds
before his payout was destroyed, and the platform said nothing about it.** He then received a streak
warning and two more clip notifications over the following days. Everything talked to him except the
one thing that mattered.

And it is not merely that the archive path forgot. **The deliberate review path has no VOIDED
notification either.** `payouts/[id]/review/route.ts` calls `createNotification` at `:430` for
`PAYOUT_APPROVED`, `:438` for `PAYOUT_REJECTED` and `:446` for `PAYOUT_PAID`. **There is no
`PAYOUT_VOIDED` arm.** So even a deliberate, correct, audited void by the owner today would tell the
clipper nothing. The silence is structural, not an accident of the cascade.

### Is either in BL-762's silent $0.00 state?

**No, and this is worth stating because it would have changed the recommendation.** BL-762 concerns a
clipper shown $0.00 with a disabled button and no explanation. Neither of these two is in that state:
both have a positive available balance on a campaign that still appears in `/api/earnings`, both clear
the $10 minimum, and the request button is live for both. **They are not staring at a wall. They are
staring at a payouts page that looks normal and gives them no reason to press the button again.**

### The finding, stated plainly

**The money is reachable and invisible at the same time.** That is a worse failure mode than a hard
block, because a hard block produces a support message and this produces nothing. Six days of silence
is the measured cost. **The owner does not strictly have to act for them, but they will not act on
their own, because from where they sit nothing happened.**

---

## PART 3 — EVERY PAYOUT EVER VOIDED, AND WHICH VOIDS NOBODY AUDITED

29 VOIDED rows exist platform-wide. Grouped by the exact `updatedAt` instant, cross-joined against
`audit_logs` where `targetType='payout'` and the action matches `%VOID%`:

| void instant `::text` | rows | clippers | gross | cash | audit rows | **SILENT** | reason |
|---|---|---|---|---|---|---|---|
| **`2026-08-07 10:26:35.219`** | **2** | **2** | **$82.13** | **$74.33** | **0** | **2** | **Campaign archived** |
| `2026-04-22 19:19:28` to `19:19:48` | 9 | 1 | $772.88 | $703.32 | 9 | 0 | (null), all `FORCE_VOID_PAID_PAYOUT` |
| **`2026-04-22 18:15:45.123`** | **1** | **1** | **$27.81** | **$25.31** | **0** | **1** | **Campaign archived** |
| **`2026-04-22 16:00:14.096`** | **1** | **1** | **$111.00** | **$101.01** | **0** | **1** | Test data cleanup |
| **`2026-04-22 15:59:02.824`** | **1** | **1** | **$200.00** | **$182.00** | **0** | **1** | Test data cleanup |
| `2026-04-10 18:27:34.157` | 9 | 2 | $442.00 | $430.00 | 9 | 0 | (null) |
| `2026-04-10 16:00:51.913` | 3 | 2 | $210.00 | $210.00 | 3 | 0 | (null) |
| `2026-04-10 16:00:47.724` | 3 | 2 | $33.00 | $33.00 | 3 | 0 | (null) |
| `2026-04-07 15:51:24` / `15:51:31` | 2 | 2 | $21.00 | $21.00 | 2 | 0 | (null) |

**Reconstructed from `updatedAt` forensics because the audit log is silent, exactly as the brief asked.**
The three multi-row April clusters look like bulk writes and are the shape that would hide a second
cascade, so each was checked individually rather than assumed: **all 15 of those rows DO carry audit
rows** and were deliberate, audited voids. The April `18:27:34.157` cluster of 9 is the largest bulk
void in the platform's history and it is fully audited.

### The silent population

**5 rows, $421.94 gross, $382.65 cash, spread across 4 clippers and 3 distinct causes:**

| cause | rows | gross | cash | live claim? |
|---|---|---|---|---|
| **Archive cascade, WinGram, 2026-08-07** | 2 | **$82.13** | **$74.33** | **YES, both unpaid, this round's subject** |
| Archive cascade, April, campaign row gone | 1 | $27.81 | $25.31 | **No.** That clipper has 0 clips, $0.00 lifetime earnings and 0 payout rows today. Test-data era, nothing behind it |
| "Test data cleanup, campaign overpaid", April | 2 | $311.00 | $283.01 | Not assessed, April test-data era, reason string is self-describing |

**`paidAt` is NULL on all 29 VOIDED rows without exception.** Under `balance.ts:122`, a VOIDED row
counts as money-out only when `paidAt` is not null, so **no money has ever left the platform through a
void.** Every voided amount returned to the clipper's available balance. Nothing is stranded anywhere.

**Total ever voided by an archive: 3 rows, $109.94 gross, $99.64 cash. Still unpaid and still owed to a
live clipper: 2 rows, $82.13 gross, $74.33 cash.** Those two are Clipper A and Clipper B.

---

## PART 4 — PROVING IT CANNOT RECUR, RATHER THAN TRUSTING BL-733

Verified independently at `018c22ca`, not inherited.

### The archive path

`campaigns/[id]/route.ts:963-995`. The `payoutRequest.updateMany` is **gone**, replaced by:

```
const pendingLeftAlone = await db.payoutRequest.count({
  where: { campaignId: id, status: { in: ["REQUESTED", "UNDER_REVIEW", "APPROVED"] } },
});
```

**A `count` is a read. A read cannot cascade.** The archive still flips the campaign to PAUSED
(`:939`), deactivates tracking jobs (`:956-960`) and pauses marketplace listings, and it now writes a
status-change audit row via `recordStatusChange` at `:944-953` with `triggeredBy: "ARCHIVE"`.

### Every other path that could reach VOIDED

| test | result |
|---|---|
| `grep payoutRequest.updateMany src/` | **1 hit**, `campaigns/[id]/destroy/route.ts:92`, and it writes `campaignId: null`, **not status**. See the fix list |
| Every `"VOIDED"` status write | **exactly one**, `payouts/[id]/review/route.ts:662` |
| That route's state machine | `:57` allows `VOIDED` **only from `PAID`, and only for `OWNER`**. The cascade reached VOIDED from REQUESTED, UNDER_REVIEW and APPROVED, none of which it permits, so the old code was bypassing the machine rather than using it |

### Every other campaign status transition, checked for the same shape

Because BL-641 found COMPLETED missing from `campaignStatusBlocks` entirely, "one status is clean" was
not accepted for the others:

| transition | side effects | touches payouts? |
|---|---|---|
| ACTIVE to PAUSED (`:488-495`, `:744-760`) | clears `lastBudgetPauseAt`, sets `pauseSource: "MANUAL"`, audit row | **No** |
| PAUSED to ACTIVE (`:496-499`, `:766-775`) | clears `pauseSource`, audit row | **No** |
| to PAST (`:478-485`) | OWNER-only guard | **No** |
| to COMPLETED (`:819-829`) | deactivates tracking jobs, logs | **No** |
| to ARCHIVED (`:925-995`) | PAUSED, jobs off, listings paused, audit row, **counts** payouts | **No** |
| DESTROY (`destroy/route.ts`) | requires `isArchived` first (`:45`), then **nulls `campaignId` on payout rows** | status **No**, linkage **yes** |

**No campaign status transition writes a payout status anywhere in the codebase.**

### Does every payout status change write an audit row?

**Yes, on both paths, and this was the second BL-733 claim worth checking rather than inheriting.**

* `payouts/[id]/review/route.ts` calls `logAudit` at `:309`, `:332`, `:349` and `:387`, including on an
  **idempotent no-op write**, and tags a force-void of a PAID row as `FORCE_VOID_PAID_PAYOUT` so it can
  be grepped apart from an ordinary void.
* `src/actions/payouts.ts:154-156`, the unwired server action, now **refuses `VOIDED` outright** with a
  message pointing at the guarded route, and audits every other transition at `:168-177`.

Measured against live data: **24 of 29 VOIDED rows carry an audit row**, and the 5 that do not are the
three archive cascades and the two April manual cleanups, all pre-dating the fix. **No unaudited void
has occurred since `2026-08-07 10:26:35.219`.**

### The honest gap that remains

**A void still notifies nobody.** BL-733 closed the cascade and the audit hole. It did not add a
`PAYOUT_VOIDED` notification, and the review route still has none, so a correct owner-initiated void
today produces an audit row the clipper cannot see and no message he can. **The silence that cost six
days is still in the code.** That is fix 1 below.

---

## PART 5 — WHAT AN ARCHIVED CAMPAIGN ACTUALLY DOES, RE-MEASURED

### WinGram today

| | BL-732, `2026-08-07 15:36` | **today** |
|---|---|---|
| Clippers with earnings | (not stated) | **43** |
| Total payable | (not stated) | **$267.58** |
| **Total available, unpaid** | **$165.77** | **$167.18** |
| Clippers with anything available | 20 | **20** (3 + 17) |
| **Able to request now** | **3** | **3**, holding **$101.53** |
| **Stuck under the $10 minimum** | **17 at $64.24** | **17 at $65.65** |

The $1.41 movement is definitional, not accrual, and that can be proven: **WinGram is completely
frozen.** 0 active tracking jobs, last clip update `2026-08-07 10:10:36.227`, last `clip_stats` check
`2026-08-07 10:10:36.178`, both 16 minutes BEFORE the archive. Nothing has accrued in three days and
nothing ever will.

The three who can request are **Clipper A ($73.23), a third clipper `cmponzpo` ($16.28, who has never
filed a request at all), and Clipper B ($12.02)**.

### What ARCHIVED does to a clipper, stated plainly

| can the clipper... | answer |
|---|---|
| see the campaign in the marketplace or campaign list? | **No.** `campaigns/route.ts:439` and `campaigns/past/route.ts:32` both filter `isArchived: false` |
| see their own clips on it? | **Yes.** No archive filter on `/api/clips/mine` |
| see their earnings from it? | **Yes.** `/api/earnings` filters only `isTestCampaign` |
| **request a payout against it?** | **YES. Nothing in the withdrawal path reads `isArchived`** |
| keep earning on it? | **No.** Tracking jobs deactivated, `campaignStatusBlocks` stops accrual |

**So archiving does NOT trap earned money, and BL-732's suspicion that it might is settled in the
negative.** The withdrawal path is clean.

### But there IS an ongoing defect, and it is a different one

**Archiving is a one-way trap for anyone below the minimum.** The two facts compose into it:

1. Archiving permanently freezes accrual. There is no path back: un-archiving is possible, but nothing
   in the product resumes accrual on a PAUSED archived campaign for clips that stopped being tracked.
2. The withdrawal gate enforces a $10 per-campaign minimum with no exception for a dead campaign.

**A clipper sitting at $3.80 on a live campaign is waiting. The same clipper on an archived campaign is
finished, permanently, and nothing tells them.** On WinGram that is **17 clippers holding $65.65 that
they can never reach**, and the number can only be reduced by the owner, never by them.

**This recurs on every campaign the owner archives.** It is not specific to WinGram, it is a property of
archiving plus a minimum. Fix 2 below.

---

## PART 6 — THE VERDICT AND THE EXACT ACTIONS

> ## **Clipper A is owed $65.50 in cash and Clipper B is owed $8.83, and YES, both can get it themselves today. Nothing blocks either of them. They simply have never been told their requests were destroyed.**

### The safe procedure, and why it is NOT a hand payment

**BL-696 established the platform cannot record a hand payment, so a balance paid outside it stays
claimable and can be requested again. That risk is LIVE here**, and this is the sharpest difference from
BL-760's case. In BL-760 the $60.47 had been reverted out of the clipper's balance, so it was
unclaimable and a hand payment could not be double-claimed. **Here the opposite is true: the voided
amounts returned in full to both clippers' available balances** (`paidAt` NULL, `balance.ts:122`), so
Clipper A's $73.23 and Clipper B's $12.02 are **claimable right now**. Paying either by hand today
creates exactly the double-pay BL-696 documented.

**Therefore, in this order:**

1. **Message both clippers.** Tell them their earlier request was cancelled by a system fault when the
   campaign was archived, that the money was never lost, and that they need to submit the request
   again on the payouts page. Name the amounts: **$73.23 available to Clipper A, $12.02 to Clipper B.**
2. **Also message the third WinGram clipper, `cmponzpo`, who holds $16.28** and has never filed a
   request. He was not caught by the cascade, but he is in the same frozen campaign and the same
   silence.
3. **Wait for each to file.** The gate will accept it: no archive check, no status gate, both above the
   minimum, no open-request slot occupied by the VOIDED row.
4. **Approve and pay against THAT row**, through `payouts/[id]/review`, and mark it **PAID** so `paidAt`
   is stamped. That is what makes the money-out real in `balance.ts` and what makes a second claim
   impossible. The cash to send is the row's own `finalAmount`, which the review UI already displays.
5. **Do not pay by hand and do not un-void the old rows.** Un-voiding is not a transition the state
   machine allows, and a hand payment leaves the claim standing.

**If a clipper does not respond**, the only safe unilateral action is to pay against a row they have
filed. There is no way to discharge a claimable balance from the owner's side without one, and inventing
one is how double payments happen.

### Ranked systemic fixes, specified and NOT performed

**1. A void must notify the clipper. `payouts/[id]/review/route.ts:646-663`.**
The route notifies on APPROVED (`:430`), REJECTED (`:438`) and PAID (`:446`), and has **no arm for
VOIDED**. Add a `PAYOUT_VOIDED` notification in the `action === "VOIDED"` branch, naming the amount, the
campaign and the fact that the balance has returned and can be requested again.
**Prove:** a void writes exactly one notification row to the payout's `userId`; a force-void of a PAID
row says something different, because that money already left; no notification on an idempotent no-op.
**Rollback:** delete the arm. It is additive and touches no money file.
**Why first:** this is the defect that actually cost six days. The cascade is fixed; the silence is not.

**2. The archived-plus-minimum trap. `payouts/route.ts:345` with `payout-minimum.ts:110`.**
17 clippers hold $65.65 they can never reach because accrual is frozen and the minimum still applies.
Options, in order of preference: waive the per-campaign minimum when `campaign.isArchived` is true;
or let the owner set a campaign's minimum to zero on archive; or add an owner-side sweep that pays out
sub-minimum balances on dead campaigns.
**Prove:** on an archived campaign a clipper with $3.80 can file and be paid $3.80; on a live campaign
the $10 minimum is byte-identical to today; BL-627's no-overpayment property still holds; no clipper's
available rises by a cent.
**Rollback:** revert the waiver; no data written.
**Why second:** it is 5.4x more money than the void, it is permanent, and it recurs on every archive.

**3. Archiving should warn about pending payouts rather than only counting them. `campaigns/[id]/route.ts:993`.**
`pendingLeftAlone` is computed and, as far as this audit found, only logged. The owner archived WinGram
with two live requests outstanding and had no idea.
**Prove:** archiving a campaign with N pending payouts returns N in the response and the UI states it
before the typed confirmation; archiving with zero pending is unchanged.
**Rollback:** revert; read-only either way.

**4. `campaigns/[id]/destroy/route.ts:92` nulls `campaignId` on every payout row of a destroyed campaign.**
This is the one surviving `payoutRequest.updateMany`. It does not change status, so it cannot void, but
it silently detaches historical payouts from their campaign, which is how the April `$27.81` archive void
now reads as "(campaign row gone)" and cannot be reconciled against any campaign. It also breaks
per-campaign liability maths for any destroyed campaign.
**Prove:** destroying a campaign preserves the payout-to-campaign link, or, if the link must go, writes
an audit row per detached payout first.
**Rollback:** revert the change; no historical data is rewritten by this fix.

**5. Reconcile the two April "Test data cleanup" voids, $311.00 gross / $283.01 cash.**
Both are silent, both are April test-data era, and neither has been assessed by any round. Low priority
and probably nothing, but it is the last unexamined silent void and it should be closed rather than
left as a known unknown.

### What could not be measured

* **Whether either clipper ever saw anything.** There is no read receipt on notifications and no page
  analytics, so "they were not told" is proven from the absence of any notification row, not from their
  behaviour. That is the strongest available evidence and it is one step short of certainty.
* **The two April test-data voids** were counted and costed but not traced to a cause, because the
  campaign rows are gone and the reason string is self-describing. Fix 5.
* **Whether un-archiving WinGram would resume accrual** was not tested, because testing it would require
  changing state. The tracking jobs are deactivated and nothing in the archive path re-activates them on
  restore, so the honest answer is that it probably would not without a manual re-activation, and that
  is an assumption rather than a measurement.

Nothing was changed. No payout was un-voided, approved, created, cancelled or paid; no balance was
touched; no campaign was un-archived; `run-select.js` refuses every write keyword by construction.
