# BL-709 (ClippersHQ) — one named account is exempt from the 30-minute posting window, on the clipper paths only

## The exemption is a frozen constant list of database ids, consulted with the server's own `session.user.id`. Exactly one account of 1,289 qualifies, measured rather than asserted, and it can never be more than one because a primary key identifies at most one row. Only the freshness refusal is skipped: the core has 26 refusal gates and exactly 2 are guarded, both of them the same check. Nothing a client sends can reach the decision.

**Shipped** `checkpoint/BL-709` `09c55ef6`, merged to `main` **`501032b2`**, origin==local verified. Base `4b1d86aa`. Tags `pre-BL-709` / `post-BL-709` / `pre-merge-BL-709` / `post-merge-BL-709`, all pushed. Worktree `C:/b709`, short path, `node_modules` never junctioned. **One source file changed**, `src/lib/clipper-submit-core.ts`, 24 non-comment lines. **No schema change, no `prisma migrate`, no data change, no submission created.** The handle is redacted throughout; this report is public.

**Rollback:** `git revert -m 1 501032b2`, or `reset --hard pre-merge-BL-709`. Removing the exemption entirely is one line: empty the `FRESHNESS_EXEMPT_USER_IDS` array.

---

## PART 0 — the mechanism, and why the other two were rejected

**Chosen: a frozen constant array of user ids, keyed on the immutable primary key.**

| option | verdict |
|---|---|
| **(a) the OWNER role** | **Rejected, and it would not even work.** The account the owner named is role **CLIPPER**, verified by a read-only SELECT. A role check would not match it at all. Separately it would exempt every future owner account, when he asked for exactly one |
| **(b) a boolean column on the user** | **Rejected because it is WRITEABLE at runtime.** A column is precise, but any `db.user.update`, any future admin toggle, any backfill script could add a second exempt account with nobody reviewing it. It also needs schema this round is not entitled to |
| **(c) a frozen constant list of ids** | **Chosen.** It cannot be written to at all. Adding an account requires an edit, a review, a build and a deploy, which is the highest bar available and exactly the property the round needs |

**Why an id and not the handle.** `User.username` is changeable by its owner. A handle key would follow a rename onto a whole different person, or fall off this account silently, and either failure would be invisible. The database id is the primary key: immutable, unique by construction, and assigned by the database rather than by anything a client sends.

**What a future engineer needs to know**, stated in the code itself: the id belonged to the named handle when BL-709 resolved it on 2026-07-31; to move or remove the exemption, change that array and nothing else; there is no environment variable, no column, no admin screen and no request field that can alter it; verify a candidate id with a read-only SELECT on `users.id`, never by trusting a handle.

### Server-side identity only, which is the lesson of BL-708

The predicate is consulted with `userId`, and both routes take that from the server session:

* `src/app/api/clips/route.ts:814` passes `userId: session.user.id`
* `src/app/api/clips/batch/route.ts:72` sets `const userId = session.user.id;`

`grep -c` for `data.userId`, `body.userId` and `req.userId` returns **0** in both routes. There is no header, body field, query parameter or cookie on this path that can influence the decision. **BL-708 found the +2% PWA bonus granted off a client-sent `X-PWA-Mode` header; that is precisely the mistake this round was told not to repeat, and it is not repeated.**

## PART 1 — only the freshness age check is bypassed

`processClipperSubmitLink` contains **26** `return fail(...)` gates. Exactly **2** are now guarded by the exemption, and both are the same freshness refusal:

* `clipper-submit-core.ts:400` — TikTok and YouTube, via `provider-createdAt`
* `clipper-submit-core.ts:514` — Instagram, via `evaluateInstagramFreshness`

**The other 24 apply to the exempt account exactly as they do to everyone else:**

