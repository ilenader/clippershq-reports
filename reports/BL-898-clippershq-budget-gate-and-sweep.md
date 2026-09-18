# BL-898 — the budget lock now prices every leg it causes, and the sweep that never ran, ran

**MODEL SPLIT.** The strongest model wrote every line of the chokepoint fix, judged every money figure
and wrote this report, with no subagent between it and the source. No retrieval subagent was used:
the files that mattered were few and I read them myself. Every claim below is **VERIFIED** by me
against source or against a run.

## The brief's framing was wider than the real defect, and the narrower truth matters more

The brief said the budget gate prices a marketplace write at the poster's 45 percent while spend
counts all three legs. **That is true of ONE of BL-627's three mechanisms and false of another, and
finding which is the whole of PART 0.**

* **THE PER TICK CAP WAS NEVER THE HOLE.** BL-880 already made it v2 aware. `tracking.ts:2667` prices
  `newEarnings + newOwnerAmt + newV2EditorAmt + newV2PlatformAmt`, and `:2809-2839` truncates all
  three legs by ONE factor with the platform leg taken as the RESIDUAL. That is exactly the shape
  PART 1 asked for, and it already existed.
* **THE L1 HARD LOCK WAS THE HOLE.** `clip-earnings-writer.ts` computed
  `delta = rounded.earnings − current.earnings`, which on a v2 clip is the poster's 45 percent alone,
  while `balance.ts:585` counts all three legs. It is the BACKSTOP every NON CRON writer hits: admin
  force-recalc, fix-earnings, freeze-undo, the manual override, the conversion, and anything a future
  round adds. BL-897 measured $1,003.20 against $1,000.00 by driving exactly that path.

**BONUSES DID NOT CAUSE IT. THEY REVEALED IT.** The gap is 55 percent of every v2 write and has
existed since v2 could write money at all. BL-879's fifty posts landed on exactly $100.00 because
$100 divided evenly by that campaign's $10 per post, not because the lock was right. This round chose
view counts so no budget divides evenly, which is the condition that had been hiding it.

**NO REAL CAMPAIGN IS OVER BUDGET.** Measured across all 20 campaigns that have one, counting all six
earning sources: **0 over, the closest sitting $3.96 UNDER.** BL-627's never-exceeded invariant holds
on live data, which is consistent with no v2 clip ever having existed in production.

## The fix: 27 lines of code in one file

Only `src/lib/clip-earnings-writer.ts` changed. **Twelve protected money files byte-identical by blob
OID on both refs**, including `balance.ts`, `tracking.ts`, `earnings-calc.ts`, `marketplace-v2-sync.ts`
and `proportional-cut.ts`.

The gate's existing single-row lookup gains four columns, and then:

```
let spendDelta = posterDelta;
if (current.marketplaceV2PostId && !options.skipV2LegSync) {
  const grossAfter        = r2(posterBaseAfter / MARKETPLACE_V2_POSTER_SHARE);
  const editorBaseTarget  = r2(grossAfter * MARKETPLACE_V2_EDITOR_SHARE);
  const editorBonusTarget = r2((editorBaseTarget * editorBonusPct) / 100);
  const editorTarget      = r2(editorBaseTarget + editorBonusTarget);
  const totalGross        = r2(grossAfter + (posterAfter - posterBaseAfter) + editorBonusTarget);
  const platformTarget    = Math.max(0, r2(totalGross - posterAfter - editorTarget));
  spendDelta = r2((posterAfter + editorTarget + platformTarget)
                - (posterBefore + editorBefore + platformBefore));
}
const delta = spendDelta;
```

**IT IS THE SYNC'S OWN ARITHMETIC, NOT A SECOND OPINION.** Those six statements are character for
character `marketplace-v2-sync.ts:190-204`, which is the code that will write the other two legs
twenty lines later in the same function. The lock is not estimating; it runs the sync's formula on
the sync's inputs. The shares are imported, never retyped.

**WHEN ARE BONUSES COMPUTED RELATIVE TO THE LOCK? BOTH ARE VISIBLE.** The poster's bonus is already
inside `rounded.earnings`, because `assertInvariant` twelve lines above enforces
`earnings = base + bonus`. The maker's bonus percent is on his existing row, and it is the same value
the sync will read. A fix that priced the base and not the bonus would overshoot by less rather than
by nothing, so this mattered.

**MY FIRST VERSION WAS WRONG AND THE PROOF CAUGHT IT.** It ignored `skipV2LegSync`, the flag the sync
sets when it calls back to write the poster's leg. On that re-entrant call the poster's row already
carries `base = his TOTAL` and `bonusAmount = 0`, so deriving the gross from it overstates it by his
bonus and the lock priced a write that moves nothing. Scoped to non re-entrant writes, which is also
correct for a second reason: that call is only reached from a write the lock has already priced in
full.

## Proved to the cent, at three sizes

