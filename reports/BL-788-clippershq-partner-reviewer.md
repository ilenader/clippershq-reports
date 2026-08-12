# BL-788 — the partner reviewer: scoped to his own invitees, and the final say behind a typed phrase

**2026-08-12 · DB `now()` = `2026-08-12 13:38:39.273663+00` before, `13:39:26.087482+00` after · BUILD.**
Base `origin/main` @ `72f05cec`, branch `checkpoint/BL-788`, isolated worktree `C:/bl788`, `node_modules` never junctioned, removed at the end. **No submission created, no clipper's clip acted on, no Apify actor run, no payout touched.** Every database read through `scripts/run-select.js`; every timestamp cast `::text` against DB `now()`. Handles redacted; ids truncated to prefixes.

## THE HEADLINE, INCLUDING THE PART THAT SHRINKS THE ROUND

> **Most of what this brief describes was already built and is REUSED, not rebuilt.** The REVIEWER role that sits alongside a clipper, the recommendation itself (`reviewerMode = "TRIAL"` writes a `ProposedClipDecision` and leaves the clip PENDING), the owner's ratification queue whose APPLY routes through the **same** audited `/api/clips/[id]/review` path the owner uses himself, the partner's own outcome views, the grant checklist, the self-review block, the re-action block, the campaign scope, the date-cutoff scope and a dedicated reviewer audit log all exist today.
>
> **What did NOT exist is the one thing the partner case turns on: scoping a reviewer to the clippers he personally invited.** Without it a partner would see every pending clip on the platform, which is the privacy breach the brief names. That is what this round adds, plus a real confirmation on the handover of the final say, which until today was a browser `confirm()` box that the server then rejected anyway.

## PART 0 — THE REFERRAL LINK, PROVEN BEFORE ANYTHING WAS BUILT

**How an inviter is recorded.** `users."referredById"` — `prisma/schema.prisma:165`, relation at `:306` (`referredBy User? @relation("Referrals", ..., onDelete: SetNull)`), index at `:436`. It is written when a signup arrives through an invite link, and is otherwise changeable only by the owner through `/admin/referral-override`, which stamps `referrerOverriddenBy` and `referrerOverriddenAt` so an override is distinguishable from a natural referral. It is also the input the platform already trusts with money: the 4% versus 9% platform fee reads exactly this column.

**Is it reliable and permanent? Yes, in the only sense that matters here, and the honest caveats are stated.** The column holds either a real inviter id or null. It is never a *wrong* id, so a partner can never be shown someone else's clipper through a stale link. It is not immutable: the owner can reassign it, and `ON DELETE SET NULL` means that if the partner's own account were deleted his invitees' links null out, which empties his queue rather than widening anyone's. **Both failure directions point the safe way.**

**Measured live at `2026-08-12 12:59:49.413882+00`:**

| measure | value |
|---|---|
| live CLIPPER users | **1,317** |
| ... with a recorded inviter | **174 (13.2%)** |
| ... with NO inviter | **1,143 (86.8%)** |
| distinct inviters | **36** |
| manually overridden referrers | **0** |
| clips by invited clippers | **699** |
| clips by clippers with no inviter | **4,730** |
| clips waiting for a decision RIGHT NOW, invited | **11** |
| clips waiting for a decision RIGHT NOW, not invited | **52** |
| proposals ever written | 10 |
| users holding the REVIEWER role today | 27 |

**What happens to the three cases the brief asks about.** A clipper invited by nobody, or who joined before the referral system, carries **null** and therefore matches no reviewer, so a scoped partner never sees them. A clipper whose inviter is not a partner is invisible to every scoped partner except that inviter. **86.8% of the platform is in that first category, which is exactly right: a partner's queue should be small, and it is.**

**What a real partner queue would contain today**, by inviter, redacted to id prefixes:

| inviter | invitees | their clips, all time | waiting for a decision now |
|---|---|---|---|
| `cmoagb` | 12 | 463 | 0 |
| `cmosmy` | 4 | 96 | 0 |
| `cmqic8` | 2 | 71 | **11** |
| `cmrng8` | 3 | 26 | 0 |

**The link is reliable enough to build on, and the round proceeded.**

## PART 1 — THE ROLE AND THE GRANT SCREEN

**A clipper keeps everything.** The role grant does not touch earning, submitting or withdrawing: those run off `canActAsClipper` and the clipper-side gates, and nothing in this diff reaches them. The reviewer-config route's own header says it: *"Pure access-gating; NEVER touches any money field."*

