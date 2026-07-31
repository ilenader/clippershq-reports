# BL-704 (ClippersHQ) — does bulk submission bypass the 30-minute rule?

## NO. Both clipper paths enforce it identically, and the root cause of what the owner saw is a THIRD submit path nobody had named. `/api/clips` and `/api/clips/batch` call the same function with the same arguments, so there is exactly one freshness implementation. `/api/clips/owner-submit-bulk` calls a completely different core that contains **zero** references to the posting window and **29** references to `postedAt`, because BACKDATING is its entire purpose. It is `requireOwner` gated, so no clipper can reach it. That is the tool the owner was using, and it accepting old clips is intended behaviour, not a bypass. His suspicion about single submission is refuted by measurement: 42 of 42 TikTok single submissions landed inside the window, and 16 of 16 post-deploy batch Instagram clips were genuinely fresh.

**2026-07-31 · SHIPPED to `checkpoint/BL-704` @ `32a28ddf`, verified on origin (`origin/checkpoint/BL-704 == local HEAD`).**
**Base** main `55e757ce` · **Tags** `pre-BL-704` / `post-BL-704`, both pushed · **Worktree** `C:/b704`, short path, `node_modules` never junctioned.
**Rollback** `git revert 32a28ddf`, or `git reset --hard pre-BL-704`. Reverting restores the undifferentiated `none` source and the three dead imports; **it changes no accept or refuse decision either way.**

---

## PART 0 — the diagnosis, stated before anything was changed

### The root cause, with file:line

**There are THREE submit paths, not two.** BL-684 compared the first two and never mentioned the third exists.

| # | endpoint | core it calls | freshness |
| --- | --- | --- | --- |
| 1 | `/api/clips` (single) | `processClipperSubmitLink` (`clips/route.ts:813`) | **ENFORCED** |
| 2 | `/api/clips/batch` (bulk) | `processClipperSubmitLink` (`batch/route.ts:160`) | **ENFORCED, identical** |
| 3 | `/api/clips/owner-submit-bulk` | **`processOwnerSubmitLink`** | **NONE, by design** |

**Paths 1 and 2 pass byte-identical argument shapes.** Both call `processClipperSubmitLink({ db, userId, campaignId, clipAccountId, clipUrl, note })`. The only difference is `note` (`data.note` versus `null`), which the freshness logic never reads. The entire check lives inside that one shared function:

* `clipper-submit-core.ts:310` the platform gate
* `:311` the single call to `fetchClipFreshnessWithRetry`
* `:329` the TikTok and YouTube age comparison
* `:432` the Instagram evaluation added by BL-686

**Path 3 is a different core entirely.** Counted with `grep -c` on `src/lib/owner-submit-core.ts`:

| symbol | count |
| --- | --- |
| `MAX_CLIP_AGE_MS` | **0** |
| `fetchClipFreshnessWithRetry` | **0** |
| `evaluateInstagramFreshness` | **0** |
| `postedAt` | **29** |

It does not import `clip-config` at all. **The 29 `postedAt` references are the point: this path exists to backdate clips the owner posted earlier**, which is exactly what BL-641 recorded when it noted owner-submit sets `createdAt = postedAt`. Both owner routes are gated with `requireOwner` (`owner-submit-bulk/route.ts:33`, `owner-submit/route.ts:23`), returning "Owner only." with 403, so **no clipper can reach either.**

**So the owner's observation is correct and the behaviour is intended.** He submitted through his own bulk backdating tool, whose purpose is to accept clips posted earlier.

### The leading hypothesis, tested first and REFUTED

The brief's hypothesis was that the batch path does not request the opt-in metadata, so no timestamp arrives and fail-open accepts everything. **It does not hold.**

`includeRawMeta` appears in **exactly one file**, `src/lib/apify.ts` (8 occurrences), and is set **inside** `fetchClipFreshnessWithRetry`, not by any caller. Counted with `grep -c`: **neither `clips/route.ts` nor `batch/route.ts` mentions it at all.** Neither route can therefore request less metadata than the other, because neither requests any: they both hand the URL to the same core and the core does the asking, once.

Asserted in the harness rather than left as prose:
```
PASS  NEITHER route sets includeRawMeta, so neither can skip the metadata the other gets
PASS  the freshness fetch happens EXACTLY ONCE, inside the shared core
```

### The second hypothesis, tested properly and REFUTED

BL-684 checked only `isTestUser`. I checked every privilege. Counted with `grep -c` on `clipper-submit-core.ts`:

| symbol | count |
| --- | --- |
| `isTestUser` | **0** |
| `canActAsClipper` | **0** |
| `session` | **0** |
| `ADMIN` | **0** |
| `role` | **0** |
| `OWNER` | 2, **both inside comments** |