| # | check | still applies |
|---|---|---|
| 1 | clip URL is a string, non-empty, under 2000 chars | yes |
| 2 | note under 2000 chars | yes |
| 3 | URL starts `http://` or `https://` | yes |
| 4 | URL parses | yes |
| 5 | host is an allowed social host | yes |
| 6 | TikTok photo-carousel block, when carousels are disabled | yes |
| 7 | database available | yes |
| 8 | **clip account exists, is APPROVED and belongs to this user** | yes |
| 9 | **user has joined the campaign** | yes |
| 10 | campaign is not DRAFT or COMPLETED | yes |
| 11 | campaign is not a test campaign | yes |
| 12 | campaign is not archived | yes |
| 13 | campaign is not PAST | yes |
| 14 | campaign is not PAUSED | yes |
| 15 | **campaign budget not exceeded** | yes |
| 16 | **per-campaign per-day submission limit** | yes |
| 17 | **URL platform matches the selected account's platform** | yes |
| 18 | campaign platform allowlist | yes |
| 19 | per-platform CPM eligibility | yes |
| 20 | provider reported a bad URL | yes |
| 21 | unrecognised platform | yes |
| 22 | **duplicate on this campaign** | yes |
| 23 | **duplicate by this user on another campaign** | yes |
| 24 | P2002 unique-constraint catch | yes |
| **25, 26** | **the freshness refusal, TikTok/YouTube and Instagram** | **bypassed, for this one id only** |

**Scope is the two clipper routes and nothing else.** `processClipperSubmitLink` has exactly two callers in the repo, `clips/route.ts:813` and `batch/route.ts:160`, so the exemption reaches `/api/clips` and `/api/clips/batch` and cannot reach anything else. `/api/clips/owner-submit` and `/api/clips/owner-submit-bulk` call a different core (`owner-submit-core.ts`) and are untouched. The whole repository contains **6** references to the exemption and all six are inside `clipper-submit-core.ts`.

## PART 2 — it is loud when it fires

At the moment of acceptance a dedicated, greppable line is emitted. **The exact line, TikTok and YouTube branch:**

```
[FRESHNESS-EXEMPT] userId=<id> platform=<tiktok|youtube> source=provider-createdAt ageMs=<n> thresholdMs=1800000 accepted=true reason=BL-709-single-account-exemption
```

**Instagram branch**, which additionally carries the skew tolerance:

```
[FRESHNESS-EXEMPT] userId=<id> platform=instagram source=<s> ageMs=<n> thresholdMs=1800000 toleranceMs=<n> accepted=true reason=BL-709-single-account-exemption
```

The pre-existing `[FRESHNESS]` summary at `:531` now also carries ` exempt=true` and an honest `accepted=true` for that case, because printing `accepted=false` for a submission that was in fact accepted would make the record lie.

**The measurement is deliberately unchanged.** An exempt submission still records `outcome=too_old`. The exemption alters **acceptance** and never **what was measured**, so the age figure stays directly comparable across every account and a future audit can still count how many over-threshold clips were let through and to whom.

## PART 3 — nobody else gets it, measured

`scripts/test-bl-709-freshness-exempt.ts` drives the **real exported predicate**, not a copy. It creates no submission, writes nothing and calls no provider.

**The live population, queried at DB now() `2026-07-31 18:50:28.391864+00`:**

```
  users on the platform: 1289
  users whose id is in the exempt list: 1
    cmn4nlfg*** handle=dus*** role=CLIPPER status=ACTIVE isTestUser=false isDeleted=false
PASS  EXACTLY ONE account platform-wide satisfies the exemption  (of 1289 users)
PASS  that account is ACTIVE and not deleted
```

That is the intended account: role CLIPPER, active, not a test user, not deleted.

**Could it ever match more than one? No, and here is the reason rather than an assurance.** The list is a frozen array of **primary keys**, and a primary key identifies at most one row by definition. The only way a second account becomes exempt is if somebody edits the array and deploys. There is no wildcard, no prefix match, no pattern, and no runtime write path.

**Every other kind of account is still refused the same over-threshold clip:**

```
  an ordinary clipper      ageMs=5400000: outcome=too_old exempt=false refused=true
  a test user              ageMs=5400000: outcome=too_old exempt=false refused=true
  a reviewer               ageMs=5400000: outcome=too_old exempt=false refused=true
  an owner-role account    ageMs=5400000: outcome=too_old exempt=false refused=true
  the empty string         ageMs=5400000: outcome=too_old exempt=false refused=true
PASS  every non-listed account is STILL refused the same old clip
```

**No client-supplied shape can satisfy the predicate.** 17 hostile inputs were tried against the real function: the id with trailing and leading whitespace, the id upper-cased, the id truncated by one character, **the handle string itself**, `*`, `.*`, `%`, `null`, `undefined`, `0`, `1`, `true`, `{}`, `[]`, `[<id>]`, and an object whose `toString()` returns the id. **None matched.** Impersonation is closed at a different layer: the value is read from the server session, so there is nothing for a client to impersonate on this path.

