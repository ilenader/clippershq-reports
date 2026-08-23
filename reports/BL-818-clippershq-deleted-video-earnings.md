# BL-818 — a clipper is no longer shown money from a video that is gone

**2026-08-23 · DB `now()` = `2026-08-23 15:25:18.059832+00` (first read) to `2026-08-23 16:07:00.759051+00` (last) · BUILD AND MERGE.**
Base `origin/main` @ `484e4d69`. Branch `checkpoint/BL-818` @ `2c044b82`. **Merged to main and verified pushed: `origin/main == local == a457637f`.** Tags `pre-BL-818` (`484e4d69`), `post-BL-818` (`2c044b82`), `pre-BL-818-merge` (`484e4d69`) and `post-BL-818-merge` (`a457637f`), all four confirmed on origin by `git ls-remote`. Isolated worktree `C:/w818`, a short path, `node_modules` never junctioned, removed at the end. Every database read through `scripts/run-select.js`, which refuses a write keyword before it connects; every timestamp cast `::text` against DB `now()`. Handles redacted to an 8 character id prefix plus an `md5` short id; no wallet address selected or printed.

**A REDEPLOY ON RAILWAY IS REQUIRED BEFORE ANY OF THIS IS LIVE.**

> **DISPLAY ONLY, and proven so rather than asserted. Zero write calls in 662 added lines. The 6 money files plus `tracking.ts`, `campaign-era.ts` and `earnings-never-decrease.ts` are byte-identical by blob OID on BOTH refs. Stored approved earnings $13,987.36, 6,001 approved clips, 189 payout rows, invariant violations 0 and the newest payout `updatedAt` are all identical before and after.**
>
> **The accessibility review ran BEFORE any UI was written and it changed what shipped. It found two CORRECTNESS defects, not styling ones, and its verdict on my draft was no-ship. Both were verified against live data before I acted, and one of its proposed fixes was wrong in a way the data showed.**
>
> **BL-817's clipper now reads `Counted $21.14` above `$26.70 earned, $5.56 of it on 3 clips that are no longer earning`. The subtraction closes to the cent, and he clears the $20.00 minimum on BOTH his campaigns today.**

---

## PART 0 — THE DESIGN SKILL, AND WHY IT DID NOT PICK AN ANCHOR

The `frontend-design` skill was read before any UI. Its first instruction is to pick one of eight aesthetic anchors and commit to its tokens. **That step does not apply here and applying it would have been the category error the skill itself names.** This round makes surgical edits inside a shipped design system that CLAUDE.md already specifies down to the hex: dark theme with a live light theme, `#2596be` accent, CSS variables for every colour, lucide icons only. Introducing a second anchor into four existing components is exactly the hybridising the skill forbids.

**The clause that does govern this round is §2, "Content is not design."** Every string below names real information, uses standard UI copy for standard actions, and invents no filler. It is quoted in full in PART 1 and PART 2 so it can be judged rather than trusted. Token fidelity here means fidelity to the EXISTING system, and PART 6 records the two new tokens and why each reuses a hex the repository already ships.

---

## PART 1 — ONE HONEST FIGURE, AND THE SUBTRACTION ON SCREEN

### The decision, and why this shape

The owner's rule was that a clipper must not be shown money he cannot have. The brief offered "the reachable figure as the headline with the deleted-video amount stated separately beneath, or something clearer". **That is what shipped, with one addition that turned out to matter more than either number: the headline now carries a LABEL.**

BL-817 established that the arithmetic was never wrong. Both figures were correct. The defect was that the campaign row printed a bare accent number with no word attached, two lines above a different bare number, and nothing on the page related them. Making the headline reachable without labelling it would have replaced one anonymous figure with another.

So the row states three things and they form a subtraction a clipper can check in his head:

| | |
|---|---|
| the labelled headline | **`Counted` · `$21.14`** |
| the reconciling line under it | **`$26.70 earned, $5.56 of it on 3 clips that are no longer earning`** |
| the existing BL-765 reminder, unchanged | `$21.14 of $20.00 minimum` (absent here: he now clears it) |

`26.70 − 5.56 = 21.14`. **Both halves are accumulated in ONE loop over ONE array** (`EarningsPremium.tsx:116-152`), so `counted + notCounted === earnedGross` holds by construction rather than by two scopes happening to agree. That is the specific failure BL-817 diagnosed and it is now structurally impossible on this row.

### Every string shipped, quoted

**The hero note** (`EarningsPremium.tsx:236-244`), which BL-698 shipped without an amount:

> **$8.48 of your earnings is not counted in this balance, because those clips are no longer earning. Money you were already paid stays yours. Your other clips keep earning as normal.**
> *See which clips*

