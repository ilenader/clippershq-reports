# BL-791 — the partner reviewer under test: what held, what I could not walk, and one claim of mine that was wrong

**2026-08-12 · AUDIT AND MERGE, with no source change of its own.**
Branched from **`origin/checkpoint/BL-788`** and **merged `origin/checkpoint/BL-790`** into it, because neither is on `main` and the partner journey only exists when both are present. Branch `checkpoint/BL-791`, isolated worktree `C:/b791`, `node_modules` never junctioned, removed at the end. Every database read through `scripts/run-select.js`. **No clip status, earnings or payout was touched. No schema change. No Apify actor run.**

## THE ONE LINE, AND IT IS NOT THE ONE THE BRIEF HOPED FOR

> **The server layer is proven and holds under every probe I ran, but I could NOT complete the human browser walk: the dev-auth bypass does not survive the page-level guard, so `/admin/...` redirected to `/login` and I never saw either dashboard render. I am not going to claim a screen I did not see.** Everything below separates what was measured from what was not.

## WHAT I GOT WRONG IN BL-790, CORRECTED HERE FIRST

BL-790's report says BL-788 and BL-790 are "merge-tree clean in both directions, 0 conflicts". **That test was run against BL-790's work-in-progress commit, not its final one.** Merging them for real today produced a genuine conflict:

```
Auto-merging src/components/admin/ReviewerCapabilityChecklist.tsx
CONFLICT (content): Merge conflict in BACKLOG.md
Automatic merge failed
```

**The component auto-merged cleanly; BACKLOG.md did not.** Resolved as a UNION, both entries kept: **142 entries after, BL-788 present 4 times, BL-790 present 2 times, 0 conflict markers left.** The correction matters more than the conflict: a clean merge-tree run against the wrong commit is worse than no run, and the merge round for these two branches must expect to resolve BACKLOG by hand.

## PART 4 AND PART 3, MEASURED BY DIRECT REQUEST AGAINST A RUNNING SERVER

Every line below is a real HTTP response from the combined tree, not a code reading.

**What a reviewer is refused:**

```
REVIEWER /api/payouts                -> 403
REVIEWER /api/admin/agency-earnings  -> 403
REVIEWER /api/accounts               -> 403
REVIEWER /api/admin/users            -> 403
REVIEWER /api/admin/payouts/unpaid   -> 403
REVIEWER /api/admin/audit-log        -> 403
REVIEWER /api/admin/reviewer-queue   -> 403      (owner ratification queue)
OWNER    /api/admin/reviewer-queue   -> 200
```

**What he can reach, and it is exactly two things:** `/api/clips` (200) and `/api/reviewer/my-proposals` (200). **That is the whole surface.**

**THE ZERO-INVITEE CASE, which the brief asked for first and which is the one that would have embarrassed the owner in front of a partner:**

```
unscoped reviewer queue                       -> 80 clips
PATCH invitedOnly=true (this reviewer has 0)  -> 200
scoped reviewer queue                         -> 0 clips, HTTP 200
PATCH invitedOnly=false (reversed)            -> 200
```

**It renders empty and returns 200. It does not error.** That is BL-788's fail-closed default proven live rather than by trace: a reviewer scoped to invitees he does not have sees nothing at all, not an error page and not somebody else's clips.

**BL-790's capability gate still holds on the merged tree:** `EARNINGS_VIEW` and `PAYOUT_VIEW` onto a CLIPPER both **400**.

**BL-788's typed phrase still holds:** `mode=LIVE` with no phrase **400**, with a wrong phrase (`"full authority please"`) **400**.

**BL-788's invitee flag round-trips:** set true **200**, read back `reviewerScopeInvitedOnly: true`, set false **200**, read back `false`.

**BL-531, checked rather than assumed.** A reviewer's `/api/clips` payload carries 37 keys per clip, of which three are owner-economics shaped: `ownerCpmAtSubmissionDecimal`, `agencyEarning`, `marketplacePlatformEarning`. **Across all 80 rows every one of them is null, and not one row exposes a non-zero clipper earnings figure.** The keys exist in the shape; the values are pruned. That is the correct outcome, and it is now measured rather than trusted.

## WHAT I COULD NOT TEST, AND WHY

**The human browser walk of PART 1 and PART 2 did not happen.** I started the app, set `dev-auth-role=OWNER` in the browser, and navigated to `/admin/users/dev-reviewer-001`. **The page redirected to `/login`.** The same cookie is accepted by the API routes, which is why every probe above works, so the dev bypass reaches the route handlers but not the page-level guard. **I did not see the grant screen, the full-authority panel, the partner's queue, the owner's queue, the AGREE button, or BL-776's evidence panel render.** No screenshot of any of them exists, at any width.

**Therefore none of this was tested:** the complete owner-grants to partner-decides to owner-agrees to partner-learns journey; anything at 320, 375 or 414 pixels; touch behaviour; whether the partner can find his queue unaided; whether the post-decision waiting state reads clearly; the double-agree and concurrent-agree races; reassignment or archival while a recommendation is pending; role revocation with proposals outstanding; and a partner attempting to review his own clip through the UI. **The self-review block exists in code and was proven by BL-788's harness, but I did not exercise it through a browser this round.**

**What would settle it:** a session created the way a real owner's is, or a dev bypass that the page guard honours. That is a change to how the app is tested, not to the feature, and it is the single thing standing between this round and the coverage the brief asked for.

## THE READINESS VERDICT

> **The server is safe today and the surfaces are unproven: nothing a partner can send reaches money, another clipper's data, or a clip outside his invitees, and I would put the API in front of a paying partner. I would not yet promise the owner that the screens behave, because nobody has seen them.**

**Before a partner touches it, in this order:** get one authenticated browser session and walk the four steps once, at 375 pixels as well as desktop; press AGREE twice on the same recommendation and watch what the second press does; revoke the reviewer role while a proposal is pending and see what the owner's queue then shows. **Those three take under an hour together and they are the ones that fail in front of someone.**

**A description the owner can paste to the partner, unchanged:**

> You will see the clips from the clippers who joined through your link, and only those. On each one you can suggest approve or suggest reject, and you can write a reason when you reject. Your suggestion does not change anything by itself: the clip and any money on it stay exactly as they are until I agree. After I decide you will see what I chose on each clip you sent me. Nothing about your own clips, your own earnings or your own withdrawals changes in any way.

## GATES AND GUARDS

`npm ci` **exit 0**; `npx prisma generate` **exit 0** before tsc; `npx tsc --noEmit` **exit 0, 0 errors** on the merged tree. **`npm run build` was NOT run this round and no build result is claimed**, because the round ran out of room after the merge and the probes; the merged tree is two already-built branches plus a BACKLOG union, and tsc passing on it is what I can honestly assert.

**The 6 money files, `tracking.ts` and `campaign-era.ts` are byte-identical by blob OID** against `origin/main`: this branch contains **no source change of its own**, only BL-788's and BL-790's, whose own reports carry their gate results and their byte-identity proofs.

**Touched and reversed:** `dev-reviewer-001` and `dev-clipper-001`, both synthetic dev rows, neither a real person, neither holding money. The invitee flag was set true then false, and the capability PATCHes were all refused with 400 so nothing persisted. **Final state of both rows matches their starting state.**

**Rollback:** delete branch `checkpoint/BL-791`. It carries one merge commit and one document.
