# BL-798 — the harm is smaller than it looked, and the build did not happen

**2026-08-12 · PART 4 ONLY. NO CODE WRITTEN, NO SCREEN RENDERED.**
Branched from **`origin/checkpoint/BL-796`**, which sits on BL-794, BL-791, BL-790 and BL-788. Worktree `C:/b798`, removed at the end. Reads through `scripts/run-select.js`, timestamps `::text`. **Nothing changed: no source file, no schema, no row, and the named partner's invitee scope flag was not touched.**

## THE FIRST LINE

> **The fix was not written and nothing was rendered, so I claim no screen and no landed change. I ran out of room in this session and I am saying so rather than shipping a half-applied navigation change to a live product. What I did establish is PART 4, the question of what the defect actually cost, and the answer materially shrinks it: NO reviewer was blocked from money they could have withdrawn.**

## PART 4 — WHAT IT COST, WHICH IS THE QUESTION THAT DECIDES THE URGENCY

BL-796 found 26 reviewers unable to reach their own clipper pages and flagged two of them as actively submitting clips. **The brief asked, correctly, whether that cost them real money or only navigation. Measured today:**

| reviewer | `canActAsClipper` | has referral code | clips submitted | approved earnings | payout requests |
|---|---|---|---|---|---|
| `cmovb0q6` | **false** | yes | 1 | **$0.00** | 0 |
| `cmpod0dh` | **false** | yes | 10 | **$1.32** | 0 |

**Neither holds a withdrawable balance.** The platform's payout minimum is $10, and the larger of the two figures is $1.32, so **there was no payout either of them could have requested and was prevented from requesting.** Neither has ever opened a payout request.

**The honest characterisation, then, sits between the two the brief offered.** It is **more** than missing navigation: BL-791 measured by direct request that a REVIEWER receives **403 on `/api/payouts` and on `/api/accounts`**, which are clipper-facing routes, so those pages were genuinely unreachable rather than merely unlinked. **But no money was unreachable**, because no affected reviewer had accumulated enough to withdraw. **It is a real defect with, so far, no financial victim.** That is worth stating precisely, because "26 reviewers lost access to their payouts" would have been true in shape and false in substance.

**What it did cost is the thing BL-796 named:** 24 of 27 reviewers hold no referral code, and the closed loop means they cannot obtain one, which is what actually blocks the partner arrangement.

## WHAT WAS NOT DONE

**The fix at `sidebar.tsx:337-347` was not written.** Referral-code issuance was not changed. No accessibility review was run, no build, no render, and **the dev-bypass page-guard blocker that has now stopped seven rounds is still unfixed.** No screenshot exists at any width and none is claimed.

**The specification in BL-796 stands unchanged and is what the next round should implement**, in this order: fix the page guard first so the work can be seen, make the reviewer navigation extend rather than replace, set `canActAsClipper` on the grant path, call `ensureReferralCode` on the same grant, then render at all five widths.

## THE THINGS THAT MUST NOT BE FORGOTTEN

**`tgsidd7`'s exposure is unchanged and untouched:** his invitee scope flag is still OFF and he can still see **all 82 pending clips from 27 clippers across 9 campaigns, 82 of 82 belonging to clippers he did not invite.** BL-794 and BL-796 both left that decision with the owner and this round did too. **It is the largest open item in this whole line of work and it is one flag.**

**Seven rounds have now delivered specifications instead of screens.** That is not a scheduling accident; the dev bypass reaches the API routes and not the page guard, and every round that plans to "prove it visually" will fail at the same place until someone fixes that first, before anything else.

**Rollback:** delete branch `checkpoint/BL-798`. It contains one document and touches nothing.
