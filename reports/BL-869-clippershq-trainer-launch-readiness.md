# BL-869 — Walking the trainer system, especially the part nobody had ever used

**2026-09-09. Shipped. `checkpoint/BL-869` merged to `main`.** Requires a Railway
redeploy. No schema change, no migration, nothing written that a revert strands.

---

## NOTHING UNREMOVABLE. FIRST LINE, AS REQUIRED.

**Zero sandbox rows remain, in any table.** Verified by direct query across all
twelve touched tables (`users`, `clips`, `payout_requests`, `campaigns`,
`clip_stats`, `clip_accounts`, `trainer_relationships`, `trainer_commissions`,
`trainer_refunds`, `notifications`, `audit_logs`) — every one returns `0` for
`bl869sbx-%`. `SELECT count(*) FROM users WHERE "isTrainer" = true` is back to
**0**, platform-wide, exactly as it was before the round.

**One incident, disclosed because it nearly became unremovable.** A run of the
walk threw partway through after creating fixtures. A later ledger repair wrote
its corrected content to `ledger.jsonl` and OVERWROTE that run's lines, orphaning
**15 rows** with no ledger entry naming them: 9 users, 5 clip accounts and 1
campaign. Because LOCK 1 deletes only what the ledger records, the tooling could
not remove them. They were recovered by `scripts/sandbox/bl869-recover-orphans.ts`,
which writes a ledger line only when the row satisfies BOTH locks re-read from
the database — the `bl869sbx-` id prefix AND the visible
`BL869-SANDBOX-DELETE-ME` marker in a human-readable column — and then removed by
the ordinary destroyer with all four locks in force. **15 recovered, 15 deleted,
0 remaining.** No lock was widened and no raw `DELETE` was issued.

Totals: **205 rows** recorded and deleted in the main teardown, plus the **15**
above. The clip count moved 9,818 → 9,826 during the round; those eight are
Prisma cuids in `PENDING`, real clippers submitting while the round ran, not
mine. **BL-868's rows were never touched and never counted as failures.** No
marketplace combination was tested — BL-868 owned that exclusively.

---

## THE MODEL SPLIT

| Work | Model | Why |
|---|---|---|
| Fetching and extracting eight prior reports (2 agents) | Haiku | Retrieval. No decision. |
| Mapping the trainer code surface | Haiku | Search and quote. No decision. |
| Accessibility review of four trainer surfaces | Specialist team | Reviews code, changes none. |
| **Everything else** | **Opus (me)** | See below. |

**NOT SPLIT, deliberately.** The trainer arithmetic, the nine-point identity fix,
the decision to change `computeTrainerCut` at all, every sandbox assertion, the
independent verdict on the two-press question, and this report were done without
delegation. Delegating the *reading* of `trainer-cut.ts` is safe; delegating the
judgement about whether a one-cent drift is reachable is not — and that judgement
was wrong on my first pass and had to be corrected by measurement.

**Rough saving:** ~368k subagent tokens of retrieval that would otherwise have run
at Opus rates, call it a 5x difference on that slice. Modest, and honestly stated:
most of this round was in the always-Opus category.

---

## PART 1 — PROMOTING A TRAINER, CLUMSILY

Every clumsy path was walked through `POST /api/admin/trainers`.

| Attempt | Result |
|---|---|
| Promote with no typed phrase | **Refused.** *"To make X a trainer, type NEW TRAINER to confirm. A trainer takes 10% of what their clippers are paid."* |
| Promote someone already a CLIPPER | Works. That is the normal case. |
| Promote the same person twice | **Refused:** *"They are already a trainer."* |
| Promote → demote → promote again | Works. |
| Set a pitch link | Works, at promotion time. |
| **Change** a pitch link | **`SET_PITCH` returns 400.** There is no action for it. |

### What the owner can tell at a glance, and what he cannot

The hub returns, per trainer: `id, username, trainerCode, trainerPitchUrl,
trainerPromotedAt, status, isDeleted, trainerPerfInsight`, plus the full pairings
list and commissions grouped by relationship and status.

**He can tell** who is a trainer and each one's code, and the pairings are present
to count trainees from.

**He cannot tell, at a glance, what each trainer has accrued.** There is no
per-trainer accrual total on the hub; the figures arrive grouped by relationship
and status and would have to be summed by eye. The accessibility review reached
the same conclusion independently.

**Nothing material is carried by colour**, which matters here more than usually:
`--text-primary`, `--text-secondary` and `--text-muted` are all `#ffffff`, emerald
against red measures **1.44:1**, and the emerald and amber card tints measure
**1.01:1 — literally the same colour**. Every state in the trainer surfaces
carries a distinct WORD, so 1.4.1 passes. That was the right original call and was
deliberately not "fixed".

