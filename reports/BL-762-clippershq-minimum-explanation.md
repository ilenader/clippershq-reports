# BL-762 — telling a clipper why he cannot withdraw, where he already is

**2026-08-10 · DB now() = `2026-08-10 17:17:18.363473+00` · BUILD. Display and messaging only.**
Base `origin/main` @ `018c22ca`. Branch `checkpoint/BL-762` @ `e35a58e0`, **verified pushed** (`origin/checkpoint/BL-762 == local HEAD`). Tags `pre-BL-762` (`018c22ca`) and `post-BL-762` (`e35a58e0`) both on origin. Isolated worktree `C:/b762`, short path, no junctioned `node_modules`, removed at the end of the round. `DATABASE_URL` from `.env.local`; every read through `scripts/run-select.js`; every timestamp cast `::text` against DB `now()`.

**No eligibility rule, minimum, balance, earning, clip status or payout changed.** `src/app/api/payouts/route.ts` is not in the diff. The clipper who prompted this round still cannot withdraw, which is correct. He can now see why.

The clipper is referred to throughout as **Clipper A** (user id prefix `cmpfozzs`, `md5` short id `540fef`). His handle is redacted and no wallet address was selected or printed.

---

## PART 0 — THE DIAGNOSIS, CONFIRMED ON LIVE DATA

### His position

| campaign | status | clips | earned (payable) | paid | **available** | **its minimum** | verdict |
|---|---|---|---|---|---|---|---|
| **Zhus Edit (0.50 CPM)** | ACTIVE | 9 | $12.18 | $0.00 | **$12.18** | **$20.00** | **BLOCKED** |
| **Zhus Meme (0.20 CPM)** | ACTIVE | 1 | $0.42 | $0.00 | **$0.42** | **$20.00** | **BLOCKED** |
| bees.n.honey | PAST | 58 | $21.18 | $33.44 | $0.00 | $10.00 | nothing to take |
| GainzAlgo (REPOST) | PAST | 46 | $0.00 | $26.54 | $0.00 | $10.00 | nothing to take |
| STRAENGE | PAST | 10 | $0.00 | $0.00 | $0.00 | $10.00 | nothing to take |
| Panic Baby | PAUSED | 6 | $0.00 | $0.00 | $0.00 | $10.00 | nothing to take |

**Two corrections to the brief, both in the clipper's favour and both worth the owner knowing.**

**It is $12.18, not $10.95.** His Zhus Edit clips are still earning on an ACTIVE campaign; the figure moved from $12.13 to $12.18 during this round alone. **And it is two campaigns, not one:** he also holds $0.42 on Zhus Meme, under the same $20.00 minimum. Across both he is holding **$12.60** he cannot reach, and he needs **$7.82** more on Zhus Edit to unlock the larger one.

The $20.00 figures are real and stored: `Campaign.minPayoutAmountDecimal = 20.0000` on both, the owner's own raises, verified as `numeric(18,4)` in BL-734. Every other campaign stores NULL and resolves to the $10 platform default through `resolveMinPayout` (`payout-minimum.ts:113`).

### Exactly which check blocks him

The server gate at **`src/app/api/payouts/route.ts:346`**: `if (toCents(roundedAmount) < toCents(campaignMinUsd))`. His maximum possible request on Zhus Edit is $12.18, the campaign's minimum is $20.00, `1218 < 2000`, refused with a typed `PayoutRefusal("AMOUNT_BELOW_CAMPAIGN_MINIMUM", 400, …)`. **The block is correct and this round does not touch it.**

### Why no explanation reaches him, which is the actual defect

`/api/earnings` returns, for him, exactly this:

| field | value |
|---|---|
| `available` | **$0.00** |
| `totalEarned` | $33.78 |
| `paidOut` | $59.98 |
| `campaignBalances` | Zhus Edit $12.18 (`minPayout` 20), Zhus Meme $0.42 (`minPayout` 20) |

His global `available` is $0.00 for a reason that has nothing to do with the minimum: BL-698 removed his retired-clip earnings from the **display** while every payment he has received stays counted, so `max(33.78 − 59.98, 0)` floors at zero. His per-campaign balance was positive the whole time.

That $0.00 is what breaks the explanation, and it does so in three compounding steps:

