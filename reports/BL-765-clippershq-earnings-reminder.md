# BL-765 — the reminder beside each campaign in earnings, and the clamp that hid it from the one clipper it was for

**2026-08-10 · DB now() = `2026-08-10 18:21:59.331419+00` · BUILD. Display and messaging only.**
Base `origin/main` @ `4f1f7113` (the BL-764 merge of BL-762). Branch `checkpoint/BL-765` @ `9d9c1936`, **verified pushed**. Tags `pre-BL-765` (`4f1f7113`) and `post-BL-765` (`9d9c1936`) both on origin. Isolated worktree `C:/b765`, short path, no junctioned `node_modules`, removed at the end of the round.

**No eligibility rule, minimum, balance or earnings changed, and no clipper became newly able or unable to withdraw.** `src/app/api/payouts/route.ts` is not in the diff. Handles are redacted throughout and no wallet address was selected or printed.

---

## THE THING I HAVE TO SAY FIRST

**BL-762 never rendered for the clipper it was written for.** I built BL-762 last round, reported it as fixing his case, and it did not. This round found out why and fixed it, and the reason is worth stating before anything else because it is the whole shape of BL-765.

`/api/earnings` clamps every per-campaign `available` to the clipper's **global** balance (`Math.min(b.available, balance.available)`, the BL-187-P2 clamp, on by default). Clipper A's global computes to **$0.00**, because BL-698 removes his retired-clip earnings from the display while every payment he has received stays counted. So both of his campaign figures were clamped to zero, and `payouts/page.tsx` dropped both rows with its `available > 0` filter. `splitCampaignsByMinimum` then received an empty array, the blocked group rendered nothing, and the hero fell through to BL-689's sentence: *"open a support ticket in our Discord."*

Measured on live data: **3 (clipper, campaign) pairs across 2 clippers, holding $13.49, are invisible for exactly this reason.** One of the two is Clipper A. BL-762 made the wall visible for 136 positions and left silent the 3 that caused the complaint.

I did not catch this in BL-762 because I read the per-campaign figure out of `computeCampaignBalances` and never followed it through the clamp applied twenty lines later in the same route. That is the correction; the rest of this report is the fix.

---

## PART 1 — THE REMINDER, WHERE HE ALREADY LOOKS

Beside every campaign row on the earnings page, with no click, hover or expansion. Healthy rows stay clean.

### The exact copy shipped

**Blocked, campaign still running:**

> **$12.19 of $20.00 minimum • $7.81 to go**

**Blocked, campaign finished and can never grow again:**

> **$3.21 of $10.00 minimum • campaign finished, so this balance will not grow**

**Withdrawable:** nothing. A row with no problem does not grow a sentence saying so.

**Held by the overall balance** (balance clears its own minimum but the global position is binding, **zero rows today**):

> **$X on this campaign, held by your overall balance**

**Once per card, only when at least one finished campaign appears:**

> A finished campaign cannot grow, so a balance under its minimum stays where it is. *Ask about a finished campaign balance* → `/help`

**One `sr-only` sentence per row**, because every visible number fragment is `aria-hidden`:

> "9 clips, $12.19 earned in the period shown. This campaign has a $20.00 minimum withdrawal and you have $12.19 available on it. You need $7.81 more on this campaign before you can withdraw from it."

The second clause is `belowMinimumMessage` — the **same function the server gate calls when it refuses the request**, passed `campaignName: "This campaign"` so the visible row name is not read twice.

### Why the copy reads like this

It states a threshold and never a judgement, per BL-518 and BL-521. Nothing implies the clipper did anything wrong, because he did not. The shortfall is measured **against the balance**, never against a typed amount, which is BL-728's rule. There is no "contact support" on a row that has an achievable answer, and there is exactly one route offered where support genuinely is the only route.

### It cannot contradict the gate

`campaignMinimumState` and `clearsMinimum` compare **`toCents(balance) >= toCents(minPayout)`**, importing `toCents` from `payout-minimum-shared.ts` — the identical function, from the identical module, that the gate performs at `payouts/route.ts:346`. `minPayout` is the campaign's own value, resolved server-side by `resolveMinPayout`. **No literal minimum was introduced.** BL-734 found seven scattered copies of this value and made them agree; this round adds a copy of neither the value nor the sentence.

---

## PART 2 — THE CASE THAT CAUSED THIS, AND THE FROZEN CASE

### Clipper A: two blocked campaigns, previously invisible, now stated