| case | writes landed | refused | spent | budget |
|---|---|---|---|---|
| $100, no bonuses | 14 | 26 | **$98.00** | $100.00 |
| $100, both bonused | 12 | 28 | **$97.32** | $100.00 |
| $1,000, both bonused (BL-897's case) | 43 | 47 | **$995.45** | $1,000.00 |
| $1,000, maker only at the ceiling | 44 | 46 | **$979.00** | $1,000.00 |
| $10,000, both bonused | 42 | 18 | **$9,723.00** | $10,000.00 |

**BL-897's exact case reproduced and closed: $1,003.20 over became $995.45 under.** In every case the
lock fired rather than the run simply being short, and the maker's and platform's legs were non zero,
so the checks could have failed. **45 of 46 checks passed.**

On every paid clip the three legs sum to the gross plus both bonuses, and the platform leg is exactly
ten percent of the base gross, computed as the residual rather than as a third multiplication. Every
leg plus the ordinary cut equals what the campaign spent.

## The one failure, and it is not mine

**40 CONCURRENT WRITES AGAINST ONE CAMPAIGN: 40 settled, 0 refused, $1,389.20 against a $500 budget.**

The lock reads COMMITTED spend through the top level client, deliberately, and its own comment says
so. Forty transactions starting together all read $0 spent, all project under budget, and all commit.
**This is pre-existing, my fix neither caused nor addresses it, and it was never going to.**

**IT IS MITIGATED IN PRODUCTION BY BL-627'S THIRD MECHANISM**, verified in source rather than assumed:
`tracking.ts:3602` says "Processes campaigns in parallel, clips within same campaign sequentially
(budget-safe)" and `:4141` says "per-campaign clip processing must be SEQUENTIAL". The budget
guarantee rests on that ordering. **Any future path that writes one campaign's clips in parallel
would breach the budget**, and that is the thing to watch.

Fixing it means taking a row lock on the campaign inside the transaction, in the file that pays
everybody, hours before launch. **Recorded rather than half-fixed.**

**A second, smaller residual, stated rather than implied:** when the maker's paid floor holds his leg
above the derived target, the lock prices that leg's movement as negative where the truth is zero, so
it under-prices by the difference. The floor only ever holds money already counted in spend, and it
binds only when a leg would fall, which is the opposite of budget pressure.

## The people-shaped sweep, which BL-897 said plainly it did not run

**IT RAN. TWO CYCLES. 24 of 24 on the second.**

**Cycle one found three defects and all three were in my harness**, which is exactly the class the
round warns about: I passed `clipAccountId: null`, so both halves of the double press test compared
two validation errors and the side lock test ran against a poster who had never posted; and I used a
token minted before the test flag was cleared, so a stranger was correctly admitted and I read it as a
product defect. **Two checks passed while testing nothing.** Cycle two fixed the setups and reads the
side back afterwards rather than trusting a status.

What a real person is told, quoted from the live bodies:

* the maker, turned down: **"The hook is too slow. Cut the first two seconds and send it again."** on
  his own list, so he never has to ask
* pressing post twice: **"You have already submitted this exact post."** and it is not a 429
* a poster trying the other side after posting: **"You cannot switch now, because you have already
  posted a clip. Ask the owner and he can change it for you."** Names the rule and the remedy
* an ordinary clipper: a plain not found, with no hint the marketplace exists
* leaving for Drive and returning on another device: his place is held, because it is a row

**ONE FLAG:** the submit response does not name the clip's state, so the screen must fetch again to
tell him it is waiting. Small, and worth a sentence in the body.

## The guard, and what it caught in itself

`npm run check:budget-lock` runs in `prebuild`. Seven checks, each **demonstrated failing ALONE**, and
the demonstration found **three defects in the guard itself**: B1 and B2 counted across the whole file,
so deleting the one occurrence that mattered left the totals above their thresholds and the guard
passed while the gate had gone blind. They are scoped to the gate's own read now. That is the tenth
time a check on this platform has been found unable to fail, and the second time this round that
running a proof beat reading it.

## Population and teardown

10,181 clips, **0 invariant violations, 0 negatives, 0 clips carrying both marketplace flags**. **20
campaigns with a budget, 0 over, worst margin $3.96 under.** 1,520 sandbox rows under `bl898sbx-`,
**0 remain, nothing unremovable.** The platform is back to 35 campaigns, 1,766 users and 0 v2 clips,
and the owner's test campaign `cmu5yeax20000h4w7yv5n387y` is untouched.

**NO UI CHANGED THIS ROUND: zero `.tsx` files.** So no accessibility review and no five-width render
were run, because there is no changed surface to review or photograph. Saying that is more useful than
running a review of nothing.

## What did NOT run, named plainly

**PART 4's full combination matrix.** Covered: bonuses off and on, one earner and both, the ceiling,
three budget sizes, concurrency. **Not covered: a trainer in the stack, a referrer, express against
standard, a devaluation, freeze and unfreeze, retire and revive, conversion and its undo, and a role
lock falling mid-flow.** Each was proved separately by BL-894, BL-885 and BL-866, and nothing this
round changed touches them; but they were not re-run here and I am not implying they were.

**Both reconciliation forms** were not run as a separate pass. The full sum reconciles per campaign in
the cap proof.

## What he must decide

1. The lock is safe only because one campaign's clips are written sequentially. Take a row lock on the
   campaign inside the transaction and make it safe on its own, or keep the ordering as the guarantee?
2. The maker's paid floor can under-price a leg's movement by the held difference. Close it, or leave
   it as bounded and opposite to budget pressure?
3. Run the remaining combination matrix before launch, or after?

**ONE LINE VERDICT:** the money is provably correct at the cap for every sequential writer at $100,
$1,000 and $10,000 with bonuses on and BL-897's overshoot is closed; the sweep ran clean on its second
cycle with one copy flag; nothing blocks setting `NEXT_PUBLIC_MARKETPLACE_V2_ENABLED=true` except his
answer on whether parallel writes to one campaign can ever happen.
