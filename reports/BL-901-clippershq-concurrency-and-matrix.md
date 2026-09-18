# BL-901 — Can the marketplace produce concurrent writes to one campaign?

**Round:** BL-901 · **Date:** 2026-09-18 · **Branch:** `checkpoint/BL-901` → `main`
**Merge commit:** `b87ac4ea` · **Tags:** `pre-BL-901`, `post-BL-901-branch`, `pre-merge-BL-901`, `post-BL-901`

**ONE LINE VERDICT:** The budget is now safe without relying on any ordering — a campaign row lock
inside the transaction makes forty racing writers land at $486.22 against $500.00 where they landed at
$1,389.20 before, and sequential now gives figures identical to concurrent — and **nothing found in
this round blocks setting `NEXT_PUBLIC_MARKETPLACE_V2_ENABLED` to true.**

---

## PART 0 — The question, answered before anything was built

### Every path by which a v2 post writes earnings

| # | Path | file:line | Reachable by |
| --- | --- | --- | --- |
| 1 | `createV2Post` → `writeMarketplaceV2Earnings` | `marketplace-v2-poster.ts:791` | `POST /api/marketplace-v2/catalogue/[id]/post` (`route.ts:122`) |
| 2 | `recomputeV2PostEarnings` → `writeMarketplaceV2Earnings` | `marketplace-v2-poster.ts:936` | **ONE production caller only:** `marketplace-v2-conversion.ts:477`. Every other caller is a sandbox script. |
| 3 | tracking tick's v2 fork | `tracking.ts:3098` (`writeClipEarnings`, `skipV2LegSync: true`) then `tracking.ts:3128` (`writeMarketplaceV2Earnings`) | the `:00` cron tick |
| 4 | `syncV2LegsAfterPosterWrite` | `clip-earnings-writer.ts:834` | ANY `writeClipEarnings` on a v2 clip without `skipV2LegSync` — admin force-recalc, fix-earnings, freeze-undo, override, review |
| 5 | conversion / undo | `marketplace-v2-conversion.ts:112`, `:284` | `POST /api/admin/clips/[id]/convert-to-marketplace` |

### Can two posters posting simultaneously produce two concurrent transactions against one campaign?

**Yes — nothing serialises them.** But it does not matter, because **a post is worth nothing.**

`createV2Post` computes its breakdown with `views: 0` (`marketplace-v2-poster.ts:724`), and
`calculateMarketplaceV2Earnings` returns an all-zero breakdown at `marketplace-v2-earnings.ts:184`
(`if (!input.views || input.views <= 0) return empty`). All three legs are $0.00, so the L1 gate's
`if (delta > 0)` is never entered and the budget is not even queried.

### Was BL-879 sequential or concurrent?

**SEQUENTIAL, and it did not use the HTTP route.** `scripts/sandbox/bl879-prove.ts:297` is
`for (let i = 0; i < POSTERS; i += 1)` with an `await` inside. It called the library function
`createV2Post` directly, not the route, and **the money came from a separate follow-up transaction of
its own** at `:313-317` calling `recomputeV2PostEarnings` with views. The $10 per post it measured did
not come from the post. It proves nothing whatever about concurrency.

### Twenty concurrent posts, driven through the real route

Production build (`npm run build` + `npm start`), `DEV_AUTH_BYPASS=false`, port 3901. Twenty sandbox
posters, each with **his own user id, his own approved ClipAccount and his own minted Auth.js
`__Secure-` session cookie**. Campaign seeded to $495.00 of a $500.00 budget, leaving **$5.00 of
headroom**, so any real cost would be unmissable.

| measure | result |
| --- | --- |
| landed | **20** |
| refused | **0** |
| rate limited (429) | **0** |
| `postedAt` spread, first to last | **270 ms** (product-stamped, inside each transaction) |
| whole batch wall clock | 4,439 ms |
| budget | $500.00 |
| spend before / after | $495.00 / **$495.00** |
| **moved by twenty posts** | **$0.00** |
| all three legs across the 20 posted clips | $0.00 / $0.00 / $0.00 |

The dev bypass was proven off by asking the same route **without** a cookie first: it answered 401,
then 200 with a cookie. Without that check a 401 storm would have read as "refused".

**11 of 11 checks passed.**

### What serialises the money path today, and is it a guarantee or an accident?

