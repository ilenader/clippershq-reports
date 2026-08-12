# BL-790 — the capability checkbox hole: reachable, persisting, and granting nothing

**2026-08-12 · DB `now()` = `2026-08-12 14:34:13.4414+00` before, `14:53:44.540699+00` after · BUILD.**
Base `origin/main` @ `72f05cec`, branch `checkpoint/BL-790`, isolated worktree `C:/bl790`, `node_modules` never junctioned, removed at the end. **No schema change. No clip status, earnings or payout touched. No Apify actor run.** Every read through `scripts/run-select.js`, every timestamp cast `::text` against DB `now()`. Handles redacted; ids truncated.

## THE FIRST LINE

> **NOBODY EVER GAINED ACCESS. Ticking one of the six boxes on a non-reviewer was reachable by keyboard and did persist, but it granted nothing**, because both runtime gates refuse a non-REVIEWER before they ever read the capability list. **No capability was wrongly held by anyone in production, then or now.**
>
> **What was real is staleness:** the demote path wipes capabilities and the promote path does not, so a key written onto a clipper would have come alive the day that person was made a reviewer, with nobody deciding it at that moment. **That is now refused at the server, and the control is now honest at the UI.**

## PART 0 — COSMETIC OR REAL, SETTLED PER CHECKBOX

**The two runtime gates, quoted.**

`src/lib/reviewer-capabilities.ts:114` — `hasCapability`:
```ts
if (user.role !== "REVIEWER") {
  if (key !== "REFERRAL_MANAGE") return false;
  ...
}
```
`src/lib/auth-guards.ts:142` — `requireOwnerOrCapability`, which refuses **before** it loads the array:
```ts
const referralRideAlong = capability === "REFERRAL_MANAGE" && !isReviewer;
if (!isReviewer && !referralRideAlong) return { error: ... 403 ... };
```

**Per checkbox, tested independently, with the surface each one governs:**

| capability | reachable by keyboard | persists on a non-reviewer | grants real access | the gate that refuses |
|---|---|---|---|---|
| `TRACK_NOW` | **yes** | **yes** | **NO** | `requireOwnerOrCapability` at `api/admin/clips/[id]/track-now/route.ts:57` |
| `CAMPAIGN_VIEW` | **yes** | **yes** | **NO** | `hasCapability` at `api/campaigns/route.ts:65` |
| `ACCOUNT_VIEW` | **yes** | **yes** | **NO** | `requireOwnerOrCapability` at `api/accounts/route.ts:25` |
| `ANALYTICS_VIEW` | **yes** | **yes** | **NO** | `hasCapability` at `api/clips/route.ts:86` |
| **`EARNINGS_VIEW`** | **yes** | **yes** | **NO** | `requireOwnerOrCapability` at `api/admin/agency-earnings/route.ts:16`, and `hasCapability` at `api/campaigns/route.ts:181` |
| **`PAYOUT_VIEW`** | **yes** | **yes** | **NO** | `requireOwnerOrCapability` at `api/payouts/route.ts:40` |

**Proven by direct request rather than by reading code**, against a running server, as a CLIPPER:

```
GET /api/payouts                as CLIPPER -> HTTP=403
GET /api/admin/agency-earnings  as CLIPPER -> HTTP=403
GET /api/accounts               as CLIPPER -> HTTP=403
```

**So the defect was reachability plus persistence, not privilege.** BL-788 called it critical on the strength of the keyboard reachability and was right to report it; this round establishes that the money surfaces were never open, which is the part that decides whether this is an incident.

## PART 1 — LIVE DATA: NOBODY HOLDS ANYTHING WRONG

Every user carrying any capability at all, at `2026-08-12 14:25:28.738814+00`, redacted:

| user | role | capabilities | mode | created |
|---|---|---|---|---|
| `cmoagb` | **REVIEWER** | `ANALYTICS_VIEW` | LIVE | 2026-04-22 19:34:04.602 |
| `cmovb0` | **REVIEWER** | `REFERRAL_MANAGE` | LIVE | 2026-05-07 09:49:07.335 |
| `dev-re` | **REVIEWER** | `CLIP_REVIEW` | LIVE | 2026-06-01 22:13:52.894 |
| `rwf2-1` x5 | **REVIEWER** | `CLIP_REVIEW` | LIVE | 2026-06-02 (test rows) |

**Eight rows, all of them REVIEWER. Not one non-reviewer holds a capability.** Nobody holds `EARNINGS_VIEW`, `PAYOUT_VIEW`, `PAYOUT_APPROVE` or `TAX_MANAGE` at all.

