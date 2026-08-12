# BL-799 — the reviewer navigation fix, written this time, and the closed loop broken at both ends

**2026-08-12 · DB `now()` = `2026-08-12 17:42:08.149543+00` (first read) to `18:26:39.334968+00` (last) · BUILD.**
Branched from **`origin/checkpoint/BL-796`** @ `87d50ba3`, which carries **BL-794**, **BL-791**, **BL-790** and **BL-788** as ancestors. Branch `checkpoint/BL-799`, isolated worktree `C:/b799`, `node_modules` never junctioned, removed at the end. Every database read through `scripts/run-select.js`, every timestamp cast `::text` against DB `now()`. Handles redacted, no wallet address read or printed.

**BL-793 is NOT on this base and was NOT cherry-picked.** Its render fix is two layers and only one of them is code: layer one is operational (run `next dev`, which loads `.env.development.local` where `NEXT_PUBLIC_DEV_AUTH_BYPASS=true`; a production-mode run leaves the client flag false and the layout pushes to `/login`) and I reused that directly. Layer two is a three-line `useSession` to `useEffectiveSession` swap on `admin/users/[id]/page.tsx`, which is a page this round does not render, so it was not needed.

## THE FIRST LINE

> **The code is written and merged into a branch, and the navigation fix renders: a REVIEWER with `canActAsClipper` OFF now sees the full clipper navigation plus their own review section, proven in a real browser and by direct request against every route behind it. Rendering is PARTIAL and I am saying so: BL-793's blocker did NOT recur, but `resize_window` never changed the CSS viewport in this session, so only the desktop width was actually seen and the four narrow widths are not claimed.**

**Two things the brief did not anticipate, and both changed the work.** First, **the navigation was only half the defect** — eleven API routes gate on the same flag, so restoring the links alone would have produced menu items that return 403 or an empty array. Second, **merging the two navigations created five duplicate accessible names**, which the accessibility review caught before the edit and which is fixed in the same diff.

---

## PART 1 — THE FIX ITSELF, WRITTEN NOT SPECIFIED

### The full diff

```diff
   let sections: NavSection[];
   if (isReviewer) {
-    sections = buildReviewerNav(reviewerCapabilities ?? []);
-    // BL-129 (2026-06-06) — additive: a REVIEWER who also holds the
-    // canActAsClipper grant sees the standard clipper sections prepended
-    // to their reviewer nav. Both surfaces are reachable; nothing the
-    // reviewer already had is hidden.
-    if (canActAsClipper) {
-      sections = [...buildClipperNav(showMarketplace), ...sections];
-    }
+    // BL-799 (2026-08-12) — THE REVIEWER ROLE ADDS, IT NEVER REMOVES.
+    // This branch used to ASSIGN the reviewer nav over the top, so a
+    // partner lost Referrals, Earnings, Accounts, Payouts, Campaigns and
+    // clip submission unless a second flag (canActAsClipper) was set.
+    // Of 27 reviewers exactly 1 held it, and 24 had no referral code,
+    // which closed the loop: no code without the referrals page, no
+    // referrals page without the flag. A reviewer is still a clipper, so
+    // the clipper sections are now UNCONDITIONAL and the reviewer's own
+    // sections are appended under a "Review" heading. canActAsClipper is
+    // no longer read here; the grant path and the API gates still read it
+    // (see BL-799 report) so it is NOT deleted in this round.
+    sections = [
+      ...buildClipperNav(showMarketplace),
+      ...buildReviewerNav(reviewerCapabilities ?? []),
+    ];
   } else if (isClient) {
```

and, inside `buildReviewerNav` only, so **CLIPPER, ADMIN, OWNER and CLIENT navigation is byte-identical**:

