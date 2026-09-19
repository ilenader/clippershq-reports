# BL-913 — the handoff document, and the three figures that were wrong before I wrote them down

**ONE LINE:** `reports/CLIPPERSHQ-HANDOFF.md` is written, 68,121 characters, and the most valuable thing in it is not the description of the product but the three places where a report this project has been citing for weeks disagreed with the code and the code won.

AUDIT ONLY. Nothing was built, no build was run and none is claimed. No code, schema, data, config or flag changed. Read only throughout, on a live platform with real makers and posters using it.

---

## THE MODEL SPLIT, AND WHY IT WAS DRAWN WHERE IT WAS

**Five retrieval subagents ran in parallel, all on Sonnet, across disjoint spans of the reports repository.** Their instructions were identical in one respect: return a VERBATIM QUOTE and a filename for every claim, say NOT STATED rather than infer, and open no database connection. They were told explicitly that a paraphrase was useless to me because I would verify each claim myself.

| Span | What it was asked for |
|---|---|
| BL-877 to BL-883 | the money foundation, the split, the chokepoint, duplicates |
| BL-884 to BL-895 | schema drift, strikes, the role lock, bonuses, access rules |
| BL-896 to BL-910 | the launch, concurrency, the dashboard, the live funnel |
| all 222 clippershq reports | a targeted sweep for the recurring failure patterns |
| BL-627, BL-824, BL-870 to BL-873, BL-899, BL-900 | budget, paid-is-final, deletion discipline |

**I read BL-876 territory, all the load-bearing source files and every database figure myself**, on Opus, and wrote every word of both documents. No subagent text was copied. Four of the five returned; the sweep across all 222 reports had not returned when the document was finished, and the document does not depend on it, which is stated below rather than hidden.

**Connections held: one at a time, mine, never concurrent.** Every database figure came from `node scripts/run-select.js`, which opens one connection and closes it. **Subagents opened zero.** No vendor call was made and no Apify actor was run.

### Every subagent claim used in the document is marked, and three were wrong

Following the rule that a document built on a relayed summary encodes its errors permanently, nothing load-bearing went in on a subagent's word.

| Claim | Status |
|---|---|
| the split constants are 45/45/10 | **VERIFIED** — read `marketplace-v2-earnings.ts:61-63` myself |
| ADDS is the live mode | **VERIFIED** — `:108`, and `v2AgencyEarningApplies()` at `:119` is its only reader |
| the side lock is **platform wide** | **WRONG, and it is the most dangerous one.** One agent returned BL-893's "PLATFORM WIDE, AND BOTH YOUR SENTENCES ARE BUILT" verbatim and correctly. The quote is real and the behaviour it describes is **gone**. `marketplace-v2-side.ts:71` records that BL-903 **deleted rule one**, and `:277` reads "RULE ONE IS GONE. THE SIDE IS DECIDED PER CAMPAIGN." A document carrying that agent's answer would have taught every future session the opposite of the live rule. |
| no word count on a switch request | **WRONG.** Same agent, honestly reported as NOT STATED in its span, and it is not in BL-893. The code has `V2_SIDE_REQUEST_MIN_WORDS = 50`. Absence from a span is not absence from the product. |
| the $163.94 / $82.04 pair does not exist | **WRONG in the span, right about the span.** One agent reported NOT FOUND across BL-877 to BL-883 and was correct; those reports print $139.00 and $57.10. The figures are in the shipped code at `v2-dashboard-panels.tsx:785` and `marketplace-v2-owner-dashboard.ts:500`, and they are the correct ones. See below. |
| "twelve guards shipped unable to fail" | **VERIFIED AT TWELVE, on the second pass.** See the amendment below; the first draft said "at least ten" and was itself an undercount. |
| "unnoticed for twenty rounds" | **NOT STATED anywhere.** What is stated is "has existed since v2 could write money at all." The document uses that instead. |
| 99 directories, 85 removed, 14 left; 1,614 files deleted, 3,106 preserved | **VERIFIED** by quote, and used |

---

## THE THREE FIGURES THAT WERE WRONG, WHICH IS THE ROUND'S REAL FINDING

### 1. The owner's cut per $100 of gross: three reports printed $139.00, and it is $163.94

This is the number the owner was given for what a marketplace campaign costs him, and it has been wrong in the record since BL-878.

BL-878, BL-880 and BL-881 each printed, for the real campaign `Zhus Edit (0.50 CPM)`: ordinary cut **$39.00**, campaign spends **$139.00**, owner nets **$57.10**. BL-880 and BL-881 each declared the figures "identical to what BL-877 and BL-878 printed," which is true and was mistaken for confirmation. **Three rounds repeated one arithmetic error and each cited the previous one as its check.**

