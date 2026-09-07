# BL-852 — a clipper can enter a trainer code

**Nothing was left behind. 8 rows created, 8 deleted, 0 of 8 remaining, verified by a separate tool. No removal
SQL is needed and none is owed. No pairing was created between real users.**

**Merged to main `ee15936d`. Branch `checkpoint/BL-852` at `6b4f3936`. Requires a Railway REDEPLOY.**

---

## Two corrections before anything else, because both change what you should do next

**1. THE CODE ENTRY WAS NOT MISSING.** It was built, complete, and reachable by every clipper. `TrainerBlock`
was mounted unconditionally at `ReferralsRedesign.tsx:222`, on `/referrals`, which is in the clipper's main
sidebar at `sidebar.tsx:135`, with `referrals/page.tsx:183` hardcoding `const isTest = true` so nobody was
gated out. Look up, the consent panel, the tick, the join, the paired state and the ask-to-leave form all
worked. **So this round is a placement problem, not a build**, and the block moved unchanged rather than being
rebuilt. That is stated first because it is the difference between a day's work and an hour's.

**2. THE REAL REASON NOBODY HAS EVER JOINED A TRAINER IS THAT YOU HAVE PROMOTED ZERO TRAINERS.** Read off the
database today: **0 trainers, 0 pairings, 0 commissions, 0 refunds, 0 payouts carrying a cut.** A perfectly
placed code box has nothing to type into it. **The next step is yours: promote somebody at `/admin/trainers`,
which needs the typed phrase `NEW TRAINER` and a full `https` pitch link.** Until then this screen will
correctly tell every clipper that no code it is given exists.

---

## PART 1 — where it lives, and why that satisfies both halves of what you asked

A new page **`/account`**, titled **Account settings**, reached from **one new row in the account menu behind
your own name in the top right**.

- **Findable:** the menu is on every page, at every width. One press, then one press.
- **Not advertised:** **the word "trainer" appears nowhere in that menu.** Asserted on the rendered DOM at all
  five widths. Somebody who does not go looking never learns the arrangement exists.
- **On no daily surface:** the block is gone from `/referrals` entirely.
- **Old links still work:** trainer links handed out as `/referrals?trainer=CODE` are redirected to `/account`
  with the code preserved. Nothing in the codebase generates those URLs, so there was no list to rewrite.

**A trainer is still named in two places a clipper visits, and that is deliberate.** `/payouts` shows
`Trainer share (10%)` with a screen-reader "less" instead of a minus sign, **but only when a cut was actually
taken**, and the payout email carries the same line. `/help` has one conditional explanatory sentence. Neither
tells anyone how to join; both disclose a deduction from the clipper's own money, which is required.

**Reachable at every width including 320, and the phone menu now actually scrolls.** The accessibility review
found it did not: the menu is `absolute` inside a `max-lg:fixed` topbar, so no ancestor scrolls it, and the
bottom navigation pill paints above it. It now has a viewport-relative cap, its own scroller,
`overscroll-contain`, `data-no-swipe`, Escape with focus return, and a route-change reset. **That fix also
repairs Sign out, Change profile picture and the notification bell, which were already unreachable in that
state.**

---

## PART 2 — every refusal, and two that were saying the wrong thing

Every case was already enforced server-side. **48 checks, 48 passed, 0 failed**, by direct HTTP request against
a production build with real minted sessions and the dev-auth bypass off.

| What the clipper does | What the platform says |
| --- | --- |
| Types a code that does not exist | "We could not find a trainer with that code. Check the spelling and try again." |
| Types a code belonging to somebody who is not a trainer | the same, deliberately |
| Types a **revoked** trainer's kept code | the same, deliberately |
| Types a **banned** trainer's code | the same, deliberately |
| **A trainer** types their own code | "That is your own trainer code… Your own code is the one you give to people you train." |
| Already has a trainer | "You already have a trainer. Ask the owner to let you leave before you join someone else." 409, and exactly **one** live pairing survives |
| Types capitals, or leading or trailing spaces | **all five variants find the trainer** |
| Presses Join without ticking the box | refused **by the server**, and by an explicit `consent: false` too |

