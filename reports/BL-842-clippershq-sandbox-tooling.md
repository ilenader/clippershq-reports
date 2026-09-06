# BL-842: a sandbox that reproduces defects instead of passing tests

**2026-09-06 · DB `now()` = `2026-09-06 12:17:48.918854+00` (first read) to `2026-09-06 12:39:43.883182+00` (destroy) · BUILD AND MERGE.**
Base `origin/main` @ `febfc88f`. Branch `checkpoint/BL-842` @ `a081132`. **Merged and verified pushed: `origin/main == local == efbb20c`.** Tags `pre-BL-842`, `post-BL-842`, `pre-BL-842-merge`, `post-BL-842-merge`, all on origin. Isolated worktree `C:/w842`, a short path, `node_modules` never junctioned, **removed at the end**. Every timestamp cast `::text` against DB `now()`. Handles redacted; no wallet address read or printed.

**A REDEPLOY ON RAILWAY IS REQUIRED BEFORE ANY OF THIS IS LIVE**, although nothing here runs in production: the entire diff is `scripts/`, `BACKLOG.md` and a README.

> ## THE HEADLINE
> **BOTH DEFECTS BL-841 FOUND WERE REPRODUCED, AND ONE OF THEM CREATED MONEY FROM NOTHING IN FRONT OF ME.** Two concurrent posts of different URLs for the same platform on one submission both returned **201** and produced **two `MarketplaceClipPost` rows and two earning `Clip` rows for one slot**, with `postedPlatforms` reading `{TIKTOK,TIKTOK}`. A poster who did nothing wrong was refused **400** because our fetch failed, nothing was recorded about the attempt, and one moved timestamp later the same sweep wrote `MISSED_POST_DEADLINE` against him. **Neither is fixed here, deliberately.**
> **AND THE DESTROYER REFUSED MY OWN LEDGER TWICE AND DELETED NOTHING BOTH TIMES.** That is the best thing that happened in this round.

> **I ALSO HAVE TO CORRECT MYSELF.** BL-841 stated that BL-840's sandbox tooling did not exist for this project. **That was true of the commit BL-841 audited, `7075e6a3`, and BL-840 merged afterwards at `febfc88f`.** `scripts/sandbox/` exists, it is well built, and this round **extends it rather than writing a second one**.

---

## PART 0: THE ISOLATION MODEL, AND WHY THE PREFERRED ANSWER IS THE WRONG ONE HERE

| option | verdict |
|---|---|
| **a separate database** | **Not achievable, and more importantly not faithful.** See below |
| **marked rows in the production database** | **CHOSEN** |

**Availability first, because it is the easy half.** There is no `psql`, no `pg_dump` and no `postgres` binary on this machine. The Docker CLI is present but **the daemon is not running** (`failed to connect to the docker API ... the daemon`). A second Supabase project is an owner action with a cost. And the schema is maintained by 25 manual SQL migrations with `prisma migrate` forbidden by house rules, so standing one up is not one command.

**But the decisive argument points the other way, and it is not about convenience.**

> **THE DEFECT THIS ROUND EXISTS TO REPRODUCE IS A DIVERGENCE BETWEEN `schema.prisma` AND THE LIVE DATABASE.** The schema declares `@@unique([submissionId, platform])` and asserts in its own comment that the index "is applied out-of-band by the owner". It never was. **A fresh database stood up from that same schema file WOULD CREATE THE INDEX.** The second post would be refused, the round would report a green sandbox, and the sandbox would have been structurally incapable of finding the very thing it was built to find.
> **A separate database cannot reproduce schema-versus-database drift by construction.** The production database is the only place the defect exists, because the defect *is* the difference between the two.

**The residual risk, stated plainly:** sandbox rows sit beside real ones and only the locks keep them apart. That risk is why PART 0's second half is an attack rather than an assertion.

### The safeguard, proven by attempting what must be refused

`scripts/sandbox/refusal.ts`, **21 checks, 0 failures.** Every one ATTEMPTS the forbidden thing.

