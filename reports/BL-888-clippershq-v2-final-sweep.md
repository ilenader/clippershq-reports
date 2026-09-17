# BL-888: the final sweep of marketplace v2, looked at whole for the first time

**UNREMOVABLE: three `audit_logs` rows naming sandbox clips remain (`MKT_V2_CLIP_APPROVED` x2, `MKT_V2_CLIP_REJECTED` x1, 16:55:18 to 16:55:38 UTC), because the audit table is deliberately append only and is not in the teardown ledger. One further clip row beyond the ledger's 91 disappeared in the teardown window and I could not recover which; see THE SANDBOX'S OWN HOLE below. Everything else this round created is gone: 91 of 91 recorded rows deleted, 0 remain, and 0 rows match `bl888sbx-` or `BL888-SANDBOX` anywhere.**

**NOTHING HAS EVER RUN IN PRODUCTION. EVERY PROOF BELOW IS A SANDBOX PROOF.** After teardown all four v2 tables hold zero rows: clips 0, posts 0, editor earnings 0, platform earnings 0. No editor has ever submitted a clip, no poster has ever posted one, no v2 money has ever moved.

## What the sweep found

**TWO SILENT DIVERGENCES, AND BOTH WERE THE SAME SHAPE: a value the code had already fetched and then never read.**

**ONE. THE GATE LIVED ON THE PAGE AND THE MONEY LIVES IN THE ROUTE.** All six v2 pages call `isMarketplaceVisibleForUser`. **Nine of the eleven v2 API routes did not**, including `/api/marketplace-v2/catalogue/[id]/post`, which mints a `Clip` and three money legs in one transaction. Measured rather than reasoned: a real clipper's token with `isTestUser` false was refused the page and **answered 201 by the route, creating an earning clip**. All nine now carry it, answering **404 and not 403** so the route's existence does not leak either. The fix is proved from both sides in the sweep: four v2 routes answer 404 to a non test user, and the same route answers 200 to a test user a moment later, so it is a gate and not a wall.

**TWO. `createV2Post` SELECTED `campaign.campaignType` AND NEVER READ IT.** Both poster reads filter `campaignType in (MARKETPLACE_ONLY, BOTH)`; the write did not. An owner who switched a campaign back to `NORMAL` removed it from the catalogue **and went on paying for posts from anybody holding the link, a bookmark or an open tab**. This is **the answer to BL-876 question 14, taken by doing it**: a new post is refused in a sentence, and work already done keeps earning, measured at 3 editor legs holding $135.00 unchanged across the switch. The cost is stated plainly in the code: a poster who made a clip and came back to paste the link in the minutes after the flip is refused and has done that work for nothing. The alternative was an owner whose own switch quietly did not work.

**ALL 27 OF BL-876'S OPEN QUESTIONS NOW HAVE THE CODE'S ANSWER ON RECORD.** 17 CHOSEN with the deciding line quoted, 7 DEFAULTED (nothing represents a decision; the behaviour is the sum of unrelated filters), 3 NOT ANSWERED. Question 11 is deliberately left open and says so in the schema; question 14 was defaulted and is now chosen.

**THE ACCESSIBILITY REVIEW FOUND 68, AND FOUR STOPPED A PERSON DEAD ON A MONEY SCREEN.** The reject dialog's over-length note made the form invalid while the only error string it could build described the *reason*, so the owner pressed the button and **nothing happened and nothing was said**, to anybody, sighted or not. The cashout dialog's validation branch **nulled the one region inside it that speaks** and moved no focus; its "you asked for more than you have" refusal did the same, so a refused withdrawal was silent and read as sent. The posting form drove **two controls from one error string**, so the account refusal rendered under the link box, marked the link invalid, and moved no focus. All four fixed, plus 15 of the 26 SERIOUS: four pages that had no title of their own, a heading that lived inside the loaded branch so a cold load had no `h1` at all and the focus effect fired against `null`, white on the accent fill at a measured **3.43:1** on three primary buttons, `truncate` on the only field that tells two queue rows apart, a link to `/admin/users/` with no id, and a money queue whose controls announced themselves unavailable without being unavailable.

**THE REVIEW'S MOST AGREED FINDING WAS FALSE.** Four independent reviewers reported `detail-client.tsx:92` toggling a plain space in a live region. The file already held a **literal U+00A0**, correct and invisible in a source read. It is now spelled as the escape so the next reader cannot repeat the mistake.