**The four identical answers are on purpose.** Telling a clipper "that person is not a trainer" would let
anyone test whether an account exists. The refusal is the same sentence and the same status line for all four.

**Two refusals named a problem and no remedy, and are rewritten.** "You cannot be your own trainer." and "That
person is not taking on new clippers right now." both now say what to do, measured at Flesch-Kincaid grade 1.6
and 3.6 against a ceiling of 6.0, longest sentences 12 and 11 words.

**And a third was a false statement about an innocent third party.** `join/route.ts` used **one string for two
different people**: a banned trainer, and **the reader's own banned account**. So a banned clipper was told
"that person is not taking on new clippers", which blamed somebody who had done nothing, and any remedy naming
them would have sent a banned clipper off to message them. Split into its own message whose remedy is real.

**A finding about your own screen, in passing:** the self-refusal is reachable by exactly one kind of person, a
trainer typing their own code. An ordinary clipper has no trainer code at all, so their own username is simply
an unknown code. My first test aimed at the wrong person and the platform was right.

---

## PART 3 — the consent screen, reused rather than rewritten

BL-835's copy, verbatim, from `src/lib/trainer-copy.ts`. **Every claim below is asserted on the rendered page
at all five widths, not in the copy file**, because a string that exists and never renders is not a disclosure.

> **Join [trainer name] as your trainer**
>
> [trainer name] will coach you to get more views and earn more.
> In return, your trainer takes 10% of your pay after fees.
>
> **What it costs you**
> Your trainer's 10% is worked out on your pay after fees.
> Take a $100 withdrawal. $9 comes off for fees.
> Your trainer then takes $9.10. You receive $81.90.
> The platform fee itself does not change.
> An express withdrawal costs extra. It does not change your trainer's 10%.
>
> **What it applies to**
> Only clips you post after you join.
> Clips you posted before today are never counted.
> Money you have already been paid is never touched.
>
> **Leaving**
> Leaving is not automatic. You ask the owner and the owner decides.
> Say why you want to leave and send anything that backs it up.
> Even if the owner lets you leave, you keep paying 10% on the clips you already posted.
> The owner can also end it. Then your 10% stops.
> You keep clipping the whole time you wait.
>
> **What your trainer will see**
> Your name and the day you joined.
> Every clip you post from now on, and whether it was approved or rejected.
> The reason for any rejection.
> They see a link to each clip. That link shows your account name.
> What they earned from you.
> They will not see your email or anything from before you joined.
>
> ☐ I understand that my trainer takes 10% of my pay after fees.
>
> [ Join ]  [ Cancel ]

**The worked example is in their own money and it branches on who is reading it.** A clipper somebody invited
pays a 4 percent fee, so their line reads "$4 comes off for fees… You receive $86.90". **That is a live path
for 190 real clippers**, not a hypothetical. The trainer's cut is $9.10 either way, so nobody is charged more
for how they arrived.

**The trainer's pitch document is shown** when they have set one, as a link whose accessible name warns that it
opens in a new tab.

**The confirmation is three deliberate acts, and a single tap cannot join.** Press Look up, read, tick the box,
press Join. Proven by pressing Join with the box unticked at all five widths: **the panel stays open, nothing
is written, and focus lands on the box that is blocking.**

---

## PART 4 — what a paired clipper can always see

On `/account`: their trainer's name, **the exact day they joined** as an absolute date rather than "3 months
ago", the 10 percent, the pitch document, what the trainer can see about them today, the ask-to-leave form, and
**new in this round, what the arrangement has cost them so far.**