```
a hand edited ledger naming a REAL owner id is refused          x3, one per live OWNER
  LEDGER REFUSED: id "cmnd5taio00418ww71ul9c5wm" does not carry the sandbox prefix...
a product row claiming a REAL owner is refused
  LEDGER REFUSED: product row "cmtkbqbik..." claims owner "cmn4m6lh6...", not a sandbox id
a table that is not on the deletable list is refused            strike_config
strike_config is deliberately NOT deletable                     a production singleton
a real owner id does not read as a sandbox id                   x3
a legacy isTestUser fixture is refused                          bl833-watch-only
mp-create.ts refuses without BL842_SANDBOX_CONFIRM              exit 2
destroy.ts   refuses without BL842_SANDBOX_CONFIRM              exit 2
SANDBOX_ROUND "../../etc", "BL 842", "a", 40 chars              all throw at import
switching to a REAL owner id is refused BY NAME                 x3, ledger populated
switching to a REAL clipper cuid is refused                     cmtkbqbik...
switching to a legacy isTestUser fixture is refused             bl833-watch-only
```

**The role-switch refusals were re-run after the ledger was populated**, because an empty ledger refuses everything for the wrong reason. With two sandbox people present the refusal reads *"REFUSED. No sandbox user is labelled ... This tool cannot name a user any other way: there is no id argument. Known labels: poster, clipper"*.

---

## PART 1: INVISIBLE TO REAL PEOPLE, AND THE CRON THAT WOULD HAVE SPENT REAL MONEY

`invisible.ts` run **live, with every sandbox row present**, acting as a **REAL clipper with 839 approved clips**, read only. **14 checks, 14 passed, 0 failed.**

| surface | answered | carries a sandbox id, prefix, marker or person |
|---|---|---|
| the campaign list | 200, 20,506 bytes | **no** |
| past campaigns | 200, 5,541 bytes | **no** |
| the cross-campaign spend map, the one BL-840 had to fix | 200, 471 bytes | **no** |
| his earnings and per-campaign balances | 200, 100,994 bytes | **no** |
| his own clips | 200, 1,937,902 bytes | **no** |
| the global top-ten leaderboard | 200, 566 bytes | **no** |
| his referrals | 200, 103 bytes | **no** |

### THE CRON WOULD HAVE POLLED THE SANDBOX AND SPENT REAL MONEY

**`tracking.ts` contains the string `isTestCampaign` ZERO TIMES.** The tick does not filter test campaigns. And `post/route.ts:751-759` creates a `TrackingJob` with **`nextCheckAt: new Date()` and `isActive: true`**, so the next tick, at most ten minutes away, would have polled a sandbox marketplace clip against HikerAPI or LamaTok at real cost. BL-838 measured Instagram at roughly $139 a month.

**BL-840 never met this because it created no tracking jobs.** This round's scenario deactivates them in the same script, one statement after the product creates them, and then proves it:

| | measured |
|---|---|
| tracking jobs the product created for sandbox clips | **2** |
| of those, still **ACTIVE** | **0** |
| `clip_stats` rows on sandbox clips | 2, the seed rows the post route writes |
| **`apify_usage_entries` rows in the whole window** | **0** |

**Not one vendor call was made for a sandbox clip.** The scenario also ran with `LAMATOK_KEY`, `HIKERAPI_KEY` and `EMAIL_API_KEY` unset, disclosed in PART 5.

---

## PART 2: TIME, AND WHETHER THE PRODUCTION CODE SEES IT

**The technique is to move the DATA, not the clock.** A route computing `now - row.deadline` and a route computing `(now + 31 days) - row.deadline` perform the identical subtraction, so shifting the row back and shifting the clock forward are the same event. **It is the production code's own comparison that changes**, which is the only sense of "the code under test sees it" that means anything.

### Why not a fake clock: the database defeats it, measured

| | count | who stamps it |
|---|---|---|
| columns with `@default(now())` | **82** | **Postgres**, emitted as `DEFAULT CURRENT_TIMESTAMP` in the repo's own DDL |
| columns with `@updatedAt` | **27** | **the client**, no DB default and **0** triggers anywhere in the migrations |
| executed raw SQL calling `now()` | **17** | Postgres, including both cron locks |

