# BL-849 — the marketplace splits get a floor, and the previous round's arithmetic is corrected

**Nothing could not be removed.** 150 sandbox rows plus 27 product-written audit rows and 5 video hashes,
all deleted by primary key, 0 remaining, both real fingerprints byte-identical. Two table counts moved by
one and are attributed rather than excused: a real clipper connected a TikTok account at 08:58:20, and
**zero rows in either table carry the sandbox prefix**. There is no leftover with an id and no SQL for
the owner to run.

Measured 2026-09-07, 08:32 to 09:10 UTC, against production. Worktree `C:/w849`, branch
`checkpoint/BL-849`, from `main` at `eb825971`.

---

## 1. The launch blocker, and the correction that had to come first

BL-847 reported "the 60 and 10 legs have no paid-is-final floor". **That is imprecise, and the precision
changes what had to be built.**

**BL-824's rule is a READ-SIDE rule and it already covered the creator's 60 percent.**
`effectivePaidOut` (`balance.ts:234-258`) folds `input.marketplaceCreatorEarnings` into
`payableByCampaign` at `:240-243` and bounds each campaign at `min(paid, payable)` at `:255-258`. Every
real caller populates that array, including the withdrawal gate at `payouts/route.ts:852`. So a creator
whose recorded 60 percent collapses is **not** clawed back and their balance does **not** go negative.

**That was proven, deliberately, with the new floor switched off:**

```
BL-824 still holds through the break: available is floored at zero, never negative
      available=$0.00 with $60.00 paid and $0.00 recorded
```

**What was missing is the WRITE side.** Nothing stopped the stored row being overwritten to zero after
the creator had been paid for it. That destroys the RECORD rather than the money, and a destroyed record
is not harmless:

- the creator's own earnings page reads **$0.00** on a campaign they were genuinely paid for, which is
  the exact shape BL-716 and BL-827 each produced on the clipper side, costing $60.47 and a manual repair
  the first time;
- the owner's two **lifetime** liability screens deliberately do NOT apply BL-824's bound
  (`balance.ts:197-201` names them and says why), so his books disagree with what he actually paid;
- and if the clip is retired while the row sits at zero, the evidence of what was earned is gone.

### The rule

```
floor   = max(0, paidGross(creator, campaign) - otherPayable)
written = max(proposed, min(current, floor))
```

Both bounds are load-bearing. `max(proposed, …)` means the floor can only ever **prevent a reduction**.
`min(current, …)` means it can never **invent money** by lifting a row to a floor it never met — without
that, a floor becomes a way to create earnings out of a payout. `paidGross` uses `clipperLiability`
(`balance.ts:126`), which is `actualPaidAmount ?? amount` and is deliberately the GROSS, because the
withdrawal fee comes out of the same gross the clipper consumed (BL-140).

### Why a chokepoint and not a check

**BL-716 and BL-827 each breached the clipper's floor at a DIFFERENT site.** There are **ten** sites in
`src/` that write these two columns. So the fix is one door:
`src/lib/marketplace-earnings-writer.ts` now owns the NaN guard, the
`streakBonusPercentAtApproval` preservation rule and the floor, and `tracking.ts`'s two raw upserts call
it.

**The three-way budget cap needed no separate fix, and that is the argument for the shape.** Its reduced
figures pass through the same writer further down the same transaction, so the vector BL-718 floored at
its two non-marketplace siblings (`tracking.ts:2586`, `:2644`) and missed at the marketplace one is
closed by construction. A floor bolted on at that line would have been the fourth site-specific patch of
one rule, which is precisely how BL-716 escaped into BL-827.

### The 30 percent poster leg needed it too, which BL-847 said it did not

BL-847 called it covered because it goes through `writeClipEarnings`. It does. But **every gate inside
that writer is conditioned on an increase**: the L1 block is `if (delta > 0)`
(`clip-earnings-writer.ts:197-198`) and its own header says *"Decreases always pass"*; BL-167's clamp and
BL-718's `capButNeverBelowStored` both sit inside it; the Y1/Y2 caps are `if (grossDelta > 0)`. A
decrease falls straight through to the update.

The floor is applied at the marketplace **call sites** rather than inside the writer, for two reasons:
it keeps `clip-earnings-writer.ts` byte-identical, and a write-time floor on every clip on the platform
is a far larger change than this round was asked to make. Scoped this way it can only touch rows that do
not yet exist.