**One incidental finding worth recording:** six of the eight carry the string `CLIP_REVIEW`, which **is not a member of the valid capability set** (the real keys are `CLIP_VIEW`, `CLIP_APPROVE`, `CLIP_REJECT`). It matches nothing in `hasCapability`, so it is inert everywhere, and it is dev and test residue rather than a grant. It is left alone: deleting rows is not this round's business.

**This turns the round from an incident into a hardening job**, and the fix is written accordingly.

## PART 2 — THE FIX, AT BOTH LAYERS, SERVER FIRST

**SERVER — `src/app/api/admin/users/[id]/reviewer-config/route.ts`.** The capabilities branch accepted any valid key for any role. It now refuses to write a capability onto someone who will not hold the REVIEWER role when the request finishes:

```ts
const effectiveRole = typeof data.role === "string" ? data.role : (before as any).role;
if (effectiveRole !== "REVIEWER") {
  const rideAlong = new Set(["REFERRAL_MANAGE"]);
  const notAllowed = (...).filter((k) => !rideAlong.has(k));
  if (notAllowed.length > 0) return NextResponse.json({ error: "..." }, { status: 400 });
}
```

**The same rule for all six, not five of six.** The single exception is `REFERRAL_MANAGE`, which BL-205 deliberately designed to ride on top of any base role and which **both** runtime gates honour for a non-REVIEWER; refusing it here would break a live grant. **"Effective role" is the role AFTER this PATCH**, so promoting to REVIEWER and granting capabilities in one request still works.

**UI — `src/components/admin/ReviewerCapabilityChecklist.tsx`.** `pointer-events-none` is gone, so mouse and keyboard stop diverging. The six locked boxes **stay focusable and in the tab order**, carry `aria-disabled` so assistive technology announces "unavailable", and carry `aria-describedby` pointing at one short sentence per locked group. **Native `disabled` was deliberately not used for the role lock**, because BL-736 established that it drops blocked options out of Tab and out of form-field quick nav, leaving a screen reader user unaware the option exists. Native `disabled` keeps its three original cases untouched: the Basic floor, an in-flight save, and a not-wired key.

**The visible reason, inside each locked group rather than at the top of the card:**

> **Operational (locked)** · Locked until this user is a Reviewer. Use the **Make this user a Reviewer (starts in TRIAL)** button at the top of this card, then tick the boxes you want them to have.

It sits inside the group so it never contradicts the Basic group's "always granted to a reviewer" line two blocks above, and so it precedes exactly the controls it describes.

**Two things the accessibility review caught that the plan had wrong, both measured and both fixed.** Keeping `opacity-60` on an **ancestor** of a now-focusable input composites the focus ring as well, dropping the accent outline to **2.71:1** against a 3:1 requirement; the dimming therefore moved onto the input's **sibling** text div and the ring stays at **5.42:1**. And `preventDefault` in `onClick` **does not stop the write**: React synthesises `onChange` from the same click and queues it during extraction, before `onClick` runs, so the `onChange` guard is the load-bearing one and both shipped.

## PART 3 — BL-788 IS UNDISTURBED

**This round was built on `main`, not on top of BL-788**, which remains unmerged on its own branch. Its invitee scope, its generic 404 on write, its fail-closed default for a clipper with no inviter and its typed `FULL AUTHORITY` phrase are **not in this diff at all**, so nothing this round did can weaken them.

**They do not conflict, and that is tested rather than assumed.** Both rounds touch `reviewer-config/route.ts` and `ReviewerCapabilityChecklist.tsx`, so a clash was plausible:

```
git merge-tree --write-tree main origin/checkpoint/BL-788            exit 0
git merge-tree --write-tree origin/checkpoint/BL-788 checkpoint/BL-790  exit 0, CONFLICT count 0
```

**Both can land in either order.** The merge round should still re-run BL-788's harness afterwards, because a clean textual merge is not the same as a proven behavioural one, and BL-788's own 28-assertion harness is the thing that proves its four protections.

## PART 4 — THE EVIDENCE

**Six direct PATCHes, one per capability, onto a role=CLIPPER account, after the fix:**

```
TRACK_NOW      -> HTTP=400  "This person is a clipper, so these can only be given to a reviewer: TRACK_NOW..."
CAMPAIGN_VIEW  -> HTTP=400  ...
ACCOUNT_VIEW   -> HTTP=400  ...
ANALYTICS_VIEW -> HTTP=400  ...
EARNINGS_VIEW  -> HTTP=400  ...
PAYOUT_VIEW    -> HTTP=400  ...
```

