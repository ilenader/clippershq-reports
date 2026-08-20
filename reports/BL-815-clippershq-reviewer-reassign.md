# BL-815 — a reviewer can move a clip to a different campaign, scoped to his own invitees and to the campaigns you assign him

**2026-08-20 · DB `now()` = `2026-08-20 17:48:01.922687+00` (first read) to `18:52:42.715943+00` (last) · BUILD AND MERGE.**
Base `origin/main` @ `a57bfda6`. Branch `checkpoint/BL-815` @ `cda7d39d`. **Merged and verified pushed: `origin/main == local == 7f97dd0f`.** Tags `pre-BL-815`, `post-BL-815`, `pre-BL-815-merge`, `post-BL-815-merge`, all on origin. Isolated worktree `C:/w815`, a short path, `node_modules` never junctioned, **removed at the end**. Every read through `scripts/run-select.js`, every timestamp cast `::text` against DB `now()`. Handles redacted, ids truncated, no wallet address read or printed.

**A REDEPLOY ON RAILWAY IS REQUIRED BEFORE ANY OF THIS IS LIVE.**

> **NOBODY HOLDS THE NEW CAPABILITY. It is off for every one of the 14 reviewer rows, and the round ends with it off.** The dev reviewer held it for 45 minutes while the proofs ran and was restored to its exact snapshot.
> **NO REAL CLIPPER'S CLIP WAS MOVED.** Every move in this round was on a synthetic fixture this round created and removed.

---

## PART 0 — THE SCOPE QUESTION, DECIDED FIRST, BECAUSE IT DEFINES THE FEATURE

**The question: which campaigns may a reviewer move a clip INTO?**

**Recommended and BUILT: only the campaigns already ticked in "Limit to campaigns" on his own profile page. With none ticked he can move nothing. THIS IS THE OWNER'S CALL AND HE CAN OVERRULE IT.**

**Why this and not "any campaign you run".** The risk the brief names is exact: he could move his own invitee's clip into a higher-paying campaign you never meant him to touch, and that is a money decision. Tying destinations to the campaigns you have already assigned him makes **every configuration an explicit decision of yours**, and it reuses a control that has existed since the reviewer system was built rather than inventing a second one.

**It is not too narrow to be useful, measured.** All four real reviewers already carry a non-empty campaign scope: 3, 1, 1 and 1 campaigns. The feature works for them the moment you grant it.

**THE ONE PLACE THIS ROUND INVERTS AN EXISTING CONVENTION, stated loudly.** `isCampaignInReviewerScope` treats an EMPTY campaign list as UNRESTRICTED, which is right for a READ tightening: the status quo there is "sees everything". A destination list cannot inherit that default. The status quo for MOVING is "cannot move at all", and picking a destination picks the rate a clipper is paid at, so **`isCampaignInReviewerMoveScope` treats EMPTY as NONE**. If it did not, one checkbox would silently hand a partner every campaign you run.

**The coupling is real and the card now says so.** Ticking campaigns to give him destinations also narrows his review queue to those campaigns, because both read the same column. The two are one idea, "the campaigns this person works on", and the profile page states both readings side by side.

**WHOSE CLIPS: his own invitees', ALWAYS. Not negotiable and not configurable.** `isClipInReviewerMoveScope` deliberately does **not** read `reviewerScopeInvitedOnly`, which is ON for exactly **1 of the 14** live reviewer rows. Had the move scope read that flag, granting the capability to any of the other thirteen would have let them move **any** clipper's clip, with the whole feature's safety property decided by a checkbox on a different line of the same page. Fail-closed in three directions: a clipper with no inviter is refused, a reviewer with no id is refused, and a reviewer's own clip is refused (the self-review block, generalised).

---

## PART 1 — THE SWITCH ON THE PROFILE PAGE

A new block, **directly under "Limit to campaigns"** because that control is this grant's precondition, headed **"Move clips between campaigns"**, off for everyone.

