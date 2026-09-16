# BL-877 — marketplace v2, the money foundation, entirely invisible

> **NOTHING IS UNREMOVABLE AND NO SQL IS OWED. FIRST LINE, AS THE ROUND REQUIRES.**
> 205 ledgered rows, **`VERIFIED: 0 of 205 recorded rows remain`**, 0 failed, 0 cascaded. A direct
> catalogue sweep after teardown returns **zero** `bl877sbx-` rows in `users`, `campaigns`, `clips`,
> `clip_accounts`, `audit_logs`, `activity_events` and `notifications`, **zero** rows in all four new
> v2 tables, and **zero** clips carrying `marketplaceV2PostId`. Nothing was left behind and there is
> nothing for the owner to run.

**2026-09-16. Shipped on `checkpoint/BL-877`, merged to `main`. Requires a Railway REDEPLOY** for the
`balance.ts` aggregate to take effect in production. Base `origin/main` @ `8dcc0c02`. Isolated
worktree `C:\w\b877`, a short path, `node_modules` never junctioned, **removed at the end and
verified by listing the path**. DB `now()` **12:59:59.999427+00** (opening census) to
**13:11:32.932778+00** (closing census), every timestamp cast `::text`.

---

## THE HEADLINE

> **1. THE ONE LINE THAT MATTERED MOST IS CLOSED, AND THE FAILURE WAS DEMONSTRATED BEFORE THE FIX
> RATHER THAN ARGUED.** With the aggregate change absent, 50 posts of one catalogue clip moved
> **$500.00** out of a sandbox campaign and `getCampaignBudgetStatus().spent` read **$225.00**. The
> hidden **$275.00** is **exactly 55.0 percent of every v2 dollar**, and every existing test would have
> passed, because every existing test reads `Clip.earnings`.
>
> **2. THE ARITHMETIC PROOF CAUGHT A REAL DEFECT THAT IS SPECIFIC TO 45/45 AND CANNOT EXIST IN
> 60/30.** Copying the v1 residual form verbatim creates money from nothing at a gross of **$0.013**:
> both 45 percent legs round UP to a cent against a gross that rounds to a cent, v1's `Math.max(0,…)`
> swallows the negative residual, and the three legs sum to **$0.02 against a $0.01 gross**. The same
> value through the LIVE v1 function sums to exactly $0.01, because 0.6 and 0.3 are asymmetric and
> only one of them can round up. **Caught at one gross in 4,237, before a single line was reachable.**
>
> **3. HIS ADDS ANSWER MAY REST ON A MISREADING, AND THIS ROUND SAYS SO RATHER THAN BURYING IT.** The
> 9 percent payout fee is present in **both** options and is not the variable. Per $100 of gross:
> **REPLACES nets him $18.10 and the campaign spends $100.00; ADDS nets him $51.43 and the campaign
> spends $133.33.** ADDS takes nothing from the earners. **It makes the CAMPAIGN pay 33.3 percent more
> for the same views, so a fixed budget buys 25.0 percent fewer views.**
>
> **4. NOTHING IS REACHABLE BY ANY USER, PROVEN BY GREP.** Zero files under `src/app` reference the v2
> modules or `marketplaceV2`, zero API route directories match `*v2*`, and zero v2 routes sit under
> `/api/marketplace`.

**PROOFS: 9 of 9 arithmetic checks and 25 of 25 sandbox checks passed. 0 failed.**
The one failure this round hit was real, is reported in full in PART 2, and was fixed.

---

## PART 0 — THE MODEL SPLIT, AND WHAT WAS CHECKED AGAINST SOURCE

| tier | what ran there | subagents | tokens |
|---|---|---|---|
| **cheapest (Haiku)** | pure retrieval: the Prisma schema and migration house style, the sandbox harness inventory, the build and lint gate inventory | **3** | **240,852** |
| **strongest (Opus), NOT SPLIT** | every line of the money arithmetic, the residual and its defect, the ADDS flag, the `balance.ts` aggregate, the v2 writer, the two new guards, every schema decision, every proof script, and this report | **0 subagents** | |

**BL-876 recorded that one retrieval subagent mischaracterised BL-866's devaluation. The same
happened again, twice, and both were caught against source:**

1. **The gate subagent reported `node_modules/.bin/eslint` DOES NOT EXIST** and warned at length that
   the BL-348 hooks gate would silently no-op. **It checked while `npm ci` was still running.**
   Verified after the install completed: `node_modules/.bin/eslint` is present in three forms, and
   the gate produced real eslint output in this round's build log. **The warning was right in
   principle and wrong in fact, and the fact was checked rather than trusted.**
2. **The sandbox subagent quoted `writeClipEarnings(db, id, { baseEarnings, bonusAmount, isApproved:
   true })`.** That signature does not exist. The real one is
   `writeClipEarnings(tx, clipId, { earnings, baseEarnings, bonusPercent, bonusAmount }, options)`,
   read directly at `src/lib/clip-earnings-writer.ts:129-134`. The v2 writer was written against the
   file, not against the quote.

**No subagent opened a database connection. Every database read in this round was made by this
orchestrator, one connection at a time, through `scripts/run-select.js` or a single
`$queryRawUnsafe` inside a proof script.** The population checks are ONE statement each, because two
prior rounds exhausted the Supabase pool and caused failed reads for the owner's live session.