**The grant screen now states what is being granted, in five plain sentences under a real heading**, rendered always and in reading order before the controls it explains:

> **What this person will be able to do**
> • They see clips that are waiting for a decision. With "Only clippers they invited" turned on, they see only clips from clippers who joined through their invite link. With it off, they see clips from every clipper.
> • They start on clips submitted from the day you make them a reviewer. Older clips stay with you.
> • On each clip they can suggest approve or suggest reject.
> • While they still need your agreement, their suggestion changes nothing on its own. The clip, and any money on it, stays exactly as it is until you agree.
> • After you decide, they can see what you chose on each clip they sent you.

**Two of those sentences are corrections the accessibility review caught, and they matter.** The second exists because granting the role writes a fresh-only cutoff, so a new reviewer never inherits the backlog and a screen promising otherwise would be lying. The fourth is scoped to *"while they still need your agreement"* rather than stated flat, because it stops being true the moment full authority is granted, and a static claim that becomes false on a toggle is worse than no claim.

**FULL AUTHORITY, off by default, behind a typed phrase.** `reviewerMode` already defaulted to `TRIAL`. What changed is the handover: the server now refuses `mode: "LIVE"` unless the body carries `confirmFullAuthority === "FULL AUTHORITY"`, and the UI replaced a browser `confirm()` with an inline panel that says in plain words what is being handed over and requires the phrase typed. **Taking the final say back requires nothing at all**, because obstructing the safe direction is a defect, not a safeguard. Demoting to CLIPPER now also clears the partner scope, so a re-promotion starts clean.

**A defect found while building this, and fixed:** the server-side phrase gate and the `invitedOnly` field landed in the route, and the component sent neither. Left as it was, the owner would have answered a confirmation box "yes" and then received a red 400 toast. **Answering a confirmation and being told no is the worst possible ordering**, and it is now impossible.

## PART 2 — WHAT THE PARTNER SEES, AND THE SERVER-SIDE PROOF

The partner uses the reviewer queue that already exists. **What this round adds is that it contains only his invitees' clips**, enforced twice:

**READ, in the WHERE clause and not by hiding anything** — `src/app/api/clips/route.ts`. The flag is loaded in the same round trip that already fetched the campaign scope, and when on:

```ts
where.user = { ...(where.user ?? {}), referredById: session.user.id };
```

An out-of-scope clip is not in the response at all. The local default is `false`, so a code path that ever missed the load stays at today's behaviour instead of widening.

**WRITE, with a generic 404 and an audit row** — `src/app/api/clips/[id]/review/route.ts`, immediately after the existing campaign-scope check:

```ts
if ((reviewerRow as any)?.reviewerScopeInvitedOnly === true) {
  const clipOwner = await db.user.findUnique({ where: { id: reviewedClip.userId }, select: { referredById: true } });
  if (!isClipperInReviewerInviteeScope({ id: session.user.id, role: "REVIEWER", reviewerScopeInvitedOnly: true }, clipOwner?.referredById ?? null)) {
    await writeReviewerAudit(db, { reviewerUserId: session.user.id, action: "INVITEE_SCOPE_VIOLATION_404", clipId: id, ... });
    return NextResponse.json({ error: "Clip not found" }, { status: 404 });
  }
}
```

**It is a 404 and not a 403 deliberately**, matching the campaign-scope pattern three lines above: a 403 confirms the clip exists. **The refusal is audited** so the owner sees the attempt rather than it vanishing.

**The rule, and it fails closed.** `isClipperInReviewerInviteeScope` (`src/lib/reviewer-capabilities.ts`) returns true only when the flag is off, the caller is not a REVIEWER, or the clipper's inviter is exactly this reviewer. **A clipper with no inviter carries null and is refused**, which is the direction that costs a partner a clip he might have been allowed rather than showing him one he was not.

**The reason field on reject already exists** and is carried into `ProposedClipDecision.reason`, which the owner's queue renders. **The post-decision state already exists**: the clip leaves the partner's PENDING list and appears in his proposals list marked as waiting.

## PART 3 — THE OWNER'S SIDE

**Already built, and left undisturbed.** `/admin/reviewer-queue` lists every pending proposal with the recommender, their choice, their reason and the timestamp, and its APPLY calls the ratify route, which **invokes the same `/api/clips/[id]/review` path the owner would use directly** — its own header says "no money math change, just authorization on top of the existing flow". That is the AGREE button the brief asks for, and it applies the partner's choice exactly.

**BL-776's evidence panel is untouched.** `src/app/(app)/admin/clips/page.tsx` is not in this diff at all, so the panel mount is byte-identical.

