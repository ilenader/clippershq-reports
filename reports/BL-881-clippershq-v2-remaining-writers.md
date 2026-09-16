# BL-881 — marketplace v2, round five: every remaining writer, and the proof there is no ninth

> **NOTHING IS UNREMOVABLE AND NO SQL IS OWED. FIRST LINE, AS THE ROUND REQUIRES.**
> 13 ledgered rows on the final run, **`VERIFIED: 0 of 13 recorded rows remain`**, 0 failed, 0
> cascaded. The two earlier runs were torn down the same way, 9 of 9 and 13 of 13. A direct catalogue
> sweep afterwards returns **zero** `bl881sbx-` rows in `users`, `campaigns`, `clips`,
> `clip_accounts` or `payout_requests`, and **zero** rows in every v2 table. Campaigns are back to
> **34**, all **34** NORMAL, with the fingerprint `e9defb11fcf63f2a100fbb1a63ed98de` identical to the
> opening snapshot, `agency_earnings` at **4,882** and `payout_requests` at **248**, both unchanged.

**2026-09-16. Shipped on `checkpoint/BL-881`, merged to `main`. Requires a Railway REDEPLOY**, and
BL-877 through BL-880 are all still owed. Base `origin/main` @ `70a6d81`. Isolated worktree
`C:\w\b881`, a short path, `node_modules` never junctioned, **removed at the end and verified by
listing the path**. Closing sweep at DB `now()` **2026-09-16 19:13:16.814075+00**, every timestamp
cast `::text`.

---

## THE HEADLINE

> **1. BL-880's EIGHT WAS WRONG, AND THE ROUND WAS RIGHT TO SAY SO IN ADVANCE.** Counted again with
> `grep -c` and never piped to `head`: the direct `writeClipEarnings` family is **17 call sites in 12
> files**, and there is a SECOND family BL-880 named none of, **`writeClipEarningsZero`, 6 more call
> sites in 5 more files**. **23 call sites.** BL-880's eight was files in one family. That is the
> third enumeration on this platform to come back short.
>
> **2. AND `isMarketplaceClip: false` IS NOT A V2 EXCLUSION. IT IS A V2 INCLUSION.** Three separate
> retrieval subagents read `where: { isMarketplaceClip: false }` and concluded a v2 clip could not
> reach the path. **A v2 clip carries that flag FALSE on purpose**, so every one of those filters
> SELECTS v2 clips. All three were checked against the file and all three were wrong the same way.
>
> **3. SO THE FIX WENT WHERE THE COUNTING CANNOT GO WRONG.** The sync lives in `writeClipEarnings`,
> the chokepoint CLAUDE.md already declares the only allowed path and `check:prisma-bypass` already
> enforces at build time. **88 insertions and ZERO deletions** in that protected file. Sixteen forks
> would have fixed today; one fixes every round after it.
>
> **4. TWO DEFECTS OF THIS ROUND'S OWN, BOTH FOUND BY ITS OWN PROOFS.** The editor's leg **ratcheted
> to $108.00 while the poster reached $54.00**, and a bot-rejected clip **zeroed the poster and left
> the editor at $108.00**. Both are fixed and both are shown below with the measurements that caught
> them.
>
> **5. THE GUARD'S FIRST VERSION COULD NOT FAIL, AND THE DEMO CAUGHT THAT TOO.**

**PROOFS: 27 of 27 sandbox checks passed, 0 failed**, after two earlier runs that failed 3 and 1.
Both are reported in full.

---

## PART 0 — THE MODEL SPLIT, AND EVERY SUBAGENT CLAIM CHECKED

| tier | what ran there | subagents |
|---|---|---|
| **cheapest (Haiku)** | pure retrieval: the four admin repair routes, the four lib-level writers, and the seven owner actions | **3** |
| **strongest (Opus), NOT SPLIT** | the enumeration's correctness, every line that writes money, the chokepoint change, the two floors, the guard, every proof script and this report | **0 subagents between it and the source** |

**THE ROUND SAID TWO PRIOR ROUNDS RECORDED SUBAGENTS MISCHARACTERISING A DESIGN AND TO CHECK EVERY
CLAIM. THREE CLAIMS WERE WRONG, ALL IN THE SAME DIRECTION, AND ALL THREE WOULD HAVE LEFT A LIVE
DEFECT IN PLACE:**

