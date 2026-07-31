# BL-706 (ClippersHQ) — can any non-owner reach the backdating endpoint, and which path did the owner's own clips use?

## NO. No non-owner can reach it, by any route, and the data agrees: all 115 backdated clips in the database trace to 3 submitters and every one of them is role OWNER. The owner's own clips used BOTH paths, and the two that behaved differently went through the owner endpoint targeting himself, which is allowed because the CLIPPER-role check is skipped when the target is the submitter.

**READ ONLY. No code, data or config was changed and no submission of any kind was created.** Every database access was a `SELECT` through `scripts/run-select.js`, which refuses any write keyword. Every timestamp below is cast `::text` and reported against DB `now()`, which read **2026-07-31 17:26 to 17:29 UTC** across the queries. Handles and emails are redacted to 8-character reference prefixes. Base: `main` `0112361e`, worktree `C:/b706` at a short path, `node_modules` never junctioned. No UI code was written or modified, so there was nothing for an accessibility review to act on.

---

## PART 1 — the gate, verified independently rather than inherited

**`requireOwner` is defined at `src/lib/auth-guards.ts:90-97`** and is three checks in sequence:

```
90  export async function requireOwner(opts?: RoleOpts): Promise<AuthResult> {
91    const base = await requireNotBanned(opts);      // 401 if no session, 403 if banned
92    if (isAuthError(base)) return base;
93    if (base.role !== "OWNER") {
94      return { error: opts?.on403Role ?? default403Role() };   // 403
95    }
96    return base;
97  }
```

**Exactly one role satisfies it: `OWNER`.** The comparison is a strict inequality against a single string literal. There is no allow-list, no capability, no flag, and no test-user branch anywhere in the function or in the two it delegates to (`requireNotBanned:77`, `requireSession:62`).

**It is applied as the first statement of the handler**, `src/app/api/clips/owner-submit-bulk/route.ts:33`, before the request body is even parsed, with a custom 403 body of `"Owner only."`. The single-link sibling `src/app/api/clips/owner-submit/route.ts` is gated the same way. Neither route uses `requireOwnerOrCapability` (`auth-guards.ts:127`), which is the one function in that file that can admit a non-OWNER, so the REVIEWER capability carve-out is not in play here at all.

**Where `role` comes from, and whether anything else can set it.** `requireSession:70` reads `session.user.role`. That value is populated in `src/lib/auth.ts` from the database `User.role` column and nothing else: `:705` on first sign-in and `:790-812` on the 5-minute JWT refresh, both selecting `role` straight from the user row. The one branch that assigns `"OWNER"` without reading it, `auth.ts:694-703`, fires only when `dbUser.email === OWNER_EMAIL`, a single env-configured address, and it **writes `role: "OWNER"` into the database** as it goes, so it is a bootstrap for the configured owner identity rather than a session-only elevation.

**The three things the brief asked me to rule out, each checked:**

| candidate | verdict |
| --- | --- |
| `isTestUser` | Propagated to the token at `auth.ts:716` as its **own** field. It never touches `role`. `grep -c isTestUser` on `auth-guards.ts`, `get-session.ts` and `owner-submit-bulk/route.ts` returns **0** in all three. |
| `canActAsClipper` | Added by BL-129, carried at `auth.ts:718` and `:811` as its **own** field, and its own comment records that gates re-read the DB on mutation so a stale token cannot widen access. It never assigns `role`. |
| `reviewerCapabilities` / `reviewerMode` | Separate fields; only `requireOwnerOrCapability` consults them, and these routes do not call it. |

**The only non-database source of a role is the dev bypass, and it is double-gated shut in production.** `get-session.ts:69-77` will honour a `DEV_AUTH_COOKIE` naming any role including `OWNER`, but only when `isDevBypassEnabled()` returns true, and that function (`src/lib/dev-auth.ts:77-82`) requires **both** `process.env.NODE_ENV !== "production"` **and** `process.env.DEV_AUTH_BYPASS === "true"`. Production runs `next start` with `NODE_ENV=production`, so the first condition alone closes it; the local `.env` additionally carries `DEV_AUTH_BYPASS=false`.

> **Stated plainly: a clipper account with no owner role cannot reach `/api/clips/owner-submit-bulk` by any route.** Calling it directly with curl rather than through the UI changes nothing, because the gate is the first line of the server-side handler, not a client-side condition. The clipper gets `403 {"error":"Owner only."}`.

