# BL-864 — a mark for the requests you have already sent your admin, and what BL-861's two controls actually do

**NOTHING IS UNREMOVABLE. 89 sandbox rows created, 89 deleted by primary key, 0 of 89 remain, verified twice and again by a direct `LIKE 'bl864sbx-%'` sweep returning 0, 0, 0, 0. No SQL is owed. NO REAL PAYOUT WAS TOUCHED.**

**2026-09-09 · DB `now()` = `2026-09-09 10:25:53` to `2026-09-09 10:49:46` · BUILD, PROVE, RENDER AND MERGE.**
Base `origin/main` @ `a527de2d`. Branch `checkpoint/BL-864` @ `66721d88`. **Merged and verified pushed: `origin/main == 2991bc87`.** Tags `pre-BL-864`, `post-BL-864`, `pre-BL-864-merge`, `post-BL-864-merge`. Worktree `C:/w864`, **removed and verified gone by listing the path**. `checkpoint/BL-723` confirmed **NOT** an ancestor of main.

**A REDEPLOY ON RAILWAY IS REQUIRED.** The marker is a new column, a new route and new UI. Until the deploy runs your screen is exactly as it was.

**Collision with BL-863, which was live throughout.** It held `C:/w863` with uncommitted edits to `payouts/[id]/review/route.ts`, `payout-calc.ts` and `trainer-relationship.ts`. This round edited **none of those three**, worked only in `C:/w864`, and never ran `prisma generate` or a build in the shared repo. The proof is in the data: of the 8 payout rows created during my window, **all 8 carry the `bl863sbx-` prefix and none carry mine**, so the two rounds' sandboxes never overlapped by a single row.

---

## PART 0 — I CHECKED WHETHER THIS ALREADY EXISTED, AND IT HALF DID

**A `ScheduledCall` row already exists per payout** (`api/calls/route.ts:268-273`), and the admin row **already renders its state** (`page.tsx:2328-2348`: "Waiting for clipper to pick time", "Call: …", "Call completed", "Clipper missed the call"). So the question was a real one.

**It cannot do this job, in four ways, each at a line number:**

| what booking a call does | why the marker must not |
| --- | --- |
| moves the payout REQUESTED to UNDER_REVIEW (`:276-280`) | you asked that the status stay REQUESTED and stay yellow |
| notifies the clipper in-app (`:302-310`) | the marker is your note to yourself |
| emails the clipper (`:318`) | same |
| refuses a second booking (`:260-265`) | the marker has to toggle, so a mistake costs one press |

**So it is genuinely new, and both can be true of one row:** a request can be sent to your admin and not yet have a call booked, or have a call booked and never have been screenshotted.

---

## PART 1 AND 2 — WHAT WAS BUILT, AND WHAT IT REFUSES TO DO

Two nullable columns, `sentToAdminAt` and `sentToAdminById`, added with `ADD COLUMN IF NOT EXISTS`. **No `prisma migrate`, no index, no enum change.** One owner-only route, `POST /api/admin/payouts/[id]/sent-to-admin`.

**The two states, in words, because colour carries nothing here.** All three text tokens are `#ffffff` and emerald against red measures 1.44:1.

* not yet sent: **`Needs screenshot`**, in full-strength text inside a bordered pill
* already sent: **`Screenshot sent`**, quiet and borderless, with the exact moment printed beneath it as visible text, e.g. `2026-09-09 10:44 UTC`

**The words are deliberately not "Sent to admin".** That, sitting two columns from a dollar figure, reads as the **money** having been sent. That confusion has cost real money on this platform four times (BL-760, BL-763, BL-812, BL-827). The column header says **Admin handoff**, which names whom it went to once instead of in every row.

**It has its own column, between Status and Actions.** Inside the Status cell it would have announced as "Status column, REQUESTED, Needs screenshot", asserting a second payout status on the one screen where status decides whether money moves.

**IT RECORDS, IT DOES NOT ACT. Each proven by a direct request, not by reading the code:**