**1. The button was natively disabled.** `PayoutsRedesign.tsx:212` read `disabled={available <= 0}` against the **global** figure. Every sentence BL-728 wrote about per-campaign minimums, and every one of the seven copies BL-734 reconciled, lives **inside** the payout flow. That flow opens from this button. **The explanation existed on a path he could not trigger.**

This is not a new discovery, and that is the uncomfortable part. BL-689 wrote it down at the time: the clipper "will see it only if they reach the flow by another route". It was recorded as a known consequence and never closed.

**2. The one sentence he did get sent him to the owner.** With `totalEarned > 0`, the empty state rendered BL-689's copy verbatim: *"No balance available to withdraw right now. If that looks wrong, open a support ticket in our Discord and the team will check it."* He opened a support ticket. **The screen instructed him to do the thing the owner is now treating as a bug report.** That sentence is right for a clipper whose balance is genuinely unexplainable from the client; it is wrong for one whose balance is fully explained by a number the client was already holding.

**3. Directly beneath it, the page contradicted itself.** The "Available by campaign" strip renders every row with `available > 0` and labels it **"Available"**. So his screen read **"$0.00"** in the hero and **"Zhus Edit (0.50 CPM) · Available · $12.18"** two inches below, with nothing reconciling them.

BL-689's accessibility review raised precisely this contradiction as a must-fix ("a screen-reader user would hear $0.00 … $52.86") and concluded it could not occur. **It occurs. Clipper A is the case that proves it**, and a screen reader read him "$0.00", then "Available $12.18", then "open a support ticket".

**So the cause is what the brief suspected, plus two more.** The explanation is behind a disabled button, the fallback copy actively misdirects, and the strip beside it asserts the opposite. Fixing only the button would have left two of the three.

---

## PART 1 — THE REASON, SHOWN WHERE HE ALREADY IS

He now has to click nothing. The exact copy shipped:

### On the payouts screen, in the hero, under the balance

**One blocked campaign** uses `belowMinimumMessage` from `payout-minimum-shared.ts`, which is **the same function the server gate calls when it refuses**:

> "Zhus Edit (0.50 CPM) has a $20.00 minimum withdrawal and you have $12.18 available on it. You need $7.82 more on this campaign before you can withdraw from it."

**More than one**, which is Clipper A's case today:

> "You have $12.60 across 2 campaigns, and each one is under its own minimum withdrawal. What each campaign still needs is listed below."

### In the campaign strip, now split

Heading: **"Your balance by campaign"**, then two groups.

> **Ready to withdraw** — cards unchanged.
>
> **Not at the minimum yet**
> Zhus Edit (0.50 CPM) · Below minimum · **$12.18 of $20.00 minimum** · **$7.82 to go**
> Zhus Meme (0.20 CPM) · Below minimum · **$0.42 of $20.00 minimum** · **$19.58 to go**

Each blocked card also carries one `sr-only` sentence, again `belowMinimumMessage`, so a screen reader hears a claim rather than three disconnected numbers. Ready cards gained the same treatment: *"$73.23 available. This clears its $10.00 minimum, so you can request a payout on it."*

### On the earnings screen, inside the hero, under the figure

> "$12.60 of this is on 2 campaigns that have not reached the minimum withdrawal yet. Each campaign sets its own."
> *See what each campaign still needs* → `/payouts`

### Why this copy

It states a threshold and never a judgement, per BL-518 and BL-521. Nothing implies he did anything wrong, because he did not: he posted clips, they were approved, they earned. The shortfall is measured **against his balance, never against a typed amount**, which is BL-728's rule; a clipper with $12.18 needs $7.82, and printing anything else sends him to earn a number that would not actually unlock it. There is no "contact support", because support is not the answer and the old sentence proved what happens when it is offered as one.

### It cannot contradict the gate, by construction

New module **`src/lib/below-minimum-campaigns.ts`** owns the predicate. It imports **`toCents`** from `payout-minimum-shared.ts` and compares `toCents(available) >= toCents(minPayout)` — **the identical integer-cent comparison, from the identical module, that the gate performs**. A campaign this file calls blocked is exactly a campaign the gate would refuse.

**No literal minimum was introduced anywhere.** Every value is the campaign's own `minPayout`, resolved server-side by `resolveMinPayout` in `/api/earnings` and already present on the payload since BL-728. The two screens share one predicate and one sentence, so BL-734's failure mode (a value copied into seven places, stale in two) is not reopened: this round adds a copy of neither.

