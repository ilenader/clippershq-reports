# BL-689 (ClippersHQ) — a legitimate payout refusal stops being reported as a crash

**2026-07-30 · SHIPPED to `checkpoint/BL-689` @ `42af6f40`, verified on origin.** Base main `765bb0e4`. Tags `pre-BL-689` / `post-BL-689`.

**MESSAGING ONLY, and it is proven rather than asserted.** The gate condition and both cap assignments are **not in the diff**. A clipper refused before this round is refused after it, for the same amount, by the same rule. All three affected clippers still compute to `effectiveCap = $0.00`. **This round unblocks nobody.**

Clippers are `C-1` / `C-2` / `C-3` throughout, matching BL-688's mapping. No handle, email or wallet address appears anywhere.

---

## PART 1 — the matcher, fixed with a type rather than a looser string

`route.ts:514` threw:

```
Amount exceeds your total available balance ($0.00 available across your account)
```

`route.ts:616` routed on:

```ts
if (err.message?.includes("Amount exceeds available balance")) { ... 400 ... }
```

The words **`your total`** sit between `exceeds` and `available`. The substring missed, and a deliberate refusal fell past `:606`, `:613`, `:616` and `:619` to the catch-all at `:623`: a **500** telling three clippers to *"try again"* at something that can never succeed.

### What shipped

A new `src/lib/payout-refusal.ts`:

```ts
export type PayoutRefusalCode =
  | "DUPLICATE_PAYOUT"
  | "AMOUNT_EXCEEDS_CAMPAIGN_BALANCE"
  | "AMOUNT_EXCEEDS_GLOBAL_BALANCE"
  | "GLOBAL_BALANCE_LOCKED_BY_PENDING_PAYOUT"
  | "GLOBAL_BALANCE_NEEDS_REVIEW";

export class PayoutRefusal extends Error {
  readonly isPayoutRefusal = true as const;
  readonly code: PayoutRefusalCode;
  readonly httpStatus: number;   // always 4xx
}
```

and the entire catch chain for refusals becomes one branch:

```ts
if (isPayoutRefusal(err)) {
  return NextResponse.json({ error: err.message }, { status: err.httpStatus });
}
```

**The fragile substring comparison is DELETED, not widened.** Widening a substring is precisely how it broke.

### Why a future edit cannot re-break it

1. **Routing never reads the prose.** The only part a future round is likely to touch is the message, and editing it changes what the clipper reads while the 400 still routes.
2. **The code is a closed union.** A typo becomes a TypeScript error at the throw site, not a 500 discovered by a clipper weeks later.
3. **The discriminant is an own PROPERTY, not `instanceof`.** `instanceof` fails silently when a class is evaluated in more than one bundle, which Next can do across server and edge. That is the same silent-mismatch failure mode as the substring, so it was avoided deliberately.
4. **A refusal cannot carry a 5xx.** `isPayoutRefusal` requires `httpStatus` in `[400, 500)`, so this class of bug cannot reappear as "refusal answered with a server error".

Proven live, from the harness:

```
PASS  the OLD global message did NOT match the OLD substring matcher (this IS the bug)
PASS  routing survives a total rewrite of the message (a future edit cannot re-break it)
PASS  a real Error is NOT treated as a refusal (genuine faults still 500)
PASS  a refusal can never carry a 5xx status
```

---

## PART 2 — every thrown refusal on the payout path

| file:line | refusal | before | now |
|---|---|---|---|
| `payouts/route.ts:393` | `DUPLICATE_PAYOUT` | **MATCHED** at `:606` by exact sentinel | typed, same 409, same words |
| **`payouts/route.ts:514`** | global balance | **ORPHANED. This is the bug.** Fell to the 500 | typed, 400 |
| `payouts/route.ts:516` | campaign balance | **MATCHED but FRAGILE**, routed by substring, one word-edit from the identical failure | typed, 400 |
| `payouts/[id]/review/route.ts:122` | `PAYOUT_NOT_FOUND` | **MATCHED** at `:281`, exact sentinel | unchanged, owner path |
| `payouts/[id]/review/route.ts:135` | `INVALID_TRANSITION:` | **MATCHED** at `:284`, prefix | unchanged, owner path |
| `payouts/[id]/review/route.ts:215` | `INSUFFICIENT_BALANCE:` | **MATCHED** at `:291`, prefix | unchanged, owner path |
| `payouts/[id]/review/route.ts:582` | internal diagnostic | **caught locally** at `:589`, never reaches the handler | unchanged |
| `payouts/referral-request/route.ts:137` | `CommissionRaceError` | **MATCHED** at `:197`, already a typed class | unchanged |

**No orphan remains.** Worth noting the pattern: the OWNER review path already routed on code-shaped sentinels and never had this bug. Only the clipper-facing path used prose, which is how the one surface a clipper actually touches became the one that could report a refusal as a crash.

The three `route.ts` throws were converted even where already matched, so the path has **one** mechanism and no future reader has to work out which throws route by sentinel and which by prose.

---

## PART 3 — what the clipper actually reads

