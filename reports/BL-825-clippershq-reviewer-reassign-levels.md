# BL-825 — two named levels for the campaign-change capability, and the second one actually reaches something

**2026-08-24 · DB `now()` = `2026-08-24 17:00:29.871+00` (first read) to `17:44:50.136+00` (last) · BUILD AND MERGE.**
Base `origin/main` @ `e5a1846a`. Branch `checkpoint/BL-825`. Isolated worktree `C:/w825`, a short path, `node_modules` never junctioned, **removed at the end**. Every read through `scripts/run-select.js`, every timestamp cast `::text` against DB `now()`. Handles redacted where they are not the subject; no wallet address read or printed.

**A REDEPLOY ON RAILWAY IS REQUIRED BEFORE ANY OF THIS IS LIVE.**

> ## THE ANSWER, FIRST
> **Level two exists, is off by default, and is granted per reviewer behind its own typed phrase `ANY CLIPPER`.** Level one is unchanged to the byte.
> **It went from 0 movable clips to 28.** Level one offers `jdb001` **1** clip today. Level two offers him **28**, which is every clip waiting for his decision.
> **It widens what he may MOVE and not one row of what he may SEE.** A clip outside his queue still answers the generic 404, byte-identical to the 404 for an id that does not exist, at level two exactly as at level one. Proven by request in PART 2.
> **Granted to him**, through the real route with the phrase typed, audited at `2026-08-24 17:40:19.706`. One press reverses it.
> **NO REAL CLIPPER'S CLIP WAS MOVED.** Every move was on a synthetic fixture that lived for 34 minutes and was removed.
> **I degraded production for about four minutes and it is disclosed in full at the end.**

---

## PART 0 — WHAT LEVEL TWO COVERS, DECIDED BEFORE IT WAS BUILT

**A reviewer's review QUEUE and his reassignment SCOPE are two different things, and this round did not merge them by accident.** It made the second equal the first, deliberately, and stopped there.

**Level two covers every clip ALREADY VISIBLE IN HIS REVIEW QUEUE.** Concretely, all five of these must hold, and they are the same five filters `/api/clips` builds his queue from, read through the same exported helpers rather than a paraphrase:

| clause | source of truth |
|---|---|
| not his own clip | the self-authored exclusion, `clips/route.ts:371` |
| inside his campaign-list scope | `isCampaignInReviewerScope`, read semantics, empty = unrestricted |
| after the BL-89 date cutoff | `isClipInReviewerScope`, the same resolver the review route uses |
| a status he may read | `REVIEWER_READABLE_STATUSES`, unless he holds `reviewerCanSeeDecided` |
| BL-802's invitee READ flag, if the owner set it | `isClipperInReviewerInviteeScope` |

**It is NOT every PENDING clip on the platform.** Measured today: 28 clips are in his queue; the platform holds many more he has never been able to see, and level two does not reveal one of them.

**THE NARROWER READING WAS TAKEN AND IT IS THE RIGHT ONE.** Widening visibility is a separate decision the owner has not asked for, and it is the decision with the privacy cost: BL-788 built the invitee read scope precisely so a partner does not see the whole platform. Level two changes what he may DO with what is already on his screen.

**BL-802's flag was NOT touched.** It is READ, exactly as BL-821 reads it, and never written. It is on for one partner deliberately. Where it is on, that reviewer's queue already contains nothing but his own invitees' clips, so **level two grants him nothing at all** until the owner unticks it, and the profile card now says so in its own block rather than letting the owner discover it.

**Destinations are unchanged at both levels.** Only the campaigns ticked in "Limit to campaigns", where EMPTY MEANS NONE. That inversion, which BL-815 flagged loudly, still stands and is still the owner's remaining money control.

---

## PART 1 — THE TWO CONTROLS

One block, headed **Move clips between campaigns**, now containing two named levels as siblings.

```
Level 1: clips from people they invited
  They can move a clip to a different campaign only if that clipper joined through their own invite link.
Level 2: any clip waiting for their decision
  They can move any clip already waiting for their decision, whoever invited the clipper,
  without seeing one clip more than they see today.
```

**AT A GLANCE, in one line above both**, exactly one of five states, read from the live capability set:

> **Level 1 and level 2 are both on.** Level 2 already covers everything level 1 covers, so this is the same reach as level 2 on its own. Turning level 1 off would not narrow it; turning level 2 off would.

That sentence exists because the accessibility review rejected the version I proposed. "Both levels are on." states a fact with no meaning, and a non-technical owner reads "both" as "more than either", then revokes level one to narrow the reviewer and narrows nothing.

**THE DELIBERATE CONFIRMATION: the typed phrase `ANY CLIPPER`**, in the same spirit as BL-788's `FULL AUTHORITY` and BL-815's `MOVE CLIPS`, and **sharing no token with either**. The review changed this too: my first choice was `MOVE ANY CLIP`, which is one inserted word from the phrase the owner has just typed on the control above it, whose natural plural fails, and whose first word is a live caret command in Dragon and Windows Voice Access.

**Taking either level away needs nothing at all**, because obstructing the safe direction is a defect rather than a safeguard, and each gate fires only on the TRANSITION to held, so re-saving an unrelated checkbox does not demand a phrase again.

**Level two is fully independent of level one.** Neither trigger is ever hidden or disabled by the other's state: unmounting the focused trigger as a side effect of granting the other would drop focus to the document body in silence. Supersession is expressed in words only, in each trigger's own description.

---

## PART 2 — THE SERVER GATE, PROVEN BY DIRECT REQUEST

Nothing below is inferred from reading code. BL-790 is why: six capability checkboxes were reachable, persisted, and granted nothing. BL-740 is the other reason: a block refusing 92 of 93 pairs was invisible to both code reading and a 69-check harness.

**The level was flipped between batches on ONE column of ONE row with no server restart, which is itself a proof:** the route states in its own header that it reads capabilities from the DATABASE on every request and never from the session token, and a flip biting immediately is that claim measured.

```
=== NEITHER LEVEL HELD ===
GET  his own invitee's clip        -> 403  "You have not been given permission to move clips between campaigns."
POST his own invitee's clip        -> 403  same
GET  a stranger's clip             -> 403  same

=== LEVEL ONE ===
/api/reviewer/move-scope           -> {"reassignEligibility":"HELD","moveLevel":1,
                                       "moveScope":{"pendingInQueue":27,"pendingMovable":1}}
GET  his invitee's clip            -> 200  the picker opens
GET  a stranger's clip in his queue-> 403  "Nothing was changed. You can move a clip to another campaign only
                                            for a clipper you invited, and this one was not invited by you."
POST a stranger's clip             -> 403  same sentence
GET  a clip he cannot see          -> 404  {"error":"Clip not found"}
GET  an id that does not exist     -> 404  {"error":"Clip not found"}     <- byte-identical
POST destination outside his set   -> 403  DEST_OUTSIDE_REVIEWER_SCOPE
POST THE MOVE                      -> 200  Zhus Edit 0.5 -> Zhus Meme 0.2

=== LEVEL TWO ===
/api/reviewer/move-scope           -> {"reassignEligibility":"HELD","moveLevel":2,
                                       "moveScope":{"pendingInQueue":27,"pendingMovable":27}}
GET  a stranger's clip in his queue-> 200  the picker opens
GET  a clip he cannot see          -> 404  {"error":"Clip not found"}     <- UNCHANGED at level two
GET  an id that does not exist     -> 404  {"error":"Clip not found"}     <- still byte-identical
POST a clip he cannot see          -> 404  {"error":"Clip not found"}
GET  HIS OWN clip                  -> 403  "Nothing was changed. You cannot move your own clip to another campaign."
POST HIS OWN clip                  -> 403  same sentence
POST destination outside his set   -> 403  DEST_OUTSIDE_REVIEWER_SCOPE
POST THE MOVE                      -> 200  Zhus Edit 0.5 -> Zhus Meme 0.2
```

**The two 404 lines at level two are the whole safety claim of the round.** Level two moved the boundary of what he may MOVE and left the boundary of what he may SEE exactly where BL-788 put it.

### The owner's side of the grant, also by direct request

