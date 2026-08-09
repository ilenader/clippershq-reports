# BL-753 — the YouTube fabricated zero is closed at source, and the never-decrease guard is proven UNSAFE

**VERDICT IN ONE LINE: `youtube.ts` no longer turns a hidden view count into a zero on either path that
writes views, and it needed NO caller change, so all six money files plus `campaign-era.ts` and `apify.ts`
are byte-identical by blob OID. A platform-wide never-decrease guard on stored views was measured and
REJECTED: 1,245 legitimate decreases across 650 clips on all three platforms would have been blocked, the
largest a 723,110 view correction.**

**2026-08-09 · Base:** `main @ d169e73b` · **Branch:** `checkpoint/BL-753`
**No data changed. No clip's stored views moved down. No clipper's earnings changed. The 13 affected clips
were NOT repaired, per BL-751. No Apify actor run. No probe of any kind, $0.00 spent. Handles redacted;
every timestamp cast `::text` against DB `now()`.**

**THERE IS NO `YOUTUBE_API_KEY` IN THIS ENVIRONMENT** (`grep -c` over `.env.local` returns 0, as BL-751 also
found). **No live YouTube call was made and none is claimed.** Every behavioural claim below is proven by a
harness that drives the real, unmodified functions with a stubbed `fetch`, run against BOTH the pre-fix and
post-fix code so the difference is measured rather than asserted.

---

## GATE RESULTS, STATED HONESTLY

| gate | result |
|---|---|
| `npm run build` | **`BUILD_EXIT=0`**, "Compiled successfully in 40s" |
| BL-348 hooks gate | **0 errors, 11 warnings** against `--max-warnings 11`. eslint **v9.39.4** confirmed present, so the gate did not silently no-op |
| `npx tsc --noEmit` | **exit 2, and it is exit 2 on clean `origin/main` too** |
| Harness, post-fix | **36 passed, 0 failed**, `HARNESS_EXIT=0` |
| Harness, pre-fix | **23 passed, 13 failed**, `PRE_EXIT=1` |
| Earnings invariant | **0 violations** |

**The `tsc` result needs saying plainly rather than buried.** `scripts/test-bl-534-era-boundary-owner-rule.ts`
raises two `TS2393 Duplicate function implementation` errors. I verified this is **pre-existing** by removing
my harness from the worktree entirely and re-running: `TRUE_BASELINE_EXIT=2`, the same two errors, on
untouched `origin/main`. **My change adds zero `tsc` errors.** It is not mine to fix and I did not touch it.

One error in that count **was** mine and is fixed: my harness declared bare top-level `check`/`main`, and
`scripts/` is type-checked as a single program, so it collided with that same file. Adding `export {}` gave
it module scope. `next build` had passed before that fix, which is exactly why `tsc` was run separately.

---

# PART 1 — THE FABRICATION, FIXED AT SOURCE

## 1.1 The defect

`youtube.ts:178`, pre-fix:

```ts
views: parseInt(stats.viewCount ?? "0", 10) || 0,
```

It fabricates twice over: `?? "0"` covers the absent key, and `|| 0` converts the resulting `NaN`. YouTube
omits `statistics.viewCount` as **documented product behaviour** when the uploader hides the view count, an
ordinary creator setting on a healthy public video. BL-751 traced the consequence: a `slim` object carrying
`views: 0` is a **truthy object**, so `apify.ts:2203` accepts it as a real stat and `tracking.ts:1782` writes
it unconditionally, permanently overwriting a real count.

The same file gets the other case right forty lines below, which is what makes this a bug and not a policy:
an absent video maps to `out.set(clipId, null)`.

## 1.2 The fix, and the one decision that made it free

BL-751's spec proposed widening `slim.views` to `number | null` and teaching `apify.ts:2201-2210` to skip it.
**I did not do that, and the reason is the most important engineering choice in this round.**

`apify.ts:2200-2210` already reads a falsy entry as a miss:

```ts
const s = ytMap.get(c.clipId);
if (s) { result.set(c.clipId, s); ytHits++; }
else   { result.set(c.clipId, null); ytMisses++; }
```

So mapping the **whole entry** to `null`, exactly as the deleted-video branch already does, reuses a contract
that is already correct. **Three consequences, all of them good:**

