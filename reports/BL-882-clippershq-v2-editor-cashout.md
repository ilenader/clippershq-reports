# BL-882 — marketplace v2, round six: the editor can see his money, and ask for it

> **NOTHING IS UNREMOVABLE AND NO SQL IS OWED. FIRST LINE, AS THE ROUND REQUIRES.**
> 267 ledgered rows across the round, **`VERIFIED: 0 of 267 recorded rows remain`**, 0 failed. An
> independent pattern sweep that the destroyer never uses returns **zero** `bl882sbx-` rows in
> `users`, `campaigns`, `clips`, `marketplace_v2_clips` and `payout_requests`, read at
> `2026-09-16 20:24:02+00` against the database's own `now()`. **LOCK 2 refused the whole ledger
> once**, on three lines this round's own proof wrote wrong, and deleted nothing until they were
> repaired by looking the rows up. The lock was never loosened.

**2026-09-16. Shipped on `checkpoint/BL-882`, merged to `main` at `c316247`. Requires a Railway
REDEPLOY**, and BL-877 through BL-881 are all still owed. Base `origin/main` @ `f2a5a81`. Isolated
worktree `C:/w/b882`, **verified gone**: `git worktree list` shows only the primary tree and
`ls /c/w/b882` returns "No such file or directory".

---

## THE HEADLINE

**An editor with $450 opened `/earnings` and read $0.00, and it was not a display bug.** `balance.ts`
referenced his table at exactly two lines, `:498` and `:502`, and both sit inside
`getCampaignBudgetStatus`, which is the CAMPAIGN side. Every user facing function in that file,
`effectivePaidOut`, `computeBalance`, `computeCampaignBalances` and the rest, had never heard of him
as an earner. The arithmetic had no term for him. He now has a page that adds up in two directions,
and he can ask for the money through the same payout route every clipper already uses.

**The trainer's mistake did not happen twice.** BL-835 built a commission, BL-840 proved its
arithmetic exactly right, and BL-843 then discovered there was no cashout route anywhere, so a
trainer accrued money that could never become money. An editor has accrued money since BL-877. As of
this round he can request it, the owner can approve it, and the owner can mark it paid.

---

## THE MODEL SPLIT, AND EVERY SUBAGENT CLAIM CHECKED

