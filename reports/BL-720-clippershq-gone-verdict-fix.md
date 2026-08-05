# BL-720 — a clip may only be marked gone when NO HUMAN can see it

**SHIPPED 2026-08-05.** Branch `checkpoint/BL-720` (`2bb26b1`), merged to `main` at **`de0169bd`**, verified on origin. Tags `pre-BL-720` / `pre-merge-BL-720` / `post-merge-BL-720`. Base main `78614080`. Isolated worktrees `C:/b720` and `C:/m720` (short paths, `node_modules` never junctioned). `C:/b575` was found holding `main`, stale with 77 dirty entries, and was **left exactly as found**.

**DB `now()` at the census: 2026-08-05 15:31:37.564137+00. At final verification: 2026-08-05 15:57:49.526483+00.** Every timestamp is cast `::text` against that clock.

**Probes disclosed: 129 HikerAPI calls, $0.129.** 113 profile calls for the census (declared cap 120) plus 16 targeted evidence calls. **No Apify actor ran**; the eleven BL-678 guards are untouched. One call per profile, cached per account per run. Clipper handles are redacted to a three-character prefix; the reports repo is PUBLIC.

---

## ONE LINE

**The retirement gate read one integer that the provider itself documents as ambiguous. It now reads a bundle, `retire` is reachable from exactly two named paths out of 672 tested combinations, and a census of all 113 accounts holding retired clips found BL-717's blind spot was real: one account is private, holding three clips worth $0.00.**

---

# PART 0 — what each provider response actually means

### The single line that decided everything

`src/lib/retire-dead-clips.ts:111`, before this round:

```ts
if (httpStatus === 404) {   // ← the entire gone verdict
```

`res.httpStatus` came from `fetchHikerInstagramByUrl` (`:104-105`) and **nothing else was read**: not the response body, not the account, not a second observation on a later day. HikerAPI's own module header says what that integer means, at `src/lib/scraper-providers/hikerapi.ts:8-9` and again at `:782-783`:

> `/v2/` returns 200 for found posts and 404 for **inaccessible/deleted**

**"Inaccessible" and "deleted" are two different facts about the world, and the platform recorded them as the same integer.**

### Every response that contributes to a gone verdict

| Response | file:line | What it genuinely means | Human can still see it? | Read as GONE before? | Should it? |
|---|---|---|---|---|---|
| HikerAPI 404, body `MediaNotFound` | `retire-dead-clips.ts:111` | that specific media id is not served | **depends on the account** | yes | **only with corroboration** |
| HikerAPI 404, other/absent body | `retire-dead-clips.ts:111` | some other refusal | probably | **yes** | **no — DEFECT** |
| **Private account** | same 404 | account is private, nothing deleted | **YES, every follower** | **yes** | **no — DEFECT** |
| **Region-locked post** | same 404 from our fixed-region egress | blocked for our egress only | **YES, in-region** | **yes** | **no — DEFECT** |
| **Age-gated post** | same 404 | needs a logged-in adult session | **YES, any adult** | **yes** | **no — DEFECT** |
| **Temporarily restricted (takedown under appeal)** | same 404 | restriction in force, may lapse | **YES, the poster, and all once it lapses** | **yes** | **no — DEFECT** |
| Account deleted or banned by Instagram | 404 media, **404 profile** | the whole account is gone | **no** | yes | **yes** |
| HikerAPI 500 / 502 / 503 | `:136` fell to ambiguous | provider outage | yes | no | no. BL-559 and BL-604 both established this |
| LamaTok slideshow `by/url` 500 (BL-712) | `lamatok.ts:261`, verdict `carousel` | slideshow endpoint quirk | yes | no | no |
| 429 rate limit | `:136` | our pacing | yes | no | no |
| 401 auth / 402 balance | `:136` | our credential | yes | no | no |
| Timeout / network | `httpStatus = -1` at `:107` | our network | yes | no | no |
| Empty or malformed body | stored as `{_nonJsonText}` at `hikerapi.ts:378-382` | unparseable | unknown | it depended on the status | no |
| HTTP 200 | `:132` | alive | yes | no | no |
| TikTok, any response | excluded at `:74` | not in scope | n/a | never | n/a |

