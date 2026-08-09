# BL-756 — per-clip CPM override, with both BL-754 gaps closed as part of the build

**VERDICT IN ONE LINE: the owner can set a custom clipper rate on one clip and his own side moves with it,
because BOTH stamps are scaled by the same ratio. All 6 money files plus `tracking.ts`, `campaign-era.ts` and
`apify.ts` are byte-identical by blob OID, because no rate column was added: the two frozen stamps already ARE
the per-clip rate at all eleven money call sites.**

**2026-08-09 · Base:** `main @ 605af18c` · **Branch:** `checkpoint/BL-756` `fca0f636`
**Tags:** `pre-BL-756` = `605af18c`, `post-BL-756` = `fca0f636`

**One real clip was touched and fully reversed** (named in PART 5). No clip's earnings, status or payout
changed. No Apify actor run. No `prisma migrate`. Handles redacted; every timestamp cast `::text` against DB
`now()`. `C:/b575` was not touched: it is stale at `91b84410` and dirty at 77 paths, so the work ran in a
separate clean worktree at a short path with `node_modules` installed, never junctioned.

---

## GATES, STATED HONESTLY

| gate | result |
|---|---|
| `npx tsc --noEmit` **baseline, before any change** | **exit 0, 0 errors** |
| `npx tsc --noEmit` after | **exit 0, 0 errors** |
| `npm run build` | **`BUILD_EXIT=0`**, "Compiled successfully in 17.5s", read from the log |
| BL-348 hooks gate | **0 errors, 11 warnings** against `--max-warnings 11` |
| eslint present | **v9.39.4**, so the gate did not silently no-op |
| Pure harness | **33 passed, 0 failed** |
| Live demo on real data | **17 passed, 0 failed**, fully reversed |
| a11y review | run **before** the markup was written; findings applied, not noted |

BL-753 wrongly reported 2 pre-existing tsc errors that were caused by stray files in its own worktree, so this
round took a clean baseline **first**: it was 0, and it is still 0.

---

# THE DESIGN DECISION THAT KEEPS THE MONEY FILES UNTOUCHED

`cpmAtSubmissionDecimal` + `ownerCpmAtSubmissionDecimal` already are the per-clip rate. BL-754 verified one by
one that **eleven** money call sites resolve through them, and that every one passes a hand-built three-key
object literal, which is why `cpm.ts:170-171`'s `clipperCpmOverride` branch is unreachable at all eleven.

Writing the stamps therefore needs **no call-site change**. Adding the override columns the resolver appears to
want would have meant editing `tracking.ts`, a money file, in the hot earnings path, to reach behaviour the
stamps already deliver. That is the whole reason the diff below contains no money file.

**A new file rather than reusing `cpm-restamp.ts`.** `restampSingleClip` has the right shape but cannot be
called: its signature takes CAMPAIGN field bundles and derives the pair at `:114-118` from
`getCampaignCpmForPlatform`, so there is no way to hand it a per-clip pair. Widening it would put the bulk
campaign-edit path, which runs across every clip on a campaign, at risk for a single-clip feature.
`cpm-restamp.ts` gets one declarative line instead.

---

# GAP 1 — REASSIGNMENT CAN NO LONGER ERASE AN OVERRIDE

BL-736's `reassign-campaign/route.ts` overwrites **both stamps** from the destination in the same update that
moves the clip. Its in-transaction re-check asserts only `status = PENDING`, `campaignId` unchanged and
`earnings = 0`, and **setting a custom rate changes none of those**, so the move would have proceeded and
erased the rate silently, passing every one of its own assertions.

## The choice, made on the merits

**REFUSE**, not rescale, not clear.

* **Rescale to the destination's locked share** either keeps the pair, which then fails
  `owner-share-guard.ts:72` against a **different `s`** and silently pays the owner $0.00, or re-derives
  against the new `s`, which silently changes the rate the owner deliberately chose. Both replace his decision
  with an inference.
* **Clear-and-tell** discards the decision on his behalf, mid-flow.
* **Refuse** loses nothing and is reversible in three explicit steps: remove the custom rate, move the clip,
  set it again on the destination. The owner stays the one deciding the economics.

