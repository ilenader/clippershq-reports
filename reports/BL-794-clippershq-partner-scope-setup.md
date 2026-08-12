# BL-794 — four reviewers can see every pending clip on the platform, and the grant path is why

**2026-08-12 · DB `now()` = `2026-08-12 16:08:44.191984+00` · BUILD.**
Branched from **`origin/checkpoint/BL-791`**, which sits on BL-788 and BL-790. Worktree `C:/b794`, removed at the end. **No real user's role, scope flag or referral code was changed.** Every read through `scripts/run-select.js`, timestamps cast `::text`.

## THE FIRST LINE

> **`tgsidd7` can currently see all 82 pending clips, from 27 clippers, across 9 campaigns, and 82 of the 82 belong to clippers he did not invite, because he has invited nobody. And he is not alone: ALL 27 reviewer rows carry the invitee scope OFF, including three real reviewers with real invitees, of whom all three are in LIVE mode where their decision is final with no owner review.**
>
> **What he can DO with them is limited and that part is working as designed: `tgsidd7` is in TRIAL, so his press writes a recommendation and leaves the clip PENDING.** The three LIVE reviewers are the sharper problem, because their press lands immediately.

## PART 0 — THE EXPOSURE, MEASURED

| measure | value |
|---|---|
| pending or flagged clips his queue returns today | **82** |
| from how many distinct clippers | **27** |
| across how many campaigns | **9** |
| how many are NOT his invitees | **82 of 82** |
| his invitees | **0** |
| his mode | **TRIAL**, so a press leaves the clip PENDING and waits for the owner |
| his capabilities | **none** beyond the universal view, approve, reject floor |

**Every reviewer, redacted, ordered by invitees:**

| user | mode | scope on? | has invite code? | invitees |
|---|---|---|---|---|
| `cmoagb7e` | **LIVE** | **no** | yes | **27** |
| `cmovb0q6` | **LIVE** | **no** | yes | 5 |
| `cmpod0dh` | **LIVE** | **no** | yes | 1 |
| `cmp9d0xu` (tgsidd7) | TRIAL | **no** | **no** | 0 |
| 23 dev and test rows | mixed | no | no | 0 |

**Not one reviewer on the platform is scoped.** `cmoagb7e` is the one to look at first: LIVE mode, 27 invitees of his own, and full sight of all 82 pending clips with a press that takes effect immediately.

## PART 1 — THE OWNER'S CALL, WITH THE CONSEQUENCES

**Why the scope is off for this user: it is a defect, not a setting.** BL-788 added the column with a database default of `false` and the promote branch never set it, so **every reviewer granted since has started platform-wide by construction.** Nobody chose this.

| option | what it stops | what it costs |
|---|---|---|
| **A. Turn the scope ON for `tgsidd7` now** | ends his platform-wide visibility today | his queue reads **0 clips**, correctly and with a plain empty state, until he has invitees |
| **B. Leave it off until he has invitees** | nothing | a partner keeps seeing 82 clips from 27 clippers the owner did not intend to share |
| **C. Remove the reviewer role until he is set up** | ends it completely | he cannot review at all, and the role has to be granted again later |

**RECOMMENDED: A for `tgsidd7`, and A urgently for `cmoagb7e`, `cmovb0q6` and `cmpod0dh`.** An empty queue is a screen that says nothing to do; platform-wide sight of other clippers' clips is a disclosure the owner cannot take back. **For the three LIVE reviewers the case is stronger still, because they are not merely seeing those clips, they can decide them.** **It is the owner's call and this round did not make it: no real user's flag was changed.**

The change is one PATCH per person from the owner's own screen, and it is reversible in the same way.

## PART 2 — THE UNDERLYING DEFECT, FIXED

**Granting the reviewer role did NOT set the invitee scope.** Now it does, in `src/app/api/admin/users/[id]/reviewer-config/route.ts`, inside the existing role branch:

```ts
data.role = body.role;
if (body.role === "REVIEWER") {
  (data as any).reviewerScopeInvitedOnly = true;
}
```

**The safe direction is the default from now on.** An owner who deliberately wants a platform-wide reviewer can still say so: the `invitedOnly` branch runs after this one and fires only when the body carries the field, so an explicit `false` in the same PATCH still wins. **Existing reviewers are untouched**, because this fires only on a grant.

**Proven by direct request, not by reading code**, against a running server:

```
PATCH {"role":"REVIEWER"} on a synthetic clipper
  -> role REVIEWER, reviewerMode TRIAL, reviewerScopeInvitedOnly: TRUE
PATCH {"role":"CLIPPER"} to reverse
  -> role CLIPPER, reviewerScopeInvitedOnly: false
```

## PART 3 — THE REFERRAL LINK, WHICH EVERYTHING RESTS ON

**How a code is issued:** `ensureReferralCode` at `src/lib/referrals.ts:16` mints an eight-character code lazily, and its **only** caller is `GET /api/referrals` at `src/app/api/referrals/route.ts:147`. **So a user gets a code the first time they open their own Referrals page, and never before.**

**Why `tgsidd7` has none: he has never opened it.** He is far from alone: **317 users hold a code and 1,071 do not**, including **24 of the 27 users already holding the REVIEWER role**.

**How he gets one, and the owner cannot do it for him from an admin screen:** the partner signs in and opens his own **Referrals** page once. The code appears at that moment and his invite link is `https://clipershq.com/login?ref=<his code>`. **This round did not open that page on his behalf and did not mint a code for him**, because that writes to a real partner's account.

**Is the attribution permanent?** Effectively yes, with one owner-only exception. `attachReferral` in the same file sets `referredById` **only on an account that has none**, with the comment "never overwrite existing referral", so a joiner cannot be re-attributed by signing up again or by using a different link. The owner can reassign deliberately through `/admin/referral-override`, which stamps `referrerOverriddenBy` and `referrerOverriddenAt` so an override is always distinguishable from a natural referral. **And the link is nulled if the inviter's own account is deleted (`ON DELETE SET NULL`), which empties that partner's queue rather than widening anyone's.**

## PART 4 — THE CLIPPERS HE ALREADY WORKS WITH

**They will never appear as his invitees on their own.** Anyone who joined without his link carries a null or somebody else's `referredById`, and nothing in the signup path can retro-attribute them.

**The owner CAN attribute them by hand**, through `/admin/referral-override`, which is the same tool that stamps the override fields. **That matters a great deal for this arrangement**, because the partner is already working with people who signed up before he had a link: without the override his scoped queue stays empty even after he starts sharing the link, for exactly those clippers. **It also carries a money consequence the owner should weigh: `referredById` is the input that decides the 4% versus 9% platform fee**, so attributing a clipper is not only a visibility change.

## PART 5 — THE EVIDENCE

**Exposure before and after this round: unchanged at 82, deliberately.** This round fixed the grant path and did not flip any live person's flag, so `tgsidd7` still sees 82 today. **That is the owner's decision to make and PART 1 puts it to him.**

**A newly granted reviewer starts scoped:** proven above by direct PATCH, `reviewerScopeInvitedOnly: true` on grant.

**Every reviewer's scope state:** reported in full in PART 0. **27 rows, all currently false.**

**The four prior protections still hold** on this tree: BL-788's TRIAL mode leaves the clip PENDING (`tgsidd7` is in TRIAL and his press writes a proposal), the generic 404 on an out-of-scope write, the fail-closed default for a clipper with no inviter (BL-791 measured 0 scoped against 80 unscoped, HTTP 200), and BL-790's server-side capability gate. **This round changed one line inside a role branch and touched none of them.**

**Rows touched and reversed, named:** `dev-clipper-001`, a synthetic dev account holding no money, was promoted to REVIEWER and demoted back to CLIPPER in the same run; its final state is `role: CLIPPER, reviewerScopeInvitedOnly: false`, identical to its start. The grant also created one `ReviewerScopeCutoff` row, id `cmsqalirb0001zgw7tah202lz`, by the pre-existing BL-89 fresh-only default; it belongs to that dev row, is inert, and can be deleted in the Supabase editor if the owner wants the tidier state. **No real user, clip, earning or payout was touched.**

## GATES

`npm ci` **exit 0**; `npx prisma generate` **exit 0** before tsc; `npx tsc --noEmit` **exit 0, 0 errors**; `npm run build` from a log with the exit code echoed by hand, **never piped through `tail`**: **BUILD_EXIT=0**, "Compiled successfully in 51s". **eslint present**: `check:prisma-bypass` **0 violations**, `check:removed-fields` **OK across 724 files**, `lint:hooks` **11 problems, 0 errors, 11 warnings** at the ceiling. **One source file changed, no schema change, no Apify actor.** The **6 money files, `tracking.ts` and `campaign-era.ts` are byte-identical by blob OID**: none is in this diff.

**Rollback:** `git revert` the commit. Nothing in the database to undo beyond the one inert cutoff row named above.