**An accident of loop structure, not a constraint.** `tracking.ts:3602` — "Processes campaigns in
parallel, clips within same campaign sequentially (budget-safe)" — and `tracking.ts:4141` —
"per-campaign clip processing must be SEQUENTIAL". There is no lock, no unique index and no
DB-level guarantee behind either. Any future path writing one campaign's clips in parallel breaches
the budget. That is precisely what this round fixed.

### Which non-cron writers could the owner run twice at once?

All of them, and **two browser tabs is enough**. Every one calls `db.$transaction(fn)` with **no
isolation level**, which is Postgres's default READ COMMITTED:

- `admin/force-recalc-earnings/route.ts:318` — "Short transaction per clip"
- `admin/campaigns/[id]/unfreeze/route.ts:187`
- `clips/[id]/review/route.ts:279`, `:635`, `:1125`
- `admin/fix-earnings`, `admin/fix-budget`, `admin/clips/[id]/cpm-override`,
  `admin/payouts/[id]/adjust`, `admin/payouts/[id]/devalue`, `admin/marketplace-v2/clip-legs`

---

## PART 1 — The fix

### The defect reproduced before a line was changed

The hole is only visible when **each write fits the headroom individually while the sum does not**.
A $5.00 headroom against a $34.73 write measures nothing, because each writer is refused alone.