**What it says it gives, in plain words:** *"Turned on, they can take a clip from one of the clippers they invited and move it to a different campaign. The clip then earns at the destination campaign's rates, so this changes what that clipper is paid. They can only move a clip that is still waiting for a decision and has earned nothing yet."*

**What it says it does NOT give**, in the same block: *"Payouts and the list of unpaid ones, agency earnings, clipper accounts, the full user list, the audit log and your ratification queue all stay refused, and they never see your own rate on a campaign."* BL-791 proved all six by direct request; this round adds the seventh, the owner rate, and proves it in PART 4.

**THE DELIBERATE CONFIRMATION: the typed phrase `MOVE CLIPS`,** in the same spirit as BL-788's `FULL AUTHORITY` and **deliberately different words**, so muscle memory from one confirmation cannot carry a person through the other. **Taking it away needs nothing at all**, because obstructing the safe direction is a defect rather than a safeguard, and the gate fires only on the TRANSITION to held, so re-saving an unrelated checkbox does not demand the phrase again.

```
PATCH capabilities=[CLIP_REASSIGN_CAMPAIGN]                              -> HTTP=400
PATCH ... confirmMoveClips="MOVE CLIP"                                   -> HTTP=400
PATCH ... confirmMoveClips="FULL AUTHORITY"   (BL-788's own phrase)      -> HTTP=400
   "To let this person move clips between campaigns, type MOVE CLIPS to confirm.
    A move changes the rate the clipper is paid at."
PATCH ... confirmMoveClips="MOVE CLIPS"                                  -> HTTP=200
```

**A control, not a checkbox, and ONE control rather than two** — the accessibility review's ruling and its reasoning is in the a11y section.

---

## PART 2 — THE SERVER GATE, PROVEN BY DIRECT REQUEST

**Nothing here is inferred from reading code.** BL-740 is why: a block that fired on 92 of 93 pairs was invisible to both code reading and a 69-check harness.

```
=== WITHOUT THE CAPABILITY ===
REVIEWER GET  /api/admin/clips/<real clip>/reassign-campaign   -> HTTP=403
REVIEWER POST /api/admin/clips/<real clip>/reassign-campaign   -> HTTP=403
   {"error":"You have not been given permission to move clips between campaigns."}
CLIPPER  GET  ...                                              -> HTTP=403  (the sentence they always got)
ADMIN    POST ...                                              -> HTTP=403  (unchanged)

=== WITH IT, BUT THE CLIP IS NOT HIS INVITEE'S ===
REVIEWER GET  /api/admin/clips/cmt1sht5y0.../reassign-campaign -> HTTP=404 {"error":"Clip not found"}
REVIEWER GET  /api/admin/clips/cmZZZZ...../reassign-campaign   -> HTTP=404 {"error":"Clip not found"}
REVIEWER POST /api/admin/clips/cmt1sht5y0.../reassign-campaign -> HTTP=404 {"error":"Clip not found"}

=== WITH IT, BUT THE CAMPAIGN IS NOT ONE OF HIS ===
REVIEWER POST destination=SomeSome App (ACTIVE, would otherwise pass) -> HTTP=403 DEST_OUTSIDE_REVIEWER_SCOPE
REVIEWER POST with NO campaign assigned at all                        -> HTTP=403
   "You have not been assigned to any campaign, so there is nowhere to move this clip to."
```

**The 404 is generic and byte-identical to the 404 for an id that does not exist**, matching BL-788, so another clipper's clip is never confirmed to exist. **The destination scope is checked BEFORE the campaign is looked up**, so an unknown id and an out-of-scope id also cannot be told apart. Both refusals are **audited** (`CAPABILITY_DENIED_403`, `INVITEE_SCOPE_VIOLATION_404`), so an attempt leaves a trace rather than vanishing. The capability is read from the **DATABASE** on every request, never from the session token, which can be 30 seconds behind a revoke.