---

## PART 1 — THE FOUR MODELS

### What was created

| model | table | rows at close |
|---|---|---|
| `MarketplaceV2Clip` | `marketplace_v2_clips` | **0** |
| `MarketplaceV2Post` | `marketplace_v2_posts` | **0** |
| `MarketplaceV2EditorEarning` | `marketplace_v2_editor_earnings` | **0** |
| `MarketplaceV2PlatformEarning` | `marketplace_v2_platform_earnings` | **0** |
| plus one new nullable column | `clips."marketplaceV2PostId"` | **0 clips carry it** |

Fields and indexes are exactly BL-876's PART 2.2. The Prisma diff is **215 insertions, 0 deletions**.

**`prisma format` WAS RUN ONCE AND WAS REVERTED, and that is worth recording.** It reformatted the
entire 3,763-line schema, producing a diff of 999 insertions and **785 deletions** across models this
round has no business touching. It was reverted with `git checkout --` and the five edits were
re-applied by hand; `npx prisma validate` was used instead, which reports validity without rewriting
anything. **Do not run `prisma format` on this repository.**

### The two fields that decide whether this is safe

**`marketplaceV2PostId` is a NEW column and deliberately not `marketplaceSubmissionId`**
(`prisma/schema.prisma`). The v1 column is read by `marketplace-cascades.ts`, which deletes and
rewrites earning rows on submission state changes a v2 clip will never have. A v2 clip must be
invisible to that code.

**`isMarketplaceClip` STAYS FALSE ON EVERY V2 CLIP.** BL-876 called this the single most dangerous
line in the build: setting it true makes `isCpmSplit = !isMarketplaceClip && …` (`tracking.ts:2047`,
`clips/[id]/review/route.ts:520`) and the two 60/30/10 writers (`tracking.ts:2099`,
`review/route.ts:526`) fire on a clip whose split is 45/45/10, and the clip is **silently paid on the
wrong split**.

**The test that fails if it is ever not**, run across the FULL population and not only the sandbox:

```
PASS  isMarketplaceClip is FALSE on every one of the fifty v2 clips
      0 of 50 carry the v1 flag.
PASS  isMarketplaceClip is FALSE on every v2 clip in the FULL population
      0 of 50 v2 clips carry it. Platform-wide, 0 of 10230 clips carry the v1 flag at all.
PASS  no v2 clip carries the v1 marketplaceSubmissionId the cascades read
      0 of 50 carry it; 50 of 50 carry the new marketplaceV2PostId instead
```

The assertion lives in `scripts/sandbox/bl877-prove.ts` and is a SQL join over
`clips JOIN marketplace_v2_posts`, so it covers every v2 clip that will ever exist rather than only
the ones a given run created.

### Why the earning tables are MIRRORS and not a reuse

Writing v2 rows into `MarketplaceCreatorEarning` would place them inside every query that already
reads it: the spend aggregate, `effectivePaidOut` (`balance.ts:234-258`), the withdrawal gate
(`payouts/route.ts:852`), and **the v1 cascades**, which delete and rewrite those rows on states a v2
clip never has. Half of that is wanted and half is catastrophic. New tables make the isolation total
and the participation explicit: **each aggregate that must see v2 money is extended by hand, one at a
time, and nothing else can reach it.**

### The unique indexes, applied CONCURRENTLY and verified in the catalogue

Prisma's `@@unique` enforces **nothing** at runtime. BL-841 found `@@unique([submissionId, platform])`
declared on `MarketplaceClipPost` with a comment asserting the index had been applied out of band,
measured `pg_indexes`, and found it had **never been created**, which left the P2002 handler
unreachable and allowed two earning clips for one slot. BL-845 applied it by hand.

`run-schema-sql.js:203` sends a whole file as ONE simple query, and Postgres wraps a multi-statement
simple query in an implicit transaction, where `CREATE INDEX CONCURRENTLY` fails with SQLSTATE 25001.
So each unique index ran as its own `--inline` statement:

```
node scripts/run-schema-sql.js --inline "CREATE UNIQUE INDEX CONCURRENTLY IF NOT EXISTS marketplace_v2_posts_clipid_key ON public.marketplace_v2_posts (\"clipId\")"
node scripts/run-schema-sql.js --inline "CREATE UNIQUE INDEX CONCURRENTLY IF NOT EXISTS marketplace_v2_editor_earnings_clipid_key ON public.marketplace_v2_editor_earnings (\"clipId\")"
node scripts/run-schema-sql.js --inline "CREATE UNIQUE INDEX CONCURRENTLY IF NOT EXISTS marketplace_v2_platform_earnings_clipid_key ON public.marketplace_v2_platform_earnings (\"clipId\")"
```

**Verified in `pg_indexes` rather than in the schema file**, 21 indexes across the four tables:

```
marketplace_v2_posts_clipid_key               unique=true valid=true ready=true
marketplace_v2_editor_earnings_clipid_key     unique=true valid=true ready=true
marketplace_v2_platform_earnings_clipid_key   unique=true valid=true ready=true
```

**And then the constraint was made to REFUSE, rather than trusted because it was listed.** A second
platform leg was attempted on a clip that already had one:

```
PASS  a SECOND platform leg on the same clip is REFUSED by the database
      refused with P2002
```

**THERE IS DELIBERATELY NO UNIQUE ON `(v2ClipId, posterId)`.** BL-876 open question 11 asks whether a
poster may post one clip to several of his OWN accounts and the owner has not answered it. That index
would forbid multi-account posting by construction and pre-empt his decision. If he answers "one
account only", the enforcement is a CONCURRENTLY unique index on `(v2ClipId, clipAccountId)`, added in
the round that asks him.

### The SQL and its rollback

The full migration is `scripts/migrations/BL-877-marketplace-v2.sql`, applied through the sanctioned
path with `IF NOT EXISTS` semantics and **never `prisma migrate`**, which is recorded as prod-fatal
here against 25 hand-run migrations. The rollback is printed in the file header, **before it was
run**, and goes through the Supabase SQL editor because `run-schema-sql.js` refuses every DROP on
purpose:

```sql
ALTER TABLE clips DROP COLUMN IF EXISTS "marketplaceV2PostId";
DROP TABLE IF EXISTS public.marketplace_v2_platform_earnings;
DROP TABLE IF EXISTS public.marketplace_v2_editor_earnings;
DROP TABLE IF EXISTS public.marketplace_v2_posts;
DROP TABLE IF EXISTS public.marketplace_v2_clips;
DROP TYPE  IF EXISTS "MarketplaceV2ClipStatus";
```

**Proven present afterwards** by `information_schema.columns`: 55 columns across the four tables plus
`clips."marketplaceV2PostId"` as `text`, `is_nullable=YES`, no default. Every column's type and
nullability is in the round's own output and matches the model.

---

## PART 2 — THE ARITHMETIC, AND THE DEFECT IT CAUGHT

### A twin in its own file, with the existing function byte-identical

The v2 calculator is `src/lib/marketplace-v2-earnings.ts`, a separate file, NOT a parameterised
rewrite of `calculateMarketplaceEarnings` (`earnings-calc.ts:629-691`), which is called from two LIVE
money writers and must not change shape. **`calculateMarketplaceEarnings` and every other existing
export in `earnings-calc.ts` are textually unchanged**; the file's only diff is one keyword and its
comment, printed in full in PART 6.

### THE DEFECT, WHICH IS REAL AND WHICH 60/30 CANNOT REACH

The first run of the arithmetic proof **FAILED**, and the failure is the most valuable thing this
round produced:

```
FAIL  4237 generated grosses, three legs sum to round2(gross)
      4236 of 4237 exact, worst drift $0.0100
FAIL  never over-allocates
      1 over-allocations
```

Located exactly, by a script written for the purpose:

```
DRIFT FOUND
  requested gross       : 0.013        (13 views at a $1.00 CPM)
  gross INSIDE the calc : 0.01
  editorBase            : 0.01
  posterBase            : 0.01
  platformBase          : 0
  legs sum              : 0.02         <-- A CENT FROM NOWHERE
  --- the SAME gross through the LIVE v1 60/30/10 function ---
  v1 creatorBase        : 0.01
  v1 posterBase         : 0
  v1 platformBase       : 0
  v1 legs sum           : 0.01 (exact)
```

**THE SYMMETRY OF 45/45 IS THE CAUSE.** `round2(0.013 × 0.45) = $0.01` for BOTH earners against a
gross that rounds to $0.01. The residual is minus a cent and v1's `Math.max(0, …)` **silently swallows
a negative residual**, leaving the legs summing to more than the gross. **V1 cannot reach that state**
because 0.6 and 0.3 are asymmetric: only one of its two earner legs can round up. The affected band
is a gross in **[$0.0111, $0.015)**.

**Copying the v1 form verbatim, which is exactly what the brief asked for, would have shipped money
created from nothing.**

### The fix, by construction rather than by special case

```ts
const grossR = round2(gross);
const editorBase = Math.min(round2(gross * 0.45), grossR);
const posterBase = Math.min(round2(gross * 0.45), round2(grossR - editorBase));
const platformBase = Math.max(0, round2(grossR - editorBase - posterBase));
```

Each leg is bounded by what is left of the gross, so the running total can never exceed it and the
platform residual is always exactly the remainder. **At every gross at or above about two cents this
is byte-identical to the uncapped form.**

### Re-proved

```
PASS  gross $0.55 legs sum exactly
      editor $0.25 + poster $0.25 + platform $0.05 = $0.55 (gross $0.55)
      three independent multiplications would have produced $0.56  <-- a cent from nowhere
PASS  gross $0.11 legs sum exactly
      editor $0.05 + poster $0.05 + platform $0.01 = $0.11 (gross $0.11)
PASS  4237 generated grosses, three legs sum to round2(gross)
      4237 of 4237 exact, worst drift $0.0000
PASS  never over-allocates          0 over-allocations
PASS  platform leg never negative   0 negative
PASS  editor $45.00, poster $45.00, platform $10.00
```

The 4,237 grosses are every cent from $0.01 to $10.00, 46 primes as dollars and as cents and as
tenths of a cent, 99 sub-cent values, and 3,000 deterministic pseudo-random values up to $5,000 so a
rerun proves the same set.