**Two findings, reported not fixed.** Promoting does not return the trainer's code
in the response, and the code is the only way a clipper can join, so the owner must
go and find it before he can hand it to anybody. And a pitch link cannot be changed
once set, because `SET_PITCH` is not an action and re-promoting is refused for an
existing trainer.

---

## PART 2 — JOINING, INCLUDING BADLY

| Attempt | Result |
|---|---|
| A code that does not exist | Refused: *"We could not find a trainer with that code. Check the spelling and try again."* |
| **Your own code** | Refused: *"That is your own trainer code. You cannot be your own trainer."* |
| No consent ticked | Refused **on the server**, not just in the component. |
| **CAPITALS with a trailing space** | **Accepted.** The commonest way a person types a code they were sent. |
| A second trainer while already trained | Refused: *"You already have a trainer. Ask the owner to let you leave before you join someone else."* |
| A **banned** trainer's code | Refused: *"This code is not open to new clippers at the moment."* |
| A **demoted** trainer's code | Refused as unknown. |

### Would a real person understand what they are agreeing to?

**Yes.** This is the strongest part of the feature and it deserves saying plainly.
Rendered at 375px, in reading order, ABOVE the checkbox:

> **What it costs you**
> • Your trainer's 10% is worked out on your pay after fees.
> • Take a $100 withdrawal. $9 comes off for fees.
> • Your trainer then takes $9.10. You receive $81.90.
> • The platform fee itself does not change.
> • An express withdrawal costs extra. It does not change your trainer's 10%.
>
> **What it applies to**
> • Only clips you post after you join.
> • Clips you posted before today are never counted.
> • Money you have already been paid is never touched.
>
> **Leaving**
> • **Leaving is not automatic. You ask the owner and the owner decides.**
> • Say why you want to leave and send anything that backs it up.
> • **Even if the owner lets you leave, you keep paying 10% on the clips you already posted.**
> • The owner can also end it. Then your 10% stops.
> • You keep clipping the whole time you wait.

Then: *"I understand that my trainer takes 10% of my pay after fees."* and
*"Tick the box to say you understand, then press Join."*

The empty state before any code is entered says *"Nothing is agreed until you press
Join."* **It does not read as a trick.** The dollar figure comes before the
percentage, the non-automatic exit is stated in the plainest available words, and
the half of the deal that survives the exit is stated rather than buried. The
$9.10 and $81.90 in that copy are exactly what the production arithmetic produces,
proven independently in PART 4.

### The join boundary, from the clip's own submission time

A clipper with **$60 posted before joining** and **$40 posted after**, withdrawing
$100:

```
eligibleFraction  0.4          (exactly 40/100)
eligibleGross     $40.00
trainer cut       $3.64        ($40 less its 9% share = $36.40, times 10%)
```

**A clip posted before joining is never charged.** With nothing in window the cut
is $0.00, and the lifetime cap stops a second charge on gross already charged
(`capBound = true`).

---

## PART 3 — THE LEAVING PROTOCOL

### The dispute surface: what the owner actually saw, and what he sees now

**This was the finding of the round.** BL-834 made leaving the owner's decision,
which is defensible and is what the consent screen promises. Measured before any
change:

- A clipper opening a dispute **told the owner nothing.** It set `appealStatus =
  "OPEN"` and wrote an audit row. It appeared only inside the
  `GET /api/admin/trainers` payload, so he learned of a person asking to leave by
  happening to open the trainer hub, or by being told outside the platform.
- The owner's decision **told the clipper nothing**, allowed or refused. The route
  even responded *"They can see your reason"* while nothing told them to look.

**A decision nobody is prompted to make is not a protocol, it is a queue with no
bell on the counter.** Fixed in both directions with three notification types.
The clipper's ALLOWED message repeats the money truth the consent screen already
promised rather than only the welcome half:

> **You can leave your trainer.** The owner agreed that you can leave your trainer.
> Your clips from here on pay you the full amount. The clips you posted while you
> were with them keep paying their 10%, which is what you agreed to when you
> joined. Money you have already been paid is not affected.

> **You are staying with your trainer for now.** The owner has looked at your
> request to leave your trainer and decided you stay with them for now. Nothing
> about your money has changed and you keep clipping as normal. You can ask again
> later.

Both are fire-and-forget: a message that cannot be delivered must never stop a
dispute being lodged or a decision standing.

