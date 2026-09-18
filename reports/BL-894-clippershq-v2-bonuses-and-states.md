# BL-894 — every bonus and every campaign state on a v2 clip, proved, and five writers that would have overpaid

**MODEL SPLIT.** The strongest model did every line of arithmetic, every judgement about whether a
figure is right, both proof harnesses, the fix, the new guard and this report, with no subagent between
it and the source. A cheap model did one read-only inventory. Claims are marked **VERIFIED** where I
re-derived them myself and **READ** where they are a subagent's and I did not.

**A SUBAGENT CLAIM WAS WRONG IN THE DANGEROUS DIRECTION, and reading the source caught it.** It
reported that the post path passes a nulled bonus config to the calculator. Literally true; the
conclusion a reader would draw, that a poster's first write zeroes his bonus, is false. **That call is
at `views: 0`**, which returns all zeros at `marketplace-v2-earnings.ts:184` before any bonus code runs.
A second claim said freeze-undo does not recompute v2 clips. It did, and that is this round's defect.

## PART 0 — where a bonus actually lands (VERIFIED)

**IT MULTIPLIES THAT EARNER'S OWN 45 PERCENT. Never the gross.** `marketplace-v2-earnings.ts:237-238`:

```
const editorBonusAmount = round2(editorBase * (editorBonusPct / 100));
const posterBonusAmount = round2(posterBase * (posterBonusPct / 100));
```

`editorBase` is that earner's own leg from `:228`. **This is what you asked for and it is already true.**

**BONUSES SIT OUTSIDE THE RESIDUAL.** The platform leg is `:233`, `grossR − editorBase − posterBase`,
computed from the BASE legs BEFORE any bonus exists. No bonus is an input to it. So the three legs sum
to the gross **plus** both bonuses: a bonus is extra money the campaign pays, not a re-carving of the
gross. **That is coherent, not broken** — nothing is created and nothing is lost, and I proved it rather
than asserting it.

## PART 1 — every bonus, every earner, every combination (VERIFIED)

| bonus | values | editor may hold | poster may hold | applies to marketplace |
|---|---|---|---|---|
| Level | 0/3/6/10/15/20 at levels 0 to 5 | yes | yes | yes |
| Streak | 1/2/3/5/7/10 at 3/7/14/30/60/90 days | yes | yes | yes |
| PWA install | 2 | yes | yes | yes |
| Manual override | owner set, ceiling 30, short-circuits the other three | yes | yes | yes |
| Referral 5 percent | **NOT a bonus to the earner** | n/a | n/a | it is a separate payment to the INVITER |

All four live on the User table, so **both earners can hold all of them**. No answer here was defaulted
silently: the referral 5 percent is the one that looks like a bonus and is not.

**3,100,136 combinations across 4,586 gross values, zero failures.** Primes as dollars, cents and
thousandths; every half cent to $20; the sub-cent band BL-877 measured; $999,999.99. No combination
creates or loses a cent. **81,120 payout breakdowns** stacking the 9 percent fee, the 4 percent referred
rate, BL-763's express premium on the gross and BL-835's trainer cut: every one recomposes to the leg
exactly and **none goes negative**, because the trainer cut is clamped to the room left after the others.

**BL-876's 9.37 PERCENT IS CONFIRMED FROM THE CODE.** At a 10 percent editor bonus and a 5 percent
poster bonus a $100 gross disburses $106.75 and the platform's $10.00 is 9.37 percent of it.

| editor | poster | disbursed | platform | platform share of what leaves |
|---|---|---|---|---|
| 0% | 0% | $100.00 | $10.00 | **10.00%** |
| 10% | 5% | $106.75 | $10.00 | **9.37%** |
| 25% | 25% | $122.50 | $10.00 | **8.16%** |

## PART 2 — the +25 percent ceiling, reached for the first time (VERIFIED)

