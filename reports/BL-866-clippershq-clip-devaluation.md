# BL-866 — Devalue the clips themselves, forward, with a floor that is never silent

**2026-09-09. Shipped. `checkpoint/BL-866` merged to `main` at `1dbafa3b`.**
Requires a Railway redeploy and the additive SQL in
`scripts/migrations/BL-866-devaluation-columns.sql` (already applied to the live
database by this round).

---

## NOTHING UNREMOVABLE. FIRST LINE, AS REQUIRED.

**Zero sandbox rows remain, in any table.** 187 rows were recorded at creation
across two runs (169 + 18) and 187 were deleted; `destroy.ts` re-verified 0 of
187 remaining. A direct query across all eight touched tables (`clips`, `users`,
`payout_requests`, `campaigns`, `audit_logs`, `notifications`, `clip_stats`,
`clip_accounts`) returns `0` for `bl866sbx-%` in every one. No real payout and no
real clip was written. `SELECT count(*) FROM clips WHERE "devaluedAt" IS NOT NULL`
returns **0** — no live clip carries a devaluation.

The platform's totals did move during the round (clips 9,815 → 9,818, users
1,694 → 1,695). That is **live traffic, not this round**: the three clips carry
Prisma cuids (`cmtu5cql0004z0xpis9quhw3t` and two siblings, created 13:41 UTC) and
one real clipper signed up at 13:35 UTC. Measured immediately after teardown and
before that traffic, counts and both fingerprints were **identical** to the
pre-round baseline: clips 9,815 = 9,815, payouts 229 = 229, users 1,694 = 1,694,
`fp_earnings` `da58e5ff861f272a26ba32e6f72686c0` unchanged, `fp_stamps`
`85a1d871532a3d7b30519686b8b55fc5` unchanged.

---

## THE MODEL SPLIT, AND WHAT WAS DELIBERATELY NOT SPLIT

| Work | Model | Why |
|---|---|---|
| Mapping BL-861 / BL-756 / balance + fee constants (3 parallel agents) | Haiku | Retrieval and measurement. No decision. |
| Accessibility review of the new UI against existing patterns | Sonnet-class specialist team | Reviews code, changes none. |
| **Everything money-touching** | **Opus (me)** | See below. |

**NOT SPLIT, and this is the important half.** The scaling arithmetic, the floor
logic, the clamp-versus-refuse decision, what gets written, the route, the
Serializable transaction, the proofs and this report were all done on Opus without
delegation. Every one of them decides money. Delegating the *reading* of
`per-clip-cpm.ts` is safe; delegating the judgement about whether restamping is
retroactive is not, and that judgement turned out to be the round.

**Rough saving:** the three retrieval agents consumed ~271k subagent tokens doing
work that would otherwise have run at Opus rates — roughly a 5x cost difference on
that slice, call it ~$3–4 saved. It is not a large number, and that is the honest
shape of this round: almost all of the work was in the ALWAYS-OPUS category.

---

## PART 0 — THE SHAPE. RESTAMP THE RATE, NOT REWRITE THE EARNINGS.

**CHOSEN: TWO (restamp the CPM).** Stated with the evidence:

- **ONE (rewrite stored earnings) is the shape that broke.** BL-826 multiplied 40
  clips by 0.1825, dropped recorded earnings to $25.65 against $78.54 already paid,
  and jammed Mark Paid at $0.00 against `payout_amount_positive` — five identical
  failures, permanent. BL-716 measured the same shape at $60.47 and a manual
  repair. BL-827 made the owner's figure authoritative and deliberately did **not**
  restore the scaling.
- **TWO is ratio-preserving and already proven.** It reuses BL-756's
  `decidePerClipCpmPair` verbatim, which derives the owner stamp from the clipper
  stamp and the **original** pair at 4dp ROUND_HALF_UP. BL-742 measured
  ratio-preserving scaling at 702 of 702 passing `owner-share-guard.ts:72` against
  648 of 648 ambiguous for clipper-only scaling. BL-539 proved a stamp-versus-share
  mismatch creates permanently ambiguous rows and BL-570 measured one at $933.94.