```diff
-    return [{ items: [
-      { label: "Referrals", href: "/admin/referrals", ... } ] }];
+    return [{ title: "Review", items: [
+      { label: "Referral Manager", href: "/admin/referrals", ... } ] }];
...
-    { label: "Clips",     href: "/admin/clips", ... },
+    { label: "Review queue",     href: "/admin/clips", ... },
-  ... main.push({ label: "Campaigns", href: "/admin/campaigns", ... });
+  ... main.push({ label: "Review campaigns", href: "/admin/campaigns", ... });
-  ... main.push({ label: "Accounts",  href: "/admin/accounts", ... });
+  ... main.push({ label: "Review accounts",  href: "/admin/accounts", ... });
-  ... main.push({ label: "Payouts",   href: "/admin/payouts", ... });
+  ... main.push({ label: "Review payouts",   href: "/admin/payouts", ... });
-  ... main.push({ label: "Referrals", href: "/admin/referrals", ... });
+  ... main.push({ label: "Referral Manager", href: "/admin/referrals", ... });
-  return [{ items: main }];
+  return [{ title: "Review", items: main }];
```

**Why the labels changed, which was not in the brief.** The accessibility review measured the accessible name of each entry as exactly `item.label` (lucide-react marks its SVGs `aria-hidden`). Merging the two navigations put **five identical names on ten different destinations**: Clips, Campaigns, Accounts, Payouts and Referrals each existed in both lists. Two of those collide for **every** reviewer, because Clips is the universal capability floor. In NVDA's Insert+F7 links list or the VoiceOver rotor only the name is shown, stripped of surrounding context, so a reviewer would hear "Clips, Clips, Campaigns, Campaigns" with nothing to choose between them. That is **WCAG 2.4.4 Link Purpose (Level A)** and an inversion of **3.2.4 Consistent Identification (AA)**. Hrefs are untouched, so `key={item.href}`, BL-235's active-match logic and the owner-only badge lookup are all unaffected. The `title: "Review"` also flips the spacing rule at `sidebar.tsx:601` from `mt-1` to `mt-6`, which is what makes the boundary between the two navigations visible rather than merely present.

**Ordering was reviewed and deliberately left clipper-first.** Both builders return sections, and the one precedent already in the file (`REFERRAL_MANAGE` on a CLIPPER, `sidebar.tsx:372`) appends the elevated link after the personal ones. Reviewer-first would have given the platform two opposite orders for the same idea, and would have changed the navigation under the one reviewer who has the flag today, for no announced difference.

### THE NAVIGATION WAS ONLY HALF THE DEFECT

Restoring the links alone would have been a lie, and this is the part neither prior round found. **Eleven API routes gate on `canActAsClipperFromSession` / `canActAsClipperDb`** (`src/lib/clipper-access.ts`), and `api/earnings/route.ts:51` carries an inline copy of the same test. With the flag off, every one of those refuses a REVIEWER — so the restored menu items would have led to 403s and empty arrays. The chokepoint now treats REVIEWER as a clipper:

```diff
 export function canActAsClipperFromSession(session: SessionShape): boolean {
   const role = session?.user?.role;
-  if (role === "CLIPPER") return true;
+  if (role === "CLIPPER" || role === "REVIEWER") return true;
   return session?.user?.canActAsClipper === true;
 }
...
-    if ((u as any).role === "CLIPPER") return true;
+    if ((u as any).role === "CLIPPER" || (u as any).role === "REVIEWER") return true;
```

**FOUR SITES WERE DELIBERATELY NOT WIDENED, because they decide money or who gets emailed, and all four read the raw column rather than the helper:**

| site | what it decides | left alone because |
|---|---|---|
| `payouts/[id]/review/route.ts:525` | whether an inviter earns the **5%** | widening it would newly pay reviewers referral money |
| `referral-backfill.ts:124` | the same 5% on the backfill path | same |
| `growth/engine.ts:190` | **who receives marketing email** | widening it would newly email 27 reviewers |
| `gamification/route.ts:42` | the streak / level audience | not a navigation question |

### Proven by direct request, with the flag OFF

`dev-reviewer-001` is role `REVIEWER`, `canActAsClipper = false`, `reviewerScopeInvitedOnly = false` — exactly the population in question.