**FOUR OF THIS ROUND'S SIX FAILURES WERE THE MEASUREMENT, NOT THE THING MEASURED.** The state route wants its own vocabulary (`action: "in-progress"`, not a status name). A foreign-URL test pasted a URL nobody had posted, so no gate could fire and 201 was correct. A render asserted `resp.status()` on a page whose `notFound()` lands **after the shell has begun streaming**, so it answers **HTTP 200 while rendering the not found screen**, and that check failed all twenty shots on a gate that was working perfectly, and now reads what is on the screen. A fourth asserted the card's copy against the detail screen. Each is reported here because a round that hides them teaches the next round nothing.

**A NINTH GUARD CHECK WAS FOUND UNABLE TO FAIL, AND IT WAS THIS ROUND'S OWN.** The new guard's demonstration matched its tag anywhere in the output, and the guard prints `G1/G2:` in its own notes, so G1 and G2 passed whether or not the check fired. Tightened to the failure list, all four then failed one at a time, each naming itself, every file restored byte for byte and re-verified clean.

## What was run, and what it said

- **THE SWEEP: 59 passed, 0 failed**, third run. Run 1 was 44/2 and run 2 was 52/0; both failures in run 1 were my checks, fixed and reported above.
- **THE RENDERS: 20 of 20**, four v2 surfaces at 320, 375, 414, 1280 and 1440, against a production build with `DEV_AUTH_BYPASS=false` and a real minted `__Secure-authjs.session-token`. **Pan measured, not `scrollWidth`: 0 pixels at every width.** One `h1` per screen, 4 distinct titles, 0 dangling `aria-controls`, 0 duplicate ids, 0 controls still white on accent, 0 `var(--bg-page)`, and the gate refusing a real clipper on every one. First pass: 0 of 20, on my own two bad checks.
- **THE GUARDS: 13 of 13 prebuild checks pass**, plus the hooks gate at 0 errors and 11 warnings, at its ceiling. `check:v2-flag-gate` is new and wired in.
- **THE INVARIANTS: 0 violations across 10,225 clips**; no negative money anywhere; one editor leg per clip; both reconciliation forms found 0 leaks and 0 out of balance rows.
- **THE MONEY FILES: all seven byte-identical by blob OID**, before and after. `prisma/schema.prisma` untouched, no migration run, no schema change.
- **THE FINGERPRINTS: the payout fingerprint is identical** (`6d48cd5b...`) and `agency_earnings` is identical at 4,903.

## The sandbox's own hole, which matters more than anything it proved

**`clips.campaignId` AND `clips.userId` ARE `ON DELETE CASCADE`.** The teardown promises it "deletes every row named in the ledger and nothing else". **That promise is not enforceable while those cascades exist**, because deleting a sandbox campaign or user silently takes any clip attached to it. This round: the 91 ledger rows came out exactly, users reconciled to the row (1772 minus 18 equals 1754) and campaigns likewise (40 minus 6 equals 34), and **one clip row beyond the ledger disappeared**. The sweep had made both sandbox campaigns non test for **29 seconds**, which is the only window in which a real clip could have landed on one. No money moved, by three independent measures above. **A future round must not make a sandbox campaign non test, and teardown must delete leaf rows before their parents.**

## Left with counts, and why

- **THE L1 BUDGET LOCK SEES ONLY 45 CENTS OF EVERY V2 DOLLAR.** `clip-earnings-writer.ts:208` takes `delta` from `Clip.earnings`, which on a v2 clip is the poster's 45 percent. BL-876 PART 7.1 asked for the full gross. The cron path is covered by an independent per tick total; **every non tick writer is not**, so a campaign can be pushed past its budget by up to 55 percent of one increment while the lock reports a clean projection. NOT FIXED because the fix is inside a protected money file and this round's whole claim is that those seven files did not move.
- **A CONVERSION PRICES BOTH PARTIES WITH ZERO BONUSES**, `marketplace-v2-conversion.ts:278-279`, `as never` suppressing the type error that would have caught it. The owner's blast radius preview understates a bonused earner and the next tick rewrites it upward.
- **THE CLIPPER IS NEVER TOLD HE WAS WARNED.** The four strike notification bodies are built verbatim and **nobody calls them**, and no UI issues or revokes a strike at all.
- **THE THEFT SURFACE HAS NO DOOR**, and the editor is invisible on the owner's clips list because that branch still tests `isMarketplaceClip`, which a v2 clip carries as false by construction.
- **11 SERIOUS ACCESSIBILITY ITEMS REMAIN**, each with a line number in BACKLOG.md.