## Closed in two places, because one is not enough

1. **`campaign-reassign.ts`** — a new `CLIP_HAS_CPM_OVERRIDE` clip-side block in the **shared** rule set, so
   the picker and the server cannot drift. `reassign-campaign-dialog.tsx:248-254` already renders clip-side
   blocks in a prominent panel and **hides the destination picker entirely** when one fires, so the owner reads
   the reason **before he confirms** and there is nothing left to confirm.
2. **`reassign-campaign/route.ts`** — `cpmOverriddenAt` added to the `FOR UPDATE` re-check and refused inside
   the lock. Needed independently, because the owner can set the rate in another tab after the dialog opened.

The reason string he sees:

> This clip has a custom rate you set by hand. Moving it would replace that rate with the destination
> campaign's rate. Remove the custom rate first, then move it.

**12 currently eligible clips are PENDING and therefore in both populations**, which is why this had to be
closed in the same round rather than after.

---

# GAP 2 — THE FIGURE AND THE RATE NOW COME FROM ONE SOURCE

`admin/clips/page.tsx` computed the owner figure from `clip.campaign.ownerCpm`, the **campaign's live rate**,
while BL-744's rate line printed `fmtRate(stampOwner)`, the **clip's stamp**. On an overridden clip those
differ by 2.5x on BL-743's live pair, which is precisely the confusion BL-744 was built to eliminate.

The two stamp constants were declared 40 lines **below** the computation. They are hoisted above it and the
clip stamp now wins, with the campaign rate kept as the fallback for a clip that has no owner stamp, which is
the pre-existing behaviour for every clip that was never overridden.

**Exposure before the fix was genuinely ZERO and this report says so rather than overstating the find**: the
eager branch requires `status = APPROVED` **and** `views >= minViews`, and every eligible clip is below its
campaign minimum, which is *why* it has no earnings. It would have fired the moment one crossed `minViews`
after an override and before the next tick wrote its agency row.

Measured in the live demo at 5,000 views: **campaign-rate figure $0.64 against stamp-rate figure $1.60, 2.5x.**

---

# PART 1 — THE ARITHMETIC

```
r        = origOwnerCpm / origClipperCpm     (from the ORIGINAL pair)
newOwner = round4(newClipper * r)            (ROUND_HALF_UP)
```

Every step runs in `Prisma.Decimal`, never IEEE floating point. **Rounding rule: four decimal places,
ROUND_HALF_UP**, because both stamps are `Decimal(10,4)` and the project's own precision policy uses 4dp for
CPM rates. **The OWNER side absorbs the fractional cent**, named and deliberate: the clipper's rate is exactly
the number the owner typed, to the digit, and the owner carries the remainder, at most $0.00005 per 1,000
views. The clipper is the party being promised a number; the owner is the party deciding.

`s` is a campaign field and this never touches it, and scaling both sides leaves `stampedRatio` equal to `r` up
to rounding, so **`owner-share-guard.ts:72` returns the identical verdict before and after** — the same
comparison on the same two numbers, which is why BL-742 measured this shape at 702 of 702 against clipper-only
at 648 of 648 ambiguous.

## Measured, from the harness

| case | old pair | typed | derived owner | guard gap |
|---|---|---|---|---|
| **BL-743 live non-round** | $0.2000 / $0.1279 | $0.50 | **$0.3198** | 0.0001000 |
| non-dividing | $0.2000 / $0.1279 | $0.33 | $0.2110 | 0.0001060 |
| floor | $0.2000 / $0.1279 | $0.005 | $0.0032 | 0.0005000 |
| large | $0.2000 / $0.1279 | $12.50 | $7.9938 | 0.0000040 |
| **the owner's own 50/50** | $0.3000 / $0.3000 | **$0.50** | **$0.5000** | **0.0000000** |

The 50/50 row is his stated rule satisfied exactly: he sets the clipper to $0.50 and his own side becomes
$0.50, with zero drift.

## Drift, against BL-754's measured budget