### The finding that reframed the round: "forward" is not free here

Two facts, both verified in source, that the brief's framing did not assume:

1. **BL-756's gate refuses the entire population this feature is for.**
   `assertForwardOnly` (`per-clip-cpm.ts:253`) refuses any clip that has earned.
   Measured: **4,600 of 8,190** approved clips have earned. Its own header says the
   never-decrease guard "cannot fire, because eligibility requires `earnings = 0`".
   That eligibility is exactly what had to change.

2. **Restamping is NOT retroactively inert.** `calculateClipperEarnings`
   (`earnings-calc.ts:176`) computes `baseEarnings = (views / 1000) * cpm` from
   **total** views. There is no incremental accrual anywhere in the engine. And the
   ordinary non-marketplace write path at `tracking.ts:2883` applies no paid floor
   and no never-decrease guard: `capButNeverBelowStored` at `tracking.ts:2697` sits
   inside the budget-cap branch only, and `clip-earnings-writer.ts` states in its
   own header that "Decreases always pass".

   **So a CPM restamp reaches BL-826's destination one tick later, through the
   sanctioned writer.** The rate change is forward-only; its effect on recorded
   earnings is not. That is why the floor in this round is load-bearing rather than
   decorative, and it is the single most important sentence in this report.

### A clip with no split to preserve — stated, not guessed

A null or zero **owner** stamp means there is no split to keep. The clip is already
ambiguous under `owner-share-guard.ts` and the owner already earns $0.00 on it, so
scaling would preserve that rather than repair it. BL-756 refused 27 of 130 clips
on exactly this. **Measured here: 1,145 of the 4,600 earned clips — 24.9 percent.**

**They are HELD, not devalued, and they still count against the floor in FULL.** A
held clip keeps its rate and therefore keeps its money, so it contributes its whole
current value to the projected position total. That is the conservative direction:
holding money the owner wanted removed can only make the floor easier to clear. Each
one is listed on screen with its reason, never silently skipped.

---

## PART 1 — THE FLOOR: IT CLAMPS, AND IT SAYS SO

### The measurement that decided it

Across the full live population:

| | |
|---|---|
| (clipper, campaign) positions | **415** |
| positions carrying paid money | **74** |
| **of those, would breach the floor at BL-826's 0.1825** | **74 — all of them** |
| positions already below paid (pre-existing) | **17**, carrying **$1,893.34** |

"Refuse entirely on breach" is therefore not a policy, it is a switch that turns
the feature off for every clipper who has ever been paid. A silent clamp is worse
than either, because the owner believes he priced at 20 percent when he did not.

### The decision

**CLAMP AT THE FLOOR, AND STATE IT LOUDLY.** The devaluation goes as far down as
the floor allows and stops there. The owner's screen receives `clamped`,
`requestedRatio`, `effectiveRatio` and the floor itself, and shows all four.

**The rejected alternative, with its arithmetic.** "Scale only the unpaid portion"
is `new = paid + (recorded − paid) × ratio`. On BL-826's numbers (recorded $140.54,
paid $78.54, ratio 0.1825) it yields **$89.86** where the clamp yields **$78.54**.
Both hold the floor; the clamp is strictly closer to what the owner asked for, and
the floor is a safety constraint rather than a preference, so there is no reason to
stop above it.

**A position already below paid is REFUSED, not deepened**, with every proposal
stripped from the response — returning stamps beside a refusal would put figures on
screen that look like a plan and are not one.

### Why the floor lives at the gate, not the write site

`tracking.ts` is a money file in the hot earnings path. BL-849 put the marketplace
poster floor at its call site there and said why. **This round does not need to**,
because the projected post-devaluation total is a *minimum* over time:

```
projected(t) = (views(t) / 1000) × newCpm,   views non-decreasing
⇒ projected(t) ≥ projected(now) for every later tick
```

