# BL-914 — shares were never broken, and the row he saw was the only row that clip ever had

**2026-09-19 · DB `now()` = `2026-09-19 13:29:04.897229+00` (first read) to `13:31:43.354233+00` (last) · AUDIT IN EFFECT: measured, found nothing broken, changed no code.**

**Nothing was left behind and there is nothing unremovable.** No sandbox was created, because nothing needed proving beyond what production had already written. Worktree `C:/w914` removed and **verified absent by listing the path**; branch `checkpoint/BL-914` deleted at **0 commits beyond main** with a clean tree. Two probe scripts were written into `scripts/` in the shared tree and both were deleted by explicit path; `git status` shows **0** files of mine remaining. **No row of any kind was written to the database** — not a clip, not a campaign, not a payout, not a snapshot. **Zero vendor calls were made and the true cost of this round is $0.00.**

> **ONE LINE: shares ARE being read and written on Instagram and TikTok.** Instagram carries `sharesSource = "reshare_count"` on **68,116 of 126,257** snapshots in the last 30 days (57,136 of them a positive count), TikTok carries `sharesSource = "shareCount"` on **6,918 of 7,792** (2,298 positive), and YouTube is ABSENT on all **61,623** snapshots ever written, which is the truth because YouTube publishes no share count.
>
> **The owner's impression is mistaken about shares, and he was looking at something real.** The row he showed is a **submit snapshot**, written in the same millisecond as the post, where views, likes, comments and shares are all zero because nothing has been measured yet. It correctly records shares as ABSENT.
>
> **THE ACTUAL CAUSE IS NOT SHARES AND BL-912 FOUND IT INDEPENDENTLY WHILE THIS ROUND WAS MEASURING.** Every marketplace post had **only** its submit snapshot, because `createV2Post` wrote every tracking job `isActive: false` and nothing ever activated them. Six real posts sat live on Instagram for hours and were never polled a second time. The first marketplace tick in the platform's history ran today at **13:00:44 UTC** and recorded a share reading on **4 of 6** clips, with the other two genuinely omitted by the provider and correctly stored as ABSENT.

---

## THIS ROUND WAS BRIEFED TO RUN ALONE AND DID NOT

Stated first because it affected the measurement rather than merely the etiquette.

`BL-912` was live in its own worktree at `C:/b912` throughout, and **merged to main mid-round**: base was `933cbeec` when this round started and `c5f4c7c5` when it finished, carrying four BL-912 commits including one titled *"v2 clips were never polled a second time"*. Its migration file `scripts/migrations/BL-912-activate-v2-tracking-jobs.sql` was written into the shared tree at `13:31:10` local, two minutes before this round read it.

Nothing about that invalidates the figures here, because every figure is a read of committed state with its timestamp printed. It does mean **the platform changed underneath the measurement**: the six marketplace tracking jobs were inactive when the owner formed his impression and active when this round measured them. Both facts are reported, with their times, rather than smoothed into one.

BL-912's conclusion and this round's were reached separately and agree. That is a useful corroboration, and it is also exactly the duplicated effort a RUN ALONE brief exists to prevent.

---

## MODEL SPLIT, AND THE PART I TOOK BACK

**Every database query, every judgement about whether a value is genuinely absent or merely unread, and every line of this report: strongest model, reading raw output.**

**One Haiku subagent was dispatched** to enumerate every share write site in `src/`, told explicitly to open no database connection, make no network call and change no file. **It was still running when the round reached the question it was dispatched for, so I did the enumeration myself rather than wait or trust it**, and every finding in PART 3 was reached first hand. That was the right call on the verdict: a fourth loss point was the only thing that could have changed "nothing is broken" into "here is the fix".

**It returned after this report was drafted, it was checked, and it corrected me on one figure.** Both of its load-bearing claims are marked:

| subagent claim | status |
|---|---|
| `isMeasuredShare` has **12** call sites | **VERIFIED, and I was wrong.** My first draft said 22. 22 is the count of *mentions*: 8 imports, 1 definition, 1 comment and **12 actual calls**. I counted lines matching a name and called them call sites, which is the exact error a count of files being mistaken for a count of call sites has produced six times on this platform. Corrected throughout. |
| `apify.ts:651` writes a TikTok share count with **no** source | **VERIFIED as written, and it is dead.** See PART 3. |

Everything else in this report was read first hand, and the two corrections above are the only places a subagent changed a word of it.

**Connection cap: one at a time, mine, never concurrent, never held.** Every read went through `node scripts/run-select.js`, which opens one connection and closes it. **Subagents opened zero.** The pool was never stressed.

---

## PART 0 — VENDOR CALLS, AND THE PROBE THAT MEASURED NOTHING

**Disclosed before making it:** six HikerAPI calls at BL-838's measured $0.00069214 = $0.00415, against a ~$2 ceiling. **No Apify actor, and none can run.**

**The probe made zero HTTP calls and the true cost is $0.00.** All six returned `classification=unknown`, `httpStatus=n/a`, `views=null`. `HikerResult.httpStatus` is documented as null when no call was made, which is the missing-key short circuit. Confirmed directly:

```
hiker_configured   = false
lamatok_configured = false
env HIKER_API_KEY      = ABSENT      env LAMATOK_API_KEY = ABSENT
env HIKERAPI_KEY       = ABSENT      env LAMATOK_KEY     = ABSENT
env HIKER_KEY          = ABSENT
hiker_cooldown = {"active":false,...}     hiker_rolling = {"totalCalls":0,...}
```

**Neither vendor key exists in this environment. They live only in Railway. PART 2 as briefed cannot be run from this session, and I am not going to imply otherwise.**

**My own probe script reported `calls_made=6` and that was wrong.** It counted loop iterations, not HTTP calls, and printed a cost of $0.00415 that was never spent. It was caught by reading `http=n/a` in its own output rather than the summary line it printed underneath. A counter that counts the wrong thing is the same defect class as a proof that reads $0.00 while every route returns 200, and it is disclosed for that reason. Both probe scripts were deleted afterwards.

**What replaces the live probe is better than the live probe.** Production ran the real thing against these exact six clips at `13:00:44` today, through `tryHikerForInstagram`, the function the tick actually calls, and **the answer is stored in `ClipStat.sharesSource`**. `sharesSource` is precisely the record of what the provider returned. A synthetic probe would have been one more reading of the same field from outside the production path.

---

## PART 1 — WHAT IS ACTUALLY STORED

### Per platform, every snapshot written in the last 30 days

| platform | snapshots | shares > 0 | shares = 0 | `sharesSource` SET | `sharesSource` NULL | positive with NO source |
|---|---|---|---|---|---|---|
| **instagram** | 126,257 | **57,136** | 69,121 | **68,116** | 58,141 | **0** |
| **tiktok** | 7,792 | **2,298** | 5,494 | **6,918** | 874 | 295 (all pre-BL-820) |
| **youtube** | 222 | 0 | 222 | **0** | 222 | 0 |

Broken out by the label actually written:

| `sharesSource` | platform | snapshots | positive | measured zero | newest |
|---|---|---|---|---|---|
| `reshare_count` | instagram | 68,116 | 57,136 | 10,980 | 2026-09-19 13:01:05.404 |
| NULL = ABSENT | instagram | 58,141 | 0 | 58,141 | 2026-09-19 13:27:52.715 |
| `shareCount` | tiktok | 6,918 | 2,003 | 4,915 | 2026-09-19 12:01:24.412 |
| NULL = ABSENT | tiktok | 874 | 295 | 579 | **2026-08-23 21:21:34.147** |
| NULL = ABSENT | youtube | 222 | 0 | 222 | 2026-09-06 21:02:52.693 |

**Three things in that table are the answer.**