**The database agrees, independently of the code.** Of the **115** clips carrying `isOwnerOverride = true`, **114** have a matching `OWNER_OVERRIDE_SUBMIT` or `OWNER_SELF_SUBMIT` audit row, those rows name **3 distinct submitters**, and the count of distinct submitter roles is **1**, namely `OWNER`. The single clip without an audit row is `cmot0t4a` from **2026-05-05 19:27:43.866**, which predates the first `OWNER_OVERRIDE_SUBMIT` audit row ever written (**2026-05-11 19:04:29.671**), and it belongs to an OWNER account. **No non-owner has ever created a backdated clip.**

## PART 2 — which UI calls which endpoint

Each endpoint has **exactly one** caller in the whole of `src/`, and in every case the endpoint is a **hardcoded string literal**, never a computed or conditional value.

| submit surface | file:line | endpoint |
| --- | --- | --- |
| clipper single-submit modal | `src/app/(app)/clips/page.tsx:226` | `/api/clips` |
| batch rows inside that modal | `src/components/clips/BatchSubmitSection.tsx:251` | `/api/clips/batch` |
| owner submit page, single | `src/app/(app)/admin/submit-clip/page.tsx:154` | `/api/clips/owner-submit` |
| owner submit page, bulk | `src/app/(app)/admin/submit-clip/page.tsx:196` | `/api/clips/owner-submit-bulk` |

> **THE QUESTION THAT MATTERS, answered: NO. When the owner uses the ordinary clipper batch UI it calls `/api/clips/batch`, exactly like everyone else. No surface switches endpoint based on who is looking at it.**

The evidence is negative and complete. `BatchSubmitSection.tsx` contains **zero** references to `owner-submit`, and zero to `OWNER`, `isTestUser`, `canActAsClipper` or `session`; its only `role` matches are ARIA roles on presentational elements (`role="status"`, `role="group"`). `clips/page.tsx` likewise contains **zero** `owner-submit` references, and its single `OWNER` match is inside a comment. Neither file can route anywhere else, because neither contains the string.

**One nuance worth recording, because it is defence at the right layer rather than a hole.** The `/admin` layout (`src/app/(app)/admin/layout.tsx:44`) admits `OWNER`, `ADMIN` **and** `REVIEWER`, and `admin/submit-clip/page.tsx` carries no additional role gate of its own. So an ADMIN or REVIEWER can **load the owner submit page and see the form**. Every submission it attempts is refused by `requireOwner` with `403 "Owner only."`. The page is reachable; the endpoint is not.

## PART 3 — which path the owner's own clips actually used

**The discriminator, and one thing it cannot tell you.** `isOwnerOverride` is written `true` at exactly one place in the codebase, `src/lib/owner-submit-core.ts:276`, reached only from the two owner routes. The clipper core contains **0** occurrences of it (`grep -c` on `clipper-submit-core.ts`). The other `isOwnerOverride: true` hits across `src/` are all `select:` shapes, not writes. The two cores also differ in signature: the owner core writes `status: "APPROVED"`, `postedAt`, `overrideReason` and `createdAt = postedAt` (`:276-278`), while the clipper core writes none of those and leaves status at the schema default of PENDING (`clipper-submit-core.ts:474-478`).

**What cannot be recovered from the clips table, stated plainly rather than guessed.** Because the owner core sets `createdAt = postedAt` when a date is supplied (`owner-submit-core.ts:277`), the arithmetic `createdAt - postedAt` is **0.0 minutes by construction** on every backdated clip. The true wall-clock submission time is not in the clips row at all. It is recoverable from `audit_logs.createdAt`, which the core writes at `:363`, and that is what the table below uses.

**No separate clipper-role account exists for the owner.** Joining `users` to itself on shared email or shared `discordId` between an `OWNER` row and any other row returns **0 rows**. His clips sit on the OWNER accounts themselves. There are 3 OWNER accounts and they hold **8** clips between them.