BL-754 corrected BL-752's "100x" claim: the margin that matters is the **ratio budget**, and the worst eligible
clip already consumes **0.004000 of the 0.01 tolerance**. Re-measured today, independently: **0.004000**, with
**0 eligible clips already ambiguous**. The harness starts from that offset:

```
gap before is the measured 0.004                     -> 0.004000
gap after never exceeds before + one perturbation    -> worst after 0.004500 vs 0.004000 + 0.0005
and stays inside the guard tolerance                 -> 0.004500 < 0.01
```

**The true worst-case margin is about 2.2x, and the code says so in a comment rather than implying comfort it
does not have.**

## BL-754 gap 7: compounding is impossible by construction

The ratio is derived from `cpmOverrideOrigClipper` / `cpmOverrideOrigOwner`, the pair as it was **before the
first override**, never from already-scaled stamps. Twelve successive overrides therefore carry **one**
perturbation:

```
after 12 overrides the gap is still one perturbation -> 0.0000556
(counter-example, deriving from current stamps:         0.0005000 — WORSE, which is why origin is used)
```

## The 27 refused clips

A clip with a clipper stamp but a null or zero **owner** stamp has **no split to preserve**. It is already
ambiguous under today's guard and the owner already earns $0.00 on it. Scaling would preserve that, not repair
it. Refused by name, with the reason on screen:

> This clip has no owner rate recorded, so there is no split to keep. Set the owner rate on the campaign first,
> or leave this clip as it is.

**BL-754's gap 3 is also closed**: rule 5's OR clause is **dropped**. Both stamps must be present and above
zero, so a clip that was following the live campaign is never silently converted into a frozen one.

## Counts, corrected to measured (`db_now = 2026-08-09 21:37:55.272547+00`)

| | BL-752 | BL-754 | **measured here** |
|---|---|---|---|
| never earned on ACTIVE | 123 | 130 | **126** |
| **eligible** | 123 | 103 | **99** |
| **refused, no split** | 49 | 27 | **27** |
| PENDING, so also reassignable | — | 22 | **12** |
| already ambiguous | — | 0 | **0** |
| worst existing gap | — | 0.004000 | **0.004000** |

---

# PART 2 — FORWARD ONLY, ENFORCED SERVER-SIDE

Refused on any clip that has earned. BL-742 measured that a retroactive change would put **37 clipper-campaign
pairs below money already paid, $1,103.41 of shortfall, worst single case $195.21**, and `email.ts:820` has
already told clippers, in words they have received, that existing clips keep their original rates.

**Isolation level: `Serializable`**, with `SELECT ... FOR UPDATE` on the clip row inside the transaction.

**The race BL-754 raised is closed by the lock, and for the right reason.** The tick fires at exactly `:00
UTC`, so a clip can go from never-earned to earned between the dialog opening and the request landing. The
tick's own `writeClipEarnings` updates the same row, so `FOR UPDATE` serialises them and the re-read sees the
tick's committed result rather than the stale value the dialog was built from. The UI check is a courtesy; the
server one is the gate.

## Where the guards sit, and where one deliberately does not

**This module writes RATES, never money.** `earnings`, `baseEarnings` and `bonusAmount` are untouched; the next
tick recomputes them through `writeClipEarnings`, the existing L1 budget hard-lock. **No new earnings write
path exists**, which is why BL-627's no-overpayment and no-over-budget properties hold by construction rather
than by argument.

* **`decideNeverDecrease` is wired**, in `assertForwardOnly`, as a gate on projected earnings before any write.
  **Stated plainly: on this population it cannot fire**, because eligibility requires `earnings = 0`, so
  `stored = 0` and every projection is INCREASE or UNCHANGED. It is defence in depth against a future
  loosening; the eligibility predicate under the lock is the mechanism.
* **BL-718's paid floor is deliberately NOT wired.** `capButNeverBelowStored(cap, stored)` returns `max` and
  belongs where a budget or pool **ceiling** could write a clip down. This path has no cap site because it
  writes no money at all. BL-742 observed the floor never fires on a decrease because it sits inside
  `if (delta > 0)` — true, and it is exactly why the floor is the wrong instrument here. **What protects money
  already paid is the refusal.** Inventing a site for the floor would be cargo cult.