A patched server would write rows whose `updatedAt` **precedes** their `createdAt` by the offset, and compare a DB-stamped cron lock against a patched `new Date()`, reading every lock as permanently stale or permanently fresh. **That is not a simulation, it is a server arguing with its own rows.** A threaded `clock.ts` seam was also costed: **113 clock reads** in the paths that matter, **80 of them, 71 percent, inside `tracking.ts`**, a money file that must stay byte identical. A seam that stops at that boundary gives a server where the marketplace believes one date and the tracking cron believes another.

### Proven, 7 checks, 0 failures

```
PASS  with expiry in the FUTURE the sweep leaves it alone
      status=PENDING expiresAt=2026-09-07T12:34:53.687Z processed=0
PASS  with ONLY that column moved, the SAME sweep expires it
      status=EXPIRED expiresAt=2026-09-06T11:34:55.082Z processed=1
PASS  the transition was caused by the timestamp and not by the second call
PASS  a clip   1 hour old  is polled on the  60 minute rung
PASS  a clip  30 hours old is polled on the 120 minute rung
PASS  a clip 100 hours old is polled on the 240 minute rung
PASS  a clip  30 days old  is polled on the dynamic rung
```

The first three are `processMarketplaceTimers`, the **real sweep the tracking cron calls at `tracking.ts:4295`**, invoked twice on the same row with one column moved between. The last four are `getLockedIntervalFloor`, which reads `Date.now()` itself, so the age comes entirely from the row.

### What it cannot reach, named rather than glossed

* **The `:00` UTC batch gate.** `tracking.ts:3473` compares the wall clock to a constant with no row in it. The run printed *"It is currently minute 34"* beside the assertion. The only way past is the pre-existing caller override `runDueTrackingJobs({ isBatchTick })`, **which is a production argument and NOT simulated time.**
* **The 30 minute freshness rule at the live submit path**, which compares against a timestamp fetched from the provider, not from a row.
* **A write-time duration as it is written.** `postDeadline = approvedAt + 24h` is stamped by the route; it can only be moved afterwards.
* **Intra-request budgets**, the 8 minute tick deadline and similar.

**So every claim is phrased as "the route decides X for a row of age N", never as "a month passed".**

---

## PART 3: ROLE SWITCHING THAT CANNOT IMPERSONATE

`as.ts` **has no id argument.** You pass a role label; the label is resolved against the **ledger**, which holds exactly the rows this round created. A real id is not in the ledger and no code path reads one from anywhere else, so **the refusal is the absence of an input channel rather than a check somebody can delete.** Before minting it re-reads the row by primary key and requires the prefix (LOCK 2) and the visible marker (LOCK 3) to still be present.

Proven working as well as refusing: the poster's minted session answers **200** on `/api/marketplace/submissions/incoming`, the poster-only route, and **200** on `/api/clips/mine`.

> ### A LIVE FALSE COMFORT FOUND AND REPORTED, NOT FIXED
> **`scripts/bl839-mint-owner.ts:21-25`** selects `findFirst({ role: "OWNER", isTestUser: true })` and throws a message reading *"no isTestUser OWNER; refusing to act as the real owner"*. Measured this round:
>
> | id | handle | role | isTestUser | audit rows | campaigns |
> |---|---|---|---|---|---|
> | `cmn4m6lh6...` | `anka..85` | OWNER | **true** | **5,054** | 9 |
> | `cmn7d5hrv...` | `dani..20` | OWNER | false | 1,299 | 1 |
> | `cmnd5taio...` | `bane..4.` | OWNER | false | 4,062 | 9 |
>
> **The only `isTestUser` OWNER IS the real owner**, the oldest account on the platform. That script mints a session for him while printing that it refused to. **`isTestUser` is not a sandbox marker: 8 live rows carry it.** The reliable marker is the minted id prefix, because no real row can carry a prefix a script chose afterwards.