```
capabilities include level two, no phrase                 -> 400
                          ... with "MOVE CLIPS"           -> 400   (level one's phrase)
                          ... with "FULL AUTHORITY"       -> 400   (BL-788's phrase)
                          ... right words, wrong field    -> 400
                          ... with "ANY CLIPPERS"         -> 400   (a near miss)
                          ... with "any clipper"          -> 400   (the server is exact; the CLIENT normalises)
                          ... with "ANY CLIPPER."         -> 400   (same reason)
both keys in one PATCH, only level two's phrase           -> 400   "type MOVE CLIPS to confirm"
both keys in one PATCH, only level one's phrase           -> 400   "type ANY CLIPPER to confirm"
both keys in one PATCH, BOTH phrases                      -> 200
revoke level two, no phrase                               -> 200
re-save an unrelated field while it is held               -> 200   (no phrase demanded again)
level two onto a role=CLIPPER account                     -> 400   BL-790's rule covers the new key
```

---

## PART 3 — THE SAME SEVEN BLOCKS, AND THE PROOF IS A BLOB OID

**`src/lib/campaign-reassign.ts` is BYTE-IDENTICAL to main: `3e513702` on `e5a1846a` and on this branch** — the same OID BL-815 and BL-821 recorded. There is no second reassignment path: both levels enter the same route, the same `evaluateDestination`, the same single `db.$transaction`, the same `SELECT ... FOR UPDATE` re-assert, and the same **CPM restamp inside that one `clip.update`**.

**The structural claim, stated precisely: the level decides WHICH CLIP is reachable and never which destination is allowed.** `evaluateDestination` is called with identical arguments at both levels and has no notion of a level at all.

**Eight codes SEEN refusing a LEVEL TWO request:**

```
409 SAME_CAMPAIGN                  "The clip is already on this campaign."
403 DEST_OUTSIDE_REVIEWER_SCOPE    also for an id that does not exist, byte-identical
409 CLIPPER_ACCOUNT_NOT_APPROVED   "This clipper's account is not approved, so it cannot be on any campaign."
409 DUPLICATE_URL_IN_DEST          seen beside the above in the picker
409 DEST_DAILY_LIMIT_REACHED       fixture limit of 0 on SomeSome App
409 CLIP_NOT_PENDING               "Only a PENDING clip can be moved. This clip is APPROVED."
409 CLIP_HAS_EARNINGS              "...has already earned money (earnings 0.42)."
409 CLIP_HAS_MONEY_ROWS            "...already has earnings rows attached to its current campaign."
```

**SEVEN CODES WERE NOT DEMONSTRATED AT LEVEL TWO AND ARE NOT CLAIMED.** `DEST_PAST`, `DEST_PAUSED`, `DEST_ARCHIVED`, `DEST_ERA_WOULD_FREEZE`, `DEST_OVER_BUDGET`, `DEST_NO_CPM_FOR_PLATFORM` and `DEST_PLATFORM_NOT_ACCEPTED` all need one of the three campaigns he is assigned to to be in that state, and all three are ACTIVE, unarchived and accept both platforms. Manufacturing any of them means editing a real live campaign's status, budget, era or rates, which this round did not do. They are asserted against the untouched rule set; BL-740 measured them firing and BL-821 saw five of them refuse at level one on the same build.

**The restamp, read out of the row after each move:**

```
BEFORE  Zhus Edit (0.50 CPM)   clipper 0.5000   owner 0.3197   PENDING   earnings 0
AFTER   Zhus Meme (0.20 CPM)   clipper 0.2000   owner 0.1279   PENDING   earnings 0
        campaign_accounts membership on the destination: 1 (created inside the same transaction)
```

Identical at both levels. **A reviewer still cannot move his own clip at either level**, proven by request above on a clip owned by his real account.

---

## PART 4 — WHAT THE OWNER SEES AFTERWARDS

**A level-two move writes its own action name**, so those moves are countable and visible without opening a JSON blob. BL-821 set the precedent when it split the two invitee violations apart for the same reason.