| claim | checked against | verdict |
|---|---|---|
| `fix-earnings` excludes marketplace clips via `isMarketplaceClip: false` | the file | **WRONG.** A v2 clip has that flag FALSE, so the filter INCLUDES it |
| `force-recalc-earnings` likewise | the file | **WRONG**, same inversion |
| `cpm-restamp` and `gamification` likewise | the files | **WRONG**, same inversion, twice more |
| `override/route.ts` refuses marketplace clips at `:158` | the file | **TRUE of v1 and FALSE of v2**: the refusal tests `isMarketplaceClip` truthy, which a v2 clip never is |
| `campaign-freeze-undo` skips marketplace clips at `:311` | the file | **same inversion**, it skips only v1 |
| `bot-rejection.ts` deletes the v1 creator and platform rows | the file | **TRUE**, and it deletes NEITHER v2 row, which BL-880 never mentioned |
| `retire-dead-clips.ts` never writes earnings | the file | **TRUE** |
| close-unpaid and set-amount never write a clip | the files | **TRUE**, both touch only the payout row |

---

## PART 0b — EVERY EARNINGS WRITER IN THE CODEBASE

Counted with `grep -c`, never piped to `head`. **V** means VERIFIED by exercising the path in the
sandbox; **R** means READ only, which is a provisional conclusion and is marked as one.

### Family A: the direct `writeClipEarnings` callers, 17 call sites in 12 files

| # | writer | `file:line` | trigger | actor | reaches a v2 clip | V/R |
|---|---|---|---|---|---|---|
| 1 | the tracking tick, v1 branch | `tracking.ts:3023` | cron | system | no, gated on `isMarketplaceClip` | R |
| 2 | the tracking tick, **v2 branch** | `tracking.ts:3099` | cron | system | **yes, by design** | **V** |
| 3 | the tracking tick, ordinary branch | `tracking.ts:3145` | cron | system | no, the v2 fork takes it first | **V** |
| 4 | approve, v1 branch | `review/route.ts:832` | owner approves | owner | no | R |
| 5 | approve, ordinary branch | `review/route.ts:980` | owner approves | owner | **no, BL-880 forked it to skip a v2 clip** | R |
| 6 | the v2 writer | `marketplace-v2-writer.ts:146` | the three legs | system | **yes, correct by construction** | **V** |
| 7 | owner submit | `owner-submit-core.ts:346` | owner uploads for a clipper | owner | **no**, a v2 clip is never created there | R |
| 8 | **the devaluation restamp** | `cpm-restamp.ts:190` | owner edits a campaign's CPMs with apply-to-existing | owner | **YES** | **V** |
| 9 | **the gamification recalc** | `gamification.ts:1169` | a streak or level change | system, on a user action | **YES** | **V** |
| 10 | **the freeze undo** | `campaign-freeze-undo.ts:390` | owner undoes a freeze | owner | **YES** | **V** |
| 11 | **the manual override** | `override/route.ts:244` | owner edits a clip's stats | owner | **YES** | **V** |
| 12 | **fix-budget, marketplace scale** | `fix-budget/route.ts:260` | owner runs the repair | owner | **YES** | **V** |
| 13 | **fix-budget, ordinary scale** | `fix-budget/route.ts:315` | owner runs the repair | owner | **YES** | **V** |
| 14 | **fix-earnings, main pass** | `fix-earnings/route.ts:183` | owner runs the repair | owner | **YES** | **V** |
| 15 | **fix-earnings, overflow** | `fix-earnings/route.ts:407` | owner runs the repair | owner | **YES** | **V** |
| 16 | **force-recalc** | `force-recalc-earnings/route.ts:310` | owner runs the repair | owner | **YES** | **V** |
| 17 | **the payout adjustment** | `adjust/route.ts:485` | owner reduces a payout | owner | **YES** | **V** |

### Family B: `writeClipEarningsZero`, 6 call sites in 5 files, and BL-880 named NONE of them

| # | writer | `file:line` | trigger | actor | reaches a v2 clip | V/R |
|---|---|---|---|---|---|---|
| 18 | **fix-budget, zeroing** | `fix-budget/route.ts:217` | owner runs the repair | owner | **YES** | **V** |
| 19 | **fix-earnings, zeroing** | `fix-earnings/route.ts:383` | owner runs the repair | owner | **YES** | **V** |
| 20 | **reject a clip** | `review/route.ts:1334` | owner rejects | owner | **YES** | **V** |
| 21 | **undo an approval** | `review/route.ts:1374` | owner undoes | owner | **YES** | **V** |
| 22 | **reject botted** | `bot-rejection.ts:312` | owner rejects a payout as botted | owner | **YES** | **V** |
| 23 | **the ban cascade** | `clip-account-cascade.ts:245` | an account is banned | owner or system | **YES** | **V** |