### Every exit, exercised with real money on the ledger

Commissions were minted through the real payout path: a $100 withdrawal stamped a
**$9.10** cut and paid the clipper **$81.90**, and the PAID transition minted it
`AVAILABLE`.

| Exit | What happened |
|---|---|
| **Clipper asks, owner AGREES** | Pairing becomes `ENDED_GOOD_TERMS`, `leftAt` stamped. **The 10% CONTINUES** on the clip posted while trained and **stops** on the one posted after, at exactly **40/150** of the withdrawal. |
| **Clipper asks, owner REFUSES** | Pairing stays `ACTIVE`, money unchanged to the cent, and the clipper is now told. |
| **Bad-faith revoke** | Required phrase `REFUND 9.10`; a wrong phrase refused and the refusal NAMES the phrase and amount. Pending **wiped from the trainer** and **REFUNDED to the clipper, $9.10 to the cent**, one refund row written. |
| **Good-terms wind-down** | Required phrase `SETTLE 9.10`. **Trainer KEEPS** the $9.10, nothing refunded, status `ENDED_OWNER_WINDDOWN`, and **accrual stops dead** even on in-window clips. |
| **Selective revoke** | The untouched pairing stayed `ACTIVE` at `{"AVAILABLE":9.1}` — **unchanged to the cent** while two siblings were ended. |

**BL-824 held**: money already PAID to a trainer stayed paid through every ending.
**BL-627 held**: the clipper had withdrawn $100.00 against $100.00 earned, and the
refund did not raise that. **No `Clip.earnings` moved** on any path.

### The silent trainer, and the two-press claim verified independently

BL-840 reported that stopping a silent trainer takes TWO presses. BL-843 replied
that it *"does not and never did: DEMOTE stops it three ways over"*. The brief
required verifying this rather than inheriting either. **Measured:**

```
before demote:  pairing ACTIVE, pending $9.10
after ONE press (DEMOTE):
   isTrainer            false
   pairing              still ACTIVE
   pending              still $9.10   <- NOT wiped
   trainer cashout      403 "Only a trainer can cash out trainer commission."
   clipper              has NOT got it back
```

**BOTH ARE HALF RIGHT.** Demoting stops the money REACHING the trainer, which is
BL-843's point and is true. It does not RETURN it, which is BL-840's point and is
also true. The $9.10 is **frozen**: reachable by nobody. Returning it to the
clipper still requires the second press, ending each pairing as bad faith.

Reported, not changed. Which of those the owner wants is his decision, and the
route already surfaces the pending figure on demote so the second step is not
invisible.

---

## PART 4 — THE MONEY, COMPUTED BY HAND FIRST

The rule, read out of `computeTrainerCut` before running anything:

```
basis = eligibleGross − platformSideOnEligible − express(excluded)
cut   = round2(basis × 10%)
```

`TRAINER_BASE_INCLUDES_EXPRESS = false`, so express never enters the basis. The
referrer's five points ARE subtracted, so fee plus referral share is always nine
points and the trainer's base does not depend on how the clipper arrived.

**Hand-computed, then confirmed to the cent by the production functions:**

| Case | Basis | Trainer cut | Clipper cash |
|---|---|---|---|
| Unreferred, $100 | $91.00 | **$9.10** | **$81.90** |
| Referred (4% fee + 5% referrer), $100 | **$91.00 — the same** | **$9.10** | **$86.90** |
| Unreferred + express 4% on the GROSS | $91.00 | $9.10 | **$77.90** |
| Referred + express | $91.00 | $9.10 | **$82.90** |
| Trainer's own cashout of $9.10 at 9% | — | fee $0.82 | **$8.28** |

Those first two figures, $81.90 and $86.90, are **exactly what the consent screen
quotes**. The screen and the arithmetic are the same claim.

**A CONTRADICTION SETTLED.** A summary of BL-863 states the trainer cut on a $100
gross is $10.00 and the clipper receives $77.00. The code says **$9.10** and
**$77.90**, because the cut is 10% of the pay AFTER fees, not of the gross. The
code and the consent screen agree; that summary does not. Reported rather than
quietly reconciled.

**24,992 combinations, 0 failures.** Every combination of amount (2,000
cent-granular values plus primes as whole dollars, as sevenths and scaled by
111.11), referred/unreferred, express on/off, and four eligibility fractions:

- `fee + express + trainerCut + clipperCash == gross` **exactly**, every time.
- Nothing ever negative.
- **The trainer base never depends on how the clipper arrived** — after the fix
  below.

### The defect this found, and fixed