| work | model | checked how |
|---|---|---|
| every line touching a payout, an earnings figure, the balance derivation, the guards, the proofs and this report | **Opus, no subagent between it and the source** | n/a |
| payout machinery inventory (request, review, fee, standing gate, minimum, `clipIdsSnapshot`, `PayoutRequest`, typed refusal) | Haiku | **VERIFIED.** Every file:line re-read. One material omission found: it reported `checkPayeeStanding` at `payouts/route.ts:379` without noting the absent `includeMarketplaceBan`, which became this round's one deliberate gate change |
| count of balance derivations | Haiku | **PARTLY VERIFIED, AND SHORT.** It found ELEVEN and I verified derivations 1, 2, 5, 6, 7 line by line. It **missed a TWELFTH**, the one that mattered most, found by reading `payouts/[id]/review/route.ts` myself |
| accessibility lead and its specialists | Sonnet family | **THREE LOAD-BEARING CLAIMS VERIFIED MYSELF** before a line of UI was written: `--bg-page` has **zero** definitions repo wide and **26** referencing files (my count and a second agent's agree); `--text-primary`, `--text-secondary` and `--text-muted` are **all `#ffffff`** at `globals.css:72-74`; `toggleTheme` is destructured at `navbar.tsx:55` and **never called**. `ScrollTable`, `Modal`'s `initialFocusRef`/`returnFocusRef`, `LiabilityView`'s `MoneyCell`, the `--mp-text-*` ramp and `belowMinimumMessage`'s server-only-free module were each opened and confirmed to exist as described |

---

## PART 0 — WHAT AN EDITOR'S MONEY ACTUALLY WAS

### Does `balance.ts` see his rows? No, and that is the finding.

`grep -n "marketplaceV2EditorEarning\|marketplaceV2PlatformEarning" src/lib/balance.ts` returns
**exactly two lines**, `balance.ts:498` and `balance.ts:502`, both inside `getCampaignBudgetStatus`
(`balance.ts:392`), which answers "what has this CAMPAIGN spent". The user side is these eight
exports and the editor appears in none of them:

| export | line | saw the editor |
|---|---|---|
| `isPayoutMoneyOut` | `:117` | no |
| `clipperLiability` | `:126` | no |
| `campaignBudgetLiability` | `:140` | no |
| `effectivePaidOut` | `:234` | no |
| `paidNoLongerOffsetting` | `:265` | no |
| `computeBalance` | `:271` | no |
| `computeCampaignBalances` | `:327` | no |
| `getCampaignBudgetStatus` | `:392` | **yes, campaign side only** |

`BalanceInput` (`balance.ts:7`) had three arms: `clips`, `payouts`, `marketplaceCreatorEarnings`. An
editor owns no clip on the campaign, holds no payout and has no creator row. **He was representable
in that type only as the number zero.**

### Can `PayoutRequest` represent his claim? Yes, and better than the trainer's could.

**The existing shape is used as it stands. Nothing is widened, no second shape is built, and no
column is added.** His claim is `(userId, campaignId, amount)`, which is the shape's own key, and
unlike BL-843 the `campaignId` is genuinely non NULL because `MarketplaceV2EditorEarning.campaignId`
is required. Five things BL-843 had to work around simply work:

1. **The one open request guarantee is real.** `uq_payout_open_per_user_campaign` is partial on
   `("userId","campaignId")`. A referral cashout carries a NULL campaignId, Postgres treats NULLs as
   distinct, and the index therefore constrained nothing for BL-843. Here it binds.
2. **The money locks the instant he asks.** `LOCKED_PAYOUT_STATUSES` (`balance.ts:54`) already holds
   REQUESTED, UNDER_REVIEW and APPROVED.
3. **Paid-is-final lands on the right campaign by construction.** `effectivePaidOut` bounds each
   payment by `payableByCampaign[campaignId]`, and that map is exactly where PART 1 adds his rows.
4. **The minimum message is not a lie.** `belowMinimumMessage` is wired to a campaign name, and an
   editor's claim has one. BL-843 had to invent a platform minimum because a referral cashout does
   not.
5. **Fee, express, price, settle-unpaid, sent-to-admin and the SLA deadline apply unchanged**,
   because none of them reads where the money came from.

### The one field that does not fit, and why NULL is the WORSE answer

`clipIdsSnapshot` is "the clip IDs that funded this payout". An editor's claim is funded by clips he
does not own. There are three possible values and **two of them write another user's money**:

* **The posters' clip ids** are actively dangerous. `admin/payouts/[id]/adjust/route.ts:236-244`
  deliberately DROPS the `userId` filter when the snapshot is non-null, so pricing an EDITOR's payout
  down would shrink **other posters'** `Clip.earnings`, and BL-881's sync would faithfully propagate
  that into every leg. One owner action, three strangers' money.
* **NULL** is worse than it looks. `adjust/route.ts:258-265` falls back to "all clips on this campaign
  owned by `payout.userId`". For a pure editor that is zero clips; for an editor who also posts on the
  same campaign, which BL-876 permits, it shrinks **his own poster clips**.
* **An explicit empty array** is the only honest value, and every consumer already handles it with no
  change: `adjust:232`, `preview-adjustment:62`, `review:367` (`snapIds.length > 0` is false, so the
  stale-reduction branch is skipped) and `reject-botted:422` (an empty scope, so bot-rejecting an
  editor's payout rejects nobody's clips, which is right because the editor did not shoot the views).

**Measured in the sandbox:** the row created by the real route carries `clipIdsSnapshot = []`.

---

## PART 1 — THE BALANCE

### How many derivations exist? The file says three. A subagent found eleven. The real figure is TWELVE.

`balance.ts:186-197` states in prose that "THREE derivations of a clipper's account-wide availability
exist". That is true of the narrow question it was written to answer. It is not the number of places
that must learn about a new earner.

| # | site | decides |
|---|---|---|
| 1 | `balance.ts` `computeBalance` | the displayed global balance |
| 2 | `balance.ts` `computeCampaignBalances` | the per campaign breakdown |
| 3 | `api/payouts/route.ts` GET per campaign `:285` | the owner's `campaignAvailable` |
| 4 | `api/payouts/route.ts` GET global `:265` | the owner's clamp |
| 5 | `api/payouts/route.ts` POST tx per campaign `:792` | **the gate that refuses** |
| 6 | `api/payouts/route.ts` POST tx global `:930` | the global clamp that refuses |
| 7 | `api/payouts/route.ts` POST minimum message `:499` | the words of a refusal |
| 8 | `actions/payouts.ts` | dead code, zero importers |
| 9 | `api/admin/payouts/user/[id]/route.ts` | what the owner is told he owes |
| 10 | `api/admin/payouts/unpaid/route.ts` | the platform wide owed list |
| 11 | `lib/liability.ts` | the owner's liability report |
| **12** | **`api/payouts/[id]/review/route.ts:322`** | **whether the OWNER MAY APPROVE OR MARK PAID** |

**Number twelve was in no inventory and is the only load bearing one.** Left out, an editor's cashout
would have been accepted, would have locked his gross out of his own balance in a REQUESTED row, and
would then have thrown `INSUFFICIENT_BALANCE` on every attempt to approve it, forever. The feature
would have looked complete, let him ask, and been unable to pay him. That is BL-843's exact defect in
a new costume, and it was found by reading the file rather than by trusting a count.

**Nine of the twelve are taught this round** (1 through 7, 9 and 12). **Three are deliberately not**,
recorded as decisions at the foot of `scripts/check-v2-editor-balance.js`:

* `api/admin/payouts/unpaid/route.ts` — **zero** references to the first marketplace's creator table.
* `lib/liability.ts` — **zero** references to it either.
* `actions/payouts.ts` — dead code, zero importers platform wide.

The first two have never known about the CREATOR's 60 percent, a **Phase 6d gap that predates v2 by
three rounds**. Teaching them about the newer earner while the older one stays invisible would make
them wrong in a new way. Reported, not half fixed.

### One filter, written once, with a guard that caught this round's own code twice

`src/lib/marketplace-v2-editor-balance.ts` owns the single payable predicate:

```
clip: { isDeleted: false, status: "APPROVED", videoUnavailable: false }
```

character for character `api/earnings/route.ts:82-87`'s `creatorEarningsWhere`. **That filter is load
bearing rather than decorative:** BL-879 made v2 money move at POST time, so a v2 clip can carry a non
zero editor row while its `Clip` row is still PENDING, and without the status test he could withdraw
against work nobody had approved. The poster is protected from the same thing only by
`computeBalance`'s own `status === "APPROVED"` test; this is the editor's copy of that protection.

`scripts/check-v2-editor-balance.js` runs inside `prebuild` and **refused the build twice on this
round's own code**: once when `marketplace-v2-editor-dashboard.ts` hand rolled the predicate to get
`v2ClipId`, and once when `reject-botted/route.ts` wrote its own `where`. Both now go through the
module.

**The guard's first version could not fail, and that was caught.** `S2` tested
`includes("marketplace-v2-editor-balance")`; a demonstration renamed an import to
`"...-balanceX"`, which **contains that string**, so the guard passed while the file no longer
imported the loader at all. That is the defect BL-835 shipped and BL-881 was caught shipping in the
round that wrote the rule down. It is now anchored to `from "@/lib/marketplace-v2-editor-balance"`
with the closing quote, and was then **demonstrated failing twice**:

* deleting the editor's fold from `computeCampaignBalances` → `FAIL S1 computeCampaignBalances has
  BOTH second-earner loops`, exit 1.
* renaming the import in the twelfth derivation → `FAIL S2 .../review/route.ts still sees the
  editor`, exit 1.

Both restored, and both files back to exactly `59/2` and `18/1`.

### How the paid floor and the balance agree

They agree because **they read the same number from the same column and neither computes a floor**.
`floorV2EditorEarnings` (BL-881) reads `PayoutRequest` rows at status PAID for that editor on that
campaign and returns `max(proposed, min(current, floor))`. The balance derivation reads
`MarketplaceV2EditorEarning.amount`, which is whatever the floor wrote. **There is no second floor
computation to diverge**, which is the shape BL-822 found between the gate and the display. The
sandbox watched it: a bot rejection drove the poster to $0.00 and the platform to $0.00 while the
editor was held at **$18.00**, his own paid floor binding on his own payment history, and the
dashboard then showed exactly $18.00 on that clip.

### No existing clipper moved by a cent, measured rather than assumed

```
MarketplaceV2EditorEarning rows in the database: 0
Sum of every row, payable or not:               $0.00
Users with at least one PAYABLE editor row:      0
```

**The set of users who CAN move is empty**, because the term added is the sum of that user's own
editor rows and nothing else. Everyone else is unchanged by construction: every new term reads
`?? []`. `scripts/bl882-balance-delta.ts` is the read-only script that measured it, and the BL-824
guard's fourteen behaviour and invariant cases pass with their inputs untouched.

---

## PART 2 — THE CASHOUT, BY REUSE, AND THE SECOND PATH THAT WAS NOT BUILT

**No new request route exists.** He posts to `POST /api/payouts`, the same handler every clipper
uses, and it works because PART 1 taught the derivations. That is the strongest possible form of
"reuse rather than build a second one": BL-843 had to write a new route only because a referral
commission belongs to no campaign.

**Proved through the real route, with a real minted `__Secure-authjs.session-token` against a
PRODUCTION BUILD with `DEV_AUTH_BYPASS=false`:**

```
PASS  THE EDITOR CAN REQUEST HIS MONEY, through /api/payouts and no second path
      status 201 for $81.00
PASS  he pays HIS OWN rate on HIS OWN withdrawal
      9 percent of $81.00 is $7.29, leaving $73.71
PASS  THE OWNER CAN APPROVE IT. Without PART 1 this is INSUFFICIENT_BALANCE   status 200
PASS  THE OWNER CAN MARK IT PAID                                              status 200
PASS  after payment his available is zero and his paid out is what he asked for
      available $0.00, paid out $81.00 gross and $73.71 cash
```

### The one deliberate gate change, and why it is narrow

`checkPayeeStanding` is called at `payouts/route.ts:379` **without** `includeMarketplaceBan`, so a
marketplace ban has never stopped an ordinary CPM withdrawal. Widening that call would freeze the
ordinary earnings of every marketplace banned clipper on the platform, which is a policy change
nobody asked for. So the marketplace ban is applied to **marketplace money only**: the check fires
when, and only when, the request draws on a v2 editor balance. It is not a new rule either, only an
earlier one, because `review/route.ts:248` already refuses APPROVE and PAID for a marketplace banned
payee; without it the request would be accepted, would lock his balance, and would be unapprovable.

```
PASS  a MARKETPLACE ban refuses a withdrawal of MARKETPLACE money, by the standing gate and not a rate limit
      status 403 code MARKETPLACE_BANNED_PAYEE
PASS  the same editor, unbanned, is let through with no other change   status 201
PASS  BL-849's payee standing gate refuses a BANNED editor              status 403
```

### The four questions, answered and justified

| question | answer | why |
|---|---|---|
| **Does a minimum apply?** | **Yes, the CAMPAIGN's own minimum**, unchanged | BL-728 made minimums per campaign, and an editor's claim carries a real `campaignId`, so `resolveMinPayout` and `belowMinimumMessage` both work and the sentence names a campaign that exists. BL-843 needed a platform minimum only because a trainer's commission has no campaign |
| **Does express apply?** | **Yes, unchanged** | Express is a property of how fast the OWNER pays, not of where the money came from. The premium is stored per row at create time, the SLA deadline is snapshotted, and nothing in either reads the source of the balance. Nothing was written to enable it and nothing to prevent it |
| **Can BL-861's close-unpaid reach him?** | **Yes, proved** | `status 200`, the row's status stays REQUESTED, which is what keeps the requested gross locked out of his balance instead of releasing it |
| **Can BL-864's set-amount reach him?** | **Yes, proved** | `status 200`, `actualPaidAmount $7.00`, stamped with who set it and when |
| **Does closing still erase a set price?** | **YES, IT STILL BITES, measured at three points** | Set to **$7.00**, erased by the close, and reopening (`status 200`) left it **still erased**. It bites an editor exactly as it bites a poster. **Not made worse by this round and not fixed by it**: inheriting the existing behaviour unchanged is the point of reusing the machinery, and it stays BL-864's to fix |

### The dangerous control refuses itself, by existing code

`admin/payouts/[id]/adjust` is the legacy coupled route BL-826 caused and BL-861's `price` route
replaced. With `clipIdsSnapshot = []` it resolves `clipsWhere.id = { in: [] }`, finds zero clips,
counts zero PRR'd clips, and **returns a 400** with its existing message. The owner is pushed to
`price`, which is BL-861's whole intent. The message wording is slightly off for an editor and is
reported, not changed.

### Every named fix proved to reach him

* **BL-688 typed refusal** — `status 400, code AMOUNT_EXCEEDS_CAMPAIGN_BALANCE`, a 4xx and never a
  500. **And a real pre-existing defect was found here.** See below.
* **BL-814 transaction budget** — the request is created inside the same Serializable transaction, and
  the editor's leg is read through `tx` so it sits in one snapshot with the write.
* **BL-827 owner-set-amount authority** — proved above.
* **BL-863 cash not gross** — every money figure the dashboard emits is a `{ gross, cash }` PAIR, and
  the cash side is derived through `calculatePayoutBreakdown`, the same function the payout uses.
* **BL-853 reject-botted** — the before and after now carry the editor's rows on both sides.

### THE PRE-EXISTING DEFECT THE PROOF FOUND: the typed refusal dropped its code

`payouts/route.ts`'s refusal branch returned `{ error: err.message }` and nothing else, so **the
`code` was dropped on every balance and duplicate refusal on that path**, while the minimum refusal
fifty lines above went through `payoutRefusalBody` and carried it. One handler, two response shapes.
BL-689 built the closed `PayoutRefusalCode` union precisely so a caller could branch on the code
rather than the prose, and prose matching is what caused BL-688: a substring looked for "Amount
exceeds available balance" while the sentence read "Amount exceeds your total available balance", the
match missed, and a legitimate 400 became a 500 telling three clippers holding **$52.86** to retry a
permanently impossible request. **Now one line, through the helper.** It is a pure addition to the
body: same status, same message, no key removed. The proof went from `code undefined` to
`code AMOUNT_EXCEEDS_CAMPAIGN_BALANCE`.

### AND THE BL-824 GUARD HAD BEEN RED ON MAIN FOR TWO ROUNDS

`scripts/bl824-paid-is-final.ts` exits 1 on `origin/main` at `f2a5a81`, and did before this round
touched anything. Two files shipped after BL-824 were never classified in its allow list:
`admin/payouts/[id]/devalue/route.ts` (BL-849's paid floor, which sums `clipperLiability` to compute
what has already been PAID, deliberately a raw paid sum and not an availability) and
`payouts/[id]/reject-botted/route.ts` (BL-853, which derives through `computeBalance` itself and whose
bare sum is a LOCKED sum, never in scope for the rule). **Nobody saw it because the guard was never
wired into `prebuild`.** Both files were read before being classified, and the guard now runs inside
every build: **14 of 14**.

---

## PART 3 — WHAT HE SEES

`/marketplace-v2/editor/earnings`, gated exactly as `editor/page.tsx` is, because `marketplace-v2` is
a SIBLING of `marketplace/` and inherits neither its layout nor its gate. `notFound()`, never a 403,
so the route's existence never leaks.

**It reconciles in two directions, and neither is a claim:**

```
PASS  the page reconciles ACROSS: earned minus paid minus held equals available
      $81.00 minus $0.00 minus $0.00 = $81.00, available reads $81.00
PASS  the page reconciles DOWN: every column's total is the sum of its rows
      1 campaign row(s) summing to $81.00 available
```

`availableGross` is **not computed on this page**. It comes from `computeCampaignBalances`, the same
function `/api/earnings` uses, and the totals row is the literal column sum of the rows above it, so
there is no second arithmetic anywhere that could disagree with the first.

**It is a real `<table>` at every width, and the reason is the DOWN reconciliation.** A card carries
the ACROSS one and cannot carry the DOWN one: there is no column for an eye, or a screen reader's
table cursor, to travel, and reading down a column IS the act of checking the sum. A responsive split
was considered and rejected: `display: none` removes a copy from the accessibility tree but both
copies stay in the DOM, so every id exists twice and every `aria-describedby` resolves against
whichever the browser saw first, possibly the hidden one, which on a money page is a wrong-number bug.
WCAG 1.4.10 excepts data tables from the no-horizontal-scroll rule and `ScrollTable` supplies the
labelled, keyboard reachable, focus ringed container the exception requires.

**Gross and cash everywhere**, in two separate columns with two separate headers, never a styled pair
in one cell. `LiabilityView.tsx:15` records why in the sharpest terms available: **BL-760 caught a
$5.44 near-overpayment and BL-763 a $7.80 one, both because a gross figure was about to be sent as
cash.** Each cell hides its digits behind one spoken sentence naming which figure it is, because in
browse mode a screen reader does not re-announce the column header and a row of eight numbers is
otherwise eight naked numbers.

**BL-876's dashboard, with one deliberate departure.** Clips submitted, approved and live, total
posts, and "Views across all posts" as a secondary line rather than a fourth tile. **Total earnings is
NOT in that strip**, and the reason is this round's own rule: it would then exist twice on one screen,
computed from two different sets, and "no two figures that could disagree" forbids exactly that. Every
dollar lives in the money block where it reconciles.

**BL-876's empty state, verbatim:** `"Approved. Waiting for its first poster."`, rendered with
`$0.00` and `0 views` exactly as any other value, with no alarm treatment, because zero here is a
legitimate expected temporary state. Photographed at all five widths.

### What he cannot see, proved by grep AND by direct request

BL-876 section 5.4's sharpest point is arithmetic rather than a field name: **printing both 45 percent
halves on one screen yields the owner's 10 by subtraction.** So the poster's leg appears nowhere, no
rate of any kind is emitted, and the editor's share arrives already multiplied.

```
PASS  the response carries none of the forbidden fields
      checked 9 field names against the live response body
PASS  no poster identity reaches the editor
      none of the three poster ids appears in his response
```

The nine were `ownerCpm`, `agencyFee`, `clientName`, `aiKnowledge`, `lockedOwnerShare`, `clipperCpm`,
`budget`, `posterId` and `walletAddress`, tested against the **live JSON body** of the real route, not
against the source. Enforcement is an explicit allow list in
`marketplace-v2-editor-dashboard.ts` with tenant isolation in the `where`, so another editor's rows
are never fetched rather than filtered out afterwards. There is no `include`, no spread of a database
row and no `select: undefined` in that file, which is the mistake `BL-532` is still open for on
`/api/campaigns`.

### The accessibility work, and three of its claims verified against source

The review ran **before any UI file was written**. Load-bearing findings I confirmed myself:

* **`--bg-page` is defined NOWHERE** and is referenced by **26 files**. `bg-[var(--bg-page)]` falls to
  `transparent`, and `ring-offset-[var(--bg-page)]` makes the composed `box-shadow` invalid and
  **deletes the focus ring outright**. Neither is written anywhere in this round's UI. **CLAUDE.md's
  CSS section names `--bg-page` as a house token; it does not exist. Reported.**
* **`--text-primary`, `--text-secondary` and `--text-muted` are all `#ffffff`**, so they give zero
  hierarchy and **colour cannot express "disabled" here at all**. The blocked cashout control
  therefore carries its state on three channels that are not colour: a heavier border, a different
  fill, and an announced sentence.
* **The light theme is unreachable**: `toggleTheme` is destructured at `navbar.tsx:55` and never
  called, `Sun`/`Moon` are imported and never rendered.

Applied throughout: `aria-disabled` and never native `disabled` on the cashout trigger, so the reason
is announced on focus and the control is not silently unfocusable; **pressing a blocked control says
why**, because a money button that does nothing is the worst outcome; a white focus ring at 18.40 to 1
against the card and **3.40 to 1 against a solid accent fill**, where an accent ring would be 1.00 to
1 and therefore no ring at all; the marketplace's own rings, measured at 1.54 and 1.69 to 1, are not
inherited; `--border-strong` at 3.48 to 1 for every boundary that carries meaning; no dimming by
opacity anywhere, because `opacity-40` on white over the card measures 3.83 to 1 and shifts with
whatever is behind it.

**The live fee breakdown is deliberately NOT a live region.** Every prefix of a number is itself a
valid number: someone typing `$412.90` pauses after the decimal point longer than any debounce window
and would be told, confidently, what they receive for `$41`. Raising the delay only moves where the
lie lands. The breakdown is visible and silent, and the complete money sentence hangs off the submit
control with `aria-describedby`, read once, complete, at the moment it matters.

---

## PART 4 — THE TWO GAPS BL-881 LEFT

### Campaign reassignment: BL-881's prediction was half right, and the harm was far worse

BL-881 predicted a v2 clip CAN be moved and that the leg rows would keep the old campaignId "until the
next tick". **The first half is right. The second was wrong: there was no next tick that fixed it.**

`marketplace-v2-writer.ts` holds the **only four writers** of either leg table platform wide. Both
CREATE branches set `campaignId`; **both UPDATE branches did not.** So a moved clip's legs stayed on
the source campaign for the life of the clip.

**BL-881 also checked one of the refusals and the answer needed all of them.**
`campaign-reassign.ts:125` blocks `isMarketplaceClip === true`, which a v2 clip never is. The other
three are all satisfiable at once on a freshly posted v2 clip, which the exercise proved:

```
PASS  a freshly posted v2 clip satisfies EVERY ONE of the FIVE reassignment refusals
      status PENDING, earnings $0.00, AgencyEarning rows 0
```

`createV2Post` creates the Clip as PENDING (`marketplace-v2-poster.ts:401`), a post with no views has
`Clip.earnings` of $0.00, the AgencyEarning row is written by the tick and does not exist yet, and
`CLIP_HAS_MONEY_ROWS` counts AgencyEarning and the FIRST marketplace's creator table and **knows
nothing about either v2 table**. **A FIFTH refusal was found by exercising rather than reading**: the
route itself blocks a test campaign destination, which no enumeration of this path had mentioned.

**What it cost, reproduced by hand and measured rather than argued:**

```
PRE-FIX STATE: the SOURCE campaign, which holds no clip at all, reads $55.00 spent.
               The DESTINATION, which holds the clip, reads $45.00.
               $55.00 of this clip's gross, 55 percent of it, is charged to the wrong budget.
PASS  IN THE PRE-FIX STATE THE EDITOR'S MONEY READS ON THE WRONG CAMPAIGN
      1 of his row(s) attribute to the source campaign while the poster's half of the same
      clip attributes to the destination.
```

His per campaign breakdown, the minimum he is held to, and the campaign his payout must name would
all have been a campaign his clip had left, while the poster's half of the same clip named the new
one. **Two earners on one clip, on two campaigns.**

**Fixed in two places, so the window is zero and cannot reopen:**

```
PASS  THE MOVE IS ALLOWED, which is the half BL-881 predicted correctly
PASS  BOTH LEG ROWS FOLLOWED THE CLIP, which is what BL-882 fixed
      The disagreement window is ZERO: they move inside the same transaction as the clip.
PASS  THE SECOND DEFENCE: the next earnings write puts both legs back on the clip's own campaign
PASS  and both campaigns then agree
      source $0.00, destination $120.00. The source holds no clip and is charged nothing.
```

### AND THIS ROUND'S OWN DEFECT, CAUGHT BY ITS OWN PROOF

The writer fix alone **would have UNDONE the route fix on the next tick.**
`recomputeV2PostEarnings` took its campaign and its CPM from `post.v2Clip.campaignId`, the EDITOR'S
SUBMISSION, so after a move it paid at the SOURCE campaign's rate, contradicting the stamps the move
had deliberately rewritten, and wrote both legs back onto the source. The legs moved with the clip and
the next recompute put them back. **The clip is the authority now**, with the v2 clip as fallback,
because the clip is what the budget is measured over: `getCampaignBudgetStatus` sums `Clip.earnings`
by `campaignId` and the two v2 aggregates beside it must name the same campaign or a campaign holding
no clip is charged for one. A move now logs `[MARKETPLACE-V2-RECOMPUTE-MOVED]` naming both campaigns.

### The agency deletions: BL-881 said eight and the real figure is THIRTEEN

Re-measured from source rather than inherited. `grep -c` over `src/`, not piped to `head`:

**Category A, seven sites that delete only when the owner's OWN computed amount is zero** —
`force-recalc-earnings:386`, `adjust:568`, `override:292`, `agency-monitor:215`, `review:1029`,
`cpm-restamp:222`, `tracking:3191`. Every one is the `else` of `if (ownerAmt > 0) upsert`. On a v2
clip that still earns, `ownerAmt > 0` because it is computed by the ordinary CPM_SPLIT path, so the
row is UPSERTED and **ADDS survives**. The delete fires only when the owner's cut is genuinely zero,
which is the right moment to clear a stale row.

**Category B, six sites where the clip has just been rejected or retired and earns NOTHING** —
`review:1352`, `review:1375`, `bot-rejection:317`, `clip-account-cascade:255`, `destroy:67`,
`destroy:72`. Each sits beside a `writeClipEarningsZero`, a `videoUnavailable: true` or a campaign
destruction, and `writeClipEarningsZero` delegates to the chokepoint, which since BL-881 fires the
three leg sync, so the other legs go to zero in the same transaction.

**BL-881's conclusion holds. Its count did not, and the REASON differs by category:** category B is
safe for the reason BL-881 gave; category A is safe for a reason it did not give, namely that the
delete is conditioned on the owner's own amount and not on the clip's state, so it cannot fire on a
clip that still earns. **Proved live:**

```
PASS  ADDS: every post carries an AgencyEarning row ON TOP of the platform's 10 percent
      $30.00 of ordinary owner cut per post, which under REPLACES would have been $0.00
```

---

## PART 5 — THE SANDBOX

Prefix `bl882sbx-`, four locks, opening snapshot before anything was created, every timestamp cast to
`::text` against the database's own `now()`.

```
OPENING SNAPSHOT, TAKEN BEFORE ANYTHING WAS CREATED
  db now(): 2026-09-16 19:53:48.337648+00
  campaigns 34, clips 10188, users 1749
  v2: clips 0, posts 0, editor 0, platform 0
  agency 4882, payouts 248
  BL-881 reconciliation query BEFORE: 0 row(s) out of balance
```

**41 of 41 money checks and 7 of 7 reassignment checks passed**, after **four runs that failed 5, 3, 1
and 1**, every one reported below.

### The full loop, as a person would do it

An editor submits through his own route, the owner approves through the ordinary queue, three posters
post, views accrue across three ticks, his page shows a figure that reconciles, he asks for it, the
owner approves, the owner marks it paid. Every one of those steps went through the real HTTP route
with a real minted cookie, so the real auth, role, ban and standing gates ran. **What did NOT run is
the tracking tick itself**, because running it would call a vendor actor and this round ran none;
`recomputeV2PostEarnings` is the function the tick calls, with the same arguments, so the money path
is real and the view fetch is not. That is said rather than implied.

### Every failure path

| path | result |
|---|---|
| more than he has | `400 AMOUNT_EXCEEDS_CAMPAIGN_BALANCE`, typed, never a 500 |
| a second open request | `409 DUPLICATE_PAYOUT`, **by the duplicate guard and not by a rate limit** |
| a banned editor | `403`, BL-849's standing gate |
| a marketplace banned editor | `403 MARKETPLACE_BANNED_PAYEE`, and the same editor unbanned goes through |
| a devaluation landing | poster $27.00 to $9.00, editor $27.00 to $9.00, in step |
| a poster's clip rejected under him | poster and platform to $0.00, **editor held at $18.00 by his own paid floor** |
| two owners at once | one outcome, not a mixture: the row ended REJECTED |
| close-unpaid and set-amount | both reach an editor's row; the erase trap still bites |

**Two of those came back 429 on an earlier run and were recorded as passes for the wrong reason.** A
rate limit is neither a duplicate guard nor a ban. `payouts/route.ts:404` allows three requests per
hour per user and one editor was driving six. **Each failure path now has its own editor**, and the
checks assert `status !== 429` so the mask cannot return.

### The full sum reconciles exactly

```
PASS  THE FULL SUM RECONCILES EXACTLY: the campaign's spend is every leg plus the owner's own cut
      spent $380.00 = posters $144.00 + editors $144.00 + platform $32.00
                    + the owner's ADDS cut $60.00 = $380.00
      Nothing created, nothing lost. Without BL-877's two v2 aggregates the same campaign
      would have read $204.00.
PASS  the editor's WITHDRAWABLE sum is smaller than the campaign's SPENT sum, and correctly so
      withdrawable $63.00 against $144.00 spent. The difference is the leg on a rejected clip,
      which the budget has still spent and which he may not withdraw.
```

An earlier run failed this by exactly **$18.00**, and the $18.00 named the answer: it is the floored
editor leg on the bot rejected clip. `getCampaignBudgetStatus` filters the two v2 aggregates on the
clip's life (`balance.ts:498`, `:502`) while the AgencyEarning aggregate at `:497` carries no clip
filter at all, which is BL-164's deliberate asymmetry. The assertion was wrong, not the aggregate, and
it now measures with the aggregate's own filters.

### Every invariant, across the full population

```
PASS  BL-627: the campaign never exceeded its budget            $380.00 of $100000.00
PASS  the earnings invariant holds across the FULL clips table  0 row(s) violating earnings = base + bonus
PASS  no editor leg is negative anywhere in the population      0 negative editor row(s)
PASS  BL-696: one editor row per clip, so nothing can be paid twice  0 clip(s) with more than one
```

BL-824's paid-is-final held for **both earners independently**: the poster fell freely while the
editor was held at money already paid to him, which is BL-849's intended lesser harm decided in
BL-881 and not a new rule.

### The reconciliation query, before and after

```
BL-881 reconciliation query BEFORE: 0 row(s) out of balance
BL-881 reconciliation query AFTER:  1 row(s) out of balance
PASS  every row the reconciliation query names is an explained paid floor, not a leak
      The one new row is the bot rejected clip: poster $0.00, editor $18.00 held at money
      already paid to him. BL-881 proved this query CAPABLE of returning a row; this run had
      it return one on a case that arose by itself.
```

An earlier run asserted "the same count before and after", which was the wrong assertion: the count
SHOULD rise by one, and what must be asserted is the PROPERTY, that every row it names is a floor case
and not a leak.

### The disclosed device, and what it cost

**The sandbox campaign was flipped non test for 30.3 seconds per run and restored.** Every clipper
facing money surface excludes test campaigns, `/api/earnings` at `:67`, `:68` and `:86` among them,
and BL-882's dashboard follows that rule, so a test campaign renders an editor an honest and entirely
uninformative $0.00. This is BL-878's device (160 ms) applied for longer and disclosed for longer.
While the flag was false these sandbox clips were visible to platform wide owner reports; nobody was
looking, the round ran alone, every person stayed `isTestUser`, every id kept the prefix, every row
was ledgered, and the window is printed in seconds by the script itself.

**It also surfaced a real divergence, reported and not settled:** the withdrawal gate passes
`includeTestCampaigns: true` because its own creator query carries no campaign filter, while the
dashboard passes false. On a test campaign those two disagree. The divergence predates this round and
this round deliberately mirrors each site rather than settling it.

### LOCK 2 refused the whole ledger, and was not loosened

Three lines recorded an AgencyEarning row under the CLIP's id with no owner named. The destroyer
**refused the entire file and deleted nothing**. `scripts/sandbox/bl882-repair-ledger.ts` rewrote
exactly those lines to the real row id with the sandbox campaign named as owner, looked up from the
database, refusing outright if any row belonged to a campaign that was not a sandbox campaign, and
dropping a line whose row no longer existed. **No row was deleted by the repair and the lock was never
weakened.**

### Teardown

```
47 deleted, 220 already gone, 0 FAILED
VERIFIED: 0 of 267 recorded rows remain.
```

And an independent sweep the destroyer never uses, by pattern rather than by ledger:

```
users 0 | camps 0 | clips 0 | v2clips 0 | payouts 0 | db_now 2026-09-16 20:24:02.435793+00
```

---

## PART 6 — RENDERS AND MERGE

**25 of 25 shots passed** at 320, 375, 414, 1280 and 1440, after **two runs that failed 9 and 6**.
BL-793's method: viewport on the CONTEXT, `window.innerWidth` read back beside every shot, URL read
back so a bounce to `/login` can never be photographed as a pass, every state asserted **in words**
so a shot that looks right but says the wrong thing fails. Surfaces: the editor's earnings page, the
same page in its empty state, his clips page, the cashout modal opened, and the owner's payout list.

### Two real UI defects, found by rendering and fixed

**1. A per clip money pair could not wrap**, costing 19 pixels at 320, because `shrink-0` sat on the
group rather than on the figures. The figures stay unbreakable; the group wraps.

**2. The earnings table panned the WHOLE PAGE by 582 pixels**, and it was verified as a real defect
rather than dismissed as a measurement artefact. Every ancestor clips: `main` is `overflow-x: hidden`
with `clientWidth 314`, `body.scrollWidth` is 320, and the region itself is 250 pixels wide scrolling
928 internally. The page still panned, and the proof was watching the `h1` move **582 pixels off
screen** when the viewport was scrolled right. Removing the table dropped the root scroll width from
902 to 320, isolating the cause. `overflow-x: clip` on two different ancestors did nothing;
**`contain: paint` on the table's own wrapper took the pan to zero at every narrow width** with the
table still scrolling inside its labelled, keyboard reachable region, which is the WCAG 1.4.10
exception actually applying rather than merely being claimed.

**The render harness was corrected too, and the correction was justified before it was made.**
`documentElement.scrollWidth` is unreliable on this app shell, so the check now **scrolls the page
right and reads the movement back**, which is what a person holding the phone experiences. That change
was made only after proving the pan was real; it loosened nothing.

### Merge

Branch `checkpoint/BL-882` pushed and **VERIFIED** at `6d0442d`. Merged `--no-ff` into `main`.
**The merge tree OID `4c45edb944de32d3972356d1db465d9f778314c0` is IDENTICAL to the branch tree OID**,
so the branch build IS the merge build. `main` pushed and **VERIFIED** at `c316247` with tags
`pre-BL-882` and `post-BL-882`. `checkpoint/BL-723` was not merged. BACKLOG is **202 items**.

### Gates, honestly

```
BUILD_EXIT=0
[event-wiring] 0 problems.
BL-882 V2 EDITOR BALANCE GUARD: 17 passed, 0 failed.
BL-824 GUARD: 14 passed, 0 failed.
eslint --config eslint.hooks.mjs --max-warnings 11   ->  0 errors, 10 warnings
Compiled successfully
```

eslint is present in `node_modules/.bin`, so the hooks gate is not silently no-opping. **All ten
warnings are pre-existing and none is in a file this round created**: they live in
`admin/archive/[campaignId]`, `admin/campaigns`, `admin/payouts`, `admin/team` (two),
`admin/users/[id]`, `PayoutCountdown` (two), `ReviewerCapabilityChecklist` and `tracking-modal`.

### The protected files

| file | state |
|---|---|
| `clip-earnings-writer.ts` | `4f63164b23af02e8310a00c654077779862a8f02` **byte-identical** |
| `earnings-calc.ts` | `00410634ee610d84a6ffb4b5d3693c99d6185549` **byte-identical** |
| `tracking.ts` | `8e2a62f554e23f3347f127d8a4a95116527e3924` **byte-identical** |
| `clip-earnings-invariant-middleware.ts` | `61cef39395363c31f0c902dd4c64e8c06b3e6449` **byte-identical** |
| `money-decimal.ts` | `ef5cdae757b9ad3c23380ee8b63e279f98d0b6ac` **byte-identical** |
| `campaign-era.ts` | `106e16ad75125c3b10b6949a2981d33614c69ab9` **byte-identical** |
| `marketplace-v2-sync.ts` | `56cb7a066706164108c2eb1042ada702a1e73876` **byte-identical** |
| `balance.ts` | **changed deliberately: 59 insertions, exactly TWO deletions** |

Both deletions in `balance.ts` are the same line, `.reduce((s, c) => s + (c.earnings \|\| 0), 0) +
creatorEarnings);`, replaced by itself with `+ v2EditorEarnings` appended, once for `totalEarned` and
once for `approvedEarnings`. Everything else in that file is pure insertion. That is BL-880's shape:
one semantic change, stated, and nothing else moved.

---

## CAN AN EDITOR SEE AND RECEIVE HIS MONEY END TO END?

**Yes, and it was watched happening rather than argued.** He submits, the owner approves, posters
post, views accrue, his page shows $81.00 gross and $73.71 cash and shows how those add up, he
requests it at his own 9 percent, the owner approves it, the owner marks it paid, and his available
returns to $0.00 with $81.00 gross and $73.71 cash recorded as paid to him. Every step through the
real route with the real gates.

**Two honest qualifications.** First, no editor has any money today: the database holds **zero**
`MarketplaceV2EditorEarning` rows, because BL-879's visibility gates are still closed and no v2 post
has ever been made in production. The path is proved and unused. Second, the whole v2 feature still
requires a **Railway redeploy**, and BL-877 through BL-881 are all owed alongside this.

## WHAT ROUNDS SEVEN AND EIGHT MUST BUILD

1. **The POSTER has no v2 surface of his own.** Half the earners on a v2 clip still cannot see their
   half in one place, which is the same sentence BL-881 wrote about the editor.
2. **The owner has no v2 specific payout view.** An editor's request and a poster's request look
   identical in his queue, and `clipIdsSnapshot = []` is the only thing distinguishing them, which is
   a fact about a JSON column rather than something a screen says.
3. **`admin/payouts/unpaid` and `liability.ts` understate what the platform owes**, and not only for
   the editor: neither has ever known about the FIRST marketplace's creator either. That is a Phase
   6d correction and deserves its own round with its own measurement, not a bolt-on.
4. **Nothing yet retires a v2 clip or removes an editor from a campaign** without leaving his floored
   leg behind, and the reconciliation query will name every one of those rows forever.
5. **BL-864's erase trap** still destroys a set price on close and does not restore it on reopen, now
   confirmed to bite an editor exactly as it bites a poster.
6. **`--bg-page` does not exist** while CLAUDE.md names it and 26 files use it, and one of them
   deletes its own focus ring by using it as a ring offset.