### The 10 percent owner leg gets a door, not a floor

The owner's 10 percent is **never withdrawn**. There is no payout row, no transfer and no ledger entry
for it anywhere in `src/`; the model has no user, no status and no `paidAt`. So "paid is final" is
meaningless for that leg and inventing a floor would be inventing a protection against nothing. What it
gets is what is real: one door, a logged and audited decrease, and a loud call when a write would zero
the platform leg while the creator leg still carries money.

### Proven by breaking it

A guard nobody has watched fail proves nothing — BL-824, BL-782 and BL-835's own guard demo all
established that, and BL-835's demo caught a guard that *could not fail*. So each case ran three times.

```
1. WITH the floor       proposed $0.00, written $60.00, floor $60.00, paid $60.00      HELD
   and the hold is on the record rather than silent                                    1 audit row
2. FLOOR SWITCHED OFF   written $0.00 while $60.00 has been paid                       THE DEFECT
3. RESTORED             written $60.00                                                 HELD AGAIN
4. budget scale-down    proposed $12.00, written $60.00                                HELD
5. no-invent bound      row was $5.00, proposed $1.00, written $5.00 (floor $60.00)     NOT LIFTED
6. poster's 30 percent  proposed $0.00, written $30.00, paid $30.00                     HELD
7. an UNPAID creator    written $0.00 with $0.00 paid                                   still falls
```

**10 checks, 0 failures.** Case 7 matters as much as case 1: the floor did not freeze the platform.

---

## 2. BL-847's homework, checked

The owner asked whether the previous round verified each item or fixed some and inferred the rest. **His
suspicion was correct.**

**"Eleven Instagram loss points, now fixed" is three changed edits, seven routed around, and one still
present.** Not one of the seven lines moved. Routing around a dead Apify tier is legitimate and the new
branch is well built, but it is **one re-route, not seven repairs**. Item 9 was item 8 counted twice: one
line change reported as two loss points. **Item 11, YouTube, was fixed by BL-845 and not by BL-847 at
all** — its own section 12 said so while its section 1 table did not.

| verdict | count |
|---|---|
| CHANGED | 3 |
| ROUTED AROUND by one new branch | 7 |
| STILL PRESENT | 1 (YouTube, a config fix) |

**"Six strike entrances" is five.** DESTROY is not an entrance: the campaign delete cascades the listing
and the submission away before any sweep can see them. And four of the remaining five are **one gate**.
Both stamps were verified firing before their returns, so that half of the claim holds.

### BL-847 opened a new entrance of its own

Its **daily settle gate** refuses the POSTER because the LISTING is full, while the 48 hour drift it
corrects is created by a CREATOR submitting across days. Twenty four hours later the sweep struck the
poster for a deadline that very line stopped them meeting. **That is the exact harm BL-847's own section
3 was written to remove, reintroduced by its section 2.**

**Four more unstamped entrances were found beside it**, and one twin:

| entrance | why it struck |
|---|---|
| owner-issued manual ban | the sweep's `activeBan` reads only strike rows; the route's check reads all three sources |
| platform-wide ban | the sweep never reads `User.isBanned` at all |
| visibility flag / role change | refuses silently between approval and deadline |
| the 30-per-hour rate limit | a poster can spend it retrying a three-platform submission near their deadline |
| the in-transaction account twin | BL-847 stamped the pre-transaction site and missed the race window |

All are stamped now through **one helper**, and **the helper checks ownership** — without that it would
be a primitive for writing `verifyFailedAt` onto somebody else's submission and suppressing THEIR strike.

### And the post route has never read the listing's own status, in any round

Every round gated on the CAMPAIGN. So a listing the budget sweep paused, or that the three-strike ban
flipped to BANNED, **still accepted posts and still spent the campaign's money**. The pause and the ban
were decorative on the one route where they cost something. Now refused, and stamped, because a listing
pausing under a live deadline is the same shape as a campaign ending under one.

---

## 3. A live money defect: a banned person is paid in full

`payouts/[id]/review/route.ts` has **zero** reads of the payee's standing across 1,232 lines — no
`User.status`, neither marketplace ban scalar, no `isUserMarketplaceBanned`. The only ban check on the
file gates the OWNER doing the reviewing.

The irony is on the same file: it **does** check standing, on the **TRAINER**, who forfeits their 10
percent if they are banned. The payee was never given the same look.