**That figure was the one genuine gap, and it had eight possible meanings.** The accessibility review traced
"how much has gone to your trainer" onto **eight numerically different totals** in this schema, which diverge
in six real situations. **One figure ships:** the sum of commissions at Available, Pending or Paid, which is
**the same set your trainer's own dashboard sums**, so the two screens cannot disagree. A voided payout is
excluded, because the clipper was never paid and nothing came off them.

**One line was written and then deleted, and you should know why.** A draft also showed "refunded to you". **No
code in the product credits a refund**: `TrainerRefund.settledAt` is never written by any route, and your hub
correctly shows "Not sent yet". Telling a clipper money came back when nothing credits their balance would be a
false statement about money. **Settling a refund is still a manual act by you.**

**A lost figure is never shown as $0.00.** A true zero reads *"So far your trainer's 10% has cost you $0.00. We
checked, and nothing has come off your pay yet."* A failed read reads *"We could not work out this figure just
now. That is not the same as $0.00."*

**The route to raise a problem is one press**, on that same screen, reading "Report a problem with your
trainer". It opens your existing one-way report form.

---

## PART 5 — proven in the sandbox, and removed without trace

**48 checks, 48 passed, 0 failed.** Five sandbox accounts, one pairing created **through the real route** with
the code typed in capitals. **Nothing real was touched and no pairing between real users was created.**

**The money rule the screen describes is the rule the code runs**, asserted against the shipped functions with
every expectation worked out from your rule by hand first:

| case | platform fee | trainer takes | clipper receives |
| --- | --- | --- | --- |
| **your own $1,000 example** | $90.00 | **$91.00** | **$819.00** |
| $100, referred clipper | $4.00 | $9.10 | $86.90 |
| $100 plus express | $9.00 | $9.10 | $77.90 |
| $100, all earnings from before joining | $9.00 | **$0.00** | $91.00 |

A clip posted a minute before joining is not eligible; a minute after is; **exactly at the join moment is**,
which is the inclusive boundary.

**This round did not create a payout, and that is a limit rather than a claim.** BL-840 proved the split on
real payout rows and BL-843 proved the whole loop including your trainer's cashout, 61 checks. Your brief
forbids creating a payout, so the arithmetic here is proven on the shipped functions instead and nothing is
re-claimed.

**And it is gone.** 8 rows created, **8 deleted, 0 of 8 remaining**: 5 users, 1 pairing written by the product,
2 audit rows found by the sweep. **50 teardown checks, 50 passed.** Real payout fingerprint and real user
fingerprint **byte-identical**, invariant **0 violations** both sides, 0 trainer holders and 0 active pairings
before and after, `audit_logs` 27,415 to 27,415.

**What moved is named and none of it is mine:** 3 clips from 1 real clipper, 174 view snapshots from the
tracking cron, 7 agency earnings rows, and approved earnings up $13.44. That is live traffic during the window.

**The safeguard refused this round once and it was right.** A pairing's id is minted by the product, so it
cannot carry the sandbox prefix; the first run recorded a line the destroyer could not prove and **it refused
the entire ledger and deleted nothing.** Fixed by recording the column that holds a sandbox id.

---

## PART 6 — render, and the merge

**60 shots, 360 assertions, 0 failures** at 320, 375, 414, 1280 and 1440, with `window.innerWidth` printed
beside every shot: **0 at the wrong width, 0 with horizontal overflow.** The menu entry, `/referrals` with the
block gone, the code form, all six refusals, the consent screen, the unticked refusal, and the paired state.
Plus **65 more assertions** on the report bridge: the dialog opens, focus lands on its heading rather than the
page body, and Escape returns focus to the exact button pressed.

**Three of my own assertions were wrong and the platform was right. Recorded, not tuned away.** The
self-refusal was aimed at an ordinary clipper who has no trainer code. A pointer click on the deliberately
`aria-disabled` Join button failed Playwright's actionability checks at every width and became a keyboard
press, which is the path that design exists for. And the money assertion was written before the review supplied
the wording.

**Nothing I could not render:** every screen in this round was photographed at every width.

