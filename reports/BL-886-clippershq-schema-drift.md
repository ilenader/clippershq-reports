# BL-886 — the schema drift, investigated completely and then resolved

Merged `80dc012`. Branch `checkpoint/BL-886` at `3b4f1853`. Tags `pre-BL-886`, `pre-merge-BL-886`,
`post-BL-886`. Merge tree `d9ead799` equals the branch tree, so the branch build **is** the merge build.

**Model split.** Opus decided what each drift item is, wrote every statement that touched the
database, wrote the guard changes and this report, with no subagent between it and the source. One
Haiku retrieval agent ran the reference sweep; its findings are marked **READ** below and every one I
relied on I re-ran myself and marked **VERIFIED**. No subagent opened a database connection.

---

## PART 0 — the investigation, complete before a single statement ran

### The guard's real output, before anything changed

```
[DRIFT-CHECK] FAIL — 10 drift item(s) detected:
  [ORPHAN TABLE] 'announcement_recipients' exists in DB but not in schema.prisma
  [ORPHAN TABLE] 'announcements' exists in DB but not in schema.prisma
  [ORPHAN TABLE] 'clip_account_connections' exists in DB but not in schema.prisma
  [ORPHAN TABLE] 'creator_review_screenshots' exists in DB but not in schema.prisma
  [ORPHAN TABLE] 'creator_review_videos' exists in DB but not in schema.prisma
  [ORPHAN TABLE] 'creator_reviews' exists in DB but not in schema.prisma
  [ORPHAN TABLE] 'creator_scans' exists in DB but not in schema.prisma
  [ORPHAN COLUMN] users.onboardingWelcomeSeenAt exists in DB but not in schema.prisma
  [ORPHAN COLUMN] users.emailMarketingOptOut exists in DB but not in schema.prisma
  [ORPHAN COLUMN] marketplace_poster_listings.audienceCountries exists in DB but not in schema.prisma
```

### What it checks, and what it does NOT

It reads `information_schema.columns` and compares **table names** and **column names**, both
directions. That is all. **VERIFIED by reading all 275 lines of the script.** It does not look at:

| dimension | why it matters | the round that paid for it |
|---|---|---|
| **INDEXES, including every `@@unique`** | Prisma enforces uniqueness **not at all** at runtime | **BL-841 / BL-845** |
| foreign key `ON DELETE` | a cascade nobody declared erases data silently | BL-837 |
| CHECK constraints | Prisma cannot express them, so nothing can see them | BL-826 |
| column types, nullability | `Decimal` declared, `Float` stored, passes in silence | — |
| enums | `parseEnumNames` is called and its result **discarded** | — |

> **SO THE ROUND'S PREMISE NEEDS ONE CORRECTION.** "A drift guard is the thing that would have caught
> BL-841" is true of *a* drift guard and **was not true of this one**. It compared columns and
> stopped. That is exactly why BL-877 had to verify twenty indexes by hand. BL-886 extends it so the
> sentence becomes true.

### The ten items, investigated

Row counts and timestamps measured 2026-09-17 against DB `now()`. Reference counts are `grep -c`,
never piped to `head`. **All VERIFIED by me**; the migration column is READ from the retrieval agent
and then confirmed by me (all eight files exist on disk).

| # | item | kind | rows | refs | writers | first appeared | classification |
|---|---|---|---|---|---|---|---|
| 1 | `creator_scans` | table | **552**, newest **2026-09-17 07:35** | 11 | 1 (`creator-scan/scan.ts:151` INSERT) | BL-336 | **LIVE, written today** |
| 2 | `creator_reviews` | table | 1 | 13 | 1 | BL-336/340/345 | LIVE |
| 3 | `creator_review_videos` | table | 3 | 22 | 1 | BL-336/340 | LIVE |
| 4 | `creator_review_screenshots` | table | 0 | 11 | 2 (INSERT + DELETE) | BL-345 | LIVE |
| 5 | `announcements` | table | 0 | 46 | 2 (`announcements.ts:142,172`) | BL-414 | LIVE |
| 6 | `announcement_recipients` | table | 0 | 7 | 2 (`announcements.ts:192,208`) | BL-414 | LIVE |
| 7 | `clip_account_connections` | table | 0 | 4 | **0**, read only | no migration found | LIVE, read only |
| 8 | `users.emailMarketingOptOut` | column | **1752 rows, 0 true** | 7 | 1 (`email-marketing-optout.ts:24`) | BL-334 | LIVE |
| 9 | `users.onboardingWelcomeSeenAt` | column | 1129 set, newest 2026-07-14 | 7 | 1 (`onboarding/seen/route.ts:54`) | BL-322 | LIVE |
| 10 | `marketplace_poster_listings.audienceCountries` | column | 1 set | 16 | 1 (`listings/route.ts:651`) | BL-317 | LIVE |

