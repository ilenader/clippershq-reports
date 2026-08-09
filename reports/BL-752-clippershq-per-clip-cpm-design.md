# BL-752 — Per-clip CPM override: complete design

AUDIT ONLY. No code or data changed. Nothing restamped. All timestamps cast `::text` against DB `now()`
(`2026-08-09 18:00:02.998624+00`). Handles redacted. No live round's files touched (BL-751).

---

## THE FINDING THAT DECIDES THE BUILD

**A per-clip CPM override does not need a new rate column. It already exists, and it is the two frozen
stamps.** `cpmAtSubmissionDecimal` + `ownerCpmAtSubmissionDecimal` are read end to end by every money path,
and `owner-submit-core.ts:330-336` already ships a per-clip custom rate by writing exactly those two fields.

The tempting alternative is a trap. `cpm.ts:170-171` reads `clip.clipperCpmOverride` / `clip.ownerCpmOverride`
at the TOP of its resolution order, and `cpm.ts:147` documents them as "per clip override; rare". Neither is a
column, and neither is reachable. I checked all nine `resolveClipCpms` call sites: every one passes a
hand-built object literal with exactly three keys, `platform`, `cpmAtSubmissionDecimal`,
`ownerCpmAtSubmissionDecimal`.

| call site | shape |
| --- | --- |
| `tracking.ts:2032` | 3-key literal |
| `tracking.ts:2068` | 3-key literal |
| `gamification.ts:826` | 3-key literal |
| `agency-monitor.ts:125` | 3-key literal |
| `proportional-cut.ts:125` | 3-key literal |
| `clips/[id]/review/route.ts:473` | 3-key literal |
| `clips/[id]/override/route.ts:268` | 3-key literal |
| `admin/fix-earnings/route.ts:202`, `:255` | 3-key literal |
| `admin/force-recalc-earnings/route.ts:347` | 3-key literal |
| `owner-submit-core.ts:347` | 3-key literal |

Nine of nine, zero pass an override key. So adding `clipperCpmOverride`/`ownerCpmOverride` columns would
change nothing until all eleven literals were edited, and two of them are inside `tracking.ts`, a money file.
That is a money-file diff, in the hot earnings path, to reach a behaviour the stamps already deliver.

`clipperCpmOverride` also is not what its name suggests. It is an in-memory parameter to
`recalculateClipEarningsBreakdown` (`earnings-calc.ts:356`, consumed at `:379`), it is **clipper only**, and
there is no owner counterpart anywhere in `earnings-calc.ts`. Its single caller is `cpm-restamp.ts:153`. A
design built on it would move the clipper's rate while leaving the owner's untouched, which is precisely the
split break the owner has ruled out.

**Verdict: write the two stamps. Add no rate column.** One additive nullable column is still recommended, for
a different reason, in PART 6 failure mode 6.

---

## PART 1 — THE ARITHMETIC, AND WHY THE GUARD CANNOT FAIL

### The test being satisfied

`owner-share-guard.ts:57-79`:

```
impliedByLockedShare = s / (1 - s)            // s = campaign.lockedOwnerShareDecimal
stampedRatio         = ownerCpm / clipperCpm  // the two resolved stamps
if (|impliedByLockedShare - stampedRatio| > 0.01) -> "ambiguous"  // owner earns $0.00
```

Two properties of that line matter and are easy to misread. The tolerance is **on the ratio, not on the CPM**,
so its difficulty scales inversely with the CPM. And the guard is **always armed**: measured across every live
clip, `guaranteeOwnerSplit` is `true` on 100% of them (PART 2 table, `guarantee_on` equals `clips` in all ten
rows). There is no "guarantee off" path to fall back on.

### The formula

```
r             = oldOwnerCpm / oldClipperCpm        // from the clip's two stored stamps
newOwnerCpm   = round4(newClipperCpm * r)          // owner side derived, never typed
newClipperCpm = exactly what the owner typed
```

`stampedRatio` after the write is `round4(newClipperCpm * r) / newClipperCpm`, which is `r` up to rounding.
`impliedByLockedShare` does not move, because `s` is a campaign field and the override does not touch it.
**The guard therefore returns the identical verdict before and after, by construction.** This is not
"probably passes"; it is the same comparison on the same two numbers. That is why BL-742 measured 702 of 702
passing for ratio-preserving scaling against 648 of 648 ambiguous for a clipper-only change.

### Rounding, and the side that absorbs it