**Removal is forward-only for the same reason.** If a clip earned under the override, restoring the lower
original pair would write it down on the next tick, which is the $1,103.41 shape again.

## BL-754 gap 4, proven rather than asserted

BL-754 could not determine whether approval re-stamps. **It does not.** `review/route.ts` reads
`cpmAtSubmissionDecimal` / `ownerCpmAtSubmissionDecimal` at `:476`, `:477` and `:526` and performs **zero**
writes to those fields (`grep -c` for a stamp write in a `clip.update` in that file returns **0**). An override
therefore survives reject then re-approval.

---

# PART 3 — THE OWNER UI

The control sits on the clip row's rates line, owner-only and CPM_SPLIT-only, which is exactly the right
gating. A clip carrying an override shows a **Custom rate** badge in words, not colour, and the trigger reads
"Set a custom rate" or "Change".

The confirmation shows **five values, every one labelled**, in a definition list:

```
Clipper rate now      $0.20
Clipper rate after    $0.50
Your rate now         $0.1279
Your rate after       $0.3198
Split                 39% you, 61% clipper, unchanged
```

plus the sentence *"You set the clipper rate. Your rate is worked out for you so the split stays exactly the
same."* BL-744 fixed this class of confusion and BL-743 lost a whole round to a misread; showing only the new
clipper rate would leave the owner to infer his own side, which is the inference that cost the round.

Note on scope: the brief lists five values and this delivers those five. BL-752 had also proposed a "campaign
budget left" row; the GET returns no budget and fetching it separately risks disagreeing with the campaign
page, so it was **dropped rather than half-built**.

**Removal and change are both implemented.** `DELETE` restores the original pair verbatim from the Orig
columns, which is lossless rather than a re-derivation. A change re-derives from the original pair, so it never
compounds.

**Bounds**: $0.005 to $100.00 per 1,000 views. The lower bound is not arbitrary: below it the 4dp rounding
perturbation of the ratio starts to eat the guard budget. The upper bound is a fat-finger guard. Absurd values,
garbage, negatives, non-numerics and no-ops are each refused with their own message.

## Accessibility — reviewed BEFORE the markup was written

The a11y lead returned four blockers and several defects. Each was applied:

* **The typed gate is the CLIP ID, not the rate.** Retyping a rate you just authored cannot catch the error the
  gate exists for: fat-finger `35.0` for `3.50` and the dialog prints "type 35.0", he types it, it ships. The
  id also has no decimal-format trap.
* **One shared 4dp formatter and parser** (`src/lib/rate-format.ts`) replace three that disagreed:
  `formatCurrency` is 2dp and would print a derived $0.1279 as **$0.13** while $0.1279 is written, which is
  BL-733 by construction; `fmtRate` was trapped inside a render IIFE; `fmtCpm` formats the same quantity
  differently. **The parser refuses `0,50` as ambiguous rather than reading it as fifty**, which matters
  because the existing normaliser strips commas and the owner is Serbian.
* **Comparison is numeric at 4dp, never by string**, so `0.5` is not rejected against a demanded `0.50`.
* **The announcement is debounced 500ms and flushed on blur.** Un-debounced, typing `1.05` enqueues four whole
  sentences whose intermediate values are order-of-magnitude wrong; a blind owner hearing a 10x wrong rate
  spoken confidently in a money dialog is a correctness hazard.
* **A definition list with self-describing labels**, not a table: two values have no "after" partner,
  `display:flex` strips implicit table roles, three currency columns do not fit the measured 240px content box
  at 320px, and `overflow-x: hidden` would clip the overflow unreachably.
* **The unit rides on the value and only on the four rates.** Appending "per 1,000 views" to the split would
  announce a factually wrong unit to screen reader users only.
* **`aria-disabled` on hand-written buttons**, never the `Button` component, whose
  `disabled={disabled || loading}` would, while busy, empty the focus trap's stop list **and** swallow Escape:
  a 2.1.2 keyboard trap for the whole flight of a request.