1. **`apify.ts` needs no change and stays byte-identical.** BL-751's shape would have required editing it.
2. **`tracking.ts` needs no change and stays byte-identical.** Widening `views` to `number | null` would have
   pushed a `null` toward `ClipStat.views`, a non-nullable `Int`, and thrown inside the tick.
3. **The return type already permitted it.** `fetchYouTubeStatsBatch` is declared
   `Promise<Map<string, {...} | null>>`, so `out.set(clipId, null)` type-checks with no signature change.

The executable change at `:178`:

```diff
+        const rawViews = stats.viewCount;
+        const parsedViews = rawViews == null ? NaN : parseInt(String(rawViews), 10);
+        if (!Number.isFinite(parsedViews)) {
+          console.log(`[YOUTUBE-BATCH] videoId=${vid} statistics.viewCount absent (hidden count) — UNKNOWN, not 0`);
+          for (const clipId of byVideoId.get(vid) ?? []) {
+            out.set(clipId, null);
+          }
+          seen.add(vid);
+          continue;
+        }
+
         const slim = {
-          views: parseInt(stats.viewCount ?? "0", 10) || 0,
+          views: parsedViews,
           likes: parseInt(stats.likeCount ?? "0", 10) || 0,
```

**Every line justified:**

* `rawViews == null ? NaN : parseInt(String(rawViews), 10)` — `== null` catches both `undefined` (key absent)
  and an explicit `null`. `String()` guards a non-string arriving from JSON. No `?? "0"`, so an absent key can
  no longer become the string `"0"`.
* `!Number.isFinite(parsedViews)` — the single test for UNKNOWN. It catches an absent key, an explicit null,
  and a non-numeric string. It does **not** catch a real `0`, which is the entire point.
* `out.set(clipId, null)` inside the loop over `byVideoId.get(vid)` — mirrors the deleted-video branch
  exactly, including the many-clips-per-video case where two clips share a video id.
* `seen.add(vid)` before `continue` — the video **did** come back in the response, so it must be marked seen.
  Omitting it would fall through to the missing-video loop, which sets the same `null`, so the outcome would
  be identical either way; it is set for correctness of meaning, not to change behaviour.
* `continue` — skips slim construction. Nothing downstream is reached.
* `likes`/`comments` deliberately keep `|| 0`. They are not views, they never reach an earnings calculation,
  and widening them would change the contract for no safety gain.

## 1.3 The second path, also fixed

`getYouTubeVideoStats` at `:35` had the same fabrication. Its **only** caller is `apify.ts:2449-2453`, which
already treats a null return as a failed fetch (`if (!ytStats) return { stats: null, provider: "youtube-api" }`)
and writes nothing. So returning **whole-object null** closes it with no caller change, again leaving
`apify.ts` byte-identical.

## 1.4 The third path, DELIBERATELY NOT FIXED, and why

`getYouTubeVideoDetails` at `:86` still fabricates. **This is a decision, not an oversight**, and it is
recorded in a comment in the file so the next reader does not have to rediscover it.

It cannot take the same medicine. Returning whole-object null would make
`marketplace/submissions/[id]/post/route.ts:114` reject a perfectly good submission with *"Could not verify
this YouTube clip. Make sure YOUTUBE_API_KEY is configured"*, a misleading error for a healthy public video
whose creator merely hid the count. The correct fix widens the return to `views: number | null` and teaches
`apify.ts:2539` to skip it, and **that is an `apify.ts` edit, which this round's safety constraints forbid.**

**RESIDUAL, stated plainly:** a hidden-count YouTube video submitted through the freshness path still records
a fabricated 0 as its **first** stat. That is far less damaging, because there is no prior real count to
destroy, but the clip will then sit at 0, since every later tick now correctly returns null and preserves the
last-known value. **It deserves its own round with its own proof.**

## 1.5 Every caller mapped, with file:line, the BL-748 way

| # | function | caller | reads `.views` | with `null` after | breaks |
|---|---|---|---|---|---|
| 1 | `fetchYouTubeStatsBatch` | **`apify.ts:2194-2210`** (the tracking tick) | yes | `if (s)` false → `result.set(clipId, null)` → **MISS**, clip keeps last-known | **NO** |
| 2 | `fetchYouTubeStatsBatch` | `tracking.ts:3868` | **NO**, comment only | n/a | **NO** |
| 3 | `fetchYouTubeStatsBatch` | `apify-ledger.ts:646` | **NO**, comment only | n/a | **NO** |
| 4 | `getYouTubeVideoStats` | **`apify.ts:2449-2465`** (per-clip fetch) | yes | `if (!ytStats)` → `{stats:null}` → nothing written | **NO** |
| 5 | `getYouTubeVideoDetails` | `apify.ts:2522-2541` (freshness) | yes | unchanged this round | **NO** |
| 6 | `getYouTubeVideoDetails` | `marketplace/.../post/route.ts:113` | **NO**, reads `publishedAt` only | unchanged this round | **NO** |

