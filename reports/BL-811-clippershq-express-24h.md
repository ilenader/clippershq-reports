# BL-811 — the express payout promise moves from 12 hours to 24 hours

**Branch** `checkpoint/BL-811` → merged to `main`. **Tags** `pre-BL-811`, `post-BL-811`.
**Requires a Railway REDEPLOY before it is live.**

**The finding that justifies the round:** all three express payout requests in flight right now
are ALREADY past their 12 hour deadline, by 2.0 hours, 3.6 days and 7.0 days. 12 was never a
promise the platform kept. Moving it to 24 is not a downgrade being hidden; it is the first
honest number.

---

## PART 0 — every occurrence, found and counted before anything changed

Counted with `grep -nFf <pattern-file>` over `git ls-files src prisma scripts public` with
`src/generated` excluded, **never piped to `head`**. Pattern file held five fixed strings:
`12h`, `12 hour`, `12 * 60 * 60 * 1000`, `+12h`, `43200000`.

**Haystack total: 46 lines across 17 files.** That splits three ways:

| bucket | lines | note |
|---|---|---|
| EXPRESS payout (the target) | **19** | listed below |
| unrelated domains | 22 | tracking intervals, marketplace timers, community mutes, growth triggers |
| **false positives** | **5** | `public/brands.html` SVG path data `M12 5v14M5 12h14` — a literal `12h14` |

The `brands.html` hits are exactly the trap this round was warned about: a naive count reports
24 "occurrences" in copy when 5 of them are plus-icon path geometry.

### The 19 express occurrences, split as asked

**Clipper-facing copy (5)**
- `src/components/payouts/PayoutRequestFlow.tsx:371` — polite live region after submit
- `src/components/payouts/PayoutRequestFlow.tsx:715` — the EXPRESS speed card's `timing` line
- `src/components/payouts/PayoutRequestFlow.tsx:801` — success step `role="status"` sentence
- `src/components/payouts/PayoutRequestFlow.tsx:816` — success summary line under the total
- `src/app/(app)/payouts/page.tsx:1009` — legacy modal EXPRESS card, "Within 12h". Unreachable
  (`useNewPayouts` is hardcoded `true` at :400) but kept for one-flip rollback, so a stale copy
  there is a lie a rollback revives. Changed anyway — that is BL-734's exact lesson.

**Admin-facing copy (0 visible)**
- `src/app/(app)/admin/payouts/page.tsx:1283` — code comment only. The rendered chip says
  "Express +4%" and carries no time; the SLA reaches the owner through `PayoutCountdown`, which
  reads the row's own `deadlineAt`. The comment was also factually stale and is corrected.
- `src/app/api/admin/command-center/route.ts:669` — code comment only.

**Email / notification text (5)** — all owner-facing, fan out to email via `sendOwnerAlert`
- `src/lib/payout-reminders.ts:152` OVERDUE body · `:159` EXPRESS_NEW title · `:160` EXPRESS_NEW
  body · `:167` EXPRESS_6H body · `:174` EXPRESS_3H body

**Computed deadline (1 real computation + 2 comments)**
- `src/app/api/payouts/route.ts:470` — `12 * 60 * 60 * 1000`. **The only arithmetic in the repo
  that produces an express deadline.** Comments at `:465` and `:815`.

**Test / fixture (1)**
- `scripts/test-bl-179-payout-reminders.ts:118` — asserted the title contains `"12h"`

**Doc comments (3)** — `src/lib/payout-sla.ts:12`, `prisma/schema.prisma:1253`, `:1281`

### Surfaces checked and found CLEAN
`/help` (both `help-redesigned.tsx` and the flagged-off `page.tsx`) mention payouts but never
express or any turnaround. No email template mentions it. `PayoutsRedesign.tsx` shows an
"Express" badge with no time. No admin tooltip carries it. Per BL-734's chat auto-reply lesson:
BL-804 deleted the chat entirely, and neither the archive nor any remaining template carries the
figure. `BACKLOG.md` holds 6 historical mentions in the BL-176/177/178/179 entries — those are an
append-only record of what was decided then and were deliberately **not** rewritten; a BL-811
entry was appended instead. `HANDOFF_FOR_NEW_CHAT.md` and `MARKETPLACE_SPEC.md` hits are tracking
and marketplace, not payouts.

---

## PART 1 — all 19 changed, and a single source of truth created

**A single source of truth WAS created, and it is the main deliverable of this round.**
`src/lib/payout-sla.ts` now holds:

```ts
export const EXPRESS_SLA_HOURS = 24;
export const EXPRESS_SLA_MS = EXPRESS_SLA_HOURS * HOUR_MS;
export const EXPRESS_SLA_LABEL_SHORT = `${EXPRESS_SLA_HOURS}h`;    // "24h"
export const EXPRESS_SLA_LABEL_LONG  = `${EXPRESS_SLA_HOURS} hours`; // "24 hours"
```