**Measured on the live database while writing this: one real user holds a REQUESTED payout of $27.35
while carrying an ACTIVE strike whose ban had not expired.** `isUserMarketplaceBanned` returns true for
them and nothing on that path reads it.

It **refuses with a named 409 rather than blocking outright**, in BL-827's shape: a ban is a marketplace
sanction, not a confiscation, and the owner may have every reason to settle a balance anyway.
`acknowledgeBannedPayee` is a way through that has to be typed.

---

## 4. Four more, each of which costs a real person something

**A creator was banned for rejections they did not cause, and the product told them so in writing.** The
cascades stamp `status: "REJECTED"` when something happens to somebody **else** — a destination account
suspended, or the POSTER's privileges revoked — and write a reason that literally reads *"Not counted
toward strikes"*, which the creator reads on their own submission row. The counter had no reason filter,
so all of them counted, and ten inside five days is a 48 hour ban of **every** marketplace action. Only a
human judgement about the clip itself counts now.

**The dispute resolver promised a ban would lift and it did not.** The confirm dialog says *"the ban will
lift immediately if no other active strikes remain"*. The route wrote `strike.bannedUntil = null` and
stopped, while `isUserMarketplaceBanned` OR-merges **three** sources by MAX and the deadline cron writes
`clipperMarketplaceBannedUntil` at the same moment it writes the strike. BL-841 recorded that scalar as
having **no reversal path in the product at all**. It is cleared now, only when no other active strike
remains, and the owner's own manual ban is deliberately left alone: removing a strike is not a statement
about a sanction he applied by hand.

**A permanent ban printed as temporary.** The sentinel is the year 9999, so the submissions route
computed and printed **"Ban lifts in 69,800,000 hours"**, and `BanCountdown` returned the bare word
"Permanent" under eight callers that all prefix it with "Ban lifts in " — so every one read **"Ban lifts
in Permanent."**

**The poster's own deadline reminder opened the creator's page.** The 12h, 6h and 1h notifications go to
the **poster** and pointed at `/marketplace/my-submissions`, which lists only rows where the viewer is
the **creator** and has the mark-as-posted button deliberately removed. The email for the same event has
always pointed at `/marketplace/incoming`.

---

## 5. The arithmetic, across 1,004,029 amounts

**The base split is exact.** `creator + poster + platform === round2(gross)` in **1,004,029 cases with 0
failures** — every cent from $0.01 to $20.00, the awkward primes, $999,999.99, 500,000 view-times-cpm
combinations, and a 200,000-case sweep of the only band where the clamp could analytically fire.

**The platform absorbs every remainder, always.** Creator and poster are each independently half-up
rounded against their own exact share and were **never** adjusted in 502,029 cases. The platform leg is
the residual and takes the whole remainder, swinging **−1.25c to +1.25c** per clip.

| gross | exact 60/30/10 | paid | platform delta |
|---|---|---|---|
| 0.55 | 0.3300 / 0.1650 / 0.0550 | 0.33 / 0.17 / **0.05** | −0.50c |
| 0.57 | 0.3420 / 0.1710 / 0.0570 | 0.34 / 0.17 / **0.06** | +0.30c |
| 4.57 | 2.7420 / 1.3710 / 0.4570 | 2.74 / 1.37 / **0.46** | +0.30c |

**The bias is not systematic; it is cpm-dependent.** On irregular cpms it is symmetric noise (±0.0004c
per clip). On round cpms the platform is systematically favoured — about **+$0.82 per 100,000 clips** at
cpm 2.50 — because float resolves exact half-cent ties on the poster leg **down** rather than half-up
(14,792 up against 5,208 down across 20,000 ties). The `Math.max(0, …)` clamp **never fired once** and is
provably unreachable above a gross of $0.15.

### Three things do not sum, and they are named rather than smoothed

**Bonuses.** Each party's level and streak bonus is added ON TOP of their share and the platform gets
none. A $100 clip at +10 creator and +5 poster disburses **$107.50**, and the platform's slice of what
actually leaves is **9.30 percent**, not 10. At the manual-override ceiling it is **7.87 percent on an
outflow of $127.00**. The campaign budget pays the difference. Range measured across 81 combinations:
platform share of outflow **7.87 to 10.00 percent**.

**The `Math.floor` budget scale-down** in the review route floors all three legs independently with no
residual leg, leaving up to **$0.03 allocated to nobody**. Confirmed at exactly $0.03 over 5,000 cases;
the platform is short most often, and the correction branch only ever reduces the platform further.