**BL-820's design is holding perfectly.** Not one Instagram snapshot with a NULL source carries a positive count, and not one with a source is unlabelled. The 295 TikTok rows that carry a positive count without a label are all **older than `2026-08-23 21:21:34`**, which is BL-820's own merge window. **Zero snapshots written since BL-820 carry a positive share count without a source.** The cutover was clean, and `isMeasuredShare`'s second clause still earns its place for the 295 pieces of correct history behind it.

**YouTube records ABSENT and has never once recorded a fabricated zero.** 61,623 snapshots across all time, 0 positive, 0 with a source. This platform has written a fabricated zero three separate times and this is not a fourth.

**A measured zero is not a failure.** 10,980 Instagram and 4,915 TikTok snapshots read zero **with a source**, which means the provider returned the field and the value was genuinely zero. A clip with 153 views and 6 likes has not been reshared. That is a measurement, not a gap.

### Against the known baselines: no regression

| baseline | then | now | verdict |
|---|---|---|---|
| BL-873, Instagram snapshots carrying a share count | **46,270 / 85,591 = 54.1 %** | **68,116 / 126,257 = 53.9 %** | **unchanged within two tenths of a point** |
| BL-819, TikTok clips carrying a positive count | 720 / 1,351 clips | 6,918 of 7,792 snapshots now labelled | improved, and now labelled |
| BL-819, Instagram, pre-fix | **0 of 142,179** | 68,116 in 30 days alone | the fix is live |
| BL-819, YouTube | 0 of 61,400 | 0 of 61,623 | correct and permanent |

### Split by clip type, which is where the owner's row lives

| clip type | platform | snapshots | clips | positive | source set |
|---|---|---|---|---|---|
| ordinary | instagram | 126,244 | 5,813 | 57,136 | 68,112 |
| ordinary | tiktok | 7,792 | 972 | 2,298 | 6,918 |
| ordinary | youtube | 222 | 222 | 0 | 0 |
| **marketplace (v2)** | instagram | **13** | **7** | **0** | **4** |

**Thirteen snapshots across seven clips is the entire marketplace history.** Every one of them, in full, because at this size a summary would hide the answer:

| clip | checked at | views | likes | shares | `sharesSource` | which snapshot |
|---|---|---|---|---|---|---|
| cmu84hotx0 | 2026-09-19 08:25:53.432 | 0 | 0 | 0 | **NULL = ABSENT** | submit |
| cmu84hotx0 | 2026-09-19 13:00:44.229 | 1,399 | 3 | 0 | **NULL = ABSENT** | tick |
| cmu84jd4r0 | 2026-09-19 08:27:11.583 | 0 | 0 | 0 | **NULL = ABSENT** | submit |
| cmu84jd4r0 | 2026-09-19 13:00:44.354 | 388 | 9 | 0 | **`reshare_count`** | tick |
| cmu84wy0z0 | 2026-09-19 08:37:45.190 | 0 | 0 | 0 | **NULL = ABSENT** | submit |
| cmu84wy0z0 | 2026-09-19 13:00:44.480 | 153 | 6 | 0 | **`reshare_count`** | tick |
| cmu855k980 | 2026-09-19 08:44:27.249 | 0 | 0 | 0 | **NULL = ABSENT** | submit |
| cmu855k980 | 2026-09-19 13:00:44.611 | 421 | 7 | 0 | **`reshare_count`** | tick |
| cmu86eyjl0 | 2026-09-19 09:19:45.284 | 0 | 0 | 0 | **NULL = ABSENT** | submit |
| cmu86eyjl0 | 2026-09-19 13:00:44.743 | 118 | 2 | 0 | **NULL = ABSENT** | tick |
| cmu87takj0 | 2026-09-19 09:58:53.670 | 0 | 0 | 0 | **NULL = ABSENT** | submit |
| cmu87takj0 | 2026-09-19 13:00:44.886 | 315 | 11 | 0 | **`reshare_count`** | tick |
| cmu8fa1re0 | 2026-09-19 13:27:52.715 | 0 | 0 | 0 | **NULL = ABSENT** | submit, not yet ticked |