**The stat tile** (`:295-315`), first of the trio:

> `COUNTED` · **$511.29** · *of $519.77 earned*

**The campaign row** (`:456-497`), rendered only when something is excluded:

> `COUNTED` · **$21.14**
> $26.70 earned, $5.56 of it on 3 clips that are no longer earning

**The card footer** (`:600-608`), stated once for the whole list:

> $8.48 of this period is on 44 clips that are no longer earning. ***See which clips***

**The one spoken sentence per row** (`:519-556`), which is what a screen reader actually hears:

> "23 clips, $26.70 earned in the period shown. $5.56 of that period total is on 3 of them, which are no longer earning, so $21.14 of this period counts. Money you were already paid stays yours. All time: your balance on this campaign is $21.14, which clears its $20.00 minimum, so you can request a payout on it."

Three wording rulings came from the accessibility review and all three are in that sentence. **"of that period total", never "less"**: an operator invites the listener to carry the result forward into the balance clause, and those are different scopes. **"3 of them", not "3 clips"**: the clip count was already spoken at the start of the same sentence. **"All time:" unconditionally**, including when the two figures coincide, so the distinction never depends on the numbers differing.

`belowMinimumMessage` was **not edited**. It is the string the server gate itself returns when it refuses a request (`payout-minimum-shared.ts`), and BL-688 cost a round to two copies of one sentence drifting apart. The "All time:" prefix is added at the call site.

### What the tiles do now, and the fourth tile that was rejected on measurement

`earnings/page.tsx:157-201` excludes not-counted clips before summing, applying the **same predicate `/api/earnings` applies at `route.ts:209`** to build `payableClips`. It is applied to the approved sum AND the pending sum, because `Earned = Approved + Pending` is an identity a reader can check on screen and excluding from one side only would break it. The server filters once, before computing either; the client now does the same.

A fourth tile was considered and **rejected on a measurement, not a preference**: `grid-cols-4` gives a 38.5px inner box at 320px, which clips `$0.00` and needs a 483px viewport; `grid-cols-2` fits but adds 93.82px of height to every clipper's page whether or not anything is excluded. A sub-line inside the existing tile costs height only for the clippers it concerns.

### The row is kept even when everything on it is excluded

The filter that decides whether a campaign row renders is `earnedGross > 0`, not the counted figure (`:154-160`). A campaign whose every clip is excluded still has something to say, and dropping the row would make the money vanish silently, which is the defect one layer deeper rather than a fix for it.

---

## PART 2 — WHICH CLIP, WHICH CAUSE, AND A ROUTE BACK

### The flag has FOUR writers, and the shipped card branched on two

BL-698 found two causes and wrote two sentences. **The accessibility review found the other two, and I verified each in the source before acting.**

| # | writer | what it means | earnings |
|---|---|---|---|
| 1 | `retire-dead-clips.ts:381-384` | the video really is not reachable | **left intact**, "reversible freeze ONLY" |
| 2 | `tracking.ts:3204-3211` | transient-unavailable retry path | **zeroed** via `writeClipEarningsZero` |
| 3 | `clip-account-cascade.ts:243` | the ACCOUNT was suspended; the video is usually still live | **zeroed** the same way |
| 4 | `override/route.ts:293` | the OWNER deleted a marketplace listing | left intact |

**Writer 4 had no copy branch at all**, so that clipper was being told his video was gone when the owner had removed a listing. It has its own sentence now. Measured today: 0 clips sit on a `BANNED` account and 0 excluded clips are marketplace clips, so branches 3 and 4 carry no rows. They are written anyway, because the alternative is copy that becomes a false accusation the first time one appears.

### The amount, and where the review's own fix was wrong

The review's first blocking item was that the excluded amount cannot come from `clip.earnings` alone, and it proposed `(earnings || 0) + (savedEarnings || 0)`. **The first half is right and the fix is not, and the data is why.** Measured at `2026-08-23 15:39:04+00`:

| | |
|---|---|
| excluded approved clips | **774** |
| of those, still carrying their earnings | **452** |
| of those, zeroed at the source | **322** |
| of the 774, carrying a non-null `savedEarnings` | **6** |
| what those six `savedEarnings` sum to | **$0.00** |

`savedEarnings` recovers nothing. **And it should not be reached for**, because a zeroed clip contributes $0.00 to the earned total AND $0.00 to the payable total: it creates no discrepancy, so there is no amount to explain. Naming a figure there would put a number on screen that reconciles with nothing, which is BL-698's nine-times error in miniature. So `notCountedAmount` returns the clip's own earnings and the card renders the sentence **without a figure** when it is zero. That is both correct and exactly the amount the campaign row subtracted for that clip.

