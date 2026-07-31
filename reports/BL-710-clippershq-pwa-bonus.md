# BL-710 (ClippersHQ) — is the PWA earnings bonus being granted to people who did not install the app?

## THE MECHANISM IS FORGEABLE, NOBODY APPEARS TO HAVE FORGED IT, AND THE ENTIRE UNCORROBORATED EXPOSURE IS AT MOST $4.72. BL-708 was right that the header is client-supplied and trivially forgeable, and the endpoint's own comment admits it. But BL-708's framing missed the guard that matters: all three call sites fire only after the browser's own install prompt returns `outcome === "accepted"`, so the flag does NOT happen automatically to ordinary users who merely see the popup. It requires deliberate tooling. Measured against the only independent corroborating signal the schema holds, **168 of the 319 flagged clippers are positively confirmed to be running the installed app, and they account for $127.29 of the $132.00 total exposure. The remaining 151 are dormant, hold at most $4.72 between 16 people, and are indistinguishable from legitimate installers who simply stopped clipping.**

**2026-07-31 · AUDIT ONLY. READ ONLY on code, data and money. No flag was cleared, no bonus altered, no earnings recalculated, no payout touched. Nothing was fixed.**
**Base** origin/main `4b1d86aa` · **Branch** `checkpoint/BL-710` · **Worktree** `C:/b710` (short path, node_modules never junctioned) · **DB `now()` at final query: 2026-07-31 18:51:12.290385+00.**

**Redaction.** The reports repo is PUBLIC. Every figure below is a count or an aggregate. **No handle, email or user id appears anywhere in this document**, and none was selected by any query.

---

## PART 1 — the grant path, traced

### What sets the flag

**`src/app/api/user/pwa-status/route.ts`**, the POST handler. In order:

| step | line | what it does |
| --- | --- | --- |
| 1 | `:24` | `requireNotBanned()` so the caller must be an authenticated, non-banned user |
| 2 | `:29` | rate limit, **30 requests per minute per user** |
| 3 | `:34-37` | reads `x-pwa-mode`; **if it is not exactly `standalone`, returns 400** |
| 4 | `:41-49` | parses `installed` from the body, defaulting to `true` |
| 5 | `:53-58` | if `installed` and not already flagged, **sets `isPWAUser: true` and `lastPWAOpenAt: now()`** |
| 6 | `:60-61` | calls `recalculateUnpaidEarnings`, so the bonus applies to unpaid clips immediately |

### Is the header the only input? Yes, and the code says so

**There is no second check and no server-side corroboration.** The only gate on the grant is the client-supplied header, and the file states this plainly at `:31-33`:

> *"Basic PWA-context signal: the app sets X-PWA-Mode: standalone from installed contexts. Not cryptographically bulletproof (headers can be forged with curl), but blocks casual abuse from someone just hitting the endpoint from a normal browser tab."*

**So BL-708's finding is confirmed: the flag is obtainable by anyone who can send a header.** The endpoint cannot tell a real installed context from a crafted request.

### But BL-708's framing missed the guard, and the distinction is the whole round

BL-708 described the install popup as rendering only for non-PWA users yet sending a standalone header to the granting endpoint. That is literally true about the header being hardcoded. **It is not true that the POST fires from merely rendering or interacting with the popup.** All three call sites are guarded:

| call site | guard | verdict |
| --- | --- | --- |
| `app-layout.tsx:153` | `if (isPWA && ...)` where `isPWA` comes from `useIsPWA()` | fires only from a genuinely standalone context |
| `pwa-install-popup.tsx:250` | inside `if (success)` after `await triggerNativeInstall()` | fires only on a real accepted install |
| `pwa-install-popup.tsx:386` | inside `if (success)` after `await triggerNativeInstall()` | fires only on a real accepted install |

`useIsPWA` (`src/hooks/use-pwa.ts:10-11`) reads `window.matchMedia("(display-mode: standalone)").matches || navigator.standalone === true`. That is the browser reporting the display mode, not the page asserting it.

`triggerNativeInstall` (`use-pwa.ts:96-118`) returns `true` **only when `result.outcome === "accepted"`** from `BeforeInstallPromptEvent.userChoice`. A user who sees the popup and dismisses it, or who opens the native prompt and cancels, gets `false` and **no POST is sent at all**.

**Is this a bug, a convenience or a leftover? It is a deliberate convenience with a known and documented weakness.** The header exists so the endpoint can reject a bare browser tab hitting it. The comment shows the author knew it was not a security boundary. What is missing is not the guard on the client, which is correct, but any server-side confirmation, which is genuinely absent.