**Five defect rows.** The fetch-failure rows were already correct and stay correct; the fix is narrow and lands entirely on the 404 family.

### Can any provider distinguish DELETED from MERELY INACCESSIBLE?

**On the media endpoint alone: NO, and HikerAPI says so itself.** There is no field on `/v2/media/info/by/code` or `by/url` that separates them. Both return the identical body, verbatim, which BL-717 measured and this round re-confirmed on eight further clips:

```json
{"detail":"Not found ({})","exc_type":"MediaNotFound"}
```

**But the platform is not limited to that endpoint, and that is the whole fix.** Three discriminators exist and none was being used:

1. **The body.** BL-559 established for TikTok that a genuine gone verdict requires **404 AND `MediaNotFound`**, and `gone-counter.ts:26-31` records that rule. **Instagram was never held to it**: `is404()` at `hikerapi.ts:270-272` regexes the derived error *string*, and `retire-dead-clips.ts:105` read the bare status. The discriminator was already in `HikerResult.rawBody` (`hikerapi.ts:97-100`, populated on every exit path at `:378-392`), free, unread.
2. **The account.** `GET /v2/user/by/username` returns **`is_private`** and distinguishes `not_found` from `transient` **by design** (`hikerapi.ts:274-349`). `clip_accounts.username` is stored for every clip. **`retire-dead-clips.ts` did not import it.**
3. **Time.** Retirement rested on a single observation at a single instant, so every transient condition that presented as a 404 for ninety seconds was indistinguishable from permanent deletion.

**What still cannot be distinguished, stated plainly:** a region lock, an age gate and a temporary restriction on a post whose account is public and healthy all look identical to a deletion on both endpoints. There is no field for it. That residue is what the persistence requirement in PART 1 exists to cover, and it is covered by *time* rather than by a signal, because no signal exists.

---

# PART 1 — the fix

### There is no longer a default-retire branch

The verdict is now a **pure exported function**, `decideGoneVerdict` in `src/lib/retire-dead-clips.ts`, and `action: "retire"` is returned from **exactly two places**, both named. Everything else keeps the clip. Extracting it was deliberate: a 500, a 429, a timeout and a malformed body cannot be summoned from HikerAPI on demand, and "we believe those fail open" is exactly the class of claim this codebase has been burned by before (BL-528 found the never-decrease guard existed only in an uncommitted script).

### What now suffices, and what no longer does

**NO LONGER SUFFICIENT.** A bare 404. Also insufficient, each proven in the harness: a 404 whose body is not `MediaNotFound`; a 404 with a different `exc_type`; an empty body; a malformed non-JSON body; any 5xx; 429; 401; 402; a timeout; a null status; an account probe that is transient or key-less; an account identity mismatch; and an `is_private` that is **absent** rather than explicitly `false`.

**PATH A — retires with no wait.**
> media 404 **AND** body `MediaNotFound` **AND** the account itself returns **`not_found`**.

The whole account is gone from Instagram. No human can reach any post on it, **including its own owner**. This is the strongest evidence available and needs no repetition.

**PATH B — must STAND.**
> media 404 **AND** body `MediaNotFound` **AND** the account **resolves**, **id-matches**, and is **explicitly `is_private: false`** **AND** the identical bundle was already true on a **separate earlier run at least 36h ago**.

The account is healthy and this specific post is the thing missing. That is consistent with deletion **and** with a temporary restriction, so it must persist.

### The corroboration is a different endpoint, not a repetition

`fetchHikerInstagramByUrl` already tries `by/code` and falls through to `by/url` on a 404 (`hikerapi.ts:249-267`), so a 404 reaching the gate has been seen on **two distinct media endpoints**. The account probe is a **third** endpoint answering a different question. That is corroboration in the sense the brief demands: a different endpoint and a distinct response shape, not more of the same signal.