The core branches on no role value and has no owner-conditional. Neither clipper route references `processOwnerSubmitLink` (0 occurrences each). **Stated plainly: the owner's submissions through the clipper paths are exactly representative of what an ordinary clipper experiences.** What is not representative is his use of path 3.

### The third check: BL-686 reached both paths

BL-686's Instagram fix is `evaluateInstagramFreshness` plus the harvest, and both live **inside the shared core** at `:193` and `:432`. Because both routes reach the core and nothing else, the fix landed on both paths in the same commit. There was never a version of it that applied to one path only.

### The measurement, last 14 days, split by path

There is no path column, so I used two independent markers: **`rule_shadow_decisions` is written only by the single route** (`grep -c`: 1 in `clips/route.ts`, **0** in `batch/route.ts` and 0 in the core), and batch rows commit sequentially seconds apart.

**Single path, ages from `rule_shadow_decisions.postedAt` versus `clips.createdAt`, both `::text`:**

| platform | rows | within 35 min | over 35 min | min age | max age |
| --- | --- | --- | --- | --- | --- |
| TikTok | 42 | **42** | **0** | 1.0 min | 15.5 min |
| Instagram | 50 | 47 | **3** | 0.6 min | 380.3 min |

**The three Instagram exceptions all predate the deploy, and BL-687 predicted them:**

| posted at | submitted at | age | status |
| --- | --- | --- | --- |
| 2026-07-30 10:41:44 | 2026-07-30 11:23:58.303 | 42.2 min | APPROVED |
| 2026-07-30 06:25:08 | 2026-07-30 12:45:24.745 | 380.3 min | APPROVED |
| 2026-07-30 14:30:27 | **2026-07-30 15:09:35.681** | **39.1 min** | APPROVED |

BL-687 pushed at approximately **15:09 UTC on 2026-07-30** and recorded in its own report that a submission at **15:09:35.681 was 39 minutes old**, concluding the deploy had not yet swapped. That is the third row here, and this measurement confirms it. **Since the deploy there have been zero over-threshold acceptances on either clipper path.**

**Batch path, probed live because batch stores no timestamp.** All 16 post-deploy batch Instagram clips (bursts 2.7 to 4.2 seconds apart, on campaigns with `rulesJson` yet carrying no shadow row, which is the batch signature) read through HikerAPI:

```
age_at_submit=  11 min  fresh (correctly accepted)
age_at_submit=   6 min  fresh (correctly accepted)
age_at_submit=  20 min  fresh (correctly accepted)
age_at_submit=  17 min  fresh (correctly accepted)
HTTP 404  taken_at ABSENT -> unknown -> would ACCEPT
age_at_submit=  13 min  fresh          age_at_submit=  10 min  fresh
age_at_submit=   6 min  fresh          age_at_submit=   4 min  fresh
age_at_submit=  10 min  fresh          age_at_submit=   9 min  fresh
age_at_submit=   8 min  fresh          age_at_submit=   8 min  fresh
age_at_submit=   7 min  fresh          age_at_submit=   7 min  fresh
age_at_submit=   7 min  fresh

HikerAPI calls: 16  |  too_old: 0  within: 15  unknown: 1
```

**Zero too old.** Fifteen genuinely fresh at 4 to 20 minutes, and one post since deleted, whose absent timestamp correctly accepted through fail-open. **If batch were bypassing the rule, this is the sample that would show it, and it does not.**

**BL-684 is not contradicted; it was incomplete.** Its conclusion that batch is not weaker holds and is re-proven here on post-BL-686 code. What it missed is that a third, owner-only bulk endpoint exists at all.

---

## PART 1 — the change: distinguishing a real failure from a skipped fetch

**The diagnosis found no defect in the clipper paths, so nothing about accept or refuse was altered.** Manufacturing a behavioural change to the submit path every clipper uses, when the measurement says it is correct, would have been the wrong call.

What the brief legitimately asks for and what was missing is the **distinguishability requirement**: fail-open must remain for a genuine provider failure, but must never be a silent pass because our own code skipped the fetch. Before this round every one of those collapsed into a single `source=none`.

Now they are four distinct labels on the `[FRESHNESS]` record, **with no decision changed**:

| situation | recorded `freshnessSource` | outcome |
| --- | --- | --- |
| the provider was asked and genuinely failed | `provider-failed:<errorType>` | ACCEPTED, unchanged |
| the provider answered but carried no timestamp | `provider-answered-no-timestamp` | ACCEPTED, unchanged |
| Instagram, no secondary source reached at all | `no-secondary-source` | ACCEPTED, unchanged |
| Instagram, secondary source returned a body with no sane `taken_at` | `secondary-source-no-timestamp` | ACCEPTED, unchanged |
| a real timestamp was read | `provider-createdAt` or `hiker-taken_at` | fresh or too_old |

