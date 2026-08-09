# BL-748 — the last fabricated zero leaves the Instagram classifier, and nobody was ever harmed by it

**NO CLIPPER'S EARNINGS FELL BECAUSE OF THIS FABRICATION. Not one Instagram clip has ever had its stored views go above 0 and then fall to 0. Zero clips, zero clippers, $0.00.**

**2026-08-09 · Base:** `main @ 6ed3a50c` · **Branch:** `checkpoint/BL-748` `ac083fd1` · **Tags:** `pre-BL-748` = `6ed3a50c`, `post-BL-748` = `ac083fd1`
**No stored views moved down. No clip status or earnings changed. No payout touched. No historical repair run. No Apify actor run. No probe made, $0.00 spent. Handles redacted; every timestamp cast `::text` against DB `now()`.**

---

## THE HEADLINE, AND A CORRECTION TO THE BRIEF

The fix is **one executable line**. But the round was commissioned on a belief that turns out to be false,
and saying so is more valuable than the line:

> "So the fabricated 0 is still live in the tracking path today."

**It is not, and it never was.** `hikerapi.ts:878`, the tracking overlay's accept gate:

```ts
if (typeof views !== "number" || !Number.isFinite(views) || views <= 0) {
  // NEVER trust a Hiker 0/null/NaN/negative. Apify is asked to confirm. This is
  // the bottom of the never-zero invariant — there is no code path through this
  // helper that returns useResult=TRUE without views > 0.
  return { useResult: false, stats: null, reason: "views <= 0 or null", verdict: "transient" };
}
```

**`views <= 0` is rejected.** A fabricated 0 produced `useResult: false`, Apify was asked to confirm, and
nothing was written. BL-746 closed the submit path; **this gate had always closed tracking.** The defect
was real, and it was structurally unreachable on two independent mechanisms.

**It is still worth fixing at source**, which is what this round does: so the two fields stop contradicting
each other, so unknown and genuinely-zero become distinguishable, and so no future caller inherits a lie.
But it is a correctness and hygiene fix, **not the emergency the brief describes**, and the owner should
know that before reading the rest.

---

# PART 0 — EVERY CALLER, MAPPED BEFORE THE CHANGE

This is the work BL-746 could not afford and the reason it stopped.

**`classifyV2Media` has exactly ONE production call site**: `hikerapi.ts:419`, inside `probeHiker`. Every
other match in the repo is a comment or a test script. So the real map is the consumers of the `views` it
produces.

| # | Consumer | file:line | Reads `.views` | With `0` today | With `null` after | Breaks on null |
|---|---|---|---|---|---|---|
| 1 | **`tryHikerForInstagram`, the TRACKING overlay** | `hikerapi.ts:878` | **yes** | rejected by `views <= 0`, returns `useResult:false, verdict:"transient"`, Apify confirms | fails the **same** `typeof views !== "number"` test in the **same condition**, returns the **identical** object | **NO** |
| 2 | **`clipper-submit-core.ts`, the SUBMIT path (BL-746)** | `:281`, guard at `:295` | **yes** | already skipped: BL-746 requires `viewSource != null` | skipped | **NO** |
| 3 | `clip-thumbnail.ts` cover frame | `:309` | **NO**, reads `rawBody` only | n/a | n/a | **NO** |
| 4 | `retire-dead-clips.ts` BL-720 gone-clip | `:297` | **NO**, reads `httpStatus` and `exc_type` | n/a | n/a | **NO** |
| 5 | `hikerapi-shadow` OWNER diagnostic | `route.ts:251` | yes, **JSON only** | displays `0` | displays `null`, strictly more honest | **NO** |
| 6 | `scripts/test-bl610-carousel.ts` | `:29,47,58` | yes, test | exercises the **carousel** branch | untouched | **NO** |

**Not one caller relies on receiving 0.** Consumers 3 and 4 never read the field at all, which was checked
by grep rather than assumed. **That is the proof BL-746 lacked, and it is what makes a source fix safe.**

**The quarantined carousel paths BL-610 owns are untouched**: image-only and mixed-carousel-with-no-readable-count
already return `null` from a **different branch** (`hikerapi.ts:555` and `:583`), and this round changes only
the single-video branch at `:603`.

---

# PART 1 — THE DAMAGE, MEASURED

## 1.1 The three populations, live

`db_now = 2026-08-09 15:35:12.905376+00`, over every non-deleted clip:

| Population | Instagram | TikTok | YouTube | Earnings |
|---|---|---|---|---|
| **A. views went above 0 then FELL to 0** | **0** | 5 | 45 | $2.91 + $3.31 |
| **B. stuck at 0 since the first stat** | 49 | 60 | 76 | **$0.00** |
| **C. never counted at all** | 50 | 1 | 0 | **$0.00** |
| D. healthy, max views above 0 | 2,432 | 1,192 | 1,319 | $12,118 |