> ### NOT ONE OF THE TEN IS A LEFTOVER.
>
> Every one of the seven tables has readers. Six of seven have writers. **`creator_scans` holds 552
> rows and was last written SIX HOURS before this round measured it.** A round that had tidied up
> "seven orphan tables" would have dropped a working feature's entire history.

**And the non-modelling is DELIBERATE, recorded in the code itself.**
`src/app/api/admin/clip-analytics/[clipId]/route.ts:39` says *"`clip_account_connections` is not
modelled in schema.prisma, so this is a [raw query]"*, and `src/lib/clip-analytics-capture.ts:222`
says it *"exists in the database but is NOT modelled in"* the schema. These tables are reached by raw
SQL by design, which is precisely why Prisma never declared them. **Declaring them would contradict a
decision the code records rather than resolve a mistake.**

**Does any of them hold data anybody would miss?** Yes: `creator_scans` (552 rows of a live scanning
feature), `creator_review_videos` (3), `creator_reviews` (1), `onboardingWelcomeSeenAt` (1,129 users)
and `audienceCountries` (1 listing). **Nothing was dropped.**

### The opposite direction — the one that cost money

Every table, column and declared uniqueness verified against `pg_index`, `pg_constraint` and
`information_schema` by `scripts/bl886-drift-audit.ts` (read only, one connection).

> ## URGENT, AND IT IS BL-841's DEFECT CLASS EXACTLY
>
> **`scheduled_calls (posterApplicationId)` is declared `@unique` at `schema.prisma:2000` and NO
> UNIQUE INDEX EXISTED IN POSTGRES.**
>
> That is the same shape BL-841 found and BL-845 had to apply by hand after proving two concurrent
> posts on one slot **both returned 201 and both earned**. Prisma's `@unique` enforces nothing at
> runtime. The code relies on the uniqueness: `schema.prisma:2035-2037` records that the application
> row is patched via the call's `posterApplicationId` in the same transaction.

| measured before acting | |
|---|---|
| `scheduled_calls` rows | 58 |
| rows with a non-null `posterApplicationId` | 1 |
| values appearing more than once | **0** |

**It had never been violated**, so the index could be created against clean data.

Everything else in that direction is clean: **140 declared uniqueness constraints, 1 missing.
0 missing tables. 0 missing columns. 0 NOT NULL mismatches** across 1,157 compared columns.

---

## PART 1 — what was done, and what was deliberately not

**ONE statement ran against the database, and its rollback was printed before it ran:**

```
ROLLBACK:  DROP INDEX IF EXISTS "ScheduledCall_posterApplicationId_key";

CREATE UNIQUE INDEX IF NOT EXISTS "ScheduledCall_posterApplicationId_key"
  ON scheduled_calls ("posterApplicationId")
```

Applied through `run-schema-sql.js`, the sanctioned path. **`prisma migrate` was not used**, which
BL-780 records as prod-fatal here against 25 hand-run migrations.

| | before | after |
|---|---|---|
| `scheduled_calls` rows | 58 | **58** |
| indexes on the table | 6 | **7** |
| the index, by name in `pg_index` | absent | **present, `indisunique = true`** |

**Three orphan columns resolved by DECLARING them**, which is the correct direction for anything
holding rows: `emailMarketingOptOut Boolean @default(false)` and `onboardingWelcomeSeenAt DateTime?`
on `User`, and `audienceCountries Json?` on `MarketplacePosterListing`. No database change of any
kind; the schema simply stopped disagreeing.

**Seven tables left exactly as they are**, allow-listed with reasons. **Nothing was dropped and no
unknown was guessed at.**

---

## PART 2 — the guard is wired

`check:schema-drift` is now the **twelfth guard in `prebuild`**. The allow-list names each exempted
table with its row count, its writer and its reason, and a `[STALE ALLOW LIST]` check fails the build
if an entry names a table that no longer exists **or one that has since been declared** — so **the
list can only shrink, and a new drift item still fails the build.**