```
reviewer_audit_log
  CLIP_CAMPAIGN_REASSIGNED      bl825-invitee-clip   17:13:05.816+00
    reviewerMoveLevel 1   "Level one: clippers they invited"      clipperWasHisInvitee true
    Zhus Edit (0.50 CPM) -> Zhus Meme (0.20 CPM)   0.5 -> 0.2   owner 0.3197 -> 0.1279
  CLIP_CAMPAIGN_REASSIGNED_ANY  bl825-stranger-clip  17:13:15.732+00
    reviewerMoveLevel 2   "Level two: any clip waiting for their decision"   clipperWasHisInvitee false
    Zhus Edit (0.50 CPM) -> Zhus Meme (0.20 CPM)   0.5 -> 0.2   owner 0.3197 -> 0.1279
```

**`clipperWasHisInvitee` is the figure the owner actually needs**: it is the one fact separating a move level one could also have made from a move only level two allowed, and it cannot be recovered later because `referredById` can be changed afterwards by the referral-override tool.

**Where he sees them, in two places.** Under **"Recent reviewer activity"** on that reviewer's own profile page, where the action name itself now distinguishes the two. And in **`/admin/audit-log`**, where the `CLIP_CAMPAIGN_REASSIGNED` details gained `reviewerMoveLevel`, `reviewerMoveLevelLabel` and `clipperWasHisInvitee` beside the `actorRole` BL-815 added.

**Every refusal carries the level too**, so a refusal at level two is never mistaken for the level-one invitee rule:

```
CAPABILITY_DENIED_403         reviewerMoveLevel 0   x3
INVITEE_SCOPE_VIOLATION_403   reviewerMoveLevel 1   (a stranger's clip, at level one)
INVITEE_SCOPE_VIOLATION_404   reviewerMoveLevel 1 and 2   (a clip he cannot see, at BOTH levels)
INVITEE_SCOPE_VIOLATION_403   reviewerMoveLevel 2   (his own clip, at level two)
```

---

## PART 5 — WHAT THE CLIPPER SEES IS IDENTICAL EITHER WAY

Proven by moving one clip at each level and reading both rows out of `notifications`:

```
17:13:06.027  moved at LEVEL ONE   "Your clip moved to a lower paying campaign"
17:13:15.885  moved at LEVEL TWO   "Your clip moved to a lower paying campaign"
  BOTH: "We moved your clip to Zhus Meme (0.20 CPM). Zhus Meme (0.20 CPM) pays $0.20 per 1,000 views
         instead of $0.50, so this clip will earn less than the campaign it was submitted to.
         Nothing you did caused this and the clip is still under review."
```

**Byte-identical title and body.** The notification names no actor and never has, and **BL-756's pay-cut warning fires at both levels**, leading with the rate, which is the branch BL-736 found a null CPM stamp silently suppressing.

---

## PART 6 — THE REVIEWER'S OWN SCREEN, AND THE RENDER PASS

His sentence had to change, because at level two the one BL-821 shipped is **false**. Read off his real screen, as him:

> You can move any clip waiting for your decision to another campaign, whoever invited the clipper. **All 28 of the clips waiting for your decision can be moved.** On those, the campaign name is a button.

Against BL-821's finding, and against the brief's figure: the brief cites **71** queued clips from BL-821's window. Measured today at `17:00:58`, his queue holds **15**; by `17:13` the route counted **27** and by the render **28**, because the owner was approving and clippers were posting throughout. The queue is a moving number and every figure here carries its clock.

**The picker, opened on a REAL clipper's clip that only level two makes reachable** (handle redacted, **no move was made** — a radio was selected and the dialog closed):

```
CLIPPER <redacted>  ACCOUNT <redacted> (Instagram)  CURRENTLY ON Zhus Edit (0.50 CPM)
CURRENT CLIPPER RATE $0.50 per 1,000 views      CURRENT OWNER RATE Not shown to you
Move to (2 available)   SomeSome App $0.50      Zhus Meme (0.20 CPM) $0.20
Archived campaigns are not shown. 11 campaigns are not shown because you are not assigned to them.
... Current owner rate Not shown to you   New owner rate Not shown to you
"The owner's rate is not shown to reviewers. It is not zero, and it is not missing."
"This takes effect straight away. Unlike approving or rejecting, it does not wait for the owner to agree."
"The clipper is told about this move either way."
```

**The owner rate stays withheld at level two**, exactly as at level one.

### Rendered, with the viewport MEASURED