### The exact copy, all three causes

**Video not reachable** (the only branch with live rows today):

> **This video is not reachable, so this clip is no longer earning. The $2.50 it earned is not counted in your balance. Money you were already paid stays yours.** *If yours is still up, send us the link on Discord and we will look at it again.*

**Account suspended:**

> **Clippers HQ has suspended the account this clip was posted from, so it is no longer earning. Your Clippers HQ login is not affected.**

**Listing removed:**

> **The listing this clip was made for has been removed, so this clip is no longer earning. Nothing about your video has changed.**

Alongside, the money treatment: **`$0.00 COUNTED`** with **~~$2.50~~ earned** struck through beneath it.

**Five wording changes came from the review and each removes a specific harm.** *"Videos can stop being available for lots of reasons"* is **deleted**: an unspecified hedge makes the reader supply the cause, and the cause he supplies is that he is being accused of taking it down. *"we will check it"* became *"send us the link on Discord and we will look at it again"*, because the sweep excludes finished campaigns and a promise to check is not always keepable. *"This account is suspended"* collided with the login page's suspension copy and now names Clippers HQ as the actor and says the login is unaffected. *"payable"* became *"counted"*, so a clipper does not learn two vocabularies for one fact. And the word **"retired"** appears nowhere clipper-facing.

**Nothing implies the clipper did anything.** Every sentence is agentless about the video, names Clippers HQ explicitly where Clippers HQ is the actor, and none of `removed`, `deducted`, `taken`, `docked`, `lost`, `forfeited` or `clawed back` appears anywhere in the diff.

### The route back, and finding the clips

BL-751 and BL-748 both found live videos wrongly read as gone, and BL-720 narrowed the verdict because of it. A clipper marked in error must have somewhere to go, and the Discord line is it.

Finding the clips was the other half. A clipper with 300 clips cannot locate 3 of them by scrolling, and the earnings page sends him to `/clips` to do exactly that. The live list (`ClipsPremium.tsx`, and the block at `clips/page.tsx:355-380` is dead code behind a const `true`) now carries a banner and a toggle:

> **Across all your clips, 44 clips are no longer earning and the $8.48 they earned is not counted in your balance. Money you were already paid stays yours.** · **[ Show only these ]**

**"Across all your clips" is not decoration.** The earnings figure is scoped to a 15 or 30 day window and this one is not; without the scope in words the two look like a contradiction.

The toggle is a real `aria-pressed` button in the banner and **deliberately not a fifth status chip**: those clips are APPROVED and would still be APPROVED afterwards, so putting it in the status group would stop the four chips partitioning the list and `counts.ALL` would quietly cease to be the sum of the others. The empty-state recovery clears BOTH narrowings, so a clipper who combines "Rejected" with "Show only these" is never stranded on an empty view with the recovery button already pressed.

### 308 rejected clips that were being told the wrong thing

`isNotCounted` also tests the status, and that is not cosmetic. **308 REJECTED clips carry the flag and every one holds $0.00.** A rejected clip earns nothing because it was rejected, so telling that clipper it is "no longer earning because the video is not reachable" names the wrong cause, and it padded Clipper K's banner from 44 to 48. **It cannot move a dollar**: `computeBalance` already sums APPROVED only (`balance.ts:164-170`), so a REJECTED clip contributes $0.00 on both sides with or without the line. Rendered before and after: the banner went from `48 clips` to `44 clips` and the amount stayed `$8.48`, which is the hero's figure exactly.

---

## PART 3 — THE OWNER'S VIEW, ON A SURFACE THAT ALREADY EXISTED

**It went on `/admin/liability`, not a new page.** That surface already owns the `retiredUnpaid` bucket in the platform waterfall, so a second screen would be a second place the same dollar is stated, and BL-734 cost a round to a value that lived in seven places and was stale in two. Everything added is derived from the SAME cells as the campaign table, so the two cannot disagree.

A new section, **"Nobody is paid for a video that is gone"**, plus clip and clipper counts folded into the per-campaign breakdown that previously stated money alone.

### The live figure

Read from `computeLiability`, **the same module the page calls**, at `2026-08-23 16:06:57+00`:

| | |
|---|---|
| excluded clips | **774** |
| clippers holding one | **71** |
| earnings on them, gross | **$3,631.71** |
| **what the exclusion actually removes from a displayed balance** | **$492.21 gross, $458.59 cash** |
| clippers whose balance is reduced | **34** |
| the difference between the two | **$3,139.50**, already paid out while those videos were live |