The guard also now verifies declared uniqueness against `pg_index`:

```
[DRIFT-CHECK] OK — no drift between prisma/schema.prisma and DB. 100 tables, 1206 columns
and 140 declared uniqueness constraints verified; 7 raw-SQL-owned tables exempted by name
with a recorded reason.
```

### The demonstration: 7 of 7, one at a time, never sampled

| case | what was broken | the guard said |
|---|---|---|
| F1 | a declared `@unique` loses its index | `[MISSING UNIQUE INDEX] marketplace_v2_posts …` |
| F2 | a declared column vanishes from the DB | `[MISSING COLUMN] users.bl886DoesNotExist` |
| F3 | a declared table vanishes from the DB | `[MISSING TABLE] 'bl886_ghost_table'` |
| F4 | allow-list keeps a now-declared table | `[STALE ALLOW LIST] 'users' … is now declared` |
| F5 | allow-list keeps a non-existent table | `[STALE ALLOW LIST] 'bl886_never_existed' …` |
| **D1** | **a real table created in the database** | `[ORPHAN TABLE] 'bl886_orphan_demo'` |
| **D2** | **a real column added to `scheduled_calls`** | `[ORPHAN COLUMN] scheduled_calls.bl886OrphanCol` |

D1 and D2 ran real DDL and were undone with their exact inverses; `scheduled_calls` read **58 → 58**
either side, and the catalogue afterwards holds **0 tables and 0 columns** matching `bl886%`.

---

## PART 3 — every unique index the money paths assume, named from `pg_index`

| index | status |
|---|---|
| `marketplace_clip_posts_submissionId_platform_key` (platform, submissionId) | **UNIQUE, present** — this is the one BL-845 applied by hand |
| `uq_payout_open_per_user_campaign` (campaignId, userId) | **UNIQUE PARTIAL, present** — the one BL-882 relied on |
| `marketplace_clip_posts_clipId_key` | UNIQUE, present |
| `marketplace_v2_posts_clipid_key` | UNIQUE, present — one post per clip |
| `marketplace_v2_editor_earnings_clipid_key` | UNIQUE, present — one editor leg per clip |
| `marketplace_v2_platform_earnings_clipid_key` | UNIQUE, present |
| `marketplace_v2_poster_states_clip_poster_key` | UNIQUE, present |
| all marketplace v2 indexes | **28 across 6 tables, 10 of them UNIQUE** |

BL-877 verified twenty by hand because no guard could. All of them, plus BL-885's three, are present.

---

## PART 4 — what else the database and the code disagree about

**FOUR UNDECLARED CASCADES**, reported and deliberately not changed:

| foreign key | database | schema |
|---|---|---|
| `channel_read_status.channelId → channels` | **Cascade** | no relation declared |
| `channel_read_status.userId → users` | **Cascade** | no relation declared |
| `community_mutes.campaignId → campaigns` | **Cascade** | no relation declared |
| `community_mutes.userId → users` | **Cascade** | no relation declared |

Both tables **are** declared as models; only the relations are missing, so Prisma does not know these
rows vanish when a user or a campaign is deleted. That is BL-837's class. Changing a foreign key to
close a cosmetic gap is a worse trade than recording it, so it is recorded.

**One ON DELETE mismatch:** `clip_limit_overrides.createdById` is `NoAction` in the database and
`Restrict` in the schema. They differ only in when the check fires; nothing is at risk.

**Two closed — this round's own drift.** BL-885's SQL created foreign keys on
`marketplace_v2_strikes.issuedById` (`ON DELETE RESTRICT`) and `.revokedById` (`ON DELETE SET NULL`)
and its Prisma model never mentioned them. Both are declared now. The RESTRICT matters
operationally: **a user who has ever issued a warning cannot be deleted while it stands**, which is
correct and was nowhere on record.

**TEN CHECK CONSTRAINTS EXIST THAT PRISMA CANNOT EXPRESS AT ALL**, so no schema and no drift guard
will ever see them: `payout_amount_positive` (the one BL-826 found jamming a payout permanently at
$0.00, five identical failures), `clip_earnings_nonneg`, `clip_base_earnings_nonneg`,
`clip_bonus_amount_nonneg`, `campaign_budget_nonneg`, `mkt_creator_amount_nonneg`,
`mkt_platform_amount_nonneg`, `owner_referral_payments_amount_nonneg`,
`clip_limit_overrides_maxClipsPerDay_check`, `marketplace_chat_threads_canonical_order_check`.