### The private-account case, explicitly

**This is the case the round exists for.** A clipper whose account goes private has **deleted nothing**. Every follower can see the post right now and it returns to everyone the instant the account goes public again.

Under the new logic a private account **keeps the clip** and **clears any standing gone evidence**, so the persistence clock restarts from scratch if the post ever legitimately goes gone later. That mirrors the reset rule `gone-counter.ts:38-41` already states for its own counter: *"a temporarily-private account that comes back loses its gone history entirely and is never condemned."*

**It never accrues a gone strike, and it is never retired, no matter how long it stays private.** Proven: `PRIVATE account is KEPT even with 40h of standing gone evidence`.

### BL-550: id-match, never row-match

The account verdict decides whether a clipper's money disappears, so trusting a profile HikerAPI did not answer with would retire a private account's clips on a stranger's public flag. `hikerapi.ts` now surfaces **`resolvedUsername`** (the username the provider actually answered with, additive, no behaviour change for the verify route) and the gate refuses to judge on any mismatch or missing username. Case and a leading `@` are normalised so a real match is never a false mismatch.

### Why this is NOT "raise K", stated separately as the brief requires

**K (`minGone`) is UNCHANGED at 3.** It was not touched.

K counts repetitions of **one ambiguous signal**, a bare 404, and more repetitions of an ambiguous signal are still ambiguous. It also decides almost nothing: BL-717 measured **76% of every retirement the platform has ever made** happening on a clip whose `consecutiveGone` was **zero**, because those clips enter through the `checkIntervalMin >= 1440` branch at `:77`, and BL-588 proved the counter structurally under-fires for Instagram.

The 36h interval is a different thing. It counts repetitions of a bundle that has **already passed the body discriminator and the account corroboration**, and its only job is to outlast the **one** failure mode those two cannot see: a **temporary** restriction. A deletion is permanent and survives the wait; a temporary restriction is by definition not. The daily cron runs at 06:00 UTC, so 36h guarantees **two separate runs** (a same-day re-run cannot satisfy it) without stretching to a third day if a run slips.

It uses a **new nullable column** rather than `consecutiveGone` precisely so it cannot change the meaning of a counter BL-576 owns or double-count against the candidate selection that reads it.

---

# PART 2 — a clip that cannot be judged

| Requirement | How it is met |
|---|---|
| Keeps tracking | The gate only ever writes `videoUnavailable`. An unjudged clip is untouched, so it stays in the cron poll (`tracking.ts:3554-3556` filters on `videoUnavailable: false`) |
| Earnings stay visible and withdrawable | Nothing is written. `earnings/route.ts:206` and `payouts/route.ts:424` both key off `videoUnavailable`, which stays `false` |
| NULL never 0 (BL-543) | The retirement path **writes no `ClipStat` at all**, in any branch. It cannot write `views = 0` because it never writes views |
| No gone strike | `consecutiveGone` is not touched by this file, before or after this round. A fetch failure also does not stamp `goneEvidenceFirstAt`, proven: `a 500 does NOT stamp gone evidence` |
| Standing evidence on an outage | **Left exactly as it was.** An outage is not evidence of life any more than of death, so the clock neither starts nor resets |

### The backoff, and its cost

There is no new polling loop. An unjudgeable clip simply remains a candidate and is re-probed on the **next daily run**, which is the existing cadence. The backoff is therefore the daily cron itself, and the only new cost is that a clip destined for retirement stays a candidate for roughly one extra run.

**Incremental cost, about $0.020 a day:**

| Component | Calls/day | $/day |
|---|---|---|
| Account profile calls (~5 distinct accounts among candidates, cached per account per run) | ~5 | $0.005 |
| Second media probe per genuinely-gone clip, because the 36h wait keeps it a candidate one extra run (a gone clip costs 2 calls: `by/code` then `by/url`) | ~15 | $0.015 |
| **Total** | **~20** | **~$0.020/day, ~$0.62/month** |

