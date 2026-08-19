# BL-814 — the owner could not send an APPROVED clip back to PENDING. It is a DEFECT, and the generic message is the reason it took a round to find

**2026-08-19 · DB `now()` = `2026-08-19 14:35:06.55123+00` (first read) to `2026-08-19 15:14:38.557324+00` (last) · BUILD AND MERGE.**
Base `origin/main` @ `89fda8a3`. Branch `checkpoint/BL-814` @ `5b122880`. **Merged to main and verified pushed: `origin/main == local == a57bfda6`.** Tags `pre-BL-814` (`89fda8a3`), `post-BL-814` (`5b122880`), `pre-BL-814-merge` and `post-BL-814-merge` (`a57bfda6`), all on origin. Isolated worktree `C:/w814`, a short path, `node_modules` never junctioned, **removed at the end**. Every read through `scripts/run-select.js`, every timestamp cast `::text` against DB `now()`. Handles redacted, no wallet address printed.

**A REDEPLOY ON RAILWAY IS REQUIRED BEFORE ANY OF THIS IS LIVE.**

> **FIRST LINE, because that is where an already-withdrawn case had to go: THE AFFECTED CLIPPER HAS NEVER BEEN PAID. Their only payout request was REJECTED, `paidAt` NULL, `actualPaidAmount` NULL. Un-approving their clip creates no debt and pushes nobody below money already received.**
>
> **THE VERDICT: A DEFECT.** Not a deliberate guard, not a permission problem. The APPROVED to PENDING transaction was blowing Prisma's **DEFAULT 5000 ms** interactive-transaction budget, because the route passed no options at all. Everything rolled back correctly. The only thing that was wrong was that the owner was told six words about it.

---

## PART 0 — THE REAL ERROR, FOUND IN PRODUCTION BEFORE ANYTHING WAS TOUCHED

### The evidence, from `audit_logs`, not from reading code

Two `BUDGET_PROBE_BYPASS` rows written by the OWNER earlier the same day:

```
targetId                    createdAt                      details
cmsvigwdr0am90xqwvst66zi6   2026-08-19 14:23:27.577        {"campaignId":null,"reason":"review:undo",
                                                            "errorMessage":"\nInvalid `prisma.clip.findUnique()` invocation:\n\n\n
                                                            Transaction API error: A query cannot be executed on an expired
                                                            transaction. The timeout for this transaction was 5000 ms, however
                                                            5329 ms passed since the start of the transaction."}
cmsyn3hrt0iwr0xo1mu7mpylv   2026-08-19 14:26:45.587        same shape, elapsed 7830 ms
```

**`reason: "review:undo"` appears in exactly ONE place in the whole codebase**, `src/app/api/clips/[id]/review/route.ts` at the OWNER/ADMIN `PENDING` branch, in the call `writeClipEarningsZero(tx, id, "review:undo")`. So the attribution is exact rather than inferred.

### file:line, the whole chain

| # | file:line | what it does |
|---|---|---|
| 1 | `admin/clips/page.tsx:2124` | the **Undo** button on an APPROVED row, `handleReview(clip.id, "PENDING")` |
| 2 | `admin/clips/page.tsx:896` | `fetch("/api/clips/<id>/review", { action: "PENDING" })` |
| 3 | `clips/[id]/review/route.ts:1176` | the `REJECTED || PENDING` branch |
| 4 | `clips/[id]/review/route.ts:1232` | **`await db.$transaction(async (tx) => { ... })` with NO options**, so it inherits `{ maxWait: 2000, timeout: 5000 }` |
| 5 | `clip-earnings-writer.ts:167` | the L1 budget probe `tx.clip.findUnique`, the statement that reported the expiry |
| 6 | `clips/[id]/review/route.ts:1564` | `return NextResponse.json({ error: "Failed to update clip" }, { status: 500 })` |

### Why it looked like "every clip" when it was intermittent

The same owner **succeeded** twice, minutes earlier, and reassigned both clips:

```
14:20:56.677  PENDING_CLIP              cmsx7yjuf...  APPROVED -> PENDING   OK
14:21:17.918  CLIP_CAMPAIGN_REASSIGNED  cmsx7yjuf...  Zhus Edit -> Zhus Meme
14:21:37.735  PENDING_CLIP              cmsy5jz8j...  APPROVED -> PENDING   OK
14:21:46.796  CLIP_CAMPAIGN_REASSIGNED  cmsy5jz8j...  Zhus Edit -> Zhus Meme
14:23:27.577  BUDGET_PROBE_BYPASS       cmsvigwdr...  FAILED, 5329 ms
14:26:45.577  BUDGET_PROBE_BYPASS       cmsyn3hrt...  FAILED, 7830 ms
```

**The transaction is not slow.** `scripts/bl814-repro.ts` runs the EXACT body against the real production row and then throws a sentinel so the whole thing rolls back:

```
PING    SELECT 1 x5 = 35, 34, 33, 34, 34 ms  (median 34 ms)

STATEMENT TIMING inside the transaction
  t+   35 ms      0 ms  BEGIN (tx callback entered)
  t+   35 ms     61 ms  tx.clip.update (status)
  t+  134 ms    335 ms  writeClipEarningsZero (2 probes + 1 update)
  t+  469 ms     37 ms  tx.agencyEarning.deleteMany
  t+  506 ms     35 ms  tx.marketplaceCreatorEarning.deleteMany
  t+  541 ms     34 ms  tx.marketplacePlatformEarning.deleteMany
  TOTAL  611 ms   (Prisma interactive-transaction default budget: 5000 ms)

OUTCOME  ROLLED BACK by sentinel
UNCHANGED: the clip is byte-identical before and after.
```

**611 ms across nine round trips.** 5000 ms is an 8x margin, and the platform crosses it whenever the Node process is busy. At `14:23` and `14:26` it was: the `:00` tracking tick runs for the better part of an hour after each hour boundary (BL-736 measured 154 clips written between `14:00:14` and `15:13:23`), and both owners were reviewing clips at a rate of one every few seconds throughout.

### Reproduced END TO END through the owner's own path

Not inferred. `scripts/bl814-repro-http.ts` holds `SELECT ... FOR UPDATE` on the clip row from a second connection (and ROLLBACKs, writing nothing), then fires the identical request the Undo button fires:

```
REQUEST POST /api/clips/cmsyn3hrt0iwr0xo1mu7mpylv/review  {"action":"PENDING"}   as OWNER
STATUS  500 Internal Server Error
BODY    {"error":"Failed to update clip"}
ELAPSED 7107 ms
UNCHANGED: the clip is identical before and after.
```

server log, verbatim:

```
Invalid `prisma.clip.findUnique()` invocation:
Transaction API error: A query cannot be executed on an expired transaction. The timeout for this transaction
was 5000 ms, however 6270 ms passed since the start of the transaction.
[F-MARKETPLACE-BUDGET-FAIRNESS] gate query failed for clipId=cmsyn3hrt0iwr0xo1mu7mpylv — passing through.
Clip review failed:
Invalid `prisma.clip.update()` invocation:
Transaction API error: ... however 6284 ms passed since the start of the transaction.
 POST /api/clips/cmsyn3hrt0iwr0xo1mu7mpylv/review 500 in 7.1s
[BUDGET_PROBE_BYPASS-ALERT] notification ... owner=cmn7d5hrv0001xow71dn372ri
```

**That is the production shape exactly**, down to the `BUDGET_PROBE_BYPASS` row and the owner alert.

### One false start, reported because it changes what the evidence means

My **first** route-level attempt held the lock for 9 s and returned **200**. That was not the fix working; `next dev` compiles a route lazily and the log shows `next.js: 5.7s` of compilation, so the lock had expired before the transaction began. The route was warmed and the test rerun. **A reproduction that has not eliminated compile time is not a reproduction.**

`scripts/bl814-itx-timeout.ts` isolates the mechanism with nothing but `pg_sleep`:

```
PROBE A  default options (what the review route used)   THREW after 6497 ms   code=P2028
         Transaction API error: A query cannot be executed on an expired transaction.
         The timeout for this transaction was 5000 ms, however 6384 ms passed ...
PROBE B  { maxWait: 10000, timeout: 20000 }             SURVIVED after 6145 ms
```