```
it changes no status        REQUESTED before, REQUESTED after
it books no call            scheduled_calls for that payout unchanged
it notifies nobody          the clipper's notification count unchanged
it moves no money           clip fingerprint IDENTICAL, available unchanged
the clipper cannot see it   neither column appears in their payload AT ALL
it writes an audit row      PAYOUT_SENT_TO_ADMIN = 1
a clipper cannot press it   403
```

The clipper check asserts the **key is absent**, not merely null, because a null still tells them the concept exists. Both of that route's query paths run every row through one strip function, so it cannot be added to one and forgotten on the other.

**One press each way**, and pressing an already-marked row is a success that writes nothing, so nothing is double-recorded.

---

## PART 3 — YOUR TWO NEW CONTROLS, IN PLAIN WORDS, CHECKED AGAINST THE CODE

### Close with no payment

**What it does.** It ends the request. Nothing is ever sent for it, and the clipper cannot open another request on that campaign.

**What it does to their money. THE MONEY DOES NOT COME BACK TO THEM.** Measured: their available balance was $60.00 before closing and $60.00 after. The full amount they asked for stays held against that closed request. **Their clip earnings are untouched** and nothing is deleted.

**What they see, and when.** Immediately: a card reading **Closed, not paid**, your reason in your own words, and a sentence saying the request still holds the money so it does not show in Available to withdraw. They also get a notification.

**Is it reversible.** Yes, completely. Reopen releases the claim in full and the request becomes ordinary again. Proven: their clips were byte-identical across the whole close-and-reopen round trip, and you could act on the row again straight after.

**Can that clipper ever get that money, in any way?** **Not while it stays closed.** They are refused if they request again, and every route that could move the row refuses it. **The only way is you pressing Reopen.** Nothing is destroyed, so the answer is not "never", it is "only if you decide so".

### Set amount

**What it does.** It writes the figure you intend to pay on the payout row. **Nothing is sent.** No clip is touched, no status moves, and nobody is notified.

**Does the difference return to their balance immediately? YES, AND THIS IS THE ONE TO KNOW.** Measured: a $100 request priced to $40 moved their available from $20.00 to $80.00 **the moment it was set**, before anything was paid.

**When does the clipper see the figure? IMMEDIATELY, not only when final.** Their card reads the reduced figure, says the owner set it, and says outright that nothing has been sent yet. That is deliberate: their balance has already moved, so hiding it would leave two numbers on one screen contradicting each other.

**Can you change it.** As many times as you like until you mark it paid. Proven $40, then $25, then $70, all accepted, with the clips byte-identical throughout. You can price it down but never above what they asked for.

### THE ORDER MATTERS, AND THE REPORT DID NOT SAY THIS

**Closing erases any amount you set, AND REOPENING DOES NOT BRING IT BACK.** Measured end to end: an $80 request priced to $20 freed $60; closing it cleared the price and took the **full $80** back into being held; reopening left the price **empty**, not $20.

**So: set an amount and pay it, OR close it. Never set an amount and then close expecting the amount to survive.** If you close by mistake after pricing, reopening is safe but you must type the amount again. **The Close dialog does not currently warn you about this.** Reported, not changed.

**Everything else BL-861's report says about these two controls was checked against the code and is accurate.** The one gap is the sentence above.

---

## PART 4 AND 5 — PROVEN, RENDERED, AND WHAT WENT WRONG

**44 sandbox checks, 44 passed, 0 failed**, every one a real HTTP request against a production build with the dev bypass off and real minted cookies.