**What was deliberately NOT built, and the reason is in the file rather than left to be discovered.** The strictly stronger design is a second cookie that `getSession()` resolves server side, plus a module-init throw refusing to boot a production build with it enabled; then editing the mint script buys nothing. **It was rejected because it puts a new authentication branch into production code, and a sandbox is not worth widening the auth surface of a platform that pays people money.**

---

## PART 4: TEARDOWN, AND THE TWO REFUSALS THAT WERE THE POINT

**30 rows deleted by primary key, in dependency order. 0 already gone. 0 FAILED. 0 of 30 remaining.**

```
marketplace_strikes 1 · marketplace_clip_posts 2 · marketplace_submissions 3
marketplace_listing_accounts 2 · marketplace_poster_listings 1 · tracking_jobs 2
clips 2 · campaign_accounts 2 · clip_accounts 2 · notifications 5 · audit_logs 5
campaigns 1 · users 2
```

**Never by pattern, never by name, never by date.** Every id was recorded with `appendFileSync` at the instant of creation. The ledger went 12 rows at creation, 32 after the scenario and the sweep adopted what the product wrote, and 30 after two `clip_stats` lines were dropped for the reason below.

**The audit-log cascade fix was verified LIVE immediately before any user was deleted**, as the brief requires:

```
audit_logs_userId_fkey   confdeltype = n
  FOREIGN KEY ("userId") REFERENCES users(id) ON UPDATE CASCADE ON DELETE SET NULL
```

BL-837's fix is in place. **Had it still been `CASCADE`, deleting the sandbox users would have ERASED their five audit rows rather than orphaning them**, and the round would have destroyed the evidence of its own actions. Because it is `SET NULL`, those rows had to be deleted explicitly first, which is why `audit_logs` sits above `users` in `DELETABLE_TABLES`.

### THE DESTROYER REFUSED THE WHOLE LEDGER TWICE AND DELETED NOTHING BOTH TIMES

Both times **my** ledger lines were wrong, and both times the lock behaved exactly as designed.

**Refusal one.** Audit rows adopted with `ownerColumn: "id"`, which names the row's own cuid rather than a column holding a sandbox id.
```
LEDGER REFUSED: product row "cmtpsn3n6..." claims owner "cmtpsn3lb...", which is not a
sandbox id. Nothing has been deleted.
```

**Refusal two, and this one is a real limit in LOCK 3 found by LOCK 3.** A `clip_stats` row's only link is `clipId`, and on the marketplace path **the PRODUCT mints the clip**, so **no column on the stat row holds a sandbox id at all**. BL-840 never met this because it minted its own clips.

**The lock was NOT loosened.** `clip_stats.clipId` is `ON DELETE CASCADE`, so those rows go with their clip and the ledger does not need to name them. `repair-ledger.ts` **drops** such a line rather than repairing it and says so, and `verify-gone` still proves none survived. `repair-ledger.ts` only ever makes a line **more** restrictive: it reads the replacement value **from the database** and refuses unless it is a sandbox id, and it keeps the original file as `.before-repair`.

**If teardown had not completed**, the ledger names every id and `destroy.ts` prints each refusal with its reason. It did complete, so no removal SQL is owed and none is offered.

---

## PART 5: BOTH DEFECTS REPRODUCED

**12 checks, 0 failures.** Against the **production build** on port 3842, `DEV_AUTH_BYPASS=false`, real minted sessions.

### DEFECT A: money from nothing, demonstrated

```
PASS  the unique index the schema declares is absent from the database
      unique indexes covering (submissionId, platform): 0
  firing both posts at once on submission bl842sbx-sub-a-95cc68b1
  response 1: http 201 in 5673 ms
  response 2: http 201 in 5634 ms
PASS  both posts were accepted                          http 201 and 201
PASS  TWO MarketplaceClipPost rows for ONE (submission, platform)   rows=2 TIKTOK,TIKTOK
PASS  TWO earning Clip rows exist for one slot           clips=2 PENDING,PENDING
PASS  the two clips carry DIFFERENT urls                 2 distinct normalizedUrl
PASS  postedPlatforms carries the duplicate              ["TIKTOK","TIKTOK"]
>>> DEFECT A REPRODUCED
```