### Which of the four it is

* **A DEFECT.** A legitimate, permitted transition fails under ordinary production load because the transaction budget was never set, and the failure is then reported in words that name nothing.
* **NOT a deliberate guard.** Nothing in the codebase forbids un-approving a clip that has earned. The clip-side rule that refuses earnings is on the **reassignment** feature, not on the status transition, and 453 `PENDING_CLIP` audit rows exist historically, 41 in the last ten days.
* **NOT a permission problem.** The OWNER passes `requireRole(["ADMIN","OWNER","REVIEWER"])` and reached the transaction every time.

---

## PART 1 — THE MONEY QUESTION

**Nobody has withdrawn a cent of this.** Redacted to the forms earlier rounds used, `md6 = 733335`, `id8 = cmst7ibi`:

| | |
|---|---|
| role / test account | CLIPPER / `isTestUser` false |
| joined | `2026-08-14 17:14:06.653` |
| payout requests, all time | **1** |
| that request | `$20.97` gross, `$18.24` net, status **REJECTED**, `paidAt` **NULL**, `actualPaidAmount` **NULL** |
| **money ever received** | **$0.00** |
| approved earnings, Zhus Edit | $36.49 across 42 clips |
| approved earnings, Zhus Meme | $8.30 across 21 clips |
| `db_now` | `2026-08-19 14:40:06.829238+00` |

### Exactly what returning an APPROVED clip to PENDING does

Read out of `clips/[id]/review/route.ts:1232-1259`, and observed on the real transition:

| | |
|---|---|
| `earnings`, `baseEarnings`, `bonusAmount`, `bonusPercent` | **zeroed**, through `writeClipEarningsZero`, never a direct update |
| `AgencyEarning` for that clip | **DELETED** inside the same transaction |
| `MarketplaceCreatorEarning`, `MarketplacePlatformEarning` | **DELETED**, same transaction |
| the clipper's balance | **drops by that clip's gross**, because `computeBalance` sums APPROVED clips |
| `TrackingJob` | reactivated, `checkIntervalMin` reset to 60 |
| the clipper | gets an SSE `clip_updated` and `earnings_updated`, and **no notification and no email** |

Observed, before and after, on the one clip this round moved:

```
BEFORE  status APPROVED  earnings 1.87  base 1.85  bonus 0.02  bonusPercent 1
AFTER   status PENDING   earnings 0     base 0     bonus 0     bonusPercent 0
        agency_earnings rows for this clip: 1 before, 0 after
```

### Could it push anyone below money already paid?

**Structurally yes, and here no.** The write is a deliberate zeroing, so **BL-538's never-decrease guard does not block it and must not**: `capButNeverBelowStored` is reached only inside the BL-167 clamp, which sits inside `if (delta > 0)` at `clip-earnings-writer.ts:198`, and a zero write has a negative delta. That is correct design, not a hole. It means the owner, not the code, is responsible for not un-approving a clip whose money has already gone out. **On this clipper that question does not arise, because nothing has gone out.**

Platform-wide the overpayment case is already tolerated rather than created here: BL-627's clamp holds and **0 clippers have a negative available balance**. This round's single change removed **$1.87** of approved earnings from a clipper whose lifetime paid figure is **$0.00**, so it moved nothing across that line.

---

## PART 2 — THE FIX

### Half one: the transaction gets the budget it needs

`src/lib/route-failure.ts`

```ts
export const CLIP_WRITE_TX = { maxWait: 5_000, timeout: 15_000 } as const;
```

15000 ms is a **24x** margin on the measured 611 ms body and still fits inside the route's own `maxDuration = 30` together with a 5000 ms wait for a connection. `admin/payouts/[id]/adjust` reached the same conclusion independently at BL-212 and set 60000 ms with a P2028 retry.

Applied to the **five** transactions in the review route that passed nothing, and to the reassignment transaction, which is longer still: a row lock, both CPM restamps, a `CampaignAccount` upsert, four repoints, an audit row and a notification.

```diff
-        });
+        }, CLIP_WRITE_TX);      x5 in clips/[id]/review/route.ts  (:270, :1041, :1230, :1253, :1475)
+        }, CLIP_WRITE_TX);      x1 in admin/clips/[id]/reassign-campaign/route.ts
```