**The merge.** Main was at `2c108cd3` and had not moved, so there were no conflicts and no unions were needed.
**The merge tree OID equals the branch tree OID exactly at `2ea9b825`, so the branch's green build is the
merge's build.** 0 conflict markers. **BACKLOG 181 to 182**, counted with `grep -c`. `checkpoint/BL-723`
confirmed **not** an ancestor of main. Worktree `C:/w852` removed and verified gone.

**Build honesty.** eslint v9.39.4 confirmed present, so the hooks gate is a real check. Clean tsc baseline on
the untouched worktree before any edit: exit 0, 0 errors. **tsc exit 0 with 0 errors and `npm run build` exit 0
both pre-commit and post-commit**, each written to a log with the exit code echoed by hand. **Hooks gate: 0
errors, 10 warnings against a ceiling of 11, zero added.** One intermediate build failed, exit 1, on a comment
I put inside a template literal; it is reported rather than hidden.

**Collision.** BL-851 merged to main at `2c108cd3` **before** this round started and held no worktree, so there
was nothing to collide with.

---

## The riskiest thing here, and the gate that now guards it

The report form's state lives in the app layout, and a page reaches that layout as an opaque slot with **no
prop path**. So the button dispatches a typed window event. **That is exactly how `support-chat:open` died: it
sat in this codebase with no dispatcher for months and the support form was unreachable on a phone the whole
time, and neither TypeScript nor the build could see it.**

Two things stop that happening again. The dispatch **returns a receipt**, so the button can say "That did not
open. Ask on Discord instead." rather than doing nothing silently. And a new build gate,
`npm run check:event-wiring`, **refuses the build** when either half goes missing.

**The gate was seen to fail before it was trusted, and its first version did not.** Commenting the listener out
left the text sitting in the file and the gate happily counted it. **That is BL-835's own lesson, that a guard
which can be satisfied by prose is not a guard, reproduced in a brand new gate on its first run.** It now reads
code only. Both halves then failed on demand and both files are byte-identical afterwards.

---

## The accessibility review: 21 blocking items, 4 outright kills, every one implemented

It ran **before any UI was written**. It killed the unqualified money figure, the refund line, menu semantics on
the dropdown, and the fire-and-forget event. **It found two real defects in this round's own half-built code**:
the money block was unreachable from the response, and it counted a voided commission as money that came off a
clipper's pay. It settled the heading structure so a reviewed component moved pages without renumbering a
single level. And it resolved one genuine conflict **in your favour**: the textbook fix for a page in no
navigation list is a sidebar entry, which is exactly what you said to avoid, so there is none.

---

## Reported, not changed

- **A rejected payout permanently consumes a pairing's lifetime headroom.** The decrement sits in an
  unreachable branch, below an earlier arm that already matches a rejection. Money-adjacent, its own round.
- **`admin/trainers` sends a Decimal through a spread**, so it crosses the wire as a JSON string against a
  client that types it as a number. Owner-facing, pre-existing.
- **Below `lg` the account menu does not exist on `/campaigns/[id]`**, where the top bar is deliberately
  suppressed, so `/account` is unreachable there without typing the URL. This is the identical loss BL-809
  already recorded for the report row on that same route.

## Safety

No schema change, no `prisma migrate`, no index, **no Apify actor run**, the 11 BL-678 guards untouched, **0
Supabase pool errors**, every timestamp cast `::text` against the database's own `now()`. **The 6 money files
plus `tracking.ts`, `campaign-era.ts`, `payout-calc.ts`, `apify.ts` and `prisma/schema.prisma` are
byte-identical by blob OID on both refs.** `CONSENT_TERMS_VERSION` bumped to `BL-852-2026-09-07`, because its
own comment says to bump it whenever any consent string changes, and without that every consent record becomes
unfalsifiable. No handle printed, no wallet address read.

**Rollback:** `git revert -m 1 ee15936d`. Nothing to run in the SQL editor.