* **Dark ink on the accent fill.** White on `#2596be` is **3.40:1 and fails 1.4.3**; `#09090b` on accent is
  5.86:1.
* **`forced-colors` outlines**, because `ring-*` compiles to `box-shadow`, which forced-colors discards.
* **The error region is persistently mounted and keyed on an attempt counter**, so a repeated identical refusal
  is still announced instead of reconciling to the same node silently. The message says the action **failed**,
  then the reason, then what to do.
* **The best typo detector there is**: when the clip has views, the dialog states what the change would
  actually pay. A 10x slip renders as a number the owner recognises instantly.
* 2.5.8 targets at 44px, `90dvh` for the soft keyboard, `data-no-swipe`, no emojis, no dashes as bullets.

**One conflict is recorded and deliberately NOT resolved here.** `Button` hard-wires
`disabled={disabled || loading}`, which conflicts with BL-556's `aria-disabled` rule and gates every inert
style on the `disabled:` variant. This dialog sidesteps it entirely with hand-written buttons. Fixing the
shared component touches shipped call sites and deserves its own round; it is in the BACKLOG.

---

# PART 4 — WHAT THE CLIPPER SEES

**The clipper sees only his own rate**, wherever his rate is already shown. No owner rate, no split, no ratio,
no platform economics.

**Proven by grep**, per BL-531:

```
src/app/api/clips/mine/route.ts   -> ownerCpm / agencyFee / ownerCpmAtSubmissionDecimal / clientName / aiKnowledge: 0
src/app/api/earnings/route.ts     -> 0
src/app/api/payouts/route.ts      -> 0
```

The new `cpmOverriddenAt` marker was added **inside** the existing `canSeeMoney` gate in `clips/route.ts`, so
it inherits that gate's redaction rather than being widened to a reviewer.

**Notification is NOT implemented, and this is stated rather than implied.** BL-752 concluded: notify on a
raise, do not notify on a decrease, and deliberately do **not** reuse `email.ts:820`, which is a campaign-edit
promise and would make a narrow per-clip action look like a platform-wide rate change. **Nothing was built.**
It is recorded in the BACKLOG as deferred, so nobody reads this round as having handled it. A clipper whose
rate is raised will see the higher rate on his next view of the clip; a decrease, which the eligibility rules
make possible only on a clip that has never earned, would be discovered silently. **That is a real gap and it
is named rather than papered over.**

---

# PART 5 — EVIDENCE

## The pure harness: 33 passed, 0 failed

Covers the five scaling cases above, the 50/50 rule, the drift bound from the measured 0.004 offset, the
12-application compounding test with its counter-example, and every refusal: no owner stamp, zero owner stamp,
no clipper stamp, below floor, absurd, `NaN`, `Infinity`, `-Infinity`, `"abc"`, `null`, `undefined`, `{}`,
negative, no-op. Plus `assertForwardOnly` against earned, base-only, bonus-only, an agency row, a clean clip
and non-finite stored earnings.

## The live demonstration: 17 passed, 0 failed, fully reversed

**Clip touched: `a704c992`** (redacted ref; id `cmsma2vb...`), PENDING on "Zhus Meme (0.20 CPM)", chosen because
it carries **BL-743's exact non-round pair**: clipper $0.2000, owner $0.1279, `s = 0.39005794`. Its earnings,
baseEarnings and bonusAmount were all 0 with no AgencyEarning row, so nothing on this path could touch money.