**A referral-only reviewer cannot slip through.** BL-190 suppresses the Basic clip caps for a reviewer whose only grant is `REFERRAL_MANAGE`, so the route requires `CLIP_VIEW` **as well as** the move capability: someone who cannot see a clip can never move one by crafting a request.

---

## PART 3 — THE SAME SEVEN BLOCKS, AND THE PROOF IS A BLOB OID

**`src/lib/campaign-reassign.ts` is BYTE-IDENTICAL to main: `3e513702` on `a57bfda6` and on merged `7f97dd0f`.** BL-736's seven hard blocks and BL-740's corrected admission condition are therefore provably untouched. There is no second reassignment path: a reviewer's move enters the same route, the same `evaluateDestination`, the same single `db.$transaction`, the same `SELECT ... FOR UPDATE` re-assert and the same **CPM restamp inside that one `clip.update`**, which is what makes the rates agree by construction (BL-539's ambiguous row, BL-570's $933.94).

**Eight block codes observed refusing IN HIS OWN PICKER, on real campaigns, with the fixture put into each state:**

```
BLOCKED  STRAENGE                    DEST_PAST + DEST_ERA_WOULD_FREEZE + CLIPPER_ACCOUNT_NOT_APPROVED
BLOCKED  BAD BITCH ANTHEM (2.50)     DEST_PAUSED + DEST_PLATFORM_NOT_ACCEPTED + CLIPPER_ACCOUNT_NOT_APPROVED
BLOCKED  bees.n.honey / Gainzalgo / GainzAlgo (REPOST) / Hapday / Panic Baby / somesome / Zhus   DEST_PAST
BLOCKED  Zhus Meme (0.20 CPM)        CLIPPER_ACCOUNT_NOT_APPROVED + DEST_DAILY_LIMIT_REACHED + DUPLICATE_URL_IN_DEST
BLOCKED  Zhus Edit (0.50 CPM)        SAME_CAMPAIGN + CLIPPER_ACCOUNT_NOT_APPROVED
```

**And they refuse the POST, not merely the picker:**

```
REVIEWER POST -> 409 "This clipper's account is not approved, so it cannot be on any campaign."  CLIPPER_ACCOUNT_NOT_APPROVED
REVIEWER POST -> 409 "STRAENGE has ended. A clip moved there can never earn."                    DEST_PAST (+DEST_ERA_WOULD_FREEZE)
REVIEWER POST -> 409 "Deja Shoe is archived. A clip moved there could never be approved or earn." DEST_ARCHIVED
REVIEWER POST -> 409 "Only a PENDING clip can be moved. This clip is REJECTED."                   CLIP_NOT_PENDING
                     + CLIP_HAS_EARNINGS + CLIP_HAS_MONEY_ROWS
```

**DEST_ARCHIVED is the one that shows the list filter is not a relaxation:** archived campaigns are hidden from the picker and the POST still refuses one by name.

**TWO BLOCKS COULD NOT BE DEMONSTRATED LIVE AND ARE NOT CLAIMED.** `DEST_OVER_BUDGET` fires on no live campaign today (none is over budget) and `DEST_NO_CPM_FOR_PLATFORM` on none either (no campaign accepts a platform it has no rate for). Manufacturing either would have meant editing a real campaign's budget or rates. Both are asserted against the shared rule set in the harness and both were measured firing by BL-740.

**The restamp, observed:**

```
BEFORE  campaign Zhus Edit (0.50 CPM)   stamp clipper 0.5000   stamp owner 0.3197   PENDING   earnings 0
POST    /api/admin/clips/<clip>/reassign-campaign  as REVIEWER  -> 200 {"success":true}
AFTER   campaign Zhus Meme (0.20 CPM)   stamp clipper 0.2000   stamp owner 0.1279   PENDING   earnings 0
        campaign_accounts membership on the destination: 1 (created inside the same transaction)
```

---

## PART 4 — WHAT THE REVIEWER SEES, AND WHERE THE OWNER SEES IT