**Two figures per clipper, and the difference is the whole point.** One clipper holds **$1,329.31** of excluded earnings of which **$15.45** is money he can no longer reach; he was paid for the rest while the videos were live. Reporting the gross as if it were the second would tell someone paid in full that he lost money he in fact received. That is the error BL-698 caught in review at nine times the true figure, and it is why `removedFromBalance` is computed here the same way `earnings/route.ts:224-226` computes it: two floored balances subtracted, never the raw total.

### Per campaign

| campaign | status | clips | clippers | earnings |
|---|---|---|---|---|
| somesome | PAST | 327 | 32 | **$3,409.83** |
| GainzAlgo (REPOST CAMPAIGN) | PAST | 169 | 13 | $71.70 |
| bees.n.honey | PAST | 61 | 9 | $44.03 |
| Panic Baby | PAST | 66 | 8 | $43.20 |
| WinGram | PAUSED, archived | 43 | 13 | $19.07 |
| Zhus Edit (0.50 CPM) | ACTIVE | 25 | 9 | $17.97 |
| Zhus Meme (0.20 CPM) | ACTIVE | 44 | 8 | $12.86 |
| SomeSome App | ACTIVE | 21 | 1 | $8.60 |
| STRAENGE | PAST | 16 | 4 | $4.15 |
| BAD BITCH ANTHEM (0.50 CPM) | PAUSED | 2 | 2 | $0.30 |

### The largest holders, redacted

| id8 | md6 | clips | campaigns | on those clips | comes off his balance |
|---|---|---|---|---|---|
| `cmps3tgl` | `3159ac` | 16 | 1 | $147.61 | **$147.61 gross, $141.71 cash** |
| `cmponzpo` | `20d221` | 15 | 2 | $65.24 | $65.24 gross, $62.63 cash |
| `cmpfozzs` | `540fef` | 100 | 6 | $59.75 | $43.29 gross, $39.39 cash |
| `cmpbazci` | `71108c` | 4 | 1 | $34.24 | $34.24 gross, $31.16 cash |
| `cmpe951o` | `5185f3` | 2 | 1 | $34.23 | $34.23 gross, $31.15 cash |
| **`cmp7153e`** | **`3a8763`** | **48** | **1** | **$1,329.31** | **$15.45 gross, $14.06 cash** |

The last row is the one that justifies stating both figures.

### Against BL-817's measurement

BL-817 measured **27 clippers seeing 40 disagreeing campaign rows worth $2,908.06 absolute**. Re-measured today at `15:35:59+00`: **86 rows rendered across 56 clippers, 39 disagreeing across 27, $2,899.75 absolute.** Ordinary six-hour drift, same population.

**This round fixes the deleted-video component of that and says plainly what it does not fix.** Of the 39, **17 rows across 12 clippers carry an excluded amount totalling $85.85**, and the fix **fully reconciles 9 rows worth $46.65** where retired money was the only cause. The other 30 rows disagree for reasons this round deliberately does not change: **$2,697.66 is money already paid out** and **$287.91 is locked in a pending payout**, both of which the clipper genuinely did earn and genuinely did have. For those rows the answer is the LABEL, not a different number: `Counted` on one figure and `of $20.00 minimum` on the other means a reader can no longer mistake a period total for a balance. Erasing already-paid earnings from an "earned" figure would be a new lie, not a fix.

---

## PART 4 — HOW THE OWNER FIXES A WRONG ONE

**A route already exists. It is one button and it was never documented anywhere the owner would find it.**

> **Admin → Clips → open the clip's tracking panel → "Force Now (debug)".**

| step | file:line |
|---|---|
| the button | `tracking-modal.tsx:290-301`, owner-only, behind a confirmation at `:364-371` |
| the request | `POST /api/admin/clips/[id]/force-now`, `tracking-modal.tsx:176` |
| the gate that ALLOWS an excluded clip | `force-now/route.ts:153` — *"Q5/E5: videoUnavailable=true ALLOWED (revival path)"* |
| what reverses the mark | `tracking.ts:1730-1747` clears `videoUnavailable`, clears `videoUnavailableSince`, clears `savedEarnings`, then the standard recompute writes fresh earnings through `writeClipEarnings` |
| the success signal | `force-now/route.ts:227` sets `revived`; the modal shows **"Clip revived!"** at `tracking-modal.tsx:185` |

**"Track Now" is the wrong button and refuses on purpose**, at `track-now/route.ts:174-177`, with `VIDEO_UNAVAILABLE` and the message *"Video is unavailable — track-now will not help"*. The two controls sit next to each other, which is worth knowing before the owner tries the obvious one.

**Nothing automatic will ever undo it.** The daily sweep excludes these clips at the where clause (`tracking.ts:3593`, `videoUnavailable: false`), so a clip in this state is never re-polled on any campaign, whatever its status. Force Now is the only door.