**`payoutReductionRatio`** re-rounds each leg independently and nothing re-derives the residual, so the
reduced total **over-allocates by up to $0.02**.

All three are **recorded, not fixed**: each is a change to the shape of the split itself and belongs to a
round that can decide the policy rather than patch the rounding under it.

---

## 6. The suite, re-run

**290 checks, 0 failures.**

| suite | checks |
|---|---|
| the floor, with the break and the restore | 10 |
| BL-847's own prove suite | 23 |
| slots, races and quota | 16 |
| **the money, all five fee combinations** | **39** |
| obligation, penalty, ban | 12 |
| every role, every surface, by request | 40 |
| render at 320 / 375 / 414 / 1280 / 1440 | 150 |

**The money is unchanged to the cent.** plain $91.00, referred $96.00, trainer $81.90 on a $91.00 base,
express $87.00, all three at once $82.90, and `final + fee + express + trainerCut = 100.00` exactly every
time. Referrer held harmless at $4.80 and $4.60. The 60/30/10 residual sums exactly at $100.00, $0.55 and
$4.57.

**The 10 percent still REPLACES the owner's normal cut rather than adding to it, and nothing in this
round changed that.** Verified across all nine sites in `src/` that could create an `AgencyEarning` row,
each closed to a marketplace clip by one of two mechanisms, plus a tenth that states the rule outright.
Measured live: `agency_earnings` joined to marketplace clips on `clipId` is **0 rows**.

**Every invariant survives, proven:** BL-824 paid-is-final (measured holding *through* the deliberate
break), BL-627 no-overpayment and BL-538 never-decrease (earnings invariant 0 violations both sides),
BL-696 no-double-pay (0 double-open payouts, payout fingerprint identical, 221 rows before and after),
the unique index BL-845 created, and the rule that a third party's cut is a stamped deduction on the
payout row rather than a change to `Clip.earnings` (all 39 money checks green).

---

## 7. Accessibility: three criticals on money controls, all confined, all fixed

**Press-and-hold committed the withdrawal on the DOWN event.** Holding past 600ms fired a real,
non-cancellable payout while the finger was still down, and there is no clipper-side cancel anywhere in
the product. A tremor, a resting finger or a stuck stylus paid the money out. It **arms** on the timer
and **commits on release** now — WCAG 2.5.2 — while keeping the non-drag path that people who cannot drag
depend on (2.5.7).

**A mistyped budget cap silently deleted the cap.** Typing `1,000` or a dollar sign into a `type="number"`
field makes the browser's own sanitiser hand back an empty string; the diff reads that as "cleared", sets
the column to null, enables Save, and one press removes the spend limit with no warning. A mouse wheel
over the focused field rewrote it just as quietly. Both cap fields are `text` with `inputMode="decimal"`
now, so a wrong character looks wrong instead of silently becoming nothing.

Everything else the review found reaches `modal.tsx`, `button.tsx`, `input.tsx` or `toast.ts` and would
touch the whole app. Left for a round that can render the whole app, as in the two previous rounds.

---

## 8. Nothing real moved

150 rows created, every id recorded in a ledger outside the repo at the moment of creation, deleted by
primary key and never by pattern: **148 deleted, 2 taken first by cascade, 0 of 150 remain.** Then
everything the **product** wrote in response, as BL-845 and BL-847 both had to: **27 audit rows and 5
`MarketplaceVideoHash` rows**, swept in two passes — list, print every id with its reason, write the ids
to a file, delete only what is in that file.

**48 of 50 verification checks passed, and the two that did not are attributed to the row rather than
excused.** `clip_accounts` 1481→1482 and `campaign_accounts` 782→783 are a **real clipper connecting a
TikTok account at 08:58:20**, and **0 rows in either table carry the sandbox prefix**. Both real
fingerprints byte-identical (`42ab3988…`, `14832ebc…`). Every marketplace table back to zero.
`payout_requests` 221 before and after. Earnings invariant **0 violations** both sides.

**Invisibility was proven by ABSENCE this round rather than by an HTTP probe, and that is stated
plainly:** the sandbox was destroyed before the check, so there was no server left to ask. What is proven
is that zero rows carrying the prefix, the marker or the sandbox username survive in any table.