**He gets the owner's picker**, with blocked destinations as a plain keyboard-reachable list carrying their reasons, never natively disabled options (BL-556's house rule, the defect BL-736's review caught). **Only the campaigns he is assigned to are listed**, and the exclusion is disclosed in ONE sentence with a count rather than repeated as identical rows, exactly as BL-740 ruled for archived campaigns: *"Archived campaigns are not shown. 12 campaigns are not shown because you are not assigned to them."* Listing the rest would also hand him your whole campaign roster by name.

**THE FOUR RATES, EACH LABELLED WITH WHOSE AND WHICH.** BL-744 fixed a bare "Current rate" that never said whose, and BL-743 lost a full round to reading an owner figure as a clipper figure, so no figure is positioned into meaning:

| the OWNER sees | the REVIEWER sees |
|---|---|
| Current clipper rate **$0.50** | Current clipper rate **$0.50** |
| New clipper rate **$0.50** | New clipper rate **$0.20** |
| Current owner rate **$0.3197** | Current owner rate **Not shown to you** |
| New owner rate **$0.25** | New owner rate **Not shown to you** |

**THE ONE PLACE THIS ROUND DELIBERATELY DEPARTS FROM THE BRIEF, flagged loudly.** PART 4 asked for both rate pairs on the confirmation. **The OWNER now gets all four, which is new.** A REVIEWER gets the two clipper figures and the words **"Not shown to you"**, because `ownerCpm` is owner-tier campaign economics: CLAUDE.md keeps it from non-owner roles, BL-240 already nulls it for a reviewer elsewhere, and BL-814 hardened the neighbouring route for exactly this reason. This route was not going to become the one place it leaks. It is rendered as WORDS, never as a dash, a blank or "No rate", each of which would tell him the owner earns nothing, and one sentence says it outright: *"The owner's rate is not shown to reviewers. It is not zero, and it is not missing."*

**EVERY MOVE WRITES AN AUDIT ROW, and a reviewer's is written INSIDE the transaction**, so a move that cannot be audited does not commit. BL-732 found an archive cascade that wrote none and went unnoticed for three days.

```
audit_logs      CLIP_CAMPAIGN_REASSIGNED  actor=dev-reviewer-001  2026-08-20 18:03:34.127
  {"actorRole":"REVIEWER","fromCampaignName":"Zhus Edit (0.50 CPM)","toCampaignName":"Zhus Meme (0.20 CPM)",
   "platform":"Instagram","oldClipperCpm":0.5,"oldOwnerCpm":0.3197,"newClipperCpm":0.2,"newOwnerCpm":0.1279,
   "rowsRepointed":{...},"clipCreatedAt":"2026-08-20T18:03:02.367Z"}

reviewer_audit_log  CLIP_CAMPAIGN_REASSIGNED  reviewerUserId=dev-reviewer-001  2026-08-20 18:03:34.048+00
  requestRoute "POST /api/admin/clips/[id]/reassign-campaign", both campaigns, both rate pairs, the clipper id
```

**WHERE THE OWNER SEES IT, in two places, neither of them after the fact.** In **`/admin/audit-log`**, where the row now carries `actorRole` so he need not resolve an id to learn whether he moved the clip himself. And under **"Recent reviewer activity" on that reviewer's own profile page**, verified by asking the endpoint as the owner: `GET /api/admin/users/dev-reviewer-001/reviewer-activity` returns the move at the top of the list.

---

## PART 5 — WHAT THE CLIPPER SEES IS IDENTICAL EITHER WAY

**Proven by moving the same clip both ways**, not by reading the code:

```
18:03:34  moved by the REVIEWER  "Your clip moved to a lower paying campaign"
  "We moved your clip to Zhus Meme (0.20 CPM). Zhus Meme (0.20 CPM) pays $0.20 per 1,000 views instead of
   $0.50, so this clip will earn less than the campaign it was submitted to. Nothing you did caused this
   and the clip is still under review."
18:04:12  moved back by the OWNER  "Your clip moved to another campaign"    (rate up, no drop language)
18:04:13  moved again by the OWNER "Your clip moved to a lower paying campaign"
  ...BYTE-IDENTICAL title and body to the reviewer's move.
```