**AND THE FORM THIS DESIGN REJECTS, MEASURED ON THE SAME POPULATION:** three independent
multiplications **over-allocate on 898 of the 4,237 grosses.**

---

## PART 3 — THE ADDS DECISION, AS ONE NAMED FLAG

`MARKETPLACE_V2_PLATFORM_CUT_MODE: "ADDS" | "REPLACES" = "ADDS"` in
`src/lib/marketplace-v2-earnings.ts`, with `v2AgencyEarningApplies()` as its single reader, so the
decision has one writer and one reader rather than a scatter of `if` statements.

**Mechanically, it is one boolean.** A v2 clip leaves `isMarketplaceClip` false, so it falls into the
ordinary `isCpmSplit` branch and an `AgencyEarning` row IS written on top of the 10 percent unless a
later round deliberately excludes it. **ADDS therefore means letting that branch run.** REPLACES would
mean suppressing it, which is what the FIRST marketplace does: BL-841 measured that no `AgencyEarning`
row is ever written for a v1 marketplace clip.

### Both outcomes, on a real worked example, computed from the constants

```
     editor   gross $45.00  cash $40.95
     poster   gross $45.00  cash $40.95
     platform leg   $10.00
     the two withdrawal fees to the owner  $8.10
     REPLACES: owner nets $18.10, campaign spends $100.00
     ADDS:     owner nets $51.43, campaign spends $133.33
PASS REPLACES reconciles to exactly $100.00
     $40.95 + $40.95 + $18.10 = $100.00
PASS ADDS reconciles to what the campaign spends
     $40.95 + $40.95 + $51.43 = $133.33 = campaign spend $133.33
```

### THE MISREADING, SURFACED

He said "we get nine percent plus the ten percent". **The 9 percent payout fee is present in BOTH
options and is not the variable.** Each earner pays it on his own withdrawal either way, and it comes
to **$8.10 per $100 in both columns above.** The variable is his **ordinary per-clip cut**, roughly 33
percent on a CPM_SPLIT campaign.

### WHAT ADDS ACTUALLY DOES TO CAMPAIGN COST PER VIEW

**It does not move money from the earners to him.** The editor takes $45.00 gross and $40.95 cash
under both options, and so does the poster. **What changes is what the CAMPAIGN pays for the same
views: $133.33 instead of $100.00**, a 33.3 percent higher cost per view. On a fixed budget that means
the same budget buys **25.0 percent fewer views** and the campaign exhausts and auto-pauses sooner.
That is the whole trade. It is his to make; this round only refuses to make it silently.

Changing it is one word in one file.

---

## PART 4 — THE ONE LINE THAT MATTERS MOST

### THE FAILURE, DEMONSTRATED FIRST

The sandbox world was built and 50 posts of one catalogue clip were written **while the aggregate
change was still absent**, because a guard nobody has watched fail proves nothing and BL-864 caught
its own proof passing on a helper that read every balance as $0.00:

```
  50 POSTS OF ONE CLIP, AGAINST ONE BUDGET
    gross across all posts   $500.00
    editor (45 percent)      $225.00
    poster (45 percent)      $225.00
    platform (residual)      $50.00
    three legs sum           $500.00
    legs exact on            50 of 50 posts

  WHAT THE BUDGET LOCK CAN SEE RIGHT NOW
    getCampaignBudgetStatus().spent  $225.00
    what actually left the budget    $500.00
    INVISIBLE TO THE LOCK            $275.00
    that is 55.0 percent of every v2 dollar
```

**A $5,000 campaign would have distributed $11,111 before auto-pausing, and every existing test would
have passed, because every existing test reads `Clip.earnings`.**

### THE FIX, AND IT HOLDING

Two aggregates added to `getCampaignBudgetStatus`, on **exactly** the filter the v1 creator and
platform legs already use (`APPROVED`, not deleted, not `videoUnavailable`), so the two marketplaces
are counted on the same basis and neither can drift. Also added to `clipperSideSpent` on the same
basis, mirroring the v1 rule so a future reader finds one rule rather than two that disagree.

```
PASS  getCampaignBudgetStatus().spent now includes the editor and platform legs
      spent $500.00 == poster $225.00 + editor $225.00 + platform $50.00 = $500.00.
      BEFORE THE FIX bl877-create.ts measured spent $225.00 against $500.00, hiding $275.00.
```

**Byte-identical to the pre-BL-877 figure for every campaign with no v2 rows**, because a SUM over
zero rows is null and coalesces to 0. Measured at ship time: **0 rows in both tables platform-wide.**

### BL-627's three mechanisms, all intact

| mechanism | where | state |
|---|---|---|
| per-tick truncation inside a Serializable transaction | `tracking.ts:2335-2534` | **untouched.** `tracking.ts` is byte-identical by blob OID |
| the L1 hard lock that reads COMMITTED spend and throws | `clip-earnings-writer.ts:199-257` | **untouched, and now better fed.** It calls `getCampaignBudgetStatus`, so the two new aggregates reach it without the file changing |
| per-campaign SEQUENTIAL tracking | `tracking.ts` | **untouched** |

```
PASS  no campaign's realized spend exceeds its budget, counting v2
      0 campaigns over budget, measured with the v2 legs INCLUDED in the sum
```