Two servers, for BL-821's reason: `app-layout.tsx:314` makes a real Auth.js session invisible while `DEV_AUTH_BYPASS` is on, and a dev-bypass session carries `reviewerCapabilities: []` so a capability-gated surface can never render under it.

```
owner-two-levels / owner-level-two-trigger / owner-level-two-panel   320 375 414 1280 1440   15 shots
reviewer-level-two-note / trigger / picker / confirm                 320 375 414 1280 1440   20 shots
ALL 35 SHOTS AT THE ASKED WIDTH (measured == asked, every one).
```

The PNGs are deliberately not committed; the harness that regenerates them is. One copy defect was found by reading the captured text at 1440 and fixed: a missing space produced "the 29 peoplethey invited".

---

## GRANTED TO HIM, AND HOW TO REVERSE IT

**Granted through the real route with the phrase typed**, not by SQL: `PATCH /api/admin/users/[id]/reviewer-config` → **200**, audited `REVIEWER_CONFIG_UPDATED` at `2026-08-24 17:40:19.706`.

```
before  reviewerCapabilities ["ANALYTICS_VIEW","CLIP_REASSIGN_CAMPAIGN"]
after   reviewerCapabilities ["ANALYTICS_VIEW","CLIP_REASSIGN_CAMPAIGN","CLIP_REASSIGN_CAMPAIGN_ANY"]
```

Nothing else about him changed: role REVIEWER, mode LIVE, the same three ticked campaigns, `reviewerScopeInvitedOnly` false, `reviewerCanSeeDecided` true, ACTIVE, all as they were at `17:00:29`.

**To reverse:** press *"Whole review queue: stop this reviewer moving any clip"* on his profile, which needs no phrase. Or run the one line in the BACKLOG entry. Level one is unaffected either way.

**What his screen now offers:** 1 clip at level one, **28** at level two.

---

## THE ACCESSIBILITY REVIEW, RUN BEFORE ANY UI WAS WRITTEN

The lead and five specialists reviewed the DESIGN. **Twelve blocking items, every one implemented.** The ones that changed the work:

**The card would have lied to a level-two-only owner.** My design read one capability key, so a reviewer holding only level two would have been described as unable to move any clip, on the paragraph that is the trigger's `aria-describedby` and is re-spoken on every focus return. The card now derives the level exactly as the server does.

**Three panel booleans became one union, and the focus effect keys on panel identity.** Two panels open in one commit means two open-focus effects in one commit and the later-declared one wins, so the owner lands in a money panel he did not open. Worse, any boolean dependency is `true` before and after a level-one to level-two switch, so it does not re-run at all, and React has by then unmounted the panel holding focus, dropping it to the document body in silence.

**Both revokes announced nothing.** A revoke relabels the button under stationary focus, and no screen reader re-announces a changed name on the node it already sits on. Each revoke now carries a sentence naming the level and what remains, through the existing toast region rather than a second live region, and it REPLACES the generic "Saved" rather than adding a fifth utterance.

**Escape was dead on every trigger.** The handlers sat on the panel divs, so Escape worked only from inside a panel; with three panels that was three dead spots. One handler now sits on the card and calls `stopPropagation` **only when a panel was actually open**, because swallowing Escape unconditionally would leave the global mobile drawer undismissable by keyboard.

**The button names would have collided.** "Level 1:" and "Level 2:" diverge at character seven, and both the NVDA element list and the JAWS button list filter by leading characters, so type-ahead on `l` would have cycled the two money grants. They now lead with the scope: *"Invited clippers: …"* and *"Whole review queue: …"*.

**The level-two phrase was changed** for the reasons in PART 1, and `normalisePhrase` now strips trailing sentence punctuation, which had been failing all three phrases for anyone dictating.

**Also implemented:** the mismatch alert on level one gained the house error treatment (it was the only alert on the card rendered identically to the help text above it, and in this theme `--text-primary` and `--text-secondary` are both `#ffffff`, so there was no colour fallback either); level two's mismatch alert is keyed on its own failure counter so a second wrong attempt still speaks; all three forms are named so their three identical cancel buttons are distinguishable; a `saving` branch on the status line; level one's save-failure copy no longer says "any clip", which would now read as a claim about level two; the destination rule is rendered once and pointed at by both triggers; `<h5>` headings for the two levels; and the `reviewerScopeInvitedOnly` block that tells the owner when level two grants nothing.