Choose the ratio so `projected(now) ≥ paid` and the floor holds at every future tick
with **not one line of `tracking.ts` changed**. That is why the 6 money files,
`tracking.ts` and `campaign-era.ts` are byte-identical.

**The projection is a proven lower bound, not an assumption.** Projecting linearly
as `currentEarnings × (newCpm / currentCpm)` is conservative even where a per-clip
cap binds: if `maxPayoutPerClip` binds today then `current = cap` and `raw ≥ cap`,
so after scaling `true = min(raw × ratio, cap) ≥ cap × ratio = projection`.

### PROVEN ON BL-826's EXACT SCENARIO

40 clips, $140.54 recorded, $78.54 already paid, ratio 0.1825 — run through the
**real route** over HTTP with a real owner session:

```
requested ratio   : 0.1825
effective ratio   : 0.559941   ← clamped
paid floor        : $78.54
current total     : $140.54
projected total   : $78.54     ← FLOOR HOLDS, exactly
Mark Paid on $11.00 -> cash $10.01   ← POSITIVE
```

The unclamped shape reproduces the historic failure precisely:
`round2(140.54 × 0.1825) = $25.65`, which is BL-826's recorded figure to the cent.

**What the owner sees, verbatim:**

> You asked for 18.3%. This clipper has already been paid $78.54 on this campaign,
> and recorded earnings can never fall below money already paid. These clips have
> been set to 56.0% of what they were worth, which is as far down as they can go.

The typed confirmation phrase carries the **applied** figure (`devalue 56.0`), not
the one he typed — the same reasoning as BL-861's price dialog asking for the cash
rather than the gross. He physically cannot complete the action while believing he
chose 20 percent.

---

## PART 2 — THE ARITHMETIC, EXACT TO THE CENT

### What absorbs the remainder

There are two roundings and they are different questions.

**WITHIN A CLIP — the split. The OWNER side absorbs it**, named and unchanged from
BL-756: the clipper's rate is the exact scaled figure, the owner's is derived and
carries the fractional remainder, at most $0.00005 per 1,000 views. This round
reuses that decider rather than restating its formula.

**ACROSS THE POSITION — the floor. NO ROW ABSORBS A REMAINDER, deliberately.** The
floor is a `≥` constraint, not an equality. Forcing the per-clip parts to sum to an
exact target would require writing the earnings rows directly, which is shape ONE,
which is the shape that jammed a payout permanently. Instead the effective ratio is
verified against the **actual 4dp-rounded stamps** and corrected proportionally
until the projection clears the floor. **Every rounding decision on this path is
directed toward the clipper.**

That correction is proportional, not a fixed step, and that mattered: the first
implementation nudged by one 4dp tick at a time and gave up still short on large
positions — **9,123 floor breaches across 52,650 generated cases, worst $1.00.**
After the fix: **0 breaches.**

### Results — 8,156 checks, 0 failed

| Property | Cases | Failures |
|---|---|---|
| Floor never breached (primes 2–113, totals $0.01–$99,999.99, 13 ratios, 9 floor fractions) | 52,650 | **0** |
| Clamp actually exercised | 27,214 clamped | — |
| Split preserved within `owner-share-guard`'s 0.01 tolerance | 343 pairs | **0** (worst drift 0.00162) |
| **Fee stack tiles the gross exactly** | **41,300** | **0** |
| Marketplace 60/30/10 tiles the gross | 572 | **0** |

The fee stack covers every combination of: the **9 percent** platform fee, the
**4 percent** referred rate, the **4 percent express premium charged on the GROSS**
(BL-763/BL-863), and the **trainer cut taken after the platform fee** (BL-835),
across 2,000 cent-granular amounts plus primes as whole dollars, as sevenths, and
scaled by 111.11. The asserted property is `fee + express + trainerCut + final ==
requestedAmount` exactly, plus `expressFeeAmount == round2(gross × 0.04)` on the
gross rather than the post-fee amount, plus no negative component anywhere.
**No combination creates or loses a cent.** BL-863's worked example reproduces
exactly: $100 express → **$87.00**.