| clip_ref | user_ref | status | `isOwnerOverride` | `createdAt` (::text) | `postedAt` (::text) | audit action | true submit time (::text) | path it came from |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cmrkgy76 | cmnd5tai | APPROVED | **true** | 2026-07-14 09:48:46.157 | **null** | `OWNER_SELF_SUBMIT` | 2026-07-14 09:48:46.341 | **owner endpoint, self-targeted, NOT backdated** |
| cmot0t4a | cmn4m6lh | APPROVED | **true** | 2026-05-05 19:27:43.866 | **null** | none (predates the action) | not recorded | **owner endpoint, self-targeted, NOT backdated** |
| cmovrbaa | cmn7d5hr | APPROVED | false | 2026-05-07 17:25:13.812 | null | none | 2026-05-07 17:25:13.812 | clipper path |
| cmovra3w | cmn7d5hr | APPROVED | false | 2026-05-07 17:24:18.871 | null | none | 2026-05-07 17:24:18.871 | clipper path |
| cmovlqdi | cmn7d5hr | APPROVED | false | 2026-05-07 14:49:00.128 | null | none | 2026-05-07 14:49:00.128 | clipper path |
| cmovl9p4 | cmn7d5hr | APPROVED | false | 2026-05-07 14:36:02.019 | null | none | 2026-05-07 14:36:02.019 | clipper path |
| cmovjam5 | cmn7d5hr | APPROVED | false | 2026-05-07 13:40:45.621 | null | none | 2026-05-07 13:40:45.621 | clipper path |
| cmovj49t | cmn7d5hr | REJECTED | false | 2026-05-07 13:35:49.679 | null | none | 2026-05-07 13:35:49.679 | clipper path |

**Age at submission for his own clips: not applicable.** All eight carry `postedAt = null`, so none was backdated and no post timestamp was ever supplied. The six clipper-path clips each have a first `ClipStat` written within 45 milliseconds of `createdAt` and one `TrackingJob`, which is the clipper core's signature; the two owner-endpoint clips have the same stat and job pattern but arrived already `APPROVED`.

**Why the self-submit was accepted at all, with the line that allows it.** `owner-submit-core.ts:87-88` reads `const effectiveUserId = targetUserId || ownerUserId;` then `if (targetUserId && targetUserId !== ownerUserId) {`, and only **inside** that block does it require `targetUser.role === "CLIPPER"` (`:91`). When the owner targets himself the condition is false and the whole block is skipped, so an OWNER-role account can be its own target even though an OWNER-role account can never be someone else's target.

**Where the backdating actually happened: on clips submitted FOR clippers, and it is still in active use.** The most recent `OWNER_OVERRIDE_SUBMIT` fired **today, 2026-07-31 14:00:41.8**, and backdated a clip to **2026-07-26T14:00:00.000Z**, five days earlier. A sample of the recent ten, all submitters role OWNER:

| true submit time (::text) | backdated to | submitter_ref |
| --- | --- | --- |
| 2026-07-31 14:00:41.8 | 2026-07-26T14:00:00.000Z | cmnd5tai |
| 2026-07-26 21:57:03.782 | 2026-07-25T21:56:00.000Z | cmnd5tai |
| 2026-07-26 18:08:31.28 | 2026-07-25T15:16:00.000Z | cmn4m6lh |
| 2026-07-26 18:06:20.521 | 2026-07-25T18:05:00.000Z | cmn4m6lh |
| 2026-07-26 18:05:25.925 | 2026-07-24T12:05:00.000Z | cmn4m6lh |
| 2026-07-25 12:53:58.142 | 2026-07-23T12:53:00.000Z | cmnd5tai |
| 2026-07-20 13:53:56.326 | 2026-07-18T13:48:00.000Z | cmn7d5hr |
| 2026-07-18 17:05:27.637 | 2026-07-15T17:04:00.000Z | cmn4m6lh |
| 2026-07-14 14:32:43.934 | 2026-07-13T14:32:00.000Z | cmn4m6lh |
| 2026-07-14 14:32:10.927 | 2026-07-13T14:32:00.000Z | cmn4m6lh |

This is also why those clips look old in any listing sorted by `createdAt`: a clip submitted today appears dated five days ago, because `createdAt` was overwritten with the backdate.

## PART 4 — every other clipper, last 30 days

**Population:** **106** distinct non-owner clippers submitted **1860** clipper-path clips (`isOwnerOverride = false`) in the 30 days to 2026-07-31 17:29 UTC.

**Coverage, stated plainly because it is a real limit on this measurement.** `clips.postedAt` is **NULL for all 1860** of them, so the clips table alone cannot date any non-owner submission. The only stored post timestamp is `rule_shadow_decisions.postedAt`, which the single-submit route writes and the batch route does not, and it is non-null for **98** clips, **5.3%** of the population. **For the remaining 1762 the age at submission is not determinable from stored data, and I am not going to guess it.** BL-704 closed the same gap for the batch path by probing 16 post-deploy Instagram clips live through HikerAPI and finding zero too old; this round is read-only against the database and did not repeat that probe.