**IT CAPS THE PERCENTAGE, PER EARNER, NOT PER CLIP.** `earnings-calc.ts:633` is
`Math.min(level + streak + pwa, 25)` and takes ONE party; a per-clip cap would need a caller that adds
the two, and there is none. **IT IS REACHABLE**: level 5 (20) plus a 90 day streak (10) plus PWA (2) is
32, which clamps to 25. A sandbox person reached it and the row stored 25 against a raw entitlement of
32. **Both earners can hold 25 at once**, so one clip can carry 50 percent of bonus.

**THE CLAMP CANNOT DISTURB THE RESIDUAL**, because it acts on a percentage the residual never reads.
Measured: platform $10.00 at the 25 cap and $10.00 at the 30 manual override ceiling, both equal to the
base residual. The 55 cents in every dollar BL-877 built the aggregate to catch cannot escape this way.

## PART 3 — freezing, and every other campaign state (VERIFIED)

**THERE IS NO FROZEN STATUS.** `CampaignStatus` is ACTIVE, PAUSED, COMPLETED, DRAFT, PAST. **Freezing on
this platform IS pausing.**

**PAUSED, PAST, COMPLETED and ARCHIVED each moved no money at all** on a live v2 clip: applied one at a
time and read back, all three legs unchanged in every one. None of them is an earnings writer. What each
earner sees while frozen is BL-765's wording, that the campaign is finished so the balance will not
grow, and it is true for both of them: **freezing stops the tick adding more, it never claws back**.

**UNFREEZING MOVES ALL THREE LEGS TOGETHER, TO THE CENT.** Proved by writing through
`writeClipEarnings` ALONE, which is the exact call `campaign-freeze-undo.ts:390` makes: the poster went
$450.00 to $900.00 and the editor and platform followed by themselves to $990.00 and $200.00, summing
exactly to the gross plus both bonuses. **`campaign-freeze-undo` has ZERO references to either v2
table** — it is the v2 sync living inside the chokepoint that makes a freeze correct, not anything the
freeze code does.

## The defect: five writers would have paid a v2 poster 100 percent instead of 45

**MEASURED, NOT REASONED ABOUT.** On a 1000 view clip at a $1000 CPM the poster's correct leg is $450.00
and `campaign-freeze-undo`'s own recompute produced **$1000.00**, 2.22 times too much. **It would not
have stopped there**: `marketplace-v2-sync` derives the gross as `posterBase / 0.45`, so it would have
derived **$2222.22 against a true $1000.00** and carried the error into the editor's leg and the
platform's too. All three legs would have moved together to the wrong place and **every reconciliation
would still have balanced, which is why nothing caught it.**

**ONE CAUSE, FIVE TIMES.** Each file excludes the FIRST marketplace with `isMarketplaceClip`, and **a v2
clip carries that flag FALSE ON PURPOSE**, because setting it true would pay it on the 60/30/10 split.
Each guard predates v2 and none was widened:

`campaign-freeze-undo.ts` (the undo you press after a mistaken freeze) · `cpm-restamp.ts` (every
campaign-wide CPM edit) · `admin/fix-earnings` · `admin/force-recalc-earnings` · `clips/[id]/override`
(the manual override).

**THE FIX IS THE ONE EACH FILE ALREADY ARGUED FOR**, applied to the case it did not know about:
`marketplaceV2PostId`, the only identifier of a v2 clip, added to each exclusion. Five files, 71
insertions, 3 deletions, and **no arithmetic touched**. `owner-submit-core.ts` recomputes and writes too
and is deliberately unchanged: it creates a brand new clip, which has no v2 stamp to protect.

## PART 4 — what you net, per $100 of gross on a v2 clip