### How hard is it to get the flag without installing? It requires intent and tooling

**Stated plainly, because the brief is right that these are very different problems.** To obtain the flag without installing, a person must:

1. already hold an authenticated, non-banned session, and
2. deliberately craft a POST to `/api/user/pwa-status` carrying `X-PWA-Mode: standalone`, using curl, devtools or a script.

**It does not happen automatically.** Seeing the popup does nothing. Dismissing it does nothing. Clicking install and then cancelling the browser dialog does nothing. There is no code path where an ordinary user is flagged without the browser itself reporting an accepted install or a standalone display mode.

**So this is the first of the two problems the brief distinguished, not the second, and it is the far less serious one.** Given that, 319 of 1,240 is not evidence of accidental mass granting; it is consistent with 319 people having installed the app, which PART 2 tests directly.

---

## PART 2 — who has it, and does it look real?

### The population

| measure | value |
| --- | --- |
| users | 1,289 |
| clippers | 1,240 |
| flagged, all roles | 323 |
| **flagged clippers** | **319** |
| flagged with `lastPWAOpenAt` NULL | **0** |
| earliest open | 2026-04-19 15:58:05.088 |
| latest open | 2026-07-31 18:47:29.942 |

**Every flagged user has a non-null `lastPWAOpenAt`.** The most recent is seconds before the query, so the installed app is in active use right now.

### The corroborating signal, and why it is independent

`lastPWAOpenAt` is refreshed by the hourly sync at `app-layout.tsx:150-161`, which is gated on `isPWA`, the real `display-mode: standalone` media query. **A recent `lastPWAOpenAt` therefore cannot be produced by a one-off forged request.** A forger would set it once and it would then go stale, because the refresh only fires from a genuinely installed context.

**Recency across the 319 flagged clippers:**

| last opened | flagged clippers | oldest in bucket | newest in bucket |
| --- | --- | --- | --- |
| within 24 hours | **37** | 2026-07-30 19:57:51.8 | 2026-07-31 18:48:08.705 |
| within 7 days | **49** | 2026-07-25 07:50:00.252 | 2026-07-30 18:21:18.88 |
| within 30 days | **82** | 2026-07-01 21:36:30.496 | 2026-07-24 09:52:17.473 |
| over 30 days | **151** | 2026-04-24 17:23:18.229 | 2026-07-01 08:34:15.889 |

**168 of 319 have opened the installed app within the last 30 days.**

### No clustering, which is what an accidental mass grant would look like

If the flag were being granted accidentally by a deploy or a popup change, the timestamps would cluster. They do not. Across every day with 3 or more dormant flagged users, **the number of distinct minutes equals the number of users on every single day** — no two people share a minute — and each day's grants spread across the full 24 hours:

| day | flagged clippers | distinct minutes | first that day | last that day |
| --- | --- | --- | --- | --- |
| 2026-06-10 | 8 | **8** | 09:40:04.612 | 19:37:27.902 |
| 2026-06-30 | 7 | **7** | 02:31:50.218 | 17:47:16.67 |
| 2026-06-16 | 7 | **7** | 04:31:25.127 | 21:44:30.285 |
| 2026-05-05 | 6 | **6** | 10:16:03.778 | 21:23:10.958 |
| 2026-06-18 | 5 | **5** | 10:52:21.137 | 22:18:23.171 |
| 2026-06-28 | 5 | **5** | 01:45:42.266 | 17:22:13.105 |

The busiest day is 8 users. **That is the organic pattern of individuals installing at their own times, and the opposite of a burst.**

### Can genuine installers be told apart from accidental or forged grants? PARTLY, and here is exactly where the line falls

**YES for 168 of them, positively.** A `lastPWAOpenAt` inside 30 days is produced only by a real standalone context, so those are confirmed installers. This is a positive proof, not an inference.

**NO for the other 151, and I will not estimate.** `lastPWAOpenAt` proves genuineness when recent, but its absence proves nothing. **A legitimate installer who stopped clipping is indistinguishable in the data from someone who forged the header once and never returned.** There is no column recording the original grant time, no user-agent capture, no request log retained, and `lastPWAOpenAt` is overwritten on every refresh, so the original grant timestamp is unrecoverable for anyone who has opened since.

**Stated plainly as the brief demands: the data cannot classify those 151, and any number I produced for "how many are illegitimate" would be invented. I am not producing one, because it would be used to take money from real people.** PART 3 shows why it does not matter anyway.

---

## PART 3 — what it has cost

### The bonus is capped, so 2% is a ceiling and not a rate

`earnings-calc.ts:157` computes `pwaBonus = isPWAUser ? PWA_BONUS_PERCENT : 0` with `PWA_BONUS_PERCENT = 2` at `:61`. Crucially, `:164`:

```ts
totalBonusPercent = Math.min(levelBonus + streakBonus + pwaBonus, maxBonusCap);
```

**The PWA bonus is additive into a CAPPED total.** For any clipper already at or above the cap from level and streak alone, the PWA flag contributes **nothing at all**. So "2% of flagged earnings" is a strict upper bound, and the true figure is lower. **The stored `Clip.bonusAmount` is the total bonus and is not decomposed by source, so the exact PWA-attributable figure is NOT recoverable from stored data.** That limit is stated rather than estimated around.

### The money

| measure | value |
| --- | --- |
| flagged clippers | 319 |
| **of which have ANY approved earnings** | **69** (the other 250 have earned nothing, so the flag has cost nothing for them) |
| flagged base earnings | $6,600.18 |
| flagged bonus of all kinds (level + streak + PWA, capped) | $370.18 |
| flagged total earnings | $6,970.35 |
| **PWA upper bound, 2% of flagged base** | **$132.00** |
| already paid out | $5,469.07 |
| still in balances | $1,501.28 |

**Split by corroboration, which is the number that decides everything:**

| group | clippers | with earnings | base earnings | **PWA upper bound** |
| --- | --- | --- | --- | --- |
| **corroborated**, opened within 30 days | 168 | 53 | $6,364.25 | **$127.29** |
| **not corroborated**, dormant 30+ days | 151 | 16 | $235.93 | **$4.72** |

**96.4% of the entire exposure sits with clippers positively confirmed to be running the installed app.** The whole uncorroborated remainder is **at most $4.72 across 16 people**.

### The monthly rate, and it is falling

| month | flagged base | PWA upper bound | clips |
| --- | --- | --- | --- |
| 2026-04 | $280.60 | $5.61 | 10 |
| 2026-05 | $2,509.57 | $50.19 | 355 |
| 2026-06 | $1,997.08 | $39.94 | 986 |
| 2026-07 | $1,812.93 | $36.26 | 929 |

**Roughly $36 to $50 a month at the ceiling, trending down.**

### Material or trivial? Trivial, stated honestly

Platform-wide: total earnings **$10,449.85**, base $9,978.47, bonus of all kinds $471.39. **The PWA upper bound of $132.00 is 1.26% of all platform earnings ever, and at most 28% of the total bonus pool.** The uncorroborated slice, $4.72, is **0.045%** of platform earnings.

### Is it inside BL-617's correctness, or a leak outside it? INSIDE

**The earnings invariant is 0 violations across the population** (`earnings = baseEarnings + bonusAmount`, ±$0.01, measured this round). The PWA bonus flows through the sanctioned calculator, is capped with the other bonuses, is written through the normal path, and satisfies the invariant. **It is not a leak outside the money model. It is a correctly computed bonus whose eligibility input is weakly authenticated.** That distinction matters: nothing is miscounted, the only question is who qualifies.

---

## PART 4 — the options

### (a) Leave it

* **Money:** $0 recovered. Ongoing ceiling ~$36 to $50 a month, falling.
* **Who is affected:** nobody. No clipper notices anything.
* **Honest downside:** the endpoint stays forgeable, and if anyone ever publicises it the cost could rise. Against that: exploiting it requires an account plus deliberate tooling for a **2% bonus that is capped and often contributes nothing**, which is a poor return on effort, and there is no evidence in the data that anyone has bothered.

### (b) Fix the grant going forward, leave existing flags alone

* **Money:** $0 taken from anyone. Stops any future uncorroborated grant.
* **Who is affected:** nobody loses anything. Future genuine installers still qualify.
* **What a clipper experiences:** nothing changes. Installing still grants the bonus.
* **Honest downside:** there is no bulletproof server-side proof that a request comes from an installed PWA. The realistic improvement is **defence in depth, not a guarantee**: require the flag to be corroborated by a subsequent standalone-context refresh before the bonus counts, or verify a `Sec-Fetch-Site` and origin combination, or simply require two separate standalone syncs at least an hour apart before granting. Each raises the effort bar without ever closing it completely. **Do not oversell this as a fix; it is a hardening.**

### (c) Fix the grant AND clear uncorroborated flags