**BL-717 priced the verdict fix at about $0.008 a day** (one extra call per retirement, 7.67/day). This round is **about 2.6 times that**, and the entire difference is the persistence wait, which BL-717's estimate did not include. Both figures are small; the honest one is $0.020.

### An operational guard, not a `maxDuration` raise

The run now makes **two paced call types**, and the route's `maxDuration` is 300s (`api/cron/retire-dead-clips/route.ts:5`). BL-717 warned explicitly: *"Do not simply raise `maxDuration`."* Instead `RUN_BUDGET_MS = 240_000` stops the run **cleanly** and reports how many candidates it deferred. Candidates are re-selected from scratch every run, so nothing is lost by stopping early and no cursor is needed. Being killed mid-flight by the platform, by contrast, would lose the run's log line entirely.

---

# PART 3 — the clips already wrongly retired

## A census, not a sample

BL-717 probed 15 retired **media** urls, got 15 x (404 + `MediaNotFound`), and said plainly what that could not prove:

> *"Every one of these 15 clips could be sitting behind a private account, visible to every follower right now, and this probe would look exactly as it does."*

The discriminator is the **account** endpoint, and the entire retired population sits on only **113 distinct accounts**. So **one call per profile answered the question for all 852 retired clips at once**, at $0.113, and this is a **census with 113 of 113 answered**, not an extrapolation.

| Bucket | Accounts | Retired clips | APPROVED clips | Frozen | Would retire under the new logic? |
|---|---|---|---|---|---|
| `RESOLVED_PUBLIC` | 68 | 468 | 312 | **$2,792.66** | yes, via path B |
| `ACCOUNT_NOT_FOUND` | 44 | 381 | 318 | **$790.84** | yes, via path A |
| **`RESOLVED_PRIVATE`** | **1** | **3** | **3** | **$0.00** | **NO** |
| transient / unusable | 0 | 0 | 0 | $0.00 | n/a |
| identity mismatch | 0 | 0 | 0 | $0.00 | n/a |
| **Total** | **113** | **852** | **633** | **$3,583.50** | |

### The answer

**Exactly THREE approved clips, on ONE account, carrying $0.00, would not be retired under the new logic.**

**BL-717's blind spot was real** — a private account genuinely does exist inside the retired population, and a media-only probe could never have found it. **And the money standing on it is zero.**

### The money, and the honest residual

**Frozen and hidden from clippers' balances on clips that should never have been retired: $0.00 provable.**

**The residual, stated without softening.** The account probe closes the **private** case definitively and permanently. It does **not** close region-lock, age-gate or temporary-restriction for clips **already retired**, because those present as *a healthy public account plus a 404 post* — which is exactly what all **468** public-account retired clips look like. Nothing distinguishes them retroactively. Going forward the 36h persistence covers them, because a temporary restriction lapses and a deletion does not; backwards, it cannot be applied, because the observations were never made.

So the honest bound is: **$0.00 proven wrongly retired, with up to $2,792.66 across 312 approved clips sitting in a state that cannot be distinguished from correct retirement using any signal the providers offer today.** BL-717 bounded its 15-of-15 sample at 18.1% at 95% confidence; this census removes the sampling uncertainty on the private case entirely and replaces it with a **named, structural** limit on the other three.

### Not bulk-revived, deliberately

**No clip was revived.** Three clips at $0.00 does not justify a money-visible mass change, and the wider $3,583.50 question is BL-717's revival schedule, which is its own round and its own decision. The costed spec is BL-717 PART 3 and stands unmodified: tiers of daily / 3-day / 7-day out to a 365-day stop, **80.7 calls = $0.081 per clip lifetime**, launch peak $0.85/day falling to ~$22/month steady state, revival being the three-column write at `tracking.ts:1739-1742` and **never** a credit, a backfill or a catch-up amount.