```
=== PART 1: CLIPPER SURFACES A REVIEWER MUST NOW REACH ===
REVIEWER /api/referrals           -> 200
REVIEWER /api/earnings            -> 200
REVIEWER /api/accounts/mine       -> 200
REVIEWER /api/payouts/mine        -> 200
REVIEWER /api/clips/mine          -> 200
REVIEWER /api/campaigns           -> 200
REVIEWER /api/gamification        -> 200

=== THE REFERRAL LINK ITSELF (must carry a real code) ===
{"referralCode":"4FT4CSLV","referralCount":0,"referralEarnings":0,...}

=== CLIP SUBMISSION GATE: must NOT be the permission refusal ===
{"error":"Campaign, account, and clip URL are required"}|HTTP=400
```

**The submission proof is the important one.** A 400 for missing fields means the request passed the permission gate and failed validation — the gate is open, and no clip was created to prove it. Before this change that same request returned the permission refusal.

### Is `canActAsClipper` now redundant? No, and it is not deleted

It is dead **only in the navigation**. Thirty sites still read it:

| file:line | what it does |
|---|---|
| `src/lib/clipper-access.ts:41,47,52,56` | the helper itself, both forms |
| `src/app/api/accounts/mine/route.ts:16` | own clip accounts |
| `src/app/api/clips/mine/route.ts:28` | own clips |
| `src/app/api/payouts/mine/route.ts:23` | own payouts |
| `src/app/api/clips/route.ts:729` | clip submission |
| `src/app/api/clips/batch/route.ts:51` · `batch/draft/route.ts:30` | batch submission |
| `src/app/api/clips/[id]/thumbnail/route.ts:36` | own clip thumbnail |
| `src/app/api/chat/campaign-chats/route.ts:30` | campaign chat as a clipper |
| `src/app/api/earnings/route.ts:45,52` | own earnings (inline copy) |
| **`src/app/api/payouts/[id]/review/route.ts:485,525`** | **the 5% referral mint — money** |
| **`src/lib/referral-backfill.ts:68,124`** | **the same 5% on backfill — money** |
| **`src/lib/growth/engine.ts:190`** | **the marketing-email audience** |
| `src/app/api/gamification/route.ts:42` | streak / level audience |
| `src/lib/auth.ts:678,718,811,862,972` | JWT + session surfacing |
| `src/components/layout/app-layout.tsx:243,244,844,865,894` | the prop and its three mounts |
| `prisma/schema.prisma:127` | the column |
| `scripts/backfill-lifecycle-state.ts:38` | a script audience |

Deleting it would silently change **who earns the 5%** and **who receives marketing email**. That is a separate decision and it is the owner's, not a side effect of a navigation fix.

**One harness now asserts the old behaviour and will fail**: `scripts/test-bl-129-recruiter-access.ts:106` asserts "REVIEWER + canActAsClipper prepends clipper nav sections". It is a string-matching harness, is not part of `npm run build`, and is reported rather than quietly edited.

---

## PART 2 — REFERRAL CODES FOR THE USERS WHO HAD NONE

### The loop, exactly

`ensureReferralCode` (`src/lib/referrals.ts:16`) had **exactly one caller in the entire product**: `GET /api/referrals` (`src/app/api/referrals/route.ts:147`). A code therefore existed only if the user had opened their own referrals page — the page the navigation defect hid from reviewers. **No code without the page, no page without the flag, no invitees without the code.**

### Both ends are now closed

**End one, the grant.** `PATCH /api/admin/users/[id]/reviewer-config` now issues the code at the moment someone becomes a reviewer:

```ts
if (isGrant) {
  try {
    const { ensureReferralCode } = await import("@/lib/referrals");
    await ensureReferralCode(id);
  } catch {
    // Non-fatal by design. A code failure must never fail a grant.
  }
}
```

It is idempotent (returns an existing code untouched), writes only `User.referralCode`, and **sets no referral relationship**, so no money is implicated.

**End two, the people already here.** `scripts/bl-799-backfill-referral-codes.js` uses the same alphabet and length as `generateCode()` at `referrals.ts:8`, so a backfilled code is indistinguishable from a minted one. The NULL guard lives in the `WHERE` clause, so a code that appears between the read and the write is never clobbered.