**One slot, two earning clips, two tracking jobs, and `totalPosted` incremented twice.** The `P2002` handler at `post/route.ts:771` is unreachable code because Prisma does not enforce `@@unique` at runtime and the transaction at `:560` takes no `isolationLevel`.

### DEFECT B: a poster struck because our fetch failed

```
  response: http 400   "We could not verify when this Instagram clip was posted."
PASS  the poster is refused because OUR fetch failed, not because they did not post
PASS  NOTHING was recorded about the refused attempt      clip posts 0, audit rows 0
PASS  with the deadline in the FUTURE the sweep does nothing        strikes 0
PASS  with ONLY that one timestamp moved, the SAME sweep strikes him
      strikes=1 reason=MISSED_POST_DEADLINE status=ACTIVE
PASS  the submission is flipped to POST_EXPIRED
PASS  the strike names the sandbox submission and listing
>>> DEFECT B REPRODUCED
```

**NEITHER DEFECT WAS FIXED.** That is a separate round with its own money proofs. Reproducing them is the proof that the tooling is faithful, and a sandbox that could not reproduce a known defect would have to be reported as unfaithful rather than declared working.

### The provider keys were unset, and here is exactly what that costs the claim

The server and the scripts ran with **`LAMATOK_KEY`, `HIKERAPI_KEY` and `EMAIL_API_KEY` unset**.

* **For defect A** the freshness gate is passed through TikTok's lenient throw branch at `post/route.ts:106`, **which is the same branch a real provider outage reaches**. With the keys set, a junk TikTok URL would cost one LamaTok call, return null, fall through the same chain and throw in the same place. **Unsetting the key removes the spend, not the path.** The defect itself lives entirely downstream, inside the transaction.
* **For defect B the failing gate IS the defect**, and an absent provider is one of the exact conditions BL-841 named.

> ### DISCLOSED BECAUSE IT WAS MY OWN MISTAKE: ONE REAL EMAIL REQUEST WAS MADE
> Unsetting `EMAIL_API_KEY` on the **server** did not stop `marketplace-timers.ts:319`, because `processMarketplaceTimers` ran in the **script** process, which loads `.env.local`.
> ```
> [EMAIL FAIL] status=403 body={"statusCode":403,"name":"validation_error",
> "message":"You can only send testing emails to your own email address..."}
> ```
> **Resend REFUSED it and nothing was delivered.** The sandbox addresses are `.invalid`, reserved by RFC 2606, so nothing could have been delivered anyway. The scripts now delete the variable before any production import, and the README says why.

---

## PART 6: THE DOCUMENTATION

`scripts/sandbox/README.md` is rewritten. It covers how to create a sandbox, the server flags, what every file does, the four locks and the attack that proves them, time and its four hard limits, role switching and why the stronger design was refused, the tracking-cron money hazard, how to reuse it for another feature, and a section headed **what this must never be used for**.

**And the section that makes it trustworthy: WHAT THE SANDBOX DOES NOT REPRODUCE.** A passing sandbox test does not prove anything gated on the `:00` UTC wall clock, real provider behaviour on a **successful** fetch, real email or Discord or Apify, concurrency at production scale, anything about a screen unless `render.mjs` ran, **or anything at all about the 9,422 real clips sitting beside the sandbox rows.**

---

## PART 7: NOTHING REAL MOVED

`verify-gone.ts`: **50 CHECKS, 50 PASSED, 0 FAILED.**

| | before | after |
|---|---|---|
| **real payout fingerprint** | `0b4194dc4211a30fb552290b247f85e6` | **identical** |
| **real user fingerprint** | `1e524212ea7d23c9fe820b21ffc100cb` | **identical** |
| **real clip status fingerprint** | `3cad8870d991400df7c39396024ea449` | **identical** |
| real clips / payouts / users / campaigns | 9,422 / 220 / 1,673 / 34 | **identical** |
| clips · clip_stats · tracking_jobs · audit_logs | 9,422 · 343,050 · 9,383 · 27,088 | **identical** |
| payout gross · paid gross | 19,995.61 · 11,726.45 | **identical** |
| over-payable holders · double-open payouts | 18 · 0 | **identical** |
| **earnings invariant violations** | **0** | **0** |
| approved earnings | 13,059.55 | **identical** |

