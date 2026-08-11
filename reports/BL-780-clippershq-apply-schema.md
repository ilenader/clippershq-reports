# BL-780 — the two SQL files APPLIED. The connect flow now has somewhere to write, and the team resolves.

**2026-08-11 · DB `now()` = `2026-08-11 20:40:04.481468+00` at the first read, `20:43:53.778416+00` at the last.**
Base `origin/main` @ `72f05cec` (BL-779's merge `499109a9` plus its report). Branch `checkpoint/BL-780`.
Isolated worktree `C:/bl780`, short path, `node_modules` never junctioned, **removed at the end**.
**No key, token or team id was logged, printed or committed.** Nothing was connected and nothing authorised.

## PART 0 — WHAT THE TWO FILES DO. Verified, not inherited from BL-777.

Both files are in the repo unchanged by this round (blob OID identical on `main` and on this branch).

| file | statements | creates | additive? | alters or drops? | writes data? | token column? |
|---|---|---|---|---|---|---|
| `scripts/migrations/BL-777-clip-account-provider-links.sql` | **4** | `clip_account_provider_links` (16 cols) + 3 indexes | yes, every non-identifier column nullable | **none** | **none** | **none** |
| `scripts/migrations/BL-773-clip-analytics-snapshots.sql` | **3** | `clip_analytics_snapshots` (20 cols) + 2 indexes | yes, all ten analytic fields nullable | **none** | **none** | **none** |

Between them: **2 `CREATE TABLE IF NOT EXISTS` and 5 `CREATE INDEX IF NOT EXISTS`, and nothing else.** No `ALTER`,
no `DROP`, no `INSERT`/`UPDATE`/`DELETE`. The only `drop` string in either file sits inside a comment stating the
rollback. This is not only a reading: `run-schema-sql.js` strips comments, hard-refuses those keyword shapes, and
then requires **every** statement to begin with an allowed verb, so a file containing anything else could not have
run at all. **NO TOKEN COLUMN, in either file**, which is the property BL-777 requires rather than an omission:
under bundle.social the vendor completes the OAuth and holds the credential, so there is nothing here to store.

**The one thing that touches an existing object, stated rather than buried:** BL-773's file declares
`FOREIGN KEY ("clipId") REFERENCES clips(id) ON DELETE CASCADE`. That constraint is defined **on the new table**.
It does not alter `clips`, which still has **57 columns**, and it writes no row. I judged that inside the rule
rather than a reason to stop, and it is reported here so the owner can disagree.

**Safe to run twice, proven by running them:** after the first apply, both files were run **twice more**. Every
run exited 0 with `All statements applied successfully` and no error and no skip message.

## PART 1 — THE BEFORE STATE, AND THE ROLLBACK, BOTH BEFORE THE WRITE

At `2026-08-11 20:40:04Z`, from `information_schema` and `to_regclass`, matching BL-779 exactly:

`to_regclass('public.clip_account_provider_links')` → **NULL**, `clip_analytics_snapshots` → **NULL**,
`information_schema.tables` rows for either → **0**, columns → **0**, indexes → **0**. `clip_account_connections`
(BL-723's legacy table) present. **88 tables in `public`.** So this was a create, not an unexpected alter.

**The exact rollback, printed before anything was applied:**

```sql
DROP TABLE IF EXISTS clip_analytics_snapshots;
DROP TABLE IF EXISTS clip_account_provider_links;
```

Dropping each table takes its indexes and its FK with it. **This must be run in the Supabase SQL editor**, because
`run-schema-sql.js` refuses `DROP TABLE` by design. Both tables are empty and read by nothing else, so it returns
the database to its 20:40 state exactly.

## PART 2 — APPLIED, IN THIS ORDER

**BL-777's file first, then BL-773's.** Neither references the other, so the order is a reading order rather than
a dependency, and I state that instead of inventing one: the link is what a clipper creates first, and a snapshot
cannot exist until an account is linked. It is also the order both BL-777 and BL-779 wrote down.

```
node scripts/run-schema-sql.js scripts/migrations/BL-777-clip-account-provider-links.sql
[schema-sql] Running 4 statement(s) against the database...
[schema-sql] All statements applied successfully.          SQL1_EXIT=0

node scripts/run-schema-sql.js scripts/migrations/BL-773-clip-analytics-snapshots.sql
[schema-sql] Running 3 statement(s) against the database...
[schema-sql] All statements applied successfully.          SQL2_EXIT=0
```

**Nothing errored and nothing was skipped as already-present** on the first run, which is consistent with both
tables having been absent. `npx prisma generate` **exit 0**. `npx tsc --noEmit` **exit 0, 0 errors**, against a
baseline measured on this same tree after `npm ci` (exit 0) — the source is byte-identical to `main`, so the
baseline and the result are the same measurement and I claim nothing more from it.

## PART 3 — IT LANDED, AND NOTHING ELSE MOVED

**Shape now in production**, from `information_schema.columns` (36 columns, exactly the two files):

`clip_account_provider_links` — `id text NOT NULL`, `clipAccountId text NOT NULL`, `userId text NOT NULL`,
`provider text NOT NULL`, `platform text NOT NULL`, `teamId text NULL`, `externalAccountId text NULL`,
`externalUsername text NULL`, `status text NOT NULL DEFAULT 'pending'`, `lastError text NULL`,
`startedAt timestamp(6) NOT NULL DEFAULT now()`, `connectedAt`/`lastCheckedAt`/`revokedAt timestamp(6) NULL`,
`createdAt`/`updatedAt timestamp(6) NOT NULL DEFAULT now()`.

`clip_analytics_snapshots` — `id text NOT NULL`, `clipId text NOT NULL`,
`capturedAt timestamp(3) NOT NULL DEFAULT CURRENT_TIMESTAMP`, `provider text NOT NULL`, `platform text NULL`,
`externalPostId text NULL`, `ok boolean NOT NULL DEFAULT true`, `errorCode text NULL`, the ten analytic fields all
**NULL** (`averageTimeWatchedSec`/`fullVideoWatchedRate`/`totalTimeWatchedSec double precision`,
`reach`/`videoViews`/`profileViews integer`, `impressionSources`/`audienceCountries`/`audienceGenders`/
`audienceAges jsonb`), `fieldStatus jsonb NOT NULL`, `rawPayload jsonb NULL`.

**7 indexes** (2 primary keys, 3 on links, 2 on snapshots), **1 FK** as written. **Both tables hold 0 rows.**
`public` tables **88 → 90**. **RLS: both new tables came up `rowsecurity = true` with 0 policies**, so the
deny-all posture holds across all 90 tables and needed no action.

**A schema addition should touch no row, and this one touched none.** Over the **5,470 clips that existed before
the write**, both fingerprints are byte-identical before and after:

| measure | before 20:40:37Z | after 20:43:53Z |
|---|---|---|
| clip money fingerprint (`id\|status\|earnings\|baseEarnings\|bonusAmount`) | `3ef74f78769226f402d1fa74ad656e45` | **same** |
| clip status fingerprint (`id\|status\|reviewedAt`) | `a62415978df83101072e3f814d6a5223` | **same** |
| payout fingerprint (`id\|status\|amount\|finalAmount\|actualPaidAmount\|updatedAt`) | `2edf145f667d2db92da1724432755c82` | **same** |
| invariant violations | **0** | **0** |
| approved earnings, `videoUnavailable = false` | **$8,651.01** | **$8,651.01** |
| payout rows / adjustments | 166 / 6 | 166 / 6 |

**The one honest difference:** total clips moved **5,470 → 5,471**, PENDING 59 → 60. That is **one ordinary
clipper submission**, `cmsp4lmwt00060xnte7mrkeoa`, created `20:41:37.853` with `earnings = 0`. Restricting every
fingerprint to clips created before `20:40:37.988` reproduces both hashes exactly, and in the same window **0
pre-existing clips were updated, 0 were reviewed, and 0 payout rows were created or modified.**

## PART 4 — HOW FAR THE FLOW CAN NOW GET

Read-only `GET` probes on the owner's real key. **No account was connected and nothing was authorised.**

| probe | result |
|---|---|
| `GET /api/v1/organization` | **200**, org `ClipperHQ`, `apiAccess: true`, `subscription: null`, `suspended: false`, `analyticsDisabled: false` |
| `GET /api/v1/team` | **200, `total: 1`** — the team exists, created `2026-08-11T20:21:45Z`. BL-777 saw `total: 0` |
| configured `BUNDLE_SOCIAL_TEAM_ID` vs that team | **matches**, so `isConnectConfigured()` is true for the first time |
| the team's `socialAccounts` | **`[]`** — nobody is connected |
| `GET /social-account/by-type?type=TIKTOK` | **400 `"Team does not have a Tiktok account"`** — no longer 404 "No team found", so the team resolves |

**The cap: 5 post imports per social account per month on the free tier**, confirmed on the vendor's own live
pricing page (**5 free / 100 / 500 / custom**) and **not** from any API field — the org returns
`monthlyImportLimitPerAccount: null`, meaning no org-level override, and no numeric cap is returned anywhere.
**It is per social ACCOUNT, not per organisation**, which BL-777's org-wide table did not capture. Against roughly
7 TikTok clips a month for an average clipper, **at most 5 of one clipper's clips can be captured this month**,
and a top clipper at ~19 loses the rest. `MONTHLY_CAPTURE_BUDGET` still defaults to **100** and counts **our own**
rows globally, so it will not stop the sixth import failing at the vendor: set `BUNDLE_SOCIAL_MONTHLY_CAPTURES=5`.

**What the clipper will now experience on Connect.** Accounts page, an APPROVED TikTok account, open the dialog:
he now sees the invitation copy and a **Link TikTok stats** button where BL-779 measured "This is not switched on
yet." He presses it, we ask the vendor for a URL and send him there in the same tab, he approves at TikTok, and on
return we ask the vendor what it actually holds. A pending row is now writable, so the attempt can complete.

**One defect the working team has just exposed, reported and NOT fixed because it is outside this round.** With a
real team the vendor answers **400** `"Team does not have a Tiktok account"`, where BL-777 could only ever observe
a 404. `src/lib/social-connect/bundle-social.ts:98` maps 404 to `no_account` and every other non-2xx to
`vendor_error`. So a clipper who presses **Cancel** on TikTok's screen returns to *"Something went wrong on our
side and nothing was linked"* instead of the calm *"Nothing was linked ... that is fine"* the flow was written
for, and his link row is stamped `error`. **Nothing is blocked and no money moves**; the fix is one branch:
treat a 400 whose message has that shape exactly as `no_account`.

**What the owner should watch for:** the first successful link writes one row to `clip_account_provider_links`
with `status = 'active'` and an `externalUsername`; if that handle does not match the clip account, the clipper is
shown both handles as plain facts. Then `/api/cron/tiktok-analytics-capture` — which requires `CRON_SECRET` and
**is still scheduled nowhere** — must be invoked for a single snapshot to exist at all.

## PART 5 — THE HONEST STATUS, IN ONE LINE

**The connect flow is now structurally complete and reachable — schema present, team resolving, `TEAM_ID`
matching — and it is NOT proven, because nobody has connected and no analytics field has ever been observed.**

**UNVERIFIED, explicitly:** no analytics field has ever been returned by this vendor, at any clip age, so all ten
remain untested; no link row has ever been written and no import has ever run; the cancel path will currently show
the wrong sentence (above); `BUNDLE_SOCIAL_TEAM_ID` is confirmed only in local `.env.local` and **whether Railway
carries it could not be checked from here**, so the owner must confirm it in Railway before messaging the clipper;
and the capture cron is scheduled nowhere. Only a real clipper connecting will settle any of it.

## GATES AND SAFETY

`npm ci` **exit 0**; `npx prisma generate` **exit 0** (run before every tsc, because `npm ci` wipes the client);
`npx tsc --noEmit` **exit 0, 0 errors**; `npm run build` written to a log with the exit code echoed by hand and
never piped through `tail`: **BUILD_EXIT=0**, "Compiled successfully in 53s". **eslint confirmed present** at
`node_modules/.bin/eslint`, so the hooks gate is not a silent no-op: `check:prisma-bypass` **0 violations**,
`check:removed-fields` **OK across 724 files**, `lint:hooks` **11 problems, 0 errors, 11 warnings** against
`--max-warnings 11`, unchanged from main and at the ceiling.

**Byte-identical by blob OID on `main` and on `checkpoint/BL-780`:** `clip-earnings-writer.ts` `ac5be7de`,
`earnings-calc.ts` `797e2098`, `balance.ts` `e887f80a`, `tracking.ts` `83ce4bab`,
`clip-earnings-invariant-middleware.ts` `61cef393`, `money-decimal.ts` `ef5cdae7`, `campaign-era.ts` `106e16ad`,
`apify.ts` `656bf4c0`. **No Apify actor was run** and `apify.ts`'s BL-678 guards are intact by that identity.
**No source file was changed this round at all**: the diff is `BACKLOG.md` and this report.

**Rollback:** `git revert <commit>` for the two documents, and the SQL rollback in PART 1 for the schema. They are
independent: reverting the commit does not drop the tables, and dropping the tables does not need the revert.