One zero hid three genuinely different realities, and BL-688 showed that answering all three with "you have no balance" is how a platform-side defect gets dressed as policy. The refusal now branches on figures already in scope. **The threshold is untouched; only the sentence differs.**

| code | when | status | shipped wording |
|---|---|---|---|
| `GLOBAL_BALANCE_NEEDS_REVIEW` | `globalPaid > globalEarned`, so more has been paid out than the countable pool holds | 400 | *"Something on our side is stopping this payout, not anything you did. Your earnings are safe. Open a support ticket in our Discord and the team will fix it."* |
| `GLOBAL_BALANCE_LOCKED_BY_PENDING_PAYOUT` | their own earlier request is still open | 400 | *"Most of your balance is held by a payout you have already requested. You can withdraw $X right now, and the rest becomes available once that payout is finished."* |
| `AMOUNT_EXCEEDS_GLOBAL_BALANCE` | account-wide figure is simply lower | 400 | *"You have $X available across your account right now. Enter $X or less and try again."* |
| `AMOUNT_EXCEEDS_CAMPAIGN_BALANCE` | asked for more than this campaign holds | 400 | *"You have $X available on this campaign right now. Enter $X or less and try again."* |
| `DUPLICATE_PAYOUT` | an open request exists | 409 | unchanged wording |

### Why the defect wording reads as it does

The accessibility lead rejected my first draft, and it was right to. My draft opened *"This balance needs a manual review"*. In every payments product a clipper has used, **"manual review" means we are checking YOU**: fraud, KYC, a hold on suspicion. The subject was "this balance" with the actor hidden, so it reads as something irregular about **their** money. That is exactly the accusation BL-518 and BL-521 forbid, and it presents a platform defect as a routine process step.

The shipped version instead:

* **names the cause and locates it with us** ("on our side"),
* **removes blame in the same breath** rather than as an afterthought ("not anything you did"),
* **answers the question they are actually asking** ("Your earnings are safe"),
* **never says "try again"**, because this condition is permanent and inviting a retry walks them into the 3-per-hour rate limit and a second, unrelated, more confusing message,
* **avoids the British idiom** "sort it out" for a global, largely non-native-English audience,
* is **154 characters**, inside the ~160 budget the error container allows at 375px before it pushes the submit control off-screen.

**One promise deliberately NOT made.** My draft said *"our team has been notified"*. I checked: **nothing on this path notifies anyone.** No email, no Discord webhook, no alert. So the claim was deleted and replaced with a support route that genuinely exists (the Discord ticket, `help-redesigned.tsx:103`). **An unkept promise here would be worse than the 500 it replaces.**

### A second, larger defect, found by the a11y review and fixed

`PayoutsRedesign.tsx` told **every** clipper sitting at $0.00:

> *"Earn on an approved clip to unlock a payout."*

That is **false** for these three. They earned on approved clips, were correctly paid, and their balance then computed to $0.00 because the clips that funded that payment were later retired. Telling someone who has earned that they have not earned is the same accusation, dressed as an empty state. It now splits on `totalEarned`, which the earnings API already returns, so there is no new request and no new field:

> *"No balance available to withdraw right now. If that looks wrong, open a support ticket in our Discord and the team will check it."*

**Stated honestly:** `totalEarned > 0` also covers the ordinary clipper who has simply withdrawn everything, and the client cannot currently tell that apart from the defect. So this copy is written to be **true for both** and to give either one a real route, rather than guessing. The API message is the specific one, because only the server knows that `globalPaid > globalEarned`. Giving the client that ability is a clean follow-up.

### The refusal is now actually heard

`PayoutRequestFlow.tsx:331` did `setLiveMsg("")` on error, silencing the one live region this component already proves works, at the exact moment it is needed. The freshly-mounted `role="alert"` races the focus move on the very next line, and NVDA and VoiceOver commonly cut an alert short to announce a newly focused control, so the refusal could be spoken partially or not at all. The error text is now **also** routed through the persistent polite region, which is precisely how the success path in the same file already solves the identical hazard. The visible `role="alert"` is unchanged for sighted users.

---

## PART 4 — evidence

`scripts/bl689-prove-messaging.ts`, **read only, 17 passed 0 failed**, against live data and the shipped code.

### The three affected clippers: still blocked, now truthfully told

```
C-1  campaignAvail=$15.74  globalEarned=$15.74   globalPaid=$25.54    globalAvail=$0.00  cap=$0.00
      refusal code -> GLOBAL_BALANCE_NEEDS_REVIEW
C-2  campaignAvail=$22.52  globalEarned=$33.26   globalPaid=$37.28    globalAvail=$0.00  cap=$0.00
      refusal code -> GLOBAL_BALANCE_NEEDS_REVIEW
C-3  campaignAvail=$14.65  globalEarned=$1848.32 globalPaid=$1894.14  globalAvail=$0.00  cap=$0.00
      refusal code -> GLOBAL_BALANCE_NEEDS_REVIEW

PASS  C-1 is STILL blocked (cap is $0.00, this round does not unblock anyone)
PASS  C-1 is classified as the PLATFORM-SIDE case, not "you have no balance"
PASS  C-2 is STILL blocked ...     PASS  C-2 is classified as the PLATFORM-SIDE case ...
PASS  C-3 is STILL blocked ...     PASS  C-3 is classified as the PLATFORM-SIDE case ...
```