Callers 2, 3 and 6 were checked by reading them, not assumed. **Not one caller relies on receiving a 0.**

## 1.6 Unknown and genuinely-zero stay distinguishable

This is the property BL-543 and BL-748 require, and the harness asserts it directly:

```
hidden count  ->  entry null  ->  clip keeps its last-known views
genuine zero  ->  views 0     ->  a real 0 is recorded
```

**Pre-fix these two were byte-identical objects.** The harness caught it:
`hidden={"views":0,...}` and `genuineZero={"views":0,...}`. That is what "indistinguishable" means in
practice, and it is now fixed.

---

# PART 2 — THE PLATFORM-WIDE GUARD IS UNSAFE, MEASURED NOT ASSUMED

## 2.1 The question

BL-751 found no never-decrease protection on stored views anywhere, and recommended a `viewsNeverDecrease`
floor. **The brief asked me to judge that honestly rather than implement it reflexively. The answer is no.**

## 2.2 Views legitimately decrease, constantly, on every platform

Every consecutive `clip_stats` pair, all non-deleted clips, `db_now = 2026-08-09 19:06:10.837939+00`:

| platform | kind | events | clips | biggest drop | avg drop | earliest | latest |
|---|---|---|---|---|---|---|---|
| instagram | **partial decrease** | 86 | 18 | **723,110** | 49.23% | 2026-05-30 07:02:37.048 | 2026-08-08 14:10:59.547 |
| tiktok | **partial decrease** | 269 | 136 | 12,876 | 41.85% | 2026-05-15 16:30:21.104 | 2026-07-31 00:10:34.827 |
| youtube | **partial decrease** | 890 | 496 | 2,372 | 8.90% | 2026-04-24 02:01:15.755 | 2026-08-05 21:10:35.308 |
| tiktok | fell to ZERO | 5 | 5 | 1,398 | 100% | 2026-05-30 21:02:18.727 | 2026-07-27 06:02:35.809 |
| youtube | fell to ZERO | 46 | 45 | 117 | 100% | 2026-05-23 11:01:21.296 | 2026-07-31 03:01:59.508 |

**1,245 legitimate decrease events across 650 distinct clips.** A never-decrease floor would have blocked
every one of them, including a 723,110 view Instagram correction three weeks ago.

BL-751's 45 YouTube and 5 TikTok zero-falls are **independently confirmed exactly** (46 YouTube events on 45
clips, one clip falling twice).

## 2.3 Why blocking them would be worse than the defect

Platforms purge bot and spam views routinely; a real 10,000 view video genuinely becoming 9,400 is ordinary.
Freezing the inflated figure would mean **permanently paying CPM on views that no longer exist**, since
earnings are `views / 1000 × cpm`. That directly contradicts BL-627's no-overpayment property. **A guard that
protects clippers from a provider bug by overpaying them out of the campaign budget is not a safety
improvement, it is a different defect.**

## 2.4 How a correction IS distinguished from a fabrication

**By the destination, not the direction.** The two populations do not overlap:

* **Corrections** land above zero. Average drop 8.90% to 49.23%, 1,245 events.
* **Fabrications** land on exactly 0 from a positive value. 100% drop, 51 events, and a real video does not
  go from 1,239 views to 0. YouTube never resets a count to zero.

That is precisely the rule `hikerapi.ts:878` already encodes for Instagram (`views <= 0` → reject → Apify
confirms), and it is why the identical classifier bug was harmless there and live here.

## 2.5 What I implemented instead, and why nothing touches `tracking.ts`

**The narrower per-provider fix, which is PART 1.** The brief's own instruction was to do exactly this if a
platform-wide guard would suppress legitimate corrections, and it would.