**ONE HONEST LIMIT, STATED RATHER THAN HIDDEN.** The L1 lock computes
`delta = rounded.earnings - current.earnings` (`clip-earnings-writer.ts:196`), which on a v2 clip is
the POSTER leg only. So `status.spent` now sees all committed v2 money, but the PROJECTION of a single
increment under-counts by 55 percent of that one increment. **This is the existing v1 shape, not a new
defect** — the v1 marketplace has had exactly this since Phase 6d. It is bounded by one clip's
increment, and the next write on that campaign sees the committed overshoot and refuses. Closing it
properly needs either a change to `clip-earnings-writer.ts` or a v2 pre-flight gate that projects the
FULL gross; `computeV2BudgetCost` in `marketplace-v2-earnings.ts` is that projection, written and
exported, **and the round that wires the tracking tick must call it.** It was not wired here because
nothing is reachable in this round and wiring it would have required touching a money file for a path
no user can take.

### The editor leg's invariant guard, which did not exist before

BL-876 found the editor's leg would have **no invariant middleware watching it at all**, the same gap
BL-841 found for the v1 marketplace's two tables (item 14). **Yes, a guard was added**, in
`src/lib/marketplace-v2-writer.ts`, and it checks two things:

1. **`assertV2EditorInvariant`** — `amount` must equal `baseAmount + bonusAmount` to within $0.01, the
   same rule and the same tolerance `assertInvariant` applies to a Clip. It **throws** rather than
   writing inconsistent state.
2. **BL-538's `decideNeverDecrease`** — a retroactive recompute may raise the editor's recorded figure
   and can never silently write it down. Blocking is fail-safe and is logged, never silent.

Both demonstrated firing:

```
PASS  a proposed DECREASE on the editor leg is blocked
      stored $4.50, proposed $4.00 -> BLOCKED_DECREASE, blocked $0.50
PASS  a proposed INCREASE is allowed
      stored $4.50, proposed $5.00 -> INCREASE
PASS  the editor-leg invariant THROWS on inconsistent state
      amount $10.00 against base $4.00 + bonus $1.00 was refused rather than written
PASS  the NEW editor-leg invariant holds across every v2 editor row
      0 of 50 rows breach amount = base + bonus.
```

---

## PART 5 — THE WRITER

`writeMarketplaceV2Earnings` (`src/lib/marketplace-v2-writer.ts`) takes a Prisma **transaction
client** and writes all three legs inside it. Passing the top-level `db` would let a clip exist with a
poster leg and no editor leg if the process died between calls, which is the one failure mode the
signature exists to prevent.

* **The poster's 45 percent goes ONLY through `writeClipEarnings`.** There is no direct `clip.update`
  on the four invariant fields anywhere in the file, and `npm run check:prisma-bypass` enforces that
  repo-wide: **0 violations across `src/` + `scripts/`**. Going through the chokepoint is what gives a
  v2 clip the L1 budget hard lock, the BL-167 pool clamp and the Clip invariant for free.
* **The editor and platform legs are written in the SAME transaction.** A throw from the L1 lock rolls
  the whole transaction back and takes all three legs with it.

### The editor's total is never stored

```
PASS  marketplace_v2_clips holds NO earnings, amount or total column
      0 such columns. The editor's total is SUM(marketplace_v2_editor_earnings.amount),
      computed at read time. BL-539 measured a second source of truth at $933.94.
PASS  the editor's total reads correctly as a SUM over his rows
      SUM over 50 rows = $225.00, which is 45 percent of $500.00 of gross
      from ONE clip he made ONCE
```

`MarketplaceV2Clip.postCount` exists as a denormalised counter for display and is documented in the
schema as **never authoritative for money**.

### The two bonus stacks, reported rather than discovered later

A v2 clip carries TWO bonus stacks where an ordinary clip carries one, because there are two earners
with two profiles, and the platform's leg gets none.

```
PASS  two-bonus-stack figure is $106.75 and the platform slice is 9.37 percent
      a $100 gross clip with a 10 percent editor bonus and a 5 percent poster bonus
      disburses $106.75, and the platform's $10.00 is 9.37 percent of what leaves.
```

**Does it interact with the ADDS decision? NO, and the two are independent.** Bonuses are added to the
two EARNER legs; the ordinary owner cut is computed from `ownerCpm` on the same views; neither term
appears in the other's arithmetic. **A campaign carrying both pays $140.08 per $100 of gross**
($133.33 for ADDS plus $6.75 of bonus). The figure is computed by `computeV2TwoBonusStackCost` from
the constants, so this report and the code can never disagree.

---

## PART 6 — THE FIRST MARKETPLACE IS UNTOUCHED

### Proven by grep

| claim | measured |
|---|---|
| no v2 row in any `Marketplace*` table | v1 submissions **0**, clip posts **0**, creator earnings **0**, platform earnings **0**, all at their opening values |
| `MarketplaceVideoHash` never written | **9 rows, unchanged** from the opening census. Its global `@unique` on `hash` would have refused a second editor's legitimate submission, and BL-868 measured how painful a false duplicate is |
| no v2 route under `/api/marketplace` | `find src/app/api/marketplace -type d -iname "*v2*"` returns **0** |
| no v2 API route anywhere | `find src/app/api -type d -iname "*v2*"` returns **0** |
| nothing under `src/app` references v2 | `grep -rn "marketplaceV2\|marketplace-v2" src/app` returns **0** |
| who imports the v2 modules at all | only the four `scripts/sandbox/bl877-*.ts` proof scripts, plus a comment in `earnings-calc.ts` and the generated Prisma client |