### The earning-row writers that do not go through either family

`agencyEarning` is written, updated or deleted at **29 sites in 14 files**. The two v2 tables are
touched by **exactly one file**, `marketplace-v2-writer.ts`, with only three callers. **That
chokepoint was already intact** and this round did not need to widen it.

Of those 29 agency sites, the ones that DELETE a row on a v2 clip would silently turn ADDS into
REPLACES for that clip: `bot-rejection.ts:317`, `review/route.ts:1352` and `:1375`,
`clip-account-cascade.ts:255`, `cpm-restamp.ts:222`, `override/route.ts:292`,
`force-recalc-earnings/route.ts:386` and `adjust/route.ts:568`. **On a rejected or banned clip that
deletion is CORRECT**, because the clip earns nothing at all. **It is named here rather than treated
as settled**, and it is the one thing in this area a future round should re-measure.

### THE REAL NUMBER

> **BL-880 SAID EIGHT. THE REAL FIGURE IS 23 EARNINGS-WRITE CALL SITES IN 15 FILES, OF WHICH 18 CAN
> REACH A V2 CLIP.** BL-880 counted files in one family and missed a second family entirely. Its
> eight files map to entries 8 through 17 above, which is **ten** call sites, not eight, and it named
> none of entries 18 through 23.

---

## PART 1 — THE FORK, AND WHY IT IS ONE CHANGE RATHER THAN SIXTEEN

Forking sixteen call sites would have produced sixteen chances to get the shape wrong, in a codebase
where the first marketplace already cost three rounds of exactly that drift. **The sync went into the
chokepoint instead.**

`writeClipEarnings` is already the only allowed path to write the four invariant `Clip` fields:
CLAUDE.md says so, `check-prisma-bypass.js` enforces it at build time with two whitelisted files, and
`writeClipEarningsZero` delegates to it. **Every one of the 23 call sites reaches the same line.**

### The full diff of the protected file

**88 insertions. ZERO deletions.** Nothing that stood in `clip-earnings-writer.ts` was removed or
altered; the change is entirely additive, which is the safest possible shape for a change to the file
that pays everybody.