I also did **not** add the narrow drop-to-zero floor at `tracking.ts:1782`, and this is a deliberate call:
with the fabrication closed at source, **no path can deliver a fabricated zero to that write any more.**
Instagram is gated at `hikerapi.ts:878`, YouTube is now closed in `youtube.ts`, and TikTok's `apidojo.ts`
uses `??` chains with no `|| 0` terminator so an absent field yields `undefined` rather than 0. Adding a
guard to the file that writes every clipper's earnings, to catch a case that can no longer reach it, is risk
without benefit. **The result is that `tracking.ts` is byte-identical, which is the strongest safety outcome
available here.**

**Recommended for a future round, not done here:** a drop-to-zero floor at the `ClipStat` write is still
worth having as defence in depth against a *future* provider, and it is now cheap to specify precisely,
because PART 2.4 gives the exact predicate: reject a write of `views = 0` when the clip's last stored value
was greater than 0. It belongs in a money-file round with its own proof.

---

# PART 3 — THE 13 ARE NOT REPAIRED, AND THEY DO NOT SELF-HEAL

**Not repaired, per BL-751's recommendation.** Live count re-confirmed today: **13** YouTube clips whose
latest stored views is 0 while their maximum ever was above 0. Money: **$0.00**, because every affected
campaign carries `minViews = 1000` and every one of these clips peaked at 1 or 2 views.

**They do NOT self-heal from this fix, and saying so matters more than the fix itself.** The mechanics:

* **Before:** hidden count → fabricated 0 written every tick → stays 0.
* **After:** hidden count → null → entry skipped → **clip keeps its last-known value, which is now 0**.

The fabricated zero has already **become** the last-known value, so preserving it preserves the wrong number.
**This fix is purely forward-looking: it stops the next clip being zeroed, it cannot un-zero these.**

They recover only if the creator un-hides the count, at which point a real value is written and the clip
heals on its own. **The 5 confirmed deleted (404) will never heal**, and per BL-543 their honest value is null
with the last-known kept, not a resurrected count.

**Repair spec, NOT run**, should the owner want it despite the $0.00: for each of the 8 non-deleted clips,
take `max(views)` from `clip_stats`, write one new `ClipStat` at that value, write **no** earnings, and let
the next tick recompute. Skip the 5 deleted. I recommend against it, as BL-751 did: a money round with
snapshots and printed rollback cannot be justified to move $0.00.

---

# PART 4 — PROOF

## 4.1 The harness, run against BOTH refs

No YouTube key exists, so `global.fetch` is stubbed with synthetic YouTube Data API v3 payloads and the
**real, unmodified** exported functions are driven through it. The stub asserts the URL is Google's
`videos.list` and never touches the network. `scripts/bl753-harness.ts`, committed.

**PRE-FIX (`git show origin/main:src/lib/youtube.ts`): 23 passed, 13 FAILED, `PRE_EXIT=1`**

```
FAIL  vidHIDDEN UNKNOWN -> FABRICATED {"views":0,"likes":4,"comments":1,"shares":0}
FAIL  vidHIDDEN apify.ts:2203 contract -> HIT views=0
FAIL  hidden !== genuine-zero -> hidden={"views":0,...} genuineZero={"views":0,...}
```

**POST-FIX: 36 passed, 0 failed, `HARNESS_EXIT=0`**

```
PASS  vidHIDDEN UNKNOWN -> null entry (clip keeps last-known)
PASS  vidHIDDEN apify.ts:2203 contract -> MISS (result.set(clipId, null), nothing written)
PASS  hidden !== genuine-zero -> hidden=null genuineZero={"views":0,"likes":0,"comments":0,"shares":0}
PASS  mB known count -> views=0 (expected 0)          <- genuine zero still records a real 0
PASS  mC known count -> views=987 (expected 987)
PASS  deleted video still null (unchanged path) -> null
PASS  hidden count -> whole-object null -> null        <- getYouTubeVideoStats
PASS  genuine zero -> real 0 -> {"views":0,...}
```

Every case also **replays `apify.ts:2200-2210`'s exact `if (s)` expression** over the result, so the caller
contract is proven rather than assumed, and asserts that **no null can reach `ClipStat.views`**.

Cases covered: hidden count, genuine zero, normal count, deleted video, `statistics` object missing entirely,
non-numeric garbage, explicit `null`, and a **mixed chunk** carrying all three kinds in one response.

## 4.2 Money files, by blob OID on both refs