**The deliberate ride-along still works, and was reversed in the same run:**

```
PATCH capabilities=["REFERRAL_MANAGE"] -> HTTP=200  reviewerCapabilities: ["REFERRAL_MANAGE"]
PATCH capabilities=[]                  -> HTTP=200  reviewerCapabilities: []
```

**Target state before and after the whole probe sequence, identical:**

```
{"user":{"id":"dev-clipper-001","role":"CLIPPER","reviewerCapabilities":[],"reviewerMode":"TRIAL", ...}}
```

**WHAT WAS TOUCHED AND HOW IT WAS REVERSED, named:** the probes PATCHed capabilities onto **`dev-clipper-001`**, a synthetic dev row with role CLIPPER that is not a real person, holds no money and was created by the dev-auth bootstrap in March. It was set back to `[]` in the same run, and the platform-wide capability fingerprint proves it: **`a452cb9ee0138b0fcd492350c7178113` before and after, identical.** No real user was touched, and no capability was granted to anybody.

**The database, before and after:**

| measure | before `14:34:13Z` | after `14:53:44Z` |
|---|---|---|
| earnings invariant violations | **0** | **0** |
| payout rows | **167** | **167** |
| capability fingerprint across every user | `a452cb9e…` | **identical** |
| approved earnings | $8,700.81 | $8,701.28 |

**The $0.47 difference is the ordinary tracking cron accruing views**, not this round: this round wrote nothing to any clip, and the two writes it did make were to a synthetic dev user's capability array, both reversed, as the identical capability fingerprint shows.

**BL-788's protections were not exercised here** because they are not on this branch. They are proven by BL-788's own harness, which the merge round must re-run.

## GATES, HONESTLY

`npm ci` **exit 0** (it had to be re-run once: an earlier stray `npx next dev` in the same worktree half-installed a different Next version and left `ENOTEMPTY` on `node_modules/next`, which is an environment mishap and not a repo fault, recorded rather than hidden); `npx prisma generate` **exit 0**, before every tsc; `npx tsc --noEmit` **exit 0, 0 errors**; `npm run build` written to a log with the exit code echoed by hand and **never piped through `tail`**: **BUILD_EXIT=0**, "Compiled successfully in 33.6s". **eslint confirmed present**: `check:prisma-bypass` **0 violations including its earnings-write check**, `check:removed-fields` **OK across 724 files**, `lint:hooks` **11 problems, 0 errors, 11 warnings** against the ceiling of 11, unchanged.

**Byte-identical by blob OID on `origin/main` and on this branch:** `clip-earnings-writer.ts` `ac5be7de`, `earnings-calc.ts` `797e2098`, `balance.ts` `e887f80a`, `tracking.ts` `83ce4bab`, `clip-earnings-invariant-middleware.ts` `61cef393`, `money-decimal.ts` `ef5cdae7`, `campaign-era.ts` `106e16ad`, `apify.ts` `656bf4c0`. **Two files changed, and no schema change at all.**

**The dev-auth bypass used for the probes was passed as a one-shot environment variable on the command line, not written into any file**, and the server was stopped afterwards. `.env.local` in the worktree carries **0** occurrences of `DEV_AUTH_BYPASS`, and the worktree is deleted.

## WHAT WAS NOT DONE

**The five recommended items from the accessibility review are reported, not fixed**, because each changes behaviour beyond this defect: `saving` in the native `disabled` expression still drops focus to `<body>` mid-save; the promote button still unmounts itself with nothing announced; the Basic group's three checkboxes still use native `disabled` and so are still absent from Tab, which is the same BL-736 pattern and must not be flipped until the guard shipped here is in place, because removing `disabled` there would make their `onChange` live; the campaign-scope list and the "view decided clips" checkbox carry `disabled={saving || !isReviewer}` and therefore have the **inverse** defect, vanishing from keyboard navigation entirely for a non-reviewer, **so after this round the card holds three different treatments of "unavailable"**, which is stated plainly rather than left to be discovered; and `globals.css` still has no `forced-colors` block, so under Windows Contrast Themes the word "(locked)" and the sentence are the only cues that survive.

**Also unfixed and reported:** the thirteen pre-existing defects BL-788 catalogued in this same component, including the demote copy that promises capabilities are preserved when the route wipes them.

**Rollback:** `git revert` this commit, or `git reset --hard pre-BL-790`. **Nothing in the database to undo.**