**0 NOT NULL mismatches** across 1,157 compared columns.

---

## PART 5 — nothing real moved

**11 of 11 proof checks passed.** No sandbox row was created, because none was needed: every
measurement is a read of production state and the only write was one index.

| | |
|---|---|
| users / clips / campaigns / payouts | 1752 / 10213 / 34 / 248 |
| payout fingerprint | `4b25d9d0f438ee9ea763c5b6ce113b43` — **identical to BL-885's close** |
| clip fingerprint | `b9ed8c77d73944ec376dd1e01f2bcf30` — **identical to BL-885's close** |
| earnings invariant | **0 violations across 10,213 clips** |
| BL-627 no-overpayment | 0 negative anywhere, 0 non-positive payouts |
| BL-696 no-double-pay | 0 clips with two editor legs |
| BL-824 paid-is-final | **26 pairs, the same documented baseline** BL-885 measured; the payable-versus-lifetime difference, not a violation. This round added none. |
| BL-538 never-decrease | 0 rows |
| reconciliation, both forms | **0 leaks, 0 rows out of balance** |
| seven protected money files | **BYTE-IDENTICAL by blob OID on both refs** |

### Every prebuild guard

| guard | wired | result |
|---|---|---|
| `check:prisma-bypass` | yes | 0 violations |
| `check:removed-fields` | yes | OK |
| `check:event-wiring` | yes | 0 problems |
| `check:v2-leg-sync` | yes | OK, 3 documented opt-outs |
| `check:v2-editor-balance` | yes | 19 passed, 0 failed |
| `check:paid-is-final` | yes | 14 passed, 0 failed |
| `check:payout-snapshot` | yes | 9 passed, 0 failed |
| `check:css-tokens` | yes | 3 passed, 0 failed |
| `check:liability-rules` | yes | 13 passed, 0 failed |
| `check:v2-strike-sites` | yes | 16 passed, 0 failed |
| **`check:schema-drift`** | **yes — NEW, and the point of this round** | **OK, 140 uniqueness constraints verified** |
| `lint:hooks` | yes | 0 errors, 10 warnings (ceiling 11) |

**Every guard is now wired. There is no longer one the build does not run.**

---

## What still stands between the owner and a real editor using the marketplace

1. **BL-879's visibility gates are closed.** No editor can reach the v2 surfaces until they are opened.
2. **No campaign has a type set.** All 34 are `NORMAL`. At least one must be `BOTH` or `MARKETPLACE_ONLY`.
3. **A redeploy is owed** — BL-885's strike table is applied; the code that reads it shipped with that merge, and this round's schema and guard changes ship with this one.
4. **The strike window (90 days) and ban length (7 days)** are one-line constants in `marketplace-v2-strikes.ts`. BL-876 said the window is his call.
5. **Question 16** — whether a poster may see which other posters took the same clip.
6. **Question 14** — whether changing a campaign's type mid-flight is blocked or grandfathered.
7. **262 dangling `aria-controls` on `/admin/payouts`**, measured at five widths.
8. **The thirteen `admin/payouts` accessibility defects.**
9. **The 33 inert `bg-[var(--bg-page)]` sites**, still needing a real token and a visual review.
10. **`text-accent` fails 1.4.3 in the light theme, repo-wide.** `globals.css:102` documents it and ships `--link-text`, but CLAUDE.md mandates `font-bold text-accent` for money. **A rulebook conflict and his call.**
11. **No admin page sets a `<title>`** — 43 pages inherit one, a 2.4.2 failure, in tension with CLAUDE.md's "Tab title: just Clippers HQ".
12. **NEW: four undeclared `ON DELETE CASCADE` foreign keys** on `channel_read_status` and `community_mutes`, and **ten CHECK constraints no schema can express**. Neither blocks launch; both are now written down.

**Rollback:** revert the merge commit, then
`DROP INDEX IF EXISTS "ScheduledCall_posterApplicationId_key"`. That returns the database to the
state measured at the start of this round, loses no data, and restores only the disagreement.