---

## PART 2 — THE DISABLED BUTTON

**Decision: keep it unpressable, but change how. `aria-disabled="true"` replaces the native `disabled` attribute, the button stays focusable, and the click handler returns early.**

```
aria-disabled={!canRequest}
aria-describedby={!canRequest ? "payout-cta-reason" : undefined}
onClick={() => { if (!canRequest) return; onRequestPayout(); }}
```

**Why not simply attach a reason to the disabled button.** `aria-describedby` is announced on a **focus** event. A natively disabled button is removed from the tab order, so NVDA in focus mode, JAWS and VoiceOver all skip it and the description is never spoken. **A reason attached to a `disabled` button is a reason nobody hears** — the same defect class this round exists to close, one attribute deeper. The accessibility review was explicit that "keep `disabled`, add `describedby`" must be rejected as a fake fix.

**Why not let it open and return BL-689's typed refusal.** Three clicks to learn a fact the client already holds, and `PayoutRefusalCode` has no below-minimum member — the sentence comes from the flow's own client-side validation, not from a typed server refusal, so "let him hit the API" would not even produce it until he had picked a campaign and typed an amount. BL-698 set the better precedent: explain at first paint, next to the number being explained.

**This is the house pattern, not a novelty.** `listing-detail-client.tsx:355-363` and `login/page.tsx:346-348` already use `aria-disabled` over native `disabled`; BL-556 established it in the payout flow itself; the BACKLOG already carries a deferred item about the shared `Button` component hard-wiring `disabled`. **This hero was the outlier.**

**Eligibility is byte-identical.** `canRequest` is the same `available > 0` expression the native attribute used, the handler refuses on exactly that condition, and the server gate is untouched. One consequence had to be handled: `disabled:cursor-not-allowed disabled:opacity-40` stop matching once the attribute is gone, so the dimming moved into the conditional class. `pointer-events-none` is deliberately not used, because it would kill focus and hover on the one control a keyboard user now needs to land on.

### A clipper holding several campaigns

The split answers this directly, and a single global figure never could. Clipper `cmq7qh6p` holds five campaigns and now sees:

> **Ready to withdraw** — WinGram **$73.23**, Panic Baby **$46.51**
> **Not at the minimum yet** — somesome $3.73 of $10.00 (**$6.27 to go**), bees.n.honey $3.25 of $10.00 (**$6.75 to go**), Zhus Meme (0.20 CPM) $1.59 of $20.00 (**$18.41 to go**)

His button is enabled and no reason line renders, because he can withdraw. Blocked campaigns sort **closest to unlocking first**, so the number he can act on reads first.

---

## PART 3 — WHO ELSE IS IN THIS POSITION

Measured at `2026-08-10 17:17:06+00`, reproducing the gate's own arithmetic in SQL:

| | pairs | clippers | dollars |
|---|---|---|---|
| **Below their campaign's minimum** | **139** | **112** | **$432.18** |
| Total still needed to unlock all of it | | | $1,187.82 |
| Of that, on the two $20.00 campaigns | **23** | **18** | **$98.71** |
| Ready to withdraw right now | 26 | 23 | $2,021.74 |

**112 clippers can currently see money they cannot withdraw and, until this round, were told nothing about why.** Against BL-758's measurement four days ago (139 pairs, $426.41) the population is flat in count and up $5.77 in value, which is ordinary accrual.

### Could anyone withdraw before the raise and not now? Yes: three clippers, $44.68

BL-731 verified **0 verdicts flipped** at merge time, and that remains true. But the owner raised the two minimums to $20.00 **afterwards**, and that raise did flip three:

| id8 | md6 | campaign | available | minimum | needs |
|---|---|---|---|---|---|
| `cmqb6eia` | `9f5e0f` | Zhus Edit (0.50 CPM) | **$19.42** | $20.00 | **$0.58** |
| `cmsiyrnw` | `a02849` | Zhus Edit (0.50 CPM) | $13.08 | $20.00 | $6.92 |
| **`cmpfozzs`** | **`540fef`** | Zhus Edit (0.50 CPM) | $12.18 | $20.00 | $7.82 |

All three cleared the old $10.00 floor. **Clipper A is one of them**, which is the whole story: he could have withdrawn, the rule changed, and nothing told him. `cmqb6eia` is 58 cents short and is the single most likely next support message. **Every one of these three will now read the exact shortfall on their own screen**, which is the outcome this round was for. Whether to lower the minimums or pay them by hand remains the owner's call; this round changes no rule and pays nobody.