Both stamps are `Decimal(10,4)` (`schema.prisma:988-989`), so the rule is **round half up to 4 decimal
places**, not to cents. Money written downstream stays 2dp; only the rates are 4dp.

Rounding `newOwnerCpm` perturbs the ratio by at most `0.00005 / newClipperCpm`. Setting that below the
guard's `0.01`:

```
0.00005 / newClipperCpm <= 0.01   =>   newClipperCpm >= 0.005
```

Any clipper rate at or above **half a cent per 1,000 views** is safe. Every live CPM on the platform is at
least $0.05, a margin of more than 100x. At the owner's own $0.50 example the induced error is 0.0001, one
hundredth of the tolerance.

**The absorbing side is the OWNER side, named and deliberate.** The clipper's rate is exactly the number the
owner typed, to the digit. The owner's rate is the derived one and carries the fractional remainder. The
reason is that the clipper is the party being promised a number and must see it honoured exactly, while the
owner is the party making the decision and absorbs at most $0.00005 per 1,000 views.

### Worked examples

| case | old pair | s | implied | typed clipper | derived owner | new ratio | diff | verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| owner's 50/50 | $0.3000 / $0.3000 | 0.5 | 1.0000 | **$0.50** | **$0.5000** | 1.0000 | 0.0000 | PASS |
| BL-743 live | $0.2000 / $0.1279 | 0.39006 | 0.6395 | $0.50 | $0.3198 | 0.6396 | 0.0001 | PASS |
| non-dividing | $0.2000 / $0.1279 | 0.39006 | 0.6395 | $0.33 | $0.2110 | 0.63939 | 0.00011 | PASS |
| boundary | $0.2000 / $0.1279 | 0.39006 | 0.6395 | $0.005 | $0.0032 | 0.6400 | 0.0005 | PASS |
| zero owner rate | $0.2000 / $0.0000 | any | > 0 | any | $0.0000 | 0 | > 0.01 | **REFUSE** |
| absent owner stamp | $0.2000 / null | any | > 0 | any | undefined | n/a | n/a | **REFUSE** |

The 50/50 row is the owner's stated rule, satisfied exactly: he sets the clipper to $0.50 and his own side
becomes $0.50 with zero ratio drift.

The last two rows are the honest limit. A clip whose owner stamp is null or zero has **no split to preserve**.
Such a clip is already `ambiguous` under today's guard and already earns the owner $0.00. Scaling preserves
that, it does not repair it, and pretending otherwise would be inventing a split the campaign never locked.
Refuse, and say why in the UI. This is a real population: 49 live clips (PART 2).

### BL-630's ghost fee

The platform fee is applied to the clipper's gross downstream of the rate and is stamped at approval
(`feePercentAtApproval`). Changing the pair does not restate a stored fee. Because eligibility (PART 2)
admits only clips that have never earned, and most of those are PENDING with no fee stamped yet, no fee row is
rewritten and no ghost fee is created. On an APPROVED never-earned clip the stamped percent is reused
unchanged, so the fee scales with the new gross exactly as it would have on a fresh approval.

---

## PART 2 — THE BOUNDARY, WITH LIVE COUNTS

### Measured population (2026-08-09 18:00:02 UTC, non-test, not deleted)

| clip status | campaign | clips | earned | never earned | both stamps | owner stamp missing | guarantee on |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PENDING | ACTIVE | 18 | 0 | **18** | 14 | 4 | 18 |
| PENDING | PAUSED | 2 | 0 | 2 | 1 | 1 | 2 |
| APPROVED | ACTIVE | 361 | 256 | **105** | 316 | 45 | 361 |
| APPROVED | PAUSED | 1298 | 535 | 763 | 549 | 749 | 1298 |
| APPROVED | PAST | 2605 | 1207 | 1398 | 427 | 2178 | 2605 |
| REJECTED | ACTIVE | 54 | 0 | 54 | 45 | 9 | 54 |
| REJECTED | PAUSED | 405 | 0 | 405 | 80 | 325 | 405 |
| REJECTED | PAST | 444 | 0 | 444 | 116 | 328 | 444 |
| FLAGGED | PAUSED | 1 | 0 | 1 | 0 | 1 | 1 |
| FLAGGED | PAST | 5 | 3 | 2 | 0 | 5 | 5 |

Three facts fall straight out. `guarantee_on` equals `clips` in every row, so the guard is universal. The
clipper stamp is never missing, zero across all 5,193 rows, so `r`'s denominator always exists. And the owner
stamp is missing on 49 live clips, which is the refusal class above.

### The rule

**Forward only. Refuse outright on any clip that has earned.** All of these must hold:

1. `earnings = 0 AND baseEarnings = 0 AND bonusAmount = 0`
2. no `AgencyEarning` row exists for the clip
3. `isDeleted = false`
4. campaign status is `ACTIVE`
5. both stamps present and `> 0`, or a live campaign pair is available to derive `r` from

**Eligible and live: 123 clips** (18 PENDING/ACTIVE + 105 APPROVED/ACTIVE), before rule 5 removes up to 49.
The refusal population that matters is the **256 APPROVED/ACTIVE clips that have already earned**; those are
BL-742's class, where a retroactive change put 37 pairs below money already paid with $1,103.41 of shortfall.

Condition 4 is a recommendation rather than a necessity. 2,161 never-earned clips sit on PAUSED and PAST
campaigns; they do not accrue, and PAST is era-frozen (budget exhaustion permanently ends an era). Allowing
them would be legal and pointless, and it would put a live write next to the era boundary for no gain.
Restrict to ACTIVE.

### Reuse of `cpm-restamp.ts`: shape yes, function no

`restampSingleClip` is close to right. It writes both stamps in one `tx.clip.update` (`:183-189`), routes the
invariant fields through `writeClipEarnings` (`:191-195`), upserts `AgencyEarning` for CPM_SPLIT (`:206-221`),
applies `payoutReductionCap`, and runs per clip so one failure does not roll back others.

It cannot be called as it stands. Its signature (`:90-97`) takes `oldCpms`/`newCpms` as **campaign** field
bundles and derives the pair at `:114-118` from `getCampaignCpmForPlatform`. There is no way to hand it a
per-clip pair. And it has no guard of any kind: it computes `newEarnings` and writes it, in either direction.

**Recommendation: a new file `src/lib/per-clip-cpm.ts` that reuses the transaction shape, not a signature
change to `cpm-restamp.ts`.** Three reasons. The bulk path `restampClipsForCampaign` runs over whole
campaigns on every campaign CPM edit, and widening its inner function's contract puts that blast radius at
risk for a single-clip feature. The guard sets genuinely differ. And it keeps `cpm-restamp.ts` byte-identical
apart from the one-line skip in PART 6.

### Where `decideNeverDecrease` goes, and where the paid floor does not

`decideNeverDecrease` goes at the point corresponding to `cpm-restamp.ts:176`, after `next` is computed and
**before** `db.$transaction` opens. Call `decideNeverDecrease(clip.earnings, newEarnings)`; on
`allowed === false`, abort the entire operation, write nothing, and surface the reason. Log through
`logNeverDecreaseBlock`.

**Stated plainly: on the eligible population this guard can never fire.** Eligibility requires
`earnings = 0`, so `stored = 0` and every proposal is `INCREASE` or `UNCHANGED`
(`earnings-never-decrease.ts:98-113`). It is defence in depth against a future eligibility bug, not the
mechanism. The thing that actually makes this forward-only is the eligibility predicate, re-checked inside the
transaction under `FOR UPDATE`.

**BL-718's paid floor has no correct wiring point in this feature, and adding one would be cargo cult.**
`capButNeverBelowStored(cap, stored)` returns `max(cap, stored)` and belongs at cap sites, where a budget or
pool ceiling could write a clip down. This feature has exactly one cap site, the `applyPayoutReductionCap`
mirror of `cpm-restamp.ts:159-162`, and the floor is a no-op there: on a never-earned clip `stored = 0` so
`max(cap, 0) = cap`, and on an earned clip we have already refused. The floor never fires on a decrease today
because it does not observe decreases at all; it prevents the creation of a below-paid state and cannot
detect an existing one. The protection here is the refusal, not a floor.

---

## PART 3 — EVERYTHING DOWNSTREAM

Every site below resolves a per-clip rate from the two stamps and therefore honours the override with **no
code change**. That is the whole argument for the stamp design.

**Rate resolution**
- `tracking.ts:2032` — `resolveClipCpms`, owner side, the hourly tick
- `tracking.ts:2110-2122` — `recalculateClipEarningsBreakdown`, clipper side, stamp passed at `:2122`
- `tracking.ts:2068` — marketplace single-rate resolution
- `gamification.ts:826` / `agency-monitor.ts:125` / `proportional-cut.ts:125`
- `clips/[id]/review/route.ts:473` / `clips/[id]/override/route.ts:268`
- `admin/fix-earnings/route.ts:202` and `:255` / `admin/force-recalc-earnings/route.ts:347`
- `owner-submit-core.ts:347`
- `earnings-calc.ts:379-385` — the internal order; `cpmAtSubmissionDecimal` is layer 2
- `cpm.ts:170-171` — the unreachable override branch. **Leave it alone. Do not wire it.**