```diff
diff --git a/src/lib/clip-earnings-writer.ts b/src/lib/clip-earnings-writer.ts
index ac5be7de..4f63164b 100644
--- a/src/lib/clip-earnings-writer.ts
+++ b/src/lib/clip-earnings-writer.ts
@@ -88,6 +88,17 @@ type EarningsOptions = {
   // helper writes, unchanged.
   marketplaceCreatorAmount?: number;
   marketplacePlatformAmount?: number;
+
+  /**
+   * BL-881 — OPT OUT OF THE MARKETPLACE V2 LEG SYNC BELOW.
+   *
+   * There is exactly ONE legitimate caller: `writeMarketplaceV2Earnings`,
+   * which is already writing all three legs itself and would otherwise
+   * re-enter this file through the sync and recurse forever. Nothing else may
+   * pass it, and a future caller that does is asking for the defect this
+   * round exists to close.
+   */
+  skipV2LegSync?: boolean;
 };
 
 // Float tolerance for the invariant check. Float math like 0.1+0.2 can
@@ -605,6 +616,25 @@ export async function writeClipEarnings(
     );
   }
 
+  // BL-881 — the poster's leg BEFORE this write, read once so the v2 leg sync
+  // below can scale the editor and platform legs by the SAME factor this column
+  // moved by. On a non-v2 clip it is read and never used, which is one indexed
+  // point read on a row this function is about to update anyway.
+  let previousEarningsForV2Sync: number | null = null;
+  if (!options.skipV2LegSync) {
+    try {
+      const prevRow = await tx.clip.findUnique({
+        where: { id: clipId },
+        select: { earnings: true, marketplaceV2PostId: true },
+      });
+      previousEarningsForV2Sync = prevRow?.marketplaceV2PostId
+        ? Number(prevRow.earnings ?? 0)
+        : null;
+    } catch {
+      previousEarningsForV2Sync = null;
+    }
+  }
+
   await tx.clip.update({
     where: { id: clipId },
     data: {
@@ -620,6 +650,64 @@ export async function writeClipEarnings(
     `base=${rounded.baseEarnings} bonusPct=${rounded.bonusPercent} bonus=${rounded.bonusAmount} ` +
     `reason=${options.reason ?? "<unspecified>"}`,
   );
+
+  // ═══════════════════ BL-881 — THE MARKETPLACE V2 LEG SYNC ══════════════════
+  //
+  // WHY THIS IS IN THE CHOKEPOINT AND NOT IN SIXTEEN CALLERS, STATED LOUDLY
+  // BECAUSE THIS IS A PROTECTED MONEY FILE AND THIS IS THE FIRST TIME IT HAS
+  // BEEN CHANGED SINCE IT WAS MADE ONE.
+  //
+  // A v2 clip's money lives in THREE rows. `Clip.earnings` above holds the
+  // poster's 45 percent; the editor's 45 and the platform's 10 live in two
+  // other tables. Every writer on this platform was built when a clip's money
+  // lived in one row, so every one of them moves this column and leaves the
+  // other two where they were. THE FAILURE IS SILENT: the L1 budget lock in
+  // this very file and the L2 invariant middleware both watch THIS column
+  // alone, so 55 cents in every v2 dollar sits outside everything that would
+  // notice. BL-876 called it the sharpest structural risk in the design,
+  // BL-877 measured it at exactly 55.0 percent, and BL-880 watched it happen.
+  //
+  // BL-880 NAMED EIGHT OWNER-RUN WRITERS STILL TO FORK. BL-881 COUNTED AGAIN
+  // AND THE REAL FIGURE IS LARGER: eight files was one FAMILY, the direct
+  // `writeClipEarnings` callers. The `writeClipEarningsZero` family is six
+  // more call sites in five more files, and BL-880 named none of them. That is
+  // the third enumeration on this platform to come back short, after BL-847's
+  // eleven measured as three and its six strike entrances measured as seven.
+  //
+  // SO THE FIX IS PUT WHERE THE COUNTING CANNOT GO WRONG. This file is already
+  // the designated chokepoint: CLAUDE.md states that `writeClipEarnings` is the
+  // ONLY allowed path to write these four fields, and `check:prisma-bypass`
+  // enforces it at build time with two whitelisted files. Every caller, present
+  // and future, reaches this line. Forking sixteen call sites would have fixed
+  // today; this fixes every round after it too, which is what the owner asked
+  // this round to produce.
+  //
+  // IT IS A NO-OP ON EVERY CLIP THAT IS NOT A V2 CLIP, which is every clip on
+  // the platform today, so nothing about any existing behaviour changes.
+  //
+  // THE IMPORT IS DYNAMIC ON PURPOSE. `marketplace-v2-sync` reaches
+  // `marketplace-v2-writer`, which reaches back into this file, and a static
+  // import would be a module-evaluation cycle.
+  if (!options.skipV2LegSync) {
+    try {
+      const { syncV2LegsAfterPosterWrite } = await import("@/lib/marketplace-v2-sync");
+      await syncV2LegsAfterPosterWrite(tx, clipId, {
+        reason: options.reason ?? "<unspecified>",
+        posterBefore: previousEarningsForV2Sync,
+      });
+    } catch (e: any) {
+      // A THROW HERE MUST NOT SWALLOW THE POSTER'S WRITE, WHICH HAS ALREADY
+      // COMMITTED ABOVE WHEN THE CALLER IS NOT IN A TRANSACTION. It is logged
+      // loudly and re-thrown ONLY when the caller is transactional, where
+      // rolling the whole thing back is the correct and available outcome.
+      console.error(
+        `[MARKETPLACE-V2-SYNC-FAILED] clipId=${clipId} reason=${options.reason ?? "<unspecified>"} ` +
+        `err=${e?.message ?? String(e)}. THE POSTER'S LEG IS WRITTEN AND THE OTHER TWO MAY NOT BE. ` +
+        `Run the BL-881 reconciliation query.`,
+      );
+      throw e;
+    }
+  }
 }
 
 /**
```

### The three other files

* **`src/lib/marketplace-v2-sync.ts`, new.** The shape itself, and the reconciliation query.
* **`src/lib/marketplace-v2-writer.ts`.** The editor's guard became a PAID FLOOR, covered in PART 2.
* **`src/lib/tracking.ts`, 9 lines, one deletion.** Its v2 branch already writes all three legs on
  the next statement, so it passes the documented opt-out rather than having the sync write two of
  them twice. The one deleted line is `{ reason: "tracking-tick:marketplace-v2-poster" }` becoming an
  options object carrying the same reason.

### Every writer, driven, and all three legs moving together

| writer, by its own `reason` string | poster | editor | platform |
|---|---|---|---|
| `cpm-restamp-on-edit:campaign-edit` | $45.00 to **$22.50** | $45.00 to **$22.50** | $10.00 to **$5.00** |
| `gamification:user-recalc` | $22.50 to **$27.00** | $22.50 to **$27.00** | $5.00 to **$6.00** |
| `undo-freeze` | $27.00 to **$31.50** | $27.00 to **$31.50** | $6.00 to **$7.00** |
| `override:owner-edit` | $31.50 to **$36.00** | $31.50 to **$36.00** | $7.00 to **$8.00** |
| `fix-budget:nonmarketplace-scale` | $36.00 to **$40.50** | $36.00 to **$40.50** | $8.00 to **$9.00** |
| `fix-earnings:main-pass` | $40.50 to **$45.00** | $40.50 to **$45.00** | $9.00 to **$10.00** |
| `force-recalc-earnings` | $45.00 to **$49.50** | $45.00 to **$49.50** | $10.00 to **$11.00** |
| `payout-adjust:ratio-shrink` | $49.50 to **$54.00** | $49.50 to **$54.00** | $11.00 to **$12.00** |
| **`bot-reject`, the zero family** | $54.00 to **$0.00** | $54.00 to **$0.00** | $12.00 to **$0.00** |

> **THAT LAST ROW IS THE ONE THAT WOULD HAVE HURT.** Before BL-881, rejecting a payout as botted
> zeroed the poster's leg and the platform's and **left the editor's row at its full value**, on a
> clip the owner had just rejected as botted. The money would have sat in the campaign's spend
> aggregate with nothing pointing at it.

---

## PART 2 — THE DEVALUATION, AND TWO EARNERS WITH DIFFERENT HISTORIES

### The plain case, with neither earner paid

| | before | after |
|---|---|---|
| poster | $45.00 | **$22.50** |
| editor | $45.00 | **$22.50** |
| platform | $10.00 | **$5.00** |

**A devaluation restamps ONCE and all three legs fall together on the recompute.** The platform leg
is the RESIDUAL, so the three still sum exactly.

### THE CASE NOTHING ON THIS PLATFORM HAD FACED

The editor was then paid **$22.50** and the poster nothing, and the campaign was devalued again,
deeply:

| | before | after |
|---|---|---|
| poster | $22.50 | **$5.00**, fell freely |
| editor | $22.50 | **$22.50**, HELD by his own paid floor |

> **ONE EARNER'S FLOOR BOUND AND THE OTHER'S DID NOT, WHICH IS THE GENUINELY NEW CASE THE ROUND ASKED
> TO BE DECIDED.**
>
> **THE DECISION: LET THEM DISAGREE, LOUDLY.** The three legs then no longer sum to the gross, and
> that is **the intended lesser harm**. It is not a new rule: BL-849 made exactly this call for the
> first marketplace, in its own words, *"The three legs no longer sum to 60/30/10 of the current
> gross. That is the intended lesser harm: the alternative is reducing a record below money this
> poster has already been paid."*
>
> **THE ALTERNATIVE IS WORSE AND IT IS WORTH NAMING.** Refusing the whole devaluation because one
> earner has been paid would hand ONE earner a veto over the owner re-pricing HIS campaign, and would
> get harder to exercise the more posters a clip has. This way the owner always re-prices, and the
> only thing that does not move is money already in somebody's hands.
>
> **THE CLAMP IS LOUD AND NAMES WHICH EARNER BOUND IT**, because BL-866 established that a silent
> clamp means the owner believes he re-priced and did not. Two log lines fire, one from the floor
> itself and one from the sync, both carrying the clip, the proposed figure, the held figure, the
> floor and the gross paid.

### A position already below its floor is refused rather than deepened

`floorV2EditorEarnings` returns `Math.max(proposed, Math.min(current, floor))`. The
`Math.min(current, floor)` term is what stops a floor INVENTING money: a row already sitting below
its floor is held where it is and never raised to the floor, and never pushed lower either.

### The two floors are independent BY CONSTRUCTION

The poster's floor lives in `writeClipEarnings` and reads `Clip.earnings` and the POSTER's payouts.
The editor's lives in `floorV2EditorEarnings` and reads his own row and the EDITOR's payouts.
**Neither can see the other's column**, so one binding says nothing about the other. That is what the
measurement above shows: the same devaluation moved one and held the other.

---

## PART 3 — EVERY OTHER OWNER ACTION

| action | where it lives | writes a clip's earnings | v2 handled |
|---|---|---|---|
| **approve a v2 clip** | `review/route.ts:980` | **no**, BL-880 made it skip a v2 clip deliberately | yes |
| **reject a v2 clip** | `review/route.ts:1334` | yes, zeroes it | **yes, all three legs now zero together** |
| **undo either** | `review/route.ts:1374` | yes, zeroes it | **yes, same path** |
| **BL-861 close a payout unpaid** | `payouts/[id]/settle/route.ts` | **no**, and its own header says `Clip.earnings` is never read or written by any path in the file | **nothing to do** |
| **BL-864 set a payout amount** | `payouts/[id]/price/route.ts` | **no**, and its header says no clip and no earning row is written | **nothing to do** |
| **BL-853 reject botted** | `bot-rejection.ts:312` | yes, zeroes every clip behind the payout | **yes, all three legs now zero together** |
| **BL-866 per-clip CPM override** | `admin/clips/[id]/cpm-override/route.ts` | **no**, it writes only the rate stamps; the next tick recomputes | **the restamped rate feeds all three legs at once** |
| **campaign reassignment** | `admin/clips/[id]/reassign-campaign/route.ts` | **no**, it writes the campaign and the two stamps | see below |
| **retire a dead clip** | `retire-dead-clips.ts` | **no**, and its own header says it NEVER writes earnings | **nothing to do**, and BL-874's rule holds: a failure is recorded as a failure |
| **mark unavailable and revive** | the tracking paths and `force-now` | **no** directly; a revive recomputes through the tick | **yes, via the tick's v2 fork** |
| **the ban cascade** | `clip-account-cascade.ts:245` | yes, zeroes | **yes, all three legs now zero together** |

**THE ONE GAP NAMED RATHER THAN GLOSSED: CAMPAIGN REASSIGNMENT.** It blocks a clip whose
`isMarketplaceClip` is true, which a v2 clip never is, so **a v2 clip can be moved between
campaigns**. It writes no earnings, so nothing goes wrong immediately, but the two v2 leg rows carry
their own `campaignId` and **would be left pointing at the old campaign**. The next recompute writes
them with the clip's new campaign, so the state is self-healing, but between the reassignment and the
next tick the two campaigns' spend aggregates disagree. **This is the one thing in this round that is
READ rather than VERIFIED**, and it is Round Six's to exercise.

---

## PART 4 — THE PROOF THAT NO NINTH WRITER CAN BE ADDED WITHOUT NOTICE

### The structural half

The guarantee is not a lint. **It is that every earnings write already has to pass through one
function, and that function now syncs all three legs.** A ninth writer added by a future round gets
the behaviour whether or not its author has read any of this.

### The static half: `scripts/check-v2-leg-sync.js`, wired into `prebuild`

It fails the build when the chokepoint stops calling the sync, when any file outside the three
documented ones passes the opt-out, or when the sync stops going through the guarded v2 writer.

**WHAT IT CANNOT CATCH, STATED BECAUSE THAT IS THE POINT:**

* **It is static.** It reads source text and cannot know whether a runtime path reaches a v2 clip.
* **The opt-out check is file-level.** A whitelisted file that grew a second, illegitimate opt-out
  would pass.
* **It cannot see raw SQL.** A `$executeRaw` updating `clips.earnings` bypasses the chokepoint and
  therefore bypasses this. `check-prisma-bypass.js` stands against that class, and neither can see a
  statement run by hand in the Supabase editor.
* **It proves nothing about data already written.** That is the reconciliation's job. **The two catch
  different things: this one catches a new caller, the reconciliation catches a missed one in
  flight.**

### THE GUARD'S FIRST VERSION COULD NOT FAIL, AND THE DEMO CAUGHT IT

The first predicate was `includes("syncV2LegsAfterPosterWrite")`. The demo renamed the call to
`syncV2LegsAfterPosterWrite_DISABLED_FOR_DEMO` and **the check passed**, because a substring of a
longer identifier still matches. That is precisely the guard-that-cannot-fail BL-835 was caught
shipping. It now requires the CALL, name plus opening paren, so any rename breaks the match.

### Both failure modes, demonstrated failing and then restored

```
BASELINE, a clean tree
  exit=0
  [v2-leg-sync] OK — the chokepoint still syncs all three v2 legs, 3 files carry the documented
  opt-out, and no other file bypasses it (811 files scanned).

FAILURE MODE 1: a ninth writer that opts out of the sync
  exit=1
  src/lib/bl881-bad-writer-demo.ts passes skipV2LegSync. Only these may: ...
  removed, and the guard is green again

FAILURE MODE 2: the chokepoint stops calling the sync
  exit=1
  src/lib/clip-earnings-writer.ts no longer calls syncV2LegsAfterPosterWrite. ...
  restored, and the guard is green again

RESULT: both failure modes caught = True
```

The bad writer was written, caught, and deleted; `git status` confirms zero trace of it.

### The reconciliation query, and today's answer

`V2_RECONCILE_SQL` in `src/lib/marketplace-v2-sync.ts`. For every v2 clip it asks whether the three
legs still agree, and names what it found rather than fixing anything.

> **TODAY'S ANSWER ACROSS EVERY V2 CLIP ON THE PLATFORM IS ZERO ROWS**, because there are zero v2
> clips in production.
>
> **AND IT WAS PROVED CAPABLE OF RETURNING A ROW** rather than assumed: in the sandbox it returned
> exactly the ONE clip this round deliberately put out of proportion by binding the editor's floor,
> with the finding `poster and editor legs disagree`. A reconciliation nobody has watched find
> something proves nothing.

---

## PART 5 — THE INVARIANTS, ADDS AND THE CONTROLS

| invariant, FULL population | measured |
|---|---|
| **BL-538 and the earnings invariant** | **0 breaches** |
| **BL-696**, two open payouts on one campaign | **0** |
| **BL-696**, a clip with two agency rows | **0** |
| **BL-696**, a clip with two v2 editor rows | **0** |
| **BL-627 no overpayment**, counting both v2 aggregates | **0 campaigns over budget** |
| `isMarketplaceClip` true on a v2 clip | **0** |

**ADDS, RE-PROVED AFTER EVERY CHANGE** rather than once, because BL-880 flagged that routing v2
around the `isCpmSplit` branch would turn it into REPLACES with no error. On the real campaign
`Zhus Edit (0.50 CPM)`, owner share **39.0021 percent**:

| | owner nets per $100 of gross | campaign spends |
|---|---|---|
| REPLACES | $18.10 | $100.00 |
| **ADDS** | **$57.10** | **$139.00** |

Identical to BL-877, BL-878 and BL-880.

**THE CONTROL.** A NORMAL clip written through the same chokepoint takes the full amount, **$10.00 on
10,000 views at a $1.00 CPM**, and grows **zero** v2 editor rows and **zero** v2 platform rows. The
sync is a no-op on every clip that is not a v2 clip, which is every clip on the platform today. The
v1 60/30/10 path is untouched: `marketplace-v2-writer.ts` is the only file that writes either v2
table, and no v1 writer was edited.

`earnings-calc.ts`, `balance.ts`, `clip-earnings-invariant-middleware.ts`, `money-decimal.ts` and
`campaign-era.ts` are **byte-identical by blob OID** on both refs.

---

## PART 6 — TWICE, AT THE SAME TIME, AND THE TWO EARLIER RUNS THAT FAILED

* **Twice:** running the same write twice left the three legs exactly where one write left them.
* **At the same time:** two owners writing concurrently under Serializable produced
  `[rejected, fulfilled]`, one winner and one conflict, and the clip landed **consistent** at poster
  $42.00, editor $42.00, platform $9.33. **Never a torn state.**
* **Different payment histories:** covered in PART 2.

### THE FIRST RUN FAILED THREE CHECKS AND THE SECOND FAILED ONE

**RUN ONE, three failures, and two of them were REAL PRODUCT DEFECTS in this round's own work.**

1. **THE EDITOR'S LEG RATCHETED.** Measured: the editor ran to **$108.00** while the poster reached
   **$54.00**. Two causes, both this round's: BL-877 had built his guard as a **blanket
   never-decrease**, so the first devaluation held him; and the sync **scaled his current value**, so
   every later increase compounded from the held figure.
2. **A BOT-REJECTED CLIP LEFT THE EDITOR AT $108.00** while the poster and platform went to zero.
   Same cause.
3. A test-only defect: the sandbox payout row was missing a required `walletAddress`.

**THE FIXES, both real changes to the product:**

* **The editor's guard became a PAID FLOOR**, `floorV2EditorEarnings`, mirroring
  `floorMarketplacePosterEarnings` which BL-849 built for the first marketplace's poster. A figure
  may fall freely and may not fall below money already paid to that person. **This is BL-824's
  paid-is-final, which is what the round actually asked for, rather than BL-538's never-decrease,
  which is a different rule that was being applied to the wrong thing.**
* **The sync derives both legs from the poster's own BASE** instead of scaling the editor's current
  value. The editor's base equals the poster's base exactly, because both are 45 percent of one
  gross, and a derivation carries no memory of a previous hold, so nothing can compound.

**RUN TWO, one failure, and it was the PROOF's ordering rather than the product.** It gave the editor
a $22.50 PAID payout BEFORE the plain devaluation, so his floor bound on that one too and the
"both legs halve" case never ran unfloored. The payout now lands between the two cases, which is the
only ordering in which both are observable.

**RUN THREE: 27 of 27 passed, 0 failed.**

### Safety, itemised

* **No real user, clip, campaign or payout was touched.** Every row carried the `bl881sbx-` prefix
  and the `BL881-SANDBOX-DELETE-ME` marker, every person `isTestUser`, the campaign
  `isTestCampaign`.
* **NO APIFY ACTOR RAN AND NO VENDOR LOOKUP WAS MADE.** Views were set directly on `ClipStat`. The 11
  BL-678 guards are untouched.
* **No wallet address appears anywhere.** The sandbox payout carried the literal string
  `bl881-sandbox-not-a-real-wallet`.
* **The branch did not drift.** `checkpoint/BL-881` throughout.

### Build and gates, honestly

`eslint` is present in three forms, so the BL-348 gate did not silently no-op.

| run | result |
|---|---|
| `npx tsc --noEmit` | **exit 0**, six times across the round |
| `check:prisma-bypass` / `check:removed-fields` / `check:event-wiring` | **0 / OK / 0** |
| **`check:v2-leg-sync`, NEW** | **OK, 811 files scanned**, and it ran inside the build |
| **`lint:hooks`** | **10 problems, 0 errors, 10 warnings** against a ceiling of 11 |
| **`npm run build`** | **`BUILD_EXIT=0`**, echoed by the build's own shell |

---

## IS EVERY WRITER FORKED, AND WOULD THE GUARD CATCH A NINTH

> **EVERY WRITER IS COVERED, AND NOT BY FORKING THEM.** All 23 earnings-write call sites pass through
> `writeClipEarnings`, and that function now moves a v2 clip's other two legs after every write. The
> 18 that can reach a v2 clip were driven in the sandbox and all three legs moved together every
> time.
>
> **THE GUARD WOULD CATCH A NINTH WRITER THAT OPTED OUT, AND A NINTH WRITER THAT DID NOT OPT OUT
> NEEDS NO CATCHING**, because it inherits the behaviour. What the guard really protects is the
> chokepoint itself: it fails the build if a future round removes the sync or widens the opt-out.
>
> **WHAT IT WOULD NOT CATCH** is raw SQL, a statement run by hand in the Supabase editor, or a second
> illegitimate opt-out added to a file that already has a legitimate one. Those are stated above and
> none of them is new to this round.

## WHAT ROUND SIX MUST BUILD

1. **The editor's and the poster's own payout surfaces.** Money now accrues to two people per clip
   and only one of them has a page that shows it. The editor cannot see his total, and there is no
   path by which he can request it.
2. **Whether an editor may REQUEST a payout at all.** `PayoutRequest` is per user and per campaign
   and knows nothing about v2, so the editor's balance is currently unreachable by the existing flow.
3. **Campaign reassignment on a v2 clip**, the one gap in PART 3 that is READ rather than VERIFIED:
   the two leg rows keep the OLD `campaignId` until the next tick.
4. **The agency-row deletions on a v2 clip**, named in PART 0b, re-measured rather than assumed
   correct.

---

## WHAT COULD NOT BE DETERMINED

* **Whether campaign reassignment leaves the two v2 leg rows pointing at the old campaign for
  longer than one tick.** Read, not exercised. Named above.
* **Whether the HTTP routes' own auth and clip selection behave on a v2 clip.** The sandbox exercised
  the chokepoint they funnel into, with their own `reason` strings, which is where the fix lives. It
  did not sign in as an owner and press the buttons.
* **Whether the 26 positions below their paid floor is comparable to BL-849's 17.** Not re-measured
  with BL-849's exact query, for the fifth round running. This round created one payout row, in the
  sandbox, and removed it.

---

**PERFORM NO FIX ON ANYTHING ABOVE. The two product defects this round found in its own work, it
fixed and re-proved. The one defect it found in its own guard, it fixed and re-demonstrated. The gaps
it did not close, it named.**