* **Money at stake: at most $4.72**, being the full upper bound on the 16 uncorroborated clippers who have earnings.
* **Who would be wrongly stripped: UNKNOWN, and that is the point.** The 151 uncorroborated users are dormant, and **a legitimate installer who stopped clipping is indistinguishable from a forger**. Some unknown fraction of the 16 with earnings installed the app honestly. I will not estimate the split because the data cannot support one.
* **What a clipper experiences:** someone who installed the app months ago, earned honestly, then took a break would return to find their bonus silently removed and their unpaid balance reduced, with no way to tell them why beyond "we could not confirm your install".
* **Honest downside: this spends real trust to recover at most $4.72, while wrongly penalising an unknown number of honest people.** The cost/benefit is not close.

### (d) The better option: fix forward, and add the corroboration column that would have answered this question

Option (b), plus **record the grant provenance** so this is answerable next time without a forensic round. Today `lastPWAOpenAt` is overwritten on every refresh, which destroys the original grant time, and nothing records how a flag was obtained. Adding a `pwaGrantedAt` and a coarse grant-source marker costs nothing, takes no bonus from anyone, and means a future audit can classify rather than shrug.

**It also enables option (b)'s strongest form:** if the grant is recorded separately from the refresh, the bonus can be made contingent on **at least one subsequent standalone refresh**, which a forged one-off request would never produce. That converts the weak client claim into a claim the client must sustain from a real installed context, without taking anything from anyone.

---

## PART 5 — the verdict

### ONE LINE

**The mechanism is genuinely forgeable but requires deliberate tooling rather than happening to ordinary users, no evidence of exploitation exists in the data, and the entire cost is at most $132.00 ever with at most $4.72 of it uncorroborated, which is 0.045% of platform earnings.**

### Recommended: option (d), which is (b) plus provenance. Explicitly NOT (c)

**Ship the forward hardening and record grant provenance. Do not touch a single existing flag.**

The reasoning is arithmetic rather than sentiment. Clearing uncorroborated flags targets **at most $4.72**, would wrongly strip an unknown number of honest installers, and buys nothing that stopping future grants does not already buy. **Meanwhile 96.4% of the exposure belongs to people positively confirmed to be running the installed app, which is exactly the behaviour the bonus exists to reward.**

**No clawback of already-paid earnings is recommended, and none should be considered.** $5,469.07 of the flagged population's earnings is already paid out. BL-538's never-decrease guard exists precisely so a clipper is never told they earned something and then charged for it, and taking back settled money over a 2% capped bonus would be the worst available outcome for the smallest available sum.

### What must be proven before the hardening ships

1. **No existing flag changes**, and no clipper's balance goes down. Measure before and after across all 1,240 clippers.
2. **A genuine install still grants the bonus.** The three existing call sites already gate correctly, so this must be re-proven, not assumed.
3. **The earnings invariant stays at 0 violations**, and no `recalculateUnpaidEarnings` run reduces anyone's unpaid total.
4. **The bonus cap still binds**, so the change cannot raise anyone above `maxBonusCap`.
5. If a corroboration requirement is added, **prove it fails OPEN for a user whose install is real but whose refresh has not yet fired**, so a fresh installer is never denied a bonus they earned.

### Rollback

The hardening is a code change to `pwa-status/route.ts` plus, optionally, an additive nullable column. **`git revert` restores today's behaviour exactly**, and because no existing flag is cleared and no earnings are recalculated downward, there is no data state to unwind. That is the main practical argument for (d) over (c): **(d) is fully reversible and (c) is not.**

### What could not be measured

**The original grant timestamp is unrecoverable** for any user who has opened the app since, because `lastPWAOpenAt` is overwritten on every refresh and no separate grant column exists. **The exact PWA-attributable share of the $370.18 bonus pool is not decomposable**, because `Clip.bonusAmount` stores the capped total and not its components, so $132.00 is a strict ceiling and the true figure is lower by an unknown amount. **Whether any of the 151 dormant flags is illegitimate is unknown and is deliberately not estimated.** No request logs, user agents or install telemetry are retained, so no forensic attribution of any individual grant is possible.

---

## Safety

READ ONLY. One document. **No `isPWAUser` flag was cleared, no bonus was altered, no earnings were recalculated, no payout was created, modified, approved or cancelled, and no clip status changed.** Every figure comes from read-only `SELECT`s via the sanctioned `scripts/run-select.js`, with every timestamp cast to `::text` and anchored against DB `now()`. **No handle, email or user id appears anywhere in this document, and none was selected by any query.** Where the data cannot distinguish a genuine installer from an accidental grant I have said so plainly rather than estimating, because an estimate would be used to take money from real people. No clawback of already-paid earnings is recommended. Nothing a live round holds was touched, including BL-709 on the submit path; this round worked in its own worktree at `C:/b710` on `checkpoint/BL-710` and changed no source file. A markdown-only diff cannot change tsc or the build, so **no build was run and none is claimed**. NO dashes used as bullets.