**Every submit row has `checkedAt` equal to the clip's `createdAt` to the millisecond.** They are written inside the same transaction as the post, at `marketplace-v2-poster.ts:953` on current main:

```ts
await tx.clipStat.create({
  data: { clipId: clip.id, views: 0, likes: 0, comments: 0, shares: 0, isManual: false },
});
```

No `sharesSource` is passed, so the column takes NULL, which reads ABSENT. **That is correct and it is the row the owner showed.** The post is milliseconds old; nothing has been measured; the row says so.

**Every tick row carries a real reading.** Four of six name `reshare_count`. The other two are the provider omitting the field, which BL-820 proved live on a real low-engagement post and built the ABSENT case for. All six read `shares = 0` because these are four-hour-old posts with 118 to 1,399 views, and a post with 153 views has not been reshared.

### Is a missing share count merely a consequence of never being polled twice? YES, and that was the whole of it

| clip | tracking job `isActive` | `lastCheckedAt` | snapshots | next check |
|---|---|---|---|---|
| cmu84hotx0 | true | 2026-09-19 13:00:44.311 | 2 | 15:00:00 |
| cmu84jd4r0 | true | 2026-09-19 13:00:44.438 | 2 | 18:00:00 |
| cmu84wy0z0 | true | 2026-09-19 13:00:44.568 | 2 | 18:00:00 |
| cmu855k980 | true | 2026-09-19 13:00:44.694 | 2 | 18:00:00 |
| cmu86eyjl0 | true | 2026-09-19 13:00:44.837 | 2 | 18:00:00 |
| cmu87takj0 | true | 2026-09-19 13:00:44.964 | 2 | 18:00:00 |
| cmu8fa1re0 | **false** | **null** | **1** | 13:27:52.725, in the past |

BL-912's own migration states the cause in its header, and it is quoted here because it is the answer to the brief's question:

> *"`createV2Post` wrote every v2 tracking job with `isActive: false` ... BL-880 fixed the tick and said in the tick itself that this 'is the line that makes activating them safe', then wired activation to the APPROVAL event only and never changed the creation path ... These six are already in the ground: job present, `nextCheckAt` in the past, DUE, `isActive` false and `lastCheckedAt` NULL. Every one of them has exactly one ClipStat, written in the same millisecond as the post, reading 0 views, while the posts have been live on Instagram for hours. Without this they stay dark for ever."*

**So when the owner looked, every marketplace post had exactly one snapshot in existence, and that snapshot was its submit row.** Not because shares failed, but because the clip had never been polled at all. Views, likes and comments were equally unmeasured on that same row.

`isActive` is `true` on the creation path on current main; BL-912 changed it and merged during this round. **The seventh clip, posted at 13:27:52, still shows `isActive: false` because it was created before that change was deployed.** It is due and will be picked up.

### Do shares move as views climb? Yes

Clips with two or more snapshots in the last 7 days:

| platform | clips | views rose | **views rose AND shares rose** | views rose, shares flat but positive | views rose, shares zero |
|---|---|---|---|---|---|
| instagram | 1,085 | 517 | **98** | 100 | 319 |
| tiktok | 143 | 49 | **1** | 13 | 35 |

**98 Instagram clips saw a share count rise in seven days.** The count is live and tracking, not frozen. The TikTok sample is 49 clips and one riser, which is small rather than alarming: TikTok shares move slowly on low-view clips and 2,003 TikTok snapshots carry a positive labelled count.

---

## PART 2 — WHAT THE PROVIDER RETURNED, READ FROM PRODUCTION'S OWN RECORD

The live probe could not run (PART 0). What follows is production's own probe, at `13:00:44` today, through the exact path the tick uses.