### Proven by exercising the existing paths

The v1 marketplace's own money path runs through `calculateMarketplaceEarnings`, which is **textually
unchanged**, and its budget accounting runs through `getCampaignBudgetStatus`, which was exercised in
this round against a live campaign and returns the v1 terms unchanged plus two new terms that sum to
zero when there are no v2 rows. The v1 residual arithmetic was run directly in
`bl877-find-drift.ts` against the live function and produced exactly its documented values.

### THE ONE REAL COUPLING, STATED HONESTLY

**A campaign carrying BOTH marketplaces draws on ONE `campaign.budget` and ONE `spent` aggregate, and
one can pause the other.** That is inherent to a shared budget rather than a defect, but it is a fact
the owner should know before he enables both on one campaign, and it is an argument for the campaign
type in Round Two being the thing that decides which marketplace a campaign carries.

### The money files

| file | `main` blob OID | branch blob OID | status |
|---|---|---|---|
| `clip-earnings-writer.ts` | `ac5be7de…` | `ac5be7de…` | **BYTE-IDENTICAL** |
| `tracking.ts` | `bf31646f…` | `bf31646f…` | **BYTE-IDENTICAL** |
| `clip-earnings-invariant-middleware.ts` | `61cef393…` | `61cef393…` | **BYTE-IDENTICAL** |
| `money-decimal.ts` | `ef5cdae7…` | `ef5cdae7…` | **BYTE-IDENTICAL** |
| `campaign-era.ts` | `106e16ad…` | `106e16ad…` | **BYTE-IDENTICAL** |
| `balance.ts` | `81a683c1…` | `25a0b2f2…` | **CHANGED, and the round exists to change it** |
| `earnings-calc.ts` | `797e2098…` | `00410634…` | **CHANGED, by one keyword** |

**`earnings-calc.ts`, the ENTIRE diff:**

```diff
-function computePartyBonusPercent(party: MarketplacePartyInput): number {
+// BL-877 — EXPORTED, and the keyword is the ONLY change to this file.
+// The second marketplace (45/45/10) needs the SAME bonus rule for its editor
+// and poster that this one uses for its creator and poster. Re-implementing it
+// in src/lib/marketplace-v2-earnings.ts would create a second source of truth
+// for a money rule, which is exactly what BL-539 measured the cost of at
+// $933.94 and what BL-570 confirmed. One definition, two callers.
+// Nothing about the function's body, signature or behaviour changed.
+export function computePartyBonusPercent(party: MarketplacePartyInput): number {
```

**One keyword. No body, no signature, no behaviour. The alternative was re-implementing the bonus rule
in the v2 file, which is precisely the second source of truth BL-539 priced at $933.94.**

**`balance.ts`** gains two aggregates in the existing `Promise.all`, one term in `spent` and two terms
in `clipperSideSpent`. The full diff is in the commit and every added line is commented with the
measured failure it prevents. **This is the change the round was called to make** and PART 4 shows it
failing and then holding.

---

## PART 7 — THE SANDBOX, THE TEARDOWN, AND THE MERGE

### The opening snapshot, taken before anything was created

BL-864 skipped it and its census reported two false failures, so it was taken first, twice: the
harness's own `snapshot.ts before` and an independent 36-row census of every table this round could
touch, with every timestamp cast `::text` against DB `now()`.

### Open versus close

| | open 12:59:59 | close 13:11:32 |
|---|---|---|
| users | 1747 | **1747** |
| campaigns | 34 | **34** |
| clips | 10180 | **10180** |
| clip_accounts | 1516 | **1516** |
| agency_earnings | 4882 | **4882** |
| payout_requests | 248 | **248** |
| every marketplace v1 table | unchanged | **unchanged** |
| `marketplace_video_hashes` | 9 | **9** |
| clips with `isMarketplaceClip = true` | 0 | **0** |
| earnings invariant breaches | 0 | **0** |

**EVERY TABLE COUNT IS IDENTICAL.**

### THREE FINGERPRINTS MOVED, AND THEY ARE ATTRIBUTED RATHER THAN EXCUSED

`fp_earnings`, `fp_agency` and `fp_payouts` all changed, and `sum_clip_earnings` rose by **$0.57**.
Measured rather than assumed:

```
cron_runs_since_open         4
cron_kinds                   lifecycle,tracking,watchdog
clips_updated_since_open     65
clips_updated_bl877sbx       0
clipstats_since_open         65
payouts_updated_since_open   1
audit_actions_since_open     APPROVED_PAYOUT,PAID_PAYOUT
```

**Four cron runs fired during the round. 65 REAL clips were recomputed by the tracking cron and 65
clip_stats written, exactly matching the +65 in the census, and ZERO of them carry the `bl877sbx-`
prefix. And the owner APPROVED AND PAID A REAL PAYOUT while this round ran**, which is what moved
`fp_payouts`. **None of it is this round.**