**The approval transaction was deliberately NOT touched.** It already carries `{ isolationLevel: "Serializable" }` and its own P2034 retry loop, it is a money path, and it is not what PART 0 named. The patch script refuses any call site that already passes options, so this cannot happen by accident.

### Half two: the message names the reason

```diff
   } catch (e: any) {
-    console.error("Clip review failed:", e?.message);
-    return NextResponse.json({ error: "Failed to update clip" }, { status: 500 });
+    console.error(`Clip review failed: action=${action} clipId=${id} code=${e?.code ?? "<none>"}:`, e?.message);
+    return writeFailureResponse(e, "this clip");
   }
```

Ten named classes, every one quoted here as the reader gets it, from `scripts/bl814-messages.ts`:

| code | status | what the owner reads |
|---|---|---|
| `DB_TRANSACTION_TIMEOUT` | 503 | *Nothing was saved. This clip is exactly as it was. The server ran out of time. It is usually just busy, so try again.* |
| `DB_WRITE_CONFLICT` | 409 | *Nothing was saved. This clip is exactly as it was. Someone else saved it at the same moment. Wait a moment, then try again.* |
| `RECORD_GONE` | 404 | *Nothing was saved. This clip no longer exists. Refresh the page to see the current list.* |
| `DUPLICATE_ROW` | 409 | *Nothing was saved. A record like this already exists. Refresh the page before trying again.* |
| `MISSING_RELATION` | 409 | *Nothing was saved. Something this points at does not exist. Refresh the page before trying again.* |
| `DB_UNAVAILABLE` | 503 | *Nothing was saved. The server could not be reached in time. Try again in a moment.* |
| `CAMPAIGN_OVER_BUDGET` | 409 | *Nothing was saved. This campaign has spent its budget. Raise the campaign budget first, then try again.* |
| `MARKETPLACE_CAP_REACHED` | 409 | *Nothing was saved. This listing has hit one of its caps. Check the listing budget and caps.* |
| `EARNINGS_INVARIANT` | 409 | *Nothing was saved. This clip is exactly as it was. Do not retry. The earnings numbers do not add up. Tell the owner.* |
| `UNEXPECTED` | 500 | *Nothing was saved. This clip is exactly as it was. Something unexpected went wrong. Try once more, then tell the owner. Reference `MFX9K0A2`.* |

**Every named refusal stopped being a 500.** BL-689 was opened because a legitimate refusal rendered as a server error; a 409 or a 503 says which kind of thing happened before a word is read.

### A SECURITY FINDING inside my own fix, caught before merge

My first draft echoed 200 characters of driver text. Two things make that wrong, and the accessibility review found both:

1. **F12 SEC-3** is written into **13 routes** and says raw error text must not reach a client. My sweep landed on several of them, so shipping the echo would have silently reversed an existing decision.
2. **The earnings guards embed money in their own throws.** `clip-earnings-writer.ts:221` and `:253` interpolate `$spent/$budget` for the campaign, plus `clipId` and `delta`. This helper is used by the clip review route, which a **REVIEWER** can reach, and CLAUDE.md forbids campaign economics to non-owner roles.

**No driver text reaches any reader now.** The unexplained case carries a short reference and the raw message is written to the server log against it.

**And a second, subtler bug in the same draft.** The guard branches used `startsWith`. A guard throw that crosses a Prisma boundary comes back **wrapped**: `"Invalid \`prisma.clip.update()\` invocation: ... [F-BUDGET-HARD-LOCK] ..."`. `startsWith` missed every one of those and dropped a fully explained deliberate refusal into the unexplained bucket, **taking the campaign budget figures with it**. Now matched with `includes`, and asserted:

```
PASS  a WRAPPED budget hard lock is still recognised
PASS  and its $spent/$budget never reaches a REVIEWER
PASS  a WRAPPED invariant refusal is still recognised
```

### BL-736's seven blocks were not weakened

Not one line of `campaign-reassign.ts` changed. The reassignment route gained one option object and one branch that maps a **driver** error rather than a domain refusal, because its own blocks already throw sentences and those are kept verbatim. Proven still refusing in PART 4.