The campaign carries `lockedOwnerShareDecimal = 0.39002074`. Those rounds read it as a share **of the clip's gross**, giving $39.00. It is the owner's share **of the total campaign spend**.

Verified against the live database rather than reasoned about:

```
clipperCpm 0.5   ownerCpm 0.3197
ownerCpm / clipperCpm              = 0.639400
s / (1 - s)  where s = 0.39002074  = 0.639400     <- identical
ordinary cut per $100 gross        = $63.94
campaign spends                    = $163.94
owner nets  10 + 63.94 + 8.10      = $82.04
63.94 / 163.94                     = 0.39002      <- s recovered
```

`calculateOwnerEarnings` at `earnings-calc.ts:450` computes `clipperGross × (ownerCpm / clipperCpm)`, and `calculateOwnerEarningsGuaranteed` at `:507` computes `clipperGross × s/(1−s)`. **Both give $63.94 on this campaign**, so the figure does not depend on which branch runs, and `guaranteeOwnerSplit` is true so the second one does.

BL-902 corrected this and the shipped code and dashboard have carried $163.94 and $82.04 since. **The header comment of `marketplace-v2-earnings.ts` still carries the wrong shape** as a $133.33 / $51.43 illustration at a nominal 33.33 percent, flagged inside the file as the other reading. Reported, not changed; this round touched no code.

### 2. "Zero posts" is out of date, and the product moved while the brief was being written

The brief describes the funnel as ending at **zero posts**, which is what BL-910 measured and was true on the first day.

Queried at 13:04 UTC on 19 September: **six posts exist**, the first at 08:25:53 and the most recent at 09:58:53 this morning, from **two distinct posters**. Eighteen marketplace clips now exist from three makers, twelve approved, three pending, three rejected.

Both money legs still read **$0.00**, which is correct rather than broken: a post earns nothing until views accrue on it.

So the platform crossed the milestone every round since BL-905 has been waiting for, and no round had looked. The document states today's figures and says plainly that the first-day funnel is a separate, historical measurement.

### 3. The unique index that was missing is now present, and I checked rather than assumed

BL-902 found `@@unique([v2ClipId, clipAccountId])` absent from `pg_indexes` entirely, after a comment claimed it had been applied concurrently, and measured the cost: one poster posted the same clip from the same account three times, all three returned 201, and each paid a full poster leg plus the maker and the platform again.

`marketplace_v2_posts_v2clipid_clipaccountid_key` **exists today**, confirmed in `pg_indexes`, alongside the application branch that gives the person a sentence instead of a constraint name. Both halves are live.

---

## WHAT THE DOCUMENT CONTAINS

`reports/CLIPPERSHQ-HANDOFF.md`, **68,121 characters, 11,157 words, 701 lines**, above the fifty thousand asked for because the marketplace section and the mistakes section both earned their length.

Eight parts: who and what; the architecture including why `prisma migrate` is never used and which six files are protected and why; the money model with the real fee, express, trainer and bonus arithmetic and every invariant named by what it prevents; **the marketplace in the greatest depth**; the state of play today; the working method; the mistakes with their numbers; and what it does not cover.

Every figure in it was verified against code or the database, or is marked unverified. The two marked unverified are the twelve-guards count and the twenty-rounds duration, both above.

**Checked before shipping:** 0 email addresses, 0 wallet-shaped strings, 0 raw user ids, 0 dash bullets. The one occurrence of "Serbia" is the rule forbidding it on a frontend page. The domain appears only as clipershq.com, one P.

### What it says about the marketplace, in one paragraph each

The per-campaign lock and the deleted platform-wide rule, with what the per-campaign rule costs stated rather than hidden. The fifty-word switch request the owner answers himself, and why it is a word count and not a character count. The 45/45/10 split, why the order of operations is not a choice, why the platform leg is a residual, and the $0.013 defect that 45/45 can have and 60/30 cannot. That a bonus multiplies only its own earner's leg, sits outside the residual, and caps at 25 **per earner** so one clip can carry 50. The ADDS decision with $163.94 and $82.04 and the explanation that ADDS moves nothing from the earners and only changes what the campaign pays for the same views. The duplicate rule both ways, with the two guarantees behind the one-post-per-account refusal and why there are two. The three campaign types from the enum. Manual strikes with exactly one creation site and a guard that fails the build at anything but one, with no ban scalar because the ban is a read-time count. The conversion action, why it exists (a conversion pays the maker and a strike only punishes the poster), and what happens to money already paid. And what each of the three people sees, with the subtraction reason spelled out: publishing the gross and one earner's 45 percent publishes the other two legs by arithmetic.

---

## WHAT I COULD NOT DO, SAID PLAINLY