Every other site imports it: the deadline arithmetic, the four clipper sentences, the legacy
modal card, the five owner reminder strings and the test assertion. **`12` is no longer written
in any of them.** Why, plainly: BL-734 needed four rounds to stop miscounting the withdrawal
minimum precisely because the value was retyped in seven places. The next person to change this
figure edits one line, and the promise and the computation move together or not at all.

**Counts, same method, same pattern file.**

| | before | after |
|---|---|---|
| haystack lines (src, prisma, scripts, public) | 46 | 33 |
| **express-related** | **19** | **6** |
| unrelated domains | 22 | 22 |
| `brands.html` SVG false positives | 5 | 5 |

The 6 that remain are all prose about the change plus one guard, with **zero live values and zero
visible copy**:

```
prisma/schema.prisma:1253   // ... 24h SLA (BL-811 moved it from 12h; the 4% premium did NOT change)
prisma/schema.prisma:1284   // old 12h promise keep their stored deadline and are never recomputed.
scripts/test-bl-179-payout-reminders.ts:125   note("EXPRESS_NEW title has no stale 12h", !c.title.includes("12h"));
src/app/(app)/payouts/page.tsx:34   // ... must not carry a stale 12h if it is ever flipped back on
src/components/payouts/PayoutRequestFlow.tsx:57   // Only the TIME moved (12 hours to 24 hours) ...
src/lib/payout-sla.ts:15    // BL-811 — the express turnaround promise moved 12h → 24h.
```

The test one is deliberate: `test-bl-179` now asserts the constant is `24h`, that the title
contains it, **and that the title contains no `12h`**. A stale number cannot return silently.

Full diff: 11 files, +431 −21 (of which `scripts/bl811-render.ts` is +332 of new proof
harness). It is in the commit `80526143` on `main`.

---

## PART 2 — the computed side, which mattered more than the words

**Every computation, enumerated.** `deadlineAt` is written in exactly one place in the whole
repo. `grep -rn "deadlineAt:"` over `src` returns six hits: four are read-side `where`/`select`
clauses, one is a type declaration, and one is the write.

- **`src/app/api/payouts/route.ts:479`** (was `:470`) — `nowForDeadline.getTime() + (isExpress ?
  EXPRESS_SLA_MS : 5 * 24 * 60 * 60 * 1000)`. **What changing it does:** every EXPRESS payout
  requested from the next deploy onward is stamped `createdAt + 24h` instead of `createdAt + 12h`.
  Nothing else changes: the fee, the amount, the campaign budget and the approval path are
  untouched.
- **Not changed, and correct unchanged:** `URGENCY_THRESHOLDS.EXPRESS` (urgent at 6h left,
  critical at 1h) and the `EXPRESS_6H / 3H / 1H` reminder ladder. These are offsets measured
  BACKWARD from the deadline, not fractions of the SLA, so on a 24h window they still mean
  "6 hours before it is due". The command-center's `expressUrgentCount` ("<6h left OR overdue")
  is likewise still correct.

**Does any existing express request gain 12 hours? No.** `deadlineAt` is snapshotted onto the row
at create time and is never recomputed anywhere. Verified against the live DB: `max(deadlineAt)`
across all 47 express rows is still `2026-08-16 12:01:46.604`, the old 12h stamp.

### The three express requests in flight, cast to `::text` against DB `now()`

DB `now()` at query time: `2026-08-16 14:00:58.925632+00`

| payout id | status | createdAt (::text) | deadline BEFORE this round | deadline AFTER this round | hours overdue |
|---|---|---|---|---|---|
| `cmsv1ifo705wr0xqwn4r8c5to` | REQUESTED | 2026-08-16 00:01:46.711 | 2026-08-16 12:01:46.604 | **unchanged** | 1.99 |
| `cmsq04pf100lr0xqzz2dos2mi` | REQUESTED | 2026-08-12 11:24:15.661 | 2026-08-12 23:24:15.511 | **unchanged** | 86.61 |
| `cmsl8dbul026r0ps2jxx43mvt` | REQUESTED | 2026-08-09 03:16:04.029 | 2026-08-09 15:16:03.877 | **unchanged** | 166.75 |

All three were verifiably stamped at exactly +12h (`deadlineAt − createdAt = 12 hours`, asserted
in SQL). Had they been created under 24h they would have been due at `2026-08-17 00:01:46`,
`2026-08-13 11:24:15` and `2026-08-10 03:16:04` respectively — but they were not, and the round
does not pretend otherwise. **No row was written.**

---

## PART 3 — the fee did not move, proven