**Of the 98 measurable, split at the BL-687 deploy (approximately 15:09 UTC on 2026-07-30):**

| era | clips | within 30 min | over 30 min | min age | max age |
| --- | --- | --- | --- | --- | --- |
| before the deploy | 29 | 27 | **2** | 0.7 min | 380.3 min |
| at or after 15:09:00 | 69 | 68 | **1** | 0.6 min | 39.1 min |

**Named in full, because the brief requires it. There are exactly three, and they are the same three BL-704 found:**

| user_ref | clip_ref | status | posted at (::text) | submitted at (::text) | age |
| --- | --- | --- | --- | --- | --- |
| cmpl310f | cms7fe9c | APPROVED | 2026-07-30 10:41:44 | 2026-07-30 11:23:58.303 | 42.2 min |
| cmpl310f | cms7iazr | APPROVED | 2026-07-30 06:25:08 | 2026-07-30 12:45:24.745 | 380.3 min |
| cms54yls | cms7ngev | APPROVED | 2026-07-30 14:30:27 | **2026-07-30 15:09:35.681** | 39.1 min |

All three are `isOwnerOverride = false` and all three carry a shadow row, so all three are **single-path clipper submissions**, not batch and not owner. The third is the boundary case BL-704 documented: BL-687's own report recorded a submission at **15:09:35.681** that was 39 minutes old and concluded the deploy had not yet swapped at that instant.

> **BL-704's finding still holds today, and is now stronger.** Restricting strictly to submissions **after 2026-07-30 15:09:35.681**: **68** measurable submissions from **16** distinct clippers across **25.5 hours** (2026-07-30 15:12:46.393 to 2026-07-31 16:45:22.826), **maximum age 26.9 minutes**, and **zero** over the 30-minute threshold. There has been no over-threshold non-owner acceptance since the deploy.

## PART 5 — the verdict

> **No non-owner can bypass the freshness rule: the backdating endpoint is closed to every role except OWNER, in code and in the data, and all 115 backdated clips in the database were submitted by an OWNER account.**

**Why the owner's own submissions behaved differently, in plain terms.** He was not using the clipper submit box for those. There is a separate owner-only page at `/admin/submit-clip` whose entire purpose is to enter clips that were posted earlier, and it calls its own endpoints. Those endpoints do not check the 30-minute window at all, because checking it would defeat the point of the tool. When he used that page, old clips were accepted. When he used the ordinary clipper box, the same 30-minute rule applied to him as to everyone else. Both are true at once, which is what made it look inconsistent.

**Is it by design? Yes, and no UI routes him there by accident.** The clipper submit box and the clipper batch rows call `/api/clips` and `/api/clips/batch` for every user, owner included, from hardcoded addresses that contain no role check. Nothing switches endpoint based on who is signed in. The owner reaches the backdating tool only by deliberately going to the owner submit page. The one thing worth his attention is that he can also point that tool **at his own account**, which is how his two odd clips (`cmrkgy76` and `cmot0t4a`) came to be marked as owner overrides. Neither was actually backdated, both have `postedAt = null`, so no date was moved on either; they were simply force-approved at submit rather than going through review, which is what that endpoint does.

**What it means for the clips he submitted that way.** They are flagged `isOwnerOverride = true` in the database, which is exactly what that flag is for: it records provenance, who pressed submit, and nothing more. It does not decide money. The clips he backdated for other clippers are also correctly flagged, and their `createdAt` was deliberately moved to the post date, which is why they read as older than they are in any list sorted by creation time. Nothing here is a bypass by a clipper, and nothing needs undoing.

---

## What was not determined

* **The age at submission of 1762 of the 1860 non-owner clipper-path clips**, 94.7% of the 30-day population, because no post timestamp is stored for them. Only the single-submit route writes one, and only on campaigns carrying rules. This is a measurement gap, not evidence of a problem; BL-704's live HikerAPI probe of the batch path found zero too old, and this round did not repeat it because it was read-only.
* **The true wall-clock submit time of `cmot0t4a`** (the owner's own 2026-05-05 clip), because it predates the `OWNER_OVERRIDE_SUBMIT` audit action and its `createdAt` is the only timestamp it has.
* **Whether any ADMIN or REVIEWER has ever loaded the owner submit page and been refused**, because a 403 leaves no database row.

**Read only. Nothing was changed, no submission was created, no build was run and none is claimed.** A markdown-only round cannot affect `tsc` or `next build`, and neither was executed.