```
TARGETS: 1039 live users with no referralCode
BY ROLE: {"REVIEWER":11,"CLIPPER":1009,"CLIENT":19}
WROTE: 1039
FAILED: 0 []
```

### Platform-wide coverage, before and after

| measure | before (`17:42:08+00`) | after (`17:52:45+00`) |
|---|---|---|
| users with no code, **live** | **1,039** | **0** |
| users with no code, including soft-deleted | 1,073 | **34** |
| REVIEWERs with no code, live | 11 | **0** |
| distinct codes / users holding one | — | **1,356 / 1,356** (no collision) |

**The 34 who still do not have one are all soft-deleted, and that is deliberate.** `attachReferral` (`referrals.ts:47-53`) already refuses a soft-deleted inviter, so a code on those rows would be dead on arrival. Of the 24 reviewers reported without a code, 13 are in that soft-deleted set; the 11 live ones all have codes now.

### The 5% is real money, and it is unchanged

Referral earnings are computed from `referredById`, which this round never writes. Both fingerprints are **identical before and after**:

| fingerprint | before | after |
|---|---|---|
| `referral_commissions` (6 rows, **$109.57**) | `a04f63aa788d2a74fcfdca4c98980538` | `a04f63aa788d2a74fcfdca4c98980538` |
| referral graph (174 `referredById` edges) | `58dd8606c30ff0de47adb26ec202523c` | `58dd8606c30ff0de47adb26ec202523c` |

BL-563 and BL-570 both show how easily this arithmetic breaks, which is why the two mint gates were left reading the raw column rather than the widened helper.

---

## PART 3 — THE SIX OWNER SURFACES STAY REFUSED

Measured by direct request **after** the change, on the running server:

```
REVIEWER /api/payouts                   -> 403
REVIEWER /api/admin/agency-earnings     -> 403
REVIEWER /api/accounts                  -> 403
REVIEWER /api/admin/users               -> 403
REVIEWER /api/admin/payouts/unpaid      -> 403
REVIEWER /api/admin/audit-log           -> 403
REVIEWER /api/admin/reviewer-queue      -> 403
OWNER    /api/admin/reviewer-queue      -> 200
```