### What is NOT built, and why

**A bulk re-check across the 71 affected clippers is specced here and deliberately not built.** Reversing the mark restores earnings through `writeClipEarnings`, which makes it a MONEY change and not a display one, and this round's absolute rule was display only. The spec, for its own round:

1. **Owner-only, preview first.** Reuse the BL-728 blast-radius pattern: state clips, clippers and dollars that WOULD revive, computed by the same code that then executes, before anything is written.
2. **Route through `writeClipEarnings` only.** It is the L1 budget hard-lock and the invariant chokepoint; a direct `clip.update` on the four invariant fields is forbidden.
3. **BL-538's never-decrease guard stays ON** (`earnings-never-decrease.ts`). A revive that recomputes BELOW the stored value must be blocked and recorded as blocked, never silently written.
4. **Cost is the real constraint.** 774 clips is 774 Apify calls at minimum, and the 11 BL-678 spend guards must be honoured. Batch it, cap it, and report what was skipped rather than silently truncating.
5. **Expect most to stay gone.** BL-698 measured only 1.2% of retired money sitting where recovery is even possible, and $3,409.83 of today's $3,631.71 is on `somesome`, a PAST campaign where `campaignStatusBlocks` refuses every further earnings write even if every video returned.

---

## PART 5 — NOTHING MOVED, MEASURED BEFORE AND AFTER

### Structural: the round cannot write

| check, on the 662 added lines | result |
|---|---|
| `db.*.update / updateMany / create / createMany / upsert / delete / deleteMany` | **0** |
| calls to `writeClipEarnings` | **0** (one mention, inside a comment naming another file) |
| `$transaction` | **0** |
| `fetch` with POST, PATCH, PUT or DELETE | **0** |
| dashes used as bullets | **0** |
| hardcoded hex in the changed `.tsx` | **0** (two mentions, both inside comments explaining why a token exists) |

### Measured: the same query before and after

`scripts/bl818-snapshot.sql`, run at `15:31:38+00` and again at `15:59:59+00`:

| | before | after |
|---|---|---|
| stored approved earnings | **$13,987.36** | **$13,987.36** |
| approved clips | 6,001 | 6,001 |
| earnings invariant violations | **0** | **0** |
| payout rows | 189 | 189 |
| newest payout `updatedAt` | `2026-08-23 13:54:54.914` | `2026-08-23 13:54:54.914` |
| paid gross total | $10,513.69 | $10,513.69 |
| **withdrawable total / pairs** | **$2,232.78 / 32** | **$2,232.78 / 32** |
| **stuck under a minimum / pairs** | **$547.62 / 157** | **$547.62 / 157** |

The newest payout `updatedAt` predates the round's first read by 90 minutes, so **no payout was created, modified, approved, cancelled or paid.**

**One thing moved and it was not me, and it is reported rather than smoothed.** A fingerprint hashed over every (clipper, campaign) pair changed between the two reads while every dollar aggregate stayed identical. Cause, measured: **4 real clips were submitted by real clippers between `15:52:29.630` and `15:56:44.078`**, on 2 distinct (clipper, campaign) pairs, **all still PENDING and all carrying $0.00**, and **0 clips were approved during the round**. Two new zero-valued rows enter the pair set, which changes the string the hash is taken over and changes no money at all. That is why every total, every pair count on the money side and the invariant are unchanged.

### The money files

`git rev-parse main:<file>` against `git hash-object <working tree>`, on both refs:

| file | blob OID | |
|---|---|---|
| `clip-earnings-writer.ts` | `ac5be7deb061` | **IDENTICAL** |
| `earnings-calc.ts` | `797e20985ad5` | **IDENTICAL** |
| `balance.ts` | `e887f80acfc7` | **IDENTICAL** |
| `tracking.ts` | `83ce4babfd39` | **IDENTICAL** |
| `clip-earnings-invariant-middleware.ts` | `61cef3939536` | **IDENTICAL** |
| `money-decimal.ts` | `ef5cdae757b9` | **IDENTICAL** |
| `campaign-era.ts` | `106e16ad7512` | **IDENTICAL** |
| `earnings-never-decrease.ts` | `c15145f51a56` | **IDENTICAL** |

**None of the eight appears in the diff.** BL-538's never-decrease guard is intact by construction: nothing in this round writes, so there is nothing for it to guard.

**No schema change and no `prisma migrate`.** `prisma generate` only, run after `npm ci` because `npm ci` wipes the generated client. **No Apify actor ran and the 11 BL-678 guards are untouched.**

### BL-817's clipper, the worked example