| case | editor cash | poster cash | platform leg | fees to you | ordinary cut | **you net** | campaign spends |
|---|---|---|---|---|---|---|---|
| no bonuses, standard | $40.95 | $40.95 | $10.00 | $8.10 | $33.33 | **$51.43** | $133.33 |
| typical bonuses (10/5) | $45.04 | $43.00 | $10.00 | $8.71 | $33.33 | **$52.04** | $140.08 |
| maximum bonuses (25/25) | $51.19 | $51.19 | $10.00 | $10.12 | $33.33 | **$53.45** | $155.83 |
| max bonuses, both referred | $54.00 | $54.00 | $10.00 | $4.50 | $33.33 | **$47.83** | $155.83 |
| max bonuses, both express | $48.94 | $48.94 | $10.00 | $14.62 | $33.33 | **$57.95** | $155.83 |
| no bonuses, REPLACES mode | $40.95 | $40.95 | $10.00 | $8.10 | $0.00 | $18.10 | $100.00 |

Every row reconciles to the cent: every party's cash plus every fee plus the platform leg plus the
ordinary cut equals what the campaign spends.

**YOUR WORST CASE IN THE LIVE MODE IS $47.83 per $100 of gross**, both earners capped and both referred,
while the campaign spends $155.83. The REPLACES row is a comparison only: `MARKETPLACE_V2_PLATFORM_CUT_MODE`
is ADDS, so $18.10 is not reachable today. **My own check first reported REPLACES as the worst case and
that would have frightened you with a number that cannot happen; it is corrected.**

## PART 5 and 6 — what was weakened, what was proved

**NOTHING WAS WEAKENED.** BL-627 no-overpayment, BL-696 no-double-pay, the chokepoint sync and the
residual platform leg all hold across the full population: 0 invariant violations across 10,233 clips,
0 negatives anywhere, 0 clips with two editor legs. **Twelve protected money files byte-identical by
blob OID on both refs.**

**MY OWN GUARD FAILED TO FAIL ONCE.** `check:v2-single-share-writers` counted with a bare substring, so
when the demonstration renamed every occurrence to `marketplaceV2PostIdXX` it still saw the old name
inside the new one and passed. Fixed to a word boundary. **That is the same blindness as the defect**:
`isMarketplaceClip` looked like it excluded the marketplace and excluded one of two.

**BL-882'S GUARD CAUGHT MY FIX THE MOMENT IT LANDED, and it was right to.** Its S4 forbids naming
`marketplaceV2PostId` outside an allow-list, absolutely, because a cleverer per-occurrence test was
tried once and demonstrated unfailable. **The five files were added to the list with the reason
recorded rather than the rule softened**, and S4 was then demonstrated still refusing an unlisted file.
**6 of 6 demonstration cases, nothing sampled**, each naming itself, every file restored byte for byte.

**THE L1 BUDGET HARD LOCK FIRED ON MY OWN TEST DATA**, rejecting a write at $1,045,000 against a
$1,000,000 budget. Reported because it happened, and it is the guard working.

**THE SANDBOX: NOTHING IS UNREMOVABLE.** 110 of 110 recorded rows deleted, 0 remain. No real user, clip,
campaign or payout was touched; the payout fingerprint is identical. **Your test campaign
`cmu5yeax20000h4w7yv5n387y` is byte-for-byte as it was**, fingerprinted before and after.

## Is the marketplace money now proven

**The arithmetic is: yes.** Where a bonus lands, the ceiling, the residual, every deduction, every
campaign state and the full sum for one clip with three differently-bonused posters are all proved with
real numbers on real rows, which no round had done because until BL-892 there was no v2 clip to do it on.

**What remains**: no v2 clip has ever been ticked by the live cron, so the tracking tick's v2 fork is
proved by reading and by its own unit path rather than by a production tick. Your walk on the test
campaign will be the first.

**WHAT YOU MUST DECIDE**: your slice of what leaves falls from 10 percent to **8.16 percent** when both
earners cap their bonuses, and under ADDS a $100 gross clip costs a campaign **$155.83** at maximum
bonuses against $133.33 with none. Nothing is wrong with either number. They are the trade, and you
should see them before fifty people arrive rather than after.

**ROLLBACK:** `git revert` the merge commit. No arithmetic changed, so nothing recomputes differently.