| clip | provider returned | stored `shares` | stored `sharesSource` | agree? |
|---|---|---|---|---|
| cmu84jd4r0 | a finite `reshare_count`, value 0 | 0 | `reshare_count` | **yes, MEASURED ZERO** |
| cmu84wy0z0 | a finite `reshare_count`, value 0 | 0 | `reshare_count` | **yes, MEASURED ZERO** |
| cmu855k980 | a finite `reshare_count`, value 0 | 0 | `reshare_count` | **yes, MEASURED ZERO** |
| cmu87takj0 | a finite `reshare_count`, value 0 | 0 | `reshare_count` | **yes, MEASURED ZERO** |
| cmu84hotx0 | no `reshare_count` on the body | 0 | NULL | **yes, ABSENT** |
| cmu86eyjl0 | no `reshare_count` on the body | 0 | NULL | **yes, ABSENT** |

**Stored and returned agree in every case, because `sharesSource` IS the record of what was returned.** `hikerapi.ts:588` sets it only when `numericOrUndef(media.reshare_count)` yields a finite number:

```ts
const shareCountDisabled = media.share_count_disabled === true;
const sharesRaw = shareCountDisabled ? undefined : numericOrUndef(media.reshare_count);
const sharesSource = sharesRaw == null ? null : "reshare_count";
```

There is no path that writes `"reshare_count"` without having read one. **So a stored source is proof of a provider read, and its absence is proof of a provider omission.**

**The field path is verified at production scale rather than by one probe.** 68,116 Instagram snapshots in 30 days named `reshare_count` and 6,918 TikTok snapshots named `shareCount`. Those are 75,034 real provider responses in which the field was found where the code looks for it. BL-746's first four probes read the wrong field shape; 75,034 agreeing responses is a stronger answer than a seventh probe would have been.

**If the provider returns nothing, no code change will conjure one**, and two of the six are exactly that case.

---

## PART 3 — NOTHING IS BROKEN, SO NOTHING WAS CHANGED

**No file was modified. No fourth loss point exists. This round's diff is empty.**

### All three of BL-820's loss points are intact

| # | site | state today |
|---|---|---|
| 1 | `hikerapi.ts:588` — the classifier | reads `reshare_count`, sets the source, **intact** |
| 2 | `hikerapi.ts:1020` — the overlay the tick reads | `sharesSource: res.sharesSource ?? null`, **intact** |
| 3 | `apify.ts:1628` — the batch fold, the one that actually runs | `sharesSource: sr.stats.sharesSource ?? null`, **intact** |
| + | `lamatok.ts:301` and `:489`, both TikTok readers | `share_count` / `shareCount` with the source, **intact** |

### Every one of the eight ClipStat creation sites, checked

| site | writes a source? | verdict |
|---|---|---|
| `tracking.ts:1818` (manual) | yes | correct |
| `tracking.ts:1832` (cron) | yes | correct |
| `clipper-submit-core.ts:754` | yes | correct |
| `owner-submit-core.ts:299` | yes | correct |
| `clips/[id]/override/route.ts:184` | yes, stamps `"manual"` | correct |
| `actions/clips.ts:119` | n/a | correct |
| `marketplace/submissions/[id]/post/route.ts:971` | no, all four metrics 0 | **correct**, v1 submit row, ABSENT |
| `marketplace-v2-poster.ts:953` | no, all four metrics 0 | **correct**, v2 submit row, ABSENT |

**The two that write no source are both submit rows on a post that is milliseconds old.** Writing ABSENT there is the honest answer, and it is the same answer for views, likes and comments.

### The one false comment still in the tree, and why it is not a fourth loss point

`src/lib/scraper-providers/apidojo.ts:681` still reads:

```ts
shares: 0, // Instagram doesn't expose share counts.
```

**That comment is false** — it is the exact claim BL-820 disproved when it found `reshare_count` on every post probed. It deserved a hard look, and it got one, because `apify.ts` imports apidojo and the Instagram tier order calls it:

* `fetchClipStats` reaches `fetchInstagramStats` at `apify.ts:2452`, **after** the Hiker overlay has already run.
* Tier 1, `fetchInstagramStatsApiScraperSingle`, carries a `BL-678` hard-off guard at `:800` and returns null.
* Tier 2 is `fetchApidojoInstagramSingle` at `:754`, and **`apidojo.ts` contains zero references to `APIFY_HARD_OFF`**. The nearest preceding `if (APIFY_HARD_OFF)` branches, at `:583` and `:1327`, are inside the **TikTok** functions and do not gate it.

**It is nevertheless unreachable, and the kill is a credential rather than a branch.** Every one of the four apidojo entry points opens with `const token = getApifyToken(); if (!token) return null;`, and:

```ts
export function apifyCredential(): null {
  return null;
}
```

An unconditional, return-type-annotated `null`. The file's own header records the design: *"returning null here stops all four BEFORE `actorRunUrl()` is called, before any URL string exists and before `fetch()` is reached ... `process.env.APIFY_API_KEY` and `process.env.APIFY_TOKEN` are no longer consulted by this file at all, so no value set anywhere can bring these four paths back."*

**So no share count is lost there, because nothing runs there.** It is a stale false comment on a dead path, the same status BL-717 recorded for the `private` regex. Reported, not fixed: editing a dead path was not this round's job and a diff touching `apify.ts` would have to justify itself against a money file's neighbour for no behavioural gain.

### A second dead-path inconsistency, surfaced by the subagent and checked

`apify.ts:651`, inside `fetchTikTokStatsLegacy`, returns `shares: item.shareCount ?? 0` **with no `sharesSource`**. Its sibling in the batch path at `:1397` does set one, with BL-820's own comment beside it:

```ts
shares: item.shareCount ?? 0,
// BL-820 — ABSENT when the actor omitted the key, never a silent zero.
sharesSource: item.shareCount == null ? null : "shareCount",
```

**BL-820 updated the batch TikTok parser and not the single legacy one.** It is unreachable: `BL-678 GUARD 2 of 5` sits at `:583`, inside the same function and above the return, and it **throws** rather than returning. *(My first check for a guard here scanned lines 600 to 651 and found none, which was a window too narrow by seventeen lines; re-read, the guard is at 583. Disclosed because a near-miss on reachability is how a dead path gets reported as live.)*

Were Apify ever re-enabled, that line would write a positive TikTok count with a NULL source. `isMeasuredShare`'s second clause would still call it measured, so it would read correctly rather than falsely, exactly like the 295 legacy rows. **No fabricated zero and no false accusation**, but the asymmetry should be closed if that path is ever revived.

### A failed read is never treated as a fact

Every share read is `numericOrUndef(...)` or `?? null`, neither of which can throw. A provider error, a malformed body, a missing key and `share_count_disabled: true` all produce `sharesSource: null`, and the row is written exactly as it would have been. **No share path anywhere inspects an exception message**, which is the defect class BL-874 found elsewhere. The `?? 0` that remains is not a fabrication because the column is `NOT NULL` and `sharesSource` carries the meaning; every reader tests the source.

### The fraud rule correction still holds

`fraud.ts` imports `isMeasuredShare` at `:32` and rule 9 filters the share series to measured snapshots only at `:204` to `:216`. `isMeasuredShare` is unchanged:

```ts
export function isMeasuredShare(stat: ShareStatLike): boolean {
  if (stat.sharesSource != null) return true;
  return typeof stat.shares === "number" && stat.shares > 0;
}
```

**12 call sites across the display surfaces and the fraud engine, all reading the one predicate** (22 lines mention the name; 8 are imports, 1 the definition and 1 a comment). A snapshot the screen calls measured and the fraud rule calls unmeasured still cannot exist. Nothing in this round re-arms the false accusation BL-820 prevented, because this round changed nothing.