The notification names no actor and never has; the pay-cut branch leads with the rate, per BL-730's recommendation and BL-736's null-stamp fix. **Yes, the clipper is told, every time, whoever moved it.**

---

## PART 6 — THE EVIDENCE

| claim | evidence |
|---|---|
| refused without the capability | 403 on GET and POST, by direct request, audited `CAPABILITY_DENIED_403` |
| only his own invitees' clips | generic 404 on a real clipper's clip, identical to the 404 for a nonexistent id |
| only campaigns he is assigned to | 403 `DEST_OUTSIDE_REVIEWER_SCOPE`, checked before the campaign lookup |
| the seven blocks refuse for him | 8 codes in his picker + `DEST_ARCHIVED` and 3 clip-side codes by POST; 2 codes not demonstrable live and not claimed |
| the CPM restamped inside the transaction | 0.5000/0.3197 → 0.2000/0.1279 in the same `clip.update` as the campaign move |
| every surface agrees | clip row, `campaign_accounts` membership, both audit tables and the notification all read the destination |
| the audit row is written | `audit_logs` + `reviewer_audit_log`, both quoted in PART 4 |
| the owner can see it | `/admin/audit-log` with `actorRole`, and the reviewer-activity endpoint answered 200 as OWNER |
| no clipper's earnings fell | **earnings invariant 0 violations** before (`17:54:20Z`) and after (`18:52:42Z`) |
| no payout touched | **no payout created, modified, approved or cancelled by this round** — see the disclosure below |
| the 6 money files + `tracking.ts`, `campaign-era.ts`, `apify.ts`, `payout-calc.ts`, `cpm.ts`, `rate-format.ts`, `campaign-reassign.ts` | **byte-identical by blob OID on BOTH refs**: `ac5be7de`, `797e2098`, `e887f80a`, `83ce4bab`, `61cef393`, `ef5cdae7`, `106e16ad`, `656bf4c0`, `029834b4`, `57240872`, `e8ae1bc3`, `3e513702` |
| schema | **no change at all**, no `prisma migrate`; `prisma generate` only |
| Apify | **no actor run**; nothing in `apify.ts` or the 11 BL-678 guards touched |

**`scripts/bl815-verify.ts`: 112 passed, 0 failed.** It drives the real exported helpers, extracts every shipped gate from source so a deleted guard fails the suite, and asserts the POSITIVE case as loudly as the refusals, which is the hole BL-740 found in BL-736's 69 checks. `scripts/test-reviewer-permissions.ts` (the pre-existing suite): **55 passed, 0 failed**.

### The clip that was moved, named, and why it is not a real one

**`bl815-fixture-clip`, a wholly synthetic clip this round created at `17:59:43Z` and removed at `18:44:41Z`.**

**Why a fixture.** The feature needs a clip whose CLIPPER was invited by the acting REVIEWER. Measured at `17:48:01Z`, **not one of the four real reviewers has an invitee with a PENDING clip** — the count is 0 for all four — so no such clip exists in production. Manufacturing one would have meant writing `users.referredById` on a live account, and that is the column deciding the 9%-versus-4% platform fee and the 5% referral mint. That is a money write and it was not made.

**BL-814's clip `cmsyn3hrt0iwr0xo1mu7mpylv` was NOT used.** It is **APPROVED again with $0.76 of earnings on Zhus Meme**, so all three clip-side blocks refuse it. It was left exactly as found.

**The fixture could not be HARD deleted, and that is a protection working.** `DELETE FROM clips` was refused by the database itself: *"reviewer_audit_log is append-only (BL-87 immutability trigger). UPDATE and DELETE are blocked at the DB layer."* The reviewer's move had written an audit row that the cascade would have removed. **The trigger was not defeated.** The fixture is soft-deleted (`isDeleted = true`, `isTestUser = true`), so it is absent from every query in the app, its campaign memberships and notifications are hard-deleted, and the audit trail survives. The SQL for every step is committed under `scripts/migrations/BL-815-fixture-*.sql`.