**One change this round makes to that spec:** a revival pass should now use the **account** endpoint first. 44 of 113 accounts are gone outright, so 381 of the 852 clips can be excluded from any revival schedule immediately for **44 calls**, cutting the programme's population by 45% before it starts.

---

# PART 4 — what still works

### Genuinely deleted posts are still retired, proven on real data

**44 of 113 accounts (39%) return `not_found`**, covering **381 retired clips and $790.84**. Every one retires immediately via path A. Id-matched evidence on a real clip:

```
=== clip cmq0n22fv004g0pp3ybs08r5g ===
  stored: status=APPROVED earnings=$110.85 videoUnavailable=true goneEvidenceFirstAt=null
  MEDIA  httpStatus=404 via=by_url exc_type="MediaNotFound" views=null definitiveBody=true
  ACCOUNT status=not_found httpStatus=404 isPrivate=null idMatch=true (asked=mem*** answered=nul***)
  VERDICT: RETIRE (path A) — the whole account is gone from Instagram, no human can see it. Same as OLD logic.
```

BL-584 retired 710 dead clips for a real reason and that reason is untouched: the Apify-era cost problem returns only if dead clips keep polling, and they still will not.

### The cron still runs and still works

Schedule unchanged: `railway-cron-scheduler.ts:92`, daily at 06:00 UTC, `retire-dead-clips`. Candidate selection unchanged (`minGone >= 3` OR `checkIntervalMin >= 1440`, cap 100/run). Auth unchanged (`CRON_SECRET` bearer). The only addition is the 240s wall budget, which reports rather than truncates silently.

### No live clip is retired

```
=== clip cms65ullm001w0pnmsdm5xist ===
  stored: status=APPROVED earnings=$5.25 videoUnavailable=false goneEvidenceFirstAt=null
  MEDIA  httpStatus=200 via=by_code exc_type=null views=10301 definitiveBody=false
  VERDICT: ALIVE — not retired, gone evidence cleared. (OLD logic also kept it.)
```

Structurally: `no combination retires without a 404` passed across every status in the matrix.

### The daily retirement rate, before and after

| | Rate |
|---|---|
| Before (BL-717, 18 days since the 2026-07-18 sweep) | **7.67 clips/day** |
| After, steady state | **~7.67 clips/day, materially unchanged** |
| After, **the first run post-deploy** | **path A only.** Every path-B candidate is a first sighting and is stamped, not retired |

The rate is unchanged because the census shows the incoming population is overwhelmingly genuinely gone. What changes is that each retirement now carries account corroboration and, on path B, a 36h wait. **The first run will look alarmingly quiet and that is correct, not a fault.**

---

# PART 5 — the evidence

### A private account's clip is KEPT where the old logic retired it

```
=== clip cmqsc7w64000x0pmsj6s7f2fw ===
  stored: status=APPROVED earnings=$0 videoUnavailable=true goneEvidenceFirstAt=null
  MEDIA  httpStatus=404 via=by_url exc_type="MediaNotFound" views=null definitiveBody=true
  ACCOUNT status=resolved httpStatus=200 isPrivate=true idMatch=true (asked=cli*** answered=cli***)
  VERDICT: KEPT — ACCOUNT IS PRIVATE, a human can still see this post. *** OLD LOGIC WOULD HAVE RETIRED THIS ***
```

### Two high-value retired clips are now PENDING, not retired on sight

```
=== clip cmpohxfpn000b0po8ygvrqofg ===   earnings=$324.00
  ACCOUNT status=resolved isPrivate=false idMatch=true (asked=det*** answered=det***)
  VERDICT: PENDING (path B) — full bundle seen for the FIRST time; stamped, NOT retired for at least 36h.
           OLD logic would have retired it TODAY.

=== clip cmp2hc6gb001u0prq0i7yvnz8 ===   earnings=$266.98
  ACCOUNT status=resolved isPrivate=false idMatch=true (asked=ish*** answered=ish***)
  VERDICT: PENDING (path B) — ... OLD logic would have retired it TODAY.
```