---

## PART 4 — NOTHING MOVED, AND ONE OF MY OWN QUERIES WAS THE DEFECT

**No sandbox was created**, so there is no `bl914sbx-` prefix, no opening snapshot to reconcile and nothing to tear down. That is the honest shape of a round that measured and changed nothing. **No failure-path users were minted and no 429 assertion was needed**, because no request was made to any route.

### The money files, branch against main

| file | blob OID | |
|---|---|---|
| `clip-earnings-writer.ts` | `416972e9ffb8` | **IDENTICAL** |
| `earnings-calc.ts` | `00410634ee61` | **IDENTICAL** |
| `balance.ts` | `67c30c895181` | **IDENTICAL** |
| `tracking.ts` | `8e2a62f554e2` | **IDENTICAL** |
| `clip-earnings-invariant-middleware.ts` | `61cef3939536` | **IDENTICAL** |
| `money-decimal.ts` | `ef5cdae757b9` | **IDENTICAL** |
| `campaign-era.ts` | `106e16ad7512` | **IDENTICAL** |

Trivially so: the branch carried **0 commits** and the tree was clean.

### Every invariant, across the full population

| invariant | measured | result |
|---|---|---|
| earnings invariant, `abs(earnings − (base + bonus)) > 0.01` | all clips | **0 violations** |
| no overpayment, counting clip earnings + agency + **both** v2 aggregates | 21 budgeted campaigns | **0 over, closest $1.90 UNDER** |
| no double pay, two open payouts on one campaign | all | **0** |
| no double pay, a clip with two agency rows | all | **0** |
| negative money anywhere (clip, v2 editor leg, v2 platform leg) | all | **0 / 0 / 0** |
| positive share count with no source since BL-820 | all snapshots after 2026-08-24 | **0** |
| negative share count with a source | all | **0** |
| marketplace clip earnings | 7 clips | **$0.00 each**, all PENDING |

Nothing was written, so nothing could move: `clip_stats` holds 382,498 rows, the share sum is 33,433,345, approved live earnings read $15,008.92, and the newest payout `updatedAt` is `2026-09-18 17:40:23.69`, **the day before this round**.

### MY FIRST NO-OVERPAYMENT QUERY WAS WRONG AND IT REPORTED A FALSE ALARM

Disclosed because a round that hides this teaches the next round nothing.

The first version reported **3 of 21 campaigns over budget, the worst $308.56 over**. That contradicted BL-627 and BL-898, both of which measured zero, so it was checked before it was believed rather than after.

**The query was the defect.** It omitted `videoUnavailable = false` when summing approved clip earnings, which CLAUDE.md requires on *every* such query, and included the earnings of clips whose videos are gone and which are not payable. On STRAENGE:

```
with unavailable clips included:  2,001.71 + 1,000.54 = 3,002.25   ->  $2.25 OVER
with the required filter:         1,997.56 + 1,000.54 = 2,998.10   ->  $1.90 UNDER
```

**$2,998.10 is BL-627's own published figure for STRAENGE, to the cent.** Corrected, the answer is **0 of 21 over budget, closest $1.90 under**. I broke the project's own documented rule, produced an alarming number, and the thing that caught it was that the number disagreed with two prior rounds.

### Gates, builds and renders: none run, and none claimed

**No build was run and none is claimed. `tsc` was not run. No guard was demonstrated. No render pass was performed.** All four would have been theatre: the diff is empty, no `.tsx` changed, no guard was touched and there is nothing to merge. Stating that is more useful than a green tick on an unchanged tree.

**The BL-678 guards are intact**, measured rather than assumed: **5** numbered `BL-678 GUARD n of 5` sites in `apify.ts` at lines 250, 563, 795, 1322 and 1785, **27** BL-678 references across **7** files, and `APIFY_HARD_OFF: true = true` plus `apifyCredential(): null`. *(The brief says eleven guards and BL-820 said eight comment lines; the code says five numbered guards and 27 references. The measured numbers are printed rather than the remembered one.)*