The express premium is 4% on top of the standard 9% (4% referred). BL-763 established it; BL-732
had never named it. **This round changed the TIME only.**

- `src/lib/payout-calc.ts` — **not in the diff at all.** The default `expressFeePercent` of 4 and
  `finalAmount = amount − feeAmount − expressFeeAmount` are byte-unchanged.
- `src/app/api/payouts/route.ts:423` — `{ isExpress: true, expressFeePercent: 4 }` is byte-unchanged.
- `PayoutRequestFlow.tsx:76` `EXPRESS_FEE_PERCENT_DISPLAY = 4` and `payouts/page.tsx:120`
  `EXPRESS_FEE_PERCENT = 4` — both byte-unchanged.

Live DB, before this round and after it, identical to the cent:

| metric | before | after |
|---|---|---|
| payout rows | 172 | 172 |
| express rows | 47 | 47 |
| Σ gross (`amount`) | 15714.34 | 15714.34 |
| Σ cash (`finalAmount`) | 13962.75 | 13962.75 |
| Σ express premium | 180.56 | 180.56 |
| distinct `expressFeePercent` | 1 (value 4) | 1 (value 4) |
| payouts with `updatedAt` in the last 3h | — | **0** |

Zero payouts were created, modified, approved or cancelled. The express premium is still exactly
4 on every one of the 47 express rows.

---

## PART 4 — what clippers see, quoted before and after

1. Speed card, the EXPRESS option's timing line
   **before:** `Arrives within 12 hours` → **after:** `Arrives within 24 hours`
2. Success screen, the `role="status"` sentence
   **before:** `Express payout requested. It arrives within 12 hours after approval.`
   **after:** `Express payout requested. It arrives within 24 hours after approval.`
3. Success screen, the summary line under the total
   **before:** `Express, within 12 hours` → **after:** `Express, within 24 hours`
4. The polite live region announced on submit
   **before:** `Payout requested. Express, arrives within 12 hours after approval.`
   **after:** `Payout requested. Express, arrives within 24 hours after approval.`
5. Legacy modal EXPRESS card (currently unreachable, kept for rollback)
   **before:** `Within 12h` → **after:** `Within 24h`

Nothing else on any clipper screen changed. The wording is plain, states the new time directly,
and does not soften or bury it. The standard option still reads "Arrives in 3 to 5 days".

### The promise already made to a real person

Three clippers have an express request open. Each of them was shown "within 12 hours" when they
requested it and each paid the 4% premium for it. **They were not silently moved to 24 hours** —
their stored deadlines are untouched and still show as overdue on the admin screen. So there is
no clipper who was told 12 and will now be given 24. What is true is worse and simpler: three
people were told 12, paid extra for it, and have been waiting 2 hours, 3.6 days and 7 days.

**What the owner should do:** pay these three now, before the redeploy. They are owed
$52.44, $8.70 and $17.98 net. Once they are paid, the new 24 hour promise starts clean and the
platform is no longer carrying a broken one. If any of them is queried, the honest line is that
the payout is late, not that the policy changed.

---

## PART 5 — evidence

**Render proof.** 320 / 375 / 414 / 1280 / 1440, each at a two-figure ($60.27) and a four-figure
($1,234.56) amount, using BL-793's method: a real Chromium with the CSS viewport set through
`browser.newContext({ viewport })`, `next dev --webpack`, and `window.innerWidth` read back and
asserted every time. **210 assertions, 0 failures.** 40 screenshots.

| width | timing line lines / last-line ratio ($60.27) | ($1,234.56) | clipped? |
|---|---|---|---|
| 320 | 2 / 0.64 | 3 / 0.61 | no (94/94) |
| 375 | 1 / 1.00 | 2 / 0.34 | no |
| 414 | 1 / 1.00 | 1 / 1.00 | no |
| 1280 | 1 / 1.00 | 1 / 1.00 | no |
| 1440 | 1 / 1.00 | 1 / 1.00 | no |