| campaign | status | **balance** | clamped `available` | minimum | shortfall | row state |
|---|---|---|---|---|---|---|
| Zhus Edit (0.50 CPM) | ACTIVE | **$12.19** | $0.00 | $20.00 | **$7.81** | below minimum |
| Zhus Meme (0.20 CPM) | ACTIVE | **$0.42** | $0.00 | $20.00 | **$19.58** | below minimum |

Before this round both rows rendered **nothing at all** on either screen, because the clamped column is what every consumer read. He now reads, beside each campaign:

> Zhus Edit (0.50 CPM) · **$12.19 of $20.00 minimum • $7.81 to go**
> Zhus Meme (0.20 CPM) · **$0.42 of $20.00 minimum • $19.58 to go**

### A mixed clipper, all three states in one screen

`cmq7qh6p` / `f191a2` holds five campaigns:

> **Ready** (no reminder line): WinGram **$73.23**, Panic Baby **$46.51**
> **Below minimum, still running**: Zhus Meme (0.20 CPM) · $1.61 of $20.00 minimum • $18.39 to go
> **Finished**: somesome · $3.73 of $10.00 minimum • campaign finished, so this balance will not grow · and bees.n.honey · $3.25 of $10.00 minimum • campaign finished, so this balance will not grow

A single global figure hid all five distinctions. There are now three visibly different row states on one screen, and the two withdrawable ones are the two carrying no reminder at all.

### The frozen case, handled rather than recorded

**I did not defer this.** BL-763 established the rule and priced it:

> "Archiving permanently freezes accrual. There is no path back: un-archiving is possible, but nothing in the product resumes accrual."
> "Archiving is a one-way trap for anyone below the minimum."
> "On WinGram that is 17 clippers holding $65.65 that they can never reach."

Measured this round across the whole platform, **93 of the 139 blocked pairs are on a campaign that can never accrue again: 85 clippers, $262.69.** That is 67% of the blocked population, so "earn $X more" would have been false for two clippers in every three.

| campaign | status | blocked pairs | clippers | dollars | can accrue |
|---|---|---|---|---|---|
| GainzAlgo (REPOST CAMPAIGN) | PAST | 21 | 21 | $72.87 | **no** |
| somesome | PAST | 23 | 23 | $71.85 | **no** |
| **WinGram** | PAUSED + archived | **17** | **17** | **$65.65** | **no** |
| bees.n.honey | PAST | 29 | 29 | $47.80 | **no** |
| STRAENGE | PAST | 3 | 3 | $4.52 | **no** |
| Zhus Edit (0.50 CPM) | ACTIVE | 8 | 8 | $63.07 | yes |
| Zhus Meme (0.20 CPM) | ACTIVE | 15 | 15 | $37.05 | yes |
| Panic Baby | PAUSED | 14 | 14 | $43.40 | yes |
| BAD BITCH ANTHEM (2.50 / 0.50) | ACTIVE | 8 | 8 | $23.27 | yes |
| SomeSome | PAUSED | 1 | 1 | $4.11 | yes |

WinGram's 17 clippers and $65.65 reproduce BL-763's figure to the cent.

**Those rows never show a shortfall**, on either screen. They read "campaign finished, so this balance will not grow", and the payouts card's right-hand figure changes from "$6.79 to go" to "will not grow". The word **"yet"** now appears only when every blocked campaign can still grow: the group heading is "Not at the minimum yet" normally and "Not at the minimum" when all of them have finished, and the hero sentence names how many have finished.

**A PAUSED campaign that is not archived is deliberately treated as still able to accrue**, because the owner can lift a pause and routinely does. Panic Baby (PAUSED, not archived, 14 pairs, $43.40) therefore still reads "to go". That is a judgement call and it is the one place the copy is optimistic; it is stated here so it can be revisited rather than discovered.

---

## PART 3 — AGREEMENT WITH BL-762'S PAYOUT SCREENS

**One module, one predicate, one sentence, shared by both screens.** `src/lib/below-minimum-campaigns.ts` owns the classification; `belowMinimumMessage` owns the wording; both screens import both. The earnings page and the payouts page are two readings of the same array of rows returned by one request.

They did **not** agree before this round, and making them agree was most of the work:

• The payouts screen classified from the **clamped** `available`. Against that figure a clipper was told he had **$0.00 of $20.00** and needed the whole **$20.00**, when he holds **$12.19** and needs **$7.81**. Both screens now read the unclamped balance for the blocked explanation.
• `shortfallToMinimum` was measuring against the clamped figure too, so it produced the same wrong number. It now measures against the balance.
• The payouts hero and the earnings hero had no finished arm, so both would have said "yet" to 85 clippers for whom it can never arrive.
• The earnings hero's link pointed at `/payouts`, which was the only place per-campaign detail existed. That detail is on the earnings page now, so the link is an in-page anchor to the card, with `id` and `tabIndex={-1}` on the heading so focus actually lands and the heading is announced.