**No vendor money was spent.** Every key unset on the sandbox server, no Apify actor, the 11 BL-678
guards untouched.

---

## 9. Recorded and not fixed

- **The bonus overflow, the `Math.floor` scale-down and the `payoutReductionRatio` re-round** (section 5).
- **A rejection after payment `deleteMany`s both marketplace rows with no `savedAmount`**, so unlike the
  `videoUnavailable` freeze there is no record of what was destroyed. BL-823's shape in a marketplace
  jacket.
- **A settle-gate race**: the post-time count runs outside the transaction and is separated from the
  insert by a live external fetch, so two tabs can both pass it. The sequential burst is closed; the race
  is not.
- **`marketplace-payout-shape.ts:125-127`** still uses naive independent rounding and its three legs fail
  to sum in **27 percent** of rates. Owner-facing display only, no money moves.
- **`counter-recompute` must still not be enabled.**
- **Campaign DESTROY still hard-deletes marketplace money rows** with no balance check and no
  notification.
- **The Instagram fix fails open when `HIKERAPI_KEY` is unset**, admitting a clip into an environment
  that can never track it.
- Roughly **thirty more user-facing strings** that state something the code does not do, tabled by the
  copy audit. The eight that cost a person money or a strike are fixed above; the rest are listed with
  file:line in this round's working notes.

---

## 10. Build honesty

**Two production builds, exit codes echoed by hand and never piped through `tail`: 0 and 0.** A clean
`tsc` baseline was taken **on the untouched worktree before any edit**: exit 0, `grep -c "error TS"` = 0.
Six further typechecks during the round, the last at exit 0 with 0 errors. Hooks gate **0 errors, 10
warnings** against a ceiling of 11. `eslint v9.39.4` confirmed present.

**ONE MONEY FILE CHANGED AND IT IS DECLARED LOUDLY: `src/lib/tracking.ts`, +94/−28**, entirely inside the
`isMarketplaceClip` branch — two raw upserts replaced by the chokepoint, plus the poster floor and its
decomposition. The non-marketplace path is untouched. **The other five money files plus `campaign-era.ts`
are byte-identical by blob OID on both refs.**

No schema change, no index, no migration, no `prisma migrate`. BACKLOG 179 → 180, counted with `grep -c`
and never piped to `head`. `checkpoint/BL-723` confirmed not an ancestor. Worktree `C:/w849` removed and
**verified gone by listing the path**, not assumed, because BL-847 left one held by a stray handle.

---

## 11. Is the marketplace safe to launch?

**Closer than it was, and the remaining list is shorter than last round's — but not yet.**

**What this round closed:** the recorded 60 and 30 can no longer fall below money already paid, and the
guard was watched failing and then holding; the three-way budget cap is covered by the same door; a
banned person is no longer paid in full without the owner saying so deliberately; a creator can no longer
be banned for rejections somebody else caused; a dispute that says a ban will lift now lifts it; the
strike trap's five real entrances are joined by five more that were open, including one the previous
round created; and the post route finally reads the listing it is posting to.

**What must happen before real money flows:**

1. **Redeploy Railway.** None of this is live until then.
2. **Decide the bonus question.** The parts do not sum to the gross once any bonus exists, and the
   platform's slice of actual outflow falls to as low as 7.87 percent. That is a policy decision about
   what 60/30/10 means, not a bug to patch.
3. **Give a rejection-after-payment the same `savedAmount` treatment the `videoUnavailable` freeze
   already has**, so the record survives.
4. **Do not enable `counter-recompute`.**
5. **Set `YOUTUBE_API_KEY`**, or accept that YouTube posting is dead.

**What remains unproven, stated plainly.** Nothing in the marketplace has ever executed in production: 0
submissions, 0 posts, 0 creator or platform earning rows, 0 marketplace clips, $0.00 ever moved. Every
proof here is a sandbox proof against production **code**, not an observation of production
**behaviour**. Three specific gaps: **the volume races were designed and predicted but not run** — a
twenty-way contention test, the settle-gate race between two tabs, and the cross-listing false
serialization on an empty table are all specified in this round's notes and none was executed; **the
Instagram happy path still has no real, freshly posted reel behind it**, only a fail-open accept and a
synthetic media object; and **invisibility was proven by absence rather than by request** this round.
The single test I would run first after the redeploy is still the same one: a real Instagram reel,
freshly posted, read by HikerAPI and accepted on its real `taken_at`.