**Guard consumers** (verdict unchanged by construction, PART 1)
- `owner-share-guard.ts:72` — the ratio test itself
- `gamification.ts:884`, `agency-monitor.ts:171`, `force-recalc-earnings/route.ts:369` — `decideOwnerGross`
- Not wired to the guard: `tracking.ts` and `cpm-restamp.ts:206-221` write agency earnings through the legacy
  formula without `decideOwnerGross`. **Pre-existing inconsistency, reported not changed**, per the standing
  rule on out-of-scope findings. It does not block this feature, because ratio preservation keeps both the
  guarded and unguarded formulas on the same rates.

**BL-642's two spend filters, both of which must keep `videoUnavailable: false`**
- `campaigns/spend/route.ts:68`, and the agency legs at `:169` and `:174`
- `balance.ts:312`, `:326`, `:330`, `:350`

**Budget and caps.** An override raises a rate, so projected spend rises and the campaign can reach its cap
sooner and auto-pause (`lastBudgetPauseAt`). That is correct behaviour and preserves BL-627's no-over-budget
property, but the owner must see it coming, so the confirmation states the campaign's remaining budget.
No-overpayment is preserved because nothing here raises a cap or writes above one.

---

## PART 4 — THE OWNER UI

Owner only, on the single admin clip row. Never batch: 123 eligible clips is a number you act on one at a
time, and a bulk control here is a bulk mistake.

The confirmation must show, **all six labelled**, because BL-744 just fixed exactly this confusion:

```
Clipper rate now          $0.30 per 1,000 views
Clipper rate after        $0.50 per 1,000 views
Your rate now             $0.30 per 1,000 views
Your rate after           $0.50 per 1,000 views
Split                     50% you / 50% clipper  (unchanged)
Campaign budget left      $X of $Y
```

Plus one plain sentence: "You set the clipper rate. Your rate is calculated so the split stays identical."
Written for a 15-year-old new clipper, no jargon, no ratio, no decimals beyond cents on screen.

**Typed confirmation.** The owner types the new clipper rate exactly, `0.50`. BL-733's defect was displaying
`$71.98` while demanding `71.98` and silently rejecting the correct input, so either echo the string without
the currency symbol or accept both forms. Show the mismatch as text, not colour alone.

**Accessibility, all house rules that have already been broken once each.** `aria-disabled`, never native
`disabled` (BL-556). Never colour alone. The dialog uses the shared `use-dialog-focus-trap.ts` from BL-736.
The confirm control carries an accessible name. A failed write must reach the toast region audibly, which is
what my own `aria-hidden` sweep broke in BL-733. `data-no-swipe` on the dialog container.

Styling: `bg-[var(--bg-card)] border border-[var(--border-color)] rounded-xl`, money in
`font-bold text-accent`, lucide-react icons only, no emojis, no dashes as bullets, mobile first at 375px.

---

## PART 5 — WHAT THE CLIPPER SEES

The clipper sees **his own new rate and nothing else**. No owner rate, no split, no ratio, no platform
economics, per BL-531. The derived owner figure never reaches a clipper-facing response, which is automatic
here because `ownerCpmAtSubmissionDecimal` is already excluded from clipper selects.

On notification, the relevant existing promise is `email.ts:820`, shown to clippers verbatim: *"Existing clips
keep their original rates. Only new submissions earn at the updated rates."* That is a **campaign-edit**
email. Do not reuse it, and do not extend it, because a per-clip override is not a campaign edit and reusing
the copy would make a narrow action look like a platform-wide rate change.

**Recommendation: notify on a raise, do not notify on a decrease.** A raise is good news, specific, and worth
sending: the clip, the new rate, one line, nothing about the owner side. A decrease on a never-earned clip
takes nothing from anyone, and an email announcing it invites a dispute over money that was never accrued.

Whether a decrease should be permitted at all is **the one judgement call I am leaving to the owner**, because
it is a policy question and not a technical one. It is safe: eligibility guarantees nothing has been paid.
It is also in tension with the platform's stated posture that rates only move forward. My recommendation is to
permit it, since refusing it would leave a typo uncorrectable, but to require the same typed confirmation and
send no email.

---

## PART 6 — FAILURE MODES, WORST FIRST