**Six for six, unchanged.** The owner control shows the surfaces are alive, not merely broken. Note `/api/accounts` (owner) stays 403 while `/api/accounts/mine` (the clipper's own) is now 200 — that pair is the whole distinction this round rests on.

### BL-788 and BL-790 both survive, each proven

```
=== BL-790 CAPABILITY GATE (six refusals, ride-along allowed) ===
TRACK_NOW       onto a CLIPPER -> 400      ANALYTICS_VIEW  onto a CLIPPER -> 400
CAMPAIGN_VIEW   onto a CLIPPER -> 400      EARNINGS_VIEW   onto a CLIPPER -> 400
ACCOUNT_VIEW    onto a CLIPPER -> 400      PAYOUT_VIEW     onto a CLIPPER -> 400
REFERRAL_MANAGE onto a CLIPPER -> 200      RESET []        onto a CLIPPER -> 200

=== BL-788 TYPED PHRASE (LIVE must refuse without the exact words) ===
mode=LIVE no phrase    -> 400
mode=LIVE wrong phrase -> 400

=== BL-788 INVITEE SCOPE: ON, queue must be EMPTY not an error, then OFF ===
queue size BEFORE       -> 73
PATCH invitedOnly=true  -> 200
queue size SCOPED       -> 0 | HTTP 200
PATCH invitedOnly=false -> 200
```

| protection | evidence |
|---|---|
| BL-788 invitee scope | 73 clips to **0** with the flag on |
| BL-788 **fail-closed** for a reviewer with no invitees | 0 at **HTTP 200**, an empty queue and not an error |
| BL-788 generic 404 on write | write-side gate at `clips/[id]/review/route.ts` unchanged in this diff |
| BL-788 typed FULL AUTHORITY phrase | LIVE refused with no phrase **and** with a wrong phrase |
| BL-790 server-side capability gate | six 400s, ride-along 200 |
| **a reviewer never reviews his own clip** | self-review block at `clips/[id]/review/route.ts:137-142`, not in this diff |

**Control, to show the change is reviewer-shaped and not a general widening:** a CLIPPER still gets 200 on `/api/referrals` and `/api/earnings`, and still 403 on `/api/payouts` and `/api/admin/users`.

---

## PART 4 — RENDERING: WHAT WAS SEEN, AND WHAT WAS NOT

**BL-793's blocker did not recur.** Running `next dev` (layer one) loaded `.env.development.local`, `/referrals` returned **HTTP 200** and `/admin/clips` returned **HTTP 200** as a REVIEWER, with no redirect to `/login`. Layer two, the `useSession` swap, applies to a page this round does not render.

**What failed instead is the viewport, and it is a different failure.** `resize_window` reported success at 1440, 1280, 375 and 414, but the page's own `window.innerWidth` never followed: it read **1568** through four resizes and then **1920**, while `window.outerWidth` sat at **160** throughout. The window object is not tracking the real geometry in this session, so the narrow widths were never actually rendered. **I claim no screen at 320, 375, 414 or 1280, and no mobile drawer.**

### What WAS seen, at the one width that worked

**The navigation, read out of the live DOM as a REVIEWER with the flag OFF** — 24 links across two mounts, zero duplicate names:

```
Campaigns -> /campaigns          Referrals -> /referrals
Clips -> /clips                  Payouts -> /payouts
Marketplace(Soon) -> /marketplace  Help -> /help
Accounts -> /accounts            [REVIEW]
Earnings -> /earnings            Review queue -> /admin/clips
Progress -> /progress            My proposals -> /reviewer/proposals
```

**The referrals page as a reviewer** rendered in full: the four stat cards (Clippers invited 0, Earned so far $0.00, Ready to cash out $0.00, Pending $0.00), the **working referral link** `…/login?ref=4FT4CSLV` with its Copy link button, and the "You earn 5% forever" / "They pay a 4% fee, not 9%" chips. **The `REVIEW` section heading renders below Help**, exactly as the accessibility review asked, with the wider `mt-6` gap separating it from the clipper block.

**The review queue as a reviewer** rendered at `/admin/clips`: the Clip Review heading, the search and status filter, and pending clip cards each carrying Approve / Ask owner / Reject / Flag. The sidebar shows Review queue highlighted **while the whole clipper navigation stays above it** — which is the entire point of the round, on screen.

**BL-776's evidence panel is intact**: `ReviewEvidencePanelMount` is imported at `admin/clips/page.tsx:23` and mounted at `:2050`, and the page renders 200.

---

## PART 5 — THE NAMED PARTNER

Handle redacted as **`tg…d7`**, user id `cmp9d0xu3000q…`.

| | before (`17:42:08+00`) | after (`18:26:39+00`) |
|---|---|---|
| role | REVIEWER | REVIEWER (unchanged) |
| `canActAsClipper` | **false** | **false** (unchanged, and no longer needed) |
| referral code | **none** | **issued** |
| referrals page | **not in his navigation** | **in his navigation, with a working link** |
| capabilities | `[]` | `[]` (unchanged) |
| review queue | Review queue + My proposals | **unchanged** — those two are the universal floor |
| `reviewerScopeInvitedOnly` | **false** | **false — NOT TOUCHED** |
| his invitees | 0 | 0 |

**He now has a referrals page and a working referral link**, which he could not previously obtain by any means: the code required the page and the page required a flag he does not have. His review queue behaves exactly as BL-788 built it, with capabilities untouched.

### The exposure, restated so it is not forgotten

**`reviewerScopeInvitedOnly` is OFF for him, and he has invited nobody.** At the last read there were **77 pending clips** on the platform and **0** of them came from anyone he invited. The figure four rounds have carried is **82 of 82**; the denominator has moved with normal traffic, the ratio has not — **every pending clip he can see belongs to someone who is not his invitee.** Switching the flag on would take his queue to zero, which is why it remains **the owner's decision**, deferred now for the fourth time rather than taken unilaterally on a paying partner's account.

---

## PART 6 — EVIDENCE, ROWS TOUCHED, AND REVERSAL

| claim | evidence |
|---|---|
| a reviewer without the flag reaches every clipper page | seven routes 200, submission gate returns 400 validation not 403 |
| the six owner surfaces still 403 | six 403s by direct request, owner control 200 |
| a user without a code now has one automatically | 1,039 written, 0 failed, **0 live users without a code** |
| the 5% is unchanged | `referral_commissions` md5 `a04f63aa…` and 174-edge graph md5 `58dd8606…` identical before and after |
| the partner before and after | table in PART 5 |
| the rendered screens | referrals page and review queue seen at desktop width; **narrow widths not claimed** |
| no payout touched | `payout_requests` md5 **`a263f1d784134c0a1712f38b076f147a`** identical before and after, 167 rows both times |
| the earnings invariant | **0 violations** before, **0 violations** after |

**One honest caveat on the clip fingerprint.** The whole-table clip fingerprint moved (`56196356…` to `d1aac896…`) because **4 clips arrived from live traffic during the round** (5,563 to 5,566 with 4 created after the start timestamp). Nothing in this diff writes a clip: no money file changed, `writeClipEarnings` is not called, and no route in the diff touches `Clip.status` or the three earnings columns. The payout fingerprint and the invariant are the clean measurements, and both are unchanged.

### Every real row touched, and how to reverse it

| rows | what changed | reversal |
|---|---|---|
| **1,039 users** | `"referralCode"` NULL to an 8-character code. **No other column.** No `referredById`, no money. | `node scripts/bl-799-backfill-referral-codes.js --revert` — it clears only rows still holding the exact code this run wrote |
| `dev-clipper-001` (synthetic) | capabilities PATCHed for the BL-790 proof | already reset to `[]` in the same run; verified `[]` |
| `dev-reviewer-001` (synthetic) | `reviewerScopeInvitedOnly` true then false | already reversed in the same run; verified `false` |

**The ledger is at `scripts/bl-799-referral-code-ledger.json` in the primary working tree and is deliberately NOT committed**, because it pairs 1,039 user ids with their codes and the repo is not the place for that. It must exist on disk for the revert to run.

### Gates, honestly

| check | result |
|---|---|
| `npx tsc --noEmit` | **0 errors**, exit 0, `grep -c "error TS"` = 0 |
| `npm run build` | **exit 0** read from `build.log`, "Compiled successfully in 54s" |
| BL-348 hooks gate | **0 errors, 11 warnings** — at the ceiling, unchanged. `node_modules/.bin/eslint` confirmed present first, so the gate did not silently no-op |
| 6 money files + `tracking.ts` + `campaign-era.ts` | **byte-identical by blob OID** against `origin/checkpoint/BL-796` |
| schema | **no change at all** |
| Apify | no actor run; the 11 BL-678 guards untouched |
| accessibility | reviewed **before** the edit; five duplicate accessible names found and fixed in the same diff |

**Rollback:** `git revert -m 1 <merge>` or `git reset --hard pre-BL-799`, then `node scripts/bl-799-backfill-referral-codes.js --revert` for the codes. The two are independent: reverting the code leaves the codes in place, which is harmless, since a code with no page is simply unused.

## WHAT THE OWNER SHOULD DECIDE NEXT

1. **`tg…d7`'s invitee scope flag**, deferred four times. On means his queue goes to zero today. Off means he reviews clips from people he did not invite.
2. **Whether `canActAsClipper` should be retired**, which is now only a money-and-email question: the 5% mint gates and the marketing audience are the only things that still turn on it.
3. **`scripts/test-bl-129-recruiter-access.ts:106`** asserts the old navigation behaviour and needs updating to match, or deleting.
4. **The narrow widths still have not been seen by anyone**, across seven rounds. The next round should render at 320, 375 and 414 with a working viewport before anything else is claimed about the mobile drawer.