| case | writers | budget | settled | refused | spent | over by |
| --- | --- | --- | --- | --- | --- | --- |
| both bonused | 20 | $500.00 | 20 | 0 | **$694.60** | $194.60 |
| no bonuses | 20 | $100.00 | 20 | 0 | **$140.00** | $40.00 |
| both bonused (BL-898's exact case) | 40 | $500.00 | 40 | 0 | **$1,389.20** | $889.20 |

The 40-against-$500 figure is **BL-898's own number to the cent**, reproduced independently.

### An isolation-level finding worth recording

The first attempt forced `Serializable` and **the defect did not reproduce**: 19 of 20 writers died
with `TransactionWriteConflict` out of the v2 leg sync, one write landed, the budget never moved.
That is not the production shape — `createV2Post` and every non-cron writer above use the default
READ COMMITTED, and BL-898's own test did too. Under Serializable, Postgres's SSI already serialises
these writers (this is what `F-TX-CONFLICT-FIX1` at `tracking.ts:4141` describes), but at a throughput
of roughly one write in twenty. The default is what was measured; Serializable is reported beside it
rather than substituted for it.

### The change — the full diff, justified

Two functional edits in **one file**, `src/lib/clip-earnings-writer.ts`.

**1. The lock, taken before the committed-spend read:**

```ts
await lockCampaignRowForBudget(tx, current.campaignId, clipId, options.reason);
const { getCampaignBudgetStatus } = await import("@/lib/balance");
const status = await getCampaignBudgetStatus(current.campaignId);
```

```ts
async function lockCampaignRowForBudget(tx, campaignId, clipId, reason): Promise<void> {
  // ALWAYS. Never behind a guess about which client this is.
  await tx.$queryRaw`SELECT id FROM campaigns WHERE id = ${campaignId} FOR UPDATE`;
  if (typeof tx?.$connect === "function") { console.warn(`[F-BUDGET-ROW-LOCK-STANDALONE] ...`); }
}
```

*Why:* the read is not the bug and is not changed — `getCampaignBudgetStatus` deliberately uses the
top-level client so the gate compares against COMMITTED state, and the note at `:173-176` saying so is
still correct. What was missing is that nothing made the writers take turns, so "committed" meant
"committed by whoever finished first", and with everyone starting together that was nobody. Postgres
holds the row until the transaction ends — **the same instant the money becomes visible** — so the
next writer's read cannot miss it.

**My first version did nothing and its own log line caught it.** It guessed which client it held by
the presence of `$transaction`, on the documented grounds that Prisma strips it from a transaction
client. It does **not** strip it from an **extended** client's transaction client, so the guard fired
on every call, the lock was skipped **120 times**, and the re-run measured $1,389.20 unchanged. The
lock is now unconditional and only the diagnosis is a guess; `$connect` and `$extends` are the
properties that actually differ, measured rather than assumed.

**2. The maker's leg priced at its floored value** — see PART 3.

### What was NOT removed

BL-627's three mechanisms all stand: the per-tick truncation inside `tracking.ts`'s Serializable
transaction, the L1 hard lock reading committed spend, and per-campaign sequential tracking at
`tracking.ts:3602` / `:4141`. `tracking.ts` is **byte-identical by blob OID** and appears in no diff.
The ordering is now redundant for budget purposes and is deliberately left in place.

### Proof the overshoot closes — every case, both ways

| case | writers | budget | before | **after (concurrent)** | **after (sequential)** |
| --- | --- | --- | --- | --- | --- |
| both bonused | 20 | $500.00 | $694.60 | **$486.22** | **$486.22** |
| no bonuses | 20 | $100.00 | $140.00 | **$98.00** | **$98.00** |
| both bonused (BL-898's case) | 40 | $500.00 | $1,389.20 | **$486.22** | **$486.22** |
| both bonused | 40 | $10,000.00 | $13,890.00 | **$9,723.00** | **$9,723.00** |

**Sequential and concurrent are now identical in every case** — the strongest available statement that
the lock makes racing behave exactly like queuing. $9,723.00 matches BL-898's own sequential figure.
Every refusal was `[F-BUDGET-HARD-LOCK]`'s own, **zero** deadlocks and **zero** write conflicts at 40
concurrent, and somebody is paid in every case, so it is a cap and not a wall. **24 of 24.**

### Deadlock — driven, not argued

A cycle needs one transaction holding campaign A while waiting for B and another the reverse. Almost
every caller runs **one clip per transaction** and takes exactly one campaign lock, which cannot be
half of a cycle. Exactly three sites loop inside one transaction and can touch several campaigns:
`payouts/[id]/adjust/route.ts:493`, `clip-account-cascade.ts:100` and `:484`.

That shape was built deliberately: two transactions, two campaigns, opposite order, each holding its
first lock 900 ms before asking for its second.

| measure | result |
| --- | --- |
| wall clock | **4,191 ms** (well inside the 60 s timeout — it resolved, it did not hang) |
| committed | 1 of 2 |
| aborted | 1 (Postgres detected the cycle and chose a victim) |
| clips left half-written | **0** — the victim lost its first write too |
| campaign spend vs surviving rows | $5.00 + $5.00 = $10.00, exactly what survived |

A refused admin action that can be retried is a better failure than a budget breach that cannot be
undone. **5 of 5.**

### Throughput — what the lock costs the tick

| measure | result |
| --- | --- |
| uncontended lock-and-commit, median of 30 real round trips | **99 ms** (min 97, max 126) |
| as a share of BL-872's 4.5 s per clip | **2.2 %** |
| worst case added across BL-872's 46-clip / 210 s tick | **≤ 4.6 s**, and that overstates it |
| a 3,000 ms holder, writer joining 300 ms in | waited **2,837 ms**, then proceeded |

The 4.6 s figure is an overstatement because it measures a whole extra transaction round trip, whereas
the tick's lock is one extra statement inside a transaction it was already opening.

**Can a slow writer starve the tick? No.** Postgres row locks are FIFO, so a waiter is granted the row
the instant the holder commits rather than being passed over. The bound on starvation is the bound on
how long any writer can hold a transaction open — the Prisma transaction timeout — and that was
already true for every other row these transactions lock. **The tick never queues behind itself**,
because it runs campaigns in parallel and the clips of one campaign sequentially, so its own
acquisitions are uncontended; this queue only ever forms between the tick and a human pressing a
button. **3 of 3.**

---

## PART 2 — The combination matrix, run inside the marketplace

Eight scenarios BL-898 named as uncovered, each against **a v2 clip with two earners**, each asked the
**same five questions by one shared battery** so no scenario could ask an easier version than its
neighbour.

The five: (1) do all three legs move together, (2) does the spend aggregate stay correct, (3) do both
paid floors hold independently, (4) does the budget still cap, (5) does the reconciliation report it
EXPLAINED rather than as a leak.

| # | scenario | outcome |
| --- | --- | --- |
| 1 | **Trainer in the stack** | The trainer's 10 % is taken at payout time from the trainee's own payout (`trainer-cut.ts`), never from a clip leg, so the clip arithmetic cannot see him. All five pass. |
| 2 | **Referrer** | A referred earner's legs are identical to an unreferred one's; the fee tier (`referredById ? 4 : 9`) is chosen at payout. All five pass. |
| 3 | **Express against standard** | On the same $45.00 poster leg: standard and express differ by the express premium, and **no leg changes** — express is a withdrawal choice. All five pass. |
| 4 | **Devaluation** | `payoutReductionRatio` on the clip moves **all three legs together**; the two 45 % legs still match and the platform leg is still the residual. All five pass. |
| 5 | **Freeze and unfreeze** | A freeze touches no money already earned; after unfreeze all three legs resume together on new views (the poster's leg is required to have RISEN, so a silent no-op would fail). All five pass. |
| 6 | **Retire and revive** | RETIRED refuses a NEW post (`createV2Post` selects only `status: "APPROVED"`, `marketplace-v2-poster.ts:626`) while leaving earned money exactly where it was; reviving lets the same call through. All five pass. |
| 7 | **Conversion and its undo** | Preview correctly answers **409 `ALREADY_CONVERTED`**; the undo restores the poster to the **whole gross** and **removes** the maker and platform rows; campaign spend is unchanged, so the undo moves money between people and creates none. All five pass. |
| 8 | **Role lock falling mid-flow** | The side gate allows then refuses across the flip, takes nothing back from work already done, and the clip **goes on earning** on the next tick. All five pass. |

**60 of 60.**

### Three of my own assertions were wrong and the product was right

1. **Conversion preview 409.** I allowed 200 or 400. The route's 409 `ALREADY_CONVERTED` is the
   correct answer for a clip that already has two earners. The check now asserts the **code** as well
   as the status, so a 409 arriving for another reason would not satisfy it.
2. **The undo.** I demanded the two 45 % legs still match afterwards. They must not: an undo
   un-marketplaces the clip, so it returns to **one earner on 100 %** and the other two rows are
   deleted. The check now asserts the poster's restored leg equals the gross all three summed to
   before, to the cent.
3. **The three-leg rule after an undo.** Same cause; the battery now runs before the undo, while the
   clip is still a v2 clip, and the undo has its own assertions.

### Two further harness defects the checks caught themselves

- `calculatePayoutBreakdown` takes **positional** arguments `(amount, feePercent, bonusPercent,
  express?, trainer?)`. I passed a named object, every field was ignored, and both nets came back
  `NaN` — caught because the check compares the two figures to each other and `NaN < NaN` is false.
- `payoutReductionRatio` lives on **`Clip`** (`schema.prisma:1102`), not `Campaign`. Prisma refused
  the write and the harness died rather than measuring a devaluation that had not happened.

---

## PART 3 — The paid-floor under-pricing: BL-898's reasoning does NOT hold

BL-898 wrote that when the maker's paid floor holds his leg above the derived target, the gate prices
that leg as falling where the truth is that it does not move, and judged this *"bounded and opposite
to budget pressure, since the floor only holds money already counted in spend and binds only when a
leg would fall."*

The claim was split into three parts and each tested separately.

| claim | verdict |
| --- | --- |
| **A** the floor binds only when the maker's leg would fall | **CONFIRMED.** Probed both directions against the live guard: a proposal above the floor passes untouched, one below is held. |
| **B** what it holds is already counted in spend | **CONFIRMED.** `getCampaignBudgetStatus` counts all three legs, so a held leg is money the budget has already paid for. |
| **C** therefore it cannot breach a budget | **FALSIFIED.** |

### The attack and the measurement

The maker's target **is** the poster's base (both shares are 0.45), so the floor binds exactly when
the poster's base falls, while the gate needs a positive delta, which normally means the poster is
rising. The one state where both hold: **the poster's base falling while his total rises** on a larger
bonus percentage.

A maker holding a **$45.00 PAID floor**, a campaign tightened to **$104.44** (its spend of $100.00 plus
the gate's own price), and a write with base $20.00 / total $80.00:

| measure | before the fix |
| --- | --- |
| what the gate priced the write at | **$4.44** (using a maker target of $20.00) |
| what the floor actually held the maker at | **$45.00** — a $25.00 gap |
| admitted? | **yes** |
| campaign landed at | **$129.44** against **$104.44** |
| **overshoot** | **$25.00** |

### The fix

Ask the same guard the write will ask, rather than approximating it:

```ts
let editorEffective = editorTarget;
const v2EditorId = (current as any).marketplaceV2EditorEarning?.editorId as string | undefined;
if (v2EditorId && editorTarget < editorBefore) {
  const { floorV2EditorEarnings } = await import("@/lib/marketplace-v2-writer");
  const held = await floorV2EditorEarnings(tx, { clipId, editorId: v2EditorId,
    campaignId: current.campaignId, proposed: editorTarget, current: editorBefore }, { ... });
  editorEffective = r2(held.written);
}
spendDelta = r2((posterAfter + editorEffective + platformTarget) - (...));
```

Plus **one column** added to a single-row lookup the function already performs:
`marketplaceV2EditorEarning: { select: { amount, bonusPercent, editorId } }`.

Deliberately **not** a defensive clamp at `editorBefore`, which would over-price every genuine decrease
and start refusing writes that ought to pass. The platform leg is deliberately **not** re-derived,
because `marketplace-v2-sync` computes it from the **unfloored** target and the three legs are meant to
stop summing to the gross when a floor binds — BL-849's chosen lesser harm, kept rather than quietly
corrected.

**It costs nothing on the ordinary path:** `floorV2EditorEarnings` returns on its first line when
`proposed >= current`, which is every rising write, issuing no query at all.

**After:** the same attack is **REFUSED**, with the lock naming the true figure — *"would push campaign
to $129.44 (budget $104.44)"*. Overshoot **$0.00**. **7 of 7.**

---

## PART 4 — Proof, guards, teardown

### The guard

`npm run check:budget-lock` (in `prebuild`) grows from seven checks to **nine**. Both new ones are
**order-and-identity** checks, not presence checks:

- **B8** — inside the delta block the campaign row lock must be taken **before** the committed-spend
  read. Scoped to the block, so *moving* the lock below the read fails it though nothing is deleted.
- **B9** — the `spendDelta` **summand** must name `editorEffective` and must **not** name the raw
  `editorTarget`. Scoped to the summand, so putting `editorTarget` back fails it even though the floor
  call above is still present.

### The demonstration found four defects, three of them pre-existing and serious

1. **B1, B2 and B8 were silently SKIPPED.** The anchors are written with `\n` and these files are
   **CRLF**, so every **multi-line** anchor matched **zero** times while every single-line one matched.
   **Three of nine checks had never been demonstrated.** The anchor is now translated to the line
   ending the file actually uses.
2. **B3's mutation also tripped B9**, so neither was shown to fail alone: B9's region ended at
   `const delta = spendDelta;` — the very line B3 rewrites — so the region collapsed. The boundary is
   now `const delta =`.
3. **B9's first scope** was the delta block, where none of the code it checks lives.
4. **B9's second scope** counted braces; a naive depth counter walking template literals closed early,
   so it saw the declaration of `editorEffective` but not the subtraction using it.

**Now 9 of 9 demonstrated failing, alone**, tree restored with identical sha256 after each, guard green
before and after. Both new mutations are deliberately subtle — B8's moves one statement, B9's changes
one identifier — because a mutation that deleted the lock outright would prove the check can fail
without proving it asks the right question.

### Full-population invariants — run AFTER teardown, on purpose

This round deliberately drove four sandbox campaigns past their budgets to reproduce the defect.
Running BL-627's invariant while those existed would have reported four breaches the round created on
purpose, and burying them in an exclusion list would have been worse.

| invariant | result |
| --- | --- |
| **BL-627 no overpayment, EVERY budgeted campaign** (both v2 aggregates included, `videoUnavailable = false`) | **20 campaigns, 0 over budget.** Closest real spender: "SomeSome App" at $1,410.59 of $2,214.00, **$803.41 under**. |
| **F-EARNINGS-INVARIANT across every clip** | **10,193 live clips, 0 violations, 0 negatives, 0 NaN** |
| **`V2_RECONCILE_SQL`** (leaks only) | 0 rows |
| **`V2_RECONCILE_ALL_SQL`** (every row with a verdict) | 0 rows |
| sandbox residue, asked by prefixed id **and** by owning column | 0 in every table |
| all four v2 tables | back at **0**, the count they held before the round |
| owner's test campaign `cmu5yeax20000h4w7yv5n387y` | present, ACTIVE, unarchived, $500.00 budget, 0 clips, **untouched** |

**Both reconciliation forms were run** — which BL-898 noted it did not do as a separate pass. Honestly:
after teardown the platform holds zero v2 clips, so a clean answer here is also a **trivial** one. The
form that proves the query still discriminates is the one inside PART 2, where **8 live v2 clips with
two earners each** were asked and each was reported EXPLAINED rather than as a leak. **7 of 7.**

### Teardown

**NOTHING IS UNREMOVABLE. 0 of 1,743 recorded rows remain.**

Prefix `bl901sbx-`, opening snapshot taken before anything was created. 1,740 deleted, 3 already gone
by cascade, 0 failed. Product-written rows were adopted by `sweep.ts` (4 adopted) before destruction;
`marketplace_v2_*`, `campaign_accounts`, `clip_stats` and `tracking_jobs` all `ON DELETE CASCADE` from
rows the ledger names, verified in `information_schema` before destroying.

| table | opening | closing | delta | explanation |
| --- | --- | --- | --- | --- |
| users | 1,766 | 1,766 | 0 | — |
| campaigns | 35 | 35 | 0 | — |
| clip_accounts | 1,527 | 1,527 | 0 | — |
| campaign_accounts | 807 | 807 | 0 | BL-889 upserts all cascaded away |
| trainer_relationships | 0 | 0 | 0 | — |
| marketplace_v2_clips / posts / editor / platform | 0 / 0 / 0 / 0 | **0 / 0 / 0 / 0** | 0 | — |
| clips | 10,269 | 10,276 | +7 | real clippers submitted; 0 touch a sandbox id |
| tracking_jobs | 10,230 | 10,237 | +7 | matches the 7 real clips exactly |
| clip_stats | 381,021 | 381,085 | +64 | the cron writing view snapshots |
| payout_requests | 249 | 250 | +1 | one real payout; **0 touch a sandbox user** |
| audit_logs | 29,620 | 29,812 | +192 | live platform activity |
| sum(clip earnings) | $19,246.78 | $19,252.50 | +$5.72 | real cron earnings on real clips |

`verify-gone.ts` reported 19 of 21 passing. Both failures are **framework artefacts, not residue**:
I never ran its `snapshot.ts before`, so it fell back to a 2026-09-06 window and attributed **30 real
users' payouts over 12 days** to this round. Measured directly against the true round window
(15:21 UTC onward): **1** payout created, and **0** payouts touch any sandbox user.

### Worktree

**No worktree was created this round.** `git worktree list` shows only the main checkout, so there is
nothing to remove and the requirement is satisfied vacuously rather than by a cleanup. The BL-899
sweep was run as required: it kept all six directories it found, every one refused for being under its
3-day floor or not being round telemetry — **0 MB reclaimed across 0 directories, which is the safe
answer.**

### Gates and money files

- `npm run build` exit **0** on the branch and again on `main` after the merge.
- 18 prebuild checks green, including **9 of 9** budget-lock checks.
- BL-348 hooks gate: **0 errors, 11 warnings** — identical to the pre-round baseline of 11.
- `eslint` confirmed present in `node_modules/.bin`, so the gate did not silently no-op.
- **Eleven protected money files byte-identical by blob OID** (`pre-BL-901` vs `main`).
  `tracking.ts` appears in **no** diff.
- **One** money file changed — `clip-earnings-writer.ts`, `b9d3a405…` → `416972e9…` — which is this
  round's purpose.
- **Zero `.tsx` changed**, so no render or accessibility pass was owed or run.
- No Apify actor ran: `APIFY_HARD_OFF` is a `const true` (`apify-hard-off.ts:32`) that reads no
  environment variable, and the 11 BL-678 guards are intact. TikTok freshness fails open with no
  external call.
- No wallet address appears anywhere; the required `walletAddress` column was written with a sandbox
  marker.

---

## Not run, and named

1. **50 concurrent writers is not measurable on this pool.** The web pool is `max: 48`
   (`src/lib/db.ts:107`) and each interactive transaction holds one connection for its life, so fifty
   racers exhausted it and **all fifty failed with no budget movement at all** — a pool failure
   wearing a budget failure's clothes. Forty is BL-898's own figure, sits inside the pool, and is what
   was measured.
2. **A single transaction that writes MANY clips still under-counts its own earlier writes.**
   `payouts/[id]/adjust/route.ts:493` and `clip-account-cascade.ts:100` / `:484` write several clips
   in one transaction; the gate reads COMMITTED spend, and those earlier writes are not committed yet.
   **Pre-existing, unrelated to the row lock, and not introduced by this round.** Reported rather than
   half-fixed hours from a launch.
3. **Every other guard demonstration on this platform should be audited for the same CRLF blindness**
   that hid three of nine checks here. Not done in this round.
4. **The referral percentage was not built**, as instructed.

---

## Rollback

`git revert b87ac4ea`. The round adds one SQL statement and one guard call and changes **no
arithmetic**, so **no stored figure changes** and no recompute is needed. Both launch flags are unset
and were not touched.