**A referred clipper's trainer was paid a cent less for identical work.** The
platform fee and the referrer's five points were rounded to the cent
**separately**, so an unreferred clipper subtracted ONE rounded figure and a
referred one subtracted TWO. Rounding twice is not rounding once.

My first assessment was that this sat below any reachable amount. **That was
wrong, and measurement corrected it.** An exhaustive cent-by-cent scan from the
$10 minimum upward found **461 reachable amounts drifting, on grosses up to
$199.94**:

```
$10.16  unreferred $0.93  vs  referred $0.92
$10.38  unreferred $0.95  vs  referred $0.94
$10.93  unreferred $1.00  vs  referred $0.99
```

Both roundings now derive from the nine-point identity, so it holds by
construction at every amount instead of only where the decimals happen to land.
The unreferred path is arithmetically unchanged, and on the round figures the
consent screen quotes nothing moves. **Exposure at the time of the fix: ZERO** —
no commission has ever been minted on this platform.

### The cut is a stamped deduction and never touches `Clip.earnings`

Proven structurally (`computeTrainerCut` is pure and receives no clip and no
earnings row, so it cannot reach them) and behaviourally: across the whole walk,
`SELECT count(*) FROM clips WHERE ABS(earnings - "baseEarnings") > 0.005` on every
sandbox clip returned **0**.

**A priced payout scales the cut** (`$100` priced to `$40` mints `$3.64`), a price
at or above the gross mints the full stamp and never more, and a payout priced to
`$0.00` mints nothing.

---

## PART 5 — WHAT ONLY BREAKS LATER

| Case | Result |
|---|---|
| **A payout CLOSED with no payment** | A $100 request stamped a $9.10 cut, was closed unpaid per BL-861, and **zero commission rows exist against it.** Money that never moved took no trainer cut with it. |
| A banned trainee | Their trainer's money did not silently move. |
| A banned trainer | Refused at join; the mint gate refuses `status = BANNED`. |
| **A trainer who is ALSO a trainee** | **Allowed.** A live trainer joined another trainer and it returned 200. |
| A trainee who stops clipping | Zero cut, no error. |
| A trainer with many trainees | Dashboard answers correctly for three. |

**Reported, not fixed:** a person can be a trainer and somebody else's trainee at
once, so a **chain** of trainers each taking 10% from the next is reachable.
BL-834's `wouldCreateCycle` blocks cycles, not chains. With one trainer this
cannot occur; it is a day-one watch item, below.

---

## PART 6 — FIXES, CYCLES AND GUARDS

**Three cycles.** Cycle 1 found the dispute-path silence and, through my own
zero-reading guard, discovered every money assertion was running on empty
commissions. Cycle 2 ran with real money and left one failure. Cycle 3 was clean
end to end.

### The five fixes

1. **The nine-point identity** (`trainer-cut.ts`) — 461 reachable one-cent drifts.
2. **Both directions of the dispute path** (`trainer/appeal`,
   `admin/trainers/appeal`, `notifications.ts`) — silence in both directions.
3. **The unguarded `res.json()`** (`TrainerBlock.tsx:222`) — a 200 with an
   unparseable body crashed the entire consent screen to an error overlay. It was
   the ONLY unguarded parse in the file, three lines above three siblings that all
   guard. Caught by rendering `/account` during a cold compile.
4. **A route module exporting a constant**
   (`payouts/trainer-request/route.ts`) — makes Next's generated route types
   reject the file, so `tsc --noEmit` fails the moment `.next/dev` exists. Zero
   importers; the `export` keyword is gone.
5. **The invisible focus ring** (`TrainerBlock.tsx`, three sites) —
   `ring-white/90` is white on white in the light theme, on the three controls
   where somebody agrees to give away 10% of their pay. Now
   `ring-[var(--text-primary)]`: 15.02:1 dark, 18.4:1 light. The dimmed state moved
   from `opacity-60` (label at 2.86:1 on an `aria-disabled` but still-active
   button) to `bg-accent/70`, which dims the fill and leaves the label at 4.66:1.

### The BL-835 guard suite had been red since a refactor

Two of its 85 assertions grepped the route files for phrase constants that had
moved to `trainer-copy.ts`. **Verified against the unmodified base first: 83
passed and 2 failed both with and without my changes**, so these were stale
assertions and not a regression I caused. The behaviour was correct throughout:
both endings do require a typed phrase carrying the amount, and `NEW TRAINER`
shares no token with `SETTLE` or `REFUND`. Repointed at the file the constants now
live in AND at the routes that enforce them. **85/85.**