## PART 4 — BL-686 is intact for everyone else

Driven through the **real exported** `evaluateInstagramFreshness`, which this round left byte-identical:

```
PASS  a genuinely old IG post is still too_old
PASS  a fresh IG post is fresh
PASS  a FUTURE-dated post accepts (clock skew never inverts)
PASS  just INSIDE the window plus tolerance still accepts
PASS  every unreadable timestamp shape is unknown, which ACCEPTS  (11 shapes, incl. the pre-2015 sanity floor)
```

The **skew tolerance** is untouched and still applied at the Instagram boundary. **Fail-open holds** on every unreadable shape: `null`, `undefined`, a number, a string, `{}`, a null / zero / negative / non-numeric / NaN `taken_at`, and a value below the 2015 sanity floor. **Future-dated posts accept**, so a clock disagreement can never invert into a refusal. The threshold is still read from `MAX_CLIP_AGE_MS` in `clip-config.ts`, which is **byte-identical** (`77e3fdfb`), and is never duplicated. **TikTok, Instagram and YouTube all still refuse a normal clipper**, proven above by the `refused=true` rows and by the unchanged `too_old` verdicts.

## PART 5 — the evidence

**Harness: 12 passed, 0 failed.**

* **The exempt account passes an over-threshold clip:** `outcome=too_old exempt=true refused=false` at `ageMs=5,400,000` against a threshold of `1,800,000`. Traced through the real predicate with no submission created.
* **Both paths:** `/api/clips` and `/api/clips/batch` call the identical core with the identical server-derived `userId`, so a single trace covers both by construction; the two call sites are `clips/route.ts:813` and `batch/route.ts:160`.
* **A normal clipper with the same old clip is still refused:** five different account shapes, all `refused=true`.
* **Exactly one account qualifies platform-wide:** 1 of 1,289.
* **No other validation is skipped:** 26 refusal gates, 2 guarded, the 24 listed above unaffected.
* **Nothing fires when the clip is fresh:** the exempt account with a fresh clip records `outcome=fresh`, no exemption line.
* **The log line appears**, quoted verbatim in PART 2.
* **No existing clip's status or earnings changed.** This round wrote nothing to the database at all; it is forward-only code.

## Gates, honestly

`npm ci` **exit 0**, then `npx prisma generate` **exit 0** before any typecheck, because `npm ci` wipes the generated client. `npx tsc --noEmit` **TSC_EXIT=0 with 0 output lines**. `npm run build` **BUILD_EXIT=0** on the branch and **again on the merged tree**, each read from a log with the exit code echoed directly, never through a pipe. Prebuild: BYPASS detector **0 violations**, removed-fields **OK**, **hooks gate 0 errors / 11 warnings** (limit 11) with eslint **v9.39.4** confirmed present so the gate ran rather than silently no-opping. 61/61 static pages. The real `.ts` diff was confirmed non-empty before any claim: **24 non-comment changed lines** in `clipper-submit-core.ts`. **No UI code was written, so no accessibility review was applicable.**

## Safety

6 money files plus `tracking.ts` and `campaign-era.ts` **byte-identical by blob OID** on both refs: `clip-earnings-writer.ts` 7aa6be48, `earnings-calc.ts` 797e2098, `balance.ts` e887f80a, `tracking.ts` 847dcf70, `clip-earnings-invariant-middleware.ts` 61cef393, `money-decimal.ts` ef5cdae7, `campaign-era.ts` 106e16ad. Also unchanged: `apify.ts` **656bf4c0**, so the BL-678 guards are intact and no Apify actor was run, and `clip-config.ts` **77e3fdfb**, so the threshold itself did not move. **Forward only:** no existing clip's status or earnings changed, no payout touched, no row written, no schema change, no `prisma migrate`, no env flag flipped. No heredocs; one shell at a time. NO dashes.

## One thing worth the owner knowing

This is the **first identity branch ever added to the clipper submit core**. BL-706 verified that the core previously contained zero references to `isTestUser`, `canActAsClipper`, `session`, `ADMIN` or any role value, which is why the freshness rule provably could not vary by account, and that property was worth something. It is now one named id narrower. The code says so loudly at the site, so the next person to read it knows the property is no longer free and that anything added to that array weakens it further.