**In all three, `globalPaid > globalEarned`.** The classifier is not guessing from a zero; it is reading the actual signature of the defect. C-3 is a useful check on the logic: a clipper with **$1,848.32** of lifetime countable earnings lands in the same class, which is exactly right, because the condition is about paid-versus-countable and never about being a small earner.

### An eligible clipper is unaffected end to end

```
most recent payout requester: earned=$47.00 paid=$32.61 locked=$14.05 globalAvail=$0.34
their last payout was created 2026-07-30T15:21:53.814Z for $14.05
PASS  an eligible request still passes the gate untouched
```

The platform's most recent successful request, made today, passes exactly as before. No new refusal can fire below the cap, because no branch was added above the unchanged threshold.

### Nothing changed that must not change

| claim | evidence |
|---|---|
| the gate condition is untouched | `git diff` for `Math.round(roundedAmount*100) > Math.round(effectiveCap*100)` returns **nothing** |
| both cap assignments are untouched | `git diff` for `effectiveCap = ` and `globalAvailable = ` returns **nothing** |
| the only variable change is a hoist | `globalEarned` / `globalPaid` / `globalLocked` moved `const` to a hoisted `let` with **byte-identical right-hand sides**, assigned in the same place, read only by the message selector |
| no payout created, modified, approved or cancelled | 144 rows, $14,123.39, identical before and after |
| refusal returns 400, not 500 | typed guard proven for all five codes; a genuine `Error` still 500s |

---

## An honest correction to the accessibility review

The review raised, as a MUST-FIX, that the **$52.86 campaign strip renders on the same screen as a $0.00 hero**, a contradiction a screen-reader user would hear as "$0.00 ... $52.86". **I checked, and that does not happen.** `/api/earnings:218` clamps every per-campaign balance to the global (`Math.min(b.available, balance.available)`), and `payouts/page.tsx:214` then filters `> 0`. With a global of $0.00 every campaign balance clamps to $0.00 and the strip renders **empty**. The contradiction is not live.

**But chasing that correction surfaced something more important, and it changes what this round can honestly claim.** The hero button is:

```tsx
disabled={available <= 0}   // PayoutsRedesign.tsx:208, `available` = the GLOBAL figure
```

So for these three clippers the button is **disabled**, and **the API message is not what they hit today**. Their binding surface is the empty-state copy, which is why fixing that false sentence matters as much as the 500. I am stating this rather than letting the round imply the three will now see the new API message; they will see it only if they reach the flow by another route.

**I did not enable the button.** That would change who can attempt a withdrawal, which this round forbids. The API fix is still necessary and correct: it protects every clipper whose global figure is above zero but below their campaign figure, it removes a permanent 500 from the codebase, and it makes the message reachable the moment the underlying money question is resolved.

---

## Safety and gates, stated honestly

* **6 money files + `tracking.ts` + `campaign-era.ts` BYTE-IDENTICAL by blob OID** on both refs: writer `7aa6be48`, earnings-calc `797e2098`, balance `e887f80a`, tracking `847dcf70`, middleware `61cef393`, money-decimal `ef5cdae7`, campaign-era `106e16ad`.
* **Diff:** 6 files. Two new (`src/lib/payout-refusal.ts`, the read-only proof script), three modified, plus `BACKLOG.md`. The real `.ts` diff is non-empty and quoted throughout. No schema change, no `prisma migrate`, no data write of any kind.
* **Gates, honest.** `npm ci` exit 0, then `npx prisma generate` exit 0 **before** typecheck. `npx tsc --noEmit` **exit 0 with 0 lines of output** (the first run failed with 5 missing-import errors, which is recorded here rather than hidden; the import was added and it now passes). `npm run build` **BUILD_EXIT=0** read from a captured log, never piped through `tail`: BYPASS detector **0 violations**, `check:removed-fields` OK, `lint:hooks` **11 problems (0 errors, 11 warnings)** at the ≤11 cap with **eslint v9.39.4 present**. Compiled 61/61 pages. Counts by `grep -c`, never `head`.
* **No dashes as bullets.** No wallet address printed. Nothing held by a live round (BL-690) was touched.
* **Rollback:** `git revert 42af6f40`, or `reset --hard pre-BL-689`.

## What is explicitly NOT fixed

**Whether these three should be paid their $52.86 is untouched and remains the owner's decision.** This round only stops the platform from calling a decision a crash. The underlying question, that the global clamp subtracts a correct past payment from a pool that no longer contains the earnings which funded it, is exactly as BL-688 left it.

Two follow-ups worth a round each: give the client enough signal to distinguish the defect from an ordinary spent balance, and reconsider `disabled={available <= 0}`, which currently means the clippers most in need of an explanation are the ones who cannot reach the screen that would give them one.