**The fifth subagent had not returned when the document was first published.** It was sweeping all 222 clippershq reports and took 503 seconds and 70 tool calls. It returned afterwards, everything load-bearing in it was verified against the report files by hand, and **both documents were amended and republished.** What it changed, and the first item is the one worth reading:

**THE DOCUMENT HAD UNDERCOUNTED, FROM THE SAME SOURCE, IN THE SAME DIRECTION AS THE DEFECT IT WAS DESCRIBING.** The first draft said "at least ten" guards had shipped unable to fail, and marked the brief's twelve as unreconcilable, because the reports' own running tally stops at ten. The sweep found **twelve individually described instances** (BL-835, BL-881, BL-882, BL-883, BL-884 twice, BL-885, BL-887, BL-888, BL-896, BL-898 twice), and showed **why** the tally is wrong: BL-896 shipped one without numbering it and BL-898 then reused "the tenth." A section about enumerations coming back short had inherited a short enumeration and repeated it. Verified by reading BL-835 and BL-887 directly, both of which describe their instance in full. It is twelve.

There is also a false twelve in the corpus and it is worth naming so nobody merges them: BL-886 speaks of being **"the twelfth guard in `prebuild`"**, which counts guards *wired into the build*, an unrelated number. The document now says so explicitly.

**The enumerations count is six, not seven.** The brief said seven. The sweep found six and flagged the seventh as unsourceable; reading BL-813:18 and BL-734 resolves it — "a truncated count once reported 5 hits here where the real number was 112" is BL-734's own disclosed near-miss, not a separate episode. Six it is, and two of them were new to the document: three rounds counting one scattered value as four, then five, then finally **seven, with copies six and seven found by neither and copy seven live and clipper-facing**; and a `-E` alternation that returned 112 hits and **silently dropped a route through shell escaping of `\$10`**, which is the `head` truncation failure arriving through a different door.

**Three sections gained their real examples**, all verified verbatim before use:

* *A list that filters only the rows it loaded* had been the document's weakest entry, carried on a generic description of the `take:` trap. It now carries the measured case: the owner shown **4 of 46** while his dashboard correctly counted **47 PENDING**, because the status filter was a client-side filter over 30 already-loaded rows that was never sent to the server, leaving him **8.7 percent of his pending queue, 0 percent of his flagged one, and 41 real clips unreachable for 73.5 hours**. Plus an admin user page computing the unpaid balance tile from the newest 50 of 870 clips.
* *Money computed in a new place* gained the case where it **reached backwards**: a self-heal recomputing every approved unpaid clip without the PWA bonus and writing the lower figure, with nothing flooring the drop, so a clipper who went quiet for two days had already-earned money reduced.
* *A failure recorded as a fact* gained the exact code: a `/not found|no results|private|removed|unavailable/i` regex at `tracking.ts:3131` run against an exception message, which zeroes earnings, currently statically unreachable rather than merely disabled, and correctly described in its own round as still being a loaded gun pointed at the money path.

**This is the round's own instance of PART SEVEN item 9.** I published a document, a slower source arrived, and it corrected me. Had I treated the first four agents' coverage as complete because it was sufficient, the handoff would have shipped teaching the next session a number that was wrong in the direction the document warns about.

**I did not read all 222 reports.** I read the forty most recent through subagents with verification, plus BL-627, BL-824 and the two deletion rounds, plus every source file that decided a fact. Reports older than BL-627 are represented only where a later round cites them.

**I did not verify the launch funnel's 1,551 emailed and 19 arrived against the database.** They are quoted from BL-910 and attributed to it as a first-day measurement. Everything in the live-state table beside them was queried today.

**The accessibility agents were not invoked.** This round wrote no user-facing code of any kind: two markdown files in a reports repository, no component, template or stylesheet.

---

## CONTAINMENT

Worktree `C:\w913` on branch `checkpoint/BL-913`, created from `main` at `933cbeec`, **removed at teardown and verified by listing the path**.

Both repositories were fetched and pulled to `main` before anything was read. The ClippersHQ repository was **read only**: no file in it was created, changed or deleted, and the branch carried **0 commits beyond main** when it was deleted. Only the reports repository received the two documents.

**The tree is shared and another session was in it, which is worth recording rather than glossing.** `git status` shows two untracked files under `scripts/`. Neither is mine: `bl-799-referral-code-ledger.json` was written on 2026-08-12 and was already there at session start, and `scripts/migrations/BL-912-activate-v2-tracking-jobs.sql` was written at **14:53 today by BL-912**, which holds its own worktree at `C:\b912`. That worktree is not mine and was left alone. It also explains the six posts measured above: a parallel round is activating tracking jobs on the marketplace clips while this one was reading.

No database write of any kind. One pooled connection at a time, mine, none concurrent, none held. No vendor call, no Apify actor, no email sent by this round other than the standing owner build notification.