---

## PART 4 — THE EVIDENCE

**Clipper A's screen now states all four facts.** From live data at `2026-08-10 17:17:18+00`, with `available = $0.00` so `canRequest` is false and the reason renders:

> Hero: "You have **$12.60** across **2 campaigns**, and each one is under its own minimum withdrawal. What each campaign still needs is listed below."
> **Not at the minimum yet** → **Zhus Edit (0.50 CPM)** · $12.18 of **$20.00** minimum · **$7.82 to go** · and Zhus Meme (0.20 CPM) · $0.42 of $20.00 minimum · $19.58 to go
> Earnings hero: "**$12.60** of this is on 2 campaigns that have not reached the minimum withdrawal yet."

Campaign, balance, minimum, shortfall. All four, without a click.

**A clipper above the minimum sees no change and can still withdraw.** `cmr0gixm` holds $545.37 on Panic Baby against a $10.00 minimum: `canRequest` is true, so the button renders with its original shadow, hover and active styling, no reason paragraph renders at all, and his card sits under "Ready to withdraw" with **byte-identical markup to before** (`{c.name}` / "Available" / `formatCurrency(c.available)` in `text-accent`). The only difference is invisible: the two numeric fragments are now `aria-hidden` behind one spoken sentence.

**A mixed clipper sees which is which.** `cmq7qh6p`, two ready ($119.74) and three blocked ($8.57), rendered in PART 2.

**The message uses the same per-campaign value the gate enforces.** `splitCampaignsByMinimum` calls `toCents` imported from `payout-minimum-shared.ts`, the module the gate imports at `payouts/route.ts:25`. The single-campaign sentence and every blocked card's spoken sentence are `belowMinimumMessage`, the gate's own string. `grep -c` for a hardcoded minimum in either touched component returns **0**, before and after.

**Nobody newly can or cannot withdraw.** `src/app/api/payouts/route.ts` is not in the diff; the whole change is three files. `canRequest` is the same `available > 0` expression the removed `disabled` attribute evaluated.

**No clip's earnings or status changed and no payout was touched.** This round wrote nothing to the database. Every DB access went through `scripts/run-select.js`, which refuses any write keyword before connecting.

### The money files

Blob OIDs compared with `git rev-parse` on **both** refs, `origin/main` and `checkpoint/BL-762`:

| file | blob OID | |
|---|---|---|
| `clip-earnings-writer.ts` | `ac5be7deb061` | **IDENTICAL** |
| `earnings-calc.ts` | `797e20985ad5` | **IDENTICAL** |
| `balance.ts` | `e887f80acfc7` | **IDENTICAL** |
| `tracking.ts` | `83ce4babfd39` | **IDENTICAL** |
| `clip-earnings-invariant-middleware.ts` | `61cef3939536` | **IDENTICAL** |
| `money-decimal.ts` | `ef5cdae757b9` | **IDENTICAL** |
| `campaign-era.ts` | `106e16ad7512` | **IDENTICAL** |

### The gates, stated honestly

**`eslint` is present** in the worktree's `node_modules/.bin`, so the BL-348 hooks gate is a real check and not a silent no-op. `npx prisma generate` was run after `npm ci` (which wipes the generated client) and before any typecheck.

| gate | baseline, before any edit | after |
|---|---|---|
| `npx tsc --noEmit` | | **exit 0**, 0 lines of output |
| `npm run build` (includes `prebuild`) | **exit 0** | **exit 0** |
| `lint:hooks` | **0 errors, 11 warnings** | **0 errors, 11 warnings** |
| `Compiled successfully` | yes | yes, 15.9s |

Exit codes were captured with `echo "BUILD_EXIT=$?"` immediately after the command, never read through a pipe. The baseline was measured on this same worktree **before** the first edit, which is why "unchanged" is a measurement and not an assumption. The gate permits `--max-warnings 11` and sits at exactly 11, so this change had to add **zero** warnings; that is why the two new computations run during render instead of inside a `useMemo` whose dependency array would be a new liability for no gain.

The diff is real and non-empty: 3 files, +345 / −24.

### Accessibility