**Reported, NOT fixed:** BL-821's page-wide silent list replacement on `/admin/clips` (B12 there, its own round), and `role="alert"` doubling as an `aria-describedby` target in the confirmation panels.

---

## GATES, HONESTLY

* **eslint confirmed present**, `v9.39.4`, so the hooks gate is a real check and not a silent no-op.
* Clean baseline on the untouched worktree **before any edit**: `npm ci` exit **0**, `npx prisma generate` exit **0** (before tsc, because `npm ci` wipes the client), `npx tsc --noEmit` exit **0**, `grep -c "error TS"` = **0**.
* `npx tsc --noEmit` exit **0**, **0** errors, run six times. **One error appeared mid-round and is PRE-EXISTING, not mine**: `.next/dev/types` reports that `clip-limit-overrides/route.ts` exports `MAX_CLIPS_PER_DAY_CAP`, which a Next route module may not do. It surfaces only after `next dev` has generated its route types, it is in a file this diff does not touch, and **BL-815 reported the identical error in the identical file**. The final `tsc` was run on a **removed `.next`** so the number is not masked by a stale artifact.
* `npm run build` written to a log with the exit code echoed by hand and **never piped through `tail`**: **`BUILD1_EXIT=0`**, "Compiled successfully in 35.2s". Prebuild clean: `check:prisma-bypass` 0 violations, `check:removed-fields` OK across **736** files, hooks gate **11 problems (0 errors, 11 warnings)** at the ceiling of 11 with **zero added**.
* Counted with `grep -c`, **never piped through `head`**. **No heredocs** were used to write any file. One shell at a time.
* **No Apify actor was run.** Nothing in `apify.ts` or the 11 BL-678 guards was touched. **No schema change**, no `prisma migrate`; the new capability is a string in an existing `text[]` column.
* **Money files byte-identical by blob OID on BOTH refs:** `clip-earnings-writer.ts` `ac5be7de`, `earnings-calc.ts` `797e2098`, `balance.ts` `81a683c1`, `tracking.ts` `359bcbbe`, `clip-earnings-invariant-middleware.ts` `61cef393`, `money-decimal.ts` `ef5cdae7`, `campaign-era.ts` `106e16ad`, **`campaign-reassign.ts` `3e513702`**.
* **Earnings invariant 0 violations.** No payout was created, modified, approved or cancelled by this round, and no real clip's status, campaign or earnings changed.

---

## DISCLOSED, BECAUSE MY OWN WORK CAUSED IT

**MY DEV SERVER EXHAUSTED THE SUPABASE CONNECTION POOL AND IT REACHED THE REAL OWNER'S LIVE SESSION.** Four `SERVER_ERROR` rows on his account between **`17:41:01.832`** and **`17:44:50.136`**, on `/api/admin/sidebar-seen` and `/api/admin/sidebar-counts`, all carrying *"Too many database connections opened"*. My own dev logs contain **zero** such errors, which is how it is attributable: the pressure was mine and the failures were his. They are failed reads; nothing was written or lost. BL-815 caused the same thing and disclosed it; BL-821 avoided it by stopping each server between phases, and I ran two servers across a longer window and did not.

**Also disclosed, and NOT mine.** The owner was working in production throughout. Inside my window he **approved a payout** (`APPROVED_PAYOUT` at `17:44:29.632`, taking the table from 190 rows to 191), hit three `PAYOUT_REVIEW_RETRY_EXHAUSTED` rows on a different payout, and **approved three clips** at `17:27` to `17:28`. Every audit row in my window is accounted for: those, plus my one `REVIEWER_CONFIG_UPDATED` (written by the dev-auth owner, not by his account) and my fixture moves.

---

## THE FIXTURES, NAMED AND REMOVED

**Three synthetic rows, because the round is about the difference between two of them.**