### The teardown

```
  marketplace_v2_platform_earnings deleted  50
  marketplace_v2_editor_earnings   deleted  50
  marketplace_v2_posts             deleted  50
  marketplace_v2_clips             deleted   1
  clips                            deleted  50
  clip_accounts                    deleted   1
  campaigns                        deleted   1
  users                            deleted   2

  205 deleted, 0 already gone, 0 FAILED
  VERIFIED: 0 of 205 recorded rows remain.
```

The four v2 tables were added to `DELETABLE_TABLES` and to the destroyer's `DELEGATE` map **before**
anything was created, so no row was ever written that the destroyer could refuse to touch. Every id
was ledgered at creation, including the 100 earning rows the writer produced, which were read back by
their own ids rather than assumed.

**A direct catalogue sweep after teardown**, independent of the ledger: **0** `bl877sbx-` rows in
users, campaigns, clips, clip_accounts, audit_logs, activity_events and notifications; **0** rows in
all four v2 tables; **0** clips carrying `marketplaceV2PostId`.

**One partial run happened and was cleaned before the real one.** The first create attempt failed on a
missing required `profileLink` on `ClipAccount` after creating two users and a campaign. Those three
rows were ledgered, destroyed (`3 deleted, 0 FAILED, VERIFIED: 0 of 3 remain`) and the ledger cleared
before the successful run. It is recorded here because a partial run that is not recorded is how a
stray row survives.

### Safety, itemised

| | |
|---|---|
| real users, clips, campaigns or payouts touched | **none.** Every person `isTestUser`, every campaign `isTestCampaign`, every id prefixed `bl877sbx-` |
| Apify actors run | **none.** The 11 BL-678 guards are untouched |
| vendor calls | **none.** Cost to the owner in vendor spend: **$0.00** |
| database connections | one at a time, by this orchestrator only. **No subagent opened one.** Population checks are ONE statement each |
| Prisma in the browser bundle | no. The v2 modules are server-only libs and no client component imports them |
| branch drift | checked before pushing: the commit sits on `checkpoint/BL-877`, and `main` was at `8dcc0c02` until the merge |
| `checkpoint/BL-723` | **not merged**, as required |
| handles and wallets | no handle printed, no wallet address read or printed |

### Build and gates, honestly

| | |
|---|---|
| tsc baseline BEFORE any change | **exit 0**, 0 lines |
| hooks gate baseline | **exit 0**, 0 errors, **10 warnings** against a cap of 11 |
| `npm run build` after the change | **exit 0** |
| `check:prisma-bypass` | **0 violations across `src/` + `scripts/`** |
| `check:removed-fields` | pass |
| `check:event-wiring` | **0 problems** |
| `lint:hooks` (BL-348) | **0 errors, 10 warnings**, identical to baseline |
| `next build` | **Compiled successfully in 55s** |
| **eslint actually present and running** | **yes**, verified after `npm ci` completed: `node_modules/.bin/eslint` exists and produced real rule output in the build log, so the gate is **not** silently no-opping |

Every exit code above was echoed by this round rather than inferred, and none was read through a pipe
into `tail`.

---

## WHAT IS AND IS NOT REACHABLE

**NOT REACHABLE BY ANY USER. Nothing in this round has a route, a page, a component or a navigation
entry.** Proven by grep in PART 6: zero files under `src/app` reference the v2 modules or
`marketplaceV2`, zero API route directories match `*v2*`, and zero v2 routes sit under
`/api/marketplace`. The only importers are four sandbox proof scripts that require a per-round
confirmation environment variable to run at all.

**What exists and is proven:** four tables, one column, three verified unique indexes, the 45/45/10
calculator with its residual, the ADDS flag, the budget aggregate, the three-leg writer, the editor
invariant and the editor never-decrease guard.

**WHAT ROUND TWO MUST BUILD to make any of this usable**, in the order BL-877's PART 9 set out:

1. **The editor's submission route and form.** The Drive link field with `isValidDriveUrl`, the title,
   the notes, and the three waiting states in words.
2. **The OWNER approval queue**, owner-only, with a REQUIRED rejection reason capped at 1,000
   characters and the separate optional improvement note.
3. **The two notifications**, matching the ordinary clip decision shape exactly, with a v2 deep-link
   destination rather than `/clips`.
4. **The campaign type**, a non-nullable enum defaulting to `NORMAL` so all 34 existing campaigns are
   unchanged with no backfill.

**No money moves in Round Two either.** An approved clip will sit in a catalogue nobody can post from.
**The poster post path, which is the first round where v2 money moves in production, is Round Four**,
and it must call `computeV2BudgetCost` as a pre-flight gate for the reason in PART 4.

---

## WHAT COULD NOT BE DETERMINED

* **Whether the 26 positions carrying $3,700.30 recorded below money already paid is comparable to
  BL-849's measured 17 carrying $1,893.34.** This round measured it with its own query nine days
  later; the shapes may differ in filters or rounding, and it was NOT re-measured with BL-849's exact
  query. **What is certain is the direction and the attribution: this round created zero payout rows,
  so it created no new position below a paid floor**, and `balance.ts` still bounds each campaign at
  `min(paid, payable)` so `available` is floored at zero and never negative.