`cmrl046b` / `299618`, at `2026-08-23 16:07:00.759051+00`:

| campaign | minimum | earned | not counted | **balance** | verdict |
|---|---|---|---|---|---|
| **Zhus Edit (0.50 CPM)** | $20.00 | $26.70 | **$5.56** | **$21.14** | **can withdraw** |
| Zhus Meme (0.20 CPM) | $20.00 | $102.96 | $2.92 | $100.04 less $21.25 paid = **$78.79** | **can withdraw** |
| bees.n.honey | $10.00 | $390.42 | $0.00 | $0.00, fully paid | nothing to take |

**He can request a payout today, on both campaigns.** BL-817 found he clears the $20.00 minimum at $21.11 and had $77.99 sitting on the other campaign the whole time; both figures have since grown on ordinary accrual and both still clear. His screen now renders, verified in a browser:

> Zhus Edit (0.50 CPM) · 23 clips · **COUNTED $21.14**
> **$26.70 earned, $5.56 of it on 3 clips that are no longer earning**

and the sentence a screen reader hears, captured from the rendered DOM:

> *"23 clips, $26.70 earned in the period shown. $5.56 of that period total is on 3 of them, which are no longer earning, so $21.14 of this period counts. Money you were already paid stays yours. All time: your balance on this campaign is $21.14, which clears its $20.00 minimum, so you can request a payout on it."*

**No clip of his was touched, no status changed, no balance moved and he was not paid.**

---

## PART 6 — RENDER, GATES AND MERGE

### Rendered, and how

BL-793's method: `next dev` on port 3100 so `.env.development.local` loads and both bypass flags are true, the `dev-auth-role` cookie to pick the role, Playwright, and `window.innerWidth` printed beside every shot so a claimed width is a measurement.

**Stated plainly: for the two clipper screens the dev-bypass CLIPPER id was pointed at a real clipper's user id for the duration of the render.** The dev user `dev-clipper-001` holds 2 clips and $0.00, so the new UI would not have rendered at all. That made every figure on those screens a real read of the live database through the real routes, with no interception. **The edit was local only, reverted before the commit, and `src/lib/dev-auth.ts` has a zero-line diff against main.** The owner screen needed no such thing: it renders real platform data under the OWNER cookie.

**Fifteen full-page shots plus ten targeted ones. Every one HTTP 200, anchor found, and `scrollWidth == clientWidth` at every width.**

| screen | 320 | 375 | 414 | 1280 | 1440 |
|---|---|---|---|---|---|
| `/earnings` | 200, no overflow | 200, no overflow | 200, no overflow | 200, no overflow | 200, no overflow |
| `/clips` | 200, no overflow | 200, no overflow | 200, no overflow | 200, no overflow | 200, no overflow |
| `/admin/liability` | 200, no overflow | 200, no overflow | 200, no overflow | 200, no overflow | 200, no overflow |
| `/clips` with the toggle pressed | `aria-pressed=true`, scoped count announced | same | same | same | same |

**What I actually saw, not just measured.** At 375 the hero reads `$99.62` with the note naming `$8.48`; the trio reads `COUNTED $119.95 / of $128.43 earned`. At 1440 the same page reads `COUNTED $511.29 / of $519.77 earned`, because the timeframe default is 15 days below 1024px and 30 above it. **The subtraction closes at BOTH settings**, which is the property that matters, and it is why the bold figure stayed period-scoped rather than being swapped for an all-time balance. The clip card was captured showing `$0.00 COUNTED` over `~~$2.50~~ earned` with the full three-sentence notice. The owner section was captured with its per-clipper list.

**The `/clips` full-page shot is 102,331 pixels tall** because this clipper holds 300 clips, which is useless as an image; the top of the page was captured separately at all five widths. Reported rather than presented as a screenshot I could read.

### Gates, stated honestly

`eslint v9.39.4` confirmed present at `node_modules/.bin/eslint`, so the hooks gate is a real check and not a silent no-op. `npm ci` exit 0, then `npx prisma generate` exit 0, **before** any typecheck.

| gate | baseline, measured on this worktree before the first edit | after |
|---|---|---|
| `npx tsc --noEmit` | **exit 0**, 0 lines of output | **exit 0**, 0 errors |
| `npm run build` | **BUILD_BASE_EXIT=0** | **BUILD_FINAL_EXIT=0**, compiled in 20.8s |
| `lint:hooks` | **0 errors, 11 warnings** | **0 errors, 11 warnings** |
| `check:prisma-bypass` | | **0 violations across `src/` + `scripts/`**, including its earnings-write check |
| `check:removed-fields` | | passed |
| BL-810's harness | 20 passed, 0 failed | **20 passed, 0 failed** against the modified module |