| id | inviter | why |
|---|---|---|
| `bl825-invitee-clipper` | jdb001 | proves LEVEL ONE still works |
| `bl825-stranger-clipper` | **NULL** | proves LEVEL TWO, and proves LEVEL ONE refuses it |
| `bl825-selfclip` | owned by jdb001's real account | proves the self-move block at both levels |

**Why fixtures.** Measured at `17:00`: jdb001 has 15 clips waiting for his decision and **zero** of them belong to a clipper he invited, so level one has nothing real to act on. The clips that are there belong to real people, and moving one sends a notification that cannot be un-sent, which is why BL-736 and BL-740 moved nothing at all. Manufacturing an invitee out of a real account means writing `users.referredById`, the column deciding the 9%-versus-4% platform fee and the 5% referral mint. That is a money write and it was not made.

```
users         bl825-invitee-clipper, bl825-stranger-clipper   isDeleted true, referredById NULL
clips         bl825-invitee-clip, bl825-stranger-clip, bl825-selfclip   isDeleted true
clip_accounts bl825-invitee-acct, bl825-stranger-acct         REJECTED
campaign_accounts / notifications / clip_limit_overrides / agency_earnings   0 rows
jdb001's invitees                                             28   (his true count)
jdb001's own live clips                                       0    (his true count)
reviewer_audit_log rows for the fixtures                      5    KEPT
```

**A hard delete is impossible and that is a protection working.** `reviewer_audit_log` is append-only (BL-87 immutability trigger) and the moves wrote rows a cascade would have removed. The trigger was **not** defeated to tidy a test fixture. Every SQL step is committed under `scripts/migrations/BL-825-*.sql`.

---

## MERGED AND PUSHED

| | |
|---|---|
| clean `tsc` baseline before any edit | `npm ci` **0**, `prisma generate` **0**, `tsc` **0**, `grep -c "error TS"` **0** |
| branch | `checkpoint/BL-825` @ **`712fb196`**, VERIFIED on origin by `safe-push` |
| merge commit | **`b5cccb7`**, `origin/main` VERIFIED by `safe-push` |
| conflicts | **none**; main never moved from `e5a1846a`, and the **merged tree OID equals the branch tree OID exactly** (`d4f45f02`), so the branch's green build IS the merge's build. `BACKLOG.md` carries **0** conflict markers |
| BACKLOG | **164 sections before, 165 after**, counted with `grep -c` and never piped to `head` |
| **`checkpoint/BL-723`** | **confirmed NOT an ancestor of main** |
| post-merge money files | all eight byte-identical by blob OID across the merge, `campaign-reassign.ts` still `3e513702` |
| worktree `C:/w825` | **removed** |
| tags | `pre-BL-825`, `pre-merge-BL-825`, `post-merge-BL-825`, all on origin |

> **A REDEPLOY ON RAILWAY IS REQUIRED.** Main carries both levels; production still knows only level one.

---

## WHAT COULD NOT BE PROVEN, AND WHY

* **jdb001 himself has not pressed the button.** The flow is proven end to end by real HTTP requests through the real route as his real session, not by a person clicking in production.
* **Seven destination-status blocks were not observed refusing at level two**, for the reason in PART 3. The structural argument is that `evaluateDestination` has no notion of a level and `campaign-reassign.ts` is byte-identical, and that argument is as strong as the blob OID.
* **Nothing was verified against production over HTTP.** Every request ran locally against this branch, pointed at the production database.
* **A real screen reader was not run.** DOM order, roles, focus behaviour and the announcement paths are reasoned and measured; NVDA, JAWS and VoiceOver were not.
* **The owner's card renders under the dev-auth session**, so it is `Dev Owner`'s view of jdb001's profile, not the owner's own login.

## WHAT THE OWNER SHOULD DECIDE NEXT

1. **The tick list is now the only thing holding him in.** With the invitee limit gone at level two, ticking a campaign hands him every clip waiting for his decision in it. He currently has three ticked.
2. **The other two real reviewers each have ONE ticked campaign**, which is a measured zero at either level, because the only permitted destination would be the campaign the clip already sits on and `SAME_CAMPAIGN` refuses it.
3. **`reviewerScopeInvitedOnly` and level two are opposites.** The one partner carrying that flag would gain nothing from level two until it is unticked, and the card now says so on the spot.