* **The live behaviour of the L1 projection gap under production concurrency.** It is bounded by one
  clip's increment by construction, and the next write refuses, but it was not exercised under a real
  concurrent tick because nothing in this round is reachable by the cron.
* **Whether the Railway deployment has picked up the `balance.ts` change.** A redeploy is required and
  was not performed by this round.

---

**PERFORM NO FIX ON ANYTHING ABOVE. The one defect this round found, it fixed and re-proved.**

---

## ADDENDUM — INDEPENDENT POST-MERGE VERIFICATION (2026-09-16)

**THIS ROUND WAS FOUND ALREADY SHIPPED AND MERGED. NOTHING WAS REBUILT AND NOTHING WAS RE-RUN
AGAINST THE DATABASE THAT WRITES A ROW.** `main` was already at `668cae6c`, the merge of
`checkpoint/BL-877` into `8dcc0c02`, with `pre-BL-877`, `post-BL-877`, `pre-merge-BL-877` and
`post-merge-BL-877` all present. Re-running the round would have meant a second
`CREATE UNIQUE INDEX CONCURRENTLY`, a second sandbox population and a duplicate merge, so the
round was instead **verified from source, from the live catalogue and from a clean build**. Every
claim below was checked directly, not read out of this report.

**DB `now()` at verification: `2026-09-16 13:45:29.932817+00`, cast `::text`.**

### What was verified, and how

| claim | how it was checked | result |
|---|---|---|
| merged and pushed | `git rev-parse HEAD origin/main` | **both `668cae6c`**, identical |
| merge is real | merge commit parents | `8dcc0c02` + `ff6bc6fd` |
| the four tables exist | `information_schema.tables` | **4 of 4** present |
| the indexes exist | `pg_indexes` | **20 indexes**, including the three unique `clipId` indexes on posts, editor earnings and platform earnings |
| nothing is user-reachable | grep over `src/app` and `src/app/api` | **0** files referencing `marketplaceV2`, **0** route dirs matching `*v2*`, **0** v2 routes under `/api/marketplace` |
| teardown was exact | live counts | **0** rows in all four v2 tables, **0** clips carrying `marketplaceV2PostId`, **0** `bl877sbx-` users, campaigns or clips |
| `isMarketplaceClip` | live join across the full population | **0** v2 clips carrying it true |
| money files unchanged | `git rev-parse <ref>:<file>` on **both** refs, blob OID | `clip-earnings-writer.ts`, `tracking.ts`, `clip-earnings-invariant-middleware.ts`, `money-decimal.ts` and `campaign-era.ts` **byte-identical**; only `balance.ts` and `earnings-calc.ts` moved, and the whole diff was read |
| `earnings-calc.ts` change | full diff | **one keyword**, `function` to `export function`, plus comment. No body, signature or behaviour change |
| the v1 marketplace | `git diff --name-only pre-BL-877 main` | **15 files**, and **not one** is a v1 marketplace source file |
| v2 never touches v1 tables | grep inside both v2 modules | **0** references to `marketplaceCreatorEarning`, `marketplacePlatformEarning`, `marketplaceSubmission` or `marketplaceVideoHash` |
| the poster leg | read `marketplace-v2-writer.ts` | written **only** through `writeClipEarnings`, with a transaction client required and `throw` on a missing one |
| no stored editor total | grep the four v2 models | **no** total field exists to drift |
| the arithmetic | **re-ran `scripts/sandbox/bl877-arith.ts`** | **9 of 9 passed, 0 failed**, exit 0. 4,237 of 4,237 grosses sum exactly; the rejected form over-allocates on 898 of the same 4,237 |
| BACKLOG | `grep -c "^## BL-"` | **197** items, one above BL-874's 196 |
| the report | blob OID, local against the reports repo | **`d0b1b75d`** on both. The published copy is byte-identical |
| the worktree | `git worktree list` and listing `C:\w` | **one worktree**, the main checkout. `C:\w` is **empty**. `C:\w\b877` is gone |

### The build, honestly

`npm run build` was re-run on `main` at verification, from a log, with the exit code echoed by the
build's own shell rather than read off a pipe: **`BUILD_EXIT=0`**.

* `check:prisma-bypass` — **0 violations**.
* `check:removed-fields` — OK across 784 files.
* `check:event-wiring` — **0 problems**.
* **BL-348 hooks gate** — `eslint` is genuinely present (**3 binaries** in `node_modules/.bin`, so the
  gate did not silently no-op) and reported **10 problems, 0 errors, 10 warnings** against the
  ceiling of 11. **Pass, with one warning of headroom.**
* `next build` completed and emitted the full route table.

### What this addendum does NOT claim

* **It did not re-run the sandbox.** The 25 sandbox checks and the $500.00-against-$225.00
  demonstration are this report's own, from the shipping round. What was re-verified is that the
  fix they justified is on `main`, that it reads the two aggregates, and that the database is clean.
* **The Railway redeploy is still owed and was not performed.** Until it happens the deployed
  `balance.ts` is the pre-BL-877 one. **This is harmless today and only today**, because there are
  zero v2 rows platform-wide, so the two new aggregates would sum to zero anyway. It must be done
  before Round Four, which is the first round where v2 money moves.