**The dev reviewer was restored to its exact snapshot** (`role REVIEWER · LIVE · caps {CLIP_REVIEW} · scope {} · invitedOnly false · canSeeDecided false`); only `sessionVersion`, a monotonic counter, is higher.

### Rendered at all five widths, with the viewport MEASURED

BL-799 could not get past this: the browser extension reported a successful resize while `window.innerWidth` never moved, so four of five widths were never actually seen. Playwright sets the viewport on the context, and `scripts/bl815-render.mjs` **prints the measured `innerWidth` beside every file**.

```
profile-switch-off / profile-confirm            320 375 414 1280 1440   10 shots
profile-switch-on / reviewer-picker / reviewer-confirm  320 375 414 1280 1440   15 shots
owner-confirm                                   320 375 414 1280 1440    5 shots
ALL 30 SHOTS AT THE ASKED WIDTH (measured == asked, every one).
```

Seen and read at 375: the confirmation panel with its six left-border blocks, the accent `MOVE CLIPS` phrase, the input and both buttons; the reviewer's dialog with Clipper / Account / Currently on / Current clipper rate `$0.50` / Current owner rate **Not shown to you**, "Move to (1 available)" with the drawn selection indicator, the exclusion sentence, the four labelled rates, the immediacy warning, the pay-cut warning and "The clipper is told about this move either way." Seen at 1440: the owner's four rates including **Current owner rate $0.3197 / New owner rate $0.25** at four decimal places. The PNGs are deliberately **not committed** (30 files); the harness that regenerates them is.

---

## THE ACCESSIBILITY REVIEW, RUN BEFORE ANY UI WAS WRITTEN

The lead and nine specialists reviewed the DESIGN. **Every blocking item was implemented rather than argued with.** The ones that changed the work:

**A money defect in my own code, and the most serious finding of the round.** The dialog used `formatCurrency`, which is Intl USD locked to two decimal places. CPM stamps are `Decimal(10,4)`, so it printed the derived owner rate `$0.1279` as **`$0.13`** — and printed `$0.1279` and `$0.1312` **identically**, so a panel whose whole purpose is to show a change could have read "Current owner rate $0.13 / New owner rate $0.13" over a real change about to be written. All twelve figures now use **BL-756's `fmtRate`**, in the visible text and in the announced text, so display and announcement are one expression.

**The switch is a BUTTON, not a checkbox, and ONE button rather than two.** `role="checkbox"` requires `aria-checked`, and a control that opens a confirmation cannot honour it: this file's own comment records that the DOM checkedness flips before any handler runs, so a screen reader would announce "checked" and then a panel would appear saying nothing had been granted. And a single node that RELABELS is what lets focus return to it after the save; two buttons would unmount the pressed one and drop focus to the document body in silence.

**Four checkboxes on this card blurred the owner to the document body on every save.** Each carried `disabled={saving}` while its own `onChange` called `patch()`, so pressing Space disabled the focused input and focus was never restored. Pre-existing, but the new flow makes the trip down to "Limit to campaigns" and back a designed part of the work. All four now use BL-790's proven pattern: `aria-disabled`, an `onClick` that cancels the native activation, and the load-bearing `onChange` guard.

**The card contradicted itself about an empty tick list**, teaching "unchecked = unrestricted" while the new panel had to assert "unchecked = nothing". Both readings now appear together, on the control itself, at the moment the money grant is made. **"Limit to campaigns" also gained a real group name**, having been a bare styled `div` wrapping about thirty loose checkboxes.