```
IDENTICAL  ac5be7deb061  src/lib/clip-earnings-writer.ts
IDENTICAL  797e20985ad5  src/lib/earnings-calc.ts
IDENTICAL  e887f80acfc7  src/lib/balance.ts
IDENTICAL  83ce4babfd39  src/lib/tracking.ts
IDENTICAL  61cef3939536  src/lib/clip-earnings-invariant-middleware.ts
IDENTICAL  ef5cdae757b9  src/lib/money-decimal.ts
IDENTICAL  106e16ad7512  src/lib/campaign-era.ts
IDENTICAL  656bf4c0c408  src/lib/apify.ts
```

**8 of 8 identical.** `tracking.ts` does not appear in the diff. The only changed source file is
`src/lib/youtube.ts`, which is not a money file, plus the new harness.

## 4.3 Data untouched

| metric | value | `db_now` |
|---|---|---|
| earnings invariant violations | **0** | 2026-08-09 19:20:55.033763+00 |
| `clip_stats` rows | 206,119 | same |
| newest `ClipStat.checkedAt` | 2026-08-09 19:11:00.126 | same |
| YouTube clips stored at 0 with a positive max | **13** (BL-751's figure, unchanged) | same |
| live YouTube clips at risk | **539** | same |
| earnings on them | **$146.16** | same |

**No stored views moved down in this round**, because this round performed **no write of any kind**. Every DB
access went through `scripts/run-select.js`, which refuses any write keyword. The newest `ClipStat` at
19:11:00 is the ordinary hourly tick, running normally and independently of this work.

## 4.4 Tick budget at `CLIPS_PER_TICK` 90

`clipsPerTick()` (`tracking.ts:164-178`) clamps to `[5, 500]` with a default of 30, so 90 is accepted
verbatim. **The change cannot affect the tick's budget**, for three reasons that are structural rather than
measured:

1. **No additional API call.** The batch is still one `videos.list` call per 50 ids. A hidden-count video
   changes what is done with a response already received.
2. **No new code path in the tick.** A hidden-count video now takes the identical route a deleted video has
   always taken. 45 YouTube clips exercise that route already.
3. **No Apify actor.** `tracking.ts:3865-3869` documents that YT batch hits Google, not Apify, and only
   TikTok and Instagram consume `MAX_APIFY_CALLS_PER_RUN`. A YT miss consumes no Apify slot.

The added work is one `Number.isFinite` per item. Harness chunks reported `took=0ms`.

**Stated honestly: I did not execute a live 90-clip tick.** Doing so would write `ClipStat` rows and
recompute earnings, which this round forbids. The claim above is a structural argument plus the harness, not
a wall-clock measurement, and I am not dressing it up as one.

## 4.5 Guards and actors

* **No Apify actor run.** `apify.ts` is byte-identical by blob OID, so its 8 `BL-678` guard comments are
  intact by construction (27 `BL-678` references across `src/`).
* **No probe of any kind. $0.00 spent.** No YouTube key exists, and no oEmbed call was needed because BL-751
  already established reachability for these 13.
* **No `prisma migrate`.** `npx prisma generate` only, after `npm ci` wiped the client.

---

# WHAT COULD NOT BE VERIFIED

* **Live YouTube behaviour.** No `YOUTUBE_API_KEY` exists in this environment, so I could not confirm against
  the real API that a hidden-count video returns `statistics` without `viewCount`. That is documented Google
  behaviour and it is the only mechanism in the code producing this exact signature, but I did not observe it
  and do not claim to have.
* **A wall-clock tick at `CLIPS_PER_TICK` 90**, for the reason in 4.4.
* **Whether the 13 were caused by the hidden-count case specifically.** BL-751 could not attribute them
  either. It is the only mechanism in the code with this signature, but that is inference from a single
  available cause, not a captured payload.
* **The 5 TikTok zero-falls.** A different provider chain, all recovered, all $0.00, and **not attributed**,
  on the same discipline BL-748 and BL-751 applied.

---

# ACCESSIBILITY

**No UI code was touched.** The diff is one scraper provider (`src/lib/youtube.ts`) and one node harness
script. There is no component, template, route handler rendering markup, or user-facing string in this
round, so there is no accessibility surface to review.

---

# ROLLBACK

`git revert -m 1 <merge>`, or `git reset --hard pre-BL-753`. **No data rollback exists or is needed, because
no data was written.**
