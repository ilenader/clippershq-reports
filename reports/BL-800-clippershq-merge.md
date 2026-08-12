# BL-800 — the stacked chain, merged and re-proven on the merged tree

Eight branches merged into main one at a time in dependency order, with tsc and a full build run BETWEEN each so a break would be attributable to one branch rather than the pile. All eight green. Every protection re-proven ON THE MERGED TREE by direct request. Two things could not be proven that way and are named rather than claimed. One real side effect on the owner is reported in full.

## STEP 0 — the chain, mapped before anything was merged

Baseline recorded on a clean worktree BEFORE the first merge: **tsc 0 errors**, **build exit 0**, **hooks gate 0 errors / 11 warnings** with **eslint v9.39.4 confirmed present**, BACKLOG **677** entries.

| branch | SHA | ancestor of main? | source or docs | built on |
| --- | --- | --- | --- | --- |
| checkpoint/BL-788 | 7e57130c | NO, 2 commits ahead | SOURCE (6 src files, schema, 2 scripts) | main@72f05cec |
| checkpoint/BL-790 | 338ad3a5 | NO, 1 commit ahead | SOURCE (2 src files) | main@72f05cec, **not BL-788** |
| checkpoint/BL-791 | 3970ff7c | NO, 5 commits ahead | docs only in its OWN commit; carries 788+790 | merge of BL-790 into BL-788 |
| checkpoint/BL-793 | 89e3579b | NO, 6 commits ahead | SOURCE (5 src files) | **BL-791** |
| checkpoint/BL-794 | 9100adc6 | NO, 6 commits ahead | SOURCE (1 src file) | **BL-791** |
| checkpoint/BL-796 | 87d50ba3 | NO, 7 commits ahead | **DOCS ONLY — no src/, no prisma/** | BL-794 |
| checkpoint/BL-797 | 18ef695f | NO, 1 commit ahead | SOURCE (13 src files, schema, 5 SQL) | main@72f05cec, standalone |
| checkpoint/BL-799 | abe11484 | NO, 9 commits ahead | SOURCE (4 src files, 1 script) | BL-796 |

Local and origin were identical for all eight. **The chain is not what the brief assumed.** Every branch forks from `main@72f05cec`, not from `82ad9779`. BL-790 is a **sibling** of BL-788, not built on it. BL-793 and BL-794 are **siblings** off BL-791, so **BL-793 is NOT carried by BL-799** and needed its own merge — merging BL-799 alone would have silently dropped BL-793's four UI fixes and its render-blocker fix. Carried by a later merge: 788, 790, 791, 794, 796 all ride inside BL-799. Needing a separate merge: **BL-793** and **BL-797**. Every branch was nevertheless merged explicitly and in order, so that a build break would name one branch.

**BL-796 carries no source.** Its entire diff is `BACKLOG.md` plus its report, matching its own commit message ("specified rather than written"). The merge changed no file under `src/` or `prisma/`, verified by diffing the merge commit against its parent. This is the second time a branch in this family has been checked rather than assumed; unlike BL-778 it is not empty, it is real but docs-only.

**Commit 82ad9779 on main is genuinely docs only.** One new file, `reports/BL-799-clippershq-reviewer-nav-written.md`, 353 insertions and 0 deletions, no source. Left in place. It is byte-identical to the same file on `checkpoint/BL-799`, which is why the BL-799 merge produced no conflict on it.

**checkpoint/BL-723 was NOT merged**, as instructed.

## STEP 1 — eight merges, verified between each

| # | merge | conflicts | resolution | tsc | build | hooks |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | BL-788 | none | — | 0 | exit 0 | 0 err / 11 warn |
| 2 | BL-790 | BACKLOG.md, 1 hunk | UNION, both blocks kept | 0 | exit 0 | 0 / 11 |
| 3 | BL-791 | BACKLOG.md, 2 hunks | UNION | 0 | exit 0 | 0 / 11 |
| 4 | BL-793 | none (BACKLOG auto-merged) | — | 0 | exit 0 | 0 / 11 |
| 5 | BL-794 | BACKLOG.md, 1 hunk | UNION | 0 | exit 0 | 0 / 11 |
| 6 | BL-796 | none | — | 0 | exit 0 | 0 / 11 |
| 7 | BL-799 | none | — | 0 | exit 0 | 0 / 11 |
| 8 | BL-797 | BACKLOG.md, 1 hunk | UNION | 0 | exit 0 | 0 / 11 |

Every build exit code was echoed from the shell, never read through a pipe. `npm ci` first, then `npx prisma generate` before every tsc, and again after the two merges that touch `prisma/schema.prisma` (BL-788, BL-797), because `npm ci` wipes the generated client.

**BACKLOG counted, not truncated: 677 → 687**, which is exactly `677 + 2 + 1 + 1 + 1 + 1 + 1 + 1 + 2`. Counted with `grep -c`, never piped to `head`. Every one of BL-788, 790, 791, 793, 794, 796, 797, 799 appears exactly once. **0 conflict markers** anywhere in the tree, checked with `git grep` across all tracked files after every merge.

Two files are genuine three-way unions rather than any single branch's version, and both were checked marker by marker: `sidebar.tsx` (BL-793's footer pixel recovery + BL-799's nav fix + BL-797's Problem Reports entry, all three present) and `reviewer-config/route.ts` (BL-788 phrase + BL-790 capability gate + BL-793 + BL-794 scope-on-grant + BL-799 referral code on grant, all five present). Every other touched file is **byte-identical by blob OID** to the branch that last wrote it, so no merge silently rewrote anyone's work.

## STEP 2 — every protection re-proven by direct request on the merged tree

Proved by asking the running server, on the merged tree, with a real HTTP request. Not by reading code.

**Six owner-only surfaces — a REVIEWER is refused, and the routes are alive.** `/api/payouts`, `/api/admin/agency-earnings`, `/api/accounts`, `/api/admin/users`, `/api/admin/payouts/unpaid`, `/api/admin/audit-log` and the owner ratification queue `/api/admin/reviewer-queue`: **403, 403, 403, 403, 403, 403, 403** as a reviewer. The same seven as OWNER: **200 ×7**, which is the control that proves the 403s are refusals rather than broken routes. 14/14.

**All six capability checkboxes still gated server-side.** PATCHing `TRACK_NOW`, `CAMPAIGN_VIEW`, `ACCOUNT_VIEW`, `ANALYTICS_VIEW`, `EARNINGS_VIEW`, `PAYOUT_VIEW` onto a non-reviewer: **400 ×6**. The deliberate `REFERRAL_MANAGE` ride-along still **200**. Restore to `[]` **200**. 8/8.

**Full authority is off by default and behind the typed phrase.** `mode=LIVE` with no phrase → **400**. With the wrong phrase → **400**. `mode=TRIAL`, taking authority back, needs no phrase → **200**. 3/3.

**The invitee scope now defaults ON at grant time (BL-794's fix survived).** A fresh REVIEWER grant returns `reviewerScopeInvitedOnly` **true**. Demoting returns it **false**. 2/2.

**A reviewer without canActAsClipper reaches every clipper page (BL-799's fix survived).** `/api/referrals`, `/api/clips/mine`, `/api/earnings`, `/api/accounts/mine`, `/api/payouts/mine`, `/api/campaigns`: **200 ×6**, including Referrals, which is the page that mints the code and so breaks the closed loop BL-796 described. 6/6.

**Invitee scoping fails closed.** With the scope ON and zero invitees, the partner reads **0 clips at HTTP 200** — not an error, not a leak — against **78** pending clips from 18 distinct clippers with the scope off. The filter is a single WHERE clause on `user.referredById`, and a clipper with no inviter carries null and therefore never matches.

### The two things NOT proven by direct request, stated plainly

**The positive half of invitee scoping** — that a partner DOES see an invitee's clips — was not reachable. The only synthetic clipper available carries two clips that are **soft-deleted** (`isDeleted: true`), so they are invisible to every role including OWNER, proven by asking as OWNER and getting 0. Attributing a real clipper to the synthetic reviewer would write a referral attribution onto a real person, which BL-794 established is effectively permanent, so it was not done.

**The self-review block** — that a reviewer can never review his own clip — was not reachable either. The guard sits at `clips/[id]/review/route.ts:137-142`, but the re-action guard in front of it fires first: a synthetic clip moved into the reviewer's name is REJECTED, and the server answers `"Cannot review clip — already REJECTED"`. Reaching the self-review guard needs a PENDING clip authored by the reviewer, and making one PENDING would be a clip status change this round is forbidden to do.

For both, `clips/[id]/review/route.ts` and `clips/route.ts` are **byte-identical by blob OID to checkpoint/BL-799** on the merged tree, so no later merge could have undone either guard. That is an argument from the merge, not a fresh proof, and it is offered as exactly that.

### A finding: a comment in the grant path is wrong

`reviewer-config/route.ts:133-135` claims an explicit `invitedOnly:false` sent in the same PATCH as a REVIEWER grant still wins. **It does not.** Line 141 sets the flag true on the grant and line 238 only fires when the field is still `undefined`, so the grant's `true` survives. Proven by request: grant + `invitedOnly:false` returned the flag **true**. The behaviour is SAFER than the comment, so nothing was changed. The comment should be corrected in a later round. This is inherited from checkpoint/BL-794, not introduced by the merge.

## STEP 3 — the money and the counts

| measure | before (21:34 UTC) | after (22:27 UTC) | verdict |
| --- | --- | --- | --- |
| earnings invariant violations | 0 | **0** | holds |
| payout_requests | 167 | **167** | none created |
| last payout createdAt / updatedAt | 11:24:15 / 11:24:15 | **11:24:15 / 11:24:15** | none modified, approved or cancelled |
| payout_adjustments | 6 | **6** | untouched |
| referral_commissions | 6 rows, all rateBps **500**, $109.57 | 6 rows, all rateBps **500**, $109.57 | 5% unchanged |
| last referral commission | 2026-07-10 | **2026-07-10** | untouched by the 1,039 codes |
| conversations / escalated / people | 54 / 13 / 50 | **54 / 13 / 50** | matches exactly |
| problem_reports | 0 | **0** | no rows written |

**The 5% referral earning is unchanged after BL-799 issued codes to 1,039 users.** Three independent checks agree: every one of the 6 commission rows carries `rateBps 500`, the total is still $109.57 with the newest row dated a month ago, and `DEFAULT_REFERRAL_PERCENT = 5` in `earnings-calc.ts`, which is itself byte-identical. Minting a referral code is not attribution and did not move money: 174 users carry a `referredById`, and the two money paths that mint the 5% read the **raw** `canActAsClipper` column, not BL-799's widened helper, which the helper documents at `clipper-access.ts:47-52`. The rate was also visible on screen during the render pass.

**No clip's status or earnings changed by my hand.** 25 clip decisions did land in the window (approved 4471 → 4490, rejected 1015 → 1021, pending 91 → 66, earnings +$6.63). All 25 are in `audit_logs` and **all 25 are the real OWNER doing normal work**, none by any dev user. Total clip count 5583 unchanged.

**The 6 money files plus tracking.ts and campaign-era.ts are byte-identical by blob OID**, compared with `git show` on BOTH refs (82ad9779 and the merged HEAD). None of the seven appears in the merged diff at all. No Apify actor was run. No `prisma migrate`.

### A real side effect on the owner, reported in full

The render pass opened 30 browser contexts against the same production `DATABASE_URL` and exhausted the Postgres connection pool. Between **21:52 and 22:01** the real owner hit **6 `SERVER_ERROR` rows**, all pool exhaustion on read-only counts (`clip.count`, `payoutRequest.count`, `marketplaceStrike.count`, `scheduledCall.count`, one avatar fetch). No data changed and nothing was corrupted, but his session was degraded for about eight minutes and that is my doing. The dev server was killed as soon as it was spotted. Future render rounds must not drive a local dev server at the live database while the owner is working.

## STEP 4 — thirty screens, every one measured

Method is BL-793's: `next dev --webpack` (Turbopack was the blocker), the dev-auth cookie, and — this is what BL-799 was missing — the viewport set on the **browser context**, not by resizing a window. Every shot records the CSS viewport width the **page itself** reports.

**30 of 30 rendered at the exact asked width. No width could not be reached.**

| screen | 320 | 375 | 414 | 1280 | 1440 |
| --- | --- | --- | --- | --- | --- |
| reviewer navigation (drawer open below 1024) | seen | seen | seen | seen | seen |
| referrals page as a reviewer | seen | seen | seen | seen | seen |
| review queue | seen | seen | seen | seen | seen |
| problem-report entry | seen | seen | seen | seen | seen |
| problem-report form | seen | seen | seen | seen | seen |
| owner's report list | seen | seen | seen | seen | seen |

Every shot is gated on two conditions, not a fixed sleep: the brand-blue splash class `html.splash-mode` must be gone, and a screen-specific string must be on the page. An earlier pass produced a 1,420-character "render" of the splash screen; that is why the gate exists and why nothing here is claimed on a character count alone. Four cold-compile stragglers per pass were re-run individually until they rendered; the dev server also restarted itself once on a memory threshold and one navigation was reset, which was re-run.

The reviewer navigation at 375 shows **the full clipper nav including Referrals, Payouts, Earnings and Accounts, plus a REVIEW section carrying Review queue and My proposals** — BL-799's fix on screen, on a reviewer who does not hold `canActAsClipper`. BL-793's footer ships one line at every width. The referrals page shows "You earn 5% forever" and "They pay a 4% fee, not 9%". The problem-report form shows the one-way notice, the 2,000-character counter and the disabled Send button.

Two things worth the owner's attention from the render, neither of them regressions and neither changed: the mobile drawer trigger at `app-layout.tsx:1016` is an **icon-only button with no `aria-label`**, so it has no accessible name; and below 768px the chat launcher is `hidden md:flex`, so the only mobile entry is the bottom nav's Chat tab.

## AFTER THE PUSH — what the owner must do

**1. Redeploy. The problem-report feature does not work in production until you do.** BL-797 stated this and it still holds: the code is merged but the running instance is the old bundle.

**2. No schema needs applying, and this corrects the BL-797 merge commit message.** `problem_reports` **already exists** in production with all 21 columns matching the Prisma model, RLS on with zero policies as designed, and 0 rows. `reviewerScopeInvitedOnly`, `canActAsClipper`, `referralCode` and `referredById` are all present too. Nothing was applied by this round and nothing is waiting.

**3. The named partner's invitee scope flag — still off, still your call, now the fifth round to leave it to you.** He sees all pending clips and **82 of 82 are not his invitees** because he has none. He is in TRIAL, so his press writes a recommendation and leaves the clip PENDING. Turning the scope on gives him an empty queue until he opens his own Referrals page once and starts inviting; leaving it off continues platform-wide visibility. Not touched by this round.

**4. Three reviewers in LIVE mode, unscoped — also still your call.** Measured on the merged tree today: **27 reviewer rows, all 27 with the invitee scope OFF, 9 in LIVE mode and all 9 unscoped, and exactly 1 holding `canActAsClipper`.** The three BL-794 named have real invitees (27, 5 and 1) and are among the LIVE nine, so their press lands immediately on money-bearing clips they were never scoped to. BL-794's recommendation stands: scope them, urgently. Not touched by this round.

**5. Existing reviewers keep the old defaults.** BL-794's and BL-799's fixes fire on the **grant** path only, so all 27 people already holding the role are unchanged by design. Whether to re-grant or hand-set them is yours.

## Safety ledger

- 8 merges, `--no-ff`, dependency order, tsc and build between each. BL-723 not merged.
- BACKLOG unioned and counted: 677 → 687 → 688 with this round's entry. 0 conflict markers.
- 6 money files + `tracking.ts` + `campaign-era.ts` byte-identical by blob OID on both refs; none in the diff.
- No clip status or earnings changed by this round; no payout created, modified, approved or cancelled; invariant 0.
- No `prisma migrate`. No Apify actor. The 11 BL-678 guards untouched. No wallet address printed; handles redacted.
- Touched and reverted, named: `dev-clipper-001` and `dev-reviewer-001` (both synthetic), and one synthetic soft-deleted clip whose author was moved and moved back. Every field verified identical to its recorded original.
- **Rollback:** `git revert -m 1 <merge>` for any single branch, or reset main to tag `pre-BL-800`.