### Every branch no provider will produce on demand

`npx tsx scripts/bl720-prove-gone-verdict.ts` → **34 passed, 0 failed**, offline, against the real exported function, re-run on the merge commit.

```
PASS  500 server error FAILS OPEN, no gone strike  -> keep/ambiguous
PASS  502 FAILS OPEN, no gone strike               PASS  503 FAILS OPEN, no gone strike
PASS  429 rate limit FAILS OPEN, no gone strike    PASS  401 auth FAILS OPEN, no gone strike
PASS  402 balance FAILS OPEN, no gone strike       PASS  timeout / network (-1) FAILS OPEN
PASS  null (no call made) FAILS OPEN, no gone strike
PASS  a 500 does NOT stamp gone evidence
PASS  BL-712 slideshow by/url 500 does not read as gone
PASS  200 is ALIVE and clears gone history
PASS  404 WITHOUT MediaNotFound is KEPT (the old code retired this)
PASS  404 with a DIFFERENT exc_type is KEPT        PASS  404 with an empty body is KEPT
PASS  404 with a malformed non-JSON body is KEPT
PASS  PRIVATE account is KEPT even with 404 + MediaNotFound
PASS  PRIVATE account is KEPT even with 40h of standing gone evidence
PASS  account probe TRANSIENT fails open           PASS  no account at all fails open
PASS  is_private absent (null) fails open — unknown is never read as public
PASS  account identity MISMATCH fails open         PASS  account answering no username fails open
PASS  case and @ differences still MATCH (not a false mismatch)
PASS  ACCOUNT NOT FOUND retires immediately (path A)
PASS  path A does not need standing evidence
PASS  public account, first sighting -> PENDING and stamps
PASS  public account, evidence only 10h old -> still PENDING
PASS  public account, evidence 40h old -> RETIRE (path B)
PASS  36h is the boundary and it is not satisfied at 35h
PASS  a corrupt goneEvidenceFirstAt re-stamps rather than retiring
PASS  across every combination, retire comes only from the two named paths
        4 retires of 672 combinations, paths=A_account_gone,B_persisted
PASS  no combination retires without a 404
PASS  no combination retires without MediaNotFound in the body
PASS  no combination retires a PRIVATE account
```

### Nothing moved

| Claim | Evidence at 2026-08-05 15:57:49 |
|---|---|
| No clip retired by this round | `videoUnavailableSince` within 3h: **0**. Retired total **852**, unchanged all round |
| No clip revived | frozen total **$3,583.50**, unchanged; 633 APPROVED retired, unchanged |
| The probes wrote nothing | `goneEvidenceFirstAt` non-null: **0 of 4,891 clips** |
| No clipper's earnings or balance changed | APPROVED earnings $11,179.56; the +$3.91 since BL-719 is the ordinary tracking cron on ACTIVE campaigns over ~2h, and this round executed no earnings write on any path |
| Earnings invariant | **0 violations** across all non-deleted clips |
| No clip's status changed | the gate writes only `videoUnavailable` / `videoUnavailableSince` / `goneEvidenceFirstAt`, and wrote none of them |
| No payout created, modified, approved or cancelled | 153 rows; the newest (`2026-08-05 14:49:19.814`) is a clipper's own request from before this round's DB work and **this round executed zero payout writes** |
| No stored views moved down **by this round** | 403 `ClipStat` rows written in 3h, **6** below a prior max. **None is on any clip this round probed** (`cmqm36vdo`, `cmse03c8g`, `cmqk9o37q`, `cmqqfq4q1`, `cmq6gzawb`, `cmqlpzlo1`), all written by the ordinary tracking cron, which is **byte-identical** this round. This round writes no `ClipStat` on any path |

---

## Safety and gates, stated honestly