---

# THE LAUNCH BRIEFING, IN PLAIN WORDS

**Before anything: nothing here has ever run for a real person.** Every number in this report came from a sandbox that was built, measured and then destroyed. The marketplace tables are empty. The first real editor and the first real poster will be the first two people ever to use this.

**HOW TO OPEN IT, IN ORDER.**

1. **Leave the flag off and use your own account first.** You are OWNER, so every v2 screen already works for you without changing anything. Walk it once: make a campaign, set its type to "Two ways to earn", submit a clip as an editor, approve it, post it, and watch the money appear. If anything surprises you, stop here. Nothing has been promised to anybody yet.
2. **Turn on one campaign, not the platform.** Set one campaign's type to "Marketplace only" or "Two ways to earn". Leave `NEXT_PUBLIC_MARKETPLACE_ENABLED` off. Only you and accounts marked as test users can see any of it, and that is now true of the screens **and** the routes behind them, which it was not before this round.
3. **Invite ONE editor and TWO posters, and mark those three as test users.** Two posters, not one, because the thing most worth watching is two people earning from the same clip at the same time.
4. **Watch them for a full day before you widen it.** Then flip `NEXT_PUBLIC_MARKETPLACE_ENABLED` to true when you want everybody in. That one switch is the whole opening.

**WHAT TO WATCH ON DAY ONE.**

- **The three legs.** Every post should produce an editor row, a poster row and a platform row. If a post has fewer than three, stop the campaign and tell me. The platform's ten percent is a **residual**, so it absorbs the rounding; expect it to be a cent or two off exactly ten percent and that is correct.
- **The campaign's spend.** Marketplace money counts against the same budget as ordinary clips, and one popular clip with fifty posters can spend a lot quickly. **Watch the budget rather than the clip count**, and know the honest limit named above: the budget lock currently projects only the poster's share on writers other than the hourly tick, so it can let a campaign overshoot by part of one increment.
- **Whether anybody gets paid twice or not at all.** The reconciliation is already written and takes seconds. If the number of editor rows ever exceeds the number of posts, something is wrong.
- **Nothing else.** Do not judge the feature by how many clips get submitted on day one. Judge it by whether the money is right.

**WHAT TO TELL THE FIRST EDITOR, in his words not ours.** "Send me clips through the marketplace page instead of posting them yourself. If I approve one, anybody on the campaign can post it, and **you get 45 percent of what every one of those posts earns, forever, on top of whatever they earn**. You will not see who posted it, only how many people did. If I do not approve one you will get a reason in writing and you can send a fixed version."

**WHAT TO TELL THE FIRST POSTER.** "There is a list of clips other people have made. Pick one, post it to your own account, paste the link back, and **you earn 45 percent of what your post makes**. What other people's posts make does not change yours. You have thirty minutes from the moment your post goes live to paste the link. **Post it to your own account only**. Pasting somebody else's link is refused, and doing it deliberately is the one thing that gets you removed."

**HOW TO STOP IT, from gentlest to hardest.**

1. **One campaign:** change its type back to "Normal". Nobody can start a new post on it from that moment. **Everything already posted keeps earning to the end of the campaign**, and that is deliberate and it is this round's answer to the open question.
2. **Everybody at once:** set `NEXT_PUBLIC_MARKETPLACE_ENABLED` back to false. Every v2 screen and every v2 route goes back to answering "not found" for everyone except you and test users. No data is touched.
3. **One person:** issue a strike from the admin screen. Three inside ninety days bans him from ordinary posting for seven days. It is reversible, it lifts the moment you revoke it, and **his money stays his**. Be aware of the gap above: **he is not currently told**, so tell him yourself.
4. **The code:** `git revert` the merge commit. No schema changed, no migration ran and no data moved, so the revert is complete on its own.

**THE ONE THING I WOULD NOT DO.** Do not open this to everybody on the same day you open it to anybody. The two defects this round found were both invisible from the screens and both only showed up when somebody called the thing underneath them. Twelve rounds built this feature and this was the first time anyone looked at all of it at once; assume there is a thirteenth thing, and let three people find it before three hundred do.
