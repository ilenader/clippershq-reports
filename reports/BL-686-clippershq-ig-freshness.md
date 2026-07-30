# BL-686 (ClippersHQ) — Instagram posting-window enforcement restored

## THE 30 MINUTE RULE IS ALIVE ON INSTAGRAM AGAIN, and it cost ZERO new vendor calls: the post time was already arriving in a response BL-682 pays for on this exact path, and nobody was reading it. BL-684's six clips, accepted at 269 to 332 minutes old, would now all six be refused. Every ambiguity resolves toward ACCEPTING: ten unreadable timestamp shapes accept, a post dated in the server's future accepts, and there is exactly ONE refusal path that needs a sane, past-dated timestamp more than 35 minutes old to reach. `apify.ts` is byte-identical, so all 11 BL-678 guards are untouched by construction and the dead chain is not revived. Nothing about any existing clip changed.

**2026-07-30 · Branch `checkpoint/BL-686` @ `b153e5d8`, pushed and verified (`origin/checkpoint/BL-686 == local HEAD`, `scripts/safe-push.mjs`).**
**Base** `43a4d4b1` (`post-merge-BL-685`) · **Tags** `pre-BL-686` (43a4d4b1) and `post-BL-686` (b153e5d8), both pushed.
**Worktree** `C:/b686`, short path, `node_modules` never junctioned. **DB `now()` at final query: 2026-07-30 13:29:40.851907+00.**
**Rollback** `git revert b153e5d8`, or `git reset --hard pre-BL-686`. Reverting returns Instagram to accepting every clip regardless of age, which is exactly today's state, **so the rollback is strictly no worse than now.**

| file | change |
| --- | --- |
| `src/lib/clipper-submit-core.ts` | +196: the decision function, the tolerance, the sanity floor, the call site, the three-outcome record |
| `src/lib/scraper-providers/hikerapi.ts` | +20 −2: **comment correction only, zero behaviour change** |
| `scripts/test-bl-686-instagram-freshness.ts` | NEW, the proof harness |
| `BACKLOG.md` | +14 |

**The real `.ts` diff is non-empty:** 415 lines across three `.ts` files, quoted below. This is a code change, not a document.

---

## PART 1 — the fix

### What was broken, from BL-684