* **Diff: 3 source-affecting files.** `src/lib/retire-dead-clips.ts`, `src/lib/scraper-providers/hikerapi.ts` (surfaces `resolvedUsername`, additive), `prisma/schema.prisma`. Plus four read-only scripts and one migration SQL.
* **BYTE-IDENTICAL by blob OID on both refs:** all 6 money files (`clip-earnings-writer` `ac5be7de`, `earnings-calc` `797e2098`, `balance` `e887f80a`, **`tracking` `83ce4bab`**, `middleware` `61cef393`, `money-decimal` `ef5cdae7`), plus `campaign-era` `106e16ad`, `gone-counter` `1d4d8244` and `apify` `656bf4c0`. **No money file changed and `tracking.ts` is not in the diff.**
* **Schema:** one **additive, nullable** column, no default, applied with `ALTER TABLE ... ADD COLUMN IF NOT EXISTS` via `run-schema-sql.js` and `npx prisma generate` only. **NEVER `prisma migrate`.** Verified `is_nullable = YES`, `column_default = null`, **0 of 4,891 rows backfilled**.
* **No Apify actor ran.** The eleven BL-678 guards are untouched; the verdict harness makes no network call at all.
* **Probes:** 129 HikerAPI calls, **$0.129**, every one disclosed. Census cap 120, used 113. Sixteen targeted evidence calls. One call per profile, cached per account. Every clip and account **id-matched** per BL-550; **0 identity mismatches** observed.
* **Accessibility:** no UI file is in the diff. No component, no JSX, no CSS, no markup, no copy string. Nothing to review.
* **Gates, honest.** `npm ci` exit 0, then `npx prisma generate` exit 0 **before** typecheck. `npx tsc --noEmit` **exit 0, 0 lines of output**. `npm run build` **BUILD_EXIT=0** read from a captured log with `echo $?`, **never piped through `tail`** — this mattered again: a backgrounded build's exit file was read before it existed and reported "still running" rather than a false green, and the build was re-run to capture the code honestly. `lint:hooks` **11 problems (0 errors, 11 warnings)** at the <=11 cap with **eslint v9.39.4 confirmed executing**. Counts by `grep -c`, never `head`. Post-merge build from a clean `npm ci`: **BUILD_EXIT=0**, harness **34/34**.
* **NO dashes** as bullets. Handles redacted to a three-character prefix; no wallet address anywhere.

## Rollback

```bash
git revert -m 1 de0169bd
# the column is additive and nullable, so nothing needs dropping. If wanted,
# AFTER reverting the code:
#   ALTER TABLE clips DROP COLUMN IF EXISTS "goneEvidenceFirstAt";
```

Reverting restores `if (httpStatus === 404)` exactly, including its defect.

## What is still open

1. **The revival schedule** (BL-717 PART 3) is still unbuilt, and retired clips are still never re-checked: `tracking.ts:3554-3556` excludes them from the poll, so the auto-restore at `:1726` is unreachable for exactly the clips that need it. **Use the account endpoint first**: 44 of 113 accounts are gone, cutting the population 45% for 44 calls.
2. **The 468 public-account retired clips ($2,792.66)** cannot be distinguished from correct retirements retroactively. Only a revival pass that re-probes them over time can answer it, and only forwards.
3. **`tracking.ts:3131`'s regex path** remains a loaded gun aimed at the money path: it matches the literal word `private` against an exception string and **zeroes earnings** via `writeClipEarningsZero`. BL-717 proved it is currently unreachable behind BL-678 GUARD 2 and has not fired in 82 days. It should be deleted or narrowed on its own round; **this round did not touch it**, and it is the one remaining place where "private" still means "take the money".
4. **The retirement cron is not watched by the watchdog** (`railway-cron-scheduler.ts:88-91`), so a missed 06:00 run raises no alarm. BL-717 noted 2026-08-04 recorded zero retirements and that this is not distinguishable from a missed run.