A suite permanently showing two red is a suite nobody reads, which is exactly how
a real regression hides.

### My own zero-reading guard fired

The first walk passed every money assertion in the bad-faith revoke, the wind-down
and the selective revoke on **empty** commissions, because `POST /api/payouts` had
refused for a missing Discord username and nothing was ever minted. The `3-pre`
check — which asserts the commission helper reads NON-ZERO values before anything
is asserted on it — caught it. Those results were meaningless and are reported
nowhere as proof. This is the same failure BL-864 shipped with a balance helper
that read every account as $0.00.

### The guard, demonstrated failing then restored

```
RUN 1 INTACT   exit 0   19,006 amounts checked, 0 drifting
RUN 2 BROKEN   exit 1   461 drifting, worst gross $199.94
RUN 3 RESTORED exit 0   0 drifting
sha256 before/after identical
```

The broken run restores the exact pre-fix line, and the source is put back in a
`finally` so an interrupted run cannot leave a money rule broken.

### Invariants, unweakened

- **BL-824 paid-is-final** — no PAID commission was ever refunded, through every ending.
- **BL-849's write side** — untouched; this round writes no earnings at all.
- **BL-627 no-overpayment** — the refund did not let a clipper withdraw more than earned.
- **BL-696 no-double-pay** — zero duplicate open payouts per (user, campaign).
- **BL-538 never-decrease** — no `Clip.earnings` moved on any trainer path.
- **The stamped-deduction rule** — the cut exists only on the payout row.

### Renders

**25 shots, 95 assertions, 0 failed**, at 320 / 375 / 414 / 1280 / 1440, real
Chromium with real minted cookies against a dev server running
`DEV_AUTH_BYPASS=false`. **0 at the wrong width, 0 with horizontal overflow.**
Four surfaces: the consent screen empty, the consent offer with the terms shown,
the paired state, the trainer's dashboard, and the owner's hub with a live dispute
open. No wallet address appeared on any trainer surface.

The render pass twice caught defects in **its own method** — a fixed sleep
photographing a loading spinner, and a negative wait that passed instantly against
the wrong placeholder — and once caught a real product defect (fix 3 above).

### Money files

The 6 money files, `tracking.ts` and `campaign-era.ts` are **byte-identical by
blob OID** on the base commit and on this branch:

```
ac5be7de clip-earnings-writer.ts   89292141 tracking.ts
797e2098 earnings-calc.ts          61cef393 clip-earnings-invariant-middleware.ts
81a683c1 balance.ts                ef5cdae7 money-decimal.ts
                                   106e16ad campaign-era.ts
```

`trainer-cut.ts` is not among them and is the one money-adjacent file this round
changed; the full reasoning is in its own header and the change is guarded above.

### Build

- `tsc --noEmit` clean before and after. `eslint` confirmed present, so the hooks
  gate is not silently no-opping: **0 errors, 10 warnings** against a permitted 11.
- `npm run build` exit **0**. Every exit code read from a file, never inferred from
  a pipe or a notification.
- BACKLOG counted with `grep -c`, never piped to `head`: 24,689 → 24,817.
- `checkpoint/BL-723` was **NOT** merged.
- The branch was checked against `main` before pushing; `main` had moved (BL-868
  merged mid-round) and was merged in first, with **zero file overlap** and no
  conflicts.

---

## LAUNCH VERDICT

**Yes — one trainer and a few trainees can run safely tomorrow.**

The money is right to the cent in every combination, the exits all do what they
say, paid money is final in every direction, and the consent screen is honest
about both the cost and the fact that leaving is not the clipper's decision. The
one arithmetic defect found had zero exposure because nothing has ever been
minted, and it is fixed before the first dollar.

**What I would watch on day one:**

1. **The first dispute.** The notification path is new as of this round and has
   never carried a real one. Confirm the owner's bell fires and that he can find
   the hub from it.
2. **The first cashout.** A trainer being paid has never happened on this
   platform. Watch the $9.10-shaped figures, and that the trainer's own 9% comes
   off their side and not the clipper's.
3. **The frozen-money case.** If the first trainer goes quiet and is demoted,
   remember the accrued money is frozen and not returned. Decide deliberately
   whether the clippers get it back, and press the second control if so.
4. **Do not let a trainer become another trainer's trainee.** Nothing refuses it
   and a chain compounds 10% per link. With one trainer it cannot happen; the
   moment there are two, it can.
5. **The pitch link and the code.** Neither can be changed after promotion without
   a demote/re-promote cycle, and the code is not returned when you promote. Hand
   it out carefully the first time.