**THE SANDBOX CAUGHT A DEFECT IN MY OWN ROUTE.** Two sessions pressing at once returned 200/**409**: the loser of the race was refused while the row already said what it had asked for. Fixed with the same retry the two BL-861 routes use, and re-proven at **200/200 with exactly one audit row**.

**AND A WORSE ONE IN MY OWN PROOF, WHICH IS THE MORE IMPORTANT OF THE TWO.** My balance helper omitted one column, so every clipper's available read **$0.00**. The close test asserts the balance is *unchanged*, and 0 to 0 is unchanged, **so it PASSED and would have been published as proof of a money claim it had never tested.** Fixed; every figure quoted above is from the corrected run.

**20 shots, 170 assertions, 0 failed, at 320, 375, 414, 1280 and 1440.** 0 at the wrong width, 0 with horizontal overflow. Marked and unmarked rows interleaved rather than grouped, because a grouped list flatters the design. Proven at every width: the flip keeps focus on the control, the status cell stays REQUESTED, one press puts it back, the filter leaves only unsent rows, and **no handoff wording reaches the clipper's screen**.

**Four render failures on the first pass were ALL harness bugs**, recorded rather than smoothed: `innerText` returns no table-header text on this page at all; the emoji and dash rules were unscoped and matched a **real** row's empty cell and a real note; and a name anchor failed *because* the accessible-name chaining works.

**THE SCANNING PROBLEM IS SOLVED BY A FILTER, NOT BY THE COLUMN.** The table is 900 pixels wide minimum, so on a phone the handoff column is off screen wherever it is put. A chip beside your existing filters reads **`Needs screenshot (7)`** and one press leaves only the ones you have missed.

**THE ACCESSIBILITY REVIEW RETURNED NO-SHIP BEFORE ANY UI WAS WRITTEN** and changed the design three times: the wording, the column placement, and the removal of a success message I had planned. **Two pre-existing defects it made blockers were fixed on the way:** the payouts table could not be scrolled sideways by keyboard **at all**, so columns nine and ten were already unreachable without a mouse; and the 15-second refresh re-sorts the rows, which dropped your focus out of a row **with you touching nothing**. Both now fixed, which protects every button already on that row.

**I MADE ONE SERIOUS MISTAKE.** A careless `git checkout main -- .` reverted four modified files mid-round. They were recovered **exactly** from the objects git had already written, verified symbol by symbol, and the restored tree was **rebuilt from scratch** to prove it is the tree that was tested.

**THE TEARDOWN CENSUS FELL BACK TO A THREE-DAY WINDOW** because I did not run its opening-snapshot step, so it attributed three days of real traffic to this round and reported two failures. Both are one fact. The 14 payouts it flagged carry **0** sandbox ids, and the 8 inside my actual window all belong to BL-863.

---

## GATES, HONESTLY

* Clean `tsc` baseline taken on the **untouched** worktree first: `npm ci` exit 0, `prisma generate` exit 0, `tsc --noEmit` exit **0**, `grep -c "error TS"` = **0**.
* `npm run build` run three times, each to a log with the exit code echoed by hand and **never piped through `tail`**: `BUILD1_EXIT=0`, `BUILD2_EXIT=0`, `BUILD3_EXIT=0` (the last on the restored tree).
* **eslint confirmed present**, `v9.39.4`, so the hooks gate is a real check. **10 problems, 0 errors, 10 warnings**, identical to the baseline and one below the 11 ceiling, with zero added.
* **The 6 money files plus `tracking.ts` and `campaign-era.ts`: byte-identical BY BLOB OID on BOTH refs.** `ac5be7de`, `797e2098`, `81a683c1`, `9563a4fc`, `61cef393`, `ef5cdae7`, `106e16ad`.
* Merged tree OID **equals** the branch tree OID (`f369ef5d`), so the branch's green build **is** the merge's build. No conflicts; main never moved from `a527de2d`. BACKLOG **196 to 197** sections, `BL-864` once, 0 conflict markers, counted with `grep -c` and never through `head`.
* BL-538, BL-627 and BL-696 all hold platform-wide: 0 violations of each, measured after the round.
* No heredocs in the shell. One shell at a time. No Apify actor run. Zero Supabase pool errors; the server was stopped **by PID on its own port**, never by image name.

## WHAT I DID NOT DO

* **The Close dialog still does not warn that closing erases a price you have set.** It is one sentence and it guards a real money mistake, but it is BL-861's copy and this round's scope was the marker. **Recommended as the next small change.**
* A real screen reader was not run; roles, names, focus behaviour and contrast are measured, NVDA and VoiceOver are not.
* Nothing was verified against production over HTTP. Every request ran locally against the merged tree, pointed at the production database.
* The mobile top bar can still cover a row reached by keyboard, which needs a one-line change to the shared layout and is reported rather than taken.
* `CopyableCell`'s copy button is 16 by 16 pixels and fails the minimum target size. Pre-existing, reported, untouched.