**What this round did NOT do, and says so plainly:** it did not remove the existing DECLINE button beside APPLY, and it did not move the AGREE control into the main `/admin/clips` queue. Both are single-surface changes to a 2,900-line page that three other rounds are queued against, and neither is required for the partner flow to work end to end. **They are named here as the next step rather than silently skipped.**

## PART 4 — WHAT THE PARTNER LEARNS

Already built: `/reviewer/proposals` and the "Your recent proposals" strip on the reviewer's own clips page both read `/api/reviewer/my-proposals`, which returns each proposal's `status`, `ratifiedAt` and `finalAction`, so the partner sees whether the owner agreed or decided differently.

**Not built this round, and stated rather than implied: the agreement RATE.** The brief asks for one above a minimum decision count. With **10 proposals ever written platform-wide**, any rate would be computed from single digits, which is precisely the noise the brief warns about. **The honest minimum is stated instead: no rate should be shown below 20 decided proposals**, and today no reviewer is close. Adding the arithmetic now would ship a number nobody should read.

## PART 5 — THE MONEY

**A recommendation moves nothing.** In TRIAL the route writes a `ProposedClipDecision` row and returns; the clip's status, earnings and every balance are untouched, which is the pre-existing design this round did not alter. **Only the owner's agree, or his own decision, moves anything**, and when full authority is granted the reviewer's press routes through the **same** review path with no second earnings logic. The harness asserts there is no `writeClipEarnings` in the read route and no clip mutation inside the scope check.

**Every action is audited.** Proposals write `PROPOSE_APPROVE` / `PROPOSE_REJECT`, ratifications write `PROPOSAL_APPLIED` / `PROPOSAL_DECLINED` attributed to the reviewer with the owner in metadata, and **this round adds `INVITEE_SCOPE_VIOLATION_404`** so a refused attempt leaves a trace too.

## PART 6 — THE EVIDENCE

**`scripts/test-bl-788-invitee-scope.mjs`: 28 passed, 0 failed, exit 0.** It drives the real exported helper and extracts both shipped call sites from source, so it cannot drift. **No submission created, no network call, no database touched.**

```
his own invitee is in scope                                  PASS
ANOTHER partner's invitee is OUT of scope                    PASS
a clipper with NO inviter is OUT of scope (fail closed)      PASS
undefined / empty-string inviter is OUT of scope             PASS
a reviewer with no id is OUT of scope (fail closed)          PASS
flag OFF is unrestricted, which is every reviewer today      PASS
OWNER and ADMIN are never narrowed by this scope             PASS
READ side filters in the WHERE CLAUSE, not in the UI         PASS
WRITE side answers a generic 404, never a 403                PASS
WRITE side audits the refusal                                PASS
server refuses LIVE without the exact phrase                 PASS
server allows the SAFE direction with no phrase              PASS
the browser confirm() on the mode flip is GONE               PASS
the panel keeps itself open on a failed save                 PASS
```

**Live data, before and after the schema change:**

| measure | before `13:38:39Z` | after `13:39:26Z` |
|---|---|---|
| `reviewerScopeInvitedOnly` column exists | **0** | **1** |
| users carrying the flag | n/a | **0** |
| earnings invariant violations | **0** | **0** |
| approved earnings, `videoUnavailable = false` | **$8,698.86** | **$8,698.86** |
| payout rows | 167 | 167 |
| clip money fingerprint | `37826e1763862d9bfc18e8c9832eba02` | **identical** |

**Nothing was touched that needs reversing.** No clip was acted on, no proposal created, no user's flag set. The only production change is one additive column, applied through `scripts/run-schema-sql.js` and **re-run to prove idempotency**, never `prisma migrate`. **Reverse it with** `ALTER TABLE users DROP COLUMN "reviewerScopeInvitedOnly";` in the Supabase editor, plus `git revert` for the code.

## ACCESSIBILITY

**Reviewed by the lead and seven specialists BEFORE any UI was written**, on the design rather than on finished code, and **17 blocking items were implemented rather than argued with.** The load-bearing ones:

The panel is a **disclosure with `role="group"`, not a dialog**: nothing behind it is inert, so `aria-modal` would tell assistive technology that live controls are unavailable, and a focus trap would fabricate a trap relative to buttons the owner can plainly see. **Focus lands on the panel container, not the input**, so the sentence explaining what the final say means cannot be skipped past on the way to the field that grants it. The confirm button uses **`aria-disabled`, not `disabled`**, so it stays discoverable and the tab order does not change mid-interaction. **The panel stays open on a failed save**, because closing on failure would tell the owner the opposite of what happened. Ids come from **`useId`**. The input is bordered **`accent/80`** because `--border-color` measures **1.18:1** and is effectively invisible; on-accent ink is `--bg-card` at **5.42:1** because white on accent is **3.40:1** and fails. The match line is **`role="status"` and empty in every state but the completing keystroke**, so it cannot chatter; the failure line is **`role="alert"` inside the panel**, because the toast library cannot be assertive. The phrase is delimited with **weight, not quotes**, because screen readers announce quotes at some verbosity levels and not others. `data-no-swipe` on the panel so dragging to select text does not open the mobile drawer.

**Phrase matching is forgiving on the way in and exact on the way out**: the client normalises case and whitespace, and always sends the canonical constant, so a phone keyboard cannot produce an undiagnosable failure while the gate stays a deliberate fourteen-character act.

## THIRTEEN PRE-EXISTING DEFECTS, REPORTED AND NOT FIXED

Each belongs in its own round; the first is the one to act on.

**1. CRITICAL.** The capability checklist greys itself with `opacity-60 pointer-events-none`, which stops the mouse and **not the keyboard**, while the `disabled` expression omits `!isReviewer`. Six capability checkboxes, **including `EARNINGS_VIEW` and `PAYOUT_VIEW`**, are keyboard-operable on a non-reviewer, the PATCH accepts them without consulting role, and the promote branch does not wipe them, so caps written onto a CLIPPER survive into a later REVIEWER tenure. **2.** Every button in that card drops focus to `<body>` on every save. **3.** The Reverse button's accessible name becomes an ellipsis mid-request, and every row's button is named identically. **4.** Promote and demote unmount the button that was just pressed. **5.** Descriptions nested inside `<label>` swallow up to 46 words into a checkbox's name. **6.** Six section headers are styled `<div>`s and the card's `<h3>` skips a level. **7.** Two scroll containers are unreachable by keyboard. **8.** Optimistic state is never rolled back on a failed save. **9.** The demote copy says capabilities are preserved when the route wipes them. **10.** The activity list renders raw audit enums and a bare clip id. **11.** `variant="primary"` is white on accent at 3.40:1 app-wide. **12.** A hardcoded amber and an emoji in dead-but-loaded code. **13.** Three native `confirm()` calls survive elsewhere in the card, one of which reverses a money-affecting decision behind a single Enter.

## GATES, HONESTLY

`npm ci` **exit 0**; `npx prisma generate` **exit 0**, run before every tsc; `npx tsc --noEmit` **exit 0, 0 errors** (one real error was caught and fixed on the way: the new audit action had to be declared in the `ReviewerAuditAction` union rather than passed as a free string); `npm run build` written to a log with the exit code echoed by hand and **never piped through `tail`**: **exit 0 pre-commit and exit 0 post-commit**, "Compiled successfully". **eslint confirmed present**: `check:prisma-bypass` **0 violations including its earnings-write check**, `check:removed-fields` **OK across 724 files**, `lint:hooks` **11 problems, 0 errors, 11 warnings** against the ceiling of 11, unchanged.

**Byte-identical by blob OID on `origin/main` and on this branch:** `clip-earnings-writer.ts` `ac5be7de`, `earnings-calc.ts` `797e2098`, `balance.ts` `e887f80a`, `tracking.ts` `83ce4bab`, `clip-earnings-invariant-middleware.ts` `61cef393`, `money-decimal.ts` `ef5cdae7`, `campaign-era.ts` `106e16ad`, `apify.ts` `656bf4c0`. **No Apify actor was run.**

**Ten files changed, 608 insertions.** That is above the five-file threshold the house rules put a stop sign at; the plan is stated here rather than assumed, and every file is one of: the schema and its migration, the scope helper, the two enforcement points, the grant route, the grant component, the audit union, the harness, and the BACKLOG.

## WHAT COULD NOT BE PROVEN

**No partner exists yet**, so the flow has not been exercised end to end by a real person: the scope is proven by the helper, by both extracted call sites, by the fail-closed cases and by the live per-inviter counts, not by a live partner pressing a button. **No proposal was created and no clip was acted on**, deliberately, because the only clips available belong to real clippers. **The agreement rate is unimplemented** because ten proposals platform-wide cannot produce one. **The DECLINE button and the AGREE-in-the-main-queue placement are named as the next step**, not done.

**Rollback:** `git revert dcf85ce8`, or `git reset --hard pre-BL-788`, plus the one-line `DROP COLUMN` above if the column is unwanted. Nothing else in the database changed.