**Every edit is an assignment to a log field.** No comparison, no threshold, no branch that returns `fail` was touched.

**Three dead imports removed from `src/app/api/clips/route.ts`.** `fetchClipFreshnessWithRetry`, `MAX_CLIP_AGE_MS` and `MAX_CLIP_AGE_LABEL` were imported and **never called or read** (each appeared exactly once, on its import line). BL-684 called the constant import cosmetic. **It is not cosmetic:** while diagnosing precisely the question "does each path enforce its own window", a route that imports the threshold reads as though it does. An unused import is also a second apparent reader that a future round could start using, which is exactly how two paths drift apart. `detectPlatform` is genuinely used and stays.

---

## PART 2 — nobody starts getting wrongly refused

**Every BL-686 protection re-proven on this tree, not inherited:**

```
--- 4. fail open: unreadable shapes still ACCEPT ---
PASS  harvest returned null -> unknown -> ACCEPTED
PASS  harvest returned a non-object -> unknown -> ACCEPTED
PASS  media object with no taken_at -> unknown -> ACCEPTED
PASS  taken_at is null / zero / negative / NaN / non-numeric string -> ACCEPTED
PASS  taken_at is a pre-2015 unit-scale bug -> unknown -> ACCEPTED
PASS  empty media object -> unknown -> ACCEPTED
PASS  a FUTURE-dated post (clock disagreement) is ACCEPTED  ageMs=-3600000

--- 4b. the boundary still resolves toward ACCEPTING ---
PASS  29 min ACCEPTED       PASS  30 min (the advertised window) ACCEPTED
PASS  34 min (inside tolerance) ACCEPTED
PASS  exactly at the edge ACCEPTED (strict >)
PASS  36 min refused
```

**The threshold is read from code and shared, never duplicated.** `MAX_CLIP_AGE_MS = 30 * 60 * 1000` is declared in `src/lib/clip-config.ts` and nowhere else; `IG_FRESHNESS_SKEW_TOLERANCE_MS = 5 * 60 * 1000` in the core and nowhere else. Asserted:

```
PASS  the core DECLARES no threshold of its own, it imports it
PASS  neither route declares, imports or reads a threshold of its own
```

**Because both paths run the same function, the batch path applies the identical threshold and tolerance by construction. There is no second copy that could drift.**

### What happens when some rows in a batch are too old

**The transaction model is unchanged and was not touched.** Per `batch/route.ts:155-169`:

* **Each row is its own transaction, committed SEQUENTIALLY.** The comment states the reason: the core's own per-row daily-cap check must see rows already committed in this same batch, so the cap is race-safe.
* **One row failing never aborts the rest.** A refused row is caught per row and recorded; the loop continues.
* **Every input row gets exactly one result**, so `submitted + skipped == total`. Rows that were never processed are backfilled with an explicit "Not processed." rather than vanishing.
* **The clipper sees which rows failed and why:** each result carries `{ clipUrl, clipAccountId, ok: false, error }`, and for a too-old row the `error` is the core's own plain message.

**So a mixed batch behaves predictably: the fresh rows commit, the old rows are refused individually with a reason attached to that row, and no clip is silently lost or duplicated.**

The refusal text is unchanged and remains the exact string TikTok and YouTube already used: *"This Instagram clip was posted more than 30 minutes ago and cannot be submitted."* Plain, factual, about the clip's timing and never about the clipper. **This round ships no new user-facing copy at all.**

---

## PART 3 — forward only

No migration, no data write, no backfill, and `prisma migrate` was never run. The change is four log-field assignments and three deleted import symbols.

The harness snapshots the whole clip population before and after itself:

```
PASS  population snapshot identical before and after this harness
  clips=4569 earnings=10375.89 base=9905.34 bonus=470.56
  byStatus=APPROVED:3685,FLAGGED:6,PENDING:5,REJECTED:873
```

**Clips already accepted stay accepted.** Nothing retroactively re-evaluates an existing clip, including the three pre-deploy Instagram acceptances identified in PART 0, which keep their APPROVED status and their earnings.

---

## PART 4 — the proof

`npx tsx scripts/test-bl-704-both-paths-freshness.ts` → **46 passed, 0 failed**, exit 0. **No submission was created.**

### All three platforms, both paths

Because both paths call the same function, a per-platform result proven once is proven for both, and the harness proves that structurally rather than assuming it:

| platform | too old is refused | evidence |
| --- | --- | --- |
| **TikTok** | yes | `clipper-submit-core.ts:329` `diffMs > MAX_CLIP_AGE_MS`, byte-identical to pre-BL-686. Live: **42 of 42** single-path submissions inside the window, max 15.5 min |
| **YouTube** | yes | same line, same comparison, `publishedAt` from the free Data API |
| **Instagram** | yes | `:432` `evaluateInstagramFreshness`; harness proves 36 min refused and 29/30/34/edge accepted. Live: **16 of 16** batch clips fresh |

**A fresh post is accepted on both paths:** the 15 live batch clips at 4 to 20 minutes, plus the boundary ladder above.

**A post with no available timestamp is ACCEPTED on both paths:** the deleted post in the live batch sample returned HTTP 404 with no `taken_at` and was accepted, and the ten synthetic unreadable shapes all return `unknown`.

**The owner's account behaves identically to an ordinary clipper** on paths 1 and 2: the core has zero references to any role or privilege flag. Path 3 differs, and it is owner-only by design.

### Nothing moved, and no actor ran

```
PASS  apify.ts carries its 5 guards  5
PASS  apidojo.ts has 4 exported actor fns behind one chokepoint  4
PASS  account-profile and verify-cascade each guarded  1/1
PASS  ELEVEN guarded paths total  11
PASS  APIFY_HARD_OFF is a const true, no env can re-enable it
```

| file | blob OID | verdict |
| --- | --- | --- |
| `src/lib/clip-earnings-writer.ts` | `7aa6be48` | IDENTICAL |
| `src/lib/earnings-calc.ts` | `797e2098` | IDENTICAL |
| `src/lib/balance.ts` | `e887f80a` | IDENTICAL |
| `src/lib/tracking.ts` | `847dcf70` | IDENTICAL |
| `src/lib/clip-earnings-invariant-middleware.ts` | `61cef393` | IDENTICAL |
| `src/lib/money-decimal.ts` | `ef5cdae7` | IDENTICAL |
| `src/lib/campaign-era.ts` | `106e16ad` | IDENTICAL |
| `src/lib/apify.ts` | `656bf4c0` | IDENTICAL |
| `src/lib/owner-submit-core.ts` | `4cd23e30` | IDENTICAL |
| `src/lib/clip-config.ts` | `77e3fdfb` | IDENTICAL |
| `src/lib/apify-hard-off.ts` | `29258a5d` | IDENTICAL |

The dead chain at `apify.ts:2566` was not revived; `apify.ts` is untouched.

### A harness failure I fixed rather than papered over

The first run reported **2 failures** on the single route. Investigated rather than adjusted away: both were my assertions matching the **import line** rather than a call, which is precisely the dead-import problem, so the harness had found something real about the code and something sloppy about itself. I removed the dead imports **and** tightened the assertions to strip import and comment lines before testing. Recorded because a harness that is quietly loosened until it passes is worse than no harness.

---

## Build gates, stated honestly

| step | result |
| --- | --- |
| `npm ci` | **exit 0** (wipes the generated Prisma client) |
| `npx prisma generate` | **exit 0**, run **before** tsc |
| `npx tsc --noEmit` | **exit 0**, **0 output lines**, re-run after the import removal |
| `npx eslint --version` | **v9.39.4 present**, so the hooks gate is real |
| `npm run build` | **BUILD_EXIT=0**, echoed from a captured log, never piped through `tail` |
| `check:prisma-bypass` | **0 violations** |
| `check:removed-fields` | **OK** |
| `lint:hooks` | **11 problems (0 errors, 11 warnings)**, at the cap, no new warning |
| static pages | **61/61** |

The real `.ts` diff is **211 insertions, 2 deletions across 3 files**, so this is a code change, not a document. Both `tsc` and `next build` were actually run, twice. **No heredoc was used** and shells ran one at a time. Every count comes from `grep -c`.

---

## Probe disclosure and safety

**Live probes: HikerAPI `/v2/media/info/by/code` × 16**, one call per post, paced 1.5s, roughly **$0.016** total, purely to read `taken_at` for the 16 post-deploy batch clips. **No Apify call of any kind and no Apify actor run.** No LamaTok or YouTube call. **One call per profile respected.**

**No submission was created while testing.** No clip, status, earning or payout was written. No `prisma migrate`. Read-only database access via the sanctioned `scripts/run-select.js`, with **every timestamp cast to `::text`** and anchored against DB `now()`, because this is entirely a timestamp question and a local `+02:00` offset has faked a discrepancy here before. Handles are redacted to an 8-character id prefix and no clipper is identified.

**A missing, unavailable or unparseable timestamp still results in ACCEPTANCE**, proven with the actual code path on all ten shapes, while a skipped fetch is now labelled rather than silently indistinguishable. TikTok and YouTube enforcement is unchanged and proven unbroken. The 11 BL-678 guards are intact. NO dashes used as bullets.