Exit codes were echoed from `$?` into a log immediately after the command and **never read through `tail`**. The gate permits `--max-warnings 11` and sits at exactly 11, so this change had to add **zero**; the reviewer corrected an assumption worth recording, that the gate counts `exhaustive-deps` warnings rather than hooks, so a correct dependency array costs nothing. Every new derivation extends an existing memo.

**The BL-810 harness could not run at first** and the reason is worth stating: `server-only` is a Next build-time alias, not an installed package, so `tsx` cannot resolve it. A local stub in `node_modules` (never committed, removed with the worktree) plus `DOTENV_CONFIG_PATH=.env.local` makes it runnable. Without those two steps the harness fails on import and on `DATABASE_URL`, which is presumably why nothing had re-run it since BL-810.

### Merge

| | |
|---|---|
| base | `484e4d69` |
| branch | `checkpoint/BL-818` @ `2c044b82`, on origin |
| merge | `--no-ff` → **`a457637f`** |
| **merge tree OID** | **`b37f3f22cf27`** |
| **branch tree OID** | **`b37f3f22cf27`, IDENTICAL** |
| conflicts | **none**; `git grep` for conflict markers tree-wide returns **0** |
| BACKLOG | `grep -c "^## BL-"` **160 → 161**, exactly **one** BL-818 entry, never piped through `head` |
| `checkpoint/BL-723` | **NOT merged**: `git branch --contains` reports it is not in main |
| push | **`origin/main == local == a457637f`**, `safe-push` reported `VERIFIED PUSHED` and `git ls-remote` agrees independently |

**The merge tree OID equals the branch tree OID exactly**, so the branch build IS the merge build. A post-merge build was run on main anyway.

**One honest note on the push.** `safe-push.mjs checkpoint/BL-818` printed `PUSH FAILED` because it was invoked from the primary worktree, where HEAD is `main`, so it compared the pushed branch against the wrong local ref. The push itself succeeded: `git ls-remote` confirms `refs/heads/checkpoint/BL-818` and both tags at the right SHAs. The main push was run from the correct worktree and reported `VERIFIED PUSHED` cleanly.

**A REDEPLOY ON RAILWAY IS REQUIRED.**

### Accessibility

The lead reviewed the plan **before any UI was written**, coordinating the contrast, ARIA, cognitive and link specialists. **Its verdict on my draft was no-ship, and it was right.** Eight items, all applied:

**(a) The amount was wrong in two of four cases.** PART 2. Corrected, with the reviewer's own proposed fix rejected on evidence.
**(b) A third cause had no branch**, so a clipper was told his video was gone when the owner removed a listing.
**(c) A focusable link inside an `aria-hidden` subtree** on each row would be a silent tab stop with no accessible name (WCAG 4.1.2, axe `aria-hidden-focus`). The per-row link was dropped for one card-level link outside the hidden subtree, which also removes five identical link names pointing at one destination.
**(d) The hero note must not pair the count with the amount**: the count is every excluded clip and the amount is a floored delta, so "$3.31 from 12 clips" would be wrong where those 12 hold $10.44. The count is not printed.
**(e) "This period" is 15 days on mobile and 30 on desktop**, so the bold figure stays period-scoped and the reconciliation closes at both.
**(f) `Earned = Approved + Pending` had to keep holding**, so the exclusion is applied to both sums and the pending chip, and the tile that no longer shows what was earned was relabelled `Counted`.
**(g) Light-theme invisibility.** `ClipCardNew.tsx` hardcoded `text-white/60,70,80` and `bg-white/[0.04]`, which measure **1.00:1 on the light card**: the panel, the icon, the "payable" qualifier and the struck figure were all invisible there, leaving a bare `$0.00`. Fixed with the copy, along with BL-698's identical hero note, which three prior rounds each recorded and each left.
**(h)** Reported, not fixed: see below.

**Two new tokens, each reusing a hex already in `globals.css`.** `--text-quiet` (`#a1a1a8` dark, `#52525b` light) is a real de-emphasis: in the dark theme `--text-primary`, `--text-secondary` and `--text-muted` are **all `#ffffff`**, so a "muted" fragment carries exactly zero hierarchy and the reconciling clause would read as flat as the figure it explains. `--link-text` (`#2596be` dark, `#1b6f8f` light) exists because the accent is 5.42:1 on the card in dark but **3.40:1 in light** and 3.09:1 on `--bg-input`, clearing AA only as large text, and every link added here is 11px. Links are underlined at rest regardless, because the hue alone is 1.32:1 against body text. Worst measured case for the new pairs: **6.90:1 / 7.03:1** and **5.22:1 / 5.14:1**.