### What was touched in the live system

**Nothing.** No snapshot was written, because no probe reached a provider. Two files were created and deleted in the shared working tree, `scripts/bl914-probe.ts` and `scripts/bl914-probe2.ts`, both untracked, both removed by explicit path, neither committed.

---

## WHAT THE OWNER SHOULD DO, AND ONE THING WORTH HIS DECISION

**Nothing about shares.** They work. The next tick on each marketplace clip is at 15:00 or 18:00 UTC today and will write another reading.

**Two observations, reported rather than fixed:**

**1. On the submit row, shares is the only honest cell, and that is probably why it caught his eye.** That row stores `views: 0, likes: 0, comments: 0, shares: 0` with a source only possible on shares. So the screen shows three apparently real zeros beside one "not measured". The odd one out is the truthful one. BL-820's accessibility review raised exactly this as item B2 and handled the *no snapshot at all* case; this is the *snapshot of nothing* case and it was not covered, because `clip_stats` has a `sharesSource` column and no equivalent for views, likes or comments. Making the other three honest on a submit row is a real piece of work with a real design question behind it, and it belongs to its own round.

**2. Two dead paths carry stale share handling.** `apidojo.ts:681` asserts in a comment that Instagram has no share counts, which BL-820 disproved, and `apify.ts:651` omits the `sharesSource` its sibling at `:1397` sets. Both are unreachable today. They should be corrected or removed together, so the next reader does not rediscover a claim already disproved and trust it, and so nothing reappears unlabelled if either path is ever revived.

---

## VERIFICATION

Shares were measured before anything was judged and nothing was changed, because nothing is broken: Instagram carries a source on 68,116 of 126,257 snapshots in 30 days against BL-873's 46,270 of 85,591, the same 54 percent within two tenths of a point; TikTok carries one on 6,918 of 7,792; YouTube is ABSENT on all 61,623 snapshots ever written and has never recorded a fabricated zero; and zero snapshots written since BL-820 carry a positive count without a label. The measurement is split by platform, by clip type and by snapshot kind, and every one of the thirteen marketplace snapshots is printed in full with its `::text` timestamp against DB `now()`, showing each submit row written in the same millisecond as its post and each tick row carrying a real reading. A missing share count on a marketplace clip was a consequence of the clip never being polled a second time, proven by tracking jobs that read `isActive false` with `lastCheckedAt` NULL, and BL-912 found and fixed the same cause independently and merged mid-round. Shares move: 98 of 517 Instagram clips whose views rose in seven days saw shares rise. The live probe could not run because neither vendor key exists in this environment, the true cost is $0.00 against a disclosed $0.00415 that was never spent, my own probe's call counter was wrong and is disclosed, and production's own read at 13:00:44 is reported instead with stored and returned agreeing in all six cases. All three BL-820 loss points are intact, all eight ClipStat creation sites were checked individually, and the one false comment left in the tree at `apidojo.ts:681` is proven unreachable through `apifyCredential(): null` rather than assumed dead. No failed read is treated as a fact and the fraud rule still filters to measured snapshots through the one shared predicate across 12 call sites, a figure this report first published as 22 by counting mentions instead of calls and corrected after a subagent returned late and disagreed. Every money file is byte-identical by blob OID, every invariant is clean across the full population including both v2 aggregates, and my own first no-overpayment query was wrong by omitting `videoUnavailable = false` and is disclosed with the corrected figure matching BL-627's STRAENGE to the cent. No build was run and none is claimed, no guard was demonstrated and none was touched, no render was performed and no surface changed. There is nothing to merge: the branch carried 0 commits, was deleted, and the worktree is verified gone by listing the path. This round was briefed to run alone and did not, which is stated first rather than last. **No dashes as bullets.**