---

## PART 3 — EVERY ADMIN ACTION THAT COULD FAIL WITHOUT SAYING WHY

Counted with an explicit loop in `scripts/bl814-generic-message-audit.py`, **never piped through `head`**.

| | before | after |
|---|---|---|
| generic failure messages in `src/app/api` | **74** | **33** |
| of those, **ADMIN or OWNER ACTIONS** (mutating handler, staff-only route) | **42** | **0** |
| of those, staff GET loaders | 19 | 19 |
| of those, clipper / community / public | 14 | 14 |

**All 42 admin actions are fixed.** Four in the clip surface where the defect lived (review catch-all, the approval branch, clip delete, and the reassignment route's driver mapping) and 38 in a sweep across 30 files, each with a subject chosen by hand rather than derived:

```
POST   accounts, admin/accounts, admin/campaign-admins, admin/clients x2, admin/owner-referral-links,
       admin/owner-referral-payments, admin/payouts/[id]/adjust, admin/payouts/unpaid/notify,
       admin/pending-edits x2, admin/referral-override x2, admin/teams x2, admin/users/[id],
       auth/magic-link, campaigns x7, client/clips comments + flag, community calls x3,
       community channels x3, community tickets, gamification, payouts/[id]/review
```

**Three of the 38 deliberately take no subject.** The magic link, the payout reminder and the campaign broadcast **send** something rather than change something, and "the magic link is exactly as it was" is nonsense about an email.

**Two had no catch binding at all** (`admin/teams/[id]:121` and `payouts/[id]/review:747` were bare `catch {`), so there was literally no error to describe. Both were given one.

**The 33 that remain are GET loaders** and they are honestly out of this round: they report a read that did not load, not an action that did not save, and the remedy for each is a different sentence. Listed by file:line in the committed audit script.

---

## PART 4 — THE OWNER'S ACTUAL GOAL, AND THE LOOP HE WAS IN

**The loop was real.** Proven read-only through the picker's own `GET /api/admin/clips/<id>/reassign-campaign`, which is the same rule set the POST enforces.

**The clip still APPROVED, `cmsvigwdr0am90xqwvst66zi6`, $2.51 on Zhus Edit:**

```
clipSideBlocks: CLIP_NOT_PENDING, CLIP_HAS_EARNINGS, CLIP_HAS_MONEY_ROWS
BLOCKED  all 14 destinations, every one carrying those three codes
  "Only a PENDING clip can be moved. This clip is APPROVED."
  "This clip has already earned money (earnings 2.51). Moving it would change what it earned on a campaign it was never on."
  "This clip already has earnings rows attached to its current campaign."
```

**The clip now PENDING, `cmsyn3hrt0iwr0xo1mu7mpylv`:**

```
clipSideBlocks: (none)
OFFERED  Zhus Meme (0.20 CPM)          cpm 0.2
OFFERED  SomeSome App                  cpm 0.5
BLOCKED  bees.n.honey  Gainzalgo  GainzAlgo (REPOST)  Grateful Songs  Hapday
         Panic Baby  somesome  STRAENGE  Zhus                              DEST_PAST
BLOCKED  BAD BITCH ANTHEM (0.50 CPM)                                       DEST_PAUSED
BLOCKED  BAD BITCH ANTHEM (2.50 CPM)              DEST_PAUSED + DEST_PLATFORM_NOT_ACCEPTED
BLOCKED  Grateful Songs                              DEST_PAST + DEST_PLATFORM_NOT_ACCEPTED
BLOCKED  Zhus Edit (0.50 CPM)                                              SAME_CAMPAIGN
archivedHiddenCount: 19
```

**So: he cannot reassign without PENDING, and reaching PENDING was the thing that kept failing.** That is exactly the loop the brief suspected, and it is now open.

### The safe route, end to end

1. **Redeploy on Railway.** Nothing below is live until then.
2. **Undo the clip to PENDING** on `/admin/clips`. It will now say what happened if it does not work.
3. **Reassign it to Zhus Meme (0.20 CPM)** through the campaign-name button, which appears only on a PENDING clip. The rate drops from `$0.50` to `$0.20`, so BL-736 sends the clipper the honest rate-drop notification. That is intended.
4. **Approve it.** The tracking tick re-derives the clipper side at the destination rate and recreates the owner accrual against the destination campaign, exactly as BL-743 verified on the one clip that had been through this before.

**On `cmsvigwdr0am90xqwvst66zi6` specifically:** step 2 will zero `$2.51` of clipper earnings and delete a `$1.60` `AgencyEarning` row, and after the move to a `$0.20` campaign it will re-earn at less than half its old rate. That is the point of the move and it is safe here only because this clipper has never been paid. **The clipper is told.**

### The one real clip this round changed, named, with its reversal

**`cmsyn3hrt0iwr0xo1mu7mpylv`**, moved **APPROVED to PENDING** by the reproduction request at `2026-08-19 14:44:36.103`: earnings `$1.87` to `$0`, base `$1.85` to `$0`, bonus `$0.02` to `$0`, its one `AgencyEarning` row deleted, tracking reactivated at 60 min.

**This was not planned and I am not dressing it up.** I expected a 500 and got a 200, because the lazy dev compile had eaten the lock window. It is safe (the clipper has never been paid) and it is the outcome the owner was trying to produce. **To reverse it: approve the clip.** It carries 26 `clip_stats` rows, so the next tracking tick re-derives both sides from real views rather than from anything I would have to hand-write.

**One cosmetic falsehood it left, and the correction.** The route stamps `reviewedById` with the acting session, and the dev-auth harness carries `dev-owner-001` (**"Dev Owner"**), which the owner's own reviewer-audit panel would have printed on a production clip. `scripts/migrations/BL-814-clear-repro-reviewer-stamp.sql` set that ONE non-money column to NULL, which is the truthful value for a clip awaiting review, and `rowCount=1`. **The audit trail was not touched:** the `PENDING_CLIP` rows still carry `dev-owner-001` as the actor with their timestamps.

**Found while checking, not caused by me:** **4 other clips** carry `reviewedById = 'dev-owner-001'`, all reviewed on **2026-06-02**, from a session months ago. Reported, not fixed.

---

## PART 5 — THE EVIDENCE

| claim | evidence |
|---|---|
| **the real error, reproduced through the owner's own path** | `POST /api/clips/<id>/review {"action":"PENDING"}` as OWNER, **500**, body `{"error":"Failed to update clip"}`, log `Transaction API error ... 6284 ms passed since the start of the transaction` |
| **the cause named and evidenced** | 2 production `BUDGET_PROBE_BYPASS` rows, `reason: "review:undo"`, 5329 ms and 7830 ms; that reason string exists at exactly one call site |
| **it is a DEFECT, not a guard or a permission** | 453 historical `PENDING_CLIP` rows, 2 of them succeeding 2 minutes before the failures; the earnings rule lives on reassignment, not on the transition |
| **the fix demonstrated on a real transition** | same request, same 7 s lock, **200 `{"success":true}`**; past the new 15 s budget it is **503** with the named reason and the clip identical before and after |
| **the message now states the reason** | 10 named classes, all quoted in PART 2; `scripts/bl814-messages.ts` **58 assertions, 0 failures** |
| **no raw driver text can leak** | asserted on every branch, including a WRAPPED `[F-BUDGET-HARD-LOCK]` carrying `$120.00/$100.00`, which is recognised and whose figures never reach the reader |
| **no clipper's earnings fell below money paid** | the affected clipper's lifetime paid is **$0.00**, one REJECTED request, `paidAt` NULL; BL-627's clamp re-verified, **0 negative available balances** |
| **no clip's earnings or status changed except the one named** | `cmsyn3hrt0iwr0xo1mu7mpylv` only. `cmsvigwdr0am90xqwvst66zi6` still APPROVED at `$2.51` with `updatedAt 2026-08-19 14:21:21.211`, before this round began |
| **no payout created, modified, approved or cancelled** | **180 rows**, Σ gross **$16,789.64**; `updatedAt` inside the round window: **0**; payout audit actions inside the window: **0** |
| **BL-736's seven blocks all still refuse** | `campaign-reassign.ts` not in the diff; live GET shows `CLIP_NOT_PENDING`, `CLIP_HAS_EARNINGS`, `CLIP_HAS_MONEY_ROWS`, `DEST_PAST`, `DEST_PAUSED`, `DEST_PLATFORM_NOT_ACCEPTED`, `SAME_CAMPAIGN` all refusing |
| **the earnings invariant** | **0 violations**, `db_now 2026-08-19 15:14:38.557324+00` |
| the 6 money files plus `tracking.ts`, `campaign-era.ts`, `payout-calc.ts` | **byte-identical by blob OID** on `89fda8a3` and on merged `a57bfda6`: `ac5be7de`, `797e2098`, `e887f80a`, `83ce4bab`, `61cef393`, `ef5cdae7`, `106e16ad`, `029834b4` |
| schema | **no change, no `prisma migrate`**; `prisma generate` only |
| Apify | **no actor run**; nothing in `apify.ts` or the BL-678 guards touched |

**Disclosed, because my own work wrote them.** The reproduction produced **3 `BUDGET_PROBE_BYPASS` audit rows** on `cmsyn3hrt0iwr0xo1mu7mpylv` (`14:47:19.51`, `14:54:36.919`, `15:01:04.641`) and refreshed the standing owner alert notification for both owners. Those are observability rows, not money, and they are the same rows the real failure writes. **2 `PENDING_CLIP` audit rows** were also written by the harness (`14:44:36.103`, `14:54:08.803`), the first of which is the real transition described above.

**Also disclosed:** both owners were working in production throughout this round, un-approving and rejecting clips at a rate of one every few seconds. Every clip that moved other than the one named above moved because they moved it or because the tracking cron did.

---

## THE ACCESSIBILITY REVIEW, WHICH CHANGED THE FIX

Run before the client was touched, with four specialists. **6 blocking items, all 6 implemented.** It also corrected the copy, which is the part worth saying out loud: my strings were **223 characters**, about 13 seconds of screen reader speech against a **7 second** toast, so the remedy sentence at the end could never have been reached by anyone.

1. **`setActing(null)` was not in a `finally`** (`admin/clips/page.tsx`). This round adds work to that `catch`; anything it threw would leave `acting` pinned on that clip id and **every button on that row disabled forever**. Now a `finally`.
2. **Focus fell to `<body>` on every review action.** `Button` natively disables while `loading`, so the control the owner pressed leaves the document mid-request, and on a failure he has no focus anywhere near the row that failed. The pressed element is now remembered and restored.
3. **The reject and approve modals stay open on failure and said nothing at all.** The reason now renders inside them, **persistently mounted** as `role="alert"` and swapped to `sr-only`, because a conditionally mounted alert is unreliable and a second identical failure has to announce again. Cleared before each attempt so a repeat is a change.
4. **`firstLine()` leaked owner-tier money into ADMIN and REVIEWER copy.** Covered in PART 2. This was the most serious finding of the round and it was in my own new code.
5. **The copy leads with the money state.** Every branch opens `Nothing was saved.` and every string is under **125 characters**, because the first clause is the only one guaranteed to be read and the one thing a person needs is whether their click did anything.
6. **Long error toasts came off the timer** (`src/lib/toast.ts`), and `closeButton` was added to the `<Toaster>`, because a **swipe was the only dismiss affordance** on the page (2.5.1 pointer gestures, 2.5.7 dragging movements). `theme="dark"` set at the same time; sonner defaults to `"light"`, which is harmless today and about 1.75:1 the moment anyone splits a toast into a title and a description.

**Where I overrode it, and why.** It cited 1.4.1 Use of Color on the error and success toasts being near-identical; the contrast specialist disagreed within the same review and I took that side, because colour is not the differentiator there, a glyph is, and the correct citation is **1.1.1** for a glyph with no accessible name. It is in the advisory list under the right number.

**Where it corrected an over-reach of mine, and I accepted.** It ruled that BL-518 and BL-521's ban on blame words should **not** extend here: their rationale is not accusing the person who earns the money, and nobody is accused when the server tells staff it refused a write. So `refused` stays.

**Reported, NOT fixed, each wanting its own round:** `Button` should use `aria-disabled` rather than native `disabled` (139 call sites in 63 files, and `use-dialog-focus-trap.ts:24` selects `button:not([disabled])`, so a loading button silently leaves every dialog's tab-stop list, which is the bug BL-556 diagnosed and routed around); `modal.tsx` still has no `role="dialog"`, `aria-modal`, focus trap or focus return; the toast type glyph has no accessible name (1.1.1); `confirm-destructive.tsx:217` and `:231` use `text-red-300`, 8.83:1 dark and **1.66:1 light**, the same defect BL-804 was opened for; `visibleToasts={4}` keeps toasts 5 and beyond in the DOM and announced at `opacity: 0`; and `page.tsx:2111`'s Flag button has no `loading` prop while the identical Flag at `:2125` does.

---

## MERGED AND PUSHED

| | |
|---|---|
| clean `tsc` baseline on the untouched worktree, **before any edit** | `npm ci` exit **0**, `npx prisma generate` exit **0** (before tsc, because `npm ci` wipes the generated client), `npx tsc --noEmit` exit **0**, `grep -c "error TS"` = **0** |
| branch | `checkpoint/BL-814` @ **`5b122880`**, verified pushed by `safe-push` |
| merge commit | **`a57bfda6`** |
| `origin/main` | **`a57bfda6`**, verified by `git ls-remote` |
| conflicts | **none**; main had not advanced from `89fda8a3`, and the **merged tree OID equals the branch tree OID exactly** (`82e34f8a...`) |
| BACKLOG sections | **157 before, 158 after**, `BL-814` x1, **0 conflict markers**, counted with `grep -c` and never piped to `head` |
| **`checkpoint/BL-723`** | **confirmed NOT an ancestor of main** |
| files | 48 changed, +1,241 / −61 |
| worktree `C:/w814` | **removed** |

> **A REDEPLOY ON RAILWAY IS REQUIRED.** Main carries the fix; production still returns "Failed to update clip".

---

## GATES, HONESTLY

* **`eslint` confirmed present**, `npx eslint --version` reports **v9.39.4**, so the hooks gate is a real check and not a silent no-op.
* `npx tsc --noEmit` exit **0**, 0 errors, run **five** times across the round. Two errors appeared mid-round and were **attributable to my own sweep, not to the baseline**: `owner-referral-links` and `payouts/[id]/adjust` stash their error in `lastErr` inside a retry loop, so the nearest enclosing `catch` binding was the wrong variable. Both fixed and `tsc` returned to 0.
* `npm run build` **twice**, both from a log with the exit code echoed by hand and **never piped through `tail`**: **`BUILD1_EXIT=0`** on the branch (`Compiled successfully in 28.6s`) and **`BUILD2_EXIT=0`** on the merged commit `a57bfda6` (`22.8s`). Prebuild clean both times: `check:prisma-bypass` **0 violations**, `check:removed-fields` **OK across 729 files**, hooks gate **11 problems (0 errors, 11 warnings)** at the ceiling of 11 with **zero added**.
* `scripts/bl814-messages.ts` **58 passed, 0 failed, exit 0**.
* Counted with `grep -c` and explicit loops, **never piped through `head`**. **No heredocs** were used to write any file.
* The first route-level reproduction returned 200 and is reported as a false start rather than quietly rerun.

---

## WHAT COULD NOT BE MEASURED, AND WHY

* **The exact thing that consumed the missing 5 seconds in production.** A DB row lock reproduces the same expiry, and both owners plus the `:00` tracking tick were saturating the process at both failure timestamps, so the mechanism is proven and the specific contended resource is not. It does not change the fix: any delay past the budget kills the transaction, and the budget was the thing that was never set.
* **Whether a real screen reader speaks the new copy as intended.** The DOM order, the `role="alert"` region, the persistent mounting and the character counts are all measured. NVDA, JAWS and VoiceOver were not run.
* **Nothing was verified against production over HTTP.** Every request ran locally against the merged tree with the dev-auth bypass, pointed at the production database. No authenticated request was made against clipershq.com and none is claimed.
* **The 33 remaining generic messages on GET loaders** were counted and listed but not rewritten.