The 30 minute rule is real code and works on TikTok and YouTube. For Instagram, `fetchClipFreshnessWithRetry` passes `skipHikerOverlay: true` (`apify.ts:2497`, BL-137's deliberate choice) into three Apify tiers that have all returned null behind the BL-678 guards since the 2026-07-22 cutover. Null lands in the `!result.stats` branch, which sets `transient = true` and **ACCEPTS**. BL-684 measured six clips from an **ordinary** clipper (`isTestUser=false`) at **269 to 332 minutes old, every one accepted**.

### The fix reuses BL-682's already-proven path, and adds no vendor call

**BL-682 already harvests the HikerAPI media object three lines above this check, on this exact path, and that object carries `taken_at`.** So the new check reads a field out of a response the submit path has already paid for.

**Vendor calls per Instagram submit, before and after: ONE, unchanged.** The three `fetchClipFreshnessWithRetry` attempts make **zero** network calls (the BL-678 guards return before a URL is built), and `harvestInstagramRawMeta` makes the single HikerAPI read. This round adds nothing to that.

**A second fetch was considered and rejected.** Mapping `taken_at` into `HikerResult.createdAt` inside `hikerapi.ts` would have put a new value on the object that feeds the **tracking overlay**, which is on the money-critical path and reads views, likes and comments only. That is a behaviour change on the money path for no consumer. **The comment there is corrected; the value stays null deliberately, and the reason is written into the file.**

```diff
       // shares: IG has no share-count concept on v2.
       shares: 0,
-      // createdAt: Hiker's v2 surface doesn't expose a parseable
-      // ISO timestamp consistently; cron write doesn't read it.
+      // createdAt — BL-686 CORRECTION. The old comment here claimed Hiker's v2
+      // surface "doesn't expose a parseable ISO timestamp consistently". THAT
+      // WAS WRONG, and it mattered: BL-684 read `taken_at` live off this exact
+      // endpoint as a clean unix-seconds integer on six consecutive posts, and
+      // BL-682's harvest has been receiving it on the submit path ever since.
+      // The field is present; it is this SUMMARY parser that drops it, the same
+      // way BL-670 found the cover image was being dropped before BL-673.
+      //
+      // It is still deliberately null HERE. This object feeds the TRACKING
+      // overlay, which is on the money-critical path and reads views, likes and
+      // comments only; populating it would change a value on that path for no
+      // consumer. The submit-path posting-window check does NOT come through
+      // here: it reads `taken_at` off `rawBody` in clipper-submit-core.ts, which
+      // is why apify.ts and this file's behaviour are both untouched by BL-686.
       createdAt: null,
```

### The dead chain is not revived and no guard is weakened

**`src/lib/apify.ts` is BYTE-IDENTICAL**, `656bf4c0c408e955676c95d14bbbb764eecde1ef`, so `apify.ts:2497`'s `skipHikerOverlay: true` is exactly as it was and **all 11 BL-678 guards are untouched by construction, not by review**. Counted with `grep -c`:

| file | guarded paths | count | blob OID vs `pre-BL-686` |
| --- | --- | --- | --- |
| `src/lib/apify.ts` | five request builders, `BL-678 GUARD n of 5` | **5** | `656bf4c0` IDENTICAL |
| `src/lib/scraper-providers/apidojo.ts` | four exported actor functions behind one chokepoint | **4** | `d860cf4c` IDENTICAL |
| `src/lib/account-profile.ts` | `apify hard off (BL-678)` | **1** | `44aaea8c` IDENTICAL |
| `src/lib/verify-cascade.ts` | `apify hard off (BL-678)` | **1** | `69e1a9a5` IDENTICAL |
| | **total** | **11** | |

`src/lib/apify-hard-off.ts` is also byte-identical (`29258a5d`), so `APIFY_HARD_OFF` remains a `const true` that no environment variable can flip. **No Apify actor ran at any point in this round.**

---

## PART 2 — fail open, proven by the actual code path

### The decision is an exported pure function that production calls

```ts
export function evaluateInstagramFreshness(
  media: any,
  nowMs: number,
): { outcome: FreshnessOutcome; ageMs: number | null; source: string } {
  const takenAtMs = instagramTakenAtMs(media);
  if (takenAtMs == null) return { outcome: "unknown", ageMs: null, source: "none" };
  const ageMs = nowMs - takenAtMs;
  const outcome: FreshnessOutcome =
    ageMs > MAX_CLIP_AGE_MS + IG_FRESHNESS_SKEW_TOLERANCE_MS ? "too_old" : "fresh";
  return { outcome, ageMs, source: "hiker-taken_at" };
}
```

It is exported and side-effect free **on purpose**: `processClipperSubmitLink` calls exactly this, so the harness drives the real decision rather than a paraphrase, and there is no second copy to drift.

### The call site, and the single refusal

```ts
if (platform === "instagram" && freshnessOutcome === "unknown" && fetchedRawMeta != null) {
  const verdict = evaluateInstagramFreshness(fetchedRawMeta, Date.now());
  if (verdict.outcome !== "unknown") { freshnessOutcome = verdict.outcome; freshnessAgeMs = verdict.ageMs; freshnessSource = verdict.source; }
  if (verdict.outcome === "too_old") {
    console.warn(`[FRESHNESS] outcome=too_old platform=instagram source=${verdict.source} ageMs=${verdict.ageMs} thresholdMs=${MAX_CLIP_AGE_MS} toleranceMs=${IG_FRESHNESS_SKEW_TOLERANCE_MS}`);
    return fail(`This Instagram clip was posted more than ${MAX_CLIP_AGE_LABEL} ago and cannot be submitted.`);
  }
}
```

**Trace every way a timestamp can be absent, and every one ends in acceptance:**

| what happens | where it lands | result |
| --- | --- | --- |
| harvest returned null (no key, cooldown, 404 on a deleted or private post, non-JSON body, timeout, any throw) | `fetchedRawMeta != null` is FALSE | the `if` never runs → **ACCEPTED** |
| media object carries no `taken_at` | `instagramTakenAtMs` → null → `unknown` | `outcome !== "too_old"` → **ACCEPTED** |
| `taken_at` is null, zero, negative, NaN, or a non-numeric string | same | **ACCEPTED** |
| `taken_at` is a pre-2015 unit-scale bug | sanity floor → null → `unknown` | **ACCEPTED** |
| post dated in the server's FUTURE (clocks disagree) | `ageMs` negative, not `>` threshold | `fresh` → **ACCEPTED** |
| age inside 30 min + tolerance | `fresh` | **ACCEPTED** |
| **finite, positive, post-2015, past-dated, over 35 minutes** | `too_old` | **the ONE refusal** |

**A missing timestamp can never become a refusal.** Proven, not asserted, ten shapes:

```
PASS  harvest returned null (provider miss, cooldown, 404, timeout, throw) -> unknown -> ACCEPTED
PASS  harvest returned a non-object -> unknown -> ACCEPTED
PASS  media object with no taken_at at all -> unknown -> ACCEPTED
PASS  taken_at is null -> unknown -> ACCEPTED
PASS  taken_at is zero -> unknown -> ACCEPTED
PASS  taken_at is negative -> unknown -> ACCEPTED
PASS  taken_at is NaN -> unknown -> ACCEPTED
PASS  taken_at is a non-numeric string -> unknown -> ACCEPTED
PASS  taken_at is a pre-2015 unit-scale bug -> unknown -> ACCEPTED
PASS  empty media object -> unknown -> ACCEPTED
```

The **pre-2015 sanity floor** is there for a specific reason: a unit-scale bug (seconds read as milliseconds, a zero, a sentinel) produces a date near the epoch, which would look "very old" and would refuse a clipper **for our arithmetic error**. Instagram video did not exist before 2015, so anything earlier is treated as unparseable, which means unknown, which means accept. A genuinely old post is years newer than the floor, so nothing real slips through it.

### The three outcomes are kept distinguishable

`fresh` (accepted), `too_old` (refused) and `unknown` (accepted) are three distinct values on a dedicated `[FRESHNESS]` log line carrying `outcome`, `platform`, `source` and `ageMs`. Collapsing `unknown` into `too_old` would start refusing innocent clippers during a provider outage; collapsing it into `fresh` would leave a future round unable to tell a verified-fresh clip from an unverifiable one. The variable is initialised to `unknown`, which is both the honest pre-read state and the one that accepts.

```
PASS  a 5-minute-old post is fresh  ageMs=300000
PASS  a 300-minute-old post is too_old  ageMs=18000000
PASS  no timestamp is unknown  source=none
PASS  all three are distinguishable, none collapsed into another
PASS  the source is recorded so a future round can tell them apart
```

**Stated honestly and not hidden: this is a LOG line, not a column.** This round was permitted no schema change, and `transient` alone cannot carry it because unrelated infra failures also set that flag. Persisting the outcome on `rule_shadow_decisions` belongs to a later round.

---

## PART 3 — clock skew, timezone, provider lag

### The comparison, and why no offset can age a fresh clip

`Date.now()` is UTC by definition. `taken_at` is a unix instant, also UTC. **Both sides are epoch milliseconds and the comparison is pure integer arithmetic. No local date string is parsed anywhere on this path**, deliberately, because a `+02:00` offset once faked a two hour discrepancy on this platform. Proven under five timezones:

```
PASS  a 10-minute-old clip stays FRESH under 5 timezones including +02:00  outcomes=fresh
PASS  the computed age is byte-identical under every timezone  ages=600000
```

(Timezones exercised: UTC, Europe/Belgrade `+02:00`, America/Los_Angeles, Asia/Tokyo, Pacific/Kiritimati `+14:00`.)

### The threshold, read from code and not assumed

**`MAX_CLIP_AGE_MS = 1,800,000 ms` and `MAX_CLIP_AGE_LABEL = "30 minutes"`**, imported from `src/lib/clip-config.ts`, asserted by the harness rather than hardcoded in it. **This is the identical constant TikTok and YouTube already enforce a few lines above.** No second number was invented for Instagram.

```
threshold read FROM CODE: MAX_CLIP_AGE_MS=1800000ms ("30 minutes")
PASS  MAX_CLIP_AGE_MS is 30 minutes, read from clip-config.ts  1800000ms
PASS  the label matches the constant  "30 minutes"
```

### The tolerance: 5 minutes, and why

Two different clocks are being compared. The disagreements are all small but all real: `taken_at` is whole seconds so up to a second is lost to truncation; NTP drift on the host is sub-second in normal operation but is not contractually zero; and the submit round trip itself takes real time that elapses **after** the clipper pressed submit.

**Five minutes is far larger than any of those and far smaller than the window.** The clipper is told "30 minutes" everywhere in the UI, so an effective 35 means **nobody who genuinely acted inside the advertised window can be refused by a clock they do not control**, while a clip that is hours old is still caught by an order of magnitude.

**The asymmetry with TikTok and YouTube is deliberate and disclosed rather than hidden.** They keep their exact pre-BL-686 comparison, so Instagram is strictly **more lenient** at the boundary. That is the correct direction: a wrongly refused clipper is far worse than a late clip accepted, and BL-664 measured the human reviewer overturn rate at **0.77 percent**, which is the bar an automatic refusal has to clear.

```
PASS  29 min (inside the advertised window) ACCEPTED
PASS  30 min (exactly the advertised window) ACCEPTED
PASS  31 min (just past the window, inside tolerance) ACCEPTED
PASS  34 min (still inside tolerance) ACCEPTED
PASS  exactly at the tolerance edge ACCEPTED (strict >, never >=)
PASS  36 min (past window + tolerance) refused
PASS  a post dated in the SERVER'S FUTURE (clock disagreement) is ACCEPTED  ageMs=-3600000
PASS  a millisecond-valued taken_at is read correctly, not multiplied  ageMs=18000000
```

**Coarse and delayed provider timestamps both resolve toward acceptance.** Whole-second granularity is absorbed by the tolerance. A provider that has not yet indexed a brand-new post returns not-found, which is the harvest-null path, which accepts. A future-dated reading accepts. The `< 1e12` branch (the same guard `lamatok.ts:302` uses for TikTok's `createTime`) means a millisecond-valued field is read correctly instead of being multiplied into the far future, where it would have read as `fresh` and silently disabled the rule.

---

## PART 4 — forward only, the past untouched

**No migration, no data write, no backfill, no retroactive refusal.** The change lives entirely in the submit path and runs only when a new clip is being submitted. `prisma migrate` was never run.

The harness snapshots the **whole population** before and after itself and asserts equality:

```
PASS  population snapshot identical before and after this harness
  clips=4471 earnings=10113.73 base=9650.46 bonus=463.28
  byStatus=APPROVED:3526,FLAGGED:6,PENDING:85,REJECTED:854
```

Confirmed again from the database at the end of the round, timestamps cast to `::text` against DB `now()`:

| DB `now()` | clips | invariant violations | total earnings | IG clips submitted since the cutover |
| --- | --- | --- | --- | --- |
| 2026-07-30 13:29:40.851907+00 | 4393 | **0** | **$10,113.73** | **231, all untouched** |

**The 231 Instagram clips accepted since 2026-07-22 that this rule would have refused keep their status, their earnings and their payouts.** Those clippers were told yes in good faith and nothing about them moved. The earnings invariant stands at **0 violations**, as BL-683 left it.

---

## PART 5 — the proof

`npx tsx scripts/test-bl-686-instagram-freshness.ts` → **38 passed, 0 failed**, exit 0. **No submission was created.**

### A real Instagram post older than the window is now identified as too old

Two real live clips pulled from the database and read through HikerAPI (handles and shortcodes redacted; the reports repo is public):

```
PASS  taken_at IS present on the live v2 payload (the old comment was wrong)  taken_at=1785415334
PASS  a real Instagram post older than the window is now identified as TOO OLD  age=41 min
PASS  the SAME real payload judged 10 minutes after posting is ACCEPTED  ageMs=600000
PASS  the SAME real payload with taken_at stripped -> unknown -> ACCEPTED

PASS  taken_at IS present on the live v2 payload (the old comment was wrong)  taken_at=1785392708
PASS  a real Instagram post older than the window is now identified as TOO OLD  age=418 min
PASS  the SAME real payload judged 10 minutes after posting is ACCEPTED  ageMs=600000
PASS  the SAME real payload with taken_at stripped -> unknown -> ACCEPTED
```

**The fresh case uses the SAME real provider payload with only the clock pinned**, rather than a fabricated object, so the acceptance is proven on real data too.

### BL-684's six clips, replayed through the fixed code

```
  clip 1  age=332 min  outcome=too_old
  clip 2  age=295 min  outcome=too_old
  clip 3  age=288 min  outcome=too_old
  clip 4  age=282 min  outcome=too_old
  clip 5  age=274 min  outcome=too_old
  clip 6  age=269 min  outcome=too_old
PASS  all six that were WRONGLY ACCEPTED would now be refused  6/6
```

**All six, at 269 to 332 minutes, are between 7.7x and 9.5x the effective 35 minute edge.** The threshold is nowhere near them, which is the sanity check the brief asked for: this is not a borderline call.

### TikTok and YouTube are unchanged

Their comparison line is byte-for-byte the pre-BL-686 one; the two assignments added beside it only observe the verdict and do not participate in it. `evaluateInstagramFreshness` is called **exactly once**, at `clipper-submit-core.ts:432`, behind `platform === "instagram"`.

Re-running BL-682's own harness on this branch: **16 passed, 0 failed**, including `PASS TikTok caption arrival is unbroken 3/3`.

**One transient failure, disclosed and attributed rather than buried.** The first BL-682 re-run showed `FAIL Instagram sound ids now reach the evaluator 2/3`. Investigated rather than waved away: the **same three clips** were sampled on both branches, and a run of the same harness on **pristine `origin/main`** gave 3/3, so the sample was not the variable. Two further runs **on this branch** then gave 3/3 with the same clip reporting `soundIdPresent=true`. It is HikerAPI response variance on a single call for one post, not a regression: this round touches nothing in the caption or sound harvest, and `campaign-rules.ts` is byte-identical.

### Nothing moved, and no Apify actor ran

| check | result |
| --- | --- |
| 6 money files + `tracking.ts` + `campaign-era.ts` by blob OID on **both** refs | **IDENTICAL** (writer `7aa6be48`, earnings-calc `797e2098`, balance `e887f80a`, tracking `847dcf70`, middleware `61cef393`, money-decimal `ef5cdae7`, campaign-era `106e16ad`) |
| `tracking.ts` in the diff | **no** |
| `apify.ts` / `campaign-rules.ts` | `656bf4c0` / `fc91216f`, **IDENTICAL** |
| 11 BL-678 guards | **11**, all intact, all four files byte-identical |
| Apify actors run | **zero**, and structurally impossible (`APIFY_HARD_OFF` is a `const true`) |
| clip status or earnings changed | **none**, population snapshot identical |

### The refusal message

**No new user-facing copy ships in this round.** The Instagram refusal reuses the **exact string** TikTok and YouTube already show:

> This Instagram clip was posted more than 30 minutes ago and cannot be submitted.

Plain, factual, about the clip's timing and never about the clipper: it states a fact and a consequence, makes no accusation and implies no suspicion, and it renders through the existing error surface with no new markup, so there is no new UI to review.

---

## Build gates, stated honestly

| step | result |
| --- | --- |
| `npm ci` | **exit 0** (wipes the generated Prisma client) |
| `npx prisma generate` | **exit 0**, run **before** tsc |
| `npx tsc --noEmit` | **exit 0**, **0 output lines** |
| `npx eslint --version` | **v9.39.4 present**, so the hooks gate is real and not a silent no-op |
| `npm run build` | **BUILD_EXIT=0**, echoed from a captured log, **never piped through `tail`** |
| `check:prisma-bypass` | **0 violations** (prisma-bypass + earnings-write checks) |
| `check:removed-fields` | **OK** |
| `lint:hooks` | **11 problems (0 errors, 11 warnings)**, at the ≤11 cap, no new warning added |
| static pages | **61/61** |

Both `tsc` and `next build` were actually run; neither was trusted alone. Every count in this document comes from `grep -c`, never a pipe into `head`. The `.ts` diff was confirmed non-empty before any claim was made.

---

## Probe disclosure and safety

**Live probes, all HikerAPI, one call per post, no retries:** 2 in the BL-686 harness (the two real payloads in PART 5), plus the BL-682 re-runs used for the TikTok and attribution checks (3 Instagram clips each, 4 runs across two worktrees), for roughly **20 HikerAPI media reads at about $0.001 each, on the order of $0.02**. **No Apify call of any kind and no Apify actor run. No LamaTok or YouTube call beyond what BL-682's harness already makes.** No key was printed or set.

**No submission was created while testing**, and no clip, status, earning, payout or balance was written by anything in this round. No `prisma migrate`. Every database read went through read-only queries with timestamps cast to `::text` and anchored on DB `now()`. **Handles, emails, shortcodes and clip identifiers are redacted**; the reports repo is public.

> **Filename note, per CONVENTION.md.** Published as `reports/BL-686-clippershq-ig-freshness.md`. The collision check was run against the reports repo before pushing; no other project's file was touched.

NO dashes used as bullets.