**No real vendor call was made for a sandbox clip: 0 `apify_usage_entries` rows in the window.** Notifications moved 14,073 to 14,074, which is live traffic; the round's own five were deleted. The live platform did its own work throughout, named rather than smoothed: **14 clips submitted by 5 real clippers, 748 view snapshots by the cron, 1 real signup, 0 payouts created, 59 audit rows.**

### Gates, honestly

| | |
|---|---|
| clean `tsc` baseline on the **untouched** tree | **stashed the two in-progress edits first**, so it is genuinely pristine: exit **0**, `grep -c "error TS"` = **0** |
| `npm ci` / `npx prisma generate` | **0** / **0** |
| `npx tsc --noEmit`, final | exit **0**, **0** errors |
| `npm run build` **twice** | **`BUILD1_EXIT=0`**, **`BUILD2_EXIT=0`**, exit codes echoed by hand into a log, never piped through `tail` |
| BL-348 hooks gate | **0 errors, 10 warnings**, under the 11 ceiling. `eslint` confirmed present first |
| prebuild | `check:prisma-bypass` and `check:removed-fields` ran in both builds |

### Merged

| | |
|---|---|
| branch | `checkpoint/BL-842` @ **`a081132`**, verified on origin by `safe-push` |
| merge commit | **`efbb20c`**, `origin/main == local` verified by `safe-push` |
| conflicts | **none.** main never moved from `febfc88f`, and the **merged tree OID equals the branch tree OID exactly** (`3f2812889a5f`), so the branch's green build IS the merge's build |
| conflict markers across every `.ts`, `.tsx`, `.md`, `.prisma` and `.sql` | **0 files** |
| BACKLOG | **174 sections before, 175 after**, counted with `grep -c`, never piped to `head` |
| **`checkpoint/BL-723`** | **confirmed NOT an ancestor** |

### Safety

| | |
|---|---|
| the 6 money files plus `campaign-era.ts`, `apify.ts`, `apify-hard-off.ts` and `prisma/schema.prisma` | **byte-identical by blob OID on BOTH refs**: `ac5be7de`, `797e2098`, `81a683c1`, `359bcbbe`, `61cef393`, `ef5cdae7`, `106e16ad`, `d66d4534`, `29258a5d`, `7cec76ce` |
| schema | **no change**, no `prisma migrate`, no index created. **The missing unique index was measured and NOT created** |
| Apify | **no actor run**; the `APIFY_HARD_OFF` guards intact |
| the diff | `scripts/sandbox/` and `BACKLOG.md` only. **Not one file under `src/`** |
| pool discipline | one statement per snapshot, sequential scripts, no parallel database work |

---

## WHAT I WOULD TELL THE NEXT ROUND

1. **The two defects are still there and now have a repeatable reproduction.** `mp-create.ts` then `mp-defects.ts` puts both in front of you in under a minute.
2. **`bl839-mint-owner.ts` should stop claiming it refuses.** One line, and it is the check `as.ts` was written with.
3. **The tracking cron does not filter test campaigns.** That is a live cost surface for every future sandbox and arguably for the platform.
4. **LOCK 3 cannot prove ownership two hops out.** Today that is covered by a cascade. If a future round needs to delete a grandchild row that does not cascade, the lock needs a chain check rather than a relaxation.

**WHAT COULD NOT BE MEASURED:** whether the reproduction is deterministic rather than merely reliable, since it depends on Node interleaving two transactions at their `await` points; it worked on the first attempt and both responses took about 5.6 seconds, but two runs is not a distribution. And the sandbox says nothing about whether a **successful** provider fetch behaves correctly, because no provider was configured.