**Population A is the one that would mean harm, and it contains ZERO Instagram clips.** The 50 that did
fall are **45 YouTube and 5 TikTok**, which never touch this Instagram-only classifier. They are a
different, pre-existing phenomenon (a re-uploaded or deleted video, or a provider hiccup on those
platforms) and **this round does not attribute them to the fabrication, because the evidence does not
support it.**

## 1.2 The 49 Instagram stuck-at-zero clips are NOT this fabrication

| status | clips | oldest zero stat | **newest zero stat** | earnings | clippers |
|---|---|---|---|---|---|
| REJECTED | 37 | 2026-05-15 13:02:38.832 | **2026-07-17 01:31:39.599** | $0.00 | 18 |
| APPROVED | 12 | 2026-06-02 08:18:45.077 | **2026-07-16 01:50:10.722** | $0.00 | 8 |

**Every one predates the 2026-07-22 Apify cutover**, and therefore predates the Hiker submit path by three
weeks. They came from the **old Apify path**, which could return a real 0. **All carry $0.00 of earnings.**

## 1.3 Reconciled against BL-746 and BL-745

* **BL-746's "newest zero-view Instagram row 2026-07-26"**: consistent. That measurement counted all zero-view rows including retired and rejected clips; restricted to clips whose **maximum** view is 0, the newest is 2026-07-17.
* **BL-745's "41 clips with no stats at all"**: that is **population C**, measured at 50 today. It churns between 41 and 57 as rejected and retired clips enter and leave, which BL-747 also observed (57 then 42 within half an hour).

## 1.4 The answer to the first-line question

**No clipper's earnings fell because of a fabricated 0.** Affected clippers: **0**. Money: **$0.00**. The
brief asked for this in the first line if it were true; it is not true, and the first line says so.

---

# PART 2 — THE FIX, AT SOURCE

## 2.1 The diff

```diff
   const singleProbe = extractViewCount(media);
   if (mediaType === 2 || singleProbe != null) {
     const cls: HikerClassification = classifyInstagramUrl(origUrl) === "reel" ? "reel" : "single_video";
     return {
-      views: singleProbe?.value ?? 0,
+      views: singleProbe?.value ?? null,
```

**One executable line.** The other 39 added lines are the comment justifying it, which records the caller
map above so the next reader does not have to redo it.

## 2.2 Each line justified

* **`?? null` instead of `?? 0`.** BL-543's rule is absolute: an unresolvable count is UNKNOWN, and unknown must be null so the clip keeps its last-known value. A 0 is a positive claim that nobody watched. `ClipStat.views` is a non-nullable `Int`, so writing it would freeze a clipper's earnings at zero.
* **No type change was needed.** `HikerResult.views` is already declared `number | null` (`hikerapi.ts:67`), so the fabricated 0 was never even required by the type.
* **The two fields stop contradicting each other.** `viewSource` on the very next line was already `singleProbe?.key ?? null`. Before this change a hidden count reported `views: 0` **and** `viewSource: null`: one field said "zero views", the other said "no field was read". They now agree.
* **The carousel branch is the precedent, not an invention.** Forty lines up, `:583` already returns `usedKey === null ? null : sum`, with a comment stating that returning 0 "would zero a clipper's views". This branch was written without that care. The fix makes the file internally consistent.

## 2.3 A genuine zero is still a zero, and that is the point

`extractViewCount` returns `{ value: 0, key: "play_count" }` when the field **is present and reads 0**, so
`singleProbe` is non-null and the branch yields `views: 0` with a real `viewSource`. **Unknown and
genuinely-zero are now tellable apart**, which is precisely the property that was missing:

```
hidden count   ->  views null,  viewSource null
genuine zero   ->  views 0,     viewSource "play_count"
```

## 2.4 No caller needed changing

Because every consumer in PART 0 already treats 0 and null identically, **no downstream change was
required**, and none was made. That is the difference between fixing at source and adding a second guard:
BL-746 had to add a guard because it could not prove this; this round proved it.

## 2.5 One copy fix, caused by this change

`hikerapi-shadow/route.ts:694` told the owner that image-only carousels are the only null-views case. That
became **incomplete**, so a new note was added stating that a reel or single_video also returns null when
Instagram hides the count, **and warning that the flip-gate numbers are not comparable across BL-748**:
those rows previously entered the distribution as `pct_diff -100` and now drop out of `compared` entirely,
so a class could move from NO-GO to INSUFFICIENT purely from this change. **That is the honest verdict, not
a regression**, and it is stated in the endpoint's own output so the owner meets it where the numbers are.

---

# PART 3 — THE TRACKING PATH IS SAFE