**`ready` is unchanged, by construction.** It is still decided by `clearsMinimum`, which still reads the clamped `available`. Not one campaign leaves that group and nobody is shown a withdrawable figure larger than the gate allows. The only movement is rows entering `blocked`, the group that by definition offers nothing.

**The request flow is untouched.** `availableCampaigns`, which is also the flow's campaign selector, is left exactly as it was; the unclamped rows travel to the display component in a separate `campaignPositions` prop. A campaign offering $0.00 can never appear as a selectable option.

---

## PART 4 — THE EVIDENCE

**A blocked row states balance, minimum and shortfall.** Clipper A's Zhus Edit row: `$12.19 of $20.00 minimum • $7.81 to go`, from `campaignBalance = 12.19`, `minPayout = 20.0000` (the owner's own stored raise, `numeric(18,4)`), `shortfallToMinimum = 7.81`.

**A withdrawable row is unchanged.** `cmr0gixm`'s Panic Baby row, $545.37 against a $10.00 minimum, renders `state === "ready"` and the reminder block does not render at all. Its markup is the pre-existing row with two additions that are invisible to sighted users: `aria-hidden` on the numeric fragments and one `sr-only` sentence.

**A mixed-campaign clipper sees which is which.** `cmq7qh6p`, rendered in PART 2: two ready rows with no reminder, one below-minimum row with a shortfall, two finished rows without one.

**A frozen row does not tell the clipper to earn more.** `cmr0gixm` on WinGram holds $3.21 against a $10.00 minimum on a PAUSED **and archived** campaign. `canAccrue` is false, so the row reads `$3.21 of $10.00 minimum • campaign finished, so this balance will not grow`. The `$6.79 to go` that BL-762's logic would have printed is suppressed.

**The figures match the gate.** `campaignMinimumState` and `clearsMinimum` compare `toCents(...)` imported from `payout-minimum-shared.ts`, the module the gate imports at `payouts/route.ts:25` and compares with at `:346`. `grep -c` for a hardcoded minimum in the touched components returns 0.

**Nobody became newly able or unable to withdraw.** The gate file is not in the diff. `ready` is still `clearsMinimum` on the clamped `available`. The 26 ready positions and the 139 blocked positions are the same sets before and after; what changed is that 3 of the 139 are now visible.

**No clip's earnings or status changed and no payout was touched.** This round wrote nothing to the database; every read went through `scripts/run-select.js`, which refuses any write keyword before connecting.

### The money files

Blob OIDs compared with `git rev-parse` on **both** refs:

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

`eslint` is present in the worktree's `node_modules/.bin`, so the BL-348 hooks gate is a real check and not a silent no-op. `npx prisma generate` was run after `npm ci` and before any typecheck.

| gate | baseline, before the first edit | after |
|---|---|---|
| `npx tsc --noEmit` | | **exit 0**, 0 lines of output |
| `npm run build` (runs `prebuild`) | | **exit 0**, compiled in 27.0s |
| `lint:hooks` | **0 errors, 11 warnings** | **0 errors, 11 warnings** |

Exit codes were captured with `echo "BUILD_EXIT=$?"` straight after the command, never read through a pipe. The gate permits `--max-warnings 11` and sits at exactly 11, so this change had to add **zero**; that is why the two new derivations run during render rather than inside a `useMemo` whose dependency array would be a new liability. The diff is real and non-empty: 5 files, +350 / −29.

### The five widths, and what I actually did

**I did not render the page in a browser, and I will not claim I did.** The clipper earnings page sits behind a Discord OAuth session I do not have, so an authenticated screenshot was not available to me. What I did instead was a static audit of the new markup for the constructs that actually cause horizontal overflow:

• The `<li>` is now a **column**. Its first child is the original flex row, so the reminder occupies the full card width instead of competing as a flex sibling with the thumbnail and the amount. At 320px it wraps as ordinary inline text.
• The reminder is a single `<p>` with **no flex children, no fixed width, no `whitespace-nowrap`**. `grep` over the added lines returns exactly one `whitespace-nowrap`, and it is the pre-existing earned figure, which is `shrink-0` beside a sibling carrying `min-w-0 flex-1` — the standard safe pairing, unchanged.
• The thumbnail drops from `h-14 w-14` to `h-12 w-12` below the `sm` breakpoint, which is the cheapest relief at 320 and 375 and costs nothing at 414, 1280 and 1440 where the `sm:h-14 sm:w-14` restores it.
• The grid columns on the payouts strip (`grid-cols-1 sm:grid-cols-2 lg:grid-cols-3`) are untouched.