The below-minimum reminder's left-border marker moved from `--border-color` to `--border-strong`: the old token is **1.16:1 in dark and 1.23:1 in light**, so the block meant to separate two stacked lines was not perceivable in either theme (WCAG 1.4.11). The two lines are now distinguished structurally, which they had to be, because colour could not do it.

**Reported, NOT fixed, each in the BACKLOG:** `layout.tsx:130` ships `maximum-scale=1, user-scalable=no`, a standalone WCAG 1.4.4 AA failure affecting every page, where `app-layout.tsx:187-190` shows the code already intends to allow pinch zoom; `ClipCardNew.tsx:206-207` gives N clips from one account N identical link names pointing at different URLs (2.4.4), live for every clipper; `timeframe-select.tsx:22-33` has no ARIA at all on the control that governs this round's scope and no "All" option; `EarningsPremium.tsx:250`'s anchor is gated all-time while its target exists only when the period-scoped list is non-empty; and four pre-existing narrow-width overflows the review measured at 320px.

### One thing I fixed that nobody asked for, and why

`src/lib/liability.ts` contained **three NUL bytes**, deliberate map-key separators written by BL-810. They are not corruption, but ripgrep and grep treat the whole file as binary and **silently skip it**, so a repository-wide audit misses a money-adjacent module. I hit it twice in this round before diagnosing it. The separator is now `::`, which cannot appear in a cuid, the keys are still unique, behaviour is identical, and `grep -c` on that file returns a real number again. BL-810's harness still passes 20/20 afterwards.

---

## WHAT THIS ROUND DID NOT DO

• **It changed no stored earning, and it paid nobody.** $3,631.71 still sits on 774 clips across 71 clippers and not a cent of it became payable. What changed is that they are told.
• **It did not build the un-marking flow.** Force Now already exists and is documented above; a bulk version restores earnings and is a money round.
• **It did not fix the other reasons two figures can differ.** $2,697.66 of already-paid and $287.91 of locked money still make an earned figure differ from a balance on 30 rows. Those are honest differences between two real things, and the fix there was to LABEL them, which shipped.
• **It ran no Apify actor and spent nothing.**
• **A dev server was up on this machine for roughly forty minutes during the coding and render window.** Prior rounds recorded that a long-lived `next dev` can exhaust the Supabase connection pool and disturb a live session. It was killed by process tree before the merge and port 3100 is confirmed clear.

---

## VERIFICATION

Display only: zero write calls across 662 added lines, no stored earning recalculated, reduced or deleted, and BL-538's never-decrease guard intact by construction. Stored approved earnings $13,987.36, 6,001 approved clips, 189 payout rows, invariant 0 and the newest payout `updatedAt` all identical before and after, with the one moving fingerprint traced to 4 real clips submitted by real clippers mid-round carrying $0.00 and 0 approvals. The 6 money files plus `tracking.ts`, `campaign-era.ts` and `earnings-never-decrease.ts` are byte-identical by blob OID on both refs and none is in the diff. The two figures reconcile on screen and the subtraction is accumulated in one loop over one array, so it closes to the cent by construction; rendered and read back, `$26.70 − $5.56 = $21.14`. The wording distinguishes all four writers of the overloaded flag, three of which get their own sentence, never implies a clipper deleted anything, and gives every affected clipper a route back on Discord. The owner's view went on the existing `/admin/liability` and reports 774 clips, 71 clippers, $3,631.71 gross and $492.21 gross / $458.59 cash actually removed across 34 clippers, re-measured against BL-817's 27 clippers and 40 rows at $2,908.06, now 27 and 39 at $2,899.75, of which this round fully reconciles 9 rows worth $46.65 and labels the rest. The un-marking route exists and is named to file:line; the bulk version is specced and deliberately not built. BL-817's clipper is the worked example and can request a payout today on both campaigns. Rendered at 320, 375, 414, 1280 and 1440 with `innerWidth` printed beside every shot and no horizontal overflow anywhere. Merged to main at `a457637f` with the merge tree OID equal to the branch tree OID, zero conflict markers, BACKLOG counted 160 to 161 by `grep -c` and never piped through `head`, `checkpoint/BL-723` excluded and proven not merged, and `origin/main == local` verified twice. `tsc` and `next build` were both actually run with their exit codes echoed directly; the hooks gate is 0 errors and 11 warnings, identical to the pre-change baseline measured on the same worktree. No schema change, no `prisma migrate`, no Apify actor, no payout created, modified, approved or cancelled. Handles redacted, no wallet address printed, every timestamp cast `::text` against DB `now()`. The worktree at `C:/w818` is removed. No dashes as bullets. **A Railway REDEPLOY is required.**