**A live defect I would otherwise have cloned:** the BL-788 mode trigger advertises `aria-expanded` but its handler only ever set it true, so a second press did nothing. Fixed, and the two typed-phrase panels are now mutually exclusive through a **focus-free** reset, because the user-facing cancel ends by focusing its own trigger and would have raced the other panel's open-focus effect.

**A TRIAL reviewer's move does not wait for you, and nothing said so.** Every other thing a TRIAL reviewer does is a suggestion you ratify. A move restamps the rate and notifies the clipper in the same request. The confirmation now tells him: *"This takes effect straight away. Unlike approving or rejecting, it does not wait for the owner to agree."* Your own panel says the same before you grant it.

**Also fixed:** the dialog's `aria-describedby` named a node that only mounts after loading, so a blocked clip could open announcing nothing; the picker's focus indicator was a Tailwind `ring`, which compiles to `box-shadow` and is discarded under Windows forced-colors, now an `outline`; the dialog's error alert is keyed on a failure counter so a second identical failure re-announces; focus after a successful move falls back to the page heading, because for a reviewer the moved clip's row unmounting is the normal case; `aria-haspopup="dialog"` on the trigger; and a hardcoded `#2596be` removed.

**The review also corrected three factual claims in my brief** — "Limit to campaigns" is above the checklist and not below it, the phrase gate is case-sensitive on the server so the client must always send the canonical constant, and `--text-primary`, `--text-secondary` and `--text-muted` are **all `#ffffff`**, which means every "render it muted so it reads as withheld" instinct is a visual no-op and the withheld figures needed words.