That is a reasoned argument from the CSS, not a measurement, and it should be read as one.

### Accessibility

The accessibility lead reviewed the plan **before** any UI was written. All four blocking items are satisfied.

**Mixed scopes, its most important catch.** `byCampaign.earned` is scoped to the selected timeframe and campaign filter; a campaign balance is all-time. A sighted reader absorbs the card's "This period" header, but a screen-reader user hearing two figures in one sentence has no way to tell them apart. Both clauses of every spoken sentence now name their own scope in words: *"$12.19 earned in the period shown"* and *"you have $12.19 available on it"*.

**Hero and rows had to move together.** The hero note is built from the same rows, so feeding only the rows from the unclamped field would have left the hero silent for exactly this clipper while the row beneath it stated a balance.

**The progress bar.** It encodes earned-versus-largest-campaign, and sitting directly above "$12.19 of $20.00 minimum" a sighted user would read it as progress toward the minimum. The reminder was moved below the amount row and separated by a left-border block. It stays `aria-hidden`, so this was sighted-only misinformation rather than a WCAG failure, but it is the same class of defect this round exists to close.

**"yet" removed from finished copy**, in the row, the group heading and both heroes.

Also applied: no `aria-live`, `role="status"` or `role="alert"`, because this is first-paint content and the rows re-render on every filter click; every numeric fragment `aria-hidden` behind one spoken sentence, with the campaign **name left visible to AT** as the row's anchor and not repeated inside the sentence; a row with no matching balance gets no reminder and no state clause, rather than a fabricated "$0.00 of $20.00" that would invent a grievance; the left-border block as the non-colour state marker, since the state words already differ and the house rule forbids dashes as bullets; and no per-row icons, which at 320px would be a fifth thing to lay out for no information.

On colour: the reminder is **never** `text-accent`. `#2596be` is 3.40:1 on this card in the light theme the navbar toggle exposes, and an 11px line is nowhere near large text. `--text-secondary` carries the meaning and `--text-muted` the trailing fragment; both are distinct in light (`#18181b` / `#27272a`) and legible in dark. The support link is `text-accent` but is `font-semibold` and underlined, so it does not rely on colour alone.

**Two items deferred, disclosed rather than skipped.** The WCAG 4.1.3 announcement for a campaign crossing its minimum during an SSE refresh still needs debounced state and an id-set comparison, and the hooks gate is at 11 of 11. BL-698's existing note in this same component is still white-on-white in the light theme; pre-existing, untouched, reported. Both are in the BACKLOG.

---

## WHAT THIS ROUND DID NOT DO

• **It did not pay anybody or lower a minimum.** 112 clippers still hold $432.18 they cannot reach, 85 of them on campaigns that can never grow. The screen now says so; the decision is the owner's.
• **It did not fix the clamp asymmetry itself.** `/api/earnings` still clamps the displayed `available` to a base that excludes retired clips, while the gate's own global clamp uses the lifetime base including them, so the display remains stricter than the gate. This round routes around it with an additive field rather than changing what any existing number means, because that is a money-semantics change and belongs in its own round with its own proof.
• **It sent no notification.** The owner explicitly did not want payout notifications, and none was added.
• **It ran no browser.** See PART 4.

---

## VERIFICATION

Display and messaging only, 5 files, +350 / −29. No eligibility rule, minimum, balance or earnings changed and nobody became newly able or unable to withdraw: the gate file is not in the diff, `ready` is still `clearsMinimum` on the clamped `available`, and the request flow's option list is byte-unchanged. Every figure comes from the gate's own `toCents` and `belowMinimumMessage` rather than a duplicate; `grep -c` for a hardcoded minimum in the touched components returns 0. The earnings page and the payout screens read the same rows through the same module, so they cannot show different numbers. Copy is plain and non-accusatory, and never tells a clipper to earn more on a campaign where that is impossible: 93 pairs across 85 clippers holding $262.69 read "will not grow" and no shortfall. The 6 money files plus `tracking.ts` and `campaign-era.ts` are byte-identical by blob OID on both refs. No `prisma migrate`; `prisma generate` only. No clip's earnings or status changed and no payout was created, modified, approved or cancelled. Handles redacted, no wallet address printed. The worktree at `C:/b765` is removed. No dashes as bullets. The hooks gate passes at 0 errors and 11 warnings, identical to the pre-change baseline measured on the same worktree, and `tsc` and `next build` were both actually run with their exit codes echoed directly.