```
AFTER THE OVERRIDE
  clipper stamp $0.5   owner stamp $0.3198   guard gap 0.0001000 of 0.01
  PASS  clipper stamp is exactly what was typed
  PASS  owner stamp is the DERIVED value on a non-round ratio -> $0.3198
  PASS  the SPLIT is preserved -> ratio 0.639600 vs 0.639500
  PASS  no drift beyond BL-754's measured budget
  PASS  EARNINGS UNCHANGED -> earnings 0, base 0, bonus 0

GAP 1
  PASS  reassignment now REFUSES the overridden clip -> 1 block(s)
  PASS  and the owner is told WHY, before confirming

GAP 2 (at 5,000 views)
  PASS  pre-fix the figure and the rate disagreed -> $0.64 vs $1.60 (2.5x)
  PASS  post-fix the row computes from the stamp it displays

AFTER REMOVAL
  PASS  clipper stamp restored EXACTLY -> $0.2 (was $0.2)
  PASS  owner stamp restored EXACTLY -> $0.1279 (was $0.1279)
  PASS  marker cleared
  PASS  earnings still untouched end to end
  PASS  reassignment is allowed again -> 0 blocks
```

**How to reverse it: nothing to reverse.** The script restored the clip in the same run and the DB confirms it
independently at `2026-08-09 22:14:59.013499+00`: stamps `0.2000 / 0.1279`, marker null, earnings 0, PENDING.
Had it been left in place, the reversal is `DELETE /api/admin/clips/<id>/cpm-override`, or directly:
`UPDATE clips SET "cpmAtSubmissionDecimal" = "cpmOverrideOrigClipper", "ownerCpmAtSubmissionDecimal" =
"cpmOverrideOrigOwner", "cpmOverriddenAt" = NULL, "cpmOverrideOrigClipper" = NULL, "cpmOverrideOrigOwner" =
NULL WHERE id = '<id>';`

**Honest scope note:** the demo replicates the route's transaction using the same library primitives and the
same `Serializable` + `FOR UPDATE` shape. It does not invoke the HTTP handler, which needs an owner session.
The handler's logic is the same code and is type-checked, and that is said plainly rather than dressed up as an
end-to-end HTTP test.

## Platform state, after everything (`db_now = 2026-08-09 22:14:59.013499+00`)

| metric | value |
|---|---|
| earnings invariant violations | **0** |
| campaigns over budget | **0** |
| clips carrying an override | **0** |
| Orig columns populated | **0** |
| payout rows | **164**, unchanged |
| total clip earnings | $12,180.47, **risen** on ordinary cron accrual, not fallen |

## Protected files, blob OID on both refs

```
IDENTICAL  ac5be7deb061  src/lib/clip-earnings-writer.ts
IDENTICAL  797e20985ad5  src/lib/earnings-calc.ts
IDENTICAL  e887f80acfc7  src/lib/balance.ts
IDENTICAL  83ce4babfd39  src/lib/tracking.ts
IDENTICAL  61cef3939536  src/lib/clip-earnings-invariant-middleware.ts
IDENTICAL  ef5cdae757b9  src/lib/money-decimal.ts
IDENTICAL  106e16ad7512  src/lib/campaign-era.ts
IDENTICAL  656bf4c0c408  src/lib/apify.ts
```

**8 of 8 identical. `tracking.ts` does not appear in the diff.** `apify.ts` identical means its 8 BL-678 guard
comments are intact by construction; no Apify actor was run.

## Schema

Three **additive, nullable** columns via `ALTER TABLE ADD COLUMN IF NOT EXISTS`, applied with
`run-schema-sql.js`, **never `prisma migrate`**. Verified in `information_schema`: `is_nullable = YES` on all
three, `Decimal(10,4)` on both rate columns. **Zero rows backfilled.**

---

# WHAT IS NOT DONE, NAMED

* **Clipper notification.** Not built. See PART 4.
* **The `Button` / `aria-disabled` conflict.** Sidestepped here, not fixed. Its own round.
* **Concurrency proven by reasoning plus the lock, not by an executed concurrent test.** BL-754 raised this and
  I did not close it: proving it needs a harness running the tick and the override against one clip
  simultaneously. The `FOR UPDATE` argument is sound and the isolation level is stated, but it is analysis.
* **An end-to-end HTTP test through the route with a real owner session.** See the scope note in PART 5.

---

# ROLLBACK

`git revert -m 1 <merge>`, or `git reset --hard pre-BL-756`. The three columns are additive and nullable and
can be left in place. **No data rollback is needed: no override survives this round.**