The accessibility lead reviewed the plan **before** any UI was written and its findings shaped the implementation rather than being checked against it afterwards. All four blocking items are satisfied: `aria-disabled` over native `disabled` (A, F3); the hero's third reason branch, without which the split would have reproduced the contradiction one line higher (F2); no progress bar, because no neutral track satisfies both theme boundaries (F1); and the `(app)` layout confirmed to render no competing `h1`, so `h1 → h2 → h3` is valid (F4).

Also applied: explicit `role="list"` on the grid `ul`, because WebKit strips list semantics from a `display: grid` list and "list, 2 items" is the entire payoff; lists named by `aria-labelledby` on the heading rather than wrapped in `<section>`, which would mint landmarks inside `main`; numeric fragments `aria-hidden` with one `sr-only` sentence, with the campaign **name left visible to AT** so it is announced once and not duplicated; and BL-698's no-live-region posture kept, since this content is present at first paint and a region on mount is either never announced or interrupts the user's own read.

On colour, the review corrected an assumption worth recording: **the light theme is live**, exposed by the navbar toggle and restored from `localStorage` on every route. `text-accent` (`#2596be`) is 5.42:1 on the card in dark but **3.40:1 in light**, clearing AA only as large text (24px, or 18.66px bold). So the blocked cards' figures use `--text-secondary` and `--text-primary`, never accent at small size, and hierarchy in dark comes from size and weight. The new earnings note uses `bg-[var(--bg-input)]` and `--text-secondary` rather than copying BL-698's hardcoded `bg-white/[0.04]` and `text-white/80`, which composite acceptably in dark by accident and are **white on white in light**. The only accent is a `Target` icon marking the blocked heading, `aria-hidden`, introducing no new hue into a palette already fully allocated in this file; the group split is carried by the visible headings, the "to go" wording and a distinct kicker, never by colour alone.

**Two items deferred, disclosed rather than quietly skipped.** The review's WCAG 4.1.3 recommendation, an `sr-only role="status"` announcing the moment a campaign **crosses** its minimum during an in-place SSE refresh, needs debounced state and an id-set comparison; with the hooks gate at exactly 11 of 11 it belongs in its own round, and the review did not list it as blocking. Separately, BL-698's existing note at `EarningsPremium.tsx:119-128` is white-on-white in the light theme and its link is 3.40:1; pre-existing, outside this round's scope, reported not edited. Both are in the BACKLOG.

---

## WHAT THIS ROUND DID NOT DO

• **It did not lower a minimum or pay anybody.** 112 clippers still hold $432.18 they cannot reach, and the three clippers who could withdraw before the raise still cannot. Those are the owner's decisions and this round deliberately leaves them open, now with the numbers to make them.
• **It did not touch the $0.00 global balance itself.** Clipper A's hero still reads $0.00, which is BL-698's display rule netting his payments against his payable earnings, and is a separate question from the minimum. What changed is that the screen no longer leaves it unexplained or contradicted.
• **It did not add a below-minimum code to `PayoutRefusalCode`.** The block is stated before the request, so no new server refusal was needed, and inventing one would have implied a server path that does not exist.
• **It ran no browser and captured no screenshot.** The rendered strings quoted in PART 4 are derived from live database values passed through the same functions the components call, not from a screen I photographed. The build compiles and the strings are deterministic from those inputs; I am not claiming a visual check I did not perform.

---

## VERIFICATION

Display and messaging only, three files, 345 insertions. No eligibility rule, minimum, balance, earning, clip status or payout changed, and nobody became newly able or unable to withdraw: the gate file is not in the diff and `canRequest` is the same expression the removed attribute evaluated. The message reads each campaign's own `minPayout` as `/api/earnings` resolved it and compares it with the gate's own `toCents`, so it cannot contradict the block; no literal minimum was added, and `grep -c` for one in the touched components returns 0. Copy states a threshold, never a judgement, and never implies the clipper did anything wrong. The 6 money files plus `tracking.ts` and `campaign-era.ts` are byte-identical by blob OID on both refs. No `prisma migrate` was run; `prisma generate` only. Handles redacted, no wallet address selected or printed, every timestamp cast `::text` against DB `now()`. The worktree at `C:/b762` is removed. No dashes as bullets. The hooks gate passes at 0 errors and 11 warnings, identical to the pre-change baseline measured on the same worktree, and `tsc` and `next build` were both actually run with their exit codes echoed directly.