**1. Clipper stamp written, owner stamp not.** The ratio breaks, `decideOwnerGross` returns `ambiguous`, and
the owner silently earns $0.00 on that clip forever. This is the worst outcome because it is invisible.
*Mitigation:* both stamps in ONE `tx.clip.update`, the `cpm-restamp.ts:183-189` pattern. Atomic by
construction, not by discipline.

**2. Applied to a clip that has earned.** BL-742's class: 37 pairs below money already paid, $1,103.41 of
shortfall. *Mitigation:* re-check the eligibility predicate **inside** the transaction under
`SELECT ... FOR UPDATE` (the BL-736 reassign pattern), never only at request time. This is not theoretical:
the tick fires at exactly :00 UTC every hour, so a clip can go from never-earned to earned between the dialog
opening and the confirm landing.

**3. The AgencyEarning delete branch.** `cpm-restamp.ts:222` deletes the row when `ownerAmt` is 0.
*Mitigation:* eligibility already requires no AgencyEarning row, so assert its absence explicitly rather than
leaning on that branch's bare `try/catch`. Never copy the delete into the new path.

**4. Ratio derived from a null or zero owner stamp.** `r` is undefined or 0, the guard goes ambiguous.
*Mitigation:* refuse, with a UI reason. 49 live clips.

**5. The raise trips the campaign budget cap** and auto-pauses the campaign. Correct behaviour, not a defect.
*Mitigation:* disclose remaining budget in the confirmation (PART 4).

**6. A later campaign CPM edit silently erases the override.** This is real and it is the strongest argument
for a schema change. `restampClipsForCampaign` writes both stamps from the campaign pair across the campaign's
clips, and would overwrite a per-clip override with no trace. *Mitigation:* add one additive nullable column,
`cpmOverriddenAt TIMESTAMP(3)`, and skip those clips in the bulk restamp. The column exists to **protect** the
rate, not to read it; resolution still goes through the stamps.

**7. Rollback.** The audit row records `prev` with both stamps, exactly as `cpm-restamp.ts:167-173` already
does. Reversal is writing `prev` back through the same function, and it is valid **only while the clip is
still never-earned**. Once it earns, the override is permanent by the same rule that made it safe to apply.

---

## PART 7 — BUILD SPEC

**Schema** — one statement, via `run-schema-sql.js`, never `prisma migrate`:
```sql
ALTER TABLE clips ADD COLUMN IF NOT EXISTS "cpmOverriddenAt" TIMESTAMP(3);
```
Nullable, zero backfill. Then `npx prisma generate`.

**New files**
- `src/lib/per-clip-cpm.ts`
  - `decidePerClipCpmPair(args)` — **pure, exported, no DB**, returns a discriminated union
    (`ok` with the pair, or `refused` with a named reason). This is the unit-testable core and the whole of
    PART 1 lives in it.
  - `applyPerClipCpmOverride(db, clipId, newClipperCpm, actorId)` — eligibility re-check under `FOR UPDATE`,
    `decideNeverDecrease` before the transaction, both stamps plus `cpmOverriddenAt` in one update,
    `writeClipEarnings` for the four invariant fields, audit row with `prev`/`next`.
- `src/app/api/admin/clips/[id]/cpm-override/route.ts` — `getSession()` + OWNER-only + `checkBanStatus()`,
  Serializable isolation, input validated (no NaN, no negatives, `>= 0.005`).
- The confirmation dialog component per PART 4.

**Edited**
- The admin clip row, to add the owner-only control.
- `src/lib/cpm-restamp.ts` — **one guard line only**: skip a clip whose `cpmOverriddenAt` is not null.
  This is the single non-money file that must change, and it is Opus tier.

**Untouched, and asserted byte-identical by blob OID**: all 6 money files, including `tracking.ts`, which must
not appear in the diff. `campaign-era.ts` likewise. `cpm.ts` unchanged; the dead override branch stays dead.

**Harness** — table-driven over `decidePerClipCpmPair`: the six PART 1 rows, plus the $0.005 boundary from
both sides, a null owner stamp, a zero owner stamp, a non-dividing ratio, a NaN input, a negative input, and a
guard re-evaluation asserting `|implied - stampedRatio|` is unchanged to 6dp across the scaling.

**SAFETY VERDICT: SAFE TO BUILD** — writing both stamps by ratio-preserving scaling leaves the owner-share
guard's comparison numerically unchanged, and restricting it to the 123 never-earned clips on ACTIVE campaigns
means no clip that has been paid against can be written down, with the single caveat that a clip whose owner
stamp is null or zero has no split to preserve and must be refused rather than repaired.