---

## PART 3 — FORWARD, AND VISIBLY REVERSIBLE

**Accrued-but-unpaid views ARE affected, and it is explicit rather than implicit.**
Because earnings re-derive from total views, the lower rate applies to views the
clips already have as well as new ones. This is stated in the dialog
("The lower rate applies to the views these clips already have, as well as new
ones"), in the clipper's message, in the BACKLOG entry and here. The alternative
would be a clipper watching a figure fall and inventing an explanation.

**Money already paid is never affected.** That is what the floor is.

### The undo, and why it does NOT reuse BL-756's Orig pair

Five new nullable columns hold the rate each clip had **immediately before this
devaluation**: `devaluedAt`, `devaluedById`, `devaluedRatio` (6dp — the clamp lands
on figures like 0.559941 and storing it rounded would make the audit disagree with
the stamps it produced), `devaluedPrevClipper`, `devaluedPrevOwner`.

`cpmOverrideOrigClipper` / `cpmOverrideOrigOwner` hold the rate before the **first**
rate change of any kind. That is exactly right for BL-756's non-compounding rule and
exactly wrong for an undo: if the owner sets a per-clip override and *then* devalues,
restoring the BL-756 pair would silently discard the override he chose on purpose.
The undo restores the BL-756 marker only when the rate it is restoring **is** the
Orig pair, returning a never-overridden clip to a virgin state.

**Proven: stamps restored to the digit** (string equality on the Decimal, all clips),
marker cleared on every clip, and the clipper is told it was undone.

**This does not create a second BL-864 trap.** The undo is on the same row, present
only when there is something to undo (presence, not a disabled control — the same
test as Reopen), its confirmation phrase carries the dollars coming back
(`restore <amount>`, the one figure the owner cannot derive from the ratio), and the
row states the state in words at all times: "Clips devalued to 56.0%" or "Clips at
full rate".

**Every devaluation writes an audit row** — `CLIP_DEVALUATION_APPLIED` on the payout
row — naming the owner (`userId`), the clipper, the campaign, the requested and
effective ratios, `clamped`, the paid floor, current and projected totals, the held
clip ids, **every clip with its before and after stamps**, the reason, and a
timestamp. Undo writes `CLIP_DEVALUATION_UNDONE` with the from/to pair per clip.

---

## PART 4 — WHAT THE CLIPPER SEES

BL-756's pay-cut warning exists for a clip **moved** to a lower-paying campaign and
says "this clip will earn less than the campaign it was submitted to". That is true
of a one-off move and **wrong about the scope here**, so this is its own message
rather than a reuse that would be accurate in direction and misleading in extent.

**Title:** `Your clips on this campaign now pay a lower rate`

**Body, quoted exactly as the server composes it:**

> We have lowered the rate on 5 of your clips on Zhus Edit to 20.0% of what it was.
> This is ongoing: those clips now earn at the lower rate on the views they already
> have and on any new views they get. Money you have already been paid is not
> affected and will not be taken back. Your other campaigns are not affected.
> Reason: Only 5% of the views were from the countries this campaign is for, against
> 40% expected. You have not broken any rule and this is not a warning. If you think
> it is wrong, open a support ticket and we will look at it again.

Written to BL-518 and BL-521: plain language, no blame, the bad news first rather
than buried under a softener, the ongoing effect named explicitly, and what is *not*
affected stated — because the most frightening reading of "your clips are worth
less" is "they are taking back money I have already been paid", and they are not.
No dashes as bullets, no emoji.

**The pay-cut warning fires, verified:** the notification was asserted present and
its body asserted to contain both the ongoing sentence and the paid-money-is-safe
sentence (checks D12/D13/D14, all PASS). BL-736's null-stamp suppression cannot
apply: this path does not compare against a possibly-null old stamp, it reports the
ratio the server computed. **The reason field is required** (minimum 3 characters,
refused server-side) — a message with a blank reason would be worse than none.

Undo sends its own message: *"Your clips are back to their full rate."*

---

## PART 5 — THE CLOSE-DIALOG TRAP BL-864 FOUND

BL-864 measured that closing a request erases a set price and reopening does not
restore it, and recommended exactly this as the next small change. Added in **both**
steps — a warning only in staging is absent at the moment of decision, and only in
the confirm arrives after the reason has been written.

**Staging list item, quoted:**

> • Closing clears any amount you set on this request, and reopening does not bring
> it back. You would need to set it again.

**Confirm body, appended, quoted:**

> Closing also clears any amount you set on this request, and reopening does not
> bring it back.

Rendered and asserted present at 1280 (check PASS).

---

## PART 6 — THE PROOFS

### Sandbox, against the REAL routes — 40 checks, 0 failed

A dev server on port 3866 with `DEV_AUTH_BYPASS=false`, driven over HTTP with a real
minted owner session. Fixtures are direct Prisma inserts (there is no product route
that can put a clip on an `isTestCampaign` campaign — BL-840 measured both submit
paths refusing); **every devaluation and undo ran through the real route**, the real
`decideDevaluation`, the real Serializable transaction, the real audit writer and the
real notification path.

| Scenario | Result |
|---|---|
| Clean devaluation to 20% (5 clips, no payments) | ratio applied exactly; every stamp scaled by 0.2; split survived; **earnings NOT written by the route** |
| Undo | stamps restored to the digit; marker cleared; clipper told |
| **BL-826's exact scenario** | clamped 18.3% → 56.0%; projected $78.54 ≥ paid $78.54; **Mark Paid $10.01** |
| A clip with no split to preserve | exactly the 4 splitless clips held, reason named, rates untouched |
| A fully paid position ($60 recorded, $60 paid) | recorded never fell below paid |
| A position already below paid ($40 recorded, $90 paid) | **REFUSED**, nothing written |
| **Two owners at once** | 200 / 409 — **one ratio** across the position, floor still held |

### All four invariants, across the FULL population

Measured as a **before/after comparison**, not an absolute — and that mattered. The
first attempt reported 18 "new" overpaid positions that were untouched real rows,
because "one payout row exceeds its position" is a different condition from "summed
paid exceeds the position" and the below-paid baseline could not classify it. With
its own baseline:

- **BL-824 paid-is-final** — 0 positions pushed below paid by this round (16 were
  already below before it ran).
- **BL-538 never-decrease** — 0 clips had stored earnings written down.
- **BL-627 no-overpayment** — 0 new; the 26-position baseline is untouched.
- **BL-696 no-double-pay** — 0 duplicate open requests per (user, campaign).

### THE GUARD, DEMONSTRATED FAILING, THEN RESTORED

```
RUN 1 INTACT   exit 0   floor holds, projected $78.54
RUN 2 BROKEN   exit 1   projected $25.60 vs $78.54 paid — FLOOR BREACHED
RUN 3 RESTORED exit 0   floor holds again
sha256 before/after: 40b3c697...aff8c0  — byte-identical
```

**The first attempt at this demo reported itself INCONCLUSIVE rather than passing
falsely**, and that is how it found something real: disabling the initial clamp left
the proportional nudge loop still raising the ratio, so the "broken" run passed. **The
floor is three enforcement points, not one** — the clamp, the re-verification against
the actual 4dp stamps, and the final assertion that refuses to propose anything still
short. All three must be disabled for the protection to be absent. The source is
restored in a `finally`, so an interrupted run cannot leave a money guard off.

### Helpers verified to read real values

BL-864 caught its own proof passing on a helper that read every balance as $0.00.
`earningsUnchanged` here **fails loudly** if it reads zero rows or if every earnings
value it reads is 0, before it is allowed to return true.

### Renders — 21 shots, 78 assertions, 0 failed

320 / 375 / 414 / 1280 / 1440, real Chromium, real owner cookie, `window.innerWidth`
printed beside every shot. **0 at the wrong width, 0 with horizontal overflow.** Five
surfaces: the row, the empty stage, the clamped stage, the typed-phrase confirm, and
the Close dialog. Nothing was confirmed — the final button was never pressed.

The render pass caught a real accessibility defect: **the clamp sentence rendered
twice**, once in the live region and once in the bordered block, so a screen reader
would have read a four-figure sentence twice. The live region is now `sr-only` and
the visible statement is the block — one string, from one server field, placed once
each. Fixed and re-rendered clean.

It also caught a defect in its **own** method twice: a fixed sleep photographed the
loading placeholder at 320 (the first width pays for the dev server compiling), and
the replacement negative wait passed instantly against the *other* placeholder. The
final wait is positive — it waits for the clamp sentence the server actually
produced.

### Accessibility

Reviewed by the specialist team **before** any UI was written, and its prescriptions
were followed: one discriminated union rather than booleans (two portalled traps
deadlock the keyboard); every figure frozen into the confirm member at Continue;
`aria-disabled` with an in-handler return rather than native `disabled` (the shared
`Button` hard-wires `disabled={disabled || loading}` and the focus trap excludes
`[disabled]`, so a busy dialog would have zero tab stops); one priority-ordered
`sr-only` gating sentence; `readOnly` not `disabled` on inputs while busy; the panel
focused on open, not the first field; focus returned by `data-action` rather than
"the row's first button"; `role="region"` + `tabIndex` + accessible name on the
scroll container; `scope="col"`/`scope="row"`, an `sr-only` caption, units in the
headers, and held rows carrying a real identical figure with `sr-only " unchanged"`
rather than a blank money cell. Rates use `fmtRate` (4dp) and earnings
`formatCurrency` (2dp) — BL-756's defect was a dialog printing $0.1279 and $0.1312
identically as "$0.13". `--bg-page` was avoided (42 uses, 0 definitions).

---

## MONEY-FILE SAFETY

**The 6 money files, `tracking.ts` and `campaign-era.ts` are BYTE-IDENTICAL by blob
OID on the base commit, on `checkpoint/BL-866` and on `main`:**

```
ac5be7de  clip-earnings-writer.ts        892921416  tracking.ts
797e2098  earnings-calc.ts               61cef393   clip-earnings-invariant-middleware.ts
81a683c1  balance.ts                     ef5cdae7   money-decimal.ts
                                         106e16ad   campaign-era.ts
```

No `writeClipEarnings` call was added. **This round writes no money at all** — two
CPM stamps and five nullable provenance columns per clip, and nothing else. It does
not touch the payout row: not `amount`, not `actualPaidAmount`, not `status`, not a
fee column, not `settledUnpaidAt`, not `sentToAdminAt`. So BL-861's price control,
BL-864's admin-handoff marker and the settle flow are arithmetically out of reach,
the settle dialog's typed phrase cannot change underneath the owner, and the
constraint BL-826 jammed guards a column this route never writes.

Schema changes are **additive and nullable**, applied via `ALTER TABLE ADD COLUMN IF
NOT EXISTS` through `run-schema-sql.js` and `prisma generate` — never `prisma
migrate`. Zero backfill, so every existing row is byte-identical.

No Apify actor ran. The 11 BL-678 guards are untouched. The connection pool was not
exhausted; the dev server was killed by PID from `netstat` on the one port, never by
image name. No wallet address is printed anywhere in this report and handles are the
sandbox marker only.

---

## TWO DEFECTS THIS ROUND CAUSED AND FIXED, BOTH CAUGHT BY ITS OWN PROOFS

**1. A failed production build, and BL-863 recorded the identical shape one round
earlier.** The client page imported `pctText` from `clip-devaluation.ts`, which
imports `Prisma` for Decimal, so `node:module` landed in the browser bundle and
Turbopack failed with *"the chunking context does not support external modules"*.
BL-863's own root cause was `mintableTrainerCutAmount` being pure but living in a
module that imported `db`, which forced three implementations of one rule.
`pctText` now lives in `rate-format.ts`, which is client-safe, and the server, the
screen and the audit row call the one definition.

**I nearly reported that build as green.** The background task notification said
"exit code 0" while the log said `Build error occurred`; the real
`BUILD_EXIT=1` was in the file I had written it to. The exit code was read from the
file, not the notification, for every build after that.

**2. A runtime bug tsc could not see.** The route's `CLIP_SELECT` asked for `url`
when the Clip column is `clipUrl`. `loadPosition(tx: any)` bypassed type checking, so
tsc passed; only the sandbox run against the real route found it.

---

## BUILD, MERGE, PUSH

- `tsc --noEmit` clean **before** any change (baseline exit 0), on the branch, and
  post-merge. Every reported exit code was echoed from the process, never inferred
  from a pipe.
- `npm run build` exit **0** on the branch and post-merge. `eslint` confirmed present
  (`node_modules/.bin/eslint`) so the hooks gate is not silently no-opping:
  **0 errors, 10 warnings** against a permitted 11.
- Merge tree OID `8fa49921` is **identical** to the branch tree OID, so the branch
  build provably is the merge build; it was re-run anyway.
- Tags: `pre-BL-866`, `post-BL-866-branch`, `pre-merge-BL-866`, `post-BL-866-merge`.
- BACKLOG counted with `grep -c` (never piped to `head`): 24,515 → 24,613 lines.
- **`checkpoint/BL-723` was NOT merged.** Only `checkpoint/BL-866` was.
- Pushes verified per BL-288: `origin/checkpoint/BL-866 == fae4bbf`,
  `origin/main == 1dbafa3`.

**A branch-drift incident, disclosed.** The first push reported "attempt OK" and then
correctly refused: `HEAD` had drifted to `main`, so both commits landed on `main`
instead of the branch. Nothing had been published (`origin/main` was still
`2d6387d`). Repaired per the rulebook — `checkpoint/BL-866` moved onto the commits,
`main` reset to the branch point — then the branch was pushed, and `main` took them
through a proper `--no-ff` merge. safe-push's verification is the reason this was
caught rather than shipped; its own "push attempt OK" line was the misleading part.

**Collision avoidance:** no worktree was used (the round runs alone and the tree was
clean of tracked changes at the start), no other agent held the tree, and no live
claim file existed. There is consequently **no worktree to verify gone** — `git
worktree list` shows only the main checkout.

---

## STILL OPEN, REPORTED NOT FIXED

- **`audit_logs.details` is a TEXT column holding a JSON string**, so every reader
  must `JSON.parse` it. Reading it as an object silently yields `undefined` for every
  field — a test that passes on nothing, which is what happened here before it was
  caught. Truncation is structurally unreachable for this feature: a 40-clip
  devaluation writes 5.7KB against `AUDIT_DETAILS_MAX_BYTES` of 100,000, and
  `loadPosition` caps a position at 500 clips.
- **The 17 pre-existing below-paid positions ($1,893.34)** are untouched and remain
  what BL-824 reports as `paidNoLongerOffsetting`. This round refuses to devalue any
  of them.
- **BL-865 has no BACKLOG entry.** It appears once in the file, in passing; its round
  shipped (`2d6387dd`) without the standing record every other round has.
- **`--bg-page` remains undefined** at its other sites and in the rulebook itself.
  This round avoided it; BL-861 measured 42 uses and 0 definitions.
- **A devaluation is invisible to `force-recalc-earnings`.** That route wires
  `decideNeverDecrease` (`:294`), so between a devaluation and the next tracking tick
  a force-recalc would refuse to write the clip down. The devaluation lands via the
  tick, not via force-recalc. Harmless today and stated so it is not discovered later.