## 3.1 Proven by the harness, before and after at every consumer

`scripts/test-bl-748-no-fabricated-zero.mjs` drives the **real exported `classifyV2Media`** and **extracts
both shipped gates from source** so it cannot drift. **39 passed, 0 failed, exit 0.** It makes no network
call and writes nothing.

```
TRACKING rejected the fabricated 0 before          PASS
TRACKING rejects null after, via the SAME condition PASS
TRACKING outcome is IDENTICAL, so the tick cannot change   PASS
TRACKING still accepts a real positive count       PASS
SUBMIT skipped the fabricated 0 before             PASS
SUBMIT skips null after                            PASS
SUBMIT outcome is IDENTICAL                        PASS
SUBMIT still writes a genuine 0 (real viewSource)  PASS
clip-thumbnail.ts never reads res.views            PASS
retire-dead-clips.ts never reads res.views         PASS
```

## 3.2 No stored views can move down

**Structurally.** The tracking overlay returns `useResult: false` for both 0 and null, so it writes no
`ClipStat` in either case and the clip keeps its last-known value. The submit path only ever writes a
**first** snapshot, where there is no prior value to lower. **There is no code path in which this change
lowers a stored number.**

**Measured.** Population A in PART 1.1 contains **zero Instagram clips**, before and after.

## 3.3 Hidden count keeps last-known, genuine zero still records

| Case | Result | Stored effect |
|---|---|---|
| Instagram hides the count | `views null`, `viewSource null` | overlay rejects, **clip keeps its last-known value** |
| Post genuinely has 0 plays | `views 0`, `viewSource "play_count"` | a **real 0** is available and distinguishable |

## 3.4 The tick budget

**The change adds no call, no await and no branch.** It substitutes one value in an object that was already
being returned, so the tick's timing cannot move.

**A correction on the number itself:** `CLIPS_PER_TICK` is **not set** in the environment, so the code
default of **30** applies (`tracking.ts:164-178`, clamped to a 5 to 500 band), not the 90 the brief states.
BL-197 lowered it from 60 to 30 precisely so a tick finishes inside the 300s ceiling and releases its lock.
Either way this round cannot affect it.

---

# PART 4 — NO HISTORICAL REPAIR IS NEEDED

PART 4 asked for a repair spec **if** clips were wrongly zeroed. **None were.**

* **Population A**, the only population that would represent harm, holds **zero Instagram clips**.
* **Populations B and C** carry **$0.00** between them and predate this code path by three weeks.
* **Rows to repair: 0. Money to recover: $0.00.**

**No repair was run, and none is spec'd, because there is nothing to repair.** That is the best possible
answer to that part, and it is why BL-716's and BL-718's warning about repairing money rows does not need
to be invoked here.

---

# PART 5 — THE EVIDENCE

## 5.1 Hidden count returns null; genuine zero returns 0

From the harness, driving the real classifier:

```
video whose count Instagram HIDES        views null,  viewSource null            (was 0)
video with a GENUINE zero play_count     views 0,     viewSource "play_count"
ordinary reel with a real count          views 160,   viewSource "play_count"
video exposing only ig_play_count        views 77,    viewSource "ig_play_count"
image-only carousel                      views null,  viewSource null            (already correct)
mixed carousel, no readable child count  views null,  viewSource "carousel_sum:none"  (already correct)
mixed carousel with counts               views 140,   viewSource "carousel_sum:play_count"
```

**THE TWO ARE DISTINGUISHABLE: PASS.** Every unknown case additionally asserts `views !== 0`.

## 5.2 No stored views moved down, no earnings changed

**Nothing was written.** This round made **no probe, no Apify run and no DB write**; every query went
through `run-select.js`, which refuses write keywords. Platform at `15:56:03`: **4,261 approved clips,
$12,005.04, 205,576 stat rows, 163 payout rows, invariant violations 0.**

## 5.3 Byte-identity

```
IDENTICAL  clip-earnings-writer  earnings-calc  balance  tracking
IDENTICAL  clip-earnings-invariant-middleware  money-decimal  campaign-era  apify.ts
```

**`apify.ts` byte-identical means no BL-678 guard was touched**; it carries the same **8** BL-678 comment
lines on both refs. **The eleven guards are a count of guards, not of that string, so 8 is the honest
measure of the grep and the blob equality is the stronger proof.** **No Apify actor was run.**

## 5.4 A BONUS FINDING THAT CLOSES BL-747's OPEN QUESTION

BL-747 had to report honestly that it **could not confirm BL-746 was live**. It now is, measured here.

Three Instagram clips submitted this afternoon each received a first `ClipStat` **0.0 seconds after
submit**, inside the submit transaction:

| clip | submitted | first stat | delay | views |
|---|---|---|---|---|
| `cmslyvoxi005f0...` | 15:38:10.806 | 15:38:10.851 | **45ms** | 0 |
| `cmslyyvq6006e0...` | 15:40:39.582 | 15:40:39.622 | **40ms** | 0 |
| `cmslz2ytj007u0...` | 15:43:50.215 | 15:43:50.244 | **29ms** | 0 |

**Against BL-745's measured median of 3,610 seconds and 0 of 777 within a minute, that is the fix working.**

**Their views are 0, and that is a GENUINE zero, provably rather than by assumption.** BL-746's guard writes
a first stat **only** when `viewSource` is non-null, so **the row's existence is itself proof that a real
`play_count` field returned 0** on a reel that was seconds old. A fabricated one would have been skipped and
no row would exist.

**And it cannot harm them.** All three carry **active 60-minute tracking jobs with no `INFRA_DEFER`**
(`nextCheckAt 17:00`), so the count rises on the next tick. **A first snapshot can only raise a clip from
nothing; BL-543's concern is a 0 REPLACING a higher value, which cannot happen on a first stat.**

## 5.5 Gates, stated honestly

* `npm ci` **exit 0**; `npx prisma generate` **exit 0**, run **after** it because `npm ci` wipes the client. Clean worktree at `C:/b748`, a short path, `.env`/`.env.local` copied, **no `node_modules` junction**.
* `tsc --noEmit` **exit 0, 0 errors** (log 0 lines), run twice, before and after the copy fix.
* `npm run build` **exit 0**, `✓ Compiled successfully`, three times (initial, after the copy fix, and post-commit), read from a log with the exit code **echoed, never piped through `tail`**.
* Hooks gate **11 problems, 0 errors, 11 warnings, at the limit of 11**, **eslint v9.39.4 confirmed present**.
* Harness **39/0, exit 0**.
* Push **verified**: `safe-push.mjs` `VERIFIED PUSHED`, `git ls-remote` agrees, `pre-BL-748` on the true base `6ed3a50c` (equals `HEAD~1`).
* **`C:/b575` left exactly as found**: `91b84410`, 77 dirty paths, re-checked after the push. It was stale and dirty, so a separate clean worktree was used.

## 5.6 Accessibility

Reviewed before shipping. **No UI change is required and none was made.** The shadow endpoint is **JSON
only**: a full-repo search found no `.tsx` rendering it, no admin page fetching it and no nav link to it;
the owner pastes the URL into a browser and reads raw JSON, where `0` and `null` are visibly different
tokens. The classifier change is invisible to every rendered surface because **`ClipStat.views` is
non-nullable** (`schema.prisma:1122`), so a null can never be persisted or reach a component.

Two findings from that review, one actioned and one deferred. **Actioned:** the `notes` string in PART 2.5.
**Deferred, its own round:** `ClipCardNew.tsx:195` renders `stat ? formatNumber(stat.views) : "0"`, so a
clip with **no stats at all** shows a literal `0`, **visually and audibly identical to a genuine zero**.
That is the presentation-layer twin of the defect fixed here. The same conflation appears at
`clips/page.tsx:434`, `admin/clips/page.tsx:1628` and `:2115`, `campaigns/[id]/page.tsx:989` and
`CampaignDetailPremium.tsx:921`; `CreatorScanPanel.tsx:975` and `admin/analytics/page.tsx:704` already use
an em dash and are the pattern to copy. Also noted: `utils.ts:15-19` `formatNumber` **throws** on a nullish
input rather than returning a sentinel, unreachable today because of the non-nullable column, but the first
thing to break if that ever loosens.

---

# WHAT SHIPPED

`src/lib/scraper-providers/hikerapi.ts` (**one executable line**) and
`src/app/api/admin/hikerapi-shadow/route.ts` (one note string), plus
`scripts/test-bl-748-no-fabricated-zero.mjs` and the `BACKLOG.md` entry.
**4 files, 310 insertions, 1 deletion.**

**Rollback:** `git revert -m 1 <merge>`, or `git reset --hard pre-BL-748`. **Nothing to undo in the
database.**

**Not merged to main.** This is a branch round; the merge is its own step.

---

# WHAT COULD NOT BE ESTABLISHED

* **How often Instagram actually hides a single video's play count.** The case is now handled honestly, but its real-world frequency needs a sample of live video posts and no probe was made this round, deliberately, since the fix did not require one.
* **Whether the three zero-view first stats in PART 5.4 reflect posts with genuinely no plays, or posts Instagram had not yet indexed.** Both are consistent with a real `play_count: 0`, both resolve upward on the next tick, and neither can harm the clipper. Re-reading those three clips after 17:00 would settle it.
* **The 45 YouTube and 5 TikTok clips in population A.** They are outside this classifier and were not investigated. If the owner wants them explained, that is its own round.