Measured, not eyeballed: the premium card is `overflow-hidden` and the money column is
`shrink-0`, so a clip there would be silent — `scrollWidth` was compared against `clientWidth` on
both the "Express" title and the timing line at every width. No sideways page scroll anywhere.
The EXPRESS radio's accessible name resolves to `Fastest Express Arrives within 24 hours Adds a
4% premium ($2.41) You receive $52.44`. The polite live region announced
`Payout requested. Express, arrives within 24 hours after approval.` at every width. No
`"12 hours"`, `"12h"` or `"within 12"` appears on any rendered screen.

Why a harness route rather than `/payouts`: the dev bypass clipper `dev-clipper-001` has 0
approved clips and $0 available, so step 1 of the real flow cannot validate without creating
earnings data, which this round forbids. The REAL `PayoutRequestFlow` component was mounted with
mock props and a stub submit, driven through the same `goToSpeed()` validation gate. **The
harness route is NOT committed** — a route rendering a payout flow with mock money has no
business shipping. Its full source is reproduced in the header of `scripts/bl811-render.ts` so
the proof is reproducible.

**Build honesty.** `eslint` confirmed present in `node_modules/.bin` before trusting the gate.
`npx prisma generate` run after `npm ci`. `npx tsc --noEmit` exit **0**, 0 errors. `npm run build`
run twice from a log with the exit code echoed directly, never piped through `tail`: **build 1
exit 0, build 2 (post-commit) exit 0**, hooks gate `11 problems (0 errors, 11 warnings)` both
times — the warning count is unchanged from baseline because this round adds no hooks. The
`bl811-render` route does not appear in either build's route table.

**Tests.** `scripts/test-bl-179-payout-reminders.ts` — 55 passed, 3 failed on the branch;
53 passed, 3 failed on `main`. The 3 failures are **identical on both refs** with identical
expected/got hashes: stale sha256 baselines for `clip-earnings-writer.ts`, `balance.ts` and
`tracking.ts` frozen into that script on 2026-06-15, which later legitimate rounds moved past.
Pre-existing, not caused by this round. The +2 are the new BL-811 assertions, all passing.

**Money-file safety, by blob OID via `git rev-parse <ref>:<path>` on BOTH refs:**

```
IDENTICAL src/lib/clip-earnings-writer.ts                ac5be7deb061768fec800aa89aae512a56a9e065
IDENTICAL src/lib/earnings-calc.ts                       797e20985ad57475ef321afcf3cb1ea7b0d6ab84
IDENTICAL src/lib/balance.ts                             e887f80acfc70fee438e719a32a60025eda22749
IDENTICAL src/lib/tracking.ts                            83ce4babfd39a6261114465639f2eac4e23bfceb
IDENTICAL src/lib/clip-earnings-invariant-middleware.ts  61cef39395363c31f0c902dd4c64e8c06b3e6449
IDENTICAL src/lib/money-decimal.ts                       ef5cdae757b9ad3c23380ee8b63e279f98d0b6ac
IDENTICAL src/lib/campaign-era.ts                        106e16ad75125c3b10b6949a2981d33614c69ab9
```

`tracking.ts` appears 0 times in the diff. No schema change, no `prisma migrate`, no Apify actor
run, the 11 BL-678 guards untouched. No wallet address printed, no handle printed.

**Earnings invariant: 0 violations**, before and after.

**One honest note on clip data.** `Σ clip.earnings` moved 12884.14 → 12892.61 (+8.47) during the
round, and 374 clips were written. That is the production tracking cron, not this round: the
writes cluster on the hour and ~11 minutes past (11:10, 12:01, 12:11, 13:11, 14:01), which is the
`:00` batch signature. This round wrote no clip and ran no cron. Approved-clip count is unchanged
at 4921.

---

## Reported, NOT changed — needs its own round

**The BL-179 reminder engine has never fired, at all.** `lastReminderTierSent` is NULL on all
three overdue express requests, and there are **zero `PAYOUT_REMINDER_*` notifications in the
database, ever**. The owner has received no overdue ping for any payout since BL-179 shipped on
2026-06-15. That is why three express payouts sat past deadline unnoticed, and it is a bigger
problem than the number this round changed. Changing it was out of scope; it wants its own round
with the cron path traced end to end.

**Pre-existing a11y defect** (found by the accessibility-lead while reviewing this change, not
worsened by it): in `PayoutRequestFlow.tsx` the `lockedReason` span sits INSIDE the `<label>`, so
when the Express option is locked by the Solana threshold, a 27 word refusal is folded into the
radio's accessible name and then repeated through `aria-describedby`. The chain radios get this
right; the speed radios do not.

**Accessibility review.** Run BEFORE any code was written. Two blocking items, both honoured:
(1) do NOT perform this as a find-and-replace of `12` in `PayoutRequestFlow.tsx`, which carries
load-bearing `12`s — `HANDLE = 48` is paired with `h-12 w-12` on the swipe handle, and rewriting
those would desync the drag-travel maths and break the payout confirm control. Only the four
literal phrases were touched. (2) Do not leave the internal SLA at 12 while the copy says 24 —
the computation was moved with the copy, which is what PART 2 required. Everything else passed:
accessible name, contrast, focus, target size, reflow at 320px, no dashes, no emojis,
lucide-only icons, CSS variables only.

**Rollback:** `git revert -m 1 <merge>` or `git reset --hard pre-BL-811`. Nothing in the database
needs undoing, because nothing in the database was touched.