**Reported, NOT fixed:** `Button` still uses native `disabled` while loading at 139 call sites in 63 files (BL-814's open item); the Basic group's three checkboxes are still natively disabled; touch targets in the older rows of this card are under 24px (2.5.8); and `visibleToasts={4}`.

---

## MERGED AND PUSHED

| | |
|---|---|
| clean `tsc` baseline on the untouched worktree, **before any edit** | `npm ci` exit **0**, `npx prisma generate` exit **0** (before tsc, because `npm ci` wipes the client), `npx tsc --noEmit` exit **0**, `grep -c "error TS"` = **0** |
| branch | `checkpoint/BL-815` @ **`cda7d39d`**, VERIFIED on origin by `safe-push` |
| merge commit | **`7f97dd0f`**, `origin/main` verified by `git ls-remote` |
| conflicts | **none**; main never moved from `a57bfda6`, and the **merged tree OID equals the branch tree OID exactly** (`c909436c`), so the branch's green build IS the merge's build |
| BACKLOG | **158 sections before, 159 after**, `BL-815` x1, **0 conflict markers**, counted with `grep -c` and never piped to `head` |
| **`checkpoint/BL-723`** | **confirmed NOT an ancestor of main** |
| files | 22 changed, 8 of them source |
| worktree `C:/w815` | **removed**, 0 node processes left behind |

> **A REDEPLOY ON RAILWAY IS REQUIRED.** Main carries the feature; production still refuses every reviewer.

---

## GATES, HONESTLY

* **eslint confirmed present**, `v9.39.4`, so the hooks gate is a real check and not a silent no-op.
* `npx tsc --noEmit` exit **0**, `grep -c "error TS"` = **0**, run seven times across the round. **Two errors appeared mid-round and BOTH were proven PRE-EXISTING rather than mine**, by stashing the file back to main and reproducing the byte-identical error: a Next route module may export only its handlers and a fixed set of config names, and `reviewer-config/route.ts` exported BL-788's `FULL_AUTHORITY_PHRASE` while `clip-limit-overrides/route.ts` exports `MAX_CLIPS_PER_DAY_CAP`. They surface only once `next dev` has generated `.next/dev/types`, which is why they had survived. **I fixed the first, because I was already in that file**: both phrases now live in `@/lib/reviewer-capabilities`, which has no database import, so the browser and the server share ONE constant instead of two copies. The second is in a file not in this diff and is reported, not touched. The final `tsc` was run on a **removed `.next`**, so the number is not masked by a stale artifact.
* `npm run build` **twice**, each written to a log with the exit code echoed by hand and **never piped through `tail`**: **`BUILD1_EXIT=0`** and **`BUILD2_EXIT=0`**, "Compiled successfully in 26.0s" and "in 20.6s". Prebuild clean both times: `check:prisma-bypass` **0 violations**, `check:removed-fields` **OK across 729 files**, hooks gate **11 problems (0 errors, 11 warnings)** at the ceiling of 11 with **zero added**.
* Counted with `grep -c` and explicit loops, **never piped through `head`**. **No heredocs** were used to write any file. One shell at a time.

---

## DISCLOSED, BECAUSE MY OWN WORK CAUSED IT

**MY DEV SERVER EXHAUSTED THE SUPABASE CONNECTION POOL AND IT REACHED THE REAL OWNER'S LIVE SESSION.** Four `SERVER_ERROR` rows between **`18:31:10.351`** and **`18:34:03.317`**, on `/api/admin/sidebar-seen`, `/api/admin/sidebar-counts` and `/api/profile/avatar`, all carrying *"Too many database connections opened"*, all against the owner's real account. It also broke one of my own render runs, which is how it was noticed. I stopped the dev server at `18:44`, and **zero such errors have occurred since**. No data was written or lost by them; they are failed reads. This is a real, if brief, production degradation caused by this round and it is on the record rather than in a log I deleted.

**Also disclosed, and NOT mine.** The owner was working in production throughout. Inside my window he **demoted and banned reviewer `cmovb0q6…`** at `18:20:10` and `18:20:27` (audited to his own id), which is what moved the platform-wide reviewer-flag fingerprint; he **rejected one payout** at `18:21:20` (`$46.51`, `paidAt` still NULL); and a clipper **requested a new payout** at `18:23:09` (`$20.30`), which is why the payout table reads 184 rows rather than 183. **No payout was created, modified, approved or cancelled by me**, and every one of the nine audit rows in my window is accounted for: five `REVIEWER_CONFIG_UPDATED` on `dev-reviewer-001` (mine), three `CLIP_CAMPAIGN_REASSIGNED` on `bl815-fixture-clip` (mine), and the owner's own actions above.

---

## WHAT COULD NOT BE PROVEN, AND WHY

* **No real reviewer has exercised this**, because none has an invitee with a pending clip. The flow is proven end to end against a synthetic clipper the reviewer really did invite, by real HTTP requests through the real route, not by a person pressing a button in production.
* **`DEST_OVER_BUDGET` and `DEST_NO_CPM_FOR_PLATFORM` were not observed refusing live**, for the reasons in PART 3. They are asserted against the untouched rule set and were measured firing by BL-740.
* **Nothing was verified against production over HTTP.** Every request ran locally against the merged tree with the dev-auth bypass, pointed at the production database. No authenticated request was made against clipershq.com and none is claimed.
* **A real screen reader was not run.** DOM order, roles, live regions, focus behaviour and the withheld-figure wording are all measured; NVDA, JAWS and VoiceOver were not.
* **The renders show the dev-auth session**, so the reviewer's screens are rendered as the synthetic `dev-reviewer-001`, not as a named partner.

---

## WHAT THE OWNER SHOULD DECIDE NEXT

1. **Whether the destination scope is right.** I built the narrow option: only campaigns you have ticked for that reviewer. Say the word and it becomes any campaign you run, or any campaign that is ACTIVE.
2. **Who, if anyone, gets it.** Nobody holds it. `tg…d7` (`cmp9d0xu…`) is the natural first candidate — TRIAL, invitee-scoped, 2 invitees now — but his single assigned campaign is **archived and paused**, so he would have nowhere to move a clip until you tick a live one.
3. **A reviewer still READS every clip in his assigned campaigns while being able to MOVE only his invitees'** — 118 readable against 1 movable on the test configuration. That is correct and deliberate, and turning on "Only clippers they invited" for anyone you grant this to would make the two match.
